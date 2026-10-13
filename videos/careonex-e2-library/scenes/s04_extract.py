"""S04 · extract → text/.

1. Every source downloaded twice, seconds apart, with ingest's User-Agent (series checks/
   html_hashes.py): 8 PDFs identical and matching the source list; 11 web pages: 6 identical,
   5 different bytes the second time (NJ Medicaid MLTSS, JACC, the 3 VA pages).
2. The real differences: an nj.gov bot-protection script tag in one copy; va.gov nonces. Extracted
   text of all 5: identical (checks/text_hash_check.py).
3. extract: HTML → keep main region → strip → Markdown; PDF → pymupdf4llm → Markdown with tables.
   Output text/nj_doas/nj_doas_jacc.html.md + text_sha256.
4. Three versions of the HTML converter (EXTRACTOR_VERSION comment in convert.py): v1 trafilatura
   dropped eligibility paragraphs; v2 strip-navigation-first emptied nj.gov (main inside a navbar);
   v3 main region first, then strip.
5. A PDF table row → a Markdown table row (the Side-by-Side table, real extracted text).
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (BAD_C, CATALOG, CODE_C, DATA_C, NARRATION, OK_C, QUERY_C, chip, container,
                    doc_glyph, link, mark_bad, mark_ok, mono, sans, serif, source_tag, store, text_panel, what_is)

SAY = NARRATION["S04"]
CHANGED = {"nj_dmahs_mltss_overview.html", "nj_doas_jacc.html", "va_homemaker_home_health_aide.html",
           "va_home_community_based_services.html", "va_aid_attendance_housebound.html"}


def glyph_row(names, color=DATA_C, per_row=11):
    g = VGroup(*[doc_glyph(color, 0.42, 0.56, lines=3) for _ in names])
    g.arrange_in_grid(cols=per_row, buff=0.14)
    return g


class Extract(VoiceScene):
    def construct(self):
        pdfs = [r["file_name"] for r in CATALOG if r["kind"] == "pdf"]
        htmls = [r["file_name"] for r in CATALOG if r["kind"] == "html"]

        # 1 ---------------------------------------------------------------- download everything twice
        with self.voiceover(SAY[0]) as vo:
            head = VGroup(serif("every source, downloaded twice, seconds apart", 30),
                          serif("(with ingest's own settings · 2026-10-10)", 22, S.GREY)).arrange(DOWN, buff=0.1)
            head.to_edge(UP, buff=0.45)
            pg = glyph_row(pdfs)
            hg = glyph_row(htmls)
            pl = VGroup(mono("8", 30, DATA_C), serif("PDFs", 28)).arrange(RIGHT, buff=0.15)
            hl = VGroup(mono("11", 30, DATA_C), serif("web pages", 28)).arrange(RIGHT, buff=0.15)
            left = VGroup(pl, pg).arrange(DOWN, buff=0.3)
            right = VGroup(hl, hg).arrange(DOWN, buff=0.3)
            VGroup(left, right).arrange(DOWN, buff=1.3).next_to(head, DOWN, buff=0.5)
            mtag = source_tag("measured").next_to(head, RIGHT, buff=0.3)
            self.play(FadeIn(head), FadeIn(mtag), run_time=0.8)
            self.play(FadeIn(left), FadeIn(right), run_time=1.0)
            twice_p = pg.copy().set_opacity(0.35).shift(RIGHT * 0.12 + DOWN * 0.08)
            twice_h = hg.copy().set_opacity(0.35).shift(RIGHT * 0.12 + DOWN * 0.08)
            self.play(FadeIn(twice_p), FadeIn(twice_h), run_time=0.9)
            vo.wait_until("All 8 PDFs")
            ticks = VGroup(*[mark_ok(0.3).next_to(g, DOWN, buff=0.08) for g in pg])
            self.play(LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.1), run_time=1.0)
            same = serif("identical · same hash as the source list", 24, OK_C).next_to(ticks, DOWN, buff=0.12)
            self.play(FadeIn(same), run_time=0.6)
            vo.wait_until("But 5 of the 11")
            marks = VGroup()
            for name, g in zip(htmls, hg):
                marks.add((mark_bad(0.26) if name in CHANGED else mark_ok(0.3)).next_to(g, DOWN, buff=0.08))
            self.play(LaggedStart(*[Create(m) for m in marks], lag_ratio=0.08), run_time=1.4)
            for name, g in zip(htmls, hg):
                if name in CHANGED:
                    g.set_color(BAD_C)
            five = serif("5 changed between the two downloads", 24, BAD_C).next_to(marks, DOWN, buff=0.25)
            self.play(FadeIn(five), run_time=0.6)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- what changed
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(head, mtag, left, right, twice_p, twice_h, ticks, same, marks, five)), run_time=0.7)
            nj = VGroup(mono("nj.gov · JACC page", 24, S.GREY),
                        text_panel(['last line, copy 1:  <script src="/_Incapsula_Resource?SWJIYLWA=…&ns=2&cb=2100165996"',
                                    '                     async></script></body>',
                                    'last line, copy 2:  </body>'],
                                   size=20, colors={0: BAD_C, 1: BAD_C})).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            va = VGroup(mono("va.gov · Aid and Attendance page", 24, S.GREY),
                        text_panel(['copy 1:  <link nonce="7HvwosMSf37iNeR3ri6xtaqtQwYQGHnS" rel="preload" …',
                                    'copy 2:  <link nonce="l0oYR4qcPsCrCjKfC3jcXK199hVIrecJ" rel="preload" …',
                                    '         … and the same on dozens of other tags'],
                                   size=20, colors={0: BAD_C, 1: BAD_C, 2: S.GREY})).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            for g in (nj, va):
                if g.width > 13:
                    g.scale_to_fit_width(13)
            VGroup(nj, va).arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to(UP * 0.5)
            self.play(FadeIn(nj, shift=UP * 0.2), run_time=0.9)
            vo.wait_until("On va.gov")
            self.play(FadeIn(va, shift=UP * 0.2), run_time=0.9)
            vo.wait_until("So the hash")
            verdict = VGroup(serif("extracted text of all 5 pages:", 28), serif("identical", 28, OK_C)).arrange(RIGHT, buff=0.2)
            verdict.next_to(va, DOWN, buff=0.5)
            self.play(FadeIn(verdict, shift=UP * 0.15), run_time=0.8)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 3 ---------------------------------------------------------------- the extract container
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(nj, va, verdict)), run_time=0.6)
            ext = container("extract", "careonex_extract.convert", width=3.4, name_size=32, sub_size=20)
            ext.to_edge(UP, buff=0.45)
            self.play(FadeIn(ext, shift=DOWN * 0.2), run_time=0.6)
            y1, y2 = 0.9, -1.3
            h_in = VGroup(doc_glyph(DATA_C, 0.5, 0.66), mono("raw .html", 22)).arrange(DOWN, buff=0.1).move_to([-5.6, y1, 0])
            p_in = VGroup(doc_glyph(DATA_C, 0.5, 0.66), mono("raw .pdf", 22)).arrange(DOWN, buff=0.1).move_to([-5.6, y2, 0])
            s1 = chip("1  keep the main region", CODE_C, 22, mono_font=False).move_to([-2.2, y1, 0])
            s1.move_to([-2.75, y1, 0])
            s2 = chip("2  strip scripts, navigation, footer, forms", CODE_C, 22, mono_font=False)
            s2.next_to(s1, RIGHT, buff=0.45)
            p1 = chip("pymupdf4llm: headings + tables", CODE_C, 22, mono_font=False).move_to([-1.0, y2, 0])
            out = VGroup(doc_glyph(DATA_C, 0.5, 0.66), mono("Markdown", 22)).arrange(DOWN, buff=0.1).move_to([5.3, -0.2, 0])
            a1 = link(h_in, s1, S.GREY)
            a2 = link(s1, s2, S.GREY)
            a3 = link(s2, out, S.GREY)
            b1 = link(p_in, p1, S.GREY)
            b2 = link(p1, out, S.GREY)
            self.play(FadeIn(h_in), run_time=0.4)
            self.play(GrowArrow(a1.arrow), FadeIn(s1), run_time=0.6)
            self.play(GrowArrow(a2.arrow), FadeIn(s2), run_time=0.6)
            self.play(GrowArrow(a3.arrow), FadeIn(out), run_time=0.6)
            self.play(FadeIn(p_in), GrowArrow(b1.arrow), FadeIn(p1), run_time=0.7)
            self.play(GrowArrow(b2.arrow), run_time=0.5)
            vo.wait_until("written as Markdown")
            mdcard = what_is("Markdown", ["plain text with a few symbols for structure:", "# a heading      |a|table|row|"],
                             width=6.6, size=24).to_edge(DOWN, buff=0.45)
            self.play(FadeIn(mdcard, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("The hash of that text")
            self.play(FadeOut(mdcard), run_time=0.4)
            key = VGroup(store("text/nj_doas/nj_doas_jacc.html.md", None, tag="S3 object", width=6.4, name_size=24),
                         mono("+ text_sha256 · extractor_version 3 in its metadata", 20, S.GREY)).arrange(DOWN, buff=0.15)
            key.to_edge(DOWN, buff=0.45)
            self.play(FadeIn(key, shift=UP * 0.2), run_time=0.8)
            self.play(Indicate(key[1], color=QUERY_C), run_time=1.0)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 4 ---------------------------------------------------------------- three versions
        with self.voiceover(SAY[3]) as vo:
            self.play(*[FadeOut(m) for m in self.mobjects if m is not ext], run_time=0.6)
            rows = []
            specs = [("v1", "a library (trafilatura) guesses the main content", "dropped the eligibility paragraphs", BAD_C),
                     ("v2", "strip navigation first, then convert", "nj.gov's page sits inside its navigation bar → empty", BAD_C),
                     ("v3", "find the main region first, then strip", "keeps what a reader sees", OK_C)]
            for v, how, what, col in specs:
                r = VGroup(mono(v, 32, col), serif(how, 26), serif("→ " + what, 26, col)).arrange(RIGHT, buff=0.3)
                rows.append(r)
            for r in rows:     # the result goes on its own line, under the method
                r[2].next_to(r[1], DOWN, aligned_edge=LEFT, buff=0.12)
            tbl = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.85)
            tbl.move_to(DOWN * 0.2).to_edge(LEFT, buff=0.6)
            vtag = source_tag("code", "the EXTRACTOR_VERSION note in convert.py").next_to(ext, RIGHT, buff=0.4)
            self.play(FadeIn(vtag), run_time=0.4)
            for k, phrase in enumerate(["Version 1", "Version 2", "Version 3"]):
                vo.wait_until(phrase)
                self.play(FadeIn(rows[k][0]), FadeIn(rows[k][1], shift=RIGHT * 0.2), run_time=0.7)
                if k == 1:   # the nesting that broke v2
                    nest = VGroup(mono('<nav class="navbar">', 22, BAD_C), mono('  <main> … the whole page … </main>', 22),
                                  mono('</nav>', 22, BAD_C)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
                    nest.to_edge(DOWN, buff=0.55).to_edge(RIGHT, buff=0.8)
                    nest_box = SurroundingRectangle(nest, buff=0.15, corner_radius=0.1, color=S.GREY_DARK)
                    nest = VGroup(nest_box, nest)
                    self.play(FadeIn(nest), run_time=0.6)
                self.play(FadeIn(rows[k][2], shift=DOWN * 0.1), run_time=0.6)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 5 ---------------------------------------------------------------- a PDF table, kept as a table
        with self.voiceover(SAY[4]) as vo:
            self.play(*[FadeOut(m) for m in self.mobjects if m is not ext], run_time=0.6)
            src = VGroup(sans("DoAS PROGRAMS SIDE-BY-SIDE (2026) · PDF", 22, S.GREY),
                         VGroup(*[VGroup(RoundedRectangle(width=w, height=0.62, corner_radius=0.04,
                                                          stroke_color=S.GREY, stroke_width=1.5),
                                         serif(t, 22, c)) for w, t, c in
                                  [(3.3, "Service Limitations", S.WHITE), (2.5, "MLTSS / PACE …", S.GREY),
                                   (2.9, "Up to $1,090/mo.", QUERY_C), (1.8, "Varies …", S.GREY)]]
                                ).arrange(RIGHT, buff=0)).arrange(DOWN, buff=0.15)
            for cell in src[1]:
                cell[1].move_to(cell[0])
            src.move_to(UP * 1.3)
            md = text_panel(["|**Service Limitations**|Based on limitations as specified …|Up to $1,090/mo.|Varies …|"],
                            size=20, border=DATA_C, t2c={"Up to $1,090/mo.": QUERY_C})
            if md.width > 13:
                md.scale_to_fit_width(13)
            md.move_to(DOWN * 0.9)
            tag = mono("pymupdf4llm", 22, CODE_C).next_to(md, UP, buff=0.35)
            self.play(FadeIn(src, shift=DOWN * 0.2), run_time=0.8)
            vo.wait_until("It keeps headings")
            self.play(FadeIn(tag), TransformFromCopy(src[1], md), run_time=1.2)
            vo.wait_until("so a number stays")
            self.play(Circumscribe(md, color=QUERY_C), run_time=1.2)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.play(FadeOut(*self.mobjects), run_time=0.8)
