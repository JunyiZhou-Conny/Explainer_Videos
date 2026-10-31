"""S02 · Four jobs (decision 0006 「结论与理由」; meeting summary 2026-10-26:24; ../SOURCES.md)

A request's path: phone → web (the page) → api (a login step inside it, "who are you?", then rules and permission
checks; Better Auth runs inside the api, D:53) → db (remembers).
The 10/26 rule 「做出来的东西能在 Mac 和 Windows 上都跑起来」 → Docker Compose wraps db · api · web. The record fills each
slot: Hono + Zod · Postgres + Drizzle · Better Auth, email code · Docker Compose.
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (API_C, AUTH_C, DB_C, NARRATION, USER_C, WEB_C, clear, device, mono, sans, token, zh)

SAY = NARRATION["S02"]


def slot(name: str, job: str, color, width: float = 2.5) -> VGroup:
    body = VGroup(mono(name, 26, color), sans(job, 20, S.GREY)).arrange(DOWN, buff=0.08)
    frame = RoundedRectangle(width=width, height=1.25, corner_radius=0.14, stroke_color=color, stroke_width=2.5)
    body.move_to(frame)
    g = VGroup(frame, body)
    g.frame = frame
    return g


class Jobs(VoiceScene):
    def construct(self):
        with self.voiceover(SAY[0]) as vo:
            phone = device("parent", phone=True, height=1.6).move_to(LEFT * 5.7 + UP * 0.8)
            web = slot("web", "the page", WEB_C, 2.0).move_to(LEFT * 3.5 + UP * 0.8)
            api = slot("api", "rules · permissions", API_C, 4.4).move_to(RIGHT * 0.6 + UP * 0.8)
            api[1].shift(RIGHT * 0.9)
            gate = VGroup(RoundedRectangle(width=1.6, height=0.95, corner_radius=0.12, stroke_color=AUTH_C, stroke_width=2.5),
                          VGroup(mono("login", 22, AUTH_C), sans("who are you?", 20, S.GREY)).arrange(DOWN, buff=0.05))
            gate[1].move_to(gate[0])
            gate.move_to(api.frame.get_left() + RIGHT * 1.0)
            db = slot("db", "remembers", DB_C, 2.2).move_to(RIGHT * 4.7 + UP * 0.8)
            arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.08, color=S.GREY, stroke_width=3)
                              for a, b in [(phone, web), (web, api), (api, db)]])
            vo.wait_until("A backend has a few jobs")
            self.play(FadeIn(phone), FadeIn(web), Create(arrows[0]), run_time=0.6)
            vo.wait_until("A server receives")
            self.play(FadeIn(api), Create(arrows[1]), run_time=0.4)
            vo.wait_until("A database remembers")
            self.play(FadeIn(db), Create(arrows[2]), run_time=0.4)
            vo.wait_until("A login step")
            self.play(FadeIn(gate, scale=1.1), run_time=0.5)
            dot = token(USER_C).move_to(phone.get_center())
            path = [phone.get_center(), web.get_center(), gate.get_center(), api[1].get_center(), db.get_center()]
            self.play(FadeIn(dot), run_time=0.2)
            for p in path[1:]:
                self.play(dot.animate.move_to(p), run_time=0.35, rate_func=linear)
            self.play(FadeOut(dot), run_time=0.2)
            vo.wait_until("one hard rule")
            rule = VGroup(sans("Monday's meeting, 10/26:", 22, S.GREY), zh("「做出来的东西能在 Mac 和 Windows 上都跑起来」", 26, USER_C)
                          ).arrange(RIGHT, buff=0.25).move_to(UP * 3.0)
            self.play(FadeIn(rule, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("into containers")
            box = DashedVMobject(RoundedRectangle(width=10.6, height=2.0, corner_radius=0.2, stroke_color=S.WHITE,
                                                  stroke_width=2), num_dashes=70).move_to(RIGHT * 0.65 + UP * 0.8)
            cmd = mono("docker compose up", 24, S.WHITE).next_to(box, DOWN, buff=0.15).align_to(box, RIGHT)
            self.play(Create(box), FadeIn(cmd), run_time=0.8)
            vo.wait_until("The record fills each slot")
            picks = VGroup(sans("Hono + Zod", 24, API_C).next_to(api, DOWN, buff=0.9).align_to(api, RIGHT).shift(LEFT * 0.3),
                           sans("Postgres + Drizzle", 24, DB_C).next_to(db, DOWN, buff=0.9),
                           sans("Better Auth · emailed code", 24, AUTH_C).next_to(gate, DOWN, buff=1.05),
                           sans("Docker Compose", 24, S.WHITE).next_to(box, DOWN, buff=0.15).align_to(box, LEFT))
            for p, phrase in zip(picks, ["Hono and Zod", "Postgres for the database", "Better Auth", "Docker Compose"]):
                vo.wait_until(phrase)
                self.play(FadeIn(p, shift=UP * 0.1), run_time=0.35)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(0.6)
        clear(self)
