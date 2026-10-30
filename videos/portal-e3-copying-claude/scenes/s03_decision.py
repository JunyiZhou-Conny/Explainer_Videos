"""S03 · Why copy?

1. Decision 0006's title and status; its three options as cards.
2. Ponder: why copy one product instead of the best parts of several?
3. Option 2 as a collage whose seams clash (0006: 「风格容易打架，也说不清每个决定从哪来」); option 3's reason
   (「能用最少的设计判断得到一个不难看、不出错的结果」); Jakob's law (NN/g, 2000); the rule and the table row.
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (BUBBLE, CHECKED_C, DANGER_C, FIELD, NARRATION, TERRA, USER_C, chip, clear, mark_bad, mark_ok,
                    ponder_zh, quote_panel, sans, serif, zh)

SAY = NARRATION["S03"]


def option_card(n: str, title: str, note: str, width: float = 4.0) -> VGroup:
    head = VGroup(serif(n, 34, USER_C), sans(title, 24)).arrange(RIGHT, buff=0.25)
    sub = sans(note, 20, S.GREY)
    body = VGroup(head, sub).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    frame = RoundedRectangle(width=width, height=body.height + 0.5, corner_radius=0.15, stroke_color=S.GREY_DARK,
                             stroke_width=2)
    body.move_to(frame).align_to(frame, LEFT).shift(RIGHT * 0.25)
    g = VGroup(frame, body)
    g.frame = frame
    return g


def fragment(fill: str, stroke: str, radius: float, key: str, key_r: float) -> VGroup:
    """A composer fragment in some other product's style: its own corners, colours and send key."""
    box = RoundedRectangle(width=2.6, height=0.9, corner_radius=radius, stroke_color=stroke, stroke_width=2
                           ).set_fill(fill, 1)
    k = RoundedRectangle(width=0.36, height=0.36, corner_radius=key_r, stroke_width=0).set_fill(key, 1)
    k.move_to(box.get_corner(DR) + LEFT * 0.3 + UP * 0.3)
    return VGroup(box, k)


class Decision(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- three options
        with self.voiceover(SAY[0]) as vo:
            ask = quote_panel("照着一个固定的参考（Claude App 的聊天界面）一比一地做，不混搭别的风格", "issue #40 · 01:45, your request",
                              width=11.0, size=26, color=USER_C).move_to(UP * 2.6)
            vo.wait_until("You asked")
            self.play(FadeIn(ask, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("decision six")
            head = VGroup(zh("0006：界面先朴素，每个界面只照抄一个参考；分诊聊天页照 Claude App 做", 26),
                          VGroup(sans("owner: Junyi", 20, S.GREY), chip("提议 · proposed", USER_C, 22, mono_font=False)
                                 ).arrange(RIGHT, buff=0.3)).arrange(DOWN, buff=0.15).move_to(UP * 2.75)
            self.play(FadeOut(ask), FadeIn(head, shift=DOWN * 0.1), run_time=0.6)
            cards = VGroup(option_card("1", "our own style", "no references: ordinary, redone"),
                           option_card("2", "best parts of several", "a little from each"),
                           option_card("3", "one mature app, exactly", "copied one to one, no mixing")
                           ).arrange(RIGHT, buff=0.3).move_to(UP * 1.2)
            for c, phrase in zip(cards, ["Invent our own style", "Take the best parts", "Or copy one mature app"]):
                vo.wait_until(phrase)
                self.play(FadeIn(c, shift=UP * 0.1), run_time=0.45)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- ponder
        with self.voiceover(SAY[1]) as vo:
            self.play(*[m.animate.set_opacity(0.15) for m in self.mobjects], run_time=0.4)
            card = ponder_zh(self, "Why would copying one product beat picking the best parts of several?",
                             "为什么照抄一个产品，比从几个产品里各取所长更好？", seconds=4.0)
        self.wait(3.5)

        # 3 ---------------------------------------------------------------- seams, and the rule
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(card), *[m.animate.set_opacity(1) for m in self.mobjects if m is not card], run_time=0.4)
            self.play(cards[0].animate.set_opacity(0.3), cards[2].animate.set_opacity(0.3), run_time=0.3)
            frags = VGroup(fragment(FIELD, "#D9D6CC", 0.22, TERRA, 0.08), fragment("#ECEFF8", "#5B7FDB", 0.04, "#5B7FDB", 0.18),
                           fragment(BUBBLE, "#222222", 0.45, "#8E6CC9", 0.0)).arrange(RIGHT, buff=0.0).move_to(DOWN * 1.0)
            self.play(LaggedStart(*[FadeIn(f, shift=UP * 0.1) for f in frags], lag_ratio=0.2), run_time=0.8)
            vo.wait_until("The seams show")
            seams = VGroup(*[Line(frags[i].get_corner(UR) + UP * 0.1, frags[i].get_corner(DR) + DOWN * 0.1,
                                  color=DANGER_C, stroke_width=5) for i in (0, 1)])
            self.play(Create(seams), rate_func=there_and_back_with_pause, run_time=0.9)
            self.add(seams)
            vo.wait_until("a second cost")
            q1 = quote_panel("风格容易打架，也说不清每个决定从哪来。", "decision 0006 · option 2", width=9.4, size=28)
            q1.move_to(DOWN * 2.6)
            self.play(FadeIn(q1, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("One mature reference")
            self.play(FadeOut(VGroup(frags, seams, q1)), cards[1].animate.set_opacity(0.3),
                      cards[2].animate.set_opacity(1), run_time=0.5)
            tick = mark_ok(0.4, CHECKED_C).next_to(cards[2].frame, UP, buff=0.1).align_to(cards[2].frame, RIGHT)
            q2 = quote_panel("照抄一个成熟的界面，能用最少的设计判断得到一个不难看、不出错的结果。", "decision 0006 · reasons",
                             width=9.6, size=28).move_to(DOWN * 1.0)
            self.play(FadeIn(tick, scale=1.3), FadeIn(q2, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("Jakob's law")
            self.play(FadeOut(q2), run_time=0.3)
            jl = quote_panel("Users spend most of their time on other sites. This means that users prefer your site to "
                             "work the same way as all the other sites they already know.",
                             "Jakob's law · Jakob Nielsen, NN/g, 2000", width=11.0, size=26, color=USER_C)
            jl.move_to(DOWN * 1.4)
            self.play(FadeIn(jl, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("The rule, now written down")
            self.play(FadeOut(jl), run_time=0.4)
            rule = VGroup(zh("每个界面只照抄一个参考", 32, USER_C),
                          zh("分诊聊天页 ← Claude App", 30)).arrange(DOWN, buff=0.3).move_to(DOWN * 1.6)
            src = sans("docs/design/README.md · decision 0006", 20, S.GREY).next_to(rule, DOWN, buff=0.2)
            self.play(FadeIn(rule[0]), run_time=0.4)
            vo.wait_until("For the chat page")
            self.play(FadeIn(rule[1]), FadeIn(src), run_time=0.5)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(0.6)
        clear(self)
