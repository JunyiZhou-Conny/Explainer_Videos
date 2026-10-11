"""S03 · Line 1: cd.

1. Line 1, large; a folder tree opens: Desktop → CareOneX_Requester_Live_Voice_App → services/ (six
   folders) + docker-compose.yml; the terminal's "you are here" marker moves into the folder.
2. Tag INFERRED: Marco's own copy of careonex-agents, with his newest changes; reason: the later
   commands need exactly the repository's folders.
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (CODE_C, DATA_C, NARRATION, QUERY_C, T1, big_line, mono, sans, serif, source_tag)

SAY = NARRATION["S03"]


def folder(name, color=DATA_C, size=24):
    icon = VGroup(Polygon([0, 0, 0], [0.18, 0, 0], [0.24, 0.07, 0], [0.5, 0.07, 0], [0.5, -0.32, 0], [0, -0.32, 0],
                          stroke_color=color, stroke_width=2).set_fill(color, 0.2))
    t = mono(name, size, S.WHITE).next_to(icon, RIGHT, buff=0.15)
    return VGroup(icon, t)


def file_row(name, size=24):
    icon = Rectangle(width=0.32, height=0.4, stroke_color=S.GREY, stroke_width=2)
    t = mono(name, size, S.WHITE).next_to(icon, RIGHT, buff=0.15)
    return VGroup(icon, t)


class ChangeDir(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- cd
        with self.voiceover(SAY[0]) as vo:
            line = big_line(T1[0], size=26).to_edge(UP, buff=0.5)
            self.play(FadeIn(line, shift=DOWN * 0.2), run_time=0.8)
            cd = SurroundingRectangle(line.rows[0][:2], color=QUERY_C, buff=0.06)
            lab = serif("cd = change directory (go into a folder)", 28, QUERY_C).next_to(line, DOWN, buff=0.3)
            self.play(Create(cd), FadeIn(lab), run_time=0.8)
            tree = VGroup(folder("C:\\Users\\Marco\\Desktop"),
                          folder("CareOneX_Requester_Live_Voice_App", QUERY_C),
                          folder("services/"),
                          *[folder(n, CODE_C, 22) for n in ("data/", "extract/", "chunk/", "kb-sync/", "retrieve/", "voice/")],
                          file_row("docker-compose.yml"))
            indents = [0, 0.5, 1.0, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.0]
            tree.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            for row, ind in zip(tree, indents):
                row.shift(RIGHT * ind)
            tree.next_to(lab, DOWN, buff=0.35).set_x(-1.5)
            vo.wait_until("It moves the terminal")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in tree], lag_ratio=0.12), run_time=1.8)
            here = VGroup(sans("YOU ARE HERE", 20, QUERY_C), Arrow(RIGHT, LEFT, color=QUERY_C, stroke_width=3)
                          ).arrange(LEFT, buff=0.1).next_to(tree[1], RIGHT, buff=0.3)
            self.play(FadeIn(here, shift=LEFT * 0.2), run_time=0.6)
            vo.wait_until("Every later command")
            self.play(Indicate(VGroup(tree[2:]), color=QUERY_C, scale_factor=1.03), run_time=1.2)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- whose folder?
        with self.voiceover(SAY[1]) as vo:
            why = VGroup(source_tag("inferred"),
                         VGroup(serif("Marco's own copy of the team", 24, S.PURPLE),
                                serif("repository, careonex-agents,", 24, S.PURPLE),
                                serif("with his newest changes.", 24, S.PURPLE),
                                serif("Reason: the next commands need", 24, S.GREY),
                                serif("exactly its folders.", 24, S.GREY)
                                ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
            why.move_to(RIGHT * 3.6 + DOWN * 0.9)
            self.play(FadeIn(why, shift=UP * 0.2), run_time=0.9)
            self.play(Indicate(tree[1], color=S.PURPLE), run_time=1.0)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.play(FadeOut(*self.mobjects), run_time=0.8)
