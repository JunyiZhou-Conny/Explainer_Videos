"""S01 · Why won't pip install? (cold open of AC215 L1).

Beats (script.md, ## S01; one voiceover block each):
0. Black frame. The house terminal (12.6 wide, 11 rows, `ssh · ac215-l01`) fades in at the
   centre with the repo prompt and a blinking cursor; the title flashes BLUE on "in the cloud".
   `pip3 install googletrans==4.0.2 art` folds onto two rows, and the real refusal prints
   (07-pip-refused.txt file lines 2-4, …, 10, …, 21, wrapped: 10 rows, nothing scrolls), the
   `error:` line RED.
1. A GREY extra tag beside the command; the typed command flashes YELLOW on "the one most of us
   would type first"; the RED error line pulses on "The error says"; YELLOW
   underlines sweep under "This environment is externally managed" and "create a virtual
   environment"; on "every line of it" a soft YELLOW reading bar runs down the output.
2. The terminal shrinks into the top-left corner and fades. "virtual" writes large, duplicates
   and the copies slide apart: "virtual machine" (BLUE) over a server-slice glyph (a box whose
   bottom strip is a server's front panel), "virtual environment" (GREEN) over a box of jars; the
   jar box and its label shrink into the slice while the nested pair settles at the centre (V7
   preview).
3. V7 ladder (README.md lines 9-14): rails, then four rungs from the bottom. A YELLOW "today"
   bracket on rungs 1-2; rung 1 lights BLUE, rung 2 GREEN with the GREY note "a fresh VM of the
   same kind" under it, "uv" pulses PURPLE; on "Docker comes next lecture" rungs 3-4 turn GREY
   dashed with an "L2" bracket.
4. "open the README beside this video": a GREY player frame ("this video") and a README page
   glyph beside it; the page flies to the corner and becomes the README tracker (left -6.5, top 3.5
   as in S03-S12, no dot lit) in a pulsing YELLOW ring. Then, piece by piece as named: the cli.py 5-9 code panel (its header circled YELLOW); the
   3-row preview strip at the bottom (tag "preview"): `sudo apt-get update` + ▶ your turn, one `…`
   line (apt's output, elided), `which python` + extra; the study-guide footer.
5. Prerequisites card (✓ Tutorial 0 / ✓ a web browser / ✗ no service account, GREY; rows appear
   as they are spoken, "a GCP project" flashes BLUE) and a GOLD cost tag beside it, level with the
   billing line; everything fades out (empty frame).
"""

import numpy as np
from manim import *

from explainer import style as S
from explainer.devops import (INK, box, cell_width, check_mark, code_panel, cross_mark, glyph_range,
                              label, mono, mono_line, substring, tag)
from explainer.scene import VoiceScene

from common import (CLOUD, COST, ERR, NARRATION, P_HOME, P_REPO, TURN, UV, VENV, capture, excerpt,
                    extra_tag, jars, term, tracker_a, your_turn)

SAY = NARRATION["S01"]

CMD = "pip3 install googletrans==4.0.2 art"
REFUSED = capture("07-pip-refused")            # debian12-part-a
assert REFUSED.cmd == CMD, REFUSED.cmd

# README.md lines 11-14, the four ways (short labels, as the README bolds them)
RUNGS = ["Manual install on the VM", "Same VM, but with uv", "Docker, on your laptop",
         "Run the Docker image on a VM"]


# ------------------------------------------------------------------ small pictures
def underline(line, sub: str, color=TURN) -> Line:
    """A line just under the substring `sub` of a terminal row (under the descenders)."""
    g = substring(line, sub)
    y = line.strut.get_bottom()[1] - 0.015
    return Line([g.get_left()[0] - 0.03, y, 0], [g.get_right()[0] + 0.03, y, 0], color=color,
                stroke_width=4)


def server_slice(w: float = 4.2, h: float = 2.8) -> VGroup:
    """One slice of a server (a VM): a BLUE box whose bottom strip is a server's front panel
    (drive bays, status lights), with an empty body (.body) above it for what lives inside."""
    frame = box(w, h, CLOUD, fill_opacity=0.08, stroke=3)
    sh = 0.5
    sep = Line(frame.get_corner(DL) + UP * sh, frame.get_corner(DR) + UP * sh, color=CLOUD,
               stroke_width=2)
    bays = VGroup(*[RoundedRectangle(width=0.55, height=0.17, corner_radius=0.05, stroke_color=CLOUD,
                                     stroke_width=2) for _ in range(4)]).arrange(RIGHT, buff=0.14)
    bays.move_to(frame.get_corner(DL) + np.array([0.3 + bays.width / 2, sh / 2, 0]))
    lights = VGroup(*[Dot(radius=0.06, color=CLOUD) for _ in range(2)]).arrange(RIGHT, buff=0.12)
    lights.move_to(frame.get_corner(DR) + np.array([-0.4, sh / 2, 0]))
    body = Rectangle(width=w - 0.3, height=h - sh - 0.2, stroke_width=0, fill_opacity=0)
    body.move_to(frame.get_top() + DOWN * (h - sh) / 2)
    g = VGroup(frame, sep, bays, lights, body)
    g.frame, g.body = frame, body
    return g


def jar_box() -> VGroup:
    """A small GREEN box holding four unlabelled GREEN jars (a project's private packages)."""
    js = VGroup(*jars(4, VENV, 0.54)).arrange(RIGHT, buff=0.22)
    frame = box(js.width + 0.6, js.height + 0.5, VENV, fill_opacity=0.08, stroke=3)
    js.move_to(frame)
    g = VGroup(frame, js)
    g.frame, g.jars = frame, js
    return g


def rung(n: int, txt: str, w: float = 6.4, h: float = 0.66) -> VGroup:
    b = box(w, h, S.GREY, fill_opacity=0.05)
    num = label(str(n), 26, S.GREY).move_to(b.get_left() + RIGHT * 0.42)
    t = label(txt, 26, INK).next_to(num, RIGHT, buff=0.32)
    t.shift(UP * (b.get_center()[1] - t.get_center()[1]))
    g = VGroup(b, num, t)
    g.box, g.num, g.text = b, num, t
    return g


def bracket(top: float, bottom: float, x: float, color, side=LEFT, tick: float = 0.2) -> VMobject:
    """A '[' (side=LEFT) or ']' (side=RIGHT) at x from y=top to y=bottom, ticks toward the ladder."""
    d = 1 if side is LEFT or np.allclose(side, LEFT) else -1
    m = VMobject(stroke_color=color, stroke_width=3.5)
    m.set_points_as_corners([[x + d * tick, top, 0], [x, top, 0], [x, bottom, 0], [x + d * tick, bottom, 0]])
    return m


def this_video(w: float = 4.6, h: float = 2.6) -> VGroup:
    """'this video': a GREY player frame with a play triangle and a progress bar, captioned."""
    frame = box(w, h, S.GREY, fill_opacity=0.05)
    play = Triangle(stroke_width=0).set_fill(S.GREY, 0.9).rotate(-PI / 2).scale(0.28).move_to(frame)
    bar = Line(frame.get_corner(DL) + np.array([0.3, 0.3, 0]), frame.get_corner(DR) + np.array([-0.3, 0.3, 0]),
               color=S.GREY_DARK, stroke_width=4)
    done = Line(bar.get_start(), bar.point_from_proportion(0.06), color=S.GREY, stroke_width=4)
    cap = label("this video", 26, S.GREY).next_to(frame, DOWN, buff=0.2)
    return VGroup(frame, play, bar, done, cap)


def readme_page(w: float = 3.0, h: float = 3.4) -> VGroup:
    """The README as a page glyph (not a screenshot): its file name and a few lines of text."""
    frame = RoundedRectangle(width=w, height=h, corner_radius=0.12, stroke_color=S.GREY,
                             stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
    name = mono("README.md", 24, INK).move_to(frame.get_top() + DOWN * 0.42)
    lines = VGroup(*[Line(LEFT * f * (w - 0.7) / 2, RIGHT * f * (w - 0.7) / 2, color=S.GREY_DARK, stroke_width=6)
                     for f in (1, 0.8, 0.95, 0.6, 1, 0.85, 0.7)]).arrange(DOWN, buff=0.26, aligned_edge=LEFT)
    lines.next_to(name, DOWN, buff=0.35).align_to(frame, LEFT).shift(RIGHT * 0.35)
    return VGroup(frame, name, lines)


def text_span(t: Text, s: str, sub: str) -> VGroup:
    """The glyphs of substring `sub` of a Text built from string `s` (spaces have no glyphs)."""
    i = s.index(sub)
    a, n = len("".join(s[:i].split())), len("".join(sub.split()))
    return VGroup(*t[a:a + n])


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

        # ========================================================== 0. pip says no
        t = term(P_REPO, rows=11).move_to(ORIGIN)
        p = P_REPO + " "
        prompt0 = mono_line(p, t.size, INK, t2c=t._prompt_colors(P_REPO))
        t._place(prompt0, 0)
        cw = cell_width(t.size)
        cursor = Rectangle(width=cw * 0.92, height=prompt0.strut.height * 0.86, stroke_width=0) \
            .set_fill(INK, 0.85)
        cursor.move_to([prompt0.strut.get_left()[0] + cw * (len(p) + 0.5), prompt0.strut.get_center()[1], 0])
        out = REFUSED.pick((1, 3), 9, 20)          # file lines 2-4, …, 10, …, 21
        lines = [(out[0], ERR)] + out[1:]

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(t), FadeIn(prompt0), run_time=1.0)
            self.add(cursor)
            vo.wait_until("in the cloud")
            self.play(Indicate(t.title, color=CLOUD, scale_factor=1.25), run_time=1.0)
            # the cursor blinks while the narration says whose machine it is
            while vo.time_until("We ask pip") > 0.9:
                self.play(cursor.animate.set_fill(opacity=0), run_time=0.15)
                self.wait(0.3)
                self.play(cursor.animate.set_fill(opacity=0.85), run_time=0.15)
                self.wait(0.3)
            vo.wait_until("We ask pip")
            self.remove(cursor, prompt0)
            cmd = t.type(self, CMD, type_time=1.7)
            vo.wait_until("pip says no")
            printed = t.print(self, lines, wrap=True, run_time=1.3, lag=0.12)

        # ========================================================== 1. read the refusal
        xtag = extra_tag().next_to(cmd.rows[-1].strut, RIGHT, buff=0.5)
        err_line = t.find("error: externally-managed-environment")
        l4 = t.find("This environment is externally managed")
        l10 = t.find("create a virtual environment")
        u1 = underline(l4, "This environment is externally managed")
        u2 = underline(l10, "create a virtual environment")
        out_rows = [m for m in printed if m.text.strip()]
        bar = Rectangle(width=t.box.width - 0.3, height=t.pitch, stroke_width=0).set_fill(TURN, 0.14)
        bar.move_to([t.box.get_center()[0], out_rows[0].strut.get_center()[1], 0])

        typed = VGroup(*glyph_range(cmd.rows[0], len(P_REPO) + 1), *glyph_range(cmd.rows[1], 0))

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeIn(xtag, shift=LEFT * 0.2), run_time=0.6)
            vo.wait_until("the one most of us")
            self.play(Indicate(typed, color=TURN, scale_factor=1.04), run_time=1.0)
            vo.wait_until("The error says")
            self.play(Indicate(err_line, color=ERR, scale_factor=1.06), run_time=0.9)
            vo.wait_until("externally managed")
            self.play(Create(u1), run_time=0.9)
            vo.wait_until("suggests a virtual")
            self.play(Create(u2), run_time=0.9)
            vo.wait_until("every line of it")
            self.play(FadeIn(bar), run_time=0.25)
            self.play(bar.animate.move_to([bar.get_center()[0], out_rows[-1].strut.get_center()[1], 0]),
                      run_time=2.0, rate_func=linear)
            self.play(FadeOut(bar), run_time=0.3)
            self.remove(bar)

        # ========================================================== 2. the word "virtual", twice
        word = label("virtual", 84, INK).move_to(UP * 0.3)
        vm_t = label("virtual machine", 44, CLOUD).move_to([-3.35, 1.75, 0])
        ve_t = label("virtual environment", 44, VENV).move_to([3.35, 1.75, 0])
        vm_glyph = server_slice().move_to([-3.35, -0.75, 0])
        jb = jar_box().move_to([3.35, -0.75, 0])
        term_parts = VGroup(t, xtag, u1, u2)

        with self.voiceover(SAY[2]) as vo:
            old = list(self.mobjects)
            self.play(term_parts.animate.scale(0.22).move_to([-5.2, 2.9, 0]).set_opacity(0), run_time=1.0)
            self.remove(*old)
            self.play(Write(word), run_time=1.0)
            vo.wait_until("twice")
            left, right = word, word.copy()
            self.add(right)
            self.play(Transform(left, VGroup(*vm_t[:7]).copy().set_color(INK)),
                      Transform(right, VGroup(*ve_t[:7]).copy().set_color(INK)), run_time=0.9)
            vo.wait_until("A virtual machine")
            self.play(left.animate.set_color(CLOUD), Write(VGroup(*vm_t[7:])), run_time=0.8)
            self.remove(left)
            self.add(vm_t)
            vo.wait_until("a whole computer")
            self.play(Create(vm_glyph.frame), run_time=0.8)
            self.play(FadeIn(VGroup(*vm_glyph[1:4]), shift=UP * 0.1), run_time=0.5)
            self.add(vm_glyph)
            vo.wait_until("A virtual environment")
            self.play(right.animate.set_color(VENV), Write(VGroup(*ve_t[7:])), run_time=0.8)
            self.remove(right)
            self.add(ve_t)
            vo.wait_until("a private set")
            self.play(Create(jb.frame), run_time=0.6)
            vo.wait_until("Python packages")
            self.play(LaggedStart(*[FadeIn(j, shift=DOWN * 0.25) for j in jb.jars], lag_ratio=0.25),
                      run_time=1.1)
            self.add(jb)
            vo.wait_until("And one will live")
            # the venv (label and jars) moves into the VM, and the nested pair settles at the centre
            dx = RIGHT * -vm_glyph.get_center()[0]
            s_lab, s_box = 26 / 44, 0.8
            inner = VGroup(ve_t.copy().scale(s_lab), jb.copy().scale(s_box)).arrange(DOWN, buff=0.2)
            inner.move_to(vm_glyph.body).shift(dx)
            self.play(VGroup(vm_t, vm_glyph).animate.shift(dx),
                      ve_t.animate.scale(s_lab).move_to(inner[0]),
                      jb.animate.scale(s_box).move_to(inner[1]), run_time=1.3)

        # ========================================================== 3. the V7 ladder
        pitch, y0 = 1.3, -2.3
        rungs = VGroup(*[rung(i + 1, s) for i, s in enumerate(RUNGS)])
        for i, r in enumerate(rungs):
            r.move_to([0, y0 + i * pitch, 0])
        rail_top, rail_bot = rungs[-1].get_top()[1] + 0.45, rungs[0].get_bottom()[1] - 0.45
        rails = VGroup(*[Line([x, rail_bot, 0], [x, rail_top, 0], color=S.GREY, stroke_width=4)
                         for x in (-3.32, 3.32)])
        head = VGroup(mono("README.md", 22, S.GREY), label("· lines 9–14", 22, S.GREY)).arrange(RIGHT, buff=0.14)
        head.next_to(rails, UP, buff=0.22)
        b_today = bracket(rungs[1].get_top()[1], rungs[0].get_bottom()[1], -3.75, TURN, LEFT)
        today = label("today", 30, TURN).next_to(b_today, LEFT, buff=0.18)
        b_l2 = bracket(rungs[3].get_top()[1], rungs[2].get_bottom()[1], 3.75, S.GREY, RIGHT)
        l2 = tag("L2", S.GREY).next_to(b_l2, RIGHT, buff=0.18)
        note = label("a fresh VM of the same kind", 22, S.GREY)
        note.move_to([0, (rungs[0].get_top()[1] + rungs[1].get_bottom()[1]) / 2, 0])
        dashed = [box(r.box.width, r.box.height, S.GREY, dashed=True).move_to(r.box) for r in rungs[2:]]
        uv_glyphs = VGroup(*rungs[1].text[-2:])

        with self.voiceover(SAY[3]) as vo:
            clear_stage(self, FadeIn(head, shift=DOWN * 0.15), run_time=0.8)
            self.add(head)
            self.play(Create(rails), run_time=0.8)
            vo.wait_until("runs one small app")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.3) for r in rungs], lag_ratio=0.45), run_time=2.8)
            vo.wait_until("Today we climb")
            self.play(Create(b_today), FadeIn(today, shift=RIGHT * 0.15), run_time=0.8)
            vo.wait_until("a manual install")
            self.play(rungs[0].box.animate.set_stroke(CLOUD).set_fill(CLOUD, 0.2),
                      rungs[0].num.animate.set_color(CLOUD), run_time=0.6)
            self.play(Indicate(rungs[0].text, color=INK, scale_factor=1.06), run_time=0.7)
            vo.wait_until("then a fresh VM")
            self.play(rungs[1].box.animate.set_stroke(VENV).set_fill(VENV, 0.2),
                      rungs[1].num.animate.set_color(VENV), run_time=0.6)
            self.play(FadeIn(note, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("with uv")
            self.play(Indicate(uv_glyphs, color=UV, scale_factor=1.3), run_time=0.8)
            vo.wait_until("Docker comes next")
            self.play(*[FadeTransform(r.box, d) for r, d in zip(rungs[2:], dashed)],
                      *[r.text.animate.set_color(S.GREY) for r in rungs[2:]],
                      Create(b_l2), FadeIn(l2, shift=LEFT * 0.15), run_time=0.9)

        # ========================================================== 4. how to follow along
        tr = tracker_a()                           # where S03-S12 pin it: left -6.5, top 3.5
        tr.shift([-6.5 - tr.get_left()[0], 3.5 - tr.get_top()[1], 0])
        ring = RoundedRectangle(width=tr.width + 0.2, height=tr.height + 0.2, corner_radius=0.14,
                                stroke_color=TURN, stroke_width=3).move_to(tr)
        panel = code_panel(excerpt("cli.py", 5, 9), "cli.py", first_line=5)
        panel.shift([-6.3 - panel.get_left()[0], 2.45 - panel.get_top()[1], 0])
        head_ring = SurroundingRectangle(panel.header, color=TURN, buff=0.08, corner_radius=0.08, stroke_width=3)
        t2 = term(P_HOME, rows=3)                  # the 3-row bottom strip of the walkthrough scenes
        t2.shift([0, -2.95 - t2.get_bottom()[1], 0])
        prev = tag("preview", S.GREY)
        prev.move_to(t2.get_corner(UR) + LEFT * (prev.width / 2 + 0.35))
        foot = VGroup(label("every command:", 22, S.GREY),
                      mono("MLOps_Learning · guides/L01-vms-venvs.md", 22, INK)).arrange(RIGHT, buff=0.2)
        foot.move_to([0, -3.3, 0])
        video = this_video().move_to([-2.3, 0.1, 0])
        page = readme_page().move_to([2.75, 0.1, 0])

        with self.voiceover(SAY[4]) as vo:
            clear_stage(self, run_time=0.8)
            self.play(FadeIn(video, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("open the README")
            self.play(FadeIn(page, shift=LEFT * 0.6), run_time=0.8)
            vo.wait_until("The tracker")
            # the README page flies up to the corner and becomes the tracker
            self.play(page.animate.scale(0.25).move_to(tr).set_opacity(0),
                      FadeIn(tr, target_position=page.get_center(), scale=0.8),
                      FadeOut(video), run_time=1.0)
            self.remove(video, page)
            self.play(Create(ring), run_time=0.6)
            for _ in range(2):
                self.play(ring.animate(rate_func=there_and_back).set_stroke(width=6), run_time=0.7)
            vo.wait_until("Code panels")
            self.play(FadeOut(ring), FadeIn(panel, shift=RIGHT * 0.6), run_time=0.8)
            self.remove(ring)
            vo.wait_until("the file and line numbers")
            self.play(Create(head_ring), run_time=0.6)
            vo.wait_until("When the yellow")
            self.play(FadeOut(head_ring), FadeIn(t2), FadeIn(prev), run_time=0.6)
            self.remove(head_ring)
            l1 = t2.type(self, "sudo apt-get update", type_time=0.9)
            yt = your_turn().next_to(l1.strut, RIGHT, buff=0.5)
            vo.wait_until("tag appears")
            self.play(FadeIn(yt, scale=0.8), run_time=0.5)
            t2.print(self, ["…"], run_time=0.3)     # apt's output, elided (script.md: `…` line)
            vo.wait_until("pause and run")
            self.play(Indicate(yt, color=TURN, scale_factor=1.15), run_time=0.8)
            vo.wait_until("A grey extra tag")
            l2_ = t2.type(self, "which python", type_time=0.6)
            xt = extra_tag().next_to(l2_.strut, RIGHT, buff=0.5)
            self.play(FadeIn(xt, scale=0.8), run_time=0.5)
            vo.wait_until("extras are safe")
            self.play(Indicate(xt, color=S.WHITE, scale_factor=1.1), run_time=0.8)
            vo.wait_until("Every command")
            self.play(FadeIn(foot, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("the MLOps Learning repo")
            self.play(Indicate(foot[1], color=S.WHITE, scale_factor=1.06), run_time=0.9)

        # ========================================================== 5. before you start
        items = [(check_mark(0.34, VENV), "Tutorial 0: a GCP project with billing", INK),
                 (check_mark(0.34, VENV), "a web browser", INK),
                 (cross_mark(0.28, S.GREY).set_stroke(width=4), "no service account, no keys today", S.GREY)]
        rows = VGroup()
        for i, (mark, s, col) in enumerate(items):
            # fixed pitch, text on a common baseline (each row starts with a letter that has no
            # descender), so a row with a 'g' or 'y' doesn't push the next one down
            y = -i * 0.68
            slot = Rectangle(width=0.4, height=0.4, stroke_width=0, fill_opacity=0).move_to([0, y, 0])
            mark.move_to(slot)
            txt = label(s, 26, col)
            txt.next_to(slot, RIGHT, buff=0.25)
            txt.shift(UP * (y - 0.1 - txt[0].get_bottom()[1]))
            row = VGroup(slot, mark, txt)
            row.mark, row.text = mark, txt
            rows.add(row)
        card_frame = box(rows.width + 0.7, rows.height + 0.7, S.GREY, fill_opacity=0.05)
        rows.move_to(card_frame)
        card = VGroup(card_frame, rows)
        money = tag("a VM costs money while it exists", COST)
        VGroup(card, money).arrange(RIGHT, buff=0.4).move_to(ORIGIN)
        money.match_y(rows[0].mark)                # level with the billing line

        def show_row(r):
            return AnimationGroup(Create(r.mark), FadeIn(r.text, shift=RIGHT * 0.15))

        with self.voiceover(SAY[5]) as vo:
            clear_stage(self, run_time=0.6)
            self.play(FadeIn(card_frame), run_time=0.4)
            vo.wait_until("finish Tutorial 0")
            self.play(show_row(rows[0]), run_time=0.8)
            vo.wait_until("a Google Cloud project")
            self.play(Indicate(text_span(rows[0].text, items[0][1], "a GCP project"), color=CLOUD,
                               scale_factor=1.08), run_time=0.9)
            vo.wait_until("billing on")
            self.play(FadeIn(money, shift=LEFT * 0.2), run_time=0.6)
            vo.wait_until("No service account")
            self.play(show_row(rows[2]), run_time=0.8)
            vo.wait_until("all you need is a browser")
            self.play(show_row(rows[1]), run_time=0.8)

        clear_stage(self, run_time=0.8)
