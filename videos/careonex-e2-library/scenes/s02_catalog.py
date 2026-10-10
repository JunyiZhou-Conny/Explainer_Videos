"""S02 · The source list.

1. ragfile_list.csv: 20 rows (kind + file name) in two columns under a header strip.
2. The rows turn into 20 document glyphs grouped by publisher (DoAS 11, VA 3, NJ Medicaid 2,
   Medicare 2, NJ Disability 1, team summary 1); then the same 20 regroup by kind (11 web pages,
   8 PDFs, 1 Markdown).
3. The JACC page's row opens into a card; program, source_url, effective_date and sha256 light in turn.
4. The list slides into the BLUE data container ("image: careonex/data:local"); a new row is added
   and the image is rebuilt.
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (CATALOG, CODE_C, DATA_C, KINDS, NARRATION, PUBLISHERS, QUERY_C, chip, container,
                    doc_glyph, mono, sans, serif, source_tag, text_panel)

SAY = NARRATION["S02"]


def row_mob(r) -> VGroup:
    k = chip(r["kind"], DATA_C, size=20)
    k.bg.stretch_to_fit_width(0.82)
    k.label.move_to(k.bg)
    name = mono(r["file_name"], 20, S.WHITE).next_to(k, RIGHT, buff=0.18)
    return VGroup(k, name)


class Catalog(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- the spreadsheet
        with self.voiceover(SAY[0]) as vo:
            head = VGroup(mono("ragfile_list.csv", 30, DATA_C),
                          sans("20 rows · columns: source_id, program, source_url, kind, effective_date, sha256 …",
                               20, S.GREY)).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.4)
            rows = [row_mob(r) for r in CATALOG]
            left = VGroup(*rows[:10]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
            right = VGroup(*rows[10:]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
            cols = VGroup(left, right).arrange(RIGHT, buff=0.6, aligned_edge=UP)
            if cols.width > 13:
                cols.scale_to_fit_width(13)
            cols.next_to(head, DOWN, buff=0.45)
            self.play(FadeIn(head, shift=DOWN * 0.2), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.12), run_time=3.0)
            src = source_tag("code", "services/data/catalog/ragfile_list.csv").to_corner(DL, buff=0.35)
            self.play(FadeIn(src), run_time=0.4)
            self.wait(max(0.2, vo.remaining() - 0.3))

        # 2 ---------------------------------------------------------------- by publisher, then by kind
        with self.voiceover(SAY[1]) as vo:
            glyphs = [doc_glyph(DATA_C, 0.42, 0.56, lines=3) for _ in CATALOG]
            groups, labels = [], []
            for sid, lab in PUBLISHERS:
                idx = [i for i, r in enumerate(CATALOG) if r["source_id"] == sid]
                g = VGroup(*[glyphs[i] for i in idx]).arrange(RIGHT, buff=0.08)
                groups.append((idx, g, lab))
            band = VGroup(*[g for _, g, _ in groups]).arrange(RIGHT, buff=0.42).move_to(UP * 0.6)
            for k, (idx, g, lab) in enumerate(groups):
                t = VGroup(serif(lab, 24, S.WHITE), mono(str(len(idx)), 26, DATA_C)).arrange(DOWN, buff=0.08)
                t.next_to(g, DOWN, buff=0.3 if k % 2 == 0 else 1.25)
                tick = Line(g.get_bottom() + DOWN * 0.05, t.get_top() + UP * 0.05, color=S.GREY_DARK,
                            stroke_width=2)
                labels.append(VGroup(tick, t))
            self.play(FadeOut(head[1]), FadeOut(src),
                      LaggedStart(*[FadeOut(rows[i], target_position=glyphs[i].get_center(), scale=0.4)
                                    for i in range(len(rows))], lag_ratio=0.04),
                      LaggedStart(*[FadeIn(glyphs[i], scale=0.6) for i in range(len(rows))], lag_ratio=0.04),
                      run_time=1.8)
            self.play(LaggedStart(*[FadeIn(l, shift=UP * 0.1) for l in labels], lag_ratio=0.2), run_time=1.6)
            self.play(Indicate(groups[0][1], color=DATA_C, scale_factor=1.05), run_time=1.0)
            vo.wait_until("11 are web pages")
            # regroup the same glyphs by kind
            kind_groups, kind_labels = [], []
            for kind, lab in KINDS:
                idx = [i for i, r in enumerate(CATALOG) if r["kind"] == kind]
                kind_groups.append((idx, lab))
            targets = []
            for idx, lab in kind_groups:
                g = VGroup(*[glyphs[i].copy() for i in idx]).arrange(RIGHT, buff=0.08)
                targets.append(g)
            tband = VGroup(*targets).arrange(RIGHT, buff=0.7).move_to(UP * 0.6)
            anims = []
            for (idx, lab), g in zip(kind_groups, targets):
                for i, tgt in zip(idx, g):
                    anims.append(glyphs[i].animate.move_to(tgt))
                kl = VGroup(mono(str(len(idx)), 30, DATA_C), serif(lab, 28, S.WHITE)).arrange(RIGHT, buff=0.15)
                kl.next_to(g, DOWN, buff=0.35)
                kind_labels.append(kl)
            self.play(FadeOut(VGroup(*labels)), *anims, run_time=1.4)
            self.play(LaggedStart(*[FadeIn(k, shift=UP * 0.1) for k in kind_labels], lag_ratio=0.3), run_time=1.2)
            vo.wait_until("1 is a summary")
            md_glyph = glyphs[[i for i, r in enumerate(CATALOG) if r["kind"] == "md"][0]]
            self.play(Indicate(md_glyph, color=DATA_C, scale_factor=1.3), Indicate(kind_labels[2], color=DATA_C),
                      run_time=1.2)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 3 ---------------------------------------------------------------- one row, opened
        with self.voiceover(SAY[2]) as vo:
            jacc = [i for i, r in enumerate(CATALOG) if r["file_name"] == "nj_doas_jacc.html"][0]
            r = CATALOG[jacc]
            fields = [("source_id", r["source_id"]), ("program", r["program"]), ("kind", r["kind"]),
                      ("source_url", "nj.gov/humanservices/doas/…/jacc/"),
                      ("effective_date", r["effective_date"]), ("sha256", r["sha256"][:16] + "…")]
            lines = [f"{k:<15}{v}" for k, v in fields]
            card = text_panel(lines, size=24, border=DATA_C)
            for row, (k, _) in zip(card.rows, fields):
                row[:len(k)].set_color(S.GREY)
            name = mono(r["file_name"], 28, DATA_C)
            VGroup(name, card).arrange(DOWN, buff=0.25).move_to(DOWN * 0.2)
            others = VGroup(*[g for i, g in enumerate(glyphs) if i != jacc], *kind_labels)
            self.play(FadeOut(others), glyphs[jacc].animate.scale(1.5).next_to(name, LEFT, buff=0.3),
                      FadeIn(name), run_time=0.9)
            self.play(FadeIn(card, shift=DOWN * 0.2), run_time=0.8)
            marks = {"the program": 1, "the web address": 3, "the date": 4, "a fingerprint": 5}
            for phrase, k in marks.items():
                vo.wait_until(phrase)
                self.play(card.rows[k].animate.set_color(QUERY_C), run_time=0.4)
                self.play(card.rows[k].animate.set_color(S.WHITE), run_time=0.4)
                card.rows[k][:len(fields[k][0])].set_color(S.GREY)
            self.play(Circumscribe(card.rows[5], color=QUERY_C), run_time=1.0)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 4 ---------------------------------------------------------------- built into the image
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(card), FadeOut(name), FadeOut(glyphs[jacc]), FadeOut(head[0]), run_time=0.7)
            sheet = VGroup(doc_glyph(DATA_C, 0.9, 1.15, lines=6), mono("ragfile_list.csv", 26, DATA_C)).arrange(DOWN, buff=0.15)
            sheet.move_to(LEFT * 4)
            box = container("data", "careonex/data:local", width=5.2, height=2.2, name_size=40, sub_size=24)
            box.move_to(RIGHT * 2.6)
            only = serif("the pipeline's only input", 28, S.GREY).next_to(sheet, DOWN, buff=0.35)
            self.play(FadeIn(sheet, shift=UP * 0.2), FadeIn(only), run_time=0.8)
            self.play(FadeIn(box, shift=LEFT * 0.2), run_time=0.7)
            vo.wait_until("To add a document")
            new = VGroup(chip("+", DATA_C, size=24), mono("new_source.pdf", 22, S.WHITE)).arrange(RIGHT, buff=0.15)
            new.next_to(sheet, UP, buff=0.35)
            self.play(FadeIn(new, shift=DOWN * 0.2), run_time=0.7)
            self.play(new.animate.move_to(sheet[0]).scale(0.3).set_opacity(0), run_time=0.7)
            vo.wait_until("because the list")
            inside = sheet.copy()
            self.play(inside[0].animate.scale(0.6).move_to(box.frame.get_right() + LEFT * 0.75),
                      FadeOut(inside[1]), run_time=1.0)
            rebuild = VGroup(serif("rebuild the image", 26, CODE_C), mono("docker compose build", 22, S.GREY)).arrange(DOWN, buff=0.1)
            rebuild.next_to(box, DOWN, buff=0.35)
            self.play(FadeIn(rebuild), Indicate(box.frame, color=CODE_C, scale_factor=1.03), run_time=1.0)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.play(FadeOut(*self.mobjects), run_time=0.8)
