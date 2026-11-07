"""S11 · The summary listens only to tests (AC215 L21). TRACKER P5 8, STRIP Summary.
Lecture: 21 · slides 16, 26–27 (beat 0 only). Set piece V4 JobGraph (S11 form: result tokens).

Beats (script.md "## S11", one voiceover block each):
0. TRACKER P5 8; the Part 2 strip moves on from `Test` to `Summary` (YELLOW). LECTURE 21 · 16, 26–27
   and a GREY chip from slide 27, "Summary: collects the results, reports pass / fail". README(325–330)
   card, which then shrinks into the tracker's caption; CODE(ci.yml 172–183) takes its place: line 175
   `needs: [unit-tests, integration-tests, system-tests]` YELLOW (the three names light in turn),
   line 176 `if: always()` PINK, with a GREY "runs ≠ passes" beside it.
1. LECTURE off. The panel transforms into CODE(ci.yml 181–192) (line 185 soft-wrapped at its `||`, a
   GREY ↪ marks each continuation row): 181–183 PINK, the two `>> $GITHUB_OUTPUT` (187, 191) PINK
   with "← for later steps", 188 `exit 1` RED, the 185 comparison YELLOW.
2. V4: GRAPH(run1) (short labels; badge above Build, tag under the middle column) top-left; three
   PINK `success` tokens ride the needs lines into Summary. LOG(run1/test-summary/01: 13–16) below
   (heading collapsed into the title): the three lines and `✅ All tests passed!` GREEN.
3. The RED lint node pulses; no token leaves it. The dashed gap with its YELLOW "?" (S05) returns;
   the "?" turns into a GREY "not in needs". The RED run badge pulses; GREY chip "any failed job →
   the run is red" top right.
4. The log leaves. README(328) card with the plain GREY note "true · lint is not a test job" (no
   erratum tag). The gap becomes a GREY dashed arrow "after the fix" (tip at Summary); GREY chip
   "exercises.md: add lint-and-format to needs + the check". On "if you want it counted" Summary turns
   RED (what it would report with lint in needs) and pulses; it turns back GREEN as beat 5 clears.
5. The graph shrinks into a text-free graph glyph (top right). CODE(history/c3b227f-service.py
   38–44) at 20 pt: the docstring's `sqrt(x^2 + y^2)` WHITE, underlined; line 44 RED, `2 * z`
   ringed. GREY chip "demo class 1 · 2025-11-13" above, GREY chip "unit tests → utils.py ·
   /euclidean_distance/ → integration + system" below. On "We ran this one for you" a GREY chip
   "watch only · we ran it for you" beside the demo chip (no command for the viewer here).
6. The glyph grows into GRAPH(run-demo) at the start state (six GREY nodes); the panel condenses to
   line 44 (RED) with a GREY chip "the demo commit" under the graph. On "Which jobs" the six nodes
   pulse left to right; on "Test Summary" the summary node pulses. No colors change.
   PONDER(8 s) card.
7. The card leaves. Build ✓; Integration Tests ✗ RED with LOG(run-demo/integration-tests/04: 32,
   35) (`assert 7.0710678118654755 == 5.0`, `1 failed, 9 passed, 1 warning` RED).
8. System Tests ✗ RED with LOG(run-demo/system-tests/06: 27, 35, 51) (GREY chips "default x=1, y=2"
   on 27, "x=3, y=4" on 35); Unit Tests ✓ GREEN with the GREY chip "Unit: only power() has unit
   tests"; Lint and Format Check ✗ RED with "Lint: still utils.py".
9. Two PINK `failure` tokens and one `success` slide into Summary; it turns RED, the run badge RED.
   LOG(run-demo/test-summary/01: 13–16): the two failures and `❌ Some tests failed!` RED; badge
   "exit 1". Fade; empty frame.

pytest's summary rulers (`==== 1 failed, 9 passed … ====`, 80 columns) are shown with the `=`
padding cut to three on each side (pytest pads that line to the terminal's width; the words are
the capture's), so the line fits one 20 pt row.
"""

import copy
import re

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S11"]

# ------------------------------------------------------------------ the real sources (checked)
CI = ".github/workflows/ci.yml"
SVC = "history/c3b227f-service.py"
assert excerpt(CI, 172, 173).split("\n") == ["  test-summary:", "    name: Test Summary"]
assert excerpt(CI, 175, 175).strip() == "needs: [unit-tests, integration-tests, system-tests]"
assert excerpt(CI, 176, 176).strip() == "if: always()"
assert excerpt(CI, 181, 181).strip() == 'echo "Unit Tests: ${{ needs.unit-tests.result }}"'
assert excerpt(CI, 185, 185).strip().startswith('if [ "${{ needs.unit-tests.result }}" != "success" ] ||')
assert excerpt(CI, 187, 187).strip() == 'echo "status=failure" >> $GITHUB_OUTPUT'
assert excerpt(CI, 188, 188).strip() == "exit 1"
assert excerpt(CI, 191, 191).strip() == 'echo "status=success" >> $GITHUB_OUTPUT'
assert excerpt(CI, 192, 192).strip() == "fi"
assert excerpt(SVC, 40, 40).strip().startswith('"""Calculate the Euclidean distance from origin: sqrt(x^2 + y^2)')
assert excerpt(SVC, 44, 44).strip() == "result = math.sqrt(2 * z)"
assert readme(328) == "- Checks the results of all test jobs", readme(328)
assert readme(325).startswith("6. **Test Summary Job**")

SUM1 = capture("run1/test-summary/01")
assert SUM1.at((13, 16)) == ["Unit Tests: success", "Integration Tests: success", "System Tests: success",
                             "✅ All tests passed!"], SUM1.at((13, 16))
SUMD = capture("run-demo/test-summary/01")
assert SUMD.at((13, 16)) == ["Unit Tests: success", "Integration Tests: failure", "System Tests: failure",
                             "❌ Some tests failed!"] and SUMD.exit == 1
INTD = capture("run-demo/integration-tests/04")
assert INTD.line(32) == "E   assert 7.0710678118654755 == 5.0", INTD.line(32)
assert "1 failed, 9 passed, 1 warning" in INTD.line(35)
SYSD = capture("run-demo/system-tests/06")
assert SYSD.line(27).startswith("E   assert 3.1622776601683795 == 2.236"), SYSD.line(27)
assert SYSD.line(35).startswith("E   assert 7.0710678118654755 == 5.0"), SYSD.line(35)
assert "2 failed, 3 passed" in SYSD.line(51)
assert results("run1") == {"build": "success", "lint-and-format": "failure", "unit-tests": "success",
                           "integration-tests": "success", "system-tests": "success",
                           "test-summary": "success"}
DEMO = results("run-demo")
assert DEMO == {"build": "success", "lint-and-format": "failure", "unit-tests": "success",
                "integration-tests": "failure", "system-tests": "failure", "test-summary": "failure"}

PONDER_Q = ("The demo commit computes sqrt(2·z)\ninstead of sqrt(z).\nWhich jobs turn red,\n"
            "and what does Test Summary say now?")

# ------------------------------------------------------------------ layout
TOP = 2.05                 # Part 2 pictures stay below PIC_TOP2 (2.15)
LEFT_X = -6.45
RIGHT_X = 6.45
PITCH = 0.64
LOG_BOTTOM = -3.38         # log panels' bottom edge (their tag straddles it)
CODE_SIZE = 20


def top_at(m, y: float = TOP, x: float = 0.0):
    return m.move_to([x, y - m.height / 2, 0])


def ruler(cap, *nums):
    """A copy of the capture whose pytest summary lines (nums) keep three '=' each side."""
    c = copy.copy(cap)
    c.raw = list(cap.raw)
    for n in nums:
        s = c.raw[n - 1]
        new = re.sub(r"^=+ (.*?) =+$", r"=== \1 ===", s)
        assert new != s and new.strip("= ") == s.strip("= "), s
        c.raw[n - 1] = new
    return c


def wrapped_code(path: str, a: int, b: int, folds: dict | None = None, size: float = CODE_SIZE) -> VGroup:
    """CODE(path: a–b) with long lines soft-wrapped, as an editor shows them (S09's helper):
    folds = {file line: [break after these substrings]}. Continuation rows are indented two columns
    deeper and marked with a GREY '↪'; every character is the file's. .code .header .rows .src_rows"""
    folds = folds or {}
    src_rows, rows = [], {}
    for n in range(a, b + 1):
        s = excerpt(path, n, n)
        ind = len(s) - len(s.lstrip())
        parts, rest = [], s
        for cut_after in folds.get(n, []):
            i = rest.index(cut_after) + len(cut_after)
            parts.append(rest[:i].rstrip())
            rest = rest[i:].lstrip()
        parts.append(rest)
        rows[n] = []
        for k, p_ in enumerate(parts):
            rows[n].append(len(src_rows))
            src_rows.append(p_ if k == 0 else " " * (ind + 2) + p_)
    assert "".join("".join(src_rows).split()) == "".join(excerpt(path, a, b).split())
    # the mono font has no emoji: each ✅ / ❌ is set as a two-cell filler, hidden, and drawn on top
    # as a GREEN check / RED cross (common.emo_line's convention)
    spots = []
    for k, r in enumerate(src_rows):
        for i, ch in enumerate(r):
            if ch in ("✅", "❌"):
                spots.append((k, len("".join(r[:i].split())), ch))
    c = code_block("\n".join(r.replace("✅", "MM").replace("❌", "MM") for r in src_rows), "yaml", size)
    emo = VGroup()
    ref_h = mono("M", size).height
    for k, j, ch in spots:
        fill = VGroup(*c.code_lines[k][j:j + 2])
        fill.set_opacity(0)
        mk = check_mark(ref_h * 1.15, PASS, stroke=4) if ch == "✅" else cross_mark(ref_h, ERR, stroke=4)
        emo.add(mk.move_to(fill.get_center()))
    head = VGroup(mono(shown_path(path), CAPTION, S.GREY), label(f"· lines {a}–{b}", CAPTION, S.GREY)) \
        .arrange(RIGHT, buff=0.14)
    head.next_to(c, UP, buff=0.1).align_to(c, LEFT).shift(RIGHT * 0.12)
    marks = VGroup()
    for n, ks in rows.items():
        for k in ks[1:]:
            marks.add(label("↪", 20, S.GREY).next_to(c.code_lines[k], LEFT, buff=0.18))
    g = VGroup(c, head, marks, emo)
    g.code, g.header, g.rows, g.marks, g.src_rows = c, head, rows, marks, src_rows
    return g


def span(panel, n: int, sub: str, occurrence: int = 0):
    """Glyphs of `sub` in file line n of a wrapped_code panel (searched row by row)."""
    for k in panel.rows[n]:
        if sub in panel.src_rows[k]:
            return code_span(panel.code, k, sub, occurrence)
    raise ValueError(f"{sub!r} not in line {n}")


def line_glyphs(panel, n: int):
    """Every glyph of file line n (all its rows)."""
    return VGroup(*[panel.code.code_lines[k] for k in panel.rows[n]])


def summary_graph(run=None) -> JobGraph:
    """GRAPH(run) in this scene's layout: short labels, nodes top-left (top TOP, left LEFT_X), the
    run badge above the Build node, the illustration tag under the middle column."""
    g = JobGraph(states=results(run) if run else None, labels="short", col_gap=1.0, pitch=PITCH)
    nodes = VGroup(*g.nodes.values())
    v = np.array([LEFT_X - nodes.get_left()[0], TOP - nodes.get_top()[1], 0])
    g.shift(v)
    g.gap.shift(v)             # not members until show_gap(): move them with the graph
    g.gap_q.shift(v)
    b = g.nodes["build"]
    g.badge.next_to(b, UP, buff=0.2).align_to(b, LEFT)
    g.tag.move_to([LEFT_X + g.tag.width / 2, nodes.get_bottom()[1] - 0.14 - g.tag.height / 2, 0])
    unit = g.nodes["unit-tests"]
    assert g.badge.get_right()[0] < unit.get_left()[0] - 0.15, (g.badge.get_right(), unit.get_left())
    return g


def right_of_graph(g: JobGraph, m, job: str):
    """m in the right-hand zone, at the height of node `job`."""
    x0 = max(n.get_right()[0] for n in g.nodes.values()) + 0.3
    assert m.width <= RIGHT_X - x0 + 1e-6, (m.width, RIGHT_X - x0)
    return m.move_to([x0 + m.width / 2, g.nodes[job].get_center()[1], 0])


def log_at_bottom(lg, x: float | None = None):
    """A log panel in the bottom zone, right-aligned (the graph's tag sits bottom-left)."""
    x = RIGHT_X - lg.width / 2 if x is None else x
    return lg.move_to([x, LOG_BOTTOM + lg.height / 2, 0])


class TheSummary(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S11"] == 10, len(SAY)

        # ========================================================== 0. the summary job: needs, if always
        tr = tracker_p5(8)
        strip = pipeline_strip("Test")
        ref = lref("16, 26–27")
        slide_chip = grey_chip("Summary: collects the results, reports pass / fail", size=22)
        slide_chip.move_to([0, 1.75, 0])
        card = readme_panel(325, 330)
        top_at(card, 1.25)
        p0 = wrapped_code(CI, 172, 183)
        assert p0.width <= 12.6, p0.width
        top_at(p0, TOP - 0.05)
        runs = label("runs ≠ passes", 22, INK).next_to(span(p0, 176, "if: always()"), RIGHT, buff=0.6)
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=RIGHT * 0.2), FadeIn(strip, shift=RIGHT * 0.3), run_time=0.6)
            self.play(strip.set_current("Summary"), run_time=0.6)
            self.add(strip)
            vo.wait_until("which the lecture says")
            self.play(FadeIn(ref), FadeIn(slide_chip, shift=DOWN * 0.15), run_time=0.6)
            self.play(FadeIn(card, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("collects the results")
            hb = VGroup(hl_bar(card.rows[328], OWN, 0.2), hl_bar(card.rows[330], OWN, 0.2))
            self.play(FadeIn(hb), Indicate(slide_chip, color=INK, scale_factor=1.05), run_time=0.7)
            vo.wait_until("Its needs line")
            cap_copy = tr.caption.copy()
            self.play(ReplacementTransform(VGroup(card, hb), cap_copy), FadeOut(slide_chip),
                      FadeIn(p0, shift=UP * 0.15), run_time=0.7)
            self.remove(cap_copy, card, hb, slide_chip)
            self.add(tr)
            s175 = span(p0, 175, "needs: [unit-tests, integration-tests, system-tests]")
            b175 = hl_bar(s175, TURN, 0.22)
            self.play(FadeIn(b175), s175.animate.set_color(TURN), run_time=0.5)
            vo.wait_until("names the three test jobs")
            names = [span(p0, 175, n_) for n_ in ("unit-tests", "integration-tests", "system-tests")]
            self.play(LaggedStart(*[Indicate(n_, color=TURN, scale_factor=1.12) for n_ in names], lag_ratio=0.4),
                      run_time=1.2)
            vo.wait_until("And if always")
            s176 = span(p0, 176, "if: always()")
            b176 = hl_bar(s176, ROUTE, 0.22)
            self.play(FadeIn(b176), s176.animate.set_color(ROUTE), run_time=0.5)
            self.play(Indicate(s176, color=ROUTE, scale_factor=1.12), run_time=0.6)
            vo.wait_until("it runs, which")
            self.play(FadeIn(runs, shift=LEFT * 0.2), run_time=0.5)
            vo.wait_until("the same as passing")
            self.play(Indicate(runs, color=INK, scale_factor=1.08), run_time=0.7)

        # ========================================================== 1. the script: print, write, exit
        p1 = wrapped_code(CI, 181, 192, {185: ['"success" ] ||', '"success" ] ||']})
        assert p1.width <= 12.6, p1.width
        top_at(p1, TOP - 0.05)
        assert p1.get_bottom()[1] > -3.6, p1.get_bottom()
        later = label("← for later steps", 20, ROUTE).next_to(span(p1, 187, ">> $GITHUB_OUTPUT"), RIGHT, buff=0.3)
        with self.voiceover(SAY[1]) as vo:
            old = VGroup(p0, b175, b176, runs)
            self.play(FadeOut(ref), FadeOut(VGroup(b175, b176, runs)), ReplacementTransform(p0, p1), run_time=0.9)
            self.remove(*old, *old.get_family(), ref)
            self.add(p1)
            vo.wait_until("prints each job's result")
            echos = VGroup(*[line_glyphs(p1, n_) for n_ in (181, 182, 183)])
            self.play(echos.animate.set_color(ROUTE), run_time=0.5)
            self.play(LaggedStart(*[Indicate(span(p1, n_, "needs."), color=ROUTE, scale_factor=1.12)
                                    for n_ in (181, 182, 183)], lag_ratio=0.3), run_time=1.0)
            vo.wait_until("writes a status to GitHub output")
            outs = VGroup(span(p1, 187, ">> $GITHUB_OUTPUT"), span(p1, 191, ">> $GITHUB_OUTPUT"))
            bo = VGroup(*[hl_bar(o, ROUTE, 0.22) for o in outs])
            self.play(FadeIn(bo), outs.animate.set_color(ROUTE), run_time=0.5)
            vo.wait_until("for later steps")
            self.play(FadeIn(later, shift=LEFT * 0.2), run_time=0.5)
            vo.wait_until("and exits with 1")
            ex = span(p1, 188, "exit 1")
            bx = hl_bar(ex, ERR, 0.25)
            self.play(FadeIn(bx), ex.animate.set_color(ERR), run_time=0.5)
            self.play(Indicate(ex, color=ERR, scale_factor=1.2), run_time=0.6)
            vo.wait_until("if any result isn't success")
            cmp_ = line_glyphs(p1, 185)
            self.play(cmp_.animate.set_color(TURN), run_time=0.5)
            nes = VGroup(*[span(p1, 185, '!= "success"', occurrence=0)])
            for k in p1.rows[185]:
                if '!= "success"' in p1.src_rows[k]:
                    nes.add(code_span(p1.code, k, '!= "success"'))
            self.play(Indicate(nes, color=TURN, scale_factor=1.1), run_time=0.7)

        # ========================================================== 2. run 1: three success tokens
        g = summary_graph("run1")
        lg2 = run_log(SUM1, ((13, 16),), heading=False, size=CODE_SIZE,
                      colors={13: PASS, 14: PASS, 15: PASS, 16: PASS})
        log_at_bottom(lg2)
        assert lg2.get_left()[0] > g.tag.get_right()[0] + 0.1 or lg2.get_top()[1] < g.tag.get_bottom()[1], \
            (lg2.get_left(), g.tag.get_right())
        with self.voiceover(SAY[2]) as vo:
            gone = VGroup(p1, bo, later, bx)
            self.play(FadeOut(gone), run_time=0.5)
            self.remove(gone, *gone.get_family())
            self.play(FadeIn(g, shift=UP * 0.15), run_time=0.7)
            shell = VGroup(*[m for m in lg2.submobjects if lg2.rows not in m.get_family()])
            self.play(FadeIn(shell, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("three success tokens arrive")
            ride_tokens(self, g, results("run1"), run_time=2.0)
            self.add(g)
            vo.wait_until("unit, integration, system")
            for n_ in (13, 14, 15):
                self.play(FadeIn(lg2.row(n_), shift=RIGHT * 0.1), run_time=0.35)
            vo.wait_until("All tests passed")
            self.play(FadeIn(lg2.row(16), shift=RIGHT * 0.1), run_time=0.35)
            self.remove(shell, *lg2.rows)
            self.add(lg2)
            self.play(Indicate(lg2.row(16), color=PASS, scale_factor=1.08), g.pulse("test-summary", PASS),
                      run_time=0.8)

        # ========================================================== 3. the hook, answered
        red_chip = grey_chip("any failed job → the run is red", size=20)
        right_of_graph(g, red_chip, "unit-tests")
        lint = g.nodes["lint-and-format"]
        summ = g.nodes["test-summary"]
        not_in = label("not in needs", 22, S.GREY)
        gq = g.gap_q
        not_in.move_to(gq).align_to(gq, LEFT)
        not_in.set_y((summ.get_bottom()[1] + lint.get_center()[1]) / 2 - 0.05)
        assert not_in.get_top()[1] < summ.get_bottom()[1] - 0.04, (not_in.get_top(), summ.get_bottom())
        assert not_in.get_bottom()[1] > lg2.get_top()[1], (not_in.get_bottom(), lg2.get_top())
        with self.voiceover(SAY[3]) as vo:
            self.play(g.pulse("lint-and-format", ERR), run_time=0.8)
            self.play(Circumscribe(lint, color=ERR, buff=0.08), run_time=0.8)
            vo.wait_until("Lint isn't in needs")
            g.show_gap(self)
            self.play(Indicate(gq, color=TURN, scale_factor=1.3), run_time=0.5)
            self.play(ReplacementTransform(gq, not_in), run_time=0.6)
            g.remove(gq)
            self.add(not_in)
            vo.wait_until("so its failure never reaches")
            self.play(Indicate(g.gap, color=ERR, scale_factor=1.0), g.pulse("test-summary", PASS), run_time=0.9)
            vo.wait_until("The run is still red")
            self.play(Circumscribe(g.badge, color=ERR, buff=0.06),
                      Indicate(g.badge.text, color=ERR, scale_factor=1.08), run_time=0.8)
            vo.wait_until("because any failed job")
            self.play(FadeIn(red_chip, shift=LEFT * 0.2), run_time=0.5)
            self.play(Indicate(red_chip, color=INK, scale_factor=1.05),
                      Indicate(g.badge, color=ERR, scale_factor=1.06), run_time=0.7)

        # ========================================================== 4. the README is literally true; the fix
        card4 = readme_panel(328, 328)
        card4.move_to([LEFT_X + card4.width / 2, -1.25 - card4.height / 2, 0])
        note4 = label("← true · lint is not a test job", 22, S.GREY).next_to(card4, RIGHT, buff=0.3)
        ex_chip = grey_chip("exercises.md: add lint-and-format to needs + the check", size=20)
        ex_chip.next_to(card4, DOWN, buff=0.35).align_to(card4, LEFT)
        after = label("after the fix", 22, S.GREY).move_to(not_in).align_to(not_in, LEFT)
        q = summ.get_left()
        tip = Triangle(fill_opacity=1, stroke_width=0).set_fill(S.GREY, 1).scale(0.09).rotate(-PI / 2)
        tip.move_to(q + LEFT * 0.08)
        fix_arrow = DashedVMobject(_gap_path(g), num_dashes=18).set_stroke(S.GREY, 3.5)
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(lg2), FadeIn(card4, shift=UP * 0.15), run_time=0.6)
            self.remove(lg2, *lg2.get_family())
            vo.wait_until("and that's literally true")
            self.play(FadeIn(note4, shift=LEFT * 0.2), run_time=0.5)
            vo.wait_until("lint isn't a test job")
            self.play(Indicate(note4, color=INK, scale_factor=1.06), g.pulse("lint-and-format", S.GREY), run_time=0.8)
            vo.wait_until("Add lint and format to needs")
            self.play(ReplacementTransform(not_in, after), Create(fix_arrow), FadeIn(tip), run_time=0.9)
            vo.wait_until("and to the check")
            self.play(FadeIn(ex_chip, shift=UP * 0.15), run_time=0.5)
            self.play(Indicate(ex_chip, color=INK, scale_factor=1.04), run_time=0.6)
            vo.wait_until("if you want it counted")
            # with lint in needs (and failed), the summary would report failure: show it on the fixed wiring
            self.play(g.set_state("test-summary", "failure"), run_time=0.4)
            self.add(g)
            self.play(g.pulse("test-summary", ERR), Indicate(fix_arrow, color=ERR, scale_factor=1.0), run_time=0.8)

        # ========================================================== 5. the bug from class
        icon = graph_icon(0.9)
        icon.move_to([RIGHT_X - icon.width / 2, 3.0, 0])
        sp = code(SVC, 38, 44, font_size=CODE_SIZE)
        demo_chip = grey_chip("demo class 1 · 2025-11-13", size=20)
        map_chip = grey_chip("unit tests → utils.py · /euclidean_distance/ → integration + system", size=20)
        block = VGroup(demo_chip, sp, map_chip).arrange(DOWN, buff=0.3)
        top_at(block, TOP - 0.05)
        assert block.get_bottom()[1] > -3.55, block.get_bottom()
        doc = code_span(sp.code, 2, "sqrt(x^2 + y^2)")
        bug = code_span(sp.code, 6, "result = math.sqrt(2 * z)")
        two = code_span(sp.code, 6, "2 * z")
        watch = grey_chip("watch only · we ran it for you", size=20).next_to(demo_chip, RIGHT, buff=0.35)
        with self.voiceover(SAY[5]) as vo:
            rest = VGroup(card4, note4, ex_chip, after, fix_arrow, tip, red_chip)
            # the fix was hypothetical: run 1's summary goes back to green as its arrow leaves
            self.play(FadeOut(rest), g.set_state("test-summary", "success"), run_time=0.5)
            self.remove(rest, *rest.get_family())
            self.add(g)
            self.play(FadeOut(g, target_position=icon.get_center(), scale=0.12),
                      FadeIn(icon, scale=1.6), run_time=0.8)
            self.remove(g, *g.get_family())
            self.add(icon)
            self.play(FadeIn(sp, shift=UP * 0.15), FadeIn(demo_chip, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("In the demo commit")
            self.play(Indicate(demo_chip, color=INK, scale_factor=1.05), run_time=0.6)
            self.play(FadeIn(map_chip, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("the distance function")
            u_doc = hl_bar(doc, INK, 0.16, buff=0.03)   # a bar, not an underline: it stays in its row
            self.play(doc.animate.set_color(INK), FadeIn(u_doc), run_time=0.6)
            vo.wait_until("takes the square root of 2 times z")
            bb = hl_bar(bug, ERR, 0.22)
            self.play(FadeIn(bb), bug.animate.set_color(ERR), run_time=0.5)
            rg = ring(two, ERR, buff=0.08, stroke=4)
            self.play(Create(rg), run_time=0.5)
            vo.wait_until("instead of z")
            self.play(Indicate(two, color=ERR, scale_factor=1.3), run_time=0.7)
            vo.wait_until("We ran this one for you")
            self.play(FadeIn(watch, shift=LEFT * 0.2), run_time=0.5)
            vo.wait_until("just watch")
            self.play(Indicate(watch, color=INK, scale_factor=1.05), run_time=0.6)

        # ========================================================== 6. predict (ponder)
        gd = summary_graph(None)
        strip44 = code_strip(SVC, 44, font_size=CODE_SIZE)
        dcommit = grey_chip("the demo commit", size=20)
        sgrp = VGroup(strip44, dcommit).arrange(RIGHT, buff=0.35)
        sgrp.move_to([LEFT_X + sgrp.width / 2, -1.55 - strip44.height / 2, 0])
        b44 = code_span(strip44.code, 0, "result = math.sqrt(2 * z)")
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(demo_chip, watch, map_chip, u_doc, rg, bb)),
                      ReplacementTransform(sp, strip44), FadeTransform(icon, gd), run_time=0.9)
            self.remove(sp, icon, demo_chip, watch, map_chip, u_doc, rg, bb)
            self.add(gd, strip44)
            self.play(b44.animate.set_color(ERR), FadeIn(dcommit, shift=LEFT * 0.2), run_time=0.5)
            vo.wait_until("Which jobs turn red now")
            order = ["build", "unit-tests", "integration-tests", "system-tests", "lint-and-format"]
            self.play(LaggedStart(*[gd.pulse(j, INK) for j in order], lag_ratio=0.3), run_time=1.6)
            vo.wait_until("and what does Test Summary say")
            self.play(gd.pulse("test-summary", TURN), run_time=0.8)
        card6 = ponder(self, PONDER_Q, seconds=8)

        # ========================================================== 7. integration: red
        lg7 = run_log(ruler(INTD, 35), (32, 35), heading=False, size=CODE_SIZE, colors={32: ERR, 35: ERR})
        log_at_bottom(lg7)
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(card6), FadeOut(VGroup(strip44, dcommit)), run_time=0.5)
            self.remove(card6, strip44, dcommit)
            self.play(gd.set_state("build", "success"), run_time=0.3)
            self.play(gd.set_state("integration-tests", "running"), run_time=0.25)
            self.play(gd.set_state("integration-tests", "failure"), run_time=0.35)
            self.add(gd)
            vo.wait_until("1 failed and 9 passed")
            self.play(FadeIn(lg7, shift=UP * 0.15), run_time=0.5)
            self.play(Indicate(lg7.row(35), color=ERR, scale_factor=1.05), run_time=0.7)
            vo.wait_until("The distance for 3 and 4")
            hb7 = hl_bar(lg7.row(32), ERR, 0.2)
            self.play(FadeIn(hb7), run_time=0.4)
            vo.wait_until("about 7, not 5")
            self.play(Indicate(substring(lg7.row(32), "7.0710678118654755"), color=ERR, scale_factor=1.12),
                      run_time=0.6)
            self.play(Indicate(substring(lg7.row(32), "5.0"), color=PASS, scale_factor=1.3), run_time=0.6)

        # ========================================================== 8. system red, unit green, lint red
        lg8 = run_log(ruler(SYSD, 51), (27, 35, 51), heading=False, size=CODE_SIZE,
                      colors={27: ERR, 35: ERR, 51: ERR})
        log_at_bottom(lg8)
        # labels, not chips: a chip is taller than a 20 pt log row and the two rows are adjacent
        c35 = label("x=3, y=4 →", 20, S.GREY).next_to(lg8.frame, LEFT, buff=0.25).set_y(lg8.row(35).get_center()[1])
        c27 = label("default x=1, y=2 →", 20, S.GREY).next_to(lg8.frame, LEFT, buff=0.25).set_y(lg8.row(27).get_center()[1])
        assert c27.get_left()[0] >= LEFT_X, c27.get_left()
        unit_chip = grey_chip("Unit: only power() has unit tests", size=20)
        right_of_graph(gd, unit_chip, "unit-tests")
        lint_chip = grey_chip("Lint: still utils.py", size=20)
        right_of_graph(gd, lint_chip, "lint-and-format")
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(lg7, hb7)), run_time=0.4)
            self.remove(lg7, hb7, *lg7.get_family())
            self.play(gd.set_state("system-tests", "running"), run_time=0.25)
            self.play(gd.set_state("system-tests", "failure"), FadeIn(lg8, shift=UP * 0.15), run_time=0.5)
            self.add(gd)
            vo.wait_until("2 failed and 3 passed")
            self.play(Indicate(lg8.row(51), color=ERR, scale_factor=1.05), run_time=0.6)
            vo.wait_until("3 and 4 again")
            self.play(FadeIn(c35, shift=LEFT * 0.2), Indicate(lg8.row(35), color=ERR, scale_factor=1.04), run_time=0.6)
            vo.wait_until("and the default point")
            self.play(FadeIn(c27, shift=LEFT * 0.2), Indicate(lg8.row(27), color=ERR, scale_factor=1.04), run_time=0.6)
            vo.wait_until("Unit: green")
            self.play(gd.set_state("unit-tests", "running"), run_time=0.25)
            self.play(gd.set_state("unit-tests", "success"), run_time=0.35)
            self.add(gd)
            vo.wait_until("because only the power function")
            self.play(FadeIn(unit_chip, shift=LEFT * 0.2), run_time=0.5)
            vo.wait_until("Lint: red anyway")
            self.play(gd.set_state("lint-and-format", "running"), run_time=0.25)
            self.play(gd.set_state("lint-and-format", "failure"), FadeIn(lint_chip, shift=LEFT * 0.2), run_time=0.45)
            self.add(gd)
            vo.wait_until("for utils dot py")
            self.play(Indicate(lint_chip, color=INK, scale_factor=1.06), gd.pulse("lint-and-format", ERR), run_time=0.7)

        # ========================================================== 9. the summary hears it
        lg9 = run_log(SUMD, ((13, 16),), heading=False, size=CODE_SIZE, colors={13: PASS, 14: ERR, 15: ERR, 16: ERR})
        log_at_bottom(lg9)
        assert lg9.get_left()[0] > gd.tag.get_right()[0] + 0.1 or lg9.get_top()[1] < gd.tag.get_bottom()[1], \
            (lg9.get_left(), gd.tag.get_right())
        with self.voiceover(SAY[9]) as vo:
            out8 = VGroup(lg8, c35, c27, unit_chip, lint_chip)
            self.play(FadeOut(out8), run_time=0.4)
            self.remove(out8, *out8.get_family())
            ride_tokens(self, gd, DEMO, run_time=1.9)
            self.play(gd.set_state("test-summary", "failure"), run_time=0.4)
            self.add(gd)
            self.play(gd.set_badge("failure"), FadeIn(lg9, shift=UP * 0.15), run_time=0.5)
            self.add(gd)
            vo.wait_until("and exits with 1")
            self.play(Indicate(lg9.row(16), color=ERR, scale_factor=1.06), run_time=0.6)
            self.play(Circumscribe(lg9.badge, color=ERR, buff=0.06), run_time=0.7)
            vo.wait_until("This time the summary heard it")
            self.play(gd.pulse("test-summary", ERR), run_time=0.8)

        self.wait(0.3)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.wait(0.2)


def ride_tokens(scene, g: JobGraph, states: dict, run_time: float = 1.5):
    """PLAYS: three PINK result tokens ride the needs lines from the test jobs into Summary (V4, S11).
    A local variant of JobGraph.tokens(): each token fades in while it leaves its node and fades out
    as it reaches Summary, so no token ever sits still on a node label or on another token; then
    Summary's mark flashes PINK."""
    anims, toks = [], []
    for j in TEST_JOBS:
        e = g.edges[(j, "test-summary")]
        t0 = route_chip(states[j], 20)
        t = t0.copy().move_to(e.get_start()).fade(1)

        def upd(m, a, e=e, t0=t0):
            m.become(t0)
            m.move_to(e.point_from_proportion(a))
            o = max(0.0, min(1.0, (a - 0.08) / 0.2, (1 - a) / 0.2))
            if o < 1:
                m.fade(1 - o)
            return m
        toks.append(t)
        anims.append(UpdateFromAlphaFunc(t, upd))
    scene.add(*toks)
    # one after another (unit, integration, system): they never meet at the shared elbow
    scene.play(LaggedStart(*anims, lag_ratio=0.8), run_time=run_time)
    scene.remove(*toks)
    scene.play(Indicate(g.nodes["test-summary"].mark, color=ROUTE), run_time=0.5)


def _gap_path(g: JobGraph) -> VMobject:
    """The lint → summary elbow (the gap's own path), solid, for a dashed arrow on top of it."""
    lint, summ = g.nodes["lint-and-format"], g.nodes["test-summary"]
    p, q = lint.get_right(), summ.get_left()
    xm = p[0] + (q[0] - p[0]) * 0.62
    m = VMobject()
    m.set_points_as_corners([p, np.array([xm, p[1], 0]), np.array([xm, q[1], 0]), q + LEFT * 0.12])
    return m
