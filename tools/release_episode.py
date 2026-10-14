#!/usr/bin/env python3
"""Release a finished episode: tag, upload the deliverables, emit the publish manifest.

Designed to run in GitHub Actions after an episode PR merges (the workflow passes the
episode directory). It can also run anywhere a GITHUB_TOKEN with contents:write is
available. Claude Code cloud sessions cannot create releases; they trigger the
release workflow instead.

Steps:
 1. Read videos/<slug>/episode.json + script.json and outputs/<slug>/ (or a directory
    given with --outputs) for the rendered deliverables and their validation sidecar.
 2. Refuse to release when validation.json is missing, its script_sha256 does not match
    the committed script.json, or REVIEW.md lacks the human sign-off line.
 3. Create release episode/<slug>-vN (N = 1 + existing releases of this slug), upload
    the MP4(s), subtitles, chapters and SHA256SUMS.txt plus PUBLISH.json / PUBLISH.md.
 4. Print the asset URLs; the catalog updater consumes them.

The PUBLISH manifest makes uploading mechanical for any executor (the Mac worker, a
computer-use agent, or a human): asset name + sha256 + bilingual title/description/tags.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("episode", type=Path, help="videos/<slug>")
    ap.add_argument("--outputs", type=Path, help="rendered deliverables (default outputs/<slug>)")
    ap.add_argument("--issue", type=int, help="the episode's issue number, for the publish worker")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    episode = args.episode.resolve()
    slug = episode.name
    out = (args.outputs or ROOT / "outputs" / slug).resolve()
    script = json.loads((episode / "script.json").read_text())
    validation_path = out / f"{slug}.validation.json"
    if not validation_path.exists():
        raise SystemExit(f"No {validation_path}; render the full episode first.")
    validation = json.loads(validation_path.read_text())
    committed = hashlib.sha256((episode / "script.json").read_bytes()).hexdigest()
    if validation.get("script_sha256") != committed:
        raise SystemExit("validation.json was made from a different script.json than the one committed. Re-render.")
    review = (episode / "REVIEW.md").read_text() if (episode / "REVIEW.md").exists() else ""
    if "human review" not in review.lower():
        raise SystemExit("REVIEW.md lacks a human-review record; the lifecycle requires Conny's listening sign-off before release (AGENTS.md).")

    deliverables = sorted(p for p in out.iterdir() if p.suffix in {".mp4", ".srt", ".ass"}
                          or p.name.endswith(".chapters.txt"))
    deliverables = [p for p in deliverables if not p.name.startswith("sample-")
                    and ".clean." not in p.name and ".scored." not in p.name]
    if not any(p.suffix == ".mp4" for p in deliverables):
        raise SystemExit(f"No final MP4 under {out}")

    token_env = {k: v for k, v in os.environ.items()}
    existing = subprocess.check_output(["gh", "api", f"repos/{os.environ['GITHUB_REPOSITORY']}/releases",
                                        "--paginate", "--jq", ".[].tag_name"], text=True, env=token_env).split()
    n = 1 + sum(1 for t in existing if re.fullmatch(rf"episode/{re.escape(slug)}-v\d+", t))
    tag = f"episode/{slug}-v{n}"

    main_mp4 = out / f"{slug}.mp4"
    manifest = {
        "schema": 1, "slug": slug, "tag": tag, "issue": args.issue,
        "validation": {k: validation.get(k) for k in ("target_seconds", "audio_mean_db", "caption_cues", "script_sha256")},
        "bilibili": {
            "asset": main_mp4.name, "sha256": sha256(main_mp4),
            "title_zh": script.get("title_zh") or script.get("title_en"),
            "description_zh": (script.get("description_zh") or script.get("description_en", ""))
                              + "\n\n字幕:视频内置中英双语字幕。\n源文件与制作记录: https://github.com/"
                              + os.environ.get("GITHUB_REPOSITORY", "") + f"/tree/main/videos/{slug}",
            "tags": script.get("tags_zh") or ["科普", "知识分享"],
            "tid": script.get("bilibili_tid", 201),
            "cover_asset": f"{slug}.cover.jpg" if (out / f"{slug}.cover.jpg").exists() else None,
        },
    }
    publish_json = out / "PUBLISH.json"
    publish_json.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    publish_md = out / "PUBLISH.md"
    publish_md.write_text(
        f"# Publish manifest: {slug}\n\nMechanical instructions for any upload executor. The fenced JSON is ground truth.\n\n"
        f"1. Download `{main_mp4.name}` from release `{tag}` and verify its sha256.\n"
        f"2. Upload to Bilibili with the title, description, tags and cover below (tools/publish_worker.py does this).\n"
        f"3. Comment the BV link on issue #{args.issue or '?'} and move its label to `state:published`.\n\n"
        "```json\n" + json.dumps(manifest, ensure_ascii=False, indent=2) + "\n```\n")
    sums = out / "SHA256SUMS.txt"
    sums.write_text("".join(f"{sha256(p)}  {p.name}\n" for p in deliverables))
    uploads = deliverables + [publish_json, publish_md, sums]
    if args.dry_run:
        print(tag); [print("  would upload", p.name) for p in uploads]
        return 0
    create = ["gh", "release", "create", tag, "--title", script.get("title_en", slug),
              "--notes", f"Episode {slug}, release v{n}. See PUBLISH.md for the publish manifest; "
                         f"REVIEW.md in videos/{slug}/ records what was verified."]
    if os.environ.get("GITHUB_SHA"):
        # Tag the commit that was actually rendered, not whatever the default branch moved to.
        create += ["--target", os.environ["GITHUB_SHA"]]
    subprocess.run(create, check=True)
    subprocess.run(["gh", "release", "upload", tag, *map(str, uploads), "--clobber"], check=True)
    for p in uploads:
        print(f"https://github.com/{os.environ.get('GITHUB_REPOSITORY','')}/releases/download/{tag}/{p.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
