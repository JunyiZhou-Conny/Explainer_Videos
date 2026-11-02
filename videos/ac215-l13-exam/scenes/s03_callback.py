"""S03 · The callback writes to the active run (V1 mechanism, four variants, the hook resolved).
Lecture: 15–16.

Beats (script.md "## S03", one voiceover block each):
 0  LECTURE 15. PONDER card 1 redrawn as it was (same question and options as S02), header
    "Answer". At "The answer is C" row C gets the YELLOW outline; rows A, B, D swap in place into
    their RED reasons as named.
 1  V1 mechanism. The card leaves. The ledger (illustration) with one open BLUE row (YELLOW
    outline) and the PINK `wandb.run` pointer on it. At "a pen" the PURPLE pen (the callback)
    appears; at "Keras holds" an epoch bar "fit · 3 epochs". At "At the end of every epoch" the
    first segment fills with the pen riding its end; at "calls wandb dot log" a GREY label
    "wandb.log → wandb.run" appears and the pen climbs to the pointer; at "writes to wandb dot
    run" it rides the arrow to the row and drops GREEN tick 1. At "whichever row is active" the
    row's outline and the arrow flash; at "not the run the pen was created with" the pen flashes.
 2  The ledger shrinks to a text-free thumbnail top right; CODE(cell-38.py: 42, 49, 55–61,
    folded, wrapped) slides in; the pen moves beside it. At "It calls init" line 42 lights BLUE,
    at "and then fit" line 55 lights, at "the Wandb Callback" line 60 lights PURPLE and a PINK line
    joins it to the pen.
 3  The panel leaves; the ledger grows back from the thumbnail. At "By default" a GREY chip
    `WandbMetricsLogger(log_freq="epoch")` + "default" beside the pen; at "one history entry per
    epoch" two more epochs run, the pen drops ticks 2 and 3. At "Per batch" a dimmer chip
    "per batch: log_freq="batch" or an int".
 4  Variant (a). A two-slot ledger; a fresh row "run 1", the pointer swings onto it, flow
    "init → fit · 2 epochs", GREY tag "callbacks: none" where the pen would be. At "Fit runs two
    epochs" two epochs run, no tick; at "the strip stays empty" the RED dashed outline and
    "0 entries"; at "our opening run" a GREY copy of the hook's empty loss outline flashes.
 5  Variant (b). Fresh row; flow "init → fit · 2 epochs → fit · 4 epochs" + GREY "no finish";
    the pen rides the arrow to the row; ticks 1–2, then the second bar (4 epochs) replaces the
    first; at "The pointer never moved" the arrow flashes; ticks 3–6 land on the same row;
    "6 entries · 1 run".
 6  Variant (c). Fresh row 1; flow "init → fit · 2 → finish → init → fit · 4"; the pen wears
    "created during row 1"; ticks 1–2; finish seals row 1, the arrow drops to None. At "then init
    again" row 2 slides in and the arrow swings onto it; at "and fit four epochs" the same pen
    (tag still on) rides the arrow down to row 2: ticks 1–4. Counters "row 1: 2" (lock flashes)
    and "row 2: 4"; the tag flashes at "made during row one", the arrow at "follows the pointer".
 7  Variant (d). Fresh row 1 with ticks 1–2; at "finish" it seals ("row 1: 2"), the arrow drops
    to None; flow "init → fit · 2 → finish → fit"; at "The first epoch trains" one segment fills;
    at "the pen follows the pointer" the pen climbs to the pointer and down into the None slot;
    at "stops with an error" the RED box `wandb.errors.Error: You must call wandb.init() before
    wandb.log()` with the PURPLE `wandb 0.15.11` chip under it; at "Nothing reaches any row" a RED
    ✗ at the pen, the count flashes.
 8  The first error box fades; in its place the second RED error: `WandbMetricsLogger()` with no
    active run → ``You must call `wandb.init()` before WandbMetricsLogger()`` + version chip.
 9  LECTURE 15–16. Back to the hook: the full row mobilenetv2_train_base_True (config, system
    charts, empty history) and two RED dashed chart outlines (illustration). At "imports both
    callbacks" CODE(task.py: 21–22), line 22 lit GREY, note "imported · unused"; at "passes none
    to fit" it transforms into CODE(task.py: 324–331); at "no curves" the outlines flash; at "The
    lecture's middle line" our redrawing of slide 15's middle line `callbacks=[WandbCallback()],`
    (GREEN dashed ghost, caption "the lecture's middle line") appears; at "the line that is
    missing" a gap opens before line 330, the ghost slides in, and the outlines fill with
    schematic curves.
10  A GREY card "the notebook prints: WandbCallback is deprecated → WandbMetricsLogger"; at "its
    replacement" the ghost line swaps to `callbacks=[WandbMetricsLogger()],`, GREY note "with a
    newer wandb pin".
11  Takeaway: the bracket timeline (init, fit · 2, finish, init, fit · 4, finish, fit) and the
    YELLOW line beside it; ticks drop into the brackets at "one per epoch", the brackets draw at
    "into whichever run is open", the stray fit's RED ✗ at "A finish ends the count", the second
    bracket flashes at "a new init starts". Fade to an empty frame.

Deviations from SHOW: beat 2 keeps the helper's honest header "lines 42–61 (folded)" (the first
quoted line is 42; line 41 is the "# W&B" comment, and adding it makes 13 rows) and the ledger
becomes a text-free thumbnail (shrinking it would take its text under 20 pt). Variant (a) also
shows the "init" chip and a GREY "callbacks: none" tag where the pen would be (the run is open,
only the pen is missing). The takeaway sits beside the bracket timeline (width 7.8), not centred.
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Create,
    DashedVMobject,
    DecimalNumber,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    Line,
    ReplacementTransform,
    RoundedRectangle,
    Text,
    VGroup,
    Write,
    there_and_back,
)

from common import *  # noqa: F401,F403
from common import guard
from explainer import style as S
from explainer.scene import VoiceScene

SAY = NARRATION["S03"]

# ------------------------------------------------------------------ the real sources
TASK = "package/trainer/task.py"
CELL = "colab/L13_wandb_tracking/cell-38.py"
assert source_line(CELL, 42).strip().startswith("wandb.init("), source_line(CELL, 42)
assert source_line(CELL, 55).strip().startswith("training_results = model.fit("), source_line(CELL, 55)
assert "callbacks=[WandbCallback(" in source_line(CELL, 60), source_line(CELL, 60)
assert source_line(TASK, 22).strip() == "from wandb.keras import WandbCallback, WandbMetricsLogger"
assert source_line(TASK, 326).startswith("training_results = model.fit("), source_line(TASK, 326)
assert source_line(TASK, 330).strip() == "verbose=1,", source_line(TASK, 330)
assert "callbacks" not in excerpt(TASK, 324, 331)

ANSWER_Q = ["`init(config=…)` → `fit` → `finish`. The run shows config, no loss curve.",
            "Which change adds a loss curve?"]
ANSWER_OPTS = ["`name=…` in `wandb.init`",
               '`wandb.config.update({"loss": …})` after fit',
               "`WandbMetricsLogger()` in fit's `callbacks`",
               "`wandb.login()` again before fit"]
REASONS = {0: "a name labels the row, logs nothing",
           1: "one number in config, not a history",
           3: "authenticates, logs nothing"}
GHOST_OLD = "callbacks=[WandbCallback()],"
GHOST_NEW = "callbacks=[WandbMetricsLogger()],"
RULE = ("If the question counts history entries, think: one per epoch, into whichever run is open when "
        "the epoch ends; finish ends the count, a new init starts a new one.")

SAFE = 6.6
LED_TOP, LED_RIGHT = 3.0, 6.5
PTR_TAIL = np.array([-3.4, 2.55, 0])
NONE_AT = np.array([-5.5, 1.3, 0])      # the pointer's None slot (left of the arrow's sweep)
REST1 = np.array([-4.4, -1.75, 0])        # the pen's rest (beats 1-3): its nib
REST2 = np.array([-5.6, -2.45, 0])        # the pen's rest (variants)
BAR_Y = -1.95                             # variant epoch bars (segments' centre)


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


def inside(*mobs, t: float = 3.6):
    for m in mobs:
        guard(m.get_left()[0] >= -SAFE and m.get_right()[0] <= SAFE and m.get_bottom()[1] >= -3.6
              and m.get_top()[1] <= t, f"outside the frame: {m.get_left()} {m.get_right()} "
                                       f"{m.get_bottom()} {m.get_top()}")


def apart(a, b, gap: float = 0.05):
    sep = (a.get_right()[0] + gap <= b.get_left()[0] or b.get_right()[0] + gap <= a.get_left()[0]
           or a.get_top()[1] + gap <= b.get_bottom()[1] or b.get_top()[1] + gap <= a.get_bottom()[1])
    guard(sep, f"overlap: {a.get_corner(DOWN + LEFT)} {a.get_corner(UP + RIGHT)} / "
               f"{b.get_corner(DOWN + LEFT)} {b.get_corner(UP + RIGHT)}")


def flash(mob, color=TURN, k: float = 1.12, run_time: float = 0.6):
    return Indicate(mob, color=color, scale_factor=k, run_time=run_time)


def text_free(m):
    """A copy of m without any text (the ledger's thumbnail: shapes only, scale freely)."""
    c = m.copy()

    def strip(x):
        for s in list(x.submobjects):
            if isinstance(s, (Text, DecimalNumber)) or hasattr(s, "pt"):
                x.remove(s)
            else:
                strip(s)
    strip(c)
    return c


def bar_at(n, caption, cx=0.0, cy=BAR_Y, width=4.0):
    """An EpochBar whose segments are centred at (cx, cy)."""
    b = EpochBar(n, width=width, caption=caption)
    b.shift(np.array([cx, cy, 0]) - b.segments.get_center())
    return b


def pulse(m, k: float = 1.12, run_time: float = 0.6):
    """Emphasis for filled tags and chips (Indicate would paint their fill over the text)."""
    return m.animate(rate_func=there_and_back, run_time=run_time).scale(k)


def put_pen(pen, nib):
    """Place the pen so its nib is at `nib` (no animation)."""
    pen.shift(np.array(nib) - pen.tip())
    return pen


def boxed(body, color, buff=0.18):
    fr = RoundedRectangle(width=body.width + 2 * buff, height=body.height + 2 * buff, corner_radius=0.1,
                          stroke_color=color, stroke_width=2.5).set_fill(S.BG, 0.92).move_to(body)
    return VGroup(fr, body)


def error_box(body):
    """A RED error box with the PURPLE `wandb 0.15.11` chip under its right end."""
    b = boxed(body, ERR)
    vc = version_chip()
    place(vc, right=b.get_right()[0], top=b.get_bottom()[1] - 0.1)
    g = VGroup(b, vc)
    g.chip = vc
    return g


# ------------------------------------------------------------------ the scene
class ActiveRun(VoiceScene):
    def epoch(self, bar, i, row, k, pen, rt=0.45):
        """One epoch: segment i fills, then the pen drops tick k into `row`."""
        self.play(bar.run(i, run_time=rt))
        self.play(pen.move_tip(row.slot_point(k) + UP * 0.22), run_time=0.25)
        self.play(*row.tick(k), run_time=0.25)

    def ride(self, pen, ptr, row, k=1, rt=0.45):
        """The pen climbs to the pointer, then rides its arrow to the row's strip slot k."""
        self.play(pen.move_tip(ptr.label.get_right() + RIGHT * 0.15 + DOWN * 0.1), run_time=rt)
        self.play(pen.move_tip(row.slot_point(k) + UP * 0.22), run_time=rt)

    def construct(self):
        assert len(SAY) == 12, len(SAY)

        # ========================================================== 0 · the answer to PONDER 1
        card = mcq_card(ANSWER_Q, ANSWER_OPTS, answer=True)
        inside(card)
        with self.voiceover(SAY[0]) as vo:
            lr = lref_swap(self, None, "15")
            self.play(FadeIn(card, scale=0.97), run_time=0.6)
            vo.wait_until("The answer is C")
            self.play(*card.mark_right(2), run_time=0.6)
            self.play(flash(card.options[2].text, TURN, 1.04, 0.8))
            for i, word in ((0, "a name only labels"), (1, "one number in the config"), (3, "logging in again")):
                vo.wait_until(word)
                self.play(*card.reason(i, REASONS[i]), run_time=0.8)

        # ========================================================== 1 · V1: the pen writes to wandb.run
        led1 = Ledger(slots=1)
        place(led1, right=LED_RIGHT, top=LED_TOP)
        row1 = led1.new_row(0, "run 1")
        ptr = RunPointer(tail=PTR_TAIL, none_at=NONE_AT)
        pen = put_pen(Pen(h=0.6), REST1)
        bar = EpochBar(3, width=4.5, caption="fit · 3 epochs")
        place(bar, cx=1.2, cy=-1.5)
        wl = VGroup(mono("wandb.log", CAPTION, S.GREY), label("→", CAPTION, S.GREY),
                    mono("wandb.run", CAPTION, S.GREY)).arrange(RIGHT, buff=0.15)
        place(wl, left=-6.2, cy=0.3)
        inside(led1, ptr, pen, bar, wl)
        apart(pen, bar, 0.2)
        apart(wl, led1, 0.1)
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(card), run_time=0.5)
            self.play(FadeIn(led1), FadeIn(row1, shift=LEFT * 0.4), FadeIn(ptr), run_time=0.8)
            self.play(*ptr.point_to(row1.pointer_point()), *row1.activate(), run_time=0.6)
            vo.wait_until("a pen")
            self.play(FadeIn(pen, shift=UP * 0.2), run_time=0.5)
            self.play(flash(pen, TOOL, 1.15), run_time=0.6)
            vo.wait_until("Keras holds")
            self.play(FadeIn(bar, shift=UP * 0.2), run_time=0.5)
            self.play(pen.move_tip(bar.segments[0].get_left() + UP * 0.2), run_time=0.5)
            vo.wait_until("At the end of every epoch")
            self.play(bar.run(0, run_time=1.0), pen.move_tip(bar.end(0) + UP * 0.2, run_time=1.0))
            vo.wait_until("it calls wandb dot log")
            self.play(FadeIn(wl, shift=RIGHT * 0.2),
                      pen.move_tip(ptr.label.get_right() + RIGHT * 0.15 + DOWN * 0.1), run_time=0.9)
            vo.wait_until("writes to wandb dot run")
            self.play(pen.move_tip(row1.slot_point(1) + UP * 0.22), flash(ptr.label, LOOKUP, 1.1), run_time=0.8)
            self.play(*row1.tick(1), run_time=0.4)
            vo.wait_until("whichever row is active")
            self.play(flash(row1.frame, TURN, 1.02, 0.8), flash(ptr.arrow, LOOKUP, 1.1, 0.8))
            vo.wait_until("not the run the pen")
            self.play(pen.move_tip(REST1), run_time=0.6)
            self.play(flash(pen, TOOL, 1.12))

        # ========================================================== 2 · the lecture's notebook
        main = VGroup(led1, row1, ptr)
        thumb = text_free(main)
        thumb.scale_to_fit_width(3.0)
        place(thumb, right=6.4, top=2.95)
        pnl = src_panel(CELL, [42, 49, (55, 61)], wrap=True)
        place(pnl, left=-6.45, bottom=-3.45)
        pen_at = np.array([4.3, -1.3, 0])
        pen2 = put_pen(pen.copy(), pen_at)
        inside(thumb, pnl, pen2)
        apart(thumb, pnl, 0.15)
        apart(pnl, pen2, 0.15)
        guard(thumb.get_top()[1] < 3.1, "thumbnail runs into the lecture tag")
        r60 = pnl.rows_of(60)
        y60 = pnl.code.code_lines[r60[0]].get_center()[1]
        with self.voiceover(SAY[2]) as vo:
            g_big = text_free(main)
            self.add(g_big)
            self.play(FadeOut(main), ReplacementTransform(g_big, thumb), FadeOut(VGroup(bar, wl)),
                      pen.move_tip(pen_at), run_time=0.9)
            self.play(FadeIn(pnl, shift=UP * 0.3), run_time=0.7)
            vo.wait_until("It calls init")
            b42 = pnl.bar(42, CLOUD, 0.25)
            self.play(FadeIn(b42), run_time=0.5)
            vo.wait_until("and then fit")
            b55 = pnl.bar(55, S.GREY, 0.2)
            self.play(FadeIn(b55), run_time=0.5)
            vo.wait_until("the Wandb Callback")
            b60 = VGroup(*[pnl.bar(60, TOOL, 0.28)])
            link = Line([pnl.code.background.get_right()[0] + 0.05, y60, 0], pen.barrel.get_left() + LEFT * 0.08,
                        color=LOOKUP, stroke_width=4)
            self.play(FadeIn(b60), run_time=0.5)
            self.play(Create(link), flash(pen, TOOL, 1.12), run_time=0.8)

        # ========================================================== 3 · one entry per epoch, by default
        dflt = VGroup(chip('WandbMetricsLogger(log_freq="epoch")', S.GREY, size=CAPTION, font=MONO),
                      note("default")).arrange(RIGHT, buff=0.2)
        place(dflt, left=-6.2, cy=-2.65)
        perb = boxed(fit_rows('per batch: `log_freq="batch"` or an int', 12, CAPTION, S.GREY), S.GREY_DARK, 0.12)
        place(perb, left=-6.2, cy=-3.25)
        inside(dflt, perb)
        with self.voiceover(SAY[3]) as vo:
            g_back = text_free(main)
            self.play(FadeOut(VGroup(pnl, b42, b55, b60, link)), run_time=0.5)
            self.play(ReplacementTransform(thumb, g_back), FadeIn(main), FadeIn(bar),
                      pen.move_tip(REST1), run_time=0.9)
            self.remove(g_back)
            apart(pen, dflt, 0.1)
            vo.wait_until("By default")
            self.play(FadeIn(dflt, shift=UP * 0.2), run_time=0.5)
            vo.wait_until("one history entry per epoch")
            for i, k in ((1, 2), (2, 3)):
                self.play(bar.run(i, run_time=0.6), pen.move_tip(bar.end(i) + UP * 0.2, run_time=0.6))
                self.play(pen.move_tip(row1.slot_point(k) + UP * 0.22), run_time=0.5)
                self.play(*row1.tick(k), run_time=0.3)
            self.play(pen.move_tip(REST1), run_time=0.5)
            vo.wait_until("Per batch")
            self.play(FadeIn(perb, shift=UP * 0.15), run_time=0.5)
            self.play(perb.animate.set_opacity(0.6), run_time=0.4)

        # ========================================================== 4 · variant (a): no pen
        led2 = Ledger(slots=2)
        place(led2, right=LED_RIGHT, top=LED_TOP)
        inside(led2)
        guard(ptr.none_slot.get_right()[0] < led2.get_left()[0] - 0.1, "None slot runs into the ledger")
        ra = led2.new_row(0, "run 1")
        fa = flow(["init", "fit · 2 epochs"])
        place(fa, right=6.4, cy=-1.0)
        nopen = grey_tag("callbacks: none")
        place(nopen, left=REST2[0], cy=BAR_Y)
        bar_a = bar_at(2, "fit · 2 epochs")
        ghost_loss = empty_chart("loss", w=2.6, h=1.4)
        ghost_loss.frame.set_stroke(S.GREY)
        place(ghost_loss, right=6.3, top=-1.55)
        inside(fa, nopen, bar_a, ghost_loss)
        apart(fa, led2, 0.05)
        apart(bar_a, fa, 0.1)
        apart(bar_a, ghost_loss, 0.2)
        apart(nopen, bar_a, 0.2)
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(pen, bar, dflt, perb, row1)), *ptr.to_none(), run_time=0.6)
            self.play(ReplacementTransform(led1, led2), run_time=0.7)
            vo.wait_until("First, no pen")
            self.play(FadeIn(ra, shift=LEFT * 0.4), FadeIn(fa.items[0]), run_time=0.6)
            self.play(*ptr.point_to(ra.pointer_point()), *ra.activate(), fa.light(0), run_time=0.6)
            self.play(FadeIn(nopen, shift=UP * 0.15), run_time=0.4)
            vo.wait_until("Fit runs two epochs")
            self.play(FadeIn(VGroup(*fa[1:])), FadeIn(bar_a), run_time=0.5)
            self.play(fa.light(1), run_time=0.3)
            self.play(bar_a.run(0, run_time=0.7))
            self.play(bar_a.run(1, run_time=0.7))
            vo.wait_until("the strip stays empty")
            self.play(*ra.parts_in("empty"), *ra.set_count("0 entries"), run_time=0.6)
            self.play(flash(ra.parts["empty"], ERR, 1.04))
            vo.wait_until("That is our opening run")
            self.play(FadeIn(ghost_loss, shift=LEFT * 0.3), run_time=0.5)
            self.play(flash(ghost_loss.frame, S.GREY, 1.06, 0.7))

        # ========================================================== 5 · variant (b): two fits, no finish
        rb = led2.new_row(0, "run 1")
        fb = flow(["init", "fit · 2 epochs", "fit · 4 epochs"])
        place(fb, right=6.4, cy=-1.0)
        nofin = grey_tag("no finish")
        place(nofin, right=fb.get_left()[0] - 0.3, cy=-1.0)
        b1, b2 = bar_at(2, "fit · 2 epochs"), bar_at(4, "fit · 4 epochs")
        put_pen(pen, REST2)
        inside(fb, nofin, b1, b2, pen)
        apart(fb, led2, 0.05)
        apart(nofin, pen, 0.1)
        apart(b2, pen, 0.2)
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(ra, fa, nopen, bar_a, ghost_loss)), *ptr.to_none(), run_time=0.6)
            vo.wait_until("init")
            self.play(FadeIn(rb, shift=LEFT * 0.4), FadeIn(fb), FadeIn(pen), run_time=0.6)
            self.play(*ptr.point_to(rb.pointer_point()), *rb.activate(), fb.light(0), run_time=0.5)
            self.ride(pen, ptr, rb, rt=0.35)
            vo.wait_until("fit for two epochs")
            self.play(FadeIn(b1), fb.light(1), run_time=0.4)
            for i in range(2):
                self.epoch(b1, i, rb, i + 1, pen, rt=0.4)
            vo.wait_until("then fit for four more")
            self.play(ReplacementTransform(b1, b2), fb.light(2), run_time=0.5)
            vo.wait_until("with no finish")
            self.play(FadeIn(nofin, shift=RIGHT * 0.2), run_time=0.4)
            self.play(pulse(nofin))
            vo.wait_until("The pointer never moved")
            self.play(flash(ptr.arrow, LOOKUP, 1.15, 0.7))
            vo.wait_until("so ticks three to six")
            for i in range(4):
                self.epoch(b2, i, rb, i + 3, pen, rt=0.35)
            vo.wait_until("One run, six entries")
            self.play(*rb.set_count("6 entries · 1 run"), run_time=0.5)
            self.play(flash(rb.count, INK, 1.08))

        # ========================================================== 6 · variant (c): finish, init, same pen
        rc1 = led2.new_row(0, "run 1")
        rc2 = led2.new_row(1, "run 2")
        fc = flow(["init", "fit · 2", "finish", "init", "fit · 4"])
        place(fc, right=6.4, cy=-1.0)
        c1, c2 = bar_at(2, "fit · 2"), bar_at(4, "fit · 4")
        inside(fc, c1, c2)
        apart(fc, led2, 0.05)
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(rb, fb, nofin, b2)), pen.move_tip(REST2), *ptr.to_none(), run_time=0.6)
            self.play(FadeIn(rc1, shift=LEFT * 0.4), FadeIn(fc), run_time=0.6)
            self.play(*ptr.point_to(rc1.pointer_point()), *rc1.activate(), fc.light(0), run_time=0.4)
            self.ride(pen, ptr, rc1, rt=0.3)
            self.play(*pen.wear("created during row 1"), run_time=0.5)
            self.play(FadeIn(c1), fc.light(1), run_time=0.3)
            for i in range(2):
                self.epoch(c1, i, rc1, i + 1, pen, rt=0.3)
            vo.wait_until("then init again")
            self.play(fc.light(2), *rc1.seal(), *ptr.to_none(), run_time=0.6)
            self.play(FadeIn(rc2, shift=LEFT * 0.4), fc.light(3), run_time=0.5)
            self.play(*ptr.point_to(rc2.pointer_point()), *rc2.activate(), run_time=0.5)
            vo.wait_until("and fit four epochs")
            self.play(ReplacementTransform(c1, c2), fc.light(4), run_time=0.4)
            self.ride(pen, ptr, rc2, rt=0.35)
            for i in range(4):
                self.epoch(c2, i, rc2, i + 1, pen, rt=0.3)
            vo.wait_until("The first row is sealed")
            self.play(*rc1.set_count("row 1: 2"), run_time=0.5)
            self.play(flash(rc1.parts["lock"], S.GREY, 1.3))
            vo.wait_until("The callback was made during row one")
            self.play(pulse(pen.badge, 1.1, 0.8))
            vo.wait_until("but it follows the pointer")
            self.play(flash(ptr.arrow, LOOKUP, 1.15, 0.7))
            vo.wait_until("so the new row gets")
            self.play(*rc2.set_count("row 2: 4"), run_time=0.5)
            self.play(flash(rc2.count, INK, 1.08))

        # ========================================================== 7 · variant (d): finish, then fit
        rd = led2.new_row(0, "run 1")
        fd = flow(["init", "fit · 2", "finish", "fit"])
        place(fd, right=6.4, cy=-1.0)
        d1 = bar_at(2, "fit")
        err1 = error_box(mono(ERR_LOG, CAPTION, ERR))
        place(err1, cx=0.0, bottom=-3.45)
        inside(fd, d1, err1)
        apart(d1, err1, 0.05)
        none_nib = ptr.none_slot.get_top() + DOWN * 0.05
        with self.voiceover(SAY[7]) as vo:
            badge = pen.badge
            pen.remove(badge)
            self.play(FadeOut(VGroup(rc1, rc2, fc, c2, badge)), *ptr.to_none(), run_time=0.6)
            self.play(pen.move_tip(REST2), run_time=0.5)
            self.play(FadeIn(rd, shift=LEFT * 0.4), FadeIn(fd), run_time=0.5)
            self.play(*ptr.point_to(rd.pointer_point()), *rd.activate(), fd.light(0), run_time=0.4)
            self.play(*rd.tick(1), *rd.tick(2), fd.light(1), run_time=0.5)
            vo.wait_until("finish")
            self.play(fd.light(2), *rd.seal(), *ptr.to_none(), *rd.set_count("row 1: 2"), run_time=0.7)
            vo.wait_until("then fit again")
            self.play(fd.light(3), FadeIn(d1), run_time=0.5)
            self.play(pen.move_tip(d1.segments[0].get_left() + UP * 0.2), run_time=0.5)
            vo.wait_until("The first epoch trains")
            self.play(d1.run(0, run_time=1.0), pen.move_tip(d1.end(0) + UP * 0.2, run_time=1.0))
            vo.wait_until("the pen follows the pointer")
            self.play(pen.move_tip(ptr.label.get_right() + RIGHT * 0.15 + DOWN * 0.1), run_time=0.6)
            self.play(pen.move_tip(none_nib), flash(ptr.none_slot, S.GREY, 1.1), run_time=0.6)
            vo.wait_until("stops with an error")
            self.play(FadeIn(err1, shift=UP * 0.2), run_time=0.6)
            self.play(pulse(err1.chip))
            vo.wait_until("Nothing reaches any row")
            xm = x_mark(0.34)
            place(xm, cx=ptr.none_slot.get_center()[0], top=ptr.none_slot.get_bottom()[1] - 0.12)
            inside(xm)
            self.play(FadeIn(xm, scale=1.4), flash(rd.count, ERR, 1.1), run_time=0.6)

        # ========================================================== 8 · the logger with no active run
        r1 = VGroup(mono("WandbMetricsLogger()", CAPTION, ERR), note("with no active run")).arrange(RIGHT, buff=0.2)
        r2 = VGroup(label("→", CAPTION, ERR), mono(ERR_LOGGER, CAPTION, ERR)).arrange(RIGHT, buff=0.15)
        body = VGroup(r1, r2).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        err2 = error_box(body)
        place(err2, cx=0.0, bottom=-3.45)
        inside(err2)
        apart(err2, fd, 0.05)
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(err1), FadeOut(d1), run_time=0.5)
            self.play(FadeIn(err2, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("fails at once")
            self.play(flash(r2, ERR, 1.04, 0.7))

        # ========================================================== 9 · back to the hook
        row = LedgerRow(RUN_NAME, width=9.0, full=True)
        row.parts_in(*[f"cfg:{k}" for k in CONFIG_KEYS], "system", "traces", "finished", "empty")
        place(row, cx=0.0, top=3.0)
        ch_l, ch_a = empty_chart("loss", w=2.5, h=1.5), empty_chart("accuracy", w=2.5, h=1.5)
        charts = VGroup(ch_l, ch_a).arrange(RIGHT, buff=0.35)
        place(charts, left=-6.45, top=row.get_bottom()[1] - 0.75)
        ctag = illustration_tag()
        place(ctag, left=-6.45, bottom=charts.get_top()[1] + 0.12)
        p21 = src_panel(TASK, 21, 22)
        place(p21, cx=0.0, bottom=-3.45)
        b22 = p21.bar(22, S.GREY, 0.25)
        unused = note("imported · unused")
        place(unused, right=6.4, bottom=p21.get_top()[1] + 0.12)
        p324 = src_panel(TASK, 324, 331)
        place(p324, right=6.45, top=0.5)
        code = p324.code
        pitch = code.code_lines[5].get_center()[1] - code.code_lines[6].get_center()[1]
        ghost_t = mono(GHOST_OLD, 22, OWN)
        ghost_fr = DashedVMobject(RoundedRectangle(width=ghost_t.width + 0.3, height=ghost_t.height + 0.3,
                                                   corner_radius=0.08), num_dashes=40).set_stroke(OWN, 2.5)
        ghost_fr.move_to(ghost_t)
        gcap = note("the lecture's middle line")
        ghost = VGroup(ghost_fr, ghost_t)
        place(ghost, left=-6.45, top=charts.get_bottom()[1] - 0.75)
        place(gcap, left=-6.45, bottom=ghost.get_top()[1] + 0.1)
        g_target = np.array([code.code_lines[5].get_left()[0] + ghost_t.width / 2, code.code_lines[6].get_center()[1], 0])
        inside(row, charts, ctag, p21, unused, p324, ghost, gcap)
        apart(row, charts, 0.1)
        apart(row, ctag, 0.1)
        apart(charts, p21, 0.1)
        apart(charts, p324, 0.1)
        apart(row, p324, 0.1)
        apart(row, unused, 0.1)
        apart(charts, unused, 0.1)
        apart(ghost, p324, 0.1)
        apart(gcap, charts, 0.05)
        guard(p324.get_bottom()[1] - pitch >= -3.6, "the opened gap pushes the panel out of the frame")
        guard(g_target[0] + ghost_t.width / 2 + 0.05 <= code.background.get_right()[0],
              "the ghost line is wider than the panel")
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(VGroup(led2, ptr, rd, pen, fd, err2, xm)), run_time=0.6)
            lr = lref_swap(self, lr, "15–16")
            vo.wait_until("Now the hook")
            self.play(FadeIn(row, shift=DOWN * 0.2), FadeIn(charts), FadeIn(ctag), run_time=0.7)
            vo.wait_until("imports both callbacks")
            self.play(FadeIn(p21, shift=UP * 0.2), run_time=0.5)
            self.play(FadeIn(b22), FadeIn(unused, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("passes none to fit")
            self.play(FadeOut(VGroup(b22, unused)), ReplacementTransform(p21, p324), run_time=0.8)
            vo.wait_until("and no curves")
            self.play(flash(ch_l.frame, ERR, 1.04), flash(ch_a.frame, ERR, 1.04), flash(row.parts["empty"], ERR, 1.03))
            vo.wait_until("The lecture's middle line")
            self.play(FadeIn(gcap), FadeIn(ghost, shift=RIGHT * 0.3), run_time=0.6)
            vo.wait_until("the line that is missing")
            self.play(code.code_lines[6].animate.shift(DOWN * pitch), code.code_lines[7].animate.shift(DOWN * pitch),
                      code.background.animate.stretch_to_fit_height(code.background.height + pitch, about_edge=UP),
                      run_time=0.6)
            self.play(ghost_t.animate.move_to(g_target), FadeOut(ghost_fr), FadeOut(gcap), run_time=0.9)
            cl, ca = curve_in(ch_l, "loss"), curve_in(ch_a, "accuracy")
            self.play(Create(cl), Create(ca), FadeOut(ch_l.caption), FadeOut(ch_a.caption), run_time=1.0)
        inside(p324)

        # ========================================================== 10 · WandbCallback is deprecated
        dep = boxed(VGroup(note("the notebook prints:"),
                           VGroup(mono("WandbCallback", CAPTION, INK), note("is deprecated")).arrange(RIGHT, buff=0.15),
                           VGroup(label("→", CAPTION, S.GREY), mono("WandbMetricsLogger", CAPTION, INK))
                           .arrange(RIGHT, buff=0.15)).arrange(DOWN, aligned_edge=LEFT, buff=0.12), S.GREY)
        place(dep, left=-6.45, top=charts.get_top()[1])
        ghost_new = mono(GHOST_NEW, 22, OWN)
        ghost_new.move_to(ghost_t, aligned_edge=LEFT)
        pin_note = note("with a newer wandb pin")
        place(pin_note, right=code.background.get_left()[0] - 0.2, cy=ghost_new.get_center()[1])
        inside(dep, ghost_new, pin_note)
        apart(dep, p324, 0.1)
        apart(pin_note, p324, 0.1)
        apart(pin_note, dep, 0.1)
        guard(ghost_new.get_right()[0] + 0.05 <= code.background.get_right()[0], "the new ghost line overruns the panel")
        gh_parent = VGroup(ghost_t)
        with self.voiceover(SAY[10]) as vo:
            vo.wait_until("the notebook warns")
            self.play(FadeOut(VGroup(charts, ctag, cl, ca)), run_time=0.5)
            self.play(FadeIn(dep, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("its replacement")
            self.play(*swap_text(gh_parent, ghost_t, ghost_new), FadeIn(pin_note, shift=UP * 0.1), run_time=1.0)
            self.play(flash(ghost_new, OWN, 1.05, 0.7))

        # ========================================================== 11 · takeaway over the bracket timeline
        bt = BracketTimeline()
        place(bt, left=-6.2, cy=0.0)
        tk = takeaway(RULE, width=7.8)
        place(tk, right=6.4, cy=0.0)
        ticks = VGroup(*[history_tick().move_to(p) for p in bt.tick_points(1, 2) + bt.tick_points(4, 4)])
        inside(bt, tk, ticks)
        apart(VGroup(bt, ticks), tk, 0.3)
        with self.voiceover(SAY[11]) as vo:
            self.play(FadeOut(VGroup(row, p324, ghost_new, dep, pin_note)), FadeOut(lr),
                      run_time=0.6)
            self.play(FadeIn(bt.rows, lag_ratio=0.1), Write(tk), run_time=1.6)
            vo.wait_until("one per epoch")
            self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.2) for t in ticks], lag_ratio=0.25), run_time=1.2)
            vo.wait_until("into whichever run is open")
            self.play(Create(bt.brackets), run_time=0.8)
            vo.wait_until("A finish ends the count")
            self.play(FadeIn(bt.cross, scale=1.4), run_time=0.5)
            vo.wait_until("a new init starts")
            self.play(flash(bt.brackets[1], TURN, 1.08, 0.7))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
        self.wait(0.3)
