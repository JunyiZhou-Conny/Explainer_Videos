"""Render a whole video project into one narrated mp4 with subtitles and chapter marks.

    python -m explainer.build videos/<video-id>                 # 1080p60 final
    python -m explainer.build videos/<video-id> -q l            # fast 480p15 draft
    python -m explainer.build videos/<video-id> --only s03,s04  # re-render some scenes, reuse the rest
    python -m explainer.build videos/<video-id> --no-render     # just re-stitch existing renders

Reads <project>/video.yaml:

    id: dp-01-calibrating-noise
    title: "..."
    papers: [dwork2006calibrating]          # ids from library/catalog.yaml
    voice: {backend: kokoro, voice: af_heart, speed: 1.0}
    scenes:
      - {file: scenes/s01_hook.py, cls: Hook, title: "The differencing attack"}

    parts:                                   # optional: also cut the video into parts
      - {id: part1, title: "...", scenes: [s01_hook, s02_map]}

Writes <project>/output/<id>.mp4, <id>.srt, chapters.txt (YouTube/Bilibili format), transcript.md,
and <id>_<part>.mp4 / .srt / chapters_<part>.txt for each part.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import textwrap
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import yaml

from . import REPO_ROOT

QUALITY_DIRS = {"l": "480p15", "m": "720p30", "h": "1080p60", "p": "1440p60", "k": "2160p60"}


def load_project(project: Path) -> dict:
    spec = yaml.safe_load((project / "video.yaml").read_text())
    spec.setdefault("id", project.name)
    return spec


def scene_env(spec: dict, tts: str | None) -> dict:
    env = dict(os.environ)
    v = spec.get("voice", {}) or {}
    env.setdefault("EXPLAINER_TTS", v.get("backend", "kokoro"))
    if tts:
        env["EXPLAINER_TTS"] = tts
    if v.get("voice") and "EXPLAINER_VOICE" not in os.environ:
        env["EXPLAINER_VOICE"] = str(v["voice"])
    if v.get("speed") and "EXPLAINER_SPEED" not in os.environ:
        env["EXPLAINER_SPEED"] = str(v["speed"])
    env["PYTHONPATH"] = os.pathsep.join(filter(None, [str(REPO_ROOT), env.get("PYTHONPATH")]))
    return env


def media_dir(project: Path, quality: str, scene: dict) -> Path:
    # one media (and LaTeX) dir per scene: parallel renders must not share Manim's Tex cache,
    # whose temp files collide when two processes typeset the same formula at once
    return project / "build" / f"media_{quality}" / Path(scene["file"]).stem


def scene_movie(project: Path, quality: str, scene: dict) -> Path:
    stem = Path(scene["file"]).stem
    return media_dir(project, quality, scene) / "videos" / stem / QUALITY_DIRS[quality] / f"{scene['cls']}.mp4"


def render_scene(project: Path, quality: str, scene: dict, env: dict) -> Path:
    cmd = [sys.executable, "-m", "manim", "render", f"-q{quality}", "--disable_caching", "--no_latex_cleanup",
           "--media_dir", str(media_dir(project, quality, scene)), scene["file"], scene["cls"]]
    log = project / "build" / "logs" / f"{Path(scene['file']).stem}_{scene['cls']}.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    with open(log, "w") as fh:
        res = subprocess.run(cmd, cwd=project, env=env, stdout=fh, stderr=subprocess.STDOUT)
    if res.returncode != 0:
        tail = "\n".join(log.read_text().splitlines()[-30:])
        raise RuntimeError(f"render failed for {scene['cls']} (see {log}):\n{tail}")
    out = scene_movie(project, quality, scene)
    if not out.exists():
        raise FileNotFoundError(out)
    for line in log.read_text(errors="replace").splitlines():
        if "anchor not found" in line:
            print(f"  WARNING {scene['cls']}: {line.strip()}", flush=True)
    print(f"  rendered {scene['cls']:<24} -> {out.relative_to(project)}", flush=True)
    return out


def ffprobe_duration(path: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                        "csv=p=0", str(path)], capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


def has_audio(path: Path) -> bool:
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries",
                        "stream=index", "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    return bool(r.stdout.strip())


def normalize(src: Path, dst: Path, crf: int | None = None) -> None:
    """Same audio layout for every scene (48 kHz stereo AAC, padded to video length).

    With `crf`, the video is re-encoded once here (x264, tuned for flat animation), so the full
    video and every part are later joined without re-encoding."""
    vcodec = ["-c:v", "copy"] if crf is None else [
        "-c:v", "libx264", "-preset", "medium", "-tune", "animation", "-crf", str(crf), "-pix_fmt", "yuv420p"]
    if has_audio(src):
        cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(src), *vcodec, "-af",
               "aresample=48000,apad", "-ac", "2", "-c:a", "aac", "-b:a", "192k", "-shortest", str(dst)]
    else:
        cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(src), "-f", "lavfi", "-i",
               "anullsrc=r=48000:cl=stereo", *vcodec, "-c:a", "aac", "-b:a", "192k",
               "-shortest", str(dst)]
    subprocess.run(cmd, check=True)


def fmt_srt(t: float) -> str:
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def fmt_chapter(t: float) -> str:
    t = int(t)
    return f"{t // 3600}:{t % 3600 // 60:02d}:{t % 60:02d}" if t >= 3600 else f"{t // 60:02d}:{t % 60:02d}"


def split_cues(start: float, end: float, text: str, width: int = 44, lines: int = 2):
    """Break one narration clip into readable cues (<= 2 lines each), never across sentences,
    timed proportionally to characters."""
    import re

    sentences = [x for x in re.split(r"(?<=[.!?])\s+", text) if x.strip()] or [text]
    chunks = []
    for sent in sentences:
        wrapped = textwrap.wrap(sent, width)
        chunks += [" ".join(wrapped[i:i + lines]) for i in range(0, len(wrapped), lines)]
    total = sum(len(c) for c in chunks) or 1
    t, cues = start, []
    for c in chunks:
        dt = (end - start) * len(c) / total
        cues.append((t, t + dt, "\n".join(textwrap.wrap(c, width))))
        t += dt
    return cues


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project", type=Path)
    ap.add_argument("-q", "--quality", default="h", choices=list(QUALITY_DIRS))
    ap.add_argument("--only", help="comma-separated scene file stems or class names to (re)render")
    ap.add_argument("--no-render", action="store_true", help="only stitch existing scene renders")
    ap.add_argument("--jobs", type=int, default=max(1, (os.cpu_count() or 2) // 2))
    ap.add_argument("--tts", help="override the voice backend (kokoro|elevenlabs|edge|espeak|silent)")
    ap.add_argument("--crf", type=int, help="re-encode each scene with x264 at this CRF (smaller files; ~25 is good)")
    ap.add_argument("--render-only", action="store_true", help="render the selected scenes, don't stitch")
    args = ap.parse_args(argv)

    project = args.project.resolve()
    spec = load_project(project)
    scenes = spec["scenes"]
    env = scene_env(spec, args.tts)
    only = set(args.only.split(",")) if args.only else None

    if args.no_render:
        todo = []
    elif only is not None:  # exactly the named scenes
        todo = [s for s in scenes if Path(s["file"]).stem in only or s["cls"] in only]
    else:                   # whatever has not been rendered yet
        todo = [s for s in scenes if not scene_movie(project, args.quality, s).exists()]
    if todo:
        # synthesize narration once, serially, so parallel renders don't race on the TTS cache
        print(f"Rendering {len(todo)} scene(s) at {QUALITY_DIRS[args.quality]} "
              f"with TTS={env['EXPLAINER_TTS']} (jobs={args.jobs})", flush=True)
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            list(pool.map(lambda s: render_scene(project, args.quality, s, env), todo))
    if args.render_only:
        return

    build = project / "build" / f"stitch_{args.quality}"
    build.mkdir(parents=True, exist_ok=True)
    out_dir = project / "output"
    out_dir.mkdir(exist_ok=True)

    normalized = []
    for i, s in enumerate(scenes):
        movie = scene_movie(project, args.quality, s)
        if not movie.exists():
            raise SystemExit(f"missing render for {s['cls']}: {movie}")
        norm = build / f"{i:02d}_{s['cls']}{'' if args.crf is None else f'_crf{args.crf}'}.mp4"
        if not norm.exists() or norm.stat().st_mtime < movie.stat().st_mtime:
            normalize(movie, norm, args.crf)
        normalized.append((s, movie, norm))

    suffix = "" if args.quality == "h" else "_" + QUALITY_DIRS[args.quality]
    title = spec.get("title", spec["id"])
    stitch(normalized, out_dir / f"{spec['id']}{suffix}", title, build, chapters_file=out_dir / "chapters.txt",
           transcript_file=out_dir / "transcript.md")
    for part in spec.get("parts") or []:
        keep = set(part["scenes"])
        subset = [t for t in normalized if Path(t[0]["file"]).stem in keep or t[0]["cls"] in keep]
        stitch(subset, out_dir / f"{spec['id']}_{part['id']}{suffix}", part.get("title", part["id"]), build,
               chapters_file=out_dir / f"chapters_{part['id']}.txt")


def stitch(items, stem: Path, title: str, build: Path, chapters_file: Path,
           transcript_file: Path | None = None) -> None:
    """Concatenate normalized scene files into stem.mp4 (+ .srt, chapters, transcript)."""
    srt, chapters, transcript, offset = [], [], [f"# {title}\n"], 0.0
    for s, movie, norm in items:
        name = s.get("title", s["cls"])
        if s.get("chapter", True):
            chapters.append(f"{fmt_chapter(offset)} {name}")
        transcript.append(f"\n## {fmt_chapter(offset)} — {name}\n")
        subs_file = movie.with_suffix(".subs.json")
        for cue in (json.loads(subs_file.read_text()) if subs_file.exists() else []):
            transcript.append(cue["text"] + "\n")
            srt.extend(split_cues(offset + cue["start"], offset + cue["end"], cue["text"]))
        offset += ffprobe_duration(norm)

    listing = build / f"concat_{stem.name}.txt"
    listing.write_text("".join(f"file '{n}'\n" for _, _, n in items))
    joined = build / f"joined_{stem.name}.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(listing),
                    "-c", "copy", str(joined)], check=True)
    final = stem.with_suffix(".mp4")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(joined), "-c:v", "copy", "-af",
                    "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "128k",
                    "-movflags", "+faststart", str(final)], check=True)
    joined.unlink(missing_ok=True)
    stem.with_suffix(".srt").write_text("".join(
        f"{n}\n{fmt_srt(a)} --> {fmt_srt(b)}\n{t}\n\n" for n, (a, b, t) in enumerate(srt, 1)))
    chapters_file.write_text("\n".join(chapters) + "\n")
    if transcript_file:
        transcript_file.write_text("".join(transcript))
    print(f"Done: {final.name}  ({fmt_chapter(offset)}, {final.stat().st_size / 1e6:.1f} MB) + .srt, "
          f"{chapters_file.name}")


if __name__ == "__main__":
    main()
