"""S03 · Hidden tokens and the stopwatch

1. A model writes one token at a time; a reasoning model first writes tokens for itself (grey).
2. Those stay hidden: not returned, but they take up room and are billed at the output price.
3. Then the answer's tokens (white): the 13-box form. The stopwatch splits at the first character of the
   answer: thinking | writing (server.ts: stage 'writing' at the first text delta).
4. Effort: low → a short grey run, high → a long one. Two real receipts (gpt-6-luna · 中): 1.6 | 1.5 and 13.5 | 8.7.
5. Ponder: what are you paying for, and how would you know?
6. The usage report of a typical turn (server.ts TYPICAL_TURN) → the price list (pricing.ts) → the receipt's price.
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (HIDDEN_C, MODEL_C, NARRATION, OURS_C, TEXT_C, USER_C, clear, link, model_box,
                    ours_box, phase_bars, ponder_zh, sans, serif, tape, text_panel, zh)

SAY = NARRATION["S03"]
N, HID = 30, 14


class HiddenTokens(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- one token at a time
        with self.voiceover(SAY[0]) as vo:
            model = model_box("gpt-6-luna", "reasoning model", width=3.0).move_to(LEFT * 5.0 + UP * 1.6)
            row = tape(N, HID, size=0.24, buff=0.06).next_to(model, RIGHT, buff=0.4)
            self.play(FadeIn(model), run_time=0.5)
            vo.wait_until("one small piece")
            one = sans("one token at a time", 22, S.GREY).next_to(row[0], UP, buff=0.35).align_to(row, LEFT)
            self.play(FadeIn(row[0], scale=0.5), FadeIn(one), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(c, scale=0.5) for c in row[1:4]], lag_ratio=0.3), run_time=0.8)
            vo.wait_until("for itself")
            thoughts = sans("its thoughts", 24, S.GREY).next_to(row[:HID], DOWN, buff=0.3)
            illus = VGroup(*[sans(t, 22, S.GREY) for t in
                             ["“fever and a sore throat … could be strep?", " any red flags? breathing OK?",
                              " is the student clinic open today? …”"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            illus.next_to(thoughts, DOWN, buff=0.25).align_to(row, LEFT)
            itag = sans("illustration: the real thoughts are never sent to us", 20, USER_C).next_to(illus, DOWN, buff=0.15)
            itag.align_to(illus, LEFT)
            self.play(LaggedStart(*[FadeIn(c, scale=0.5) for c in row[4:HID]], lag_ratio=0.15),
                      FadeIn(thoughts), run_time=1.3)
            self.play(FadeIn(illus, shift=UP * 0.1), FadeIn(itag), run_time=0.6)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(2.0)   # time to read the illustrated thoughts before they are hidden

        # 2 ---------------------------------------------------------------- hidden, but billed
        with self.voiceover(SAY[1]) as vo:
            grey = row[:HID]
            curtain = Rectangle(width=grey.width + 0.25, height=0.7, stroke_color=HIDDEN_C, stroke_width=2
                                ).set_fill(S.BG, 0.93).move_to(grey)
            hid = sans("hidden", 22, S.GREY).move_to(curtain)
            self.play(FadeIn(curtain), FadeIn(hid), FadeOut(thoughts), FadeOut(illus), FadeOut(itag), run_time=0.6)
            vo.wait_until("take up room")
            bill = VGroup(sans("not returned · still in the context · billed as output", 22, S.GREY),
                          zh("不返回 · 仍占上下文 · 按输出计费", 22, S.GREY)).arrange(DOWN, buff=0.1)
            bill.next_to(curtain, DOWN, buff=0.3).align_to(curtain, LEFT)
            self.play(FadeIn(bill, shift=UP * 0.1), run_time=0.6)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 3 ---------------------------------------------------------------- then the answer; the stopwatch splits
        with self.voiceover(SAY[2]) as vo:
            white = row[HID:]
            self.play(FadeOut(one), FadeOut(bill), LaggedStart(*[FadeIn(c, scale=0.5) for c in white], lag_ratio=0.08), run_time=1.4)
            form = sans("the answer: our 13-box form, as JSON", 22, S.WHITE).next_to(white, DOWN, buff=0.3).align_to(white, LEFT)
            self.play(FadeIn(form), run_time=0.4)
            vo.wait_until("our stopwatch")
            b1 = Brace(grey, UP, color=HIDDEN_C, buff=0.12)
            b2 = Brace(white, UP, color=TEXT_C, buff=0.12)
            l1 = VGroup(zh("思考", 26, S.GREY), sans("thinking", 20, S.GREY)).arrange(RIGHT, buff=0.15).next_to(b1, UP, buff=0.08)
            l2 = VGroup(zh("写", 26), sans("writing", 20)).arrange(RIGHT, buff=0.15).next_to(b2, UP, buff=0.08)
            self.play(GrowFromCenter(b1), FadeIn(l1), run_time=0.6)
            vo.wait_until("until the first character")
            split = Line(white[0].get_left() + LEFT * 0.04 + DOWN * 0.5, white[0].get_left() + LEFT * 0.04 + UP * 1.1,
                         color=USER_C, stroke_width=4)
            first = zh("答案的第一个字到达", 22, USER_C).next_to(split, DOWN, buff=0.1).align_to(split, RIGHT).shift(LEFT * 0.12)
            self.play(Create(split), FadeIn(first), run_time=0.5)
            vo.wait_until("Writing runs")
            self.play(GrowFromCenter(b2), FadeIn(l2), run_time=0.5)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 4 ---------------------------------------------------------------- effort, and two real receipts
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(form, first, split)), run_time=0.4)
            # same answer (14 white tokens), more or less thinking before it
            low = VGroup(zh("低", 24, S.GREY), tape(18, 4, size=0.2, buff=0.05)).arrange(RIGHT, buff=0.3)
            high = VGroup(zh("高", 24, S.GREY), tape(27, 13, size=0.2, buff=0.05)).arrange(RIGHT, buff=0.3)
            dial = VGroup(low, high).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(DOWN * 0.35 + LEFT * 1.3)
            eff = sans("effort", 22, S.GREY).next_to(dial, LEFT, buff=0.35)
            self.play(FadeIn(eff), FadeIn(low), run_time=0.5)
            self.play(FadeIn(high), run_time=0.5)
            vo.wait_until("Even on the same setting")
            g = phase_bars(1.6, 1.5, unit=0.36)
            c = phase_bars(13.5, 8.7, unit=0.36)
            gl = VGroup(zh("「你好」", 22, USER_C), g).arrange(RIGHT, buff=0.3)
            cl = VGroup(zh("「近期预约学校医疗中心」", 22, USER_C), c).arrange(RIGHT, buff=0.3)
            pair = VGroup(gl, cl).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(DOWN * 2.35)
            tagm = zh("gpt-6-luna · 思考强度 中 · 来自两张收据", 20, S.GREY).next_to(pair, DOWN, buff=0.18).align_to(pair, LEFT)
            vo.wait_until("1.6 seconds")
            self.play(FadeIn(gl[0]), GrowFromEdge(g.think, LEFT), GrowFromEdge(g.write, LEFT), FadeIn(g[2:]), run_time=0.6)
            vo.wait_until("for 13.5")
            self.play(FadeIn(cl[0]), GrowFromEdge(c.think, LEFT), GrowFromEdge(c.write, LEFT), FadeIn(c[2:]),
                      FadeIn(tagm), run_time=0.7)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(2.0)   # let the two real receipts sink in before the ponder

        # 5 ---------------------------------------------------------------- ponder
        with self.voiceover(SAY[4]) as vo:
            self.play(*[m.animate.set_opacity(0.15) for m in self.mobjects], run_time=0.4)
            card = ponder_zh(self, "If the thoughts are hidden, what are you paying for, and how would you know?",
                             "思考看不见，那你付的是什么钱？你怎么知道？", seconds=4.0)
        self.wait(3.5)

        # 6 ---------------------------------------------------------------- the usage report
        with self.voiceover(SAY[5]) as vo:
            clear(self, 0.4)
            usage = text_panel(["usage",
                                "  input_tokens            26,500",
                                "    cached_tokens         25,600",
                                "  output_tokens            1,000",
                                "    reasoning_tokens         150"], size=26, width=6.6,
                               colors={3: USER_C, 4: USER_C})
            usage.move_to(LEFT * 3.0 + UP * 0.5)
            note = sans("the typical turn server.ts assumes for prices · reasoning varies", 20, S.GREY).next_to(usage, DOWN, buff=0.2).align_to(usage, LEFT)
            self.play(FadeIn(usage, shift=UP * 0.1), FadeIn(note), run_time=0.7)
            vo.wait_until("counts the reasoning tokens")
            self.play(Circumscribe(VGroup(usage.rows[3], usage.rows[4]), color=USER_C), run_time=0.8)
            vo.wait_until("Our server reads it")
            server = ours_box("server", "reads usage", width=2.8).move_to(RIGHT * 2.2 + UP * 1.4)
            price = ours_box("price list", "pricing.ts", width=2.8).move_to(RIGHT * 2.2 + DOWN * 0.6)
            a1 = link(usage, server, OURS_C)
            self.play(FadeIn(server), Create(a1), run_time=0.6)
            vo.wait_until("the price list")
            a2 = link(server, price, OURS_C)
            self.play(FadeIn(price), Create(a2), run_time=0.6)
            vo.wait_until("dollar figure")
            cost = VGroup(zh("收据上的价钱", 24), Text("≈ $0.0009 on Luna", font=S.FONT, font_size=30, color=USER_C)
                          ).arrange(DOWN, buff=0.1).next_to(price, DOWN, buff=0.45)
            calc = sans("computed from the typical turn", 20, S.GREY).next_to(cost, DOWN, buff=0.1)
            self.play(FadeIn(cost, shift=UP * 0.1), FadeIn(calc), run_time=0.6)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(0.6)
        clear(self)
