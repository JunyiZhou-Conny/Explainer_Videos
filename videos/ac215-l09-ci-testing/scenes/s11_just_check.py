"""S11 · One command is the gate (guest lecture, step-03 -> step-04b; tracker E4 -> E5).

Beats (script.md, ## S11; one voiceover block each):
0. TRACKER E4, `Lecture 9 · slides 34–43` (top right, until the refusals). An 11-row `laptop ·
   babykev` terminal (20 pt): `git switch --detach step-03` -> s03-01: 3 (cut); `just setup` ->
   s03-02: 2, …, 19, …, 25; on "lockfile sync" / "hook install" the two halves of line 2 ring, line
   25 rings YELLOW; `▶ your turn` on the setup. Cleared, then `cat "$(git rev-parse --git-path
   hooks)/pre-commit"` (walk.md:230, folds) -> s03-05: 2–3, …, 6–9, …, 15. The hand-over: TEAL ring
   on `.pre-commit-config.yaml` (line 8), PURPLE ring on `-mpre_commit` (line 15) with a PURPLE row
   tag "→ pre-commit". Line 7's venv path gets a YELLOW bar and the caption "this machine's path ·
   why it is never committed" above the terminal.
1. CODE(babykev/.pre-commit-config.yaml) in two 10-line windows (5–14, 15–24) over two turnstiles
   side by side (V5): S09's nine (GREY names, "cheese-app-ci-cd · 9 hooks") and babykev's four
   ("babykev · 4 hooks"). Each hook is barred YELLOW in the code as it is named and its arch lights
   with its name; the shared guards (large files, merge markers) flash in both rows. `entry: just
   check`, `pass_filenames: false`, `always_run: true` barred. Then the code and the cheese row
   clear, babykev's turnstile rises, and a 5-row strip types `just --show check` (walk.md:245) ->
   s03-08: 9–12 (step-03's recipe, four checks); each row flies out of the strip into a stack fed
   by the `just check` arch, on its spoken name.
2. TRACKER E4. 12-row terminal: `just check` -> s03-09: 2–7, …, 18–21 (line 7's progress dots cut
   before pytest's padding); `All checks passed!`, line 18 and `53 passed` GREEN. A coverage gauge
   (0–100 %, the 90 % floor marked) fills GREEN to 100.00 %. The terminal keeps the command and line
   18; `just test -k confidence --cov-fail-under=90` -> s03-10: 2, …, 11–12, …, 25–26 (line 26 cut
   after its timing). The 9 dots and `9 passed`, `total of 49`, then line 25 RED; the gauge drops to
   49.40 % RED under the floor. `▶ your turn` on both.
3. Config beat: CODE(babykev/.pre-commit-config.yaml: 9–10) as a card above a 10-row terminal; the
   walk's mis-indent sed (Linux form, as captured; walk.md:260 spells it `sed -i ''` for a Mac)
   folds over three rows -> no output, and line 10 shifts right two columns, RED; `uv run yamllint
   --strict .` -> s03-13: 2–3, line 3 RED (cut), `10:15` ringed; `git restore
   .pre-commit-config.yaml` -> no output, line 10 shifts back; `just lint-config` -> s03-28: …, 7–8
   GREEN. The card gives way to three GREY chips `validate-pyproject` · `uv lock --check` ·
   `just --fmt --check`.
4. TRACKER E4, the lecture tag clears. `perl -pi -e 's/^(from typing)/import os\\n$1/' …`
   (walk.md:296, folds) -> no output; `git commit -am "try"` -> s03-31: 6–9, …, 16–17, …, 32
   (`▶ your turn`); Passed GREEN, Skipped GREY, `just check…Failed` and `F401` RED; `git status`
   (walk.md:301) -> s03-32: 2–3, …, 6, row tag "no commit"; `git restore src/babykev/api.py`
   (walk.md:302). Cleared: `echo X=1 > .env && git add -f .env` -> no output, `git commit -m "try"`
   -> s03-35: 2–10, `no .env file…Failed` RED and line 8 (the config's own sentence) RED, quoted
   whole in a RED card above the terminal; the undo `git rm --cached -q .env && rm .env`
   (walk.md:311).
5. TRACKER E5. Two style cards: GREEN "babykev: check points, you run just fmt yourself", TEAL
   "cheese: black rewrites, you look and re-stage", over the gate table (tests and system filled,
   S09 left "format + lint" empty): as the two format styles are named, the "format + lint" row
   fills (YELLOW on babykev's card, settles on cheese's: both styles are that gate row); cards and
   table clear. One 11-row terminal: `just docs
   check` (row tag "at step-04") -> s04-04: 2–7, …, 93, `50 of 88` RED; it keeps the command and
   line 93 and runs it again (row tag "at step-04b") -> s04b-03: 2–9, `88 of 88` GREEN. A capture
   card `git commit -am "try"` with s04b-09: 5–7, 35–36 and the GREY chip "one deleted description
   blocks the commit". V1: the gate table returns (tests, format + lint, system) and the two rows
   join, "docs" and "config files", GREEN inside the turnstile frame. Fade to an empty frame.

Deviations (reported to the coordinator):
- Over-wide lines keep their text verbatim up to a house "…" cut (common.py `cut`). pre-commit's
  hook rows (79 columns) are cut inside their dot leader and keep their verdict: `name……Failed`
  is `cut(row, name + dots) + verdict` and only padding dots are dropped (asserted), as the script
  itself writes `just check…Failed`. s03-35:8 (80 columns) is cut after "It is never" in the
  terminal and quoted whole, verbatim from the capture, in a one-line card above it.
- Skipped lines between two shown ranges always get a "…" row (the house picker's rule), also where
  the script's list runs them together (s03-02 19/25, s03-05 3/6, s03-09 7/18, s03-10 2/11, 12/25,
  s03-31 9/16, s03-28 before 7).
- The mis-indent sed's quoted pattern (68 characters, with spaces) cannot fold with the house
  4-space continuation indent in a 72-column row: it folds at the same two spaces outside the
  quotes with a 2-space indent (still one valid shell command when pasted; asserted).
- "two small terminals" for the docs checks: one full-width terminal runs both in turn (the house
  forbids half-width terminals), each command tagged with its step.
- The gate table's "format + lint" row is empty when it appears (S09 leaves it empty) and fills
  during the two format-gate style cards, so "Two rows join the table" stays true at the end; the
  config row's tools read "yamllint, uv, just" (step-03's lint-config: no hadolint until step-05b).
- The coverage gauge above the beat-2 terminal is an addition (a mechanism for "floor"): its two
  values are the capture's own (100.00 %, 49.40 %).
"""

import re

import numpy as np  # noqa: I001  (manim first, then common: common must win)
from manim import *

from explainer.scene import VoiceScene
from explainer import style as S

from common import (BOTTOM, ERR, IMAGE, INK, NARRATION, P_BABYKEV, PASS, SKIP, TOOL, TURN, T_BABYKEV,
                    VENV, BABYKEV_HOOKS, CHEESE_HOOKS, GateTable, Turnstile, arrow, attach, beside, box,
                    capture, code, code_panel, code_span, cut, excerpt, glyph_range, grey_chip, hl_bar,
                    label, line_bar, line_pitch, lref, mono, note, outline_box, pin, resize, ring,
                    row_tag, shown_path, steady, substring, term, track, tracker, turn_row, type_cmd,
                    under, unpin, walk, your_turn)

SAY = NARRATION["S11"]
PT = 20                                  # terminal size: 72 characters a row
COLS = 72
CFG = "babykev/.pre-commit-config.yaml"
WINDOWS = ((5, 14), (15, 24))

_HOOK = re.compile(r"^(.*?[^.])(\.{3,})((?:\(no files to check\))?(?:Passed|Failed|Skipped))$")


# ---------------------------------------------------------------- line fitting (text verbatim)
def leader(s: str, n: int = COLS) -> str:
    """A pre-commit hook row wider than the terminal: the house '…' cut placed inside its dot
    leader, the verdict kept. Only padding dots are dropped."""
    if len(s) <= n:
        return s
    m = _HOOK.match(s)
    assert m, s
    name, dots, tail = m.groups()
    keep = n - len(name) - len(tail) - 1
    assert keep >= 3, s
    out = cut(s, name + dots[:keep]) + tail
    assert out.replace("…", "." * (len(s) - len(out) + 1)) == s and len(out) <= n, (s, out)
    return out


def fit(lines):
    """Capture lines ready to print: hook rows cut in their leader; everything else must fit."""
    out = []
    for x in lines:
        s, c = (x, None) if isinstance(x, str) else x
        s = leader(s) if _HOOK.match(s) else s
        assert len(s) <= COLS, s
        out.append((s, c) if c else s)
    return out


# ---------------------------------------------------------------- terminal helpers (S09's)
def strip_top20(rows: int) -> float:
    return BOTTOM + rows * line_pitch(PT) + 0.85


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
    scene.remove(gone)
    if len(stay):
        scene.play(stay.animate.shift(UP * t.pitch * over), run_time=run_time * 0.6)


def out(scene, t, lines, run_time: float = 0.6, lag: float = 0.08) -> VGroup:
    """Print capture lines ((text, colour) or text) in chunks that fit; returns the new rows."""
    items = [(x, None) if isinstance(x, str) else x for x in fit(lines)]
    k = max(1, min(t.rows, 4))
    chunks = [items[i:i + k] for i in range(0, len(items), k)]
    rows = VGroup()
    for ch in chunks:
        room(scene, t, len(ch))
        rows.add(*t.print(scene, [(s, c) if c else s for s, c in ch], run_time=run_time / len(chunks) + 0.1,
                          lag=lag))
    return rows


def typ(scene, t, cmd: str, type_time: float | None = None, rows: list[str] | None = None):
    """type_cmd with room made first. `rows`: a hand fold for a command the house fold would
    break inside its quotes (asserted to paste back as exactly `cmd`)."""
    if len(t.lines) and getattr(t.lines[-1], "bare", False):
        last = t.lines[-1]
        scene.remove(last, *last.submobjects)
        t.lines.remove(last)
    p = t.prompt + " "
    if rows is None:
        room(scene, t, len(t.fold(p + cmd, first_prefix=len(p))))
        return type_cmd(scene, t, cmd, type_time)
    parts = [r[:-2] if r.endswith(" \\") else r for r in rows]
    assert all(r.endswith(" \\") for r in rows[:-1]) and all(len(r) <= COLS for r in rows), rows
    assert " ".join([parts[0]] + [q.lstrip(" ") for q in parts[1:]]) == p + cmd, rows
    room(scene, t, len(rows))
    t.fold = lambda text, first_prefix=0: list(rows)
    try:
        return type_cmd(scene, t, cmd, type_time)
    finally:
        del t.fold


def bare(scene, t):
    """The prompt returns with no output."""
    room(scene, t, 1)
    ln = t.type(scene, "", type_time=0)
    ln.bare = True
    return ln


def rows_of(line) -> list:
    return list(line.rows) if hasattr(line, "rows") else [line]


def find_in(line, sub: str) -> VGroup:
    """The glyphs of `sub` in a typed command, on whichever of its folded rows holds it."""
    for r in rows_of(line):
        if sub in r.text:
            return substring(r, sub)
    raise KeyError(f"{sub!r} is not on one row of {[r.text for r in rows_of(line)]}")


def flash(tg, color, scale: float = 1.15, run_time: float = 0.7) -> list:
    """Flash a filled tag: its word and its outline (Indicate on the whole tag hides the word)."""
    return [Indicate(tg.text, color=color, scale_factor=scale, run_time=run_time),
            tg.box.animate(rate_func=there_and_back, run_time=run_time).set_stroke(width=4)]


def each(pieces, color, scale: float = 1.1, lag: float = 0.15):
    """Flash scattered pieces one by one (one Indicate on their group pulls glyphs off rows)."""
    return LaggedStart(*[Indicate(p, color=color, scale_factor=scale) for p in pieces], lag_ratio=lag)


def tag_on(scene, t, line, mk, buff: float = 0.45):
    """Pin a row tag beside a typed command; when the row has no room, the house tag stands over
    the terminal's top-right corner and the command is underlined YELLOW. Returns (key, tag)."""
    rs = rows_of(line)
    tg = beside(mk(), rs[-1], buff=buff)
    if tg.get_right()[0] <= 6.55:
        pin(scene, rs[-1], tg)
        return rs[-1], tg
    yt = your_turn()
    yt.move_to([6.4 - yt.width / 2, t.box.get_top()[1] + 0.06 + yt.height / 2, 0])
    p = len(t.prompt) + 1
    typed = VGroup(*[glyph_range(r, p if r is rs[0] else 0) for r in rs])
    ul = under(typed, TURN, stroke=3)
    scene.play(FadeIn(yt, shift=LEFT * 0.1), Create(ul), run_time=0.5)
    attach(scene, rs[-1], ul)
    return (rs[-1], ul), yt


def drop_tag(scene, key, tg):
    if isinstance(key, tuple):
        r, ul = key
        scene.play(FadeOut(VGroup(tg, ul)), run_time=0.3)
        if ul in r.submobjects:
            r.remove(ul)
        scene.remove(tg, ul)
    else:
        unpin(scene, key, tg)


def wipe(scene, t, *extra, run_time: float = 0.4):
    """Clear the terminal's rows (and their pinned marks) together with `extra` overlays."""
    gone = VGroup(*t.lines.submobjects, *extra)
    if len(gone):
        scene.play(FadeOut(gone), run_time=run_time)
    scene.remove(gone, *gone.get_family())
    for m in list(t.lines):
        t.lines.remove(m)


# ---------------------------------------------------------------- pictures
def cfg_panel(a: int, b: int):
    """CODE(.pre-commit-config.yaml: a–b) at 20 pt; line 16 (96 characters) gets the house cut."""
    lines = excerpt(CFG, a, b).split("\n")
    cuts = []
    for i, s in enumerate(lines):
        if len(s) > COLS:
            lines[i] = cut(s, "secrets of one")
            assert len(lines[i]) <= 66, lines[i]
            cuts.append(i)
    p = code_panel("\n".join(lines), shown_path(CFG), a, "yaml", font_size=20)
    for i in cuts:                      # pygments paints the cut's "…" as an error (pink)
        code_span(p.code, i, "…").set_color(S.GREY)
    return p.move_to([0, 0, 0]).align_to([0, 2.8, 0], UP)


def light(arch, color=INK, run_time: float = 0.4):
    """Animation: an idle arch lights (frame and lamp) without taking a pass/fail state."""
    return AnimationGroup(arch.frame.animate.set_stroke(color), arch.lamp.animate.set_color(color),
                          run_time=run_time)


def style_card(head: str, body: str, color) -> VGroup:
    h = label(head, 26, color)
    b = label(body, 22, INK)
    inner = VGroup(h, b).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
    frame = outline_box(6.2, inner.height + 0.7, color, solid=True, fill_opacity=0.08)
    assert inner.width <= 6.2 - 0.6, inner.width
    inner.move_to(frame).align_to(frame, LEFT).shift(RIGHT * 0.35)
    g = VGroup(frame, inner)
    g.frame, g.head, g.body = frame, h, b
    return g


class Gauge(VGroup):
    """A coverage gauge 0–100 % with the floor marked: .track .fill .floor .floor_label .value (None at first).
    set_to(pct, colour) -> animations."""

    def __init__(self, x0: float, x1: float, y: float, floor: float = 90, **kw):
        super().__init__(**kw)
        self.x0, self.x1, self.y = x0, x1, y
        h = 0.24
        self.track = Rectangle(width=x1 - x0, height=h, stroke_color=S.GREY, stroke_width=2) \
            .move_to([(x0 + x1) / 2, y, 0])
        self.fill = self._bar(0.5, PASS)
        xf = self.x(floor)
        self.floor = Line([xf, y - 0.26, 0], [xf, y + 0.26, 0], color=INK, stroke_width=4)
        self.floor_label = label("floor 90%", 20, INK).next_to(self.floor, UP, buff=0.08)
        self.name = label("coverage", 20, S.GREY).next_to(self.track, LEFT, buff=0.2)
        self.value = None
        self.add(self.track, self.fill, self.floor, self.floor_label, self.name)

    def x(self, pct: float) -> float:
        return self.x0 + (self.x1 - self.x0) * pct / 100

    def _bar(self, pct: float, color) -> Rectangle:
        w = max(0.02, self.x(pct) - self.x0)
        return Rectangle(width=w, height=0.24, stroke_width=0).set_fill(color, 0.75) \
            .move_to([self.x0 + w / 2, self.y, 0])

    def set_to(self, pct: float, text: str, color) -> list:
        val = steady(text, 20, color, mono_font=True).next_to(self.track, RIGHT, buff=0.2)
        old = self.value
        if old is not None:
            self.remove(old)
        self.add(val)
        self.value = val                  # a cross-fade: a morph between two numbers garbles them
        fade = [FadeOut(old, shift=UP * 0.15)] if old is not None else []
        return [Transform(self.fill, self._bar(pct, color)), *fade, FadeIn(val, shift=UP * 0.15)]


class JustCheck(VoiceScene):
    def construct(self):
        assert len(SAY) == 6, len(SAY)

        sw3, setup3, hook = capture("babykev/s03-01"), capture("babykev/s03-02"), capture("babykev/s03-05")
        show, check, floor = capture("babykev/s03-08"), capture("babykev/s03-09"), capture("babykev/s03-10")
        brk, yl, rst, lc = (capture("babykev/s03-12"), capture("babykev/s03-13"), capture("babykev/s03-14"),
                            capture("babykev/s03-28"))
        perl, c1, st, rst2 = (capture("babykev/s03-30"), capture("babykev/s03-31"), capture("babykev/s03-32"),
                              capture("babykev/s03-33"))
        env, c2, undo = capture("babykev/s03-34"), capture("babykev/s03-35"), capture("babykev/s03-36")
        d4, d4b, c4b = capture("babykev/s04-04"), capture("babykev/s04b-03"), capture("babykev/s04b-09")
        assert sw3.cmd == "git switch --detach step-03" and setup3.cmd == "just setup", (sw3.cmd, setup3.cmd)
        assert hook.cmd == walk(230)[2:] and show.cmd == walk(245)[2:] and check.cmd == walk(249)[2:]
        assert floor.cmd == walk(253)[2:] and yl.cmd == walk(261)[2:] and rst.cmd == walk(262)[2:]
        assert lc.cmd == walk(288)[2:] and perl.cmd == walk(296)[2:] and c1.cmd == walk(297)[2:]
        assert st.cmd == walk(301)[2:] and rst2.cmd == walk(302)[2:] and env.cmd == walk(306)[2:]
        assert c2.cmd == walk(307)[2:] and undo.cmd == walk(311)[2:]
        assert d4.cmd == walk(348)[2:] and d4b.cmd == walk(419)[2:]
        # the capture ran the Linux sed; the walk spells it for a Mac (sed -i '' …)
        assert walk(260)[2:].replace("sed -i '' ", "sed -i ") == brk.cmd, brk.cmd
        assert all(x.exit == 0 for x in (brk, rst, perl, rst2, env, undo))
        sentence = c2.line(8)
        assert excerpt(CFG, 16, 16).strip() == "entry: " + sentence, sentence

        # ========================================================== 0. just setup; the hook file
        tr = tracker("E", 4)
        ref = lref("34–43")
        t = term(P_BABYKEV, rows=11, title=T_BABYKEV, size=PT)
        cap0 = VGroup(label("this machine's path", 22, TURN), label("· why it is never committed", 22, INK))
        cap0.arrange(RIGHT, buff=0.15)
        cap0[1].align_to(cap0[0], DOWN)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(ref), FadeIn(t, shift=UP * 0.2), run_time=0.8)
            typ(self, t, sw3.cmd, type_time=0.8)
            out(self, t, [cut(sw3.line(3), "and docstrings")], run_time=0.3)
            vo.wait_until("one recipe, just setup")
            s_ln = typ(self, t, setup3.cmd, type_time=0.5)
            s_out = out(self, t, setup3.at(2, "…", 19, "…", 25), run_time=0.7)
            how, hooked = s_out[0], s_out[4]
            vo.wait_until("lockfile sync")
            r_sync = ring(substring(how, "uv sync --locked"), INK, buff=0.05)
            self.play(Create(r_sync), run_time=0.4)
            vo.wait_until("hook install together")
            r_inst = ring(substring(how, "uv run pre-commit install"), INK, buff=0.05)
            r_hook = ring(hooked.glyphs, TURN, buff=0.06)
            self.play(Create(r_inst), run_time=0.4)
            self.play(Create(r_hook), Indicate(substring(hooked, ".git/hooks/pre-commit"), color=TURN,
                                               scale_factor=1.08), run_time=0.7)
            for r, m in ((how, r_sync), (how, r_inst), (hooked, r_hook)):
                attach(self, r, m)
            vo.wait_until("Pause and run it.")
            k_setup, y_setup = tag_on(self, t, s_ln, turn_row)
            self.play(*flash(y_setup, TURN), run_time=0.7)
            vo.wait_until("The walk's next command")
            wipe(self, t)
            c_ln = typ(self, t, hook.cmd, type_time=1.2)
            h_out = out(self, t, hook.at((2, 3), "…", (6, 9), "…", 15), run_time=0.9)
            l7, l8, l15 = h_out[4], h_out[5], h_out[8]
            assert l7.text.startswith("INSTALL_PYTHON=") and l15.text.strip().startswith("exec"), (l7.text, l15.text)
            vo.wait_until("the same hand-over chain")
            r_cfg = ring(substring(l8, ".pre-commit-config.yaml"), IMAGE, buff=0.05)
            r_pc = ring(substring(l15, "-mpre_commit"), TOOL, buff=0.05)
            self.play(Create(r_pc), run_time=0.5)
            hand = beside(row_tag("→ pre-commit", TOOL), l15)
            pin(self, l15, hand)
            self.play(Create(r_cfg), run_time=0.5)
            attach(self, l15, r_pc)
            attach(self, l8, r_cfg)
            vo.wait_until("with one difference")
            path = substring(l7, "/home/student/babykev/.venv/bin/python")
            bar7 = hl_bar(path, TURN, 0.28)
            self.play(FadeIn(bar7), path.animate.set_color(TURN), run_time=0.6)
            self.remove(bar7)
            l7.add_to_back(bar7)                 # behind the glyphs, and part of the row
            self.add(l7)
            vo.wait_until("This machine's own venv path")
            cap0.move_to([0, (t.box.get_top()[1] + 2.9) / 2, 0])
            self.play(FadeIn(cap0, shift=DOWN * 0.15), Indicate(path, color=TURN, scale_factor=1.06), run_time=0.8)
            vo.wait_until("so it is never committed")
            self.play(Indicate(cap0[1], color=INK, scale_factor=1.08), run_time=0.8)

        # ========================================================== 1. four hooks; just check = four checks
        panels = [cfg_panel(a, b) for a, b in WINDOWS]
        ch = Turnstile(9, None, arch_w=0.6, arch_h=0.75, gap=0.23)
        ch_names = ch.name_labels(CHEESE_HOOKS, color=S.GREY)
        bk = Turnstile(4, None, arch_w=0.6, arch_h=0.75, gap=0.45)
        bk_names = bk.name_labels(BABYKEV_HOOKS)
        chg, bkg = VGroup(ch, ch_names), VGroup(bk, bk_names)
        pair = VGroup(chg, bkg).arrange(RIGHT, buff=0.5, aligned_edge=DOWN)
        pair.move_to([0, 0, 0]).shift(UP * (-3.45 - pair.get_bottom()[1]))
        y_cap = (panels[0].get_bottom()[1] + pair.get_top()[1]) / 2
        ch_cap = note("cheese-app-ci-cd · 9 hooks", S.GREY, 20).move_to([chg.get_center()[0], y_cap, 0])
        bk_cap = note("babykev · 4 hooks", INK, 20).move_to([bkg.get_center()[0], y_cap, 0])
        assert all(p.get_bottom()[1] > ch_cap.get_top()[1] + 0.05 for p in panels)
        assert ch_cap.get_bottom()[1] > pair.get_top()[1] + 0.05, (ch_cap.get_bottom(), pair.get_top())
        p0, p1 = panels

        with self.voiceover(SAY[1]) as vo:
            gone = VGroup(t, cap0)
            self.play(FadeOut(gone), run_time=0.5)
            self.remove(gone, *gone.get_family())
            for m in list(t.lines):
                t.lines.remove(m)
            self.play(FadeIn(p0, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("four hooks, not nine")
            self.play(FadeIn(VGroup(ch, ch_names, ch_cap)), FadeIn(bk_cap),
                      LaggedStart(*[FadeIn(a, shift=DOWN * 1.0) for a in bk.arches], lag_ratio=0.15),
                      FadeIn(bk.floor), run_time=0.9)
            vo.wait_until("large files,")
            b9 = line_bar(p0.code, 9 - 5, TURN, 0.18)
            self.play(FadeIn(b9), FadeIn(bk_names[0], shift=UP * 0.1), light(bk.arches[0]), run_time=0.5)
            self.play(each([bk_names[0], ch_names[3]], TURN, 1.15, lag=0.0), run_time=0.6)
            vo.wait_until("merge markers,")
            b11 = line_bar(p0.code, 11 - 5, TURN, 0.18)
            self.play(FadeIn(b11), FadeIn(bk_names[1], shift=UP * 0.1), light(bk.arches[1]), run_time=0.5)
            self.play(each([bk_names[1], ch_names[5]], TURN, 1.15, lag=0.0), run_time=0.6)
            vo.wait_until("a policy hook")
            b14 = line_bar(p0.code, 14 - 5, TURN, 0.18)
            self.play(FadeIn(b14), FadeIn(bk_names[2], shift=UP * 0.1), light(bk.arches[2]), run_time=0.5)
            vo.wait_until("refusing any dot env file")
            self.play(FadeOut(VGroup(p0, b9, b11, b14), shift=UP * 0.3), FadeIn(p1, shift=UP * 0.3), run_time=0.6)
            b16 = line_bar(p1.code, 16 - 15, TURN, 0.18)
            b18 = line_bar(p1.code, 18 - 15, TURN, 0.18)
            self.play(FadeIn(b16), FadeIn(b18), run_time=0.4)
            vo.wait_until("one local hook that runs just check")
            b21 = line_bar(p1.code, 21 - 15, TURN, 0.18)
            self.play(FadeOut(VGroup(b16, b18)), FadeIn(b21), FadeIn(bk_names[3], shift=UP * 0.1),
                      light(bk.arches[3]), run_time=0.5)
            self.play(Indicate(code_span(p1.code, 21 - 15, "just check"), color=TURN, scale_factor=1.12),
                      Indicate(bk_names[3], color=TURN, scale_factor=1.15), run_time=0.7)
            vo.wait_until("So the hook runs exactly what you type")
            b23 = line_bar(p1.code, 23 - 15, TURN, 0.18)
            b24 = line_bar(p1.code, 24 - 15, TURN, 0.18)
            self.play(FadeIn(b23), FadeIn(b24), run_time=0.4)
            self.play(each([code_span(p1.code, 8, "pass_filenames: false"),
                            code_span(p1.code, 9, "always_run: true")], TURN, 1.1, lag=0.3), run_time=0.9)

            # the strip: step-03's recipe, its four checks fed by the `just check` arch
            vo.wait_until("At this step")
            gone = VGroup(p1, b21, b23, b24, chg, ch_cap, bk_cap)
            self.play(FadeOut(gone), run_time=0.5)
            self.remove(gone, *gone.get_family())
            s = term(P_BABYKEV, rows=5, title=T_BABYKEV, size=PT)
            band_lo = strip_top20(5) + 0.15
            self.play(bkg.animate.move_to([-3.7, (band_lo + 2.8) / 2 - 0.1, 0]), FadeIn(s, shift=UP * 0.2),
                      run_time=0.7)
            typ(self, s, show.cmd, type_time=0.6)
            x_stack = 0.4
            ys = [2.25 - 0.62 * i for i in range(4)]
            src = bk.arches[3]
            feed = arrow(src.get_right() + RIGHT * 0.1, np.array([x_stack - 0.25, (ys[0] + ys[-1]) / 2, 0]), INK)
            self.play(GrowArrow(feed), Indicate(bk_names[3], color=INK, scale_factor=1.12), run_time=0.5)
            stack = VGroup()
            for n, (anchor, sub) in enumerate(zip(("format check", "lint,", "tests with a 90 percent coverage floor",
                                                   "config linting"),
                                                  ("just fmt --check", "just lint",
                                                   "just test -q --cov-fail-under=90", "just lint-config"))):
                vo.wait_until(anchor)
                row = out(self, s, show.at(9 + n), run_time=0.3)[0]
                assert row.text.strip() == sub, row.text
                g = substring(row, sub)
                fly = g.copy()
                dot = Dot(radius=0.06, color=INK).move_to([x_stack, ys[n], 0])
                self.play(fly.animate.move_to([x_stack + 0.25 + g.width / 2, ys[n], 0]), FadeIn(dot),
                          Indicate(g, color=INK, scale_factor=1.06), run_time=0.6)
                stack.add(VGroup(dot, fly))
            u90 = under(stack[2][1][-len("--cov-fail-under=90"):], TURN, stroke=3)
            self.play(Create(u90), run_time=0.5)

        # ========================================================== 2. just check: green; the floor bites
        t = term(P_BABYKEV, rows=12, title=T_BABYKEV, size=PT)
        gauge = Gauge(-5.0, -0.9, 2.15)

        with self.voiceover(SAY[2]) as vo:
            gone = VGroup(bkg, feed, stack, u90, *s.lines)
            self.play(FadeOut(gone), run_time=0.5)
            self.remove(gone, *gone.get_family())
            for m in list(s.lines):
                s.lines.remove(m)
            self.play(ReplacementTransform(s, t), run_time=0.6)      # the strip grows into the terminal
            vo.wait_until("Run just check")
            jc_ln = typ(self, t, check.cmd, type_time=0.5)
            j_out = out(self, t, check.at((2, 6)) + [cut(check.line(7), "." * 53), "…"] + check.at((18, 21)),
                        run_time=1.0)
            ok, l18, l19 = j_out[3], j_out[7], j_out[8]
            vo.wait_until("everything green")
            self.play(ok.animate.set_color(PASS), l18.animate.set_color(PASS),
                      substring(l19, "53 passed").animate.set_color(PASS), run_time=0.5)
            k_jc, y_jc = tag_on(self, t, jc_ln, turn_row)
            vo.wait_until("the floor reads 100 percent")
            self.play(FadeIn(gauge.track), FadeIn(gauge.floor), FadeIn(gauge.floor_label), FadeIn(gauge.name),
                      run_time=0.4)
            self.play(*gauge.set_to(100, "100.00%", PASS),
                      Indicate(substring(l18, "100.00%"), color=PASS, scale_factor=1.15), run_time=0.9)
            vo.wait_until("Now watch it bite")
            resize(self, t, 12, keep=[jc_ln, l18], run_time=0.5)
            f_ln = typ(self, t, floor.cmd, type_time=0.9)
            vo.wait_until("ask for only the confidence tests")
            self.play(Indicate(find_in(f_ln, "-k confidence"), color=INK, scale_factor=1.1),
                      Indicate(find_in(f_ln, "--cov-fail-under=90"), color=TURN, scale_factor=1.1),
                      run_time=0.7)
            f_out = out(self, t, floor.at(2, "…", (11, 12), "…", 25) + [cut(floor.line(26), "in 0.17s")], run_time=0.9)
            l11, l12, l25, l26 = f_out[2], f_out[3], f_out[5], f_out[6]
            vo.wait_until("9 tests pass")
            self.play(Indicate(substring(l11, "........."), color=INK, scale_factor=1.15),
                      Indicate(substring(l26, "9 passed"), color=INK, scale_factor=1.15), run_time=0.7)
            vo.wait_until("half the code is never exercised")
            self.play(Indicate(substring(l12, "total of 49"), color=ERR, scale_factor=1.15), run_time=0.7)
            vo.wait_until("fails at 49.4 percent coverage")
            self.play(l25.animate.set_color(ERR), *gauge.set_to(49.4, "49.40%", ERR), run_time=0.8)
            self.play(Indicate(substring(l25, "49.40%"), color=ERR, scale_factor=1.15),
                      Indicate(gauge.floor, color=INK, scale_factor=1.3), run_time=0.7)
            vo.wait_until("A floor is a gate, not a goal.")
            self.play(Indicate(gauge.floor_label, color=INK, scale_factor=1.15),
                      Wiggle(gauge.fill, scale_value=1.05, rotation_angle=0.01 * TAU), run_time=0.9)
            vo.wait_until("Pause and run both.")
            k_fl, y_fl = tag_on(self, t, f_ln, turn_row)
            self.play(*flash(y_jc, TURN), *flash(y_fl, TURN), run_time=0.8)

        # ========================================================== 3. config files are checked too
        card = code(CFG, 9, 10, font_size=20)
        sed_rows = ["student@laptop:~/babykev$ sed -i \\",
                    "  's/^        args: \\[--maxkb=1000\\]$/          args: [--maxkb=1000]/' \\",
                    "  .pre-commit-config.yaml"]
        chips = VGroup(*[grey_chip(s, 20, mono_font=True) for s in ("validate-pyproject", "uv lock --check",
                                                                    "just --fmt --check")])
        chips.arrange(RIGHT, buff=0.35)

        with self.voiceover(SAY[3]) as vo:
            drop = VGroup(gauge, y_fl, *([k_fl[1]] if isinstance(k_fl, tuple) else []))
            self.play(FadeOut(VGroup(*t.lines, drop)), run_time=0.5)
            self.remove(*t.lines, drop, *drop.get_family())
            for m in list(t.lines):
                t.lines.remove(m)
            resize(self, t, 10, keep=0, run_time=0.5)
            card.move_to([0, (t.box.get_top()[1] + 2.85) / 2, 0])
            vo.wait_until("Config files are checked too")
            self.play(FadeIn(card, shift=DOWN * 0.15), run_time=0.6)
            args = code_span(card.code, 1, "args: [--maxkb=1000]")
            vo.wait_until("a broken hook config breaks every commit")
            self.play(Indicate(card.header, color=INK, scale_factor=1.08), run_time=0.6)
            vo.wait_until("One wrong indent")
            typ(self, t, brk.cmd, type_time=1.6, rows=sed_rows)
            bare(self, t)
            bar10 = line_bar(card.code, 1, ERR, 0.2)
            self.play(args.animate.shift(RIGHT * 2 * 0.1667).set_color(ERR), FadeIn(bar10), run_time=0.6)
            typ(self, t, yl.cmd, type_time=0.6)
            y_out = out(self, t, [yl.line(2), cut(yl.line(3), "not allowed here")], run_time=0.5)
            err = y_out[1]
            vo.wait_until("yamllint names the exact line")
            r1015 = ring(substring(err, "10:15"), ERR, buff=0.05)
            self.play(err.animate.set_color(ERR), Create(r1015), run_time=0.5)
            attach(self, err, r1015)
            self.play(Indicate(substring(err, "10:15"), color=ERR, scale_factor=1.2),
                      Indicate(args, color=ERR, scale_factor=1.08), run_time=0.8)
            vo.wait_until("Restored,")
            typ(self, t, rst.cmd, type_time=0.6)
            bare(self, t)
            self.play(args.animate.shift(LEFT * 2 * 0.1667).set_color(INK), FadeOut(bar10), run_time=0.6)
            vo.wait_until("the recipe runs green")
            typ(self, t, lc.cmd, type_time=0.4)
            l_out = out(self, t, ["…"] + lc.at((7, 8)), run_time=0.5)
            valid, locked = l_out[1], l_out[2]
            self.play(valid.animate.set_color(PASS), locked.animate.set_color(PASS), run_time=0.5)
            vo.wait_until("it also validates pyproject.toml")
            chips.move_to(card)
            self.play(FadeOut(card, shift=UP * 0.15), FadeIn(chips[0], shift=DOWN * 0.15),
                      Indicate(substring(valid, "pyproject.toml"), color=PASS, scale_factor=1.1), run_time=0.7)
            self.remove(card)
            vo.wait_until("checks the lockfile")
            self.play(FadeIn(chips[1], shift=DOWN * 0.15),
                      Indicate(substring(locked, "Resolved 29 packages"), color=PASS, scale_factor=1.1), run_time=0.6)
            self.play(FadeIn(chips[2], shift=DOWN * 0.15), run_time=0.5)

        # ========================================================== 4. the gate refuses, twice
        quote = VGroup(label(sentence, 22, INK))
        q_box = box(quote.width + 0.5, quote.height + 0.32, ERR, fill_opacity=0.12, radius=0.12)

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(chips, ref, *t.lines)), run_time=0.5)
            self.remove(chips, ref, *t.lines)
            for m in list(t.lines):
                t.lines.remove(m)
            resize(self, t, 12, keep=0, run_time=0.5)
            vo.wait_until("Now the gate refuses, twice")
            p_ln = typ(self, t, perl.cmd, type_time=1.2)
            bare(self, t)
            cm_ln = typ(self, t, c1.cmd, type_time=0.6)
            vo.wait_until("pause and try the first")
            k_c1, y_c1 = tag_on(self, t, cm_ln, turn_row)
            self.play(*flash(y_c1, TURN), run_time=0.7)
            vo.wait_until("An unused import goes in")
            self.play(Indicate(find_in(p_ln, "import os"), color=INK, scale_factor=1.15), run_time=0.7)
            vo.wait_until("the commit fails on F401")
            o1 = out(self, t, c1.at((6, 9), "…", (16, 17), "…", 32), run_time=0.9)
            v_pass = [substring(o1[i], "Passed") for i in (0, 1)]
            self.play(*[v.animate.set_color(PASS) for v in v_pass], substring(o1[2], "Skipped").animate.set_color(SKIP),
                      o1[3].animate.set_color(ERR), substring(o1[5], "F401").animate.set_color(ERR), run_time=0.6)
            self.play(Indicate(substring(o1[3], "Failed"), color=ERR, scale_factor=1.2),
                      Indicate(substring(o1[5], "F401"), color=ERR, scale_factor=1.2), run_time=0.7)
            vo.wait_until("no commit made")
            typ(self, t, st.cmd, type_time=0.4)
            s_out = out(self, t, st.at((2, 3), "…", 6), run_time=0.5)
            nc = beside(row_tag("no commit", S.GREY), s_out[3])
            pin(self, s_out[3], nc)
            typ(self, t, rst2.cmd, type_time=0.6)
            bare(self, t)
            vo.wait_until("Then a dot env file is staged")
            wipe(self, t)
            typ(self, t, env.cmd, type_time=0.7)
            bare(self, t)
            typ(self, t, c2.cmd, type_time=0.5)
            o2 = out(self, t, c2.at((2, 7)) + [cut(sentence, "It is never")] + c2.at((9, 10)), run_time=0.9)
            fail_env, said = o2[2], o2[6]
            self.play(*[substring(o2[i], "Passed").animate.set_color(PASS) for i in (0, 1)],
                      fail_env.animate.set_color(ERR), run_time=0.5)
            vo.wait_until("the refusal is the config's own sentence")
            self.play(said.animate.set_color(ERR), Indicate(substring(fail_env, "Failed"), color=ERR, scale_factor=1.2),
                      run_time=0.6)
            q = VGroup(q_box, quote)
            quote.move_to(q_box)
            q.move_to([0, (t.box.get_top()[1] + 2.88) / 2, 0])
            r_said = ring(said.glyphs, ERR, buff=0.05)
            vo.wait_until("a dot env file holds the settings")
            # the cut row, quoted whole above the terminal (a morph between the two fonts smears)
            self.play(Create(r_said), Create(q_box), FadeIn(quote, shift=UP * 0.25), run_time=0.9)
            attach(self, said, r_said)
            vo.wait_until("It is never committed.")
            tail = quote[0][-len("Itisnevercommitted"):]
            self.play(Indicate(tail, color=ERR, scale_factor=1.08), run_time=0.8)
            typ(self, t, undo.cmd, type_time=0.7)
            bare(self, t)

        # ========================================================== 5. two styles; docs join the gate
        cards = VGroup(style_card("babykev", "check points, you run just fmt yourself", VENV),
                       style_card("cheese", "black rewrites, you look and re-stage", IMAGE))
        cards.arrange(RIGHT, buff=0.3)
        cards.move_to([0, 2.75 - cards.height / 2, 0])
        t2 = term(P_BABYKEV, rows=11, title=T_BABYKEV, size=PT)
        gt = GateTable(keys=("tests", "format", "docs", "config", "system"), filled=("tests", "system"),
                       rows={"config": ("config files", "yamllint, uv, just", "just lint-config", "yes", True)})
        gt.shift(UP * (cards.get_bottom()[1] - 0.35 - gt.get_top()[1]))     # under the style cards
        assert gt.get_bottom()[1] >= -3.5, gt.get_bottom()
        cc_lines = fit(c4b.at((5, 7), "…", (35, 36)))
        cc = term(P_BABYKEV, rows=len(cc_lines), title=c4b.cmd, size=PT, place=False)
        cc.move_to([0, 0.35, 0])
        cc_chip = grey_chip("one deleted description blocks the commit", 22)
        cc_chip.next_to(cc.box, DOWN, buff=0.3)

        with self.voiceover(SAY[5]) as vo:
            gone = VGroup(t, q_box, quote)
            self.play(FadeOut(gone), track(tr, 5), run_time=0.6)
            self.remove(gone, *gone.get_family())
            vo.wait_until("Two gate styles, both fine")
            self.play(FadeIn(cards[0].frame), FadeIn(cards[1].frame), FadeIn(gt), run_time=0.6)
            vo.wait_until("this one points and you run just fmt")
            self.play(FadeIn(cards[0].head), FadeIn(cards[0].body, shift=RIGHT * 0.2), run_time=0.6)
            gt.fill(self, "format", run_time=0.6)           # just check's fmt --check + lint: the row S09 left empty
            vo.wait_until("the cheese gate rewrites and makes you look")
            self.play(FadeIn(cards[1].head), FadeIn(cards[1].body, shift=RIGHT * 0.2), run_time=0.6)
            gt.settle(self, "format")
            vo.wait_until("Steps 4 and 4 b put documentation in the gate")
            self.play(FadeOut(VGroup(cards, gt)), FadeIn(t2, shift=UP * 0.2), run_time=0.6)
            self.remove(cards, gt)
            gt.move_to([0, -0.35, 0])                       # it returns centred for the last beat
            d_ln = typ(self, t2, d4.cmd, type_time=0.5)
            pin(self, d_ln, beside(row_tag("at step-04", S.GREY), d_ln))
            d_out = out(self, t2, d4.at((2, 7), "…", 93), run_time=0.8)
            l93 = d_out[7]
            vo.wait_until("first 50 of 88")
            self.play(substring(l93, "50 of 88").animate.set_color(ERR), run_time=0.3)
            self.play(Indicate(substring(l93, "50 of 88"), color=ERR, scale_factor=1.2), run_time=0.6)
            vo.wait_until("classes typed and documented")
            self.play(Indicate(substring(l93, "typed and documented"), color=INK, scale_factor=1.1), run_time=0.7)
            vo.wait_until("one step later 88 of 88")
            resize(self, t2, 11, keep=[d_ln, l93], run_time=0.5)
            e_ln = typ(self, t2, d4b.cmd, type_time=0.5)
            pin(self, e_ln, beside(row_tag("at step-04b", S.GREY), e_ln))
            e_out = out(self, t2, d4b.at((2, 9)), run_time=0.7)
            l9 = e_out[7]
            self.play(substring(l9, "88 of 88").animate.set_color(PASS), run_time=0.3)
            self.play(Indicate(substring(l9, "88 of 88"), color=PASS, scale_factor=1.2), run_time=0.6)
            vo.wait_until("deleting one description blocks a commit")
            self.play(FadeOut(t2), run_time=0.4)
            self.remove(t2, *t2.get_family())
            self.play(FadeIn(cc, shift=UP * 0.2), run_time=0.4)
            c_rows = cc.print(self, cc_lines, run_time=0.4, lag=0.08)
            self.play(c_rows[0].animate.set_color(ERR), substring(c_rows[4], "no docment").animate.set_color(ERR),
                      substring(c_rows[5], "87 of 88").animate.set_color(ERR), FadeIn(cc_chip, shift=UP * 0.15),
                      run_time=0.5)
            self.play(Indicate(substring(c_rows[0], "Failed"), color=ERR, scale_factor=1.2),
                      Indicate(substring(c_rows[4], "babykev.api:render(indent)"), color=ERR, scale_factor=1.1),
                      run_time=0.9)
            self.wait(0.6)
            vo.wait_until("Two rows join the table.")
            self.play(FadeOut(VGroup(cc, cc_chip)), run_time=0.5)
            self.remove(cc, cc_chip, *cc.get_family())
            self.play(FadeIn(gt), run_time=0.6)
            gt.fill(self, "docs", run_time=0.6)
            gt.settle(self, "docs")
            gt.fill(self, "config", run_time=0.6)
            gt.settle(self, "config")
            self.play(Indicate(gt.rows["docs"].cells[3], color=PASS, scale_factor=1.2),
                      Indicate(gt.rows["config"].cells[3], color=PASS, scale_factor=1.2), run_time=0.7)
        self.wait(0.8)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
