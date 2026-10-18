"""S02 · Image, layer, container, registry (concept scene: no README tracker, no terminal).

Beats (script.md "## S02", one voiceover block each):
 0. A GREY header across the top, `image · layer · container · registry` (each word turns TEAL in
    the block that defines it: image and layer in 1, container in 3, registry in 5). L1's closing
    picture at left: a BLUE VM box holding a GREEN venv box. At "the same setup" three GREY mono
    chips appear beside it, `apt`, `git clone`, `uv sync`; at "on an operating system" a
    RED-outlined "the right OS". At "A Docker image" a dashed TEAL box opens at right; each chip
    becomes what it produced as it is named: `apt` -> ORANGE "OS files" and ORANGE "Python",
    `uv sync` -> GREEN "packages", `git clone` -> GREY "your code"; the box closes solid TEAL,
    caption "an image".
 1. The VM picture fades; the box (with "an image") moves center-left and opens: its items become
    three translucent slabs with TEAL outlines, bottom-up "OS files + Python" (ORANGE; the two
    items' boxes merge and their letters regroup into the label), "packages" (GREEN), "your code"
    (GREY); a lock glyph "read-only" on the stack's top corner. Each slab pulses on "Each layer".
    At "Beside it" a TEAL config card with four empty rows ENV, ENTRYPOINT, CMD, WorkingDir slides
    in at right (its top 0.12 under the tag); ENV lights on "settings like", ENTRYPOINT + CMD on
    "which program". The GREY tag "Lecture 2 · slides 30–31, 35" (right-aligned under the header)
    shows from the block's start ("An image is a stack") through "Think of the image as a class": it
    leaves with the class/instance captions at "One small slip" (block 4).
 2. A GREY page "Dockerfile" at far left, lines `FROM …`, `RUN …`, `COPY …`, `CMD …`. A YELLOW bar
    reads them one at a time and each keyword flies (TransformFromCopy) to what it makes, landing as
    a TEAL tile just left of its slab: FROM by the base slab, RUN and COPY by theirs (a brace on
    their right: "adds a layer"); CMD arcs over the stack into the card's CMD slot as a tile
    `["…"]` ("config only" under the card). No arrows: the flying keywords are the arrows.
 3. The page, the card and its notes ("adds a layer", "config only") fade (the slide tag stays);
    the lock moves to the stack's side. A PURPLE `docker run` chip: a dashed, glowing TEAL glass
    slab lands on the stack ("writable layer") with a TEAL dot "main process"; the chip turns into
    the label "container". At "the same layers" it lifts left and a second container appears
    beside it, both linked by thin TEAL lines to the SAME stack,
    caption "shared, not copied". The glass slabs pulse on "plus a thin", the dots on "one main
    process". The first dot
    goes out ("stopped"); a `--rm` chip lands on it and, at "deletes it", that whole container
    (glass, labels, link) dissolves; the chip leaves with the GREEN check "image unchanged".
 4. The remaining container settles on the stack and the picture moves left; captions under it:
    "image = class", "container = instance" (TEAL). They fade with the slide tag at "One small slip";
    README card (README.md · line 173)
    "Build the docker container by running", and a second card slides in under it (README.md ·
    line 146) "Install uv & copy source code into the container". At "the docker container" both
    "container"s are struck YELLOW with "image" above them, tag "erratum". "Building makes an
    image" pulses the stack, "running makes a container" the glass. (The keyword tiles fade; the
    picture keeps its size, since shrinking it would take its labels under 20 pt.)
 5. The cards and the picture fade. A BLUE shelf unit "registry · Docker Hub": small TEAL stacks
    with sticky notes `python:3.12-slim-bookworm` and `dlops/simple-translate:latest`. A newer stack
    lands; `:latest` lights YELLOW and the note peels off the old stack and sticks to the newer one;
    caption "a tag: a name that points at one image".
 6. V8, first half: three BLUE VMs, each with its own "kernel" bar and "OS" band; the kernels pulse
    YELLOW on "A VM boots", a GREY caption "kernel: the core of the operating system" on "the core
    of". At "Containers are" the VMs shrink into TEAL "container" boxes and the caption becomes
    "isolated processes, not machines", and GREY "user space" appears beside the leftmost container
    (slide 22); at "that share one" the kernel bars slide together into one GREY "Linux kernel ·
    shared", which pulses; then GREY tags "namespaces" and "cgroups" sit on the bar under the outer
    containers (slide 22).
    Tag "Lecture 2 · slides 9–12, 22–24" (under the header) from the block's start ("And a container
    is not a small VM", with the VMs) through block 7: it fades with the V8 picture at block 8's start.
 7. V8, second half: a GREY laptop outline wraps the picture ("Mac · Windows"); a dashed GREY box
    "Linux VM · Docker Desktop" slides in under the kernel bar. Then the laptop outline morphs into
    a BLUE VM outline ("cloud VM", ending under the kernel bar), the dashed box fades: caption "on a
    cloud VM: its own Linux". "user space" leaves with the caption at the start; the two chips stay on
    the bar (no arrow through a daemon: SLIDES.md Conflict 9).
 8. L1's three chips return beside a stack whose two bottom slots are empty (dashed), each RED-
    outlined chip level with its slot: "the operating system's files" slides into the bottom slot at
    "the system's files", "system libraries" into the next at "and libraries", both becoming ORANGE
    slabs (GREEN check); the third, "GPU drivers", stays outside below them and turns GREY, "still
    the host's", at "GPU drivers still". Tag "Lecture 2 · slides 5–7, 10, 22" in the V8 tag's spot,
    in with the stack and chips (SLIDES.md claim 3; the host's GPU drivers: slide 22). Fade out to an
    empty frame (the tag with it).
"""

import numpy as np  # noqa: I001  (manim first, then common: common must win)
from manim import *

from explainer import style as S
from explainer.devops import lecture_ref
from explainer.scene import VoiceScene

from common import (CLOUD, ERR, IMAGE, INK, LAPTOP, MONO, NARRATION, SYSTEM, TOOL, TURN, VENV, ConfigCard,
                    Glass, KernelPicture, LayerStack, Nest, RegistryShelf, Slab, box, check_mark, chip,
                    docker_chip, erratum_tag, label, lock_glyph, mini_stack, mono, outline_box,
                    readme_card, steady, sticky, tag)

SAY = NARRATION["S02"]
assert len(SAY) == 9, len(SAY)

HEAD_Y = 3.15
SLAB_H = 0.72
GAP = 0.04
STACK_W = 3.4
STACK_X = -1.1           # the stack's centre in blocks 1-3
FLOOR_Y = -2.1           # where the stack stands in blocks 1-3
TOP_Y = FLOOR_Y + 3 * (SLAB_H + GAP)
GLASS_W = 3.0


# ------------------------------------------------------------------ small pictures
def header() -> VGroup:
    """`image · layer · container · registry`, GREY, on one baseline (steady texts); .words[i]."""
    words = VGroup(*[steady(w, 32, S.GREY) for w in ("image", "layer", "container", "registry")])
    dots = VGroup(*[steady("·", 32, S.GREY_DARK) for _ in range(3)])
    row = VGroup()
    for i, w in enumerate(words):
        row.add(w)
        if i < 3:
            row.add(dots[i])
    row.arrange(RIGHT, buff=0.3, aligned_edge=DOWN)
    row.move_to([0, HEAD_Y, 0])
    row.words, row.dots = words, dots
    return row


def slide_ref(head: VGroup, slides: str) -> VGroup:
    """lecture_ref(2, slides), right-aligned at x 6.6 just under the header row (the header reaches
    x 3.58, so the default top-right spot would cover "registry")."""
    r = lecture_ref(2, slides)
    return r.move_to([6.6 - r.width / 2, head.get_bottom()[1] - 0.1 - r.height / 2, 0])


def item(s: str, color, item_w: float = 2.6) -> VGroup:
    """One thing an image holds (block 0): a filled rounded bar with a 26 pt label. .box .text"""
    b = box(item_w, 0.56, color, fill_opacity=0.3, radius=0.1)
    t = label(s, 26, INK).move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def slab_label(slab, s: str, size: float = 24):
    """Give a text-less Slab a serif label (steady, so it may move)."""
    t = steady(s, size, INK).move_to(slab.box)
    slab.text = t
    slab.add(t)
    return slab


def word_glyphs(t: Text, s: str, word: str) -> VGroup:
    """The glyphs of `word` inside Text `t` built from string `s` (spaces have no glyphs)."""
    i = s.find(word)
    a = len("".join(s[:i].split()))
    return VGroup(*t.submobjects[a:a + len("".join(word.split()))])


def strike(g, color=TURN) -> Line:
    """A YELLOW strike line through glyphs `g`."""
    return Line(g.get_left() + LEFT * 0.06, g.get_right() + RIGHT * 0.06, color=color,
                stroke_width=4).move_to(g.get_center())


def dockerfile_page(top: float, pitch: float = 0.62, page_w: float = 2.4) -> VGroup:
    """A GREY page glyph 'Dockerfile' with four lines, top-down FROM, RUN, COPY, CMD (title's top
    at `top`, left edge at x = 0). .frame .title .lines[i]"""
    title = mono("Dockerfile", 22, S.GREY)
    lines = VGroup(*[mono(n, 24, INK) for n in ("FROM …", "RUN …", "COPY …", "CMD …")])
    title.move_to([0.25, top, 0], aligned_edge=UL)
    for k, ln in enumerate(lines):
        ln.move_to([0.25, title.get_bottom()[1] - 0.45 - k * pitch, 0], aligned_edge=LEFT)
    t, b = top + 0.22, lines[-1].get_bottom()[1] - 0.3
    frame = Polygon([0, t, 0], [page_w - 0.28, t, 0], [page_w, t - 0.28, 0], [page_w, b, 0], [0, b, 0],
                    stroke_color=S.GREY, stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
    g = VGroup(frame, title, lines)
    g.frame, g.title, g.lines = frame, title, lines
    return g


def kw_tile(s: str) -> VGroup:
    """A Dockerfile keyword as a small TEAL tile (lands on the slab or the card it made)."""
    t = steady(s, 20, INK, mono_font=True)
    f = RoundedRectangle(width=t.width + 0.26, height=0.4, corner_radius=0.08, stroke_color=IMAGE,
                         stroke_width=2.2).set_fill(IMAGE, 0.22)
    t.move_to(f)
    return VGroup(f, t)


def laptop_outline(w: float, h: float, color=S.GREY) -> VGroup:
    """A big laptop outline (screen + base) to wrap a picture. .screen .base"""
    screen = RoundedRectangle(width=w, height=h, corner_radius=0.18, stroke_color=color, stroke_width=3)
    base = Polygon([-w / 2 - 0.45, 0, 0], [w / 2 + 0.45, 0, 0], [w / 2 + 0.2, 0.22, 0],
                   [-w / 2 - 0.2, 0.22, 0], stroke_color=color, stroke_width=3).set_fill(color, 0.25)
    base.next_to(screen, DOWN, buff=0.05)
    g = VGroup(screen, base)
    g.screen, g.base = screen, base
    return g


class FourNouns(VoiceScene):
    def construct(self):
        head = header()

        # ================================================================ 0 · four words, L1's setup
        nest = Nest(vm_w=3.9, vm_h=2.8, size=26).move_to([-4.4, -0.3, 0])
        setup = VGroup(*[chip(s, S.GREY, size=26, font=MONO) for s in ("apt", "git clone", "uv sync")])
        right_os = chip("the right OS", ERR, size=26, fill_opacity=0.06)
        VGroup(*setup, right_os).arrange(DOWN, buff=0.36).move_to([-0.55, -0.3, 0])
        apt, git, uvs = setup
        ibox = outline_box(3.3, 3.75, IMAGE).move_to([4.1, -0.15, 0])
        ibox_solid = outline_box(3.3, 3.75, IMAGE, solid=True).move_to(ibox)
        items = VGroup(item("your code", LAPTOP), item("packages", VENV), item("Python", SYSTEM),
                       item("OS files", SYSTEM)).arrange(DOWN, buff=0.24).move_to(ibox)
        i_code, i_pkg, i_py, i_os = items
        an_image = label("an image", 28, IMAGE).next_to(ibox, DOWN, buff=0.25)

        with self.voiceover(SAY[0]) as vo:
            self.play(LaggedStart(*[FadeIn(m, shift=DOWN * 0.15) for m in head], lag_ratio=0.12),
                      run_time=1.6)
            vo.wait_until("In lecture 1")
            self.play(FadeIn(nest, scale=0.9), run_time=0.8)
            vo.wait_until("the same setup")
            self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.3) for c in setup], lag_ratio=0.3),
                      run_time=1.1)
            vo.wait_until("on an operating system")
            self.play(FadeIn(right_os, shift=LEFT * 0.3), run_time=0.6)
            self.play(Indicate(right_os, color=ERR, scale_factor=1.08), run_time=0.8)
            vo.wait_until("A Docker image")
            self.play(Create(ibox.frame), run_time=0.9)
            vo.wait_until("system files")
            self.play(TransformFromCopy(apt, i_os), run_time=0.5)
            vo.wait_until("Python, the")
            self.play(ReplacementTransform(apt, i_py), run_time=0.5)
            vo.wait_until("the packages")
            self.play(ReplacementTransform(uvs, i_pkg), run_time=0.5)
            vo.wait_until("and the code")
            self.play(ReplacementTransform(git, i_code), run_time=0.5)
            self.play(ReplacementTransform(ibox, ibox_solid), FadeIn(an_image, shift=UP * 0.1),
                      run_time=0.6)

        # ================================================================ 1 · layers + config card
        stack = LayerStack(stack_w=STACK_W, gap=GAP)
        stack.floor.move_to([STACK_X, FLOOR_Y, 0])
        s_os = slab_label(stack.make(None, SYSTEM, SLAB_H), "OS files + Python")
        s_pkg = slab_label(stack.make(None, VENV, SLAB_H), "packages")
        s_code = slab_label(stack.make(None, LAPTOP, SLAB_H), "your code")
        slabs = [s_os, s_pkg, s_code]
        lock_g = VGroup(lock_glyph(0.4, S.GREY), label("read-only", 24, S.GREY)).arrange(RIGHT, buff=0.15)
        lock_g.next_to(s_code.box, UP, buff=0.14).align_to(s_code.box, RIGHT)
        ref1 = slide_ref(head, "30–31, 35")
        card = ConfigCard(rows=("ENV", "ENTRYPOINT", "CMD", "WorkingDir"), card_w=3.2)
        # the slide tag stays on through block 4's class/instance line, so the card's top keeps 0.12
        # under it (its bottom then sits 0.2 below the stack's base)
        card.move_to([4.9, ref1.get_bottom()[1] - 0.12 - card.height / 2, 0])

        with self.voiceover(SAY[1]) as vo:
            self.play(head.words[0].animate.set_color(IMAGE), FadeOut(VGroup(nest, right_os)), FadeIn(ref1),
                      VGroup(ibox_solid, items, an_image).animate.shift(
                          np.array([STACK_X, FLOOR_Y + 1.6, 0]) - ibox_solid.get_center()), run_time=0.9)
            # the box opens: what it held becomes three slabs, bottom-up. "OS files" and "Python"
            # merge into one slab: the boxes become its box, their letters regroup into its label.
            self.play(FadeOut(ibox_solid, scale=1.12), FadeOut(an_image),
                      LaggedStart(AnimationGroup(ReplacementTransform(VGroup(i_os.box, i_py.box), s_os.box),
                                                 TransformMatchingShapes(VGroup(i_os.text, i_py.text), s_os.text)),
                                  ReplacementTransform(i_pkg, s_pkg),
                                  ReplacementTransform(i_code, s_code), lag_ratio=0.3),
                      run_time=1.2)
            self.remove(s_os.box, s_os.text)
            stack.accept(self, *slabs)
            vo.wait_until("read-only layers")
            self.play(FadeIn(lock_g, shift=DOWN * 0.15), head.words[1].animate.set_color(IMAGE), run_time=0.6)
            vo.wait_until("Each layer")
            self.play(LaggedStart(*[Indicate(s.box, color=IMAGE, scale_factor=1.04) for s in slabs],
                                  lag_ratio=0.45), run_time=2.2)
            vo.wait_until("Beside it")
            self.play(FadeIn(card, shift=LEFT * 0.4), run_time=0.8)
            vo.wait_until("settings like")
            self.play(Indicate(card.keys["ENV"], color=TURN, scale_factor=1.15), run_time=0.9)
            vo.wait_until("and which program")
            self.play(Indicate(card.keys["ENTRYPOINT"], color=TURN, scale_factor=1.1),
                      Indicate(card.keys["CMD"], color=TURN, scale_factor=1.15), run_time=1.0)

        # ================================================================ 2 · the recipe
        page = dockerfile_page(top=0.95)
        page.shift(RIGHT * (-6.45 - page.frame.get_left()[0]))
        page.shift(UP * ((FLOOR_Y + TOP_Y) / 2 + 0.25 - page.frame.get_center()[1]))
        ln_from, ln_run, ln_copy, ln_cmd = page.lines

        def bar(ln):
            return Rectangle(width=page.frame.width - 0.2, height=0.44, stroke_width=0) \
                .set_fill(TURN, 0.22).move_to([page.frame.get_center()[0], ln.get_center()[1], 0])

        def land(slab, word):
            """The keyword tile, just left of the slab it made."""
            k = kw_tile(word)
            return k.move_to(slab.box.get_left() + LEFT * (0.15 + k.width / 2))

        k_from, k_run, k_copy = land(s_os, "FROM"), land(s_pkg, "RUN"), land(s_code, "COPY")
        brace = Brace(VGroup(s_pkg.box, s_code.box), RIGHT, buff=0.12, color=IMAGE)
        adds = tag("adds a layer", IMAGE).next_to(brace, RIGHT, buff=0.1)
        cmd_tile = card.place("CMD", card.tile('["…"]'))
        cfg_only = tag("config only", IMAGE).next_to(card.frame, DOWN, buff=0.18)

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeIn(page, shift=RIGHT * 0.4), run_time=0.8)
            hb = bar(ln_from)
            vo.wait_until("read one instruction")
            self.play(FadeIn(hb), run_time=0.3)
            self.play(TransformFromCopy(VGroup(*ln_from[:4]), k_from), run_time=0.8)
            self.play(Indicate(s_os.box, color=SYSTEM, scale_factor=1.03), run_time=0.6)
            vo.wait_until("Instructions that change")
            self.play(hb.animate.move_to(bar(ln_run)), run_time=0.3)
            vo.wait_until("like RUN")
            self.play(TransformFromCopy(VGroup(*ln_run[:3]), k_run), run_time=0.6)
            vo.wait_until("and COPY")
            self.play(hb.animate.move_to(bar(ln_copy)), run_time=0.3)
            self.play(TransformFromCopy(VGroup(*ln_copy[:4]), k_copy), run_time=0.7)
            vo.wait_until("add a layer")
            self.play(GrowFromCenter(brace), FadeIn(adds, shift=LEFT * 0.2), run_time=0.6)
            vo.wait_until("Others, like CMD")
            self.play(hb.animate.move_to(bar(ln_cmd)), run_time=0.3)
            self.play(TransformFromCopy(ln_cmd, cmd_tile, path_arc=-0.6), run_time=1.0)
            vo.wait_until("only write on")
            self.play(FadeIn(cfg_only, shift=UP * 0.15), Indicate(cmd_tile, color=IMAGE, scale_factor=1.1),
                      run_time=0.7)

        # ================================================================ 3 · container
        lock_side = lock_g.copy().arrange(DOWN, buff=0.12).next_to(s_pkg.box, RIGHT, buff=0.3)
        run_chip = docker_chip("docker run", 26)
        g1 = Glass(glass_w=GLASS_W, process="main process").on(stack)
        c1 = steady("container", 26, IMAGE).next_to(g1.slab, LEFT, buff=0.3)
        run_chip.next_to(g1.slab, LEFT, buff=0.3)
        up_y = TOP_Y + 1.2                                  # the lifted glasses' centre
        left_c = np.array([STACK_X - GLASS_W / 2 - 0.2, up_y, 0])
        right_c = np.array([STACK_X + GLASS_W / 2 + 0.2, up_y, 0])
        g2 = Glass(glass_w=GLASS_W, process="main process")
        g2.shift(right_c - g2.slab.get_center())
        c2 = steady("container", 26, IMAGE).next_to(g2.slab, RIGHT, buff=0.3)
        hub_pt = np.array([STACK_X, TOP_Y + 0.02, 0])

        def link(center):
            return Line(center + DOWN * 0.27, hub_pt, color=IMAGE, stroke_width=2.5)

        l1, l2 = link(left_c), link(right_c)
        shared = label("shared, not copied", 26, IMAGE)
        shared.move_to([right_c[0] + 0.55, (up_y + TOP_Y) / 2 - 0.05, 0], aligned_edge=LEFT)
        rm = docker_chip("--rm", 26)
        ok = VGroup(check_mark(0.36), label("image unchanged", 26, INK)).arrange(RIGHT, buff=0.15)
        ok.next_to(stack.slabs, DOWN, buff=0.3)

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(page, hb, brace, adds, cfg_only)), FadeOut(card.everything()),
                      ReplacementTransform(lock_g, lock_side), head.words[2].animate.set_color(IMAGE),
                      FadeIn(run_chip, shift=RIGHT * 0.3), run_time=0.7)
            self.play(FadeIn(g1, shift=DOWN * 0.6), run_time=0.7)
            vo.wait_until("you get a container")
            self.play(FadeTransform(run_chip, c1), run_time=0.6)
            vo.wait_until("the same layers")
            self.play(VGroup(g1, c1).animate.shift(left_c - g1.slab.get_center()),
                      FadeIn(VGroup(g2, c2), shift=DOWN * 0.3), run_time=0.8)
            self.play(Create(l1), Create(l2), FadeIn(shared, shift=LEFT * 0.2), run_time=0.6)
            vo.wait_until("plus a thin")
            self.play(Indicate(g1.text, color=IMAGE, scale_factor=1.08),
                      Indicate(g2.text, color=IMAGE, scale_factor=1.08),
                      g1.glow.animate.set_stroke(opacity=0.5), g2.glow.animate.set_stroke(opacity=0.5),
                      run_time=1.0)
            vo.wait_until("and one main process")
            self.play(Flash(g1.dot, color=IMAGE), Flash(g2.dot, color=IMAGE),
                      Indicate(g1.dot_label, color=IMAGE), Indicate(g2.dot_label, color=IMAGE),
                      run_time=1.0)
            vo.wait_until("When that process ends")
            self.play(g1.stop("stopped"), run_time=0.7)
            vo.wait_until("and dash dash rm")
            rm.next_to(g1.slab, UP, buff=0.12).align_to(g1.slab, LEFT)
            self.play(FadeIn(rm, shift=DOWN * 0.2), run_time=0.5)
            vo.wait_until("deletes it")
            # --rm stays on screen while the whole stopped container (glass, label, link) dissolves
            self.play(Indicate(rm, color=TOOL, scale_factor=1.1), FadeOut(VGroup(g1, c1, l1), shift=UP * 0.3),
                      run_time=1.0)
            vo.wait_until("The image never")
            self.play(FadeOut(rm, shift=UP * 0.2), Create(ok[0]), FadeIn(ok[1], shift=RIGHT * 0.1),
                      Indicate(VGroup(*[s.box for s in slabs]), color=IMAGE, scale_factor=1.03),
                      run_time=0.8)

        # ================================================================ 4 · class/instance, erratum
        settle = np.array([STACK_X, TOP_Y + GAP + g2.glass_h / 2, 0]) - g2.slab.get_center()
        pic = VGroup(stack, lock_side, g2, c2)
        cls_cap = VGroup(label("image = class", 28, IMAGE), label("container = instance", 28, IMAGE))
        cls_cap.arrange(DOWN, buff=0.2, aligned_edge=LEFT)

        def card_with_room(line_no, s):
            t = label(s, 23, INK)
            body = VGroup(Rectangle(width=t.width, height=0.42, stroke_width=0, fill_opacity=0), t)
            body.arrange(DOWN, buff=0.0, aligned_edge=LEFT)
            return readme_card(line_no, body), t

        s173 = "Build the docker container by running"
        s146 = "Install uv & copy source code into the container"
        card173, t173 = card_with_room(173, s173)
        card146, t146 = card_with_room(146, s146)
        cards = VGroup(card173, card146).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        cards.move_to([0, -0.35, 0]).align_to([-0.75, 0, 0], LEFT)
        err = erratum_tag().next_to(card173.frame, UP, buff=0.12).align_to(card173.frame, RIGHT)

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(shared, ok, l2, k_from, k_run, k_copy)), VGroup(g2, c2).animate.shift(settle),
                      run_time=0.8)
            shift = np.array([-6.3 - stack.slabs.get_left()[0], 0.55, 0])
            self.play(pic.animate.shift(shift), run_time=0.8)
            cls_cap.next_to(stack.slabs, DOWN, buff=0.4).align_to(stack.slabs, LEFT)
            vo.wait_until("as a class")
            self.play(FadeIn(cls_cap[0], shift=UP * 0.1), Indicate(stack.slabs, color=IMAGE, scale_factor=1.02),
                      run_time=0.6)
            vo.wait_until("and each container")
            self.play(FadeIn(cls_cap[1], shift=UP * 0.1), Indicate(g2.slab, color=IMAGE, scale_factor=1.04),
                      run_time=0.6)
            vo.wait_until("One small slip")
            # both README lines come in as one group; both get corrected when "container" is said
            self.play(FadeOut(VGroup(cls_cap, ref1)), FadeIn(card173, shift=LEFT * 0.4), run_time=0.7)
            self.play(FadeIn(card146, shift=UP * 0.3), run_time=0.6)
            w1 = word_glyphs(t173, s173, "container")
            k1 = strike(w1)
            im1 = label("image", 24, TURN).next_to(w1, UP, buff=0.08)
            w2 = word_glyphs(t146, s146, "container")
            k2 = strike(w2)
            im2 = label("image", 24, TURN).next_to(w2, UP, buff=0.08)
            vo.wait_until("the docker container")
            self.play(Create(k1), w1.animate.set_opacity(0.55), Create(k2), w2.animate.set_opacity(0.55),
                      run_time=0.5)
            self.play(FadeIn(im1, shift=DOWN * 0.1), FadeIn(im2, shift=DOWN * 0.1), FadeIn(err), run_time=0.5)
            vo.wait_until("Building makes")
            self.play(Indicate(stack.slabs, color=IMAGE, scale_factor=1.04), run_time=0.9)
            vo.wait_until("running makes")
            self.play(Indicate(g2.slab, color=IMAGE, scale_factor=1.06), Flash(g2.dot, color=IMAGE),
                      run_time=0.9)

        # ================================================================ 5 · registry and tags
        hub = RegistryShelf("registry · Docker Hub", shelf_w=11.6, shelf_h=3.9, boards=2, size=26)
        hub.move_to([0.25, -0.45, 0])
        fills = (SYSTEM, SYSTEM, LAPTOP, VENV)
        py_stack = mini_stack((SYSTEM,) * 4, glyph_w=1.2, slab_h=0.19)
        old = mini_stack(fills, glyph_w=1.2, slab_h=0.19)
        new = mini_stack(fills, glyph_w=1.2, slab_h=0.19)
        py_stack.move_to(hub.spot(1, 0, 7), aligned_edge=DOWN)
        old.move_to(hub.spot(0, 0, 7), aligned_edge=DOWN)
        new.move_to(hub.spot(0, 6, 7), aligned_edge=DOWN)
        n_py = sticky("python:3.12-slim-bookworm", size=22)
        n_dl = sticky("dlops/simple-translate:latest", size=22)
        n_py.next_to(py_stack, RIGHT, buff=0.55).shift(UP * 0.12)
        n_dl.next_to(old, RIGHT, buff=0.55).shift(UP * 0.12)
        k_py = Line(n_py.get_left(), py_stack.get_right() + RIGHT * 0.05, color=IMAGE, stroke_width=2.5)
        k_dl = Line(n_dl.get_left(), old.get_right() + RIGHT * 0.05, color=IMAGE, stroke_width=2.5)
        n_dl_new = n_dl.copy().next_to(new, LEFT, buff=0.55).align_to(n_dl, UP)
        k_dl_new = Line(n_dl_new.get_right(), new.get_left() + LEFT * 0.05, color=IMAGE, stroke_width=2.5)
        latest = word_glyphs(n_dl.text, "dlops/simple-translate:latest", ":latest")
        tag_cap = label("a tag: a name that points at one image", 28, IMAGE)
        tag_cap.next_to(hub.frame, DOWN, buff=0.22)

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(pic, cards, err, k1, k2, im1, im2)),
                      head.words[3].animate.set_color(IMAGE), run_time=0.7)
            self.play(FadeIn(hub, shift=LEFT * 0.4), run_time=0.8)
            vo.wait_until("stores images by name")
            self.play(FadeIn(py_stack, shift=DOWN * 0.3), FadeIn(old, shift=DOWN * 0.3), run_time=0.6)
            self.play(FadeIn(n_py, shift=LEFT * 0.2), Create(k_py), FadeIn(n_dl, shift=LEFT * 0.2),
                      Create(k_dl), run_time=0.7)
            vo.wait_until("A tag is")
            self.play(FadeIn(new, shift=DOWN * 0.5), latest.animate.set_color(TURN), run_time=0.6)
            self.play(Rotate(n_dl, -0.12, about_point=n_dl.get_corner(UR)), FadeOut(k_dl), run_time=0.3)
            self.play(n_dl.animate.rotate(0.12).move_to(n_dl_new), run_time=0.8)
            self.play(Create(k_dl_new), FadeIn(tag_cap, shift=UP * 0.1), run_time=0.6)

        # ================================================================ 6 · container ≠ VM
        kp = KernelPicture(3, vm_w=3.0, vm_h=2.9, gap=0.4, size=22).move_to([0, 0.35, 0])
        core = label("kernel: the core of the operating system", 28, S.GREY)
        core.next_to(kp.vms, DOWN, buff=0.4)
        iso = label("isolated processes, not machines", 28, IMAGE).move_to(core)
        ref2 = slide_ref(head, "9–12, 22–24")
        # slide 22's two kernel features on the shared bar (under the outer containers; the bar's own
        # text stays in the middle), and its "Container = User Space" beside the containers
        ns_chips = VGroup(tag("namespaces", S.GREY), tag("cgroups", S.GREY))
        uspace = label("user space", 22, S.GREY)

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(hub, py_stack, old, new, n_py, n_dl, k_py, k_dl_new, tag_cap)),
                      run_time=0.6)
            self.play(LaggedStart(*[FadeIn(v, shift=UP * 0.2) for v in kp.vms], lag_ratio=0.25), FadeIn(ref2),
                      run_time=1.2)
            vo.wait_until("A VM boots")
            self.play(LaggedStart(*[Indicate(v.kernel, color=TURN, scale_factor=1.08) for v in kp.vms],
                                  lag_ratio=0.25), run_time=1.4)
            vo.wait_until("the core of")
            self.play(FadeIn(core, shift=UP * 0.1), run_time=0.6)
            anims = kp.to_containers()
            shrink = [a for k, a in enumerate(anims) if k % 4 != 3]
            merge = [a for k, a in enumerate(anims) if k % 4 == 3]
            vo.wait_until("Containers are")
            # the kernel bars drop to the shared bar's height as the VMs shrink, so the containers
            # stand clear of them until they merge (Transform starts from where they are then)
            drop = kp.vms[0].kernel.get_center()[1] - (kp.vms.get_bottom()[1] + 0.23)
            self.play(*shrink, *[v.kernel.animate.shift(DOWN * drop) for v in kp.vms],
                      FadeTransform(core, iso), run_time=1.1)
            # "user space" comes in with "isolated processes" (after the merge it would only flash:
            # it leaves with iso at block 7's start, before the laptop outline it would cross)
            uspace.next_to(kp.vms[0].frame, LEFT, buff=0.25)
            self.play(FadeIn(uspace, shift=RIGHT * 0.15), run_time=0.5)
            vo.wait_until("that share one")
            self.play(*merge, run_time=1.0)
            self.play(Indicate(kp.bar, color=TURN, scale_factor=1.03), run_time=0.7)
            for c, v in zip(ns_chips, (kp.vms[0], kp.vms[2])):
                c.move_to([v.frame.get_center()[0], kp.bar.get_center()[1], 0])
            self.play(LaggedStart(*[FadeIn(c, scale=0.9) for c in ns_chips], lag_ratio=0.25), run_time=0.6)

        # ================================================================ 7 · Docker Desktop's VM
        dvm = kp.desktop_vm()
        inside = VGroup(*[v.frame for v in kp.vms], kp.bar, dvm)
        mac = label("Mac · Windows", 26, S.GREY)
        lap = laptop_outline(inside.width + 0.9, inside.height + mac.height + 0.85)
        lap.screen.move_to(inside.get_center() + UP * (mac.height + 0.25) / 2)
        lap.base.next_to(lap.screen, DOWN, buff=0.05)
        mac.move_to(lap.screen.get_corner(UL) + np.array([0.3, -0.22, 0]), aligned_edge=UL)
        # the cloud VM wraps only what remains (no hidden Linux VM): same top, ends under the kernel bar
        vm_top, vm_bot = lap.screen.get_top()[1], kp.bar.get_bottom()[1] - 0.3
        vm_out = box(lap.screen.width, vm_top - vm_bot, CLOUD, fill_opacity=0.04)
        vm_out.move_to([lap.screen.get_center()[0], (vm_top + vm_bot) / 2, 0])
        vm_lab = label("cloud VM", 26, CLOUD).move_to(mac, aligned_edge=LEFT)
        own = label("on a cloud VM: its own Linux", 28, CLOUD)

        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(iso, uspace)), Create(lap.screen), FadeIn(lap.base, shift=UP * 0.1),
                      FadeIn(mac),
                      run_time=1.0)
            vo.wait_until("Docker Desktop provides")
            self.play(FadeIn(dvm, shift=UP * 0.4), run_time=0.9)
            vo.wait_until("with a small")
            self.play(Indicate(dvm.text, color=INK, scale_factor=1.06), run_time=0.9)
            vo.wait_until("On a cloud VM")
            self.play(ReplacementTransform(lap.screen, vm_out), FadeOut(lap.base), FadeOut(dvm),
                      FadeTransform(mac, vm_lab), run_time=1.0)
            own.next_to(vm_out, DOWN, buff=0.25)
            vo.wait_until("Docker runs right")
            self.play(FadeIn(own, shift=UP * 0.1), Indicate(kp.bar, color=CLOUD, scale_factor=1.03),
                      run_time=0.8)

        # ================================================================ 8 · what a venv couldn't isolate
        h8 = 0.68
        st2 = LayerStack(stack_w=STACK_W, gap=GAP)
        st2.floor.move_to([-2.9, -2.05, 0])
        hole1 = st2.make(None, SYSTEM, h8, dashed=True)
        hole2 = st2.make(None, SYSTEM, h8, dashed=True)
        p2 = slab_label(st2.make(None, VENV, h8), "packages")
        y2 = slab_label(st2.make(None, LAPTOP, h8), "your code")
        new_os = slab_label(Slab(None, SYSTEM, STACK_W, h8).move_to(hole1), "OS files")
        new_lib = slab_label(Slab(None, SYSTEM, STACK_W, h8).move_to(hole2), "system libraries")
        img_lab = label("image", 28, IMAGE).next_to(y2, UP, buff=0.2)
        # L1's chips stand level with the slots they will fill, so each slides straight in as it is
        # named (stacked in reading order they would cross paths); GPU drivers stays below, outside.
        lib_c, os_c, gpu_c = VGroup(*[chip(n, ERR, size=26, fill_opacity=0.06) for n in (
            "system libraries", "the operating system's files", "GPU drivers")])
        chips_x = 0.3
        lib_c.move_to([chips_x, hole2.get_center()[1], 0], aligned_edge=LEFT)
        os_c.move_to([chips_x, hole1.get_center()[1], 0], aligned_edge=LEFT)
        gpu_c.move_to([chips_x, hole1.get_center()[1] - 0.85, 0], aligned_edge=LEFT)
        ok2 = check_mark(0.45).next_to(VGroup(hole1, hole2), LEFT, buff=0.3)
        gpu_grey = chip("GPU drivers", S.GREY, size=26, fill_opacity=0.06).move_to(gpu_c, aligned_edge=LEFT)
        hosts = label("still the host's", 26, S.GREY).next_to(gpu_grey, RIGHT, buff=0.3)
        # this picture cites what each tool isolates (SLIDES.md claim 3: slides 5–7, 10; the host's GPU
        # drivers: slide 22), so the V8 tag leaves with V8 and this one takes its spot
        ref3 = slide_ref(head, "5–7, 10, 22")
        # QA 03:06: the GPU chip (review P36, exercise D1c) greys on its own sentence, "GPU drivers
        # still come from the host." (if a SAY revision drops that sentence, it greys with the libraries)
        gpu_said = "GPU drivers still" in SAY[8]

        def gpu_out():
            return ReplacementTransform(gpu_c, gpu_grey), FadeIn(hosts, shift=LEFT * 0.1)

        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(kp, ns_chips, vm_out, vm_lab, own, ref2)), run_time=0.6)
            self.play(FadeIn(VGroup(hole1, hole2, p2, y2, img_lab), shift=UP * 0.2), FadeIn(ref3),
                      LaggedStart(*[FadeIn(c, shift=LEFT * 0.3) for c in (os_c, lib_c, gpu_c)], lag_ratio=0.2),
                      run_time=1.0)
            vo.wait_until("the system's files")
            self.play(FadeTransform(os_c, new_os), FadeOut(hole1), run_time=0.8)
            vo.wait_until("and libraries")
            self.play(FadeTransform(lib_c, new_lib), FadeOut(hole2), Create(ok2),
                      *(() if gpu_said else gpu_out()), run_time=0.8)
            vo.wait_until("is now inside")
            self.play(Indicate(VGroup(new_os.box, new_lib.box), color=SYSTEM, scale_factor=1.04),
                      Indicate(img_lab, color=IMAGE), run_time=0.9)
            if gpu_said:
                vo.wait_until("GPU drivers still")
                self.play(*gpu_out(), run_time=0.8)
                self.play(Indicate(hosts, color=INK, scale_factor=1.08), run_time=0.7)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.wait(0.2)
