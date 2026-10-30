#!/usr/bin/env python3
"""A week of pull requests in another repository, as a Markdown digest for a video brief.

The build-log series (docs/PORTAL_SERIES.md) explains what the owner's pull requests did in a
week: which problem each one solved, in what order the work happened, and what changed. This
tool reads that history from a local clone, so it works the same on a laptop and in a cloud
session, and it never needs a token:

- merged pull requests come from main's first-parent merge commits
  ("Merge pull request #N from owner/branch"): their own commits are M^1..M^2;
- open branches are the remote branches main does not contain; a branch stacked on another
  open branch (its base was merged into it) gets only its own commits.

Commit authors do not say whose work it is (agents commit as "Claude"), so "my PRs" comes
from GitHub: pass --prs with a JSON list of pull requests (number, title, state, user.login,
head.ref, as `gh pr list --json` or the GitHub MCP list_pull_requests returns them) and
--pr-author to keep one person's. Without --prs every branch with commits in the window is
listed, titled from its merge commit or its branch name.

    python3 tools/pr_digest.py --repo ../InternationalHealthportal --since 2026-10-26 \\
        --until 2026-11-01 --prs prs.json --pr-author JunyiZhou-Conny > week.md
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

MERGE_RE = re.compile(r"^Merge pull request #(\d+) from [^/\s]+/(\S+)")
DECISION_RE = re.compile(r"^docs/decisions/(\d{4})-[^/]+\.md$")
# A gap this long between two commits starts a new work session in the timeline.
SESSION_GAP = timedelta(minutes=90)


@dataclass
class Commit:
    sha: str
    when: datetime
    subject: str
    merge: bool
    files: list[tuple[str, int, int]] = field(default_factory=list)


@dataclass
class Unit:
    """One pull request (merged or open) or one open branch without a known PR."""
    branch: str
    tip: str
    number: int | None = None
    title: str | None = None
    state: str = "open"
    author: str | None = None
    commits: list[Commit] = field(default_factory=list)


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True,
                          text=True).stdout


def resolve_main(repo: Path, name: str) -> str:
    for ref in (f"refs/remotes/origin/{name}", f"refs/heads/{name}"):
        if subprocess.run(["git", "-C", str(repo), "rev-parse", "-q", "--verify", ref],
                          capture_output=True).returncode == 0:
            return ref
    raise SystemExit(f"no branch {name!r} in {repo}")


def is_ancestor(repo: Path, a: str, b: str) -> bool:
    return subprocess.run(["git", "-C", str(repo), "merge-base", "--is-ancestor", a, b],
                          capture_output=True).returncode == 0


def merged_units(repo: Path, main: str, since: datetime, until: datetime) -> list[Unit]:
    out = git(repo, "log", main, "--first-parent", "--merges", "--format=%H%x00%P%x00%cI%x00%B%x1e")
    units = []
    for rec in filter(str.strip, out.split("\x1e")):
        sha, parents, when, body = rec.strip("\n").split("\x00")
        m = MERGE_RE.match(body)
        if not m or not since <= datetime.fromisoformat(when) < until:
            continue
        lines = [ln for ln in body.splitlines()[1:] if ln.strip()]
        first, second = parents.split()[:2]
        units.append(Unit(branch=m.group(2), tip=f"{first}..{second}", number=int(m.group(1)),
                          title=lines[0] if lines else None, state="merged"))
    return units


def open_units(repo: Path, main: str) -> list[Unit]:
    """Remote (else local) branches main does not contain, each with its stacked-on bases."""
    refs: dict[str, str] = {}
    out = git(repo, "for-each-ref", "--format=%(refname)%00%(objectname)", "refs/heads", "refs/remotes/origin")
    for line in out.splitlines():
        ref, sha = line.split("\x00")
        name = ref.removeprefix("refs/remotes/origin/").removeprefix("refs/heads/")
        if name in ("HEAD", main.rsplit("/", 1)[-1]):
            continue
        if ref.startswith("refs/remotes/") or name not in refs:
            refs[name] = sha
    tips = {n: s for n, s in refs.items() if not is_ancestor(repo, s, main)}
    units = []
    for name, sha in sorted(tips.items()):
        bases = [s for n, s in tips.items() if n != name and s != sha and is_ancestor(repo, s, sha)]
        units.append(Unit(branch=name, tip=" ".join([sha, "--not", main, *bases])))
    return units


def load_commits(repo: Path, unit: Unit, since: datetime, until: datetime, tz: ZoneInfo) -> None:
    out = git(repo, "log", "--reverse", "--numstat", "--no-renames", "--format=%x1e%H%x00%aI%x00%P%x00%s", *unit.tip.split())
    for rec in filter(str.strip, out.split("\x1e")):
        head, *stats = rec.strip("\n").split("\n")
        sha, when, parents, subject = head.split("\x00")
        at = datetime.fromisoformat(when)
        if not since <= at < until:
            continue
        c = Commit(sha=sha[:7], when=at.astimezone(tz), subject=subject, merge=len(parents.split()) > 1)
        for line in filter(None, stats):
            added, deleted, path = line.split("\t", 2)
            if added != "-":  # binary files have no line counts
                c.files.append((path, int(added), int(deleted)))
        unit.commits.append(c)


def area(path: str) -> str:
    parts = path.split("/")
    return "/".join(parts[:2]) + "/" if len(parts) > 2 else path


def decision_title(repo: Path, rev: str, path: str) -> str:
    try:
        text = git(repo, "show", f"{rev}:{path}")
    except subprocess.CalledProcessError:
        return path
    return next((ln.lstrip("# ").strip() for ln in text.splitlines() if ln.startswith("# ")), path)


def render_unit(repo: Path, unit: Unit) -> list[str]:
    own = [c for c in unit.commits if not c.merge]
    merges = [c for c in unit.commits if c.merge]
    name = f"#{unit.number} · {unit.title}" if unit.number else f"`{unit.branch}`"
    lines = [f"## {name}", ""]
    span = f"{own[0].when:%m-%d %H:%M} → {own[-1].when:%m-%d %H:%M}" if own else "no own commits"
    hours = (own[-1].when - own[0].when).total_seconds() / 3600 if own else 0
    added = sum(a for c in own for _, a, _ in c.files)
    deleted = sum(d for c in own for _, _, d in c.files)
    lines += [f"- Branch `{unit.branch}` · {unit.state}" + (f" · by {unit.author}" if unit.author else ""),
              f"- {len(own)} commits (+{len(merges)} merges) over {hours:.1f} h: {span}",
              f"- +{added} / −{deleted} lines", ""]
    areas: dict[str, tuple[set[str], list[int]]] = {}
    for c in own:
        for path, a, d in c.files:
            files, counts = areas.setdefault(area(path), (set(), [0, 0]))
            files.add(path)
            counts[0] += a
            counts[1] += d
    if areas:
        lines += ["| Area | Files | + | − |", "|---|---:|---:|---:|"]
        for where, (files, (a, d)) in sorted(areas.items(), key=lambda kv: -sum(kv[1][1])):
            lines.append(f"| `{where}` | {len(files)} | {a} | {d} |")
        lines.append("")
    rev = unit.tip.split()[0].split("..")[-1]
    decisions = sorted({p for c in own for p, _, _ in c.files if DECISION_RE.match(p)})
    if decisions:
        lines += ["Decision records touched:", ""]
        lines += [f"- `{p}`: {decision_title(repo, rev, p)}" for p in decisions] + [""]
    if own:
        lines += ["Timeline (a blank line marks a pause of 90 minutes or more):", ""]
        prev = None
        for c in own:
            if prev and c.when - prev > SESSION_GAP:
                lines.append("")
            lines.append(f"- {c.when:%m-%d %H:%M} `{c.sha}` {c.subject}")
            prev = c.when
        lines.append("")
    return lines


def apply_prs(units: list[Unit], prs: list[dict]) -> None:
    by_branch = {p["head"]["ref"] if isinstance(p.get("head"), dict) else p.get("headRefName"): p for p in prs}
    by_number = {p["number"]: p for p in prs}
    for u in units:
        p = by_number.get(u.number) if u.number else by_branch.get(u.branch)
        if not p:
            continue
        u.number, u.title = p["number"], p.get("title") or u.title
        user = p.get("user") or p.get("author") or {}
        u.author = user.get("login")
        if u.state != "merged":
            u.state = "draft" if p.get("draft") or p.get("isDraft") else str(p.get("state", "open")).lower()


def digest(repo: Path, since: datetime, until: datetime, tz: ZoneInfo, main_name: str = "main",
           prs: list[dict] | None = None, pr_author: str | None = None) -> str:
    main = resolve_main(repo, main_name)
    units = merged_units(repo, main, since, until) + open_units(repo, main)
    if prs is not None:
        apply_prs(units, prs)
        if pr_author:
            units = [u for u in units if u.author == pr_author]
    for u in units:
        load_commits(repo, u, since, until, tz)
    units = [u for u in units if any(not c.merge for c in u.commits)]
    units.sort(key=lambda u: min(c.when for c in u.commits if not c.merge))
    title = f"# Pull requests, {since:%Y-%m-%d} to {(until - timedelta(days=1)):%Y-%m-%d}"
    lines = [title, "", f"Repository `{repo.name}`, read from git at main = "
             f"`{git(repo, 'rev-parse', '--short', main).strip()}`; times in {tz.key}."
             + (f" Pull requests by {pr_author}." if pr_author else ""), ""]
    if not units:
        return "\n".join(lines + ["No commits in this window.", ""])
    lines += ["| PR | State | Commits | Lines | First → last commit |", "|---|---|---:|---:|---|"]
    for u in units:
        own = [c for c in u.commits if not c.merge]
        size = sum(a + d for c in own for _, a, d in c.files)
        label = f"#{u.number} {u.title or ''}".strip() if u.number else f"`{u.branch}`"
        lines.append(f"| {label} | {u.state} | {len(own)} | {size} | "
                     f"{own[0].when:%m-%d %H:%M} → {own[-1].when:%m-%d %H:%M} |")
    lines.append("")
    for u in units:
        lines += render_unit(repo, u)
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--repo", type=Path, required=True, help="local clone (fetch the branches first)")
    ap.add_argument("--since", required=True, help="first day, YYYY-MM-DD")
    ap.add_argument("--until", required=True, help="day after the last, YYYY-MM-DD")
    ap.add_argument("--tz", default="America/New_York", help="time zone for the timeline")
    ap.add_argument("--main", default="main")
    ap.add_argument("--prs", type=Path, help="JSON list of pull requests from GitHub")
    ap.add_argument("--pr-author", help="keep only pull requests by this GitHub login (needs --prs)")
    ap.add_argument("--out", type=Path)
    args = ap.parse_args(argv)
    if args.pr_author and not args.prs:
        ap.error("--pr-author needs --prs: commit authors do not say whose pull request it is")
    tz = ZoneInfo(args.tz)
    since = datetime.fromisoformat(args.since).replace(tzinfo=tz)
    until = datetime.fromisoformat(args.until).replace(tzinfo=tz)
    prs = json.loads(args.prs.read_text(encoding="utf-8")) if args.prs else None
    text = digest(args.repo, since, until, tz, args.main, prs, args.pr_author)
    if args.out:
        args.out.write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
