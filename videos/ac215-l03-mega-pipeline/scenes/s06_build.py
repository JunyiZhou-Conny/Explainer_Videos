r"""S06 · Build: five steps, one fat layer (README › transcribe_audio step 5; V2 sizes; PONDER 2).

The house terminal is 13 rows here (script: 14): with BOTTOM fixed at -3.5 a 14-row terminal
would run into the tracker band. Beat 1 and beat 5 shrink it to a strip so a picture fits above.

Beats (script.md "## S06", one voiceover block each):
 0  TRACKER A4 -> A5 · extra. Terminal (13 rows, laptop, transcribe_audio prompt) types `ls -a`
    (extra; the capture's `; git status` half is not typed) -> 11-ls-before-build.txt lines 2-9;
    `Dockerfile` and then `pyproject.toml` turn GREEN with a GREEN bar, as named.
 1  TRACKER A5. The terminal clears and shrinks to the 3-row strip. Under the tracker band the
    README chip `transcribe_audio/README.md · line 95` "give your image the name transcribe_audio"
    (11.5 wide: it can't sit right of the tracker), GREY tag "erratum · no command given" above
    its right end. It types `docker build -t transcribe_audio .` (folds after `build`), no Enter.
    `-t transcribe_audio` underlines GREY with "the image's name" on the row below; the final `.`
    underlines PINK with "this folder = the build context". As the PINK label lands the
    transcribe_audio/ folder (GREY, its files and a tiny GOLD key) appears above the strip; copies
    of its files pack into lecture 2's parcel "build context" (1.5 s), which slides to a PURPLE
    "builder" box.
 2  Enter: the picture, the chip and the labels go; ▶ your turn beside the command ("Pause and run
    it"); the terminal grows to 13 rows, its title becomes "laptop · the same build, full log";
    top right, the GREY caption "your terminal shows a compact live view; / this is the full log
    (--progress=plain)". TERM(12-build.txt: 9, 23, …, 148-149, …, 1368, 1375, 1377): `[2/5]` gets a
    TEAL box and the TEAL badge "build step 2" on the `…` row under it; `237 newly installed` and
    `205 MB` underline ORANGE, `uv-0.13.0` turns PURPLE, `DONE 46.9s` underlines YELLOW; GREY note
    beside it: "first build: Docker also pulls python:3.12-slim-bookworm".
 3  TERM(12-build.txt: 1379, 1382) with badges "build step 3", "build step 4" (and `[k/5]` TEAL);
    then 1385-1388 (wrap: 1386 folds): badge "build step 5"; line 1386 underlines ORANGE, line
    1387's `/home/app/.venv` turns GREEN, a GREY tag "only the project itself" beside line 1388.
 4  TERM(12-build.txt: …, 1399, …, 1404-1405; wrap) (printed here, on "It ends by naming"): line
    1399 gets a GREEN bar; lines 1404-1405 a GREY bar. The live-view caption goes and the terminal
    shrinks to its last 6 rows; above it CODE(files/transcribe_audio.Dockerfile: 10), headed
    `transcribe_audio/Dockerfile · line 10` (the GREY "from transcribe_audio/README.md / lines
    41–90" caption top right, as in S05), whose header's "line 10" grows out of the warning's
    `(line 10)`. `CREDENTIALS` underlines YELLOW; the value `secrets/mega-pipeline.json` underlines
    PINK; GREY tag "a name check · harmless here"; the warning rows pulse on "every build".
 5  TRACKER A5 · extra. The inset goes, the terminal clears (title "laptop") and shrinks to a
    4-row strip (the command folds onto 2 rows) while V2 fades in above it, as S05 left it. It
    types `docker images transcribe_audio` (extra) -> 13-images.txt lines 2-3 (cut at 65: "357…");
    `1.35GB` gets a YELLOW bar; a GREY brace "≈ 1 GB of layers" + note "+ 357 MB compressed copy /
    = 1.35 GB disk usage · this machine". On "By far the biggest" the apt slab swells and reads
    `842MB` (17-history.txt line 9) while the empty uv sync slab thins to a hairline (the brace
    follows); the thin GREY COPY slab pulses on "the copied folder is tiny". The five slabs take
    TEAL badges 1-5 (fanned, with leader lines: three slabs are thin).
 6  TRACKER A5. The strip and the brace go. Bottom: a RED-bordered panel, header "if you skipped uv
    init", GREY tag "illustration · what if", TERM(26-g21-no-pyproject.txt: 34, 51) in RED (folded
    at spaces to the panel's 66 characters). On "build step 5 fails" badge 5 and the sync slab
    flash RED.
 7  The panel fades. A GREY chip "edit: group_name in cli.py" hovers right of the stack; the five
    badges pulse on "which of the five". After the SAY: PONDER (8 s) at the bottom, "You change only group_name in cli.py / and build again. /
    Which of the five build steps run again?".
 8  The card goes. The chip drops into the COPY slab, which flashes YELLOW; V2 settles nearer
    the centre (the bottom band is free) and badges 4, 5 turn YELLOW; the COPY slab and then the
    uv sync slab dissolve and re-form; badges 1-3 turn GREEN and the apt and WORKDIR slabs get
    GREEN "CACHED" stamps (the base slab stays as is). GREY caption "part 2: for real" under the
    floor. Fade out: empty frame.
"""

import numpy as np
from manim import *

from explainer import style as S
from explainer.components import ponder_card
from explainer.devops import (cell_width, code_span, file_glyph, folder_glyph, label, line_pitch, mono,
                              step_badge, substring, tag)
from explainer.scene import VoiceScene

from common import (CTR, ERR, INK, LAPTOP, LOOKUP, NARRATION, P_A, SYSTEM, TERMINAL, TOOL, TURN, VENV,
                    LayerStack, asset_lines, bare_prompt, beside, builder_box, cached_stamp, capture,
                    caption_extra, extra_tag, file_panel, history_row, illustration_tag, key_glyph,
                    log_panel, parcel_glyph, pin, readme_chip, resize, sans, source_text, term, tracker,
                    type_cmd, your_turn)

SAY = NARRATION["S06"]

# ------------------------------------------------------------------ commands and real outputs
LS = capture("11-ls-before-build")
assert LS.cmd == "ls -a; git status", LS.cmd
LS_CMD = "ls -a"                      # the `;`-joined capture: only `ls -a` is typed (script.md)
LS_OUT = LS.at((2, 9))
assert LS_OUT == [".", "..", ".gitignore", "Dockerfile", "README.md", "cli.py", "pyproject.toml",
                  "secrets"], LS_OUT
assert LS.line(10).startswith("On branch")

BUILD = "docker build -t transcribe_audio ."           # README :95 names the image, no command
_B = capture("12-build")
assert _B.cmd == "docker build --network host -t transcribe_audio .", _B.cmd   # never typed
# The script's line numbers are the file's (sed) lines. capture() reads with universal newlines,
# so apt's 21 lone '\r' progress rows shift its numbering after line ~390: read the file's own
# lines here, and check every one against capture() (the same text, from the same capture).
with open(TERMINAL / "laptop" / "12-build.txt", encoding="utf-8", newline="") as _f:
    _RAW = [s.rstrip("\r") for s in _f.read().split("\n")]


def bl(*spec) -> list[str]:
    """Build-log lines by file line number (ints, (a, b) ranges, "…")."""
    out = []
    for s in spec:
        if isinstance(s, str):
            out.append(s)
            continue
        a, b = (s, s) if isinstance(s, int) else s
        for n in range(a, b + 1):
            line = _RAW[n - 1]
            assert line in _B.lines, (n, line)
            out.append(line)
    return out


LOG_A = bl(9, 23, "…", (148, 149), "…", 1368, 1375, 1377)
assert LOG_A[1].startswith("#5 [2/5] RUN apt-get update")
assert "237 newly installed" in LOG_A[3] and "205 MB" in LOG_A[4]
assert LOG_A[7].endswith("Successfully installed uv-0.13.0") and LOG_A[8] == "#5 DONE 46.9s"
LOG_B1 = bl(1379, 1382)
assert LOG_B1 == ["#7 [3/5] WORKDIR /app", "#8 [4/5] COPY --chown=app:app . ./"]
LOG_B2 = bl((1385, 1388))
assert LOG_B2[0] == "#9 [5/5] RUN uv sync"
assert LOG_B2[1].endswith("Using CPython 3.12.15 interpreter at: /usr/local/bin/python3")
assert LOG_B2[2].endswith("/home/app/.venv") and "Resolved 1 package" in LOG_B2[3]
LOG_C = bl("…", 1399, "…", (1404, 1405))
assert LOG_C[1] == "#10 naming to docker.io/library/transcribe_audio:latest done"
assert LOG_C[3].strip().startswith("1 warning found") and LOG_C[4].endswith("(line 10)")

IMG = capture("13-images")
assert IMG.cmd == "docker images transcribe_audio"
IMG_OUT = IMG.at((2, 3))
assert "1.35GB" in IMG_OUT[1] and "357MB" in IMG_OUT[1]
_hist = capture("17-history")
assert history_row(_hist.line(9)).startswith("RUN |1 DEBIAN_PACKAGES") and \
    history_row(_hist.line(9)).endswith("842MB")
APT_SIZE = "842MB"                     # 17-history.txt line 9: the same cached apt layer

NOPY = capture("26-g21-no-pyproject")
NOPY_OUT = NOPY.at(34, 51)
assert "No `pyproject.toml` found" in NOPY_OUT[0] and NOPY_OUT[1].startswith("ERROR: failed to build")

DF = "files/transcribe_audio.Dockerfile"
assert asset_lines(DF, 10, 10) == "ENV GOOGLE_APPLICATION_CREDENTIALS=secrets/mega-pipeline.json"
_ra = source_text("transcribe_audio/README.md").split("\n")
assert "give your image the name `transcribe_audio`" in _ra[94], _ra[94]     # line 95
assert _ra[93].startswith("## Docker Build")

PONDER_Q = ("You change only group_name in cli.py\nand build again.\n"
            "Which of the five build steps run again?")

# ------------------------------------------------------------------ layout
BIG = 13                          # the terminal's rows while the log is up (top at y 2.59)
TRACK_BOTTOM = 2.916
SLAB_W = 5.2
SX, FLOOR_Y = -1.6, -0.85         # V2 above the 4-row strip (strip top -1.04)
APT_H, THIN = 1.9, 0.08           # the apt slab after it swells; the WORKDIR / uv sync hairlines
H0 = {"base": 0.5, "apt": 0.7, "workdir": THIN, "copy": 0.36, "sync": 0.42}   # as S05 left it
DROP = np.array([1.0, -0.8, 0])   # beat 8: V2 settles nearer the centre once the bottom is free


# ------------------------------------------------------------------ small helpers
def uline(line, sub, color, stroke=3.5, occ=0, pad=0.02) -> Line:
    """A Line under substring `sub` of terminal row `line`, in the gap under the row."""
    g = substring(line, sub, occ)
    y = line.strut.get_bottom()[1] + 0.01
    return Line([g.get_left()[0] - pad, y, 0], [g.get_right()[0] + pad, y, 0], color=color,
                stroke_width=stroke)


def rbar(lines, color, opacity=0.2, pad=0.08, right=None) -> Rectangle:
    """A translucent bar behind whole terminal rows (from the first glyph to the last, or to x=right)."""
    lines = lines if isinstance(lines, (list, tuple)) else [lines]
    left = min(ln.glyphs.get_left()[0] for ln in lines) - pad
    rx = right if right is not None else max(ln.glyphs.get_right()[0] for ln in lines) + pad
    top = lines[0].strut.get_top()[1] + 0.03
    bot = lines[-1].strut.get_bottom()[1] - 0.03
    return Rectangle(width=rx - left, height=top - bot, stroke_width=0).set_fill(color, opacity) \
        .move_to([(left + rx) / 2, (top + bot) / 2, 0])


def sbar(line, sub, color, opacity=0.28) -> Rectangle:
    """A translucent bar over substring `sub` of a terminal row."""
    g = substring(line, sub)
    return Rectangle(width=g.width + 0.14, height=line.strut.height * 0.95, stroke_width=0) \
        .set_fill(color, opacity).move_to([g.get_center()[0], line.strut.get_center()[1], 0])


def row_badge(k: int) -> VGroup:
    """TEAL 'build step k' badge that fits inside one terminal row (0.34 tall)."""
    b = step_badge(k, CTR, size=20, radius=0.17)
    return VGroup(b, sans(f"build step {k}", 20, CTR)).arrange(RIGHT, buff=0.1)


def scroll(scene, t, lines, wrap: bool = False):
    """Make room for `lines` before t.print: the oldest rows fade where they are, then the rest
    move up (Terminal's own scroll slides the old rows up over the title bar and the tracker)."""
    n = sum(max(1, -(-len(s) // t.max_chars)) if wrap else 1 for s in lines)
    over = len(t.lines) + n - t.rows
    if over <= 0:
        return
    gone = t.lines.submobjects[:over]
    stay = VGroup(*t.lines.submobjects[over:])
    scene.play(FadeOut(VGroup(*gone)), run_time=0.25)
    for m in gone:
        t.lines.remove(m)
        scene.remove(m)
    scene.play(stay.animate.shift(UP * t.pitch * over), run_time=0.35)


def stick(scene, line, *mobs):
    """Make mobs (already on screen) part of terminal row `line` (its last row when folded), so
    they scroll, shrink and clear with it."""
    row = line.rows[-1] if hasattr(line, "rows") else line
    for m in mobs:
        scene.remove(m)
        row.add(m)
    scene.add(row)


def pulse(b, color, k: float = 1.25):
    """A badge (circle, number) grows and takes `color`, then returns (no fill flash)."""
    tgt = b.copy().scale(k)
    tgt[0].set_stroke(color)
    tgt[1].set_color(color)
    return Transform(b, tgt, rate_func=there_and_back)


def recolor(b, color):
    """A badge's ring and number take `color` (and keep it)."""
    tgt = b.copy()
    tgt[0].set_stroke(color)
    tgt[1].set_color(color)
    return Transform(b, tgt)


def row_tag(s: str, color=S.GREY) -> VGroup:
    return tag(s, color, size=20)


def row_y(t, i: int) -> float:
    """Centre height of text row i of terminal t."""
    return t._slot(i)[1] - line_pitch(t.size) / 1.32 / 2


def place(m, left=None, right=None, top=None, bottom=None, cx=None, cy=None):
    if left is not None:
        m.shift(RIGHT * (left - m.get_left()[0]))
    if right is not None:
        m.shift(RIGHT * (right - m.get_right()[0]))
    if top is not None:
        m.shift(UP * (top - m.get_top()[1]))
    if bottom is not None:
        m.shift(UP * (bottom - m.get_bottom()[1]))
    if cx is not None:
        m.set_x(cx)
    if cy is not None:
        m.set_y(cy)
    return m


def fold_words(s: str, n: int) -> list[str]:
    """Fold a log line at spaces into rows of at most n characters (the text itself unchanged)."""
    rows = []
    while len(s) > n:
        i = s.rfind(" ", 0, n + 1)
        i = n if i <= 0 else i
        rows.append(s[:i])
        s = s[i:].lstrip(" ")
    return rows + [s]


def fan(ys, gap=0.5) -> list[float]:
    """Spread sorted badge heights apart to at least `gap` (pairs pushed symmetrically)."""
    ys = list(ys)
    for _ in range(400):
        moved = False
        for i in range(len(ys) - 1):
            d = ys[i + 1] - ys[i]
            if d < gap - 1e-4:
                m = (gap - d) / 2
                ys[i] -= m
                ys[i + 1] += m
                moved = True
        if not moved:
            break
    return ys


def compact_ponder(question: str, width: float = 9.5, size: float = 24) -> VGroup:
    """pause_and_ponder's card (frame, header, question, timer bar) with less padding, so it fits
    under the stack. Returns VGroup(frame, header, question, bar)."""
    card = ponder_card(question, width=width, size=size)
    fr, head, q, bar = card
    body = VGroup(head, q).arrange(DOWN, buff=0.16)
    fr.become(RoundedRectangle(width=width, height=body.height + 0.6, corner_radius=0.2,
                               stroke_color=TURN, stroke_width=3).set_fill(S.BG, 0.96))
    body.move_to(fr).shift(UP * 0.1)
    bar.become(Line(fr.get_corner(DL) + RIGHT * 0.3 + UP * 0.2, fr.get_corner(DR) + LEFT * 0.3 + UP * 0.2,
                    color=TURN, stroke_width=4))
    return card


# ------------------------------------------------------------------ the pictures
def context_folder() -> VGroup:
    """The transcribe_audio/ folder on the laptop: a GREY frame, its name, five files and the
    secrets/ folder with a tiny GOLD key. .frame .files (the six glyphs) .key"""
    fr = box_frame(4.5, 2.1)
    head = VGroup(folder_glyph(0.3, LAPTOP), mono("transcribe_audio/", 22, INK)).arrange(RIGHT, buff=0.14)
    head.move_to(fr.get_corner(UL) + np.array([0.25, -0.36, 0]), aligned_edge=LEFT)
    files = VGroup(*[file_glyph(0.6, LAPTOP) for _ in range(5)], folder_glyph(0.48, LAPTOP))
    files.arrange(RIGHT, buff=0.24).move_to(fr.get_center() + DOWN * 0.28)
    k = key_glyph(0.22).move_to(files[5].get_center() + np.array([0.06, -0.05, 0]))
    g = VGroup(fr, head, files, k)
    g.frame, g.files, g.key = fr, files, k
    return g


def box_frame(w, h, color=LAPTOP):
    return RoundedRectangle(width=w, height=h, corner_radius=0.14, stroke_color=color,
                            stroke_width=2.5).set_fill(color, 0.06)


def make_stack() -> LayerStack:
    """V2 as S05 left it: five slabs (base, apt, WORKDIR hairline, COPY with its files and a tiny
    GOLD key, the empty GREEN uv sync slab), floor at (SX, FLOOR_Y)."""
    st = LayerStack(slab_w=SLAB_W)
    for name in ("base", "apt", "workdir", "copy", "sync"):
        s = st.make(name, h=H0[name])
        st.slabs[name] = s
        st.order.append(name)
        st.add(s)
    st.copy_files = st.files("copy", key=True)
    st.add(st.copy_files)
    st.move_to([SX, FLOOR_Y, 0], aligned_edge=DOWN)
    return st


def restack(st: LayerStack, heights: dict, label_top=("apt",), hide_labels=("sync",)):
    """Animations that give the slabs new heights (bottom-up, the floor fixed), and the target
    boxes. Labels move with their slab (to its top for `label_top`; faded for `hide_labels`);
    the COPY slab's files ride along."""
    from explainer.devops import box
    anims, targets = [], {}
    y = st.floor.get_center()[1]
    x = st.floor.get_center()[0]
    for name in st.order:
        s = st.slabs[name]
        h = heights.get(name, s.h)
        nb = box(st.slab_w, h, s.hue, fill_opacity=0.25, radius=min(0.06, h / 2),
                 stroke=2.5 if h > 0.12 else 2)
        nb.move_to([x, y + st.gap + h / 2, 0])
        dy = nb.get_center()[1] - s.box.get_center()[1]
        anims.append(Transform(s.box, nb))
        if len(s.label):
            if name in hide_labels:
                anims.append(s.label.animate.move_to(nb).set_opacity(0))
            elif name in label_top:
                anims.append(s.label.animate.move_to([x, nb.get_top()[1] - 0.1 - s.label.height / 2, 0]))
            else:
                anims.append(s.label.animate.move_to(nb))
        if name == "copy" and abs(dy) > 1e-4:
            anims.append(st.copy_files.animate.shift(UP * dy))
        s.h = h
        targets[name] = nb
        y += st.gap + h
    return anims, targets


def brace_group(boxes) -> VGroup:
    """GREY brace along the slabs with "≈ 1 GB of layers" and the disk-usage note."""
    br = Brace(VGroup(*boxes), RIGHT, color=S.GREY, buff=0.12)
    txt = VGroup(sans("≈ 1 GB of layers", 20, INK),
                 label("+ 357 MB compressed copy", 20, S.GREY),
                 label("= 1.35 GB disk usage · this machine", 20, S.GREY))
    txt.arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(br, RIGHT, buff=0.15)
    g = VGroup(br, txt)
    g.brace, g.text = br, txt
    return g


def stack_badges(st: LayerStack) -> tuple[VGroup, VGroup]:
    """TEAL circled 1-5 left of the slabs, fanned so they don't touch, with leader lines."""
    names = st.order
    ys = fan([st.slabs[n].box.get_center()[1] for n in names], gap=0.52)
    x_edge = st.slabs[names[0]].box.get_left()[0]
    badges, leaders = VGroup(), VGroup()
    for k, (n, y) in enumerate(zip(names, ys), start=1):
        b = step_badge(k, CTR).move_to([x_edge - 0.62, y, 0])
        sy = st.slabs[n].box.get_center()[1]
        leaders.add(Line(b.get_right() + RIGHT * 0.02, [x_edge - 0.02, sy, 0], color=CTR, stroke_width=2))
        badges.add(b)
    return badges, leaders


def what_if_panel() -> VGroup:
    """RED-bordered panel: the G21 build's error lines, folded at spaces. .frame .rows .header"""
    width = 11.6
    n = int((width - 0.5) / cell_width(20))
    rows = [r for s in NOPY_OUT for r in fold_words(s, n)]
    p = log_panel(rows, "x", width=width, size=20, color=ERR)
    p.frame.set_stroke(ERR, 2.5)
    head = label("if you skipped uv init", 20, S.GREY)
    head.next_to(p.frame, UP, buff=0.14).align_to(p.frame, LEFT).shift(RIGHT * 0.12)
    p.remove(p.header)
    p.header = head
    p.add(head)
    return p


def edit_chip() -> VGroup:
    """GREY chip "edit: group_name in cli.py" (mono: the names are code). .frame .text"""
    t = mono("edit: group_name in cli.py", 20, INK)
    fr = RoundedRectangle(width=t.width + 0.44, height=0.52, corner_radius=0.18, stroke_color=S.GREY,
                          stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
    t.move_to(fr)
    g = VGroup(fr, t)
    g.frame, g.text = fr, t
    return g


# ------------------------------------------------------------------ the scene
class BuildImage(VoiceScene):
    def construct(self):
        assert len(SAY) == 9, f"S06 has {len(SAY)} SAY lines; this scene times 9"

        tr = tracker("A", 4)
        t = term(P_A, BIG)

        # ========================================================== 0 · ls -a (extra)
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.1), FadeIn(t), run_time=0.6)
            self.play(tr.goto(5), run_time=0.5)
            self.play(caption_extra(tr), run_time=0.3)
            c0 = type_cmd(self, t, LS_CMD, 0.4)
            pin(self, c0, beside(extra_tag(), t, c0), run_time=0.3)
            out0 = t.print(self, LS_OUT, run_time=0.7)
            dock, pyp = out0[3], out0[6]
            vo.wait_until("your Dockerfile")
            b0 = rbar(dock, VENV, 0.22, right=dock.glyphs.get_right()[0] + 0.1)
            self.play(FadeIn(b0), dock.glyphs.animate.set_color(VENV), run_time=0.5)
            stick(self, dock, b0)
            vo.wait_until("named exactly that")
            self.play(Indicate(dock.glyphs, color=VENV, scale_factor=1.25), run_time=0.8)
            vo.wait_until("sits next to")
            b1 = rbar(pyp, VENV, 0.22)
            self.play(FadeIn(b1), pyp.glyphs.animate.set_color(VENV), run_time=0.5)
            stick(self, pyp, b1)
            self.play(Indicate(pyp.glyphs, color=VENV, scale_factor=1.15), run_time=0.7)

        # ========================================================== 1 · the command (no Enter yet)
        chip_r = readme_chip("transcribe_audio/README.md · line 95",
                             "give your image the name transcribe_audio", max_w=11.6)
        place(chip_r, right=6.45, top=TRACK_BOTTOM - 0.12)
        err = row_tag("erratum · no command given")
        err.scale(22 / 20)                     # the house tag size (22 pt): text >= 20 pt
        place(err, right=6.45, bottom=chip_r.get_top()[1] + 0.1)
        if err.get_top()[1] > 3.55:
            err.shift(DOWN * (err.get_top()[1] - 3.55))
        folder = context_folder()
        folder.move_to([-3.75, 0.4, 0])
        parcel = parcel_glyph(1.1, "build context")
        parcel.move_to([-0.3, 0, 0])
        parcel.shift(UP * (folder.files.get_center()[1] - parcel.frame.get_center()[1]))
        builder = builder_box("builder").scale(1.5)
        builder.move_to([4.6, parcel.frame.get_center()[1], 0])
        parcel_end = parcel.copy().shift(RIGHT * (builder.get_left()[0] - 0.25 - parcel.frame.get_right()[0]))

        with self.voiceover(SAY[1]) as vo:
            self.play(caption_extra(tr, False), run_time=0.3)
            t.clear(self, run_time=0.3)
            resize(self, t, 3, run_time=0.7)
            bare_prompt(self, t)
            self.play(Indicate(tr.caption, color=TURN, scale_factor=1.12), run_time=0.7)
            vo.wait_until("A small gap")
            self.play(FadeIn(chip_r, shift=DOWN * 0.1), run_time=0.5)
            self.play(Indicate(chip_r.phrase, color=INK, scale_factor=1.05), run_time=0.7)
            vo.wait_until("but gives no command")
            self.play(FadeIn(err, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("Here it is")
            c1 = type_cmd(self, t, BUILD, 1.3)
            rb = c1.rows[1]
            assert rb.text == "    -t transcribe_audio .", rb.text
            vo.wait_until("dash t and the name")
            u_name = uline(rb, "-t transcribe_audio", S.GREY)
            l_name = label("the image's name", 20, S.GREY)
            l_name.move_to([u_name.get_center()[0], row_y(t, 2), 0])
            self.play(Create(u_name), run_time=0.4)
            self.play(FadeIn(l_name, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("then a dot")
            dot = substring(rb, ".")
            u_dot = Line([dot.get_left()[0] - 0.06, u_name.get_y(), 0],
                         [dot.get_right()[0] + 0.06, u_name.get_y(), 0], color=LOOKUP, stroke_width=4)
            l_dot = label("this folder = the build context", 20, LOOKUP)
            place(l_dot, left=dot.get_left()[0] - 0.08, cy=row_y(t, 2))
            self.play(dot.animate.set_color(LOOKUP), Create(u_dot), run_time=0.4)
            self.play(FadeIn(l_dot, shift=UP * 0.1), FadeIn(folder, shift=UP * 0.15), FadeIn(builder),
                      run_time=0.5)
            # as the PINK label lands, lecture 2's parcel (1.5 s): copies of the folder's files pack
            # into it and it slides to the builder
            flying = VGroup(*[m.copy() for m in folder.files], folder.key.copy())
            self.add(flying)
            self.play(FadeIn(parcel, scale=0.8),
                      *[m.animate.move_to(parcel.frame).scale(0.3).set_opacity(0) for m in flying],
                      run_time=0.7)
            self.remove(flying)
            self.play(Transform(parcel, parcel_end), run_time=0.8)
            vo.wait_until("the build context")
            self.play(Indicate(parcel[-1], color=INK, scale_factor=1.15),
                      Indicate(builder.frame, color=TOOL, scale_factor=1.06), run_time=0.8)

        # ========================================================== 2 · Enter: the full log, build step 2
        live = VGroup(label("your terminal shows a compact live view;", 20, S.GREY),
                      VGroup(label("this is the full log", 20, S.GREY),
                             mono("(--progress=plain)", 20, S.GREY)).arrange(RIGHT, buff=0.14))
        live.arrange(DOWN, aligned_edge=RIGHT, buff=0.1)
        place(live, right=6.45, top=3.47)

        with self.voiceover(SAY[2]) as vo:
            yt = beside(your_turn(), t, c1)
            self.play(FadeIn(yt, shift=LEFT * 0.1), FadeOut(VGroup(l_name, l_dot, u_name, u_dot)),
                      run_time=0.4)
            stick(self, c1, yt)
            self.play(Wiggle(yt, scale_value=1.15, rotation_angle=0.025 * TAU), run_time=0.7)
            self.play(FadeOut(VGroup(folder, parcel, builder, chip_r, err)), run_time=0.4)
            resize(self, t, BIG, run_time=0.8)
            new_title = mono("laptop · the same build, full log", 20, S.GREY).move_to(t.title)
            self.play(Transform(t.title, new_title), run_time=0.5)
            vo.wait_until("Your terminal shows")
            self.play(FadeIn(live, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("here are the full")
            outA = t.print(self, LOG_A, run_time=1.4, lag=0.12)
            r23, dots1, r148, r149, r1375, r1377 = outA[1], outA[2], outA[3], outA[4], outA[7], outA[8]

            vo.wait_until("Build step 2")
            k2 = substring(r23, "[2/5]")
            box2 = SurroundingRectangle(k2, color=CTR, buff=0.05, stroke_width=2.5, corner_radius=0.05)
            bd2 = row_badge(2)
            place(bd2, left=k2.get_left()[0] - 0.05, cy=dots1.strut.get_center()[1])
            self.play(Create(box2), k2.animate.set_color(CTR), run_time=0.4)
            stick(self, r23, box2)
            pin(self, dots1, bd2, run_time=0.4, anim=FadeIn(bd2, shift=UP * 0.1))
            vo.wait_until("apt installs")
            u148 = uline(r148, "237 newly installed", SYSTEM)
            pin(self, r148, u148, run_time=0.5, anim=Create(u148))
            vo.wait_until("a 205 megabyte")
            u149 = uline(r149, "205 MB", SYSTEM)
            pin(self, r149, u149, run_time=0.4, anim=Create(u149))
            vo.wait_until("then pip installs")
            uvg = substring(r1375, "uv-0.13.0")
            u1375 = uline(r1375, "uv-0.13.0", TOOL)
            self.play(uvg.animate.set_color(TOOL), Create(u1375), run_time=0.5)
            stick(self, r1375, u1375)
            vo.wait_until("all in 46.9")
            u1377 = uline(r1377, "DONE 46.9s", TURN)
            pin(self, r1377, u1377, run_time=0.5, anim=Create(u1377))
            note = VGroup(label("first build: Docker also pulls", 20, S.GREY),
                          mono("python:3.12-slim-bookworm", 20, S.GREY)).arrange(RIGHT, buff=0.14)
            note[1].align_to(note[0], DOWN)
            place(note, left=r1377.glyphs.get_right()[0] + 0.45, cy=r1377.strut.get_center()[1])
            pin(self, r1377, note, run_time=0.5)

        # ========================================================== 3 · build steps 3, 4, 5
        with self.voiceover(SAY[3]) as vo:
            outB1 = t.print(self, LOG_B1, run_time=0.5)
            for k, ln in zip((3, 4), outB1):
                g = substring(ln, f"[{k}/5]")
                bd = beside(row_badge(k), t, ln, buff=0.35)
                self.play(g.animate.set_color(CTR), run_time=0.25)
                pin(self, ln, bd, run_time=0.4)
            vo.wait_until("and copy our files")
            self.play(Indicate(substring(outB1[1], "COPY --chown=app:app . ./"), color=INK,
                               scale_factor=1.08), run_time=0.7)
            vo.wait_until("Build step 5")
            scroll(self, t, LOG_B2, wrap=True)
            outB2 = t.print(self, LOG_B2, run_time=0.8, wrap=True)
            r1385, r1386a, r1386b, r1387, r1388 = outB2
            assert r1386b.text == "hon3", r1386b.text
            self.play(substring(r1385, "[5/5]").animate.set_color(CTR), run_time=0.25)
            pin(self, r1385, beside(row_badge(5), t, r1385, buff=0.35), run_time=0.4)
            vo.wait_until("with the image's own")
            ua = uline(r1386a, "Using CPython 3.12.15 interpreter at: /usr/local/bin/pyt", SYSTEM)
            ub = uline(r1386b, "hon3", SYSTEM)
            self.play(Create(ua), run_time=0.6)
            self.play(Create(ub), run_time=0.2)
            stick(self, r1386a, ua)
            stick(self, r1386b, ub)
            self.play(Indicate(substring(r1386a, "3.12.15"), color=SYSTEM, scale_factor=1.2), run_time=0.7)
            vo.wait_until("creates the venv")
            vg = substring(r1387, "/home/app/.venv")
            u1387 = uline(r1387, "/home/app/.venv", VENV)
            self.play(vg.animate.set_color(VENV), Create(u1387), run_time=0.5)
            stick(self, r1387, u1387)
            vo.wait_until("and resolves 1 package")
            self.play(Indicate(substring(r1388, "Resolved 1 package"), color=INK, scale_factor=1.1),
                      run_time=0.7)
            vo.wait_until("the project itself")
            pin(self, r1388, beside(row_tag("only the project itself"), t, r1388, buff=0.35), run_time=0.5)

        # ========================================================== 4 · naming, and the warning
        inset = file_panel(DF, 10, 10, "transcribe_audio/Dockerfile", size=22)
        place(inset, cx=0, top=2.55)
        src_cap = VGroup(VGroup(label("from", 20, S.GREY), mono("transcribe_audio/README.md", 20, S.GREY))
                         .arrange(RIGHT, buff=0.12), label("lines 41–90", 20, S.GREY))
        src_cap.arrange(DOWN, aligned_edge=RIGHT, buff=0.08)
        place(src_cap, right=6.45, top=3.47)
        cred = code_span(inset.code, 0, "CREDENTIALS")
        val = code_span(inset.code, 0, "secrets/mega-pipeline.json")
        harmless = tag("a name check · harmless here", S.GREY)
        place(harmless, left=inset.code.get_left()[0] + 0.1, top=inset.code.get_bottom()[1] - 0.18)

        with self.voiceover(SAY[4]) as vo:
            scroll(self, t, LOG_C, wrap=True)
            outC = t.print(self, LOG_C, run_time=0.8, wrap=True)
            r1399, r1404, r1405a, r1405b = outC[1], outC[3], outC[4], outC[5]
            assert r1405b.text.endswith("(line 10)"), r1405b.text
            g1399 = rbar(r1399, VENV, 0.24)
            self.play(FadeIn(g1399), run_time=0.4)
            stick(self, r1399, g1399)
            self.play(Indicate(substring(r1399, "transcribe_audio:latest"), color=VENV, scale_factor=1.1),
                      run_time=0.6)
            vo.wait_until("with a warning")
            gw = rbar([r1404, r1405a, r1405b], S.GREY, 0.22, right=t.box.get_right()[0] - 0.12)
            l10 = substring(r1405b, "(line 10)")
            box10 = SurroundingRectangle(l10, color=S.GREY, buff=0.04, stroke_width=2.5, corner_radius=0.05)
            self.play(FadeIn(gw), Create(box10), run_time=0.5)
            stick(self, r1404, gw)
            stick(self, r1405b, box10)
            resize(self, t, 6, run_time=0.7, extra=[FadeOut(live)])
            self.play(FadeIn(inset.code), FadeIn(inset.header[0]), FadeIn(src_cap),
                      TransformFromCopy(l10, inset.header[1]), run_time=0.8)
            vo.wait_until("Docker flags")
            u_cred = Line(cred.get_corner(DL) + DOWN * 0.07, cred.get_corner(DR) + DOWN * 0.07,
                          color=TURN, stroke_width=4)
            self.play(Create(u_cred), run_time=0.5)
            vo.wait_until("whose name sounds secret")
            self.play(Indicate(cred, color=TURN, scale_factor=1.15), run_time=0.8)
            vo.wait_until("The value is just a path")
            u_val = Line(val.get_corner(DL) + DOWN * 0.07, val.get_corner(DR) + DOWN * 0.07,
                         color=LOOKUP, stroke_width=4)
            self.play(Create(u_val), run_time=0.5)
            vo.wait_until("so it's harmless")
            self.play(FadeIn(harmless, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("and you'll see it")
            self.play(Indicate(VGroup(r1404.glyphs, r1405a.glyphs, r1405b.glyphs), color=INK,
                               scale_factor=1.03), run_time=0.9)

        # ========================================================== 5 · docker images (extra), V2 sizes
        st = make_stack()
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(inset, src_cap, harmless, u_cred, u_val)), caption_extra(tr),
                      Transform(t.title, mono("laptop", 20, S.GREY).move_to(t.title)), run_time=0.4)
            t.clear(self, run_time=0.3)
            resize(self, t, 4, run_time=0.7, extra=[FadeIn(st, shift=UP * 0.2)])
            c5 = type_cmd(self, t, IMG.cmd, 0.9)
            pin(self, c5, beside(extra_tag(), t, c5), run_time=0.3)
            out5 = t.print(self, IMG_OUT, run_time=0.5)
            assert out5[1].text.endswith("357…"), out5[1].text
            vo.wait_until("says 1.35")
            b135 = sbar(out5[1], "1.35GB", TURN, 0.3)
            pin(self, out5[1], b135, run_time=0.4)
            self.play(Indicate(substring(out5[1], "1.35GB"), color=TURN, scale_factor=1.2), run_time=0.6)
            brace = brace_group([st.slabs[n].box for n in st.order])
            self.play(GrowFromCenter(brace.brace), FadeIn(brace.text, shift=LEFT * 0.1), run_time=0.7)

            vo.wait_until("By far the biggest")
            anims, targets = restack(st, {"apt": APT_H, "sync": THIN})
            brace2 = brace_group([targets[n] for n in st.order])
            self.play(*anims, Transform(brace, brace2), run_time=1.2)
            apt = st.slabs["apt"]
            size = mono(APT_SIZE, 22, SYSTEM).move_to(apt.box).shift(DOWN * 0.12)
            st.attach(self, size, anims=[FadeIn(size, scale=1.3)], run_time=0.5)
            vo.wait_until("842 megabytes")
            self.play(Indicate(size, color=SYSTEM, scale_factor=1.25), run_time=0.8)
            vo.wait_until("while the copied folder")
            cp = st.slabs["copy"]
            self.play(Indicate(VGroup(cp.box, st.copy_files), color=INK, scale_factor=1.12), run_time=0.8)
            badges, leaders = stack_badges(st)
            st.attach(self, *leaders, *badges,
                      anims=[LaggedStart(*[AnimationGroup(Create(ln), FadeIn(b, scale=1.2))
                                           for ln, b in zip(leaders, badges)], lag_ratio=0.25)],
                      run_time=1.2)

        # ========================================================== 6 · what if (no pyproject.toml)
        panel = what_if_panel()
        place(panel, cx=0, bottom=-3.5)
        ill = illustration_tag("what if")
        place(ill, right=panel.frame.get_right()[0], cy=panel.header.get_center()[1])
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(t), FadeOut(brace), caption_extra(tr, False), run_time=0.5)
            self.play(FadeIn(panel, shift=UP * 0.15), FadeIn(ill), run_time=0.6)
            vo.wait_until("build step 5 fails")
            sync = st.slabs["sync"]
            self.play(pulse(badges[4], ERR, 1.35), Indicate(sync.box, color=ERR, scale_factor=1.06),
                      Indicate(panel.rows[0], color=ERR, scale_factor=1.03), run_time=0.9)
            vo.wait_until("because there's no")
            self.play(Indicate(substring(panel.rows[0], "No `pyproject.toml` found"), color=INK,
                               scale_factor=1.12), run_time=0.8)

        # ========================================================== 7 · ponder
        chip = edit_chip()
        place(chip, left=st.slabs["copy"].box.get_right()[0] + 0.45, cy=st.slabs["copy"].box.get_center()[1])
        card = compact_ponder(PONDER_Q)
        place(card, cx=0, bottom=-3.55)
        assert card.get_top()[1] < st.floor.get_center()[1] - 0.12, card.get_top()[1]
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(panel), FadeOut(ill), run_time=0.5)
            vo.wait_until("You change only")
            self.play(FadeIn(chip, shift=LEFT * 0.2), run_time=0.6)
            self.play(chip.animate(rate_func=there_and_back).shift(UP * 0.1), run_time=1.2)
            vo.wait_until("which of the five")
            self.play(LaggedStart(*[pulse(b, TURN) for b in badges], lag_ratio=0.15), run_time=1.1)
            self.play(chip.animate(rate_func=there_and_back).shift(UP * 0.1), run_time=1.2)
        self.play(FadeIn(card, scale=0.95), run_time=0.6)
        bar = card[3]
        self.play(bar.animate(rate_func=linear).become(bar.copy().scale(0.001, about_point=bar.get_start())),
                  run_time=8)

        # ========================================================== 8 · the answer
        cp, sync = st.slabs["copy"], st.slabs["sync"]
        with self.voiceover(SAY[8]) as vo:
            saved_cp = VGroup(cp.box.copy(), st.copy_files.copy())
            saved_sync = sync.box.copy()
            self.play(FadeOut(card), run_time=0.3)
            self.play(chip.animate.move_to(cp.box).scale(0.5).set_opacity(0),
                      cp.box.animate.set_stroke(TURN, 3).set_fill(TURN, 0.35), run_time=0.7)
            self.remove(chip)
            # the bottom band is free: V2 settles nearer the centre (the saved looks ride along)
            saved_cp.shift(DROP)
            saved_sync.shift(DROP)
            self.play(st.animate.shift(DROP), run_time=0.6)
            self.play(recolor(badges[3], TURN), recolor(badges[4], TURN), run_time=0.4)
            vo.wait_until("The copied folder changed")
            self.play(cp.box.animate.set_opacity(0).scale(1.04), st.copy_files.animate.set_opacity(0),
                      run_time=0.6)
            self.play(Transform(cp.box, saved_cp[0]), Transform(st.copy_files, saved_cp[1]),
                      pulse(badges[3], TURN), run_time=0.8)
            vo.wait_until("and so does every step")
            self.play(sync.box.animate.set_opacity(0).scale(1.04), run_time=0.5)
            self.play(Transform(sync.box, saved_sync), pulse(badges[4], TURN), run_time=0.8)

            stamps, stamp_leads = VGroup(), VGroup()
            for n in ("apt", "workdir"):
                b = st.slabs[n].box
                s_ = cached_stamp()
                s_.move_to([b.get_right()[0] + 0.45 + s_.width / 2, b.get_center()[1], 0])
                stamp_leads.add(Line([b.get_right()[0] + 0.03, b.get_center()[1], 0], s_.get_left(),
                                     color=VENV, stroke_width=2.5))
                stamps.add(s_)
            part2 = label("part 2: for real", 22, S.GREY)
            place(part2, cx=st.floor.get_center()[0], top=st.floor.get_center()[1] - 0.4)

            vo.wait_until("build steps 1 to 3")
            self.play(*[recolor(b, VENV) for b in badges[:3]], run_time=0.6)
            self.play(LaggedStart(*[AnimationGroup(Create(ln), FadeIn(s_, scale=1.4))
                                    for ln, s_ in zip(stamp_leads, stamps)], lag_ratio=0.4), run_time=0.9)
            vo.wait_until("We'll see it")
            self.play(FadeIn(part2, shift=UP * 0.1), run_time=0.6)
        self.wait(0.6)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
