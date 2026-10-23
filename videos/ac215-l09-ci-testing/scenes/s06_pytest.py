"""S06 · pytest, under the hood (concept scene, no tracker).

Beats (script.md, ## S06; one voiceover block each). GREY tag `Lecture 9 · slides 26, 58–61`
top right for the whole scene.
0. A PURPLE `pytest` chip, then CODE(cheese-app-ci-cd/pytest.ini) in two windows (code() never shows
   more than 12 lines): lines 4–9 with the three `test_*` rules (6–8) highlighted in turn (their
   patterns turn GREEN, the colour the collector lights them), then the panel scrolls to 11–17 and
   line 17 `-ra` turns YELLOW with the caption "the summary where skips confess".
1. V3 collector: the tests/ tree, a YELLOW scanner sweeps, 26 tiles light GREEN, counter 26.
2. The tree dims and moves down; README card (README.md · line 388) with the echo line; the
   `broken` glyphs fly out of the card into the unit folder as a dark chip. PONDER (8 s).
3. Second sweep: `broken` stays dark beside a GREY ruler `python_functions = test_*` (cross between),
   a GREEN `test_broken` lights up past a check, `erratum` tag on the README card.
4. Two illustration cards, each tagged (assert shows both values · approx for floats: a value a
   hair off 2.0 falls inside the default rel 1e-6 band, drawn wide) above
   CODE(tests/unit/test_utils.py: 69–72) with `pytest.raises(TypeError)` GREEN; on "the invalid tray
   from earlier" S02's invalid tray returns with `power("3", 4)` in it.
5. CODE(tests/integration/test_api.py: 7–11), line 11 highlighted; `client` flies into a conftest.py
   box (V3 FixtureWiring, GREY caption "what it could look like · not this repo's code"): tests ask
   for it, fresh copies per test (default), then one shared instance (scope="session"); then
   Parametrize's four power() assert cards (top) fold into one function (below): each card's inputs
   fly into its input chip (shows what became what; no text morph). Fade to an empty frame.
"""

import numpy as np  # noqa: I001  (manim first, then common: common must win)
from manim import *

from explainer.scene import VoiceScene
from explainer import style as S

from common import (ERR, INK, MONO, NARRATION, PARAM_CASES, PASS, TOOL, TURN, UNIT, Collector, FixtureWiring,
                    Parametrize, check_mark, chip, code, code_span, cross_mark, erratum_tag, grey_chip,
                    illustration_tag, label, line_bar, lref, ring, mono, mono_line, note, pause_and_ponder, readme,
                    readme_card, substring, tool_chip, under)

SAY = NARRATION["S06"]
INI = "cheese-app-ci-cd/pytest.ini"
UTILS = "cheese-app-ci-cd/tests/unit/test_utils.py"
API = "cheese-app-ci-cd/tests/integration/test_api.py"
ECHO = 'echo "def broken(): assert False" >> tests/unit/test_utils.py'


def bin_tray(name: str, tray_w: float = 2.9, wall_h: float = 0.6) -> VGroup:
    """S02's open 'invalid' tray (slide 25's bins), drawn at the origin. .shape .text .spot"""
    shape = VMobject(stroke_color=S.GREY, stroke_width=3)
    pts = [[-tray_w / 2, wall_h, 0], [-tray_w / 2 + 0.12, 0, 0], [tray_w / 2 - 0.12, 0, 0], [tray_w / 2, wall_h, 0]]
    shape.set_points_as_corners(pts)
    fill = Polygon(*pts, stroke_width=0).set_fill(S.GREY, 0.1)
    t = label(name, 24, INK).next_to(shape, DOWN, buff=0.12)
    g = VGroup(fill, shape, t)
    g.shape, g.text = shape, t
    g.spot = Dot(radius=0.001, fill_opacity=0).move_to([0, 0.3, 0])
    g.add(g.spot)
    return g


def glyphs_of(t: Text, full: str, sub: str) -> VGroup:
    """The glyphs of `sub` inside a chip's Text built from `full` (Text drops spaces and their glyphs)."""
    assert len(t.submobjects) == len("".join(full.split())), full
    i = full.index(sub)
    a, n = len("".join(full[:i].split())), len("".join(sub.split()))
    return VGroup(*t.submobjects[a:a + n])


def mini_card(title: str, card_w: float = 5.9, card_h: float = 2.8) -> VGroup:
    """An empty card with its title at the top. .frame .title"""
    frame = RoundedRectangle(width=card_w, height=card_h, corner_radius=0.16, stroke_color=S.GREY,
                             stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
    t = label(title, 26, INK).next_to(frame.get_top(), DOWN, buff=0.22)
    g = VGroup(frame, t)
    g.frame, g.title = frame, t
    return g


class PytestInside(VoiceScene):
    def construct(self):
        assert len(SAY) == 6, len(SAY)
        assert readme(388) == ECHO, readme(388)

        # ========================================================== 0. the rules in pytest.ini
        ref = lref("26, 58–61")
        pyt = tool_chip("pytest", size=28).move_to([0, 0.3, 0])
        w1 = code(INI, 4, 9, font_size=26)
        w1.move_to([1.3, 0.45, 0])
        w2 = code(INI, 11, 17, font_size=26)
        w2.move_to(w1, aligned_edge=UL)
        pats = [code_span(w1.code, k - 4, s) for k, s in ((6, "test_*.py"), (7, "Test*"), (8, "test_*"))]
        bar = line_bar(w1.code, 6 - 4, TURN, 0.2)
        reads = Arrow(LEFT, RIGHT, color=S.GREY, stroke_width=3, buff=0, tip_length=0.18)
        what = note("finds tests · runs them · reports", S.GREY, 22)
        rings = VGroup()

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(ref), FadeIn(pyt, scale=0.9), run_time=0.7)
            what.next_to(pyt, DOWN, buff=0.3)
            self.play(FadeIn(what, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("The config file pytest.ini")
            self.play(FadeOut(what), pyt.animate.move_to([-4.6, 0.3, 0]), run_time=0.7)
            self.remove(what)
            reads.put_start_and_end_on(pyt.get_right() + RIGHT * 0.15, w1.get_left() + LEFT * 0.15)
            self.play(FadeIn(w1, shift=LEFT * 0.2), GrowArrow(reads), run_time=0.8)
            for p, k, anchor in zip(pats, (6, 7, 8), ("files named test underscore", "classes named Test",
                                                       "functions named test underscore")):
                vo.wait_until(anchor)
                target = line_bar(w1.code, k - 4, TURN, 0.2)
                rg = ring(p, PASS, buff=0.06)
                rings.add(rg)
                if k == 6:
                    self.play(FadeIn(bar), p.animate.set_color(PASS), Create(rg), run_time=0.5)
                else:
                    self.play(Transform(bar, target), p.animate.set_color(PASS), Create(rg), run_time=0.5)
                self.play(Indicate(p, color=PASS, scale_factor=1.12), run_time=0.6)
            vo.wait_until("It also adds options")
            # scroll: lines 4-9 leave upwards, 11-17 rise from below
            self.play(FadeOut(VGroup(bar, rings)), run_time=0.3)
            self.remove(bar, rings)
            self.play(FadeOut(w1, shift=UP * 0.6), FadeIn(w2, shift=UP * 0.6), run_time=0.8)
            self.remove(w1)
            addopts = code_span(w2.code, 12 - 11, "addopts")
            self.play(Indicate(addopts, color=INK, scale_factor=1.1), run_time=0.7)
            vo.wait_until("dash r a")
            ra = code_span(w2.code, 17 - 11, "-ra")
            bar2 = line_bar(w2.code, 17 - 11, TURN, 0.22)
            self.play(FadeIn(bar2), ra.animate.set_color(TURN), run_time=0.5)
            self.play(Indicate(ra, color=TURN, scale_factor=1.25), run_time=0.7)
            vo.wait_until("the summary of everything")
            cap = label("the summary where skips confess", 26, TURN)
            cap.next_to(w2, DOWN, buff=0.35).align_to(w2, LEFT)
            self.play(FadeIn(cap, shift=UP * 0.15), run_time=0.6)

        # ========================================================== 1. the collector sweeps
        col = Collector()
        col.move_to([0, 0.2, 0])

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(pyt, reads, w2, bar2, cap)), run_time=0.5)
            self.remove(pyt, reads, w2, bar2, cap)
            self.play(FadeIn(col, shift=UP * 0.2), run_time=0.7)
            vo.wait_until("every matching name")
            col.sweep(self, run_time=3.0)
            vo.wait_until("26 tests in all")
            self.play(Indicate(col.counter, color=PASS, scale_factor=1.2), run_time=0.8)

        # ========================================================== 2. README Part 6 + ponder
        line = mono_line(ECHO, 22, INK)
        card = readme_card(388, line)
        card.move_to([0, 2.45, 0])
        dbroken = substring(line, "def broken(): assert False")
        name = substring(line, "broken")
        col.save_state()
        col.generate_target()
        col.target.shift(UP * (card.get_bottom()[1] - 0.3 - col.get_top()[1])).fade(0.55)
        dark = col.extra("broken", "unit")
        dark.shift(UP * (card.get_bottom()[1] - 0.3 - col.get_top()[1]))
        dline = under(dbroken, INK, stroke=3)

        with self.voiceover(SAY[2]) as vo:
            self.play(MoveToTarget(col), run_time=0.8)
            vo.wait_until("A later README part")
            self.play(FadeIn(card, shift=DOWN * 0.2), run_time=0.7)
            vo.wait_until("def broken, assert False")
            self.play(Create(dline), Indicate(dbroken, color=INK, scale_factor=1.05), run_time=0.8)
            vo.wait_until("to a test file")
            fly = name.copy()
            self.play(fly.animate(rate_func=smooth).move_to(dark.text), run_time=1.0)
            self.play(FadeIn(dark.box, scale=1.15), ReplacementTransform(fly, dark.text), run_time=0.4)
            vo.wait_until("Will the unit test run go red?")
            unit_tiles = col.columns["unit"].tiles
            self.play(Indicate(VGroup(unit_tiles, dark), color=TURN, scale_factor=1.03), run_time=0.9)
        ponder = pause_and_ponder(self, "README Part 6 appends def broken(): assert False\n"
                                        "to a test file. Will the unit tests go red?", seconds=8, width=11.6)

        # ========================================================== 3. it stays dark
        cross = cross_mark(0.3, S.GREY)
        ruler = grey_chip("python_functions = test_*", size=22, mono_font=True)
        tick = check_mark(0.32, PASS)
        lit = chip("test_broken", PASS, size=20, font=MONO, fill_opacity=0.35)
        row = VGroup(cross, ruler, tick, lit).arrange(RIGHT, buff=0.3)
        row.next_to(dark, RIGHT, buff=0.3)
        err = erratum_tag()
        err.move_to([card.frame.get_right()[0] - err.width / 2 - 0.25, card.head.get_center()[1], 0])

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(ponder), run_time=0.5)
            self.remove(ponder)
            vo.wait_until("Watch the collector")
            # back to full strength (the dark chip is not part of the tree)
            col.saved_state.shift(UP * (col.get_top()[1] - col.saved_state.get_top()[1]))
            self.play(Restore(col), dline.animate.set_stroke(opacity=0.4), run_time=0.6)
            sx = col.scanner.get_x()           # the scanner now reaches down past the appended chip
            col.scanner.put_start_and_end_on([sx, col.get_top()[1] + 0.1, 0], [sx, dark.get_bottom()[1] - 0.1, 0])
            col.sweep(self, run_time=2.2, again=True)
            vo.wait_until("stays dark")
            self.play(Indicate(dark, color=S.GREY, scale_factor=1.2), run_time=0.8)
            vo.wait_until("The name does not match")
            self.play(FadeIn(ruler, shift=LEFT * 0.2), run_time=0.6)
            self.play(Create(cross), run_time=0.4)
            vo.wait_until("never collected, never run")
            self.play(Indicate(col.counter, color=INK, scale_factor=1.2), run_time=0.8)
            vo.wait_until("call it test underscore broken")
            self.play(Create(tick), FadeTransform(dark.copy(), lit), run_time=0.8)
            self.play(Indicate(lit, color=PASS, scale_factor=1.15), FadeIn(err, shift=LEFT * 0.15), run_time=0.8)
            vo.wait_until("cuts both ways")
            self.play(Indicate(ruler, color=INK, scale_factor=1.08), run_time=0.9)

        # ========================================================== 4. three more verbs
        ca = mini_card("assert shows both values").move_to([-3.25, 1.5, 0])
        cb = mini_card("approx for floats").move_to([3.25, 1.5, 0])
        ill = illustration_tag().next_to(ca.frame, UP, buff=0.12).align_to(ca.frame, LEFT)
        ill2 = illustration_tag().next_to(cb.frame, UP, buff=0.12).align_to(cb.frame, LEFT)
        # card A: a failed compare, both sides printed under it (illustration)
        expr = mono_line("assert power(2, 3) == 9", 24, INK)
        expr.move_to(ca.frame).shift(UP * 0.1)
        lhs, rhs = substring(expr, "power(2, 3)"), substring(expr, "9")
        v_l = chip("8", ERR, size=24, font=MONO).next_to(lhs, DOWN, buff=0.45)
        v_r = chip("9", S.GREY, size=24, font=MONO).next_to(rhs, DOWN, buff=0.45)
        neq = mono("≠", 28, ERR).move_to([(v_l.get_right()[0] + v_r.get_left()[0]) / 2, v_l.get_center()[1], 0])
        links = VGroup(Line(lhs.get_bottom() + DOWN * 0.06, v_l.get_top() + UP * 0.04),
                       Line(rhs.get_bottom() + DOWN * 0.06, v_r.get_top() + UP * 0.04)).set_stroke(S.GREY, 2)
        # card B: two values inside a tolerance band (illustration)
        axis = Line(LEFT * 2.3, RIGHT * 2.3, color=S.GREY, stroke_width=2).move_to(cb.frame).shift(DOWN * 0.3)
        band = Rectangle(width=1.4, height=0.5, stroke_color=PASS, stroke_width=2).set_fill(PASS, 0.18)
        band.move_to(axis)
        want = Dot(axis.get_center(), radius=0.09, color=INK)
        got = Dot(axis.get_center() + RIGHT * 0.32, radius=0.09, color=S.GREY)   # a hair off 2.0
        appr = mono_line("== pytest.approx(2.0)", 24, INK).next_to(band, UP, buff=0.32)
        rel = note("rel 1e-6", S.GREY, 20).next_to(band, DOWN, buff=0.12)
        # card C: the real code
        pc = code(UTILS, 69, 72, font_size=20)
        pc.move_to([-1.55, -1.95, 0])
        raises = code_span(pc.code, 71 - 69, "pytest.raises(TypeError)")
        bar71 = line_bar(pc.code, 71 - 69, PASS, 0.2)
        terr = code_span(pc.code, 71 - 69, "TypeError")
        tray = bin_tray("invalid")
        tray.move_to([4.95, -2.35, 0])
        inv = grey_chip('power("3", 4)', size=20, mono_font=True)
        call = code_span(pc.code, 72 - 69, 'power("3", 4)')
        old = VGroup(col, card, err, dark, row, dline)

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(old), run_time=0.6)
            self.remove(old)
            self.play(LaggedStart(FadeIn(ca, shift=UP * 0.2), FadeIn(cb, shift=UP * 0.2), lag_ratio=0.3),
                      FadeIn(ill), FadeIn(ill2), run_time=0.9)
            vo.wait_until("A plain assert")
            self.play(FadeIn(expr, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("shows both values")
            self.play(Create(links), FadeIn(v_l, shift=DOWN * 0.15), FadeIn(v_r, shift=DOWN * 0.15), run_time=0.6)
            self.play(FadeIn(neq, scale=1.4), run_time=0.4)
            vo.wait_until("For floats")
            self.play(Create(axis), FadeIn(want), FadeIn(got), FadeIn(appr), run_time=0.7)
            vo.wait_until("compares with a tolerance")
            self.play(GrowFromCenter(band), FadeIn(rel, shift=UP * 0.1), run_time=0.8)
            self.play(got.animate.set_color(PASS), band.animate.set_fill(PASS, 0.32), run_time=0.4)
            vo.wait_until("And pytest dot raises")
            self.play(FadeIn(pc, shift=UP * 0.2), run_time=0.6)
            self.play(FadeIn(bar71), raises.animate.set_color(PASS), run_time=0.5)
            vo.wait_until("the named error")
            self.play(Indicate(terr, color=PASS, scale_factor=1.15), run_time=0.7)
            vo.wait_until("the invalid tray")
            inv.move_to(tray.spot)
            self.play(FadeIn(tray, shift=LEFT * 0.3), run_time=0.5)
            fly = call.copy()
            self.play(fly.animate(rate_func=smooth).move_to(inv.text), run_time=0.8)
            self.play(FadeIn(inv.box, scale=1.15), ReplacementTransform(fly, inv.text), run_time=0.4)

        # ========================================================== 5. fixtures and parametrize
        pa = code(API, 7, 11)
        pa.move_to([0, 0.4, 0])
        bar11 = line_bar(pa.code, 11 - 7, TURN, 0.2)
        glob = note("module global · built once, at import", S.GREY, 22).next_to(pa, DOWN, buff=0.35)
        glob.align_to(pa, LEFT)
        cl = code_span(pa.code, 11 - 7, "client")
        fw = FixtureWiring()
        look = note("what it could look like · not this repo's code", S.GREY, 22)
        look.move_to([-6.4 + look.width / 2, 2.85, 0])
        copies, per_anims = fw.per_test()
        fresh = grey_chip('scope="function" · the default', size=20, mono_font=True)
        fresh.next_to(copies, DOWN, buff=0.25).align_to(fw.conftest.frame, LEFT)
        verbs4 = VGroup(ca, cb, ill, ill2, expr, v_l, v_r, neq, links, axis, band, want, got, appr, rel, pc, bar71, tray, inv)

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(verbs4), run_time=0.6)
            self.remove(verbs4)
            self.play(FadeIn(pa, shift=UP * 0.2), run_time=0.7)
            vo.wait_until("The integration tests build")
            self.play(FadeIn(bar11), run_time=0.4)
            vo.wait_until("as a module global")
            self.play(FadeIn(glob, shift=UP * 0.15), Indicate(cl, color=INK, scale_factor=1.15), run_time=0.8)
            vo.wait_until("A fixture would do it better")
            # the name leaves line 11 and becomes the fixture inside conftest.py
            fly = cl.copy()
            self.add(fly)
            self.play(FadeOut(VGroup(pa, bar11, glob)), fly.animate.move_to(fw.fixture.text), run_time=0.9)
            self.remove(pa, bar11, glob)
            self.play(FadeIn(fw.conftest), FadeIn(fw.fixture.box, scale=1.15), ReplacementTransform(fly, fw.fixture.text),
                      FadeIn(look, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("A test asks for client by name")
            self.play(LaggedStart(*[FadeIn(t, shift=LEFT * 0.2) for t in fw.tests], lag_ratio=0.25), run_time=0.9)
            self.play(LaggedStart(*[GrowArrow(a) for a in fw.asks], lag_ratio=0.2), FadeIn(fw.ask_label),
                      run_time=0.7)
            vo.wait_until("pytest builds and injects it")
            self.play(Indicate(fw.fixture, color=TOOL, scale_factor=1.2),
                      LaggedStart(*[Indicate(a, color=TOOL, scale_factor=1.0) for a in fw.asks], lag_ratio=0.2),
                      run_time=1.0)
            vo.wait_until("each test gets a fresh one")
            # the 'asks for' arrows step back so each copy's own line to its test reads clearly
            self.play(*per_anims, FadeIn(fresh, shift=UP * 0.1), fw.asks.animate.set_opacity(0.25), run_time=1.0)
            vo.wait_until("the whole run shares one")
            inst, sess_anims = fw.session()
            shared = grey_chip('scope="session" · one, shared', size=20, mono_font=True)
            shared.next_to(inst, DOWN, buff=0.3).align_to(fw.conftest.frame, LEFT)
            # the fresh copies collapse into one shared instance; the per-test links give way to one
            chips3, links3 = copies
            self.play(*[c.animate.move_to(inst[0]) for c in chips3], FadeOut(links3),
                      FadeTransform(fresh, shared), fw.asks.animate.set_opacity(1), run_time=0.6)
            self.remove(*chips3, *links3, chips3, links3, fresh)   # each copy was added on its own
            self.add(inst[0])
            self.play(*sess_anims[1:], run_time=0.6)
            vo.wait_until("And parametrize")
            # four would-be copies of one test (test_utils.py:15-18) above; the one function below
            pz = Parametrize()
            pz.cards.move_to([0, 1.45, 0])
            m = pz.merged
            m.move_to([0, -0.95, 0])
            self.play(FadeOut(VGroup(fw, fw.ask_label, inst, shared)), run_time=0.5)
            self.remove(fw, fw.ask_label, inst, shared)
            self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.15) for c in pz.cards], lag_ratio=0.15), run_time=0.7)
            vo.wait_until("into one function")
            # each copy's inputs leave its card and become one input row of the single function
            flies, homes = VGroup(), []
            for c, ch, (a, b) in zip(pz.cards, m.chips, PARAM_CASES):
                for sub in (a, b):
                    flies.add(glyphs_of(c.text, f"assert power({a}) == {b}", sub).copy())
                    homes.append(glyphs_of(ch.text, f"({a}, {b})", sub))
            self.add(flies)
            self.play(FadeIn(m.frame), FadeIn(m.head, shift=DOWN * 0.1), pz.cards.animate.fade(0.6),
                      *[f.animate.move_to(h) for f, h in zip(flies, homes)], run_time=0.9)
            self.play(FadeIn(m.chips), FadeOut(pz.cards), run_time=0.35)
            self.remove(flies, pz.cards)
            vo.wait_until("four inputs")
            self.play(Indicate(m.chips, color=UNIT, scale_factor=1.1), run_time=0.8)
        self.wait(1.2)                         # the folded function is the last picture: let it be read

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
