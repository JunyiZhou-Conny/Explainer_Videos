"""S03 · Three kinds of test, and a gate (concept scene, no tracker, no terminal).

Beats (script.md, ## S03; one voiceover block each). GREY tag `Lecture 9 · slides 66, 95` (top
right, whole scene).
0. Unit: the glowing PINK token `GET /euclidean_distance/?x=3&y=4` at the top; the app's chain
   routing → validation → handler → power() (GREY: just the app). `power()` turns GREEN and
   detaches from the handler; the rest swells and fades past the frame (the zoom) while the chip
   grows into a GREEN `unit test` box holding `power(3, 2)` (service.py:43 squares x with
   power(x, 2)); the token shrinks to the numbers 3 and 2, which drop into the call; a GREEN
   check and `9` pop out (test_utils.py:16 expects 9).
1. Integration: the unit box folds into a GREEN `unit` chip on a shelf at the bottom. A TEAL box
   `TestClient` wraps routing → validation → handler → power(); the token enters with no wire
   (becomes a PINK dot), hops through the four chips as they are named, and leaves as the PINK
   JSON chip `{"distance": 5.0}`. Caption "in-process · no socket"; then the capture's own count
   `10 passed, 1 warning in 0.41s` (part3-opt1-03:24) with `at the time of recording`.
2. System: the integration box folds into a TEAL shelf chip. A BLUE `system test` box and a BLUE
   `the running server` box with `port 9000`; a dark "black box" covers the server's insides.
   The request (PINK dot) leaves the test, rides the PINK wire to port 9000 and comes back as the
   JSON chip. "most honest · slowest · most fragile": on "fragile" the wire flickers.
3. The system boxes fold into a BLUE shelf chip; the three chips stack into the README's pyramid
   (TestPyramid: GREEN "unit · many, fast", TEAL, BLUE "system · few, slow"); a GREY "cost per
   test" arrow up its right side.
4. The pyramid re-draws as the lecture's nested boxes (NestedKinds); the GREEN dashed hermetic
   border closes around unit and integration; GREEN caption "hermetic: only your code can make it
   fail"; the PINK wire crosses the border to `server :9000`, which goes down (GREY, RED cross).
5. Back to the pyramid with two faint dashed rows (smoke, acceptance · none yet). Then the
   erratum cards, stacked (side by side would need ~20 units at 22 pt): CODE(test_system_api.py:
   1–4), the header's `system` folder underlined BLUE, line 2 "Integration tests" struck YELLOW
   with "system" written above it; CODE(pytest.ini: 19–23) with the GREY caption "markers defined,
   never used". Tag `erratum` beside the first card.
6. The cards fade; the empty gate table (built at 30 pt) slides in; its four headers light YELLOW
   in turn; it shrinks (a Transform into the 20 pt table, never a scale) to its resting place and
   everything fades.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene
from explainer import style as S

from common import (ERR, INK, INTEG, MODIFIED, MONO, RESPONSE, ROUTE, SYSTEM_TEST, UNIT, NARRATION, GateTable,
                    NestedKinds, RequestToken, TestPyramid, app_chain, capture, check_mark,
                    chip, code, code_span, cross_mark, erratum_tag, kind_box, label, line_bar, lref, mono,
                    note, recording_tag, ring, strike, under)

SAY = NARRATION["S03"]
SYS_FILE = "cheese-app-ci-cd/tests/system/test_system_api.py"
INI = "cheese-app-ci-cd/pytest.ini"


def shelf_chip(kind: str, color) -> VGroup:
    """A finished test kind, parked on the shelf at the bottom (22 pt chip in its colour)."""
    return chip(kind, color, size=22)


def shelf_x(i: int) -> float:
    return -3.2 + 3.2 * i


SHELF_Y = -3.1


class ThreeKinds(VoiceScene):
    def construct(self):
        assert len(SAY) == 7, len(SAY)
        ref = lref("66, 95")

        # ========================================================== 0. unit: power(3, 2) alone
        tok = RequestToken().move_to([0, 2.45, 0])
        xy = VGroup(*tok.text[-7:])                       # the glyphs of "x=3&y=4"
        chain = app_chain(color=S.GREY)
        chain.move_to([0, 0.55, 0])
        app_name = label("the FastAPI app", 22, S.GREY).next_to(chain, UP, buff=0.35).align_to(chain, LEFT)
        handler, pw = chain.chips[2], chain.chips[3]
        to_pw = chain.arrows[2]
        rest = VGroup(*chain.chips[:3], *chain.arrows[:2], app_name)

        ubox = kind_box("unit", "unit test", 5.2, 2.3, size=24)
        ubox.move_to([0, -0.75, 0])
        call = mono("power(3, 2)", 36, INK).move_to(ubox.frame).shift(DOWN * 0.15)
        three, two = call[6], call[8]
        n3 = chip("3", ROUTE, size=24, font=MONO)
        n2 = chip("2", ROUTE, size=24, font=MONO)
        nums = VGroup(n3, n2).arrange(RIGHT, buff=0.5).move_to(tok)
        ok = check_mark(0.5, UNIT, 7)
        nine = mono("9", 36, UNIT)
        res = VGroup(ok, nine).arrange(RIGHT, buff=0.25).next_to(ubox.frame, RIGHT, buff=0.45)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(ref), FadeIn(tok, shift=DOWN * 0.2), run_time=0.8)
            vo.wait_until("get euclidean distance")
            self.play(tok.glow.animate.set_stroke(width=22, opacity=0.35), run_time=0.5)
            self.play(tok.glow.animate.set_stroke(width=12, opacity=0.18), run_time=0.5)
            vo.wait_until("with x 3 and y 4")
            xy_line = under(xy, ROUTE, stroke=3)
            self.play(Create(xy_line), run_time=0.6)
            vo.wait_until("Inside the handler")
            self.play(FadeIn(app_name), LaggedStart(*[FadeIn(m, shift=RIGHT * 0.15) for m in
                                                      (chain.chips[0], chain.arrows[0], chain.chips[1],
                                                       chain.arrows[1], handler, to_pw, pw)],
                                                    lag_ratio=0.15), FadeOut(xy_line), run_time=1.2)
            self.play(Indicate(handler, color=INK, scale_factor=1.12), run_time=0.7)
            vo.wait_until("power of 3 and 2")
            self.play(pw.box.animate.set_stroke(UNIT).set_fill(UNIT, 0.2), Indicate(pw.text, color=UNIT),
                      run_time=0.8)
            vo.wait_until("A unit test skips the app")
            # the chip comes loose from the handler
            self.play(FadeOut(to_pw), pw.animate.shift(DOWN * 1.1 + RIGHT * 0.3), run_time=0.8)
            self.play(rest.animate.fade(0.7), tok.animate.fade(0.5), run_time=0.5)
            vo.wait_until("calls that one function alone")
            # the zoom: the app swells past the frame and fades; the chip becomes the unit box,
            # the token becomes just its numbers
            self.play(rest.animate.scale(1.6, about_point=pw.get_center()).set_opacity(0),
                      ReplacementTransform(pw, VGroup(ubox, call)),
                      ReplacementTransform(tok, nums), run_time=1.3)
            self.remove(rest)
            self.play(n3.animate.move_to(three), n2.animate.move_to(two), run_time=0.8)
            self.play(FadeOut(nums, scale=0.6), Indicate(VGroup(three, two), color=ROUTE, scale_factor=1.3),
                      run_time=0.6)
            vo.wait_until("It is fast")
            self.play(Create(ok), FadeIn(nine, shift=LEFT * 0.2), run_time=0.6)
            vo.wait_until("you know where to look")
            where = ring(call, UNIT, buff=0.15, stroke=4)
            self.play(Create(where), Indicate(call, color=UNIT, scale_factor=1.08), run_time=0.9)

        # ========================================================== 1. integration: in process
        unit_g = VGroup(ubox, call, res, where)
        s_unit = shelf_chip("unit", UNIT).move_to([shelf_x(0), SHELF_Y, 0])

        ibox = kind_box("integration", "integration test", 11.6, 2.2, size=22)
        ibox.move_to([0, 0.35, 0])
        tc = mono("TestClient", 22, INTEG).next_to(ibox.title, RIGHT, buff=0.3).align_to(ibox.title, DOWN)
        ichain = app_chain(color=INTEG).move_to(ibox.frame).shift(DOWN * 0.25)
        tok2 = RequestToken().move_to([-6.3 + RequestToken().width / 2, 2.55, 0])
        dot = Dot(radius=0.12, color=ROUTE)
        hops = [c.get_top() + UP * 0.2 for c in ichain.chips]
        entry = np.array([ibox.frame.get_left()[0] + 0.3, ichain.get_center()[1], 0])
        json = chip(RESPONSE, ROUTE, size=22, font=MONO).move_to([3.6, 2.55, 0])
        cap = note("in-process · no socket", S.GREY, 24).next_to(ibox.frame, DOWN, buff=0.35)
        line = capture("part3-opt1-03").line(24).strip("= ")
        timing = mono(line, 22, INK)
        timing[:8].set_color(UNIT)                       # "10passed" (no space glyph)
        rec = recording_tag()
        tim = VGroup(timing, rec).arrange(RIGHT, buff=0.35).next_to(cap, DOWN, buff=0.4)

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeTransform(unit_g, s_unit), run_time=0.9)
            vo.wait_until("wires several of our parts")
            self.play(FadeIn(ibox), FadeIn(tc), LaggedStart(*[FadeIn(c, shift=RIGHT * 0.15) for c in
                                                             [*ichain.chips, *ichain.arrows]], lag_ratio=0.1),
                      run_time=1.1)
            vo.wait_until("The test client hands the request")
            self.play(FadeIn(tok2, shift=DOWN * 0.2), Indicate(tc, color=INTEG, scale_factor=1.1), run_time=0.7)
            vo.wait_until("straight to the FastAPI app")
            # no wire: the token drops straight into the box and becomes the request inside
            dot.move_to(tok2.get_left() + RIGHT * 0.3)
            self.play(FadeTransform(tok2, dot), run_time=0.6)
            self.play(dot.animate.move_to(entry), run_time=0.5)
            for k, anchor in enumerate(("routing,", "validation,", "handler and power", "power all run")):
                vo.wait_until(anchor)
                self.play(dot.animate.move_to(hops[k]), Indicate(ichain.chips[k], color=INK, scale_factor=1.1),
                          run_time=0.5)
            # back through the handler, out of the box as JSON
            self.play(dot.animate.move_to(hops[2]), run_time=0.35)
            self.play(dot.animate.move_to(json.get_center()), run_time=0.5)
            self.play(FadeTransform(dot, json), run_time=0.5)
            vo.wait_until("but no server and no network")
            self.play(FadeIn(cap, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("Ten of those run here")
            self.play(FadeIn(timing, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("at the time of recording")
            self.play(FadeIn(rec, shift=LEFT * 0.15), run_time=0.5)

        # ========================================================== 2. system: over a real wire
        integ_g = VGroup(ibox, tc, ichain)
        s_integ = shelf_chip("integration", INTEG).move_to([shelf_x(1), SHELF_Y, 0])

        tbox = kind_box("system", "system test", 4.0, 2.0, size=22).move_to([-4.3, 0.35, 0])
        sbox = kind_box("system", "the running server", 4.8, 2.0, size=22).move_to([3.9, 0.35, 0])
        port = chip("port 9000", SYSTEM_TEST, size=20, font=MONO)
        port.move_to(sbox.frame).align_to(sbox.frame, LEFT).shift(RIGHT * 0.2 + DOWN * 0.22)
        bb = RoundedRectangle(width=sbox.frame.width - port.width - 0.65, height=1.05, corner_radius=0.08,
                              stroke_color=S.GREY, stroke_width=2).set_fill("#000000", 1)
        bb.next_to(port, RIGHT, buff=0.25)
        bb_t = label("black box", 20, S.GREY).move_to(bb)
        wy = port.get_center()[1]
        wire = Line([tbox.frame.get_right()[0], wy, 0], port.get_left(), color=ROUTE, stroke_width=4)
        tok3 = RequestToken().move_to([-6.3 + RequestToken().width / 2, 2.55, 0])
        dot2 = Dot(radius=0.12, color=ROUTE).move_to([tbox.frame.get_center()[0], wy, 0])
        json2 = chip(RESPONSE, ROUTE, size=20, font=MONO).move_to(dot2)
        words = VGroup(label("most honest", 24, INK), label("·", 24, S.GREY), label("slowest", 24, S.GREY),
                       label("·", 24, S.GREY), label("most fragile", 24, S.GREY))
        words.arrange(RIGHT, buff=0.25).move_to([0, -1.55, 0])

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(json, cap, tim)), FadeTransform(integ_g, s_integ), run_time=0.9)
            vo.wait_until("A system test treats")
            self.play(FadeIn(tbox, shift=RIGHT * 0.2), FadeIn(sbox, shift=LEFT * 0.2), FadeIn(port), run_time=0.8)
            vo.wait_until("as a black box")
            self.play(FadeIn(bb), FadeIn(bb_t), run_time=0.7)
            vo.wait_until("The request leaves the test")
            self.play(FadeIn(tok3, shift=DOWN * 0.2), Create(wire), run_time=0.7)
            self.play(FadeTransform(tok3, dot2), run_time=0.6)
            vo.wait_until("crosses a real network wire")
            self.play(dot2.animate.move_to(port.get_left()), run_time=1.0, rate_func=linear)
            vo.wait_until("to port 9000")
            self.play(Indicate(port, color=SYSTEM_TEST, scale_factor=1.12), dot2.animate.move_to(bb), run_time=0.7)
            vo.wait_until("comes back as JSON")
            self.play(dot2.animate.move_to([tbox.frame.get_right()[0] - 0.2, wy, 0]), run_time=0.9,
                      rate_func=linear)
            self.play(FadeTransform(dot2, json2), run_time=0.5)
            vo.wait_until("the most honest test")
            self.play(FadeIn(words[0], shift=UP * 0.15), run_time=0.5)
            vo.wait_until("the slowest")
            self.play(FadeIn(words[1:3], shift=UP * 0.15), run_time=0.5)
            vo.wait_until("most fragile")
            self.play(FadeIn(words[3:], shift=UP * 0.15), run_time=0.5)
            self.play(wire.animate.set_stroke(opacity=0.15), run_time=0.2)
            self.play(wire.animate.set_stroke(opacity=1), run_time=0.2)
            self.play(wire.animate.set_stroke(opacity=0.15), run_time=0.2)
            self.play(wire.animate.set_stroke(opacity=1), run_time=0.2)

        # ========================================================== 3. the pyramid
        sys_g = VGroup(tbox, sbox, port, bb, bb_t, wire, json2)
        s_sys = shelf_chip("system", SYSTEM_TEST).move_to([shelf_x(2), SHELF_Y, 0])
        pyr = TestPyramid().move_to([0, 0.1, 0])
        lay = pyr.layers
        cost = Arrow([4.4, lay["unit"].get_bottom()[1], 0], [4.4, lay["system"].get_top()[1], 0], buff=0,
                     color=S.GREY, stroke_width=3, tip_length=0.2)
        cost_t = label("cost per test", 22, S.GREY).next_to(cost, RIGHT, buff=0.2)

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(words), FadeTransform(sys_g, s_sys), run_time=0.9)
            vo.wait_until("that is the testing pyramid")
            self.play(ReplacementTransform(s_unit, lay["unit"]), ReplacementTransform(s_integ, lay["integration"]),
                      ReplacementTransform(s_sys, lay["system"]), run_time=1.3)
            vo.wait_until("many cheap unit tests")
            self.play(Indicate(lay["unit"], color=UNIT, scale_factor=1.06), run_time=0.9)
            vo.wait_until("few expensive system tests")
            self.play(Indicate(lay["system"], color=SYSTEM_TEST, scale_factor=1.12), GrowArrow(cost),
                      FadeIn(cost_t, shift=LEFT * 0.15), run_time=1.0)

        # ========================================================== 4. the hermetic border
        nk = NestedKinds().move_to([0, 0.45, 0])
        herm = note("hermetic: only your code can make it fail", UNIT, 24).move_to([0, -2.4, 0])
        down = cross_mark(0.36, ERR, 6).next_to(nk.server, UP, buff=0.15)

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(cost, cost_t)), FadeTransform(lay["unit"], nk.unit),
                      FadeTransform(lay["integration"], nk.integration),
                      FadeTransform(lay["system"], nk.system), run_time=1.3)
            self.remove(nk.unit, nk.integration, nk.system)
            self.add(nk.system, nk.integration, nk.unit)
            self.play(Create(nk.wire), FadeIn(nk.server), run_time=0.6)
            vo.wait_until("a border.")
            self.play(Create(nk.border.frame), run_time=1.0)
            self.play(FadeIn(nk.border.text), run_time=0.4)
            vo.wait_until("A test is hermetic")
            self.play(Indicate(nk.border.text, color=UNIT, scale_factor=1.2), FadeIn(herm, shift=UP * 0.15),
                      run_time=0.9)
            vo.wait_until("Unit and integration tests live inside")
            self.play(Indicate(nk.unit, color=UNIT, scale_factor=1.05), run_time=0.6)
            self.play(Indicate(nk.integration.frame, color=INTEG, scale_factor=1.03), run_time=0.6)
            vo.wait_until("The system test crosses it")
            self.play(ShowPassingFlash(nk.wire.copy().set_stroke(INK, 8), time_width=0.5),
                      Indicate(nk.system.title, color=SYSTEM_TEST), run_time=1.0)
            vo.wait_until("a live server can be down")
            self.play(nk.server.animate.set_opacity(0.35), nk.wire.animate.set_stroke(opacity=0.3),
                      Create(down), run_time=0.8)
            vo.wait_until("not your bug")
            self.play(Indicate(down, color=ERR, scale_factor=1.25), run_time=0.7)

        # ========================================================== 5. faint rows, and an erratum
        pyr2 = TestPyramid().move_to([0, 0.95, 0])
        extra = pyr2.extra_rows()
        lay2 = pyr2.layers

        sysc = code(SYS_FILE, 1, 4).to_corner(UL, buff=0.6).shift(DOWN * 0.15)
        sys_folder = VGroup(*sysc.header[0][6:12])            # "system" in tests/system/...
        folder_line = under(sys_folder, SYSTEM_TEST, stroke=3)
        integ_words = code_span(sysc.code, 1, "Integration tests")
        cross = strike(integ_words, MODIFIED, 4)
        fix = label("system", 22, MODIFIED)
        fix.next_to(integ_words, UP, buff=0.04).align_to(integ_words, LEFT).shift(RIGHT * 0.9)
        etag = erratum_tag().next_to(sysc, RIGHT, buff=0.5).align_to(sysc.code, UP)
        inic = code(INI, 19, 23)
        inic.next_to(sysc, DOWN, buff=0.45).align_to(sysc, LEFT)
        bars = VGroup(*[line_bar(inic.code, k, S.GREY, 0.2) for k in (2, 3, 4)])
        never = note("markers defined, never used", S.GREY, 22).next_to(inic, DOWN, buff=0.25).align_to(inic, LEFT)

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(nk.border, nk.wire, nk.server, down, herm)),
                      FadeTransform(nk.unit, lay2["unit"]),
                      FadeTransform(nk.integration, lay2["integration"]),
                      FadeTransform(nk.system, lay2["system"]), run_time=1.2)
            vo.wait_until("a smoke test")
            self.play(FadeIn(extra[0], shift=UP * 0.15), run_time=0.6)
            vo.wait_until("acceptance tests")
            self.play(FadeIn(extra[1], shift=UP * 0.15), run_time=0.6)
            vo.wait_until("for now")
            self.play(Indicate(extra[1][1], color=INK, scale_factor=1.08), run_time=0.7)
            vo.wait_until("One note about kinds")
            self.play(FadeOut(VGroup(*lay2.values(), extra)), run_time=0.6)
            self.play(FadeIn(sysc, shift=UP * 0.2), FadeIn(etag, shift=LEFT * 0.2), run_time=0.8)
            vo.wait_until("not by its folder")
            self.play(Create(folder_line), sys_folder.animate.set_color(SYSTEM_TEST), run_time=0.7)
            vo.wait_until("calls itself integration tests")
            self.play(Create(cross), run_time=0.6)
            self.play(FadeIn(fix, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("its pytest config defines markers")
            self.play(FadeIn(inic, shift=UP * 0.2), run_time=0.8)
            vo.wait_until("labels for selecting tests")
            self.play(FadeIn(bars), run_time=0.6)
            vo.wait_until("that nobody uses")
            self.play(FadeIn(never, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("markers return in part 2")
            self.play(Indicate(never, color=INK, scale_factor=1.08), run_time=0.8)

        # ========================================================== 6. the empty gate table
        big = GateTable(size=30, row_h=0.75).move_to([0, 0.4, 0])
        small = GateTable().move_to([0, -1.2, 0])

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(sysc, etag, folder_line, cross, fix, inic, bars, never)), run_time=0.6)
            vo.wait_until("an empty table")
            self.play(FadeIn(big, shift=LEFT * 1.5), run_time=1.0)
            for i, anchor in enumerate(("What is checked", "how,", "with which command",
                                        "does it run on every commit")):
                vo.wait_until(anchor)
                self.play(big.header_pulse(i, run_time=0.7))
            vo.wait_until("Part 1 fills it in")
            self.play(ReplacementTransform(big, small), run_time=1.0)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
