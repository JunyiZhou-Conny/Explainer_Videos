"""S05 · The system Python and PEP 668 (README steps 7-8, three extras, the V2 shelves).

Beats (script.md "## S05", one voiceover block each):
 0  TRACKER A7. The house terminal (14 rows, repo prompt) types `sudo apt install python3-pip`
    (two rows) -> 05-pip.txt lines 4-6 +Done, …, 54-57 ([Y/n] Y; line 56 folds), …, 603-604.
    "107 newly installed" underlines YELLOW; GREY row tag "package list varies by VM" on the
    first `…`. ▶ your turn.
 1  TRACKER A7 · extra. The terminal clears; `pip3 --version` (extra) -> 06-pip-version.txt line 2.
    `pip 23.0.1` and `(python 3.11)` pulse as named; the path underlines ORANGE with the tag
    "apt's folder"; `/usr` gets a GREY tag "U-S-R: the system's, not your home".
 2  The terminal clears; `pip3 install googletrans==4.0.2 art` (extra, two rows) -> 07-pip-refused.txt
    lines 2-5, …, 10, …, 20 (wrapped: 14 rows), line 2 RED. YELLOW underlines on "This environment
    is externally managed", "create a virtual environment" and `--break-system-packages`.
 3  `python3 -c 'import sys; print("\\n".join(sys.path))'` (extra) -> 15-syspath.txt lines 2-7. The six
    lines lift out and become V2 (six full-width shelves; the terminal shrinks to the 3-row strip):
    GREY current folder, three GREY standard-library shelves (bracketed), the ORANGE /usr/local
    shelf (empty) and apt's ORANGE shelf with four jars. A PINK search-light ("import pip") sweeps
    down and stops on apt's shelf; "import " drops away and "pip" becomes the jar's name tag
    (beside the jar: no room above it at this pitch). The three standard-library shelves merge
    into one GREY band "standard library".
 4  The strip leaves (all picture; tracker drops "· extra"). apt's shelf glows; GREY gears
    "OS tools" under the shelf link up to its jars; caption "a shared kitchen" (+ "externally
    managed") under the shelf's left end; an ORANGE chip "PEP 668" stamps onto the shelf's front
    edge; the pip jar's name tag returns above it on "makes pip respect it".
 5  TRACKER A8. The shelves fade, the terminal (14 rows) fades back in and types
    `sudo pip3 install --break-system-packages googletrans==4.0.2 art` (two rows); the flag and `sudo`
    are underlined as named; ▶ your turn; 08-pip-break.txt lines 2-5, …; a row chip "asked for 2"
    by the two `Collecting` lines; lines 34-35 (wrapped): the chip becomes "installed 12" (ORANGE)
    and the 12 package names turn ORANGE; GREY note "yours may say ‘Requirement already satisfied’
    for some"; line 36 (wrapped) gets a YELLOW bracket, "conflicting behaviour with the system
    package manager" underlines.
 6  Twelve ORANGE jars rise from the package names and fly onto the /usr/local shelf while the
    terminal shrinks to the strip and the shelves return; a chip "12". TRACKER A8 · extra.
    `python3 -c 'import googletrans; print(googletrans.__file__)'` (extra) -> 09-where.txt line 2; the
    PINK search-light stops on the /usr/local shelf, the googletrans jar gets its name tag; GREY tag
    "system-wide · every user" on that shelf; the two ORANGE shelves glow in turn ("above").
 7  The strip fades (tracker back to A8); the shelves spread out; tag "illustration · what if".
    A dashed ORANGE jar "httpx 0.23.3 (apt's copy)" on apt's shelf; GREY note "googletrans needs
    httpx ≥ 0.27.2" and the name tag "httpx 0.28.1" on pip's jar; a PINK light stops on pip's shelf,
    its label "import httpx" riding above it and landing beside "httpx 0.28.1"; the apt jar dims
    with a RED "hidden" tag; caption "shadowing · for every program that uses the system Python".
 8  A GREY README tip card (README.md · line 56) over the dimmed shelves; "We use it here
    deliberately as a quick demonstration" highlighted YELLOW.
 9  The picture narrows to the /usr/local shelf with one empty slot named httpx (S08's opening
    layout); two GREY students with requests "httpx 0.13" (classmate) and "httpx 0.28" (you).
    PONDER (8 s), card at the bottom.
10  The picture settles into the room the card leaves; the 0.28 jar lands in the slot, the 0.13
    jar knocks it off as it lands; caption "one shelf · the last install wins, for everyone";
    "you" turns RED. Fade out to an empty frame.
"""

import numpy as np
from manim import *

from explainer import style as S
from explainer.components import person_icon, ponder_card
from explainer.devops import (MONO, OUTPUT, box, chip, glyph_range, label, mono, mono_line, substring,
                              tag)
from explainer.scene import VoiceScene

from common import (ERR, INK, LOOKUP, NARRATION, P_REPO, SYSTEM, TURN, VENV, Shelves, capture, extra_tag,
                    jar, jars, name_tag, source_text, term, tracker_a, your_turn)

SAY = NARRATION["S05"]

# ------------------------------------------------------------------ commands (README spelling)
APT_PIP = "sudo apt install python3-pip"
PIP_VER = "pip3 --version"
PIP_NO = "pip3 install googletrans==4.0.2 art"
SYSPATH = "python3 -c 'import sys; print(\"\\n\".join(sys.path))'"
PIP_BREAK = "sudo pip3 install --break-system-packages googletrans==4.0.2 art"
WHERE = "python3 -c 'import googletrans; print(googletrans.__file__)'"

# ------------------------------------------------------------------ real outputs (pick = file line - 1)
_DONE = ("Reading package lists...", "Building dependency tree...", "Reading state information...")


def plus_done(lines):
    """apt prints ' Done' after its progress lines on a terminal (lost in the capture: ASSETS.md)."""
    return [s + " Done" if s in _DONE else s for s in lines]


_pip = capture("05-pip")
assert _pip.cmd.endswith(APT_PIP)                          # captured as `yes | sudo apt install ...`
PIP_READ = plus_done(_pip.pick((3, 5)))                    # file lines 4-6
PIP_SUM = _pip.pick((53, 55))                              # file lines 54-56
assert PIP_SUM[0].startswith("0 upgraded, 107 newly installed"), PIP_SUM[0]
PIP_ASK = _pip.pick(56)[0]                                 # file line 57, cut after [Y/n]
PIP_ASK = PIP_ASK[:PIP_ASK.index("[Y/n]") + len("[Y/n]")]
# capture() reads with universal newlines, so apt's mid-line \r progress rows split into extra
# lines: file lines 603-604 are the last two body lines (checked here).
PIP_TAIL = _pip.pick((-2, -1))
assert PIP_TAIL[0].startswith("Setting up python3-dev") and PIP_TAIL[1].startswith("Processing triggers")

_ver = capture("06-pip-version")
assert _ver.cmd == PIP_VER
VER_OUT = _ver.pick(1)[0]                                  # file line 2

_ref = capture("07-pip-refused")
assert _ref.cmd == PIP_NO
REF_OUT = _ref.pick((1, 4), 9, 19)                         # file lines 2-5, …, 10, …, 20
assert REF_OUT[0] == "error: externally-managed-environment"

_sys = capture("15-syspath")
assert _sys.cmd == SYSPATH, _sys.cmd
SYS_OUT = _sys.pick((1, 6))                                # file lines 2-7
assert SYS_OUT[0] == "" and len(SYS_OUT) == 6

_brk = capture("08-pip-break")
assert _brk.cmd == PIP_BREAK
BRK_HEAD = _brk.pick((1, 4))                               # file lines 2-5
BRK_INST = _brk.pick((33, 34))                             # file lines 34-35
BRK_WARN = _brk.pick(35)[0]                                # file line 36
assert BRK_INST[1].startswith("Successfully installed") and BRK_WARN.startswith("WARNING")
PKGS = BRK_INST[1].split()[2:]                             # the 12 name-version tokens
assert len(PKGS) == 12, PKGS
HTTPX_REQ = next(s for s in _brk.lines if s.startswith("Collecting httpx"))   # file line 7
assert HTTPX_REQ.endswith(">=0.27.2")

_where = capture("09-where")
assert _where.cmd == WHERE
WHERE_OUT = _where.pick(1)[0]                              # file line 2
LOCAL = "/usr/local/lib/python3.11/dist-packages"
assert WHERE_OUT.startswith(LOCAL)

# README.md line 56 (the tip after step 8), broken into card rows (checked against the file)
TIP56 = ["--break-system-packages: Modern Debian and Ubuntu treat their system",
         "Python as externally managed: its packages are maintained by the",
         "operating system through apt. By default, pip refuses to modify it.",
         "--break-system-packages overrides that protection. We use it here",
         "deliberately as a quick demonstration; the next walkthrough uses uv",
         "to keep project packages isolated."]
_line56 = source_text("README.md").split("\n")[55]
assert " ".join(TIP56) == _line56[2:].replace("**", "").replace("`", ""), _line56

PONDER_Q = ("A classmate's project on this VM needs httpx 0.13.\nYours needs httpx 0.28.\n"
            "Both install system-wide like this. What happens?")

# ------------------------------------------------------------------ layout
BOTTOM = -3.57           # terminal bottom edge (a 14-row terminal must clear the tracker)
TRACK_LEFT, TRACK_TOP = -6.5, 3.58
ROWS = 14
B6 = [2.4 - 0.74 * k for k in range(6)]          # six shelves above the strip (board y)
B4 = [2.4, 2.4 - 3.7 / 3, 2.4 - 7.4 / 3, -1.3]   # four shelves above the strip
B4W = [2.4, 0.9, -0.6, -2.1]                     # four shelves, whole frame (no strip)
SLOT_BOARD_Y = 0.85                              # S08's opening picture (one shelf, two students)


def place_tracker(tr):
    tr.shift(np.array([TRACK_LEFT - tr.get_left()[0], TRACK_TOP - tr.get_top()[1], 0]))
    return tr


def put_bottom(t):
    t.shift(np.array([-t.box.get_center()[0], BOTTOM - t.box.get_bottom()[1], 0]))
    return t


def caption_extra(tr, on: bool = True):
    """The tracker caption with (or without) ' · extra' while a non-README command is on screen."""
    k = tr.k
    s = f"step {k} of {len(tr.steps)}: {tr.steps[k - 1]}"
    new = label(s + " · extra", tr.size, tr.hi_color, t2c={"· extra": S.GREY}) if on else \
        label(s, tr.size, tr.hi_color)
    new.next_to(tr.dots, RIGHT, buff=0.25)
    return Transform(tr.caption, new)


def row_y(t, i: int) -> float:
    """Centre height of text row i of terminal t."""
    ln = mono_line("|", t.size)
    t._place(ln, i)
    return ln.strut.get_center()[1]


def under(g, color, y=None, stroke=4, pad=0.03) -> Line:
    y = g.get_bottom()[1] - 0.06 if y is None else y
    return Line([g.get_left()[0] - pad, y, 0], [g.get_right()[0] + pad, y, 0], color=color,
                stroke_width=stroke)


def line_under(line, sub, color, stroke=4):
    """Underline the substring `sub` of a terminal row, under the row's descenders."""
    return under(substring(line, sub), color, y=line.strut.get_bottom()[1] - 0.01, stroke=stroke)


def row_tag(parts, color=S.GREY, size: float = 22, fill: float = 0.92, text_color=None) -> VGroup:
    """A tag that fits inside one terminal row (the house tag is taller than a row).
    parts: a string, or (text, 'mono'|'label') pairs."""
    if isinstance(parts, str):
        parts = [(parts, "label")]
    tc = text_color or color
    t = VGroup(*[mono(x, size, tc) if k == "mono" else label(x, size, tc) for x, k in parts])
    t.arrange(RIGHT, buff=0.12)
    h = 0.37
    b = RoundedRectangle(width=t.width + 0.36, height=h, corner_radius=h / 2, stroke_color=color,
                         stroke_width=2).set_fill(S.BG, fill)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def row_chip(s: str, color, size: float = 22) -> VGroup:
    """A chip (border + faint tint, WHITE text) the height of a terminal row."""
    t = label(s, size, INK)
    h = 0.37
    b = RoundedRectangle(width=t.width + 0.4, height=h, corner_radius=h / 2.6, stroke_color=color,
                         stroke_width=2.5).set_fill(color, 0.2)
    bg = b.copy().set_stroke(width=0).set_fill(S.BG, 1)
    t.move_to(b)
    g = VGroup(bg, b, t)
    g.box, g.text = b, t
    return g


def beside(mob, line, buff=0.45, min_x=None):
    """Put `mob` right of terminal row `line`, centred on the row (left edge at least min_x)."""
    x = line.strut.get_right()[0] + buff
    if min_x is not None:
        x = max(x, min_x)
    return mob.move_to([x + mob.width / 2, line.strut.get_center()[1], 0])


def hl_bar(g, color=TURN, opacity=0.25, buff=0.05) -> Rectangle:
    return Rectangle(width=g.width + 2 * buff, height=g.height + 2 * buff, stroke_width=0) \
        .set_fill(color, opacity).move_to(g)


def text_span(t: Text, s: str, sub: str) -> VGroup:
    """The glyphs of `sub` in a Text built from string `s` (whole text if absent, e.g. translated)."""
    i = s.find(sub)
    if i < 0 or len(t) != len("".join(s.split())):
        return VGroup(t)
    a, n = len("".join(s[:i].split())), len("".join(sub.split()))
    return VGroup(*t[a:a + n])


def gear(r: float = 0.18, n: int = 8, color: str = S.GREY) -> VGroup:
    """A small cog (an OS tool that runs on the system Python)."""
    teeth = VGroup(*[Rectangle(width=r * 0.42, height=r * 0.5, stroke_width=0).set_fill(color, 1)
                     .move_to(UP * r * 1.05).rotate(k * TAU / n, about_point=ORIGIN) for k in range(n)])
    ring = Circle(radius=r, stroke_color=color, stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
    hub = Circle(radius=r * 0.38, stroke_color=color, stroke_width=2).set_fill(S.BG, 1)
    return VGroup(teeth, ring, hub)


def dashed_jar(color: str = SYSTEM, height: float = 0.36) -> VGroup:
    """A jar drawn dashed (a hypothetical package, 'what if')."""
    j = jar(color, height)
    body = DashedVMobject(j[0].copy().set_fill(opacity=0), num_dashes=14, dashed_ratio=0.55)
    body.set_stroke(color, 2.5)
    fill = j[0].copy().set_stroke(width=0).set_fill(color, 0.12)
    lid = DashedVMobject(j[1].copy().set_fill(opacity=0), num_dashes=8, dashed_ratio=0.55)
    lid.set_stroke(color, 2)
    return VGroup(fill, body, lid)


def light_band(board_y: float, color=LOOKUP, opacity: float = 0.22, h: float = 0.62) -> Rectangle:
    """A translucent band over the shelf whose board is at board_y (its label and jars)."""
    return Rectangle(width=12.7, height=h, stroke_width=0).set_fill(color, opacity) \
        .move_to([0, board_y + h / 2 - 0.08, 0])


def bracket(top: float, bottom: float, x: float, color, tick: float = 0.13) -> VMobject:
    """A ']' at x from y=top to y=bottom, ticks pointing left."""
    m = VMobject(stroke_color=color, stroke_width=3)
    m.set_points_as_corners([[x - tick, top, 0], [x, top, 0], [x, bottom, 0], [x - tick, bottom, 0]])
    return m


def readme_card(line_no: int, body: VGroup, extra: str = "") -> VGroup:
    """A GREY README card: header 'README.md · line n', the README's own words, a quote bar."""
    head = VGroup(mono("README.md", 20, S.GREY), label(f"· line {line_no}{extra}", 20, S.GREY))
    head.arrange(RIGHT, buff=0.12)
    bar = Line(body.get_corner(UL) + np.array([-0.22, 0.04, 0]),
               body.get_corner(DL) + np.array([-0.22, -0.04, 0]), color=S.GREY, stroke_width=4)
    inner = VGroup(head, VGroup(bar, body)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    frame = box(inner.width + 0.55, inner.height + 0.4, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
    inner.move_to(frame).align_to(frame, LEFT).shift(RIGHT * 0.28)
    g = VGroup(frame, inner)
    g.frame, g.head = frame, head
    return g


class SystemPip(VoiceScene):
    # ------------------------------------------------------------- terminal helpers (as in S04)
    def bare_prompt(self, t):
        ln = t.type(self, "", type_time=0)
        ln.bare = True
        return ln

    def type_cmd(self, t, cmd, type_time=None):
        """Type at the waiting prompt (replacing a bare prompt line if there is one)."""
        if len(t.lines) and getattr(t.lines[-1], "bare", False):
            last = t.lines[-1]
            self.remove(last, *last.submobjects)
            t.lines.remove(last)
        return t.type(self, cmd, type_time)

    def attach(self, line, mob):
        """Make `mob` part of terminal row `line` (it scrolls and clears with it)."""
        self.remove(mob)
        line.add(mob)
        self.add(line)
        return mob

    def pin(self, line, mob, run_time=0.4, anim=None):
        self.play(anim or FadeIn(mob, shift=LEFT * 0.1), run_time=run_time)
        return self.attach(line, mob)

    def unpin(self, pairs, run_time=0.3, *extra):
        self.play(*[FadeOut(m) for _, m in pairs], *extra, run_time=run_time)
        for line, m in pairs:
            if m in line.submobjects:
                line.remove(m)

    def answer_yes(self, t, text, pause=0.6):
        """apt's question, a pause, then the `Y` keystroke (flashes YELLOW). Returns (line, Y)."""
        ln = t.print(self, [text], run_time=0.3)[0]
        self.wait(pause)
        y = mono_line(text + " Y", t.size, OUTPUT)
        y.shift(ln.strut.get_corner(UL) - y.strut.get_corner(UL))
        yg = y.glyphs[-1].set_color(TURN)
        self.play(FadeIn(yg, scale=1.6), run_time=0.2)
        self.play(Indicate(yg, color=TURN, scale_factor=1.8), run_time=0.45)
        self.play(yg.animate.set_color(INK), run_time=0.2)
        self.attach(ln, yg)
        return ln, yg

    def resize(self, t, rows, run_time=0.8, extra=(), keep=None):
        """Grow or shrink the terminal to `rows` (bottom edge fixed); it keeps its last lines
        (at most `keep` of them)."""
        ref = put_bottom(term(prompt=t.prompt, rows=rows))
        n_keep = min(len(t.lines), rows, len(t.lines) if keep is None else keep)
        kept = t.lines.submobjects[len(t.lines) - n_keep:]
        gone = t.lines.submobjects[:len(t.lines) - n_keep]
        if gone:
            self.play(FadeOut(VGroup(*gone)), run_time=0.25)
            for ln in gone:
                t.lines.remove(ln)
                self.remove(ln)
        anims = [Transform(t.box, ref.box), Transform(t.bar, ref.bar),
                 t.dots.animate.move_to(ref.dots), t.title.animate.move_to(ref.title)]
        for i, ln in enumerate(kept):
            anims.append(ln.animate.shift(ref._slot(i) - ln.strut.get_corner(UL)))
        self.play(*anims, *extra, run_time=run_time)
        t.rows = rows
        return t

    # ------------------------------------------------------------- the scene
    def construct(self):
        assert len(SAY) == 11, f"S05 has {len(SAY)} SAY lines; this scene times 11"

        tr = place_tracker(tracker_a(6))
        t = put_bottom(term(prompt=P_REPO, rows=ROWS))

        # ========================================================== 0 · sudo apt install python3-pip
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.1), FadeIn(t), run_time=0.6)
            self.play(tr.goto(7), run_time=0.5)
            cmd0 = self.type_cmd(t, APT_PIP, 1.1)
            pkg_word = substring(cmd0.rows[1], "python3-pip")

            vo.wait_until("That's Debian's own")
            self.play(pkg_word.animate.set_color(SYSTEM), run_time=0.3)
            self.play(Indicate(pkg_word, color=SYSTEM, scale_factor=1.2), run_time=0.7)
            t.print(self, PIP_READ, run_time=0.5)
            dots0 = t.print(self, ["…"], run_time=0.2)[0]
            summ = t.print(self, PIP_SUM, run_time=0.6, wrap=True)

            vo.wait_until("Answer Y again")
            self.answer_yes(t, PIP_ASK, pause=0.2)
            t.print(self, ["…", *PIP_TAIL], run_time=0.5)

            vo.wait_until("Ours pulled in")
            ul0 = line_under(summ[0], "107 newly installed", TURN)
            self.play(Create(ul0), run_time=0.6)
            self.attach(summ[0], ul0)
            vo.wait_until("a real VM usually")
            vary = beside(row_tag("package list varies by VM"), dots0)
            self.pin(dots0, vary, run_time=0.5)

            # the tag arrives a beat before "Pause and run it", which then shakes it (on screen ~3 s)
            self.wait(0.8)
            yt0 = beside(your_turn(), cmd0.rows[1])
            self.pin(cmd0.rows[1], yt0, run_time=0.4)
            vo.wait_until("Pause and run it")
            self.play(Wiggle(yt0, scale_value=1.15, rotation_angle=0.025 * TAU), run_time=0.7)

        # ========================================================== 1 · pip3 --version (extra)
        with self.voiceover(SAY[1]) as vo:
            self.wait(0.6)                     # the your-turn tag stays a moment into the next block
            self.unpin([(cmd0.rows[1], yt0), (dots0, vary)], 0.3, caption_extra(tr))
            t.clear(self, run_time=0.3)
            cmd1 = self.type_cmd(t, PIP_VER, 0.7)
            xt1 = beside(tag("extra", S.GREY), cmd1)
            self.pin(cmd1, xt1, run_time=0.3)
            out1 = t.print(self, [VER_OUT], run_time=0.4)[0]

            vo.wait_until("It's pip 23.0.1")
            self.play(Indicate(substring(out1, "pip 23.0.1"), color=S.WHITE, scale_factor=1.2), run_time=0.8)
            vo.wait_until("for Python 3.11")
            self.play(Indicate(substring(out1, "(python 3.11)"), color=S.WHITE, scale_factor=1.2), run_time=0.8)

            vo.wait_until("in a folder called")
            path = substring(out1, "/usr/lib/python3/dist-packages/pip")
            ul1 = line_under(out1, "/usr/lib/python3/dist-packages/pip", SYSTEM)
            apt_tag = row_tag("apt's folder", SYSTEM)
            apt_tag.move_to([path.get_right()[0] - apt_tag.width / 2, row_y(t, 2), 0])
            self.play(Create(ul1), path.animate.set_color(SYSTEM), run_time=0.7)
            self.attach(out1, ul1)
            self.play(FadeIn(apt_tag, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("dist-packages under")
            self.play(Indicate(substring(out1, "dist-packages"), color=SYSTEM, scale_factor=1.15), run_time=0.8)
            vo.wait_until("under user lib")
            self.play(Indicate(substring(out1, "/usr/lib"), color=SYSTEM, scale_factor=1.25), run_time=0.8)

            vo.wait_until("That user is spelled")
            usr = substring(out1, "/usr")
            usr_tag = row_tag("U-S-R: the system's, not your home", S.GREY)
            y3 = row_y(t, 3)
            usr_tag.move_to([usr.get_left()[0] - 0.15 + usr_tag.width / 2, y3, 0])
            stem = Line([usr.get_center()[0], ul1.get_y() - 0.05, 0],
                        [usr.get_center()[0], usr_tag.get_top()[1], 0], color=S.GREY, stroke_width=2.5)
            self.play(Indicate(usr, color=S.WHITE, scale_factor=1.5), run_time=0.7)
            self.play(Create(stem), FadeIn(usr_tag, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("not your home")
            self.play(Indicate(usr_tag.text, color=S.WHITE, scale_factor=1.08), run_time=0.8)

        # ========================================================== 2 · pip refuses (extra)
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(apt_tag, usr_tag, stem)), run_time=0.3)
            t.clear(self, run_time=0.3)
            cmd2 = self.type_cmd(t, PIP_NO, 1.4)
            vo.wait_until("without sudo")
            self.play(Indicate(substring(cmd2.rows[0], "pip3"), color=S.WHITE, scale_factor=1.3), run_time=0.8)
            vo.wait_until("it isn't in the README")
            xt2 = beside(extra_tag(), cmd2.rows[1])
            self.pin(cmd2.rows[1], xt2, run_time=0.4)

            vo.wait_until("Again, pip refuses")
            out2 = t.print(self, [(REF_OUT[0], ERR)] + REF_OUT[1:], wrap=True, run_time=1.1, lag=0.1)
            err2 = out2[0]
            self.play(Indicate(err2, color=ERR, scale_factor=1.06), run_time=0.7)

            vo.wait_until("this environment is externally")
            l4 = t.find("This environment is externally managed")
            u4 = line_under(l4, "This environment is externally managed", TURN)
            self.play(Create(u4), run_time=0.8)
            vo.wait_until("install with apt")
            l5 = t.find("try apt install")
            self.play(Indicate(substring(l5, "try apt install"), color=SYSTEM, scale_factor=1.12), run_time=0.8)
            vo.wait_until("or create a virtual")
            l10 = t.find("create a virtual environment")
            u10 = line_under(l10, "create a virtual environment", TURN)
            self.play(Create(u10), run_time=0.8)

            vo.wait_until("Its last note")
            l20 = t.find("--break-system-packages")
            first_note = t.find("note: If you believe")
            note_all = VGroup(*t.lines.submobjects[list(t.lines).index(first_note):
                                                   list(t.lines).index(l20) + 1])
            self.play(Indicate(note_all, color=S.WHITE, scale_factor=1.02), run_time=0.8)
            vo.wait_until("names a way around it")
            u20 = line_under(l20, "--break-system-packages", TURN)
            self.play(Create(u20), substring(l20, "--break-system-packages").animate.set_color(TURN),
                      run_time=0.7)
            for ln, u in ((l4, u4), (l10, u10), (l20, u20)):
                self.attach(ln, u)

        # ========================================================== 3 · sys.path -> V2 shelves (extra)
        sh = Shelves(["(empty) = the current folder"] + SYS_OUT[1:], width=12.4, size=22, pitch=0.74,
                     colors={4: SYSTEM, 5: SYSTEM})
        sh.shift(UP * (B6[0] - sh.rows[0][0].get_y()))
        apt_jars = sh.put(5, jars(4, SYSTEM))
        pip_jar = apt_jars[0]
        pip_tag = mono("pip", 22, INK).next_to(pip_jar, LEFT, buff=0.18)
        std_top = sh.rows[1][1].get_top()[1] + 0.02
        std_bot = sh.rows[3][0].get_y() - 0.04
        std_br = bracket(std_top, std_bot, 6.42, S.GREY)
        std_br_t = label("standard library", 24, S.GREY)
        std_br_t.move_to([6.2 - std_br_t.width / 2, sh.rows[2][0].get_y() + 0.32, 0])
        look = mono("import pip", 22, LOOKUP)

        with self.voiceover(SAY[3]) as vo:
            self.unpin([(l4, u4), (l10, u10), (l20, u20)], 0.3,
                       substring(l20, "--break-system-packages").animate.set_color(OUTPUT))
            self.play(Indicate(err2, color=ERR, scale_factor=1.06), run_time=0.9)
            vo.wait_until("Picture how Python")
            self.play(Indicate(substring(t.find("error:"), "externally-managed-environment"), color=ERR,
                               scale_factor=1.08), run_time=0.9)
            vo.wait_until("This extra one-liner")
            cmd3 = self.type_cmd(t, SYSPATH, 1.6)
            xt3 = beside(tag("extra", S.GREY), cmd3.rows[1])
            self.pin(cmd3.rows[1], xt3, run_time=0.3)
            vo.wait_until("prints the list")
            out3 = t.print(self, SYS_OUT, run_time=0.8, lag=0.12)
            vo.wait_until("the folders Python searches")
            self.play(Indicate(VGroup(*[ln.glyphs for ln in out3[1:]]), color=LOOKUP, scale_factor=1.05),
                      run_time=0.9)

            vo.wait_until("Think of them as shelves")
            # the six printed lines lift out of the terminal and become the shelf labels
            for ln in out3:
                t.lines.remove(ln)
            moving = []
            for i, ln in enumerate(out3):
                if len(ln.glyphs):
                    self.add(ln.glyphs)
                    moving.append(ReplacementTransform(ln.glyphs, sh.rows[i][1]))
            empty_y = out3[0].strut.get_y()
            # the command steps aside while the lines rise (nothing crosses), then returns in the strip
            cmd_rows = list(cmd3.rows)
            self.play(FadeOut(VGroup(*t.lines)), run_time=0.3)
            for ln in list(t.lines):
                t.lines.remove(ln)
            lift = [*moving, FadeIn(sh.rows[0][1], shift=UP * (sh.rows[0][1].get_y() - empty_y))]
            self.resize(t, 3, run_time=1.2, extra=lift)
            for ln in cmd_rows:
                t._place(ln, len(t.lines))
                t.lines.add(ln)
            # the boards slide in under the labels once the terminal is out of the way (none crosses it)
            self.play(LaggedStart(*[Create(r[0]) for r in sh.rows], lag_ratio=0.1),
                      FadeIn(VGroup(*cmd_rows), shift=UP * 0.1), run_time=0.7)
            self.bare_prompt(t)
            self.play(Create(std_br), FadeIn(std_br_t, shift=LEFT * 0.1),
                      LaggedStart(*[FadeIn(j, shift=DOWN * 0.15) for j in apt_jars], lag_ratio=0.15),
                      run_time=0.7)

            vo.wait_until("On every import")
            lt = light_band(B6[0])
            look.move_to([2.3, lt.get_y(), 0])
            beam = VGroup(lt, look)
            self.play(FadeIn(beam), run_time=0.3)
            self.play(beam.animate.shift(UP * (B6[5] - B6[0])), run_time=2.2, rate_func=linear)
            vo.wait_until("takes the first match")
            # the looked-up name finds its jar: "import " drops away, "pip" becomes the jar's name tag
            # (beside it: the six-shelf pitch leaves no room above a jar on the bottom shelf)
            self.play(Indicate(pip_jar, color=LOOKUP, scale_factor=1.5), FadeOut(look[:6]),
                      ReplacementTransform(look[6:], pip_tag), run_time=0.8)
            self.wait(0.3)

            # the three standard-library shelves merge into one GREY band
            std_board = Line(LEFT * 6.2, RIGHT * 6.2, color=S.GREY, stroke_width=5).set_y(B4[1])
            std_lbl = label("standard library", 24, S.GREY)
            std_lbl.next_to(std_board, UP, buff=0.1).align_to(std_board, LEFT)
            band = Rectangle(width=12.4, height=0.8, stroke_width=0).set_fill(S.GREY, 0.12)
            band.move_to(std_board, aligned_edge=DOWN)
            self.play(FadeOut(lt), run_time=0.3)     # the pip tag stays while the shelves merge
            self.play(ReplacementTransform(VGroup(*[sh.rows[i][0] for i in (1, 2, 3)]), std_board),
                      ReplacementTransform(std_br_t, std_lbl),
                      FadeOut(VGroup(*[sh.rows[i][1] for i in (1, 2, 3)]), target_position=std_lbl),
                      FadeOut(std_br), FadeIn(band),
                      sh.rows[4].animate.shift(UP * (B4[2] - B6[4])),
                      run_time=1.2)
        row0, local_row, apt_row = sh.rows[0], sh.rows[4], sh.rows[5]
        std_g = VGroup(band, std_board, std_lbl)

        # ========================================================== 4 · a shared kitchen; PEP 668
        # The strip (the sys.path one-liner) leaves: this beat is all picture, and the room under apt's
        # shelf takes the OS tools (the shelf's right end is full of jars) and the caption.
        apt_glow = light_band(B4[3], SYSTEM, 0.18)
        g1, g2 = gear(0.22), gear(0.22)
        jx = [j.get_x() for j in apt_jars]
        g1.move_to([(jx[0] + jx[1]) / 2, -2.3, 0])
        g2.move_to([(jx[2] + jx[3]) / 2, -2.3, 0])
        gears = VGroup(g1, g2)
        os_lbl = label("OS tools", 24, S.GREY).next_to(gears, LEFT, buff=0.3)
        links = VGroup(*[Line(g.get_top() + UP * 0.02, apt_jars[k].get_bottom(), color=S.GREY, stroke_width=2.5)
                         for g, ks in ((g1, (0, 1)), (g2, (2, 3))) for k in ks])
        kitchen = label("a shared kitchen", 30, INK)
        kitchen.move_to([-6.2 + kitchen.width / 2, -2.2, 0])
        ext = label("“externally managed”", 24, S.GREY).next_to(kitchen, DOWN, buff=0.15).align_to(kitchen, LEFT)
        pep_chip = chip("PEP 668", SYSTEM, size=24)
        pep = VGroup(pep_chip.box.copy().set_stroke(width=0).set_fill(S.BG, 1), pep_chip)
        pep.move_to([1.3, B4[3], 0])          # stamped on the shelf's front edge

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(t), FadeOut(pip_tag), caption_extra(tr, False), FadeIn(apt_glow),
                      Indicate(apt_row[1], color=SYSTEM, scale_factor=1.06), run_time=0.9)
            for ln in list(t.lines):
                t.lines.remove(ln)
            vo.wait_until("Debian itself runs")
            self.play(FadeIn(gears, scale=0.6), FadeIn(os_lbl, shift=RIGHT * 0.1), run_time=0.6)
            self.play(Rotate(g1, -PI / 2), Rotate(g2, PI / 2), run_time=0.8)
            vo.wait_until("that depend on exactly")
            self.play(LaggedStart(*[Create(l) for l in links], lag_ratio=0.2), Rotate(g1, -PI / 2),
                      Rotate(g2, PI / 2), run_time=0.9)
            vo.wait_until("at exactly those versions")
            self.play(LaggedStart(*[Indicate(j, color=SYSTEM, scale_factor=1.3) for j in apt_jars],
                                  lag_ratio=0.15), run_time=1.0)

            vo.wait_until("The system Python is")
            self.play(FadeIn(kitchen, shift=UP * 0.1), run_time=0.6)
            self.play(Indicate(VGroup(local_row, apt_row), color=SYSTEM, scale_factor=1.02), run_time=0.9)
            vo.wait_until("and apt is the cook")
            self.play(Indicate(apt_row[1], color=SYSTEM, scale_factor=1.08), Rotate(g1, -PI / 2),
                      Rotate(g2, PI / 2), run_time=0.9)
            vo.wait_until("That's what externally managed")
            self.play(FadeIn(ext, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("PEP 668 is the rule")
            self.play(FadeIn(pep, scale=2.4), run_time=0.45, rate_func=rush_into)
            self.play(Indicate(pep_chip.text, color=SYSTEM, scale_factor=1.15), run_time=0.5)
            vo.wait_until("makes pip respect it")
            pip_tag4 = name_tag(pip_jar, "pip", INK, 22)    # the merge left room above the jar
            self.play(FadeIn(pip_tag4, shift=UP * 0.1), Indicate(pip_jar, color=SYSTEM, scale_factor=1.4),
                      run_time=0.8)

        beat4 = VGroup(apt_glow, gears, os_lbl, links, kitchen, ext, pep, pip_tag4)
        shelves = VGroup(row0, std_g, local_row, apt_row, apt_jars)

        # ========================================================== 5 · sudo pip3 install --break-system-packages
        t = put_bottom(term(prompt=P_REPO, rows=ROWS))       # the terminal comes back, full size

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(beat4), FadeOut(shelves), tr.goto(8), FadeIn(t), run_time=0.7)
            cmd5 = self.type_cmd(t, PIP_BREAK, 1.8)
            r0, r1 = cmd5.rows

            vo.wait_until("with the flag")
            flag = substring(r1, "--break-system-packages")
            u_flag = line_under(r1, "--break-system-packages", TURN)
            self.play(Create(u_flag), run_time=0.6)
            vo.wait_until("The flag overrides")
            guard = row_tag("overrides the guard", S.GREY)
            guard.move_to([flag.get_left()[0] - 0.1 + guard.width / 2, row_y(t, 2), 0])
            self.play(FadeIn(guard, shift=UP * 0.1), Indicate(flag, color=TURN, scale_factor=1.08), run_time=0.7)
            vo.wait_until("sudo lets pip")
            sudo = substring(r0, "sudo")
            u_sudo = line_under(r0, "sudo", S.WHITE)
            self.play(Create(u_sudo), Indicate(sudo, color=S.WHITE, scale_factor=1.3), run_time=0.8)

            vo.wait_until("Pause and run it")
            yt5 = beside(your_turn(), r1)
            self.play(FadeOut(VGroup(u_flag, guard, u_sudo)), run_time=0.25)
            self.pin(r1, yt5, run_time=0.4)
            head = t.print(self, BRK_HEAD, run_time=0.5)
            dots5 = t.print(self, ["…"], run_time=0.2)[0]

            vo.wait_until("We asked for 2")
            asked = row_chip("asked for 2", S.GREY)
            beside(asked, head[2], buff=0.45)
            self.play(Indicate(substring(head[0], "googletrans==4.0.2"), color=S.WHITE, scale_factor=1.12),
                      Indicate(substring(head[2], "art"), color=S.WHITE, scale_factor=1.3),
                      FadeIn(asked, shift=LEFT * 0.1), run_time=0.8)
            self.attach(head[2], asked)
            vo.wait_until("and got 12")
            inst = t.print(self, BRK_INST, wrap=True, run_time=0.6)
            n_inst = -(-len(BRK_INST[0]) // t.max_chars)
            inst_rows, succ_rows = list(inst[:n_inst]), list(inst[n_inst:])
            # the 12 package names, ORANGE: they now live in the system Python
            succ = BRK_INST[1]
            names, starts = [], []
            for p in PKGS:
                i0 = succ.index(" " + p + " " if p != PKGS[-1] else " " + p) + 1
                starts.append(i0)
                for k in range(len(p)):
                    r, c = divmod(i0 + k, t.max_chars)
                    g = glyph_range(succ_rows[r], c, c + 1)
                    names.extend(g)
            got = row_chip("installed 12", SYSTEM)
            got.move_to([inst_rows[-1].strut.get_right()[0] + 0.45 + got.width / 2,
                         inst_rows[-1].strut.get_y(), 0])
            head[2].remove(asked)
            self.add(asked)
            self.play(VGroup(*names).animate.set_color(SYSTEM), ReplacementTransform(asked, got),
                      run_time=0.9)
            self.attach(inst_rows[-1], got)
            vo.wait_until("if yours says")
            sat = row_tag("yours may say “Requirement already satisfied” for some", S.GREY)
            beside(sat, dots5, buff=0.4)
            self.pin(dots5, sat, run_time=0.5)
            vo.wait_until("apt already had")
            self.play(Indicate(sat.text, color=S.WHITE, scale_factor=1.05), run_time=0.8)

            vo.wait_until("And the warning says")
            warn = t.print(self, [BRK_WARN], wrap=True, run_time=0.6)
            x_b = t.box.get_left()[0] + 0.17
            wbr = VMobject(stroke_color=TURN, stroke_width=3.5).set_points_as_corners([
                [x_b + 0.1, warn[0].strut.get_top()[1], 0], [x_b, warn[0].strut.get_top()[1], 0],
                [x_b, warn[-1].strut.get_bottom()[1], 0], [x_b + 0.1, warn[-1].strut.get_bottom()[1], 0]])
            self.play(Create(wbr), run_time=0.5)
            self.attach(warn[0], wbr)
            vo.wait_until("running pip as root")
            self.play(Indicate(substring(warn[0], "Running pip as the 'root' user"), color=TURN,
                               scale_factor=1.06), run_time=0.8)
            vo.wait_until("can clash")
            conf = t.find("conflicting behaviour with the system package manager")
            u_conf = line_under(conf, "conflicting behaviour with the system package manager", TURN)
            self.play(Create(u_conf), run_time=0.8)
            self.attach(conf, u_conf)

        # ========================================================== 6 · where did they go? (extra)
        fly = VGroup()
        for i0 in starts:
            r, c = divmod(i0, t.max_chars)
            g = glyph_range(succ_rows[r], c, min(c + 3, t.max_chars))
            fly.add(jar(SYSTEM).move_to(g.get_center() + UP * 0.05))
        local_jars = sh.put(4, jars(12, SYSTEM))
        gt_jar, hx_jar = local_jars[PKGS.index("googletrans-4.0.2")], local_jars[PKGS.index("httpx-0.28.1")]
        n12 = chip("12", SYSTEM, size=24, font=MONO)
        n12.move_to([local_jars.get_right()[0] - n12.width / 2, local_jars.get_top()[1] + 0.12 + n12.height / 2, 0])
        gt_tag = name_tag(gt_jar, "googletrans", INK, 22)
        sys_tag = tag("system-wide · every user", S.GREY)
        sys_tag.move_to([-6.2 + sys_tag.width / 2, local_row[1].get_top()[1] + 0.1 + sys_tag.height / 2, 0])

        with self.voiceover(SAY[6]) as vo:
            self.play(LaggedStart(*[FadeIn(j, scale=0.4) for j in fly], lag_ratio=0.06), run_time=0.7)
            targets = [j.get_center() for j in local_jars]
            t.clear(self, run_time=0.25)
            self.resize(t, 3, run_time=1.0,
                        extra=[FadeIn(shelves), *[fj.animate.move_to(p) for fj, p in zip(fly, targets)]])
            self.remove(*fly)
            self.add(local_jars)
            self.play(FadeIn(n12, shift=DOWN * 0.1), Indicate(local_row[1], color=SYSTEM, scale_factor=1.04),
                      caption_extra(tr), run_time=0.6)
            cmd6 = self.type_cmd(t, WHERE, 1.3)
            xt6 = beside(tag("extra", S.GREY), cmd6.rows[1])
            self.pin(cmd6.rows[1], xt6, run_time=0.3)

            vo.wait_until("where it lives")
            out6 = t.print(self, [WHERE_OUT], run_time=0.4)[0]
            vo.wait_until("in dist-packages under")
            lt6 = light_band(B4[0])
            self.play(FadeIn(lt6), run_time=0.25)
            self.play(lt6.animate.move_to(light_band(B4[2]).get_center()), run_time=1.3, rate_func=linear)
            u6 = line_under(out6, LOCAL, LOOKUP)
            self.play(Indicate(gt_jar, color=LOOKUP, scale_factor=1.5), FadeIn(gt_tag, shift=UP * 0.15),
                      Create(u6), run_time=0.8)
            self.attach(out6, u6)

            vo.wait_until("still the system's")
            self.play(FadeOut(lt6), FadeIn(sys_tag, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("shared by every user")
            self.play(Indicate(sys_tag.text, color=S.WHITE, scale_factor=1.08), run_time=0.8)

            vo.wait_until("Look at the shelves")
            glow_l = light_band(B4[2], SYSTEM, 0.2)
            glow_a = light_band(B4[3], SYSTEM, 0.2)
            self.play(Indicate(VGroup(local_row, apt_row), color=SYSTEM, scale_factor=1.02), run_time=0.8)
            vo.wait_until("that shelf sits above")
            self.play(FadeIn(glow_l), run_time=0.5)
            vo.wait_until("the one apt owns")
            self.play(FadeOut(glow_l), FadeIn(glow_a), run_time=0.6)
            self.play(FadeOut(glow_a), run_time=0.4)

        # ========================================================== 7 · what if: shadowing
        ill = tag("illustration · what if", S.GREY)
        ill.move_to([6.45 - ill.width / 2, 3.3, 0])
        dy = [B4W[k] - B4[k] for k in range(4)]
        d_jar = dashed_jar(SYSTEM)
        caption7 = label("shadowing · for every program that uses the system Python", 26, INK)
        caption7.move_to([0, -2.95, 0])
        look7 = mono("import httpx", 22, LOOKUP)

        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(t), FadeOut(VGroup(n12, gt_tag, sys_tag)), caption_extra(tr, False),
                      FadeIn(ill, shift=LEFT * 0.1), run_time=0.6)
            self.play(row0.animate.shift(UP * dy[0]), std_g.animate.shift(UP * dy[1]),
                      VGroup(local_row, local_jars).animate.shift(UP * dy[2]),
                      VGroup(apt_row, apt_jars).animate.shift(UP * dy[3]), run_time=0.9)
            d_jar.move_to(apt_jars[0]).shift(LEFT * (apt_jars[1].get_x() - apt_jars[0].get_x()))
            d_tag = VGroup(mono("httpx 0.23.3", 22, INK), label("(apt's copy)", 22, S.GREY)).arrange(RIGHT, buff=0.15)
            d_tag.next_to(d_jar, UP, buff=0.14)
            if d_tag.get_right()[0] > 6.3:
                d_tag.shift(LEFT * (d_tag.get_right()[0] - 6.3))
            vo.wait_until("an older httpx")
            self.play(FadeIn(d_jar, shift=DOWN * 0.2), FadeIn(d_tag, shift=DOWN * 0.1), run_time=0.7)
            vo.wait_until("for some system tool")
            self.play(Indicate(apt_row[1], color=SYSTEM, scale_factor=1.05), Indicate(d_jar, color=SYSTEM,
                                                                                   scale_factor=1.4),
                      run_time=0.9)

            vo.wait_until("Our googletrans needs")
            hx_tag = mono("httpx 0.28.1", 22, INK).next_to(hx_jar, UP, buff=0.14)
            need = label("googletrans needs httpx ≥ 0.27.2", 22, S.GREY)
            need.next_to(hx_tag, UP, buff=0.14)
            need.shift(RIGHT * min(0, 6.3 - need.get_right()[0]))
            self.play(FadeIn(need, shift=DOWN * 0.1), Indicate(gt_jar, color=S.WHITE, scale_factor=1.3),
                      run_time=0.8)
            vo.wait_until("so pip would add")
            self.play(Indicate(hx_jar, color=SYSTEM, scale_factor=1.5), FadeIn(hx_tag, shift=UP * 0.15),
                      run_time=0.8)
            vo.wait_until("on the higher shelf")
            self.play(Indicate(local_row[1], color=SYSTEM, scale_factor=1.05), run_time=0.8)

            vo.wait_until("Python would find")
            # the query rides just above the light and lands beside the jar it finds
            lt7 = light_band(B4W[0])
            lt7_end = light_band(B4W[2])
            look7.move_to([hx_tag.get_left()[0] - 0.6 - look7.width / 2, hx_tag.get_y(), 0])
            look7.shift(UP * (lt7.get_y() - lt7_end.get_y()))
            self.play(FadeIn(lt7), FadeIn(look7, shift=DOWN * 0.1), run_time=0.4)
            self.play(VGroup(lt7, look7).animate.shift(DOWN * (lt7.get_y() - lt7_end.get_y())), run_time=1.4,
                      rate_func=linear)
            self.play(Indicate(hx_jar, color=LOOKUP, scale_factor=1.6), run_time=0.7)
            vo.wait_until("and hide the one")
            hidden = tag("hidden", ERR)
            hidden.next_to(d_tag, LEFT, buff=0.25)
            self.play(d_jar.animate.set_opacity(0.3), d_tag.animate.set_opacity(0.35),
                      FadeIn(hidden, shift=RIGHT * 0.1), run_time=0.7)
            vo.wait_until("for every program")
            self.play(FadeIn(caption7, shift=UP * 0.1), run_time=0.7)
            vo.wait_until("not just ours")
            self.play(Indicate(caption7, color=S.WHITE, scale_factor=1.04), run_time=0.8)
            vo.wait_until("That's what the flag breaks")
            self.play(Indicate(hidden.text, color=ERR, scale_factor=1.3), Indicate(d_jar, color=ERR, scale_factor=1.3),
                      run_time=0.8)

        # ========================================================== 8 · the README is fair about it
        rows = VGroup(*[label(s, 22, INK) for s in TIP56]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        card = readme_card(56, rows, " (tip after step 8)")
        card.move_to([0, 0.15, 0])
        hl1 = VGroup(*[hl_bar(text_span(rows[3], TIP56[3], "We use it here"), TURN, 0.28),
                       hl_bar(text_span(rows[4], TIP56[4], "deliberately as a quick demonstration"), TURN, 0.28)])
        nxt = VGroup(hl_bar(text_span(rows[4], TIP56[4], "the next walkthrough uses uv"), VENV, 0.2),
                     hl_bar(text_span(rows[5], TIP56[5], "to keep project packages isolated."), VENV, 0.2))
        scrim = Rectangle(width=13.2, height=6.5, stroke_width=0).set_fill(S.BG, 0.72)  # under the tracker
        scrim.move_to([0, -0.3, 0])
        scene7 = VGroup(lt7, look7, d_jar, d_tag, hidden, need, hx_tag, caption7)

        with self.voiceover(SAY[8]) as vo:
            self.play(FadeIn(scrim), FadeIn(card, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("deliberately")
            self.play(LaggedStart(*[FadeIn(b) for b in hl1], lag_ratio=0.4), run_time=0.8)
            vo.wait_until("as a quick demonstration")
            self.play(Indicate(hl1, color=TURN, scale_factor=1.03), run_time=0.8)
            vo.wait_until("and the next walkthrough")
            self.play(LaggedStart(*[FadeIn(b) for b in nxt], lag_ratio=0.4), run_time=0.9)

        # ========================================================== 9 · ponder: two projects, one shelf
        s_board = Line(LEFT * 2.7, RIGHT * 2.7, color=SYSTEM, stroke_width=6).set_y(SLOT_BOARD_Y)
        s_label = mono("/usr/local/… (pip's)", 24, SYSTEM)
        s_label.next_to(s_board, UP, buff=0.08).align_to(s_board, LEFT)
        slot = dashed_jar(SYSTEM, 0.6)
        slot.next_to(s_board, UP, buff=0.04).align_to(s_board, RIGHT).shift(LEFT * 0.3)
        slot_tag = name_tag(slot, "httpx", INK, 24)

        students = []
        for side, who, want in ((-1, "classmate", "httpx 0.13"), (1, "you", "httpx 0.28")):
            icon = person_icon(S.GREY, 1.3).move_to([side * 4.85, 1.25, 0])
            who_t = label(who, 26, S.GREY).next_to(icon, DOWN, buff=0.15)
            req = chip(want, S.GREY, size=24, font=MONO).next_to(icon, UP, buff=0.25)
            students.append((icon, who_t, req))
        (icon_l, who_l, req_l), (icon_r, who_r, req_r) = students
        arr_l = Arrow(req_l.get_right(), slot_tag.get_left(), buff=0.15, color=S.GREY, stroke_width=3,
                      max_tip_length_to_length_ratio=0.06)
        arr_r = Arrow(req_r.get_left(), slot_tag.get_right(), buff=0.15, color=S.GREY, stroke_width=3,
                      max_tip_length_to_length_ratio=0.12)
        others = VGroup(*[j for j in local_jars if j is not hx_jar])

        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(VGroup(card, hl1, nxt, scrim, scene7, row0, std_g, apt_row, apt_jars, others)),
                      run_time=0.6)
            self.play(Transform(local_row[0], s_board), Transform(local_row[1], s_label),
                      ReplacementTransform(hx_jar, slot), FadeIn(slot_tag, shift=DOWN * 0.1), run_time=1.0)
            vo.wait_until("A classmate's project")
            self.play(FadeIn(VGroup(icon_l, who_l), shift=UP * 0.15), run_time=0.6)
            vo.wait_until("needs httpx 0.13")
            self.play(FadeIn(req_l, shift=DOWN * 0.15), run_time=0.6)
            vo.wait_until("and yours needs")
            self.play(FadeIn(VGroup(icon_r, who_r), shift=UP * 0.15), run_time=0.6)
            vo.wait_until("needs httpx 0.28")
            self.play(FadeIn(req_r, shift=DOWN * 0.15), run_time=0.6)
            vo.wait_until("Both install system-wide")
            self.play(GrowArrow(arr_l), GrowArrow(arr_r), run_time=0.7)
            self.play(Indicate(VGroup(slot, slot_tag), color=SYSTEM, scale_factor=1.15), run_time=0.8)
            vo.wait_until("What happens?")
            self.play(Wiggle(slot_tag, scale_value=1.2), run_time=0.8)

        q = ponder_card(PONDER_Q)
        q.move_to([0, -3.45 + q.height / 2, 0])
        self.play(FadeIn(q, scale=0.95), run_time=0.6)
        bar = q[3]
        self.play(bar.animate(rate_func=linear).become(bar.copy().scale(0.001, about_point=bar.get_start())),
                  run_time=8)

        # ========================================================== 10 · the last install wins
        DY10 = 0.8                     # the picture settles into the room the ponder card leaves
        picture = VGroup(local_row[0], local_row[1], slot, slot_tag, icon_l, who_l, req_l, icon_r, who_r, req_r)
        j28, j13 = jar(SYSTEM, 0.6).move_to(slot), jar(SYSTEM, 0.6).move_to(slot)
        tag28 = name_tag(slot, "httpx 0.28", INK, 24)
        tag13 = name_tag(slot, "httpx 0.13", INK, 24)
        VGroup(j28, j13, tag28, tag13).shift(DOWN * DY10)
        caption10 = label("one shelf · the last install wins, for everyone", 28, INK).move_to([0, -0.75 - DY10, 0])

        with self.voiceover(SAY[10]) as vo:
            self.play(FadeOut(q), FadeOut(VGroup(arr_l, arr_r)), picture.animate.shift(DOWN * DY10), run_time=0.6)
            vo.wait_until("only one shelf")
            self.play(Indicate(VGroup(local_row[0], local_row[1]), color=SYSTEM, scale_factor=1.05), run_time=0.8)
            vo.wait_until("room for only one")
            self.play(ReplacementTransform(req_r, j28, path_arc=PI / 3), FadeOut(slot),
                      Transform(slot_tag, tag28), run_time=1.0)
            vo.wait_until("The last install wins")
            # the classmate's jar arrives from the left and knocks yours off as it lands
            self.play(LaggedStart(ReplacementTransform(req_l, j13, path_arc=-PI / 3, run_time=0.8),
                                  AnimationGroup(j28.animate.shift(RIGHT * 1.3 + DOWN * 1.2).rotate(-1.4).set_color(ERR),
                                                 Transform(slot_tag, tag13), run_time=0.55),
                                  lag_ratio=0.8))
            self.play(FadeOut(j28, shift=DOWN * 0.4), run_time=0.3)
            vo.wait_until("for everyone")
            self.play(FadeIn(caption10, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("one of the two projects breaks")
            self.play(icon_r.animate.set_color(ERR), who_r.animate.set_color(ERR), run_time=0.6)

        self.wait(0.3)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.wait(0.2)
