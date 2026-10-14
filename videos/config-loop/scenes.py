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
        self.header("A number under the wrong key")
        singular = card("x_dimension", "the class reads this", -3.3, 0.55, 4.2, 1.8)
        plural = card("x_dimensions", "setup writes this", 3.3, 0.55, 4.2, 1.8, accent=True)
        with self.say(0) as vo:
            self.cue(vo, 0.1, FadeIn(singular), FadeIn(plural))
            num = at("18024", 3.3, -0.7, 36, RED, bold=True)
            vo.wait_until("eighteen thousand")
            self.play(FadeIn(num), run_time=0.4)
        with self.say(1) as vo:
            vo.wait_until("with an s")
            self.play(Create(line(1.3, 0.2, 5.2, 0.9, RED, 4)), run_time=0.4)
        with self.say(2) as vo:
            vo.wait_until("which value")
            self.dim_for_ponder()
            self.play(FadeIn(ponder("差一个字母时，模型拿到的是哪个值？",
                                    "One letter differs. Which value does the model get?")), run_time=0.45)
        self.finish()


class S02(EpisodeScene):
    def construct(self):
        self.header("Setup looks up a name")
        with self.say(0) as vo:
            shown = code_card(["if 'scGenModel' in models:", "    scGenModel(nested dict)"], 0, 0.35, 7.2)
            self.cue(vo, 0.15, FadeIn(shown))
        with self.say(1) as vo:
            old = code_card(["if 'IdentityModel' in models:"], 0, -1.15, 7.2)
            tag = at("committed file, no scGen branch", 0, -2.0, 22, GRAY)
            vo.wait_until("Identity model")
            self.play(FadeIn(old), FadeIn(tag), run_time=0.55)
        with self.say(2) as vo:
            steps = at("class, then yaml key, then notebook", 0, 1.75, 26, INK)
            vo.wait_until("three places")
            self.play(FadeIn(steps), run_time=0.4)
        self.finish()


class S03(EpisodeScene):
    def construct(self):
        self.header("Three spellings, one number")
        a = card("1  config.yaml", "x_dimension", -4.2, 0.5, 3.6, 1.7)
        b = card("2  setup", "x_dimensions", 0, 0.5, 3.4, 1.7, accent=True)
        c = card("3  VAEArith", "self.x_dimensions", 4.2, 0.5, 3.8, 1.7)
        with self.say(0) as vo:
            self.cue(vo, 0.12, FadeIn(a))
            vo.wait_until("singular")
            self.play(FadeIn(at("1000", -4.2, -0.65, 28, INK)), run_time=0.3)
        with self.say(1) as vo:
            hop = Arrow(a.get_right(), b.get_left(), buff=0.1, color=RED, stroke_width=3)
            vo.wait_until("different key")
            self.play(Create(hop), FadeIn(b), FadeIn(at("18024", 0, -0.65, 28, RED, bold=True)), run_time=0.7)
        with self.say(2) as vo:
            miss = Arrow(b.get_right(), c.get_left(), buff=0.1, color=GRAY, stroke_width=3)
            vo.wait_until("never set")
            self.play(Create(miss), FadeIn(c), FadeIn(at("missing", 4.2, -0.7, 26, RED)), run_time=0.6)
        self.finish()


class S04(EpisodeScene):
    def construct(self):
        self.header("Train is called with nothing")
        with self.say(0) as vo:
            leftc = code_card(["def train(self):", "    model.train()"], -3.3, 0.3, 5.2)
            self.cue(vo, 0.12, FadeIn(leftc))
        with self.say(1) as vo:
            right = code_card(["def train(self, training_data):"], 3.2, 0.3, 6.0)
            vo.wait_until("training data")
            self.play(FadeIn(right), run_time=0.5)
            self.play(FadeIn(at("Identity survives. scGen does not.", 0, -1.2, 26, RED)), run_time=0.4)
        with self.say(2) as vo:
            vo.wait_until("uncomment")
            self.play(FadeIn(at("uncomment experiment.train()", 0, -1.9, 26, INK)), run_time=0.4)
        self.finish()


class S05(EpisodeScene):
    def construct(self):
        self.header("What the notebook already printed")
        with self.say(0) as vo:
            shown = code_card(["x_dimensions: 18024"], 0, 0.4, 5.6)
            self.cue(vo, 0.15, FadeIn(shown))
        with self.say(1) as vo:
            note = at("saved output. not re-run. not a commit.", 0, -0.8, 26, GRAY)
            vo.wait_until("not a commit")
            self.play(FadeIn(note), run_time=0.45)
        with self.say(2) as vo:
            vo.wait_until("which spelling")
            self.dim_for_ponder()
            self.play(FadeIn(ponder("setup 之后，打印出来的是哪一种拼写？",
                                    "After setup, which spelling does the print show?")), run_time=0.45)
        self.finish()


class S06(EpisodeScene):
    def construct(self):
        self.header("Edit, then look")
        steps = VGroup(
            card("1  edit class", "the attribute", -4.2, 0.4, 3.5, 1.7),
            card("2  same string", "the yaml key", 0, 0.4, 3.5, 1.7, accent=True),
            card("3  print", "models[1].config", 4.2, 0.4, 3.6, 1.7),
        )
        with self.say(0) as vo:
            self.cue(vo, 0.1, FadeIn(steps[0]))
            vo.wait_until("same string")
            self.play(FadeIn(steps[1]), FadeIn(steps[2]), run_time=0.6)
        with self.say(1) as vo:
            vo.wait_until("did not receive")
            self.play(FadeIn(at("printed key must be the key that is read", 0, -1.15, 26, RED)), run_time=0.4)
        with self.say(2) as vo:
            vo.wait_until("singular spelling")
            self.play(FadeIn(at("find both spellings before you train", 0, -1.8, 26, INK)), run_time=0.4)
        self.finish()
