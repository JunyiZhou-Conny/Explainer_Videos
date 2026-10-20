"""S09 · ADK: clone, configure, and a sync that fails (dlops-io/llm-agent-google-adk README
"Getting Started", steps 1–6). Part 2 opens here. Lecture: 35 (beat 6 only).

Beats (script.md "## S09", one voiceover block each):
0. A new picture, centred while it is alone: the GREY laptop zone with a GREY dashed "no Docker this
   time" chip, a PURPLE uv chip and an empty GREEN `.venv` box; across a dashed boundary a BLUE
   "Gemini API" chip, reached by a PINK arrow carrying the GOLD key "AI Studio key". At "Open a new
   terminal" the picture rises; below it the terminal (5 rows, title laptop,
   prompt student@laptop:~/AC215$) fades in with the GREY caption "a new terminal · the folder that
   holds your clones · not inside llm-rag"; ~/AC215 flashes.
1. The picture leaves. TRACKER Start 1; the terminal grows to 12 rows; the README chip
   "README.md · line 77 · git clone <repository-url>" + expected sits in the band between the
   tracker and the terminal (the top band beside the tracker is too narrow for it). It types
   the clone (folds onto two rows) -> adk-laptop/01 line 2, GREY note "the README's placeholder,
   filled in" beside it. TRACKER Start 2: the chip becomes "line 78 · cd google-adk-tutorial"; it
   types `cd google-adk-tutorial` -> 02 line 2, RED; tag `erratum` on the command.
2. "llm-agent-google-adk" in the clone's output flashes GREEN; it types `cd llm-agent-google-adk`
   (no output), the prompt becomes ~/AC215/llm-agent-google-adk$ and its new part flashes GREEN; a
   GREEN tag "named after the repo" on that new prompt row (it fades as beat 3 starts).
3. The chip leaves. TRACKER Start 2 · extra. `ls -a` (extra) -> 04 lines 2–4: the rows are 70–76
   characters, so each folds at its last column gap (a GREY ↪ row; names never split). The six
   module folders get GREY boxes, pyproject.toml turns GREEN; a GREY dashed ghost `uv.lock`
   "git-ignored · .gitignore line 34" sits beside it.
4. TRACKER Start 3: `cp .env.example .env` (the prompt returns). TRACKER Start 3 · extra:
   `grep -v '^#' .env | grep .` (extra; folds) -> 06 lines 2–5; line 2 GREY + tag "placeholder",
   line 4 YELLOW.
5. TRACKER Start 4: the terminal shrinks to the 3-row strip (06 lines 2–4). Above it, right: the
   GREY `.env` card (".env · your copy · git-ignored": GOOGLE_API_KEY= + a dashed key slot,
   GEMINI_MODEL=gemini-2.5-flash) and the GREY note "README: the key's source is the next step;
   paste it here". TRACKER Start 5: a GREY browser (illustration) "Google AI Studio · API keys"
   with a "Create API key" button, left; a GOLD key appears in the page's key list and flies
   into the slot after `=`.
6. The GEMINI_MODEL line lights YELLOW; LECTURE 35 fades in, the browser leaves, the card moves to
   the centre; gemini-2.5-flash slides out, gemini-3.1-flash-lite slides in GREEN; GREY tag "your
   edit · the model llm-rag uses (cli.py · line 27)".
7. The lecture tag leaves. Two GREY chips under the card, each with `erratum`: "the code's
   fallback: gemini-2.0-flash (1-baseline/agent.py · line 12) · shut down" and "gemini-2.5-flash ·
   limited to earlier users"; GREY tag "Google's model pages, checked October 18, 2026". They
   leave for a GREY dashed card (module READMEs' Setup steps: skip them · the root sync and the
   root .env cover every module · only the nearest .env is loaded, PINK). The cards leave; ▶ on a
   static GREY card (clone, cd, cp, the two .env lines, a GOLD key line). Hold 2 s.
8. The card and the strip leave (the 12-line panel needs the frame). CODE(pyproject.toml: 8–19):
   line 8 GREEN, line 10 YELLOW + tag "no upper bound", lines 18–19 GREY + "→ onnxruntime, PyTorch".
9. V5: line 8 becomes the number line's GREEN `>=3.10` label; axis 3.10 … 3.16, the band glows to
   the right edge; no ORANGE dot; GREY chip "no python3 on PATH" (adk-laptop/00 line 9, extra).
   PONDER(6 s) in the lower third.
10. TRACKER Start 6. The terminal returns (9 rows, under the number line): `uv sync` -> 07 lines
    2–4; a PURPLE download arrow drops CPython 3.15.0 at the newest end; tag "at the time of
    recording" on "Using CPython 3.15.0". (9 rows, not 12: the number line must stay in view.)
11. 07 lines 5–7 joined and 9–11 joined, re-wrapped at spaces as uv wraps them (the error's rows
    with uv's 7-space hanging indent; 4 + 3 rows, so "Using CPython 3.15.0" scrolls off), RED;
    `onnxruntime` flashes in the hint. The terminal shrinks to the strip (the hint's three rows);
    above it the wheel shelf (onnxruntime 1.31.0: cp311 … cp314t, an empty cp315 slot) with a GREY
    arrow from the excerpt chip `"chromadb>=0.5.0",` (pyproject.toml · line 18); cp315 turns RED.
12. GREY tag "erratum · fails whenever uv picks 3.15" beside the tracker; GREY note "uv tries the
    Pythons it downloaded before the system's (as in lecture 1): a uv-managed 3.15 wins over a
    system 3.12". TRACKER Start 6 · extra: `uv python pin 3.13` (extra) -> 09 line 2, tag "fix · not
    in the README"; the band collapses to 3.13, the cp313 wheel clicks GREEN, a GREEN
    `.python-version` card "3.13" drops in; the picture holds 1.2 s.
13. TRACKER Start 6. The picture leaves; the terminal grows to 12 rows: `uv sync` -> 12 lines 2–4,
    …, 38, …, 89, …, 155; "CPython 3.13.16", google-adk==2.12.0 and onnxruntime==1.31.0 GREEN. A GREY
    card in the terminal's empty right part: ".venv: about 1.6 GB (du -sh .venv, extra) · on a Linux
    PC: about 3 GB more of CUDA packages · a Mac: none" (adk-laptop/14 line 12, 10); its frame starts
    around the first row and grows as the other two write in.
14. TRACKER Start 6 · extra: `uv run adk --version` (extra) -> 13 line 2, tags extra and "at the time
    of recording". The terminal shrinks to the strip; ▶ on a static GREY card (cd, cp, key +
    GEMINI_MODEL in .env, uv python pin 3.13 (extra), uv sync). Hold 2 s. Empty frame.
"""

import textwrap

import numpy as np
from common import (
    API_KEY_PLACEHOLDER,
    COST,
    DATA,
    ERR,
    INK,
    LOOKUP,
    MODEL_ADK,
    MODEL_RAG,
    NARRATION,
    P_ADK,
    P_WS,
    STRIP_TOP,
    TOOL,
    TURN,
    VENV,
    WHEEL_TAGS,
    Prose,
    VersionLine,
    WheelShelf,
    bare_prompt,
    beside,
    caption_extra,
    capture,
    cd_prompt,
    col_box,
    erratum_tag,
    excerpt,
    excerpt_chip,
    expected_tag,
    extra_tag,
    file_row,
    fix_tag,
    ghost_file,
    grey_tag,
    illustration_tag,
    key_glyph,
    key_outline,
    laptop_zone,
    lref,
    note,
    pin,
    ponder_at,
    recording_tag,
    resize,
    source_text,
    src_panel,
    term,
    tracker,
    turn_card,
    type_cmd,
)
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Create,
    DashedLine,
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
    LaggedStart,
    ReplacementTransform,
    RoundedRectangle,
    Transform,
    VGroup,
)

from explainer import style as S
from explainer.devops import (
    CAPTION,
    MONO,
    box,
    browser_window,
    chip,
    label,
    mono,
    mono_line,
    substring,
    tag,
)
from explainer.scene import VoiceScene

SAY = NARRATION["S09"]

# ------------------------------------------------------------------ the real captures and sources
ENV = capture("00", "adk-laptop")
assert ENV.line(9) == "no python3 on PATH", ENV.line(9)
CLONE = capture("01", "adk-laptop")
assert CLONE.cmd == "git clone https://github.com/dlops-io/llm-agent-google-adk.git", CLONE.cmd
assert CLONE.line(2) == "Cloning into 'llm-agent-google-adk'...", CLONE.line(2)
CD_BAD = capture("02", "adk-laptop")
assert CD_BAD.cmd == "cd google-adk-tutorial" and CD_BAD.exit == 1, CD_BAD.cmd
assert CD_BAD.line(2).endswith("No such file or directory"), CD_BAD.line(2)
CD = capture("03", "adk-laptop")
assert CD.cmd == "cd llm-agent-google-adk" and not CD.lines, CD.cmd
LS = capture("04", "adk-laptop")
assert LS.cmd == "ls -a", LS.cmd
MODULES = ("1-baseline", "2-litellm", "3-mcp-tools", "4-production-ready", "5-custom-agent", "6-rag")
assert all(any(m in LS.line(n) for n in (2, 3, 4)) for m in MODULES)
assert "pyproject.toml" in LS.line(4) and not any("uv.lock" in LS.line(n) for n in (2, 3, 4))
CP = capture("05", "adk-laptop")
assert CP.cmd == "cp .env.example .env" and not CP.lines, CP.cmd
GREP = capture("06", "adk-laptop")
assert GREP.cmd == "grep -v '^#' .env | grep .", GREP.cmd
assert GREP.line(2) == f"GOOGLE_API_KEY={API_KEY_PLACEHOLDER}", GREP.line(2)
assert GREP.line(4) == f"GEMINI_MODEL={MODEL_ADK}", GREP.line(4)
SYNC1 = capture("07", "adk-laptop")
assert SYNC1.cmd == "uv sync" and SYNC1.exit == 2, SYNC1.cmd
assert SYNC1.line(2) == "Using CPython 3.15.0" and SYNC1.line(4).startswith("Resolved 189 packages")
ERR_ROW = SYNC1.join(5, 6, 7)
HINT_ROW = SYNC1.join(9, 10, 11)
assert "onnxruntime==1.31.0" in ERR_ROW and "`cp315`" in HINT_ROW, (ERR_ROW, HINT_ROW)
assert all(f"`{w}`" in HINT_ROW for w in WHEEL_TAGS), HINT_ROW


def uv_wrap(s: str, limit: int = 65, indent: int = 0) -> list[str]:
    """One uv message re-wrapped for a 65-column terminal the way uv wraps its own (07 lines 5-7
    and 9-11: at spaces, the error's rows with a 7-space hanging indent). Nothing is added or cut:
    the asserts check the words and their order."""
    rows = textwrap.wrap(s, limit, subsequent_indent=" " * indent, break_long_words=False,
                         break_on_hyphens=False)
    assert " ".join(r.strip() for r in rows) == " ".join(s.split()), rows
    assert all(len(r) <= limit for r in rows), rows
    return rows


ERR_ROWS = uv_wrap(ERR_ROW, 65, 7)            # 4 rows ("…@" / "registry+https://pypi.org/simple` …")
HINT_ROWS = uv_wrap(HINT_ROW, 65)             # 3 rows; "(v1.31.0)" and every tag stay whole
assert len(HINT_ROWS) == 3 and "`onnxruntime`" in HINT_ROWS[0], HINT_ROWS
PIN = capture("09", "adk-laptop")
assert PIN.cmd == "uv python pin 3.13" and PIN.line(2) == "Pinned `.python-version` to `3.13`", PIN.lines
PLAN = capture("10", "adk-laptop")          # uv sync --dry-run on a Linux PC: the CUDA packages
assert sum("nvidia-" in s for s in PLAN.lines) == 15 and " + torch==2.14.1" in PLAN.lines
SYNC2 = capture("12", "adk-laptop")
assert SYNC2.cmd == "uv sync" and SYNC2.exit == 0, SYNC2.cmd
assert SYNC2.line(2).startswith("Using CPython 3.13"), SYNC2.line(2)
assert SYNC2.line(38) == " + google-adk==2.12.0" and SYNC2.line(89) == " + onnxruntime==1.31.0"
assert SYNC2.line(155) == " + zipp==4.1.1", SYNC2.line(155)
VER = capture("13", "adk-laptop")
assert VER.cmd == "uv run adk --version" and VER.line(2) == "adk, version 2.12.0", VER.lines
PKGS = capture("14", "adk-laptop")
assert PKGS.line(12).startswith("1.6G") and PKGS.line(12).endswith(".venv"), PKGS.line(12)

README = source_text("llm-agent-google-adk/README.md").splitlines()
README_77, README_78 = README[76].strip(), README[77].strip()
assert README_77 == "git clone <repository-url>" and README_78 == "cd google-adk-tutorial"
PYPROJECT = "llm-agent-google-adk/pyproject.toml"
assert excerpt(PYPROJECT, 8, 8).strip() == 'requires-python = ">=3.10"'
assert excerpt(PYPROJECT, 10, 10).strip() == '"google-adk>=1.8.0",'
CHROMA_LINE = excerpt(PYPROJECT, 18, 18)
assert CHROMA_LINE.strip() == '"chromadb>=0.5.0",' and "sentence-transformers" in excerpt(PYPROJECT, 19, 19)
assert '"gemini-2.0-flash"' in excerpt("llm-agent-google-adk/1-baseline/agent.py", 12, 12)
assert f'GENERATIVE_MODEL = "{MODEL_RAG}"' == excerpt("cli.py", 27, 27).strip()

# ------------------------------------------------------------------ layout
AXIS_Y = 1.95                  # the V5 number line, beats 9–12 (tick labels end at y ≈ 1.38)
RUN_ROWS = 9                   # the failing sync's terminal: its top (0.98) stays under the ticks
GAP_Y = STRIP_TOP + 0.14       # the lowest y a picture above the 3-row strip may use
TOP_Y = 2.8                    # nothing above this but the tracker band
LIFT0 = 1.6                    # beat 0: the picture starts this much lower (centred), then rises


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


def attach(scene, row, *mobs):
    """Make mobs (already on screen) part of terminal row `row`: they scroll and fade with it."""
    for m in mobs:
        scene.remove(m)
        row.add(m)
    scene.add(row)


def last_row(line):
    """The last row of a typed command (folded or not)."""
    return line.rows[-1] if hasattr(line, "rows") else line


def column_fold(s: str, limit: int = 65) -> list[str]:
    """An `ls` row wider than the terminal, folded at its last column gap that fits: the names stay
    whole, the rest goes on a GREY ↪ row (the capture's own text, nothing added but the mark)."""
    if len(s) <= limit:
        return [s]
    i = s.rfind("  ", 0, limit)
    assert i > 0, s
    head, rest = s[:i].rstrip(), s[i:].strip()
    assert head.split() + rest.split() == s.split()
    return [head, f"  ↪ {rest}"]


def dashed_chip(s: str, color: str = S.GREY, size: float = 22, text_color: str | None = None) -> VGroup:
    """A GREY dashed chip: something that isn't there this time. .box .text"""
    t = label(s, size, text_color or color)
    h = mono("|", size).height + 0.26
    b = box(t.width + 0.5, h, color, dashed=True, radius=h / 2.6)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def readme_cmd_chip(line_no: int, cmd: str) -> VGroup:
    """The one-line README chip for a README command (the command in mono) + `expected`."""
    where = VGroup(mono("README.md", CAPTION, S.GREY), label(f"· line {line_no}", CAPTION, S.GREY))
    where.arrange(RIGHT, buff=0.12)
    row = VGroup(where, mono(cmd, CAPTION, INK)).arrange(RIGHT, buff=0.3)
    fr = box(row.width + 0.4, row.height + 0.24, S.GREY, fill=S.BG, fill_opacity=0.92, radius=0.1)
    fr.move_to(row)
    tg = expected_tag().next_to(fr, RIGHT, buff=0.15)
    return VGroup(fr, row, tg)


def env_card() -> VGroup:
    """The GREY `.env` file card: GOOGLE_API_KEY= with a dashed key slot, and the model line.
    .frame .key_row .slot .model_row .val .header"""
    size = 22
    k_row = mono_line("GOOGLE_API_KEY=", size, INK)
    m_row = mono_line(f"GEMINI_MODEL={MODEL_ADK}", size, INK)
    rows = VGroup(k_row, m_row).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
    wide = mono_line(f"GEMINI_MODEL={MODEL_RAG}", size, INK)       # the row after the edit
    fr = box(wide.width + 0.7, rows.height + 0.5, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.14)
    rows.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.35)
    slot = key_outline(0.34).next_to(k_row.glyphs, RIGHT, buff=0.22)
    head = VGroup(mono(".env", CAPTION, S.GREY), label("· your copy · git-ignored", CAPTION, S.GREY))
    head.arrange(RIGHT, buff=0.12).next_to(fr, UP, buff=0.1).align_to(fr, LEFT).shift(RIGHT * 0.12)
    g = VGroup(fr, rows, slot, head)
    g.frame, g.key_row, g.slot, g.model_row, g.header = fr, k_row, slot, m_row, head
    g.val = substring(m_row, MODEL_ADK)
    return g


def regroup(scene, parent, add=(), drop=(), at: int | None = None):
    """Make `add` (on screen) members of `parent` (at index `at`, else on top), take `drop` out of
    it and off the screen, and list `parent` once on the scene (no member drawn twice)."""
    for m in drop:
        parent.remove(m)
    for m in add:
        if at is None:
            parent.add(m)
        else:
            parent.submobjects.insert(at, m)
    scene.remove(*{*parent.get_family(), *add, *drop, parent})
    scene.add(parent)


def ai_studio() -> VGroup:
    """The schematic AI Studio page (no logo, no screenshot): a GREY browser titled "Google AI
    Studio · API keys" with a "Create API key" button. .button .title"""
    b = browser_window("x", width=5.4, height=3.3)
    b.remove(b.address)                       # the title goes in the address field instead
    ttl = label("Google AI Studio · API keys", CAPTION, S.GREY)
    ttl.move_to(b[3]).align_to(b[3], LEFT).shift(RIGHT * 0.2)
    btn_t = label("Create API key", 22, INK)
    btn = RoundedRectangle(width=btn_t.width + 0.6, height=0.6, corner_radius=0.12, stroke_color=S.GREY,
                           stroke_width=2.5).set_fill(S.GREY, 0.22)
    btn_t.move_to(btn)
    button = VGroup(btn, btn_t).move_to(b.content.get_center() + UP * 0.25)
    bars = VGroup(*[RoundedRectangle(width=w, height=0.12, corner_radius=0.06, stroke_width=0)
                    .set_fill(S.GREY_DARK, 1) for w in (3.6, 2.8)]).arrange(DOWN, buff=0.18)
    bars.next_to(button, DOWN, buff=0.4)
    g = VGroup(b, ttl, button, bars)
    g.button, g.title, g.frame, g.bars = button, ttl, b.frame, bars
    return g


def model_chip_row(parts) -> VGroup:
    """A GREY chip holding a row of (text, kind, colour) pieces: kind "m" mono, else serif."""
    row = VGroup(*[(mono(s, CAPTION, c) if k == "m" else label(s, CAPTION, c)) for s, k, c in parts])
    row.arrange(RIGHT, buff=0.12)
    fr = box(row.width + 0.44, row.height + 0.26, S.GREY, fill=S.BG, fill_opacity=0.92, radius=0.12)
    fr.move_to(row)
    g = VGroup(fr, row)
    g.frame, g.row = fr, row
    return g


def mixed_row(parts) -> VGroup:
    """A row of (text, kind, colour) pieces, kind "m" mono, else serif; a piece that starts with
    punctuation, or follows an opening bracket, sits close to its neighbour."""
    row = VGroup()
    prev = None
    for s, k, c in parts:
        m = mono(s, CAPTION, c) if k == "m" else label(s, CAPTION, c)
        if prev is not None:
            tight = s[:1] in ",):" or prev[0].endswith("(")
            m.next_to(row[-1], RIGHT, buff=0.05 if tight else 0.12)
            m.align_to(row[-1], DOWN) if k == prev[1] else m.set_y(row[-1].get_y())
        row.add(m)
        prev = (s, k)
    return row


def nearest_card() -> VGroup:
    """The GREY dashed card: keep everything in the root .env. .rows .nearest (the PINK words)"""
    s3, hot = "only the nearest .env is loaded", "the nearest .env"
    r3 = label(s3, CAPTION, INK, t2c={hot: LOOKUP})     # one Text: the words share a baseline
    assert len(r3.submobjects) == len("".join(s3.split())), len(r3.submobjects)
    a = len("".join(s3[:s3.index(hot)].split()))
    rows = VGroup(
        mixed_row([("module READMEs' Setup steps (", "s", INK), ("uv sync, cp .env.example .env", "m", INK),
                   ("): skip them", "s", INK)]),
        mixed_row([("the root sync and the root", "s", INK), (".env", "m", INK),
                   ("cover every module", "s", INK)]),
        r3,
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    fr = box(rows.width + 0.7, rows.height + 0.46, S.GREY, dashed=True, radius=0.14)
    bg = RoundedRectangle(width=fr.width, height=fr.height, corner_radius=0.14, stroke_width=0) \
        .set_fill(S.BG, 0.95).move_to(fr)
    rows.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.35)
    g = VGroup(bg, fr, rows)
    g.frame, g.rows = fr, rows
    g.nearest = VGroup(*r3.submobjects[a:a + len("".join(hot.split()))])
    return g


def pyver_card() -> VGroup:
    """The GREEN `.python-version` file card: "3.13". .frame"""
    fr_row = file_row(".python-version", INK, VENV)
    val = mono("3.13", 24, VENV)
    rows = VGroup(fr_row, val).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    val.shift(RIGHT * 0.4)
    fr = box(rows.width + 0.6, rows.height + 0.44, VENV, fill=S.BG, fill_opacity=0.95, radius=0.14)
    rows.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.3)
    head = note("new in the repo · from the pin")
    head.next_to(fr, UP, buff=0.1).align_to(fr, LEFT).shift(RIGHT * 0.1)
    g = VGroup(fr, rows, head)
    g.frame = fr
    return g


def size_card() -> VGroup:
    """The GREY size card: .venv about 1.6 GB (extra du -sh), CUDA on a Linux PC, none on a Mac."""
    r1 = VGroup(mono(".venv", CAPTION, INK), label("about 1.6 GB ·", CAPTION, INK),
                mono("du -sh .venv", CAPTION, S.GREY), extra_tag()).arrange(RIGHT, buff=0.14)
    r2 = label("on a Linux PC: about 3 GB more of CUDA packages", CAPTION, INK)
    r3 = label("on a Mac: none", CAPTION, INK)
    rows = VGroup(r1, r2, r3).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    fr = box(rows.width + 0.6, rows.height + 0.5, S.GREY, fill=S.BG, fill_opacity=0.97, radius=0.14)
    rows.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.3)
    g = VGroup(fr, rows)
    g.frame, g.rows = fr, rows
    return g


class AdkSetup(VoiceScene):
    def construct(self):
        assert len(SAY) == 15, len(SAY)

        # ========================================================== 0 · part 2: the laptop, no Docker
        zone = laptop_zone(7.2, 2.95, caption="your laptop")
        place(zone, left=-6.4, top=3.35)
        nodock = dashed_chip("no Docker this time")
        place(nodock, left=zone.frame.get_left()[0] + 0.3, top=zone.frame.get_top()[1] - 0.3)
        uvc = chip("uv", TOOL, size=26, font=MONO)
        uvc.move_to([-5.0, 1.55, 0])
        venv_box = box(2.5, 1.25, VENV, fill_opacity=0.05)
        venv_box.move_to([-1.55, 1.55, 0])
        venv_t = mono(".venv", 22, VENV).move_to(venv_box.get_corner(UP + LEFT) + np.array([0.55, -0.27, 0]))
        venv_e = label("empty", CAPTION, S.GREY).move_to(venv_box).shift(DOWN * 0.15)
        venv = VGroup(venv_box, venv_t, venv_e)
        uv_arrow = Arrow(uvc.get_right(), venv_box.get_left(), buff=0.12, color=TOOL, stroke_width=4,
                         max_tip_length_to_length_ratio=0.25, tip_length=0.18)
        zx = zone.frame.get_right()[0]
        bnd = DashedLine([zx + 0.55, zone.frame.get_bottom()[1], 0], [zx + 0.55, zone.frame.get_top()[1], 0],
                         color=S.GREY, stroke_width=2.5, dash_length=0.12)
        gem = chip("Gemini API", S.BLUE, size=24)
        place(gem, left=zx + 2.75, cy=1.85)
        link = Arrow([zx + 0.05, 1.85, 0], gem.get_left(), buff=0.12, color=LOOKUP, stroke_width=4,
                     max_tip_length_to_length_ratio=0.15, tip_length=0.2)
        kmid = (zx + 0.05 + gem.get_left()[0]) / 2 + 0.25
        key0 = key_glyph(0.34).move_to([kmid, 2.3, 0])
        key0_l = label("AI Studio key", CAPTION, COST).move_to([kmid, 1.42, 0])
        picture = VGroup(zone, nodock, uvc, uv_arrow, venv, bnd, gem, link, key0, key0_l)
        picture.shift(DOWN * LIFT0)          # centred while it is alone; it rises for the terminal

        t = term(P_WS, rows=5, title="laptop")
        cap0 = note("a new terminal · the folder that holds your clones · not inside llm-rag")
        place(cap0, left=-6.25, bottom=t.box.get_top()[1] + 0.16)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(zone), Create(bnd), FadeIn(gem, shift=LEFT * 0.2), run_time=1.0)
            vo.wait_until("No Docker this time")
            self.play(FadeIn(nodock, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("Google's Agent Development Kit")
            self.play(GrowArrow(link), FadeIn(key0, scale=0.7), FadeIn(key0_l), run_time=0.8)
            vo.wait_until("runs in a uv environment")
            self.play(FadeIn(uvc, scale=0.9), run_time=0.5)
            self.play(GrowArrow(uv_arrow), FadeIn(venv), run_time=0.6)
            vo.wait_until("on your laptop")
            self.play(Indicate(zone.caption, color=TURN, scale_factor=1.15), run_time=0.8)
            vo.wait_until("Open a new terminal")
            self.play(picture.animate.shift(UP * LIFT0), run_time=0.6)
            self.play(FadeIn(t, shift=UP * 0.2), FadeIn(cap0, shift=UP * 0.1), run_time=0.6)
            p0 = bare_prompt(self, t)
            vo.wait_until("where you keep your clones")
            self.play(Indicate(substring(p0, "~/AC215"), color=TURN, scale_factor=1.15), run_time=0.8)

        # ========================================================== 1 · clone; the README's cd fails
        tr = tracker("Start", 1)
        rc77 = readme_cmd_chip(77, README_77)
        rc78 = readme_cmd_chip(78, README_78)
        for rc in (rc77, rc78):
            place(rc, right=6.45, cy=2.56)            # the band between the tracker and the terminal
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(picture), FadeOut(cap0), FadeIn(tr, shift=DOWN * 0.25), run_time=0.6)
            resize(self, t, 12, run_time=0.6)
            type_cmd(self, t, CLONE.cmd, 1.1)
            out1 = t.print(self, [CLONE.line(2)], run_time=0.4)[0]
            vo.wait_until("the README writes a placeholder")
            self.play(FadeIn(rc77, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("for the address")
            fill = beside(note("the README's placeholder, filled in"), t, out1, buff=0.5)
            pin(self, out1, fill, run_time=0.5)
            self.play(Indicate(rc77[1][1], color=TURN, scale_factor=1.05), run_time=0.7)
            vo.wait_until("The next line says")
            self.play(tr.goto(2), FadeOut(rc77, shift=UP * 0.15), FadeIn(rc78, shift=UP * 0.15), run_time=0.6)
            c2 = type_cmd(self, t, CD_BAD.cmd, 0.7)
            vo.wait_until("but no such folder exists")
            t.print(self, [(CD_BAD.line(2), ERR)], run_time=0.4)
            er = beside(erratum_tag(), t, c2, buff=0.5)
            pin(self, c2, er, run_time=0.4)

        # ========================================================== 2 · the folder is named after the repo
        with self.voiceover(SAY[2]) as vo:
            nm = substring(out1, "llm-agent-google-adk")
            self.play(Indicate(nm, color=DATA, scale_factor=1.12), run_time=0.9)
            self.play(nm.animate.set_color(DATA), run_time=0.4)
            vo.wait_until("Type cd")
            type_cmd(self, t, CD.cmd, 0.7)
            p3 = cd_prompt(self, t, P_ADK, color=DATA)
            # the tag sits on the new prompt, beside the folder name that just turned GREEN (on the
            # cd row it touched the error row above and, later, the `extra` tag of `ls -a` below)
            named = beside(tag("named after the repo", DATA), t, p3, buff=0.5)
            pin(self, p3, named, run_time=0.4)

        # ========================================================== 3 · ls -a: six modules, no lock file
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(rc78), FadeOut(named), caption_extra(tr, True), run_time=0.5)
            p3.remove(named)                    # the bare prompt row is replaced when ls -a is typed
            c4 = type_cmd(self, t, LS.cmd, 0.4)
            pin(self, c4, beside(extra_tag(), t, c4, buff=0.4), run_time=0.3)
            rows = [r for n in (2, 3, 4) for r in column_fold(LS.line(n), t.max_chars)]
            ls_out = t.print(self, rows, run_time=0.7)
            for r in ls_out:
                if "↪" in r.text:
                    substring(r, "↪").set_color(S.GREY)
            vo.wait_until("six numbered module folders")
            boxes = []
            for m in MODULES:
                r = next(x for x in ls_out if m in x.text)
                a = r.text.index(m)
                b = col_box(r, a, a + len(m), S.GREY)
                boxes.append((r, b))
            self.play(LaggedStart(*[Create(b) for _, b in boxes], lag_ratio=0.15), run_time=1.0)
            for r, b in boxes:
                attach(self, r, b)
            vo.wait_until("but no lock file")
            pyr = next(x for x in ls_out if "pyproject.toml" in x.text)
            ghost = VGroup(ghost_file("uv.lock"), note("git-ignored · .gitignore line 34"))
            ghost.arrange(RIGHT, buff=0.3)
            beside(ghost, t, pyr, buff=0.6)
            self.play(substring(pyr, "pyproject.toml").animate.set_color(DATA), run_time=0.5)
            pin(self, pyr, ghost, run_time=0.6)
            vo.wait_until("the repo ignores it")
            self.play(Indicate(ghost[1], color=TURN, scale_factor=1.06), run_time=0.8)
            vo.wait_until("so everyone resolves fresh versions")
            self.play(Indicate(ghost[0], color=TURN, scale_factor=1.15), run_time=0.8)

        # ========================================================== 4 · cp .env.example .env; an extra grep
        with self.voiceover(SAY[4]) as vo:
            self.play(tr.goto(3), run_time=0.5)
            vo.wait_until("copy dot env dot example")
            type_cmd(self, t, CP.cmd, 0.7)
            bare_prompt(self, t)
            vo.wait_until("An extra grep")
            self.play(caption_extra(tr, True), run_time=0.4)
            c5 = type_cmd(self, t, GREP.cmd, 1.0)
            pin(self, last_row(c5), beside(extra_tag(), t, last_row(c5), buff=0.4), run_time=0.3)
            out4 = t.print(self, [GREP.line(n) for n in (2, 3, 4, 5)], run_time=0.6)
            k_out, m_out = out4[0], out4[2]
            vo.wait_until("a placeholder Google API key")
            ph = beside(grey_tag("placeholder"), t, k_out, buff=0.5)
            self.play(k_out.animate.set_color(S.GREY), run_time=0.4)
            pin(self, k_out, ph, run_time=0.4)
            vo.wait_until("and the model")
            self.play(m_out.animate.set_color(TURN), run_time=0.5)
            self.play(Indicate(substring(m_out, MODEL_ADK), color=TURN, scale_factor=1.08), run_time=0.7)

        # ========================================================== 5 · AI Studio key -> the root .env
        envc = env_card()
        place(envc, right=6.45, top=2.55)
        n5 = VGroup(note("README: the key's source is the next step;"), note("paste it here"))
        n5.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        place(n5, left=envc.frame.get_left()[0] + 0.1, top=envc.frame.get_bottom()[1] - 0.25)
        web = ai_studio()
        place(web, left=-6.45, top=2.55)
        ill = illustration_tag()
        place(ill, right=web.frame.get_right()[0] - 0.2, cy=web.frame.get_bottom()[1])
        key5 = key_glyph(0.34).move_to(web.bars[0])          # the new key, first in the page's list
        with self.voiceover(SAY[5]) as vo:
            resize(self, t, 3, keep=[out4[0], out4[1], out4[2]], run_time=0.6, extra=[tr.goto(4)])
            self.play(FadeIn(envc, shift=DOWN * 0.15), run_time=0.6)
            self.play(FadeIn(n5, shift=UP * 0.1), Indicate(envc.slot, color=COST, scale_factor=1.2), run_time=0.7)
            vo.wait_until("in Google AI Studio")
            self.play(tr.goto(5), FadeIn(web, shift=RIGHT * 0.2), FadeIn(ill), run_time=0.7)
            self.play(Indicate(web.button, color=TURN, scale_factor=1.08), run_time=0.6)
            self.play(FadeIn(key5, scale=0.5), run_time=0.4)
            vo.wait_until("and paste it into dot env")
            self.play(key5.animate.move_to(envc.slot), run_time=0.9)
            regroup(self, envc, add=[key5], drop=[envc.slot])
            envc.slot = key5
            vo.wait_until("after Google API key equals")
            self.play(Indicate(envc.key_row, color=TURN, scale_factor=1.05),
                      Indicate(key5, color=COST, scale_factor=1.2), run_time=0.8)

        # ========================================================== 6 · the model line: the LLM core (slide 35)
        hl = box(envc.frame.width - 0.3, envc.model_row.strut.height + 0.16, TURN, fill_opacity=0.12,
                 radius=0.08)
        lr = lref("35")
        with self.voiceover(SAY[6]) as vo:
            hl.move_to(envc.model_row.strut).set_x(envc.frame.get_center()[0])
            self.play(FadeOut(n5), FadeIn(hl), run_time=0.5)
            regroup(self, envc, add=[hl], at=1)            # over the frame, under the text
            vo.wait_until("Choosing the LLM core")
            self.play(FadeIn(lr), FadeOut(VGroup(web, ill)), run_time=0.6)
            self.play(envc.animate.move_to([0, envc.get_center()[1], 0]), run_time=0.8)
            vo.wait_until("and here it's one line")
            self.play(Indicate(envc.model_row, color=TURN, scale_factor=1.04), run_time=0.8)
            vo.wait_until("a current model")
            new_row = mono_line(f"GEMINI_MODEL={MODEL_RAG}", 22, INK)
            new_row.shift(envc.model_row.strut.get_corner(UP + LEFT) - new_row.strut.get_corner(UP + LEFT))
            new_val = substring(new_row, MODEL_RAG).set_color(DATA)
            old_val = envc.val
            envc.model_row.remove(*old_val)
            self.add(old_val)
            self.play(FadeOut(old_val, shift=DOWN * 0.35), run_time=0.45)
            self.play(FadeIn(new_val, shift=DOWN * 0.35), run_time=0.5)
            regroup(self, envc, add=[new_val])
            envc.val = new_val
            edit = grey_tag("your edit · the model llm-rag uses (cli.py · line 27)")
            place(edit, right=envc.frame.get_right()[0], top=envc.frame.get_bottom()[1] - 0.15)
            self.play(FadeIn(edit, shift=UP * 0.1), run_time=0.5)

        # ========================================================== 7 · retired models; one root .env; ▶
        ch1 = model_chip_row([("the code's fallback:", "s", INK), ("gemini-2.0-flash", "m", INK),
                              ("· shut down", "s", ERR)])
        src1 = VGroup(mono("1-baseline/agent.py", CAPTION, S.GREY), label("· line 12", CAPTION, S.GREY))
        src1.arrange(RIGHT, buff=0.12)
        ch2 = model_chip_row([("gemini-2.5-flash", "m", INK), ("· limited to earlier users", "s", ERR)])
        e1, e2 = erratum_tag(), erratum_tag()
        r1 = VGroup(ch1, src1, e1).arrange(RIGHT, buff=0.2)
        src7 = grey_tag("Google's model pages, checked October 18, 2026")
        r2 = VGroup(ch2, e2).arrange(RIGHT, buff=0.2)
        chips = VGroup(r1, r2, src7).arrange(DOWN, buff=0.11)
        place(chips, cx=0, top=envc.frame.get_bottom()[1] - 0.18)    # 0.35 clear of the strip
        dcard = nearest_card()
        place(dcard, cx=0, top=envc.frame.get_bottom()[1] - 0.4)
        card7 = turn_card([CLONE.cmd, CD.cmd, CP.cmd,
                           ("GOOGLE_API_KEY=<your key>", "in .env"),
                           (f"GEMINI_MODEL={MODEL_RAG}", "in .env"),
                           (Prose("the key stays in the git-ignored .env"), COST)], header=None)
        k7 = key_glyph(0.3).next_to(card7.rows[-1], RIGHT, buff=0.25)
        card7.add(k7)
        place(card7, cx=0, bottom=GAP_Y)
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(lr), FadeOut(edit), run_time=0.4)
            self.play(FadeIn(r1, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("as shut down")
            self.play(Indicate(ch1.row[-1], color=ERR, scale_factor=1.1), run_time=0.7)
            vo.wait_until("and limits 2.5 Flash")
            self.play(FadeIn(r2, shift=UP * 0.1), run_time=0.6)
            self.play(FadeIn(src7, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Keep everything in this root file")
            self.play(FadeOut(chips), run_time=0.4)
            self.play(FadeIn(dcard, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("only the nearest dot env")
            self.play(Indicate(dcard.nearest, color=LOOKUP, scale_factor=1.08), run_time=0.8)
            vo.wait_until("Pause, and set up yours")
            self.play(FadeOut(VGroup(envc, dcard)), run_time=0.4)
            self.play(FadeIn(card7, shift=UP * 0.15), run_time=0.6)
        self.wait(2)                                    # ▶ beat: hold the frame

        # ========================================================== 8 · pyproject.toml: >=3.10, no upper bound
        pp = src_panel(PYPROJECT, 8, 19)
        place(pp, left=-6.3, top=TOP_Y)
        bar8 = pp.bar(8, DATA, 0.22)
        bar10 = pp.bar(10, TURN, 0.22)
        bar18 = VGroup(pp.bar(18, S.GREY, 0.25), pp.bar(19, S.GREY, 0.25))
        nb = tag("no upper bound", TURN)
        place(nb, left=pp.get_right()[0] + 0.3, cy=bar10.get_center()[1])
        pulls = label("→ onnxruntime, PyTorch", 22, S.GREY)
        place(pulls, left=pp.get_right()[0] + 0.3, cy=bar18.get_center()[1])
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(card7), FadeOut(t), run_time=0.5)
            self.play(FadeIn(pp, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("Python 3.10 or newer")
            self.play(FadeIn(bar8), Indicate(pp.span(8, ">=3.10"), color=DATA, scale_factor=1.1), run_time=0.8)
            vo.wait_until("and ADK 1.8 or newer")
            self.play(FadeIn(bar10), Indicate(pp.span(10, ">=1.8.0"), color=TURN, scale_factor=1.1),
                      run_time=0.7)
            vo.wait_until("with no upper bound")
            self.play(FadeIn(nb, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("plus Chroma")
            self.play(FadeIn(bar18), run_time=0.5)
            self.play(FadeIn(pulls, shift=LEFT * 0.15), run_time=0.5)

        # ========================================================== 9 · V5: no Python on this laptop; ponder
        vl = VersionLine()
        vl.shift(UP * AXIS_Y)
        band_full = vl.band.copy()
        vl.band.stretch_to_fit_width(0.01).align_to(band_full, LEFT)
        line8 = pp.code.code_lines[0]
        for f in pp.get_family():
            if line8 in f.submobjects:
                f.remove(line8)
        nopy = excerpt_chip(ENV.line(9), "command -v python3 python", line=ENV.line(9))
        assert "command -v python3 python ||" in ENV.cmd, ENV.cmd
        hdr = mono("command -v python3 python", CAPTION, S.GREY)    # a command: mono, as everywhere
        hdr.move_to(nopy.header).align_to(nopy.header, LEFT)
        nopy.remove(nopy.header)
        nopy.add(hdr)
        nopy.header = hdr
        exn = extra_tag().next_to(nopy.header, RIGHT, buff=0.2)
        nopy.add(exn)
        place(nopy, left=0.6, bottom=vl.band.get_top()[1] + 0.12)
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(VGroup(pp, bar8, bar10, bar18, nb, pulls)),
                      ReplacementTransform(line8, vl.band_label), Create(vl.axis),
                      LaggedStart(*[FadeIn(tk, shift=UP * 0.1) for tk in vl.ticks], lag_ratio=0.1),
                      run_time=1.2)
            self.play(Transform(vl.band, band_full), run_time=0.8)
            self.remove(vl.axis, vl.band, vl.band_label, *vl.ticks)
            self.add(vl)
            vo.wait_until("no Python at all")
            self.play(FadeIn(nopy, shift=DOWN * 0.1), run_time=0.6)
        card9 = ponder_at(self, "This laptop has no Python at all.\nThe project asks for 3.10 or newer.\n"
                                "Which Python will uv sync use?", seconds=6)

        # ========================================================== 10 · uv sync: uv downloads the newest
        drop = vl.drop(15, "CPython 3.15.0")
        short = Arrow(vl.point(15, 0.85), vl.point(15, 0.15), buff=0, color=TOOL, stroke_width=5,
                      max_tip_length_to_length_ratio=0.3)      # clears the erratum tag of beat 12
        drop.remove(drop.arrow)
        drop.add_to_back(short)
        drop.arrow = short
        drop.text.next_to(drop.arrow, RIGHT, buff=0.15).set_y(drop.arrow.get_center()[1])
        with self.voiceover(SAY[10]) as vo:
            self.play(FadeOut(card9), FadeIn(t), tr.goto(6), run_time=0.6)
            resize(self, t, RUN_ROWS, run_time=0.6)
            vo.wait_until("uv sync")
            type_cmd(self, t, SYNC1.cmd, 0.4)
            vo.wait_until("As in lecture 1")
            out10 = t.print(self, SYNC1.at(2, 3, 4), run_time=0.6)
            using = out10[0]
            vo.wait_until("uv downloads the newest")
            self.play(FadeOut(nopy), GrowArrow(drop.arrow), run_time=0.6)
            self.play(FadeIn(drop.dot, scale=0.5), FadeIn(drop.text, shift=DOWN * 0.1), run_time=0.5)
            self.remove(drop.arrow, drop.dot, drop.text)
            self.add(drop)
            vo.wait_until("CPython 3.15.0")
            self.play(Indicate(substring(using, "CPython 3.15.0"), color=TOOL, scale_factor=1.1),
                      Indicate(drop.text, color=TOOL, scale_factor=1.08), run_time=0.8)
            vo.wait_until("at the time of recording")
            pin(self, using, beside(recording_tag(), t, using, buff=0.5), run_time=0.4)

        # ========================================================== 11 · the error: no cp315 wheel
        ws = WheelShelf(slot_w=1.05)
        place(ws, left=-6.35, bottom=GAP_Y + 0.15)
        chroma = excerpt_chip(CHROMA_LINE.strip(), "pyproject.toml · line 18", line=CHROMA_LINE)
        place(chroma, right=6.3, top=1.0)
        title = ws.parts["title"]
        pull_arrow = Arrow(chroma.chip.get_left(), title.get_right() + RIGHT * 0.05, buff=0.15,
                           color=S.GREY, stroke_width=3, max_tip_length_to_length_ratio=0.12, tip_length=0.18)
        pull_l = label("pulls in", CAPTION, S.GREY).next_to(pull_arrow.get_center(), UP, buff=0.12)
        with self.voiceover(SAY[11]) as vo:
            self.play(Indicate(out10[2], color=TURN, scale_factor=1.04), run_time=0.7)
            vo.wait_until("then fails")
            assert t.max_chars == 65, t.max_chars
            err = t.print(self, [(r, ERR) for r in ERR_ROWS + HINT_ROWS], run_time=0.9)
            hint_rows = list(err)[-3:]
            assert hint_rows[0].text.startswith("hint:"), [r.text for r in err]
            vo.wait_until("O-N-N-X runtime")
            self.play(Indicate(substring(hint_rows[0], "`onnxruntime`"), color=TURN, scale_factor=1.1),
                      run_time=0.8)
            vo.wait_until("which Chroma pulls in")
            resize(self, t, 3, keep=hint_rows, run_time=0.5)
            self.play(FadeIn(ws, shift=UP * 0.1), FadeIn(chroma, shift=LEFT * 0.1), run_time=0.6)
            self.play(GrowArrow(pull_arrow), FadeIn(pull_l), run_time=0.5)
            vo.wait_until("has wheels only up to Python 3.14")
            self.play(LaggedStart(*[Indicate(ws.wheel(w), color=TURN, scale_factor=1.1) for w in WHEEL_TAGS],
                                  lag_ratio=0.12), run_time=1.2)
            self.play(*ws.missing(), Indicate(drop.dot, color=ERR, scale_factor=1.4), run_time=0.7)

        # ========================================================== 12 · fails whenever uv picks 3.15; the pin
        err_tr = grey_tag("erratum · fails whenever uv picks 3.15")
        cap_x = caption_extra(tracker("Start", 6), True).target_mobject     # " · extra" comes later
        place(err_tr, left=cap_x.get_right()[0] + 0.3, cy=tr.get_center()[1])
        n12 = VGroup(note("uv tries the Pythons it downloaded"), note("before the system's (as in lecture 1):"),
                     note("a uv-managed 3.15 wins"), note("over a system 3.12"))
        n12.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        place(n12, left=ws.get_right()[0] + 0.4, cy=ws.get_center()[1] + 0.2)
        pv = pyver_card()
        place(pv, left=ws.get_right()[0] + 0.8, cy=ws.get_center()[1] - 0.05)
        with self.voiceover(SAY[12]) as vo:
            self.play(FadeOut(VGroup(chroma, pull_arrow, pull_l)), run_time=0.4)
            self.play(FadeIn(err_tr, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("on a fresh laptop")
            self.play(Indicate(drop.text, color=ERR, scale_factor=1.08), run_time=0.8)
            vo.wait_until("or where uv already has 3.15")
            self.play(FadeIn(n12, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("even beside an older Python")
            self.play(Indicate(VGroup(n12[2], n12[3]), color=TURN, scale_factor=1.04), run_time=0.8)
            vo.wait_until("The fix")
            self.play(caption_extra(tr, True), FadeOut(n12), run_time=0.4)
            type_cmd(self, t, PIN.cmd, 0.6)
            o12 = t.print(self, [PIN.line(2)], run_time=0.3)[0]
            ft = VGroup(fix_tag(), extra_tag()).arrange(RIGHT, buff=0.2)
            pin(self, o12, beside(ft, t, o12, buff=0.5), run_time=0.4)
            vo.wait_until("uv python pin 3.13")
            self.play(*vl.collapse(13, "pinned: 3.13"), drop.animate.set_opacity(0.3), run_time=0.8)
            self.play(*ws.click("cp313"), FadeIn(pv, shift=DOWN * 0.3), run_time=0.7)
        self.wait(1.2)                                  # the pinned picture, before it leaves

        # ========================================================== 13 · uv sync again: 3.13, it installs
        sc = size_card()
        with self.voiceover(SAY[13]) as vo:
            self.play(FadeOut(VGroup(vl, drop, ws, pv, err_tr)), caption_extra(tr, False), run_time=0.6)
            resize(self, t, 12, run_time=0.6)
            vo.wait_until("Then uv sync again")
            type_cmd(self, t, SYNC2.cmd, 0.4)
            vo.wait_until("CPython 3.13 this time")
            o13 = t.print(self, SYNC2.at(2, 3, 4), run_time=0.5)
            self.play(substring(o13[0], "CPython 3.13.16").animate.set_color(DATA), run_time=0.5)
            vo.wait_until("and it installs")
            o13b = t.print(self, SYNC2.at("", 38, "", 89, "", 155), run_time=0.8)
            adk_row, onnx_row = o13b[1], o13b[3]
            vo.wait_until("ADK 2.12.0 included")
            self.play(substring(adk_row, "google-adk==2.12.0").animate.set_color(DATA),
                      substring(onnx_row, "onnxruntime==1.31.0").animate.set_color(DATA), run_time=0.6)
            self.play(Indicate(substring(adk_row, "google-adk==2.12.0"), color=DATA, scale_factor=1.08),
                      run_time=0.7)
            place(sc, right=t.box.get_right()[0] - 0.15, top=-1.0)   # inside the frame, over short rows only
            r0 = sc.rows[0]                                 # the card starts as large as its first row
            fr1 = box(r0.width + 0.6, r0.height + 0.5, S.GREY, fill=S.BG, fill_opacity=0.97, radius=0.14)
            place(fr1, left=sc.frame.get_left()[0], top=sc.frame.get_top()[1])
            vo.wait_until("PyTorch makes it big")
            self.play(FadeIn(fr1), FadeIn(r0, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("plus about 3 gigabytes")
            self.play(Transform(fr1, sc.frame), FadeIn(sc.rows[1], shift=UP * 0.1), run_time=0.6)
            self.play(FadeIn(sc.rows[2], shift=UP * 0.1), run_time=0.5)
            sc.remove(sc.frame)                             # fr1 now draws the frame: it leaves with sc
            sc.add_to_back(fr1)
            sc.frame = fr1

        # ========================================================== 14 · uv run adk --version; ▶
        card14 = turn_card([CD.cmd, CP.cmd, Prose("your key + GEMINI_MODEL in .env"),
                            (PIN.cmd, "extra"), SYNC2.cmd], header=None)
        place(card14, cx=0, bottom=GAP_Y)
        with self.voiceover(SAY[14]) as vo:
            self.play(FadeOut(sc), caption_extra(tr, True), run_time=0.5)
            c14 = type_cmd(self, t, VER.cmd, 0.9)
            o14 = t.print(self, [VER.line(2)], run_time=0.4)[0]
            ex14 = beside(extra_tag(), t, o14, buff=0.5)
            pin(self, o14, ex14, run_time=0.3)
            vo.wait_until("says 2.12.0")
            self.play(Indicate(substring(o14, "2.12.0"), color=TURN, scale_factor=1.15), run_time=0.7)
            vo.wait_until("at the time of recording")
            rec14 = recording_tag().next_to(ex14, RIGHT, buff=0.2)
            pin(self, o14, rec14, run_time=0.4)
            p14 = bare_prompt(self, t)
            resize(self, t, 3, keep=[c14, o14, p14], run_time=0.6)
            vo.wait_until("Pause, and get your sync to succeed")
            self.play(FadeIn(card14, shift=UP * 0.15), run_time=0.6)
        self.wait(2)                                    # ▶ beat: hold the frame
        self.play(FadeOut(VGroup(card14, t, tr)), run_time=0.8)
        self.wait(0.3)
