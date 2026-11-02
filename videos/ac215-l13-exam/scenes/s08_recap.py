"""S08 · Six rules for Tuesday (the recap: the S01 miniatures return, two rules per frame).
Lecture: 5, 10, 15, 24, 27, 29.

Beats (script.md "## S08", one voiceover block each):
 0  LECTURE 15, 24. The title "Six rules for Tuesday" over the six miniatures in a row (the five of
    S01 plus "the data": a bucket linked to a record card). On "Rule one" the title fades, the row
    drops to a strip at the bottom and the run miniature rises to the left column; it replays (a
    tick drops into the open row) while rule 1's first sentence writes under it in YELLOW; on
    "init opens" its second sentence (`wandb.init` opens a run; `finish` closes it).
 1  On "Rule two" the package miniature rises to the right column; its replay: `setup.py` makes
    room for a GREEN `trainer/` and a PINK scan line sweeps the box, lighting `trainer/`. Rule 2
    writes; on "your own modules" its second sentence.
 2  LECTURE 27, 29. Rules 1–2 (with their miniatures) fade; the GPU miniature rises left; its
    replay: the all-reduce ring pulses. Rule 3 writes; on "across machines" the second part; on
    "because separate" its last row flashes.
 3  The batch miniature rises right; its replay: the tray's four column-slices part along the
    PINK cut lines and close again. Rule 4 writes; on "split across" the second part.
 4  LECTURE 10, 24. Rules 3–4 fade; the job miniature rises left; its replay: the ticket returns
    its GREY id `‹job-id›` (stays beside it). Rule 5 writes; on "never into" the second sentence.
 5  The data miniature rises right; its replay: the link flashes between snapshot and record.
    Rule 6 writes; on "archived snapshot" its second part. The strip is now empty.
 6  LECTURE 5. Rules 5–6 fade. Our redrawing of slide 5: "The 3 components for better Deep
    Learning" over three GREY pillars "More Data", "Better/Faster Models", "Faster Hardware",
    each built as it is named; on "Today was the hardware lever" the third lights YELLOW; on "plus
    the bookkeeping" a GREY note "+ the bookkeeping: W&B runs" under the floor. Fade to an empty
    frame.

Deviations from SHOW: the rules on screen are short written forms of the SAY (each split in two
parts written at the spoken clause, so the text moves with the voice); the package replay is drawn
in the scene (the miniature's own replay only pulses the box) and so is the batch split and the
job id; a GREY note names "the bookkeeping" in beat 6 so something moves in the 13 s closing line.
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    AnimationGroup,
    Create,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    Line,
    Polygon,
    Rectangle,
    Succession,
    VGroup,
    Write,
    there_and_back_with_pause,
)

from common import *  # noqa: F401,F403
from common import guard
from explainer import style as S
from explainer.scene import VoiceScene

SAY = NARRATION["S08"]

SAFE = 6.6
COL_X = (-3.3, 3.3)        # the two rule columns
COL_W = 6.3                # rule text width per column
MINI_TOP = 2.85            # a risen miniature's top (under the lecture tag's bottom 3.13)
STRIP_BOTTOM = -3.4        # the strip of waiting miniatures
RULE_SIZE = 28

RULES = {
    "run": ("Rule 1: a callback logs one entry per epoch into the active run.",
            "`wandb.init` opens a run; `finish` closes it."),
    "package": ("Rule 2: pip installs only what `setup.py` declares.",
                "Your own modules must be inside the package it builds, not just inside the tarball."),
    "gpus": ("Rule 3: `MirroredStrategy` = the GPUs of one machine.",
             "Across machines: `MultiWorkerMirroredStrategy` + `TF_CONFIG`. "
             "Separate strategies, separate models."),
    "batch": ("Rule 4: under a strategy, `dataset.batch(n)` makes the global batch,",
              "split across the replicas in sync: n ÷ `num_replicas_in_sync` each."),
    "job": ("Rule 5: long training → a durable job with an id.",
            "Never a request handler, a thread or a longer timeout."),
    "data": ("Rule 6: a data version =",
             "an archived snapshot + the record that points at it."),
}
CUES = {   # (the replay cue, the second part's cue) — words of the SAY lines
    "run": ("Rule one", "init opens"),
    "package": ("Rule two", "your own modules"),
    "gpus": ("Rule three", "across machines"),
    "batch": ("Rule four", "split across"),
    "job": ("Rule five", "never into"),
    "data": ("Rule six", "archived snapshot"),
}
for _k, (_a, _b) in CUES.items():
    _i = MINI_KINDS.index(_k)
    assert _a in SAY[_i] and _b in SAY[_i], (_k, _a, _b)
assert "because separate" in SAY[2]

PILLARS = ("More Data", "Better/Faster Models", "Faster Hardware")
PILLAR_CUES = ("more data", "better models", "faster hardware")
SLIDE5_TITLE = "The 3 components for better Deep Learning"


# ------------------------------------------------------------------ layout helpers (as in s06)
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


def inside(*ms, t: float = 3.6):
    for m in ms:
        guard(m.get_left()[0] >= -SAFE and m.get_right()[0] <= SAFE and m.get_bottom()[1] >= -3.6
              and m.get_top()[1] <= t,
              f"outside the frame: {m.get_left()} {m.get_right()} {m.get_bottom()} {m.get_top()}")


def apart(a, b, gap: float = 0.1):
    """a and b do not overlap (boxes at least `gap` apart on x or on y)."""
    dx = max(a.get_left()[0] - b.get_right()[0], b.get_left()[0] - a.get_right()[0])
    dy = max(a.get_bottom()[1] - b.get_top()[1], b.get_bottom()[1] - a.get_top()[1])
    guard(dx >= gap or dy >= gap, f"overlap: dx {dx:.2f} dy {dy:.2f}")


def below_tag(m, slides: str):
    t = lref(slides)
    guard(m.get_top()[1] <= t.get_bottom()[1] - 0.05 or m.get_right()[0] <= t.get_left()[0] - 0.05,
          f"under the lecture tag {slides}")


def flash(mob, color=TURN, k: float = 1.08, run_time: float = 0.6):
    return Indicate(mob, color=color, scale_factor=k, run_time=run_time)


# ------------------------------------------------------------------ the rule columns
class RuleColumn:
    """One risen miniature with its rule (head rows, tail rows) under it, in column `col`.
    Positions only: the miniature is moved there by the scene."""

    def __init__(self, mini: Miniature, col: int):
        self.mini = mini
        head_s, tail_s = RULES[mini.kind]
        x = COL_X[col]
        self.target = mini.copy()
        place(self.target, cx=x, top=MINI_TOP)
        self.head = fit_rows(head_s, COL_W, RULE_SIZE, TURN, buff=0.12)
        self.tail = fit_rows(tail_s, COL_W, RULE_SIZE, TURN, buff=0.12)
        place(self.head, left=x - COL_W / 2, top=self.target.get_bottom()[1] - 0.3)
        place(self.tail, left=x - COL_W / 2, top=self.head.get_bottom()[1] - 0.12)
        self.extra = VGroup()      # anything the replay leaves beside the miniature
        self.text = VGroup(self.head, self.tail)

    def all(self):
        return VGroup(self.mini, self.extra, self.head, self.tail)


def package_replay(scene, mini: Miniature):
    """setup.py makes room for trainer/, a PINK scan line sweeps the box, trainer/ lights."""
    box, name = mini.glyph[0], mini.glyph[1]
    tr = mono("trainer/", CAPTION, OWN)
    tr.move_to(box.get_center() + DOWN * 0.2)
    guard(tr.width <= box.width - 0.15, "trainer/ wider than the package box")
    scan = Line(box.get_corner(UP + LEFT) + RIGHT * 0.05, box.get_corner(UP + RIGHT) + LEFT * 0.05,
                color=LOOKUP, stroke_width=5)
    scene.play(name.animate.move_to(box.get_center() + UP * 0.2), FadeIn(tr, shift=UP * 0.1), run_time=0.4)
    scene.add(scan)
    scene.play(scan.animate.shift(DOWN * (box.height - 0.05)), run_time=0.6)
    scene.play(FadeOut(scan), flash(tr, TURN, 1.2, 0.5), run_time=0.5)
    mini.glyph.add(tr)


def batch_replay(mini: Miniature, run_time: float = 1.2):
    """The tray's four 2-column slices part along the cut lines and close again."""
    fr, tray, cuts = mini.glyph[0], mini.glyph[1], mini.glyph[2]
    slices = [VGroup(*[tray[r * 8 + c] for r in range(2) for c in (2 * j, 2 * j + 1)]) for j in range(4)]
    offs = (-0.16, -0.05, 0.05, 0.16)
    anims = [s.animate(rate_func=there_and_back_with_pause).shift(RIGHT * o) for s, o in zip(slices, offs)]
    anims += [c.animate(rate_func=there_and_back_with_pause).shift(RIGHT * o).set_stroke(width=4)
              for c, o in zip(cuts, (-0.105, 0.0, 0.105))]
    return AnimationGroup(*anims, run_time=run_time)


def job_id_chip(mini: Miniature):
    i = mono(JOB_ID, CAPTION, S.GREY)
    i.next_to(mini.glyph, RIGHT, buff=0.25)
    return i


class Recap(VoiceScene):
    def construct(self):
        assert len(SAY) == 7, len(SAY)

        # ========================================================== the row of six
        title = label("Six rules for Tuesday", 34, INK)
        row = miniature_row(MINI_KINDS, gap=0.45)
        row.move_to([0, -0.2, 0])
        place(title, cx=0, bottom=row.get_top()[1] + 0.6)
        minis = row.items
        strip_shift = STRIP_BOTTOM - row.get_bottom()[1]
        cols = {k: RuleColumn(minis[k], i % 2) for i, k in enumerate(MINI_KINDS)}
        inside(title, row)
        lr_slides = {"run": "15, 24", "package": "15, 24", "gpus": "27, 29", "batch": "27, 29",
                     "job": "10, 24", "data": "10, 24"}
        strip = row.copy().shift(UP * strip_shift)
        inside(strip)
        for k, c in cols.items():
            inside(c.target, c.head, c.tail)
            apart(c.target, c.head, 0.2)
            guard(c.tail.get_bottom()[1] >= strip.get_top()[1] + 0.25,
                  f"rule {k} reaches the strip ({c.tail.get_bottom()[1]:.2f})")
            below_tag(c.target, lr_slides[k])
            below_tag(c.head, lr_slides[k])
        for a, b in (("run", "package"), ("gpus", "batch"), ("job", "data")):
            apart(cols[a].text, cols[b].text, 0.3)
            apart(cols[a].target, cols[b].target, 0.3)
        jid = job_id_chip(cols["job"].target)
        inside(jid)
        apart(jid, cols["data"].target, 0.3)

        def rise(k):
            c = cols[k]
            return c.mini.animate.move_to(c.target.get_center())

        def rule_block(vo, k, i, replay):
            """Rise, replay with the head, then the tail at its cue."""
            c = cols[k]
            vo.wait_until(CUES[k][0])
            self.play(rise(k), run_time=0.8)
            self.play(replay(), Write(c.head), run_time=1.4)   # built after the rise (positions)
            vo.wait_until(CUES[k][1])
            self.play(Write(c.tail), run_time=1.6)

        # ---------------------------------------------------------- 0 · rule 1
        lr = None
        with self.voiceover(SAY[0]) as vo:
            lr = lref_swap(self, lr, "15, 24")
            self.play(Write(title), LaggedStart(*[FadeIn(m, shift=UP * 0.2) for m in row], lag_ratio=0.15),
                      run_time=1.4)
            vo.wait_until("Rule one")
            others = [minis[k] for k in MINI_KINDS if k != "run"]
            self.play(FadeOut(title), *[m.animate.shift(UP * strip_shift) for m in others], rise("run"),
                      run_time=0.9)
            self.play(minis["run"].replay(run_time=1.0), Write(cols["run"].head), run_time=1.4)
            vo.wait_until(CUES["run"][1])
            self.play(Write(cols["run"].tail), run_time=1.4)

        # ---------------------------------------------------------- 1 · rule 2
        with self.voiceover(SAY[1]) as vo:
            c = cols["package"]
            vo.wait_until(CUES["package"][0])
            self.play(rise("package"), run_time=0.8)
            package_replay(self, c.mini)
            self.play(Write(c.head), run_time=1.2)
            vo.wait_until(CUES["package"][1])
            self.play(Write(c.tail), run_time=1.6)

        # ---------------------------------------------------------- 2 · rule 3
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(cols["run"].all()), FadeOut(cols["package"].all()), run_time=0.6)
            lr = lref_swap(self, lr, "27, 29")
            rule_block(vo, "gpus", 2, lambda: minis["gpus"].replay(run_time=1.0))
            vo.wait_until("because separate")
            self.play(flash(cols["gpus"].tail[-1], TURN, 1.06, 0.8))

        # ---------------------------------------------------------- 3 · rule 4
        with self.voiceover(SAY[3]) as vo:
            rule_block(vo, "batch", 3, lambda: batch_replay(minis["batch"]))

        # ---------------------------------------------------------- 4 · rule 5
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(cols["gpus"].all()), FadeOut(cols["batch"].all()), run_time=0.6)
            lr = lref_swap(self, lr, "10, 24")
            c = cols["job"]
            vo.wait_until(CUES["job"][0])
            self.play(rise("job"), run_time=0.8)
            jid.move_to(job_id_chip(c.mini).get_center())
            c.extra.add(jid)
            self.play(minis["job"].replay(run_time=0.7), run_time=0.7)
            self.play(FadeIn(jid, shift=RIGHT * 0.3), Write(c.head), run_time=1.2)
            vo.wait_until(CUES["job"][1])
            self.play(Write(c.tail), run_time=1.4)

        # ---------------------------------------------------------- 5 · rule 6
        with self.voiceover(SAY[5]) as vo:
            rule_block(vo, "data", 5, lambda: minis["data"].replay(run_time=1.0))

        # ---------------------------------------------------------- 6 · LECTURE 5: three levers
        head = label(SLIDE5_TITLE, 28, S.GREY)
        place(head, cx=0, top=2.75)
        xs = (-4.2, 0.0, 4.2)
        pillars = VGroup()
        for x, name in zip(xs, PILLARS):
            cap = Rectangle(width=2.0, height=0.22, stroke_color=S.GREY, stroke_width=3)
            shaft = Rectangle(width=1.3, height=2.2, stroke_color=S.GREY, stroke_width=3).set_fill(S.GREY, 0.08)
            base = cap.copy()
            p = VGroup(cap, shaft, base).arrange(DOWN, buff=0)
            p.move_to([x, -0.55, 0])
            t = label(name, 26, INK).next_to(p, UP, buff=0.25)
            g = VGroup(t, p)
            g.shaft, g.text = shaft, t
            pillars.add(g)
        label_y = max(g.text.get_center()[1] for g in pillars)
        for g in pillars:
            g.text.set_y(label_y)
        floor = Line([-6.0, 0, 0], [6.0, 0, 0], color=S.GREY, stroke_width=3)
        floor.set_y(pillars[0][1].get_bottom()[1] - 0.05)
        book = note("+ the bookkeeping that shows whether it helped: W&B runs", color=S.GREY, size=24)
        place(book, cx=0, top=floor.get_y() - 0.35)
        inside(head, pillars, floor, book)
        for a, b in zip(pillars[:-1], pillars[1:]):
            apart(a, b, 0.3)
        apart(head, pillars, 0.3)
        apart(floor, book, 0.2)
        below_tag(head, "5")
        below_tag(pillars, "5")

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(cols["job"].all()), FadeOut(cols["data"].all()), run_time=0.6)
            lr = lref_swap(self, lr, "5")
            self.play(FadeIn(head, shift=DOWN * 0.15), Create(floor), run_time=0.8)
            for p, cue in zip(pillars, PILLAR_CUES):
                vo.wait_until(cue)
                self.play(FadeIn(p, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("Today was the hardware lever")
            hw = pillars[2]
            self.play(hw.shaft.animate.set_fill(TURN, 0.35).set_stroke(TURN),
                      hw[1][0].animate.set_stroke(TURN), hw[1][2].animate.set_stroke(TURN),
                      hw.text.animate.set_color(TURN),
                      pillars[0].animate.fade(0.5), pillars[1].animate.fade(0.5), run_time=0.8)
            vo.wait_until("plus the bookkeeping")
            self.play(FadeIn(book, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("Good luck")
            self.play(flash(hw, TURN, 1.04, 0.8))
        self.wait(0.6)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
        self.wait(0.3)
