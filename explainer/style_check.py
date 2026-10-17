"""Pixel checks against a preset's tokens: does the render actually wear the style?

Samples frames from a CLEAN (pre-burn) render and asserts measurable invariants from
presets/<id>.tokens.json: the background colour dominates within tolerance, and the
reserved caption band holds nothing but background (the presets promise that area to the
subtitles). The band is checked twice: as a whole (97% clear) and tile by tile, because a
small tag can hide inside a 3% global tolerance — any ~120x42px tile that is more than
`checks.band_tile_tolerance` (default 15%) non-background is an intrusion, and a tile is
excused as a scene-painted band only when it is almost entirely band-coloured, so
ink-coloured objects are caught even where ink equals the band colour (swiss). These are
guardrails against a silent style drift, not a design review.

  .venv/bin/python -m explainer.style_check outputs/<slug>/<slug>.clean.mp4 --preset swiss
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

from .styles import tokens


def _hex_rgb(value: str) -> tuple[int, int, int]:
    v = value.lstrip("#")
    return int(v[0:2], 16), int(v[2:4], 16), int(v[4:6], 16)


def sample_frames(movie: Path, count: int, out_dir: Path) -> list[Path]:
    duration = float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
         str(movie)], text=True))
    frames = []
    for i in range(count):
        t = duration * (i + 0.5) / count
        frame = out_dir / f"frame-{i:02d}.png"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", str(movie),
                        "-frames:v", "1", str(frame)], check=True)
        frames.append(frame)
    return frames


def check_frames(frames: list[Path], preset: str) -> list[str]:
    """Problems found; empty means the sampled frames satisfy the tokens."""
    import numpy as np
    from PIL import Image

    t = tokens(preset)
    bg = np.array(_hex_rgb(t["palette"]["background"]), dtype=float)
    band_colour = np.array(_hex_rgb(t.get("captions", {}).get("band_colour",
                                                              t["palette"]["background"])), dtype=float)
    checks = t.get("checks", {})
    bg_tol = float(checks.get("background_tolerance", 30))
    band_tol = float(checks.get("band_tolerance", 40))
    min_share = float(checks.get("min_background_share", 0.35))
    tile_tol = float(checks.get("band_tile_tolerance", 0.15))
    reserve = int(t.get("captions", {}).get("reserve_px", 0))
    problems = []
    for frame in frames:
        img = np.asarray(Image.open(frame).convert("RGB"), dtype=float)
        height = img.shape[0]
        dist = np.sqrt(((img - bg) ** 2).sum(axis=2))
        share = float((dist < bg_tol).mean())
        if share < min_share:
            problems.append(f"{frame.name}: background {t['palette']['background']} covers "
                            f"{share:.0%} < {min_share:.0%} of the frame")
        if reserve:
            band = img[height - reserve:, :, :]
            near_bg = np.sqrt(((band - bg) ** 2).sum(axis=2)) < band_tol
            near_band = np.sqrt(((band - band_colour) ** 2).sum(axis=2)) < band_tol
            clear = float((near_bg | near_band).mean())
            if clear < 0.97:
                problems.append(f"{frame.name}: the reserved caption band (bottom {reserve}px) is "
                                f"only {clear:.0%} background — diagrams are intruding on the "
                                "subtitle area")
            problems += _band_tiles(frame.name, near_bg, near_band, tile_tol, height - reserve)
    return problems


def _band_tiles(name: str, near_bg, near_band, tile_tol: float,
                band_y: int, rows: int = 4, cols: int = 16) -> list[str]:
    """Concentrated intrusions the global share misses: flag tiles mostly not background.

    A tile that is almost entirely band-coloured counts as a scene-painted band and is
    excused; a small object merely the same colour as the band sits in a mixed tile and
    is still caught."""
    import numpy as np

    h, w = near_bg.shape
    intruding = ~near_bg
    hits = []
    worst = 0.0
    for r in range(rows):
        y0, y1 = h * r // rows, h * (r + 1) // rows
        for c in range(cols):
            x0, x1 = w * c // cols, w * (c + 1) // cols
            share = float(intruding[y0:y1, x0:x1].mean())
            if share > tile_tol and float(near_band[y0:y1, x0:x1].mean()) < 0.95:
                hits.append((x0, y0, x1, y1))
                worst = max(worst, share)
    if not hits:
        return []
    xs0, ys0, xs1, ys1 = (min(t[0] for t in hits), min(t[1] for t in hits),
                          max(t[2] for t in hits), max(t[3] for t in hits))
    return [f"{name}: object intruding on the caption band around x {xs0}-{xs1}px, "
            f"y {band_y + ys0}-{band_y + ys1}px ({len(hits)} tile(s), worst {worst:.0%} "
            "non-background)"]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("movie", type=Path, help="the clean (pre-burn) render")
    ap.add_argument("--preset", required=True)
    ap.add_argument("--frames", type=int, default=6)
    args = ap.parse_args(argv)
    with tempfile.TemporaryDirectory() as td:
        frames = sample_frames(args.movie, args.frames, Path(td))
        problems = check_frames(frames, args.preset)
    for p in problems:
        print(f"STYLE {p}", file=sys.stderr)
    if not problems:
        print(f"Style check passed: {args.frames} frames match the {args.preset} tokens.")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
