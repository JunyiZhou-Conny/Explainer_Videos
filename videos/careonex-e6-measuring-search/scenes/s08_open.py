"""S08 · Fixes, and what is still open.

1. E2's table that hid its program names, on Marco's branch:
   chunker B repeats the header row → the $1,090 chunk names JACC ✓ (MEASURED, table_chunk_check.py);
   new extractor (v5, doas_tables.py) fails on the real PDF: 9 columns where it needs 7 (empty spacer
   columns), and on pages 3-4 a header row split in two ✗ (MEASURED, doas_pages.py);
   retrieve drops side-by-side chunks without table_verified → the table does not reach the agent (READ IN CODE).
2. Voice safety (READ IN CODE): phone number saved only after readback + "yes"; one search per lookup;
   blank or malformed results are never evidence.
3. Open list, incl. the public account and library IDs (INFERRED: worth a team decision).
4. Test yourself. 5. Closing map.
"""

from manim import *

from explainer import style as S
from explainer.components import ponder_card
from explainer.scene import VoiceScene

from common import (BAD_C, CHUNKERS, CODE_C, DATA_C, GUESS_C, MARCO_C, NARRATION, OK_C, QUERY_C, container, mark_bad,
                    mark_ok, mono, sans, serif, source_tag, system_map, text_panel)

SAY = NARRATION["S08"]


def step_row(n: int, who: str, color: str) -> VGroup:
    return VGroup(mono(str(n), 30, QUERY_C), container(who, None, width=1.9, name_size=24)).arrange(RIGHT, buff=0.25)


class OpenItems(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- the E2 table, three steps
        with self.voiceover(SAY[0]) as vo:
            hdr = VGroup(sans("E2'S OPEN ITEM 3: THE TABLE THAT HID ITS PROGRAM NAMES", 22, QUERY_C)).to_edge(UP, buff=0.4)
            self.play(FadeIn(hdr), run_time=0.6)
            recap = VGroup(serif("E2: the chunk with", 30), mono('"Up to $1,090/mo."', 28, QUERY_C),
                           serif("never said", 30), mono('"JACC"', 28, BAD_C)).arrange(RIGHT, buff=0.2)
            three = serif("Marco's branch: three changes, three steps of the pipeline", 26, S.GREY).next_to(recap, DOWN, buff=0.35)
            self.play(FadeIn(recap, shift=UP * 0.1), run_time=0.8)
            vo.wait_until("Marco's branch attacks it")
            self.play(FadeIn(three), run_time=0.6)
            # step 1: chunk
            s1 = step_row(1, "chunk", CODE_C)
            hdr_row = text_panel(["|Field|MLTSS/PACE|JACC|SRCP|AADSP|CHSP|OAA|", "|Service Limitations|…|Up to $1,090/mo.|…"],
                                 size=22, border=DATA_C, t2c={"JACC": QUERY_C, "$1,090": QUERY_C})
            r1 = VGroup(s1, serif("B repeats the header row:", 26), hdr_row).arrange(RIGHT, buff=0.3)
            ok1 = VGroup(mark_ok(0.35), source_tag("measured")).arrange(RIGHT, buff=0.15)
            # step 2: extract
            s2 = step_row(2, "extract", CODE_C)
            cells = ["", "MLTSS/PACE", "JACC", "SRCP", "AADSP", "CHSP", "", "OAA", ""]
            row = VGroup()
            for c in cells:
                box = Rectangle(width=1.0 if c else 0.45, height=0.42, stroke_color=BAD_C if not c else S.GREY,
                                stroke_width=2).set_fill(BAD_C if not c else DATA_C, 0.25 if not c else 0.1)
                t = mono(c, 16) if c else VGroup()
                if c:
                    t.move_to(box)
                    if t.width > 0.92:
                        t.scale_to_fit_width(0.92)
                row.add(VGroup(box, t))
            row.arrange(RIGHT, buff=0)
            need = VGroup(serif("real PDF, page 2:", 24, S.GREY), row).arrange(RIGHT, buff=0.2)
            r2 = VGroup(s2, need).arrange(RIGHT, buff=0.3)
            bad2 = VGroup(mark_bad(0.3), serif("finds 9 columns where it needs 7 · fails on all 4 pages", 24, BAD_C),
                          source_tag("measured")).arrange(RIGHT, buff=0.15)
            # step 3: retrieve
            s3 = step_row(3, "retrieve", CODE_C)
            r3 = VGroup(s3, serif("drops every side-by-side chunk the extractor did not verify", 26),
                        source_tag("code")).arrange(RIGHT, buff=0.3)
            rows = VGroup(r1, r2, r3).arrange(DOWN, buff=0.75, aligned_edge=LEFT)
            if rows.width > 13:
                rows.scale_to_fit_width(13)
            rows.move_to(UP * 0.1)
            ok1.next_to(r1, DOWN, buff=0.1).align_to(r1[1], LEFT)
            bad2.next_to(r2, DOWN, buff=0.1).align_to(r2[1], LEFT)
            vo.wait_until("The new chunker fixes it")
            self.play(FadeOut(recap), FadeOut(three), run_time=0.5)
            self.play(FadeIn(r1, shift=RIGHT * 0.15), run_time=0.9)
            vo.wait_until("now says JACC")
            self.play(FadeIn(ok1), Indicate(hdr_row.rows[0], color=QUERY_C), run_time=0.8)
            vo.wait_until("A new extractor")
            self.play(FadeIn(r2, shift=RIGHT * 0.15), run_time=0.9)
            vo.wait_until("because it finds nine columns")
            empties = VGroup(*[row[i][0] for i, c in enumerate(cells) if not c])
            self.play(Indicate(empties, color=BAD_C, scale_factor=1.2), FadeIn(bad2), run_time=1.0)
            vo.wait_until("And retrieve now drops")
            self.play(FadeIn(r3, shift=RIGHT * 0.15), run_time=0.9)
            vo.wait_until("So for now")
            res = VGroup(serif("for now the table does not reach the agent;", 26, BAD_C),
                         serif("the team summary still carries its numbers", 26, S.GREY)).arrange(RIGHT, buff=0.2)
            if res.width > 13:
                res.scale_to_fit_width(13)
            res.to_edge(DOWN, buff=0.45)
            self.play(FadeIn(res), run_time=0.7)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- voice safety
        with self.voiceover(SAY[1]) as vo:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
            hdr = VGroup(sans("ON THE VOICE SIDE", 22, QUERY_C), source_tag("code")).arrange(RIGHT, buff=0.3).to_edge(UP, buff=0.4)
            convo = VGroup(
                VGroup(sans("AGENT", 18, CODE_C), serif('"I have 2 0 1, 5 5 5, 0 1 2 3. Is that right?"', 28)).arrange(RIGHT, buff=0.25),
                VGroup(sans("CALLER", 18, S.WHITE), serif('"Yes."', 28, QUERY_C)).arrange(RIGHT, buff=0.25),
                VGroup(mark_ok(0.32), mono("save_intake: callback number", 24, OK_C)).arrange(RIGHT, buff=0.2),
            ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(UP * 0.9)
            src = mono("services/voice/nova_sonic/intake_confirmation.py", 20, S.GREY).next_to(convo, DOWN, buff=0.3).align_to(convo, LEFT)
            fake = serif("(made-up number)", 20, S.GREY).next_to(convo[0], RIGHT, buff=0.2)
            self.play(FadeIn(hdr), run_time=0.5)
            self.play(FadeIn(convo[0]), FadeIn(fake), run_time=0.7)
            vo.wait_until("and the caller says yes")
            self.play(FadeIn(convo[1]), run_time=0.5)
            self.play(FadeIn(convo[2]), FadeIn(src), run_time=0.6)
            vo.wait_until("And empty search results")
            more = VGroup(serif("· blank or malformed search results are never presented as evidence", 26),
                          serif("· one search per lookup (an age in the question no longer doubles it)", 26, S.GREY)
                          ).arrange(DOWN, buff=0.18, aligned_edge=LEFT).to_edge(DOWN, buff=0.8)
            if more.width > 13:
                more.scale_to_fit_width(13)
            self.play(FadeIn(more, shift=UP * 0.1), run_time=0.8)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 3 ---------------------------------------------------------------- what is open
        with self.voiceover(SAY[2]) as vo:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
            hdr = sans("WHAT IS OPEN", 22, BAD_C).to_edge(UP, buff=0.4)
            items = [("grade the 40-question feedback run", "ideally without knowing which mode produced which passage", "grade the feedback run"),
                     ("decide whether the merge should let new passages in", "S05: today it can only reorder", "Decide whether the merge"),
                     ("fix the extractor for the real PDF", "drop empty spacer columns; join a header split over two rows", "Fix the extractor"),
                     ("choose the live library", "none of this is in the main library yet; rebuilding it needs team approval", "Decide which library"),
                     ("public IDs", "the branch puts the AWS account number and library IDs in a public repository", "And note that the branch")]
            rows = VGroup()
            for i, (t, sub, _) in enumerate(items, 1):
                col = GUESS_C if i == 5 else S.WHITE
                rows.add(VGroup(mono(str(i), 26, BAD_C), VGroup(serif(t, 28, col), serif(sub, 21, S.GREY)
                                                                  ).arrange(DOWN, buff=0.05, aligned_edge=LEFT)).arrange(RIGHT, buff=0.3, aligned_edge=UP))
            rows.arrange(DOWN, buff=0.28, aligned_edge=LEFT)
            if rows.width > 12.6:
                rows.scale_to_fit_width(12.6)
            rows.next_to(hdr, DOWN, buff=0.35)
            self.play(FadeIn(hdr), run_time=0.4)
            for (t, sub, anchor), r in zip(items, rows):
                vo.wait_until(anchor)
                self.play(FadeIn(r, shift=RIGHT * 0.15), run_time=0.6)
            guess = VGroup(source_tag("inferred"),
                           serif("not a password, but the setup guide kept them out: worth a team decision", 21, GUESS_C)
                           ).arrange(RIGHT, buff=0.2).next_to(rows, DOWN, buff=0.25).align_to(rows, LEFT)
            if guess.get_bottom()[1] < -3.85:
                guess.shift(UP * (-3.85 - guess.get_bottom()[1]))
            self.play(FadeIn(guess), run_time=0.5)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 4 ---------------------------------------------------------------- test yourself
        with self.voiceover(SAY[3]) as vo:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
            card = ponder_card("1. Why can a search with a perfect MRR still have a low precision?\n"
                               "2. Why can today's extra search reorder the top 5 but not add to it?\n"
                               "3. Why is high word similarity not proof of a correct answer?",
                               width=12.4, size=28)
            card[1].become(serif("Test yourself", 26, QUERY_C).move_to(card[1]))
            self.play(FadeIn(card, scale=0.95), run_time=0.7)
            bar = card[3]
            target = bar.copy().scale(0.001, about_point=bar.get_start())
            self.play(bar.animate(rate_func=linear).become(target), run_time=max(1.0, vo.remaining() - 0.3))

        # 5 ---------------------------------------------------------------- next
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(card), run_time=0.5)
            m = system_map()
            m.build.set_opacity(0.25)
            self.play(FadeIn(m), run_time=1.0)
            self.play(Indicate(m.part["retrieve"].frame, color=QUERY_C), run_time=1.0)
            nxt = VGroup(serif("Next", 26, S.GREY),
                         VGroup(serif("E3 · Finding the right passage", 32, QUERY_C),
                                serif("E4 · The voice loop", 32, QUERY_C)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
                         ).arrange(RIGHT, buff=0.3)
            nxt.move_to(LEFT * 2.6 + DOWN * 0.3)
            bg = SurroundingRectangle(nxt, buff=0.2, corner_radius=0.12, color=QUERY_C).set_fill(S.BG, 0.95)
            vo.wait_until("episode 4")
            self.play(FadeIn(bg), FadeIn(nxt), run_time=0.8)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.play(FadeOut(*self.mobjects), run_time=1.0)
