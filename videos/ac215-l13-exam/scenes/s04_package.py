"""S04 · What the package carries (V2 "what pip unwraps": setup.py, the tarball, the prebuilt image,
and the ModuleNotFoundError of a team module that never travelled).
Lecture: 23–25.

Beats (script.md "## S04", one voiceover block each):
 0  LECTURE 23–24. Our redrawing of slides 23–24 as one strip: GREY notebook → GREEN "Python file ·
    arguments" (three flag chips push up into it) → GREEN tarball → BLUE bucket → BLUE job; GREY step
    badges 1, 2, 3 light YELLOW in turn.
 1  The strip becomes a compact flow at the top. The GREEN package/ tree (left) and
    CODE(package/setup.py: 1, 5, 7–13 folded; line 12 wrapped) (right); each named row flashes.
 2  Lines 5 and 10 light PURPLE: the pin peels off the panel into the "shopping list" card (under the
    tree). Line 11 lights PINK: the find_packages() scanner sweeps the tree; trainer/ turns bright
    GREEN, setup.cfg and PKG-INFO dim; __init__.py flashes.
 3  CODE(package-trainer.sh: 1–4) replaces the setup panel (the strip leaves). Line 2: the tree
    wraps into trainer.tar; line 3: it becomes trainer.tar.gz; line 4: it flies along a PINK path into
    the BLUE bucket labelled $GCS_BUCKET_URI/cheese-app-trainer.tar.gz. Then CODE(cli.sh: 10–11): the
    package path and "trainer.task" light PINK.
 4  The BLUE job VM (TEAL prebuilt image, ORANGE shelf); the bucket and a BLUE "Vertex AI" chip above
    it. Left, a GREY laptop with the TEAL model-training-cli box: arrows "package & upload" (to the
    bucket) and "submit" (to Vertex AI); a GREY dashed arrow to the VM is struck with a RED ✗.
    Excerpt chip cli.sh · line 31. The tarball drops from the bucket onto the VM's pip shelf.
 5  The rest leaves, the VM rises; the ORANGE shelf glows; GREY dashed links from scikit-learn and
    requests to excerpt chips task.py · line 17 / line 3; GREY note "not in setup.py · luck, not
    declaration".
 6  pip unwraps the tarball: the shopping list comes out, fetches wandb from the GREY PyPI cloud
    (PINK arrows, GREEN ✓); the tarball becomes the trainer chip (GREEN ✓). Schematic log line
    "Successfully installed cheese-app-trainer … wandb …" (illustration); then the
    `python -m trainer.task` chip lights.
 7  Rewind to the laptop: the tree and a GREY dashed augment.py beside package/ (illustration,
    example · not in the repo). Excerpt chip package-trainer.sh · line 2: a ring round package/
    only, the tree's copy wraps into a tarball and flies to the bucket; augment.py stays ("stays on
    your laptop"). Then the tree morphs so that augment.py sits beside setup.py: it rides in a new
    tarball, but the scanner lights only trainer/ (GREY note "uploaded ≠ installed").
 8  The VM again with both chips and the log line; schematic `import augment` lights; the PINK search
    beam sweeps the shelves and finds nothing (RED ✗); RED ModuleNotFoundError box right under the
    log line. GREY laptop inset: augment.py and `import augment` with a GREEN ✓.
 9  The fix (schematic, illustration): augment.py slides into trainer/, the scanner lights it GREEN;
    `from trainer import augment` + GREEN ✓; option chip `py_modules=["augment"]` "or, in
    setup(...)"; RED-struck `from somewhere import augment` "renaming the import: the file still
    isn't there".
10  RED-struck `install_requires=[..., "augment"]` "fetches from PyPI · not your file"; PINK arrow
    from the shopping list to the PyPI cloud, a GREY dashed one to the tarball struck RED.
11  Takeaway (YELLOW, centred), then an empty frame.

Deviations from SHOW: beat 1 wraps setup.py line 12 (the tree and an unwrapped panel do not fit
side by side); package-trainer.sh line 4 and cli.sh line 10 are wrapped before $GCS_BUCKET_URI for
the same reason. The scanner's find_packages() label stays fixed above the tree (beside the moving
bar it would run into the code panel). Beat 7's "inset" is the same laptop tree morphing so that
augment.py moves beside setup.py (one tree on screen at a time, ≤ 3 groups). The excerpt chips
are headed "task.py · line N (excerpt)" as SHOW writes them.
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
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
    LaggedStart,
    Line,
    ReplacementTransform,
    Transform,
    VGroup,
    VMobject,
    Write,
)

from common import *  # noqa: F401,F403
from common import guard
from explainer import style as S
from explainer.scene import VoiceScene

SAY = NARRATION["S04"]

# ------------------------------------------------------------------ the real sources
SETUP = "package/setup.py"
TASK = "package/trainer/task.py"
PTS = "package-trainer.sh"
CLI = "cli.sh"
assert source_line(SETUP, 5).strip() == 'REQUIRED_PACKAGES = ["wandb==0.15.11"]', source_line(SETUP, 5)
assert source_line(SETUP, 10).strip() == "install_requires=REQUIRED_PACKAGES,", source_line(SETUP, 10)
assert source_line(SETUP, 11).strip() == "packages=find_packages(),", source_line(SETUP, 11)
assert source_line(PTS, 2).strip() == "tar cvf trainer.tar package", source_line(PTS, 2)
assert source_line(PTS, 3).strip() == "gzip trainer.tar", source_line(PTS, 3)
assert source_line(PTS, 4).strip() == "gsutil cp trainer.tar.gz $GCS_BUCKET_URI/cheese-app-trainer.tar.gz"
assert source_line(CLI, 10).strip() == "export PYTHON_PACKAGE_URI=$GCS_BUCKET_URI/cheese-app-trainer.tar.gz"
assert source_line(CLI, 11).strip() == 'export PYTHON_MODULE="trainer.task"', source_line(CLI, 11)
assert IMAGE_CPU in source_line(CLI, 31), source_line(CLI, 31)
assert source_line(TASK, 3).strip() == "import requests", source_line(TASK, 3)
assert source_line(TASK, 17).startswith("from sklearn.model_selection"), source_line(TASK, 17)
assert "augment" not in source_text(SETUP) + source_text(TASK) + source_text(PTS)

SAFE = 6.6
TREE_IN = ("package/", "  setup.py", "  augment.py", "  setup.cfg", "  PKG-INFO", "  trainer/",
           "    __init__.py", "    task.py", "    task_multi_gpu.py")


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


def tile(title: str, sub: str | None, color: str, w: float, h: float = 1.25) -> VGroup:
    """One tile of the lecture strip: a rounded box, a 24 pt title, an optional GREY sub-line."""
    t = label(title, 24, INK)
    parts = [t]
    if sub:
        parts.append(label(sub, CAPTION, S.GREY))
    body = VGroup(*parts).arrange(DOWN, buff=0.1)
    fr = box(w, h, color, fill_opacity=0.1, radius=0.14, stroke=3)
    body.move_to(fr)
    g = VGroup(fr, body)
    g.frame = fr
    return g


def arrow(a, b, color=S.GREY, stroke: float = 3, buff: float = 0.08) -> Arrow:
    return Arrow(a, b, buff=buff, color=color, stroke_width=stroke, max_tip_length_to_length_ratio=0.25,
                 tip_length=0.16)


def dim_rows(tree, names, k: float = 0.4) -> list:
    """Animations that fade the named rows' text and glyph to k (no highlight box)."""
    out = []
    for n in names:
        r = tree.row(n)
        out += [g.animate.set_fill(opacity=k) for g in r.name_text.glyphs]
        out.append(r.glyph.animate.set_stroke(opacity=k))
    return out


def scanner_for(tree):
    """A Scanner whose bar spans the tree; its label is taken out and parked above the tree."""
    sc = Scanner(width=tree.width + 0.3)
    sc.remove(sc.label)
    lab = sc.label
    sc.set_x(tree.get_center()[0]).set_y(tree.get_top()[1] + 0.1)
    place(lab, left=tree.get_left()[0], bottom=tree.get_top()[1] + 0.12)
    return sc, lab


class WhatPipInstalls(VoiceScene):
    def construct(self):
        assert len(SAY) == 12, len(SAY)

        # ========================================================== 0 · slides 23–24 as one strip
        t_nb = tile("notebook", None, LAPTOP, 1.9)
        t_py = tile("Python file", "arguments", OWN, 2.3)
        t_tar = tarball("trainer.tar.gz")
        bk0 = bucket(None)
        t_bk = VGroup(bk0, label("bucket", CAPTION, CLOUD).next_to(bk0, DOWN, buff=0.12))
        t_job = tile("job", "Vertex AI", CLOUD, 1.8)
        tiles = [t_nb, t_py, t_tar, t_bk, t_job]
        strip = VGroup(*tiles).arrange(RIGHT, buff=0.62)
        place(strip, cx=0, cy=0.3)
        for t in (t_tar, t_bk):
            t.set_y(t_py.get_center()[1] + (t.get_center()[1] - (t[0].get_center()[1])))
        inside(strip)
        arrows0 = VGroup(*[arrow(a.get_right() * [1, 0, 0] + [0, t_py.get_center()[1], 0],
                                 b.get_left() * [1, 0, 0] + [0, t_py.get_center()[1], 0], OWN)
                           for a, b in zip(tiles, tiles[1:])])
        badge_x = [t_py.get_center()[0], (t_tar.get_center()[0] + t_bk.get_center()[0]) / 2, t_job.get_center()[0]]
        badges = [step_badge(n, S.GREY, radius=0.26).move_to([x, 1.75, 0]) for n, x in zip((1, 2, 3), badge_x)]
        lit = [step_badge(n, TURN, radius=0.26).move_to(b) for n, b in zip((1, 2, 3), badges)]
        flags = VGroup(*[chip(f, S.GREY, size=CAPTION, font=MONO) for f in ("--model_name", "--epochs", "--batch_size")])
        flags.arrange(DOWN, buff=0.14)
        place(flags, cx=t_py.get_center()[0], top=t_py.get_bottom()[1] - 0.45)
        inside(flags)
        lr = None
        with self.voiceover(SAY[0]) as vo:
            lr = lref_swap(self, lr, "23–24")
            self.play(LaggedStart(*[FadeIn(t, shift=RIGHT * 0.2) for t in tiles], lag_ratio=0.15),
                      LaggedStart(*[GrowArrow(a) for a in arrows0], lag_ratio=0.2), run_time=1.6)
            self.play(*[FadeIn(b) for b in badges], run_time=0.4)
            vo.wait_until("a Python file with arguments")
            self.play(Transform(badges[0], lit[0]), FadeIn(flags, shift=UP * 0.2), run_time=0.5)
            self.play(LaggedStart(*[FadeOut(f, shift=UP * (f.get_center()[1] - t_py.get_center()[1]))
                                    for f in flags], lag_ratio=0.2),
                      flash(t_py.frame, OWN, 1.05, 1.2), run_time=1.2)
            vo.wait_until("a package in a bucket")
            self.play(Transform(badges[1], lit[1]), flash(t_tar, OWN, 1.1), flash(t_bk, CLOUD, 1.1), run_time=0.7)
            vo.wait_until("and a training job")
            self.play(Transform(badges[2], lit[2]), flash(t_job, CLOUD, 1.1), run_time=0.7)

        # ========================================================== 1 · the package folder + setup.py
        fl = flow(["notebook", "Python file", "trainer.tar.gz", "bucket", "job"])
        place(fl, cx=0, cy=2.8)
        inside(fl)
        guard(fl.get_top()[1] < LREF_BOTTOM, "strip runs into the lecture tag")
        tree = PackageTree()
        place(tree, left=-6.4, top=2.0)
        inside(tree)
        setup = src_panel(SETUP, [1, 5, (7, 13)], wrap={12: ['"Cheese']})
        place(setup, right=6.45, top=2.0)
        inside(setup)
        apart(tree, setup, "tree runs into the setup panel")
        fl_arrows = [m for m in fl if m not in fl.items]
        with self.voiceover(SAY[1]) as vo:
            self.play(*[ReplacementTransform(t, c) for t, c in zip(tiles, fl.items)],
                      *[ReplacementTransform(a, b) for a, b in zip(arrows0, fl_arrows)],
                      *[FadeOut(b) for b in badges], run_time=1.0)
            self.play(fl.light(2), FadeIn(tree, shift=RIGHT * 0.3), run_time=0.7)
            vo.wait_until("setup dot py")
            self.play(FadeIn(setup, shift=LEFT * 0.3), flash(tree.row("setup.py").name_text, OWN), run_time=0.7)
            vo.wait_until("and a trainer folder")
            self.play(flash(tree.row("trainer/"), OWN, 1.1), run_time=0.6)
            vo.wait_until("an empty init file")
            self.play(flash(tree.row("__init__.py"), INK, 1.1), run_time=0.6)
            vo.wait_until("the two training scripts")
            self.play(flash(VGroup(tree.row("task.py"), tree.row("task_multi_gpu.py")), INK, 1.06), run_time=0.7)

        # ========================================================== 2 · two lists: install_requires, find_packages
        sl = shopping_list()
        place(sl, left=-6.4, bottom=-3.45)
        inside(sl)
        apart(sl, tree, "shopping list runs into the tree")
        apart(sl, setup, "shopping list runs into the setup panel")
        b5, b10 = setup.bar(5, TOOL, 0.22), setup.bar(10, TOOL, 0.22)
        b11 = setup.bar(11, LOOKUP, 0.25)
        sc, sc_lab = scanner_for(tree)
        inside(sc_lab)
        apart(sc_lab, fl, "scanner label runs into the strip", buff=0.02)
        with self.voiceover(SAY[2]) as vo:
            self.play(flash(setup.code, INK, 1.02, 0.7))
            vo.wait_until("Install requires")
            self.play(FadeIn(b5), FadeIn(b10), run_time=0.5)
            pin = setup.span(5, "wandb==0.15.11").copy()
            self.play(FadeIn(sl.frame), FadeIn(sl.header), ReplacementTransform(pin, sl.chip), run_time=1.0)
            vo.wait_until("from the Python Package Index")
            self.play(flash(sl.header, S.GREY, 1.08), run_time=0.6)
            vo.wait_until("one pinned wandb version")
            self.play(flash(sl.chip, TOOL, 1.1), run_time=0.6)
            vo.wait_until("Find packages decides")
            self.play(FadeOut(b5), FadeOut(b10), FadeIn(b11), FadeIn(sc), FadeIn(sc_lab), run_time=0.5)
            vo.wait_until("get installed")
            self.play(*sc.sweep(tree, lit=("trainer/",)), run_time=1.6)
            self.play(*dim_rows(tree, ("setup.cfg", "PKG-INFO")), run_time=0.5)
            vo.wait_until("only folders with an init file")
            self.play(flash(tree.row("__init__.py"), OWN, 1.12), flash(tree.row("trainer/"), OWN, 1.1), run_time=0.8)

        # ========================================================== 3 · tar, gzip, copy; the job script
        pts = src_panel(PTS, 1, 4, wrap={4: ["$GCS_BUCKET_URI"]})
        place(pts, right=6.45, top=2.95)
        inside(pts)
        guard(pts.get_top()[1] < LREF_BOTTOM or pts.get_right()[0] < lref("23–24").get_left()[0],
              "panel runs into the lecture tag")
        for r in tree.tree.rows:
            if r.get_top()[1] > pts.get_bottom()[1]:
                guard(r.get_right()[0] < pts.get_left()[0] - 0.1, f"tree row {r.name} under the panel")
        cli = src_panel(CLI, 10, 11, wrap={10: ["$GCS_BUCKET_URI"]})
        place(cli, right=6.45, top=2.95)
        inside(cli)
        bk = bucket(PACKAGE_URI)
        place(bk, right=6.4, bottom=-3.4)
        bk.shift(RIGHT * (2.6 - bk.glyph.get_center()[0]))
        inside(bk)
        apart(bk, pts, "bucket runs into the panel")
        tar1 = tarball("trainer.tar").move_to(tree.get_center())
        tar2 = tarball("trainer.tar.gz").move_to(tar1)
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(sl, sc, sc_lab, b11, fl)), ReplacementTransform(setup, pts), run_time=0.9)
            self.play(FadeIn(bk, shift=UP * 0.2), run_time=0.5)
            vo.wait_until("tars the package folder")
            p2 = pts.bar(2, OWN, 0.22)
            rg = ring(tree, OWN, buff=0.15)
            self.play(FadeIn(p2), Create(rg), run_time=0.6)
            self.play(ReplacementTransform(VGroup(tree, rg), tar1), run_time=0.9)
            vo.wait_until("compresses it")
            p3 = pts.bar(3, OWN, 0.22)
            self.play(FadeOut(p2), FadeIn(p3), Transform(tar1, tar2), run_time=0.7)
            vo.wait_until("and copies it")
            p4 = pts.bar(4, LOOKUP, 0.22)
            mouth = bk.mouth()
            path = VMobject(stroke_color=LOOKUP, stroke_width=3)
            path.set_points_smoothly([tar1.glyph.get_right() + RIGHT * 0.1,
                                      np.array([(tar1.get_right()[0] + mouth[0]) / 2, mouth[1] + 0.9, 0]),
                                      mouth + UP * 0.35])
            self.play(FadeOut(p3), FadeIn(p4), Create(path), run_time=0.6)
            self.play(tar1.glyph.animate.scale(0.55).move_to(bk.glyph.get_center() + DOWN * 0.1),
                      FadeOut(tar1.text), run_time=1.0)
            self.play(flash(bk.text, LOOKUP, 1.06), FadeOut(path), run_time=0.6)
            vo.wait_until("The job script")
            self.play(FadeOut(p4), ReplacementTransform(pts, cli), run_time=0.8)
            vo.wait_until("at that file")
            c10 = cli.bar(10, LOOKUP, 0.22)
            self.play(FadeIn(c10), flash(bk.text, LOOKUP, 1.06), run_time=0.7)
            vo.wait_until("and names the module")
            c11 = cli.bar(11, LOOKUP, 0.22)
            ul = under(cli.span(11, '"trainer.task"'), LOOKUP)
            self.play(FadeOut(c10), FadeIn(c11), Create(ul), run_time=0.6)
        packed = tar1.glyph

        # ========================================================== 4 · the key fact: who trains where
        vm = JobVM()
        vm.move_to([2.95, -1.25, 0])
        inside(vm)
        bk_spot = np.array([1.15, 1.75, 0])
        vx = chip("Vertex AI", CLOUD, size=24)
        vx.move_to([4.6, 1.75, 0])
        lap = laptop_zone(4.5, 3.0, caption="your laptop")
        place(lap, left=-6.5, top=2.55)
        ctr = container_box("model-training-cli", w=3.4, h=1.0)
        ctr.move_to(lap.frame.get_center() + UP * 0.25)
        inside(lap)
        apart(lap, vm, "laptop runs into the VM")
        ex31 = excerpt_chip(IMAGE_CPU, "cli.sh · line 31 (excerpt)", line=source_line(CLI, 31))
        place(ex31, left=-6.4, top=lap.get_bottom()[1] - 0.45)
        inside(ex31)
        apart(ex31, vm, "excerpt 31 runs into the VM")
        with self.voiceover(SAY[4]) as vo:
            bshift = bk_spot - bk.glyph.get_center()
            self.play(FadeOut(VGroup(cli, c11, ul)), FadeOut(bk.text),
                      bk.glyph.animate.shift(bshift), packed.animate.shift(bshift), run_time=0.9)
            bk.remove(bk.text)
            self.play(FadeIn(vm, shift=UP * 0.3), FadeIn(vx), run_time=0.8)
            a_vx = arrow(vx.get_bottom(), [vx.get_center()[0], vm.vm.frame.get_top()[1], 0], CLOUD)
            self.play(GrowArrow(a_vx), run_time=0.4)
            vo.wait_until("Your own Docker image")
            self.play(FadeIn(lap), FadeIn(ctr, shift=UP * 0.2), run_time=0.7)
            vo.wait_until("packages, uploads")
            a_up = arrow(ctr.get_right() + UP * 0.2, bk.glyph.get_left(), S.GREY)
            l_up = label("package & upload", CAPTION, S.GREY)
            l_up.move_to(a_up.get_center()).shift(UP * 0.32 + LEFT * 0.1)
            apart(l_up, bk.glyph, "label runs into the bucket", buff=0.0)
            self.play(GrowArrow(a_up), FadeIn(l_up), run_time=0.6)
            vo.wait_until("and submits")
            route = [ctr.get_top() + RIGHT * 1.0, np.array([ctr.get_top()[0] + 1.0, 2.85, 0]),
                     np.array([vx.get_center()[0], 2.85, 0]), vx.get_top() + UP * 0.05]
            sub_line = VMobject(stroke_color=S.GREY, stroke_width=3).set_points_as_corners(route[:3])
            sub_tip = arrow(route[2], route[3], S.GREY, buff=0.0)
            l_sub = label("submit", CAPTION, S.GREY)
            place(l_sub, cx=(route[1][0] + bk.glyph.get_left()[0]) / 2, top=route[1][1] - 0.1)
            guard(route[1][1] + 0.05 < LREF_BOTTOM, "submit route runs into the lecture tag")
            apart(l_sub, l_up, "submit label runs into upload label", buff=0.02)
            self.play(Create(sub_line), run_time=0.5)
            self.play(GrowArrow(sub_tip), FadeIn(l_sub), run_time=0.4)
            vo.wait_until("but it never trains")
            no = DashedLine(ctr.get_bottom() + RIGHT * 0.6, vm.vm.frame.get_left() + UP * 0.3,
                            color=S.GREY, stroke_width=3, dash_length=0.12)
            xm = x_mark(0.34).move_to(no.get_center())
            self.play(Create(no), run_time=0.5)
            self.play(FadeIn(xm, scale=1.3), run_time=0.4)
            vo.wait_until("The job runs in")
            self.play(flash(vm.parts["image"], CTR, 1.03, 0.8), run_time=0.8)
            vo.wait_until("prebuilt training image")
            self.play(FadeIn(ex31, shift=UP * 0.2), flash(vm.image_title, CTR, 1.06), run_time=0.7)
            vo.wait_until("only through the tarball")
            shelf = vm.shelves[1]
            spot = np.array([shelf.get_right()[0] - 0.55, shelf.get_center()[1], 0])
            self.play(packed.animate.scale(0.9).move_to(spot), run_time=1.0)
            self.play(flash(packed, OWN, 1.25), run_time=0.6)

        # ========================================================== 5 · what the image already ships
        up5 = np.array([0, 2.2, 0])
        lft = -6.4
        ex3 = excerpt_chip("import requests", "task.py · line 3 (excerpt)", line=source_line(TASK, 3))
        ex17 = excerpt_chip("from sklearn.model_selection", "task.py · line 17 (excerpt)",
                            line=source_line(TASK, 17))
        place(ex17, left=lft, cy=2.4)
        place(ex3, left=lft, cy=-1.35)
        luck = note("not in setup.py · luck, not declaration", size=24)
        place(luck, left=lft, cy=-2.6)
        for m in (ex3, ex17, luck):
            inside(m)
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(lap, ctr, a_up, l_up, sub_line, sub_tip, l_sub, no, xm, ex31, vx, a_vx,
                                     bk.glyph)), FadeOut(lr), run_time=0.6)
            lr = None
            self.play(vm.animate.shift(up5), packed.animate.shift(up5), run_time=0.8)
            inside(vm)
            for m in (ex3, ex17):
                apart(m, vm, "excerpt chip runs into the VM")
            apart(luck, vm, "note runs into the VM")
            vo.wait_until("TensorFlow")
            self.play(flash(vm.libs[0], SHIPPED, 1.1), run_time=0.5)
            self.play(flash(vm.libs[1], SHIPPED, 1.1), run_time=0.5)
            self.play(flash(vm.libs[2], SHIPPED, 1.1), run_time=0.5)
            vo.wait_until("so the trainer imports them")
            k17 = DashedLine(vm.libs[1].get_corner(UP + LEFT), ex17.chip.get_right(), color=S.GREY, stroke_width=2.5,
                             dash_length=0.1)
            k3 = DashedLine(vm.libs[2].get_bottom(), ex3.chip.get_right(), color=S.GREY, stroke_width=2.5,
                            dash_length=0.1)
            self.play(FadeIn(ex17, shift=RIGHT * 0.2), Create(k17), run_time=0.6)
            self.play(FadeIn(ex3, shift=RIGHT * 0.2), Create(k3), run_time=0.6)
            vo.wait_until("although setup dot py")
            self.play(FadeIn(luck, shift=UP * 0.15), run_time=0.6)
            self.play(flash(luck, S.GREY, 1.06), run_time=0.6)

        # ========================================================== 6 · pip unwraps the tarball on the job machine
        sl6 = shopping_list()
        place(sl6, left=lft, top=2.6)
        py6 = pypi_cloud()
        place(py6, cx=sl6.get_center()[0], cy=0.1)
        for m in (sl6, py6):
            inside(m)
            apart(m, vm, "left column runs into the VM")
        log = output_box(["Successfully installed cheese-app-trainer … wandb …"])
        place(log, right=6.4, top=vm.get_bottom()[1] - 0.2)
        inside(log)
        apart(log, py6, "log runs into the PyPI cloud")
        ltag = illustration_tag()
        place(ltag, right=log.get_right()[0], top=log.get_bottom()[1] - 0.12)
        run = cmd_chip("python -m trainer.task")
        place(run, left=log.get_left()[0], cy=ltag.get_center()[1] - 0.45)
        inside(run)
        apart(run, ltag, "run chip runs into the tag")
        w_chip, t_chip = vm.parts["wandb"], vm.parts["trainer"]
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(ex3, ex17, k3, k17, luck)), run_time=0.5)
            vo.wait_until("pip unwraps the tarball")
            self.play(flash(packed, TOOL, 1.3), run_time=0.6)
            self.play(ReplacementTransform(packed.copy(), sl6), run_time=0.9)
            vo.wait_until("The shopping list fetches")
            self.play(FadeIn(py6), run_time=0.4)
            a1 = arrow(sl6.frame.get_bottom(), py6.get_top(), LOOKUP)
            self.play(GrowArrow(a1), flash(sl6.chip, TOOL, 1.1), run_time=0.6)
            a2 = arrow(py6.get_right(), w_chip.get_left(), LOOKUP)
            self.play(GrowArrow(a2), *vm.install("wandb"), run_time=0.8)
            tk1 = tick_mark(0.3).next_to(w_chip, UP, buff=0.06)
            self.play(Create(tk1), run_time=0.3)
            vo.wait_until("and the trainer package")
            self.play(FadeOut(packed, scale=0.6), *vm.install("trainer"), run_time=0.8)
            tk2 = tick_mark(0.3).next_to(t_chip, UP, buff=0.06)
            self.play(Create(tk2), FadeIn(log, shift=UP * 0.15), FadeIn(ltag), run_time=0.6)
            vo.wait_until("Then Vertex runs")
            self.play(FadeIn(run, shift=UP * 0.15), run_time=0.5)
            self.play(run.box.animate.set_stroke(TURN, 3), run.text.animate.set_color(TURN), run_time=0.5)

        # ========================================================== 7 · a teammate's module that never travels
        lap7 = laptop_zone(6.3, 6.3, caption="your laptop", corner=DOWN + RIGHT)
        place(lap7, left=-6.5, top=3.25)
        tree7 = PackageTree()
        place(tree7, left=-6.2, top=2.45)
        gm = ghost_module()
        gm.shift(tree7.row_point(0, "task_multi_gpu.py") - np.array([gm.glyph.get_left()[0], gm.text.get_center()[1], 0]))
        gtags = VGroup(illustration_tag(), example_tag()).arrange(RIGHT, buff=0.1)
        place(gtags, left=gm.get_left()[0], top=gm.get_bottom()[1] - 0.15)
        for m in (lap7, tree7, gm, gtags):
            inside(m)
        guard(gtags.get_right()[0] < lap7.get_right()[0] - 0.1, "tags stick out of the laptop")
        apart(gtags, lap7.caption, "tags run into the laptop caption", buff=0.05)
        ex2 = excerpt_chip("tar cvf trainer.tar package", "package-trainer.sh · line 2 (excerpt)",
                           line=source_line(PTS, 2))
        place(ex2, right=6.4, top=2.75)
        inside(ex2)
        guard(ex2.get_top()[1] < LREF_BOTTOM - 0.05, "excerpt runs into the lecture tag")
        apart(ex2, lap7, "excerpt runs into the laptop")
        bk7 = bucket(None)
        bk7.move_to([4.6, 0.0, 0])
        tar7 = tarball("trainer.tar.gz").move_to([1.7, 0.0, 0])
        stays = note("stays on your laptop", size=24)
        place(stays, left=gm.get_left()[0], top=gm.get_bottom()[1] - 0.15)
        tree7b = PackageTree(entries=TREE_IN)
        tree7b.shift(tree7.tree.rows[0].glyph.get_left() - tree7b.tree.rows[0].glyph.get_left())
        inside(tree7b)
        tar7b = tarball("trainer.tar.gz").move_to([1.7, -1.7, 0])
        rides = note("augment.py inside", size=24)
        place(rides, cx=tar7b.get_center()[0], top=tar7b.get_bottom()[1] - 0.1)
        uploaded = note("uploaded ≠ installed", color=S.GREY, size=24)
        place(uploaded, right=6.4, cy=rides.get_center()[1])
        for m in (bk7, tar7, stays, tar7b, rides, uploaded):
            inside(m)
        apart(rides, uploaded, "notes run together")
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(vm, log, ltag, run, sl6, py6, a1, a2, tk1, tk2)), run_time=0.6)
            self.play(FadeIn(lap7), FadeIn(tree7), run_time=0.6)
            vo.wait_until("augment dot py")
            self.play(FadeIn(gm, shift=LEFT * 0.3), run_time=0.6)
            vo.wait_until("a made-up example")
            self.play(FadeIn(gtags), run_time=0.5)
            vo.wait_until("The script tars only")
            self.play(FadeIn(ex2, shift=DOWN * 0.15), FadeIn(bk7), run_time=0.6)
            rg7 = ring(tree7, OWN, buff=0.12)
            self.play(Create(rg7), run_time=0.5)
            self.play(ReplacementTransform(VGroup(tree7.copy(), rg7), tar7), run_time=0.9)
            vo.wait_until("never leaves your laptop")
            self.play(tar7.glyph.animate.scale(0.55).move_to(bk7.glyph.get_center() + DOWN * 0.1),
                      FadeOut(tar7.text), run_time=0.8)
            self.play(FadeOut(gtags), FadeIn(stays), flash(gm, S.GREY, 1.1), run_time=0.6)
            vo.wait_until("Placed next to setup dot py")
            self.play(FadeOut(stays), ReplacementTransform(VGroup(tree7, gm), tree7b), run_time=1.0)
            vo.wait_until("it travels")
            self.play(ReplacementTransform(tree7b.copy(), tar7b), run_time=0.8)
            self.play(FadeIn(rides), run_time=0.4)
            vo.wait_until("but find packages skips it")
            sc7, sc7_lab = scanner_for(tree7b)
            apart(sc7_lab, ex2, "scanner label runs into the excerpt")
            self.play(FadeIn(sc7), FadeIn(sc7_lab), run_time=0.3)
            self.play(*sc7.sweep(tree7b, lit=("trainer/",)), run_time=1.4)
            self.play(flash(tree7b.row("augment.py"), S.GREY, 1.1), FadeIn(uploaded, shift=LEFT * 0.2), run_time=0.6)

        # ========================================================== 8 · ModuleNotFoundError under "Successfully installed"
        vm8 = JobVM()
        vm8.move_to([2.95, 0.95, 0])
        log8 = output_box(["Successfully installed cheese-app-trainer … wandb …"])
        place(log8, right=6.4, top=vm8.get_bottom()[1] - 0.2)
        err = output_box([("ModuleNotFoundError: No module named 'augment'", ERR)])
        place(err, left=log8.get_left()[0], top=log8.get_bottom()[1] - 0.12)
        imp = cmd_chip("import augment", color=S.GREY, size=24)
        itag = illustration_tag()
        imp_g = VGroup(imp, itag).arrange(RIGHT, buff=0.2)
        place(imp_g, left=lft, cy=2.3)
        lap8 = laptop_zone(5.6, 1.9, caption="your laptop", corner=DOWN + RIGHT)
        place(lap8, left=lft, top=1.35)
        f8 = file_row("augment.py", color=INK)
        i8 = cmd_chip("import augment", color=OWN)
        row8 = VGroup(f8, i8).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        place(row8, left=lap8.get_left()[0] + 0.3, top=lap8.get_top()[1] - 0.3)
        tk8 = tick_mark(0.3)
        place(tk8, left=i8.get_right()[0] + 0.15, cy=i8.get_center()[1])
        for m in (vm8, log8, err, imp_g, lap8, row8, tk8):
            inside(m)
        apart(imp_g, vm8, "import chip runs into the VM")
        apart(lap8, vm8, "laptop inset runs into the VM")
        apart(lap8, log8, "laptop inset runs into the log")
        guard(tk8.get_right()[0] < lap8.get_right()[0] - 0.1, "tick sticks out of the inset")
        apart(VGroup(row8, tk8), lap8.caption, "inset rows run into the laptop caption", buff=0.05)
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(lap7, tree7b, tar7b, rides, uploaded, ex2, bk7, tar7.glyph, sc7, sc7_lab)),
                      run_time=0.6)
            self.play(FadeIn(vm8), run_time=0.5)
            self.play(*vm8.install("wandb"), *vm8.install("trainer"), FadeIn(log8), run_time=0.5)
            vo.wait_until("import augment")
            self.play(FadeIn(imp_g, shift=RIGHT * 0.2), run_time=0.4)
            self.play(imp.box.animate.set_stroke(TURN, 3), imp.text.animate.set_color(TURN), run_time=0.4)
            vo.wait_until("Python searches")
            self.play(*vm8.search(run_time=1.5))
            vo.wait_until("and finds nothing")
            xi = x_mark(0.34)
            place(xi, left=itag.get_right()[0] + 0.25, cy=imp.get_center()[1])
            inside(xi)
            guard(xi.get_right()[0] < vm8.get_left()[0] - 0.05, "x runs into the VM")
            self.play(FadeOut(vm8.beam), FadeIn(xi, scale=1.3), run_time=0.5)
            vo.wait_until("Module Not Found Error")
            self.play(FadeIn(err, shift=DOWN * 0.15), run_time=0.5)
            self.play(flash(err, ERR, 1.04), run_time=0.6)
            vo.wait_until("right under the line")
            self.play(flash(log8.rows, OWN, 1.04, 0.8), run_time=0.8)
            vo.wait_until("Locally it worked")
            self.play(FadeIn(lap8), FadeIn(row8, shift=UP * 0.15), run_time=0.6)
            self.play(Create(tk8), run_time=0.4)
            vo.wait_until("because the file sat")
            self.play(flash(f8, OWN, 1.12), run_time=0.7)

        # ========================================================== 9 · the fix: the file has to travel
        tree9 = PackageTree()
        place(tree9, left=-6.3, top=2.2)
        gm9 = ghost_module()
        gm9.shift(tree9.row_point(0, "task_multi_gpu.py") - np.array([gm9.glyph.get_left()[0], gm9.text.get_center()[1], 0]))
        dest = tree9.row_point(2, "task_multi_gpu.py")
        mv = dest - np.array([gm9.glyph.get_left()[0], gm9.text.get_center()[1], 0])
        solid = file_row("augment.py", color=OWN, glyph_color=OWN, size=22)
        solid.shift(dest - np.array([solid.glyph.get_left()[0], solid.text.get_center()[1], 0]))
        ftag = illustration_tag()
        place(ftag, left=-6.3, top=solid.get_bottom()[1] - 0.35)
        rx = -0.3
        fix1 = fix_chip("from trainer import augment", font=MONO)
        place(fix1, left=rx, cy=1.8)
        tk9 = tick_mark(0.34)
        place(tk9, left=fix1.get_right()[0] + 0.2, cy=fix1.get_center()[1])
        fix2 = fix_chip('py_modules=["augment"]', font=MONO)
        fix2_note = note("or, in setup(...)", size=24)
        VGroup(fix2_note, fix2).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        place(VGroup(fix2_note, fix2), left=rx, cy=0.55)
        bad = chip("from somewhere import augment", ERR, size=CAPTION, font=MONO)
        place(bad, left=rx, cy=-1.0)
        bad_s = strike(bad)
        bad_n = note("renaming the import: the file still isn't there", size=24)
        place(bad_n, left=rx, top=bad.get_bottom()[1] - 0.15)
        for m in (tree9, gm9, solid, ftag, fix1, tk9, fix2, fix2_note, bad, bad_n):
            inside(m)
        apart(tree9, fix1, "tree runs into the fix chip")
        apart(solid, bad, "augment row runs into the struck chip")
        guard(solid.get_right()[0] < rx - 0.2, "augment row runs into the right column")
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(VGroup(vm8, log8, err, imp_g, xi, lap8, row8, tk8)), run_time=0.6)
            self.play(FadeIn(tree9), FadeIn(gm9), FadeIn(ftag), run_time=0.6)
            vo.wait_until("put the file inside")
            self.play(gm9.animate.shift(mv), run_time=0.9)
            sc9, sc9_lab = scanner_for(VGroup(tree9, gm9))
            inside(sc9_lab)
            self.play(FadeIn(sc9), FadeIn(sc9_lab), run_time=0.3)
            self.play(*sc9.sweep(tree9, lit=("trainer/",), run_time=1.2))
            self.play(sc9.animate.shift(DOWN * (sc9.bar.get_center()[1] - solid.get_bottom()[1] + 0.1)),
                      ReplacementTransform(gm9, solid), run_time=0.6)
            self.play(FadeIn(fix1, shift=LEFT * 0.2), run_time=0.5)
            self.play(Create(tk9), run_time=0.3)
            vo.wait_until("or list it in setup dot py")
            self.play(FadeIn(fix2_note), FadeIn(fix2, shift=LEFT * 0.2), run_time=0.6)
            vo.wait_until("A new import line")
            self.play(FadeIn(bad), run_time=0.4)
            self.play(Create(bad_s), FadeIn(bad_n, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("the file has to travel")
            self.play(flash(solid, OWN, 1.15), run_time=0.7)

        # ========================================================== 10 · install_requires is the wrong list
        sl10 = shopping_list()
        place(sl10, left=-6.0, cy=1.5)
        py10 = pypi_cloud()
        py10.move_to([3.9, 1.6, 0])
        tar10 = tarball("trainer.tar.gz").move_to([3.9, -0.6, 0])
        wrong = chip('install_requires=[..., "augment"]', ERR, size=CAPTION, font=MONO)
        place(wrong, left=-6.0, cy=-1.9)
        wrong_s = strike(wrong)
        wrong_n = note("fetches from PyPI · not your file", size=24)
        place(wrong_n, left=-6.0, top=wrong.get_bottom()[1] - 0.15)
        else_n = note("same name on PyPI = someone else's code", size=24)
        place(else_n, cx=py10.get_center()[0], bottom=py10.get_top()[1] + 0.15)
        for m in (sl10, py10, tar10, wrong, wrong_n, else_n):
            inside(m)
        guard(else_n.get_top()[1] < LREF_BOTTOM - 0.05, "note runs into the lecture tag")
        apart(wrong_n, tar10, "note runs into the tarball")
        with self.voiceover(SAY[10]) as vo:
            self.play(FadeOut(VGroup(tree9, solid, ftag, sc9, sc9_lab, fix1, tk9, fix2, fix2_note, bad, bad_s,
                                     bad_n)), run_time=0.6)
            self.play(FadeIn(sl10), FadeIn(wrong, shift=UP * 0.15), run_time=0.6)
            self.play(Create(wrong_s), FadeIn(wrong_n), run_time=0.6)
            vo.wait_until("That list downloads")
            self.play(FadeIn(py10), FadeIn(tar10), run_time=0.5)
            a10 = arrow(sl10.frame.get_right(), py10.get_left(), LOOKUP)
            self.play(GrowArrow(a10), run_time=0.6)
            vo.wait_until("never from your tarball")
            no10 = DashedLine(sl10.frame.get_right() + DOWN * 0.2, tar10.glyph.get_left() + LEFT * 0.1,
                              color=S.GREY, stroke_width=3, dash_length=0.12)
            x10 = x_mark(0.34).move_to(no10.get_center())
            self.play(Create(no10), run_time=0.5)
            self.play(FadeIn(x10, scale=1.3), run_time=0.4)
            vo.wait_until("and a package there")
            self.play(FadeIn(else_n, shift=DOWN * 0.1), flash(py10, ERR, 1.08), run_time=0.7)

        # ========================================================== 11 · takeaway
        tk = takeaway("If the question says dependencies installed but `ModuleNotFoundError`, think: the file "
                      "never travelled inside the package that `setup.py` builds.")
        inside(tk)
        with self.voiceover(SAY[11]) as vo:
            self.play(FadeOut(VGroup(sl10, py10, tar10, wrong, wrong_s, wrong_n, else_n, a10, no10, x10)),
                      run_time=0.6)
            self.play(Write(tk), run_time=1.6)
            vo.wait_until("the file never travelled")
            self.play(flash(tk, TURN, 1.04, 0.8))
        self.play(FadeOut(tk), run_time=0.6)
        self.wait(0.4)
