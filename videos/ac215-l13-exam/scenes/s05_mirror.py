"""S05 · One machine or many (V3 "mirrors vs islands": MirroredStrategy inside one machine, two
independent MirroredStrategy islands that drift apart, MultiWorkerMirroredStrategy with TF_CONFIG).
Lecture: 26–27, 29–30.

Beats (script.md "## S05", one voiceover block each):
 0  LECTURE 27. Slide 27 redrawn as a three-row ladder: the three row outlines draw, then each
    row's text fades in as it is named: One Device
    (GREY dashed, concept · lecture only), Mirrored (PURPLE), Multi Worker (GREY dashed, concept).
    The YELLOW pin "the repo is here" lands on row 2.
 1  LECTURE 30. Rows 1 and 3 leave; row 2 with its pin rises to the top. CODE(cli-multi-gpu.sh:
    6–12, folded to 6–7, 11–12) left; the BLUE machine "n1-standard-32" with two T4 chips right.
    Line 6 lights with the machine title, lines 11–12 with the GPUs, line 7 with a GREY caption
    "1 = one machine".
 2  LECTURE 29. CODE(task_multi_gpu.py: 286–289) replaces it. Line 287 lights PURPLE and the PURPLE
    MirroredStrategy frame wraps the machine; line 289 lights and the mono counter
    `num_replicas_in_sync = 2` fills in under the machine as the GPUs flash. The panel transforms
    into CODE(task_multi_gpu.py: 303–321 folded to 303–306, 315, 320–321); line 304 lights PURPLE and
    a GREEN replica (one shade) appears on each GPU; lines 306 and 315 light; the replicas flash.
 3  One step, slowly. Code and counter leave, the machine moves to the centre, its PINK all-reduce
    ring appears. A GREEN batch tray splits into two slices that land under the GPUs (PINK arrows
    up into them); a gradient arrow grows on each replica; the arrows rise into the ring and merge
    into one YELLOW averaged arrow; it splits back down; both replicas turn the same new shade.
 4  Islands. Everything leaves. Two BLUE machines "machine 0" / "machine 1", each with its own
    PURPLE MirroredStrategy frame and replicas in the same shade (GREY "same start"); shard chips
    "shard 1" / "shard 2". Each ring works (one step each, different shades); a GREY dashed wire
    with a RED ✗ between them; a second round of steps drifts them further apart; RED Δ "different
    weights".
 5  Multi Worker. The PURPLE frames and per-machine rings fade; a GREY dashed frame round both
    machines, headed `MultiWorkerMirroredStrategy` + concept · lecture only. A schematic TF_CONFIG
    card under each machine (index 0 / 1; illustration · plain TF example); the worker list, then
    the index rows flash. The shard chips flash (same shards); the ✗ wire becomes a PINK cable,
    one PINK ring spans all four replicas; two joint steps: gradients from all four
    replicas merge in the one ring and every replica takes the same shade. (The Δ leaves with the
    PURPLE frames, before the cards take its place.)
 6  The cards leave; a GREY note under the machines: "on Vertex AI: machine 0 is the chief pool,
    extra machines a second worker pool · Vertex writes TF_CONFIG". Then the naming card: row 2
    first ("worker" in `MultiWorkerMirroredStrategy` → "a machine", GREY dashed arrow), then row 1
    (excerpt chip `num_workers`, task_multi_gpu.py · line 289 (excerpt) → "GPUs on one machine",
    PINK arrow).
 7  Takeaway (YELLOW, centred), then an empty frame.

Deviations from SHOW: cli-multi-gpu.sh 6–12 is folded to 6–7, 11–12 (header "lines 6–12
(folded)"): lines 8–9 are 89 and 67 characters and the full panel is 12.5 wide, which leaves no room
for the machine the lines are matched to (the four lit lines are all kept). The 303–321 panel drops
the comment line 314 ("# Optimizer") and wraps lines 303, 315 and 321 by hand at 20 pt, so the
panel fits beside the machine in 12 rows; its header reads "lines 303–321 (folded)" (the ↪ marks
show the wraps; "line N wrapped" ×3 made the header 15 wide). The code panel leaves at the start
of beat 3, not 4: the step needs the machine in the centre with the tray under it. The single
machine's step is played stage by stage (same drawing as Machine.step) so each stage meets its
clause. The islands are titled "machine 0" / "machine 1" to match the TF_CONFIG indices and the
note's "machine 0 is the chief pool"; their shard chips are drawn a little lower than Machine's own
"shard" part so the Multi Worker frame passes between box and chip. In beat 5 the per-machine
PURPLE MirroredStrategy frames fade (a MirroredStrategy label inside a Multi Worker picture would
contradict it), and the re-convergence is drawn as joint all-reduce steps over the spanning ring.
The naming card's two rows appear in the order the SAY needs them (worker first, as the context).
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
    ReplacementTransform,
    RoundedRectangle,
    Transform,
    VGroup,
    Write,
)

from common import *  # noqa: F401,F403
from common import _with_header, guard
from explainer import style as S
from explainer.scene import VoiceScene

SAY = NARRATION["S05"]

# ------------------------------------------------------------------ the real sources
CLI = "cli-multi-gpu.sh"
MG = "package/trainer/task_multi_gpu.py"
assert source_line(CLI, 6).strip() == 'export MACHINE_TYPE="n1-standard-32"', source_line(CLI, 6)
assert source_line(CLI, 7).strip() == "export REPLICA_COUNT=1", source_line(CLI, 7)
assert source_line(CLI, 11).strip() == 'export ACCELERATOR_TYPE="NVIDIA_TESLA_T4"', source_line(CLI, 11)
assert source_line(CLI, 12).strip() == "export ACCELERATOR_COUNT=2", source_line(CLI, 12)
assert source_line(MG, 287).strip() == "strategy = tf.distribute.MirroredStrategy()", source_line(MG, 287)
assert source_line(MG, 289).strip() == "num_workers = strategy.num_replicas_in_sync", source_line(MG, 289)
assert source_line(MG, 304).strip() == "with strategy.scope():", source_line(MG, 304)
assert source_line(MG, 306).strip() == "model = build_mobilenet_model(", source_line(MG, 306)
assert source_line(MG, 315).strip().startswith("optimizer = keras.optimizers.SGD("), source_line(MG, 315)
assert source_line(MG, 321).strip().startswith("model.compile("), source_line(MG, 321)
assert "MultiWorkerMirroredStrategy" not in source_text(MG)       # the repo does not use it
assert "TF_CONFIG" not in source_text(MG) + source_text(CLI)

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


def inside(m, t: float = 3.6):
    guard(m.get_left()[0] >= -SAFE and m.get_right()[0] <= SAFE and m.get_bottom()[1] >= -3.6
          and m.get_top()[1] <= t, f"outside the frame: {m.get_left()} {m.get_right()} {m.get_bottom()} {m.get_top()}")


def apart(a, b, msg, buff: float = 0.08):
    """Guard: the bounding boxes of a and b do not overlap."""
    sep = (a.get_right()[0] + buff <= b.get_left()[0] or b.get_right()[0] + buff <= a.get_left()[0]
           or a.get_top()[1] + buff <= b.get_bottom()[1] or b.get_top()[1] + buff <= a.get_bottom()[1])
    guard(sep, msg)


def flash(mob, color=TURN, k: float = 1.12, run_time: float = 0.6):
    return Indicate(mob, color=color, scale_factor=k, run_time=run_time)


def arrow(a, b, color=S.GREY, stroke: float = 3, buff: float = 0.08) -> Arrow:
    return Arrow(a, b, buff=buff, color=color, stroke_width=stroke, max_tip_length_to_length_ratio=0.25,
                 tip_length=0.16)


def dashed_arrow(a, b, color=S.GREY) -> VGroup:
    """A GREY dashed arrow (a dashed shaft and a solid tip)."""
    full = arrow(a, b, color)
    shaft = DashedLine(full.get_start(), full.get_end() - (full.get_end() - full.get_start()) * 0.12,
                       color=color, stroke_width=3, dash_length=0.1)
    tip = full.get_tip().copy() if hasattr(full, "get_tip") else full.tip.copy()
    return VGroup(shaft, tip)


def step_arrows(replicas, center):
    """The drawing of Machine.step for any set of replicas meeting in one ring centre: a gradient
    arrow on each replica, the merged (averaged) arrow at the centre, the update arrows back down."""
    grads = [Arrow(r.get_top(), r.get_top() + UP * 0.45, buff=0, color=INK, stroke_width=4,
                   max_tip_length_to_length_ratio=0.35) for r in replicas]
    merged = Arrow(center + DOWN * 0.18, center + UP * 0.18, buff=0, color=TURN, stroke_width=5,
                   max_tip_length_to_length_ratio=0.4)
    back = [Arrow(center, r.get_top() + UP * 0.05, buff=0.05, color=TURN, stroke_width=4,
                  max_tip_length_to_length_ratio=0.25) for r in replicas]
    return grads, merged, back


def play_step(scene, replicas, center, shade, run_time: float = 2.4):
    """A joint all-reduce step over `replicas` (Multi Worker: the ring spans the machines)."""
    grads, merged, back = step_arrows(replicas, center)
    q = run_time / 4
    scene.play(*[GrowArrow(a) for a in grads], run_time=q)
    scene.play(*[Transform(a, merged.copy()) for a in grads], run_time=q)
    scene.play(*[FadeOut(a) for a in grads], *[GrowArrow(b) for b in back], run_time=q)
    scene.play(*[FadeOut(b) for b in back], *[r.set_shade(shade) for r in replicas], run_time=q)


class MirrorsAndIslands(VoiceScene):
    def construct(self):
        assert len(SAY) == 8, len(SAY)

        # ========================================================== 0 · slide 27: the ladder
        lad = StrategyLadder()
        place(lad, cx=0, cy=0.3)
        inside(lad)
        rows = lad.rows
        c0, c2, pin = lad.parts["concept0"], lad.parts["concept2"], lad.parts["pin"]
        lr = None
        with self.voiceover(SAY[0]) as vo:
            lr = lref_swap(self, lr, "27")
            self.play(LaggedStart(*[Create(r.frame) for r in rows], lag_ratio=0.25), run_time=1.4)
            vo.wait_until("One machine with one GPU")
            self.play(FadeIn(rows[0][1], shift=RIGHT * 0.2), FadeIn(c0), run_time=0.7)
            vo.wait_until("One machine with several GPUs")
            self.play(FadeIn(rows[1][1], shift=RIGHT * 0.2), run_time=0.7)
            self.play(flash(rows[1].right, TOOL, 1.06), run_time=0.6)
            vo.wait_until("Several machines use")
            self.play(FadeIn(rows[2][1], shift=RIGHT * 0.2), FadeIn(c2), run_time=0.7)
            self.play(*lad.parts_in("pin"), run_time=0.6)

        # ========================================================== 1 · the repo's machine: cli-multi-gpu.sh
        top_row = VGroup(rows[1], pin)
        top_target = top_row.copy()
        place(top_target, cx=0, top=3.02)
        inside(top_target)
        guard(top_target.get_top()[1] < LREF_BOTTOM - 0.05, "ladder row runs into the lecture tag")
        cli = src_panel(CLI, [(6, 7), (11, 12)])
        place(cli, left=-6.5, top=2.15)
        inside(cli)
        mach = Machine(2, MACHINE_MULTI, width=4.0)
        place(mach, right=6.45, top=2.05)
        inside(mach)
        apart(cli, mach, "cli panel runs into the machine")
        apart(top_target, mach, "ladder row runs into the machine")
        apart(top_target, cli, "ladder row runs into the cli panel")
        cap7 = note("1 = one machine", S.GREY)
        place(cap7, left=cli.span(7, "1").get_right()[0] + 0.5, cy=cli.span(7, "1").get_center()[1])
        guard(cap7.get_right()[0] < cli.get_right()[0], "line 7 caption leaves the panel")
        with self.voiceover(SAY[1]) as vo:
            lr = lref_swap(self, lr, "30")
            self.play(FadeOut(VGroup(rows[0], rows[2], c0, c2)), flash(pin.text, INK, 1.15), run_time=0.7)
            self.play(Transform(top_row, top_target), run_time=0.8)
            vo.wait_until("Its multi GPU script")
            self.play(FadeIn(cli, shift=RIGHT * 0.3), run_time=0.7)
            vo.wait_until("for one machine")
            self.play(FadeIn(mach, shift=LEFT * 0.3), run_time=0.7)
            vo.wait_until("type n1")
            b6 = cli.bar(6, CLOUD)
            self.play(FadeIn(b6), flash(mach.box.title, CLOUD, 1.1), run_time=0.7)
            vo.wait_until("with two T4")
            b1112 = VGroup(cli.bar(11, CLOUD), cli.bar(12, CLOUD))
            self.play(FadeIn(b1112), *[flash(g, CLOUD, 1.15) for g in mach.gpus], run_time=0.8)
            vo.wait_until("A replica count")
            b7 = cli.bar(7, TURN)
            self.play(FadeIn(b7), run_time=0.5)
            vo.wait_until("means one machine")
            self.play(FadeIn(cap7, shift=LEFT * 0.15), flash(mach.box.frame, CLOUD, 1.03), run_time=0.7)

        # ========================================================== 2 · MirroredStrategy and strategy.scope()
        p286 = src_panel(MG, 286, 289)
        place(p286, left=-6.5, top=2.15)
        inside(p286)
        apart(p286, mach, "286 panel runs into the machine")
        p303 = src_panel(MG, [(303, 306), 315, (320, 321)], size=20,
                         wrap={303: ["within"], 315: ["learning_rate="], 321: ["metrics"]})
        _with_header(p303, f"{shown_path(MG)} · lines 303–321 (folded)")
        place(p303, left=-6.55, top=2.15)
        inside(p303)
        guard(p303.header.get_right()[0] <= p303.code.get_right()[0] + 0.05, "303 header wider than its panel")
        apart(p303, mach, "303 panel runs into the machine", buff=0.05)
        cnt_l = mono("num_replicas_in_sync =", CAPTION, INK)
        cnt_v = mono("2", 26, TURN)
        cnt = VGroup(cnt_l, cnt_v).arrange(RIGHT, buff=0.18)
        cnt_v.align_to(cnt_l, DOWN)
        place(cnt, cx=mach.get_center()[0], top=mach.get_bottom()[1] - 0.35)
        inside(cnt)
        apart(cnt, p303, "counter runs into the 303 panel", buff=0.05)
        with self.voiceover(SAY[2]) as vo:
            lr = lref_swap(self, lr, "29")
            self.play(FadeOut(VGroup(cli, b6, b1112, b7, cap7)), run_time=0.5)
            self.play(FadeIn(p286, shift=RIGHT * 0.3), run_time=0.6)
            vo.wait_until("creates the Mirrored Strategy")
            b287 = p286.bar(287, TOOL)
            self.play(FadeIn(b287), *mach.parts_in("strategy"), run_time=0.8)
            vo.wait_until("asks how many replicas")
            b289 = p286.bar(289, TURN)
            self.play(FadeIn(b289), FadeIn(cnt_l, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("one per GPU")
            self.play(*[flash(g, CLOUD, 1.18) for g in mach.gpus], run_time=0.7)
            vo.wait_until("so two")
            self.play(FadeIn(cnt_v, scale=1.4), run_time=0.5)
            vo.wait_until("Then it builds")
            self.play(FadeOut(VGroup(b287, b289)), run_time=0.3)
            self.play(ReplacementTransform(p286, p303), run_time=1.0)
            vo.wait_until("inside strategy dot scope")
            b304 = p303.bar(304, TOOL)
            self.play(FadeIn(b304), *mach.parts_in("replicas"), run_time=0.8)
            vo.wait_until("so every weight")
            b306 = VGroup(p303.bar(306, OWN), p303.bar(315, OWN))
            self.play(FadeIn(b306), run_time=0.6)
            vo.wait_until("one copy per GPU")
            self.play(*[flash(r, OWN, 1.15) for r in mach.replicas], run_time=0.8)

        # ========================================================== 3 · one training step, slowly
        mach_c = [0.0, 0.45, 0]
        center_shift = np.array(mach_c) - mach.get_center()
        tray = BatchTray(8, cols=8, cell=0.3, caption=None)
        tray_l = label("one batch", CAPTION, INK)
        trayg = VGroup(tray_l, tray).arrange(RIGHT, buff=0.3)
        place(trayg, cx=0, cy=-3.0)
        inside(trayg)
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(p303, b304, b306, cnt)), run_time=0.5)
            self.play(mach.animate.shift(center_shift), run_time=0.8)
            gpu_x = [g.get_center()[0] for g in mach.gpus]
            land = [np.array([x, mach.get_bottom()[1] - 0.95, 0]) for x in gpu_x]
            apart(top_row, mach, "ladder row runs into the centred machine")
            self.play(*mach.parts_in("ring"), FadeIn(trayg, shift=UP * 0.2), run_time=0.7)
            vo.wait_until("Each GPU takes")
            self.play(*tray.split_to(land, 2, cols=2, max_h=0.55), FadeOut(tray_l), run_time=1.0)
            slices = tray.slices(2)
            ups = [arrow(s.get_top(), g.get_bottom() + DOWN * 0.08, LOOKUP, stroke=4)
                   for s, g in zip(slices, mach.gpus)]
            self.play(*[GrowArrow(a) for a in ups], run_time=0.6)
            grads, merged, back = step_arrows(mach.replicas, mach.ring_center())
            vo.wait_until("and computes a gradient")
            self.play(*[GrowArrow(a) for a in grads], run_time=0.8)
            vo.wait_until("The gradients meet")
            self.play(*[Transform(a, merged.copy()) for a in grads], run_time=1.2)
            vo.wait_until("and are averaged")
            self.play(flash(mach.ring, LOOKUP, 1.08), run_time=0.6)
            vo.wait_until("and the same update")
            self.play(*[FadeOut(a) for a in grads], *[GrowArrow(b) for b in back], run_time=0.8)
            vo.wait_until("to both copies")
            self.play(*[FadeOut(b) for b in back], *[r.set_shade(SHADES[1]) for r in mach.replicas], run_time=0.8)

        # ========================================================== 4 · islands: two machines, no wire
        ma = Machine(2, "machine 0", width=5.0)
        mb = Machine(2, "machine 1", width=5.0)
        ma.move_to([-3.25, 1.1, 0])
        mb.move_to([3.25, 1.1, 0])
        for m in (ma, mb):
            inside(m)
        sh = [chip(f"shard {i}", S.GREY, size=CAPTION).move_to([m.get_center()[0], -1.1, 0])
              for i, m in zip((1, 2), (ma, mb))]
        for c in sh:
            inside(c)
            guard(c.get_top()[1] < ma.get_bottom()[1] - 0.2, "shard chip too close to its machine")
        same = note("same start", S.GREY)
        place(same, cx=0, cy=-1.1)
        apart(same, sh[0], "same-start caption runs into shard 1")
        apart(same, sh[1], "same-start caption runs into shard 2")
        nw = no_wire(ma, mb)
        dm = delta_mark()
        place(dm, cx=0, cy=-2.4)
        inside(dm)
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(top_row, mach, *slices, *ups, lr)), run_time=0.6)
            lr = None
            self.play(FadeIn(ma, shift=RIGHT * 0.3), FadeIn(mb, shift=LEFT * 0.3), run_time=0.8)
            self.play(*ma.parts_in("replicas"), *mb.parts_in("replicas"), FadeIn(same), run_time=0.6)
            vo.wait_until("its own Mirrored Strategy")
            self.play(*ma.parts_in("strategy"), *mb.parts_in("strategy"), run_time=0.7)
            vo.wait_until("on its own shard")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in sh], lag_ratio=0.3), run_time=0.8)
            vo.wait_until("Inside each machine")
            self.play(*ma.parts_in("ring"), *mb.parts_in("ring"), run_time=0.5)
            self.play(ma.step(SHADES[2]), mb.step(SHADES[5]))
            vo.wait_until("but between the machines")
            self.play(Create(nw[0]), run_time=0.6)
            self.play(FadeIn(nw[1], scale=1.4), run_time=0.4)
            vo.wait_until("After a few steps")
            self.play(ma.step(SHADES[2]), mb.step(SHADES[3]), FadeOut(same))
            vo.wait_until("they hold different weights")
            self.play(FadeIn(dm, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("two separate models")
            self.play(flash(ma.box.frame, ERR, 1.03), flash(mb.box.frame, ERR, 1.03), flash(dm, ERR, 1.1),
                      run_time=0.9)

        # ========================================================== 5 · Multi Worker: TF_CONFIG and the wire
        pair = VGroup(ma, mb)
        fw = pair.width + 0.3
        fh = ma.box.frame.height + 0.24
        mf = DashedVMobject(RoundedRectangle(width=fw, height=fh, corner_radius=0.16), num_dashes=110,
                            dashed_ratio=0.55).set_stroke(CONCEPT, 2.5)
        mf.move_to([0, ma.box.frame.get_center()[1], 0])
        mw_l = mono("MultiWorkerMirroredStrategy", CAPTION, INK)
        mw_t = concept_tag()
        mw = VGroup(mw_l, mw_t).arrange(RIGHT, buff=0.3)
        place(mw, left=mf.get_left()[0] + 0.1, bottom=mf.get_top()[1] + 0.08)
        inside(mw)
        for c in sh:
            guard(c.get_top()[1] < mf.get_bottom()[1] - 0.05, "the Multi Worker frame cuts a shard chip")
        cards = [tf_config_card(0), tf_config_card(1)]
        for card, m in zip(cards, (ma, mb)):
            place(card, cx=m.get_center()[0], top=-1.45)
            inside(card)
        apart(cards[0], cards[1], "the TF_CONFIG cards overlap")
        for card, c in zip(cards, sh):
            apart(card, c, "a TF_CONFIG card runs into a shard chip", buff=0.04)
        it = illustration_tag("plain TF example")
        place(it, cx=0, cy=-1.1)
        apart(it, sh[0], "tag runs into shard 1")
        apart(it, sh[1], "tag runs into shard 2")
        cb = cable(ma, mb)
        sr = span_ring(ma, mb)
        reps = [*ma.replicas, *mb.replicas]
        with self.voiceover(SAY[5]) as vo:
            vo.wait_until("use Multi Worker")
            self.play(*ma.parts_out("strategy"), *mb.parts_out("strategy"), Create(mf),
                      FadeIn(mw, shift=DOWN * 0.15), FadeOut(dm), run_time=0.9)
            vo.wait_until("Each machine reads")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cards], lag_ratio=0.3),
                      FadeIn(it), run_time=0.9)
            vo.wait_until("the list of all the workers")
            self.play(*[flash(VGroup(c.rows[0], c.rows[1]), TURN, 1.05) for c in cards], run_time=0.8)
            vo.wait_until("and its own index")
            self.play(*[flash(c.rows[3], TURN, 1.1) for c in cards], run_time=0.8)
            vo.wait_until("Same shards as before")
            self.play(*[flash(c, S.GREY, 1.12) for c in sh], run_time=0.7)
            vo.wait_until("the only change is the wire")
            self.play(FadeOut(nw), *ma.parts_out("ring"), *mb.parts_out("ring"), run_time=0.4)
            self.play(Create(cb), Create(sr), run_time=0.8)
            vo.wait_until("and now every copy")
            play_step(self, reps, sr.get_center(), SHADES[1], run_time=2.0)
            play_step(self, reps, sr.get_center(), SHADES[4], run_time=2.0)

        # ========================================================== 6 · Vertex worker pools + the naming trap
        vx = fit_rows("on Vertex AI: machine 0 is the chief pool, extra machines a second worker pool · "
                      "Vertex writes `TF_CONFIG`", 11.0, color=S.GREY, align=LEFT)
        place(vx, cx=0, top=-1.65)
        inside(vx)
        apart(vx, sh[0], "note runs into shard 1", buff=0.05)
        # the naming card
        r1l = excerpt_chip("num_workers", "task_multi_gpu.py · line 289 (excerpt)", line=source_line(MG, 289))
        r1r = label("GPUs on one machine", 24, INK)
        r2l = fit_rows('"worker" in `MultiWorkerMirroredStrategy`', 7.0)
        r2r = label("a machine", 24, INK)
        left_x = -6.0
        place(r1l, left=left_x, cy=0.55)
        place(r2l, left=left_x, cy=-1.15)
        col_x = max(r1l.get_right()[0], r2l.get_right()[0]) + 1.6
        place(r1r, left=col_x, cy=r1l.chip.get_center()[1])
        place(r2r, left=col_x, cy=r2l.get_center()[1])
        a1 = arrow(np.array([r1l.chip.get_right()[0] + 0.15, r1r.get_center()[1], 0]),
                   np.array([col_x - 0.15, r1r.get_center()[1], 0]), LOOKUP, stroke=4)
        a2 = dashed_arrow(np.array([r2l.get_right()[0] + 0.15, r2r.get_center()[1], 0]),
                          np.array([col_x - 0.15, r2r.get_center()[1], 0]))
        trap = label("one naming trap", 26, TURN)
        place(trap, left=left_x, cy=2.1)
        naming = VGroup(trap, r1l, r1r, r2l, r2r, a1, a2)
        naming.shift(RIGHT * -naming.get_center()[0])
        inside(naming)
        apart(r1l, r2l, "naming rows overlap")
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(*cards, it)), run_time=0.5)
            vo.wait_until("on Vertex AI")
            self.play(FadeIn(vx, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("second worker pool")
            self.play(flash(mb.box.frame, CLOUD, 1.03), run_time=0.7)
            vo.wait_until("and Vertex sets")
            self.play(flash(vx[-1], TURN, 1.05), run_time=0.7)
            vo.wait_until("One naming trap")
            self.play(FadeOut(VGroup(ma, mb, *sh, mf, mw, cb, sr, vx)), run_time=0.6)
            self.play(FadeIn(trap), FadeIn(r2l, shift=RIGHT * 0.2), run_time=0.5)
            self.play(Create(a2[0]), FadeIn(a2[1]), FadeIn(r2r, shift=LEFT * 0.2), run_time=0.6)
            vo.wait_until("calls its replica count")
            self.play(FadeIn(r1l, shift=RIGHT * 0.2), run_time=0.6)
            vo.wait_until("but it counts GPUs")
            self.play(GrowArrow(a1), FadeIn(r1r, shift=LEFT * 0.2), run_time=0.7)
            self.play(flash(r1r, LOOKUP, 1.08), run_time=0.6)

        # ========================================================== 7 · takeaway
        tk = takeaway("If the question says several machines must train one model, think "
                      "`MultiWorkerMirroredStrategy` with `TF_CONFIG`; a `MirroredStrategy` never looks past its "
                      "own machine.")
        inside(tk)
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(naming), run_time=0.5)
            self.play(Write(tk), run_time=1.6)
            vo.wait_until("A Mirrored Strategy never")
            self.play(flash(tk, TURN, 1.04, 0.8))
        self.play(FadeOut(tk), run_time=0.6)
        self.wait(0.4)
