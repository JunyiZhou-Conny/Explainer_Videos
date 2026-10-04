"""S01 · The differencing attack (reference scene for the rest of the video).

Beats: the hospital count (41) -> Alice arrives (42) -> subtract -> ponder: would rounding to the
nearest ten help? -> the rounding number line 40..50 with its jump at 44 -> 45 (S05 brings the same
number line back) -> the two questions -> the paper -> the roadmap.
"""

import numpy as np
from manim import *

from explainer import style as S
from explainer.components import paper_page, person_icon, ponder_card
from explainer.scene import VoiceScene

from common import ALICE, NARRATION, PAPER_P1, X_COLOR, XP_COLOR

SAY = NARRATION["S01"]


def query_card(question: str, width: float = 4.6) -> VGroup:
    q = S.text(question, 28, S.WHITE, line_spacing=1.0)
    if q.width > width - 0.5:
        q.scale_to_fit_width(width - 0.5)
    head = S.text("Query", 22, S.GREY, font=S.FONT_SANS)
    body = VGroup(head, q).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    frame = RoundedRectangle(width=width, height=body.height + 0.5, corner_radius=0.15,
                             stroke_color=S.GREY, stroke_width=2).set_fill(S.GREY_DARKER, 1)
    body.move_to(frame)
    return VGroup(frame, head, q)


def drain(scene, card, seconds: float) -> None:
    """The silent ponder timer of explainer.components.pause_and_ponder, for a card already shown."""
    bar = card[3]
    target = bar.copy().scale(0.001, about_point=bar.get_start())
    scene.play(bar.animate(rate_func=linear).become(target), run_time=seconds)


class Hook(VoiceScene):
    def construct(self):
        rng = np.random.default_rng(3)

        # ---------------------------------------------------------- the database
        cols, rows = 15, 8
        n_slots = cols * rows                       # 120 slots; the last one is Alice's
        sick = set(rng.choice(n_slots - 1, size=41, replace=False).tolist())
        icons = VGroup(*[person_icon(ALICE if (i in sick or i == n_slots - 1) else S.GREY, height=0.34)
                         for i in range(n_slots)])
        icons.arrange_in_grid(rows=rows, cols=cols, buff=(0.14, 0.16))
        icons.to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        alice = icons[-1]
        patients = VGroup(*icons[:-1])
        alice_slot = alice.get_center()
        db_title = S.text("Hospital database", 30, S.GREY).next_to(icons, UP, buff=0.35)
        legend = VGroup(person_icon(ALICE, 0.3), S.text("has condition X", 22, S.GREY))
        legend.arrange(RIGHT, buff=0.15).next_to(icons, DOWN, buff=0.3).align_to(icons, LEFT)

        card = query_card("How many patients\nhave condition X?").to_edge(RIGHT, buff=0.6).shift(UP * 1.2)
        answer = S.text("41", 72, S.WHITE).next_to(card, DOWN, buff=0.5)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(db_title), LaggedStart(*[FadeIn(p, scale=0.6) for p in patients],
                                                    lag_ratio=0.01), run_time=2.2)
            self.play(FadeIn(legend), run_time=0.5)
            vo.wait_until("A researcher")
            self.play(FadeIn(card, shift=LEFT * 0.4), run_time=0.8)
            vo.wait_until("how many patients")
            self.play(Indicate(card[2], color=S.WHITE, scale_factor=1.06), run_time=0.9)
            vo.wait_until("The hospital releases")
            self.play(Indicate(icons, color=S.WHITE, scale_factor=1.02), run_time=1.0)
            vo.wait_until("It just says")
            sick_icons = VGroup(*[patients[i] for i in sorted(sick)])
            self.play(LaggedStart(*[Indicate(p, color=ALICE, scale_factor=1.25) for p in sick_icons],
                                  lag_ratio=0.03), run_time=1.0)
            self.play(Write(answer), run_time=0.5)

        # ---------------------------------------------------------- Alice arrives
        alice_label = S.text("Alice", 24, ALICE)
        week = S.text("one week later", 24, S.GREY).next_to(card, UP, buff=0.3)
        answers_y = card.get_bottom()[1] - 0.9
        with self.voiceover(SAY[1]) as vo:
            old_answer = answer
            self.play(old_answer.animate.scale(0.6).set_color(S.GREY)
                      .move_to([card.get_center()[0] - 1.1, answers_y, 0]), FadeIn(week), run_time=0.8)
            alice.move_to([alice_slot[0] + 3.2, alice_slot[1] - 0.2, 0])
            alice_label.next_to(alice, DOWN, buff=0.1)
            vo.wait_until("Alice, is admitted")
            self.play(FadeIn(alice), FadeIn(alice_label), run_time=0.5)
            self.play(alice.animate.move_to(alice_slot),
                      alice_label.animate.next_to(alice_slot, DOWN, buff=0.12),
                      run_time=1.2)
            vo.wait_until("The researcher asks")
            self.play(ShowPassingFlash(card[0].copy().set_stroke(S.WHITE, 5), time_width=0.6),
                      Indicate(card[2], color=S.WHITE, scale_factor=1.06), run_time=0.9)
            new_answer = S.text("42", 72, S.WHITE).move_to([card.get_center()[0] + 0.9, answers_y, 0])
            vo.wait_until("The answer is now")
            self.play(Write(new_answer), run_time=0.6)

        # ---------------------------------------------------------- the subtraction -> ponder
        diff = S.math("42", "-", "41", "=", "1", size=60)
        diff[4].set_color(ALICE)
        diff.move_to([card.get_center()[0], answers_y - 1.15, 0])
        tag = S.text("Alice has condition X", 30, S.RED).next_to(diff, DOWN, buff=0.45)

        col_x = 3.55                                   # centre of the right-hand column
        pair = VGroup()
        for num, who, col in (("41", "without Alice", S.GREY), ("42", "with Alice", ALICE)):
            m = S.math(num, r"\to", "{?}", size=60)    # {?}: ordinary, so \to keeps its space after it
            m[2].set_color(S.YELLOW)
            lab = S.text(who, 22, col).next_to(m[0], DOWN, buff=0.18)
            pair.add(VGroup(m, lab))
        pair.arrange(RIGHT, buff=1.0).move_to([col_x, 2.35, 0])
        ponder = ponder_card("Would rounding the count\nto the nearest ten\nprotect Alice?", width=5.9)
        ponder.move_to([col_x, -0.95, 0])

        with self.voiceover(SAY[2]) as vo:
            self.play(TransformFromCopy(new_answer, diff[0]), TransformFromCopy(old_answer, diff[2]),
                      FadeIn(diff[1]), run_time=1.0)
            self.play(Write(diff[3:]), run_time=0.6)
            self.play(FadeIn(tag, shift=UP * 0.2), run_time=0.6)
            arrow = CurvedArrow(tag.get_left() + LEFT * 0.1, alice.get_right() + RIGHT * 0.12,
                                angle=-0.6, color=ALICE, stroke_width=4, tip_length=0.2)
            self.play(Create(arrow), run_time=0.8)
            self.play(Flash(alice, color=S.RED, flash_radius=0.4), run_time=0.6)
            vo.wait_until("without seeing")
            self.play(Circumscribe(VGroup(old_answer, new_answer), color=S.WHITE), run_time=1.2)
            vo.wait_until("Before we go on")
            # clear the right-hand column; the two published numbers stay as the ponder's prompt
            self.play(FadeOut(VGroup(card, week, diff, tag, arrow)),
                      VGroup(icons, db_title, legend, alice_label).animate.set_opacity(0.35),
                      ReplacementTransform(old_answer, pair[0][0][0]),
                      ReplacementTransform(new_answer, pair[1][0][0]), run_time=1.0)
            self.play(FadeIn(pair[0][1]), FadeIn(pair[1][1]), run_time=0.5)
            vo.wait_until("Pause and ponder")
            self.play(FadeIn(ponder, scale=0.95), run_time=0.6)
            vo.wait_until("to the nearest ten")
            self.play(LaggedStart(*[FadeIn(VGroup(p[0][1], p[0][2]), shift=RIGHT * 0.2) for p in pair],
                                  lag_ratio=0.4), run_time=1.0)
            vo.wait_until("Pause the video")
            self.play(Indicate(ponder[1], color=S.YELLOW), run_time=1.0)
        drain(self, ponder, 10)                       # PONDER(10 s): silent timer

        # ---------------------------------------------------------- the rounding jump
        nl = NumberLine(x_range=[40, 50, 1], length=10.4, color=S.GREY, stroke_width=2,
                        include_ticks=True, tick_size=0.08).move_to(DOWN * 0.8)
        nl_labs = VGroup(*[S.text(str(v), 22, S.GREY).next_to(nl.n2p(v), DOWN, buff=0.18)
                           for v in range(40, 51)])
        cut = DashedLine(nl.n2p(44.5) + DOWN * 0.25, nl.n2p(44.5) + UP * 2.6, color=S.GREY,
                         stroke_width=2, dash_length=0.1)
        cut_lab = S.text("rounding cut", 22, S.GREY).next_to(cut, UP, buff=0.1)
        reg_y = nl.n2p(40)[1] + 1.55
        reg40 = VGroup(Line([nl.n2p(40)[0] + 0.05, reg_y, 0], [nl.n2p(44.5)[0] - 0.1, reg_y, 0],
                            color=S.GREY_DARK, stroke_width=3),
                       S.text("rounds to 40", 24, S.GREY))
        reg40[1].next_to(reg40[0], UP, buff=0.12)
        reg50 = VGroup(Line([nl.n2p(44.5)[0] + 0.1, reg_y, 0], [nl.n2p(50)[0] - 0.05, reg_y, 0],
                            color=S.GREY_DARK, stroke_width=3),
                       S.text("rounds to 50", 24, S.GREY))
        reg50[1].next_to(reg50[0], UP, buff=0.12)

        # same look as S05's return of this number line: x (BLUE) without Alice, x' (ORANGE) with her
        dot_a = Dot(nl.n2p(41), color=X_COLOR, radius=0.1)
        dot_b = Dot(nl.n2p(42), color=XP_COLOR, radius=0.1)

        def count_lab(world, v, side):
            """'x: 44' (or x') under the tick label of v, flush with its `side` edge, plus who it is."""
            tick = nl_labs[int(v) - 40]
            tex, col, who, who_col = ((r"x\!:\ ", X_COLOR, "without Alice", S.GREY) if world == "x"
                                      else (r"x'\!:\ ", XP_COLOR, "with Alice", ALICE))
            base = S.math(r"x\!:\ 0", size=32).next_to(tick, DOWN, buff=0.22)     # common baseline
            m = S.math(tex + str(v), size=32, color=col).align_to(base, DOWN).align_to(tick, side)
            w = S.text(who, 22, who_col).next_to(m, DOWN, buff=0.12).align_to(m, side)
            return VGroup(m, w)

        lab_a, lab_b = count_lab("x", 41, RIGHT), count_lab("xp", 42, LEFT)
        arr44 = CurvedArrow(nl.n2p(44) + UP * 0.18, nl.n2p(40) + UP * 0.18 + RIGHT * 0.12, angle=PI / 3,
                            color=X_COLOR, stroke_width=4, tip_length=0.2)
        arr45 = CurvedArrow(nl.n2p(45) + UP * 0.18, nl.n2p(50) + UP * 0.18 + LEFT * 0.12, angle=-PI / 3,
                            color=XP_COLOR, stroke_width=4, tip_length=0.2)
        exposed = S.text("Alice exposed", 30, S.RED).next_to(nl.n2p(50), UP, buff=2.25).shift(LEFT * 0.6)
        jump = S.text("jump", 26, S.RED).next_to(cut, UP, buff=0.1)
        rule_cap = S.text("Any fixed rule that ever changes its answer has a jump somewhere.", 28, S.WHITE)
        rule_cap.to_edge(DOWN, buff=0.45)
        same = VGroup(*[S.math("40", size=60, color=S.WHITE).move_to(p[0][2], aligned_edge=LEFT) for p in pair])
        check = S.text("same answer", 26, S.GREEN).next_to(pair, DOWN, buff=0.3)

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(ponder), Transform(pair[0][0][2], same[0]), Transform(pair[1][0][2], same[1]),
                      run_time=0.6)
            self.play(FadeIn(check, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("But if the count")
            self.play(FadeOut(VGroup(icons, db_title, legend, alice_label, pair, check)),
                      Create(nl), FadeIn(nl_labs), FadeIn(dot_a), FadeIn(dot_b), FadeIn(lab_a),
                      FadeIn(lab_b), run_time=1.0)
            self.play(Create(cut), FadeIn(cut_lab), FadeIn(reg40), FadeIn(reg50), run_time=0.6)
            vo.wait_until("forty-four to forty-five")
            # Alice's arrival now straddles the cut: 44 without her, 45 with her
            self.play(dot_a.animate.move_to(nl.n2p(44)), dot_b.animate.move_to(nl.n2p(45)),
                      Transform(lab_a, count_lab("x", 44, RIGHT)), Transform(lab_b, count_lab("xp", 45, LEFT)),
                      run_time=1.0)
            vo.wait_until("the rounded answer jumps")
            self.play(Create(arr44), Indicate(nl_labs[0], color=S.WHITE, scale_factor=1.6), run_time=0.8)
            self.play(Create(arr45), Indicate(nl_labs[10], color=S.RED, scale_factor=1.6), run_time=0.8)
            nl_labs[10].set_color(S.RED)
            vo.wait_until("and Alice is exposed")
            self.play(Flash(nl.n2p(50) + UP * 0.05, color=S.RED, flash_radius=0.45),
                      FadeIn(exposed, shift=DOWN * 0.15), run_time=0.8)
            vo.wait_until("Any fixed rule")
            self.play(FadeOut(cut_lab), cut.animate.set_color(S.RED), FadeIn(jump, shift=DOWN * 0.1),
                      run_time=0.7)
            self.play(FadeIn(rule_cap, shift=UP * 0.2), run_time=0.8)
            self.play(Indicate(jump, color=S.RED, scale_factor=1.3), run_time=vo.remaining(0.6))

        # ---------------------------------------------------------- the questions
        qmark = S.text("?", 160, S.YELLOW).shift(UP * 1.2)
        q1 = S.text("What makes a statistic private?", 38, S.WHITE)
        q2 = S.text("How much noise is enough?", 38, S.WHITE)
        qs = VGroup(q1, q2).arrange(DOWN, buff=0.35).next_to(qmark, DOWN, buff=0.4)
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(Group(*self.mobjects)), run_time=0.7)
            self.play(FadeIn(qmark, scale=0.5), run_time=0.6)
            vo.wait_until("to be private")
            self.play(FadeIn(q1, shift=UP * 0.2), run_time=0.7)
            vo.wait_until("And if the fix")
            self.play(FadeIn(q2, shift=UP * 0.2), run_time=0.7)
            vo.wait_until("how much is enough")
            self.play(Indicate(q2, color=S.WHITE, scale_factor=1.05), run_time=vo.remaining(0.6))

        # ---------------------------------------------------------- the paper
        img, frame = paper_page(PAPER_P1, height=7.2)
        page = Group(img, frame).to_edge(LEFT, buff=0.7).shift(DOWN * 0.15)
        w, h = img.width, img.height
        ul = img.get_corner(UL)
        title_box = Rectangle(width=w * 0.80, height=h * 0.062, color=S.YELLOW, stroke_width=4)
        title_box.move_to(ul + RIGHT * w * 0.5 + DOWN * h * 0.0995)
        authors = S.text("Dwork · McSherry · Nissim · Smith", 32, S.WHITE)
        venue = S.text("TCC 2006", 28, S.GREY)
        prize = S.text("Gödel Prize 2017", 30, S.YELLOW)
        info = VGroup(authors, venue, prize).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        info.next_to(page, RIGHT, buff=0.6).shift(UP * 0.6)
        if info.get_right()[0] > 6.6:
            info.scale_to_fit_width(6.6 - info.get_left()[0])
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(qmark, qs)), FadeIn(page, shift=RIGHT * 0.5), run_time=1.0)
            vo.wait_until("Cynthia Dwork")
            self.play(FadeIn(authors, shift=LEFT * 0.2), run_time=0.8)
            vo.wait_until("Calibrating Noise")
            self.play(Create(title_box), FadeIn(venue), run_time=0.9)
            vo.wait_until("It founded")
            self.play(Indicate(title_box, color=S.YELLOW, scale_factor=1.03), run_time=1.0)
            vo.wait_until("and in 2017")
            self.play(FadeIn(prize, scale=1.2), run_time=0.7)

        # ---------------------------------------------------------- the roadmap
        ideas = [
            ("1", "A definition of privacy", S.YELLOW),
            ("2", "Sensitivity", S.GREEN),
            ("3", "The Laplace mechanism", S.RED),
            ("4", "Why one published table falls short", S.GREY),
        ]
        cards = VGroup()
        for num, label, col in ideas:
            badge = Circle(radius=0.32, color=col, stroke_width=3).set_fill(col, 0.15)
            n = S.text(num, 28, col).move_to(badge)
            lab = S.text(label, 32, S.WHITE).next_to(badge, RIGHT, buff=0.35)
            cards.add(VGroup(badge, n, lab))
        cards.arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(ORIGIN)
        tent = FunctionGraph(lambda t: 0.45 * np.exp(-abs(t) * 3.0), x_range=[-0.9, 0.9, 0.01],
                             color=S.RED, stroke_width=4)
        heading = S.text("In this video", 30, S.GREY).to_edge(UP, buff=0.8)
        cards.next_to(heading, DOWN, buff=0.7)
        tent.next_to(cards[2], RIGHT, buff=0.4)
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(Group(page, title_box, info)), run_time=0.8)
            self.play(FadeIn(heading, shift=DOWN * 0.2), run_time=0.6)
            anchors = ["a definition of privacy", "a number called sensitivity",
                       "a recipe for", "Plus a surprising limit"]
            for card_i, phrase in zip(cards, anchors):
                vo.wait_until(phrase)
                self.play(FadeIn(card_i, shift=RIGHT * 0.3), run_time=0.6)
                if card_i is cards[2]:
                    self.play(Create(tent), run_time=0.5)
            vo.wait_until("if it must be private")
            self.play(Indicate(cards[3][2], color=S.WHITE, scale_factor=1.04), run_time=vo.remaining(0.6))
        self.wait(0.4)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
