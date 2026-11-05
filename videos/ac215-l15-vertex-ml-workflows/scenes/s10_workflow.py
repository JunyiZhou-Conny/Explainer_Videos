"""S10 · From four terminals to one workflow — part 2 opens: V6 ManualToPipeline (slides 19–22, 24),
then README B › Setup Environments (tracker B1 1 → 9).

Beats (script.md "## S10"; one voiceover block each):
0. No tracker. LECTURE 15 · 19–21. V6: four GREY stage tiles with two-headed arrows; on "each run by
   a person" a GREY person + CLI chip comes under each tile; the headline types "How do we execute
   these steps?", then rewrites to "Can we automate this flow?".
1. LECTURE 15 · 21. On "The answer is an orchestrator" the people go and one BLUE "SageMaker
   Pipelines" box rises in; on "Vertex AI Pipelines" the GREY-dashed "Vertex AI Pipelines ·
   Kubeflow" box with "≈" sits beside it; on "This tutorial uses" the README B card (lines 4–7)
   appears and shrinks into four one-line chips on the tiles; the S02 mini-legend chip
   (bridge row 4) sits lower right.
2. LECTURE 15 · 22. The boxes and chips go; slide 22's duty card fills one row per phrase (order,
   repeatable, resources, monitoring: GREEN ticks; scheduling → L23 GREY, dashed ring). On
   "And it is managed" the tag becomes LECTURE 15 · 24 and a GREY chip "managed · no cluster to run".
3. Everything goes. TRACKER B1 1. Terminal `laptop` at student@laptop:~$: `git clone …` → laptop/50: 2
   (row tag extra); `cd ml-workflow-aws`; TRACKER B1 1 · extra: `git log …` (extra, title bar) →
   laptop/51: 2 wrapped, `f165c6e` YELLOW; on "An extra tree" the terminal clears: `tree …` (extra)
   → laptop/52: 7–8, 16, 24, 39, …, 52; the four src/ folders YELLOW, three GREY "stage" tags and a
   BLUE "the orchestrator" tag; ▶ your turn on the title bar.
4. The terminal goes. TRACKER B1 2 → 4, one schematic console form at a time, each transforming
   into the next (illustration): "AWS services" (B:20–24; the domain row's dashed mini-graph
   flickers on "where you will watch the pipeline"; first-form chip "labels from the README …") →
   "S3 › Create bucket" (B:30, ORANGE "[REPLACE …]") → "IAM › Users › Create user" (B:36–43:
   ml-workflow-user, four ORANGE policy chips); the bucket note becomes an ORANGE chip "bucket:
   cheese-app-ml-workflow-demo → yours" under the user form until the block ends.
5. TRACKER B1 5. The form becomes "ml-workflow-user › Security credentials" (B:46–49): CLI radio,
   Create access key, Download .csv file; a GREY .csv icon falls into a GREY laptop (no values).
   GOLD cost tag on "stay in your account", pulsing once on "check them".
6. TRACKER B1 6. README card (B:52–53) + chip "ours: AWS CLI 2.34.63 …". TRACKER B1 7: the card goes,
   terminal at …/ml-workflow-aws: `aws configure` → laptop/55: 2–5 (the two PLACEHOLDER values
   ORANGE, chip "obviously fake · capture only"; [us-east-1] / [json] flash: kept with Enter; chip
   "replaces part 1's default profile · clean up part 1 first"). TRACKER B1 7 · extra:
   `aws configure list` (extra) → laptop/56: 4–6, the masked key GREY.
7. TRACKER B1 8. Terminal clears: `aws sts get-caller-identity` / `aws s3 ls` → laptop/57: 4, 6
   wrapped, RED. GREY card over the terminal: "before configuring: no keys at all" + laptop/53:4
   from "(NoCredentials)" to "Unable to locate credentials". GREEN chip "with your keys: your
   account · your buckets"; ▶ your turn.
8. TRACKER B1 9. The terminal goes. CONSOLE "IAM › Roles" (B:72–81): the two role names fill, each
   with its trusted service and ORANGE policy count; V1 reprise: two BLUE role badges form at the
   right. CODE src/workflow/model.py 26–28 (20 pt; line 28 starts at `f"arn…`, see the report): on
   "from your account number" `{account_id}` PINK, on "and the exact role name" the role name
   YELLOW + chip "found by name"; ▶ your turn on the form. Fade to empty.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403
from common import _small_file  # noqa: F401
from explainer import style as S

SAY = NARRATION["S10"]

TS = 20                                   # the configure terminal: 72 characters a row (laptop/56)
MODEL_PY = "B/src/workflow/model.py"


# ------------------------------------------------------------------ helpers of this scene
def fixed_tracker(key: str, step: int, extra=False) -> VGroup:
    """common.tracker() with its head put back above the dots (common.py's head arrange() centres
    it at y 0; same workaround as S01/S04; requested fix in the report)."""
    tr = tracker(key, step, extra)
    tr.head.next_to(tr.dots, UP, buff=0.14, aligned_edge=LEFT)
    place_tracker(tr)
    assert tr.get_bottom()[1] >= TRACK_BOTTOM - 0.05, tr.get_bottom()
    return tr


def recolor(glyphs, color):
    """ANIMs, glyph by glyph (never animate a substring group itself: split trap)."""
    return [g.animate.set_color(color) for g in glyphs]


def seat(scene, t, *over):
    """Re-seat terminal t as one mobject after animating loose glyphs, then bring its tags forward."""
    scene.add(t)
    for m in over:
        if m in scene.mobjects:
            scene.bring_to_front(m)


def top_right_tag(f, tg, dx: float = 0.25):
    """A tag sitting on the form's top edge, right end."""
    return tg.move_to([f.frame.get_right()[0] - dx - tg.width / 2, f.frame.get_top()[1], 0])


def checks_form(title, rows_spec, path=None, form_w=8.6):
    """console_form whose ('check', name) rows show their name as an ORANGE policy chip (AWS-managed)
    instead of plain text; ticks GREY. Returns (form, chips): the chips are separate mobjects over
    the hidden texts (re-place them with place_chips() after moving the form)."""
    f = console_form(title, rows_spec, form_w=form_w, path=path)
    chips = VGroup()
    for r in f.rows:
        if getattr(r, "kind", "") == "check":
            r.tick.set_color(S.GREY)
            c = chip(r.text.text, SHARED, size=20, font=MONO)
            r.text.set_opacity(0)
            chips.add(c)
    # the chips are taller than the label rows console_form spaces them for: give each check row an
    # invisible strut of the chip's height, re-stack the rows (≥ 0.1 between adjacent chip outlines)
    # and re-fit the frame and the separator around them
    ch = max(c.height for c in chips) - 0.1
    for r in f.rows:
        if getattr(r, "kind", "") == "check":
            r.add(Rectangle(width=0.01, height=ch, stroke_opacity=0, fill_opacity=0).move_to(r.text))
    head, sep = f[2], f[1]
    f.rows.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
    body = VGroup(head, f.rows).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    f.frame.stretch_to_fit_height(body.height + 0.6)
    body.move_to(f.frame).align_to(f.frame, LEFT).shift(RIGHT * 0.3)
    sep.move_to([f.frame.get_center()[0], head.get_bottom()[1] - 0.15, 0])
    return f, place_chips(f, chips)


def place_chips(f, chips):
    rows = [r for r in f.rows if getattr(r, "kind", "") == "check"]
    for r, c in zip(rows, chips):
        c.move_to(r.text, aligned_edge=LEFT).shift(LEFT * 0.05)
    return chips


def mini_graph() -> VGroup:
    """A text-free GREY-dashed preview of S15's five-step graph (for the Studio domain row)."""
    bxs = VGroup(*[DashedVMobject(RoundedRectangle(width=0.36, height=0.22, corner_radius=0.05,
                                                   stroke_color=PAST, stroke_width=2), num_dashes=10)
                   for _ in range(5)]).arrange(RIGHT, buff=0.16)
    ars = VGroup(*[Line(bxs[i].get_right(), bxs[i + 1].get_left(), color=PAST, stroke_width=2)
                   for i in range(4)])
    return VGroup(bxs, ars)


class FourTerminals(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S10"] == 9, len(SAY)

        # ========================================================== 0. four people, four terminals
        v = ManualToPipeline(people=False).shift(UP * 0.5)   # room under the boxes for the README card
        ref = lref("19–21")
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(v, lag_ratio=0.1), FadeIn(ref), run_time=1.0)
            vo.wait_until("four stages")
            self.play(LaggedStart(*[Indicate(tl.frame, color=INK, scale_factor=1.06) for tl in v.tiles],
                                  lag_ratio=0.2), run_time=0.8)
            vo.wait_until("each run by a person at a terminal")
            v.people_in(self, run_time=1.0)
            vo.wait_until("How do we execute these steps?")
            v.headline(self, "How do we execute these steps?", run_time=1.0)
            vo.wait_until("And can we automate this flow?")
            v.headline(self, "Can we automate this flow?", run_time=0.8)

        # ========================================================== 1. the orchestrator (slide 21)
        rb_body = VGroup(*[label(s, 20, INK) for s in (
            "Data Collector: Gathers images from the internet …",
            "Data Processor: Removes duplicate images, … TFRecord format.",
            "Model Training: Submits training jobs to Amazon Sagemaker AI …",
            "Model Deploy: Updates the model signature … deploys it as an endpoint.")]) \
            .arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        rb = readme_card((4, 7), rb_body, repo="B")
        rb.move_to([0, -3.54 + rb.height / 2, 0])
        legend = bridge_chip(4)
        legend.move_to([6.55 - legend.width / 2, -3.5 + legend.height / 2, 0])
        ref21 = lref("21")
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeTransform(ref, ref21), run_time=0.5)
            v.orchestrator(self, "SageMaker Pipelines", run_time=1.2)
            vo.wait_until("The lecture uses Vertex AI Pipelines")
            v.vertex(self, "Vertex AI Pipelines · Kubeflow", run_time=0.8)
            vo.wait_until("This tutorial uses SageMaker Pipelines")
            self.play(Indicate(v.box_o[1], color=CLOUD, scale_factor=1.06), FadeIn(rb, shift=UP * 0.15),
                      run_time=0.8)
            vo.wait_until("the same idea of managed steps in a graph")
            notes = ("gathers images", "dedupe · TFRecords", "training jobs", "signature · endpoint")
            chips_ = [grey_chip(s).move_to(v.p(x, 0.12)) for x, s in zip(v.XS, notes)]
            self.play(*[TransformFromCopy(rb_body[i], chips_[i]) for i in range(4)], FadeOut(rb), run_time=1.2)
            self.remove(*chips_)
            v.note_chips = chips_
            v.add(*chips_)
            v.heal(self)
            self.play(FadeIn(legend, shift=LEFT * 0.15), run_time=0.6)

        # ========================================================== 2. workflow management (slide 22, 24)
        duty = duty_card([("order (references)", True), ("repeatable (caching, same definition)", True),
                          ("resources (instance type per step)", True), ("monitoring (Studio's graph)", True),
                          ("scheduling → L23", False)], head="workflow management · in this repo")
        duty.move_to([-2.0, -1.75, 0])
        sched_ring = ring(duty.rows[4], PAST, buff=0.05, dashed=True)
        managed = grey_chip("managed · no cluster to run")
        managed.move_to([duty.frame.get_right()[0] + 0.5 + managed.width / 2, -1.2, 0])
        ref22, ref24 = lref("22"), lref("24")
        with self.voiceover(SAY[2]) as vo:
            v.drop(self, v.box_o, v.box_v, *v.note_chips,
                   extra=[FadeOut(legend), FadeTransform(ref21, ref22)], run_time=0.6)
            v.note_chips = []
            self.play(FadeIn(duty.frame), FadeIn(duty.head), run_time=0.5)
            self.play(FadeIn(duty.rows[0], shift=RIGHT * 0.1), run_time=0.5)
            vo.wait_until("makes a run repeatable")
            self.play(FadeIn(duty.rows[1], shift=RIGHT * 0.1), run_time=0.5)
            vo.wait_until("gives each step its machine")
            self.play(FadeIn(duty.rows[2], shift=RIGHT * 0.1), run_time=0.5)
            vo.wait_until("and shows it")
            self.play(FadeIn(duty.rows[3], shift=RIGHT * 0.1), run_time=0.5)
            vo.wait_until("This repo covers those four")
            self.play(LaggedStart(*[Indicate(r.mark, color=OWN, scale_factor=1.4) for r in duty.rows[:4]],
                                  lag_ratio=0.25), run_time=1.0)
            vo.wait_until("Scheduling waits for lecture 23")
            self.play(FadeIn(duty.rows[4], shift=RIGHT * 0.1), Create(sched_ring), run_time=0.7)
            vo.wait_until("And it is managed")
            self.play(FadeTransform(ref22, ref24), FadeIn(managed, shift=LEFT * 0.15), run_time=0.7)
            self.play(Indicate(managed.text, color=CLOUD, scale_factor=1.06), run_time=0.6)

        # ========================================================== 3. clone + two extras
        tr = fixed_tracker("B1", 1)
        t = term(P_HOME, 9)
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
            self.remove(*self.mobjects)
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(t), run_time=0.6)
            c50 = capture("50")
            type_cmd(self, t, c50.cmd, type_time=0.8)
            o50 = out(self, t, c50.at(2), run_time=0.4)
            vo.wait_until("Our git clone is extra again")
            pin(self, o50[0], beside(extra_row(), o50[0]))
            type_cmd(self, t, "cd ml-workflow-aws", type_time=0.3)
            cd_prompt(self, t, P_MW, run_time=0.4)
            c51 = capture("51")
            self.play(track(tr, 1, True), run_time=0.3)
            type_cmd(self, t, c51.cmd, type_time=0.5)
            ex51 = on_bar(t, extra_row())
            o51 = out(self, t, c51.at(2), wrap=True, run_time=0.3)
            assert o51[0].text.startswith("f165c6e")
            self.play(FadeIn(ex51), *recolor(glyph_range(o51[0], 0, 7), TURN), run_time=0.3)
            seat(self, t, ex51)
            vo.wait_until("An extra tree shows four folders")
            self.play(FadeOut(ex51), run_time=0.2)
            t.clear(self)
            c52 = capture("52")
            type_cmd(self, t, c52.cmd, type_time=0.4)
            ex52 = on_bar(t, extra_row())
            self.play(FadeIn(ex52), run_time=0.3)
            rows = out(self, t, c52.at(7, 8, 16, 24, 39, "…", 52), run_time=0.5)
            names = ("data-collector", "data-processor", "model-training", "workflow")
            folder_rows = [rows[1], rows[2], rows[3], rows[4]]
            for r, n in zip(folder_rows, names):
                assert r.text.endswith(n), (r.text, n)
            self.play(*[a for r, n in zip(folder_rows, names) for a in recolor(substring(r, n), TURN)],
                      run_time=0.4)
            seat(self, t, ex52)
            vo.wait_until("three stages")
            x_tags = max(r.strut.get_right()[0] for r in folder_rows) + 0.5
            stage_tags = [beside(row_tag("stage"), r, min_x=x_tags) for r in folder_rows[:3]]
            for r, tg in zip(folder_rows[:3], stage_tags):
                attach(self, r, tg)
            self.remove(*stage_tags)
            self.play(LaggedStart(*[FadeIn(tg, shift=LEFT * 0.1) for tg in stage_tags], lag_ratio=0.3),
                      run_time=0.8)
            seat(self, t, ex52)
            vo.wait_until("and the workflow")
            orch = beside(row_tag("the orchestrator", CLOUD), folder_rows[3], min_x=x_tags)
            pin(self, folder_rows[3], orch)
            tturn = on_bar(t, turn_row())
            tturn.next_to(ex52, LEFT, buff=0.2)
            self.play(FadeIn(tturn), run_time=0.4)
            self.wait(1.2)                                    # hold the finished listing

        # ========================================================== 4. console: services, bucket, user
        sf = console_form("AWS services", [
            ("check", "SageMaker AI → Set up for single user (Quick setup)", False),
            ("check", "SageMaker Unified Studio → Create domain", False),
            ("check", "S3 → Create bucket", False),
            ("check", "ECR → container image registry", False),
            ("check", "Lambda → automated model deployment", False)], form_w=9.6, path="AWS Console")
        for r in sf.rows:
            r.tick.set_color(S.GREY)
        sf.move_to([0.6, 0.55, 0])
        ill = top_right_tag(sf, illustration_tag())
        lbl = grey_chip("labels from the README · if yours differ, look for the same field")
        lbl.next_to(sf, DOWN, buff=0.3).align_to(sf, RIGHT)
        mg = mini_graph().next_to(sf.rows[1].text, RIGHT, buff=0.45)

        bf = console_form("Create bucket", [("Bucket name", BUCKET_B), ("note", "[REPLACE WITH YOUR BUCKET NAME]"),
                                            ("button", "Create bucket")], path="S3", form_w=7.6)
        bf.rows[1].text.set_color(SHARED)
        bf.move_to([0.6, 0.55, 0])
        uf, pols = checks_form("Create user", [("User name", ""), ("note", "Attach policies directly"),
                                               ("check", "AmazonS3FullAccess"),
                                               ("check", "AmazonSageMakerFullAccess"),
                                               ("check", "AmazonEC2ContainerRegistryFullAccess"),
                                               ("check", "AWSLambda_FullAccess"),
                                               ("button", "Create user")], path="IAM › Users", form_w=7.6)
        uf.move_to([0.6, -0.1, 0])                   # taller since the chip rows were re-spaced
        place_chips(uf, pols)
        # the bucket stays on screen under the user form (README B:30's "[REPLACE …]" was only ~1.5 s)
        bchip = chip(f"bucket: {BUCKET_B} → yours", SHARED, size=20)
        bchip.next_to(uf, DOWN, buff=0.12).align_to(uf, LEFT)
        assert bchip.get_bottom()[1] >= -3.6 and uf.get_top()[1] < TRACK_BOTTOM - 0.1, (bchip.get_bottom(), uf.get_top())

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(t), FadeOut(tturn), FadeOut(ex52), track(tr, 2), run_time=0.5)
            self.remove(t, tturn, ex52)
            self.play(FadeIn(sf, shift=UP * 0.1), FadeIn(ill), run_time=0.6)
            self.play(FadeIn(lbl, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("quick setup for SageMaker AI")
            self.play(sf.rows[0].tick.animate.set_opacity(1), Indicate(sf.rows[0].text, color=TURN, scale_factor=1.04),
                      run_time=0.6)
            vo.wait_until("and a Unified Studio domain")
            self.play(sf.rows[1].tick.animate.set_opacity(1), Indicate(sf.rows[1].text, color=TURN, scale_factor=1.04),
                      run_time=0.6)
            vo.wait_until("where you will watch the pipeline")
            self.play(FadeIn(mg), run_time=0.3)
            self.play(mg.animate(rate_func=there_and_back).set_opacity(0.25), run_time=0.5)
            self.play(LaggedStart(*[r.tick.animate.set_opacity(1) for r in sf.rows[2:]], lag_ratio=0.4),
                      run_time=0.8)
            vo.wait_until("Then your bucket")
            self.add(sf)
            self.play(track(tr, 3), FadeOut(lbl), FadeOut(mg), ReplacementTransform(sf, bf),
                      ill.animate.move_to(top_right_tag(bf, ill.copy()).get_center()), run_time=0.8)
            self.bring_to_front(ill)
            self.play(Indicate(bf.rows[0].value, color=TURN, scale_factor=1.04),
                      Indicate(bf.rows[1].text, color=SHARED, scale_factor=1.04), run_time=0.7)
            vo.wait_until("and a user named ml workflow user")
            self.play(track(tr, 4), ReplacementTransform(bf, uf), TransformFromCopy(bf.rows[1], bchip),
                      ill.animate.move_to(top_right_tag(uf, ill.copy()).get_center()), run_time=0.7)
            self.bring_to_front(ill)
            self.play(uf.fill(0, USER_B), run_time=0.7)
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.1) for c in pols], lag_ratio=0.3), run_time=1.0)
            vo.wait_until("with four policies")
            self.play(LaggedStart(*[Indicate(c.text, color=SHARED, scale_factor=1.05) for c in pols], lag_ratio=0.25),
                      run_time=1.0)
            self.play(uf.press(6), run_time=0.6)
            self.wait(0.6)

        # ========================================================== 5. access key + .csv; the cost tag
        kf = console_form("Security credentials", [
            ("note", "Access keys → Create access key"),
            ("radio", "Command Line Interface (CLI)", False),
            ("check", "Confirmation", False),
            ("button", "Create access key"),
            ("button", "Download .csv file")], path=f"IAM › Users › {USER_B}", form_w=7.0)
        kf.move_to([-6.5 + kf.width / 2, 0.45, 0])
        lap = laptop_glyph(1.9, LAPTOP).move_to([4.4, -0.2, 0])
        lap_cap = label("your laptop", 20, S.GREY).next_to(lap, DOWN, buff=0.15)
        csv = file_icon(".csv", LAPTOP)
        csv.move_to(kf.rows[4].box.get_right() + RIGHT * 0.6)
        cost = cost_tag("quick setup · Studio domain · bucket · check at clean-up")
        cost.move_to([0, -3.15, 0])
        with self.voiceover(SAY[5]) as vo:
            self.play(track(tr, 5), FadeOut(pols), FadeOut(bchip), ReplacementTransform(uf, kf),
                      ill.animate.move_to(top_right_tag(kf, ill.copy()).get_center()), run_time=0.8)
            self.bring_to_front(ill)
            self.play(FadeIn(lap), FadeIn(lap_cap), run_time=0.5)
            vo.wait_until("for the command line")
            self.play(kf.rows[1].tick.animate.set_opacity(1), Indicate(kf.rows[1].text, color=TURN, scale_factor=1.04),
                      run_time=0.6)
            self.play(kf.rows[2].tick.animate.set_opacity(1), run_time=0.3)
            self.play(kf.press(3), run_time=0.6)
            vo.wait_until("and download the C S V file")
            self.play(kf.press(4), FadeIn(csv, shift=RIGHT * 0.1), run_time=0.6)
            self.play(csv.animate.move_to(lap.get_center() + UP * 0.12), run_time=1.0)
            vo.wait_until("stay in your account")
            self.play(Write(cost), run_time=0.8)
            vo.wait_until("check them when you clean up")
            flash_tag(self, cost)

        # ========================================================== 6. install the CLI, aws configure
        cli_rows = VGroup(
            VGroup(label("macOS:", 22, INK), mono("brew install awscli", 20, INK),
                   label("or download installer from AWS", 22, S.GREY)).arrange(RIGHT, buff=0.18),
            VGroup(label("Linux:", 22, INK), mono("sudo snap install aws-cli --classic", 20, INK),
                   label("or use curl installer", 22, S.GREY)).arrange(RIGHT, buff=0.18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        rc = readme_card((52, 53), cli_rows, repo="B")
        rc.move_to([-6.5 + rc.width / 2, 1.7, 0])
        ours = grey_chip("ours: AWS CLI 2.34.63 from the laptop's packages · at the time of recording")
        ours.next_to(rc, DOWN, buff=0.3).align_to(rc, LEFT)
        t = term(P_MW, 10, size=TS)
        fake = grey_chip("obviously fake · capture only")
        repl = grey_chip("replaces part 1's default profile · clean up part 1 first")
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(kf), FadeOut(ill), FadeOut(lap), FadeOut(lap_cap), FadeOut(csv), FadeOut(cost),
                      track(tr, 6), run_time=0.6)
            self.play(FadeIn(rc, shift=UP * 0.1), run_time=0.6)
            self.play(FadeIn(ours, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("then aws configure")
            self.play(FadeOut(rc), FadeOut(ours), track(tr, 7), FadeIn(t), run_time=0.6)
            c55 = capture("55")
            type_cmd(self, t, c55.cmd, type_time=0.6)
            vo.wait_until("and paste the two values")
            keys = out(self, t, c55.at(2, 3), wrap=True, run_time=0.6)
            assert keys[0].text.endswith(KEY_PH) and keys[-1].text == SECRET_PH, [k.text for k in keys]
            self.play(*recolor(substring(keys[0], KEY_PH), SHARED), *recolor(keys[-1], SHARED), run_time=0.5)
            seat(self, t)
            under_term(t, fake)
            self.play(FadeIn(fake, shift=DOWN * 0.1), run_time=0.4)
            p45 = out(self, t, c55.at(4, 5), run_time=0.5)
            self.play(*recolor(substring(p45[0], "[us-east-1]"), TURN), *recolor(substring(p45[1], "[json]"), TURN),
                      run_time=0.5)
            seat(self, t, fake)
            vo.wait_until("From here on")
            repl.next_to(t.box, UP, buff=0.12).align_to(t.box, RIGHT)
            fake.generate_target()
            fake.target.next_to(repl, LEFT, buff=0.3)
            self.play(MoveToTarget(fake), FadeIn(repl, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("we typed obviously fake placeholders")
            self.play(Indicate(fake.text, color=SHARED, scale_factor=1.06), run_time=0.6)
            vo.wait_until("so AWS answers with real errors")
            c56 = capture("56")
            self.play(track(tr, 7, True), run_time=0.4)
            ln56 = type_cmd(self, t, c56.cmd, type_time=0.5)
            pin(self, ln56, beside(extra_row(), ln56), run_time=0.3)
            o56 = out(self, t, [s.rstrip() for s in c56.at(4, 5, 6)], run_time=0.6)
            self.play(*recolor(substring(o56[0], "****************_KEY"), S.GREY),
                      *recolor(substring(o56[1], "****************0000"), S.GREY), run_time=0.4)
            seat(self, t, fake, repl)

        # ========================================================== 7. test the configuration
        c53 = capture("53")
        e53 = from_phrase(cut(c53.line(4), "Unable to locate credentials", ellipsis=""), "(NoCredentials)")
        before = card([label("before configuring: no keys at all", 20, S.GREY), mono(e53, 20, ERR)], size=20)
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(fake), FadeOut(repl), track(tr, 8), run_time=0.4)
            t.clear(self)
            c57 = capture("57")
            type_capture(self, t, c57, type_time=0.6)
            vo.wait_until("AWS itself rejects the fake token")
            e57 = out(self, t, c57.at(4, 6), wrap=True, color=ERR, run_time=0.8)
            under_term(t, before)
            self.play(FadeIn(before, shift=DOWN * 0.1), run_time=0.5)
            ids = [substring(r, s) for r in e57 for s in ("InvalidClientTokenId", "InvalidAccessKeyId") if s in r.text]
            uls = VGroup(*[under(g, ERR) for g in ids])
            self.play(Create(uls), run_time=0.5)
            vo.wait_until("With yours")
            yours = ok_chip("with your keys: your account · your buckets")
            yours.move_to([e57[-1].strut.get_left()[0] + yours.width / 2, e57[-1].strut.get_bottom()[1] - 0.42, 0])
            self.play(FadeIn(yours, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Don't go on until they do")
            tturn = on_bar(t, turn_row())
            self.play(FadeIn(tturn), Indicate(yours.text, color=OWN, scale_factor=1.05), run_time=0.6)

        # ========================================================== 8. two roles; the ARN built by name
        rf = console_form("Create role", [
            ("Name", ROLE_SM), ("note", "trusted: SageMaker · 3 managed policies"),
            ("Name", ROLE_SM), ("note", "trusted: Lambda · 2 managed policies")],
            path="IAM › Roles", form_w=6.0)          # 'Name': README B:75's own label
        for k in (0, 2):
            rf.rows[k].value.set_opacity(0)           # sized for the long name; fill() types it in
        for k, n in ((1, "3"), (3, "2")):
            tx = rf.rows[k].text                      # a label Text: .text and glyphs skip the spaces
            a = tx.text.index(f"{n}managedpolicies")
            for g in tx.submobjects[a:a + len(n) + 15]:
                g.set_color(SHARED)
        rf.move_to([-6.5 + rf.width / 2, 2.75 - rf.height / 2, 0])
        rill = top_right_tag(rf, illustration_tag())
        rturn = your_turn().next_to(rf, RIGHT, buff=0.4).align_to(rf, UP).shift(DOWN * 0.45)
        lines = excerpt(MODEL_PY, 26, 28).split("\n")
        ind = min(len(s) - len(s.lstrip()) for s in lines)
        lines = [s[ind:] for s in lines]
        assert lines[2].startswith('role_arn = f"arn:aws:iam::{account_id}:role/' + ROLE_SM), lines[2]
        lines[2] = "… " + from_phrase(lines[2], 'f"arn', ellipsis="")
        cp = code_panel("\n".join(lines), shown_path(MODEL_PY), 26, "python", font_size=20)
        cp.move_to([0, -3.5 + cp.height / 2, 0])
        code_span(cp.code, 2, "…").set_color(S.GREY)   # the house cut mark (the highlighter makes it PINK)
        # V1 reprise: the two BLUE badges side by side between the form and the code (5.4 wide each:
        # no room beside the form)
        bdg = VGroup(role_badge(ROLE_SM), role_badge(ROLE_LAMBDA)).arrange(RIGHT, buff=0.5)
        bdg.move_to([-6.5 + bdg.width / 2, (rf.get_bottom()[1] + cp.get_top()[1]) / 2, 0])
        assert rf.get_bottom()[1] - bdg.get_top()[1] > 0.1 and bdg.get_bottom()[1] - cp.get_top()[1] > 0.1, \
            (rf.get_bottom(), bdg.get_top(), bdg.get_bottom(), cp.get_top())
        found = grey_chip("found by name")
        with self.voiceover(SAY[8]) as vo:
            self.play(track(tr, 9), AnimationGroup(
                AnimationGroup(FadeOut(t), FadeOut(tturn), FadeOut(yours), FadeOut(before), FadeOut(uls)),
                AnimationGroup(FadeIn(rf, shift=UP * 0.1), FadeIn(rill)), lag_ratio=0.6), run_time=0.9)
            self.remove(t)
            self.play(rf.fill(0, ROLE_SM), run_time=0.8)
            self.play(GrowFromCenter(bdg[0]), run_time=0.6)
            vo.wait_until("and Cheese App Lambda Execution Role")
            self.play(rf.fill(2, ROLE_LAMBDA), run_time=0.8)
            self.play(GrowFromCenter(bdg[1]), run_time=0.6)
            vo.wait_until("The code builds each A R N")
            self.play(FadeIn(cp, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("from your account number")
            acc = code_span(cp.code, 2, "{account_id}")
            acc_ul = under(acc, ROUTE)
            self.play(*recolor(acc, ROUTE), Create(acc_ul), run_time=0.5)
            self.add(cp, acc_ul)
            vo.wait_until("and the exact role name")
            rn = code_span(cp.code, 2, ROLE_SM)
            rn_ul = under(rn, TURN)
            self.play(*recolor(rn, TURN), Create(rn_ul), run_time=0.5)
            self.add(cp, acc_ul, rn_ul)
            found.move_to([cp.get_right()[0] - found.width / 2, cp.header.get_center()[1] + 0.06, 0])
            self.play(FadeIn(found, shift=DOWN * 0.1), Indicate(bdg[0].text, color=TURN, scale_factor=1.05),
                      run_time=0.6)
            vo.wait_until("and pause here")
            self.play(FadeIn(rturn, shift=UP * 0.1), run_time=0.4)
            self.wait(1.2)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
        self.remove(*self.mobjects)
        self.wait(0.3)
