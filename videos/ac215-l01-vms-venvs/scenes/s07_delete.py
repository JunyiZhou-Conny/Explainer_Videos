"""S07 · Delete, don't stop (walkthrough: README step 10, Delete VM; the end of part 1).

Beats (script.md "## S07", one voiceover block each):
 0  TRACKER A10. The schematic console (GREY browser, tag illustration): Compute Engine › VM
    instances, a toolbar with "Stop" and "Delete", the `ac215-l01` row. On "delete the VM" the
    row's checkbox ticks and Delete lights up. A GREY README card at right, header
    `README.md · line 62`, quoting the real line: "keeps charging" turns GOLD, "even when idle"
    underlines GOLD. "So why delete it" -> Delete pulses; "not just stop it" -> Stop pulses.
 1  The card leaves; the V1 coda takes its place (S03's picture): server, hypervisor, our BLUE
    slice (Debian 12, `ac215-l01`, a "CPU + memory" block), its linked BLUE disk "disk · Debian 12",
    and the GOLD dial, sweeping. Stop is pressed: the row's status turns GREY, the CPU/memory block
    greys out and the needle slows to a slow sweep; the disk stays BLUE (it lights up, then flashes
    GOLD as the GOLD tag "disk: still billing" appears); a dashed GOLD chip "reserved IP: also
    billing".
 2  Delete is pressed: the page dims under a confirm dialog that pops out of the Delete button (it
    carries the live `illustration` tag; the browser's own tag dims) "Delete ac215-l01? / Its boot
    disk is deleted with it" (YELLOW bar as it's said; the slice->disk link flashes), GREY tag
    "default · a setting on the boot disk". "And the meter stops": the slice and its disk (and the
    GOLD billing tags) dissolve, the needle stops where it is (no rewind). ▶ your turn beside the
    toolbar's Delete, just above the dialog; the dialog's Delete pulses on "click Delete" and the
    dialog closes; on "until it's gone" the row leaves the list.
 3  The empty list's heading "VM instances" becomes the first line of a checklist card
    "VM instances: empty" / "Disks: empty" (GREEN ticks as each is named) while the browser and
    the rest of V1 clear. TRACKER A10 · extra: a
    3-row laptop terminal along the bottom (title "your laptop", GREY tag "optional · needs the
    gcloud CLI on your laptop") types `gcloud compute instances list` and `gcloud compute disks
    list` (no output shown); each one lights its checklist row; a GREY bracket "extra · not in the
    README" on "Neither is in the README".
 4  Part-1 recap strip: BLUE VM slice -> the crowded ORANGE `/usr/local/… (pip's)` shelf (12 jars)
    -> RED tag "shared with the whole OS". Closing card "Part 2 · the same app, on a fresh VM, the
    clean way" with a small GREEN venv box. Fade out to an empty frame (end of part 1).

Nothing here is terminal output: the README sentence comes from excerpt("README.md", 62, 62), and
the gcloud commands are typed exactly as script.md spells them, with no output (none was captured).
"""

import numpy as np
from manim import *

from explainer import style as S
from explainer.devops import (PANEL, TERM_BG, box, browser_window, check_mark, chip, label,
                              layer_bar, mono, server, tag)
from explainer.scene import VoiceScene

from common import (CLOUD, COST, ERR, INK, NARRATION, SYSTEM, TURN, VENV, CostDial, excerpt,
                    illustration_tag, jars, term, tracker_a, your_turn)

SAY = NARRATION["S07"]

# ------------------------------------------------------------------ the README's own words
README_62 = excerpt("README.md", 62, 62)
QUOTE = ["A running VM", "keeps charging", "even when idle."]
assert " ".join(QUOTE) in README_62, README_62

# ------------------------------------------------------------------ commands (script.md spelling)
LIST_VMS = "gcloud compute instances list"         # extra: not in the README
LIST_DISKS = "gcloud compute disks list"           # extra: not in the README
assert LIST_VMS not in README_62 and "gcloud" not in excerpt("README.md", 1, 200)

URL = "console.cloud.google.com/compute/instances"

# ------------------------------------------------------------------ layout
TRACK_LEFT, TRACK_TOP = -6.5, 3.5
BR_LEFT, BR_TOP, BR_W, BR_H = -6.55, 2.75, 8.7, 5.3       # the console (left; as in S03)
C_LEFT = BR_LEFT + 0.35                                   # left edge of the page content
LIST_RIGHT = 1.75                                         # right end of the instance list
D_LEFT, D_RIGHT = C_LEFT + 0.55, 1.9                      # the confirm dialog's sides
TERM_BOTTOM = -3.45

# V1 coda (right of the browser): S03's picture, our slice wide, three thin neighbours
X0, WIDTHS, GAP = 2.75, [2.4, 0.36, 0.36, 0.36], 0.1       # S03's small layout
SLICE = (-0.45, 0.95)                                     # our slice, bottom and top
OS_H, HYP_H, SERVER_H = 0.4, 0.36, 0.7
DISK_Y, DISK_W, DISK_H, DISK_PITCH = -2.3, 0.44, 0.38, 0.56
DIAL_C, DIAL_R = np.array([2.95, 2.3, 0]), 0.46

RUN, STOPPED = 1 / 7, 1 / 40                              # dial turns per second: running, stopped


# ------------------------------------------------------------------ glyphs (S03's V1 vocabulary)
def wide_server(w: float, h: float, color=S.GREY) -> VGroup:
    """The house rack glyph (`server()`), widened to w (as in S03)."""
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
    """A small disk (a cylinder), as in S03."""
    e = w * 0.3
    rect = Rectangle(width=w, height=h)
    top = Ellipse(width=w, height=e).move_to(rect.get_top())
    bot = Ellipse(width=w, height=e).move_to(rect.get_bottom())
    body = Union(rect, top, bot).set_stroke(color, 2.5).set_fill(color, 0.22)
    lid = Ellipse(width=w, height=e, stroke_color=color, stroke_width=2.5).set_fill(color, 0.45)
    lid.move_to(rect.get_top())
    return VGroup(body, lid)


def gold_tag(lines: list[str], size: float = 20, dashed: bool = False) -> VGroup:
    """A GOLD billing tag of one or two lines (S03's look: GOLD text on an opaque dark pill);
    dashed = hypothetical."""
    t = VGroup(*[label(s, size, COST) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    w, h = t.width + 0.36, t.height + 0.26
    r = min(0.16, h / 2)
    if dashed:
        bg = RoundedRectangle(width=w, height=h, corner_radius=r, stroke_width=0).set_fill(S.BG, 0.92)
        edge = DashedVMobject(RoundedRectangle(width=w, height=h, corner_radius=r), num_dashes=30,
                              dashed_ratio=0.55).set_stroke(COST, 2)
        b = VGroup(bg, edge)
    else:
        b = RoundedRectangle(width=w, height=h, corner_radius=r, stroke_color=COST,
                             stroke_width=2).set_fill(S.BG, 0.92)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def icon_chip(icon: VMobject, s: str, color=S.GREY, size: float = 24) -> VGroup:
    """A console button: a small icon and a word in a GREY pill. .box .text .icon"""
    t = label(s, size, INK)
    inner = VGroup(icon, t).arrange(RIGHT, buff=0.14)
    h = mono("|", size).height + 0.24
    b = box(inner.width + 0.5, h, color, fill_opacity=0.16, radius=h / 2.6)
    inner.move_to(b)
    g = VGroup(b, inner)
    g.box, g.text, g.icon = b, t, icon
    return g


def stop_icon(s: float = 0.17, color=INK) -> Square:
    return Square(side_length=s, stroke_width=0).set_fill(color, 1)


def trash_icon(h: float = 0.24, color=INK) -> VGroup:
    w = h * 0.8
    can = Polygon([-w / 2, h * 0.3, 0], [w / 2, h * 0.3, 0], [w * 0.38, -h / 2, 0], [-w * 0.38, -h / 2, 0],
                  stroke_color=color, stroke_width=2.2)
    lid = Line([-w * 0.62, h * 0.42, 0], [w * 0.62, h * 0.42, 0], color=color, stroke_width=2.5)
    knob = Line([-w * 0.18, h * 0.52, 0], [w * 0.18, h * 0.52, 0], color=color, stroke_width=2.5)
    ribs = VGroup(*[Line([x, h * 0.18, 0], [x * 0.85, -h * 0.36, 0], color=color, stroke_width=1.6)
                    for x in (-w * 0.17, w * 0.17)])
    return VGroup(can, lid, knob, ribs)


def checkbox(s: float = 0.28) -> VGroup:
    """An empty console checkbox; .tick (hidden) and .fill_anims() tick it (BLUE, like the console)."""
    sq = RoundedRectangle(width=s, height=s, corner_radius=0.04, stroke_color=S.GREY,
                          stroke_width=2).set_fill(TERM_BG, 1)
    tick = check_mark(s * 0.62, INK, stroke=3.5).move_to(sq).shift(DOWN * s * 0.02)
    g = VGroup(sq)
    g.sq, g.tick = sq, tick
    return g


def stopped_icon(s: float = 0.24) -> Square:
    return Square(side_length=s, stroke_color=S.GREY, stroke_width=2.5).set_fill(S.GREY, 0.5)


def pulse(m, factor: float = 1.15):
    """A tag's pulse: grow and settle back (Indicate would flood an opaque tag with its colour)."""
    return m.animate(rate_func=there_and_back).scale(factor)


def place_tracker(tr):
    tr.shift(np.array([TRACK_LEFT - tr.get_left()[0], TRACK_TOP - tr.get_top()[1], 0]))
    return tr


def caption_extra(tr):
    """The tracker caption with ' · extra' while a non-README command is on screen (S03's way):
    returns (new caption, its ' · extra' glyphs). Fade in only the suffix, then swap_caption():
    a Transform between captions of different lengths scrambles the letters mid-way."""
    k = tr.k
    s = f"step {k} of {len(tr.steps)}: {tr.steps[k - 1]}"
    new = label(s + " · extra", tr.size, tr.hi_color, t2c={"· extra": S.GREY})
    new.next_to(tr.dots, RIGHT, buff=0.25)
    n = len(label(s, tr.size, tr.hi_color).submobjects)
    return new, VGroup(*new.submobjects[n:])


def swap_caption(scene, tr, new, suffix):
    scene.remove(tr.caption, suffix)
    tr.remove(tr.caption)
    tr.caption = new
    tr.add(new)
    scene.add(tr)


def ring(dial, color=COST) -> Succession:
    """Circumscribe for the dial: a ring just outside its face, drawn from the top and faded.
    (Circumscribe's Circle surrounds the bounding box's diagonal and crossed the 'cost' label.)"""
    r = Circle(radius=dial.radius + 0.09, stroke_color=color, stroke_width=4).move_to(dial.face)
    r.rotate(PI / 2, about_point=dial.face.get_center())
    return Succession(Create(r, run_time=0.55), FadeOut(r, run_time=0.3))


def readme_card(line_no: int, body: VGroup) -> VGroup:
    """A GREY README card: header 'README.md · line n', the README's own words, a quote bar."""
    head = VGroup(mono("README.md", 20, S.GREY), label(f"· line {line_no}", 20, S.GREY))
    head.arrange(RIGHT, buff=0.12)
    bar = Line(body.get_corner(UL) + np.array([-0.22, 0.04, 0]),
               body.get_corner(DL) + np.array([-0.22, -0.04, 0]), color=S.GREY, stroke_width=4)
    inner = VGroup(head, VGroup(bar, body)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    frame = box(inner.width + 0.55, inner.height + 0.4, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
    inner.move_to(frame).align_to(frame, LEFT).shift(RIGHT * 0.28)
    g = VGroup(frame, inner)
    g.frame, g.head = frame, head
    return g


def words(t: Text, sub: str) -> VGroup:
    """The glyphs of `sub` inside a Text (spaces have no glyphs)."""
    s = t.text
    i = s.find("".join(sub.split()))
    assert i >= 0, (sub, s)
    return VGroup(*t.submobjects[i:i + len("".join(sub.split()))])


def under(g, color, stroke: float = 3.5, dy: float = 0.07) -> Line:
    y = g.get_bottom()[1] - dy
    return Line([g.get_left()[0] - 0.03, y, 0], [g.get_right()[0] + 0.03, y, 0], color=color,
                stroke_width=stroke)


def dust(mob, color, rng, n: int, r: float = 0.03) -> VGroup:
    """Small dots scattered over mob's area (what a dissolving thing turns into)."""
    lo, hi = mob.get_corner(DL), mob.get_corner(UR)
    pts = np.c_[rng.uniform(lo[0], hi[0], n), rng.uniform(lo[1], hi[1], n), np.zeros(n)]
    return VGroup(*[Dot(p, radius=r, color=color) for p in pts])


def bracket(top: float, bottom: float, x: float, color, tick: float = 0.13) -> VMobject:
    """A ']' at x from y=top to y=bottom, ticks pointing left."""
    m = VMobject(stroke_color=color, stroke_width=3)
    m.set_points_as_corners([[x - tick, top, 0], [x, top, 0], [x, bottom, 0], [x - tick, bottom, 0]])
    return m


# ------------------------------------------------------------------ V1 coda
def build_v1() -> VGroup:
    """S03's V1, right of the browser: server, hypervisor, four slices (ours BLUE and wide), our
    OS layer, name, CPU/memory block, three BLUE disks with ours linked and labelled.
    Parts: .server .hyp .slices .os .name .block .disks .link .disk_lab .storage .ours .xs"""
    v = VGroup()
    y0, y1 = SLICE
    xs, x = [], X0
    for w in WIDTHS:
        xs.append(x + w / 2)
        x += w + GAP
    total = sum(WIDTHS) + GAP * (len(WIDTHS) - 1)
    cx = X0 + total / 2
    v.slices, v.os = VGroup(), VGroup()
    for i, (xc, w) in enumerate(zip(xs, WIDTHS)):
        col = CLOUD if i == 0 else S.GREY
        v.slices.add(box(w, y1 - y0, col, fill_opacity=0.15 if i == 0 else 0.1, radius=0.08)
                     .move_to([xc, (y0 + y1) / 2, 0]))
        bar = layer_bar("Debian 12" if i == 0 else " ", w, OS_H, col, size=20, fill_opacity=0.3)
        v.os.add(bar.move_to([xc, y1 + OS_H / 2, 0]))
    v.hyp = layer_bar("hypervisor", total, HYP_H, S.GREY, size=20, fill_opacity=0.25)
    v.hyp.move_to([cx, y0 - HYP_H / 2, 0])
    v.server = wide_server(total, SERVER_H).move_to([cx, y0 - HYP_H - SERVER_H / 2, 0])
    v.name = mono("ac215-l01", 22, CLOUD).move_to([xs[0], y1 - 0.3, 0])
    bb = box(2.2, 0.42, CLOUD, fill_opacity=0.25, radius=0.06)
    v.block = VGroup(bb, label("CPU + memory", 20, INK).move_to(bb)).move_to([xs[0], y0 + 0.33, 0])
    first = X0 + 0.1 + DISK_W / 2
    v.disks = VGroup(*[disk_glyph(DISK_W, DISK_H).move_to([first + k * DISK_PITCH, DISK_Y, 0])
                       for k in range(3)])
    xl, ys = X0 - 0.3, (y0 + y1) / 2
    v.link = VMobject(stroke_color=CLOUD, stroke_width=3).set_points_as_corners(
        [[X0, ys, 0], [xl, ys, 0], [xl, DISK_Y, 0], [v.disks[0].get_left()[0], DISK_Y, 0]])
    v.disk_lab = label("disk · Debian 12", 20, CLOUD)
    v.disk_lab.next_to(v.disks[0], DOWN, buff=0.14).align_to(v.disks[0], LEFT).shift(LEFT * 0.12)
    v.storage = label("storage network", 20, S.GREY).move_to([0, DISK_Y, 0])
    v.storage.set_x(v.disks[-1].get_right()[0] + 0.16, LEFT)
    v.ours = VGroup(v.slices[0], v.os[0], v.name, v.block)
    v.xs = xs
    v.add(v.server, v.hyp, v.slices, v.os, v.name, v.block, v.disks, v.link, v.disk_lab, v.storage)
    return v


class DeleteVM(VoiceScene):
    def construct(self):
        assert len(SAY) == 5, f"S07 has {len(SAY)} SAY lines; this scene times 5"
        rng = np.random.default_rng(7)

        # ========================================================== 0 · step 10: delete the VM
        tr = place_tracker(tracker_a(9))
        br = browser_window(URL, width=BR_W, height=BR_H)
        br.shift(np.array([BR_LEFT - br.frame.get_left()[0], BR_TOP - br.frame.get_top()[1], 0]))
        ill = illustration_tag()          # on the bottom edge: the top edge is the address bar
        ill.move_to(br.frame.get_corner(DR) + np.array([-ill.width / 2 - 0.3, 0, 0]))

        heading = VGroup(label("Compute Engine", 28, INK), label("›", 28, S.GREY),
                         label("VM instances", 28, INK)).arrange(RIGHT, buff=0.2)
        heading.move_to([0, 1.78, 0]).set_x(C_LEFT, LEFT)
        stop_b = icon_chip(stop_icon(), "Stop")
        del_b = icon_chip(trash_icon(), "Delete")
        toolbar = VGroup(stop_b, del_b).arrange(RIGHT, buff=0.3).move_to([0, 1.0, 0]).set_x(C_LEFT, LEFT)
        sep = Line([C_LEFT - 0.1, 0.5, 0], [LIST_RIGHT, 0.5, 0], color=S.GREY_DARK,
                   stroke_width=2)
        X_CB, X_ST, X_NAME, X_ZONE, X_CONN = C_LEFT + 0.2, C_LEFT + 0.62, C_LEFT + 1.7, C_LEFT + 3.75, C_LEFT + 6.5
        Y_HEAD, Y_ROW = 0.12, -0.6
        cb_head = checkbox().move_to([X_CB, Y_HEAD, 0])
        heads = VGroup(*[label(s, 22, S.GREY).move_to([0, Y_HEAD, 0]).set_x(x, LEFT)
                         for s, x in (("Status", X_ST), ("Name", X_NAME), ("Zone", X_ZONE), ("Connect", X_CONN))])
        cb = checkbox().move_to([X_CB, Y_ROW, 0])
        running = check_mark(0.28, S.GREEN).move_to([X_ST + 0.2, Y_ROW, 0])
        stopped = stopped_icon().move_to(running)
        r_name = mono("ac215-l01", 22, INK).move_to([0, Y_ROW, 0]).set_x(X_NAME, LEFT)
        r_zone = mono("us-central1-a", 22, S.GREY).move_to([0, Y_ROW, 0]).set_x(X_ZONE, LEFT)
        r_ssh = chip("SSH", CLOUD, size=22).move_to([0, Y_ROW, 0]).set_x(X_CONN, LEFT)
        row_frame = box(LIST_RIGHT - (C_LEFT - 0.1), 0.66, S.GREY, fill_opacity=0.05,
                        radius=0.08)
        row_frame.move_to([(C_LEFT - 0.1 + LIST_RIGHT) / 2, Y_ROW, 0])
        row = VGroup(row_frame, cb, running, r_name, r_zone, r_ssh)
        page = VGroup(heading, toolbar, sep, cb_head, heads, row)

        q = VGroup(*[label(s, 28, INK) for s in QUOTE]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        card = readme_card(62, q)
        card.move_to([0, 0.75, 0]).set_x(6.5, RIGHT)
        assert card.get_left()[0] > br.frame.get_right()[0] + 0.12, card.get_left()
        charging = words(q[1], "keeps charging")
        idle = words(q[2], "even when idle")
        idle_ul = under(idle, COST)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.1), FadeIn(br, shift=RIGHT * 0.3), FadeIn(ill), run_time=0.7)
            self.play(tr.goto(10), FadeIn(page, shift=UP * 0.1), run_time=0.7)
            vo.wait_until("delete the VM")
            cb.tick.move_to(cb.sq).shift(DOWN * 0.005)
            self.play(cb.sq.animate.set_fill(CLOUD, 1).set_stroke(CLOUD), Create(cb.tick),
                      row_frame.animate.set_stroke(CLOUD).set_fill(CLOUD, 0.1), run_time=0.45)
            self.remove(cb.tick)
            cb.add(cb.tick)
            self.play(Indicate(del_b, color=S.WHITE, scale_factor=1.15), run_time=0.7)
            vo.wait_until("As the README says")
            self.play(FadeIn(card, shift=LEFT * 0.3), run_time=0.6)
            vo.wait_until("keeps charging")
            self.play(charging.animate.set_color(COST), run_time=0.4)
            self.play(Indicate(charging, color=COST, scale_factor=1.12), run_time=0.6)
            vo.wait_until("even when idle")
            self.play(Create(idle_ul), idle.animate.set_color(COST), run_time=0.6)
            vo.wait_until("So why delete it")
            self.play(Indicate(del_b, color=S.WHITE, scale_factor=1.15), run_time=0.7)
            vo.wait_until("and not just stop it")
            self.play(Indicate(stop_b, color=S.WHITE, scale_factor=1.15), run_time=0.7)

        # ========================================================== 1 · Stop: the disk keeps billing
        V = build_v1()
        dial = CostDial(radius=DIAL_R, caption=None).move_to(DIAL_C)
        cost = label("cost", 22, COST).next_to(dial, UP, buff=0.18)     # clear of ring()
        rate = ValueTracker(RUN)
        dial.tracker.add_updater(lambda m, dt: m.increment_value(dt * rate.get_value()))
        still = gold_tag(["disk: still billing"])
        still.move_to([0, DIAL_C[1] + 0.38, 0]).set_x(dial.get_right()[0] + 0.3, LEFT)
        rip = gold_tag(["reserved IP:", "also billing"], dashed=True)
        rip.next_to(still, DOWN, buff=0.14, aligned_edge=LEFT)
        block_grey = V.block.copy()
        block_grey[0].set_stroke(S.GREY).set_fill(S.GREY, 0.12)
        block_grey[1].set_color(S.GREY)

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(card, shift=RIGHT * 0.3), FadeOut(idle_ul, shift=RIGHT * 0.3), run_time=0.35)
            self.play(FadeIn(V, shift=LEFT * 0.2), FadeIn(dial, scale=0.8), FadeIn(cost), run_time=0.6)
            self.add(dial.tracker)        # the needle starts once the dial is in (no jump)
            vo.wait_until("ends the billing")
            self.play(Indicate(stop_b, color=S.WHITE, scale_factor=1.15), run_time=0.5)
            vo.wait_until("CPU and memory")
            self.play(Transform(V.block, block_grey), Transform(running, stopped),
                      rate.animate.set_value(STOPPED), run_time=0.8)
            vo.wait_until("but the disk")
            self.play(Indicate(V.disks[0], color=CLOUD, scale_factor=1.3),
                      ShowPassingFlash(V.link.copy().set_stroke(CLOUD, 7), time_width=0.5),
                      Indicate(V.disk_lab, color=CLOUD, scale_factor=1.12), run_time=0.9)
            vo.wait_until("so it keeps billing")
            self.play(FadeIn(still, shift=LEFT * 0.15), Indicate(V.disks[0], color=COST, scale_factor=1.25),
                      run_time=0.6)
            self.play(ring(dial))
            vo.wait_until("a reserved IP")
            self.play(FadeIn(rip, shift=LEFT * 0.15), run_time=0.5)

        # ========================================================== 2 · Delete: the meter stops
        dim = Rectangle(width=BR_W - 0.04, height=BR_H - 0.57, stroke_width=0).set_fill(S.BG, 0.62)
        dim.align_to(br.frame, DOWN).shift(UP * 0.02).set_x(br.frame.get_x())    # the page, under the address bar
        d_title = VGroup(label("Delete", 28, INK), mono("ac215-l01", 26, INK), label("?", 28, INK))
        d_title.arrange(RIGHT, buff=0.12)
        d_title[2].next_to(d_title[1], RIGHT, buff=0.05)
        for m in d_title[1:]:
            m.align_to(d_title[0], DOWN)
        d_body = label("Its boot disk is deleted with it", 24, INK)
        d_default = tag("default · a setting on the boot disk", S.GREY)
        d_text = VGroup(d_title, d_body, d_default).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        cancel = chip("Cancel", S.GREY, size=22)
        confirm = chip("Delete", CLOUD, size=22)
        buttons = VGroup(cancel, confirm).arrange(RIGHT, buff=0.25)
        yt = your_turn()
        d_w = D_RIGHT - D_LEFT          # covers Status..Connect; the ticked checkbox stays in view
        d_h = d_text.height + buttons.height + 0.9
        d_frame = RoundedRectangle(width=d_w, height=d_h, corner_radius=0.14, stroke_color=S.GREY,
                                   stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
        d_frame.move_to([(D_LEFT + D_RIGHT) / 2, -0.8, 0])
        d_text.move_to(d_frame).align_to(d_frame, UP).align_to(d_frame, LEFT).shift(RIGHT * 0.4 + DOWN * 0.32)
        buttons.align_to(d_frame, RIGHT).align_to(d_frame, DOWN).shift(LEFT * 0.35 + UP * 0.26)
        d_ill = illustration_tag()
        d_ill.move_to(d_frame.get_corner(UR) + np.array([-d_ill.width / 2 - 0.12, 0, 0]))
        # ▶ your turn beside the toolbar's Delete, just above the dialog: it outlives the dialog,
        # so it is still up while the row leaves the list ("pause until it's gone")
        yt.next_to(del_b, RIGHT, buff=0.3)
        # clear of the dialog's tag even mid-pulse (pulse() scales by 1.15)
        assert yt.get_right()[0] + 0.08 * yt.width < d_ill.get_left()[0] - 0.12, (yt.get_right(), d_ill.get_left())
        assert yt.get_bottom()[1] > d_frame.get_top()[1] + 0.05, (yt.get_bottom(), d_frame.get_top())
        dialog = VGroup(d_frame, d_title, d_body, buttons, d_ill)
        body_bar = Rectangle(width=d_body.width + 0.16, height=d_body.height + 0.14, stroke_width=0) \
            .set_fill(TURN, 0.2).move_to(d_body)

        gone_v = VGroup(V.ours, V.disks[0], V.link, V.disk_lab)
        dust_v = VGroup(dust(VGroup(V.slices[0], V.os[0]), CLOUD, rng, 46),
                        dust(V.disks[0], CLOUD, rng, 10), dust(V.disk_lab, CLOUD, rng, 10))
        gold_dust = VGroup(dust(still, COST, rng, 14), dust(rip, COST, rng, 14))

        with self.voiceover(SAY[2]) as vo:
            self.play(Indicate(del_b, color=S.WHITE, scale_factor=1.15), run_time=0.4)
            ill.save_state()                  # the dialog carries the live `illustration` tag now
            # the dialog pops out of the Delete button (opaque all the way: no ghosting over the row)
            self.play(FadeIn(dim), GrowFromPoint(dialog, del_b.get_center()), ill.animate.set_opacity(0.25),
                      run_time=0.5)
            vo.wait_until("removes the VM")
            self.play(Indicate(V.slices[0], color=CLOUD, scale_factor=1.04),
                      Indicate(d_title[1], color=CLOUD, scale_factor=1.12), run_time=0.8)
            vo.wait_until("its boot disk goes")
            self.play(FadeIn(body_bar), run_time=0.4)
            self.play(ShowPassingFlash(V.link.copy().set_stroke(CLOUD, 7), time_width=0.5),
                      Indicate(V.disks[0], color=CLOUD, scale_factor=1.3), run_time=0.9)
            vo.wait_until("That's a setting")
            self.play(FadeIn(d_default, shift=UP * 0.1), FadeOut(body_bar), run_time=0.5)
            vo.wait_until("and it's on")
            self.play(pulse(d_default, 1.1), Indicate(V.disk_lab, color=CLOUD, scale_factor=1.12), run_time=0.8)
            vo.wait_until("And the meter stops")
            self.play(FadeOut(gone_v, scale=0.96), FadeOut(VGroup(still, rip)),
                      FadeIn(dust_v), FadeIn(gold_dust), run_time=0.35)
            drift = [d.animate.shift(UP * rng.uniform(0.25, 0.7) + RIGHT * rng.uniform(-0.25, 0.25)).set_opacity(0)
                     for d in [*dust_v.family_members_with_points(), *gold_dust.family_members_with_points()]]
            self.play(*drift, rate.animate.set_value(0), run_time=0.8)
            self.remove(dust_v, gold_dust)
            dial.tracker.clear_updaters()
            self.remove(dial.tracker)
            dial.freeze()
            self.remove(rate)
            self.play(ring(dial))
            vo.wait_until("Select your instance")
            self.play(FadeIn(yt, shift=RIGHT * 0.1), run_time=0.4)
            self.play(pulse(yt), run_time=0.6)
            vo.wait_until("click Delete")
            self.play(Indicate(confirm, color=S.WHITE, scale_factor=1.2), run_time=0.6)
            # the click: the dialog closes; the row is still listed until the deletion finishes
            self.play(FadeOut(VGroup(dialog, d_default, dim), scale=0.96), Restore(ill), run_time=0.25)
            vo.wait_until("until it's gone")
            self.play(FadeOut(row, shift=LEFT * 0.4), run_time=0.5)           # gone from the list
            self.play(pulse(yt), run_time=0.6)

        # ========================================================== 3 · check two pages (+ gcloud)
        items = []
        for name in ("VM instances", "Disks"):
            sq = RoundedRectangle(width=0.46, height=0.46, corner_radius=0.07, stroke_color=S.GREY,
                                  stroke_width=2.5).set_fill(TERM_BG, 1)
            t = label(f"{name}: empty", 34, INK)
            t.next_to(sq, RIGHT, buff=0.32)
            tk = check_mark(0.42, S.GREEN, stroke=6)
            it = VGroup(sq, t)
            it.sq, it.text, it.tick, it.empty = sq, t, tk, words(t, "empty")
            items.append(it)
        rows = VGroup(*items).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        c_frame = box(rows.width + 1.4, rows.height + 0.9, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
        rows.move_to(c_frame)
        check = VGroup(c_frame, rows).move_to([0, 1.05, 0])

        t = term(prompt="$", rows=3, title="your laptop")
        t.shift(np.array([0 - t.box.get_center()[0], TERM_BOTTOM - t.box.get_bottom()[1], 0]))
        opt = tag("optional · needs the gcloud CLI on your laptop", S.GREY)
        opt.next_to(t.box, UP, buff=0.14).align_to(t.box, RIGHT).shift(LEFT * 0.2)

        # the (now empty) list's own heading "VM instances" becomes the first checklist line
        vm_words = words(items[0].text, "VM instances")
        check_rest = VGroup(c_frame, items[0].sq,
                            *[g for g in items[0].text.submobjects if g not in vm_words.submobjects],
                            items[1])

        with self.voiceover(SAY[3]) as vo:
            v_rest = VGroup(V.server, V.hyp, *V.slices[1:], *V.os[1:], *V.disks[1:], V.storage)
            # z-order: the heading stays above the fading browser and above the arriving card
            # (play() would otherwise add the new groups on top of it)
            clear = VGroup(br, ill, heading[:2], page[1:-1], yt, v_rest, dial, cost)
            self.remove(heading[2])
            self.add(clear, heading[2])
            self.play(FadeOut(clear), run_time=0.45)
            self.add(check_rest)
            self.bring_to_front(heading[2])
            self.play(ReplacementTransform(heading[2], vm_words), FadeIn(check_rest, shift=UP * 0.1), run_time=0.6)
            self.remove(vm_words, check_rest)
            self.add(check)
            for it, phrase in zip(items, ("VM instances", "and Disks")):
                vo.wait_until(phrase)
                it.tick.move_to(it.sq).shift(UP * 0.03 + RIGHT * 0.03)
                self.play(Create(it.tick), it.sq.animate.set_stroke(S.GREEN), run_time=0.45)
                self.remove(it.tick)
                it.add(it.tick)
            vo.wait_until("should both be empty")
            self.play(*[it.empty.animate.set_color(S.GREEN) for it in items], run_time=0.5)

            vo.wait_until("With the gcloud tool")
            cap_x, suffix = caption_extra(tr)
            self.play(FadeIn(t, shift=UP * 0.3), FadeIn(suffix, shift=LEFT * 0.1), run_time=0.6)
            swap_caption(self, tr, cap_x, suffix)
            self.play(FadeIn(opt, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("two extra commands")
            self.play(pulse(opt, 1.08), run_time=0.7)
            vo.wait_until("gcloud compute instances list")
            l1 = t.type(self, LIST_VMS, type_time=1.1)
            self.play(Indicate(items[0].text, color=S.WHITE, scale_factor=1.06), run_time=0.6)
            vo.wait_until("and gcloud compute disks list")
            l2 = t.type(self, LIST_DISKS, type_time=1.0)
            self.play(Indicate(items[1].text, color=S.WHITE, scale_factor=1.06), run_time=0.6)
            vo.wait_until("Neither is in the README")
            bx = max(l1.get_right()[0], l2.get_right()[0]) + 0.45
            br_x = bracket(l1.strut.get_top()[1] - 0.02, l2.strut.get_bottom()[1] + 0.02, bx, S.GREY)
            xt = tag("extra · not in the README", S.GREY).next_to(br_x, RIGHT, buff=0.2)
            self.play(Create(br_x), FadeIn(xt, shift=LEFT * 0.1), run_time=0.5)
            self.play(pulse(xt, 1.1), run_time=0.6)

        # ========================================================== 4 · part 1 in one line; part 2
        vm = box(2.0, 1.0, CLOUD, fill_opacity=0.15, radius=0.08)
        vm_os = layer_bar("Debian 12", 2.0, 0.42, CLOUD, size=22, fill_opacity=0.3).next_to(vm, UP, buff=0)
        vm_t = mono("ac215-l01", 24, CLOUD).move_to(vm)
        vm_g = VGroup(vm, vm_os, vm_t)
        jar_row = VGroup(*jars(12, SYSTEM, 0.44)).arrange(RIGHT, buff=0.035)
        board = Line(LEFT * (jar_row.width / 2 + 0.15), RIGHT * (jar_row.width / 2 + 0.15), color=SYSTEM,
                     stroke_width=6)
        jar_row.next_to(board, UP, buff=0.04)
        shelf_t = mono("/usr/local/… (pip's)", 24, SYSTEM).next_to(board, DOWN, buff=0.16)
        shelf = VGroup(board, jar_row, shelf_t)
        shared = tag("shared with the whole OS", ERR)
        strip = VGroup(vm_g, shelf, shared).arrange(RIGHT, buff=0.7)
        assert strip.width < 12.9, strip.width
        strip.move_to([0, 0.35, 0])
        vm_g.shift(UP * (board.get_y() + 0.3 - vm.get_y()))
        shared.shift(UP * (board.get_y() + 0.3 - shared.get_y()))
        a1 = Arrow(vm.get_right(), [board.get_left()[0], vm.get_y(), 0], buff=0.12, color=S.GREY,
                   stroke_width=3, max_tip_length_to_length_ratio=0.25)
        a2 = Arrow([board.get_right()[0], shared.get_y(), 0], shared.get_left(), buff=0.12, color=ERR,
                   stroke_width=3, max_tip_length_to_length_ratio=0.25)

        venv = box(1.7, 1.25, VENV, fill_opacity=0.12, radius=0.12, stroke=3)
        v_jars = VGroup(*jars(3, VENV, 0.42)).arrange(RIGHT, buff=0.12).move_to(venv).shift(DOWN * 0.17)
        v_name = mono(".venv", 22, VENV).next_to(v_jars, UP, buff=0.12)
        venv_g = VGroup(venv, v_jars, v_name)
        p2 = label("Part 2", 28, S.GREY)
        p2_t = label("the same app, on a fresh VM, the clean way", 36, INK,
                     t2c={"fresh VM": CLOUD, "the clean way": VENV})
        txt = VGroup(p2, p2_t).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        inner = VGroup(venv_g, txt).arrange(RIGHT, buff=0.55)
        p_frame = box(inner.width + 0.9, inner.height + 0.7, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
        inner.move_to(p_frame)
        part2 = VGroup(p_frame, inner).move_to([0, -1.35, 0])
        clean = words(p2_t, "the clean way")

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(check, t, opt, br_x, xt, tr)), FadeIn(vm_g, shift=RIGHT * 0.2), run_time=0.6)
            self.play(GrowArrow(a1), FadeIn(board), FadeIn(shelf_t), run_time=0.45)
            self.play(LaggedStart(*[FadeIn(j, shift=DOWN * 0.25) for j in jar_row], lag_ratio=0.12),
                      run_time=0.9)
            vo.wait_until("the system Python")
            self.play(ShowPassingFlash(board.copy().set_stroke(S.WHITE, 9), time_width=0.6),
                      Indicate(jar_row, color=SYSTEM, scale_factor=1.06), run_time=0.9)
            vo.wait_until("for every program")
            self.play(GrowArrow(a2), FadeIn(shared, shift=LEFT * 0.15), run_time=0.6)
            self.play(pulse(shared, 1.1), run_time=0.6)
            vo.wait_until("In part 2")
            recap = VGroup(vm_g, a1, shelf, a2, shared)
            self.play(recap.animate.shift(UP * 1.45).fade(0.6), FadeIn(part2, shift=UP * 0.3), run_time=0.9)
            vo.wait_until("on a fresh VM")
            self.play(Indicate(words(p2_t, "fresh VM"), color=CLOUD, scale_factor=1.04), run_time=0.7)
            vo.wait_until("the clean way")
            self.play(Indicate(clean, color=VENV, scale_factor=1.04), Indicate(venv_g, color=VENV, scale_factor=1.08),
                      run_time=0.8)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.wait(0.2)
