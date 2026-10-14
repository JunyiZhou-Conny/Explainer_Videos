"""S01 · One command on a fresh VM (cold open of AC215 L2).

Beats (script.md, ## S01; one voiceover block each):
0. Black frame, no tracker. The house terminal (12.6 wide, 12 rows, `ssh · ac215-l02`, prompt
   `student@ac215-l02:~$`) fades in with a blinking cursor; its title flashes BLUE on "in the
   cloud". Above it, right-aligned, three GREY chips "code", "venv", "uv" appear as named and are
   crossed RED; a PURPLE `docker` chip gets a GREEN check on "only Docker". On "we type one command"
   `sudo docker run --rm -ti dlops/simple-translate` (README.md line 215) types (two rows); on
   "Just watch" the GREY tag "preview · you'll run it in part 2" sits on the terminal's top-left.
1. The chips fade; a small BLUE shelf glyph "Docker Hub" sits at the top right. vm-debian12/06 lines
   2-3 print; on "in seven layers" a PINK arrow runs from the shelf into the terminal and pulses
   seven times while lines 4, …, 10 print and a TEAL counter beside them counts "1 layer" to
   "7 layers"; lines 11-12 (hash12). On "starts a shell" the arrow and shelf leave and the prompt
   becomes `root@c7c280390994:/#` (line 13); on "There we run the app" it types `python cli.py`
   -> lines 16-20, 24 (wrapped), 26-27; the terminal scrolls. "I love cheese" pulses on the
   Input line; on "comes back in Italian" `Adoro il formaggio` turns GREEN and stays on screen.
2. `python --version` (line 28, GREY `extra` tag) -> line 29; on "It's 3.14.7" `3.14.7` turns
   YELLOW. On "Yet the recipe" the terminal shrinks to the 3-row bottom strip (the preview tag rides
   on its top edge) and CODE(Dockerfile.txt: 2) slides in above it; `python:3.12` turns ORANGE and
   is underlined; a copy of `3.14.7` rises from the strip to the right of the panel with a YELLOW
   "?" between them; the "?" wiggles on "Hold that thought".
3. V1 ladder (README.md lines 9-16, all rungs dim): rung 4 is circled YELLOW ("that's where ...
   ends"); on "Last lecture" rungs 1-2 light softly with a GREY bracket "L1" (rung 1, then rung 2,
   pulse as named); on "Today" rungs 3-4 light fully with a YELLOW bracket "today"; rung 3's laptop
   icon pulses on "package the app"; a BLUE "Docker Hub" shelf right of the ladder gets a PINK route
   from rung 3 on "push it", and a second route up to rung 4's VM on "run it on a VM".
4. Layout preview: a README page glyph appears ("open the README"); on "Three trackers" it flies to
   the top-left corner and becomes a YELLOW ring; three tracker chips appear in it as named, each
   with its icon: "A · Developing App using Containers · 16" (GREY laptop), "B · Pushing Docker
   Image to Docker Hub · 4" (BLUE shelf), "C · Running App on VM using Docker · 7" (BLUE VM); the
   ring pulses. On "When the yellow" a 2-row strip (GREY tag "preview") types `docker image ls` with
   a YELLOW `▶ your turn` row tag (pulses on "pause and run"), then `ls -a` with the GREY `extra`
   tag; the footer "every command: MLOps_Learning · guides/L02-containers-1.md" fades in.
5. Checklist card, rows as named: ✓ Docker Desktop running (Tutorial 0), ✓ a free Docker Hub
   account, ✓ your GCP project, for the VM at the end (+ GOLD tag "a VM costs money while it
   exists" beside it), GREY ✗ no service account, no keys (README.md · line 23). Fade out to an
   empty frame.
"""

import numpy as np  # noqa: I001  (manim first, then common: common must win)
from manim import *

from explainer import style as S
from explainer.devops import cell_width, code_span
from explainer.scene import VoiceScene

from common import (CLOUD, COST, DEPLOY, ERR, IMAGE, IMAGE_LS, INK, LAPTOP, NARRATION, P_LAPTOP,
                    P_LAPTOP_HOME, P_VM, ROUTE, SECTION_A, SECTION_B, SECTION_C, STEPS_A, STEPS_B,
                    STEPS_C, STRIP_TOP, SYSTEM, TURN, VENV, VM12, Ladder, box, capture, check_mark,
                    chip, code, cross_mark, docker_chip, hash12, label, laptop, mono, mono_line,
                    preview_tag, resize, row_tag, shelf_glyph, short_extra, split_prompt, steady,
                    substring, tag, term, type_cmd, vm_term)

SAY = NARRATION["S01"]

RUN6 = capture("06", VM12)                     # vm-debian12/06-docker-run.txt
assert RUN6.cmd == DEPLOY, RUN6.cmd
GUIDE = "MLOps_Learning · guides/L02-containers-1.md"


# ------------------------------------------------------------------ small pictures
def bracket(top: float, bottom: float, x: float, color, tick: float = 0.2) -> VMobject:
    """A '[' at x from y=top to y=bottom, ticks pointing right (toward the ladder)."""
    m = VMobject(stroke_color=color, stroke_width=3.5)
    m.set_points_as_corners([[x + tick, top, 0], [x, top, 0], [x, bottom, 0], [x + tick, bottom, 0]])
    return m


def readme_page(w: float = 2.8, h: float = 3.3) -> VGroup:
    """The README as a page glyph (not a screenshot): its file name and a few lines of text."""
    frame = RoundedRectangle(width=w, height=h, corner_radius=0.12, stroke_color=S.GREY,
                             stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
    name = mono("README.md", 24, INK).move_to(frame.get_top() + DOWN * 0.42)
    lines = VGroup(*[Line(LEFT * f * (w - 0.7) / 2, RIGHT * f * (w - 0.7) / 2, color=S.GREY_DARK,
                          stroke_width=6) for f in (1, 0.8, 0.95, 0.6, 1, 0.85, 0.7)])
    lines.arrange(DOWN, buff=0.26, aligned_edge=LEFT)
    lines.next_to(name, DOWN, buff=0.35).align_to(frame, LEFT).shift(RIGHT * 0.35)
    return VGroup(frame, name, lines)


def vm_icon(w: float = 0.62) -> VGroup:
    """A small BLUE VM (two server slots), no text."""
    h = w * 0.72
    f = box(w, h, CLOUD, fill_opacity=0.15, radius=0.06)
    slots = VGroup(*[RoundedRectangle(width=w * 0.7, height=h * 0.18, corner_radius=0.03,
                                      stroke_color=CLOUD, stroke_width=1.5) for _ in range(2)])
    slots.arrange(DOWN, buff=h * 0.14).move_to(f)
    return VGroup(f, slots)


def tracker_chip(letter: str, section: str, n: int, icon: VGroup, chip_w: float) -> VGroup:
    """One tracker of the video, as a chip: icon, 'A · <README section> · <steps>'. .icon .text"""
    t = label(f"{letter} · {section} · {n}", 22, INK)
    t[0].set_color(TURN)                          # one Text: the letter shares the baseline
    icon.scale_to_fit_height(0.4)
    frame = box(chip_w, 0.62, S.GREY, fill_opacity=0.06, radius=0.12)
    icon.move_to(frame.get_left() + RIGHT * (0.22 + icon.width / 2))
    t.next_to(icon, RIGHT, buff=0.25)
    g = VGroup(frame, icon, t)
    g.icon, g.text = icon, t
    return g


def counter_box(k: int, box_w: float) -> tuple[VGroup, Text]:
    """A TEAL row tag 'k layers' whose text can Transform (steady)."""
    b = RoundedRectangle(width=box_w, height=0.36, corner_radius=0.18, stroke_color=IMAGE,
                         stroke_width=2).set_fill(S.BG, 0.92)
    return b, counter_text(k, b)


def counter_text(k: int, b) -> Text:
    s = f"{k} layer" + ("" if k == 1 else "s")
    t = steady(s, 20, IMAGE)
    return t.move_to(b).align_to(b, LEFT).shift(RIGHT * 0.17)


def baseline_y(t: Text, s: str) -> float:
    """The baseline of text `t` (made from `s`): the bottom of its first glyph without a descender."""
    for c, g in zip([c for c in s if not c.isspace()], t):
        if c.isalnum() and c not in "gjpqyQ":
            return g.get_bottom()[1]
    return t.get_bottom()[1]


def clear_stage(scene, *anims, run_time: float = 0.6):
    """Fade out everything on screen (together with `anims`), then drop it from the scene."""
    old = [m for m in scene.mobjects]
    if old:
        scene.play(FadeOut(Group(*old)), *anims, run_time=run_time)
        scene.remove(*old)
    elif anims:
        scene.play(*anims, run_time=run_time)


# ------------------------------------------------------------------ the scene
class Hook(VoiceScene):
    def construct(self):
        assert len(SAY) == 6, len(SAY)

        # ========================================================== 0. a fresh VM, one command
        t = vm_term(12)                               # bottom edge at -3.5, top at ~2.19
        row_y = 2.9                                   # the row above the terminal
        p = P_VM + " "
        prompt0 = mono_line(p, t.size, INK, t2c=t._prompt_colors(P_VM))
        t._place(prompt0, 0)
        cw = cell_width(t.size)
        cursor = Rectangle(width=cw * 0.92, height=prompt0.strut.height * 0.86, stroke_width=0) \
            .set_fill(INK, 0.85)
        cursor.move_to([prompt0.strut.get_left()[0] + cw * (len(p) + 0.5), prompt0.strut.get_center()[1], 0])

        gone = VGroup(*[chip(s, S.GREY, size=24) for s in ("code", "venv", "uv")]).arrange(RIGHT, buff=0.3)
        dock = docker_chip(size=24)
        tick = check_mark(0.4, VENV)
        chips = VGroup(gone, dock, tick).arrange(RIGHT, buff=0.55)
        tick.shift(LEFT * 0.3)
        chips.move_to([t.box.get_right()[0] - chips.width / 2, row_y, 0])
        crosses = VGroup(*[Line(c.get_left() + LEFT * 0.1 + DOWN * 0.04, c.get_right() + RIGHT * 0.1 + UP * 0.04,
                                color=ERR, stroke_width=5) for c in gone])     # struck out
        prev = preview_tag()
        prev.move_to([t.box.get_left()[0] + prev.width / 2, row_y, 0])

        def blink(until: str, vo):
            while vo.time_until(until) > 0.9:
                self.play(cursor.animate.set_fill(opacity=0), run_time=0.15)
                self.wait(0.3)
                self.play(cursor.animate.set_fill(opacity=0.85), run_time=0.15)
                self.wait(0.3)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(t), FadeIn(prompt0), run_time=1.0)
            self.add(cursor)
            vo.wait_until("in the cloud")
            self.play(Indicate(t.title, color=CLOUD, scale_factor=1.25), run_time=0.9)
            for c, x, anchor in zip(gone, crosses, ("no copy of our code", "no virtual environment",
                                                    "no uv")):
                blink(anchor, vo)
                vo.wait_until(anchor)
                self.play(FadeIn(c, shift=DOWN * 0.15), run_time=0.4)
                self.play(Create(x), run_time=0.4)
            vo.wait_until("It has only Docker")
            self.play(FadeIn(dock, shift=DOWN * 0.15), run_time=0.5)
            self.play(Create(tick), run_time=0.4)
            vo.wait_until("we type one command")
            self.remove(cursor, prompt0)
            t.type(self, DEPLOY, type_time=1.6)
            vo.wait_until("Just watch")
            self.play(FadeIn(prev, shift=RIGHT * 0.2), run_time=0.6)

        # ========================================================== 1. pull, shell, translate
        shelf = shelf_glyph(1.0)
        hub = label("Docker Hub", 24, CLOUD)
        top_right = VGroup(hub, shelf).arrange(RIGHT, buff=0.25)
        top_right.move_to([t.box.get_right()[0] - top_right.width / 2, row_y, 0])

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(gone, crosses, dock, tick), shift=UP * 0.15), run_time=0.35)
            self.remove(gone, crosses, dock, tick)
            self.play(FadeIn(top_right, shift=LEFT * 0.2), run_time=0.35)
            t.print(self, RUN6.at(2, 3), run_time=0.35)
            # "downloads": the route from Docker Hub to the "…" row (two rows down), where a counter
            # rides; it counts the seven layers while "in seven layers" is said, and the pull is
            # over by "starts a shell"
            cb, ct = counter_box(1, 1.45)
            row_c = t.lines[-1].strut.get_center()[1] - 2 * t.pitch
            cb.move_to([t.box.get_right()[0] - 0.3 - cb.width / 2, row_c, 0])
            ct = counter_text(1, cb)
            a0 = np.array([shelf.get_center()[0], shelf.get_bottom()[1] - 0.08, 0])
            a1 = np.array([cb.get_center()[0], cb.get_top()[1] + 0.06, 0])
            arrow = Arrow(a0, a1, buff=0, color=ROUTE, stroke_width=4, tip_length=0.2,
                          max_tip_length_to_length_ratio=0.2)
            lane = Line(a0, a1, color=IMAGE, stroke_width=8)
            self.play(GrowArrow(arrow), run_time=0.35)
            t.print(self, RUN6.at(4), run_time=0.2)
            self.play(ShowPassingFlash(lane.copy(), time_width=0.6), FadeIn(cb), FadeIn(ct), run_time=0.25)
            dots = t.print(self, ["…"], run_time=0.12)[0]
            for k in range(2, 7):
                new = counter_text(k, cb)
                self.play(ShowPassingFlash(lane.copy(), time_width=0.6), Transform(ct, new), run_time=0.14)
            t.print(self, RUN6.at(10), run_time=0.12)
            self.play(ShowPassingFlash(lane.copy(), time_width=0.6), Transform(ct, counter_text(7, cb)),
                      Indicate(cb, color=IMAGE, scale_factor=1.08), run_time=0.3)
            # the counter becomes part of the "…" row, so it scrolls away with it
            self.remove(cb, ct)
            dots.add(cb, ct)
            self.add(dots)
            t.print(self, [hash12(s) for s in RUN6.at(11, 12)], run_time=0.25)
            vo.wait_until("starts a shell")
            prompt, typed = split_prompt(RUN6.line(13))
            assert typed == "python cli.py", typed
            t.set_prompt(prompt)
            shell = t.type(self, "", type_time=0)
            shell.bare = True
            self.play(FadeOut(arrow), FadeOut(top_right),
                      Indicate(substring(shell, prompt), color=IMAGE, scale_factor=1.06), run_time=0.8)
            self.remove(arrow, top_right)
            self.add(shell)
            vo.wait_until("There we run the app")
            type_cmd(self, t, typed, type_time=0.6)
            t.print(self, RUN6.at((16, 20), 24, 26, 27), wrap=True, run_time=0.8, lag=0.1)
            inp = t.find("Input: I love cheese")
            out = t.find("Output: Adoro il formaggio")
            vo.wait_until("I love cheese")
            self.play(Indicate(substring(inp, "I love cheese"), color=INK, scale_factor=1.12), run_time=0.8)
            self.add(inp)
            vo.wait_until("comes back in Italian")
            ita = substring(out, "Adoro il formaggio")
            self.play(ita.animate.set_color(VENV), run_time=0.4)
            self.play(Indicate(ita, color=VENV, scale_factor=1.12), run_time=0.7)
            self.add(out)

        # ========================================================== 2. which Python?
        ver_cap = RUN6.line(29)                       # "Python 3.14.7"
        assert ver_cap == "Python 3.14.7", ver_cap
        panel = code("Dockerfile.txt", 2, font_size=28)
        num_up = mono("3.14.7", 32, TURN)
        q = label("?", 64, TURN)
        pair = VGroup(q, num_up).arrange(RIGHT, buff=0.55)
        row_w = panel.width + 0.55 + pair.width
        panel.move_to([-row_w / 2 + panel.width / 2, 0.75, 0])
        pair.next_to(panel.code, RIGHT, buff=0.55).match_y(panel.code)
        span = code_span(panel.code, 0, "python:3.12")
        ul = Line(span.get_corner(DL) + DOWN * 0.08, span.get_corner(DR) + DOWN * 0.08, color=SYSTEM,
                  stroke_width=4)

        with self.voiceover(SAY[2]) as vo:
            prompt, typed = split_prompt(RUN6.line(28))
            assert typed == "python --version", typed
            t.set_prompt(prompt)
            ver_cmd = type_cmd(self, t, typed, type_time=0.7)
            xt = short_extra().next_to(ver_cmd.strut, RIGHT, buff=0.45)
            self.play(FadeIn(xt, shift=LEFT * 0.1), run_time=0.4)
            self.remove(xt)
            ver_cmd.add(xt)
            self.add(ver_cmd)
            vo.wait_until("which Python")
            ver = t.print(self, [ver_cap], run_time=0.3)[0]
            vo.wait_until("It's 3.14.7")
            num = substring(ver, "3.14.7")
            self.play(num.animate.set_color(TURN), run_time=0.3)
            self.play(Indicate(num, color=TURN, scale_factor=1.25), run_time=0.7)
            self.add(ver)
            vo.wait_until("Yet the recipe")
            # strip: Output line, the --version line (with its tag), the answer
            resize(self, t, 3, run_time=0.8,
                   extra=[prev.animate.move_to([prev.get_center()[0], STRIP_TOP + 0.06 + prev.height / 2, 0])])
            self.play(FadeIn(panel, shift=RIGHT * 0.8), run_time=0.8)
            vo.wait_until("starts from Python")
            self.play(span.animate.set_color(SYSTEM), Create(ul), run_time=0.5)
            # 3.14.7 rises out of the strip to the right of the panel, a "?" between the two
            self.play(TransformFromCopy(num, num_up), Indicate(span, color=SYSTEM, scale_factor=1.1),
                      run_time=0.8)
            self.play(FadeIn(q, scale=0.6), run_time=0.35)
            vo.wait_until("Hold that thought")
            self.play(Wiggle(q, scale_value=1.3), run_time=1.0)

        # ========================================================== 3. the V1 ladder
        lad = Ladder().move_to([0.15, -0.05, 0])

        def rung(i):
            return lad.rungs[i]

        def r_frame(i):
            return lad.rungs[i][0]

        left_x = r_frame(0).get_left()[0] - 0.42
        b_l1 = bracket(r_frame(1).get_top()[1], r_frame(0).get_bottom()[1], left_x, S.GREY)
        l1 = tag("L1", S.GREY).next_to(b_l1, LEFT, buff=0.18)
        b_today = bracket(r_frame(3).get_top()[1], r_frame(2).get_bottom()[1], left_x, TURN)
        today = label("today", 30, TURN).next_to(b_today, LEFT, buff=0.18)
        ring4 = SurroundingRectangle(r_frame(3), color=TURN, buff=0.08, corner_radius=0.14, stroke_width=3)
        hub_shelf = shelf_glyph(0.9)
        hub_lab = label("Docker Hub", 20, CLOUD)
        hub_g = VGroup(hub_lab, hub_shelf).arrange(DOWN, buff=0.12)
        y34 = (lad.icons[2].get_center()[1] + lad.icons[3].get_center()[1]) / 2
        hub_g.shift([lad.rails.get_right()[0] + 1.3 - hub_shelf.get_center()[0], y34 - hub_shelf.get_center()[1], 0])
        push = Arrow(lad.icons[2].get_right() + RIGHT * 0.05, hub_shelf.get_left() + DOWN * 0.18 + LEFT * 0.06,
                     buff=0, path_arc=0.9, color=ROUTE, stroke_width=4, tip_length=0.18,
                     max_tip_length_to_length_ratio=0.3)
        pull = Arrow(hub_shelf.get_left() + UP * 0.18 + LEFT * 0.06, lad.icons[3].get_right() + RIGHT * 0.05,
                     buff=0, path_arc=0.9, color=ROUTE, stroke_width=4, tip_length=0.18,
                     max_tip_length_to_length_ratio=0.3)

        with self.voiceover(SAY[3]) as vo:
            clear_stage(self, run_time=0.6)
            self.play(FadeIn(lad.header, shift=DOWN * 0.1), Create(lad.rails), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(VGroup(r, v), shift=UP * 0.2) for r, v in zip(lad.rungs, lad.veils)],
                                  lag_ratio=0.3), run_time=1.0)
            self.add(lad)
            self.play(Create(ring4), run_time=0.6)
            self.play(ring4.animate(rate_func=there_and_back).set_stroke(width=6), run_time=0.6)
            vo.wait_until("Last lecture")
            self.play(FadeOut(ring4), lad.light(0, 0.6), lad.light(1, 0.6), Create(b_l1),
                      FadeIn(l1, shift=RIGHT * 0.15), run_time=0.8)
            self.remove(ring4)
            vo.wait_until("a manual install")
            self.play(Indicate(rung(0)[2], color=SYSTEM, scale_factor=1.06), run_time=0.8)
            vo.wait_until("then uv")
            self.play(Indicate(rung(1)[2], color=VENV, scale_factor=1.06), run_time=0.8)
            vo.wait_until("Today, the other two")
            self.play(lad.light(2), lad.light(3), Create(b_today), FadeIn(today, shift=RIGHT * 0.15),
                      run_time=0.9)
            vo.wait_until("package the app")
            self.play(Indicate(lad.icons[2], color=IMAGE, scale_factor=1.3), run_time=0.9)
            vo.wait_until("push it to Docker Hub")
            self.play(FadeIn(hub_g, shift=LEFT * 0.2), run_time=0.5)
            self.play(Create(push), run_time=0.7)
            vo.wait_until("and run it on a VM")
            self.play(Create(pull), run_time=0.7)
            self.play(Indicate(lad.icons[3], color=IMAGE, scale_factor=1.3), run_time=0.8)

        # ========================================================== 4. how to follow along
        page = readme_page().move_to([0, 0.2, 0])
        icons = [laptop(0.62, LAPTOP), shelf_glyph(0.62), vm_icon()]
        rows = [("A", SECTION_A, len(STEPS_A)), ("B", SECTION_B, len(STEPS_B)), ("C", SECTION_C, len(STEPS_C))]
        probe = [label(f"{a} · {s} · {n}", 22) for a, s, n in rows]
        chip_w = max(p_.width for p_ in probe) + 1.25
        tchips = VGroup(*[tracker_chip(a, s, n, ic, chip_w) for (a, s, n), ic in zip(rows, icons)])
        tchips.arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        tchips.move_to([-6.4 + tchips.width / 2 + 0.12, 3.42 - tchips.height / 2 - 0.12, 0])
        veils = VGroup(*[Rectangle(width=c.width + 0.04, height=c.height + 0.04, stroke_width=0)
                         .set_fill(S.BG, 0.72).move_to(c) for c in tchips])
        ring = RoundedRectangle(width=tchips.width + 0.24, height=tchips.height + 0.24, corner_radius=0.16,
                                stroke_color=TURN, stroke_width=3).move_to(tchips)
        t2 = term(P_LAPTOP_HOME, rows=2)              # the 2-row preview strip
        t2.shift([0, -2.9 - t2.box.get_bottom()[1], 0])
        prev2 = tag("preview", S.GREY)
        prev2.move_to(t2.box.get_corner(UR) + LEFT * (prev2.width / 2 + 0.35))
        foot = VGroup(label("every command:", 22, S.GREY), mono(GUIDE, 22, INK)).arrange(RIGHT, buff=0.2)
        foot.move_to([0, -3.28, 0])

        with self.voiceover(SAY[4]) as vo:
            clear_stage(self, run_time=0.6)
            vo.wait_until("open the README")
            self.play(FadeIn(page, shift=UP * 0.2), run_time=0.7)
            vo.wait_until("Three trackers")
            # the page flies into the corner and becomes the three trackers (dim until named)
            self.play(page.animate.scale(0.3).move_to(tchips).set_opacity(0),
                      FadeIn(tchips, target_position=page.get_center(), scale=0.6), FadeIn(veils),
                      Create(ring), run_time=1.0)
            self.remove(page)
            for c, v, anchor in zip(tchips, veils, ("on the laptop", "on Docker Hub", "on the VM")):
                vo.wait_until(anchor)
                self.play(FadeOut(v), run_time=0.35)
                self.remove(v)
                self.play(Indicate(c.icon, color=INK, scale_factor=1.3), run_time=0.5)
            self.play(ring.animate(rate_func=there_and_back).set_stroke(width=7), run_time=0.7)
            vo.wait_until("When the yellow")
            self.play(FadeIn(t2), FadeIn(prev2), ring.animate.set_stroke(width=2, opacity=0.5), run_time=0.5)
            l1_ = t2.type(self, IMAGE_LS, type_time=0.7)
            yt = row_tag("▶ your turn", TURN).next_to(l1_.strut, RIGHT, buff=0.45)
            vo.wait_until("tag appears")
            self.play(FadeIn(yt, scale=0.8), run_time=0.45)
            vo.wait_until("pause and run")
            self.play(Indicate(yt, color=TURN, scale_factor=1.15), run_time=0.8)
            vo.wait_until("a gray extra tag")
            t2.set_prompt(P_LAPTOP)
            l2_ = t2.type(self, "ls -a", type_time=0.4)
            xt2 = row_tag("extra").next_to(l2_.strut, RIGHT, buff=0.45)
            self.play(FadeIn(xt2, scale=0.8), run_time=0.45)
            vo.wait_until("isn't in the README")
            self.play(FadeIn(foot, shift=UP * 0.15), run_time=0.6)

        # ========================================================== 5. before you start
        items = [(True, "Docker Desktop running (Tutorial 0)"),
                 (True, "a free Docker Hub account"),
                 (True, "your GCP project, for the VM at the end"),
                 (False, "no service account, no keys")]
        card_rows = VGroup()
        for i, (ok, s) in enumerate(items):
            y = -i * 0.68
            slot = Rectangle(width=0.4, height=0.4, stroke_width=0, fill_opacity=0).move_to([0, y, 0])
            mark = check_mark(0.34, VENV) if ok else cross_mark(0.28, S.GREY).set_stroke(width=4)
            mark.move_to(slot)
            words = label(s, 24, INK if ok else S.GREY)
            words.next_to(slot, RIGHT, buff=0.25)
            words.shift(UP * (y - 0.09 - baseline_y(words, s)))       # common baseline
            txt = VGroup(words)
            if not ok:                                # where the README says so, under the row
                where = VGroup(mono("README.md", 20, S.GREY), label("· line 23", 20, S.GREY))
                where.arrange(RIGHT, buff=0.12).next_to(words, DOWN, buff=0.12, aligned_edge=LEFT)
                txt.add(where)
            r = VGroup(slot, mark, txt)
            r.mark, r.text = mark, txt
            card_rows.add(r)
        card_frame = box(card_rows.width + 0.7, card_rows.height + 0.7, S.GREY, fill_opacity=0.05)
        card_rows.move_to(card_frame)
        card = VGroup(card_frame, card_rows)
        money = tag("a VM costs money while it exists", COST)
        VGroup(card, money).arrange(RIGHT, buff=0.35).move_to(ORIGIN)
        money.match_y(card_rows[2].mark)

        def show_row(r):
            return AnimationGroup(Create(r.mark), FadeIn(r.text, shift=RIGHT * 0.15))

        with self.voiceover(SAY[5]) as vo:
            clear_stage(self, run_time=0.6)
            self.play(FadeIn(card_frame), run_time=0.3)
            self.play(show_row(card_rows[0]), run_time=0.6)
            vo.wait_until("a free Docker Hub account")
            self.play(show_row(card_rows[1]), run_time=0.6)
            vo.wait_until("and your Google Cloud project")
            self.play(show_row(card_rows[2]), run_time=0.6)
            vo.wait_until("for the VM at the end")
            self.play(FadeIn(money, shift=LEFT * 0.2), run_time=0.6)
            vo.wait_until("No service account")
            self.play(show_row(card_rows[3]), run_time=0.7)

        clear_stage(self, run_time=0.8)
