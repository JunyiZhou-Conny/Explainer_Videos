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
    the committed script.json, or REVIEW.md lacks the human sign-off line (recorded with
    the phrase "human review" or "listening sign-off").
 3. Create release episode/<slug>-vN (N = 1 + existing releases of this slug), upload
    the MP4(s), subtitles, chapters and SHA256SUMS.txt plus PUBLISH.json / PUBLISH.md.
 4. Print the asset URLs; the catalog updater consumes them.

A legacy-route episode (videos/<slug>/video.yaml, no script.json; built by explainer.build
into videos/<slug>/output/) has no render-time sidecar. For it the validation is measured
here, from the stitched files: both cuts present and the same length, every part present,
loudness, bilingual cue count, and whether the regenerated subtitle files equal the
committed ones (they do when the release render reproduces the reviewed one). Its Bilibili
title, description and tags come from the `publish:` block of video.yaml; the uploaded
asset is the copy with the bilingual subtitles burned in (<slug>.zh-en.mp4).
.github/workflows/legacy-release.yml renders such an episode scene by scene and calls this.

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


SIGNOFF_PHRASES = ("human review", "listening sign-off")


def require_signoff(episode: Path) -> None:
    review = (episode / "REVIEW.md").read_text() if (episode / "REVIEW.md").exists() else ""
    if not any(phrase in review.lower() for phrase in SIGNOFF_PHRASES):
        raise SystemExit(
            "REVIEW.md lacks a human-review record; the lifecycle requires Conny's listening "
            "sign-off before release (AGENTS.md). Record it with the phrase 'human review' "
            "or 'listening sign-off'."
        )


def probe_seconds(path: Path) -> float:
    out = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                   "-of", "csv=p=0", str(path)], text=True)
    return round(float(out.strip()), 3)


def integrated_loudness(path: Path) -> float | None:
    """EBU R128 integrated loudness of the first audio stream, in LUFS."""
    res = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-map", "0:a:0",
                          "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True)
    found = re.findall(r"I:\s+(-?[\d.]+) LUFS", res.stderr)
    return float(found[-1]) if found else None


def srt_cues(path: Path) -> list[list[str]]:
    """The text lines of each cue of an .srt file."""
    blocks = re.split(r"\n\s*\n", path.read_text(encoding="utf-8").strip())
    return [b.splitlines()[2:] for b in blocks if len(b.splitlines()) >= 3 and "-->" in b.splitlines()[1]]


PUBLISH_KEYS = ("title_zh", "description_zh", "tags_zh", "tid")


def legacy_spec(episode: Path) -> dict:
    """video.yaml, refused unless its `publish:` block holds everything a Bilibili upload needs.
    No defaults: a missing tid would file the video under the episode.json route's partition."""
    import yaml
    spec = yaml.safe_load((episode / "video.yaml").read_text())
    publish = spec.get("publish") or {}
    missing = [k for k in PUBLISH_KEYS if not publish.get(k)]
    if missing:
        raise SystemExit(f"video.yaml's publish block lacks {', '.join('publish.' + k for k in missing)}: "
                         "write the Bilibili title_zh, description_zh, tags_zh and tid before releasing.")
    if not isinstance(publish["tags_zh"], list) or not str(publish["tid"]).isdigit():
        raise SystemExit("publish.tags_zh must be a list and publish.tid a Bilibili partition number.")
    return spec


def legacy_preflight(episode: Path) -> dict:
    """What .github/workflows/legacy-release.yml checks before it spends an hour of runners:
    the sign-off and the publish block; then the scenes to render, one job each, and whether
    any of them typesets with LaTeX (the runners skip the TeX packages otherwise)."""
    require_signoff(episode)
    spec = legacy_spec(episode)
    tex = re.compile(r"\b(MathTex|Tex|SingleStringMathTex)\(|\bS\.(math|tex)\(")
    latex = any(tex.search(p.read_text()) for p in (episode / "scenes").glob("*.py"))
    return {"scenes": [Path(s["file"]).stem for s in spec["scenes"]], "latex": latex}


def legacy_inputs(episode: Path, out: Path) -> tuple[str, dict, dict, list[Path], Path]:
    """Title, Bilibili metadata, measured validation, deliverables and the uploaded MP4 of a
    video.yaml episode stitched by explainer.build (see the module docstring)."""
    spec = legacy_spec(episode)
    vid = spec["id"]
    publish = spec["publish"]
    full, burned = out / f"{vid}.mp4", out / f"{vid}.zh-en.mp4"
    for need in (full, burned, out / f"{vid}.zh-en.srt"):
        if not need.exists():
            raise SystemExit(f"No {need}; stitch with `python -m explainer.build {episode} --no-render --burn` first.")
    seconds = {p.name: probe_seconds(p) for p in (full, burned)}
    if abs(seconds[full.name] - seconds[burned.name]) > 0.5:
        raise SystemExit(f"The clean and the burned cut differ in length: {seconds}")
    parts = []
    for part in spec.get("parts") or []:
        movie = out / f"{vid}_{part['id']}.mp4"
        if not movie.exists():
            raise SystemExit(f"No {movie}: every part in video.yaml is released with the full cut.")
        seconds[movie.name] = probe_seconds(movie)
        parts.append(movie)
    cues = srt_cues(out / f"{vid}.zh-en.srt")
    one_language = sum(1 for lines in cues if len(lines) < 2)
    if not cues or one_language:
        raise SystemExit(f"{vid}.zh-en.srt: {len(cues)} cues, {one_language} without both languages.")
    committed = subprocess.run(["git", "diff", "--quiet", "--", str(out)], cwd=ROOT,
                               capture_output=True).returncode == 0
    validation = {
        "route": "video.yaml", "source_commit": os.environ.get("GITHUB_SHA") or subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "seconds": seconds, "loudness_lufs": integrated_loudness(full), "caption_cues": len(cues),
        "subtitles_match_committed": committed,
    }
    (out / f"{vid}.validation.json").write_text(json.dumps(validation, ensure_ascii=False, indent=2))
    keep = {".mp4", ".srt", ".ass"}
    deliverables = sorted(p for p in out.iterdir() if p.is_file() and (
        p.suffix in keep or re.fullmatch(r"chapters(_\w+)?\.txt", p.name) or p.name == f"{vid}.validation.json"))
    main_mp4 = out / (publish.get("asset") or burned.name)
    meta = {"title_zh": publish["title_zh"], "title_en": publish.get("title_en") or spec.get("title", vid),
            "description_zh": publish["description_zh"], "tags_zh": [str(t) for t in publish["tags_zh"]],
            "bilibili_tid": int(publish["tid"])}
    return meta["title_en"], meta, validation, deliverables, main_mp4


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("episode", type=Path, help="videos/<slug>")
    ap.add_argument("--outputs", type=Path, help="rendered deliverables (default outputs/<slug>, or "
                                                  "videos/<slug>/output for a video.yaml episode)")
    ap.add_argument("--issue", type=int, help="the episode's issue number, for the publish worker")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--preflight", action="store_true", help="video.yaml episode: check the sign-off and the "
                    "publish block, print scenes=[...] and latex=true|false for $GITHUB_OUTPUT, and stop")
    args = ap.parse_args()
    episode = args.episode.resolve()
    slug = episode.name
    legacy = not (episode / "script.json").exists() and (episode / "video.yaml").exists()
    if args.preflight:
        if not legacy:
            raise SystemExit(f"--preflight is for video.yaml episodes; {episode} has none (or has script.json)")
        plan = legacy_preflight(episode)
        print("scenes=" + json.dumps(plan["scenes"]))
        print("latex=" + str(plan["latex"]).lower())
        return 0
    if legacy:
        out = (args.outputs or episode / "output").resolve()
        require_signoff(episode)
        title_en, script, validation, deliverables, main_mp4 = legacy_inputs(episode, out)
        manifest_validation = validation
    else:
        out = (args.outputs or ROOT / "outputs" / slug).resolve()
        script = json.loads((episode / "script.json").read_text())
        validation_path = out / f"{slug}.validation.json"
        if not validation_path.exists():
            raise SystemExit(f"No {validation_path}; render the full episode first.")
        validation = json.loads(validation_path.read_text())
        committed = hashlib.sha256((episode / "script.json").read_bytes()).hexdigest()
        if validation.get("script_sha256") != committed:
            raise SystemExit("validation.json was made from a different script.json than the one committed. Re-render.")
        require_signoff(episode)
        deliverables = sorted(p for p in out.iterdir() if p.suffix in {".mp4", ".srt", ".ass"}
                              or p.name.endswith(".chapters.txt"))
        deliverables = [p for p in deliverables if not p.name.startswith("sample-")
                        and ".clean." not in p.name and ".scored." not in p.name]
        main_mp4 = out / f"{slug}.mp4"
        title_en = script.get("title_en", slug)
        manifest_validation = {k: validation.get(k) for k in
                               ("target_seconds", "audio_mean_db", "caption_cues", "script_sha256")}
    if not any(p.suffix == ".mp4" for p in deliverables):
        raise SystemExit(f"No final MP4 under {out}")
    if not main_mp4.exists():
        raise SystemExit(f"No {main_mp4} to publish")

    token_env = {k: v for k, v in os.environ.items()}
    if args.dry_run and not os.environ.get("GITHUB_REPOSITORY"):
        existing = []                     # a local dry run: no repository to ask, call it v1
    else:
        existing = subprocess.check_output(["gh", "api", f"repos/{os.environ['GITHUB_REPOSITORY']}/releases",
                                            "--paginate", "--jq", ".[].tag_name"], text=True, env=token_env).split()
    n = 1 + sum(1 for t in existing if re.fullmatch(rf"episode/{re.escape(slug)}-v\d+", t))
    tag = f"episode/{slug}-v{n}"

    manifest = {
        "schema": 1, "slug": slug, "tag": tag, "issue": args.issue,
        "validation": manifest_validation,
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
    create = ["gh", "release", "create", tag, "--title", title_en,
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
