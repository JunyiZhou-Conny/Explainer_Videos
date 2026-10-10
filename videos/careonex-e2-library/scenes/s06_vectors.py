"""S06 · kb-sync → vectors.

1. One chunk (the team summary's JACC section) → ORANGE "Titan Text Embeddings v2" → a column of
   numbers labelled "1,024 numbers" (values illustrative: Titan is not called for this video).
2. A 2-D cartoon of the space ("1,024 directions, drawn in 2"): chunk dots in three topic clusters;
   two arrows from the origin and the angle between them, "cosine similarity = cos θ".
3. The stack (kb-sync/provision.py): S3 Vectors bucket ac215-program-vectors-<account-id>, index
   program-kb (1,024 · cosine · float32); Bedrock Knowledge Base ac215-program-kb; data source
   "chunks" over chunks/, chunking NONE.
4. Ingestion job 0 → 232 → COMPLETE; config/knowledge-base.json → (dim) retrieve: next episode.
5. Monthly floor (kb-sync README): S3 Vectors cents · Aurora pgvector ~$45 · OpenSearch Serverless
   ~$175; latency: S3 Vectors ~100–300 ms, OpenSearch tens of ms.
"""

import numpy as np
from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (AWS_C, BAD_C, CODE_C, DATA_C, NARRATION, OK_C, QUERY_C, aws, chip, container, dim,
                    doc_glyph, link, mono, sans, serif, store, text_panel)

SAY = NARRATION["S06"]


class Vectors(VoiceScene):
    def construct(self):
        rng = np.random.default_rng(7)

        # 1 ---------------------------------------------------------------- chunk → 1,024 numbers
        with self.voiceover(SAY[0]) as vo:
            kb = container("kb-sync", None, width=2.6, name_size=30).to_corner(UL, buff=0.4)
            self.play(FadeIn(kb), run_time=0.6)
            chunk = text_panel(["… > JACC (Jersey Assistance for",
                                "  Community Caregiving) 2026",
                                "- Who: New Jersey resident age 60",
                                "  or older, living at home …",
                                "- Countable income limit 2026:",
                                "  $4,855 per month …"], size=20, border=DATA_C, colors={0: QUERY_C, 1: QUERY_C})
            chunk.to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
            titan = aws("embedding model", "Titan Text", "Embeddings v2", width=2.8, name_size=26, sub_size=22)
            titan.move_to(RIGHT * 0.7 + DOWN * 0.3)
            vals = [f"{v:+.3f}" for v in rng.normal(0, 0.05, 9)]
            col = VGroup(*[mono(v, 22) for v in vals[:4]], mono("⋮", 26, S.GREY), *[mono(v, 22) for v in vals[4:6]])
            col.arrange(DOWN, buff=0.12)
            br = VGroup(mono("[", 72, S.GREY).stretch_to_fit_height(col.height + 0.3).next_to(col, LEFT, buff=0.08),
                        mono("]", 72, S.GREY).stretch_to_fit_height(col.height + 0.3).next_to(col, RIGHT, buff=0.08))
            vec = VGroup(br, col).move_to(RIGHT * 4.3 + DOWN * 0.3)
            n = VGroup(mono("1,024", 30, AWS_C), serif("numbers", 26)).arrange(RIGHT, buff=0.15).next_to(vec, UP, buff=0.25)
            note = serif("(values drawn for the picture)", 20, S.GREY).next_to(vec, DOWN, buff=0.2)
            a1 = link(chunk, titan, S.GREY)
            a2 = link(titan, vec, S.GREY)
            self.play(FadeIn(chunk, shift=RIGHT * 0.2), run_time=0.8)
            vo.wait_until("An embedding model")
            self.play(GrowArrow(a1.arrow), FadeIn(titan), run_time=0.8)
            self.play(GrowArrow(a2.arrow), FadeIn(vec), run_time=0.9)
            self.play(FadeIn(n, shift=DOWN * 0.1), FadeIn(note), run_time=0.6)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- directions and angles
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(chunk, titan, a1, a2, note)), VGroup(vec, n).animate.scale(0.6).to_corner(UR, buff=0.55),
                      run_time=0.8)
            origin = DOWN * 1.9 + LEFT * 1.0
            plane = VGroup(Line(origin + LEFT * 4.5, origin + RIGHT * 6.5, color=S.GREY_DARK),
                           Line(origin + DOWN * 1.2, origin + UP * 5.0, color=S.GREY_DARK))
            cap = serif("1,024 directions, drawn in 2", 24, S.GREY).to_edge(DOWN, buff=0.35)
            self.play(Create(plane), FadeIn(cap), run_time=0.8)
            clusters = [("JACC limits", 62, DATA_C), ("Medicare home health", 20, DATA_C), ("VA benefits", 120, DATA_C)]
            dots, labels, centers = VGroup(), VGroup(), []
            for name, ang, col in clusters:
                d = np.array([np.cos(np.radians(ang)), np.sin(np.radians(ang)), 0])
                c = origin + d * 3.8
                centers.append((ang, c))
                for _ in range(9):
                    jitter = rng.normal(0, 0.28, 3)
                    jitter[2] = 0
                    dots.add(Dot(c + jitter, radius=0.06, color=col))
                labels.add(serif(name, 24).next_to(c, UP if ang > 90 else RIGHT, buff=0.8 if ang > 90 else 0.45))
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.03), run_time=1.6)
            self.play(FadeIn(labels), run_time=0.7)
            vo.wait_until("and the angle")
            v1 = Arrow(origin, centers[0][1], buff=0, color=QUERY_C, stroke_width=4)
            v2 = Arrow(origin, centers[1][1], buff=0, color=S.WHITE, stroke_width=4)
            self.play(GrowArrow(v1), GrowArrow(v2), run_time=0.9)
            arc = Arc(radius=1.1, start_angle=np.radians(20), angle=np.radians(42), arc_center=origin, color=QUERY_C)
            th = MathTex(r"\theta", color=QUERY_C).move_to(origin + 1.45 * np.array([np.cos(np.radians(41)), np.sin(np.radians(41)), 0]))
            self.play(Create(arc), FadeIn(th), run_time=0.7)
            cs = VGroup(serif("cosine similarity", 28), MathTex(r"= \cos\theta", color=QUERY_C)).arrange(RIGHT, buff=0.2)
            cs.move_to(RIGHT * 4.4 + DOWN * 1.55)
            small = serif("small angle → similar meaning", 24, S.GREY).next_to(cs, DOWN, buff=0.2)
            self.play(FadeIn(cs), FadeIn(small), run_time=0.8)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 3 ---------------------------------------------------------------- the stack
        with self.voiceover(SAY[2]) as vo:
            self.play(*[FadeOut(m) for m in self.mobjects if m is not kb], run_time=0.7)
            idx = aws("s3 vectors index", "program-kb", "1,024 dims · cosine · float32", width=5.4, name_size=30, sub_size=22)
            vb = sans("in vector bucket ac215-program-vectors-<account-id>", 20, AWS_C)
            kbx = aws("bedrock knowledge base", "ac215-program-kb", "embeds with Titan v2", width=5.4, name_size=30,
                      sub_size=22)
            ds = store("chunks/", "data source · chunking: NONE", tag="data source", width=5.4, name_size=30, sub_size=22)
            idx.move_to(LEFT * 2.6 + DOWN * 2.0)
            vb.next_to(idx, DOWN, buff=0.12)
            kbx.move_to(LEFT * 2.6 + UP * 0.4)
            ds.move_to(RIGHT * 3.6 + UP * 0.4)
            self.play(FadeIn(idx, shift=UP * 0.2), FadeIn(vb), run_time=0.9)
            vo.wait_until("On top sits")
            l1 = link(kbx, idx, AWS_C, label="stores vectors in", label_side=RIGHT)
            self.play(FadeIn(kbx, shift=DOWN * 0.2), GrowArrow(l1.arrow), FadeIn(l1.label), run_time=1.0)
            l2 = link(ds, kbx, DATA_C, label="reads", label_side=UP)
            self.play(FadeIn(ds, shift=LEFT * 0.2), GrowArrow(l2.arrow), FadeIn(l2.label), run_time=1.0)
            vo.wait_until("Its own chunking")
            off = chip("Bedrock's own chunking: off", BAD_C, 24, mono_font=False).next_to(ds, DOWN, buff=0.3)
            why = serif("our chunk container already did it", 24, S.GREY).next_to(off, DOWN, buff=0.15)
            self.play(FadeIn(off), Indicate(ds.sub, color=QUERY_C), run_time=0.9)
            self.play(FadeIn(why), run_time=0.6)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 4 ---------------------------------------------------------------- ingestion, then the config
        with self.voiceover(SAY[3]) as vo:
            self.play(*[FadeOut(m) for m in self.mobjects if m is not kb], run_time=0.6)
            job = serif("ingestion job", 30).move_to(UP * 2.0)
            bar = RoundedRectangle(width=8, height=0.45, corner_radius=0.1, stroke_color=S.GREY).next_to(job, DOWN, buff=0.3)
            prog = ValueTracker(0.001)
            fill = always_redraw(lambda: Rectangle(width=8 * prog.get_value(), height=0.45, stroke_width=0)
                                 .set_fill(AWS_C, 0.8).align_to(bar, LEFT).set_y(bar.get_y()))
            cnt = always_redraw(lambda: mono(f"{int(232 * prog.get_value())} / 232 vectors", 26).next_to(bar, DOWN, buff=0.2))
            self.play(FadeIn(job), Create(bar), run_time=0.6)
            self.add(fill, cnt)
            self.play(prog.animate.set_value(1.0), run_time=2.4, rate_func=smooth)
            fill.clear_updaters()
            cnt.clear_updaters()
            done = mono("COMPLETE", 28, OK_C).next_to(bar, RIGHT, buff=0.3)
            if done.get_right()[0] > 6.5:
                done.next_to(cnt, DOWN, buff=0.15)
            self.play(FadeIn(done), run_time=0.5)
            vo.wait_until("Then it writes")
            cfg = text_panel(['config/knowledge-base.json', '{"knowledge_base_id": "…",',
                              ' "data_source_id": "…",', ' "index_name": "program-kb",',
                              ' "ingestion_status": "COMPLETE", …}'], size=22, border=DATA_C, colors={0: DATA_C})
            cfg.move_to(LEFT * 2.6 + DOWN * 1.9)
            ret = container("retrieve", "next episode", width=2.8, name_size=30, sub_size=22).move_to(RIGHT * 4.2 + DOWN * 1.9)
            dim(ret, 0.5)
            self.play(FadeIn(cfg, shift=UP * 0.2), run_time=0.9)
            l3 = link(cfg, ret, CODE_C, label="reads the id", label_side=UP)
            self.play(FadeIn(ret), GrowArrow(l3.arrow), FadeIn(l3.label), run_time=1.0)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 5 ---------------------------------------------------------------- why S3 Vectors
        with self.voiceover(SAY[4]) as vo:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
            head = serif("vector store: monthly minimum", 32).to_edge(UP, buff=0.5)
            opts = [("S3 Vectors", 0.3, "cents", OK_C), ("Aurora pgvector", 45, "~$45", S.GREY),
                    ("OpenSearch Serverless", 175, "~$175", S.GREY)]
            rows = VGroup()
            for name, v, lab, col in opts:
                bar_ = Rectangle(width=max(0.06, 6.6 * v / 175), height=0.45, stroke_width=0).set_fill(col, 0.85)
                rows.add(VGroup(mono(name, 24), bar_, mono(lab, 24, col)))
            lw = max(r[0].width for r in rows)
            for i, r in enumerate(rows):
                r[0].move_to([-6.2 + lw - r[0].width / 2, 1.3 - i * 0.9, 0])
                r[1].move_to([-6.2 + lw + 0.3 + r[1].width / 2, r[0].get_y(), 0])
                r[2].next_to(r[1], RIGHT, buff=0.15)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.3), run_time=1.6)
            pick = SurroundingRectangle(rows[0], color=OK_C, buff=0.12, corner_radius=0.08)
            self.play(Create(pick), run_time=0.6)
            vo.wait_until("The price is speed")
            lat = VGroup(serif("time per search", 28),
                         VGroup(mono("S3 Vectors", 24), mono("~100–300 ms", 24, QUERY_C)).arrange(RIGHT, buff=0.3),
                         VGroup(mono("OpenSearch", 24), mono("tens of ms", 24, S.GREY)).arrange(RIGHT, buff=0.3)
                         ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to(DOWN * 2.0)
            self.play(FadeIn(lat, shift=UP * 0.2), run_time=0.9)
            vo.wait_until("and on a phone call")
            phone = serif("the team's target: a turn under 1 second", 26, S.GREY).next_to(lat, RIGHT, buff=0.8)
            if phone.get_right()[0] > 6.5:
                phone.next_to(lat, DOWN, buff=0.25)
            self.play(FadeIn(phone), Indicate(lat[1][1], color=QUERY_C), run_time=1.0)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.play(FadeOut(*self.mobjects), run_time=0.8)
