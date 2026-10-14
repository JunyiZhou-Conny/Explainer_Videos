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
        self.header("The search comes back empty")
        with self.say(0) as vo:
            box = card("notebooks", "import scgen  →  0", 0, 0.45, 6.2, 1.8, accent=True)
            self.cue(vo, 0.12, FadeIn(box))
        with self.say(1) as vo:
            other = card("scGenModel", "does import scgen", 0, -0.95, 5.4, 1.5)
            vo.wait_until("not the program")
            self.play(FadeIn(other), run_time=0.45)
        with self.say(2) as vo:
            vo.wait_until("which one wrote")
            self.dim_for_ponder()
            self.play(FadeIn(ponder("两个都叫 scGen。检查点是哪一个写的？",
                                    "Both are named scGen. Which one wrote the checkpoint?")), run_time=0.45)
        self.finish()


class S02(EpisodeScene):
    def construct(self):
        self.header("Pipe A stops at pass")
        with self.say(0) as vo:
            a = card("setup", "import scgen", -4.0, 0.5, 3.4, 1.6)
            b = card("VAEArith", "upload, not a commit", 0, 0.5, 4.2, 1.6, accent=True)
            self.cue(vo, 0.1, FadeIn(a))
            vo.wait_until("VAE Arith")
            self.play(Create(Arrow(a.get_right(), b.get_left(), buff=0.1, color=RED, stroke_width=3)), FadeIn(b), run_time=0.6)
        with self.say(1) as vo:
            c = card("train", "pass", 4.2, 0.5, 2.8, 1.6)
            vo.wait_until("word pass")
            self.play(FadeIn(c), run_time=0.45)
        with self.say(2) as vo:
            vo.wait_until("source cells")
            self.play(FadeIn(at("predict returns the source cells", 0, -1.2, 26, RED)), run_time=0.4)
        self.finish()


class S03(EpisodeScene):
    def construct(self):
        self.header("The same constructor, really training")
        with self.say(0) as vo:
            shown = code_card(["network = scgen.VAEArith(...)", "network.train(train, ...)"], 0, 0.4, 7.6)
            self.cue(vo, 0.15, FadeIn(shown))
        with self.say(1) as vo:
            vo.wait_until("third stack")
            self.play(FadeIn(at("atlas-paper-vae  is a separate stack", 0, -1.0, 26, INK)), run_time=0.4)
        with self.say(2) as vo:
            vo.wait_until("does not mean")
            self.play(FadeIn(at("import scgen  ≠  the hub checkpoint", 0, -1.7, 26, RED)), run_time=0.4)
        self.finish()


class S04(EpisodeScene):
    def construct(self):
        self.header("Pipe B never imports scgen")
        spec = card("spec", "name: scgen", -4.2, 0.45, 3.3, 1.6)
        train = card("train.py", "train_auto_encoder", 0, 0.45, 4.0, 1.6, accent=True)
        shift = card("transport", "decode(encode + shift)", 4.2, 0.45, 4.0, 1.6)
        with self.say(0) as vo:
            self.cue(vo, 0.1, FadeIn(spec))
        with self.say(1) as vo:
            hop = Arrow(spec.get_right(), train.get_left(), buff=0.1, color=RED, stroke_width=3)
            vo.wait_until("train auto encoder")
            self.play(Create(hop), FadeIn(train), run_time=0.65)
        with self.say(2) as vo:
            hop2 = Arrow(train.get_right(), shift.get_left(), buff=0.1, color=RED, stroke_width=3)
            vo.wait_until("one shift")
            self.play(Create(hop2), FadeIn(shift), run_time=0.65)
        self.finish()


class S05(EpisodeScene):
    def construct(self):
        self.header("The pipes do not join")
        with self.say(0) as vo:
            leftp = card("pipe A", "VAEArith", -3.2, 0.55, 3.6, 1.6)
            right = card("pipe B", "AutoEncoder", 3.2, 0.55, 3.8, 1.6, accent=True)
            gap = at("no shared function", 0, 0.55, 22, RED)
            self.cue(vo, 0.12, FadeIn(leftp), FadeIn(right), FadeIn(gap))
        with self.say(1) as vo:
            vo.wait_until("compute scgen shift")
            self.play(FadeIn(at("compute_scgen_shift  lives in CellOT", 0, -0.9, 26, INK)), run_time=0.45)
        with self.say(2) as vo:
            vo.wait_until("which file")
            self.dim_for_ponder()
            self.play(FadeIn(ponder("检查点用的平移，在哪个文件里？",
                                    "Which file holds the shift the checkpoint uses?")), run_time=0.45)
        self.finish()


class S06(EpisodeScene):
    def construct(self):
        self.header("Three doors")
        doors = VGroup(
            card("import scgen", "TensorFlow package", -4.2, 0.4, 3.8, 1.8),
            card("name: scgen", "CellOT autoencoder", 0, 0.4, 3.8, 1.8, accent=True),
            card("Experiment", "src/speciesot", 4.2, 0.4, 3.6, 1.8),
        )
        with self.say(0) as vo:
            self.cue(vo, 0.1, FadeIn(doors[0]))
        with self.say(1) as vo:
            vo.wait_until("CellOT tree")
            self.play(FadeIn(doors[1]), run_time=0.45)
        with self.say(2) as vo:
            vo.wait_until("still writing")
            self.play(FadeIn(doors[2]), run_time=0.45)
        self.finish()
