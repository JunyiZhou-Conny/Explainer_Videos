"""S07 · What is solid, what is open.

1. The five containers over their prefixes, each with its "skip if" key (run reports under snapshots/).
2. Open 1 (found while making this video): VA Home and Community Based Services → 560 characters,
   mostly the site menu (real extracted text); the page's service list is <ul class="flex-menu">.
3. Open 2: the JACC monthly service cap: JACC page "$1,156 per participant per month" vs. the 2026
   Side-by-Side table and the team summary "Up to $1,090/mo." — both 2026.
4. Open 3: the Side-by-Side chunk with $1,090 (chunk 5 of 12) starts with the group-title row only;
   the row with MLTSS/PACE · JACC · SRCP … stayed in chunk 0. Note: Caroline's notes said "lost in
   extraction"; they survive extraction, the split drops them.
4b. Update, same evening (Marco's branch, E6): chunker v4 names JACC in the $1,090 chunk ✓ (MEASURED);
   the new table reader fails on the real PDF ✗ (MEASURED); retrieve drops unverified table chunks
   (READ IN CODE). Open items 1 and 2 unchanged there.
5. Also open: no schedule; the team summary is updated by hand.
6. Ponder card: three questions.
7. Closing: the map; retrieve → Knowledge Base lit; "Next: E3 · Finding the right passage".
"""

import json

from manim import *

from explainer import style as S
from explainer.components import ponder_card
from explainer.scene import VoiceScene

from common import (AWS_C, BAD_C, CODE_C, DATA_C, NARRATION, OK_C, PEOPLE, QUERY_C, SERIES, chip,
                    container, mark_bad, mark_ok, mono, sans, serif, source_tag, store, system_map, text_panel)

SAY = NARRATION["S07"]
CHUNKS = json.loads((SERIES / "checks" / "chunks_index.json").read_text())


def open_tag(n: int, text: str, found: bool = False) -> VGroup:
    t = VGroup(mono(f"open {n}", 26, BAD_C), serif(text, 30)).arrange(RIGHT, buff=0.3)
    if found:
        t.add(source_tag("measured", "found while making this video").next_to(t, RIGHT, buff=0.3))
    if t.width > 13:
        t.scale_to_fit_width(13)
    return t.to_edge(UP, buff=0.45).set_x(0)


class OpenItems(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- two habits
        with self.voiceover(SAY[0]) as vo:
            names = ["data", "ingest", "extract", "chunk", "kb-sync"]
            owns = ["(bucket)", "raw/", "text/", "chunks/", "config/"]
            keys = ["create if missing", "file hash", "file hash +\nextractor version", "text hash +\nchunker version",
                    "get or create"]
            cols = VGroup()
            for n, o, k in zip(names, owns, keys):
                c = container(n, None, width=2.35, name_size=28)
                p = store(o, None, tag="writes", width=2.35, name_size=26)
                kk = VGroup(sans("SKIP IF UNCHANGED", 18, S.GREY) if n not in ("data", "kb-sync") else sans("IDEMPOTENT", 18, S.GREY),
                            serif(k, 22, QUERY_C)).arrange(DOWN, buff=0.08)
                cols.add(VGroup(c, p, kk).arrange(DOWN, buff=0.35))
            cols.arrange(RIGHT, buff=0.22).move_to(UP * 0.2)
            note = serif("+ each run's report under snapshots/", 24, S.GREY).next_to(cols, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(VGroup(c[0], c[1]), shift=UP * 0.2) for c in cols], lag_ratio=0.15), run_time=1.6)
            self.play(FadeIn(note), run_time=0.5)
            vo.wait_until("And each one skips")
            self.play(LaggedStart(*[FadeIn(c[2], shift=UP * 0.1) for c in cols], lag_ratio=0.15), run_time=1.4)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- open 1: the VA page
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(cols, note)), run_time=0.6)
            tag = open_tag(1, "a page that loses its content", found=True)
            if tag.width > 13:
                tag.scale_to_fit_width(13)
            self.play(FadeIn(tag, shift=DOWN * 0.15), run_time=0.7)
            vo.wait_until("Veterans Affairs")
            txt = CHUNKS["texts"]["va_home_community_based_services.html#0"].splitlines()
            shown = [ln for ln in txt if ln.strip()][:12]
            panel = text_panel(shown + ["…"], size=20, border=BAD_C)
            title = VGroup(mono("va_home_community_based_services.html → text", 22, S.GREY),
                           mono("560 characters · 2 chunks", 22, BAD_C)).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
            left = VGroup(title, panel).arrange(DOWN, buff=0.2, aligned_edge=LEFT).to_edge(LEFT, buff=0.6).shift(DOWN * 0.4)
            self.play(FadeIn(left, shift=UP * 0.2), run_time=1.0)
            vo.wait_until("Its list of services")
            html = text_panel(['<ul class="flex-menu">',
                               '  <li>… Adult Day Health Care …</li>',
                               '  <li>… Home Based Primary Care …</li>',
                               '  …',
                               '</ul>'], size=20, border=S.GREY_DARK, colors={0: BAD_C, 4: BAD_C})
            html.to_edge(RIGHT, buff=0.6).shift(UP * 0.6)
            rule = VGroup(serif('the strip rule: a small element whose', 22, S.GREY),
                          serif('class contains "menu" is a widget', 22, S.GREY)).arrange(DOWN, buff=0.06)
            rule.next_to(html, DOWN, buff=0.35)
            self.play(FadeIn(html, shift=LEFT * 0.2), run_time=0.9)
            self.play(FadeIn(rule), Indicate(html.rows[0], color=BAD_C), run_time=1.0)
            vo.wait_until("throws it away")
            x = Cross(html, stroke_color=BAD_C, stroke_width=5)
            self.play(Create(x), run_time=0.7)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 3 ---------------------------------------------------------------- open 2: two sources disagree
        with self.voiceover(SAY[2]) as vo:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
            tag = open_tag(2, "two 2026 sources disagree", found=True)
            if tag.width > 13:
                tag.scale_to_fit_width(13)
            self.play(FadeIn(tag, shift=DOWN * 0.15), run_time=0.7)
            a = VGroup(sans("JACC PAGE · nj.gov · 2026", 22, DATA_C),
                       text_panel(["JACC services are limited to", "$1,156 per participant", "per month, plus care management."],
                                  size=22, border=DATA_C, t2c={"$1,156": QUERY_C})).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
            b = VGroup(sans("2026 SIDE-BY-SIDE TABLE · TEAM SUMMARY", 22, DATA_C),
                       text_panel(["table, JACC column:", "  Up to $1,090/mo.", "summary: up to $1,090 per month"],
                                  size=22, border=DATA_C, t2c={"$1,090": QUERY_C})).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
            pair = VGroup(a, b).arrange(RIGHT, buff=1.2, aligned_edge=UP)
            if pair.width > 12.6:
                pair.scale_to_fit_width(12.6)
            pair.move_to(UP * 0.2)
            neq = mono("≠", 64, BAD_C).move_to(pair.get_center())
            self.play(FadeIn(a, shift=RIGHT * 0.2), run_time=0.8)
            vo.wait_until("The state's 2026")
            self.play(FadeIn(b, shift=LEFT * 0.2), run_time=0.8)
            self.play(FadeIn(neq, scale=1.3), run_time=0.5)
            vo.wait_until("Both are 2026")
            pol = VGroup(serif('retrieve\'s rule "prefer the newest year":', 26, S.GREY),
                         VGroup(mono("2026", 28), mono("vs", 26, S.GREY), mono("2026", 28)).arrange(RIGHT, buff=0.3),
                         serif("→ no winner", 26, BAD_C)).arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=0.7)
            if pol.width > 13:
                pol.scale_to_fit_width(13)
            self.play(FadeIn(pol, shift=UP * 0.2), run_time=0.9)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 4 ---------------------------------------------------------------- open 3: the table that hides its names
        with self.voiceover(SAY[3]) as vo:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
            tag = open_tag(3, "a table that hides its program names", found=True)
            if tag.width > 13:
                tag.scale_to_fit_width(13)
            self.play(FadeIn(tag, shift=DOWN * 0.15), run_time=0.7)
            row1 = ["2026", "MEDICAID WAIVER PROGRAM", "", "", "NON-MEDICAID WAIVER", "PROGRAMS", ""]
            row2 = ["", "MLTSS/PACE", "JACC", "SRCP", "AADSP", "CHSP", "OAA"]
            row3 = ["Service Limitations", "Based on …", "Up to $1,090/mo.", "Varies …", "5 days/wk", "Varies …", "…"]
            widths = [2.6, 2.1, 2.3, 1.2, 1.6, 1.5, 1.3]

            def table_row(cells, colors, fill=0.0):
                g = VGroup()
                for w, t, col in zip(widths, cells, colors):
                    box = Rectangle(width=w, height=0.5, stroke_color=S.GREY_DARK, stroke_width=1.5).set_fill(DATA_C, fill)
                    lab = serif(t, 20, col) if t else VGroup()
                    if t and lab.width > w - 0.1:
                        lab.scale_to_fit_width(w - 0.1)
                    if t:
                        lab.move_to(box)
                    g.add(VGroup(box, lab))
                return g.arrange(RIGHT, buff=0)

            def group_row():
                spans = [(widths[0], "2026"), (sum(widths[1:4]), "MEDICAID WAIVER PROGRAM"),
                         (sum(widths[4:7]), "NON-MEDICAID WAIVER PROGRAMS")]
                g = VGroup()
                for w, t in spans:
                    box = Rectangle(width=w, height=0.5, stroke_color=S.GREY_DARK, stroke_width=1.5).set_fill(DATA_C, 0.25)
                    lab = serif(t, 20, S.GREY)
                    if lab.width > w - 0.15:
                        lab.scale_to_fit_width(w - 0.15)
                    lab.move_to(box)
                    g.add(VGroup(box, lab))
                return g.arrange(RIGHT, buff=0)

            r1 = group_row()
            r2 = table_row(row2, [S.WHITE, S.WHITE, QUERY_C, S.WHITE, S.WHITE, S.WHITE, S.WHITE])
            r3 = table_row(row3, [S.WHITE, S.GREY, QUERY_C, S.GREY, S.GREY, S.GREY, S.GREY])
            full = VGroup(r1, r2, r3).arrange(DOWN, buff=0).move_to(UP * 1.2)
            lab_full = sans("THE TABLE, AS EXTRACTED", 20, S.GREY).next_to(full, UP, buff=0.12).align_to(full, LEFT)
            self.play(FadeIn(lab_full), FadeIn(r1), run_time=0.6)
            self.play(FadeIn(r2), run_time=0.6)
            self.play(FadeIn(r3), run_time=0.6)
            vo.wait_until("They survive extraction")
            self.play(Indicate(r2, color=QUERY_C, scale_factor=1.02), run_time=1.0)
            vo.wait_until("But when the chunker")
            # chunk 5: first row repeated, then the row with $1,090; row 2 is not there
            c5_r1 = r1.copy()
            c5_r3 = r3.copy()
            chunk5 = VGroup(c5_r1, c5_r3).arrange(DOWN, buff=0).move_to(DOWN * 1.7)
            frame = SurroundingRectangle(chunk5, color=DATA_C, buff=0.12, corner_radius=0.08)
            lab5 = sans("CHUNK 5 OF 12", 20, DATA_C).next_to(frame, UP, buff=0.08).align_to(frame, LEFT)
            self.play(TransformFromCopy(r1, c5_r1), run_time=0.8)
            self.play(TransformFromCopy(r3, c5_r3), Create(frame), FadeIn(lab5), run_time=0.9)
            gap = mono('"JACC" appears nowhere in this chunk', 24, BAD_C).next_to(frame, DOWN, buff=0.2)
            vo.wait_until("So the chunk")
            self.play(FadeIn(gap), Indicate(c5_r3[2], color=QUERY_C), run_time=1.0)
            fix = serif("(Caroline's notes: \"lost in extraction\": they survive extraction; the split drops them)",
                        20, S.GREY).to_edge(DOWN, buff=0.3)
            if fix.width > 13:
                fix.scale_to_fit_width(13)
            self.play(FadeIn(fix), run_time=0.6)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 4b --------------------------------------------------------------- update: Marco's branch
        with self.voiceover(SAY[4]) as vo:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
            head = VGroup(sans("UPDATE, SAME EVENING", 22, QUERY_C), mono("feat/sonic_with_rag_updated", 24, PEOPLE["Marco"]),
                          serif("(details in E6)", 24, S.GREY)).arrange(RIGHT, buff=0.3).to_edge(UP, buff=0.45)
            self.play(FadeIn(head, shift=DOWN * 0.15), run_time=0.7)

            def upd(name, text, mark, tag):
                return VGroup(container(name, None, width=2.0, name_size=26), mark, serif(text, 26),
                              source_tag(tag)).arrange(RIGHT, buff=0.3)

            rows = VGroup(upd("chunk", "repeats the header row → the $1,090 chunk now says JACC", mark_ok(0.35), "measured"),
                          upd("extract", "new table reader: 9 columns on the real PDF, needs 7 → stops", mark_bad(0.28), "measured"),
                          upd("retrieve", "drops the table's chunks that were not verified", mono("→", 30, S.GREY), "code")
                          ).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
            if rows.width > 13:
                rows.scale_to_fit_width(13)
            rows.move_to(UP * 0.3)
            vo.wait_until("Its new chunker")
            self.play(FadeIn(rows[0], shift=RIGHT * 0.15), run_time=0.8)
            vo.wait_until("But his new table reader")
            self.play(FadeIn(rows[1], shift=RIGHT * 0.15), run_time=0.8)
            vo.wait_until("and retrieve now drops")
            self.play(FadeIn(rows[2], shift=RIGHT * 0.15), run_time=0.8)
            res = serif("for now the table does not reach the agent", 28, BAD_C).next_to(rows, DOWN, buff=0.5)
            self.play(FadeIn(res), run_time=0.6)
            vo.wait_until("Open items 1 and 2")
            same = VGroup(mono("open 1", 24, S.GREY), mono("open 2", 24, S.GREY), serif("unchanged on his branch", 26, S.GREY),
                          source_tag("measured")).arrange(RIGHT, buff=0.25).to_edge(DOWN, buff=0.5)
            self.play(FadeIn(same), run_time=0.6)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 5 ---------------------------------------------------------------- also open
        with self.voiceover(SAY[5]) as vo:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
            items = VGroup(VGroup(mono("open 4", 26, S.GREY), serif("nothing re-runs the pipeline on a schedule", 30)).arrange(RIGHT, buff=0.3),
                           VGroup(mono("open 5", 26, S.GREY), serif("the team summary is updated by hand (January, March)", 30)
                                  ).arrange(RIGHT, buff=0.3)).arrange(DOWN, buff=0.6, aligned_edge=LEFT)
            if items.width > 13:
                items.scale_to_fit_width(13)
            self.play(LaggedStart(*[FadeIn(i, shift=RIGHT * 0.2) for i in items], lag_ratio=0.5), run_time=1.4)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 6 ---------------------------------------------------------------- test yourself
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(items), run_time=0.5)
            card = ponder_card("1. Why does extract hash the text, not the downloaded file?\n"
                               "2. Why is the heading path stamped on every chunk?\n"
                               "3. One new PDF joins the list: which containers do real work on the next run?",
                               width=12.4, size=28)
            card[1].become(serif("Test yourself", 26, QUERY_C).move_to(card[1]))
            self.play(FadeIn(card, scale=0.95), run_time=0.7)
            bar = card[3]
            target = bar.copy().scale(0.001, about_point=bar.get_start())
            self.play(bar.animate(rate_func=linear).become(target), run_time=max(1.0, vo.remaining() - 0.3))

        # 7 ---------------------------------------------------------------- next episode
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(card), run_time=0.5)
            m = system_map()
            m.build.set_opacity(0.25)
            self.play(FadeIn(m), run_time=1.0)
            q = m.links["retrieve>kb"].arrow
            self.play(Indicate(m.part["retrieve"].frame, color=QUERY_C), q.animate.set_stroke(width=7), run_time=1.2)
            nxt = VGroup(serif("Next", 26, S.GREY), serif("E3 · Finding the right passage", 34, QUERY_C)).arrange(RIGHT, buff=0.3)
            nxt.move_to(LEFT * 2.6 + DOWN * 0.3)
            bg = SurroundingRectangle(nxt, buff=0.2, corner_radius=0.12, color=QUERY_C).set_fill(S.BG, 0.95)
            self.play(FadeIn(bg), FadeIn(nxt), run_time=0.8)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.play(FadeOut(*self.mobjects), run_time=1.0)
