"""S06 · Step 3: install uv, copy the code (README A9, V5 seed: the build context, V2: two new slabs).

Beats (script.md "## S06", one voiceover block each):
 0  TRACKER A8 -> A9. CODE(README.md: 148–151) at the top; RUN and COPY pulse on "two
    instructions". Line 149 gets a YELLOW bar on "RUN pip install uv"; `pip` underlines ORANGE on
    "uses the pip of the base image"; `uv` turns PURPLE and a PURPLE `uv` chip pops beside the line
    on "to install uv". The bar moves to line 151 on "And the COPY line": the first `.` gets a GREY
    label "this folder" (leader to the left), `./` a TEAL label "the image's top folder" (leader to
    the right). On "Add both at the end" the 6-row strip below types `cat Dockerfile` (TRACKER A9 ·
    extra, row tag `extra`) -> laptop/17 "…", 7–10; "and save": YELLOW bar on the four new rows.
 1  V5 seed. The panel leaves and the build command writes small at the top (the strip stays a
    moment longer, so the cat output can be read); its final `.` turns PINK with a ring on "the
    final dot", the strip leaves and a copy of the ring flies down-left and becomes a GREY folder
    `simple-translate/` holding ten file glyphs (`.git/`, `cli.py`, `Dockerfile` named: ten
    entries, as in the clone); the folder pulses on "Docker packs". "into one parcel": the folder's
    tab goes, PINK tape closes it, its title becomes "build context" (PINK). "and sends it to the
    builder": S04's
    PURPLE builder chip appears on the right and grows into a box holding the image: four thin
    ORANGE base slabs and on them the TEAL box `/` "the image's top folder" with the system's own
    `bin etc usr …` (ORANGE); a PINK route draws from the parcel to it. "Every file goes in": the
    items pulse; `.git/` and `Dockerfile` light YELLOW as they are said. "a file called dot
    dockerignore": a GREY dashed sieve `.dockerignore` hangs across the route; "but this repo has
    none": tag "none in this repo"; the parcel (names hidden) shrinks and rides the route through
    the dashed sieve into the builder, nothing caught. "The COPY line unpacks it": tape and box
    fall away and the ten items spread into `/` next to `bin etc usr …`.
 2  TRACKER A9. Full terminal (13 rows): `docker build -t simple-translate -f Dockerfile .` (two
    rows) + ▶ your turn -> laptop/18 lines 12–13, 16–17. "there's no dockerignore": row 13 gets the
    GREY tag "no .dockerignore" and its `2B` an underline; "and the whole context": `63.12kB` turns
    PINK, row tag "the parcel" (PINK) on "63 kilobytes here".
 3  The terminal continues -> laptop/18 "…", 27, 33, then 34 (wrap: six rows), then on "and COPY
    runs" "…", 40–41. `uv-0.13.0` underlines with the row tag "at the time of recording"; on "two
    new layers" the two step names (`[2/3] RUN pip install uv`, `[3/3] COPY . ./`) get TEAL bars.
    "Pip also warns": a YELLOW bracket spans the six warning rows, "Running pip as the 'root' user"
    underlines YELLOW; "In lecture 1": "use a virtual environment" underlines GREEN. "here, the
    image itself is the isolation": the terminal shrinks to the 3-row strip (rows 27, 33, 40); the
    V2 stack (S05's: four thin ORANGE slabs, brace "base image", caption
    `python:3.12-slim-bookworm`) fades in; the strip's `RUN pip install uv` and `COPY . ./` are
    copied up into two slabs: ORANGE with a PURPLE `uv` chip beside it, GREY with file glyphs;
    "adds a layer" (TEAL) beside each.
 4  The stack above the strip; the `uv` chip pulses on "uv is installed", the COPY slab on "and the
    code is in the image", its glyphs on "Will python cli.py run?". PONDER (6 s) card at the bottom:
    the strip fades out as it comes in (its rows would show through the card and past its sides).
 5  The ponder card gets a RED cross beside the question on "No." and leaves with the picture.
    Full wide terminal (13.2 wide, 20 pt, 13 rows): `docker run --rm -ti simple-translate` +
    ▶ your turn (on the next row: the command fills its row) -> at the capture's prompt
    `root@1f2c7df8735d:/#`, TRACKER A9 · extra, `ls` (row tag `extra`) -> laptop/19 lines 3–7 in
    columns. "our files sit": the seven repo entries turn white and pulse; "the system's own
    folders": the others dim ORANGE.
 6  At the same prompt `python cli.py` (row tag `extra`) -> laptop/19 lines 9–12, RED;
    `ModuleNotFoundError` pulses, then both `art`s. "We installed the installer": the terminal
    shrinks to the 3-row strip (the command, the RED line, the prompt); above it the V2 stack
    returns, the PURPLE `uv` chip glows; "not the packages": a dashed GREY slot "packages: none
    yet" appears on top of the stack. "Type exit": `exit` (line 13) -> line 14, the laptop prompt
    returns. Fade out to an empty frame.
"""

import numpy as np  # noqa: I001  (manim first, then common: common must win)
from manim import *

from explainer import style as S
from explainer.components import ponder_card
from explainer.devops import code_span, line_bar
from explainer.scene import VoiceScene

from common import (BUILD, CAT, ERR, IMAGE, INK, LAPTOP, LAPTOP_DIR, MONO, NARRATION, P_LAPTOP, ROUTE, RUN,
                    STRIP_ROWS, SYSTEM, TOOL, TURN, VENV, LayerStack, Parcel, Sieve, Slab, attach,
                    bare_prompt, beside, box, builder_box, capture, chip, code, cross_mark, file_glyph,
                    folder_glyph, glyph_range, hl_bar, istep, label, laptop_term, mono, mono_line,
                    outline_box, pin, resize, route, row_tag, substring, tag, track, tracker_a,
                    type_cmd, under, unpin, wide_term)

SAY = NARRATION["S06"]
PONDER_Q = "uv is installed and the code is copied in.\nWill python cli.py run?"

# ------------------------------------------------------------------ real outputs (file line numbers)
C17 = capture("17", LAPTOP_DIR)                          # laptop/17-dockerfile-v3.txt
assert C17.cmd == CAT, C17.cmd
CAT_OUT = C17.at("…", (7, 10))                           # …, # Install uv, RUN pip install uv, # Copy…, COPY . ./
assert CAT_OUT[-1] == "COPY . ./" and CAT_OUT[2] == "RUN pip install uv", CAT_OUT

C18 = capture("18", LAPTOP_DIR)                          # laptop/18-build-v3.txt
assert C18.cmd == BUILD, C18.cmd
CTX_OUT = C18.at((12, 13), (16, 17))                     # load .dockerignore … 2B / load build context … 63.12kB
assert "2B" in CTX_OUT[1] and "63.12kB" in CTX_OUT[3], CTX_OUT
UV_OUT = C18.at("…", 27, 33)                             # [2/3] RUN pip install uv · Successfully installed uv-0.13.0
WARN = C18.line(34)                                      # the root-user WARNING (wraps onto 6 rows)
COPY_OUT = C18.at("…", (40, 41))                         # [3/3] COPY . ./ · DONE
assert "uv-0.13.0" in UV_OUT[2] and WARN.startswith("#6 4.908 WARNING") and "[3/3] COPY . ./" in COPY_OUT[1]

C19 = capture("19", LAPTOP_DIR)                          # laptop/19-run-v3.txt
assert C19.cmd == RUN, C19.cmd
LS_OUT = C19.at((3, 7))                                  # ls in columns (up to 70 characters)
PY_ERR = C19.at((9, 12))                                 # Traceback … ModuleNotFoundError: No module named 'art'
EXIT_ECHO = C19.at(14)                                   # ["exit"]
assert PY_ERR[-1] == "ModuleNotFoundError: No module named 'art'", PY_ERR
REPO_FILES = ["Dockerfile", "Dockerfile.txt", "README.md", "cli.py", "docker-build-push.sh",
              "docker-shell.sh", "pyproject.toml"]

# ------------------------------------------------------------------ layout
PANEL_X = -0.9                       # beat 0: README panel (4.6 wide) left of centre, the uv chip right of it
STACK_X, FLOOR_Y = -1.2, -0.25       # the V2 stack (3.2 wide; S05's height, centred: no config card here)
PARCEL_X = -3.95                     # beat 1: the folder / parcel (left)
BUILDER_X, BUILDER_Y = 3.85, -0.55   # beat 1: the builder box (right)
SHRINK = 0.4                         # the parcel's size while it travels (names hidden)


# ------------------------------------------------------------------ helpers
def lead(vo, phrase: str, early: float) -> None:
    """Wait until `early` seconds before `phrase` is spoken."""
    dt = vo.time_until(phrase) - early
    if dt > 1 / 60:
        vo.scene.wait(dt)


def turn_tag() -> VGroup:
    """YELLOW '▶ your turn', the height of a terminal row."""
    return row_tag("▶ your turn", TURN)


def leader(glyphs, lab, side) -> VMobject:
    """An L-shaped leader from under `glyphs` down to the middle of label `lab` (side LEFT: the label
    is left of the glyphs; RIGHT: right of them)."""
    x = glyphs.get_center()[0]
    y0 = glyphs.get_bottom()[1] - 0.08
    y1 = lab.get_center()[1]
    x1 = lab.get_right()[0] + 0.1 if side is LEFT else lab.get_left()[0] - 0.1
    return VMobject().set_points_as_corners([[x, y0, 0], [x, y1, 0], [x1, y1, 0]]).set_stroke(S.GREY, 2.5)


def bracket(rows, x: float, color=TURN) -> VMobject:
    """A '[' bracket left of terminal rows, from the first row's top to the last row's bottom."""
    top = rows[0].strut.get_top()[1] - 0.02
    bot = rows[-1].strut.get_bottom()[1] + 0.02
    return VMobject().set_points_as_corners([[x + 0.1, top, 0], [x, top, 0], [x, bot, 0], [x + 0.1, bot, 0]]) \
        .set_stroke(color, 4)


def token_spans(s: str) -> list[tuple[str, int, int]]:
    """(token, start, end) of every whitespace-separated token of an `ls` row."""
    out, i = [], 0
    for tok in s.split():
        i = s.index(tok, i)
        out.append((tok, i, i + len(tok)))
        i += len(tok)
    return out


def bar_on(scene, row, glyphs, color, opacity: float = 0.25):
    """A translucent bar behind `glyphs` of terminal row `row` (part of the row: it scrolls with it)."""
    b = hl_bar(glyphs, color, opacity)
    row.add_to_back(b)
    scene.add(row)
    return b


def folder_shape(frame, title: str):
    """The project folder drawn on a parcel's frame: a tab on its top-left with the folder's name.
    .tab .title"""
    t = mono(title, 20, LAPTOP)
    tab = RoundedRectangle(width=t.width + 0.4, height=0.44, corner_radius=0.1, stroke_color=LAPTOP,
                           stroke_width=2.5).set_fill(LAPTOP, 0.1)
    tab.next_to(frame, UP, buff=-0.02).align_to(frame, LEFT)
    t.move_to(tab)
    g = VGroup(tab, t)
    g.tab, g.title = tab, t
    return g


def copy_slab(stack: LayerStack) -> Slab:
    """The GREY `COPY . ./` slab with a few file glyphs (a folder for .git/ first) beside its text."""
    s = stack.make("COPY . ./", LAPTOP)
    glyphs = VGroup(folder_glyph(0.2, LAPTOP), *[file_glyph(0.24, LAPTOP) for _ in range(3)])
    glyphs.arrange(RIGHT, buff=0.1)
    row = VGroup(s.text, glyphs)
    glyphs.next_to(s.text, RIGHT, buff=0.3)
    row.move_to(s.box)
    glyphs.set_y(s.box.get_center()[1])
    s.add(glyphs)
    s.glyphs = glyphs
    return s


# ------------------------------------------------------------------ the scene
class StepCopy(VoiceScene):
    def construct(self):
        assert len(SAY) == 7, f"S06 has {len(SAY)} SAY lines; this scene times 7"

        tr = tracker_a(8)

        # ========================================================== 0 · two instructions
        panel = code("README.md", 148, 151, "docker")
        panel.move_to([PANEL_X, 2.78 - panel.height / 2, 0])
        src = panel.code
        g_run, g_copy = code_span(src, 1, "RUN"), code_span(src, 3, "COPY")
        bar_a = line_bar(src, 1, TURN, 0.18)
        bar_b = line_bar(src, 3, TURN, 0.18)
        g_pip = code_span(src, 1, "pip")
        g_uv = code_span(src, 1, "uv")
        u_pip = under(g_pip, SYSTEM, y=src.code_lines[1].get_bottom()[1] - 0.06)
        uv_chip = chip("uv", TOOL, size=22, font=MONO)
        uv_chip.next_to(src, RIGHT, buff=0.35).set_y(src.code_lines[1].get_center()[1])
        g_dot = code_span(src, 3, ".")                    # COPY [.] ./
        g_dst = code_span(src, 3, "./")                   # COPY . [./]
        lab_y = src.get_bottom()[1] - 0.42
        lab_this = label("this folder", 22, LAPTOP)
        lab_this.move_to([g_dot.get_center()[0] - 0.35 - lab_this.width / 2, lab_y, 0])
        lab_top = label("the image's top folder", 22, IMAGE)
        lab_top.move_to([g_dst.get_center()[0] + 0.35 + lab_top.width / 2, lab_y, 0])
        lead_this = leader(g_dot, lab_this, LEFT)
        lead_top = leader(g_dst, lab_top, RIGHT).set_stroke(IMAGE)
        strip = laptop_term(6)                             # 6 rows: the command, "…" and the four new lines

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.1), run_time=0.4)
            self.play(track(tr, 9), FadeIn(panel, shift=DOWN * 0.15), run_time=0.6)
            self.play(Indicate(VGroup(tr.dots[8], tr.caption), color=TURN, scale_factor=1.12),
                      FadeIn(strip), run_time=0.6)
            bare_prompt(self, strip)
            vo.wait_until("two instructions")
            self.play(LaggedStart(Indicate(g_run, color=TURN, scale_factor=1.2),
                                  Indicate(g_copy, color=TURN, scale_factor=1.2), lag_ratio=0.4), run_time=0.9)
            vo.wait_until("RUN pip install uv")
            self.play(FadeIn(bar_a), Indicate(src.code_lines[1], color=TURN, scale_factor=1.05), run_time=0.6)
            vo.wait_until("uses the pip")
            self.play(Create(u_pip), g_pip.animate.set_color(SYSTEM), run_time=0.5)
            self.play(Indicate(g_pip, color=SYSTEM, scale_factor=1.2), run_time=0.6)
            vo.wait_until("to install uv")
            self.play(g_uv.animate.set_color(TOOL), FadeIn(uv_chip, scale=0.6), run_time=0.5)
            self.play(Indicate(uv_chip, color=TOOL, scale_factor=1.2), run_time=0.6)
            vo.wait_until("And the COPY line")
            self.play(ReplacementTransform(bar_a, bar_b), Indicate(src.code_lines[3], color=TURN, scale_factor=1.05),
                      run_time=0.6)
            vo.wait_until("this folder, dot")
            self.play(Indicate(g_dot, color=INK, scale_factor=2.0), Create(lead_this), run_time=0.6)
            self.play(FadeIn(lab_this, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("into the image's top")
            self.play(Indicate(g_dst, color=IMAGE, scale_factor=1.6), Create(lead_top), run_time=0.6)
            self.play(FadeIn(lab_top, shift=RIGHT * 0.1), run_time=0.4)
            vo.wait_until("Add both at the end")
            self.play(track(tr, 9, extra=True), run_time=0.3)
            c0 = type_cmd(self, strip, CAT, 0.45)
            pin(self, c0, beside(row_tag("extra"), c0), run_time=0.25)
            out0 = strip.print(self, CAT_OUT, run_time=0.45, lag=0.12)
            vo.wait_until("and save")
            bar_new = bar_on(self, out0[1], VGroup(*[r.glyphs for r in out0[1:]]), TURN, 0.2)
            self.play(FadeIn(bar_new), Indicate(VGroup(*[r.glyphs for r in out0[1:]]), color=TURN,
                                                         scale_factor=1.03), run_time=0.6)

        # ========================================================== 1 · V5 seed: the build context
        big = mono_line(BUILD, 22, INK)
        big.move_to([0.55, 2.4, 0])
        g_ctx = glyph_range(big, len(BUILD) - 1)
        ring = Circle(radius=0.17, color=ROUTE, stroke_width=4).move_to(g_ctx)

        parcel = Parcel((".git/", "cli.py", "Dockerfile"), extra=7)   # 3 named + 7 = the ten entries
        names = VGroup(*[it.name_text for it in parcel.items.values()])
        glyphs = VGroup(parcel.crowd, *[it.glyph for it in parcel.items.values()])
        inner = VGroup(glyphs, names)
        # the builder: the image as four base slabs, its top folder `/` on them (room for the parcel's items)
        sys_row = VGroup()
        for n in ("bin", "etc", "usr"):
            sys_row.add(VGroup(folder_glyph(0.22, SYSTEM), mono(n, 20, SYSTEM)).arrange(RIGHT, buff=0.1))
        sys_row.add(mono("…", 20, SYSTEM))
        sys_row.arrange(RIGHT, buff=0.38)
        root_w = 4.5
        root = RoundedRectangle(width=root_w, height=sys_row.height + inner.height + 0.75, corner_radius=0.12,
                                stroke_color=IMAGE, stroke_width=2.5).set_fill(IMAGE, 0.06)
        base4 = VGroup(*[Slab(None, SYSTEM, root_w, 0.15) for _ in range(4)]).arrange(UP, buff=0.04)
        root.next_to(base4, UP, buff=0.04)
        sys_row.move_to(root).align_to(root, UP).shift(DOWN * 0.25)
        root_lab = VGroup(mono("/", 26, IMAGE), label("the image's top folder", 20, S.GREY))
        root_lab.arrange(RIGHT, buff=0.2, aligned_edge=DOWN)
        root_lab.next_to(root, UP, buff=0.12).align_to(root, LEFT)
        image_g = VGroup(base4, root, sys_row, root_lab)
        b_lab = label("builder", 24, TOOL)
        b_frame = box(root_w + 0.5, image_g.height + b_lab.height + 0.75, TOOL, fill_opacity=0.08)
        b_frame.move_to([BUILDER_X, BUILDER_Y, 0])
        b_lab.move_to(b_frame.get_corner(UL) + np.array([0.25 + b_lab.width / 2, -0.22 - b_lab.height / 2, 0]))
        image_g.move_to(b_frame).align_to(b_frame, DOWN).shift(UP * 0.22)
        slot_c = np.array([root.get_center()[0], sys_row.get_bottom()[1] - 0.2 - inner.height / 2, 0])
        chip0 = builder_box("builder", 2.1, 0.95, 24).move_to(b_frame)

        # the folder / parcel on the left, its contents at the height of the slot in `/`
        parcel.shift(np.array([PARCEL_X, slot_c[1], 0]) - inner.get_center())
        home = inner.get_center().copy()
        g_off = glyphs.get_center() - home
        folder = folder_shape(parcel.frame, "simple-translate/")
        ry = parcel.frame.get_center()[1]
        r_a = np.array([parcel.frame.get_right()[0] + 0.12, ry, 0])
        r_b = np.array([b_frame.get_left()[0] - 0.1, ry, 0])
        path = route(r_a, r_b, arc=0)
        sieve = Sieve(1.5, 0.5)
        mesh = VGroup(sieve.frame, sieve.mesh)
        mesh.rotate(PI / 2)
        sx = (r_a[0] + r_b[0]) / 2
        mesh.move_to([sx, ry, 0])
        sieve.title.next_to(mesh, UP, buff=0.14).set_x(sx)
        none_tag = tag("none in this repo", S.GREY).next_to(mesh, DOWN, buff=0.18).set_x(sx)

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(panel, bar_b, u_pip, uv_chip, lab_this, lab_top, lead_this, lead_top),
                              shift=UP * 0.1),
                      ShowIncreasingSubsets(big.glyphs, rate_func=linear), run_time=0.8)
            vo.wait_until("the final dot")
            self.play(g_ctx.animate.set_color(ROUTE), Create(ring), run_time=0.4)
            # the dot is this folder: its ring flies down and becomes the folder (the cat output leaves)
            self.play(FadeOut(strip), track(tr, 9), TransformFromCopy(ring, parcel.frame), run_time=0.7)
            self.play(FadeIn(folder, shift=DOWN * 0.1), LaggedStart(*[FadeIn(m) for m in glyphs], lag_ratio=0.1),
                      FadeIn(names), run_time=0.6)
            vo.wait_until("Docker packs")
            self.play(Indicate(VGroup(parcel.frame, folder), color=LAPTOP, scale_factor=1.04),
                      Indicate(ring, color=ROUTE, scale_factor=1.3), run_time=0.8)
            vo.wait_until("into one parcel")
            self.play(FadeOut(folder.tab, shift=DOWN * 0.2), ReplacementTransform(folder.title, parcel.title),
                      Create(parcel.tape), run_time=0.8)
            vo.wait_until("the build context")
            self.play(Indicate(parcel.title, color=ROUTE, scale_factor=1.2),
                      Indicate(ring, color=ROUTE, scale_factor=1.3), run_time=0.7)
            vo.wait_until("and sends it")
            self.play(FadeIn(chip0, scale=0.8), run_time=0.4)
            self.play(ReplacementTransform(chip0.frame, b_frame), ReplacementTransform(chip0.text, b_lab),
                      run_time=0.7)
            self.play(FadeIn(image_g), GrowArrow(path), run_time=0.6)
            vo.wait_until("Every file goes in")
            self.play(LaggedStart(*[Indicate(m, color=INK, scale_factor=1.25) for m in parcel.crowd],
                                  *[Indicate(it, color=INK, scale_factor=1.15) for it in parcel.items.values()],
                                  lag_ratio=0.08), run_time=1.2)
            vo.wait_until("the hidden git folder")
            self.play(parcel.light(".git/", TURN), run_time=0.5)
            self.play(Indicate(parcel.items[".git/"], color=TURN, scale_factor=1.2), run_time=0.6)
            vo.wait_until("and your Dockerfile")
            self.play(parcel.light("Dockerfile", TURN), run_time=0.5)
            self.play(Indicate(parcel.items["Dockerfile"], color=TURN, scale_factor=1.2), run_time=0.6)
            vo.wait_until("a file called dot dockerignore")
            self.play(FadeIn(mesh, shift=DOWN * 0.3), FadeIn(sieve.title, shift=DOWN * 0.3), run_time=0.7)
            vo.wait_until("could leave some out")
            self.play(Indicate(VGroup(mesh, sieve.title), color=S.GREY, scale_factor=1.12), run_time=0.8)
            vo.wait_until("but this repo has none")
            self.play(FadeIn(none_tag, shift=UP * 0.1), run_time=0.4)
            # the parcel closes (names hidden), shrinks and rides the route through the empty sieve
            mover = VGroup(parcel.frame, parcel.tape, glyphs)
            mover.set_z_index(1)                           # it rides on the route, not under it
            self.play(FadeOut(names), FadeOut(parcel.title), run_time=0.3)
            self.play(mover.animate.scale(SHRINK).move_to(r_a + RIGHT * 0.1), run_time=0.5)
            line = Line(mover.get_center(), r_b + LEFT * 0.05)
            self.play(MoveAlongPath(mover, line), run_time=1.1)
            vo.wait_until("The COPY line unpacks")
            names.shift(slot_c - home)
            self.play(FadeOut(VGroup(parcel.frame, parcel.tape)),
                      glyphs.animate.scale(1 / SHRINK).move_to(slot_c + g_off), run_time=0.9)
            self.play(FadeIn(names), Indicate(root_lab[0], color=IMAGE, scale_factor=1.5), run_time=0.6)

        # ========================================================== 2 · build: the context travels
        t = laptop_term(13)

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(big, ring, glyphs, names, b_frame, b_lab, image_g, path, mesh, sieve.title,
                                     none_tag)), run_time=0.5)
            self.play(FadeIn(t), run_time=0.4)
            bare_prompt(self, t)
            c2 = type_cmd(self, t, BUILD, 0.8)
            yt2 = beside(turn_tag(), c2.rows[1])
            pin(self, c2.rows[1], yt2, run_time=0.3)
            self.play(Wiggle(yt2, scale_value=1.15, rotation_angle=0.025 * TAU), run_time=0.5)
            vo.wait_until("The log confirms")
            o2 = t.print(self, CTX_OUT, run_time=0.6, lag=0.15)
            r13, r17 = o2[1], o2[3]
            vo.wait_until("there's no dockerignore")
            g2b = substring(r13, "2B")
            u2b = under(g2b, S.GREY, y=r13.strut.get_bottom()[1] - 0.01)
            self.play(Create(u2b), Indicate(g2b, color=INK, scale_factor=1.4), run_time=0.5)
            attach(self, r13, u2b)
            no_ign = beside(row_tag([("no", "label"), (".dockerignore", "mono")]), r13)
            pin(self, r13, no_ign, run_time=0.4)
            vo.wait_until("so nothing is filtered")
            self.play(Indicate(no_ign, color=INK, scale_factor=1.08), run_time=0.6)
            vo.wait_until("and the whole context")
            g63 = substring(r17, "63.12kB")
            self.play(g63.animate.set_color(ROUTE), run_time=0.4)
            self.play(Indicate(g63, color=ROUTE, scale_factor=1.25), run_time=0.6)
            vo.wait_until("63 kilobytes here")
            parcel_tag = beside(row_tag("the parcel", ROUTE), r17)
            pin(self, r17, parcel_tag, run_time=0.4)
            vo.wait_until("travels to the builder")
            self.play(Indicate(parcel_tag, color=ROUTE, scale_factor=1.12), run_time=0.7)

        # ========================================================== 3 · pip installs uv, COPY runs
        stack = LayerStack(stack_w=3.2)
        stack.floor.move_to([STACK_X, FLOOR_Y, 0])
        base = [stack.make(None, SYSTEM, 0.15) for _ in range(4)]
        brace = stack.brace(base, "base image")
        base_name = mono("python:3.12-slim-bookworm", 20, S.GREY)
        base_name.next_to(stack.floor, DOWN, buff=0.12)
        uv_slab = stack.make("RUN pip install uv", SYSTEM)
        cp_slab = copy_slab(stack)
        uv_tag = chip("uv", TOOL, size=20, font=MONO)
        uv_tag.next_to(uv_slab.box, RIGHT, buff=0.15)
        adds = [label("adds a layer", 20, IMAGE) for _ in range(2)]
        adds[0].next_to(uv_tag, RIGHT, buff=0.3)
        adds[1].next_to(cp_slab.box, RIGHT, buff=0.3).align_to(adds[0], LEFT)
        picture = VGroup(*base, brace, base_name)

        with self.voiceover(SAY[3]) as vo:
            unpin(self, [(c2.rows[1], yt2)], 0.25)
            o3 = t.print(self, UV_OUT, run_time=0.5, lag=0.2)
            r27, r33 = o3[1], o3[2]
            warn = t.print(self, [WARN], run_time=0.6, wrap=True, lag=0.08)
            assert len(warn) == 6 and warn[0].text.startswith("#6 4.908 WARNING")
            vo.wait_until("version 0.13.0")
            g_ver = substring(r33, "uv-0.13.0")
            u_ver = under(g_ver, INK, y=r33.strut.get_bottom()[1] - 0.01)
            self.play(Create(u_ver), Indicate(g_ver, color=INK, scale_factor=1.15), run_time=0.6)
            attach(self, r33, u_ver)
            rec = beside(row_tag("at the time of recording"), r33)
            pin(self, r33, rec, run_time=0.4)
            vo.wait_until("and COPY runs")
            o3b = t.print(self, COPY_OUT, run_time=0.5, lag=0.2)
            r40 = o3b[1]
            vo.wait_until("two new layers")
            s27 = substring(r27, "[2/3] RUN pip install uv")
            s40 = substring(r40, "[3/3] COPY . ./")
            b27, b40 = bar_on(self, r27, s27, IMAGE), bar_on(self, r40, s40, IMAGE)
            self.play(FadeIn(b27), FadeIn(b40), Indicate(s27, color=IMAGE, scale_factor=1.08),
                      Indicate(s40, color=IMAGE, scale_factor=1.08), run_time=0.8)
            vo.wait_until("Pip also warns")
            br_w = bracket(warn, t.box.get_left()[0] + 0.14)
            g_root = substring(warn[0], "Running pip as the 'root' user")
            u_root = under(g_root, TURN, y=warn[0].strut.get_bottom()[1] - 0.01)
            self.play(Create(br_w), Create(u_root), run_time=0.6)
            attach(self, warn[0], br_w)
            attach(self, warn[0], u_root)
            self.play(Indicate(g_root, color=TURN, scale_factor=1.06), run_time=0.7)
            vo.wait_until("In lecture 1")
            g_venv = substring(warn[3], "use a virtual environment")
            u_venv = under(g_venv, VENV, y=warn[3].strut.get_bottom()[1] - 0.01)
            self.play(Create(u_venv), g_venv.animate.set_color(VENV), run_time=0.6)
            attach(self, warn[3], u_venv)
            self.play(Indicate(g_venv, color=VENV, scale_factor=1.06), run_time=0.7)
            vo.wait_until("here, the image itself")
            unpin(self, [(r33, rec)], 0.2)
            resize(self, t, STRIP_ROWS, keep=[r27, r33, r40], run_time=0.6)
            self.play(FadeIn(picture, shift=UP * 0.1), run_time=0.5)
            stack.accept(self, *base)
            stack.drop(self, uv_slab, anim=TransformFromCopy(substring(r27, "RUN pip install uv"), uv_slab),
                       run_time=0.7)
            self.play(FadeIn(uv_tag, scale=0.6), FadeIn(adds[0], shift=LEFT * 0.1), run_time=0.4)
            stack.drop(self, cp_slab, anim=TransformFromCopy(substring(r40, "COPY . ./"), cp_slab), run_time=0.7)
            self.play(FadeIn(adds[1], shift=LEFT * 0.1), run_time=0.4)

        # ========================================================== 4 · ponder
        with self.voiceover(SAY[4]) as vo:
            vo.wait_until("uv is installed")
            # the slabs pulse in their own colours (fill = what they hold); only the chip flashes PURPLE
            self.play(Indicate(uv_tag, color=TOOL, scale_factor=1.3),
                      uv_slab.animate(rate_func=there_and_back).scale(1.05), run_time=0.8)
            vo.wait_until("and the code is in")
            self.play(cp_slab.animate(rate_func=there_and_back).scale(1.06), run_time=0.8)
            vo.wait_until("Will python cli.py")
            self.play(Indicate(cp_slab.glyphs, color=TURN, scale_factor=1.25), run_time=0.8)

        q = ponder_card(PONDER_Q)
        q.move_to([0, -3.45 + q.height / 2, 0])
        # the card takes the strip's place (the strip's rows would show through the card and past its sides)
        self.play(FadeIn(q, scale=0.95), FadeOut(t), run_time=0.6)
        bar = q[3]
        self.play(bar.animate(rate_func=linear).become(bar.copy().scale(0.001, about_point=bar.get_start())),
                  run_time=6)

        # ========================================================== 5 · run it: ls
        w = wide_term(13)
        q_text = q[2]                                       # the question; its last glyph is the "?"
        no = cross_mark(0.55, ERR, stroke=7).next_to(q_text[-1], RIGHT, buff=0.45)
        no.set_y(q_text[-1].get_center()[1])
        picture4 = VGroup(*stack.slabs, brace, base_name, uv_tag)

        with self.voiceover(SAY[5]) as vo:
            self.play(Create(no), run_time=0.4)
            self.play(Indicate(no, color=ERR, scale_factor=1.25), run_time=0.5)
            self.play(FadeOut(VGroup(q, no)), FadeOut(picture4), FadeOut(VGroup(*adds)), run_time=0.5)
            self.play(FadeIn(w), run_time=0.3)
            bare_prompt(self, w)
            vo.wait_until("Pause and run it")
            c5 = type_cmd(self, w, RUN, 0.8)
            assert not hasattr(c5, "rows"), "RUN fits one 75-character row"
            yt5 = row_tag("▶ your turn", TURN)
            yt5.move_to([c5.strut.get_right()[0] - yt5.width / 2, c5.strut.get_center()[1] - w.pitch, 0])
            self.play(FadeIn(yt5, shift=LEFT * 0.1), run_time=0.3)
            self.play(Wiggle(yt5, scale_value=1.15, rotation_angle=0.025 * TAU), run_time=0.5)
            vo.wait_until("then look around")
            self.play(track(tr, 9, extra=True), run_time=0.3)
            r_ls = istep(self, w, C19.line(2), 0.3)
            attach(self, r_ls, yt5)
            pin(self, r_ls, beside(row_tag("extra"), r_ls), run_time=0.25)
            o5 = w.print(self, LS_OUT, run_time=0.6, lag=0.12)
            ours, theirs = [], []
            for row in o5:
                for tok, a, b in token_spans(row.text):
                    (ours if tok in REPO_FILES else theirs).append(glyph_range(row, a, b))
            assert len(ours) == 7, len(ours)
            vo.wait_until("our files sit")
            self.play(*[g.animate.set_color(INK) for g in ours], run_time=0.4)
            self.play(LaggedStart(*[Indicate(g, color=INK, scale_factor=1.12) for g in ours], lag_ratio=0.12),
                      run_time=1.0)
            vo.wait_until("the system's own folders")
            self.play(*[g.animate.set_color(SYSTEM).set_opacity(0.7) for g in theirs], run_time=0.6)

        # ========================================================== 6 · python cli.py: no module named art
        slot = outline_box(3.2, 0.46, S.GREY)
        slot.move_to([STACK_X, stack.top_y() + 0.04 + 0.23, 0])
        slot_t = label("packages: none yet", 20, S.GREY).move_to(slot)
        glow = Circle(radius=0.42, color=TOOL, stroke_width=4).move_to(uv_tag)

        with self.voiceover(SAY[6]) as vo:
            r_py = istep(self, w, C19.line(8), 0.5)
            vo.wait_until("another extra")
            pin(self, r_py, beside(row_tag("extra"), r_py), run_time=0.3)
            lead(vo, "ModuleNotFoundError", 0.5)
            o6 = w.print(self, [(s, ERR) for s in PY_ERR], run_time=0.5, lag=0.12)
            r_err = o6[3]
            p6 = bare_prompt(self, w)
            self.play(Indicate(r_err.glyphs, color=ERR, scale_factor=1.06), run_time=0.7)
            vo.wait_until("no module named art")
            u_art = under(substring(r_err, "'art'"), ERR, y=r_err.strut.get_bottom()[1] - 0.01)
            self.play(Create(u_art), Indicate(substring(o6[2], "art"), color=INK, scale_factor=1.3), run_time=0.6)
            attach(self, r_err, u_art)
            vo.wait_until("We installed the installer")
            resize(self, w, STRIP_ROWS, keep=[r_py, r_err, p6], run_time=0.6)
            self.play(FadeIn(picture4, shift=UP * 0.1), run_time=0.5)
            self.play(Create(glow), Indicate(uv_tag, color=TOOL, scale_factor=1.3), run_time=0.6)
            self.play(FadeOut(glow, scale=1.4), run_time=0.4)
            vo.wait_until("not the packages")
            self.play(Create(slot.frame), FadeIn(slot_t, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("Type exit")
            istep(self, w, C19.line(13), 0.3)
            w.print(self, EXIT_ECHO, run_time=0.25)
            w.set_prompt(P_LAPTOP)
            bare_prompt(self, w)

        self.wait(0.8)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
