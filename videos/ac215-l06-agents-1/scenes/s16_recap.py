"""S16 · Tear down, recap, and what's next (the end of part 2: ADK README "Running Agents" step 1 with
extras, the Colab runtimes and the three keys; the lecture's anatomy and formula; five test-yourself
questions). Lecture: 41 (and 32–33).

Beats (script.md "## S16", one voiceover block each):
0. TRACKER RunAg 1 (" · extra" from the git status on). The ADK laptop terminal as the 3-row strip,
   the restarted server running (its `uv run adk web` row, then adk-laptop/29 line 40 wrapped, as S10
   left it). Ctrl+C -> 29 lines 364, 367–369 (the 79-column box rows cut with …; "^C" flashes while
   the server's log rows fade in place, so the box doesn't slide them up over the title bar; the
   box prints right after). The strip grows to 12 rows keeping the box (it scrolls away under the
   output) and types the extra `git status --short; git status --short --ignored | grep '^!!'`
   (folded under the prompt, tag extra) -> 39 lines 2, …, 16–21, …, 24. The renamed folders' rows
   flash YELLOW; `?? .python-version` GREEN + GREEN tag "your pin"; `!! .env`, `!! .venv/`, the '…'
   (two __pycache__/ rows) and `!! uv.lock` GREY with a GREY bracket and the tag "ignored".
1. The terminal keeps its last 7 rows. Above it: the excerpt chip `baseline/.adk/session.db` (header
   "uv run adk web · log (excerpt)", 29 lines 41–42 joined), its ".adk/" RED; the RED-outlined
   (dashed) ghost folder `baseline/.adk/` grows out of it with the RED tag "sessions · not in
   .gitignore"; in the terminal `baseline/` gets a RED box. A GREY chip "add .adk/ to your ignore
   file (exercises)" under it; top right a GREY two-row chip ".venv · 1.6 GB · delete when done /
   on a Linux PC: about 3 GB more (CUDA)" (adk-laptop/14 line 12; S09's CUDA note) while the
   `!! .venv/` row flashes.
2. The terminal, the tracker and the chips leave. A BLUE Colab frame "Colab · every notebook" (tag
   illustration): Runtime › Disconnect and delete runtime (lit YELLOW), ticked three times: Cheese
   Quiz, Travel Planner, Newsletter. Three GOLD keys: "service account · in secrets/ beside llm-rag"
   ("beside" underlined YELLOW), "AI Studio key · root .env", "OpenAI key · Colab Secrets only"; the
   GREY note "delete or cap when the course ends" under the last two as said. A GREY chip "llm-rag:
   stopped in part 1"; a GOLD card "tried 6-rag/1-vertex-rag-engine? its corpus is billable ·
   exercises.md deletes it".
3. LECTURE 41. V1's anatomy full size (Anatomy(box_w=11.8, block_h=1.75, ends=False)); each block
   lights YELLOW and fills with GREY code chips as the SAY names it: LLM core
   `gemini-3.1-flash-lite`, `gpt-4o`; Instructions `instruction=`, `output_type`; Tools
   `FunctionDeclaration` (by hand), `@function_tool` (decorated), `MCPToolset` (over MCP); Memory
   "message history", "session state · one session".
4. Dynamic Control lights, then fills PURPLE with `Runner`, `max_turns=12`; the TEAL chip "llm-rag:
   two calls by hand" joins them. LECTURE 32–33: the formula writes in under the anatomy (our words)
   "agent ≈ LLM + reasoning + instructions + tools", term by term as said, each term lighting its
   block (LLM + reasoning: the core, SLIDES.md's terms table; instructions; tools); two GREEN chips
   append: "+ a loop the framework runs" (the PURPLE bar flashes) and "+ checks your code enforces".
5. The lecture tag and the anatomy leave. "Test yourself" (YELLOW underline); Q1 writes in, its key
   words YELLOW as said; Q2 writes in below as Q1 turns small and GREY (glyph for glyph; words that
   move up a row on the re-wrap dip under it on an arc, so no glyphs cross).
6. Q3, Q4 the same way.
7. Q5 the same way; then it turns small too, the five questions stay at the top; the footer cards
   "Answers: exercises.md · study guide §8" and "Study guide + every command:
   github.com/JunyiZhou-Conny/MLOps_Learning · guides/L06-agents-1.md" ("MLOps_Learning" underlined
   YELLOW); a GREY dashed chip "Lecture 7 · Agents II: the harness" top right. Everything fades: an
   empty frame (the end of part 2).

Deviations from SHOW (see the scene report): the strip opens on the server's `uv run adk web` row and
its last log line from S10 (29 line 40), so the Ctrl+C has something to stop; the 12-row terminal
keeps the shutdown box until the git status output scrolls it away. The git status shows a second
'…' for capture lines 22–23 (script.md's TERM lists 2, …, 16–21, 24), so the ignored list doesn't
look complete. The Tools block shows `@function_tool`
in place of `.as_tool`: the SAY names "by hand, decorated, or over MCP" and `.as_tool` does not fit
beside the other three. The "delete or cap" note sits under the AI Studio and OpenAI keys only (the
SAY: "the other two keys"); the service account key's line says where it stays. The .venv chip adds
"delete when done" (the SAY's instruction, readable when paused) and a row with S09's Linux CUDA
note (1.6 GB is the CPU-only capture). The GOLD 6-rag chip is a two-row
card (one row would be 11.5 wide). "Test yourself" is a title, as in L05; a question that turns
small re-wraps to one row (Q5: two), so all five and the footer fit. The Answers card also names the
study guide's §8, which holds the same answers.
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    AnimationGroup,
    Create,
    DashedVMobject,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    Line,
    Rectangle,
    Transform,
    TransformFromCopy,
    VGroup,
    VMobject,
    Write,
)

from common import (
    COST,
    CTR,
    DATA,
    ERR,
    INK,
    KEY,
    MODEL_CQ,
    MODEL_RAG,
    NARRATION,
    OUTPUT,
    P_ADK,
    TOOL,
    TURN,
    Anatomy,
    _keep,
    beside,
    capture,
    caption_extra,
    col_box,
    colab_frame,
    concept_box,
    excerpt_chip,
    extra_tag,
    key_glyph,
    lref,
    lref_swap,
    menu_path,
    pin,
    resize,
    term,
    tracker,
    type_cmd,
    under,
)
from explainer import style as S
from explainer.devops import MONO, box, check_mark, chip, folder_glyph, label, mono, mono_line, step_badge, \
    substring, tag
from explainer.scene import VoiceScene

SAY = NARRATION["S16"]

# ------------------------------------------------------------------ the real captures
WEB2 = capture("29", "adk-laptop")                 # the restarted `uv run adk web` (after S10's rename)
assert WEB2.cmd == "uv run adk web", WEB2.cmd
RUNNING = WEB2.line(40)                            # the last log row S10 showed
assert RUNNING.endswith('"GET /dev/apps/baseline/build_graph HTTP/1.1" 200 OK'), RUNNING
STOP = WEB2.at(364, (367, 369))
assert STOP[0].startswith("^C") and "ADK Web Server shutting down..." in STOP[2], STOP
SESS_LOG = WEB2.join(41, 42)                       # where ADK keeps the sessions
SESS_DB = "baseline/.adk/session.db"
assert "Creating local session service at" in SESS_LOG and SESS_LOG.endswith(
    "/llm-agent-google-adk/" + SESS_DB), SESS_LOG

GIT = capture("39", "adk-laptop")                  # extra: git status after the rename
assert GIT.cmd == "git status --short; git status --short --ignored | grep '^!!'", GIT.cmd
GIT_OUT = GIT.at(2, "…", (16, 21), "…", 24)     # the second '…': the two __pycache__/ rows (22-23)
assert GIT_OUT[0] == " D 1-baseline/.env.example", GIT_OUT[0]
assert GIT_OUT[2:] == ["?? .python-version", "?? baseline/", "?? custom_agent/", "?? mcp_tools/",
                       "!! .env", "!! .venv/", "…", "!! uv.lock"], GIT_OUT
VENV_SIZE = capture("14", "adk-laptop").line(12)   # du: the virtual environment's size
assert VENV_SIZE.split() == ["1.6G", ".venv"], VENV_SIZE

GUIDE_REPO = "github.com/JunyiZhou-Conny/MLOps_Learning"
GUIDE_PATH = "guides/L06-agents-1.md"

# the anatomy's chips (BRIEF.md S16; the tutorial's own names)
FILL = {
    "core": [f"`{MODEL_RAG}`", f"`{MODEL_CQ}`"],
    "instructions": ["`instruction=`", "`output_type`"],
    "tools": ["`FunctionDeclaration`", "`@function_tool`", "`MCPToolset`"],
    "memory": ["message history", "session state · one session"],
}
FORMULA = "agent ≈ LLM + reasoning + instructions + tools"

QUESTIONS = [   # (text, code spans) — script.md S16
    ("In function calling, who runs the function, and what travels back to the model in call 2?", ()),
    ('What does mode="any" change, and why only on call 1?', ('mode="any"',)),
    ("What ends an agent loop, what cap do frameworks add, and which lecture block is that?", ()),
    ("How does TripSummarizer get the travel plan without a message from TravelPlanner?",
     ("TripSummarizer", "TravelPlanner")),
    ("In the last two notebooks, what decides that a run succeeded, and why not the model's final text?",
     ()),
]
Q_BIG, Q_SMALL = 26, 22         # the current question, the earlier ones
Q_X, Q_W = -5.75, 12.1          # left edge of the question text, wrap width
Q_TOP = 2.55
NBSP = " "
NOBREAK = ("who runs the function", "what travels back", "call 2?", "only on call 1?", "ends an agent loop",
           "lecture block", "without a message", "decides that a run succeeded",
           "not the model's final text?")   # highlighted as one span


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


def preload(t, cmd: str, rows) -> None:
    """The state the scene opens on: a typed command row and output rows, placed without animation
    (they appear with the terminal)."""
    ln = mono_line(f"{t.prompt} {cmd}", t.size, INK, t2c=t._prompt_colors(t.prompt))
    t._place(ln, len(t.lines))
    t.lines.add(ln)
    for s in rows:
        ln = mono_line(s, t.size, OUTPUT)
        t._place(ln, len(t.lines))
        t.lines.add(ln)


def wrap_rows(s: str, n: int) -> list:
    """A long output line folded at the terminal's edge (Terminal.print(wrap=True))."""
    return [s[i:i + n] for i in range(0, len(s), n)]


def mixed(parts, size: float = 20, color: str = INK):
    """One row of text mixing mono ("`code`") and serif pieces, as ONE Text (one baseline); a serif
    piece that starts with punctuation joins the one before it without a space ("`llm-rag`",
    ": stopped"). Ligatures off, so submobject i is character i (spaces included): see span()."""
    s, mono_spans = "", []
    for p in parts:
        code = p.startswith("`") and p.endswith("`")
        txt = p[1:-1] if code else p
        if s and (code or txt[0] not in ":?,."):      # ".env" is code, not punctuation
            s += " "
        if code:
            mono_spans.append((len(s), len(s) + len(txt)))
        s += txt
    t2f = {f"[{a}:{b}]": MONO for a, b in mono_spans}
    t = S.text(s, size, color, t2f=t2f, disable_ligatures=True)
    assert len(t.submobjects) == len(s), (s, len(t.submobjects))
    t.s = s
    return t


def span(t, sub: str) -> VGroup:
    """The glyphs of `sub` in a mixed() row."""
    i = t.s.index(sub)
    return VGroup(*t.submobjects[i:i + len(sub)])


def mixed_chip(rows, color: str = S.GREY, size: float = 20) -> VGroup:
    """A chip (one row, or several rows of mixed pieces) in `color`, opaque dark fill. .frame .rows"""
    rows = [rows] if isinstance(rows[0], str) else rows
    body = VGroup(*[mixed(r, size) for r in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    h = body.height + 0.26
    fr = box(body.width + 0.48, h, color, fill=S.BG, fill_opacity=0.92, radius=min(0.2, h / 2.6))
    tint = box(body.width + 0.48, h, color, fill_opacity=0.14, stroke=0, radius=min(0.2, h / 2.6))
    body.move_to(fr)
    g = VGroup(fr, tint, body)
    g.frame, g.rows = fr, body
    return _keep(g)


def rbracket(rows, x: float, color: str = S.GREY) -> VMobject:
    """A ']' bracket at x spanning the terminal rows."""
    top = max(r.strut.get_top()[1] for r in rows) - 0.02
    bot = min(r.strut.get_bottom()[1] for r in rows) + 0.02
    ln = VMobject(stroke_color=color, stroke_width=3)
    ln.set_points_as_corners([[x - 0.1, top, 0], [x, top, 0], [x, bot, 0], [x - 0.1, bot, 0]])
    return ln


def ghost_folder(name: str, color: str = ERR) -> VGroup:
    """A dashed folder that is not ignored (it exists, but nothing protects it). .glyph .text"""
    g = folder_glyph(0.36, color)
    dashed = VGroup(*[DashedVMobject(m, num_dashes=16, dashed_ratio=0.55).set_stroke(color, 2.5) for m in g])
    t = mono(name, 22, INK).next_to(dashed, RIGHT, buff=0.16)
    out = VGroup(dashed, t)
    out.glyph, out.text = dashed, t
    return _keep(out)


def key_column(name: str, where, x: float, y: float) -> VGroup:
    """A GOLD key, its name and where it lives (its content is never drawn). .key .name .where"""
    k = key_glyph(0.5)
    n = label(name, 24, INK)
    w = mixed(where, 22, S.GREY)
    col = VGroup(k, n, w).arrange(DOWN, buff=0.16)
    col.move_to([x, y, 0]).align_to([0, y, 0], UP)
    col.key, col.name, col.where = k, n, w
    return col


def end_note(col) -> VGroup:
    """The GREY 'delete or cap when the course ends' note under a key column."""
    n = VGroup(label("delete or cap", 20, S.GREY), label("when the course ends", 20, S.GREY))
    n.arrange(DOWN, buff=0.06).next_to(col, DOWN, buff=0.22)
    return n


def tick_row(names) -> VGroup:
    items = [VGroup(check_mark(0.26, DATA), label(n, 24, INK)).arrange(RIGHT, buff=0.14) for n in names]
    row = VGroup(*items).arrange(RIGHT, buff=0.75)
    for it in items[1:]:         # one baseline: every name has an ascender ("Quiz" has a tail)
        it[1].align_to(items[0][1], UP)
    return row


# ------------------------------------------------------------------ beats 5–7: question text (L05's helpers)
def text_line(s: str, size: float, color: str, code=()) -> VGroup:
    """One line of house-font text whose code spans use the code font, with a FIXED vertical extent
    (a leading '|' dropped after layout). Ligatures off, so glyph i is non-space character i.
    .glyphs .strut"""
    spans: list[tuple[int, int]] = []
    for c in sorted(code, key=len, reverse=True):
        i = s.find(c)
        while i >= 0:
            if all(i + len(c) <= a or i >= b for a, b in spans):
                spans.append((i, i + len(c)))
            i = s.find(c, i + 1)
    t2f = {f"[{a + 1}:{b + 1}]": MONO for a, b in spans}
    t = S.text("|" + s, size, color, t2f=t2f, disable_ligatures=True)
    pipe = t.submobjects[0]
    strut = Rectangle(width=max(0.01, t.width), height=pipe.height, stroke_width=0, fill_opacity=0)
    strut.move_to(pipe.get_center()).align_to(t, LEFT)
    subs = t.submobjects[1:]
    assert len(subs) == len(s), (s, len(subs))       # ligatures off: one submobject per character
    gl = VGroup(*[m for ch, m in zip(s, subs) if not ch.isspace()])
    strut.stretch_to_fit_width(max(0.01, gl.width)).align_to(gl, LEFT)
    g = VGroup(strut, *gl.submobjects)
    g.glyphs, g.strut = VGroup(*gl.submobjects), strut
    return g


_WIDTHS: dict = {}


def _line_width(s: str, size: float, code: tuple) -> float:
    key = (s, size, code)
    if key not in _WIDTHS:
        _WIDTHS[key] = text_line(s, size, INK, code).glyphs.width
    return _WIDTHS[key]


def wrap_lines(s: str, size: float, width: float, code=()) -> list:
    """Greedy wrap at spaces; a code span or a highlighted span is never split."""
    code = tuple(code)
    for c in code + NOBREAK:
        s = s.replace(c, c.replace(" ", NBSP))
    lines, cur = [], ""
    for w in s.split(" "):
        trial = f"{cur} {w}" if cur else w
        if cur and _line_width(trial.replace(NBSP, " "), size, code) > width:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    return [ln.replace(NBSP, " ") for ln in lines + [cur]]


def question(i: int, size: float, color: str, badge_color: str) -> VGroup:
    """Question i (1-based): rows wrapped at its own size, a numbered badge left of the first row; the
    text's top-left at (Q_X, 0). .badge .lines .strs .flat (badge + glyphs, for glyph-to-glyph
    transforms: the same string at another size has the same glyph count)."""
    s, code = QUESTIONS[i - 1]
    strs = wrap_lines(s, size, Q_W, code)
    assert " ".join(strs) == s, (strs, s)
    rows = [text_line(ln, size, color, code) for ln in strs]
    pitch = rows[0].strut.height * 1.22
    for k, r in enumerate(rows):
        r.shift(np.array([Q_X - r.strut.get_left()[0], -k * pitch - r.strut.get_top()[1], 0]))
    big = size >= Q_BIG
    rad = 0.24 if big else 0.2
    b = step_badge(i, badge_color, size=22 if big else 20, radius=rad)
    b.move_to([Q_X - 0.22 - rad, rows[0].strut.get_center()[1], 0])
    g = VGroup(b, *rows)
    g.badge, g.lines, g.strs = b, rows, strs
    g.flat = VGroup(b, *[gl for r in rows for gl in r.glyphs])
    return g


def _glyph_rows(q: VGroup) -> list:
    """The row index of every member of q.flat (None for the badge)."""
    return [None] + [k for k, r in enumerate(q.lines) for _ in r.glyphs]


def shrink(q_big: VGroup, q_small: VGroup, arc: float = 1.0) -> AnimationGroup:
    """Question q_big becomes q_small glyph for glyph. A glyph that moves up to the end of the row
    above (the small question re-wraps) travels on an arc that dips below the chord, so it passes
    under the row it joins instead of through its glyphs."""
    anims = []
    for a, b, ra, rb in zip(q_big.flat, q_small.flat, _glyph_rows(q_big), _glyph_rows(q_small)):
        if ra is not None and ra != rb:
            dx = b.get_center()[0] - a.get_center()[0]
            anims.append(Transform(a, b, path_arc=arc if dx >= 0 else -arc))
        else:
            anims.append(Transform(a, b))
    return AnimationGroup(*anims)


def q_at(q: VGroup, top: float) -> VGroup:
    return q.shift(UP * (top - q.lines[0].strut.get_top()[1]))


def q_bottom(q: VGroup) -> float:
    return q.lines[-1].strut.get_bottom()[1]


def q_span(q: VGroup, sub: str) -> VGroup:
    """The glyphs of `sub` in question q (a span never crosses a line break)."""
    key = "".join(sub.split())
    for r, s in zip(q.lines, q.strs):
        flat = "".join(s.split())
        i = flat.find(key)
        if i >= 0:
            return VGroup(*r.glyphs[i:i + len(key)])
    raise AssertionError((sub, q.strs))


def text_span(t, sub: str) -> VGroup:
    """The glyphs of `sub` in a Text without spaces in `sub` (Text drops spaces from its glyphs)."""
    flat = "".join(t.text.split())
    i = flat.find(sub)
    assert i >= 0, (sub, t.text)
    return VGroup(*t.submobjects[i:i + len(sub)])


def footer_cards() -> VGroup:
    """Beat 7: the Answers card and the study-guide card, side by side. .answers .guide .repo"""
    a_body = VGroup(label("Answers:", 24, INK), mono("exercises.md", 22, INK),
                    label("and study guide §8", 22, INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    g_url = mono(GUIDE_REPO, 20, INK)
    g_body = VGroup(label("Study guide + every command:", 24, INK), g_url,
                    mono(GUIDE_PATH, 20, INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    h = max(a_body.height, g_body.height) + 0.5
    a_box = box(a_body.width + 0.7, h, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
    g_box = box(g_body.width + 0.7, h, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
    a_body.move_to(a_box).align_to(a_box, LEFT).shift(RIGHT * 0.35)
    g_body.move_to(g_box).align_to(g_box, LEFT).shift(RIGHT * 0.35)
    row = VGroup(VGroup(a_box, a_body), VGroup(g_box, g_body)).arrange(RIGHT, buff=0.3)
    row.answers, row.guide = row[0], row[1]
    row.repo = text_span(g_url, "MLOps_Learning")
    return row


# ------------------------------------------------------------------ the scene
class Recap(VoiceScene):
    def construct(self):
        assert len(SAY) == 8, len(SAY)

        # ========================================================== 0 · stop adk web; git status
        tr = tracker("RunAg", 1)
        t = term(P_ADK, rows=3, title="laptop")
        preload(t, WEB2.cmd, wrap_rows(RUNNING, t.max_chars))
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.25), FadeIn(t, shift=UP * 0.2), run_time=0.8)
            vo.wait_until("control C stops")
            stop = t.print(self, [STOP[0]], run_time=0.35)
            # the server's log rows fade where they are while ^C flashes: printing the 3-row box
            # into the full strip would slide all three rows up over the title bar
            old = list(t.lines.submobjects[:-1])
            self.play(Indicate(substring(stop[0], "^C"), color=TURN, scale_factor=1.5),
                      FadeOut(VGroup(*old)), run_time=0.5)
            for m in old:
                t.lines.remove(m)
            # the shutdown box right away (the ^C row scrolls out of the strip): the terminal keeps it
            # while it grows and the git status is typed, and it scrolls away with that output
            t.print(self, STOP[1:], run_time=0.3)
            # the strip grows right away (the box stays, " · extra" lands as "An extra" is said), so
            # the git status output is up by "the renamed folders" rather than a phrase late
            resize(self, t, 12, keep=3, run_time=0.6, extra=[caption_extra(tr, True)])
            vo.wait_until("An extra git status")
            cg = type_cmd(self, t, GIT.cmd, 1.0)
            out = t.print(self, GIT_OUT, run_time=0.6)
            # out[1] and out[8] are '…' rows (the deleted files; the two ignored __pycache__/ folders)
            renamed, pin_row, ignored = [out[0], out[3], out[4], out[5]], out[2], [out[6], out[7], out[9]]
            vo.wait_until("the renamed folders")
            xt = beside(extra_tag(), t, cg.rows[0], buff=0.4)     # the extra tag joins the flash
            pin(self, cg.rows[0], xt, anim=AnimationGroup(
                FadeIn(xt, shift=LEFT * 0.1),
                LaggedStart(*[Indicate(r.glyphs, color=TURN, scale_factor=1.06) for r in renamed], lag_ratio=0.2)),
                run_time=1.0)
            vo.wait_until("and your Python pin")
            self.play(pin_row.glyphs.animate.set_color(DATA), run_time=0.4)
            pin(self, pin_row, beside(_keep(tag("your pin", DATA)), t, pin_row), run_time=0.4)
            vo.wait_until("dot env, the virtual environment")
            self.play(*[r.glyphs.animate.set_color(S.GREY) for r in ignored + [out[8]]], run_time=0.5)
            bx = max(r.glyphs.get_right()[0] for r in ignored) + 0.35
            br = rbracket(ignored, bx)          # spans the '…' row between .venv/ and uv.lock
            ig = _keep(tag("ignored", S.GREY)).next_to(br, RIGHT, buff=0.15).set_y(br.get_center()[1])
            pin(self, ignored[1], VGroup(br, ig), anim=AnimationGroup(Create(br), FadeIn(ig, shift=LEFT * 0.1)),
                run_time=0.5)

        # ========================================================== 1 · .adk/ sessions; the 1.6 GB .venv
        ex = excerpt_chip(SESS_DB, "uv run adk web · log (excerpt)", line=SESS_LOG)
        place(ex, left=-6.2, top=2.75)
        a = SESS_DB.index(".adk/")
        assert len(ex.text.submobjects) == len(SESS_DB), len(ex.text.submobjects)
        adk_part = VGroup(*ex.text.submobjects[a:a + len(".adk/")])
        gh = ghost_folder("baseline/.adk/")
        place(gh, left=-6.1, top=ex.get_bottom()[1] - 0.3)
        red = _keep(tag("sessions · not in .gitignore", ERR)).next_to(gh, RIGHT, buff=0.3)
        fix = mixed_chip(["add", "`.adk/`", "to your ignore file (exercises)"])
        place(fix, left=-6.2, top=gh.get_bottom()[1] - 0.3)
        # 1.6 GB is this capture's CPU-only torch (a Mac's too); S09: a Linux PC adds the CUDA packages
        venv = mixed_chip([["`.venv`", "· 1.6 GB · delete when done"],
                           ["on a Linux PC: about 3 GB more (CUDA)"]])
        place(venv, right=6.3, top=ex.get_top()[1])
        with self.voiceover(SAY[1]) as vo:
            resize(self, t, 7, keep=7, run_time=0.7)
            base_row = out[3]
            vo.wait_until("The sessions in the agent")
            self.play(FadeIn(ex, shift=DOWN * 0.15), run_time=0.5)
            self.play(adk_part.animate.set_color(ERR), run_time=0.3)
            self.play(TransformFromCopy(VGroup(*ex.text.submobjects[:a + len(".adk/")]), gh.text),
                      Create(gh.glyph), run_time=0.8)
            self.play(FadeIn(red, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("aren't ignored")
            rb = col_box(base_row, 3, len("?? baseline/"), ERR)
            self.play(Create(rb), Indicate(base_row.glyphs, color=ERR, scale_factor=1.06), run_time=0.7)
            base_row.add(rb)
            vo.wait_until("so don't commit them")
            self.play(FadeIn(fix, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("and delete the 1.6 gigabyte")
            self.play(FadeIn(venv, shift=DOWN * 0.1), Indicate(out[7].glyphs, color=INK, scale_factor=1.12),
                      run_time=0.8)

        # ========================================================== 2 · Colab runtimes; three keys
        cf = colab_frame("Colab · every notebook", width=12.6, top=3.3, bottom=1.25)
        mp = menu_path(["Runtime", "Disconnect and delete runtime"])
        place(mp, left=-5.9, cy=2.42)
        ticks = tick_row(["Cheese Quiz", "Travel Planner", "Newsletter"])
        place(ticks, left=-5.9, cy=1.7)
        cols = [key_column("service account", ["in", "`secrets/`", "beside", "`llm-rag`"], -4.2, 0.85),
                key_column("AI Studio key", ["root", "`.env`"], 0.0, 0.85),
                key_column("OpenAI key", ["Colab Secrets only"], 4.2, 0.85)]
        beside_w = span(cols[0].where, "beside")
        notes = [end_note(cols[1]), end_note(cols[2])]
        y_note = min(c.get_bottom()[1] for c in cols[1:]) - 0.22
        for n in notes:
            place(n, top=y_note)
        stopped = mixed_chip(["`llm-rag`", ": stopped in part 1"])
        corpus = mixed_chip([["tried", "`6-rag/1-vertex-rag-engine`", "?"],
                             ["its corpus is billable ·", "`exercises.md`", "deletes it"]], COST)
        place(stopped, cx=-4.2, top=notes[0].get_bottom()[1] - 0.45)
        place(corpus, left=stopped.get_right()[0] + 0.5, cy=stopped.get_center()[1])
        ul_b = under(beside_w, TURN, 3)
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(t, tr, ex, gh, red, fix, venv)), run_time=0.5)
            self.play(Create(cf.frame), FadeIn(cf.title), FadeIn(cf.tag), run_time=0.6)
            vo.wait_until("disconnect and delete the runtime")
            self.play(FadeIn(mp, shift=RIGHT * 0.15), run_time=0.4)
            self.play(mp.light(1), run_time=0.4)
            for item in ticks:
                self.play(Create(item[0]), FadeIn(item[1]), run_time=0.35)
            vo.wait_until("Keep the service account key")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in cols], lag_ratio=0.25), run_time=0.9)
            self.play(Indicate(cols[0].key, color=KEY, scale_factor=1.25), run_time=0.6)
            vo.wait_until("never inside")
            self.play(beside_w.animate.set_color(TURN), Create(ul_b), FadeIn(stopped, shift=UP * 0.1),
                      run_time=0.6)
            vo.wait_until("and delete or cap the other two keys")
            self.play(*[FadeIn(n, shift=UP * 0.1) for n in notes],
                      *[Indicate(c.key, color=KEY, scale_factor=1.2) for c in cols[1:]], run_time=0.7)
            vo.wait_until("when the course ends")
            self.play(FadeIn(corpus, shift=LEFT * 0.15), run_time=0.6)
        self.wait(1.0)                                  # the two chips are read once

        # ========================================================== 3 · slide 41, filled with today's code
        A = Anatomy(box_w=11.8, block_h=1.75, ends=False)
        A.move_to([0, 3.05 - A.height / 2, 0])
        lr = lref("41")
        filled = []                      # the chips (not members of A)
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(cf, mp, ticks, *cols, ul_b, *notes, stopped, corpus)), run_time=0.5)
            self.play(FadeIn(lr), FadeIn(A, shift=UP * 0.15), run_time=0.8)
            for name, phrase in (("core", "Gemini and OpenAI models"), ("instructions", "prompts and output types"),
                                 ("tools", "tools by hand"), ("memory", "history and session state")):
                vo.wait_until(phrase)
                self.play(A.light(name), run_time=0.3)
                # fill() after light(): two pending .animate builders on one name would share a target
                chips, anims = A.fill(name, FILL[name])
                filled.append(chips)
                lead = anims[:len(anims) - len(chips)]
                if name == "tools":       # one chip per word: by hand · decorated · over MCP
                    self.play(*lead, anims[len(lead)], run_time=0.45)
                    vo.wait_until("decorated")
                    self.play(anims[len(lead) + 1], run_time=0.35)
                    vo.wait_until("or over MCP")
                    self.play(anims[len(lead) + 2], run_time=0.35)
                else:
                    self.play(*lead, *anims[len(lead):], run_time=0.5)
            self.wait(0.4)
            self.play(A.unlight(), run_time=0.4)

        # ========================================================== 4 · the loop; the lecture's formula
        f_text = label(FORMULA, 24, INK)
        assert len(f_text.submobjects) == len("".join(FORMULA.split())), len(f_text.submobjects)
        # written term by term as the SAY names them; each term lights its block (the lecture's
        # "reasoning" is the LLM core's own thinking: SLIDES.md terms table)
        f_terms = [(text_span(f_text, "agent≈"), None), (text_span(f_text, "LLM+reasoning"), "core"),
                   (text_span(f_text, "+instructions"), "instructions"), (text_span(f_text, "+tools"), "tools")]
        g1 = _keep(chip("+ a loop the framework runs", DATA, size=20, pad_y=0.09))
        g2 = _keep(chip("+ checks your code enforces", DATA, size=20, pad_y=0.09))
        VGroup(g1, g2).arrange(RIGHT, buff=0.3)
        place(f_text, cx=0, top=A.get_bottom()[1] - 0.12)
        place(VGroup(g1, g2), cx=0, top=f_text.get_bottom()[1] - 0.12)
        with self.voiceover(SAY[4]) as vo:
            self.play(A.light("control"), run_time=0.5)
            vo.wait_until("the framework's loop")
            self.play(*A.fill_control(), run_time=0.6)
            cchips, canims = A.fill("control", ["`Runner`", "`max_turns=12`",
                                                _keep(chip("llm-rag: two calls by hand", CTR, size=20))])
            self.play(canims[0], canims[1], canims[2], run_time=0.6)
            vo.wait_until("or two calls by hand")
            self.play(canims[3], run_time=0.5)
            vo.wait_until("The lecture's formula")
            lr = lref_swap(self, lr, "32–33", run_time=0.5)
            self.play(Write(f_terms[0][0]), run_time=0.5)
            for (part, blk), phrase, rt in zip(f_terms[1:], ("LLM plus reasoning", "instructions and tools",
                                                             "tools, gains"), (0.7, 0.6, 0.5)):
                vo.wait_until(phrase)
                self.play(Write(part), A.light(blk), run_time=rt)
            self.remove(*[p for p, _ in f_terms])
            self.add(f_text)
            vo.wait_until("gains two pieces")
            self.play(Indicate(f_text, color=INK, scale_factor=1.06), run_time=0.6)
            vo.wait_until("a loop the framework runs")
            self.play(FadeIn(g1, shift=LEFT * 0.15), A.unlight(), Indicate(A.parts["control_fill"], color=TOOL,
                                                                             scale_factor=1.03), run_time=0.7)
            vo.wait_until("and checks that your own code enforces")
            self.play(FadeIn(g2, shift=LEFT * 0.15), run_time=0.6)

        # ========================================================== 5 · test yourself: Q1, Q2
        title = label("Test yourself", 34, INK)
        place(title, left=-6.2, top=3.5)
        t_ul = Line(title.get_corner(DOWN + LEFT) + DOWN * 0.08, title.get_corner(DOWN + RIGHT) + DOWN * 0.08,
                    color=TURN, stroke_width=3)
        q1 = q_at(question(1, Q_BIG, INK, TURN), Q_TOP)
        smalls = []

        def step(q_cur, i_cur, top_cur):
            """Question i_cur turns small and GREY at top_cur (re-wrapped); question i_cur + 1 writes
            in under it. Returns (new question, its top)."""
            small = q_at(question(i_cur, Q_SMALL, S.GREY, S.GREY), top_cur)
            top_new = q_bottom(small) - 0.3
            q_new = q_at(question(i_cur + 1, Q_BIG, INK, TURN), top_new)
            self.play(shrink(q_cur, small), run_time=0.6)
            self.remove(q_cur, q_cur.flat)
            self.add(small)
            smalls.append(small)
            self.play(FadeIn(q_new, shift=UP * 0.15), run_time=0.5)
            return q_new, top_new

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(A, *filled, cchips, f_text, g1, g2, lr)),
                      run_time=0.6)
            self.play(FadeIn(title, shift=DOWN * 0.15), Create(t_ul), run_time=0.6)
            vo.wait_until("One:")
            self.play(FadeIn(q1, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("who runs the function")
            self.play(q_span(q1, "who runs the function").animate.set_color(TURN), run_time=0.4)
            vo.wait_until("and what goes back in call 2")
            self.play(q_span(q1, "what travels back").animate.set_color(TURN),
                      q_span(q1, "call 2?").animate.set_color(TURN), run_time=0.5)
            vo.wait_until("Two:")
            q2, top2 = step(q1, 1, Q_TOP)
            vo.wait_until("what does mode any change")
            self.play(q_span(q2, 'mode="any"').animate.set_color(TURN), run_time=0.4)
            vo.wait_until("and why only on call 1")
            self.play(q_span(q2, "only on call 1?").animate.set_color(TURN), run_time=0.4)

        # ========================================================== 6 · Q3, Q4
        with self.voiceover(SAY[6]) as vo:
            q3, top3 = step(q2, 2, top2)
            vo.wait_until("what ends an agent loop")
            self.play(q_span(q3, "ends an agent loop").animate.set_color(TURN), run_time=0.4)
            vo.wait_until("what cap do frameworks add")
            self.play(q_span(q3, "cap").animate.set_color(TURN), run_time=0.4)
            vo.wait_until("and which block is that")
            self.play(q_span(q3, "lecture block").animate.set_color(TURN), run_time=0.4)
            vo.wait_until("Four:")
            q4, top4 = step(q3, 3, top3)
            vo.wait_until("how does the summarizer")
            self.play(q_span(q4, "TripSummarizer").animate.set_color(TURN), run_time=0.4)
            vo.wait_until("without a message")
            self.play(q_span(q4, "without a message").animate.set_color(TURN), run_time=0.4)

        # ========================================================== 7 · Q5; answers, the guide, next time
        foot = footer_cards()
        nxt = concept_box("Lecture 7 · Agents II: the harness", 22)
        place(nxt, right=6.4, cy=title.get_center()[1])
        with self.voiceover(SAY[7]) as vo:
            q5, top5 = step(q4, 4, top4)
            vo.wait_until("what decides that a harness run succeeded")
            self.play(q_span(q5, "decides that a run succeeded").animate.set_color(TURN), run_time=0.4)
            vo.wait_until("and why not the model's word")
            self.play(q_span(q5, "not the model's final text?").animate.set_color(TURN), run_time=0.4)
            vo.wait_until("Answers and every command")
            small5 = q_at(question(5, Q_SMALL, S.GREY, S.GREY), top5)
            self.play(shrink(q5, small5), run_time=0.6)
            self.remove(q5, q5.flat)
            self.add(small5)
            smalls.append(small5)
            place(foot, left=-6.2, top=q_bottom(small5) - 0.5)
            self.play(FadeIn(foot.answers, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("and the study guide")
            self.play(FadeIn(foot.guide, shift=UP * 0.15), run_time=0.6)
            self.play(Create(under(foot.repo, TURN, 3)), foot.repo.animate.set_color(TURN), run_time=0.6)
            vo.wait_until("Next lecture")
            self.play(FadeIn(nxt, shift=LEFT * 0.2), run_time=0.6)

        self.wait(0.6)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9)
        self.wait(0.3)
