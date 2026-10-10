"""S08 · Which library? CAREONEX_KB_ID.

1. The line (KB id masked); an ORANGE Knowledge Base box with an ID badge; inside, GREEN chunks →
   vectors (as in E2). READ IN CODE.
2. retrieve/config.py knowledge_base_id(): the sticky note first, else config/knowledge-base.json
   from the S3 bucket. READ IN CODE.
3. INFERRED: two possible reasons side by side; "settles it: Marco's branch".
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (AWS_C, DATA_C, KB_ID_MASKED, NARRATION, QUERY_C, aws, big_line, code_panel, container,
                    doc_glyph, mono, sans, serif, source_tag, sticky, store)

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
            q = serif("Why set it by hand?", 36).move_to(UP * 1.6)
            self.play(FadeIn(q), run_time=0.6)
            r1 = VGroup(source_tag("inferred"), serif("skip one read from storage", 28, S.PURPLE)).arrange(DOWN, buff=0.2)
            r2 = VGroup(source_tag("inferred"), serif("point at a different knowledge base,", 28, S.PURPLE),
                        serif("e.g. one built for Marco's experiments", 28, S.PURPLE)).arrange(DOWN, buff=0.12)
            VGroup(r1, r2).arrange(RIGHT, buff=1.6, aligned_edge=UP).move_to(DOWN * 0.2)
            or_ = serif("or", 30, S.GREY).move_to([(r1.get_right()[0] + r2.get_left()[0]) / 2, r1.get_y(), 0])
            vo.wait_until("It saves one read")
            self.play(FadeIn(r1, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("Or Marco points")
            self.play(FadeIn(or_), FadeIn(r2, shift=UP * 0.15), run_time=0.8)
            vo.wait_until("His code will tell us")
            settle = VGroup(sans("WHAT WOULD SETTLE IT", 20, S.GREY), serif("Marco's branch, once it is pushed", 28)
                            ).arrange(DOWN, buff=0.1).to_edge(DOWN, buff=0.6)
            self.play(FadeIn(settle, shift=UP * 0.15), run_time=0.7)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.play(FadeOut(*self.mobjects), run_time=0.8)
