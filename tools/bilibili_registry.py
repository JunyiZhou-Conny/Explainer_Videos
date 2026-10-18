#!/usr/bin/env python3
"""Which catalog episodes are live on Bilibili: catalog/bilibili.json.

The registry maps an episode slug to its Bilibili video. Two writers keep it current:

- tools/publish_worker.py records every upload it makes (it knows the slug and the BV id);
- `python3 tools/bilibili_registry.py sync` (run daily by .github/workflows/bilibili-sync.yml)
  reads the channel's public video list and records videos whose title equals an episode's
  `title_zh` in videos/<slug>/script.json — this catches uploads made by hand. Channel videos
  it cannot place are kept under "unmatched" so the library page can show them.

Bilibili's risk control intermittently refuses datacenter IPs (HTTP 412). A refused sync
changes nothing and exits 0; the next run, or the publish worker, fills the gap.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "catalog" / "bilibili.json"
LIST_URL = "https://api.bilibili.com/x/series/recArchivesByKeywords?mid={mid}&keywords=&ps={ps}&pn={pn}"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 (KHTML, like Gecko)"


class Unavailable(RuntimeError):
    """Bilibili refused or returned something other than the expected JSON."""


def load(path: Path = REGISTRY) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def dumps(reg: dict) -> str:
    return json.dumps(reg, indent=2, ensure_ascii=False) + "\n"


def record(reg: dict, slug: str, bvid: str, title: str, pubdate: int) -> bool:
    """Register slug -> video. Returns True when the registry changed."""
    prior = reg["episodes"].get(slug)
    if prior and prior["bvid"] == bvid:
        pubdate = prior["pubdate"]  # re-recording the same video never moves its date
    entry = {"bvid": bvid, "title": title, "pubdate": int(pubdate)}
    if prior == entry:
        return False
    reg["episodes"][slug] = entry
    reg["unmatched"] = [a for a in reg.get("unmatched", []) if a["bvid"] != bvid]
    return True


def known_titles(root: Path = ROOT) -> dict[str, str]:
    """title_zh -> slug, from every episode.json project's script.json."""
    titles = {}
    for script in sorted((root / "videos").glob("*/script.json")):
        title = json.loads(script.read_text(encoding="utf-8")).get("title_zh")
        if title:
            titles[title.strip()] = script.parent.name
    return titles


def match(reg: dict, archives: list[dict], titles: dict[str, str]) -> bool:
    """Record channel videos whose title names an unregistered episode; keep the rest as unmatched."""
    changed = False
    registered = {e["bvid"] for e in reg["episodes"].values()}
    unmatched = []
    for a in archives:
        if a["bvid"] in registered:
            continue
        slug = titles.get(a["title"].strip())
        if slug and slug not in reg["episodes"]:
            changed |= record(reg, slug, a["bvid"], a["title"], a["pubdate"])
            registered.add(a["bvid"])
        else:
            unmatched.append({"bvid": a["bvid"], "title": a["title"], "pubdate": int(a["pubdate"])})
    unmatched.sort(key=lambda a: a["pubdate"], reverse=True)
    if unmatched != reg.get("unmatched", []):
        reg["unmatched"] = unmatched
        changed = True
    return changed


def fetch_channel(mid: int, page_size: int = 100) -> list[dict]:
    archives, page = [], 1
    while True:
        req = urllib.request.Request(LIST_URL.format(mid=mid, ps=page_size, pn=page), headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                body = json.loads(resp.read().decode("utf-8"))
        except Exception as e:  # HTTP 412 from risk control, HTML error pages, timeouts
            raise Unavailable(str(e)) from e
        if body.get("code") != 0:
            raise Unavailable(f"code {body.get('code')}: {body.get('message')}")
        batch = (body.get("data") or {}).get("archives") or []
        archives += [{"bvid": a["bvid"], "title": a["title"], "pubdate": a["pubdate"]} for a in batch]
        if len(batch) < page_size:
            return archives
        page += 1
        time.sleep(2)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("sync", help="match the channel's public video list against the episodes")
    rec = sub.add_parser("record", help="register one upload")
    rec.add_argument("--slug", required=True)
    rec.add_argument("--bvid", required=True)
    rec.add_argument("--title", required=True)
    rec.add_argument("--pubdate", type=int, default=None, help="unix seconds (default: now)")
    args = ap.parse_args()

    reg = load()
    if args.cmd == "record":
        changed = record(reg, args.slug, args.bvid, args.title, args.pubdate or int(time.time()))
    else:
        try:
            archives = fetch_channel(reg["mid"])
        except Unavailable as e:
            print(f"Bilibili unavailable, registry unchanged: {e}", file=sys.stderr)
            return 0
        changed = match(reg, archives, known_titles())
        for a in reg.get("unmatched", []):
            print(f"unmatched on the channel: {a['bvid']} {a['title']}")
    if changed:
        REGISTRY.write_text(dumps(reg), encoding="utf-8")
    print("changed" if changed else "unchanged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
