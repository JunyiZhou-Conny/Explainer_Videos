"""S12 · Activation is just PATH (part 2: the real .venv, source activate, the GREEN door, the runs).

Beats (script.md "## S12", one voiceover block each):
 0  TRACKER B9 · extra. A 12-row terminal: `ls -la .venv/bin` (extra) -> 11-venv-bin.txt lines 5, …,
    13, 15-16, 18-19, 21 (wrapped: line 18 folds onto 3 rows, so with the ghost row the 12 rows are
    full and `activate` stays on screen). The S08 three-part card returns top-right. Line 18 (the
    python link) GREEN + badge "1 · the link", card part 1 ticks; art/httpx/idna/translate get a GREY
    bracket "launchers from the packages"; a RED-struck ghost row `pip` under the listing.
 1  The terminal clears to 9 rows: `cat .venv/pyvenv.cfg` (extra) -> 10-pyvenv.txt lines 2-7
    (wrapped). Line 2 GREY + "a folder"; line 6 badge "3" (card part 3 ticks); line 7 YELLOW; above
    the terminal, 22-syspath-venv.txt line 6 with badge "2 · site-packages" (card part 2 ticks).
 2  TRACKER B10. The terminal clears to a 3-row strip: `source .venv/bin/activate` -> the prompt
    gets `(app)` (GREEN); ▶ your turn (on the new prompt row: the command row has no room). The new
    prompt is copied up, enlarged, (app) boxed GREEN. README card line 92 "(e.g. (simple-translate)
    $)" top-left, YELLOW note "→ (app)", GREY "erratum"; CODE(pyproject.toml: 2) beside it (no room
    under it), "app" and (app) light up together.
 3  V3 above the strip: ~/.local/bin (PURPLE), /usr/local/bin, /usr/bin, /bin, … (12-python-before
    lines 3-8). The `python` figure knocks on every door -> RED "not found". PANEL activate lines
    97-98; line 98 GREEN; the GREEN `.venv/bin` door slides in at the front; python walks in.
 4  TRACKER B10 · extra. The strip grows to 6 rows: `which python`, `python --version` (+ "at the
    time of recording", GREY "Debian 13: Python 3.13.5" from debian13-part-b), `which pip` -> no
    output, RED "nothing" on the prompt row that comes back; a pip figure walks past every door.
 5  The terminal goes. README card line 92 "python and pip resolve to the venv's binaries", YELLOW
    "a uv venv has no pip", GREY "erratum". The doors become an illustration "a machine with a
    system pip": /usr/bin turns ORANGE, pip walks past the GREEN door and in at /usr/bin; RED chip
    "externally-managed-environment". GREEN `uv add <package>` -> pyproject.toml and uv.lock.
 6  Card "after activation" (13-activate.txt lines 5-8) and a checklist (4 GREEN items, a 5th
    RED-struck). A second terminal "new SSH window" (bottom strip): no (app), its PATH row has no
    GREEN door, "activation: this shell only"; `cd simple-translate`, `source .venv/bin/activate`
    -> (app), the GREEN mini door slides in.
 7  TRACKER B11. That window grows into the 12-row terminal: `python cli.py` (14-run-default.txt
    2-15), the es and fr runs (15/16-run-*.txt 12-15), each Output line GREEN; "real capture ·
    2026-10-12" on the frame; GREY note "copy from the README, quotes included"; ▶ your turn.
 8  TRACKER B11 · extra. The terminal shrinks to the strip; two GREEN chips with "extra" and "no
    activation needed": `uv run python cli.py`, `.venv/bin/python cli.py` (no output).
 9  11-venv-bin.txt line 5 returns with "not executable"; a child-shell bubble gets the GREEN door
    and pops, the parent's row is unchanged (the S09 picture). Fade out.
"""

import numpy as np
from manim import *

from explainer import style as S
from explainer.components import person_icon
from explainer.devops import (MONO, OUTPUT, box, check_mark, chip, code_panel, code_span, cross_mark,
                              file_glyph, glyph_range, label, line_bar, mono, mono_line, step_badge,
                              substring, tag)
from explainer.scene import VoiceScene

from common import (ERR, INK, LOOKUP, NARRATION, P_HOME, P_REPO, P_VENV, SYSTEM, TURN, UV, VENV,
                    PathDoors, capture, excerpt, illustration_tag, recorded_tag, term, tracker_b,
                    your_turn)

SAY = NARRATION["S12"]
PB, PB13 = "debian12-part-b", "debian13-part-b"

# ------------------------------------------------------------------ commands
LS = "ls -la .venv/bin"
CAT = "cat .venv/pyvenv.cfg"
ACTIVATE = "source .venv/bin/activate"           # README spelling
CD = "cd simple-translate"
RUN_IT = "python cli.py"
RUN_ES = 'python cli.py -t "Good morning. It is a good morning for cheese." -s "en" -d "es"'
RUN_FR = 'python cli.py -t "Good afternoon. Would you like some cheese?" -s "en" -d "fr"'

# ------------------------------------------------------------------ real outputs (pick index = file line - 1)
_bin = capture("11-venv-bin", PB)
assert _bin.cmd == LS
L5 = _bin.pick(4)[0]
LS_OUT = [L5, "…", *_bin.pick(12), *_bin.pick((14, 15)), *_bin.pick((17, 18)), *_bin.pick(20)]
assert L5.endswith(" activate") and LS_OUT[2].endswith(" art") and LS_OUT[6].endswith(" python3 -> python")
assert "python -> /home/student/.local/share/uv/python/cpython-3.15" in LS_OUT[5]
assert LS_OUT[-1].endswith(" translate")

_cfg = capture("10-pyvenv", PB)
assert _cfg.cmd == CAT
CFG_OUT = _cfg.pick((1, 6))                                                  # file lines 2-7
assert CFG_OUT[0].startswith("home = ") and CFG_OUT[4] == "include-system-site-packages = false"
assert CFG_OUT[5] == "prompt = app" and 65 < len(CFG_OUT[0]) <= 130

SITE = capture("22-syspath-venv", PB).pick(5)[0]                             # file line 6
assert SITE == "/home/student/simple-translate/.venv/lib/python3.15/site-packages"

_path = capture("12-python-before", PB).pick((2, 7))                         # file lines 3-8
assert _path == ["/home/student/.local/bin", "/usr/local/bin", "/usr/bin", "/bin",
                 "/usr/local/games", "/usr/games"]
DOORS = ["~/.local/bin", "/usr/local/bin", "/usr/bin", "/bin", "…"]          # the two games folders: …

_act = capture("25-activate-file", PB).pick(9, 10)                           # file lines 10-11
assert _act[0].startswith("97:") and _act[1].startswith("98:")
ACT_SRC = "\n".join(s.split(":", 1)[1] for s in _act)                        # activate lines 97-98
assert ACT_SRC == '_OLD_VIRTUAL_PATH="$PATH"\nPATH="$VIRTUAL_ENV/bin:$PATH"'

_chk = capture("13-activate", PB).lines
WHICH_PY, PY_VER = _chk[0], _chk[1]                                          # file lines 2, 3
assert WHICH_PY == "/home/student/simple-translate/.venv/bin/python" and PY_VER == "Python 3.15.0"
AFTER = _chk[3:7]                                                            # file lines 5-8
assert AFTER[0].endswith("/.venv/bin") and AFTER[3].startswith("VIRTUAL_ENV=")
PY_VER13 = capture("13-activate", PB13).lines[1]                             # file line 3
assert PY_VER13 == "Python 3.13.5"

RUN_OUT = capture("14-run-default", PB).pick((1, 14))                        # file lines 2-15
ES_OUT = capture("15-run-es", PB).pick((11, 14))                             # file lines 12-15
FR_OUT = capture("16-run-fr", PB).pick((11, 14))                             # file lines 12-15
assert RUN_OUT[-1] == "Output: Adoro il formaggio" and ES_OUT[-1].startswith("Output: Buen")
assert FR_OUT[-1].startswith("Output: Bon") and FR_OUT[-2].startswith("Input: ")

NAME2 = excerpt("pyproject.toml", 2, 2)
assert NAME2 == 'name = "app"'

PARTS = ["bin/python", "lib/python3.X/site-packages/", "pyvenv.cfg"]        # the S08 card

# ------------------------------------------------------------------ layout
TRACK_LEFT, TRACK_TOP = -6.5, 3.5
BOTTOM = -3.5            # terminal bottom edge
DOOR_TOP = 2.2           # top of the PATH door frames
DOOR_H = 0.9


def place_tracker(tr):
    tr.shift(np.array([TRACK_LEFT - tr.get_left()[0], TRACK_TOP - tr.get_top()[1], 0]))
    return tr


def caption_extra(tr, on: bool = True):
    """The tracker caption with (or without) ' · extra' while a non-README command is on screen."""
    k = tr.k
    s = f"step {k} of {len(tr.steps)}: {tr.steps[k - 1]}"
    new = label(s + " · extra", tr.size, tr.hi_color, t2c={"· extra": S.GREY}) if on else \
        label(s, tr.size, tr.hi_color)
    new.next_to(tr.dots, RIGHT, buff=0.25)
    return Transform(tr.caption, new)


def short_extra():
    return tag("extra", S.GREY)


def row_extra() -> VGroup:
    """A compact 'extra' tag (20 pt, one row high) for a command row too long for the house tag
    (`(app) …$ python --version` leaves 1.19 of the 12.6 terminal's width)."""
    t = label("extra", 20, S.GREY)
    h = 0.34
    b = RoundedRectangle(width=t.width + 0.3, height=h, corner_radius=h / 2, stroke_color=S.GREY,
                         stroke_width=2).set_fill(S.BG, 0.92)
    t.move_to(b)
    return VGroup(b, t)


def readme_card(line_no: int, body: VGroup, width: float | None = None) -> VGroup:
    head = VGroup(mono("README.md", 20, S.GREY), label(f"· line {line_no}", 20, S.GREY))
    head.arrange(RIGHT, buff=0.12)
    inner = VGroup(head, body).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    frame = box(width or inner.width + 0.5, inner.height + 0.4, S.GREY, fill=S.GREY_DARKER,
                fill_opacity=1)
    inner.move_to(frame).align_to(frame, LEFT).shift(RIGHT * 0.25)
    g = VGroup(frame, inner)
    g.frame, g.body = frame, body
    return g


def figure(word: str) -> VGroup:
    """The walking command: a small PINK figure carrying the word (as in S09)."""
    p = person_icon(LOOKUP, 0.42)
    w = mono(word, 26, LOOKUP)
    g = VGroup(p, w).arrange(RIGHT, buff=0.1, aligned_edge=DOWN)
    return g


def mini_door(color) -> VGroup:
    f = RoundedRectangle(width=0.36, height=0.54, corner_radius=0.04, stroke_color=color,
                         stroke_width=2.5).set_fill(color, 0.15 if color == S.GREY else 0.4)
    k = Dot(radius=0.03, color=color).move_to(f.get_right() + LEFT * 0.07)
    return VGroup(f, k)


def mini_path(colors) -> VGroup:
    """'PATH' and a row of mini doors (a shell's PATH at a glance). .doors"""
    doors = VGroup(*[mini_door(c) for c in colors]).arrange(RIGHT, buff=0.12)
    g = VGroup(mono("PATH", 22, LOOKUP), doors).arrange(RIGHT, buff=0.25)
    g.doors = doors
    return g


def parts_card() -> VGroup:
    """The S08 corner card, back: the venv's three parts, GREY badges until each one is found.
    .rows .badges .lit (GREEN badges) .ticks (check marks)"""
    rows, lit, ticks = VGroup(), [], []
    for n, p in enumerate(PARTS, start=1):
        b = step_badge(n, S.GREY_DARK, size=20, radius=0.17)
        rows.add(VGroup(b, mono(p, 20, INK)).arrange(RIGHT, buff=0.18))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.06)
    frame = box(rows.width + 0.95, rows.height + 0.22, S.GREY, fill_opacity=0.08)
    rows.move_to(frame).align_to(frame, LEFT).shift(RIGHT * 0.2)
    for n, r in enumerate(rows, start=1):
        lit.append(step_badge(n, VENV, size=20, radius=0.17).move_to(r[0]))
        ticks.append(check_mark(0.26, VENV).move_to([frame.get_right()[0] - 0.33, r.get_y(), 0]))
    g = VGroup(frame, rows)
    g.frame, g.rows, g.lit, g.ticks = frame, rows, lit, ticks
    shift = np.array([6.5 - frame.get_right()[0], 3.58 - frame.get_top()[1], 0])
    for m in (g, *lit, *ticks):
        m.shift(shift)
    return g


def row_bar(line, color, opacity=0.2, pad=0.08):
    """A translucent bar behind a terminal line's glyphs."""
    g = line.glyphs
    return Rectangle(width=g.width + 2 * pad, height=line.strut.height + 0.04, stroke_width=0) \
        .set_fill(color, opacity).move_to([g.get_center()[0], line.strut.get_center()[1], 0])


def under(m, color, buff=0.06, stroke=3):
    return Line(m.get_corner(DL) + DOWN * buff, m.get_corner(DR) + DOWN * buff, color=color,
                stroke_width=stroke)


def file_chip(name: str, color) -> VGroup:
    g = VGroup(file_glyph(0.36, color), mono(name, 24, color)).arrange(RIGHT, buff=0.15)
    frame = box(g.width + 0.45, g.height + 0.3, color, fill_opacity=0.08).move_to(g)
    return VGroup(frame, g)


class Activate(VoiceScene):
    # ------------------------------------------------------------- terminal helpers
    def pin(self, line, mob, run_time=0.4, anim=None, behind=False):
        """Show `mob` beside a terminal line and make it part of that line (it scrolls with it).
        The line is re-added whole (an earlier Indicate on some of its glyphs splits it)."""
        self.play(anim or FadeIn(mob, shift=LEFT * 0.1), run_time=run_time)
        self.remove(mob)
        if behind:
            line.submobjects.insert(0, mob)
        else:
            line.add(mob)
        self.add(line)
        return mob

    def bare_prompt(self, t):
        """The prompt returns (no output): a prompt line with nothing typed yet."""
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

    def resize(self, t, rows, keep=None, run_time=0.8, extra=()):
        """Grow or shrink the terminal to `rows` (bottom edge fixed). It keeps the lines with
        indices `keep` (default: the last ones that fit), in order, and fades the rest."""
        ref = term(prompt=t.prompt, rows=rows)
        ref.shift(np.array([t.box.get_center()[0] - ref.box.get_center()[0],
                            BOTTOM - ref.box.get_bottom()[1], 0]))
        lines = list(t.lines.submobjects)
        if keep is None:
            keep = list(range(max(0, len(lines) - rows), len(lines)))
        kept = [lines[i] for i in keep]
        gone = [ln for i, ln in enumerate(lines) if i not in keep]
        anims = [Transform(t.box, ref.box), Transform(t.bar, ref.bar),
                 t.dots.animate.move_to(ref.dots), t.title.animate.move_to(ref.title)]
        for j, ln in enumerate(kept):
            anims.append(ln.animate.shift(ref._slot(j) - ln.strut.get_corner(UL)))
        if gone:
            anims.append(FadeOut(VGroup(*gone)))
        self.play(*anims, *extra, run_time=run_time)
        t.lines.submobjects = kept
        t.rows = rows
        return t

    def walk(self, fig, doors, upto, step=0.3, knock=True, enter=None, knock_time=0.32):
        """Walk the figure along the doors 0..upto (knocking PINK on each), then enter door
        `enter` (it lights up in its own colour) if given."""
        for i in range(upto + 1):
            d = doors[i]
            self.play(fig.animate.next_to(d.frame, UP, buff=0.12), run_time=step)
            if knock and i != enter:
                col = d.frame.get_stroke_color()
                self.play(Wiggle(d.frame.set_stroke(LOOKUP), scale_value=1.04, rotation_angle=0.015 * TAU,
                                 n_wiggles=2), run_time=knock_time)
                d.frame.set_stroke(col)
        if enter is not None:
            d = doors[enter]
            # the door opens (its knob goes) and the figure steps in; its word stays >= 20 pt
            k = 0.77
            assert fig.width * k <= d.frame.width - 0.1, "figure wider than the door"
            self.play(fig.animate.scale(k).move_to(d.frame), d.frame.animate.set_fill(d.color, 0.45),
                      d[1].animate.set_fill(opacity=0), run_time=0.5)

    # ------------------------------------------------------------- the scene
    def construct(self):
        assert len(SAY) == 10, f"S12 has {len(SAY)} SAY lines; this scene times 10"

        tr = place_tracker(tracker_b(9))
        tr.caption.become(label(f"step 9 of 12: {tr.steps[8]} · extra", tr.size, tr.hi_color,
                                t2c={"· extra": S.GREY}).next_to(tr.dots, RIGHT, buff=0.25))

        # ========================================================== 0 · ls -la .venv/bin
        t = term(prompt=P_REPO, rows=12)
        t.shift(np.array([0 - t.box.get_center()[0], BOTTOM - t.box.get_bottom()[1], 0]))
        frame0 = VGroup(t.box, t.bar, t.dots, t.title)
        card = parts_card()

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.1), FadeIn(frame0), run_time=0.7)
            vo.wait_until("as promised")
            self.play(FadeIn(card, shift=LEFT * 0.3), run_time=0.7)
            vo.wait_until("This extra command")
            cmd = t.type(self, LS, type_time=0.8)
            ex = short_extra().next_to(cmd.strut, RIGHT, buff=0.35)
            self.pin(cmd, ex, run_time=0.3)
            out = t.print(self, LS_OUT, run_time=0.8, wrap=True)
            n_py = -(-len(LS_OUT[5]) // t.max_chars)
            py_rows = out[5:5 + n_py]
            art, httpx, idna, transl = out[2], out[3], out[4], out[-1]

            vo.wait_until("python, a link")
            bars = [row_bar(r, VENV, 0.2) for r in py_rows]
            b1 = VGroup(step_badge(1, VENV, size=20, radius=0.17), label("the link", 24, VENV))
            b1.arrange(RIGHT, buff=0.15).next_to(py_rows[-1].glyphs, RIGHT, buff=0.45)
            b1.match_y(py_rows[-1].strut)
            self.play(*[FadeIn(b) for b in bars], FadeIn(b1, shift=LEFT * 0.15),
                      Transform(card.rows[0][0], card.lit[0]), Create(card.ticks[0]),
                      run_time=0.7)
            for r, b in zip(py_rows, bars):
                self.remove(b)
                r.submobjects.insert(0, b)
                self.add(r)
            arrow_part = substring(py_rows[0], "->")
            self.play(Indicate(arrow_part, color=VENV, scale_factor=1.4), run_time=0.7)
            self.add(py_rows[0])

            # the launchers: a GREY bracket (brace on art/httpx/idna, a lead from translate)
            names = [glyph_range(r, r.text.rindex(r.text.split()[-1])) for r in (art, httpx, idna, transl)]
            boxes = [SurroundingRectangle(n, buff=0.05, corner_radius=0.05, color=S.GREY, stroke_width=2)
                     for n in names]
            x_b = max(r.glyphs.get_right()[0] for r in (art, httpx, idna)) + 0.12
            ref = Line([x_b, art.strut.get_top()[1], 0], [x_b, idna.strut.get_bottom()[1], 0])
            brace = Brace(ref, RIGHT, buff=0.04, color=S.GREY)
            lab_l = VGroup(label("launchers from", 22, S.GREY), label("the packages", 22, S.GREY))
            lab_l.arrange(DOWN, aligned_edge=LEFT, buff=0.06).next_to(brace, RIGHT, buff=0.12)
            x_lead = 6.18                                  # clear of the python link's GREEN bar
            lead = VMobject(stroke_color=S.GREY, stroke_width=2).set_points_as_corners([
                boxes[3].get_right(), [x_lead, boxes[3].get_y(), 0],
                [x_lead, lab_l.get_bottom()[1] - 0.04, 0], [lab_l.get_right()[0] + 0.08, lab_l.get_bottom()[1] - 0.04, 0]])
            launchers = VGroup(*boxes, brace, lab_l, lead)
            self.play(*[Create(b) for b in boxes], GrowFromCenter(brace), FadeIn(lab_l), Create(lead),
                      run_time=0.6)

            # the ghost row: no pip
            col = len(transl.text) - len(transl.text.split()[-1])
            ghost = mono_line(" " * col + "pip", t.size, S.GREY)
            ghost.shift(t._slot(len(t.lines)) - ghost.strut.get_corner(UL))
            gbox = DashedVMobject(SurroundingRectangle(ghost.glyphs, buff=0.07, corner_radius=0.05,
                                                       stroke_width=2, color=S.GREY), num_dashes=16)
            strike = Line(gbox.get_left() + LEFT * 0.08, gbox.get_right() + RIGHT * 0.08, color=ERR,
                          stroke_width=4)
            nopip = tag("no pip", ERR).next_to(gbox, RIGHT, buff=0.3)
            vo.wait_until("and, notice")
            self.play(FadeIn(ghost.glyphs, shift=UP * 0.1), Create(gbox), run_time=0.4)
            vo.wait_until("no pip")
            self.play(Create(strike), FadeIn(nopip, shift=LEFT * 0.1), run_time=0.4)
            ghost_all = VGroup(ghost.glyphs, gbox, strike, nopip)
        self.wait(0.7)                                   # let "no pip" land before the terminal clears

        # ========================================================== 1 · cat .venv/pyvenv.cfg
        site = mono_line(SITE, 22, S.GREY)
        site_part = substring(site, ".venv/lib/python3.15/site-packages")
        site_part.set_color(VENV)
        t9 = term(prompt=P_REPO, rows=9)
        t9.shift(np.array([0, BOTTOM - t9.box.get_bottom()[1], 0]))
        site.move_to([0, t9.box.get_top()[1] + 0.45, 0])
        site_cap = label("sys.path inside the venv · its last entry", 20, S.GREY)
        site_cap.next_to(site, UP, buff=0.2).align_to(site, LEFT)
        b2 = VGroup(step_badge(2, VENV, size=20, radius=0.17), label("site-packages", 24, VENV))
        b2.arrange(RIGHT, buff=0.15)
        b2.move_to([0, site_cap.get_y(), 0]).align_to(site_part, RIGHT)
        sp_ul = under(site_part, VENV)

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(launchers, ghost_all, b1)), run_time=0.4)
            t.clear(self, run_time=0.3)
            self.resize(t, 9, run_time=0.6)
            cmd = t.type(self, CAT, type_time=0.7)
            ex = short_extra().next_to(cmd.strut, RIGHT, buff=0.35)
            self.pin(cmd, ex, run_time=0.3)
            out = t.print(self, CFG_OUT, run_time=0.7, wrap=True)
            home_rows = list(out[:2])                                 # line 2 folds onto two rows
            inc = t.find("include-system-site-packages")
            prm = t.find("prompt = app")

            vo.wait_until("home is")
            hb = [row_bar(r, S.GREY, 0.22) for r in home_rows]
            folder = tag("a folder", S.GREY).next_to(home_rows[-1].glyphs, RIGHT, buff=0.4)
            folder.match_y(home_rows[-1].strut)
            self.play(*[FadeIn(b) for b in hb], FadeIn(folder, shift=LEFT * 0.1), run_time=0.5)
            for r, b in zip(home_rows, hb):
                self.remove(b)
                r.submobjects.insert(0, b)
                self.add(r)
            self.play(Indicate(substring(home_rows[-1], "/bin"), color=S.WHITE, scale_factor=1.3), run_time=0.6)
            self.add(home_rows[-1])

            vo.wait_until("include system site")
            b3 = step_badge(3, VENV, size=20, radius=0.17).next_to(inc.glyphs, RIGHT, buff=0.4).match_y(inc.strut)
            self.play(FadeIn(b3, scale=0.6), Transform(card.rows[2][0], card.lit[2]),
                      Create(card.ticks[2]), substring(inc, "false").animate.set_color(VENV), run_time=0.6)
            self.add(inc)

            vo.wait_until("and the prompt is")
            yb = row_bar(prm, TURN, 0.25)
            self.pin(prm, yb, run_time=0.4, anim=FadeIn(yb), behind=True)
            self.play(Indicate(substring(prm, "app"), color=TURN, scale_factor=1.3), run_time=0.6)
            self.add(prm)

            vo.wait_until("All three parts")
            self.play(FadeIn(site_cap), FadeIn(site, shift=DOWN * 0.1), run_time=0.5)
            self.play(FadeIn(b2, shift=DOWN * 0.1), Create(sp_ul),
                      Transform(card.rows[1][0], card.lit[1]), Create(card.ticks[1]), run_time=0.6)
            self.play(Indicate(card.frame, color=VENV, scale_factor=1.04), run_time=0.7)

        # ========================================================== 2 · source .venv/bin/activate
        body92 = VGroup(
            label("changes your shell prompt to show", 24, INK), label("the venv name as a prefix", 24, INK),
            VGroup(label("(e.g.", 24, INK), mono("(simple-translate) $", 24, INK), label(")", 24, INK))
            .arrange(RIGHT, buff=0.12))
        body92.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        note_app = VGroup(label("→", 26, TURN), mono("(app)", 26, TURN)).arrange(RIGHT, buff=0.15)
        card92 = readme_card(92, body92, width=body92.width + note_app.width + 1.2)
        card92.move_to([0, 1.65, 0]).align_to([-6.2, 0, 0], LEFT)
        note_app.next_to(body92[2], RIGHT, buff=0.45)
        eg = body92[2][1]
        err92 = tag("erratum", S.GREY).move_to(card92.frame.get_corner(UR) + np.array([-0.85, 0, 0]))
        eg_ul = under(eg, TURN)
        p2 = code_panel(NAME2, "pyproject.toml", 2, language="toml", font_size=24)
        p2.move_to([0, card92.get_y() - 0.1, 0]).align_to([6.2, 0, 0], RIGHT)
        app_word = code_span(p2.code, 0, '"app"')

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(site, site_cap, b2, sp_ul, b3, folder)),
                      FadeOut(VGroup(card, *card.ticks)), tr.goto(10), run_time=0.5)
            t.clear(self, run_time=0.3)
            # the 9-row terminal stays while the command is typed (nothing else needs the frame
            # yet); it shrinks to the strip as the new prompt is lifted out of it
            vo.wait_until("source dot venv")
            src = t.type(self, ACTIVATE, type_time=1.0)
            t.set_prompt(P_VENV)
            p_venv = self.bare_prompt(t)
            vo.wait_until("Pause and run")
            yt = your_turn().next_to(p_venv.glyphs, RIGHT, buff=0.5)
            self.pin(p_venv, yt, run_time=0.4)
            self.play(Indicate(substring(src, ACTIVATE), color=TURN, scale_factor=1.06), run_time=0.8)
            self.add(src)
            vo.wait_until("Your prompt now")
            big = mono_line(P_VENV, 32, INK, t2c=t._prompt_colors(P_VENV)).move_to([0, -0.35, 0])
            app_p = substring(big, "(app)")
            app_box = SurroundingRectangle(app_p, buff=0.1, corner_radius=0.08, color=VENV, stroke_width=3)
            self.resize(t, 3, run_time=0.9, extra=[TransformFromCopy(p_venv.glyphs, big.glyphs)])
            self.play(Create(app_box), Indicate(app_p, color=VENV, scale_factor=1.25), run_time=0.8)
            vo.wait_until("The README's example")
            self.play(FadeIn(card92, shift=UP * 0.15), run_time=0.6)
            self.play(Create(eg_ul), FadeIn(err92, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("But uv names")
            self.play(FadeIn(note_app, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("and pyproject.toml calls")
            self.play(FadeIn(p2, shift=UP * 0.2), run_time=0.6)
            self.play(app_word.animate.set_color(VENV), run_time=0.4)
            self.play(Indicate(app_word, color=VENV, scale_factor=1.3), Indicate(app_p, color=VENV, scale_factor=1.3),
                      run_time=0.9)

        # ========================================================== 3 · V3: the GREEN door
        doors = PathDoors(DOORS, colors={"~/.local/bin": UV}, door_w=0.6, door_h=DOOR_H, gap=0.35, size=22)
        new_door = doors._door(".venv/bin", VENV)
        gap = doors.gap
        total = new_door.frame.width + gap + doors.width
        doors.shift(np.array([-doors.width / 2 - doors.doors[0].frame.get_left()[0],
                              DOOR_TOP - doors.doors[0].frame.get_top()[1], 0]))
        shift_old = (new_door.frame.width + gap) / 2
        left0 = -total / 2
        new_door.shift(np.array([left0 - new_door.frame.get_left()[0], DOOR_TOP - new_door.frame.get_top()[1], 0]))
        lr_y = doors.doors[0].label.get_bottom()[1] - 0.2
        path_lbl = mono("PATH", 24, LOOKUP)

        def lr_for(x0, x1):
            path_lbl.move_to([x0 + path_lbl.width / 2, lr_y, 0])
            a = Arrow(LEFT, RIGHT, color=LOOKUP, stroke_width=4, buff=0, tip_length=0.18,
                      max_tip_length_to_length_ratio=0.05)
            a.put_start_and_end_on(np.array([x0 + path_lbl.width + 0.2, lr_y, 0]), np.array([x1, lr_y, 0]))
            return a

        lr = lr_for(doors.get_left()[0], doors.get_right()[0])
        path_lbl0 = path_lbl.copy()
        lr_new = lr_for(left0, doors.get_right()[0] + shift_old)
        path_lbl1 = path_lbl.copy()
        path_lbl = path_lbl0

        actp = code_panel(ACT_SRC, ".venv/bin/activate", 97, language="bash", font_size=22)
        actp.move_to([0, lr_y - 0.36 - actp.height / 2, 0]).align_to([left0, 0, 0], LEFT)
        bar97, bar98 = line_bar(actp.code, 0, TURN, 0.2), line_bar(actp.code, 1, VENV, 0.2)
        venv_bin = code_span(actp.code, 1, "$VIRTUAL_ENV/bin")

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(card92, err92, eg_ul, note_app, p2, yt, big.glyphs, app_box)), run_time=0.5)
            p_venv.remove(yt)
            self.play(LaggedStart(*[FadeIn(d, shift=DOWN * 0.2) for d in doors.doors], lag_ratio=0.15),
                      FadeIn(path_lbl), GrowArrow(lr), run_time=1.0)
            vo.wait_until("Before activating")
            fig = figure("python").next_to(doors.doors[0].frame, UP, buff=0.12)
            self.play(FadeIn(fig, shift=DOWN * 0.2), run_time=0.3)
            self.walk(fig, doors.doors, len(doors.doors) - 1, step=0.22, knock_time=0.26)
            nf = label("not found", 26, ERR).move_to([doors.doors[2].frame.get_x(), lr_y - 0.42, 0])
            self.play(fig.animate.set_color(ERR), FadeIn(nf, shift=UP * 0.1), run_time=0.4)

            vo.wait_until("The activate script")
            self.play(FadeIn(actp, shift=UP * 0.15), run_time=0.6)
            self.play(FadeIn(bar97), run_time=0.4)
            vo.wait_until("then puts")
            self.play(FadeOut(fig), FadeOut(nf), FadeOut(bar97), FadeIn(bar98), venv_bin.animate.set_color(VENV), run_time=0.5)
            self.play(doors.doors.animate.shift(RIGHT * shift_old), Transform(lr, lr_new),
                      Transform(path_lbl, path_lbl1), run_time=0.5)
            self.play(FadeIn(new_door, shift=DOWN * 1.2), run_time=0.6)
            doors.doors.submobjects.insert(0, new_door)
            vo.wait_until("so python is found")
            fig = figure("python").next_to(new_door.frame, UP, buff=0.12)
            self.play(FadeIn(fig, shift=DOWN * 0.2), run_time=0.3)
            self.walk(fig, doors.doors, 0, step=0.2, knock=False, enter=0)

        # ========================================================== 4 · which python, python --version, which pip
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(actp, bar98, fig)), caption_extra(tr),
                      new_door.frame.animate.set_fill(VENV, 0.1), new_door[1].animate.set_fill(opacity=1),
                      run_time=0.5)
            self.resize(t, 6, run_time=0.6)
            l1 = self.type_cmd(t, "which python", 0.5)
            self.pin(l1, row_extra().next_to(l1.strut, RIGHT, buff=0.15), run_time=0.25)
            o1 = t.print(self, [WHICH_PY], run_time=0.3)[0]
            part = substring(o1, ".venv/bin")
            self.play(part.animate.set_color(VENV), Indicate(new_door.frame, color=VENV, scale_factor=1.08),
                      run_time=0.7)
            self.add(o1)

            vo.wait_until("and python reports")
            l2 = self.type_cmd(t, "python --version", 0.5)
            x2 = row_extra().next_to(l2.strut, RIGHT, buff=0.15)
            assert x2.get_right()[0] <= t.box.get_right()[0] - 0.1, "extra tag runs past the terminal"
            self.pin(l2, x2, run_time=0.25)
            o2 = t.print(self, [PY_VER], run_time=0.3)[0]
            rec = recorded_tag().next_to(o2.strut, RIGHT, buff=0.4)
            self.pin(o2, rec, run_time=0.4)
            vo.wait_until("on Debian 13")
            d13 = VGroup(tag("Debian 13", S.GREY), mono(PY_VER13, t.size, S.GREY)).arrange(RIGHT, buff=0.25)
            d13.next_to(rec, RIGHT, buff=0.4)
            self.pin(o2, d13, run_time=0.4)

            vo.wait_until("And which pip")
            l3 = self.type_cmd(t, "which pip", 0.4)
            ex3 = row_extra().next_to(l3.strut, RIGHT, buff=0.15)
            # the lookup first (pip walks past every door), then the empty answer
            pipf = figure("pip").next_to(doors.doors[0].frame, UP, buff=0.12)
            self.pin(l3, ex3, run_time=0.25, anim=AnimationGroup(FadeIn(ex3, shift=LEFT * 0.1),
                                                                 FadeIn(pipf, shift=DOWN * 0.2)))
            self.walk(pipf, doors.doors, len(doors.doors) - 1, step=0.1, knock=False)
            p_none = self.bare_prompt(t)
            nothing = tag("nothing", ERR).next_to(p_none.glyphs, RIGHT, buff=0.5)
            self.pin(p_none, nothing, run_time=0.35,
                     anim=AnimationGroup(FadeIn(nothing, shift=LEFT * 0.1), pipf.animate.set_color(ERR)))
        self.wait(0.6)                                   # let "nothing" land before the terminal goes

        # ========================================================== 5 · erratum: a uv venv has no pip
        dd = doors.doors
        usr_bin = dd[3]
        assert usr_bin.dir == "/usr/bin"
        body_a = label("(1) prepends .venv/bin/ to PATH so python and pip", 24, INK,
                       t2f={".venv/bin/": MONO, "PATH": MONO, "python": MONO, "pip": MONO})
        body_b = label("resolve to the venv's binaries", 24, INK)
        body5 = VGroup(body_a, body_b).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        card5 = readme_card(92, body5)
        card5.move_to([0, -1.2, 0]).align_to([-6.0, 0, 0], LEFT)
        err5 = tag("erratum", S.GREY).move_to(card5.frame.get_corner(UR) + np.array([-0.85, 0, 0]))
        pip_ul = under(text_part(body_a, "and pip"), TURN)
        nopip_note = label("a uv venv has no pip", 26, TURN).next_to(card5.frame, RIGHT, buff=0.4)
        ill = VGroup(illustration_tag(), label("a machine with a system pip", 22, S.GREY)).arrange(RIGHT, buff=0.25)
        ill.move_to([0, 3.25, 0]).align_to([6.5, 0, 0], RIGHT)
        refuse = chip("externally-managed-environment", ERR, size=22, font=MONO, fill_opacity=0.12)
        refuse.move_to([usr_bin.frame.get_x(), lr_y - 0.5, 0])          # clear of the PATH arrow
        if refuse.get_right()[0] > 6.4:
            refuse.shift(LEFT * (refuse.get_right()[0] - 6.4))
        uvadd = chip("uv add <package>", VENV, size=26, font=MONO).move_to([-3.4, -2.82, 0])
        f_toml = file_chip("pyproject.toml", INK).move_to([1.4, -2.5, 0])
        f_lock = file_chip("uv.lock", VENV).move_to([1.4, -3.22, 0]).align_to(f_toml, LEFT)
        a_toml = Arrow(uvadd.get_right(), f_toml.get_left(), buff=0.15, color=VENV, stroke_width=4,
                       max_tip_length_to_length_ratio=0.1)
        a_lock = Arrow(uvadd.get_right(), f_lock.get_left(), buff=0.15, color=VENV, stroke_width=4,
                       max_tip_length_to_length_ratio=0.1)

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(t.box, t.bar, t.dots, t.title, t.lines)), FadeOut(pipf),
                      caption_extra(tr, False), run_time=0.6)
            for ln in list(t.lines):
                t.lines.remove(ln)
            self.play(FadeIn(card5, shift=UP * 0.15), FadeIn(err5, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("it says activation")
            self.play(Create(pip_ul), run_time=0.5)
            vo.wait_until("but a uv venv")
            self.play(FadeIn(nopip_note, shift=LEFT * 0.15), run_time=0.5)

            vo.wait_until("On a machine")
            self.play(FadeIn(ill, shift=DOWN * 0.1),
                      usr_bin.frame.animate.set_stroke(SYSTEM).set_fill(SYSTEM, 0.15),
                      usr_bin[1].animate.set_fill(SYSTEM), usr_bin.label.animate.set_color(SYSTEM), run_time=0.7)
            usr_bin.color = SYSTEM
            vo.wait_until("which pip finds")
            pipf = figure("pip").next_to(dd[0].frame, UP, buff=0.12)
            self.play(FadeIn(pipf, shift=DOWN * 0.2), run_time=0.3)
            self.walk(pipf, dd, 3, step=0.3, knock=False, enter=3)
            vo.wait_until("and it refuses")
            self.play(FadeIn(refuse, shift=UP * 0.15), pipf.animate.set_color(ERR), run_time=0.5)
            self.play(Indicate(refuse, color=ERR, scale_factor=1.06), run_time=0.6)

            vo.wait_until("To add a package")
            # the "what if" picture has made its point: it steps back for the fix
            self.play(FadeIn(uvadd, shift=RIGHT * 0.2),
                      VGroup(dd, path_lbl, lr, pipf, refuse, ill).animate.fade(0.65), run_time=0.6)
            vo.wait_until("which also records")
            self.play(GrowArrow(a_toml), FadeIn(f_toml, shift=LEFT * 0.1), run_time=0.6)
            self.play(GrowArrow(a_lock), FadeIn(f_lock, shift=LEFT * 0.1), run_time=0.6)

        # ========================================================== 6 · what activation changes
        after_lines = VGroup(*[mono_line(s, 20, OUTPUT) for s in AFTER]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        substring(after_lines[0], ".venv/bin").set_color(VENV)
        after_head = label("after activation", 24, INK)
        after_body = VGroup(after_head, after_lines).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        after_box = box(after_body.width + 0.5, after_body.height + 0.4, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
        after_body.move_to(after_box)
        after_card = VGroup(after_box, after_body)
        after_card.move_to([0, 1.45, 0]).align_to([-6.5, 0, 0], LEFT)
        venv_line = after_lines[3]

        def item(text, code=(), green=(), ok=True):
            mk = check_mark(0.26, VENV) if ok else cross_mark(0.24, ERR, stroke=4)
            t_ = label(text, 22, INK if ok else S.GREY, t2f={c: MONO for c in code}, t2c={g: VENV for g in green})
            return VGroup(mk, t_).arrange(RIGHT, buff=0.16)

        items = VGroup(
            item(".venv/bin first in PATH", [".venv/bin"], [".venv/bin"]),
            item("VIRTUAL_ENV set", ["VIRTUAL_ENV"]),
            item("prompt (app)", ["(app)"], ["(app)"]),
            item("a deactivate command", ["deactivate"]),
            item("installs or loads packages", ok=False),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        items.move_to([0, after_card.get_y(), 0]).align_to([after_card.get_right()[0] + 0.45, 0, 0], LEFT)
        strike5 = Line(items[4][1].get_left() + LEFT * 0.05, items[4][1].get_right() + RIGHT * 0.05, color=ERR,
                       stroke_width=3)

        t2 = term(prompt=P_HOME, rows=3)
        t2.shift(np.array([0, BOTTOM - t2.box.get_bottom()[1], 0]))
        frame2 = VGroup(t2.box, t2.bar, t2.dots, t2.title)
        new_ssh = tag("new SSH window", S.GREY).move_to(t2.bar).align_to(t2.box, LEFT).shift(RIGHT * 0.9)
        new_ssh.set_y(t2.box.get_top()[1] - t2.bar_h / 2)
        mp = mini_path([UV, S.GREY, S.GREY, S.GREY, S.GREY])
        mgreen = mini_door(VENV)
        door_step = mgreen.width + 0.12                 # the doors make room for the GREEN one
        mp.next_to(t2.box, UP, buff=0.3).align_to(t2.box, RIGHT).shift(LEFT * (0.3 + door_step))
        only = label("activation: this shell only", 24, INK).next_to(mp, LEFT, buff=0.6)

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(dd, path_lbl, lr, pipf, card5, err5, pip_ul, nopip_note, ill, refuse,
                                     uvadd, f_toml, f_lock, a_toml, a_lock)), run_time=0.6)
            self.remove(doors)
            self.play(FadeIn(after_card, shift=RIGHT * 0.2), run_time=0.6)
            self.play(FadeIn(items[0], shift=LEFT * 0.15), Indicate(after_lines[0], color=VENV, scale_factor=1.04),
                      run_time=0.7)
            vo.wait_until("sets a variable")
            vbar = row_bar(venv_line, VENV, 0.2)
            self.play(FadeIn(items[1], shift=LEFT * 0.15), FadeIn(vbar), run_time=0.5)
            self.play(Indicate(substring(venv_line, "VIRTUAL_ENV"), color=S.WHITE, scale_factor=1.15), run_time=0.6)
            self.add(venv_line)
            vo.wait_until("changes the prompt")
            self.play(FadeIn(items[2], shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("adds a command")
            self.play(FadeIn(items[3], shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("that undoes")
            self.play(Indicate(items[:4], color=S.WHITE, scale_factor=1.04), run_time=0.8)
            vo.wait_until("It only changes")
            self.play(FadeIn(items[4], shift=LEFT * 0.15), run_time=0.5)
            self.play(Create(strike5), run_time=0.4)
            self.play(Indicate(items[0], color=VENV, scale_factor=1.08), run_time=0.7)

            vo.wait_until("and only in this shell")
            self.play(FadeIn(frame2, shift=UP * 0.4), FadeIn(new_ssh), run_time=0.6)
            p_home = self.bare_prompt(t2)
            self.play(FadeIn(mp, shift=DOWN * 0.1), FadeIn(only, shift=RIGHT * 0.1), run_time=0.6)
            vo.wait_until("If your SSH")
            self.play(Indicate(p_home, color=S.WHITE, scale_factor=1.06), run_time=0.8)
            self.add(p_home)
            vo.wait_until("cd into")
            self.type_cmd(t2, CD, 0.6)
            t2.set_prompt(P_REPO)
            self.bare_prompt(t2)
            vo.wait_until("and activate again")
            self.type_cmd(t2, ACTIVATE, 0.7)
            t2.set_prompt(P_VENV)
            p_new = self.bare_prompt(t2)
            mgreen.move_to(mp.doors[0])
            self.play(mp.doors.animate.shift(RIGHT * door_step), run_time=0.3)
            mgreen.shift(UP * 0.7).set_opacity(0)
            self.play(mgreen.animate.shift(DOWN * 0.7).set_opacity(1),
                      Indicate(substring(p_new, "(app)"), color=VENV, scale_factor=1.35), run_time=0.7)
            self.add(p_new)

        # ========================================================== 7 · step 11: the three runs
        t = t2
        note7 = label("copy from the README, quotes included", 22, S.GREY)
        real = recorded_tag("real capture · 2026-10-12")

        def green_output(lines):
            o = [ln for ln in lines if ln.text.startswith("Output:")][-1]
            bar = row_bar(o, VENV, 0.25)
            self.pin(o, bar, run_time=0.4, anim=FadeIn(bar), behind=True)
            return o

        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(after_card, vbar, items, strike5, mp, mgreen, only, new_ssh)), tr.goto(11),
                      run_time=0.6)
            t.clear(self, run_time=0.3)
            self.resize(t, 12, run_time=0.7)
            real.move_to([0, t.box.get_top()[1] - t.bar_h / 2, 0]).align_to(t.box, RIGHT).shift(LEFT * 0.3)
            self.type_cmd(t, RUN_IT, 0.6)
            t.print(self, RUN_OUT[:8], run_time=0.5)
            o = t.print(self, RUN_OUT[8:], run_time=0.5)
            green_output(o)
            vo.wait_until("Copy the long ones")
            note7.move_to([0, 2.62, 0]).align_to([6.5, 0, 0], RIGHT)
            self.play(FadeIn(note7, shift=DOWN * 0.1), run_time=0.5)
            self.type_cmd(t, RUN_ES, 1.4)
            o = t.print(self, ES_OUT, run_time=0.5)
            green_output(o)
            vo.wait_until("and pause")
            fr = self.type_cmd(t, RUN_FR, 1.4)
            yt = your_turn().next_to(fr.rows[-1].glyphs, RIGHT, buff=0.4)
            self.pin(fr.rows[-1], yt, run_time=0.4)
            o = t.print(self, FR_OUT, run_time=0.5)
            out_fr = green_output(o)
            vo.wait_until("This time Google")
            self.play(FadeIn(real, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("these are real")
            self.play(Indicate(t.find("Output: Buen"), color=VENV, scale_factor=1.04),
                      Indicate(out_fr, color=VENV, scale_factor=1.04), run_time=1.0)
            vo.wait_until("If you get a 429")
            in_fr = t.find("Input: Good afternoon")
            ib = row_bar(in_fr, TURN, 0.22)
            self.pin(in_fr, ib, run_time=0.4, anim=FadeIn(ib), behind=True)
            vo.wait_until("your venv works")
            self.play(Indicate(in_fr, color=TURN, scale_factor=1.05), run_time=0.9)

        # ========================================================== 8 · two ways without activating
        def way(cmd, what):
            c = chip(cmd, VENV, size=26, font=MONO)
            tags = VGroup(tag("extra", S.GREY), tag("no activation needed", S.GREY)).arrange(RIGHT, buff=0.25)
            top = VGroup(c, tags).arrange(RIGHT, buff=0.4)
            d = label(what, 24, INK).next_to(c, DOWN, buff=0.2).align_to(c, LEFT).shift(RIGHT * 0.15)
            g = VGroup(top, d)
            g.chip, g.tags, g.desc = c, tags, d
            return g

        w1 = way("uv run python cli.py", "syncs if needed, then runs in the venv")
        w2 = way(".venv/bin/python cli.py", "call the venv's python by its path")
        ways = VGroup(w1, w2).arrange(DOWN, aligned_edge=LEFT, buff=0.6).move_to([0, 0.75, 0]).align_to([-6.0, 0, 0], LEFT)
        for w in (w1, w2):
            w.desc.set_opacity(0)

        with self.voiceover(SAY[8]) as vo:
            # the YELLOW "look here" on the Input line is done: the chips are the subject now
            self.play(FadeOut(VGroup(real, note7)), FadeOut(ib), caption_extra(tr), run_time=0.4)
            in_fr.remove(ib)
            self.resize(t, 3, run_time=0.7)
            self.play(LaggedStart(FadeIn(w1[0], shift=RIGHT * 0.2), FadeIn(w2[0], shift=RIGHT * 0.2), lag_ratio=0.3),
                      run_time=0.9)
            vo.wait_until("that skip activation")
            self.play(Indicate(VGroup(w1.tags[1].text, w2.tags[1].text), color=S.WHITE, scale_factor=1.12),
                      run_time=0.8)
            vo.wait_until("First, uv run")
            self.play(Indicate(w1.chip, color=VENV, scale_factor=1.08), run_time=0.7)
            vo.wait_until("syncs the venv")
            self.play(text_part(w1.desc, "syncs if needed,").animate.set_opacity(1), run_time=0.5)
            vo.wait_until("then runs the app")
            self.play(text_part(w1.desc, "then runs in the venv").animate.set_opacity(1), run_time=0.5)
            vo.wait_until("Or call")
            self.play(Indicate(w2.chip, color=VENV, scale_factor=1.08), run_time=0.7)
            self.play(w2.desc.animate.set_opacity(1), run_time=0.5)
            self.play(Indicate(code_like(w2.chip, ".venv/bin/python"), color=S.WHITE, scale_factor=1.04), run_time=0.7)

        # ========================================================== 9 · why source, not run
        l5 = mono_line(L5, 22, OUTPUT).move_to([0, 2.05, 0])
        l5_cap = label("ls -la .venv/bin · line 5", 20, S.GREY).next_to(l5, UP, buff=0.18).align_to(l5, LEFT)
        mode = substring(l5, "-rw-r--r--")
        mode_ul = under(mode, S.GREY)
        not_x = tag("not executable", S.GREY).next_to(mode_ul, DOWN, buff=0.2).align_to(mode, LEFT)

        def bubble(title, w, h):
            b = box(w, h, S.GREY, fill_opacity=0.06)
            tt = label(title, 22, S.GREY).move_to(b.get_corner(UL), aligned_edge=UL).shift(np.array([0.2, -0.12, 0]))
            row = mini_path([UV, S.GREY, S.GREY, S.GREY, S.GREY])
            row.move_to(b).shift(DOWN * 0.15)
            g = VGroup(b, tt, row)
            g.frame, g.title, g.row = b, tt, row
            return g

        parent = bubble("your shell", 5.2, 1.5).move_to([-2.2, 0.15, 0])
        child = bubble("child shell (run as a program)", 5.6, 1.5).move_to([1.4, -1.95, 0])
        spawn = Line(parent.frame.get_bottom() + RIGHT * 1.2, child.frame.get_top() + LEFT * 1.4,
                     color=S.GREY, stroke_width=2.5)
        cg = mini_door(VENV)
        exits = label("exits at once", 24, ERR).next_to(child.frame, RIGHT, buff=0.3)
        if exits.get_right()[0] > 6.4:
            exits.next_to(child.frame, UP, buff=0.15).align_to(child.frame, RIGHT)
        ill9 = illustration_tag().next_to(parent.frame, RIGHT, buff=0.4).align_to(parent.frame, UP)

        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(VGroup(w1, w2)), FadeOut(VGroup(t.box, t.bar, t.dots, t.title, t.lines)),
                      caption_extra(tr, False), run_time=0.6)
            for ln in list(t.lines):
                t.lines.remove(ln)
            self.play(FadeIn(l5_cap), FadeIn(l5, shift=DOWN * 0.15), run_time=0.6)
            vo.wait_until("the activate script")
            self.play(Indicate(substring(l5, "activate"), color=S.WHITE, scale_factor=1.15), run_time=0.7)
            self.add(l5)
            vo.wait_until("It isn't even")
            self.play(Create(mode_ul), FadeIn(not_x, shift=UP * 0.1), run_time=0.6)
            self.play(Indicate(mode, color=S.WHITE, scale_factor=1.15), run_time=0.7)
            vo.wait_until("and run as a program")
            self.play(FadeIn(parent, shift=UP * 0.15), FadeIn(ill9), run_time=0.5)
            self.play(Create(spawn), FadeIn(child, shift=DOWN * 0.3, scale=0.85), run_time=0.6)
            cg.move_to(child.row.doors[0])
            self.play(child.row.doors.animate.shift(RIGHT * (cg.width + 0.12)), run_time=0.3)
            cg.shift(UP * 0.35).set_opacity(0)
            self.play(cg.animate.shift(DOWN * 0.35).set_opacity(1), run_time=0.4)
            vo.wait_until("that exits at once")
            self.play(FadeIn(exits), run_time=0.3)
            self.play(FadeOut(VGroup(child, cg), scale=1.25), FadeOut(spawn), FadeOut(exits), run_time=0.6)
            xp = cross_mark(0.42, ERR, stroke=7).next_to(parent.row, RIGHT, buff=0.35)
            self.play(Create(xp), Indicate(parent.row, color=S.WHITE, scale_factor=1.06), run_time=0.7)
            vo.wait_until("like the env file")
            self.play(Indicate(parent.row.doors[0], color=UV, scale_factor=1.3), run_time=0.7)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.wait(0.2)


def text_part(t, sub):
    """The glyphs of `sub` in a Text (its submobjects skip spaces)."""
    k = "".join(sub.split())
    i = "".join(t.text.split()).index(k)
    return VGroup(*t.submobjects[i:i + len(k)])


def code_like(c, sub):
    """The glyphs of `sub` inside a chip's mono text."""
    k = "".join(sub.split())
    full = "".join(c.text.text.split())
    i = full.index(k)
    return VGroup(*c.text.submobjects[i:i + len(k)])
