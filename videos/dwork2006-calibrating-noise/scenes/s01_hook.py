"""S01 · The differencing attack (reference scene for the rest of the video)."""

from pathlib import Path

import numpy as np
from manim import *

from explainer import style as S
from explainer.components import highlight_box, paper_page, person_icon
from explainer.scene import VoiceScene

from common import ALICE, NARRATION, PAPER_P1, X_COLOR

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
            vo.wait_until("It just says")
            sick_icons = VGroup(*[patients[i] for i in sorted(sick)])
            self.play(LaggedStart(*[Indicate(p, color=ALICE, scale_factor=1.25) for p in sick_icons],
                                  lag_ratio=0.03), run_time=1.6)
            self.play(Write(answer), run_time=0.6)

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
            self.play(Indicate(card, color=S.WHITE, scale_factor=1.05), run_time=0.8)
            new_answer = S.text("42", 72, S.WHITE).move_to([card.get_center()[0] + 0.9, answers_y, 0])
            vo.wait_until("The answer is now")
            self.play(Write(new_answer), run_time=0.6)

        # ---------------------------------------------------------- the subtraction
        diff = S.math("42", "-", "41", "=", "1", size=60)
        diff[4].set_color(ALICE)
        diff.move_to([card.get_center()[0], answers_y - 1.15, 0])
        tag = S.text("Alice has condition X", 30, S.RED).next_to(diff, DOWN, buff=0.45)
        with self.voiceover(SAY[2]) as vo:
            self.play(TransformFromCopy(new_answer, diff[0]), TransformFromCopy(old_answer, diff[2]),
                      FadeIn(diff[1]), run_time=1.0)
            self.play(Write(diff[3:]), run_time=0.6)
            self.play(FadeIn(tag, shift=UP * 0.2), run_time=0.6)
            arrow = CurvedArrow(tag.get_left() + LEFT * 0.1, alice.get_right() + RIGHT * 0.12,
                                angle=-0.6, color=ALICE, stroke_width=4, tip_length=0.2)
            self.play(Create(arrow), run_time=0.8)
            self.play(Flash(alice, color=S.RED, flash_radius=0.4), run_time=0.6)
            vo.wait_until("No names")
            self.play(Circumscribe(VGroup(old_answer, new_answer), color=S.YELLOW), run_time=1.4)

        # ---------------------------------------------------------- the questions
        qmark = S.text("?", 160, S.YELLOW).shift(UP * 1.2)
        q1 = S.text("What makes a statistic private?", 38, S.WHITE)
        q2 = S.text("How much noise is enough?", 38, S.WHITE)
        qs = VGroup(q1, q2).arrange(DOWN, buff=0.35).next_to(qmark, DOWN, buff=0.4)
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
            self.play(FadeIn(qmark, scale=0.5), run_time=0.6)
            vo.wait_until("what would it even mean")
            self.play(FadeIn(q1, shift=UP * 0.2), run_time=0.7)
            vo.wait_until("And if the fix")
            self.play(FadeIn(q2, shift=UP * 0.2), run_time=0.7)

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
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(qmark, qs)), FadeIn(page, shift=RIGHT * 0.5), run_time=1.0)
            vo.wait_until("Cynthia Dwork")
            self.play(FadeIn(authors, shift=LEFT * 0.2), run_time=0.8)
            vo.wait_until("Calibrating Noise")
            self.play(Create(title_box), FadeIn(venue), run_time=0.9)
            vo.wait_until("and in 2017")
            self.play(FadeIn(prize, scale=1.2), run_time=0.7)

        # ---------------------------------------------------------- the roadmap
        ideas = [
            ("1", "A definition of privacy", S.YELLOW),
            ("2", "Sensitivity", S.GREEN),
            ("3", "The Laplace mechanism", S.RED),
            ("4", "A limit on one-shot releases", S.GREY),
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
        tent.next_to(cards[2], RIGHT, buff=0.4)
        heading = S.text("In this video", 30, S.GREY).to_edge(UP, buff=0.8)
        cards.next_to(heading, DOWN, buff=0.7)
        tent.next_to(cards[2], RIGHT, buff=0.4)
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(Group(page, title_box, info)), run_time=0.8)
            self.play(FadeIn(heading, shift=DOWN * 0.2), run_time=0.6)
            anchors = ["a definition of privacy", "a number called sensitivity",
                       "a recipe for exactly", "Plus a surprising limit"]
            for card_i, phrase in zip(cards, anchors):
                vo.wait_until(phrase)
                self.play(FadeIn(card_i, shift=RIGHT * 0.3), run_time=0.6)
                if card_i is cards[2]:
                    self.play(Create(tent), run_time=0.5)
        self.wait(0.6)
        self.play(FadeOut(VGroup(heading, cards, tent)), run_time=0.8)
