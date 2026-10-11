"""S02 · Two terminals, two programs.

1. A laptop; inside, terminal 1 → retrieve (search server), terminal 2 → voice (talks to you). AWS
   cloud outside. Tag READ IN CODE.
2. Microphone and speaker on voice; voice → retrieve "127.0.0.1:8080"; voice → Nova 2 Sonic,
   retrieve → Knowledge Base, inside the cloud.
3. "A terminal = a window where you type commands"; PowerShell (Windows); tag INFERRED with the reason.
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (AWS_C, CODE_C, NARRATION, PERSON_C, QUERY_C, T1, aws, cloud, container, laptop, link,
                    mono, sans, serif, source_tag, terminal)

SAY = NARRATION["S02"]


def mic_icon(color=PERSON_C, h=0.55):
    head = RoundedRectangle(width=h * 0.42, height=h * 0.62, corner_radius=h * 0.2, stroke_color=color, stroke_width=3)
    cup = Arc(radius=h * 0.32, start_angle=PI, angle=PI, color=color, stroke_width=3).next_to(head, DOWN, buff=-h * 0.32)
    stem = Line(cup.get_bottom(), cup.get_bottom() + DOWN * h * 0.18, color=color, stroke_width=3)
    return VGroup(head, cup, stem)


def speaker_icon(color=PERSON_C, h=0.5):
    box = Rectangle(width=h * 0.3, height=h * 0.4, stroke_color=color, stroke_width=3)
    cone = Polygon(box.get_corner(UR), box.get_corner(UR) + RIGHT * h * 0.35 + UP * h * 0.25,
                   box.get_corner(DR) + RIGHT * h * 0.35 + DOWN * h * 0.25, box.get_corner(DR),
                   stroke_color=color, stroke_width=3)
    waves = VGroup(*[Arc(radius=h * r, start_angle=-PI / 4, angle=PI / 2, color=color, stroke_width=2.5)
                     .move_to(cone.get_right() + RIGHT * h * r * 0.6) for r in (0.25, 0.42)])
    return VGroup(box, cone, waves)


class TwoPrograms(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- two programs
        with self.voiceover(SAY[0]) as vo:
            lap = laptop(7.6, 4.6).shift(LEFT * 2.6 + UP * 0.2)
            cl = cloud("AWS · the team's account", width=4.0).move_to(RIGHT * 4.6 + UP * 0.35)
            cl.shape.stretch_to_fit_height(4.2)
            cl.label.move_to(cl.shape).shift(DOWN * 1.3)
            self.play(Create(lap.screen), FadeIn(lap[1]), FadeIn(lap.label), run_time=0.9)
            self.play(FadeIn(cl), run_time=0.6)
            ret = container("retrieve", "a search server", width=2.6, name_size=28, sub_size=22)
            voi = container("voice", "the one you talk to", width=2.6, name_size=28, sub_size=22)
            tt1 = sans("TERMINAL 1", 20, S.GREY)
            tt2 = sans("TERMINAL 2", 20, S.GREY)
            g1 = VGroup(tt1, ret).arrange(DOWN, buff=0.12)
            g2 = VGroup(tt2, voi).arrange(DOWN, buff=0.12)
            sc = lap.screen
            g1.move_to(sc.get_center() + RIGHT * 1.85 + UP * 1.0)
            g2.move_to(sc.get_center() + LEFT * 1.95 + DOWN * 0.35)
            vo.wait_until("Terminal 1 starts")
            self.play(FadeIn(g1, shift=DOWN * 0.2), run_time=0.8)
            vo.wait_until("Terminal 2 starts")
            self.play(FadeIn(g2, shift=DOWN * 0.2), run_time=0.8)
            tag = source_tag("code").next_to(lap, DOWN, buff=0.2).align_to(lap, LEFT)
            self.play(FadeIn(tag), run_time=0.4)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- who talks to whom
        with self.voiceover(SAY[1]) as vo:
            mic = mic_icon().next_to(voi, DOWN, buff=0.3).shift(LEFT * 0.5)
            spk = speaker_icon().next_to(voi, DOWN, buff=0.35).shift(RIGHT * 0.5)
            self.play(FadeIn(mic, shift=UP * 0.15), FadeIn(spk, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("When it needs a fact")
            l1 = link(voi.frame.get_corner(UR), ret.frame.get_corner(DL), QUERY_C)
            lab = mono("127.0.0.1:8080", 22, QUERY_C).next_to(l1.arrow.get_center(), RIGHT, buff=0.15)
            self.play(GrowArrow(l1.arrow), FadeIn(lab), run_time=0.9)
            vo.wait_until("Both programs also")
            kb = aws("bedrock", "Knowledge Base", None, width=2.6, name_size=24)
            nova = aws("bedrock model", "Nova 2 Sonic", None, width=2.6, name_size=24)
            kb.move_to([cl.shape.get_x(), ret.get_y() - 0.05, 0])
            nova.move_to([cl.shape.get_x(), voi.get_y() + 0.1, 0])
            cl.label.next_to(nova, DOWN, buff=0.15)
            self.play(FadeIn(nova), FadeIn(kb), run_time=0.7)
            a1 = link(voi, nova, AWS_C)
            a2 = link(ret, kb, AWS_C)
            self.play(GrowArrow(a1.arrow), GrowArrow(a2.arrow), run_time=0.9)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 3 ---------------------------------------------------------------- what is a terminal
        with self.voiceover(SAY[2]) as vo:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
            term = terminal(["PS C:\\Users\\Marco> _"], "PowerShell", size=28).move_to(UP * 1.2)
            what = serif("a terminal = a window where you type commands", 30).next_to(term, DOWN, buff=0.45)
            self.play(FadeIn(term, shift=UP * 0.2), run_time=0.8)
            self.play(FadeIn(what), run_time=0.6)
            vo.wait_until("Marco is on Windows")
            clue = VGroup(mono('$env:AWS_PROFILE = "…"', 26, QUERY_C), mono('C:\\Users\\Marco\\…', 26, QUERY_C)
                          ).arrange(RIGHT, buff=0.8).next_to(what, DOWN, buff=0.55)
            why = VGroup(source_tag("inferred"),
                         serif("$env: and C:\\ paths are how Windows PowerShell writes things", 24, S.PURPLE)
                         ).arrange(RIGHT, buff=0.25).next_to(clue, DOWN, buff=0.35)
            self.play(FadeIn(clue, shift=UP * 0.15), run_time=0.8)
            self.play(FadeIn(why), run_time=0.7)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.play(FadeOut(*self.mobjects), run_time=0.8)
