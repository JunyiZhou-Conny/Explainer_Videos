"""Golden-frame regression: has a re-render silently changed frames it should not have?

A golden file stores coarse signatures of frames sampled from the CLEAN (pre-burn) render:
each frame reduced to a 32x18 grid of mean colours (a ~60x60px cell at 1080p), small enough
to commit as text, precise enough to locate a moved or recoloured element to one cell. On
the next full build, episode.py re-samples the same times and fails the build on any drift,
printing the pixel region that changed — so an unintended layout change is caught before
review instead of during it. An INTENDED change is accepted by regenerating the file:

  .venv/bin/python -m explainer.golden update outputs/<slug>/<slug>.clean.mp4 \
      --golden videos/<slug>/golden.json
  .venv/bin/python -m explainer.golden check  outputs/<slug>/<slug>.clean.mp4 \
      --golden videos/<slug>/golden.json [--save-diffs outputs/<slug>/golden-diffs]

Episodes opt in by committing videos/<slug>/golden.json; episodes without one build as
before. Cell-mean colours are insensitive to encoder noise and antialiasing (which move a
mean by a level or two), so the default distance threshold of 18 never fires on a faithful
re-render but does on anything a reviewer could see.
"""
from __future__ import annotations

import argparse
import base64
import json
import subprocess
import sys
import tempfile
from pathlib import Path

GRID_W, GRID_H = 32, 18
SCHEMA = 1
DEFAULT_FRAMES = 12
DEFAULT_TOLERANCE = 18.0   # euclidean RGB distance between a cell's mean colours
DURATION_SLACK = 0.1       # seconds; beyond this the stored times no longer line up


def _duration(movie: Path) -> float:
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
         str(movie)], text=True))


def _extract(movie: Path, t: float, out: Path) -> Path:
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", str(movie),
                    "-frames:v", "1", str(out)], check=True)
    return out


def frame_times(duration: float, count: int) -> list[float]:
    return [duration * (i + 0.5) / count for i in range(count)]


def signature(frame: Path) -> bytes:
    """GRID_H x GRID_W cells of mean RGB, row-major, 3 bytes per cell."""
    import numpy as np
    from PIL import Image

    img = Image.open(frame).convert("RGB").resize((GRID_W, GRID_H), Image.BOX)
    return np.asarray(img, dtype=np.uint8).tobytes()


def changed_cells(a: bytes, b: bytes, tolerance: float) -> list[tuple[int, int]]:
    """(row, col) of cells whose mean colour moved beyond the tolerance."""
    import numpy as np

    pa = np.frombuffer(a, dtype=np.uint8).reshape(GRID_H, GRID_W, 3).astype(float)
    pb = np.frombuffer(b, dtype=np.uint8).reshape(GRID_H, GRID_W, 3).astype(float)
    dist = np.sqrt(((pa - pb) ** 2).sum(axis=2))
    return [(int(r), int(c)) for r, c in zip(*np.nonzero(dist > tolerance))]


def update(movie: Path, golden_path: Path, count: int = DEFAULT_FRAMES) -> dict:
    duration = _duration(movie)
    frames = []
    with tempfile.TemporaryDirectory() as td:
        for i, t in enumerate(frame_times(duration, count)):
            png = _extract(movie, t, Path(td) / f"g-{i:02d}.png")
            frames.append({"t": round(t, 3),
                           "sig": base64.b64encode(signature(png)).decode()})
    golden = {"schema": SCHEMA, "source": movie.name, "duration": round(duration, 3),
              "grid": [GRID_W, GRID_H], "tolerance": DEFAULT_TOLERANCE, "frames": frames}
    golden_path.parent.mkdir(parents=True, exist_ok=True)
    golden_path.write_text(json.dumps(golden, indent=2) + "\n")
    return golden


def check(movie: Path, golden_path: Path, save_diffs: Path | None = None) -> list[str]:
    """Problems found; empty means every sampled frame matches its golden signature."""
    golden = json.loads(golden_path.read_text())
    if golden.get("schema") != SCHEMA or golden.get("grid") != [GRID_W, GRID_H]:
        return [f"{golden_path}: unsupported schema/grid — regenerate with "
                "python -m explainer.golden update"]
    tolerance = float(golden.get("tolerance", DEFAULT_TOLERANCE))
    duration = _duration(movie)
    if abs(duration - float(golden["duration"])) > DURATION_SLACK:
        return [f"duration {duration:.3f}s differs from the golden {golden['duration']}s "
                "by more than 0.1s — the stored sample times no longer line up; review the "
                "cut, then regenerate the golden file"]
    problems = []
    with tempfile.TemporaryDirectory() as td:
        for i, entry in enumerate(golden["frames"]):
            png = _extract(movie, float(entry["t"]), Path(td) / f"c-{i:02d}.png")
            cells = changed_cells(base64.b64decode(entry["sig"]), signature(png), tolerance)
            if not cells:
                continue
            from PIL import Image
            with Image.open(png) as img:
                w, h = img.size
                cw, ch = w / GRID_W, h / GRID_H
                x0 = int(min(c for _, c in cells) * cw)
                x1 = int((max(c for _, c in cells) + 1) * cw)
                y0 = int(min(r for r, _ in cells) * ch)
                y1 = int((max(r for r, _ in cells) + 1) * ch)
                if save_diffs is not None:
                    save_diffs.mkdir(parents=True, exist_ok=True)
                    marked = img.convert("RGB")
                    _mark(marked, cells, cw, ch)
                    marked.save(save_diffs / f"t-{entry['t']}.png")
            problems.append(f"t={entry['t']}s: {len(cells)} cell(s) changed around "
                            f"x {x0}-{x1}px, y {y0}-{y1}px")
    return problems


def _mark(img, cells: list[tuple[int, int]], cw: float, ch: float) -> None:
    from PIL import ImageDraw

    draw = ImageDraw.Draw(img)
    for r, c in cells:
        draw.rectangle([c * cw, r * ch, (c + 1) * cw - 1, (r + 1) * ch - 1],
                       outline="#FF0000", width=3)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    up = sub.add_parser("update", help="store golden signatures for this render")
    up.add_argument("movie", type=Path)
    up.add_argument("--golden", type=Path, required=True)
    up.add_argument("--frames", type=int, default=DEFAULT_FRAMES)
    ck = sub.add_parser("check", help="compare a render against stored signatures")
    ck.add_argument("movie", type=Path)
    ck.add_argument("--golden", type=Path, required=True)
    ck.add_argument("--save-diffs", type=Path, default=None,
                    help="write frames with changed cells outlined in red here")
    args = ap.parse_args(argv)
    if args.cmd == "update":
        golden = update(args.movie, args.golden, args.frames)
        print(f"Golden stored: {len(golden['frames'])} frames of {args.movie.name} "
              f"-> {args.golden}")
        return 0
    problems = check(args.movie, args.golden, args.save_diffs)
    for p in problems:
        print(f"GOLDEN {p}", file=sys.stderr)
    if not problems:
        print(f"Golden check passed: {args.movie.name} matches {args.golden.name}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
