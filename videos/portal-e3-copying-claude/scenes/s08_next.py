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

from common import (CREAM, FAINT, INK, INK2, NARRATION, OURS_C, USER_C, chip, clear, page_frame, sans, serif_zh, zh,
                    zh_wrap)

# demo 01's folded parent summary (parentSummaryZh) and demo 03's English line (sayEn), recordings.json
PARENT_SUMMARY = ("你家孩子喉咙痛了两天，吞咽时特别疼，今天体温 38.5°C，应今天打电话联系 BU 学生健康中心，争取当天评估。"
                  "你可以提醒孩子尽快打电话；如果出现呼吸困难或连口水都咽不下，请孩子立即在当地寻求紧急帮助。")
SAY_EN = ["I twisted my right ankle playing basketball. It is very swollen,", "and I can barely put weight on it."]

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
            VGroup(VGroup(*chips[:3]).arrange(RIGHT, buff=0.35), VGroup(*chips[3:]).arrange(RIGHT, buff=0.35)
                   ).arrange(DOWN, buff=0.35).move_to(UP * 1.6)
            for c, (_, phrase) in zip(chips, items):
                vo.wait_until(phrase)
                self.play(FadeIn(c, shift=UP * 0.1), run_time=0.3)
            src = sans("Claude Help Center · OpenAI help and announcements · as of 2026-10-30", 20, S.GREY)
            src.next_to(chips, DOWN, buff=0.3)
            vo.wait_until("accounts and storage")
            need = sans("most of them need accounts and storage", 26, USER_C).next_to(src, DOWN, buff=0.3)
            self.play(FadeIn(src), FadeIn(need), run_time=0.5)
            vo.wait_until("voice may matter most")
            self.play(Circumscribe(chips[2], color=USER_C, buff=0.06), run_time=0.6)
            v1 = sans("voice: a worried parent may rather speak than type", 22, S.GREY)
            v2 = sans("history, memory: storing health conversations needs a privacy decision first", 22, S.GREY)
            verdict = VGroup(v1, v2).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(need, DOWN, buff=0.3)
            self.play(FadeIn(v1), run_time=0.4)
            vo.wait_until("history and memory would mean")
            self.play(FadeIn(v2), run_time=0.4)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- what only we could build (drawn)
        with self.voiceover(SAY[1]) as vo:
            clear(self, 0.4)
            head2 = sans("what only this product could build · ideas, not built", 26, USER_C).move_to(UP * 3.25)
            self.play(FadeIn(head2), run_time=0.3)
            vo.wait_until("One answer for two readers")
            # a split answer: the student's version | the parent's version, the parent summary opened
            left = page_frame(4.6, 4.2).move_to(LEFT * 4.25 + UP * 0.7)
            right = page_frame(4.6, 4.2).move_to(RIGHT * 0.45 + UP * 0.7)
            lt = VGroup(zh("学生", 22, OURS_C), serif_zh("1. 今天打电话联系", 20, INK), serif_zh("    BU 学生健康中心", 20, INK),
                        *[Rectangle(width=w, height=0.09, stroke_width=0).set_fill(INK2, 0.5) for w in (3.6, 3.0, 3.3)]
                        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
            lt.align_to(left, UP).align_to(left, LEFT).shift(DOWN * 0.3 + RIGHT * 0.25)
            summary = zh_wrap(PARENT_SUMMARY, 4.1, 20, INK)
            rt = VGroup(zh("家长", 22, USER_C), zh("给家长的摘要", 22, INK2), summary).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
            rt.align_to(right, UP).align_to(right, LEFT).shift(DOWN * 0.3 + RIGHT * 0.25)
            if rt.height > 3.8:
                summary = zh_wrap(PARENT_SUMMARY, 4.2, 20, INK, buff=0.04)
                rt = VGroup(rt[0], rt[1], summary).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
                rt.align_to(right, UP).align_to(right, LEFT).shift(DOWN * 0.2 + RIGHT * 0.2)
            seed = sans("today: folded under every answer (demo 01's text)", 20, S.GREY).next_to(VGroup(left, right), DOWN, buff=0.15)
            self.play(FadeIn(left), FadeIn(lt), FadeIn(right), FadeIn(rt[:2]), run_time=0.6)
            vo.wait_until("a folded summary for parents")
            self.play(FadeIn(rt[2], shift=DOWN * 0.1), FadeIn(seed), run_time=0.6)
            vo.wait_until("A summary card")
            phone = RoundedRectangle(width=2.5, height=3.2, corner_radius=0.25, stroke_color=S.GREY, stroke_width=2)
            phone.move_to(RIGHT * 5.0 + UP * 1.35)
            card = VGroup(zh("孩子发来的", 20, FAINT), zh("喉咙痛 · 今天", 20, INK), zh("打给 SHS", 20, INK),
                          zh("不是诊断 · 模拟", 20, FAINT)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            cbg = RoundedRectangle(width=2.2, height=card.height + 0.3, corner_radius=0.12, stroke_width=0).set_fill(CREAM, 1)
            card.move_to(cbg)
            cardg = VGroup(cbg, card).move_to(phone)
            arrow = CurvedArrow(right.get_right() + UP * 0.6, phone.get_left() + UP * 0.6, angle=-PI / 4, color=USER_C)
            cn = sans("parent · China", 20, USER_C).next_to(phone, DOWN, buff=0.1)
            self.play(Create(phone), Create(arrow), FadeIn(cardg, shift=LEFT * 0.2), FadeIn(cn), run_time=0.8)
            vo.wait_until("a hand-off to booking")
            say = VGroup(serif_zh("可以这样说：", 22, INK), sans(SAY_EN[0], 20, INK), sans(SAY_EN[1], 20, INK)
                         ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            sbg = RoundedRectangle(width=say.width + 0.5, height=say.height + 0.35, corner_radius=0.14, stroke_width=0
                                   ).set_fill(CREAM, 1)
            say.move_to(sbg)
            sayg = VGroup(sbg, say).move_to(LEFT * 2.2 + DOWN * 2.6)
            form = RoundedRectangle(width=2.6, height=1.1, corner_radius=0.12, stroke_color=OURS_C, stroke_width=2)
            form_lab = VGroup(sans("booking", 22, OURS_C), sans("call · or fill the form", 20, S.GREY)).arrange(DOWN, buff=0.06)
            form_lab.move_to(form)
            formg = VGroup(form, form_lab).move_to(RIGHT * 4.3 + DOWN * 2.6)
            link_a = Arrow(sayg.get_right(), formg.get_left(), color=OURS_C, buff=0.15, stroke_width=3)
            src = sans("demo 03's English line", 20, S.GREY).next_to(sayg, UP, buff=0.06).align_to(sayg, LEFT)
            self.play(FadeOut(seed), FadeIn(sayg), FadeIn(src), run_time=0.5)
            self.play(GrowArrow(link_a), FadeIn(formg), run_time=0.5)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 3 ---------------------------------------------------------------- waiting for you
        with self.voiceover(SAY[2]) as vo:
            clear(self, 0.4)
            head = VGroup(zh("等你决定", 36, USER_C), sans("waiting for you", 24, S.GREY)).arrange(RIGHT, buff=0.3).move_to(UP * 2.4)
            self.play(FadeIn(head), run_time=0.4)
            dozen = sans("12 open items in PR #41's handoff, among them:", 24, S.GREY).move_to(UP * 1.5)
            vo.wait_until("a dozen open items")
            self.play(FadeIn(dozen), run_time=0.3)
            rows = VGroup(VGroup(chip("decision 0006 + what the agent added that night", USER_C, 26, mono_font=False),
                                 zh("提议", 26, USER_C)),
                          VGroup(chip("a stopped message: not taken back, sent with your next", S.GREY, 26, mono_font=False),
                                 sans("chosen unattended", 22, S.GREY)),
                          VGroup(chip("parents: no dial link for crisis lines", S.GREY, 26, mono_font=False),
                                 sans("chosen unattended", 22, S.GREY)))
            for r in rows:
                r.arrange(RIGHT, buff=0.3)
            rows.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(DOWN * 0.4)
            for r, phrase in zip(rows, ["still a proposal", "a stopped message", "no dial link"]):
                vo.wait_until(phrase)
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.4)
            added = sans("added that night: progress-only streaming · the model menu · retry", 22, S.GREY)
            added.next_to(rows, DOWN, buff=0.3).align_to(rows, LEFT)
            src = sans("decision 0006 · PR #41 handoff, next steps 1, 2 and 5", 20, S.GREY).next_to(added, DOWN, buff=0.3)
            self.play(FadeIn(added), run_time=0.3)
            self.play(FadeIn(src), run_time=0.3)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(0.6)
        clear(self)
