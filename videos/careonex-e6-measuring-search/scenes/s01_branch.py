"""S01 · What is on Marco's branch.

1. One commit, 213 files, +46,458 lines (git diff main → feat/sonic_with_rag_updated@1591ed2), split
   by kind of file: evaluation data 26,302 · code 7,978 · docs 4,171 · tests 4,046 · lockfiles 3,466 ·
   other 495. Note: main never had the pipeline, so the commit carries it too.
2. retrieve in the middle, three dials around it (cut · search · order) and a fourth below (check
   answers).
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (AWS_C, CODE_C, DATA_C, MARCO_C, NARRATION, QUERY_C, container, mono, sans, serif,
                    source_tag)

SAY = NARRATION["S01"]

# git diff --numstat origin/main origin/feat/sonic_with_rag_updated, grouped by path
DIFF = [("evaluation data", 26302, DATA_C), ("code", 7978, CODE_C), ("docs", 4171, S.GREY),
        ("tests", 4046, S.TEAL), ("lockfiles", 3466, S.GREY_DARK), ("other", 495, S.GREY_DARK)]


def dial(label: str, sub: str, color: str, radius: float = 0.72) -> VGroup:
    face = Circle(radius=radius, stroke_color=color, stroke_width=3).set_fill(color, 0.08)
    ticks = VGroup(*[Line(ORIGIN, UP * 0.1, stroke_color=color, stroke_width=2)
                     .shift(UP * (radius - 0.12)).rotate(a, about_point=ORIGIN)
                     for a in np.linspace(-2.2, 2.2, 7)]).move_to(face)
    needle = Line(face.get_center(), face.get_center() + UP * (radius - 0.15), stroke_color=S.WHITE,
                  stroke_width=4).rotate(1.6, about_point=face.get_center())
    hub = Dot(face.get_center(), radius=0.05, color=S.WHITE)
    text = VGroup(serif(label, 28), mono(sub, 22, color)).arrange(DOWN, buff=0.06)
    g = VGroup(face, ticks, needle, hub, text)
    text.next_to(face, DOWN, buff=0.15)
    g.face, g.needle, g.text = face, needle, text
    return g


class Branch(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- one big commit
        with self.voiceover(SAY[0]) as vo:
            head = VGroup(sans("MARCO'S BRANCH", 22, MARCO_C), mono("feat/sonic_with_rag_updated", 30, MARCO_C)
                          ).arrange(DOWN, buff=0.08, aligned_edge=LEFT).to_corner(UL, buff=0.5)
            stats = VGroup(mono("1 commit", 30), mono("213 files", 30), mono("+46,458 lines", 30, QUERY_C)
                           ).arrange(RIGHT, buff=0.6).next_to(head, DOWN, buff=0.45).align_to(head, LEFT)
            self.play(FadeIn(head, shift=DOWN * 0.15), run_time=0.7)
            self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.15) for s in stats], lag_ratio=0.3), run_time=1.2)
            total = sum(n for _, n, _ in DIFF)
            W = 12.4
            segs = VGroup()
            for name, n, col in DIFF:
                segs.add(Rectangle(width=W * n / total, height=0.7, stroke_color=S.BG, stroke_width=2)
                         .set_fill(col, 0.85))
            segs.arrange(RIGHT, buff=0).move_to(DOWN * 0.35)
            labs = VGroup()
            for (name, n, col), seg in zip(DIFF[:5], segs):
                lab = VGroup(serif(name, 22, S.WHITE if col != S.GREY_DARK else S.GREY),
                             mono(f"{n:,}", 20, S.GREY)).arrange(DOWN, buff=0.04)
                labs.add(lab)
            for lab, seg in zip(labs, segs):
                lab.next_to(seg, DOWN, buff=0.15)
            # the three narrow right-hand segments: stagger their labels
            labs[3].shift(DOWN * 0.0)
            labs[4].next_to(segs[4], DOWN, buff=0.85)
            tag = VGroup(mono("git diff main", 20, S.GREY), source_tag("code")).arrange(RIGHT, buff=0.25)
            tag.next_to(segs, UP, buff=0.18).align_to(segs, RIGHT)
            vo.wait_until("Most of those lines")
            self.play(LaggedStart(*[GrowFromEdge(s, LEFT) for s in segs], lag_ratio=0.15), FadeIn(tag), run_time=1.4)
            self.play(FadeIn(labs), run_time=0.7)
            vo.wait_until("They are evidence")
            brace = Brace(segs[0], UP, color=DATA_C)
            ev = serif("test questions · saved search results · grades", 24, DATA_C).next_to(brace, UP, buff=0.1)
            self.play(FadeOut(tag), GrowFromCenter(brace), FadeIn(ev), run_time=0.9)
            note = serif("the commit also carries the whole library pipeline (E2) and the voice app: main never had them",
                         22, S.GREY).to_edge(DOWN, buff=0.45)
            if note.width > 13:
                note.scale_to_fit_width(13)
            self.play(FadeIn(note), run_time=0.6)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- three dials around retrieve
        with self.voiceover(SAY[1]) as vo:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
            ret = container("retrieve", "finds passages for a question", width=3.4, name_size=30, sub_size=20)
            ret.move_to(UP * 0.5)
            q = VGroup(sans("CALLER ASKS", 18, QUERY_C), serif('"Can someone help my mother shower?"', 24, QUERY_C)
                       ).arrange(DOWN, buff=0.06).next_to(ret, UP, buff=0.5)
            self.play(FadeIn(ret), run_time=0.6)
            self.play(FadeIn(q, shift=DOWN * 0.15), run_time=0.6)
            d1 = dial("how the text is cut", "chunking", DATA_C).move_to(LEFT * 4.9 + UP * 0.6)
            d2 = dial("how the search is run", "one search or feedback", QUERY_C).move_to(RIGHT * 4.9 + UP * 0.6)
            d3 = dial("how results are ordered", "reranking", CODE_C).move_to(DOWN * 1.9 + LEFT * 2.6)
            d4 = dial("how answers are checked", "text_eval", MARCO_C).move_to(DOWN * 1.9 + RIGHT * 2.6)
            wires = VGroup(*[DashedLine(d.face.get_center(), ret.get_center(), stroke_color=S.GREY_DARK,
                                        stroke_width=2, dash_length=0.08) for d in (d1, d2, d3)])
            for w, d in zip(wires, (d1, d2, d3)):
                w.put_start_and_end_on(d.face.get_center() + (ret.get_center() - d.face.get_center()) * 0.2,
                                       ret.get_center() + (d.face.get_center() - ret.get_center()) * 0.38)
            wires.set_z_index(-1)
            for anchor, d, w in [("How the documents are cut", d1, wires[0]), ("How the search is run", d2, wires[1]),
                                 ("And how results are ordered", d3, wires[2])]:
                vo.wait_until(anchor)
                self.play(FadeIn(d, scale=0.9), Create(w), run_time=0.7)
                self.play(Rotate(d.needle, -2.0, about_point=d.face.get_center()), run_time=0.6)
            vo.wait_until("He also added")
            self.play(FadeIn(d4, scale=0.9), run_time=0.7)
            self.play(Rotate(d4.needle, -2.0, about_point=d4.face.get_center()), run_time=0.6)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.play(FadeOut(*self.mobjects), run_time=0.8)
