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
        self.header("Only one of them is a test")
        folder_box = folder("Tests/", 0, 1.15, 3.4)
        a = card("test_evaluation.py", "one test function", -3.3, -0.35, 4.4, 1.6, accent=True)
        b = card("test_model.py", "no test function", 3.3, -0.35, 4.2, 1.6)
        with self.say(0) as vo:
            self.cue(vo, 0.1, FadeIn(folder_box))
            vo.wait_until("Only one")
            self.play(FadeIn(a), FadeIn(b), run_time=0.55)
        with self.say(1) as vo:
            vo.wait_until("never collects")
            self.play(Create(line(1.4, 0.15, 5.2, -0.7, RED, 4)), run_time=0.4)
        with self.say(2) as vo:
            vo.wait_until("failed test")
            self.dim_for_ponder()
            self.play(FadeIn(ponder("setup 崩了，你会看到失败的测试，还是测试还没开始就崩了？",
                                    "If setup crashes, is that a failed test?")), run_time=0.45)
        self.finish()


class S02(EpisodeScene):
    def construct(self):
        self.header("Pytest keeps one kind of name")
        with self.say(0) as vo:
            rule = at("keep names that start with test_", 0, 1.5, 30, RED, bold=True)
            self.cue(vo, 0.12, FadeIn(rule))
        with self.say(1) as vo:
            kept = card("kept", "test_mmd_is_zero...", -3.2, 0.1, 4.6, 1.6, accent=True)
            dropped = card("dropped", "test_model.py", 3.2, 0.1, 4.0, 1.6)
            vo.wait_until("empty list")
            self.play(FadeIn(kept), FadeIn(dropped), run_time=0.6)
        with self.say(2) as vo:
            vo.wait_until("folder name")
            self.play(FadeIn(at("the folder name does not matter", 0, -1.3, 26, INK)), run_time=0.4)
        self.finish()


class S03(EpisodeScene):
    def construct(self):
        self.header("Identical clouds, score zero")
        with self.say(0) as vo:
            leftc = card("predicted", "0,0  1,1  2,2", -3.2, 0.45, 4.0, 1.8)
            right = card("truth", "the same three rows", 3.2, 0.45, 4.2, 1.8)
            self.cue(vo, 0.1, FadeIn(leftc), FadeIn(right))
        with self.say(1) as vo:
            mid = at("MMD", 0, 0.45, 36, RED, bold=True)
            vo.wait_until("distance")
            self.play(FadeIn(mid), run_time=0.35)
            self.play(FadeIn(at("score == approx 0", 0, -0.9, 28, INK)), run_time=0.4)
        with self.say(2) as vo:
            vo.wait_until("assert")
            self.play(FadeIn(at("assert is the test. print is not.", 0, -1.7, 26, GRAY)), run_time=0.4)
        self.finish()


class S04(EpisodeScene):
    def construct(self):
        self.header("The other file just runs")
        with self.say(0) as vo:
            shown = code_card(["experiment = Experiment(path)", "experiment.setup()"], 0, 0.45, 7.4)
            self.cue(vo, 0.15, FadeIn(shown))
        with self.say(1) as vo:
            vo.wait_until("no function")
            self.play(FadeIn(at("no function whose name starts with test_", 0, -0.9, 26, RED)), run_time=0.45)
        with self.say(2) as vo:
            vo.wait_until("notebook")
            self.play(FadeIn(at("the replica notebook is a caller too", 0, -1.65, 26, INK)), run_time=0.4)
        self.finish()


class S05(EpisodeScene):
    def construct(self):
        self.header("A crash is not a failed test")
        with self.say(0) as vo:
            box = card("collection", "find test_* first", 0, 0.6, 5.0, 1.7, accent=True)
            self.cue(vo, 0.12, FadeIn(box))
        with self.say(1) as vo:
            boom = at("setup() runs while the file is loading", 0, -0.7, 26, RED)
            vo.wait_until("while the file loads")
            self.play(FadeIn(boom), run_time=0.45)
        with self.say(2) as vo:
            vo.wait_until("before any test")
            self.dim_for_ponder()
            self.play(FadeIn(ponder("文件在加载时就执行了 setup。测试开始了吗？",
                                    "Setup ran while the file loaded. Did a test start?")), run_time=0.45)
        self.finish()


class S06(EpisodeScene):
    def construct(self):
        self.header("What to run")
        with self.say(0) as vo:
            cmd = code_card(["pytest src/speciesot/Tests/test_evaluation.py"], 0, 0.45, 10.2)
            self.cue(vo, 0.12, FadeIn(cmd))
        with self.say(1) as vo:
            vo.wait_until("not a result")
            self.play(FadeIn(at("a command, not a result from this session", 0, -0.85, 26, GRAY)), run_time=0.4)
        with self.say(2) as vo:
            vo.wait_until("function name")
            self.play(FadeIn(at("look for def test_  before you trust the folder", 0, -1.6, 26, RED)), run_time=0.4)
        self.finish()
