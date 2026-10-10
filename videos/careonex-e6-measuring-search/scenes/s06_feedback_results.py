"""S06 · What the saved 40-question run shows (MEASURED from evaluation/universal_homecare_v2_full_prior.json).

1. 40 questions, library C, an earlier planner, equal-weight merge: extra searches for 18; top 5 unchanged
   for 23 (22 without an extra search + 1 with).
2. Time per search, one dot per question: median 0.43 → 0.51 s; slowest tenth 0.51 → 1.01 s.
3. Grades: 0 of 788 saved passages carry one.
4. Today's planner replayed on the same 40 first searches: extra search for 17 (16 rewrites, 1 from a
   heading); feedback is the voice app's default.
"""

import statistics as st

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (BAD_C, CODE_C, DATA_C, METRICS, NARRATION, QUERY_C, REPLAY, mono, sans, serif, source_tag,
                    sticky, text_panel)

SAY = NARRATION["S06"]
RUN = METRICS["feedback_run"]
CASES = RUN["cases"]


class FeedbackResults(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- 40 questions
        with self.voiceover(SAY[0]) as vo:
            hdr = VGroup(sans("THE SAVED 40-QUESTION RUN", 22, QUERY_C), source_tag("measured")).arrange(RIGHT, buff=0.3)
            hdr.to_edge(UP, buff=0.4)
            sub = serif("library C · same questions with and without feedback · an earlier planner · equal-weight merge",
                        22, S.GREY).next_to(hdr, DOWN, buff=0.15)
            if sub.width > 13:
                sub.scale_to_fit_width(13)
            dots = VGroup(*[Circle(0.22, stroke_color=S.GREY, stroke_width=2.5).set_fill(S.GREY_DARK, 0.6) for _ in CASES])
            dots.arrange_in_grid(rows=4, cols=10, buff=0.32).move_to(DOWN * 0.1 + LEFT * 2.2)
            self.play(FadeIn(hdr), FadeIn(sub), run_time=0.7)
            self.play(LaggedStart(*[FadeIn(d, scale=0.6) for d in dots], lag_ratio=0.02), run_time=1.2)
            legend = VGroup(VGroup(Circle(0.16, stroke_color=QUERY_C, stroke_width=4), serif("an extra search was used", 24)).arrange(RIGHT, buff=0.2),
                            VGroup(Circle(0.16, stroke_width=0).set_fill(QUERY_C, 0.85), serif("top 5 changed", 24)).arrange(RIGHT, buff=0.2),
                            VGroup(Circle(0.16, stroke_width=0).set_fill(S.GREY_DARK, 0.9), serif("top 5 identical", 24)).arrange(RIGHT, buff=0.2)
                            ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).next_to(dots, RIGHT, buff=0.8)
            vo.wait_until("Extra searches were used")
            used = [d for d, c in zip(dots, CASES) if c["extra_searches"] > 0]
            n_used = len(used)
            c1 = mono(f"{n_used} / 40", 34, QUERY_C).next_to(legend[0], UP, buff=0.5).align_to(legend, LEFT)
            self.play(FadeIn(legend[0]), *[d.animate.set_stroke(QUERY_C, 4.5) for d in used], FadeIn(c1), run_time=1.0)
            vo.wait_until("For 23 of the 40")
            changed = [d for d, c in zip(dots, CASES) if not c["top5_identical"]]
            n_same = sum(c["top5_identical"] for c in CASES)
            c2 = VGroup(mono(f"{n_same} / 40", 34, S.WHITE), serif("identical", 24, S.GREY)).arrange(RIGHT, buff=0.2)
            c2.next_to(legend, DOWN, buff=0.5).align_to(legend, LEFT)
            self.play(FadeIn(legend[1:]), *[d.animate.set_fill(QUERY_C, 0.85) for d in changed], run_time=1.0)
            self.play(FadeIn(c2), run_time=0.5)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- time per search
        with self.voiceover(SAY[1]) as vo:
            self.play(*[FadeOut(m) for m in self.mobjects if m is not hdr], run_time=0.6)
            ax_w, x0 = 10.0, -5.0
            tmax = 2.0

            def x_of(ms):
                return x0 + ax_w * min(ms / 1000, tmax) / tmax

            axis = NumberLine(x_range=[0, tmax, 0.5], length=ax_w, include_numbers=False, color=S.GREY)
            axis.move_to([x0 + ax_w / 2, -2.2, 0])
            ticks = VGroup(*[mono(f"{t:g} s", 20, S.GREY).next_to(axis.n2p(t), DOWN, buff=0.15) for t in (0, 0.5, 1, 1.5, 2)])
            rows = {}
            for key, y, col, label in [("baseline_ms", 0.6, S.GREY, "one search"), ("feedback_ms", -1.0, QUERY_C, "feedback")]:
                vals = [c[key] for c in CASES]
                pts = VGroup(*[Dot([x_of(v), y + ((i % 5) - 2) * 0.12, 0], radius=0.07, color=col).set_opacity(0.85)
                               for i, v in enumerate(vals)])
                med = st.median(vals)
                p90 = st.quantiles(vals, n=10)[-1]
                mline = Line([x_of(med), y - 0.4, 0], [x_of(med), y + 0.4, 0], color=S.WHITE, stroke_width=4)
                pline = DashedLine([x_of(p90), y - 0.4, 0], [x_of(p90), y + 0.4, 0], color=S.WHITE, stroke_width=3)
                lab = serif(label, 26, col).move_to([x0 - 0.2, y, 0], aligned_edge=RIGHT)
                mtxt = mono(f"median {med / 1000:.2f} s", 20).next_to(mline, UP, buff=0.08)
                ptxt = mono(f"slowest tenth {p90 / 1000:.2f} s", 20, S.GREY).next_to(pline, UP, buff=0.08)
                if ptxt.get_left()[0] < mtxt.get_right()[0] + 0.15:
                    ptxt.next_to(pline, DOWN, buff=0.08)
                rows[key] = VGroup(lab, pts, mline, pline, mtxt, ptxt)
            ttl = serif("time per search, one dot per question", 24, S.GREY).next_to(hdr, DOWN, buff=0.25)
            self.play(FadeIn(ttl), Create(axis), FadeIn(ticks), run_time=0.8)
            self.play(FadeIn(rows["baseline_ms"][0]), LaggedStart(*[FadeIn(d) for d in rows["baseline_ms"][1]], lag_ratio=0.02),
                      run_time=1.0)
            self.play(FadeIn(rows["feedback_ms"][0]), LaggedStart(*[FadeIn(d) for d in rows["feedback_ms"][1]], lag_ratio=0.02),
                      run_time=1.0)
            vo.wait_until("The typical search")
            self.play(*[Create(rows[k][2]) for k in rows], *[FadeIn(rows[k][4]) for k in rows], run_time=0.8)
            vo.wait_until("and the slowest tenth")
            self.play(*[Create(rows[k][3]) for k in rows], *[FadeIn(rows[k][5]) for k in rows], run_time=0.8)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 3 ---------------------------------------------------------------- no grades
        with self.voiceover(SAY[2]) as vo:
            self.play(*[FadeOut(m) for m in self.mobjects if m is not hdr], run_time=0.6)
            rows = ["question            mode       rank  relevance",
                    "daily_bathing       one search  1     —",
                    "daily_bathing       feedback    1     —",
                    "daily_dressing      one search  1     —",
                    "daily_meals         feedback    3     —",
                    "…                   …           …     —"]
            tbl = text_panel(rows, size=22, colors={0: S.GREY}, t2c={"—": BAD_C}).move_to(UP * 0.6 + LEFT * 2.4)
            big = VGroup(mono(f"{RUN['passages_graded']} / {RUN['passages_total']}", 54, BAD_C),
                         serif("saved passages", 26, BAD_C), serif("with a grade", 26, BAD_C)).arrange(DOWN, buff=0.1).next_to(tbl, RIGHT, buff=0.7)
            self.play(FadeIn(tbl, shift=UP * 0.1), run_time=0.9)
            vo.wait_until("none of the 788")
            self.play(FadeIn(big, scale=1.1), run_time=0.8)
            vo.wait_until("So the run tells us")
            tells = VGroup(VGroup(serif("tells us:", 26, S.GREY), serif("speed · how often the list changes", 26)).arrange(RIGHT, buff=0.2),
                           VGroup(serif("does not tell us:", 26, S.GREY), serif("whether the passages got better", 26, BAD_C)).arrange(RIGHT, buff=0.2)
                           ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).to_edge(DOWN, buff=0.7)
            self.play(FadeIn(tells[0]), run_time=0.6)
            self.play(FadeIn(tells[1]), run_time=0.6)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 4 ---------------------------------------------------------------- today's planner, replayed
        with self.voiceover(SAY[3]) as vo:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
            hdr4 = VGroup(sans("TODAY'S PLANNER, REPLAYED ON THE SAME 40 FIRST SEARCHES", 22, QUERY_C), source_tag("measured")
                          ).arrange(RIGHT, buff=0.3).to_edge(UP, buff=0.4)
            reasons = REPLAY["reasons"]
            spec = [("question_rewrite_used", "extra search from the caller's words", QUERY_C),
                    ("feedback_used", "extra search from a heading", QUERY_C),
                    ("no_safe_expansion", "no safe extra search", S.GREY),
                    ("unverified_provider_claim", "asks about a specific provider", S.GREY),
                    ("already_supported", "first results already match", S.GREY)]
            unit = 0.32
            rows = VGroup()
            for key, label, col in spec:
                n = reasons.get(key, 0)
                bar = Rectangle(width=max(0.02, n * unit), height=0.36, stroke_width=0).set_fill(col, 0.85)
                rows.add(VGroup(serif(label, 24, S.WHITE if col == QUERY_C else S.GREY), bar, mono(str(n), 24, col)))
            lw = max(r[0].width for r in rows)
            for i, r in enumerate(rows):
                r[0].move_to([0, -i * 0.58, 0], aligned_edge=RIGHT)
                r[1].next_to(r[0], RIGHT, buff=0.25)
                r[2].next_to(r[1], RIGHT, buff=0.15)
            rows.move_to(UP * 0.5 + RIGHT * 0.9)
            brace = Brace(VGroup(rows[0], rows[1]), LEFT, color=QUERY_C)
            btxt = mono(f"{reasons.get('question_rewrite_used', 0) + reasons.get('feedback_used', 0)} / 40", 30, QUERY_C)
            btxt.next_to(brace, LEFT, buff=0.15)
            self.play(FadeIn(hdr4), run_time=0.5)
            vo.wait_until("We replayed today's version")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(r[0]), GrowFromEdge(r[1], LEFT), FadeIn(r[2])) for r in rows],
                                  lag_ratio=0.25), run_time=2.0)
            vo.wait_until("it adds a search for 17")
            self.play(GrowFromCenter(brace), FadeIn(btxt), run_time=0.7)
            vo.wait_until("And feedback is now the default")
            note = sticky("CAREONEX_VOICE_SEARCH_MODE", '"feedback"').scale(1.1)
            cap = VGroup(serif("the voice app's default", 24), mono("services/voice/nova_sonic/tools.py", 18, S.GREY),
                         source_tag("code")).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
            VGroup(note, cap).arrange(RIGHT, buff=0.35).to_edge(DOWN, buff=0.5)
            self.play(FadeIn(note, shift=UP * 0.15), FadeIn(cap), run_time=0.8)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.play(FadeOut(*self.mobjects), run_time=0.8)
