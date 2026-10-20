"""S13 · Many agents: who plans the order? (Colab · Cheese Quiz › Cheese Quiz Guild; dlops-io/
llm-agent-google-adk 1-baseline and 5-custom-agent, code panels only). Lecture: 44–49 (and 38).

Beats (script.md "## S13", one voiceover block each):
0. LECTURE 44–49. No tracker. Left: the lecture's research example as a GREY dashed tree (our
   redrawing; title "deep research" + dashed tag "concept · lecture example"): lead agent → planner
   → three parallel "web search" → synthesis → report, each node writing in as it is named. Right,
   two tutorial trees with plain-word nodes: "Cheese Quiz Guild", a BLUE orchestrator over GREEN
   chips facts · write · review · vegan (title line "Cheese Quiz Guild · 4 of its 6 tools": cell 70's
   orchestrator also holds format_quiz_json and ask_head_cheesemonger); "Cheese Newsletter", a BLUE
   orchestrator over researcher · editor · send_email (the tools of cell-25's orchestrator).
1. LECTURE 38. The planner pulses YELLOW as it is named; at "raises the question" the trees fade while
   the YELLOW question "Who plans the order?" writes in at the top; three
   empty dashed slots in a row under it: "the code", "the model", "Python reading the model's
   label". Slot 1 lights alone: CODE(1-baseline/agent.py: 35–39) (subtitle "your copy:
   baseline/agent.py"), SequentialAgent PURPLE, and an assembly line of three GREY stations
   (validator, processor, summarizer) on a PURPLE belt; the order list on line 37 highlighted
   YELLOW while a YELLOW token rides the belt station by station. After the SAY (silent): the panel
   leaves and the line shrinks into slot 1 as a small assembly-line icon.
2. Slot 2 lights; the row folds up out of the way (the question moves right of the tracker and
   stays); TRACKER CQ-Guild 1. CODE(cell-68: 1–8) at 20 pt (lines 5–8 wrapped before their
   description strings, 12 rows): a YELLOW highlighter on `.as_tool(` in lines 2, 5, 6, 7, 8. Under
   it, a BLUE agent `stilton_agent` (its name turns BLUE in line 2) shrinks into one GREEN tool chip
   `research_facts` (turns GREEN in line 3), which drops into a small GREY "orchestration" bin (S12's
   bin, redrawn). TRACKER CQ-Guild 2: a BLUE
   "orchestrator" beside the bin points at the chip.
3. CODE(cell-70: 4–5, 9–11) folded (8 rows): "Follow the assembly line strictly" and "(Make at most
   2 total review rounds.)" turn YELLOW; GREY tag "a rule in prose · no code enforces it". Bottom
   left, the GREEN excerpt chip `orchestrator, prompt, max_turns=12` (cell 71 · line 6).
4. TRACKER CQ-Guild 3. RECORDED(c75: 3–5, 7, 13) (header "Cheese Quiz · cell 75 · saved output",
   tag recorded · the staff's last saved run): three RED `ERROR:openai.agents:Error getting
   response` rows print one by one; the display line as a GREY label "a quiz widget", then the
   first question's text; GREY tag "a quiz anyway" under the box; the bin and the orchestrator become
   the Guild tree, small. Three RED "?" marks sit on its hops, then shift one hop over, with the GREY tag
   "which calls failed: not in the log"; then GOLD ticks on every hop. They fade with the lecture
   tag; ▶ your turn on a static GREY card "Cheese Quiz Guild: every cell, from Some Utils to
   Example 2", its last line GOLD "hosted web search · paid". Hold 2 s. Then (silent) the card and
   the tracker leave, the row comes back with the lecture tag, and a small Guild tree shrinks into
   slot 2 as an icon.
5. Slot 3 lights; the row folds up again. CODE(conditional_agent.py: 85, 89, 94, 99) folded at
   20 pt (header "5-custom-agent/conditional_agent.py · lines 85–99 (folded)"; the GREY subtitle
   "your copy: custom_agent/conditional_agent.py" under the panel, since it doesn't fit beside the
   header): line 85 PINK; a GREY chip "classifier: output_key="query_complexity" (line 171)"; lines
   89, 94, 99 YELLOW, each with a GREY label at its right: → simple handler, → complex handler,
   → clarification handler; a GREY chip "code only · running it: exercises.md". PONDER 6 s (the
   two chips fade while the card is up).
6. The card leaves. A GREY "if the classifier answers" + PINK `"Simple"` token; a copy visits line
   89 (RED cross on its label), line 94 (RED cross), and stops at line 99, whose label lights
   YELLOW. The capital S ringed RED against `"simple"` underlined RED in line 89. A GREEN fix chip
   `complexity.strip().lower()` · "or a structured output (exercises)"; the code-only chip returns.
   After the SAY (silent): the panel leaves, its PINK and YELLOW bars shrink into slot 3 as a small
   routing icon, and the row comes back with all three answers.
7. The lecture tag leaves. A GREY dashed chip "handoffs" enters at the right as it is named; the
   small GREY orchestration bin returns under the row, holding `research_facts` (labelled "agents as
   tools"), and the chip slides over it and drops in, with the dashed tag "concept · lecture only"
   and a GREY note "lecture 7 · slides". Everything fades: empty frame.
"""

import numpy as np
from common import (
    CLOUD,
    COST,
    DATA,
    ERR,
    INK,
    LOOKUP,
    NARRATION,
    TOOL,
    TURN,
    Prose,
    capture,
    concept_box,
    concept_tag,
    cost_tick,
    excerpt,
    excerpt_chip,
    grey_tag,
    lref,
    mini_bin,
    output_box,
    ponder_at,
    _with_header,
    ring,
    saved_run_tag,
    src_panel,
    tracker,
    turn_card,
    under,
    your_copy,
)
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    AnimationGroup,
    Arrow,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    Line,
    Rectangle,
    ReplacementTransform,
    RoundedRectangle,
    Square,
    Transform,
    VGroup,
    Write,
)
from pygments.token import Punctuation, String

from explainer import style as S
from explainer.devops import HOUSE_CODE_STYLE, MONO, box, chip, cross_mark, label, mono
from explainer.scene import VoiceScene

SAY = NARRATION["S13"]
assert len(SAY) == 8, len(SAY)

# ------------------------------------------------------------------ the real sources and the recording
AGENT1 = "llm-agent-google-adk/1-baseline/agent.py"
assert excerpt(AGENT1, 35, 35) == "root_agent = SequentialAgent(", excerpt(AGENT1, 35, 35)
ORDER = "[validator, processor, summarizer]"
assert ORDER in excerpt(AGENT1, 37, 37), excerpt(AGENT1, 37, 37)
STATIONS = ("validator", "processor", "summarizer")

CELL68 = "colab/cheese-quiz/cell-68.py"
AS_TOOL = ".as_tool("
AS_TOOL_LINES = (2, 5, 6, 7, 8)
assert all(AS_TOOL in excerpt(CELL68, n, n) for n in AS_TOOL_LINES)
assert excerpt(CELL68, 2, 2) == "stilton_tool = stilton_agent.as_tool("
assert excerpt(CELL68, 3, 3).strip().startswith('"research_facts",')
WRAP68 = {5: ['"Convert'], 6: ['"QA'], 7: ['"Format'], 8: ['"Format']}   # 12 rows at 20 pt

CELL70 = "colab/cheese-quiz/cell-70.py"
STRICT = "Follow the assembly line strictly"
ROUNDS = "(Make at most 2 total review rounds.)"
assert STRICT in excerpt(CELL70, 5, 5) and ROUNDS in excerpt(CELL70, 11, 11)
CELL71 = "colab/cheese-quiz/cell-71.py"
CAP_LINE = excerpt(CELL71, 6, 6)
CAP = "orchestrator, prompt, max_turns=12"
assert CAP_LINE.strip() == CAP, CAP_LINE

C75 = capture("expected/colab-cheese-quiz-c75-guild-star-wars.txt")
ERRS = C75.at((3, 5))
assert ERRS == ["ERROR:openai.agents:Error getting response"] * 3, ERRS
assert C75.line(7).startswith("[display: HTML quiz widget"), C75.line(7)   # shown as a GREY label
Q1 = C75.line(13)
assert Q1.strip().startswith('"text": "What type of cheese was served'), Q1

COND = "llm-agent-google-adk/5-custom-agent/conditional_agent.py"
assert excerpt(COND, 85, 85).strip() == 'complexity = ctx.session.state.get("query_complexity", "simple")'
assert excerpt(COND, 89, 89).strip() == 'if complexity == "simple":'
assert excerpt(COND, 94, 94).strip() == 'elif complexity == "complex":'
assert excerpt(COND, 99, 99).strip() == "else:  # ambiguous"
assert 'output_key="query_complexity"' in excerpt(COND, 171, 171)
HANDLERS = {89: "→ simple handler", 94: "→ complex handler", 99: "→ clarification handler"}
for _n, _h in ((90, "simple"), (95, "complex"), (100, "clarification")):    # the labels' source
    assert f"Routing to {_h} handler" in excerpt(COND, _n, _n)
FIX = "complexity.strip().lower()"

assert "Some Utils" in excerpt("colab/cheese-quiz/cell-62.py", 1, 1)
assert "Example 2" in excerpt("colab/cheese-quiz/cell-76.md", 1, 1)
TURN_ROWS = [Prose("Cheese Quiz Guild: every cell, from Some Utils to Example 2"),
             (Prose("hosted web search · paid"), COST)]
PONDER_Q = 'The classifier answers "Simple", with a capital S.\nWhich handler runs?'

STR_HEX = "#" + HOUSE_CODE_STYLE.style_for_token(String)["color"]
PUN_HEX = "#" + HOUSE_CODE_STYLE.style_for_token(Punctuation)["color"]

# ------------------------------------------------------------------ layout
Q_Y = 3.2                          # the question, in the top band
Q_X_TRACK = 1.1                    # ... between the tracker (right edge -1.48) and the lecture tag
ROW_Y = 2.15                       # the slot row
SLOT_W, SLOT_H, SLOT_GAP = 4.2, 0.95, 0.1
TOP = 2.75                         # content top while the row is folded away
STRIP_Y = -2.75                    # beats 2-3: agent, bin, orchestrator under the panel
BIN_X, ORCH_X = 1.75, 5.0
TOKEN_GAP = 0.25                   # beats 5-6: code end → "Simple" token → RED cross → label


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


def unwrap(scene, anims):
    """Put back in its place, member by member, the wrapper Group an AnimationGroup / LaggedStart
    added to the scene (as in S12)."""
    for a in anims:
        if not isinstance(a, AnimationGroup):
            continue
        g = a.group
        if g in scene.mobjects:
            i = scene.mobjects.index(g)
            scene.mobjects[i:i + 1] = list(g.submobjects)
        unwrap(scene, a.animations)


def pl(scene, *anims, **kw):
    """scene.play, then unwrap the AnimationGroup / LaggedStart wrappers."""
    scene.play(*anims, **kw)
    unwrap(scene, anims)


def explode(scene, group):
    """Take a VGroup's members onto the scene as separate mobjects (so each can morph or fade on
    its own). Returns the members."""
    mems = list(group.submobjects)
    scene.remove(group)
    for m in mems:
        group.remove(m)
    scene.add(*mems)
    return mems


def adopt(scene, parent, *mobs):
    """Top-level mobjects become members of `parent` (which is on the scene)."""
    scene.remove(*mobs)
    parent.add(*mobs)


def node(text, color, dashed=False, mono_=False, size=22, h=0.56, fill=0.14, pad=0.5):
    """A labelled box (a tree node or a station). .box .text"""
    t = mono(text, size, INK) if mono_ else label(text, size, INK)
    b = box(t.width + pad, h, color, dashed=dashed, fill_opacity=fill, radius=0.12)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def link(a, b, dashed=False, color=S.GREY):
    """A plain edge from a's bottom to b's top."""
    p, q = a.get_bottom() + DOWN * 0.04, b.get_top() + UP * 0.04
    if dashed:
        return DashedLine(p, q, dash_length=0.08).set_stroke(color, 2.5)
    return Line(p, q).set_stroke(color, 2.5)


def mixed_chip(parts, frame=S.GREY, size=22):
    """A chip of serif and mono pieces: parts = [(text, "mono"|"serif", colour), …]."""
    ts = VGroup(*[(mono if kind == "mono" else label)(s, size, col) for s, kind, col in parts])
    ts.arrange(RIGHT, buff=0.2)
    b = box(ts.width + 0.48, mono("|", size).height + 0.26, frame, fill_opacity=0.12, radius=0.14)
    ts.move_to(b)
    g = VGroup(b, ts)
    g.box, g.text = b, ts
    return g


def color_strings(panel, nums):
    """Workaround (as in S11): src_panel wraps before lexing, so a wrapped string literal comes out
    half-coloured. Colour each wrapped line's string from its opening quote to its closing quote."""
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


def span_band(span, color=TURN, opacity=0.28):
    """A highlighter band over a code span (no stroke, lower than a row pitch at 20 pt)."""
    return Rectangle(width=span.width + 0.1, height=0.3, stroke_width=0).set_fill(color, opacity) \
        .move_to(span)


def code_row(p, n, k=0):
    """The k-th code row of file line n in a src_panel."""
    return p.code.code_lines[p.rows_of(n)[k]]


# ------------------------------------------------------------------ pictures
def lecture_tree(cx=-3.4):
    """Slides 44–49 redrawn as a generic GREY dashed tree. .title .lead .plan .web .syn .rep and the
    edges .e_lp .e_pw .e_ws .e_sr"""
    title = VGroup(label("deep research", 22, S.GREY), concept_tag("concept · lecture example"))
    title.arrange(RIGHT, buff=0.25).move_to([cx, 2.3, 0])
    lead = node("lead agent", S.GREY, dashed=True).move_to([cx, 1.5, 0])
    plan = node("planner", S.GREY, dashed=True).move_to([cx, 0.55, 0])
    web = VGroup(*[node("web search", S.GREY, dashed=True, pad=0.3) for _ in range(3)]).arrange(RIGHT, buff=0.14)
    web.move_to([cx, -0.4, 0])
    syn = node("synthesis", S.GREY, dashed=True).move_to([cx, -1.35, 0])
    rep = node("report", S.GREY, dashed=True).move_to([cx, -2.3, 0])
    g = VGroup(title, lead, plan, web, syn, rep)
    g.title, g.lead, g.plan, g.web, g.syn, g.rep = title, lead, plan, web, syn, rep
    g.e_lp = link(lead, plan, dashed=True)
    g.e_pw = VGroup(*[link(plan, w, dashed=True) for w in web])
    g.e_ws = VGroup(*[link(w, syn, dashed=True) for w in web])
    g.e_sr = link(syn, rep, dashed=True)
    g.add(g.e_lp, g.e_pw, g.e_ws, g.e_sr)
    return g


DESCENDERS = set("gjpqy_,;")


def level_baselines(chips, names):
    """chip() centres each word in its box, so a word with a descender ("vegan", "send_email") sits
    higher than its neighbours; put every word of a row on the baseline of one without."""
    def offset(c, s):
        chars = [ch for ch in s if not ch.isspace()]
        for g, ch in zip(c.text.submobjects, chars):
            if ch not in DESCENDERS:
                return g.get_bottom()[1] - c.box.get_center()[1]
        return c.text.get_bottom()[1] - c.box.get_center()[1]
    plain = [offset(c, s) for c, s in zip(chips, names) if not set(s) & DESCENDERS]
    if not plain:
        return
    for c, s in zip(chips, names):
        c.text.shift(UP * (plain[0] - offset(c, s)))


def agent_tree(names, cx, orch_y, chip_y, title=None, title_y=None, mono_names=()):
    """A BLUE orchestrator over GREEN tool chips. .orch .chips .edges .title"""
    orch = node("orchestrator", CLOUD).move_to([cx, orch_y, 0])
    chips = VGroup(*[chip(n, DATA, size=22, font=MONO if n in mono_names else None)
                     for n in names]).arrange(RIGHT, buff=0.25)
    level_baselines(chips, names)
    chips.move_to([cx, chip_y, 0])
    edges = VGroup(*[link(orch, c) for c in chips])
    g = VGroup(orch, edges, chips)
    g.orch, g.chips, g.edges, g.title = orch, chips, edges, None
    if title:
        t = label(title, 22, S.GREY).move_to([cx, title_y, 0])
        g.add(t)
        g.title = t
    return g


def assembly_line():
    """Beat 1: three GREY stations on a PURPLE belt, PURPLE arrows between them, a YELLOW token.
    .stations .arrows .belt .token"""
    st = VGroup(*[node(n, S.GREY, mono_=True) for n in STATIONS]).arrange(RIGHT, buff=0.9)
    arrows = VGroup(*[Arrow(st[i].get_right(), st[i + 1].get_left(), buff=0.12, stroke_width=4,
                            color=TOOL, max_tip_length_to_length_ratio=0.35) for i in range(2)])
    belt = Line(st.get_corner(DOWN + LEFT) + DOWN * 0.28 + LEFT * 0.3,
                st.get_corner(DOWN + RIGHT) + DOWN * 0.28 + RIGHT * 0.3).set_stroke(TOOL, 4)
    token = Dot(belt.get_start(), radius=0.1, color=TURN)
    g = VGroup(st, arrows, belt, token)
    g.stations, g.arrows, g.belt, g.token = st, arrows, belt, token
    return g


def icon_line():
    """Slot 1's icon: three small GREY stations, PURPLE arrows, a PURPLE belt (text-free)."""
    sqs = VGroup(*[RoundedRectangle(width=0.3, height=0.3, corner_radius=0.05).set_stroke(S.GREY, 2.5)
                   .set_fill(S.GREY, 0.2) for _ in range(3)]).arrange(RIGHT, buff=0.24)
    arrows = VGroup(*[Line(sqs[i].get_right() + RIGHT * 0.03, sqs[i + 1].get_left() + LEFT * 0.03)
                      .set_stroke(TOOL, 3) for i in range(2)])
    belt = Line(sqs.get_corner(DOWN + LEFT) + DOWN * 0.12 + LEFT * 0.06,
                sqs.get_corner(DOWN + RIGHT) + DOWN * 0.12 + RIGHT * 0.06).set_stroke(TOOL, 3)
    g = VGroup(sqs, arrows, belt)
    g.sqs, g.arrows, g.belt = sqs, arrows, belt
    return g


def icon_tree():
    """Slot 2's icon: a BLUE orchestrator over four GREEN tool squares (text-free)."""
    top = RoundedRectangle(width=0.56, height=0.26, corner_radius=0.06).set_stroke(CLOUD, 2.5) \
        .set_fill(CLOUD, 0.3)
    sqs = VGroup(*[Square(0.2).set_stroke(DATA, 2.5).set_fill(DATA, 0.25) for _ in range(4)])
    sqs.arrange(RIGHT, buff=0.14).next_to(top, DOWN, buff=0.24)
    lines = VGroup(*[Line(top.get_bottom(), s.get_top()).set_stroke(S.GREY, 2) for s in sqs])
    g = VGroup(top, lines, sqs)
    g.head, g.lines, g.sqs = top, lines, sqs
    return g


def icon_route():
    """Slot 3's icon: a PINK label → a GREY decision diamond → three branch boxes (text-free;
    ≈ 1.1 wide, so it keeps clear of the slot's two-line label)."""
    pill = RoundedRectangle(width=0.3, height=0.18, corner_radius=0.07).set_stroke(LOOKUP, 2.5) \
        .set_fill(LOOKUP, 0.3)
    dia = Square(0.2).rotate(np.pi / 4).set_stroke(S.GREY, 2.5).set_fill(S.GREY, 0.15)
    dia.next_to(pill, RIGHT, buff=0.08)
    sqs = VGroup(*[RoundedRectangle(width=0.26, height=0.15, corner_radius=0.04).set_stroke(TURN, 2.5)
                   .set_fill(TURN, 0.2) for _ in range(3)]).arrange(DOWN, buff=0.07)
    sqs.next_to(dia, RIGHT, buff=0.18)
    stem = Line(pill.get_right(), dia.get_left()).set_stroke(S.GREY, 2)
    branches = VGroup(*[Line(dia.get_right(), s.get_left()).set_stroke(S.GREY, 2) for s in sqs])
    g = VGroup(pill, stem, dia, branches, sqs)
    g.pill, g.stem, g.dia, g.branches, g.sqs = pill, stem, dia, branches, sqs
    return g


def agent_glyph():
    """Beat 2: a whole agent (stilton_agent, cell 68 line 2): a BLUE card with its name and two GREY
    instruction lines."""
    name = mono("stilton_agent", 22, INK)
    bars = VGroup(Line(LEFT * 1.0, RIGHT * 1.0), Line(LEFT * 1.0, RIGHT * 0.4)).set_stroke(S.GREY, 3)
    bars.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    body = VGroup(name, bars).arrange(DOWN, buff=0.16)
    fr = box(body.width + 0.45, body.height + 0.32, CLOUD, fill_opacity=0.15, radius=0.12)
    body.move_to(fr)
    return VGroup(fr, body)


def make_slot(text, cx):
    """One answer slot: a GREY dashed frame, its label at the left, room for an icon at the right.
    .frame .label .hl (set when lit) .icon_right (the icon's right edge, 0.3 inside the frame)"""
    fr = box(SLOT_W, SLOT_H, S.GREY, dashed=True, radius=0.14).move_to([cx, ROW_Y, 0])
    lb = label(text, 22, INK)
    place(lb, left=fr.get_left()[0] + 0.25, cy=ROW_Y)
    g = VGroup(fr, lb)
    g.frame, g.label, g.hl = fr, lb, None
    g.icon_right = fr.get_right()[0] - 0.3
    return g


class ManyAgents(VoiceScene):
    def light_slot(self, sl, run_time=0.4, extra=()):
        """The slot lights: a solid YELLOW frame replaces the GREY dashed one (no dashes over it)."""
        hl = box(SLOT_W, SLOT_H, TURN, fill_opacity=0.06, stroke=3, radius=0.14).move_to(sl.frame)
        pl(self, Create(hl), sl.frame.animate.set_stroke(opacity=0), *extra, run_time=run_time)
        self.remove(hl)
        sl.add_to_back(hl)
        sl.hl = hl

    def close_slot(self, sl, pairs, icon, follow=(), fade=(), extra=(), run_time=0.9, instant=False):
        """The open slot's picture shrinks into its slot: each (source, icon part) pair morphs, the
        rest of `icon` grows in, each (text, icon part) in `follow` flies with its box into that part
        while it fades and shrinks, `fade` fades in place; the slot's frame turns solid GREY
        (instant=True: set at once, for a row that is off screen and fades in with `extra`)."""
        place(icon, right=sl.icon_right, cy=ROW_Y)
        targets = {id(b) for _, b in pairs}
        leaves = [m for m in icon.get_family() if not m.submobjects]
        rest = [m for m in leaves if id(m) not in targets]
        anims = [ReplacementTransform(a, b) for a, b in pairs]
        anims += [FadeIn(m, scale=1.6) for m in rest]
        anims += [FadeOut(m, target_position=b.get_center(), scale=0.2) for m, b in follow]
        anims += [FadeOut(m) for m in fade]
        if instant:
            sl.hl.set_stroke(S.GREY, 2.5).set_fill(S.GREY, 0.08)
            sl.frame.set_stroke(opacity=0)
        else:
            anims += [sl.hl.animate.set_stroke(S.GREY, 2.5).set_fill(S.GREY, 0.08),
                      sl.frame.animate.set_stroke(opacity=0)]
        pl(self, *anims, *extra, run_time=run_time)
        parts = [b for _, b in pairs] + rest
        self.remove(*parts)
        sl.add(*parts)

    def construct(self):
        # ============================================================ 0 · three trees (slides 44–49)
        lt = lecture_tree()
        guild = agent_tree(("facts", "write", "review", "vegan"), 3.45, 1.5, 0.45,
                           title="Cheese Quiz Guild", title_y=2.3)
        # the four chips are a selection: cell 70's orchestrator holds six tools (format_quiz_json
        # and ask_head_cheesemonger are not drawn), so the title line says so
        part = label("· 4 of its 6 tools", 20, S.GREY)
        VGroup(guild.title, part).arrange(RIGHT, buff=0.15).move_to([3.45, 2.3, 0])
        part.shift(UP * (guild.title[1].get_bottom()[1] - part[3].get_bottom()[1]))   # "h" and "f": one baseline
        guild.add(part)
        news = agent_tree(("researcher", "editor", "send_email"), 3.45, -1.25, -2.3,
                          title="Cheese Newsletter", title_y=-0.5, mono_names=("send_email",))
        lr = lref("44–49")
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(lr), FadeIn(lt.title, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("a tree of agents")
            self.play(Indicate(lt.title[0], color=INK, scale_factor=1.08), run_time=0.7)
            vo.wait_until("a lead agent")
            self.play(FadeIn(lt.lead, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("a planner")
            self.play(Create(lt.e_lp), FadeIn(lt.plan, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("parallel web searchers")
            pl(self, LaggedStart(*[AnimationGroup(Create(e), FadeIn(w, shift=DOWN * 0.1))
                                   for e, w in zip(lt.e_pw, lt.web)], lag_ratio=0.25), run_time=0.9)
            vo.wait_until("and a synthesis")
            pl(self, *[Create(e) for e in lt.e_ws], FadeIn(lt.syn, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("into a report")
            self.play(Create(lt.e_sr), FadeIn(lt.rep, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("The tutorial builds trees")
            self.play(FadeIn(guild.title), FadeIn(guild.orch, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("the Cheese Quiz Guild")
            pl(self, LaggedStart(*[AnimationGroup(Create(e), FadeIn(c, shift=DOWN * 0.1))
                                   for e, c in zip(guild.edges, guild.chips)],
                                 FadeIn(part, shift=LEFT * 0.1), lag_ratio=0.2), run_time=1.0)
            vo.wait_until("and the newsletter")
            self.play(FadeIn(news.title), FadeIn(news.orch, shift=DOWN * 0.1), run_time=0.4)
            pl(self, LaggedStart(*[AnimationGroup(Create(e), FadeIn(c, shift=DOWN * 0.1))
                                   for e, c in zip(news.edges, news.chips)], lag_ratio=0.2), run_time=0.8)

        # ============================================================ 1 · the question; slot 1: the code
        trees = [m for t in (lt, guild, news) for m in t.submobjects]
        q = label("Who plans the order?", 28, TURN).move_to([0, Q_Y, 0])
        slots = [make_slot("the code", -(SLOT_W + SLOT_GAP)), make_slot("the model", 0),
                 make_slot("Python reading\nthe model's label", SLOT_W + SLOT_GAP)]
        row = VGroup(*slots)
        p1 = src_panel(AGENT1, 35, 39, subtitle=your_copy(AGENT1))
        place(p1, top=1.5, cx=0)
        seq = p1.span(35, "SequentialAgent")
        u_order = span_band(p1.span(37, ORDER), opacity=0.25)
        al = assembly_line().move_to([0, -2.15, 0])
        with self.voiceover(SAY[1]) as vo:
            lr38 = lref("38")
            # the three trees stay up while the lecture's planner is named; they leave as the
            # question it raises writes in
            self.play(Indicate(lt.plan, color=TURN, scale_factor=1.1), run_time=0.8)
            vo.wait_until("raises the question")
            self.play(*[FadeOut(m) for m in trees], FadeOut(lr), FadeIn(lr38), Write(q), run_time=0.9)
            vo.wait_until("who plans the order")
            pl(self, LaggedStart(*[FadeIn(s, shift=DOWN * 0.15) for s in slots], lag_ratio=0.3),
               run_time=1.0)
            self.remove(*slots)
            self.add(row)
            vo.wait_until("First answer")
            self.light_slot(slots[0])
            self.play(FadeIn(p1, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("The sequential agent is an assembly line")
            self.play(seq.animate.set_color(TOOL), run_time=0.4)
            pl(self, LaggedStart(*[FadeIn(s, shift=UP * 0.1) for s in al.stations], lag_ratio=0.3),
               Create(al.belt), run_time=0.9)
            self.play(*[Create(a) for a in al.arrows], FadeIn(al.token), run_time=0.4)
            vo.wait_until("its order fixed in Python")
            self.play(FadeIn(u_order), run_time=0.4)
            for st in al.stations:
                self.play(al.token.animate.set_x(st.get_center()[0]), run_time=0.35)
                self.play(Indicate(st.box, color=TURN, scale_factor=1.06), run_time=0.3)
            self.play(al.token.animate.move_to(al.belt.get_end()), run_time=0.3)
        # (silent) slot 1 closes: the line shrinks into it, the station names riding their boxes
        ic1 = icon_line()
        st_parts = list(al.stations)
        for s in st_parts:
            explode(self, s)
        self.close_slot(slots[0],
                        [(s.box, ic1.sqs[i]) for i, s in enumerate(st_parts)]
                        + [(al.arrows[i], ic1.arrows[i]) for i in range(2)] + [(al.belt, ic1.belt)],
                        ic1, follow=[(s.text, ic1.sqs[i]) for i, s in enumerate(st_parts)]
                        + [(al.token, ic1.sqs[2])], fade=[p1, u_order])

        # ============================================================ 2 · slot 2: the model (agents as tools)
        tr = tracker("CQ-Guild", 1)
        p68 = src_panel(CELL68, 1, 8, size=20, wrap=WRAP68)
        _with_header(p68, "Cheese Quiz · cell 68 · lines 1–8")
        place(p68, top=TOP, cx=0)
        spans = [p68.span(n, AS_TOOL) for n in AS_TOOL_LINES]
        u_tools = [span_band(s) for s in spans]
        s_agent = p68.span(2, "stilton_agent")
        s_name = p68.span(3, '"research_facts"')
        ag = agent_glyph().move_to([-4.3, STRIP_Y, 0])
        rf = chip("research_facts", DATA, size=22, font=MONO).move_to(ag)
        bin_ = mini_bin("orchestration", w=3.4, h=0.85).move_to([BIN_X, STRIP_Y - 0.12, 0])
        orch = node("orchestrator", CLOUD).move_to([ORCH_X, STRIP_Y, 0])
        in_bin = np.array([BIN_X, bin_.shape.get_bottom()[1] + 0.34, 0])
        with self.voiceover(SAY[2]) as vo:
            self.light_slot(slots[1])                  # lit while "Second answer: the model" is said
            vo.wait_until("In the Guild")
            self.play(FadeOut(row, shift=UP * 0.3), q.animate.move_to([Q_X_TRACK, Q_Y, 0]),
                      FadeIn(tr, shift=DOWN * 0.25), run_time=0.5)
            self.play(FadeIn(p68, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("each specialist becomes a tool")
            pl(self, LaggedStart(*[FadeIn(u) for u in u_tools], lag_ratio=0.25), run_time=1.1)
            vo.wait_until("a whole agent")
            self.play(FadeIn(ag, shift=UP * 0.1), s_agent.animate.set_color(CLOUD), FadeIn(bin_), run_time=0.5)
            vo.wait_until("behind one function")
            self.play(ReplacementTransform(ag, rf), s_name.animate.set_color(DATA), run_time=0.6)
            self.play(rf.animate.move_to(in_bin), run_time=0.6)
            vo.wait_until("An orchestrator decides")
            ptr = Arrow(orch.get_left(), rf.get_right(), buff=0.08, stroke_width=4, color=CLOUD,
                        max_tip_length_to_length_ratio=0.4)
            pl(self, tr.goto(2), FadeIn(orch, shift=LEFT * 0.15), run_time=0.5)
            self.play(Create(ptr), run_time=0.4)
            self.play(Indicate(rf, color=CLOUD, scale_factor=1.06), run_time=0.6)

        # ============================================================ 3 · the orchestrator's rule in prose
        p70 = src_panel(CELL70, [(4, 5), (9, 11)], wrap=True)
        color_strings(p70, [9, 10])
        _with_header(p70, "Cheese Quiz · cell 70 · lines 4–11 (folded)")
        place(p70, top=TOP, cx=0)
        s_strict = p70.span(5, STRICT)
        s_rounds = p70.span(11, ROUNDS)
        u_strict = under(s_strict, TURN, stroke=3)
        u_rounds = under(s_rounds, TURN, stroke=3)
        prose = grey_tag("a rule in prose · no code enforces it")
        place(prose, right=p70.get_right()[0] - 0.1, top=p70.get_bottom()[1] - 0.15)
        c71 = excerpt_chip(CAP, "Cheese Quiz · cell 71 · line 6 (excerpt)", line=CAP_LINE, frame=DATA)
        place(c71, left=-6.4, cy=STRIP_Y + 0.2)
        u_cap = under(c71.chip.text[len("orchestrator,prompt,"):], TURN, stroke=3)
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(p68), *[FadeOut(u) for u in u_tools], FadeIn(p70, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("follow the assembly line strictly")
            self.play(s_strict.animate.set_color(TURN), Create(u_strict), run_time=0.5)
            vo.wait_until("at most 2 review rounds")
            self.play(s_rounds.animate.set_color(TURN), Create(u_rounds), run_time=0.5)
            vo.wait_until("That's a rule in prose")
            self.play(FadeIn(prose, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("no code enforces it")
            self.play(Indicate(prose, color=INK, scale_factor=1.05), run_time=0.6)
            vo.wait_until("except a cap of 12 turns")
            self.play(FadeIn(c71, shift=RIGHT * 0.15), run_time=0.5)
            self.play(Create(u_cap), run_time=0.4)

        # ============================================================ 4 · the saved run; ▶
        ob = output_box([(e, ERR) for e in ERRS] + ["x", Q1], header="Cheese Quiz · cell 75 · saved output",
                        size=20)
        place(ob, top=TOP, cx=0)
        ob_rows = ob.rows
        ob.remove(ob_rows)
        widget = label("a quiz widget", 22, S.GREY)
        place(widget, left=ob_rows[4].get_left()[0],
              cy=(ob_rows[2].get_center()[1] + ob_rows[4].get_center()[1]) / 2)
        anyway = grey_tag("a quiz anyway")
        place(anyway, right=ob.frame.get_right()[0] - 0.2, top=ob.frame.get_bottom()[1] - 0.1)
        srt = saved_run_tag()
        place(srt, right=ob.frame.get_right()[0], cy=ob.header.get_center()[1])
        small = agent_tree(("facts", "write", "review", "vegan"), -3.3, -1.05, -2.4)
        # a mark per hop sits on the edge a little below its middle, where the four edges have
        # spread apart; a dark disc cuts the edge under each "?" so the mark reads cleanly
        hops = [e.point_from_proportion(0.58) for e in small.edges]
        qs = [VGroup(Dot(radius=0.2, color=S.BG), label("?", 30, ERR, weight="BOLD")) for _ in range(3)]
        for k, m in enumerate(qs):
            m.move_to(hops[k])
        failed = grey_tag("which calls failed: not in the log")
        place(failed, left=0.4, cy=-1.72)
        ticks = [VGroup(Dot(radius=0.11, color=S.BG), cost_tick()).move_to(h) for h in hops]   # the edge stops under the coin
        card = turn_card(TURN_ROWS).move_to([0, -0.4, 0])
        with self.voiceover(SAY[4]) as vo:
            pl(self, tr.goto(3), FadeOut(p70), FadeOut(u_strict), FadeOut(u_rounds), FadeOut(prose),
               FadeOut(c71), FadeOut(u_cap), FadeOut(ptr), FadeIn(ob), FadeIn(srt), run_time=0.7)
            vo.wait_until("logged three errors")
            pl(self, LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in ob_rows[:3]], lag_ratio=0.45),
               run_time=1.3)
            vo.wait_until("and still produced a quiz")
            self.play(FadeIn(widget), FadeIn(ob_rows[4], shift=RIGHT * 0.1), run_time=0.5)
            self.play(FadeIn(anyway, shift=LEFT * 0.1), run_time=0.4)
            # the bin and its orchestrator become the Guild tree, small: the run that went on anyway
            self.play(orch.animate.move_to(small.orch), ReplacementTransform(rf, small.chips[0]),
                      FadeOut(bin_), run_time=0.7)
            pl(self, *[Create(e) for e in small.edges], *[FadeIn(c) for c in small.chips[1:]], run_time=0.5)
            vo.wait_until("the log doesn't say")
            pl(self, LaggedStart(*[FadeIn(m, scale=1.4) for m in qs], lag_ratio=0.3),
               FadeIn(failed, shift=LEFT * 0.1), run_time=0.7)
            vo.wait_until("which calls failed")
            self.play(*[m.animate.move_to(hops[k + 1]) for k, m in enumerate(qs)], run_time=0.6)
            vo.wait_until("Every hop adds cost")
            pl(self, *[FadeOut(m) for m in qs],
               LaggedStart(*[FadeIn(t, scale=1.5) for t in ticks], lag_ratio=0.2), run_time=0.8)
            vo.wait_until("and a way to fail")
            pl(self, *[Indicate(e, color=ERR, scale_factor=1.0) for e in small.edges], run_time=0.6)
            vo.wait_until("pause, and run the Guild")
            gone = [ob, srt, widget, anyway, failed, orch, *ob_rows[:3], ob_rows[4], *small.edges,
                    *small.chips, *ticks, lr38]
            self.play(*[FadeOut(m) for m in gone], run_time=0.5)
            self.play(FadeIn(card, shift=UP * 0.1), run_time=0.5)
        self.wait(2)
        # (silent) slot 2 closes: the row comes back and a small Guild tree shrinks into it
        mini = agent_tree(("facts", "write", "review", "vegan"), 0, 0.3, -0.75)
        lr38 = lref("38")
        self.play(FadeOut(card), FadeOut(tr, shift=UP * 0.25), q.animate.move_to([0, Q_Y, 0]),
                  FadeIn(row, shift=DOWN * 0.3), FadeIn(lr38), run_time=0.6)
        self.play(FadeIn(mini, shift=UP * 0.1), run_time=0.4)      # after the card: no cross-fade
        ic2 = icon_tree()
        explode(self, mini)
        orch_m = mini.orch
        explode(self, orch_m)
        chips_m = explode(self, mini.chips)
        edges_m = explode(self, mini.edges)
        for c in chips_m:
            explode(self, c)
        self.close_slot(slots[1],
                        [(orch_m.box, ic2.head)] + [(c.box, ic2.sqs[i]) for i, c in enumerate(chips_m)]
                        + [(e, ic2.lines[i]) for i, e in enumerate(edges_m)],
                        ic2, follow=[(orch_m.text, ic2.head)] + [(c.text, ic2.sqs[i]) for i, c in enumerate(chips_m)])

        # ============================================================ 5 · slot 3: Python reading the label; PONDER
        p3 = src_panel(COND, [85, 89, 94, 99], size=20)
        place(p3, top=TOP, cx=0)
        sub3 = label(your_copy(COND), 20, S.GREY)
        place(sub3, left=p3.code.get_left()[0] + 0.1, top=p3.get_bottom()[1] - 0.1)
        bar85 = p3.bar(85, LOOKUP, 0.22)
        bars = {n: p3.bar(n, TURN, 0.16) for n in (89, 94, 99)}
        # one lane right of the longest branch row (line 94) holds the visiting "Simple" token, then
        # the RED cross, then the handler label, so the token never touches the code
        tok = chip('"Simple"', LOOKUP, size=22, font=MONO)
        code_end = max(code_row(p3, n).get_right()[0] for n in (89, 94, 99))
        token_x = code_end + TOKEN_GAP + tok.width / 2
        cross_x = token_x + tok.width / 2 + TOKEN_GAP
        labs = {}
        for n, h in HANDLERS.items():
            labs[n] = label(h, 22, S.GREY)
            place(labs[n], left=cross_x + 0.33, cy=code_row(p3, n).get_center()[1])
        clf = mixed_chip([("classifier:", "serif", INK), ('output_key="query_complexity"', "mono", INK),
                          ("(line 171)", "serif", S.GREY)])
        clf.text[1][len("output_key="):].set_color(LOOKUP)
        place(clf, left=p3.code.get_left()[0], cy=-1.45)
        only = mixed_chip([("code only · running it:", "serif", INK), ("exercises.md", "mono", INK)])
        place(only, left=p3.code.get_left()[0], cy=-2.2)
        with self.voiceover(SAY[5]) as vo:
            self.light_slot(slots[2])
            vo.wait_until("In this custom agent")
            self.play(FadeOut(row, shift=UP * 0.3), run_time=0.4)
            self.play(FadeIn(p3, shift=UP * 0.15), FadeIn(sub3), run_time=0.5)
            vo.wait_until("a classifier writes one word")
            self.play(FadeIn(bar85), FadeIn(clf, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("and plain if statements")
            pl(self, LaggedStart(*[AnimationGroup(FadeIn(bars[n]), FadeIn(labs[n], shift=LEFT * 0.1))
                                   for n in (89, 94, 99)], lag_ratio=0.35), run_time=1.1)
            self.play(FadeIn(only, shift=UP * 0.1), run_time=0.4)
        pcard = ponder_at(self, PONDER_Q, 6, hide=(clf, only))

        # ============================================================ 6 · the answer: the else branch
        ifans = label("if the classifier answers", 22, S.GREY)
        VGroup(ifans, tok).arrange(RIGHT, buff=0.3)
        place(VGroup(ifans, tok), left=p3.code.get_left()[0], cy=-1.45)
        ifans.align_to(tok.text, DOWN)
        mover = tok.copy()
        row_y = {n: code_row(p3, n).get_center()[1] for n in (89, 94, 99)}
        crosses = {n: cross_mark(0.26, ERR).move_to([cross_x, row_y[n], 0]) for n in (89, 94)}
        s_ring = ring(tok.text[1], ERR, buff=0.06)
        u_simple = under(p3.span(89, '"simple"'), ERR, stroke=3)
        fx = chip(FIX, DATA, size=22, font=MONO)
        fx_note = label("or a structured output (exercises)", 22, S.GREY)
        fix_row = VGroup(fx, fx_note).arrange(RIGHT, buff=0.3)
        place(fix_row, left=p3.code.get_left()[0], cy=-2.3)
        fx_note.align_to(fx.text, DOWN)
        place(only, left=p3.code.get_left()[0], cy=-3.1)
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(pcard), FadeIn(ifans), FadeIn(tok, shift=UP * 0.1), run_time=0.4)
            self.play(mover.animate.move_to([token_x, row_y[89], 0]), run_time=0.35)
            self.play(Create(crosses[89]), labs[89].animate.set_opacity(0.45), run_time=0.25)
            self.play(mover.animate.move_to([token_x, row_y[94], 0]), run_time=0.3)
            self.play(Create(crosses[94]), labs[94].animate.set_opacity(0.45), run_time=0.25)
            self.play(mover.animate.move_to([token_x, row_y[99], 0]), run_time=0.3)
            self.play(labs[99].animate.set_color(TURN), bars[99].animate.set_fill(TURN, 0.3), run_time=0.3)
            vo.wait_until("The comparison is exact")
            self.play(Create(s_ring), Create(u_simple), run_time=0.5)
            vo.wait_until("lowercase the label first")
            self.play(FadeIn(fx, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("or ask for structured output")
            self.play(FadeIn(fx_note, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("The exercises try both")
            self.play(FadeIn(only, shift=UP * 0.1), run_time=0.4)
            self.play(Indicate(only.text[1], color=TURN, scale_factor=1.08), run_time=0.6)
        # (silent) slot 3 closes: while the panel fades, the PINK and YELLOW bars shrink in their rows
        # to the icon's pill and boxes (at the icon's x), then rise into the slot as the row comes back
        # (so no bar sweeps across the slot's label)
        ic3 = icon_route()
        place(ic3, right=slots[2].icon_right, cy=ROW_Y)
        pairs3 = [(bar85, ic3.pill)] + [(bars[n], ic3.sqs[i]) for i, n in enumerate((89, 94, 99))]
        fade3 = [p3, sub3, *labs.values(), *crosses.values(), mover, tok, ifans, s_ring, u_simple,
                 fx, fx_note, only]
        self.play(*[FadeOut(m) for m in fade3],
                  *[Transform(b, part.copy().move_to([part.get_x(), b.get_y(), 0])) for b, part in pairs3],
                  run_time=0.6)
        self.close_slot(slots[2], pairs3, ic3, extra=[FadeIn(row, shift=DOWN * 0.3)], instant=True)

        # ============================================================ 7 · handoffs, lecture only
        bin7 = mini_bin("orchestration", w=3.6, h=1.75).move_to([0, -1.1, 0])
        rf7 = chip("research_facts", DATA, size=22, font=MONO)
        rf7.move_to([0, bin7.shape.get_bottom()[1] + 0.36, 0])
        aat = label("agents as tools", 22, S.GREY)
        place(aat, right=bin7.shape.get_left()[0] - 0.35, cy=rf7.get_center()[1])
        ho = concept_box("handoffs", size=22)
        ho_y = rf7.get_center()[1] + 0.72
        above = bin7.shape.get_top()[1] + ho.height / 2 + 0.2      # it slides in above the bin, then drops in
        ho.move_to([6.6 - ho.width / 2 - 0.1, above, 0])
        ctag = concept_tag("concept · lecture only")
        place(ctag, left=bin7.shape.get_right()[0] + 0.35, cy=ho_y)
        l7 = label("lecture 7 · slides", 22, S.GREY)
        place(l7, left=ctag.get_left()[0] + 0.1, top=ctag.get_bottom()[1] - 0.15)
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(lr38), run_time=0.4)
            vo.wait_until("lists handoffs")
            self.play(FadeIn(ho, shift=LEFT * 0.2), run_time=0.4)
            vo.wait_until("among the orchestration tools")
            self.play(FadeIn(bin7), FadeIn(rf7), run_time=0.5)
            self.play(ho.animate.move_to([0, above, 0]), run_time=0.6)
            self.play(ho.animate.move_to([0, ho_y, 0]), run_time=0.4)
            self.play(FadeIn(ctag, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("These tutorials use agents as tools")
            self.play(FadeIn(aat, shift=RIGHT * 0.1), Indicate(rf7, color=DATA, scale_factor=1.08), run_time=0.6)
            vo.wait_until("lecture 7 sketches handoffs")
            self.play(FadeIn(l7, shift=UP * 0.1), run_time=0.4)
        self.play(*[FadeOut(m) for m in (q, row, bin7, rf7, aat, ho, ctag, l7)], run_time=0.8)
