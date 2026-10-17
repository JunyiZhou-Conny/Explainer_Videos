"""S04 · Dockerfile step 1: FROM (README A6-A7, three extras, V2 base slabs, V3 config card).

Beats (script.md "## S04", one voiceover block each):
 0  TRACKER A6 (the tracker fades in at A5 and moves on). A schematic editor sidebar (title "files",
    tag `illustration` in its title bar): the clone's tree `simple-translate/` with the entries of
    laptop/05; the root row pulses on "inside the simple-translate folder". Top right, a README card
    (README.md · lines 128–130). On "create a file called" a new row `Dockerfile` slides in YELLOW
    (the rows under it make room); its "D" pulses on "capital D"; a GREY tag "exactly this name · no
    extension" points at it. Tracker dots 7–11 pulse on "five steps"; "(Do a Build + Run after each
    step)" underlines YELLOW on "a build and a run". ▶ your turn under the tag.
 1  TRACKER A7. CODE(README.md: 135–136) at the top; the FROM line gets a YELLOW bar on "one
    instruction"; python (TEAL), 3.12, slim, bookworm (ORANGE) underline as they are read. Four chips
    drop out of the name on sentence 2: `python` "official image" (TEAL), `3.12` "Python 3.12",
    `slim` "fewer packages", `bookworm` "Debian 12" (ORANGE). The 3-row strip fades in; TRACKER A7 ·
    extra: `cat Dockerfile` (row tag `extra`) -> laptop/08 lines 2-3.
 2  TRACKER A7. Panel, chips and strip leave. Header `README.md · line 174` and the build command
    writes large (28 pt). `-t simple-translate` underlines TEAL ("the image's name"), `-f Dockerfile`
    WHITE ("the recipe"), the final `.` gets a PINK ring ("build context: this folder"); a GREY
    folder pops out of the dot and rides a PINK route into a PURPLE "builder" box. On "Step 3" the
    tracker's step-9 dot pulses. GREY `Lecture 2 · slides 32, 56` (lecture_ref, top right) from
    "Dash t names" through the build (beat 3); it fades with the build's notes as beat 4 starts.
 3  The labels leave and the 13-row laptop terminal fades in while the big command's glyphs fly
    into its two folded rows (the slide is the typing). ▶ your turn. laptop/09 lines 2, …, 15 (cut
    after `@sha256:34386ef0`, folds onto 2 rows), …, 31-34 (hash12), …, 38 (67 columns: soft-wraps
    onto a 14th row, so the log scrolls by one and the first command row goes), printed in chunks
    like a progress log. GREY row tags on the `…` rows: "your terminal: a compact view · this is the full
    log (--progress=plain)" (its flag pulses on "add dash dash progress"), then "default" in line 2
    underlines YELLOW and 'Docker Desktop: builder "desktop-linux" · …' appears under it; last, on
    the bottom `…` row: "stops with toomanyrequests? → wait a while, or docker login (part 2)".
 4  The notes leave. The four sizes turn ORANGE in turn ("four layers"); on "under 50" copies of
    them fly up into a right-aligned list while the terminal shrinks to the 3-row strip (keeping
    the log's tail: `…` and line 38's two rows), summed "≈ 47.6 MB compressed".
    `simple-translate:latest` in line 38 turns TEAL on "saves the result", ":latest" pulses on
    "tagged latest". On "Those four layers" V2 starts, drawn as S05-S09 draw it (S05's layout,
    the stack 0.35 higher): four thin equal ORANGE slabs (TEAL outlines) drop as one group left of the list,
    brace "base image" on their left, `python:3.12-slim-bookworm` (mono, GREY) under the stack.
 5  TRACKER A7 · extra. The list leaves; the strip grows to 5 rows and types
    `docker image inspect simple-translate --format '…'` (row tag `extra`; the quoted format starts
    at column 0, as in S05, and soft-wraps at the terminal edge on the space before WorkingDir=)
    -> laptop/10 line 2. V3: the TEAL config card (stacked: key above slot, S05's size and place,
    top right) appears right of the stack; `null` and `""` copy down from the
    output into the ENTRYPOINT and WorkingDir slots, `["python3"]` into the CMD slot as a tile;
    GREY "inherited from / the base image" points at the CMD row while the base slabs pulse. Just
    before "So we predict" the strip shrinks to its last 3 rows (the 5-row strip leaves no room
    under the stacked card); then, under the card (left-aligned, as in S05), the start-up line
    `python3` copies down from the tile, then "→ >>>" (prediction).
 6  TRACKER A7. The picture leaves except the prediction, which moves top right with "predicted:".
    The terminal clears and grows to 10 rows; `docker run --rm -ti simple-translate` (two rows),
    typed at the pace it is spoken;
    `--rm` underlines with "clean up on exit" under it, `-ti` with "type into it" under it (in the
    empty row 2); ▶ your turn on "Pause and run it". The -ti label leaves just before the output
    takes its row: laptop/11 lines 2-3 (66 and 70 columns: each soft-wraps onto a second row) and
    the `>>>` prompt; GREEN check on the prediction.
    `Python 3.12.15` underlines ORANGE with the row tag "3.12.15 · at the time of recording" under
    it (in the row of the wrapped "x");
    `exit()` is typed (line 4) and the laptop prompt returns.
 7  TRACKER A7 · extra. The strip (5 rows): `git status` (row tag `extra`) -> laptop/12 lines 2-5;
    line 5 YELLOW bar. Top right a YELLOW `Dockerfile` file chip ("you just made it");
    CODE(dot-gitignore.txt: 1–4) slides in left (header `.gitignore · lines 1–4`), line 3 YELLOW,
    tag `erratum`; the file chip dims with "hidden from git"; a GREEN chip `git add -f Dockerfile`
    "to commit it anyway", `-f` pulses as the file chip returns ("hidden from git" leaves). Fade
    out to an empty frame.
"""

import numpy as np  # noqa: I001  (manim first, then common: common must win)
from manim import *

from explainer import style as S
from explainer.devops import code_span, lecture_ref, line_bar
from explainer.scene import VoiceScene

from common import (BUILD, CAT, IMAGE, INK, INSPECT_V1, LAPTOP, MONO, NARRATION, P_LAPTOP, ROUTE,
                    RUN, STRIP_ROWS, SYSTEM, TURN, VENV, ConfigCard, LayerStack, attach, bare_prompt,
                    beside, box, builder_box, capture, check_mark, chip, code, cut, erratum_tag, file_glyph,
                    folder_glyph, glyph_range, hash12, hl_bar, label, laptop_term, mono,
                    mono_line, pin, project_tree, readme_card, resize, route, row_tag, substring,
                    tag, track, tracker_a, travel, type_cmd, under, unpin, your_turn)

SAY = NARRATION["S04"]

# ------------------------------------------------------------------ real outputs (file line numbers)
C08 = capture("08")                                      # laptop/08-dockerfile-v1.txt
assert C08.cmd == CAT, C08.cmd
CAT_OUT = C08.at((2, 3))                                 # the comment + FROM python:3.12-slim-bookworm

C09 = capture("09")                                      # laptop/09-build-v1.txt
assert C09.cmd == BUILD, C09.cmd
B_L2 = C09.line(2)                                       # #0 building with "default" instance …
B_L15 = cut(C09.line(15), "@sha256:34386ef0")            # only laptop/09 and 14 may show 34386ef0
B_SIZES = [hash12(C09.line(n)) for n in range(31, 35)]   # the four base layers
B_L38 = C09.line(38)                                     # #5 unpacking to …simple-translate:latest
SIZES = ["3.34MB", "15.97MB", "28.25MB", "249B"]
assert all(s in ln for s, ln in zip(SIZES, B_SIZES)) and '"default"' in B_L2
assert "simple-translate:latest" in B_L38

C10 = capture("10")                                      # laptop/10-config-v1.txt
assert C10.cmd == INSPECT_V1, C10.cmd
CFG = C10.line(2)
assert CFG == 'Entrypoint=null Cmd=["python3"] WorkingDir=""', CFG

C11 = capture("11")                                      # laptop/11-run-v1.txt
assert C11.cmd == RUN, C11.cmd
REPL_OUT = C11.at((2, 3))                                # Python 3.12.15 (main, …) / Type "help", …
REPL_PROMPT, REPL_TYPED = ">>>", "exit()"
assert C11.line(4) == f"{REPL_PROMPT} {REPL_TYPED}" and "Python 3.12.15" in REPL_OUT[0]

C12 = capture("12")                                      # laptop/12-git-status.txt
GIT_STATUS = "git status"                                # extra (not in the README)
assert C12.cmd == GIT_STATUS, C12.cmd
GIT_OUT = C12.at((2, 5))
assert GIT_OUT[-1] == "nothing to commit, working tree clean"

GIT_ADD_F = "git add -f Dockerfile"                      # said, not run
P = P_LAPTOP + " "

# ------------------------------------------------------------------ layout (S05's, so V2/V3 look the same)
STACK_X, FLOOR_Y = -3.0, 0.1         # the V2 stack (3.2 wide; its left brace label stays in frame),
                                      # 0.35 above S05's floor: its caption clears beat 5's 5-row strip
CARD_W, CARD_RIGHT, CARD_TOP = 3.4, 6.5, 3.4   # S05's stacked config card, clear of the tracker caption

# `docker image inspect …` folded for a 65-column row: house folds (" \") at the two spaces outside
# the quotes, then the quoted format starts a row at column 0 (as in S05) and soft-wraps at the
# terminal edge like a real terminal (no "\"). Column 65 is the space before WorkingDir=, so the
# wrap splits no token. Terminal.fold would put " \" inside the quotes and drop a character there.
_FMT = INSPECT_V1[INSPECT_V1.index("'"):]
assert _FMT[64] == " ", _FMT[:65]
INSPECT_ROWS = [P + "docker image inspect \\", "    simple-translate --format \\", _FMT[:64], _FMT[65:]]
assert "docker image inspect simple-translate --format " + " ".join(INSPECT_ROWS[2:]) == INSPECT_V1
assert all(len(r) <= 65 for r in INSPECT_ROWS)


# ------------------------------------------------------------------ helpers
def lead(vo, phrase: str, early: float) -> None:
    """Wait until `early` seconds before `phrase` is spoken (a typed command lands on its words)."""
    dt = vo.time_until(phrase) - early
    if dt > 1 / 60:
        vo.scene.wait(dt)


def row_y(t, i: int) -> float:
    """Centre height of text row i of terminal t (wherever the terminal is now)."""
    ln = mono_line("|", t.size)
    t._place(ln, i)
    return ln.strut.get_center()[1]


def at_row(mob, t, i: int, x: float | None = None):
    """Left edge at x (default: the terminal's text column), centred on row i."""
    x = t._slot(0)[0] if x is None else x
    return mob.move_to([x + mob.width / 2, row_y(t, i), 0])


def turn_tag() -> VGroup:
    """YELLOW '▶ your turn', the height of a terminal row."""
    return row_tag("▶ your turn", TURN)


def make_rows(t, texts: list[str]) -> list:
    """Rows of a typed command (texts[0] starts with the prompt), placed as t's next lines (not added)."""
    t2c = t._prompt_colors(t.prompt)
    rows = []
    for k, s in enumerate(texts):
        ln = mono_line(s, t.size, INK, t2c=t2c if k == 0 else None)
        t._place(ln, len(t.lines))
        t.lines.add(ln)
        rows.append(ln)
    return rows


def type_rows(scene, t, texts: list[str], type_time: float) -> VGroup:
    """Terminal.type with rows folded by hand (see INSPECT_ROWS). Returns the rows (.rows)."""
    p = t.prompt + " "
    t._make_room(scene, len(texts))
    rows = make_rows(t, texts)
    scene.add(glyph_range(rows[0], 0, len(p)))
    typed = VGroup(*glyph_range(rows[0], len(p)), *[g for r in rows[1:] for g in glyph_range(r, 0)])
    scene.play(ShowIncreasingSubsets(typed, rate_func=linear), run_time=type_time)
    for r in rows:
        scene.add(r)
    g = VGroup(*rows)
    g.rows = rows
    return g


def text_span(t: Text, s: str, sub: str, occurrence: int = 0) -> VGroup:
    """The glyphs of `sub` in a one-line Text made from string `s` (spaces have no glyphs)."""
    i = -1
    for _ in range(occurrence + 1):
        i = s.find(sub, i + 1)
    if i < 0:
        raise ValueError(f"{sub!r} not in {s!r}")
    a, n = len("".join(s[:i].split())), len("".join(sub.split()))
    return VGroup(*t.submobjects[a:a + n])


def editor_sidebar(tree) -> VGroup:
    """A schematic editor's file sidebar (no product look): title bar 'files' + the tree. .frame
    .title .tag .tree"""
    w, bar_h = 4.75, 0.5
    h = tree.height + bar_h + 0.55
    frame = box(w, h, S.GREY_DARK, fill=S.GREY_DARKER, fill_opacity=1, radius=0.16)
    bar = Line(frame.get_corner(UL) + DOWN * bar_h, frame.get_corner(UR) + DOWN * bar_h,
               color=S.GREY_DARK, stroke_width=2)
    title = label("files", 20, S.GREY).move_to(frame.get_corner(UL) + np.array([0.55, -bar_h / 2, 0]))
    ill = row_tag("illustration")
    ill.move_to(frame.get_corner(UR) + np.array([-0.15 - ill.width / 2, -bar_h / 2, 0]))
    tree.move_to(frame).align_to(frame, LEFT).shift(RIGHT * 0.3)
    tree.align_to(bar, UP).shift(DOWN * 0.28)
    g = VGroup(frame, bar, title, ill, tree)
    g.frame, g.bar, g.title, g.tag, g.tree = frame, bar, title, ill, tree
    return g


def name_chip(word: str, meaning: str, color) -> VGroup:
    """A decoded part of the image name: mono chip in its colour over a short meaning. .chip .meaning"""
    c = chip(word, color, size=22, font=MONO)
    m = label(meaning, 22, INK).next_to(c, DOWN, buff=0.14)
    g = VGroup(c, m)
    g.chip, g.meaning = c, m
    return g


def two_lines(a: str, b: str, size: float = 20, color=S.GREY) -> VGroup:
    return VGroup(label(a, size, color), label(b, size, color)).arrange(DOWN, buff=0.08)


# ------------------------------------------------------------------ the scene
class StepFrom(VoiceScene):
    def construct(self):
        assert len(SAY) == 8, f"S04 has {len(SAY)} SAY lines; this scene times 8"

        tr = tracker_a(5)

        # ========================================================== 0 · create a file called Dockerfile
        tree = project_tree(new="Dockerfile")
        side = editor_sidebar(tree)
        side.move_to([-6.3 + side.width / 2, 2.72 - side.height / 2, 0])
        rows = list(tree.rows)
        new_row = tree.row("Dockerfile")
        k_new = rows.index(new_row)
        pitch = rows[k_new].get_center()[1] - rows[k_new + 1].get_center()[1]     # > 0
        below = VGroup(*rows[k_new + 1:])
        below.shift(UP * pitch)                     # room is made when the file appears

        card_lines = VGroup(
            label("Inside the simple-translate folder", 22, INK, t2f={"simple-translate": MONO}),
            label("create a file called Dockerfile", 22, INK, t2f={"Dockerfile": MONO}),
            label("… (Do a Build + Run after each step):", 22, INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        card0 = readme_card((128, 130), card_lines)
        card0.move_to([6.3 - card0.width / 2, 2.72 - card0.height / 2, 0])
        each = text_span(card_lines[2], "… (Do a Build + Run after each step):",
                         "(Do a Build + Run after each step)")
        each_ul = under(each, TURN, y=each.get_bottom()[1] - 0.07)

        exact = tag("exactly this name · no extension", S.GREY)
        exact.move_to([side.frame.get_right()[0] + 0.55 + exact.width / 2, new_row.get_center()[1], 0])
        exact_arrow = Arrow(exact.get_left() + LEFT * 0.05,
                            [new_row.name_text.get_right()[0] + 0.15, new_row.get_center()[1], 0],
                            buff=0, color=S.GREY, stroke_width=3, tip_length=0.16,
                            max_tip_length_to_length_ratio=0.3)
        yt0 = your_turn().next_to(exact, DOWN, buff=0.35).align_to(exact, LEFT)
        five = VGroup(*tr.dots[6:11])

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.1), run_time=0.5)
            self.play(track(tr, 6), FadeIn(VGroup(side.frame, side.bar, side.title, side.tag)),
                      FadeIn(VGroup(*rows[:k_new]), below), run_time=0.7)
            self.play(Indicate(rows[0].name_text, color=TURN, scale_factor=1.12), run_time=0.7)
            self.play(FadeIn(card0, shift=DOWN * 0.15), run_time=0.6)
            vo.wait_until("create a file called")
            self.play(below.animate.shift(DOWN * pitch), FadeIn(new_row, shift=RIGHT * 0.4), run_time=0.7)
            self.play(Indicate(text_span(card_lines[1], "create a file called Dockerfile", "Dockerfile"),
                               color=TURN, scale_factor=1.15), run_time=0.7)
            vo.wait_until("capital D")
            self.play(Indicate(glyph_range(new_row.name_text, 0, 1), color=TURN, scale_factor=1.8), run_time=0.7)
            vo.wait_until("no extension")
            self.play(GrowArrow(exact_arrow), FadeIn(exact, shift=LEFT * 0.2), run_time=0.6)
            vo.wait_until("The README fills")
            self.play(LaggedStart(*[Indicate(d, color=TURN, scale_factor=2.0) for d in five], lag_ratio=0.25),
                      run_time=1.2)
            vo.wait_until("with a build and a run")
            self.play(Create(each_ul), run_time=0.6)
            lead(vo, "Pause and create", 0.3)
            self.play(FadeIn(yt0, shift=UP * 0.1), run_time=0.4)
            self.play(Wiggle(yt0, scale_value=1.15, rotation_angle=0.025 * TAU), run_time=0.7)

        # ========================================================== 1 · FROM python:3.12-slim-bookworm
        panel = code("README.md", 135, 136, "docker")
        panel.move_to([0, 2.78 - panel.height / 2, 0])
        src = panel.code
        bar1 = line_bar(src, 1, TURN, 0.16)
        parts = [("python", "official image", IMAGE), ("3.12", "Python 3.12", SYSTEM),
                 ("slim", "fewer packages", SYSTEM), ("bookworm", "Debian 12", SYSTEM)]
        spans = [code_span(src, 1, w) for w, _, _ in parts]
        uls = [under(sp, col, stroke=4, y=src.code_lines[1].get_bottom()[1] - 0.08)
               for sp, (_, _, col) in zip(spans, parts)]
        chips = [name_chip(w, m, col) for w, m, col in parts]
        for c, x in zip(chips, (-4.6, -1.55, 1.55, 4.6)):
            c.shift(np.array([x, 0.3, 0]) - c.chip.get_center())     # chips in one row, meanings under
        links = [Line([sp.get_center()[0], u.get_bottom()[1] - 0.08, 0], c.chip.get_top() + UP * 0.08,
                      color=col, stroke_width=2, stroke_opacity=0.8)
                 for sp, u, c, (_, _, col) in zip(spans, uls, chips, parts)]

        strip = laptop_term(STRIP_ROWS)

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(side, below, new_row, card0, each_ul, exact, exact_arrow, yt0),
                              shift=UP * 0.1), track(tr, 7), run_time=0.5)
            self.play(FadeIn(panel, shift=DOWN * 0.15), run_time=0.6)
            vo.wait_until("one instruction")
            self.play(FadeIn(bar1), Indicate(code_span(src, 1, "FROM"), color=TURN, scale_factor=1.2),
                      run_time=0.7)
            vo.wait_until("FROM python")
            self.play(Create(uls[0]), run_time=0.4)
            vo.wait_until("3.12, slim")
            self.play(Create(uls[1]), run_time=0.3)
            vo.wait_until("slim bookworm")
            self.play(Create(uls[2]), run_time=0.3)
            self.play(Create(uls[3]), run_time=0.3)
            vo.wait_until("That's the official")
            self.play(*[Create(ln) for ln in links[:2]],
                      *[FadeIn(c, shift=DOWN * 0.2) for c in chips[:2]], run_time=0.7)
            vo.wait_until("on a slim")
            self.play(Create(links[2]), FadeIn(chips[2], shift=DOWN * 0.2), run_time=0.6)
            vo.wait_until("Debian 12")
            self.play(Create(links[3]), FadeIn(chips[3], shift=DOWN * 0.2), run_time=0.6)
            vo.wait_until("called bookworm")
            self.play(Indicate(spans[3], color=SYSTEM, scale_factor=1.15),
                      Indicate(chips[3].chip, color=SYSTEM, scale_factor=1.1), run_time=0.7)
            vo.wait_until("Paste it in")
            self.play(FadeIn(strip), track(tr, 7, extra=True), run_time=0.5)
            bare_prompt(self, strip)
            lead(vo, "check with cat", 0.4)
            c1 = type_cmd(self, strip, CAT, 0.5)
            pin(self, c1, beside(row_tag("extra"), c1), run_time=0.3)
            strip.print(self, CAT_OUT, run_time=0.4)

        # ========================================================== 2 · the build command, part by part
        big = mono_line(BUILD, 28, INK)
        big.move_to([0, 1.45, 0])
        head2 = VGroup(mono("README.md", 20, S.GREY), label("· line 174", 20, S.GREY)).arrange(RIGHT, buff=0.12)
        head2.next_to(big, UP, buff=0.4).align_to(big, LEFT)
        g_name, g_recipe, g_dot = (substring(big, "-t simple-translate"), substring(big, "-f Dockerfile"),
                                   glyph_range(big, len(BUILD) - 1))
        ul_name = under(g_name, IMAGE, y=big.strut.get_bottom()[1] - 0.04)
        ul_recipe = under(g_recipe, INK, y=big.strut.get_bottom()[1] - 0.04)
        lab_name = label("the image's name", 24, IMAGE).next_to(ul_name, DOWN, buff=0.22)
        lab_recipe = label("the recipe", 24, INK).next_to(ul_recipe, DOWN, buff=0.22)
        ring = Circle(radius=0.22, color=ROUTE, stroke_width=4).move_to(g_dot)
        lab_ctx = label("build context: this folder", 24, ROUTE)
        lab_ctx.move_to([5.05 - lab_ctx.width / 2, -0.15, 0])
        folder = folder_glyph(0.5, LAPTOP).move_to(g_dot)
        builder = builder_box("builder", 2.1, 0.95, 24)
        builder.move_to([5.2, -2.45, 0])
        path2 = route(ring.get_bottom() + DOWN * 0.08, builder.frame.get_top() + UP * 0.05, arc=-0.35)
        lref = lecture_ref(2, "32, 56")                     # top right, bottom at 3.13 (all else < 2.8,
                                                            # the 13-row terminal's top at 2.59)

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(panel, bar1, *uls, *links, *chips), shift=UP * 0.1),
                      FadeOut(strip), track(tr, 7), run_time=0.5)
            self.play(FadeIn(head2), ShowIncreasingSubsets(big.glyphs, rate_func=linear), run_time=1.0)
            vo.wait_until("Dash t names")
            self.play(Create(ul_name), substring(big, "simple-translate").animate.set_color(IMAGE), FadeIn(lref),
                      run_time=0.5)
            self.play(FadeIn(lab_name, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("dash f picks")
            self.play(Create(ul_recipe), run_time=0.5)
            self.play(FadeIn(lab_recipe, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("And the final dot")
            self.play(g_dot.animate.set_color(ROUTE), Create(ring), run_time=0.5)
            self.play(Indicate(ring, color=ROUTE, scale_factor=1.4), run_time=0.6)
            vo.wait_until("the build context")
            self.play(FadeIn(lab_ctx, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("this folder")
            self.play(GrowFromCenter(folder), run_time=0.5)
            vo.wait_until("which Docker sends")
            self.play(Create(path2), FadeIn(builder, shift=UP * 0.1), run_time=0.6)
            self.play(travel(folder, path2.copy(), run_time=1.1))
            self.play(folder.animate.move_to(builder.frame.get_center() + LEFT * 0.62).scale(0.8),
                      builder.text.animate.shift(RIGHT * 0.3), run_time=0.4)
            vo.wait_until("Step 3 shows")
            self.play(Indicate(tr.dots[8], color=TURN, scale_factor=2.2),
                      Indicate(ring, color=ROUTE, scale_factor=1.3), run_time=0.9)

        # ========================================================== 3 · the build, the full log
        t = laptop_term(13)
        texts = t.fold(P + BUILD, first_prefix=len(P))
        assert len(texts) == 2 and texts[0].endswith(" \\")

        # the command's rows, placed but not yet in t.lines (so FadeIn(t) below leaves them alone)
        t2c = t._prompt_colors(t.prompt)
        r0, r1 = [mono_line(s, t.size, INK, t2c=t2c if k == 0 else None) for k, s in enumerate(texts)]
        t._place(r0, 0)
        t._place(r1, 1)
        typed = VGroup(*glyph_range(r0, len(P), len(texts[0]) - 2), *glyph_range(r1, 0))
        assert len(typed) == len(big.glyphs)

        with self.voiceover(SAY[3]) as vo:
            # the labels leave and the terminal appears while the command flies into its rows
            self.play(FadeOut(VGroup(head2, ul_name, ul_recipe, lab_name, lab_recipe, ring, lab_ctx, folder,
                                     builder, path2)), FadeIn(t),
                      *[ReplacementTransform(a, b) for a, b in zip(big.glyphs, typed)],
                      FadeIn(glyph_range(r0, 0, len(P))), FadeIn(glyph_range(r0, len(texts[0]) - 1)),
                      run_time=0.9)
            t.lines.add(r0, r1)
            self.remove(*typed)
            self.add(r0, r1)
            yt3 = beside(turn_tag(), r1)
            pin(self, r1, yt3, run_time=0.3)
            self.play(Wiggle(yt3, scale_value=1.15, rotation_angle=0.025 * TAU), run_time=0.5)
            vo.wait_until("Your terminal shows")
            o2 = t.print(self, [B_L2, "…"], run_time=0.4)
            o15 = t.print(self, [B_L15], wrap=True, run_time=0.3)
            dots6 = t.print(self, ["…"], run_time=0.2)[0]
            o_sz = t.print(self, B_SIZES, run_time=1.0, lag=0.3)
            # line 38 (67 columns) soft-wraps onto a 14th row: the log scrolls by one (the first
            # command row goes, as in a real terminal); nothing of the line is cut
            dots11, o38, o38b = t.print(self, ["…", B_L38], wrap=True, run_time=0.4)
            assert o15[0].text.endswith("@sha256:") and o15[1].text == "34386ef0…"
            assert o38.text + o38b.text == B_L38 and r0 not in t.lines
            vo.wait_until("Here you see")
            note_c = row_tag([("your terminal: a compact view · this is the full log", "label"),
                              ("(--progress=plain)", "mono")])
            pin(self, dots6, beside(note_c, dots6), run_time=0.5)
            vo.wait_until("add dash dash progress")
            self.play(Indicate(note_c.text[1], color=TURN, scale_factor=1.15), run_time=0.8)
            note_r = row_tag([("stops with", "label"), ("toomanyrequests", "mono"),
                              ("? → wait a while, or", "label"), ("docker login", "mono"), ("(part 2)", "label")])
            self.wait(0.3)
            pin(self, dots11, beside(note_r, dots11), run_time=0.5)
            vo.wait_until("On Docker Desktop")
            l2 = o2[0]
            ul_def = under(substring(l2, '"default"'), TURN, y=l2.strut.get_bottom()[1] - 0.01)
            self.play(Create(ul_def), run_time=0.4)
            attach(self, l2, ul_def)
            note_d = row_tag([("Docker Desktop: builder", "label"), ('"desktop-linux"', "mono"),
                              ('· and a "View build details" link at the end', "label")])
            pin(self, o2[1], beside(note_d, o2[1]), run_time=0.5)
            vo.wait_until("not default")
            self.play(Indicate(substring(l2, '"default"'), color=TURN, scale_factor=1.2), run_time=0.6)

        # ========================================================== 4 · four base layers, the stack
        # the V2 stack as S05-S09 draw it: brace on the left, GREY caption, S05's place
        stack = LayerStack(stack_w=3.2)
        stack.floor.move_to([STACK_X, FLOOR_Y, 0])
        base = [stack.make(None, SYSTEM, 0.15) for _ in range(4)]
        br = stack.brace(base, "base image")
        cap = mono("python:3.12-slim-bookworm", 20, S.GREY)
        cap.next_to(stack.floor, DOWN, buff=0.12)

        sz_targets = VGroup(*[mono(s, 20, SYSTEM) for s in SIZES]).arrange(DOWN, buff=0.14, aligned_edge=RIGHT)
        # right edge at 1.4: the total under the list stays well apart from the stack's caption
        sz_targets.move_to([1.4 - sz_targets.width / 2, 0.95, 0]).align_to([1.4, 0, 0], RIGHT)
        rule = Line(sz_targets.get_corner(DR) + np.array([0.05, -0.12, 0]),
                    sz_targets.get_corner(DR) + np.array([-1.3, -0.12, 0]), color=SYSTEM, stroke_width=2)
        total = label("≈ 47.6 MB compressed", 22, SYSTEM)
        total.next_to(rule, DOWN, buff=0.14).align_to(rule, LEFT)

        with self.voiceover(SAY[4]) as vo:
            unpin(self, [(dots6, note_c), (o2[1], note_d), (dots11, note_r), (r1, yt3)], 0.3,
                  FadeOut(lref))                     # the tag stays through the build (script.md)
            vo.wait_until("four layers")
            sz_glyphs = [substring(row, s) for row, s in zip(o_sz, SIZES)]
            self.play(LaggedStart(*[g.animate.set_color(SYSTEM) for g in sz_glyphs], lag_ratio=0.35),
                      run_time=1.0)
            copies = [g.copy() for g in sz_glyphs]
            self.add(*copies)
            vo.wait_until("under 50")
            resize(self, t, STRIP_ROWS, keep=[dots11, o38, o38b], run_time=0.8,
                   extra=[ReplacementTransform(c, s) for c, s in zip(copies, sz_targets)])
            self.play(Create(rule), FadeIn(total, shift=UP * 0.1), run_time=0.5)
            lead(vo, "and saves the result", 0.2)
            name38 = substring(o38, "simple-translate:latest")
            self.play(name38.animate.set_color(IMAGE), run_time=0.5)
            self.play(Indicate(name38, color=IMAGE, scale_factor=1.12), run_time=0.6)
            vo.wait_until("tagged latest")
            self.play(Indicate(substring(o38, ":latest"), color=IMAGE, scale_factor=1.12), run_time=0.6)
            vo.wait_until("Those four layers")          # the narrated thing: the base slabs land now
            stack.drop(self, *base, run_time=0.8)
            self.play(GrowFromCenter(br.brace), FadeIn(br.text), FadeIn(cap, shift=UP * 0.1), run_time=0.6)

        # ========================================================== 5 · inspect: the config card (V3)
        card = ConfigCard(card_w=CARD_W)                 # the stacked card, where S05 shows it
        card.shift(np.array([CARD_RIGHT - card.frame.get_right()[0], CARD_TOP - card.frame.get_top()[1], 0]))
        n_entry = card.note("ENTRYPOINT", "null")
        n_wd = card.note("WorkingDir", '""')
        cmd_tile = card.place("CMD", card.tile('["python3"]'))
        cmd_y = card.slots["CMD"].get_center()[1]
        inh = two_lines("inherited from", "the base image")
        inh.move_to([card.frame.get_left()[0] - 0.55 - inh.width / 2, cmd_y, 0])
        inh_arrow = Arrow(inh.get_right() + RIGHT * 0.06, [card.frame.get_left()[0] - 0.04, cmd_y, 0],
                          buff=0, color=S.GREY, stroke_width=3, tip_length=0.15,
                          max_tip_length_to_length_ratio=0.5)
        start = card.startup("python3", buff=0.22).align_to(card.frame, LEFT)   # where S05 has it
        spot = np.array([start.get_left()[0], start.get_center()[1], 0])
        arr = label("→", 26, S.GREY)
        repl = chip(">>>", SYSTEM, size=20, font=MONO, pad_y=0.08)
        pred = VGroup(start, arr, repl).arrange(RIGHT, buff=0.25)
        pred.shift(spot - np.array([start.get_left()[0], start.get_center()[1], 0]))

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(sz_targets, rule, total), shift=UP * 0.1), track(tr, 7, extra=True),
                      run_time=0.4)
            t.clear(self)
            resize(self, t, 5, run_time=0.6)
            self.play(Indicate(VGroup(*base), color=IMAGE, scale_factor=1.05), run_time=0.7)
            lead(vo, "An extra docker image inspect", 0.1)
            c5 = type_rows(self, t, INSPECT_ROWS, 1.4)
            pin(self, c5.rows[1], beside(row_tag("extra"), c5.rows[1]), run_time=0.3)
            out5 = t.print(self, [CFG], run_time=0.3)[0]
            vo.wait_until("reads the config card")
            self.play(FadeIn(card, shift=LEFT * 0.2), run_time=0.6)
            vo.wait_until("no entrypoint")
            self.play(TransformFromCopy(substring(out5, "null"), n_entry), run_time=0.5)
            self.play(Indicate(card.keys["ENTRYPOINT"], color=IMAGE, scale_factor=1.1), run_time=0.4)
            self.play(TransformFromCopy(substring(out5, '""'), n_wd), run_time=0.35)
            vo.wait_until("and the command python3")
            self.play(TransformFromCopy(substring(out5, '["python3"]'), cmd_tile), run_time=0.7)
            vo.wait_until("inherited from the base")
            self.play(FadeIn(inh, shift=RIGHT * 0.15), GrowArrow(inh_arrow),
                      LaggedStart(*[Indicate(s, color=SYSTEM, scale_factor=1.06) for s in base], lag_ratio=0.15),
                      run_time=0.9)
            # the strip shrinks to its last 3 rows, so the start-up line has S05's place under the card
            lead(vo, "So we predict", 0.8)
            resize(self, t, STRIP_ROWS, run_time=0.5)
            vo.wait_until("So we predict")
            self.play(TransformFromCopy(cmd_tile.text, start), run_time=0.6)
            self.play(FadeIn(arr, shift=RIGHT * 0.1), FadeIn(repl, scale=0.8), run_time=0.5)

        # ========================================================== 6 · docker run: the Python prompt
        said = label("predicted:", 22, S.GREY)
        pred_to = VGroup(said, pred.copy()).arrange(RIGHT, buff=0.3)
        pred_to.move_to([5.7 - pred_to.width / 2, 2.2, 0])
        tick = check_mark(0.36, VENV).next_to(pred_to, RIGHT, buff=0.22)

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(stack, br, cap, card, n_entry, n_wd, cmd_tile, inh, inh_arrow)),
                      pred.animate.move_to(pred_to[1]), FadeIn(said, shift=LEFT * 0.1), track(tr, 7),
                      run_time=0.7)
            t.clear(self)
            resize(self, t, 10, run_time=0.6)
            lead(vo, "docker run, dash", 0.15)
            c6 = type_cmd(self, t, RUN, 3.3)                 # typed as it is spoken
            r6a, r6b = c6.rows
            vo.wait_until("Dash dash rm cleans")
            g_rm = substring(r6a, "--rm")
            u_rm = under(g_rm, INK, y=r6a.strut.get_bottom()[1] - 0.01)
            l_rm = at_row(row_tag("clean up on exit"), t, 1, x=g_rm.get_left()[0] - 0.1)
            self.play(Create(u_rm), run_time=0.4)
            attach(self, r6a, u_rm)
            pin(self, r6b, l_rm, run_time=0.4)
            vo.wait_until("dash t i lets")
            g_ti = substring(r6b, "-ti")
            u_ti = under(g_ti, INK, y=r6b.strut.get_bottom()[1] - 0.01)
            l_ti = at_row(row_tag("type into it"), t, 2, x=g_ti.get_left()[0] - 0.1)
            self.play(Create(u_ti), run_time=0.4)
            attach(self, r6b, u_ti)
            self.play(FadeIn(l_ti, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("Pause and run it")
            yt6 = beside(turn_tag(), r6a)
            pin(self, r6a, yt6, run_time=0.3)
            self.play(Wiggle(yt6, scale_value=1.15, rotation_angle=0.025 * TAU), run_time=0.6)
            vo.wait_until("There's the Python prompt")
            self.play(FadeOut(l_ti), run_time=0.25)          # its row is where the output goes
            o6 = t.print(self, REPL_OUT, wrap=True, run_time=0.4)    # 66 and 70 columns: 4 rows
            assert [o6[0].text + o6[1].text, o6[2].text + o6[3].text] == REPL_OUT
            t.set_prompt(REPL_PROMPT)
            p6 = bare_prompt(self, t)
            self.play(Indicate(substring(p6, ">>>"), color=SYSTEM, scale_factor=1.5),
                      Indicate(repl, color=SYSTEM, scale_factor=1.2), run_time=0.7)
            self.play(Create(tick), run_time=0.4)
            vo.wait_until("3.12.15 at the time")
            g_ver = substring(o6[0], "Python 3.12.15")
            u_ver = under(g_ver, SYSTEM, y=o6[0].strut.get_bottom()[1] - 0.01)
            self.play(Create(u_ver), run_time=0.4)
            attach(self, o6[0], u_ver)
            rec = row_tag([("3.12.15", "mono"), ("· at the time of recording", "label")])
            at_row(rec, t, 3, x=substring(o6[0], "3.12.15").get_left()[0] - 0.1)   # under the version,
            self.play(FadeIn(rec, shift=LEFT * 0.1), run_time=0.4)   # in the row of the wrapped "x"
            vo.wait_until("Type exit with")
            type_cmd(self, t, REPL_TYPED, 0.5)
            t.set_prompt(P_LAPTOP)
            bare_prompt(self, t)

        # ========================================================== 7 · git status: .gitignore hides it
        gi = code("dot-gitignore.txt", 1, 4)
        gi.move_to([-4.2, 1.35, 0])
        gi_bar = line_bar(gi.code, 2, TURN, 0.22)
        err7 = erratum_tag().next_to(gi.code, RIGHT, buff=0.25).set_y(gi.code.code_lines[2].get_center()[1])
        fchip = VGroup(file_glyph(0.36, TURN), mono("Dockerfile", 22, TURN)).arrange(RIGHT, buff=0.16)
        fchip.move_to([3.0, 2.25, 0])
        made = label("you just made it", 20, S.GREY).next_to(fchip, DOWN, buff=0.14)
        hidden = label("hidden from git", 20, S.GREY).move_to(made)
        add_f = chip(GIT_ADD_F, VENV, size=22, font=MONO)
        add_f.move_to([3.0, 0.75, 0])
        anyway = label("to commit it anyway", 20, S.GREY).next_to(add_f, DOWN, buff=0.14)

        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(said, pred, tick, rec)), FadeOut(t.lines), track(tr, 7, extra=True),
                      run_time=0.4)                          # the picture and the run's rows go together
            for m in list(t.lines):
                t.lines.remove(m)
            resize(self, t, 5, run_time=0.45)
            lead(vo, "an extra git status", 0.2)
            c7 = type_cmd(self, t, GIT_STATUS, 0.5)
            pin(self, c7, beside(row_tag("extra"), c7), run_time=0.3)
            o7 = t.print(self, GIT_OUT, run_time=0.5)
            vo.wait_until("says nothing to commit")
            l5 = o7[-1]
            bar5 = hl_bar(l5.glyphs, TURN, 0.25)
            l5.add_to_back(bar5)
            self.add(l5)
            self.play(FadeIn(bar5), Indicate(l5.glyphs, color=INK, scale_factor=1.06), run_time=0.6)
            vo.wait_until("though we just made")
            self.play(FadeIn(fchip, shift=DOWN * 0.15), FadeIn(made), run_time=0.5)
            vo.wait_until("The gitignore file")
            self.play(FadeIn(gi, shift=RIGHT * 0.3), run_time=0.6)
            vo.wait_until("lists Dockerfile on line 3")
            self.play(FadeIn(gi_bar), Indicate(gi.code.code_lines[2], color=TURN, scale_factor=1.15),
                      run_time=0.7)
            self.play(FadeIn(err7, scale=1.3), run_time=0.4)
            vo.wait_until("so git hides yours")
            fchip.save_state()
            self.play(fchip.animate.fade(0.7), ReplacementTransform(made, hidden), run_time=0.6)
            vo.wait_until("To commit it anyway")
            self.play(FadeIn(add_f, shift=UP * 0.15), FadeIn(anyway), run_time=0.6)
            vo.wait_until("use git add dash f")
            self.play(Indicate(text_span(add_f.text, GIT_ADD_F, "-f"), color=TURN, scale_factor=1.6),
                      Restore(fchip), FadeOut(hidden), run_time=0.8)   # no longer hidden once added

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
