"""S10 · Terminal 2: where to ask, and how.

1. `$env:CAREONEX_RETRIEVE_URL = "http://127.0.0.1:8080"` taken apart: http:// · 127.0.0.1 (this
   computer) · :8080 (the door). Without it: the tool says "knowledge base unavailable" (tools.py).
   READ IN CODE.
2. `$env:CAREONEX_VOICE_SEARCH_MODE = "feedback"`: a search of all four branches finds 0 results
   (MEASURED) → INFERRED: a switch inside Marco's new code.
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (BAD_C, CODE_C, NARRATION, PEOPLE, QUERY_C, big_line, code_panel, laptop, mono, sans, serif,
                    source_tag, text_panel)

SAY = NARRATION["S10"]


class VoiceSettings(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- the address of retrieve
        with self.voiceover(SAY[0]) as vo:
            line = big_line('$env:CAREONEX_RETRIEVE_URL = "http://127.0.0.1:8080"', 26).to_edge(UP, buff=0.45)
            self.play(FadeIn(line, shift=DOWN * 0.2), run_time=0.7)
            parts = VGroup(mono("http://", 44, S.GREY), mono("127.0.0.1", 44, QUERY_C), mono(":8080", 44, QUERY_C)
                           ).arrange(RIGHT, buff=0.1).move_to(UP * 1.0)
            labs = VGroup(serif("a web address", 24, S.GREY), serif("this same computer", 24, QUERY_C),
                          serif("the door retrieve opened", 24, QUERY_C))
            for p, l in zip(parts, labs):
                l.next_to(p, DOWN, buff=0.25)
            labs[2].next_to(parts[2], DOWN, buff=0.85)
            vo.wait_until("127.0.0.1 always means")
            self.play(FadeIn(parts), run_time=0.7)
            self.play(LaggedStart(*[FadeIn(l) for l in labs], lag_ratio=0.4), run_time=1.4)
            vo.wait_until("Without this note")
            code = code_panel('if not RETRIEVE_URL:\n'
                              '    return {"error": "knowledge base unavailable", ...}', size=22, width=8.6)
            code.move_to(DOWN * 1.6)
            src = VGroup(mono("services/voice/nova_sonic/tools.py (shortened)", 20, S.GREY), source_tag("code")
                         ).arrange(RIGHT, buff=0.3).next_to(code, DOWN, buff=0.15).align_to(code, LEFT)
            self.play(FadeIn(code, shift=UP * 0.15), FadeIn(src), run_time=0.9)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- a setting that is not on GitHub
        with self.voiceover(SAY[1]) as vo:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
            line2 = big_line('$env:CAREONEX_VOICE_SEARCH_MODE = "feedback"', 28).to_edge(UP, buff=0.45)
            self.play(FadeIn(line2, shift=DOWN * 0.2), run_time=0.7)
            search = text_panel(['search "SEARCH_MODE" in nadirbt/careonex-agents',
                                 "  main                  0 results",
                                 "  data-retrieval        0 results",
                                 "  feat/sonic_with_rag   0 results",
                                 "  feat/prompt-tuning    0 results"], size=24, colors={0: S.GREY})
            search.move_to(UP * 0.6)
            for k in range(1, 5):
                search.rows[k][-8:].set_color(BAD_C)
            tag = source_tag("measured").next_to(search, RIGHT, buff=0.3).align_to(search, UP)
            vo.wait_until("We searched all four")
            self.play(FadeIn(search, shift=UP * 0.15), FadeIn(tag), run_time=1.0)
            vo.wait_until("So it belongs")
            marco = VGroup(sans("MARCO'S NEW WORK", 22, PEOPLE["Marco"]), serif("not on GitHub yet", 24, S.GREY)
                           ).arrange(DOWN, buff=0.08).next_to(search, DOWN, buff=0.5)
            self.play(FadeIn(marco, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("It probably switches")
            guess = VGroup(source_tag("inferred"),
                           serif("a switch that chooses how voice searches; \"feedback\" is one of its modes", 24, S.PURPLE)
                           ).arrange(RIGHT, buff=0.25).to_edge(DOWN, buff=0.5)
            if guess.width > 13:
                guess.scale_to_fit_width(13)
            self.play(FadeIn(guess), run_time=0.7)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.play(FadeOut(*self.mobjects), run_time=0.8)
