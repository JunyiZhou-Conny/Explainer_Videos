"""S10 · Guest lecture: uv, just, and two failing tests (part 2 opens; tracker E1 -> E3).

Beats (script.md, ## S10; one voiceover block each):
0. Empty frame after the part break. TRACKER E1 (tracker E appears, 8 dots) and `Lecture 9 · slides
   14–20, 25–28` (top right, whole scene). "Part 2 · guest lecture" (no name on screen); an
   unlabeled 4-arch turnstile drops under it ("the same gate"). An `illustration` of babykev: a
   README question card (README.md:13) -> babykev -> five option bars and a confidence; on "a pure
   guess" the bars level and the confidence reads 0. On "No Docker" the tracker's last dot is
   ringed TEAL with a dashed TEAL chip. Then a 6-row `laptop · babykev` terminal: two PURPLE chips
   (uv, just); `uv --version` (extra) -> babykev/02: 2 and `just --version` (extra) -> babykev/04:
   2, each output row tagged `at the time of recording`.
1. `git clone https://github.com/rahuldave/babykev` -> babykev/05: 2, `cd babykev` (prompt flashes),
   `git tag -n1 --list 'step-*'` (README.md:148) -> babykev/07: 2–10. The nine step names light in
   turn; a GREY row tag "the repo is its own slide deck"; a ring jumps between steps on "moves you to
   any step". `▶ your turn` on the clone's output row and on the tag command.
2. TRACKER E1. `git switch --detach step-00` (README.md:150) -> s00-01: 2; `uv sync --locked` (walk
   step-00) -> s00-02: 2–4, 6 (soft-wrapped), 9–10; `Using CPython 3.13.16` GREEN. The terminal
   shrinks to a 3-row strip (CPython + the warning) and the lockfile mechanism plays above it
   (tagged `illustration`): a dashed GREY "no lockfile" column whose versions tick upward as a
   time marker slides, and a GREEN `uv sync --locked` column under a GREEN `uv.lock` card with a lock
   glyph that shakes at every tick and prints a RED "stop". The warning row gets `at the time of
   recording`. A TEAL frost glyph "the cheese way: freeze an image". Then `just` -> s00-05: 2–6; the
   recipe names ringed; three row tags beside `[setup]` (for people GREY, the hook PURPLE, CI · later
   GREY). `▶ your turn`.
3. TRACKER E2. `git switch --detach step-01` -> s01-01: 3; `just setup` -> s01-02: 2–3, 9, …, 19;
   `uv run pytest` (walk step-01) -> s01-03: 10–11 (soft-wrapped), …, 53–54 (wrapped), 55 (its '='
   padding dropped, as S07 does): `2 failed` RED, `50 passed` GREEN. The terminal shrinks to a
   5-row strip holding 53–55; above it, a card (titled by its command) with s01-06: 32–35 (wrap):
   the guess `[1 / 3] * 3` YELLOW, `0.5` RED, `pytest.approx(0)` GREEN. Row tags: RED "77 × 0.01 =
   0.77" on the rounding test, GREEN "fix the code, not the tests" on the card. `▶ your turn`.
4. TRACKER E3. PURPLE chips `ruff format` / `ruff check` ("both roles"). V4 funnel reprise over a
   6-row strip: `uv run ruff check --statistics` (walk step-02) -> s02-12: 2–6, …, 14–15 ("Found 70
   errors."); `just lint --fix` -> s02-14: 692 (69); `just lint --fix --unsafe-fixes` -> s02-15:
   360 (37). The bar starts at 70 with a faint notch above it at 79 carrying the GREY chip
   `recorded · walk.md: 79 before just fmt` (not spoken); it settles at 37, "the rest need a person".
   Then three GREY dashed width chips from part 1 (black 88, flake8 79, hook + CI 120) fold into a
   GREEN card with CODE(babykev/pyproject.toml: 65), `line-length = 100` highlighted, and GREEN
   arrows run to both ruff chips. Fade to an empty frame.

Deviations (reported to the coordinator): the pyproject card shows line 65 only, not 60–65: lines
60–64 are comments of 100–109 characters that do not fit the frame at >= 20 pt. The terminal is
20 pt (72 characters a row, as S04/S05) so pytest's progress rows and test ids fit. Before "Two
tools first" the narration's bridge gets an `illustration` (babykev's question -> bars ->
confidence, from README.md:13 and the test's own rule) so the first 15 seconds move.
"""

import numpy as np  # noqa: I001  (manim first, then common: common must win)
from manim import *

from explainer.scene import VoiceScene
from explainer import style as S

from common import (BOTTOM, ERR, HOST, IMAGE, INK, NARRATION, P_BABYKEV, P_BABYKEV_HOME, PASS, TOOL,
                    TURN, T_BABYKEV, VENV, Turnstile, arrow, attach, beside, capture, cd_prompt, code, code_span,
                    dashed_chip, excerpt, extra_row, file_card, illustration_tag, label,
                    line_bar, line_pitch, lock_glyph, lref, mono, note, outline_box, pin, recorded_tag,
                    resize, ring, row_tag, steady, substring, term, time_row, tool_chip, track, tracker,
                    turn_row, type_cmd, walk, FindingsFunnel)

SAY = NARRATION["S10"]
PT = 20                                       # terminal size: 72 characters a row
README = "babykev/README.md"
PYPROJECT = "babykev/pyproject.toml"


def strip_top20(rows: int) -> float:
    """Top edge of a `rows`-row 20 pt terminal standing on BOTTOM."""
    return BOTTOM + rows * line_pitch(PT) + 0.85


def soft(lines: list[str], n: int) -> list[str]:
    """Long rows broken at their last space that fits a row (the text is the capture's, only the
    row break moves); a token longer than a row breaks at the edge, as a terminal wraps it."""
    out = []
    for s in lines:
        while len(s) > n:
            k = s.rfind(" ", 0, n + 1)
            if k > 0:
                out.append(s[:k].rstrip())
                s = s[k + 1:].lstrip()
            else:
                out.append(s[:n])
                s = s[n:]
        out.append(s)
    return out


def summary(cap, n: int) -> str:
    """A pytest summary line without its '=' padding (as S03/S07 show them)."""
    s = cap.line(n)
    assert s.startswith("=") and s.endswith("="), s
    return s.strip("= ")


def at_ids(lines: list[str]) -> list[str]:
    """pytest's 'FAILED path::test_id - …' rows broken after '::' (too long for a row; the text is
    the capture's, only the row break moves), so the test's name stays whole on its row."""
    out = []
    for s in lines:
        k = s.index("::") + 2
        out += [s[:k], s[k:]]
    return out


def readme_cmd(n: int) -> str:
    """babykev README.md line n without its trailing '# comment'."""
    return excerpt(README, n, n).split("#")[0].strip()


def flash_tag(tag, color) -> list:
    """Flash a filled row tag: its word and its outline (Indicate on the whole tag hides the word).
    A list to unpack into play(): wrapped in an AnimationGroup, the group's Group(text, box) is
    added on top of the row and the tag's filled box then hides its own word."""
    return [tag.box.animate(rate_func=there_and_back).set_stroke(width=4),
            Indicate(tag.text, color=color, scale_factor=1.2)]


# ---------------------------------------------------------------- beat 0: babykev, illustrated
OPTIONS = ("cow", "goat", "sheep", "buffalo", "mixed")      # README.md:14-17, the milk question
SURE = (0.86, 0.06, 0.04, 0.01, 0.03)                       # illustrative
BAR_MAX = 1.5


def bar_rect(p: float, x: float, base: float) -> Rectangle:
    h = max(0.04, BAR_MAX * p)
    return Rectangle(width=0.5, height=h, stroke_color=INK, stroke_width=1.5).set_fill(INK, 0.55) \
        .move_to([x, base + h / 2, 0])


def babykev_demo() -> VGroup:
    """README question card -> babykev -> five option bars + a confidence (illustration).
    .card .model .arrows .bars .names .conf .tag .xs .base"""
    q = VGroup(label("What kind of milk goes", 22, INK), label("into this cheese?", 22, INK))
    q.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    qbox = RoundedRectangle(width=q.width + 0.5, height=q.height + 0.45, corner_radius=0.14,
                            stroke_color=S.GREY, stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
    q.move_to(qbox)
    head = mono("README.md · line 13", 20, S.GREY).next_to(qbox, UP, buff=0.12).align_to(qbox, LEFT)
    card = VGroup(qbox, q, head).move_to([-4.55, 0.35, 0])
    mbox = RoundedRectangle(width=2.3, height=1.15, corner_radius=0.16, stroke_color=INK,
                            stroke_width=3).set_fill(S.GREY_DARKER, 1)
    model = VGroup(mbox, mono("babykev", 26, INK)).move_to([-1.05, 0.2, 0])
    model.box = mbox
    base = -0.35
    xs = [1.75 + 0.95 * i for i in range(5)]
    bars = VGroup(*[bar_rect(p, x, base) for p, x in zip(SURE, xs)])
    names = VGroup(*[label(s, 20, S.GREY).move_to([x, base - 0.27, 0]) for s, x in zip(OPTIONS, xs)])
    axis = Line([xs[0] - 0.45, base, 0], [xs[-1] + 0.45, base, 0], color=S.GREY, stroke_width=2)
    word = label("confidence", 24, INK)
    num = steady("0.8", 24, INK)
    conf = VGroup(word, num).arrange(RIGHT, buff=0.18).move_to([3.65, -1.25, 0])
    num.align_to(word, DOWN)
    conf.word, conf.num = word, num
    a1 = arrow(qbox.get_right(), mbox.get_left() + LEFT * 0.05, INK)
    a2 = arrow(mbox.get_right() + RIGHT * 0.05, np.array([xs[0] - 0.55, 0.2, 0]), INK)
    tag = illustration_tag().move_to([3.65, 1.75, 0])
    g = VGroup(card, model, a1, a2, axis, bars, names, conf, tag)
    g.card, g.model, g.arrows, g.bars, g.names, g.conf, g.tag = card, model, VGroup(a1, a2), bars, names, conf, tag
    g.axis, g.xs, g.base = axis, xs, base
    return g


# ---------------------------------------------------------------- beat 2: lockfile mechanism
PKGS = ("pydantic", "pytest", "coverage")
LOCKED = ("2.13.5", "9.1.1", "7.16.2")                      # s01-02's lock (step-01)
DRIFT = (("2.14.0", "9.2.0", "7.17.0"), ("2.15.1", "9.3.2", "7.18.1"))   # illustrative


def dep_rows(versions, color) -> VGroup:
    rows = VGroup(*[steady(f"{p}=={v}", 22, color, mono_font=True) for p, v in zip(PKGS, versions)])
    return rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22)


def frost_glyph(r: float = 0.55, color=IMAGE) -> VGroup:
    """A snowflake: three crossing spokes with V tips (the cheese way: freeze an image)."""
    g = VGroup()
    for k in range(6):
        ang = k * PI / 3
        d = np.array([np.cos(ang), np.sin(ang), 0])
        g.add(Line(ORIGIN, d * r, color=color, stroke_width=4))
        mid = d * r * 0.6
        for s in (1, -1):
            e = np.array([np.cos(ang + s * PI / 4), np.sin(ang + s * PI / 4), 0])
            g.add(Line(mid, mid + e * r * 0.3, color=color, stroke_width=3))
    return g


class OneCommand(VoiceScene):
    def construct(self):
        assert len(SAY) == 5, len(SAY)

        uv_v, just_v = capture("babykev/02"), capture("babykev/04")
        clone, tags = capture("babykev/05"), capture("babykev/07")
        sw0, sync, just0 = capture("babykev/s00-01"), capture("babykev/s00-02"), capture("babykev/s00-05")
        sw1, setup1, pyt = capture("babykev/s01-01"), capture("babykev/s01-02"), capture("babykev/s01-03")
        two = capture("babykev/s01-06")
        stats, fix, unsafe = capture("babykev/s02-12"), capture("babykev/s02-14"), capture("babykev/s02-15")
        assert tags.cmd == readme_cmd(148) and sw0.cmd == readme_cmd(150), (tags.cmd, sw0.cmd)
        assert sync.cmd == walk(22)[2:] and pyt.cmd == walk(65)[2:], (sync.cmd, pyt.cmd)
        assert stats.cmd == walk(181)[2:] and fix.cmd == walk(190)[2:] and unsafe.cmd == walk(195)[2:]
        assert just0.cmd == "just" and setup1.cmd == "just setup" and sw1.cmd == "git switch --detach step-01"

        # ========================================================== 0. part 2: babykev; two tools
        tr = tracker("E", 1)
        ref = lref("14–20, 25–28")
        title = VGroup(label("Part 2", 44, INK), label("guest lecture", 32, S.GREY)).arrange(DOWN, buff=0.2)
        title.move_to([0, 1.1, 0])
        gate = Turnstile(4, arch_w=0.6, arch_h=1.2, gap=0.25)
        gate.next_to(title, DOWN, buff=0.55)
        demo = babykev_demo()
        last_dot = tr.dots[-1]
        dot_ring = Circle(radius=0.17, color=IMAGE, stroke_width=3).move_to(last_dot)
        docker = dashed_chip("Docker: only at the very end", IMAGE)
        docker.move_to([-6.5 + docker.width / 2, 2.45, 0])
        t = term(P_BABYKEV_HOME, rows=6, title=T_BABYKEV, size=PT)
        uv_chip, just_chip = tool_chip("uv", size=26), tool_chip("just", size=26)
        uv_note = note("package manager · lecture 2", S.GREY, 20)
        just_note = note("command runner", S.GREY, 20)
        VGroup(uv_chip, uv_note).arrange(DOWN, buff=0.18).move_to([-3.2, 0.75, 0])
        VGroup(just_chip, just_note).arrange(DOWN, buff=0.18).move_to([3.2, 0.75, 0])

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(ref), FadeIn(title, shift=UP * 0.2), run_time=0.9)
            self.play(Indicate(tr.dots[0], color=TURN, scale_factor=1.8), run_time=0.7)
            vo.wait_until("It builds the same gate")
            self.play(FadeIn(gate, shift=DOWN * 1.2), run_time=0.8)
            self.play(Indicate(gate, color=INK, scale_factor=1.06), run_time=0.8)
            vo.wait_until("babykev, which")
            self.play(FadeOut(VGroup(title, gate), shift=UP * 0.3), FadeIn(demo.model, scale=0.9), run_time=0.7)
            self.remove(title, gate)
            vo.wait_until("answers questions about cheese")
            self.play(FadeIn(demo.card, shift=RIGHT * 0.2), GrowArrow(demo.arrows[0]), run_time=0.7)
            self.play(Indicate(demo.model.box, color=INK, scale_factor=1.05), GrowArrow(demo.arrows[1]),
                      Create(demo.axis), FadeIn(demo.names), FadeIn(demo.tag), run_time=0.7)
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in demo.bars], lag_ratio=0.15), run_time=0.8)
            vo.wait_until("reports how confident it is")
            self.play(FadeIn(demo.conf, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("a pure guess")
            level = [bar_rect(0.2, x, demo.base) for x in demo.xs]
            self.play(*[Transform(b, n) for b, n in zip(demo.bars, level)],
                      Transform(demo.conf.num, steady("0", 24, INK).move_to(demo.conf.num, aligned_edge=LEFT)),
                      run_time=1.0)
            vo.wait_until("should score zero")
            self.play(Indicate(demo.conf.num, color=INK, scale_factor=1.4), run_time=0.7)
            vo.wait_until("No Docker")
            self.play(Create(dot_ring), FadeIn(docker, shift=DOWN * 0.15), run_time=0.7)
            vo.wait_until("Two tools first")
            self.play(FadeOut(VGroup(demo, dot_ring, docker)), FadeIn(t, shift=UP * 0.2), run_time=0.7)
            self.remove(demo, dot_ring, docker)
            vo.wait_until("the package manager uv")
            self.play(FadeIn(uv_chip, shift=DOWN * 0.2), FadeIn(uv_note), run_time=0.5)
            uv_ln = type_cmd(self, t, uv_v.cmd, type_time=0.5)
            x1 = beside(extra_row(), uv_ln)
            pin(self, uv_ln, x1, anim=AnimationGroup(FadeIn(x1, shift=LEFT * 0.1), track(tr, extra=True)))
            uv_out = t.print(self, uv_v.at(2), run_time=0.4)[0]
            vo.wait_until("0.13.2")
            self.play(Indicate(substring(uv_out, "0.13.2"), color=INK, scale_factor=1.2), run_time=0.5)
            tt1 = beside(time_row(), uv_out)
            pin(self, uv_out, tt1)
            vo.wait_until("the command runner just")
            self.play(FadeIn(just_chip, shift=DOWN * 0.2), FadeIn(just_note), run_time=0.5)
            just_ln = type_cmd(self, t, just_v.cmd, type_time=0.5)
            x2 = beside(extra_row(), just_ln)
            pin(self, just_ln, x2)
            just_out = t.print(self, just_v.at(2), run_time=0.4)[0]
            vo.wait_until("1.59.0")
            tt2 = beside(time_row(), just_out)
            pin(self, just_out, tt2, anim=AnimationGroup(FadeIn(tt2, shift=LEFT * 0.1),
                                                         Indicate(substring(just_out, "1.59.0"), color=INK,
                                                                  scale_factor=1.2)))

        # ========================================================== 1. clone, tags
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(uv_chip, uv_note, just_chip, just_note)), track(tr, extra=False),
                      run_time=0.5)
            self.remove(uv_chip, uv_note, just_chip, just_note)
            t.clear(self)
            resize(self, t, 13, keep=0)
            type_cmd(self, t, clone.cmd, type_time=1.2)
            c_out = t.print(self, clone.at(2), run_time=0.3)[0]
            type_cmd(self, t, "cd babykev", type_time=0.4)
            cd_prompt(self, t, P_BABYKEV)
            vo.wait_until("list its tags")
            g_ln = type_cmd(self, t, tags.cmd, type_time=0.8)
            rows = t.print(self, tags.at((2, 10)), run_time=0.9, lag=0.1)
            names = [substring(r, r.text.split()[0]) for r in rows]
            vo.wait_until("9 steps")
            self.play(LaggedStart(*[n.animate.set_color(TURN) for n in names], lag_ratio=0.25), run_time=1.6)
            vo.wait_until("The repo is its own slide deck")
            deck = beside(row_tag("the repo is its own slide deck", S.GREY), rows[0])
            pin(self, rows[0], deck)
            vo.wait_until("git switch")
            jump = ring(names[0], TURN, buff=0.07)
            self.play(Create(jump), run_time=0.4)
            vo.wait_until("moves you to any step")
            for k in (3, 7, 0):
                self.play(Transform(jump, ring(names[k], TURN, buff=0.07)), run_time=0.45)
            vo.wait_until("Pause and run both")
            y1 = beside(turn_row(), c_out)
            y2 = beside(turn_row(), g_ln)
            self.play(FadeIn(y1, shift=LEFT * 0.1), FadeIn(y2, shift=LEFT * 0.1), FadeOut(jump), run_time=0.5)
            self.remove(jump)
            attach(self, c_out, y1)
            attach(self, g_ln, y2)
            self.play(*flash_tag(y1, TURN), *flash_tag(y2, TURN), run_time=0.7)

        # ========================================================== 2. step-00: uv sync --locked; just
        band_lo = strip_top20(3) + 0.15
        left_rows = dep_rows(LOCKED, INK)
        right_rows = dep_rows(LOCKED, INK)
        lw = right_rows.width + 0.6
        lbox = outline_box(lw, right_rows.height + 0.6, S.GREY, solid=False)
        rbox = outline_box(lw, right_rows.height + 0.6, VENV, solid=True, fill_opacity=0.08)
        lbox.move_to([-4.45, 0.6, 0])
        rbox.move_to([-0.35, 0.6, 0])
        left_rows.move_to(lbox)
        right_rows.move_to(rbox)
        l_head = label("no lockfile", 22, S.GREY).next_to(lbox, UP, buff=0.22)
        lock_card = file_card("uv.lock", VENV, size=22)
        lk = lock_glyph(0.42, VENV)
        lock = VGroup(lk, lock_card).arrange(RIGHT, buff=0.18).next_to(rbox, UP, buff=0.12)
        stop = label("stop", 28, ERR).next_to(lock, RIGHT, buff=0.3)
        r_cmd = mono("uv sync --locked", 20, VENV).next_to(rbox, DOWN, buff=0.15)
        t_axis = Arrow([-6.1, band_lo + 0.3, 0], [1.4, band_lo + 0.3, 0], buff=0, color=S.GREY, stroke_width=3,
                       tip_length=0.18, max_tip_length_to_length_ratio=0.05)
        t_lab = note("time", S.GREY, 20).next_to(t_axis, RIGHT, buff=0.15)
        marker = Dot(t_axis.get_start(), radius=0.09, color=INK)
        ill = illustration_tag().move_to([4.6, band_lo + 0.3, 0])
        frost = frost_glyph()
        f_cap = VGroup(label("the cheese way:", 22, IMAGE), label("freeze an image", 22, IMAGE))
        f_cap.arrange(DOWN, buff=0.1)
        cheese = VGroup(frost, f_cap).arrange(DOWN, buff=0.3).move_to([4.6, 0.85, 0])

        with self.voiceover(SAY[2]) as vo:
            t.clear(self, run_time=0.4)
            resize(self, t, 11, keep=0)
            type_cmd(self, t, sw0.cmd, type_time=0.7)
            t.print(self, sw0.at(2), run_time=0.3)
            vo.wait_until("one command builds the environment")
            u_ln = type_cmd(self, t, sync.cmd, type_time=0.6)
            vo.wait_until("uv sync, dash dash locked")
            self.play(Indicate(substring(u_ln, "--locked"), color=VENV, scale_factor=1.15), run_time=0.6)
            out = t.print(self, sync.at((2, 4)) + soft(sync.at(6), t.max_chars) + sync.at((9, 10)),
                          run_time=0.9, lag=0.1)
            cpy, warn_a, warn_b, pkg = out[0], out[3], out[4], out[6]
            vo.wait_until("It installs Python 3.13.16")
            self.play(cpy.animate.set_color(PASS), run_time=0.4)
            self.play(Indicate(cpy, color=PASS, scale_factor=1.06), run_time=0.6)
            vo.wait_until("and the project")
            self.play(Indicate(substring(pkg, "babykev==0.1.0"), color=INK, scale_factor=1.12), run_time=0.6)
            vo.wait_until("Locked means stop")
            resize(self, t, 3, keep=[cpy, warn_a, warn_b], run_time=0.6)
            self.play(FadeIn(VGroup(lbox, left_rows, l_head)), FadeIn(VGroup(rbox, right_rows, r_cmd)),
                      FadeIn(lock, shift=DOWN * 0.15), GrowArrow(t_axis), FadeIn(t_lab), FadeIn(marker),
                      FadeIn(ill), run_time=0.6)
            for k, vers in enumerate(DRIFT):
                x = t_axis.get_start()[0] + (k + 1) * (t_axis.get_length() - 0.4) / 2
                new = dep_rows(vers, HOST).move_to(left_rows, aligned_edge=LEFT)
                self.play(marker.animate.set_x(x),
                          *[Transform(a, b) for a, b in zip(left_rows, new)],
                          Wiggle(lk, scale_value=1.25, rotation_angle=0.08 * TAU), run_time=0.8)
            self.play(FadeIn(stop, scale=1.3), Indicate(right_rows, color=VENV, scale_factor=1.04), run_time=0.5)
            vo.wait_until("Its warning is harmless")
            self.play(Indicate(warn_a, color=INK, scale_factor=1.03), run_time=0.5)
            ttw = beside(time_row(), warn_b)
            pin(self, warn_b, ttw)
            vo.wait_until("The cheese repo froze an image")
            self.play(FadeIn(cheese, shift=LEFT * 0.2), run_time=0.6)
            self.play(Rotate(frost, PI / 3), run_time=0.6)
            vo.wait_until("babykev pins a lockfile")
            self.play(Indicate(lock_card.text, color=VENV, scale_factor=1.2),
                      lock_card.box.frame.animate(rate_func=there_and_back).set_stroke(width=5), run_time=0.7)
            vo.wait_until("Typing just, alone")
            pic = VGroup(lbox, left_rows, l_head, rbox, right_rows, r_cmd, lock, stop, t_axis, t_lab, marker,
                         ill, cheese)
            self.play(FadeOut(pic), run_time=0.5)
            self.remove(pic)
            resize(self, t, 8, keep=0)
            j_ln = type_cmd(self, t, just0.cmd, type_time=0.3)
            j_out = t.print(self, just0.at((2, 6)), run_time=0.7, lag=0.12)
            vo.wait_until("lists the recipes")
            recipes = [substring(j_out[1], "help"), substring(j_out[4], "setup")]
            r_rings = VGroup(*[ring(g, TURN, buff=0.07) for g in recipes])
            self.play(Create(r_rings), run_time=0.5)
            vo.wait_until("one name per task")
            self.play(*[Indicate(g, color=TURN, scale_factor=1.15) for g in recipes], run_time=0.7)
            vo.wait_until("for people")
            # the same name for everyone: three row tags beside `[setup]` (the row above the recipe)
            sect = j_out[3]
            users = [row_tag("for people", S.GREY), row_tag("the hook", TOOL), row_tag("CI · later", S.GREY)]
            beside(users[0], sect, buff=0.6)
            for a, b in zip(users, users[1:]):
                b.next_to(a, RIGHT, buff=0.25)
            pin(self, sect, users[0])
            vo.wait_until("hook")
            pin(self, sect, users[1])
            vo.wait_until("and later CI")
            pin(self, sect, users[2])
            vo.wait_until("Pause and run these")
            yj = beside(turn_row(), j_ln)
            pin(self, j_ln, yj)
            self.play(*flash_tag(yj, TURN), run_time=0.7)

        # ========================================================== 3. step-01: 2 failed, 50 passed
        with self.voiceover(SAY[3]) as vo:
            # the tags are part of their rows: they leave with the terminal's lines
            self.play(FadeOut(VGroup(r_rings, t.lines)), track(tr, 2), run_time=0.5)
            self.remove(r_rings, t.lines)
            for m in list(t.lines):
                t.lines.remove(m)
            resize(self, t, 14, keep=0, run_time=0.6)
            type_cmd(self, t, sw1.cmd, type_time=0.6)
            t.print(self, sw1.at(3), run_time=0.3)
            vo.wait_until("the contract and its tests")
            type_cmd(self, t, setup1.cmd, type_time=0.4)
            t.print(self, setup1.at((2, 3), 9, "…", 19), run_time=0.6, lag=0.1)
            vo.wait_until("Run uv run pytest")
            type_cmd(self, t, pyt.cmd, type_time=0.6)
            prog = t.print(self, soft(pyt.at((10, 11)), t.max_chars), run_time=0.5, lag=0.1)
            t.print(self, ["…"], run_time=0.2)
            fails = t.print(self, at_ids(pyt.at((53, 54))), run_time=0.5, lag=0.1)
            summ = t.print(self, summary(pyt, 55), run_time=0.3)[0]
            vo.wait_until("2 failed, 50 passed")
            self.play(substring(summ, "2 failed").animate.set_color(ERR),
                      substring(summ, "50 passed").animate.set_color(PASS),
                      *[g.animate.set_color(ERR) for g in (substring(prog[0], "F", 0), substring(prog[0], "F", 1))],
                      run_time=0.5)
            self.play(Indicate(substring(summ, "2 failed"), color=ERR, scale_factor=1.15), run_time=0.6)
            vo.wait_until("and the tests are right")
            resize(self, t, 5, keep=[*fails, summ], run_time=0.6)
            card_lines = soft(two.at((32, 35)), 72)
            card = term(P_BABYKEV, rows=len(card_lines), title=two.cmd, size=PT, place=False)
            card.shift(np.array([-card.box.get_center()[0],
                                 strip_top20(5) + 0.15 - card.box.get_bottom()[1], 0]))
            self.play(FadeIn(card, shift=UP * 0.2), run_time=0.5)
            c_rows = card.print(self, card_lines, run_time=0.6, lag=0.1)
            guess_row, got_row = c_rows[3], c_rows[4]
            vo.wait_until("One failure is a pure guess")
            guess = substring(guess_row, "[1 / 3] * 3")
            g_ring = ring(guess, TURN, buff=0.06)
            self.play(Create(g_ring), guess.animate.set_color(TURN), run_time=0.5)
            self.play(substring(guess_row, "pytest.approx(0)").animate.set_color(PASS), run_time=0.4)
            vo.wait_until("half confident")
            half = substring(got_row, "0.5")
            self.play(half.animate.set_color(ERR), run_time=0.3)
            self.play(Indicate(half, color=ERR, scale_factor=1.4), run_time=0.6)
            vo.wait_until("the other is 77 rounded probabilities")
            rr = ring(substring(fails[1], "test_rounded_probabilities_still_sum_to_one"), ERR, buff=0.05)
            self.play(Create(rr), run_time=0.5)
            vo.wait_until("sum to 0.77")
            sum_tag = beside(row_tag("77 × 0.01 = 0.77", ERR), fails[1])
            pin(self, fails[1], sum_tag)
            vo.wait_until("fix the code, not the tests")
            rule = beside(row_tag("fix the code, not the tests", VENV), got_row, buff=1.2)
            pin(self, got_row, rule)
            self.play(*flash_tag(rule, VENV), run_time=0.7)
            vo.wait_until("Pause and run it")
            ys = beside(turn_row(), summ)
            pin(self, summ, ys)
            self.play(*flash_tag(ys, TURN), run_time=0.7)

        # ========================================================== 4. step-02: ruff, the funnel, one width
        r_fmt, r_chk = tool_chip("ruff format", size=24), tool_chip("ruff check", size=24)
        VGroup(r_fmt, r_chk).arrange(RIGHT, buff=2.2).move_to([0.4, 2.3, 0])
        ff = FindingsFunnel([79, 70, 69, 37], ["before just fmt", "after just fmt", "safe fixes", "unsafe fixes, applied deliberately"],
                            bar_w=7.6)
        ff.move_to([-1.2, 0.45, 0])
        # start at 70: a faint notch stays at 79 (walk.md's record before `just fmt`, not spoken)
        old_x = ff.bar.get_right()[0]
        ff.k = 1
        ff.bar.become(ff._bar(1))
        ff.count.become(ff._count(1))
        ff.note.become(ff._note(1))
        notch79 = Line([old_x, ff.track.get_top()[1] + 0.08, 0], [old_x, ff.track.get_bottom()[1] - 0.08, 0],
                       color=ERR, stroke_width=2, stroke_opacity=0.45)
        ff.notches.add(notch79)
        rec = recorded_tag("recorded · walk.md: 79 before just fmt")
        rec.next_to(ff.track, UP, buff=0.2).align_to(notch79, RIGHT).shift(RIGHT * 0.3)
        tick = DashedLine([old_x, rec.get_bottom()[1], 0], [old_x, ff.track.get_top()[1] + 0.08, 0],
                          color=S.GREY, stroke_width=2)
        person = steady("the rest need a person", 22, INK)

        with self.voiceover(SAY[4]) as vo:
            pin_marks = VGroup(card, *t.lines, g_ring, rr)
            self.play(FadeOut(pin_marks), track(tr, 3), run_time=0.6)
            self.remove(pin_marks, *pin_marks.get_family())
            for m in list(t.lines):
                t.lines.remove(m)
            resize(self, t, 6, keep=0, run_time=0.6)
            vo.wait_until("ruff in both roles")
            self.play(FadeIn(r_fmt, shift=DOWN * 0.15), FadeIn(r_chk, shift=DOWN * 0.15), run_time=0.6)
            type_cmd(self, t, stats.cmd, type_time=0.8)
            self.play(Indicate(r_chk.text, color=TOOL, scale_factor=1.15), run_time=0.5)
            t.print(self, stats.at((2, 6)), run_time=0.7, lag=0.08)
            st = t.print(self, ["…"] + stats.at(14) + soft(stats.at(15), t.max_chars), run_time=0.6, lag=0.08)
            found70 = st[1]
            vo.wait_until("the linter counts 70 findings")
            self.play(FadeIn(ff.track), FadeIn(ff.bar, shift=RIGHT * 0.3), FadeIn(ff.count), FadeIn(ff.note),
                      FadeIn(notch79), FadeIn(rec), Create(tick), run_time=0.7)
            self.play(substring(found70, "Found 70 errors.").animate.set_color(ERR),
                      Indicate(ff.count, color=ERR, scale_factor=1.15), run_time=0.6)
            vo.wait_until("Safe automatic fixes")
            type_cmd(self, t, fix.cmd, type_time=0.5)
            f_out = t.print(self, fix.at(692), run_time=0.3)[0]
            vo.wait_until("remove one")
            self.play(ff.step(), Indicate(substring(f_out, "1 fixed"), color=INK, scale_factor=1.15), run_time=0.9)
            vo.wait_until("Unsafe fixes")
            type_cmd(self, t, unsafe.cmd, type_time=0.7)
            u_out = t.print(self, unsafe.at(360), run_time=0.3)[0]
            vo.wait_until("remove 32 more")
            self.play(ff.step(run_time=1.1), Indicate(substring(u_out, "32 fixed"), color=INK, scale_factor=1.15),
                      run_time=1.1)
            vo.wait_until("37 remain")
            self.play(Indicate(substring(u_out, "37 remaining"), color=ERR, scale_factor=1.15),
                      Indicate(ff.count, color=ERR, scale_factor=1.15), run_time=0.7)
            vo.wait_until("those need a person")
            person.move_to(ff.note, aligned_edge=LEFT)
            self.play(Transform(ff.note, person), run_time=0.6)
            self.play(Indicate(ff.note, color=INK, scale_factor=1.08), run_time=0.5)

            # one width, written once
            vo.wait_until("the width war from part 1")
            funnel = VGroup(ff, rec, tick)
            self.play(FadeOut(VGroup(funnel, t)), run_time=0.6)
            self.remove(funnel, t, *t.get_family())
            war = VGroup(dashed_chip("black: 88", size=24), dashed_chip("flake8: 79", size=24),
                         dashed_chip("hook + CI: 120", size=24)).arrange(RIGHT, buff=0.6).move_to([0, 0.3, 0])
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in war], lag_ratio=0.25), run_time=0.8)
            self.play(*[Wiggle(c, scale_value=1.08, rotation_angle=0.03 * TAU) for c in war], run_time=0.7)
            panel = code(PYPROJECT, 65, 65, font_size=26)
            panel.move_to([0, 0.15, 0])
            lbar = line_bar(panel.code, 0, VENV, 0.22)
            frame = outline_box(panel.width + 0.6, panel.height + 0.5, VENV, solid=True, fill_opacity=0.08)
            frame.move_to(panel)
            vo.wait_until("is settled in one line")
            self.play(FadeTransform(war, frame), run_time=0.8)
            self.play(FadeIn(panel), run_time=0.4)
            vo.wait_until("line length 100")
            hundred = code_span(panel.code, 0, "line-length = 100")
            self.play(FadeIn(lbar), Indicate(hundred, color=VENV, scale_factor=1.12), run_time=0.7)
            vo.wait_until("written once in pyproject.toml")
            self.play(Indicate(panel.header, color=INK, scale_factor=1.1), run_time=0.7)
            vo.wait_until("the formatter and the linter both follow it")
            self.play(r_fmt.animate.move_to([-3.0, -1.9, 0]), r_chk.animate.move_to([3.0, -1.9, 0]), run_time=0.7)
            a_f = arrow(frame.get_bottom() + LEFT * 0.8, r_fmt.get_top(), VENV)
            a_c = arrow(frame.get_bottom() + RIGHT * 0.8, r_chk.get_top(), VENV)
            self.play(GrowArrow(a_f), GrowArrow(a_c), run_time=0.6)
            self.play(Indicate(r_fmt.text, color=TOOL, scale_factor=1.12),
                      Indicate(r_chk.text, color=TOOL, scale_factor=1.12), run_time=0.7)
        self.wait(0.8)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
