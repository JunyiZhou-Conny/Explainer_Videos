"""S04 · The key, and uv init (README › transcribe_audio steps 2-3: the Canvas key into the five
secrets/ folders, uv if you don't have it, uv init --bare, and the first half of V7).

Beats (script.md "## S04", one voiceover block each):
 0  TRACKER A1 -> A2. Schematic (illustration): a GREY card "course site · Files" (text only, no
    logo: two text-free placeholder rows and the GOLD key glyph `mega-pipeline.json`). On "It lets
    your code act" the key leaves the card, enlarges centre-right and gets a GOLD glow; GREY label
    under it: "the course's service account", then (on "so guard it") "spends the course's money".
 1  The glow and labels go; the key shrinks back into the card. Right: the five GREY folders
    `<component>/secrets/` of the clone; bottom-left: the GREY README card "README.md · lines
    97–99" (the README's own words). On "download it" an arrow carries a copy of the key onto
    `transcribe_audio/secrets/`; on "with a copy in each" the card's "each component folder" line
    gets a YELLOW underline and four copies drop onto the other four folders. Then ▶ your turn
    beside `transcribe_audio/secrets/` and the GREY caption "check: ls secrets → mega-pipeline.json".
 2  The rest fades; the caption's `mega-pipeline.json` enlarges to the centre (GREEN check), caption
    "exact name"; on "If your browser" `mega-pipeline (1).json` appears under it (RED cross, struck
    through RED); on "rename it" a GREY "rename" arc points from the bad name to the good one.
 3  Two GREY link cards side by side: left `README.md · line 99` (link `mega-pipeline.json` ->
    Canvas file 25687801), right `transcribe_audio/README.md · line 17` (the same link text ->
    Canvas file 23163432), GREY `erratum` above the right one. On "older Canvas file" the right
    number flashes; on "so use the main" the left card gets a GREEN check "use this one" and the
    right one a GREY "older" stamp. GREY note "how the code finds the key: part 2".
 4  TRACKER A3. The house terminal (12 rows, laptop, transcribe_audio prompt). The README chip
    `transcribe_audio/README.md · lines 26–34` "Don't have uv installed?" sits right-aligned
    between the terminal and the top band (9.7 wide: it can't sit right of the tracker).
    TRACKER A3 · extra. `uv --version` (extra) -> 06-uv-missing.txt line 2 in RED, "command not
    found" underlined RED. On "so skip ahead to uv init" the tracker caption pulses.
 5  TRACKER A3 (extra off). The chip flashes YELLOW ("the README's installer"). `curl -LsSf
    https://astral.sh/uv/install.sh | sh` (folds onto two rows; GREY tag "macOS / Linux") ->
    07-uv-install.txt lines 2-6, …, 8, 10 (no ▶: only for viewers without uv). Line 2 gets
    "at the time of recording"; a PURPLE `uv` chip lifts off line 4 and drops into the GREY folder
    `~/.local/bin` drawn right of lines 4-5. On "On Windows" the terminal shrinks to the strip (the
    curl command and line 8); above it two GREY command chips (shown, not typed): the PowerShell
    line (two rows: 79 characters don't fit one row at 20 pt; note "Windows (PowerShell) · one
    line") and, on "on any system", `pip install uv` "any system".
 6  Line 8's "either restart your shell" gets a YELLOW bar. On "as the installer says" the chips
    go, the terminal clears and grows back to 12 rows (GREY "new terminal" in its title bar,
    prompt student@laptop:~$). TRACKER A3 · extra: `cd mega-pipeline/transcribe_audio` (extra) ->
    no output, the transcribe_audio prompt; `uv --version` -> 08-uv-version.txt line 2.
 7  TRACKER A3 (extra off; chip and "new terminal" go). `uv init --bare` -> 09-uv-init.txt
    line 2; on "pyproject.toml" a GREEN file glyph `pyproject.toml` appears above the terminal;
    `transcribe-audio` underlined GREEN; ▶ your turn on "Pause and run it".
 8  TRACKER A3 · extra. `cat pyproject.toml` (extra; folds after `cat`) -> 10-cat-pyproject.txt
    lines 2-6. "name" and "version" pulse as named; GREY tag "none yet" beside `dependencies = []`;
    YELLOW bar on `requires-python = ">=3.11"` and its 3.11 pulses.
 9  The terminal shrinks to the strip (the cat command and the requires-python line). V7 above
    it: the axis 3.10 … 3.16; a GREY dot "laptop · 3.11.2" drops onto 3.11; the GREEN interval
    grows from 3.11 while the strip's `requires-python = ">=3.11"` flies up to become its label.
    ORANGE dot "image · Python 3.12" lands inside; PURPLE `uv sync` chip + "in range?" (the dot
    pulses PURPLE), then a GREEN check.
10  GREY caption "your number depends on your laptop" + tag "illustration · another laptop"; the
    GREY dot slides to 3.13 ("another laptop · 3.13"); the interval's start follows; the image's
    dot turns RED, the check becomes a RED cross, a dashed PURPLE arrow drops onto 3.15 ("preview:
    generate_text"). A GREEN edit chip `requires-python = ">=3.12"` covers the label and drags the
    start back to 3.12: the dot is ORANGE again, the check returns, the arrow goes. GREY tag "not in
    the README" beside the chip; the preview caption pulses on "generate text shows why". Fade out.
"""

import numpy as np
from manim import *

from explainer import style as S
from explainer.devops import (MONO, box, check_mark, chip, cross_mark, file_glyph, folder_glyph,
                              label, mono, substring, tag)
from explainer.scene import VoiceScene

from common import (CAPTION, COMPONENTS, COST, ERR, INK, LAPTOP, NARRATION, P_A, P_HOME, SYSTEM,
                    TOOL, TURN, VENV, VersionLine, beside, bare_prompt, capture, caption_extra,
                    cmd_chip, erratum_tag, extra_tag, illustration_tag, key_glyph, readme_card,
                    readme_chip, recorded_tag, resize, sans, source_text, stamp, strike, term,
                    tracker, type_cmd, under, your_turn)

SAY = NARRATION["S04"]

# ------------------------------------------------------------------ commands and captures
MISSING = capture("06-uv-missing")
assert MISSING.cmd == "uv --version", MISSING.cmd
MISSING_OUT = MISSING.at(2)                                  # bash: line 1: uv: command not found
INSTALL = capture("07-uv-install")
assert INSTALL.cmd == "curl -LsSf https://astral.sh/uv/install.sh | sh", INSTALL.cmd
INSTALL_OUT = INSTALL.at((2, 6), "…", 8, 10)
assert "uv 0.13.0" in INSTALL.line(2) and INSTALL.line(3).endswith("/.local/bin")
assert INSTALL.line(4).strip() == "uv" and "either restart your shell" in INSTALL.line(8)
VERSION = capture("08-uv-version")
assert VERSION.cmd == "uv --version"
VERSION_OUT = VERSION.at(2)                                  # uv 0.13.0 (x86_64-unknown-linux-gnu)
INIT = capture("09-uv-init")
assert INIT.cmd == "uv init --bare"
INIT_OUT = INIT.at(2)                                        # Initialized project `transcribe-audio`
CAT = capture("10-cat-pyproject")
assert CAT.cmd == "cat pyproject.toml"
CAT_OUT = CAT.at((2, 6))
assert CAT.line(5) == 'requires-python = ">=3.11"' and CAT.line(6) == "dependencies = []"
assert capture("00-laptop").line(6) == "Python 3.11.2"     # the GREY dot of beat 9
CD_BACK = "cd mega-pipeline/transcribe_audio"                # extra (script.md S04)

# the README's own words (assets/source, pinned commit)
_MAIN = source_text("README.md").split("\n")
_A = source_text("transcribe_audio/README.md").split("\n")
RC_LINES = ["… download it from the link below and place it inside",
            "each component folder <app_folder>/secrets/ you build:"]
assert ("download it from the link below and place it inside each component folder "
        "`<app_folder>/secrets/` you build:") in _MAIN[96]           # README.md:97
assert "files/25687801/" in _MAIN[98] and "files/23163432/" in _A[16]  # README.md:99, A:17
assert "Don't have `uv` installed?" in _A[25]                         # A:26
PS_ROWS = ["powershell -ExecutionPolicy ByPass -c", '"irm https://astral.sh/uv/install.ps1 | iex"']
assert _A[31] == "> " + " ".join(PS_ROWS)                            # A:32
PIP = "pip install uv"
assert f"`{PIP}`" in _A[33]                                           # A:34
assert "`uv init --bare`" in _A[33] and "restart your terminal" in _A[33]

# ------------------------------------------------------------------ layout
TRACK_BOTTOM = 2.917               # the tracker band's lower edge
CARD_C = np.array([-4.25, 0.9, 0])  # the course-site card (beats 0-1)
BIG_C = np.array([2.6, 1.1, 0])     # the enlarged key (beat 0)
ROWS_X = -0.8                      # left edge of the five secrets/ folders (beat 1)
ROW_Y = [1.8, 0.65, 0.05, -0.55, -1.15]
AXIS_Y = 0.3                       # V7's axis (beats 9-10), above the 3-row strip


# ------------------------------------------------------------------ small helpers
def place(m, left=None, top=None, right=None, cy=None, cx=None):
    if left is not None:
        m.shift(RIGHT * (left - m.get_left()[0]))
    if right is not None:
        m.shift(RIGHT * (right - m.get_right()[0]))
    if top is not None:
        m.shift(UP * (top - m.get_top()[1]))
    if cy is not None:
        m.set_y(cy)
    if cx is not None:
        m.set_x(cx)
    return m


def stick(scene, line, *mobs):
    """Make mobs (already on screen) part of terminal row `line` (its last row when folded), so
    they scroll and fade with it."""
    row = line.rows[-1] if hasattr(line, "rows") else line
    for m in mobs:
        scene.remove(m)
        row.add(m)
    scene.add(row)


def under_row(mob, t, line):
    """Position a tag for a command row that is too long to have one beside it: at the right end
    of the row below (whose output is short), as the pilot does. Returns mob (not added)."""
    row = line.rows[-1] if hasattr(line, "rows") else line
    mob.set_y(row.strut.get_center()[1] - t.pitch)
    return mob.align_to(t.box, RIGHT).shift(LEFT * 0.12)


def rows_of(line) -> list:
    """The row mobjects of a typed line (one, or several when it folded)."""
    return list(line.rows) if hasattr(line, "rows") else [line]


def unstick(scene, line, mob):
    row = line.rows[-1] if hasattr(line, "rows") else line
    if mob in row.submobjects:
        row.remove(mob)
    scene.add(mob)
    return mob


def row_bar(line, sub, color=TURN, opacity=0.28) -> Rectangle:
    """A bar over substring `sub` of a terminal row, as tall as the row's strut."""
    g = substring(line, sub)
    return Rectangle(width=g.width + 0.12, height=line.strut.height * 0.92, stroke_width=0) \
        .set_fill(color, opacity).move_to([g.get_center()[0], line.strut.get_center()[1], 0])


def placeholder(w: float) -> VGroup:
    """A text-free file row of the schematic course site (a file glyph and a GREY bar)."""
    g = file_glyph(0.28, S.GREY_DARK)
    b = RoundedRectangle(width=w, height=0.12, corner_radius=0.06, stroke_width=0) \
        .set_fill(LAPTOP, 0.35).next_to(g, RIGHT, buff=0.18)
    return VGroup(g, b)


def site_card():
    """The schematic course site: frame, title, separator, two placeholders (one VGroup), and
    the key row (separate: it leaves the card in beat 0)."""
    w, h = 4.3, 2.2
    fr = box(w, h, LAPTOP, fill=S.GREY_DARKER, fill_opacity=1).move_to(CARD_C)
    title = sans("course site · Files", 22, LAPTOP)
    place(title, left=fr.get_left()[0] + 0.28, cy=fr.get_top()[1] - 0.32)
    sep_y = fr.get_top()[1] - 0.62
    sep = Line([fr.get_left()[0], sep_y, 0], [fr.get_right()[0], sep_y, 0], color=S.GREY_DARK,
               stroke_width=2)
    p1, p2 = placeholder(2.4), placeholder(1.9)
    keyrow = key_glyph(name="mega-pipeline.json")
    x0 = fr.get_left()[0] + 0.3
    for m, y in ((p1, sep_y - 0.38), (keyrow, sep_y - 0.92), (p2, sep_y - 1.46)):
        place(m, left=x0, cy=y)
    frame = VGroup(fr, title, sep, p1, p2)
    return frame, keyrow


def halo(center, radii=(0.42, 0.62, 0.82), ops=(0.2, 0.11, 0.05)) -> VGroup:
    """A soft GOLD glow: concentric translucent discs."""
    return VGroup(*[Circle(radius=r, stroke_width=0).set_fill(COST, o).move_to(center)
                    for r, o in zip(radii, ops)])


def secrets_rows() -> VGroup:
    """The clone's five secrets/ folders (GREY glyph + mono name), one row each. .glyph .text"""
    rows = VGroup()
    for c, y in zip(COMPONENTS, ROW_Y):
        g = folder_glyph(0.4, LAPTOP)
        t = mono(f"{c}/secrets/", CAPTION, INK).next_to(g, RIGHT, buff=0.2)
        r = VGroup(g, t)
        r.glyph, r.text = g, t
        place(r, left=ROWS_X)
        r.shift(UP * (y - g.get_center()[1]))
        rows.add(r)
    return rows


def link_card(path: str, line_no: int, number: str, width: float = 5.9) -> VGroup:
    """A README link as a card: the link text (a key and `mega-pipeline.json`, underlined) and
    the Canvas file it points to; header `path · line N` above. .frame .number .head"""
    k = key_glyph(0.26)
    link = mono("mega-pipeline.json", 22, INK)
    ul = Line(link.get_corner(DL) + DOWN * 0.07, link.get_corner(DR) + DOWN * 0.07, color=INK,
              stroke_width=1.5)
    r1 = VGroup(k, VGroup(link, ul)).arrange(RIGHT, buff=0.2)
    num = mono(number, 22, INK)
    r2 = VGroup(sans("→ Canvas file", 22, LAPTOP), num).arrange(RIGHT, buff=0.18)
    body = VGroup(r1, r2).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    fr = box(width, body.height + 0.6, LAPTOP, fill=S.BG, fill_opacity=0.92)
    body.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.35)
    head = VGroup(mono(path, CAPTION, LAPTOP), label(f"· line {line_no}", CAPTION, LAPTOP))
    head.arrange(RIGHT, buff=0.12).next_to(fr, UP, buff=0.1).align_to(fr, LEFT).shift(RIGHT * 0.1)
    g = VGroup(fr, body, head)
    g.frame, g.number, g.head = fr, num, head
    return g


def ps_chip() -> VGroup:
    """The README's PowerShell line as a GREY command chip on two rows (79 characters don't fit
    one row at 20 pt), with its note. .chip .note"""
    rows = VGroup(*[mono(s, CAPTION, INK) for s in PS_ROWS]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    rows[1].shift(RIGHT * 0.4)
    fr = box(rows.width + 0.5, rows.height + 0.32, LAPTOP, fill_opacity=0.16, radius=0.14)
    fr.move_to(rows)
    c = VGroup(fr, rows)
    note = label("Windows (PowerShell) · one line", CAPTION, LAPTOP).next_to(c, DOWN, buff=0.1)
    note.align_to(c, LEFT)
    g = VGroup(c, note)
    g.chip, g.note = c, note
    return g


def lo_label(vl, lo: int):
    """V7's interval label `requires-python = ">=3.lo"`, always over the interval's start (the
    shared VersionLine puts it left of the start when it fits; beat 10 needs the room there for
    the edit chip's drag, so the label stays over the start like it is for 3.11 and 3.12)."""
    return mono(f'requires-python = ">=3.{lo}"', vl.size, VENV).move_to(vl.point(lo, 1.05),
                                                                         aligned_edge=LEFT)


def down_arrow(top, tip, color=TOOL) -> VGroup:
    """A dashed arrow from `top` down to `tip`."""
    head = Triangle(stroke_width=0).set_fill(color, 1).rotate(PI).scale(0.11)
    head.move_to(tip, aligned_edge=DOWN)
    shaft = DashedLine(top, head.get_top(), dash_length=0.08, color=color, stroke_width=4)
    return VGroup(shaft, head)


class KeyAndInit(VoiceScene):
    def construct(self):
        assert len(SAY) == 11, f"S04 has {len(SAY)} SAY lines; this scene animates 11"

        tr = tracker("A", 1)

        # ========================================================== 0 · the key
        card, keyrow = site_card()
        ill0 = illustration_tag()
        place(ill0, left=card[0].get_left()[0], top=card[0].get_bottom()[1] - 0.18)
        slot = keyrow.get_center()
        lab1 = sans("the course's service account", 22, LAPTOP)
        lab2 = sans("spends the course's money", 22, LAPTOP)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.1), FadeIn(card), FadeIn(ill0), run_time=0.6)
            self.play(tr.goto(2), run_time=0.5)
            vo.wait_until("a file from Canvas")
            self.play(FadeIn(keyrow, shift=RIGHT * 0.2), run_time=0.5)
            vo.wait_until("called mega-pipeline")
            self.play(Indicate(keyrow.name, color=COST, scale_factor=1.12), run_time=0.7)
            vo.wait_until("It lets your code")
            self.play(keyrow.animate.scale(1.8).move_to(BIG_C), run_time=1.0)
            glow = halo(keyrow.key.get_center())
            self.add(glow)
            self.bring_to_back(glow)
            self.play(FadeIn(glow, scale=0.5), run_time=0.6)
            labs = VGroup(lab1, lab2).arrange(DOWN, buff=0.16).next_to(keyrow, DOWN, buff=0.5)
            vo.wait_until("the course's service account")
            self.play(FadeIn(lab1, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("a robot Google account")
            self.play(Indicate(lab1, color=INK, scale_factor=1.06), run_time=0.7)
            vo.wait_until("so guard it")
            self.play(FadeIn(lab2, shift=UP * 0.1), glow.animate.scale(1.2), run_time=0.6)
            self.play(glow.animate.scale(1 / 1.2), run_time=0.6)

        # ========================================================== 1 · into the five secrets/
        rows = secrets_rows()
        targets = [r.glyph.get_center() + DOWN * 0.03 for r in rows]
        rc = readme_card("README.md · lines 97–99", RC_LINES)
        place(rc, left=-6.35, top=-1.8)
        rc_ul = under(rc.rows[1], TURN, stroke=3)
        cap = VGroup(sans("check:", CAPTION, LAPTOP), mono("ls secrets", CAPTION, INK),
                     sans("→", CAPTION, LAPTOP), mono("mega-pipeline.json", CAPTION, COST))
        cap.arrange(RIGHT, buff=0.15)
        place(cap, left=rows[0].text.get_left()[0], top=rows[0].get_bottom()[1] - 0.16)
        yt1 = your_turn().next_to(rows[0].text, RIGHT, buff=0.3)

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(glow), FadeOut(labs), keyrow.animate.scale(1 / 1.8).move_to(slot),
                      run_time=0.7)
            self.play(FadeIn(rows, shift=LEFT * 0.15), FadeIn(rc, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("download it")
            k0 = keyrow.key.copy()
            arr = Arrow(card[0].get_right() + np.array([0.05, -0.1, 0]),
                        rows[0].glyph.get_left() + np.array([-0.08, -0.08, 0]), buff=0,
                        stroke_width=4, color=COST, max_tip_length_to_length_ratio=0.2)
            self.play(GrowArrow(arr), run_time=0.4)
            self.play(k0.animate.scale(0.75).move_to(targets[0]), run_time=0.7)
            vo.wait_until("and put it")
            self.play(FadeOut(arr), Indicate(rows[0].text, color=INK, scale_factor=1.08), run_time=0.6)
            vo.wait_until("with a copy")
            copies = [k0.copy() for _ in range(4)]
            self.play(Create(rc_ul), run_time=0.4)
            self.play(LaggedStart(*[c.animate.move_to(p) for c, p in zip(copies, targets[1:])],
                                  lag_ratio=0.25), run_time=1.3)
            self.play(FadeIn(yt1, shift=LEFT * 0.1), FadeIn(cap, shift=UP * 0.1), run_time=0.5)
            self.play(Wiggle(yt1, scale_value=1.15, rotation_angle=0.025 * TAU), run_time=0.7)

        # ========================================================== 2 · the exact name
        good = mono("mega-pipeline.json", 40, COST)
        bad = mono("mega-pipeline (1).json", 40, COST)
        good.move_to([0.0, 1.0, 0])
        bad.next_to(good, DOWN, buff=0.75).align_to(good, LEFT)
        names = VGroup(good, bad)
        names.set_x(0.0)
        chk2 = check_mark(0.5, VENV).next_to(good, LEFT, buff=0.45)
        crs2 = cross_mark(0.42, ERR).next_to(bad, LEFT, buff=0.45).match_x(chk2)
        st2 = strike(bad, ERR, stroke=5)
        exact = sans("exact name", 24, LAPTOP).next_to(good, UP, buff=0.5).align_to(good, LEFT)
        ren = ArcBetweenPoints(bad.get_right() + np.array([0.25, 0.05, 0]),
                               good.get_right() + np.array([0.25, -0.05, 0]), angle=PI * 0.55)
        ren.set_stroke(LAPTOP, 3)
        ren.add_tip(tip_length=0.18)
        ren_l = sans("rename", 22, LAPTOP).next_to(ren, RIGHT, buff=0.15)
        beat1 = VGroup(card, keyrow, ill0, rows, k0, *copies, rc, rc_ul, yt1, *cap[:3])

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(beat1), run_time=0.5)
            self.play(Transform(cap[3], good), run_time=0.8)
            self.play(Create(chk2), FadeIn(exact, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("If your browser")
            self.play(FadeIn(bad, shift=UP * 0.15), run_time=0.5)
            self.play(Create(crs2), Create(st2), run_time=0.5)
            vo.wait_until("rename it")
            self.play(Create(ren), FadeIn(ren_l), run_time=0.6)
            self.play(Indicate(cap[3], color=COST, scale_factor=1.08), run_time=0.6)

        # ========================================================== 3 · two Canvas links (erratum)
        left = link_card("README.md", 99, "25687801")
        right = link_card("transcribe_audio/README.md", 17, "23163432")
        pair = VGroup(left, right).arrange(RIGHT, buff=0.5).move_to([0, 0.35, 0])
        err3 = erratum_tag().next_to(right.head, UP, buff=0.25).align_to(right.frame, RIGHT)
        use = VGroup(check_mark(0.34, VENV), sans("use this one", 24, VENV)).arrange(RIGHT, buff=0.18)
        use.next_to(left.frame, DOWN, buff=0.35)
        older = stamp("older", LAPTOP, size=24).next_to(right.frame, DOWN, buff=0.35)
        note3 = sans("how the code finds the key: part 2", 22, LAPTOP).move_to([0, -2.2, 0])

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(cap[3], bad, chk2, crs2, st2, exact, ren, ren_l)), run_time=0.4)
            self.play(FadeIn(left, shift=UP * 0.15), FadeIn(right, shift=UP * 0.15), run_time=0.6)
            self.play(FadeIn(err3, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("the component READMEs")
            self.play(Indicate(right.head, color=INK, scale_factor=1.05), run_time=0.6)
            self.play(Indicate(right.number, color=INK, scale_factor=1.2), run_time=0.6)
            vo.wait_until("so use the main")
            self.play(Create(use[0]), FadeIn(use[1], shift=UP * 0.1),
                      left.frame.animate.set_stroke(VENV, 3), run_time=0.5)
            self.play(FadeIn(older, scale=1.3), run_time=0.4)
            self.play(FadeIn(note3, shift=UP * 0.1), run_time=0.5)

        # ========================================================== 4 · uv? (not on this laptop)
        t = term(P_A, 12)
        chip_r = readme_chip("transcribe_audio/README.md · lines 26–34", "Don't have uv installed?",
                             max_w=9.8)
        place(chip_r, right=6.45, cy=(t.box.get_top()[1] + TRACK_BOTTOM) / 2)

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(left, right, err3, use, older, note3)), run_time=0.4)
            self.play(tr.goto(3), FadeIn(t), run_time=0.6)
            self.play(FadeIn(chip_r, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("After Tutorial 0")
            self.play(caption_extra(tr), run_time=0.3)
            c0 = type_cmd(self, t, MISSING.cmd, 0.6)
            x0 = under_row(extra_tag(), t, c0)
            self.play(FadeIn(x0, shift=LEFT * 0.1), run_time=0.3)
            stick(self, c0, x0)
            vo.wait_until("so skip ahead")
            self.play(Indicate(tr.caption, color=TURN, scale_factor=1.12), run_time=0.8)
            vo.wait_until("This recording laptop")
            o0 = t.print(self, [(MISSING_OUT[0], ERR)], run_time=0.4)[0]
            vo.wait_until("command not found")
            u0 = under(substring(o0, "command not found"), ERR, stroke=3)
            self.play(Create(u0), run_time=0.4)
            stick(self, o0, u0)

        # ========================================================== 5 · the README's installer
        with self.voiceover(SAY[5]) as vo:
            self.play(caption_extra(tr, False), run_time=0.3)
            vo.wait_until("use the README's installer")
            self.play(chip_r.frame.animate.set_stroke(TURN, 3),
                      Indicate(chip_r.phrase, color=TURN, scale_factor=1.08), run_time=0.7)
            vo.wait_until("on macOS or Linux")
            c1 = type_cmd(self, t, INSTALL.cmd, 1.4)
            os1 = tag("macOS / Linux", LAPTOP)
            beside(os1, t, c1)
            self.play(FadeIn(os1, shift=LEFT * 0.1), chip_r.frame.animate.set_stroke(LAPTOP, 2.5),
                      run_time=0.4)
            stick(self, c1, os1)
            out1 = t.print(self, INSTALL_OUT, run_time=0.8)
            l2, l4, l8 = out1[0], out1[2], out1[-2]
            vo.wait_until("which installed")
            rt = beside(recorded_tag(), t, l2)
            self.play(FadeIn(rt, shift=LEFT * 0.1), Indicate(substring(l2, "uv 0.13.0"), color=INK,
                                                            scale_factor=1.12), run_time=0.6)
            stick(self, l2, rt)
            fg = folder_glyph(0.72, LAPTOP)
            fl = mono("~/.local/bin", CAPTION, INK).next_to(fg, RIGHT, buff=0.18)
            fold = VGroup(fg, fl)
            place(fold, right=t.box.get_right()[0] - 0.5,
                  cy=(l4.strut.get_center()[1] + out1[3].strut.get_center()[1]) / 2)
            uvc = chip("uv", TOOL, size=CAPTION, font=MONO).move_to(substring(l4, "uv"))
            self.play(FadeIn(fold, shift=LEFT * 0.1), FadeIn(uvc, scale=1.3), run_time=0.5)
            self.play(uvc.animate.move_to(fg[1].get_center()), run_time=0.9)
            stick(self, l4, fold, uvc)

            vo.wait_until("On Windows")
            ps = ps_chip()
            pip = cmd_chip(PIP, "any system")
            place(ps, left=-4.1, cy=1.25)
            place(pip, left=-4.1, top=ps.get_bottom()[1] - 0.45)
            resize(self, t, 3, keep=[*rows_of(c1), l8], run_time=0.9)
            self.play(FadeIn(ps, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("on any system")
            self.play(FadeIn(pip, shift=UP * 0.15), run_time=0.5)

        # ========================================================== 6 · new terminal, uv answers
        with self.voiceover(SAY[6]) as vo:
            b8 = row_bar(l8, "either restart your shell")
            self.play(FadeIn(b8), run_time=0.4)
            stick(self, l8, b8)
            self.play(Indicate(substring(l8, "restart your shell"), color=TURN, scale_factor=1.08),
                      run_time=0.6)
            vo.wait_until("as the installer says")
            t.clear(self, run_time=0.3)
            resize(self, t, 12, run_time=0.8, extra=[FadeOut(ps), FadeOut(pip)])
            newterm = label("new terminal", CAPTION, LAPTOP)
            place(newterm, right=t.box.get_right()[0] - 0.3, cy=t.title.get_center()[1])
            t.set_prompt(P_HOME)
            bare_prompt(self, t)
            self.play(FadeIn(newterm), run_time=0.3)
            vo.wait_until("cd back")
            self.play(caption_extra(tr), run_time=0.25)
            c2 = type_cmd(self, t, CD_BACK, 0.9)
            x2 = beside(extra_tag(), t, c2)
            self.play(FadeIn(x2, shift=LEFT * 0.1), run_time=0.3)
            stick(self, c2, x2)
            t.set_prompt(P_A)
            bare_prompt(self, t)
            vo.wait_until("and uv answers")
            type_cmd(self, t, VERSION.cmd, 0.5)
            o2 = t.print(self, VERSION_OUT, run_time=0.4)[0]
            self.play(Indicate(substring(o2, "uv 0.13.0"), color=INK, scale_factor=1.12), run_time=0.6)

        # ========================================================== 7 · uv init --bare
        pyfile = VGroup(file_glyph(0.4, VENV), mono("pyproject.toml", 22, VENV)).arrange(RIGHT, buff=0.15)
        place(pyfile, right=6.3, cy=(t.box.get_top()[1] + TRACK_BOTTOM) / 2)

        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(chip_r), FadeOut(newterm), caption_extra(tr, False), run_time=0.4)
            vo.wait_until("uv init dash")
            c3 = type_cmd(self, t, INIT.cmd, 0.7)
            vo.wait_until("It writes just")
            o3 = t.print(self, INIT_OUT, run_time=0.4)[0]
            vo.wait_until("pyproject.toml")
            self.play(FadeIn(pyfile, shift=UP * 0.25), run_time=0.6)
            vo.wait_until("for a project named")
            u3 = under(substring(o3, "transcribe-audio"), VENV, stroke=3)
            self.play(Create(u3), substring(o3, "transcribe-audio").animate.set_color(VENV), run_time=0.5)
            stick(self, o3, u3)
            vo.wait_until("Pause and run it")
            yt3 = under_row(your_turn(), t, c3)
            self.play(FadeIn(yt3, shift=LEFT * 0.1), run_time=0.4)
            stick(self, c3, yt3)
            self.play(Wiggle(yt3, scale_value=1.15, rotation_angle=0.025 * TAU), run_time=0.7)

        # ========================================================== 8 · cat pyproject.toml
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(unstick(self, c3, yt3)), caption_extra(tr), run_time=0.3)
            c4 = type_cmd(self, t, CAT.cmd, 0.7)
            out4 = t.print(self, CAT_OUT, run_time=0.5)
            l_name, l_ver, l5, l6 = out4[1], out4[2], out4[3], out4[4]
            x4 = beside(extra_tag(), t, c4)
            self.play(FadeIn(x4, shift=LEFT * 0.1), Indicate(pyfile, color=VENV, scale_factor=1.08),
                      run_time=0.4)
            stick(self, c4, x4)
            vo.wait_until("a name")
            self.play(Indicate(substring(l_name, "name"), color=INK, scale_factor=1.25), run_time=0.5)
            vo.wait_until("a version")
            self.play(Indicate(substring(l_ver, "version"), color=INK, scale_factor=1.25), run_time=0.5)
            vo.wait_until("an empty list")
            ny = beside(tag("none yet", LAPTOP), t, l6)
            self.play(FadeIn(ny, shift=LEFT * 0.1), run_time=0.4)
            stick(self, l6, ny)
            vo.wait_until("and the minimum")
            b5 = row_bar(l5, l5.text)
            self.play(FadeIn(b5), run_time=0.4)
            stick(self, l5, b5)
            self.play(Indicate(substring(l5, "3.11"), color=TURN, scale_factor=1.3), run_time=0.7)

        # ========================================================== 9 · V7: the interval
        vl = VersionLine(10, 16, lo=11)
        vl.shift(UP * (AXIS_Y - vl.axis.get_center()[1]))
        d1 = vl.dot(11.1, "laptop · 3.11.2", LAPTOP)
        d2 = vl.dot(12.15, "image · Python 3.12", SYSTEM, above=False)
        uvs = chip("uv sync", TOOL, size=22, font=MONO)
        q = sans("in range?", 22, LAPTOP)
        ask = VGroup(uvs, q).arrange(RIGHT, buff=0.22)
        place(ask, left=d2.text.get_right()[0] + 0.6, cy=d2.text.get_center()[1])
        ck = check_mark(0.36, VENV).next_to(q, RIGHT, buff=0.3)

        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(pyfile), run_time=0.3)
            resize(self, t, 3, keep=[*rows_of(c4), l5], run_time=0.8)
            self.play(FadeIn(vl.axis), FadeIn(vl.ticks), run_time=0.6)
            self.play(Indicate(substring(l5, "3.11"), color=TURN, scale_factor=1.3), run_time=0.6)
            vo.wait_until("this laptop's Python")
            self.play(FadeIn(d1, shift=DOWN * 0.4), run_time=0.6)
            self.play(GrowFromEdge(vl.band, LEFT), TransformFromCopy(l5.glyphs, vl.band_label),
                      run_time=1.0)
            self.bring_to_back(vl.band)
            vo.wait_until("In the image")
            self.play(FadeIn(d2, shift=DOWN * 0.4), run_time=0.6)
            vo.wait_until("uv sync needs")
            self.play(FadeIn(ask, shift=LEFT * 0.15), run_time=0.5)
            self.play(Indicate(d2.dot, color=TOOL, scale_factor=1.8), run_time=0.7)
            vo.wait_until("and 3.12 is in it")
            self.play(Create(ck), run_time=0.4)
            vo.wait_until("so all is well")
            self.play(Indicate(ck, color=VENV, scale_factor=1.3), run_time=0.6)

        # ========================================================== 10 · another laptop
        cap10 = sans("your number depends on your laptop", 22, LAPTOP)
        ill10 = illustration_tag("another laptop")
        top10 = VGroup(cap10, ill10).arrange(RIGHT, buff=0.35)
        place(top10, right=6.4, cy=2.4)
        lab13 = mono("another laptop · 3.13", 22, LAPTOP).next_to(vl.point(13), UP, buff=0.41)
        crs = cross_mark(0.3, ERR).move_to(ck)
        ck_back = check_mark(0.36, VENV).move_to(ck)
        tip = vl.point(15, 0.05)
        dl = down_arrow(vl.point(15, 0.7), tip)
        prev = VGroup(sans("preview:", CAPTION, LAPTOP), mono("generate_text", CAPTION, LAPTOP))
        prev.arrange(RIGHT, buff=0.12)
        place(prev, left=dl.get_right()[0] + 0.15, cy=vl.point(15, 0.55)[1])
        edit = chip('requires-python = ">=3.12"', VENV, size=22, font=MONO)
        edit.box.set_fill(interpolate_color(ManimColor(S.BG), ManimColor(VENV), 0.18), 1)
        dx = vl.point(13)[0] - vl.point(12)[0]
        nr = tag("not in the README", LAPTOP)

        with self.voiceover(SAY[10]) as vo:
            self.play(FadeIn(top10, shift=DOWN * 0.1), run_time=0.5)
            self.play(d1.dot.animate.move_to(vl.point(13)), Transform(d1.text, lab13), run_time=1.0)
            vo.wait_until("If yours says")
            band_to, _ = vl.move_lo(13)      # the label keeps sitting over the start (lo_label)
            self.play(band_to, Transform(vl.band_label, lo_label(vl, 13)), run_time=0.9)
            vo.wait_until("the image's 3.12 falls outside")
            self.play(d2.animate.set_color(ERR), Transform(ck, crs), run_time=0.5)
            self.play(FadeIn(dl, shift=DOWN * 0.2), FadeIn(prev), run_time=0.6)
            vo.wait_until("so edit it to 3.12")
            # the edit chip covers the label exactly (opaque), then drags the start with it
            edit.shift(np.array([vl.point(13)[0] - edit.text.get_left()[0],
                                 vl.band_label.get_center()[1] - edit.text.get_center()[1], 0]))
            self.play(FadeIn(edit, scale=1.1), run_time=0.5)
            band_to, _ = vl.move_lo(12)
            self.play(band_to, edit.animate.shift(LEFT * dx), d2.animate.set_color(SYSTEM),
                      Transform(ck, ck_back), FadeOut(dl), run_time=1.0)
            vl.band_label.become(lo_label(vl, 12))      # ">=3.12", hidden under the opaque chip
            vo.wait_until("That fix isn't")
            nr.next_to(edit, LEFT, buff=0.3)
            self.play(FadeIn(nr, shift=RIGHT * 0.1), run_time=0.4)
            vo.wait_until("generate text shows why")
            self.play(Indicate(prev, color=INK, scale_factor=1.1), run_time=0.7)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
        self.wait(0.3)
