"""Golden-frame regression: has a re-render silently changed frames it should not have?

A golden file stores coarse signatures of frames sampled from the CLEAN (pre-burn) render:
each frame reduced to a 32x18 grid of mean colours (a ~60x60px cell at 1080p), small enough
to commit as text, precise enough to locate a moved or recoloured element to one cell. On
the next full build, episode.py re-samples and fails the build on any drift, printing the
pixel region that changed — so an unintended layout change is caught before review instead
of during it.

Sampling is PER SCENE, at fractions of each scene's own duration, never at absolute times:
scene durations come from the narration (frame_budget redistributes them whenever any line
changes), so an absolute time would drift off its visual beat on every faithful re-render.
Instead, each sample is stored as (scene, fraction) and re-anchored to the current plan's
scene offsets at check time; update() nudges each sample onto a settled frame (one that
equals its successor), and check() accepts a match within +/-2 frames, absorbing sub-frame
cue drift from TTS re-synthesis. A scene whose own duration moved beyond half a frame is
reported as "narration timing changed", which is a different finding than layout drift —
review it, then accept the new cut:

  .venv/bin/python -m explainer.golden update outputs/<slug>/<slug>.clean.mp4 \
      --golden videos/<slug>/golden.json
  .venv/bin/python -m explainer.golden check  outputs/<slug>/<slug>.clean.mp4 \
      --golden videos/<slug>/golden.json [--save-diffs outputs/<slug>/golden-diffs]

The CLI reads scene offsets from plan.json next to the movie; episode.py passes them
directly. Episodes opt in by committing videos/<slug>/golden.json; episodes without one
build as before. Cell-mean colours are insensitive to encoder noise and antialiasing (which
move a mean by a level or two), so the default distance threshold of 18 never fires on a
faithful re-render but does on anything a reviewer could see.
"""
from __future__ import annotations

import argparse
import base64
import binascii
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

GRID_W, GRID_H = 32, 18
SCHEMA = 2
SAMPLE_FRACTIONS = (0.35, 0.7)  # per scene; clamped away from entrances and the finish fade
EDGE_START_S = 0.3              # never sample earlier than this into a scene
EDGE_END_S = 0.6                # never sample later than this before a scene's end
DEFAULT_TOLERANCE = 18.0        # euclidean RGB distance between a cell's mean colours
DURATION_SLACK = 0.05           # seconds a scene's duration may move before timing changed
MATCH_WINDOW = 2                # frames each side a sample may shift and still match


def _probe(movie: Path) -> tuple[float, float]:
    """(video stream duration, fps) — the stream, not the container: audio padding can
    make the container outlast the last video frame."""
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=duration,r_frame_rate", "-of", "json", str(movie)], text=True)
    stream = json.loads(out)["streams"][0]
    num, den = stream["r_frame_rate"].split("/")
    return float(stream["duration"]), float(num) / float(den)


def _extract(movie: Path, t: float, out: Path) -> Path | None:
    """One frame as PNG, or None when t is past the last video frame (ffmpeg exits 0
    without writing the file there)."""
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{max(t, 0):.3f}", "-i",
                    str(movie), "-frames:v", "1", str(out)], check=True)
    return out if out.is_file() else None


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


def scenes_from_plan(movie: Path) -> list[dict]:
    """[{id, start, duration}] from the plan.json the build wrote next to the movie."""
    plan_path = movie.parent / "plan.json"
    if not plan_path.is_file():
        raise SystemExit(f"{plan_path} not found — run from a full build's output "
                         "directory, or pass scene offsets programmatically")
    plan = json.loads(plan_path.read_text())
    scenes, start = [], 0.0
    for s in plan["scenes"]:
        scenes.append({"id": s["id"], "start": start, "duration": float(s["duration"])})
        start += float(s["duration"])
    return scenes


def _sample_times(scene: dict) -> list[float]:
    lo = scene["start"] + EDGE_START_S
    hi = scene["start"] + scene["duration"] - EDGE_END_S
    if hi <= lo:  # very short scene: one midpoint sample
        return [scene["start"] + scene["duration"] / 2]
    return sorted({min(max(scene["start"] + f * scene["duration"], lo), hi)
                   for f in SAMPLE_FRACTIONS})


def update(movie: Path, golden_path: Path, scenes: list[dict],
           tolerance: float = DEFAULT_TOLERANCE) -> dict:
    video_end, fps = _probe(movie)
    entries = []
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        for scene in scenes:
            samples = []
            cap = scene["start"] + max(scene["duration"] / 2,
                                       scene["duration"] - EDGE_END_S)
            for t in _sample_times(scene):
                # Settle: prefer a frame identical to its successor, so the sample sits in
                # a still moment rather than mid-animation; nudge forward a few times. The
                # stored frac must name the frame actually captured, so t is clamped
                # BEFORE extraction and never advanced after the final attempt.
                for nudge in range(4):
                    t = min(t, cap, video_end - 1.5 / fps)
                    png = _extract(movie, t, td / "a.png")
                    nxt = _extract(movie, min(t + 1 / fps, video_end - 0.5 / fps), td / "b.png")
                    if png and (not nxt or not changed_cells(signature(png), signature(nxt),
                                                             tolerance)):
                        break
                    if nudge < 3:
                        t += 0.25
                if png is None:
                    continue
                samples.append({"frac": round((t - scene["start"]) / scene["duration"], 4),
                                "sig": base64.b64encode(signature(png)).decode()})
            entries.append({"id": scene["id"], "duration": round(scene["duration"], 3),
                            "samples": samples})
    golden = {"schema": SCHEMA, "source": movie.name, "fps": fps,
              "grid": [GRID_W, GRID_H], "tolerance": tolerance, "scenes": entries}
    golden_path.parent.mkdir(parents=True, exist_ok=True)
    golden_path.write_text(json.dumps(golden, indent=2) + "\n")
    return golden


def check(movie: Path, golden_path: Path, scenes: list[dict],
          save_diffs: Path | None = None) -> list[str]:
    """Problems found; empty means every sampled frame matches its golden signature."""
    regen = ("regenerate with python -m explainer.golden update after reviewing the cut")
    golden = json.loads(golden_path.read_text())
    if golden.get("schema") != SCHEMA or golden.get("grid") != [GRID_W, GRID_H]:
        return [f"{golden_path}: unsupported schema/grid — {regen}"]
    if not golden.get("scenes"):
        return [f"{golden_path}: no scenes stored — {regen}"]
    tolerance = float(golden.get("tolerance", DEFAULT_TOLERANCE))
    video_end, fps = _probe(movie)
    current = {s["id"]: s for s in scenes}
    if save_diffs is not None:  # hold exactly this run's failing frames, never stale ones
        shutil.rmtree(save_diffs, ignore_errors=True)
    problems = []
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        for stored in golden["scenes"]:
            scene = current.get(stored["id"])
            if scene is None:
                problems.append(f"scene {stored['id']} is not in the current cut — {regen}")
                continue
            if abs(scene["duration"] - float(stored["duration"])) > DURATION_SLACK:
                problems.append(
                    f"narration timing changed in {stored['id']} "
                    f"({stored['duration']}s -> {scene['duration']:.3f}s) — its frames are "
                    f"not comparable; {regen}")
                continue
            for sample in stored["samples"]:
                try:
                    sig = base64.b64decode(sample["sig"], validate=True)
                except (binascii.Error, KeyError, TypeError):
                    return [f"{golden_path}: corrupted signature in {stored['id']} — {regen}"]
                if len(sig) != GRID_W * GRID_H * 3:
                    return [f"{golden_path}: corrupted signature in {stored['id']} — {regen}"]
                t = scene["start"] + float(sample["frac"]) * scene["duration"]
                # Accept a match within +/-MATCH_WINDOW frames: sub-frame cue drift from
                # TTS re-synthesis moves a beat slightly without changing the layout.
                best_cells, best_png = None, None
                for df in (0, 1, -1, 2, -2):
                    png = _extract(movie, min(t + df / fps, video_end - 0.5 / fps),
                                   td / "c.png")
                    if png is None:
                        continue
                    cells = changed_cells(sig, signature(png), tolerance)
                    if not cells:
                        best_cells = []
                        break
                    if best_cells is None or len(cells) < len(best_cells):
                        best_cells, best_png = cells, td / "kept.png"
                        shutil.copyfile(png, best_png)
                if best_cells is None:
                    problems.append(f"{stored['id']} t={t:.2f}s: the video stream ends "
                                    f"before this sample — {regen}")
                    continue
                if not best_cells:
                    continue
                problems.append(_report(stored["id"], t, best_cells, best_png, save_diffs))
    return problems


def _report(scene_id: str, t: float, cells: list[tuple[int, int]], png: Path,
            save_diffs: Path | None) -> str:
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
            marked.save(save_diffs / f"{scene_id}-t{t:.2f}.png")
    return (f"{scene_id} t={t:.2f}s: {len(cells)} cell(s) changed around "
            f"x {x0}-{x1}px, y {y0}-{y1}px")


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
    ck = sub.add_parser("check", help="compare a render against stored signatures")
    ck.add_argument("movie", type=Path)
    ck.add_argument("--golden", type=Path, required=True)
    ck.add_argument("--save-diffs", type=Path, default=None,
                    help="write frames with changed cells outlined in red here")
    args = ap.parse_args(argv)
    scenes = scenes_from_plan(args.movie)
    if args.cmd == "update":
        golden = update(args.movie, args.golden, scenes)
        n = sum(len(s["samples"]) for s in golden["scenes"])
        print(f"Golden stored: {n} samples across {len(golden['scenes'])} scenes of "
              f"{args.movie.name} -> {args.golden}")
        return 0
    problems = check(args.movie, args.golden, scenes, args.save_diffs)
    for p in problems:
        print(f"GOLDEN {p}", file=sys.stderr)
    if not problems:
        print(f"Golden check passed: {args.movie.name} matches {args.golden.name}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
