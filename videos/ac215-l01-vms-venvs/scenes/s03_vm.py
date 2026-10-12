"""S03 · Renting a computer: the VM (walkthrough: README step 1 Create VM, step 2 SSH).

Beats (script.md "## S03", one voiceover block each):
 0  V1, big and centred. A GREY rack (`server()`, "physical server"); a "hypervisor" slab slides
    down onto it; a translucent copy of the machine rises out of it, is cut in four and the
    slices spread ("virtual machines"); each slice gets virtual CPU + memory glyphs that fly up
    from the server; a row of BLUE disks appears below ("storage network"); each slice grows an
    OS layer (Debian 12, Ubuntu 24.04, Debian 13, …); the first slice turns BLUE, is named
    `ac215-l01` and a short BLUE line links it to one disk.
 1  V1 shrinks to the right (only our slice keeps its detail). TRACKER A1 appears. A GREY browser
    (`console.cloud.google.com/compute/instances`, tag illustration): project selector "your
    Tutorial 0 project" (YELLOW pulse), "Compute Engine › VM instances", the GREY dashed note
    "first visit: Enable Compute Engine API" (a progress bar fills: "give it a minute"), and the
    BLUE "Create instance" button (pulses).
 2  The page becomes the create form (`form_rows`); rows fill as they are named and our slice
    builds the matching part: name -> its label pulses; zone -> a GREY pin "us-central1-a";
    machine type -> the CPU/memory glyphs become a block "CPU + memory"; boot disk -> the linked
    disk gets "disk · Debian 12". GREY footnote under the browser (two lines).
 3  The External IPv4 row highlights YELLOW; PINK routes run from our slice to "Debian mirrors",
    "GitHub", "PyPI" (they pulse on "can't reach the internet" / "every download").
 4  The GOLD cost dial (no digits) appears above our slice and starts sweeping; three GOLD tags
    slide in under it as they are named; the CPU block dims ("even when it sits idle") but the
    needle keeps going; a GOLD "estimate" tag pulses on the empty estimate panel.
 5  Create -> the form collapses into the instance row (GREEN check, ac215-l01, us-central1-a,
    External IP, SSH). SSH -> a PINK beam into our slice; V1 + dial shrink to a badge top right
    (the dial keeps sweeping to the end of the scene); TRACKER A2; a GREY "Authorize" dialog
    flashes ("first time only"); the browser becomes the terminal (9 rows, `ssh · ac215-l01`);
    YELLOW "your username here" under `student`; ▶ your turn beside the prompt.
 6  TRACKER A2 · extra. `cat /etc/os-release` (extra) -> 00-os.txt lines 2-5, …; the
    PRETTY_NAME line gets a YELLOW bar, "bookworm" underlined.
 7  `python3 --version` (extra) -> line 6 `Python 3.11.2` + ORANGE chip "system Python"; a GREY
    "Debian 13" card at the right edge shows debian13-part-b/00-os.txt line 6 `Python 3.13.5`.
 8  `which python` (extra) -> the prompt simply returns (line 7 records exit status 1); RED
    "nothing" blinks beside it; PINK caption "which: the program a name would run · only python3
    exists here" above the terminal. Fade out to an empty frame.
"""

import numpy as np
from manim import *

from explainer import style as S
from explainer.devops import (CAPTION, MONO, OUTPUT, PANEL, TERM_BG, box, browser_window, chip,
                              check_mark, form_rows, label, layer_bar, mono, mono_line, server,
                              substring, tag)
from explainer.scene import VoiceScene

from common import (CLOUD, COST, ERR, INK, LOOKUP, NARRATION, P_HOME, SYSTEM, TURN, CostDial,
                    capture, extra_tag, illustration_tag, term, tracker_a, your_turn)

SAY = NARRATION["S03"]

# ------------------------------------------------------------------ commands and real outputs
CAT = "cat /etc/os-release"
PYV = "python3 --version"
WHICH = "which python"
OS12 = capture("00-os")                                   # debian12-part-a (pick = file line - 1)
OS13 = capture("00-os", "debian13-part-b")
assert OS12.cmd.startswith(CAT) and PYV in OS12.cmd and WHICH in OS12.cmd
OS_RELEASE = OS12.pick((1, 4)) + ["…"]                    # file lines 2-5, then a … line
PY12 = OS12.pick(5)[0]                                    # file line 6: Python 3.11.2
PY13 = OS13.pick(5)[0]                                    # file line 6: Python 3.13.5
assert OS12.pick(6)[0] == "which-python-exit:1"           # file line 7: `which python` printed nothing
assert PY12 == "Python 3.11.2" and PY13 == "Python 3.13.5"

URL = "console.cloud.google.com/compute/instances"
FIELDS = [("Name", "ac215-l01"), ("Region", "us-central1"), ("Zone", "us-central1-a"),
          ("Machine type", "e2-small"), ("Boot disk", "Debian GNU/Linux 12 (bookworm)"),
          ("External IPv4", "Ephemeral")]

# ------------------------------------------------------------------ layout
TRACK_LEFT, TRACK_TOP = -6.5, 3.5
BR_LEFT, BR_TOP, BR_W, BR_H = -6.55, 2.75, 8.7, 5.3     # the browser (left)
TERM_BOTTOM = -3.45
BADGE_DIAL = np.array([6.2, 3.13, 0])
RATE = 1 / 60                                             # dial turns per second while the VM exists

BIG = dict(x0=-4.74, widths=[2.0] * 4, gap=0.16, slice=(0.25, 1.55), os_h=0.42, os_pt=22,
           hyp_h=0.42, hyp_pt=22, server_h=1.2, disk_y=-2.02, disk_w=0.55, disk_h=0.42,
           n_disks=6, disk_pitch=0.95, name_pt=24, cpu=0.42, link_dx=0.32)
SMALL = dict(x0=2.75, widths=[2.4, 0.36, 0.36, 0.36], gap=0.1, slice=(-1.58, -0.58), os_h=0.38,
             os_pt=20, hyp_h=0.34, hyp_pt=20, server_h=0.66, disk_y=-2.96, disk_w=0.42, disk_h=0.36,
             n_disks=3, disk_pitch=0.56, name_pt=20, cpu=0.3, link_dx=0.28)


# ------------------------------------------------------------------ glyphs
def wide_server(w: float, h: float, color=S.GREY) -> VGroup:
    """The house rack glyph (`server()`), widened to w: each slab keeps its lights at the right
    end and its vents at the left end."""
    s = server(height=h, units=3, color=color)
    for slab in s:
        r, lights, vents = slab.submobjects
        nr = RoundedRectangle(width=w, height=r.height, corner_radius=0.05, stroke_color=color,
                              stroke_width=r.get_stroke_width()).set_fill(PANEL, 1).move_to(r)
        slab.submobjects[0] = nr
        lights.move_to(nr.get_right() + LEFT * 0.28)
        vents.move_to(nr.get_left() + RIGHT * 0.4)
    return s


def disk_glyph(w: float, h: float, color=CLOUD) -> VGroup:
    """A small disk (a cylinder): silhouette plus the lid's front edge."""
    e = w * 0.3
    rect = Rectangle(width=w, height=h)
    top = Ellipse(width=w, height=e).move_to(rect.get_top())
    bot = Ellipse(width=w, height=e).move_to(rect.get_bottom())
    body = Union(rect, top, bot).set_stroke(color, 2.5).set_fill(color, 0.22)
    lid = Ellipse(width=w, height=e, stroke_color=color, stroke_width=2.5).set_fill(color, 0.45)
    lid.move_to(rect.get_top())
    return VGroup(body, lid)


def cpu_glyph(s: float, color=S.GREY) -> VGroup:
    """Virtual CPU + memory: a chip with pins and a memory stick (no text)."""
    core = Square(side_length=s, stroke_color=color, stroke_width=2.5).set_fill(color, 0.25)
    pins = VGroup()
    for k in (-1, 0, 1):
        o = k * s * 0.28
        for d in (UP, DOWN, LEFT, RIGHT):
            p = core.get_center() + d * s / 2
            along = np.array([d[1], d[0], 0]) * o
            pins.add(Line(p + along, p + along + d * s * 0.16, color=color, stroke_width=2))
    ram = Rectangle(width=s * 1.7, height=s * 0.5, stroke_color=color, stroke_width=2.5)
    ram.set_fill(color, 0.25)
    cells = VGroup(*[Rectangle(width=s * 0.24, height=s * 0.22, stroke_width=0).set_fill(color, 0.8)
                     for _ in range(4)]).arrange(RIGHT, buff=s * 0.13).move_to(ram)
    ram_g = VGroup(ram, cells)
    g = VGroup(VGroup(core, pins), ram_g).arrange(RIGHT, buff=s * 0.45)
    return g


def pin_glyph(h: float = 0.5, color=S.GREY) -> VGroup:
    """A map pin, tip at the bottom (.tip)."""
    r = h * 0.32
    head = Circle(radius=r).move_to(UP * (h - r))
    tri = Polygon([-r * 0.85, h - r * 1.45, 0], [r * 0.85, h - r * 1.45, 0], [0, 0, 0])
    shape = Union(head, tri).set_stroke(color, 2.5).set_fill(color, 0.55)
    hole = Circle(radius=r * 0.38, stroke_width=0).set_fill(S.BG, 1).move_to(head)
    g = VGroup(shape, hole)
    g.tip = lambda: shape.get_bottom()
    return g


def gold_tag(lines: list[str], size: float = 20) -> VGroup:
    """A GOLD tag of one or two lines (the house tag() look: GOLD text on an opaque dark pill)."""
    t = VGroup(*[label(s, size, COST) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    b = RoundedRectangle(width=t.width + 0.32, height=t.height + 0.24, corner_radius=0.16,
                         stroke_color=COST, stroke_width=2).set_fill(S.BG, 0.92)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def pulse(m, factor: float = 1.18):
    """A tag's pulse: grow and settle back (Indicate would flood an opaque tag with its colour)."""
    return m.animate(rate_func=there_and_back).scale(factor)


def caret(size: float = 0.13, color=S.GREY) -> VMobject:
    return Triangle(stroke_width=0).set_fill(color, 1).rotate(PI).scale_to_fit_width(size)


# ------------------------------------------------------------------ V1 · slicing a server
def build_v1(L: dict, ours_blue: bool = False) -> VGroup:
    """V1 in one of two layouts (BIG: centred, all slices alike; SMALL: right third, our slice
    wide). Parts: .server .hyp .slices .os (layer bars; .box .text) .cpus .disks .name .link
    .labels (BIG only: virtual machines / physical server / storage network) .storage"""
    v = VGroup()
    y0, y1 = L["slice"]
    sh = y1 - y0
    xs, x = [], L["x0"]
    for w in L["widths"]:
        xs.append(x + w / 2)
        x += w + L["gap"]
    total = sum(L["widths"]) + L["gap"] * (len(L["widths"]) - 1)
    cx = L["x0"] + total / 2
    big = L is BIG

    v.slices = VGroup()
    for i, (xc, w) in enumerate(zip(xs, L["widths"])):
        col = CLOUD if (i == 0 and ours_blue) else S.GREY
        v.slices.add(box(w, sh, col, fill_opacity=0.15 if col == CLOUD else 0.1, radius=0.08)
                     .move_to([xc, (y0 + y1) / 2, 0]))
    names = ["Debian 12", "Ubuntu 24.04", "Debian 13", "…"]
    v.os = VGroup()
    for i, (xc, w) in enumerate(zip(xs, L["widths"])):
        col = CLOUD if (i == 0 and ours_blue) else S.GREY
        txt = names[i] if (big or i == 0) else " "
        bar = layer_bar(txt, w, L["os_h"], col, size=L["os_pt"], fill_opacity=0.3)
        bar.move_to([xc, y1 + L["os_h"] / 2, 0])
        v.os.add(bar)
    v.hyp = layer_bar("hypervisor", total, L["hyp_h"], S.GREY, size=L["hyp_pt"], fill_opacity=0.25)
    v.hyp.move_to([cx, y0 - L["hyp_h"] / 2, 0])
    v.server = wide_server(total, L["server_h"])
    v.server.move_to([cx, y0 - L["hyp_h"] - L["server_h"] / 2, 0])
    v.cpus = VGroup()
    for i, xc in enumerate(xs):
        g = cpu_glyph(L["cpu"] if (big or i == 0) else 0.1, CLOUD if (i == 0 and ours_blue) else S.GREY)
        g.move_to([xc, y0 + sh * (0.36 if big else 0.3), 0])
        v.cpus.add(g)
    v.disks = VGroup()
    first = xs[0] - L["widths"][0] / 2 + L["disk_w"] / 2 + (0.5 if big else 0.1)
    for k in range(L["n_disks"]):
        v.disks.add(disk_glyph(L["disk_w"], L["disk_h"]).move_to([first + k * L["disk_pitch"], L["disk_y"], 0]))
    xl = L["x0"] - L["link_dx"]
    d0 = v.disks[0]
    ys = (y0 + y1) / 2
    v.link = VMobject(stroke_color=CLOUD, stroke_width=3).set_points_as_corners(
        [[L["x0"], ys, 0], [xl, ys, 0], [xl, L["disk_y"], 0], [d0.get_left()[0], L["disk_y"], 0]])
    if big:
        v.name = mono("ac215-l01", L["name_pt"], CLOUD).next_to(v.os[0], UP, buff=0.18)
        lx = L["x0"] + total + 0.3
        v.labels = VGroup(
            label("virtual machines", 22, S.GREY).move_to([0, ys, 0], aligned_edge=LEFT).set_x(lx, LEFT),
            label("physical server", 22, S.GREY).move_to(v.server).set_x(lx, LEFT),
            label("storage network", 22, S.GREY).move_to([0, L["disk_y"], 0]).set_x(lx, LEFT))
        v.storage = v.labels[2]
    else:
        v.name = mono("ac215-l01", L["name_pt"], CLOUD).move_to([xs[0], y1 - 0.22, 0])
        v.storage = label("storage network", 20, S.GREY).move_to([0, L["disk_y"], 0])
        v.storage.set_x(v.disks[-1].get_right()[0] + 0.15, LEFT)
        v.labels = VGroup(v.storage)
    v.xs, v.total, v.cx = xs, total, cx
    v.add(v.server, v.hyp, v.slices, v.os, v.cpus, v.disks)
    return v


def place_tracker(tr):
    tr.shift(np.array([TRACK_LEFT - tr.get_left()[0], TRACK_TOP - tr.get_top()[1], 0]))
    return tr


def caption_extra(scene, tr, run_time: float = 0.5):
    """Append ' · extra' to the tracker caption while a non-README command is on screen. Only
    the new glyphs fade in (a Transform between captions of different lengths scrambles the
    letters mid-way); the caption's other glyphs sit exactly where the old ones were."""
    k = tr.k
    s = f"step {k} of {len(tr.steps)}: {tr.steps[k - 1]}"
    new = label(s + " · extra", tr.size, tr.hi_color, t2c={"· extra": S.GREY})
    new.next_to(tr.dots, RIGHT, buff=0.25)
    n = len(tr.caption.submobjects)
    scene.play(FadeIn(VGroup(*new.submobjects[n:]), shift=LEFT * 0.1), run_time=run_time)
    scene.remove(tr.caption, *new.submobjects[n:])
    tr.remove(tr.caption)
    tr.caption = new
    tr.add(new)
    scene.add(tr)


class RentAComputer(VoiceScene):
    # ------------------------------------------------------------- terminal helpers
    def bare_prompt(self, t):
        """The prompt returns (no output): a prompt line with nothing typed yet."""
        ln = t.type(self, "", type_time=0)
        ln.bare = True
        return ln

    def type_cmd(self, t, cmd, type_time=None):
        """Type at the waiting prompt (replacing a bare prompt line if there is one)."""
        if len(t.lines) and getattr(t.lines[-1], "bare", False):
            last = t.lines[-1]
            self.remove(last, *last.submobjects)
            t.lines.remove(last)
        return t.type(self, cmd, type_time)

    def pin(self, line, mob, run_time=0.4, anim=None):
        """Show `mob` beside a terminal line and make it part of that line (it scrolls with it)."""
        self.play(anim or FadeIn(mob, shift=LEFT * 0.1), run_time=run_time)
        self.remove(mob)
        line.add(mob)
        self.add(line)          # the line may have been split by an earlier substring animation
        return mob

    def unpin(self, line, mob, run_time=0.3):
        self.play(FadeOut(mob), run_time=run_time)
        if mob in line.submobjects:
            line.remove(mob)

    # ------------------------------------------------------------- the scene
    def construct(self):
        assert len(SAY) == 9, f"S03 has {len(SAY)} SAY lines; this scene times 9"

        # ========================================================== 0 · V1, slicing a server
        B = build_v1(BIG)
        hyp_start = B.hyp.copy().shift(UP * 2.2).set_opacity(0)
        y0, y1 = BIG["slice"]
        whole = box(B.total, y1 - y0, S.GREY, fill_opacity=0.1, radius=0.08).move_to(B.server)
        whole_up = whole.copy()
        whole.set_stroke(opacity=0).set_fill(opacity=0)
        pieces = VGroup(*[box(B.total / 4, y1 - y0, S.GREY, fill_opacity=0.1, radius=0.08)
                          .move_to([BIG["x0"] + B.total * (k + 0.5) / 4, (y0 + y1) / 2, 0]) for k in range(4)])
        cuts = VGroup(*[DashedLine([BIG["x0"] + B.total * k / 4, y0 + 0.06, 0],
                                   [BIG["x0"] + B.total * k / 4, y1 - 0.06, 0], color=S.WHITE,
                                   stroke_width=2.5, dash_length=0.1) for k in (1, 2, 3)])

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(B.server, shift=UP * 0.2), run_time=1.0)
            vo.wait_until("a real server")
            self.play(FadeIn(B.labels[1], shift=LEFT * 0.15), run_time=0.6)
            vo.wait_until("Google's data centers")
            lights = VGroup(*[slab[1][0] for slab in B.server])
            self.play(LaggedStart(*[Flash(d, color=S.GREEN, line_length=0.12, num_lines=8, flash_radius=0.1)
                                    for d in lights], lag_ratio=0.25), run_time=0.9)
            vo.wait_until("Software called a hypervisor")
            self.play(ReplacementTransform(hyp_start, B.hyp), run_time=1.0, rate_func=rate_functions.ease_out_bounce)
            vo.wait_until("carves the machine")
            whole_up.move_to(pieces)
            self.add(whole)
            self.play(Transform(whole, whole_up), run_time=0.9)
            self.play(Create(cuts), run_time=0.5)
            self.remove(whole)
            self.add(pieces)
            self.play(*[ReplacementTransform(p, s) for p, s in zip(pieces, B.slices)], FadeOut(cuts),
                      FadeIn(B.labels[0], shift=LEFT * 0.15), run_time=0.8)
            vo.wait_until("Each slice gets")
            flights = []
            for g in B.cpus:
                src = g.copy().scale(0.5).move_to(B.server).set_opacity(0)
                flights.append(src)
            self.add(*flights)
            self.play(LaggedStart(*[ReplacementTransform(src, g) for src, g in zip(flights, B.cpus)],
                                  lag_ratio=0.2), run_time=1.6)
            vo.wait_until("a disk from")
            self.play(LaggedStart(*[FadeIn(d, shift=UP * 0.15) for d in B.disks], lag_ratio=0.12),
                      FadeIn(B.labels[2], shift=LEFT * 0.15), run_time=1.1)
            vo.wait_until("its own operating system")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in B.os], lag_ratio=0.2), run_time=1.3)
            vo.wait_until("One of them")
            self.play(B.slices[0].animate.set_stroke(CLOUD).set_fill(CLOUD, 0.15),
                      B.os[0].box.animate.set_stroke(CLOUD).set_fill(CLOUD, 0.3),
                      B.cpus[0].animate.set_color(CLOUD), run_time=0.5)
            self.play(Write(B.name), Create(B.link), Indicate(B.disks[0], color=CLOUD), run_time=0.8)

        # ========================================================== 1 · the console
        C = build_v1(SMALL, ours_blue=True)
        C.cpus[0].set_color(CLOUD)
        br = browser_window(URL, width=BR_W, height=BR_H)
        br.shift(np.array([BR_LEFT - br.frame.get_left()[0], BR_TOP - br.frame.get_top()[1], 0]))
        ill = illustration_tag()          # on the bottom edge: the top edge is the address bar
        ill.move_to(br.frame.get_corner(DR) + np.array([-ill.width / 2 - 0.3, 0, 0]))
        # built at step 1: a goto() from the blank caption grows the text out of the frame's centre
        tr = place_tracker(tracker_a(1))

        sel_t = label("your Tutorial 0 project", 24, INK)
        sel_c = caret(0.16)
        sel_in = VGroup(sel_t, sel_c).arrange(RIGHT, buff=0.25)
        sel_box = RoundedRectangle(width=sel_in.width + 0.45, height=sel_in.height + 0.26, corner_radius=0.1,
                                   stroke_color=S.GREY, stroke_width=2).set_fill(TERM_BG, 1)
        sel_in.move_to(sel_box)
        sel = VGroup(sel_box, sel_in)
        h_ce = label("Compute Engine", 30, INK)
        h_gt = label("›", 30, S.GREY)
        h_vm = label("VM instances", 30, INK)
        heading = VGroup(h_ce, h_gt, h_vm).arrange(RIGHT, buff=0.2)
        create_i = chip("Create instance", CLOUD, size=24)
        note_t = label("first visit: Enable Compute Engine API", 24, S.GREY)
        prog_bg = Line(LEFT * note_t.width / 2, RIGHT * note_t.width / 2, color=S.GREY_DARK, stroke_width=5)
        prog_bg.next_to(note_t, DOWN, buff=0.16)
        prog = Line(prog_bg.get_start(), prog_bg.get_start() + RIGHT * 0.001, color=S.GREY, stroke_width=5)
        note_in = VGroup(note_t, prog_bg)
        note_box = box(note_in.width + 0.5, note_in.height + 0.36, S.GREY, dashed=True)
        note_in.move_to(note_box)
        prog.move_to(prog_bg.get_start(), aligned_edge=LEFT)
        page1 = VGroup(sel, heading, create_i, VGroup(note_box, note_in)).arrange(DOWN, aligned_edge=LEFT, buff=0.55)
        page1.move_to(br.content).align_to(br.content, LEFT).align_to(br.content, UP).shift(RIGHT * 0.35 + DOWN * 0.35)
        prog.move_to(prog_bg.get_start(), aligned_edge=LEFT)

        big_only = [B.labels[0], B.labels[1], *[b.text for b in B.os[1:]], *B.cpus[1:], *B.disks[3:]]

        with self.voiceover(SAY[1]) as vo:
            self.play(*[ReplacementTransform(getattr(B, k), getattr(C, k)) for k in ("server", "hyp", "link", "name")],
                      *[ReplacementTransform(a, b) for a, b in zip(B.slices, C.slices)],
                      ReplacementTransform(B.os[0], C.os[0]),
                      *[ReplacementTransform(B.os[i].box, C.os[i].box) for i in (1, 2, 3)],
                      ReplacementTransform(B.cpus[0], C.cpus[0]),
                      *[ReplacementTransform(B.disks[k], C.disks[k]) for k in range(3)],
                      ReplacementTransform(B.storage, C.storage),
                      *[FadeOut(m) for m in big_only], run_time=1.3)
            self.play(FadeIn(br, shift=RIGHT * 0.3), FadeIn(ill), FadeIn(tr, shift=DOWN * 0.1), run_time=0.7)
            self.play(Indicate(tr.dots[0], color=TURN, scale_factor=1.8),
                      Indicate(tr.caption, color=TURN, scale_factor=1.08), run_time=0.6)
            vo.wait_until("check that your Tutorial 0")
            self.play(FadeIn(sel, shift=DOWN * 0.1), run_time=0.4)
            self.play(sel_box.animate(rate_func=there_and_back).set_stroke(TURN, width=6),
                      Indicate(sel_t, color=TURN, scale_factor=1.06), run_time=1.0)
            vo.wait_until("then open Compute Engine")
            self.play(FadeIn(h_ce, shift=RIGHT * 0.15), run_time=0.5)
            vo.wait_until("then VM instances")
            self.play(FadeIn(VGroup(h_gt, h_vm), shift=RIGHT * 0.15), run_time=0.5)
            self.play(FadeIn(create_i, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("The first time")
            self.play(Create(note_box), FadeIn(note_t), FadeIn(prog_bg), run_time=0.7)
            vo.wait_until("click enable")
            self.play(Indicate(note_t, color=S.WHITE, scale_factor=1.05), run_time=0.7)
            self.add(prog)
            self.play(prog.animate.put_start_and_end_on(prog_bg.get_start(), prog_bg.get_end()),
                      run_time=1.8, rate_func=smooth)
            vo.wait_until("Then click Create")
            self.play(Indicate(create_i, color=S.WHITE, scale_factor=1.15), run_time=0.7)

        # ========================================================== 2 · the create form
        ftitle = label("Create an instance", 26, INK)
        form = form_rows(FIELDS, width=8.4, size=22, buff=0.07)
        lw = max(r.label.width for r in form.rows)
        slack = 8.4 * 0.38 - (lw + 0.4)
        for r in form.rows:
            VGroup(r.field, r.value).shift(LEFT * slack)
            r.value.set_opacity(0)
        create = chip("Create", CLOUD, size=22)
        est = box(3.2, 0.44, S.GREY, fill_opacity=0.05, radius=0.08)
        est_lines = VGroup(*[Line(LEFT * f, RIGHT * f, color=S.GREY_DARK, stroke_width=5) for f in (1.1, 0.7)])
        est_lines.arrange(DOWN, buff=0.1, aligned_edge=LEFT).move_to(est).align_to(est, LEFT).shift(RIGHT * 0.25)
        estimate = VGroup(est, est_lines)
        page2 = VGroup(ftitle, form, create).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        page2.move_to(br.content).align_to(br.content, LEFT).shift(RIGHT * 0.3)
        estimate.move_to(ftitle).align_to(form.rows[0].field, RIGHT)   # top right, as on the real page
        foot1 = label("the README gives no settings: these are sensible choices", 20, S.GREY)
        foot2 = label("Debian 13 works too", 20, S.GREY)
        foot = VGroup(foot1, foot2).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        foot.next_to(br.frame, DOWN, buff=0.27).align_to(br.frame, LEFT).shift(RIGHT * 0.12)

        pin = pin_glyph(0.5)
        pin.shift(np.array([6.2, -0.12, 0]) - pin.tip())
        zone = mono("us-central1-a", 20, S.GREY).next_to(pin, LEFT, buff=0.15).shift(UP * 0.12)
        pin_start = pin.copy().shift(UP * 0.6).set_opacity(0)
        block = VGroup(box(2.2, 0.38, CLOUD, fill_opacity=0.25, radius=0.06),
                       label("CPU + memory", 20, INK))
        block[1].move_to(block[0])
        block.move_to(C.cpus[0]).set_y(C.slices[0].get_bottom()[1] + 0.28)
        disk_lab = label("disk · Debian 12", 20, CLOUD)
        disk_lab.next_to(C.disks[0], DOWN, buff=0.1).align_to(C.disks[0], LEFT).shift(LEFT * 0.1)

        def fill(row, rt=0.45):
            row.value.set_opacity(1)
            self.play(ShowIncreasingSubsets(row.value, rate_func=linear), run_time=rt)

        rows = form.rows
        with self.voiceover(SAY[2]) as vo:
            # the clicked "Create instance" button becomes the form's title (what became what)
            self.play(FadeOut(VGroup(sel, heading, note_box, note_t, prog_bg, prog), shift=UP * 0.3),
                      FadeTransform(create_i, ftitle), run_time=0.7)
            self.play(LaggedStart(*[FadeIn(VGroup(r.label, r.field)) for r in rows], lag_ratio=0.08),
                      FadeIn(create), FadeIn(estimate), run_time=0.8)
            vo.wait_until("so here are sensible")
            self.play(FadeIn(foot1, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("A name")
            fill(rows[0])
            self.play(Indicate(C.name, color=CLOUD, scale_factor=1.25), run_time=0.7)
            vo.wait_until("A region and zone")
            fill(rows[1], 0.4)
            fill(rows[2], 0.45)
            vo.wait_until("where the machine")
            self.play(ReplacementTransform(pin_start, pin), FadeIn(zone, shift=RIGHT * 0.1), run_time=0.6)
            vo.wait_until("A machine type")
            fill(rows[3], 0.4)
            vo.wait_until("which sets the CPUs")
            self.play(ReplacementTransform(C.cpus[0], block), run_time=0.8)
            vo.wait_until("e2-small is plenty")
            self.play(Indicate(rows[3].value, color=S.WHITE, scale_factor=1.2), run_time=0.7)
            vo.wait_until("And a boot disk")
            fill(rows[4], 0.7)
            self.play(FadeIn(disk_lab, shift=UP * 0.1), Indicate(C.disks[0], color=CLOUD), run_time=0.7)
            fill(rows[5], 0.4)
            vo.wait_until("Debian 13 works too")
            self.play(FadeIn(foot2, shift=UP * 0.1), run_time=0.6)

        # ========================================================== 3 · keep the external IP
        ip_row = rows[5]
        ip_hl = SurroundingRectangle(VGroup(ip_row.label, ip_row.field), color=TURN, buff=0.08,
                                     corner_radius=0.08, stroke_width=3)
        bus_x = C.xs[0] - 0.8
        start = np.array([bus_x, C.os[0].get_top()[1], 0])
        chips = [chip(s, S.GREY, size=22) for s in ("PyPI", "GitHub", "Debian mirrors")]
        ys = [1.3, 2.1, 2.9]
        for c, y in zip(chips, ys):
            c.move_to([0, y, 0]).set_x(bus_x + 0.4, LEFT)
        bus = Line(start, [bus_x, ys[-1], 0], color=LOOKUP, stroke_width=4)
        branches = [Line([bus_x, y, 0], [c.get_left()[0], y, 0], color=LOOKUP, stroke_width=4)
                    for c, y in zip(chips, ys)]
        hub = Dot(start, radius=0.07, color=LOOKUP)

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(foot), Create(ip_hl), run_time=0.6)
            self.play(FadeIn(hub, scale=0.5), Create(bus), run_time=0.7)
            self.play(LaggedStart(*[AnimationGroup(Create(b), FadeIn(c, shift=RIGHT * 0.1))
                                    for b, c in zip(branches, chips)], lag_ratio=0.3), run_time=1.1)
            vo.wait_until("on by default")
            self.play(Indicate(ip_row.value, color=TURN, scale_factor=1.15), run_time=0.8)
            vo.wait_until("Without it")
            self.play(ip_hl.animate(rate_func=there_and_back).set_stroke(width=8), run_time=0.8)
            vo.wait_until("can't reach the internet")
            flashes = [bus.copy().set_stroke(width=8)] + [b.copy().set_stroke(width=8) for b in branches]
            self.play(ShowPassingFlash(flashes[0], time_width=0.5), run_time=0.7)
            self.play(*[ShowPassingFlash(f, time_width=0.6) for f in flashes[1:]], run_time=0.5)
            vo.wait_until("every download")
            self.play(LaggedStart(*[Indicate(c, color=LOOKUP, scale_factor=1.1) for c in chips], lag_ratio=0.25),
                      run_time=1.2)

        # ========================================================== 4 · the meter starts
        dial = CostDial(radius=0.4, caption=None)
        dial.move_to([C.xs[0] - 0.6, 3.0, 0])
        cost = label("cost", 22, COST).next_to(dial, RIGHT, buff=0.2)
        tags = [gold_tag(["CPU + memory:", "billed per second while running"]),
                gold_tag(["disk: billed while it exists"]),
                gold_tag(["external IP:", "small hourly fee while running"])]
        top = dial.get_bottom()[1] - 0.18
        for tg in tags:                                   # stacked under the dial, left-aligned
            tg.move_to([0, top - tg.height / 2, 0]).set_x(SMALL["x0"] - 0.3, LEFT)
            top -= tg.height + 0.12
        est_tag = tag("estimate", COST).move_to(est)

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(hub, bus, *branches, *chips, pin, zone, ip_hl)), run_time=0.5)
            dial.tracker.add_updater(lambda m, dt: m.increment_value(dt * RATE))
            self.add(dial.tracker)
            self.play(FadeIn(dial, scale=0.8), FadeIn(cost, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("CPU and memory are billed")
            self.play(FadeIn(tags[0], shift=DOWN * 0.15), run_time=0.5)
            self.play(Indicate(block, color=COST, scale_factor=1.08), run_time=0.8)
            vo.wait_until("even when it sits idle")
            block.save_state()
            self.play(block.animate.fade(0.7), run_time=0.6)
            self.wait(0.9)
            self.play(Restore(block), run_time=0.5)
            vo.wait_until("The disk is billed")
            self.play(FadeIn(tags[1], shift=DOWN * 0.15), Indicate(C.disks[0], color=COST), run_time=0.7)
            vo.wait_until("for as long as it exists")
            self.play(FadeIn(tags[2], shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("The estimate is small")
            self.play(FadeIn(est_tag, scale=0.8), run_time=0.4)
            self.play(pulse(est_tag), run_time=0.7)
            vo.wait_until("never stops on its own")
            self.play(Circumscribe(dial.face, Circle, color=COST, buff=0.08), run_time=1.0)

        # ========================================================== 5 · Create, SSH, a terminal
        h3 = VGroup(label("Compute Engine", 26, INK), label("›", 26, S.GREY), label("VM instances", 26, INK))
        h3.arrange(RIGHT, buff=0.2)
        ok = check_mark(0.3, S.GREEN)
        inst_name = mono("ac215-l01", 22, INK)
        inst_zone = mono("us-central1-a", 22, S.GREY)
        inst_ip = label("External IP", 22, S.GREY)
        ssh = chip("SSH", CLOUD, size=22)
        inst = VGroup(ok, inst_name, inst_zone, inst_ip, ssh).arrange(RIGHT, buff=0.4)
        row_frame = box(inst.width + 0.5, inst.height + 0.36, S.GREY, fill_opacity=0.05, radius=0.08)
        row_frame.move_to(inst)
        page3 = VGroup(h3, VGroup(row_frame, inst)).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        page3.move_to(br.content).align_to(br.content, LEFT).align_to(br.content, UP).shift(RIGHT * 0.3 + DOWN * 0.3)

        beam = Line(ssh.get_right() + RIGHT * 0.05, C.slices[0].get_left() + RIGHT * 0.05 + UP * 0.1,
                    color=LOOKUP, stroke_width=5)
        mini_t = mono("ac215-l01", 20, CLOUD)
        mini_b = box(mini_t.width + 0.4, mini_t.height + 0.3, CLOUD, fill_opacity=0.15, radius=0.08)
        mini_t.move_to(mini_b)
        badge_dial = CostDial(radius=0.28, caption=None).move_to(BADGE_DIAL)
        mini = VGroup(mini_b, mini_t).next_to(badge_dial, LEFT, buff=0.2)

        dlg_t = label("authorize the connection?", 24, INK)
        dlg_btn = chip("Authorize", CLOUD, size=22)
        dlg_in = VGroup(dlg_t, dlg_btn).arrange(DOWN, buff=0.3)
        dlg_box = RoundedRectangle(width=dlg_in.width + 1.0, height=dlg_in.height + 0.8, corner_radius=0.14,
                                   stroke_color=S.GREY, stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
        dlg_in.move_to(dlg_box)
        dlg_tag = tag("first time only", S.GREY)
        dlg_tag.move_to(dlg_box.get_corner(UR) + np.array([-dlg_tag.width / 2 - 0.2, 0, 0]))
        dlg = VGroup(dlg_box, dlg_in, dlg_tag).move_to(br.content).shift(DOWN * 0.95)

        t = term(prompt=P_HOME, rows=9)
        t.shift(np.array([0 - t.box.get_center()[0], TERM_BOTTOM - t.box.get_bottom()[1], 0]))
        v1_rest = VGroup(C.server, C.hyp, *C.slices[1:], C.os, C.disks, C.link, C.storage, block, disk_lab)

        with self.voiceover(SAY[5]) as vo:
            self.play(Indicate(create, color=S.WHITE, scale_factor=1.15), FadeOut(VGroup(*tags)), run_time=0.6)
            form_parts = VGroup(ftitle, form, create, estimate, est_tag)
            self.play(form_parts.animate.scale(0.3, about_point=row_frame.get_center()).set_opacity(0),
                      FadeIn(h3), FadeIn(row_frame), FadeIn(VGroup(inst_name, inst_zone, inst_ip, ssh)),
                      run_time=0.8)
            self.remove(form_parts)
            vo.wait_until("wait for the green check")
            self.play(Create(ok), run_time=0.5)
            self.play(Indicate(ok, color=S.GREEN, scale_factor=1.4), run_time=0.5)
            vo.wait_until("then click SSH")
            self.play(Indicate(ssh, color=S.WHITE, scale_factor=1.25), tr.goto(2), run_time=0.5)
            self.play(Create(beam), run_time=0.5)
            self.play(ShowPassingFlash(beam.copy().set_stroke(width=10), time_width=0.5),
                      Indicate(C.slices[0], color=LOOKUP, scale_factor=1.04), run_time=0.7)
            # V1 and the meter become a badge (the needle keeps sweeping: the VM exists)
            badge_dial.tracker.set_value(dial.tracker.get_value())
            dial.tracker.clear_updaters()
            self.remove(dial.tracker)
            badge_dial.tracker.add_updater(lambda m, dt: m.increment_value(dt * RATE))
            self.add(badge_dial.tracker)
            self.play(ReplacementTransform(C.slices[0], mini_b), ReplacementTransform(C.name, mini_t),
                      FadeOut(v1_rest, scale=0.3, target_position=mini.get_center()),
                      FadeOut(beam), FadeOut(dial, scale=0.5, target_position=BADGE_DIAL),
                      FadeOut(cost, target_position=BADGE_DIAL), FadeIn(badge_dial), run_time=1.0)
            vo.wait_until("If it asks you")
            self.play(FadeIn(dlg, scale=0.92), run_time=0.5)
            vo.wait_until("click Authorize")
            self.play(Indicate(dlg_btn, color=S.WHITE, scale_factor=1.2), run_time=0.7)
            self.play(FadeOut(dlg, scale=0.95), run_time=0.4)
            vo.wait_until("A terminal opens")
            self.play(ReplacementTransform(br.frame, t.box),
                      FadeOut(VGroup(*[m for m in br.submobjects if m is not br.frame]), ill, page3),
                      FadeIn(VGroup(t.bar, t.dots, t.title)), run_time=1.1)
            self.remove(t.box, t.bar, t.dots, t.title)
            self.add(t)
            p0 = self.bare_prompt(t)
            vo.wait_until("logged in to your new VM")
            self.play(Indicate(t.title, color=CLOUD, scale_factor=1.25), run_time=0.9)
            vo.wait_until("Our prompt says student")
            who = substring(p0, "student")
            yt_name = tag("your username here", TURN)
            yt_name.next_to(who, DOWN, buff=0.42).align_to(who, LEFT).shift(LEFT * 0.05)
            stem = Line([who.get_center()[0], yt_name.get_top()[1], 0],
                        [who.get_center()[0], p0.strut.get_bottom()[1], 0], color=TURN, stroke_width=3)
            self.play(Indicate(who, color=TURN, scale_factor=1.2), run_time=0.7)
            self.play(FadeIn(yt_name, shift=UP * 0.1), Create(stem), run_time=0.5)
            vo.wait_until("Pause here")
            yt = your_turn().next_to(p0.strut, RIGHT, buff=0.35)
            self.pin(p0, yt, run_time=0.5)
            self.play(pulse(yt), run_time=0.7)

        # ========================================================== 6 · which OS?
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(yt_name), FadeOut(stem), run_time=0.4)
            self.unpin(p0, yt)
            vo.wait_until("extra checks")
            caption_extra(self, tr)
            vo.wait_until("First, which operating system")
            l_cat = self.type_cmd(t, CAT, type_time=0.9)
            xt1 = extra_tag().next_to(l_cat.strut, RIGHT, buff=0.5)
            self.pin(l_cat, xt1)
            vo.wait_until("Print the os-release file")
            t.print(self, OS_RELEASE, run_time=0.8)
            pretty = t.find("PRETTY_NAME")
            bar = Rectangle(width=pretty.strut.width + 0.25, height=t.pitch, stroke_width=0).set_fill(TURN, 0.18)
            bar.move_to(pretty.strut)
            vo.wait_until("Debian 12, nicknamed")
            self.play(FadeIn(bar), run_time=0.5)
            self.remove(bar)
            pretty.add_to_back(bar)
            vo.wait_until("bookworm")
            bw = substring(pretty, "bookworm")
            u = Line([bw.get_left()[0] - 0.03, pretty.strut.get_bottom()[1] + 0.01, 0],
                     [bw.get_right()[0] + 0.03, pretty.strut.get_bottom()[1] + 0.01, 0], color=TURN, stroke_width=4)
            self.play(Create(u), run_time=0.5)
            self.remove(u)
            pretty.add(u)

        # ========================================================== 7 · which python3?
        card_t = label("Debian 13", 22, S.GREY)
        card_v = mono(PY13, 22, OUTPUT)
        card_in = VGroup(card_t, card_v).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        card_box = RoundedRectangle(width=card_in.width + 0.7, height=card_in.height + 0.5, corner_radius=0.12,
                                    stroke_color=S.GREY, stroke_width=2.5).set_fill(TERM_BG, 1)
        card_in.move_to(card_box)
        card = VGroup(card_box, card_in)
        card.move_to([0, 1.95, 0]).set_x(6.45, RIGHT)

        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(bar), FadeOut(u), run_time=0.4)
            pretty.remove(bar, u)
            l_py = self.type_cmd(t, PYV, type_time=0.8)
            xt2 = tag("extra", S.GREY).next_to(l_py.strut, RIGHT, buff=0.5)
            self.pin(l_py, xt2, run_time=0.3)
            out = t.print(self, [PY12], run_time=0.4)[0]
            vo.wait_until("Debian 12 ships")
            self.play(Indicate(substring(out, "3.11.2"), color=SYSTEM, scale_factor=1.25), run_time=0.8)
            vo.wait_until("for the operating system")
            # pad_y 0.08: a tag-high pill (0.47); the default chip (0.55) is taller than a terminal
            # row and its edges cut the glyphs of the rows above and below
            sp = chip("system Python", SYSTEM, size=22, pad_y=0.08).next_to(out.strut, RIGHT, buff=0.5)
            self.pin(out, sp, run_time=0.5)
            vo.wait_until("On Debian 13")
            self.play(FadeIn(card, shift=LEFT * 0.3), run_time=0.6)
            vo.wait_until("Keep both numbers")
            self.play(Indicate(substring(out, "3.11.2"), color=SYSTEM, scale_factor=1.25),
                      Indicate(card_v[-6:], color=S.WHITE, scale_factor=1.25), run_time=1.0)

        # ========================================================== 8 · which python?
        # t2f only behaves for a leading span here, so the second half is three pieces set on one
        # baseline (the bottoms of o / h / e, which sit on it)
        cap_a = label("which: the program a name would run", 22, LOOKUP, t2f={"which": MONO})
        dot = label("·", 22, LOOKUP)
        only, py3, rest = label("only", 22, LOOKUP), mono("python3", 22, LOOKUP), label("exists here", 22, LOOKUP)
        cap_c = VGroup(only, py3, rest).arrange(RIGHT, buff=0.14)
        base = only[0].get_bottom()[1]
        py3.shift(UP * (base - py3[3].get_bottom()[1]))
        rest.shift(UP * (base - rest[0].get_bottom()[1]))
        VGroup(cap_a, dot, cap_c).arrange(RIGHT, buff=0.25)
        cap_c.shift(UP * (cap_a[-1].get_bottom()[1] - only[0].get_bottom()[1]))     # 'n' of "run"
        dot.set_y(only[0].get_center()[1])
        cap_b = VGroup(dot, cap_c)
        VGroup(cap_a, cap_b).move_to([0, 1.62, 0])

        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(card, shift=RIGHT * 0.3), run_time=0.4)
            l_wh = self.type_cmd(t, WHICH, type_time=0.7)
            xt3 = tag("extra", S.GREY).next_to(l_wh.strut, RIGHT, buff=0.5)
            self.pin(l_wh, xt3, run_time=0.3)
            vo.wait_until("without the 3")
            self.play(Indicate(substring(l_wh, "python"), color=LOOKUP, scale_factor=1.2), run_time=0.8)
            vo.wait_until("The which command")
            self.play(FadeIn(cap_a, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("For python, nothing")
            p_back = self.bare_prompt(t)
            nothing = tag("nothing", ERR).next_to(p_back.strut, RIGHT, buff=0.35)
            self.play(FadeIn(nothing, scale=0.8), run_time=0.3)
            for _ in range(2):
                self.play(nothing.animate.set_opacity(0.15), run_time=0.2)
                self.play(nothing.animate.set_opacity(1), run_time=0.2)
            vo.wait_until("Debian has python3")
            self.play(FadeIn(cap_b, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("Remember this")
            self.play(Indicate(py3, color=S.WHITE, scale_factor=1.08), run_time=0.8)

        badge_dial.tracker.clear_updaters()
        self.remove(badge_dial.tracker)
        badge_dial.freeze()
        old = list(self.mobjects)
        self.play(FadeOut(Group(*old)), run_time=0.8)
        self.remove(*old)
