"""S02 · One app, four ways to deploy it — where L14 sits, the lecture's 2x2 (V1) built, two errata.

Beats (script.md "## S02"; one voiceover block each; no tracker in this scene):
0. Lecture 14 · slide 5. Slide 5 redrawn small: a wide GREY arrow with the phases POC, Prototype,
   MVP and dashed boundaries; three thin bars under it (Build better models, ML workflow,
   Deployment, scaling & automation); a dashed YELLOW box over the Prototype block, chip 'you are here'.
1. Slide 6. The roadmap slides up and away; four tiles (1 Data Collector … 4 Model Deploy, our
   shapes); GREEN ticks write into tiles 1-3, tile 4 pulses YELLOW; a GREY 'Milestone 3' card under it.
2. Slides 8-9. The tiles leave; three lines write in one per phrase, each with a tiny moving picture
   (a dashed instance blinking, a struck-through rack, one step of three lighting GOLD). The line
   being spoken is WHITE, the earlier ones dim to GREY.
3. Slides 8-9. Three brackets on a timeline: GREY-dashed LAST WEEK (L13), YELLOW TODAY, GREY-dashed
   NEXT (L15), under the GREY word 'serverless'.
4. Slide 10. V1 DeployGrid built: the faded GREEN lecture sketch, four PINK arrows fan into the 2x2;
   column headers on "Across", row headers on "down", L1/L2 ticks on "top row", today's two cells
   glow YELLOW on "today fills the bottom".
5. Slide 10. README card (README.md · lines 12-17, columns Part / New idea) slides under the grid;
   the card fades and its Part cells turn into the four part chips: 1 under the file cell, 2-4 under
   the container cell; a GREY 'job' tag beside chip 4.
6. The grid folds into its corner icon (bottom right). README card (lines 7-10); 'application code
   around the model' turns GREEN; an ORANGE 'model service' cloud, a GREY-dashed 'Cheese App backend'
   box with an arrow to it.
7. Two GREY erratum cards: the course page's two dead anchors (RED 'no such section today', GREEN
   'start at the top …'); the course map pin 4eaf343 (2025) struck GREY, the README the link serves
   46cc62f · 2026-10-22 in GREEN. Everything fades: empty frame.
"""

import re

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import (CLOUD, COST, ERR, INK, NARRATION, OWN, PAST, SAY_COUNT, SHARED, TURN,
                    DeployGrid, box, card, check_glyph, chip, cross_glyph, cloud_shape, erratum_tag, grid_icon, instance,
                    label, lref, mono, outline_box, rack, readme, readme_card, strike, tag)
from explainer import style as S

SAY = NARRATION["S02"]
GRID_UP = 0.35          # the grid sits a little higher so the README table fits under it (beat 5)
CHIP_NUDGE = 0.12       # part chips 1 and 2 pushed apart (DeployGrid.parts() leaves them touching)


# ------------------------------------------------------------------ pictures of this scene
def roadmap() -> VGroup:
    """Slide 5 redrawn small (our shapes): .arrow .phases .bounds .bars (3) .here .chip"""
    yc, hh = 1.95, 0.34
    pts = [[-6.3, yc + hh, 0], [5.75, yc + hh, 0], [5.75, yc + hh + 0.16, 0], [6.45, yc, 0],
           [5.75, yc - hh - 0.16, 0], [5.75, yc - hh, 0], [-6.3, yc - hh, 0]]
    arr = Polygon(*pts, stroke_color=S.GREY, stroke_width=3).set_fill(S.GREY, 0.22)
    phases = VGroup(*[label(s, 24, INK).move_to([x, yc, 0]) for s, x in (("POC", -4.15), ("Prototype", 0.0),
                                                                          ("MVP", 3.85))])
    bounds = VGroup(*[DashedLine([x, yc - hh - 0.05, 0], [x, -0.05, 0], color=S.GREY, stroke_width=2,
                                 dash_length=0.12) for x in (-2.0, 2.0)])
    bars = VGroup()
    for s, x0, x1, y in (("Build better models", -1.8, 1.8, 0.95), ("ML workflow", -1.8, 1.8, 0.25),
                         ("Deployment, scaling & automation", 0.2, 6.6 - 0.05, -0.45)):
        b = box(x1 - x0, 0.5, S.GREY, fill_opacity=0.15).move_to([(x0 + x1) / 2, y, 0])
        t = label(s, 20, INK).move_to(b)
        if x1 > 2.0:            # the long bar: its words start right of the Prototype box
            t.move_to([2.17, y, 0], aligned_edge=LEFT)
        bars.add(VGroup(b, t))
    here = outline_box(3.9, 3.3, TURN, solid=False, stroke=3).move_to([0, 0.75, 0])
    ch = tag("you are here", TURN).next_to(here, DOWN, buff=0.15)
    g = VGroup(arr, phases, bounds, bars, here, ch).shift(DOWN * 0.45)
    g.arrow, g.phases, g.bounds, g.bars, g.here, g.chip = arr, phases, bounds, bars, here, ch
    return g


def tiles() -> VGroup:
    """Slide 6's four Cheese App parts as our tiles: .tiles[i] (.frame .num .name) .ticks"""
    names = ("Data Collector", "Data Processor", "Model Training", "Model Deploy")
    ts = VGroup()
    for i, n in enumerate(names):
        fr = box(2.75, 1.7, S.GREY, fill_opacity=0.08).move_to([-4.5 + 3.0 * i, 1.0, 0])
        num = VGroup(Circle(radius=0.26, stroke_color=S.GREY, stroke_width=2.5).set_fill(S.BG, 1),
                     label(str(i + 1), 22, INK))
        num[1].move_to(num[0])
        num.move_to(fr.get_center() + UP * 0.32)
        nm = label(n, 22, INK).move_to(fr.get_center() + DOWN * 0.38)
        t = VGroup(fr, num, nm)
        t.frame, t.num, t.name = fr, num, nm
        ts.add(t)
    ticks = VGroup(*[check_glyph(0.34).move_to(t.frame.get_corner(UR) + np.array([-0.3, -0.3, 0]))
                     for t in ts[:3]])
    g = VGroup(ts, ticks)
    g.tiles, g.ticks = ts, ticks
    return g


def blink_instance() -> VGroup:
    return instance(1.1, 0.7)


def three_steps() -> VGroup:
    """Three small steps in a row with arrows; .steps[1] is the one that needs hardware."""
    st = VGroup(*[RoundedRectangle(width=0.42, height=0.42, corner_radius=0.06, stroke_color=S.GREY,
                                   stroke_width=2.5).set_fill(S.GREY, 0.1) for _ in range(3)]).arrange(RIGHT, buff=0.3)
    arrs = VGroup(*[Arrow(st[i].get_right(), st[i + 1].get_left(), buff=0.04, color=S.GREY, stroke_width=2.5,
                          tip_length=0.12, max_tip_length_to_length_ratio=0.5) for i in range(2)])
    g = VGroup(st, arrs)
    g.steps = st
    return g


def bracket(x0: float, x1: float, y: float, color, dashed: bool) -> VMobject:
    """A squared brace under [x0, x1] at y, pointing down (solid or dashed)."""
    xm, d = (x0 + x1) / 2, 0.16
    m = VMobject(stroke_color=color, stroke_width=3)
    m.set_points_as_corners([[x0, y, 0], [x0, y - d, 0], [xm - d, y - d, 0], [xm, y - 2 * d, 0],
                             [xm + d, y - d, 0], [x1, y - d, 0], [x1, y, 0]])
    if dashed:
        m = DashedVMobject(m, num_dashes=int((x1 - x0) * 6), dashed_ratio=0.55).set_stroke(color, 3)
    return m


def week_card(head: str, rows, color, dashed: bool, x: float, y: float) -> VGroup:
    txt = S.GREY if dashed else INK
    c = card([label(r, 20, txt) for r in rows], color, size=20, dashed=dashed, head=head, card_w=3.6)
    if not dashed:
        c.frame.frame.set_stroke(color, 3)
        c.head.set_color(color)
    c.move_to([x, y, 0])
    return c


def readme_table() -> VGroup:
    """README.md · lines 12-17 as a card with the columns Part and New idea only (link markup
    stripped). .parts[i] .ideas[i] .colheads"""
    cols = [[c.strip() for c in readme(n).strip().strip("|").split("|")] for n in range(14, 18)]
    parts = [re.sub(r"\[(.*?)\]\(.*?\)", r"\1", c[0]) for c in cols]
    ideas = [c[2] for c in cols]
    head = [s.strip() for s in readme(12).strip().strip("|").split("|")]
    assert head[0] == "Part" and head[2] == "New idea", head
    x2, pitch = 2.95, 0.36
    ch = VGroup(label("Part", 20, S.GREY).move_to([0, 0, 0], aligned_edge=LEFT),
                label("New idea", 20, S.GREY).move_to([x2, 0, 0], aligned_edge=LEFT))
    pm = VGroup(*[label(p, 20, INK).move_to([0, -(i + 1) * pitch, 0], aligned_edge=LEFT) for i, p in enumerate(parts)])
    im = VGroup(*[label(s, 20, INK).move_to([x2, -(i + 1) * pitch, 0], aligned_edge=LEFT) for i, s in enumerate(ideas)])
    body = VGroup(ch, pm, im)
    c = readme_card((12, 17), body)
    c.parts, c.ideas, c.colheads = pm, im, ch
    return c


def part_chips(g: DeployGrid) -> list:
    """The four part chips where DeployGrid.parts() puts them (built here so the README's Part cells
    can turn into them)."""
    texts = ("1 Deploy a function", "2 Deploy a web app", "3 Add speech", "4 Run a job")
    chips = [chip(t, CLOUD, size=20) for t in texts]
    top = g.cells[1][0].frame.get_bottom()[1] - 0.18
    # both columns' chips are wider than their cells: nudge them apart so chips 1 and 2 don't touch
    chips[0].move_to([g.cells[1][0].frame.get_center()[0] - CHIP_NUDGE, top - chips[0].height / 2, 0])
    y = top
    for c in chips[1:]:
        c.move_to([g.cells[1][1].frame.get_center()[0] + CHIP_NUDGE, y - c.height / 2, 0])
        y -= c.height + 0.1
    return chips


def glyph_slice(t: Text, phrase: str) -> list:
    """The glyphs of `phrase` in a one-line Text (Text has no glyphs for spaces)."""
    flat = t.text.replace(" ", "")
    i = flat.find(phrase.replace(" ", ""))
    assert i >= 0, (phrase, t.text)
    return list(t[i:i + len(phrase.replace(" ", ""))])


class FourWays(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S02"] == 8, len(SAY)

        # ========================================================== 0. slide 5: where this lecture sits
        ref = lref("5")
        rm = roadmap()
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(ref, shift=LEFT * 0.2), DrawBorderThenFill(rm.arrow), run_time=0.9)
            self.play(LaggedStart(*[FadeIn(p, shift=RIGHT * 0.15) for p in rm.phases], lag_ratio=0.3),
                      Create(rm.bounds), run_time=0.9)
            vo.wait_until("inside the prototype phase")
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in rm.bars[:2]], lag_ratio=0.3),
                      run_time=0.7)
            self.play(Create(rm.here.frame), FadeIn(rm.chip, shift=UP * 0.15), rm.phases[1].animate.set_color(TURN),
                      run_time=0.8)
            vo.wait_until("where deployment begins")
            self.play(GrowFromEdge(rm.bars[2], LEFT), run_time=0.8)
            self.play(Indicate(rm.bars[2][1], color=TURN, scale_factor=1.06), run_time=0.8)

        # ========================================================== 1. slide 6: three parts done, deploy left
        tl = tiles()
        ms = card(["deploy your model or API", "using Cloud Functions or Cloud Run"], S.GREY, size=22,
                  head="Milestone 3")
        ms.next_to(tl.tiles, DOWN, buff=0.75).align_to(tl.tiles[3].frame, RIGHT)
        link = Arrow(tl.tiles[3].frame.get_bottom(), [tl.tiles[3].frame.get_center()[0], ms.get_top()[1], 0],
                     buff=0.08, color=S.GREY, stroke_width=3, tip_length=0.16)
        with self.voiceover(SAY[1]) as vo:
            ref2 = lref("6")
            self.play(FadeOut(rm, shift=UP * 1.2), FadeOut(ref), FadeIn(ref2), run_time=0.7)
            self.remove(*rm.get_family())
            ref = ref2
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.2) for t in tl.tiles], lag_ratio=0.2), run_time=1.0)
            vo.wait_until("three are done")
            self.play(LaggedStart(*[Create(k) for k in tl.ticks], lag_ratio=0.3), run_time=0.9)
            vo.wait_until("Model deploy is left")
            self.play(tl.tiles[3].frame.animate.set_stroke(TURN, 4), run_time=0.4)
            self.play(Indicate(tl.tiles[3].name, color=TURN, scale_factor=1.12), run_time=0.8)
            vo.wait_until("and milestone 3 asks")
            self.play(GrowArrow(link), FadeIn(ms, shift=DOWN * 0.15), run_time=0.7)
            vo.wait_until("Cloud Functions or Cloud Run")
            self.play(Indicate(ms.body[1], color=TURN, scale_factor=1.06), run_time=0.9)

        # ========================================================== 2. slides 8-9: what serverless means
        pics = [blink_instance(), rack(0.9), three_steps()]
        texts = ["code runs only when needed", "no servers to set up",
                 "expensive hardware only for the step that needs it"]
        rows = []
        for i, (p, s) in enumerate(zip(pics, texts)):
            y = 1.5 - 1.5 * i
            p.move_to([-4.7, y, 0])
            t = label(s, 26, INK).move_to([-3.6, y, 0], aligned_edge=LEFT)
            rows.append((p, t))
        cut = strike(pics[1], ERR)
        with self.voiceover(SAY[2]) as vo:
            ref2 = lref("8–9")
            self.play(FadeOut(VGroup(tl, ms, link), shift=DOWN * 0.3), FadeOut(ref), FadeIn(ref2), run_time=0.6)
            self.remove(*tl.get_family(), *ms.get_family(), link)
            ref = ref2
            p, t = rows[0]
            self.play(FadeIn(p, scale=0.8), run_time=0.5)
            vo.wait_until("code runs only when needed")
            self.play(Write(t), p.animate(rate_func=there_and_back).set_opacity(0.08), run_time=0.9)
            self.play(p.animate(rate_func=there_and_back).set_opacity(0.08), run_time=0.8)
            vo.wait_until("no servers to set up")
            p, t = rows[1]
            self.play(FadeIn(p), Write(t), rows[0][1].animate.set_color(S.GREY), run_time=0.8)
            self.play(Create(cut), run_time=0.5)
            vo.wait_until("and costly hardware")
            p, t = rows[2]
            self.play(FadeIn(p), Write(t), rows[1][1].animate.set_color(S.GREY), run_time=1.0)
            self.play(p.steps[1].animate.set_fill(COST, 0.8).set_stroke(COST), run_time=0.6)
            self.play(rows[0][0].animate(rate_func=there_and_back).set_opacity(0.08), run_time=0.8)

        # ========================================================== 3. one idea across three weeks
        yt = 0.95
        tline = Arrow([-6.4, yt, 0], [6.45, yt, 0], buff=0, color=S.GREY, stroke_width=3, tip_length=0.2)
        word = label("serverless", 24, S.GREY).move_to([0, yt + 0.45, 0])
        spans = ((-6.2, -2.15, PAST, True, "LAST WEEK", ("Vertex AI", "training job", "L13")),
                 (-1.85, 1.85, TURN, False, "TODAY", ("Cloud Functions", "Cloud Run", "L14")),
                 (2.15, 6.2, PAST, True, "NEXT", ("Vertex AI endpoint", "pipelines", "L15")))
        weeks = []
        for x0, x1, col, dsh, head, rws in spans:
            br = bracket(x0, x1, yt - 0.15, col, dsh)
            wc = week_card(head, rws, col, dsh, (x0 + x1) / 2, yt - 1.75)
            weeks.append(VGroup(br, wc))
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(*[m for r in rows for m in r], cut)), run_time=0.4)
            self.play(GrowArrow(tline), FadeIn(word, shift=DOWN * 0.1), run_time=0.7)
            self.play(Create(weeks[0][0]), FadeIn(weeks[0][1], shift=DOWN * 0.15), run_time=0.7)
            vo.wait_until("today, functions")
            self.play(Create(weeks[1][0]), FadeIn(weeks[1][1], shift=DOWN * 0.15), run_time=0.7)
            vo.wait_until("next week")
            self.play(Create(weeks[2][0]), FadeIn(weeks[2][1], shift=DOWN * 0.15), run_time=0.7)
            self.play(Indicate(weeks[1][1].body, color=TURN, scale_factor=1.06), run_time=0.8)

        # ========================================================== 4. slide 10: the 2x2 built
        g = DeployGrid(built=False).shift(UP * GRID_UP)
        with self.voiceover(SAY[4]) as vo:
            ref2 = lref("10")
            self.play(FadeOut(VGroup(tline, word, *weeks)), FadeOut(ref), FadeIn(ref2), run_time=0.6)
            ref = ref2
            self.play(FadeIn(g, shift=RIGHT * 0.2), run_time=0.7)
            vo.wait_until("four ways to deploy it")
            g.fan(self, run_time=1.8)
            vo.wait_until("Across")
            g.headers(self, "cols", run_time=0.8)
            vo.wait_until("a code file")
            self.play(Indicate(g.cols[0], color=INK, scale_factor=1.1), run_time=0.6)
            g.heal(self)
            vo.wait_until("or a container")
            self.play(Indicate(g.cols[1], color=INK, scale_factor=1.1), run_time=0.6)
            g.heal(self)
            vo.wait_until("down, where it runs")
            g.headers(self, "rows", run_time=0.8)
            vo.wait_until("Lectures 1 and 2")
            g.tick_vm(self, run_time=0.9)
            vo.wait_until("today fills the bottom")
            g.today(self, run_time=0.8)

        # ========================================================== 5. the README's four parts in the bottom row
        tb = readme_table()
        tb.move_to([0.0, -3.55 + tb.height / 2, 0])
        chips = part_chips(g)
        job = tag("job", S.GREY).next_to(chips[3], LEFT, buff=0.15)   # left: on the right it would touch x = 6.6
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeIn(tb, shift=UP * 0.6), run_time=0.8)
            self.play(LaggedStart(*[Indicate(p, color=INK, scale_factor=1.08) for p in tb.parts], lag_ratio=0.25),
                      run_time=1.2)
            vo.wait_until("Part 1 hands over a file")
            # the ideas column leaves first; the card frame keeps holding Parts 2-4 until they move too
            g.show(self, chips[0], anims=[ReplacementTransform(tb.parts[0], chips[0])], run_time=0.8,
                   extra=[FadeOut(VGroup(tb.colheads, tb.ideas)), Indicate(g.cols[0], color=OWN, scale_factor=1.1)])
            vo.wait_until("Parts 2 to 4")
            g.show(self, *chips[1:], anims=[LaggedStart(*[ReplacementTransform(tb.parts[i], chips[i])
                                                          for i in (1, 2, 3)], lag_ratio=0.2)],
                   run_time=1.0, extra=[FadeOut(VGroup(tb.frame, tb.head)),
                                        Indicate(g.cols[1], color=S.TEAL, scale_factor=1.1)])
            self.remove(*tb.get_family())
            g.part_chips = chips
            g.heal(self)
            vo.wait_until("first as a web service")
            self.play(g.pulse_part(1), g.pulse_part(2), run_time=0.8)
            g.heal(self)
            vo.wait_until("then as a job")
            g.show(self, job, anims=[FadeIn(job, shift=RIGHT * 0.15)], run_time=0.5, extra=[g.pulse_part(3)])

        # ========================================================== 6. the application code around the model
        icon = grid_icon(0.36).move_to([5.95, -3.0, 0])
        for c in icon.cells[1]:
            c.frame.set_stroke(TURN)
        body = VGroup(label("We are deploying the application code around the model,", 22, INK),
                      label("not training or hosting the translation model ourselves.", 22, INK)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        rc = readme_card((7, 10), body, quote=True).move_to([0, 1.55, 0])
        phrase = glyph_slice(body[0], "application code around the model")
        model = cloud_shape("model service", SHARED, cloud_w=2.6).move_to([2.9, -1.35, 0])
        backend = outline_box(3.2, 0.95, S.GREY, solid=False)
        backend.add(label("Cheese App backend", 22, INK).move_to(backend))
        backend.move_to([-2.9, -1.35, 0])
        call = Arrow(backend.get_right(), model.get_left(), buff=0.15, color=S.GREY, stroke_width=3, tip_length=0.18)
        with self.voiceover(SAY[6]) as vo:
            frames = [g.cells[r][c].frame for r in range(2) for c in range(2)]
            rest = [m for m in g.submobjects if m not in [g.cells[r][c] for r in range(2) for c in range(2)]]
            rest += [g.cells[r][c].glyph for r in range(2) for c in range(2)]
            self.play(FadeOut(VGroup(*rest)), FadeOut(ref),
                      *[ReplacementTransform(f, ic) for f, ic in zip(frames, [icon.cells[r][c] for r in range(2)
                                                                                for c in range(2)])],
                      run_time=1.0)
            self.remove(*g.get_family())
            self.add(icon)
            self.play(FadeIn(rc, shift=DOWN * 0.2), run_time=0.7)
            vo.wait_until("Not the translation model")
            self.play(FadeIn(model, scale=0.9), run_time=0.7)
            vo.wait_until("which an outside service runs")
            self.play(Indicate(model.text, color=SHARED, scale_factor=1.1), run_time=0.7)
            vo.wait_until("but the application code around it")
            self.play(*[m.animate.set_color(OWN) for m in phrase], run_time=0.7)
            self.add(rc)
            vo.wait_until("Your Cheese App backend")
            self.play(Create(backend[1]), FadeIn(backend[2]), run_time=0.7)
            self.play(GrowArrow(call), run_time=0.6)
            self.play(Indicate(backend[2], color=INK, scale_factor=1.08), run_time=0.7)

        # ========================================================== 7. two small notes (errata)
        old_links = ("…#running-app-as-cloud-function", "…#running-app-in-cloud-run")
        link_rows = []
        for s in old_links:
            m = mono(s, 20, INK)
            x = VGroup(cross_glyph(0.22), label("no such section today", 20, ERR))
            x.arrange(RIGHT, buff=0.12)
            link_rows.append(VGroup(m, x))
        lw = max(r[0].width for r in link_rows)
        for r in link_rows:
            r[1].next_to(r[0], RIGHT, buff=0.4).align_to(r[0], LEFT).shift(RIGHT * (lw + 0.4))
        fix = VGroup(Arrow(LEFT * 0.3, RIGHT * 0.3, buff=0, color=OWN, stroke_width=4, tip_length=0.16),
                     label("start at the top · Part 1 = function · Parts 2–4 = Cloud Run", 20, OWN)
                     ).arrange(RIGHT, buff=0.15)
        c1 = card([*link_rows, fix], S.GREY, size=20, head="the course page's links", buff=0.2)
        pin_old = VGroup(label("course map pin", 20, S.GREY), mono("4eaf343", 20, S.GREY), label("(2025)", 20, S.GREY)
                         ).arrange(RIGHT, buff=0.14)
        pin_new = VGroup(label("README the link serves:", 20, OWN), mono("46cc62f", 20, OWN),
                         label("· 2026-10-22", 20, OWN)).arrange(RIGHT, buff=0.14)
        c2 = card([pin_old, pin_new], S.GREY, size=20, head="which README", buff=0.2, card_w=c1.width)
        VGroup(c1, c2).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to([-0.5, -0.1, 0])
        tags = []
        for c in (c1, c2):
            et = erratum_tag()
            et.move_to(c.frame.get_corner(UR) + np.array([-et.width / 2 - 0.2, 0, 0]))
            tags.append(et)
        cross_old = strike(pin_old, S.GREY)
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(rc, model, backend, call)), run_time=0.5)
            self.play(FadeIn(c1.frame), FadeIn(c1.head), FadeIn(tags[0]), run_time=0.5)
            vo.wait_until("The course page links")
            self.play(LaggedStart(*[FadeIn(r[0], shift=RIGHT * 0.15) for r in link_rows], lag_ratio=0.3), run_time=0.8)
            vo.wait_until("no longer has")
            self.play(LaggedStart(*[FadeIn(r[1], shift=LEFT * 0.15) for r in link_rows], lag_ratio=0.3), run_time=0.7)
            vo.wait_until("so start at the top")
            self.play(GrowArrow(fix[0]), Write(fix[1]), run_time=1.0)
            vo.wait_until("And we follow the README")
            self.play(FadeIn(c2.frame), FadeIn(c2.head), FadeIn(tags[1]), FadeIn(pin_old, shift=UP * 0.1),
                      run_time=0.6)
            self.play(FadeIn(pin_new, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("not the older commit")
            self.play(Create(cross_old), run_time=0.6)
            self.play(Indicate(pin_new, color=OWN, scale_factor=1.05), run_time=0.7)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
        self.wait(0.3)
