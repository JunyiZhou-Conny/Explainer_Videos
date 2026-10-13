"""S05 · Feedback search, step by step (READ IN CODE: retriever.py, feedback_expansion.py).

1. Six steps: first search (10 candidates) → read the top results → plan at most one extra search →
   run it → admit a new passage only if it matches the question → merge, keep the top 5.
2. Where an extra search comes from: (a) a phrase from a top result + "Relevant to caller question: …"
   (saved run, showering → "bathing in bed, in the tub or shower"), (b) the caller's key words plus a
   variant from a fixed list ("prepare meals preparation", today's planner).
3. Model-free vs the `intent` mode (Nova Lite; README: permission the team profile may not have).
4. Reciprocal rank fusion, worked example with weights 1.5 / 1.0.
5. The consequence (MEASURED with his own function, checks/marco/rrf_reach.py): a new-only passage scores
   at most 1/61 < 1.5/70, so it cannot reach the top 5 unless the first search returned fewer than 5.
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (AWS_C, BAD_C, CODE_C, DATA_C, GUESS_C, MARCO_C, NARRATION, OK_C, QUERY_C, aws, mark_bad,
                    mark_ok, mono, sans, serif, source_tag, strike, text_panel)

SAY = NARRATION["S05"]
NEW_C = S.TEAL


def step_box(n: int, text: str, width: float = 3.7) -> VGroup:
    num = mono(str(n), 30, QUERY_C)
    t = VGroup(*[serif(ln, 24) for ln in text.split("\n")]).arrange(DOWN, buff=0.05, aligned_edge=LEFT)
    inner = VGroup(num, t).arrange(RIGHT, buff=0.25)
    frame = RoundedRectangle(width=width, height=1.25, corner_radius=0.14, stroke_color=CODE_C,
                             stroke_width=2.5).set_fill(CODE_C, 0.08)
    if inner.width > width - 0.3:
        inner.scale_to_fit_width(width - 0.3)
    inner.move_to(frame).align_to(frame, LEFT).shift(RIGHT * 0.2)
    g = VGroup(frame, inner)
    g.frame = frame
    return g


def pchip(label: str, color: str = DATA_C, width: float = 1.1) -> VGroup:
    t = mono(label, 22)
    bg = RoundedRectangle(width=width, height=0.42, corner_radius=0.08, stroke_color=color,
                          stroke_width=2).set_fill(color, 0.25)
    t.move_to(bg)
    return VGroup(bg, t)


class Feedback(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- six steps
        with self.voiceover(SAY[0]) as vo:
            hdr = VGroup(sans("FEEDBACK MODE", 22, QUERY_C), mono("retriever.py · feedback_expansion.py", 20, S.GREY),
                         source_tag("code")).arrange(RIGHT, buff=0.3).to_edge(UP, buff=0.4)
            steps = [step_box(1, "first search: the caller's\nexact words (10 results)"),
                     step_box(2, "read the top results"),
                     step_box(3, "plan at most\none more search"),
                     step_box(4, "run it"),
                     step_box(5, "admit a new passage only\nif it matches the question"),
                     step_box(6, "merge the two lists,\nkeep the top 5")]
            top = VGroup(*steps[:3]).arrange(RIGHT, buff=0.6).move_to(UP * 1.2)
            bot = VGroup(*steps[3:][::-1]).arrange(RIGHT, buff=0.6).move_to(DOWN * 1.2)
            arrows = VGroup(Arrow(steps[0].get_right(), steps[1].get_left(), buff=0.06, color=S.GREY, stroke_width=3),
                            Arrow(steps[1].get_right(), steps[2].get_left(), buff=0.06, color=S.GREY, stroke_width=3),
                            Arrow(steps[2].get_bottom(), steps[3].get_top(), buff=0.06, color=S.GREY, stroke_width=3),
                            Arrow(steps[3].get_left(), steps[4].get_right(), buff=0.06, color=S.GREY, stroke_width=3),
                            Arrow(steps[4].get_left(), steps[5].get_right(), buff=0.06, color=S.GREY, stroke_width=3))
            self.play(FadeIn(hdr), run_time=0.6)
            anchors = ["retrieve first searches", "Then it reads", "may plan one more search", "It runs it",
                       "keeps a new passage", "and merges the two lists"]
            for i, a in enumerate(anchors):
                vo.wait_until(a)
                anims = [FadeIn(steps[i], shift=UP * 0.1)]
                if i:
                    anims.append(GrowArrow(arrows[i - 1]))
                self.play(*anims, run_time=0.6)
                self.play(Indicate(steps[i].frame, color=QUERY_C, scale_factor=1.03), run_time=0.5)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- where an extra search comes from
        with self.voiceover(SAY[1]) as vo:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
            hdr2 = sans("WHERE THE EXTRA SEARCH COMES FROM", 22, QUERY_C).to_edge(UP, buff=0.4)
            self.play(FadeIn(hdr2), run_time=0.5)
            # (a) from the results
            la = VGroup(mono("a", 28, QUERY_C), sans("FROM THE FIRST RESULTS", 20, S.GREY)).arrange(RIGHT, buff=0.2)
            qa = VGroup(serif('"My mother needs help showering.', 26, QUERY_C),
                        serif(' What kind of assistance might be available?"', 26, QUERY_C)).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
            pa = text_panel(["PCA page · top result", "… help with bathing in bed,", "in the tub or shower …"], size=22,
                            border=DATA_C, colors={0: S.GREY}, t2c={"bathing in bed,": QUERY_C, "in the tub or shower": QUERY_C})
            ea = text_panel(["extra search:", "bathing in bed, in the tub or shower.", "Relevant to caller question: My mother …"],
                            size=22, border=QUERY_C, colors={0: S.GREY, 1: QUERY_C})
            A = VGroup(la, qa, pa, ea).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
            # (b) from the caller's words
            lb = VGroup(mono("b", 28, QUERY_C), sans("ELSE: FROM THE CALLER'S WORDS", 20, S.GREY)).arrange(RIGHT, buff=0.2)
            words = ["Can", "a", "caregiver", "help", "prepare", "meals", "at", "home?"]
            qb = VGroup(*[serif(w, 26, QUERY_C) for w in words]).arrange(RIGHT, buff=0.14)
            keep = {"prepare", "meals"}
            pairs = text_panel(["fixed list (~30 pairs):", "prepare → preparation", "showering → bathing",
                                "lonely → companionship", "…"], size=22, colors={0: S.GREY, 1: QUERY_C})
            eb = text_panel(["extra search:", "prepare meals preparation"], size=22, border=QUERY_C,
                            colors={0: S.GREY, 1: QUERY_C})
            B = VGroup(lb, qb, pairs, eb).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
            cols = VGroup(A, B).arrange(RIGHT, buff=0.8, aligned_edge=UP)
            if cols.width > 13.2:
                cols.scale_to_fit_width(13.2)
            cols.next_to(hdr2, DOWN, buff=0.4)
            vo.wait_until("a heading or phrase")
            self.play(FadeIn(la), FadeIn(qa), run_time=0.6)
            self.play(FadeIn(pa, shift=UP * 0.1), run_time=0.7)
            vo.wait_until("If none qualifies")
            self.play(FadeIn(lb), FadeIn(qb), run_time=0.6)
            strikes = VGroup(*[strike(m, S.GREY, 3) for w, m in zip(words, qb) if w not in keep])
            self.play(Create(strikes), *[m.animate.set_opacity(0.4) for w, m in zip(words, qb) if w not in keep], run_time=0.8)
            vo.wait_until("plus a variant")
            self.play(FadeIn(pairs, shift=UP * 0.1), run_time=0.6)
            self.play(Indicate(pairs.rows[1], color=QUERY_C), run_time=0.6)
            self.play(FadeIn(eb, shift=UP * 0.1), run_time=0.6)
            tagb = VGroup(source_tag("measured"), serif("today's planner", 20, S.GREY)).arrange(RIGHT, buff=0.15)
            tagb.next_to(eb, DOWN, buff=0.15).align_to(eb, LEFT)
            self.play(FadeIn(tagb), run_time=0.4)
            vo.wait_until("one run added the search")
            self.play(FadeIn(ea, shift=UP * 0.1), run_time=0.7)
            taga = VGroup(source_tag("code"), serif("saved 40-question run", 20, S.GREY)).arrange(RIGHT, buff=0.15)
            taga.next_to(ea, DOWN, buff=0.15).align_to(ea, LEFT)
            self.play(FadeIn(taga), Indicate(ea.rows[1], color=QUERY_C), run_time=0.8)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 3 ---------------------------------------------------------------- model-free
        with self.voiceover(SAY[2]) as vo:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
            left = VGroup(mono('search_mode = "feedback"', 26, QUERY_C), serif("model-free", 30),
                          text_panel(["fixed rules only:", "· a stop-word list", "· ~30 word pairs",
                                      "· shared-word checks"], size=22, colors={0: S.GREY}),
                          VGroup(mark_ok(0.35), serif("no AI model is called", 24, OK_C)).arrange(RIGHT, buff=0.15)
                          ).arrange(DOWN, buff=0.3)
            nova = aws("bedrock model", "Nova Lite", "writes extra searches", width=3.6, name_size=26, sub_size=20)
            lock = VGroup(mark_bad(0.3), serif("may not be allowed", 24, BAD_C)).arrange(RIGHT, buff=0.15)
            right = VGroup(mono('search_mode = "intent"', 26, S.GREY), serif("asks a language model", 30), nova, lock
                           ).arrange(DOWN, buff=0.3)
            pair = VGroup(left, right).arrange(RIGHT, buff=1.6, aligned_edge=UP).move_to(UP * 0.3)
            self.play(FadeIn(left, shift=UP * 0.15), run_time=1.0)
            vo.wait_until("Another mode, called intent")
            self.play(FadeIn(right[:3], shift=UP * 0.15), run_time=0.9)
            vo.wait_until("the README warns")
            quote = VGroup(source_tag("notes"),
                           serif('README: "require IAM permission your team profile may not have"', 22, S.GREY)
                           ).arrange(RIGHT, buff=0.2).to_edge(DOWN, buff=0.45)
            self.play(FadeIn(lock), FadeIn(quote), run_time=0.8)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 4 ---------------------------------------------------------------- reciprocal rank fusion
        with self.voiceover(SAY[3]) as vo:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
            hdr = VGroup(sans("MERGING: RECIPROCAL RANK FUSION", 22, QUERY_C), source_tag("code")).arrange(RIGHT, buff=0.3)
            hdr.to_edge(UP, buff=0.4)
            rule = VGroup(mono("points = weight / (60 + rank)", 28), serif("first search: weight 1.5 · extra search: 1.0", 24, S.GREY)
                          ).arrange(DOWN, buff=0.1).next_to(hdr, DOWN, buff=0.3)
            self.play(FadeIn(hdr), FadeIn(rule), run_time=0.8)
            first = ["p1", "p2", "p3", "p4", "p5"]
            extra = ["p3", "new", "p1"]
            colA = VGroup(sans("FIRST SEARCH ×1.5", 18, S.GREY),
                          *[VGroup(mono(str(r), 20, S.GREY), pchip(p)).arrange(RIGHT, buff=0.15) for r, p in enumerate(first, 1)],
                          serif("… to rank 10", 20, S.GREY)).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
            colB = VGroup(sans("EXTRA SEARCH ×1.0", 18, S.GREY),
                          *[VGroup(mono(str(r), 20, S.GREY), pchip(p, NEW_C if p == "new" else DATA_C)).arrange(RIGHT, buff=0.15)
                            for r, p in enumerate(extra, 1)]).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
            score = {"p1": 1.5 / 61 + 1 / 63, "p2": 1.5 / 62, "p3": 1.5 / 63 + 1 / 61, "p4": 1.5 / 64, "p5": 1.5 / 65}
            how = {"p1": "1.5/61 + 1/63", "p2": "1.5/62", "p3": "1.5/63 + 1/61", "p4": "1.5/64", "p5": "1.5/65"}
            merged = sorted(score, key=lambda k: -score[k])
            colC = VGroup(sans("MERGED TOP 5", 18, QUERY_C),
                          *[VGroup(mono(str(r), 20, S.GREY), pchip(p), mono(f"{how[p]} = {score[p]:.4f}", 20, S.WHITE)
                                   ).arrange(RIGHT, buff=0.15) for r, p in enumerate(merged, 1)]
                          ).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
            cols = VGroup(colA, colB, colC).arrange(RIGHT, buff=0.9, aligned_edge=UP).next_to(rule, DOWN, buff=0.45)
            if cols.width > 13:
                cols.scale_to_fit_width(13)
            cols.set_x(0)
            self.play(FadeIn(colA, shift=UP * 0.1), run_time=0.8)
            self.play(FadeIn(colB, shift=UP * 0.1), run_time=0.8)
            vo.wait_until("and the first search counts")
            self.play(Indicate(colA[0], color=QUERY_C), run_time=0.7)
            vo.wait_until("A passage that both")
            self.play(LaggedStart(*[FadeIn(r, shift=LEFT * 0.1) for r in colC], lag_ratio=0.2), run_time=1.6)
            rise = VGroup(colA[3][1], colB[1][1], colC[2][1])
            self.play(Indicate(rise, color=QUERY_C, scale_factor=1.1), run_time=1.0)
            note = serif("p3 was 3rd; both searches found it → now 2nd", 24, QUERY_C).to_edge(DOWN, buff=0.4)
            self.play(FadeIn(note), run_time=0.6)
            where = VGroup(pchip("new", NEW_C), mono("1/62 = 0.0161 → 11th, after p6 … p10", 20, NEW_C)).arrange(RIGHT, buff=0.15)
            where.next_to(colC, DOWN, buff=0.3).align_to(colC, LEFT)
            self.play(FadeIn(where, shift=UP * 0.1), run_time=0.6)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 5 ---------------------------------------------------------------- can a new passage get in?
        with self.voiceover(SAY[4]) as vo:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
            hdr = VGroup(sans("CAN A PASSAGE FOUND ONLY BY THE EXTRA SEARCH REACH THE TOP 5?", 22, QUERY_C),
                         source_tag("measured")).arrange(RIGHT, buff=0.3).to_edge(UP, buff=0.4)
            if hdr.width > 13:
                hdr.scale_to_fit_width(13)
            self.play(FadeIn(hdr), run_time=0.6)
            W = 5.6 / (1.5 / 70)
            b_new = Rectangle(width=W / 61, height=0.55, stroke_width=0).set_fill(NEW_C, 0.9)
            b_10 = Rectangle(width=W * 1.5 / 70, height=0.55, stroke_width=0).set_fill(DATA_C, 0.9)
            r1 = VGroup(serif("best a new-only passage can score", 26), b_new,
                        mono("1/61 = 0.016", 24, NEW_C))
            r2 = VGroup(serif("10th result of the first search", 26), b_10,
                        mono("1.5/70 = 0.021", 24, DATA_C))
            r2[0].next_to(r1[0], DOWN, buff=0.5).align_to(r1[0], RIGHT)
            for r in (r1, r2):
                r[1].next_to(r1[0], RIGHT, buff=0.3).set_y(r[0].get_y())
                r[2].next_to(r[1], RIGHT, buff=0.2)
            bars = VGroup(r1, r2)
            bars.move_to(UP * 1.4)
            if bars.width > 13:
                bars.scale_to_fit_width(13)
            vo.wait_until("A passage found only")
            self.play(FadeIn(r1[0]), GrowFromEdge(r1[1], LEFT), FadeIn(r1[2]), run_time=0.9)
            vo.wait_until("The tenth result")
            self.play(FadeIn(r2[0]), GrowFromEdge(r2[1], LEFT), FadeIn(r2[2]), run_time=0.9)
            vo.wait_until("So today the extra search")
            res = text_panel(["his reciprocal_rank_fusion, weights [1.5, 1.0], every extra hit new:",
                              "  first search returned 10 → top 5 = first1 … first5",
                              "  first search returned  4 → top 5 = first1 … first4, new1"],
                             size=20, colors={0: S.GREY, 1: S.WHITE, 2: S.WHITE}).move_to(DOWN * 0.45)
            if res.width > 12.6:
                res.scale_to_fit_width(12.6)
            self.play(FadeIn(res, shift=UP * 0.1), run_time=0.8)
            concl = serif("today the extra search can reorder what the first search found, not add to it", 26, QUERY_C)
            concl.next_to(res, DOWN, buff=0.3)
            if concl.width > 13:
                concl.scale_to_fit_width(13)
            self.play(FadeIn(concl), run_time=0.6)
            vo.wait_until("The code's comments")
            guess = VGroup(source_tag("inferred"),
                           serif('code comment: "… before RRF can promote it" → new passages were meant to get in? ask Marco',
                                 21, GUESS_C)).arrange(RIGHT, buff=0.2).to_edge(DOWN, buff=0.4)
            if guess.width > 13:
                guess.scale_to_fit_width(13)
            self.play(FadeIn(guess), run_time=0.6)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.play(FadeOut(*self.mobjects), run_time=0.8)
