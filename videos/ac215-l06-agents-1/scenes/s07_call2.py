"""S07 · Call 2: your code ran it, the model answers (llm-rag › Agents steps 1–2; lecture slide 39).

Beats (script.md "## S07", one voiceover block each):
0. TRACKER Agents 1; the call strip (beside the tracker, where S06 left it) moves from "call 1" to
   "your code". Under it the excerpt chip `function_responses = agent_tools.execute_function_calls(`
   (cli.py · line 459 (excerpt)), caption "hand the calls to the dispatcher"; it stays while
   CODE(agent_tools.py: 84–94) (line 88 YELLOW "match the name") Transforms into
   CODE(agent_tools.py: 95–100, 103–107) folded (95–100 GREEN "call the real function", 103–107 TEAL
   "wrap the result"). No mini-map: the call strip orients.
1. TRACKER · extra. The extra card (two lines) "feed the model's call from the staff's run through
   agent_tools.execute_function_calls, against this collection" with the PINK `stand-in` tag "a stored
   chunk's vector replaces Google's embedding"; a 7-row TEAL container terminal prints
   TERM(cli-container/33: 36, 37–44 folded, 45, 48; wrap), author masked.
2. Line 36 turns PINK, `stand-in` tag pinned; the search text of line 48 PINK. The terminal shrinks to a
   3-row strip (line 36 kept), V3's compact stage comes in above, with a TEAL dashed band under it
   ("inside llm-rag-cli", the CLI box lit) holding the BLUE call card: its search_content turns PINK and
   a dashed PINK vector glyph rises out of the cylinder (stand-in, "a stored chunk's vector"); the
   query `collection.query(…, n_results=10, where={"author": …})` writes in (the vector into its "…",
   the card's author into where=) with a PINK arrow up into the cylinder; GREY "which 10 may differ".
3. TERM(33: 51–57, …, 135; wrap) scrolls through the strip (51–53, then pairs, so two lines of text
   always show). Ten GREEN chunk cards drop out of the
   cylinder into the band; the first opens into a card with lines 51, 57, 59's first words (Mara and
   Anja YELLOW). They merge into one GREEN string, "3509 characters" (line 135) YELLOW, which becomes
   the TEAL {"content": …} card "3,509 characters", stapled to the BLUE call card. The cylinder never
   moves toward the cloud.
4. CODE(cli.py: 464–477) at 20 pt, comment cut, lines 470–472 as one row; the call strip lights
   "call 2"; a fresh V2 envelope "call 2" beside it. As named: line 468 GREY → sheet "the question";
   469 BLUE → sheet "the model's turn" with its seal; the function_responses row TEAL → sheet "your
   function responses"; line 475 GREEN → the GREEN "the menu" card clips on; a GREY dashed ghost sheet
   "no tool config" and a GREY dashed ghost under the panel "no tool_config → mode back to
   automatic", dashed to line 474.
5. LECTURE 39 + the duty chip "interpret its outputs" lit YELLOW under it. TRACKER · extra. The
   envelope opens into a 13-row TEAL terminal: TERM(33: 137 cut at the row, the folds, 151 cut, 167,
   168, 170 cut, …, 231, 233), `built, not sent`; `"thoughtSignature":` boxed BLUE and the seal from the
   BLUE sheet lands on it; `"functionResponse"` TEAL; `"generationConfig": {}` GREY; a BLUE rule and
   "the model's own turn" beside rows 148–163; "unchanged · seal kept" at the last sentence.
6. The terminal folds into a small envelope; V3's compact stage returns: the envelope crosses into the
   cloud, a BLUE prose card comes back and unfolds into PANEL(expected/out-txt-agent-run.txt: 99, 105
   cut, 111 cut, 112 cut; wrapped at spaces, GREY ↪) (out.txt · lines 98–111 (excerpt), staff tag with
   "old book") while the stage leaves; Alpine region, limestone caves underlined, transhumance YELLOW,
   the seasonal movement underlined; then two GOLD chips "247 tokens" / "1,269 tokens" (out.txt lines
   49, 135).
7. The hook's YELLOW card, centre: "Who searched your database?" / "Who chose the book?"; BLUE "Gemini
   wrote the call" then GREEN "your Python, on your laptop" as said; GOLD tag "2 Gemini calls + 1
   embedding call per question", GREY source note (agent_tools.py · line 43 → cli.py · lines 75–84).
8. TRACKER Agents 1 · extra. The lecture tag and the call strip leave. A 10-row second terminal (20 pt
   so the table's 70 columns fit) under the extra card "count four of the answer's words …": in the
   narration's order, TERM(laptop/10: 2–5) first, "book today 0" boxed RED; then it types the git show …;
   head -4 … command (extra, folds) → TERM(laptop/09: 2 cut after "2026-09-22", 4–6), the commit and
   both files underlined YELLOW; at "The staff's index" the "book before 85bba32" column boxed GREEN.
9. The TEAL cylinder with the staff's index: its cards turn GREY dashed "old book"; today's 24 GREEN
   cards slide in, "Mara", "the curd", "the wheels" as said; caption "an index answers from what was
   loaded · lecture 5".
10. The `erratum` README chip (README.md · line 266, expected) "Displays the LLM's response"; under it
   CODE(cli.py: 478), `response` underlined RED; then the GREEN fix chip `print(response.text)` "just
   the answer".
11. TRACKER Agents 2 (· extra while the curl is up). A GREY browser frame (illustration) at
   ac215-llm-rag.dlops.io/agent with an empty chat box; a 4-row strip (laptop · second terminal: the
   container still runs) types the curl (extra on its first row, folds) →
   TERM(laptop/11: 2), `at the time of recording`; the README chip (README.md · line 271, expected)
   "Use Chrome browser for best performance". Hold, then everything fades: empty frame.
"""

import numpy as np
from common import (
    CLOUD,
    COST,
    CTR,
    DATA,
    ERR,
    INK,
    LOOKUP,
    MONO,
    NARRATION,
    P_REPO,
    SECOND,
    TURN,
    CallStrip,
    Envelope,
    TrustStage,
    answer_bars,
    beside,
    call_card,
    capture,
    caption_extra,
    card_rows,
    chunk_card,
    col_box,
    concept_box,
    cylinder,
    erratum_tag,
    excerpt,
    excerpt_chip,
    extra_card,
    extra_tag,
    fix_chip,
    illustration_tag,
    json_card,
    log_panel,
    lref,
    note,
    notsent_tag,
    pin,
    readme_chip,
    recording_tag,
    resize,
    response_card,
    ring,
    src_panel,
    staff_run_tag,
    standin_tag,
    switch_section,
    term,
    tracker,
    type_cmd,
    under,
)
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Create,
    DashedLine,
    DashedVMobject,
    FadeIn,
    FadeOut,
    FadeTransform,
    GrowArrow,
    Indicate,
    LaggedStart,
    Line,
    Polygon,
    VMobject,
    ReplacementTransform,
    Transform,
    TransformFromCopy,
    RoundedRectangle,
    VGroup,
    Write,
)

from explainer import style as S
from explainer.devops import box, browser_window, chip, glyph_range, label, mono, mono_line, substring, tag
from explainer.scene import VoiceScene

SAY = NARRATION["S07"]

# ------------------------------------------------------------------ the real sources
C33 = capture("33", "cli-container")          # the extra script: the staff's call through the dispatcher
OUT = capture("out-txt-agent-run", "expected")  # the staff's run (out.txt = file line - 1)
C09 = capture("09", "laptop")                 # extra: git show 85bba32; head -4 the book
C10 = capture("10", "laptop")                 # extra: four of the answer's words, counted
C11 = capture("11", "laptop")                 # extra: curl the hosted Cheese Agent Tool

L459 = excerpt("cli.py", 459, 459)
SUB459 = "function_responses = agent_tools.execute_function_calls("
assert SUB459 in L459

# beat 1: the dispatcher's prints (cli-container/33 lines 36, 37-44 folded, 45, 48)
D36 = C33.line(36)
D_FOLD = C33.fold(37, 44, "Function calls: [FunctionCall( … name='get_book_by_author' )]")
D45 = C33.line(45)
D48 = C33.line(48)
assert D36.startswith("stand-in embed_func") and D45 == "Function: get_book_by_author"
assert "cheese making importance location" in D48

# beat 3: the response (51-57), …, the summary line 135
D_RESP = C33.at((51, 57), "…", 135)
D135 = C33.line(135)
assert "3509 characters" in D135

# beat 5: call 2's request, built, not sent (the script's folds; each fold checked)
REQ = [
    C33.line(137),
    C33.fold(138, 147, '{ "contents": [ { … "role": "user" },'),
    "    " + C33.fold(148, 150, '{ "parts": [ {'),
    C33.cut(151, '"AY89a186') + '…",',
    " " * 10 + C33.fold(152, 159, '"functionCall": { … "name": "get_book_by_author" }'),
    " " * 8 + C33.fold(160, 163, '} ], "role": "model" },'),
    "    " + C33.fold(164, 166, '{ "parts": [ {'),
    C33.line(167),
    C33.line(168),
    C33.cut(170, "Mara asked.") + "…",
    "…",
    C33.line(231),
    (C33.line(233), S.GREY),
]
assert '"functionResponse"' in REQ[7] and REQ[11].strip() == '"generationConfig": {}'
assert REQ[12][0].startswith("-- stopped here")

# beat 6: the staff's answer (out.txt 98-111)
A99 = OUT.line(99)
A105 = OUT.cut(105, "Alpine region,") + " …"
A111 = OUT.cut(111, "limestone caves") + " …"
A112 = OUT.cut(112, "(the seasonal movement of livestock)") + " …"
assert OUT.line(50).strip() == "total_token_count=247," and OUT.line(136).strip() == "total_token_count=1269,"

# beat 8
GIT_CMD = C09.cmd
G2 = C09.cut(2, "2026-09-22")
TABLE = C10.at(2, 3, 4, 5)
# beat 11
CURL_CMD = C11.cmd

# the chunk text card (first words of lines 51, 57, 59), each an exact piece of its line
CHUNK_ROWS = ["is ready?” Mara asked.", "Anja smiled. …", "Over the following hours, …"]
assert CHUNK_ROWS[0] in C33.line(51) and C33.line(57).startswith("Anja smiled.")
assert C33.line(59).startswith("Over the following hours,")

COLS = 65               # characters a row in the house terminal (22 pt)
TOP_Y = 2.78            # the top of the picture area (the call strip sits beside the tracker)
SAFE_L, SAFE_R = -6.45, 6.45


# ------------------------------------------------------------------ helpers
def place(m, left=None, right=None, top=None, bottom=None, cx=None, cy=None):
    """Move m so the given edge / centre coordinate is where asked."""
    if left is not None:
        m.shift(RIGHT * (left - m.get_left()[0]))
    if right is not None:
        m.shift(RIGHT * (right - m.get_right()[0]))
    if cx is not None:
        m.set_x(cx)
    if top is not None:
        m.shift(UP * (top - m.get_top()[1]))
    if bottom is not None:
        m.shift(UP * (bottom - m.get_bottom()[1]))
    if cy is not None:
        m.set_y(cy)
    return m


def wrapped_span(rows, full: str, sub: str, occurrence: int = 0, width: int = COLS) -> VGroup:
    """The glyphs of `sub` in a line Terminal.print(wrap=True) split into `rows`."""
    i = -1
    for _ in range(occurrence + 1):
        i = full.find(sub, i + 1)
    if i < 0:
        raise ValueError(f"{sub!r} not in {full!r}")
    j = i + len(sub)
    out = VGroup()
    for r, row in enumerate(rows):
        a, b = r * width, (r + 1) * width
        lo, hi = max(i, a), min(j, b)
        if lo < hi:
            out.add(*glyph_range(row, lo - a, hi - a))
    return out


def rows_of_line(printed, items, k, width: int = COLS):
    """The printed rows (a list) of item k, given the items as passed to Terminal.print(wrap=True)."""
    start = 0
    for n, s in enumerate(items):
        s = s if isinstance(s, str) else s[0]
        cnt = max(1, -(-len(s) // width))
        if n == k:
            return list(printed[start:start + cnt])
        start += cnt
    raise IndexError(k)


def line_note(s, color=DATA, size=20, arrow="←"):
    return label(f"{arrow} {s}", size, color)


def wrap_words(line: str, limit: int) -> list[str]:
    """Break a recorded line at spaces into rows of at most `limit` characters; continuation rows
    get the line's indent plus '  ↪ ' (the code panels' mark)."""
    if len(line) <= limit:
        return [line]
    indent = line[:len(line) - len(line.lstrip())]
    pre = indent + "  ↪ "
    rows, rest, first = [], line, True
    while len(rest) > (limit if first else limit - len(pre)):
        lim = limit if first else limit - len(pre)
        i = rest.rfind(" ", 1, lim)
        rows.append(rest[:i] if first else pre + rest[:i])
        rest = rest[i + 1:]
        first = False
    rows.append(rest if first else pre + rest)
    return rows


def phrase_glyphs(rows, phrase):
    """The glyphs of `phrase` in log-panel rows that wrap_words() may have split at a space: a list
    of VGroups, one per row it spans (underline each)."""
    for k, r in enumerate(rows):
        if phrase in r.text:
            return [substring(r, phrase)]
    words = phrase.split(" ")
    for k, r in enumerate(rows[:-1]):
        for cut in range(1, len(words)):
            head, tail = " ".join(words[:cut]), " ".join(words[cut:])
            nxt = rows[k + 1].text
            if r.text.rstrip().endswith(head) and nxt.lstrip().lstrip("↪ ").startswith(tail):
                return [substring(r, head), substring(rows[k + 1], tail)]
    raise ValueError(f"{phrase!r} in no row")


def two_line_extra(lines, size=20):
    """The GREY extra card (as common.extra_card) with a purpose that needs several rows, and a
    PINK stand-in row: `lines` are mobjects (rows). .frame .rows .header .tag"""
    c = card_rows(lines, buff=0.14)
    tg = extra_tag()
    hd = VGroup(tg, note("an extra check · in the study guide")).arrange(RIGHT, buff=0.2)
    hd.next_to(c.frame, UP, buff=0.08).align_to(c.frame, LEFT).shift(RIGHT * 0.1)
    c.add(hd)
    c.header, c.tag = hd, tg
    return c


def dashed_vector(color=LOOKUP, length=0.85):
    """A dashed query-vector glyph (the stand-in): a dashed shaft and a solid tip."""
    d = np.array([np.cos(np.radians(28)), np.sin(np.radians(28)), 0])
    tip_pt = d * length
    shaft = DashedLine(np.array([0, 0, 0]), tip_pt - d * 0.16, color=color, stroke_width=5,
                       dash_length=0.09)
    n = np.array([-d[1], d[0], 0])
    tip = Polygon(tip_pt, tip_pt - d * 0.2 + n * 0.09, tip_pt - d * 0.2 - n * 0.09, stroke_width=0) \
        .set_fill(color, 1)
    return VGroup(shaft, tip).move_to(np.array([0, 0, 0]))


def dashed_frame(w, h, color, stroke=2, radius=0.14, dashes=None):
    r = RoundedRectangle(width=w, height=h, corner_radius=radius)
    return DashedVMobject(r, num_dashes=dashes or int((w + h) * 7), dashed_ratio=0.55).set_stroke(color, stroke)


def ghost_sheet(env, text):
    """A GREY dashed sheet the size of `env`'s sheets: something absent."""
    w, h = env.env_w - 0.5, env.pitch - 0.1
    fr = dashed_frame(w, h, S.GREY, radius=0.06, dashes=40)
    t = label(text, 20, S.GREY).move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.3)
    return VGroup(fr, t)


def staple_glyph(x, y):
    """Two short GREY staples across a joint at x, centred on y."""
    return VGroup(*[Line([x - 0.16, y + dy, 0], [x + 0.16, y + dy, 0], color=S.GREY, stroke_width=4)
                    for dy in (0.2, -0.2)])


def grid(n_rows, n_cols, w=0.55, h=0.34, gap=0.12, color=DATA):
    cards = VGroup(*[chunk_card(w, h, color) for _ in range(n_rows * n_cols)])
    cards.arrange_in_grid(n_rows, n_cols, buff=(gap, gap))
    return cards


def ghost_card(card):
    """A GREY dashed ghost at `card`'s place (an old-book chunk)."""
    fr = dashed_frame(card.width, card.height, S.GREY, radius=0.06, dashes=14).move_to(card)
    marks = card[1].copy().set_stroke(S.GREY, opacity=0.6)
    return VGroup(fr, marks)


def chat_box(width):
    """An empty chat box: a rounded input field with a GREY send arrow (no text)."""
    fr = RoundedRectangle(width=width, height=0.5, corner_radius=0.22, stroke_color=S.GREY,
                          stroke_width=2).set_fill(S.BG, 1)
    send = Polygon([0, 0.12, 0], [0.22, 0, 0], [0, -0.12, 0], stroke_width=0).set_fill(S.GREY, 1)
    send.move_to(fr.get_right() + LEFT * 0.35)
    return VGroup(fr, send)


class CallTwo(VoiceScene):
    def construct(self):
        assert len(SAY) == 12, len(SAY)

        # ============================================================ 0 · the dispatcher
        tr = switch_section(self, None, "Agents", 1, run_time=0.5)
        cs = CallStrip()
        probe = tracker("Agents", 1)                # right of the tracker even with " · extra"
        probe.caption.become(caption_extra(probe, True).target_mobject)
        place(cs, left=probe.get_right()[0] + 0.3, cy=tr.get_center()[1] - 0.02)
        cs.steps[0].set_color(TURN)                 # where S06 left it: call 1
        chip459 = excerpt_chip(SUB459, "cli.py · line 459 (excerpt)", line=L459)
        place(chip459, left=SAFE_L, top=TOP_Y)
        cap0 = VGroup(label("hand the calls", 22, INK), label("to the dispatcher", 22, INK)) \
            .arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        place(cap0, left=chip459.get_right()[0] + 0.3, cy=chip459.chip.get_center()[1])
        assert cap0.get_right()[0] < SAFE_R
        p0 = place(src_panel("agent_tools.py", 84, 94), left=SAFE_L, top=1.78)
        p1 = place(src_panel("agent_tools.py", [(95, 100), (103, 107)]), left=SAFE_L, top=1.78)
        c0, c1 = p0.code.code_lines, p1.code.code_lines
        b88 = p0.bar(88, TURN)
        n88 = line_note("match the name", TURN).next_to(c0[p0.rows_of(88)[0]], RIGHT, buff=0.25)
        assert n88.get_right()[0] < SAFE_R
        b95 = VGroup(*[p1.bar(n, DATA) for n in range(95, 101)])
        b103 = VGroup(*[p1.bar(n, CTR) for n in range(103, 108)])
        y95 = (c1[p1.rows_of(95)[0]].get_center()[1] + c1[p1.rows_of(100)[0]].get_center()[1]) / 2
        y103 = (c1[p1.rows_of(103)[0]].get_center()[1] + c1[p1.rows_of(107)[0]].get_center()[1]) / 2
        n95 = line_note("call the real function", DATA)
        place(n95, left=p1.get_right()[0] + 0.3, cy=y95)
        n103 = line_note("wrap the result", CTR)
        place(n103, left=p1.get_right()[0] + 0.3, cy=y103)
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(cs, shift=DOWN * 0.1), run_time=0.4)
            self.play(cs.light(1), run_time=0.4)
            self.play(FadeIn(chip459, shift=DOWN * 0.1), FadeIn(cap0, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("a dispatcher matches")
            self.play(FadeIn(p0, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("matches each call's name")
            self.play(FadeIn(b88), FadeIn(n88, shift=LEFT * 0.15), run_time=0.5)
            self.play(Indicate(p0.span(88, 'function_call.name == "get_book_by_author"'), color=TURN,
                               scale_factor=1.05), run_time=0.7)
            vo.wait_until("runs the real function")
            self.play(FadeOut(VGroup(b88, n88)), FadeTransform(p0, p1), run_time=0.8)
            self.play(FadeIn(b95), FadeIn(n95, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("and wraps the result")
            self.play(FadeIn(b103), FadeIn(n103, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("as a function response")
            self.play(Indicate(p1.span(104, "types.Part.from_function_response("), color=CTR,
                               scale_factor=1.05), run_time=0.8)

        # ============================================================ 1 · the staff's call, our dispatcher
        rows1 = [
            label("“feed the model's call from the staff's run through", 20, INK),
            VGroup(mono("agent_tools.execute_function_calls", 20, INK),
                   label(", against this collection”", 20, INK)).arrange(RIGHT, buff=0.06),
            VGroup(standin_tag(), label("a stored chunk's vector replaces Google's embedding", 20, LOOKUP))
            .arrange(RIGHT, buff=0.2),
        ]
        rows1[1][1].align_to(rows1[1][0], DOWN)
        xc = two_line_extra(rows1)
        place(xc, left=SAFE_L, top=TOP_Y)
        t1 = term(rows=7, container=True)
        items1 = [D36, D_FOLD, D45, D48]
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(p1, b95, b103, n95, n103, chip459, cap0)), caption_extra(tr, True),
                      run_time=0.6)
            vo.wait_until("an extra script")
            self.play(FadeIn(xc, shift=DOWN * 0.15), run_time=0.6)
            vo.wait_until("feeds the staff's recorded call")
            self.play(FadeIn(t1, shift=UP * 0.3), run_time=0.5)
            out1a = t1.print(self, items1[:2], wrap=True, run_time=0.6)
            fold_row = rows_of_line(out1a, items1[:2], 1)[0]
            self.play(Indicate(fold_row, color=CLOUD, scale_factor=1.04), run_time=0.7)
            vo.wait_until("through the tutorial's own dispatcher")
            out1b = t1.print(self, items1[2:], wrap=True, run_time=0.6)
            r45 = rows_of_line(out1b, items1[2:], 0)[0]
            self.play(Indicate(substring(r45, "Function: get_book_by_author"), color=TURN, scale_factor=1.06),
                      run_time=0.7)
            vo.wait_until("against our collection")
            self.play(Indicate(rows1[1][1], color=INK, scale_factor=1.06), run_time=0.7)
        r36 = rows_of_line(out1a, items1[:2], 0)
        r48 = rows_of_line(out1b, items1[2:], 1)

        # ============================================================ 2 · one stand-in
        st = TrustStage(compact=True)
        st.shift(UP * (2.8 - st.get_top()[1]))
        band_top, band_bot = 0.82, -1.3
        band = dashed_frame(SAFE_R - SAFE_L, band_top - band_bot, CTR, stroke=2, radius=0.16)
        band.move_to([0, (band_top + band_bot) / 2, 0])
        legend_t = mono("inside llm-rag-cli", 20, CTR)
        legend_bg = RoundedRectangle(width=legend_t.width + 0.3, height=legend_t.height + 0.12, corner_radius=0.08,
                                     stroke_width=0).set_fill(S.BG, 1)
        legend = VGroup(legend_bg, legend_t)
        place(legend, cx=st.parts["cli"].frame.get_center()[0], cy=band_top)
        legend_t.move_to(legend_bg)
        cc = call_card()
        place(cc, left=SAFE_L + 0.2, top=band_top - 0.2)
        sc_glyphs = substring(cc.rows[2], "search_content")
        au_glyphs = substring(cc.rows[1], "author")
        cyl = st.parts["chroma"].cyl
        vec = dashed_vector()
        vec_at = np.array([cc.frame.get_right()[0] + 0.95, sc_glyphs.get_center()[1] + 0.05, 0])
        vec_tag = standin_tag()
        place(vec_tag, cx=vec_at[0] - 0.05, bottom=vec_at[1] + 0.35)
        vec_arrow = Arrow([cc.frame.get_right()[0] + 0.02, sc_glyphs.get_center()[1], 0],
                          [vec_at[0] - 0.42, sc_glyphs.get_center()[1], 0], buff=0.04, color=LOOKUP,
                          stroke_width=3, max_tip_length_to_length_ratio=0.3, tip_length=0.14)
        q1 = mono_line("collection.query(…, n_results=10,", 20, INK)
        q2 = mono_line('    where={"author": …})', 20, INK)
        qlab = VGroup(q1, q2).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        place(qlab, left=max(vec_at[0] + 0.75, vec_tag.get_right()[0] + 0.3), top=band_top - 0.3)
        assert qlab.get_right()[0] < SAFE_R - 0.1 and vec_tag.get_top()[1] < band_top - 0.05
        q_dots = substring(q1, "…")
        q_auth = substring(q2, '"author"')
        q_arrow = Arrow([cyl.get_center()[0], qlab.get_top()[1] + 0.02, 0],
                        [cyl.get_center()[0], cyl.get_bottom()[1] - 0.02, 0], buff=0.0, color=LOOKUP,
                        stroke_width=4, max_tip_length_to_length_ratio=0.2, tip_length=0.18)
        assert legend.get_right()[0] < q_arrow.get_left()[0] - 0.2 and legend.get_bottom()[1] > qlab.get_top()[1]
        assert legend.get_left()[0] > cc.get_right()[0] - 0.1 or legend.get_bottom()[1] > cc.get_top()[1]
        differ = note("which 10 may differ from a real query's")
        place(differ, left=qlab.get_left()[0], top=qlab.get_bottom()[1] - 0.2)
        with self.voiceover(SAY[2]) as vo:
            r36g = VGroup(*r36)
            self.play(r36g.animate.set_color(LOOKUP), run_time=0.5)
            pin(self, r36[-1], beside(standin_tag(), t1, r36[-1], buff=0.35), run_time=0.4)
            vo.wait_until("without Google")
            srch = wrapped_span(r48, D48, "cheese making importance location")
            self.play(srch.animate.set_color(LOOKUP), run_time=0.5)
            self.play(FadeOut(xc, shift=UP * 0.15), run_time=0.4)
            resize(self, t1, 3, keep=list(r36), run_time=0.7,
                   extra=(FadeIn(st, shift=DOWN * 0.2), FadeIn(band), FadeIn(legend)))
            self.play(FadeIn(cc, shift=RIGHT * 0.2), *st.light("cli"), run_time=0.6)
            self.play(sc_glyphs.animate.set_color(LOOKUP), run_time=0.4)
            vo.wait_until("so a stored chunk's vector")
            vec.move_to(cyl.get_center())
            vec.scale(0.5)
            self.add(vec)
            self.play(vec.animate.scale(2.0).move_to(vec_at), *st.unlight("cli"), run_time=0.9)
            self.play(GrowArrow(vec_arrow), FadeIn(vec_tag, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("and the 10 chunks")
            q_auth.set_opacity(0)
            self.play(FadeIn(qlab, shift=LEFT * 0.15), run_time=0.5)
            v_copy, a_copy = vec.copy(), au_glyphs.copy()
            self.add(v_copy, a_copy)
            self.play(v_copy.animate.scale(0.3).move_to(q_dots).set_opacity(0), q_dots.animate.set_color(LOOKUP),
                      a_copy.animate.move_to(q_auth), run_time=0.7)
            q_auth.set_opacity(1)
            self.remove(v_copy, a_copy)
            self.play(GrowArrow(q_arrow), run_time=0.5)
            self.play(FadeIn(differ, shift=UP * 0.1), run_time=0.4)

        # ============================================================ 3 · ten passages, one string, stapled
        row_y = -1.0
        cards = VGroup(*[chunk_card(0.6, 0.32) for _ in range(10)]).arrange(RIGHT, buff=0.12)
        place(cards, left=cc.get_right()[0] + 0.45, cy=row_y)
        assert cards.get_right()[0] < SAFE_R - 0.1
        targets = [c.get_center() for c in cards]
        for c in cards:
            c.move_to(cyl.get_center()).scale(0.4)
        txt = json_card(CHUNK_ROWS, DATA)
        place(txt, left=targets[0][0] - 0.3, bottom=row_y + 0.26)
        assert txt.get_top()[1] < band_top - 0.05
        mara = substring(txt.rows[0], "Mara")
        anja = substring(txt.rows[1], "Anja")
        string = RoundedRectangle(width=targets[-1][0] - targets[0][0] + 0.6, height=0.22,
                                  corner_radius=0.11, stroke_color=DATA, stroke_width=2).set_fill(DATA, 0.45)
        place(string, left=targets[0][0] - 0.3, cy=row_y)
        one_s = label("one string", 20, DATA).next_to(string, UP, buff=0.12).align_to(string, LEFT)
        rc = response_card(note_="3,509 characters")
        place(rc, cx=2.6, cy=-0.25)
        rc_to = rc.copy()
        place(rc_to, left=cc.frame.get_right()[0] + 0.02, cy=cc.frame.get_center()[1])
        stp = staple_glyph(cc.frame.get_right()[0] + 0.01, cc.frame.get_center()[1])
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(qlab, differ, vec, vec_arrow, vec_tag)), FadeOut(q_arrow),
                      run_time=0.4)
            self.add(cards)
            self.play(LaggedStart(*[c.animate.scale(2.5).move_to(p) for c, p in zip(cards, targets)],
                                  lag_ratio=0.08), run_time=1.2)
            # lines 52, 54 and 56 are empty: print in pairs after the first three, so the 3-row
            # strip always shows two lines of text (51/53, 53/55, 55/57)
            t1.print(self, D_RESP[0:3], run_time=0.4)          # 51-53
            vo.wait_until("from today's story")
            self.play(TransformFromCopy(cards[0], txt), run_time=0.7)
            t1.print(self, D_RESP[3:5], run_time=0.4)          # 54-55
            vo.wait_until("about Mara and Anja")
            self.play(mara.animate.set_color(TURN), run_time=0.35)
            t1.print(self, D_RESP[5:7], run_time=0.4)          # 56-57: Anja smiled.
            self.play(anja.animate.set_color(TURN), run_time=0.35)
            t1.print(self, D_RESP[7:8], run_time=0.3)          # …
            vo.wait_until("Joined into one string")
            self.play(FadeOut(txt, shift=DOWN * 0.2), run_time=0.4)
            self.play(ReplacementTransform(cards, string), FadeIn(one_s, shift=UP * 0.1), run_time=0.8)
            out135 = t1.print(self, [D135], wrap=True, run_time=0.4)
            vo.wait_until("of 3,509 characters")
            n3509 = wrapped_span(list(out135), D135, "3509 characters")
            self.play(n3509.animate.set_color(TURN), run_time=0.4)
            self.play(FadeOut(one_s), ReplacementTransform(string, rc), run_time=0.8)
            vo.wait_until("they're stapled")
            self.play(rc.animate.move_to(rc_to.get_center()), run_time=0.8)
            self.play(Create(stp), run_time=0.3)                # the staple is the narrated thing
            self.play(Indicate(stp, color=TURN, scale_factor=1.5), run_time=0.5)

        # ============================================================ 4 · call 2 sends three things
        p4 = src_panel("cli.py", 464, 477, join=[(470, 472)], cut_comments=True, size=20)
        place(p4, left=SAFE_L, top=TOP_Y)
        c4 = p4.code.code_lines
        env = Envelope(width=3.8, slots=4)
        env.move_to([4.35, 0.55, 0])
        assert env.get_left()[0] > p4.get_right()[0] + 0.2
        env_l = label("call 2", 22, S.GREY)
        b468, b469, b470, b475 = p4.bar(468, S.GREY), p4.bar(469, CLOUD), p4.bar(470, CTR), p4.bar(475, DATA)
        s_q = env.sheet("the question", S.GREY)
        s_m = env.sheet("the model's turn", CLOUD, with_seal=True)
        s_r = env.sheet("your function responses", CTR)
        ghost = ghost_sheet(env, "no tool config").move_to(env.slot_point(3))
        menu = chip("the menu", DATA, size=20, fill_opacity=0.14)
        body = env.parts["body"]
        place(menu, right=body.get_right()[0] - 0.25, top=body.get_bottom()[1] - 0.12)
        place(env_l, left=body.get_left()[0] + 0.25, cy=menu.get_center()[1])
        clip = Line(menu.get_top() + UP * 0.02, [menu.get_center()[0], body.get_bottom()[1] + 0.2, 0],
                    color=DATA, stroke_width=4)
        r474 = c4[p4.rows_of(474)[0]]
        gtxt = VGroup(label("no", 20, S.GREY), mono("tool_config", 20, S.GREY),
                      label("→ mode back to automatic", 20, S.GREY)).arrange(RIGHT, buff=0.1)
        gfr = dashed_frame(gtxt.width + 0.5, gtxt.height + 0.3, S.GREY, radius=0.12)
        gfr.move_to(gtxt)
        gnote = VGroup(gfr, gtxt)
        place(gnote, left=SAFE_L + 0.6, top=p4.get_bottom()[1] - 0.3)
        x_lead = r474.get_left()[0] - 0.25
        lead = VMobject().set_points_as_corners([[x_lead, gnote.get_top()[1], 0],
                                                 [x_lead, r474.get_center()[1], 0],
                                                 [r474.get_left()[0] - 0.06, r474.get_center()[1], 0]])
        glead = DashedVMobject(lead, num_dashes=18, dashed_ratio=0.55).set_stroke(S.GREY, 2)

        def fly(row_bar, sheet):
            sheet.move_to(row_bar.get_center()).align_to(row_bar, RIGHT)
            return FadeTransform(row_bar.copy(), sheet)

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(st, band, legend, cc, rc, stp, t1)), caption_extra(tr, False),
                      run_time=0.6)
            self.play(FadeIn(p4, shift=UP * 0.15), FadeIn(env, scale=0.9), FadeIn(env_l), cs.light(2),
                      run_time=0.7)
            vo.wait_until("the question")
            self.play(FadeIn(b468), run_time=0.3)
            self.play(fly(b468, s_q), run_time=0.4)
            env.add_sheet(self, s_q, run_time=0.5)
            vo.wait_until("the model's own turn")
            self.play(FadeIn(b469), run_time=0.3)
            self.play(fly(b469, s_m), run_time=0.4)
            env.add_sheet(self, s_m, run_time=0.5)
            vo.wait_until("and your function responses")
            self.play(FadeIn(b470), run_time=0.3)
            self.play(fly(b470, s_r), run_time=0.4)
            env.add_sheet(self, s_r, run_time=0.5)
            vo.wait_until("The tools go along again")
            self.play(FadeIn(b475), run_time=0.3)
            self.play(FadeIn(menu, shift=UP * 0.2), Create(clip), run_time=0.5)
            vo.wait_until("but no tool config")
            self.play(FadeIn(ghost), Create(glead), FadeIn(gnote, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("the mode is back to automatic")
            self.play(Indicate(gtxt[2], color=S.GREY, scale_factor=1.06), run_time=0.7)

        # ============================================================ 5 · the request: the seal goes back
        ref = lref("39")
        duty = concept_box("interpret its outputs", h=0.42)
        place(duty, right=SAFE_R, top=ref.get_bottom()[1] - 0.06)
        t5 = term(rows=13, container=True)
        t5.shift(DOWN * 0.05)
        assert duty.get_bottom()[1] > t5.box.get_top()[1] + 0.01
        seal_fly = s_m.seal.copy()
        with self.voiceover(SAY[5]) as vo:
            self.add(seal_fly)
            self.play(FadeIn(ref), FadeIn(duty, shift=DOWN * 0.1), *env.open(),
                      FadeOut(VGroup(p4, b468, b469, b470, b475, gnote, glead)), caption_extra(tr, True),
                      run_time=0.6)
            self.play(duty.box.animate.set_stroke(TURN), duty.text.animate.set_color(TURN), run_time=0.3)
            # the envelope's frame becomes the terminal (its sheets fade: their rows print next)
            shell = env.parts["body"].copy()
            chrome = VGroup(t5.bar, t5.dots, t5.title)
            self.add(shell)
            self.play(FadeOut(VGroup(env, env_l, ghost, menu, clip)), Transform(shell, t5.box.copy()),
                      run_time=0.5)
            self.play(FadeIn(chrome), run_time=0.25)
            self.remove(shell, chrome)
            self.add(t5)
            out5 = t5.print(self, REQ, run_time=0.7, lag=0.06)
            self.play(substring(out5[7], '"functionResponse"').animate.set_color(CTR),
                      out5[11].animate.set_color(S.GREY), run_time=0.3)
            pin(self, out5[12], beside(notsent_tag(), t5, out5[12], buff=0.4), run_time=0.3)
            ts = substring(out5[3], '"thoughtSignature":')
            box_ts = ring(ts, CLOUD, buff=0.06)
            self.play(Create(box_ts), run_time=0.4)
            seal_to = np.array([out5[3].glyphs.get_right()[0] + 0.35, out5[3].strut.get_center()[1], 0])
            self.play(seal_fly.animate(path_arc=-0.6).move_to(seal_to).scale(1.3), run_time=0.8)
            vo.wait_until("Gemini's thinking models")
            x_rule = out5[2].glyphs.get_left()[0] - 0.22
            rule = Line([x_rule, out5[2].strut.get_top()[1], 0], [x_rule, out5[5].strut.get_bottom()[1], 0],
                        color=CLOUD, stroke_width=4)
            turn_l = label("the model's own turn", 22, CLOUD)
            place(turn_l, left=out5[5].glyphs.get_right()[0] + 0.5, cy=out5[5].strut.get_center()[1])
            self.play(Create(rule), FadeIn(turn_l, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("and want it back")
            self.play(Indicate(VGroup(ts, seal_fly), color=CLOUD, scale_factor=1.1), run_time=0.8)
            vo.wait_until("Resending the turn unchanged")
            kept = label("unchanged · seal kept", 22, CLOUD)
            place(kept, left=turn_l.get_left()[0], cy=out5[6].strut.get_center()[1])
            self.play(FadeIn(kept, shift=UP * 0.1), Indicate(seal_fly, color=CLOUD, scale_factor=1.3),
                      run_time=0.7)

        # ============================================================ 6 · the staff's answer
        st6 = TrustStage(compact=True)
        st6.shift(UP * (2.8 - st6.get_top()[1]))
        md = st6.parts["model"]
        lap = st6.parts["laptop"]
        cli_fr = st6.parts["cli"].frame
        margin_y = (cli_fr.get_bottom()[1] + lap.get_bottom()[1]) / 2
        small = Envelope(width=0.9, slots=1, pitch=0.2, margin=0.12)
        small.move_to([st6._bx.get_center()[0] + 0.75, margin_y + 0.08, 0])
        prose_fr = box(1.1, 0.5, CLOUD, fill=S.BG, fill_opacity=1.0, radius=0.1)
        prose = VGroup(prose_fr, answer_bars(3, 0.75, CLOUD, h=0.07).move_to(prose_fr))
        prose.move_to(md)
        maxc = int((12.9 - 0.5) / 0.1667) - 1
        a_rows = [A99] + wrap_words(A105, maxc) + wrap_words(A111, maxc) + wrap_words(A112, maxc)
        lp = log_panel(a_rows, "out.txt · lines 98–111 (excerpt)", width=12.9)
        place(lp, cx=0, top=TOP_Y - 0.15)
        for r in lp.rows:
            if "↪" in r.text:
                substring(r, "↪").set_color(S.GREY)
        stf = staff_run_tag(old_book=True).next_to(lp.header, RIGHT, buff=0.35)
        assert stf.get_right()[0] < SAFE_R
        alp = phrase_glyphs(lp.rows, "Alpine region,")
        cav = phrase_glyphs(lp.rows, "limestone caves")
        trh = phrase_glyphs(lp.rows, "transhumance")[0]
        mov = phrase_glyphs(lp.rows, "the seasonal movement of livestock")
        g1 = VGroup(label("call 1", 20, S.GREY), tag("247 tokens", COST)).arrange(RIGHT, buff=0.15)
        g2 = VGroup(label("call 2", 20, S.GREY), tag("1,269 tokens", COST)).arrange(RIGHT, buff=0.15)
        src6 = note("out.txt · lines 49, 135")
        golds = VGroup(g1, g2, src6).arrange(RIGHT, buff=0.5)
        place(golds, cx=0, top=lp.frame.get_bottom()[1] - 0.35)
        assert golds.get_bottom()[1] > -3.55
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(box_ts, rule, turn_l, kept)), FadeOut(duty), caption_extra(tr, False),
                      FadeTransform(t5, small), seal_fly.animate.move_to(small).scale(0.5).set_opacity(0),
                      FadeIn(st6, shift=DOWN * 0.2), run_time=0.7)
            self.remove(seal_fly)
            self.play(small.animate.move_to(md.get_center()).scale(0.5), run_time=0.6)
            self.play(FadeOut(small, scale=0.5), Indicate(md, color=CLOUD, scale_factor=1.1), run_time=0.4)
            prose.scale(0.5)
            self.add(prose)
            back = np.array([st6._bx.get_center()[0] + 0.25 + prose.width, margin_y, 0])
            self.play(prose.animate.scale(2.0).move_to(back), run_time=0.6)
            self.play(FadeTransform(prose, lp), FadeIn(stf), FadeOut(st6), run_time=0.7)
            vo.wait_until("An Alpine valley")
            u_alp = VGroup(*[under(g, CLOUD, 3) for g in alp])
            self.play(Create(u_alp), run_time=0.4)
            vo.wait_until("its caves")
            u_cav = VGroup(*[under(g, CLOUD, 3) for g in cav])
            self.play(Create(u_cav), run_time=0.4)
            vo.wait_until("and transhumance")
            self.play(trh.animate.set_color(TURN), run_time=0.3)
            self.play(Indicate(trh, color=TURN, scale_factor=1.15), run_time=0.6)
            vo.wait_until("the seasonal movement")
            u_mov = VGroup(*[under(g, CLOUD, 3) for g in mov])
            self.play(Create(u_mov), run_time=0.5)
            vo.wait_until("The two calls used")
            self.play(FadeIn(g1, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("and 1,269 tokens")
            self.play(FadeIn(g2, shift=UP * 0.1), FadeIn(src6), run_time=0.5)

        # ============================================================ 7 · who searched, who chose
        q1h = label("Who searched your database?", 28, TURN)
        q2h = label("Who chose the book?", 28, TURN)
        a1h = label("your Python, on your laptop", 28, DATA)
        a2h = label("Gemini wrote the call", 28, CLOUD)
        ar1 = label("→", 28, S.GREY)
        ar2 = label("→", 28, S.GREY)
        qx = -5.2
        ax = qx + q1h.width + 1.0
        q1h.move_to([qx, 1.3, 0], aligned_edge=LEFT)
        q2h.move_to([qx, 0.4, 0], aligned_edge=LEFT)
        ar1.move_to([ax - 0.45, 1.3, 0])
        ar2.move_to([ax - 0.45, 0.4, 0])
        a1h.move_to([ax, 1.3, 0], aligned_edge=LEFT)
        a2h.move_to([ax, 0.4, 0], aligned_edge=LEFT)
        hook_body = VGroup(q1h, q2h, ar1, ar2, a1h, a2h)
        hfr = box(hook_body.width + 0.9, hook_body.height + 0.8, TURN, fill=S.BG, fill_opacity=0.95, radius=0.16)
        hfr.move_to(hook_body)
        hook = VGroup(hfr, hook_body)
        hook.shift(RIGHT * -hook.get_center()[0])
        gold7 = tag("2 Gemini calls + 1 embedding call per question", COST)
        place(gold7, cx=0, top=hfr.get_bottom()[1] - 0.45)
        src7 = VGroup(label("the embedding:", 20, S.GREY), mono("agent_tools.py", 20, S.GREY),
                      label("· line 43 →", 20, S.GREY), mono("cli.py", 20, S.GREY),
                      label("· lines 75–84", 20, S.GREY)).arrange(RIGHT, buff=0.12)
        place(src7, cx=0, top=gold7.get_bottom()[1] - 0.2)
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(lp, stf, u_alp, u_cav, u_mov, golds)), run_time=0.5)
            self.play(FadeIn(hfr, scale=0.95), Write(q1h), run_time=0.7)
            self.play(Write(q2h), run_time=0.6)
            vo.wait_until("Gemini wrote the call")
            self.play(FadeIn(ar2), FadeIn(a2h, shift=LEFT * 0.15), run_time=0.6)
            vo.wait_until("your Python ran it")
            self.play(FadeIn(ar1), FadeIn(a1h, shift=LEFT * 0.15), run_time=0.6)
            vo.wait_until("That's two model calls")
            self.play(FadeIn(gold7, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("and one embedding call")
            self.play(FadeIn(src7, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("all paid")
            self.play(Indicate(gold7, color=COST, scale_factor=1.06), run_time=0.6)

        # ============================================================ 8 · the book changed under the run
        xc8 = extra_card("count four of the answer's words in out.txt, today's book, and the book before 85bba32")
        place(xc8, cx=0, top=TOP_Y + 0.04)
        t8 = term(P_REPO, rows=11, title=SECOND, size=20)
        assert xc8.get_bottom()[1] > t8.box.get_top()[1] + 0.1
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(hook, gold7, src7)), FadeOut(ref), FadeOut(cs), caption_extra(tr, True),
                      run_time=0.5)
            self.play(FadeIn(xc8, shift=DOWN * 0.15), FadeIn(t8, shift=UP * 0.3), run_time=0.6)
            tab = t8.print(self, TABLE, run_time=0.6)
            vo.wait_until("never says transhumance")
            reds = []
            for ln in tab:
                a = ln.text.index("book today")
                reds.append(col_box(ln, a, a + len("book today  0"), ERR))
            self.play(Create(reds[0]), run_time=0.4)
            vo.wait_until("nor three other words")
            self.play(LaggedStart(*[Create(r) for r in reds[1:]], lag_ratio=0.3), run_time=0.7)
            vo.wait_until("the commit that added")
            cmd8 = type_cmd(self, t8, GIT_CMD, 1.8)
            pin(self, cmd8, beside(extra_tag(), t8, cmd8), run_time=0.3)
            out8 = t8.print(self, [G2] + C09.at(4, 5, 6), run_time=0.5)
            u_hash = under(substring(out8[0], "85bba32"), TURN, 3)
            u_book = under(substring(out8[1], "input-datasets/books/Tolminc Cheese.txt"), TURN, 3)
            u_out = under(substring(out8[2], "out.txt"), TURN, 3)
            self.play(Create(u_hash), Create(u_book), Create(u_out), run_time=0.6)
            vo.wait_until("The staff's index")
            greens = []
            for ln in tab:
                a = ln.text.index("book before")
                greens.append(col_box(ln, a, len(ln.text), DATA))
            self.play(LaggedStart(*[Create(g) for g in greens], lag_ratio=0.2), run_time=0.8)

        # ============================================================ 9 · an index answers from what was loaded
        cy9 = cylinder(1.2, 1.4)
        cy9.move_to([-4.7, 0.75, 0])
        cl9 = mono("char-split-collection", 20, CTR).next_to(cy9, DOWN, buff=0.22)
        place(cl9, left=max(SAFE_L, cl9.get_left()[0]))
        slot = dashed_frame(8.9, 2.1, CTR, stroke=2, radius=0.16)
        place(slot, right=SAFE_R - 0.05, cy=0.75)
        assert slot.get_left()[0] > cl9.get_right()[0] + 0.2
        link = Line(cy9.get_right() + RIGHT * 0.06, [slot.get_left()[0] - 0.04, cy9.get_center()[1], 0],
                    color=CTR, stroke_width=3)
        card_kw = dict(w=0.78, h=0.42, gap=0.14)    # 24 cards fill the slot: 3 rows of 8
        old = grid(3, 4, **card_kw)
        old.move_to(slot)
        ghosts = VGroup(*[ghost_card(c) for c in old])
        ghost_to = ghosts.copy().scale(0.8)
        place(ghost_to, left=slot.get_left()[0] + 0.3, top=slot.get_bottom()[1] - 0.3)
        old_tag = tag("old book", S.GREY).next_to(ghost_to, LEFT, buff=0.3)
        new = grid(3, 8, **card_kw)
        new.move_to(slot)
        assert new.width < slot.width - 0.5 and new.height < slot.height - 0.3
        new_l = label("today's book · 24 chunks", 20, DATA)
        place(new_l, right=slot.get_right()[0], bottom=slot.get_top()[1] + 0.12)
        words = VGroup(*[chip(w, DATA, size=20, fill_opacity=0.12) for w in ("Mara", "the curd", "the wheels")])
        words.arrange(RIGHT, buff=0.3)
        place(words, right=slot.get_right()[0], top=slot.get_bottom()[1] - 0.3)
        assert words.get_left()[0] > ghost_to.get_right()[0] + 0.3 and old_tag.get_top()[1] < cl9.get_bottom()[1] - 0.1
        cap9 = VGroup(label("an index answers from what was loaded", 24, INK),
                      label("· lecture 5", 24, S.GREY)).arrange(RIGHT, buff=0.15)
        place(cap9, cx=0, cy=-2.75)
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(VGroup(xc8, t8, *reds, *greens, u_hash, u_book, u_out)), caption_extra(tr, False),
                      run_time=0.5)
            self.play(FadeIn(cy9), FadeIn(cl9), Create(link), FadeIn(slot), FadeIn(old), run_time=0.6)
            self.play(FadeOut(old), FadeIn(ghosts), run_time=0.5)
            self.play(ghosts.animate.scale(0.8).move_to(ghost_to), FadeIn(old_tag, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("draws on passages")
            self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 1.0) for c in new], lag_ratio=0.03),
                      FadeIn(new_l), run_time=1.1)
            vo.wait_until("Mara")
            self.play(FadeIn(words[0], shift=UP * 0.1), run_time=0.35)
            vo.wait_until("the curd")
            self.play(FadeIn(words[1], shift=UP * 0.1), run_time=0.35)
            vo.wait_until("the wheels")
            self.play(FadeIn(words[2], shift=UP * 0.1), run_time=0.35)
            vo.wait_until("An index answers")
            self.play(FadeIn(cap9, shift=UP * 0.1), Indicate(slot, color=CTR, scale_factor=1.02), run_time=0.7)

        # ============================================================ 10 · the slip: print(response)
        rc266 = readme_chip("README.md · line 266", "Displays the LLM's response", expected=True)
        err10 = erratum_tag()
        top10 = VGroup(rc266, err10).arrange(RIGHT, buff=0.2)
        place(top10, cx=0, cy=1.9)
        p478 = src_panel("cli.py", 478)
        place(p478, cx=0, top=1.2)
        resp = p478.span(478, "response")
        u_resp = under(resp, ERR, 4)
        fx = fix_chip("print(response.text)", font=MONO)
        fx_n = label("just the answer", 22, INK)
        fix_row = VGroup(fx, fx_n).arrange(RIGHT, buff=0.3)
        place(fix_row, cx=0, top=p478.get_bottom()[1] - 0.7)
        fx_arrow = Arrow([0, p478.get_bottom()[1] - 0.05, 0], [0, fix_row.get_top()[1] + 0.05, 0], buff=0,
                         color=S.GREY, stroke_width=3, max_tip_length_to_length_ratio=0.3, tip_length=0.16)
        fx_arrow.set_x(fx.get_center()[0])
        with self.voiceover(SAY[10]) as vo:
            self.play(FadeOut(VGroup(cy9, cl9, link, slot, ghosts, old_tag, new, new_l, words, cap9)),
                      run_time=0.5)
            self.play(FadeIn(rc266, shift=DOWN * 0.1), run_time=0.5)
            self.play(FadeIn(err10, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("the README promises")
            self.play(Indicate(rc266.phrase, color=TURN, scale_factor=1.06), run_time=0.7)
            vo.wait_until("but line 478")
            self.play(FadeIn(p478, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("the whole response object")
            self.play(Create(u_resp), run_time=0.5)
            self.play(Indicate(resp, color=ERR, scale_factor=1.1), run_time=0.6)
            vo.wait_until("Print response dot text")
            self.play(GrowArrow(fx_arrow), FadeIn(fx, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("for just the answer")
            self.play(FadeIn(fx_n, shift=LEFT * 0.1), run_time=0.4)

        # ============================================================ 11 · step 2: the hosted Cheese Agent Tool
        rc271 = readme_chip("README.md · line 271", "Use Chrome browser for best performance", expected=True)
        place(rc271, cx=0, top=2.75)
        bw = browser_window("ac215-llm-rag.dlops.io/agent", width=8.0, height=2.8)
        place(bw, cx=0, top=rc271.get_bottom()[1] - 0.3)
        cb = chat_box(6.4)
        place(cb, cx=bw.get_center()[0], bottom=bw.frame.get_bottom()[1] + 0.3)
        ill = illustration_tag()
        place(ill, left=bw.get_right()[0] + 0.25, top=bw.get_top()[1])
        t11 = term(P_REPO, rows=4, title=SECOND)     # the container still runs (S08 types exit)
        assert bw.get_bottom()[1] > t11.box.get_top()[1] + 0.05
        with self.voiceover(SAY[11]) as vo:
            self.play(FadeOut(VGroup(top10, p478, u_resp, fx_arrow, fix_row)), tr.goto(2), run_time=0.5)
            self.play(FadeIn(bw, shift=UP * 0.15), FadeIn(cb), FadeIn(ill), run_time=0.6)
            vo.wait_until("hosted Cheese Agent Tool")
            self.play(FadeIn(t11, shift=UP * 0.3), caption_extra(tr, True), run_time=0.4)
            cmd11 = type_cmd(self, t11, CURL_CMD, 1.4)
            # beside the command's first row: on its last row the tag would sit right above the
            # "at the time of recording" tag of the output row and touch it
            row11 = cmd11.rows[0] if hasattr(cmd11, "rows") else cmd11
            pin(self, row11, beside(extra_tag(), t11, row11), run_time=0.3)
            out11 = t11.print(self, [C11.line(2)], run_time=0.4)
            pin(self, out11[0], beside(recording_tag(), t11, out11[0], buff=0.4), run_time=0.3)
            vo.wait_until("try it in Chrome")
            self.play(FadeIn(rc271, shift=DOWN * 0.1), run_time=0.5)
        self.wait(1.0)
        self.play(FadeOut(VGroup(tr, rc271, bw, cb, ill, t11)), run_time=0.8)
        self.wait(0.3)
