"""What does import speciesot load? Swiss scenes.

On-screen code is copied from the commits named in SOURCES.md, or marked as the
2026-10-14 upload when no commit exists. Content stays above y = -2.45.
"""
import json
import os
from pathlib import Path

from manim import *
from explainer.scene import VoiceScene
from explainer.styles import swiss
from explainer.styles.swiss import (
    PAPER, INK, RED, GRAY, at, left, line, card, folder,
)

swiss.setup_fonts()
config.background_color = PAPER
MONO = "DejaVu Sans Mono"


def mono(s, size=26, color=INK):
    return Text(s, font=MONO, font_size=size, color=color)


def code_card(lines, x, y, w=6.2):
    h = 0.42 * len(lines) + 0.45
    frame = Rectangle(width=w, height=h, stroke_color=INK, stroke_width=2,
                      fill_color=PAPER, fill_opacity=1).move_to([x, y, 0])
    text = VGroup(*[mono(row, 22) for row in lines]).arrange(DOWN, buff=0.12)
    text.move_to(frame.get_center())
    return VGroup(frame, text)


def ponder(zh, en, y=-1.15):
    frame = Rectangle(width=10.2, height=1.85, stroke_color=RED, stroke_width=3,
                      fill_color=PAPER, fill_opacity=1).move_to([0, y, 0])
    q = at("想一想 / PAUSE AND PONDER", 0, y + 0.52, 22, RED, bold=True)
    z = at(zh, 0, y + 0.05, 28, INK, 9.4)
    e = at(en, 0, y - 0.48, 22, GRAY, 9.4)
    return VGroup(frame, q, z, e)


class EpisodeScene(VoiceScene):
    pad_after_clip = 0.18
    total = "06"

    def setup(self):
        super().setup()
        self.camera.background_color = PAPER
        plan = json.loads(Path(os.environ["EPISODE_PLAN"]).read_text())
        self.spec = next(s for s in plan["scenes"] if s["id"].upper() == self.__class__.__name__)

    def header(self, name):
        ident = self.spec["id"][1:]
        self.add(line(-6.3, 3.42, 6.3, 3.42),
                 left("CONNY / EXPLAINER STUDIES", -6.3, 3.67, 15),
                 at(f"{ident} / {self.total}", 5.85, 3.67, 16, RED))
        self.play(FadeIn(left(name, -6.3, 2.85, 40, INK, 12.2, True), shift=UP * 0.1), run_time=0.4)
        self.add(left(self.spec["title_zh"], -6.3, 2.30, 20, GRAY, 12))

    def say(self, i):
        return self.voiceover(self.spec["lines"][i]["en"])

    def cue(self, vo, f, *anims, run_time=0.6):
        delay = vo.duration * f - vo.elapsed
        if delay > 0.04:
            self.wait(delay)
        self.play(*anims, run_time=run_time)

    def dim_for_ponder(self):
        dims = [m for m in self.mobjects if isinstance(m, VMobject)]
        if dims:
            self.play(VGroup(*dims).animate.set_opacity(0.15), run_time=0.45)

    def finish(self):
        remaining = self.spec["duration"] - self.renderer.time
        if remaining > 0.37:
            self.wait(remaining - 0.30)
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.30)
        elif remaining > 0.015:
            self.wait(remaining)


class S01(EpisodeScene):
    def construct(self):
        self.header("Which file answered?")
        with self.say(0) as vo:
            books = folder("notebooks/", -4.5, 0.55, 3.3)
            cap = folder("speciesOT/", 0, 0.55, 3.3)
            src = folder("src/", 4.5, 0.55, 3.3)
            self.cue(vo, 0.08, FadeIn(books), FadeIn(cap), FadeIn(src))
            cmd = mono("from speciesot import Experiment", 26).move_to([0, -1.15, 0])
            vo.wait_until("import Experiment")
            self.play(Write(cmd), run_time=0.7)
        with self.say(1) as vo:
            vo.wait_until("not the owner")
            self.play(Create(line(-5.9, 1.15, -3.1, -0.05, RED, 5)), run_time=0.45)
        with self.say(2) as vo:
            vo.wait_until("which file")
            self.dim_for_ponder()
            self.play(FadeIn(ponder("两个文件都定义了 Experiment，import 的是哪一个？",
                                    "If two files define Experiment, which one loaded?")), run_time=0.45)
        self.finish()


class S02(EpisodeScene):
    def construct(self):
        self.header("The installer looks in src")
        with self.say(0) as vo:
            repo = folder("speciesOT repo", -3.8, 0.4, 4.2)
            self.cue(vo, 0.15, FadeIn(repo))
            mark = at("not a full scan", -3.8, -0.7, 24, GRAY)
            vo.wait_until("project file")
            self.play(FadeIn(mark), run_time=0.4)
        with self.say(1) as vo:
            shown = code_card(['[tool.setuptools.packages.find]', 'where = ["src"]'], 2.6, 0.35, 6.4)
            vo.wait_until("where equals src")
            self.play(FadeIn(shown, shift=LEFT * 0.2), run_time=0.6)
            only = Arrow(shown.get_left(), repo.get_right(), buff=0.12, color=RED, stroke_width=3)
            self.play(Create(only), run_time=0.5)
        with self.say(2) as vo:
            cite = at("pyproject.toml  lines 19-20", 2.6, -1.35, 22, RED)
            vo.wait_until("Those two lines")
            self.play(FadeIn(cite), run_time=0.4)
        self.finish()


class S03(EpisodeScene):
    def construct(self):
        self.header("One import is the door")
        with self.say(0) as vo:
            box = folder("src/speciesot/", 0, 0.7, 5.2)
            self.cue(vo, 0.12, FadeIn(box))
            vo.wait_until("three lines")
            self.play(FadeIn(at("3 lines", 0, -0.35, 28, RED, bold=True)), run_time=0.4)
        with self.say(1) as vo:
            shown = code_card(["from .speciesot_core import Experiment"], 0, -1.15, 8.4)
            vo.wait_until("Line one")
            self.play(FadeIn(shown, shift=UP * 0.1), run_time=0.55)
        with self.say(2) as vo:
            alias = at("the name is an alias", 0, 1.7, 28, INK)
            vo.wait_until("alias")
            self.play(FadeIn(alias), run_time=0.4)
        self.finish()


class S04(EpisodeScene):
    def construct(self):
        self.header("The name lands on the class")
        init = card("__init__.py", "imports Experiment", -4.3, 0.55, 3.4, 1.7)
        klass = card("Experiment", "speciesot_core.py", 0.2, 0.55, 3.6, 1.7, accent=True)
        train = card("train()", "no extra arguments", 4.4, 0.55, 3.3, 1.7)
        with self.say(0) as vo:
            self.cue(vo, 0.1, FadeIn(init))
            vo.wait_until("lands on the class")
            hop = Arrow(init.get_right(), klass.get_left(), buff=0.12, color=RED, stroke_width=3)
            self.play(Create(hop), FadeIn(klass), run_time=0.8)
        with self.say(1) as vo:
            snippet = code_card(["def train(self):", "    model.train()"], 0.2, -1.25, 4.8)
            vo.wait_until("yaml path")
            self.play(FadeIn(train), FadeIn(snippet), run_time=0.6)
        with self.say(2) as vo:
            note = at("128 lines in git. No scGenModel.", 0, -2.05, 24, RED)
            vo.wait_until("one hundred twenty eight")
            self.play(FadeIn(note), run_time=0.4)
        self.finish()


class S05(EpisodeScene):
    def construct(self):
        self.header("Two files, one name")
        git = card("in git", "128 lines", -3.2, 0.7, 4.0, 2.0)
        up = card("upload", "346 lines", 3.2, 0.7, 4.0, 2.0, accent=True)
        with self.say(0) as vo:
            self.cue(vo, 0.12, FadeIn(git), FadeIn(up))
            vo.wait_until("scGen model")
            tag = at("has scGenModel", 3.2, -0.55, 24, RED, bold=True)
            self.play(FadeIn(tag), run_time=0.4)
        with self.say(1) as vo:
            missing = at("not a commit on main", 3.2, -1.15, 24, GRAY)
            vo.wait_until("not a commit")
            self.play(FadeIn(missing), run_time=0.45)
        with self.say(2) as vo:
            vo.wait_until("which of these two")
            self.dim_for_ponder()
            self.play(FadeIn(ponder("笔记本导入的是已经安装的那一份。是哪一份？",
                                    "The notebook imported the installed file. Which one?")), run_time=0.45)
        self.finish()


class S06(EpisodeScene):
    def construct(self):
        self.header("The path, once")
        steps = VGroup(
            card("1  pyproject", "where = src", -4.2, 0.45, 3.5, 1.8),
            card("2  __init__", "import Experiment", 0, 0.45, 3.6, 1.8, accent=True),
            card("3  class", "speciesot_core.py", 4.2, 0.45, 3.6, 1.8),
        )
        with self.say(0) as vo:
            self.cue(vo, 0.1, FadeIn(steps[0]))
            vo.wait_until("Init imports")
            self.play(FadeIn(steps[1]), FadeIn(steps[2]), run_time=0.7)
        with self.say(1) as vo:
            caller = at("a notebook only calls", 0, -1.15, 28, INK)
            vo.wait_until("caller")
            self.play(FadeIn(caller), run_time=0.4)
        with self.say(2) as vo:
            tryit = at("open src/speciesot/__init__.py", 0, -1.85, 26, RED)
            vo.wait_until("init file")
            self.play(FadeIn(tryit), run_time=0.4)
        self.finish()
