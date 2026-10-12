"""S08 · What a virtual environment is (concept scene: no tracker, no terminal).

Beats (script.md "## S08"):
0. S05's ponder picture returns, without a timer: one ORANGE `/usr/local` shelf with its httpx
   jar, two GREY students asking for httpx 0.13 and 0.28. The shelf splits into two GREEN
   toolboxes, one under each student, labelled with the project folder; each request drops in as
   a GREEN jar -> "virtual environment".
1. The "you" toolbox becomes a GREEN `.venv/` folder at center, which opens (three dim badges).
   Part 1: `bin/python`, a GREEN link arrow out of the folder to a GREY "real Python interpreter".
2. Part 2: an empty GREEN shelf `lib/python3.X/site-packages/`; GREY note dist- vs site-packages.
3. Part 3: a `pyvenv.cfg` card; its real line (debian12-part-b/10-pyvenv.txt line 6)
   `include-system-site-packages = false` highlighted YELLOW.
4. V2, one stack morphing in place (tag illustration): "python3 (system)" -> ".venv/bin/python";
   the standard library band stays ("from the real interpreter"); both ORANGE dist-packages shelves
   slide out right and fade; an empty GREEN `.venv/lib/python3.X/site-packages` shelf slides in
   from the left into their place.
5. Engine ("interpreter") with two toolboxes that plug in in turn; RED barrier between them; each
   side's jars dim while the other toolbox is plugged in ("invisible ... and the other way round").
6. pip's hint (debian12-part-a/07-pip-refused.txt line 10), `python3 -m venv` underlined YELLOW,
   a GREY arrow "the classic way" to the venv toolbox; a PURPLE uv chip "today: uv makes it for us".
7. V7: the venv toolbox inside a dashed GREY "container (L2)" inside the BLUE VM; three
   RED-outlined chips outside the venv: the operating system, system libraries (C), GPU drivers.
8. The venv opens into its three numbered parts, which shrink into a corner card
   "coming up: the real files, after uv sync"; fade to an empty frame.
"""

import numpy as np
from manim import *

from explainer import style as S
from explainer.components import person_icon
from explainer.devops import (MONO, OUTPUT, box, chip, file_glyph, folder_glyph, label, machine_box, mono,
                              mono_line, step_badge, substring, tag)
from explainer.scene import VoiceScene

from common import (CLOUD, ERR, INK, NARRATION, SYSTEM, TURN, UV, VENV, Shelves, capture, jar, jars,
                    name_tag)

SAY = NARRATION["S08"]

# real lines (pick index = file line - 1)
HINT = capture("07-pip-refused", "debian12-part-a").pick(9)[0].strip()       # file line 10
CFG_LINE = capture("10-pyvenv", "debian12-part-b").pick(5)[0]               # file line 6
assert HINT.startswith("create a virtual environment using python3 -m venv"), HINT
assert CFG_LINE == "include-system-site-packages = false", CFG_LINE

PARTS = ["bin/python", "lib/python3.X/site-packages/", "pyvenv.cfg"]


# ------------------------------------------------------------------ small glyphs
def toolbox(w: float, h: float, color: str, fill: float = 0.1) -> VGroup:
    """A toolbox: a rounded body with a handle on top. .body .handle"""
    body = box(w, h, color, fill_opacity=fill, radius=0.12, stroke=3)
    hw, hh = min(1.1, w * 0.3), 0.26
    handle = VMobject(stroke_color=color, stroke_width=4)
    handle.set_points_as_corners([[-hw / 2, 0, 0], [-hw / 2, hh, 0], [hw / 2, hh, 0], [hw / 2, 0, 0]])
    handle.next_to(body, UP, buff=0)
    g = VGroup(body, handle)
    g.body, g.handle = body, handle
    return g


def gear(r: float = 0.6, n: int = 9, color: str = S.GREY) -> VGroup:
    """An engine glyph: a cog with a hub."""
    teeth = VGroup(*[Rectangle(width=r * 0.34, height=r * 0.42, stroke_width=0).set_fill(color, 1)
                     .move_to(UP * r * 1.02).rotate(k * TAU / n, about_point=ORIGIN) for k in range(n)])
    ring = Circle(radius=r, stroke_color=color, stroke_width=3).set_fill(S.GREY_DARKER, 1)
    hub = Circle(radius=r * 0.36, stroke_color=color, stroke_width=3).set_fill(S.BG, 1)
    return VGroup(teeth, ring, hub)


def badge(n: int, color: str = VENV, r: float = 0.22, size: float = 22) -> VGroup:
    return step_badge(n, color, size=size, radius=r)


def jar_row(n: int, color: str, height: float = 0.42, buff: float = 0.14) -> VGroup:
    return VGroup(*jars(n, color, height)).arrange(RIGHT, buff=buff)


def labelled_toolbox(text: str, color: str, n_jars: int, w: float = 4.4, h: float = 1.3) -> VGroup:
    """A toolbox with its folder name inside at the top and a row of jars at the bottom."""
    tb = toolbox(w, h, color)
    name = mono(text, 22, color)
    name.move_to(tb.body.get_top() + DOWN * 0.3)
    row = jar_row(n_jars, color)
    row.move_to(tb.body.get_bottom() + UP * 0.38)
    tb.add(name, row)
    tb.name, tb.jars = name, row
    return tb


def flash_frame(m, color: str, width: float = 7, run_time: float = 0.9):
    """A bright pass along a frame's outline."""
    c = m.copy().set_stroke(color, width).set_fill(opacity=0)
    return ShowPassingFlash(c, time_width=0.5, run_time=run_time)


class WhatIsAVenv(VoiceScene):
    def construct(self):
        assert len(SAY) == 9, len(SAY)

        # ========================================================== 0 · back to the puzzle
        board = Line(LEFT * 2.7, RIGHT * 2.7, color=SYSTEM, stroke_width=6).move_to(UP * 0.85)
        board_label = mono("/usr/local/… (pip's)", 24, SYSTEM)
        board_label.next_to(board, UP, buff=0.08).align_to(board, LEFT)
        sjar = jar(SYSTEM, 0.6).next_to(board, UP, buff=0.04).align_to(board, RIGHT).shift(LEFT * 0.3)
        sjar_tag = name_tag(sjar, "httpx", INK, 24)
        shelf = VGroup(board, board_label, sjar, sjar_tag)

        students = []
        for side, who, want in ((-1, "classmate", "httpx 0.13"), (1, "you", "httpx 0.28")):
            icon = person_icon(S.GREY, 1.3).move_to([side * 4.85, 1.25, 0])
            who_t = label(who, 26, S.GREY).next_to(icon, DOWN, buff=0.15)
            req = chip(want, S.GREY, size=24, font=MONO).next_to(icon, UP, buff=0.25)
            students.append((icon, who_t, req, want))
        (icon_l, who_l, req_l, want_l), (icon_r, who_r, req_r, want_r) = students
        arr_l = Arrow(req_l.get_right(), sjar_tag.get_left(), buff=0.15, color=S.GREY, stroke_width=3,
                      max_tip_length_to_length_ratio=0.06)
        arr_r = Arrow(req_r.get_left(), sjar_tag.get_right(), buff=0.15, color=S.GREY, stroke_width=3,
                      max_tip_length_to_length_ratio=0.12)

        tb_y = -1.6
        boxes = []
        for side, proj in ((-1, "classmate-app/"), (1, "simple-translate/")):
            tb = toolbox(3.6, 1.5, VENV).move_to([side * 4.7, tb_y, 0])
            proj_t = mono(proj, 24, INK).next_to(tb.body, DOWN, buff=0.2)
            boxes.append((tb, proj_t))
        (tb_l, proj_l), (tb_r, proj_r) = boxes

        def drop(tb, want):
            j = jar(VENV, 0.6).move_to(tb.body.get_bottom() + UP * 0.45)
            t = name_tag(j, want, INK, 24)
            return VGroup(j, t)

        new_l, new_r = drop(tb_l, want_l), drop(tb_r, want_r)
        venv_word = label("virtual environment", 32, VENV).move_to([0, tb_y, 0])
        venv_arrows = VGroup(
            Arrow(venv_word.get_left(), tb_l.body.get_right(), buff=0.12, color=VENV, stroke_width=3,
                  max_tip_length_to_length_ratio=0.3),
            Arrow(venv_word.get_right(), tb_r.body.get_left(), buff=0.12, color=VENV, stroke_width=3,
                  max_tip_length_to_length_ratio=0.3))

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(shelf, shift=DOWN * 0.15),
                      LaggedStart(*[FadeIn(VGroup(i, w), shift=UP * 0.15) for i, w, _, _ in students],
                                  lag_ratio=0.3), run_time=1.2)
            vo.wait_until("two versions")
            self.play(LaggedStart(FadeIn(req_l, shift=DOWN * 0.15), FadeIn(req_r, shift=DOWN * 0.15),
                                  lag_ratio=0.4), run_time=0.8)
            vo.wait_until("one shared shelf")
            self.play(GrowArrow(arr_l), GrowArrow(arr_r), run_time=0.6)
            self.play(Indicate(board, color=SYSTEM, scale_factor=1.05), Wiggle(sjar, scale_value=1.15),
                      run_time=0.8)
            vo.wait_until("The fix")
            half_l = Line(board.get_start(), board.get_center(), color=SYSTEM, stroke_width=6)
            half_r = Line(board.get_center(), board.get_end(), color=SYSTEM, stroke_width=6)
            self.remove(board)
            self.add(half_l, half_r)
            # each half of the shelf drops under a student and becomes the lid of a toolbox
            lid_l = Line(tb_l.body.get_corner(UL), tb_l.body.get_corner(UR), color=VENV, stroke_width=4)
            lid_r = Line(tb_r.body.get_corner(UL), tb_r.body.get_corner(UR), color=VENV, stroke_width=4)
            self.play(FadeOut(VGroup(board_label, sjar, sjar_tag, arr_l, arr_r)),
                      Transform(half_l, lid_l), Transform(half_r, lid_r), run_time=0.8)
            self.play(ReplacementTransform(half_l, tb_l), ReplacementTransform(half_r, tb_r),
                      FadeIn(proj_l, shift=UP * 0.1), FadeIn(proj_r, shift=UP * 0.1), run_time=0.8)
            # each request is carried round the inner side of its student and drops into the toolbox
            paths = [CubicBezier(r.get_center(), r.get_center() + RIGHT * inward * 2.2,
                                 np.array([-inward * 2.95, 1.0, 0]), np.array([-inward * 2.95, -0.35, 0]))
                     for r, inward in ((req_l, 1), (req_r, -1))]
            self.play(MoveAlongPath(req_l, paths[0]), MoveAlongPath(req_r, paths[1]), run_time=0.8)
            self.play(ReplacementTransform(req_l, new_l), ReplacementTransform(req_r, new_r), run_time=0.6)
            vo.wait_until("That toolbox")
            self.play(FadeIn(venv_word, scale=0.9), GrowArrow(venv_arrows[0]), GrowArrow(venv_arrows[1]),
                      run_time=0.8)

        # ========================================================== 1 · a folder with three parts
        frame = box(8.4, 5.7, VENV, fill_opacity=0.04, stroke=3).move_to([-2.3, -0.2, 0])
        closed = VGroup(folder_glyph(1.0, VENV), mono(".venv/", 40, VENV)).arrange(RIGHT, buff=0.3)
        header = VGroup(folder_glyph(0.42, VENV), mono(".venv/", 30, VENV)).arrange(RIGHT, buff=0.2)
        header.align_to(frame, LEFT).align_to(frame, UP).shift(RIGHT * 0.3 + DOWN * 0.25)

        x_badge, x_text = frame.get_left()[0] + 0.5, frame.get_left()[0] + 0.95
        y1, y2, y3 = 1.35, -0.05, -1.75
        dim_badges = VGroup(*[badge(n, S.GREY_DARK).move_to([x_badge, y, 0])
                              for n, y in ((1, y1), (2, y2 + 0.2), (3, y3))])
        lit = [badge(n).move_to(dim_badges[n - 1]) for n in (1, 2, 3)]

        # part 1: bin/python -> a real interpreter, somewhere else
        p1 = mono("bin/python", 26, INK)
        p1.move_to([0, y1, 0]).align_to([x_text, 0, 0], LEFT)
        real = label("a real Python interpreter,\nsomewhere else", 22, INK)
        real_box = box(real.width + 0.5, real.height + 0.4, S.GREY, fill_opacity=0.1)
        real_box.move_to([4.5, y1 + 0.05, 0])
        real.move_to(real_box)
        link = Arrow(p1.get_right() + RIGHT * 0.1, real_box.get_left(), buff=0.08, color=VENV, stroke_width=4,
                     max_tip_length_to_length_ratio=0.06)
        link_t = label("a link, not a copy", 22, S.GREY).next_to(link, UP, buff=0.1)
        link_t.set_x(link.get_center()[0] - 0.4)

        # part 2: its own (empty) site-packages shelf
        sp_board = Line([x_text, y2 - 0.12, 0], [frame.get_right()[0] - 0.4, y2 - 0.12, 0], color=VENV,
                        stroke_width=5)
        sp_label = mono(PARTS[1], 24, VENV).next_to(sp_board, UP, buff=0.1).align_to(sp_board, LEFT)
        sp_empty = label("empty", 22, S.GREY).next_to(sp_board, UP, buff=0.1).align_to(sp_board, RIGHT)
        sp_light = Rectangle(width=sp_board.get_length() + 0.3, height=0.62, stroke_width=0) \
            .set_fill(VENV, 0.25).move_to(sp_board.get_center() + UP * 0.24)
        n1, n2 = label("Debian's system Python:", 22, S.GREY), mono("dist-packages", 22, SYSTEM)
        n3, n4 = label("everywhere else:", 22, S.GREY), mono("site-packages", 22, S.GREY)
        note = VGroup(n1, n2, n3, n4).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        n2.shift(RIGHT * 0.3)
        n4.shift(RIGHT * 0.3)
        n3.shift(DOWN * 0.08)
        n4.shift(DOWN * 0.08)
        note.move_to([0, y2 - 0.1, 0]).align_to(real_box, LEFT).shift(RIGHT * 0.05)

        # part 3: pyvenv.cfg (its real line, from the part-b capture)
        cfg_head = VGroup(file_glyph(0.32, S.GREY), mono("pyvenv.cfg", 24, INK)).arrange(RIGHT, buff=0.15)
        cfg_lines = VGroup(mono_line("…", 22, S.GREY), mono_line(CFG_LINE, 22, INK),
                           mono_line("…", 22, S.GREY)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        cfg_body = VGroup(cfg_head, cfg_lines).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        cfg_box = box(cfg_body.width + 0.6, cfg_body.height + 0.36, S.GREY, fill_opacity=0.08)
        cfg_body.move_to(cfg_box)
        cfg_sep = Line(cfg_box.get_left() + RIGHT * 0.12, cfg_box.get_right() + LEFT * 0.12, color=S.GREY_DARK,
                       stroke_width=2).set_y((cfg_head.get_bottom()[1] + cfg_lines.get_top()[1]) / 2)
        cfg = VGroup(cfg_box, cfg_sep, cfg_body)
        cfg.move_to([0, y3, 0]).align_to([x_text, 0, 0], LEFT)
        inc = cfg_lines[1]
        inc_bar = Rectangle(width=inc.glyphs.width + 0.36, height=inc.strut.height + 0.08, stroke_width=0) \
            .set_fill(TURN, 0.22).move_to([inc.glyphs.get_x(), inc.strut.get_y(), 0])
        false_box = SurroundingRectangle(substring(inc, "false"), color=TURN, buff=0.09, stroke_width=3,
                                         corner_radius=0.05)

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(icon_l, who_l, icon_r, who_r, tb_l, proj_l, new_l, proj_r, new_r,
                                     venv_word, venv_arrows)),
                      ReplacementTransform(tb_r, closed), run_time=1.0)
            vo.wait_until("usually called")
            self.play(Indicate(closed[1], color=VENV, scale_factor=1.12), run_time=0.8)
            vo.wait_until("with three parts")
            self.play(ReplacementTransform(closed, header), FadeIn(frame, scale=0.4),
                      LaggedStart(*[FadeIn(b, scale=0.6) for b in dim_badges], lag_ratio=0.25), run_time=1.0)
            vo.wait_until("First")
            self.play(ReplacementTransform(dim_badges[0], lit[0]), Write(p1), run_time=0.9)
            vo.wait_until("not a copy")
            self.play(GrowArrow(link), FadeIn(link_t, shift=DOWN * 0.1), run_time=0.9)
            vo.wait_until("a real interpreter")
            self.play(FadeIn(real_box), Write(real), run_time=1.0)

        with self.voiceover(SAY[2]) as vo:
            self.play(ReplacementTransform(dim_badges[1], lit[1]), Create(sp_board), FadeIn(sp_label, shift=UP * 0.1),
                      run_time=1.0)
            vo.wait_until("empty when")
            self.play(FadeIn(sp_empty, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("Site-packages is")
            self.play(FadeIn(VGroup(n3, n4), shift=LEFT * 0.15), run_time=0.7)
            vo.wait_until("Debian calls")
            self.play(FadeIn(VGroup(n1, n2), shift=LEFT * 0.15), run_time=0.7)
            vo.wait_until("dist-packages")
            self.play(Indicate(n2, color=SYSTEM, scale_factor=1.1), run_time=0.8)
            vo.wait_until("This is where")
            self.play(FadeIn(sp_light), Indicate(header, color=VENV, scale_factor=1.06), run_time=0.9)
            vo.wait_until("only this project")
            self.play(FadeOut(sp_light), run_time=0.8)

        with self.voiceover(SAY[3]) as vo:
            self.play(ReplacementTransform(dim_badges[2], lit[2]), FadeIn(cfg, shift=UP * 0.15), run_time=1.0)
            vo.wait_until("When Python starts")
            self.play(Indicate(p1, color=VENV, scale_factor=1.05), run_time=0.9)
            vo.wait_until("it reads this file")
            self.play(Indicate(cfg_head, color=VENV, scale_factor=1.1), run_time=0.9)
            vo.wait_until("It says")
            self.play(FadeIn(inc_bar), run_time=0.5)
            vo.wait_until("use my site-packages")
            self.play(Indicate(sp_label, color=VENV, scale_factor=1.06), run_time=0.9)
            vo.wait_until("leave the system")
            self.play(Create(false_box), run_time=0.6)

        folder_all = VGroup(frame, header, *lit, p1, link, link_t, real_box, real, sp_board, sp_label, sp_empty,
                            note, cfg, inc_bar, false_box)

        # ========================================================== 4 · V2: one stack, morphing in place
        stack = Shelves(["(empty) = the current folder", "standard library", "/usr/local/… (pip's)",
                         "/usr/lib/python3/… (apt's)"], width=12.4, size=22, pitch=1.3,
                        colors={2: SYSTEM, 3: SYSTEM})
        std_board, std_mono = stack.rows[1]
        std_text = label("standard library", 24, S.GREY).move_to(std_mono, aligned_edge=LEFT)
        stack.rows[1].remove(std_mono)
        stack.rows[1].add(std_text)
        stack.move_to([0, 0, 0]).shift(UP * (1.3 - stack.rows[0][0].get_y()))
        band = Rectangle(width=12.4, height=0.8, stroke_width=0).set_fill(S.GREY, 0.12)
        band.move_to(std_board, aligned_edge=DOWN)
        pip_jars = stack.put(2, jars(12, SYSTEM))
        apt_jars = stack.put(3, jars(4, SYSTEM))
        title_sys = mono("python3 (system)", 28, SYSTEM)
        title_sys.move_to([0, 2.35, 0]).align_to(stack, LEFT)
        title_venv = mono(".venv/bin/python", 28, VENV).move_to(title_sys, aligned_edge=LEFT)
        ill = tag("illustration · a venv made from this same python3", S.GREY)
        ill.move_to([0, 3.2, 0]).align_to(stack, RIGHT)
        std_tag = tag("from the real interpreter", S.GREY).move_to(band).align_to(band, RIGHT).shift(LEFT * 0.2)
        green = Shelves([".venv/lib/python3.X/site-packages"], width=12.4, size=22, colors={0: VENV})
        green.shift(stack.rows[2][0].get_center() - green.rows[0][0].get_center())
        leaving = VGroup(stack.rows[2], stack.rows[3], pip_jars, apt_jars)

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(folder_all), run_time=0.6)
            self.play(FadeIn(band), FadeIn(title_sys, shift=DOWN * 0.1), FadeIn(ill),
                      LaggedStart(*[FadeIn(r, shift=DOWN * 0.1) for r in stack.rows], lag_ratio=0.15),
                      FadeIn(pip_jars), FadeIn(apt_jars), run_time=1.3)
            vo.wait_until("Started from")
            self.play(ReplacementTransform(title_sys, title_venv), run_time=1.0)
            vo.wait_until("The standard library")
            self.play(Indicate(std_text, color=INK, scale_factor=1.08), FadeIn(std_tag, shift=LEFT * 0.2),
                      run_time=1.0)
            vo.wait_until("But both")
            self.play(FadeOut(leaving, shift=RIGHT * 4.5), run_time=1.3)
            vo.wait_until("and the venv")
            self.play(FadeIn(green, shift=RIGHT * 4.5), run_time=1.1)

        v2_all = VGroup(band, title_venv, ill, stack.rows[0], stack.rows[1], std_tag, green)

        # ========================================================== 5 · same engine, different toolbox
        eng = gear(0.6).move_to([0, 2.35, 0])
        eng_t = label("interpreter", 26, INK).next_to(eng, RIGHT, buff=0.35)
        socket = Line(eng.get_bottom() + DOWN * 0.02, eng.get_bottom() + DOWN * 0.42, color=S.GREY, stroke_width=5)
        motto = label("same engine, different toolbox", 26, INK)
        motto.move_to([0, eng.get_y(), 0]).align_to([-6.3, 0, 0], LEFT)
        tb_sys = labelled_toolbox("/usr/…/dist-packages", SYSTEM, 4)
        tb_venv = labelled_toolbox(".venv/…/site-packages", VENV, 3)
        rest_y = -1.85
        tb_sys.move_to([-3.95, rest_y, 0])
        tb_venv.move_to([3.95, rest_y, 0])
        rest_sys, rest_venv = tb_sys.get_center(), tb_venv.get_center()
        plug = socket.get_end() - (tb_sys.handle.get_top() - tb_sys.get_center())
        barrier = Line([0, -0.85, 0], [0, -3.1, 0], color=ERR, stroke_width=4)

        def plug_in(tb, color, jar_opacity=None):
            tb.generate_target()
            tb.target.move_to(plug)
            if jar_opacity is not None:              # the jar row moves with its box: one target
                tb.target[3].set_opacity(jar_opacity)
            return [MoveToTarget(tb), socket.animate.set_color(color)]

        def unplug(tb, home):
            return [tb.animate.move_to(home), socket.animate.set_color(S.GREY)]

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(v2_all), FadeIn(VGroup(eng, eng_t, socket)), FadeIn(tb_sys, shift=UP * 0.2),
                      FadeIn(tb_venv, shift=UP * 0.2), run_time=0.8)
            self.play(*plug_in(tb_sys, SYSTEM), Rotate(eng, -PI / 3), FadeIn(motto, shift=RIGHT * 0.2),
                      run_time=0.7)
            self.play(*unplug(tb_sys, rest_sys), run_time=0.45)
            self.play(*plug_in(tb_venv, VENV), Rotate(eng, -PI / 3), run_time=0.6)
            vo.wait_until("don't mix")
            self.play(*unplug(tb_venv, rest_venv), run_time=0.5)
            self.play(Create(barrier), run_time=0.6)
            vo.wait_until("invisible")
            self.play(*plug_in(tb_sys, SYSTEM), Rotate(eng, -PI / 3), tb_venv.jars.animate.set_opacity(0.2),
                      run_time=0.8)
            vo.wait_until("the other way")
            self.play(*unplug(tb_sys, rest_sys), run_time=0.45)
            self.play(*plug_in(tb_venv, VENV, jar_opacity=1), Rotate(eng, -PI / 3),
                      tb_sys.jars.animate.set_opacity(0.2), run_time=0.7)

        # ========================================================== 6 · pip's hint, and uv
        hint = mono_line(HINT, 22, OUTPUT).move_to([0, 2.6, 0])
        hint_cap = label("pip's hint, in the refusal from part 1", 22, S.GREY)
        hint_cap.next_to(hint, UP, buff=0.18).align_to(hint, LEFT)
        classic = substring(hint, "python3 -m venv")
        ul = Line(classic.get_corner(DL) + DOWN * 0.1, classic.get_corner(DR) + DOWN * 0.1, color=TURN,
                  stroke_width=4)
        venv_tb_pos = np.array([0.0, -1.2, 0])
        venv_name = mono(".venv/", 26, VENV)
        uv_chip = chip("uv", UV, size=32, font=MONO)
        uv_chip.move_to([4.6, venv_tb_pos[1] + 0.15, 0])
        uv_cap = label("today: uv makes it for us", 24, INK).next_to(uv_chip, DOWN, buff=0.25)

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(eng, eng_t, socket, motto, tb_sys, barrier)),
                      tb_venv.animate.move_to(venv_tb_pos), run_time=0.8)
            venv_name.move_to(tb_venv.name)
            self.play(Transform(tb_venv.name, venv_name), FadeIn(hint_cap), FadeIn(hint, shift=DOWN * 0.1),
                      run_time=0.8)
            vo.wait_until("It suggested")
            self.play(Create(ul), classic.animate.set_color(TURN), run_time=0.6)
            vo.wait_until("the classic way")
            make1 = Arrow(ul.get_center() + DOWN * 0.05, tb_venv.handle.get_top() + RIGHT * 0.9, buff=0.12,
                          color=S.GREY, stroke_width=3, max_tip_length_to_length_ratio=0.08)
            make1_t = label("the classic way", 22, S.GREY).next_to(make1.get_center(), RIGHT, buff=0.25)
            self.play(GrowArrow(make1), FadeIn(make1_t, shift=LEFT * 0.1), run_time=0.8)
            vo.wait_until("Today")
            make2 = Arrow(uv_chip.get_left(), tb_venv.body.get_right(), buff=0.15, color=UV, stroke_width=4,
                          max_tip_length_to_length_ratio=0.15)
            self.play(FadeIn(uv_chip, shift=LEFT * 1.2), run_time=0.6)
            self.play(GrowArrow(make2), FadeIn(uv_cap, shift=UP * 0.1), run_time=0.7)
            vo.wait_until("a lot more")
            self.play(Indicate(uv_chip, color=UV, scale_factor=1.2), run_time=0.8)

        # ========================================================== 7 · what a venv doesn't isolate
        vm = machine_box("VM", "a whole machine", width=12.7, height=6.45, color=CLOUD)
        vm.move_to([0, -0.22, 0])
        ctr = machine_box("container (L2)", "next lecture", width=11.9, height=4.85, color=S.GREY, dashed=True,
                          fill_opacity=0)
        ctr.move_to([0, -0.72, 0])
        venv_pos = np.array([-3.25, ctr.body.get_y() - 0.1, 0])
        names = ["the operating system", "system libraries (C)", "GPU drivers"]
        outs = VGroup(*[chip(n, ERR, size=24, fill_opacity=0.06) for n in names])
        outs.arrange(DOWN, buff=0.32).move_to([3.05, ctr.body.get_y() - 0.1, 0])

        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(hint, hint_cap, ul, make1, make1_t, uv_chip, uv_cap, make2)),
                      tb_venv.animate.move_to(venv_pos), run_time=0.8)
            self.play(FadeIn(ctr, scale=0.92), FadeIn(vm, scale=0.92), run_time=0.8)
            for n, c in zip(["the operating system", "system libraries", "and drivers"], outs):
                vo.wait_until(n)
                self.play(FadeIn(c, shift=LEFT * 0.3), run_time=0.5)
            vo.wait_until("a whole machine")
            self.play(flash_frame(vm.frame, CLOUD), Indicate(vm.header, color=CLOUD, scale_factor=1.08), run_time=1.0)
            vo.wait_until("or a container")
            solid = RoundedRectangle(width=11.9, height=4.85, corner_radius=0.14).move_to(ctr)
            self.play(flash_frame(solid, INK), Indicate(ctr.header, color=INK, scale_factor=1.08), run_time=1.0)

        # ========================================================== 8 · coming up: the real files
        big = VGroup()
        for n, p in enumerate(PARTS, start=1):
            row = VGroup(badge(n, VENV, 0.26, 24), mono(p, 28, INK)).arrange(RIGHT, buff=0.3)
            big.add(row)
        big.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(ORIGIN)

        small = VGroup()
        for n, p in enumerate(PARTS, start=1):
            small.add(VGroup(badge(n, VENV, 0.2, 20), mono(p, 20, INK)).arrange(RIGHT, buff=0.2))
        small.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        card_head = label("coming up: the real files, after uv sync", 20, INK)
        card_body = VGroup(card_head, small).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        card_box = box(card_body.width + 0.45, card_body.height + 0.4, S.GREY, fill_opacity=0.08)
        card_body.move_to(card_box)
        card = VGroup(card_box, card_body)
        card.to_corner(UR, buff=0.6)

        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(vm, ctr, outs)), FadeOut(tb_venv, scale=0.6), run_time=0.7)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.3) for r in big], lag_ratio=0.3), run_time=1.0)
            vo.wait_until("find all three")
            self.play(ReplacementTransform(big, small), run_time=0.8)
            self.play(FadeIn(card_box), FadeIn(card_head, shift=DOWN * 0.1), run_time=0.5)

        self.wait(0.4)
        self.play(FadeOut(*self.mobjects), run_time=0.8)
