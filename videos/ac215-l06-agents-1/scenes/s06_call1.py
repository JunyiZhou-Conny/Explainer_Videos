"""S06 · Call 1: the model writes the call (llm-rag › Agents step 1; lecture slides 35, then 10–13).

Beats (script.md "## S06", one voiceover block each):
0. TRACKER Agents 1; the call strip under it lights "call 1". CODE(cli.py: 431–437) (line 435
   wrapped, masked): the user turn, the question PINK, role="user" barred. At "Then comes the first
   call" it Transforms into CODE(cli.py: 441–452); generate_content flashes BLUE.
1. Line 445 YELLOW; line 446 GREEN "← the menu"; lines 447–451 YELLOW, mode="any" boxed. LECTURE 35
   at "The lecture lists": a GREY dashed chip (slide 35, our words) "LLM core: model · parameters ·
   response format" beside line 445; temperature=0 flashes.
2. TRACKER Agents 1 · extra. The lecture tag leaves; the boxed mode="any" becomes an excerpt chip
   (cli.py · line 449); a 6-row TEAL container terminal types the extra one-liner (folds, `extra`
   tag) → TERM(cli-container/32: 2–4). Both ANY turn YELLOW; a GREY arrow from the chip, caption
   "the model must answer with a function call".
3. LECTURE 10–13. V3's column returns (the two GREEN menu cards, the GREY dashed "retrieval
   decision" card); beside it a GREY dashed Self-RAG box: "Retrieve?" with yes/no branches, tag
   `concept · lecture only`. A RED line crosses out "retrieval decision"; a YELLOW ring hops over the
   two menu cards; caption "chooses which search · never whether"; GREY chip "exercise: delete
   tool_config, then greet it".
4. The lecture tag leaves. V2: a closed envelope "call 1" opens and becomes a full-width TEAL
   terminal; the extra card "runs agent() unchanged · prints the request instead of sending it"
   (top right, TRACKER · extra); TERM(cli-container/31: 20 wrap, the six folds of script.md, 95
   GREY), 12 rows; `built, not sent` beside line 95. Line 20's locations/global and
   gemini-3.1-flash-lite BLUE; then, as named: the question PINK, both declaration names and "enum"
   GREEN, "mode": "ANY" and "temperature": 0.0 YELLOW.
5. A GREY dashed ghost card "systemInstruction" slides in next to the body (top band, where the
   extra card was) with `erratum · never sent (as in lecture 5)` and "defined at cli.py lines 40–58".
6. TRACKER Agents 1. The terminal clears and types `python cli.py --agent --chunk_type char-split`
   → TERM(cli-container/30: 2–3, 8–10, 16–17, …, 71; wrap); `real run · no key` beside agent();
   GREEN tag "the lookup passed" beside line 10; line 71 RED. A GREY "with your key, look for"
   card (top right): `LLM Response:` with a function_call · cli.py line 454.
7. The terminal clears and leaves; the call strip moves up beside the tracker; V3's stage
   (compact) returns in the upper part; PANEL(expected/out-txt-agent-run.txt: 15 cut + " …",
   21–28, 29 cut) in the lower part (header "out.txt · lines 14–28 (excerpt)", 10 rows, line 23
   masked, staff tag on its header row). The BLUE model's speech bubble becomes the BLUE call card
   {name, args} with its seal ("thought signature"), beside the rows it summarises; the name, the
   author and the PINK search text are marked as named.
8. The search text flashes, GREY tag "4 words"; "the description asked for" + excerpt chip
   agent_tools.py · line 33 "a sentence or two". The id row and the seal pulse.
9. The panel becomes PANEL(out.txt line 52, "out.txt · line 51"): automatic_function_calling_
   history=[] GREY + tag "the SDK ran nothing". The BLUE card moves to the trust boundary
   (extended down), unopened; caption "Gemini wrote arguments · nothing has run yet". A GOLD tick
   "1 paid call" after the call strip. ▶ your turn on a static two-column GREY card (with your
   key: the command; look for, in order; if it fails with your key; GOLD "1 Gemini call · paid").
   Hold 2 s. Everything fades: empty frame.
"""

from common import (
    CLOUD,
    COST,
    DATA,
    ERR,
    INK,
    LOOKUP,
    MASK,
    NARRATION,
    TURN,
    CallStrip,
    Envelope,
    MenuColumn,
    TrustStage,
    beside,
    call_card,
    capture,
    caption_extra,
    concept_box,
    concept_tag,
    cost_tick,
    erratum_tag,
    excerpt,
    excerpt_chip,
    extra_card,
    extra_tag,
    grey_tag,
    log_panel,
    lref,
    note,
    nokey_tag,
    notsent_tag,
    pin,
    ring,
    src_panel,
    staff_run_tag,
    switch_section,
    term,
    type_cmd,
    under,
    your_turn,
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
    Dot,
    FadeIn,
    FadeOut,
    FadeTransform,
    GrowArrow,
    Indicate,
    Polygon,
    RoundedRectangle,
    VGroup,
)

from explainer import style as S
from explainer.devops import box, glyph_range, label, mono, substring, tag
from explainer.scene import VoiceScene

SAY = NARRATION["S06"]

# ------------------------------------------------------------------ the real sources
C32 = capture("32", "cli-container")          # the extra one-liner: mode="any" -> ANY
C31 = capture("31", "cli-container")          # the extra script: call 1's request, built, not sent
C30 = capture("30", "cli-container")          # step 1 with the collection loaded, no key
OUT = capture("out-txt-agent-run", "expected")  # the staff's run (out.txt = file line - 1)

assert C30.cmd == "python cli.py --agent --chunk_type char-split", C30.cmd
assert "ANY" in C32.line(3)
L449 = excerpt("cli.py", 449, 449)
L33 = excerpt("agent_tools.py", 33, 33)
assert 'mode="any"' in L449 and "a sentence or two" in L33

# call 1's request (cli-container/31): line 20 and the script's six folds, every fold checked
REQ_20 = C31.line(20)
REQ = [
    REQ_20,
    C31.fold(21, 31, '{ "contents": [ { "parts": [ { "text": "Describe where cheese making … book?" } ], '
                     '"role": "user" } ],'),
    "  " + C31.fold(32, 41, '"tools": [ { "functionDeclarations": [ { … "name": "get_book_by_author", …'),
    "      " + C31.fold(42, 52, '"enum": [ … ],').replace("[ … ]", "[ … 9 names … ]"),
    "    " + C31.fold(53, 85, '… "name": "get_book_by_search_content" … ],'),
    "  " + C31.fold(86, 90, '"toolConfig": { "functionCallingConfig": { "mode": "ANY" } },'),
    "  " + C31.fold(91, 93, '"generationConfig": { "temperature": 0.0 }'),
]
REQ_95 = C31.line(95)
assert REQ_95.startswith("-- stopped here")

# the staff's recorded response (out.txt lines 14-28)
RESP = [OUT.cut(15, "LLM Response:") + " …"] + OUT.at((21, 28)) + [OUT.cut(29, "=k_") + "…',"]
assert MASK in RESP[3] and "cheese making importance location" in RESP[4], RESP
L52 = OUT.line(52)
assert "automatic_function_calling_history=[]" in L52

AGENT_CMD = C30.cmd
COLS = 65                                    # characters a row in the house terminal

# ------------------------------------------------------------------ layout
TOP_Y = 2.15            # under the call strip (2.28)
PANEL_L = -6.45
BAND_R = 6.45           # the top band right of the call strip: x -2.3 .. 6.45, y 2.26 .. 3.58
BAND_TOP = 3.56


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
    """The glyphs of `sub` in a line Terminal.print(wrap=True) split into `rows` (every row holds
    exactly `width` characters but the last)."""
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


def rows_of_line(printed, items, k):
    """The printed rows (a list) of item k, given the items as passed to Terminal.print(wrap=True)."""
    start = 0
    for n, s in enumerate(items):
        s = s if isinstance(s, str) else s[0]
        cnt = max(1, -(-len(s) // COLS))
        if n == k:
            return list(printed[start:start + cnt])
        start += cnt
    raise IndexError(k)


def line_note(s, color=DATA, size=20, arrow="←"):
    return label(f"{arrow} {s}", size, color)


def speech_bubble(color=CLOUD):
    """The model's speech bubble: a BLUE rounded box with three dots, its tail pointing left
    (at the model)."""
    body = RoundedRectangle(width=0.9, height=0.5, corner_radius=0.18, stroke_color=color,
                            stroke_width=3).set_fill(S.BG, 1)
    tail = Polygon([-0.4, 0.08, 0], [-0.4, -0.12, 0], [-0.66, -0.16, 0], stroke_color=color,
                   stroke_width=3).set_fill(S.BG, 1)
    dots = VGroup(*[Dot(radius=0.05, color=color) for _ in range(3)]).arrange(RIGHT, buff=0.1)
    dots.move_to(body)
    return VGroup(tail, body, dots)


def self_rag(size=20):
    """Slide 10-11's first decision, redrawn: a GREY dashed diamond "Retrieve?" with a "yes" branch
    to retrieval and a "no" branch to answering directly, in a dashed frame titled Self-RAG.
    .diamond .no .yes"""
    dia = Polygon([0, 0.52, 0], [0.92, 0, 0], [0, -0.52, 0], [-0.92, 0, 0])
    dia = DashedVMobject(dia, num_dashes=24, dashed_ratio=0.55).set_stroke(S.GREY, 3)
    dt = label("Retrieve?", size, INK).move_to(dia)
    d = VGroup(dia, dt)
    no_box = concept_box("answer directly", size)
    yes_box = concept_box("retrieve, then answer", size)
    no_box.next_to(d, RIGHT, buff=0.45)
    yes_box.next_to(d, DOWN, buff=0.6).align_to(d, LEFT)
    a_no = Arrow(d.get_right(), no_box.get_left(), buff=0.06, color=S.GREY, stroke_width=3,
                 max_tip_length_to_length_ratio=0.3, tip_length=0.16)
    a_yes = Arrow(d.get_bottom(), [d.get_bottom()[0], yes_box.get_top()[1], 0], buff=0.06, color=S.GREY,
                  stroke_width=3, max_tip_length_to_length_ratio=0.3, tip_length=0.16)
    l_no = label("no", size, S.GREY).next_to(a_no, UP, buff=0.06)
    l_yes = label("yes", size, S.GREY).next_to(a_yes, RIGHT, buff=0.1)
    inner = VGroup(d, no_box, yes_box, a_no, a_yes, l_no, l_yes)
    title = label("Self-RAG", 22, S.GREY)
    title.next_to(inner, UP, buff=0.3).align_to(inner, LEFT)
    content = VGroup(title, inner)
    fr = box(content.width + 0.44, content.height + 0.44, S.GREY, dashed=True, radius=0.16)
    fr.move_to(content)
    g = VGroup(fr, content)
    g.diamond, g.no, g.yes, g.no_branch = d, no_box, yes_box, VGroup(a_no, l_no, no_box)
    return g


def ghost_card(size=20):
    """The GREY dashed ghost of the system instruction that is never sent, with its erratum."""
    key = mono('"systemInstruction"', size, S.GREY)
    err = erratum_tag()
    row1 = VGroup(key, err).arrange(RIGHT, buff=0.35)
    row2 = label("defined at cli.py lines 40–58 · never sent (as in lecture 5)", size, S.GREY)
    rows = VGroup(row1, row2).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    fr = box(rows.width + 0.5, rows.height + 0.36, S.GREY, dashed=True, fill=S.BG, fill_opacity=0.95,
             radius=0.12)
    fr.move_to(rows)
    g = VGroup(fr, rows)
    g.err = err
    return g


def look_for_card(size=20):
    """The GREY "with your key, look for" caption card: one row."""
    ttl = label("with your key, look for", size, S.GREY)
    row = VGroup(mono("LLM Response:", size, INK), label("with a function_call", size, INK),
                 label("· cli.py line 454", size, S.GREY)).arrange(RIGHT, buff=0.15)
    rows = VGroup(ttl, row).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    fr = box(rows.width + 0.5, rows.height + 0.34, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.12)
    fr.move_to(rows)
    return VGroup(fr, rows)


def _row(*parts, buff=0.13):
    return VGroup(*parts).arrange(RIGHT, buff=buff)


def _ind(*parts, buff=0.13, indent=0.4):
    """A row indented by `indent` (an invisible strut first: Text drops leading spaces)."""
    strut = RoundedRectangle(width=indent - buff, height=0.05, corner_radius=0.01, stroke_width=0,
                             fill_opacity=0)
    return VGroup(strut, *parts).arrange(RIGHT, buff=buff)


def turn_card_two_cols(size=20):
    """The static ▶ card of this step: the command on top, two columns (look for, in order · if
    it fails with your key), the GOLD cost line last. .frame .tag"""
    m = lambda s, c=INK: mono(s, size, c)          # noqa: E731
    s = lambda t, c=INK: label(t, size, c)         # noqa: E731
    g = lambda t: label(t, size, S.GREY)           # noqa: E731
    top = _row(s("with your key:"), m(AGENT_CMD))
    left = VGroup(
        g("look for, in order:"),
        _row(m("LLM Response:"), s("with a function_call"), g("· cli.py line 454")),
        _row(m("Function calls:"), g("· line 458")),
        _row(m("Function:"), s("and"), m("Calling function with args:")),
        _ind(g("agent_tools.py lines 87, 89")),
        _row(m("Response:"), s("10 passages from today's story"), g("· line 101")),
        _row(s("a second"), m("LLM Response:"), s("about today's book")),
        _ind(g("cli.py line 478")),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    right = VGroup(
        g("if it fails with your key:"),
        _row(m("DefaultCredentialsError", ERR), s("→")),
        _ind(s("is"), m("llm-service-account.json"), s("in")),
        _ind(m("secrets/,", INK), s("beside llm-rag?")),
        _row(m("403 PERMISSION_DENIED", ERR), s("→")),
        _ind(s("the service account's roles")),
        _ind(g("README.md · lines 56–58")),
        _ind(s("and the Vertex AI API")),
        _row(m("KeyError: 'GCP_PROJECT'", ERR), s("→")),
        _ind(s("start with"), m("sh docker-shell.sh")),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    cols = VGroup(left, right).arrange(RIGHT, aligned_edge=UP, buff=0.55)
    cost = s("1 Gemini call · paid", COST)
    body = VGroup(top, cols, cost).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
    fr = box(body.width + 0.6, body.height + 0.6, S.GREY, fill=S.BG, fill_opacity=0.97, radius=0.14)
    fr.move_to(body)
    tg = your_turn().move_to(fr.get_corner(UP + RIGHT)).shift(LEFT * 1.0)
    card = VGroup(fr, body, tg)
    card.frame, card.tag = fr, tg
    return card


class CallOne(VoiceScene):
    def construct(self):
        assert len(SAY) == 10, len(SAY)

        # ============================================================ 0 · the user turn, then call 1
        p0 = place(src_panel("cli.py", 431, 437, wrap=True), left=PANEL_L, top=TOP_Y)
        p1 = place(src_panel("cli.py", 441, 452), left=PANEL_L, top=TOP_Y)
        q_a = p0.span(435, '"Describe where cheese making is important')
        q_b = VGroup(*p0.span(435, "in"), *p0.span(435, "'s book?\""))
        with self.voiceover(SAY[0]) as vo:
            tr = switch_section(self, None, "Agents", 1, run_time=0.6)
            cs = CallStrip()
            self.play(FadeIn(cs, shift=DOWN * 0.1), run_time=0.4)
            self.play(cs.light(0), run_time=0.4)
            vo.wait_until("the agent function builds")
            self.play(FadeIn(p0, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("the question")
            self.play(q_a.animate.set_color(LOOKUP), q_b.animate.set_color(LOOKUP), run_time=0.6)
            vo.wait_until("with the role user")
            b433 = p0.bar(433, TURN)
            self.play(FadeIn(b433), run_time=0.5)
            vo.wait_until("Then comes the first call")
            self.play(FadeOut(b433), FadeTransform(p0, p1), run_time=0.9)
            self.play(Indicate(p1.span(441, "llm_client.models.generate_content"), color=CLOUD,
                               scale_factor=1.05), run_time=0.8)

        # ============================================================ 1 · three settings
        c1 = p1.code.code_lines
        b445 = p1.bar(445, TURN)
        b446 = p1.bar(446, DATA)
        b447 = VGroup(*[p1.bar(n, TURN) for n in range(447, 452)])
        any_box = ring(p1.span(449, 'mode="any"'), TURN, buff=0.07)
        r445 = c1[p1.rows_of(445)[0]]
        core = concept_box("LLM core: model · parameters · response format", h=0.38)   # fits between rows
        core.next_to(r445, RIGHT, buff=0.45).set_y(r445.get_center()[1])
        menu_n = line_note("the menu").next_to(c1[p1.rows_of(446)[0]], RIGHT, buff=0.35)
        with self.voiceover(SAY[1]) as vo:
            vo.wait_until("temperature zero")
            self.play(FadeIn(b445), run_time=0.5)
            vo.wait_until("the menu as tools")
            self.play(FadeIn(b446), FadeIn(menu_n, shift=LEFT * 0.15), run_time=0.6)
            vo.wait_until("and a tool config")
            self.play(FadeIn(b447), run_time=0.5)
            self.play(Create(any_box), run_time=0.5)
            vo.wait_until("The lecture lists")
            ref = lref("35")
            self.play(FadeIn(ref), FadeIn(core, shift=LEFT * 0.15), run_time=0.7)
            vo.wait_until("Zero keeps")
            self.play(Indicate(p1.span(445, "temperature=0"), color=TURN, scale_factor=1.15),
                      run_time=0.8)

        # ============================================================ 2 · mode="any" becomes ANY
        chip = excerpt_chip('mode="any"', "cli.py · line 449 (excerpt)", frame=TURN, line=L449)
        place(chip, cx=0, top=TOP_Y - 0.1)
        t2 = term(rows=6, container=True)
        with self.voiceover(SAY[2]) as vo:
            src = VGroup(p1.span(449, 'mode="any"').copy(), any_box)
            self.remove(any_box)
            self.play(FadeOut(VGroup(p1, b445, b446, b447, menu_n, core)), FadeOut(ref),
                      FadeTransform(src, chip), caption_extra(tr, True), run_time=0.9)
            self.play(FadeIn(t2, shift=UP * 0.3), run_time=0.5)
            cmd2 = type_cmd(self, t2, C32.cmd, 1.6)
            pin(self, cmd2, beside(extra_tag(), t2, cmd2), run_time=0.3)
            out2 = t2.print(self, C32.at(2, 3, 4), run_time=0.5)
            vo.wait_until("the enum value ANY")
            anys = VGroup(*substring(out2[1], "ANY", 0), *substring(out2[1], "ANY", 1))
            self.play(anys.animate.set_color(TURN), run_time=0.4)
            self.play(Indicate(anys, color=TURN, scale_factor=1.2), run_time=0.6)
            vo.wait_until("The model must answer")
            x_any = substring(out2[1], "ANY", 0).get_center()[0]
            arr = Arrow([x_any, chip.get_bottom()[1] - 0.05, 0], [x_any, t2.box.get_top()[1] + 0.08, 0],
                        buff=0, color=S.GREY, stroke_width=3, max_tip_length_to_length_ratio=0.2,
                        tip_length=0.18)
            cap2 = label("the model must answer with a function call", 22, INK)
            cap2.next_to(arr, LEFT, buff=0.3)
            self.play(GrowArrow(arr), FadeIn(cap2, shift=LEFT * 0.15), run_time=0.7)

        # ============================================================ 3 · which search, never whether
        mc = MenuColumn(show=("llm_top", "llm_bot", "menu0", "menu1", "box2"))
        dec = mc.parts[f"box{MenuColumn.DECISION}"]
        dec.move_to(mc._dec_target.get_center())          # where S04 left it, under the two cards
        mc.shift(RIGHT * (-6.4 - mc.parts["menu0"].get_left()[0]))
        sr = self_rag()
        place(sr, right=6.45, top=1.95)
        ctag = concept_tag().next_to(sr, DOWN, buff=0.18).align_to(sr, RIGHT)
        cross = mc.cross_decision()
        cap3 = label("chooses which search · never whether", 22, INK)
        cap3.move_to([dec.get_center()[0], dec.get_bottom()[1] - 0.45, 0])
        ex = VGroup(label("exercise: delete", 20, INK), mono("tool_config", 20, INK),
                    label(", then greet it", 20, INK)).arrange(RIGHT, buff=0.1)
        ex[2].shift(LEFT * 0.06)
        ex_fr = box(ex.width + 0.4, ex.height + 0.26, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.1)
        ex_fr.move_to(ex)
        exc = VGroup(ex_fr, ex)
        place(exc, right=6.45, bottom=-3.45)
        with self.voiceover(SAY[3]) as vo:
            ref = lref("10–13")
            self.play(FadeOut(VGroup(t2, chip, arr, cap2)), caption_extra(tr, False), FadeIn(ref),
                      FadeIn(mc), run_time=0.8)
            self.play(FadeIn(sr, shift=LEFT * 0.2), FadeIn(ctag), run_time=0.7)
            self.play(Indicate(sr.no_branch, color=TURN, scale_factor=1.05), run_time=0.8)
            vo.wait_until("Self-RAG starts")
            self.play(Indicate(sr.diamond, color=TURN, scale_factor=1.1), run_time=0.7)
            self.play(Indicate(dec, color=TURN, scale_factor=1.08), run_time=0.6)
            vo.wait_until("Ours can't")
            self.play(Create(cross), run_time=0.6)
            vo.wait_until("It chooses which search")
            hop = ring(mc.parts["menu0"], TURN, buff=0.06)
            self.play(Create(hop), run_time=0.4)
            self.play(hop.animate.move_to(mc.parts["menu1"]), FadeIn(cap3, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("never whether")
            self.play(Indicate(cross, color=ERR, scale_factor=1.05), FadeIn(exc, shift=UP * 0.15),
                      run_time=0.7)

        # ============================================================ 4 · the envelope opens on the real request
        env = Envelope(width=3.0, slots=2)
        env.move_to([0, 0.1, 0])
        env_l = label("call 1", 22, S.GREY).next_to(env.parts["body"], DOWN, buff=0.25)
        xc = extra_card("runs agent() unchanged · prints the request instead of sending it")
        place(xc, right=BAND_R, top=BAND_TOP)
        t4 = term(rows=12, container=True)
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(mc, sr, ctag, cross, cap3, exc, hop)), FadeOut(ref), run_time=0.6)
            self.play(FadeIn(env, scale=0.8), FadeIn(env_l), run_time=0.6)
            vo.wait_until("An extra script")
            self.play(FadeIn(xc, shift=DOWN * 0.15), caption_extra(tr, True), run_time=0.6)
            vo.wait_until("but prints the request")
            self.play(*env.open(), run_time=0.4)
            self.play(FadeTransform(VGroup(env, env_l), t4), run_time=0.8)
            r20 = t4.print(self, [REQ_20], wrap=True, run_time=0.4)
            rest = t4.print(self, REQ[1:] + [(REQ_95, S.GREY)], wrap=True, run_time=0.8, lag=0.08)
            wrapped_span(rows_of_line(rest, REQ[1:], 2), REQ[3], "9 names").set_color(S.GREY)
            blue = VGroup(*wrapped_span(list(r20), REQ_20, "locations/global"),
                          *wrapped_span(list(r20), REQ_20, "gemini-3.1-flash-lite"))
            self.play(blue.animate.set_color(CLOUD), run_time=0.5)
            row95 = rest[-1]
            pin(self, row95, beside(notsent_tag(), t4, row95, buff=0.4), run_time=0.4)
            vo.wait_until("the question")
            r_q = rows_of_line(rest, REQ[1:], 0)
            q = VGroup(*wrapped_span(r_q, REQ[1], "Describe where cheese making"),
                       *wrapped_span(r_q, REQ[1], "book?"))
            self.play(q.animate.set_color(LOOKUP), run_time=0.4)
            vo.wait_until("both declarations")
            r_t = rows_of_line(rest, REQ[1:], 1)
            r_s = rows_of_line(rest, REQ[1:], 3)
            decl = VGroup(*wrapped_span(r_t, REQ[2], "get_book_by_author"),
                          *wrapped_span(r_s, REQ[4], "get_book_by_search_content"))
            self.play(decl.animate.set_color(DATA), run_time=0.4)
            vo.wait_until("with the enum")
            r_e = rows_of_line(rest, REQ[1:], 2)
            enum = wrapped_span(r_e, REQ[3], '"enum"')
            self.play(enum.animate.set_color(DATA), run_time=0.3)
            self.play(Indicate(enum, color=DATA, scale_factor=1.15), run_time=0.5)
            vo.wait_until("mode ANY")
            r_m = rows_of_line(rest, REQ[1:], 4)
            mode = wrapped_span(r_m, REQ[5], '"mode": "ANY"')
            self.play(mode.animate.set_color(TURN), run_time=0.4)
            vo.wait_until("temperature zero")
            r_g = rows_of_line(rest, REQ[1:], 5)
            temp = wrapped_span(r_g, REQ[6], '"temperature": 0.0')
            self.play(temp.animate.set_color(TURN), run_time=0.4)

        # ============================================================ 5 · no system instruction
        gc = ghost_card()
        place(gc, right=BAND_R, cy=(xc.get_top()[1] + xc.get_bottom()[1]) / 2 - 0.05)
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(xc, shift=UP * 0.15), FadeIn(gc, shift=LEFT * 1.2), run_time=0.8)
            vo.wait_until("as in lecture 5")
            self.play(Indicate(gc.err, color=S.GREY, scale_factor=1.08), run_time=0.7)
            vo.wait_until("never sends it")
            self.play(Indicate(gc[0], color=S.GREY, scale_factor=1.03), run_time=0.7)

        # ============================================================ 6 · step 1 again, without a key
        lf = look_for_card()
        place(lf, right=BAND_R, top=BAND_TOP)
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(gc), caption_extra(tr, False), run_time=0.5)
            t4.clear(self, run_time=0.4)
            type_cmd(self, t4, AGENT_CMD, 1.2)
            vo.wait_until("The lookup passes")
            items_a = C30.at(2, 3, 8, 9, 10)
            out_a = t4.print(self, items_a, wrap=True, run_time=0.7)
            r3 = rows_of_line(out_a, items_a, 1)[0]
            r10 = rows_of_line(out_a, items_a, 4)[0]
            pin(self, r3, beside(nokey_tag(), t4, r3, buff=0.5), run_time=0.4)
            pin(self, r10, beside(tag("the lookup passed", DATA), t4, r10, buff=0.4), run_time=0.4)
            vo.wait_until("but the first model call")
            items_b = C30.at(16, 17, "…") + [(C30.line(71), ERR)]
            out_b = t4.print(self, items_b, wrap=True, run_time=0.7)
            vo.wait_until("default credentials error")
            r71 = rows_of_line(out_b, items_b, 3)
            err71 = VGroup(*wrapped_span(r71, C30.line(71), "DefaultCredentialsError"),
                           *wrapped_span(r71, C30.line(71), "was not found."))
            self.play(Indicate(err71, color=ERR, scale_factor=1.1), run_time=0.8)
            self.play(FadeIn(lf, shift=DOWN * 0.15), run_time=0.6)

        # ============================================================ 7 · what the staff saw
        st = TrustStage(compact=True)
        st.shift(UP * (2.8 - st.get_top()[1]))
        cs_to = cs.copy()
        place(cs_to, left=tr.get_right()[0] + 0.3, cy=tr.get_center()[1] - 0.02)
        lp = log_panel(RESP, "out.txt · lines 14–28 (excerpt)", width=12.9)
        place(lp, cx=0, bottom=-3.55)
        stf = staff_run_tag().next_to(lp.header, RIGHT, buff=0.35)
        rows = lp.rows
        cc = call_card()
        place(cc, right=lp.frame.get_right()[0] - 0.2, top=rows[5].get_top()[1] + 0.02)
        assert cc.get_left()[0] > rows[9].get_right()[0] + 0.2
        sig = VGroup(label("thought", 20, CLOUD), label("signature", 20, CLOUD))
        sig.arrange(DOWN, aligned_edge=RIGHT, buff=0.06)
        place(sig, right=cc.frame.get_right()[0] - 0.05, bottom=cc.seal.get_top()[1] + 0.06)
        assert sig.get_left()[0] > rows[4].get_right()[0] + 0.2
        md = st.parts["model"]
        bub = speech_bubble()
        bub.move_to(md.frame.get_right() + RIGHT * (0.12 + bub.width / 2) + UP * 0.12)
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(lf), t4.lines.animate.set_opacity(0), run_time=0.4)
            for ln in list(t4.lines):
                t4.lines.remove(ln)
                self.remove(ln)
            self.play(FadeOut(t4), cs.animate.move_to(cs_to), run_time=0.6)
            self.play(FadeIn(st, shift=DOWN * 0.2), run_time=0.6)
            self.play(FadeIn(lp, shift=UP * 0.2), FadeIn(stf), run_time=0.6)
            vo.wait_until("The model's whole answer")
            self.play(FadeIn(bub, scale=0.4), run_time=0.4)
            self.play(FadeTransform(bub, cc), Indicate(rows[1], color=CLOUD, scale_factor=1.04),
                      run_time=0.9)
            self.play(FadeIn(sig, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("get book by author")
            u_name = under(substring(rows[7], "name='get_book_by_author'"), CLOUD, 4)
            self.play(Create(u_name), run_time=0.5)
            vo.wait_until("with the instructor")
            u_auth = under(substring(rows[3], "'author': '‹instructor›'"), CLOUD, 4)
            self.play(Create(u_auth), run_time=0.5)
            vo.wait_until("and the search text")
            srch = substring(rows[4], "'cheese making importance location'")
            self.play(srch.animate.set_color(LOOKUP), run_time=0.5)

        # ============================================================ 8 · four words, an id, a seal
        t_four = tag("4 words", S.GREY)
        t_four.move_to([srch.get_left()[0] + 0.15 + t_four.width / 2, rows[5].get_center()[1], 0])
        assert t_four.get_right()[0] < cc.get_left()[0] - 0.2
        asked = note("the description asked for", size=20)
        ex33 = excerpt_chip("a sentence or two", "agent_tools.py · line 33 (excerpt)", line=L33)
        grp33 = VGroup(asked, ex33).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        place(grp33, right=lp.frame.get_right()[0] - 0.2, top=lp.frame.get_top()[1] - 0.1)
        assert grp33.get_left()[0] > max(rows[1].get_right()[0], t_four.get_right()[0]) + 0.2
        with self.voiceover(SAY[8]) as vo:
            self.play(Indicate(srch, color=LOOKUP, scale_factor=1.08), FadeIn(t_four, shift=LEFT * 0.1),
                      run_time=0.7)
            vo.wait_until("though the description")
            self.play(FadeIn(grp33, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("There's also an ID")
            self.play(Indicate(rows[6], color=TURN, scale_factor=1.06), run_time=0.8)
            vo.wait_until("and a thought signature")
            self.play(Indicate(cc.seal, color=CLOUD, scale_factor=1.6), Indicate(sig, color=CLOUD),
                      Indicate(rows[9], color=CLOUD, scale_factor=1.04), run_time=0.9)

        # ============================================================ 9 · nothing has run yet; your turn
        lp52 = log_panel([L52], "out.txt · line 51")
        place(lp52, cx=0, bottom=-3.55)
        stf52 = staff_run_tag().next_to(lp52.header, RIGHT, buff=0.35)
        bx = st._bx.get_center()[0]
        cc_to = cc.copy()
        cc_to.move_to([bx, -0.3, 0])
        gate = DashedLine([bx, st._bottom.get_center()[1], 0], [bx, cc_to.get_bottom()[1] + 0.05, 0],
                          color=S.GREY, stroke_width=3, dash_length=0.12)
        gate.set_z_index(-1)
        cap9 = label("Gemini wrote arguments · nothing has run yet", 22, INK)
        cap9.next_to(cc_to, DOWN, buff=0.3).set_x(bx)
        tick = cost_tick().next_to(cs_to, RIGHT, buff=0.3)
        paid = label("1 paid call", 20, COST).next_to(tick, RIGHT, buff=0.12)
        card = turn_card_two_cols()
        place(card, cx=0, top=2.75)
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(VGroup(t_four, grp33, u_name, u_auth, sig, stf, lp)), FadeIn(lp52),
                      FadeIn(stf52), run_time=0.8)
            afc = substring(lp52.rows[0], "automatic_function_calling_history=[]")
            u52 = under(afc, S.GREY, 4)
            sdk = grey_tag("the SDK ran nothing").next_to(lp52.rows[0], RIGHT, buff=0.4)
            self.play(Create(u52), FadeIn(sdk, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("it only has declarations")
            self.play(Create(gate), cc.animate.move_to(cc_to), run_time=0.9)
            self.play(FadeIn(cap9, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("So far, one paid call")
            self.play(FadeIn(tick, scale=1.5), FadeIn(paid, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("Pause here")
            self.play(FadeOut(VGroup(st, cc, gate, cap9, lp52, stf52, u52, sdk)),
                      FadeIn(card, shift=UP * 0.15), run_time=0.8)
        self.wait(2)                                    # ▶ beat: hold the frame
        self.play(FadeOut(VGroup(tr, cs, tick, paid, card)), run_time=0.8)
        self.wait(0.3)
