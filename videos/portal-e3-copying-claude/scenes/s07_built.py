"""S07 · How it was built (PR #41's commits, Boston time; ../SOURCES.md)

1. The night of Wednesday 2026-10-28: 01:45 issue #40 · 01:59 e8df1b7 decision 0006 · 02:16 a937b94 the rebuilt
   page (27 files) · 02:22 2934fde end-to-end tests (41 checks).
2. The day's reviews: 10:14 independent visual review (0df09f6) · 11:09–12:06 second visual review, Claude's
   phone layout (8153818) · 12:06 streaming review fixes (26b85e0) · 16:52–19:03 final review from five angles,
   36 findings (about 30 after duplicates), fixed on parallel branches.
3. One button, two jobs: stop's click re-sent the message (fixed 26b85e0, preventDefault); Bugbot's mirror
   image, a double-click on send stopped the request (fixed f95aa77, ignore the second click).
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (DANGER_C, FIELD, NARRATION, OURS_C, TERRA, USER_C, clear, mono, sans, send_key, zh)

SAY = NARRATION["S07"]


def axis(h0: float, h1: float, x0: float, x1: float, y: float, step: float, fmt) -> tuple:
    line = Line([x0, y, 0], [x1, y, 0], color=S.GREY, stroke_width=2)

    def x_of(h):
        return x0 + (h - h0) / (h1 - h0) * (x1 - x0)
    ticks = VGroup()
    h = h0
    while h <= h1 + 1e-9:
        ticks.add(VGroup(Line([x_of(h), y - 0.08, 0], [x_of(h), y + 0.08, 0], color=S.GREY),
                         sans(fmt(h), 20, S.GREY).move_to([x_of(h), y - 0.35, 0])))
        h += step
    return line, ticks, x_of


def hm(h: float) -> str:
    return f"{int(h):02d}:{round(h % 1 * 60):02d}"


def event(x_of, h, y, text, color, height, sub=None):
    p = np.array([x_of(h), y, 0])
    ln = Line(p, p + UP * height, color=color, stroke_width=3)
    lab = VGroup(sans(hm(h), 22, color), sans(text, 24))
    if sub:
        lab.add(sans(sub, 20, S.GREY))
    lab.arrange(RIGHT, buff=0.2).next_to(p + UP * height, RIGHT, buff=0.12)
    return VGroup(ln, lab)


class Built(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- the night
        with self.voiceover(SAY[0]) as vo:
            title = sans("Wednesday 2026-10-28 · Boston time · PR #41", 24, S.GREY).move_to(UP * 3.2)
            line, ticks, x_of = axis(1 + 40 / 60, 2.5, -6.0, 1.0, -2.2, 10 / 60, hm)
            self.play(FadeIn(title), Create(line), FadeIn(ticks), run_time=0.7)
            e0 = event(x_of, 1.75, -2.2, "issue #40", S.GREY, 3.4)
            self.play(FadeIn(e0), run_time=0.4)
            vo.wait_until("wrote the decision down")
            e1 = event(x_of, 1 + 59 / 60, -2.2, "decision 0006 recorded", USER_C, 2.6)
            self.play(FadeIn(e1), run_time=0.4)
            vo.wait_until("Seventeen minutes later")
            gap = DoubleArrow([x_of(1 + 59 / 60), -1.75, 0], [x_of(2 + 16 / 60), -1.75, 0], color=USER_C, buff=0,
                              stroke_width=3, tip_length=0.15)
            g_lab = sans("17 min", 22, USER_C).next_to(gap, DOWN, buff=0.06)
            self.play(GrowFromCenter(gap), FadeIn(g_lab), run_time=0.5)
            vo.wait_until("27 files")
            e2 = event(x_of, 2 + 16 / 60, -2.2, "the rebuilt page", OURS_C, 1.8, "27 files")
            self.play(FadeIn(e2), run_time=0.4)
            vo.wait_until("end-to-end tests")
            e3 = event(x_of, 2 + 22 / 60, -2.2, "end-to-end tests", OURS_C, 1.0, "41 checks")
            self.play(FadeIn(e3), run_time=0.4)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- the day's reviews
        with self.voiceover(SAY[1]) as vo:
            clear(self, 0.4)
            title = sans("the same Wednesday · when each round's fixes landed", 24, S.GREY).move_to(UP * 3.25)
            line, ticks, x_of = axis(9, 20, -6.0, 6.0, -2.6, 1, lambda h: f"{int(h)}:00")
            self.play(FadeIn(title), Create(line), FadeIn(ticks), run_time=0.6)

            def band(h0, h1, row, text, color, sub=None):
                r = Rectangle(width=max(0.12, x_of(h1) - x_of(h0)), height=0.34, stroke_width=0).set_fill(color, 0.7)
                r.move_to([(x_of(h0) + x_of(h1)) / 2, -2.6 + 0.45 + row * 0.82, 0])
                lab = VGroup(sans(text, 22))
                if sub:
                    lab.add(sans(sub, 20, S.GREY))
                lab.arrange(RIGHT, buff=0.2).next_to(r, UP, buff=0.08)
                lab.align_to(r, LEFT)
                if lab.get_right()[0] > 6.5:
                    lab.shift(LEFT * (lab.get_right()[0] - 6.5))
                return VGroup(r, lab)
            rows = [(10 + 2 / 60, 10 + 14 / 60, 0, "independent visual review", USER_C, None, "independent visual"),
                    (10 + 40 / 60, 11 + 4 / 60, 1, "streaming + model menu", OURS_C, "your request", "The streaming"),
                    (11 + 35 / 60, 12 + 6 / 60, 2, "streaming review", OURS_C, None, "a review of it"),
                    (11 + 23 / 60, 15 + 21 / 60, 3, "second visual review", USER_C, "phone layout, parent wording, accessibility",
                     "A second visual review"),
                    (16 + 52 / 60, 19 + 16 / 60, 4, "final review, five angles", DANGER_C, "36 findings, about 30 unique",
                     "five angles")]
            for h0, h1, row, text, color, sub, phrase in rows:
                vo.wait_until(phrase)
                self.play(FadeIn(band(h0, h1, row, text, color, sub), shift=UP * 0.1), run_time=0.45)
            vo.wait_until("parallel branches")
            angles = zh("安全和状态 · 流式后端 · 排版和无障碍 · 文案和文档 · 测试和检查规则", 20, S.GREY).move_to(UP * 2.75)
            par = sans("four parallel fix branches, each bug reproduced first", 22, S.GREY).next_to(angles, DOWN, buff=0.1)
            self.play(FadeIn(angles), FadeIn(par), run_time=0.5)
            vo.wait_until("checked once more")
            again = sans("re-review 19:04–19:16: 8 more found and fixed", 22, DANGER_C).next_to(par, DOWN, buff=0.1)
            self.play(FadeIn(again), run_time=0.4)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 3 ---------------------------------------------------------------- one button, two jobs
        with self.voiceover(SAY[2]) as vo:
            clear(self, 0.4)
            key = send_key(1.2).move_to(UP * 1.6)
            k_lab = sans("send", 26, S.GREY).next_to(key, DOWN, buff=0.2)
            self.play(FadeIn(key, scale=0.8), FadeIn(k_lab), run_time=0.5)
            vo.wait_until("send turns into stop")
            stop = send_key(1.2, stop=True).move_to(key)
            self.play(Transform(key, stop), Transform(k_lab, sans("stop", 26, S.GREY).move_to(k_lab)), run_time=0.5)
            vo.wait_until("Click stop")
            cursor = Triangle(color=USER_C, fill_opacity=1, stroke_width=0).scale(0.14).rotate(PI / 6)
            cursor.move_to(key.get_center() + DR * 0.2)
            self.play(FadeIn(cursor), cursor.animate.scale(0.8), rate_func=there_and_back, run_time=0.4)
            vo.wait_until("turns back into send")
            back = send_key(1.2).move_to(key)
            self.play(Transform(key, back), Transform(k_lab, sans("send", 26, S.GREY).move_to(k_lab)), run_time=0.3)
            vo.wait_until("whatever was in the box went out")
            bug1 = VGroup(sans("bug 1 · stop's click lands on send: the box is sent", 24, DANGER_C),
                          VGroup(mono("26b85e0", 22, S.GREY), sans("one line: the stop click does nothing else", 22)
                                 ).arrange(RIGHT, buff=0.3)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            bug1.move_to(DOWN * 0.6)
            self.play(FadeIn(bug1[0], shift=UP * 0.1), run_time=0.5)
            vo.wait_until("In a demo replay")
            demo = sans("(in a demo replay: the very message you had just stopped)", 22, S.GREY).next_to(bug1[0], DOWN, buff=0.08)
            demo.align_to(bug1[0], LEFT)
            bug1[1].next_to(demo, DOWN, buff=0.12).align_to(demo, LEFT)   # not on screen yet: move it, don't animate it
            self.play(FadeIn(demo), run_time=0.4)
            vo.wait_until("The fix was one line")
            self.play(FadeIn(bug1[1]), run_time=0.4)
            vo.wait_until("the mirror image")
            bug2 = VGroup(sans("bug 2 · Bugbot, Medium: double-click send, the second click hits stop", 24, DANGER_C),
                          VGroup(mono("f95aa77", 22, S.GREY), sans("one line: ignore the second click of a double-click", 22)
                                 ).arrange(RIGHT, buff=0.3)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            bug2.next_to(bug1, DOWN, buff=0.45).align_to(bug1, LEFT)
            self.play(FadeOut(cursor), FadeIn(bug2[0], shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Another one-line fix")
            self.play(FadeIn(bug2[1]), run_time=0.4)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(0.6)
        clear(self)
