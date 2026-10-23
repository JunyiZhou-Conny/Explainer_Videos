"""S02 · The bug that almost shipped (concept scene, no tracker).

Beats (script.md, ## S02; one voiceover block each):
0. The repo's history (cheese-app-ci-cd-history/git-log-oneline.txt: 1–8) as a GREY commit chain,
   oldest left, newest right, under a GREY time arrow ("older" → "newer"): 91eb786 → c2dce32 (RED)
   → 8eb63fc → one GREY ellipsis dot "3 more" (1a5e363, 199abd9, 3dea317) → c3b227f (RED, its
   `sqrt(2 * z)`) → b8458ff (GREEN, HEAD, `sqrt(z)` again). The commit messages are the log's own.
   Tag `Lecture 9 · slides 25, 27–28` for the whole scene. A 3-row strip with the GREY `extra` tag
   types `git log -1 --format='%H %ci'` and prints laptop/02:2 (66 characters: the house `…` cut
   drops the last digit of the time zone); its hash rings GREEN, its date is underlined.
1. A plane: the point (3, 4) with its dashed projections; a GREEN radius sweeps the circle of
   radius 5 ("5"); a RED arrow along the same ray overshoots to √50 ("√50 ≈ 7.07"). Beside it the
   two computations (docstring vs line 44 of c3b227f, S01) and the GREY caption "no crash · just
   wrong". No error icon.
2. CODE(cheese-app-ci-cd/tests/integration/test_api.py: 31–38): the request `?x=3&y=4` (line 33)
   is underlined PINK, line 38 `assert data["distance"] == 5.0` turns GREEN; GREY chip "an
   executable specification"; the RED arrow (with its 7.07) comes down and bounces off the panel.
3. The panel becomes the GREEN chip "the test", the arrow the TEAL chip "the code", on a card "two
   suspects"; a YELLOW "fix this" stamp and arrow land on the code chip; GREY caption "slide 28:
   when a test fails, fix the code"; a dashed "rewrite the test to match the bug" under the test
   chip gets struck RED on "into a diary".
4. Three trays slide in (slide 25 redrawn): normal, edge, invalid. `power(2, 3)` drops into normal;
   `0`, `inf`, `nan` into edge; CODE(cheese-app-ci-cd/tests/unit/test_utils.py: 69–76) appears above
   the invalid tray, `pytest.raises(TypeError)` (line 71) is barred, and `power("3", 4)` (line 72)
   leaves the panel and drops into the invalid tray. Fade to an empty frame.
"""

import numpy as np  # noqa: I001  (manim first, then common: common must win)
from manim import *

from explainer.scene import VoiceScene
from explainer import style as S

from common import (ERR, IMAGE, INK, MONO, NARRATION, P_LAPTOP, ROUTE, TURN, VENV, arrow, capture,
                    chip, code, code_span, dashed_chip, extra_tag, grey_chip, label, line_bar, lref,
                    mono, ring, source_text, strike, substring, term, type_cmd, under)

SAY = NARRATION["S02"]
LOG = "cheese-app-ci-cd-history/git-log-oneline.txt"
TEST_API = "cheese-app-ci-cd/tests/integration/test_api.py"
TEST_UTILS = "cheese-app-ci-cd/tests/unit/test_utils.py"

CHAIN_Y = 1.0                      # the commit line (the picture band above a 3-row strip)
NODE_X = (-5.3, -3.0, -0.7, 0.95, 2.6, 4.9)


def log_lines() -> dict[str, str]:
    """git-log-oneline.txt as {short hash: message} (the file's own text)."""
    out = {}
    for ln in source_text(LOG).strip("\n").split("\n"):
        h, _, msg = ln.partition(" ")
        out[h] = msg
    return out


def commit_node(x: float, sha: str, msg_lines, color=S.GREY) -> VGroup:
    """A commit: dot on the chain, short hash above, the message (quoted) below. .dot .sha .msg"""
    dot = Circle(radius=0.16, stroke_color=color, stroke_width=3).set_fill(color, 0.55)
    dot.move_to([x, CHAIN_Y, 0])
    sha_t = mono(sha, 20, INK).next_to(dot, UP, buff=0.2)
    msg = VGroup(*[label(s, 20, S.GREY) for s in msg_lines]).arrange(DOWN, buff=0.08)
    msg.next_to(dot, DOWN, buff=0.22)
    g = VGroup(dot, sha_t, msg)
    g.dot, g.sha, g.msg = dot, sha_t, msg
    return g


def bin_tray(name: str, x: float, tray_w: float = 3.5, wall_h: float = 0.75, floor_y: float = -2.75) -> VGroup:
    """An open tray (slide 25's bins): floor, two walls, its name underneath. .shape .text .spot"""
    shape = VMobject(stroke_color=S.GREY, stroke_width=3)
    shape.set_points_as_corners([[x - tray_w / 2, floor_y + wall_h, 0], [x - tray_w / 2 + 0.12, floor_y, 0],
                                 [x + tray_w / 2 - 0.12, floor_y, 0], [x + tray_w / 2, floor_y + wall_h, 0]])
    fill = Polygon([x - tray_w / 2, floor_y + wall_h, 0], [x - tray_w / 2 + 0.12, floor_y, 0],
                   [x + tray_w / 2 - 0.12, floor_y, 0], [x + tray_w / 2, floor_y + wall_h, 0],
                   stroke_width=0).set_fill(S.GREY, 0.1)
    t = label(name, 24, INK).next_to(shape, DOWN, buff=0.14)
    g = VGroup(fill, shape, t)
    g.shape, g.text = shape, t
    g.spot = np.array([x, floor_y + 0.33, 0])
    return g


class BugAlmostShipped(VoiceScene):
    def construct(self):
        assert len(SAY) == 5, len(SAY)
        log = log_lines()

        # ========================================================== 0. the repo's own log
        ref = lref("25, 27–28")
        older = label("older", 20, S.GREY)
        newer = label("newer", 20, S.GREY)
        t_y = 2.35
        older.move_to([-5.9, t_y, 0])
        newer.move_to([5.9, t_y, 0])
        t_arrow = Arrow([older.get_right()[0] + 0.1, t_y, 0], [newer.get_left()[0] - 0.1, t_y, 0], buff=0,
                        color=S.GREY, stroke_width=2.5, tip_length=0.18, max_tip_length_to_length_ratio=0.05)
        time_arrow = VGroup(older, t_arrow, newer)

        # the log's own messages, broken at spaces to fit 2.3 units per commit
        msgs = {"91eb786": ["“readd  messy", "code”"],
                "c2dce32": ["“readd messy code", "v2 - with wrong", "variable”"],
                "8eb63fc": ["“fixed the", "a problem”"]}
        for h, parts in msgs.items():
            assert " ".join(parts).strip("“”") == log[h], h
        n0 = commit_node(NODE_X[0], "91eb786", msgs["91eb786"])
        n1 = commit_node(NODE_X[1], "c2dce32", msgs["c2dce32"], ERR)
        n2 = commit_node(NODE_X[2], "8eb63fc", msgs["8eb63fc"])
        n4 = commit_node(NODE_X[4], "c3b227f", [f"“{log['c3b227f']}”"], ERR)
        n5 = commit_node(NODE_X[5], "b8458ff", [f"“{log['b8458ff']}”"], VENV)
        for h in ("1a5e363", "199abd9", "3dea317"):
            assert h in log                    # the three commits the ellipsis dot stands for
        ell_dot = Circle(radius=0.11, stroke_color=S.GREY, stroke_width=2.5).set_fill(S.BG, 1)
        ell_dot.move_to([NODE_X[3], CHAIN_Y, 0])
        ell_txt = label("3 more", 20, S.GREY).next_to(ell_dot, DOWN, buff=0.22)
        ell = VGroup(ell_dot, ell_txt)
        bug_note = mono("sqrt(2 * z)", 20, ERR).next_to(n4.msg, DOWN, buff=0.16)
        fix_note = mono("sqrt(z)", 20, VENV).next_to(n5.msg, DOWN, buff=0.16)
        head = chip("HEAD", VENV, size=20, font=MONO).next_to(fix_note, DOWN, buff=0.16)
        xs = [n0.dot, n1.dot, n2.dot, ell_dot, n4.dot, n5.dot]
        segs = [Line(a.get_right(), b.get_left(), color=S.GREY, stroke_width=3) for a, b in zip(xs, xs[1:])]
        chain = VGroup(time_arrow, *segs, n0, n1, n2, ell, n4, n5, bug_note, fix_note, head)

        strip = term(P_LAPTOP, rows=3)
        xt = extra_tag().next_to(strip.box, UP, buff=0.15).align_to(strip.box, LEFT)
        cap = capture("02-git-log")
        assert cap.cmd == "git log -1 --format='%H %ci'"

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(ref), FadeIn(older), FadeIn(newer), GrowArrow(t_arrow), run_time=1.0)
            vo.wait_until("This repo's own log")
            self.play(FadeIn(n0, shift=DOWN * 0.15), run_time=0.6)
            vo.wait_until("messy code re-added")
            self.play(Indicate(n0.msg, color=INK, scale_factor=1.08), run_time=0.7)
            vo.wait_until("then a crash")
            self.play(Create(segs[0]), FadeIn(n1, shift=LEFT * 0.2), run_time=0.7)
            self.play(Indicate(n1.dot, color=ERR, scale_factor=1.4), run_time=0.5)
            vo.wait_until("then a fix")
            self.play(Create(segs[1]), FadeIn(n2, shift=LEFT * 0.2), run_time=0.7)
            vo.wait_until("Then the class demo")
            self.play(Create(segs[2]), FadeIn(ell, shift=LEFT * 0.2), run_time=0.5)
            self.play(Create(segs[3]), FadeIn(n4, shift=LEFT * 0.2), run_time=0.6)
            vo.wait_until("the wrong square root in")
            self.play(FadeIn(bug_note, shift=UP * 0.1), Indicate(n4.dot, color=ERR, scale_factor=1.4),
                      run_time=0.7)
            vo.wait_until("and the revert took it out")
            self.play(Create(segs[4]), FadeIn(n5, shift=LEFT * 0.2), run_time=0.6)
            self.play(FadeIn(fix_note, shift=UP * 0.1), FadeIn(head, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("An extra git log")
            self.play(FadeIn(strip), FadeIn(xt, shift=RIGHT * 0.2), run_time=0.6)
            type_cmd(self, strip, cap.cmd, type_time=1.2)
            vo.wait_until("confirms the clone")
            out = strip.print(self, cap.at(2))[0]
            sha_out = substring(out, "b8458ff")
            r = ring(sha_out, VENV)
            self.play(Create(r), Indicate(head, color=VENV, scale_factor=1.15), run_time=0.8)
            vo.wait_until("from November 2025")
            u = under(substring(out, "2025-11-13"), INK, stroke=3)
            self.play(Create(u), run_time=0.6)

        # ========================================================== 1. 5 versus √50
        u_ = 0.5
        origin = np.array([-2.6, -0.5, 0])

        def P(x, y):
            return origin + u_ * np.array([x, y, 0])

        x_axis = Line(P(-6.4, 0), P(6.3, 0), color=S.GREY, stroke_width=2)
        y_axis = Line(P(0, -5.6), P(0, 6.0), color=S.GREY, stroke_width=2)
        ticks = VGroup(*[Line(P(k, 0) + DOWN * 0.06, P(k, 0) + UP * 0.06, color=S.GREY, stroke_width=2)
                         for k in range(-6, 7) if k],
                       *[Line(P(0, k) + LEFT * 0.06, P(0, k) + RIGHT * 0.06, color=S.GREY, stroke_width=2)
                         for k in range(-5, 7) if k])
        axes = VGroup(x_axis, y_axis, ticks)
        pt = Dot(P(3, 4), radius=0.09, color=INK)
        proj = VGroup(DashedLine(P(3, 4), P(3, 0), color=S.GREY, stroke_width=2, dash_length=0.08),
                      DashedLine(P(3, 4), P(0, 4), color=S.GREY, stroke_width=2, dash_length=0.08))
        three = label("3", 20, S.GREY).next_to(P(3, 0), DOWN, buff=0.12)
        four = label("4", 20, S.GREY).next_to(P(0, 4), LEFT, buff=0.12)
        pt_lbl = label("(3, 4)", 24, INK).move_to(P(3, 4) + np.array([0.75, -0.25, 0]))
        point = VGroup(proj, three, four, pt, pt_lbl)

        radius = Line(origin, P(3, 4), color=VENV, stroke_width=5)
        circle = Circle(radius=5 * u_, color=VENV, stroke_width=4).move_to(origin)
        circle.rotate(np.arctan2(4, 3), about_point=origin)           # start the sweep on the radius
        five = label("5", 26, VENV).move_to((origin + P(3, 4)) / 2 + np.array([-0.32, 0.24, 0]))
        tip = origin + np.array([0.6, 0.8, 0]) * np.sqrt(50) * u_
        wrong = Arrow(origin, tip, buff=0, color=ERR, stroke_width=5, tip_length=0.22,
                      max_tip_length_to_length_ratio=0.1)
        wrong_lbl = label("√50 ≈ 7.07", 26, ERR).next_to(tip, RIGHT, buff=0.18)

        true_row = VGroup(label("docstring", 20, S.GREY), mono("sqrt(x^2 + y^2)", 22, VENV),
                          label("= √25 = 5", 26, VENV))
        bug_row = VGroup(label("line 44", 20, S.GREY), mono("math.sqrt(2 * z)", 22, ERR),
                         label("= √50 ≈ 7.07", 26, ERR))
        for row in (true_row, bug_row):
            row[1:].arrange(RIGHT, buff=0.2)
            row.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        rows = VGroup(true_row, bug_row).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        rows.move_to([3.55, 0.4, 0])
        no_crash = label("no crash · just wrong", 26, S.GREY).next_to(rows, DOWN, buff=0.6).align_to(rows, LEFT)

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(chain, strip, xt, r, u)), run_time=0.7)
            self.remove(chain, strip, xt, r, u)
            self.play(Create(axes), run_time=0.8)
            vo.wait_until("the point 3 comma 4")
            self.play(Create(proj), FadeIn(three), FadeIn(four), run_time=0.6)
            self.play(FadeIn(pt, scale=1.5), FadeIn(pt_lbl, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("Its true distance")
            self.play(Create(radius), run_time=0.7)
            vo.wait_until("is 5,")
            self.play(FadeIn(five, shift=UP * 0.1), FadeIn(true_row, shift=LEFT * 0.2), run_time=0.6)
            vo.wait_until("the radius of this circle")
            self.play(Create(circle), Rotate(radius, 2 * PI, about_point=origin), run_time=1.6)
            vo.wait_until("The buggy line returns")
            self.play(FadeIn(bug_row, shift=LEFT * 0.2), run_time=0.6)
            self.bring_to_back(wrong)
            self.play(GrowArrow(wrong), run_time=1.0)
            vo.wait_until("about 7.07")
            self.play(FadeIn(wrong_lbl, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("it overshoots the circle")
            self.play(Indicate(wrong, color=ERR, scale_factor=1.06), Flash(tip, color=ERR, flash_radius=0.3),
                      run_time=0.8)
            vo.wait_until("No crash")
            self.play(FadeIn(no_crash, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("only a wrong number")
            self.play(Indicate(bug_row[2], color=ERR, scale_factor=1.1), run_time=0.8)

        # ========================================================== 2. the test that knew
        panel = code(TEST_API, 31, 38)
        panel.move_to([0, -1.25, 0])
        query = code_span(panel.code, 33 - 31, "?x=3&y=4")
        q_line = under(query, ROUTE, stroke=3)
        expect = code_span(panel.code, 38 - 31, 'data["distance"] == 5.0')
        bar38 = line_bar(panel.code, 38 - 31, VENV, 0.22)
        spec = grey_chip("an executable specification", size=22)
        spec.move_to([-3.2, 2.0, 0])
        ray = VGroup(wrong, wrong_lbl)
        hit_x = 3.6
        top = panel.get_top()[1]

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(axes, point, radius, circle, five, rows, no_crash)),
                      run_time=0.7)
            self.remove(axes, point, radius, circle, five, rows, no_crash)
            # the wrong answer waits above, pointing down at where the panel will be
            self.play(wrong.animate.rotate(-PI / 2 - np.arctan2(4, 3)).scale(0.5).move_to([hit_x, top + 1.25, 0]),
                      wrong_lbl.animate.move_to([hit_x + 1.4, top + 1.25, 0]), run_time=0.9)
            vo.wait_until("already knew the right answer")
            self.play(FadeIn(panel, shift=UP * 0.2), run_time=0.8)
            vo.wait_until("It asks the app")
            self.play(Create(q_line), Indicate(query, color=ROUTE, scale_factor=1.08), run_time=0.8)
            vo.wait_until("insists on exactly 5.0")
            self.play(FadeIn(bar38), expect.animate.set_color(VENV), run_time=0.6)
            self.play(Indicate(expect, color=VENV, scale_factor=1.06), run_time=0.7)
            vo.wait_until("A test is an executable specification")
            self.play(FadeIn(spec, shift=DOWN * 0.15), run_time=0.6)
            vo.wait_until("would have said no")
            hit = [hit_x, top + 0.05 + wrong.height / 2, 0]
            self.play(Succession(wrong.animate(run_time=0.45, rate_func=rush_into).move_to(hit),
                                 wrong.animate(run_time=0.55, rate_func=rush_from).move_to(
                                     [hit_x, top + 1.25, 0])),
                      Indicate(bar38, color=VENV, scale_factor=1.0), run_time=1.0)
            self.play(VGroup(wrong, wrong_lbl).animate.set_opacity(0.45), run_time=0.5)

        # ========================================================== 3. two suspects
        card_bg = RoundedRectangle(width=9.0, height=3.5, corner_radius=0.18, stroke_color=S.GREY,
                                   stroke_width=2.5).set_fill(S.GREY_DARKER, 1).move_to([0, 0.55, 0])
        heading = label("two suspects", 24, S.GREY).move_to([0, 1.95, 0])
        code_chip = chip("the code", IMAGE, size=28)
        test_chip = chip("the test", VENV, size=28)
        code_chip.move_to([-2.3, 0.95, 0])
        test_chip.move_to([2.3, 0.95, 0])
        stamp = chip("fix this", TURN, size=24, text_color=TURN)
        stamp.move_to([-2.3, -0.45, 0])
        stamp_arrow = arrow(stamp, code_chip, TURN, stroke=4)
        rewrite = dashed_chip("rewrite the test to match the bug", size=20)
        rewrite.move_to([2.3, -0.45, 0])
        no = strike(rewrite, ERR, stroke=5)
        rule = label("slide 28: when a test fails, fix the code", 24, S.GREY).next_to(card_bg, DOWN, buff=0.35)
        diary = label("a diary of the bug", 20, ERR).next_to(rewrite, DOWN, buff=0.15)

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(spec), FadeIn(card_bg), run_time=0.5)
            self.remove(spec)
            vo.wait_until("two suspects")
            self.play(FadeIn(heading),
                      FadeTransform(VGroup(panel, bar38, q_line), test_chip),
                      FadeTransform(VGroup(wrong, wrong_lbl), code_chip), run_time=1.1)
            vo.wait_until("the code and the test")
            self.play(Indicate(code_chip, color=IMAGE, scale_factor=1.12), run_time=0.6)
            self.play(Indicate(test_chip, color=VENV, scale_factor=1.12), run_time=0.6)
            vo.wait_until("first believe the test")
            self.play(test_chip.box.animate.set_stroke(width=5), run_time=0.5)
            vo.wait_until("and fix the code")
            self.play(FadeIn(stamp, scale=1.4), GrowArrow(stamp_arrow), run_time=0.6)
            self.play(Indicate(code_chip, color=TURN, scale_factor=1.12), FadeIn(rule, shift=UP * 0.15),
                      run_time=0.8)
            vo.wait_until("Rewriting the test")
            self.play(FadeIn(rewrite, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("into a diary")
            self.play(Create(no), FadeIn(diary, shift=UP * 0.1), run_time=0.6)

        # ========================================================== 4. normal, edge, invalid
        trays = [bin_tray(n, x) for n, x in (("normal", -4.3), ("edge", 0.0), ("invalid", 4.3))]
        norm_chip = grey_chip("power(2, 3)", size=22, mono_font=True)
        edge_chips = VGroup(*[grey_chip(s, size=22, mono_font=True) for s in ("0", "inf", "nan")])
        edge_chips.arrange(RIGHT, buff=0.22)
        norm_chip.move_to(trays[0].spot)
        edge_chips.move_to(trays[1].spot)
        drops = [norm_chip, *edge_chips]
        for c in drops:
            c.shift(UP * 2.6)
        panel2 = code(TEST_UTILS, 69, 76)
        panel2.move_to([0, 0.35, 0]).align_to(trays[2].shape, RIGHT)
        raises = code_span(panel2.code, 71 - 69, "pytest.raises(TypeError)")
        bar71 = line_bar(panel2.code, 71 - 69, TURN, 0.2)
        call = code_span(panel2.code, 72 - 69, 'power("3", 4)')
        inv_chip = grey_chip('power("3", 4)', size=22, mono_font=True).move_to(call)
        terr = code_span(panel2.code, 71 - 69, "TypeError")
        old = VGroup(card_bg, heading, code_chip, test_chip, stamp, stamp_arrow, rewrite, no, rule, diary)

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(old), run_time=0.6)
            self.remove(old)
            vo.wait_until("three trays")
            self.play(LaggedStart(*[FadeIn(t, shift=RIGHT * 1.5) for t in trays], lag_ratio=0.25),
                      run_time=1.2)
            vo.wait_until("normal, edge, and invalid")
            for t in trays:
                self.play(Indicate(t.text, color=INK, scale_factor=1.12), run_time=0.4)
            vo.wait_until("2 to the power 3")
            self.play(FadeIn(norm_chip), run_time=0.3)
            self.play(norm_chip.animate(rate_func=rush_into).shift(DOWN * 2.6), run_time=0.6)
            vo.wait_until("zero exponents")
            for c, anchor in zip(edge_chips, ("zero exponents", "infinity", "not a number")):
                vo.wait_until(anchor)
                self.play(FadeIn(c), run_time=0.2)
                self.play(c.animate(rate_func=rush_into).shift(DOWN * 2.6), run_time=0.5)
            vo.wait_until("And for invalid input")
            self.play(FadeIn(panel2, shift=UP * 0.2), run_time=0.8)
            vo.wait_until("pytest dot raises")
            self.play(FadeIn(bar71), Indicate(raises, color=TURN, scale_factor=1.05), run_time=0.8)
            vo.wait_until("power on a string")
            self.play(FadeIn(inv_chip, scale=1.15), run_time=0.4)
            self.play(inv_chip.animate(rate_func=smooth).move_to(trays[2].spot), run_time=0.9)
            vo.wait_until("raises a type error")
            self.play(Indicate(terr, color=VENV, scale_factor=1.12), run_time=0.8)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
