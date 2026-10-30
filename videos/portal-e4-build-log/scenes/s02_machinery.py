"""S02 · How the work is organised (docs/workflow.md, AGENTS.md, the handoff skill; ../SOURCES.md)

1. issue → branch → draft PR → pushes wake Bugbot (every push) and Codex (once the PR is ready for review); both
   comment only (AGENTS.md 「review bot（Cursor Bugbot、Codex 等）只提意见，不直接改代码。」).
2. A handoff note and a decision record, 「提议」 → 「已采纳」 by a person only; 「聊天是临时的，仓库是永久的」.
3. Two agent sessions on the clock (first to last commit); PR #41 stacked on PR #36, pulling it in 13 times.
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (M41, MODEL_C, NARRATION, OURS_C, USER_C, chip, clear, link, mono, quote_panel, sans, week_axis, zh)

SAY = NARRATION["S02"]


def step(name: str, sub: str | None, color, width: float = 2.4) -> VGroup:
    """A plain box: a name and an optional line under it."""
    rows = VGroup(mono(name, 24, S.WHITE), *([sans(sub, 20, S.GREY)] if sub else [])).arrange(DOWN, buff=0.08)
    frame = RoundedRectangle(width=max(width, rows.width + 0.4), height=rows.height + 0.4, corner_radius=0.14,
                             stroke_color=color, stroke_width=2.5)
    rows.move_to(frame)
    return VGroup(frame, rows)


class Machinery(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- issue → branch → PR → bots
        with self.voiceover(SAY[0]) as vo:
            chain = VGroup(step("issue", "one small job", S.WHITE), step("branch", "its own", S.WHITE),
                           step("draft PR", "after the first commit", OURS_C, 2.9)).arrange(RIGHT, buff=0.7)
            chain.move_to(UP * 2.0)
            arrows = VGroup(*[link(a, b, S.GREY) for a, b in zip(chain, chain[1:])])
            for box, phrase in zip(chain, ["starts as an issue", "its own branch", "a draft pull request"]):
                vo.wait_until(phrase)
                self.play(FadeIn(box, shift=UP * 0.1), *([Create(arrows[chain.submobjects.index(box) - 1])]
                                                        if box is not chain[0] else []), run_time=0.45)
            vo.wait_until("Pushes wake")
            bots = VGroup(step("Bugbot", "Cursor · every push", S.GREY, 2.3), step("Codex", "OpenAI · once ready", S.GREY, 2.3)
                          ).arrange(RIGHT, buff=0.5)
            bots.move_to(DOWN * 0.35)
            wake = link(chain[2], bots, S.GREY)
            wake_l = sans("pushes", 20, S.GREY).next_to(wake, RIGHT, buff=0.12)
            self.play(FadeIn(bots, shift=UP * 0.1), Create(wake), FadeIn(wake_l), run_time=0.6)
            vo.wait_until("They may comment")
            back = CurvedArrow(bots[1].get_right() + RIGHT * 0.1, chain[2].get_right() + RIGHT * 0.1 + DOWN * 0.1,
                               angle=PI / 2, color=S.GREY)
            note = VGroup(sans("comments only", 22, S.GREY), sans("·  never change code", 22, S.GREY)
                          ).arrange(RIGHT, buff=0.4).next_to(bots, DOWN, buff=0.3)
            self.play(Create(back), FadeIn(note), run_time=0.6)
            q = quote_panel("review bot（Cursor Bugbot、Codex 等）只提意见，不直接改代码。", "AGENTS.md", width=9.4, size=24)
            q.to_edge(DOWN, buff=0.45)
            self.play(FadeIn(q, shift=UP * 0.1), run_time=0.5)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- handoff notes, decision records
        with self.voiceover(SAY[1]) as vo:
            clear(self, 0.4)
            vo.wait_until("a handoff note")
            heads = VGroup(*[zh(t, 22) for t in ["交接（无人值守，未经人确认）", "做了什么", "没做完的", "下一步（等 Junyi 定）", "踩过的坑"]]
                           ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
            heads[0].set_color(USER_C)
            frame = SurroundingRectangle(heads, color=S.GREY_DARK, buff=0.3, corner_radius=0.14)
            hand = VGroup(frame, heads, sans("a handoff note, on the PR", 20, S.GREY).next_to(frame, DOWN, buff=0.12))
            hand.move_to(LEFT * 3.6 + UP * 0.6)
            self.play(FadeIn(hand, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("decision records")
            rec = VGroup(zh("决策记录", 26), VGroup(chip("提议", S.GREY, 24, mono_font=False), Arrow(LEFT * 0.4, RIGHT * 0.4, buff=0,
                                                                                               color=S.GREY),
                                                    chip("已采纳", USER_C, 24, mono_font=False)).arrange(RIGHT, buff=0.2),
                         sans("only a person marks it adopted", 22, USER_C)).arrange(DOWN, buff=0.25)
            rec.move_to(RIGHT * 3.4 + UP * 1.0)
            self.play(FadeIn(rec[0]), FadeIn(rec[1][0]), run_time=0.4)
            vo.wait_until("until a person marks")
            self.play(GrowArrow(rec[1][1]), FadeIn(rec[1][2]), FadeIn(rec[2]), run_time=0.6)
            vo.wait_until("chat is temporary")
            q = quote_panel("聊天是临时的，仓库是永久的。agent 读不到的信息，对团队来说就不存在。", "docs/workflow.md",
                            width=11.0, size=26, color=USER_C).to_edge(DOWN, buff=0.45)
            self.play(FadeIn(q, shift=UP * 0.1), run_time=0.6)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 3 ---------------------------------------------------------------- two sessions; a stacked PR
        with self.voiceover(SAY[2]) as vo:
            clear(self, 0.4)
            line, ticks, x_of = week_axis(y=0.4)
            self.play(Create(line), FadeIn(ticks), run_time=0.6)
            s1 = Rectangle(width=x_of(24 + 7 / 60) - x_of(12 + 22 / 60), height=0.4, stroke_width=0).set_fill(MODEL_C, 0.6)
            s1.move_to([(x_of(12 + 22 / 60) + x_of(24 + 7 / 60)) / 2, 1.2, 0])
            s2 = Rectangle(width=x_of(48 + 45 / 60) - x_of(25 + 51 / 60), height=0.4, stroke_width=0).set_fill(OURS_C, 0.6)
            s2.move_to([(x_of(25 + 51 / 60) + x_of(48 + 45 / 60)) / 2, 1.2, 0])
            l1 = VGroup(sans("session 1", 22), sans("commits Tue 12:22 → Wed 00:07", 20, S.GREY)
                        ).arrange(DOWN, aligned_edge=LEFT, buff=0.05).next_to(s1, UP, buff=0.12).align_to(s1, LEFT)
            l2 = VGroup(sans("session 2", 22), sans("commits Wed 01:51 → Thu 00:45", 20, S.GREY)
                        ).arrange(DOWN, aligned_edge=LEFT, buff=0.05).next_to(s2, UP, buff=0.12).align_to(s2, LEFT)
            vo.wait_until("the first until")
            self.play(GrowFromEdge(s1, LEFT), FadeIn(l1), run_time=0.6)
            vo.wait_until("the second from")
            self.play(GrowFromEdge(s2, LEFT), FadeIn(l2), run_time=0.6)
            vo.wait_until("stacked on top")
            b36 = Line([x_of(12.3), -1.7, 0], [x_of(48.8), -1.7, 0], color=MODEL_C, stroke_width=6)
            b41 = Line([x_of(25.98), -2.7, 0], [x_of(48.8), -2.7, 0], color=OURS_C, stroke_width=6)
            n36 = sans("#36 brain", 22, MODEL_C).next_to(b36, LEFT, buff=0.1).shift(RIGHT * 0.0)
            n36.move_to([x_of(12.3), -1.35, 0], aligned_edge=LEFT)
            n41 = sans("#41 page, built on #36", 22, OURS_C).move_to([x_of(25.98), -3.05, 0], aligned_edge=LEFT)
            fork = Line([x_of(25.9), -1.7, 0], [x_of(25.98), -2.7, 0], color=OURS_C, stroke_width=4)
            self.play(Create(b36), FadeIn(n36), Create(fork), Create(b41), FadeIn(n41), run_time=0.8)
            vo.wait_until("13 times")
            # #41's 18 merges minus the 5 fix-branch merges (18:24, 18:24, 18:25, 19:03, 19:16) = the 13 merges of #36
            merges = [h for h in M41 if h not in (42.405, 42.406, 42.417, 43.057, 43.275)]
            assert len(merges) == 13
            pulls = VGroup(*[Arrow([x_of(h), -1.75, 0], [x_of(h), -2.65, 0], buff=0, color=S.GREY, stroke_width=2,
                                   max_tip_length_to_length_ratio=0.2) for h in merges])
            cnt = sans("13 merges of #36 into #41", 22, S.GREY).move_to([5.9, -3.05, 0], aligned_edge=RIGHT)
            self.play(LaggedStart(*[GrowArrow(a) for a in pulls], lag_ratio=0.08), FadeIn(cnt), run_time=1.0)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(0.6)
        clear(self)
