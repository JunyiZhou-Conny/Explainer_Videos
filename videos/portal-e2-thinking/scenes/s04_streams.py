"""S04 · Two kinds of streaming

1. A typical chat app: model → page, words travel as they are written (token streaming, SSE).
2. Ours: model → server (SSE in); the words stop at the server, which tracks the box and the character
   count; server → page: only NDJSON progress lines, in the real TriageStreamEvent shapes.
3. Those lines become the page's text: 「正在思考 · 11 秒」 → 「正在写回答 · 去处和步骤 · 已写 320 字」
   (the design doc's example) → 「正在检查」 → the answer.
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (CHECKED_C, MODEL_C, NARRATION, OURS_C, TEXT_C, chip, clear, link, model_box, ours_box,
                    page_box, quote_panel, sans, screen, tag_box, text_panel, thinking_line, zh)

SAY = NARRATION["S04"]
# the real TriageStreamEvent shapes (apiTypes.ts); "…" stands for fields left out (model, mode, attempt)
EVENTS = ['{"type":"start","effort":"medium",…}',
          '{"type":"stage","stage":"thinking",…}',
          '{"type":"progress","section":"options",',
          ' "chars":320,"emergency":false,…}',
          '{"type":"stage","stage":"checking",…}',
          '{"type":"result","response":{…}}']
WORDS = ["孩子", "可以", "先", "去", "学校", "医疗", "中心", "……"]


def flow(scene, words, start, end, color=TEXT_C, run_time=1.2, mono_font=False):
    """Small text pieces travelling from start to end, one after another."""
    pieces = [(Text(w, font="Noto Sans CJK SC", font_size=22, color=color) if not mono_font
               else Text(w, font="DejaVu Sans Mono", font_size=20, color=color)) for w in words]
    anims = []
    for k, p in enumerate(pieces):
        p.move_to(start)
        anims.append(Succession(FadeIn(p, run_time=0.1), p.animate(run_time=run_time, rate_func=linear).move_to(end),
                                FadeOut(p, run_time=0.1)))
    scene.play(LaggedStart(*anims, lag_ratio=0.25), run_time=run_time + 0.25 * len(pieces))


class TwoStreams(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- a typical chat app
        with self.voiceover(SAY[0]) as vo:
            why = quote_panel("干等 10–30 秒，人不知道在发生什么。", "decision 0006 · 10-28 addendum", width=8.0, size=32)
            vo.wait_until("puts it plainly")
            self.play(FadeIn(why, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("Most chat apps")
            self.play(FadeOut(why), run_time=0.4)
            head = sans("a typical chat app", 24, S.GREY).move_to(UP * 3.3 + LEFT * 4.6)
            m = model_box("the model", None, width=2.6).move_to(LEFT * 4.6 + UP * 2.2)
            p = tag_box("chat app", "page", None, S.GREY, width=2.6, fill=0.0).move_to(RIGHT * 4.6 + UP * 2.2)
            a = link(m, p, S.GREY, label="token streaming · server-sent events (SSE)", label_size=20)
            self.play(FadeIn(head), FadeIn(m), FadeIn(p), Create(a), run_time=0.8)
            vo.wait_until("every few words")
            flow(self, WORDS, m.get_right() + RIGHT * 0.3, p.get_left() + LEFT * 0.3, run_time=1.4)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- ours: the words stop at the server
        with self.voiceover(SAY[1]) as vo:
            head2 = sans("ours", 24, OURS_C).move_to(UP * 0.55 + LEFT * 5.4)
            m2 = model_box("gpt-6-luna", "OpenAI", width=2.4).move_to(LEFT * 5.4 + DOWN * 0.6)
            srv = ours_box("server", "reads the form as it fills", width=3.2).move_to(LEFT * 0.7 + DOWN * 0.6)
            pg = page_box(width=2.2).move_to(RIGHT * 5.5 + DOWN * 0.6)
            a1 = link(m2, srv, MODEL_C, label="SSE: words", label_size=20)
            a2 = link(srv, pg, OURS_C, label="NDJSON: progress", label_size=20)
            self.play(FadeIn(head2), FadeIn(m2), FadeIn(srv), FadeIn(pg), Create(a1), run_time=0.8)
            vo.wait_until("does not pass the words on")
            flow(self, WORDS[:6], m2.get_right() + RIGHT * 0.3, srv.get_center(), run_time=1.0)
            stop = sans("the words stop here", 20, S.RED).next_to(srv, DOWN, buff=0.2)
            self.play(FadeIn(stop), run_time=0.3)
            vo.wait_until("notes which box")
            readout = chip("box: options · 320 字", OURS_C, 22).next_to(srv, UP, buff=0.25)
            self.play(FadeIn(readout, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("sends the page only progress")
            ndj = zh("每行一个 JSON", 20, OURS_C).next_to(a2.arrow, DOWN, buff=0.12)
            self.play(Create(a2), FadeIn(ndj), run_time=0.5)
            flow(self, ["{…stage…}", "{…progress…}", "{…progress…}"], srv.get_right() + RIGHT * 0.3,
                 pg.get_left() + LEFT * 0.3, color=OURS_C, run_time=1.0, mono_font=True)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 3 ---------------------------------------------------------------- what the page makes of them
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(head, m, p, a, head2, m2, a1, stop, readout, ndj)),
                      VGroup(srv, a2, pg).animate.shift(UP * 3.2), run_time=0.7)
            events = text_panel(EVENTS, size=21).move_to(DOWN * 0.9).to_edge(LEFT, buff=0.55)
            tag = sans("the real event shapes (apiTypes.ts)", 20, S.GREY).next_to(events, DOWN, buff=0.12).align_to(events, LEFT)
            self.play(FadeIn(events), FadeIn(tag), run_time=0.6)
            scr = screen(5.5, 3.4).move_to(RIGHT * 3.75 + DOWN * 0.9)
            lines = [thinking_line(11),
                     zh("正在写回答 · 去处和步骤 · 已写 320 字", 21, S.GREY),
                     zh("正在检查", 24, S.GREY),
                     zh("检查过的回答", 24, CHECKED_C)]
            for ln in lines:
                if ln.width > 5.2:
                    ln.scale_to_fit_width(5.2)
                ln.move_to(scr)
            example = sans("example from docs/design/README.md", 20, S.GREY).next_to(scr, DOWN, buff=0.12)
            self.play(FadeIn(scr), run_time=0.3)
            shown = None
            for i, (ln, row, phrase) in enumerate(zip(lines, [[1], [2, 3], [4], [5]],
                                                      ["thinking, eleven", "Writing the places", "Checking", "never sees a word"])):
                vo.wait_until(phrase)
                anims = [Indicate(VGroup(*[events.rows[r] for r in row]), color=OURS_C, scale_factor=1.02)]
                anims.append(FadeIn(ln) if shown is None else ReplacementTransform(shown, ln))
                if i == 1:
                    anims.append(FadeIn(example))
                self.play(*anims, run_time=0.5)
                shown = ln
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.wait(0.6)
        clear(self)
