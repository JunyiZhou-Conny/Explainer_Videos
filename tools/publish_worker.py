#!/usr/bin/env python3
"""Publish released episodes to Bilibili from the one machine that holds a login.

Runs on Conny's Mac (launchd or cron, every ~15 minutes; also fine by hand). For every
GitHub release asset set that carries a PUBLISH.md manifest and is not yet published:
download the MP4, verify its sha256 against the manifest, upload it with biliup using
the manifest's title/description/tags/cover, then comment the BV link on the episode's
issue, move the label to state:published and close the issue.

State lives in ~/.config/explainer-publish/state.json - the repo stays the source of
intent (PUBLISH.md), this file only remembers what was already uploaded or failed.
cookies.json (biliup's login) stays in ~/.config/biliup/ and must never enter git,
GitHub secrets, or a cloud container.

Set up once with setup/macos/install-publish-worker.sh: it logs in (gh auth login; biliup login
in ~/.config/biliup, where biliup reads cookies.json from the working directory) and installs
launchd jobs that run this worker with --upload every 15 minutes and `biliup renew` weekly.
By hand, the prerequisites are:
  npm install -g @biliup/cli            # or the release binary from github.com/biliup/biliup
  cd ~/.config/biliup && biliup login   # scan the QR with the Bilibili app
  gh auth login                         # any account that can read the repo and comment

Dry run (default is to do nothing destructive without --upload):
  python3 tools/publish_worker.py --repo JunyiZhou-Conny/Explainer_Videos
  python3 tools/publish_worker.py --repo JunyiZhou-Conny/Explainer_Videos --upload
"""
from __future__ import annotations
import argparse
import base64
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import bilibili_registry

STATE_DIR = Path.home() / ".config" / "explainer-publish"
STATE = STATE_DIR / "state.json"


def sh(args: list[str], **kw) -> subprocess.CompletedProcess:
    print("+", " ".join(str(a) for a in args), flush=True)
    return subprocess.run([str(a) for a in args], check=True, text=True, **kw)


def gh_json(repo: str, path: str):
    out = subprocess.check_output(["gh", "api", f"repos/{repo}/{path}", "--paginate"], text=True)
    return json.loads(out)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def parse_publish_md(text: str) -> dict:
    """PUBLISH.md is a human-readable manifest with a fenced JSON block as ground truth."""
    m = re.search(r"```json\n(.*?)```", text, re.S)
    if not m:
        raise ValueError("PUBLISH.md has no fenced json block")
    return json.loads(m.group(1))


def load_state() -> dict:
    try:
        return json.loads(STATE.read_text())
    except FileNotFoundError:
        return {"published": {}, "failed": {}}


def save_state(state: dict) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, indent=2, ensure_ascii=False))


def record_on_github(repo: str, slug: str, bvid: str, title: str) -> None:
    """Add the upload to catalog/bilibili.json on the default branch, so the library shows it."""
    path = f"repos/{repo}/contents/catalog/bilibili.json"
    current = json.loads(subprocess.check_output(["gh", "api", path], text=True))
    reg = json.loads(base64.b64decode(current["content"]).decode("utf-8"))
    if not bilibili_registry.record(reg, slug, bvid, title, int(time.time())):
        return
    print(f"+ recording {slug} -> {bvid} in catalog/bilibili.json", flush=True)
    subprocess.run(["gh", "api", "-X", "PUT", path,
                    "-f", f"message=catalog: {slug} is live on Bilibili ({bvid})",
                    "-f", "content=" + base64.b64encode(bilibili_registry.dumps(reg).encode("utf-8")).decode("ascii"),
                    "-f", f"sha={current['sha']}"], check=True, capture_output=True, text=True)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", required=True, help="owner/name")
    ap.add_argument("--upload", action="store_true", help="actually upload (default: report what would happen)")
    ap.add_argument("--line", help="pinned biliup upload line (benchmark once, e.g. kodo or ws)")
    ap.add_argument("--limit", type=int, default=1, help="max uploads per run (rate-limit friendly)")
    args = ap.parse_args()
    state = load_state()
    uploads = 0
    for release in gh_json(args.repo, "releases"):
        assets = {a["name"]: a for a in release.get("assets", [])}
        manifest_asset = assets.get("PUBLISH.json")
        if not manifest_asset:
            continue
        tag = release["tag_name"]
        if tag in state["published"]:
            continue
        if uploads >= args.limit:
            print(f"limit {args.limit} reached; {tag} waits for the next run")
            break
        with tempfile.TemporaryDirectory() as td:
            tdir = Path(td)
            sh(["gh", "release", "download", tag, "--repo", args.repo,
                "--pattern", "PUBLISH.json", "--dir", tdir])
            manifest = json.loads((tdir / "PUBLISH.json").read_text())
            video_name = manifest["bilibili"]["asset"]
            sh(["gh", "release", "download", tag, "--repo", args.repo,
                "--pattern", video_name, "--dir", tdir])
            video = tdir / video_name
            actual = sha256(video)
            if actual != manifest["bilibili"]["sha256"]:
                print(f"BAD digest for {video_name}: {actual}", file=sys.stderr)
                state["failed"][tag] = {"reason": "sha256 mismatch", "at": time.strftime("%F %T")}
                save_state(state)
                continue
            meta = manifest["bilibili"]
            cmd = ["biliup", "upload", str(video),
                   "--title", meta["title_zh"][:80],
                   "--desc", meta["description_zh"],
                   "--tag", ",".join(meta["tags"][:10]),
                   "--tid", str(meta.get("tid", 201))]
            if args.line:
                cmd += ["--line", args.line]
            cover = meta.get("cover_asset")
            if cover and cover in assets:
                sh(["gh", "release", "download", tag, "--repo", args.repo, "--pattern", cover, "--dir", tdir])
                cmd += ["--cover", str(tdir / cover)]
            if not args.upload:
                print("DRY RUN, would run:", " ".join(cmd))
                continue
            try:
                out = subprocess.run(cmd, capture_output=True, text=True, check=True)
                print(out.stdout[-2000:])
            except subprocess.CalledProcessError as e:
                print(e.stdout, e.stderr, file=sys.stderr)
                state["failed"][tag] = {"reason": (e.stderr or "")[-500:], "at": time.strftime("%F %T")}
                save_state(state)
                issue = manifest.get("issue")
                if issue:
                    sh(["gh", "issue", "comment", str(issue), "--repo", args.repo, "--body",
                        f"Bilibili upload of `{video_name}` failed on the publish worker; "
                        f"it will retry next run. Last error tail:\n```\n{(e.stderr or '')[-400:]}\n```\n\n---\n"
                        "_Generated by [Claude Code](https://claude.ai/code)_"])
                continue
            bv = re.search(r"BV[0-9A-Za-z]{10}", out.stdout or "")
            link = f"https://www.bilibili.com/video/{bv.group(0)}/" if bv else "(BV id not in biliup output; check member.bilibili.com)"
            state["published"][tag] = {"bv": bv.group(0) if bv else None, "at": time.strftime("%F %T")}
            state["failed"].pop(tag, None)
            save_state(state)
            uploads += 1
            if bv:
                try:
                    record_on_github(args.repo, manifest["slug"], bv.group(0), meta["title_zh"][:80])
                except Exception as e:  # the upload stands; the daily registry sync matches it by title
                    print(f"could not record {bv.group(0)} in catalog/bilibili.json: {e}", file=sys.stderr)
            issue = manifest.get("issue")
            if issue:
                sh(["gh", "issue", "comment", str(issue), "--repo", args.repo, "--body",
                    f"Published to Bilibili: {link}\n\n---\n_Generated by [Claude Code](https://claude.ai/code)_"])
                sh(["gh", "issue", "edit", str(issue), "--repo", args.repo,
                    "--remove-label", "state:publishing", "--add-label", "state:published"])
                sh(["gh", "issue", "close", str(issue), "--repo", args.repo,
                    "--comment", "Video is live; closing the episode thread.\n\n---\n_Generated by [Claude Code](https://claude.ai/code)_"])
    print("done:", json.dumps({k: len(v) for k, v in state.items()}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
