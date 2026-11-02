"""S05 · Enforcing order: edges, not clocks (V4, the four lanes; the launcher coda).
Lecture: 20–22, 34, 37.

Beats (script.md "## S05", one voiceover block each):
 0  LECTURE 20–22. The sequence prep → train → deploy as three nodes (GREY dotted: how does each
    one wait?); they give way to V4 (tag `illustration`): one clock axis 1:00 → 5:00.
 1  The four lanes write in as the SAY names them, each with three bars prep / train / deploy:
    ORANGE "cron · 1:00 / 2:00 / 3:00" (bars hang from ORANGE ticks); ORANGE `prep & train & deploy`
    (all three bars at the left edge); "event → train · tracker → deploy" with a BLUE leaderboard
    beside it (top row `model · run 12 · acc 0.91`, GREY dashed: an older run); PINK "pipeline
    edges" (each bar snapped to a GREEN ✓).
 2  A die (bottom left) rolls the length of prep: 40, 75, 55 min; every lane re-lays its bars by
    its rule. After the first roll today's model lands in the leaderboard *below* run 12.
 3  Replay: the die goes back to 40 (cron ✓), then 75, slower: train starts at 2:00 under a
    still-running prep, RED flash, flag "half-written file", cron ✗. The `&` lane: ✗, flag "nothing
    waits", and three RED marks "40 ✗ 75 ✗ 55 ✗" beside it.
 4  Tracker lane ✗: a RED spark where the event fires on prep's first file (flag "half-written");
    deploy reaches (PINK arrow) into the leaderboard and takes the top row, run 12 (RED ring "not
    this run"), though today's model sits in row 2. Edge lane ✓: GREY dashed ghosts of its bars at
    40 show they only slid right; a chip "it just stretches".
 5  LECTURE 34, 37. The lanes leave (the code needs the room: deviation from "the lanes shrink to
    the top"). CODE(ml-workflow/src/workflow/cli.py: 229–257) folded to 231–233, 247–248, 255–256;
    the three `.after(...)` lines lit PINK one by one while the four-node chain draws beside it with
    PINK dashed wires.
 6  The panel Transforms into CODE(ml-workflow/src/workflow/pipeline.yaml: 180–209) folded to
    185–188, 194–195, 208–209; the three `dependentTasks` pairs lit PINK, the lower two labelled
    "Model Deploy ← Model Training" and "Model Training ← Data Processor". Under it
    PANEL(ml-workflow/README.md: 218) with the sentence lit YELLOW; the chain runs step by step.
 7  Panels clear. A `train` node sends a BLUE "job" bubble to another machine, "a step can launch
    work elsewhere"; it moves to the top band and the PONDER P3 card comes in (8 s).
 8  Reveal: B fills YELLOW ✓. Above the card the bubble becomes the launcher (V4 coda, small): the
    5 s `train · step` bar with its ✓, the BLUE training job running on, the PINK dashed edge to
    deploy, which takes a GREY dashed "previous model". RED reason under A.
 9  RED reasons under C and D. (The card fades at the start of the next beat.)
10  CODE(ml-workflow/src/workflow/model.py: 52–63) folded to 52, 54–56, 61–63 (62 `sync=True,` lit
    GREEN; 53 never shown); the launcher, full size below it, stretches (sync), then the job fails
    and the step and deploy follow; a GREY chip with the commit.
11  Everything fades. TAKEAWAY (two rows), each row flashes as the SAY reaches it; empty frame.
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Create,
    DashedVMobject,
    FadeIn,
    FadeOut,
    GrowFromEdge,
    Indicate,
    LaggedStart,
    Line,
    ReplacementTransform,
    RoundedRectangle,
    Transform,
    VGroup,
)

from common import *  # noqa: F401,F403
from explainer import style as S
from explainer.scene import VoiceScene

SAY = NARRATION["S05"]

# ------------------------------------------------------------------ the real sources
CLI = "ml-workflow/src/workflow/cli.py"
PYAML = "ml-workflow/src/workflow/pipeline.yaml"
MODEL = "ml-workflow/src/workflow/model.py"
CLI_FOLD = [(231, 233), (247, 248), (255, 256)]
AFTER = {233: "data_collector_task", 248: "data_processor_task", 256: "model_training_task"}
for _n, _v in AFTER.items():
    assert source_line(CLI, _n).strip() == f".after({_v})", source_line(CLI, _n)
assert source_line(CLI, 232).strip() == '.set_display_name("Data Processor")', source_line(CLI, 232)
assert source_line(CLI, 247).strip() == '.set_display_name("Model Training")', source_line(CLI, 247)
assert source_line(CLI, 255).strip() == '.set_display_name("Model Deploy")', source_line(CLI, 255)
YAML_FOLD = [(185, 188), (194, 195), (208, 209)]
DEP = {185: "data-collector", 194: "model-training", 208: "data-processor"}     # dependentTasks: - <dep>
for _n, _d in DEP.items():
    assert source_line(PYAML, _n).strip() == "dependentTasks:", source_line(PYAML, _n)
    assert source_line(PYAML, _n + 1).strip() == f"- {_d}", source_line(PYAML, _n + 1)
assert source_line(PYAML, 188).strip() == "name: Data Processor", source_line(PYAML, 188)
assert source_line(PYAML, 189).strip() == "model-deploy:", source_line(PYAML, 189)       # 194's task
assert source_line(PYAML, 203).strip() == "model-training:", source_line(PYAML, 203)     # 208's task
README_SENT = "Each step starts only after the previous one succeeds."
assert README_SENT in source_line("ml-workflow/README.md", 218)
MODEL_FOLD = [(52, 52), (54, 56), (61, 63)]                 # line 53 (the old comment) is never shown
assert source_line(MODEL, 62).strip() == "sync=True,", source_line(MODEL, 62)
assert source_line(MODEL, 54).strip() == "job.run(", source_line(MODEL, 54)

# V4 (script.md "Notes for scene authors"): train 50, deploy 10, rolls 40 / 75 / 55
assert (V4_TRAIN, V4_DEPLOY, tuple(V4_ROLLS)) == (50, 10, (40, 75, 55))
PREP0 = 25                                   # before the first roll (the die shows pips)
for _p, _ok in ((40, True), (75, False), (55, True)):
    assert lane_spans("cron", _p)[1] is _ok, _p                   # cron: fine at 40 and 55, broken at 75
    assert lane_spans("amp", _p)[1] is False                      # &: broken on every roll
    assert lane_spans("tracker", _p)[1] is False                  # tracker: never this run
    assert lane_spans("edges", _p)[1] is True                     # edges: right on every roll
assert "train" in lane_spans("tracker", 75)[2] and "train" not in lane_spans("tracker", 40)[2]

# P3 (script.md PONDER P3; the right answer is B: index 1). Re-derived: an edge (.after) waits for
# the upstream TASK to succeed; the task returns after 5 s, so deploy starts ~5 s after train
# starts, while the job it launched may still run: the previous model may be deployed. A is wrong
# (Vertex does not track work a step launched), C (.after needs no data), D (it is dependentTasks).
P3_Q = ("`deploy` has `.after(train_task)`. The `train` step submits a training job to another "
        "machine and returns after 5 seconds, without waiting. When can `deploy` start?")
P3_OPTS = ["only when the training job finishes: Vertex tracks every job a step starts",
           "about 5 s after `train` starts — it may deploy the previous model",
           "never: `.after()` fails because no data was passed",
           "at the same time as the first task: `.after()` is only a hint"]
P3_ANSWER = 1

# ------------------------------------------------------------------ layout
SAFE_L, SAFE_R = -6.45, 6.45
TOP_Y = 3.05
K_SMALL = 0.5                    # the launcher above the P3 card


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


def split_header(p):
    """Put a panel's header on two rows: the directory, then the file name and the line note (as in S04)."""
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


def ghost_bar(fl, a, b, y):
    """A GREY dashed outline of a bar from minute a to b on fl's clock, at height y."""
    w = fl.x_of(b) - fl.x_of(a)
    r = RoundedRectangle(width=w, height=0.24, corner_radius=0.06).move_to([fl.x_of(a) + w / 2, y, 0])
    return DashedVMobject(r.set_stroke(STALE, 2), num_dashes=max(10, int(w * 8))).set_stroke(STALE, 2)


def align_rows(la, gap):
    """The launcher's row names right-aligned `gap` left of the step bar (after a rescale, which
    keeps text at its size but moves its centre)."""
    x = la.step_bar.get_left()[0] - gap
    for lab in la.parts["rows"]:
        lab.shift(RIGHT * (x - lab.get_right()[0]))


class EdgesNotClocks(VoiceScene):
    def construct(self):
        assert len(SAY) == 12, len(SAY)

        # ========================================================== 0 · the sequence, four ways, one clock
        seq = Dag({"prep": (-3.6, 0.3), "train": (0, 0.3), "deploy": (3.6, 0.3)},
                  [("prep", "train", "pending"), ("train", "deploy", "pending")], node_kw={"outputs": ()})
        inside(seq)
        q = label("how does each step wait?", CAPTION, S.GREY).next_to(seq, DOWN, buff=0.5)
        fl = FourLanes(prep=PREP0, show=("axis",), names={
            "cron": "cron at 1:00, 2:00, 3:00",
            "amp": "`prep & train & deploy`",
            "tracker": "event → train, tracker → deploy",
            "edges": "pipeline edges"})
        inside(fl, t=3.0)
        tag4 = illustration_tag()
        place(tag4, left=SAFE_L + 0.05, top=3.5)
        apart(tag4, fl, 0.05, "illustration tag vs lanes")
        with self.voiceover(SAY[0]) as vo:
            lr = lref_swap(self, None, "20–22")
            self.play(FadeIn(seq, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("preprocess, train, deploy")
            self.play(LaggedStart(*[flash(seq.node[n], INK, 1.12) for n in ("prep", "train", "deploy")],
                                  lag_ratio=0.45), run_time=1.2)
            self.play(FadeIn(q, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Here are four ways")
            self.play(FadeOut(VGroup(seq, q), shift=UP * 0.3), run_time=0.6)
            self.play(*fl.parts_in("axis"), FadeIn(tag4), run_time=0.7)
            vo.wait_until("on one clock")
            self.play(LaggedStart(*[flash(m, TURN, 1.2) for m in fl.parts["axis"][0::2]], lag_ratio=0.2),
                      run_time=1.0)

        # ========================================================== 1 · the four lanes
        lb = Leaderboard().move_to([3.65, fl.lane_y("tracker"), 0])
        inside(lb)
        badges = VGroup()
        for t in TASKS3:
            b = fl.bar("edges", t)
            bd = ok_badge(0.11).move_to(b.get_right() + RIGHT * 0.15)
            bd.add_updater(lambda m, b=b: m.move_to(b.get_right() + RIGHT * 0.15))
            badges.add(bd)
        with self.voiceover(SAY[1]) as vo:
            vo.wait_until("Lane one")
            self.play(*fl.parts_in("lane:cron"), run_time=0.6)
            self.play(flash(fl.ticks, CLOCK, 1.1), run_time=0.6)
            vo.wait_until("Lane two")
            self.play(*fl.parts_in("lane:amp"), run_time=0.6)
            vo.wait_until("Lane three")
            self.play(*fl.parts_in("lane:tracker"), run_time=0.6)
            vo.wait_until("and deploy takes the best model")
            self.play(FadeIn(lb, shift=LEFT * 0.2), run_time=0.6)
            self.play(flash(lb.rows[0], CLOUD, 1.06), run_time=0.6)
            vo.wait_until("Lane four")
            self.play(*fl.parts_in("lane:edges"), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(bd, scale=1.5) for bd in badges], lag_ratio=0.4), run_time=0.8)
        apart(lb, fl.bar("tracker", "deploy"), 0.1, "leaderboard vs tracker bars")

        # ========================================================== 2 · roll the length of preprocessing
        die = Die().move_to([-5.6, -2.85, 0])
        dlab = label("prep takes", CAPTION, S.GREY).next_to(die, RIGHT, buff=0.2)
        inside(VGroup(die, dlab))
        apart(die, fl, 0.1, "die vs lanes")
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeIn(die, shift=UP * 0.2), FadeIn(dlab), run_time=0.6)
            vo.wait_until("40 minutes")
            self.play(*die.roll(40), *fl.set_prep(40), run_time=1.0)
            self.play(*lb.add_row("model · today · acc 0.88", 1), run_time=0.6)
            vo.wait_until("Then 75")
            self.play(*die.roll(75), *fl.set_prep(75), run_time=1.0)
            vo.wait_until("Then 55")
            self.play(*die.roll(55), *fl.set_prep(55), run_time=1.0)

        # ========================================================== 3 · the clock lane and the background lane
        two = fl.x_of(60)
        late = Line([two, fl.bar("cron", "prep").get_top()[1] + 0.05, 0],
                    [two, fl.bar("cron", "train").get_bottom()[1] - 0.05, 0], color=ERR, stroke_width=5)
        marks = VGroup()
        for p in V4_ROLLS:
            marks.add(VGroup(mono(str(p), CAPTION, ERR), x_mark(0.22).set_color(ERR)).arrange(RIGHT, buff=0.08))
        marks.arrange(RIGHT, buff=0.35).move_to([1.9, fl.lane_y("amp") + 0.12, 0])
        with self.voiceover(SAY[3]) as vo:
            vo.wait_until("The clock lane is fine at 40")
            self.play(*die.roll(40), *fl.set_prep(40), run_time=0.8)
            self.play(*fl.parts_in("mark:cron"), flash(fl.bar("cron", "train"), OWN, 1.08), run_time=0.6)
            vo.wait_until("and broken at 75")
            self.play(*die.roll(75, run_time=2.0), *fl.set_prep(75, run_time=2.0), run_time=2.0)
            vo.wait_until("training reads a half-written file")
            self.play(Create(late), flash(fl.bar("cron", "prep"), ERR, 1.08), run_time=0.6)
            fc = fl.flag("cron", "train")
            self.play(FadeIn(fc), FadeOut(late), run_time=0.6)
            vo.wait_until("The background lane")
            fa = fl.flag("amp", "train")
            apart(marks, fa, 0.15, "RED roll marks vs the & flag")
            apart(marks, lb, 0.05, "RED roll marks vs leaderboard")
            self.play(*fl.parts_in("mark:amp"), FadeIn(fa), run_time=0.6)
            vo.wait_until("on every roll")
            self.play(LaggedStart(*[FadeIn(m, scale=1.4) for m in marks], lag_ratio=0.4), run_time=1.0)
            vo.wait_until("because nothing waits")
            self.play(flash(VGroup(*[fl.bar("amp", t) for t in TASKS3]), ERR, 1.06), run_time=0.7)

        # ========================================================== 4 · the tracker lane; the edge lane stretches
        fire = spark(0.16).move_to([fl.x_of(60), fl.bar("tracker", "prep").get_center()[1], 0])
        dep = fl.bar("tracker", "deploy")
        reach = Arrow(dep.get_right() + RIGHT * 0.02, lb.rows[0].frame.get_left() + DOWN * 0.04, color=EDGE,
                      buff=0.04, stroke_width=4, max_tip_length_to_length_ratio=0.3, tip_length=0.16)
        ghosts = VGroup(*[ghost_bar(fl, *lane_spans("edges", 40)[0][t], fl.bar("edges", t).get_center()[1])
                          for t in TASKS3])
        stretch = note_chip("it just stretches", color=EDGE, width=4.0)
        place(stretch, right=fl.x_of(240), top=fl.lane_y("edges") - 0.62)
        inside(stretch)
        apart(stretch, die, 0.1, "chip vs die")
        with self.voiceover(SAY[4]) as vo:
            self.play(*fl.parts_in("mark:tracker"), run_time=0.5)
            vo.wait_until("The event can fire on the first file")
            self.play(FadeIn(fire, scale=1.6), run_time=0.5)
            ft = fl.flag("tracker", "train")
            self.play(FadeIn(ft), flash(fl.bar("tracker", "train"), ERR, 1.08), run_time=0.6)
            vo.wait_until("And the tracker's best model")
            self.play(GrowFromEdge(reach, LEFT), flash(lb.rows[0], ERR, 1.05), run_time=0.7)
            pick = lb.pick(0)
            dring = ring(dep, ERR, buff=0.05, stroke=3)
            self.play(FadeIn(pick), Create(dring), run_time=0.6)
            vo.wait_until("not this run's")
            self.play(flash(lb.rows[1], OWN, 1.06), run_time=0.6)
            vo.wait_until("Only the edge lane")
            self.play(*fl.parts_in("mark:edges"), LaggedStart(*[flash(bd, OWN, 1.5) for bd in badges],
                                                              lag_ratio=0.3), run_time=0.8)
            vo.wait_until("It just stretches")
            self.play(FadeIn(ghosts), run_time=0.4)
            self.play(LaggedStart(*[flash(fl.bar("edges", t), EDGE, 1.06) for t in TASKS3], lag_ratio=0.3),
                      FadeIn(stretch, shift=UP * 0.1), run_time=0.8)
        self.wait(0.8)

        # ========================================================== 5 · the cheese app: .after() on each step
        for bd in badges:
            bd.clear_updaters()
        pc = src_panel(CLI, CLI_FOLD)
        split_header(pc)
        place(pc, left=SAFE_L + 0.01, top=TOP_Y)
        inside(pc)
        CH = dict(zip(("collector", "processor", "training", "deploy"), CHEESE))
        CX = 4.72
        chain = Dag({k: (CX + dx, y) for k, dx, y in zip(CH, (0, 0, 0, 0), (2.55, 1.15, -0.25, -1.65))},
                    [(a, b, "order") for a, b in zip(list(CH), list(CH)[1:])], flow="down", titles=CH,
                    show=("node:collector",), node_kw={"outputs": (), "font": SANS})
        inside(chain, t=3.08)
        apart(pc, chain, 0.15, "cli panel vs chain")
        keys = list(CH)
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(fl, lb, die, dlab, badges, fc, fa, marks, fire, ft, reach, pick, dring,
                                     ghosts, stretch, tag4)), run_time=0.7)
            lr = lref_swap(self, lr, "34, 37")
            self.play(FadeIn(pc, shift=RIGHT * 0.2), FadeIn(chain), run_time=0.8)
            bars = {}
            for (n, _), (a, b), anchor in zip(AFTER.items(), zip(keys, keys[1:]),
                                             ("processing after collection", "training after processing",
                                              "deployment after training")):
                vo.wait_until(anchor)
                bars[n] = pc.bar(n, EDGE, 0.3)
                self.play(FadeIn(bars[n]), *chain.parts_in(f"node:{b}"), run_time=0.5)
                self.play(*chain.parts_in(f"wire:{a}->{b}", anim=Create), run_time=0.5)
            vo.wait_until("each with dot after")
            self.play(*[flash(pc.span(n, ".after"), EDGE, 1.15) for n in AFTER],
                      *[chain.wire[(a, b)].light(EDGE) for a, b in zip(keys, keys[1:])], run_time=0.8)

        # ========================================================== 6 · dependentTasks; the README sentence
        py = src_panel(PYAML, YAML_FOLD)
        split_header(py)
        place(py, left=SAFE_L + 0.01, top=TOP_Y)
        inside(py)
        rd = readme_panel("ml-workflow", 218, clip={218: ("Each step starts", "succeeds.")}, chars=30)
        place(rd, left=SAFE_L + 0.1, top=py.get_bottom()[1] - 0.25)
        inside(rd)
        apart(rd, chain, 0.15, "README panel vs chain")
        dep_lab = {}
        for n, txt in ((194, "Model Deploy ← Model Training"), (208, "Model Training ← Data Processor")):
            rows = VGroup(*[py.code.code_lines[k] for k in py.rows_of(n)] +
                          [py.code.code_lines[k] for k in py.rows_of(n + 1)])
            t = label(txt, CAPTION, EDGE)
            t.next_to(py.code, RIGHT, buff=0.35).set_y(rows.get_center()[1])
            dep_lab[n] = t
            inside(t)
            apart(t, chain, 0.1, f"label {n} vs chain")
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(*bars.values())), ReplacementTransform(pc, py), run_time=0.8)
            vo.wait_until("dependent tasks")
            dbars = VGroup(*[py.bar(m, EDGE, 0.3) for n in DEP for m in (n, n + 1)])
            self.play(FadeIn(dbars), run_time=0.5)
            self.play(FadeIn(dep_lab[194], shift=LEFT * 0.1), chain.wire[("training", "deploy")].light(EDGE),
                      run_time=0.6)
            self.play(FadeIn(dep_lab[208], shift=LEFT * 0.1), chain.wire[("processor", "training")].light(EDGE),
                      run_time=0.6)
            vo.wait_until("And the README says it plainly")
            self.play(FadeIn(rd, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("each step starts only after")
            rbar = rd.bar(README_SENT, TURN, 0.3)
            self.play(FadeIn(rbar), run_time=0.4)
            for k in keys:
                self.play(*chain.run(k), run_time=0.3)
                self.play(*chain.succeed(k), run_time=0.3)

        # ========================================================== 7 · a step that launches work elsewhere; P3
        tn = TaskNode("train", outputs=())
        mach = machine_glyph(1.0, CLOUD, "another machine")
        hint = label("a step can launch work elsewhere", CAPTION, S.GREY)
        pre = VGroup(tn, mach, hint)
        tn.move_to([-4.2, 0.4, 0])
        mach.move_to([0.0, 0.4, 0]).shift(UP * (tn.frame.get_center()[1] - mach.slab.get_center()[1]))
        hint.next_to(mach.slab, RIGHT, buff=0.6)
        go = Arrow(tn.frame.get_right(), mach.slab.get_left(), color=CLOUD, buff=0.12, stroke_width=3,
                   tip_length=0.16)
        job = value_token("job", CLOUD)
        job.move_to(tn.frame.get_right() + RIGHT * 0.45)
        pre.add(go)
        inside(VGroup(pre, job))
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(py, rd, chain, dbars, *dep_lab.values(), rbar)), run_time=0.6)
            self.play(FadeIn(tn, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Some steps only launch work")
            self.play(FadeIn(mach, shift=UP * 0.1), run_time=0.5)
            self.play(*tn.run(), Create(go), FadeIn(job, scale=0.8), run_time=0.6)
            self.play(job.animate.move_to(mach.slab.get_left() + LEFT * 0.5), FadeIn(hint, shift=LEFT * 0.1),
                      run_time=0.8)
            vo.wait_until("Remember exactly")
            self.play(flash(tn.frame, EDGE, 1.12), run_time=0.6)
            vo.wait_until("Pause here")
            band = VGroup(pre, job)
            self.play(band.animate.shift(UP * (2.45 - tn.frame.get_center()[1])), run_time=0.6)
            card = mcq_ponder(self, P3_Q, P3_OPTS, seconds=8)
        guard(card.get_top()[1] <= LREF_BOTTOM - 0.03, "MCQ card under the lecture tag")
        apart(band, card, 0.05, "launch figure vs P3 card")
        apart(band, lr, 0.05, "launch figure vs lecture tag")

        # ========================================================== 8 · B: the edge waits for the task
        la = Launcher(show=())
        off = la.pick.get_center() - la.dep_bar.get_center()          # the pick's place at full size
        la.rescale(K_SMALL)
        align_rows(la, 0.15)
        la.pick.next_to(la.dep_bar, RIGHT, buff=0.15)
        place(la, left=-5.6, cy=2.45)
        inside(la)
        apart(la, card, 0.05, "small launcher vs P3 card")
        apart(la, lr, 0.05, "small launcher vs lecture tag")
        with self.voiceover(SAY[8]) as vo:
            self.play(*card.reveal(P3_ANSWER), run_time=0.8)
            vo.wait_until("An edge waits for the task")
            self.play(FadeOut(band, shift=UP * 0.1), *la.parts_in("rows"), run_time=0.5)
            self.play(*la.parts_in("step", anim=lambda m: GrowFromEdge(m, LEFT)),
                      *la.parts_in("job", anim=lambda m: GrowFromEdge(m, LEFT)), run_time=0.8)
            vo.wait_until("succeeded after 5 seconds")
            self.play(flash(la.badge, OWN, 1.5), *la.parts_in("edge", anim=Create), run_time=0.6)
            self.play(*la.parts_in("deploy", anim=lambda m: GrowFromEdge(m, LEFT)), run_time=0.5)
            vo.wait_until("The pipeline never sees the job")
            self.play(flash(la.job_bar, CLOUD, 1.05), run_time=0.6)
            vo.wait_until("so A is wrong")
            self.play(*card.reason(0, "the edge waits for the task, not for the job it launched"), run_time=0.7)
            vo.wait_until("the previous model")
            self.play(*la.parts_in("pick"), run_time=0.5)

        # ========================================================== 9 · why C and D are wrong
        with self.voiceover(SAY[9]) as vo:
            self.play(*card.reason(2, "`.after()` needs no data"), run_time=0.7)
            vo.wait_until("D: dot after is enforced")
            self.play(*card.reason(3, "enforced: it is `dependentTasks` in the YAML"), run_time=0.7)
            vo.wait_until("as a dependent task")
            self.play(flash(card.options[3].text, ERR, 1.03), run_time=0.6)

        # ========================================================== 10 · sync=True: the step waits for its job
        pm = src_panel(MODEL, MODEL_FOLD)
        place(pm, left=SAFE_L + 0.01, top=TOP_Y)
        inside(pm)
        big = la.copy()
        big.rescale(1 / K_SMALL)
        align_rows(big, 0.3)
        big.pick.move_to(big.dep_bar.get_center() + off)
        place(big, cx=0.0, bottom=-3.5)
        inside(big)
        apart(big, pm, 0.1, "launcher vs model.py panel")
        commit = note_chip("commit: Wait for training to finish before deployment · `sync=False` → `sync=True`",
                           width=4.1)
        place(commit, right=SAFE_R, top=pm.get_top()[1] - 1.1)
        inside(commit)
        apart(commit, pm, 0.1, "commit chip vs model.py panel")
        apart(commit, lr, 0.1, "commit chip vs lecture tag")
        apart(commit, big, 0.1, "commit chip vs launcher")
        with self.voiceover(SAY[10]) as vo:
            self.play(FadeOut(card), Transform(la, big), run_time=0.8)
            self.play(FadeIn(pm, shift=RIGHT * 0.2), run_time=0.6)
            vo.wait_until("With sync set to true")
            g62 = pm.bar(62, OWN, 0.3)
            self.play(FadeIn(g62), flash(pm.span(62, "sync=True"), OWN, 1.15), run_time=0.6)
            vo.wait_until("it waits for its job")
            self.play(*la.sync(), run_time=1.2)
            vo.wait_until("and fails if the job fails")
            self.play(*la.job_fails(), run_time=0.8)
            vo.wait_until("so deploy never runs")
            self.play(flash(la.dep_bar, S.GREY, 1.05), run_time=0.6)
            vo.wait_until("A recent commit")
            self.play(FadeIn(commit, shift=LEFT * 0.15), run_time=0.6)

        # ========================================================== 11 · takeaway
        tk = takeaway("cron offsets, `&`, or 'pick the best from the tracker' → race or wrong model · "
                      "edges preprocess → train → deploy → correct by construction")
        inside(tk)
        with self.voiceover(SAY[11]) as vo:
            self.play(FadeOut(VGroup(la, pm, g62, commit)), run_time=0.6)
            self.play(*tk.write(), run_time=1.4)
            vo.wait_until("If an option uses")
            self.play(flash(tk.rows[0], TURN, 1.04), run_time=0.6)
            vo.wait_until("think race or wrong model")
            self.play(flash(tk.rows[0], ERR, 1.04), run_time=0.6)
            vo.wait_until("Edges from preprocess")
            self.play(flash(tk.rows[-1], TURN, 1.04), run_time=0.6)
        self.play(FadeOut(tk), FadeOut(lr), run_time=0.6)
        self.wait(0.3)
