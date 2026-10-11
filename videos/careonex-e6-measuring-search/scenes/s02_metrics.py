"""S02 · How do you measure "found the right passage"?

1. A question, the top 5 passages, a person grades each: 0 no help · 1 partly · 2 answers it → 0 2 1 0 0.
2. Precision@5 = 2 / 5 = 0.4. MRR: first helpful passage at rank 2 → 1 / 2 = 0.5.
3. NDCG: gain 2^g − 1, discount log2(rank + 1); ours 2.39, best order (2 1 0 0 0) 3.63 → 0.66.
   Footnote: Marco's scorer builds the best order from every passage any of the three libraries returned.
4. Warning: the scores are only as good as the grades.
"""

import math

from manim import *

from explainer import style as S
from explainer.components import person_icon
from explainer.scene import VoiceScene

from common import BAD_C, DATA_C, NARRATION, OK_C, QUERY_C, doc_glyph, mono, sans, serif, source_tag, text_panel

SAY = NARRATION["S02"]
GRADES = [0, 2, 1, 0, 0]
GRADE_C = {0: S.GREY, 1: S.GOLD, 2: OK_C}


def dcg(grades):
    return sum((2 ** g - 1) / math.log2(r + 1) for r, g in enumerate(grades, 1))


class Metrics(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- a person grades the top 5
        with self.voiceover(SAY[0]) as vo:
            q = VGroup(sans("QUESTION", 20, QUERY_C), serif('"Does Medicaid pay for help with bathing at home?"', 30, QUERY_C)
                       ).arrange(RIGHT, buff=0.3).to_edge(UP, buff=0.5)
            self.play(FadeIn(q, shift=DOWN * 0.15), run_time=0.7)
            vo.wait_until("take the top 5")
            cards = VGroup()
            for r in range(1, 6):
                g = doc_glyph(DATA_C, width=1.0, height=1.3, lines=5)
                lab = mono(f"rank {r}", 22, S.GREY).next_to(g, DOWN, buff=0.15)
                cards.add(VGroup(g, lab))
            cards.arrange(RIGHT, buff=0.75).move_to(UP * 0.4)
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cards], lag_ratio=0.15), run_time=1.3)
            vo.wait_until("a person grades")
            grader = VGroup(person_icon(S.WHITE, height=0.7), sans("A PERSON", 18, S.GREY)).arrange(DOWN, buff=0.08)
            grader.to_edge(LEFT, buff=0.5).shift(DOWN * 1.6)
            legend = VGroup(*[VGroup(mono(str(k), 28, GRADE_C[k]), serif(t, 24, S.GREY)).arrange(RIGHT, buff=0.15)
                              for k, t in [(0, "no help"), (1, "partly helps"), (2, "answers it")]]
                            ).arrange(RIGHT, buff=0.7).move_to(DOWN * 2.4)
            self.play(FadeIn(grader), FadeIn(legend), run_time=0.8)
            marks = VGroup()
            for c, g in zip(cards, GRADES):
                m = mono(str(g), 44, GRADE_C[g]).next_to(c[0], UP, buff=0.2)
                marks.add(m)
            vo.wait_until("0 if it does not help")
            self.play(LaggedStart(*[FadeIn(m, scale=1.4) for m in marks], lag_ratio=0.35), run_time=2.2)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- precision and MRR
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(grader), FadeOut(legend), run_time=0.5)
            helpful = [i for i, g in enumerate(GRADES) if g > 0]
            boxes = VGroup(*[SurroundingRectangle(VGroup(cards[i], marks[i]), color=OK_C, buff=0.1, corner_radius=0.1)
                             for i in helpful])
            p = VGroup(mono("precision@5", 30, S.WHITE), mono("=", 30, S.GREY), mono("2 / 5", 30, OK_C),
                       mono("=", 30, S.GREY), mono("0.4", 34, QUERY_C)).arrange(RIGHT, buff=0.2)
            p_sub = serif("share of the five that help at all", 24, S.GREY)
            P = VGroup(p, p_sub).arrange(DOWN, buff=0.1, aligned_edge=LEFT).move_to(DOWN * 2.2 + LEFT * 3.4)
            self.play(Create(boxes), run_time=0.8)
            self.play(FadeIn(P, shift=UP * 0.15), run_time=0.8)
            vo.wait_until("MRR looks only")
            arrow = Arrow(cards[1].get_bottom() + DOWN * 0.85, cards[1].get_bottom() + DOWN * 0.05, color=QUERY_C,
                          buff=0.05, stroke_width=5)
            m = VGroup(mono("MRR", 30, S.WHITE), mono("=", 30, S.GREY), mono("1 / 2", 30, QUERY_C),
                       mono("=", 30, S.GREY), mono("0.5", 34, QUERY_C)).arrange(RIGHT, buff=0.2)
            m_sub = serif("1 / rank of the first helpful passage", 24, S.GREY)
            M = VGroup(m, m_sub).arrange(DOWN, buff=0.1, aligned_edge=LEFT).move_to(DOWN * 2.2 + RIGHT * 3.3)
            self.play(FadeOut(boxes), GrowArrow(arrow), run_time=0.7)
            self.play(FadeIn(M, shift=UP * 0.15), run_time=0.8)
            vo.wait_until("Rank 1 would score 1")
            r1 = serif("(helpful passage at rank 1 → MRR = 1)", 22, S.GREY).next_to(M, DOWN, buff=0.15).align_to(M, LEFT)
            self.play(FadeIn(r1), run_time=0.5)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 3 ---------------------------------------------------------------- NDCG, worked out
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(P, M, r1, arrow)), VGroup(cards, marks).animate.scale(0.55).to_edge(UP, buff=1.0),
                      FadeOut(q), run_time=0.8)
            hdr = sans("NDCG: REWARDS PUTTING THE BEST PASSAGES FIRST", 22, QUERY_C).to_edge(UP, buff=0.45)
            self.play(FadeIn(hdr), run_time=0.5)

            def table(grades, label, color):
                rows = [f"{'rank':<6}{'grade':<7}{'points':<8}{'÷ discount':<12}"]
                for r, g in enumerate(grades, 1):
                    rows.append(f"{r:<6}{g:<7}{2 ** g - 1:<8}{'÷ %.2f' % math.log2(r + 1):<12}")
                rows.append(f"total {dcg(grades):.2f}")
                t = text_panel(rows, size=20, colors={0: S.GREY, 6: color})
                return VGroup(sans(label, 20, color), t).arrange(DOWN, buff=0.12, aligned_edge=LEFT)

            ours = table(GRADES, "OUR ORDER", S.WHITE)
            best = table(sorted(GRADES, reverse=True), "BEST POSSIBLE ORDER", OK_C)
            pair = VGroup(ours, best).arrange(RIGHT, buff=0.8, aligned_edge=UP)
            if pair.width > 10.5:
                pair.scale_to_fit_width(10.5)
            pair.move_to(UP * 0.15)
            self.play(FadeIn(ours, shift=UP * 0.15), run_time=0.8)
            rule = serif("points = 2^grade − 1 · discount = log2(rank + 1), grows with rank", 22, S.GREY).next_to(pair, DOWN, buff=0.2)
            self.play(FadeIn(rule), run_time=0.5)
            vo.wait_until("then scores the best possible order")
            self.play(FadeIn(best, shift=UP * 0.15), run_time=0.8)
            vo.wait_until("and divides")
            res = VGroup(mono("NDCG", 30), mono("=", 30, S.GREY), mono(f"{dcg(GRADES):.2f} / {dcg(sorted(GRADES, reverse=True)):.2f}", 30),
                         mono("=", 30, S.GREY), mono(f"{dcg(GRADES) / dcg(sorted(GRADES, reverse=True)):.2f}", 36, QUERY_C)
                         ).arrange(RIGHT, buff=0.2)
            perfect = serif("(1 = perfect order)", 24, S.GREY)
            VGroup(res, perfect).arrange(RIGHT, buff=0.4).next_to(rule, DOWN, buff=0.3)
            self.play(FadeIn(res, shift=LEFT * 0.15), run_time=0.8)
            self.play(FadeIn(perfect), run_time=0.5)
            foot = VGroup(source_tag("code"),
                          serif("in Marco's scorer, \"best order\" = the best five passages any of the three test libraries returned",
                                20, S.GREY)).arrange(RIGHT, buff=0.2).to_edge(DOWN, buff=0.35)
            if foot.width > 13:
                foot.scale_to_fit_width(13)
            self.play(FadeIn(foot), run_time=0.5)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 4 ---------------------------------------------------------------- no grades, no score
        with self.voiceover(SAY[3]) as vo:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
            three = VGroup(mono("precision@5", 32), mono("MRR", 32), mono("NDCG", 32)).arrange(RIGHT, buff=0.9)
            three.move_to(UP * 1.0)
            src = VGroup(person_icon(S.WHITE, height=0.6), serif("grades 0 · 1 · 2, given by a person", 28)
                         ).arrange(RIGHT, buff=0.3).move_to(DOWN * 0.9)
            arrows = VGroup(*[Arrow(src.get_top(), t.get_bottom(), buff=0.15, color=S.GREY, stroke_width=3)
                              for t in three])
            self.play(FadeIn(three), run_time=0.6)
            self.play(FadeIn(src), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2), run_time=1.0)
            vo.wait_until("No grades, no score")
            warn = serif("no grades → no score", 34, BAD_C).to_edge(DOWN, buff=0.7)
            self.play(FadeIn(warn, shift=UP * 0.15), run_time=0.6)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.play(FadeOut(*self.mobjects), run_time=0.8)
