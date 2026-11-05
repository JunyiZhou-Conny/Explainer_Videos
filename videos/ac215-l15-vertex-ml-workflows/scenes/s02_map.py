"""S02 · Where we are, in AWS words — the lecture's roadmap and console map, the Vertex AI → AWS
bridge, the sandbox framing, the versions.

Beats (script.md "## S02"; one voiceover block each; no tracker in this scene):
0. Lecture 15 · slides 6–7. Slide 6 redrawn small: a wide GREY arrow with POC, Prototype, MVP;
   three thin bars under it (Build Better Models, ML Workflow, Deployment, Scaling & Automation); an
   unlabelled dashed YELLOW box over the Prototype block. The roadmap slides up and away; four tiles
   (1 Data Collector … 4 Model Deploy, our shapes); GREEN ticks write into tiles 1-3, tile 4 pulses
   YELLOW.
1. Slides 6–7 (held). A YELLOW chip 'part 1' under tile 4; a PINK bracket under all four tiles with
   a PINK chip 'part 2'.
2. Slide 8. The tiles go with their tag. A GREY-dashed card 'L14 · Cloud Run · containers' slides in
   from the left holding a small TEAL container; on "Today" a GREEN model bulb lights inside it and
   'today: the container serves a trained model' writes in; the card parks at the left edge.
3. Slide 10. The card goes with its tag. Slide 10 redrawn as a four-row sidebar under a dashed
   'Vertex AI console' head: Workbench · notebooks, Training · L13 (GREY tick), Online prediction,
   Pipelines; on "today's two" the last two rows light YELLOW one by one.
4. The sidebar goes with its tag. bridge_card builds: its frame and the two column heads ('the
   lecture · Vertex AI' GREY dashed, 'this tutorial · AWS' BLUE); a GREY card under it: the course
   map's GCP repos → the two AWS repos we follow.
5. The three bridge rows write in on their phrases (bucket → S3; service-account key → IAM user +
   access key / role, with a GREY key card and a BLUE role badge under the card; endpoint →
   endpoint configuration + endpoint). The card folds into a text-free mini-legend icon at the lower
   right, which fades.
6. A GREY card 'this recording: no AWS account' with three lines: GREEN laptop steps · real, RED AWS
   calls · honest first error, GREY cloud answers · recorded or a tagged stand-in. A 4-row strip
   types `aws sts get-caller-identity` (extra) and prints laptop/15:3 wrapped, RED. On "Never" a
   RED chip 'faked success' is struck through.
7. The card, strip and chip go. Two version chips with 'at the time of recording', each over its
   capture line as a one-line strip (laptop/00:4, laptop/01:2 to 'aws-cli/2.34.63'). Fade to empty.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import (CLOUD, ERR, IMAGE, INK, LAPTOP, NARRATION, OWN, P_HOME, PAST, ROUTE, SAY_COUNT, TURN,
                    box, bridge_card, capture, card, check_glyph, chip, cut, dashed_chip, extra_row, key_card,
                    label, lref, mono, TERM_BG, outline_box, pin, beside, out, role_badge, strike, strip_term,
                    type_capture, version_chip)
from explainer import style as S

SAY = NARRATION["S02"]


# ------------------------------------------------------------------ pictures of this scene
def roadmap() -> VGroup:
    """Slide 6 redrawn small (our shapes): .arrow .phases .bounds .bars (3) .here (unlabelled)."""
    yc, hh = 1.95, 0.34
    pts = [[-6.3, yc + hh, 0], [5.75, yc + hh, 0], [5.75, yc + hh + 0.16, 0], [6.45, yc, 0],
           [5.75, yc - hh - 0.16, 0], [5.75, yc - hh, 0], [-6.3, yc - hh, 0]]
    arr = Polygon(*pts, stroke_color=S.GREY, stroke_width=3).set_fill(S.GREY, 0.22)
    phases = VGroup(*[label(s, 24, INK).move_to([x, yc, 0]) for s, x in (("POC", -4.15), ("Prototype", 0.0),
                                                                          ("MVP", 3.85))])
    bounds = VGroup(*[DashedLine([x, yc - hh - 0.05, 0], [x, -0.05, 0], color=S.GREY, stroke_width=2,
                                 dash_length=0.12) for x in (-2.0, 2.0)])
    bars = VGroup()
    for s, x0, x1, y in (("Build Better Models", -1.8, 1.8, 0.95), ("ML Workflow", -1.8, 1.8, 0.25),
                         ("Deployment, Scaling & Automation", 0.2, 6.55, -0.45)):
        b = box(x1 - x0, 0.5, S.GREY, fill_opacity=0.15).move_to([(x0 + x1) / 2, y, 0])
        t = label(s, 20, INK).move_to(b)
        if x1 > 2.0:            # the long bar: its words start right of the Prototype box
            t.move_to([2.25, y, 0], aligned_edge=LEFT)
        bars.add(VGroup(b, t))
    here = outline_box(3.8, 2.15, TURN, solid=False, stroke=3).move_to([0, 0.28, 0])   # under the arrow
    g = VGroup(arr, phases, bounds, bars, here).shift(DOWN * 0.55)
    g.arrow, g.phases, g.bounds, g.bars, g.here = arr, phases, bounds, bars, here
    return g


def tiles() -> VGroup:
    """Slide 7's four Cheese App parts as our tiles: .tiles[i] (.frame .num .name) .ticks"""
    names = ("Data Collector", "Data Processor", "Model Training", "Model Deploy")
    ts = VGroup()
    for i, n in enumerate(names):
        fr = box(2.75, 1.7, S.GREY, fill_opacity=0.08).move_to([-4.5 + 3.0 * i, 1.1, 0])
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


def bracket(x0: float, x1: float, y: float, color) -> VMobject:
    """A squared brace under [x0, x1] at y, pointing down."""
    xm, d = (x0 + x1) / 2, 0.16
    m = VMobject(stroke_color=color, stroke_width=4)
    m.set_points_as_corners([[x0, y, 0], [x0, y - d, 0], [xm - d, y - d, 0], [xm, y - 2 * d, 0],
                             [xm + d, y - d, 0], [x1, y - d, 0], [x1, y, 0]])
    return m


def bulb(r: float = 0.24, color=OWN) -> VGroup:
    """A small model bulb (text-free): a glass circle on a short base."""
    glass = Circle(radius=r, stroke_color=color, stroke_width=3).set_fill(color, 0.35)
    base = VGroup(*[Line(LEFT * r * 0.5, RIGHT * r * 0.5, color=color, stroke_width=3) for _ in range(2)])
    base.arrange(DOWN, buff=0.06).next_to(glass, DOWN, buff=0.04)
    return VGroup(glass, base)


def l14_card() -> VGroup:
    """'L14 · Cloud Run · containers': a GREY-dashed card holding a small TEAL container. .frame .head .box"""
    hd = label("L14 · Cloud Run · containers", 22, S.GREY)
    cb = box(3.0, 1.6, IMAGE, fill_opacity=0.15)
    ct = label("container", 22, INK).move_to(cb.get_center() + DOWN * 0.48)
    cont = VGroup(cb, ct)
    inner = VGroup(hd, cont).arrange(DOWN, buff=0.3)
    fr = outline_box(inner.width + 0.7, inner.height + 0.6, PAST, solid=False)
    fr.move_to(inner)
    g = VGroup(fr, inner)
    g.frame, g.head, g.box = fr, hd, cont
    return g


def sidebar() -> VGroup:
    """Slide 10 redrawn as a four-row sidebar (no screenshot). .head .frame .rows[i] (.box .text) .tick"""
    texts = ("Workbench · notebooks", "Training · L13", "Online prediction", "Pipelines")
    rw, rh = 5.0, 0.62
    rows = VGroup()
    for i, s in enumerate(texts):
        b = box(rw, rh, S.GREY, fill_opacity=0.08, radius=0.1).move_to([0, 1.2 - 0.85 * i, 0])
        t = label(s, 24, INK).move_to(b).align_to(b, LEFT).shift(RIGHT * 0.3)
        r = VGroup(b, t)
        r.box, r.text = b, t
        rows.add(r)
    tick = check_glyph(0.32, S.GREY).move_to(rows[1].box.get_right() + LEFT * 0.4)
    fr = outline_box(rw + 0.5, rows.height + 0.5, S.GREY, solid=True, fill_opacity=0.04).move_to(rows)
    hd = dashed_chip("Vertex AI console").next_to(fr, UP, buff=0.2)
    g = VGroup(hd, fr, rows, tick)
    g.head, g.frame, g.rows, g.tick = hd, fr, rows, tick
    return g


def legend_icon() -> VGroup:
    """The bridge card folded: a text-free mini-legend icon (dashed box, three short rows)."""
    fr = outline_box(1.0, 0.72, PAST, solid=False)
    rws = VGroup(*[VGroup(Line(LEFT * 0.3, ORIGIN, color=S.GREY, stroke_width=3),
                          Line(ORIGIN, RIGHT * 0.06, color=S.GREY, stroke_width=0),
                          Line(RIGHT * 0.1, RIGHT * 0.3, color=INK, stroke_width=3)) for _ in range(3)])
    rws.arrange(DOWN, buff=0.12).move_to(fr)
    return VGroup(fr, rws)


def version_strip(s: str) -> VGroup:
    """A capture line as a one-line terminal strip (GREY frame, mono)."""
    t = mono(s, 20, INK)
    b = box(t.width + 0.5, 0.5, S.GREY, fill=TERM_BG,
            fill_opacity=1, radius=0.08)
    t.move_to(b)
    return VGroup(b, t)


class LectureMap(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S02"] == 8, len(SAY)

        # ========================================================== 0. slides 6-7: where this lecture sits
        ref = lref("6–7")
        rm = roadmap()
        tl = tiles()
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(ref, shift=LEFT * 0.2), DrawBorderThenFill(rm.arrow), run_time=0.9)
            self.play(LaggedStart(*[FadeIn(p, shift=RIGHT * 0.15) for p in rm.phases], lag_ratio=0.3),
                      Create(rm.bounds), run_time=0.9)
            vo.wait_until("The course project")
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in rm.bars], lag_ratio=0.3), run_time=0.9)
            self.play(Create(rm.here.frame), rm.phases[1].animate.set_color(TURN), run_time=0.8)
            vo.wait_until("and of the four parts")
            self.play(FadeOut(rm, shift=UP * 1.5), run_time=0.5)
            self.remove(*rm.get_family())
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.2) for t in tl.tiles], lag_ratio=0.1), run_time=0.7)
            vo.wait_until("three are done")
            self.play(LaggedStart(*[Create(k) for k in tl.ticks], lag_ratio=0.3), run_time=0.9)
            vo.wait_until("Model deploy is still open")
            self.play(tl.tiles[3].frame.animate.set_stroke(TURN, 4), run_time=0.4)
            self.play(Indicate(tl.tiles[3].name, color=TURN, scale_factor=1.12), run_time=0.8)

        # ========================================================== 1. part 1 fills tile 4, part 2 connects all four
        p1 = chip("part 1", TURN, size=22).next_to(tl.tiles[3].frame, DOWN, buff=0.3)
        y_br = p1.get_bottom()[1] - 0.3
        br = bracket(tl.tiles[0].frame.get_left()[0], tl.tiles[3].frame.get_right()[0], y_br, ROUTE)
        p2 = chip("part 2", ROUTE, size=22).next_to(br, DOWN, buff=0.2)
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeIn(p1, shift=UP * 0.15), run_time=0.5)
            self.play(Indicate(tl.tiles[3].frame, color=TURN, scale_factor=1.04), run_time=0.8)
            vo.wait_until("Part 2 connects")
            self.play(Create(br), FadeIn(p2, shift=UP * 0.15), run_time=0.8)
            self.play(LaggedStart(*[t.frame.animate.set_stroke(ROUTE, 3) for t in tl.tiles[:3]], lag_ratio=0.2),
                      run_time=0.7)

        # ========================================================== 2. slide 8: last week's containers now serve a model
        lc = l14_card()
        lc.move_to([-2.6, 0.3, 0])
        bl = bulb(0.3).move_to(lc.box[0].get_center() + UP * 0.15)
        today = VGroup(label("today:", 24, OWN), label("the container serves", 24, INK),
                       label("a trained model", 24, INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        today.next_to(lc, RIGHT, buff=0.9)
        with self.voiceover(SAY[2]) as vo:
            ref2 = lref("8")
            self.play(FadeOut(VGroup(tl, p1, br, p2), shift=DOWN * 0.3), FadeOut(ref), run_time=0.6)
            self.remove(*tl.get_family(), *p1.get_family(), br, *p2.get_family())
            ref = ref2
            self.play(FadeIn(ref, shift=LEFT * 0.2), FadeIn(lc, shift=RIGHT * 2.5), run_time=0.9)
            vo.wait_until("put containers on Cloud Run")
            self.play(Indicate(lc.box, color=IMAGE, scale_factor=1.08), run_time=0.8)
            vo.wait_until("Today, the container")
            self.play(GrowFromCenter(bl), run_time=0.6)
            self.play(Write(today), lc.box[0].animate.set_stroke(OWN, 3.5), run_time=1.0)
            self.play(VGroup(lc, bl).animate.shift(LEFT * (lc.get_left()[0] + 6.4)),
                      today.animate.shift(LEFT * (lc.get_left()[0] + 6.4)), run_time=0.7)

        # ========================================================== 3. slide 10: the console's four rows, today's two
        sb = sidebar()
        with self.voiceover(SAY[3]) as vo:
            ref2 = lref("10")
            self.play(FadeOut(VGroup(lc, bl, today), shift=LEFT * 0.4), FadeOut(ref), run_time=0.6)
            self.remove(*lc.get_family(), *bl.get_family(), *today.get_family())
            ref = ref2
            self.play(FadeIn(ref, shift=LEFT * 0.2), FadeIn(sb.head, shift=DOWN * 0.15), FadeIn(sb.frame), run_time=0.7)
            vo.wait_until("notebooks")
            self.play(FadeIn(sb.rows[0], shift=RIGHT * 0.2), run_time=0.5)
            vo.wait_until("training from lecture 13")
            self.play(FadeIn(sb.rows[1], shift=RIGHT * 0.2), run_time=0.5)
            self.play(Create(sb.tick), run_time=0.5)
            vo.wait_until("and today's two")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in sb.rows[2:]], lag_ratio=0.3), run_time=0.7)
            vo.wait_until("online prediction")
            self.play(sb.rows[2].box.animate.set_stroke(TURN, 4).set_fill(TURN, 0.18), run_time=0.5)
            vo.wait_until("and pipelines")
            self.play(sb.rows[3].box.animate.set_stroke(TURN, 4).set_fill(TURN, 0.18), run_time=0.5)

        # ========================================================== 4. the bridge: Vertex AI words, AWS words
        bc = bridge_card()
        bc.move_to([0, 1.25, 0])
        cm1 = label("course map: dlops-io/model-deployment · dlops-io/ml-workflow (GCP)", 20, S.GREY)
        cm2 = label("→ we follow model-deployment-aws · ml-workflow-aws", 20, INK)
        cm = card([cm1, cm2], S.GREY, size=20, buff=0.14)
        cm.next_to(bc, DOWN, buff=0.45)
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(sb, shift=DOWN * 0.3), FadeOut(ref), run_time=0.6)
            self.remove(*sb.get_family(), *ref.get_family())
            self.play(FadeIn(bc.frame), FadeIn(bc.heads[0], shift=DOWN * 0.15), run_time=0.7)
            vo.wait_until("This course also ships")
            self.play(FadeIn(bc.heads[1], shift=DOWN * 0.15), FadeIn(cm.frame), FadeIn(cm1, shift=UP * 0.1),
                      run_time=0.8)
            vo.wait_until("and that is the one we follow")
            self.play(FadeIn(cm2, shift=RIGHT * 0.2), run_time=0.7)
            self.play(Indicate(bc.heads[1], color=CLOUD, scale_factor=1.08), run_time=0.8)
            vo.wait_until("Same ideas, different names")
            self.play(Indicate(bc.heads[0], color=INK, scale_factor=1.06),
                      Indicate(bc.heads[1], color=CLOUD, scale_factor=1.06), run_time=0.9)
            vo.wait_until("I'll point out each one")
            self.play(FadeOut(cm, shift=DOWN * 0.3), run_time=0.6)
            self.remove(*cm.get_family())

        # ========================================================== 5. three rows, then a mini-legend
        kc = key_card("access key · laptop")
        rb = role_badge("role · cloud")
        icons = VGroup(kc, rb).arrange(RIGHT, buff=0.5)
        icons.next_to(bc, DOWN, buff=0.45).align_to(bc.rows[1].right, LEFT)
        icon = legend_icon().move_to([5.9, -3.0, 0])
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeIn(bc.rows[0][0], shift=RIGHT * 0.15), run_time=0.5)
            self.play(FadeIn(bc.rows[0][1]), FadeIn(bc.rows[0][2], shift=RIGHT * 0.2), run_time=0.6)
            vo.wait_until("A service account key")
            self.play(FadeIn(bc.rows[1][0], shift=RIGHT * 0.15), run_time=0.5)
            self.play(FadeIn(bc.rows[1][1]), FadeIn(bc.rows[1][2], shift=RIGHT * 0.2), run_time=0.6)
            vo.wait_until("with a key on your laptop")
            self.play(FadeIn(kc, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("plus a role in the cloud")
            self.play(FadeIn(rb, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("And an endpoint")
            self.play(FadeIn(bc.rows[2][0], shift=RIGHT * 0.15), run_time=0.5)
            self.play(FadeIn(bc.rows[2][1]), FadeIn(bc.rows[2][2], shift=RIGHT * 0.2), run_time=0.6)
        words = VGroup(bc.heads, *bc.rows)
        self.play(FadeOut(icons, shift=DOWN * 0.2), FadeOut(words, shift=DR * 0.5),
                  ReplacementTransform(bc.frame, icon[0]), FadeIn(icon[1]), run_time=0.9)
        self.remove(*bc.get_family(), *icons.get_family())
        self.play(FadeOut(icon), run_time=0.4)
        self.remove(*icon.get_family())

        # ========================================================== 6. the sandbox framing, one honest first error
        l1 = label("laptop steps · real", 22, OWN)
        l2 = label("AWS calls · honest first error", 22, ERR)
        l3 = label("cloud answers · recorded or a tagged stand-in", 22, S.GREY)
        nc = card([l1, l2, l3], S.GREY, size=22, head="this recording: no AWS account", buff=0.18)
        nc.move_to([-2.2, 1.05, 0])
        fk = chip("faked success", ERR, size=22)
        fk.move_to([4.3, 1.05, 0])
        fx = strike(fk, ERR)
        t = strip_term(P_HOME, rows=4)
        c15 = capture("15")
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeIn(nc.frame), FadeIn(nc.head, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("Every step that runs")
            self.play(FadeIn(l1, shift=RIGHT * 0.2), run_time=0.5)
            self.play(Indicate(l1, color=OWN, scale_factor=1.06), run_time=0.6)
            vo.wait_until("Every AWS call stops")
            self.play(FadeIn(l2, shift=RIGHT * 0.2), FadeIn(t), run_time=0.6)
            ln = type_capture(self, t, c15)[0]
            ex = beside(extra_row(), ln)
            pin(self, ln, ex)
            vo.wait_until("like this one")
            out(self, t, c15.at(3), wrap=True, color=ERR)
            vo.wait_until("Where the cloud would answer")
            self.play(FadeIn(l3, shift=RIGHT * 0.2), run_time=0.5)
            vo.wait_until("Never a faked success")
            self.play(FadeIn(fk, scale=0.9), run_time=0.4)
            self.play(Create(fx), run_time=0.5)

        # ========================================================== 7. versions at the time of recording
        v_dock = version_chip("Docker 29.8.2")
        v_aws = version_chip("AWS CLI 2.34.63")
        s_dock = version_strip(capture("00").at(4)[0])
        s_aws = version_strip(cut(capture("01").at(2)[0], "aws-cli/2.34.63"))
        col_d = VGroup(v_dock, s_dock).arrange(DOWN, buff=0.3).move_to([-3.1, 0.3, 0])
        col_a = VGroup(v_aws, s_aws).arrange(DOWN, buff=0.3).move_to([3.1, 0.3, 0])
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(nc, fk, fx, t)), run_time=0.5)
            self.remove(*nc.get_family(), *fk.get_family(), fx, *t.get_family())
            self.play(LaggedStart(FadeIn(col_d, shift=UP * 0.2), FadeIn(col_a, shift=UP * 0.2), lag_ratio=0.35),
                      run_time=1.0)
        self.wait(0.8)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
        self.wait(0.3)
