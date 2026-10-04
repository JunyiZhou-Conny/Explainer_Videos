#!/usr/bin/env python3
"""Scaffold a new explainer-video project for one or more library papers.

    python tools/new_video.py schulman2017ppo
    python tools/new_video.py shao2024grpo yu2025dapo --id grpo-to-dapo --title "From GRPO to DAPO"

Creates videos/<id>/ with video.yaml, a script.md skeleton, scenes/common.py, a first scene,
exercises.md, and page images of each paper in assets/. Then follow docs/WORKFLOW.md.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import catalog  # noqa: E402

ROOT = catalog.ROOT

COMMON = '''"""Shared settings for this video: semantic colours, assets, and the narration from script.md."""

from pathlib import Path

from explainer import style as S
from explainer.script import load_narration

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
ASSETS = PROJECT / "assets"

# Semantic colours — one meaning per colour for the whole video (list them in script.md too).
MAIN = S.BLUE
CONTRAST = S.ORANGE
HIGHLIGHT = S.YELLOW
DIM = S.GREY

NARRATION = load_narration(PROJECT / "script.md")
'''

SCENE = '''"""S01 · {title}"""

from manim import *

from explainer import style as S
from explainer.components import paper_page
from explainer.scene import VoiceScene

from common import ASSETS, NARRATION

SAY = NARRATION["S01"]


class Intro(VoiceScene):
    def construct(self):
        img, frame = paper_page(ASSETS / "{first}_p1.png", height=6.8)
        page = Group(img, frame).to_edge(LEFT, buff=0.8)
        title = S.text({title!r}, 40).next_to(page, RIGHT, buff=0.6)
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(page, shift=RIGHT * 0.4), run_time=1.0)
            self.play(Write(title), run_time=vo.remaining())
        self.play(FadeOut(Group(*self.mobjects)))
'''

SCRIPT = '''# {title} — narration script & visual plan

Papers: {papers}

Audience: {audience}

Conventions
- `SAY:` lines are spoken verbatim (one voiceover block each) and become subtitles. Spell out symbols.
- `SHOW:` lines describe the visuals for the following `SAY:` line.
- Semantic colours: (fill in — e.g. "x = BLUE, x' = ORANGE, epsilon = YELLOW")

---

## S01 · Hook — `s01_intro.py` · `Intro`

SHOW: (a concrete, surprising situation the paper resolves)
SAY: (one or two sentences)

## S02 · Where this paper sits — `s02_map.py` · `Lineage`

SHOW: timeline of the papers before this one (paper cards), arrows into this paper
SAY: ...
'''

EXERCISES = '''# Exercises — {title}

Work these *before* re-watching. Answers are folded below each question.

1. (question)
   <details><summary>Answer</summary>

   (answer)
   </details>
'''


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("papers", nargs="+", help="paper ids from library/catalog.yaml")
    ap.add_argument("--id", help="video id / folder name (default: first paper id)")
    ap.add_argument("--title")
    ap.add_argument("--audience", default="curious newcomer to the field")
    args = ap.parse_args(argv)

    cat = catalog.load()
    by_id = {p["id"]: p for p in cat.get("papers") or []}
    missing = [p for p in args.papers if p not in by_id]
    if missing:
        ap.error(f"unknown paper id(s): {', '.join(missing)}")
    vid = args.id or args.papers[0]
    title = args.title or by_id[args.papers[0]]["title"]
    proj = ROOT / "videos" / vid
    if proj.exists():
        ap.error(f"{proj} already exists")
    (proj / "scenes").mkdir(parents=True)
    (proj / "assets").mkdir()

    for pid in args.papers:
        pdf = ROOT / by_id[pid]["pdf"]
        subprocess.run(["pdftoppm", "-png", "-r", "200", "-f", "1", "-l", "1", "-singlefile",
                        str(pdf), str(proj / "assets" / f"{pid}_p1")], check=True)

    spec = {
        "id": vid, "title": title, "papers": args.papers, "audience": args.audience,
        "voice": {"backend": "kokoro", "voice": "af_heart", "speed": 1.0},
        "scenes": [{"file": "scenes/s01_intro.py", "cls": "Intro", "title": "Hook"}],
    }
    (proj / "video.yaml").write_text(yaml.safe_dump(spec, sort_keys=False, allow_unicode=True))
    (proj / "script.md").write_text(SCRIPT.format(
        title=title, audience=args.audience,
        papers="; ".join(f"{by_id[p]['title']} ({by_id[p].get('year', '')}) — `{by_id[p]['pdf']}`"
                         for p in args.papers)))
    (proj / "scenes" / "common.py").write_text(COMMON)
    (proj / "scenes" / "s01_intro.py").write_text(SCENE.format(title=title, first=args.papers[0]))
    (proj / "exercises.md").write_text(EXERCISES.format(title=title))
    print(f"created {proj.relative_to(ROOT)}/ — next: write script.md (see docs/WORKFLOW.md)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
