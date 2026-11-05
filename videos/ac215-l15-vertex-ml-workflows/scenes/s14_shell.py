"""S14 · The workflow container and one processing job (README B › Automate Collector steps 1-3,
slides 32-33 and 36 redrawn, V2 and V7 reprised).

Beats (script.md "## S14", one voiceover block each):
 0  TRACKER B6 (appears, 3 dots) -> step 1. 3-row strip at ~/ml-workflow-aws/src/data-processor:
    `cd ../workflow` (chip "still on your laptop · from data-processor to workflow": S13 ends on the
    laptop, so script.md's "exit the container first" would send a newcomer out of nothing) -> prompt. V2's
    version line (StarVsPin) above, lit ORANGE by `sagemaker = "*"`, chip "before your first sh
    docker-shell.sh here". The lock that never boards: two GREEN file cards (`Pipfile`,
    `Pipfile.lock · 2.250.0`) on the GREY laptop; a TEAL `cheese-app-workflow` image; a PINK ADD
    arrow under laptop/87:3 (`40:ADD --chown=app:app Pipfile /app/`) carries only the Pipfile in;
    the lock bounces off the image wall (RED cross). The PURPLE resolver drops V2's dot at 3.29
    (ORANGE).
 1  TRACKER B6 1 · extra · check. The strip grows to 7 rows: laptop/85 line 1 (bar tag "extra ·
    check") -> TERM(laptop/85: 10) `sagemaker==3.29.0` RED; on "the imports failing" TERM(laptop/86: 9
    cut, 10) `ModuleNotFoundError: No module named 'sagemaker.processing'` RED, row tag "import check
    · on 3.29.0" (the narration's picture; its long command is not typed); laptop/89 line 1 -> TERM(laptop/89: 9334
    from "Pipfile.lock not found") RED. TRACKER B6 1 · extra: laptop/88 line 1 (the sed fix + git
    diff) -> TERM(laptop/88: 10-11), ▶ your turn. V2: GREEN wall at 3.0 + `sagemaker = "<3"`, the dot
    jumps back to 2.257.7.
 2  TRACKER B6 1. V2 leaves; 9-row terminal: `sh docker-shell.sh` -> TERM(laptop/90: 24-27, 29 wrap,
    30) (`(InvalidClientTokenId)` RED), prompt `(app) app@<id>:/app$` (▶ your turn). TRACKER B6 1 ·
    extra: laptop/90 line 32 -> TERM(90: 35, 37 to "aws-cli/2.39.4") (2.257.7 GREEN, "at the time
    of recording"); line 38 -> TERM(90: 44) RED. CODE(src/workflow/docker-shell.sh: 33-34) at 20 pt,
    `/var/run/docker.sock` YELLOW, chip "socket mounted · no docker program inside".
 3  LECTURE 15 · 32-33. The terminal shrinks to a strip. Slide 32 redrawn: GREY "You (Python)" box
    -> PURPLE "SDK" box with a remote-control glyph ("a remote control") -> BLUE "SageMaker" cloud
    with three dim machines. A PINK request dot travels You -> SDK -> cloud; on "AWS machines run"
    the machines light up while the laptop stays still. Tag and picture leave together.
 4  TRACKER B6 2. 8-row terminal: `python cli.py --data_collector` -> TERM(laptop/90: 53, 55, 60
    RED, …, 98-99 wrap RED) (rich borders off). CODE(src/workflow/cli.py: 30-32) at 20 pt, line 32
    barred RED, chip "top of the file · runs at import"; ▶ your turn.
 5  TRACKER B6 2. Terminal leaves. CODE(src/workflow/cli.py: 52-59): `image_uri=DATA_COLLECTOR_IMAGE`
    TEAL, `instance_type="ml.t3.medium"` GOLD, `entrypoint=["python3", "/app/cli.py"]` YELLOW; GOLD
    cost tag "Processing job · ml.t3.medium · while it runs" top right. Then CODE(cli.py: 63-69,
    line 67 cut) + CODE(cli.py: 77-80) side by side: `arguments=[` PINK, `logs=True` / `wait=True`
    YELLOW (lines 70-76, the outputs, are left out: 63-80 is 18 lines, over the 12-line cap).
 6  LECTURE 15 · 36. V7 reprise (CallableImage, built) inside a BLUE dashed "SageMaker · AWS" border:
    production mode lights; a BLUE arrow labelled "SageMaker" plugs `python3 /app/cli.py --search …`
    into the switch; the image pulses; the BLUE CheeseAppSageMakerExecutionRole badge appears; a
    GREY key card from the laptop bounces off the border ("your key stays home").
 7  TRACKER B6 3. CONSOLE("Processing jobs", path "Amazon SageMaker AI › Processing", B:224): Name
    `cheese-app-data-collector-…` (cli.py:61's prefix only), Status a GREY-dashed chip; tag
    illustration. Fade to empty.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S14"]
SIZE = 20                                     # terminal font: 72 characters a row

# ------------------------------------------------------------------ the real sources (checked)
C85, C86, C88, C89, C90 = capture("85"), capture("86"), capture("88"), capture("89"), capture("90")
assert C85.cmd.startswith("docker run --rm --tmpfs /tmp:exec,size=4g") and C85.cmd.endswith("sagemaker boto3")
L85 = C85.at(10)
assert L85 == ["  sagemaker==3.29.0"], L85
assert C89.cmd == "docker build -t cheese-app-workflow --platform=linux/amd64 -f Dockerfile ."
L89 = from_phrase(C89.line(9334), "Pipfile.lock not found")
assert L89 == "…Pipfile.lock not found, creating...", L89
assert C88.cmd == """sed -i 's/^sagemaker = "\\*"/sagemaker = "<3"/' Pipfile && git diff Pipfile"""
L88 = C88.at(10, 11)
assert L88 == ['-sagemaker = "*"', '+sagemaker = "<3"'], L88
assert "sagemaker==3.29.0" in C86.cmd and "sagemaker_import_check.sh" in C86.cmd
L86 = [cut(C86.line(9), "import"), C86.line(10)]
assert L86 == [">>> from sagemaker.processing import…",
               "ModuleNotFoundError: No module named 'sagemaker.processing'"], L86
ADD87 = capture("87").at(3)[0]
assert ADD87 == "40:ADD --chown=app:app Pipfile /app/", ADD87
assert C90.cmd == "sh docker-shell.sh"
L90_BANNER = C90.at(24, 25, 26, 27)
assert L90_BANNER[1] == "AWS Region: us-east-1" and L90_BANNER[2] == "S3 Bucket: cheese-app-ml-workflow-demo"
L90_29 = C90.line(29)
assert "(InvalidClientTokenId)" in L90_29 and L90_29.startswith("aws: [ERROR]")
L90_30 = C90.line(30)
assert L90_30 == "Launching subshell in virtual environment..."
T32, T38, T45 = C90.typed(32), C90.typed(38), C90.typed(45)
assert T32.startswith("python --version; pip list") and T38.startswith("ls /data-collector")
assert T45 == "python cli.py --data_collector"
L90_35 = C90.line(35)
assert L90_35 == "sagemaker                 2.257.7"
L90_37 = cut(C90.line(37), "aws-cli/2.39.4")
assert L90_37.startswith("aws-cli/2.39.4"), L90_37
L90_44 = C90.line(44)
assert L90_44 == "bash: docker: command not found"
L90_53 = C90.line(53)
assert L90_53 == "INFO:botocore.credentials:Found credentials in environment variables."
L90_55 = unbox(C90.line(55)).strip()
assert L90_55 == "/app/cli.py:32 in <module>", L90_55
L90_60 = unbox(C90.line(60)).strip()
assert L90_60 == "❱  32 ACCOUNT_ID = sts_client.get_caller_identity()['Account']", L90_60
L90_98 = C90.at(98, 99)
assert L90_98[0].startswith("ClientError: An error occurred (InvalidClientTokenId)")

CLI = "B/src/workflow/cli.py"
SH = "B/src/workflow/docker-shell.sh"
assert excerpt(CLI, 32, 32) == "ACCOUNT_ID = sts_client.get_caller_identity()['Account']"
assert excerpt(CLI, 61, 61).strip() == 'job_name = f"cheese-app-data-collector-{generate_uuid()}"'
assert "-v /var/run/docker.sock:/var/run/docker.sock" in excerpt(SH, 34, 34)
assert readme(223, "B").startswith("* Run `python cli.py --data_collector`")
assert "Amazon SageMaker AI → Processing → Processing Jobs" in readme(224, "B")
PLUG_CMD = "python3 /app/cli.py --search …"   # cli.py:57 + the first job argument (cli.py:65)


def fixed_tracker(key: str, step=None, extra=False) -> VGroup:
    """common.tracker() with its head put back above the dots (the head's arrange() centres it at
    y 0; the workaround of S01, S03-S13; requested fix in the report)."""
    tr = tracker(key, step, extra)
    tr.head.next_to(tr.dots, UP, buff=0.14, aligned_edge=LEFT)
    place_tracker(tr)
    assert tr.get_bottom()[1] >= TRACK_BOTTOM - 0.05, tr.get_bottom()
    return tr


def two_line_chip(top: str, bottom: str, color=S.GREY) -> VGroup:
    """A chip of two label rows. .box .text"""
    t = VGroup(label(top, 20, INK), label(bottom, 20, INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    b = box(t.width + 0.48, t.height + 0.3, color, fill_opacity=0.16, radius=0.16)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def mono_strip(s: str, color=IMAGE) -> VGroup:
    """A one-line mono strip (capture text) in a thin outlined box. .box .text"""
    t = mono(s, 20, INK)
    b = box(t.width + 0.4, t.height + 0.26, color, fill=S.BG, fill_opacity=0.9, radius=0.1)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def first_resolve(scene, v, ver: str, color, run_time: float = 1.0):
    """PLAYS: StarVsPin.resolve() for the first dot, with the 'resolver' label top-aligned to its
    arrow so it clears the dot's version label (which keep_inside pulls left at 3.29; requested
    fix in the report)."""
    assert v.dot is None
    pt = v.x_of(ver)
    d = Dot(pt, radius=0.13, color=color)
    t = mono(ver, 22, color).next_to(d, UP, buff=0.42)
    keep_inside(t)
    arr = Arrow(pt + UP * 1.5, pt + UP * 0.2, buff=0, color=TOOL, stroke_width=4, tip_length=0.18)
    rl = label("resolver", 20, TOOL).next_to(arr, LEFT, buff=0.1, aligned_edge=UP)
    assert rl.get_bottom()[1] > t.get_top()[1] + 0.05, (rl.get_bottom(), t.get_top())
    v.show(scene, arr, rl, anims=[GrowArrow(arr), FadeIn(rl)], run_time=run_time * 0.5)
    g = VGroup(d, t)
    v.show(scene, g, anims=[FadeIn(d, scale=0.5), FadeIn(t)], run_time=run_time * 0.5)
    v.drop(scene, arr, rl, run_time=0.3)
    v.dot = g
    return g


def remote_glyph(h: float = 0.75, color=TOOL) -> VGroup:
    """A text-free remote control: a rounded body, a big button, two small ones, and signal arcs."""
    body = RoundedRectangle(width=h * 0.48, height=h, corner_radius=h * 0.12, stroke_color=color,
                            stroke_width=3).set_fill(color, 0.2)
    big = Circle(radius=h * 0.1, stroke_width=0).set_fill(color, 1).move_to(body.get_top() + DOWN * h * 0.24)
    small = VGroup(*[Dot(radius=h * 0.045, color=color) for _ in range(4)]).arrange_in_grid(2, 2, buff=h * 0.09)
    small.move_to(body.get_center() + DOWN * h * 0.15)
    arcs = VGroup(*[Arc(radius=r, start_angle=PI / 4, angle=PI / 2, color=color, stroke_width=3)
                    for r in (h * 0.16, h * 0.3)])
    for a in arcs:
        a.move_arc_center_to(body.get_top() + UP * 0.02)
    return VGroup(body, big, small, arcs)


class WorkflowShell(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S14"] == 8, len(SAY)
        self.bar_tags = []
        self.t = None

        # ========================================================== 0. the lock that never boards
        tr = fixed_tracker("B6")
        t = term(P_SRC("data-processor"), rows=3, size=SIZE)
        self.t = t
        exit_c = grey_chip("still on your laptop · from data-processor to workflow")
        under_term(t, exit_c)

        v = StarVsPin().shift(UP * 0.3)
        before_c = grey_chip("before your first sh docker-shell.sh here")
        before_c.move_to([-3.0 + before_c.width / 2, v.p(0, 2.3)[1], 0])
        assert before_c.get_right()[0] < 5.6 and before_c.get_top()[1] < TRACK_BOTTOM, before_c.get_top()

        y_band = -0.6
        lap_box = outline_box(4.9, 1.5, LAPTOP, solid=True, fill_opacity=0.06).move_to([-4.0, y_band, 0])
        lap_cap = label("your laptop", 20, S.GREY).next_to(lap_box, UP, buff=0.1).align_to(lap_box, LEFT)
        pf = file_card("Pipfile", OWN)
        lock = file_card("Pipfile.lock · 2.250.0", OWN)
        VGroup(pf, lock).arrange(DOWN, buff=0.14, aligned_edge=LEFT).move_to(lap_box)
        img = image_block(None, box_w=4.75, box_h=1.5).move_to([4.05, y_band, 0])
        img_name = mono("cheese-app-workflow", 20, INK).move_to(img.block.get_top() + DOWN * 0.3)
        add_s = mono_strip(ADD87)
        add_s.move_to([1.0, lap_cap.get_center()[1], 0])
        wall_x = img.block.get_left()[0]
        add_r = route(np.array([lap_box.get_right()[0] + 0.08, pf.get_center()[1], 0]),
                      np.array([wall_x - 0.05, pf.get_center()[1], 0]))
        assert add_s.get_left()[0] > lap_cap.get_right()[0] + 0.2 and add_s.get_right()[0] < 6.5, add_s.get_right()
        assert add_s.get_top()[1] < v.ticks.get_bottom()[1] - 0.05, (add_s.get_top(), v.ticks.get_bottom())
        assert lap_box.get_bottom()[1] > t.box.get_top()[1] + 0.1 and img.get_right()[0] < 6.5, lap_box.get_bottom()
        assert lock.get_right()[0] < lap_box.get_right()[0] - 0.05, lock.get_right()
        pf_dest = [wall_x + 0.4 + pf.width / 2, img.block.get_center()[1] - 0.2, 0]
        lock_hit = [wall_x - 0.08 - lock.width / 2, lock.get_center()[1], 0]
        xmark = cross_glyph(0.3).move_to([wall_x, lock.get_center()[1], 0])
        band = VGroup(lap_box, lap_cap, pf, lock, img, img_name, add_s, add_r)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.2), FadeIn(t), run_time=0.6)
            self.play(track(tr, 1), run_time=0.5)
            self.play(FadeIn(exit_c, shift=DOWN * 0.1), run_time=0.3)
            type_cmd(self, t, "cd ../workflow", type_time=0.5)
            cd_prompt(self, t, P_SRC("workflow"), run_time=0.4)
            self.play(FadeOut(exit_c), run_time=0.3)
            vo.wait_until("Before you run")
            self.play(FadeIn(v), run_time=0.6)
            v.star(self, run_time=0.7)
            self.play(FadeIn(before_c, shift=DOWN * 0.1), run_time=0.4)
            self.play(Indicate(v.star_label, color=SHARED, scale_factor=1.1), run_time=0.6)
            v.heal(self)
            vo.wait_until("A lock is committed")
            self.play(FadeIn(lap_box), FadeIn(lap_cap), FadeIn(pf, shift=UP * 0.1), FadeIn(lock, shift=UP * 0.1),
                      run_time=0.6)
            self.play(Indicate(lock.text, color=OWN, scale_factor=1.06), run_time=0.6)
            vo.wait_until("but the Dockerfile copies")
            self.play(FadeIn(img), FadeIn(img_name), FadeIn(add_s, shift=DOWN * 0.1), run_time=0.6)
            self.play(GrowArrow(add_r), run_time=0.4)
            self.play(pf.animate.move_to(pf_dest), run_time=0.9)
            self.play(bounce(lock, lock_hit, run_time=0.9), FadeIn(xmark, scale=0.5, run_time=0.6))
            vo.wait_until("so the build would resolve")
            self.play(Indicate(pf.text, color=OWN, scale_factor=1.08), run_time=0.5)
            first_resolve(self, v, "3.29.0", color=SHARED, run_time=1.2)
            self.play(Indicate(v.dot, color=SHARED, scale_factor=1.25), run_time=0.6)
            v.heal(self)

        # ========================================================== 1. the checks · the same fix
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(band), FadeOut(xmark), FadeOut(before_c), track(tr, 1, "check"), run_time=0.5)
            self.resize(7, keep=1, run_time=0.5)              # block 1 is tight: imports, then the fix
            assert t.box.get_top()[1] < v.ticks.get_bottom()[1] - 0.1, (t.box.get_top(), v.ticks.get_bottom())
            self.bar(on_bar(t, extra_row("check")))
            type_cmd(self, t, C85.cmd, type_time=0.6)
            out(self, t, [(L85[0], ERR)], run_time=0.3)
            self.reseat()
            vo.wait_until("the imports failing")
            r86 = out(self, t, [L86[0], (L86[1], ERR)], run_time=0.3)    # laptop/86: 9-10, its long command untyped
            pin(self, r86[0], beside(row_tag("import check · on 3.29.0"), r86[0]), run_time=0.3)
            self.reseat()
            type_cmd(self, t, C89.cmd, type_time=0.4)
            out(self, t, [(L89, ERR)], run_time=0.3)
            self.reseat()
            vo.wait_until("So make the same fix")
            self.play(track(tr, 1, True), *self.unbar_anims(), run_time=0.4)
            self.bar(on_bar(t, extra_row()))
            ln = type_cmd(self, t, C88.cmd, type_time=0.7)
            out(self, t, [(L88[0], SHARED), (L88[1], OWN)], run_time=0.5)
            self.bar(on_bar(t, turn_row()))
            v.pin(self, run_time=1.6)
            self.play(Indicate(v.pin_label, color=OWN, scale_factor=1.1), run_time=0.6)
            v.heal(self)
            self.play(Indicate(v.dot, color=OWN, scale_factor=1.25), run_time=0.7)
            v.heal(self)
            self.wait(0.6)
            self.reseat()

        # ========================================================== 2. sh docker-shell.sh · extras
        sh_p = code(SH, 33, 34, font_size=20)
        sh_p.move_to([-6.45 + sh_p.width / 2, 2.72 - sh_p.height / 2, 0])
        sock_c = two_line_chip("socket mounted ·", "no docker program inside")
        sock_c.next_to(sh_p, RIGHT, buff=0.3).align_to(sh_p, DOWN)
        assert sock_c.get_right()[0] < 6.5, sock_c.get_right()

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(v), *self.unbar_anims(), track(tr, 1), run_time=0.5)
            self.reseat()
            self.wipe()
            self.resize(9, keep=0)
            assert t.box.get_top()[1] < sh_p.get_bottom()[1] - 0.15, (t.box.get_top(), sh_p.get_bottom())
            type_cmd(self, t, C90.cmd, type_time=0.5)
            self.bar(on_bar(t, turn_row()))
            vo.wait_until("The banner shows")
            rb = out(self, t, L90_BANNER, run_time=0.5)
            self.play(each([rb[1], rb[2]], TURN, 1.05), run_time=0.7)
            self.reseat()
            vo.wait_until("and the who am I check fails")
            r29 = out(self, t, [(L90_29, ERR), L90_30], wrap=True, run_time=0.5)
            hit = [r for r in r29 if "(InvalidClientTokenId)" in r.text][0]
            self.play(Indicate(substring(hit, "(InvalidClientTokenId)"), color=ERR, scale_factor=1.1), run_time=0.6)
            self.reseat()
            cd_prompt(self, t, P_APP, color=IMAGE, run_time=0.4)
            vo.wait_until("Extras:")
            self.play(track(tr, 1, True), run_time=0.4)
            self.bar(on_bar(t, extra_row()))
            type_cmd(self, t, T32, type_time=0.6)
            r35 = out(self, t, [(L90_35, OWN), L90_37], run_time=0.4)
            pin(self, r35[1], beside(time_row(), r35[1]))
            self.play(Indicate(substring(r35[0], "2.257.7"), color=OWN, scale_factor=1.15), run_time=0.6)
            self.reseat()
            vo.wait_until("and no docker command")
            type_cmd(self, t, T38, type_time=0.5)
            r44 = out(self, t, [(L90_44, ERR)], run_time=0.4)
            self.play(Indicate(r44[0], color=ERR, scale_factor=1.06), run_time=0.6)
            self.reseat()
            vo.wait_until("The socket is mounted")
            self.play(FadeIn(sh_p, shift=DOWN * 0.2), run_time=0.5)
            self.play(code_span(sh_p.code, 1, "/var/run/docker.sock").animate.set_color(TURN), run_time=0.4)
            self.add(sh_p)
            self.play(FadeIn(sock_c, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("but no docker program")
            self.play(Indicate(sock_c.text[1], color=ERR, scale_factor=1.06),
                      Indicate(r44[0], color=ERR, scale_factor=1.04), run_time=0.8)
            self.reseat()

        # ========================================================== 3. slide 32: the remote control
        lt = lref("32–33")
        you_b = outline_box(2.9, 1.5, LAPTOP, solid=True, fill_opacity=0.08).move_to([-4.6, 0.9, 0])
        you_t = VGroup(you(None, h=0.55), label("You (Python)", 22, INK)).arrange(DOWN, buff=0.12).move_to(you_b)
        sdk_b = outline_box(2.4, 1.5, TOOL, solid=True, fill_opacity=0.12).move_to([-0.7, 0.9, 0])
        sdk_t = VGroup(remote_glyph(0.7), label("SDK", 22, INK)).arrange(RIGHT, buff=0.3).move_to(sdk_b)
        rc_cap = label("a remote control", 20, TOOL).next_to(sdk_b, DOWN, buff=0.15)
        cl = cloud_shape(None, cloud_w=4.4).move_to([3.95, 1.0, 0])
        cl_t = label("SageMaker", 22, INK).move_to(cl.get_center() + UP * 0.45)
        racks = VGroup(*[rack(0.55) for _ in range(3)]).arrange(RIGHT, buff=0.3).move_to(cl.get_center() + DOWN * 0.3)
        racks.set_opacity(0.25)
        a1 = arrow(you_b.get_right(), sdk_b.get_left(), S.GREY)
        a2 = arrow(sdk_b.get_right(), cl.get_left() + RIGHT * 0.1, TOOL)
        pic = VGroup(you_b, you_t, sdk_b, sdk_t, rc_cap, cl, cl_t, racks, a1, a2)
        assert cl.get_right()[0] < 6.5 and pic.get_top()[1] < 2.8 and lt.get_bottom()[1] > cl.get_top()[1] + 0.1, \
            (cl.get_right(), pic.get_top(), lt.get_bottom())

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(sh_p), FadeOut(sock_c), *self.unbar_anims(), run_time=0.4)
            self.resize(3, keep=1)
            assert pic.get_bottom()[1] > t.box.get_top()[1] + 0.1, (pic.get_bottom(), t.box.get_top())
            self.play(FadeIn(lt), FadeIn(you_b), FadeIn(you_t), run_time=0.5)
            self.play(GrowArrow(a1), FadeIn(sdk_b), FadeIn(sdk_t), run_time=0.6)
            vo.wait_until("is your remote control")
            self.play(FadeIn(rc_cap, shift=UP * 0.1), Indicate(sdk_t[0], color=TOOL, scale_factor=1.2), run_time=0.7)
            self.play(GrowArrow(a2), FadeIn(cl), FadeIn(cl_t), FadeIn(racks), run_time=0.7)
            vo.wait_until("Your Python asks")
            d = pulse_dot().move_to(you_b.get_right())
            self.add(d)
            self.play(d.animate.move_to(sdk_b.get_center()), run_time=0.6)
            self.play(d.animate.move_to(cl.get_center()), run_time=0.6)
            vo.wait_until("and AWS machines run")
            self.play(FadeOut(d), racks.animate.set_opacity(1), run_time=0.5)
            self.play(LaggedStart(*[Indicate(r, color=CLOUD, scale_factor=1.12) for r in racks], lag_ratio=0.25),
                      run_time=1.0)
            self.play(Indicate(cl_t, color=CLOUD, scale_factor=1.06), run_time=0.6)

        # ========================================================== 4. step 2: stops at import
        cp = code(CLI, 30, 32, font_size=20)
        cp.move_to([-6.45 + cp.width / 2, 2.72 - cp.height / 2, 0])
        top_c = two_line_chip("top of the file ·", "runs at import")
        top_c.next_to(cp, RIGHT, buff=0.3).align_to(cp, DOWN)
        assert top_c.get_right()[0] < 6.5, top_c.get_right()

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(pic), FadeOut(lt), track(tr, 2), run_time=0.5)
            self.resize(8, keep=1)
            assert t.box.get_top()[1] < cp.get_bottom()[1] - 0.15, (t.box.get_top(), cp.get_bottom())
            ln = type_cmd(self, t, T45, type_time=0.6)
            pin(self, ln, beside(turn_row(), ln))
            vo.wait_until("It stops at line 32")
            r = out(self, t, [L90_53, L90_55, (L90_60, ERR), "…"] + [(s, ERR) for s in L90_98], wrap=True,
                    run_time=0.7)
            self.play(Indicate(substring(r[1], "cli.py:32"), color=TURN, scale_factor=1.15), run_time=0.6)
            self.reseat()
            vo.wait_until("a lookup of your account")
            self.play(FadeIn(cp, shift=DOWN * 0.2), run_time=0.5)
            bar32 = line_bar(cp.code, 2, ERR, 0.25)
            self.play(FadeIn(bar32), run_time=0.4)
            self.play(Indicate(substring(r[2], "get_caller_identity()"), color=ERR, scale_factor=1.08), run_time=0.6)
            self.reseat()
            vo.wait_until("before the function even starts")
            self.play(FadeIn(top_c, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("Every flag")
            self.play(Indicate(top_c.text[1], color=TURN, scale_factor=1.08), run_time=0.7)
            self.play(Indicate(cp.code, color=ERR, scale_factor=1.02), run_time=0.7)
            self.add(cp, bar32)                    # (re-seating cp alone hid the RED bar under its fill)

        # ========================================================== 5. with keys: the processor
        cost = cost_tag("Processing job · ml.t3.medium · while it runs")
        cost.move_to([6.45 - cost.width / 2, 2.5, 0])
        pa = code(CLI, 52, 59, font_size=20)
        pa.move_to([0, 0.15, 0])                  # centred: the frame's lower half was empty
        pb = code(CLI, 63, 69, font_size=20, cuts={67: '"brie cheese",'})
        pc = code(CLI, 77, 80, font_size=20)
        pc.next_to(pb, RIGHT, buff=0.35).align_to(pb, UP)
        VGroup(pb, pc).move_to([0, 0.15, 0])
        assert pa.get_bottom()[1] > -3.55 and pc.get_right()[0] < 6.5 and pb.get_bottom()[1] > -3.55, \
            (pa.get_bottom(), pc.get_right(), pb.get_bottom())
        assert cost.get_left()[0] > tr.get_right()[0] + 0.2 and cost.get_bottom()[1] > pa.get_top()[1] + 0.05, \
            (cost.get_left(), tr.get_right(), cost.get_bottom(), pa.get_top())

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(cp), FadeOut(bar32), FadeOut(top_c), FadeOut(t), *self.unbar_anims(), run_time=0.5)
            self.remove(t)
            self.t = None
            self.play(FadeIn(pa, shift=DOWN * 0.2), run_time=0.6)
            vo.wait_until("from your ECR image")
            self.paint(pa, 1, "image_uri=DATA_COLLECTOR_IMAGE", IMAGE)
            vo.wait_until("on one M L T3 medium")
            self.paint(pa, 3, 'instance_type="ml.t3.medium"', COST)
            self.play(FadeIn(cost, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("Its entry point")
            self.paint(pa, 5, 'entrypoint=["python3", "/app/cli.py"]', TURN)
            self.play(Indicate(code_span(pa.code, 5, '"/app/cli.py"'), color=TURN, scale_factor=1.08), run_time=0.6)
            self.add(pa)
            vo.wait_until("Then it runs the job")
            self.play(FadeOut(pa), run_time=0.4)
            self.play(FadeIn(pb, shift=DOWN * 0.2), FadeIn(pc, shift=DOWN * 0.2), run_time=0.6)
            self.paint(pb, 1, "arguments=[", ROUTE)
            self.play(Indicate(code_span(pb.code, 2, '"--search"'), color=ROUTE, scale_factor=1.1), run_time=0.6)
            self.add(pb)
            vo.wait_until("and waits")
            self.paint(pc, 2, "wait=True", TURN)
            vo.wait_until("showing the logs")
            self.paint(pc, 1, "logs=True", TURN)
            flash_tag(self, cost)

        # ========================================================== 6. V7 reprise: production mode
        lt36 = lref("36")
        ci = CallableImage(built=True)
        dy = 0.35
        ci.shift(UP * dy)
        ci.pivot = ci.image.frame.get_left() + RIGHT * 0.05      # (the piece stores it at build time)
        border = DashedVMobject(RoundedRectangle(width=13.16, height=4.55, corner_radius=0.2), num_dashes=90)
        border.set_stroke(CLOUD, 2.5).move_to([0, 0.05, 0])
        b_cap = label("SageMaker · AWS", 20, CLOUD)
        b_cap.move_to([border.get_left()[0] + 0.25 + b_cap.width / 2, border.get_top()[1] - 0.25, 0])
        kc = key_card("access key")
        kc.move_to([-5.0, -3.1, 0])
        home_c = grey_chip("your key stays home")
        home_c.next_to(kc, RIGHT, buff=0.3)
        assert border.get_top()[1] < TRACK_BOTTOM and kc.get_bottom()[1] > -3.6, (border.get_top(), kc.get_bottom())

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(pb, pc)), FadeOut(cost), run_time=0.4)
            self.play(FadeIn(lt36), FadeIn(ci), Create(border), FadeIn(b_cap), run_time=0.8)
            assert ci.image.get_top()[1] < b_cap.get_bottom()[1] - 0.2, (ci.image.get_top(), b_cap.get_bottom())
            ci.choose(self, "prod")
            vo.wait_until("SageMaker puts its own command")
            ci.plug(self, PLUG_CMD, by="SageMaker", run_time=1.6)
            self.play(Indicate(ci.cmd_chip[0], color=CLOUD, scale_factor=1.06), run_time=0.6)
            ci.heal(self)
            assert border.get_bottom()[1] < ci.get_bottom()[1] - 0.05, (border.get_bottom(), ci.get_bottom())
            vo.wait_until("Same image, same cli.py")
            self.play(Indicate(ci.image.frame, color=IMAGE, scale_factor=1.04), run_time=0.8)
            ci.heal(self)
            vo.wait_until("on a machine you never log in to")
            self.play(Indicate(ci.cards["prod"].rows, color=CLOUD, scale_factor=1.05), run_time=0.7)
            ci.heal(self)
            vo.wait_until("The job acts as the role")
            bdg = role_badge(ROLE_SM).next_to(ci.cards["prod"].frame, DOWN, buff=0.15)
            bdg.shift(RIGHT * (border.get_right()[0] - 0.2 - bdg.get_right()[0]))   # (CallableImage.badge
            ci.show(self, bdg, anims=[GrowFromCenter(bdg)], run_time=0.6)          #  touches the border)
            ci.badge_g = bdg
            assert border.get_bottom()[1] < bdg.get_bottom()[1] - 0.05, bdg.get_bottom()
            assert bdg.get_left()[0] > ci.cmd_chip.get_right()[0] + 0.2, (bdg.get_left(), ci.cmd_chip.get_right())
            vo.wait_until("not with your key")
            self.play(FadeIn(kc, shift=UP * 0.2), run_time=0.4)
            self.play(bounce(kc, [kc.get_center()[0], border.get_bottom()[1] - 0.05 - kc.height / 2, 0], run_time=0.9))
            self.play(FadeIn(home_c, shift=LEFT * 0.1), run_time=0.4)
            self.play(Indicate(home_c.text, color=INK, scale_factor=1.05), run_time=0.6)

        # ========================================================== 7. step 3: the console
        form = console_form("Processing jobs", [("Name", "cheese-app-data-collector-…"), ("Status", "")],
                            form_w=9.0, path="Amazon SageMaker AI › Processing")
        form.move_to([0, 0.2, 0])
        form.rows[1].field.set_opacity(0)          # the status is a dashed chip: only your account shows it
        st = dashed_chip("on your account")
        st.move_to(form.rows[1].field).align_to(form.rows[1].field, LEFT)
        ill = illustration_tag()
        ill.next_to(form, DOWN, buff=0.2).align_to(form, RIGHT)
        assert form.get_top()[1] < TRACK_BOTTOM - 0.1 and ill.get_bottom()[1] > -3.55, form.get_top()

        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(ci, border, b_cap, kc, home_c)), FadeOut(lt36), track(tr, 3), run_time=0.6)
            self.play(FadeIn(form, shift=UP * 0.2), FadeIn(ill), run_time=0.6)
            vo.wait_until("then Processing jobs")
            self.play(Indicate(form.title_text, color=TURN, scale_factor=1.08), run_time=0.6)
            self.play(FadeIn(st, scale=0.9), Indicate(form.rows[0].value, color=CLOUD, scale_factor=1.04),
                      run_time=0.7)
            self.wait(1.0)

        self.play(FadeOut(VGroup(form, st, ill, tr)), run_time=0.8)
        self.wait(0.3)

    # ------------------------------------------------------------------ helpers
    def paint(self, panel, k: int, sub: str, color, run_time: float = 0.5):
        """PLAYS: colour `sub` on code line k of `panel` and re-seat the panel (split trap)."""
        self.play(code_span(panel.code, k, sub).animate.set_color(color), run_time=run_time)
        self.add(panel)

    def bar(self, tg):
        """Show a title-bar tag (on_bar; left of the tags already there) and remember it, so it
        fades with the terminal."""
        if self.bar_tags:
            tg.next_to(self.bar_tags[-1], LEFT, buff=0.15)
        self.play(FadeIn(tg), run_time=0.3)
        self.bar_tags.append(tg)

    def unbar_anims(self):
        tgs, self.bar_tags = self.bar_tags, []
        return [FadeOut(tg) for tg in tgs]

    def resize(self, rows: int, keep=None, run_time: float = 0.8):
        """common.resize() with the title-bar tags riding along."""
        dy = (rows - self.t.rows) * self.t.pitch
        resize(self, self.t, rows, keep=keep, extra=[tg.animate.shift(UP * dy) for tg in self.bar_tags],
               run_time=run_time)

    def wipe(self, *extra, run_time: float = 0.4):
        """PLAYS: the terminal's rows fade out (with `extra` alongside) and leave it for good."""
        t = self.t
        gone = list(t.lines.submobjects)
        for m in gone:
            t.lines.remove(m)
        if gone or extra:
            self.play(*[FadeOut(m) for m in gone], *extra, run_time=run_time)
        self.remove(*gone)
        self.reseat()

    def reseat(self):
        """Re-seat the terminal as one mobject (split trap) and keep its bar tags on top."""
        if self.t is not None:
            self.add(self.t, *self.bar_tags)
