"""S10 · Terminal 2: where to ask, and how.

1. `$env:CAREONEX_RETRIEVE_URL = "http://127.0.0.1:8080"` taken apart: http:// · 127.0.0.1 (this
   computer) · :8080 (the door). Without it: the tool says "knowledge base unavailable" (tools.py).
   READ IN CODE.
2. `$env:CAREONEX_VOICE_SEARCH_MODE = "feedback"`: the four branches on GitHub that morning: 0 results
   (MEASURED). Marco's branch (READ IN CODE): tools.py reads it, default "feedback"; "baseline" = one
   search only. Our earlier guess (a switch for how voice searches) gets a ✓.
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (BAD_C, CODE_C, NARRATION, OK_C, PEOPLE, QUERY_C, big_line, code_panel, laptop, mark_ok, mono,
                    sans, serif, source_tag, text_panel)

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

        # 2 ---------------------------------------------------------------- the search-mode note, settled
        with self.voiceover(SAY[1]) as vo:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
            line2 = big_line('$env:CAREONEX_VOICE_SEARCH_MODE = "feedback"', 28).to_edge(UP, buff=0.45)
            self.play(FadeIn(line2, shift=DOWN * 0.2), run_time=0.7)
            vo.wait_until("When we first looked")
            search = text_panel(['morning: search "SEARCH_MODE" in nadirbt/careonex-agents',
                                 "  main, data-retrieval, feat/sonic_with_rag,",
                                 "  feat/prompt-tuning        0 results"], size=22, colors={0: S.GREY})
            search.rows[2][-8:].set_color(BAD_C)
            search.move_to(UP * 1.3 + LEFT * 0.8)
            tag = source_tag("measured").next_to(search, RIGHT, buff=0.3).align_to(search, UP)
            self.play(FadeIn(search, shift=UP * 0.15), FadeIn(tag), run_time=0.9)
            vo.wait_until("Marco's branch, pushed later")
            code = code_panel('mode = os.environ.get("CAREONEX_VOICE_SEARCH_MODE", "feedback")', size=22, width=11.0)
            src = VGroup(mono("feat/sonic_with_rag_updated · services/voice/nova_sonic/tools.py", 20, PEOPLE["Marco"]),
                         source_tag("code")).arrange(RIGHT, buff=0.3)
            ev = VGroup(src, code).arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to(DOWN * 0.3)
            self.play(search.animate.set_opacity(0.35), tag.animate.set_opacity(0.35), FadeIn(ev, shift=UP * 0.15),
                      run_time=0.9)
            vo.wait_until("Feedback runs a first search")
            modes = VGroup(VGroup(mono('"feedback"', 26, QUERY_C), serif("first search, maybe one more, merged", 26)
                                  ).arrange(RIGHT, buff=0.3),
                           VGroup(mono('"baseline"', 26, S.WHITE), serif("one search only (the rollback switch)", 26)
                                  ).arrange(RIGHT, buff=0.3)).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
            modes.next_to(ev, DOWN, buff=0.45).align_to(ev, LEFT)
            self.play(FadeIn(modes[0], shift=RIGHT * 0.15), run_time=0.7)
            vo.wait_until("Baseline runs")
            self.play(FadeIn(modes[1], shift=RIGHT * 0.15), run_time=0.7)
            vo.wait_until("Feedback is also the default")
            self.play(Circumscribe(code, color=QUERY_C, buff=0.08), run_time=1.0)
            vo.wait_until("Episode 6")
            e6 = VGroup(mark_ok(0.35), serif("our guess: a switch for how voice searches", 24, OK_C),
                        serif("· more in E6", 24, QUERY_C)).arrange(RIGHT, buff=0.2).to_edge(DOWN, buff=0.4)
            self.play(FadeIn(e6), run_time=0.6)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.play(FadeOut(*self.mobjects), run_time=0.8)
