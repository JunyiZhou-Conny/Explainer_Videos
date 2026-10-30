"""S06 · What we added (docs/design/README.md, 「因为产品和安全而加的」)

1. Ponder over a map: the student in Boston, the parent in China.
2. For parents: the fine print's two endings (TriageChatPage.tsx:848–851); a phone number for a student and
   for a parent, 「+1 …（从中国拨打）」; 911 for a parent, 「（请孩子或身边的人在当地拨打）」, no link
   (answerBlocks.ts:69–77).
3. For everyone: 「现在就做」 first and at once, role=alert (TriageAnswer.tsx:61–64); 「紧急情况」 in the top bar;
   「模拟」 tags; 「复制给家长」 appends 「（AI 分诊原型生成，不是诊断；模拟）」 (answerBlocks.ts:99).
4. Accessibility: hidden headings 「你说」「回答」「回答（紧急）」; source links one per line, at least 24 px
   (WCAG 2.2 2.5.8); 「紧急情况」 in view at 400 % zoom.
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (CREAM, DANGER_C, FAINT, INK, NARRATION, OURS_C, SAFETY_RED, USER_C, chip, clear, page_frame,
                    pill, ponder_zh, sans, serif_zh, zh)

SAY = NARRATION["S06"]


def on_paper(mobs: VGroup, pad: float = 0.3, width: float | None = None) -> VGroup:
    """Put product strings on a cream strip, as they appear on the page."""
    w = width or mobs.width + 2 * pad
    bg = RoundedRectangle(width=w, height=mobs.height + 2 * pad, corner_radius=0.14, stroke_width=0).set_fill(CREAM, 1)
    mobs.move_to(bg).align_to(bg, LEFT).shift(RIGHT * pad)
    return VGroup(bg, mobs)


class Added(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- ponder: a parent in China
        with self.voiceover(SAY[0]) as vo:
            boston = VGroup(Dot(LEFT * 4.2 + DOWN * 0.3, radius=0.12, color=OURS_C),
                            sans("student · Boston", 24, OURS_C))
            boston[1].next_to(boston[0], DOWN, buff=0.15)
            china = VGroup(Dot(RIGHT * 4.2 + UP * 0.2, radius=0.12, color=USER_C), sans("parent · China", 24, USER_C))
            china[1].next_to(china[0], DOWN, buff=0.15)
            arc = ArcBetweenPoints(boston[0].get_center(), china[0].get_center(), angle=-PI / 3, color=S.GREY,
                                   stroke_width=2)
            self.play(FadeIn(boston), FadeIn(china), Create(arc), run_time=0.9)
            vo.wait_until("What do they need")
            card = ponder_zh(self, "What does a parent in China need from this page that the student doesn't?",
                             "在中国的家长，需要这个页面给他什么，是在波士顿的学生不需要的？", seconds=4.0)
        self.wait(3.5)

        # 2 ---------------------------------------------------------------- 911 from China
        with self.voiceover(SAY[1]) as vo:
            clear(self, 0.4)
            hs = VGroup(sans("student", 24, OURS_C), sans("parent", 24, USER_C)).arrange(RIGHT, buff=5.2).move_to(UP * 3.1)
            self.play(FadeIn(hs), run_time=0.3)
            vo.wait_until("can't dial it from China")
            s_fp = on_paper(VGroup(zh("…危及生命直接打 911", 24, FAINT)), width=5.6)
            p_fp = on_paper(VGroup(zh("…危及生命请孩子或身边的人在当地打 911", 24, FAINT)), width=6.6)
            row1 = VGroup(s_fp, p_fp).arrange(RIGHT, buff=0.4).move_to(UP * 2.0)
            lab1 = sans("the fine print", 20, S.GREY).next_to(row1, UP, buff=0.1).align_to(row1, LEFT)
            self.play(FadeIn(s_fp), FadeIn(lab1), run_time=0.4)
            vo.wait_until("every fixed line")
            self.play(FadeIn(p_fp, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("a plus one")
            s_ph = on_paper(VGroup(VGroup(zh("617-353-3575", 24, INK), sans("tap to dial", 20, OURS_C)
                                          ).arrange(RIGHT, buff=0.3)), width=5.6)
            p_ph = on_paper(VGroup(VGroup(zh("+1 617-353-3575（从中国拨打）", 24, INK), sans("tap to dial", 20, OURS_C)
                                          ).arrange(RIGHT, buff=0.25)), width=6.6)
            row2 = VGroup(s_ph, p_ph).arrange(RIGHT, buff=0.4).move_to(UP * 0.3)
            lab2 = sans("a phone number in an answer", 20, S.GREY).next_to(row2, UP, buff=0.1).align_to(row2, LEFT)
            self.play(FadeIn(s_ph), FadeIn(lab2), FadeIn(p_ph, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("Emergency and crisis numbers")
            s_911 = on_paper(VGroup(VGroup(zh("911", 24, INK), sans("tap to dial", 20, OURS_C)).arrange(RIGHT, buff=0.3)),
                             width=5.6)
            p_911 = on_paper(VGroup(zh("911（请孩子或身边的人在当地拨打）", 24, INK)), width=6.6)
            row3 = VGroup(s_911, p_911).arrange(RIGHT, buff=0.4).move_to(DOWN * 1.4)
            lab3 = sans("911, 988, crisis lines: no dial link for parents", 20, S.GREY).next_to(row3, UP, buff=0.1
                                                                                                ).align_to(row3, LEFT)
            self.play(FadeIn(s_911), FadeIn(lab3), FadeIn(p_911, shift=LEFT * 0.1), run_time=0.6)
            src = sans("TriageChatPage.tsx:848–851 · answerBlocks.ts:69–77 · the number: BU SHS, demo 01", 20, S.GREY)
            src.move_to(DOWN * 3.0)
            self.play(FadeIn(src), run_time=0.3)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 3 ---------------------------------------------------------------- for everyone
        with self.voiceover(SAY[2]) as vo:
            clear(self, 0.4)
            block = VGroup(serif_zh("现在就做", 30, SAFETY_RED),
                           Rectangle(width=4.2, height=0.12, stroke_width=0).set_fill(INK, 0.5),
                           Rectangle(width=3.4, height=0.12, stroke_width=0).set_fill(INK, 0.5)
                           ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            frame = RoundedRectangle(width=5.0, height=block.height + 0.5, corner_radius=0.12, stroke_color=SAFETY_RED,
                                     stroke_width=4).set_fill(CREAM, 1)
            block.move_to(frame).align_to(frame, LEFT).shift(RIGHT * 0.3)
            emerg = VGroup(frame, block).move_to(LEFT * 3.4 + UP * 1.9)
            notes = VGroup(sans("first · at once · no animation", 22, S.GREY),
                           sans('read aloud: role="alert"', 22, S.GREY)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            notes.next_to(emerg, DOWN, buff=0.15).align_to(emerg, LEFT)
            vo.wait_until("a red do-this-now block")
            self.play(Create(frame), FadeIn(block), run_time=0.6)
            vo.wait_until("read aloud")
            self.play(FadeIn(notes), run_time=0.4)
            vo.wait_until("in the top bar")
            bar = on_paper(VGroup(VGroup(zh("AI 分诊", 22, INK), pill("原型", 20, FAINT), zh("紧急情况", 22, SAFETY_RED)
                                         ).arrange(RIGHT, buff=0.4)))
            bar.move_to(RIGHT * 3.4 + UP * 2.3)
            always = sans("always there", 22, S.GREY).next_to(bar, DOWN, buff=0.12)
            self.play(FadeIn(bar), FadeIn(always), run_time=0.5)
            vo.wait_until("labelled simulated")
            tags = VGroup(pill("模拟", 22, FAINT), pill("模拟估算", 22, FAINT), pill("演示回放（模拟）", 22, FAINT)
                          ).arrange(RIGHT, buff=0.2).move_to(LEFT * 3.0 + DOWN * 1.2)
            self.play(LaggedStart(*[FadeIn(t) for t in tags], lag_ratio=0.2), run_time=0.6)
            vo.wait_until("the label goes with it")
            copy = VGroup(sans("for students:", 22, S.GREY), pill("复制给家长", 24, INK), Arrow(LEFT * 0.4, RIGHT * 0.4, color=S.GREY, buff=0),
                          on_paper(VGroup(zh("……（AI 分诊原型生成，不是诊断；模拟）", 22, INK)))).arrange(RIGHT, buff=0.25)
            copy.move_to(DOWN * 2.6)
            self.play(FadeIn(copy, shift=UP * 0.1), run_time=0.6)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 4 ---------------------------------------------------------------- accessibility
        with self.voiceover(SAY[3]) as vo:
            clear(self, 0.4)
            heads = VGroup(*[VGroup(sans("h2", 20, OURS_C), zh(t, 24)).arrange(RIGHT, buff=0.2)
                             for t in ["你说", "回答", "你说", "回答（紧急）"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
            heads.move_to(LEFT * 4.4 + UP * 0.6)
            h_lab = sans("hidden headings: jump turn by turn", 22, S.GREY).next_to(heads, DOWN, buff=0.35).align_to(heads, LEFT)
            vo.wait_until("hidden headings")
            self.play(LaggedStart(*[FadeIn(h, shift=RIGHT * 0.1) for h in heads], lag_ratio=0.2), FadeIn(h_lab), run_time=0.8)
            vo.wait_until("24 pixels")
            links = VGroup(*[RoundedRectangle(width=2.6, height=0.42, corner_radius=0.06, stroke_color=OURS_C,
                                              stroke_width=2) for _ in range(3)]).arrange(DOWN, buff=0.12)
            links.move_to(UP * 0.6)
            brace = Brace(links[0], RIGHT, color=USER_C, buff=0.08)
            px = sans("≥ 24 px", 22, USER_C).next_to(brace, RIGHT, buff=0.1)
            l_lab = sans("source links, one per line", 22, S.GREY).next_to(links, DOWN, buff=0.35)
            wcag = sans("WCAG 2.2 · 2.5.8 target size", 20, S.GREY).next_to(l_lab, DOWN, buff=0.1)
            self.play(FadeIn(links), GrowFromCenter(brace), FadeIn(px), FadeIn(l_lab), FadeIn(wcag), run_time=0.7)
            vo.wait_until("400 percent")
            big = page_frame(3.2, 3.0).move_to(RIGHT * 4.5 + UP * 0.6)
            em = zh("紧急情况", 40, SAFETY_RED).move_to(big.get_top() + DOWN * 0.55)
            z = sans("400 %", 30, USER_C).next_to(big, UP, buff=0.12)
            z_lab = VGroup(sans("opens at the top:", 22, S.GREY), sans("emergency link in view", 22, S.GREY)).arrange(DOWN, buff=0.06)
            z_lab.next_to(big, DOWN, buff=0.25)
            self.play(FadeIn(big), FadeIn(em, scale=0.5), FadeIn(z), FadeIn(z_lab), run_time=0.7)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(0.6)
        clear(self)
