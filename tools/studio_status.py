#!/usr/bin/env python3
"""Build the Studio site's data: episode progress (status.json) and the video library (library.json).

The site is static glass over the repository. At every deploy (.github/workflows/pages.yml runs
on issue labels, issue comments, pushes to main and hourly) this reads

  - episode issues, their comments and label timelines, open pull requests and episode
    releases (GitHub REST API; GH_TOKEN or GITHUB_TOKEN if set), and
  - catalog/videos.json, catalog/bilibili.json and catalog/series.json,

and writes <out>/status.json and <out>/library.json, so the browser makes no API calls.

An episode's progress follows the stage vocabulary in AGENTS.md ("Progress on the Studio
board"): the state: labels at the end of the pipeline win; otherwise the newer of the episode's
stage label (the "▶ …" labels) and its latest CHECKPOINT; an optional "Progress: <stage> n/m"
line refines the current stage. Weights below turn the stage into an approximate percent.

  python3 tools/studio_status.py --out site/data                 # live
  python3 tools/studio_status.py --offline --out site/data       # files only: library, empty board
  python3 tools/studio_status.py --save-snapshot snap.json ...   # keep the raw API payloads
  python3 tools/studio_status.py --snapshot snap.json ...        # rebuild from saved payloads
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API = "https://api.github.com"
DEFAULT_REPO = "JunyiZhou-Conny/Explainer_Videos"
WORKER = "python3 tools/publish_worker.py --repo {repo} --upload"

# key, label, short (bar legend), weight (% of an episode's work, from the measured AC215
# cycle: digest+script ~half a day, scenes ~1 day, QA+fixes ~1 day, render+stitch ~half a
# day), and who acts at that stage.
STAGES = [
    ("brief", "素材与大纲", "素材", 10, "agent"),
    ("script", "脚本", "脚本", 10, "agent"),
    ("scenes", "场景制作", "场景", 30, "agent"),
    ("qa", "整片审查", "审查", 14, "agent"),
    ("finish", "收尾修改", "修改", 12, "agent"),
    ("render", "1080p 渲染", "渲染", 10, "agent"),
    ("stitch", "拼接与检查", "拼接", 8, "agent"),
    ("ready", "等你合并发布", "合并", 2, "you"),
    ("publishing", "等你上传 B 站", "上传", 2, "you"),
    ("published", "已上 B 站", "上线", 2, "done"),
]
INDEX = {key: i for i, (key, *_rest) in enumerate(STAGES)}

# Labels, normalised by norm_label(): the "▶ …" stage labels a session moves while it works,
# and the lifecycle state: labels. state:scripting carries no stage and is ignored.
STAGE_LABELS = {
    "制作场景": "scenes", "整片审查": "qa", "收尾修改": "finish", "渲染1080p": "render",
    "拼接与检查": "stitch", "等待合并发布": "ready",
}
STATE_LABELS = {
    "state:sample-review": "scenes", "state:full-review": "ready",
    "state:publishing": "publishing", "state:published": "published",
}
PAUSE_LABEL = "暂停"
QUESTION_LABEL = "blocked:question"

# "CHECKPOINT <stage>" marks <stage> finished, so work continues at the next one. A checkpoint
# that says it paused marks an interruption inside <stage> instead.
CHECKPOINT_NEXT = {
    "captures": "brief", "digest": "brief", "brief": "script", "script": "scenes",
    "sample": "scenes", "scenes": "qa", "qa": "finish", "finish": "render", "fixes": "render",
    "render": "stitch", "stitch": "ready", "full-cut": "ready",
}
CHECKPOINT_SELF = {"captures": "brief", "digest": "brief", "brief": "brief", "script": "script",
                   "sample": "scenes", "scenes": "scenes", "qa": "qa", "finish": "finish",
                   "fixes": "finish", "render": "render", "stitch": "stitch", "full-cut": "stitch"}
STAGE_ALIASES = {key: key for key, *_ in STAGES} | {
    "素材": "brief", "大纲": "brief", "脚本": "script", "场景": "scenes", "审查": "qa",
    "修改": "finish", "收尾": "finish", "渲染": "render", "拼接": "stitch",
}

CLAIM_RE = re.compile(r"^Claiming\.?\s*Model:\s*([^,]+)", re.I)
MARK_RE = re.compile(r"^(CHECKPOINT|HANDOFF)\b[\s:：—–-]*([\w-]*)", re.I)
BRANCH_RE = re.compile(r"branch\s+`?([\w./-]+)", re.I)
PROGRESS_RE = re.compile(r"^[ \t]*(?:[-*][ \t]*)?\**progress\**[ \t]*[:：][ \t]*\**[ \t]*"
                         r"([^\s*]+)[ \t]+(\d+)[ \t]*/[ \t]*(\d+)", re.I | re.M)
SLUG_RE = re.compile(r"(?:videos|episode)/([a-z0-9][a-z0-9-]*[a-z0-9])")
RELEASE_TAG_RE = re.compile(r"^episode/(.+)-v(\d+)$")


# ----------------------------------------------------------------------------- fetching
def _get(url: str, token: str | None):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "studio-status"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers),
                                        timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8")), resp.headers.get("Link", "")
        except urllib.error.HTTPError as e:
            if e.code < 500 or attempt == 3:
                raise
        except urllib.error.URLError:
            if attempt == 3:
                raise
        time.sleep(2 ** attempt)
    raise RuntimeError("unreachable")


def api(path: str, token: str | None) -> list | dict:
    """GET an API path; list endpoints are followed through every page."""
    url = path if path.startswith("http") else API + path
    data, link = _get(url, token)
    if not isinstance(data, list):
        return data
    out = list(data)
    while (m := re.search(r'<([^>]+)>;\s*rel="next"', link)):
        data, link = _get(m.group(1), token)
        out += data
    return out


def fetch_snapshot(repo: str, token: str | None) -> dict:
    issues = [i for i in api(f"/repos/{repo}/issues?labels=episode&state=all&per_page=100", token)
              if "pull_request" not in i]
    snap = {"issues": issues, "comments": {}, "events": {}, "validations": {}}
    for issue in issues:
        if issue["state"] != "open":
            continue
        n = str(issue["number"])
        snap["comments"][n] = api(f"/repos/{repo}/issues/{n}/comments?per_page=100", token)
        snap["events"][n] = api(f"/repos/{repo}/issues/{n}/events?per_page=100", token)
    snap["pulls"] = api(f"/repos/{repo}/pulls?state=open&per_page=100", token)
    snap["releases"] = api(f"/repos/{repo}/releases?per_page=100", token)
    # Checkpoints only come at stage boundaries (scenes alone take about a day); a session's
    # pushes to its branch are the steadier sign that it is alive.
    snap["branches"] = {}
    for comments in snap["comments"].values():
        b = (protocol(comments)["claim"] or {}).get("branch")
        if b and b not in snap["branches"]:
            try:
                head = api(f"/repos/{repo}/branches/{urllib.parse.quote(b, safe='')}", token)
                snap["branches"][b] = head["commit"]["commit"]["committer"]["date"]
            except urllib.error.HTTPError:
                snap["branches"][b] = None      # merged and deleted, or never pushed
    return snap


# ----------------------------------------------------------------------------- helpers
def norm_label(name: str) -> str:
    return re.sub(r"[\s▶✔⏸️]+", "", name).lower()


def iso_ts(value: str | None) -> float:
    if not value:
        return 0.0
    return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()


def ts_iso(ts: float) -> str | None:
    if not ts:
        return None
    return datetime.fromtimestamp(ts, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def first_line(body: str | None) -> str:
    # ">" is kept on purpose: a quote-reply to a protocol comment is not a protocol event.
    for line in (body or "").splitlines():
        line = re.sub(r"^[\s#*_`]+", "", line).strip()
        if line:
            return line
    return ""


def load_series(path: Path) -> list[dict]:
    series = json.loads(path.read_text(encoding="utf-8"))["series"]
    for s in series:
        s["_slug"] = re.compile(s["slug_number"]) if s.get("slug_number") else None
        s["_title"] = re.compile(s["title_number"]) if s.get("title_number") else None
    return series


def series_for(series: list[dict], labels: set[str] | None = None, slug: str | None = None) -> dict:
    for s in series:
        if labels and s.get("issue_label") in labels:
            return s
        if slug and s.get("slug_prefix") and slug.startswith(s["slug_prefix"]):
            return s
    return next(s for s in series if s["id"] == "standalone")


def number_in(s: dict, title: str | None = None, slug: str | None = None) -> int | None:
    for rx, text in ((s.get("_title"), title), (s.get("_slug"), slug)):
        if rx and text and (m := rx.search(text)):
            return int(m.group(1))
    return None


def code_for(s: dict, n: int | None) -> str | None:
    return s["code"].format(n) if n is not None and s.get("code") else None


def clean_title(title: str, s: dict) -> str:
    t = re.sub(r"^\s*\[episode\]\s*", "", title, flags=re.I)
    if s.get("short") and s.get("_title"):
        t = re.sub(r"^\s*" + re.escape(s["short"]) + r"\s+" + s["_title"].pattern
                   + r"\s*[·:：\-—]\s*", "", t)
    return t.strip()


# ----------------------------------------------------------------------------- progress
def protocol(comments: list[dict]) -> dict:
    """Claims, checkpoints and progress lines from an issue's comments (oldest first)."""
    out = {"claim": None, "checkpoint": None, "progress": None, "last": 0.0}
    for c in sorted(comments, key=lambda c: c["created_at"]):
        at = iso_ts(c["created_at"])
        out["last"] = max(out["last"], at)
        line = first_line(c.get("body"))
        if (m := CLAIM_RE.match(line)):
            b = BRANCH_RE.search(line)
            out["claim"] = {"model": m.group(1).strip(), "at": at,
                            "branch": b.group(1).rstrip(".,;)") if b else None}
        elif (m := MARK_RE.match(line)) and m.group(1).upper() == "CHECKPOINT":
            out["checkpoint"] = {"stage": m.group(2).lower(), "at": at,
                                 "paused": bool(re.search(r"paus|暂停", line, re.I))}
        elif (m := MARK_RE.match(line)):          # HANDOFF releases the claim
            out["claim"] = None
        for pm in PROGRESS_RE.finditer(c.get("body") or ""):
            stage = STAGE_ALIASES.get(pm.group(1).lower().rstrip(":："))
            done, total = int(pm.group(2)), int(pm.group(3))
            if stage and total > 0:
                out["progress"] = {"stage": stage, "done": min(done, total), "total": total, "at": at}
    return out


def label_times(events: list[dict]) -> dict[str, float]:
    """When each currently-relevant label was last applied."""
    applied: dict[str, float] = {}
    for e in events:
        if e.get("event") == "labeled" and e.get("label"):
            applied[e["label"]["name"]] = iso_ts(e["created_at"])
    return applied


def derive(issue: dict, comments: list[dict], events: list[dict]) -> dict:
    """Stage and status of one episode issue, before cross-episode context (queued)."""
    labels = {lab["name"] for lab in issue.get("labels", [])}
    normed = {norm_label(n): n for n in labels}
    applied = label_times(events)
    proto = protocol(comments)
    fallback_t = iso_ts(issue.get("updated_at"))

    stage, since, source = None, 0.0, None
    # 1. the lifecycle tail: once an episode is ready, released or live, that is the truth
    tail = [STATE_LABELS[n] for n in labels if n in STATE_LABELS]
    tail += [STAGE_LABELS[k] for k in normed if STAGE_LABELS.get(k) == "ready"]
    tail = [t for t in tail if INDEX[t] >= INDEX["ready"]]
    if tail:
        stage = max(tail, key=INDEX.get)
        since = max((applied.get(n, 0) for n in labels if STATE_LABELS.get(n) == stage
                     or STAGE_LABELS.get(norm_label(n)) == stage), default=0) or fallback_t
        source = "label"
    else:
        # 2. the newer of the stage label and the latest checkpoint
        lab = [(STAGE_LABELS[k], applied.get(n, 0)) for k, n in normed.items() if k in STAGE_LABELS]
        lab += [(STATE_LABELS[n], applied.get(n, 0)) for n in labels if n in STATE_LABELS]
        lab_stage, lab_t = max(lab, key=lambda x: (x[1], INDEX[x[0]]), default=(None, 0.0))
        cp = proto["checkpoint"]
        cp_stage = None
        if cp:
            table = CHECKPOINT_SELF if cp["paused"] else CHECKPOINT_NEXT
            cp_stage = table.get(cp["stage"])
        if lab_stage and (not cp_stage or lab_t >= cp["at"]):
            stage, since, source = lab_stage, lab_t or fallback_t, "label"
        elif cp_stage:
            stage = max(filter(None, [cp_stage, lab_stage]), key=INDEX.get)
            since, source = cp["at"], "checkpoint"
        elif proto["claim"]:
            stage, since, source = "brief", proto["claim"]["at"], "claim"

    activity = max([proto["last"], *applied.values()], default=0.0) or fallback_t
    paused = any(norm_label(n) == PAUSE_LABEL for n in labels)
    question = QUESTION_LABEL in labels
    progress = proto["progress"]
    if not (progress and stage and progress["stage"] == stage and progress["at"] >= since - 1):
        progress = None

    if stage == "published":
        state = "published"
    elif issue["state"] != "open" and stage != "publishing":
        state = "closed"
    elif question:
        state = "question"
    elif paused:
        state = "paused"
    elif stage in ("ready", "publishing"):
        state = stage
    elif source in (None, "claim"):
        state = "starting"          # resolved to active or queued with the branch context
    else:
        state = "active"

    return {"stage": stage or "brief", "source": source, "since": since, "activity": activity,
            "state": state, "paused": paused, "question": question, "progress": progress,
            "claim": proto["claim"], "checkpoint": proto["checkpoint"]}


def percent(stage: str, state: str, progress: dict | None) -> int:
    if state == "published":
        return 100
    i = INDEX[stage]
    done = sum(w for _, _, _, w, _ in STAGES[:i])
    frac = progress["done"] / progress["total"] if progress else 0.0
    return int(round(done + STAGES[i][3] * frac))


def build_status(snap: dict, series: list[dict], registry: dict, repo: str, now: float) -> dict:
    prs_by_branch = {p["head"]["ref"]: p for p in snap.get("pulls", [])}
    episodes = []
    for issue in snap.get("issues", []):
        n = str(issue["number"])
        d = derive(issue, snap.get("comments", {}).get(n, []), snap.get("events", {}).get(n, []))
        if d["state"] == "closed":
            continue
        labels = {lab["name"] for lab in issue.get("labels", [])}
        slugs = SLUG_RE.findall(issue.get("body") or "")
        s = series_for(series, labels, slugs[0] if slugs else None)
        slug = next((x for x in slugs if not s.get("slug_prefix") or x.startswith(s["slug_prefix"])),
                    slugs[0] if slugs else None)
        order = number_in(s, issue["title"], slug)
        pr = prs_by_branch.get(f"episode/{slug}") if slug else None
        bili = registry.get("episodes", {}).get(slug) if slug else None
        episodes.append({
            "number": issue["number"], "url": issue["html_url"],
            "title": clean_title(issue["title"], s), "series": s["id"], "order": order,
            "code": code_for(s, order), "slug": slug, "state": d["state"], "stage": d["stage"],
            "stage_since": ts_iso(d["since"]), "activity_at": ts_iso(d["activity"]),
            "progress": {k: d["progress"][k] for k in ("done", "total")} if d["progress"] else None,
            "paused": d["paused"], "question": d["question"],
            "claim": ({"model": d["claim"]["model"], "branch": d["claim"]["branch"],
                       "at": ts_iso(d["claim"]["at"])} if d["claim"] else None),
            "checkpoint": ({"stage": d["checkpoint"]["stage"], "at": ts_iso(d["checkpoint"]["at"])}
                           if d["checkpoint"] else None),
            "pr": ({"number": pr["number"], "url": pr["html_url"], "draft": pr["draft"]}
                   if pr else None),
            "bilibili": ({"bvid": bili["bvid"], "url": f"https://www.bilibili.com/video/{bili['bvid']}/"}
                         if bili else None),
            "_activity": d["activity"],
        })

    # A batch session pipelines its episodes on one branch: a claimed episode with no
    # progress waits its turn while a sibling moves, and staleness is judged per branch.
    branch_last: dict[str, float] = {b: iso_ts(at) for b, at in (snap.get("branches") or {}).items() if at}
    branch_moving: set[str] = set()
    for e in episodes:
        b = (e["claim"] or {}).get("branch")
        if b:
            branch_last[b] = max(branch_last.get(b, 0), e["_activity"])
            if e["state"] in ("active", "paused", "ready", "question"):
                branch_moving.add(b)
    for e in episodes:
        b = (e["claim"] or {}).get("branch")
        if e["state"] == "starting":
            e["state"] = "queued" if (not e["claim"] or b in branch_moving) else "active"
        e["branch_activity_at"] = ts_iso(branch_last.get(b, e["_activity"]))
        e["percent"] = percent(e["stage"], e["state"], e["progress"])
        del e["_activity"]

    ser_order = {s["id"]: i for i, s in enumerate(series)}
    episodes.sort(key=lambda e: (ser_order[e["series"]], e["order"] is None,
                                 e["order"] or 0, -e["number"]))
    return {
        "schema": 1, "generated_at": ts_iso(now), "repo": repo,
        "worker_command": WORKER.format(repo=repo),
        "stages": [{"key": k, "label": lab, "short": sh, "weight": w, "who": who}
                   for k, lab, sh, w, who in STAGES],
        "episodes": episodes,
        "series": [overview(s, episodes) for s in series if s.get("planned")],
        "pulls": [{"number": p["number"], "title": p["title"], "url": p["html_url"],
                   "branch": p["head"]["ref"], "draft": p["draft"], "updated_at": p["updated_at"]}
                  for p in sorted(snap.get("pulls", []), key=lambda p: p["updated_at"], reverse=True)],
    }


RANK = {"published": 6, "publishing": 5, "ready": 5, "question": 4, "active": 3, "paused": 2,
        "queued": 1}


def overview(s: dict, episodes: list[dict]) -> dict:
    """One cell per planned episode of a numbered series (the AC215 lecture map)."""
    mine = [e for e in episodes if e["series"] == s["id"] and e["order"]]
    skip = {int(k): v for k, v in (s.get("skip") or {}).items()}
    cells, counts = [], {}
    for n in range(1, s["planned"] + 1):
        best = max((e for e in mine if e["order"] == n), key=lambda e: RANK.get(e["state"], 0),
                   default=None)
        state = "skip" if n in skip else (best["state"] if best else "none")
        counts[state] = counts.get(state, 0) + 1
        cells.append({"n": n, "code": s["code"].format(n), "state": state,
                      "note": skip.get(n), "number": best["number"] if best else None,
                      "title": best["title"] if best else None,
                      "percent": best["percent"] if best else 0,
                      "stage": best["stage"] if best else None,
                      "bilibili": best["bilibili"] if best else None,
                      "url": best["url"] if best else None})
    return {"id": s["id"], "name": s["name"], "planned": s["planned"], "cells": cells,
            "counts": counts}


# ----------------------------------------------------------------------------- library
VARIANT_RANK = [  # the primary download: the bilingual cut a viewer would want
    (r"bilingual.*burned(?!.*part)", 0), (r"bilingual captions$", 1), (r"^Short / Chinese", 2),
    (r"Mandarin narration$", 3), (r"clean$", 4), (r"part", 8),
]


def variant_rank(v: str) -> int:
    return next((r for rx, r in VARIANT_RANK if re.search(rx, v or "")), 6)


def release_artifacts(releases: list[dict], have: set[str], validations: dict) -> dict[str, list]:
    """Catalog-shaped artifacts for episode releases the catalog does not list yet."""
    newest: dict[str, tuple[int, dict]] = {}
    for r in releases:
        m = RELEASE_TAG_RE.match(r.get("tag_name", ""))
        if m and not r.get("draft") and m.group(1) not in have:
            v = int(m.group(2))
            if v > newest.get(m.group(1), (0, None))[0]:
                newest[m.group(1)] = (v, r)
    out = {}
    for slug, (_, r) in newest.items():
        secs = (validations.get(slug) or {}).get("seconds", {})
        arts = []
        for a in r.get("assets", []):
            name = a["name"]
            mm = re.fullmatch(re.escape(slug) + r"(_part(\d+))?(\.zh-en)?\.mp4", name)
            if not mm:
                continue
            variant = "English narration / " + ("bilingual captions (burned)" if mm.group(3)
                                                 else "clean")
            if mm.group(2):
                variant += f" / part {mm.group(2)}"
            arts.append({"episode": slug, "title": re.sub(r"\s*\(follow-along:.*\)$", "",
                                                          r.get("name") or slug),
                         "variant": variant, "bytes": a["size"], "duration_seconds": secs.get(name),
                         "download_url": a["browser_download_url"], "release_tag": r["tag_name"],
                         "_released": iso_ts(r.get("published_at") or r.get("created_at"))})
        if arts:
            out[slug] = arts
    return out


CJK_RE = re.compile(r"[\u3400-\u9fff]")


def display_titles(s: dict, title_en: str | None, title_zh: str | None, slug: str) -> tuple[str, str | None]:
    """(title, subtitle): the Chinese title when there is one, the English one beneath it.
    A series card already shows its code (L02, E6), so 'AC215 L2: ' style prefixes go."""
    short = re.escape(s.get("short") or "")
    en, zh = (title_en or "").strip(), (title_zh or "").strip()
    if short:
        en = re.sub(rf"^{short}\s*(?:·\s*)?(?:L|E|EP|Lecture\s*|Episode\s*)?\d+\s*[:：—–·-]\s*", "", en, flags=re.I)
        zh = re.sub(rf"^{short}\s*第\s*\d+\s*讲\S*\s*·\s*", "", zh, flags=re.I)
    if en[:1].islower():
        en = en[0].upper() + en[1:]
    if not en:
        en = slug.replace("-", " ").capitalize()
    if zh and CJK_RE.search(zh):
        return zh, (en if en != zh else None)
    return en, None


def build_library(catalog: dict, registry: dict, series: list[dict], releases: list[dict],
                  validations: dict, now: float) -> dict:
    by_ep: dict[str, list] = {}
    first_seen: dict[str, int] = {}
    for i, a in enumerate(catalog.get("artifacts", [])):
        by_ep.setdefault(a["episode"], []).append(a)
        first_seen.setdefault(a["episode"], i)
    for slug, arts in release_artifacts(releases, set(by_ep), validations).items():
        by_ep[slug] = arts
        first_seen[slug] = len(first_seen) + 1000
    groups: dict[str, list] = {s["id"]: [] for s in series}
    for slug, arts in by_ep.items():
        s = series_for(series, slug=slug)
        n = number_in(s, slug=slug)
        variants = sorted(({"variant": a.get("variant") or "—", "url": a["download_url"],
                            "bytes": a.get("bytes"), "seconds": a.get("duration_seconds")}
                           for a in arts), key=lambda v: (variant_rank(v["variant"]), v["variant"]))
        bili = registry.get("episodes", {}).get(slug)
        released = max((a.get("_released", 0) for a in arts), default=0)
        title, subtitle = display_titles(s, next((a["title"] for a in arts if a.get("title")), None),
                                         bili["title"] if bili else None, slug)
        groups[s["id"]].append({
            "slug": slug, "series": s["id"], "order": n, "code": code_for(s, n),
            "title": title, "subtitle": subtitle,
            "seconds": variants[0]["seconds"], "primary": variants[0], "variants": variants,
            "bilibili": ({"bvid": bili["bvid"], "pubdate": bili.get("pubdate"),
                          "url": f"https://www.bilibili.com/video/{bili['bvid']}/"} if bili else None),
            "_sort": (bili or {}).get("pubdate") or released or first_seen[slug],
        })
    out = []
    for s in series:
        eps = groups[s["id"]]
        if not eps:
            continue
        if any(e["order"] is not None for e in eps):
            eps.sort(key=lambda e: (e["order"] is None, e["order"] or 0))
        else:
            eps.sort(key=lambda e: e["_sort"], reverse=True)
        for e in eps:
            del e["_sort"]
        out.append({"id": s["id"], "name": s["name"], "short": s.get("short", s["name"]),
                    "description": s.get("description", ""), "episodes": eps,
                    "counts": {"episodes": len(eps),
                               "published": sum(1 for e in eps if e["bilibili"]),
                               "seconds": round(sum(e["seconds"] or 0 for e in eps))}})
    total = {k: sum(g["counts"][k] for g in out) for k in ("episodes", "published", "seconds")}
    return {"schema": 1, "generated_at": ts_iso(now), "series": out, "totals": total,
            "unmatched": registry.get("unmatched", [])}


def fetch_validations(snap: dict, have: set[str]) -> None:
    """Durations for uncatalogued releases come from their small validation sidecar."""
    for r in snap.get("releases", []):
        m = RELEASE_TAG_RE.match(r.get("tag_name", ""))
        if not m or m.group(1) in have or m.group(1) in snap["validations"]:
            continue
        asset = next((a for a in r.get("assets", [])
                      if a["name"] == f"{m.group(1)}.validation.json"), None)
        if asset:
            try:
                snap["validations"][m.group(1)] = api(asset["browser_download_url"], None)
            except (urllib.error.URLError, ValueError):
                pass


# ----------------------------------------------------------------------------- main
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY", DEFAULT_REPO))
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--catalog", type=Path, default=ROOT / "catalog")
    ap.add_argument("--offline", action="store_true", help="files only; no GitHub API")
    ap.add_argument("--snapshot", type=Path, help="build from saved API payloads")
    ap.add_argument("--save-snapshot", type=Path, help="also write the raw API payloads here")
    ap.add_argument("--now", help="ISO time to stamp (tests)")
    args = ap.parse_args(argv)

    now = iso_ts(args.now) if args.now else time.time()
    series = load_series(args.catalog / "series.json")
    catalog = json.loads((args.catalog / "videos.json").read_text(encoding="utf-8"))
    registry = json.loads((args.catalog / "bilibili.json").read_text(encoding="utf-8"))
    if args.snapshot:
        snap = json.loads(args.snapshot.read_text(encoding="utf-8"))
        snap.setdefault("validations", {})
    elif args.offline:
        snap = {"issues": [], "comments": {}, "events": {}, "pulls": [], "releases": [],
                "validations": {}}
    else:
        token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
        snap = fetch_snapshot(args.repo, token)
        fetch_validations(snap, {a["episode"] for a in catalog.get("artifacts", [])})
    if args.save_snapshot:
        args.save_snapshot.write_text(json.dumps(snap, ensure_ascii=False), encoding="utf-8")

    status = build_status(snap, series, registry, args.repo, now)
    library = build_library(catalog, registry, series, snap.get("releases", []),
                            snap.get("validations", {}), now)
    args.out.mkdir(parents=True, exist_ok=True)
    for name, data in (("status.json", status), ("library.json", library)):
        (args.out / name).write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")),
                                     encoding="utf-8")
    live = [e for e in status["episodes"] if e["state"] != "published"]
    print(f"status: {len(status['episodes'])} episodes ({len(live)} in flight), "
          f"{len(status['pulls'])} open PRs; library: {library['totals']['episodes']} videos "
          f"in {len(library['series'])} series -> {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
