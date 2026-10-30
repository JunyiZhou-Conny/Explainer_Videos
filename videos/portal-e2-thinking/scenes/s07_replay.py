"""S07 · A replay, and a real stop

1. The checked answer arrives whole (GREEN); a playhead runs a timeline of characters: text blocks type,
   structural blocks (places to go) drop in whole; at most 2.5 s (reveal.ts MAX_REVEAL_MS).
2. Emergency answers appear at once (answerBlocks.ts shouldAnimate). Stop: the page hangs up, the server
   aborts the model call (server.ts abortOnDisconnect).
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (CHECKED_C, DANGER_C, MODEL_C, NARRATION, OURS_C, clear, link, model_box, ours_box,
                    page_box, sans, screen, zh)

SAY = NARRATION["S07"]


def text_block(width, lines=2, color=S.WHITE):
    rows = VGroup(*[Rectangle(width=width - 0.5 * k, height=0.13, stroke_width=0).set_fill(color, 0.8)
                    for k in range(lines)]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    return rows


class Replay(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- a replay of checked text
        with self.voiceover(SAY[0]) as vo:
            scr = screen(6.4, 4.6).move_to(LEFT * 3.2 + DOWN * 0.2)
            chk = sans("checked answer, arrived whole", 20, CHECKED_C).next_to(scr, UP, buff=0.15).align_to(scr, LEFT)
            expl = text_block(5.6, 3)
            o1 = VGroup(zh("1. 去处和步骤", 24, S.WHITE), text_block(4.6, 1))
            o2 = VGroup(zh("2. ……", 24, S.WHITE), text_block(4.2, 1))
            for o in (o1, o2):
                o.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            watch = VGroup(zh("注意", 22, S.GREY), text_block(5.0, 2)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            content = VGroup(expl, o1, o2, watch).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(scr)
            self.play(FadeIn(scr), FadeIn(chk), run_time=0.5)
            # the timeline of characters: typed blocks are long, structural blocks a fixed pause
            seg = [("typed", 2.2), ("block", 0.8), ("block", 0.8), ("typed", 1.6)]
            bar = VGroup(*[Rectangle(width=w, height=0.32, stroke_color=S.GREY_DARK, stroke_width=2)
                           .set_fill(CHECKED_C if k == "typed" else S.GREY, 0.35) for k, w in seg]).arrange(RIGHT, buff=0)
            bar.move_to(RIGHT * 3.6 + UP * 1.4)
            labels = VGroup(*[sans(k, 20, S.GREY).next_to(b, DOWN, buff=0.08) for (k, _), b in zip(seg, bar)])
            cap = VGroup(zh("≤ 2.5 秒", 30, S.WHITE), sans("reveal.ts · MAX_REVEAL_MS = 2500", 20, S.GREY)
                         ).arrange(DOWN, buff=0.08).next_to(bar, UP, buff=0.3)
            self.play(FadeIn(bar), FadeIn(labels), FadeIn(cap), run_time=0.5)
            vo.wait_until("sentences type")
            head = Line(bar.get_corner(UL) + UP * 0.15, bar.get_corner(DL) + DOWN * 0.15, color=S.WHITE, stroke_width=4)
            self.add(head)
            for blk, b in zip([expl, o1, o2, watch], bar):
                target = b.get_right()[0]
                if blk in (o1, o2):
                    self.play(head.animate.set_x(target), FadeIn(blk, shift=DOWN * 0.08), run_time=0.35)
                else:
                    self.play(head.animate.set_x(target),
                              *[GrowFromEdge(r, LEFT) for r in (blk if blk is expl else blk[1])],
                              *([FadeIn(blk[0])] if blk is watch else []), run_time=0.7, rate_func=linear)
            vo.wait_until("It looks like streaming")
            replay = VGroup(sans("a replay, not a stream", 26, CHECKED_C)).next_to(bar, DOWN, buff=0.75)
            self.play(FadeIn(replay, shift=UP * 0.1), run_time=0.5)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- emergencies at once; stop really stops
        with self.voiceover(SAY[1]) as vo:
            clear(self, 0.4)
            scr2 = screen(4.8, 2.4).move_to(LEFT * 4.2 + UP * 1.7)
            red = RoundedRectangle(width=4.3, height=1.5, corner_radius=0.12, stroke_color=DANGER_C, stroke_width=3).move_to(scr2)
            now = zh("现在就做", 30, DANGER_C).move_to(red)
            at_once = sans("emergency: the whole answer at once", 20, S.GREY).next_to(scr2, DOWN, buff=0.12)
            self.play(FadeIn(scr2), FadeIn(red), FadeIn(now), FadeIn(at_once), run_time=0.4)
            vo.wait_until("the stop button")
            pg = page_box(width=2.6).move_to(LEFT * 4.6 + DOWN * 1.9)
            srv = ours_box("server", None, width=2.6).move_to(LEFT * 0.2 + DOWN * 1.9)
            mdl = model_box("gpt-6-luna", "OpenAI", width=2.6).move_to(RIGHT * 4.4 + DOWN * 1.9)
            l1 = link(pg, srv, OURS_C)
            l2 = link(srv, mdl, MODEL_C)
            stop_btn = VGroup(Circle(radius=0.35, color=S.WHITE, stroke_width=3),
                              Square(side_length=0.26, stroke_width=0).set_fill(S.WHITE, 1)).next_to(pg, UP, buff=0.25)
            self.play(FadeIn(pg), FadeIn(srv), FadeIn(mdl), Create(l1), Create(l2), FadeIn(stop_btn), run_time=0.7)
            vo.wait_until("hangs up")
            self.play(stop_btn.animate.scale(0.85), rate_func=there_and_back, run_time=0.3)
            x1 = Cross(l1, stroke_color=DANGER_C, stroke_width=5, scale_factor=0.5)
            self.play(FadeOut(l1), FadeIn(x1), run_time=0.4)
            vo.wait_until("cancels the model call")
            x2 = Cross(l2, stroke_color=DANGER_C, stroke_width=5, scale_factor=0.5)
            abort = sans("abort · the call stops", 22, DANGER_C).next_to(mdl, DOWN, buff=0.25)
            self.play(FadeOut(l2), FadeIn(x2), FadeIn(abort), run_time=0.5)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(0.6)
        clear(self)
