"""S09 · Recap

1. The four slots with their choices and reasons; the data model's job: privacy.
2. Three test-yourself questions, a held pause.
3. End card: 「项目周记 · 第 44 周 完」.
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (API_C, AUTH_C, DB_C, NARRATION, USER_C, WEB_C, clear, sans, serif, zh)

SAY = NARRATION["S09"]
SLOTS = [("TypeScript", "the page decides", API_C, "the page decides"), ("Postgres", "the data is links", DB_C, "the data is links"),
         ("emailed codes", "every parent has email", AUTH_C, "every parent has email"),
         ("containers", "runs on any laptop", WEB_C, "run on any laptop")]


class Recap(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- four choices, one job
        with self.voiceover(SAY[0]) as vo:
            cards = VGroup()
            for name, why, color, _ in SLOTS:
                body = VGroup(sans(name, 28, color), sans(why, 20, S.GREY)).arrange(DOWN, buff=0.12)
                frame = RoundedRectangle(width=3.1, height=1.4, corner_radius=0.16, stroke_color=color, stroke_width=2.5)
                body.move_to(frame)
                cards.add(VGroup(frame, body))
            cards.arrange(RIGHT, buff=0.15).move_to(UP * 1.6)
            for c, (*_, phrase) in zip(cards, SLOTS):
                vo.wait_until(phrase)
                self.play(FadeIn(c, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("whose real job is privacy")
            job = VGroup(sans("and a data model whose real job is privacy", 28, USER_C),
                         sans("fixed roles · links only students start · read-only cards · no card photos", 22, S.GREY)
                         ).arrange(DOWN, buff=0.12).move_to(DOWN * 0.8)
            self.play(FadeIn(job, shift=UP * 0.1), run_time=0.6)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- questions
        with self.voiceover(SAY[1]) as vo:
            clear(self, 0.4)

            def q(en, cn):
                return VGroup(serif(en, 30), zh(cn, 22, S.GREY)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            qs = VGroup(serif("Test yourself", 34, USER_C),
                        q("1.  Why isn't the backend in Python?", "为什么后端不用 Python？"),
                        q("2.  What stops a student from making themselves a parent?", "是什么阻止学生把自己改成家长？"),
                        q("3.  What would have caught the unlink bug without a bot?", "没有 bot 的话，什么能抓住解除关联的那个 bug？")
                        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(UP * 1.1)
            self.play(FadeIn(qs[0]), run_time=0.4)
            for qq, phrase in zip(qs[1:], ["Why isn't the backend", "What stops a student", "And what would have caught"]):
                vo.wait_until(phrase)
                self.play(FadeIn(qq, shift=RIGHT * 0.1), run_time=0.4)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(5.0)

        # 3 ---------------------------------------------------------------- end of the week
        with self.voiceover(SAY[2]) as vo:
            self.play(qs.animate.set_opacity(0.3), run_time=0.4)
            end = VGroup(zh("项目周记 · 第 44 周 完", 40), sans("next week's episodes start from next week's pull requests", 22, S.GREY)
                         ).arrange(DOWN, buff=0.18).move_to(DOWN * 2.45)
            frame = SurroundingRectangle(end, color=USER_C, buff=0.3, corner_radius=0.15)
            self.play(FadeIn(end, shift=UP * 0.1), Create(frame), run_time=0.7)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(1.0)
        clear(self)
