"""S03 · The page decides the language (decision 0006 D:21-39; ../SOURCES.md)

1. A browser box: runs JavaScript / TypeScript. The first question was language.
2. Ponder: you read Python; why isn't the backend in Python?
3. 「前端是固定的约束，应该是后端适配前端。」 (D:25); both prototypes already TypeScript, in open PRs (#36, #38); one shape
   of data shared by page and server (Hono `hc`, D:32): a field renamed on the server fails the page's check.
4. Rejected, with the record's reasons: Python + FastAPI (D:36; kept as a later separate service, D:39), Express (D:34),
   NestJS (D:35), Supabase / Firebase (D:37). Fastify: 「同样合适…没有决定性差异」 (D:33), an equal alternative, not struck.
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (API_C, CHECKED_C, DANGER_C, NARRATION, USER_C, WEB_C, chip, clear, mark_bad, mono, option, ponder_zh,
                    quote_panel, sans)

SAY = NARRATION["S03"]


class Language(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- the question
        with self.voiceover(SAY[0]) as vo:
            browser = VGroup(RoundedRectangle(width=6.2, height=1.5, corner_radius=0.16, stroke_color=WEB_C, stroke_width=2.5),
                             VGroup(sans("a browser runs", 22, S.GREY), mono("JavaScript / TypeScript", 26, WEB_C)
                                    ).arrange(DOWN, buff=0.08))
            browser[1].move_to(browser[0])
            browser.move_to(UP * 1.2)
            q = sans("which language for the server?", 30, USER_C).next_to(browser, DOWN, buff=0.5)
            self.play(FadeIn(browser), FadeIn(q), run_time=0.6)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- ponder
        with self.voiceover(SAY[1]) as vo:
            clear(self, 0.3)
            card = ponder_zh(self, "You read Python. Why isn't the backend in Python?", "你看得懂 Python。为什么后端不用 Python？",
                             seconds=4.0)
        self.wait(2.0)

        # 3 ---------------------------------------------------------------- the page decides
        with self.voiceover(SAY[2]) as vo:
            clear(self, 0.3)
            browser.move_to(UP * 1.2)
            self.play(FadeIn(browser), run_time=0.4)
            rule = quote_panel("前端是固定的约束，应该是后端适配前端。", "decision record · backend stack", width=8.4, size=30,
                               color=USER_C).move_to(UP * 2.75)
            vo.wait_until("The record makes it a rule")
            self.play(FadeOut(browser), FadeIn(rule, shift=DOWN * 0.1), run_time=0.6)
            protos = VGroup(chip("triage · TypeScript · PR #36", WEB_C, 22), chip("insurance · TypeScript · PR #38", WEB_C, 22)
                            ).arrange(RIGHT, buff=0.4).move_to(UP * 1.25)
            vo.wait_until("Both prototypes")
            self.play(LaggedStart(*[FadeIn(p) for p in protos], lag_ratio=0.3), run_time=0.7)
            shape = VGroup(RoundedRectangle(width=3.2, height=1.5, corner_radius=0.14, stroke_color=USER_C, stroke_width=2.5),
                           VGroup(mono("InsuranceCard", 24, USER_C), mono("memberId", 22), mono("groupNumber", 22)
                                  ).arrange(DOWN, aligned_edge=LEFT, buff=0.06))
            shape[1].move_to(shape[0])
            shape.move_to(DOWN * 0.9)
            page = VGroup(RoundedRectangle(width=2.4, height=1.0, corner_radius=0.14, stroke_color=WEB_C, stroke_width=2.5),
                          sans("page", 26, WEB_C))
            page[1].move_to(page[0])
            page.move_to(LEFT * 4.6 + DOWN * 0.9)
            server = VGroup(RoundedRectangle(width=2.4, height=1.0, corner_radius=0.14, stroke_color=API_C, stroke_width=2.5),
                            sans("server", 26, API_C))
            server[1].move_to(server[0])
            server.move_to(RIGHT * 4.6 + DOWN * 0.9)
            links = VGroup(Line(page.get_right(), shape.get_left(), color=S.GREY), Line(shape.get_right(), server.get_left(), color=S.GREY))
            vo.wait_until("share a single description")
            illus = sans("illustration", 20, S.GREY).next_to(shape, UP, buff=0.12)
            self.play(FadeIn(page), FadeIn(server), FadeIn(shape), FadeIn(illus), Create(links), run_time=0.8)
            vo.wait_until("rename a field")
            renamed = mono("memberNo", 22, API_C).move_to(shape[1][1], aligned_edge=LEFT)
            self.play(Transform(shape[1][1], renamed), run_time=0.5)
            vo.wait_until("fails its check")
            fail = VGroup(mark_bad(0.28, DANGER_C), sans("page: check fails, before anyone runs it", 24, DANGER_C)
                          ).arrange(RIGHT, buff=0.15).next_to(shape, DOWN, buff=0.4)
            self.play(page[0].animate.set_stroke(DANGER_C), FadeIn(fail), run_time=0.5)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 4 ---------------------------------------------------------------- what lost, and why
        with self.voiceover(SAY[3]) as vo:
            clear(self, 0.4)
            py = option("Python + FastAPI", "its strength, AI retrieval libraries, isn't needed: triage looks up fact cards "
                        "by code, not by vector search; two copies of every type", False, width=6.4)
            exit_ = sans("→ kept as a separate service later", 22, CHECKED_C)
            opts = VGroup(option("Express", "没有内建的请求检查和类型，要自己拼", False, width=6.0),
                          option("NestJS", "规矩多、样板代码多，对三个人的 MVP 太重", False, width=6.0),
                          option("Supabase · Firebase", "user and health data with a third party, before privacy rules exist",
                                 False, width=6.0),
                          option("Fastify", "同样合适……没有决定性差异 · an equal alternative", True, width=6.0)
                          ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
            left = VGroup(py, exit_).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(LEFT * 3.25 + UP * 1.0)
            opts.move_to(RIGHT * 3.3 + DOWN * 0.1)
            opts[3][0].set_stroke(S.GREY)
            vo.wait_until("Python's main advantage")
            self.play(FadeIn(py), run_time=0.5)
            vo.wait_until("Python stays an exit")
            self.play(FadeIn(exit_), run_time=0.4)
            for o, phrase in zip(opts[:3], ["Express lost", "NestJS", "hosted backends"]):
                vo.wait_until(phrase)
                self.play(FadeIn(o, shift=LEFT * 0.1), run_time=0.4)
            self.play(FadeIn(opts[3]), run_time=0.4)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(0.6)
        clear(self)
