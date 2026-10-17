"""Lint a scene without rendering frames: anything off-frame, text under 20 pt, leftovers at the end.

    python -m explainer.check videos/<id>/scenes/s08_payoff.py Payoff [--lang zh] [--tts silent]

Runs the scene as a Manim dry run (narration audio comes from the TTS cache, so timings are
real) and, after every play()/wait(), reports:
  OUT    a visible mobject outside the safe area x in [-6.6, 6.6], y in [-3.6, 3.6]
  SMALL  a Text / MathTex rendered below 20 pt
  BAND   a visible mobject dipping into the reserved caption band (the bottom 170 of 1080
         pixel rows; in scene units y below -2.74 on the default frame). Only for projects
         that burn captions in overlay mode (episode.json route): legacy video.yaml
         projects scale the whole picture above the band, so their scenes may use the full
         frame and are skipped, as are portrait shorts and full-bleed backdrops. Set
         EXPLAINER_CAPTION_RESERVE to the band height in pixels for other presets, or 0 to
         disable. Policy: this lint is deliberately stricter than the pixel gate
         (explainer.style_check excuses a uniformly scene-painted band; here any in-band
         ink is advice to move it, and a preset route that paints its own band disables
         the lint via the environment variable).
and at the end lists mobjects still visible (scenes should end on an empty frame). For a short-format
BeatScene the HUD (fixed in the frame) may be tiny and a scene may end with objects on screen (they
carry over into the next shot); its length in bars is printed instead.
"""

from __future__ import annotations

import importlib.util
import os
import sys
import tempfile
from pathlib import Path

import numpy as np

XL, YL, MIN_PT = 6.6, 3.6, 19.5


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    lang = tts = None
    if "--lang" in argv:                    # python -m explainer.check <file> <Class> --lang zh
        i = argv.index("--lang")
        lang = argv[i + 1]
        del argv[i:i + 2]
    if "--tts" in argv:                     # e.g. --tts silent for a quick layout check
        i = argv.index("--tts")
        tts = argv[i + 1]
        del argv[i:i + 2]
        os.environ["EXPLAINER_TTS"] = tts
    if len(argv) != 2:
        print(__doc__)
        return 2
    scene_file, cls_name = Path(argv[0]).resolve(), argv[1]
    project = scene_file.parent.parent
    environ_before = dict(os.environ)       # main() mutates env/cwd/sys.path; restore for
    cwd_before = os.getcwd()                # in-process callers (tests, future tooling)
    path_before = list(sys.path)
    reserve = float(os.environ.get("EXPLAINER_CAPTION_RESERVE", "170"))  # px rows of 1080; 0 disables
    if (project / "video.yaml").exists():   # the video's own voice (and language), as preview uses
        # Legacy route: burn() scales the picture above the band, so scenes own the full frame.
        reserve = 0.0
        import yaml

        from .build import scene_env
        spec = yaml.safe_load((project / "video.yaml").read_text())
        os.environ.update({k: v for k, v in scene_env(spec, tts, lang or "en").items()
                           if k.startswith("EXPLAINER_")})
        os.environ["EXPLAINER_PROJECT"] = str(project)
    sys.path.insert(0, str(scene_file.parent))
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

    from manim import Scene, SingleStringMathTex, Text, VMobject, tempconfig
    from manim import config as mconfig

    seen: set = set()
    problems = 0

    def visible(m) -> bool:
        if not isinstance(m, VMobject) or len(m.points) == 0:
            return False
        fo = max([0, *m.get_fill_opacities()])
        so = max([0, *m.get_stroke_opacities()]) if m.get_stroke_width() > 0 else 0
        return fo > 0.02 or so > 0.02

    def leaves(m):
        if isinstance(m, (Text, SingleStringMathTex)):
            yield m, getattr(m, "text", None) or getattr(m, "tex_string", "")
            return
        if isinstance(m, VMobject) and len(m.points):
            yield m, ""
        for s in m.submobjects:
            yield from leaves(s)

    def bbox(m):
        pts = [s.points for s in m.get_family() if isinstance(s, VMobject) and len(s.points) and visible(s)]
        if not pts:
            return None
        p = np.concatenate(pts)
        return p[:, 0].min(), p[:, 1].min(), p[:, 0].max(), p[:, 1].max()

    def check(scene):
        nonlocal problems
        t = scene.renderer.time
        hud = {id(x) for m in getattr(scene.renderer.camera, "fixed_mobjects", []) for x in m.get_family()}
        fw, fh = mconfig.frame_width, mconfig.frame_height
        # The presets reserve the bottom RESERVE of 1080 pixel rows for burned captions;
        # dry runs render at other pixel sizes, so work in frame units via the fraction.
        band_top = None
        if reserve > 0 and fw > fh and getattr(scene, "grid", None) is None:
            band_top = -fh / 2 + reserve / 1080 * fh
        for top in scene.mobjects:
            for m, label in leaves(top):
                if isinstance(m, (Text, SingleStringMathTex)):
                    bb = bbox(m)
                else:  # a plain shape: only its own points
                    bb = None
                    if len(m.points) and visible(m):
                        p = m.points
                        bb = p[:, 0].min(), p[:, 1].min(), p[:, 0].max(), p[:, 1].max()
                if bb is None:
                    continue
                x0, y0, x1, y1 = bb
                if x0 < -XL - 0.01 or x1 > XL + 0.01 or y0 < -YL - 0.01 or y1 > YL + 0.01:
                    key = ("out", id(m), round(x0, 1), round(y0, 1), round(x1, 1), round(y1, 1))
                    if key not in seen:
                        seen.add(key)
                        problems += 1
                        print(f"[{t:6.2f}s] OUT   {type(m).__name__} x[{x0:.2f}, {x1:.2f}] "
                              f"y[{y0:.2f}, {y1:.2f}] {label!r:.60}")
                if (band_top is not None and y0 < band_top - 0.01
                        and not (x1 - x0 >= 0.95 * fw and y1 - y0 >= 0.95 * fh)):  # backdrops may
                    key = ("band", id(m), round(x0, 1), round(y0, 1))
                    if key not in seen:
                        seen.add(key)
                        problems += 1
                        print(f"[{t:6.2f}s] BAND  {type(m).__name__} dips to y={y0:.2f}; "
                              f"captions own y < {band_top:.2f} {label!r:.60}")
                if isinstance(m, (Text, SingleStringMathTex)) and id(m) not in hud:   # (HUD: tiny on purpose)
                    fs = getattr(m, "font_size", None)
                    if fs is not None and fs < MIN_PT:
                        key = ("small", id(m), round(fs, 1))
                        if key not in seen:
                            seen.add(key)
                            problems += 1
                            print(f"[{t:6.2f}s] SMALL {fs:.1f}pt {type(m).__name__} {label!r:.60}")

    orig_play, orig_wait = Scene.play, Scene.wait

    def play(self, *a, **k):
        orig_play(self, *a, **k)
        check(self)

    def wait(self, *a, **k):
        orig_wait(self, *a, **k)
        check(self)

    Scene.play, Scene.wait = play, wait

    try:
        spec = importlib.util.spec_from_file_location(scene_file.stem, scene_file)
        mod = importlib.util.module_from_spec(spec)
        os.chdir(scene_file.parent.parent)
        spec.loader.exec_module(mod)
        with tempfile.TemporaryDirectory() as media, tempconfig({
                "dry_run": True, "quality": "low_quality", "disable_caching": True,
                "progress_bar": "none", "verbosity": "WARNING", "media_dir": media}):
            scene = getattr(mod, cls_name)()
            scene.render()
            left = [m for m in scene.mobjects if any(visible(s) for s in m.get_family())]
            print(f"end at {scene.renderer.time:.1f}s; {len(left)} visible mobject(s) left on screen")
            for m in left:
                print("  LEFT:", type(m).__name__)
            if getattr(scene, "grid", None) is not None:  # a short: shots hand objects on (match cuts)
                bar = scene.grid.bar
                off = scene.renderer.time / bar - round(scene.renderer.time / bar)
                print(f"short: {scene.renderer.time / bar:.2f} bars" + ("" if abs(off) < 1e-3 else "  (NOT on a bar line)"))
                left = []
    finally:
        Scene.play, Scene.wait = orig_play, orig_wait  # repeated in-process calls must not stack wrappers
        os.environ.clear()
        os.environ.update(environ_before)
        os.chdir(cwd_before)
        sys.path[:] = path_before
    print("OK" if problems == 0 and not left else f"{problems + len(left)} problem(s)")
    return 0 if problems == 0 and not left else 1


if __name__ == "__main__":
    sys.exit(main())
