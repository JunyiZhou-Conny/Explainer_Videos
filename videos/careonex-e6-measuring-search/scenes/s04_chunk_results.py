"""S04 · What the chunking test shows (MEASURED: Marco's scorer rerun on his grades).

1. Grouped bars: precision@5 A .52 B .47 C .50 · MRR A .69 B .67 C .73 · NDCG A .60 B .53 C .58;
   ~0.41 s per search for all three.
2. Best NDCG per question: A 9 · C 7 · tie 6 · B alone 0 · nothing helpful in any library 3.
3. Notes: B is the default on this branch, A built the main library; 25 questions, provisional grades.
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (BAD_C, CHUNKERS, METRICS, NARRATION, QUERY_C, mono, sans, serif, source_tag)

SAY = NARRATION["S04"]
AVG = METRICS["chunking"]["averages"]
BEST = METRICS["chunking"]["best_ndcg_per_question"]
SCALE = 4.6   # 1.0 → 4.6 units of bar height


class ChunkResults(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- the averages
        with self.voiceover(SAY[0]) as vo:
            hdr = VGroup(sans("A/B/C TEST · AVERAGES OVER 25 QUESTIONS", 22, QUERY_C),
                         source_tag("measured", "his scoring script, rerun on his grades")).arrange(RIGHT, buff=0.35)
            hdr.to_edge(UP, buff=0.35)
            base_y = -2.2
            groups = VGroup()
            bars = {}
            for gi, (metric, label) in enumerate([("precision_at_k", "precision@5"), ("mrr_at_k", "MRR"),
                                                  ("ndcg_at_k", "NDCG")]):
                g = VGroup()
                for ci, (key, letter, name, col) in enumerate(CHUNKERS):
                    v = AVG[key][metric]
                    b = Rectangle(width=0.8, height=v * SCALE, stroke_width=0).set_fill(col, 0.9)
                    b.move_to([ci * 0.95, base_y + v * SCALE / 2, 0])
                    val = mono(f"{v:.2f}", 22).next_to(b, UP, buff=0.08)
                    let = mono(letter, 22, col).next_to(b, DOWN, buff=0.1)
                    bars[(metric, key)] = VGroup(b, val, let)
                    g.add(bars[(metric, key)])
                lab = mono(label, 26, S.WHITE).next_to(g, DOWN, buff=0.15).set_y(base_y - 0.75)
                groups.add(VGroup(g, lab))
            groups.arrange(RIGHT, buff=1.1, aligned_edge=DOWN).shift(LEFT * 1.6)
            axis = Line(groups.get_corner(DL) + UP * 0.72 + LEFT * 0.3, groups.get_corner(DR) + UP * 0.72 + RIGHT * 0.3,
                        stroke_color=S.GREY_DARK, stroke_width=2)
            legend = VGroup(*[VGroup(mono(letter, 26, col), serif(name, 24, col)).arrange(RIGHT, buff=0.15)
                              for key, letter, name, col in CHUNKERS]).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
            legend.next_to(groups, RIGHT, buff=0.8).shift(UP * 0.8)
            self.play(FadeIn(hdr), Create(axis), FadeIn(legend), run_time=0.8)
            for g in groups:
                self.play(LaggedStart(*[GrowFromEdge(bb[0], DOWN) for bb in g[0]], lag_ratio=0.2),
                          FadeIn(VGroup(*[VGroup(bb[1], bb[2]) for bb in g[0]])), FadeIn(g[1]), run_time=0.9)
            vo.wait_until("The original chunker A")
            win = VGroup(*[SurroundingRectangle(bars[(m, "legacy")], color=QUERY_C, buff=0.06)
                           for m in ("precision_at_k", "ndcg_at_k")])
            self.play(Create(win), run_time=0.8)
            vo.wait_until("The hierarchical chunker C")
            winC = SurroundingRectangle(bars[("mrr_at_k", "hierarchical")], color=QUERY_C, buff=0.06)
            self.play(Create(winC), run_time=0.7)
            vo.wait_until("B is lowest")
            lows = VGroup(*[bars[(m, "section")][0] for m in ("precision_at_k", "mrr_at_k", "ndcg_at_k")])
            self.play(Indicate(lows, color=BAD_C, scale_factor=1.04), run_time=1.0)
            vo.wait_until("All three take")
            lat = VGroup(serif("time per search", 24, S.GREY),
                         *[mono(f"{letter} {AVG[key]['latency_ms'] / 1000:.2f} s", 24, col) for key, letter, _, col in CHUNKERS]
                         ).arrange(DOWN, buff=0.12, aligned_edge=LEFT).next_to(legend, DOWN, buff=0.6).align_to(legend, LEFT)
            self.play(FadeIn(lat, shift=UP * 0.1), run_time=0.7)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- question by question
        with self.voiceover(SAY[1]) as vo:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
            hdr = VGroup(sans("WHICH CHUNKER HAD THE BEST NDCG, PER QUESTION", 22, QUERY_C), source_tag("measured")
                         ).arrange(RIGHT, buff=0.35).to_edge(UP, buff=0.35)
            self.play(FadeIn(hdr), run_time=0.5)
            rows_spec = [("A best", BEST.get("legacy", 0), CHUNKERS[0][3], None),
                         ("C best", BEST.get("hierarchical", 0), CHUNKERS[2][3], None),
                         ("tie", BEST.get("tie", 0), S.WHITE, "B shares the top in 3 of them"),
                         ("B best", BEST.get("section", 0), CHUNKERS[1][3], None),
                         ("nothing helpful", BEST.get("no relevant passage", 0), BAD_C, "in any of the three")]
            rows = VGroup()
            for label, n, col, note in rows_spec:
                lab = serif(label, 28, col)
                dots = VGroup(*[Circle(0.17, stroke_color=col, stroke_width=3).set_fill(col, 0.5 if col != S.WHITE else 0.0)
                                for _ in range(n)]).arrange(RIGHT, buff=0.12)
                cnt = mono(str(n), 30, col)
                r = VGroup(lab, cnt, dots)
                if note:
                    r.add(serif(f"({note})", 22, S.GREY))
                rows.add(r)
            for r in rows:
                r[0].move_to(ORIGIN, aligned_edge=RIGHT)
                r[1].next_to(r[0], RIGHT, buff=0.35)
                if len(r[2]):
                    r[2].next_to(r[1], RIGHT, buff=0.35)
                if len(r) > 3:
                    r[3].next_to(r[2] if len(r[2]) else r[1], RIGHT, buff=0.3)
            rows.arrange(DOWN, buff=0.38, aligned_edge=LEFT)
            for r in rows:
                r.shift(RIGHT * (rows[0][0].get_right()[0] - r[0].get_right()[0]))
            rows.move_to(UP * 0.4).shift(LEFT * 0.5)
            for anchor, idx in [("A was best 9 times", [0, 1]), ("6 were ties", [2, 3]), ("For 3 questions", [4])]:
                vo.wait_until(anchor)
                self.play(LaggedStart(*[FadeIn(rows[i], shift=RIGHT * 0.15) for i in idx], lag_ratio=0.4), run_time=1.0)
            qs = VGroup(serif('"Can Medicaid send a home health aide to help my grandmother with meals and getting dressed?"', 20, S.GREY),
                        serif('"Can Medicaid pay a family caregiver to help my elderly parent at home?"', 20, S.GREY),
                        serif('"Where do I start if I need Medicaid-funded home care for my mother?"', 20, S.GREY)
                        ).arrange(DOWN, buff=0.08, aligned_edge=LEFT).next_to(rows, DOWN, buff=0.35).align_to(rows, LEFT)
            if qs.width > 12.8:
                qs.scale_to_fit_width(12.8)
            qs.set_x(0)
            self.play(FadeIn(qs), run_time=0.6)
            vo.wait_until("although related words")
            words = VGroup(source_tag("measured"), serif('"home health aide" appears in 15 passages of the E2 library', 22)
                           ).arrange(RIGHT, buff=0.2).to_edge(DOWN, buff=0.35)
            self.play(FadeIn(words), run_time=0.6)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 3 ---------------------------------------------------------------- why it matters
        with self.voiceover(SAY[2]) as vo:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
            n1 = VGroup(source_tag("code"),
                        VGroup(serif("on this branch,", 28), mono("careonex-chunk run", 28, S.BLUE), serif("cuts with", 28),
                               mono("B", 30, CHUNKERS[1][3]), mono("(CHUNKER_VERSION 4)", 24, S.GREY)).arrange(RIGHT, buff=0.18)
                        ).arrange(RIGHT, buff=0.3)
            n2 = VGroup(source_tag("code"),
                        VGroup(serif("the main library was built with", 28), mono("A", 30, CHUNKERS[0][3]),
                               mono("(CHUNKER_VERSION 2)", 24, S.GREY)).arrange(RIGHT, buff=0.18)).arrange(RIGHT, buff=0.3)
            notes = VGroup(n1, n2).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(UP * 1.4)
            if notes.width > 13:
                notes.scale_to_fit_width(13)
            self.play(FadeIn(n1, shift=RIGHT * 0.15), run_time=0.8)
            self.play(FadeIn(n2, shift=RIGHT * 0.15), run_time=0.8)
            vo.wait_until("With 25 questions")
            caution = serif("25 questions, provisional grades: gaps this small could change", 28, S.GREY).move_to(DOWN * 0.4)
            self.play(FadeIn(caution), run_time=0.7)
            vo.wait_until("But nothing here")
            ask = VGroup(serif("nothing here shows B is better", 32, QUERY_C),
                         serif("→ worth a team discussion before the main library is rebuilt with it", 26, QUERY_C)
                         ).arrange(DOWN, buff=0.15).move_to(DOWN * 1.9)
            box = SurroundingRectangle(ask, color=QUERY_C, buff=0.25, corner_radius=0.12)
            self.play(FadeIn(ask), Create(box), run_time=0.9)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.play(FadeOut(*self.mobjects), run_time=0.8)
