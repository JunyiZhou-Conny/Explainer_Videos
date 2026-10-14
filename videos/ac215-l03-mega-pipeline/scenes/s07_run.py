r"""S07 · Run: a window into your laptop (README › transcribe_audio step 6; V3; PONDER 3; end of part 1).

V3 (common.Window, 5 rows: the fifth holds beat 2's new page and, in the ponder, lecture 2's
/app/.venv) is drawn at full size; it can't shrink, and with the README chip in the top band a
10-row terminal leaves no room above it, so V3 leaves while the terminal is up (beats 5-10) and
returns above a 3-row strip in beat 11.

Beats (script.md "## S07", one voiceover block each):
 0  TRACKER A5 -> A6. No terminal. V3 builds with the image block centred (the laptop is still
    hidden): the TEAL image block (caption "image · transcribe_audio"), then the /app cavity and
    its copied files (cli.py, Dockerfile, pyproject.toml, secrets/), then the GREEN
    /home/app/.venv box outside the cavity. The dashed TEAL writable layer settles on top; GREY
    caption "container = image + a thin writable layer", then "thrown away on exit: --rm" while
    a ghost of the layer floats up and fades.
 1  V3 slides right and the laptop (GREY, transcribe_audio/) fades in at left. The PINK route
    draws with its label -v "$(pwd):/app"; the folder name pulses ("the current folder, pwd").
    A GREY sheet carrying the laptop's files appears on the laptop folder and slides along the
    route over the cavity; the copied files dim underneath. Caption "/app now is your folder".
 2  Caption "one folder, seen from two sides". A pencil edits cli.py in the laptop folder; at the
    same instant cli.py blinks on the sheet over the cavity and the route pulses (nothing
    travels). A page appears in the fifth row on both sides at the same instant, blinks on both
    (route pulse), and gets a GREEN check (it stays). A page lands on the dashed writable layer,
    with a GREY tag "/tmp · throwaway" above it.
 3  The beat-2 marks go. Tag "illustration · lecture 2's layout: .venv next to the code". The
    laptop sheet slides halfway back along the route (the copied files undim); the GREEN venv
    box slides into the cavity's fifth row as /app/.venv. PONDER (8 s, card under V3) while the
    sheet waits half open.
 4  The sheet slides back over the cavity and covers the .venv box completely (copied files dim
    again). A TEAL label "start: bash, venv on" above the layer sends an "activate" arrow down;
    it hits the sheet and turns RED with a cross and "no .venv on your laptop". The marks and
    the illustration tag go; the box slides back out to /home/app/.venv and CODE(Dockerfile: 9)
    appears under the image (GREY "from transcribe_audio/README.md · lines 41–90"), GREEN bar;
    UV_PROJECT_ENVIRONMENT pulses; /home/app/.venv underlines GREEN as the venv label pulses.
 5  TRACKER A6. V3 and the panel leave; the terminal (full width, 10 rows, laptop) rises; the
    README chip "transcribe_audio/README.md · line 99" in the top band. It types
    `docker run --rm -ti -v "$(pwd):/app" transcribe_audio` (folds after `run`). GREY labels
    under the parts, on the word: --rm "delete on exit", -ti "interactive terminal" (one row
    lower, with a tick), -v "$(pwd):/app" "the window" (PINK, as the route), the image name "the
    image". The chip pulses on "README"; the quotes turn YELLOW on "quotes included"; ▶ your turn.
 6  The labels go; the terminal shrinks to the 3-row strip (command still on it). Above, a GREY
    card "README.md · lines 227–235", "Notes for running on Windows": Git BASH, quote $(pwd), the
    TTY error -> winpty, written on the word; the command chip
    `winpty docker run --rm -ti -v "$(pwd)":/app generate_text` (shown, not typed) with
    "swap in your component's name"; `winpty` turns YELLOW.
 7  The card, the chip and ▶ go; the terminal grows back to 10 rows, title "container ·
    transcribe_audio", TEAL frame; the prompt app@5b4d4981ec25:/app$ (01-docker-run-tty.txt
    line 2). Underlines and tags on the word: app "user" (GREY), /app "the window" (PINK),
    5b4d4981ec25 "container id · yours differs" (GREY, one row lower with a tick).
 8  TRACKER A6 · extra. The tags go. Above the terminal a GREY note: "no (transcribe-audio) in
    the prompt" (the name struck through) · "the venv is active anyway". `which python` (extra)
    -> line 3, /home/app/.venv underlines GREEN; `python --version` (extra) -> line 5, 3.12.15
    underlines ORANGE (the image's Python).
 9  The note goes. `ls -a` (extra) -> line 7 (wrap); Dockerfile, pyproject.toml and secrets get
    GREY bars and a GREY tag "your laptop's files". `echo $GOOGLE_APPLICATION_CREDENTIALS`
    (extra) -> line 9; above the terminal CODE(Dockerfile: 10); the value underlines PINK in
    both places at once.
10  The inset goes. `python cli.py --help` (extra) -> lines 11-14, line 14 RED; "Module not
    found" underlines RED; line 13's `google` underlines on "no module named google".
11  TRACKER A6. The terminal shrinks to the strip (the import and the RED error stay); V3
    returns above it, mounted: the route pulses, the sheet over /app pulses; cli.py turns RED,
    a RED "?" hovers between it and a BLUE "google" chip above the empty venv box, which pulses.
    On "In part 2" the strip goes and the caption "Part 2: packages, and why they vanish"
    appears. Fade out: empty frame (end of part 1).
"""

import numpy as np
from manim import *

from explainer import style as S
from explainer.components import ponder_card
from explainer.devops import MONO, box, check_mark, chip, code_span, cross_mark, label, line_bar, mono, substring, tag
from explainer.scene import VoiceScene

from common import (CLOUD, CTR, ERR, INK, LAPTOP, LOOKUP, NARRATION, P_A, P_CTR, SYSTEM, TURN, VENV,
                    Window, _save_op, _set_op, asset_lines, bare_prompt, beside, capture, caption_extra,
                    cmd_chip, enter_container, extra_tag, file_panel, illustration_tag, page_token, pin,
                    readme_chip, resize, sans, source_text, term, tracker, type_cmd, unpin, your_turn)

SAY = NARRATION["S07"]

# ------------------------------------------------------------------ commands and real outputs
RUN = 'docker run --rm -ti -v "$(pwd):/app" transcribe_audio'          # transcribe_audio/README.md:99
_ra = source_text("transcribe_audio/README.md").split("\n")
assert _ra[98] == RUN, _ra[98]
_rm = source_text("README.md").split("\n")
assert _rm[226] == "### Notes for running on Windows", _rm[226]
assert _rm[229].startswith("* Run docker commands from **Git BASH**"), _rm[229]
assert _rm[230].startswith("* **Always quote `$(pwd)`**"), _rm[230]
assert "`the input device is not a TTY`" in _rm[231] and "`winpty`" in _rm[231], _rm[231]
WINPTY = _rm[234].strip()
assert WINPTY == 'winpty docker run --rm -ti -v "$(pwd)":/app generate_text', WINPTY

TTY = capture("01-docker-run-tty", "transcribe_audio")
assert TTY.cmd == RUN, TTY.cmd
assert TTY.line(2).startswith(P_CTR + " "), (TTY.line(2), P_CTR)
WHICH, VERSION, LS, ECHO, HELP = (TTY.typed(n) for n in (2, 4, 6, 8, 10))
assert (WHICH, VERSION, LS) == ("which python", "python --version", "ls -a")
assert ECHO == "echo $GOOGLE_APPLICATION_CREDENTIALS" and HELP == "python cli.py --help"
OUT_WHICH, OUT_VERSION, OUT_LS, OUT_ECHO = (TTY.line(n) for n in (3, 5, 7, 9))
assert OUT_WHICH == "/home/app/.venv/bin/python" and OUT_VERSION == "Python 3.12.15"
assert OUT_LS.split() == [".", "..", ".gitignore", "Dockerfile", "README.md", "cli.py", "pyproject.toml",
                          "secrets"], OUT_LS
assert OUT_ECHO == "secrets/mega-pipeline.json"
OUT_HELP = TTY.at((11, 14))
assert OUT_HELP[2].strip() == "from google.cloud import storage"
assert OUT_HELP[3] == "ModuleNotFoundError: No module named 'google'"

DF = "files/transcribe_audio.Dockerfile"
assert asset_lines(DF, 9, 9) == "ENV UV_PROJECT_ENVIRONMENT=/home/app/.venv"
assert asset_lines(DF, 10, 10) == "ENV GOOGLE_APPLICATION_CREDENTIALS=secrets/mega-pipeline.json"

PONDER_Q = ("In lecture 2 the venv sat right next to the code.\n"
            "If it sat next to the code here, at /app/.venv,\n"
            "what would the container find there with this mount?")

# ------------------------------------------------------------------ layout
Y0 = 0.35                     # V3's centre in beats 0-2 (no terminal: the frame's middle)
Y_WIN = 0.75                  # from beat 3: room for the ponder card under it; above a 3-row strip
X_SOLO = -3.125               # beat 0: the image block alone, centred (the laptop still hidden)
CAP_Y = Y0 - 2.47             # captions under V3 (beats 0-2)
TRACK_BOTTOM = 2.917
BIG = 10                      # the terminal's rows (top at y 1.38)
SZ = 20


# ------------------------------------------------------------------ small helpers
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


def hide_part(piece, name: str, mob):
    """Register an existing member of a set piece as a hidden part (opacity 0, still a member),
    so piece.reveal(scene, name) brings it in."""
    _save_op(mob)
    _set_op(mob, 0)
    mob.hidden = True
    piece.parts[name] = mob


def unhide(piece, *names):
    """Restore the saved opacities of hidden parts without playing anything (the caller animates
    them in). Returns the parts."""
    out = []
    for n in names:
        m = piece.parts[n]
        if getattr(m, "hidden", False):
            _set_op(m)
        piece._flag(m, False)
        out.append(m)
    return out


def op_target(m, k: float):
    """A copy of m whose members have k times the opacities saved under '_orig'."""
    c = m.copy()
    _set_op(c, k, "_orig")
    return c


def row_y(t, i: int) -> float:
    """Centre height of text row i of terminal t."""
    return t._slot(i)[1] - t.pitch / 1.32 / 2


def uline(line, sub, color, stroke=3.5, occ=0, pad=0.02) -> Line:
    """A Line under substring `sub` of terminal row `line`, in the gap under the row."""
    g = substring(line, sub, occ)
    y = line.strut.get_bottom()[1] + 0.01
    return Line([g.get_left()[0] - pad, y, 0], [g.get_right()[0] + pad, y, 0], color=color,
                stroke_width=stroke)


def sbar(line, sub, color, opacity=0.28, occ=0) -> Rectangle:
    """A translucent bar over substring `sub` of a terminal row."""
    g = substring(line, sub, occ)
    return Rectangle(width=g.width + 0.14, height=line.strut.height * 0.95, stroke_width=0) \
        .set_fill(color, opacity).move_to([g.get_center()[0], line.strut.get_center()[1], 0])


def stick(scene, line, *mobs):
    """Make mobs (already on screen) part of terminal row `line` (its last row when folded), so
    they scroll, shrink and clear with it."""
    row = line.rows[-1] if hasattr(line, "rows") else line
    for m in mobs:
        scene.remove(m)
        row.add(m)
    scene.add(row)


def row_tag(s: str, color=S.GREY) -> VGroup:
    return tag(s, color, size=SZ)


def caption(*parts, color=S.GREY) -> VGroup:
    """A GREY caption: plain strings in serif, strings wrapped in backticks in mono."""
    ms = []
    for p in parts:
        if p.startswith("`") and p.endswith("`"):
            ms.append(mono(p[1:-1], SZ, color))
        else:
            ms.append(label(p, SZ, color))
    g = VGroup(*ms).arrange(RIGHT, buff=0.12)
    for m in ms[1:]:
        m.align_to(ms[0], DOWN)
    return g


def pencil(h: float = 0.62) -> VGroup:
    """A small pencil (an edit in VS Code on the laptop), tip pointing down-left. .tip"""
    w = 0.14
    body = Rectangle(width=w, height=h, stroke_color=S.GREY, stroke_width=2).set_fill(S.GREY_DARK, 1)
    band = Rectangle(width=w, height=0.1, stroke_color=S.GREY, stroke_width=2).set_fill(S.GREY, 1)
    band.next_to(body, UP, buff=0)
    tip = Polygon(body.get_corner(DL), body.get_corner(DR), body.get_bottom() + DOWN * 0.18,
                  stroke_color=S.GREY, stroke_width=2).set_fill(INK, 1)
    g = VGroup(body, band, tip).rotate(-1.3)
    g.tip = tip
    return g


def page_glyph(h: float = 0.32) -> VGroup:
    """A small page of text (bars, no words)."""
    return page_token().scale_to_fit_height(h)


def compact_ponder(question: str, width: float = 10.4, size: float = 24) -> VGroup:
    """pause_and_ponder's card (frame, header, question, timer bar) with less padding, so it fits
    under V3. Returns VGroup(frame, header, question, bar)."""
    card = ponder_card(question, width=width, size=size)
    fr, head, q, bar = card
    body = VGroup(head, q).arrange(DOWN, buff=0.14)
    fr.become(RoundedRectangle(width=width, height=body.height + 0.55, corner_radius=0.2,
                               stroke_color=TURN, stroke_width=3).set_fill(S.BG, 0.96))
    body.move_to(fr).shift(UP * 0.09)
    bar.become(Line(fr.get_corner(DL) + RIGHT * 0.3 + UP * 0.17, fr.get_corner(DR) + LEFT * 0.3 + UP * 0.17,
                    color=TURN, stroke_width=4))
    return card


def frame_pulse(m, color, width: float = 5):
    """A frame's stroke brightens and thickens, then returns (its fill is left alone)."""
    return m.animate(rate_func=there_and_back).set_stroke(color=color, width=width)


def route_pulse(win, width: float = 12):
    """The PINK route thickens and returns (nothing travels along it)."""
    return win.route.animate(rate_func=there_and_back).set_stroke(width=width)


def windows_card() -> VGroup:
    """The README's Windows notes: its heading (README.md line 227) and bullets (230–235), one row
    per bullet, and the command chip with its caption. .frame .header .title .rows .chip .note
    .winpty"""
    r1 = caption("Run docker commands from", color=INK)
    r1.add(label("Git BASH", SZ, INK, weight="BOLD").next_to(r1, RIGHT, buff=0.12).align_to(r1, DOWN))
    r2 = caption("Always quote", "`$(pwd)`", color=INK)
    r3 = caption("If you see", "`the input device is not a TTY`", ", prefix with", "`winpty`", color=INK)
    r3[2].next_to(r3[1], RIGHT, buff=0.04)
    r3[3].next_to(r3[2], RIGHT, buff=0.12)
    for m in r3[2:]:
        m.align_to(r3[0], DOWN)
    title = label("Notes for running on Windows", SZ, INK, weight="BOLD")
    rows = VGroup(r1, r2, r3).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    c = cmd_chip(WINPTY, "swap in your component's name")
    body = VGroup(title, rows, c).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
    fr = box(body.width + 0.6, body.height + 0.5, S.GREY, fill=S.BG, fill_opacity=0.92, radius=0.12)
    body.move_to(fr)
    head = VGroup(mono("README.md", SZ, S.GREY), label("· lines 227–235", SZ, S.GREY)).arrange(RIGHT, buff=0.12)
    head.next_to(fr, UP, buff=0.08).align_to(fr, LEFT).shift(RIGHT * 0.1)
    g = VGroup(fr, head, title, rows, c)
    g.frame, g.header, g.title, g.rows, g.chip, g.note = fr, head, title, rows, c.chip, c.note
    g.winpty = VGroup(*c.chip.text[:6])
    return g


# ------------------------------------------------------------------ the scene
class RunContainer(VoiceScene):
    def construct(self):
        assert len(SAY) == 12, f"S07 has {len(SAY)} SAY lines; this scene times 12"

        tr = tracker("A", 5)

        # V3, every member hidden until its beat
        win = Window(rows=5, sheet=False)
        win.shift(UP * Y0 + RIGHT * X_SOLO)
        _save_op(win.copied, "_orig")
        hide_part(win, "laptop", win.laptop)
        hide_part(win, "img", win.image.frame)
        hide_part(win, "img_cap", win.image.caption)
        hide_part(win, "cavity", VGroup(win.image.cavity, win.image.app))
        hide_part(win, "copied", win.copied)
        hide_part(win, "venv", win.venv)
        self.add(win)

        # ========================================================== 0 · the image, the venv, the layer
        cap0a = caption("container = image + a thin writable layer")
        cap0b = caption("thrown away on exit:", "`--rm`")
        VGroup(cap0a, cap0b).arrange(DOWN, buff=0.14).move_to([0, CAP_Y - 0.12, 0])
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.1), run_time=0.5)
            self.play(tr.goto(6), run_time=0.5)
            vo.wait_until("so first, a picture")
            unhide(win, "img", "img_cap")
            self.play(Create(win.image.frame), FadeIn(win.image.caption, shift=UP * 0.1), run_time=0.9)
            vo.wait_until("The copied files")
            unhide(win, "cavity")
            self.play(FadeIn(win.image.cavity), FadeIn(win.image.app, shift=RIGHT * 0.1), run_time=0.5)
            unhide(win, "copied")
            self.play(LaggedStart(*[FadeIn(r, shift=DOWN * 0.15) for r in win.copied], lag_ratio=0.2),
                      run_time=0.9)
            self.play(Indicate(win.image.app, color=INK, scale_factor=1.25), run_time=0.6)
            vo.wait_until("the venv sits outside")
            unhide(win, "venv")
            self.play(FadeIn(win.venv, shift=LEFT * 0.2), run_time=0.6)
            self.play(Indicate(win.venv.label, color=VENV, scale_factor=1.12), run_time=0.7)
            vo.wait_until("As in lecture 2")
            win.reveal(self, "sheet", anim=lambda m: FadeIn(m, shift=DOWN * 0.4), run_time=0.9)
            self.play(FadeIn(cap0a, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(win.sheet.frame, color=CTR, scale_factor=1.03), run_time=0.7)
            vo.wait_until("thrown away on exit")
            ghost = win.sheet.copy()
            self.add(ghost)
            self.play(ghost.animate.shift(UP * 0.55).set_opacity(0), FadeIn(cap0b, shift=UP * 0.1),
                      run_time=1.0)
            self.remove(ghost)
            self.play(Indicate(cap0b[1], color=INK, scale_factor=1.2), run_time=0.6)

        # ========================================================== 1 · -v: the laptop sheet covers /app
        cap1 = caption("`/app`", "now is your folder").move_to([0, CAP_Y, 0])
        with self.voiceover(SAY[1]) as vo:
            self.play(win.animate.shift(LEFT * X_SOLO), FadeOut(VGroup(cap0a, cap0b)), run_time=0.7)
            win.reveal(self, "laptop", anim=lambda m: FadeIn(m, shift=RIGHT * 0.2), run_time=0.5)
            win.reveal(self, "route", anim=Create, run_time=0.5)
            win.reveal(self, "route_label", anim=lambda m: FadeIn(m, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("pwd")
            self.play(Indicate(win.laptop.folder, color=INK, scale_factor=1.12), run_time=0.6)
            vo.wait_until("it covers the copied files")
            win.reveal(self, "cover", run_time=0.3)
            self.play(win.cover_to(1.0), Transform(win.copied, op_target(win.copied, 0.3)), run_time=1.1)
            win.mounted = True
            vo.wait_until("so slash app is now")
            self.play(FadeIn(cap1, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(win.image.app, color=INK, scale_factor=1.3), frame_pulse(win.cover.frame, INK),
                      run_time=0.8)

        # ========================================================== 2 · one folder, two sides
        cap2 = caption("one folder, seen from two sides").move_to([0, CAP_Y, 0])
        pen = pencil()
        cli_l = win.row("cli.py", "laptop")
        pen.shift(cli_l.text.get_right() + RIGHT * 0.1 - pen.tip.get_bottom())
        pages = []
        for area in (win.laptop.area, win.cover.frame):
            pg = page_glyph()
            pg.move_to(win._row_pos(area, 4), aligned_edge=LEFT).shift(RIGHT * 0.02)
            pages.append(pg)
        pg_l, pg_c = pages
        chk = check_mark(0.26, VENV).next_to(pg_l, RIGHT, buff=0.25)
        tmp_pg = page_glyph(0.3).move_to([2.35, win.sheet.frame.get_center()[1], 0])
        tmp_tag = row_tag("/tmp · throwaway")
        place(tmp_tag, cx=tmp_pg.get_center()[0] + 0.55, bottom=win.sheet.frame.get_top()[1] + 0.1)
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(cap1, shift=UP * 0.1), FadeIn(cap2, shift=UP * 0.1), FadeIn(pen, shift=DOWN * 0.2),
                      run_time=0.6)
            vo.wait_until("show up inside")
            self.play(pen.animate(rate_func=wiggle).shift(RIGHT * 0.12), win.blink("cli.py"),
                      route_pulse(win), run_time=1.1)
            self.play(pen.animate(rate_func=wiggle).shift(RIGHT * 0.12), win.blink("cli.py"),
                      route_pulse(win), run_time=1.0)
            vo.wait_until("Anything written under")
            self.play(FadeOut(pen), FadeIn(pg_l, scale=1.3), FadeIn(pg_c, scale=1.3), run_time=0.5)
            self.remove(pg_l, pg_c)
            win.laptop.rows.add(pg_l)
            win.cover.rows.add(pg_c)
            vo.wait_until("goes straight into")
            self.play(Indicate(pg_l, color=TURN, scale_factor=1.3), Indicate(pg_c, color=TURN, scale_factor=1.3),
                      route_pulse(win), run_time=0.9)
            vo.wait_until("and stays")
            self.play(Create(chk), run_time=0.4)
            vo.wait_until("anything else")
            self.play(FadeIn(tmp_pg, shift=DOWN * 0.45), run_time=0.6)
            vo.wait_until("the throwaway layer")
            self.play(FadeIn(tmp_tag, shift=DOWN * 0.1), Indicate(win.sheet.frame, color=CTR, scale_factor=1.02),
                      run_time=0.6)

        # ========================================================== 3 · ponder: lecture 2's layout
        cav = win.image.cavity
        card = compact_ponder(PONDER_Q)

        def layout3():
            """What is placed against V3 once it has moved up to Y_WIN: the illustration tag,
            lecture 2's /app/.venv box (frame, label), and the ponder card."""
            ill = illustration_tag("lecture 2's layout")
            place(ill, left=win.laptop.frame.get_left()[0],
                  cy=(win.laptop.frame.get_top()[1] + TRACK_BOTTOM) / 2)
            fr = box(cav.width - 0.3, 0.34, VENV, fill_opacity=0.12)
            fr.move_to(win._row_pos(cav, 4), aligned_edge=LEFT).shift(LEFT * 0.03)
            lab = mono("/app/.venv", SZ, VENV).move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.15)
            place(card, cx=0, top=win.laptop.caption.get_bottom()[1] - 0.1)
            assert card.get_bottom()[1] > -3.58, card.get_bottom()[1]
            return ill, fr, lab

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(cap2, chk, tmp_pg, tmp_tag)), win.animate.shift(UP * (Y_WIN - Y0)),
                      run_time=0.6)
            ill, v_fr, v_lab = layout3()
            home_fr, home_lab = win.venv.frame.copy(), win.venv.label.copy()
            vo.wait_until("In lecture 2")
            self.play(FadeIn(ill, shift=DOWN * 0.1), run_time=0.4)
            self.play(win.cover_to(0.5), Transform(win.copied, op_target(win.copied, 1.0)), run_time=1.0)
            vo.wait_until("the venv sat next to")
            v_lab.set_opacity(0)
            win.venv.add(v_lab)              # under the laptop sheet, like the rest of the venv box
            self.play(Transform(win.venv.frame, v_fr), win.venv.label.animate.move_to(v_lab).set_opacity(0),
                      v_lab.animate.set_opacity(1), run_time=1.1)
            vo.wait_until("If it sat in slash app")
            self.play(Indicate(win.venv, color=VENV, scale_factor=1.08), run_time=0.8)
            vo.wait_until("with this mount")
            self.play(frame_pulse(win.cover.frame, INK), route_pulse(win), run_time=0.8)
        self.play(FadeIn(card, scale=0.95), run_time=0.6)
        bar = card[3]
        self.play(bar.animate(rate_func=linear).become(bar.copy().scale(0.001, about_point=bar.get_start())),
                  run_time=8)

        # ========================================================== 4 · the answer, and line 9
        start = sans("start: bash, venv on", SZ, CTR)
        ax = cav.get_left()[0] + 2.1
        place(start, cx=ax, bottom=win.sheet.frame.get_top()[1] + 0.32)
        tip_y = cav.get_top()[1] + 0.03
        arr = Arrow([ax, start.get_bottom()[1] - 0.06, 0], [ax, tip_y, 0], buff=0, color=CTR, stroke_width=5,
                    max_tip_length_to_length_ratio=0.12)
        act = sans("activate", SZ, CTR)
        place(act, left=ax + 0.15, cy=(win.image.frame.get_top()[1] + cav.get_top()[1]) / 2)
        xm = cross_mark(0.24, ERR).move_to([ax, tip_y + 0.02, 0])
        nov = sans("no .venv on your laptop", SZ, ERR)
        place(nov, left=act.get_left()[0], cy=act.get_center()[1])
        p9 = file_panel(DF, 9, 9, "transcribe_audio/Dockerfile")
        place(p9, right=6.3, top=win.image.caption.get_bottom()[1] - 0.14)
        src9 = VGroup(label("from", SZ, S.GREY), mono("transcribe_audio/README.md", SZ, S.GREY),
                      label("· lines 41–90", SZ, S.GREY)).arrange(RIGHT, buff=0.12)
        place(src9, right=p9.code.get_right()[0], top=p9.code.get_bottom()[1] - 0.1)
        bar9 = line_bar(p9.code, 0, VENV, 0.2)
        var9 = code_span(p9.code, 0, "UV_PROJECT_ENVIRONMENT")
        val9 = code_span(p9.code, 0, "/home/app/.venv")
        u9 = Line(val9.get_corner(DL) + DOWN * 0.07, val9.get_corner(DR) + DOWN * 0.07, color=VENV, stroke_width=4)
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(card), run_time=0.4)
            self.play(win.cover_to(1.0), Transform(win.copied, op_target(win.copied, 0.3)), run_time=1.1)
            vo.wait_until("with no venv in it")
            self.play(FadeIn(start, shift=DOWN * 0.1), run_time=0.4)
            self.play(GrowArrow(arr), FadeIn(act), run_time=0.6)
            vo.wait_until("so activation would fail")
            self.play(arr.animate.set_color(ERR), act.animate.set_color(ERR), FadeIn(xm, scale=1.4), run_time=0.5)
            self.play(FadeOut(act), FadeIn(nov), run_time=0.5)
            vo.wait_until("That's what line 9")
            self.play(FadeOut(VGroup(start, arr, nov, xm, ill)), run_time=0.4)
            self.play(Transform(win.venv.frame, home_fr), Transform(win.venv.label, home_lab),
                      v_lab.animate.set_opacity(0), run_time=1.0)
            win.venv.remove(v_lab)
            self.play(FadeIn(p9, shift=UP * 0.15), FadeIn(src9), run_time=0.5)
            self.play(FadeIn(bar9), run_time=0.3)
            vo.wait_until("uv project environment")
            self.play(Indicate(var9, color=VENV, scale_factor=1.12), run_time=0.7)
            vo.wait_until("prevents")
            self.play(Create(u9), Indicate(win.venv.label, color=VENV, scale_factor=1.15), run_time=0.7)

        # ========================================================== 5 · docker run (README line 99)
        t = term(P_A, BIG)
        chip_r = readme_chip("transcribe_audio/README.md · line 99")
        place(chip_r, right=6.45, cy=tr.get_center()[1])
        assert chip_r.get_left()[0] > tr.get_right()[0] + 0.15
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(win, shift=UP * 0.3), FadeOut(VGroup(p9, src9, bar9, u9), shift=UP * 0.3),
                      FadeIn(t, shift=UP * 0.3), FadeIn(chip_r, shift=DOWN * 0.1), run_time=0.7)
            c5 = type_cmd(self, t, RUN, 1.1)
            r2 = c5.rows[1]
            assert r2.text == '    --rm -ti -v "$(pwd):/app" transcribe_audio', r2.text
            y_a, y_b = row_y(t, 2), row_y(t, 3)

            def part(sub, words, color, y, tick=False):
                u = uline(r2, sub, color)
                lab = label(words, SZ, color).move_to([u.get_center()[0], y, 0])
                g = VGroup(u, lab)
                if tick:
                    g.add(Line([u.get_center()[0], u.get_y() - 0.03, 0], [u.get_center()[0], lab.get_top()[1] + 0.04, 0],
                               color=color, stroke_width=2))
                return g

            l_rm = part("--rm", "delete on exit", S.GREY, y_a)
            l_ti = part("-ti", "interactive terminal", S.GREY, y_b, tick=True)
            l_v = part('-v "$(pwd):/app"', "the window", LOOKUP, y_a)
            l_img = part("transcribe_audio", "the image", S.GREY, y_a)
            place(l_rm[1], right=l_ti[2].get_x() - 0.15)
            labels5 = VGroup(l_rm, l_ti, l_v, l_img)
            vo.wait_until("dash dash r m")
            self.play(Create(l_rm[0]), FadeIn(l_rm[1], shift=UP * 0.08), run_time=0.4)
            vo.wait_until("dash t i")
            self.play(Create(l_ti[0]), Create(l_ti[2]), FadeIn(l_ti[1], shift=UP * 0.08), run_time=0.4)
            vo.wait_until("dash v with the mount")
            self.play(Create(l_v[0]), FadeIn(l_v[1], shift=UP * 0.08),
                      substring(r2, '-v "$(pwd):/app"').animate.set_color(LOOKUP), run_time=0.5)
            vo.wait_until("and the image name")
            self.play(Create(l_img[0]), FadeIn(l_img[1], shift=UP * 0.08), run_time=0.4)
            self.play(Indicate(substring(r2, "transcribe_audio"), color=CTR, scale_factor=1.1), run_time=0.6)
            vo.wait_until("Copy it from the README")
            self.play(frame_pulse(chip_r.frame, TURN, 4), Indicate(chip_r.where, color=TURN, scale_factor=1.06),
                      run_time=0.7)
            vo.wait_until("quotes included")
            q1, q2 = substring(r2, '"', 0), substring(r2, '"', 1)
            self.play(q1.animate.set_color(TURN).scale(1.3), q2.animate.set_color(TURN).scale(1.3), run_time=0.4)
            self.play(q1.animate.scale(1 / 1.3), q2.animate.scale(1 / 1.3), run_time=0.3)
            vo.wait_until("and pause to run it")
            yt = beside(your_turn(), t, c5)
            pin(self, c5, yt, run_time=0.4)
            self.play(Wiggle(yt, scale_value=1.15, rotation_angle=0.025 * TAU), run_time=0.7)

        # ========================================================== 6 · Windows notes
        wc = windows_card()
        place(wc, cx=0, bottom=-1.32)
        assert wc.header.get_top()[1] < TRACK_BOTTOM - 0.05, wc.header.get_top()[1]
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(labels5), run_time=0.3)
            resize(self, t, 3, run_time=0.7)
            self.play(FadeIn(wc.frame), FadeIn(wc.header), FadeIn(wc.title, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("run these commands")
            self.play(FadeIn(wc.rows[0], shift=RIGHT * 0.15), run_time=0.5)
            self.play(Indicate(wc.rows[0][-1], color=INK, scale_factor=1.12), run_time=0.6)
            vo.wait_until("keep the quotes")
            self.play(FadeIn(wc.rows[1], shift=RIGHT * 0.15), run_time=0.5)
            self.play(Indicate(q1, color=TURN, scale_factor=1.6), Indicate(q2, color=TURN, scale_factor=1.6),
                      Indicate(wc.rows[1][1], color=TURN, scale_factor=1.15), run_time=0.8)
            vo.wait_until("and if docker run says")
            self.play(FadeIn(wc.rows[2], shift=RIGHT * 0.15), run_time=0.5)
            self.play(Indicate(wc.rows[2][1], color=ERR, scale_factor=1.08), run_time=0.8)
            vo.wait_until("put winpty in front")
            self.play(FadeIn(wc.chip, shift=UP * 0.1), FadeIn(wc.note), run_time=0.5)
            self.play(wc.winpty.animate.set_color(TURN), Indicate(wc.rows[2][3], color=TURN, scale_factor=1.2),
                      run_time=0.6)

        # ========================================================== 7 · inside: the prompt
        with self.voiceover(SAY[7]) as vo:
            unpin(self, c5, yt)
            self.play(FadeOut(wc), FadeOut(chip_r), run_time=0.4)
            resize(self, t, BIG, run_time=0.7)
            self.play(*enter_container(t, "transcribe_audio"), run_time=0.5)
            pr = bare_prompt(self, t)
            self.play(Indicate(pr, color=INK, scale_factor=1.06), run_time=0.6)
            ya, yb = row_y(t, 3), row_y(t, 4) - 0.14      # the id tag clears the two tags above it

            def ptag(sub, words, color, y, tick=False):
                u = uline(pr, sub, color)
                tg = row_tag(words, color).move_to([u.get_center()[0], y, 0])
                g = VGroup(u, tg)
                if tick:
                    g.add(Line([u.get_center()[0], u.get_y() - 0.03, 0], [u.get_center()[0], tg.get_top()[1], 0],
                               color=color, stroke_width=2))
                return g

            g_user = ptag("app", "user", S.GREY, ya)
            g_app = ptag("/app", "the window", LOOKUP, ya)
            g_id = ptag("5b4d4981ec25", "container id · yours differs", S.GREY, yb, tick=True)
            place(g_user[1], left=t.box.get_left()[0] + 0.15)
            vo.wait_until("you're user app")
            self.play(Create(g_user[0]), FadeIn(g_user[1], shift=UP * 0.08), run_time=0.4)
            vo.wait_until("in slash app")
            self.play(Create(g_app[0]), FadeIn(g_app[1], shift=UP * 0.08), run_time=0.4)
            vo.wait_until("and after the at sign")
            self.play(Create(g_id[0]), Create(g_id[2]), FadeIn(g_id[1], shift=UP * 0.08), run_time=0.5)
            vo.wait_until("new on every run")
            self.play(Indicate(substring(pr, "5b4d4981ec25"), color=INK, scale_factor=1.15), run_time=0.8)
        tags7 = VGroup(g_user, g_app, g_id)

        # ========================================================== 8 · which python, python --version
        nm = mono("(transcribe-audio)", SZ, S.GREY)
        note1 = VGroup(label("no", SZ, S.GREY), nm, label("in the prompt", SZ, S.GREY)).arrange(RIGHT, buff=0.12)
        note2 = label("· the venv is active anyway", SZ, S.GREY)
        note = VGroup(note1, note2).arrange(RIGHT, buff=0.15)
        for m in (*note1[::2], note2):
            m.align_to(note1[0], DOWN)
        place(note, left=t.box.get_left()[0] + 0.1, cy=(t.box.get_top()[1] + TRACK_BOTTOM) / 2)
        nm_x = Line(nm.get_left() + LEFT * 0.05, nm.get_right() + RIGHT * 0.05, color=S.GREY, stroke_width=3)
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(tags7), caption_extra(tr), run_time=0.4)
            self.play(FadeIn(note1, shift=DOWN * 0.1), run_time=0.5)
            self.play(Create(nm_x), Indicate(substring(pr, P_CTR), color=INK, scale_factor=1.05), run_time=0.6)
            vo.wait_until("yet the venv is active")
            self.play(FadeIn(note2, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("two extra checks")
            c8a = type_cmd(self, t, WHICH, 0.5)
            pin(self, c8a, beside(extra_tag(), t, c8a), run_time=0.3)
            o8a = t.print(self, [OUT_WHICH], run_time=0.3)[0]
            vo.wait_until("find python in slash home")
            u8a = uline(o8a, "/home/app/.venv", VENV)
            self.play(substring(o8a, "/home/app/.venv").animate.set_color(VENV), Create(u8a), run_time=0.4)
            stick(self, o8a, u8a)
            c8b = t.type(self, VERSION, 0.6)
            pin(self, c8b, beside(extra_tag(), t, c8b), run_time=0.3)
            o8b = t.print(self, [OUT_VERSION], run_time=0.3)[0]
            vo.wait_until("version 3.12")
            u8b = uline(o8b, "3.12.15", SYSTEM)
            self.play(substring(o8b, "3.12.15").animate.set_color(SYSTEM), Create(u8b), run_time=0.4)
            stick(self, o8b, u8b)
            self.play(FadeOut(VGroup(note, nm_x)), run_time=0.3)

        # ========================================================== 9 · ls -a, echo (extras)
        p10 = file_panel(DF, 10, 10, "transcribe_audio/Dockerfile", size=SZ)
        place(p10, left=t.box.get_left()[0], bottom=t.box.get_top()[1] + 0.14)
        assert p10.get_top()[1] < TRACK_BOTTOM - 0.05, p10.get_top()[1]
        val10 = code_span(p10.code, 0, "secrets/mega-pipeline.json")
        u10 = Line(val10.get_corner(DL) + DOWN * 0.07, val10.get_corner(DR) + DOWN * 0.07, color=LOOKUP,
                   stroke_width=4)
        with self.voiceover(SAY[9]) as vo:
            c9a = t.type(self, LS, 0.3)
            pin(self, c9a, beside(extra_tag(), t, c9a), run_time=0.3)
            o9 = t.print(self, [OUT_LS], run_time=0.4, wrap=True)
            ra, rb = o9[0], o9[1]
            assert "pyproject.toml" in ra.text and rb.text.strip() == "secrets", (ra.text, rb.text)
            vo.wait_until("shows your laptop's files")
            bars = [sbar(ra, "Dockerfile", S.GREY, 0.35), sbar(ra, "pyproject.toml", S.GREY, 0.35),
                    sbar(rb, "secrets", S.GREY, 0.35)]
            yf = beside(row_tag("your laptop's files"), t, rb, buff=0.45)
            self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.25), run_time=0.6)
            stick(self, ra, bars[0], bars[1])
            stick(self, rb, bars[2])
            pin(self, rb, yf, run_time=0.4)
            c9b = t.type(self, ECHO, 0.9)
            pin(self, c9b, beside(extra_tag(), t, c9b), run_time=0.3)
            o9b = t.print(self, [OUT_ECHO], run_time=0.3)[0]
            vo.wait_until("from line 10")
            self.play(FadeIn(p10, shift=DOWN * 0.1), run_time=0.4)
            u9b = uline(o9b, OUT_ECHO, LOOKUP)
            self.play(o9b.glyphs.animate.set_color(LOOKUP), Create(u9b), Create(u10),
                      val10.animate.set_color(LOOKUP), run_time=0.5)
            stick(self, o9b, u9b)

        # ========================================================== 10 · python cli.py --help (extra)
        with self.voiceover(SAY[10]) as vo:
            c10 = t.type(self, HELP, 0.8)
            pin(self, c10, beside(extra_tag(), t, c10), run_time=0.3)
            self.play(FadeOut(VGroup(p10, u10), shift=UP * 0.1), run_time=0.3)
            o10 = t.print(self, [*OUT_HELP[:3], (OUT_HELP[3], ERR)], run_time=0.8)
            r13, r14 = o10[2], o10[3]
            vo.wait_until("Module not found")
            u14 = uline(r14, "ModuleNotFoundError", ERR)
            self.play(Create(u14), Indicate(r14.glyphs, color=ERR, scale_factor=1.04), run_time=0.7)
            stick(self, r14, u14)
            vo.wait_until("no module named google")
            u14b = uline(r14, "No module named 'google'", ERR)
            u13 = uline(r13, "google", ERR)
            self.play(Create(u14b), Create(u13), substring(r13, "google").animate.set_color(ERR), run_time=0.6)
            stick(self, r14, u14b)
            stick(self, r13, u13)
            vo.wait_until("the packages aren't")
            self.play(Indicate(r13.glyphs, color=INK, scale_factor=1.06), run_time=0.8)

        # ========================================================== 11 · V3 returns; end of part 1
        q = sans("?", 40, ERR, weight="BOLD")
        gchip = chip("google", CLOUD, size=SZ, font=MONO)
        cli_c = win.row("cli.py", "cover")
        part2 = caption("Part 2: packages, and why they vanish", color=S.GREY)
        part2.scale(22 / 20).move_to([0, -2.45, 0])
        with self.voiceover(SAY[11]) as vo:
            self.play(caption_extra(tr, False), run_time=0.3)
            resize(self, t, 3, run_time=0.7)
            self.play(FadeIn(win, shift=DOWN * 0.2), run_time=0.7)
            place(gchip, cx=win.venv.frame.get_center()[0],
                  cy=(win.image.frame.get_top()[1] + win.venv.label.get_top()[1]) / 2 + 0.02)
            place(q, cx=(cav.get_right()[0] + gchip.get_left()[0]) / 2 - 0.25, cy=gchip.get_center()[1])
            vo.wait_until("and sees your folder")
            self.play(route_pulse(win), frame_pulse(win.cover.frame, INK), run_time=0.8)
            vo.wait_until("but Python can't find")
            self.play(cli_c.text.animate.set_color(ERR), FadeIn(gchip, shift=DOWN * 0.1), run_time=0.5)
            link = DashedLine(cli_c.text.get_right() + RIGHT * 0.1, q.get_left() + LEFT * 0.06, color=ERR,
                              stroke_width=2.5, dash_length=0.08)
            self.play(Create(link), FadeIn(q, scale=1.5), Indicate(win.venv.frame, color=VENV, scale_factor=1.06),
                      run_time=0.6)
            self.play(Wiggle(q, scale_value=1.2), run_time=0.8)
            vo.wait_until("In part 2")
            self.play(FadeOut(t), FadeIn(part2, shift=UP * 0.1), run_time=0.6)
        self.wait(0.6)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

