"""S06 · Global batch, per-replica batch (V4, the batch splitter; task_multi_gpu.py's multiplication).
Lecture: 28–29.

Beats (script.md "## S06", one voiceover block each):
 0  LECTURE 28–29. V4: a GREEN tray `dataset.batch(n)` (16 image squares, GREY "global batch")
    above a PURPLE MirroredStrategy frame round four BLUE T4 chips. On "cuts that tray" PINK
    dashed cut lines divide the tray into four equal slices and PINK splitter arrows point down;
    the slices slide one onto each GPU (GREY "one slice per replica"), the tray's place stays as a
    GREY dashed outline. The counter writes at the bottom: `global = per-replica × replicas`.
 1  The counter rewrites as `per-replica = global ÷ num_replicas_in_sync` (the slices pulse,
    then the whole batch), and on "Turn it around" flips back.
 2  Dial play with 8 replicas: the tray and the four GPUs leave; eight T4 chips (two rows of
    four, "8 replicas") on the right, a tray of 16 with a dial `batch(16)` on the left. GREY tag
    "intended: 16" under the GPUs. "Batch by 16": PINK arrows, the tray splits into 8 slices of
    2; the readout `16 ÷ 8 = 2` writes in RED and the tag turns RED. "Batch by 128": the dial
    turns, a tray of 128 replaces the old slices; "Each GPU gets 16": it splits into 8 slices of
    16, the readout becomes `128 ÷ 8 = 16` in GREEN, the tag turns GREEN, a GREEN tick.
 3  The picture leaves (the counter stays); CODE(task_multi_gpu.py: 291–301) at the top. On
    "multiplies it by the replica count" line 293 lights GREEN and the counter flies onto it; on
    "hands the product" line 300 lights PINK and the excerpt chip `task_multi_gpu.py · line 198
    (excerpt)` `train_data = train_data.batch(batch_size)` comes in under the panel; on "Its own
    comment" line 292 lights YELLOW and slide 29's call-out writes in GREY ("Adjust dataset batch
    size"), then the GREY note "repo: 32 × 2 replicas = 64".
 4  Everything fades (lecture tag too). PONDER card 2 (mcq_card, centred). After the block the
    timer drains (10 s, silent); the card fades.
 5  The same card returns with the header "Answer"; row B gets the YELLOW outline. On "The
    trainer multiplies first" the card steps aside: the counter `32 × 4 = 128` writes, a tray of
    128 splits into four slices of 32 on four GPUs ("32 each"). On "A: that is" the demo leaves
    and the card returns; rows A, C, D swap in place into their RED reasons as named.
 6  Takeaway (YELLOW, centred): "If the question says per replica, multiply before you batch:
    global = per-replica × replicas." Fade to an empty frame.

Deviations from SHOW: beat 2 shows the per-GPU count once, as a readout `16 ÷ 8 = 2` under the
GPU grid, instead of a "2" on each of the 8 slices (a label above each slice has no room between
the two chip rows); beat 5 lets the answer card step out while the tray of 128 splits (a tray, four
GPUs and a 12.4 × 5.2 card do not share the frame), then brings the same card back for the reasons.
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Create,
    DashedLine,
    DashedVMobject,
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
    LaggedStart,
    VGroup,
    Write,
    linear,
)

from common import *  # noqa: F401,F403
from common import guard
from explainer import style as S
from explainer.scene import VoiceScene

SAY = NARRATION["S06"]

# ------------------------------------------------------------------ the real sources
MGPU = "package/trainer/task_multi_gpu.py"
assert source_line(MGPU, 198).strip() == "train_data = train_data.batch(batch_size)", source_line(MGPU, 198)
assert source_line(MGPU, 289).strip() == "num_workers = strategy.num_replicas_in_sync", source_line(MGPU, 289)
assert "expects the global batch size" in source_line(MGPU, 292), source_line(MGPU, 292)
assert source_line(MGPU, 293).strip() == "global_batch_size = args.batch_size * num_workers", source_line(MGPU, 293)
assert source_line(MGPU, 300).strip() == "batch_size=global_batch_size,", source_line(MGPU, 300)
assert "--batch_size=32" in source_line("cli-multi-gpu.sh", 16), source_line("cli-multi-gpu.sh", 16)
assert source_line("cli-multi-gpu.sh", 12).strip() == "export ACCELERATOR_COUNT=2", source_line("cli-multi-gpu.sh", 12)
# the dial and the ponder (script.md "Numbers")
assert 16 // 8 == 2 and 128 // 8 == 16 and 32 * 4 == 128 and 128 // 4 == 32 and 32 * 2 == 64

RULE_MUL = "global = per-replica × replicas"
RULE_DIV = "per-replica = global ÷ num_replicas_in_sync"
PONDER_Q = ["The repo's multi-GPU trainer runs on 4 GPUs with `--batch_size=32`.",
            "Global batch, and per GPU per step?"]
PONDER_OPTS = ["global 32 · 8 per GPU", "global 128 · 32 per GPU", "global 32 · 32 per GPU",
               "global 128 · 128 per GPU"]
RIGHT_I = 1
REASONS = {0: "a script that never multiplied", 2: "the flag is per replica, not global",
           3: "the global batch is split, not copied"}
for _o in PONDER_OPTS:
    assert len(_o) <= 46, _o
SAFE = 6.6


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


def below_tag(m, slides: str = "28–29"):
    t = lref(slides)
    guard(m.get_top()[1] <= t.get_bottom()[1] - 0.05 or m.get_right()[0] <= t.get_left()[0] - 0.05,
          "under the lecture tag")


def flash(mob, color=TURN, k: float = 1.12, run_time: float = 0.6):
    return Indicate(mob, color=color, scale_factor=k, run_time=run_time)


def cut_lines(tray: BatchTray, k: int) -> VGroup:
    """PINK dashed lines between the tray's k column-block slices."""
    sl = tray.slices(k)
    top, bot = tray.frame.get_top()[1] + 0.05, tray.frame.get_bottom()[1] - 0.05
    out = VGroup()
    for a, b in zip(sl[:-1], sl[1:]):
        x = (a.get_right()[0] + b.get_left()[0]) / 2
        out.add(DashedLine([x, top, 0], [x, bot, 0], color=LOOKUP, stroke_width=3, dash_length=0.08))
    return out


def split_arrows(tray: BatchTray, points, k: int) -> VGroup:
    """PINK arrows from each slice's spot on the tray to its landing point."""
    sl = tray.slices(k)
    out = VGroup()
    for g, p in zip(sl, points):
        start = np.array([g.get_center()[0], tray.frame.get_bottom()[1] - 0.05, 0])
        end = np.array(p) + UP * 0.05
        out.add(Arrow(start, end, color=LOOKUP, stroke_width=3, buff=0.05, max_tip_length_to_length_ratio=0.12,
                      tip_length=0.16))
    return out


class GlobalBatch(VoiceScene):
    def construct(self):
        assert len(SAY) == 7, len(SAY)

        # ========================================================== 0 · V4: the tray and the splitter
        tray = BatchTray(16, cols=8, cell=0.3, caption="dataset.batch(n)")
        place(tray, cx=0, top=2.95)
        g_lab = label("global batch", 22, S.GREY)
        place(g_lab, right=tray.frame.get_left()[0] - 0.3, cy=tray.frame.get_center()[1])
        grid = gpu_grid(4)
        place(grid, cx=0, cy=-0.75)
        r_lab = label("one slice per replica", 22, S.GREY)
        place(r_lab, left=grid.get_right()[0] + 0.25, cy=grid.chips.get_center()[1] + 0.35)
        rule = VGroup(mono(RULE_MUL, 26, INK))
        place(rule, cx=0, cy=-2.95)
        cuts = cut_lines(tray, 4)
        ghost = DashedVMobject(tray.frame.copy().set_fill(opacity=0).set_stroke(S.GREY, 2), num_dashes=40)
        arrows0 = split_arrows(tray, [grid.slot(i) + UP * 0.35 for i in range(4)], 4)
        inside(tray, g_lab, grid, r_lab, rule)
        below_tag(tray)
        apart(tray, grid, 0.2)
        apart(grid, rule, 0.2)
        apart(g_lab, tray, 0.2)
        apart(r_lab, grid, 0.15)
        with self.voiceover(SAY[0]) as vo:
            lr = lref_swap(self, None, "28–29")
            self.play(FadeIn(tray, shift=DOWN * 0.2), run_time=0.8)
            vo.wait_until("Under a strategy")
            self.play(FadeIn(grid), run_time=0.8)
            vo.wait_until("is the global batch")
            self.play(FadeIn(g_lab, shift=RIGHT * 0.15), flash(tray.frame, OWN, 1.05, 0.8), run_time=0.8)
            vo.wait_until("The strategy cuts")
            self.play(Create(cuts), run_time=0.7)
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows0], lag_ratio=0.15), run_time=0.8)
            vo.wait_until("one per replica")
            self.play(*tray.split_to([grid.slot(i) for i in range(4)], 4, cols=2), FadeOut(cuts), FadeOut(arrows0),
                      FadeIn(ghost), run_time=1.2)
            tray.remove(tray.frame)
            self.play(FadeIn(r_lab, shift=LEFT * 0.15), Write(rule), run_time=1.0)
        slices0 = tray.slices(4)

        # ========================================================== 1 · the counter, both ways round
        rule_div = mono(RULE_DIV, 26, INK).move_to(rule[0])
        rule_mul = mono(RULE_MUL, 26, INK).move_to(rule[0])
        inside(rule_div)
        with self.voiceover(SAY[1]) as vo:
            self.play(*swap_text(rule, rule[0], rule_div), run_time=1.0)
            vo.wait_until("the global batch divided")
            self.play(flash(VGroup(*slices0), OWN, 1.06, 0.8))
            vo.wait_until("the number of replicas")
            self.play(flash(grid.chips, CLOUD, 1.06, 0.8))
            vo.wait_until("Turn it around")
            self.play(*swap_text(rule, rule_div, rule_mul), run_time=1.0)
            vo.wait_until("times the replicas")
            self.play(flash(rule_mul, TURN, 1.05, 0.8))

        # ========================================================== 2 · the dial: 8 replicas
        grid8 = gpu_grid(8, per_row=4)
        place(grid8, right=6.2, top=2.55)
        n_lab = label("8 replicas", 22, S.GREY)
        place(n_lab, cx=grid8.get_center()[0], bottom=grid8.get_top()[1] + 0.1)
        tray16 = BatchTray(16, cols=8, cell=0.3, caption=None)
        tray128 = BatchTray(128, cols=16, cell=0.16, caption=None)
        place(tray128, cx=-3.9, cy=1.2)
        place(tray16, cx=-3.9, cy=1.2)
        dial = BatchDial(16)
        place(dial, cx=-3.9, top=tray128.frame.get_bottom()[1] - 0.35)
        intended = tag("intended: 16", S.GREY, size=22)
        read16 = mono("16 ÷ 8 = 2", 26, ERR)
        read128 = mono("128 ÷ 8 = 16", 26, OWN)
        readout = VGroup(read16, intended).arrange(RIGHT, buff=0.35)
        place(readout, cx=grid8.get_center()[0] - 0.3, top=grid8.get_bottom()[1] - 0.2)
        read128.move_to(read16, aligned_edge=RIGHT)
        tick = tick_mark(0.34)
        place(tick, left=intended.get_right()[0] + 0.2, cy=intended.get_center()[1])
        readout_g = VGroup(read16)          # the parent of the swap
        slots8 = [grid8.slot(i) for i in range(8)]
        arrows16 = VGroup(Arrow([tray128.frame.get_right()[0] + 0.1, 1.2, 0], [grid8.get_left()[0] - 0.1, 1.2, 0],
                                color=LOOKUP, stroke_width=4, buff=0.05, tip_length=0.2))
        inside(grid8, n_lab, tray16, tray128, dial, readout, read128, tick)
        below_tag(n_lab)
        below_tag(grid8)
        apart(tray128, grid8, 0.3)
        apart(dial, tray128, 0.1)
        apart(readout, rule, 0.1)
        apart(VGroup(readout, tick), grid8, 0.1)
        apart(dial, rule, 0.1)
        apart(grid8, rule, 0.1)
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(tray, ghost, grid, g_lab, r_lab)), run_time=0.6)
            self.play(FadeIn(grid8), FadeIn(n_lab, shift=DOWN * 0.1), run_time=0.8)
            vo.wait_until("say you want 16")
            self.play(FadeIn(intended, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("Batch by 16")
            self.play(FadeIn(tray16, shift=RIGHT * 0.2), FadeIn(dial), run_time=0.6)
            self.play(GrowArrow(arrows16[0]), run_time=0.5)
            self.play(*tray16.split_to(slots8, 8, run_time=1.0), FadeOut(arrows16), run_time=1.0)
            tray16.remove(tray16.frame)
            vo.wait_until("gets only 2")
            self.play(Write(read16), intended.box.animate.set_stroke(ERR), intended.text.animate.set_color(ERR),
                      run_time=0.8)
            vo.wait_until("Batch by 128")
            old = VGroup(*tray16.squares)
            self.play(*dial.turn_to(128), FadeOut(old), FadeIn(tray128, shift=RIGHT * 0.2), run_time=1.0)
            vo.wait_until("Each GPU gets 16")
            self.play(*tray128.split_to(slots8, 8, run_time=1.2), run_time=1.2)
            tray128.remove(tray128.frame)
            self.play(*swap_text(readout_g, read16, read128), intended.box.animate.set_stroke(OWN),
                      intended.text.animate.set_color(OWN), FadeIn(tick, scale=1.3), run_time=0.8)
        self.wait(0.6)

        # ========================================================== 3 · the repo does the same multiplication
        panel = src_panel(MGPU, 291, 301)
        place(panel, left=-6.4, top=3.0)
        chip_ = excerpt_chip("train_data = train_data.batch(batch_size)", "task_multi_gpu.py · line 198 (excerpt)",
                             line=source_line(MGPU, 198))
        place(chip_, left=-6.4, bottom=-3.45)
        call = label("slide 29 · “Adjust dataset batch size”", 22, S.GREY)
        note64 = label("repo: 32 × 2 replicas = 64", 22, S.GREY)
        notes = VGroup(call, note64).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        place(notes, right=6.4, cy=chip_.get_center()[1])
        b292, b293, b300 = panel.bar(292, TURN), panel.bar(293, OWN, 0.25), panel.bar(300, LOOKUP, 0.25)
        land = rule_mul.copy()
        place(land, right=panel.get_right()[0] - 0.35, cy=b293.get_center()[1])
        land.set_opacity(0)
        inside(panel, chip_, notes)
        below_tag(panel)
        apart(panel, chip_, 0.15)
        apart(panel, notes, 0.15)
        apart(chip_, notes, 0.2)
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(grid8, n_lab, dial, tray128, readout_g, intended, tick)), run_time=0.6)
            self.play(FadeIn(panel, shift=UP * 0.2), run_time=0.8)
            vo.wait_until("multiplies it by")
            self.play(FadeIn(b293), run_time=0.4)
            self.play(rule_mul.animate.move_to(b293.get_center()).set_opacity(0), run_time=1.0)
            self.remove(rule_mul)
            self.play(flash(panel.span(293, "args.batch_size * num_workers"), OWN, 1.08, 0.7))
            vo.wait_until("hands the product")
            self.play(FadeIn(b300), run_time=0.4)
            self.play(FadeIn(chip_, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("Its own comment")
            self.play(FadeIn(b292), run_time=0.4)
            self.play(Write(call), run_time=0.8)
            vo.wait_until("the global batch size")
            self.play(FadeIn(note64, shift=UP * 0.1), run_time=0.6)
        self.wait(1.0)

        # ========================================================== 4 · PONDER 2
        card = mcq_card(PONDER_Q, PONDER_OPTS)
        inside(card)
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(panel, b292, b293, b300, chip_, notes)), FadeOut(lr), run_time=0.6)
            lr = None
            self.play(FadeIn(card, scale=0.95), run_time=0.6)
            vo.wait_until("The repo's multi GPU")
            self.play(flash(card.question[0], INK, 1.03, 0.7))
            vo.wait_until("What is the global batch")
            self.play(flash(card.question[1], TURN, 1.04, 0.7))
            vo.wait_until("Pause here")
            self.play(LaggedStart(*[flash(o.text, INK, 1.04, 0.5) for o in card.options], lag_ratio=0.3),
                      run_time=1.2)
        bar = card[3]
        self.play(bar.animate(rate_func=linear).become(bar.copy().scale(0.001, about_point=bar.get_start())),
                  run_time=10.0)
        self.play(FadeOut(card), run_time=0.6)

        # ========================================================== 5 · the answer
        ans = mcq_card(PONDER_Q, PONDER_OPTS, answer=True)
        inside(ans)
        calc = mono("32 × 4 = 128", 28, INK)
        place(calc, cx=0, top=2.95)
        t128 = BatchTray(128, cols=16, cell=0.16, caption=None)
        place(t128, cx=0, top=calc.get_bottom()[1] - 0.3)
        g4 = gpu_grid(4)
        place(g4, cx=0, bottom=-3.1)
        each = label("32 each", 24, OWN)
        place(each, left=g4.get_right()[0] + 0.25, cy=g4.chips.get_center()[1] + 0.35)
        inside(calc, t128, g4, each)
        apart(calc, t128, 0.15)
        apart(t128, g4, 0.15)
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeIn(ans, scale=0.97), run_time=0.6)
            vo.wait_until("The answer is B")
            self.play(*ans.mark_right(RIGHT_I), run_time=0.6)
            self.play(flash(ans.options[RIGHT_I].text, TURN, 1.04, 0.7))
            vo.wait_until("The trainer multiplies first")
            self.play(FadeOut(ans), run_time=0.5)
            self.play(Write(calc), FadeIn(g4), run_time=0.8)
            vo.wait_until("32 times 4")
            self.play(flash(calc, TURN, 1.06, 0.6), FadeIn(t128, shift=DOWN * 0.2), run_time=0.8)
            vo.wait_until("splits 128 four ways")
            self.play(*t128.split_to([g4.slot(i) for i in range(4)], 4, run_time=1.2), run_time=1.2)
            t128.remove(t128.frame)
            vo.wait_until("each GPU sees 32")
            self.play(FadeIn(each, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("A: that is")
            self.play(FadeOut(VGroup(calc, t128.squares, g4, each)), run_time=0.4)
            self.remove(t128)
            self.play(FadeIn(ans), run_time=0.5)
            self.play(*ans.reason(0, REASONS[0]), run_time=0.8)
            for i, word in ((2, "C: the flag"), (3, "D: the global")):
                vo.wait_until(word)
                self.play(*ans.reason(i, REASONS[i]), run_time=0.8)
        self.wait(0.5)

        # ========================================================== 6 · takeaway
        tk = takeaway("If the question says per replica, multiply before you batch: "
                      "global = per-replica × replicas.", width=10.4)
        inside(tk)
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(ans), run_time=0.5)
            self.play(Write(tk), run_time=1.6)
            vo.wait_until("the global batch is")
            self.play(flash(tk, TURN, 1.04, 0.8))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
        self.wait(0.3)
