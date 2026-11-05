"""S06 · --prepare: a SavedModel in a tarball (README A › Prepare, deploy, predict, step 1; the V4
ArtifactTrip set piece; LECTURE 15 · 12 in block 0 only).

Beats (script.md "## S06", one voiceover block each):
 0  TRACKER A3 1 (fades in: a new README section). README card (README.md · lines 113–117, chip A)
    top-left, the four bullets lighting YELLOW as spoken; lecture tag "Lecture 15 · slide 12" top
    right. V4 ArtifactTrip under the card draws node by node with the bullets: GREY-dashed GitHub
    release v1.0, TEAL container, GREEN SavedModel, GREEN model.tar.gz, BLUE S3 bucket; on "Those are
    steps 1 and 3" the PINK step numbers 1 and 3 and the GREY-struck "2 · signature" chip; the struck
    chip flashes on "Step 2". The card, the step marks and the lecture tag go at the end.
 1  V4 moves up (shifted, never scaled). 7-row terminal (20 pt) at the container prompt
    (app) app@<id>:/app$ with a GREY chip on its title bar "our capture: a fresh container per step ·
    stay in yours". Types `python cli.py --prepare` (▶ your turn) -> TERM(laptop/27: 52, …, 74, 79,
    …, 227); 79 and 227 RED. On "at line 73" V4's RED "create bucket" node appears first, above the
    download, and the chain dims and stops. `ls -la artifacts` (extra) -> TERM(laptop/27: 229) RED;
    the dimmed GitHub node flashes on "nothing was downloaded".
 2  Terminal and V4 go. CODE(cli.py: 71–82) + CODE(cli.py: 84–85, line 85 cut) at 20 pt: lines 71–82
    YELLOW (73 stronger), lines 84–85 GREY; `erratum` + chip "the README list skips this" top right.
    On "or reuses yours" lines 79–82 GREEN; the download panel gives way to a GREY card on lines
    79–80: "someone else's name → 'already exists', then AccessDenied on upload · pick a unique
    name (README A:195–197)".
 3  TRACKER A3 1 · extra · capture stub. V4 returns at the top without its create-bucket node,
    dimmed; 10-row host terminal "laptop · another tab": laptop/40's line 1 (cut). On "with S3
    replaced by a stub" a GREY dashed "stub" chip under the bucket. TERM(laptop/40: 18, 19 wrap
    GREY, 21, 22 wrap GREEN, …, 293 wrap, …, 323–327 wrap RED + row tag "extra · capture stub"),
    printed with the clauses, while a PINK dot runs the chain (download -> container -> SavedModel
    -> tarball) and stops at a RED wall "not sent" on the arrow into the bucket.
 4  TRACKER A3 1 · extra. laptop/41's line 1 (folds) -> TERM(laptop/41: 12–20 wrap); on "A
    SavedModel is a folder" the three /1/ rows (fingerprint.pb, saved_model.pb, variables) light
    GREEN; on "the graph" the terminal shrinks to 4 rows keeping them and V4's SavedModel unfolds
    into a GREEN card: saved_model.pb (the graph · named entry points · serving_default), variables/
    (the weights), fingerprint.pb, assets/. saved_model.pb and variables/ flash on their words.
 5  TRACKER A3 1 · extra. The card, the wall and the terminal go. CODE(cli.py: 101–104) +
    CODE(cli.py: 115–117) at 20 pt: 102–104 YELLOW, 116–117 GREEN; V4 chip "1/" under the
    SavedModel; on "because TensorFlow Serving" a GREY chip "TF Serving: <name>/<version>/" top
    right. On "then version" the panels give way to a 9-row terminal: `tar tzvf …model.tar.gz`
    (extra) -> TERM(laptop/42: 2–8, line 7 wrapped); "1/ inside" under the tarball; the `1/` prefix
    YELLOW on every line.
 6  TRACKER A3 1 · extra. The version chips go; 8-row terminal. laptop/44's line 1 (extra) ->
    TERM(laptop/44: 2–4): ` M Pipfile` and ` M docker-shell.sh` YELLOW + row tag "your two
    edits", line 4 GREY. On "In your account": `aws s3 ls s3://your-models-bucket-placeholder/ --recursive` (extra;
    README A:187) + row tag "extra · README A:187 · your bucket name · needs your account · no output shown"; a PINK
    dot reaches the bucket; the PINK dashed URI s3://<bucket>/…/model.tar.gz under it with "with
    your keys"; on "and storage bills" the GOLD cost tag "the tarball in S3 · storage". Fade to an
    empty frame.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S06"]
SIZE = 20                                     # terminal font: 72 characters a row

# ------------------------------------------------------------------ the real sources (checked)
C27, C40, C41, C42, C44 = (capture(n) for n in ("27", "40", "41", "42", "44"))
CMD27 = C27.typed(35)
LS27 = C27.typed(228)
assert CMD27 == "python cli.py --prepare" and LS27 == "ls -la artifacts"
OUT27 = [C27.line(52), "…", unbox(C27.line(74)), unbox(C27.line(79)), "…", C27.line(227)]
assert OUT27[2] == "/app/cli.py:73 in prepare", OUT27[2]
assert "s3_client.create_bucket(Bucket=S3_MODELS_BUCKET_NAME)" in OUT27[3] and OUT27[3].startswith("❱  73")
assert OUT27[5] == "NoCredentialsError: Unable to locate credentials"
OUT27_LS = C27.at(229)
assert OUT27_LS[0].startswith("ls: cannot access 'artifacts'")

CMD40 = cut(C40.cmd, n=72 - len(P_MD) - 1)                     # script.md: (extra; cut)
assert C40.cmd.startswith(CMD40[:-1]) and len(P_MD) + 1 + len(CMD40) <= 72
L40_19 = C40.line(19)
L40_22 = C40.line(22)
L40_293 = C40.line(293)
L40_ERR = C40.at((323, 327))
assert L40_19.startswith("[capture stub] create_bucket(") and "NOT sent" in L40_19
assert L40_22.startswith("Saved artifact at './artifacts/model-mobilenetv2_train_base_True.v1/1'")
assert C40.line(21) == "Using Keras 3 export()" and L40_293.startswith("Uploading model to s3://")
assert L40_ERR[0].startswith("RuntimeError: [capture stub]") and "NOT sent" in L40_ERR[3]

OUT41 = C41.at((12, 20))
assert OUT41[0] == "artifacts/model-mobilenetv2_train_base_True.v1"
assert OUT41[4].endswith("/1/saved_model.pb") and OUT41[5].endswith("/1/variables")
OUT42 = C42.at((2, 8))
assert all(" 1/" in s for s in OUT42), OUT42
OUT44 = C44.at((2, 4))
assert OUT44[0] == " M Pipfile" and OUT44[1] == " M docker-shell.sh" and OUT44[2].startswith(".gitignore:33:artifacts/")

AWS_LS = "aws s3 ls s3://your-models-bucket-placeholder/ --recursive"  # script.md S06 block 6 (extra; README A:187);
# bracket-free bucket (the docker-shell.sh value): `<your-bucket>` is a shell redirection, the S09 erratum
assert "Verify the model.tar.gz was uploaded" in readme(187, "A")

README_ROWS = (["Run ", ("python cli.py --prepare", "mono"), ", this will:"],
               "1. Download the model from GitHub",
               "2. Prepare the model in TensorFlow SavedModel format",
               "3. Package it as model.tar.gz (required by SageMaker)",
               "4. Upload to the specified S3 bucket")
assert "Run `python cli.py --prepare`, this will:" in readme(113, "A")
for _k in range(1, 5):
    assert README_ROWS[_k][3:] in readme(113 + _k, "A"), README_ROWS[_k]

Y_LOW = -1.5        # V4 under the README card (block 0)
Y_MID = 0.72        # V4 with its create-bucket node, over a 7-row terminal (block 1)
Y_TOP = 2.2         # V4 without node 0, over a 10-row terminal (blocks 3-6)


def fixed_tracker(key: str, step: int, extra=False) -> VGroup:
    """common.tracker() with its head put back above the dots (common.py's head arrange() centres
    it at y 0; the workaround of S01/S03/S04/S05; requested fix in the report)."""
    tr = tracker(key, step, extra)
    tr.head.next_to(tr.dots, UP, buff=0.14, aligned_edge=LEFT)
    place_tracker(tr)
    assert tr.get_bottom()[1] >= TRACK_BOTTOM - 0.05, tr.get_bottom()
    return tr


def shift_trip(v, dy: float, members: bool = True) -> None:
    """Shift ArtifactTrip `v` by dy, including the nodes and arrows it has not shown yet (they are
    built in __init__ at the layout position and do not follow a shift of the piece: workaround,
    requested fix in the report). members=False: only the parts not yet in the piece (the caller
    animates the piece itself)."""
    fam = v.get_family()
    parts = list(v.nodes) + list(v.arrows.values())
    for m in parts:
        if m not in fam:
            m.shift(UP * dy)
    if members:
        v.shift(UP * dy)


def readme_body() -> VGroup:
    rows = VGroup()
    for r in README_ROWS:
        if isinstance(r, str):
            rows.add(label(r, 22, INK))
        else:
            rows.add(VGroup(*[mono(x[0], 22, INK) if isinstance(x, tuple) else label(x, 22, INK)
                              for x in r]).arrange(RIGHT, buff=0.1))
    return rows.arrange(DOWN, aligned_edge=LEFT, buff=0.14)


class PrepareArtifact(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S06"] == 7, len(SAY)
        self.bar_tags = []
        self.t = None

        # ========================================================== 0. four bullets, V4, slide 12
        tr = fixed_tracker("A3", 1)
        body = readme_body()
        rc = readme_card((113, 117), body, repo="A")
        rc.move_to([-6.5 + rc.width / 2, 2.8 - rc.height / 2, 0])
        lt = lref("12")
        v = ArtifactTrip()
        shift_trip(v, Y_LOW)
        self.v = v
        assert rc.get_bottom()[1] > Y_LOW + 1.2, rc.get_bottom()

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.2), FadeIn(rc, shift=DOWN * 0.2), run_time=0.7)
            self.play(Indicate(tr.caption, color=TURN, scale_factor=1.06),
                      Indicate(body[0][1], color=TURN, scale_factor=1.06), run_time=0.8)
            vo.wait_until("The README lists four things")
            self.play(LaggedStart(*[Indicate(body[k], color=TURN, scale_factor=1.04) for k in range(1, 5)],
                                  lag_ratio=0.3), run_time=1.4)
            vo.wait_until("Download the model from GitHub")
            self.lit(body, 1)
            self.play(FadeIn(lt), run_time=0.3)
            v.build(self, 1, lag=0.6)
            vo.wait_until("convert it to the SavedModel format")
            self.lit(body, 2)
            v.build(self, 3, lag=0.45)
            vo.wait_until("pack it as model dot tar dot G Z")
            self.lit(body, 3)
            v.build(self, 4, lag=0.5)
            vo.wait_until("and upload it to your bucket")
            self.lit(body, 4)
            v.build(self, 5, lag=0.5)
            vo.wait_until("Those are steps 1 and 3")
            self.lit(body, None)
            v.marks(self, run_time=0.7)
            self.play(Indicate(v.step_marks[0], color=ROUTE, scale_factor=1.3),
                      Indicate(v.step_marks[1], color=ROUTE, scale_factor=1.3), run_time=0.7)
            v.heal(self)
            vo.wait_until("Step 2, the signature change")
            self.play(Indicate(v.step_marks[2], color=S.GREY, scale_factor=1.12), run_time=0.8)
            v.heal(self)
        self.play(FadeOut(rc), FadeOut(lt), run_time=0.5)
        v.drop(self, v.step_marks, run_time=0.4)
        v.step_marks = None

        # ========================================================== 1. run it: NoCredentialsError
        t = term(P_APP, rows=7, size=SIZE)
        self.t = t
        fresh = on_bar(t, row_tag("our capture: a fresh container per step · stay in yours"))
        if t.title is not None:     # the wide chip would cover the centred title: move it left of it
            t.title.move_to([(t.box.get_left()[0] + 1.0 + fresh.get_left()[0]) / 2, t.title.get_y(), 0])
            assert t.title.get_right()[0] < fresh.get_left()[0] - 0.2, (t.title.get_right(), fresh.get_left())
        assert t.box.get_top()[1] < Y_MID - 0.575 - 0.08, t.box.get_top()

        with self.voiceover(SAY[1]) as vo:
            shift_trip(v, Y_MID - Y_LOW, members=False)
            self.play(v.animate.shift(UP * (Y_MID - Y_LOW)), run_time=0.7)
            self.play(FadeIn(t), run_time=0.4)
            self.bar(fresh)
            ln = type_cmd(self, t, CMD27, type_time=0.9)
            pin(self, ln, beside(turn_row(), ln))
            vo.wait_until("Ours stops right away")
            rows = out(self, t, [OUT27[0], OUT27[1], OUT27[2], (OUT27[3], ERR), OUT27[4], (OUT27[5], ERR)],
                       run_time=0.7)
            vo.wait_until("no credentials")
            self.play(Indicate(substring(rows[5], "NoCredentialsError"), color=ERR, scale_factor=1.1), run_time=0.6)
            self.reseat()
            vo.wait_until("at line 73 of cli.py")
            self.play(Indicate(substring(rows[3], "73"), color=ERR, scale_factor=1.4), run_time=0.6)
            self.reseat()
            vo.wait_until("which creates the bucket")
            self.play(Indicate(substring(rows[3], "create_bucket"), color=ERR, scale_factor=1.1), run_time=0.5)
            self.reseat()
            v.stop(self, run_time=0.8)
            vo.wait_until("And the artifacts folder")
            ln = type_cmd(self, t, LS27, type_time=0.6)
            pin(self, ln, beside(extra_row(), ln))
            out(self, t, [(OUT27_LS[0], ERR)], run_time=0.4)
            vo.wait_until("so nothing was downloaded")
            self.play(Indicate(v.nodes[1], color=ERR, scale_factor=1.08), run_time=0.8)
            v.heal(self)

        # ========================================================== 2. a gap in the README list
        p1 = code("A/cli.py", 71, 82, font_size=20)
        p1.move_to([0, 2.8 - p1.height / 2, 0])
        p2 = code("A/cli.py", 84, 85, font_size=20, cuts={85: "model-deployment-aws/"})
        p2.next_to(p1, DOWN, buff=0.1).align_to(p1, LEFT)
        assert p2.get_bottom()[1] > -3.58, p2.get_bottom()
        c1 = p1.code
        blk = self.block(c1, 0, 11, TURN, 0.12)
        bar73 = line_bar(c1, 2, TURN, 0.28)
        grn = self.block(c1, 8, 11, OWN, 0.25)
        bar_dl = self.block(p2.code, 0, 1, S.GREY, 0.2)
        tags2 = VGroup(erratum_tag(), grey_chip("the README list skips this")).arrange(RIGHT, buff=0.2)
        tags2.move_to([6.55 - tags2.width / 2, 3.2, 0])
        assert tags2.get_left()[0] > tr.get_right()[0] + 0.2, (tags2.get_left(), tr.get_right())
        note2 = card(["someone else's name → 'already exists',",
                      "then AccessDenied on upload · pick a unique name (README A:195–197)"], size=20)
        note2.move_to([6.5 - note2.width / 2, p1.get_bottom()[1] - 0.2 - note2.height / 2, 0])
        # from the end of line 80, right past the longer line 82, then down to the note (a straight
        # drop would cross line 82's text)
        x_lk = max(c1.code_lines[9].get_right()[0], c1.code_lines[11].get_right()[0]) + 0.3
        y_lk = c1.code_lines[9].get_center()[1]
        assert x_lk < min(p1.get_right()[0], note2.get_right()[0]) - 0.2, x_lk
        lk = DashedVMobject(VMobject().set_points_as_corners(
            [[c1.code_lines[9].get_right()[0] + 0.15, y_lk, 0], [x_lk, y_lk, 0], [x_lk, note2.get_top()[1], 0]]),
            num_dashes=24).set_stroke(S.GREY, 2.5)

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(t), FadeOut(v), *self.unbar_anims(), run_time=0.6)
            self.remove(t, v)
            self.t = None
            self.play(FadeIn(p1, shift=DOWN * 0.2), FadeIn(blk), run_time=0.6)
            self.play(FadeIn(bar73), run_time=0.3)
            self.play(FadeIn(tags2, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("the code creates the bucket")
            self.play(Indicate(code_span(c1, 2, "create_bucket"), color=TURN, scale_factor=1.12), run_time=0.7)
            self.add(p1, blk, bar73)
            vo.wait_until("before it downloads anything")
            p2.code.code_lines.set_opacity(0.55)
            self.play(FadeIn(p2, shift=UP * 0.15), FadeIn(bar_dl), run_time=0.6)
            vo.wait_until("a step the list does not mention")
            flash_tag(self, tags2[1])
            vo.wait_until("With your keys")
            self.play(Indicate(c1.code_lines[2], color=TURN, scale_factor=1.04), run_time=0.7)
            self.add(p1, blk, bar73)
            vo.wait_until("or reuses yours")
            self.play(FadeIn(grn), *[c1.code_lines[k].animate.set_color(OWN) for k in (8, 10)], run_time=0.5)
            self.add(p1, blk, bar73, grn)
            self.play(FadeOut(p2), FadeOut(bar_dl), run_time=0.4)
            self.remove(p2, bar_dl)
            self.play(Create(lk), FadeIn(note2, shift=UP * 0.15), run_time=0.6)

        # ========================================================== 3. extra: S3 stubbed
        # V4 comes back at the top, without its create-bucket node (block 1 showed it).
        for m in (v.nodes[0], v.arrows[0], v.cross):
            v._detach(m)
        v.cross = None
        shift_trip(v, Y_TOP - Y_MID)
        t = term(P_MD, rows=10, size=SIZE, title="laptop · another tab")
        self.t = t
        assert t.box.get_top()[1] < Y_TOP - 0.6 - 0.45, t.box.get_top()
        stub_bar = on_bar(t, extra_row("capture stub"))
        dot = pulse_dot(ROUTE, 0.11).move_to(v.nodes[1].frame.get_right())

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(p1), FadeOut(blk), FadeOut(bar73), FadeOut(grn), FadeOut(note2), FadeOut(lk),
                      FadeOut(tags2), track(tr, 1, "capture stub"), run_time=0.6)
            self.play(FadeIn(v), FadeIn(t), run_time=0.6)
            self.bar(stub_bar)
            type_cmd(self, t, CMD40, type_time=1.2)
            vo.wait_until("with S3 replaced by a stub")
            stub = dashed_chip("stub").next_to(v.nodes[5].frame, DOWN, buff=0.12)
            v.show(self, stub, anims=[FadeIn(stub, shift=UP * 0.1)], run_time=0.4)
            self.play(Indicate(v.nodes[5], color=S.GREY, scale_factor=1.06), run_time=0.8)
            v.heal(self)
            vo.wait_until("The release zip downloads")
            v.resume(self, run_time=0.5)
            out(self, t, [C40.line(18), (L40_19, S.GREY), C40.line(21)], wrap=True, run_time=0.6)
            self.play(FadeIn(dot), run_time=0.2)
            self.play(dot.animate.move_to(v.nodes[2].frame.get_left()), run_time=0.6)
            vo.wait_until("the model is exported")
            r22 = out(self, t, [(L40_22, OWN)], wrap=True, run_time=0.4)
            self.play(dot.animate.move_to(v.nodes[3].frame.get_left()), run_time=0.6)
            self.play(Indicate(v.nodes[3], color=OWN, scale_factor=1.06), run_time=0.5)
            v.heal(self)
            vo.wait_until("and the stub stops the upload")
            out(self, t, ["…", L40_293, "…"], wrap=True, run_time=0.4)
            rerr = out(self, t, [(s, ERR) for s in L40_ERR], wrap=True, run_time=0.5)
            pin(self, rerr[0], beside(extra_row("capture stub"), rerr[0]))
            self.play(dot.animate.move_to(v.arrows[4].get_center() + LEFT * 0.2), run_time=0.5)
            v.wall(self, run_time=0.4)
            vo.wait_until("Nothing reaches AWS")
            self.play(FadeOut(dot), Indicate(v.wall_g[1], color=ERR, scale_factor=1.2), run_time=0.8)
            v.heal(self)
            v.drop(self, stub, run_time=0.3)

        # ========================================================== 4. what it made: a SavedModel
        with self.voiceover(SAY[4]) as vo:
            self.wipe(track(tr, 1, True), *self.unbar_anims())
            ex4 = on_bar(t, extra_row())
            self.bar(ex4)
            type_cmd(self, t, C41.cmd, type_time=0.8)
            r41 = out(self, t, OUT41, wrap=True, run_time=0.5)
            keep = [r for r in r41 if any(r.text.endswith(e) for e in ("/1/fingerprint.pb", "/1/saved_model.pb",
                                                                     "/1/variables"))]
            assert len(keep) == 3, [r.text for r in r41]
            vo.wait_until("A SavedModel is a folder")
            self.play(*[substring(r, "/1/").animate.set_color(OWN) for r in keep], run_time=0.4)
            self.reseat()
            self.play(*[Indicate(r, color=OWN, scale_factor=1.03) for r in keep], run_time=0.8)
            self.reseat()
            vo.wait_until("the graph and its named entry points")
            resize(self, t, 4, keep=keep, extra=[tg.animate.shift(DOWN * 6 * t.pitch) for tg in self.bar_tags],
                   run_time=0.5)
            v.unfold(self, run_time=0.6)
            assert v.card.get_bottom()[1] > t.box.get_top()[1] + 0.08, (v.card.get_bottom(), t.box.get_top())
            items = v.card[1][1]
            self.play(Indicate(items[0], color=OWN, scale_factor=1.06), run_time=0.7)
            v.heal(self)
            self.paint(keep[1], "saved_model.pb", TURN)
            vo.wait_until("and the weights in a variables folder")
            self.play(Indicate(items[1], color=OWN, scale_factor=1.08), run_time=0.8)
            v.heal(self)
            self.paint(keep[2], "variables", TURN)

        # ========================================================== 5. a folder named 1, in a tarball
        pa = code("A/cli.py", 101, 104, font_size=20)
        pb = code("A/cli.py", 115, 117, font_size=20)
        pans = VGroup(pa, pb).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        pans.move_to([-6.5 + pans.width / 2, 0.7 - pans.height / 2, 0])
        assert pans.get_bottom()[1] > -3.55, pans.get_bottom()
        ya = self.block(pa.code, 1, 3, TURN, 0.22)
        gb = self.block(pb.code, 1, 2, OWN, 0.22)

        with self.voiceover(SAY[5]) as vo:
            v.drop(self, v.card, v.wall_g, extra=[FadeOut(t), *self.unbar_anims()], run_time=0.5)
            v.card = v.wall_g = None
            self.remove(t)
            self.play(FadeIn(pans, shift=RIGHT * 0.2), run_time=0.6)
            self.play(FadeIn(ya), code_span(pa.code, 2, '"1"').animate.set_color(TURN), run_time=0.5)
            self.add(pans, ya)
            c3 = chip("1/", OWN, size=20, font=MONO).next_to(v.nodes[3].frame, DOWN, buff=0.12)
            c4 = chip("1/ inside", OWN, size=20, font=MONO).next_to(v.nodes[4].frame, DOWN, buff=0.12)
            v.show(self, c3, anims=[FadeIn(c3, shift=DOWN * 0.15)], run_time=0.4)
            vo.wait_until("because TensorFlow Serving")
            tfs = grey_chip("TF Serving: <name>/<version>/")
            tfs.move_to([6.55 - tfs.width / 2, 3.22, 0])           # top right: no lecture tag here
            assert tfs.get_left()[0] > tr.get_right()[0] + 0.3, (tfs.get_left(), tr.get_right())
            v.show(self, tfs, anims=[FadeIn(tfs, shift=DOWN * 0.15)],
                   extra=[FadeIn(gb), code_span(pb.code, 2, 'arcname="1"').animate.set_color(OWN)], run_time=0.5)
            self.add(pans, ya, gb)
            flash_tag(self, tfs, run_time=0.6)
            vo.wait_until("then version")
            self.play(FadeOut(pans), FadeOut(ya), FadeOut(gb), run_time=0.4)
            self.remove(pans, ya, gb)
            t = term(P_MD, rows=9, size=SIZE, title="laptop · another tab")
            self.t = t
            ex5 = on_bar(t, extra_row())
            self.play(FadeIn(t), FadeIn(ex5), run_time=0.3)
            self.bar_tags.append(ex5)
            type_cmd(self, t, C42.cmd, type_time=0.8)
            vo.wait_until("The tarball holds that folder")
            r42 = out(self, t, OUT42, wrap=True, run_time=0.4)
            v.show(self, c4, anims=[FadeIn(c4, shift=DOWN * 0.15)], run_time=0.3)
            slashes = [self.one_slash(r) for r in r42 if self.one_slash(r) is not None]
            assert len(slashes) == len(OUT42), len(slashes)
            self.play(*[g.animate.set_color(TURN) for g in slashes], run_time=0.4)
            self.reseat()
            self.play(*[Indicate(g, color=TURN, scale_factor=1.3) for g in slashes], run_time=0.7)
            self.reseat()
            v.version_g = VGroup(c3, c4, tfs)
        self.wait(0.8)

        # ========================================================== 6. git status; the tarball in S3
        cost = cost_tag("the tarball in S3 · storage")

        with self.voiceover(SAY[6]) as vo:
            v.drop(self, *v.version_g, run_time=0.4)
            v.version_g = None
            self.wipe()
            resize(self, t, 8, extra=[tg.animate.shift(DOWN * 1 * t.pitch) for tg in self.bar_tags], run_time=0.4)
            type_cmd(self, t, C44.cmd, type_time=1.2)
            r44 = out(self, t, [(OUT44[0], TURN), (OUT44[1], TURN), (OUT44[2], S.GREY)], run_time=0.5)
            vo.wait_until("shows your two edits")
            pin(self, r44[1], beside(row_tag("your two edits", TURN), r44[1]))
            vo.wait_until("and Git ignores the artifacts folder")
            self.play(Indicate(substring(r44[2], ".gitignore:33:artifacts/"), color=S.GREY, scale_factor=1.1),
                      run_time=0.7)
            self.reseat()
            vo.wait_until("In your account")
            ln = type_cmd(self, t, AWS_LS, type_time=0.8)
            # the bracket-free bucket fills its row, so the chip takes the row below (where output
            # would be): the oldest row scrolls off, and the chip rides with the command's last row
            room(self, t, 1)
            last = ln.rows[-1] if hasattr(ln, "rows") else ln
            ls_tag = row_tag("extra · README A:187 · your bucket name · needs your account · no output shown")
            ls_tag.next_to(last, DOWN, buff=0, aligned_edge=LEFT)
            ls_tag.move_to([ls_tag.get_center()[0], last.get_center()[1] - t.pitch, 0])
            keep_inside(ls_tag)
            assert ls_tag.get_bottom()[1] > t.box.get_bottom()[1] and ls_tag.get_right()[0] < t.box.get_right()[0], ls_tag
            pin(self, ln, ls_tag)
            dot = pulse_dot(ROUTE, 0.11).move_to(v.nodes[4].frame.get_right())
            self.play(FadeIn(dot), run_time=0.2)
            self.play(dot.animate.move_to(v.nodes[5].frame.get_left()), run_time=0.6)
            self.play(FadeOut(dot), Indicate(v.nodes[5], color=CLOUD, scale_factor=1.06), run_time=0.5)
            v.heal(self)
            v.uri(self, run_time=0.5)
            keys = label("with your keys", 20, ROUTE).next_to(v.uri_text, LEFT, buff=0.25)
            keep_inside(keys)
            v.show(self, keys, run_time=0.3)
            cost.next_to(v.uri_text, DOWN, buff=0.18).align_to(v.uri_text, RIGHT)
            assert cost.get_bottom()[1] > t.box.get_top()[1] + 0.05, (cost.get_bottom(), t.box.get_top())
            vo.wait_until("and storage bills")
            self.play(FadeIn(cost, shift=DOWN * 0.1), run_time=0.4)
            flash_tag(self, cost)
        self.wait(1.0)

        self.play(FadeOut(t), FadeOut(v), FadeOut(cost), FadeOut(tr), *self.unbar_anims(), run_time=0.8)
        self.remove(t, v, cost, tr)
        self.wait(0.3)

    # ------------------------------------------------------------------ helpers
    def lit(self, body, k, run_time: float = 0.3):
        """The README bullet k lights YELLOW (the others back to WHITE); k=None: all WHITE."""
        anims = [r.animate.set_color(TURN if i == k else INK) for i, r in enumerate(body) if i]
        self.play(*anims, run_time=run_time)

    @staticmethod
    def block(c, a: int, b: int, color, opacity: float) -> Rectangle:
        """A translucent bar over lines a..b (0-based) of a code block."""
        top = c.code_lines[a].get_top()[1] + 0.07
        bot = c.code_lines[b].get_bottom()[1] - 0.07
        bg = c.background
        return Rectangle(width=bg.width - 0.12, height=top - bot, stroke_width=0) \
            .set_fill(color, opacity).move_to([bg.get_center()[0], (top + bot) / 2, 0])

    @staticmethod
    def one_slash(row):
        """The '1/' path prefix of a tar listing row (a wrapped row starts with it), or None."""
        s = row.text
        i = 0 if s.startswith("1/") else (s.index(" 1/") + 1 if " 1/" in s else -1)
        return glyph_range(row, i, i + 2) if i >= 0 else None

    def bar(self, tg):
        """Show a title-bar tag (on_bar) and remember it, so it fades with the terminal."""
        self.play(FadeIn(tg), run_time=0.3)
        self.bar_tags.append(tg)

    def unbar_anims(self):
        tgs, self.bar_tags = self.bar_tags, []
        return [FadeOut(tg) for tg in tgs]

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

    def paint(self, row, sub, color, run_time: float = 0.4):
        self.play(substring(row, sub).animate.set_color(color), run_time=run_time)
        self.reseat()
