"""S14 · A VM with only Docker (README C1-C4: create, SSH, install Docker, its version; V8, S14 half).

Beats (script.md "## S14", one voiceover block each):
 0  S13 ended on an empty frame: TRACKER B4 · extra fades in and switches to "README › Running App on
    VM using Docker" (7 dots); its section name pulses. "First, create a VM": C1, a schematic console
    (browser `console.cloud.google.com/compute/instances`, tag `illustration`): "Compute Engine ›
    VM instances" and a BLUE "Create instance" button that pulses and becomes the form's title. "The
    README gives no settings": GREY footnote "the README gives no settings: sensible choices". The
    rows fill as named: Name `ac215-l02`, Machine type `e2-small`, Boot disk `Debian GNU/Linux 12
    (bookworm)`; footnote "Debian 13 works too", then "· E2 = amd64" (amd64 BLUE, e2-small pulses
    BLUE). "The meter starts": the GOLD dial (no digits) fades in at the right and sweeps; GOLD tags
    "billed per second / while running" and "disk: billed / while it exists" (the boot disk row
    pulses GOLD).
 1  TRACKER C2. Create -> the form collapses into the instance row (GREEN check, `ac215-l02`,
    `e2-small`, SSH); SSH is clicked; the browser becomes the VM terminal (9 rows, `ssh · ac215-l02`,
    `student@ac215-l02:~$`) while the dial moves into a badge top right (a BLUE `ac215-l02` box and
    the dial, which keeps sweeping to the end of the scene). "Pause now": ▶ your turn beside the
    prompt; "until its SSH terminal is open": the title pulses.
 2  TRACKER C3. It types `sudo apt install docker.io` (README.md line 210); "Pause and run it": ▶ your
    turn. "In our stand-in": vm-debian12/01: 4-8 (+Done), lines 7-8 RED, row tag `stand-in · empty
    package lists` on line 7; "it fails": the RED rows pulse. "unable to locate package": a small GREY
    "Debian 13" card above the terminal shows vm-debian13/01: 7 (RED). "If yours installed": GREY
    note "installed? / → skip to the version check" left of the card.
 3  The card and note go; the terminal shrinks to the strip (the RED rows stay, with their tag).
    Above it: README card `README.md · line 210` (`sudo apt install docker.io`) with tag `erratum`;
    "skips sudo apt-get update": README card `README.md · line 44` ("Update OS packages: `sudo apt-get
    update`"), "used in lecture 1": GREY caption "README › Installing App on VM Manually · lecture 1"
    and its command pulses. "Without it": an ORANGE open book "package lists" stands empty; "may be
    empty, as here": GREY label "empty, or out of date" and the strip's RED rows pulse. "Run the
    update first": TRACKER C3 · extra; the strip types `sudo apt-get update` (row tag `extra`) ->
    vm-debian12/02: 8-9 (+Done); the book's pages fill with ORANGE lines. "pause after it": ▶ your
    turn.
 4  TRACKER C3. The picture goes; the strip grows to 9 rows and types `sudo apt install docker.io`
    -> vm-debian12/03: 4-6 (+Done), 55-57 (57 wraps), 58 cut after `[Y/n]`. "92 new packages":
    YELLOW bars behind lines 55-56; "a 107 megabyte download": `107 MB` underlined, GREY row tag
    "download"; "on Debian 12": GREY row tag "package list varies by VM" in the title bar; "on Debian
    13": the GREY "Debian 13" card shows vm-debian13/03: 77-78, `91` and `118 MB` underlined. "Answer
    Y": the `Y` is typed and flashes YELLOW; then `…`, 560, 581. "Pause and run it": ▶ your turn on
    the answer row (the command row has scrolled away by then).
 5  TRACKER C4. It types `sudo docker --version` -> vm-debian12/04: 2. "Debian's own Docker
    package": PURPLE chip `docker.io` · "Debian's package" above the terminal, left. "20.10.24":
    underlined; "26.1.5 on Debian 13": the GREY "Debian 13" card shows vm-debian13/04: 2, `26.1.5`
    underlined; "at the time of recording": that tag on the version row and on the card's top edge.
    "Older than the laptop's": GREY note "laptop: Docker 29.8.2" (laptop/00 line 4) under the chip.
 6  The chip, card and note go; the terminal shrinks to the strip. V8 (S14 half) above it: the BLUE
    VM `ac215-l02` with its own bar "Debian · Linux kernel"; the PURPLE `dockerd` block drops onto
    the bar; an empty dashed TEAL "container" slot above it. "there's no hidden VM": S02's dashed
    GREY "Linux VM" box appears small at the right and is crossed out (GREY); "unlike Docker
    Desktop": caption "Docker Desktop only".
 7  V8 fades. TRACKER C4 · extra. The strip grows to 5 rows (the error is 4 rows wrapped); above it a
    PURPLE door `/var/run/docker.sock` with a GREY lock and the PURPLE `dockerd` box behind it. "Without
    it": the strip types `docker ps` (row tag `extra`). "is refused": a PURPLE `docker ps` chip rides a
    PINK route to the door and bounces back, the door flashes RED, a RED cross; the strip prints
    vm-debian12/05: 2 (wrap) in RED. "permission denied on the Docker socket": `permission denied` and
    `/var/run/docker.sock` underline RED, the door label pulses; "the door to Docker's background
    service": GREY caption "background service" under `dockerd`. "Only root and the docker group":
    two GREY keys "root" and "docker group" fade in; the first one slides into the lock. Fade out to
    an empty frame.
"""

import numpy as np  # noqa: I001  (manim first, then common: common must win)
from manim import *

from explainer import style as S
from explainer.devops import MONO, OUTPUT, TERM_BG, browser_window, form_rows
from explainer.scene import VoiceScene

from common import (APT_DOCKER, APT_UPDATE, CLOUD, COST, DOCKER_VERSION, ERR, INK, LAPTOP_DIR,
                    NARRATION, SECTION_C, SYSTEM, TOOL, TURN, VM12, VM13, VM_HOST, CostDial,
                    ask, attach, bare_prompt, beside, box, capture, check_mark, chip, cross_mark,
                    erratum_tag, illustration_tag, label, lock_glyph, mono, mono_line, pin,
                    plus_done, readme_card, resize, route, row_tag, substring, track, tracker_b,
                    tracker_c, type_answer, type_cmd, under, unpin, vm_term, vm_with_docker,
                    your_turn)

SAY = NARRATION["S14"]

# ------------------------------------------------------------------ real outputs (file line numbers)
C01 = capture("01", VM12)                       # captured as `yes | sudo apt install docker.io`
assert C01.cmd == "yes | " + APT_DOCKER and C01.exit == 100, C01.cmd
OUT01 = plus_done(C01.at((4, 8)))
assert OUT01[3] == "E: Unable to locate package docker.io", OUT01
D01 = capture("01", VM13).line(7)
assert D01 == "Error: Unable to locate package docker.io", D01

C02 = capture("02", VM12)
assert C02.cmd == APT_UPDATE and C02.exit == 0, C02.cmd
OUT02 = plus_done(C02.at(8, 9))
assert OUT02[0].startswith("Fetched ") and OUT02[1] == "Reading package lists... Done", OUT02

C03 = capture("03", VM12)                       # captured as `yes | sudo apt install docker.io`
assert C03.cmd == "yes | " + APT_DOCKER and C03.exit == 0, C03.cmd
OUT03_A = plus_done(C03.at((4, 6))) + C03.at((55, 57))
ASK58 = ask(C03.line(58), "[Y/n]")
OUT03_B = ["…"] + C03.at(560, 581)
assert OUT03_A[3].startswith("1 upgraded, 92 newly installed") and OUT03_A[4] == "Need to get 107 MB of archives."
assert ASK58 == "Do you want to continue? [Y/n]", ASK58
assert OUT03_B[1].startswith("Setting up docker.io (20.10.24") and OUT03_B[2].startswith("Processing triggers")
D03 = [s.strip() for s in capture("03", VM13).at(77, 78)]   # the card drops apt 3's two-space indent
assert D03 == ["Upgrading: 1, Installing: 91, Removing: 0, Not Upgrading: 0", "Download size: 118 MB"], D03

C04 = capture("04", VM12)
assert C04.cmd == DOCKER_VERSION, C04.cmd
V12 = C04.line(2)
V13 = capture("04", VM13).line(2)
assert V12.startswith("Docker version 20.10.24") and V13.startswith("Docker version 26.1.5"), (V12, V13)
LAPTOP_V = capture("00", LAPTOP_DIR).line(4)
assert LAPTOP_V == "Docker client 29.8.2, engine 29.8.2", LAPTOP_V

C05 = capture("05", VM12)
PS = C05.cmd
assert PS == "docker ps" and C05.exit == 1, PS
ERR05 = C05.line(2)
assert ERR05.startswith("permission denied while trying to connect to the Docker daemon socket"), ERR05

URL = "console.cloud.google.com/compute/instances"
FIELDS = [("Name", VM_HOST), ("Machine type", "e2-small"), ("Boot disk", "Debian GNU/Linux 12 (bookworm)")]
README_210 = APT_DOCKER                          # README.md:210 "* `sudo apt install docker.io`"
README_44 = ("Update OS packages:", APT_UPDATE)    # README.md:44 "* Update OS packages: `sudo apt-get update`"

# ------------------------------------------------------------------ layout
BR_LEFT, BR_TOP, BR_W, BR_H = -6.5, 2.62, 8.8, 4.3    # the console (beats 0-1)
DIAL_C = np.array([3.3, 1.75, 0])                      # the big dial (beat 0)
BADGE_DIAL = np.array([6.2, 3.13, 0])                  # the badge dial (beats 1-7)
RATE = 1 / 60                                          # dial turns per second while the VM exists
ROWS = 9                                               # the VM terminal (top edge at y 0.98)
CARD_RIGHT, CARD_BOTTOM = 6.45, 1.14                   # the "Debian 13" card, above the terminal
NOTE_LEFT = -6.3


# ------------------------------------------------------------------ small builders
def gold_tag(lines: list[str], size: float = 20) -> VGroup:
    """A GOLD tag of one or two lines (L1's: GOLD text on an opaque dark pill)."""
    t = VGroup(*[label(s, size, COST) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    b = RoundedRectangle(width=t.width + 0.32, height=t.height + 0.24, corner_radius=0.16,
                         stroke_color=COST, stroke_width=2).set_fill(S.BG, 0.92)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def pulse(m, factor: float = 1.15):
    """A tag's pulse: grow and settle back (Indicate would flood an opaque tag with its colour)."""
    return m.animate(rate_func=there_and_back).scale(factor)


def quick(t: float) -> float:
    """Rate function: a fade that is done in the first third of a longer move."""
    return min(1.0, 3.0 * t)


def deb13_card(rows, size: float = 20) -> VGroup:
    """The small GREY 'Debian 13' card: a GREY header, then capture lines (str or (str, colour)) as
    mono_lines. Right edge CARD_RIGHT, bottom CARD_BOTTOM. .frame .head .rows"""
    head = label("Debian 13", size, S.GREY)
    lines = VGroup()
    for r in rows:
        s, col = r if isinstance(r, tuple) else (r, OUTPUT)
        lines.add(mono_line(s, size, col))
    lines.arrange(DOWN, aligned_edge=LEFT, buff=0.06)
    inner = VGroup(head, lines).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    fr = RoundedRectangle(width=inner.width + 0.6, height=inner.height + 0.36, corner_radius=0.12,
                          stroke_color=S.GREY, stroke_width=2.5).set_fill(TERM_BG, 1)
    inner.move_to(fr)
    g = VGroup(fr, inner)
    g.shift(np.array([CARD_RIGHT - fr.get_right()[0], CARD_BOTTOM - fr.get_bottom()[1], 0]))
    g.frame, g.head, g.rows = fr, head, lines
    return g


def pkg_chip(size: float = 22) -> VGroup:
    """PURPLE chip: `docker.io` (mono) · Debian's package."""
    t = VGroup(mono("docker.io", size, INK), label("· Debian's package", size, INK)).arrange(RIGHT, buff=0.14)
    h = mono("|", size).height + 0.24
    b = box(t.width + 0.5, h, TOOL, fill_opacity=0.16, radius=h / 2.6)
    t.move_to(b)
    return VGroup(b, t)


def row_bar(row, color, opacity: float = 0.24) -> Rectangle:
    """A translucent bar the height of terminal row `row`, behind its glyphs."""
    g = row.glyphs
    return Rectangle(width=g.width + 0.16, height=row.strut.height * 0.92, stroke_width=0) \
        .set_fill(color, opacity).move_to([g.get_center()[0], row.strut.get_center()[1], 0])


def attach_back(scene, line, mob):
    """attach(), drawn behind the row's glyphs."""
    scene.remove(mob)
    line.add_to_back(mob)
    scene.add(line)
    return mob


def in_title_bar(t, mob, right: float = 0.25):
    """Put `mob` inside terminal t's title bar, right-aligned."""
    return mob.move_to([t.box.get_right()[0] - right - mob.width / 2, t.box.get_top()[1] - t.bar_h / 2, 0])


def open_book(page_w: float = 1.25, page_h: float = 1.5, color=SYSTEM) -> VGroup:
    """An open book (two pages and a spine), ORANGE: apt's catalog. .pages .spine"""
    tilt = 0.12
    left = Polygon([0, -page_h / 2, 0], [-page_w, -page_h / 2 + tilt, 0], [-page_w, page_h / 2 + tilt, 0],
                   [0, page_h / 2, 0], stroke_color=color, stroke_width=3).set_fill(color, 0.08)
    right = left.copy().flip(UP, about_point=ORIGIN)
    spine = Line([0, -page_h / 2 - 0.05, 0], [0, page_h / 2 + 0.05, 0], color=color, stroke_width=3)
    g = VGroup(left, right, spine)
    g.pages, g.spine = VGroup(left, right), spine
    g.page_w, g.page_h, g.tilt = page_w, page_h, tilt
    return g


def book_lines(book: VGroup, n: int = 6, color=SYSTEM) -> VGroup:
    """Short text lines on both pages (the catalog filled), following the pages' tilt."""
    out = VGroup()
    pw, ph, tilt = book.page_w, book.page_h, book.tilt
    c = book.spine.get_center()
    for side in (-1, 1):
        for k in range(n):
            y = ph / 2 - 0.22 - (ph - 0.44) * k / (n - 1)
            x0, x1 = side * 0.16, side * (pw - 0.16) * (0.72 if k % 3 == 2 else 1.0)
            out.add(Line(c + np.array([x0, y + tilt * abs(x0) / pw, 0]),
                         c + np.array([x1, y + tilt * abs(x1) / pw, 0]), color=color, stroke_width=3))
    return out


def door_glyph(door_w: float = 1.25, door_h: float = 1.85, color=TOOL) -> VGroup:
    """A PURPLE door: frame, two panels, a knob. .frame .knob"""
    fr = Rectangle(width=door_w, height=door_h, stroke_color=color, stroke_width=3.5).set_fill(color, 0.12)
    panels = VGroup(*[RoundedRectangle(width=door_w * 0.62, height=door_h * 0.32, corner_radius=0.05,
                                       stroke_color=color, stroke_width=2) for _ in range(2)])
    panels.arrange(DOWN, buff=door_h * 0.1).move_to(fr).shift(LEFT * door_w * 0.06)
    knob = Dot(radius=0.06, color=color).move_to(fr.get_right() + LEFT * door_w * 0.13 + DOWN * door_h * 0.04)
    g = VGroup(fr, panels, knob)
    g.frame, g.knob = fr, knob
    return g


def key_glyph(key_h: float = 0.3, color=S.GREY) -> VGroup:
    """A key pointing right: ring, shaft, two teeth. .tip"""
    ring = Circle(radius=key_h * 0.5, stroke_color=color, stroke_width=3).set_fill(color, 0.2)
    shaft = Line(ring.get_right(), ring.get_right() + RIGHT * key_h * 2.0, color=color, stroke_width=4)
    teeth = VGroup(*[Line(shaft.get_end() + LEFT * key_h * d, shaft.get_end() + LEFT * key_h * d + DOWN * key_h * 0.4,
                          color=color, stroke_width=4) for d in (0.12, 0.55)])
    g = VGroup(ring, shaft, teeth)
    g.tip = lambda: shaft.get_end()
    return g


# ------------------------------------------------------------------ the scene
class DockerOnVM(VoiceScene):
    def construct(self):
        assert len(SAY) == 8, f"S14 has {len(SAY)} SAY lines; this scene times 8"

        # ========================================================== 0 · C1: create a VM
        tr_b = tracker_b(4, extra=True)
        tr = tracker_c()
        br = browser_window(URL, width=BR_W, height=BR_H, size=20)
        br.shift(np.array([BR_LEFT - br.frame.get_left()[0], BR_TOP - br.frame.get_top()[1], 0]))
        ill = illustration_tag()
        ill.move_to(br.frame.get_corner(DR) + np.array([-ill.width / 2 - 0.3, 0, 0]))
        heading = VGroup(label("Compute Engine", 26, INK), label("›", 26, S.GREY), label("VM instances", 26, INK))
        heading.arrange(RIGHT, buff=0.2)
        create_i = chip("Create instance", CLOUD, size=24)
        page1 = VGroup(heading, create_i).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        page1.move_to(br.content).align_to(br.content, LEFT).align_to(br.content, UP).shift(RIGHT * 0.35 + DOWN * 0.35)

        ftitle = label("Create an instance", 26, INK)
        form = form_rows(FIELDS, width=8.4, size=22, buff=0.14)
        lw = max(r.label.width for r in form.rows)
        slack = 8.4 * 0.38 - (lw + 0.4)
        for r in form.rows:
            VGroup(r.field, r.value).shift(LEFT * slack)
            r.value.set_opacity(0)
        create = chip("Create", CLOUD, size=22)
        page2 = VGroup(ftitle, form, create).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        page2.move_to(br.content).align_to(br.content, LEFT).shift(RIGHT * 0.35)
        assert form.get_right()[0] < br.frame.get_right()[0] - 0.2, "form wider than the page"
        foot1 = label("the README gives no settings: sensible choices", 20, S.GREY)
        foot2a = label("Debian 13 works too", 20, S.GREY)
        foot2b = label("· E2 = amd64", 20, S.GREY, t2c={"amd64": CLOUD})
        foot2 = VGroup(foot2a, foot2b).arrange(RIGHT, buff=0.14)
        foot = VGroup(foot1, foot2).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        foot.next_to(br.frame, DOWN, buff=0.25).align_to(br.frame, LEFT).shift(RIGHT * 0.12)

        dial = CostDial(radius=0.5, caption=None).move_to(DIAL_C)
        cost = label("cost", 22, COST).next_to(dial, RIGHT, buff=0.2)
        tags = [gold_tag(["billed per second", "while running"]), gold_tag(["disk: billed", "while it exists"])]
        top = dial.get_bottom()[1] - 0.3
        for tg in tags:
            tg.move_to([0, top - tg.height / 2, 0]).set_x(dial.get_left()[0], LEFT)
            top -= tg.height + 0.16

        def fill(row, rt=0.45):
            row.value.set_opacity(1)
            self.play(ShowIncreasingSubsets(row.value, rate_func=linear), run_time=rt)

        rows = form.rows
        sec = readme_card(203, label(SECTION_C, 34, INK)).move_to([0, 0.5, 0])
        tr_rest = VGroup(tr.head[0], tr.head[1], tr.dots, tr.caption)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr_b, shift=DOWN * 0.1), run_time=0.5)
            self.play(FadeIn(sec, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("Running App on VM using Docker")
            # the README's heading becomes the new tracker's section name (what became what)
            self.play(FadeOut(tr_b, shift=UP * 0.25), FadeIn(tr_rest, shift=UP * 0.25),
                      ReplacementTransform(sec.body, tr.head[2]), FadeOut(VGroup(sec.frame, sec.head), rate_func=quick),
                      run_time=1.0)
            self.remove(tr_rest, tr.head[2])
            self.add(tr)
            self.play(Indicate(tr.head[2], color=TURN, scale_factor=1.08), run_time=0.8)
            vo.wait_until("First, create a VM")
            self.play(track(tr, 1), FadeIn(br, shift=RIGHT * 0.2), FadeIn(ill), run_time=0.6)
            self.play(FadeIn(heading, shift=RIGHT * 0.15), FadeIn(create_i, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(create_i, color=S.WHITE, scale_factor=1.12), run_time=0.6)
            vo.wait_until("as in lecture 1")
            # the clicked button becomes the form's title (what became what)
            self.play(FadeOut(heading, shift=UP * 0.3), FadeTransform(create_i, ftitle), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(VGroup(r.label, r.field)) for r in rows], lag_ratio=0.12),
                      FadeIn(create), run_time=0.7)
            vo.wait_until("The README gives no settings")
            self.play(FadeIn(foot1, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("An ordinary E2 machine")
            fill(rows[0], 0.4)
            fill(rows[1], 0.4)
            vo.wait_until("with Debian 12 or 13")
            fill(rows[2], 0.6)
            self.play(FadeIn(foot2a, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("E2 machines are amd64")
            self.play(FadeIn(foot2b, shift=LEFT * 0.1), run_time=0.4)
            self.play(Indicate(rows[1].value, color=CLOUD, scale_factor=1.2),
                      Indicate(foot2b[-5:], color=CLOUD, scale_factor=1.15), run_time=0.8)
            vo.wait_until("The meter starts")
            dial.tracker.add_updater(lambda m, dt: m.increment_value(dt * RATE))
            self.add(dial.tracker)
            self.play(FadeIn(dial, scale=0.8), FadeIn(cost, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("the VM bills by the second")
            self.play(FadeIn(tags[0], shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("its disk while it exists")
            self.play(FadeIn(tags[1], shift=DOWN * 0.15), Indicate(rows[2].value, color=COST, scale_factor=1.06),
                      run_time=0.7)

        # ========================================================== 1 · C2: SSH in
        h3 = VGroup(label("Compute Engine", 26, INK), label("›", 26, S.GREY), label("VM instances", 26, INK))
        h3.arrange(RIGHT, buff=0.2)
        ok = check_mark(0.3, S.GREEN)
        inst = VGroup(ok, mono(VM_HOST, 22, INK), mono("e2-small", 20, S.GREY), chip("SSH", CLOUD, size=22))
        inst.arrange(RIGHT, buff=0.35)
        ssh = inst[3]
        row_frame = box(inst.width + 0.45, inst.height + 0.36, S.GREY, fill_opacity=0.05, radius=0.08).move_to(inst)
        page3 = VGroup(h3, VGroup(row_frame, inst)).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        page3.move_to(br.content).align_to(br.content, UP).align_to(br.content, LEFT).shift(DOWN * 0.3 + RIGHT * 0.35)

        t = vm_term(ROWS)
        badge_dial = CostDial(radius=0.28, caption=None).move_to(BADGE_DIAL)
        mini_t = mono(VM_HOST, 20, CLOUD)
        mini_b = box(mini_t.width + 0.4, mini_t.height + 0.3, CLOUD, fill_opacity=0.15, radius=0.08)
        mini_t.move_to(mini_b)
        mini = VGroup(mini_b, mini_t).next_to(badge_dial, LEFT, buff=0.2)

        with self.voiceover(SAY[1]) as vo:
            self.play(track(tr, 2), FadeOut(VGroup(*tags)), Indicate(create, color=S.WHITE, scale_factor=1.15),
                      run_time=0.45)
            form_parts = VGroup(ftitle, form, create)
            self.play(form_parts.animate.scale(0.3, about_point=row_frame.get_center()).set_opacity(0),
                      FadeOut(foot), FadeIn(h3), FadeIn(row_frame), FadeIn(VGroup(*inst[1:])), run_time=0.55)
            self.remove(form_parts)
            self.play(Create(ok), Indicate(ssh, color=S.WHITE, scale_factor=1.25), run_time=0.45)
            # the dial moves into the badge (one dial on screen): freeze its needle, morph it onto a
            # still copy of the badge dial, then swap in the live badge dial
            badge_dial.tracker.set_value(dial.tracker.get_value())
            dial.tracker.clear_updaters()
            self.remove(dial.tracker)
            badge_dial.tracker.add_updater(lambda m, dt: m.increment_value(dt * RATE))
            self.add(badge_dial.tracker)
            dial.needle.clear_updaters()
            badge_dial.needle.update()
            dial_parts = VGroup(dial.face, dial.ticks, dial.needle, dial.hub)
            dial_to = VGroup(badge_dial.face, badge_dial.ticks, badge_dial.needle, badge_dial.hub).copy()
            for m in dial_to.get_family():
                m.clear_updaters()
            # the page fades out early in the move, so it never sits under the terminal's title
            self.play(ReplacementTransform(br.frame, t.box),
                      FadeOut(VGroup(*[m for m in br.submobjects if m is not br.frame], ill, page3),
                              rate_func=quick),
                      FadeIn(VGroup(t.bar, t.dots, t.title), rate_func=rate_functions.ease_in_quad),
                      Transform(dial_parts, dial_to), FadeOut(cost, rate_func=quick), FadeIn(mini, shift=LEFT * 0.2),
                      run_time=1.0)
            self.remove(dial, dial_parts, t.box, t.bar, t.dots, t.title)
            self.add(badge_dial, t)
            p0 = bare_prompt(self, t)
            vo.wait_until("Pause now")
            yt1 = your_turn().next_to(p0.strut, RIGHT, buff=0.35)
            pin(self, p0, yt1, run_time=0.4)
            self.play(pulse(yt1), run_time=0.7)
            vo.wait_until("until its SSH terminal is open")
            self.play(Indicate(t.title, color=CLOUD, scale_factor=1.25), run_time=0.9)

        # ========================================================== 2 · C3: apt install fails
        card2 = deb13_card([(D01, ERR)])
        note2 = VGroup(label("installed?", 22, S.GREY), label("→ skip to the version check", 22, S.GREY))
        note2.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        note2.move_to([NOTE_LEFT + note2.width / 2, card2.frame.get_y(), 0])
        assert note2.get_right()[0] < card2.frame.get_left()[0] - 0.2, "note runs into the card"

        with self.voiceover(SAY[2]) as vo:
            unpin(self, [(p0, yt1)], 0.3, track(tr, 3))
            c_apt = type_cmd(self, t, APT_DOCKER, 1.0)
            vo.wait_until("Pause and run it")
            yt2 = your_turn().next_to(c_apt.strut, RIGHT, buff=0.4)
            pin(self, c_apt, yt2, run_time=0.4)
            self.play(pulse(yt2), run_time=0.7)
            vo.wait_until("In our stand-in")
            out2 = t.print(self, OUT01[:3] + [(s, ERR) for s in OUT01[3:]], run_time=0.6)
            red = VGroup(*[r.glyphs for r in out2[3:]])
            st_tag = beside(row_tag("stand-in · empty package lists"), out2[3], buff=0.4)
            pin(self, out2[3], st_tag, run_time=0.4)
            vo.wait_until("it fails")
            self.play(Indicate(red, color=ERR, scale_factor=1.04), run_time=0.8)
            self.add(*out2[3:])
            vo.wait_until("unable to locate package")
            self.play(FadeIn(card2, shift=DOWN * 0.15), run_time=0.5)
            self.play(Indicate(card2.rows[0], color=ERR, scale_factor=1.05), run_time=0.6)
            p2 = bare_prompt(self, t)
            vo.wait_until("If yours installed")
            self.play(FadeIn(note2, shift=RIGHT * 0.15), run_time=0.5)
            vo.wait_until("skip ahead to the version check")
            self.play(Indicate(note2[1], color=INK, scale_factor=1.06), run_time=0.8)
        del p2

        # ========================================================== 3 · the README's gap: apt-get update
        c210 = readme_card(210, mono_line(README_210, 22, INK))
        c44_body = VGroup(label(README_44[0], 22, INK), mono_line(README_44[1], 22, INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        c44 = readme_card(44, c44_body)
        cards = VGroup(c210, c44).arrange(RIGHT, buff=0.55, aligned_edge=UP)
        cards.move_to([0, 2.62 - cards.height / 2, 0])
        assert cards.width < 12.8, cards.width
        err3 = erratum_tag().next_to(c210.frame, DOWN, buff=0.18).align_to(c210.frame, LEFT).shift(RIGHT * 0.2)
        sect = label("README › Installing App on VM Manually · lecture 1", 20, S.GREY)
        sect.next_to(c44.frame, DOWN, buff=0.18).align_to(c44.frame, RIGHT)
        if sect.get_right()[0] > 6.45:
            sect.shift(LEFT * (sect.get_right()[0] - 6.45))
        book = open_book().move_to([-2.2, -0.35, 0])
        book_t = label("package lists", 24, SYSTEM).next_to(book, RIGHT, buff=0.45).shift(UP * 0.3)
        book_n = label("empty, or out of date", 22, S.GREY).next_to(book_t, DOWN, buff=0.14).align_to(book_t, LEFT)
        filled = book_lines(book)

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(card2, note2)), run_time=0.4)
            resize(self, t, 3)
            self.play(FadeIn(c210, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("this section skips")
            self.play(FadeIn(err3, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("sudo apt-get update")
            self.play(FadeIn(c44, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("used in lecture 1")
            self.play(FadeIn(sect, shift=UP * 0.1), Indicate(c44_body[1], color=TURN, scale_factor=1.06), run_time=0.8)
            vo.wait_until("Without it")
            self.play(FadeIn(book, shift=UP * 0.15), FadeIn(book_t, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("may be empty, as here")
            self.play(FadeIn(book_n, shift=UP * 0.1), Indicate(red, color=ERR, scale_factor=1.03), run_time=0.8)
            self.add(*out2[3:])
            vo.wait_until("or out of date")
            self.play(Indicate(book.pages, color=S.GREY, scale_factor=1.05), run_time=0.8)
            vo.wait_until("Run the update first")
            c_upd = type_cmd(self, t, APT_UPDATE, 0.7)
            x3 = beside(row_tag("extra"), c_upd, buff=0.4)
            pin(self, c_upd, x3, run_time=0.3, anim=AnimationGroup(FadeIn(x3, shift=LEFT * 0.1),
                                                                   track(tr, 3, extra=True)))
            t.print(self, OUT02, run_time=0.4)
            yt3 = your_turn().next_to(x3, RIGHT, buff=0.3)
            self.play(LaggedStart(*[Create(ln) for ln in filled], lag_ratio=0.06), FadeOut(book_n),
                      FadeIn(yt3, shift=LEFT * 0.1), run_time=0.7)
            attach(self, c_upd, yt3)
            vo.wait_until("pause after it")
            self.play(pulse(yt3), run_time=0.6)

        # ========================================================== 4 · C3: the install works
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(c210, c44, err3, sect, book, book_t, filled)), track(tr, 3), run_time=0.4)
            unpin(self, [(c_upd, x3), (c_upd, yt3)], 0.2)
            resize(self, t, ROWS, run_time=0.6)
            c_apt2 = type_cmd(self, t, APT_DOCKER, 0.8)
            del c_apt2
            out4 = t.print(self, OUT03_A + [ASK58], run_time=0.6, wrap=True)
            asked_at = self.renderer.time
            r55, r56 = t.find("newly installed"), t.find("Need to get")
            r58 = out4[-1]
            vo.wait_until("92 new packages")
            bars = [row_bar(r, TURN, 0.24) for r in (r55, r56)]
            self.play(*[FadeIn(b) for b in bars], run_time=0.5)
            for r, b in zip((r55, r56), bars):
                attach_back(self, r, b)
            self.play(Indicate(substring(r55, "92 newly installed"), color=TURN, scale_factor=1.1), run_time=0.7)
            self.add(r55)
            vo.wait_until("a 107 megabyte download")
            mb = substring(r56, "107 MB")
            u107 = under(mb, TURN)
            dl = beside(row_tag("download"), r56, buff=0.35)
            self.play(Create(u107), FadeIn(dl, shift=LEFT * 0.1), run_time=0.5)
            attach(self, r56, u107)
            attach(self, r56, dl)
            vo.wait_until("on Debian 12")
            varies = in_title_bar(t, row_tag("package list varies by VM"))
            self.play(FadeIn(varies, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("91 packages and 118 megabytes")
            card4 = deb13_card(D03)
            self.play(FadeIn(card4, shift=DOWN * 0.15), run_time=0.5)
            u91 = under(substring(card4.rows[0], "91"), TURN)
            u118 = under(substring(card4.rows[1], "118 MB"), TURN)
            self.play(Create(u91), run_time=0.4)
            self.play(Create(u118), run_time=0.4)
            vo.wait_until("Answer Y")
            type_answer(self, t, r58, ASK58, "Y", asked_at)
            t.print(self, OUT03_B, run_time=0.5)
            vo.wait_until("Pause and run it")
            yt4 = your_turn().next_to(r58.glyphs, RIGHT, buff=0.5)
            pin(self, r58, yt4, run_time=0.4)
            self.play(pulse(yt4), run_time=0.6)

        # ========================================================== 5 · C4: docker --version
        chip5 = pkg_chip()
        chip5.move_to([NOTE_LEFT + chip5.width / 2, 2.3, 0])
        lap5 = VGroup(label("laptop:", 22, S.GREY), mono("Docker 29.8.2", 22, S.GREY)).arrange(RIGHT, buff=0.14)
        lap5.next_to(chip5, DOWN, buff=0.3).align_to(chip5, LEFT).shift(RIGHT * 0.1)
        card5 = deb13_card([V13])
        rec_card = row_tag("at the time of recording")
        rec_card.move_to([card5.frame.get_right()[0] - 0.25 - rec_card.width / 2, card5.frame.get_top()[1], 0])
        assert chip5.get_right()[0] < card5.frame.get_left()[0] - 0.2, "chip runs into the card"

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(card4, u91, u118, varies)), track(tr, 4), run_time=0.4)
            unpin(self, [(r58, yt4)], 0.2)
            bare_prompt(self, t)
            type_cmd(self, t, DOCKER_VERSION, 0.8)
            r_ver = t.print(self, [V12], run_time=0.4)[0]
            bare_prompt(self, t)
            vo.wait_until("This is Debian's own Docker package")
            self.play(FadeIn(chip5, shift=RIGHT * 0.15), run_time=0.5)
            self.play(Indicate(chip5, color=TOOL, scale_factor=1.06), run_time=0.7)
            vo.wait_until("20.10.24 on Debian 12")
            v12 = substring(r_ver, "20.10.24")
            u12 = under(v12, TURN)
            self.play(Create(u12), Indicate(v12, color=TURN, scale_factor=1.15), run_time=0.7)
            attach(self, r_ver, u12)
            vo.wait_until("26.1.5 on Debian 13")
            self.play(FadeIn(card5, shift=DOWN * 0.15), run_time=0.5)
            v13 = substring(card5.rows[0], "26.1.5")
            u13 = under(v13, TURN)
            self.play(Create(u13), Indicate(v13, color=TURN, scale_factor=1.15), run_time=0.7)
            vo.wait_until("at the time of recording")
            rec_row = beside(row_tag("at the time of recording"), r_ver, buff=0.4)
            pin(self, r_ver, rec_row, run_time=0.4, anim=AnimationGroup(FadeIn(rec_row, shift=LEFT * 0.1),
                                                                         FadeIn(rec_card, shift=DOWN * 0.1)))
            vo.wait_until("Older than the laptop's")
            self.play(FadeIn(lap5, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("but plenty")
            self.play(Indicate(r_ver.glyphs, color=INK, scale_factor=1.04), run_time=0.8)
            self.add(r_ver)

        # ========================================================== 6 · V8: Docker right on the VM's kernel
        vm = vm_with_docker(vm_w=5.6, vm_h=3.4, size=22)
        vm.move_to([-1.3, 0.72, 0])
        dvm_box = box(2.3, 0.75, S.GREY, dashed=True)
        dvm_t = label("Linux VM", 22, S.GREY).move_to(dvm_box)
        dvm = VGroup(dvm_box, dvm_t).move_to([4.15, 1.05, 0])
        dvm_x = VGroup(Circle(radius=0.24, stroke_color=S.GREY, stroke_width=2.5).set_fill(S.BG, 1),
                       cross_mark(0.2, S.GREY, stroke=4)).move_to(dvm_box.get_corner(UR))
        dvm_cap = label("Docker Desktop only", 22, S.GREY).next_to(dvm, DOWN, buff=0.3)

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(chip5, lap5, card5, u13, rec_card)), run_time=0.4)
            resize(self, t, 3, run_time=0.6)
            self.play(FadeIn(VGroup(vm.frame, vm.title, vm.kernel), shift=UP * 0.15), run_time=0.6)
            self.play(FadeIn(vm.dockerd, shift=DOWN * 1.0), run_time=0.6, rate_func=rate_functions.ease_out_cubic)
            self.play(FadeIn(vm.slot), Indicate(vm.kernel, color=CLOUD, scale_factor=1.04), run_time=0.6)
            vo.wait_until("there's no hidden VM")
            self.play(FadeIn(dvm, scale=0.7), run_time=0.5)
            self.play(FadeIn(dvm_x, scale=1.5), run_time=0.4)
            vo.wait_until("unlike Docker Desktop")
            self.play(FadeIn(dvm_cap, shift=UP * 0.1), Indicate(dvm_box, color=S.GREY, scale_factor=1.08), run_time=0.7)

        # ========================================================== 7 · why sudo: the socket's door
        door = door_glyph().move_to([0.6, 0.95, 0])
        sock = mono("/var/run/docker.sock", 22, TOOL).next_to(door, UP, buff=0.2)
        lock = lock_glyph(0.36, S.GREY).move_to(door.knob.get_center() + UP * 0.32 + LEFT * 0.02)
        dk = VGroup(box(2.0, 0.7, TOOL, fill_opacity=0.18), mono("dockerd", 22, TOOL))
        dk[1].move_to(dk[0])
        dk.move_to([4.0, 0.95, 0])
        bg = label("background service", 22, S.GREY).next_to(dk, DOWN, buff=0.22)
        link = DashedLine(door.get_right() + RIGHT * 0.1, dk.get_left() + LEFT * 0.1, color=TOOL, stroke_width=3,
                          dash_length=0.1)
        ps_chip = chip(PS, TOOL, size=22, font=MONO).move_to([-4.3, 1.45, 0])
        path = route(ps_chip.get_right() + RIGHT * 0.1, door.get_left() + LEFT * 0.12 + UP * 0.5, arc=-0.35)
        x7 = cross_mark(0.36, ERR).next_to(door, LEFT, buff=0.25).shift(DOWN * 0.15)
        keys = VGroup()
        for word in ("root", "docker group"):
            k = key_glyph(0.28)
            w = label(word, 22, S.GREY).next_to(k, LEFT, buff=0.25)
            g = VGroup(w, k)
            g.key = k
            keys.add(g)
        keys.arrange(DOWN, aligned_edge=RIGHT, buff=0.3).move_to([-3.2, 0.0, 0])

        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(vm, dvm, dvm_x, dvm_cap)), track(tr, 4, extra=True), run_time=0.5)
            resize(self, t, 5, run_time=0.5)
            self.play(FadeIn(VGroup(door, sock, lock), shift=UP * 0.15), FadeIn(dk), Create(link), run_time=0.6)
            vo.wait_until("Without it")
            c_ps = type_cmd(self, t, PS, 0.5)
            x7t = beside(row_tag("extra"), c_ps, buff=0.4)
            pin(self, c_ps, x7t, run_time=0.3)
            self.play(FadeIn(ps_chip, shift=RIGHT * 0.2), Create(path), run_time=0.5)
            vo.wait_until("is refused")
            back = ps_chip.get_center().copy()
            self.play(ps_chip.animate.move_to(path.get_end() + LEFT * ps_chip.width / 2), run_time=0.4,
                      rate_func=rate_functions.ease_in_quad)
            self.play(ps_chip.animate.move_to(back), door.frame.animate(rate_func=there_and_back).set_stroke(ERR),
                      FadeIn(x7, scale=1.4), run_time=0.5)
            err_rows = t.print(self, [(ERR05, ERR)], run_time=0.5, wrap=True)
            vo.wait_until("permission denied on the Docker socket")
            u_pd = under(substring(err_rows[0], "permission denied"), ERR)
            u_sock = under(substring(err_rows[1], "/var/run/docker.sock"), ERR)
            self.play(Create(u_pd), Create(u_sock), Indicate(sock, color=TOOL, scale_factor=1.1), run_time=0.7)
            attach(self, err_rows[0], u_pd)
            attach(self, err_rows[1], u_sock)
            vo.wait_until("the door to Docker's background service")
            self.play(Indicate(door, color=TOOL, scale_factor=1.06), run_time=0.6)
            self.play(FadeIn(bg, shift=UP * 0.1), Indicate(dk, color=TOOL, scale_factor=1.08), run_time=0.7)
            vo.wait_until("Only root and the docker group")
            self.play(FadeOut(VGroup(x7, path)), LaggedStart(*[FadeIn(k, shift=RIGHT * 0.15) for k in keys],
                                                              lag_ratio=0.3), run_time=0.8)
            vo.wait_until("may open it")
            k0 = keys[0]
            self.play(k0.animate.shift(lock.get_left() + LEFT * 0.05 - k0.key.tip()), FadeOut(ps_chip), run_time=0.8)
            self.play(Indicate(lock, color=S.WHITE, scale_factor=1.3), run_time=0.6)

        # ========================================================== end · empty frame
        badge_dial.tracker.clear_updaters()
        badge_dial.freeze()
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
        self.wait(0.2)
