"""S09 · Cost, endpoint and chat (README "Fine-tune › Cost" and "Fine-tune › Chat"). Lecture: none.
Ends part 1 on an empty frame.

Beats (script.md "## S09", one voiceover block each):
 0  TRACKER FtCost 1. QUOTE(expected/readme-cost-table: 4–11) headed "README.md · lines 269–276",
    tag `expected`, GOLD outline (the prose line serif, the Markdown table rows mono so its columns
    stay aligned: the cells' padding is narrowed, whitespace only, and line 7's |---| row is drawn
    as a rule); "$0.008" lights as the price is said, "$112.73" and "16,444" GOLD, the line
    "*** Way too much data for this fine tuning!" lights, then "$0.573" and "88" GOLD.
 1  An `erratum` tag on the table: "Gemini 1.5 Flash · 3 epochs" lights in the table, against the
    code's excerpt chips gemini-finetuner/cli.py line 15 (gemini-3.1-flash-lite) and line 53
    (epoch_count=1). The table greys; a GOLD chip "check the pricing page the README links ·
    README.md:278" and a small GOLD chip "generating the data: cents".
 2  TRACKER FtChat 1 (extra). CODE(gemini-finetuner/cli.py: 102–107); line 107 YELLOW with the
    `erratum` tag "the instructor's endpoint"; a schematic console page (illustration) below holds
    the YELLOW template chip projects/<your-number>/locations/us/endpoints/<id>, which slides over
    line 107. Then the second window (109–110, 113–117 folded): line 114 `model=MODEL_ENDPOINT`
    lights, the RED note "the instructor's endpoint: your key can't reach it".
 3  TRACKER FtChat 2. Full TEAL terminal at app@2a2550dec953:/app$ (tags no key · billed):
    `python cli.py --chat` + ▶ your turn -> gemini-finetuner/03 lines 2–5, …, 66 (wrapped): the
    query (persona masked) lights, line 5 "Using serving location: us" PINK, line 66 RED. The
    terminal shrinks to a strip; V2 above it: the route toward the `us` pin (GREY dashed) stops at
    the wall, RED "no key". 2 s hold.
 4  V2 leaves. QUOTE(expected/readme-chat-example: 10, 12, 14 cut after "heart of cheesemaking!")
    headed "README.md · lines 296–300" (the script's 295–301 counts the ``` fences), tag `expected`;
    the opener "Yello" lights BLUE, the persona chip GREY; a GREY `erratum` chip "the README's query
    is older than the code's" with the code's query (cli.py line 109) as an excerpt chip; GREY tag
    "your answer will differ". The --chat strip stays below.
 5  The strip leaves. TRACKER FtChat 3: the GREY hosted-demo chip (README.md:303–306, optional) and
    its GREY dashed note "its vector-database line belongs to the RAG app (L10)". TRACKER FtChat 4:
    a schematic training monitor (illustration, README.md:308–316): two falling GREY loss curves,
    training and validation, on unlabeled axes, and a GREY "data distribution" histogram.
 6  V2 whole: laptop, both containers, cloud with its four pins; the four routes light in order
    (generate, upload, then train with the bucket -> job arrow, then chat). A GREY curtain slides
    over the cloud: a crossed-out eye, "you never saw a weight". A GREEN adapter glyph (B and A)
    glints in the dark, caption "part 2". Everything fades to an empty frame (end of part 1).
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    ArcBetweenPoints,
    Circle,
    Create,
    DashedVMobject,
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
    LaggedStart,
    Line,
    Rectangle,
    RoundedRectangle,
    ShowPassingFlash,
    Transform,
    VGroup,
    VMobject,
)

from common import *  # noqa: F401,F403
from common import _header_text, _md_text, _mixed_row, _with_header, _wrap_words
from explainer import style as S
from explainer.scene import VoiceScene

SAY = NARRATION["S09"]

# ------------------------------------------------------------------ the real captures and sources
GF = "gemini-finetuner/cli.py"
COST_TABLE = capture("expected/readme-cost-table")
assert COST_TABLE.line(4).startswith("Gemini 1.5 Flash Tuning is 0.008 USD"), COST_TABLE.line(4)
assert "$112.73" in COST_TABLE.line(8) and "16,444" in COST_TABLE.line(8), COST_TABLE.line(8)
assert "$0.573" in COST_TABLE.line(9) and "88" in COST_TABLE.line(9), COST_TABLE.line(9)
assert COST_TABLE.line(11) == "*** Way too much data for this fine tuning!", COST_TABLE.line(11)
CHAT_EX = capture("expected/readme-chat-example")
assert CHAT_EX.line(10) == "How is cheese made?" and CHAT_EX.line(12).startswith("Fine-tuned LLM Response")
assert CHAT_EX.line(14).startswith("Yello - this is"), CHAT_EX.line(14)
CHAT = capture("gemini-finetuner/03")
assert CHAT.cmd == "python cli.py --chat" and CHAT.exit == 1, CHAT.cmd
assert CHAT.line(5) == "Using serving location: us" and "was not found." in CHAT.line(66), CHAT.line(66)
L15, L53, L109 = (source_line(GF, n) for n in (15, 53, 109))
assert 'GENERATIVE_SOURCE_MODEL = "gemini-3.1-flash-lite"' in L15 and "epoch_count=1" in L53, (L15, L53)
assert "How is cheese made in Greece?" in L109, L109
QUERY_109 = unname(L109.split('"')[1])        # the code's query, persona masked
assert "MODEL_ENDPOINT" in source_line(GF, 107) and "model=MODEL_ENDPOINT" in source_line(GF, 114)
README_278 = source_line("README.md", 278)
assert "pricing page" in README_278, README_278
assert "finetunechat" in source_line("README.md", 303) and "Chrome" in source_line("README.md", 306)
assert "Training Monitor" in source_line("README.md", 310) and "Data distribution" in source_line("README.md", 314)
DEMO_URL = "ac215-llm-rag.dlops.io/finetunechat"
assert DEMO_URL in source_line("README.md", 303)
CONSOLE_URL = "console.cloud.google.com/agent-platform/tuning/managed"
TEMPLATE = "projects/<your-number>/locations/us/endpoints/<id>"

# ------------------------------------------------------------------ layout
TOP_Y = 2.86                     # top of a panel under the tracker
SAFE_R = 6.45


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


def flash(mob, color: str = TURN, k: float = 1.15):
    return Indicate(mob, color=color, scale_factor=k)


def cost_card() -> VGroup:
    """QUOTE(expected/readme-cost-table: 4–11) as the house quote card (GREY card, header, `expected`
    tag), the GOLD outline the script asks for. Line 4 is prose (serif, wrapped); lines 6–9 are the
    README's Markdown table, kept mono so its columns stay aligned (each column padded to its widest
    cell: whitespace only, so the 13-wide frame fits; line 7's |---| row drawn as a rule); line 11 serif.
    .frame .rows .prose .table (dict file line -> mono_line) .footer .header .tag"""
    prose = VGroup(*[_md_text(r) for r in _wrap_words(COST_TABLE.line(4), 70)]).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=0.12)
    cells = {n: [c.strip() for c in COST_TABLE.line(n).strip().strip("|").split("|")] for n in (6, 8, 9)}
    widths = [max(len(cells[n][k]) for n in cells) for k in range(len(cells[6]))]
    table = {n: mono_line("".join("| " + c.ljust(w) for c, w in zip(cells[n], widths)) + "|", CAPTION, INK)
             for n in (6, 8, 9)}
    sep = Line(LEFT, RIGHT, color=S.GREY_DARK, stroke_width=2).set_width(table[6].width)
    tbl = VGroup(table[6], sep, table[8], table[9]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    table[7] = sep
    footer = _md_text(COST_TABLE.line(11))
    rows = VGroup(prose, tbl, footer).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
    fr = box(rows.width + 0.5, rows.height + 0.4, COST, fill=S.BG, fill_opacity=0.92, radius=0.12, stroke=3)
    rows.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.25)
    head = _header_text("README.md · lines 269–276").next_to(fr, UP, buff=0.08).align_to(fr, LEFT).shift(RIGHT * 0.1)
    tg = expected_tag().next_to(head, RIGHT, buff=0.25)
    g = VGroup(fr, rows, head, tg)
    g.frame, g.rows, g.prose, g.table, g.footer, g.header, g.tag = fr, rows, prose, table, footer, head, tg
    return g


def text_span(t, sub: str) -> VGroup:
    """The glyphs of `sub` inside a serif/mono Text (spaces have no glyphs)."""
    s = "".join(t.text.split())          # Text.text holds the glyph string (no spaces)
    k = "".join(sub.split())
    a = s.find(k)
    if a < 0:
        raise ValueError(f"{sub!r} not in {s!r}")
    return VGroup(*t.submobjects[a:a + len(k)])


def console_card(width: float = 11.8) -> VGroup:
    """A small schematic console page (illustration, README.md:261's address): "endpoint:" and the
    YELLOW template chip of your own endpoint path. .window .chip .tag"""
    w = browser_window(CONSOLE_URL, width=width, height=1.55)
    lab = label("endpoint:", CAPTION, S.GREY)
    c = chip(TEMPLATE, TURN, size=CAPTION, font=MONO, fill_opacity=0.0)
    c.box.set_fill(S.BG, 1)
    row = VGroup(lab, c).arrange(RIGHT, buff=0.25)
    row.move_to(w.content).align_to(w.content, LEFT).shift(RIGHT * 0.25)
    tg = illustration_tag()
    tg.next_to(w.frame, UP, buff=0.08).align_to(w.frame, RIGHT)
    g = VGroup(w, lab, c, tg)
    g.window, g.chip, g.tag, g.lab = w, c, tg, lab
    return g


def ghost_route(stg, cmd: str) -> VMobject:
    """The route `cmd` would take with a key: a GREY dashed path (the PINK stub stops at the wall)."""
    a = stg.route(cmd)
    return DashedVMobject(a, num_dashes=24, dashed_ratio=0.5).set_stroke(S.GREY, 2.5, opacity=0.7)


def chat_quote() -> VGroup:
    """QUOTE(expected/readme-chat-example: 10, 12, 14 cut after "heart of cheesemaking!"): the README's
    example of a working endpoint (README.md lines 296, 298, 300). .frame .rows .header .tag"""
    rows_txt = [CHAT_EX.line(10), CHAT_EX.line(12).rstrip(), CHAT_EX.cut(14, "heart of cheesemaking!")]
    rows = VGroup()
    for r in rows_txt:
        for piece in _wrap_words(r, 72):
            rows.add(_md_text(piece))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    fr = box(rows.width + 0.5, rows.height + 0.4, S.GREY, fill=S.BG, fill_opacity=0.92, radius=0.12)
    rows.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.25)
    head = _header_text("README.md · lines 296–300").next_to(fr, UP, buff=0.08).align_to(fr, LEFT).shift(RIGHT * 0.1)
    tg = expected_tag().next_to(head, RIGHT, buff=0.25)
    g = VGroup(fr, rows, head, tg)
    g.frame, g.rows, g.header, g.tag = fr, rows, head, tg
    return g


def demo_chip() -> VGroup:
    """The GREY hosted-demo chip (README.md:303–306) and its GREY dashed note. .chip .note"""
    row = VGroup(_mixed_row(["hosted demo ·", f"`{DEMO_URL}`", "· optional"]),
                 label("use Chrome · README.md:303–306", CAPTION, S.GREY)).arrange(DOWN, buff=0.12)
    fr = box(row.width + 0.6, row.height + 0.4, S.GREY, fill_opacity=0.1, radius=0.2)
    row.move_to(fr)
    c = VGroup(fr, row)
    n = concept_box("its vector-database line belongs to the RAG app (L10)")
    n.next_to(c, DOWN, buff=0.2)
    g = VGroup(c, n)
    g.chip, g.note = c, n
    return g


def training_monitor() -> VGroup:
    """A schematic of the console's training monitor (illustration; README.md:308–316, never its
    images): two falling GREY loss curves on unlabeled axes, and a GREY data-distribution histogram.
    .loss .train .val .dist .bars .tag .header"""
    w, h = 4.6, 2.4

    def axes():
        return VGroup(Line([0, 0, 0], [w, 0, 0], color=S.GREY_DARK, stroke_width=2.5),
                      Line([0, 0, 0], [0, h, 0], color=S.GREY_DARK, stroke_width=2.5))

    ax = axes()
    xs = np.linspace(0.15, w - 0.15, 40)
    tr_pts = [np.array([x, 0.35 + 1.75 * np.exp(-x / 1.2) + 0.05 * np.sin(5 * x), 0]) for x in xs]
    va_pts = [np.array([x, 0.6 + 1.55 * np.exp(-x / 1.4), 0]) for x in xs]
    trc = VMobject().set_points_smoothly(tr_pts).set_stroke(S.GREY, 3.5)
    vac = DashedVMobject(VMobject().set_points_smoothly(va_pts), num_dashes=30).set_stroke(S.GREY, 3)
    lt = label("training", CAPTION, S.GREY).next_to(tr_pts[-1], DOWN, buff=0.12).align_to(ax, RIGHT)
    lv = label("validation", CAPTION, S.GREY).next_to(va_pts[-1], UP, buff=0.12).align_to(ax, RIGHT)
    cap1 = label("training monitor", CAPTION, S.GREY).next_to(ax, DOWN, buff=0.15)
    loss = VGroup(ax, trc, vac, lt, lv, cap1)
    ax2 = axes()
    heights = [0.45, 0.9, 1.5, 1.95, 1.7, 1.2, 0.75, 0.4]
    bw = w / (len(heights) + 1)
    bars = VGroup(*[Rectangle(width=bw * 0.8, height=hh, stroke_color=S.GREY, stroke_width=2)
                    .set_fill(S.GREY, 0.3).move_to([bw * (k + 1), hh / 2, 0]) for k, hh in enumerate(heights)])
    cap2 = label("data distribution", CAPTION, S.GREY).next_to(ax2, DOWN, buff=0.15)
    dist = VGroup(ax2, bars, cap2)
    dist.next_to(loss, RIGHT, buff=1.2).align_to(loss, DOWN)
    body = VGroup(loss, dist)
    fr = box(body.width + 0.8, body.height + 0.7, S.GREY_DARK, fill=PANEL, fill_opacity=1, radius=0.14)
    body.move_to(fr)
    head = _header_text("README.md · lines 308–316 · Agent Platform › Tuning")
    head.next_to(fr, UP, buff=0.08).align_to(fr, LEFT).shift(RIGHT * 0.1)
    tg = illustration_tag().next_to(fr, UP, buff=0.08).align_to(fr, RIGHT)
    g = VGroup(fr, body, head, tg)
    g.frame, g.loss, g.train, g.val, g.dist, g.bars, g.tag, g.header = fr, loss, trc, vac, dist, bars, tg, head
    g.axes1, g.labels1 = VGroup(ax, cap1), VGroup(lt, lv)
    return g


def crossed_eye(w: float = 1.0) -> VGroup:
    """An eye with a slash through it (you never saw a weight)."""
    l, r = np.array([-w / 2, 0, 0]), np.array([w / 2, 0, 0])
    top = ArcBetweenPoints(l, r, angle=-1.6).set_stroke(INK, 3.5)
    bot = ArcBetweenPoints(l, r, angle=1.6).set_stroke(INK, 3.5)
    pupil = Circle(radius=w * 0.14, color=INK, stroke_width=3.5).set_fill(INK, 0.8)
    slash = Line([-w * 0.5, -w * 0.42, 0], [w * 0.5, w * 0.42, 0], color=INK, stroke_width=5)
    return VGroup(top, bot, pupil, slash)


def adapter_glyph() -> VGroup:
    """The GREEN LoRA adapters: a tall thin B and a flat thin A (part 2's 4.6 MB you own)."""
    b = Rectangle(width=0.2, height=1.0, stroke_color=ADAPTER, stroke_width=3).set_fill(ADAPTER, 0.45)
    a = Rectangle(width=1.0, height=0.2, stroke_color=ADAPTER, stroke_width=3).set_fill(ADAPTER, 0.45)
    lb = label("B", CAPTION, ADAPTER).next_to(b, LEFT, buff=0.1)
    la = label("A", CAPTION, ADAPTER).next_to(a, UP, buff=0.1)
    a.next_to(b, RIGHT, buff=0.15).align_to(b, UP)
    la.next_to(a, UP, buff=0.1)
    return VGroup(b, a, lb, la)


class CostAndChat(VoiceScene):
    def construct(self):
        assert len(SAY) == 7, len(SAY)

        # ========================================================== 0 · step 1: the README's cost table
        tr = tracker("FtCost", 1)
        card = cost_card()
        place(card, cx=0, cy=0.15)            # centred while alone; it moves up in beat 1
        r8, r9 = card.table[8], card.table[9]
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.25), run_time=0.5)
            self.play(FadeIn(card.frame), FadeIn(card.header), FadeIn(card.tag), run_time=0.5)
            self.play(FadeIn(card.prose, shift=UP * 0.1), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(card.table[n], shift=UP * 0.08) for n in (6, 7, 8, 9)], lag_ratio=0.25),
                      FadeIn(card.footer), run_time=1.0)
            vo.wait_until("At 0.008 dollars")
            p8 = VGroup(substring(r8, "$0.008"), substring(r9, "$0.008"))
            self.play(p8.animate.set_color(COST), text_span(card.prose[0], "0.008 USD per 1,000 tokens")
                      .animate.set_color(COST), run_time=0.6)
            vo.wait_until("16,444 documents")
            self.play(substring(r8, "16,444").animate.set_color(COST), run_time=0.4)
            vo.wait_until("come to 112 dollars")
            c112 = substring(r8, "$112.73")
            self.play(c112.animate.set_color(COST), run_time=0.4)
            self.play(flash(c112, COST, 1.25), run_time=0.6)
            vo.wait_until("the table calls that")
            self.play(card.footer.animate.set_color(TURN), run_time=0.4)
            self.play(flash(card.footer, TURN, 1.06), run_time=0.6)
            vo.wait_until("88 documents")
            self.play(substring(r9, "88").animate.set_color(COST), run_time=0.4)
            c573 = substring(r9, "$0.573")
            self.play(c573.animate.set_color(COST), run_time=0.4)
            self.play(flash(c573, COST, 1.25), run_time=0.6)

        # ========================================================== 1 · erratum: Gemini 1.5 Flash · 3 epochs; check the pricing page
        card_up = TOP_Y - card.get_top()[1]
        card.shift(UP * card_up)                # lay out beat 1 from the card's final place
        err = erratum_tag("Gemini 1.5 Flash · 3 epochs")
        place(err, left=card.frame.get_left()[0] + 0.1, top=card.frame.get_bottom()[1] - 0.1)
        e15 = excerpt_chip('"gemini-3.1-flash-lite"', f"{GF} · line 15 (excerpt)", line=L15)
        e53 = excerpt_chip("epoch_count=1", "line 53 (excerpt)", line=L53)
        code_lab = label("the code:", CAPTION, INK)
        crow = VGroup(code_lab, e15, e53).arrange(RIGHT, buff=0.35, aligned_edge=DOWN)
        code_lab.set_y(e15.chip.get_center()[1])     # level with the chips, not their baseline
        place(crow, left=err.get_left()[0], top=err.get_bottom()[1] - 0.15)
        price = chip("check the pricing page the README links · README.md:278", COST, size=CAPTION)
        gen = chip("generating the data: cents", COST, size=CAPTION)
        grow = VGroup(price, gen).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        place(grow, left=err.get_left()[0], top=crow.get_bottom()[1] - 0.18)
        assert grow.get_bottom()[1] > -3.55 and grow.get_right()[0] < SAFE_R, (grow.get_bottom(), grow.get_right())
        assert crow.get_right()[0] < SAFE_R, crow.get_right()
        ep_cells = VGroup(substring(r8, "| 3 ")[1:], substring(r9, "| 3 ")[1:])   # the 3s, not the bars
        card.shift(DOWN * card_up)
        with self.voiceover(SAY[1]) as vo:
            self.play(card.animate.shift(UP * card_up), run_time=0.7)
            vo.wait_until("the table prices")
            g15 = text_span(card.prose[0], "Gemini 1.5 Flash")
            self.play(g15.animate.set_color(TURN), FadeIn(err, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("for 3 epochs")
            self.play(ep_cells.animate.set_color(TURN), run_time=0.4)
            self.play(flash(ep_cells, TURN, 1.2), run_time=0.5)
            vo.wait_until("while the code tunes")
            self.play(FadeIn(code_lab), FadeIn(e15, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("for 1.")
            self.play(FadeIn(e53, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Treat these numbers")
            dim = [m for m in card.rows.family_members_with_points()]
            self.play(*[m.animate.set_color(S.GREY_DARK) for m in dim],
                      card.frame.animate.set_stroke(S.GREY, 2.5), run_time=0.8)
            vo.wait_until("check the pricing page")
            self.play(FadeIn(price, shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(gen, shift=UP * 0.1), run_time=0.5)

        # ========================================================== 2 · extra edit: line 107 holds the instructor's endpoint
        w1 = src_panel(GF, [(102, 105), 107], size=20,
                       wrap={104: ["after the job"], 105: ["use locations"], 107: ['"projects', "/endpoints"]})
        _with_header(w1, f"{GF} · lines 102–107 (folded) · long lines wrapped")
        place(w1, cx=0, top=TOP_Y)
        w2 = src_panel(GF, [(109, 110), (113, 117)], size=20)
        place(w2, left=w1.get_left()[0], top=TOP_Y)
        assert w1.get_right()[0] < 6.5 and w2.get_right()[0] < 6.5, (w1.get_right(), w2.get_right())
        sp107a = w1.span(107, '"projects/‹instructor-project-number›/locations/us')
        sp107b = w1.span(107, '/endpoints/‹endpoint-id›"')
        sp107 = VGroup(sp107a, sp107b)
        head107 = w1.span(107, "MODEL_ENDPOINT =")
        err2 = erratum_tag("the instructor's endpoint")
        con = console_card()
        place(con, cx=0, bottom=-3.45)
        assert con.get_top()[1] < w1.get_bottom()[1] - 0.05, (con.get_top(), w1.get_bottom())
        # the tag sits just under the panel, below line 107's wrapped rows (no code row is covered),
        # left of the console's 'illustration' tag and above its window
        place(err2, left=head107.get_left()[0], top=w1.get_bottom()[1] - 0.06)
        assert err2.get_top()[1] < w1.get_bottom()[1], (err2.get_top(), w1.get_bottom())
        assert err2.get_bottom()[1] > con.window.get_top()[1] + 0.03, (err2.get_bottom(), con.window.get_top())
        assert err2.get_right()[0] < con.tag.get_left()[0] - 0.2, (err2.get_right(), con.tag.get_left())
        sp114 = w2.span(114, "model=MODEL_ENDPOINT")
        no_reach = chip("the instructor's endpoint · your key can't reach it", ERR, size=CAPTION)
        with self.voiceover(SAY[2]) as vo:
            gone = [card, err, crow, grow]
            self.play(*[FadeOut(m) for m in gone], run_time=0.5)
            tr = switch_section(self, tr, "FtChat", 1)
            self.play(caption_extra(tr), run_time=0.4)
            self.play(FadeIn(w1, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("Line 107 still holds")
            b107 = w1.bar(107, TURN)
            self.play(FadeIn(b107), sp107.animate.set_color(TURN), run_time=0.5)
            vo.wait_until("the instructor's endpoint")
            self.play(FadeIn(err2, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("Copy yours from the console")
            self.play(FadeIn(con.window), FadeIn(con.tag), FadeIn(con.lab), run_time=0.5)
            self.play(FadeIn(con.chip, shift=RIGHT * 0.15), run_time=0.5)
            vo.wait_until("a path ending in locations")
            self.play(flash(con.chip.text, TURN, 1.06), run_time=0.8)
            vo.wait_until("Paste it there")
            target = con.chip.copy()
            target.move_to(sp107).align_to(sp107a, LEFT).shift(LEFT * 0.1)
            over = target.get_right()[0] - (w1.get_right()[0] - 0.08)
            if over > 0:                             # keep the pasted chip inside the code panel
                target.shift(LEFT * over)
            self.play(con.chip.animate.move_to(target), sp107.animate.set_opacity(0), FadeOut(err2), run_time=0.9)
            self.play(flash(con.chip.text, TURN, 1.05), run_time=0.5)   # the text only: a filled flash hides it
            vo.wait_until("otherwise chat points")
            self.play(FadeOut(VGroup(con.window, con.tag, con.lab, con.chip, b107)), run_time=0.4)
            body1 = VGroup(*[m for m in w1.submobjects if m is not w1.header])
            body2 = VGroup(*[m for m in w2.submobjects if m is not w2.header])
            self.play(FadeOut(w1.header, run_time=0.3), Transform(body1, body2, run_time=0.8),
                      FadeIn(w2.header, run_time=0.8, rate_func=lambda x: max(0.0, (x - 0.6) / 0.4)))
            self.remove(body1, w1)
            self.add(w2)
            b114 = w2.bar(114, ERR)
            self.play(FadeIn(b114), sp114.animate.set_color(ERR), run_time=0.5)
            place(no_reach, left=w2.get_left()[0] + 0.1, top=w2.get_bottom()[1] - 0.3)
            vo.wait_until("which your key")
            self.play(FadeIn(no_reach, shift=UP * 0.1), run_time=0.5)

        # ========================================================== 3 · step 2: python cli.py --chat (no key)
        t = term(P_CTR_GF, rows=12, container="gf")
        tags3 = frame_tags(t, nokey_tag(), billed_tag())
        stg = Stage(show=("laptop", "key", "gf", "mounts_gf", "cloud", "pin_global", "pin_bucket", "pin_tune",
                          "pin_us"))
        blk = stg.blocked("--chat")
        ghost = ghost_route(stg, "--chat")
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(w2, b114, no_reach)), run_time=0.5)
            self.play(tr.goto(2), FadeIn(t, shift=UP * 0.2), FadeIn(tags3, shift=UP * 0.2), run_time=0.6)
            bare_prompt(self, t)
            vo.wait_until("python cli.py dash dash chat")
            tc = type_cmd(self, t, CHAT.cmd, 0.5)
            pin(self, tc, beside(your_turn(), t, tc), run_time=0.4)
            vo.wait_until("It prints its question")
            out = show(self, t, CHAT, 2, 3, 4, run_time=0.5)
            q = out[2]
            self.play(substring(q, "How is cheese made in Greece?").animate.set_color(TURN), run_time=0.4)
            vo.wait_until("answered the instructor's way")
            self.play(flash(substring(q, PERSONA), S.GREY, 1.25), run_time=0.6)
            vo.wait_until("Then it prints the serving location")
            r5 = show(self, t, CHAT, 5, run_time=0.4)[0]
            self.play(r5.animate.set_color(LOOKUP), run_time=0.4)
            vo.wait_until("and the same missing key")
            show(self, t, CHAT, "…", run_time=0.3)
            r66 = t.print(self, [(CHAT.line(66), ERR)], wrap=True, run_time=0.4)
            self.play(flash(wrapped_glyphs(r66, "was not found."), ERR, 1.12), run_time=0.6)
            vo.wait_until("Pause and run it")
            resize(self, t, 3, keep=[tc, *r66], run_time=0.6,
                   extra=[tags3.animate.set_y(STRIP_TOP - t.bar_h / 2)])
            self.play(FadeIn(stg), run_time=0.5)
            self.play(Create(ghost), run_time=0.5)
            self.play(Create(blk.stub), FadeIn(blk.stamp, scale=1.3), run_time=0.5)
        self.wait(2)

        # ========================================================== 4 · the README's example of a working endpoint
        cq = chat_quote()
        place(cq, cx=0, top=TOP_Y)
        r_q, r_open = cq.rows[0], cq.rows[2]
        e109 = excerpt_chip(QUERY_109, f"{GF} · line 109 (excerpt)", line=L109)
        erq = erratum_tag("the README's query is older than the code's")
        row4 = VGroup(erq, e109).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        place(row4, left=cq.frame.get_left()[0] + 0.1, top=cq.frame.get_bottom()[1] - 0.2)
        differ = grey_tag("your answer will differ")
        place(differ, right=cq.frame.get_right()[0], cy=cq.header.get_center()[1])
        assert row4.get_bottom()[1] > STRIP_TOP + 0.05, row4.get_bottom()
        assert differ.get_left()[0] > cq.tag.get_right()[0] + 0.2, (differ.get_left(), cq.tag.get_right())
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(stg, ghost, blk)), run_time=0.5)
            self.play(FadeIn(cq, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("to an older question")
            self.play(flash(r_q, TURN, 1.08), run_time=0.6)
            self.play(FadeIn(erq, shift=DOWN * 0.1), FadeIn(e109, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("the same Yello opener")
            yello = text_span(r_open, "Yello")
            self.play(yello.animate.set_color(MODEL), run_time=0.4)
            self.play(flash(yello, MODEL, 1.3), flash(text_span(r_open, PERSONA), S.GREY, 1.15), run_time=0.7)
            vo.wait_until("Your answer will differ")
            self.play(FadeIn(differ, shift=UP * 0.1), run_time=0.5)

        # ========================================================== 5 · steps 3 and 4: hosted demo, training monitor
        demo = demo_chip()
        place(demo, cx=0, top=TOP_Y - 0.05)
        mon = training_monitor()
        place(mon, cx=0, bottom=-3.4)
        assert mon.get_top()[1] < demo.get_bottom()[1] - 0.15, (mon.get_top(), demo.get_bottom())
        assert demo.width < 12.9 and mon.width < 12.9, (demo.width, mon.width)
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(cq, erq, e109, differ, t, tags3)), run_time=0.6)
            self.play(tr.goto(3), FadeIn(demo.chip, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("is optional")
            self.play(FadeIn(demo.note, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("Step 4")
            self.play(tr.goto(4), FadeIn(mon.frame), FadeIn(mon.header), FadeIn(mon.tag), FadeIn(mon.axes1),
                      run_time=0.6)
            vo.wait_until("shows your job's loss curves")
            self.play(Create(mon.train), Create(mon.val), run_time=1.2)
            self.play(FadeIn(mon.labels1), run_time=0.4)
            vo.wait_until("and its data distribution")
            ax2, bars, cap2 = mon.dist
            self.play(FadeIn(ax2), FadeIn(cap2), LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in bars],
                                                           lag_ratio=0.12), run_time=1.0)

        # ========================================================== 6 · track A in one picture; you never saw a weight
        st6 = Stage()
        st6.shift(DOWN * 0.75)                  # no strip, no tracker: centre the stage
        cl = st6.cloud_frame
        routes = {c: st6.route(c) for c in ("--generate", "--upload", "--train", "--chat")}
        jarr = st6.job_arrow()
        curtain = RoundedRectangle(width=cl.width - 0.1, height=cl.height - 0.1, corner_radius=0.26,
                                   stroke_color=S.GREY, stroke_width=2.5)
        curtain.set_fill(S.GREY_DARKER, 1).move_to(cl)
        curtain0 = curtain.copy().stretch(0.02, 1, about_edge=UP)
        eye = crossed_eye(1.1).move_to(cl.get_center() + UP * 1.15)
        never = VGroup(label("you never saw", CAPTION, INK), label("a weight", CAPTION, INK)).arrange(DOWN, buff=0.08)
        never.next_to(eye, DOWN, buff=0.2)
        ad = adapter_glyph().move_to(cl.get_center() + DOWN * 1.0 + LEFT * 0.5)
        assert never.get_bottom()[1] > ad.get_top()[1] + 0.25, (never.get_bottom(), ad.get_top())
        assert ad.get_bottom()[1] > curtain.get_bottom()[1] + 0.2, (ad.get_bottom(), curtain.get_bottom())
        p2 = label("part 2", 26, ADAPTER).next_to(ad, RIGHT, buff=0.35)
        assert p2.get_right()[0] < cl.get_right()[0] - 0.1, (p2.get_right(), cl.get_right())
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(demo, mon)), FadeOut(tr), run_time=0.6)
            self.play(FadeIn(st6), run_time=0.7)
            vo.wait_until("a teacher wrote the data")
            self.play(GrowArrow(routes["--generate"]), run_time=0.6)
            self.play(GrowArrow(routes["--upload"]), run_time=0.6)
            vo.wait_until("Google ran the job")
            self.play(GrowArrow(routes["--train"]), run_time=0.6)
            self.play(Create(jarr), run_time=0.5)
            vo.wait_until("and you have an endpoint")
            self.play(GrowArrow(routes["--chat"]), run_time=0.6)
            self.play(flash(st6.pins["pin_us"], CLOUD, 1.1), run_time=0.5)
            vo.wait_until("And you never saw")
            self.play(Transform(curtain0, curtain), run_time=1.0)
            self.play(FadeIn(eye, scale=0.8), FadeIn(never, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("In part 2")
            self.play(FadeIn(ad, scale=0.6), run_time=0.6)
            self.play(ShowPassingFlash(VGroup(*[m.copy().set_stroke(INK, 5) for m in ad[:2]]), time_width=0.5),
                      FadeIn(p2, shift=LEFT * 0.1), run_time=0.8)
            vo.wait_until("the weights are in your hands")
            self.play(flash(ad, ADAPTER, 1.25), run_time=0.7)
        self.wait(0.6)
        self.play(FadeOut(VGroup(st6, *routes.values(), jarr, curtain0, eye, never, ad, p2)), run_time=0.9)
        self.wait(0.3)
