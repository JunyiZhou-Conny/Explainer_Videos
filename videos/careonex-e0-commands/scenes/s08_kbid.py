"""S08 · Which library? CAREONEX_KB_ID.

1. The line (KB id masked); an ORANGE Knowledge Base box with an ID badge; inside, GREEN chunks →
   vectors (as in E2). READ IN CODE.
2. retrieve/config.py knowledge_base_id(): the sticky note first, else config/knowledge-base.json
   from the S3 bucket. READ IN CODE.
3. Our two guesses (INFERRED), then Marco's branch settles it (READ IN CODE): his README line
   "# example staging KB" → library C, one of three test libraries (E6); the second guess gets a ✓.
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (AWS_C, DATA_C, KB_ID_MASKED, NARRATION, OK_C, PEOPLE, QUERY_C, aws, big_line, code_panel,
                    container, doc_glyph, mark_ok, mono, sans, serif, source_tag, sticky, store)

SAY = NARRATION["S08"]


class KnowledgeBaseId(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- what a knowledge base is
        with self.voiceover(SAY[0]) as vo:
            line = big_line(f'$env:CAREONEX_KB_ID = "{KB_ID_MASKED}"', 28).to_edge(UP, buff=0.45)
            masked = serif("(masked here: this repository is public)", 20, S.GREY).next_to(line, DOWN, buff=0.1)
            self.play(FadeIn(line, shift=DOWN * 0.2), FadeIn(masked), run_time=0.8)
            kb = RoundedRectangle(width=9.0, height=3.4, corner_radius=0.2, stroke_color=AWS_C, stroke_width=3).set_fill(AWS_C, 0.06)
            kb.move_to(DOWN * 1.0)
            kbt = VGroup(sans("BEDROCK KNOWLEDGE BASE", 22, AWS_C), serif("e.g. the team's, ac215-program-kb", 24, S.GREY)).arrange(RIGHT, buff=0.4)
            kbt.next_to(kb, UP, buff=0.12).align_to(kb, LEFT)
            docs = VGroup(*[doc_glyph(DATA_C, 0.42, 0.56) for _ in range(6)]).arrange(RIGHT, buff=0.12)
            docs.move_to(kb.get_center() + LEFT * 2.6 + DOWN * 0.3)
            dl = serif("232 passages", 22, DATA_C).next_to(docs, DOWN, buff=0.15)
            arr = Arrow(docs.get_right(), docs.get_right() + RIGHT * 1.6, buff=0.15, color=S.GREY, stroke_width=3)
            dots = VGroup(*[Dot(radius=0.06, color=AWS_C) for _ in range(14)])
            dots.arrange_in_grid(rows=2, buff=0.18).next_to(arr, RIGHT, buff=0.2)
            vl = serif("searchable as numbers", 22, AWS_C).next_to(dots, DOWN, buff=0.2)
            self.play(Create(kb), FadeIn(kbt), run_time=0.9)
            self.play(FadeIn(docs), FadeIn(dl), run_time=0.7)
            self.play(GrowArrow(arr), LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.05), FadeIn(vl), run_time=1.2)
            vo.wait_until("Every knowledge base has an ID")
            badge = VGroup(sans("ID", 20, QUERY_C), mono(KB_ID_MASKED, 26, QUERY_C)).arrange(RIGHT, buff=0.2)
            bbox = SurroundingRectangle(badge, buff=0.12, corner_radius=0.08, color=QUERY_C)
            badge = VGroup(bbox, badge).next_to(kb, RIGHT, buff=-1.6).align_to(kb, DOWN).shift(UP * 0.25)
            badge.move_to(kb.get_corner(DR) + LEFT * 1.4 + UP * 0.4)
            tag = source_tag("code").next_to(kb, DOWN, buff=0.15).align_to(kb, LEFT)
            self.play(FadeIn(badge, scale=1.2), FadeIn(tag), run_time=0.8)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- where retrieve gets it
        with self.voiceover(SAY[1]) as vo:
            self.play(*[FadeOut(m) for m in self.mobjects if m is not line], run_time=0.6)
            code = code_panel('def knowledge_base_id() -> str:\n'
                              '    """CAREONEX_KB_ID wins; otherwise read what kb-sync published."""\n'
                              '    env = os.environ.get("CAREONEX_KB_ID")\n'
                              '    if env:\n'
                              '        return env\n'
                              '    body = s3.get_object(Bucket=bucket_name(),\n'
                              '                         Key="config/knowledge-base.json")["Body"].read()\n'
                              '    return json.loads(body)["knowledge_base_id"]', size=20, width=10.0)
            code.move_to(UP * 0.4)
            src = VGroup(mono("services/retrieve/careonex_retrieve/config.py (shortened)", 20, S.GREY), source_tag("code")
                         ).arrange(RIGHT, buff=0.3).next_to(code, DOWN, buff=0.15).align_to(code, LEFT)
            self.play(FadeIn(code, shift=UP * 0.2), FadeIn(src), run_time=1.0)
            note = sticky("CAREONEX_KB_ID", KB_ID_MASKED, 22).move_to(LEFT * 4.2 + DOWN * 2.5)
            file = store("config/knowledge-base.json", "written by kb-sync", tag="in the S3 bucket", width=4.6,
                         name_size=22, sub_size=20).move_to(RIGHT * 3.4 + DOWN * 2.5)
            n1 = mono("1st", 26, QUERY_C).next_to(note, UP, buff=0.12)
            n2 = mono("2nd", 26, S.GREY).next_to(file, UP, buff=0.12)
            self.play(FadeIn(note), FadeIn(n1), run_time=0.7)
            vo.wait_until("If it is missing")
            self.play(FadeIn(file), FadeIn(n2), run_time=0.7)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 3 ---------------------------------------------------------------- why set it by hand?
        with self.voiceover(SAY[2]) as vo:
            self.play(*[FadeOut(m) for m in self.mobjects if m is not line], run_time=0.6)
            q = serif("Why set it by hand?", 36).move_to(UP * 2.0)
            self.play(FadeIn(q), run_time=0.6)
            r1 = VGroup(source_tag("inferred"), serif("skip one read from storage", 28, S.PURPLE)).arrange(DOWN, buff=0.2)
            r2 = VGroup(source_tag("inferred"), serif("point at a different knowledge base,", 28, S.PURPLE),
                        serif("e.g. one built for Marco's experiments", 28, S.PURPLE)).arrange(DOWN, buff=0.12)
            VGroup(r1, r2).arrange(RIGHT, buff=1.6, aligned_edge=UP).move_to(UP * 0.6)
            or_ = serif("or", 30, S.GREY).move_to([(r1.get_right()[0] + r2.get_left()[0]) / 2, r1.get_y(), 0])
            vo.wait_until("We had guessed")
            self.play(FadeIn(r1, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("or to point retrieve")
            self.play(FadeIn(or_), FadeIn(r2, shift=UP * 0.15), run_time=0.8)
            vo.wait_until("Marco's branch, pushed later")
            readme = VGroup(VGroup(mono("README.md", 20, S.GREY), mono("feat/sonic_with_rag_updated", 20, PEOPLE["Marco"]),
                                   source_tag("code")).arrange(RIGHT, buff=0.25),
                            mono(f'$env:CAREONEX_KB_ID = "{KB_ID_MASKED}"  # example staging KB', 24, QUERY_C)
                            ).arrange(DOWN, buff=0.12, aligned_edge=LEFT).to_edge(DOWN, buff=1.3)
            self.play(FadeIn(readme, shift=UP * 0.15), run_time=0.8)
            vo.wait_until("This ID is one of three")
            tick = mark_ok(0.45).next_to(r2, UP, buff=0.15)
            self.play(Create(tick), r1.animate.set_opacity(0.3), or_.animate.set_opacity(0.3),
                      Indicate(r2, color=OK_C, scale_factor=1.03), run_time=0.9)
            lib = serif("library C: one of three test libraries for comparing chunkers", 26).next_to(readme, DOWN, buff=0.25)
            lib.align_to(readme, LEFT)
            self.play(FadeIn(lib), run_time=0.6)
            vo.wait_until("Without this line")
            alt = serif("without the line → config/knowledge-base.json → the main library", 24, S.GREY).to_edge(DOWN, buff=0.3)
            self.play(FadeIn(alt), run_time=0.6)
            vo.wait_until("Episode 6")
            e6 = VGroup(serif("more in", 24, S.GREY), serif("E6 · Measuring search", 28, QUERY_C)).arrange(RIGHT, buff=0.2)
            e6.next_to(lib, RIGHT, buff=0.8)
            if e6.get_right()[0] > 6.9:
                e6.next_to(readme, UP, buff=0.3).align_to(readme, RIGHT).shift(RIGHT * 1.5)
            self.play(FadeIn(e6), run_time=0.5)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.play(FadeOut(*self.mobjects), run_time=0.8)
