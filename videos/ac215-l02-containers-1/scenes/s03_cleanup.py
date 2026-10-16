"""S03 · A clean slate, and the clone (README A1-A5, two extras).

Beats (script.md "## S03", one voiceover block each):
 0  TRACKER A1: the tracker fades in, its first dot and caption pulse YELLOW. The house laptop
    terminal (10 rows, title `laptop`, `student@laptop:~$`) fades in with a bare prompt; its title
    pulses on "Open a terminal on your laptop" and a GREY chip "Docker Desktop: running" with a
    GREEN dot appears above its top-right corner. On "On a Mac" the prompt pulses and a GREY note
    appears above the terminal's left end, one line per clause: "on a Mac: zsh, a % prompt" /
    "on Windows: Git Bash · same commands" (the terminal fills the frame down to the bottom edge, so
    the note sits above it rather than under it).
 1  TRACKER A1. `docker container ls` -> laptop/01 line 2 (squeezed: the 70-character header does
    not fit a 65-column row). The header pulses; GREY row tag under it "the columns · no rows:
    nothing running". On "If yours can't connect" a GREY chip "cannot connect? → start Docker
    Desktop" appears left of the Docker Desktop chip (above the terminal, for the same reason), and
    that chip is circled on "start Docker Desktop". ▶ your turn (wiggles on "Pause and run it").
 2  TRACKER A2. Above the terminal: README card (README.md · line 116) "Stop any container that is
    running"; the row tag "no rows: nothing running" pulses on "There's nothing to stop"; beside the
    card a GREY mono chip `docker stop <CONTAINER ID>` with the tag "only if you have one · not run
    here" under it.
 3  TRACKER A3. The terminal clears; `docker system prune` -> laptop/02 lines 2-7, line 8 cut after
    "[y/N]", 0.6 s, the `y` keystroke flashes YELLOW (on "type y"); line 9 ("0B" pulses) gets the
    GREY row tag "a fresh Docker · yours may reclaim hello-world's container" in the row under it.
    ▶ your turn.
 4  TRACKER A3. Line 5 (`  - all dangling images`) gets a YELLOW bar. The terminal shrinks to the
    3-row strip keeping lines 3-5 (the first three items). Above it (tag illustration): two small
    TEAL image stacks with sticky names `hello-world` and `<none>`; line 5 gets the GREY row tag
    "images with no name" and the `<none>` stack is swept away (FadeOut + shift) on "without a
    name". Right column: README card (README.md · line 113) "… and clear up an unused images" with
    the tag `erratum`; on "named images survive" the hello-world stack gets a GREEN check "named:
    kept"; on "With dash a" a GREY mono chip `docker system prune -a` with its caption "every
    unused image" under it (the caption pulses as it is said).
 5  TRACKER A4. The right column leaves, the hello-world image moves to the middle. The strip clears;
    `docker image ls` -> laptop/03 line 2 (squeeze). GREY row tag "no images yet · yours may list
    hello-world" under the header; the hello-world name and then its check pulse as they are
    named; YELLOW underline on Docker 29's columns "DISK USAGE  CONTENT SIZE  EXTRA"; row tag "at
    the time of recording" beside the header. ▶ your turn.
 6  TRACKER A5. The picture changes: README card (README.md · lines 122-123, NOTE quote, "your
    laptop" bold); a small BLUE VM ("last lecture") holding a GREY folder gets a RED cross on
    "doesn't help" and dims (fade, so its fill stays faint); a GREY laptop with a PURPLE `docker`
    chip on its screen appears on "Docker Desktop runs on your laptop". The card leaves and the strip
    grows to 5 rows while the picture rises into the card's room, so both commands stay on screen
    for "Pause and run both". The strip types `git clone https://github.com/dlops-io/simple-
    translate.git` (folds onto a second row) -> laptop/04 line 2; the word simple-translate copies
    down from the output into the laptop's new folder label while a GREY folder appears on its
    screen; on "then cd into" `cd simple-translate` (no output) and the prompt becomes
    `student@laptop:~/simple-translate$`, its new path flashing BLUE. A GREY row tag "README.md ·
    lines 50–51 · same as L1" beside the first `git clone` row and ▶ your turn beside the cd row
    (wiggles on "Pause and run both").
 7  TRACKER A5 · extra. The picture leaves; the strip grows back to 10 rows WITHOUT clearing (the
    clone and cd rows, with their tags, stay until the listing scrolls them off). `ls -a` (row tag
    `extra`) at the waiting prompt -> laptop/05 lines 4-12 (the clone's own listing; lines 2-3 are
    . and ..). Dockerfile.txt gets a YELLOW bar and the GREY row tag "the solution"; dashed GREY
    ghost chips `Dockerfile` and `uv.lock` appear side by side on that row, right of the listing, as
    they are named; "not in the repo" comes under the first and slides to the pair's middle.
 8  TRACKER A5 · extra. The listing clears (the ghosts and their caption stay); `docker build -t
    simple-translate -f Dockerfile .` (two rows, row tag `extra`); then `uv.lock` and the caption
    go -> laptop/07 line 7, wrapped, RED; "failed to read dockerfil|e" is underlined YELLOW and the
    `Dockerfile` ghost slides beside "no such file or directory". On "The README wants you to write
    it" a YELLOW brace grows under tracker dots 7-11 (FROM … CMD); the ghost fades up out of the
    terminal and fades up in under the brace with "5 steps" (a flight would cross the RED rows);
    the five dots pulse on "in five steps". Fade out to an empty frame.
"""

import numpy as np  # noqa: I001  (manim first, then common: common must win)
from manim import *

from explainer import style as S
from explainer.devops import line_pitch
from explainer.scene import VoiceScene

from common import (BOTTOM, BUILD, CD, CLONE, CLOUD, CONTAINER_LS, ERR, IMAGE_LS, INK, LAPTOP, MONO,
                    NARRATION, P_LAPTOP, P_LAPTOP_HOME, PRUNE, STRIP_ROWS, SYSTEM, TRACK_BOTTOM,
                    TURN, ask, attach, bare_prompt, beside, box, capture, check_mark, chip, cross_mark,
                    docker_chip, erratum_tag, folder_glyph, glyph_range, hl_bar, illustration_tag, label, laptop,
                    laptop_term, mini_stack, mono, mono_line, pin, readme_card, resize, row_tag,
                    squeeze, sticky, substring, tag, track, tracker_a, type_answer, type_cmd, under,
                    unpin)

SAY = NARRATION["S03"]

# ------------------------------------------------------------------ real outputs (file line numbers)
LS_A = "ls -a"                                           # extra (not in the README)
STOP = "docker stop <CONTAINER ID>"                      # README.md:116, said, not run
PRUNE_A = "docker system prune -a"                       # said, not run

C01 = capture("01")                                      # laptop/01-container-ls.txt
assert C01.cmd == CONTAINER_LS, C01.cmd
PS_HEAD = squeeze(C01.at(2))                             # line 2: 70 chars -> 58 (65-column rows)

C02 = capture("02")                                      # laptop/02-system-prune.txt
assert C02.cmd == PRUNE, C02.cmd
PRUNE_LIST = C02.at((2, 7))                              # WARNING! … unused build cache, ""
PRUNE_ASK = ask(C02.line(8), "[y/N]")                    # cut after [y/N]; the y is typed
PRUNE_TOTAL = C02.line(9)
assert C02.line(5) == "  - all dangling images" and PRUNE_TOTAL == "Total reclaimed space: 0B"

C03 = capture("03")                                      # laptop/03-image-ls.txt
assert C03.cmd == IMAGE_LS, C03.cmd
IMG_HEAD = squeeze(C03.at(2))[0]
DOCKER29 = "DISK USAGE  CONTENT SIZE  EXTRA"
assert DOCKER29 in IMG_HEAD, IMG_HEAD

C04 = capture("04")                                      # laptop/04-clone.txt
assert C04.cmd == CLONE, C04.cmd
CLONE_OUT = C04.at(2)                                    # Cloning into 'simple-translate'...

C05 = capture("05")                                      # laptop/05-ls.txt
assert C05.cmd == LS_A, C05.cmd
LISTING = C05.at((4, 12))                                # .git … pyproject.toml
assert "Dockerfile.txt" in LISTING and "Dockerfile" not in LISTING and "uv.lock" not in LISTING

C07 = capture("07")                                      # laptop/07-build-no-dockerfile.txt
assert C07.cmd == BUILD, C07.cmd
BUILD_ERR = C07.line(7)
assert "failed to read dockerfile" in BUILD_ERR

# README.md lines 122-123 (the NOTE under "Clone the github repository"), checked against the file
NOTE_1 = "If you cloned earlier on a VM, that doesn't help here —"
NOTE_2 = "Docker Desktop runs on your laptop, so clone the repo locally:"

# ------------------------------------------------------------------ small pictures
def row_y(t, i: int) -> float:
    """Centre height of text row i of terminal t (wherever the terminal is now)."""
    ln = mono_line("|", t.size)
    t._place(ln, i)
    return ln.strut.get_center()[1]


def at_row(mob, t, i: int, x: float | None = None):
    """Left edge at x (default: the terminal's text column), centred on row i."""
    x = t._slot(0)[0] if x is None else x
    return mob.move_to([x + mob.width / 2, row_y(t, i), 0])


def turn_tag() -> VGroup:
    """YELLOW '▶ your turn', the height of a terminal row."""
    return row_tag("▶ your turn", TURN)


def status_chip(s: str, size: float = 22) -> VGroup:
    """A GREY chip with a GREEN status light ('Docker Desktop: running'). .box .dot .text"""
    t = label(s, size, INK)
    d = Dot(radius=0.08, color=S.GREEN)
    inner = VGroup(d, t).arrange(RIGHT, buff=0.16)
    h = mono("|", size).height + 0.24
    b = box(inner.width + 0.5, h, S.GREY, fill_opacity=0.16, radius=h / 2.6)
    inner.move_to(b)
    g = VGroup(b, inner)
    g.box, g.dot, g.text = b, d, t
    return g


def ghost(s: str, size: float = 20) -> VGroup:
    """A dashed GREY chip the height of a terminal row: a file that is not there. .box .text"""
    t = mono(s, size, S.GREY)
    w, h = t.width + 0.42, 0.38
    # short, dense dashes and nearly square corners: box(dashed=True)'s long dashes put a single
    # curved dash on each short side, which reads as a pair of brackets around the name
    r = RoundedRectangle(width=w, height=h, corner_radius=0.04)
    b = DashedVMobject(r, num_dashes=round(2 * (w + h) / 0.15), dashed_ratio=0.6)
    b.set_stroke(S.GREY, 2.5)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def image_glyph(name: str) -> VGroup:
    """An image as a small TEAL stack with its name on a sticky note above. .stack .note"""
    st = mini_stack((SYSTEM, SYSTEM, LAPTOP), glyph_w=1.9, slab_h=0.27, gap=0.06)
    note = sticky(name)
    note.next_to(st, UP, buff=0.2)
    g = VGroup(st, note)
    g.stack, g.note = st, note
    return g


def vm_box() -> VGroup:
    """Last lecture's VM (BLUE) holding a clone (GREY folder). .frame .folder .caption"""
    f = box(2.4, 1.45, CLOUD, fill_opacity=0.1)
    title = label("VM", 22, CLOUD).move_to(f.get_corner(UL) + np.array([0.38, -0.28, 0]))
    fold = folder_glyph(0.55, LAPTOP).move_to(f.get_center() + DOWN * 0.12)
    cap = label("last lecture", 20, S.GREY).next_to(f, DOWN, buff=0.15)
    g = VGroup(f, title, fold, cap)
    g.frame, g.folder, g.caption = f, fold, cap
    return g


def brace_under(mob, color=TURN) -> VMobject:
    """A thin bracket under `mob` (a flat brace: ticks up at both ends, a notch in the middle)."""
    l, r, y = mob.get_left()[0] - 0.04, mob.get_right()[0] + 0.04, mob.get_bottom()[1] - 0.1
    c = (l + r) / 2
    m = VMobject(stroke_color=color, stroke_width=3)
    m.set_points_as_corners([[l, y + 0.08, 0], [l, y, 0], [c - 0.08, y, 0], [c, y - 0.1, 0],
                             [c + 0.08, y, 0], [r, y, 0], [r, y + 0.08, 0]])
    return m


def lead(vo, phrase: str, early: float) -> None:
    """Wait until `early` seconds before `phrase` is spoken (a typed command lands on its words)."""
    dt = vo.time_until(phrase) - early
    if dt > 1 / 60:
        vo.scene.wait(dt)


# ------------------------------------------------------------------ the scene
class CleanSlate(VoiceScene):
    def construct(self):
        assert len(SAY) == 9, f"S03 has {len(SAY)} SAY lines; this scene times 9"

        tr = tracker_a(1)
        t = laptop_term(10, prompt=P_LAPTOP_HOME)          # 12.6 wide, top edge 1.38, bottom -3.5
        band_y = (t.box.get_top()[1] + TRACK_BOTTOM) / 2   # the free band between tracker and terminal
        t_left, t_right = t.box.get_left()[0], t.box.get_right()[0]

        # ========================================================== 0 · open a terminal
        note = VGroup(label("on a Mac: zsh, a % prompt", 22, S.GREY),
                      label("on Windows: Git Bash · same commands", 22, S.GREY))
        note.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        note.move_to([t_left + note.width / 2, band_y, 0])
        dd = status_chip("Docker Desktop: running")
        dd.move_to([t_right - dd.width / 2, band_y, 0])

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.1), run_time=0.6)
            self.play(Indicate(VGroup(tr.dots[0], tr.caption), color=TURN, scale_factor=1.15), run_time=0.8)
            self.play(FadeIn(t), run_time=0.6)
            p0 = bare_prompt(self, t)
            vo.wait_until("Open a terminal")
            self.play(Indicate(t.title, color=INK, scale_factor=1.4), run_time=0.8)
            self.play(FadeIn(dd, shift=LEFT * 0.2), run_time=0.5)
            self.play(Flash(dd.dot, color=S.GREEN, line_length=0.12, flash_radius=0.16), run_time=0.6)
            vo.wait_until("On a Mac")
            self.play(Indicate(substring(p0, P_LAPTOP_HOME), color=TURN, scale_factor=1.12), run_time=0.7)
            self.play(FadeIn(note[0], shift=UP * 0.1), run_time=0.5)
            vo.wait_until("on Windows")
            self.play(FadeIn(note[1], shift=UP * 0.1), run_time=0.5)

        # ========================================================== 1 · docker container ls
        cc = chip("cannot connect? → start Docker Desktop", S.GREY, size=22)
        cc.move_to([dd.get_left()[0] - 0.35 - cc.width / 2, band_y, 0])

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(note, shift=UP * 0.1), run_time=0.3)
            c1 = type_cmd(self, t, CONTAINER_LS, 0.8)
            h1 = t.print(self, PS_HEAD, run_time=0.4)[0]
            vo.wait_until("Here it shows")
            self.play(Indicate(h1.glyphs, color=INK, scale_factor=1.04), run_time=0.8)
            cols = at_row(row_tag("the columns · no rows: nothing running"), t, 2)
            pin(self, h1, cols, run_time=0.5)
            vo.wait_until("If yours can't connect")
            self.play(FadeIn(cc, shift=RIGHT * 0.2), run_time=0.5)
            vo.wait_until("start Docker Desktop")
            self.play(Circumscribe(dd, color=TURN, buff=0.06), run_time=1.0)
            yt1 = beside(turn_tag(), c1)
            lead(vo, "Pause and run it", 0.8)
            pin(self, c1, yt1)
            vo.wait_until("Pause and run it")
            self.play(Wiggle(yt1, scale_value=1.15, rotation_angle=0.025 * TAU), run_time=0.7)

        # ========================================================== 2 · stop any running container
        card2 = readme_card(116, "Stop any container that is running")
        card2.move_to([t_left + card2.width / 2, band_y, 0])
        stop = chip(STOP, S.GREY, size=22, font=MONO)
        only = tag("only if you have one · not run here", S.GREY)
        side = VGroup(stop, only).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        side.move_to([card2.get_right()[0] + 0.4 + side.width / 2, band_y, 0])

        with self.voiceover(SAY[2]) as vo:
            self.wait(0.3)
            unpin(self, [(c1, yt1)], 0.3, FadeOut(VGroup(cc, dd), shift=UP * 0.1), track(tr, 2))
            self.play(FadeIn(card2, shift=DOWN * 0.15), run_time=0.6)
            vo.wait_until("There's nothing to stop")
            self.play(Indicate(cols.text, color=INK, scale_factor=1.1), run_time=0.8)
            vo.wait_until("if you have one")
            self.play(FadeIn(stop, shift=LEFT * 0.2), run_time=0.5)
            vo.wait_until("docker stop with")
            # a small scale: at 1.15 the 14 glyphs grow over the space and read "stop<CONTAINER ID>"
            self.play(Indicate(substring_text(stop.text, STOP, "<CONTAINER ID>"), color=TURN, scale_factor=1.05),
                      run_time=0.7)
            self.play(FadeIn(only, shift=UP * 0.1), run_time=0.4)

        # ========================================================== 3 · docker system prune
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(card2, side), shift=UP * 0.1), track(tr, 3), run_time=0.5)
            t.clear(self)
            c3 = type_cmd(self, t, PRUNE, 0.85)
            vo.wait_until("It lists what")
            t.print(self, PRUNE_LIST, run_time=0.8, lag=0.12)
            q = t.print(self, [PRUNE_ASK], run_time=0.3)[0]
            asked = self.renderer.time
            vo.wait_until("type y")
            type_answer(self, t, q, PRUNE_ASK, "y", asked)
            vo.wait_until("Nothing to reclaim")
            tot = t.print(self, [PRUNE_TOTAL], run_time=0.3)[0]
            self.play(Indicate(substring(tot, "0B"), color=INK, scale_factor=1.4), run_time=0.7)
            vo.wait_until("yours may delete")
            fresh = at_row(row_tag("a fresh Docker · yours may reclaim hello-world's container"), t, 9)
            pin(self, tot, fresh, run_time=0.5)
            yt3 = beside(turn_tag(), c3)
            lead(vo, "Pause and run it", 0.8)
            pin(self, c3, yt3)
            vo.wait_until("Pause and run it")
            self.play(Wiggle(yt3, scale_value=1.15, rotation_angle=0.025 * TAU), run_time=0.7)

        # ========================================================== 4 · dangling images (V: two stacks)
        l3, l4, l5 = t.find("all stopped containers"), t.find("all networks"), t.find("all dangling images")
        bar5 = hl_bar(l5.glyphs, TURN, 0.25)
        none_tag = row_tag("images with no name")

        named = image_glyph("hello-world")
        nameless = image_glyph("<none>")
        pair = VGroup(named, nameless).arrange(RIGHT, buff=1.1, aligned_edge=DOWN)
        pair.move_to([-3.3, 0.75, 0])
        ill = illustration_tag().move_to([t_left + 0.95, 2.35, 0])
        kept = VGroup(check_mark(0.32, S.GREEN), label("named: kept", 22, S.GREY)).arrange(RIGHT, buff=0.15)
        kept.next_to(named.stack, DOWN, buff=0.3)

        card4 = readme_card(113, "… and clear up an unused images")
        card4.move_to([3.4, 2.0, 0])
        err4 = erratum_tag().next_to(card4, DOWN, buff=0.18).align_to(card4, RIGHT)
        all_chip = chip(PRUNE_A, S.GREY, size=22, font=MONO).move_to([3.4, 0.0, 0])
        every = label("every unused image", 22, S.GREY).next_to(all_chip, DOWN, buff=0.2)

        with self.voiceover(SAY[4]) as vo:
            unpin(self, [(c3, yt3)], 0.3)
            l5.add_to_back(bar5)
            self.add(l5)
            self.play(FadeIn(bar5), Indicate(l5.glyphs, color=INK, scale_factor=1.06), run_time=0.6)
            resize(self, t, STRIP_ROWS, keep=[l3, l4, l5])
            vo.wait_until("dangling images")
            self.play(FadeIn(pair, shift=UP * 0.2), FadeIn(ill), run_time=0.6)
            vo.wait_until("the ones without")
            beside(none_tag, l5)
            pin(self, l5, none_tag, run_time=0.4)
            vo.wait_until("without a name")
            self.play(Indicate(nameless.note, color=INK, scale_factor=1.15), run_time=0.5)
            self.play(FadeOut(nameless, shift=RIGHT * 1.0 + DOWN * 0.4), run_time=0.7)
            vo.wait_until("Despite the README")
            self.play(FadeIn(card4, shift=DOWN * 0.15), run_time=0.6)
            self.play(FadeIn(err4, scale=1.3), run_time=0.4)
            vo.wait_until("named images survive")
            self.play(Create(kept[0]), FadeIn(kept[1], shift=UP * 0.1), run_time=0.6)
            vo.wait_until("With dash a")
            # the caption comes with the chip (on its own words it showed for under a second)
            self.play(FadeIn(all_chip, shift=UP * 0.15), FadeIn(every, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(substring_text(all_chip.text, PRUNE_A, "-a"), color=TURN, scale_factor=1.5), run_time=0.6)
            vo.wait_until("every unused image")
            self.play(Indicate(every, color=INK, scale_factor=1.1), run_time=0.6)

        # ========================================================== 5 · docker image ls
        survivor = VGroup(named, kept)
        s_to = survivor.copy().move_to([0.4, 0.55, 0])
        ill_to = ill.copy().next_to(s_to[0].note, LEFT, buff=0.6)
        cap5 = row_tag("no images yet · yours may list hello-world")
        rec5 = row_tag("at the time of recording")

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(card4, err4, all_chip, every), shift=UP * 0.1), track(tr, 4),
                      survivor.animate.move_to(s_to), ill.animate.move_to(ill_to),
                      run_time=0.7)
            t.clear(self)
            c5 = type_cmd(self, t, IMAGE_LS, 0.7)
            h5 = t.print(self, [IMG_HEAD], run_time=0.4)[0]
            vo.wait_until("The list is empty")
            at_row(cap5, t, 2)
            pin(self, h5, cap5, run_time=0.5)
            vo.wait_until("yours may still show")
            self.play(Indicate(named.note, color=INK, scale_factor=1.2), run_time=0.8)
            vo.wait_until("it has a name")
            self.play(Indicate(kept, color=S.GREEN, scale_factor=1.2), run_time=0.8)
            vo.wait_until("Your columns may differ")
            ul5 = under(substring(h5, DOCKER29), TURN, y=h5.strut.get_bottom()[1] - 0.01)
            self.play(Create(ul5), run_time=0.6)
            attach(self, h5, ul5)
            vo.wait_until("this is Docker 29")
            beside(rec5, h5)
            pin(self, h5, rec5, run_time=0.5)
            yt5 = beside(turn_tag(), c5)
            self.wait(0.6)
            pin(self, c5, yt5)

        # ========================================================== 6 · the clone, on your laptop
        lines = VGroup(label(NOTE_1, 22, INK), label(NOTE_2, 22, INK, t2w={"your laptop": BOLD}))
        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        card6 = readme_card((122, 123), lines, quote=True)
        card6.move_to([0, 2.75 - card6.height / 2, 0])
        glyph_top = card6.get_bottom()[1] - 0.3
        vm = vm_box()
        vm.shift(np.array([-2.9, glyph_top, 0]) - vm.frame.get_top())
        x_vm = cross_mark(1.0, ERR, stroke=7).move_to(vm.frame)
        lap = laptop(2.4, LAPTOP)
        lap.shift(np.array([2.6, glyph_top, 0]) - lap.screen.get_top())
        dock = docker_chip("docker", size=20).move_to(lap.screen.get_center() + UP * 0.36)
        pic = VGroup(vm, x_vm, lap, dock)
        fold = folder_glyph(0.5, LAPTOP)
        lap_name = mono("simple-translate", 20, S.GREY)
        same = row_tag([("README.md", "mono"), ("· lines 50–51 · same as L1", "label")])
        # Before the clone the card leaves and the strip grows to 5 rows, so that both commands
        # (git clone on two rows, its output, cd, the new prompt) stay on screen for "Pause and
        # run both"; the picture rises into the card's room, centred between tracker and strip.
        strip5_top = BOTTOM + 5 * line_pitch(t.size) + 0.85
        pic_low = lap.get_bottom()[1] - 0.15 - lap_name.height        # the folder label's bottom
        rise = (strip5_top + TRACK_BOTTOM) / 2 - (glyph_top + pic_low) / 2

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(survivor, ill), shift=UP * 0.1), track(tr, 5), run_time=0.6)
            t.clear(self)
            vo.wait_until("As the README notes")
            self.play(FadeIn(card6, shift=DOWN * 0.15), run_time=0.6)
            vo.wait_until("a clone on last")
            self.play(FadeIn(vm, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("doesn't help")
            # fade(), not set_opacity(): the VM keeps its faint fill (set_opacity(0.45) filled it solid)
            self.play(Create(x_vm), vm.animate.fade(0.55), run_time=0.6)
            vo.wait_until("Docker Desktop runs")
            self.play(FadeIn(lap, shift=UP * 0.15), run_time=0.6)
            self.play(FadeIn(dock, scale=0.8), run_time=0.3)
            self.play(FadeOut(card6, shift=UP * 0.15), run_time=0.3)
            resize(self, t, 5, extra=[pic.animate.shift(UP * rise)], run_time=0.6)
            fold.move_to(lap.screen.get_center() + DOWN * 0.3)
            lap_name.next_to(lap, DOWN, buff=0.15)
            lead(vo, "Clone it here", 0.8)
            c6a = type_cmd(self, t, CLONE, 1.0)
            out6 = t.print(self, CLONE_OUT, run_time=0.3)[0]
            self.play(TransformFromCopy(substring(out6, "simple-translate"), lap_name),
                      GrowFromCenter(fold), run_time=0.6)
            vo.wait_until("then cd into")
            c6 = type_cmd(self, t, CD, 0.5)
            t.set_prompt(P_LAPTOP)
            p6 = bare_prompt(self, t)
            self.play(Indicate(substring(p6, "~/simple-translate"), color=CLOUD, scale_factor=1.15), run_time=0.5)
            # the README tag beside the clone command (README.md:50-51), ▶ your turn beside cd
            pin(self, c6a.rows[0], beside(same, c6a.rows[0]), run_time=0.4)
            yt6 = beside(turn_tag(), c6)
            lead(vo, "Pause and run both", 0.4)
            pin(self, c6, yt6, run_time=0.4)
            self.play(Wiggle(yt6, scale_value=1.15, rotation_angle=0.025 * TAU), run_time=0.6)

        # ========================================================== 7 · ls -a (extra)
        g_df, g_uv = ghost("Dockerfile"), ghost("uv.lock")
        not_repo = label("not in the repo", 20, S.GREY)
        sol = row_tag("the solution")

        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(vm, x_vm, lap, dock, fold, lap_name), shift=UP * 0.1),
                      track(tr, 5, extra=True), run_time=0.6)
            # no clear: the clone and cd rows (with their tags) stay while the strip grows back to
            # 10 rows and `ls -a` is typed at the waiting prompt under them, so a viewer who pauses a
            # moment after "Pause and run both" still has the clone URL; the listing scrolls them off
            resize(self, t, 10)
            lead(vo, "ls dash a", 0.5)
            c7 = type_cmd(self, t, LS_A, 0.4)
            pin(self, c7, beside(row_tag("extra"), c7), run_time=0.3)
            out7 = t.print(self, LISTING, run_time=0.9, lag=0.1)
            assert list(t.lines).index(c7) == 0, "the listing scrolls `ls -a` up to the first row"
            df = out7[LISTING.index("Dockerfile.txt")]
            vo.wait_until("There's the solution")
            bar7 = hl_bar(df.glyphs, TURN, 0.25)
            df.add_to_back(bar7)
            self.add(df)
            beside(sol, df)
            self.play(FadeIn(bar7), run_time=0.4)
            pin(self, df, sol, run_time=0.4)
            vo.wait_until("Dockerfile.txt")
            self.play(Indicate(df.glyphs, color=INK, scale_factor=1.12), run_time=0.7)
            vo.wait_until("but no file called")
            row_df = list(t.lines).index(df)
            gx = sol.get_right()[0] + 1.4
            at_row(g_df, t, row_df, x=gx)
            at_row(g_uv, t, row_df, x=g_df.get_right()[0] + 0.35)
            # "not in the repo" comes under the first ghost and slides to the middle of the pair when
            # uv.lock joins it (only on the sentence's last words it showed for under a second)
            not_repo.move_to([g_df.get_center()[0], row_y(t, row_df + 1), 0])
            self.play(FadeIn(g_df, shift=LEFT * 0.2), run_time=0.5)
            self.play(FadeIn(not_repo, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("and no uv.lock")
            self.play(FadeIn(g_uv, shift=LEFT * 0.2),
                      not_repo.animate.set_x(VGroup(g_df, g_uv).get_center()[0]), run_time=0.5)

        # ========================================================== 8 · the build fails (extra here)
        five = VGroup(*tr.dots[6:11])
        br = brace_under(five)
        steps5 = label("5 steps", 22, TURN)

        with self.voiceover(SAY[8]) as vo:
            # the listing clears; both ghosts and "not in the repo" stay while the build command is
            # typed (rows 0-1, above them), then uv.lock and the caption go and the Dockerfile ghost stays
            t.clear(self)
            c8 = type_cmd(self, t, BUILD, 1.3)
            self.play(FadeOut(VGroup(g_uv, not_repo)), run_time=0.3)
            pin(self, c8.rows[1], beside(row_tag("extra"), c8.rows[1]), run_time=0.3)
            vo.wait_until("failed to read")
            err = t.print(self, [BUILD_ERR], color=ERR, wrap=True, run_time=0.4)
            cut = len(err[0].text)                       # the wrap splits "dockerfile" after "dockerfil"
            part1 = substring(err[0], "failed to read dockerfil")
            part2 = glyph_range(err[1], 0, len("failed to read dockerfile") - len("failed to read dockerfil"))
            assert cut == t.max_chars
            u1 = under(part1, TURN, y=err[0].strut.get_bottom()[1] - 0.01)
            u2 = under(part2, TURN, y=err[1].strut.get_bottom()[1] - 0.01)
            self.play(Create(u1), Create(u2), run_time=0.5)
            attach(self, err[0], u1)
            attach(self, err[1], u2)
            gone = substring(err[1], "no such file or directory")
            # along its own empty row to the right, then up beside the text (a straight diagonal
            # crossed "or directory")
            p0 = g_df.get_center()
            p1 = np.array([gone.get_right()[0] + 0.45 + g_df.width / 2, row_y(t, 3), 0])
            r = min(0.2, (p1[1] - p0[1]) / 2)
            assert p1[0] - p0[0] > r and r > 0, "the ghost moves right, then up one row"
            route = VMobject()
            route.start_new_path(p0)
            route.add_line_to(np.array([p1[0] - r, p0[1], 0]))
            route.add_quadratic_bezier_curve_to(np.array([p1[0], p0[1], 0]), np.array([p1[0], p0[1] + r, 0]))
            route.add_line_to(p1)
            self.play(MoveAlongPath(g_df, route), run_time=0.6)
            self.play(Wiggle(g_df, scale_value=1.15, rotation_angle=0.02 * TAU), run_time=0.45)
            vo.wait_until("The README wants")
            steps5.next_to(br, DOWN, buff=0.2)
            row5 = VGroup(g_df.copy(), steps5.copy()).arrange(RIGHT, buff=0.25)
            row5.next_to(br, DOWN, buff=0.18).align_to(br, LEFT).shift(LEFT * 0.3)
            # the ghost leaves the terminal in place and reappears under the brace, both drifting up:
            # a flight to the tracker would cross the RED error row, which fills the terminal's width
            g_up = g_df.copy().move_to(row5[0])
            self.play(Create(br), run_time=0.4)
            # (a short drift for the one that leaves: 0.3 reached row 2's YELLOW underline)
            self.play(FadeOut(g_df, shift=UP * 0.1), FadeIn(g_up, shift=UP * 0.3),
                      FadeIn(steps5.move_to(row5[1]), shift=LEFT * 0.1), run_time=0.7)
            vo.wait_until("in five steps")
            self.play(LaggedStart(*[Indicate(d, color=TURN, scale_factor=2.0) for d in five], lag_ratio=0.25),
                      run_time=1.0)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)


def substring_text(t: Text, s: str, sub: str) -> VGroup:
    """The glyphs of `sub` in a one-line Text made from string `s` (spaces have no glyphs)."""
    i = s.find(sub)
    if i < 0:
        raise ValueError(f"{sub!r} not in {s!r}")
    a, n = len("".join(s[:i].split())), len("".join(sub.split()))
    return VGroup(*t.submobjects[a:a + n])
