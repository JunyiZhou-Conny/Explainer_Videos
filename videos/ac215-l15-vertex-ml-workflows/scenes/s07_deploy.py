"""S07 · --deploy: model, endpoint configuration, endpoint (README A › Prepare, deploy, predict,
step 2; the V5 ThreeObjects set piece built; LECTURE 15 · 11–12, 12, then 16–17).

Beats (script.md "## S07", one voiceover block each):
 0  TRACKER A3 2 fades in; lecture tag "Lecture 15 · slides 11–12" top right. V5's three slots of
    S01 come back (artifact, container, machine) and flash on "Remember the three pieces".
    CODE(cli.py: 151–154) at 22 pt under them; the machine slot dims. On "describes" the artifact
    and container slots Transform into the GREY-dashed TensorFlowModel card; line 152 lights PINK
    with the S3 URI, line 154 TEAL with "TF Serving 2.13", line 153 BLUE as the role badge drops
    in. GREY caption "a description in Python · nothing in AWS yet".
 1  Panel and caption go; the lecture tag becomes "slide 12"; V5 moves down (never scaled). The
    GREY-dashed "Model Registry (the lecture)" box above the card with its arrow; `erratum` beside
    it; GREY chip "README: 'Model Registry' · code: a plain Model" under the card; the S02
    mini-legend chip "Model Registry → SageMaker Model" lower right.
 2  Registry, chips and lecture tag go. A TEAL ring on the container slot and a TEAL callout under
    it: "AWS prebuilt TensorFlow Serving image · picked from framework_version" (no URI). Chips
    TEAL "served by 2.13" and GREEN "exported by TF 2.18" + "at the time of recording"; on
    "In step 3" a GREY-dashed arrow to "checked locally in step 3".
 3  Callout goes, V5 moves back up. CODE(cli.py: 164–171) at 20 pt (164 and 166 cut): 169–170 GOLD
    on "with one instance", 164–167 YELLOW on "a name with a timestamp"; line 168's `deploy(` lights
    on "That one call creates all three". The dashed card turns into the solid BLUE Model card; the
    machine slot Transforms into the endpoint configuration card (AllTraffic · ml.m5.xlarge ·
    count 1 · weight 1) and the endpoint plate `…-endpoint-<timestamp>` with its machine and dial;
    GREY chip "shape from the part 2 Lambda".
 4  V5 and the panel go (the terminal needs the frame). 8-row terminal at (app) app@<id>:/app$:
    `python cli.py --deploy` (▶ your turn) -> TERM(laptop/28: 52, 58, …, 78, 83, …, 308); 83 and
    308 RED. GREY card above: "with your keys · 5–10 min (README A:127)" / "the endpoint name ·
    endpoint_config.json written · no output shown"; GREY chip "fails? the endpoint's CloudWatch
    logs · the tarball in S3 · README A:186–188".
 5  Terminal goes; V5 returns. BLUE "serverless = no server to manage"; the rack flashes and the
    GOLD dial sweeps; GOLD cost tag "endpoint · ml.m5.xlarge · 24/7 while it exists"; the PINK
    request lane with "0 requests" while the dial keeps sweeping; GREY-dashed "Cloud Run · lecture 14"
    card whose dashed instance blinks off ("scales to zero"); RED-struck "scale to zero".
 6  Everything goes. LECTURE 15 · 16–17: the two-column card: BLUE "managed model serving ·
    SageMaker endpoint · Vertex AI online prediction" with "deploy a model directly",
    "versioning", "A/B variants", "monitoring" writing in on their phrases; GREY-dashed "run any
    container · Cloud Run (L14)" with "you containerize", "you configure", "you add monitoring".
 7  LECTURE (held). The rule of thumb writes under the card; on "Here" a small endpoint plate
    slides in under the left column and three GREY chips "1 instance", "1 variant", "no
    monitoring" fly from the features onto it, captioned "available · not used here". Fade to an
    empty frame.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S07"]

# ------------------------------------------------------------------ the real sources (checked)
C28 = capture("28")
CMD28 = C28.typed(35)
assert CMD28 == "python cli.py --deploy", CMD28
OUT28 = [C28.line(52), C28.line(58), "…", unbox(C28.line(78)), unbox(C28.line(83)), "…", C28.line(308)]
assert OUT28[0] == "Deploy model" and OUT28[1] == "Deploying model to SageMaker endpoint...", OUT28
assert OUT28[3] == "/app/cli.py:168 in deploy", OUT28[3]
assert OUT28[4].startswith("❱ 168") and "tensorflow_model.deploy(" in OUT28[4], OUT28[4]
assert OUT28[6] == "NoCredentialsError: Unable to locate credentials", OUT28[6]

assert "typically 5-10 minutes" in readme(127, "A")
assert "Endpoint Creation Fails" in readme(186, "A") and "model.tar.gz was uploaded" in readme(187, "A")
assert "CloudWatch logs" in readme(188, "A")
assert 'framework_version="2.13"' in excerpt("A/cli.py", 154, 154)
assert 'instance_type="ml.m5.xlarge"' in excerpt("A/cli.py", 170, 170)
assert "tensorflow_model.deploy(" in excerpt("A/cli.py", 168, 168)
CUTS3 = {164: "datetime.utcnow()", 166: '.replace(".", "-")'}

S_TOP = 0.45        # V5 shift: card top at 2.78, room under it for a panel or the lane (blocks 0, 3, 5)
S_LOW = -0.45       # V5 shift with the registry box above the card (blocks 1-2)
SIZE = 20           # terminal font: 72 characters a row


def fixed_tracker(key: str, step: int, extra=False) -> VGroup:
    """common.tracker() with its head put back above the dots (common.py's head arrange() centres
    it at y 0; the workaround of S01, S03-S06; requested fix in the report)."""
    tr = tracker(key, step, extra)
    tr.head.next_to(tr.dots, UP, buff=0.14, aligned_edge=LEFT)
    place_tracker(tr)
    assert tr.get_bottom()[1] >= TRACK_BOTTOM - 0.05, tr.get_bottom()
    return tr


def faded(m, k: float):
    """A copy of `m` with every member's own fill and stroke opacity scaled by k (Transform target)."""
    c = m.copy()
    for a, b in zip(c.family_members_with_points(), m.family_members_with_points()):
        a.set_fill(opacity=b.get_fill_opacity() * k).set_stroke(opacity=b.get_stroke_opacity() * k)
    return c


def block(c, a: int, b: int, color, opacity: float) -> Rectangle:
    """A translucent bar over lines a..b (0-based) of a code block."""
    top = c.code_lines[a].get_top()[1] + 0.07
    bot = c.code_lines[b].get_bottom()[1] - 0.07
    bg = c.background
    return Rectangle(width=bg.width - 0.12, height=top - bot, stroke_width=0) \
        .set_fill(color, opacity).move_to([bg.get_center()[0], (top + bot) / 2, 0])


def column(head: str, subs, items, color, dashed: bool, col_w: float = 6.15, col_h: float = 3.7):
    """One column of the slides 16–17 comparison card (subs: GREY lines under the head).
    .frame .head .sub .rows"""
    hd = label(head, 26, color)
    sb = VGroup(*[label(x, 20, S.GREY) for x in subs]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    rows = VGroup(*[label("· " + x, 24, INK) for x in items]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    inner = VGroup(hd, sb, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    assert inner.width < col_w - 0.5 and inner.height < col_h - 0.4, (inner.width, inner.height)
    fr = outline_box(col_w, col_h, color, solid=not dashed, fill_opacity=0.06)
    inner.move_to(fr).align_to(fr, LEFT).align_to(fr, UP).shift(RIGHT * 0.3 + DOWN * 0.25)
    g = VGroup(fr, hd, sb, rows)
    g.frame, g.head, g.sub, g.rows = fr, hd, sb, rows
    return g


class ModelToEndpoint(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S07"] == 8, len(SAY)

        # ========================================================== 0. describe a TensorFlowModel
        tr = fixed_tracker("A3", 2)
        lt = lref("11–12")
        v = ThreeObjects(slots=False)
        v.shift(UP * S_TOP)
        p0 = code("A/cli.py", 151, 154, font_size=22)
        p0.move_to([-6.45 + p0.width / 2, -0.4 - p0.height / 2, 0])
        c0 = p0.code
        bars0 = {k: line_bar(c0, k, col, 0.28) for k, col in ((1, ROUTE), (2, ROLE), (3, IMAGE))}
        cap0 = label("a description in Python · nothing in AWS yet", 22, S.GREY)
        cap0.next_to(p0, DOWN, buff=0.28).align_to(p0, LEFT)
        assert cap0.get_bottom()[1] > -3.55, cap0.get_bottom()

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.2), run_time=0.6)
            self.play(Indicate(tr.caption, color=TURN, scale_factor=1.06), run_time=0.6)
            vo.wait_until("Remember the three pieces")
            v.slots(self, run_time=0.7)
            assert v.slot_list[0].get_top()[1] < PIC_TOP, v.slot_list[0].get_top()
            self.play(each(v.slot_list, TURN, scale=1.05, lag=0.3), FadeIn(lt), run_time=1.2)
            v.heal(self)
            vo.wait_until("In code, it first describes")
            self.play(FadeIn(p0, shift=UP * 0.2), Transform(v.slot_list[2], faded(v.slot_list[2], 0.4)),
                      Transform(v.slot_caps[2], faded(v.slot_caps[2], 0.4)), run_time=0.6)
            v.heal(self)
            v.model_card(self, run_time=1.2)
            assert v.card.get_top()[1] < PIC_TOP + 0.01 and v.card.get_bottom()[1] > p0.get_top()[1] + 0.05, \
                (v.card.get_top(), v.card.get_bottom(), p0.get_top())
            vo.wait_until("the tarball in S3")
            self.play(FadeIn(bars0[1]), Indicate(v.sub["artifact"][2], color=ROUTE, scale_factor=1.1),
                      run_time=0.7)
            v.heal(self)
            vo.wait_until("and the serving container")
            self.play(FadeIn(bars0[3]), Indicate(v.sub["container"][2], color=IMAGE, scale_factor=1.1),
                      run_time=0.7)
            v.heal(self)
            vo.wait_until("plus the role")
            self.play(FadeIn(bars0[2]), run_time=0.3)
            v.fill_role(self, run_time=0.7)
            vo.wait_until("Nothing exists in AWS yet")
            self.play(FadeIn(cap0, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(v.card.title, color=S.GREY, scale_factor=1.08), run_time=0.8)
            v.heal(self)

        # ========================================================== 1. the lecture's Model Registry
        lt12 = lref("12")
        err1 = erratum_tag()
        rd1 = grey_chip("README: 'Model Registry' · code: a plain Model")
        br1 = bridge_chip(2)
        br1.move_to([6.5 - br1.width / 2, -3.5 + br1.height / 2, 0])

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(p0), FadeOut(cap0), *[FadeOut(b) for b in bars0.values()], FadeOut(lt),
                      FadeIn(lt12), v.animate.shift(DOWN * (S_TOP - S_LOW)), run_time=0.8)
            vo.wait_until("The lecture uploads to a model registry")
            v.registry(self, run_time=0.7)
            rg = v.registry_g
            assert rg.get_top()[1] < PIC_TOP + 0.05 and rg.get_left()[0] > tr.get_right()[0] - 9, rg.get_top()
            err1.next_to(rg[0], RIGHT, buff=0.3)
            rd1.next_to(v.card.frame, DOWN, buff=0.25).align_to(v.card.frame, LEFT)
            assert err1.get_right()[0] < lt12.get_left()[0] or err1.get_top()[1] < lt12.get_bottom()[1], \
                (err1.get_right(), lt12.get_left())
            self.play(Indicate(rg[1], color=S.GREY, scale_factor=1.06), run_time=0.7)
            v.heal(self)
            vo.wait_until("Both READMEs say model registry too")
            self.play(FadeIn(rd1, shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(err1, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("but the code creates a plain model")
            self.play(FadeIn(br1, shift=UP * 0.1),
                      Indicate(v.card.title, color=INK, scale_factor=1.1), run_time=0.8)
            v.heal(self)
            flash_tag(self, rd1, color=INK)

        # ========================================================== 2. the serving image, by version
        cont = v.sub["container"]
        rg2 = ring(cont[0], IMAGE, buff=0.08, stroke=4)
        cl_rows = VGroup(label("AWS prebuilt TensorFlow Serving image", 22, INK),
                         VGroup(label("picked from", 22, INK), mono("framework_version", 22, IMAGE))
                         .arrange(RIGHT, buff=0.14, aligned_edge=DOWN)).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        cl_fr = outline_box(cl_rows.width + 0.6, cl_rows.height + 0.45, IMAGE, solid=True, fill_opacity=0.1)
        cl_rows.move_to(cl_fr)
        callout = VGroup(cl_fr, cl_rows)
        callout.move_to([-6.45 + callout.width / 2, -1.15 - callout.height / 2, 0])
        link2 = DashedLine(cont[0].get_bottom() + DOWN * 0.1, [cont[0].get_center()[0], callout.get_top()[1] + 0.05, 0],
                           color=IMAGE, stroke_width=3)
        served = chip("served by 2.13", IMAGE, size=20)
        exported = ok_chip("exported by TF 2.18")
        chips2 = VGroup(exported, served).arrange(RIGHT, buff=0.3)
        chips2.next_to(callout, DOWN, buff=0.3).align_to(callout, LEFT)
        rec2 = recording_tag()
        rec2.next_to(callout, RIGHT, buff=0.3)
        ahead = dashed_chip("checked locally in step 3")
        ahead.move_to([6.4 - ahead.width / 2, chips2.get_center()[1], 0])
        go2 = DashedLine(served.get_right() + RIGHT * 0.12, ahead.get_left() + LEFT * 0.12, color=S.GREY,
                         stroke_width=3).add_tip(tip_length=0.18)
        assert chips2.get_bottom()[1] > -3.55 and ahead.get_left()[0] > served.get_right()[0] + 0.5, \
            (rec2.get_bottom(), ahead.get_left())
        assert callout.get_right()[0] < v.slot_list[2].get_left()[0] - 0.1 or \
            callout.get_top()[1] < v.slot_caps[2].get_bottom()[1], callout.get_right()

        with self.voiceover(SAY[2]) as vo:
            v.unregistry(self, run_time=0.4)
            self.play(FadeOut(err1), FadeOut(rd1), FadeOut(br1), FadeOut(lt12), run_time=0.4)
            vo.wait_until("the SDK picks")
            self.play(Create(rg2), run_time=0.5)
            self.play(Create(link2), FadeIn(callout, shift=DOWN * 0.15), run_time=0.7)
            vo.wait_until("from framework version 2.13")
            self.play(Indicate(cl_rows[1][1], color=IMAGE, scale_factor=1.1), run_time=0.6)
            self.play(FadeIn(served, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("Our model was exported")
            self.play(FadeIn(exported, shift=UP * 0.1), FadeIn(rec2), run_time=0.5)
            vo.wait_until("In step 3")
            self.play(Create(go2), FadeIn(ahead, shift=RIGHT * 0.1), run_time=0.7)
            vo.wait_until("Serving 2.13 loads it")
            flash_tag(self, ahead, color=INK)

        # ========================================================== 3. deploy(): all three objects
        p3 = code("A/cli.py", 164, 171, font_size=20, cuts=CUTS3)
        c3 = p3.code
        lam = grey_chip("configuration shape: from the part 2 Lambda")

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(rg2), FadeOut(link2), FadeOut(callout), FadeOut(chips2), FadeOut(rec2),
                      FadeOut(go2), FadeOut(ahead), run_time=0.5)
            self.play(v.animate.shift(UP * (S_TOP - S_LOW)), run_time=0.6)
            p3.move_to([-6.45 + p3.width / 2, v.card.frame.get_bottom()[1] - 0.15 - p3.height / 2, 0])
            assert p3.get_bottom()[1] > -3.58, p3.get_bottom()
            gold = block(c3, 5, 6, COST, 0.22)
            yb = block(c3, 0, 3, TURN, 0.0)
            yel = Rectangle(width=yb.width, height=yb.height, stroke_color=TURN, stroke_width=3).move_to(yb)
            self.play(FadeIn(p3, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("with one instance")
            self.play(FadeIn(gold), run_time=0.4)
            self.play(Indicate(code_span(c3, 6, '"ml.m5.xlarge"'), color=COST, scale_factor=1.12), run_time=0.7)
            self.add(p3, gold)
            vo.wait_until("under a name with a timestamp")
            self.play(Create(yel), run_time=0.5)
            self.play(Indicate(code_span(c3, 0, "utcnow()"), color=TURN, scale_factor=1.12), run_time=0.7)
            self.add(p3, gold, yel)
            vo.wait_until("That one call creates all three")
            dep = code_span(c3, 4, "deploy(")
            self.play(dep.animate.set_color(TURN), run_time=0.3)
            self.add(p3, gold, yel)
            self.play(Indicate(code_span(c3, 4, "deploy("), color=TURN, scale_factor=1.15), run_time=0.6)
            self.add(p3, gold, yel)
            vo.wait_until("the model in SageMaker")
            v.solidify(self, run_time=0.8)
            vo.wait_until("an endpoint configuration")
            v.deploy(self, run_time=1.6)
            assert v.ep.get_left()[0] > p3.get_right()[0] + 0.3, (v.ep.get_left(), p3.get_right())
            lam.move_to([6.45 - lam.width / 2, v.ep.get_bottom()[1] - 0.3 - lam.height / 2, 0])
            assert lam.get_left()[0] > p3.get_right()[0] + 0.2 and lam.get_bottom()[1] > -3.55, lam.get_left()
            v.show(self, lam, run_time=0.4)
            vo.wait_until("which names the machine and the model")
            self.play(Indicate(v.config.rows[2], color=CLOUD, scale_factor=1.08),
                      Indicate(v.card.title, color=CLOUD, scale_factor=1.06), run_time=0.9)
            v.heal(self)
            vo.wait_until("and the endpoint, the address you call")
            self.play(Indicate(v.ep.text, color=INK, scale_factor=1.08),
                      Indicate(c3.code_lines[7], color=TURN, scale_factor=1.04), run_time=0.9)
            v.heal(self)
            self.add(p3, gold, yel)

        # ========================================================== 4. run it: NoCredentialsError
        t = term(P_APP, rows=8, size=SIZE)
        k1 = card(["with your keys · 5–10 min (README A:127)",
                   "the endpoint name · endpoint_config.json written · no output shown"], size=20)
        k1.next_to(t.box, UP, buff=0.18).align_to(t.box, LEFT)
        k2 = grey_chip("fails? the endpoint's CloudWatch logs · the tarball in S3 · README A:186–188")
        k2.next_to(k1, UP, buff=0.18).align_to(k1, LEFT)
        assert k2.get_top()[1] < TRACK_BOTTOM - 0.05, k2.get_top()

        with self.voiceover(SAY[4]) as vo:
            v.drop(self, lam, run_time=0.3)
            self.play(FadeOut(v), FadeOut(p3), FadeOut(gold), FadeOut(yel), run_time=0.6)
            self.remove(v, p3, gold, yel)
            self.play(FadeIn(t), run_time=0.4)
            ln = type_cmd(self, t, CMD28, type_time=0.9)
            pin(self, ln, beside(turn_row(), ln))
            vo.wait_until("Ours stops at line 168")
            rows = out(self, t, [OUT28[0], OUT28[1], OUT28[2], OUT28[3], (OUT28[4], ERR), OUT28[5],
                                 (OUT28[6], ERR)], run_time=0.8)
            self.play(Indicate(substring(rows[4], "168"), color=ERR, scale_factor=1.4), run_time=0.6)
            self.add(t)
            vo.wait_until("the deploy call")
            self.play(Indicate(substring(rows[4], "tensorflow_model.deploy("), color=ERR, scale_factor=1.08),
                      run_time=0.7)
            self.add(t)
            vo.wait_until("no credentials")
            self.play(Indicate(substring(rows[6], "NoCredentialsError"), color=ERR, scale_factor=1.1), run_time=0.7)
            self.add(t)
            vo.wait_until("With yours")
            self.play(FadeIn(k1, shift=UP * 0.15), run_time=0.5)
            self.play(Indicate(k1.body[0], color=INK, scale_factor=1.05), run_time=0.7)
            vo.wait_until("then it prints the endpoint name")
            self.play(Indicate(k1.body[1], color=INK, scale_factor=1.05), run_time=0.8)
            vo.wait_until("and saves it in endpoint config dot JSON")
            self.play(FadeIn(k2, shift=UP * 0.15), run_time=0.5)

        # ========================================================== 5. serverless, still billing
        sv = label("serverless = no server to manage", 24, CLOUD)
        sv.move_to([-6.4 + sv.width / 2, -3.2, 0])
        cost5 = cost_tag("endpoint · ml.m5.xlarge · 24/7 while it exists")
        l14_fr = outline_box(4.0, 1.75, PAST, solid=False)
        l14_t = label("Cloud Run · lecture 14", 20, S.GREY)
        l14_i = instance(1.2, 0.7, PAST, inner=True, dashed=True, inner_color=PAST)
        l14_z = label("0 instances", 20, S.GREY)
        l14 = VGroup(l14_fr, l14_t, l14_i, l14_z)
        no_zero = label("scale to zero", 24, ERR)
        no_zero_s = strike(no_zero, ERR)

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(t), FadeOut(k1), FadeOut(k2), run_time=0.5)
            self.remove(t)
            self.play(FadeIn(v), run_time=0.7)
            l14_fr.move_to([-6.4 + 2.0, -1.0 - 0.875, 0])
            l14_t.move_to(l14_fr.get_corner(UL) + np.array([0.2, -0.28, 0]), aligned_edge=LEFT)
            l14_i.move_to(l14_fr.get_center() + np.array([-0.95, -0.25, 0]))
            l14_z.next_to(l14_i, RIGHT, buff=0.35)
            no_zero.move_to([l14_fr.get_right()[0] + 0.4 + no_zero.width / 2, l14_fr.get_center()[1], 0])
            no_zero_s = strike(no_zero, ERR)
            cost5.move_to([6.45 - cost5.width / 2, v.ep.get_bottom()[1] - 0.25 - cost5.height / 2, 0])
            assert cost5.get_left()[0] > no_zero.get_right()[0] + 0.1 or \
                cost5.get_top()[1] < no_zero.get_bottom()[1], (cost5.get_left(), no_zero.get_right())
            assert sv.get_top()[1] < l14_fr.get_bottom()[1] - 0.1 and cost5.get_bottom()[1] > -3.55
            vo.wait_until("The lecture calls this serverless")
            self.play(Write(sv), run_time=0.9)
            vo.wait_until("It is still one machine")
            self.play(Indicate(v.ep.rack, color=CLOUD, scale_factor=1.15), run_time=0.7)
            v.heal(self)
            v.meter(self)
            vo.wait_until("billing around the clock")
            v.run(self, 0.25, 0.8)
            self.play(FadeIn(cost5, shift=UP * 0.1), v.dial.sweep(0.1), run_time=0.5)
            vo.wait_until("even with zero traffic")
            v.lane(self, run_time=0.5)
            zc = grey_chip("0 requests").move_to([-1.0, v.lane_g[0].get_center()[1] - 0.45, 0])
            v.zero_chip = zc
            v.show(self, zc, anims=[FadeIn(zc), v.dial.sweep(0.1)], run_time=0.4)
            v.run(self, 0.2, vo.until("Unlike Cloud Run", minimum=0.5))
            self.play(FadeIn(l14_fr), FadeIn(l14_t), FadeIn(l14_i), v.dial.sweep(0.08), run_time=0.6)
            self.play(Transform(l14_i, faded(l14_i, 0.15)), v.dial.sweep(0.06), run_time=0.4)
            self.play(Transform(l14_i, faded(l14_i, 1 / 0.15)), v.dial.sweep(0.06), run_time=0.4)
            self.play(Transform(l14_i, faded(l14_i, 0.15)), FadeIn(l14_z), v.dial.sweep(0.08), run_time=0.6)
            vo.wait_until("does not scale to zero")
            self.play(FadeIn(no_zero), v.dial.sweep(0.05), run_time=0.4)
            self.play(Create(no_zero_s), v.dial.sweep(0.05), run_time=0.4)
            v.run(self, 0.15, max(0.6, vo.remaining()))

        # ========================================================== 6. slides 16–17: two ways to serve
        lt16 = lref("16–17")
        left = column("managed model serving", ("SageMaker endpoint", "Vertex AI online prediction"),
                      ("deploy a model directly", "versioning", "A/B variants", "monitoring"), CLOUD, False)
        right = column("run any container", ("Cloud Run (L14)",),
                       ("you containerize", "you configure", "you add monitoring"), PAST, True)
        left.move_to([-6.45 + left.frame.width / 2, 2.75 - left.frame.height / 2, 0])
        right.move_to([6.45 - right.frame.width / 2, 2.75 - right.frame.height / 2, 0])
        assert left.rows.get_bottom()[1] > left.frame.get_bottom()[1] + 0.1, left.rows.get_bottom()

        with self.voiceover(SAY[6]) as vo:
            v.dial.freeze()
            self.play(FadeOut(v), FadeOut(l14_fr), FadeOut(l14_t), FadeOut(l14_i), FadeOut(l14_z),
                      FadeOut(no_zero), FadeOut(no_zero_s), FadeOut(sv), FadeOut(cost5), run_time=0.6)
            self.remove(v)
            self.play(FadeIn(lt16), FadeIn(left.frame), FadeIn(right.frame), run_time=0.6)
            self.play(FadeIn(left.head), FadeIn(left.sub), FadeIn(right.head), FadeIn(right.sub), run_time=0.6)
            for phrase, k in (("A model endpoint deploys", 0), ("with versioning", 1), ("A B testing", 2),
                              ("and monitoring available", 3)):
                vo.wait_until(phrase)
                self.play(Write(left.rows[k]), run_time=0.5)
            vo.wait_until("A general container service")
            self.play(Indicate(right.head, color=S.GREY, scale_factor=1.08), run_time=0.7)
            vo.wait_until("and you build the rest yourself")
            for k in range(3):
                self.play(Write(right.rows[k]), run_time=0.45)

        # ========================================================== 7. the rule of thumb; unused here
        rule = VGroup(label("rule of thumb: an endpoint to serve a trained model,", 22, TURN),
                      label("a container service when the model is one part of a larger app", 22, TURN))
        rule.arrange(DOWN, buff=0.14).move_to([0, left.frame.get_bottom()[1] - 0.25 - rule.height / 2, 0])
        mini = endpoint_plate(machine=None, plate_w=4.1)
        mini.move_to([left.frame.get_center()[0], rule.get_bottom()[1] - 0.3 - mini.height / 2, 0])
        unused = VGroup(grey_chip("1 instance"), grey_chip("1 variant"), grey_chip("no monitoring"))
        unused.arrange(RIGHT, buff=0.22).next_to(mini, RIGHT, buff=0.4)
        cap7 = label("available · not used here", 22, S.GREY)
        cap7.next_to(unused, DOWN, buff=0.2).align_to(unused, LEFT)
        assert unused.get_bottom()[1] > -3.55 and cap7.get_right()[0] < 6.55, (unused.get_bottom(), cap7.get_right())
        srcs = (left.rows[1], left.rows[2], left.rows[3])

        with self.voiceover(SAY[7]) as vo:
            self.play(Write(rule[0]), run_time=1.0)
            vo.wait_until("a container service when")
            self.play(Write(rule[1]), run_time=1.0)
            vo.wait_until("Here, those features go unused")
            self.play(FadeIn(mini, shift=UP * 0.3), run_time=0.5)
            self.play(*[FadeTransform(s.copy(), u) for s, u in zip(srcs, unused)], FadeIn(cap7), run_time=0.9)
            self.play(each(unused, S.GREY, scale=1.06, lag=0.25), run_time=0.8)

        self.play(*[FadeOut(m) for m in (left, right, rule, mini, unused, cap7, lt16, tr)], run_time=0.8)
        self.remove(left, right, rule, mini, unused, cap7, lt16, tr)
        self.wait(0.3)
