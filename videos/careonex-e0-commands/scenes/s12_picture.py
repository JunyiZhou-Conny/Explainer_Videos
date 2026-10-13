"""S12 · The whole picture.

1. Laptop (retrieve in its container on port 8080, voice with mic and speaker) and the AWS account
   (Nova 2 Sonic, Knowledge Base → S3 Vectors + S3 bucket; Titan inside); the 8-hour SSO key feeds
   both programs. A question animates through: mic → voice → Nova → tool request → voice → retrieve →
   Knowledge Base → passages back → Nova → speaker.
2. A cheat-sheet card with every new term.
3. The series: E1 … E5, Marco's experiments; "Next: E1 · The big picture".
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (AWS_C, CODE_C, DATA_C, NARRATION, PEOPLE, PERSON_C, QUERY_C, aws, cloud, container, laptop,
                    link, mono, sans, serif, store, token)

SAY = NARRATION["S12"]

TERMS = [("terminal", "a window where you type commands"),
         ("environment variable", "a sticky note that programs started from that window can read"),
         ("AWS account", "the team's own fenced-off corner of Amazon's cloud"),
         ("SSO / profile", "sign in once in a browser; the profile names which account and role"),
         ("permission set AC215", "what every teammate is allowed to do"),
         ("region us-east-1", "the AWS data centers in Northern Virginia"),
         ("Docker image / container", "a frozen box with a program / that box, running"),
         ("port, 127.0.0.1", "a numbered door / this same computer"),
         ("Bedrock", "Amazon's AI models as a service: Nova 2 Sonic, Titan"),
         ("Knowledge Base", "Amazon's managed library + search for the team's documents"),
         ("uv", "sets up the right Python and libraries, then runs a command")]


class WholePicture(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- everything at once
        with self.voiceover(SAY[0]) as vo:
            lap = laptop(6.4, 4.8, "Marco's laptop").move_to(LEFT * 3.3 + UP * 0.1)
            ret = container("retrieve", "Docker · :8080", width=2.6, name_size=26, sub_size=20)
            voi = container("voice", "uv run · mic + speaker", width=2.6, name_size=26, sub_size=20)
            ret.move_to(lap.screen.get_center() + RIGHT * 1.4 + UP * 1.1)
            voi.move_to(lap.screen.get_center() + LEFT * 1.4 + DOWN * 0.9)
            acct = RoundedRectangle(width=5.0, height=6.4, corner_radius=0.3, stroke_color=AWS_C, stroke_width=3)
            acct = DashedVMobject(acct, num_dashes=70).move_to(RIGHT * 3.9 + DOWN * 0.15)
            at = sans("AWS · TEAM ACCOUNT · us-east-1", 20, AWS_C).next_to(acct, UP, buff=0.08)
            kb = aws("bedrock", "Knowledge Base", "searches the passages", width=4.0, name_size=24, sub_size=20)
            vec = aws("s3 vectors", "program-kb", "232 vectors (Titan)", width=4.0, name_size=24, sub_size=20)
            nova = aws("bedrock model", "Nova 2 Sonic", "hears and speaks", width=4.0, name_size=24, sub_size=20)
            kb.move_to([acct.get_x(), ret.get_y() - 0.2, 0])
            vec.next_to(kb, UP, buff=0.35)
            nova.move_to([acct.get_x(), voi.get_y() - 0.3, 0])
            at.next_to(acct, DOWN, buff=0.08)
            self.play(FadeIn(lap), FadeIn(ret), FadeIn(voi), run_time=0.9)
            self.play(Create(acct), FadeIn(at), FadeIn(kb), FadeIn(vec), FadeIn(nova), run_time=1.0)
            key = VGroup(Circle(radius=0.14, color=QUERY_C, stroke_width=3), Line(RIGHT * 0.14, RIGHT * 0.55, color=QUERY_C, stroke_width=3))
            keyl = VGroup(key, mono("8-hour login", 20, QUERY_C)).arrange(RIGHT, buff=0.15)
            keyl.move_to(lap.screen.get_corner(DL) + RIGHT * 1.4 + UP * 0.45)
            vo.wait_until("Both programs use")
            self.play(FadeIn(keyl), Indicate(ret.frame, color=QUERY_C), Indicate(voi.frame, color=QUERY_C), run_time=1.0)
            vo.wait_until("You speak")
            l_vn = link(voi, nova, AWS_C)
            l_vr = link(voi, ret, QUERY_C)
            l_rk = link(ret, kb, QUERY_C)
            l_kv = link(kb.frame.get_top(), vec.frame.get_bottom(), AWS_C)
            self.play(*[GrowArrow(l.arrow) for l in (l_vn, l_vr, l_rk, l_kv)], run_time=0.8)
            t = token(QUERY_C, 0.13)
            hops = [voi.get_center() + DOWN * 1.2, voi.get_center(), nova.get_center(), voi.get_center(), ret.get_center(),
                    kb.get_center(), vec.get_center(), kb.get_center(), ret.get_center(), voi.get_center(), nova.get_center(),
                    voi.get_center() + DOWN * 1.2]
            t.move_to(hops[0])
            self.play(FadeIn(t), run_time=0.2)
            for h in hops[1:]:
                self.play(t.animate.move_to(h), run_time=0.45)
            self.play(FadeOut(t), run_time=0.2)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- the cheat sheet
        with self.voiceover(SAY[1]) as vo:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
            rows = VGroup(*[VGroup(mono(a, 22, QUERY_C), serif(b, 22)).arrange(RIGHT, buff=0.3) for a, b in TERMS])
            for r in rows:
                r[1].move_to(r[0].get_right() + RIGHT * 0.3, aligned_edge=LEFT)
            lw = max(r[0].width for r in rows)
            for r in rows:
                r[0].move_to([0, 0, 0], aligned_edge=LEFT)
                r[1].move_to([lw + 0.4, 0, 0], aligned_edge=LEFT)
            rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
            card = VGroup(serif("New words from this video", 30), rows).arrange(DOWN, buff=0.3)
            if card.width > 12.8:
                card.scale_to_fit_width(12.8)
            if card.height > 6.9:
                card.scale_to_fit_height(6.9)
            frame = SurroundingRectangle(card, buff=0.25, corner_radius=0.15, color=QUERY_C)
            self.play(FadeIn(frame), FadeIn(card[0]), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows], lag_ratio=0.12), run_time=2.4)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 3 ---------------------------------------------------------------- the series
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(frame, card)), run_time=0.5)
            eps = [("E0", "these commands", S.GREY), ("E1", "the big picture", QUERY_C), ("E2", "building the library", DATA_C),
                   ("E3", "finding the right passage", DATA_C), ("E4", "the voice loop", CODE_C),
                   ("E5", "checking the answers", CODE_C), ("E6+", "Marco's experiments", PEOPLE["Marco"])]
            rows = VGroup(*[VGroup(mono(e, 28, c), serif(t, 28)).arrange(RIGHT, buff=0.35) for e, t, c in eps])
            rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(ORIGIN)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows], lag_ratio=0.15), run_time=1.6)
            self.play(Circumscribe(rows[1], color=QUERY_C), rows[0].animate.set_opacity(0.4), run_time=1.2)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.play(FadeOut(*self.mobjects), run_time=1.0)
