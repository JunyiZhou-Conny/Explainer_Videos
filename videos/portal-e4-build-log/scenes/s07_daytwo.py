"""S07 · Day two: a queue of fix agents (PR #41 + #36, Wed; handoff of 10-29)

1. Wed: 01:59 the chat page (E3); the brain's fixes beside it; 15:37 a final review from five angles, about
   30 problems.
2. Six fix branches (fix41/labels · state · layout · tests · fix36/parent-911 · cost-shs), their agents queued
   (「6 个修复 agent 排着队跑」; fix commits 16:52 → 19:07), each reproducing its bug first; merged back 18:24 → 19:11;
   collisions, e.g. 9106471 at 19:04 (「4 项不通过」); a second review of the merged result: 8 more fixes
   (fix41/review3, merged 19:16).
3. Session 2 (no times recorded): two five-hour usage limits, two container restarts; the six fix agents queued at
   ≈ 800,000 tokens each; afterwards at most three per round (handoff).
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (CHECKED_C, DANGER_C, MODEL_C, NARRATION, OURS_C, USER_C, clear, mark_ok, mono, sans, tag_box, zh)

SAY = NARRATION["S07"]
BRANCHES = [("fix41/labels", OURS_C), ("fix41/state", OURS_C), ("fix41/layout", OURS_C), ("fix41/tests", OURS_C),
            ("fix36/parent-911", MODEL_C), ("fix36/cost-shs", MODEL_C)]


class DayTwo(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- a final review from five angles
        with self.voiceover(SAY[0]) as vo:
            head = sans("Wednesday · session 2", 26, S.GREY).move_to(UP * 3.2)
            self.play(FadeIn(head), run_time=0.3)
            page = tag_box("01:59", "the chat page", "episode 3", OURS_C, width=4.0).move_to(LEFT * 4.2 + UP * 1.6)
            brain = tag_box("all day", "the brain's fixes", "PR #36", MODEL_C, width=4.0).move_to(LEFT * 4.2 + DOWN * 0.2)
            vo.wait_until("built the chat page")
            self.play(FadeIn(page, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("kept fixing the brain")
            self.play(FadeIn(brain, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("five angles")
            angles = ["安全和状态", "流式后端", "排版和无障碍", "文案和文档", "测试和检查规则"]
            centre = RIGHT * 2.6 + UP * 0.6
            pent = RegularPolygon(5, radius=1.5, color=USER_C).move_to(centre)
            labs = VGroup(*[zh(a, 22).move_to(centre + 2.2 * np.array([np.cos(PI / 2 + k * 2 * PI / 5),
                                                                       np.sin(PI / 2 + k * 2 * PI / 5), 0]))
                            for k, a in enumerate(angles)])
            when = sans("15:37 · the final review", 22, USER_C).move_to(centre + DOWN * 2.3)
            self.play(Create(pent), LaggedStart(*[FadeIn(l) for l in labs], lag_ratio=0.15), FadeIn(when), run_time=1.0)
            vo.wait_until("about 30 problems")
            found = sans("about 30 problems", 28, DANGER_C).move_to(centre + DOWN * 2.85)
            self.play(FadeIn(found, scale=1.2), run_time=0.4)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- six branches, reproduce first
        with self.voiceover(SAY[1]) as vo:
            clear(self, 0.4)
            base = Line(LEFT * 6.2 + DOWN * 2.6, RIGHT * 6.2 + DOWN * 2.6, color=S.GREY, stroke_width=6)
            x_out, x_in = -3.4, 3.6
            ys = [2.4 - k * 0.78 for k in range(6)]
            branches = VGroup()
            for (name, color), y in zip(BRANCHES, ys):
                up = Line([x_out, -2.6, 0], [x_out + 0.6, y, 0], color=color, stroke_width=3)
                run = Line([x_out + 0.6, y, 0], [x_in - 0.6, y, 0], color=color, stroke_width=3)
                down = Line([x_in - 0.6, y, 0], [x_in, -2.6, 0], color=color, stroke_width=3)
                lab = mono(name, 20).next_to(run, UP, buff=0.05).align_to(run, LEFT).shift(RIGHT * 0.1)
                rep = VGroup(mark_ok(0.2, CHECKED_C), sans("reproduced", 20, CHECKED_C)).arrange(RIGHT, buff=0.1)
                rep.next_to(run, UP, buff=0.05).align_to(run, RIGHT)
                branches.add(VGroup(up, run, down, lab, rep))
            self.play(Create(base), run_time=0.4)
            vo.wait_until("one after another")
            self.play(LaggedStart(*[AnimationGroup(Create(b[0]), Create(b[1]), FadeIn(b[3])) for b in branches], lag_ratio=0.15),
                      run_time=1.4)
            vo.wait_until("first reproduced")
            self.play(LaggedStart(*[FadeIn(b[4]) for b in branches], lag_ratio=0.1), run_time=0.8)
            vo.wait_until("Merging them back")
            when = sans("fixes 16:52 → 19:07 · merged back 18:24 → 19:11", 22, S.GREY).move_to(RIGHT * 3.2 + DOWN * 3.05)
            self.play(LaggedStart(*[Create(b[2]) for b in branches], lag_ratio=0.1), FadeIn(when), run_time=1.0)
            vo.wait_until("had collisions")
            hit = VGroup(Star(n=8, outer_radius=0.3, inner_radius=0.14, color=DANGER_C, fill_opacity=1),
                         sans("e.g. labels added a field; the tests branch rejected it: 4 failures, fixed 19:04", 22, DANGER_C)
                         ).arrange(RIGHT, buff=0.2).move_to(DOWN * 3.3 + LEFT * 1.2)
            self.play(FadeOut(when), FadeIn(hit), run_time=0.5)
            vo.wait_until("A second review")
            more = VGroup(mark_ok(0.24, CHECKED_C), sans("a second review of the merged result: 8 more fixes · 19:16", 22, CHECKED_C)
                          ).arrange(RIGHT, buff=0.15).move_to(UP * 3.25)
            self.play(FadeIn(more), run_time=0.4)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 3 ---------------------------------------------------------------- limits and restarts
        with self.voiceover(SAY[2]) as vo:
            clear(self, 0.4)
            vo.wait_until("five-hour usage limit")
            walls = VGroup(*[VGroup(Rectangle(width=0.35, height=2.3, stroke_width=0).set_fill(DANGER_C, 0.7),
                                    sans("5-hour usage limit", 20, DANGER_C)) for _ in range(2)])
            for w in walls:
                w[1].next_to(w[0], UP, buff=0.1)
            walls.arrange(RIGHT, buff=3.2).move_to(UP * 1.05)
            self.play(LaggedStart(*[FadeIn(w, shift=DOWN * 0.2) for w in walls], lag_ratio=0.4), run_time=0.8)
            vo.wait_until("six fix agents ran in a row")
            queue = VGroup(*[tag_box("agent", f"fix {i + 1}", None, S.GREY, width=1.5) for i in range(6)]
                           ).arrange(RIGHT, buff=0.12).move_to(DOWN * 1.4)
            tok = sans("queued one after another · ≈ 800,000 tokens each", 24, USER_C).next_to(queue, DOWN, buff=0.2)
            self.play(LaggedStart(*[FadeIn(q) for q in queue], lag_ratio=0.1), FadeIn(tok), run_time=0.8)
            vo.wait_until("restarted twice")
            rs = VGroup(sans("container restarts: 2", 24), sans("local commits survive · a running test is cut off", 20, S.GREY)
                        ).arrange(DOWN, buff=0.06).move_to(UP * 3.1)
            self.play(FadeIn(rs), run_time=0.4)
            vo.wait_until("at most three")
            self.play(VGroup(*queue[3:]).animate.set_opacity(0.2), run_time=0.4)
            rule = sans("afterwards: at most 3 agents per round", 26, CHECKED_C).next_to(tok, DOWN, buff=0.3)
            self.play(FadeIn(rule), run_time=0.4)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(0.6)
        clear(self)
