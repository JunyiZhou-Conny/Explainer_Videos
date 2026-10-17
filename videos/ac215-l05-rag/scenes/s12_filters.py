"""S12 · Filters come first (README "Query", step 2 still lit; every command here is an extra).
Lecture: A54–A55.

Beats (script.md "## S12", one voiceover block each):
 0  TRACKER Query 2 · extra. CODE(cli.py: 352–361): line 356 `n_results=10` (YELLOW bar), line 357
    `where={"book": ...}` and line 358 `where_document={"$contains": search_string}` (PINK-edged
    bars, line 353 `search_string = "Italian"` with them) highlight in turn; a PINK chip under the
    panel names each filter as the SAY does.
 1  V6, second half: the char-split collection as ~1,000 GREEN dots (GREY caption "char-split
    collection · 1 dot ≈ 8 chunks", tag "our illustration"); the PINK question card (top right)
    drops into the cloud as a PINK point inside the cluster labelled "Tolminc story". PONDER (8 s)
    in the lower third, the cloud above it.
 2  GREY card "an extra Python check · counts with the query's filters". Under the cloud a filter
    row: the counter "chunks: 8,248"; the PINK chip "book = The Complete Book of Cheese" appears and
    the mask dims all but the book's dots (1,355); the PINK chip `$contains "Italian"` appears and
    the mask dims all but 64 brighter dots (caption "64 bright dots = 64 chunks"). The card gives
    way to the 3-row container strip: recorded-embeddings/08 lines 13–15 (the tag "recorded · the
    staff's vectors (68e0bde)" on the strip's top right); line 14 boxed YELLOW and a YELLOW
    "mentioning Tolminc: 0" on the fully dimmed Tolminc cluster.
 3  After "Now a search." the picture leaves; the strip grows to 11 rows; the card above it becomes
    "an extra Python check · query with a stored vector" (the staff tag moves up beside it); the
    question card becomes the tag "stand-in query · a stored story chunk's vector".
    TERM(recorded-embeddings/09: 16–17 word-folded, the chunk id PINK; then 18–28, "-- no filter"
    flashes): 0.0000 boxed with the GREY tag "itself", 0.1627 boxed YELLOW.
 4  The terminal clears: TERM(09: 29–39); the book names of the ten rows boxed YELLOW, 0.2833 and
    0.3123 boxed YELLOW. The terminal shrinks to the strip and the cloud returns unmasked: the PINK
    beam from the stand-in reaches its ten nearest, inside the Tolminc cluster. The mask returns,
    and the beam stretches past the dimmed cluster to the far, lit survivors, labelled "all 10: The
    Complete Book of Cheese" under the cloud; the long beam flashes ("however far").
 5  LECTURE A54–A55. The lecture's four-stage strip (Indexing → Vector Database → Querying → Post
    Processing) with the PINK-edged "metadata filter" under Post Processing: ten story result cards
    come out of Querying, slide through the filter and are all struck out: an empty list `[]`, RED
    "nothing left". The filter slides to before Querying; ten cards come out of Querying again and
    the GREY caption reads "Chroma: filter, then rank · 10 results, wrong cheese".
 6  CODE(cli.py: 325–331), the '#' column boxed GREY, tag "erratum"; README chip "README.md · line
    186" "Apply various types of filters"; GREY card "uncomment lines 326–331 / variant 4 still
    prints after it / needs your key / no rebuild: the code is mounted"; chip "$contains = keyword
    filter (case-sensitive) · not keyword ranking (later)".
 7  Container terminal (TEAL, 10 rows): `python cli.py --get --chunk_type char-split` (tag extra +
    GREY note "not in the README · cli.py · lines 402–418") -> recorded-embeddings/05 lines 2–3
    (word-folded) and line 6 cut after the ids list's "]" (word-folded), tag "recorded · the
    staff's vectors (68e0bde)", GREY note "no distances: no ranking". The terminal shrinks to a
    4-row strip holding the ids while copies of the ten ids become ten cards ("-0" … "-9") in a row
    beside a TEAL cylinder, bracketed "-0 to -2 / Gutenberg header" (RED), "-3 to -5 / title page,
    contents" (GREY), "-6 to -9 / chapter one begins" (GREEN); the RED cards flash, the cylinder
    pulses ("indexed like any text"); last, the GREEN fix card "strip outside the START/END markers /
    then chunk, embed, load again". Everything fades: empty frame.

Deviations from SHOW (see the scene report): the "extra Python check" cards are one-line GREY cards
with the SHOW's own wording (the two-line check_card does not fit above an 11-row terminal under
the tracker band). Beat 3 shows no picture: its beam (the ten nearest inside the Tolminc cluster)
opens beat 4's picture, so the unfiltered and the filtered beam are seen one after the other while
"The filters act first" is said, and beat 3's narration stays on the numbers it reads out. Beat 7's
terminal has 10 rows (the folded command, the folded Namespace line and the four ids rows need
10), and it shrinks to a 4-row strip so all ten ids stay on screen while they become cards; the
ten cards stand in a row beside the cylinder (ten cards stacked inside it would be 0.22 tall,
too small for their 20 pt labels). The `$contains` chip says "(later)" for "(S15)": scene numbers
are not on screen anywhere. Additions: PINK chips naming the two filters under the beat-0 panel
and the filter chips in beat 2's row (the SAY names them), "64 bright dots = 64 chunks" (the 64
brighter dots would contradict "1 dot ≈ 8 chunks"), ten result cards out of Querying in beat 5.
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Create,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    Line,
    ReplacementTransform,
    RoundedRectangle,
    ShowPassingFlash,
    Transform,
    VGroup,
)

from common import (
    BOOK,
    COUNTS,
    DATA,
    ERR,
    INK,
    LOOKUP,
    NARRATION,
    P_CTR2,
    STANDIN_ID,
    STRIP_TOP,
    TURN,
    Counter,
    DotCloud,
    StageStrip,
    beside,
    capture,
    caption_extra,
    card_rows,
    chunk_card,
    col_box,
    cylinder,
    erratum_tag,
    excerpt,
    extra_tag,
    grey_tag,
    grid_x0,
    lref,
    note,
    our_illustration_tag,
    pin,
    ponder_at,
    question_card,
    readme_chip,
    resize,
    sans,
    src_panel,
    staff_tag,
    standin_tag,
    term,
    tracker,
    type_cmd,
    under,
)
from explainer import style as S
from explainer.devops import CAPTION, MONO, cell_width, chip, cross_mark, mono, substring
from explainer.scene import VoiceScene

SAY = NARRATION["S12"]

PONDER_Q = ("The question is about Tolminc.\n"
            "The query keeps one book, and only chunks containing 'Italian'.\n"
            "What will the ten results be about?")


# ------------------------------------------------------------------ the real captures
def word_fold(s: str, n: int = 65) -> list[str]:
    """A long output line folded at spaces into rows of at most n characters (no token is cut)."""
    rows, cur = [], ""
    for w in s.split(" "):
        if cur and len(cur) + 1 + len(w) > n:
            rows.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}" if cur else w
    rows.append(cur)
    assert all(len(r) <= n for r in rows), rows
    return rows


CNT = capture("08", "recorded-embeddings")              # the counts with the query's filters
assert CNT.line(11).split() == ["all", "chunks:", str(COUNTS["char-split"])], CNT.line(11)
assert CNT.line(13).endswith("$contains 'Italian':    64") and CNT.line(14).endswith("'Tolminc':    0")
assert CNT.line(15).startswith("any book, $contains 'Tolminc':") and CNT.line(15).endswith(" 3")
WC = capture("11", "cli-container")                     # the book's chunk file: 1,355 lines
assert WC.line(8).split()[0] == str(COUNTS["book"]) and WC.line(8).endswith(f"-{BOOK}.jsonl"), WC.line(8)
assert COUNTS["italian"] == 64 and COUNTS["italian_tolminc"] == 0

Q = capture("09", "recorded-embeddings")                # the stand-in query, without and with filters
assert Q.line(16).startswith("stand-in query vector:") and STANDIN_ID in Q.line(16)
assert Q.line(18) == "-- no filter" and Q.line(29).startswith("-- where book + $contains 'Italian'")
NOFILT = Q.at((19, 28))
FILT = Q.at((30, 39))
assert all(s.endswith("  Tolminc Cheese") for s in NOFILT) and NOFILT[0].startswith("0.0000")
assert NOFILT[-1].startswith("0.1627") and all(s.endswith(f"  {BOOK}") for s in FILT)
assert FILT[0].startswith("0.2833") and FILT[-1].startswith("0.3123")
STANDIN_ROWS = word_fold(Q.line(16)) + word_fold(Q.line(17))
assert len(STANDIN_ROWS) == 4 and STANDIN_ROWS[1].startswith(STANDIN_ID), STANDIN_ROWS

GET = capture("05", "recorded-embeddings")              # --get: the same book filter, no question
assert GET.cmd == "python cli.py --get --chunk_type char-split" and GET.line(3) == "get()"
ARGS_ROWS = word_fold(GET.line(2))
IDS = GET.cut(6, "]")
IDS_ROWS = word_fold(IDS)
ID_BASE = "1021665fac86c5a5-"
assert len(ARGS_ROWS) == 3 and len(IDS_ROWS) == 4 and IDS.count(ID_BASE) == 10, (ARGS_ROWS, IDS_ROWS)

# cli.py lines this scene quotes (checked: the panels below would fail on a different file)
assert excerpt("cli.py", 356, 356).strip() == "n_results=10,"
assert excerpt("cli.py", 357, 357).strip() == 'where={"book": "The Complete Book of Cheese"},'
assert excerpt("cli.py", 353, 353).strip() == 'search_string = "Italian"'
assert excerpt("cli.py", 325, 325).strip() == "# # 1: Query based on embedding value"
assert excerpt("cli.py", 402, 402).startswith("def get(") and "limit=10" in excerpt("cli.py", 416, 416)

# ------------------------------------------------------------------ layout
CC = np.array([0.0, 1.25, 0])           # the dot cloud's centre (10.0 x 2.6: y -0.05..2.55)
ROW_Y = -0.5                            # the filter row under the cloud
BAND_Y = 3.22                           # tags in the band right of the tracker
CARD_Y = 2.36                           # the check card (left) and the staff tag (right) above an 11-row terminal
LABEL_Y = -0.25                         # the survivors' label, under the cloud
CARDS_Y = 2.33                          # beat 7: the ten record cards, above a 4-row strip
FIX_Y = 0.22                            # beat 7: the fix card (its header included)


def pink_bar(panel, n: int):
    """A PINK bar with PINK edges over code line n (a filter)."""
    b = panel.bar(n, LOOKUP, 0.12)
    b.set_stroke(LOOKUP, 2.5, 1)
    return b


def backed(m, pad: float = 0.08, opacity: float = 0.88):
    """m on an opaque rounded patch of the background (a label over dimmed dots)."""
    r = RoundedRectangle(width=m.width + 2 * pad, height=m.height + 2 * pad, corner_radius=0.06,
                         stroke_width=0).set_fill(S.BG, opacity).move_to(m)
    return VGroup(r, m)


def rows_box(lines, a: int, b: int, color: str = TURN, pad: float = 0.05):
    """One box over character columns a..b of several consecutive mono lines."""
    cw = cell_width(lines[0].pt)
    x0 = grid_x0(lines[0]) + a * cw
    top = lines[0].strut.get_top()[1] + pad
    bot = lines[-1].strut.get_bottom()[1] - pad
    r = RoundedRectangle(width=(b - a) * cw + 2 * pad, height=top - bot, corner_radius=0.06,
                         stroke_color=color, stroke_width=3).set_fill(opacity=0)
    return r.move_to([x0 + (b - a) * cw / 2, (top + bot) / 2, 0])


def one_line_card(text: str):
    """The GREY "an extra Python check · …" card, on one line (its code is never shown)."""
    return card_rows([text])


def survivors(dc) -> VGroup:
    return VGroup(*[dc.dots[i] for i in dc.italian_ids])


def mask_to(dc, level: str, dim: float = 0.12, bright: float = 1.7) -> list:
    """DotCloud.mask; for "italian" the 64 survivors also grow (the SHOW's "64 separate brighter
    dots"), each in one animation (fill and scale together, so no two animations share a dot)."""
    if level != "italian":
        return dc.mask(level, dim)
    keep = set(dc.italian_ids)
    off = VGroup(*[d for i, d in enumerate(dc.dots) if i not in keep])
    dc.level = level
    return [off.animate.set_fill(S.GREY, dim)] + \
        [d.animate.set_fill(DATA, 1).scale(bright) for d in survivors(dc)]


class FiltersFirst(VoiceScene):
    def construct(self):
        assert len(SAY) == 8, f"S12 has {len(SAY)} SAY lines; this scene times 8"

        tr = tracker("Query", 2)

        # ========================================================== 0 · the query the code sends
        panel = src_panel("cli.py", 352, 361).move_to([0, 0.5, 0])
        b356 = panel.bar(356, TURN)
        b357 = pink_bar(panel, 357)
        b358 = pink_bar(panel, 358)
        b353 = panel.bar(353, LOOKUP, 0.12)
        u_ten = under(panel.span(356, "n_results=10"), TURN)
        u_book = under(panel.span(357, '"The Complete Book of Cheese"'), LOOKUP)
        u_ital = under(panel.span(353, '"Italian"'), LOOKUP)
        c_meta = chip("metadata filter · keeps one book", LOOKUP, size=CAPTION)
        c_doc = chip("document filter · keeps chunks that contain “Italian”", LOOKUP, size=CAPTION)
        VGroup(c_meta, c_doc).arrange(RIGHT, buff=0.45).move_to([0, -2.45, 0])

        def code_rows(n):
            return VGroup(*[panel.code.code_lines[k] for k in panel.rows_of(n)])

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.1), FadeIn(panel, shift=UP * 0.2), run_time=0.7)
            self.play(caption_extra(tr, True), run_time=0.4)
            vo.wait_until("10 results")
            self.play(FadeIn(b356), Create(u_ten), run_time=0.5)
            vo.wait_until("and two filters")
            self.play(Indicate(code_rows(357), color=LOOKUP, scale_factor=1.03),
                      Indicate(code_rows(358), color=LOOKUP, scale_factor=1.03), run_time=0.8)
            vo.wait_until("The metadata filter")
            self.play(FadeIn(b357), FadeIn(c_meta, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("The Complete Book of Cheese")
            self.play(Create(u_book), run_time=0.6)
            vo.wait_until("The document filter")
            self.play(FadeIn(b358), FadeIn(c_doc, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("that contain Italian")
            self.play(FadeIn(b353), Create(u_ital), run_time=0.6)

        # ========================================================== 1 · the cloud; ponder
        dc = DotCloud(width=10.0, height=2.6, show=("dots",)).shift(CC)
        dc.parts["tolminc_label"].shift(UP * 0.12)      # clear of the cloud's top edge
        ill = our_illustration_tag().move_to([6.45 - our_illustration_tag().width / 2, 2.5, 0])
        cap = VGroup(note("char-split collection"), note("1 dot ≈ 8 chunks")).arrange(DOWN, aligned_edge=LEFT,
                                                                                       buff=0.1)
        cap.move_to([6.4 - cap.width / 2, 0.22, 0])
        cap2 = note("64 bright dots = 64 chunks").move_to(cap[1]).align_to(cap, RIGHT)
        qcard = question_card()
        qcard.move_to([6.45 - qcard.width / 2, BAND_Y, 0])

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(panel, b356, b357, b358, b353, u_ten, u_book, u_ital, c_meta, c_doc),
                              shift=DOWN * 0.2), run_time=0.5)
            self.play(FadeIn(dc), FadeIn(ill), FadeIn(cap), FadeIn(qcard, shift=LEFT * 0.2), run_time=0.8)
            vo.wait_until("about Tolminc")
            fly = qcard.copy()
            self.play(fly.animate.scale(0.05).move_to(dc.standin_dot).set_opacity(0),
                      *dc.parts_in("standin", "tolminc_label"), run_time=0.8)
            self.remove(fly)
            vo.wait_until("What will the 10 results")
            self.play(Indicate(dc.standin_dot, color=LOOKUP, scale_factor=1.8), run_time=0.7)
        pcard = ponder_at(self, PONDER_Q, 8.0, y=-2.2)

        # ========================================================== 2 · counts with the filters
        ck = one_line_card("an extra Python check · counts with the query's filters").move_to([0, -2.45, 0])
        f_book = chip(f"book = {BOOK}", LOOKUP, size=CAPTION)
        f_ital = chip('$contains "Italian"', LOOKUP, size=CAPTION, font=MONO)
        f_book.move_to([-6.3 + f_book.width / 2, ROW_Y, 0])
        f_ital.next_to(f_book, RIGHT, buff=0.35)
        cnt = Counter("chunks", COUNTS["char-split"], size=26)
        cnt.num.scale(1.38)                     # the TeX digits as tall as the 26 pt label's
        cnt.num.next_to(cnt.label, RIGHT, buff=0.15).align_to(cnt.label, DOWN)
        cnt.move_to([6.3 - cnt.width / 2, ROW_Y, 0])
        t = term(P_CTR2, rows=3, container=True)
        stf = staff_tag()
        stf.move_to([6.3 - stf.width / 2, STRIP_TOP + 0.06 + stf.height / 2, 0])     # on the strip's top right
        stf_hi = [6.3 - stf.width / 2, CARD_Y, 0]                                      # above an 11-row terminal
        tc = dc.standin_dot.get_center()
        tz = backed(sans("mentioning Tolminc: 0", 24, TURN)).move_to(tc + DOWN * 0.62)

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(pcard), run_time=0.4)
            self.play(FadeIn(ck, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("Of 8,248 chunks")
            self.play(FadeIn(cnt, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("the book filter keeps")
            self.play(FadeIn(f_book, shift=RIGHT * 0.1), run_time=0.4)
            self.play(*mask_to(dc, "book"), cnt.count_to(COUNTS["book"]), run_time=1.1)
            vo.wait_until("the word Italian keeps")
            self.play(FadeIn(f_ital, shift=RIGHT * 0.1), run_time=0.4)
            self.play(*mask_to(dc, "italian"), cnt.count_to(COUNTS["italian"]), Transform(cap[1], cap2),
                      run_time=1.1)
            vo.wait_until("How many mention Tolminc")
            self.play(FadeOut(ck), FadeIn(t, shift=UP * 0.2), run_time=0.5)
            out = t.print(self, CNT.at((13, 15)), run_time=0.5)
            self.play(FadeIn(stf, shift=DOWN * 0.1), run_time=0.3)
            vo.wait_until("None")
            z14 = col_box(out[1], 0, len(out[1].text), TURN)
            pin(self, out[1], z14, anim=Create(z14), run_time=0.4)
            self.play(FadeIn(tz, scale=0.9), run_time=0.5)
        cnt.freeze()

        # ========================================================== 3 · a stand-in query, no filter
        ck2 = one_line_card("an extra Python check · query with a stored vector")
        ck2.move_to([-6.3 + ck2.width / 2, CARD_Y, 0])
        sti = standin_tag()
        sti.move_to([6.5 - sti.width / 2, BAND_Y, 0])

        with self.voiceover(SAY[3]) as vo:
            vo.wait_until("The real question")          # "Now a search.": the count stays a moment
            self.play(FadeOut(VGroup(dc, ill, cap, f_book, f_ital, cnt, tz)), run_time=0.5)
            resize(self, t, 11, keep=0, extra=[FadeIn(ck2, shift=DOWN * 0.1), stf.animate.move_to(stf_hi)])
            vo.wait_until("so we use a stand-in")
            self.play(ReplacementTransform(qcard, sti), run_time=0.7)
            vo.wait_until("the stored vector")
            o16 = t.print(self, STANDIN_ROWS, run_time=0.6)
            self.play(substring(o16[1], STANDIN_ID).animate.set_color(LOOKUP), run_time=0.4)
            vo.wait_until("Without filters")
            o18 = t.print(self, Q.at((18, 28)), run_time=0.7)
            self.play(Indicate(o18[0], color=TURN, scale_factor=1.06), run_time=0.6)
            vo.wait_until("the chunk itself")
            z0 = col_box(o18[1], 0, 6, S.GREY)
            pin(self, o18[1], z0, anim=Create(z0), run_time=0.3)
            pin(self, o18[1], beside(grey_tag("itself"), t, o18[1], buff=0.45), run_time=0.3)
            vo.wait_until("up to 0.16")
            z1 = col_box(o18[10], 0, 6, TURN)
            pin(self, o18[10], z1, anim=Create(z1), run_time=0.4)

        # ========================================================== 4 · with the code's filters
        for d in dc.dots:                       # the picture comes back unmasked
            d.set_fill(DATA, 1)
        for d in survivors(dc):
            d.scale(1 / 1.7)
        dc.level = "all"
        near0 = dc.nearest(10, "all")
        beam = dc.beam(near0)
        far = dc.nearest(10, "italian")
        fv = VGroup(*far)
        surv_lab = backed(note(f"all 10: {BOOK}", INK)).move_to([fv.get_center()[0], LABEL_Y, 0])

        with self.voiceover(SAY[4]) as vo:
            t.clear(self)
            o29 = t.print(self, Q.at((29, 39)), run_time=0.7)
            vo.wait_until("all 10 results")
            bk = rows_box(list(o29[1:]), 8, 8 + len(BOOK), TURN)
            self.play(Create(bk), run_time=0.6)
            vo.wait_until("at 0.28")
            z2 = col_box(o29[1], 0, 6, TURN)
            pin(self, o29[1], z2, anim=Create(z2), run_time=0.35)
            vo.wait_until("to 0.31")
            z3 = col_box(o29[10], 0, 6, TURN)
            pin(self, o29[10], z3, anim=Create(z3), run_time=0.35)
            vo.wait_until("The filters act first")
            self.play(FadeOut(bk), FadeOut(ck2), run_time=0.3)
            stf_lo = [6.3 - stf.width / 2, STRIP_TOP + 0.06 + stf.height / 2, 0]
            resize(self, t, 3, run_time=0.6, extra=[stf.animate.move_to(stf_lo)])
            self.play(FadeIn(dc), FadeIn(ill), FadeIn(cap[0]), run_time=0.5)
            self.play(Create(beam), run_time=0.5)
            self.play(*mask_to(dc, "italian"), FadeIn(cap[1]), run_time=0.8)
            beam2 = dc.beam(far)
            self.play(Transform(beam, beam2), run_time=0.9)
            vo.wait_until("with whatever survives")
            self.play(FadeIn(surv_lab, shift=UP * 0.1), Indicate(fv, color=DATA, scale_factor=1.3),
                      run_time=0.6)
            vo.wait_until("however far")
            self.play(ShowPassingFlash(beam2.copy().set_stroke(TURN, 5), time_width=0.6), run_time=0.9)

        # ========================================================== 5 · the lecture: after ranking
        lr = lref("A54–A55")
        st = StageStrip().shift(UP * 1.75)
        qbox = st.boxes[2]
        filt = st.parts["filter"]
        filt.set_z_index(2)                     # the cards pass behind it
        story = VGroup(*[chunk_card(0.5, 0.32) for _ in range(10)]).arrange_in_grid(2, 5, buff=0.1)
        story.move_to([qbox.get_center()[0], filt.get_center()[1], 0])
        s_lab = note("10 story chunks, ranked").next_to(story, DOWN, buff=0.15)
        through = story.copy().move_to([filt.get_center()[0], -0.35, 0])
        strikes = VGroup(*[cross_mark(0.26, ERR, 4).move_to(c) for c in through])
        empty = mono("[]", 26, INK)
        nothing = sans("nothing left", CAPTION + 2, ERR)
        none_g = VGroup(empty, nothing).arrange(RIGHT, buff=0.3).move_to([filt.get_center()[0], -1.3, 0])
        res = VGroup(*[chunk_card(0.5, 0.32) for _ in range(10)]).arrange_in_grid(2, 5, buff=0.1)
        res_x = (st.boxes[2].get_center()[0] + st.boxes[3].get_center()[0]) / 2
        res.move_to([res_x, filt.get_center()[1], 0])
        caption = note("Chroma: filter, then rank · 10 results, wrong cheese").move_to([0, -0.55, 0])

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(dc, beam, ill, cap, surv_lab, t, stf)), FadeOut(sti),
                      FadeIn(lr), run_time=0.6)
            self.play(FadeIn(st, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("here, that would drop")
            self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.25) for c in story], lag_ratio=0.08),
                      FadeIn(s_lab), run_time=0.9)
            self.play(FadeOut(s_lab), story.animate.scale(0.4).move_to(filt), run_time=0.7)
            self.play(story.animate.scale(2.5).move_to(through), run_time=0.6)
            self.play(LaggedStart(*[Create(x) for x in strikes], lag_ratio=0.08),
                      story.animate.set_fill(S.GREY, 0.15).set_stroke(S.GREY, opacity=0.5), run_time=0.9)
            vo.wait_until("and return nothing")
            self.play(FadeIn(none_g, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Chroma filters first")
            self.play(FadeOut(VGroup(story, strikes, none_g)), run_time=0.4)
            self.play(st.slide_filter(2, run_time=1.1))
            vo.wait_until("so you get 10 results")
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.25) for c in res], lag_ratio=0.08), run_time=0.8)
            vo.wait_until("about the wrong cheese")
            self.play(FadeIn(caption, shift=UP * 0.1), run_time=0.5)

        # ========================================================== 6 · the commented-out variants
        p2 = src_panel("cli.py", 325, 331)
        p2.move_to([-6.3 + p2.width / 2, 0.45, 0])
        hashes = VGroup(*[p2.span(n, "#") for n in range(325, 332)])
        hbox = RoundedRectangle(width=hashes.width + 0.2, height=hashes.height + 0.16, corner_radius=0.08,
                                stroke_color=S.GREY, stroke_width=3).set_fill(S.GREY, 0.12).move_to(hashes)
        err = erratum_tag().next_to(p2.header, RIGHT, buff=0.4)
        rm = readme_chip("README.md · line 186", "Apply various types of filters")
        rm.move_to([-6.3 + rm.width / 2, 2.55, 0])
        unc = card_rows(["uncomment lines 326–331", "variant 4 still prints after it", "needs your key",
                         "no rebuild: the code is mounted"])
        unc.move_to([6.35 - unc.width / 2, 0.45, 0])
        cont = VGroup(mono("$contains", CAPTION, INK),
                      note("= keyword filter (case-sensitive) · not keyword ranking (later)", INK))
        cont.arrange(RIGHT, buff=0.2)
        cont_box = RoundedRectangle(width=cont.width + 0.5, height=cont.height + 0.3, corner_radius=0.12,
                                    stroke_color=LOOKUP, stroke_width=2.5).set_fill(LOOKUP, 0.08)
        cont_g = VGroup(cont_box, cont.move_to(cont_box)).move_to([0, -2.35, 0])

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(st, res, caption, lr)), run_time=0.5)
            self.play(FadeIn(p2, shift=UP * 0.2), FadeIn(err), run_time=0.6)
            vo.wait_until("the README promises")
            self.play(FadeIn(rm, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("variants 1 to 3")
            self.play(FadeIn(hbox), Indicate(hashes, color=INK, scale_factor=1.2), run_time=0.8)
            vo.wait_until("Uncomment the first")
            self.play(hbox.animate.set_stroke(TURN).set_fill(TURN, 0.12), FadeIn(unc.frame), run_time=0.5)
            for r in unc.rows:
                self.play(FadeIn(r, shift=RIGHT * 0.1), run_time=0.3)
            vo.wait_until("And contains is")
            self.play(FadeIn(cont_g, shift=UP * 0.1), run_time=0.6)

        # ========================================================== 7 · --get: the Gutenberg header
        tg = term(P_CTR2, rows=10, container=True)
        rm_note = note("not in the README · cli.py · lines 402–418")
        nd = note("no distances: no ranking")

        cyl = cylinder(1.25, 1.45).move_to([-5.6, CARDS_Y - 0.55, 0])
        cards = VGroup()
        for k in range(10):
            fr = RoundedRectangle(width=0.82, height=0.46, corner_radius=0.07, stroke_color=DATA,
                                  stroke_width=2.5).set_fill(S.BG, 0.9)
            tx = mono(f"-{k}", CAPTION, INK).move_to(fr)
            cards.add(VGroup(fr, tx))
        cards.arrange(RIGHT, buff=0.12)
        cards.move_to([cyl.get_right()[0] + 0.3 + cards.width / 2, CARDS_Y, 0])
        groups = [(range(0, 3), ERR, "-0 to -2", "Gutenberg header"),
                  (range(3, 6), S.GREY, "-3 to -5", "title page, contents"),
                  (range(6, 10), DATA, "-6 to -9", "chapter one begins")]
        brackets, labels = VGroup(), VGroup()
        y_br = cards.get_bottom()[1] - 0.16
        for ks, col, ids_, words in groups:
            g = VGroup(*[cards[k] for k in ks])
            x0, x1 = g.get_left()[0], g.get_right()[0]
            br = VGroup(Line([x0, y_br, 0], [x1, y_br, 0], color=col, stroke_width=3),
                        Line([x0, y_br, 0], [x0, y_br + 0.1, 0], color=col, stroke_width=3),
                        Line([x1, y_br, 0], [x1, y_br + 0.1, 0], color=col, stroke_width=3))
            lb = VGroup(mono(ids_, CAPTION, col), sans(words, CAPTION, col)).arrange(DOWN, buff=0.08)
            lb.next_to(br, DOWN, buff=0.14)
            brackets.add(br)
            labels.add(lb)
        fix = card_rows(["strip outside the START/END markers", "then chunk, embed, load again"],
                        header="the fix", frame_color=DATA)
        fix.move_to([cards.get_center()[0], FIX_Y, 0])

        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(p2, hbox, err, rm, unc, cont_g)), run_time=0.5)
            self.play(FadeIn(tg, shift=UP * 0.2), run_time=0.5)
            g = type_cmd(self, tg, GET.cmd, type_time=1.0)
            assert hasattr(g, "rows") and len(g.rows) == 2       # the command folds under the prompt
            tagrow = VGroup(extra_tag(), rm_note).arrange(RIGHT, buff=0.3)
            beside(tagrow, tg, g.rows[0], buff=0.5)
            pin(self, g.rows[0], tagrow, run_time=0.4)
            vo.wait_until("uses the same book filter")
            out7 = tg.print(self, ARGS_ROWS + [GET.line(3)], run_time=0.5)
            pin(self, out7[3], beside(staff_tag(), tg, out7[3], buff=0.6), run_time=0.3)
            ids = tg.print(self, IDS_ROWS, run_time=0.5)
            vo.wait_until("but no question")
            pin(self, ids[3], beside(nd, tg, ids[3], buff=0.5), run_time=0.4)
            vo.wait_until("Its 10 records start")
            resize(self, tg, 4, keep=list(ids), run_time=0.7)
            self.play(FadeIn(cyl), run_time=0.4)
            flying = VGroup()
            for k in range(10):
                sid = f"'{ID_BASE}{k}'"
                row = next(r for r in ids if sid in r.text)
                flying.add(substring(row, sid).copy())
            self.play(*[ReplacementTransform(flying[k], cards[k]) for k in range(10)], run_time=1.0)
            self.play(Create(brackets[0]), FadeIn(labels[0], shift=DOWN * 0.1),
                      *[cards[k][0].animate.set_stroke(ERR) for k in range(3)], run_time=0.5)
            vo.wait_until("then the title page")
            self.play(Create(brackets[1]), FadeIn(labels[1], shift=DOWN * 0.1),
                      *[cards[k][0].animate.set_stroke(S.GREY) for k in range(3, 6)], run_time=0.5)
            self.play(Create(brackets[2]), FadeIn(labels[2], shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("That header")
            self.play(*[Indicate(cards[k], color=ERR, scale_factor=1.15) for k in range(3)],
                      Indicate(labels[0], color=ERR, scale_factor=1.06), run_time=0.9)
            vo.wait_until("are indexed like any text")
            self.play(Indicate(cyl, color=DATA, scale_factor=1.08), run_time=0.8)
            vo.wait_until("strip them before chunking")
            self.play(FadeIn(fix, shift=UP * 0.15), run_time=0.6)

        self.play(FadeOut(VGroup(tr, tg, cyl, cards, brackets, labels, fix)), run_time=0.8)
        self.wait(0.3)
