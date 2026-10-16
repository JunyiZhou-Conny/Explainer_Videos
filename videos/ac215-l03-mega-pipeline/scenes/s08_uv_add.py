r"""S08 · uv add: what lands where (README › transcribe_audio steps 7–9; V3 + V4).

Part 2 opens here. The house terminal is the container's (TEAL frame, title `container ·
transcribe_audio`, prompt `app@5b4d4981ec25:/app$`) throughout; it is a 3-row strip whenever a
picture needs the frame (beats 0, 3, 6–9) and 12 rows otherwise.

Beats (script.md "## S08", one voiceover block each):
 0  TRACKER A6. Part 1's last picture exactly as S07 leaves it (s07_run.py beat 11: V3 mounted at
    y 0.75, S07's page at row 4, `cli.py` RED on the sheet, a solid BLUE `google` chip above the
    empty GREEN venv box, a dashed RED line from `cli.py` ending at a RED "?"; V4's shelf hidden,
    as S07 keeps it) above the 3-row strip, which holds the last two lines of part 1 (01-docker-run-tty.txt lines 10 and 14, the
    second RED) and the waiting prompt. The title, then the RED line, the "?" and the chip pulse.
 1  TRACKER A7. The picture shrinks away while the strip grows to 12 rows and the README chip
    `transcribe_audio/README.md · lines 104–110 · 3 packages` arrives under the tracker band. Part
    2 is its own upload, so the rows move down and part 1's `docker run --rm -ti -v "$(pwd):/app"
    transcribe_audio` (01-docker-run-tty.txt line 1 on the laptop prompt, folded after `run`)
    fades in on top with a GREY tag "new terminal? run this". It types `uv add
    google-cloud-storage google-cloud-speech ffmpeg-python` (folds after `google-cloud-storage`);
    ▶ your turn on "Pause and run it". The docker run, --help and error rows scroll off;
    TERM(02-uv-add.txt: 2, …, 8, …, 13, …, 18–19, …, 34: every skip marked); the three asked-for
    names turn GREEN in the `+` lines; GREY tag "at the time of recording" beside the version list.
 2  A chip "asked for 3" beside line 8 (`Installed 26 packages`) transforms into GREEN "installed
    26", with an arrow to the line. On "each package brings" the three `…` rows among the `+` rows
    and `urllib3` get GREY bars and a GREY label "dependencies"; "Resolved" underlines PURPLE ("uv resolves the whole
    tree").
 3  The terminal shrinks to the strip (the command and line 8 with its counter chip). V3 + V4
    above it: on "pyproject.toml" its row turns GREEN on the laptop and on the sheet over /app at
    the same instant (three GREEN lines draw into both glyphs); `uv.lock` appears GREEN on both
    sides at once; `/app` pulses; both files blink on both sides and the route pulses (nothing
    travels). On "The 26 packages" the counter chip pulses and 26 GREEN chips drop into the
    /home/app/.venv box; the venv label pulses; on "on the container's throwaway layer" the GREEN
    shelf of the dashed writable layer (hidden until now, as in S07) draws right above the venv and
    the chips rise onto it (where they are stored); the sheet's caption becomes "writable layer ·
    throwaway".
 4  TRACKER A7 · extra. The picture goes; the terminal grows back to 12 rows (cleared). `cat
    pyproject.toml` (extra) → TERM(03: 2–10); lines 7–9 turn GREEN with a bar, their `>=…` lower
    bounds underline GREEN. The cat block scrolls off; `ls -la` (extra) → TERM(04: 2–11); line 11
    (`uv.lock`) GREEN with a bar, `138445` pulses, `cli.py`'s row pulses, the owner `app` of
    uv.lock underlines YELLOW.
 5  `echo $VIRTUAL_ENV` (extra; the capture's `;`-joined line, only this command typed) →
    TERM(10-venv-where.txt: 3); `/home/app/.venv` turns GREEN and underlines GREEN; GREY tag
    "outside the window".
 6  TRACKER A7. The terminal shrinks to the strip. Two GREY-framed cards above it, one after the
    other, each frame growing as its items arrive. First: GREEN chip `ffmpeg-python` + GREEN
    check, GREY chip `ffmpeg` + RED cross, "different PyPI projects". On "And on a Linux laptop"
    it lifts away and the second takes its place: tag `extra` + "Linux, folder not owned by uid
    1000" with GREY "Docker Desktop (macOS, Windows) handles this" right under it (up for the whole
    aside); TERM(13-g7-root-owned.txt: 4) in RED, folded at a space onto 2 rows; GREY "fix (not in
    the README): exit, then on your laptop, in the component folder:" over `sudo chown -R
    1000:1000 .` + GREY "· then docker run again" (the container's user app can't chown /app).
    The card holds about 4 s after the fix arrives (2 s past the line).
 7  The card goes. The README chip `transcribe_audio/README.md · line 110` "After exiting the
    container, re-build the image" above the strip; the phrase turns YELLOW and underlines; GREY
    tag "step 13" under it, and the tracker's step-13 dot pulses.
 8  TRACKER A8. A GREY editor window "VS Code · on your laptop" with CODE(transcribe_audio/
    cli.py: 21) (comment cut); `"pavlos"` transforms into `"group-01"` (the line from
    06-group-name.txt line 2, `21:` stripped); ▶ your turn; GREY note "the same name in all five
    cli.py" with five TEAL boxes A–E.
 9  TRACKER A8 · extra. In the strip `grep -n "^group_name" cli.py` (extra) → TERM(06: 2);
    `group-01` turns YELLOW with a box. A PINK arrow labelled `-v · the window` from the editor's
    `"group-01"` to the strip; both `group-01`s blink at the same instant and the arrow pulses
    (two-headed: one folder, two sides; nothing travels). The note pulses; the five boxes flash
    GREEN, then GREY arrows draw V1's real hand-offs: A→B, B→C, B→D (curving under C), D→E.
10  TRACKER A9 (on "Step 9", as the editor goes); the terminal grows back to 12 rows (cleared):
    `python cli.py --help` → TERM(05-help.txt: 2–10). The README's block (transcribe_audio/
    README.md · lines 117–126, its first line on the typed command) fades in from the upper right
    as a translucent GREY overlay and lands exactly on the printed rows; a GREEN check ticks beside
    each non-blank row. On "Pause" the overlay lifts off (checks and header stay); ▶ your turn
    beside the command. Everything fades: empty frame.
"""

import numpy as np
from manim import *

from explainer import style as S
from explainer.devops import (MONO, box, cell_width, check_mark, chip, code_panel, code_span,
                              cross_mark, label, mono, mono_line, substring, tag)
from explainer.scene import VoiceScene

from common import (CLOUD, CTR, ERR, GROUP, INK, LOOKUP, NARRATION, P_A, P_CTR, STRIP_TOP, TOOL, TURN, VENV,
                    Window,
                    beside, caption_extra, capture, cut_comment, editor_inset, excerpt, extra_tag,
                    page_token, pin, pkg_dots, readme_chip, recorded_tag, resize, sans, source_text,
                    src_panel, term, tracker, type_cmd, unpin, your_turn)

SAY = NARRATION["S08"]

# ------------------------------------------------------------------ commands and real outputs
_RUN = capture("01-docker-run-tty", "transcribe_audio")
RUN_CMD = _RUN.cmd                                # line 1: how part 1 got inside (README :99)
assert RUN_CMD == 'docker run --rm -ti -v "$(pwd):/app" transcribe_audio', RUN_CMD
RECAP_CMD = _RUN.line(10)                         # the prompt line as captured
RECAP_ERR = _RUN.line(14)
assert RECAP_CMD == f"{P_CTR} python cli.py --help", RECAP_CMD
assert RECAP_ERR == "ModuleNotFoundError: No module named 'google'", RECAP_ERR

ADD = capture("02-uv-add", "transcribe_audio")
ADD_CMD = "uv add google-cloud-storage google-cloud-speech ffmpeg-python"   # README :104-108
assert ADD.cmd == ADD_CMD, ADD.cmd
# every skipped run of lines gets its `…` row (lines 3-7 are the downloads, the others packages)
ADD_OUT = ADD.at(2, "…", 8, "…", 13, "…", (18, 19), "…", 34)
assert ADD_OUT[0].startswith("Resolved 27 packages") and ADD_OUT[2].startswith("Installed 26 packages")
assert ADD_OUT[4] == " + ffmpeg-python==0.2.0" and ADD_OUT[6].startswith(" + google-cloud-speech==")
assert ADD_OUT[7].startswith(" + google-cloud-storage==") and ADD_OUT[9].startswith(" + urllib3==")
assert [ADD_OUT[i] for i in (1, 3, 5, 8)] == ["…"] * 4, ADD_OUT
ASKED = ["ffmpeg-python", "google-cloud-speech", "google-cloud-storage"]

CAT = capture("03-cat-pyproject", "transcribe_audio")
assert CAT.cmd == "cat pyproject.toml", CAT.cmd
CAT_OUT = CAT.at((2, 10))
assert [s.strip() for s in CAT_OUT[5:8]] == ['"ffmpeg-python>=0.2.0",', '"google-cloud-speech>=2.41.0",',
                                              '"google-cloud-storage>=3.17.0",'], CAT_OUT

LS = capture("04-ls", "transcribe_audio")
assert LS.cmd == "ls -la", LS.cmd
LS_OUT = LS.at((2, 11))
assert LS_OUT[-1].endswith("uv.lock") and " 138445 " in LS_OUT[-1] and LS_OUT[6].endswith("cli.py")

_VE = capture("10-venv-where", "transcribe_audio")
VE_CMD = "echo $VIRTUAL_ENV"                       # the `;`-joined capture: only this one is typed
assert _VE.cmd.split("; ")[1] == VE_CMD, _VE.cmd
VE_OUT = _VE.at(3)
assert VE_OUT == ["/home/app/.venv"], VE_OUT

G7_ERR = capture("13-g7-root-owned", "transcribe_audio").line(4)
assert G7_ERR.endswith("Permission denied (os error 13)"), G7_ERR

GREP = capture("06-group-name", "transcribe_audio")
assert GREP.cmd == 'grep -n "^group_name" cli.py', GREP.cmd
GREP_OUT = GREP.at(2)
assert GREP_OUT[0].startswith('21:group_name = "group-01"'), GREP_OUT
AFTER_21 = cut_comment(GREP_OUT[0][3:])          # the "after" line 21, prefix `21:` stripped
BEFORE_21 = excerpt("transcribe_audio/cli.py", 21, 21, cut_comments=True)
assert BEFORE_21 == 'group_name = "pavlos"  # …' and AFTER_21 == 'group_name = "group-01"  # …'

HELP = capture("05-help", "transcribe_audio")
assert HELP.cmd == "python cli.py --help", HELP.cmd
HELP_OUT = HELP.at((2, 10))
_RA = source_text("transcribe_audio/README.md").split("\n")
README_BLOCK = _RA[116:126]                      # transcribe_audio/README.md lines 117-126
assert README_BLOCK[0] == "python cli.py --help" and README_BLOCK[1:] == HELP_OUT, README_BLOCK
assert _RA[103] == "## Python packages required" and all(p in _RA[104 + i] for i, p in
                                                         enumerate(["google-cloud-storage",
                                                                    "google-cloud-speech",
                                                                    "ffmpeg-python"], start=1))
REBUILD = "After exiting the container, re-build the image"
assert REBUILD in _RA[109], _RA[109]             # line 110
assert _RA[98] == RUN_CMD, _RA[98]               # line 99

# ------------------------------------------------------------------ layout
BIG = 12                           # terminal rows when it is up (top at y 2.19)
TRACK_BOTTOM = 2.92                # the tracker band is y 2.92..3.5
WIN_Y = 0.75                       # Window centre above a 3-row strip
EDGE = 6.45


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


def make_room(scene, t, n: int, at_least: int = 0):
    """Room for n new rows before typing/printing: the oldest rows fade where they are, then the
    rest move up (Terminal's own scroll would slide them over the title bar)."""
    over = max(len(t.lines) + n - t.rows, at_least)
    over = min(over, len(t.lines))
    if over <= 0:
        return
    gone = t.lines.submobjects[:over]
    stay = VGroup(*t.lines.submobjects[over:])
    scene.play(FadeOut(VGroup(*gone)), run_time=0.25)
    for m in gone:
        t.lines.remove(m)
        scene.remove(m)
    if len(stay):
        scene.play(stay.animate.shift(UP * t.pitch * over), run_time=0.35)


def seed(t, text: str, color=INK, prompt: bool = False, bare: bool = False):
    """Put a line on terminal t without animation (the terminal fades in with it)."""
    ln = mono_line(text, t.size, color, t2c=t._prompt_colors(t.prompt) if prompt else None)
    t._place(ln, len(t.lines))
    t.lines.add(ln)
    if bare:
        ln.bare = True
    return ln


def rbar(lines, color, opacity=0.2, pad=0.08, right=None) -> Rectangle:
    """A translucent bar behind whole terminal rows (first glyph to last, or to x=right)."""
    lines = lines if isinstance(lines, (list, tuple)) else [lines]
    left = min(ln.glyphs.get_left()[0] for ln in lines) - pad
    rx = right if right is not None else max(ln.glyphs.get_right()[0] for ln in lines) + pad
    top = lines[0].strut.get_top()[1] + 0.02
    bot = lines[-1].strut.get_bottom()[1] - 0.02
    return Rectangle(width=rx - left, height=top - bot, stroke_width=0).set_fill(color, opacity) \
        .move_to([(left + rx) / 2, (top + bot) / 2, 0])


def uline(line, sub, color, stroke=3.5, occ=0, pad=0.02) -> Line:
    """A Line under substring `sub` of terminal row `line`, in the gap under the row."""
    g = substring(line, sub, occ)
    y = line.strut.get_bottom()[1] + 0.01
    return Line([g.get_left()[0] - pad, y, 0], [g.get_right()[0] + pad, y, 0], color=color,
                stroke_width=stroke)


def stick(scene, line, *mobs):
    """Make mobs (already on screen) part of terminal row `line` (its last row when folded)."""
    row = line.rows[-1] if hasattr(line, "rows") else line
    for m in mobs:
        scene.remove(m)
        row.add(m)
    scene.add(row)


def three_lines(glyph) -> VGroup:
    """Three short GREEN text lines drawn inside a file glyph (pyproject.toml gains 3 lines)."""
    page = glyph[0]
    w, h = page.width, page.height
    x0 = page.get_left()[0] + w * 0.18
    ys = [page.get_center()[1] + h * f for f in (0.05, -0.12, -0.29)]
    return VGroup(*[Line([x0, y, 0], [x0 + w * 0.6, y, 0], color=VENV, stroke_width=2.2) for y in ys])


def counter_chip(text: str, color) -> VGroup:
    return chip(text, color, size=22, text_color=color if color != S.GREY else INK)


def readme_note_chip(where: str, note: str) -> VGroup:
    """A README chip whose words are ours, not the README's (so: no quotes)."""
    path, _, rest = where.partition(" · ")
    row = VGroup(mono(path, 20, S.GREY), label(f"· {rest}", 20, S.GREY), label(f"· {note}", 20, INK))
    row.arrange(RIGHT, buff=0.12)
    for p in row[1:]:
        p.align_to(row[0], DOWN)
    fr = box(row.width + 0.4, row.height + 0.24, S.GREY, fill=S.BG, fill_opacity=0.92, radius=0.1)
    fr.move_to(row)
    return VGroup(fr, row)


def card_frame(content, pad_x=0.3, pad_y=0.22) -> RoundedRectangle:
    fr = RoundedRectangle(width=content.width + 2 * pad_x, height=content.height + 2 * pad_y,
                          corner_radius=0.14, stroke_color=S.GREY, stroke_width=2).set_fill(S.BG, 0.95)
    return fr.move_to(content)


def frame_to(full: RoundedRectangle, last, across: bool = False) -> RoundedRectangle:
    """The card frame `full`, cut short below `last` (top and width kept) or, across=True, right
    of `last` (left edge and height kept): a card that grows as its lines arrive."""
    if across:
        w, h, edge = last.get_right()[0] + 0.3 - full.get_left()[0], full.height, LEFT
    else:
        w, h, edge = full.width, full.get_top()[1] - (last.get_bottom()[1] - 0.22), UP
    fr = RoundedRectangle(width=w, height=h, corner_radius=0.14, stroke_color=S.GREY,
                          stroke_width=2).set_fill(S.BG, 0.95)
    return fr.move_to(full.get_edge_center(edge), aligned_edge=edge)


def fold_words(s: str, n: int) -> list[str]:
    """Fold a line at spaces into rows of at most n characters (the text itself unchanged)."""
    rows = []
    while len(s) > n:
        i = s.rfind(" ", 0, n + 1)
        i = n if i <= 0 else i
        rows.append(s[:i])
        s = s[i:].lstrip(" ")
    return rows + [s]


# ------------------------------------------------------------------ pictures
def recap_window() -> Window:
    """S07's closing V3, rebuilt exactly as s07_run.py leaves it: Window(rows=5) centred at
    (0, 0.75), mounted, the writable sheet on, no key glyph, and the page S07 wrote under /app at
    row 4 on both sides (s07_run.py page_glyph: page_token at 0.32 tall)."""
    win = Window(rows=5, mounted=True).move_to([0, WIN_Y, 0])
    win.sheet.shelf.set_stroke(opacity=0)        # S07 keeps V4's shelf hidden (s07_run.py:308-310)
    for area, rows in ((win.laptop.area, win.laptop.rows), (win.cover.frame, win.cover.rows)):
        pg = page_token().scale_to_fit_height(0.32)
        pg.move_to(win._row_pos(area, 4), aligned_edge=LEFT).shift(RIGHT * 0.02)
        rows.add(pg)
    return win


def recap_extras(win: Window) -> VGroup:
    """S07's closing marks (s07_run.py beat 11), same geometry: cli.py on the laptop sheet RED; a
    SOLID BLUE `google` chip (20 pt mono) centred over the venv box, between the image's top edge
    and the venv label; a RED '?' (40 pt bold) between /app and the chip; a dashed RED line from
    cli.py that ends at the '?'. .chip .link .q (cli.py's colour is set on the window itself)."""
    cli = win.row("cli.py", "cover")
    cli.text.set_color(ERR)
    g = chip("google", CLOUD, size=20, font=MONO)
    place(g, cx=win.venv.frame.get_center()[0],
          cy=(win.image.frame.get_top()[1] + win.venv.label.get_top()[1]) / 2 + 0.02)
    q = sans("?", 40, ERR, weight="BOLD")
    place(q, cx=(win.image.cavity.get_right()[0] + g.get_left()[0]) / 2 - 0.25, cy=g.get_center()[1])
    link = DashedLine(cli.text.get_right() + RIGHT * 0.1, q.get_left() + LEFT * 0.06, color=ERR,
                      stroke_width=2.5, dash_length=0.08)
    grp = VGroup(link, g, q)
    grp.chip, grp.link, grp.q = g, link, q
    return grp


def ffmpeg_card() -> VGroup:
    good = VGroup(chip("ffmpeg-python", VENV, size=22, font=MONO), check_mark(0.3, VENV))
    bad = VGroup(chip("ffmpeg", S.GREY, size=22, font=MONO), cross_mark(0.26, ERR))
    good.arrange(RIGHT, buff=0.18)
    bad.arrange(RIGHT, buff=0.18)
    cap = label("different PyPI projects", 22, S.GREY)
    row = VGroup(good, bad, cap).arrange(RIGHT, buff=0.6)
    fr = card_frame(row)
    g = VGroup(fr, row)
    g.frame, g.good, g.bad, g.cap = fr, good, bad, cap
    return g


def root_card() -> VGroup:
    """Who the aside is for (head, and right under it who it is not for: desk), the error, and the
    fix with where to run it (the container's user app can't chown the folder). .head .desk .err
    .fix (.where .cmd)"""
    head = VGroup(extra_tag(), label("Linux, folder not owned by uid 1000", 22, INK)).arrange(RIGHT, buff=0.2)
    desk = label("Docker Desktop (macOS, Windows) handles this", 20, S.GREY)
    top = VGroup(head, desk).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    folded = fold_words(G7_ERR, 52)               # at the space after `.../pyproject.toml`:
    assert folded == ["error: failed to create file `/app/pyproject.toml`:",
                      "Permission denied (os error 13)"], folded
    err_rows = VGroup(*[mono_line(s, 20, ERR) for s in folded])
    for i, r in enumerate(err_rows):
        r.shift(DOWN * i * 0.36 - r.strut.get_corner(UL))
    where = label("fix (not in the README): exit, then on your laptop, in the component folder:", 20, S.GREY)
    cmd = VGroup(mono("sudo chown -R 1000:1000 .", 20, INK), label("· then docker run again", 20, S.GREY))
    cmd.arrange(RIGHT, buff=0.18)
    cmd[0].align_to(cmd[1], DOWN).shift(DOWN * 0.02)
    fix = VGroup(where, cmd).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    body = VGroup(top, err_rows, fix).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
    fr = card_frame(body, pad_x=0.3, pad_y=0.22)
    g = VGroup(fr, body)
    g.frame, g.head, g.desk, g.err, g.fix = fr, head, desk, err_rows, fix
    g.where, g.cmd = where, cmd
    return g


def stage_boxes() -> VGroup:
    boxes = VGroup(*[VGroup(box(0.5, 0.5, CTR, fill_opacity=0.12, radius=0.08), sans(c, 22, INK))
                     for c in "ABCDE"])
    for b in boxes:
        b[1].move_to(b[0])
    boxes.arrange(RIGHT, buff=0.32)
    return boxes


def readme_overlay(t) -> VGroup:
    """transcribe_audio/README.md lines 117-126 as mono rows at the terminal's size, each placed on
    terminal row k (row 0 after the prompt, where the typed command starts), on a translucent GREY
    panel; the header (path · lines) under its right end. .rows .panel .header"""
    cw = cell_width(t.size)
    rows = VGroup()
    for k, s in enumerate(README_BLOCK):
        ln = mono_line(s if s else " ", t.size, S.GREY)
        off = (len(P_CTR) + 1) * cw if k == 0 else 0.0
        ln.shift(t._slot(k) + RIGHT * off - ln.strut.get_corner(UL))
        rows.add(ln)
    glyphs = VGroup(*[r.glyphs for r in rows if len(r.glyphs)])
    left = t._slot(0)[0] - 0.14
    x_cmd = rows[0].glyphs.get_left()[0] - 0.1          # row 0: from where the command starts
    right = glyphs.get_right()[0] + 0.2
    top = rows[0].strut.get_top()[1] + 0.04
    mid = rows[1].strut.get_top()[1] + 0.02
    bot = rows[-1].strut.get_bottom()[1] - 0.06
    panel = Polygon([x_cmd, top, 0], [right, top, 0], [right, bot, 0], [left, bot, 0], [left, mid, 0],
                    [x_cmd, mid, 0], stroke_color=S.GREY, stroke_width=2).set_fill(S.GREY, 0.16)
    header = VGroup(mono("transcribe_audio/README.md", 20, S.GREY), label("· lines 117–126", 20, S.GREY))
    header.arrange(RIGHT, buff=0.12)
    header[1].align_to(header[0], DOWN)
    place(header, right=right, top=bot - 0.1)
    g = VGroup(panel, rows, header)
    g.rows, g.panel, g.header = rows, panel, header
    return g


# ------------------------------------------------------------------ the scene
class UvAdd(VoiceScene):
    def construct(self):
        assert len(SAY) == 11, f"S08 has {len(SAY)} SAY lines; this scene times 11"

        tr = tracker("A", 6)

        # ========================================================== 0 · welcome back (part 1's picture)
        t = term(P_CTR, 3, component="transcribe_audio")
        seed(t, RECAP_CMD, prompt=True)
        err0 = seed(t, RECAP_ERR, ERR)
        seed(t, P_CTR + " ", prompt=True, bare=True)
        win0 = recap_window()                          # S07's last picture, unchanged
        ex0 = recap_extras(win0)
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.1), FadeIn(t), FadeIn(win0), FadeIn(ex0), run_time=0.9)
            vo.wait_until("We're inside")
            self.play(Indicate(t.title, color=CTR, scale_factor=1.15),
                      Indicate(win0.image.caption, color=CTR, scale_factor=1.12), run_time=0.9)
            vo.wait_until("and Python can't find")
            self.play(Indicate(err0, color=ERR, scale_factor=1.05), Indicate(ex0.q, color=ERR, scale_factor=1.4),
                      run_time=0.9)
            self.play(Indicate(ex0.chip, color=CLOUD, scale_factor=1.15), run_time=0.8)

        # ========================================================== 1 · step 7: uv add
        chip_a = readme_note_chip("transcribe_audio/README.md · lines 104–110", "3 packages")
        place(chip_a, right=EDGE, top=TRACK_BOTTOM - 0.1)
        with self.voiceover(SAY[1]) as vo:
            # the tracker moves on "Step 7" while part 1's picture shrinks away; the README chip
            # arrives as the terminal grows (it lands right after "the README lists")
            self.play(tr.goto(7), FadeOut(win0, scale=0.4, shift=UP * 0.6),
                      FadeOut(ex0, scale=0.4, shift=UP * 0.6), run_time=0.6)
            resize(self, t, BIG, run_time=0.7, extra=[FadeIn(chip_a, shift=DOWN * 0.1)])
            # part 2 is its own upload: the docker run that got us inside (part 1) moves in on top,
            # on the laptop's prompt as S07 typed it, for a viewer starting in a new terminal
            run_rows = t.fold(f"{P_A} {RUN_CMD}", first_prefix=len(P_A) + 1)
            assert run_rows[0].endswith("docker run \\") and len(run_rows) == 2, run_rows
            run_lns = [mono_line(s, t.size, INK, t2c=t._prompt_colors(P_A) if k == 0 else None)
                       for k, s in enumerate(run_rows)]
            for k, ln in enumerate(run_lns):
                t._place(ln, k)
            old = list(t.lines.submobjects)
            nt = beside(tag("new terminal? run this", S.GREY), t, run_lns[-1])
            run_g = VGroup(*run_lns)
            self.play(*[ln.animate.shift(DOWN * t.pitch * len(run_lns)) for ln in old],
                      FadeIn(run_g, shift=DOWN * 0.1), run_time=0.5)
            self.remove(run_g)
            t.lines.remove(*old)
            t.lines.add(*run_lns, *old)
            pin(self, run_lns[-1], nt, run_time=0.4)
            vo.wait_until("the README lists")
            self.play(Indicate(chip_a[1][2], color=INK, scale_factor=1.12), run_time=0.7)
            vo.wait_until("so type all three")
            c1 = type_cmd(self, t, ADD_CMD, 2.0)
            assert c1.rows[0].text.endswith("uv add google-cloud-storage \\"), c1.rows[0].text
            vo.wait_until("Pause and run it")
            yt = beside(your_turn(), t, c1)
            pin(self, c1, yt, run_time=0.4)
            self.play(Wiggle(yt, scale_value=1.12, rotation_angle=0.02 * TAU), run_time=0.6)
            make_room(self, t, len(ADD_OUT))            # docker run, --help and its error go
            assert len(t.lines) == 2, len(t.lines)
            out1 = t.print(self, ADD_OUT, run_time=0.8, lag=0.1)
            resolved, installed = out1[0], out1[2]
            plus = [out1[4], out1[6], out1[7]]
            self.play(*[substring(ln, name).animate.set_color(VENV) for ln, name in zip(plus, ASKED)],
                      run_time=0.5)
            rec = recorded_tag()
            place(rec, right=t.box.get_right()[0] - 0.15, cy=(out1[6].strut.get_center()[1]
                                                               + out1[7].strut.get_center()[1]) / 2)
            pin(self, out1[6], rec, run_time=0.4)

        # ========================================================== 2 · asked for 3, installed 26
        c_ask = counter_chip("asked for 3", S.GREY)
        c_inst = counter_chip("installed 26", VENV)
        x_chip = installed.glyphs.get_right()[0] + 1.25
        for c in (c_ask, c_inst):
            place(c, left=x_chip, cy=installed.strut.get_center()[1])
        arr = Arrow(c_inst.get_left() + LEFT * 0.05, [installed.glyphs.get_right()[0] + 0.12,
                                                      installed.strut.get_center()[1], 0],
                    buff=0, color=VENV, stroke_width=3.5, max_tip_length_to_length_ratio=0.3,
                    tip_length=0.16)
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeIn(c_ask, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("and 26 installed")
            self.play(Transform(c_ask, c_inst), GrowArrow(arr), run_time=0.7)
            stick(self, installed, c_ask, arr)
            self.play(Indicate(substring(installed, "Installed 26 packages"), color=VENV, scale_factor=1.1),
                      run_time=0.7)
            vo.wait_until("each package brings")
            # the rows nobody asked for (the `…` among the + rows, and urllib3) light up GREY:
            # dependencies (the `…` under Resolved stands for the downloads, not packages)
            dep_rows = [out1[3], out1[5], out1[8], out1[9]]
            x_r = out1[7].glyphs.get_right()[0] + 0.08          # as wide as the longest + row
            x_l = min(ln.glyphs.get_left()[0] for ln in dep_rows) - 0.08   # one left edge for all
            dep_bars = [rbar(ln, S.GREY, 0.2, right=x_r) for ln in dep_rows]
            for b in dep_bars:
                b.stretch_to_fit_width(x_r - x_l).align_to([x_l, 0, 0], LEFT)
            dep_lab = label("dependencies", 22, S.GREY)
            place(dep_lab, left=x_r + 0.3, cy=out1[9].strut.get_center()[1])
            self.play(*[FadeIn(b) for b in dep_bars], FadeIn(dep_lab, shift=LEFT * 0.1), run_time=0.6)
            for ln, b in zip(dep_rows, dep_bars):
                stick(self, ln, b)
            stick(self, out1[9], dep_lab)
            self.play(Indicate(VGroup(*[ln.glyphs for ln in dep_rows]), color=INK, scale_factor=1.1),
                      run_time=0.8)
            vo.wait_until("and uv resolves")
            u_res = uline(resolved, "Resolved", TOOL, stroke=4)
            pin(self, resolved, u_res, run_time=0.5, anim=Create(u_res))
            self.play(Indicate(substring(resolved, "Resolved 27 packages"), color=TOOL, scale_factor=1.08),
                      run_time=0.8)

        # ========================================================== 3 · what lands where (V3 + V4)
        win = Window(rows=5, mounted=True).move_to([0, WIN_Y, 0])
        win.sheet.shelf.set_stroke(opacity=0)          # as in beat 0; it draws when it is named
        with self.voiceover(SAY[3]) as vo:
            unpin(self, c1, yt, run_time=0.25)
            resize(self, t, 3, keep=[c1.rows[0], c1.rows[1], installed], run_time=0.7,
                   extra=[FadeOut(chip_a)])
            self.play(FadeIn(win, shift=DOWN * 0.15), run_time=0.6)

            vo.wait_until("The list, pyproject.toml")
            rows_p = [win.row("pyproject.toml", "laptop"), win.row("pyproject.toml", "cover")]
            lines3 = [three_lines(r.glyph) for r in rows_p]
            self.play(*[r.animate.set_color(VENV) for r in rows_p], run_time=0.5)
            win.attach(self, *lines3, anims=[Create(lines3[0]), Create(lines3[1])], run_time=0.6)
            self.play(win.blink("pyproject.toml", VENV), run_time=0.8)

            vo.wait_until("and the receipt")
            win.add_file(self, "uv.lock", VENV, run_time=0.7)
            vo.wait_until("sit in slash app")
            self.play(Indicate(win.image.app, color=TURN, scale_factor=1.4), run_time=0.8)
            vo.wait_until("so they're written")
            both = VGroup(win.row("pyproject.toml", "laptop"), win.row("uv.lock", "laptop"))
            both2 = VGroup(win.row("pyproject.toml", "cover"), win.row("uv.lock", "cover"))
            self.play(Indicate(both, color=VENV, scale_factor=1.12), Indicate(both2, color=VENV, scale_factor=1.12),
                      Indicate(win.route, color=LOOKUP, scale_factor=1.0),
                      Indicate(win.laptop.caption, color=INK, scale_factor=1.15), run_time=1.0)

            vo.wait_until("The 26 packages")
            pk = pkg_dots(26, cols=13)                    # as Window.fill_shelf sizes them
            shelf = win.sheet.shelf
            if pk.width > shelf.get_length() - 0.1:
                pk.scale_to_fit_width(shelf.get_length() - 0.1)
            on_shelf = pk.copy().next_to(shelf, UP, buff=0.03).get_center()
            pk.move_to(win.venv.frame)
            self.play(Indicate(c_ask, color=VENV, scale_factor=1.12), run_time=0.6)
            win.attach(self, pk, anims=[LaggedStart(*[FadeIn(c, shift=DOWN * 0.3) for c in pk],
                                                    lag_ratio=0.05)], run_time=1.3, into=win.sheet)
            win.sheet.chips = pk
            vo.wait_until("in slash home")
            self.play(Indicate(win.venv.label, color=VENV, scale_factor=1.15), run_time=0.8)
            vo.wait_until("on the container's throwaway")
            # where they are stored: the shelf of the dashed writable layer draws, the chips rise
            shelf.set_stroke(opacity=1)
            self.play(Create(shelf), run_time=0.35)
            self.play(pk.animate.move_to(on_shelf), run_time=0.8)
            cap = win.sheet.caption
            new_cap = sans("writable layer · throwaway", 20, CTR).move_to(cap, aligned_edge=LEFT)
            self.play(Transform(cap, new_cap), Indicate(win.sheet.frame, color=CTR, scale_factor=1.03),
                      run_time=0.9)

        # ========================================================== 4 · cat pyproject.toml, ls -la (extras)
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(win), caption_extra(tr), run_time=0.6)
            t.clear(self, run_time=0.3)
            resize(self, t, BIG, run_time=0.6)
            vo.wait_until("The pyproject.toml now")
            c4 = type_cmd(self, t, CAT.cmd, 0.8)
            pin(self, c4, beside(extra_tag(), t, c4), run_time=0.3)
            out4 = t.print(self, CAT_OUT, run_time=0.6, lag=0.1)
            deps3 = list(out4[5:8])
            vo.wait_until("the three packages")
            b3 = rbar(deps3, VENV, 0.2)
            self.play(FadeIn(b3), *[ln.glyphs.animate.set_color(VENV) for ln in deps3], run_time=0.5)
            stick(self, deps3[0], b3)
            vo.wait_until("each with a lower bound")
            lows = [uline(ln, ">=" + ln.text.split(">=")[1].split('"')[0], VENV, stroke=3) for ln in deps3]
            self.play(*[Create(u) for u in lows], run_time=0.5)
            for ln, u in zip(deps3, lows):
                stick(self, ln, u)
            self.play(*[Indicate(substring(ln, ">="), color=INK, scale_factor=1.3) for ln in deps3], run_time=0.7)

            vo.wait_until("and a new uv.lock")
            make_room(self, t, 1 + len(LS_OUT), at_least=len(t.lines))
            c4b = type_cmd(self, t, LS.cmd, 0.4)
            pin(self, c4b, beside(extra_tag(), t, c4b), run_time=0.3)
            out4b = t.print(self, LS_OUT, run_time=0.6, lag=0.08)
            lock, cli = out4b[-1], out4b[6]
            bl = rbar(lock, VENV, 0.2)
            self.play(FadeIn(bl), lock.glyphs.animate.set_color(VENV), run_time=0.4)
            stick(self, lock, bl)
            vo.wait_until("of about 138")
            self.play(Indicate(substring(lock, "138445"), color=VENV, scale_factor=1.3), run_time=0.8)
            vo.wait_until("sits next to cli.py")
            self.play(Indicate(substring(cli, "cli.py"), color=INK, scale_factor=1.3),
                      Indicate(substring(lock, "uv.lock"), color=VENV, scale_factor=1.3), run_time=0.8)
            vo.wait_until("owned by user app")
            u_own = uline(lock, "app", TURN, stroke=4)
            pin(self, lock, u_own, run_time=0.4, anim=Create(u_own))
            self.play(Indicate(substring(lock, "app"), color=TURN, scale_factor=1.4), run_time=0.7)

        # ========================================================== 5 · echo $VIRTUAL_ENV (extra)
        with self.voiceover(SAY[5]) as vo:
            make_room(self, t, 2)
            c5 = type_cmd(self, t, VE_CMD, 0.7)
            pin(self, c5, beside(extra_tag(), t, c5), run_time=0.3)
            out5 = t.print(self, VE_OUT, run_time=0.4)
            venv_ln = out5[0]
            vo.wait_until("the venv variable says")
            u5 = uline(venv_ln, "/home/app/.venv", VENV, stroke=4)
            self.play(venv_ln.glyphs.animate.set_color(VENV), Create(u5), run_time=0.6)
            stick(self, venv_ln, u5)
            vo.wait_until("outside the window")
            out_tag = tag("outside the window", S.GREY)
            beside(out_tag, t, venv_ln, buff=0.4)
            pin(self, venv_ln, out_tag, run_time=0.5)
            self.play(Indicate(out_tag.text, color=INK, scale_factor=1.15), run_time=0.7)

        # ========================================================== 6 · two asides
        fc = ffmpeg_card()
        rc = root_card()
        place(fc, cx=0, top=2.78)
        place(rc, cx=0, top=2.78)              # one card at a time: the root card takes fc's place
        assert rc.get_bottom()[1] > STRIP_TOP + 0.3, (rc.get_bottom()[1], STRIP_TOP)
        assert rc.get_left()[0] > -6.6 and rc.get_right()[0] < 6.6, rc.width
        with self.voiceover(SAY[6]) as vo:
            self.play(caption_extra(tr, False), run_time=0.3)
            resize(self, t, 3, run_time=0.7)
            vo.wait_until("The package is")
            row5 = venv_ln
            row5.remove(out_tag)
            self.add(out_tag)
            full_f = fc.frame.copy()
            fc.frame.become(frame_to(full_f, fc.good, across=True))
            self.play(FadeIn(fc.frame), FadeIn(fc.good[0], shift=UP * 0.1), FadeOut(out_tag), run_time=0.5)
            self.play(Create(fc.good[1]), run_time=0.4)
            vo.wait_until("plain ffmpeg")
            self.play(Transform(fc.frame, frame_to(full_f, fc.bad, across=True)),
                      FadeIn(fc.bad[0], shift=UP * 0.1), run_time=0.4)
            self.play(Create(fc.bad[1]), run_time=0.4)
            self.play(Transform(fc.frame, full_f), FadeIn(fc.cap, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("And on a Linux laptop")
            # who it's for and, right under it, who it isn't (Mac and Windows: Docker Desktop),
            # so the scope stays up for the whole aside
            full = rc.frame.copy()
            rc.frame.become(frame_to(full, rc.desk))       # the card grows as its lines arrive
            self.play(FadeOut(fc, shift=UP * 0.3), run_time=0.4)
            self.play(FadeIn(rc.frame), FadeIn(rc.head, shift=UP * 0.1), FadeIn(rc.desk, shift=UP * 0.1),
                      run_time=0.6)
            vo.wait_until("isn't owned by")
            self.play(Indicate(rc.head[1], color=INK, scale_factor=1.08), run_time=0.8)
            vo.wait_until("uv add fails")
            self.play(Transform(rc.frame, frame_to(full, rc.err)),
                      LaggedStart(*[FadeIn(r) for r in rc.err], lag_ratio=0.3), run_time=0.7)
            self.play(Indicate(substring(rc.err[-1], "Permission denied"), color=ERR, scale_factor=1.15),
                      run_time=0.7)
            vo.wait_until("the chown command")
            self.play(Transform(rc.frame, full), FadeIn(rc.fix, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(rc.cmd[0], color=INK, scale_factor=1.12), run_time=0.7)
            # a Linux viewer has to read this: it holds after the line ends (~4 s up in all)
            self.wait(1.0)
            self.play(Indicate(rc.where, color=INK, scale_factor=1.04), run_time=0.8)
            self.wait(1.8)

        # ========================================================== 7 · the README: rebuild after exit
        chip_r = readme_chip("transcribe_audio/README.md · line 110", REBUILD, max_w=12.4)
        place(chip_r, cx=0, cy=1.0)
        s13 = tag("step 13", S.GREY)
        place(s13, right=chip_r.get_right()[0] - 0.2, top=chip_r.get_bottom()[1] - 0.18)
        u_reb = Line(chip_r.phrase.get_corner(DL) + DOWN * 0.07, chip_r.phrase.get_corner(DR) + DOWN * 0.07,
                     color=TURN, stroke_width=4)
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(rc), run_time=0.5)        # (fc went when rc came)
            self.play(FadeIn(chip_r, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("when you exit")
            self.play(chip_r.phrase.animate.set_color(TURN), Create(u_reb), run_time=0.6)
            vo.wait_until("We'll do that")
            self.play(FadeIn(s13, shift=UP * 0.1), run_time=0.4)
            self.play(Indicate(tr.dots[12], color=TURN, scale_factor=2.2),
                      Indicate(s13.text, color=INK, scale_factor=1.15),
                      run_time=0.9)

        # ========================================================== 8 · step 8: the group name (VS Code)
        before = src_panel("transcribe_audio/cli.py", 21, 21, cut_comments=True)
        ed = editor_inset(before)
        place(ed, left=-6.2, top=2.62)
        after = code_panel(AFTER_21, "transcribe_audio/cli.py", 21, "python")
        after.code.shift(before.code.background.get_left() - after.code.background.get_left())
        old_str = code_span(before.code, 0, '"pavlos"')
        new_str = code_span(after.code, 0, '"group-01"')
        old_tail = code_span(before.code, 0, "# …")
        new_tail = code_span(after.code, 0, "# …")
        yt8 = your_turn()
        place(yt8, left=ed.get_right()[0] + 0.35, cy=before.code.get_center()[1])
        note = label("the same name in all five cli.py", 22, S.GREY)
        boxes = stage_boxes()
        notes = VGroup(note, boxes).arrange(DOWN, buff=0.22)
        place(notes, left=ed.get_right()[0] + 0.35, top=ed.get_bottom()[1] + 0.25)
        if notes.get_right()[0] > EDGE:
            notes.shift(LEFT * (notes.get_right()[0] - EDGE))
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(chip_r), FadeOut(s13), FadeOut(u_reb), run_time=0.4)
            self.play(tr.goto(8), run_time=0.5)
            vo.wait_until("On your laptop")
            self.play(FadeIn(ed, shift=DOWN * 0.15), run_time=0.7)
            self.play(Indicate(ed.title, color=INK, scale_factor=1.1), run_time=0.7)
            vo.wait_until("and change line 21")
            self.play(Indicate(before.header, color=INK, scale_factor=1.08),
                      Indicate(old_str, color=TURN, scale_factor=1.15), run_time=0.9)
            vo.wait_until("ours is group-01")
            self.play(ReplacementTransform(old_str, new_str), Transform(old_tail, new_tail),
                      Transform(before.code.background, after.code.background), run_time=0.9)
            vo.wait_until("Pause and make")
            self.play(FadeIn(yt8, shift=LEFT * 0.1), run_time=0.4)
            self.play(Wiggle(yt8, scale_value=1.12, rotation_angle=0.02 * TAU), run_time=0.6)
            self.play(FadeIn(note, shift=UP * 0.1), LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.15),
                      run_time=0.8)

        # ========================================================== 9 · grep inside: the window both ways
        with self.voiceover(SAY[9]) as vo:
            self.play(caption_extra(tr), run_time=0.4)
            make_room(self, t, 2)
            c9 = type_cmd(self, t, GREP.cmd, 1.0)
            pin(self, c9, beside(extra_tag(), t, c9), run_time=0.3)
            out9 = t.print(self, GREP_OUT, run_time=0.4)
            g_ln = out9[0]
            g_term = substring(g_ln, GROUP)
            box9 = SurroundingRectangle(g_term, color=TURN, buff=0.04, stroke_width=2.5, corner_radius=0.05)
            self.play(g_term.animate.set_color(TURN), Create(box9), run_time=0.5)
            stick(self, g_ln, box9)
            vo.wait_until("the window works")
            a_start = new_str.get_bottom() + DOWN * 0.08
            a_end = np.array([g_term.get_center()[0], t.box.get_top()[1] + 0.04, 0])
            # one folder seen from two sides: a two-headed PINK link (nothing travels along it)
            link = DoubleArrow(a_start, a_end, buff=0, color=LOOKUP, stroke_width=4, tip_length=0.2,
                               max_tip_length_to_length_ratio=0.15)
            link_lab = VGroup(mono("-v", 22, LOOKUP), label("· the window", 22, LOOKUP)).arrange(RIGHT, buff=0.12)
            link_lab[1].align_to(link_lab[0], DOWN)
            place(link_lab, left=link.get_center()[0] + 0.3, cy=link.get_center()[1])
            self.play(FadeIn(link), FadeIn(link_lab, shift=LEFT * 0.1), run_time=0.6)
            self.play(Indicate(new_str, color=TURN, scale_factor=1.2), Indicate(g_term, color=TURN, scale_factor=1.2),
                      Indicate(link, color=LOOKUP, scale_factor=1.0), run_time=0.9)
            vo.wait_until("Use the same name")
            self.play(Indicate(note, color=INK, scale_factor=1.08), FadeOut(yt8), run_time=0.7)
            self.play(LaggedStart(*[b[0].animate(rate_func=there_and_back).set_fill(VENV, 0.5) for b in boxes],
                                  lag_ratio=0.2), run_time=1.0)
            vo.wait_until("or the stages")
            # who reads whose work (V1's DAG: A→B, B→C, B→D, D→E; C does not feed D)
            def hop(i, j):
                return Arrow(boxes[i].get_right(), boxes[j].get_left(), buff=0.04, color=S.GREY,
                             stroke_width=3, tip_length=0.12, max_tip_length_to_length_ratio=0.5)
            b_to_d = CurvedArrow(boxes[1][0].get_bottom() + DOWN * 0.04, boxes[3][0].get_bottom() + DOWN * 0.04,
                                 angle=0.6 * PI, color=S.GREY, stroke_width=3, tip_length=0.12)
            hops = VGroup(hop(0, 1), hop(1, 2), b_to_d, hop(3, 4))
            self.play(LaggedStart(*[Create(h) for h in hops], lag_ratio=0.25), run_time=1.0)

        # ========================================================== 10 · step 9: --help matches the README
        with self.voiceover(SAY[10]) as vo:
            # goto(9) rebuilds the caption, so it also drops " · extra"
            self.play(FadeOut(VGroup(ed, new_str, note, boxes, hops, link, link_lab)), tr.goto(9), run_time=0.5)
            t.clear(self, run_time=0.3)
            resize(self, t, BIG, run_time=0.6)
            vo.wait_until("python cli.py dash dash help")
            c10 = type_cmd(self, t, HELP.cmd, 0.9)
            out10 = t.print(self, HELP_OUT, run_time=0.6, lag=0.1)
            ov = readme_overlay(t)
            vo.wait_until("This time it works")
            self.play(Indicate(VGroup(*[ln.glyphs for ln in out10 if len(ln.glyphs)]), color=INK,
                               scale_factor=1.03), run_time=0.8)
            vo.wait_until("and it matches")
            self.play(FadeIn(ov, shift=DOWN * 0.45 + LEFT * 0.9), run_time=1.0)
            marks = VGroup()
            x_m = ov.panel.get_right()[0] + 0.32
            for k, s in enumerate(README_BLOCK):
                if s.strip():
                    row = c10 if k == 0 else out10[k - 1]
                    marks.add(check_mark(0.26, VENV).move_to([x_m, row.strut.get_center()[1], 0]))
            self.play(LaggedStart(*[Create(m) for m in marks], lag_ratio=0.25), run_time=1.4)
            vo.wait_until("Pause, and get")
            # the overlay has done its job: it lifts off (checks and header stay), so the paused
            # frame shows the real output and the tag beside the command overlaps nothing
            self.play(FadeOut(VGroup(ov.panel, ov.rows), shift=UP * 0.15), run_time=0.5)
            self.remove(ov.panel, ov.rows)       # gone for good (FadeOut restores opacity on clean-up)
            yt10 = beside(your_turn(), t, c10)
            self.play(FadeIn(yt10, shift=LEFT * 0.1), run_time=0.4)
            self.play(Wiggle(yt10, scale_value=1.12, rotation_angle=0.02 * TAU), run_time=0.6)
        self.wait(0.8)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

