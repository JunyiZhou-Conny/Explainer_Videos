"""Lint a scene without rendering frames: anything off-frame, text under 20 pt, leftovers at the end.

    python -m explainer.check videos/<id>/scenes/s08_payoff.py Payoff [--lang zh] [--tts silent]

Runs the scene as a Manim dry run (narration audio comes from the TTS cache, so timings are
real) and, after every play()/wait(), reports:
  OUT    a visible mobject outside the safe area x in [-6.6, 6.6], y in [-3.6, 3.6]
  SMALL  a Text / MathTex rendered below 20 pt
and at the end lists mobjects still visible (scenes should end on an empty frame).
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
    if (project / "video.yaml").exists():   # the video's own voice (and language), as preview uses
        import yaml

        from .build import scene_env
        spec = yaml.safe_load((project / "video.yaml").read_text())
        os.environ.update({k: v for k, v in scene_env(spec, tts, lang or "en").items()
                           if k.startswith("EXPLAINER_")})
        os.environ["EXPLAINER_PROJECT"] = str(project)
    sys.path.insert(0, str(scene_file.parent))
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

    from manim import Scene, SingleStringMathTex, Text, VMobject, tempconfig

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
                if isinstance(m, (Text, SingleStringMathTex)):
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
    print("OK" if problems == 0 and not left else f"{problems + len(left)} problem(s)")
    return 0 if problems == 0 and not left else 1


if __name__ == "__main__":
    sys.exit(main())
