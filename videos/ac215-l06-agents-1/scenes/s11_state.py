"""S11 · Runner, session, state: the shared whiteboard (dlops-io/llm-agent-google-adk,
1-baseline/README.md "Pick baseline"). Lecture: 40–41 (and 20–22).

Beats (script.md "## S11", one voiceover block each):
0. TRACKER Base 1. CODE(1-baseline/agent.py: 14–19), header "1-baseline/agent.py · lines 14–19" and the
   GREY subtitle "your copy: baseline/agent.py", on the left (rows of at most 40 characters, so the
   map fits beside it); a YELLOW bar walks model=, instruction=, output_key= as they are named; the
   panel becomes lines 21–26. LECTURE 40–41: the mini-map appears bottom right and grows into the
   right third (V1, compact, glyphs named); as each block is named it lights YELLOW and the argument
   flashes in the code as its label fades in on the map: model= over the LLM core (BLUE), instruction= over Instructions,
   a GREY dashed "tools= · none here" under Tools, output_key= and "within one session" under Memory.
1. The panel becomes lines 35–39; SequentialAgent turns PURPLE and the map's Dynamic Control fills
   PURPLE with the chip "Runner + SequentialAgent"; validator, processor, summarizer flash in turn.
   The panel, the map and the lecture tag leave. TRACKER · extra; the extra card "ask the server for
   the agent tree the UI loads" (top right), and a full-width 11-row terminal (laptop · second
   terminal) prints adk-laptop/31 lines 2–5, each cut after its instruction's first sentence (wrap);
   "model gemini-2.5-flash" boxed YELLOW in the three agent rows, YELLOW tag "from your root .env ·
   yours: the model you set" above the terminal, then the GREY tag "the capture kept
   .env.example's 2.5-flash" beside the tree's last row (the viewer set gemini-3.1-flash-lite in S09);
   the YELLOW tag's border flares at "check yours".
2. The second terminal types `curl -s -X POST http://localhost:8000/apps/baseline/users/student/
   sessions; echo` (extra; folds) -> adk-laptop/32 line 2 (wrap); "state":{} and "events":[] GREEN;
   the session id underlined GREY, tag "your numbers will differ". The terminal shrinks to the 3-row
   strip; V6 starts above it: the GREEN "session state" board with three empty cells
   (itinerary_validation, travel_plan, trip_summary) and the empty events column beside it.
3. V6, captioned "what ADK does once you add your key / no model output was recorded" (tag
   illustration, top right). The strip leaves; the events column slides left, the board right; the
   three LlmAgents (BLUE name chip over the GREY instruction card, cut with …) stand between them, the
   GREY message card (the request text of adk-laptop/33 line 1) at the top. A PURPLE Runner chip takes
   it; a PURPLE frame (the Runner's turn) surrounds ItineraryValidator; its chip lights (GOLD tick per
   call); a blank GREEN reply card flies into cell 1 ("goes into the state") and an event block stacks;
   at "under its output key" the GREEN label output_key and its arrow trace the route and the cell's
   name itinerary_validation flashes GREEN.
   The frame moves to TravelPlanner; the PINK hole {itinerary_validation} flashes and a copy of cell
   1's card flies into it before the chip lights; its reply fills cell 2.
4. TripSummarizer reads {travel_plan} the same way and fills cell 3; three event blocks stand in the
   column, labelled "the Events tab". GREY crossed-out arrows between the agents, "no calls between
   agents"; the board flashes GREEN; thin GREY lines run from the events column into each instruction
   card, labelled "history". The picture dims under a GREY dashed coda (tag concept · module README
   only): ParallelAgent fills three cells at once on three branch lines.
5. LECTURE 20–22. The picture fades under the coda's scrim, then the scrim lifts off the three agents
   as they slide left (no flash of the full picture); the lecture's request
   card (from S01, in our words) appears at the right with the GREY dashed chips "live systems" and
   "tools that act"; each agent shows a GREY dashed "tools= none"; the two chips slide toward the
   pipeline, find nothing to attach to and dim. Caption "costs: the model's own estimates"; a GREY
   dashed chip "later · the trip planner notebook".
6. LECTURE 40–41. README chip "README.md · line 140 (excerpt)" "Memory: Structured state tied to a
   session_id" (expected); the board returns with its three cards, titled "session state · one
   session"; a second, empty board "new session" slides in while the first dims ("nothing carries
   over"); a GREY dashed box "memory across sessions / the lecture's sense / not in today's runs"
   holds the sheet "a profile from past sessions", tag "typed into the notebook (cell 42)".
7. TRACKER · extra. Extra card "send a trip request with the placeholder key (POST /run)"; a 2-row
   second terminal prints adk-laptop/33 line 2 "Internal Server Error" (tag real run · placeholder
   key); in the band between the two terminals a small route: GREY "adk web · your laptop" holding the
   GOLD key "placeholder key", a PINK arrow across a GREY dashed boundary to the BLUE "Gemini API". The
   server strip (laptop) prints adk-laptop/29 lines 357–363 joined, cut after "Please pass a valid API
   key." (wrap), RED; "API key not valid" flashes; at "The placeholder reached Google" the key travels
   to the Gemini API ("google.genai" underlined); at "and was refused" a RED arrow "400" comes back, a
   RED cross lands on the key and "400 INVALID_ARGUMENT" flashes.
8. The "with your key, look for" card writes in its two items as named, each citing the code line
   behind it (agent.py · line 37, the sub_agents order; lines 18, 25, 32, the output_key= lines);
   PANEL(adk-laptop/29: 41–42 joined, "adk web log", wrapped with GREY ↪) with baseline/.adk/session.db
   PINK and the PINK tag "a file in the agent's folder" under the path. ▶ your turn on a static GREY
   card (pick baseline · the trip request; GOLD last line "3 Gemini calls per request · free tier has
   limits"); the PINK tag fades as it enters, so no tags stack over the ▶. Hold 2 s. Fade to an
   empty frame.
"""

import numpy as np
from common import (
    COST,
    DATA,
    ERR,
    INK,
    LOOKUP,
    MINI_CENTER,
    NARRATION,
    P_ADK,
    SECOND,
    STATE_KEYS,
    STRIP_TOP,
    TOOL,
    TURN,
    AgentCard,
    Anatomy,
    AnatomyMini,
    Envelope,
    LookFor,
    Prose,
    Whiteboard,
    _with_header,
    beside,
    capture,
    caption_extra,
    col_box,
    concept_box,
    concept_tag,
    cost_tick,
    covers_text,
    differ_tag,
    excerpt,
    extra_card,
    extra_tag,
    grey_tag,
    illustration_tag,
    key_glyph,
    log_panel,
    lref,
    note,
    pin,
    placeholder_tag,
    readme_chip,
    resize,
    sans,
    src_panel,
    term,
    tracker,
    turn_card,
    type_cmd,
    under,
    wrapped_at,
    your_copy,
)
from manim import (
    DOWN,
    LEFT,
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
    Indicate,
    LaggedStart,
    Line,
    Rectangle,
    ReplacementTransform,
    RoundedRectangle,
    Transform,
    VGroup,
    smooth,
    squish_rate_func,
    there_and_back,
)
from pygments.token import Punctuation, String

from explainer import style as S
from explainer.devops import (
    CAPTION,
    HOUSE_CODE_STYLE,
    MONO,
    box,
    chip,
    cross_mark,
    glyph_range,
    label,
    mono,
    substring,
    tag,
)
from explainer.scene import VoiceScene

SAY = NARRATION["S11"]

# ------------------------------------------------------------------ the real sources and captures
AGENT_PY = "1-baseline/agent.py"
YOUR_COPY = your_copy(AGENT_PY)
assert YOUR_COPY == "your copy: baseline/agent.py", YOUR_COPY
L17, L24, L31 = (excerpt(AGENT_PY, n, n) for n in (17, 24, 31))
INSTR = {   # what each AgentCard shows of its instruction (cut with …; the pieces are the code's own)
    "ItineraryValidator": ("You validate trip requests. …", None),
    "TravelPlanner": ("Using {itinerary_validation}, …", "{itinerary_validation}"),
    "TripSummarizer": ("… based on {travel_plan}. …", "{travel_plan}"),
}
for _ln, (_shown, _) in zip((L17, L24, L31), INSTR.values()):
    for _piece in _shown.split("…"):
        assert _piece.strip(" ") in _ln, (_piece, _ln)
assert 'name="TravelPlanner"' in excerpt(AGENT_PY, 22, 22)
assert "sub_agents=[validator, processor, summarizer]" in excerpt(AGENT_PY, 37, 37)

TREE = capture("31", "adk-laptop")            # extra: the agent tree the dev UI loads
TREE_ROWS = [TREE.line(2), TREE.cut(3, "You validate trip requests."), TREE.line(4),
             TREE.cut(5, "{travel_plan}.")]
assert TREE_ROWS[0] == "TravelPlannerPipeline | Sequential itinerary planning pipeline", TREE_ROWS[0]
assert TREE_ROWS[2].endswith("key booking recommendations."), TREE_ROWS[2]   # one sentence: all of it
MODEL_TXT = "model gemini-2.5-flash"
assert all(MODEL_TXT in r for r in TREE_ROWS[1:]), TREE_ROWS
assert [r.split("|")[0].strip() for r in TREE_ROWS[1:]] == ["ItineraryValidator", "TravelPlanner",
                                                            "TripSummarizer"]
assert all(f"output_key {k}" in r for k, r in zip(STATE_KEYS, TREE_ROWS[1:]))

SESS = capture("32", "adk-laptop")            # extra: a new session
assert SESS.cmd == "curl -s -X POST http://localhost:8000/apps/baseline/users/student/sessions; echo"
SESS_OUT = SESS.line(2)
SESS_ID = SESS_OUT.split('"id":"')[1].split('"')[0]
assert '"state":{}' in SESS_OUT and '"events":[]' in SESS_OUT, SESS_OUT

RUN = capture("33", "adk-laptop")             # extra: a trip request with the placeholder key
MSG = "2 adults, Boston to Montreal, Oct 30 - Nov 2, 1500 dollars, train preferred"
assert f'"text": "{MSG}"' in RUN.cmd, RUN.cmd
assert RUN.line(2) == "Internal Server Error", RUN.line(2)

WEB = capture("29", "adk-laptop")             # the adk web server's log
_err = WEB.join(*range(357, 364))
ERR_ROW = _err[:_err.index("Please pass a valid API key.") + len("Please pass a valid API key.")]
assert ERR_ROW.startswith("google.genai.errors.ClientError: 400 INVALID_ARGUMENT."), ERR_ROW
SESSION_LOG = WEB.join(41, 42)
SESSION_DB = "/home/student/AC215/llm-agent-google-adk/baseline/.adk/session.db"
assert SESSION_LOG.endswith("Creating local session service at " + SESSION_DB), SESSION_LOG
LOG_ROWS = [SESSION_LOG[:SESSION_LOG.index(" Creating")],        # wrapped at spaces, GREY ↪
            "  ↪ Creating local session service at",
            "  ↪ " + SESSION_DB]
assert " ".join(r.replace("  ↪ ", "") for r in LOG_ROWS) == SESSION_LOG

README_140 = excerpt("llm-agent-google-adk/README.md", 140, 140)
assert README_140.startswith("- **Memory**: Structured state tied to a `session_id`"), README_140
MEMORY_PHRASE = "Memory: Structured state tied to a session_id"

REQUEST = ["5 days in Paris", "flights and hotels within budget", "activities you'd enjoy",
           "replan if it rains or a flight is late"]     # S01's card (slide 20, in our words)
MISSING = ["live systems", "tools that act"]              # S01's chips (slide 22)

STR_HEX = "#" + HOUSE_CODE_STYLE.style_for_token(String)["color"]
PUN_HEX = "#" + HOUSE_CODE_STYLE.style_for_token(Punctuation)["color"]

# ------------------------------------------------------------------ layout
SAFE_X = 6.5
CODE_L, CODE_TOP = -6.45, 2.5     # the code panel (its header sits above, under the tracker band)
CODE_COLS = 40                    # characters a code row (the map takes the right third)
MAP_R, MAP_TOP = 6.5, 2.2         # V1, compact, right third
MID_L = -3.75                     # V6: the agents' left edge
EV_W = 1.75                       # V6: the events column
BOARD_L, V6_TOP = 2.62, 1.95      # V6: the board's left edge, the board / events / first agent's top
A_TOPS = (1.95, 0.5, -0.95)       # V6: the three agents' tops
CROSS_X = 1.15                    # V6: the crossed-out "call" arrows between agents
MSG_Y = 2.45                      # V6: the Runner and the message


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


def pop(m, k: float = 1.08):
    """A colour-safe emphasis (Indicate would flood a filled box with its colour): m swells and
    settles back."""
    return m.animate(rate_func=there_and_back).scale(k)


def flare(frame, color: str, width: float = 6):
    """A frame's border flares (thicker, in `color`) and settles back."""
    return frame.animate(rate_func=there_and_back).set_stroke(color, width)


def attach(scene, row, *mobs):
    """Make mobs (already on screen) part of terminal row `row`: they scroll and fade with it."""
    for m in mobs:
        scene.remove(m)
        row.add(m)
    scene.add(row)


def scene_level(scene, *mobs) -> list:
    """The mobjects in mobs' families that sit on the scene at top level. Fading these one by one
    keeps their place in the drawing order; FadeOut of a wrapper group re-adds it on top."""
    out = []

    def walk(m):
        if any(m is s for s in scene.mobjects):
            out.append(m)
        else:
            for s in m.submobjects:
                walk(s)

    for m in mobs:
        walk(m)
    return out


def dashed_card(w: float, h: float, color: str = S.GREY, radius: float = 0.16) -> VGroup:
    """An opaque card with a dashed border (a lecture-only concept). .bg .frame"""
    bg = RoundedRectangle(width=w, height=h, corner_radius=radius, stroke_width=0).set_fill(S.BG, 1)
    d = box(w, h, color, dashed=True, radius=radius)
    g = VGroup(bg, d)
    g.bg, g.frame = bg, d
    return g


# ------------------------------------------------------------------ the code panel (left two thirds)
def wrap_rows(line: str, cols: int = CODE_COLS) -> list[str]:
    """The continuation rows (text only) of a code line wrapped at spaces to `cols` characters:
    row 1 holds up to cols, every later row cols minus the indent and '  ↪ '."""
    indent = line[:len(line) - len(line.lstrip())]
    rows, rest, lim, first = [], line, cols, True
    while len(rest) > lim:
        i = rest.rfind(" ", len(indent) + 1 if first else 1, lim + 1)
        assert i > 0, rest
        rows.append(rest[:i])
        rest = rest[i + 1:]
        lim, first = cols - len(indent) - 4, False
    rows.append(rest)
    return rows[1:]


def color_strings(panel, nums):
    """Workaround (as in S03): src_panel wraps before lexing, so a wrapped string literal comes out
    half-coloured. Colour each wrapped line's string from its opening quote to its closing quote;
    the GREY ↪ and the closing ',' keep their colours."""
    rows = panel.code.source.split("\n")

    def glyphs(k, a, b):
        row = rows[k]
        i, j = len("".join(row[:a].split())), len("".join(row[:b].split()))
        return VGroup(*panel.code.code_lines[k][i:j])

    for n in nums:
        ks = panel.rows_of(n)
        if len(ks) < 2 or '"' not in rows[ks[0]]:
            continue
        first = rows[ks[0]]
        glyphs(ks[0], first.index('"'), len(first)).set_color(STR_HEX)
        for k in ks[1:]:
            row = rows[k]
            a = row.index("↪") + 1
            q = row.rfind('"')
            b = q + 1 if q > a else len(row)
            glyphs(k, a, b).set_color(STR_HEX)
            glyphs(k, b, len(row)).set_color(PUN_HEX)
    return panel


def agent_panel(a: int, b: int):
    """1-baseline/agent.py lines a–b, rows of at most CODE_COLS characters, header with the GREY
    "your copy" subtitle, placed top left."""
    spec = {n: wrap_rows(excerpt(AGENT_PY, n, n)) for n in range(a, b + 1)
            if len(excerpt(AGENT_PY, n, n)) > CODE_COLS}
    p = src_panel(AGENT_PY, a, b, wrap=spec or None)
    _with_header(p, f"{AGENT_PY} · lines {a}–{b}", subtitle=YOUR_COPY)
    color_strings(p, list(spec))
    p.shift(np.array([CODE_L - p.code.get_left()[0], CODE_TOP - p.code.get_top()[1], 0]))
    return p


# ------------------------------------------------------------------ V1, labelled
def labelled_map():
    """V1 compact in the right third, and the labels the constructor's arguments become.
    Returns (anatomy, labels dict)."""
    an = Anatomy(box_w=4.6, block_h=0.8, bar_h=1.0, ends=False, size=20)
    place(an, right=MAP_R, top=MAP_TOP)
    fr = an.frames
    top = an.parts["box"].get_top()[1]
    bot = an.parts["box"].get_bottom()[1]
    lab = {}
    lab["core"] = mono("model=", CAPTION, S.BLUE).move_to([fr["core"].get_x(), top + 0.25, 0])
    lab["instructions"] = mono("instruction=", CAPTION, INK).move_to([fr["instructions"].get_x(), top + 0.25, 0])
    t_in = VGroup(mono("tools=", CAPTION, S.GREY), label("none here", CAPTION, INK)).arrange(DOWN, buff=0.1)
    t_bx = box(t_in.width + 0.4, t_in.height + 0.26, S.GREY, dashed=True, radius=0.14).move_to(t_in)
    lab["tools"] = VGroup(t_bx, t_in)
    lab["memory_key"] = mono("output_key=", CAPTION, INK)
    lab["memory_note"] = note("within one session")
    place(lab["tools"], top=bot - 0.2)
    lab["tools"].set_x(fr["tools"].get_x())
    place(lab["memory_key"], top=bot - 0.2)
    lab["memory_key"].set_x(fr["memory"].get_x() + 0.15)
    place(lab["memory_note"], top=lab["memory_key"].get_bottom()[1] - 0.12, right=SAFE_X)
    assert lab["tools"].get_right()[0] < lab["memory_note"].get_left()[0] - 0.05
    # the Dynamic Control bar, filled: its name moves up, the chip goes under it
    bar = fr["control"]
    ctl_chip = chip("Runner + SequentialAgent", TOOL, size=CAPTION)
    ctl_chip.move_to([bar.get_x(), bar.get_bottom()[1] + 0.08 + ctl_chip.height / 2, 0])
    name_to = an.names["control"].copy().move_to([bar.get_x(), bar.get_top()[1] - 0.08
                                                  - an.names["control"].height / 2, 0])
    assert ctl_chip.width < bar.width - 0.2 and name_to.get_bottom()[1] > ctl_chip.get_top()[1]
    lab["control_chip"], lab["control_name"] = ctl_chip, name_to
    return an, lab


# ------------------------------------------------------------------ V6 helpers
def runner_frame(mob, color: str = TOOL) -> RoundedRectangle:
    """The PURPLE frame of the Runner's turn around an agent."""
    return RoundedRectangle(width=mob.width + 0.26, height=mob.height + 0.18, corner_radius=0.14,
                            stroke_color=color, stroke_width=3).set_fill(opacity=0).move_to(mob)


def message_card() -> VGroup:
    """The GREY user message (the request text of adk-laptop/33). .frame .text"""
    t = sans(MSG, CAPTION, INK)
    fr = box(t.width + 0.5, t.height + 0.3, S.GREY, fill=S.BG, fill_opacity=1.0, radius=0.12)
    t.move_to(fr)
    g = VGroup(fr, t)
    g.frame, g.text = fr, t
    return g


def crossed_arrow(top_y: float, bot_y: float, x: float = CROSS_X) -> VGroup:
    """A GREY 'call' arrow from one agent to the next, crossed out."""
    a = Arrow([x, top_y, 0], [x, bot_y, 0], buff=0.0, color=S.GREY, stroke_width=3,
              max_tip_length_to_length_ratio=0.25, tip_length=0.14)
    x_ = cross_mark(0.22, ERR, stroke=4).move_to(a.get_center())
    return VGroup(a, x_)


def coda_card() -> VGroup:
    """The GREY dashed coda (concept · module README only): ParallelAgent fills three cells at once
    on three branch lines. .frame .chip .lines .cells .tag"""
    w, h = 6.0, 2.3
    fr = dashed_card(w, h)
    pa_chip = chip("ParallelAgent", S.GREY, size=CAPTION, font=MONO)
    pa_chip.move_to(fr.get_center() + LEFT * 1.55 + DOWN * 0.1)
    cells, lines = VGroup(), VGroup()
    for i in range(3):
        c = RoundedRectangle(width=1.5, height=0.42, corner_radius=0.06, stroke_color=DATA,
                             stroke_width=2).set_fill(S.BG, 1)
        c.move_to(fr.get_center() + RIGHT * 1.85 + DOWN * 0.1 + UP * (0.55 * (1 - i)))
        cells.add(c)
        ln = Line(pa_chip.get_right() + RIGHT * 0.05, c.get_left() + LEFT * 0.05, color=S.GREY, stroke_width=2.5)
        lines.add(ln)
    fills = VGroup(*[RoundedRectangle(width=1.2, height=0.24, corner_radius=0.05, stroke_color=DATA,
                                      stroke_width=2).set_fill(DATA, 0.35).move_to(c) for c in cells])
    tg = concept_tag("concept · module README only")
    tg.move_to(fr.get_corner(UP + LEFT) + RIGHT * (0.3 + tg.width / 2))
    g = VGroup(fr, pa_chip, lines, cells, fills, tg)
    g.frame, g.chip, g.lines, g.cells, g.fills, g.tag = fr, pa_chip, lines, cells, fills, tg
    return g


def request_card() -> VGroup:
    """The lecture's trip request (S01's card, our words, slide 20) and its two missing pieces
    (slide 22). .card .chips"""
    rows = VGroup(*[label(s, CAPTION, INK) for s in REQUEST]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    dots = VGroup(*[Circle(radius=0.045, stroke_width=0).set_fill(S.GREY, 1).next_to(r, LEFT, buff=0.2)
                    for r in rows])
    body = VGroup(dots, rows)
    fr = box(body.width + 0.6, body.height + 0.45, S.GREY, fill=S.BG, fill_opacity=1.0, radius=0.14)
    body.move_to(fr)
    head = note("the lecture's trip request · in our words").next_to(fr, UP, buff=0.08) \
        .align_to(fr, LEFT).shift(RIGHT * 0.1)
    card = VGroup(fr, body, head)
    chips = VGroup(*[concept_box(s) for s in MISSING]).arrange(RIGHT, buff=0.3)
    chips.next_to(fr, DOWN, buff=0.35)
    g = VGroup(card, chips)
    g.card, g.chips = card, chips
    return g


def tools_ghost() -> VGroup:
    """A GREY dashed 'tools= none' (the LlmAgent's empty tools)."""
    t = VGroup(mono("tools=", CAPTION, S.GREY), label("none", CAPTION, INK)).arrange(RIGHT, buff=0.12)
    b = box(t.width + 0.36, t.height + 0.22, S.GREY, dashed=True, radius=0.12).move_to(t)
    return VGroup(b, t)


def memory_box() -> VGroup:
    """The lecture's memory (dashed: not in today's runs) with the Cheese Quiz's profile sheet; the
    tag hangs under the box. .frame .rows .sheet .tag"""
    rows = VGroup(label("memory across sessions", CAPTION, INK),
                  note("the lecture's sense"), note("not in today's runs")).arrange(DOWN, aligned_edge=LEFT,
                                                                                    buff=0.12)
    sheet = Envelope(width=4.2, slots=1).sheet("a profile from past sessions", S.GREY)
    inner = VGroup(rows, sheet).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    fr = dashed_card(inner.width + 0.5, inner.height + 0.5)
    inner.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.25)
    tg = grey_tag("typed into the notebook (cell 42)")
    tg.next_to(fr, DOWN, buff=0.15).align_to(fr, RIGHT)
    g = VGroup(fr, rows, sheet, tg)
    g.frame, g.rows, g.sheet, g.tag = fr, rows, sheet, tg
    return g


def route_row(top: float, bottom: float) -> VGroup:
    """Beat 7, in the band between the two terminals: adk web on your laptop (GREY) holds the GOLD
    placeholder key; a PINK route crosses the dashed boundary to the BLUE Gemini API; the RED
    "400" comes back. .web .lap .gem .bnd .out .back .key .no .key_to (where the key lands)"""
    yc = (top + bottom) / 2 + 0.02
    web = chip("adk web", S.GREY, size=CAPTION, font=MONO)
    gem = chip("Gemini API", S.BLUE, size=CAPTION)
    place(web, cx=-4.2, cy=yc)
    place(gem, cx=4.2, cy=yc)
    lap = note("your laptop")
    place(lap, cx=web.get_x(), top=web.get_bottom()[1] - 0.1)
    xa, xb = web.get_right()[0] + 0.14, gem.get_left()[0] - 0.14
    out = Arrow([xa, yc + 0.09, 0], [xb, yc + 0.09, 0], buff=0.0, color=LOOKUP, stroke_width=4,
                max_tip_length_to_length_ratio=0.1, tip_length=0.18)
    back = Arrow([xb, yc - 0.13, 0], [xa, yc - 0.13, 0], buff=0.0, color=ERR, stroke_width=4,
                 max_tip_length_to_length_ratio=0.1, tip_length=0.18)
    key = VGroup(key_glyph(0.3), label("placeholder key", CAPTION, COST)).arrange(RIGHT, buff=0.14)
    place(key, left=xa + 0.25, bottom=yc + 0.25)
    key_to = key.copy()
    place(key_to, right=xb - 0.3)
    bx = (xa + xb) / 2
    bnd = DashedLine([bx, top - 0.12, 0], [bx, bottom + 0.12, 0], color=S.GREY, stroke_width=2.5,
                     dash_length=0.12)
    no = mono("400", CAPTION, ERR)
    place(no, cx=(bx + xb) / 2, top=yc - 0.13 - 0.18)
    g = VGroup(bnd, web, lap, gem, out, key, back, no)
    g.web, g.lap, g.gem, g.bnd, g.out, g.back, g.key, g.no, g.key_to = web, lap, gem, bnd, out, back, key, no, key_to
    assert key.get_top()[1] < top - 0.1 and min(lap.get_bottom()[1], no.get_bottom()[1]) > bottom + 0.1, \
        (key.get_top(), lap.get_bottom(), no.get_bottom(), top, bottom)
    assert key.get_left()[0] > xa and key.get_right()[0] < bx - 0.1 and key_to.get_left()[0] > bx + 0.1, \
        (key.get_left(), key.get_right(), key_to.get_left(), bx)
    return g


def board_only(title: str, filled: bool):
    """A session board without its events column (beat 6), optionally with its three reply cards.
    Returns (group, whiteboard)."""
    wb = Whiteboard(cell_pitch=1.0, title=title)
    parts = [wb.parts["board"], *wb.cells]
    if filled:
        for i in range(3):
            c = wb.blank_card(i)
            c.move_to(wb.slot(i))
            parts.append(c)
    return VGroup(*parts), wb


class SharedState(VoiceScene):
    def construct(self):
        assert len(SAY) == 9, len(SAY)

        # ========================================================== 0 · three LlmAgents, the lecture's blocks
        tr = tracker("Base", 1)
        p14 = agent_panel(14, 19)
        p21 = agent_panel(21, 26)
        lr = lref("40–41")
        mini = AnatomyMini(center=MINI_CENTER)
        an, lab = labelled_map()
        assert p21.code.get_right()[0] < an.get_left()[0] - 0.15, p21.code.get_right()
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.25), FadeIn(p14, shift=UP * 0.15), run_time=0.8)
            vo.wait_until("each with a model")
            b1 = p14.bar(16)
            self.play(FadeIn(b1), run_time=0.3)
            vo.wait_until("an instruction")
            b2 = p14.bar(17)
            self.play(ReplacementTransform(b1, b2), run_time=0.3)
            vo.wait_until("and an output key")
            b3 = p14.bar(18)
            self.play(ReplacementTransform(b2, b3), run_time=0.3)
            self.wait(0.5)
            self.play(FadeOut(b3), ReplacementTransform(p14, p21), run_time=0.8)
            vo.wait_until("In the lecture's blocks")
            self.play(FadeIn(lr), FadeIn(mini, scale=0.9), run_time=0.4)
            self.play(FadeTransform(mini, an), run_time=0.9)
            vo.wait_until("the LLM core")
            # each argument flashes on its line and its label fades in on the map (flying copies
            # crossed the code and the map's labels)
            self.play(an.light("core"), Indicate(p21.span(23, "model="), color=TURN, scale_factor=1.1),
                      FadeIn(lab["core"], rate_func=squish_rate_func(smooth, 0.3, 1.0)), run_time=0.7)
            vo.wait_until("the instructions")
            self.play(an.light("instructions"), Indicate(p21.span(24, "instruction="), color=TURN, scale_factor=1.1),
                      FadeIn(lab["instructions"], rate_func=squish_rate_func(smooth, 0.3, 1.0)), run_time=0.7)
            vo.wait_until("and no tools at all")
            self.play(an.light("tools"), FadeIn(lab["tools"], shift=UP * 0.1), run_time=0.6)
            self.play(an.light("memory"), Indicate(p21.span(25, "output_key="), color=TURN, scale_factor=1.1),
                      FadeIn(lab["memory_key"], rate_func=squish_rate_func(smooth, 0.3, 1.0)),
                      FadeIn(lab["memory_note"], shift=UP * 0.1), run_time=0.7)
        self.play(an.unlight(), run_time=0.3)

        # ========================================================== 1 · SequentialAgent; the tree the UI loads
        p35 = agent_panel(35, 39)
        xc1 = extra_card("ask the server for the agent tree the UI loads")
        place(xc1, right=SAFE_X, top=3.55)
        t = term(P_ADK, rows=11, title=SECOND)
        env_tag = tag("from your root .env · yours: the model you set", TURN)
        place(env_tag, left=-6.5, bottom=t.box.get_top()[1] + 0.12)
        assert env_tag.get_right()[0] < xc1.get_left()[0] - 0.1, env_tag.get_right()
        kept_tag = grey_tag("the capture kept .env.example's 2.5-flash")   # S09 set gemini-3.1-flash-lite
        with self.voiceover(SAY[1]) as vo:
            self.play(ReplacementTransform(p21, p35), run_time=0.8)
            self.play(p35.span(35, "SequentialAgent").animate.set_color(TOOL), *an.fill_control(), run_time=0.7)
            self.play(an.names["control"].animate.move_to(lab["control_name"]),
                      FadeIn(lab["control_chip"], shift=UP * 0.08), run_time=0.5)
            for word, sub in (("validator", "validator"), ("planner", "processor"), ("summarizer", "summarizer")):
                vo.wait_until(word)
                self.play(Indicate(p35.span(37, sub), color=TURN, scale_factor=1.15), run_time=0.5)
            vo.wait_until("An extra request")
            self.play(FadeOut(VGroup(p35, an, lab["core"], lab["instructions"], lab["tools"], lab["memory_key"],
                                     lab["memory_note"], lab["control_chip"])), FadeOut(lr), run_time=0.5)
            self.play(FadeIn(xc1, shift=DOWN * 0.15), caption_extra(tr, True), FadeIn(t, shift=UP * 0.2),
                      run_time=0.6)
            printed = [t.print(self, [r], wrap=True, run_time=0.3) for r in TREE_ROWS]
            vo.wait_until("with the model from your root")
            boxes = []
            for rows in printed[1:]:
                r0 = rows[0]
                a = r0.text.index(MODEL_TXT)
                bx = col_box(r0, a, a + len(MODEL_TXT), TURN)
                boxes.append((r0, bx, glyph_range(r0, a, a + len(MODEL_TXT))))
            self.play(*[Create(bx) for _, bx, _ in boxes], *[g.animate.set_color(TURN) for _, _, g in boxes],
                      FadeIn(env_tag, shift=DOWN * 0.1), run_time=0.6)
            for r0, bx, _ in boxes:
                attach(self, r0, bx)
            beside(kept_tag, t, printed[-1][-1])
            assert not covers_text(kept_tag, printed[-1][-1])
            assert kept_tag.get_right()[0] < t.box.get_right()[0] - 0.1, kept_tag.get_right()
            self.play(FadeIn(kept_tag, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("check yours")
            # a flare, not pop(): the tag fills the room between x = -6.5 and the extra card, and a
            # 1.08 swell crossed the safe edge and touched the card's corner at its peak
            self.play(flare(env_tag.box, TURN, 6), run_time=0.7)

        # ========================================================== 2 · a new session: empty state, no events
        wb = Whiteboard(events_w=EV_W, cell_pitch=1.1)
        ev = wb.parts["events"]
        board = VGroup(wb.parts["board"], *wb.cells)
        # the events column on the left of the board, the pair centred above the strip
        ev.shift(RIGHT * (board.get_left()[0] - 0.3 - ev.get_right()[0]))
        place(wb, cx=0, top=STRIP_TOP + 0.14 + wb.height)
        assert wb.get_top()[1] < 2.8, wb.get_top()
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(xc1), FadeOut(env_tag), FadeOut(kept_tag), run_time=0.3)
            cmd = type_cmd(self, t, SESS.cmd, 1.2)
            pin(self, cmd, beside(extra_tag(), t, cmd), run_time=0.3)
            out = t.print(self, [SESS_OUT], wrap=True, run_time=0.4)
            vo.wait_until("an empty state")
            hl = []
            for sub in ('"state":{}', '"events":[]'):
                r, c = wrapped_at(out, sub)        # the row that holds it (word-boundary fold)
                hl.append((r, col_box(r, c, c + len(sub), DATA), glyph_range(r, c, c + len(sub))))
            r, bx, g = hl[0]
            self.play(Create(bx), g.animate.set_color(DATA), run_time=0.4)
            attach(self, r, bx)
            vo.wait_until("and no events yet")
            r, bx, g = hl[1]
            self.play(Create(bx), g.animate.set_color(DATA), run_time=0.4)
            attach(self, r, bx)
            r_id, c = wrapped_at(out, SESS_ID)
            u_id = under(glyph_range(r_id, c, c + len(SESS_ID)), S.GREY, stroke=3)
            self.play(Create(u_id), run_time=0.3)
            attach(self, r_id, u_id)
            pin(self, out[-1], beside(differ_tag(), t, out[-1], buff=0.4), run_time=0.3)
            vo.wait_until("Think of the state")
            resize(self, t, 3, run_time=0.6, extra=[caption_extra(tr, False)])
            self.play(FadeIn(wb.parts["board"], shift=UP * 0.1), run_time=0.5)
            vo.wait_until("shared whiteboard")
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.1) for c in wb.cells], lag_ratio=0.25),
                      FadeIn(ev, shift=RIGHT * 0.1), run_time=0.8)
            self.remove(wb.parts["board"], *wb.cells, ev)
            self.add(wb)

        # ========================================================== 3 · the Runner, output_key, {key}
        cap = VGroup(note("what ADK does once you add your key"), note("no model output was recorded")) \
            .arrange(DOWN, aligned_edge=RIGHT, buff=0.08)
        place(cap, right=SAFE_X, top=3.55)
        ill = illustration_tag()
        place(ill, right=cap.get_left()[0] - 0.25, cy=cap.get_y())
        ags = []
        for (name, (shown, hole)), top in zip(INSTR.items(), A_TOPS):
            a = AgentCard(name, shown, hole=hole)
            place(a, left=MID_L, top=top)
            ags.append(a)
        dy = V6_TOP - wb.get_top()[1]
        d_board = np.array([BOARD_L - board.get_left()[0], dy, 0])
        d_ev = np.array([-SAFE_X - ev.get_left()[0], dy, 0])
        assert ags[1].card.get_right()[0] < BOARD_L - 0.4, ags[1].card.get_right()
        msg = message_card()
        runner = chip("Runner", TOOL, size=CAPTION, font=MONO)
        place(runner, left=-SAFE_X, cy=MSG_Y)
        place(msg, left=runner.get_right()[0] + 0.25, cy=MSG_Y)
        assert msg.get_right()[0] < SAFE_X, msg.get_right()
        cur = runner_frame(ags[0])
        ticks = [cost_tick().next_to(a.model, RIGHT, buff=0.18) for a in ags]
        replies = [wb.blank_card(i) for i in range(3)]
        for c, a in zip(replies, ags):          # each reply emerges, small, at its card's right end
            c.scale(0.35).move_to(a.card.get_right())
        ok_lbl = mono("output_key", CAPTION, DATA)
        place(ok_lbl, left=ticks[0].get_right()[0] + 0.3, cy=ags[0].model.get_y())
        assert ok_lbl.get_right()[0] < BOARD_L - 0.1, ok_lbl.get_right()

        def fly(i):
            """Animations: reply card i (shown at its agent's card) flies into board cell i, growing to
            the cell's card size."""
            target = wb.blank_card(i).move_to(wb.slot(i))
            return [Transform(replies[i], target)]

        def glow(i):
            """The agent's model call: its chip lights, a GOLD tick per call."""
            return [Indicate(ags[i].model, color=S.BLUE, scale_factor=1.12), FadeIn(ticks[i], scale=1.4)]

        def into_hole(i):
            """A copy of board cell i-1's card flies into agent i's PINK hole (its {key})."""
            src = replies[i - 1]
            cp = src.copy()
            h = ags[i].hole
            self.add(cp)
            target = cp.copy().stretch_to_fit_width(h.width - 0.06).stretch_to_fit_height(h.height - 0.03).move_to(h)
            self.play(Transform(cp, target), h.animate.set_fill(LOOKUP, 0.3), run_time=0.8)
            self.remove(cp)
            ags[i].add(cp)
            return cp

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(t, shift=DOWN * 0.2), FadeIn(cap), FadeIn(ill),
                      *[m.animate.shift(d_board) for m in board], ev.animate.shift(d_ev), run_time=1.0)
            ok_arrow = Arrow(ags[0].card.get_right() + RIGHT * 0.08,
                             wb.slot(0).get_left() + LEFT * 0.08, buff=0.0, color=DATA, stroke_width=3,
                             max_tip_length_to_length_ratio=0.3, tip_length=0.14)
            self.play(LaggedStart(*[FadeIn(a, shift=RIGHT * 0.15) for a in ags], lag_ratio=0.2),
                      FadeIn(msg, shift=DOWN * 0.1), run_time=0.9)
            vo.wait_until("the Runner does this")
            self.play(FadeIn(runner, shift=RIGHT * 0.15), run_time=0.4)
            self.play(flare(msg.frame, TOOL, 4), Create(cur), run_time=0.7)
            vo.wait_until("The validator's reply")
            self.play(*glow(0), run_time=0.5)
            self.play(FadeIn(replies[0], shift=RIGHT * 0.15), run_time=0.25)
            self.play(*fly(0), run_time=0.6)                     # "goes into the state"
            e0 = wb.event_block("validator")
            self.play(FadeIn(e0, shift=DOWN * 0.1), run_time=0.3)
            vo.wait_until("under its output key")              # the route it took, and the cell's name
            self.play(FadeIn(ok_lbl, shift=DOWN * 0.05), GrowArrow(ok_arrow),
                      Indicate(wb.cells[0].key, color=DATA, scale_factor=1.1), run_time=0.7)
            vo.wait_until("before the planner runs")
            self.play(Transform(cur, runner_frame(ags[1])), run_time=0.5)
            vo.wait_until("its instruction's placeholder")
            self.play(Indicate(ags[1].hole, color=LOOKUP, scale_factor=1.1), run_time=0.6)
            vo.wait_until("is filled from that cell")
            into_hole(1)
            self.play(*glow(1), run_time=0.5)
            self.play(FadeIn(replies[1], shift=RIGHT * 0.15), run_time=0.25)
            self.play(*fly(1), run_time=0.6)
            e1 = wb.event_block("planner")
            self.play(FadeIn(e1, shift=DOWN * 0.1), run_time=0.3)

        # ========================================================== 4 · the summarizer; no calls between agents; coda
        ev_lbl = note("the Events tab")
        place(ev_lbl, cx=wb.events_frame.get_x(), top=wb.events_frame.get_bottom()[1] - 0.15)
        calls = VGroup(crossed_arrow(ags[0].get_bottom()[1] - 0.04, ags[1].card.get_top()[1] + 0.04),
                       crossed_arrow(ags[1].get_bottom()[1] - 0.04, ags[2].card.get_top()[1] + 0.04))
        no_calls = note("no calls between agents")
        place(no_calls, cx=(MID_L + BOARD_L) / 2, top=ags[2].get_bottom()[1] - 0.2)
        hist = VGroup(*[Line([wb.events_frame.get_right()[0] + 0.04, a.card.get_y(), 0],
                             [a.card.get_left()[0] - 0.06, a.card.get_y(), 0], color=S.GREY, stroke_width=2)
                        for a in ags])
        hist_lbl = note("history")
        place(hist_lbl, cx=(wb.events_frame.get_right()[0] + MID_L) / 2, bottom=hist[0].get_y() + 0.1)
        assert hist_lbl.get_left()[0] > wb.events_frame.get_right()[0], hist_lbl.get_left()
        scrim = Rectangle(width=13.2, height=6.45, stroke_width=0).set_fill(S.BG, 0.82)
        place(scrim, cx=0, top=2.85)
        coda = coda_card()
        place(coda, cx=0, cy=-0.45)
        with self.voiceover(SAY[4]) as vo:
            self.play(Transform(cur, runner_frame(ags[2])), run_time=0.5)
            into_hole(2)
            self.play(*glow(2), run_time=0.5)
            self.play(FadeIn(replies[2], shift=RIGHT * 0.15), run_time=0.25)
            self.play(*fly(2), run_time=0.6)
            e2 = wb.event_block("summarizer")
            self.play(FadeIn(e2, shift=DOWN * 0.1), FadeIn(ev_lbl, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("The agents never call each other")
            self.play(FadeOut(cur), LaggedStart(*[GrowArrow(c[0]) for c in calls], lag_ratio=0.3), run_time=0.6)
            self.play(*[FadeIn(c[1], scale=1.4) for c in calls], FadeIn(no_calls, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("in its state")
            self.play(flare(wb.board_frame, DATA, 8), run_time=0.7)
            vo.wait_until("and its history of events")
            self.play(LaggedStart(*[Create(h) for h in hist], lag_ratio=0.25), FadeIn(hist_lbl),
                      flare(wb.events_frame, INK, 5), run_time=0.9)
            vo.wait_until("A parallel agent")
            self.play(FadeIn(scrim), FadeIn(VGroup(coda.frame, coda.chip, coda.cells, coda.tag), scale=0.96),
                      run_time=0.6)
            self.play(*[Create(ln) for ln in coda.lines], run_time=0.4)
            self.play(*[FadeIn(f, scale=0.6) for f in coda.fills], run_time=0.4)

        # ========================================================== 5 · the lecture's planner needs live systems
        lr20 = lref("20–22")
        req = request_card()
        place(req, right=SAFE_X - 0.05, top=2.6)
        ghosts = [tools_ghost() for _ in ags]
        shift5 = LEFT * (MID_L + SAFE_X - 0.2)
        cost_note = note("costs: the model's own estimates")
        later = concept_box("later · the trip planner notebook")
        v6_rest = VGroup(wb, e0, e1, e2, *replies, ev_lbl, calls, no_calls, hist, hist_lbl, ok_lbl, ok_arrow,
                         runner, msg, *ticks, cap, ill)
        with self.voiceover(SAY[5]) as vo:
            # the picture fades under the scrim (FadeOut of the wrapper would lift it above the scrim
            # first: a flash), then the scrim lifts off the three agents as they slide left
            self.play(FadeOut(coda), *[FadeOut(m) for m in scene_level(self, v6_rest)], run_time=0.6)
            self.play(FadeOut(scrim), *[a.animate.shift(shift5) for a in ags], FadeIn(lr20), run_time=0.7)
            for g, a in zip(ghosts, ags):
                place(g, left=a.model.get_right()[0] + 0.3, cy=a.model.get_y())
            place(cost_note, left=ags[2].get_left()[0], top=ags[2].get_bottom()[1] - 0.3)
            place(later, right=SAFE_X - 0.05, cy=cost_note.get_y())
            self.play(FadeIn(req.card, shift=LEFT * 0.15), run_time=0.6)
            vo.wait_until("needs live systems")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in req.chips], lag_ratio=0.3), run_time=0.6)
            vo.wait_until("this pipeline has no tools")
            self.play(LaggedStart(*[FadeIn(g, shift=RIGHT * 0.1) for g in ghosts], lag_ratio=0.15), run_time=0.6)
            # the two chips reach for the pipeline: nothing to plug into
            stop_x = max(a.card.get_right()[0] for a in ags) + 0.5      # short of the pipeline
            c0, c1 = req.chips
            assert req.card.get_bottom()[1] > ags[1].card.get_top()[1] + 0.2, req.card.get_bottom()
            self.play(c0.animate.move_to([stop_x + c0.width / 2, ags[1].card.get_y(), 0]),
                      c1.animate.move_to([stop_x + c1.width / 2, ags[2].model.get_y(), 0]), run_time=0.8)
            self.play(*[Indicate(g, color=S.GREY, scale_factor=1.08) for g in ghosts], run_time=0.5)
            self.play(req.chips.animate.set_opacity(0.35), run_time=0.4)
            vo.wait_until("so its prices are")
            self.play(FadeIn(cost_note, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("A later notebook")
            self.play(FadeIn(later, shift=LEFT * 0.1), run_time=0.5)
        self.play(FadeOut(lr20), run_time=0.3)

        # ========================================================== 6 · memory: one session, not across sessions
        rc = readme_chip("README.md · line 140 (excerpt)", MEMORY_PHRASE, expected=True)
        place(rc, cx=0, top=2.78)
        b1, w1 = board_only("session state · one session", filled=True)
        b2, w2 = board_only("new session", filled=False)
        place(b1, left=-SAFE_X, top=1.85)
        place(b2, left=b1.get_right()[0] + 0.25, top=1.85)
        mem = memory_box()
        place(mem, right=SAFE_X, top=1.85)
        assert mem.get_left()[0] > b2.get_right()[0] + 0.15, (mem.get_left(), b2.get_right())
        dim1 = Rectangle(width=b1.width + 0.1, height=b1.height + 0.1, stroke_width=0).set_fill(S.BG, 0.65).move_to(b1)
        nothing = note("nothing carries over")
        place(nothing, cx=b2.get_x(), top=b2.get_bottom()[1] - 0.2)
        lr40 = lref("40–41")
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(*ags, *ghosts, req, cost_note, later)), run_time=0.5)
            self.play(FadeIn(rc, shift=DOWN * 0.1), FadeIn(lr40), run_time=0.5)
            self.play(Indicate(rc.phrase, color=TURN, scale_factor=1.04), run_time=0.7)
            vo.wait_until("The code calls it session state")
            self.play(FadeIn(b1, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("and it lasts one session")
            self.play(FadeIn(b2, shift=LEFT * 1.2), FadeIn(dim1), run_time=0.8)
            self.play(FadeIn(nothing, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("the lecture's memory")
            self.play(FadeIn(VGroup(mem.frame, mem.rows), shift=LEFT * 0.15), run_time=0.6)
            self.play(FadeIn(mem.sheet, shift=RIGHT * 0.2), FadeIn(mem.tag), run_time=0.5)
            vo.wait_until("which none of today's runs")
            self.play(Indicate(mem.rows[2], color=TURN, scale_factor=1.1), run_time=0.7)

        # ========================================================== 7 · a trip request with the placeholder key
        xc7 = extra_card("send a trip request with the placeholder key (POST /run)")
        place(xc7, right=SAFE_X, top=3.55)
        t2 = term(P_ADK, rows=2, title=SECOND, top=xc7.get_bottom()[1] - 0.2)
        srv = term(P_ADK, rows=3, title="laptop")
        route = route_row(t2.get_bottom()[1], srv.get_top()[1])
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(rc, b1, b2, dim1, nothing, mem)), FadeOut(lr40), run_time=0.5)
            self.play(FadeIn(xc7, shift=DOWN * 0.15), caption_extra(tr, True), FadeIn(t2, shift=UP * 0.15),
                      run_time=0.6)
            ise = t2.print(self, [RUN.line(2)], run_time=0.3)[0]
            pin(self, ise, beside(placeholder_tag(), t2, ise, buff=0.4), run_time=0.3)
            vo.wait_until("an internal server error")
            self.play(Indicate(ise.glyphs, color=ERR, scale_factor=1.06), run_time=0.6)
            # between the terminals: who holds the key, and where the request goes
            self.play(FadeIn(VGroup(route.bnd, route.web, route.lap, route.gem)), GrowArrow(route.out),
                      FadeIn(route.key, shift=RIGHT * 0.1), run_time=0.7)
            vo.wait_until("The server log says why")
            self.play(FadeIn(srv, shift=UP * 0.15), run_time=0.4)
            err = srv.print(self, [(ERR_ROW, ERR)], wrap=True, run_time=0.5)

            def span_in(rows, sub):
                r, c = wrapped_at(rows, sub)       # the row that holds it (word-boundary fold)
                return glyph_range(r, c, c + len(sub))

            vo.wait_until("API key not valid")
            self.play(Indicate(span_in(err, "API key not valid."), color=ERR, scale_factor=1.12), run_time=0.7)
            vo.wait_until("The placeholder reached Google")
            g_span = span_in(err, "google.genai")
            u_g = under(g_span, S.GREY, stroke=3)
            self.play(route.key.animate.move_to(route.key_to), Create(u_g),
                      Indicate(g_span, color=INK, scale_factor=1.1), run_time=0.8)
            attach(self, err[0], u_g)
            vo.wait_until("and was refused")
            no_x = cross_mark(0.3, ERR, stroke=4).move_to(route.key[0])
            self.play(GrowArrow(route.back), FadeIn(route.no, shift=LEFT * 0.1), FadeIn(no_x, scale=1.4),
                      Indicate(span_in(err, "400 INVALID_ARGUMENT"), color=ERR, scale_factor=1.12), run_time=0.7)
        self.wait(0.8)                                  # let the refusal land before the frame clears

        # ========================================================== 8 · with your key; the session file; ▶
        lf = LookFor([("three replies, in order", "agent.py · line 37"),           # sub_agents=[…]
                      (VGroup(label("State tab:", CAPTION, INK),
                              mono(" · ".join(STATE_KEYS), CAPTION, INK)).arrange(RIGHT, buff=0.15),
                       "lines 18, 25, 32")])                                        # the three output_key=
        place(lf, left=-6.4, top=tr.get_bottom()[1] - 0.12)
        assert lf.get_right()[0] < SAFE_X, lf.get_right()
        assert all(f'output_key="{k}"' in excerpt(AGENT_PY, n, n) for k, n in zip(STATE_KEYS, (18, 25, 32)))
        lp = log_panel(LOG_ROWS, "adk web log")
        place(lp, cx=0, top=lf.get_bottom()[1] - 0.18)
        for r in lp.rows[1:]:
            substring(r, "↪").set_color(S.GREY)
        db_row = lp.rows[2]
        db_span = substring(db_row, "baseline/.adk/session.db")
        db_tag = tag("a file in the agent's folder", LOOKUP)
        place(db_tag, right=lp.frame.get_right()[0] - 0.1, top=lp.frame.get_bottom()[1] - 0.1)   # under the path
        card = turn_card([Prose("pick baseline · send a trip request, e.g."), Prose(f"“{MSG}”"),
                          (Prose("3 Gemini calls per request · free tier has limits"), COST)], header=None)
        place(card, cx=0, bottom=-3.55)
        assert card.get_top()[1] < db_tag.get_bottom()[1] - 0.08, (card.get_top(), db_tag.get_bottom(), tr.get_bottom())
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(xc7, t2, srv, route, no_x)), caption_extra(tr, False), run_time=0.5)
            self.play(FadeIn(lf.frame), FadeIn(lf.title), run_time=0.4)
            vo.wait_until("three replies in order")
            self.play(lf.write_item(0))
            vo.wait_until("and three new entries")
            self.play(lf.write_item(1))
            vo.wait_until("the session is a file")
            self.play(FadeIn(lp, shift=UP * 0.1), run_time=0.5)
            self.play(db_span.animate.set_color(LOOKUP), FadeIn(db_tag, shift=DOWN * 0.08), run_time=0.5)
            vo.wait_until("Each request is three model calls")
            self.play(FadeOut(db_tag), FadeIn(card, shift=UP * 0.15), run_time=0.6)   # no tag stack over the ▶
            vo.wait_until("pause, and plan a trip")
            self.play(pop(card.tag, 1.12), run_time=0.6)
        self.wait(2)                                    # ▶ beat: hold the frame
        self.play(FadeOut(VGroup(tr, lf, lp, card)), run_time=0.8)
        self.wait(0.3)
