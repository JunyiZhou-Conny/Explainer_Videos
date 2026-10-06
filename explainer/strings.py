"""Inventory every piece of on-screen text a video creates (for translation and review).

    python -m explainer.strings videos/<id>                  # all scenes -> build/strings.json
    python -m explainer.strings videos/<id> --only s03_stop  # some scenes

Each scene runs as a Manim dry run (no frames; narration from the TTS cache) in its own process,
with Text / MarkupText / Paragraph / Tex / MathTex / Code constructors patched to record the string,
the kind, the font size and the line in the scene (or helper) file that created it. Identical
(kind, text) entries are merged with all their call sites.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

RUNNER = r'''
import importlib.util, inspect, json, os, sys, tempfile
from pathlib import Path
scene_file, cls_name, out, project = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4])
toolkit = Path(sys.argv[5])
sys.path.insert(0, str(scene_file.parent)); sys.path.insert(0, str(toolkit.parent))
import manim
from manim import Code, MarkupText, MathTex, Paragraph, Tex, Text, tempconfig
records = []

def site():
    for fr in inspect.stack()[2:]:
        p = Path(fr.filename).resolve()
        if p.name == "style.py" and p.parent == toolkit:
            continue
        if project in p.parents or p.parent == toolkit:
            return f"{p.relative_to(project) if project in p.parents else 'explainer/' + p.name}:{fr.lineno}"
    return "?"

def patch(cls, kind, getter):
    orig = cls.__init__
    def init(self, *a, **k):
        try:
            texts = getter(a, k)
            for t in (texts if isinstance(texts, list) else [texts]):
                records.append({"kind": kind, "text": t, "size": k.get("font_size"), "site": site()})
        except Exception as e:  # never break the scene
            records.append({"kind": kind, "text": f"<unreadable: {e}>", "size": None, "site": site()})
        orig(self, *a, **k)
    cls.__init__ = init

# the i18n hooks translate each string argument separately, so record them separately
patch(Text, "text", lambda a, k: a[0] if a else k.get("text"))
patch(MarkupText, "markup", lambda a, k: a[0] if a else k.get("text"))
patch(Paragraph, "paragraph", lambda a, k: list(a))
patch(MathTex, "mathtex", lambda a, k: [x for x in a if isinstance(x, str)])
patch(Tex, "tex", lambda a, k: [x for x in a if isinstance(x, str)])
patch(Code, "code", lambda a, k: k.get("code_string") or k.get("code_file") or "")
spec = importlib.util.spec_from_file_location(scene_file.stem, scene_file)
mod = importlib.util.module_from_spec(spec)
os.chdir(project)
spec.loader.exec_module(mod)
with tempfile.TemporaryDirectory() as media, tempconfig({"dry_run": True, "quality": "low_quality",
        "disable_caching": True, "progress_bar": "none", "verbosity": "ERROR", "media_dir": media}):
    getattr(mod, cls_name)().render()
out.write_text(json.dumps(records, ensure_ascii=False))
'''


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project", type=Path)
    ap.add_argument("--only", help="comma-separated scene file stems or class names")
    ap.add_argument("--lang", default=os.environ.get("EXPLAINER_LANG", "en"))
    ap.add_argument("-o", "--out", type=Path)
    args = ap.parse_args(argv)

    import yaml

    from .build import scene_env

    project = args.project.resolve()
    spec = yaml.safe_load((project / "video.yaml").read_text())
    env = {**scene_env(spec, None), "EXPLAINER_LANG": args.lang}
    only = set(args.only.split(",")) if args.only else None
    toolkit = Path(__file__).resolve().parent
    merged: dict[tuple, dict] = {}
    order = []
    tmp = project / "build" / "strings_tmp"
    tmp.mkdir(parents=True, exist_ok=True)
    for s in spec["scenes"]:
        stem = Path(s["file"]).stem
        if only and stem not in only and s["cls"] not in only:
            continue
        out = tmp / f"{stem}.json"
        r = subprocess.run([sys.executable, "-c", RUNNER, str(project / s["file"]), s["cls"], str(out),
                            str(project), str(toolkit)], env=env, capture_output=True, text=True)
        if r.returncode != 0:
            print(f"!! {stem}: dry run failed\n{r.stderr[-3000:]}")
            continue
        recs = json.loads(out.read_text())
        print(f"{stem:<24} {len(recs):5d} text objects")
        for rec in recs:
            key = (rec["kind"], rec["text"])
            if key not in merged:
                merged[key] = {"kind": rec["kind"], "text": rec["text"], "sizes": set(), "sites": set(),
                               "scenes": set(), "count": 0}
                order.append(key)
            m = merged[key]
            m["count"] += 1
            m["sites"].add(rec["site"])
            m["scenes"].add(stem)
            if rec["size"] is not None:
                m["sizes"].add(round(float(rec["size"]), 1))
    rows = [{**merged[k], "sizes": sorted(merged[k]["sizes"]), "sites": sorted(merged[k]["sites"]),
             "scenes": sorted(merged[k]["scenes"])} for k in order]
    dest = args.out or project / "build" / f"strings.{args.lang}.json"
    dest.write_text(json.dumps(rows, ensure_ascii=False, indent=1))
    kinds: dict[str, int] = {}
    for r in rows:
        kinds[r["kind"]] = kinds.get(r["kind"], 0) + 1
    print(f"{len(rows)} distinct strings {kinds} -> {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
