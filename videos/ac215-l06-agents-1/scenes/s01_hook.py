"""S01 · Who searched your database? (cold open of AC215 L6). Lecture: 20–22.

Beats (script.md "## S01", one voiceover block each):
0. Black frame, no tracker. Top left a GREY question card types in the staff's question
   (expected/out-txt-agent-run.txt line 9, masked); top right the tag "recorded · the staff's run,
   September 22, 2026". Bottom centre the GREY laptop zone holding the TEAL llm-rag-chromadb
   container (a cylinder, PINK localhost:8000); far right the BLUE cloud "Google Cloud" with the
   BLUE chip "Gemini". Between them PANEL(expected/out-txt-agent-run.txt: 65, 68), header
   "out.txt · lines 64, 67 · line 67 wrapped" (76 characters do not fit one row at 20 pt), types
   in line by line as named.
1. A PINK arrow runs from the panel's arguments line down into the cylinder; ten GREEN chunk cards
   rise out of it into two rows, each labelled "one book" (GREY); the masked author in the panel is
   underlined as "filtered by author" is said. A RED dashed line leaves Gemini toward
   localhost:8000 and stops at the cloud's edge, where the GREY chip "localhost = this machine"
   appears. The picture dims; "Who searched your database?" and "Who chose the book?" write in
   YELLOW, centre.
2. LECTURE 20–22, with a GREY caption under the tag "the lecture slides this stands on" (this beat
   only). The picture shrinks away; the two questions shrink into a small YELLOW card top right,
   which stays until the scene ends (call 2 answers it). A GREY request card writes in (our words,
   slide 20): 5 days in Paris · flights and hotels within budget · activities you'd enjoy · replan
   if it rains or a flight is late. Under it "Can an LLM or RAG alone do this?" and two verdicts:
   BLUE "LLM: drafts a plan, can't act as things change", TEAL-outlined "RAG: fetches and
   summarizes".
3. Three GREY dashed chips under the verdicts as named (slide 22): live systems, tools that act,
   autonomy.
4. The lecture tag leaves. Three bands write in top to bottom as named: by hand · llm-rag --agent
   (TEAL container glyph, BLUE "Gemini", "Docker · Gemini on Vertex AI"); with a framework · Google
   ADK (PURPLE uv glyph, BLUE "Gemini", "uv · the Gemini API"); with a harness · two Colab notebooks
   (BLUE notebook with a GREEN check, "OpenAI"). A GREY chip along the left edge spans all three:
   "ideas along the way: the Cheese Quiz notebook"; "part 1" / "part 2" markers at the right edge.
5. Layout preview, each step clearing the last: the tracker top left, its head cycling llm-rag,
   ADK, Colab inside a pulsing YELLOW ring; a GREY lecture_ref(6, "51–53") sample top right; a
   3-row container strip (tag preview) with `python cli.py --agent --chunk_type char-split` and
   ▶ your turn (held 2 s). Then a row of tags writes in above the strip: recorded · expected ·
   illustration · extra · stand-in (PINK, as it appears later) · no key · built, not sent.
6. A "You need" checklist writes in row by row as named (GOLD keys for the three keys).
7. A card "Recorded October 18, 2026 · no Google or OpenAI keys", three rows as named: GREEN check
   real runs; GREY crossed-out key model calls; tag recorded model answers.
8. The GREY ‹instructor› chip with "the instructor's name, hidden on screen"; the footer card
   "every command: MLOps_Learning · guides/L06-agents-1.md". Fade to an empty frame.
"""

import numpy as np
from common import (
    CLOUD,
    CTR,
    DATA,
    ERR,
    INK,
    LOOKUP,
    MASK,
    MONO,
    NARRATION,
    P_CTR,
    QUESTION,
    TOOL,
    TURN,
    beside,
    capture,
    chunk_card,
    concept_box,
    cylinder,
    expected_tag,
    extra_tag,
    grey_tag,
    illustration_tag,
    key_glyph,
    laptop_zone,
    log_panel,
    lref,
    mtext,
    notebook_glyph,
    notsent_tag,
    note,
    pin,
    preview_tag,
    recorded_tag,
    staff_run_tag,
    standin_tag,
    term,
    tracker,
    type_cmd,
    under,
    your_turn,
)
from manim import (
    DOWN,
    LEFT,
    PI,
    RIGHT,
    UP,
    Arrow,
    Circle,
    Create,
    DashedLine,
    FadeIn,
    FadeOut,
    FadeTransform,
    GrowArrow,
    Group,
    Indicate,
    LaggedStart,
    Line,
    Rectangle,
    ReplacementTransform,
    RoundedRectangle,
    VGroup,
    VMobject,
    Write,
    there_and_back,
)

from explainer import style as S
from explainer.devops import (
    box,
    check_mark,
    chip,
    cloud,
    cross_mark,
    glyph_range,
    label,
    mono,
    substring,
)
from explainer.scene import VoiceScene

SAY = NARRATION["S01"]

# ------------------------------------------------------------------ the real sources
OUT = capture("out-txt-agent-run", "expected")        # out.txt; out.txt's own line = file line - 1
assert OUT.line(9) == f'  text="{QUESTION}"', OUT.line(9)
L65 = OUT.line(65)
L68 = OUT.line(68)
assert L65 == "Function: get_book_by_author", L65
ARGS_CUT = f"Calling function with args: {MASK} ,"
assert L68.startswith(ARGS_CUT), L68
ARGS_REST = L68[len(ARGS_CUT):].strip()
assert ARGS_REST == "cheese making importance location", ARGS_REST
PANEL_ROWS = [L65, ARGS_CUT, "  ↪ " + ARGS_REST]            # line 68 wrapped (house ↪ format)
PANEL_HEAD = "out.txt · lines 64, 67 · line 67 wrapped"
Q_ROWS = ["Describe where cheese making is", "important in ‹instructor›'s book?"]
assert " ".join(Q_ROWS) == QUESTION, QUESTION

CMD = "python cli.py --agent --chunk_type char-split"   # script.md S01 / README "Agents"
GUIDE = "MLOps_Learning · guides/L06-agents-1.md"

REQUEST = ["5 days in Paris", "flights and hotels within budget", "activities you'd enjoy",
           "replan if it rains or a flight is late"]
MISSING = ["live systems", "tools that act", "autonomy"]
NEED = [("lecture 5's char-split collection (or the load step)", None),
        ("service-account key · lecture 5", "key"),
        ("Docker", None), ("uv", None), ("Node.js", None),
        ("Google AI Studio key", "key"),
        ("OpenAI key · billing on", "key")]
REC_HEAD = "Recorded October 18, 2026 · no Google or OpenAI keys"
REC_ROWS = [["real runs: Docker, Chroma, uv,", "the ADK web server, two MCP servers"],
            ["model calls: stopped before sending, or refused"],
            ["model answers: the teaching staff's saved outputs"]]

SAFE_X, SAFE_Y = 6.5, 3.5
QCARD_TOP, QCARD_RIGHT = 2.75, 6.5             # the YELLOW questions card, from beat 2 on


# ------------------------------------------------------------------ small helpers
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


def inside_frame(*mobs):
    for m in mobs:
        assert m.get_left()[0] >= -6.6 and m.get_right()[0] <= 6.6, (m.get_left(), m.get_right())
        assert m.get_bottom()[1] >= -3.6 and m.get_top()[1] <= 3.6, (m.get_bottom(), m.get_top())


def apart(a, b, gap: float = 0.05):
    """Assert the bounding boxes of a and b do not overlap."""
    sep = (a.get_right()[0] + gap <= b.get_left()[0] or b.get_right()[0] + gap <= a.get_left()[0]
           or a.get_top()[1] + gap <= b.get_bottom()[1] or b.get_top()[1] + gap <= a.get_bottom()[1])
    assert sep, (a.get_corner(DOWN + LEFT), a.get_corner(UP + RIGHT), b.get_corner(DOWN + LEFT),
                 b.get_corner(UP + RIGHT))


def hidden(*glyph_groups):
    """Set glyphs to opacity 0 (they are typed in later with type_in)."""
    for g in glyph_groups:
        for m in g:
            m.set_opacity(0)


def type_in(glyphs, run_time: float):
    """A typing effect on glyphs that are already on screen at opacity 0 (members of a parent that
    is in the scene): each glyph appears in turn. No new top-level mobjects are created."""
    gl = list(glyphs)
    return LaggedStart(*[g.animate(rate_func=lambda t: 1.0 if t > 0 else 0.0).set_opacity(1)
                         for g in gl], lag_ratio=1.0, run_time=run_time)


def text_glyphs(t) -> list:
    """The glyph mobjects of a Text, or of a mono_line (its .glyphs)."""
    return list(t.glyphs) if hasattr(t, "glyphs") else list(t.submobjects)


def clear_stage(scene, keep=(), anims=(), run_time: float = 0.6):
    """Fade out every top-level mobject but `keep` (with `anims`), then drop them from the scene."""
    old = [m for m in scene.mobjects if m not in keep]
    if old:
        scene.play(FadeOut(Group(*old)), *anims, run_time=run_time)
        scene.remove(*old)
    elif anims:
        scene.play(*anims, run_time=run_time)


def pulse(m, color: str = TURN, k: float = 1.06, run_time: float = 0.7):
    return m.animate(rate_func=there_and_back, run_time=run_time).scale(k).set_stroke(color)


def card_frame(w: float, h: float, color: str = S.GREY, fill_opacity: float = 0.95):
    return box(w, h, color, fill=S.BG, fill_opacity=fill_opacity, radius=0.14)


# ---- beat 0/1 pictures
CLOUD_W = 4.0
CLOUD_U = CLOUD_W / 3.0
CLOUD_AT = np.array([4.7, 1.5, 0])        # where the cloud's own origin goes (see cloud())


def in_cloud(p) -> bool:
    """Is point p inside the cloud outline (explainer.devops.cloud's geometry, origin CLOUD_AT)?"""
    u = CLOUD_U
    x, y = p[0] - CLOUD_AT[0], p[1] - CLOUD_AT[1]
    for cx, cy, r in ((-0.75 * u, -0.1 * u, 0.55 * u), (0.0, 0.2 * u, 0.75 * u), (0.8 * u, -0.1 * u, 0.55 * u)):
        if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
            return True
    hw, hh, r = 1.3 * u, 0.375 * u, 0.37 * u
    dx, dy = abs(x), abs(y + 0.3 * u)
    if dx > hw or dy > hh:
        return False
    if dx <= hw - r or dy <= hh - r:
        return True
    return (dx - (hw - r)) ** 2 + (dy - (hh - r)) ** 2 <= r * r


def container_glyph(color: str = CTR, w: float = 0.95, h: float = 0.6) -> VGroup:
    """A small TEAL shipping container: a box with vertical ridges."""
    fr = RoundedRectangle(width=w, height=h, corner_radius=0.06, stroke_color=color, stroke_width=3) \
        .set_fill(color, 0.14)
    ridges = VGroup(*[Line(UP * h * 0.32, DOWN * h * 0.32, color=color, stroke_width=2)
                      .move_to(fr.get_center() + RIGHT * (k - 2) * w * 0.17) for k in range(5)])
    return VGroup(fr, ridges)


def uv_glyph(color: str = TOOL, s: float = 0.62) -> VGroup:
    """A PURPLE tool glyph for uv: a rounded square with the name in mono."""
    fr = RoundedRectangle(width=s, height=s, corner_radius=0.1, stroke_color=color, stroke_width=3) \
        .set_fill(color, 0.16)
    t = mono("uv", 24, color).move_to(fr)
    return VGroup(fr, t)


def v_bracket(top: float, bottom: float, x: float, color=S.GREY, tick: float = 0.12, opens=LEFT) -> VMobject:
    d = -tick if opens is LEFT else tick
    return VMobject().set_points_as_corners(
        [[x + d, top, 0], [x, top, 0], [x, bottom, 0], [x + d, bottom, 0]]).set_stroke(color, 2.5)


# ------------------------------------------------------------------ the scene
class Hook(VoiceScene):
    def construct(self):
        assert len(SAY) == 9, len(SAY)

        # ========================================================== 0. the question, the picture
        q_rows = VGroup(*[mtext(s, 20, INK) for s in Q_ROWS]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        q_fr = card_frame(q_rows.width + 0.5, q_rows.height + 0.36)
        q_rows.move_to(q_fr).align_to(q_fr, LEFT).shift(RIGHT * 0.25)
        qcard = VGroup(q_fr, q_rows)
        place(qcard, left=-SAFE_X + 0.05, top=SAFE_Y - 0.05)
        q_glyphs = [g for r in q_rows for g in text_glyphs(r)]
        hidden(q_glyphs)
        staff = staff_run_tag()
        place(staff, right=SAFE_X, cy=qcard.get_top()[1] - staff.height / 2)
        apart(qcard, staff, 0.3)

        # the panel: out.txt lines 64 and 67 (file lines 65, 68), line 68 wrapped
        panel = log_panel(PANEL_ROWS, PANEL_HEAD, width=7.6)
        place(panel, left=-SAFE_X + 0.05, top=qcard.get_bottom()[1] - 0.28)
        arrow_row = panel.rows[2]
        glyph_range(arrow_row, 2, 3).set_color(S.GREY)                 # the ↪ mark
        row_glyphs = [text_glyphs(r) for r in panel.rows]
        hidden(*row_glyphs)

        # bottom centre: the laptop with the Chroma container
        cyl = cylinder(0.8, 0.72)
        names = VGroup(mono("llm-rag-chromadb", 22, CTR), mono("localhost:8000", 22, LOOKUP)) \
            .arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        inner = VGroup(cyl, names).arrange(RIGHT, buff=0.35)
        ctr = box(inner.width + 0.7, inner.height + 0.5, CTR, fill=S.BG, fill_opacity=1.0, stroke=3)
        ctr_tint = box(ctr.width, ctr.height, CTR, fill_opacity=0.06, stroke=0).move_to(ctr)
        ctr = VGroup(ctr, ctr_tint)
        inner.move_to(ctr)
        chroma = VGroup(ctr, inner)
        lap = laptop_zone(7.9, 2.15, corner=DOWN + RIGHT)
        place(lap, bottom=-SAFE_Y, cx=-1.2)
        place(chroma, left=lap.get_left()[0] + 0.45, cy=lap.get_center()[1] + 0.05)
        assert chroma.get_right()[0] < lap.caption.get_left()[0] - 0.2
        localhost = names[1]

        # far right: Google's cloud and Gemini
        cl = cloud(width=CLOUD_W, color=CLOUD, fill_opacity=0.08)
        cl.shift(CLOUD_AT)                        # built around its own origin: keep that origin
        gem = chip("Gemini", CLOUD, size=24, fill_opacity=0.2)
        gem.move_to(CLOUD_AT + np.array([0.38, 0.27, 0]) * CLOUD_U)    # right of centre: a longer run
        gcl = label("Google Cloud", 20, CLOUD).move_to(CLOUD_AT + np.array([0.3, -0.42, 0]) * CLOUD_U)
        sky = VGroup(cl, gcl, gem)
        apart(sky, staff, 0.2)
        apart(sky, panel, 0.3)
        inside_frame(qcard, staff, panel, lap, sky)
        apart(panel, lap, 0.6)

        cur = Rectangle(width=0.035, height=0.3, stroke_width=0).set_fill(INK, 1)
        cur.move_to(q_rows[0].get_left() + RIGHT * 0.03)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(qcard), run_time=0.5)
            self.add(cur)                                    # a cursor waits in the empty card
            for _ in range(int(vo.time_until("describe where cheese making") / 0.6)):
                self.play(cur.animate.set_opacity(0), run_time=0.3)
                self.play(cur.animate.set_opacity(1), run_time=0.3)
            vo.wait_until("describe where cheese making")
            self.remove(cur)
            self.play(type_in(q_glyphs, 2.4))
            self.play(FadeIn(lap), FadeIn(chroma, shift=UP * 0.15), run_time=0.7)
            self.play(FadeIn(sky, shift=LEFT * 0.2), run_time=0.7)
            vo.wait_until("In the staff's recorded run")
            self.play(FadeIn(staff, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("these two lines print")
            self.play(FadeIn(panel), run_time=0.5)
            vo.wait_until("a function called")
            self.play(type_in(row_glyphs[0], 0.9))
            vo.wait_until("and its arguments")
            self.play(type_in(row_glyphs[1], 1.0))
            self.play(type_in(row_glyphs[2], 0.8))

        # ========================================================== 1. ten passages, and localhost
        args_span = substring(arrow_row, ARGS_REST)
        start = np.array([args_span.get_center()[0], panel.frame.get_bottom()[1] - 0.05, 0])
        start[0] = cyl.get_center()[0]
        dip = Arrow(start, cyl.top.get_top() + UP * 0.03, buff=0, color=LOOKUP, stroke_width=5,
                    max_tip_length_to_length_ratio=0.12, tip_length=0.22)
        args_ul = under(args_span, LOOKUP)
        author_ul = under(substring(panel.rows[1], MASK), TURN)
        # ten GREEN cards, each labelled "one book", in two rows right of the arrow
        cards = VGroup()
        for _ in range(10):
            c = chunk_card(1.3, 0.44, rows=0)
            t = note("one book").move_to(c)
            cards.add(VGroup(c, t))
        slots = VGroup(*[c.copy() for c in cards]).arrange_in_grid(2, 5, buff=(0.1, 0.1))
        place(slots, left=dip.get_right()[0] + 0.35, top=panel.frame.get_bottom()[1] - 0.35)
        assert slots.get_bottom()[1] > lap.get_top()[1] + 0.08, slots.get_bottom()
        for c, s in zip(cards, slots):
            c.move_to(cyl.get_center()).scale(0.3)
            c.target_pos = s.get_center()
            c.set_opacity(0)
        # the RED dashed line from Gemini toward localhost:8000, stopped at the cloud's edge
        g0 = gem.get_left() + DOWN * 0.12
        aim = localhost.get_center()
        d = (aim - g0) / np.linalg.norm(aim - g0)
        k = 0.0
        while in_cloud(g0 + d * (k + 0.02)):
            k += 0.02
        stop = g0 + d * k
        red = DashedLine(g0, stop, color=ERR, stroke_width=4, dash_length=0.12)
        n = np.array([-d[1], d[0], 0])
        stop_bar = Line(stop - n * 0.18, stop + n * 0.18, color=ERR, stroke_width=5)
        lh_chip = chip("localhost = this machine", S.GREY, size=20)
        place(lh_chip, left=min(stop[0] - 0.15, SAFE_X - lh_chip.width), top=min(stop[1] - 0.1, cl.get_bottom()[1]))
        apart(lh_chip, slots, 0.1)
        apart(lh_chip, panel, 0.1)
        inside_frame(lh_chip, slots)
        # the two questions, centre
        qa = label("Who searched your database?", 32, TURN)
        qb = label("Who chose the book?", 32, TURN)
        qs = VGroup(qa, qb).arrange(DOWN, buff=0.3).move_to([0, 0.35, 0])
        qs_bg = Rectangle(width=13.0, height=qs.height + 0.7, stroke_width=0).set_fill(S.BG, 0.9) \
            .move_to([0, qs.get_center()[1], 0])                 # a band across the dimmed picture
        picture = VGroup(qcard, staff, panel, lap, chroma, sky)

        with self.voiceover(SAY[1]) as vo:
            self.play(Create(args_ul), GrowArrow(dip), run_time=0.8)
            self.add(cards)
            self.play(LaggedStart(*[c.animate(path_arc=-0.6).scale(1 / 0.3).move_to(c.target_pos)
                                    .set_opacity(1) for c in cards], lag_ratio=0.12), run_time=1.6)
            vo.wait_until("all from one book")
            self.play(LaggedStart(*[Indicate(c[1], color=INK, scale_factor=1.15) for c in cards],
                                  lag_ratio=0.06), run_time=1.0)
            vo.wait_until("filtered by author")
            self.play(Create(author_ul), run_time=0.5)
            vo.wait_until("But Gemini runs")
            self.play(Indicate(gem, color=CLOUD, scale_factor=1.1), run_time=0.6)
            self.play(Create(red), run_time=0.8)
            vo.wait_until("where localhost means nothing")
            self.play(Create(stop_bar), FadeIn(lh_chip, shift=UP * 0.1),
                      Indicate(localhost, color=LOOKUP, scale_factor=1.1), run_time=0.7)
            vo.wait_until("So who searched")
            dimmed = VGroup(picture, dip, args_ul, author_ul, cards, red, stop_bar, lh_chip)
            self.play(dimmed.animate.fade(0.8), FadeIn(qs_bg), run_time=0.5)
            self.play(Write(qa), run_time=0.9)
            vo.wait_until("and who chose the book")
            self.play(Write(qb), run_time=0.8)

        # ========================================================== 2. the lecture: a trip to Paris
        lr = lref("20–22")
        lr_cap = note("the lecture slides this stands on")
        place(lr_cap, right=SAFE_X, top=lr.get_bottom()[1] - 0.06)
        # the small YELLOW questions card, top right (stays until the end)
        ya = label("Who searched your database?", 20, TURN)
        yb = label("Who chose the book?", 20, TURN)
        ytx = VGroup(ya, yb).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        yfr = box(ytx.width + 0.45, ytx.height + 0.32, TURN, fill=S.BG, fill_opacity=0.95, radius=0.12)
        ytx.move_to(yfr)
        ycard = VGroup(yfr, ytx)
        place(ycard, right=QCARD_RIGHT, top=QCARD_TOP)
        apart(ycard, lr_cap, 0.05)
        # the request (our words, slide 20)
        req_rows = VGroup(*[label(s, 24, INK) for s in REQUEST]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        dots = VGroup(*[Circle(radius=0.05, stroke_width=0).set_fill(S.GREY, 1)
                        .next_to(r, LEFT, buff=0.22) for r in req_rows])
        req_body = VGroup(dots, req_rows)
        req_fr = card_frame(req_body.width + 0.7, req_body.height + 0.5)
        req_body.move_to(req_fr)
        req_head = note("a trip request · in our words").next_to(req_fr, UP, buff=0.08) \
            .align_to(req_fr, LEFT).shift(RIGHT * 0.12)
        req = VGroup(req_fr, req_body, req_head)
        place(req, cx=-1.4, top=2.6)
        apart(req, ycard, 0.2)
        ask = label("Can an LLM or RAG alone do this?", 28, INK)
        place(ask, cx=0, top=req.get_bottom()[1] - 0.5)
        v_llm = chip("LLM: drafts a plan, can't act as things change", CLOUD, size=24)
        v_rag = chip("RAG: fetches and summarizes", CTR, size=24, fill_opacity=0.0)
        verdicts = VGroup(v_llm, v_rag).arrange(RIGHT, buff=0.4)
        place(verdicts, cx=0, top=ask.get_bottom()[1] - 0.45)
        # beat 3: what's missing (slide 22)
        miss_lbl = label("missing:", 24, S.GREY)
        miss = VGroup(*[concept_box(s, size=24) for s in MISSING]).arrange(RIGHT, buff=0.35)
        miss_row = VGroup(miss_lbl, miss).arrange(RIGHT, buff=0.35)
        place(miss_row, cx=0, top=verdicts.get_bottom()[1] - 0.75)
        inside_frame(req, ask, verdicts, miss_row, ycard, lr_cap)

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeIn(lr), FadeIn(lr_cap, shift=DOWN * 0.1),
                      FadeOut(dimmed, scale=0.4), FadeOut(qs_bg),
                      ReplacementTransform(qa, ya), ReplacementTransform(qb, yb), FadeIn(yfr),
                      run_time=1.0)
            self.remove(dimmed, qs_bg, ya, yb, yfr)
            self.add(ycard)
            vo.wait_until("plan five days in Paris")
            self.play(FadeIn(req_fr), FadeIn(req_head), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(VGroup(dots[i], req_rows[i]), shift=RIGHT * 0.15)
                                    for i in range(3)], lag_ratio=0.5), run_time=1.3)
            vo.wait_until("and replan if it rains")
            self.play(FadeIn(VGroup(dots[3], req_rows[3]), shift=RIGHT * 0.15), run_time=0.5)
            vo.wait_until("A model can draft")
            self.play(FadeIn(ask, shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(v_llm, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("and RAG can fetch")
            self.play(FadeIn(v_rag, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("but neither can act")
            self.play(pulse(v_llm.box, CLOUD, 1.04), pulse(v_rag.box, CTR, 1.04), run_time=0.8)
        self.play(FadeOut(lr_cap), run_time=0.4)
        self.remove(lr_cap)

        # ========================================================== 3. what's missing
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeIn(miss_lbl, shift=RIGHT * 0.1), run_time=0.4)
            for c, a in zip(miss, ["live systems", "tools that act", "and the autonomy"]):
                vo.wait_until(a)
                self.play(FadeIn(c, shift=UP * 0.2), run_time=0.45)

        # ========================================================== 4. three steps, three bands
        band_w, band_h, gap = 10.7, 1.42, 0.2
        bx0 = -5.45
        titles = [("by hand", "llm-rag --agent", True), ("with a framework", "Google ADK", False),
                  ("with a harness", "two Colab notebooks", False)]
        glyph_sets = [
            (VGroup(container_glyph(), chip("Gemini", CLOUD, size=22)), "Docker · Gemini on Vertex AI"),
            (VGroup(uv_glyph(), chip("Gemini", CLOUD, size=22)), "uv · the Gemini API"),
            (VGroup(notebook_glyph(0.62, CLOUD, check=True)), "OpenAI"),
        ]
        bands = VGroup()
        top0 = 1.55
        for i, ((a, b, b_mono), (gl, cap)) in enumerate(zip(titles, glyph_sets)):
            fr = box(band_w, band_h, S.GREY, fill_opacity=0.04, radius=0.16)
            place(fr, left=bx0, top=top0 - i * (band_h + gap))
            head = VGroup(label(a, 26, INK), label("·", 26, S.GREY),
                          mono(b, 24, INK) if b_mono else label(b, 26, INK)).arrange(RIGHT, buff=0.18)
            place(head, left=fr.get_left()[0] + 0.4, cy=fr.get_center()[1])
            gl.arrange(RIGHT, buff=0.3)
            cp = note(cap)
            right = VGroup(gl, cp).arrange(DOWN, buff=0.14)
            place(right, cx=fr.get_left()[0] + 8.3, cy=fr.get_center()[1])
            assert head.get_right()[0] < right.get_left()[0] - 0.3, (i, head.get_right(), right.get_left())
            assert right.get_right()[0] < fr.get_right()[0] - 0.2, (i, right.get_right())
            band = VGroup(fr, head, right)
            bands.add(band)
        assert bands.get_bottom()[1] > -SAFE_Y, bands.get_bottom()
        apart(bands, ycard, 0.1)
        # the Cheese Quiz along the left edge, spanning both parts
        cq_txt = VGroup(note("ideas along the way:"), note("the Cheese Quiz notebook")) \
            .arrange(DOWN, buff=0.1).rotate(PI / 2)
        cq_fr = box(cq_txt.width + 0.3, bands.height, S.GREY, fill_opacity=0.08, radius=0.14)
        place(cq_fr, right=bx0 - 0.12, cy=bands.get_center()[1])
        cq_txt.move_to(cq_fr)
        cq = VGroup(cq_fr, cq_txt)
        # part markers at the right edge
        xr = bands.get_right()[0] + 0.14
        b1 = v_bracket(bands[0].get_top()[1], bands[0].get_bottom()[1], xr + 0.12, opens=LEFT)
        b2 = v_bracket(bands[1].get_top()[1], bands[2].get_bottom()[1], xr + 0.12, opens=LEFT)
        p1 = label("part 1", 22, S.GREY).next_to(b1, RIGHT, buff=0.1)
        p2 = label("part 2", 22, S.GREY).next_to(b2, RIGHT, buff=0.1)
        parts = VGroup(b1, b2, p1, p2)
        inside_frame(bands, cq, parts)

        with self.voiceover(SAY[4]) as vo:
            clear_stage(self, keep=(ycard,), run_time=0.6)              # the lecture tag leaves too
            for band, a in zip(bands, ["By hand", "with a framework", "and with a harness"]):
                vo.wait_until(a)
                self.play(FadeIn(band[0]), FadeIn(band[1], shift=RIGHT * 0.15), run_time=0.45)
                self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.1) for m in band[2]], lag_ratio=0.4),
                          run_time=0.6)
            self.play(FadeIn(cq, shift=RIGHT * 0.15), run_time=0.5)
            self.play(Create(b1), FadeIn(p1), run_time=0.4)
            self.play(Create(b2), FadeIn(p2), run_time=0.4)
        self.wait(0.8)

        # ========================================================== 5. how to follow along
        trs = [tracker("Agents", 1), tracker("Start", 1), tracker("CQ-Pre", 1)]
        wmax = max(t.width for t in trs)
        hmax = max(t.height for t in trs)
        halo = RoundedRectangle(width=wmax + 0.16, height=hmax + 0.14, corner_radius=0.1,
                                stroke_color=TURN, stroke_width=4).set_fill(opacity=0)
        place(halo, left=trs[0].get_left()[0] - 0.08, top=trs[0].get_top()[1] + 0.07)
        sample = lref("51–53")
        apart(sample, ycard, 0.05)
        t = term(P_CTR, rows=3, container=True)
        prev = preview_tag()
        place(prev, right=t.box.get_right()[0] - 0.2, bottom=t.box.get_top()[1] + 0.1)
        tag_row = VGroup(recorded_tag(), expected_tag(), illustration_tag(), extra_tag(), standin_tag(),
                         grey_tag("no key"), notsent_tag()).arrange(RIGHT, buff=0.18)
        place(tag_row, cx=0, bottom=prev.get_top()[1] + 0.35)
        inside_frame(halo, sample, t, tag_row)
        apart(tag_row, ycard, 0.2)

        with self.voiceover(SAY[5]) as vo:
            clear_stage(self, keep=(ycard,), run_time=0.6)
            vo.wait_until("The tracker, top left")
            self.play(FadeIn(trs[0], shift=DOWN * 0.15), Create(halo), run_time=0.6)
            self.play(pulse(halo, TURN, 1.03, 0.5))
            self.play(FadeTransform(trs[0], trs[1]), run_time=0.6)
            self.play(pulse(halo, TURN, 1.03, 0.5))
            self.play(FadeTransform(trs[1], trs[2]), run_time=0.6)
            vo.wait_until("the gray tag, top right")
            self.play(FadeOut(trs[2]), FadeOut(halo), FadeIn(sample), run_time=0.5)
            self.remove(trs[2], halo)
            self.play(sample.box.animate(rate_func=there_and_back).set_stroke(TURN, 5), run_time=0.8)
            vo.wait_until("Pause at each yellow")
            self.play(FadeOut(sample), FadeIn(t), FadeIn(prev), run_time=0.5)
            self.remove(sample)
            ln = type_cmd(self, t, CMD, type_time=1.2)
            pin(self, ln, beside(your_turn(), t, ln))
        self.wait(2)
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.12) for m in tag_row], lag_ratio=0.25), run_time=1.6)
        self.wait(1.0)

        # ========================================================== 6. what you need
        icons, rows = VGroup(), VGroup()
        for s, kind in NEED:
            rows.add(label(s, 24, INK))
            if kind == "key":
                icons.add(key_glyph(0.3))
            else:
                icons.add(RoundedRectangle(width=0.26, height=0.26, corner_radius=0.04,
                                           stroke_color=S.GREY, stroke_width=2.5).set_fill(opacity=0))
        for i, r in enumerate(rows):                       # a fixed pitch: short words sit evenly
            r.move_to([0, -i * 0.56, 0], aligned_edge=LEFT)
        for ic, r in zip(icons, rows):
            ic.move_to([rows.get_left()[0] - 0.5, r.get_center()[1], 0])
        need_head = label("You need", 26, INK)
        need_body = VGroup(icons, rows)
        need_head.next_to(need_body, UP, buff=0.32).align_to(need_body, LEFT)
        need_all = VGroup(need_head, need_body)
        need_fr = card_frame(need_all.width + 0.8, need_all.height + 0.6)
        need_all.move_to(need_fr)
        need = VGroup(need_fr, need_all)
        place(need, cx=-0.9, cy=-0.75)
        inside_frame(need)
        apart(need, ycard, 0.1)
        anchors6 = ["the database and key", "the database and key", "Docker", "uv, Node", "Node, and two",
                    "one from Google AI Studio", "one from OpenAI"]

        with self.voiceover(SAY[6]) as vo:
            clear_stage(self, keep=(ycard,), run_time=0.6)
            self.play(FadeIn(need_fr), FadeIn(need_head, shift=UP * 0.1), run_time=0.5)
            for i, a in enumerate(anchors6):
                vo.wait_until(a)
                self.play(FadeIn(icons[i]), FadeIn(rows[i], shift=RIGHT * 0.15), run_time=0.4)

        # ========================================================== 7. how this was recorded
        r_head = label(REC_HEAD, 26, INK)
        r_rows = VGroup(*[VGroup(*[label(s, 24, INK) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
                          for lines in REC_ROWS]).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        rec_tag = recorded_tag()
        col_w = rec_tag.width
        tick = check_mark(0.36, DATA)
        kg = key_glyph(0.34, S.GREY)
        kx = cross_mark(0.44, S.GREY, stroke=4).move_to(kg)
        r_icons = [tick, VGroup(kg, kx), rec_tag]
        for ic, r in zip(r_icons, r_rows):
            ic.move_to([r_rows.get_left()[0] - 0.3 - col_w / 2, r[0].get_center()[1], 0])
        r_body = VGroup(r_rows, *r_icons)
        r_head.next_to(r_body, UP, buff=0.4).align_to(r_body, LEFT)
        r_all = VGroup(r_head, r_body)
        r_fr = card_frame(r_all.width + 0.8, r_all.height + 0.65)
        r_all.move_to(r_fr)
        rec = VGroup(r_fr, r_all)
        place(rec, cx=-0.7, cy=-0.5)
        inside_frame(rec)
        apart(rec, ycard, 0.1)

        with self.voiceover(SAY[7]) as vo:
            clear_stage(self, keep=(ycard,), run_time=0.6)
            self.play(FadeIn(r_fr), FadeIn(r_head, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("Docker, Chroma")
            self.play(Create(tick), FadeIn(r_rows[0], shift=RIGHT * 0.15), run_time=0.6)
            vo.wait_until("every model call")
            self.play(FadeIn(kg), Create(kx), FadeIn(r_rows[1], shift=RIGHT * 0.15), run_time=0.6)
            vo.wait_until("Model answers")
            self.play(FadeIn(rec_tag, shift=RIGHT * 0.1), FadeIn(r_rows[2], shift=RIGHT * 0.15), run_time=0.6)

        # ========================================================== 8. the name, the study guide
        m_chip = chip(MASK, S.GREY, size=26, text_color=S.GREY, font=MONO)
        m_cap = label("the instructor's name, hidden on screen", 24, INK)
        m_row = VGroup(m_chip, m_cap).arrange(RIGHT, buff=0.4)
        place(m_row, cx=-0.6, cy=0.5)
        foot_txt = VGroup(label("every command:", 24, S.GREY), mono(GUIDE, 22, INK)).arrange(RIGHT, buff=0.25)
        foot_fr = card_frame(foot_txt.width + 0.7, foot_txt.height + 0.5)
        foot_txt.move_to(foot_fr)
        foot = VGroup(foot_fr, foot_txt)
        place(foot, cx=0, cy=-1.4)
        inside_frame(m_row, foot)
        apart(m_row, ycard, 0.1)

        with self.voiceover(SAY[8]) as vo:
            clear_stage(self, keep=(ycard,), run_time=0.6)
            vo.wait_until("On screen we hide")
            self.play(FadeIn(m_chip, scale=0.9), run_time=0.5)
            self.play(FadeIn(m_cap, shift=RIGHT * 0.15), run_time=0.5)
            vo.wait_until("Every command is in")
            self.play(FadeIn(foot, shift=UP * 0.15), run_time=0.6)
        self.wait(1.0)
        clear_stage(self, run_time=0.8)
