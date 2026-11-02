"""S08 · Seven rules for the quiz (the recap; slide 40's chain, slide 41's cleanup).
Lecture: 40–41.

Beats (script.md "## S08", one voiceover block each):
 0  Seven empty rule rows (GREY numbers 1–7, faint GREY slots). Row 1 writes in, its thumbnail
    (V1's tracer: four nodes drop into the Y, wires connect) plays its 1-second loop once and holds:
    "pipeline = DAG · a call creates a task"; "a call creates a task" flashes at "Calling".
 1  Rows 2 (V2's token rides a PINK solid wire into the next box) and 3 (the stale sticky note,
    a RED dashed reach into it, RED ✗): "`.output` → edge + this run's value"; "guessed path → no
    edge, maybe stale".
 2  Rows 4 (a PINK dashed wire draws, no token) and 5 (V3's Gantt: prep, two parallel bars, the
    join after the longer): "`.after()` → order, no data"; "no path → parallel · join waits for
    all"; the Gantt thumbnail's longest path flashes at "longest path".
 3  Row 6 (V4's lanes: the ORANGE clock lane's bars collide RED, the edge lane's bars chain GREEN):
    "edges, not clocks · launcher must wait"; "launcher must wait" flashes.
 4  Row 7 (V5's plate and meter: plate appears, the GOLD needle sweeps): "registry → endpoint →
    deploy ($) → predict"; "deploy ($)" flashes GOLD at "Billing"; all seven rows glow YELLOW once
    at "SageMaker".
 5  LECTURE 40. The list (centred until now) shrinks left (text 26 → 20.3 pt). Right: slide 40's chain as an assembly
    line, five boxes top to bottom "recipe (DSL)" → "printed YAML (compiler)" → "operator (SDK)"
    → "engine (Kubeflow)" → "manager (Vertex AI Pipelines)"; a GREEN sheet rides down the line as
    each box lights; TEAL worker glyphs under the last box with "no Kubernetes to set up".
 6  LECTURE 41 (tag only). The chain gives way to the endpoint plate with a running GOLD meter;
    the meter stops as two GREY chips write "undeploy", "delete the endpoint"; everything fades
    except a small GREY line "AC215 · Lecture 15 · exam edition", then an empty frame.
"""

import numpy as np
from manim import (
    DOWN,
    AnimationGroup,
    LEFT,
    PI,
    RIGHT,
    UP,
    Arrow,
    Circle,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    GrowFromEdge,
    Indicate,
    LaggedStart,
    Line,
    MoveAlongPath,
    Rectangle,
    Rotate,
    RoundedRectangle,
    VGroup,
    linear,
)

import common as C
from common import *  # noqa: F401,F403
from explainer import style as S
from explainer.scene import VoiceScene

SAY = NARRATION["S08"]

# ------------------------------------------------------------------ the seven rules (script.md SHOW)
RULES = (
    "pipeline = DAG · a call creates a task",
    "`.output` → edge + this run's value",
    "guessed path → no edge, maybe stale",
    "`.after()` → order, no data",
    "no path → parallel · join waits for all",
    "edges, not clocks · launcher must wait",
    "registry → endpoint → deploy ($) → predict",
)
CHAIN = (                      # slide 40's chain: (role, tool, colour)
    ("recipe", "DSL", TOOL),
    ("printed YAML", "compiler", OWN),
    ("operator", "SDK", TOOL),
    ("engine", "Kubeflow", CLOUD),
    ("manager", "Vertex AI Pipelines", CLOUD),
)
CHAIN_WORDS = ("a recipe", "printed as YAML", "submitted by", "run on the Kubeflow", "and managed by")
assert len(RULES) == 7 and len(CHAIN) == 5

# ------------------------------------------------------------------ layout
SAFE_L, SAFE_R = -6.45, 6.45
ROW_PT = 26                    # rule text; the list later shrinks by SHRINK (26 × 0.78 = 20.3 pt)
SHRINK = 0.78
PITCH = 0.84                   # row pitch
TH_W, TH_H = 1.2, 0.66         # thumbnail frame
END_LINE = "AC215 · Lecture 15 · exam edition"


def place(m, left=None, right=None, top=None, bottom=None, cx=None, cy=None):
    """Move m so the given edge / centre coordinate is where asked."""
    if left is not None:
        m.shift(RIGHT * (left - m.get_left()[0]))
    if right is not None:
        m.shift(RIGHT * (right - m.get_right()[0]))
    if cx is not None:
        m.set_x(cx)
    if top is not None:
        m.shift(UP * (top - m.get_top()[1]))
    if bottom is not None:
        m.shift(UP * (bottom - m.get_bottom()[1]))
    if cy is not None:
        m.set_y(cy)
    return m


def inside(m, l=SAFE_L, r=SAFE_R, b=-3.58, t=3.55):
    guard(m.get_left()[0] >= l and m.get_right()[0] <= r and m.get_bottom()[1] >= b and m.get_top()[1] <= t,
          f"out of the frame: {m.get_left()[0]:.2f} {m.get_right()[0]:.2f} {m.get_bottom()[1]:.2f} "
          f"{m.get_top()[1]:.2f}")


def apart(a, b, gap=0.1, msg=""):
    """a and b do not overlap (their boxes are at least `gap` apart on one axis)."""
    sep = (a.get_right()[0] + gap <= b.get_left()[0] or b.get_right()[0] + gap <= a.get_left()[0]
           or a.get_top()[1] + gap <= b.get_bottom()[1] or b.get_top()[1] + gap <= a.get_bottom()[1])
    guard(sep, f"overlap: {msg}")


def flash(mob, color: str = TURN, k: float = 1.15, run_time: float = 0.6):
    return Indicate(mob, color=color, scale_factor=k, run_time=run_time)


def glyphs(text_mob, plain: str, sub: str) -> VGroup:
    """The glyphs of `sub` inside a Text built from `plain` (Text has no glyphs for spaces)."""
    i = plain.find(sub)
    assert i >= 0, (sub, plain)
    a = len("".join(plain[:i].split()))
    n = len("".join(sub.split()))
    return VGroup(*text_mob.submobjects[a:a + n])


# ------------------------------------------------------------------ thumbnails (shapes only, no text)
def _node(w=0.24, h=0.13, color=INK):
    return RoundedRectangle(width=w, height=h, corner_radius=0.03, stroke_color=color, stroke_width=2)


def _bar(x0, x1, y, color, h=0.09):
    return Rectangle(width=x1 - x0, height=h, stroke_width=0).set_fill(color, 0.9).move_to([(x0 + x1) / 2, y, 0])


def thumb_tracer():
    """V1: the Y of four nodes; loop: they drop in, then the PINK wires connect."""
    pts = [(-0.3, 0.17), (0.3, 0.17), (0.0, -0.02), (0.0, -0.21)]
    nodes = [_node().move_to([x, y, 0]) for x, y in pts]
    wires = [Line(nodes[0].get_bottom(), nodes[2].get_top() + LEFT * 0.05, color=EDGE, stroke_width=2.5),
             Line(nodes[1].get_bottom(), nodes[2].get_top() + RIGHT * 0.05, color=EDGE, stroke_width=2.5),
             Line(nodes[2].get_bottom(), nodes[3].get_top(), color=EDGE, stroke_width=2.5)]
    g = VGroup(*nodes, *wires)

    def loop():
        return seq(LaggedStart(*[FadeIn(n, shift=DOWN * 0.12) for n in nodes], lag_ratio=0.2, run_time=0.55),
                   LaggedStart(*[Create(w) for w in wires], lag_ratio=0.2, run_time=0.45))
    return g, loop


def thumb_token():
    """V2: prep → train on a PINK solid wire; loop: a GREEN token rides it, train turns GREEN."""
    a = _node(0.3, 0.2).move_to([-0.36, 0, 0])
    b = _node(0.3, 0.2).move_to([0.36, 0, 0])
    w = Line(a.get_right(), b.get_left(), color=EDGE, stroke_width=3)
    tok = Dot(radius=0.06, color=OWN).move_to(w.get_start())
    g = VGroup(a, b, w, tok)

    def loop():
        return seq(FadeIn(VGroup(a, b, w), run_time=0.3), FadeIn(tok, run_time=0.1),
                   MoveAlongPath(tok, w.copy(), run_time=0.45),
                   b.animate(run_time=0.15).set_fill(OWN, 0.5))
    return g, loop


def thumb_sticky():
    """The stale sticky note: a GREY note, a RED dashed reach from the task into it, a RED ✗."""
    note_ = RoundedRectangle(width=0.36, height=0.34, corner_radius=0.03, stroke_color=S.GREY,
                             stroke_width=2).set_fill(C._mix(S.GREY, 0.25), 1).rotate(0.08).move_to([-0.33, 0.02, 0])
    lines_ = VGroup(*[Line(LEFT * 0.11, RIGHT * 0.11, color=INK, stroke_width=1.5) for _ in range(2)])
    lines_.arrange(DOWN, buff=0.08).move_to(note_)
    task = _node(0.3, 0.2).move_to([0.36, 0, 0])
    reach = DashedLine(task.get_left(), note_.get_right(), color=ERR, stroke_width=2.5, dash_length=0.05)
    xm = x_mark(0.16).move_to([0.03, 0.17, 0])
    g = VGroup(note_, lines_, task, reach, xm)

    def loop():
        return seq(FadeIn(VGroup(note_, lines_, task), run_time=0.35), Create(reach, run_time=0.35),
                   FadeIn(xm, scale=1.6, run_time=0.3))
    return g, loop


def thumb_dashed():
    """A PINK dashed ordering wire: no token rides it."""
    a = _node(0.3, 0.2).move_to([-0.36, 0, 0])
    b = _node(0.3, 0.2).move_to([0.36, 0, 0])
    w = DashedLine(a.get_right(), b.get_left(), color=EDGE, stroke_width=3, dash_length=0.06)
    g = VGroup(a, b, w)

    def loop():
        return seq(FadeIn(VGroup(a, b), run_time=0.3), Create(w, run_time=0.4),
                   b.animate(run_time=0.3).set_stroke(TURN))
    return g, loop


def thumb_gantt():
    """V3: prep, two parallel trainings, the join after the longer one (bars grow in time order)."""
    x0, u = -0.45, 0.09                       # V3 timings: prep 2, train_a 6, train_b 4, compare 1
    spans = [(0, 2, 0.19), (2, 8, 0.06), (2, 6, -0.07), (8, 9, -0.2)]
    bars = [_bar(x0 + a * u, x0 + b * u, y, OWN) for a, b, y in spans]
    axis = Line([x0 - 0.04, -0.28, 0], [x0 + 10 * u, -0.28, 0], color=S.GREY, stroke_width=1.5)
    g = VGroup(axis, *bars)
    g.longest = VGroup(bars[0], bars[1], bars[3])

    def loop():
        return seq(FadeIn(axis, run_time=0.1),
                   GrowFromEdge(bars[0], LEFT, run_time=0.25, rate_func=linear),
                   AnimationGroup(GrowFromEdge(bars[1], LEFT, rate_func=linear, run_time=0.4),
                                  GrowFromEdge(bars[2], LEFT, rate_func=linear, run_time=0.27)),
                   GrowFromEdge(bars[3], LEFT, run_time=0.15, rate_func=linear))
    return g, loop


def thumb_lanes():
    """V4: the clock lane (ORANGE clock, two bars that collide RED) over the edge lane (three bars
    that chain GREEN)."""
    clock = Circle(radius=0.09, color=CLOCK, stroke_width=2).move_to([-0.43, 0.13, 0])
    hand = Line(clock.get_center(), clock.get_center() + UP * 0.07, color=CLOCK, stroke_width=2)
    top = [_bar(-0.28, 0.12, 0.17, ERR, 0.08), _bar(0.0, 0.42, 0.09, ERR, 0.08)]
    sep = DashedLine([-0.55, -0.01, 0], [0.55, -0.01, 0], color=S.GREY, stroke_width=1, dash_length=0.04)
    link = Line([-0.55, -0.15, 0], [-0.33, -0.15, 0], color=EDGE, stroke_width=2)
    bot = [_bar(-0.3, -0.06, -0.15, OWN, 0.08), _bar(-0.03, 0.27, -0.15, OWN, 0.08),
           _bar(0.3, 0.46, -0.15, OWN, 0.08)]
    g = VGroup(clock, hand, sep, *top, link, *bot)

    def loop():
        return seq(FadeIn(VGroup(clock, hand, sep), run_time=0.15),
                   AnimationGroup(Rotate(hand, angle=-PI, about_point=clock.get_center()),
                                  LaggedStart(*[GrowFromEdge(b, LEFT) for b in top], lag_ratio=0.3),
                                  run_time=0.4),
                   AnimationGroup(Create(link), LaggedStart(*[GrowFromEdge(b, LEFT) for b in bot], lag_ratio=0.8),
                                  run_time=0.45))
    return g, loop


def thumb_plate():
    """V5: the BLUE endpoint plate and the GOLD meter whose needle sweeps once."""
    plate = RoundedRectangle(width=0.5, height=0.26, corner_radius=0.04, stroke_color=CLOUD,
                             stroke_width=2.5).set_fill(C._mix(CLOUD, 0.2), 1).move_to([-0.27, 0, 0])
    bolts = VGroup(*[Dot(radius=0.025, color=CLOUD).move_to(plate.get_corner(c) + (-c) * 0.06)
                     for c in (UP + LEFT, UP + RIGHT, DOWN + LEFT, DOWN + RIGHT)])
    r = 0.2
    hub_at = np.array([0.3, -0.1, 0])
    arc = C._poly([hub_at + np.array([np.cos(a), np.sin(a), 0]) * r for a in np.linspace(PI, 0, 16)], COST, 2.5)
    needle = Line(hub_at, hub_at + LEFT * r * 0.8, color=COST, stroke_width=2.5)
    hub = Dot(hub_at, radius=0.03, color=COST)
    g = VGroup(plate, bolts, arc, needle, hub)

    def loop():
        return seq(FadeIn(VGroup(plate, bolts, arc, hub, needle), run_time=0.3),
                   Rotate(needle, angle=-PI, about_point=hub.get_center(), rate_func=linear, run_time=0.7))
    return g, loop


def seq(*anims):
    """Play anims one after the other; every member starts in its first frame (no early flash)."""
    return AnimationGroup(*anims, lag_ratio=1.0)


THUMBS = (thumb_tracer, thumb_token, thumb_sticky, thumb_dashed, thumb_gantt, thumb_lanes, thumb_plate)


class RuleRow(VGroup):
    """One rule row: GREY number, thumbnail frame (content hidden until .write_in()), rule text
    (hidden until .write_in()) over a faint GREY slot line."""

    def __init__(self, k: int, text: str):
        super().__init__()
        self.plain = text.replace("`", "")
        self.num = label(f"{k + 1}", ROW_PT, S.GREY)
        self.frame = RoundedRectangle(width=TH_W, height=TH_H, corner_radius=0.08, stroke_color=S.GREY,
                                      stroke_width=1.5)
        self.pic, self._loop = THUMBS[k]()
        self.pic.move_to(self.frame)
        rows = fit_rows(text, 10.0, ROW_PT)
        assert len(rows) == 1, rows.row_texts
        self.text = rows[0]
        self.num.move_to(np.array([-0.25, 0, 0]))
        self.frame.next_to(self.num, RIGHT, buff=0.22)
        self.pic.move_to(self.frame)
        self.text.next_to(self.frame, RIGHT, buff=0.3)
        self.slot = None
        self.add(self.num, self.frame, self.pic, self.text)      # the slot line is not a member

    def empty(self) -> VGroup:
        """What the empty row shows: number, frame, slot line (built here, where the row now is)."""
        y = self.frame.get_bottom()[1] + 0.12
        x = self.text.get_left()[0]
        self.slot = Line([x, y, 0], [x + 2.2, y, 0], color=S.GREY, stroke_width=1.5).set_opacity(0.5)
        return VGroup(self.num, self.frame, self.slot)

    def write_in(self, run_time: float = 1.0) -> list:
        """Animations: the slot gives way to the text, the number turns white, the thumbnail plays
        its 1-second loop once (then holds still)."""
        return [FadeOut(self.slot, run_time=0.3),
                self.num.animate(run_time=0.3).set_color(INK),
                FadeIn(self.text, shift=RIGHT * 0.2, run_time=0.8),
                self._loop()]

    def part(self, sub: str) -> VGroup:
        return glyphs(self.text, self.plain, sub)


class Recap(VoiceScene):
    def construct(self):
        assert len(SAY) == 7, len(SAY)

        rows = [RuleRow(k, t) for k, t in enumerate(RULES)]
        top_y = (len(rows) - 1) * PITCH / 2
        for k, r in enumerate(rows):
            r.shift(UP * (top_y - k * PITCH))
        lst = VGroup(*rows)
        place(lst, cx=0.0, cy=0.0)                # centred while it fills; shrinks left in beat 5
        inside(lst)
        for a, b in zip(rows, rows[1:]):
            apart(a, b, 0.05, "rule rows")
        # the thumbnails and texts are not added until write_in (the loops FadeIn / Create / Grow them)
        empty = VGroup(*[r.empty() for r in rows])

        # ========================================================== 0 · seven rows, row 1
        with self.voiceover(SAY[0]) as vo:
            self.play(LaggedStart(*[FadeIn(e, shift=RIGHT * 0.15) for e in empty], lag_ratio=0.1), run_time=1.0)
            vo.wait_until("One")
            self.play(*rows[0].write_in(), run_time=1.0)
            vo.wait_until("Calling a component")
            self.play(flash(rows[0].part("a call creates a task"), TURN, 1.08), run_time=0.7)
            vo.wait_until("Nothing runs")
            self.play(flash(rows[0].pic, TURN, 1.1), run_time=0.7)

        # ========================================================== 1 · rows 2 and 3
        with self.voiceover(SAY[1]) as vo:
            self.play(*rows[1].write_in(), run_time=1.0)
            vo.wait_until("makes the edge")
            self.play(flash(rows[1].part("edge + this run's value"), EDGE, 1.06), run_time=0.7)
            vo.wait_until("Three")
            self.play(*rows[2].write_in(), run_time=1.0)
            vo.wait_until("and may be stale")
            self.play(flash(rows[2].part("maybe stale"), ERR, 1.08), run_time=0.7)

        # ========================================================== 2 · rows 4 and 5
        with self.voiceover(SAY[2]) as vo:
            self.play(*rows[3].write_in(), run_time=1.0)
            vo.wait_until("Five")
            self.play(*rows[4].write_in(), run_time=1.0)
            vo.wait_until("a join waits")
            self.play(flash(rows[4].part("join waits for all"), TURN, 1.06), run_time=0.7)
            vo.wait_until("longest path")
            self.play(flash(rows[4].pic.longest, TURN, 1.2), run_time=0.7)

        # ========================================================== 3 · row 6
        with self.voiceover(SAY[3]) as vo:
            self.play(*rows[5].write_in(), run_time=1.0)
            vo.wait_until("not clocks")
            self.play(flash(rows[5].part("edges, not clocks"), EDGE, 1.06), run_time=0.7)
            vo.wait_until("and a step that launches")
            self.play(flash(rows[5].part("launcher must wait"), TURN, 1.06), run_time=0.7)

        # ========================================================== 4 · row 7, all glow
        with self.voiceover(SAY[4]) as vo:
            self.play(*rows[6].write_in(), run_time=1.0)
            vo.wait_until("Billing starts")
            self.play(flash(rows[6].part("deploy ($)"), COST, 1.1), run_time=0.7)
            vo.wait_until("SageMaker")
            self.play(LaggedStart(*[flash(r.text, TURN, 1.04, 0.5) for r in rows], lag_ratio=0.15), run_time=1.6)

        # ========================================================== 5 · LECTURE 40: the chain
        lst_target = lst.copy().scale(SHRINK)
        place(lst_target, left=SAFE_L + 0.05, cy=-0.1)
        inside(lst_target)
        chain = VGroup()
        boxes = []
        for role, tool, col in CHAIN:
            t = VGroup(label(role, CAPTION, INK), label(f"({tool})", CAPTION, col)).arrange(RIGHT, buff=0.15)
            fr = RoundedRectangle(width=4.2, height=0.58, corner_radius=0.1, stroke_color=col, stroke_width=2.5)
            fr.set_fill(C._mix(col, 0.12), 1)
            t.move_to(fr)
            b = VGroup(fr, t)
            b.frame, b.text = fr, t
            boxes.append(b)
        bx = VGroup(*boxes).arrange(DOWN, buff=0.42)
        arrows = VGroup(*[Arrow(a.get_bottom(), b.get_top(), buff=0.04, color=S.GREY, stroke_width=3,
                                tip_length=0.14, max_tip_length_to_length_ratio=0.5)
                          for a, b in zip(boxes, boxes[1:])])
        workers = VGroup(*[machine_glyph(0.62, CTR) for _ in range(3)]).arrange(RIGHT, buff=0.3)
        workers.next_to(boxes[-1], DOWN, buff=0.22)
        nok = label("no Kubernetes to set up", CAPTION, S.GREY).next_to(workers, DOWN, buff=0.14)
        chain.add(bx, arrows, workers, nok)
        place(chain, right=SAFE_R - 0.1, top=C.LREF_BOTTOM - 0.25)
        inside(chain)
        lr = lref("40")
        apart(chain, lr, 0.05, "chain vs lecture tag")
        apart(chain, lst_target, 0.2, "chain vs shrunk list")
        sheet = RoundedRectangle(width=0.3, height=0.38, corner_radius=0.04, stroke_color=OWN,
                                 stroke_width=2.5).set_fill(C._mix(OWN, 0.3), 1)     # the work item on the line
        sheet.next_to(boxes[0].frame, LEFT, buff=0.15)
        apart(sheet, lst_target, 0.05, "sheet vs list")
        with self.voiceover(SAY[5]) as vo:
            self.play(Transform(lst, lst_target), FadeIn(lr), run_time=0.9)
            for k, (b, word) in enumerate(zip(boxes, CHAIN_WORDS)):
                vo.wait_until(word)
                if k == 0:
                    self.play(FadeIn(b, shift=DOWN * 0.15), FadeIn(sheet, scale=0.6), run_time=0.6)
                else:
                    self.play(FadeIn(arrows[k - 1]), FadeIn(b, shift=DOWN * 0.15),
                              sheet.animate.next_to(b.frame, LEFT, buff=0.15), run_time=0.6)
                self.play(flash(b.text, TURN, 1.1, 0.4))
            vo.wait_until("with no Kubernetes")
            self.play(LaggedStart(*[FadeIn(w, shift=UP * 0.1) for w in workers], lag_ratio=0.2),
                      FadeIn(nok), FadeOut(sheet), run_time=0.9)

        # ========================================================== 6 · LECTURE 41: clean up, end
        plate = endpoint_plate()
        meter = gold_meter()
        pm = VGroup(plate, meter).arrange(RIGHT, buff=0.5)
        place(pm, right=SAFE_R - 0.1, cy=1.0)
        chips = VGroup(chip("undeploy", S.GREY, size=CAPTION), chip("delete the endpoint", S.GREY, size=CAPTION))
        chips.arrange(DOWN, buff=0.22)
        place(chips, cx=pm.get_center()[0], top=pm.get_bottom()[1] - 0.4)
        inside(VGroup(pm, chips))
        apart(VGroup(pm, chips), lst_target, 0.2, "cleanup vs list")
        apart(pm, lref("41"), 0.05, "plate vs lecture tag")
        endline = label(END_LINE, CAPTION, S.GREY).move_to([0, 0, 0])
        with self.voiceover(SAY[6]) as vo:
            lr = lref_swap(self, lr, "41")
            self.play(FadeOut(chain), run_time=0.5)
            self.play(FadeIn(pm, shift=UP * 0.1), meter.run(1.0), run_time=1.0)
            vo.wait_until("undeploy")
            self.play(FadeIn(chips[0], shift=UP * 0.1), meter.stop(0.6), run_time=0.6)
            vo.wait_until("delete the endpoint")
            self.play(FadeIn(chips[1], shift=UP * 0.1), plate.animate.set_opacity(0.3), run_time=0.6)
            vo.wait_until("Good luck")
            self.play(FadeOut(VGroup(lst, pm, chips, lr)), FadeIn(endline), run_time=0.9)
        self.wait(1.0)
        self.play(FadeOut(endline), run_time=0.6)
        self.wait(0.3)
