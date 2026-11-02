"""S04 · Maximum safe overlap (V3, the wavefront and the Gantt chart).
Lecture: 29, 34, 40.

Beats (script.md "## S04", one voiceover block each):
 0  LECTURE 29. CODE(ml-workflow/src/workflow/cli.py: 297–301) on the left, 298–299 lit; on the right
    the toy graph (Y shape, PINK solid wires). A GREY ✗ between the two square nodes (no wire); both
    fill YELLOW at the same instant.
 1  The panel Transforms into CODE(ml-workflow/src/workflow/sample-pipeline1.yaml: 176, 181–183,
    folded) with 181–183 lit PINK. `square` finishes first (GREEN ✓, 9.0; its token rides to add's
    input and waits there); a GREY label "join" by `add`, which stays WHITE until `square-2` finishes
    (16.0 rides in), then fills YELLOW.
 2  LECTURE 34, 40. The toy and the panel leave. V3 (tag `illustration`): prep → {train_a, train_b} →
    compare in three columns, PINK solid wires; each node flashes as the SAY names it; the empty Gantt
    chart (names + time axis 0–14 min) fades in beneath.
 3  The YELLOW wavefront sweeps the columns; a node lights when every incoming wire carries a token.
    The Gantt grows in time: prep 0–2, train_a 2–8 and train_b 2–6 side by side (train_b's model
    waits in its socket), compare 8–9 with a PINK dashed guide at 8; "9" writes after compare's bar.
 4  An extra PINK dashed wire train_a → train_b on the DAG (`.after()`); a variant row
    `train_b.after(train_a)` slides in under the axis: prep, train_a, train_b, compare chained, ending
    at 13; a GREY chip "same answer, slower".
 5  The dashed wire leaves; compare's two wires turn GREY dotted and two GREY sticky-note paths sit
    by compare; the trainings fill YELLOW (still writing) while compare runs and turns RED. A second
    variant row "guessed paths": compare's bar at 0–1, RED, chip "no edges → starts at 0 → race".
 6  The variant rows fade; the DAG is restored. YELLOW halo on prep → train_a → compare, train_b
    dims, "9" lights. Then train_a turns RED (its bar too) and compare GREY dashed, "never runs".
 7  The canvas clears. PONDER P2 (MCQ card with p2_dag() as its figure, tag `illustration`, 8 s).
 8  Reveal: B fills YELLOW ✓; YELLOW halo on ingest → clean → train_cnn → compare in the figure; the
    sum "2 + 3 + 10 + 1 = 16" writes in GREEN under B; train_tree and report flash GREEN.
 9  RED reasons under A, D and C as the SAY reaches each.
10  The card fades. TAKEAWAY (two rows), each row flashes as the SAY reaches it; empty frame.
"""

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Create,
    FadeIn,
    FadeOut,
    GrowFromEdge,
    Indicate,
    Rectangle,
    ReplacementTransform,
    UpdateFromAlphaFunc,
    linear,
    VGroup,
)

from common import *  # noqa: F401,F403
from explainer import style as S
from explainer.scene import VoiceScene

SAY = NARRATION["S04"]

# ------------------------------------------------------------------ the real sources
CLI = "ml-workflow/src/workflow/cli.py"
YAML = "ml-workflow/src/workflow/sample-pipeline1.yaml"
assert source_line(CLI, 298).strip() == "a_sq_task = square(x=a)", source_line(CLI, 298)
assert source_line(CLI, 299).strip() == "b_sq_task = square(x=b)", source_line(CLI, 299)
assert source_line(CLI, 300).strip() == "sum_task = add(x=a_sq_task.output, y=b_sq_task.output)", \
    source_line(CLI, 300)
assert source_line(YAML, 176).strip() == "add:", source_line(YAML, 176)
assert source_line(YAML, 181).strip() == "dependentTasks:", source_line(YAML, 181)
assert source_line(YAML, 182).strip() == "- square", source_line(YAML, 182)
assert source_line(YAML, 183).strip() == "- square-2", source_line(YAML, 183)
assert TOY_VALUES["square"] == "9.0" and TOY_VALUES["square-2"] == "16.0", TOY_VALUES

# V3 timings (script.md "Notes for scene authors": prep 2, train_a 6, train_b 4, compare 1)
assert V3_TIMES == {"prep": (0, 2), "train_a": (2, 8), "train_b": (2, 6), "compare": (8, 9)}, V3_TIMES
GOOD_TOTAL = 9
SERIAL = [("prep", 0, 2), ("train_a", 2, 8), ("train_b", 8, 12), ("compare", 12, 13)]
SERIAL_TOTAL = 13
assert SERIAL_TOTAL == sum(b - a for _, a, b in SERIAL) == SERIAL[-1][2]

# P2 (script.md PONDER P2; the right answer is B: index 1), re-derived here
P2_Q = "Every task gets its own machine. What is the shortest possible run?"
P2_OPTS = ["22 min", "16 min", "10 min", "20 min"]
P2_ANSWER = 1
_p2 = p2_dag()
assert _p2.longest(P2_MIN) == (16, ["ingest", "clean", "train_cnn", "compare"]), _p2.longest(P2_MIN)
assert sum(P2_MIN.values()) == 22                                       # A: everything in sequence
assert P2_MIN["ingest"] + P2_MIN["clean"] + P2_MIN["train_cnn"] + P2_MIN["train_tree"] + P2_MIN["compare"] == 20  # D
assert max(P2_MIN.values()) == 10                                       # C: the longest single task
assert P2_OPTS[P2_ANSWER] == "16 min"

# ------------------------------------------------------------------ layout
SAFE_L, SAFE_R = -6.45, 6.45
TOP_Y = 2.95                     # under the lecture tag (its bottom is at 3.13)
DAG_Y = 1.95                     # V3's DAG: the middle row of its three columns
GANTT_TOP = 0.8
GANTT_X0 = -2.3                  # x of t = 0 on the Gantt axis


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


def inside(m, l=SAFE_L, r=SAFE_R, b=-3.5, t=3.5):
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


def wrapped_header(p, lines_note: str):
    """Put a panel's "· lines … wrapped" header parts on a second header row (as in S03)."""
    h = p.header
    extras = list(h.submobjects[2:])
    for m in extras:
        h.remove(m)
    row1 = VGroup(*h.submobjects)
    row2 = label(lines_note, CAPTION, S.GREY)
    row2.next_to(row1, DOWN, buff=0.06).align_to(row1, LEFT)
    h.add(row2)
    h.next_to(p.code, UP, buff=0.1).align_to(p.code, LEFT).shift(RIGHT * 0.12)
    return p


def split_header(p):
    """Put a panel's header on two rows: the directory, then the file name and the line note (as in S03)."""
    path = p.source_name
    d, f = path.rsplit("/", 1)
    h = p.header
    rest = list(h.submobjects[1:])
    for m in rest:
        h.remove(m)
    row1 = mono(d + "/", CAPTION, S.GREY)
    row2 = VGroup(mono(f, CAPTION, S.GREY), *rest).arrange(RIGHT, buff=0.12)
    for m in rest:
        m.align_to(row2[0], DOWN)
    new = VGroup(row1, row2).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
    new.next_to(p.code, UP, buff=0.1).align_to(p.code, LEFT).shift(RIGHT * 0.12)
    p.remove(h)
    p.header = new
    p.add(new)
    return p


def note_chip(text: str, color: str = S.GREY, width: float = 6.0, text_color: str = INK):
    """An outlined note: serif rows with `code` mono, wrapped to `width`. .frame .rows"""
    rows = fit_rows(text, width, CAPTION, text_color)
    fr = box(rows.width + 0.4, rows.height + 0.26, color, fill=S.BG, fill_opacity=0.9, radius=0.14)
    rows.move_to(fr)
    g = VGroup(fr, rows)
    g.frame, g.rows = fr, rows
    return g


def bar_at(gt, a, b, y, color, h=0.3):
    """A Gantt-style bar on gt's time scale at height y (for the variant rows under the axis)."""
    w = max(0.02, gt.x_of(b) - gt.x_of(a))
    return Rectangle(width=w, height=h, stroke_color=color, stroke_width=2).set_fill(color, 0.45) \
        .move_to([gt.x_of(a) + w / 2, y, 0])


def grow_part(gt, name, f0, f1):
    """Like Gantt.grow, from fraction f0 to f1 of the bar (a long bar grows in two plays, so the
    node animations between them stay top-level plays: an AnimationGroup holding a node's frame
    re-adds the frame on top of its title)."""
    bar = gt.bar[name]
    a, b = gt.spans[name]
    y = gt.row_y(name)
    gt._flag(bar, False)

    def upd(m, alpha):
        f = f0 + (f1 - f0) * alpha
        m.become(gt._rect(a, a + (b - a) * max(f, 0.002), y, TURN))
    return UpdateFromAlphaFunc(bar, upd, rate_func=linear)


def dim(node, wires, k):
    """Animations: a succeeded node (frame, name, socket, ✓) and its wires to opacity k."""
    out = [node.frame.animate.set_stroke(opacity=k), node.title.animate.set_opacity(k),
           node.sockets.animate.set_stroke(opacity=k), node.ok.animate.set_opacity(k)]
    for w in wires:
        out += [w.line.animate.set_stroke(opacity=k), w.tip.animate.set_fill(opacity=k)]
    return out


class SafeOverlap(VoiceScene):
    def construct(self):
        assert len(SAY) == 11, len(SAY)

        # ========================================================== 0 · no path between the squares → parallel
        pa = src_panel(CLI, 297, 301, wrap={297: ["b: float"], 300: ["y=b_sq"], 301: ["x=sum_task"]})
        wrapped_header(pa, "· lines 297, 300 and 301 wrapped")
        place(pa, left=SAFE_L, top=TOP_Y)
        inside(pa)
        toy = toy_dag("data")
        place(toy, right=SAFE_R, top=TOP_Y - 0.25)
        inside(toy)
        apart(pa, toy, 0.1, "code panel vs toy graph")
        sq, sq2, add, root = (toy.node[n] for n in TOY)
        lit = VGroup(pa.bar(298, TURN), pa.bar(299, TURN))
        gap_x = x_mark(0.3).set_color(S.GREY)
        gap_x.move_to((sq.frame.get_right() + sq2.frame.get_left()) / 2)
        apart(gap_x, sq.frame, 0.05, "no-wire mark vs square")
        apart(gap_x, sq2.frame, 0.05, "no-wire mark vs square-2")
        with self.voiceover(SAY[0]) as vo:
            lr = lref_swap(self, None, "29")
            self.play(FadeIn(pa, shift=RIGHT * 0.2), FadeIn(toy, shift=LEFT * 0.2), run_time=0.9)
            vo.wait_until("No path of wires")
            self.play(FadeIn(lit), flash(sq.frame, INK, 1.08), flash(sq2.frame, INK, 1.08), run_time=0.7)
            vo.wait_until("connects the two square tasks")
            self.play(FadeIn(gap_x, scale=1.4), run_time=0.5)
            vo.wait_until("so Vertex is free")
            self.play(*toy.run("square", "square-2"), FadeOut(gap_x), run_time=0.6)
            vo.wait_until("at the same time")
            self.play(flash(lit, TURN, 1.03), run_time=0.6)

        # ========================================================== 1 · add is a join: it waits for both
        y1 = src_panel(YAML, [(176, 176), (181, 183)])
        split_header(y1)
        place(y1, left=SAFE_L, top=TOP_Y)
        inside(y1)
        apart(y1, toy, 0.15, "YAML panel vs toy graph")
        join = label("join", CAPTION, S.GREY).next_to(add.frame, RIGHT, buff=0.3)
        inside(join)
        with self.voiceover(SAY[1]) as vo:
            self.play(*toy.succeed("square", TOY_VALUES["square"]), run_time=0.6)
            t9 = toy.send(self, "square", "add", TOY_VALUES["square"], run_time=0.9)
            vo.wait_until("Add is a join")
            self.play(FadeIn(join, shift=LEFT * 0.1), flash(add.frame, INK, 1.08), run_time=0.6)
            vo.wait_until("Its YAML lists")
            self.play(FadeOut(lit), ReplacementTransform(pa, y1), run_time=0.8)
            dep = VGroup(*[y1.bar(n, EDGE, 0.3) for n in (181, 182, 183)])
            self.play(FadeIn(dep), run_time=0.4)
            vo.wait_until("both squares")
            self.play(flash(y1.span(182, "square"), EDGE, 1.2), flash(y1.span(183, "square-2"), EDGE, 1.2),
                      toy.wire[("square", "add")].light(EDGE), toy.wire[("square-2", "add")].light(EDGE),
                      run_time=0.8)
            vo.wait_until("so it starts only")
            self.play(flash(t9, OWN, 1.3), run_time=0.6)
            vo.wait_until("the second one finishes")
            self.play(*toy.succeed("square-2", TOY_VALUES["square-2"]), run_time=0.5)
            t16 = toy.send(self, "square-2", "add", TOY_VALUES["square-2"], run_time=0.8)
            self.play(FadeOut(t9, scale=0.6), FadeOut(t16, scale=0.6), *toy.run("add"), run_time=0.6)

        # ========================================================== 2 · the same shape, one size up
        dg = Dag({"prep": (-4.75, DAG_Y), "train_a": (-0.45, DAG_Y + 0.6), "train_b": (-0.45, DAG_Y - 0.6),
                  "compare": (3.95, DAG_Y)},
                 [("prep", "train_a"), ("prep", "train_b"), ("train_a", "compare"), ("train_b", "compare")])
        inside(dg, t=3.0)
        pr, ta, tb, cp = (dg.node[n] for n in ("prep", "train_a", "train_b", "compare"))
        tag3 = illustration_tag()
        place(tag3, left=SAFE_L + 0.05, top=3.5)
        apart(tag3, pr, 0.1, "illustration tag vs prep")
        gt = Gantt([(k, a, b) for k, (a, b) in V3_TIMES.items()], 14, width=12.6, row_h=0.42, name_w=3.9)
        place(gt, top=GANTT_TOP)
        gt.shift(RIGHT * (GANTT_X0 - gt.x_of(0)))           # the name column holds the variant labels too
        cap = gt.axis[3]                                    # "min": left of the "0" label (common.Gantt puts it
        cap.move_to([gt.x_of(0) - 0.35 - cap.width / 2, gt.axis[2][0].get_center()[1], 0])   # on the "14")
        inside(gt)
        seen = VGroup(*[m for n in dg.node.values() for m in (n.frame, n.sockets)])   # the hidden socket labels
        apart(gt, seen, 0.1, "Gantt vs DAG")                                              # never show here
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(toy, y1, dep, join)), run_time=0.6)
            lr = lref_swap(self, lr, "34, 40")
            self.play(FadeIn(dg), FadeIn(tag3), run_time=0.8)
            vo.wait_until("one preprocessing task")
            self.play(flash(pr.frame, INK, 1.1), run_time=0.5)
            vo.wait_until("two trainings")
            self.play(flash(ta.frame, INK, 1.1), flash(tb.frame, INK, 1.1),
                      dg.wire[("prep", "train_a")].light(EDGE), dg.wire[("prep", "train_b")].light(EDGE),
                      run_time=0.7)
            vo.wait_until("and a comparison")
            self.play(flash(cp.frame, INK, 1.1),
                      dg.wire[("train_a", "compare")].light(EDGE), dg.wire[("train_b", "compare")].light(EDGE),
                      run_time=0.7)
            self.play(FadeIn(gt, shift=UP * 0.15), run_time=0.7)

        # ========================================================== 3 · the wavefront and the Gantt grow together
        wf = Wavefront(height=2.2, x=pr.frame.get_left()[0] - 0.4, y=DAG_Y)
        nine = mono(f"{GOOD_TOTAL}", CAPTION, INK).move_to([gt.x_of(GOOD_TOTAL) + 0.3, gt.row_y("compare"), 0])
        inside(nine)
        guide = gt.guide(V3_TIMES["train_a"][1])
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeIn(wf), run_time=0.4)
            self.play(wf.to(pr.frame.get_center()[0], run_time=0.5), *pr.run(), run_time=0.5)
            self.play(gt.grow("prep", run_time=0.8))
            self.play(*pr.succeed("data"), *gt.done("prep"), run_time=0.4)
            ka, kb = pr.token("data"), pr.token("data")
            self.play(FadeIn(ka), FadeIn(kb), run_time=0.2)
            self.play(dg.wire[("prep", "train_a")].ride(ka, 0.8), dg.wire[("prep", "train_b")].ride(kb, 0.8))
            vo.wait_until("Both trainings start together")
            self.play(wf.to(ta.frame.get_center()[0], run_time=0.6), *ta.run(), *tb.run(),
                      FadeOut(ka, scale=0.6), FadeOut(kb, scale=0.6), run_time=0.6)
            k = (V3_TIMES["train_b"][1] - 2) / (V3_TIMES["train_a"][1] - 2)    # train_b ends 4/6 of the way
            self.play(grow_part(gt, "train_a", 0, k), gt.grow("train_b", run_time=1.6), run_time=1.6)
            self.play(grow_part(gt, "train_a", k, 1), *gt.done("train_b"), *tb.succeed("model"), run_time=0.8)
            vo.wait_until("and the comparison starts")
            self.play(*ta.succeed("model"), *gt.done("train_a"), run_time=0.4)
            ma, mb = ta.token("model"), tb.token("model")
            self.play(FadeIn(ma), FadeIn(mb), run_time=0.2)
            self.play(dg.wire[("train_a", "compare")].ride(ma, 0.8), dg.wire[("train_b", "compare")].ride(mb, 0.8),
                      Create(guide), run_time=0.8)
            vo.wait_until("when the slower one ends")
            self.play(wf.to(cp.frame.get_center()[0], run_time=0.5), *cp.run(), FadeOut(ma, scale=0.6),
                      FadeOut(mb, scale=0.6), run_time=0.5)
            self.play(gt.grow("compare", run_time=0.5))
            self.play(*cp.succeed(), *gt.done("compare"), FadeIn(nine, shift=LEFT * 0.1), FadeOut(wf), run_time=0.5)

        # ========================================================== 4 · one edge too many: same answer, slower
        ROW1_Y = gt.ay - 0.95
        lab1 = mono("train_b.after(train_a)", CAPTION, INK)
        k0 = lab1.text.index(".after")
        lab1[k0:k0 + len(".after")].set_color(EDGE)
        lab1.move_to([gt.x_of(0) - 0.15 - lab1.width / 2, ROW1_Y, 0])
        bars1 = VGroup(*[bar_at(gt, a, b, ROW1_Y, OWN) for _, a, b in SERIAL])
        thirteen = mono(f"{SERIAL_TOTAL}", CAPTION, INK).move_to([gt.x_of(SERIAL_TOTAL) + 0.3, ROW1_Y, 0])
        slower = note_chip("same answer, slower", width=4.0)
        place(slower, right=thirteen.get_right()[0], top=ROW1_Y - 0.28)
        row1 = VGroup(lab1, bars1, thirteen)
        for m in (row1, slower):
            inside(m)
        guard(lab1.get_left()[0] >= SAFE_L, "variant label 1 left of the frame")
        apart(row1, gt, 0.15, "variant row 1 vs Gantt axis labels")
        extra = Wire(ta, tb, "order", start=ta.frame.get_bottom(), end=tb.frame.get_top(), flow="down")
        with self.voiceover(SAY[4]) as vo:
            self.play(extra.draw(), run_time=0.6)
            self.play(FadeIn(lab1, shift=UP * 0.15), run_time=0.4)
            vo.wait_until("same answer")
            for b, sp in zip(bars1, SERIAL):            # chained: each bar starts where the last one ends
                self.play(GrowFromEdge(b, LEFT), run_time=0.1 + 0.12 * (sp[2] - sp[1]), rate_func=linear)
            vo.wait_until("longer run")
            self.play(FadeIn(thirteen, shift=LEFT * 0.1), FadeIn(slower, shift=UP * 0.1), extra.light(EDGE),
                      run_time=0.6)

        # ========================================================== 5 · too few edges: guessed paths race
        ROW2_Y = slower.get_bottom()[1] - 0.45
        lab2 = label("guessed paths", CAPTION, S.GREY)
        lab2.move_to([gt.x_of(0) - 0.15 - lab2.width / 2, ROW2_Y, 0])
        bar2 = bar_at(gt, 0, 1, ROW2_Y, TURN)
        race = note_chip("no edges → starts at 0 → race", color=ERR, width=5.0)
        place(race, left=gt.x_of(1) + 0.3, cy=ROW2_Y)
        row2 = VGroup(lab2, bar2, race)
        inside(row2)
        apart(row2, slower, 0.08, "variant row 2 vs slower chip")
        note_a = sticky_note('"…/model_a"')
        note_b = sticky_note('"…/model_b"')
        place(note_a, cx=cp.frame.get_center()[0] + 0.2, bottom=cp.frame.get_top()[1] + 0.08)
        place(note_b, cx=cp.frame.get_center()[0] + 0.2, top=cp.frame.get_bottom()[1] - 0.08)
        for m in (note_a, note_b):
            inside(m, t=3.05)
            apart(m, cp.frame, 0.03, "sticky note vs compare")
        apart(note_b, gt, 0.03, "sticky note vs Gantt")
        guard(note_a.get_right()[0] <= lr.get_left()[0] - 0.1 or note_a.get_top()[1] <= lr.get_bottom()[1] - 0.05,
              "sticky note vs lecture tag")
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(extra), run_time=0.4)
            vo.wait_until("with guessed paths")
            self.play(*dg.restyle("train_a", "compare", "pending"), *dg.restyle("train_b", "compare", "pending"),
                      run_time=0.6)
            self.play(FadeIn(note_a, shift=DOWN * 0.1), FadeIn(note_b, shift=UP * 0.1), FadeIn(lab2), run_time=0.6)
            vo.wait_until("starts at time zero")
            self.play(*ta.run(), *tb.run(), *cp.run(), run_time=0.5)
            self.play(GrowFromEdge(bar2, LEFT, run_time=0.6))
            vo.wait_until("and reads half-finished results")
            self.play(flash(note_a, ERR, 1.1), flash(note_b, ERR, 1.1), run_time=0.7)
            self.play(*cp.fail(), bar2.animate.set_fill(ERR, 0.45).set_stroke(ERR), FadeIn(race, shift=LEFT * 0.1),
                      run_time=0.6)
            vo.wait_until("That is a race")
            self.play(flash(race.rows, ERR, 1.08), run_time=0.7)

        # ========================================================== 6 · exactly the edges the data needs
        halo = dg.halo(["prep", "train_a", "compare"])
        ring_a = ring(gt.bar["train_a"], TURN)
        never = label("never runs", CAPTION, S.GREY).next_to(cp.frame, DOWN, buff=0.12)
        apart(never, gt, 0.05, "never-runs label vs Gantt")
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(row1, slower, row2, note_a, note_b)), *dg.restyle("train_a", "compare", "data"),
                      *dg.restyle("train_b", "compare", "data"), run_time=0.7)
            self.play(*ta.succeed(), *tb.succeed(), *cp.reset(), run_time=0.5)
            self.play(*cp.succeed(), run_time=0.4)
            vo.wait_until("no more and no fewer")
            self.play(*[w.light(EDGE) for w in dg.wire.values()], run_time=0.8)
            vo.wait_until("The run then lasts its longest path")
            self.play(FadeIn(halo), *dim(tb, [dg.wire[("prep", "train_b")], dg.wire[("train_b", "compare")]], 0.3),
                      run_time=0.7)
            self.play(nine.animate.set_color(TURN), flash(nine, TURN, 1.5), Create(ring_a),
                      run_time=0.7)
            vo.wait_until("If an upstream task fails")
            self.play(FadeOut(halo), FadeOut(ring_a),
                      *dim(tb, [dg.wire[("prep", "train_b")], dg.wire[("train_b", "compare")]], 1.0),
                      run_time=0.5)
            self.play(*ta.fail(), *gt.fail("train_a"), run_time=0.5)
            vo.wait_until("the join never runs")
            self.play(*cp.skip(), gt.bar["compare"].animate.set_fill(STALE, 0.1).set_stroke(STALE),
                      nine.animate.set_color(S.GREY), FadeIn(never, shift=UP * 0.1), run_time=0.6)

        # ========================================================== 7 · PONDER P2
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(dg, gt, guide, nine, never, tag3)), run_time=0.6)
            card = mcq_ponder(self, P2_Q, P2_OPTS, seconds=8, figure=p2_dag(), cols=2)
        guard(card.get_top()[1] <= LREF_BOTTOM - 0.03, "MCQ card under the lecture tag")
        fig = card.figure

        # ========================================================== 8 · B: the longest path
        path = ["ingest", "clean", "train_cnn", "compare"]
        with self.voiceover(SAY[8]) as vo:
            self.play(*card.reveal(P2_ANSWER), run_time=0.8)
            vo.wait_until("The longest path is")
            h2 = fig.halo(path)
            self.play(FadeIn(h2), run_time=0.7)
            vo.wait_until("2, plus 3")
            self.play(*card.reason(P2_ANSWER, "longest path: 2 + 3 + 10 + 1 = 16", OWN), run_time=0.7)
            vo.wait_until("The small training and the report")
            self.play(flash(fig.node["train_tree"].frame, OWN, 1.12), flash(fig.node["report"].frame, OWN, 1.12),
                      run_time=0.7)
            vo.wait_until("overlap with the big one")
            self.play(flash(fig.node["train_cnn"].frame, TURN, 1.08), run_time=0.6)

        # ========================================================== 9 · why A, D, C are wrong
        with self.voiceover(SAY[9]) as vo:
            self.play(*card.reason(0, "adds every task in sequence: 22"), run_time=0.7)
            vo.wait_until("D runs the two trainings")
            self.play(*card.reason(3, "runs the two trainings one after the other"), run_time=0.7)
            vo.wait_until("C ignores the edges")
            self.play(*card.reason(2, "ignores the edges: clean → train → compare"), run_time=0.7)
            vo.wait_until("and compare waits")
            self.play(flash(fig.node["compare"].frame, ERR, 1.1), run_time=0.6)

        # ========================================================== 10 · takeaway
        tk = takeaway("no path of wires between two steps → parallel · "
                      "a step that consumes several outputs → waits for all of them")
        inside(tk)
        with self.voiceover(SAY[10]) as vo:
            self.play(FadeOut(card), FadeOut(h2), run_time=0.6)
            self.play(*tk.write(), run_time=1.4)
            vo.wait_until("If there is no path")
            self.play(flash(tk.rows[0], TURN, 1.04), run_time=0.6)
            vo.wait_until("If a step consumes")
            self.play(flash(tk.rows[1], TURN, 1.04), run_time=0.6)
        self.play(FadeOut(tk), FadeOut(lr), run_time=0.6)
        self.wait(0.3)
