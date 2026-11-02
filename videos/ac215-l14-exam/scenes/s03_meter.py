"""S03 · Who pays for the idle hours? (AC215 L14 exam edition). Lecture: 14 · 8, 11, 14, 16; then 15 · 11.

Beats (script.md "## S03", one voiceover block each):
0. The exam map (slot 1 filled) fades in, slot 2 activates ("2 · who pays for idle") and pulses;
   lref(14, "8, 11, 14") top right. Three GREY lecture chips write in and stack top left (slide 8
   "Brings down code execution cost", 11 "Pay only for the time your code runs", 14 "Only pay
   when your code is running"). At "two meters, one day" V2's 24-hour axis draws; at "The yellow
   ticks" the nine YELLOW request ticks (two clusters) grow and pulse.
1. The chips go; the solid BLUE VM rack ("VM") and its GOLD meter come in. At "Its meter runs" the
   cursor sweeps the day: the VM meter fills at a constant rate and the row shades GOLD ("idle ·
   billed"); at "The gold shading" the shading pulses.
2. The dashed BLUE function instance ("function") and its meter come in. At "request-based
   billing" two GOLD excerpt chips of README.md lines 281 and 282 ("Request-based billing",
   "Minimum number of instances `0`") write in under the axis. At "Its meter moves only" an
   instance blinks at each tick and the function meter steps up one block per tick.
3. Transform 1: the chips go; at "Now stretch" the quiet gap widens (the day reads 36 h, the ticks
   keep count and width), a YELLOW "more idle time" span marks the gap; the VM meter grows, the
   function meter gets the GREY "+0" chip. "The VM meter grows" / "does not move" pulse each meter.
4. lref(14, "16") at "slide 16". At "After a quiet stretch" the GREY puff and the delayed first
   tick of cluster 2 (RED "cold start"). At "The README's remedy" the excerpt chip README.md line
   223 "Minimum-instance settings can keep capacity". At "Set it to 1" the GOLD slider 0 -> 1: an
   always-on dashed instance with its GOLD drip runs along the function row, the puff goes; at
   "with its own meter running" the drip pulses; a later burst tick still gets a small puff, chip
   "fewer cold starts, not none".
5. The band and its drip lift into the VM row ("always on"); the slider goes. lref(15, "11") at
   "So does next lecture's": a BLUE "Vertex AI endpoint" card slides into the always-on row; at
   "minimum replica count" the GOLD excerpt chip model-deployment/cli.py line 215
   `min_replica_count=1`; at "the part that costs money" the excerpt chip model-deployment/README.md
   line 66 "This is the part that costs money."
6. The chips, the endpoint, the always-on band and the lecture tag go (end of the idea); a GREY "?"
   sits on the meters. After the block: PONDER P2 (10 s), map and meters dimmed to 20 %.
7. Reveal: B fills YELLOW ✓ (GREEN note, the highlight grown to cover it). At "Watch" the card steps aside, the meters come back and
   transform 2 plays: the axis is one day again, every tick splits in two, the function meter climbs
   to 18 blocks, the VM meter stays ("flat", GREY footnote "until it runs out of capacity"). At "A
   is backwards" the card returns: RED reasons for A, then C at "C is wrong", D at "D confuses".
8. The card and meters go. A GREY chip "serverless = cheap" is struck RED at "serverless is cheap";
   at "is anything always on" the GOLD-outlined question card; its two arrows draw at "Idle time
   moves" and "Request count". The GREEN exam-rule card writes in and shrinks into map slot 2.
   Everything fades to an empty frame.
"""

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Create,
    DoubleArrow,
    FadeIn,
    FadeOut,
    GrowArrow,
    GrowFromEdge,
    Indicate,
    LaggedStart,
    RoundedRectangle,
    VGroup,
    Write,
)

from explainer import style as S
from explainer.scene import VoiceScene

from common import (
    CAPTION,
    CLOUD,
    COST,
    ERR,
    INK,
    NARRATION,
    SAFE_X,
    SAFE_Y,
    TURN,
    ExamMap,
    RuleCard,
    TwoMeters,
    _arrow,
    _save_op,
    _set_op,
    chip,
    dim,
    excerpt_chip,
    guard,
    label,
    lref,
    lref_swap,
    MCQCard,
    model_box,
    puff,
    shown_path,
    source_line,
    strike,
    undim,
)

SAY = NARRATION["S03"]

# ------------------------------------------------------------------ the real sources (checked)
README = "README.md"
CLI = "cli.py"
MD_README = "model-deployment/README.md"
REQ_BILLING = "Request-based billing"
assert REQ_BILLING in source_line(README, 281)
MIN_ZERO = "Minimum number of instances `0`"
assert MIN_ZERO in source_line(README, 282)
WARM = "Minimum-instance settings can keep capacity"
assert WARM in source_line(README, 223) and "warm when that matters" in source_line(README, 224)
MIN_REPLICA = "min_replica_count=1"
assert source_line(CLI, 215).strip() == MIN_REPLICA + ","
COSTS = "This is the part that costs money."
assert COSTS in source_line(MD_README, 66)

# the lecture's own words (deck text: slides 8, 11, 14)
SLIDE_CHIPS = [("Brings down code execution cost", "8"),
               ("Pay only for the time your code runs", "11"),
               ("Only pay when your code is running", "14")]

# ------------------------------------------------------------------ P2 (script.md S03, BRIEF "Ponder questions")
P2_Q = ("Ignore free tiers. Same work on a Cloud Run function (min instances 0) and on an always-on VM. "
        "Next month: twice the requests, same length, same days. Which bill changes?")
P2_OPTS = ["Only the VM's",
           "Only the function's",
           "Both double",
           "Neither: serverless has no minimum charge"]
P2_RIGHT = (1, "more invocations · more execution time")
P2_WRONG = {0: "the VM bills provisioned hours: unchanged",
            2: "the VM is flat with traffic",
            3: "no minimum ≠ free work: idle is free, requests are not"}
# re-derived: the function bills invocations × execution time (both doubled per day); the VM bills
# its provisioned hours (same days, same hours) -> only the function's bill changes: B.
assert P2_RIGHT[0] == 1 and P2_OPTS[1] == "Only the function's"

RULE_TOP = "idle time changes → only always-on bills move (VM · min instances ≥ 1 · endpoint replica)"
RULE_BOTTOM = "request count or duration changes → only the pay-per-use bill moves"

BOTTOM_ZONE = -1.9        # below the axis labels ("0 h", "24 h"): chips live under this line


def inside_frame(*mobs):
    for m in mobs:
        guard(m.get_left()[0] >= -SAFE_X - 1e-6 and m.get_right()[0] <= SAFE_X + 1e-6,
              f"x out of frame: {m.get_left()[0]:.2f}..{m.get_right()[0]:.2f}")
        guard(m.get_bottom()[1] >= -SAFE_Y - 1e-6 and m.get_top()[1] <= SAFE_Y + 1e-6,
              f"y out of frame: {m.get_bottom()[1]:.2f}..{m.get_top()[1]:.2f}")


def apart(a, b, gap: float = 0.05):
    sep = (a.get_right()[0] + gap <= b.get_left()[0] or b.get_right()[0] + gap <= a.get_left()[0]
           or a.get_top()[1] + gap <= b.get_bottom()[1] or b.get_top()[1] + gap <= a.get_bottom()[1])
    guard(sep, f"overlap: {a.get_corner(DOWN + LEFT)} {a.get_corner(UP + RIGHT)} / "
               f"{b.get_corner(DOWN + LEFT)} {b.get_corner(UP + RIGHT)}")


def hide_now(piece, *names):
    """Start these shown-by-default parts of a set piece invisible (revealed later with parts_in)."""
    for n in names:
        m = piece.parts[n]
        _save_op(m)
        _set_op(m, 0)
        piece._flag(m, True)


def slide_chip(text: str, n: str):
    """A GREY lecture chip: the slide's words in quotes, then the slide number."""
    return chip(f"“{text}” · slide {n}", S.GREY, size=CAPTION)


def arrow_row(left: str, right: str, width: float = 2.0):
    """One row of the GOLD question card: `left` → `right` (the arrow draws separately)."""
    a = label(left, 24, INK)
    b = label(right, 24, COST)
    arr = _arrow([0, 0, 0], [width, 0, 0], COST, 4, buff=0)
    g = VGroup(a, arr, b).arrange(RIGHT, buff=0.25)
    g.left_t, g.arrow, g.right_t = a, arr, b
    return g


def ponder(scene, question, options, seconds, dimmed=(), hide=()):
    """common.mcq_ponder, inlined (written while its `dim=` argument still shadowed common.dim()).
    Same card, same place, same guard, same timer."""
    card = MCQCard(question, options)
    card.move_to([0, -3.55 + card.frame.height / 2, 0])
    guard(card.get_top()[1] <= 2.58, f"ponder card top {card.get_top()[1]:.2f} reaches the exam map's label")
    scene.play(FadeIn(card, scale=0.97), *[dim(x) for x in dimmed], *[FadeOut(x) for x in hide], run_time=0.6)
    card.run_timer(scene, seconds)
    return card


def right_covering_note(card, k, note_):
    """card.right(k, note_) with the YELLOW highlight grown to cover the GREEN note too (as built,
    the highlight's lower edge runs through the note's letters; reported)."""
    anims = card.right(k, note_)
    hl, nt = card.marks[-3], card.marks[-1]
    top = card.rows[k].get_top()[1] + 0.07
    bottom = nt.get_bottom()[1] - 0.06
    hl.stretch_to_fit_height(top - bottom).move_to([hl.get_center()[0], (top + bottom) / 2, 0])
    if k + 1 < len(card.rows):
        guard(bottom >= card.rows[k + 1].get_top()[1] + 0.02, "the grown highlight reaches the next option")
    return anims


class IdleMeter(VoiceScene):
    def construct(self):
        assert len(SAY) == 9, len(SAY)

        # ========================================================== 0. the promise, one day
        m = ExamMap(filled=(1,))
        lr = lref(14, "8, 11, 14")
        chips = VGroup(*[slide_chip(t, n) for t, n in SLIDE_CHIPS]).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        chips.move_to([-6.45, 1.55, 0], aligned_edge=LEFT)
        tm = TwoMeters()
        hide_now(tm, "rack", "inst_icon", "axis", "t0", "t_end", "ticks", "vm_meter", "fn_meter")
        tm.parts["slider"].move_to([3.45, -2.25, 0])
        vm_lab = label("VM", CAPTION, CLOUD).next_to(tm.parts["rack"], DOWN, buff=0.12)
        fn_lab = label("function", CAPTION, CLOUD).next_to(tm.parts["inst_icon"], DOWN, buff=0.12)
        inside_frame(chips, tm, vm_lab, fn_lab)
        guard(chips.get_top()[1] <= 2.55, "lecture chips reach the map's label")
        guard(chips.get_bottom()[1] >= tm.parts["ticks"].get_top()[1] + 0.1, "lecture chips touch the ticks")
        apart(fn_lab, tm.parts["axis"])
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(m), FadeIn(lr), run_time=0.6)
            self.play(*m.activate(2), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.15) for c in chips], lag_ratio=0.45),
                      m.pulse(2), run_time=2.0)
            self.add(tm)
            vo.wait_until("two meters, one day")
            self.play(*tm.parts_in("axis", anim=Create), *tm.parts_in("t0", "t_end"), run_time=0.8)
            vo.wait_until("The yellow ticks")
            self.play(*tm.parts_in("ticks", anim=lambda t: LaggedStart(
                *[GrowFromEdge(x, DOWN) for x in t], lag_ratio=0.15)), run_time=1.2)
            self.play(Indicate(tm.parts["ticks"], color=TURN, scale_factor=1.05), run_time=vo.remaining(0.6))

        # ========================================================== 1. the VM row: billed from boot to shutdown
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(chips, shift=LEFT * 0.2), run_time=0.4)
            self.play(*tm.parts_in("rack", "vm_meter"), FadeIn(vm_lab), run_time=0.6)
            vo.wait_until("Its meter runs")
            self.play(*tm.sweep(run_time=4.0))
            vo.wait_until("The gold shading")
            self.play(Indicate(tm.parts["idle"], color=COST, scale_factor=1.03),
                      Indicate(tm.parts["idle_lab"], color=COST), run_time=1.0)
            self.play(Indicate(tm.parts["vm_fill"], color=COST, scale_factor=1.05), run_time=vo.remaining(0.6))

        # ========================================================== 2. the function row: billed per invocation
        c281 = excerpt_chip(REQ_BILLING, f"{README} · line 281 (excerpt)", color=COST, frame=COST,
                            line=source_line(README, 281))
        c282 = excerpt_chip(MIN_ZERO, f"{README} · line 282 (excerpt)", color=COST, frame=COST,
                            line=source_line(README, 282))
        VGroup(c281, c282).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).move_to([-6.45, -3.0, 0], aligned_edge=LEFT)
        inside_frame(c281, c282)
        guard(max(c281.get_top()[1], c282.get_top()[1]) <= BOTTOM_ZONE, "README chips reach the axis labels")
        with self.voiceover(SAY[2]) as vo:
            self.play(*tm.parts_in("inst_icon", "fn_meter"), FadeIn(fn_lab), run_time=0.8)
            vo.wait_until("request-based billing")
            self.play(FadeIn(c281, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("minimum instances 0")
            self.play(FadeIn(c282, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("Its meter moves only")
            self.play(tm.blink_all(run_time=4.0))
            self.play(Indicate(tm.parts["fn_meter"], color=COST, scale_factor=1.05), run_time=vo.remaining(0.6))

        # ========================================================== 3. transform 1: more idle time
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(c281, c282)), run_time=0.5)
            vo.wait_until("Now stretch")
            self.play(*tm.stretch(), run_time=1.6)
            gap = DoubleArrow([tm.hx(11.0) + 0.1, -2.15, 0], [tm.hx(17.0) - 0.1, -2.15, 0], color=TURN,
                              stroke_width=3, buff=0, tip_length=0.16)
            more = label("more idle time", CAPTION, TURN).next_to(gap, DOWN, buff=0.12)
            inside_frame(gap, more)
            guard(gap.get_top()[1] <= BOTTOM_ZONE + 0.05, "the gap arrow reaches the axis labels")
            self.play(GrowArrow(gap), FadeIn(more), run_time=0.6)
            vo.wait_until("The VM meter grows")
            self.play(Indicate(tm.parts["vm_fill"], color=COST, scale_factor=1.06), run_time=1.0)
            vo.wait_until("The function meter does not move")
            self.play(Indicate(tm.parts["fn_meter"], color=COST, scale_factor=1.05),
                      Indicate(tm.parts["plus0"], color=INK), run_time=vo.remaining(1.0))

        # ========================================================== 4. the price: cold starts; minimum instances
        c223 = excerpt_chip(WARM, f"{README} · line 223 (excerpt)", line=source_line(README, 223))
        c223.move_to([-6.5, -3.0, 0], aligned_edge=LEFT)
        inside_frame(c223, tm.parts["slider"])
        apart(c223, tm.parts["slider"])
        guard(c223.get_top()[1] <= BOTTOM_ZONE, "the line-223 chip reaches the axis labels")
        burst_x = tm.hx(19.0)
        puff2 = puff(0.17).move_to([burst_x, 0.0, 0])
        puff2.shift(UP * (tm.parts["ticks"].get_top()[1] + 0.05 - puff2.get_bottom()[1]))
        fewer = chip("fewer cold starts, not none", S.GREY, size=CAPTION).next_to(puff2, UP, buff=0.12)
        guard(fewer.get_top()[1] <= tm.parts["idle"].get_bottom()[1] - 0.05, "the 'fewer' chip reaches the shading")
        inside_frame(fewer)
        apart(fewer, tm.parts["vm_meter"])
        with self.voiceover(SAY[4]) as vo:
            vo.wait_until("slide 16")
            self.play(FadeOut(VGroup(gap, more)), run_time=0.4)
            lr = lref_swap(self, lr, 14, "16")
            vo.wait_until("After a quiet stretch")
            self.play(*tm.cold_start(), run_time=0.9)
            self.play(Indicate(tm.parts["cold"], color=ERR), run_time=0.8)
            vo.wait_until("The README's remedy")
            self.play(FadeIn(c223, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("Set it to 1")
            self.play(*tm.min_instances(1), run_time=1.2)
            vo.wait_until("with its own meter running")
            self.play(Indicate(tm.parts["band"].drip, color=COST, scale_factor=1.3), run_time=0.9)
            self.play(FadeIn(puff2, scale=0.6), FadeIn(fewer, shift=DOWN * 0.1), run_time=0.6)
            self.wait(vo.remaining(0.3))

        # ========================================================== 5. the always-on row: min instances, the endpoint
        ccli = excerpt_chip(MIN_REPLICA, f"{shown_path(CLI)} · line 215 (excerpt)", color=COST, frame=COST,
                            line=source_line(CLI, 215))
        cmd = excerpt_chip(COSTS, f"{shown_path(MD_README)} · line 66 (excerpt)", color=COST, frame=COST,
                           line=source_line(MD_README, 66))
        ccli.move_to([-6.5, -3.0, 0], aligned_edge=LEFT)
        cmd.move_to([6.55, -3.0, 0], aligned_edge=RIGHT)
        inside_frame(ccli, cmd)
        apart(ccli, cmd)
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(puff2, fewer, c223)), *tm.parts_out("slider"), run_time=0.5)
            self.play(*tm.lift_always_on(), run_time=1.0)
            ep = model_box("Vertex AI endpoint", w=2.6, h=0.5).move_to(tm.always_on_slot())
            inside_frame(ep)
            apart(ep, tm.parts["always"])
            apart(ep, tm.parts["ticks"])
            vo.wait_until("So does next lecture")
            lr = lref_swap(self, lr, 15, "11")
            self.play(FadeIn(ep, shift=LEFT * 0.6), run_time=0.7)
            vo.wait_until("minimum replica count")
            self.play(FadeIn(ccli, shift=UP * 0.1), Indicate(ep, color=COST, scale_factor=1.05), run_time=0.7)
            vo.wait_until("the part that costs money")
            self.play(FadeIn(cmd, shift=UP * 0.1), run_time=0.6)
            self.play(Indicate(tm.parts["band"].drip, color=COST, scale_factor=1.3), run_time=vo.remaining(0.6))

        # ========================================================== 6. test it on a new case (PONDER P2)
        qm = label("?", 48, S.GREY).move_to([5.2, 0.4, 0])
        apart(qm, tm.parts["vm_meter"])
        apart(qm, tm.parts["fn_meter"])
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(ep, ccli, cmd)), FadeOut(lr), *tm.parts_out("band", "always"), run_time=0.7)
            vo.wait_until("Twice as many requests")
            self.play(Indicate(tm.parts["ticks"], color=TURN, scale_factor=1.05), run_time=1.0)
            vo.wait_until("Which bill changes")
            self.play(FadeIn(qm, scale=0.6), m.pulse(2), run_time=vo.remaining(0.6))
        card = ponder(self, P2_Q, P2_OPTS, 10, dimmed=[m, tm], hide=[qm])

        # ========================================================== 7. the reveal: transform 2
        foot = label("until it runs out of capacity", CAPTION, S.GREY)
        foot.move_to([6.5, tm.VM_Y - 0.5, 0], aligned_edge=RIGHT)
        inside_frame(foot)
        with self.voiceover(SAY[7]) as vo:
            self.play(*right_covering_note(card, *P2_RIGHT), run_time=0.7)
            vo.wait_until("Watch")
            self.play(FadeOut(card), run_time=0.5)
            self.play(undim(tm), run_time=0.4)
            self.play(*tm.unstretch(), run_time=0.9)
            vo.wait_until("every request splits")
            self.play(*tm.double(), run_time=1.6)
            vo.wait_until("The VM meter does not move")
            self.play(Indicate(tm.parts["vm_meter"], color=COST, scale_factor=1.05), FadeIn(foot), run_time=0.9)
            apart(foot, tm.parts["flat"])
            vo.wait_until("A is backwards")
            self.play(FadeIn(card), run_time=0.4)
            self.play(*card.wrong(0, P2_WRONG[0]), run_time=0.5)
            vo.wait_until("C is wrong")
            self.play(*card.wrong(2, P2_WRONG[2]), run_time=0.5)
            vo.wait_until("D confuses")
            self.play(*card.wrong(3, P2_WRONG[3]), run_time=0.5)
            self.wait(vo.remaining(0.3))

        # ========================================================== 8. the rule -> map slot 2
        myth = chip("serverless = cheap", S.GREY, size=24).move_to([0, 1.95, 0])
        cross = strike(myth)
        q = label("Is anything always on?", 28, INK, weight="BOLD")
        row1 = arrow_row("idle time", "always-on bills only")
        row2 = arrow_row("requests × duration", "pay-per-use bill only")
        rows = VGroup(row1, row2).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        body = VGroup(q, rows).arrange(DOWN, buff=0.35)
        frame = RoundedRectangle(width=body.width + 0.8, height=body.height + 0.6, corner_radius=0.16,
                                 stroke_color=COST, stroke_width=3).set_fill(S.BG, 0.96)
        body.move_to(frame)
        gold = VGroup(frame, body).move_to([0, 0.35, 0])
        rule = RuleCard(RULE_TOP, RULE_BOTTOM)
        inside_frame(myth, gold, rule)
        apart(myth, gold)
        apart(gold, rule)
        guard(myth.get_top()[1] <= 2.55, "the myth chip reaches the map's label")
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(card), FadeOut(foot), FadeOut(tm), FadeOut(VGroup(vm_lab, fn_lab)), undim(m),
                      run_time=0.7)
            self.play(FadeIn(myth, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("serverless is cheap")
            self.play(Create(cross), myth.animate.set_opacity(0.5), run_time=0.6)
            vo.wait_until("is anything always on")
            self.play(FadeIn(frame), Write(q), FadeIn(row1.left_t), FadeIn(row2.left_t), run_time=0.9)
            vo.wait_until("Idle time moves")
            self.play(GrowArrow(row1.arrow), FadeIn(row1.right_t, shift=RIGHT * 0.15), run_time=0.8)
            vo.wait_until("Request count and duration")
            self.play(GrowArrow(row2.arrow), FadeIn(row2.right_t, shift=RIGHT * 0.15), run_time=0.8)
            self.play(rule.frame_in(), run_time=0.4)
            self.play(rule.line_in(0), run_time=0.6)
            self.play(rule.line_in(1), run_time=vo.remaining(0.6))
        self.wait(0.8)
        rule.shrink_into(self, m, 2)
        self.play(m.pulse(2), run_time=0.7)
        self.wait(0.5)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.8)
        self.wait(0.3)
