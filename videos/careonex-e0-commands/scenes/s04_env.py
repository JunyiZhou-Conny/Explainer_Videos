"""S04 · Sticky notes: environment variables.

1. The line `$env:AWS_PROFILE = "careonex-team"` taken apart: `$env:` (environment) · name · `=` · value.
   A terminal grows a column of sticky notes, one per $env line of terminal 1.
2. A program started from the terminal reads the notes; the real code line from voice/config.py
   (`os.environ.get("CAREONEX_RETRIEVE_URL", "")`). Tag READ IN CODE.
3. Terminal 2 has its own notes; nothing crosses over: that is why the AWS lines are repeated.
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (CODE_C, NARRATION, QUERY_C, T1, T2, big_line, code_panel, container, mono, sans, serif,
                    source_tag, sticky, terminal)

SAY = NARRATION["S04"]


def env_pairs(lines):
    out = []
    for ln in lines:
        if ln.startswith("$env:"):
            name, value = ln[5:].split(" = ", 1)
            out.append((name, value.strip('"')))
    return out


class EnvVars(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- the shape of the line
        with self.voiceover(SAY[0]) as vo:
            parts = VGroup(mono("$env:", 40, QUERY_C), mono("AWS_PROFILE", 40), mono("=", 40, S.GREY),
                           mono('"careonex-team"', 40)).arrange(RIGHT, buff=0.3).move_to(UP * 1.6)
            labels = VGroup(serif("the environment", 26, QUERY_C), serif("a name", 26), serif("", 26),
                            serif("a value", 26))
            for p, l in zip(parts, labels):
                l.next_to(p, DOWN, buff=0.3)
            self.play(LaggedStart(*[FadeIn(p, shift=DOWN * 0.15) for p in parts], lag_ratio=0.3), run_time=1.4)
            self.play(LaggedStart(*[FadeIn(l) for l in labels], lag_ratio=0.3), run_time=1.2)
            vo.wait_until("Each one sets")
            title = serif("an environment variable", 34, QUERY_C).next_to(labels, DOWN, buff=0.5)
            self.play(Write(title), run_time=1.0)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- sticky notes, read by programs
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(parts, labels, title)), run_time=0.5)
            term = terminal(["PS C:\\…> _"], "terminal 1", size=24, width=4.2).move_to(LEFT * 4.2 + UP * 2.4)
            notes = VGroup(*[sticky(n, v, 18) for n, v in env_pairs(T1)]).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
            notes.next_to(term, DOWN, buff=0.25).align_to(term, LEFT)
            self.play(FadeIn(term), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(n, shift=LEFT * 0.2, scale=0.9) for n in notes], lag_ratio=0.25), run_time=1.4)
            vo.wait_until("Every program started")
            prog = container("a program", "started from this window", width=3.2, name_size=26, sub_size=22)
            prog.move_to(RIGHT * 1.0 + UP * 1.6)
            self.play(FadeIn(prog, shift=LEFT * 0.2), run_time=0.6)
            arrows = VGroup(*[Arrow(n.get_right(), prog.frame.get_left(), buff=0.1, stroke_width=2, color=QUERY_C,
                                    max_tip_length_to_length_ratio=0.06) for n in notes])
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.15), run_time=1.0)
            vo.wait_until("The CareOneX code")
            code = code_panel('RETRIEVE_URL = os.environ.get("CAREONEX_RETRIEVE_URL", "").rstrip("/")', size=22, width=6.6)
            code.next_to(prog, DOWN, buff=0.5).set_x(3.0)
            src = VGroup(mono("services/voice/nova_sonic/config.py", 20, S.GREY), source_tag("code")
                         ).arrange(DOWN, buff=0.12, aligned_edge=LEFT).next_to(code, DOWN, buff=0.15).align_to(code, LEFT)
            self.play(FadeIn(code, shift=UP * 0.15), FadeIn(src), run_time=0.9)
            vo.wait_until("so nothing about")
            note = serif("no laptop-specific settings inside the code", 26, S.GREY).next_to(src, DOWN, buff=0.35).align_to(code, LEFT)
            self.play(FadeIn(note), run_time=0.6)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 3 ---------------------------------------------------------------- one window only
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(prog, arrows, code, src, note)), run_time=0.5)
            term2 = terminal(["PS C:\\…> _"], "terminal 2", size=24, width=4.2).move_to(RIGHT * 3.0 + UP * 2.4)
            notes2 = VGroup(*[sticky(n, v, 18) for n, v in env_pairs(T2)]).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
            notes2.next_to(term2, DOWN, buff=0.25).align_to(term2, LEFT)
            self.play(FadeIn(term2), LaggedStart(*[FadeIn(n, shift=LEFT * 0.2) for n in notes2], lag_ratio=0.2), run_time=1.3)
            wall = DashedLine(UP * 3.4, DOWN * 3.4, color=S.GREY_DARK).set_x(-0.6)
            self.play(Create(wall), run_time=0.5)
            same = VGroup(*[n for n in notes if n.name.text in ("AWS_PROFILE", "AWS_DEFAULT_REGION")],
                          *[n for n in notes2 if n.name.text in ("AWS_PROFILE", "AWS_DEFAULT_REGION")])
            self.play(*[Indicate(n, color=S.WHITE, scale_factor=1.06) for n in same], run_time=1.2)
            rep = serif("set again in each window", 26, QUERY_C).to_edge(DOWN, buff=0.4)
            self.play(FadeIn(rep), run_time=0.5)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.play(FadeOut(*self.mobjects), run_time=0.8)
