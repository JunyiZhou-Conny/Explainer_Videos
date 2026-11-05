"""S12 · Train locally, sign the model (README B › Model Training steps 1-5, one extra, the V3 right
pipe redrawn compact, lecture slides 14 and 37).

Beats (script.md "## S12", one voiceover block each):
 0  TRACKER B4 1 (tracker appears). A 12-row laptop terminal (20 pt) at the data-processor prompt:
    `cd ../model-training` (GREY chip "exit the container first · this runs on your laptop") -> the
    prompt changes; `sh docker-shell.sh` -> TERM(laptop/70: 53) RED; TRACKER B4 1 · extra: the swap
    sed (extra; soft-wrapped) -> TERM(laptop/71: 3-5); `sh docker-shell.sh` -> TERM(laptop/73: 16
    squeezed, 22-23), line 16 GREEN, GREEN chip "from its committed lock · sagemaker 2.250.0 · no pin
    needed" (laptop/73:29); the prompt becomes (app) app@<id>:/app$.
 1  TRACKER B4 2. The training command (folds; the bucket value ringed YELLOW, row tag "your
    bucket") -> TERM(laptop/73: 95, 99 cut, 103, …, 110, 117, 119, …, 132 cut, 134); the Keras table
    rows re-aligned to fit; 95 + "at the time of recording"; 103 PINK + "← through the shared folder";
    119's (None, 3) RED; GREY chip "one epoch on 32 photos · not a result". ▶ your turn on the bar.
 2  TERM(laptop/73: …, 142-143, 146): 146 PermissionError RED. Two YELLOW chips "fix A", "fix B"
    appear above the terminal, still empty.
 3  The terminal leaves. CODE(task.py: 66-69): line 68 RED, `3` turns into a GREEN `4` on "Change
    it to 4"; tag erratum; chip "fix A" moves beside it. Under it: the four label folders
    (parmigiano, gruyere, brie, gouda) with arrows to the output bars of dense_1 (None, 3): three
    bars, gouda's slot a RED dashed stub; after the fix, (None, 4) and a fourth GREEN bar.
 4  TERM(laptop/61: 9) as a one-line strip (root root … persistent-folder ORANGE); under it the
    ORANGE root-owned folder, a RED lock, the TEAL container with its badge "app · uid 1000"
    (laptop/73:13); tag erratum, chip "fix B". On "Exit": the picture leaves, the fix B card (create
    the folder yourself · or sudo chown … · uid 1000 · Docker Desktop on a Mac: not needed) and a
    5-row host strip: `sudo chown -R $USER ../../../persistent-folder`, `sh docker-shell.sh`, the
    container prompt and the step 2 command again; GREY chip "after the fixes · not captured";
    ▶ your turn on the bar. "Docker Desktop on a Mac" lights the card's last line.
 5  CODE(task.py: 303-312): line 310 GREEN, line 307 BLUE; GREY chip "the save after the fixes was
    not captured". PINK arrows: line 310 -> a GREY laptop folder persistent-folder/model/1, line 307
    -> a BLUE training-job box (SM_MODEL_DIR/1). GREY dashed caption with the expected end state.
 6  LECTURE 15 · 14. The right pipe, redrawn compact (set pieces are never scaled): JPEG bytes ->
    the model with decode_jpeg → float32 → resize inside, serving_default (callout 3). The code grows
    out of it: CODE(task.py: 277-281) (callout 1 "define preprocessing"; the three lines light with
    the three gears) + CODE(task.py: 292-294) (callout 2 "new signature: a batch of strings"). On "A
    small slip" picture and tag leave; README card (README.md · line 7, chip B) "Model Deploy: Updates
    the model signature …", "Model Deploy" struck, a GREY arrow re-pointed to "Model Training"; tag
    erratum.
 7  TRACKER B4 3. CODE(package-trainer.sh: 1-4), line 4 PINK; a 6-row terminal types `sh
    package-trainer.sh` -> TERM(laptop/73: 150-156, 157 to "(InvalidAccessKeyId)" wrap), 157 RED.
    YELLOW chip "after fix A · the tarball carries it", GOLD cost tag "trainer tarball in S3".
 8  TRACKER B4 4. LECTURE 15 · 37: duty card "Model Training · train, save the model" + GREY chip
    "the AWS trainer also signs the model"; `python cli.py --train` -> TERM(laptop/73: 163, …,
    313-314) RED. On "With keys": terminal, card and tag leave; CODE(cli.py: 53-60, dedented, line 55
    cut) with instance_type / framework_version / py_version lit, a BLUE training-job glyph; CODE(
    cli.py: 74) with wait=False YELLOW + chip "returns at once"; GOLD cost tag "training job ·
    ml.m5.xlarge · while it runs".
 9  TRACKER B4 5. CONSOLE("Training jobs", B:141-145), path "SageMaker AI › Training": one row
    cheese-… with a GREY-dashed "InProgress" chip; illustration tag. Fade to empty.
"""

import re

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S12"]
SIZE = 20                                     # terminal font: 72 characters a row
TASK = "B/src/model-training/package/trainer/task.py"
CLI = "B/src/model-training/cli.py"

# ------------------------------------------------------------------ the real sources (checked)
C61, C70, C71, C73 = (capture(n) for n in ("61", "70", "71", "73"))
assert C70.cmd == "sh docker-shell.sh" == C73.cmd
assert C70.line(53) == "#6 0.116 exec /bin/sh: exec format error"
assert C71.cmd.startswith("sed -i -e 's|^docker build -t $IMAGE_NAME --platform=linux/arm64/v8")
OUT71 = C71.at((3, 5))
assert OUT71[0] == "docker build -t $IMAGE_NAME -f Dockerfile ." and all(len(s) <= 72 for s in OUT71)


def squeeze(s: str) -> str:
    """Runs of padding spaces (BuildKit's right-aligned timings, ls's columns) squeezed to two."""
    return re.sub(r" {3,}", "  ", s.rstrip())


def realign(rows):
    """The Keras summary rows re-aligned with narrower columns (same cells, same borders)."""
    cells = [[c.strip() for c in re.split(r"[┃│]", r)[1:-1]] for r in rows]
    ws = [max(len(r[k]) for r in cells) for k in range(len(cells[0]))]
    outr = []
    for raw, r in zip(rows, cells):
        bar = raw[0]
        parts = [r[0].ljust(ws[0]), r[1].ljust(ws[1]), r[2].rjust(ws[2])]
        outr.append(bar + " " + f" {bar} ".join(parts) + " " + bar)
    return outr


L16 = squeeze(C73.line(16))
assert L16 == " => CACHED [6/7] RUN pipenv sync  0.0s", L16
assert C73.line(29) == "sagemaker                 2.250.0"
assert C73.line(22) == "Container is running!!!"
assert '-u 1000' in C73.line(13)
TRAIN = C73.typed(48)
assert TRAIN == "python -m package.trainer.task --epochs=1 --batch_size=4 --bucket_name=cheese-app-ml-workflow-demo"
assert C73.line(95) == "tensorflow version 2.20.0"
assert C73.line(103) == "TFRecords found at /persistent/dataset/tfrecords"
TABLE = realign([C73.line(110), C73.line(117), C73.line(119)])
assert all(len(s) <= 72 for s in TABLE) and "(None, 3)" in TABLE[2], TABLE
L99 = cut(C73.line(99), n=72)
L132 = cut(C73.line(132), n=72)
assert L132.startswith("8/8") and "accuracy: 0.4062" in L132
assert C73.line(134) == "Change model signature and save"
assert C73.line(146) == "PermissionError: [Errno 13] Permission denied: '/persistent/model'"
OUT_SAVE = [C73.line(142), C73.line(143), (C73.line(146), ERR)]
L61 = squeeze(C61.line(9))
assert L61 == "drwxr-sr-x  3 root  root  4096 Nov  5 05:12 persistent-folder", L61
PKG = C73.typed(149)
assert PKG == "sh package-trainer.sh"
OUT_PKG = C73.at((150, 156))
assert OUT_PKG[0] == "package/" and OUT_PKG[-1] == "package/PKG-INFO"
ERR157 = cut(C73.line(157), "(InvalidAccessKeyId)")
assert ERR157.startswith("upload failed: ./trainer.tar.gz to s3://") and ERR157.endswith("(InvalidAccessKeyId)…")
TRAIN_CLI = C73.typed(160)
assert TRAIN_CLI == "python cli.py --train" and C73.line(163) == "Train Model"
ERR313 = C73.line(313)
assert ERR313.startswith("RuntimeError: Unable to derive SageMaker execution role")
assert C73.line(314) == "in your AWS account."
CHOWN = "sudo chown -R $USER ../../../persistent-folder"

assert excerpt(TASK, 68, 68) == "num_classes = 3"
assert excerpt(TASK, 310, 310).strip() == 'ARTIFACT_URI = os.path.join("/persistent", "model", "1")'
assert excerpt(TASK, 307, 307).strip().startswith('ARTIFACT_URI = os.path.join(sm_model_dir, "1")')
assert "decode_jpeg" in excerpt(TASK, 278, 278) and "resize" in excerpt(TASK, 280, 280)
assert excerpt(TASK, 292, 292).startswith("@tf.function(input_signature=[tf.TensorSpec([None], tf.string)])")
assert excerpt(TASK, 317, 317).strip() == 'signatures={"serving_default": serving_function},'
assert excerpt("B/src/model-training/package-trainer.sh", 4, 4).startswith("aws s3 cp trainer.tar.gz")
assert 'instance_type="ml.m5.xlarge"' in excerpt(CLI, 58, 58) and "wait=False" in excerpt(CLI, 74, 74)
README7 = readme(7, "B")
assert README7.startswith("* Model Deploy: Updates the model signature with preprocessing logic,"), README7
assert LABELS == ("parmigiano", "gruyere", "brie", "gouda")


def fixed_tracker(key: str, step=None, extra=False) -> VGroup:
    """common.tracker() with its head put back above the dots (common.py's head arrange() centres
    it at y 0; the workaround of S01, S03-S11; requested fix in the report)."""
    tr = tracker(key, step, extra)
    tr.head.next_to(tr.dots, UP, buff=0.14, aligned_edge=LEFT)
    place_tracker(tr)
    assert tr.get_bottom()[1] >= TRACK_BOTTOM - 0.05, tr.get_bottom()
    return tr


def fix_chip(name: str) -> VGroup:
    """A YELLOW 'fix A' / 'fix B' chip (20 pt)."""
    return chip(name, TURN, size=20)


def lock_glyph(h: float = 0.62, color=ERR) -> VGroup:
    """A padlock: body + shackle (text-free)."""
    body = RoundedRectangle(width=h * 0.9, height=h * 0.62, corner_radius=0.06, stroke_color=color,
                            stroke_width=4).set_fill(color, 0.25)
    sh = Arc(radius=h * 0.27, start_angle=0, angle=PI, color=color, stroke_width=5)
    sh.next_to(body, UP, buff=-0.02)
    return VGroup(sh, body)


def callout(n: int, text: str, color, mono_text: bool = False) -> VGroup:
    """Slide 14's numbered call-outs, redrawn (S05's look, 20 pt): circled number + a short label."""
    c = Circle(radius=0.2, stroke_color=color, stroke_width=3).set_fill(S.BG, 1)
    d = label(str(n), 20, color).move_to(c)
    t = (mono(text, 20, color) if mono_text else label(text, 20, INK))
    g = VGroup(VGroup(c, d), t).arrange(RIGHT, buff=0.18)
    g.num, g.text = g[0], t
    return g


def h_bar(length: float, color, dashed: bool = False) -> VMobject:
    """One horizontal output bar (left-anchored at ORIGIN)."""
    if dashed:
        b = DashedVMobject(Rectangle(width=length, height=0.32), num_dashes=14).set_stroke(color, 3)
    else:
        b = Rectangle(width=length, height=0.32, stroke_color=color, stroke_width=2).set_fill(color, 0.6)
    return b.move_to([length / 2, 0, 0])


class TrainLocally(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S12"] == 10, len(SAY)
        self.bar_tags = []

        # ========================================================== 0. step 1: arm64 again, same swap
        tr = fixed_tracker("B4", 1)
        t = term(P_SRC("data-processor"), rows=12, size=SIZE)
        self.t = t
        exit_c = grey_chip("exit the container first · this runs on your laptop")
        under_term(t, exit_c)
        lock_c = ok_chip("from its committed lock · sagemaker 2.250.0 · no pin needed")
        under_term(t, lock_c)
        for c in (exit_c, lock_c):
            assert c.get_left()[0] > tr.get_right()[0] + 0.2 and c.get_top()[1] < 3.55, (c.get_left(), tr.get_right())

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.2), FadeIn(t), FadeIn(exit_c, shift=DOWN * 0.1), run_time=0.6)
            type_cmd(self, t, "cd ../model-training", type_time=0.5, soft=True)
            cd_prompt(self, t, P_SRC("model-training"), run_time=0.4)
            type_cmd(self, t, C70.cmd, type_time=0.4)
            vo.wait_until("Same A R M 64 line")
            r70 = out(self, t, [(C70.line(53), ERR)], run_time=0.4)
            self.play(Indicate(substring(r70[0], "exec format error"), color=ERR, scale_factor=1.1), run_time=0.5)
            self.reseat()
            vo.wait_until("same swap")
            self.play(FadeOut(exit_c), track(tr, 1, True), run_time=0.3)
            type_cmd(self, t, C71.cmd, type_time=0.8, soft=True)
            self.bar(on_bar(t, extra_row()))
            r71 = out(self, t, [(OUT71[0], OWN), OUT71[1], OUT71[2]], run_time=0.4)
            vo.wait_until("This image installs from its committed lock")
            self.play(track(tr, 1), *self.unbar_anims(), run_time=0.3)
            type_cmd(self, t, C73.cmd, type_time=0.4)
            r73 = out(self, t, [(L16, OWN), C73.line(22), C73.line(23)], run_time=0.5)
            self.play(Indicate(substring(r73[0], "RUN pipenv sync"), color=OWN, scale_factor=1.1), run_time=0.5)
            self.reseat()
            vo.wait_until("with SageMaker version 2")
            self.play(FadeIn(lock_c, shift=DOWN * 0.1), run_time=0.4)
            self.play(Indicate(lock_c.text if hasattr(lock_c, "text") else lock_c, color=OWN, scale_factor=1.04),
                      run_time=0.6)
            vo.wait_until("so it needs no pin")
            cd_prompt(self, t, P_APP, color=TURN, run_time=0.5)

        # ========================================================== 1. step 2: local training
        epoch_c = grey_chip("one epoch on 32 photos · not a result")
        under_term(t, epoch_c)
        yt1 = on_bar(t, turn_row())

        with self.voiceover(SAY[1]) as vo:
            self.wipe(FadeOut(lock_c), track(tr, 2))
            cmd = type_cmd(self, t, TRAIN, type_time=1.4)
            self.bar(yt1)
            row_b = [r for r in rows_of(cmd) if BUCKET_B in r.text][0]
            bk = substring(row_b, BUCKET_B)
            rg = ring(bk, TURN)
            yb = beside(row_tag("your bucket", TURN), row_b, buff=0.3)
            self.play(Create(rg), FadeIn(yb, shift=LEFT * 0.1), run_time=0.5)
            attach(self, row_b, rg)
            attach(self, row_b, yb)
            self.reseat()
            vo.wait_until("TensorFlow 2.20 on the CPU")
            r95 = out(self, t, [C73.line(95), L99], run_time=0.4)
            pin(self, r95[0], beside(time_row(), r95[0], buff=0.3))
            vo.wait_until("finds the TFRecords from the processor")
            r103 = out(self, t, [(C73.line(103), ROUTE)], run_time=0.3)
            vo.wait_until("through the shared folder")
            sf = beside(row_tag("← through the shared folder", ROUTE), r103[0], buff=0.25)
            pin(self, r103[0], sf)
            vo.wait_until("Look at the last layer")
            rt = out(self, t, ["…", TABLE[0], TABLE[1], TABLE[2]], run_time=0.6)
            vo.wait_until("three outputs")
            self.paint(rt[3], "(None, 3)", ERR)
            self.play(Indicate(substring(rt[3], "(None, 3)"), color=ERR, scale_factor=1.15), run_time=0.6)
            self.reseat()
            vo.wait_until("One epoch runs")
            r132 = out(self, t, ["…", L132, C73.line(134)], run_time=0.5)
            vo.wait_until("Its accuracy means nothing yet")
            self.play(FadeIn(epoch_c, shift=DOWN * 0.1), run_time=0.4)
            self.play(Indicate(substring(r132[1], "accuracy: 0.4062"), color=TURN, scale_factor=1.08), run_time=0.7)
            self.reseat()

        # ========================================================== 2. saving fails; two fixes
        fa = fix_chip("fix A")
        fb = fix_chip("fix B")
        VGroup(fa, fb).arrange(RIGHT, buff=0.3)
        under_term(t, VGroup(fa, fb))

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(epoch_c), run_time=0.3)
            r146 = out(self, t, ["…"] + OUT_SAVE, run_time=0.6)
            vo.wait_until("permission denied")
            self.play(Indicate(substring(r146[3], "Permission denied: '/persistent/model'"), color=ERR,
                               scale_factor=1.08), run_time=0.8)
            self.reseat()
            vo.wait_until("Pause here for two small fixes")
            self.play(FadeIn(fa, shift=DOWN * 0.1), run_time=0.4)
            self.play(FadeIn(fb, shift=DOWN * 0.1), run_time=0.4)
            self.play(Indicate(VGroup(fa, fb), color=TURN, scale_factor=1.1), run_time=0.6)

        # ========================================================== 3. fix A: num_classes = 3 -> 4
        p68 = code(TASK, 66, 69)
        p68.move_to([-6.45 + p68.width / 2, 2.78 - p68.height / 2, 0])
        er68 = erratum_tag()
        fa2 = fix_chip("fix A")
        VGroup(fa2, er68).arrange(RIGHT, buff=0.3).next_to(p68, DOWN, buff=0.18).align_to(p68, RIGHT)
        folders = VGroup()
        for name in LABELS:
            fi = folder_icon(0.36, LAPTOP)
            nm = mono(name, 20, INK).next_to(fi, RIGHT, buff=0.18)
            folders.add(VGroup(fi, nm))
        folders.arrange(DOWN, buff=0.36, aligned_edge=LEFT)
        folders.move_to([-6.2 + folders.width / 2, -1.8, 0])
        f_head = label("label folders · 4", 20, S.GREY).next_to(folders, UP, buff=0.22).align_to(folders, LEFT)
        x0 = 1.2
        lens = (1.6, 1.1, 0.8)
        bars3 = VGroup(*[h_bar(L_, OWN).move_to([x0 + L_ / 2, folders[k].get_center()[1], 0])
                         for k, L_ in enumerate(lens)])
        stub = h_bar(1.2, ERR, dashed=True).move_to([x0 + 0.6, folders[3].get_center()[1], 0])
        nox = cross_glyph(0.26).next_to(stub, RIGHT, buff=0.2)
        b4 = h_bar(1.0, OWN).move_to([x0 + 0.5, folders[3].get_center()[1], 0])
        o_head = mono("dense_1 · (None, 3)", 20, ERR).next_to(bars3, UP, buff=0.22).align_to(bars3, LEFT)
        o_head4 = mono("dense_1 · (None, 4)", 20, OWN).move_to(o_head, aligned_edge=LEFT)
        o_head.align_to(f_head, DOWN)
        o_head4.align_to(f_head, DOWN)
        arrs = VGroup(*[Arrow(folders[k].get_right() + RIGHT * 0.15, [x0 - 0.15, folders[k].get_center()[1], 0],
                              buff=0, color=S.GREY, stroke_width=3, tip_length=0.16) for k in range(4)])
        arrs[3].set_color(ERR)
        pic3 = VGroup(folders, f_head, bars3, stub, nox, o_head, arrs)
        assert pic3.get_top()[1] < fa2.get_bottom()[1] - 0.1 and pic3.get_bottom()[1] > -3.5, \
            (pic3.get_top(), fa2.get_bottom(), pic3.get_bottom())

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(t), *self.unbar_anims(), FadeOut(fb), run_time=0.5)
            self.remove(t)
            self.play(FadeIn(p68, shift=DOWN * 0.2), ReplacementTransform(fa, fa2), run_time=0.6)
            b68 = line_bar(p68.code, 2, ERR, 0.25)
            self.play(FadeIn(b68), FadeIn(er68, shift=LEFT * 0.1), run_time=0.4)
            self.play(Indicate(code_span(p68.code, 2, "3"), color=ERR, scale_factor=1.4), run_time=0.6)
            self.add(p68, b68)
            vo.wait_until("while the data has four labels")
            self.play(FadeIn(f_head), LaggedStart(*[FadeIn(f, shift=RIGHT * 0.1) for f in folders], lag_ratio=0.15),
                      run_time=0.8)
            self.play(FadeIn(o_head), LaggedStart(*[GrowArrow(a) for a in arrs[:3]], lag_ratio=0.1),
                      LaggedStart(*[GrowFromEdge(b, LEFT) for b in bars3], lag_ratio=0.1), run_time=0.8)
            vo.wait_until("so gouda gets no target")
            self.play(GrowArrow(arrs[3]), Create(stub), FadeIn(nox), folders[3][1].animate.set_color(ERR), run_time=0.6)
            self.play(Indicate(folders[3], color=ERR, scale_factor=1.1), run_time=0.6)
            vo.wait_until("Change it to 4")
            three = code_span(p68.code, 2, "3")
            four = mono("4", 22, OWN).move_to(three)
            b68g = line_bar(p68.code, 2, OWN, 0.25)
            self.play(ReplacementTransform(three, four), ReplacementTransform(b68, b68g), run_time=0.5)
            self.add(p68, b68g, four)
            self.play(ReplacementTransform(o_head, o_head4), FadeOut(stub), FadeOut(nox),
                      arrs[3].animate.set_color(S.GREY), folders[3][1].animate.set_color(INK),
                      GrowFromEdge(b4, LEFT), run_time=0.7)

        # ========================================================== 4. fix B: the root-owned folder
        s61 = term(P_SRC("data-collector"), rows=1, size=SIZE, place=False)
        s61.move_to([0, 2.15, 0])
        lockg = lock_glyph()
        f_root = VGroup(folder_icon(0.6, SHARED), mono("persistent-folder", 20, SHARED),
                        label("owner: root", 20, SHARED)).arrange(DOWN, buff=0.12)
        box_c = outline_box(4.2, 1.7, IMAGE, solid=True, fill_opacity=0.08)
        name_c = mono("cheese-app-training-cli", 20, IMAGE).move_to(box_c.get_top() + DOWN * 0.32)
        badge = chip("app · uid 1000", IMAGE, size=20).move_to(box_c.get_center() + DOWN * 0.25)
        cont = VGroup(box_c, name_c, badge)
        row4 = VGroup(f_root, lockg, cont).arrange(RIGHT, buff=1.0).move_to([0, 0.15, 0])
        er4 = erratum_tag()
        fb2 = fix_chip("fix B")
        VGroup(fb2, er4).arrange(RIGHT, buff=0.3).next_to(row4, DOWN, buff=0.3).align_to(row4, RIGHT)
        h = term(P_SRC("model-training"), rows=5, size=SIZE)
        assert row4.get_top()[1] < s61.box.get_bottom()[1] - 0.1, (row4.get_top(), s61.box.get_bottom())
        assert VGroup(fb2, er4).get_bottom()[1] > -3.4
        mac = label("Docker Desktop on a Mac: not needed", 20, S.GREY)
        card_b = card([
            VGroup(label("create", 20, INK), mono("persistent-folder", 20, INK),
                   label("yourself before the first", 20, INK), mono("docker-shell.sh", 20, INK)).arrange(RIGHT, buff=0.12),
            VGroup(label("or", 20, INK), mono(CHOWN, 20, INK)).arrange(RIGHT, buff=0.16),
            VGroup(label("works when your uid is 1000", 20, INK), mono("(id -u)", 20, INK)).arrange(RIGHT, buff=0.12),
            mac,
        ], color=TURN, head="fix B · on your laptop", size=20, buff=0.14)
        card_b.move_to([0, 1.15, 0])
        nc = grey_chip("after the fixes · not captured")
        under_term(h, nc)
        assert card_b.get_bottom()[1] > nc.get_top()[1] + 0.05 and card_b.get_top()[1] < PIC_TOP, \
            (card_b.get_bottom(), nc.get_top(), card_b.get_top())

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(p68, b68g, four, fa2, er68, pic3, b4, o_head4)), run_time=0.5)
            self.play(FadeIn(s61), run_time=0.4)
            r61 = out(self, s61, [L61], run_time=0.3)
            self.play(*[g.animate.set_color(SHARED) for g in (substring(r61[0], "root  root"),
                                                              substring(r61[0], "persistent-folder"))], run_time=0.4)
            self.add(s61)
            self.play(FadeIn(f_root, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("and this container runs as the app user")
            self.play(FadeIn(cont, shift=LEFT * 0.15), run_time=0.5)
            self.play(Indicate(badge, color=IMAGE, scale_factor=1.12), run_time=0.5)
            self.play(FadeIn(lockg, scale=0.6), FadeIn(fb2), FadeIn(er4, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("Exit, and on your laptop")
            self.play(FadeOut(VGroup(s61, row4, er4)), ReplacementTransform(fb2, card_b), run_time=0.6)
            self.play(FadeIn(h), run_time=0.4)
            self.t = h
            type_cmd(self, h, CHOWN, type_time=0.9, soft=True)
            vo.wait_until("or change its owner")
            self.play(Indicate(card_b.body[1], color=TURN, scale_factor=1.05), run_time=0.6)
            vo.wait_until("Then run step 2 again")
            type_cmd(self, h, C73.cmd, type_time=0.4)
            self.play(FadeIn(nc, shift=DOWN * 0.1), run_time=0.3)
            cd_prompt(self, h, P_APP, color=TURN, run_time=0.4)
            type_cmd(self, h, TRAIN, type_time=1.0)
            self.bar(on_bar(h, turn_row()))
            vo.wait_until("Docker Desktop on a Mac avoids this")
            self.play(mac.animate.set_color(INK), run_time=0.3)
            self.play(Indicate(mac, color=TURN, scale_factor=1.06), run_time=0.7)

        # ========================================================== 5. where the save would go
        p303 = code(TASK, 303, 312, font_size=20, cuts={303: "versioned directory", 307: '"1")'})
        p303.move_to([-6.45 + p303.width / 2, 2.78 - p303.height / 2, 0])
        nsave = grey_chip("the save after the fixes was not captured")
        nsave.move_to([6.5 - nsave.width / 2, 3.2, 0])
        assert nsave.get_left()[0] > tr.get_right()[0] + 0.2, (nsave.get_left(), tr.get_right())
        lap_f = VGroup(folder_icon(0.5, LAPTOP), mono("persistent-folder/model/1", 20, LAPTOP)).arrange(RIGHT, buff=0.2)
        lap_t = label("your laptop", 20, LAPTOP)
        lap = VGroup(lap_f, lap_t).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        lap.move_to([-0.2, -2.3, 0])
        job_b = outline_box(2.9, 1.05, CLOUD, solid=True, fill_opacity=0.1)
        job_t = VGroup(label("training job", 20, CLOUD), mono("SM_MODEL_DIR/1", 20, INK)).arrange(DOWN, buff=0.08)
        job_t.move_to(job_b)
        job = VGroup(job_b, job_t).move_to([4.95, -2.3, 0])
        expect = dashed_chip("expected: ls -laR /persistent/model → a 1/ folder with saved_model.pb")
        expect.move_to([0, -3.25, 0])
        assert lap.get_top()[1] < p303.get_bottom()[1] - 0.3 and expect.get_top()[1] < lap.get_bottom()[1] + 0.02, \
            (lap.get_top(), p303.get_bottom(), expect.get_top(), lap.get_bottom())
        assert job.get_top()[1] < p303.get_bottom()[1] - 0.3 and expect.width < 12.9, expect.width

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(card_b, nc)), FadeOut(h), *self.unbar_anims(), run_time=0.5)
            self.remove(h)
            self.play(FadeIn(p303, shift=DOWN * 0.2), FadeIn(nsave, shift=DOWN * 0.1), run_time=0.6)
            b310 = line_bar(p303.code, 7, OWN, 0.25)
            b307 = line_bar(p303.code, 4, CLOUD, 0.25)
            vo.wait_until("the persistent folder on your laptop")
            self.play(FadeIn(b310), code_span(p303.code, 7, '"/persistent", "model", "1"').animate.set_color(OWN),
                      run_time=0.4)
            self.add(p303, b310)
            x_r = p303.get_right()[0] + 0.12
            a310 = route(np.array([x_r, p303.code.code_lines[7].get_center()[1], 0]),
                         lap_f.get_top() + UP * 0.08 + RIGHT * 1.2, arc=-0.6)
            self.play(Create(a310), run_time=0.6)
            self.play(FadeIn(lap, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("or the SageMaker model folder inside a training job")
            self.play(FadeIn(b307), run_time=0.3)
            a307 = route(np.array([x_r, p303.code.code_lines[4].get_center()[1], 0]),
                         job_b.get_top() + UP * 0.08, arc=-0.5)
            self.play(Create(a307), run_time=0.6)
            self.play(FadeIn(job, shift=UP * 0.1), run_time=0.4)
            self.play(FadeIn(expect, shift=UP * 0.1), run_time=0.4)

        # ========================================================== 6. slide 14: the signature, in the trainer
        lt14 = lref("14")
        jp = VGroup(file_glyph(0.5, INK), label("JPEG bytes", 20, IMAGE)).arrange(DOWN, buff=0.08)
        ops = ("decode_jpeg", "float32", "resize")
        gears3 = [gear(0.17) for _ in ops]
        oplab = [mono(o, 20, TOOL) for o in ops]
        oprow = VGroup()
        for k in range(3):
            oprow.add(VGroup(gears3[k], oplab[k]).arrange(RIGHT, buff=0.12))
            if k < 2:
                oprow.add(label("→", 20, TOOL))
        oprow.arrange(RIGHT, buff=0.12)
        mbox = RoundedRectangle(width=oprow.width + 1.0, height=0.95, corner_radius=0.12, stroke_color=CLOUD,
                                stroke_width=3).set_fill(CLOUD, 0.1)
        oprow.move_to(mbox)
        door = RoundedRectangle(width=0.22, height=0.7, corner_radius=0.05, stroke_color=OWN,
                                stroke_width=3).set_fill(S.BG, 1).move_to(mbox.get_left() + RIGHT * 0.05)
        c3 = callout(3, "serving_default", OWN, mono_text=True)
        pipe = VGroup(jp, mbox, c3).arrange(RIGHT, buff=0.4)
        pipe.move_to([0, 1.95, 0])
        oprow.move_to(mbox).shift(RIGHT * 0.15)
        door.move_to(mbox.get_left() + RIGHT * 0.05)
        wire = Line(jp.get_right() + RIGHT * 0.1, door.get_left(), color=ROUTE, stroke_width=4)
        mlab = label("the model", 20, CLOUD).next_to(mbox, DOWN, buff=0.08).align_to(mbox, RIGHT)
        pic6 = VGroup(jp, wire, mbox, door, oprow, c3)
        assert pic6.get_top()[1] < PIC_TOP and pic6.get_right()[0] < 6.5 and pic6.get_left()[0] > -6.5, \
            (pic6.get_top(), pic6.get_left(), pic6.get_right())
        pA = code(TASK, 277, 281, font_size=20)
        pA.move_to([-6.45 + pA.width / 2, 1.2 - pA.height / 2, 0])
        pB = code(TASK, 292, 294, font_size=20)
        pB.move_to([-6.45 + pB.width / 2, pA.get_bottom()[1] - 0.15 - pB.height / 2, 0])
        assert pB.get_bottom()[1] > -3.5 and pA.get_top()[1] < pic6.get_bottom()[1] - 0.05 - 0.0 + 0.4, \
            (pB.get_bottom(), pA.get_top(), pic6.get_bottom())
        c1 = callout(1, "define preprocessing", TOOL)
        c1.move_to([pA.code.code_lines[0].get_right()[0] + 0.5 + c1.width / 2, pA.code.code_lines[0].get_center()[1], 0])
        c2 = callout(2, "new signature: a batch of strings", ROUTE)
        c2.move_to([pB.code.code_lines[1].get_right()[0] + 0.5 + c2.width / 2, pB.code.code_lines[1].get_center()[1], 0])
        assert c1.get_right()[0] < 6.5 and c2.get_right()[0] < 6.5, (c1.get_right(), c2.get_right())
        md = label("Model Deploy:", 22, INK)
        rc = readme_card(7, VGroup(
            VGroup(md, label("Updates the model signature with", 22, INK)).arrange(RIGHT, buff=0.14),
            label("preprocessing logic, then uploads the model …", 22, INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.12),
            repo="B")
        rc.move_to([0, 1.2, 0])
        er6 = erratum_tag().next_to(rc, RIGHT, buff=0.25).align_to(rc, UP)
        if er6.get_right()[0] > 6.5:
            er6.next_to(rc, UP, buff=0.15).align_to(rc, RIGHT)
        mt = ok_chip("Model Training · task.py")
        mt.move_to([max(-6.4 + mt.width / 2, md.get_center()[0]), -0.9, 0])
        assert er6.get_right()[0] < 6.5 and er6.get_top()[1] < PIC_TOP + 0.3

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(p303, b310, b307, a310, a307, lap, job, expect, nsave)), track(tr, 2), run_time=0.5)
            self.play(FadeIn(lt14, shift=LEFT * 0.1), FadeIn(jp), Create(wire), FadeIn(mbox), FadeIn(door),
                      run_time=0.6)
            self.play(LaggedStart(*[FadeIn(m) for m in oprow], lag_ratio=0.12), FadeIn(c3, shift=LEFT * 0.1),
                      run_time=0.7)
            vo.wait_until("decode, convert, resize")
            self.play(GrowFromPoint(pA, mbox.get_center()), run_time=0.5)
            self.play(FadeIn(c1, shift=LEFT * 0.1), run_time=0.3)
            for k, (ln, g) in enumerate(zip((1, 2, 3), gears3)):
                self.play(Indicate(pA.code.code_lines[ln], color=TURN, scale_factor=1.04),
                          Rotate(g, PI / 2), Indicate(oplab[k], color=TURN, scale_factor=1.12), run_time=0.45)
            self.add(pA)
            vo.wait_until("inside the model")
            self.play(GrowFromPoint(pB, mbox.get_center()), run_time=0.5)
            self.play(FadeIn(c2, shift=LEFT * 0.1),
                      code_span(pB.code, 0, "tf.string").animate.set_color(ROUTE), run_time=0.4)
            self.add(pB)
            self.play(Indicate(c3, color=OWN, scale_factor=1.1), door.animate.set_fill(OWN, 0.4), run_time=0.6)
            vo.wait_until("A small slip")
            self.play(FadeOut(VGroup(jp, wire, mbox, door, oprow, c3, pA, pB, c1, c2)), FadeOut(lt14), run_time=0.5)
            self.play(FadeIn(rc, shift=DOWN * 0.2), FadeIn(er6, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("the README gives this job to model deploy")
            sk = strike(md)
            self.play(Indicate(md, color=ERR, scale_factor=1.1), run_time=0.5)
            self.play(Create(sk), run_time=0.4)
            vo.wait_until("The trainer does it")
            ar6 = arrow(np.array([md.get_center()[0], rc.get_bottom()[1], 0]), mt.get_top(), color=S.GREY)
            self.play(GrowArrow(ar6), FadeIn(mt, shift=UP * 0.1), run_time=0.6)
            self.play(Indicate(mt, color=OWN, scale_factor=1.08), run_time=0.6)

        # ========================================================== 7. step 3: package the trainer
        pk = code("B/src/model-training/package-trainer.sh", 1, 4, font_size=20)
        pk.move_to([-6.45 + pk.width / 2, 2.78 - pk.height / 2, 0])
        t = term(P_APP, rows=7, size=SIZE)
        afa = chip("after fix A · the tarball carries it", TURN, size=20)
        ct7 = cost_tag("trainer tarball in S3")
        VGroup(ct7, afa).arrange(RIGHT, buff=0.35)
        under_term(t, VGroup(ct7, afa), buff=0.05)
        assert VGroup(ct7, afa).get_top()[1] < pk.get_bottom()[1] - 0.05, (VGroup(ct7, afa).get_top(), pk.get_bottom())

        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(rc, er6, sk, ar6, mt)), track(tr, 3), run_time=0.5)
            self.t = t
            self.play(FadeIn(t), FadeIn(pk, shift=DOWN * 0.2), run_time=0.5)
            type_cmd(self, t, PKG, type_time=0.5)
            vo.wait_until("packs the package folder")
            pk_bars = VGroup(line_bar(pk.code, 1, TOOL, 0.22), line_bar(pk.code, 2, TOOL, 0.22))
            self.play(FadeIn(pk_bars), run_time=0.3)
            out(self, t, OUT_PKG, run_time=0.8, lag=0.1)
            vo.wait_until("and copies it to S3")
            self.play(code_span(pk.code, 3, "$S3_PACKAGE_URI/cheese-app-trainer.tar.gz").animate.set_color(ROUTE),
                      FadeIn(ct7, shift=DOWN * 0.1), run_time=0.5)
            self.add(pk, pk_bars)
            vo.wait_until("The tar file is real")
            self.play(FadeIn(afa, shift=DOWN * 0.1), run_time=0.4)
            self.play(Indicate(afa, color=TURN, scale_factor=1.06), run_time=0.6)
            vo.wait_until("The upload fails on our fake key")
            r157 = out(self, t, [(ERR157, ERR)], wrap=True, run_time=0.5)
            hit = [r for r in r157 if "(InvalidAccessKeyId)" in r.text][0]
            self.play(Indicate(substring(hit, "(InvalidAccessKeyId)"), color=ERR, scale_factor=1.1), run_time=0.6)
            self.reseat()

        # ========================================================== 8. step 4: --train
        lt37 = lref("37")
        duty = duty_card([("Model Training · train, save the model", True)])
        duty.move_to([-6.45 + duty.width / 2, 1.85, 0])
        signs = grey_chip("the AWS trainer also signs the model").next_to(duty, DOWN, buff=0.25).align_to(duty, LEFT)
        t8 = term(P_APP, rows=7, size=SIZE)
        assert signs.get_bottom()[1] > t8.box.get_top()[1] + 0.1, (signs.get_bottom(), t8.box.get_top())
        c53 = code(CLI, 53, 60, font_size=20, dedent=True, cuts={55: 'source_dir=f"'})
        c53.move_to([-6.45 + c53.width / 2, 2.78 - c53.height / 2, 0])
        c74 = code(CLI, 74, 74, font_size=20, dedent=True)
        c74.move_to([-6.45 + c74.width / 2, c53.get_bottom()[1] - 0.2 - c74.height / 2, 0])
        rack_g = VGroup(rack(1.1), label("training job", 20, CLOUD))
        rack_g[1].next_to(rack_g[0], DOWN, buff=0.14)
        rack_g.move_to([(c53.get_right()[0] + 6.5) / 2, 1.2, 0])
        ret = chip("returns at once", TURN, size=20)
        ct8 = cost_tag("training job · ml.m5.xlarge · while it runs")
        ct8.move_to([-6.45 + ct8.width / 2, c74.get_bottom()[1] - 0.25 - ct8.height / 2, 0])
        ret.next_to(c74, DOWN, buff=0.25).align_to(c74, RIGHT)
        assert ct8.get_bottom()[1] > -3.5 and ret.get_left()[0] > ct8.get_right()[0] + 0.2, (ct8.get_bottom(), ret.get_left())
        assert rack_g.get_right()[0] < 6.5 and rack_g.get_left()[0] > c53.get_right()[0] + 0.2

        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(pk, pk_bars, ct7, afa)), FadeOut(t), track(tr, 4), run_time=0.5)
            self.remove(t)
            self.t = t = t8
            self.play(FadeIn(t), FadeIn(lt37), FadeIn(duty, shift=RIGHT * 0.2), run_time=0.6)
            self.play(FadeIn(signs, shift=UP * 0.1), run_time=0.4)
            type_cmd(self, t, TRAIN_CLI, type_time=0.5)
            vo.wait_until("It asks AWS who you are")
            out(self, t, [C73.line(163), "…"], run_time=0.4)
            vo.wait_until("and stops there")
            r313 = out(self, t, [(ERR313, ERR), (C73.line(314), ERR)], wrap=True, run_time=0.5)
            self.play(Indicate(substring(r313[0], "Unable to derive SageMaker execution role"), color=ERR,
                               scale_factor=1.06), run_time=0.6)
            self.reseat()
            vo.wait_until("With keys")
            self.play(FadeOut(t), FadeOut(VGroup(duty, signs)), FadeOut(lt37), run_time=0.5)
            self.remove(t)
            self.play(FadeIn(c53, shift=DOWN * 0.2), FadeIn(c74, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("it starts a training job")
            c53_bars = VGroup(*[line_bar(c53.code, k, COST, 0.22) for k in (5, 6, 7)])
            self.play(FadeIn(c53_bars),
                      FadeIn(rack_g, shift=LEFT * 0.1), FadeIn(ct8, shift=UP * 0.1), run_time=0.6)
            self.play(Indicate(code_span(c53.code, 5, '"ml.m5.xlarge"'), color=COST, scale_factor=1.12), run_time=0.6)
            self.add(c53, c53_bars)
            vo.wait_until("and returns at once")
            self.play(code_span(c74.code, 0, "wait=False").animate.set_color(TURN), FadeIn(ret, shift=UP * 0.1),
                      run_time=0.5)
            self.add(c74)
            self.play(Indicate(code_span(c74.code, 0, "wait=False"), color=TURN, scale_factor=1.15), run_time=0.6)
            self.add(c74)

        # ========================================================== 9. step 5: the console
        form = console_form("Training jobs", [("Name", "cheese-…"),
                                              ("note", "click the job name: details, logs, metrics")],
                            path="SageMaker AI › Training", form_w=8.6)
        form.move_to([0, 0.3, 0])
        st = dashed_chip("InProgress")
        st.move_to(form.rows[0].field.get_right() + LEFT * (st.width / 2 + 0.15))
        il = illustration_tag().next_to(form, UP, buff=0.15).align_to(form, RIGHT)
        assert form.get_top()[1] < PIC_TOP and il.get_top()[1] < 3.55 and il.get_left()[0] > tr.get_right()[0] + 0.1

        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(VGroup(c53, c53_bars, c74, rack_g, ct8, ret)), track(tr, 5), run_time=0.6)
            self.play(FadeIn(form, shift=UP * 0.2), FadeIn(il), run_time=0.6)
            vo.wait_until("under Training")
            self.play(Indicate(form.path_text, color=TURN, scale_factor=1.08), run_time=0.7)
            self.play(Indicate(form.title_text, color=TURN, scale_factor=1.08), run_time=0.6)
            vo.wait_until("Its name starts with cheese")
            self.play(Indicate(form.rows[0].value, color=TURN, scale_factor=1.15), FadeIn(st), run_time=0.7)

        self.play(FadeOut(VGroup(form, st, il)), FadeOut(tr), run_time=0.8)
        self.wait(0.3)

    # ------------------------------------------------------------------ helpers (S11's)
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
        self.add(self.t, *self.bar_tags)

    def paint(self, row, sub, color, run_time: float = 0.4):
        """Colour substring `sub` of terminal row `row`."""
        self.play(substring(row, sub).animate.set_color(color), run_time=run_time)
        self.reseat()
