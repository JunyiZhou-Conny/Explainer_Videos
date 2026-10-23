"""S14 · Hooks are local; CI checks again (guest lecture, step-05b; tracker E8, then GREY dashed).

Beats (script.md, ## S14; one voiceover block each):
0. TRACKER E7 -> E8, `Lecture 9 · slides 20, 94–99` (top right, whole scene). A 9-row `laptop ·
   babykev` terminal (20 pt): `git switch --detach step-05b` -> s05b-01: 3 (cut); `just setup` ->
   s05b-02: …, 12 (`+ hadolint-bin==2.15.1`, `at the time of recording`); `just test` (walk:813)
   -> s05b-03: 9, …, 67 (its '=' padding dropped, as S03/S07/S10 show summaries), with the small
   GREY row tag `recorded · walk.md: Mac, 103 passed` beside it (S13's card, small). The terminal
   shrinks to a 4-row strip; CODE(babykev/pyproject.toml: 53–57) above it at 20 pt (53, 54, 57 get
   the house cut), line 56 YELLOW and `-m 'not system'` YELLOW. Line 9 gets a YELLOW bar, `1
   deselected` a ring and a GREY dashed dot beside it.
1. The panel clears; the strip grows to 6 rows. Picture above: the GREEN dashed hermetic border
   around 103 small dots ("103 selected by just test"); the GREY dashed dot flies outside it (BLUE
   label "system · the real model"). `just test -m system` (walk:814) -> s05b-06: 9, …, 11 (cut
   after its dot), …, 26 (no padding). On "says 1 passed, 103 deselected" the 103 dots turn GREY
   dashed (deselected) and the outside dot turns solid BLUE; `1 passed` GREEN. A GREY chip "part 1:
   a silent skip" with a skip dot; `▶ your turn` on the command.
2. TRACKER E8. 8-row terminal: `uv run hadolint Dockerfile` (walk:778) -> no output, a GREEN check;
   `docker build --target run --tag babykev-run .` (walk:719; 71 columns, it fills its row) ->
   s05b-18: 2 RED, tag `exit 127` beside that output row; `just image build run` (walk:759) -> s05b-19: 2 (cut), tag `exit 2`. The terminal shrinks
   to a 3-row strip; above it a GREY card, tag `recorded · walk.md` (walk.md step-05b, lines 711,
   734, 816–822): uv.lock -> two TEAL image bars (length by size) "run image · 1.15 GB", "dev
   image · 1.84 GB"; a TEAL container running `just check` (GREEN check) with its network wire cut
   (`--network none`), then the GREEN dashed hermetic border around it.
3. The tracker dims inside a GREY dashed outline (CI is not a walk step). The gate table, complete:
   six rows (config with hadolint), the system row GREY dashed outside. The five hermetic rows' names fly
   onto the five arches of a CommitGate (the table becomes the turnstile), the system row becomes a
   GREY dashed chip outside it; "one machine: your laptop" under the floor. A GREY chip `git commit
   --no-verify` rides the envelope up and over the whole turnstile into the vault.
4. The laptop gate moves down; a BLUE dashed "CI server" box appears above and the same turnstile
   (arches and names) is copied into it; the laptop gate clears. An envelope walks through every
   server arch (each beam flashes). CODE(cheese-app-ci-cd/.github/workflows/ci.yml: 13–17) at 20 pt,
   dimmed, caption "Part 5 of this same repo · lecture 21". The server clears; a GREY card, tag
   `erratum`: the SHOW's text in four rows (hook / image / README rows flash on the narration, the
   differing words YELLOW, "one command for everyone is the lesson" YELLOW). Coverage floors in one
   line: babykev `just test -q --cov-fail-under=90` (justfile:152), "Milestone 5 · at least 70%"
   (BRIEF S14 / milestone5.md:48). Fade to an empty frame.

Deviations (reported to the coordinator):
- Summary rows (s05b-03:67, s05b-06:26) drop their '=' padding (house convention of S03/S07/S10);
  s05b-01:3 is cut after `from the lockfile,`; s05b-06:11 after its dot; s05b-19:2 after `run the
  recipes` (92 columns); pyproject.toml 53, 54 and 57 get the house cut (72 columns at 20 pt).
- s05b-06:26: only `1 passed` turns GREEN (the script says the whole `1 passed, 103 deselected`):
  a deselected test is never GREEN on screen (SCENE-NOTES colours).
- The exit codes are shown as RED row tags (from the captures' `[exit N]` lines, which
  Capture.line() refuses to print): `exit 127` beside docker's error row (the command fills its
  row), `exit 2` beside `just image build run` (its output row is full).
- Beat 3: the turnstile the `--no-verify` envelope walks around is built from the table (its five
  hermetic rows become five named arches); the table itself has no room for an envelope beside it at
  13 wide. "The gate table clears before the server arrives" is that gate leaving in beat 4.
- The config row is common.py's step-05b row ("yamllint, uv, hadolint": justfile:125 puts hadolint in
  lint-config at this step, as the narration says); the table is 13.1 wide.
"""

import re

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene
from explainer import style as S

from common import (CLOUD, ERR, GATE_ORDER, IMAGE, INK, NARRATION, P_BABYKEV, PASS, ROUTE, SKIP,
                    SYSTEM_TEST, TURN, T_BABYKEV, VENV, CommitGate, GateTable, HermeticBorder, TestDot,
                    Turnstile, attach, beside, capture, check_mark, code, code_panel, code_span, cross_mark,
                    cut, dashed_chip, envelope, erratum_tag, excerpt, grey_chip, hl_bar, label, line_bar,
                    lock_glyph, lref, mono, note, outline_box, pin, recorded_tag, resize, ring, row_tag,
                    shown_path, substring, term, time_row, track, tracker, turn_row, type_cmd, walk)

SAY = NARRATION["S14"]
PT = 20                                  # terminal size: 72 characters a row
COLS = 72
PYP = "babykev/pyproject.toml"
P_FIRST, P_LAST, P_MARK = 53, 57, 56
CI = "cheese-app-ci-cd/.github/workflows/ci.yml"
JUSTFILE = "babykev/justfile"
INSIDE = ("tests", "format", "docs", "config", "types")           # the hermetic rows, table order
ARCH_NAMES = ("tests", "format + lint", "docs", "config files", "types")
FLOOR = -1.6                             # the laptop gate's floor in beat 3
GATE_X = -0.45                           # the gate sits a little left: the system chip is outside it


# ---------------------------------------------------------------- terminal helpers (S09/S11/S12's)
def fit(lines):
    """Capture lines ready to print: every row must already fit (cuts are made explicitly)."""
    for x in lines:
        s = x if isinstance(x, str) else x[0]
        assert len(s) <= COLS, (len(s), s)
    return list(lines)


def room(scene, t, n: int, run_time: float = 0.3) -> None:
    """Make room for n new rows: the oldest rows fade where they are, then the rest slide up (the
    toolkit's scroll sails the old rows over the tracker)."""
    over = len(t.lines) + n - t.rows
    if over <= 0:
        return
    gone = VGroup(*t.lines.submobjects[:over])
    stay = VGroup(*t.lines.submobjects[over:])
    scene.play(FadeOut(gone), run_time=run_time * 0.4)
    for m in gone:
        t.lines.remove(m)
    scene.remove(gone, *gone.get_family())
    if len(stay):
        scene.play(stay.animate.shift(UP * t.pitch * over), run_time=run_time * 0.6)


def out(scene, t, lines, run_time: float = 0.6, lag: float = 0.08) -> VGroup:
    """Print capture lines ((text, colour) or text) at once (they must fit the box)."""
    items = fit(lines)
    assert len(items) <= t.rows, (len(items), t.rows)
    room(scene, t, len(items))
    return t.print(scene, items, run_time=run_time, lag=lag)


def typ(scene, t, cmd: str, type_time: float | None = None):
    """type_cmd with room made first (long commands fold with the house fold)."""
    p = t.prompt + " "
    room(scene, t, len(t.fold(p + cmd, first_prefix=len(p))))
    return type_cmd(scene, t, cmd, type_time)


def bare(scene, t):
    """The prompt returns with no output."""
    room(scene, t, 1)
    ln = t.type(scene, "", type_time=0)
    ln.bare = True
    return ln


def rows_of(line) -> list:
    return list(line.rows) if hasattr(line, "rows") else [line]


def flash(tg, color, scale: float = 1.15, run_time: float = 0.7) -> list:
    """Flash a filled tag: its word and its outline (Indicate on the whole tag hides the word)."""
    return [Indicate(tg.text, color=color, scale_factor=scale, run_time=run_time),
            tg.box.animate(rate_func=there_and_back, run_time=run_time).set_stroke(width=4)]


def tag_on(scene, line, tg, buff: float = 0.45):
    """Pin a row tag beside a row (a folded command: its last row); returns (row, tag)."""
    r = rows_of(line)[-1]
    beside(tg, r, buff=buff)
    assert tg.get_right()[0] <= 6.55, tg.get_right()
    pin(scene, r, tg)
    return r, tg


def wipe(scene, t, *extra, run_time: float = 0.4):
    """Clear the terminal's rows (and their pinned marks) together with `extra` overlays."""
    gone = VGroup(*t.lines.submobjects, *extra)
    if len(gone):
        scene.play(FadeOut(gone), run_time=run_time)
    scene.remove(gone, *gone.get_family())
    for m in list(t.lines):
        t.lines.remove(m)


def dots_cut(s: str) -> str:
    """A pytest progress row cut after its dots (the padding and the `[ nn%]` column dropped)."""
    m = re.match(r"^(\S+ \.+)\s+\[", s)
    assert m, s
    return cut(s, m.group(1))


def summary(cap, n: int) -> str:
    """A pytest summary line without its '=' padding (as S03/S07/S10 show them)."""
    s = cap.line(n)
    assert s.startswith("=") and s.endswith("="), s
    return s.strip("= ")


# ---------------------------------------------------------------- pictures
def part(t, sub: str) -> VGroup:
    """The glyphs of `sub` in a label/mono Text (its submobjects skip spaces)."""
    s = t.original_text                     # Text.text has its spaces dropped
    i = s.index(sub)
    a = len("".join(s[:i].split()))
    return VGroup(*t.submobjects[a:a + len("".join(sub.split()))])


def ring_dot(r: float, color=SKIP, dashed: bool = True, width: float = 2.5) -> VMobject:
    return DashedVMobject(Circle(radius=r), num_dashes=10 if r > 0.1 else 6,
                          dashed_ratio=0.5 if dashed else 0.999).set_stroke(color, width)


def deselected_dot(r: float = 0.2) -> TestDot:
    """A BLUE (system) test dot shown deselected: a GREY dashed ring, no 's' (it never ran)."""
    d = TestDot(SYSTEM_TEST, r)
    d.ring.become(ring_dot(r).move_to(d.disc))
    return d


def small_dots(n: int = 103, cols: int = 26, r: float = 0.07, buff: float = 0.075) -> VGroup:
    """n small GREY rings: the hermetic tests `just test` selects."""
    g = VGroup(*[Circle(radius=r).set_stroke(S.GREY, 2) for _ in range(n)])
    return g.arrange_in_grid(cols=cols, buff=buff)


def pyproject_panel():
    lines = excerpt(PYP, P_FIRST, P_LAST).split("\n")
    lines[53 - P_FIRST] = cut(lines[53 - P_FIRST], "and lists")
    lines[54 - P_FIRST] = cut(lines[54 - P_FIRST], "(the Hub, the real")
    lines[57 - P_FIRST] = cut(lines[57 - P_FIRST], "or a device;")
    assert all(len(s) <= COLS for s in lines), [len(s) for s in lines]
    panel = code_panel("\n".join(lines), shown_path(PYP), P_FIRST, "toml", font_size=PT)
    for n in (53, 54, 57):              # pygments marks the house "…" as an Error token (pink-red)
        code_span(panel.code, n - P_FIRST, "…").set_color(S.GREY)
    return panel


def image_bar(gb: float, scale: float, text: str) -> VGroup:
    """A TEAL bar as long as the image is big, its name and size after it. .bar .text"""
    b = Rectangle(width=gb * scale, height=0.42, stroke_color=IMAGE, stroke_width=2.5).set_fill(IMAGE, 0.3)
    t = label(text, 22, INK).next_to(b, RIGHT, buff=0.2)
    g = VGroup(b, t)
    g.bar, g.text = b, t
    return g


class HooksThenCI(VoiceScene):
    def construct(self):
        assert len(SAY) == 5, len(SAY)

        sw, setup, test = capture("babykev/s05b-01"), capture("babykev/s05b-02"), capture("babykev/s05b-03")
        system, hado = capture("babykev/s05b-06"), capture("babykev/s05b-07")
        dbuild, ibuild = capture("babykev/s05b-18"), capture("babykev/s05b-19")
        assert sw.cmd == "git switch --detach step-05b" and setup.cmd == walk(705)[2:], (sw.cmd, setup.cmd)
        assert test.cmd == walk(813)[2:] and system.cmd == walk(814)[2:], (test.cmd, system.cmd)
        assert hado.cmd == walk(778)[2:] and hado.lines == [] and hado.exit == 0, hado.lines
        assert dbuild.cmd == walk(719)[2:] and ibuild.cmd == walk(759)[2:], (dbuild.cmd, ibuild.cmd)
        assert dbuild.exit == 127 and ibuild.exit == 2, (dbuild.exit, ibuild.exit)
        assert capture("babykev/s05b-04").at((2, 6)) == excerpt(PYP, P_FIRST, P_LAST).split("\n")
        floor_line = excerpt(JUSTFILE, 152, 152).strip()
        assert floor_line == "just test -q --cov-fail-under=90", floor_line
        assert "1.84 GB" in walk(711) and "1.15 GB" in walk(711), walk(711)
        assert "--network none" in walk(816) and "green" in walk(820), (walk(816), walk(820))

        # ========================================================== 0. step-05b: 1 deselected, on purpose
        tr = tracker("E", 7)
        ref = lref("20, 94–99")
        t = term(P_BABYKEV, rows=9, title=T_BABYKEV, size=PT)
        assert setup.line(12) == " + hadolint-bin==2.15.1", setup.line(12)
        sum67 = summary(test, 67)
        assert sum67 == "1 failed, 102 passed, 1 deselected in 4.38s", sum67

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(ref), FadeIn(t, shift=UP * 0.2), run_time=0.7)
            self.play(track(tr, 8), run_time=0.5)
            typ(self, t, sw.cmd, type_time=0.6)
            out(self, t, [cut(sw.line(3), "from the lockfile,")], run_time=0.3)
            typ(self, t, setup.cmd, type_time=0.4)
            s_out = out(self, t, setup.at("…", 12), run_time=0.4)
            l12 = s_out[1]
            tag_on(self, l12, time_row())
            vo.wait_until("A new real model test")
            j_ln = typ(self, t, test.cmd, type_time=0.4)
            j_out = out(self, t, [test.line(9), "…", sum67], run_time=0.6)
            l9, ell, l67 = j_out
            rec = row_tag("recorded · walk.md: Mac, 103 passed", S.GREY)
            tag_on(self, l67, rec, buff=0.35)
            vo.wait_until("the config deselects that marker")
            panel = pyproject_panel()
            resize(self, t, 4, keep=[j_ln, l9, ell, l67], run_time=0.6)
            panel.move_to([0, 0, 0]).align_to([0, 2.75, 0], UP)
            assert panel.get_bottom()[1] > t.box.get_top()[1] + 0.15 and panel.width <= 13.2, \
                (panel.get_bottom(), t.box.get_top(), panel.width)
            k = P_MARK - P_FIRST
            bar = line_bar(panel.code, k, TURN, 0.2)
            mark = code_span(panel.code, k, "-m 'not system'")
            self.play(FadeIn(panel, shift=DOWN * 0.2), run_time=0.6)
            self.play(FadeIn(bar), mark.animate.set_color(TURN), run_time=0.5)
            self.play(Indicate(mark, color=TURN, scale_factor=1.12), run_time=0.7)
            vo.wait_until("every just test says 1 deselected")
            hb = hl_bar(l9.glyphs, TURN, 0.2)
            one = substring(l9, "1 deselected")
            r1 = ring(one, S.GREY, buff=0.05)
            dot = deselected_dot().move_to(beside(Dot(radius=0.2), l9, buff=0.5))
            self.play(FadeIn(hb), Create(r1), run_time=0.5)
            self.remove(hb)
            l9.submobjects.insert(0, hb)                # behind the glyphs, scrolls with the row
            self.add(l9)
            attach(self, l9, r1)
            self.play(FadeIn(dot, scale=0.6), run_time=0.5)
            vo.wait_until("on purpose")
            self.play(Indicate(one, color=INK, scale_factor=1.15),
                      dot.ring.animate(rate_func=there_and_back).set_stroke(width=5), run_time=0.8)

        # ========================================================== 1. asked for: 1 passed, 103 deselected
        inner = small_dots()
        border = HermeticBorder.around(inner, buff=0.35)
        pic_l = VGroup(border, inner)
        pic_l.move_to([-2.0, 1.55, 0])
        sel = note("103 selected by just test", S.GREY, 22).next_to(border, DOWN, buff=0.2)
        out_at = np.array([border.get_right()[0] + 1.5, inner.get_center()[1] + 0.2, 0])
        sys_lab = label("system · the real model", 22, SYSTEM_TEST).move_to(out_at + DOWN * 0.6)
        sys_lab.align_to(out_at + LEFT * 0.5, LEFT)
        l11 = dots_cut(system.line(11))
        sum26 = summary(system, 26)
        assert sum26 == "1 passed, 103 deselected in 7.30s" and l11.endswith(".…"), (sum26, l11)

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(panel, bar)), run_time=0.4)
            self.remove(panel, bar)
            wipe(self, t, run_time=0.4)
            resize(self, t, 6, run_time=0.5)
            assert t.box.get_top()[1] < sel.get_bottom()[1] - 0.15, (t.box.get_top(), sel.get_bottom())
            assert sys_lab.get_right()[0] <= 6.5, sys_lab.get_right()
            self.play(FadeIn(border), LaggedStart(*[FadeIn(d) for d in inner], lag_ratio=0.004),
                      FadeIn(sel, shift=UP * 0.1), dot.animate.move_to(out_at), run_time=1.0)
            self.play(FadeIn(sys_lab, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("just test, dash m system")
            m_ln = typ(self, t, system.cmd, type_time=0.6)
            m_out = out(self, t, [system.line(9), "…", l11, "…", sum26], run_time=0.6)
            l26 = m_out[4]
            vo.wait_until("says 1 passed")
            ones = substring(l26, "1 passed")
            self.play(ones.animate.set_color(PASS), dot.to("pass"),
                      LaggedStart(*[d.animate.become(ring_dot(0.07).move_to(d)) for d in inner],
                                  lag_ratio=0.003), run_time=0.9)
            self.play(Indicate(ones, color=PASS, scale_factor=1.15), run_time=0.6)
            vo.wait_until("the real model ran")
            self.play(Indicate(sys_lab, color=SYSTEM_TEST, scale_factor=1.08),
                      dot.disc.animate(rate_func=there_and_back).scale(1.4), run_time=0.8)
            vo.wait_until("it had to pass, not skip")
            pass_ring = ring(dot, PASS, buff=0.1)
            self.play(Create(pass_ring), run_time=0.5)
            vo.wait_until("part 1's silent skip")
            skip = TestDot(SYSTEM_TEST, 0.17, state="skip")
            skip_note = VGroup(skip, label("part 1: a silent skip", 22, S.GREY)).arrange(RIGHT, buff=0.2)
            skip_note.next_to(sys_lab, DOWN, buff=0.35).align_to(sys_lab, LEFT)
            assert skip_note.get_bottom()[1] > t.box.get_top()[1] + 0.1, skip_note.get_bottom()
            self.play(FadeIn(skip_note, shift=UP * 0.15), run_time=0.6)
            self.play(Indicate(skip_note[1], color=S.GREY, scale_factor=1.08), run_time=0.6)
            vo.wait_until("Pause and run both forms.")
            _, yt = tag_on(self, m_ln, turn_row())
            self.play(*flash(yt, TURN), run_time=0.8)

        # ========================================================== 2. hadolint; no Docker here; the walk's record
        lock = VGroup(lock_glyph(0.42, VENV), mono("uv.lock", 22, INK)).arrange(RIGHT, buff=0.18)
        scale = 2.4
        run_bar = image_bar(1.15, scale, "run image · 1.15 GB")
        dev_bar = image_bar(1.84, scale, "dev image · 1.84 GB")
        box_c = RoundedRectangle(width=3.6, height=0.8, corner_radius=0.12, stroke_color=IMAGE,
                                 stroke_width=3).set_fill(IMAGE, 0.12)
        jc = VGroup(mono("just check", 22, INK), check_mark(0.3, PASS)).arrange(RIGHT, buff=0.25)

        with self.voiceover(SAY[2]) as vo:
            gone = VGroup(border, inner, sel, dot, sys_lab, pass_ring, skip_note)
            self.play(FadeOut(gone), run_time=0.5)
            self.remove(gone, *gone.get_family())
            wipe(self, t, run_time=0.3)
            resize(self, t, 8, run_time=0.5)
            vo.wait_until("hadolint lints the Dockerfile")
            h_ln = typ(self, t, hado.cmd, type_time=0.6)
            bare(self, t)
            ok = check_mark(0.32, PASS).move_to(beside(Dot(radius=0.16), h_ln, buff=0.35))
            vo.wait_until("clean.")
            self.play(Create(ok), run_time=0.5)
            attach(self, h_ln, ok)
            vo.wait_until("so the recipes fail politely")
            d_ln = typ(self, t, dbuild.cmd, type_time=0.8)
            vo.wait_until("docker build is command not found")
            d_out = out(self, t, [(dbuild.line(2), ERR)], run_time=0.4)
            _, x127 = tag_on(self, d_out[0], row_tag(f"exit {dbuild.exit}", ERR), buff=0.35)   # the command fills its row
            self.play(Indicate(substring(d_out[0], "command not found"), color=ERR, scale_factor=1.1), run_time=0.6)
            vo.wait_until("and the image recipe explains itself")
            i_ln = typ(self, t, ibuild.cmd, type_time=0.5)
            i_out = out(self, t, [cut(ibuild.line(2), "run the recipes")], run_time=0.4)
            _, x2 = tag_on(self, i_ln, row_tag(f"exit {ibuild.exit}", ERR), buff=0.35)
            self.play(Indicate(substring(i_out[0], "there is no docker here."), color=INK, scale_factor=1.08),
                      run_time=0.8)
            vo.wait_until("On your laptop, with Docker Desktop")
            resize(self, t, 3, keep=[d_out[0], rows_of(i_ln)[-1], i_out[0]], run_time=0.6)
            top = 2.5                                   # the tag on its edge stays under the tracker
            frame = RoundedRectangle(width=12.6, height=top - (t.box.get_top()[1] + 0.2), corner_radius=0.16,
                                     stroke_color=S.GREY, stroke_width=2.5).set_fill(S.GREY_DARKER, 0.6)
            frame.move_to([0, (top + t.box.get_top()[1] + 0.2) / 2, 0])
            rtag = recorded_tag().move_to(frame.get_corner(UL) + np.array([0.3, 0, 0]), aligned_edge=LEFT)
            head = label("with Docker Desktop", 22, S.GREY).next_to(rtag, RIGHT, buff=0.3)
            head.add_background_rectangle(color=S.BG, opacity=1, buff=0.06)
            # row A: one lockfile, two images (bar length = size)
            ya = frame.get_top()[1] - 1.0
            lock.move_to([-4.9, ya - 0.35, 0])
            x0 = -2.7
            run_bar.shift(np.array([x0 - run_bar.bar.get_left()[0], ya - run_bar.bar.get_center()[1], 0]))
            dev_bar.shift(np.array([x0 - dev_bar.bar.get_left()[0], ya - 0.7 - dev_bar.bar.get_center()[1], 0]))
            arr_r = Arrow(lock.get_right(), run_bar.bar.get_left(), buff=0.15, color=S.GREY, stroke_width=3,
                          tip_length=0.16)
            arr_d = Arrow(lock.get_right(), dev_bar.bar.get_left(), buff=0.15, color=S.GREY, stroke_width=3,
                          tip_length=0.16)
            assert dev_bar.get_right()[0] <= 6.2, dev_bar.get_right()
            # row B: just check in a container with no network
            yb = frame.get_bottom()[1] + 0.85
            box_c.move_to([-1.0, yb, 0])
            jc.move_to(box_c)
            c_lab = label("dev image container", 20, IMAGE).next_to(box_c, LEFT, buff=0.45)
            wire = DashedLine(box_c.get_right() + RIGHT * 0.22, box_c.get_right() + RIGHT * 3.0, dash_length=0.12,
                              color=S.GREY, stroke_width=3)
            cutx = cross_mark(0.3, S.GREY).move_to(wire.get_center())
            netw = label("network", 22, S.GREY).next_to(wire, RIGHT, buff=0.2)
            flag = mono("--network none", 22, INK).next_to(wire, UP, buff=0.3)
            flag.align_to(wire.get_left() + RIGHT * 0.35, LEFT)       # clear of the hermetic border
            herm = HermeticBorder.around(box_c, buff=0.22)
            assert herm.get_top()[1] < dev_bar.get_bottom()[1] - 0.05 and herm.get_bottom()[1] > frame.get_bottom()[1], \
                (herm.get_top(), dev_bar.get_bottom(), herm.get_bottom(), frame.get_bottom())
            assert c_lab.get_left()[0] >= -6.2 and netw.get_right()[0] <= 6.2, (c_lab.get_left(), netw.get_right())
            self.play(FadeIn(frame), FadeIn(rtag, shift=DOWN * 0.1), FadeIn(head), run_time=0.5)
            vo.wait_until("both images build for real")
            self.play(FadeIn(lock, shift=RIGHT * 0.15), run_time=0.5)
            self.play(GrowArrow(arr_r), GrowArrow(arr_d), GrowFromEdge(run_bar.bar, LEFT),
                      GrowFromEdge(dev_bar.bar, LEFT), run_time=0.8)
            vo.wait_until("The walk's record shows the rest.")
            self.play(*flash(rtag, S.GREY), run_time=0.7)
            vo.wait_until("Two images from one lockfile")
            self.play(Indicate(lock[1], color=INK, scale_factor=1.15), run_time=0.6)
            vo.wait_until("1.15 and 1.84 gigabytes")
            self.play(FadeIn(run_bar.text, shift=LEFT * 0.15), run_time=0.5)
            self.play(FadeIn(dev_bar.text, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("And just check runs green")
            self.play(FadeIn(box_c), FadeIn(c_lab), FadeIn(jc[0]), run_time=0.5)
            self.play(Create(jc[1]), run_time=0.4)
            vo.wait_until("with no network")
            self.play(Create(wire), FadeIn(netw), run_time=0.6)
            self.play(FadeIn(cutx, scale=1.4), FadeIn(flag, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("the hermetic claim")
            self.play(FadeIn(herm), run_time=0.6)
            vo.wait_until("proved by experiment")
            self.play(Indicate(herm.text[1], color=VENV, scale_factor=1.2),
                      Indicate(jc[1], color=PASS, scale_factor=1.3), run_time=0.8)

        # ========================================================== 3. the table is full; --no-verify walks past
        gt = GateTable(keys=GATE_ORDER, filled=GATE_ORDER)       # config row: step-05b's, hadolint in it
        gt.move_to([0, -0.35, 0])
        assert gt.get_top()[1] <= 2.8 and gt.get_bottom()[1] >= -3.5 and gt.width <= 13.2, \
            (gt.get_top(), gt.get_bottom(), gt.width)
        dim_box = outline_box(tr.width + 0.18, tr.height + 0.2, S.GREY, solid=False).move_to(tr)
        gate = CommitGate(5, arch_h=1.2)
        gate.shift(np.array([GATE_X - gate.get_center()[0], FLOOR - gate.floor.get_center()[1], 0]))
        names = gate.turnstile.name_labels(ARCH_NAMES)          # built AFTER placing (SCENE-NOTES trap)
        sys_chip = dashed_chip("system tests")
        sys_chip.move_to(gate.vault.frame.get_right() + RIGHT * (0.3 + sys_chip.width / 2))
        sys_chip.align_to([0, FLOOR + 0.08, 0], DOWN)
        assert sys_chip.get_right()[0] <= 6.5, sys_chip.get_right()
        one_m = label("one machine: your laptop", 22, S.GREY)
        one_m.move_to([gate.turnstile.get_center()[0], min(n.get_bottom()[1] for n in names) - 0.4, 0])
        nv = grey_chip("git commit --no-verify", 20, mono_font=True)
        env = gate.envelope

        with self.voiceover(SAY[3]) as vo:
            gone = VGroup(frame, rtag, head, lock, arr_r, arr_d, run_bar, dev_bar, box_c, c_lab, jc, wire, cutx,
                          netw, flag, herm)
            self.play(FadeOut(gone), run_time=0.5)
            self.remove(gone, *gone.get_family())
            wipe(self, t, run_time=0.3)
            self.play(FadeOut(t), tr.animate.fade(0.6), Create(dim_box), run_time=0.5)
            self.remove(t)
            self.play(FadeIn(gt, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("six rows")
            whats = [gt.rows[k].cells[0] for k in GATE_ORDER]
            self.play(LaggedStart(*[Indicate(w, color=INK, scale_factor=1.12) for w in whats], lag_ratio=0.15),
                      run_time=1.0)
            vo.wait_until("system outside the turnstile")
            srow = gt.rows["system"]
            self.play(srow.outline.animate(rate_func=there_and_back).set_stroke(width=5),
                      Indicate(srow.cells[0], color=S.GREY, scale_factor=1.12), run_time=0.8)
            self.play(Indicate(gt.icon.frame, color=INK, scale_factor=1.3), run_time=0.6)
            vo.wait_until("Now the limit.")
            # the table becomes the turnstile: the five hermetic names fly onto five arches, the
            # system row becomes a chip outside it; everything else fades
            movers = [gt.rows[k].cells[0] for k in INSIDE]
            s_what, s_out = srow.cells[0], srow.outline
            for k in INSIDE:
                gt.rows[k].cells.remove(gt.rows[k].cells[0])
            srow.cells.remove(s_what)
            srow.remove(s_out)
            self.add(*movers, s_what, s_out)
            rest = VGroup(*[m for m in gt.submobjects])
            moves = []
            for i, (m, n) in enumerate(zip(movers, names)):
                if m.text.replace(" ", "") == n.text.replace(" ", ""):
                    moves.append(ReplacementTransform(m, n))
                else:
                    moves.append(AnimationGroup(FadeOut(m, shift=(n.get_center() - m.get_center()) * 0.5),
                                                FadeIn(n, shift=(n.get_center() - m.get_center()) * 0.5)))
            self.play(FadeOut(rest), run_time=0.4)
            self.remove(gt, rest)
            self.play(FadeIn(gate.floor), FadeIn(gate.vault), gate.drop_in(run_time=0.8), *moves,
                      ReplacementTransform(s_what, sys_chip.text), ReplacementTransform(s_out, sys_chip.box),
                      run_time=1.0)
            self.add(sys_chip)
            self.play(FadeIn(env, shift=RIGHT * 0.3), run_time=0.4)
            vo.wait_until("A hook runs on one machine")
            self.play(FadeIn(one_m, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("and git commit")
            nv.next_to(env, UP, buff=0.7)                  # above the arch names
            self.play(FadeIn(nv, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("walks straight past it")
            rider = VGroup(env, nv)
            start = rider.get_center()
            # up, over every arch, and down into the vault (it never touches an arch)
            end = gate.vault.frame.get_center() + (rider.get_center() - env.get_center())
            peak = max(n.get_top()[1] for n in names) + 0.15 + (rider.get_center()[1] - rider.get_bottom()[1])
            path = VMobject().set_points_smoothly([start, [start[0] + 0.3, peak, 0],
                                                   [end[0] - 0.3, peak, 0], end])
            self.play(gate.open(), run_time=0.4)
            assert peak + rider.height / 2 <= 2.85, peak
            self.play(MoveAlongPath(rider, path), run_time=1.6, rate_func=smooth)
            self.play(FadeOut(env), FadeOut(nv), run_time=0.4)
            gate.remove(env)
            self.remove(env, nv)
            gate.envelope = None
            self.play(gate.shut(), Indicate(gate.turnstile.arches, color=S.GREY, scale_factor=1.04), run_time=0.6)

        # ========================================================== 4. CI re-runs the checks; one command for everyone
        drop = FLOOR + 2.95                     # the laptop floor goes to -2.95
        srv_ts = Turnstile(5, arch_w=0.7, arch_h=1.2, gap=0.22)
        srv_ts.move_to([0.9, 0, 0]).shift(UP * (0.65 - srv_ts.arches.get_bottom()[1]))
        srv_names = srv_ts.name_labels(ARCH_NAMES)
        srv_box = outline_box(9.8, 2.6, CLOUD, solid=False, fill_opacity=0.06)
        srv_box.move_to([0, 1.3, 0])
        srv_lab = label("CI server", 22, CLOUD).move_to(srv_box.get_corner(UL) + np.array([0.3, -0.35, 0]),
                                                        aligned_edge=LEFT)
        assert srv_box.get_top()[1] <= 2.85 and srv_lab.get_right()[0] < min(n.get_left()[0] for n in srv_names), \
            (srv_box.get_top(), srv_lab.get_right())
        s_env = envelope("your commit")
        s_env.move_to([srv_ts.get_left()[0] - 0.25 - s_env.width / 2, 0.65 + 0.62, 0])
        assert s_env.get_left()[0] > srv_box.get_left()[0] + 0.1, s_env.get_left()
        ci = code(CI, 13, 17, font_size=PT)
        ci.move_to([0, 0, 0]).align_to([-6.4, 0, 0], LEFT).align_to([0, -0.4, 0], UP)
        ci.code.set_opacity(0.55)
        ci.header.set_opacity(0.55)
        cap = VGroup(label("Part 5 of this same repo", 20, S.GREY), label("lecture 21", 20, S.GREY))
        cap.arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(ci, RIGHT, buff=0.3)
        assert ci.get_bottom()[1] >= -3.5 and cap.get_right()[0] <= 6.5, (ci.get_bottom(), cap.get_right())

        # the erratum card (SHOW's text, four rows) and the coverage floors
        e_rows = VGroup(label("here: hook pins black 24.1.1", 24, INK), label("image installs the newest", 24, INK),
                        label("README widths vary", 24, INK))
        e_rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        lesson = label("one command for everyone is the lesson", 24, TURN)
        body = VGroup(e_rows, lesson).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        e_frame = RoundedRectangle(width=body.width + 1.0, height=body.height + 0.9, corner_radius=0.16,
                                   stroke_color=S.GREY, stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
        card = VGroup(e_frame, body)
        body.move_to(e_frame).shift(DOWN * 0.1)
        card.move_to([0, 0.75, 0])
        etag = erratum_tag().move_to(e_frame.get_corner(UL) + np.array([0.3, 0, 0]), aligned_edge=LEFT)
        rule = Line(e_rows.get_corner(DL) + DOWN * 0.2, e_rows.get_corner(DL) + DOWN * 0.2 + RIGHT * body.width,
                    color=S.GREY_DARK, stroke_width=2)
        odd = [part(e_rows[0], "24.1.1"), part(e_rows[1], "the newest"), part(e_rows[2], "vary")]
        cov_a = VGroup(label("babykev", 22, S.GREY), grey_chip(floor_line, 22, mono_font=True))
        cov_b = VGroup(label("Milestone 5", 22, S.GREY), label("at least 70%", 22, INK))
        for g in (cov_a, cov_b):
            g.arrange(RIGHT, buff=0.3)
        cov = VGroup(cov_a, cov_b).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        cov.next_to(e_frame, DOWN, buff=0.45)
        cov_b[1].align_to(cov_a[1].text, LEFT)
        assert cov.get_bottom()[1] >= -3.5 and e_frame.get_top()[1] + 0.25 <= 2.85, (cov.get_bottom(), e_frame.get_top())

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(one_m, sys_chip)), run_time=0.4)
            self.remove(one_m, sys_chip)
            self.play(VGroup(gate, names).animate.shift(DOWN * drop), run_time=0.6)
            self.play(Create(srv_box.frame), FadeIn(srv_box.fill), FadeIn(srv_lab),
                      TransformFromCopy(gate.turnstile.arches, srv_ts.arches),
                      TransformFromCopy(names, srv_names), run_time=1.0)
            self.play(Create(srv_ts.floor), run_time=0.3)
            self.add(srv_ts, srv_names)
            self.play(FadeOut(VGroup(gate, names)), run_time=0.5)
            self.remove(gate, names)
            vo.wait_until("on a server nobody can skip")
            self.play(FadeIn(s_env, shift=RIGHT * 0.3), run_time=0.4)
            for a in srv_ts.arches:
                self.play(s_env.animate.move_to([a.get_center()[0], s_env.get_center()[1], 0]),
                          a.beam.animate(rate_func=there_and_back).set_stroke(INK, width=5, opacity=1),
                          a.lamp.animate(rate_func=there_and_back).set_color(INK), run_time=0.3)
            self.play(s_env.animate.shift(RIGHT * 1.2), FadeOut(s_env), run_time=0.5)
            self.remove(s_env)
            vo.wait_until("part 5 of this same repo")
            self.play(FadeIn(ci, shift=UP * 0.15), run_time=0.6)
            self.play(FadeIn(cap[0], shift=LEFT * 0.15), run_time=0.4)
            vo.wait_until("in lecture 21")
            self.play(FadeIn(cap[1], shift=LEFT * 0.15), run_time=0.4)
            vo.wait_until("It is also why")
            gone = VGroup(srv_box, srv_lab, srv_ts, srv_names, ci, cap)
            self.play(FadeOut(gone), run_time=0.5)
            self.remove(gone, *gone.get_family())
            self.play(FadeIn(e_frame), FadeIn(etag, shift=DOWN * 0.1), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in e_rows], lag_ratio=0.3),
                      Create(rule), run_time=0.9)
            vo.wait_until("the hook, CI and the README")
            for r, w in zip(e_rows, ("hook", "image", "README")):
                self.play(Indicate(part(r, w), color=INK, scale_factor=1.2), run_time=0.45)
            vo.wait_until("does not quite manage that")
            self.play(*[o.animate.set_color(TURN) for o in odd], run_time=0.5)
            self.play(LaggedStart(*[Indicate(o, color=TURN, scale_factor=1.15) for o in odd], lag_ratio=0.25),
                      run_time=0.9)
            vo.wait_until("One command for everyone")
            self.play(FadeIn(lesson, shift=UP * 0.15), run_time=0.6)
            self.play(Indicate(lesson, color=TURN, scale_factor=1.06), run_time=0.8)
            vo.wait_until("Coverage floors in one line")
            self.play(FadeIn(cov_a[0]), FadeIn(cov_a[1], shift=UP * 0.1), run_time=0.5)
            vo.wait_until("babykev chose 90")
            self.play(Indicate(part(cov_a[1].text, "90"), color=INK, scale_factor=1.3), run_time=0.6)
            vo.wait_until("milestone 5 asks at least 70")
            self.play(FadeIn(cov_b, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(part(cov_b[1], "70%"), color=INK, scale_factor=1.25), run_time=0.6)
        self.wait(0.6)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
