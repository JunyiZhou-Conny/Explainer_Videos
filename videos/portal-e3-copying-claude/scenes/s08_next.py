"""S08 · What else

1. What mainstream chat apps have and we don't (Claude Help Center; OpenAI; as of 2026-10-30): chat history and
   projects · file uploads · voice · a side panel for documents and code · memory across chats.
2. What only we could build: one answer for two readers · a card the student sends home · a hand-off to booking.
3. Waiting for the owner: decision 0006 (提议); a stopped message is sent with the next one; no dial link for
   crisis lines for parents (PR #41 handoff, next steps 2 and 5).
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import NARRATION, USER_C, chip, clear, sans, zh

SAY = NARRATION["S08"]


def card(title: str, lines: list[str], color: str, width: float = 4.0) -> VGroup:
    body = VGroup(sans(title, 26, color), *[sans(t, 22, S.GREY) for t in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    frame = RoundedRectangle(width=width, height=body.height + 0.5, corner_radius=0.15, stroke_color=color, stroke_width=2)
    body.move_to(frame).align_to(frame, LEFT).shift(RIGHT * 0.25)
    return VGroup(frame, body)


class Next(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- what they have
        with self.voiceover(SAY[0]) as vo:
            head = sans("mainstream chat apps have · we don't", 28, S.GREY).move_to(UP * 3.1)
            self.play(FadeIn(head), run_time=0.4)
            items = [("chat history · projects", "history and projects"), ("file uploads", "file uploads"),
                     ("voice", "voice"), ("a side panel for documents and code", "a side panel"),
                     ("memory across chats", "memory across chats")]
            chips = VGroup(*[chip(t, S.GREY, 26, mono_font=False) for t, _ in items])
            chips.arrange_in_grid(2, 3, buff=(0.35, 0.35)).move_to(UP * 1.6)
            for c, (_, phrase) in zip(chips, items):
                vo.wait_until(phrase)
                self.play(FadeIn(c, shift=UP * 0.1), run_time=0.3)
            src = sans("Claude Help Center · OpenAI help and announcements · as of 2026-10-30", 20, S.GREY)
            src.next_to(chips, DOWN, buff=0.3)
            vo.wait_until("accounts and storage")
            need = sans("most of them need accounts and storage", 26, USER_C).next_to(src, DOWN, buff=0.3)
            self.play(FadeIn(src), FadeIn(need), run_time=0.5)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- what only we could build
        with self.voiceover(SAY[1]) as vo:
            clear(self, 0.4)
            head2 = sans("what only this product could build", 28, USER_C).move_to(UP * 3.1)
            self.play(FadeIn(head2), run_time=0.3)
            ideas = VGroup(card("one answer for two readers", ["student and parent side by side; the folded 「给家长的摘要」 is the seed"],
                                USER_C, width=11.0),
                           card("a card the student sends home", ["「复制给家长」 is the first step"], USER_C, width=11.0),
                           card("a hand-off to booking", ["the answer already writes the English to say (「可以这样说」);",
                                                          "the page could place the call or fill in the form"], USER_C, width=11.0)
                           ).arrange(DOWN, buff=0.25).move_to(DOWN * 0.1)
            for c, phrase in zip(ideas, ["One answer for two readers", "A summary card", "a hand-off to booking"]):
                vo.wait_until(phrase)
                self.play(FadeIn(c, shift=UP * 0.1), run_time=0.45)
            tag = sans("ideas, not built", 20, S.GREY).next_to(ideas, DOWN, buff=0.15)
            self.play(FadeIn(tag), run_time=0.3)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 3 ---------------------------------------------------------------- waiting for you
        with self.voiceover(SAY[2]) as vo:
            clear(self, 0.4)
            head = VGroup(zh("等你决定", 36, USER_C), sans("waiting for you", 24, S.GREY)).arrange(RIGHT, buff=0.3).move_to(UP * 2.4)
            self.play(FadeIn(head), run_time=0.4)
            dozen = sans("12 open items in PR #41's handoff, among them:", 24, S.GREY).move_to(UP * 1.5)
            vo.wait_until("a dozen open items")
            self.play(FadeIn(dozen), run_time=0.3)
            rows = VGroup(VGroup(chip("decision 0006 and its addendum", USER_C, 26, mono_font=False), zh("提议", 26, USER_C),
                                 sans("progress-only streaming · model menu · retry", 20, S.GREY)),
                          VGroup(chip("a stopped message is sent with your next one", S.GREY, 26, mono_font=False),
                                 sans("chosen unattended", 22, S.GREY)),
                          VGroup(chip("parents: no dial link for crisis lines", S.GREY, 26, mono_font=False),
                                 sans("chosen unattended", 22, S.GREY)))
            for r in rows:
                r.arrange(RIGHT, buff=0.3)
            rows.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(DOWN * 0.4)
            for r, phrase in zip(rows, ["still a proposal", "a stopped message", "no dial link"]):
                vo.wait_until(phrase)
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.4)
            src = sans("decision 0006 · PR #41 handoff, next steps 2 and 5", 20, S.GREY).next_to(rows, DOWN, buff=0.4)
            self.play(FadeIn(src), run_time=0.3)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(0.6)
        clear(self)
