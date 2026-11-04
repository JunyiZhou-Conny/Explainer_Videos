"""S06 · Rent the machine, not the server (AC215 L13) — `RentTheMachine`.

Beats (script.md, ## S06; one voiceover block each). No tracker; lref("18–24") top right, whole scene.
0. Slides 19 and 21 as a schematic sidebar (`illustration`, no logo): 'Workbench → notebooks' ·
   'Training → jobs' (YELLOW, a small tab 'Custom jobs') · 'Pipelines → workflows' (GREY dashed 'L15').
1. Slide 22: a BLUE job tile materialises, its GOLD meter starts (no numbers), the training step runs,
   a GREY 'a server to set up' chip is struck, the tile dissolves and the meter stops. Caption
   'there is a machine · you don't manage its lifetime'.
2. V4 step 1 (TarballTrip.flags()): notebook globals peel off into a GREEN task.py as --epochs,
   --batch_size, --model_name, then --train_base, --wandb_key. GREY chip 'slide: epochs=25 · cli.sh
   sends --epochs=2'.
3. V1 (TrainingMap.at("S06")) lit as a plan (GREY 'plan · drawn'): task.py becomes the tarball and
   rides '2 · package & upload' into the bucket; 'Model Trainer CLI Container' over the cockpit fades
   to model-training-cli; '3 · create jobs' to Vertex AI; two tiles (CPU, RAM · T4), each with its own
   TEAL container. Then the CPU tile plays V4 step 4 in miniature (TarballTrip.vm(mini=True)) over the
   dimmed map: machine + meter, Google's image, the tarball unwraps, python -m trainer.task with the
   flag chips, the machine goes.
4. Two GREY cards: 'the job can't see your laptop' (PINK route from the internet into the job tile,
   CODE task.py: 96–100 small, 'anything to keep → somewhere durable'); 'the image that runs is
   Google's' (ORANGE 'Google' tabs on the job containers; the cockpit stays put).
5. All machines outlined; QUICK(4 s).
6. The answer: Colab runtimes and the job containers turn GREEN; the cockpit gets 'never · proved in
   scene 9'. Fade to an empty frame.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import (CLOUD, FLAGS, IMAGE, INK, NARRATION, OWNED, ROUTE, SAY_COUNT, SYSTEM, TURN, TarballTrip,
                    TrainingMap, band, card, code, dashed_chip, each, flag_chip, grey_chip, illustration_tag,
                    job_tile, label, lref, meter_run, meter_stop, note, outline_box, parcel, plan_tag, ponder_card,
                    ring, strike)
from common import console as console_window
from explainer import style as S

SAY = NARRATION["S06"]
QUICK_TEXT = "Your laptop has no GPU and no TensorFlow.\nWhich machines here will ever import TensorFlow?"
LIFT = 0.35      # beat 5: the map rises so the low QUICK card clears its bottom row (laptop, job tiles)
SIDEBAR_ENTRIES = (("Workbench", "notebooks"), ("Training", "jobs"), ("Pipelines", "workflows"))
TASK_CUTS = {97: ("github.com/", "releases/", "releases/")}     # keeps 'github.com/…releases/…'


def sidebar_row(name: str, what: str, row_w: float = 6.4) -> VGroup:
    """One console entry: 'Name → what' in a GREY row. .frame .name .what"""
    fr = RoundedRectangle(width=row_w, height=0.66, corner_radius=0.1, stroke_color=S.GREY,
                          stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
    n = label(name, 24, INK)
    w = label(f"→ {what}", 24, S.GREY)
    row = VGroup(n, w).arrange(RIGHT, buff=0.22).move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.3)
    g = VGroup(fr, row)
    g.frame, g.name_t, g.what = fr, n, w
    return g


def inner_box(tile) -> RoundedRectangle:
    """The job's own TEAL container, drawn as a frame just inside a map tile."""
    fr = tile.frame
    return RoundedRectangle(width=fr.width - 0.16, height=fr.height - 0.16, corner_radius=0.08,
                            stroke_color=IMAGE, stroke_width=2.5).move_to(fr)


def google_tab() -> VGroup:
    """The ORANGE 'Google' band on a job's container, on an opaque backing (the tile edge runs under it)."""
    b = band("Google", SYSTEM, 0.9, 0.32, 20)
    bk = RoundedRectangle(width=0.9, height=0.32, corner_radius=0.06, stroke_width=0).set_fill(S.BG, 1).move_to(b)
    return VGroup(bk, b)


def step_dot(n: int) -> VGroup:
    """A small GREY circle with the step number."""
    c = Circle(radius=0.2, stroke_color=S.GREY, stroke_width=2.5).set_fill(S.BG, 1)
    return VGroup(c, label(str(n), 20, INK).move_to(c))


def low_quick(scene, question: str, bottom: float = -3.58, width: float = 12.0, seconds: float = 4) -> VGroup:
    """QUICK(4 s) drawn like common.quick_predict (opaque frame, 'Quick predict' header, draining bar)
    with tighter padding, its bottom edge at `bottom`: it fits under the lifted map (top ≈ −1.2)."""
    src = ponder_card(question, width=width)
    yellow = src[0].get_stroke_color()
    q = src[2]
    hd = S.text("Quick predict", S.SMALL_SIZE, TURN, weight="BOLD")
    body = VGroup(hd, q).arrange(DOWN, buff=0.2)
    fr = RoundedRectangle(width=width, height=body.height + 0.7, corner_radius=0.2, stroke_color=yellow,
                          stroke_width=3).set_fill(S.BG, 1)
    fr.move_to([0, bottom + fr.height / 2, 0])
    body.move_to(fr).shift(UP * 0.15)
    bar = Line(fr.get_corner(DL) + RIGHT * 0.3 + UP * 0.22, fr.get_corner(DR) + LEFT * 0.3 + UP * 0.22,
               color=yellow, stroke_width=4)
    c = VGroup(fr, hd, q, bar)
    scene.play(FadeIn(c, scale=0.95), run_time=0.6)
    target = bar.copy().scale(0.001, about_point=bar.get_start())
    scene.play(bar.animate(rate_func=linear).become(target), run_time=seconds)
    return c


class RentTheMachine(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S06"] == 7, len(SAY)
        ref = lref("18–24")

        # ========================================================== 0. the console's three entries
        win = console_window(("Vertex AI",), win_w=7.4, win_h=3.5).move_to([0, 0.2, 0])
        ill = illustration_tag().next_to(win, UP, buff=0.12).align_to(win, RIGHT)
        rows = [sidebar_row(a, b) for a, b in SIDEBAR_ENTRIES]
        VGroup(*rows).arrange(DOWN, buff=0.22).move_to(win.content)
        tab = grey_chip("Custom jobs", color=TURN).move_to(rows[1].frame).align_to(rows[1].frame, RIGHT).shift(LEFT * 0.2)
        gcp_note = note("Google Cloud · machine learning platform").next_to(win.crumbs, RIGHT, buff=0.4)
        l15 = dashed_chip("L15").move_to(rows[2].frame).align_to(rows[2].frame, RIGHT).shift(LEFT * 0.2)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(ref), FadeIn(win, scale=0.97), run_time=0.8)
            self.play(FadeIn(ill, shift=LEFT * 0.15), run_time=0.4)
            vo.wait_until("Google Cloud's machine learning platform")
            self.play(FadeIn(gcp_note, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("Three console entries matter")
            self.play(LaggedStart(*[Create(r.frame) for r in rows], lag_ratio=0.25), run_time=0.9)
            for r, anchor in zip(rows, ("Workbench for notebooks", "Training for jobs", "and Pipelines for workflows")):
                vo.wait_until(anchor)
                self.play(FadeIn(r[1], shift=RIGHT * 0.25), run_time=0.5)
            vo.wait_until("Today is Training")
            r1 = rows[1]
            self.play(r1.frame.animate.set_stroke(TURN, 3), r1.name_t.animate.set_color(TURN),
                      rows[0].animate.set_opacity(0.45), rows[2].animate.set_opacity(0.45), run_time=0.7)
            vo.wait_until("on the custom jobs tab")
            self.play(FadeIn(tab, shift=LEFT * 0.2), run_time=0.5)
            vo.wait_until("lecture 15 uses Pipelines")
            self.play(rows[2].animate.set_opacity(1), FadeIn(l15, shift=LEFT * 0.2), run_time=0.6)

        # ========================================================== 1. rent the hardware for the step
        tile = job_tile("CPU, RAM", False, 22, 2.6, 2.2).move_to([0, 0.6, 0])
        step_t = label("training step", 22, INK).move_to(tile.frame.get_center() + UP * 0.35)
        bar_box = Rectangle(width=1.9, height=0.24, stroke_color=S.GREY, stroke_width=2).next_to(step_t, DOWN, buff=0.18)
        bar = Rectangle(width=1.9, height=0.24, stroke_width=0).set_fill(INK, 0.85).move_to(bar_box)
        bar.stretch(0.02, 0, about_edge=LEFT)
        server = dashed_chip("a server to set up", size=22).move_to([-4.3, 0.6, 0])
        server_x = strike(server, INK)
        ghost = outline_box(2.6, 2.2, S.GREY, solid=False).move_to(tile.frame)
        cap1 = label("there is a machine ·", 26, INK)
        cap2 = label("you don't manage its lifetime", 26, INK)
        VGroup(cap1, cap2).arrange(RIGHT, buff=0.2).move_to([0, -1.55, 0])

        with self.voiceover(SAY[1]) as vo:
            old = VGroup(win, ill, gcp_note, *rows, tab, l15)
            self.play(FadeOut(old), run_time=0.6)
            self.remove(*old)
            self.play(FadeIn(tile, scale=0.9), run_time=0.7)
            self.play(meter_run(tile.meter), FadeIn(step_t), FadeIn(bar_box), run_time=0.8)
            vo.wait_until("only for the training step")
            self.add(bar)
            self.play(bar.animate.stretch_to_fit_width(1.9, about_edge=LEFT), run_time=3.0, rate_func=linear)
            vo.wait_until("Nobody sets up a server")
            self.play(FadeIn(server, shift=RIGHT * 0.2), run_time=0.5)
            self.play(Create(server_x), run_time=0.5)
            vo.wait_until("and billing stops when the step ends")
            self.play(meter_stop(tile.meter), run_time=0.7)
            self.play(FadeOut(VGroup(tile, step_t, bar_box, bar), scale=0.92), FadeIn(ghost), run_time=0.9)
            self.remove(tile, step_t, bar_box, bar)
            vo.wait_until("There is still a machine")
            self.play(FadeIn(cap1, shift=UP * 0.15), Indicate(ghost, color=INK, scale_factor=1.04), run_time=0.8)
            vo.wait_until("you just don't manage its lifetime")
            self.play(FadeIn(cap2, shift=UP * 0.15), FadeOut(ghost), run_time=0.8)
            self.remove(ghost)

        # ========================================================== 2. V4 step 1: code to a file, choices to flags
        trip = TarballTrip.flags()
        head1 = VGroup(step_dot(1), label("move code to a Python file · pass arguments", 24, INK))
        head1.arrange(RIGHT, buff=0.2).move_to([0, 3.3, 0]).align_to([-6.5, 0, 0], LEFT)
        slide_chip = grey_chip("slide: epochs=25 · cli.sh sends --epochs=2").move_to([0, -1.25, 0])

        with self.voiceover(SAY[2]) as vo:
            old = VGroup(server, server_x, cap1, cap2)
            self.play(FadeOut(old), run_time=0.5)
            self.remove(*old)
            self.play(FadeIn(head1, shift=RIGHT * 0.2), FadeIn(trip, shift=UP * 0.2), run_time=0.8)
            vo.wait_until("and turn its hard-coded choices into flags")
            self.play(trip.peel(), run_time=1.8)
            self.play(FadeIn(slide_chip, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("The flags are epochs")
            self.play(each(trip.task.rows[:3], OWNED, scale=1.1, lag=0.25), run_time=1.2)
            vo.wait_until("plus train base")
            self.play(trip.more(), run_time=1.0)

        # ========================================================== 3. V1 as a plan, then V4 step 4 in miniature
        m = TrainingMap.at("S06")
        P = m.parts
        ptag = plan_tag().move_to([0, 3.3, 0]).align_to([-6.5, 0, 0], LEFT)
        pkg = parcel(None, OWNED, 20, 0.55, 0.4).move_to([-4.4, 1.4, 0])
        up_lab = VGroup(step_dot(2), note("package", INK), note("& upload", INK)).arrange(DOWN, buff=0.06)
        up_lab.move_to([-2.93, 1.25, 0])
        sub_lab = VGroup(step_dot(3), note("create jobs", INK)).arrange(RIGHT, buff=0.12).move_to([-0.65, -0.74, 0])
        mtc = card(["Model Trainer CLI", "Container"], size=20, buff=0.06)
        mtc.move_to(P["cockpit"].get_center() + DOWN * 0.05)
        cpu_c, gpu_c = inner_box(P["cpu_tile"]), inner_box(P["gpu_tile"])
        veil = Rectangle(width=13.2, height=7.2, stroke_width=0).set_fill(S.BG, 0.86)
        vm = TarballTrip.vm(mini=True, center=(-1.55, 0.5))
        tcopy = VGroup(P["cpu_tile"].copy(), cpu_c.copy())
        fr = vm.box[0]
        backing = fr.copy().set_stroke(width=0).set_fill(S.BG, 1)
        call = VGroup(DashedLine(tcopy[0].frame.get_corner(UL), fr.get_corner(UR), color=S.GREY, stroke_width=2),
                      DashedLine(tcopy[0].frame.get_corner(DL), fr.get_corner(DR), color=S.GREY, stroke_width=2))
        fchips = VGroup(*[flag_chip(f) for f in FLAGS]).arrange(DOWN, aligned_edge=RIGHT, buff=0.12)
        fchips.next_to(fr, LEFT, buff=0.15).align_to(fr, UP)

        with self.voiceover(SAY[3]) as vo:
            gone = VGroup(head1, slide_chip, trip.nb, *trip.task.rows, trip.task[1])
            self.play(FadeOut(gone), ReplacementTransform(trip.task[0], pkg), FadeIn(m), FadeIn(ptag),
                      run_time=1.2)
            self.remove(*gone, trip)
            vo.wait_until("one compressed archive")
            self.play(m.light("laptop"), Indicate(pkg, color=OWNED, scale_factor=1.25), run_time=0.8)
            vo.wait_until("and uploads it to a bucket")
            self.play(m.light("gcp"), m.reveal("upload"), FadeIn(up_lab), run_time=0.8)
            self.play(pkg.animate.move_to([-3.4, 0.6, 0]), run_time=0.4)
            self.play(pkg.animate.move_to(P["tarball"]), run_time=0.7)
            self.play(FadeOut(pkg), m.reveal("tarball"), run_time=0.4)
            self.remove(pkg)
            vo.wait_until("Model Trainer CLI Container")
            self.play(FadeIn(mtc, scale=1.1), run_time=0.6)
            vo.wait_until("our cockpit on your laptop")
            self.play(FadeOut(mtc), m.light("cockpit"), run_time=0.8)
            self.remove(mtc)
            vo.wait_until("it asks Vertex AI for a job")
            self.play(m.reveal("submit"), m.light("vertex"), FadeIn(sub_lab), run_time=0.9)
            vo.wait_until("Vertex AI then starts a machine")
            self.play(m.reveal("cpu_tile"), run_time=0.6)
            self.play(meter_run(P["cpu_tile"].meter), Create(cpu_c), run_time=0.7)
            vo.wait_until("or with one T4")
            self.play(m.reveal("gpu_tile"), run_time=0.6)
            self.play(meter_run(P["gpu_tile"].meter), Create(gpu_c), run_time=0.7)
            vo.wait_until("It loads Google's prebuilt")
            self.add(veil, ref, ptag, tcopy)
            self.play(FadeIn(veil), Create(call), run_time=0.5)
            self.add(backing)
            self.play(FadeIn(backing), vm.appear(), run_time=0.7)
            self.play(vm.image_in(), run_time=0.8)
            vo.wait_until("installs your tarball")
            self.play(vm.unwrap(), run_time=1.0)
            self.play(vm.pip(), run_time=0.5)
            vo.wait_until("runs your trainer with your flags")
            self.play(vm.run(), run_time=0.7)
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in fchips], lag_ratio=0.2), run_time=1.0)
            vo.wait_until("and deletes the machine")
            self.play(meter_stop(vm.meter), meter_stop(P["cpu_tile"].meter), meter_stop(P["gpu_tile"].meter),
                      run_time=0.6)
            inside = VGroup(backing, vm.box, vm.meter, vm.image, vm.layer, vm.trainer, vm.wandb_chip, vm.argv)
            self.play(FadeOut(inside, scale=0.9), FadeOut(fchips), FadeOut(call), FadeOut(tcopy), FadeOut(veil),
                      FadeOut(ptag), run_time=1.0)
            self.remove(inside, vm, fchips, call, tcopy, veil, ptag)

        # ========================================================== 4. two facts: no laptop, Google's image
        panel = code("package/trainer/task.py", 96, 100, font_size=20, cuts=TASK_CUTS)
        keep = grey_chip("anything to keep → somewhere durable", color=INK)
        card1 = card(["the job can't see your laptop", panel, keep], size=24, buff=0.25, card_w=7.65)
        card1.move_to([0, 0, 0]).align_to([-6.5, 0, 0], LEFT).align_to([0, 2.75, 0], UP)
        card1.body.remove(keep)
        net = grey_chip("internet · a GitHub release").move_to([2.27, -2.1, 0])
        pull = Arrow(net.get_top(), P["cpu_tile"].frame.get_bottom(), buff=0.06, color=ROUTE, stroke_width=5,
                     tip_length=0.2)
        url = panel.code.code_lines[1]
        card2 = card(["the image that runs is Google's"], size=24).move_to([2.3, -2.1, 0])
        tabs = VGroup(*[google_tab().move_to([t.frame.get_left()[0] + 0.5, t.frame.get_top()[1] + 0.04, 0])
                        for t in (P["cpu_tile"], P["gpu_tile"])])
        stays = note("your image · stays on the laptop", INK).move_to([0, -1.75, 0]).align_to([-6.5, 0, 0], LEFT)
        hring = ring(P["cockpit"], S.GREY, buff=0.1)

        with self.voiceover(SAY[4]) as vo:
            vo.wait_until("The job cannot see your laptop")
            self.play(FadeIn(card1, shift=RIGHT * 0.2), run_time=0.8)
            vo.wait_until("its data comes from the internet")
            self.play(FadeIn(net, shift=UP * 0.15), run_time=0.4)
            self.play(GrowArrow(pull), Indicate(url, color=ROUTE, scale_factor=1.04), run_time=0.9)
            vo.wait_until("and anything it should keep")
            self.play(FadeIn(keep, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("And the image is Google's")
            self.play(FadeOut(VGroup(card1, keep, net, pull)), run_time=0.6)
            self.remove(card1, keep, net, pull)
            self.play(FadeIn(card2, shift=UP * 0.15), LaggedStart(*[FadeIn(t, shift=DOWN * 0.15) for t in tabs],
                                                                  lag_ratio=0.3), run_time=0.9)
            vo.wait_until("not yours")
            self.play(Create(hring), FadeIn(stays, shift=UP * 0.15), run_time=0.7)

        # ========================================================== 5. quick predict: who imports TensorFlow?
        outlined = {"nbA": P["nbA"], "nbB": P["nbB"], "laptop": m.laptop_frame, "cockpit": P["cockpit"],
                    "cpu": P["cpu_tile"].frame, "gpu": P["gpu_tile"].frame}
        rings = {k: ring(v, INK, buff=0.1, dashed=True) for k, v in outlined.items() if k not in ("cpu", "gpu")}
        for k, t, tb in (("cpu", P["cpu_tile"], tabs[0]), ("gpu", P["gpu_tile"], tabs[1])):
            rings[k] = ring(VGroup(t.frame, tb), INK, buff=0.05, dashed=True)

        for r in rings.values():
            r.shift(UP * LIFT)

        with self.voiceover(SAY[5]) as vo:
            lift = Group(*[x for x in self.mobjects if x not in (ref, card2, stays, hring)])
            self.play(FadeOut(VGroup(card2, stays, hring)), lift.animate.shift(UP * LIFT), run_time=0.8)
            self.remove(card2, stays, hring)
            vo.wait_until("Your laptop has no GPU")
            self.play(Create(rings["laptop"]), run_time=0.6)
            vo.wait_until("Which machines in this picture")
            self.play(LaggedStart(*[Create(rings[k]) for k in ("nbA", "nbB", "cockpit", "cpu", "gpu")],
                                  lag_ratio=0.2), run_time=1.2)
        qc = low_quick(self, QUICK_TEXT)     # under the lifted map: the ringed machines stay visible

        # ========================================================== 6. the answer
        never = grey_chip("never · proved in scene 9").move_to([0, -1.75, 0]).align_to([-6.5, 0, 0], LEFT)

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(qc), FadeOut(rings["laptop"]), run_time=0.5)
            self.remove(qc, rings["laptop"])
            vo.wait_until("the Colab runtime")
            self.play(rings["nbA"].animate.set_color(OWNED), rings["nbB"].animate.set_color(OWNED), run_time=0.7)
            vo.wait_until("and the container inside each Vertex job")
            self.play(rings["cpu"].animate.set_color(OWNED), rings["gpu"].animate.set_color(OWNED),
                      cpu_c.animate.set_stroke(OWNED, 3), gpu_c.animate.set_stroke(OWNED, 3), run_time=0.7)
            vo.wait_until("Never the cockpit")
            self.play(rings["cockpit"].animate.set_color(S.GREY), FadeIn(never, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("the tarball chapter proves it")
            self.play(Indicate(never.text, color=INK, scale_factor=1.08), run_time=0.8)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
