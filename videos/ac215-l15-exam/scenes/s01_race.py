"""S01 · The 2 a.m. race (cold open; then the lecture's question, slides 20–22, and the map).
Lecture: 19–22.

Beats (script.md "## S01", one voiceover block each):
 0  Cold open, no lecture tag; tag `illustration`. An ORANGE clock face at the left; to its right a
    timeline 0:00–4:00 and three WHITE-outlined job boxes prep · 1:00, train · 2:00, deploy · 3:00,
    each hanging from an ORANGE tick (the time is the tick it hangs from). The hands sweep; at each
    tick the box fills YELLOW, then gets a GREEN ✓. A GREY counter top left flips "night 1 … 90".
 1  The counter stops at "night 91". The prep bar grows past the 2:00 tick (to 2:15) while the file
    under it fills from the bottom; at 2:00 train fills YELLOW anyway and an arrow from it reaches
    into the file, only half filled (upper half hatched GREY); the arrow turns RED ("half written").
    Prep finishes the file at 2:15, after the read. At 3:00 deploy fills and ships a small model
    glyph labelled "trained on half the data".
 2  Three GREEN `exit 0` chips pop over the three boxes; a BLUE endpoint box writes in around the
    model, which is outlined RED. Two lines write in: "Nothing failed." (GREEN) "Nothing was right."
    (RED).
 3  LECTURE 20–21. The timeline shrinks away. Our redrawing of slides 20–21: four GREY tiles
    1 Data Collector … 4 Model Deploy, each above a GREY person-at-a-terminal glyph labelled CLI,
    GREY arrows down into a dashed BLUE "Google Cloud" box. The headline "How do we execute these
    steps?" swaps to "Can we automate this flow?"; a hollow arrow points to a BLUE chip
    "Vertex AI Pipelines".
 4  LECTURE 22. The tiles fade. Two phrases write in large: ORANGE "at 2:00" (then crossed out),
    PINK "when prep ✓" beside it; under them a prep box with a GREEN ✓, a PINK arrow to a train
    box, which then runs (YELLOW).
 5  The phrases shrink to the top; the map of the video builds left to right as each item is named:
    graph (three nodes), wires (PINK edge with a GREEN token), overlap (two parallel bars), order
    (four lanes), deployment (a GOLD meter), the Cheese App (a zig-zag of four nodes).
 6  The lecture tag top right pulses once (YELLOW ring); a GREY chip "no live runs · concepts, not
    clicks" writes in under the map.
 7  Map, chips and tag fade. TAKEAWAY "fixed times (cron offsets) → think race: clocks don't know
    about data". Then everything fades to an empty frame.
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    PI,
    RIGHT,
    TAU,
    UP,
    Arc,
    AnimationGroup,
    Arrow,
    Circle,
    Create,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    Line,
    Polygon,
    Rectangle,
    Rotate,
    RoundedRectangle,
    Transform,
    VGroup,
    Write,
    linear,
)

from common import *  # noqa: F401,F403
from explainer import style as S
from explainer.scene import VoiceScene

SAY = NARRATION["S01"]

# ------------------------------------------------------------------ the toy night (illustration)
X0, HOUR = -3.6, 2.4                     # timeline: 0:00 at x = X0, one hour = HOUR units
AXIS_Y = 2.55
ROW_Y = {"prep": 1.45, "train": 0.15, "deploy": -1.1}
JOBS = (("prep", 1, 40), ("train", 2, 50), ("deploy", 3, 45))      # name, start hour, minutes (normal night)
BAR_H = 0.5
PREP_LATE = 75                           # the bad night (script.md S01 SAY 1)
assert PREP_LATE == 75 and 60 + PREP_LATE == 135     # prep 1:00 → 2:15


def tx(h: float, m: float = 0) -> float:
    return X0 + HOUR * (h + m / 60)


def inside(m, msg: str):
    guard(m.get_left()[0] >= -6.6 and m.get_right()[0] <= 6.6 and m.get_bottom()[1] >= -3.6
          and m.get_top()[1] <= 3.6, f"{msg} out of the frame: {m.get_left()}, {m.get_right()}")


def bar_frame(x0: float, x1: float, y: float, color: str = INK, fill=None, op: float = 1.0):
    r = RoundedRectangle(width=x1 - x0, height=BAR_H, corner_radius=0.1, stroke_color=color, stroke_width=2.5)
    r.set_fill(fill or S.BG, op)
    return r.move_to([(x0 + x1) / 2, y, 0])


def job_bar(name: str, h: int, minutes: int) -> VGroup:
    """A job box from its start tick, width = its run time; mono label inside. .frame .title .x0"""
    y = ROW_Y[name]
    fr = bar_frame(tx(h), tx(h, minutes), y)
    t = mono(f"{name}", 22, INK)
    t.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.16)
    g = VGroup(fr, t)
    g.frame, g.title, g.x0, g.name_ = fr, t, tx(h), name
    return g


def badge_at(bar) -> VGroup:
    return ok_badge().move_to(bar.frame.get_right() + LEFT * 0.27)


def hatch(x0, x1, y0, y1, step=0.12, color=S.GREY) -> VGroup:
    """Diagonal hatching clipped to the rectangle [x0, x1] × [y0, y1]."""
    lines = VGroup()
    for c in np.arange(x0 - (y1 - y0), x1, step):         # lines y - y0 = x - c
        a = max(x0, c)
        b = min(x1, c + (y1 - y0))
        if b - a < 0.02:
            continue
        lines.add(Line([a, y0 + a - c, 0], [b, y0 + b - c, 0], stroke_width=1.6, color=color))
    return lines


def half_file(h: float = 0.95) -> VGroup:
    """A page glyph that fills from the bottom: .page .low (lower half) .high (upper half) .hatch"""
    w = h * 0.76
    c = h * 0.26
    page = Polygon([-w / 2, h / 2, 0], [w / 2 - c, h / 2, 0], [w / 2, h / 2 - c, 0], [w / 2, -h / 2, 0],
                   [-w / 2, -h / 2, 0], stroke_color=S.GREY, stroke_width=2.5).set_fill(S.BG, 1)
    inner_w, half = w - 0.12, (h - 0.12) / 2
    low = Rectangle(width=inner_w, height=half, stroke_width=0).set_fill(S.GREY, 0.85)
    low.move_to([0, -h / 2 + 0.06 + half / 2, 0])
    high = low.copy().move_to([0, -h / 2 + 0.06 + 1.5 * half, 0]).stretch_to_fit_width(inner_w - 0.08)
    hx = hatch(-inner_w / 2, inner_w / 2 - c * 0.6, low.get_top()[1] + 0.02, h / 2 - 0.06)
    g = VGroup(page, low, high, hx)
    g.page, g.low, g.high, g.hatch_ = page, low, high, hx
    return g


def person_at_cli() -> VGroup:
    """A GREY person (head + shoulders) at a small laptop, "CLI" under them. .cli"""
    head = Circle(radius=0.15, stroke_color=LAPTOP, stroke_width=3).set_fill(LAPTOP, 0.25)
    sh = Arc(radius=0.3, start_angle=0, angle=PI, stroke_color=LAPTOP, stroke_width=3)
    sh_base = Line(sh.get_left(), sh.get_right(), color=LAPTOP, stroke_width=3)
    body = VGroup(sh, sh_base)
    head.next_to(body, UP, buff=0.05)
    person = VGroup(head, body)
    lt = laptop(0.8, LAPTOP)
    lt.next_to(person, RIGHT, buff=0.08).align_to(person, DOWN)
    fig = VGroup(person, lt)
    cli = mono("CLI", 22, LAPTOP).next_to(fig, DOWN, buff=0.14)
    g = VGroup(fig, cli)
    g.cli = cli
    return g


def hollow_arrow(start, end, w: float = 0.32, head_w: float = 0.62, head_l: float = 0.3,
                 color: str = CLOUD) -> Polygon:
    """An outlined (hollow) block arrow from start to end."""
    start, end = np.array(start, float), np.array(end, float)
    d = end - start
    L = np.linalg.norm(d)
    u = d / L
    n = np.array([-u[1], u[0], 0])
    s = L - head_l
    pts = [start + n * w / 2, start + u * s + n * w / 2, start + u * s + n * head_w / 2, end,
           start + u * s - n * head_w / 2, start + u * s - n * w / 2, start - n * w / 2]
    return Polygon(*pts, stroke_color=color, stroke_width=3).set_fill(S.BG, 0)


# ------------------------------------------------------------------ the map icons (beat 5)
def icon_graph() -> VGroup:
    pts = [np.array([-0.4, 0.3, 0]), np.array([0.4, 0.3, 0]), np.array([0, -0.35, 0])]
    edges = VGroup(*[Line(pts[i], pts[2], color=EDGE, stroke_width=3) for i in (0, 1)])
    nodes = VGroup(*[Circle(radius=0.16, stroke_color=INK, stroke_width=2.5).set_fill(S.BG, 1).move_to(p)
                     for p in pts])
    return VGroup(edges, nodes)


def icon_wires() -> VGroup:
    a = RoundedRectangle(width=0.36, height=0.3, corner_radius=0.06, stroke_color=INK, stroke_width=2.5)
    b = a.copy()
    a.move_to([-0.55, 0, 0])
    b.move_to([0.55, 0, 0])
    w = Line(a.get_right(), b.get_left(), color=EDGE, stroke_width=4)
    tok = Circle(radius=0.09, stroke_color=OWN, stroke_width=2).set_fill(OWN, 0.9).move_to(w)
    return VGroup(w, a, b, tok)


def icon_overlap() -> VGroup:
    b1 = Rectangle(width=1.1, height=0.22, stroke_color=TURN, stroke_width=2).set_fill(TURN, 0.5)
    b2 = Rectangle(width=0.8, height=0.22, stroke_color=TURN, stroke_width=2).set_fill(TURN, 0.5)
    b2.next_to(b1, DOWN, buff=0.16).align_to(b1, LEFT)
    return VGroup(b1, b2).move_to([0, 0, 0])


def icon_order() -> VGroup:
    g = VGroup()
    for i, (a, b) in enumerate(((0.0, 0.35), (0.1, 0.55), (0.3, 0.75), (0.45, 1.0))):
        y = 0.36 - i * 0.24
        g.add(Line([-0.55, y, 0], [0.55, y, 0], color=S.GREY, stroke_width=1.5))
        g.add(Rectangle(width=(b - a) * 1.1, height=0.13, stroke_width=0).set_fill(OWN if i == 3 else CLOCK, 0.8)
              .move_to([-0.55 + (a + b) / 2 * 1.1, y, 0]))
    return g


def icon_meter() -> VGroup:
    m = gold_meter(0.42)
    m.remove(m[-1])                    # the "$ / hour" caption: the map label says "deployment"
    return m.move_to([0, 0, 0])


def icon_cheese() -> VGroup:
    pts = [np.array([-0.6 + 0.4 * i, 0.22 if i % 2 == 0 else -0.22, 0]) for i in range(4)]
    edges = VGroup(*[Line(pts[i], pts[i + 1], color=EDGE, stroke_width=3) for i in range(3)])
    nodes = VGroup(*[RoundedRectangle(width=0.26, height=0.22, corner_radius=0.05, stroke_color=CTR, stroke_width=2.5)
                     .set_fill(S.BG, 1).move_to(p) for p in pts])
    return VGroup(edges, nodes)


class Race(VoiceScene):
    def construct(self):
        assert len(SAY) == 8, len(SAY)

        # ========================================================== 0 · three nightly jobs on a clock
        clock = ClockFace(r=0.9, hour=0, minute=45).move_to([-5.25, 0.9, 0])
        ill = illustration_tag().next_to(clock, DOWN, buff=0.45)
        axis = Line([tx(0) - 0.15, AXIS_Y, 0], [tx(4) + 0.15, AXIS_Y, 0], color=CLOCK, stroke_width=3)
        ticks = VGroup(*[Line([tx(h), AXIS_Y - 0.1, 0], [tx(h), AXIS_Y + 0.1, 0], color=CLOCK, stroke_width=3)
                         for h in range(5)])
        tlabels = VGroup(*[mono(f"{h}:00", 22, CLOCK).next_to(ticks[h], UP, buff=0.1) for h in range(5)])
        bars = {name: job_bar(name, h, m) for name, h, m in JOBS}
        hangers = VGroup(*[Line([tx(h), AXIS_Y, 0], [tx(h), ROW_Y[name] + BAR_H / 2, 0], color=CLOCK,
                                stroke_width=3) for name, h, _ in JOBS])
        timeline = VGroup(axis, ticks, tlabels)
        night_lbl = label("night", 26, S.GREY)
        night = Counter(None, 1, color=S.GREY, size=26)
        night.next_to(night_lbl, RIGHT, buff=0.15).align_to(night_lbl, DOWN)
        counter = VGroup(night_lbl, night)
        counter.move_to([-6.45 + counter.width / 2, 3.25, 0])
        for m, nm in ((clock, "clock"), (ill, "illustration tag"), (timeline, "timeline"), (counter, "counter"),
                      *[(b, n) for n, b in bars.items()]):
            inside(m, nm)
        guard(clock.get_right()[0] < tlabels[0].get_left()[0] - 0.3, "clock vs timeline")
        guard(counter.get_bottom()[1] > clock.get_top()[1] + 0.3, "counter vs clock")
        badges = {}

        def run_job(name, h, m, vo=None):
            """clock to the start tick, the box fills YELLOW."""
            self.play(*clock.set_time(h, 0), run_time=0.8)
            self.play(bars[name].frame.animate.set_fill(TURN, 0.35).set_stroke(TURN, 3), run_time=0.4)

        def finish_job(name, h, m, run_time=0.8):
            self.play(*clock.set_time(h, m), run_time=run_time)
            badges[name] = badge_at(bars[name])
            self.play(bars[name].frame.animate.set_fill(S.BG, 1).set_stroke(INK, 2.5),
                      FadeIn(badges[name], scale=0.5), run_time=0.4)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(clock, scale=0.8), Create(axis), FadeIn(ticks), FadeIn(tlabels), run_time=1.0)
            self.play(LaggedStart(*[AnimationGroup(Create(hangers[i]), FadeIn(bars[n], shift=DOWN * 0.15))
                                    for i, (n, _, _) in enumerate(JOBS)], lag_ratio=0.3),
                      FadeIn(counter), FadeIn(ill), run_time=1.0)
            vo.wait_until("Prepare the data")
            run_job("prep", 1, 40)
            finish_job("prep", 1, 40)
            vo.wait_until("Train at 2")
            run_job("train", 2, 50)
            finish_job("train", 2, 50, run_time=0.6)
            vo.wait_until("Deploy at 3")
            run_job("deploy", 3, 45)
            finish_job("deploy", 3, 45, run_time=0.6)
            vo.wait_until("For months")
            c = clock.face.get_center()
            self.play(night.count_to(90, run_time=2.4),
                      Rotate(clock.m_hand, angle=-TAU * 12, about_point=c, rate_func=linear),
                      Rotate(clock.h_hand, angle=-TAU, about_point=c, rate_func=linear),
                      LaggedStart(*[Indicate(badges[n], color=OWN, scale_factor=1.35) for n, _, _ in JOBS],
                                  lag_ratio=0.3), run_time=2.4)

        # ========================================================== 1 · night 91: prep takes 75 minutes
        f = half_file().move_to([tx(0, 30), 0.9, 0])
        f_lbl = mono("clean data", 20, S.GREY).next_to(f, UP, buff=0.12)
        late = bar_frame(tx(1), tx(1, PREP_LATE), ROW_Y["prep"], TURN, TURN, 0.35).set_stroke(TURN, 3)
        late.set_fill(TURN, 0.35)
        to_2 = bar_frame(tx(1), tx(2), ROW_Y["prep"], TURN, TURN, 0.35).set_stroke(TURN, 3)
        to_2.set_fill(TURN, 0.35)
        f_hi = f.high.copy()
        f.remove(f.high)
        read = Arrow(bars["train"].frame.get_left() + UP * 0.12, f.get_right() + RIGHT * 0.05, buff=0.08,
                     color=TURN, stroke_width=4, max_tip_length_to_length_ratio=0.15)
        half_lbl = label("half written", 22, ERR).next_to(f, DOWN, buff=0.12)
        model = model_box("model", w=1.15, h=0.55, color=OWN).move_to([5.45, -2.3, 0])
        model_lbl = label("trained on half the data", 22, ERR).next_to(model, DOWN, buff=0.45)
        model_lbl.shift(RIGHT * (min(6.45, model_lbl.get_right()[0]) - model_lbl.get_right()[0]))
        for m, nm in ((f_lbl, "clean data label"), (half_lbl, "half written"), (model, "model"),
                      (model_lbl, "model label"), (late, "late prep bar")):
            inside(m, nm)
        guard(half_lbl.get_right()[0] < bars["train"].frame.get_left()[0] - 0.5, "half written vs train bar")
        guard(f.get_right()[0] < bars["prep"].frame.get_left()[0] - 0.3, "file vs prep bar")
        guard(f_lbl.get_right()[0] < bars["prep"].frame.get_left()[0] - 0.15 and f_lbl.get_top()[1] < AXIS_Y - 0.2, "file label vs prep bar, axis")
        guard(late.get_right()[0] > tx(2) + 0.3, "the late prep bar crosses the 2:00 tick")

        with self.voiceover(SAY[1]) as vo:
            self.play(night.count_to(91, run_time=0.6),
                      *[FadeOut(badges[n], scale=0.5) for n, _, _ in JOBS],
                      FadeIn(f), FadeIn(f_lbl), f.low.animate.set_opacity(0),
                      run_time=0.6)
            self.play(Indicate(counter, color=INK, scale_factor=1.15), run_time=0.6)
            night.freeze()
            vo.wait_until("preparation takes")
            self.play(*clock.set_time(1, 0), run_time=0.7)
            prep_old = bars["prep"].frame
            self.play(Transform(prep_old, bar_frame(tx(1), tx(1, 30), ROW_Y["prep"], TURN, TURN, 0.35)
                                .set_stroke(TURN, 3)),
                      f.low.animate.set_opacity(0.45), run_time=1.0)
            self.play(Transform(prep_old, to_2), *clock.set_time(2, 0), f.low.animate.set_opacity(0.85),
                      run_time=1.6, rate_func=linear)
            vo.wait_until("training starts anyway")
            self.play(bars["train"].frame.animate.set_fill(TURN, 0.35).set_stroke(TURN, 3), run_time=0.5)
            self.play(Create(read), run_time=0.6)
            vo.wait_until("on a file")
            self.play(read.animate.set_color(ERR), FadeIn(half_lbl, shift=UP * 0.1),
                      Indicate(f.hatch_, color=ERR, scale_factor=1.15), run_time=0.8)
            # prep only finishes now, after the read
            self.play(Transform(prep_old, late), *clock.set_time(2, 15), run_time=0.9, rate_func=linear)
            badges["prep"] = badge_at(bars["prep"])
            self.play(prep_old.animate.set_fill(S.BG, 1).set_stroke(INK, 2.5), FadeIn(badges["prep"], scale=0.5),
                      FadeIn(f_hi), FadeOut(f.hatch_), run_time=0.5)
            self.play(*clock.set_time(2, 50), run_time=0.7)
            badges["train"] = badge_at(bars["train"])
            self.play(bars["train"].frame.animate.set_fill(S.BG, 1).set_stroke(INK, 2.5),
                      FadeIn(badges["train"], scale=0.5), run_time=0.4)
            vo.wait_until("deployment ships")
            self.play(*clock.set_time(3, 0), run_time=0.5)
            self.play(bars["deploy"].frame.animate.set_fill(TURN, 0.35).set_stroke(TURN, 3), run_time=0.4)
            dest = model.get_center()
            model.move_to(bars["deploy"].frame)
            self.play(FadeIn(model, scale=0.9), run_time=0.3)
            self.play(model.animate.move_to(dest), run_time=0.8)
            self.play(FadeIn(model_lbl, shift=UP * 0.1), *clock.set_time(3, 45), run_time=0.8)
            badges["deploy"] = badge_at(bars["deploy"])
            self.play(bars["deploy"].frame.animate.set_fill(S.BG, 1).set_stroke(INK, 2.5),
                      FadeIn(badges["deploy"], scale=0.5), run_time=0.4)

        # ========================================================== 2 · every job exits 0
        exits = VGroup(*[chip("exit 0", OWN, size=22, font=MONO).next_to(bars[n].frame, UP, buff=0.08)
                         for n, _, _ in JOBS])
        ep_title = mono("endpoint", 22, INK)
        ep = box(model.width + ep_title.width + 0.75, 1.0, CLOUD, fill_opacity=0.14, radius=0.14, stroke=3)
        ep.move_to(model).align_to(model, RIGHT).shift(RIGHT * 0.2)
        ep_title.move_to(ep).align_to(ep, LEFT).shift(RIGHT * 0.22)
        model_ring = ring(model.frame, ERR, buff=0.08, stroke=4)
        failed = label("Nothing failed.", 34, OWN)
        right = label("Nothing was right.", 34, ERR)
        lines = VGroup(failed, right).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to([-0.4, -2.4, 0])
        for m, nm in ((exits, "exit chips"), (ep, "endpoint"), (lines, "two lines")):
            inside(m, nm)
        guard(lines.get_right()[0] < ep.get_left()[0] - 0.3, "two lines vs endpoint")
        guard(lines.get_top()[1] < bars["deploy"].frame.get_bottom()[1] - 0.2, "two lines vs deploy bar")
        guard(exits[0].get_top()[1] < AXIS_Y - 0.05, "prep exit chip vs axis")
        guard(exits[1].get_bottom()[1] > half_lbl.get_top()[1] - 0.6 or exits[1].get_left()[0] > half_lbl.get_right()[0],
              "train exit chip vs half written")

        with self.voiceover(SAY[2]) as vo:
            self.play(LaggedStart(*[FadeIn(e, scale=0.6) for e in exits], lag_ratio=0.35), run_time=1.2)
            vo.wait_until("Nothing failed")
            self.play(Write(failed), run_time=0.8)
            vo.wait_until("And the endpoint")
            self.play(FadeIn(ep), FadeIn(ep_title), run_time=0.7)
            self.play(Create(model_ring), model.frame.animate.set_stroke(ERR), run_time=0.7)
            vo.wait_until("Nothing was right")
            self.play(Write(right), run_time=0.9)

        # ========================================================== 3 · LECTURE 20–21: four people at four CLIs
        night_scene = VGroup(clock, ill, timeline, hangers, *bars.values(), *badges.values(), counter, f, f_hi,
                             f_lbl, read, half_lbl, model, model_lbl, exits, ep, ep_title, model_ring, lines)
        tiles = VGroup()
        for i, nm in enumerate(CHEESE):
            t = label(f"{i + 1}  {nm}", 22, INK)
            fr = box(2.8, 0.8, LAPTOP, fill_opacity=0.14, radius=0.12, stroke=2.5)
            t.move_to(fr)
            tiles.add(VGroup(fr, t))
        tiles.arrange(RIGHT, buff=0.22).move_to([0, 1.0, 0])
        people = VGroup(*[person_at_cli().next_to(tl, DOWN, buff=0.25) for tl in tiles])
        gcp = box(tiles.width, 0.72, CLOUD, dashed=True, stroke=2.5)
        gcp.move_to([0, people.get_bottom()[1] - 0.95, 0])
        gcp_t = label("Google Cloud", 24, CLOUD).move_to(gcp)
        downs = VGroup(*[Arrow(p.cli.get_bottom(), [p.cli.get_x(), gcp.get_top()[1], 0], buff=0.06,
                               color=LAPTOP, stroke_width=3, max_tip_length_to_length_ratio=0.35)
                         for p in people])
        q1 = label("How do we execute these steps?", 34, INK).move_to([-0.6, 2.45, 0])
        q2 = label("Can we automate this flow?", 34, INK).move_to(q1)
        head = VGroup(q1)
        vtx = chip("Vertex AI Pipelines", CLOUD, size=26)
        vtx.move_to([1.6, gcp.get_bottom()[1] - 0.62, 0])
        harrow = hollow_arrow([vtx.get_left()[0] - 2.2, vtx.get_y(), 0], [vtx.get_left()[0] - 0.12, vtx.get_y(), 0])
        for m, nm in ((tiles, "tiles"), (people, "people"), (gcp, "gcp box"), (q1, "q1"), (vtx, "vertex chip"),
                      (harrow, "hollow arrow")):
            inside(m, nm)
        lr = lref("20–21")
        guard(q1.get_right()[0] < lr.get_left()[0] - 0.1 or q1.get_top()[1] < lr.get_bottom()[1] - 0.05,
              "headline vs lecture tag")
        guard(q1.get_bottom()[1] > tiles.get_top()[1] + 0.2, "headline vs tiles")
        guard(vtx.get_bottom()[1] > -3.55, "vertex chip bottom")

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeIn(lr), FadeOut(night_scene, scale=0.4), run_time=1.0)
            vo.wait_until("four steps")
            self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.2) for t in tiles], lag_ratio=0.25), run_time=1.2)
            vo.wait_until("each run by a person")
            self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.15) for p in people], lag_ratio=0.2),
                      FadeIn(gcp), FadeIn(gcp_t), run_time=1.2)
            self.play(LaggedStart(*[Create(a) for a in downs], lag_ratio=0.2), run_time=0.8)
            vo.wait_until("How do we execute")
            self.play(FadeIn(q1, shift=DOWN * 0.15), run_time=0.7)
            vo.wait_until("Can we automate")
            self.play(*swap_text(head, q1, q2), run_time=0.9)
            self.play(Create(harrow), run_time=0.6)
            self.play(FadeIn(vtx, shift=RIGHT * 0.2), run_time=0.5)

        # ========================================================== 4 · LECTURE 22: not "at 2", but "when prep ✓"
        at2 = mono("at 2:00", 44, CLOCK)
        when_t = label("when prep", 44, EDGE)
        when_b = ok_badge(0.24).next_to(when_t, RIGHT, buff=0.18)
        when = VGroup(when_t, when_b)
        phrases = VGroup(at2, when).arrange(RIGHT, buff=1.4).move_to([0, 0.9, 0])
        x_at = strike(at2, ERR, 6)
        n_prep = TaskNode("prep", outputs=())
        n_train = TaskNode("train", outputs=())
        nodes = VGroup(n_prep, n_train).arrange(RIGHT, buff=2.4).move_to([0, -1.0, 0]).scale(1.25)
        edge = Arrow(n_prep.frame.get_right(), n_train.frame.get_left(), buff=0.1, color=EDGE, stroke_width=5,
                     max_tip_length_to_length_ratio=0.12)
        for m, nm in ((phrases, "phrases"), (nodes, "nodes")):
            inside(m, nm)
        guard(nodes.get_top()[1] < phrases.get_bottom()[1] - 0.6, "nodes vs phrases")

        with self.voiceover(SAY[4]) as vo:
            lr = lref_swap(self, lr, "22")
            self.play(FadeOut(VGroup(tiles, people, gcp, gcp_t, downs, head, harrow, vtx)), run_time=0.8)
            self.play(FadeIn(at2, shift=DOWN * 0.15), run_time=0.6)
            vo.wait_until("Not: train")
            self.play(Create(x_at), at2.animate.set_opacity(0.5), run_time=0.6)
            vo.wait_until("Instead")
            self.play(Write(when_t), FadeIn(when_b, scale=0.5), run_time=0.9)
            self.play(FadeIn(nodes), run_time=0.5)
            self.play(*n_prep.succeed(), run_time=0.5)
            self.play(Create(edge), run_time=0.6)
            vo.wait_until("That is what")
            self.play(*n_train.run(), Indicate(edge, color=EDGE, scale_factor=1.1), run_time=0.8)

        # ========================================================== 5 · the map of the video
        words = VGroup(phrases, x_at)
        icons = [icon_graph(), icon_wires(), icon_overlap(), icon_order(), icon_meter(), icon_cheese()]
        names = ["graph", "wires", "overlap", "order", "deployment", "the Cheese App"]
        anchors = ["graphs", "wires", "overlap", "order", "deployment", "the cheese app"]
        items = VGroup()
        for ic, nm in zip(icons, names):
            lb = label(nm, 24, INK)
            ic.scale(1.35).move_to([0, 0.45, 0])
            lb.move_to([0, -0.55, 0])
            items.add(VGroup(ic, lb))
        widths = [max(it[0].width, it[1].width) for it in items]
        gap = (12.6 - sum(widths)) / (len(items) - 1)
        x = -6.3
        for it, w_ in zip(items, widths):
            it.shift(RIGHT * (x + w_ / 2))
            x += w_ + gap
        for k in range(len(items) - 1):
            guard(items[k][1].get_right()[0] < items[k + 1][1].get_left()[0] - 0.15, f"map labels {k}")
        inside(items, "map")
        words_target = words.copy().scale(0.55).move_to([-0.8, 2.55, 0])
        guard(words_target.get_right()[0] < lr.get_left()[0] - 0.2, "small words vs lecture tag")
        guard(at2.height * 0.55 >= mono("at 2:00", 22).height * 0.98, "shrunk words stay ≥ 22 pt")

        with self.voiceover(SAY[5]) as vo:
            self.play(Transform(words, words_target), FadeOut(VGroup(nodes, edge)), run_time=0.9)
            for it, an in zip(items, anchors):
                vo.wait_until(an)
                self.play(FadeIn(it[0], scale=0.7), FadeIn(it[1], shift=UP * 0.1), run_time=0.45)

        # ========================================================== 6 · the gray tag; no live runs
        nolive = chip("no live runs · concepts, not clicks", S.GREY, size=24)
        nolive.move_to([0, -1.9, 0])
        tag_ring = under(lr.box, TURN, stroke=5, buff=0.08)
        inside(tag_ring, "tag underline")
        inside(nolive, "no live runs chip")

        with self.voiceover(SAY[6]) as vo:
            vo.wait_until("top right")
            self.play(Create(tag_ring), Indicate(lr.text, color=TURN, scale_factor=1.0), run_time=1.0)
            self.play(FadeOut(tag_ring), run_time=0.5)
            vo.wait_until("Nothing here")
            self.play(FadeIn(nolive, shift=UP * 0.15), run_time=0.7)
            self.play(Indicate(nolive, color=INK, scale_factor=1.06), run_time=0.8)

        # ========================================================== 7 · takeaway
        card = takeaway("fixed times (cron offsets) → think race: clocks don't know about data", y=0.0)
        inside(card, "takeaway")

        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(items, words, nolive)), FadeOut(lr), run_time=0.8)
            self.play(*card.write(), run_time=1.4)
            vo.wait_until("a clock knows")
            self.play(Indicate(card.rows, color=TURN, scale_factor=1.04), run_time=0.8)
        self.play(FadeOut(card), run_time=0.8)
        self.wait(0.3)
