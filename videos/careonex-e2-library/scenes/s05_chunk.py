"""S05 · chunk → chunks/.

1. A tall bar "Program Guide · 22 pages · 51,856 characters" next to a short bar "one chunk ≈ 1,600";
   the tall bar is sliced into its 68 chunks.
2. The team's summary: its outline (H1 + 11 sections) → 12 chunks; the JACC chunk opens, with its
   heading path stamped on top (real text, chunk 0004 of the normalised Markdown).
3. Three rules: a table stays whole (a table bigger than the cap is split between rows, first row
   repeated) · aim 1,600, cap 2,800 · merge scraps under 200.
4. Chunks per document (20 bars, from checks/pipeline_report.json), counter → 232, median 854.
5. chunks/…/0004-74147252db63.md + .metadata.json (541 bytes) on a 1 KB meter.
"""

import statistics

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (BAD_C, CODE_C, DATA_C, NARRATION, OK_C, QUERY_C, REPORT, SERIES, bar_chart, chip,
                    container, doc_glyph, mono, sans, serif, store, text_panel)

import json

SAY = NARRATION["S05"]
CHUNKS = json.loads((SERIES / "checks" / "chunks_index.json").read_text())
SUMMARY = "nj_doas_2026_program_limits.md"

SHORT = {   # readable bar labels for the 20 documents
    "nj_doas_program_guide.pdf": "DoAS program guide (PDF)",
    "cms_10969_medicare_and_home_health_care.pdf": "Medicare home health booklet",
    "nj_dmahs_mltss_application_guidance_2026.pdf": "MLTSS application guidance",
    "nj_doas_2026_program_limits.md": "team summary 2026",
    "nj_doas_programs_side_by_side_2026.pdf": "DoAS side-by-side 2026",
    "nj_dmahs_mltss_overview.html": "MLTSS overview page",
    "medicare_home_health_services_coverage.html": "Medicare coverage page",
    "nj_doas_statewide_respite_brochure_en.pdf": "Respite brochure",
    "nj_doas_alzheimers_adult_day.html": "Alzheimer's adult day page",
    "va_aid_attendance_housebound.html": "VA aid & attendance page",
    "nj_dds_personal_care_assistant.html": "PCA page (DDS)",
    "nj_doas_jacc_brochure_en.pdf": "JACC brochure",
    "nj_doas_alzheimers_adult_day_brochure_en.pdf": "Adult day brochure",
    "nj_doas_pace.html": "PACE page",
    "nj_doas_pace_flyer_en.pdf": "PACE flyer",
    "va_homemaker_home_health_aide.html": "VA homemaker page",
    "nj_doas_jacc.html": "JACC page",
    "nj_doas_statewide_respite.html": "Respite page",
    "nj_doas_county_offices_adrc.html": "County offices page",
    "va_home_community_based_services.html": "VA community services page",
}


class Chunk(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- too big to hand over
        with self.voiceover(SAY[0]) as vo:
            H = 5.6
            guide = Rectangle(width=1.6, height=H, stroke_color=DATA_C, stroke_width=2).set_fill(DATA_C, 0.18)
            guide.move_to(LEFT * 3.2 + DOWN * 0.3)
            gl = VGroup(serif("DoAS program guide", 26), mono("22 pages · 51,856 characters", 22, S.GREY)
                        ).arrange(DOWN, buff=0.08).next_to(guide, UP, buff=0.2)
            one = Rectangle(width=1.6, height=H * 1600 / 51856, stroke_color=QUERY_C, stroke_width=2).set_fill(QUERY_C, 0.3)
            one.move_to(RIGHT * 3.6).align_to(guide, UP)
            ol = VGroup(serif("what a search should return", 26), mono("one passage ≈ 1,600 characters", 22, S.GREY)
                        ).arrange(DOWN, buff=0.08).next_to(one, UP, buff=0.2)
            ol.align_to(gl, UP)
            self.play(GrowFromEdge(guide, UP), FadeIn(gl), run_time=1.2)
            self.play(GrowFromEdge(one, UP), FadeIn(ol), run_time=0.8)
            vo.wait_until("So the chunk container")
            ch = container("chunk", None, width=2.4, name_size=30).next_to(guide, RIGHT, buff=0.6).shift(DOWN * 1.5)
            self.play(FadeIn(ch, shift=LEFT * 0.2), run_time=0.6)
            sizes = [c["chars"] for c in CHUNKS["chunks"] if c["file"] == "nj_doas_program_guide.pdf"]
            tot = sum(sizes)
            cuts, y = VGroup(), guide.get_top()[1]
            for sz in sizes[:-1]:
                y -= H * sz / tot
                cuts.add(Line([guide.get_left()[0], y, 0], [guide.get_right()[0], y, 0], color=DATA_C, stroke_width=1.5))
            self.play(LaggedStart(*[Create(c) for c in cuts], lag_ratio=0.03), run_time=2.0)
            n68 = mono("68 chunks", 28, DATA_C).next_to(guide, LEFT, buff=0.3)
            self.play(FadeIn(n68, shift=RIGHT * 0.2), run_time=0.6)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- headings start chunks
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(guide, gl, one, ol, cuts, n68, ch)), run_time=0.8)
            mine = [c for c in CHUNKS["chunks"] if c["file"] == SUMMARY]
            heads = ["# NJ home-care program limits for 2026"] + [
                "## " + c["heading_path"][-1].split(" (")[0].split(" 2026")[0] for c in mine[1:] if len(c["heading_path"]) > 1]
            seen, outline_lines = set(), []
            for h in heads:
                if h not in seen:
                    seen.add(h)
                    outline_lines.append(h)
            outline = text_panel(outline_lines, size=20, border=DATA_C, colors={0: S.WHITE})
            if outline.width > 7.2:
                outline.scale_to_fit_width(7.2)
            title = mono("team summary · 8,546 characters", 22, DATA_C).next_to(outline, UP, buff=0.15, aligned_edge=LEFT)
            VGroup(title, outline).to_edge(LEFT, buff=0.5).shift(DOWN * 0.1)
            self.play(FadeIn(title), FadeIn(outline, shift=UP * 0.2), run_time=1.0)
            cards = VGroup(*[RoundedRectangle(width=0.62, height=0.3 + 0.9 * c["chars"] / 1500, corner_radius=0.06,
                                              stroke_color=DATA_C, stroke_width=2).set_fill(DATA_C, 0.2) for c in mine])
            cards.arrange_in_grid(rows=2, buff=0.2, cell_alignment=DOWN).move_to(RIGHT * 4.3 + UP * 0.2)
            nums = VGroup(*[mono(f"{i}", 20, S.GREY).next_to(cd, DOWN, buff=0.06) for i, cd in enumerate(cards)])
            self.play(LaggedStart(*[TransformFromCopy(outline.rows[min(i, len(outline.rows) - 1)], cards[i])
                                    for i in range(len(cards))], lag_ratio=0.1), FadeIn(nums), run_time=2.0)
            twelve = mono("12 chunks", 28, DATA_C).next_to(cards, UP, buff=0.3)
            self.play(FadeIn(twelve), run_time=0.5)
            vo.wait_until("So the line")
            text = CHUNKS["texts"][f"{SUMMARY}#4"]
            path_line = "New Jersey home-care program limits for 2026 (curated summary) >"
            body = ["JACC (Jersey Assistance for Community Caregiving) 2026", "",
                    "- Who: New Jersey resident age 60 or older, living at home …",
                    "- Countable income limit 2026: $4,855 per month for an",
                    "  individual; $6,582 per month for a couple …"]
            assert "$4,855 per month for an individual" in text and text.startswith(path_line)
            panel = text_panel([path_line] + body, size=20, border=DATA_C,
                               colors={0: QUERY_C, 1: QUERY_C}, t2c={"$4,855": QUERY_C})
            if panel.width > 12.6:
                panel.scale_to_fit_width(12.6)
            panel.move_to(DOWN * 0.6)
            stamp = chip("heading path, stamped on every chunk", QUERY_C, 22, mono_font=False).next_to(panel, UP, buff=0.12).align_to(panel, LEFT)
            self.play(Indicate(cards[4], color=QUERY_C), run_time=0.6)
            self.play(FadeOut(VGroup(title, outline, nums, twelve)),
                      *[c.animate.set_opacity(0.25) for i, c in enumerate(cards) if i != 4], run_time=0.6)
            self.play(cards.animate.scale(0.7).to_edge(UP, buff=0.5), run_time=0.6)
            self.play(TransformFromCopy(cards[4], panel), FadeIn(stamp), run_time=1.0)
            self.play(Circumscribe(VGroup(panel.rows[1], panel.rows[4]), color=QUERY_C), run_time=1.2)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 3 ---------------------------------------------------------------- three more rules
        with self.voiceover(SAY[2]) as vo:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
            # rule A: tables
            tab = VGroup(*[Rectangle(width=2.2, height=0.24, stroke_color=DATA_C, stroke_width=1.5)
                           .set_fill(DATA_C, 0.35 if i == 0 else 0.12) for i in range(8)]).arrange(DOWN, buff=0)
            ta = VGroup(serif("a table stays whole", 26), tab).arrange(DOWN, buff=0.25)
            big = VGroup(*[Rectangle(width=2.2, height=0.24, stroke_color=DATA_C, stroke_width=1.5)
                           .set_fill(DATA_C, 0.35 if i == 0 else 0.12) for i in range(4)]).arrange(DOWN, buff=0)
            big2 = VGroup(big[0].copy(), *[Rectangle(width=2.2, height=0.24, stroke_color=DATA_C, stroke_width=1.5)
                                           .set_fill(DATA_C, 0.12) for _ in range(3)]).arrange(DOWN, buff=0)
            split = VGroup(big, big2).arrange(DOWN, buff=0.25)
            rep = serif("too big? split between rows,\nfirst row repeated", 22, S.GREY)
            tb = VGroup(split, rep).arrange(DOWN, buff=0.2)
            ruleA = VGroup(ta, tb).arrange(DOWN, buff=0.45)
            # rule B: size
            ax = Line(LEFT * 2.0, RIGHT * 2.0, color=S.GREY)
            tgt = VGroup(Line(UP * 0.3, DOWN * 0.3, color=OK_C, stroke_width=4).move_to(ax.point_from_proportion(1600 / 3000)),
                         mono("1,600", 22, OK_C)).arrange(DOWN, buff=0.08)
            tgt[0].move_to(ax.point_from_proportion(1600 / 3000))
            tgt[1].next_to(tgt[0], DOWN, buff=0.08)
            cap = VGroup(Line(UP * 0.3, DOWN * 0.3, color=BAD_C, stroke_width=4), mono("2,800", 22, BAD_C))
            cap[0].move_to(ax.point_from_proportion(2800 / 3000))
            cap[1].next_to(cap[0], DOWN, buff=0.08)
            ruleB = VGroup(serif("aim for 1,600 characters", 26), serif("cap 2,800", 26, BAD_C),
                           VGroup(ax, tgt, cap)).arrange(DOWN, buff=0.3)
            # rule C: scraps
            scrap = RoundedRectangle(width=0.5, height=0.3, corner_radius=0.05, stroke_color=DATA_C).set_fill(DATA_C, 0.2)
            nbr = RoundedRectangle(width=1.6, height=0.9, corner_radius=0.08, stroke_color=DATA_C).set_fill(DATA_C, 0.2)
            pair = VGroup(scrap, nbr).arrange(RIGHT, buff=0.5)
            ruleC = VGroup(serif("scraps under 200", 26), serif("merge into a neighbour", 26), pair).arrange(DOWN, buff=0.3)
            rules = VGroup(ruleA, ruleB, ruleC).arrange(RIGHT, buff=1.2, aligned_edge=UP).move_to(ORIGIN)
            if rules.height > 6.6:
                rules.scale_to_fit_height(6.6)
            self.play(FadeIn(ta, shift=UP * 0.2), run_time=0.8)
            vo.wait_until("Only a table bigger")
            self.play(FadeIn(tb, shift=UP * 0.2), run_time=0.9)
            self.play(Indicate(big2[0], color=QUERY_C), Indicate(big[0], color=QUERY_C), run_time=1.0)
            vo.wait_until("Long text")
            self.play(FadeIn(ruleB, shift=UP * 0.2), run_time=0.9)
            vo.wait_until("Scraps")
            self.play(FadeIn(ruleC, shift=UP * 0.2), run_time=0.8)
            self.play(scrap.animate.move_to(nbr.get_left() + RIGHT * 0.3), run_time=0.8)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 4 ---------------------------------------------------------------- 232
        with self.voiceover(SAY[3]) as vo:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
            rep_sorted = sorted(REPORT, key=lambda r: -r["chunks"])
            chart = bar_chart([r["chunks"] for r in rep_sorted], [SHORT[r["file"]] for r in rep_sorted],
                              width=5.6, bar_h=0.2, size=20, gap=0.06)
            if chart.height > 6.8:
                chart.scale_to_fit_height(6.8)
            chart.move_to(LEFT * 1.0 + DOWN * 0.05)
            total = ValueTracker(0)
            counter = always_redraw(lambda: VGroup(mono(f"{int(round(total.get_value()))}", 64, DATA_C),
                                                   serif("chunks", 30)).arrange(DOWN, buff=0.1).move_to(RIGHT * 5.0 + UP * 1.6))
            self.add(counter)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in chart], lag_ratio=0.08),
                      total.animate.set_value(sum(r["chunks"] for r in REPORT)), run_time=3.2)
            counter.clear_updaters()
            vo.wait_until("The two longest PDFs")
            half = SurroundingRectangle(VGroup(chart[0], chart[1]), color=QUERY_C, buff=0.06, corner_radius=0.06)
            pct = mono("108 / 232", 26, QUERY_C).next_to(counter, DOWN, buff=0.5)
            self.play(Create(half), FadeIn(pct), run_time=0.9)
            vo.wait_until("Most chunks")
            sizes = [c["chars"] for c in CHUNKS["chunks"]]
            med = int(statistics.median(sizes))
            mline = VGroup(serif("median chunk", 26), mono(f"{med} characters", 26, DATA_C),
                           serif("(target 1,600)", 22, S.GREY)).arrange(DOWN, buff=0.08).next_to(pct, DOWN, buff=0.6)
            self.play(FadeIn(mline, shift=UP * 0.15), run_time=0.8)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 5 ---------------------------------------------------------------- one object per chunk; the 1 KB trap
        with self.voiceover(SAY[4]) as vo:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
            prefix = "chunks/careonex_curated/nj_doas_2026_program_limits.md/"
            objs = VGroup(store(prefix + "0004-74147252db63.md", "the chunk text (919 characters)", tag="S3 object",
                                width=12.4, name_size=24, sub_size=22),
                          store(prefix + "0004-74147252db63.md.metadata.json", "its sidecar", tag="S3 object",
                                width=12.4, name_size=24, sub_size=22)).arrange(DOWN, buff=0.3).move_to(UP * 1.0)
            self.play(FadeIn(objs[0], shift=DOWN * 0.2), run_time=0.7)
            self.play(FadeIn(objs[1], shift=DOWN * 0.2), run_time=0.7)
            vo.wait_until("That sidecar must stay")
            bar = Rectangle(width=8.0, height=0.4, stroke_color=S.GREY, stroke_width=2).move_to(DOWN * 1.4)
            fill = Rectangle(width=8.0 * 541 / 1024, height=0.4, stroke_width=0).set_fill(DATA_C, 0.8)
            fill.align_to(bar, LEFT).move_to([bar.get_left()[0] + fill.width / 2, bar.get_y(), 0])
            lim = VGroup(Line(UP * 0.4, DOWN * 0.4, color=BAD_C, stroke_width=5).move_to(bar.get_right()),
                         mono("1,024 bytes: Bedrock's limit", 22, BAD_C))
            lim[1].next_to(lim[0], UP, buff=0.12)
            lim[1].align_to(lim[0], RIGHT)
            val = mono("541 bytes", 24, DATA_C).next_to(fill, UP, buff=0.12).align_to(fill, LEFT)
            self.play(Create(bar), GrowFromEdge(fill, LEFT), FadeIn(val), FadeIn(lim), run_time=1.2)
            vo.wait_until("Bedrock silently skips")
            over = Rectangle(width=8.0 * 1.25, height=0.4, stroke_width=0).set_fill(BAD_C, 0.5)
            over.move_to([bar.get_left()[0] + over.width / 2, bar.get_y(), 0])
            ghost = VGroup(over, VGroup(serif("a sidecar over 1 KB:", 26, BAD_C), serif("the chunk is skipped", 26, BAD_C)
                                        ).arrange(RIGHT, buff=0.2).next_to(bar, DOWN, buff=0.45).align_to(bar, LEFT))
            self.play(FadeIn(ghost), run_time=0.8)
            ok = VGroup(serif("… and the job still reports", 26, S.GREY), mono("COMPLETE", 26, OK_C)).arrange(RIGHT, buff=0.2)
            ok.next_to(ghost[1], DOWN, buff=0.3).align_to(bar, LEFT)
            self.play(FadeIn(ok), run_time=0.8)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.play(FadeOut(*self.mobjects), run_time=0.8)
