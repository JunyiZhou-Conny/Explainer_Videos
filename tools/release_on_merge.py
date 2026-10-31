#!/usr/bin/env python3
"""Start the release workflow for every episode a merged PR adds (.github/workflows/release-on-merge.yml).

An episode counts as added when the PR adds its spec (videos/<slug>/video.yaml → legacy-release.yml,
videos/<slug>/episode.json → episode-release.yml), the spec is on main, the slug has no
episode/<slug>-v* release and catalog/bilibili.json does not list it. Re-releases stay a manual
dispatch: a v2 release is a second Bilibili upload.

The episode issue passed to the release (so the publish worker can report back) is the first of
these that names exactly one `episode`-labelled issue:
  1. the issue the merged PR closes, when the PR adds a single episode spec (counted before any
     skip, so a batch PR's closing issue never moves to a different episode);
  2. the issue the episode's own REVIEW.md / BRIEF.md links most often;
  3. issues whose body names videos/<slug> or episode/<slug> exactly (the PR's closing issues
     first, then every episode issue).
No match, or a tie, releases without an issue and prints a ::warning:: rather than guessing.

  python3 tools/release_on_merge.py --pr 62 [--repo owner/name] [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = re.compile(r"^videos/([A-Za-z0-9._-]+)/(video\.yaml|episode\.json)$")
WORKFLOW = {"video.yaml": "legacy-release.yml", "episode.json": "episode-release.yml"}


def added_episodes(added_files: list[str], released_tags: list[str], registry: dict, root: Path = ROOT,
                   dry: bool = False) -> list[tuple[str, str]]:
    """(slug, workflow) for each episode spec the PR adds that is on main and was never released.
    dry=True decides silently (main's early exit); plan() prints why each skipped slug is skipped."""
    say = (lambda msg: None) if dry else print
    released = {re.sub(r"-v\d+$", "", t).removeprefix("episode/") for t in released_tags if t.startswith("episode/")}
    on_bilibili = set((registry.get("episodes") or {}).keys())
    out, seen = [], set()
    for path in sorted(added_files):
        m = SPEC.match(path)
        if not m or m.group(1) in seen:
            continue
        slug, spec = m.groups()
        seen.add(slug)
        if not (root / path).is_file():
            say(f"skip {slug}: {path} is not on main")
        elif slug in released:
            say(f"skip {slug}: already released (re-releases are manual)")
        elif slug in on_bilibili:
            say(f"skip {slug}: already on Bilibili")
        else:
            out.append((slug, WORKFLOW[spec]))
    return out


def names_slug(text: str, slug: str) -> bool:
    """True when text names videos/<slug> or episode/<slug> exactly (not a longer slug)."""
    return re.search(rf"(?:videos|episode)/{re.escape(slug)}(?![A-Za-z0-9._-])", text or "") is not None


def linked_issue(slug: str, repo: str, root: Path = ROOT) -> int | None:
    """The issue the episode's REVIEW.md / BRIEF.md links most often, if one stands out."""
    text = "".join((root / "videos" / slug / f).read_text(encoding="utf-8")
                   for f in ("REVIEW.md", "BRIEF.md") if (root / "videos" / slug / f).is_file())
    counts = Counter(int(n) for n in re.findall(rf"{re.escape(repo)}/issues/(\d+)", text)).most_common(2)
    if not counts or (len(counts) == 2 and counts[0][1] == counts[1][1]):
        return None
    return counts[0][0]


def pick_issue(slug: str, n_added: int, closing: list[dict], issues: list[dict], repo: str, root: Path = ROOT) -> int | None:
    episode_numbers = {i["number"] for i in issues}
    closing = [i for i in closing if i["number"] in episode_numbers]
    if n_added == 1 and len(closing) == 1:
        return closing[0]["number"]
    linked = linked_issue(slug, repo, root)
    if linked in episode_numbers:
        return linked
    for pool in (closing, issues):
        hits = [i["number"] for i in pool if names_slug(i.get("body") or "", slug)]
        if len(hits) == 1:
            return hits[0]
        if len(hits) > 1:
            print(f"::warning::{slug}: issues {hits} all name it; releasing without an issue")
            return None
    print(f"::warning::{slug}: no episode issue found; releasing without an issue")
    return None


def plan(added_files: list[str], released_tags: list[str], registry: dict, closing: list[dict],
         issues: list[dict], repo: str, root: Path = ROOT) -> list[tuple[str, str, int | None]]:
    """(slug, workflow, issue) per episode to release. Rule 1 counts every episode spec the PR adds,
    released or not: a PR that adds two specs and closes one issue never hands that issue to the
    other episode just because the first one was already released."""
    n_specs = len({m.group(1) for p in added_files if (m := SPEC.match(p))})
    return [(slug, wf, pick_issue(slug, n_specs, closing, issues, repo, root))
            for slug, wf in added_episodes(added_files, released_tags, registry, root)]


def gh(*args: str) -> str:
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pr", type=int, required=True)
    ap.add_argument("--repo", default="JunyiZhou-Conny/Explainer_Videos")
    ap.add_argument("--dry-run", action="store_true", help="print the dispatches instead of running them")
    args = ap.parse_args(argv)
    owner, name = args.repo.split("/")

    # Every call fails loudly (check=True): an API error must not read as "nothing to release".
    added = gh("api", f"repos/{args.repo}/pulls/{args.pr}/files", "--paginate",
               "--jq", '.[] | select(.status == "added") | .filename').split()
    tags = gh("api", f"repos/{args.repo}/releases", "--paginate", "--jq", ".[].tag_name").split()
    registry = json.loads((ROOT / "catalog/bilibili.json").read_text(encoding="utf-8"))
    if not added_episodes(added, tags, registry, dry=True):
        print(f"PR #{args.pr} adds no unreleased episode; nothing to release.")
        return 0
    issues = json.loads(gh("issue", "list", "--repo", args.repo, "--label", "episode", "--state", "all",
                           "--limit", "1000", "--json", "number,body"))
    query = ("query($o:String!,$n:String!,$p:Int!){repository(owner:$o,name:$n){pullRequest(number:$p)"
             "{closingIssuesReferences(first:50){nodes{number body}}}}}")
    closing = json.loads(gh("api", "graphql", "-f", f"query={query}", "-F", f"o={owner}", "-F", f"n={name}",
                            "-F", f"p={args.pr}"))["data"]["repository"]["pullRequest"]["closingIssuesReferences"]["nodes"]
    for slug, workflow, issue in plan(added, tags, registry, closing, issues, args.repo):
        cmd = ["workflow", "run", workflow, "--repo", args.repo, "--ref", "main", "-f", f"episode=videos/{slug}"]
        if issue:
            cmd += ["-f", f"issue={issue}"]
        print(f"release {slug} with {workflow} (issue {issue or 'none'})")
        if args.dry_run:
            print("  would run: gh " + " ".join(cmd))
        else:
            gh(*cmd)
    return 0


if __name__ == "__main__":
    sys.exit(main())
