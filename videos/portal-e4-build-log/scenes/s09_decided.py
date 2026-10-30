"""S09 · Who decided, and what waits (../SOURCES.md)

1. Some of the owner's calls, as the agents recorded them (YELLOW): the model and its effort (decision 0004, 10-27); the turn (Tue 21:21);
   batch the fixes (PR #36 handoff, Wed 00:26); copy Claude's page (issue #40); the stop rule
   「做到 99% 就停，之后 bot 的新评论先放着；最晚周四晚上 7 点（按北京时间算）收尾。」 (PR #41 handoff).
   Deadline Thu 19:00 Beijing = Thu 07:00 Boston; the last push Thu 00:45 Boston, 6 h 15 min early; the handoff
   addendum (Thu 11:12 Boston) wrote down 4 later bot findings, unfixed, for the next person.
2. Some choices the agents made alone (WHITE), written as 「提议」 under 「无人值守，未经人确认」; one took a click
   docs/workflow.md reserves for a person (「两次点击都由人来做」: marking PR #36 ready, Tue 22:23); the PR #36
   handoff admits 「agent 早先说「Bugbot 意见都修了」，实际有 2 条没修」.
3. Ponder: with no person having reviewed it yet, what makes this code trustworthy?
4. Layers, each with holes (an illustration): 807 unit tests (one replays the 1,060 probes) · two review bots ·
   records that stay 「提议」 until signed. Decision 0004 is itself still 「提议」; before any real user it requires an
   evaluation and the medical reviewer's look at the red-flag cases. Then the 12 headings under
   「下一步（等 Junyi 定）」 (PR #41 handoff), 1 and 5 lit.
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (CHECKED_C, DANGER_C, NARRATION, USER_C, chip, clear, mark_bad, ponder_zh, quote_panel, sans, zh)

SAY = NARRATION["S09"]
OWNER = [("the model and its effort", "decision 0004 · Tue", "the model and its effort"),
         ("the turn to the model's judgement", "Tue 21:21", "the turn to"),
         ("batch the fixes", "PR #36 handoff · Wed 00:26", "batching the fixes"),
         ("copy Claude's page, one to one", "issue #40 · episode 3", "copying Claude's page"),
         ("the stop rule", "PR #41 handoff · 10-29", "and the stop rule")]
AGENTS = ["probe the checker before pushing", "at most 3 agents per round", "loosen 6 checker exceptions · 请过目",
          "Stop keeps the unanswered message", "mark PR #36 ready for review"]
TODO = ["决策 0006 的「10-28 晚补充」", "停止以后的新做法", "Codex P3「调用前预留预算」", "Codex P2「引用格式和评估」",
        "家长看到的危机热线", "开发者看原始草稿的开关", "离线假模型更保守了", "放宽的检查例外，请过目", "合并顺序",
        "urgent care 的营业时间", "SHS 开放时间卡过期以后", "已知不管的两处"]


def card(title: str, sub: str | None, color, width: float) -> VGroup:
    t = zh(title, 22) if not title.isascii() else sans(title, 22)
    rows = VGroup(t, *([sans(sub, 20, S.GREY)] if sub else [])).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
    frame = RoundedRectangle(width=width, height=rows.height + 0.26, corner_radius=0.12, stroke_color=color,
                             stroke_width=2.5).set_fill(color, 0.08)
    rows.move_to(frame).align_to(frame, LEFT).shift(RIGHT * 0.2)
    return VGroup(frame, rows)


class Decided(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- the owner's calls
        with self.voiceover(SAY[0]) as vo:
            head_l = sans("your calls, as the agents recorded them", 26, USER_C).move_to(LEFT * 3.6 + UP * 3.2)
            who = chip("who decided?", USER_C, 30, mono_font=False).move_to(RIGHT * 3.0 + UP * 1.75)
            self.play(FadeIn(who, scale=1.1), run_time=0.4)
            vo.wait_until("names your calls")
            self.play(FadeIn(head_l), run_time=0.4)
            owner = VGroup(*[card(t, s, USER_C, 5.0) for t, s, _ in OWNER]).arrange(DOWN, buff=0.14)
            owner.move_to(LEFT * 3.6 + DOWN * 0.15)
            for c, (_, _, phrase) in zip(owner, OWNER):
                vo.wait_until(phrase)
                self.play(FadeIn(c, shift=RIGHT * 0.1), run_time=0.35)
            vo.wait_until("stop at 99 percent")
            rule = quote_panel("做到 99% 就停，之后 bot 的新评论先放着；最晚周四晚上 7 点（按北京时间算）收尾。",
                               "PR #41 handoff · 收尾的约定", width=6.4, size=24, color=USER_C).move_to(RIGHT * 3.0 + UP * 1.75)
            self.play(Circumscribe(owner[4], color=USER_C), FadeOut(who), FadeIn(rule, shift=LEFT * 0.1), run_time=0.7)
            vo.wait_until("The code kept it")
            x0, x1, y = 0.4, 6.0, -1.1

            def x_of(h):
                return x0 + h / 8 * (x1 - x0)
            axis = Line([x0, y, 0], [x1, y, 0], color=S.GREY, stroke_width=2)
            ticks = VGroup(*[VGroup(Line([x_of(h), y - 0.07, 0], [x_of(h), y + 0.07, 0], color=S.GREY),
                                    sans(f"{h:02d}:00", 20, S.GREY).move_to([x_of(h), y - 0.32, 0])) for h in (0, 2, 4, 6, 8)])
            day = sans("Thursday · Boston time", 20, S.GREY).move_to([x0, y - 0.7, 0], aligned_edge=LEFT)
            push = VGroup(Dot([x_of(0.75), y, 0], radius=0.09, color=CHECKED_C),
                          sans("last push 00:45", 22, CHECKED_C).move_to([x_of(0.75), y + 0.45, 0], aligned_edge=LEFT))
            push[1].shift(LEFT * 0.15)
            dead = VGroup(Line([x_of(7), y - 0.25, 0], [x_of(7), y + 0.3, 0], color=USER_C, stroke_width=4),
                          VGroup(sans("deadline 07:00", 22, USER_C), sans("= Thu 19:00 Beijing", 20, S.GREY)
                                 ).arrange(DOWN, aligned_edge=RIGHT, buff=0.04))
            dead[1].move_to([x1, y + 0.75, 0], aligned_edge=RIGHT)
            self.play(Create(axis), FadeIn(ticks), FadeIn(day), FadeIn(dead), run_time=0.6)
            self.play(FadeIn(push, scale=1.2), run_time=0.4)
            vo.wait_until("six hours early")
            gap = DoubleArrow([x_of(0.75), y - 1.05, 0], [x_of(7), y - 1.05, 0], buff=0, color=CHECKED_C, stroke_width=3,
                              max_tip_length_to_length_ratio=0.06)
            gap_l = sans("6 h 15 min to spare", 22, CHECKED_C).next_to(gap, DOWN, buff=0.1)
            self.play(GrowFromCenter(gap), FadeIn(gap_l), run_time=0.5)
            vo.wait_until("four later bot findings")
            later = sans("4 later bot findings: written down, left for the next person", 20, S.GREY).move_to([3.2, -3.35, 0])
            self.play(FadeIn(later), run_time=0.4)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- what the agents decided alone
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(rule, axis, ticks, day, push, dead, gap, gap_l, later)),
                      *[c[0].animate.set_stroke(opacity=0.45).set_fill(opacity=0.03) for c in owner],
                      *[c[1].animate.set_opacity(0.45) for c in owner], run_time=0.4)
            head_r = sans("some of the agents' own calls", 26).move_to(RIGHT * 3.4 + UP * 3.2)
            agents = VGroup(*[card(t, None, S.WHITE, 5.6) for t in AGENTS]).arrange(DOWN, buff=0.12)
            agents.move_to(RIGHT * 3.4 + UP * 0.35)
            vo.wait_until("Many smaller choices")
            self.play(FadeIn(head_r), LaggedStart(*[FadeIn(c, shift=LEFT * 0.1) for c in agents], lag_ratio=0.12), run_time=1.0)
            tags = VGroup(chip("提议", S.GREY, 22, mono_font=False), chip("无人值守，未经人确认", S.GREY, 22, mono_font=False)
                          ).arrange(RIGHT, buff=0.2).next_to(agents, UP, buff=0.2)
            vo.wait_until("as proposals")
            self.play(FadeIn(tags[0], scale=1.1), run_time=0.35)
            vo.wait_until("marked unattended")
            self.play(FadeIn(tags[1], scale=1.1), run_time=0.35)
            vo.wait_until("reserves for a person")
            rule2 = VGroup(zh("「两次点击都由人来做」", 22, DANGER_C), sans("docs/workflow.md", 20, S.GREY)
                           ).arrange(RIGHT, buff=0.2).next_to(agents[4], DOWN, buff=0.12).align_to(agents[4], RIGHT)
            self.play(Circumscribe(agents[4], color=DANGER_C), FadeIn(rule2), run_time=0.7)
            vo.wait_until("honest about slips")
            slip = quote_panel("agent 早先说「Bugbot 意见都修了」，实际有 2 条没修", "PR #36 handoff · Wed 00:26",
                               width=6.4, size=24).move_to(RIGHT * 3.4 + DOWN * 2.6)
            self.play(FadeOut(rule2), FadeIn(slip, shift=UP * 0.1), run_time=0.5)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 3 ---------------------------------------------------------------- ponder
        with self.voiceover(SAY[2]) as vo:
            clear(self, 0.4)
            ponder_zh(self, "With no person having reviewed it yet, what makes this code trustworthy?",
                      "还没有人审过，这份代码凭什么可信？", seconds=4.0)
        self.wait(3.5)
        clear(self, 0.4)

        # 4 ---------------------------------------------------------------- layers, then the twelve items
        with self.voiceover(SAY[3]) as vo:
            names = ["807 unit tests", "2 review bots", "「提议」 until signed"]
            subs = ["one replays the 1,060 probes", "Bugbot · Codex", "decision records"]
            phrases = ["hundreds of tests", "two review bots", "decision records"]
            holes = [(0, 1), (0, 2), (1, 2)]      # which bug lanes each layer lets through
            lanes = [1.9, 0.95, 0.0]
            xs = [-3.6, 0.0, 3.6]
            layers = VGroup()
            for x, open_, name, sub in zip(xs, holes, names, subs):
                slab = Rectangle(width=0.4, height=2.9, stroke_color=S.GREY, stroke_width=2).set_fill(S.GREY_DARKER, 1)
                slab.move_to([x, 0.95, 0])
                gaps = VGroup(*[Circle(radius=0.19, stroke_color=S.GREY, stroke_width=2).set_fill(S.BG, 1)
                                .move_to([x, lanes[i], 0]) for i in open_])
                lab = VGroup(zh(name, 24) if not name.isascii() else sans(name, 24), sans(sub, 20, S.GREY)
                             ).arrange(DOWN, buff=0.06).move_to([x, -1.05, 0])
                layers.add(VGroup(slab, gaps, lab))
            vo.wait_until("No single check")
            note = sans("illustration: every layer has holes; together they catch more", 22, S.GREY).move_to(UP * 3.2)
            self.play(FadeIn(note), run_time=0.4)
            for layer, phrase in zip(layers, phrases):
                vo.wait_until(phrase)
                self.play(FadeIn(layer[0]), FadeIn(layer[1]), FadeIn(layer[2]), run_time=0.35)
            # three bugs: each slips through some layers and is stopped by another
            stops = []
            for lane_i, y in enumerate(lanes):
                for k, (x, open_) in enumerate(zip(xs, holes)):
                    if lane_i not in open_:
                        stops.append((y, x - 0.32))
                        break
            bugs = VGroup(*[Dot([-6.2, y, 0], radius=0.1, color=DANGER_C) for y, _ in stops])
            self.play(FadeIn(bugs), run_time=0.2)
            self.play(*[b.animate.move_to([sx, y, 0]) for b, (y, sx) in zip(bugs, stops)], run_time=1.0, rate_func=linear)
            self.play(*[FadeIn(mark_bad(0.24, DANGER_C).move_to(b.get_center() + LEFT * 0.35)) for b in bugs], run_time=0.3)
            vo.wait_until("Decision four itself")
            d4 = VGroup(VGroup(sans("decision 0004", 24), chip("提议", S.GREY, 22, mono_font=False)).arrange(RIGHT, buff=0.2),
                        sans("before any real user: an evaluation, and the medical reviewer's look at the red-flag cases", 22, S.GREY)
                        ).arrange(DOWN, buff=0.1).move_to(DOWN * 2.6)
            self.play(FadeIn(d4, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Twelve more questions")
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)
            title = VGroup(zh("下一步（等 Junyi 定）", 30, USER_C), sans("12 items waiting · PR #41 handoff, headings", 20, S.GREY)
                           ).arrange(DOWN, buff=0.08).move_to(UP * 3.0)
            items = VGroup(*[zh(f"{i + 1:>2}. {t}", 24) for i, t in enumerate(TODO)])
            col_a = VGroup(*items[:6]).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
            col_b = VGroup(*items[6:]).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
            VGroup(col_a, col_b).arrange(RIGHT, buff=0.9, aligned_edge=UP).move_to(DOWN * 0.45)
            self.play(FadeIn(title), LaggedStart(*[FadeIn(i, shift=UP * 0.1) for i in items], lag_ratio=0.05), run_time=1.0)
            vo.wait_until("decision six's addendum")
            self.play(Circumscribe(items[0], color=USER_C), items[0].animate.set_color(USER_C), run_time=0.6)
            vo.wait_until("a dial link")
            self.play(Circumscribe(items[4], color=USER_C), items[4].animate.set_color(USER_C), run_time=0.6)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(1.0)
        clear(self)
