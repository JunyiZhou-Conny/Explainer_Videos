"""S02 · The app: cli.py (concept scene: no README tracker).

Beats (script.md "## S02", one voiceover block each):
 0. CODE(cli.py: 5-9) at left; a GREY chip with where the file lives on GitHub. Lines 5-6 get a
    GREY bracket "comes with Python"; `art` and `googletrans` turn PINK and lines 8-9 get a PINK
    bracket "where from?".
 1. main(): CODE(12-15): line 14 -> the AC215 banner (expected/10-run-default.txt lines 4-8) at
    right; line 15 -> the Arguments line (line 12) under both. CODE(17-23): line 23 -> `Input: ...`
    (line 14), then lines 19-21 get the GREY "-f" tag (the narration's order). Thin GREY arrows
    link code lines to outputs; each panel's outputs leave with it (17-23 is 9.9 wide at 22 pt).
 2. V6 starts in the top half (code panels sit in the bottom half from here on): `argv` -> a GREY
    Namespace table; CODE(45-51) then CODE(59-70) as two panels side by side, 59-64 + 65-70
    (12 lines at 22 pt don't fit the bottom half); each default lights its row (`file`, whose
    default sits in lines 52-58, lights as the panels scroll past it).
 3. CODE(72): the table feeds an event loop "asyncio.run(main(args))"; CODE(25-31), lines 25, 27.
 4. A BLUE VM box holds the loop; a PINK "HTTPS GET" reaches the BLUE cloud
    translate.googleapis.com ("unofficial · no API key"); "JSON" comes back; CODE(39) flashes and
    `Output: Adoro il formaggio` (expected line 15, tag expected output) appears under the VM.
 5. CODE(25) with raise_exception=True boxed YELLOW; two mini pipelines (tag illustration): the
    library default hands your input back ("looks fine, is wrong"); with True, the RED answer
    becomes an exception box that rises up the pipeline.
 6. CODE(32-37) alone, full width: RED bracket "catches every error"; `from error` underlined PINK.
 7. The whole V6 loop in one picture; `art` and `googletrans` drop below the VM with PINK "?"
    tags. Fade out to an empty frame.

Every output line comes from capture("10-run-default", "expected"); every code line from
excerpt("cli.py", a, b).
"""

import numpy as np
from manim import *

from explainer import style as S
from explainer.devops import (INK, MONO, OUTPUT, box, chip, code_panel, code_span, cloud, label,
                              line_bar, machine_box, mono, mono_line, tag)
from explainer.scene import VoiceScene

from common import (CLOUD, ERR, LOOKUP, NARRATION, TURN, capture, excerpt, expected_tag,
                    illustration_tag)

SAY = NARRATION["S02"]

RUN = capture("10-run-default", "expected")       # pick index = file line - 1
BANNER = RUN.pick((3, 7))                          # file lines 4-8: the AC215 banner
ARGS_LINE = RUN.pick(11)[0]                        # file line 12: Arguments: Namespace(...)
INPUT_LINE = RUN.pick(13)[0]                       # file line 14: Input: I love cheese
OUTPUT_LINE = RUN.pick(14)[0]                      # file line 15: Output: Adoro il formaggio

X0 = -6.3            # left edge of the code panels
CODE_BOTTOM = -3.4   # bottom edge of the panels in the bottom half
OUT_PT = 20          # program output (the full Arguments line only fits at 20 pt)


# ------------------------------------------------------------------ small helpers
def panel(a: int, b: int, size: float = 22) -> VGroup:
    """CODE(cli.py: a-b): a real excerpt, header "cli.py · lines a-b"."""
    p = code_panel(excerpt("cli.py", a, b), "cli.py", first_line=a, font_size=size)
    p.first = a
    return p


def place(m, left=None, top=None, bottom=None, cy=None, cx=None):
    """Move m so its left/top/bottom edge or centre sits at the given coordinate."""
    if left is not None:
        m.shift(RIGHT * (left - m.get_left()[0]))
    if cx is not None:
        m.set_x(cx)
    if top is not None:
        m.shift(UP * (top - m.get_top()[1]))
    if bottom is not None:
        m.shift(UP * (bottom - m.get_bottom()[1]))
    if cy is not None:
        m.set_y(cy)
    return m


def cl(p, n: int):
    """The glyphs of file line n in panel p."""
    return p.code.code_lines[n - p.first]


def bar(p, n: int, color=TURN, opacity=0.16):
    return line_bar(p.code, n - p.first, color, opacity)


def span(p, n: int, sub: str, occurrence: int = 0):
    return code_span(p.code, n - p.first, sub, occurrence)


def bracket(top: float, bottom: float, x: float, color, opens=LEFT, tick: float = 0.14) -> VMobject:
    """A thin square bracket from top to bottom at x; its ticks point toward `opens`."""
    d = tick if np.allclose(opens, RIGHT) else -tick
    return VMobject().set_points_as_corners(
        [[x + d, top, 0], [x, top, 0], [x, bottom, 0], [x + d, bottom, 0]]).set_stroke(color, 3)


def lines_span(p, a: int, b: int):
    """(top, bottom) y of file lines a..b in panel p (padding included)."""
    g = VGroup(*[cl(p, n) for n in range(a, b + 1) if len(cl(p, n))])
    return g.get_top()[1] + 0.07, g.get_bottom()[1] - 0.07


def thin_arrow(start, end, color=S.GREY, width=2.5):
    return Arrow(start, end, buff=0.06, color=color, stroke_width=width, tip_length=0.16,
                 max_tip_length_to_length_ratio=0.35, max_stroke_width_to_length_ratio=20)


def out_line(s: str, size: float = OUT_PT) -> VGroup:
    return mono_line(s, size, OUTPUT)


def boxed_tag(s: str, color=S.GREY, size: float = 22) -> VGroup:
    """A tag whose text may run over two rows (opaque dark fill, rounded)."""
    t = label(s, size, color, line_spacing=0.9)
    b = RoundedRectangle(width=t.width + 0.36, height=t.height + 0.24, corner_radius=0.14,
                         stroke_color=color, stroke_width=2).set_fill(S.BG, 0.92)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def loop_glyph(radius: float = 0.6, color=INK) -> VGroup:
    """A circular arrow: the event loop."""
    arc = Arc(radius=radius, start_angle=PI / 2 + 0.45, angle=TAU - 0.9, stroke_width=4, color=color)
    arc.add_tip(tip_length=0.2, tip_width=0.2)
    return VGroup(arc)


def namespace_table(size: float = 22, width: float = 4.6, row_h: float = 0.46) -> VGroup:
    """The parsed arguments as a four-row GREY table; rows start dim (.light(i) lights one)."""
    items = [("text", "'I love cheese'"), ("file", "''"), ("src", "'en'"), ("dest", "'it'")]
    rows = VGroup()
    for k, v in items:
        r = Rectangle(width=width, height=row_h, stroke_color=S.GREY, stroke_width=2) \
            .set_fill(S.GREY_DARKER, 1)
        t = mono_line(f"{k:<4} = {v}", size, INK)
        t.move_to(r).align_to(r, LEFT).shift(RIGHT * 0.22)
        t.glyphs.set_opacity(0.3)
        rows.add(VGroup(r, t))
    rows.arrange(DOWN, buff=0)
    head = mono("Namespace", size, S.GREY).next_to(rows, UP, buff=0.12).align_to(rows, LEFT)
    g = VGroup(head, rows)
    g.rows, g.head = rows, head
    return g


def light_row(scene, table, i: int, run_time: float = 0.5):
    """Light row i (its text goes to full opacity) under a brief YELLOW wash; also used to point
    at a row that is already lit. The wash is translucent, so the text stays readable (an
    Indicate(color=...) would turn the opaque row fill solid YELLOW over the text)."""
    r, t = table.rows[i]
    flash = r.copy().set_fill(TURN, 0.28).set_stroke(TURN, 3)
    scene.play(t.glyphs.animate.set_opacity(1), FadeIn(flash), run_time=run_time * 0.5)
    scene.play(FadeOut(flash), run_time=run_time * 0.5)


def scroll(scene, old, new, *extra, dist: float = 0.35, run_time: float = 0.8):
    """Swap one code panel for the next, as if scrolling down the file: the old one leaves upward
    (with any `extra` animations), then the new one arrives from below. No cross-fade overlap."""
    scene.play(FadeOut(old, shift=UP * dist), *extra, run_time=run_time * 0.45)
    scene.play(FadeIn(new, shift=UP * dist), run_time=run_time * 0.55)


# ------------------------------------------------------------------ the scene
class TheApp(VoiceScene):
    def construct(self):
        assert len(SAY) == 8, f"S02 has {len(SAY)} SAY lines; this scene animates 8"

        # ========================================================== 0. the imports
        p0 = panel(5, 9, size=28)
        place(p0, left=X0, cy=-0.5)
        gh = chip("github.com/dlops-io/simple-translate · cli.py", S.GREY, size=22, font=MONO)
        place(gh, left=X0, top=2.7)
        xb = p0.get_right()[0] + 0.28
        t56, b56 = lines_span(p0, 5, 6)
        t89, b89 = lines_span(p0, 8, 9)
        br56 = bracket(t56, b56, xb, S.GREY)
        br89 = bracket(t89, b89, xb, LOOKUP)
        tag56 = tag("comes with Python", S.GREY).next_to(br56, RIGHT, buff=0.2)
        tag89 = tag("where from?", LOOKUP).next_to(br89, RIGHT, buff=0.2)
        bar56 = VGroup(bar(p0, 5, S.GREY, 0.14), bar(p0, 6, S.GREY, 0.14))
        bar89 = VGroup(bar(p0, 8, LOOKUP, 0.14), bar(p0, 9, LOOKUP, 0.14))
        w_art, w_gt = span(p0, 8, "art"), span(p0, 9, "googletrans")
        w_argparse, w_asyncio = span(p0, 5, "argparse"), span(p0, 6, "asyncio")
        ul_art, ul_gt = [Line(w.get_corner(DL) + DOWN * 0.07, w.get_corner(DR) + DOWN * 0.07, color=LOOKUP,
                              stroke_width=4) for w in (w_art, w_gt)]

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(p0, shift=UP * 0.2), run_time=1.0)
            vo.wait_until("Open cli.py")
            self.play(FadeIn(gh, shift=DOWN * 0.15), run_time=0.7)
            self.play(Circumscribe(gh, color=TURN, buff=0.06, run_time=1.2))
            vo.wait_until("clone it onto")
            self.play(Indicate(gh.text, color=INK, scale_factor=1.05), run_time=0.9)
            vo.wait_until("The first two imports")
            self.play(FadeIn(bar56), run_time=0.5)
            vo.wait_until("argparse and")
            self.play(Indicate(w_argparse, color=INK, scale_factor=1.15), run_time=0.6)
            self.play(Indicate(w_asyncio, color=INK, scale_factor=1.15), run_time=0.6)
            vo.wait_until("come with Python")
            self.play(Create(br56), FadeIn(tag56, shift=LEFT * 0.15), run_time=0.6)
            vo.wait_until("The next two")
            self.play(FadeIn(bar89), run_time=0.4)
            vo.wait_until("art and googletrans")
            self.play(w_art.animate.set_color(LOOKUP), Create(ul_art), run_time=0.4)
            self.play(w_gt.animate.set_color(LOOKUP), Create(ul_gt), run_time=0.4)
            vo.wait_until("They have to come")
            self.play(Create(br89), FadeIn(tag89, shift=LEFT * 0.15), run_time=0.6)
            vo.wait_until("This whole lecture")
            # each word pulses in place (one Indicate on the pair would scale them about their
            # common centre and push them onto their neighbours)
            self.play(*[Indicate(w, color=LOOKUP, scale_factor=1.1) for w in (w_art, w_gt)],
                      Wiggle(tag89, scale_value=1.1), run_time=1.2)

        # ========================================================== 1. main(): what it prints
        pA = panel(12, 15)
        place(pA, left=X0, top=2.75)
        banner = VGroup(*[out_line(s) for s in BANNER])
        for i, row in enumerate(banner):
            row.shift(DOWN * i * 0.367 - row.strut.get_corner(UL))
        place(banner, left=0.95, cy=pA.code.get_center()[1])
        y14 = cl(pA, 14).get_center()[1]
        a14 = thin_arrow([cl(pA, 14).get_right()[0] + 0.12, y14, 0], [banner.get_left()[0] - 0.12, y14, 0])
        args_line = out_line(ARGS_LINE)
        place(args_line, cx=0, cy=-0.75)
        x15 = cl(pA, 15).get_center()[0]
        a15 = thin_arrow([x15, pA.get_bottom()[1] - 0.02, 0], [x15, args_line.get_top()[1] + 0.04, 0])
        bar14, bar15 = bar(pA, 14), bar(pA, 15)

        pB = panel(17, 23)
        place(pB, left=X0, top=2.75)
        input_line = out_line(INPUT_LINE, 22)
        x23 = cl(pB, 23).get_center()[0]
        place(input_line, cx=x23, top=pB.get_bottom()[1] - 0.55)
        a23 = thin_arrow([x23, pB.get_bottom()[1] - 0.02, 0], [x23, input_line.get_top()[1] + 0.04, 0])
        bar23 = bar(pB, 23)
        t19, b21 = lines_span(pB, 19, 21)
        br_f = bracket(t19, b21, pB.get_right()[0] + 0.22, S.GREY)
        tag_f = boxed_tag("-f: read the text\nfrom a file").next_to(br_f, RIGHT, buff=0.2)
        bars_f = VGroup(*[bar(pB, n, S.GREY, 0.12) for n in (19, 20, 21)])
        bar21 = bar(pB, 21)

        with self.voiceover(SAY[1]) as vo:
            scroll(self, VGroup(p0, bar56, bar89, ul_art, ul_gt, gh, br56, br89, tag56, tag89), pA, run_time=0.9)
            self.play(Indicate(span(pA, 12, "main"), color=INK, scale_factor=1.2), run_time=0.7)
            vo.wait_until("a banner")
            self.play(FadeIn(bar14), GrowArrow(a14), run_time=0.5)
            self.play(LaggedStart(*[Write(r) for r in banner], lag_ratio=0.25), run_time=1.3)
            vo.wait_until("then the parsed")
            self.play(FadeOut(bar14), FadeIn(bar15), GrowArrow(a15), run_time=0.5)
            self.play(FadeIn(args_line, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("then the text")
            scroll(self, VGroup(pA, bar15), pB, FadeOut(VGroup(banner, a14, args_line, a15)), run_time=0.8)
            self.play(FadeIn(bar23), GrowArrow(a23), run_time=0.4)
            self.play(FadeIn(input_line, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("If you pass")
            self.play(FadeIn(bars_f), Create(br_f), FadeIn(tag_f, shift=LEFT * 0.15), run_time=0.7)
            vo.wait_until("the text comes from")
            self.play(FadeOut(bars_f), FadeIn(bar21), run_time=0.5)
            self.play(Indicate(span(pB, 21, "text"), color=INK, scale_factor=1.2),
                      Indicate(span(pB, 23, "text", 0), color=INK, scale_factor=1.2), run_time=0.9)

        # ========================================================== 2. argparse defaults -> Namespace
        p45 = panel(45, 51)
        place(p45, left=X0, bottom=CODE_BOTTOM)
        p59, p65 = panel(59, 64), panel(65, 70)
        VGroup(p59, p65).arrange(RIGHT, buff=0.3, aligned_edge=DOWN)
        place(VGroup(p59, p65), left=X0, bottom=CODE_BOTTOM)
        argv = chip("argv", S.GREY, size=24, font=MONO)
        table = namespace_table()
        place(argv, left=X0, cy=1.6)
        place(table, left=-3.75, top=3.2)
        argv.set_y(table.rows.get_center()[1])
        a_argv = thin_arrow(argv.get_right() + RIGHT * 0.05, [table.rows.get_left()[0] - 0.05, argv.get_y(), 0],
                            color=S.GREY, width=3)
        no_opts = label("no options", 22, S.GREY).next_to(argv, DOWN, buff=0.2)
        bar49, bar62, bar68 = bar(p45, 49), bar(p59, 62), bar(p65, 68)

        with self.voiceover(SAY[2]) as vo:
            scroll(self, VGroup(pB, bar23, bar21), p45, FadeOut(VGroup(input_line, a23, br_f, tag_f)),
                   dist=0.5, run_time=0.9)
            vo.wait_until("defines four options")
            self.play(FadeIn(argv, shift=RIGHT * 0.2), run_time=0.5)
            self.play(GrowArrow(a_argv), FadeIn(table, shift=RIGHT * 0.2), run_time=0.8)
            vo.wait_until("the text I love")
            self.play(FadeIn(bar49), run_time=0.3)
            light_row(self, table, 0)
            vo.wait_until("source language")
            # scrolling past lines 52-58 (the -f option, default "") quietly lights the file row on
            # the way; it isn't narrated, so it gets no YELLOW wash (that belongs to src now)
            scroll(self, VGroup(p45, bar49), VGroup(p59, p65), table.rows[1][1].glyphs.animate.set_opacity(1),
                   run_time=0.6)
            self.play(FadeIn(bar62), run_time=0.3)
            light_row(self, table, 2, run_time=0.5)
            vo.wait_until("destination Italian")
            self.play(FadeIn(bar68), run_time=0.3)
            light_row(self, table, 3)
            vo.wait_until("So running")
            self.play(FadeIn(no_opts, shift=UP * 0.1), run_time=0.5)
            self.play(ShowPassingFlash(a_argv.copy().set_stroke(TURN, 6), time_width=0.6), run_time=0.8)
            vo.wait_until("translates I love")
            light_row(self, table, 0, run_time=0.8)
            vo.wait_until("into Italian")
            light_row(self, table, 3, run_time=0.8)

        # ========================================================== 3. asyncio.run -> the event loop
        p72 = panel(72, 72)
        place(p72, left=X0, cy=-1.75)
        bar72 = bar(p72, 72)
        loop = loop_glyph(0.6)
        loop.move_to([3.3, table.rows.get_center()[1] + 0.3, 0])
        main_t = mono("main", 22, INK).move_to(loop)
        loop_l1 = label("event loop", 24, INK).next_to(loop, DOWN, buff=0.18)
        loop_l2 = mono("asyncio.run(main(args))", 20, S.GREY).next_to(loop_l1, DOWN, buff=0.1)
        a_ns = thin_arrow([table.rows.get_right()[0] + 0.05, loop.get_y(), 0],
                          [loop.get_left()[0] - 0.08, loop.get_y(), 0], color=S.GREY, width=3)
        p25 = panel(25, 31)
        place(p25, left=X0, bottom=CODE_BOTTOM)
        bar25, bar27 = bar(p25, 25), bar(p25, 27)

        with self.voiceover(SAY[3]) as vo:
            scroll(self, VGroup(p59, p65, bar62, bar68), p72, FadeOut(no_opts), dist=0.5, run_time=0.8)
            self.play(FadeIn(bar72), run_time=0.3)
            vo.wait_until("starts an event loop")
            self.play(GrowArrow(a_ns), Create(loop[0]), run_time=0.8)
            self.play(FadeIn(loop_l1, shift=UP * 0.1), FadeIn(loop_l2, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("runs main")
            self.play(FadeIn(main_t, scale=0.6), Rotate(loop[0], -TAU / 3, about_point=loop.get_center()),
                      run_time=0.8)
            vo.wait_until("because googletrans")
            self.play(Rotate(loop[0], -TAU / 2, about_point=main_t.get_center()), run_time=1.6,
                      rate_func=smooth)
            vo.wait_until("Inside main")
            scroll(self, VGroup(p72, bar72), p25, dist=0.5, run_time=0.7)
            vo.wait_until("a Translator")
            self.play(FadeIn(bar25), Indicate(span(p25, 25, "Translator"), color=INK, scale_factor=1.15),
                      run_time=0.8)
            vo.wait_until("one awaited call")
            self.play(FadeOut(bar25), FadeIn(bar27), run_time=0.4)
            self.play(Indicate(span(p25, 27, "await"), color=INK, scale_factor=1.2), run_time=0.8)

        # ========================================================== 4. one HTTPS request
        vm = machine_box("VM", "ac215-l01", width=4.2, height=2.95, color=CLOUD)
        place(vm, left=X0, top=3.35)
        loop_in = VGroup(loop_glyph(0.5), mono("main", 22, INK))
        loop_in[1].move_to(loop_in[0])
        loop_in.move_to(vm.body.get_center() + UP * 0.25)
        lbl_in = label("event loop", 24, INK).next_to(loop_in, DOWN, buff=0.15)
        gcloud = cloud(2.7, CLOUD).move_to([4.2, 2.05, 0])
        host = mono("translate.googleapis.com", 20, CLOUD).next_to(gcloud, DOWN, buff=0.2)
        # the answer leaves from the cloud's lower lobe, well clear of the host name under it
        y_req, y_ret = 2.5, gcloud.get_bottom()[1] + 0.22
        x_vm, x_cl = vm.get_right()[0] + 0.05, gcloud.get_left()[0] + 0.05
        req = Arrow([x_vm, y_req, 0], [x_cl, y_req, 0], buff=0, color=LOOKUP, stroke_width=5,
                    tip_length=0.22, max_tip_length_to_length_ratio=0.1)
        req_l = mono("HTTPS GET", 22, LOOKUP).next_to(req, UP, buff=0.12)
        ret = Arrow([x_cl, y_ret, 0], [x_vm, y_ret, 0], buff=0, color=LOOKUP, stroke_width=3,
                    tip_length=0.2, max_tip_length_to_length_ratio=0.1)
        # once the code panel has gone, the picture drops to the middle of the frame (DROP)
        DROP = 0.8
        picture = VGroup(vm, loop_in, lbl_in, gcloud, host, req, req_l)
        ret.shift(DOWN * DROP)
        y_ret -= DROP
        unoff = tag("unofficial · no API key", S.GREY).next_to(gcloud, UP, buff=0.15).shift(DOWN * DROP)
        json = chip("JSON", S.GREY, size=22, font=MONO).move_to([x_cl - 0.65, y_ret + 0.38, 0])
        output_line = out_line(OUTPUT_LINE, 22)
        place(output_line, left=X0 + 0.1, top=vm.get_bottom()[1] - DROP - 0.3)
        exp = expected_tag().next_to(output_line, RIGHT, buff=0.3)
        p39 = panel(39, 39)
        place(p39, left=X0, cy=output_line.get_center()[1] - 1.5)
        bar39 = bar(p39, 39)
        x39 = output_line.get_center()[0] + 1.0
        a39 = thin_arrow([x39, p39.code.get_top()[1] + 0.02, 0], [x39, output_line.get_bottom()[1] - 0.04, 0])

        with self.voiceover(SAY[4]) as vo:
            # the rest clears first (so the VM box never fades in over the table), then the loop and
            # its label carry over into the VM, in time for "a single HTTPS request"
            self.play(FadeOut(VGroup(argv, a_argv, table, a_ns, loop_l2)), run_time=0.4)
            self.play(ReplacementTransform(VGroup(loop, main_t), loop_in), ReplacementTransform(loop_l1, lbl_in),
                      FadeIn(vm), run_time=0.8)
            vo.wait_until("a single HTTPS")
            self.play(GrowArrow(req), FadeIn(req_l, shift=UP * 0.1), run_time=1.0)
            vo.wait_until("to translate dot")
            self.play(FadeIn(gcloud, scale=0.85), run_time=0.6)
            self.play(Write(host), run_time=1.0)
            vo.wait_until("It's Google's unofficial")
            self.play(FadeOut(VGroup(p25, bar27), shift=DOWN * 0.3), run_time=0.5)
            self.play(picture.animate.shift(DOWN * DROP), FadeIn(unoff, shift=DOWN * (DROP + 0.1)), run_time=0.8)
            vo.wait_until("no API key")
            # pulse the words, not the whole tag: Indicate(color=...) on the tag would paint its
            # opaque fill the text's colour
            self.play(Indicate(unoff.text, color=INK, scale_factor=1.08), run_time=0.8)
            vo.wait_until("no promises")
            self.play(Wiggle(gcloud, scale_value=1.05, rotation_angle=0.03 * TAU), run_time=0.9)
            vo.wait_until("A little JSON")
            self.play(GrowArrow(ret), FadeIn(json, scale=0.6), run_time=0.6)
            self.play(json.animate.move_to([x_vm + 0.75, y_ret + 0.38, 0]), run_time=1.0)
            vo.wait_until("and line 39")
            self.play(FadeIn(p39, shift=UP * 0.2), run_time=0.5)
            self.play(FadeIn(bar39), Flash(p39.code.get_right() + LEFT * 0.3, color=TURN, line_length=0.18,
                                            num_lines=10, flash_radius=0.35), run_time=0.6)
            vo.wait_until("prints the translation")
            self.play(GrowArrow(a39), FadeIn(output_line, shift=UP * 0.1), run_time=0.6)
            self.play(FadeIn(exp, shift=LEFT * 0.1), run_time=0.4)

        # ========================================================== 5. raise_exception=True
        p25b = panel(25, 25)
        place(p25b, cx=0, top=3.45)
        rx = span(p25b, 25, "raise_exception=True")
        rx_box = SurroundingRectangle(rx, color=TURN, buff=0.07, stroke_width=3, corner_radius=0.05)
        CX = (-3.3, 3.3)
        titles = VGroup(label("library default (False)", 26, S.GREY),
                        mono("raise_exception=True", 24, INK))
        gts, gcs, reqs = VGroup(), VGroup(), VGroup()
        for cx, t in zip(CX, titles):
            t.move_to([cx, 1.72, 0])
            g = chip("googletrans", S.GREY, size=26, font=MONO).move_to([cx, -0.45, 0])
            c = cloud(2.3, CLOUD).move_to([cx, -2.3, 0])
            c_l = label("Google", 24, CLOUD).move_to(c).shift(DOWN * 0.1)
            r = Arrow(g.get_bottom() + LEFT * 0.45, [cx - 0.45, c.get_top()[1] + 0.02, 0], buff=0.04,
                      color=LOOKUP, stroke_width=4, tip_length=0.18, max_tip_length_to_length_ratio=0.3)
            gts.add(g)
            gcs.add(VGroup(c, c_l))
            reqs.add(r)
        divider = DashedLine([0, 1.95, 0], [0, -2.95, 0], color=S.GREY_DARK, dash_length=0.12)
        illus = illustration_tag().move_to([0, -3.28, 0])

        def answer(i):
            g, c = gts[i], gcs[i][0]
            return Arrow([CX[i] + 0.45, c.get_top()[1] + 0.02, 0], g.get_bottom() + RIGHT * 0.45, buff=0.04,
                         color=ERR, stroke_width=4, tip_length=0.18, max_tip_length_to_length_ratio=0.3)

        def rise(i, color, top):
            return Arrow(gts[i].get_top(), [CX[i], top, 0], buff=0.06, color=color, stroke_width=4,
                         tip_length=0.18, max_tip_length_to_length_ratio=0.3)

        Y_END = 1.05
        ans_l = answer(0)
        err_l = label("error", 24, ERR).next_to(ans_l, RIGHT, buff=0.15)
        end_txt = VGroup(mono("Output:", 24, INK), label("(your input, unchanged)", 24, INK)) \
            .arrange(RIGHT, buff=0.15)
        end_box = box(end_txt.width + 0.4, end_txt.height + 0.3, S.GREY, fill_opacity=0.12)
        end_box.move_to(end_txt)
        end = VGroup(end_box, end_txt).move_to([CX[0], Y_END, 0])
        up_l = rise(0, S.GREY, end.get_bottom()[1])
        wrong = tag("looks fine, is wrong", ERR)
        place(wrong, cy=(end.get_bottom()[1] + gts[0].get_top()[1]) / 2)
        wrong.shift(RIGHT * (CX[0] - 0.2 - wrong.get_right()[0]))
        ans_r = answer(1)
        exc = boxed_tag("an error you can read", ERR, 24)
        exc.box.set_fill(ERR, 0.18)
        exc.move_to(ans_r)
        exc_end = [CX[1], Y_END, 0]
        up_r = rise(1, ERR, Y_END - exc.height / 2)

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(vm, loop_in, lbl_in, req, req_l, gcloud, host, unoff, ret, json,
                                     output_line, exp, p39, bar39, a39)), run_time=0.7)
            self.play(FadeIn(p25b, shift=DOWN * 0.2), run_time=0.6)
            vo.wait_until("raise exception equals")
            self.play(Create(rx_box), run_time=0.6)
            self.play(Indicate(rx, color=TURN, scale_factor=1.08), run_time=0.8)
            # the two pipelines arrive just before "Without it", so the requests are out by the
            # time the narration reaches "when Google answers"
            self.wait(max(0.0, vo.time_until("Without it") - 0.6))
            self.play(LaggedStart(FadeIn(titles), FadeIn(gts), FadeIn(gcs), Create(divider), FadeIn(illus),
                                  lag_ratio=0.15), run_time=0.9)
            self.play(LaggedStart(*[GrowArrow(r) for r in reqs], lag_ratio=0.2), run_time=0.5)
            vo.wait_until("when Google answers")
            self.play(GrowArrow(ans_l), FadeIn(err_l, shift=UP * 0.1), run_time=0.7)
            vo.wait_until("googletrans hides it")
            self.play(err_l.animate.move_to(gts[0]).scale(0.4).set_opacity(0),
                      ans_l.animate.set_opacity(0.35), run_time=0.7)
            self.play(Indicate(gts[0], color=S.GREY, scale_factor=1.1), run_time=0.6)
            vo.wait_until("and hands your")
            self.play(GrowArrow(up_l), run_time=0.5)
            self.play(FadeIn(end, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("so nothing looks")
            self.play(FadeIn(wrong, scale=0.9), run_time=0.6)
            vo.wait_until("With it")
            self.play(GrowArrow(ans_r), run_time=0.5)
            # the RED answer passes up through googletrans and comes out the top as a small exception
            # box, which grows as it rises up the pipeline; its words fade in on the way. (Moving
            # the full box through the chip put its words on top of "googletrans".)
            exc.move_to(exc_end)
            seed = exc.box.copy().scale(0.25).next_to(gts[1], UP, buff=0.06)
            self.play(FadeTransform(ans_r.copy(), seed, stretch=True), run_time=0.5)
            self.play(Transform(seed, exc.box), GrowArrow(up_r),
                      FadeIn(exc.text, shift=UP * (exc_end[1] - seed.get_center()[1]), scale=0.25),
                      run_time=0.9, rate_func=rush_from)
            self.remove(seed, exc.text)
            self.add(exc)
            self.play(Indicate(exc, color=ERR, scale_factor=1.08), run_time=0.6)

        # ========================================================== 6. lines 32-37: catches everything
        p32 = panel(32, 37, size=21)
        place(p32, left=-5.65, cy=-0.35)
        t32, b37 = lines_span(p32, 32, 37)
        br32 = bracket(t32, b37, p32.get_left()[0] - 0.22, ERR, opens=RIGHT)
        catches = label("catches every error", 26, ERR)
        place(catches, left=-6.45, bottom=p32.get_top()[1] + 0.2)
        frm = span(p32, 37, "from error")
        frm_ul = Line(frm.get_corner(DL) + DOWN * 0.08, frm.get_corner(DR) + DOWN * 0.08, color=LOOKUP,
                      stroke_width=4)
        msg_bars = VGroup(*[bar(p32, n, S.GREY, 0.12) for n in (34, 35, 36)])

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(p25b, rx_box, titles, gts, gcs, reqs, divider, illus, ans_l, err_l,
                                     up_l, end, wrong, ans_r, exc, up_r)), run_time=0.7)
            self.play(FadeIn(p32, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("catch any error")
            self.play(Create(br32), FadeIn(catches, shift=RIGHT * 0.15), run_time=0.7)
            vo.wait_until("and wrap it")
            self.play(Create(frm_ul), Indicate(frm, color=LOOKUP, scale_factor=1.15), run_time=0.8)
            vo.wait_until("a friendlier message")
            self.play(FadeIn(msg_bars), run_time=0.6)
            vo.wait_until("Remember these lines")
            self.play(Indicate(VGroup(br32, catches), color=ERR, scale_factor=1.06), run_time=0.9)
            vo.wait_until("they'll fool us")
            self.play(Circumscribe(p32.code, color=TURN, buff=0.06), run_time=1.2)

        # ========================================================== 7. the whole loop, and two packages
        vm2 = machine_box("VM", "ac215-l01", width=4.2, height=3.95, color=CLOUD)
        place(vm2, left=X0, top=3.45)
        argv2 = chip("argv", S.GREY, size=22, font=MONO)
        ns2 = chip("Namespace", S.GREY, size=22, font=MONO)
        loop2 = VGroup(loop_glyph(0.42), mono("main", 20, INK))
        loop2[1].move_to(loop2[0])
        stack = VGroup(argv2, ns2, loop2).arrange(DOWN, buff=0.42)
        stack.move_to(vm2.body).shift(LEFT * 0.55)
        st_arrows = VGroup(*[thin_arrow(a.get_bottom(), b.get_top(), color=S.GREY, width=2.5)
                             for a, b in ((argv2, ns2), (ns2, loop2))])
        loop2_l = label("event loop", 22, INK).next_to(loop2, RIGHT, buff=0.2)
        gcloud2 = cloud(2.7, CLOUD).move_to([4.2, 1.75, 0])
        host2 = mono("translate.googleapis.com", 20, CLOUD).next_to(gcloud2, DOWN, buff=0.2)
        y_req2, y_ret2 = 2.2, gcloud2.get_bottom()[1] + 0.22
        x_vm2, x_cl2 = vm2.get_right()[0] + 0.05, gcloud2.get_left()[0] + 0.05
        req2 = Arrow([x_vm2, y_req2, 0], [x_cl2, y_req2, 0], buff=0, color=LOOKUP, stroke_width=5,
                     tip_length=0.22, max_tip_length_to_length_ratio=0.1)
        req2_l = mono("HTTPS GET", 22, LOOKUP).next_to(req2, UP, buff=0.12)
        ret2 = Arrow([x_cl2, y_ret2, 0], [x_vm2, y_ret2, 0], buff=0, color=LOOKUP, stroke_width=3,
                     tip_length=0.2, max_tip_length_to_length_ratio=0.1)
        json2 = chip("JSON", S.GREY, size=22, font=MONO).move_to([x_cl2 - 0.65, y_ret2 + 0.38, 0])
        out2 = out_line(OUTPUT_LINE, 22)
        place(out2, left=X0 + 0.1, top=vm2.get_bottom()[1] - 0.25)
        exp2 = expected_tag().next_to(out2, RIGHT, buff=0.3)
        pk = VGroup(chip("art", LOOKUP, size=26, font=MONO),
                    chip("googletrans", LOOKUP, size=26, font=MONO)).arrange(RIGHT, buff=0.6)
        pk.move_to([vm2.get_center()[0], -2.55, 0])
        qs = VGroup(*[tag("?", LOOKUP, size=24).next_to(c, UP, buff=0.14) for c in pk])

        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(p32, br32, catches, frm_ul, msg_bars)), run_time=0.6)
            self.play(FadeIn(vm2), LaggedStart(FadeIn(argv2), GrowArrow(st_arrows[0]), FadeIn(ns2),
                                               GrowArrow(st_arrows[1]), FadeIn(loop2), FadeIn(loop2_l),
                                               lag_ratio=0.25), run_time=1.1)
            vo.wait_until("arguments in")
            self.play(Indicate(argv2, color=TURN, scale_factor=1.15), run_time=0.6)
            vo.wait_until("one web request")
            self.play(GrowArrow(req2), FadeIn(req2_l), FadeIn(gcloud2, scale=0.85), FadeIn(host2), run_time=0.8)
            vo.wait_until("one line out")
            self.play(GrowArrow(ret2), FadeIn(json2), run_time=0.4)
            self.play(json2.animate.move_to([x_vm2 + 0.75, y_ret2 + 0.38, 0]),
                      FadeIn(out2, shift=DOWN * 0.1), FadeIn(exp2), run_time=0.8)
            vo.wait_until("What it needs")
            self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.6) for c in pk], lag_ratio=0.3), run_time=1.0)
            vo.wait_until("third-party packages")
            self.play(LaggedStart(*[FadeIn(q, scale=0.5) for q in qs], lag_ratio=0.3), run_time=0.6)
            vo.wait_until("find them a home")
            self.play(*[Indicate(c, color=LOOKUP, scale_factor=1.12) for c in pk],
                      *[Wiggle(q, scale_value=1.2) for q in qs], run_time=1.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.wait(0.2)
