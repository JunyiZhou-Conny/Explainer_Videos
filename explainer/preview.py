"""Fast layout check for one scene: render low-res, then dump a contact sheet of frames.

    python -m explainer.preview videos/<id>/scenes/s01_hook.py Hook
    python -m explainer.preview <file> <Class> --every 1.5           # denser sheet
    python -m explainer.preview <file> <Class> --at 3.2,10 -q m      # exact frames at 720p
    python -m explainer.preview <file> <Class> --tts silent          # skip TTS (timings approximate)

Prints the paths of the sheet PNGs (4x4 grid, timestamp burned into each tile) so you can
open them and look for overlaps, clipped text and empty stretches.
"""

from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from pathlib import Path

from .build import QUALITY_DIRS, ffprobe_duration, scene_env

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def find_project(scene_file: Path) -> Path:
    for p in [scene_file.parent, *scene_file.parents]:
        if (p / "video.yaml").exists():
            return p
    return scene_file.parent


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", type=Path)
    ap.add_argument("cls")
    ap.add_argument("-q", "--quality", default="l", choices=list(QUALITY_DIRS))
    ap.add_argument("--every", type=float, default=2.0, help="seconds between sheet tiles")
    ap.add_argument("--at", help="comma-separated timestamps for full-size frames")
    ap.add_argument("--tts", help="voice backend override (e.g. silent)")
    ap.add_argument("--no-render", action="store_true")
    ap.add_argument("--movie", type=Path, help="make sheets from this existing mp4 instead of rendering")
    args = ap.parse_args(argv)

    scene_file = args.file.resolve()
    project = find_project(scene_file)
    import yaml
    spec = yaml.safe_load((project / "video.yaml").read_text()) if (project / "video.yaml").exists() else {}
    env = scene_env(spec, args.tts)
    media = project / "build" / f"preview_{args.quality}"
    out = media / "videos" / scene_file.stem / QUALITY_DIRS[args.quality] / f"{args.cls}.mp4"
    if args.movie:
        out, args.no_render = args.movie.resolve(), True
    if not args.no_render:
        r = subprocess.run([sys.executable, "-m", "manim", "render", f"-q{args.quality}",
                            "--disable_caching", "--media_dir", str(media), str(scene_file), args.cls],
                           cwd=project, env=env, capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stdout[-4000:], r.stderr[-6000:], sep="\n")
            raise SystemExit("render failed")
    dur = ffprobe_duration(out)
    sheets_dir = project / "build" / "sheets" / f"{scene_file.stem}_{args.cls}"
    sheets_dir.mkdir(parents=True, exist_ok=True)
    for old in sheets_dir.glob("*.png"):
        old.unlink()

    n = max(1, math.ceil(dur / args.every))
    rows = min(4, math.ceil(n / 4))
    vf = (f"drawtext=fontfile={FONT}:text='%{{pts\\:hms}}':x=8:y=8:fontsize=h/18:"
          f"fontcolor=yellow:box=1:boxcolor=black@0.6,fps=1/{args.every},scale=480:-2,"
          f"tile=4x{rows}:padding=6:margin=6:color=white")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(out), "-vf", vf,
                    str(sheets_dir / "sheet_%02d.png")], check=True)
    frames = []
    for t in (args.at.split(",") if args.at else []):
        f = sheets_dir / f"frame_{float(t):07.2f}.png"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", t, "-i", str(out), "-frames:v", "1",
                        str(f)], check=True)
        frames.append(f)

    subs = out.with_suffix(".subs.json")
    print(f"movie:    {out}  ({dur:.1f}s)")
    if subs.exists():
        for c in json.loads(subs.read_text()):
            print(f"  [{c['start']:6.1f}-{c['end']:6.1f}] {c['text'][:90]}")
    for s in sorted(sheets_dir.glob("sheet_*.png")):
        print(f"sheet:    {s}")
    for f in frames:
        print(f"frame:    {f}")


if __name__ == "__main__":
    main()
