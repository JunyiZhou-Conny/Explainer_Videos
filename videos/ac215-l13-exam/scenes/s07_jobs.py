"""S07 · Training that outlives the request (V5, request clock vs job ticket; cli.sh's submission).
Lecture: 22, 24–25.

Beats (script.md "## S07", one voiceover block each):
 0  V5 opens: a GREY laptop client (a "retrain" button on its screen) on the left, the schematic
    web server with its handler `POST /retrain` in the middle (illustration tag); on "retrain
    button" a GREY request arrow grows from the laptop to the handler; on "training takes an
    hour" a clock "training: ~1 hour" comes in top left and its hand turns.
 1  Three nested lifetime rings form round the server (request · server instance · job, each with
    its lifetime). On "Inside the request handler" a training track is pinned to the handler
    inside the inner ring; its GREEN fill grows to the request ring's edge and snaps (RED +
    crack), the request arrow turns RED with a ✗ where the request ring cuts it; RED verdict "in
    the handler".
 2  The cracked bar and the cut arrow leave; a new track is pinned in the server ring, below the
    request ring ("a thread" origin label); it grows past the request ring to the server ring's
    edge, then the server instance blinks out with its handler and a fresh one appears; the bar
    vanishes with it. RED verdict "a server thread".
 3  A GREY dashed client-timeout ring round the laptop stretches wide (past the server ring); a
    new request arrow, a GREY "proxy" chip on the request ring's edge, and the request ring still
    cuts the arrow (RED ✗); the laptop lid closes and the waiting client disappears. RED verdict
    "a longer client timeout · wrong clock".
 4  The V1 ledger miniature sits outside the rings (top right) with a GREY chip "W&B · watches
    · no engine"; a GREEN bar flies at it and bounces off (RED ✗): no bar can be pinned to it.
 5  LECTURE 22, 24. The right design: the request and server rings fade, the handler moves left
    inside a small GREEN "request · seconds" ring, a new laptop above it; a BLUE "Vertex AI" box
    fills the job ring's right side. On "submits a durable job" a request arrow, then a BLUE
    ticket slides from the handler into Vertex; on "returns its id" `job id: ‹job-id›` jumps back
    under the laptop. The job's own BLUE VM appears with a training bar and the GOLD "$ while
    running" meter; the state chips light QUEUED, PENDING, RUNNING as spoken (the bar starts on
    RUNNING, the meter turns); the laptop closes; on "Anyone with access" a second client polls
    the id and reads RUNNING; then the bar reaches its end, SUCCEEDED lights GREEN and the meter
    stops.
 6  The picture leaves (the tag stays); slide 22's points redrawn as four GREY chips ("on an
    as-need basis", "GPU only for the training step", "no server setup", "lower training cost")
    and the GREY note "serverless ≠ no machine: a VM you don't own" beside a BLUE VM glyph whose
    dashed GREY outline reads "not yours".
 7  CODE(cli.sh: 30–37, wrap=True): line 32 lights BLUE and a copy of it becomes the ticket under
    the panel; lines 33, 34, 35, 36 light in turn as the SAY names region, name, package and
    worker pool, each adding a GREY field chip beside the ticket; then machine-type,
    replica-count, executor-image-uri, python-module light inside the wrapped line 36.
 8  Everything fades (lecture tag too). PONDER card 3 (mcq_card, centred). After the block the
    timer drains (10 s, silent); the card fades.
 9  The same card returns with the header "Answer"; row B gets the YELLOW outline; rows A, C, D
    swap in place into their RED reasons as named.
10  Takeaway (YELLOW, centred): "If the question says training takes longer than the request,
    think: submit a durable job, return its id, poll; W&B only watches." Fade to an empty frame.

Deviations from SHOW: (1) in beat 2 the "server thread" bar runs in the band between the request
ring and the server ring (not over the handler), so it visibly starts outside the request; (2)
the laptop sits inside the job ring's left band in beats 0–3 (the job ring fills the frame; no
room outside it); (3) beat 5 rearranges the V5 picture inside the job ring (the request and
server rings fade; a small GREEN request ring and a Vertex AI box take their place) because the
ticket, VM, meter and the 8.1-wide state machine do not fit between the nested rings; (4) the
state chips light QUEUED → RUNNING as they are said, and SUCCEEDED lights only after the second
client has polled RUNNING (so the poll does not read a state that has already passed); (5) beat
7's field chips (region, name, package, worker pool) beside the ticket show "lines 33–36 light
in turn" a second time, in words, so the ticket visibly gathers its fields.
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Circle,
    Create,
    DashedVMobject,
    Ellipse,
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
    LaggedStart,
    Line,
    RoundedRectangle,
    Rotate,
    VGroup,
    Write,
    linear,
)

from common import *  # noqa: F401,F403
from common import guard
from explainer import style as S
from explainer.scene import VoiceScene

SAY = NARRATION["S07"]

# ------------------------------------------------------------------ the real sources
assert source_line("cli.sh", 30).strip() == "# Run training with No GPU", source_line("cli.sh", 30)
assert source_line("cli.sh", 32).strip() == "gcloud ai custom-jobs create \\", source_line("cli.sh", 32)
assert source_line("cli.sh", 33).strip().startswith("--region="), source_line("cli.sh", 33)
assert source_line("cli.sh", 34).strip().startswith("--display-name="), source_line("cli.sh", 34)
assert source_line("cli.sh", 35).strip().startswith("--python-package-uris="), source_line("cli.sh", 35)
L36 = source_line("cli.sh", 36)
assert L36.strip().startswith("--worker-pool-spec="), L36
KEYS36 = ("machine-type", "replica-count", "executor-image-uri", "python-module")
for _k in KEYS36:
    assert _k in L36, _k
assert JOB_STATES == ("QUEUED", "PENDING", "RUNNING", "SUCCEEDED"), JOB_STATES

PONDER_Q = ["Your Vertex AI custom job shows `RUNNING`. You close the laptop for the night.",
            "What happens to the training?"]
PONDER_OPTS = ["it stops once the CLI container exits", "it runs on its own VM until done or failed",
               "it pauses until W&B reconnects", "it restarts from epoch 1 later"]
RIGHT_I = 1
REASONS = {0: "the CLI container's part ended at submit", 2: "W&B logs, it doesn't drive",
           3: "nothing on your laptop holds the job's state"}
for _o in PONDER_OPTS:
    assert len(_o) <= 46, _o
# break line 36 at its keys so each key stays whole on its own row (12 rows in all)
WRAP = {31: ['"us-docker'], 36: ["replica-count", "executor-image-uri", "python-module"]}
SLIDE22 = ("on an as-need basis", "GPU only for the training step", "no server setup", "lower training cost")
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


def within(m, frame, pad: float = 0.05):
    """m lies inside the rectangle of `frame`."""
    guard(m.get_left()[0] >= frame.get_left()[0] + pad and m.get_right()[0] <= frame.get_right()[0] - pad
          and m.get_bottom()[1] >= frame.get_bottom()[1] + pad and m.get_top()[1] <= frame.get_top()[1] - pad,
          "not inside its frame")


def below_tag(m, slides: str = "22, 24"):
    t = lref(slides)
    guard(m.get_top()[1] <= t.get_bottom()[1] - 0.05 or m.get_right()[0] <= t.get_left()[0] - 0.05,
          "under the lecture tag")


def flash(mob, color=TURN, k: float = 1.12, run_time: float = 0.6):
    return Indicate(mob, color=color, scale_factor=k, run_time=run_time)


def frac_to(bar: TrainingBar, x: float) -> float:
    """The grow() fraction that puts the fill's right end at x."""
    left = bar.track.get_left()[0] + 0.06
    return (x - left) / (bar.w - 0.12)


def clock_glyph(r: float = 0.3) -> VGroup:
    face = Circle(radius=r, stroke_color=INK, stroke_width=3).set_fill(S.BG, 1)
    minute = Line(face.get_center(), face.get_center() + UP * r * 0.78, color=INK, stroke_width=3)
    hour = Line(face.get_center(), face.get_center() + RIGHT * r * 0.55, color=INK, stroke_width=3)
    g = VGroup(face, hour, minute)
    g.face, g.minute = face, minute
    return g


def verdict(text: str) -> VGroup:
    """A RED label with a ✗, for the bottom band of the job ring."""
    g = VGroup(x_mark(0.26), label(text, 22, ERR)).arrange(RIGHT, buff=0.18)
    return g


def close_lid(lap):
    """The laptop's screen folds down onto its base."""
    sc = lap.screen
    return sc.animate.stretch_to_fit_height(0.06).move_to(sc.get_bottom() + UP * 0.03)


class DurableJob(VoiceScene):
    def construct(self):
        assert len(SAY) == 11, len(SAY)

        # ========================================================== 0 · the retrain button
        rings = LifetimeRings()
        job_fr, srv_fr, req_fr = rings.ring("job"), rings.ring("server"), rings.ring("request")
        for fr in (job_fr, srv_fr, req_fr):
            fr.set_z_index(3)
        hb = handler_box().move_to(rings.inner_center())
        lap = laptop(1.1)
        place(lap, cx=-5.6, cy=hb.get_center()[1])
        btn = chip("retrain", S.GREY, size=20, pad_x=0.12, pad_y=0.06).move_to(lap.screen)
        client = VGroup(lap, btn)
        y_req = hb.get_center()[1]
        arrow0 = Arrow([lap.get_right()[0] + 0.05, y_req, 0], [hb.get_left()[0] - 0.05, y_req, 0],
                       color=S.GREY, stroke_width=4, buff=0, tip_length=0.2)
        clock = clock_glyph()
        clock_t = label("training: ~1 hour", 24, INK)
        clk = VGroup(clock, clock_t).arrange(RIGHT, buff=0.2)
        place(clk, left=-6.3, cy=2.95)
        itag = illustration_tag()
        place(itag, left=-6.4, cy=-3.36)
        inside(rings, hb, client, clk, itag)
        guard(lap.get_left()[0] > job_fr.get_left()[0] + 0.05 and lap.get_right()[0] < srv_fr.get_left()[0] - 0.05,
              "the laptop is not in the job ring's left band")
        guard(clk.get_bottom()[1] > job_fr.get_top()[1] + 0.1, "the clock touches the job ring")
        guard(itag.get_top()[1] < job_fr.get_bottom()[1] - 0.03, "the illustration tag touches the job ring")
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(hb, shift=UP * 0.2), FadeIn(itag), run_time=0.8)
            vo.wait_until("retrain button")
            self.play(FadeIn(client, shift=RIGHT * 0.2), run_time=0.6)
            self.play(flash(btn, TURN, 1.15, 0.5), GrowArrow(arrow0), run_time=0.8)
            vo.wait_until("training takes an hour")
            self.play(FadeIn(clk, shift=DOWN * 0.15), run_time=0.6)
            self.play(Rotate(clock.minute, -2 * np.pi, about_point=clock.face.get_center()), run_time=1.2)
            vo.wait_until("Where should")
            self.play(flash(clock_t, TURN, 1.08, 0.8))

        # ========================================================== 1 · lifetimes; inside the handler
        bar1 = TrainingBar(4.6, caption=None)
        place(bar1, left=hb.get_right()[0] + 0.2, cy=y_req)
        x_req = req_fr.get_right()[0]
        cut1 = x_mark(0.34).move_to([req_fr.get_left()[0], y_req, 0]).set_z_index(5)
        v1 = verdict("in the handler")
        y_v = (srv_fr.get_bottom()[1] + job_fr.get_bottom()[1]) / 2
        place(v1, cx=0, cy=y_v)
        inside(bar1, v1)
        guard(bar1.get_right()[0] < job_fr.get_right()[0] - 0.2, "the bar leaves the job ring")
        guard(v1.get_top()[1] < srv_fr.get_bottom()[1] - 0.05 and v1.get_bottom()[1] > job_fr.get_bottom()[1] + 0.05,
              "the verdict leaves the band under the server ring")
        with self.voiceover(SAY[1]) as vo:
            rings.reveal(self, "request", run_time=0.6)
            self.bring_to_front(hb, client, arrow0)
            self.play(*rings.parts_in("server"), run_time=0.6)
            self.play(*rings.parts_in("job"), run_time=0.6)
            vo.wait_until("Inside the request handler")
            self.play(flash(rings.parts["request"], TURN, 1.02, 0.6))
            self.play(FadeIn(bar1, shift=RIGHT * 0.15), run_time=0.5)
            self.play(bar1.grow(frac_to(bar1, x_req - 0.04), run_time=vo.until("it dies", 1.2)))
            vo.wait_until("it dies")
            self.play(*bar1.snap(), arrow0.animate.set_color(ERR), FadeIn(cut1, scale=1.4), run_time=0.6)
            self.play(FadeIn(v1, shift=UP * 0.15), run_time=0.5)

        # ========================================================== 2 · a server thread
        bar2 = TrainingBar(6.4, caption=None)
        y_thr = (req_fr.get_bottom()[1] + srv_fr.get_bottom()[1]) / 2
        place(bar2, left=-0.3, cy=y_thr)
        thr = label("thread", 20, S.GREY)
        place(thr, right=bar2.get_left()[0] - 0.15, cy=y_thr)
        v2 = verdict("a server thread")
        place(v2, cx=0, cy=y_v)
        x_srv = srv_fr.get_right()[0]
        inside(bar2, thr, v2)
        guard(bar2.get_top()[1] < req_fr.get_bottom()[1] - 0.05 and bar2.get_bottom()[1] > srv_fr.get_bottom()[1] + 0.05,
              "the thread bar leaves the band between the request and server rings")
        guard(bar2.get_right()[0] < job_fr.get_right()[0] - 0.2, "the thread bar leaves the job ring")
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(bar1, cut1, arrow0, v1)), run_time=0.5)
            self.play(FadeIn(bar2, shift=RIGHT * 0.15), FadeIn(thr), run_time=0.5)
            self.play(bar2.grow(frac_to(bar2, x_req), run_time=1.4))
            vo.wait_until("that server instance")
            self.play(bar2.grow(frac_to(bar2, x_srv - 0.1), run_time=vo.until("which the platform", 1.0)))
            vo.wait_until("recycles")
            self.play(*rings.parts_out("server", "request"), hb.animate.set_opacity(0.08), FadeOut(bar2),
                      FadeOut(thr), run_time=0.5)
            self.play(*rings.parts_in("server", "request"), hb.animate.set_opacity(1), run_time=0.6)
            self.play(FadeIn(v2, shift=UP * 0.15), run_time=0.5)

        # ========================================================== 3 · a longer client timeout
        cring = DashedVMobject(Ellipse(width=1.6, height=1.6, stroke_color=S.GREY, stroke_width=3), num_dashes=28)
        cring.move_to(lap.get_center())
        cring_w = DashedVMobject(Ellipse(width=2.45, height=1.6, stroke_color=S.GREY, stroke_width=3),
                                 num_dashes=44)
        place(cring_w, left=cring.get_left()[0], cy=lap.get_center()[1])
        c_lab = VGroup(label("client", 20, S.GREY), label("timeout", 20, S.GREY)).arrange(DOWN, buff=0.06)
        place(c_lab, cx=lap.get_center()[0], bottom=cring_w.get_top()[1] + 0.15)
        arrow3 = arrow0.copy().set_color(S.GREY)
        proxy = chip("proxy", S.GREY, size=20)
        place(proxy, cx=req_fr.get_left()[0], top=y_req - 0.3)
        cut3 = x_mark(0.34).move_to([req_fr.get_left()[0], y_req, 0]).set_z_index(5)
        v3 = verdict("a longer client timeout · wrong clock")
        place(v3, cx=0, cy=y_v)
        inside(cring, cring_w, c_lab, proxy, v3)
        guard(cring_w.get_right()[0] < req_fr.get_left()[0] - 0.1, "the client ring reaches the request ring")
        guard(cring_w.get_right()[0] > srv_fr.get_left()[0] + 0.3, "the client ring does not pass the server ring")
        apart(c_lab, cring_w, 0.05)
        apart(proxy, cring_w, 0.05)
        apart(proxy, hb, 0.1)
        guard(proxy.get_bottom()[1] > req_fr.get_bottom()[1] + 0.05, "the proxy chip leaves the request ring's edge")
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(v2), Create(cring), run_time=0.6)
            vo.wait_until("moves the wrong clock")
            self.play(cring.animate.become(cring_w), FadeIn(c_lab, shift=UP * 0.1), run_time=1.2)
            vo.wait_until("The server and the proxies")
            self.play(GrowArrow(arrow3), FadeIn(proxy, shift=DOWN * 0.1), run_time=0.7)
            vo.wait_until("still cut the request")
            self.play(arrow3.animate.set_color(ERR), FadeIn(cut3, scale=1.4), flash(proxy, ERR, 1.1, 0.6),
                      run_time=0.6)
            vo.wait_until("a sleeping laptop")
            self.play(close_lid(lap), FadeOut(btn), run_time=0.7)
            self.play(FadeOut(VGroup(lap, cring, c_lab, arrow3, cut3)), run_time=0.6)
            self.play(FadeIn(v3, shift=UP * 0.15), run_time=0.5)

        # ========================================================== 4 · W&B is not a clock
        mini = miniature("run", caption=False)
        place(mini, right=6.3, cy=2.95)
        wchip = chip("W&B · watches · no engine", S.GREY, size=20)
        place(wchip, right=mini.get_left()[0] - 0.25, cy=mini.get_center()[1])
        ghost = TrainingBar(1.6, caption=None)
        ghost.fill.stretch_to_fit_width(1.3).move_to(ghost.track)
        place(ghost, cx=0.8, cy=y_v)
        bounce = x_mark(0.3)
        inside(mini, wchip, ghost)
        guard(mini.get_bottom()[1] > job_fr.get_top()[1] + 0.08, "the W&B miniature touches the job ring")
        apart(wchip, clk, 0.3)
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(v3, proxy)), run_time=0.5)
            self.play(FadeIn(mini, shift=LEFT * 0.2), run_time=0.6)
            vo.wait_until("it logs runs")
            self.play(FadeIn(wchip, shift=LEFT * 0.15), mini.replay(), run_time=1.0)
            vo.wait_until("has no engine")
            self.play(FadeIn(ghost), run_time=0.4)
            self.play(ghost.animate.move_to(mini.get_center()).scale(0.7), run_time=0.8)
            place(bounce, cx=ghost.get_center()[0], cy=ghost.get_center()[1])
            self.play(FadeIn(bounce, scale=1.4), ghost.animate.set_opacity(0.25), run_time=0.4)
            self.play(FadeOut(VGroup(ghost, bounce), shift=DOWN * 0.4), flash(wchip, TURN, 1.06, 0.6), run_time=0.6)

        # ========================================================== 5 · the right design: a durable job
        # left column: laptop, handler in a small GREEN request ring, a second client
        hb_to = hb.copy()
        place(hb_to, cx=-4.4, cy=-0.5)
        gring = RoundedRectangle(width=hb_to.width + 0.4, height=hb_to.height + 0.4, corner_radius=0.3,
                                 stroke_color=OWN, stroke_width=3).set_fill(opacity=0).move_to(hb_to)
        g_lab = label("request · seconds", 20, OWN)
        place(g_lab, cx=gring.get_center()[0], top=gring.get_bottom()[1] - 0.08)
        lap2 = laptop(1.0)
        place(lap2, cx=-4.4, top=job_fr.get_top()[1] - 0.38)
        req5 = Arrow(lap2.get_bottom() + DOWN * 0.05, [hb_to.get_center()[0], hb_to.get_top()[1] + 0.03, 0],
                     color=S.GREY, stroke_width=4, buff=0, tip_length=0.18)
        id_chip = chip(f"job id: {JOB_ID}", S.GREY, size=20, font=MONO)
        id_chip.text.set_color(S.GREY)
        place(id_chip, cx=lap2.get_center()[0], cy=(lap2.get_bottom()[1] + gring.get_top()[1]) / 2)
        # the Vertex AI box on the right
        vx = RoundedRectangle(width=8.6, height=4.65, corner_radius=0.25, stroke_color=CLOUD,
                              stroke_width=3).set_fill(CLOUD, 0.06)
        place(vx, right=job_fr.get_right()[0] - 0.12, bottom=job_fr.get_bottom()[1] + 0.15)
        vx_t = label("Vertex AI", 24, CLOUD)
        place(vx_t, left=vx.get_left()[0] + 0.25, top=vx.get_top()[1] - 0.15)
        vm = RoundedRectangle(width=5.8, height=2.3, corner_radius=0.15, stroke_color=CLOUD,
                              stroke_width=3).set_fill(CLOUD, 0.1)
        place(vm, right=vx.get_right()[0] - 0.25, top=vx.get_top()[1] - 0.3)
        vm_t = label("its own VM", 20, CLOUD)
        place(vm_t, left=vm.get_left()[0] + 0.2, top=vm.get_top()[1] - 0.1)
        bar5 = TrainingBar(3.2)
        place(bar5, left=vm.get_left()[0] + 0.25, top=vm_t.get_bottom()[1] - 0.25)
        meter = CostMeter()
        place(meter, right=vm.get_right()[0] - 0.15, cy=bar5.track.get_center()[1] - 0.05)
        ticket = JobTicket(w=1.9)
        place(ticket, left=vx.get_left()[0] + 0.2, cy=vm.get_center()[1] - 0.25)
        states = StateChips()
        place(states, cx=vx.get_center()[0], bottom=vx.get_bottom()[1] + 0.4)
        # the second client
        lap3 = laptop(0.8)
        place(lap3, left=job_fr.get_left()[0] + 0.25, cy=states.get_center()[1] - 0.05)
        poll = label("poll", 22, LOOKUP)
        place(poll, left=lap3.get_right()[0] + 0.15, cy=lap3.get_center()[1])
        reads = chip("RUNNING", CLOUD, size=20, font=MONO)
        place(reads, left=poll.get_right()[0] + 0.2, cy=lap3.get_center()[1])
        poll_ar = Arrow([poll.get_right()[0] + 0.05, reads.get_center()[1], 0],
                        [vx.get_left()[0] - 0.02, reads.get_center()[1], 0],
                        color=LOOKUP, stroke_width=4, buff=0, tip_length=0.18)
        hand_ar = Arrow([gring.get_right()[0] + 0.02, ticket.get_center()[1], 0],
                        [ticket.get_left()[0] - 0.15, ticket.get_center()[1], 0],
                        color=CLOUD, stroke_width=4, buff=0, tip_length=0.18)
        inside(gring, g_lab, lap2, id_chip, vx, lap3, poll, reads, poll_ar)
        below_tag(vx)
        for m in (vx_t, vm, bar5, meter, ticket, states):
            within(m, vx)
        for m in (vm_t, bar5, meter):
            within(m, vm)
        apart(vx_t, vm, 0.1)
        apart(ticket, vm, 0.15)
        apart(states, vm, 0.15)
        apart(bar5, meter, 0.15)
        apart(gring, vx, 0.15)
        apart(lap2, id_chip, 0.05)
        apart(id_chip, gring, 0.05)
        apart(g_lab, lap3, 0.1)
        apart(g_lab, poll, 0.1)
        apart(g_lab, reads, 0.1)
        apart(reads, vx, 0.15)
        guard(poll_ar.get_length() > 0.6, "the poll arrow is too short")
        apart(lap2, rings.parts["job"][1], 0.1)
        apart(vx, rings.parts["job"][1], 0.1)
        guard(gring.get_left()[0] > job_fr.get_left()[0] + 0.1, "the request ring leaves the job ring")
        guard(lap3.get_bottom()[1] > job_fr.get_bottom()[1] + 0.05, "the second client leaves the job ring")
        with self.voiceover(SAY[5]) as vo:
            self.play(*rings.parts_out("request", "server"), FadeOut(VGroup(mini, wchip)),
                      hb.animate.move_to(hb_to), run_time=0.9)
            lr = lref_swap(self, None, "22, 24")
            self.play(Create(gring), FadeIn(g_lab), FadeIn(lap2, shift=DOWN * 0.15), FadeIn(vx), FadeIn(vx_t),
                      run_time=0.8)
            vo.wait_until("the handler submits")
            self.play(GrowArrow(req5), run_time=0.5)
            self.play(GrowArrow(hand_ar), FadeIn(ticket, shift=RIGHT * 0.6), run_time=0.8)
            vo.wait_until("returns its id")
            id_src = id_chip.copy().move_to(hb.get_center())
            self.play(FadeOut(req5), FadeOut(hand_ar), id_src.animate.move_to(id_chip), run_time=0.6)
            self.remove(id_src)
            self.add(id_chip)
            self.play(flash(gring, OWN, 1.04, 0.6))
            vo.wait_until("The job moves")
            self.play(FadeIn(vm), FadeIn(vm_t), FadeIn(bar5), FadeIn(meter), FadeIn(states), run_time=0.7)
            vo.wait_until("queued")
            self.play(*states.light(0), run_time=0.3)
            vo.wait_until("pending")
            self.play(*states.light(1), run_time=0.3)
            vo.wait_until("running")
            self.play(*states.light(2), run_time=0.3)
            vo.wait_until("on its own machine")
            self.play(bar5.grow(0.3, run_time=1.2), meter.run(1.2), flash(vm_t, CLOUD, 1.1, 1.2), run_time=1.2)
            vo.wait_until("billed only")
            self.play(flash(meter, COST, 1.08, 0.7), bar5.grow(0.4, run_time=0.7))
            self.play(close_lid(lap2), FadeOut(id_chip), bar5.grow(0.5, run_time=0.8), run_time=0.8)
            self.play(FadeOut(lap2), bar5.grow(0.55, run_time=0.4), run_time=0.4)
            vo.wait_until("Anyone with access")
            self.play(FadeIn(lap3, shift=RIGHT * 0.15), FadeIn(poll), bar5.grow(0.65, run_time=0.6), run_time=0.6)
            vo.wait_until("poll the id")
            self.play(GrowArrow(poll_ar), flash(ticket.id_text, LOOKUP, 1.15, 0.6), bar5.grow(0.72, run_time=0.6),
                      run_time=0.6)
            reply = states.chips[2].copy()
            self.play(FadeOut(poll_ar), flash(states.chips[2], CLOUD, 1.1, 0.5), bar5.grow(0.76, run_time=0.5),
                      run_time=0.5)
            self.play(reply.animate.move_to(reads), bar5.grow(0.8, run_time=0.7), run_time=0.7)
            self.remove(reply)
            self.add(reads)
        self.play(bar5.grow(1.0, run_time=1.0), run_time=1.0)
        self.play(*states.light(3), meter.stop(), run_time=0.5)
        self.wait(0.4)

        # ========================================================== 6 · slide 22: serverless training
        chips22 = VGroup(*[chip(s, S.GREY, size=24) for s in SLIDE22])
        grid22 = VGroup(VGroup(chips22[0], chips22[1]).arrange(RIGHT, buff=0.5),
                        VGroup(chips22[2], chips22[3]).arrange(RIGHT, buff=0.5)).arrange(DOWN, buff=0.4)
        head22 = label("slide 22 · serverless training", 24, S.GREY)
        top22 = VGroup(head22, grid22).arrange(DOWN, buff=0.45)
        place(top22, cx=0, top=2.7)
        vmg = RoundedRectangle(width=1.5, height=0.9, corner_radius=0.12, stroke_color=CLOUD,
                               stroke_width=3).set_fill(CLOUD, 0.15)
        vmg_t = label("VM", 24, CLOUD).move_to(vmg)
        own = DashedVMobject(RoundedRectangle(width=2.3, height=1.6, corner_radius=0.2, stroke_color=S.GREY,
                                              stroke_width=2.5), num_dashes=36).move_to(vmg)
        own_t = label("not yours", 20, S.GREY)
        place(own_t, cx=own.get_center()[0], top=own.get_bottom()[1] - 0.1)
        vm_g = VGroup(own, vmg, vmg_t, own_t)
        note22 = label("serverless ≠ no machine: a VM you don't own", 26, INK)
        bottom22 = VGroup(vm_g, note22).arrange(RIGHT, buff=0.5)
        place(bottom22, cx=0, top=top22.get_bottom()[1] - 0.6)
        inside(top22, bottom22)
        below_tag(top22)
        apart(top22, bottom22, 0.3)
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(rings, hb, gring, g_lab, vx, vx_t, vm, vm_t, bar5, meter, ticket, states,
                                     lap3, poll, reads, clk, itag)), run_time=0.6)
            self.play(FadeIn(head22, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("hardware rented")
            self.play(LaggedStart(FadeIn(chips22[1], shift=UP * 0.1), FadeIn(chips22[0], shift=UP * 0.1),
                                  lag_ratio=0.4), run_time=0.9)
            vo.wait_until("no server to manage")
            self.play(FadeIn(chips22[2], shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(chips22[3], shift=UP * 0.1), run_time=0.5)
            vo.wait_until("There is still a machine")
            self.play(FadeIn(vmg), FadeIn(vmg_t), Write(note22), run_time=0.9)
            vo.wait_until("you just do not own")
            self.play(Create(own), FadeIn(own_t), run_time=0.8)
            self.play(flash(note22, TURN, 1.04, 0.6))

        # ========================================================== 7 · the ticket in the repo: cli.sh
        panel = src_panel("cli.sh", 30, 37, wrap=WRAP)
        place(panel, cx=0, top=3.05)
        b32, b33, b34, b35, b36 = (panel.bar(n, CLOUD, 0.2) for n in (32, 33, 34, 35, 36))
        ticket7 = JobTicket()
        place(ticket7, left=-6.2, top=panel.get_bottom()[1] - 0.3)
        fields = VGroup(*[chip(s, S.GREY, size=20) for s in ("region", "name", "package", "worker pool")])
        fields.arrange(RIGHT, buff=0.2)
        place(fields, left=ticket7.get_right()[0] + 0.4, cy=ticket7.get_center()[1])
        spans = [panel.span(36, k) for k in KEYS36]
        inside(panel, ticket7, fields)
        below_tag(panel)
        apart(panel, ticket7, 0.15)
        apart(panel, fields, 0.15)
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(top22, bottom22)), run_time=0.5)
            self.play(FadeIn(panel, shift=UP * 0.2), run_time=0.7)
            vo.wait_until("the ticket is one command")
            self.play(FadeIn(b32), run_time=0.4)
            line32 = panel.span(32, "gcloud ai custom-jobs create").copy()
            self.play(line32.animate.move_to(ticket7).set_opacity(0), FadeIn(ticket7, shift=DOWN * 0.2),
                      run_time=0.9)
            self.remove(line32)
            for n, b, f, word in ((33, b33, fields[0], "with a region"), (34, b34, fields[1], "a name"),
                                  (35, b35, fields[2], "the package"), (36, b36, fields[3], "a worker pool")):
                vo.wait_until(word)
                self.play(FadeIn(b), FadeIn(f, shift=LEFT * 0.1), run_time=0.4)
            for k, word in zip(KEYS36, ("machine type", "replica count", "prebuilt image", "and module")):
                vo.wait_until(word)
                self.play(flash(spans[KEYS36.index(k)], CLOUD, 1.12, 0.5))
        self.wait(0.6)

        # ========================================================== 8 · PONDER 3
        card = mcq_card(PONDER_Q, PONDER_OPTS)
        inside(card)
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(panel, b32, b33, b34, b35, b36, ticket7, fields)), FadeOut(lr), run_time=0.6)
            lr = None
            self.play(FadeIn(card, scale=0.95), run_time=0.6)
            vo.wait_until("Your custom job")
            self.play(flash(card.question[0], INK, 1.03, 0.7))
            vo.wait_until("What happens")
            self.play(flash(card.question[1], TURN, 1.04, 0.7))
            vo.wait_until("Pause here")
            self.play(LaggedStart(*[flash(o.text, INK, 1.04, 0.5) for o in card.options], lag_ratio=0.3),
                      run_time=1.2)
        tbar = card[3]
        self.play(tbar.animate(rate_func=linear).become(tbar.copy().scale(0.001, about_point=tbar.get_start())),
                  run_time=10.0)
        self.play(FadeOut(card), run_time=0.6)

        # ========================================================== 9 · the answer
        ans = mcq_card(PONDER_Q, PONDER_OPTS, answer=True)
        inside(ans)
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeIn(ans, scale=0.97), run_time=0.6)
            vo.wait_until("The answer is B")
            self.play(*ans.mark_right(RIGHT_I), run_time=0.6)
            vo.wait_until("it keeps running")
            self.play(flash(ans.options[RIGHT_I].text, TURN, 1.04, 0.7))
            for i, word in ((0, "A: the CLI"), (2, "C: W and B"), (3, "D: nothing")):
                vo.wait_until(word)
                self.play(*ans.reason(i, REASONS[i]), run_time=0.8)
        self.wait(0.5)

        # ========================================================== 10 · takeaway
        tk = takeaway("If the question says training takes longer than the request, think: submit a durable job, "
                      "return its id, poll; W&B only watches.")
        inside(tk)
        with self.voiceover(SAY[10]) as vo:
            self.play(FadeOut(ans), run_time=0.5)
            self.play(Write(tk), run_time=1.8)
            vo.wait_until("return its id")
            self.play(flash(tk[-1] if len(tk) > 1 else tk, OWN, 1.03, 0.7))
            vo.wait_until("W and B only watches")
            self.play(flash(tk, TURN, 1.04, 0.8))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
        self.wait(0.3)
