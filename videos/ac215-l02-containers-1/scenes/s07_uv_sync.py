"""S07 · Step 4: uv sync, and two Pythons (README A10, V4: the number line and the PATH doors, V2: the
GREEN slab).

Beats (script.md "## S07", one voiceover block each):
 0  TRACKER A9 -> A10. A README card (`README.md · line 155`, "Setup a virtual environment by running
    uv sync") over CODE(README.md: 157); on "RUN uv sync" the line turns GREEN on a GREEN bar; "add it
    at the end, and save": the panel is circled YELLOW. "Like on last lecture's VM": a small flow
    under the panel, a GREY "as in lecture 1" tag, then `pyproject.toml` (file chip) -> PURPLE
    `uv sync` -> GREEN "venv + packages", each part as it is said.
 1  The card, panel and flow leave; the `uv sync` chip moves to the middle. CODE(Dockerfile.txt: 2)
    beside CODE(pyproject.toml: 6): `3.12` ORANGE + underline on "This image's Python is 3.12",
    `>=3.13` GREEN + underline on "asks for 3.13 or newer". "What will uv sync do": a YELLOW "?"
    next to the chip and three GREY answer chips "fail?", "use 3.12 anyway?", "something else?".
    PONDER (8 s): the card covers the panels and the question, the answers stay visible under it.
 2  TRACKER A10. Full terminal (12 rows): `docker build -t simple-translate -f Dockerfile .` (two
    rows) + ▶ your turn -> laptop/21 lines 23–24, 26–27. "the pip step says CACHED": `#6 CACHED`
    TEAL; "but COPY says DONE": `#7 DONE 0.1s` on a YELLOW bar, row tag "COPY ran again · part 2"
    (GREY); it pulses on "Keep that question".
 3  The terminal continues: "Now the answer" -> lines 29, 30 (wraps onto 2 rows); "As on the Debian
    12 VM": a PURPLE bar over both rows of line 30, `cpython-3.15.0` pulses PURPLE; "its own
    Python": GREY row tag "Apple Silicon: …linux-aarch64-gnu" beside the wrapped row; "CPython
    3.15.0" -> line 32, `3.15.0` underlined + row tag "at the time of recording"; "Then it creates
    a venv" -> lines 33–34, `/.venv` GREEN; "and installs 11 packages" -> 36–37, …, 47,
    `Installed 11 packages` GREEN.
 4  The terminal shrinks to the 3-row strip (line 29 and the two rows of line 30). V4 full width
    above it: axis and ticks 3.10 … 3.16; "the requirement covers": the GREEN glow from 3.13 grows
    with `requires-python = ">=3.13"`. "The base image's 3.12": an ORANGE dot drops on 3.12, label
    `3.12.15` / "base image"; "falls outside": RED cross. "so uv downloads": a PURPLE `uv` chip
    (top right), a PURPLE arrow, a GREEN dot rides it down to 3.15, label `3.15.0` / "uv download ·
    35.9 MiB"; "the newest stable": tag "newest stable · at the time of recording" beside the uv
    chip; "and the python in the venv": GREEN chip `/.venv/bin/python` (below right); "links to
    it": a GREEN link arrow to the dot. After the sentence the number line fades except the GREEN dot; the V2 stack
    (S06's: four thin ORANGE base slabs, brace "base image", caption `python:3.12-slim-bookworm`,
    ORANGE `RUN pip install uv` with its PURPLE uv chip, GREY `COPY . ./` with file glyphs, the
    dashed slot "packages: none yet") slides in from the right; a copy of the strip's `RUN uv sync`
    (line 29) travels along its empty row and up the clear column right of the stack to meet the
    GREEN dot beside the slot, and the two fly into the slot as the fat GREEN slab "RUN uv sync"
    (a straight flight would cut through the base slabs); GREY note "CPython 3.15.0 + /.venv" /
    "11 packages". The link holds 0.5 s, then the line fades and the stack comes in quickly; the
    finished stack and its note hold 2 s in silence before the run (about 3.9 s past the sentence).
 5  TRACKER A10. The picture and the strip go; full wide terminal (13.2 wide, 20 pt, 13 rows):
    `docker run --rm \\` / `    -ti simple-translate` (folded as in S04/S05/S06/S08/S09: it would
    fill its row) + ▶ your turn beside its second row -> TRACKER A10 · extra, `ls -a` (row tag
    `extra`) at the capture's prompt `root@01dca6d0f4d8:/#`, its `-a` pulses YELLOW on "which also
    lists hidden files" -> laptop/22 lines 3–9; `.venv` and `uv.lock` GREEN as they are said.
    "But python cli.py" -> `python cli.py` (row tag `extra`) -> lines 11–14 RED, the prompt
    returns; "Why?": the ModuleNotFoundError row pulses. The `your turn` tag belongs to the
    command's second row: it scrolls away with it (2 + 1 + 7 + 1 + 4 + 1 rows in 13).
 6  V4's PATH half. The terminal shrinks to the strip (the `python cli.py` row, the RED line, the
    prompt). The base image's `ENV PATH=/usr/local/bin:/usr/local/sbin:/usr…` (laptop/34 line 22)
    as a GREY chip top right; its three parts are copied down into three doors: `/usr/local/bin`
    (ORANGE), `/usr/local/sbin`, `…`; the chip's `PATH` pulses PINK on "activation is just PATH".
    "Nothing has activated the venv": caption "venv not activated" (GREY). "so the word python":
    the PINK `python` figure appears over the first door and walks in (the door fills ORANGE),
    `/usr/local/bin` pulses; "from the base image": the figure walks down to the ORANGE dot
    `3.12.15`. "That's 3.12" pulses it; "none of our packages": RED "no art, no googletrans", the
    figure turns RED, the strip's RED line pulses.
 7  The RED figure and note go; the caption becomes "venv activated" (GREEN); "put its bin folder
    in front": a GREEN `/.venv/bin` door drops in at the front (the other doors and the ORANGE dot
    make room); "and python would find 3.15.0": a new figure walks in through it, down to the GREEN
    dot `3.15.0`. "Two extra checks": the strip grows to 5 rows (TRACKER A10 · extra):
    `.venv/bin/python --version` (row tag `extra`) -> laptop/22 line 16, `3.15.0` GREEN with the
    dot; `source .venv/bin/activate && python cli.py` (row tag `extra`) -> lines 28, 30–31 (it
    scrolls; `Output: Adoro il formaggio` GREEN stays); "The prompt now shows app": the prompt
    `(app) root@01dca6d0f4d8:/#` (line 32), `(app)` GREEN pulses, GREY row tag `pyproject.toml ·
    line 2: name = "app"` beside it (why "app", not "simple-translate"; it fades before typing);
    "Type exit" -> `exit`, line 33, the laptop prompt returns.
 8  TRACKER A10. The strip and the doors go; the two dots move up side by side with two-line labels:
    ORANGE `3.12.15` / "base · only ran pip install uv", GREEN `3.15.0` / "uv download · runs the
    app" (each as it is said). "half of the opening puzzle": S01's `3.12` YELLOW "?" GREY `3.14.7`
    returns, with "half solved". "a small mismatch": tag `erratum` and the sources (README.md ·
    line 133, Dockerfile.txt · line 2 vs pyproject.toml · line 6). "In your own projects": two GREEN
    fix chips, `FROM python:3.13-slim-bookworm` and "or a requires-python the image already
    meets". Fade out to an empty frame.

Deviations from SHOW (see the scene report): the slab's text is copied from the strip's
`#8 [4/4] RUN uv sync` (the README panel is not on screen in beat 4); the 3.15 dot's "newest
stable" tag sits beside the uv chip, and `/.venv/bin/python` below the line (the band label leaves
no room above the dot for both).
"""

import numpy as np  # noqa: I001  (manim first, then common: common must win)
from manim import *

from explainer import style as S
from explainer.devops import code_span, line_bar
from explainer.scene import VoiceScene

from common import (BUILD, ERR, IMAGE, INK, LAPTOP, LAPTOP_DIR, MONO, NARRATION, P_LAPTOP, ROUTE,
                    RUN, STRIP_ROWS, SYSTEM, TOOL, TURN, VENV, VM12, LayerStack, PathDoors,
                    VersionLine, attach, bare_prompt, beside, box, capture, chip, code, cross_mark,
                    erratum_tag, excerpt, figure, file_glyph, folder_glyph, glyph_range, hl_bar, istep,
                    label, laptop_term, mono, mono_line, outline_box, pin, readme_card, resize, row_tag,
                    steady, substring, tag, track, tracker_a, type_cmd, under, unpin, wide_term)

SAY = NARRATION["S07"]

# ------------------------------------------------------------------ real outputs (file line numbers)
C21 = capture("21", LAPTOP_DIR)                          # laptop/21-build-v4.txt
assert C21.cmd == BUILD, C21.cmd
BUILD_A = C21.at((23, 24), (26, 27))                     # [2/4] RUN pip install uv · CACHED · COPY · DONE
assert BUILD_A[1] == "#6 CACHED" and BUILD_A[3] == "#7 DONE 0.1s", BUILD_A
BUILD_B = C21.at(29, 30)                                 # [4/4] RUN uv sync · Downloading cpython (wraps)
assert BUILD_B[0] == "#8 [4/4] RUN uv sync" and "cpython-3.15.0-linux-x86_64-gnu" in BUILD_B[1]
assert BUILD_B[1].endswith("(35.9MiB)"), BUILD_B[1]
BUILD_C = C21.at(32)                                     # Using CPython 3.15.0
assert BUILD_C == ["#8 3.842 Using CPython 3.15.0"], BUILD_C
BUILD_D = C21.at((33, 34))                               # Creating virtual environment at: /.venv · Resolved
assert BUILD_D[0].endswith("Creating virtual environment at: /.venv"), BUILD_D
BUILD_E = C21.at((36, 37), "…", 47)                      # Installed 11 packages · + anyio · … · + idna
assert "Installed 11 packages" in BUILD_E[0] and BUILD_E[-1].endswith("+ idna==3.20"), BUILD_E

C22 = capture("22", LAPTOP_DIR)                          # laptop/22-run-v4.txt
assert C22.cmd == RUN, C22.cmd
# beat 5: the run command folded as S04/S05/S06/S08/S09 show it (it would fill the wide row, leaving no
# room for ▶ your turn); the house fold " \" + 4-space indent pastes back as the same command
RUN_ROWS = [P_LAPTOP + " docker run --rm \\", "    -ti simple-translate"]
assert RUN_ROWS[0][:-2] + " " + RUN_ROWS[1].strip() == P_LAPTOP + " " + RUN, RUN_ROWS
LS_LINE = C22.line(2)                                    # root@01dca6d0f4d8:/# ls -a
C_PROMPT, _ls = C22.istep(2)
assert (C_PROMPT, _ls) == ("root@01dca6d0f4d8:/#", "ls -a"), LS_LINE
LS_OUT = C22.at((3, 9))
assert LS_OUT[5].startswith(".venv") and LS_OUT[4].endswith("uv.lock"), LS_OUT
PY_LINE = C22.line(10)
assert C22.istep(10)[1] == "python cli.py", PY_LINE
PY_ERR = C22.at((11, 14))
assert PY_ERR[3] == "ModuleNotFoundError: No module named 'art'", PY_ERR
VER_LINE = C22.line(15)
assert C22.istep(15)[1] == ".venv/bin/python --version", VER_LINE
VER_OUT = C22.at(16)
assert VER_OUT == ["Python 3.15.0"], VER_OUT
SRC_LINE = C22.line(17)
assert C22.istep(17)[1] == "source .venv/bin/activate && python cli.py", SRC_LINE
SRC_OUT = C22.at(28, (30, 31))
assert SRC_OUT[0].startswith("Arguments: Namespace(") and SRC_OUT[2] == "Output: Adoro il formaggio", SRC_OUT
EXIT_LINE = C22.line(32)
APP_PROMPT, _ex = C22.istep(32)
assert (APP_PROMPT, _ex) == ("(app) root@01dca6d0f4d8:/#", "exit"), EXIT_LINE
EXIT_ECHO = C22.at(33)
assert EXIT_ECHO == ["exit"], EXIT_ECHO
APP_NAME = excerpt("pyproject.toml", 2, 2)               # where the prompt's (app) comes from
assert APP_NAME == 'name = "app"' and APP_PROMPT.startswith("(app) "), APP_NAME

_hist = capture("34", LAPTOP_DIR).line(22)               # the base image's ENV PATH row (docker history)
ENV_PATH = _hist[_hist.index("ENV PATH="):_hist.index("…") + 1]
assert ENV_PATH == "ENV PATH=/usr/local/bin:/usr/local/sbin:/usr…", ENV_PATH
BASE_PY = capture("33", LAPTOP_DIR).line(11)             # /usr/local/bin/python --version
assert BASE_PY == "Python 3.12.15", BASE_PY
VM_PY = capture("06", VM12).line(29)                     # S01: the instructor's image on the VM
assert VM_PY == "Python 3.14.7", VM_PY
V_BASE, V_UV, V_VM = BASE_PY.split()[1], VER_OUT[0].split()[1], VM_PY.split()[1]

# ------------------------------------------------------------------ layout
AX_Y = 0.45                           # beat 4: the number line (full width, 11 units)
STACK_X, FLOOR_Y = -1.2, -0.25        # the V2 stack where S06 left it (3.2 wide)
UP_X = 2.75                           # beat 4: the clear column right of the stack the slab text rises in
DOOR_LEFT, DOOR_TOP, DOOR_H = -6.0, 1.75, 0.95  # beats 6-7: the PATH doors
DEST_Y = -0.1                         # beats 6-7: the Pythons the doors lead to (clear of a 5-row strip)
DEST_DX = 1.55                        # a destination dot sits this far right of its door's left edge
PONDER_Q = ("This image's Python is 3.12.\npyproject.toml asks for 3.13 or newer.\n"
            "What will uv sync do during the build?")


# ------------------------------------------------------------------ helpers
def turn_tag() -> VGroup:
    """YELLOW '▶ your turn', the height of a terminal row."""
    return row_tag("▶ your turn", TURN)


def type_rows(scene, t, rows_text: list[str], type_time: float) -> VGroup:
    """type_cmd with rows folded by the caller (rows_text[0] starts with the prompt; a bare prompt
    line is replaced, as type_cmd does). Returns the rows (.rows). As S05/S06's type_rows."""
    p = t.prompt + " "
    assert rows_text[0].startswith(p) and all(len(s) <= t.max_chars for s in rows_text)
    if len(t.lines) and getattr(t.lines[-1], "bare", False):
        last = t.lines[-1]
        scene.remove(last, *last.submobjects)
        t.lines.remove(last)
    t2c = t._prompt_colors(t.prompt)
    t._make_room(scene, len(rows_text))
    rows = []
    for k, s in enumerate(rows_text):
        ln = mono_line(s, t.size, INK, t2c=t2c if k == 0 else None)
        t._place(ln, len(t.lines))
        t.lines.add(ln)
        rows.append(ln)
    typed = [glyph_range(rows[0], len(p))] + [glyph_range(r, 0) for r in rows[1:]]
    scene.add(glyph_range(rows[0], 0, len(p)))
    scene.play(ShowIncreasingSubsets(VGroup(*[g for grp in typed for g in grp]), rate_func=linear),
               run_time=type_time)
    for r in rows:
        scene.add(r)
    g = VGroup(*rows)
    g.rows, g.text = rows, " ".join(r.text for r in rows)
    return g


def bar_on(scene, row, glyphs, color, opacity: float = 0.25):
    """A translucent bar behind `glyphs` of terminal row `row` (part of the row: it scrolls with it)."""
    b = hl_bar(glyphs, color, opacity)
    row.add_to_back(b)
    scene.add(row)
    return b


def text_span(t: Text, s: str, sub: str) -> VGroup:
    """Glyphs of `sub` in a Text built from string `s` (spaces have no glyphs)."""
    i = s.index(sub)
    a = len("".join(s[:i].split()))
    n = len("".join(sub.split()))
    return VGroup(*t.submobjects[a:a + n])


def file_chip(name: str, color) -> VGroup:
    """A file glyph and its name in a box."""
    g = VGroup(file_glyph(0.3, color), mono(name, 22, color)).arrange(RIGHT, buff=0.14)
    frame = box_around(g, color)
    return VGroup(frame, g)


def box_around(g, color, pad_x: float = 0.22, pad_y: float = 0.14):
    return box(g.width + 2 * pad_x, g.height + 2 * pad_y, color, fill_opacity=0.08).move_to(g)


def flow_arrow(a, b, color=S.GREY) -> Arrow:
    return Arrow(a.get_right(), b.get_left(), buff=0.15, color=color, stroke_width=4, tip_length=0.18,
                 max_tip_length_to_length_ratio=0.3)


def copy_slab(stack: LayerStack):
    """S06's GREY `COPY . ./` slab with a row of file glyphs (a folder for .git/ first) beside its text
    (here three files, so the row stays inside the slab)."""
    s = stack.make("COPY . ./", LAPTOP)
    glyphs = VGroup(folder_glyph(0.22, LAPTOP), *[file_glyph(0.26, LAPTOP) for _ in range(3)])
    glyphs.arrange(RIGHT, buff=0.1)
    s.text.shift(LEFT * 0.75)
    glyphs.next_to(s.text, RIGHT, buff=0.25).set_y(s.box.get_center()[1])
    assert glyphs.get_right()[0] < s.box.get_right()[0] - 0.1
    s.add(glyphs)
    s.glyphs = glyphs
    return s


def dest(color, version: str) -> VGroup:
    """A Python a door leads to: a dot and its version (mono). .dot .text"""
    d = Dot(radius=0.12, color=color)
    t = mono(version, 22, color).next_to(d, RIGHT, buff=0.18)
    g = VGroup(d, t)
    g.dot, g.text = d, t
    return g


def place_dest(g: VGroup, door) -> VGroup:
    g.shift(np.array([door.frame.get_left()[0] + DEST_DX, DEST_Y, 0]) - g.dot.get_center())
    return g


def two_line(top: str, bottom: str, color) -> VGroup:
    """Version (mono, in its colour) over a short role (GREY), centred."""
    return VGroup(mono(top, 22, color), label(bottom, 22, S.GREY)).arrange(DOWN, buff=0.1)


# ------------------------------------------------------------------ the scene
class StepUvSync(VoiceScene):
    def ponder_over(self, question: str, seconds: float, over_w: float, over_h: float, center) -> VGroup:
        """The toolkit's ponder card (pause_and_ponder's look and timer) sized to cover a region, so the
        answer chips under it stay visible. Returns the card (removed at the start of the next block)."""
        from explainer.components import ponder_card
        card = ponder_card(question, width=over_w)
        fr, head, q, bar = card
        new_fr = RoundedRectangle(width=over_w, height=over_h, corner_radius=0.2, stroke_color=TURN,
                                  stroke_width=3).set_fill(S.BG, 1).move_to(center)
        fr.become(new_fr)
        VGroup(head, q).move_to(new_fr).shift(UP * 0.12)
        bar.put_start_and_end_on(new_fr.get_corner(DL) + np.array([0.3, 0.25, 0]),
                                 new_fr.get_corner(DR) + np.array([-0.3, 0.25, 0]))
        self.play(FadeIn(card, scale=0.95), run_time=0.6)
        self.play(bar.animate(rate_func=linear).become(bar.copy().scale(0.001, about_point=bar.get_start())),
                  run_time=seconds)
        return card

    def construct(self):
        assert len(SAY) == 9, f"S07 has {len(SAY)} SAY lines; this scene times 9"

        tr = tracker_a(9)

        # ========================================================== 0 · Step 4: RUN uv sync
        card = readme_card(155, "Setup a virtual environment by running uv sync")
        card.move_to([0, 1.6, 0])
        panel = code("README.md", 157, language="docker")
        panel.move_to([0, 0.05, 0])
        p_line = code_span(panel.code, 0, "RUN uv sync")
        p_bar = line_bar(panel.code, 0, VENV, 0.2)
        l1 = tag("as in lecture 1", S.GREY)
        toml = file_chip("pyproject.toml", S.GREY)
        uvc = chip("uv sync", TOOL, size=24, font=MONO)
        venv = chip("venv + packages", VENV, size=24)
        flow = VGroup(l1, toml, uvc, venv).arrange(RIGHT, buff=0.75)
        flow.move_to([0, -1.75, 0])
        a_read = flow_arrow(toml, uvc)
        a_inst = flow_arrow(uvc, venv, VENV)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.1), run_time=0.3)
            self.play(track(tr, 10), FadeIn(card, shift=DOWN * 0.1), FadeIn(panel, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("adds RUN uv sync")
            # the translucent bar goes on top of the panel (re-adding panel.code would put the code's
            # opaque background over it, as line_bar's docstring warns)
            self.play(FadeIn(p_bar), p_line.animate.set_color(VENV), run_time=0.5)
            self.play(Indicate(p_line, color=VENV, scale_factor=1.12), run_time=0.6)
            vo.wait_until("add it at the end")
            self.play(Circumscribe(panel, color=TURN, buff=0.08, stroke_width=4), run_time=1.0)
            vo.wait_until("Like on last")
            self.play(FadeIn(l1, shift=RIGHT * 0.1), run_time=0.4)
            vo.wait_until("it reads")
            self.play(FadeIn(uvc, scale=0.8), run_time=0.4)
            self.play(FadeIn(toml, shift=RIGHT * 0.1), GrowArrow(a_read), run_time=0.5)
            vo.wait_until("and installs")
            self.play(GrowArrow(a_inst), FadeIn(venv, shift=RIGHT * 0.15), run_time=0.6)
            self.play(Indicate(venv, color=VENV, scale_factor=1.1), run_time=0.6)

        # ========================================================== 1 · predict
        pd = code("Dockerfile.txt", 2)
        pt = code("pyproject.toml", 6)
        panels = VGroup(pd, pt).arrange(RIGHT, buff=0.5).move_to([0, 1.5, 0])
        g312 = code_span(pd.code, 0, "3.12")
        g313 = code_span(pt.code, 0, ">=3.13")
        u312 = under(g312, SYSTEM)
        u313 = under(g313, VENV)
        uvq = uvc.copy().move_to([-0.35, 0.05, 0])
        qm = label("?", 40, TURN).next_to(uvq, RIGHT, buff=0.2)
        during = label("during the build", 24, S.GREY).next_to(qm, RIGHT, buff=0.3)
        answers = VGroup(*[chip(s, S.GREY, size=24) for s in ("fail?", "use 3.12 anyway?", "something else?")])
        answers.arrange(RIGHT, buff=0.6).move_to([0, -1.85, 0])

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(card, panel, p_bar, l1, toml, a_read, a_inst, venv)),
                      uvc.animate.move_to(uvq), run_time=0.6)
            self.play(FadeIn(panels, shift=DOWN * 0.15), run_time=0.6)
            vo.wait_until("This image's Python")
            self.play(g312.animate.set_color(SYSTEM), Create(u312), run_time=0.5)
            self.play(Indicate(g312, color=SYSTEM, scale_factor=1.25), run_time=0.7)
            vo.wait_until("and line 6")
            self.play(Indicate(pt.header, color=INK, scale_factor=1.1), run_time=0.7)
            vo.wait_until("asks for 3.13")
            self.play(g313.animate.set_color(VENV), Create(u313), run_time=0.5)
            self.play(Indicate(g313, color=VENV, scale_factor=1.2), run_time=0.7)
            vo.wait_until("What will uv sync")
            self.play(FadeIn(qm, scale=1.5), FadeIn(during, shift=LEFT * 0.1), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(a, shift=DOWN * 0.1) for a in answers], lag_ratio=0.3), run_time=1.0)

        pcard = self.ponder_over(PONDER_Q, 8, 12.4, 3.5, [0, 0.55, 0])

        # ========================================================== 2 · build: CACHED, then COPY again
        t = laptop_term(12)

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(pcard, panels, u312, u313, uvc, qm, during, answers)), FadeIn(t), run_time=0.45)
            bare_prompt(self, t)
            c2 = type_cmd(self, t, BUILD, 0.8)
            assert len(c2.rows) == 2, "BUILD folds onto two rows"
            yt2 = beside(turn_tag(), c2.rows[0])
            pin(self, c2.rows[0], yt2, run_time=0.35)
            self.play(Wiggle(yt2, scale_value=1.15, rotation_angle=0.025 * TAU), run_time=0.5)
            vo.wait_until("First, notice")
            o2 = t.print(self, BUILD_A, run_time=0.5, lag=0.15)
            r24, r27 = o2[1], o2[3]
            vo.wait_until("the pip step")
            self.play(r24.glyphs.animate.set_color(IMAGE), run_time=0.3)
            self.play(Indicate(r24.glyphs, color=IMAGE, scale_factor=1.15), run_time=0.6)
            vo.wait_until("but COPY says")
            b27 = bar_on(self, r27, r27.glyphs, TURN, 0.25)
            self.play(FadeIn(b27), Indicate(r27.glyphs, color=TURN, scale_factor=1.15), run_time=0.6)
            vo.wait_until("it ran again")
            note27 = beside(row_tag("COPY ran again · part 2"), r27)
            pin(self, r27, note27, run_time=0.4)
            vo.wait_until("Keep that question")
            self.play(Wiggle(note27, scale_value=1.12, rotation_angle=0.02 * TAU), run_time=0.8)

        # ========================================================== 3 · the answer: uv downloads a Python
        with self.voiceover(SAY[3]) as vo:
            o3 = t.print(self, BUILD_B, run_time=0.5, wrap=True, lag=0.15)
            r29, r30a, r30b = o3
            assert len(o3) == 3 and r30b.text == "35.9MiB)", [r.text for r in o3]
            vo.wait_until("As on the Debian")
            b30a = bar_on(self, r30a, glyph_range(r30a, 9), TOOL, 0.22)
            b30b = bar_on(self, r30b, r30b.glyphs, TOOL, 0.22)
            g_cpy = substring(r30a, "cpython-3.15.0")
            self.play(FadeIn(b30a), FadeIn(b30b), run_time=0.4)
            vo.wait_until("uv downloads its own")
            self.play(Indicate(g_cpy, color=TOOL, scale_factor=1.1), run_time=0.7)
            arm = beside(row_tag([("Apple Silicon:", "label"), ("…linux-aarch64-gnu", "mono")]), r30b)
            pin(self, r30b, arm, run_time=0.4)
            vo.wait_until("CPython 3.15.0")
            r32 = t.print(self, BUILD_C, run_time=0.3)[0]
            g_v = substring(r32, "3.15.0")
            u_v = under(g_v, INK, y=r32.strut.get_bottom()[1] - 0.01)
            self.play(Create(u_v), Indicate(g_v, color=INK, scale_factor=1.2), run_time=0.6)
            attach(self, r32, u_v)
            vo.wait_until("at the time of recording")
            rec = beside(row_tag("at the time of recording"), r32)
            pin(self, r32, rec, run_time=0.4)
            vo.wait_until("Then it creates")
            o3d = t.print(self, BUILD_D, run_time=0.4, lag=0.2)
            g_venv = substring(o3d[0], "/.venv")
            self.play(g_venv.animate.set_color(VENV), run_time=0.3)
            self.play(Indicate(g_venv, color=VENV, scale_factor=1.25), run_time=0.6)
            vo.wait_until("and installs 11")
            o3e = t.print(self, BUILD_E, run_time=0.5, lag=0.12)
            g_inst = substring(o3e[0], "Installed 11 packages")
            self.play(g_inst.animate.set_color(VENV), run_time=0.3)
            self.play(Indicate(g_inst, color=VENV, scale_factor=1.1), run_time=0.6)

        # ========================================================== 4 · V4: the number line, then the slab
        vl = VersionLine(10, 16, lo=13, line_w=11.0)
        vl.shift(UP * AX_Y)
        band_full = vl.band.copy()
        o_dot = Dot(vl.point(12), radius=0.12, color=SYSTEM)
        o_lab = two_line(V_BASE, "base image", SYSTEM).next_to(o_dot, UP, buff=0.32)
        o_x = cross_mark(0.46, ERR, stroke=6).move_to(o_dot)
        uv_chip = chip("uv", TOOL, size=24, font=MONO)
        uv_chip.move_to([6.4 - uv_chip.width / 2, 2.3, 0])
        newest = tag("newest stable · at the time of recording", S.GREY)
        newest.next_to(uv_chip, LEFT, buff=0.25)
        g_end = vl.point(15)
        g_dot = Dot(radius=0.12, color=VENV).move_to(uv_chip.get_bottom() + DOWN * 0.15)
        drop = Arrow(uv_chip.get_bottom() + LEFT * 0.1, g_end + np.array([0.12, 0.12, 0]), buff=0.05,
                     color=TOOL, stroke_width=5, tip_length=0.22, max_tip_length_to_length_ratio=0.15)
        g_lab = two_line(V_UV, "uv download · 35.9 MiB", VENV).next_to(Dot(g_end), UP, buff=0.32)
        vpy = chip("/.venv/bin/python", VENV, size=22, font=MONO)
        vpy.move_to([6.45 - vpy.width / 2, AX_Y - 1.08, 0])
        # the link threads the gap between the 3.15 and 3.16 tick labels (through x = 3.92 at the
        # labels' height) and reaches the dot from below right
        link_end = g_end + np.array([0.1, -0.06, 0])
        gap_pt = np.array([(vl.ticks[5][1].get_right()[0] + vl.ticks[6][1].get_left()[0]) / 2,
                           vl.ticks[5][1].get_center()[1], 0])
        k = (vpy.get_top()[1] - link_end[1]) / (gap_pt[1] - link_end[1])
        link_start = link_end + k * (gap_pt - link_end)
        assert abs(link_start[0] - vpy.get_center()[0]) < vpy.width / 2 - 0.3, link_start
        link = Arrow(link_start, link_end, buff=0.05, color=VENV, stroke_width=4,
                     tip_length=0.18, max_tip_length_to_length_ratio=0.25)

        stack = LayerStack(stack_w=3.2)
        stack.floor.move_to([STACK_X, FLOOR_Y, 0])
        base = [stack.make(None, SYSTEM, 0.15) for _ in range(4)]
        brace = stack.brace(base, "base image")
        base_name = mono("python:3.12-slim-bookworm", 20, S.GREY).next_to(stack.floor, DOWN, buff=0.12)
        uv_slab = stack.make("RUN pip install uv", SYSTEM)
        cp_slab = copy_slab(stack)
        uv_tag = chip("uv", TOOL, size=20, font=MONO).next_to(uv_slab.box, RIGHT, buff=0.15)
        sync = stack.make("RUN uv sync", VENV, 0.8)
        slot = outline_box(3.2, 0.46, S.GREY)
        slot.move_to([STACK_X, sync.box.get_bottom()[1] + 0.23, 0])
        slot_t = label("packages: none yet", 20, S.GREY).move_to(slot)
        picture = VGroup(*base, uv_slab, cp_slab, brace, base_name, uv_tag, slot, slot_t)
        note = VGroup(label(f"CPython {V_UV} + /.venv", 22, S.GREY, t2f={"/.venv": MONO}),
                      label("11 packages", 22, S.GREY)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        note.next_to(sync.box, RIGHT, buff=0.3)

        with self.voiceover(SAY[4]) as vo:
            # the note fades with the rows the strip drops (one step), then the terminal shrinks
            r30b.remove(arm)
            self.add(arm)
            drop_rows = [ln for ln in t.lines.submobjects if ln not in (r29, r30a, r30b)]
            self.play(FadeOut(arm), FadeOut(VGroup(*drop_rows)), run_time=0.25)
            for ln in drop_rows:
                t.lines.remove(ln)
                self.remove(ln)
            resize(self, t, STRIP_ROWS, keep=[r29, r30a, r30b], run_time=0.6)
            self.play(Create(vl.axis), LaggedStart(*[FadeIn(tk, shift=UP * 0.1) for tk in vl.ticks], lag_ratio=0.1),
                      run_time=0.9)
            vo.wait_until("the requirement covers")
            vl.band.stretch_to_fit_width(0.01).align_to(band_full, LEFT)
            self.add(vl.band)
            self.play(Transform(vl.band, band_full), FadeIn(vl.band_label, shift=RIGHT * 0.2), run_time=1.0)
            self.play(Indicate(vl.band_label, color=VENV, scale_factor=1.06), run_time=0.6)
            vo.wait_until("The base image's 3.12")
            self.play(FadeIn(o_dot, shift=DOWN * 0.8), run_time=0.5)
            self.play(FadeIn(o_lab, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("falls outside")
            self.play(Create(o_x), run_time=0.4)
            vo.wait_until("so uv downloads")
            self.play(FadeIn(uv_chip, scale=0.7), run_time=0.3)
            self.add(g_dot)
            self.play(GrowArrow(drop), g_dot.animate.move_to(g_end), run_time=0.7)
            self.play(FadeOut(drop), FadeIn(g_lab, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("the newest stable")
            self.play(FadeIn(newest, shift=LEFT * 0.15), run_time=0.4)
            self.play(Indicate(g_dot, color=VENV, scale_factor=1.6), run_time=0.6)
            vo.wait_until("and the python in the venv")
            self.play(FadeIn(vpy, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("links to it")
            self.play(GrowArrow(link), run_time=0.5)
            self.wait(0.5)                      # chip -> link -> dot, read before the line goes
            # the picture of the image: everything but the GREEN dot goes, the stack comes back (quick,
            # so the finished stack can hold 2 s before the run; overlapped, the two pictures smear)
            line_parts = VGroup(vl.axis, vl.ticks, vl.band, vl.band_label, o_dot, o_lab, o_x, uv_chip,
                                newest, g_lab, vpy, link)
            self.play(FadeOut(line_parts), run_time=0.4)
            self.play(FadeIn(picture, shift=LEFT * 1.5), run_time=0.6)
            stack.accept(self, *base, uv_slab, cp_slab)
            # the strip's `RUN uv sync` travels round the right of the stack (along its own empty row,
            # then up a clear column) to meet the GREEN dot beside the slot; together they fly into
            # the slot and become the slab (a straight flight would cut through the base slabs)
            txt = substring(r29, "RUN uv sync").copy()
            y_slab = sync.box.get_center()[1]
            p0 = txt.get_center()
            corner = np.array([UP_X, p0[1], 0])
            route = VMobject()
            route.start_new_path(p0)
            route.add_line_to(corner + LEFT * 0.6)
            route.add_quadratic_bezier_curve_to(corner, corner + UP * 0.6)
            route.add_line_to(np.array([UP_X, y_slab, 0]))
            assert UP_X - txt.width / 2 > uv_tag.get_right()[0] + 0.3, "the column clears the uv tag"
            self.add(txt)
            self.play(MoveAlongPath(txt, route), g_dot.animate.move_to([UP_X + txt.width / 2 + 0.4, y_slab, 0]),
                      FadeOut(VGroup(slot, slot_t)), run_time=0.7)
            self.play(ReplacementTransform(txt, sync.text), ReplacementTransform(g_dot, sync.box), run_time=0.6)
            self.remove(sync.box, sync.text)
            stack.accept(self, sync)
            self.play(FadeIn(note, shift=LEFT * 0.1), run_time=0.5)
            self.wait(2.0)                      # the finished stack and its note hold before the run

        # ========================================================== 5 · run it: .venv, uv.lock, same error
        w = wide_term(13)
        everything4 = VGroup(*stack.slabs, brace, base_name, uv_tag, note)

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(everything4), FadeOut(t), run_time=0.5)
            self.play(FadeIn(w), run_time=0.3)
            bare_prompt(self, w)
            c5 = type_rows(self, w, RUN_ROWS, 0.8)
            yt5 = beside(turn_tag(), c5.rows[1])            # beside the command's own row: it scrolls with it
            pin(self, c5.rows[1], yt5, run_time=0.3)
            self.play(Wiggle(yt5, scale_value=1.15, rotation_angle=0.025 * TAU), run_time=0.5)
            vo.wait_until("then two extras")
            self.play(track(tr, 10, extra=True), run_time=0.3)
            r_ls = istep(self, w, LS_LINE, 0.3)
            pin(self, r_ls, beside(row_tag("extra"), r_ls), run_time=0.25)
            vo.wait_until("which also lists hidden")
            self.play(Indicate(substring(r_ls, "-a"), color=TURN, scale_factor=1.5), run_time=0.7)
            vo.wait_until("Now the listing")
            o5 = w.print(self, LS_OUT, run_time=0.6, lag=0.12)
            g_dv = substring(o5[5], ".venv")
            g_lock = substring(o5[4], "uv.lock")
            vo.wait_until("dot venv")
            self.play(g_dv.animate.set_color(VENV), run_time=0.3)
            self.play(Indicate(g_dv, color=VENV, scale_factor=1.3), run_time=0.6)
            vo.wait_until("and a new uv.lock")
            self.play(g_lock.animate.set_color(VENV), run_time=0.3)
            self.play(Indicate(g_lock, color=VENV, scale_factor=1.3), run_time=0.6)
            vo.wait_until("But python cli.py")
            r_py = istep(self, w, PY_LINE, 0.5)
            pin(self, r_py, beside(row_tag("extra"), r_py), run_time=0.25)
            o5e = w.print(self, [(s, ERR) for s in PY_ERR], run_time=0.5, lag=0.12)
            r_err = o5e[3]
            p5 = bare_prompt(self, w)
            vo.wait_until("Why?")
            self.play(Indicate(r_err.glyphs, color=ERR, scale_factor=1.06), run_time=0.7)

        # ========================================================== 6 · PATH: python finds /usr/local/bin first
        env = chip(ENV_PATH, S.GREY, size=20, font=MONO)
        env.move_to([6.45 - env.width / 2, 2.45, 0])
        dirs = ["/usr/local/bin", "/usr/local/sbin", "…"]
        doors = PathDoors(dirs, colors={"/usr/local/bin": SYSTEM}, door_h=DOOR_H)
        d0 = doors.doors[0]
        doors.shift(np.array([DOOR_LEFT - d0.frame.get_left()[0], DOOR_TOP - d0.frame.get_top()[1], 0]))
        srcs = [text_span(env.text, ENV_PATH, "/usr/local/bin"), text_span(env.text, ENV_PATH, "/usr/local/sbin"),
                text_span(env.text, ENV_PATH, "/usr…")]
        g_path = text_span(env.text, ENV_PATH, "PATH")
        cap_off = steady("venv not activated", 24, S.GREY)
        cap_off.move_to([4.85, DOOR_TOP - DOOR_H / 2, 0])
        cap_on = steady("venv activated", 24, VENV).move_to(cap_off, aligned_edge=LEFT)
        fig = figure("python").next_to(d0.frame, UP, buff=0.12)
        orange = place_dest(dest(SYSTEM, V_BASE), d0)
        no_pkgs = label("no art, no googletrans", 22, ERR).next_to(orange, RIGHT, buff=0.35)

        with self.voiceover(SAY[6]) as vo:
            resize(self, w, STRIP_ROWS, keep=[r_py, r_err, p5], run_time=0.6)
            self.play(FadeIn(env, shift=DOWN * 0.1), run_time=0.5)
            self.play(LaggedStart(*[TransformFromCopy(s, d.label) for s, d in zip(srcs, doors.doors)], lag_ratio=0.2),
                      LaggedStart(*[FadeIn(VGroup(d.frame, d[1]), shift=DOWN * 0.2) for d in doors.doors],
                                  lag_ratio=0.2), run_time=1.1)
            self.remove(*[d.label for d in doors.doors])
            self.add(doors)
            vo.wait_until("activation is just PATH")
            self.play(g_path.animate.set_color(ROUTE), run_time=0.3)
            self.play(Indicate(g_path, color=ROUTE, scale_factor=1.3), run_time=0.7)
            vo.wait_until("Nothing has activated")
            self.play(FadeIn(cap_off, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("so the word python")
            self.play(FadeIn(fig, shift=DOWN * 0.2), run_time=0.4)
            self.play(fig.animate.move_to(d0.frame), d0.frame.animate.set_fill(SYSTEM, 0.4),
                      d0[1].animate.set_fill(opacity=0), run_time=0.6)
            vo.wait_until("in user local bin")
            self.play(Indicate(d0.label, color=SYSTEM, scale_factor=1.15), run_time=0.7)
            vo.wait_until("from the base image")
            fig_at = np.array([orange.dot.get_left()[0] - 0.25 - fig.width / 2, DEST_Y, 0])
            self.play(fig.animate.move_to(fig_at), run_time=0.6)
            self.play(FadeIn(orange, scale=0.8), run_time=0.4)
            vo.wait_until("That's 3.12")
            self.play(Indicate(orange, color=SYSTEM, scale_factor=1.2), run_time=0.7)
            vo.wait_until("none of our packages")
            self.play(FadeIn(no_pkgs, shift=LEFT * 0.1), fig.animate.set_color(ERR), run_time=0.5)
            self.play(Indicate(r_err.glyphs, color=ERR, scale_factor=1.06), run_time=0.7)

        # ========================================================== 7 · the GREEN door; the two checks
        green_door = doors._door("/.venv/bin", VENV)
        step = green_door.frame.width + doors.gap
        green_door.shift(np.array([DOOR_LEFT - green_door.frame.get_left()[0],
                                   DOOR_TOP - green_door.frame.get_top()[1], 0]))
        fig2 = figure("python").next_to(green_door.frame, UP, buff=0.12)
        green = place_dest(dest(VENV, V_UV), green_door)

        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(fig, no_pkgs)), d0.frame.animate.set_fill(SYSTEM, 0.1),
                      d0[1].animate.set_fill(opacity=1), Transform(cap_off, cap_on), run_time=0.6)
            vo.wait_until("put its bin folder")
            self.play(doors.doors.animate.shift(RIGHT * step), orange.animate.shift(RIGHT * step), run_time=0.5)
            self.play(FadeIn(green_door, shift=DOWN * 0.6), run_time=0.5)
            doors.doors.submobjects.insert(0, green_door)
            self.add(doors)
            vo.wait_until("and python would find")
            self.play(FadeIn(fig2, shift=DOWN * 0.2), run_time=0.3)
            self.play(fig2.animate.move_to(green_door.frame), green_door.frame.animate.set_fill(VENV, 0.4),
                      green_door[1].animate.set_fill(opacity=0), run_time=0.6)
            fig2_at = np.array([green.dot.get_left()[0] - 0.25 - fig2.width / 2, DEST_Y, 0])
            self.play(fig2.animate.move_to(fig2_at), run_time=0.5)
            self.play(FadeIn(green, scale=0.8), run_time=0.4)
            self.play(Indicate(green, color=VENV, scale_factor=1.2), run_time=0.6)

            vo.wait_until("Two extra checks")
            resize(self, w, 5, run_time=0.5)
            r_ver = istep(self, w, VER_LINE, 0.6)
            pin(self, r_ver, beside(row_tag("extra"), r_ver), run_time=0.25)
            vo.wait_until("the venv's own python")
            o7 = w.print(self, VER_OUT, run_time=0.3)[0]
            g_v7 = substring(o7, V_UV)
            self.play(g_v7.animate.set_color(VENV), run_time=0.3)
            self.play(Indicate(g_v7, color=VENV, scale_factor=1.3), Indicate(green, color=VENV, scale_factor=1.2),
                      run_time=0.7)
            vo.wait_until("and after sourcing")
            r_src = istep(self, w, SRC_LINE, 1.0)
            pin(self, r_src, beside(row_tag("extra"), r_src), run_time=0.25)
            vo.wait_until("python cli.py works")
            o7b = w.print(self, [SRC_OUT[0], SRC_OUT[1], (SRC_OUT[2], VENV)], run_time=0.5, lag=0.15)
            self.play(Indicate(o7b[2].glyphs, color=VENV, scale_factor=1.08), run_time=0.7)
            vo.wait_until("The prompt now shows")
            w.set_prompt(APP_PROMPT)
            p7 = bare_prompt(self, w)
            g_app = substring(p7, "(app)")
            # why "app" (not simple-translate): the project's name, shown with the pulse so it can be read
            app_src = beside(row_tag([("pyproject.toml", "mono"), ("· line 2:", "label"), (APP_NAME, "mono")]), p7)
            self.play(Indicate(g_app, color=VENV, scale_factor=1.4), FadeIn(app_src, shift=LEFT * 0.1), run_time=0.8)
            attach(self, p7, app_src)
            vo.wait_until("Type exit")
            unpin(self, [(p7, app_src)], 0.25)          # typing at the prompt replaces its bare row
            istep(self, w, EXIT_LINE, 0.3)
            w.print(self, EXIT_ECHO, run_time=0.25)
            w.set_prompt(P_LAPTOP)
            p7b = bare_prompt(self, w)
            self.play(Indicate(substring(p7b, P_LAPTOP), color=INK, scale_factor=1.05), run_time=0.6)

        # ========================================================== 8 · two Pythons; half the puzzle; the fix
        o_sum = Dot(radius=0.16, color=SYSTEM).move_to([-3.6, 2.1, 0])
        g_sum = Dot(radius=0.16, color=VENV).move_to([2.6, 2.1, 0])
        o_top = mono(V_BASE, 28, SYSTEM).next_to(o_sum, RIGHT, buff=0.22)
        g_top = mono(V_UV, 28, VENV).next_to(g_sum, RIGHT, buff=0.22)
        o_role = label("base · only ran pip install uv", 22, S.GREY).next_to(VGroup(o_sum, o_top), DOWN, buff=0.15)
        g_role = label("uv download · runs the app", 22, S.GREY).next_to(VGroup(g_sum, g_top), DOWN, buff=0.15)
        p_old = mono("3.12", 32, SYSTEM)
        p_q = label("?", 52, TURN)
        p_new = mono(V_VM, 32, S.GREY)
        VGroup(p_old, p_q, p_new).arrange(RIGHT, buff=0.55).move_to([0, 0.35, 0])     # the puzzle row
        half = label("half solved", 24, TURN).next_to(p_q, DOWN, buff=0.12)
        err = erratum_tag()
        refs = label("README.md · line 133,  Dockerfile.txt · line 2  vs  pyproject.toml · line 6", 22, S.GREY,
                     t2f={"README.md": MONO, "Dockerfile.txt": MONO, "pyproject.toml": MONO})
        err_row = VGroup(err, refs).arrange(RIGHT, buff=0.3).move_to([0, -1.05, 0])
        fix1 = chip("FROM python:3.13-slim-bookworm", VENV, size=22, font=MONO)
        fix2 = chip("or a requires-python the image already meets", VENV, size=22,
                    text_color=INK)
        fixes = VGroup(fix1, fix2).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([0, -2.4, 0])
        fixl = label("fix:", 24, VENV).next_to(fix1, LEFT, buff=0.3)

        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(w, env, doors, cap_off, fig2)), track(tr, 10), run_time=0.6)
            # ORANGE first (up and left), then GREEN (up and right, passing under it): no crossing
            self.play(ReplacementTransform(orange.dot, o_sum), ReplacementTransform(orange.text, o_top), run_time=0.6)
            self.play(ReplacementTransform(green.dot, g_sum), ReplacementTransform(green.text, g_top), run_time=0.8)
            vo.wait_until("3.12 from the base")
            self.play(Indicate(o_top, color=SYSTEM, scale_factor=1.2), run_time=0.6)
            vo.wait_until("which only installed uv")
            self.play(FadeIn(o_role, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("and 3.15 for the app")
            self.play(Indicate(g_top, color=VENV, scale_factor=1.2), run_time=0.6)
            self.play(FadeIn(g_role, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("That's half")
            self.play(FadeIn(p_old, shift=RIGHT * 0.2), FadeIn(p_new, shift=LEFT * 0.2), run_time=0.5)
            self.play(FadeIn(p_q, scale=1.6), run_time=0.4)
            self.play(Wiggle(p_q, scale_value=1.3), FadeIn(half, shift=UP * 0.1), run_time=0.7)
            vo.wait_until("and a small mismatch")
            self.play(FadeIn(err_row, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("In your own projects")
            self.play(FadeIn(fixl, shift=RIGHT * 0.1), FadeIn(fix1, shift=RIGHT * 0.15), run_time=0.5)
            vo.wait_until("or make requires-python")
            self.play(FadeIn(fix2, shift=RIGHT * 0.15), run_time=0.5)
            self.play(Indicate(fixes, color=VENV, scale_factor=1.04), run_time=0.8)

        self.wait(0.4)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
