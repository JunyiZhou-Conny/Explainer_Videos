"""S15 · Tear down, recap, and what's next (README section B step 12; the end of part 2).

Beats (script.md "## S15", one voiceover block each):
 0  TRACKER B12. S07's schematic console (GREY browser, tag illustration) with S03's V1 picture and
    the GOLD dial sweeping: the `ac215-l01` row ticks, Delete lights, the confirm dialog "Delete
    ac215-l01? / Its boot disk is deleted with it" (tag illustration; YELLOW bar as it's said, the
    slice->disk link flashes); Delete: the dialog closes and the row leaves the list (as in S07),
    the slice and its disk dissolve and the needle stops where it is. The console makes way for
    the checklist "VM instances: empty" / "Disks: empty" (GREEN ticks as each is named), the
    frozen dial beside it; ▶ your turn on "Pause".
 1  V7. A BLUE box "VM" containing a GREEN toolbox "venv" (S08's look), centred. Labels appear as
    they are said: VM "a whole machine: wreck it, delete it"; venv "one project's Python
    packages". On "away from that machine's Python" the venv moves aside as the ORANGE system
    Python (a shelf of jars) comes in, and a solid GREY wall rises between them (GREY dashed is
    kept for the future container). "between the two": a GREY dashed box "container · L2" fades
    in between the VM and the venv.
 2  The dashed box turns solid (GREY, tag "L2"); the picture compacts into a tall column at left
    (the venv dims: not built yet) and CODE(Dockerfile.txt: 21-29) slides in at right. "copy the
    code": line 22 YELLOW, a `cli.py` chip flies into the container; "run the same uv sync": line
    24 GREEN, the venv lights up and its jars drop in; "start in a shell with the venv activated":
    line 29 GREEN, an `(app) $` shell appears in the container; "baked into an image": the
    container and the panel flash together.
 3  CODE(Dockerfile.txt: 2) and CODE(pyproject.toml: 6) side by side, a YELLOW "?" between them,
    and S10's number line in miniature below: a GREY dot drops from "3.12" in the FROM line onto
    3.12; the GREEN glow grows from 3.13 as `>=3.13` is named; the dot turns RED just outside the
    glow. "You already know": a PURPLE `uv sync` chip under the "?"; "what uv will do": a dashed
    PURPLE arrow from it into the glow, and the "?" pulses (a hint, not the answer).
 4  "Test yourself" (YELLOW underline). Q1 appears (28 pt, YELLOW badge); beside it a thumbnail of
    S05's shelves: pip's ORANGE jars land on the /usr/local shelf, above apt's.
 5  Q1 shrinks to 22 pt GREY, Q2 appears below (thumbnail: the three-part venv card, badges turn
    GREEN one by one); then Q2 shrinks and Q3 appears (thumbnail: PATH doors, the GREEN
    `.venv/bin` door slides in at the front).
 6  Q4 (thumbnail: the two wishes, art and googletrans; on "became 11 packages" the tree grows
    level by level to 11 nodes, the real `uv tree` shape; on "which file" it rolls into the GREEN
    uv.lock scroll); Q5 (thumbnail: the number line's glow shrinks to the 3.13 segment).
 7  The thumbnail goes; the questions reflow to full width and shrink to the top; footer cards
    "Answers: exercises.md" and "Study guide + every command" / the MLOps_Learning link
    (MLOps_Learning underlined YELLOW as it is said); on "Next time: containers" a GREY dashed chip
    "next: containers · L2". Everything fades to an empty frame (end of part 2).

The console, V1 and dialog vocabulary is copied from s07_delete.py (same constants, same glyphs) so
the step looks exactly like S07's; nothing here is terminal output. Code panels quote
assets/source/Dockerfile.txt and pyproject.toml through excerpt() with their real line numbers.
"""

import re
from functools import lru_cache

import numpy as np
from manim import *

from explainer import style as S
from explainer.devops import (MONO, PANEL, TERM_BG, box, browser_window, check_mark, chip,
                              code_panel, code_span, file_glyph, folder_glyph, label, layer_bar,
                              line_bar, mono, server, step_badge, tag)
from explainer.scene import VoiceScene

from common import (CLOUD, COST, ERR, INK, LOOKUP, NARRATION, SYSTEM, TURN, UV, VENV, CostDial,
                    VersionLine, excerpt, illustration_tag, jar, jars, tracker_b, your_turn)

SAY = NARRATION["S15"]

# ------------------------------------------------------------------ real sources
DOCKER_21_29 = excerpt("Dockerfile.txt", 21, 29)
DOCKER_2 = excerpt("Dockerfile.txt", 2, 2)
TOML_6 = excerpt("pyproject.toml", 6, 6)
D_LINES = DOCKER_21_29.split("\n")
assert D_LINES[1] == "COPY . ./" and D_LINES[3] == "RUN uv sync", D_LINES
assert D_LINES[8] == 'CMD ["-c", "source .venv/bin/activate && exec bash"]', D_LINES[8]
assert DOCKER_2 == "FROM python:3.12-slim-bookworm", DOCKER_2
assert TOML_6 == 'requires-python = ">=3.13"', TOML_6

URL = "console.cloud.google.com/compute/instances"
NBSP = "\u00a0"                               # keeps a code span such as `sudo pip3` on one line
GUIDE = "github.com/JunyiZhou-Conny/MLOps_Learning · guides/L01-vms-venvs.md"

# the five questions (script.md S15, on screen); spans in the code font
QUESTIONS = [
    ("What does --break-system-packages break, and where did sudo pip3 put the files?",
     ["--break-system-packages", "sudo pip3"]),
    ("Name the three parts of a venv.", []),
    ("What does activation change? Name two ways to run the app without it.", []),
    ("pyproject.toml lists 2 dependencies. Why were 11 packages installed, and which file makes "
     "everyone get the same ones?", ["pyproject.toml"]),
    ("Is >=3.13 a pin? What would make the Python version deterministic?", [">=3.13"]),
]

# ------------------------------------------------------------------ layout (beat 0 = S07's)
TRACK_LEFT, TRACK_TOP = -6.5, 3.5
BR_LEFT, BR_TOP, BR_W, BR_H = -6.55, 2.75, 8.7, 5.3
C_LEFT = BR_LEFT + 0.35
LIST_RIGHT = 1.75
D_LEFT, D_RIGHT = C_LEFT + 0.55, 1.9
X0, WIDTHS, GAP = 2.75, [2.4, 0.36, 0.36, 0.36], 0.1
SLICE = (-0.45, 0.95)
OS_H, HYP_H, SERVER_H = 0.4, 0.36, 0.7
DISK_Y, DISK_W, DISK_H, DISK_PITCH = -2.3, 0.44, 0.38, 0.56
DIAL_C, DIAL_R = np.array([2.95, 2.3, 0]), 0.46
RUN = 1 / 7                                   # dial turns per second while the VM exists

# questions (beats 4-7)
Q_X = -5.72                                   # left edge of the question text
Q_W = 7.0                                     # wrap width beside a thumbnail
Q_TOP = 2.35
Q_BIG, Q_SMALL, Q_FINAL = 26, 22, 21          # current question, earlier ones, the final list
THUMB_X, THUMB_W = 4.15, 4.7                  # thumbnail column: x in [1.8, 6.5]


# ------------------------------------------------------------------ S07's console + V1 glyphs
def wide_server(w: float, h: float, color=S.GREY) -> VGroup:
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
    e = w * 0.3
    rect = Rectangle(width=w, height=h)
    top = Ellipse(width=w, height=e).move_to(rect.get_top())
    bot = Ellipse(width=w, height=e).move_to(rect.get_bottom())
    body = Union(rect, top, bot).set_stroke(color, 2.5).set_fill(color, 0.22)
    lid = Ellipse(width=w, height=e, stroke_color=color, stroke_width=2.5).set_fill(color, 0.45)
    lid.move_to(rect.get_top())
    return VGroup(body, lid)


def icon_chip(icon: VMobject, s: str, color=S.GREY, size: float = 24) -> VGroup:
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
    sq = RoundedRectangle(width=s, height=s, corner_radius=0.04, stroke_color=S.GREY,
                          stroke_width=2).set_fill(TERM_BG, 1)
    tick = check_mark(s * 0.62, INK, stroke=3.5).move_to(sq).shift(DOWN * s * 0.02)
    g = VGroup(sq)
    g.sq, g.tick = sq, tick
    return g


def build_v1() -> VGroup:
    """S03's V1 (as in S07): server, hypervisor, four slices (ours BLUE and wide), our OS layer,
    name, CPU/memory block, three BLUE disks with ours linked and labelled."""
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
    v.add(v.server, v.hyp, v.slices, v.os, v.name, v.block, v.disks, v.link, v.disk_lab, v.storage)
    return v


def dust(mob, color, rng, n: int, r: float = 0.03) -> VGroup:
    """Small dots scattered over mob's area (what a dissolving thing turns into)."""
    lo, hi = mob.get_corner(DL), mob.get_corner(UR)
    pts = np.c_[rng.uniform(lo[0], hi[0], n), rng.uniform(lo[1], hi[1], n), np.zeros(n)]
    return VGroup(*[Dot(p, radius=r, color=color) for p in pts])


def place_tracker(tr):
    tr.shift(np.array([TRACK_LEFT - tr.get_left()[0], TRACK_TOP - tr.get_top()[1], 0]))
    return tr


def words(t: Text, sub: str) -> VGroup:
    """The glyphs of `sub` inside a Text (spaces have no glyphs)."""
    s = "".join(t.text.split())
    i = s.find("".join(sub.split()))
    assert i >= 0, (sub, t.text)
    return VGroup(*t.submobjects[i:i + len("".join(sub.split()))])


def pulse(m, factor: float = 1.15):
    """A tag's pulse: grow and settle back (Indicate would flood an opaque tag with its colour)."""
    return m.animate(rate_func=there_and_back).scale(factor)


def under(g, color, stroke: float = 3.5, dy: float = 0.07) -> Line:
    y = g.get_bottom()[1] - dy
    return Line([g.get_left()[0] - 0.03, y, 0], [g.get_right()[0] + 0.03, y, 0], color=color,
                stroke_width=stroke)


def dashed_arrow(a, b, angle: float, color: str) -> VGroup:
    """A dashed curved arrow from a to b (a hint, not a fact)."""
    arc = ArcBetweenPoints(a, b, angle=angle)
    d = DashedVMobject(arc, num_dashes=14, dashed_ratio=0.55).set_stroke(color, 3)
    end, prev = arc.point_from_proportion(1), arc.point_from_proportion(0.94)
    v = end - prev
    tip = Triangle(stroke_width=0).set_fill(color, 1).scale(0.11)
    tip.rotate(np.arctan2(v[1], v[0]) - PI / 2).move_to(end - v / np.linalg.norm(v) * 0.06)
    return VGroup(d, tip)


def flash_frame(m, color: str, width: float = 7, run_time: float = 0.9):
    """A bright pass along a frame's outline."""
    c = m.copy().set_stroke(color, width).set_fill(opacity=0)
    return ShowPassingFlash(c, time_width=0.5, run_time=run_time)


# ------------------------------------------------------------------ V7 pieces
def toolbox(w: float, h: float, color: str, fill: float = 0.1, stroke: float = 3) -> VGroup:
    """S08's toolbox: a rounded body with a handle on top. .body .handle"""
    body = box(w, h, color, fill_opacity=fill, radius=0.12, stroke=stroke)
    hw, hh = min(1.1, w * 0.3), 0.24
    handle = VMobject(stroke_color=color, stroke_width=4)
    handle.set_points_as_corners([[-hw / 2, 0, 0], [-hw / 2, hh, 0], [hw / 2, hh, 0], [hw / 2, 0, 0]])
    handle.next_to(body, UP, buff=0)
    g = VGroup(body, handle)
    g.body, g.handle = body, handle
    return g


def venv_box(w: float, h: float, title_size: float, n_jars: int, jar_h: float) -> VGroup:
    """The GREEN venv: a toolbox titled "venv" with a row of GREEN jars. .tb .title .jars"""
    tb = toolbox(w, h, VENV)
    t = label("venv", title_size, VENV).move_to(tb.body.get_top() + DOWN * (title_size / 60 + 0.12))
    js = VGroup(*jars(n_jars, VENV, jar_h)).arrange(RIGHT, buff=jar_h * 0.35)
    js.move_to(tb.body.get_bottom() + UP * (jar_h / 2 + 0.2))
    g = VGroup(tb, t, js)
    g.tb, g.title, g.jars = tb, t, js
    return g


def container_box(w: float, h: float, dashed: bool, size: float = 24) -> VGroup:
    """The GREY container (L2): dashed while it is a future thing, solid once it is named.
    .frame .head"""
    frame = box(w, h, S.GREY, fill_opacity=0 if dashed else 0.06, dashed=dashed, stroke=2.5)
    if dashed:
        head = label("container · L2", size, S.GREY)
    else:
        head = VGroup(label("container", size, S.GREY), tag("L2", S.GREY, size=20)).arrange(RIGHT, buff=0.2)
    head.move_to(frame.get_top() + DOWN * 0.38)
    g = VGroup(frame, head)
    g.frame, g.head = frame, head
    return g


# ------------------------------------------------------------------ question text
def text_line(s: str, size: float, color: str, code=()) -> VGroup:
    """One line of house-font text whose code spans use the code font, with a FIXED vertical
    extent (built with a leading '|' that is dropped, as mono_line does). .glyphs .strut"""
    t2f = {c: MONO for c in code if c in s}
    t = S.text("|" + s, size, color, t2f=t2f)
    pipe = t.submobjects[0]
    strut = Rectangle(width=max(0.01, t.width), height=pipe.height, stroke_width=0, fill_opacity=0)
    strut.move_to(pipe.get_center()).align_to(t, LEFT)
    gl = VGroup(*t.submobjects[1:])
    strut.stretch_to_fit_width(max(0.01, gl.width)).align_to(gl, LEFT)
    g = VGroup(strut, *gl.submobjects)
    g.glyphs, g.strut = VGroup(*gl.submobjects), strut
    return g


@lru_cache(maxsize=None)
def _line_width(s: str, size: float, code: tuple) -> float:
    return text_line(s, size, INK, code).glyphs.width


def _layout(s: str, size: float, width: float, code: tuple) -> list:
    """Line breaks with the fewest lines and, among those, the most even fill (least squared
    slack, last line included: no orphan word)."""
    words_ = s.split(" ")
    ws = [_line_width(w.replace(NBSP, " "), size, code) for w in words_]
    sp = _line_width("x x", size, ()) - _line_width("xx", size, ())
    n = len(words_)
    best, nxt = [0.0] * (n + 1), [n] * (n + 1)
    for i in range(n - 1, -1, -1):
        best[i], acc = float("inf"), -sp
        for j in range(i + 1, n + 1):
            acc += ws[j - 1] + sp
            if acc > width and j > i + 1:
                break
            c = (width - acc) ** 2 + 1000.0 + best[j] if acc <= width else 1e9 + best[j]
            if c < best[i]:
                best[i], nxt[i] = c, j
    lines, i = [], 0
    while i < n:
        lines.append(" ".join(words_[i:nxt[i]]))
        i = nxt[i]
    return lines


def wrap_lines(s: str, size: float, width: float, code=()) -> list:
    """Line breaks for s: one sentence per line group when that costs no extra line, otherwise a
    balanced wrap. A code span is never split."""
    code = tuple(code)
    for c in code:
        s = s.replace(c, c.replace(" ", NBSP))
    whole = _layout(s, size, width, code)
    sentences = re.split(r"(?<=[.?]) (?=[A-Z0-9])", s)
    if len(sentences) > 1:
        per = [ln for sen in sentences for ln in _layout(sen, size, width, code)]
        if len(per) <= len(whole):
            whole = per
    return [ln.replace(NBSP, " ") for ln in whole]


def wrapped(s: str, size: float, color: str, width: float, code=()) -> VGroup:
    """Wrapped house-font text at `width` (see wrap_lines). .lines .glyphs"""
    strs = wrap_lines(s, size, width, code)
    rows = [text_line(ln, size, color, code) for ln in strs]
    pitch = rows[0].strut.height * 1.22
    for k, r in enumerate(rows):
        r.shift(np.array([-r.strut.get_left()[0], -k * pitch - r.strut.get_top()[1], 0]))
    g = VGroup(*rows)
    g.lines, g.strs = rows, strs
    g.glyphs = VGroup(*[gl for r in rows for gl in r.glyphs])
    return g


def question(i: int, size: float, color: str, badge_color: str, width: float) -> VGroup:
    """Question i (1-based): a numbered badge and the wrapped text, the text's top-left at the
    origin. .badge .text .flat (badge + glyphs, for glyph-to-glyph transforms)"""
    s, code = QUESTIONS[i - 1]
    txt = wrapped(s, size, color, width, code)
    r = 0.24 if size >= Q_BIG else 0.19
    b = step_badge(i, badge_color, size=22 if size >= Q_BIG else 20, radius=r)
    first = txt.lines[0].strut
    b.move_to([-0.2 - r, first.get_center()[1], 0])
    g = VGroup(b, txt)
    g.badge, g.text = b, txt
    g.flat = VGroup(b, *txt.glyphs)
    return g


def q_span(q: VGroup, sub: str) -> VGroup:
    """The glyphs of `sub` in question q's text (a span never crosses a line break)."""
    key = "".join(sub.split())
    for r, s in zip(q.text.lines, q.text.strs):
        i = "".join(s.split()).find(key)
        if i >= 0:
            return VGroup(*r.glyphs[i:i + len(key)])
    raise AssertionError((sub, q.text.strs))


def thumb_frame(content: VGroup, h: float | None = None) -> VGroup:
    """A small dark card holding a thumbnail. .frame .content"""
    h = h or content.height + 0.55
    frame = box(THUMB_W, h, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
    content.move_to(frame)
    g = VGroup(frame, content)
    g.frame, g.content = frame, content
    return g


def thumb_shelves() -> VGroup:
    """Q1: S05's shelves, short labels under the boards; pip's 12 jars (.drop) land above apt's."""
    w = 4.3
    out = VGroup()

    def shelf(lbl):
        board = Line(LEFT * w / 2, RIGHT * w / 2, color=SYSTEM, stroke_width=5)
        t = mono(lbl, 20, SYSTEM).next_to(board, DOWN, buff=0.1).align_to(board, LEFT)
        return VGroup(board, t)

    pip_s, apt_s = shelf("/usr/local/… (pip's)"), shelf("/usr/lib/python3/… (apt's)")
    VGroup(pip_s, apt_s).arrange(DOWN, buff=0.62, aligned_edge=LEFT)
    apt_j = VGroup(*jars(4, SYSTEM, 0.34)).arrange(RIGHT, buff=0.05)
    apt_j.next_to(apt_s[0], UP, buff=0.03).align_to(apt_s[0], RIGHT).shift(LEFT * 0.08)
    pip_j = VGroup(*jars(12, SYSTEM, 0.34)).arrange(RIGHT, buff=0.05)
    pip_j.next_to(pip_s[0], UP, buff=0.03).align_to(pip_s[0], RIGHT).shift(LEFT * 0.08)
    out.add(pip_s, apt_s, apt_j)
    g = thumb_frame(VGroup(out, pip_j.copy().set_opacity(0)))
    g.drop = pip_j.move_to(g.content[1])
    g.extras = [g.drop]
    return g


def thumb_parts() -> VGroup:
    """Q2: the three-part venv card; .lit = GREEN badges that replace the GREY ones."""
    head = VGroup(folder_glyph(0.26, VENV), mono(".venv/", 22, VENV)).arrange(RIGHT, buff=0.15)
    rows, lit = VGroup(), []
    for n, p in enumerate(["bin/python", "lib/…/site-packages/", "pyvenv.cfg"], start=1):
        rows.add(VGroup(step_badge(n, S.GREY_DARK, size=20, radius=0.17), mono(p, 20, INK))
                 .arrange(RIGHT, buff=0.18))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    body = VGroup(head, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
    rows.shift(RIGHT * 0.3)
    g = thumb_frame(body)
    for n, r in enumerate(rows, start=1):
        lit.append(step_badge(n, VENV, size=20, radius=0.17).move_to(r[0]))
    g.rows, g.lit, g.extras = rows, lit, lit
    return g


def thumb_doors() -> VGroup:
    """Q3: PATH as mini doors; .new = the GREEN .venv/bin door (+ label) to slide in at the front."""
    def door(color, w=0.46):
        f = RoundedRectangle(width=w, height=0.76, corner_radius=0.04, stroke_color=color,
                             stroke_width=2.5).set_fill(color, 0.15 if color == S.GREY else 0.35)
        k = Dot(radius=0.03, color=color).move_to(f.get_right() + LEFT * 0.08)
        return VGroup(f, k)

    doors = VGroup(door(UV), door(S.GREY), door(S.GREY), door(S.GREY), door(S.GREY, 0.26))
    doors.arrange(RIGHT, buff=0.13, aligned_edge=DOWN)
    path = mono("PATH", 22, LOOKUP)
    row = VGroup(path, doors).arrange(RIGHT, buff=0.3)
    new = door(VENV)
    new_lab = mono(".venv/bin", 20, VENV)
    slot_w = new.width + 0.13
    # the content reserves room for the new door (and its label under it)
    room = Rectangle(width=row.width + slot_w, height=row.height + 0.6, stroke_width=0, fill_opacity=0)
    VGroup(row).move_to(room).align_to(room, LEFT).align_to(room, UP)
    g = thumb_frame(VGroup(room, row))
    new.move_to(doors[0])
    new_lab.next_to(doors[0], DOWN, buff=0.14)
    g.doors, g.new, g.new_lab, g.slot = doors, new, new_lab, slot_w
    g.extras = [new, new_lab]
    return g


def lock_scroll(w: float = 1.0, h: float = 1.2, name_size: float = 22) -> VGroup:
    """S11's GREEN uv.lock scroll (the receipt)."""
    paper = Rectangle(width=w, height=h, stroke_color=VENV, stroke_width=3).set_fill(VENV, 0.12)
    rh = max(0.07, h * 0.12)
    rods = VGroup(*[RoundedRectangle(width=w * 1.23, height=rh, corner_radius=rh / 2, stroke_color=VENV,
                                     stroke_width=2.5).set_fill(VENV, 0.55).move_to(p)
                    for p in (paper.get_top(), paper.get_bottom())])
    lines = VGroup(*[Line(LEFT * w * 0.32, RIGHT * w * (0.32 if k % 2 == 0 else 0.1), color=VENV,
                          stroke_width=2) for k in range(5)])
    lines.arrange(DOWN, buff=h * 0.11, aligned_edge=LEFT).move_to(paper)
    name = mono("uv.lock", name_size, VENV).next_to(rods[1], DOWN, buff=0.12)
    g = VGroup(paper, lines, rods, name)
    g.name = name
    return g


def thumb_tree() -> VGroup:
    """Q4: two wishes grow into 11 packages; .tree rolls into .scroll."""
    def node(r=0.09):
        return Dot(radius=r, color=VENV)

    art = chip("art", VENV, size=20, font=MONO)
    gt = chip("googletrans", VENV, size=20, font=MONO)
    top = VGroup(art, gt).arrange(RIGHT, buff=0.35)
    httpx = node().next_to(gt, DOWN, buff=0.38)
    lvl2 = VGroup(*[node() for _ in range(5)]).arrange(RIGHT, buff=0.32).next_to(httpx, DOWN, buff=0.42)
    lvl3 = VGroup(*[node() for _ in range(3)])
    lvl3[0].next_to(lvl2[2], DOWN, buff=0.42)
    lvl3[1].next_to(lvl2[4], DOWN, buff=0.42).shift(LEFT * 0.2)
    lvl3[2].next_to(lvl2[4], DOWN, buff=0.42).shift(RIGHT * 0.2)

    def edge(a, b):
        return Line(a.get_bottom(), b.get_top(), color=S.GREY, stroke_width=2, buff=0.04)

    edges = VGroup(edge(gt, httpx), *[edge(httpx, n) for n in lvl2], edge(lvl2[2], lvl3[0]),
                   edge(lvl2[4], lvl3[1]), edge(lvl2[4], lvl3[2]))
    tree = VGroup(edges, top, httpx, lvl2, lvl3)
    g = thumb_frame(tree)                 # the card is sized for the whole tree ...
    tree.remove(edges, httpx, lvl2, lvl3)  # ... but holds only the two wishes at first
    # the tree grows level by level (art + googletrans + 9 = 11 packages) ...
    g.levels = [(VGroup(edges[0]), VGroup(httpx)), (VGroup(*edges[1:6]), lvl2), (VGroup(*edges[6:]), lvl3)]
    g.grown = VGroup(edges, httpx, lvl2, lvl3)
    # ... and then rolls up into the uv.lock scroll, centred in the card
    scroll = lock_scroll(1.0, 1.2)
    scroll.move_to(g.frame)
    g.top, g.scroll = top, scroll
    g.extras = [g.grown, scroll]
    return g


def thumb_glow() -> VGroup:
    """Q5: S10's number line in miniature; .seg = the 3.13 segment the glow shrinks to."""
    vl = VersionLine(12, 16, lo=13, width=4.2, size=20)
    vl.remove(vl.band_label)
    # a shorter run-off past 3.16 than S10's, so the line keeps a margin inside the card
    vl.band.stretch_to_fit_width(vl.band.width - 0.15, about_edge=LEFT)
    lab = mono(">=3.13", 20, VENV).next_to(vl.band, UP, buff=0.18).align_to(vl.band, LEFT)
    body = VGroup(vl, lab)
    g = thumb_frame(body, h=body.height + 0.75)
    x13, x14 = vl.point(13)[0], vl.point(14)[0]
    seg = Rectangle(width=(x14 - x13) * 0.75, height=vl.band.height, stroke_width=0).set_fill(VENV, 0.5)
    seg.move_to([x13 + (x14 - x13) * 0.375, vl.band.get_y(), 0])
    seg_lab = mono("3.13", 20, VENV).move_to(lab).align_to(seg, LEFT)
    g.vl, g.lab, g.seg, g.seg_lab = vl, lab, seg, seg_lab
    g.extras = [seg, seg_lab]
    return g


class Recap(VoiceScene):
    # ------------------------------------------------------------- question helpers
    def place_q(self, q: VGroup, top: float) -> VGroup:
        """Put question q's text top-left at (Q_X, top)."""
        t = q.text.lines[0].strut
        q.shift(np.array([Q_X - t.get_left()[0], top - t.get_top()[1], 0]))
        return q

    @staticmethod
    def q_bottom(q: VGroup) -> float:
        return q.text.lines[-1].strut.get_bottom()[1]

    def thumb_at(self, th: VGroup, q: VGroup) -> VGroup:
        """Park a thumbnail in the right column, level with question q (inside the frame)."""
        y = q.text.get_center()[1]
        h = th.frame.height
        y = min(Q_TOP + 0.1 - h / 2, max(-3.45 + h / 2, y))
        d = np.array([THUMB_X, y, 0]) - th.frame.get_center()
        th.shift(d)
        for m in getattr(th, "extras", []):
            m.shift(d)
        return th

    def demote(self, q: VGroup, i: int, top: float, width: float = Q_W, size: float = Q_SMALL):
        """The animation that turns the current question q into its small GREY version at `top`
        (glyph to glyph). Returns (anim, new question)."""
        small = self.place_q(question(i, size, S.GREY, S.GREY, width), top)
        return Transform(q.flat, small.flat), small

    def swap_in(self, q_old, new):
        """After a glyph transform: the scene holds `new`, not the transformed old glyphs (nor the
        old lines' invisible struts)."""
        self.remove(q_old.flat, q_old, *[ln.strut for ln in q_old.text.lines])
        self.add(new)

    def construct(self):
        assert len(SAY) == 8, f"S15 has {len(SAY)} SAY lines; this scene times 8"
        rng = np.random.default_rng(15)

        # ========================================================== 0 · step 12: delete the VM
        tr = place_tracker(tracker_b(11))
        br = browser_window(URL, width=BR_W, height=BR_H)
        br.shift(np.array([BR_LEFT - br.frame.get_left()[0], BR_TOP - br.frame.get_top()[1], 0]))
        ill = illustration_tag()
        ill.move_to(br.frame.get_corner(DR) + np.array([-ill.width / 2 - 0.3, 0, 0]))

        heading = VGroup(label("Compute Engine", 28, INK), label("›", 28, S.GREY),
                         label("VM instances", 28, INK)).arrange(RIGHT, buff=0.2)
        heading.move_to([0, 1.78, 0]).set_x(C_LEFT, LEFT)
        stop_b = icon_chip(stop_icon(), "Stop")
        del_b = icon_chip(trash_icon(), "Delete")
        toolbar = VGroup(stop_b, del_b).arrange(RIGHT, buff=0.3).move_to([0, 1.0, 0]).set_x(C_LEFT, LEFT)
        sep = Line([C_LEFT - 0.1, 0.5, 0], [LIST_RIGHT, 0.5, 0], color=S.GREY_DARK, stroke_width=2)
        X_CB, X_ST, X_NAME, X_ZONE, X_CONN = C_LEFT + 0.2, C_LEFT + 0.62, C_LEFT + 1.7, C_LEFT + 3.75, C_LEFT + 6.5
        Y_HEAD, Y_ROW = 0.12, -0.6
        cb_head = checkbox().move_to([X_CB, Y_HEAD, 0])
        heads = VGroup(*[label(s, 22, S.GREY).move_to([0, Y_HEAD, 0]).set_x(x, LEFT)
                         for s, x in (("Status", X_ST), ("Name", X_NAME), ("Zone", X_ZONE), ("Connect", X_CONN))])
        cb = checkbox().move_to([X_CB, Y_ROW, 0])
        running = check_mark(0.28, S.GREEN).move_to([X_ST + 0.2, Y_ROW, 0])
        r_name = mono("ac215-l01", 22, INK).move_to([0, Y_ROW, 0]).set_x(X_NAME, LEFT)
        r_zone = mono("us-central1-a", 22, S.GREY).move_to([0, Y_ROW, 0]).set_x(X_ZONE, LEFT)
        r_ssh = chip("SSH", CLOUD, size=22).move_to([0, Y_ROW, 0]).set_x(X_CONN, LEFT)
        row_frame = box(LIST_RIGHT - (C_LEFT - 0.1), 0.66, S.GREY, fill_opacity=0.05, radius=0.08)
        row_frame.move_to([(C_LEFT - 0.1 + LIST_RIGHT) / 2, Y_ROW, 0])
        row = VGroup(row_frame, cb, running, r_name, r_zone, r_ssh)
        page = VGroup(heading, toolbar, sep, cb_head, heads, row)

        V = build_v1()
        dial = CostDial(radius=DIAL_R, caption=None).move_to(DIAL_C)
        cost = label("cost", 22, COST).next_to(dial, UP, buff=0.1)
        rate = ValueTracker(RUN)
        dial.tracker.add_updater(lambda m, dt: m.increment_value(dt * rate.get_value()))

        # the confirm dialog (S07's)
        dim = Rectangle(width=BR_W - 0.04, height=BR_H - 0.57, stroke_width=0).set_fill(S.BG, 0.62)
        dim.align_to(br.frame, DOWN).shift(UP * 0.02).set_x(br.frame.get_x())
        d_title = VGroup(label("Delete", 28, INK), mono("ac215-l01", 26, INK), label("?", 28, INK))
        d_title.arrange(RIGHT, buff=0.12)
        d_title[2].next_to(d_title[1], RIGHT, buff=0.05)
        for m in d_title[1:]:
            m.align_to(d_title[0], DOWN)
        d_body = label("Its boot disk is deleted with it", 24, INK)
        d_text = VGroup(d_title, d_body).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        cancel = chip("Cancel", S.GREY, size=22)
        confirm = chip("Delete", CLOUD, size=22)
        buttons = VGroup(cancel, confirm).arrange(RIGHT, buff=0.25)
        d_w = D_RIGHT - D_LEFT
        d_h = d_text.height + buttons.height + 0.95
        d_frame = RoundedRectangle(width=d_w, height=d_h, corner_radius=0.14, stroke_color=S.GREY,
                                   stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
        d_frame.move_to([(D_LEFT + D_RIGHT) / 2, -0.75, 0])
        d_text.move_to(d_frame).align_to(d_frame, UP).align_to(d_frame, LEFT).shift(RIGHT * 0.4 + DOWN * 0.32)
        buttons.align_to(d_frame, RIGHT).align_to(d_frame, DOWN).shift(LEFT * 0.35 + UP * 0.26)
        d_ill = illustration_tag()
        d_ill.move_to(d_frame.get_corner(UR) + np.array([-d_ill.width / 2 - 0.3, 0, 0]))
        dialog = VGroup(d_frame, d_text, buttons, d_ill)
        body_bar = Rectangle(width=d_body.width + 0.16, height=d_body.height + 0.14, stroke_width=0) \
            .set_fill(TURN, 0.2).move_to(d_body)

        gone_v = VGroup(V.ours, V.disks[0], V.link, V.disk_lab)
        dust_v = VGroup(dust(VGroup(V.slices[0], V.os[0]), CLOUD, rng, 46),
                        dust(V.disks[0], CLOUD, rng, 10), dust(V.disk_lab, CLOUD, rng, 10))

        # the checklist (S07's), the frozen dial beside it
        items = []
        for name in ("VM instances", "Disks"):
            sq = RoundedRectangle(width=0.46, height=0.46, corner_radius=0.07, stroke_color=S.GREY,
                                  stroke_width=2.5).set_fill(TERM_BG, 1)
            t = label(f"{name}: empty", 34, INK).next_to(sq, RIGHT, buff=0.32)
            it = VGroup(sq, t)
            it.sq, it.text, it.tick, it.empty = sq, t, check_mark(0.42, S.GREEN, stroke=6), words(t, "empty")
            items.append(it)
        rows_c = VGroup(*items).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        c_frame = box(rows_c.width + 1.4, rows_c.height + 0.9, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
        rows_c.move_to(c_frame)
        check = VGroup(c_frame, rows_c).move_to([-1.35, 0.45, 0])
        yt = your_turn().next_to(check, DOWN, buff=0.35)
        dial_to = np.array([check.get_right()[0] + 1.9, check.get_y() - 0.15, 0])

        # a short establishing shot before the narration: S07's console, the VM still running
        self.play(FadeIn(tr, shift=DOWN * 0.1), FadeIn(br, shift=RIGHT * 0.3), FadeIn(ill), FadeIn(page),
                  FadeIn(V, shift=LEFT * 0.2), FadeIn(dial, scale=0.8), FadeIn(cost), run_time=0.8)
        self.add(dial.tracker)

        with self.voiceover(SAY[0]) as vo:
            self.play(tr.goto(12), run_time=0.5)
            cb.tick.move_to(cb.sq).shift(DOWN * 0.005)
            self.play(cb.sq.animate.set_fill(CLOUD, 1).set_stroke(CLOUD), Create(cb.tick),
                      row_frame.animate.set_stroke(CLOUD).set_fill(CLOUD, 0.1), run_time=0.35)
            self.remove(cb.tick)
            cb.add(cb.tick)
            vo.wait_until("delete the VM")
            self.play(Indicate(del_b, color=S.WHITE, scale_factor=1.15), run_time=0.4)
            self.play(FadeIn(dim), FadeIn(dialog, scale=0.94), run_time=0.4)
            vo.wait_until("with its boot disk")
            self.play(FadeIn(body_bar),
                      ShowPassingFlash(V.link.copy().set_stroke(CLOUD, 7), time_width=0.5),
                      Indicate(V.disks[0], color=CLOUD, scale_factor=1.3), run_time=0.6)
            self.play(Indicate(confirm, color=S.WHITE, scale_factor=1.2), run_time=0.35)
            # Delete (as in S07): the dialog closes, the row leaves the list, the slice and its
            # disk dissolve, and the needle stops where it is (no rewind)
            self.play(FadeOut(VGroup(dialog, body_bar, dim), scale=0.96), FadeOut(row, shift=LEFT * 0.4),
                      FadeOut(gone_v, scale=0.96), FadeIn(dust_v), run_time=0.35)
            page.remove(row)                  # (FadeOut resets it: keep it out of the page's fade)
            drift =[d.animate.shift(UP * rng.uniform(0.25, 0.7) + RIGHT * rng.uniform(-0.25, 0.25)).set_opacity(0)
                     for d in dust_v.family_members_with_points()]
            self.play(*drift, rate.animate.set_value(0), run_time=0.7)
            self.remove(dust_v)
            dial.tracker.clear_updaters()
            self.remove(dial.tracker, rate)
            dial.freeze()
            dial_g = VGroup(dial, cost)
            vo.wait_until("then check")
            v_rest = VGroup(V.server, V.hyp, *V.slices[1:], *V.os[1:], *V.disks[1:], V.storage)
            self.play(FadeOut(VGroup(br, ill, page, v_rest)), dial_g.animate.move_to(dial_to), run_time=0.5)
            self.play(FadeIn(check, shift=UP * 0.15), run_time=0.4)
            for it, phrase in zip(items, ("VM instances", "and Disks")):
                vo.wait_until(phrase)
                it.tick.move_to(it.sq).shift(UP * 0.03 + RIGHT * 0.03)
                self.play(Create(it.tick), it.sq.animate.set_stroke(S.GREEN), run_time=0.4)
                self.remove(it.tick)
                it.add(it.tick)
            vo.wait_until("are both empty")
            self.play(*[it.empty.animate.set_color(S.GREEN) for it in items],
                      Circumscribe(dial.face, Circle, color=COST, buff=0.06), run_time=0.7)
            vo.wait_until("Pause")
            self.play(FadeIn(yt, shift=UP * 0.1), run_time=0.4)
            self.play(pulse(yt), run_time=0.6)
            vo.wait_until("before you forget")
            self.play(pulse(yt), run_time=0.6)

        # ========================================================== 1 · V7: VM ⊃ venv, room between
        vm = box(12.7, 6.5, CLOUD, fill_opacity=0.04)
        vm.move_to([0, -0.15, 0])
        vm_t = label("VM", 34, CLOUD)
        vm_t.move_to(vm.get_corner(UL) + np.array([0.45 + vm_t.width / 2, -0.45, 0]))
        vm_sub = label("a whole machine: wreck it, delete it", 28, INK)
        vm_sub.next_to(vm_t, RIGHT, buff=0.4).align_to(vm_t, DOWN)
        vm_sep = Line(vm.get_corner(UL) + DOWN * 0.9, vm.get_corner(UR) + DOWN * 0.9, color=CLOUD,
                      stroke_width=1.5, stroke_opacity=0.6)
        VM_G = VGroup(vm, vm_sep, vm_t)

        # the venv starts in the middle of the VM and moves away when the system Python arrives
        VEN_X = -2.95
        ven = venv_box(3.8, 1.55, 28, 4, 0.44).move_to([0, -0.7, 0])
        ven_cap = label("one project's Python packages", 26, INK).next_to(ven, DOWN, buff=0.3)
        ctr = container_box(6.0, 4.55, dashed=True).move_to([VEN_X, -0.62, 0])

        board = Line(LEFT * 1.8, RIGHT * 1.8, color=SYSTEM, stroke_width=6).move_to([3.55, -0.75, 0])
        sys_j = VGroup(*jars(5, SYSTEM, 0.44)).arrange(RIGHT, buff=0.12).next_to(board, UP, buff=0.04)
        sys_t = label("the system Python", 26, SYSTEM).next_to(board, DOWN, buff=0.22)
        sys_g = VGroup(board, sys_j, sys_t)
        # a solid wall (GREY dashed is reserved for future things such as the container)
        wall = Line([0.75, 1.35, 0], [0.75, -2.55, 0], color=S.GREY, stroke_width=5)

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(check, yt, dial_g, tr)), run_time=0.6)
            self.play(FadeIn(VM_G, scale=0.96), run_time=0.6)
            self.play(FadeIn(ven, shift=UP * 0.2), run_time=0.5)
            vo.wait_until("a whole machine")
            self.play(FadeIn(vm_sub, shift=RIGHT * 0.2), run_time=0.6)
            vo.wait_until("wreck and delete")
            self.play(flash_frame(vm, CLOUD), Indicate(vm_t, color=CLOUD, scale_factor=1.15), run_time=0.9)
            vo.wait_until("The venv keeps")
            self.play(FadeIn(ven_cap, shift=UP * 0.1), Indicate(ven.jars, color=VENV, scale_factor=1.15),
                      run_time=0.7)
            vo.wait_until("away from")
            self.play(VGroup(ven, ven_cap).animate.shift(RIGHT * (VEN_X - ven.get_x())),
                      FadeIn(sys_g, shift=LEFT * 0.8), run_time=0.9)
            self.play(Create(wall), run_time=0.5)
            vo.wait_until("between the two")
            self.play(FadeIn(ctr, scale=1.06), run_time=0.9)
            vo.wait_until("one more layer")
            outline = RoundedRectangle(width=ctr.frame.width, height=ctr.frame.height,
                                       corner_radius=0.14).move_to(ctr.frame)
            self.play(flash_frame(outline, INK, width=5, run_time=0.9),
                      Indicate(ctr.head, color=INK, scale_factor=1.1), run_time=0.9)

        # ========================================================== 2 · the container: the Dockerfile
        ctr_solid = container_box(6.0, 4.55, dashed=False).move_to(ctr)
        panel = code_panel(DOCKER_21_29, "Dockerfile.txt", first_line=21, language="docker", font_size=20)
        panel.move_to([0, 0.25, 0]).align_to([6.5, 0, 0], RIGHT)
        # the compact picture: a tall column at left (VM ⊃ container ⊃ venv)
        c_left, c_right = -6.5, panel.get_left()[0] - 0.3
        cw = c_right - c_left
        vm2 = box(cw, 6.75, CLOUD, fill_opacity=0.04).move_to([(c_left + c_right) / 2, -0.05, 0])
        vm2_t = label("VM", 28, CLOUD).move_to(vm2.get_corner(UL) + np.array([0.4, -0.36, 0]))
        vm2_t.set_x(vm2.get_left()[0] + 0.3, LEFT)
        vm2_sep = Line(vm2.get_corner(UL) + DOWN * 0.72, vm2.get_corner(UR) + DOWN * 0.72, color=CLOUD,
                       stroke_width=1.5, stroke_opacity=0.6)
        ctr2 = container_box(cw - 0.4, 5.6, dashed=False, size=22)
        ctr2.move_to([vm2.get_x(), vm2_sep.get_y() - 0.12 - 2.8, 0])
        ven2 = venv_box(cw - 1.0, 1.35, 24, 4, 0.36).move_to([vm2.get_x(), ctr2.get_y() - 0.3, 0])
        ven2_dim = ven2.copy()
        ven2_dim.jars.set_opacity(0)
        ven2_dim.tb.body.set_stroke(opacity=0.35).set_fill(opacity=0.02)
        ven2_dim.tb.handle.set_stroke(opacity=0.35)
        ven2_dim.title.set_opacity(0.3)
        code_chip = VGroup(file_glyph(0.3, S.GREY), mono("cli.py", 22, INK)).arrange(RIGHT, buff=0.14)
        code_chip.move_to([vm2.get_x(), ctr2.head.get_y() - 0.95, 0])
        shell = VGroup(mono("(app)", 22, VENV), mono("$", 22, INK)).arrange(RIGHT, buff=0.15)
        sh_box = RoundedRectangle(width=shell.width + 0.45, height=shell.height + 0.3, corner_radius=0.08,
                                  stroke_color=S.GREY_DARK, stroke_width=2).set_fill(TERM_BG, 1)
        shell.move_to(sh_box)
        shell_g = VGroup(sh_box, shell).move_to([vm2.get_x(), ven2.get_bottom()[1] - 1.0, 0])

        code = panel.code
        bar22 = line_bar(code, 1, TURN, 0.22)
        bar24 = line_bar(code, 3, VENV, 0.22)
        bar29 = line_bar(code, 8, VENV, 0.22)

        with self.voiceover(SAY[2]) as vo:
            # "container · L2" -> "container (L2)": the word stays, "· L2" becomes the tag
            w_old, r_old = words(ctr.head, "container"), words(ctr.head, "· L2")
            self.play(FadeOut(ctr.frame), FadeIn(ctr_solid.frame),
                      Transform(w_old, ctr_solid.head[0]), Transform(r_old, ctr_solid.head[1]), run_time=0.7)
            self.remove(ctr, w_old, r_old, ctr_solid.frame)
            self.add(ctr_solid)
            head = ctr_solid.head
            vo.wait_until("next lecture")
            self.play(pulse(head[1], 1.25), run_time=0.6)
            vo.wait_until("Dockerfile already")
            self.play(FadeOut(VGroup(vm_sub, ven_cap, sys_g, wall)), run_time=0.4)
            # the picture compacts first, then the panel slides into the space it freed (no overlap)
            self.play(Transform(vm, vm2), Transform(vm_sep, vm2_sep), Transform(vm_t, vm2_t),
                      Transform(ctr_solid.frame, ctr2.frame), Transform(head, ctr2.head),
                      Transform(ven, ven2_dim), run_time=0.8)
            self.play(FadeIn(panel, shift=LEFT * 0.6), run_time=0.6)
            vo.wait_until("copy the code")
            self.play(FadeIn(bar22), run_time=0.3)
            fly = code_chip.copy().move_to(code_span(code, 1, "COPY . ./")).set_opacity(0)
            self.play(Transform(fly, code_chip), run_time=0.7)
            self.remove(fly)
            self.add(code_chip)
            vo.wait_until("run the same uv sync")
            self.play(FadeOut(bar22), FadeIn(bar24), run_time=0.3)
            lit = ven2.copy()
            drops = lit.jars.copy()
            lit.jars.set_opacity(0)
            self.play(Transform(ven, lit), run_time=0.4)
            for j in drops:
                j.shift(UP * 0.5).set_opacity(0)
            self.play(LaggedStart(*[j.animate.shift(DOWN * 0.5).set_opacity(1) for j in drops], lag_ratio=0.2),
                      run_time=0.8)
            vo.wait_until("and start in a shell")
            self.play(FadeOut(bar24), FadeIn(bar29), run_time=0.3)
            vo.wait_until("with the venv activated")
            self.play(FadeIn(shell_g, shift=UP * 0.2), run_time=0.5)
            self.play(Indicate(shell[0], color=VENV, scale_factor=1.2), run_time=0.6)
            vo.wait_until("Everything you did today")
            self.play(FadeOut(bar29), flash_frame(ctr2.frame.copy(), INK, width=6, run_time=1.0),
                      flash_frame(code.background.copy(), INK, width=6, run_time=1.0), run_time=1.0)

        # ========================================================== 3 · 3.12 image, >=3.13 project
        p2 = code_panel(DOCKER_2, "Dockerfile.txt", first_line=2, language="docker", font_size=22)
        p6 = code_panel(TOML_6, "pyproject.toml", first_line=6, language="toml", font_size=22)
        p2.move_to([0, 1.4, 0]).align_to([-6.45, 0, 0], LEFT)
        p6.move_to([0, 1.4, 0]).align_to([6.45, 0, 0], RIGHT)
        p6.shift(UP * (p2.code.get_top()[1] - p6.code.get_top()[1]))   # the boxes level, not the headers
        mid_x = (p2.get_right()[0] + p6.get_left()[0]) / 2
        qmark = label("?", 56, TURN).move_to([mid_x, p2.code.get_y(), 0])
        v312 = code_span(p2.code, 0, "3.12")
        v313 = code_span(p6.code, 0, ">=3.13")
        # S10's number line in miniature, under the two panels
        vl = VersionLine(10, 16, lo=13, width=8.4, size=22)
        vl.remove(vl.band_label)
        vl.move_to([0.2, -1.55, 0])
        band_full = vl.band.copy()
        vl.band.stretch_to_fit_width(0.01).align_to(band_full, LEFT)
        dot = Dot(v312.get_bottom() + DOWN * 0.2, radius=0.11, color=S.GREY)
        dot_lab = label("3.12 · the image's Python", 24, ERR).next_to(vl.point(12), UP, buff=0.42)
        dot_lab.align_to(vl.point(12) + RIGHT * 0.45, RIGHT)
        # what uv will do (S10): a PURPLE hint from a `uv sync` chip under the "?" into the glow
        uvc = chip("uv sync", UV, size=24, font=MONO).move_to([mid_x, 0.1, 0])
        hint = dashed_arrow(uvc.get_right() + RIGHT * 0.1, vl.point(15, 0.3), -0.7, UV)

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(vm, vm_sep, vm_t, ctr_solid, ven, drops, code_chip,
                                     shell_g, panel)), run_time=0.7)
            self.play(FadeIn(p2, shift=DOWN * 0.15), run_time=0.6)
            self.play(Create(vl.axis), FadeIn(vl.ticks), run_time=0.8)
            vo.wait_until("The Dockerfile starts")
            self.play(Indicate(code_span(p2.code, 0, "FROM"), color=TURN, scale_factor=1.15), run_time=0.8)
            vo.wait_until("a Python 3.12 image")
            ul312 = under(v312, TURN)
            self.play(Create(ul312), v312.animate.set_color(TURN), FadeIn(dot, scale=0.5), run_time=0.5)
            self.play(dot.animate.move_to(vl.point(12)), run_time=0.7, rate_func=rate_functions.ease_in_quad)
            vo.wait_until("but the project wants")
            self.play(FadeIn(p6, shift=DOWN * 0.15), run_time=0.6)
            vo.wait_until("3.13 or newer")
            ul313 = under(v313, VENV)
            self.play(Create(ul313), Transform(vl.band, band_full), run_time=0.8)
            self.play(dot.animate.set_color(ERR), FadeIn(dot_lab, shift=UP * 0.1), FadeIn(qmark, scale=0.6),
                      run_time=0.6)
            vo.wait_until("You already know")
            self.play(FadeIn(uvc, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("what uv will do")
            self.play(Create(hint), run_time=0.8)
            self.play(Indicate(qmark, color=TURN, scale_factor=1.3),
                      vl.band.animate(rate_func=there_and_back).set_fill(opacity=0.6), run_time=0.9)

        # ========================================================== 4 · Test yourself: Q1
        title = label("Test yourself", 40, INK).move_to([0, 3.1, 0]).set_x(-6.35, LEFT)
        t_ul = Line(title.get_corner(DL) + DOWN * 0.1, title.get_corner(DR) + DOWN * 0.1, color=TURN,
                    stroke_width=4)
        q1 = self.place_q(question(1, Q_BIG, INK, TURN, Q_W), Q_TOP)
        th1 = self.thumb_at(thumb_shelves(), q1)

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(p2, p6, qmark, vl, dot, dot_lab, uvc, hint, ul312, ul313)),
                      run_time=0.6)
            self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.6)
            vo.wait_until("five questions")
            self.play(Create(t_ul), run_time=0.6)
            vo.wait_until("One")
            self.play(FadeIn(q1, shift=UP * 0.15), run_time=0.6)
            self.play(FadeIn(th1, shift=LEFT * 0.2), run_time=0.5)
            # the words being read light up in the question (demote() turns them GREY again)
            vo.wait_until("break-system-packages")
            flag = q_span(q1, "--break-system-packages")
            self.play(flag.animate.set_color(TURN), run_time=0.5)
            vo.wait_until("actually break")
            self.play(Indicate(flag, color=TURN, scale_factor=1.06), run_time=0.7)
            vo.wait_until("where did sudo pip3")
            self.play(q_span(q1, "sudo pip3").animate.set_color(TURN), flag.animate.set_color(INK),
                      LaggedStart(*[FadeIn(j, shift=DOWN * 0.5) for j in th1.drop], lag_ratio=0.12),
                      run_time=1.3)
            self.play(Indicate(th1.content[0][0], color=SYSTEM, scale_factor=1.05), run_time=0.6)

        # ========================================================== 5 · Q2, Q3
        def step(q_cur, i_cur, top_cur, th_old, th_new_fn):
            """Demote the current question, bring question i_cur + 1 in below it, swap thumbnails.
            Returns (small, new question, new thumbnail, its top)."""
            anim, small = self.demote(q_cur, i_cur, top_cur)
            top_new = self.q_bottom(small) - 0.32
            q_new = self.place_q(question(i_cur + 1, Q_BIG, INK, TURN, Q_W), top_new)
            th_new = self.thumb_at(th_new_fn(), q_new)
            self.play(anim, FadeOut(th_old, shift=RIGHT * 0.2), run_time=0.6)
            self.swap_in(q_cur, small)
            self.play(FadeIn(q_new, shift=UP * 0.15), FadeIn(th_new, shift=LEFT * 0.2), run_time=0.6)
            return small, q_new, th_new, top_new

        smalls = []
        with self.voiceover(SAY[5]) as vo:
            s1, q2, th2, top2 = step(q1, 1, Q_TOP, VGroup(th1, th1.drop), thumb_parts)
            smalls.append(s1)
            vo.wait_until("three parts")
            for k, b in enumerate(th2.lit):
                self.play(Transform(th2.rows[k][0], b), Indicate(th2.rows[k][1], color=VENV, scale_factor=1.08),
                          run_time=0.45)
            vo.wait_until("Three")
            s2, q3, th3, top3 = step(q2, 2, top2, th2, thumb_doors)
            smalls.append(s2)
            vo.wait_until("activation change")
            self.play(th3.doors.animate.shift(RIGHT * th3.slot), run_time=0.5)
            self.play(FadeIn(th3.new, shift=DOWN * 0.45), run_time=0.5)
            self.play(FadeIn(th3.new_lab, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("two ways")
            self.play(Indicate(th3.new, color=VENV, scale_factor=1.2), run_time=0.7)

        # ========================================================== 6 · Q4, Q5
        with self.voiceover(SAY[6]) as vo:
            s3, q4, th4, top4 = step(q3, 3, top3, VGroup(th3, th3.new, th3.new_lab), thumb_tree)
            smalls.append(s3)
            vo.wait_until("became 11 packages")
            for edges_k, nodes_k in th4.levels:       # 2 wishes -> 11 packages
                self.play(Create(edges_k), FadeIn(nodes_k, scale=0.5), run_time=0.4)
            self.remove(*[m for lv in th4.levels for m in lv])
            self.add(th4.grown)
            vo.wait_until("which file")
            whole = VGroup(th4.top, th4.grown)
            self.play(whole.animate.scale(0.3).move_to(th4.scroll).set_opacity(0),
                      FadeIn(th4.scroll, scale=0.3), run_time=1.1)
            self.play(Indicate(th4.scroll, color=VENV, scale_factor=1.15), run_time=0.6)
            vo.wait_until("Five")
            s4, q5, th5, top5 = step(q4, 4, top4, VGroup(th4, th4.grown, th4.scroll), thumb_glow)
            smalls.append(s4)
            vo.wait_until("a pin")
            pin = q_span(q5, ">=3.13")
            self.play(pin.animate.set_color(TURN), Indicate(th5.lab, color=TURN, scale_factor=1.2),
                      run_time=0.7)
            vo.wait_until("what would make")
            self.play(Transform(th5.vl.band, th5.seg), Transform(th5.lab, th5.seg_lab),
                      pin.animate.set_color(INK), run_time=1.0)
            self.play(Indicate(th5.vl.band, color=VENV, scale_factor=1.2), run_time=0.6)

        # ========================================================== 7 · shrink to the top; where next
        title2 = label("Test yourself", 32, INK).move_to([0, 3.25, 0]).set_x(-6.35, LEFT)
        t_ul2 = Line(title2.get_corner(DL) + DOWN * 0.08, title2.get_corner(DR) + DOWN * 0.08, color=TURN,
                     stroke_width=3)
        finals, top = [], title2.get_bottom()[1] - 0.35
        for i in range(1, 6):
            f = self.place_q(question(i, Q_FINAL, S.GREY, S.GREY, 12.15), top)
            finals.append(f)
            top = self.q_bottom(f) - 0.2
        ans = VGroup(label("Answers:", 28, INK), mono("exercises.md", 26, INK)).arrange(RIGHT, buff=0.2)
        ans_box = box(ans.width + 0.7, ans.height + 0.5, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
        ans.move_to(ans_box)
        card1 = VGroup(ans_box, ans)
        g_head = label("Study guide + every command:", 28, INK)
        g_url = mono(GUIDE, 21, INK)
        g_body = VGroup(g_head, g_url).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        g_box = box(g_body.width + 0.7, g_body.height + 0.5, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
        g_body.move_to(g_box)
        card2 = VGroup(g_box, g_body)
        card1.move_to([0, top - 0.35 - card1.height / 2, 0]).set_x(-6.35, LEFT)
        card2.next_to(card1, DOWN, buff=0.3, aligned_edge=LEFT)
        repo = words(g_url, "MLOps_Learning")
        nxt = VGroup(label("next:", 26, S.GREY), label("containers · L2", 26, INK)).arrange(RIGHT, buff=0.15)
        nxt_box = box(nxt.width + 0.6, nxt.height + 0.4, S.GREY, dashed=True)
        nxt.move_to(nxt_box)
        nxt_g = VGroup(nxt_box, nxt).move_to(card1).set_x(6.35, RIGHT)

        with self.voiceover(SAY[7]) as vo:
            anim5, s5 = self.demote(q5, 5, top5)
            self.play(anim5, FadeOut(th5), run_time=0.5)
            self.swap_in(q5, s5)
            smalls.append(s5)
            self.play(Transform(title, title2), Transform(t_ul, t_ul2),
                      *[Transform(s.flat, f.flat) for s, f in zip(smalls, finals)], run_time=1.0)
            for s, f in zip(smalls, finals):
                self.swap_in(s, f)
            vo.wait_until("in the exercises")
            self.play(FadeIn(card1, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("Every command")
            self.play(FadeIn(card2, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("in the MLOps Learning repo")
            self.play(Create(under(repo, TURN)), repo.animate.set_color(TURN), run_time=0.6)
            vo.wait_until("Next time")
            self.play(FadeIn(nxt_g, shift=LEFT * 0.2), run_time=0.6)

        self.wait(0.3)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.9)
        self.wait(0.2)
