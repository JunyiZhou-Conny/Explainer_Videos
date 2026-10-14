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
        self.header("The title overclaims")
        with self.say(0) as vo:
            title = card("notebook 02", "scGen training analysis", 0, 0.7, 6.4, 1.7, accent=True)
            self.cue(vo, 0.12, FadeIn(title))
        with self.say(1) as vo:
            reader = card("load_scalars", "reads cache/scalars", 0, -0.7, 5.6, 1.5)
            vo.wait_until("does not train")
            self.play(FadeIn(reader), run_time=0.5)
        with self.say(2) as vo:
            vo.wait_until("where is the door")
            self.dim_for_ponder()
            self.play(FadeIn(ponder("训练已经发生了。启动它的门在哪里？",
                                    "Training already happened. Where is the door?")), run_time=0.45)
        self.finish()


class S02(EpisodeScene):
    def construct(self):
        self.header("A file of numbers comes out")
        with self.say(0) as vo:
            shown = code_card(["path = result_dir + '/cache/scalars'", "read_hdf(path, 'train')"], 0, 0.45, 8.2)
            self.cue(vo, 0.12, FadeIn(shown))
        with self.say(1) as vo:
            vo.wait_until("Nothing in that door")
            self.play(FadeIn(at("train and eval tables. no call to train.", 0, -1.05, 26, RED)), run_time=0.45)
        with self.say(2) as vo:
            vo.wait_until("without being the run")
            self.play(FadeIn(at("a viewer is not the run", 0, -1.75, 26, INK)), run_time=0.4)
        self.finish()


class S03(EpisodeScene):
    def construct(self):
        self.header("The spec is the door")
        spec = card("m2_baseline.yaml", "experiment_tag", -3.6, 0.5, 4.4, 1.7)
        cfg = card("render", "name: scgen", 3.4, 0.5, 3.6, 1.7, accent=True)
        with self.say(0) as vo:
            self.cue(vo, 0.12, FadeIn(spec))
        with self.say(1) as vo:
            hop = Arrow(spec.get_right(), cfg.get_left(), buff=0.12, color=RED, stroke_width=3)
            vo.wait_until("name is scgen")
            self.play(Create(hop), FadeIn(cfg), run_time=0.65)
        with self.say(2) as vo:
            vo.wait_until("does not submit")
            self.play(FadeIn(at("generate writes the job. you submit it.", 0, -1.15, 26, INK)), run_time=0.4)
        self.finish()


class S04(EpisodeScene):
    def construct(self):
        self.header("Prep already absorbed a notebook")
        nb = card("notebook 01.5", "built the h5ad", -3.4, 0.45, 4.2, 1.7)
        prep = card("hub prep", "ports that notebook", 3.4, 0.45, 4.4, 1.7, accent=True)
        with self.say(0) as vo:
            self.cue(vo, 0.12, FadeIn(nb))
        with self.say(1) as vo:
            hop = Arrow(nb.get_right(), prep.get_left(), buff=0.12, color=RED, stroke_width=3)
            vo.wait_until("ports that notebook")
            self.play(Create(hop), FadeIn(prep), run_time=0.65)
        with self.say(2) as vo:
            vo.wait_until("already exists")
            self.play(FadeIn(at("do not rebuild this door on scGenModel", 0, -1.15, 26, RED)), run_time=0.4)
        self.finish()


class S05(EpisodeScene):
    def construct(self):
        self.header("What to search for")
        with self.say(0) as vo:
            box = folder("specs/", 0, 0.7, 3.6)
            self.cue(vo, 0.12, FadeIn(box))
        with self.say(1) as vo:
            vo.wait_until("the notebook is a viewer")
            self.play(FadeIn(at("same result directory → viewer", 0, -0.55, 28, RED)), run_time=0.45)
        with self.say(2) as vo:
            vo.wait_until("which string")
            self.dim_for_ponder()
            self.play(FadeIn(ponder("笔记本 02 里，你第一个拿去搜索的字符串是什么？",
                                    "Which string from notebook 02 would you search first?")), run_time=0.45)
        self.finish()


class S06(EpisodeScene):
    def construct(self):
        self.header("Viewer, door, and the class")
        doors = VGroup(
            card("viewer", "reads scalars", -4.2, 0.4, 3.5, 1.7),
            card("door", "spec + generate", 0, 0.4, 3.8, 1.7, accent=True),
            card("class", "src/speciesot", 4.2, 0.4, 3.6, 1.7),
        )
        with self.say(0) as vo:
            self.cue(vo, 0.1, FadeIn(doors[0]))
        with self.say(1) as vo:
            vo.wait_until("hub generate")
            self.play(FadeIn(doors[1]), run_time=0.45)
        with self.say(2) as vo:
            vo.wait_until("not a second hub")
            self.play(FadeIn(doors[2]), run_time=0.45)
        self.finish()
