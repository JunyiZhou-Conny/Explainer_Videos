"""S01 · The run with no curves (cold open of AC215 L13, exam edition). Lecture: 6, 8, 15–16.

Beats (script.md "## S01", one voiceover block each):
 0  Cold open, no lecture tag. V1 broken: the header "wandb.ai · project cheese-training-vertex-ai"
    with the `illustration` tag, one BLUE run row `mobilenetv2_train_base_True`; at "finished" the
    GREEN "finished" badge; at "the run exists" the header lights; at "Its config" the four config
    chips clip on one by one (learning_rate, epochs, batch_size, model_name); at "system charts"
    the system tile appears and its two traces draw left to right, once.
 1  At "no loss chart" two RED dashed chart outlines (loss, accuracy, GREY "no data logged") slide
    in under the row with an `illustration` tag; a YELLOW "?" pulses between them at "Where are the
    curves". At "Here is the line" the charts move left and CODE(task.py: 324–331) slides in on
    the right; the closing parenthesis of line 331 gets a faint YELLOW outline (no callback is
    pointed out). At "Hold that thought" the outline pulses once.
 2  LECTURE 6. Charts and "?" fade; the row and the code shrink into a text-free thumbnail in the
    top-left corner. Our redrawing of slide 6's roadmap: the long arrow POC → Prototype → MVP with
    dashed phase lines and five GREY pastel bars (Data Collection, Setup Experiment Tracking, Build
    Baseline Models, Build Better Models, ML Workflow); an arrow from the GREY lecture tag to the
    caption "the lecture slides behind each idea" at "The gray tag"; at "experiment tracking is
    set up early" a YELLOW dashed box draws around the tracking bar, at "together with the
    baseline models" it grows to hold both bars; at "right after data collection" the Data
    Collection bar flashes.
 3  The roadmap, caption and tag fade; the title "Lecture 13 · exam edition"; the five miniatures
    (run, package, GPUs, batch, job) with one-word captions; the corner thumbnail flies into the
    "run" miniature. At "quietly breaks" the GREY caption "where it quietly breaks"; each miniature
    lights (replay) and gets its RED crack as named.
 4  The title and caption fade; the miniatures move down to a strip at the bottom. Above: the
    sample YELLOW takeaway "If the question says X, think Y." writes in at "one rule"; beside it,
    at "Three times", a small YELLOW ponder card outline with A–D rows; at "Pause" its timer ring
    sweeps once (2 s); at "pick an answer" the A–D badges tick in turn; at "why each wrong option"
    one row turns YELLOW and the other three RED.
 5  LECTURE 8. The strip, line and card fade. Two GREY words from slide 8, "Reproducibility" and
    "Accountability", write in; at "If the question says" the YELLOW takeaway writes. Everything
    fades to an empty frame.
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    AnimationGroup,
    Arc,
    Arrow,
    Create,
    DashedLine,
    DashedVMobject,
    FadeIn,
    FadeOut,
    FadeTransform,
    GrowArrow,
    Indicate,
    LaggedStart,
    Line,
    Rectangle,
    RoundedRectangle,
    VGroup,
    Write,
    linear,
    there_and_back,
)

from common import guard as _guard
from common import *  # noqa: F401,F403
from explainer import style as S
from explainer.scene import VoiceScene

SAY = NARRATION["S01"]

# ------------------------------------------------------------------ the real sources
TASK = "package/trainer/task.py"
assert source_line(TASK, 326).startswith("training_results = model.fit("), source_line(TASK, 326)
assert source_line(TASK, 331) == ")", repr(source_line(TASK, 331))
assert "callbacks" not in excerpt(TASK, 324, 331)

ROADMAP_CAPTION = "the lecture slides behind each idea"
SAMPLE_RULE = "If the question says X, think Y."
RULE = "If the question says experiment tracking, think: what produced this result, and can I repeat it?"
SLIDE8_WORDS = ("Reproducibility", "Accountability")

SAFE = 6.6


# ------------------------------------------------------------------ layout helpers
def place(m, left=None, right=None, top=None, bottom=None, cx=None, cy=None):
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


def inside_frame(*mobs):
    for m in mobs:
        _guard(m.get_left()[0] >= -SAFE and m.get_right()[0] <= SAFE, f"x out of frame: {m.get_left()} {m.get_right()}")
        _guard(m.get_bottom()[1] >= -3.6 and m.get_top()[1] <= 3.6, f"y out of frame: {m.get_bottom()} {m.get_top()}")


def apart(a, b, gap: float = 0.05):
    sep = (a.get_right()[0] + gap <= b.get_left()[0] or b.get_right()[0] + gap <= a.get_left()[0]
           or a.get_top()[1] + gap <= b.get_bottom()[1] or b.get_top()[1] + gap <= a.get_bottom()[1])
    _guard(sep, f"overlap: {a.get_corner(DOWN + LEFT)} {a.get_corner(UP + RIGHT)} / "
                f"{b.get_corner(DOWN + LEFT)} {b.get_corner(UP + RIGHT)}")


def outline(mob, color=TURN, buff=0.06, stroke=2.5, opacity=0.7):
    return RoundedRectangle(width=mob.width + 2 * buff, height=mob.height + 2 * buff, corner_radius=0.06,
                            stroke_color=color, stroke_width=stroke, stroke_opacity=opacity) \
        .set_fill(opacity=0).move_to(mob)


def thumb_of(row, panel) -> VGroup:
    """A text-free thumbnail of the run row and the code panel (shapes only; scale freely)."""
    r = row.glyph_only()
    fr = RoundedRectangle(width=panel.width, height=panel.height, corner_radius=0.15, stroke_color=S.GREY,
                          stroke_width=3).set_fill(S.BG, 0.6)
    bars = VGroup(*[RoundedRectangle(width=w, height=0.16, corner_radius=0.05, stroke_width=0)
                    .set_fill(S.GREY, 0.6) for w in (3.6, 5.0, 4.2, 3.0, 2.4, 0.6)]) \
        .arrange(DOWN, aligned_edge=LEFT, buff=0.32)
    place(bars, left=fr.get_left()[0] + 0.4, top=fr.get_top()[1] - 0.6)
    p = VGroup(fr, bars)
    g = VGroup(r, p).arrange(RIGHT, buff=0.5)
    return g


# ------------------------------------------------------------------ slide 6, redrawn
PHASES = (("POC", -5.78, -2.97), ("Prototype", -2.97, 0.98), ("MVP", 0.98, 5.03))
# (text, left x, width): the slide's structure, bars widened to hold their 20 pt text
BARS = (("Data Collection", -5.78, 2.3), ("Setup Experiment Tracking", -5.78, 3.9),
        ("Build Baseline Models", -4.66, 3.4), ("Build Better Models", -2.34, 3.3),
        ("ML Workflow", -2.34, 3.3))


def roadmap() -> VGroup:
    """Slide 6 in our colours: the phase arrow, dashed boundaries, five GREY bars.
    .arrow .phases .lines .bars (each .frame .text)"""
    y_arrow, top_bar, pitch, bh = 1.55, 0.85, 0.66, 0.48
    arr = Arrow([-5.9, y_arrow, 0], [5.8, y_arrow, 0], buff=0, color=S.GREY, stroke_width=10,
                max_tip_length_to_length_ratio=0.03, max_stroke_width_to_length_ratio=12)
    phases = VGroup(*[label(n, 22, S.GREY).move_to([(a + b) / 2, y_arrow + 0.45, 0]) for n, a, b in PHASES])
    bottom = top_bar - (len(BARS) - 1) * pitch - bh / 2 - 0.1
    lines = VGroup(*[DashedLine([x, y_arrow - 0.25, 0], [x, bottom, 0], color=S.GREY_DARK, stroke_width=2,
                                dash_length=0.08) for x in (-2.97, 0.98, 5.03)])
    bars = VGroup()
    fills = (0.30, 0.22, 0.22, 0.16, 0.16)
    for k, ((t, x, w), op) in enumerate(zip(BARS, fills)):
        tx = label(t, 20, INK)
        _guard(tx.width + 0.3 <= w, f"roadmap bar {t!r} too narrow")
        fr = RoundedRectangle(width=w, height=bh, corner_radius=0.06, stroke_color=S.GREY,
                              stroke_width=1.5).set_fill(S.GREY, op)
        fr.move_to([x + w / 2, top_bar - k * pitch, 0])
        tx.move_to(fr)
        b = VGroup(fr, tx)
        b.frame, b.text = fr, tx
        bars.add(b)
    g = VGroup(arr, phases, lines, bars)
    g.arrow, g.phases, g.lines, g.bars = arr, phases, lines, bars
    return g


def dashed_box(mob, color=TURN, buff=0.14) -> VGroup:
    r = RoundedRectangle(width=mob.width + 2 * buff, height=mob.height + 2 * buff, corner_radius=0.1)
    return DashedVMobject(r, num_dashes=70, dashed_ratio=0.55).set_stroke(color, 3).move_to(mob)


# ------------------------------------------------------------------ the small ponder card (beat 4)
def mini_ponder(w: float = 3.4) -> VGroup:
    """A small YELLOW ponder-card outline: four rows (letter badge + GREY placeholder bar), a timer
    ring top right. .frame .rows (each .badge .bar) .ring_slot"""
    rows = VGroup()
    for letter, bw in zip("ABCD", (1.9, 1.5, 2.1, 1.7)):
        badge = step_badge(letter, S.GREY, size=TAG, radius=0.2)
        bar = RoundedRectangle(width=bw, height=0.16, corner_radius=0.06, stroke_width=0).set_fill(S.GREY, 0.6)
        bar.next_to(badge, RIGHT, buff=0.25)
        r = VGroup(badge, bar)
        r.badge, r.bar = badge, bar
        rows.add(r)
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    fr = RoundedRectangle(width=w, height=rows.height + 0.9, corner_radius=0.18, stroke_color=TURN,
                          stroke_width=3).set_fill(S.BG, 0.9)
    place(rows, left=fr.get_left()[0] + 0.35, bottom=fr.get_bottom()[1] + 0.3)
    g = VGroup(fr, rows)
    g.frame, g.rows = fr, rows
    g.ring_slot = lambda: fr.get_corner(UP + RIGHT) + np.array([-0.4, -0.35, 0])
    return g


# ------------------------------------------------------------------ the scene
class Hook(VoiceScene):
    def construct(self):
        assert len(SAY) == 6, len(SAY)

        # ========================================================== 0. the run that finished
        row = LedgerRow(RUN_NAME, width=9.0, full=True)
        head = VGroup(label("wandb.ai · project", CAPTION, CLOUD), mono(WB_PROJECT, CAPTION, INK)) \
            .arrange(RIGHT, buff=0.18)
        itag = illustration_tag()
        place(row, cx=0, top=2.95)
        place(head, left=row.get_left()[0] + 0.1, bottom=row.get_top()[1] + 0.18)
        place(itag, right=row.get_right()[0] - 0.1)
        itag.set_y(head.get_center()[1])
        apart(head, itag, 0.3)
        inside_frame(row, head, itag)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.15), FadeIn(itag), run_time=0.6)
            self.play(FadeIn(row, shift=LEFT * 0.4), run_time=0.8)
            vo.wait_until("finished without")
            self.play(*row.parts_in("finished", anim=lambda m: FadeIn(m, scale=1.3)), run_time=0.6)
            vo.wait_until("the run exists")
            self.play(Indicate(head[1], color=CLOUD, scale_factor=1.06), run_time=0.9)
            vo.wait_until("Its config")
            for k in CONFIG_KEYS:
                self.play(*row.clip(k), run_time=0.35)
            vo.wait_until("system charts")
            self.play(*row.parts_in("system"), run_time=0.4)
            self.play(*row.parts_in("traces", anim=lambda m: Create(m, rate_func=linear)), run_time=1.4)

        # ========================================================== 1. no curves; the fit call
        ch_loss, ch_acc = empty_chart("loss", w=2.5, h=1.9), empty_chart("accuracy", w=2.5, h=1.9)
        charts = VGroup(ch_loss, ch_acc).arrange(RIGHT, buff=0.6)
        place(charts, cx=0, top=row.get_bottom()[1] - 0.6)
        qm = S.text("?", 40, TURN).move_to(charts)
        ctag = illustration_tag()
        place(ctag, left=charts.get_left()[0], top=charts.get_bottom()[1] - 0.15)
        chart_grp = VGroup(charts, qm, ctag)

        panel = src_panel(TASK, 324, 331)
        place(panel, right=SAFE - 0.05, top=row.get_bottom()[1] - 0.3)
        paren = panel.span(331, ")")
        paren_box = outline(paren, TURN, buff=0.07, stroke=2.5, opacity=0.6)
        chart_left = chart_grp.copy()
        place(chart_left, left=-SAFE + 0.1)
        apart(chart_left, panel, 0.1)
        apart(row, panel, 0.1)
        apart(row, chart_grp, 0.1)
        inside_frame(chart_grp, panel, chart_left)

        with self.voiceover(SAY[1]) as vo:
            vo.wait_until("no loss chart")
            self.play(FadeIn(ch_loss, shift=UP * 0.4), FadeIn(ctag), run_time=0.7)
            vo.wait_until("no accuracy chart")
            self.play(FadeIn(ch_acc, shift=UP * 0.4), run_time=0.7)
            vo.wait_until("Where are the curves")
            self.play(FadeIn(qm, scale=1.5), run_time=0.4)
            self.play(qm.animate(rate_func=there_and_back).scale(1.35), run_time=0.8)
            vo.wait_until("Here is the line")
            self.play(chart_grp.animate.move_to(chart_left), FadeIn(panel, shift=LEFT * 0.8), run_time=0.9)
            self.play(Create(paren_box), run_time=0.6)
            vo.wait_until("Hold that thought")
            self.play(paren_box.animate(rate_func=there_and_back).set_stroke(TURN, 5, opacity=1), run_time=0.9)

        # ========================================================== 2. LECTURE 6 · the roadmap
        lr = lref("6")
        rm = roadmap()
        cap = note(ROADMAP_CAPTION)
        place(cap, right=lr.get_left()[0] - 0.9)
        cap.set_y(lr.get_center()[1])
        cap_arrow = Arrow(lr.get_left() + LEFT * 0.08, cap.get_right() + RIGHT * 0.08, buff=0, color=S.GREY,
                          stroke_width=3, max_tip_length_to_length_ratio=0.3)
        thumb = thumb_of(row, panel)
        thumb.scale_to_fit_width(2.6)
        place(thumb, left=-SAFE + 0.05, top=3.55)
        track, base, dc = rm.bars[1], rm.bars[2], rm.bars[0]
        box1 = dashed_box(track)
        box2 = dashed_box(VGroup(track, base))
        apart(thumb, cap, 0.2)
        apart(thumb, rm, 0.1)
        apart(cap, rm, 0.1)
        inside_frame(lr, rm, cap, thumb, box2)

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(chart_grp), run_time=0.4)
            self.play(FadeTransform(VGroup(row, head, itag, panel, paren_box), thumb), run_time=0.9)
            self.play(FadeIn(lr), run_time=0.4)
            self.play(GrowArrow(cap_arrow), FadeIn(cap, shift=LEFT * 0.2), run_time=0.6)
            vo.wait_until("On the lecture")
            self.play(GrowArrow(rm.arrow), LaggedStart(*[FadeIn(p) for p in rm.phases], lag_ratio=0.3),
                      run_time=0.9)
            self.play(LaggedStart(*[Create(ln) for ln in rm.lines], lag_ratio=0.2),
                      LaggedStart(*[FadeIn(b, shift=RIGHT * 0.3) for b in rm.bars], lag_ratio=0.25),
                      run_time=1.3)
            vo.wait_until("experiment tracking is set up early")
            self.play(Create(box1), track.frame.animate.set_stroke(TURN, 2.5), run_time=0.8)
            vo.wait_until("together with the baseline")
            self.play(box1.animate.become(box2), base.frame.animate.set_stroke(TURN, 2.5), run_time=0.8)
            vo.wait_until("right after data collection")
            self.play(Indicate(dc, color=INK, scale_factor=1.06), run_time=0.9)

        # ========================================================== 3. the map: five places
        title = label("Lecture 13 · exam edition", 30, INK)
        place(title, cx=0, top=2.7)
        minis = miniature_row()
        minis.move_to([0, 0.15, 0])
        breaks = note("where it quietly breaks", color=ERR)
        place(breaks, cx=0, top=minis.get_bottom()[1] - 0.45)
        apart(title, minis, 0.3)
        apart(minis, breaks, 0.2)
        inside_frame(title, minis, breaks)
        order = ("run", "package", "gpus", "batch", "job")
        cues = ("the run record", "the package", "the GPUs", "the batch", "the job itself")
        run_glyph = minis.items["run"]

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(rm), FadeOut(box1), FadeOut(cap), FadeOut(cap_arrow), FadeOut(lr), run_time=0.6)
            self.play(Write(title), run_time=0.8)
            vo.wait_until("five places")
            others = [minis.items[k] for k in order if k != "run"]
            self.play(FadeTransform(thumb, run_glyph),
                      LaggedStart(*[FadeIn(m, shift=UP * 0.2) for m in others], lag_ratio=0.2), run_time=1.2)
            vo.wait_until("quietly breaks")
            self.play(FadeIn(breaks, shift=UP * 0.1), run_time=0.5)
            for k, cue in zip(order, cues):
                vo.wait_until(cue)
                m = minis.items[k]
                self.play(m.replay(run_time=0.7), *m.crack(), run_time=0.7)

        # ========================================================== 4. how each part ends
        strip_y = -2.8
        rule = takeaway(SAMPLE_RULE)
        card = mini_ponder()
        top_row = VGroup(rule, card).arrange(RIGHT, buff=1.0).move_to([0, 0.75, 0])
        timer = Arc(radius=0.2, start_angle=np.pi / 2, angle=-2 * np.pi, color=TURN, stroke_width=4)
        timer.move_to(card.ring_slot())
        minis_low = minis.copy().set_y(strip_y)
        apart(top_row, minis_low, 0.4)
        inside_frame(top_row, minis_low)

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(title), FadeOut(breaks), minis.animate.set_y(strip_y), run_time=0.9)
            vo.wait_until("one rule")
            self.play(Write(rule), run_time=1.2)
            vo.wait_until("Three times")
            self.play(FadeIn(card, scale=0.9), run_time=0.6)
            vo.wait_until("Pause")
            self.play(Create(timer, rate_func=linear), run_time=2.0)
            vo.wait_until("pick an answer")
            self.play(LaggedStart(*[AnimationGroup(r.badge.animate(rate_func=there_and_back).scale(1.3),
                                                   r.bar.animate(rate_func=there_and_back).set_fill(TURN, 0.9))
                                    for r in card.rows], lag_ratio=0.5), run_time=1.6)
            vo.wait_until("why each wrong option")
            right = card.rows[1]
            wrong = [r for i, r in enumerate(card.rows) if i != 1]
            self.play(right.badge[0].animate.set_stroke(TURN), right.badge[1].animate.set_color(TURN),
                      right.bar.animate.set_fill(TURN, 0.9),
                      *[a for r in wrong for a in (r.badge[0].animate.set_stroke(ERR),
                                                    r.badge[1].animate.set_color(ERR),
                                                    r.bar.animate.set_fill(ERR, 0.8))], run_time=0.8)

        # ========================================================== 5. LECTURE 8 · the first rule
        lr8 = lref("8")
        words = VGroup(*[label(w, 30, S.GREY) for w in SLIDE8_WORDS]).arrange(RIGHT, buff=1.2)
        place(words, cx=0, cy=1.5)
        final = takeaway(RULE)
        final.move_to([0, -0.2, 0])
        apart(words, final, 0.3)
        apart(words, lr8, 0.3)
        inside_frame(words, final, lr8)

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(minis), FadeOut(rule), FadeOut(card), FadeOut(timer), run_time=0.6)
            self.play(FadeIn(lr8), run_time=0.4)
            self.play(LaggedStart(*[Write(w) for w in words], lag_ratio=0.5), run_time=1.4)
            vo.wait_until("If the question says")
            self.play(Write(final), run_time=2.0)
        self.wait(1.0)
        self.play(FadeOut(words), FadeOut(final), FadeOut(lr8), run_time=0.8)
        self.wait(0.3)
