"""S16 · Tear down, recap, and what's next (README C7; the end of part 2).

Beats (script.md "## S16", one voiceover block each):
 0  S15 ended on an empty frame. TRACKER C6 · extra, the VM strip (3 rows, `ssh · ac215-l02`) and, above
    it, the BLUE VM `ac215-l02` as S15 left it: the dlops image's seven slabs (TEAL caption
    `dlops/simple-translate`) and its BLUE boot disk; the GOLD dial at the right keeps sweeping (no
    digits) from where S14/S15's badge dial left it (S15_END: it never rewinds). "An extra check":
    the strip types `sudo docker ps -a` (row tag `extra`) -> vm-debian12/11: 2 (squeeze): the header
    only, and the prompt returns. "shows no containers left behind": a YELLOW bar
    on the header row; in the VM, a GREY dashed slot on top of the stack, "no containers". "thanks to
    dash dash rm": a TEAL `--rm` chip beside the slot, GREY "removed at exit"; the chip pulses.
 1  TRACKER C7. The strip goes (the SSH session is over); the VM compacts into the right column (its
    shapes shrink, its 20+ pt labels keep their size) while the dial keeps sweeping above it. The
    schematic console (tag `illustration`, S14's "Compute Engine › VM instances" with the instance row:
    GREEN check, `ac215-l02`, `e2-small`, SSH): the row's box is ticked; "delete the VM": Delete lights,
    the confirm dialog "Delete ac215-l02? / Its boot disk is deleted with it" (as in L1; the console's
    one `illustration` tag covers it); "with its boot disk": a YELLOW bar on that line, the VM's disk
    pulses. Delete: the dialog closes, the row leaves the list, the BLUE VM and its disk dissolve into
    dust and the needle stops where it is. "then check": the console makes way for the checklist
    "VM instances: empty" / "Disks: empty" (GREEN ticks as each is named, "empty" GREEN), the frozen
    dial beside it; "Pause": ▶ your turn.
 2  TRACKER C7 · extra (the commands on screen are not README ones). GREY heading "optional". "Your Docker
    Hub repository": a BLUE shelf glyph and the GREY chip "Docker Hub repository: public until you
    delete it or make it private"; "stays public": "public" underlined YELLOW; "or make it private": a
    GREY padlock lands on the shelf, "private" underlined. "And to reclaim the space": a GREY laptop
    whose screen holds a TEAL bar (the images), and the tag `Lecture 2 · slide 73` (top right, until
    the chores leave at beat 3's start); "run docker system prune dash a": the GREY mono chip
    `docker system prune -a` with "frees the laptop's disk · said, not typed here"; the TEAL bar
    shrinks to a sliver. Then, smaller and unspoken: `docker buildx rm multi-arch` "if you ran the push
    script" and `docker logout` "optional", held 3 s on a pause so they can be read.
 3  V1 closing picture. The tracker goes. "Lecture 1": L1's nest (BLUE VM "VM" holding a GREEN "venv"),
    tag "L1". "Today a container slid in between": the dashed GREY "container · L2" fades in between
    them and its dashes close into a solid TEAL "container"; "the venv now lives in an image": the venv
    slides into it; "at slash dot venv": `/.venv` under it. "You built it on your laptop": the nest
    shrinks (shapes only) and slides right to become the "run" end; a GREY laptop with a small image on
    its screen fades in at the left, "build". "pushed it to a registry": a PINK route draws to a BLUE
    Docker Hub shelf ("push") and the image rides it; "and ran it on a VM": a second PINK route into
    the nest ("run"), the image rides it and the container flashes; "with one command": the nest's
    container pulses.
 4  "Test yourself" (YELLOW underline). "One": Q1 (26 pt, YELLOW badge) and a text-free icon card: four
    slabs (an image); "and a container": a dashed glowing TEAL glass slab with a dot lands on top; "and
    what does dash dash rm delete": `--rm` in the question turns YELLOW and the glass dissolves upward,
    the slabs untouched. "Two": Q1 becomes the first list row at left ("image vs container", GREY);
    Q2 + icon: a TEAL card with two tile rows and a start-up line under it; "what does our container
    run at startup": both tiles copy down into the line; "and what happens if you add": a WHITE tile
    slides in and knocks the CMD tile off the card; the line's second part turns WHITE.
 5  "Three": Q2 -> "start-up command line"; Q3 + icon: a text-free number line; "Python 3.12": an ORANGE
    dot drops at 3.12; "so why does python report": the GREEN interval glows from 3.13 and a GREEN dot
    lands at 3.15; "or 3.14": a second, dimmer GREEN dot at 3.14. "Four": Q3 -> "two Pythons"; Q4 + icon:
    four build-step boxes on dominoes; a GREY file glyph lands on box 3 (COPY); "which steps rerun":
    boxes 3-4 turn RED and their dominoes topple RED; "and how would you reorder": two dashed YELLOW
    swap arrows over boxes 3-4 (a hint, not the answer). "Five": Q4 -> "cache order"; Q5 + icon: a GREY
    laptop over a GREY arm64 glyph chip, a BLUE VM over a BLUE amd64 glyph chip; "name two ways": two
    dashed PINK routes arc from the arm64 chip to the amd64 chip, each with a YELLOW "?".
 6  Q5 -> "platforms"; the five-row list stays at left. "The answers": card "Answers: exercises.md";
    "every command": card "Study guide + every command:" github.com/JunyiZhou-Conny/MLOps_Learning /
    guides/L02-containers-1.md. "Next time": a GREY dashed card "Next: L3 · Containers II"; "five
    containers": five small dashed TEAL boxes linked in a row; "a working directory": chip `WORKDIR /app`;
    "a non-root user": chip "non-root user"; "and your laptop's folder": a GREY folder, a dashed arrow
    into a dashed TEAL container, "mounted". The tag `Lecture 2 · slides 42–51, 78–79` comes with the Next
    card ("Next time"), under it and right-aligned with it (the Answers card holds the top right), and
    leaves with it. Everything fades to an empty frame (end of part 2).

Terminal output comes from capture() only (vm-debian12/11). The console, dialog and checklist
vocabulary is L1's s15_recap.py / S14's console (same layout ideas, same glyphs); the question layout
and wrapping are L1's. Every icon is made of its set piece's shapes and carries no text.
"""

import re  # noqa: I001  (manim first, then common: common must win)
from functools import cache

import numpy as np
from manim import *

from explainer import style as S
from explainer.devops import MONO, TERM_BG, browser_window, file_glyph, folder_glyph, lecture_ref, step_badge
from explainer.scene import VoiceScene

from common import (CLOUD, COST, ERR, IMAGE, INK, LAPTOP, NARRATION, ROUTE, STRIP_ROWS, SYSTEM, TURN,
                    VENV, VM12, VM_HOST, CostDial, Nest, Slab, bare_prompt, beside, box, capture,
                    check_mark, chip, glyph_row, illustration_tag, label, laptop, lock_glyph, mini_stack,
                    mono, pin, route, row_tag, shelf_glyph, squeeze, tag, track, tracker_c, travel, type_cmd,
                    vm_term, your_turn)

SAY = NARRATION["S16"]

# ------------------------------------------------------------------ real outputs (file line numbers)
C11 = capture("11", VM12)                         # `sudo docker ps -a` on the VM, after every --rm run
PS_A = C11.cmd
assert PS_A == "sudo docker ps -a" and C11.exit == 0, PS_A
HEADER = squeeze(C11.at(2))                       # the header only (a header-only table keeps its columns)
assert len(HEADER) == 1 and HEADER[0].startswith("CONTAINER ID") and HEADER[0].endswith("NAMES"), HEADER

URL = "console.cloud.google.com/compute/instances"
GUIDE_REPO = "github.com/JunyiZhou-Conny/MLOps_Learning"
GUIDE_FILE = "guides/L02-containers-1.md"
NBSP = " "

# the five questions (script.md S16, on screen); spans in the code font
QUESTIONS = [
    ("What is the difference between an image and a container, and what does --rm delete?", ["--rm"]),
    (("What command line does our container run at start-up, and what happens with "
      "docker run --rm -ti simple-translate python cli.py?"),
     ["docker run --rm -ti simple-translate python cli.py"]),
    (("The Dockerfile says python:3.12. Why does python --version print 3.15 (or 3.14), and what does "
      "/usr/local/bin/python print?"), ["python:3.12", "python --version", "/usr/local/bin/python"]),
    (("You edit one line of cli.py. Which build steps re-run, and how would you reorder the Dockerfile so "
      "uv sync stays cached?"), ["cli.py", "uv sync"]),
    ("Name two ways to make an image built on Apple Silicon run on a default GCP VM.", []),
]
ROWS = ["image vs container", "start-up command line", "two Pythons", "cache order", "platforms"]

# ------------------------------------------------------------------ layout
VM_C, VM_W, VM_H = np.array([-0.4, 0.82, 0]), 6.5, 3.7       # beat 0: the VM above the strip
STACK_X, FLOOR_Y = -1.25, -0.36                             # its image stack (bottom edge)
DIAL_C, DIAL_R = np.array([4.55, 1.7, 0]), 0.55             # beats 0-1: the dial (it never moves while it runs)
RATE = 1 / 60                                               # dial turns per second while the VM exists (S14's)
# The meter never rewinds (script.md conventions): the needle starts where the VM's meter has got to.
# S14's dial starts at "The meter starts" (24:56.3 in the 2026-10-15 draft) and sweeps at 1/60 turn/s
# until S14 freezes it before its last fade (26:34.0); S15 (121 s then, 124.3 s re-measured 2026-10-17
# after its narration edits; S14's meter span still 97.7 s) carries it on at the same rate. Re-measure
# if S14 or S15 changes length by more than a few seconds (1 s = 6 degrees).
# These are clock values. A rendered updater loses one frame of dt per play()/wait(), so S14's needle
# really stops near 1.55 turns at 30 fps (1.48 in the 15 fps draft). Starting S16 from the clock value
# therefore errs forward, never back.
S14_END = (1594.0 - 1496.3) / 60                            # 1.63 turns
S15_END = S14_END + 124.3 / 60                              # 3.70 turns: S16's dial starts here
SM_C, SM_W, SM_H = np.array([4.45, -0.88, 0]), 3.8, 2.55    # beat 1: the VM in the right column
BR_LEFT, BR_TOP, BR_W, BR_H = -6.55, 2.72, 8.6, 5.2         # beat 1: the console
C_LEFT = BR_LEFT + 0.35
LIST_RIGHT = BR_LEFT + BR_W - 0.3
D_LEFT, D_RIGHT = C_LEFT + 0.45, LIST_RIGHT - 0.25

Q_X, Q_TOP, Q_W, Q_SIZE = -5.8, 2.52, 12.15, 26             # the current question (full width)
LIST_X, LIST_TOP, LIST_PITCH, LIST_SIZE = -5.2, 0.72, 0.62, 22   # badges clear of the drop column
ICON_C, ICON_W, ICON_H = np.array([1.75, -0.78, 0]), 5.6, 3.3
RIGHT_L, RIGHT_R = -1.85, 6.4                                # beat 6: the right column


# ------------------------------------------------------------------ timing
def cue(scene, vo, phrase: str, shift: float = 0.0) -> None:
    """vo.wait_until(phrase), moved by `shift` seconds. Inside a sentence an anchor is interpolated by
    character count; the shifts used below were measured on the cached Kokoro clips (af_heart, 0.9):
    each phrase starts right after the pause at its clause's comma. Re-measure after a SAY edit."""
    t = vo.clip.time_of(phrase)
    if t is None:                     # logs "voiceover anchor not found" (an error, PLAYBOOK 2.6)
        vo.wait_until(phrase)
        return
    left = t + shift - vo.elapsed
    if left > 1 / 60:
        scene.wait(left)


# ------------------------------------------------------------------ small glyphs (L1's)
def pulse(m, factor: float = 1.15):
    """A tag's pulse: grow and settle back (Indicate would flood an opaque tag with its colour)."""
    return m.animate(rate_func=there_and_back).scale(factor)


def disk_glyph(w: float, h: float, color=CLOUD) -> VGroup:
    """A disk (a short cylinder), as in L1's V1."""
    e = w * 0.3
    rect = Rectangle(width=w, height=h)
    top = Ellipse(width=w, height=e).move_to(rect.get_top())
    bot = Ellipse(width=w, height=e).move_to(rect.get_bottom())
    body = Union(rect, top, bot).set_stroke(color, 2.5).set_fill(color, 0.22)
    lid = Ellipse(width=w, height=e, stroke_color=color, stroke_width=2.5).set_fill(color, 0.45)
    lid.move_to(rect.get_top())
    return VGroup(body, lid)


def dust(mob, color, rng, n: int, r: float = 0.03) -> VGroup:
    """Small dots scattered over mob's area (what a dissolving thing turns into)."""
    lo, hi = mob.get_corner(DL), mob.get_corner(UR)
    pts = np.c_[rng.uniform(lo[0], hi[0], n), rng.uniform(lo[1], hi[1], n), np.zeros(n)]
    return VGroup(*[Dot(p, radius=r, color=color) for p in pts])


def icon_chip(icon: VMobject, s: str, color=S.GREY, size: float = 22) -> VGroup:
    t = label(s, size, INK)
    inner = VGroup(icon, t).arrange(RIGHT, buff=0.14)
    h = mono("|", size).height + 0.24
    b = box(inner.width + 0.5, h, color, fill_opacity=0.16, radius=h / 2.6)
    inner.move_to(b)
    g = VGroup(b, inner)
    g.box, g.text, g.icon = b, t, icon
    return g


def stop_icon(s: float = 0.16, color=INK) -> Square:
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


def words(t: Text, sub: str) -> VGroup:
    """The glyphs of `sub` inside a Text (spaces have no glyphs)."""
    s = "".join(t.text.split())
    i = s.find("".join(sub.split()))
    assert i >= 0, (sub, t.text)
    return VGroup(*t.submobjects[i:i + len("".join(sub.split()))])


def uline(g, color, stroke: float = 3.5, dy: float = 0.07) -> Line:
    y = g.get_bottom()[1] - dy
    return Line([g.get_left()[0] - 0.03, y, 0], [g.get_right()[0] + 0.03, y, 0], color=color,
                stroke_width=stroke)


def slab_stack(fills, heights, stack_w: float, gap: float = 0.03) -> VGroup:
    """Text-free layer slabs bottom-up (TEAL outlines, fills by content)."""
    return VGroup(*[Slab(None, f, stack_w, h) for f, h in zip(fills, heights)]).arrange(UP, buff=gap)


def glass_shape(glass_w: float, glass_h: float = 0.42) -> VGroup:
    """A container's writable layer without text (Glass's look): glow, dashed TEAL slab, process dot."""
    base = RoundedRectangle(width=glass_w, height=glass_h, corner_radius=0.08)
    glow = base.copy().set_stroke(IMAGE, 10, opacity=0.25).set_fill(IMAGE, 0.08)
    slab = DashedVMobject(base.copy().set_stroke(IMAGE, 2.5), num_dashes=40, dashed_ratio=0.6)
    dot = Dot(radius=0.09, color=IMAGE).move_to(base.get_right() + LEFT * 0.3)
    return VGroup(glow, slab, dot)


def dashed_arrow(a, b, angle: float, color: str, n: int = 14) -> VGroup:
    """A dashed curved arrow from a to b (a hint, a future thing)."""
    arc = ArcBetweenPoints(a, b, angle=angle)
    d = DashedVMobject(arc, num_dashes=n, dashed_ratio=0.55).set_stroke(color, 3)
    end, prev = arc.point_from_proportion(1), arc.point_from_proportion(0.94)
    v = end - prev
    tip = Triangle(stroke_width=0).set_fill(color, 1).scale(0.1)
    tip.rotate(np.arctan2(v[1], v[0]) - PI / 2).move_to(end - v / np.linalg.norm(v) * 0.06)
    g = VGroup(d, tip)
    g.arc = arc
    return g


# ------------------------------------------------------------------ beat 0/1: the VM
def vm_picture() -> VGroup:
    """The BLUE VM ac215-l02 with the dlops image (seven slabs) and its boot disk.
    .frame .title .slabs .name .disk .disk_lab .slot .slot_text .rm .rm_cap"""
    g = VGroup()
    frame = box(VM_W, VM_H, CLOUD, fill_opacity=0.06).move_to(VM_C)
    title = VGroup(label("VM", 24, CLOUD), mono(VM_HOST, 22, CLOUD)).arrange(RIGHT, buff=0.18)
    title.move_to(frame.get_corner(UL) + np.array([0.32 + title.width / 2, -0.4, 0]))
    slabs = slab_stack([SYSTEM] * 5 + [LAPTOP, VENV], [0.12] * 4 + [0.28, 0.24, 0.5], 2.4)
    slabs.move_to([STACK_X, 0, 0]).align_to([0, FLOOR_Y, 0], DOWN)
    name = mono("dlops/simple-translate", 20, IMAGE).next_to(slabs, DOWN, buff=0.12)
    slot = VGroup(DashedVMobject(RoundedRectangle(width=2.4, height=0.42, corner_radius=0.08),
                                 num_dashes=34, dashed_ratio=0.55).set_stroke(S.GREY, 2.5))
    slot.next_to(slabs, UP, buff=0.08)
    slot_text = label("no containers", 20, S.GREY).move_to(slot)
    rm = chip("--rm", IMAGE, size=22, font=MONO)
    rm.move_to(slot).align_to([slot.get_right()[0] + 0.45, 0, 0], LEFT)
    rm_cap = label("removed at exit", 20, S.GREY).next_to(rm, DOWN, buff=0.14).align_to(rm, LEFT)
    disk = disk_glyph(0.5, 0.42).move_to([rm.get_x() + 0.1, FLOOR_Y + 0.55, 0])
    disk_lab = label("boot disk", 20, CLOUD).next_to(disk, DOWN, buff=0.14)
    g.add(frame, title, slabs, name, disk, disk_lab)
    g.frame, g.title, g.slabs, g.name, g.disk, g.disk_lab = frame, title, slabs, name, disk, disk_lab
    g.slot, g.slot_text, g.rm, g.rm_cap = slot, slot_text, rm, rm_cap
    return g


def vm_small(v: VGroup) -> VGroup:
    """Targets for the VM in the right column: the frame and slabs shrink, the labels keep their size.
    .frame .title .slabs .disk .disk_lab"""
    frame = box(SM_W, SM_H, CLOUD, fill_opacity=0.06).move_to(SM_C)
    title = v.title.copy()
    title.move_to(frame.get_corner(UL) + np.array([0.3 + title.width / 2, -0.38, 0]))
    slabs = v.slabs.copy().scale(0.62)
    slabs.move_to([SM_C[0] - 0.8, 0, 0]).align_to(frame, DOWN).shift(UP * 0.38)
    disk = v.disk.copy().move_to([SM_C[0] + 1.05, slabs.get_y() + 0.12, 0])
    disk_lab = v.disk_lab.copy().next_to(disk, DOWN, buff=0.14)
    g = VGroup(frame, title, slabs, disk, disk_lab)
    g.frame, g.title, g.slabs, g.disk, g.disk_lab = frame, title, slabs, disk, disk_lab
    return g


# ------------------------------------------------------------------ question text (L1's)
def text_line(s: str, size: float, color: str, code=()) -> VGroup:
    """One line of house-font text whose code spans use the code font, with a FIXED vertical
    extent (built with a leading '|' that is dropped, as mono_line does). .glyphs .strut"""
    t2f = {c: MONO for c in code if c in s}
    # no ligatures ("fi" in "Dockerfile" would be one glyph): one submobject per character, spaces
    # included as empty dots, which are dropped so that glyph k is the k-th non-space character
    t = S.text("|" + s, size, color, t2f=t2f, disable_ligatures=True)
    subs = [m for ch, m in zip("|" + s, t.submobjects) if not ch.isspace()]
    assert len(t.submobjects) == len(s) + 1, (s, len(t.submobjects))
    pipe = subs[0]
    strut = Rectangle(width=max(0.01, t.width), height=pipe.height, stroke_width=0, fill_opacity=0)
    strut.move_to(pipe.get_center()).align_to(t, LEFT)
    gl = VGroup(*subs[1:])
    strut.stretch_to_fit_width(max(0.01, gl.width)).align_to(gl, LEFT)
    g = VGroup(strut, *gl.submobjects)
    g.glyphs, g.strut = VGroup(*gl.submobjects), strut
    return g


@cache
def _line_width(s: str, size: float, code: tuple) -> float:
    return text_line(s, size, INK, code).glyphs.width


def _layout(s: str, size: float, width: float, code: tuple) -> list:
    """Line breaks with the fewest lines and, among those, the most even fill."""
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
    strs = wrap_lines(s, size, width, code)
    rows = [text_line(ln, size, color, code) for ln in strs]
    pitch = rows[0].strut.height * 1.22
    for k, r in enumerate(rows):
        r.shift(np.array([-r.strut.get_left()[0], -k * pitch - r.strut.get_top()[1], 0]))
    g = VGroup(*rows)
    g.lines, g.strs = rows, strs
    g.glyphs = VGroup(*[gl for r in rows for gl in r.glyphs])
    return g


def question(i: int) -> VGroup:
    """Question i (1-based), its text's top-left at (Q_X, Q_TOP): a YELLOW badge and the wrapped
    text (at most 2 lines). .badge .text"""
    s, code = QUESTIONS[i - 1]
    txt = wrapped(s, Q_SIZE, INK, Q_W, code)
    assert len(txt.lines) <= 2, (i, txt.strs)
    b = step_badge(i, TURN, size=22, radius=0.24)
    b.move_to([-0.2 - 0.24, txt.lines[0].strut.get_center()[1], 0])
    g = VGroup(b, txt)
    g.badge, g.text = b, txt
    first = txt.lines[0].strut
    g.shift(np.array([Q_X - first.get_left()[0], Q_TOP - first.get_top()[1], 0]))
    return g


def q_span(q: VGroup, sub: str) -> VGroup:
    """The glyphs of `sub` in question q's text (a span never crosses a line break)."""
    key = "".join(sub.split())
    for r, s in zip(q.text.lines, q.text.strs):
        i = "".join(s.split()).find(key)
        if i >= 0:
            return VGroup(*r.glyphs[i:i + len(key)])
    raise AssertionError((sub, q.text.strs))


def list_row(i: int) -> VGroup:
    """Row i (1-based) of the list at left: a GREY badge and a one-line label. .badge .text"""
    t = text_line(ROWS[i - 1], LIST_SIZE, S.GREY)
    y = LIST_TOP - (i - 1) * LIST_PITCH
    t.shift(np.array([LIST_X - t.strut.get_left()[0], y - t.strut.get_center()[1], 0]))
    b = step_badge(i, S.GREY, size=20, radius=0.19).move_to([LIST_X - 0.38, y, 0])
    g = VGroup(b, t)
    g.badge, g.text = b, t
    return g


# ------------------------------------------------------------------ the five icons (text-free)
def icon_frame() -> VMobject:
    return box(ICON_W, ICON_H, S.GREY, fill=S.GREY_DARKER, fill_opacity=1).move_to(ICON_C)


def icon_glass() -> VGroup:
    """Q1: four slabs (an image) and, landing on them, a container's glass slab. .slabs .glass"""
    fr = icon_frame()
    slabs = slab_stack([SYSTEM, SYSTEM, LAPTOP, VENV], [0.16, 0.36, 0.26, 0.56], 2.8, gap=0.05)
    glass = glass_shape(2.8)
    VGroup(slabs, glass).arrange(UP, buff=0.07).move_to(ICON_C)
    g = VGroup(fr, slabs)
    g.frame, g.slabs, g.glass = fr, slabs, glass
    return g


def icon_card() -> VGroup:
    """Q2: a TEAL config card with two tile rows (ENTRYPOINT, CMD: text-free) and the start-up line
    under it; a WHITE tile waits at the right. .card .keys .tiles .line .words .new .new_word"""
    fr = icon_frame()
    card = box(3.0, 1.45, IMAGE, fill_opacity=0.06)
    keys = VGroup(*[Line(LEFT * 0.3, RIGHT * 0.3, color=S.GREY, stroke_width=5) for _ in range(2)])
    keys.arrange(DOWN, buff=0.52)
    tiles = VGroup(*[RoundedRectangle(width=1.55, height=0.42, corner_radius=0.08, stroke_color=IMAGE,
                                      stroke_width=2.5).set_fill(IMAGE, 0.3) for _ in range(2)])
    for k, t in zip(keys, tiles):
        t.next_to(k, RIGHT, buff=0.35)
    VGroup(keys, tiles).move_to(card)
    line = RoundedRectangle(width=3.3, height=0.42, corner_radius=0.08, stroke_color=S.GREY_DARK,
                            stroke_width=2).set_fill(TERM_BG, 1).next_to(card, DOWN, buff=0.38)
    wds = VGroup(*[RoundedRectangle(width=w, height=0.16, corner_radius=0.06, stroke_width=0)
                   .set_fill(IMAGE, 0.85) for w in (1.05, 1.6)]).arrange(RIGHT, buff=0.2).move_to(line)
    VGroup(card, keys, tiles, line, wds).move_to(ICON_C).shift(LEFT * 0.4)
    new = tiles[1].copy().set_stroke(INK).set_fill(INK, 0.3)
    new.move_to([fr.get_right()[0] - 0.3 - new.width / 2, tiles[1].get_y(), 0])
    new_word = wds[1].copy().set_fill(INK, 0.9)
    g = VGroup(fr, card, keys, tiles, line)
    g.frame, g.card, g.keys, g.tiles, g.line, g.words, g.new, g.new_word = (fr, card, keys, tiles, line,
                                                                         wds, new, new_word)
    return g


def icon_versions() -> VGroup:
    """Q3: a text-free number line (3.11 to 3.16); .band (GREEN from 3.13), .orange (3.12),
    .green (3.15), .green2 (3.14, dimmer)."""
    fr = icon_frame()
    w = 4.4
    axis = Line(LEFT * w / 2, RIGHT * w / 2, color=S.GREY, stroke_width=3)
    first, last = 11, 16

    def x(m):
        return -w / 2 + (m - first + 0.5) / (last - first + 1) * w

    ticks = VGroup(*[Line([x(m), -0.12, 0], [x(m), 0.12, 0], color=S.GREY, stroke_width=2.5)
                     for m in range(first, last + 1)])
    right = w / 2 + 0.2
    band = Rectangle(width=right - x(13) + 0.15, height=0.3, stroke_width=0).set_fill(VENV, 0.3)
    band.move_to([(x(13) - 0.15 + right) / 2, 0, 0])
    body = VGroup(band, axis, ticks).move_to(ICON_C + DOWN * 0.35)
    off = body[1].get_center() - ORIGIN

    def pt(m, dy=0.0):
        return np.array([x(m), dy, 0]) + off

    orange = Dot(pt(12, 0.0), radius=0.13, color=SYSTEM)
    green = Dot(pt(15, 0.0), radius=0.13, color=VENV)
    green2 = Dot(pt(14, 0.0), radius=0.11, color=VENV).set_opacity(0.55)
    g = VGroup(fr, axis, ticks)
    g.frame, g.axis, g.ticks, g.band, g.orange, g.green, g.green2 = fr, axis, ticks, band, orange, green, green2
    g.pt = pt
    return g


class Topple(Rotate):
    """Rotate a domino about its bottom-right corner and recolour it on the way."""

    def __init__(self, mob, angle, color, **kw):
        self.to_color = color
        super().__init__(mob, angle=angle, about_point=mob.get_corner(DR), **kw)

    def create_target(self):
        t = super().create_target()
        t.set_fill(self.to_color, 0.6).set_stroke(self.to_color)
        return t


def icon_dominoes() -> VGroup:
    """Q4: four build-step boxes on dominoes; .boxes .dominoes .file (lands on box 3) .swap (hint)."""
    fr = icon_frame()
    boxes = VGroup(*[RoundedRectangle(width=0.92, height=0.62, corner_radius=0.08, stroke_color=S.GREY,
                                      stroke_width=2.5).set_fill(S.GREY_DARK, 0.6) for _ in range(4)])
    boxes.arrange(RIGHT, buff=0.32)
    dominoes = VGroup()
    for b in boxes:
        d = Rectangle(width=0.18, height=0.62, stroke_color=S.GREY, stroke_width=2).set_fill(S.GREY, 0.45)
        d.next_to(b, DOWN, buff=0.35)
        dominoes.add(d)
    floor = Line(dominoes.get_corner(DL) + LEFT * 0.3, dominoes.get_corner(DR) + RIGHT * 0.6,
                 color=S.GREY_DARK, stroke_width=2)
    body = VGroup(boxes, dominoes, floor).move_to(ICON_C + DOWN * 0.2)
    f = file_glyph(0.42, S.GREY).next_to(boxes[2], UP, buff=0.18)
    a, b = boxes[2].get_top() + UP * 0.12, boxes[3].get_top() + UP * 0.12
    swap = VGroup(dashed_arrow(a, b, -1.2, TURN, n=10), dashed_arrow(b + DOWN * 0.0, a, -1.2, TURN, n=10))
    swap[1].shift(DOWN * (boxes.get_height() + 0.24))
    g = VGroup(fr, boxes, dominoes, floor)
    g.frame, g.boxes, g.dominoes, g.file, g.swap, g.body = fr, boxes, dominoes, f, swap, body
    return g


def icon_platforms() -> VGroup:
    """Q5: a GREY laptop over an arm64 glyph chip, a BLUE VM over an amd64 glyph chip.
    .routes (two dashed PINK arcs) .qs (two YELLOW ?)"""
    fr = icon_frame()

    def glyph_chip(kind, color):
        gl = glyph_row(kind, 5, glyph_h=0.2)
        b = box(gl.width + 0.5, 0.62, color, fill_opacity=0.12, radius=0.2)
        gl.move_to(b)
        return VGroup(b, gl)

    arm, amd = glyph_chip("arm64", LAPTOP), glyph_chip("amd64", CLOUD)
    lap = laptop(1.0, LAPTOP)
    vmb = box(1.0, 0.68, CLOUD, fill_opacity=0.15, radius=0.08)
    slots = VGroup(*[RoundedRectangle(width=0.7, height=0.12, corner_radius=0.03, stroke_color=CLOUD,
                                      stroke_width=1.5) for _ in range(2)]).arrange(DOWN, buff=0.1).move_to(vmb)
    vm = VGroup(vmb, slots)
    left = VGroup(lap, arm).arrange(DOWN, buff=0.25)
    right = VGroup(vm, amd).arrange(DOWN, buff=0.25)
    right.align_to(left, DOWN)
    VGroup(left, right).arrange(RIGHT, buff=1.3, aligned_edge=DOWN).move_to(ICON_C)
    a, b = arm.get_right() + RIGHT * 0.12, amd.get_left() + LEFT * 0.12
    r1 = dashed_arrow(a + UP * 0.12, b + UP * 0.12, -0.9, ROUTE, n=12)
    r2 = dashed_arrow(a + DOWN * 0.12, b + DOWN * 0.12, 0.9, ROUTE, n=12)
    qs = VGroup(*[label("?", 30, TURN).move_to(r.arc.point_from_proportion(0.5)) for r in (r1, r2)])
    qs[0].shift(UP * 0.28)
    qs[1].shift(DOWN * 0.28)
    g = VGroup(fr, left, right)
    g.frame, g.arm, g.amd, g.lap, g.vm, g.routes, g.qs = fr, arm, amd, lap, vm, VGroup(r1, r2), qs
    return g


# ------------------------------------------------------------------ beat 6: where next
def card(body: VMobject, card_w: float | None = None, dashed: bool = False) -> VGroup:
    w = card_w or body.width + 0.7
    if dashed:
        frame = box(w, body.height + 0.5, S.GREY, dashed=True)
    else:
        frame = box(w, body.height + 0.5, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
    body.move_to(frame).align_to(frame, LEFT).shift(RIGHT * 0.35)
    g = VGroup(frame, body)
    g.frame, g.body = frame, body
    return g


def teaser(card_w: float) -> VGroup:
    """The L3 teaser (GREY dashed, a future thing): five dashed TEAL containers linked in a row, the
    chips `WORKDIR /app` and "non-root user", and a GREY folder with a dashed arrow into a dashed TEAL
    container, "mounted". .head .five .links .workdir .user .folder .arrow .ctr .mounted .frame"""
    head = VGroup(label("Next:", 26, S.GREY), label("L3 · Containers II", 26, INK)).arrange(RIGHT, buff=0.15)
    five = VGroup(*[box(0.66, 0.5, IMAGE, dashed=True) for _ in range(5)]).arrange(RIGHT, buff=0.25)
    links = VGroup(*[Line(five[k].get_right(), five[k + 1].get_left(), color=S.GREY, stroke_width=2.5)
                     for k in range(4)])
    workdir = chip("WORKDIR /app", S.GREY, size=20, font=MONO)
    user = chip("non-root user", S.GREY, size=20)
    chips = VGroup(workdir, user).arrange(RIGHT, buff=0.2)
    left = VGroup(VGroup(five, links), chips).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
    folder = folder_glyph(0.5, LAPTOP)
    ctr = box(1.0, 0.85, IMAGE, dashed=True)
    ctr_f = folder_glyph(0.36, LAPTOP).move_to(ctr).set_opacity(0.6)
    VGroup(folder, ctr).arrange(RIGHT, buff=0.95)
    arrow = dashed_arrow(folder.get_right() + RIGHT * 0.12, ctr.get_left() + LEFT * 0.1, 0, S.GREY, n=8)
    ctr_f.move_to(ctr)
    mounted = label("mounted", 22, S.GREY).next_to(VGroup(folder, arrow, ctr), DOWN, buff=0.16)
    rgrp = VGroup(folder, ctr, ctr_f, arrow, mounted)
    content = VGroup(left, rgrp).arrange(RIGHT, buff=0.3, aligned_edge=UP)
    body = VGroup(head, content).arrange(DOWN, buff=0.32, aligned_edge=LEFT)
    g = card(body, card_w, dashed=True)
    g.head, g.five, g.links, g.workdir, g.user = head, five, links, workdir, user
    g.folder, g.arrow, g.ctr, g.ctr_f, g.mounted = folder, arrow, ctr, ctr_f, mounted
    return g


# ------------------------------------------------------------------ the scene
class Recap(VoiceScene):
    def construct(self):
        assert len(SAY) == 7, f"S16 has {len(SAY)} SAY lines; this scene times 7"
        rng = np.random.default_rng(16)

        # ========================================================== 0 · docker ps -a: nothing left
        tr = tracker_c(6, extra=True)
        t = vm_term(STRIP_ROWS)
        V = vm_picture()
        dial = CostDial(radius=DIAL_R, caption=None).move_to(DIAL_C)
        dial.tracker.set_value(S15_END)               # it goes on from where S15 left it
        dial.needle.update()                          # (FadeIn suspends the redraw: draw it there now)
        cost = label("cost", 22, COST).next_to(dial, RIGHT, buff=0.2)
        rate = ValueTracker(RATE)
        dial.tracker.add_updater(lambda m, dt: m.increment_value(dt * rate.get_value()))

        with self.voiceover(SAY[0]) as vo:
            self.add(dial.tracker)
            self.play(FadeIn(tr, shift=DOWN * 0.1), FadeIn(t, shift=UP * 0.2), FadeIn(V, scale=0.97),
                      FadeIn(dial, scale=0.8), FadeIn(cost), run_time=0.9)
            vo.wait_until("An extra check")
            c_ps = type_cmd(self, t, PS_A, 0.8)
            x_tag = beside(row_tag("extra"), c_ps, buff=0.45)
            pin(self, c_ps, x_tag, run_time=0.35)
            vo.wait_until("sudo docker ps dash a")          # the clause start (SAY[0] now says "sudo")
            out = t.print(self, HEADER, run_time=0.4)
            bare_prompt(self, t)
            vo.wait_until("shows no containers")
            head_row = out[0]
            bar = Rectangle(width=head_row.glyphs.width + 0.16, height=head_row.strut.height * 0.92,
                            stroke_width=0).set_fill(TURN, 0.22).move_to(
                [head_row.glyphs.get_center()[0], head_row.strut.get_center()[1], 0])
            self.play(FadeIn(bar), run_time=0.4)
            self.remove(bar)
            head_row.add_to_back(bar)
            self.add(head_row)
            self.play(Create(V.slot), FadeIn(V.slot_text), run_time=0.7)
            vo.wait_until("thanks to dash dash rm")
            self.play(FadeIn(V.rm, shift=LEFT * 0.15), FadeIn(V.rm_cap, shift=UP * 0.1), run_time=0.5)
            self.play(pulse(V.rm, 1.25), run_time=0.7)

        # ========================================================== 1 · C7: delete the VM
        sm = vm_small(V)
        br = browser_window(URL, width=BR_W, height=BR_H, size=20)
        br.shift(np.array([BR_LEFT - br.frame.get_left()[0], BR_TOP - br.frame.get_top()[1], 0]))
        ill = illustration_tag()
        ill.move_to(br.frame.get_corner(DR) + np.array([-ill.width / 2 - 0.3, 0, 0]))
        heading = VGroup(label("Compute Engine", 26, INK), label("›", 26, S.GREY), label("VM instances", 26, INK))
        heading.arrange(RIGHT, buff=0.2).move_to([0, 1.72, 0]).set_x(C_LEFT, LEFT)
        stop_b = icon_chip(stop_icon(), "Stop")
        del_b = icon_chip(trash_icon(), "Delete")
        toolbar = VGroup(stop_b, del_b).arrange(RIGHT, buff=0.3).move_to([0, 0.98, 0]).set_x(C_LEFT, LEFT)
        sep = Line([C_LEFT - 0.1, 0.5, 0], [LIST_RIGHT, 0.5, 0], color=S.GREY_DARK, stroke_width=2)
        X_CB, X_ST, X_NAME, X_MT, X_CONN = C_LEFT + 0.2, C_LEFT + 0.62, C_LEFT + 1.7, C_LEFT + 3.75, C_LEFT + 6.45
        Y_HEAD, Y_ROW = 0.12, -0.6
        cb_head = checkbox().move_to([X_CB, Y_HEAD, 0])
        heads = VGroup(*[label(s, 22, S.GREY).move_to([0, Y_HEAD, 0]).set_x(x, LEFT)
                         for s, x in (("Status", X_ST), ("Name", X_NAME), ("Machine type", X_MT),
                                      ("Connect", X_CONN))])
        cb = checkbox().move_to([X_CB, Y_ROW, 0])
        running = check_mark(0.28, S.GREEN).move_to([X_ST + 0.2, Y_ROW, 0])
        r_name = mono(VM_HOST, 22, INK).move_to([0, Y_ROW, 0]).set_x(X_NAME, LEFT)
        r_mt = mono("e2-small", 20, S.GREY).move_to([0, Y_ROW, 0]).set_x(X_MT, LEFT)
        r_ssh = chip("SSH", CLOUD, size=22).move_to([0, Y_ROW, 0]).set_x(X_CONN, LEFT)
        row_frame = box(LIST_RIGHT - (C_LEFT - 0.1), 0.66, S.GREY, fill_opacity=0.05, radius=0.08)
        row_frame.move_to([(C_LEFT - 0.1 + LIST_RIGHT) / 2, Y_ROW, 0])
        row = VGroup(row_frame, cb, running, r_name, r_mt, r_ssh)
        page = VGroup(heading, toolbar, sep, cb_head, heads, row)
        assert r_ssh.get_right()[0] < LIST_RIGHT - 0.1, "SSH chip outside the row"

        # the confirm dialog (L1's)
        dim = Rectangle(width=BR_W - 0.04, height=BR_H - 0.57, stroke_width=0).set_fill(S.BG, 0.62)
        dim.align_to(br.frame, DOWN).shift(UP * 0.02).set_x(br.frame.get_x())
        d_title = VGroup(label("Delete", 28, INK), mono(VM_HOST, 26, INK), label("?", 28, INK))
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
        dialog = VGroup(d_frame, d_text, buttons)     # the console's `illustration` tag covers it
        body_bar = Rectangle(width=d_body.width + 0.16, height=d_body.height + 0.14, stroke_width=0) \
            .set_fill(TURN, 0.2).move_to(d_body)

        # the checklist (L1's), the frozen dial beside it
        items = []
        for name in ("VM instances", "Disks"):
            sq = RoundedRectangle(width=0.46, height=0.46, corner_radius=0.07, stroke_color=S.GREY,
                                  stroke_width=2.5).set_fill(TERM_BG, 1)
            tx = label(f"{name}: empty", 34, INK).next_to(sq, RIGHT, buff=0.32)
            it = VGroup(sq, tx)
            it.sq, it.text, it.tick, it.empty = sq, tx, check_mark(0.42, S.GREEN, stroke=6), words(tx, "empty")
            items.append(it)
        rows_c = VGroup(*items).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        c_frame = box(rows_c.width + 1.4, rows_c.height + 0.9, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
        rows_c.move_to(c_frame)
        check = VGroup(c_frame, rows_c).move_to([-1.4, 0.35, 0])
        yt = your_turn().next_to(check, DOWN, buff=0.35)
        dial_to = np.array([check.get_right()[0] + 1.25, check.get_y(), 0])

        with self.voiceover(SAY[1]) as vo:
            # the SSH session is over; the VM compacts into the right column, the console comes in
            v_out = VGroup(V.slot, V.slot_text, V.rm, V.rm_cap, V.name)
            self.play(track(tr, 7), FadeOut(t), FadeOut(v_out),
                      Transform(V.frame, sm.frame), Transform(V.title, sm.title), Transform(V.slabs, sm.slabs),
                      Transform(V.disk, sm.disk), Transform(V.disk_lab, sm.disk_lab), run_time=0.7)
            V.remove(V.name)
            self.remove(*v_out)
            self.play(FadeIn(br, shift=RIGHT * 0.2), FadeIn(ill), FadeIn(page), run_time=0.45)
            cb.tick.move_to(cb.sq).shift(DOWN * 0.005)
            self.play(cb.sq.animate.set_fill(CLOUD, 1).set_stroke(CLOUD), Create(cb.tick),
                      row_frame.animate.set_stroke(CLOUD).set_fill(CLOUD, 0.1), run_time=0.35)
            self.remove(cb.tick)
            cb.add(cb.tick)
            cue(self, vo, "delete the VM", 0.3)             # measured: 1.71 s (interpolated 1.40)
            self.play(Indicate(del_b, color=S.WHITE, scale_factor=1.15), run_time=0.4)
            self.play(FadeIn(dim), FadeIn(dialog, scale=0.94), run_time=0.4)
            cue(self, vo, "with its boot disk", 0.35)       # measured: 2.98 s (2.55)
            self.play(FadeIn(body_bar), Indicate(V.disk, color=CLOUD, scale_factor=1.3), run_time=0.55)
            self.play(Indicate(confirm, color=S.WHITE, scale_factor=1.2), run_time=0.3)
            # Delete: the dialog closes, the row leaves the list, the VM and its disk dissolve and the
            # needle stops where it is (it never rewinds)
            gone = VGroup(V.frame, V.title, V.slabs, V.disk, V.disk_lab)
            dust_v = VGroup(dust(V.frame, CLOUD, rng, 60), dust(V.disk, CLOUD, rng, 12))
            self.play(FadeOut(VGroup(dialog, body_bar, dim), scale=0.96), FadeOut(row, shift=LEFT * 0.4),
                      FadeOut(gone, scale=0.96), FadeIn(dust_v), run_time=0.35)
            page.remove(row)
            self.remove(V, *gone)
            drift = [d.animate.shift(UP * rng.uniform(0.25, 0.7) + RIGHT * rng.uniform(-0.25, 0.25)).set_opacity(0)
                     for d in dust_v.family_members_with_points()]
            self.play(*drift, rate.animate.set_value(0), run_time=0.6)
            self.remove(dust_v)
            dial.tracker.clear_updaters()
            self.remove(dial.tracker, rate)
            dial.freeze()
            dial_g = VGroup(dial, cost)
            vo.wait_until("then check")
            self.play(FadeOut(VGroup(br, ill, page)), dial_g.animate.move_to(dial_to + RIGHT * 0.35),
                      run_time=0.4)
            self.play(FadeIn(check, shift=UP * 0.15), run_time=0.35)
            for it, phrase, shift in zip(items, ("VM instances", "and Disks"), (-0.2, -0.35)):
                cue(self, vo, phrase, shift)                # measured: 5.37, 6.22 s (5.60, 6.60)
                it.tick.move_to(it.sq).shift(UP * 0.03 + RIGHT * 0.03)
                self.play(Create(it.tick), it.sq.animate.set_stroke(S.GREEN), run_time=0.4)
                self.remove(it.tick)
                it.add(it.tick)
            cue(self, vo, "are both empty", -0.4)           # measured: 6.87 s (7.30)
            self.play(*[it.empty.animate.set_color(S.GREEN) for it in items], run_time=0.6)
            vo.wait_until("Pause and do it now")
            self.play(FadeIn(yt, shift=UP * 0.1), run_time=0.4)
            self.play(pulse(yt), run_time=0.6)

        # ========================================================== 2 · two optional chores
        opt = label("optional", 28, S.GREY).move_to([0, 2.28, 0]).set_x(-6.3, LEFT)
        ICON_X, CHIP_L = -5.3, -4.3
        shelf = shelf_glyph(1.3).move_to([ICON_X, 1.2, 0])
        hub_txt = "Docker Hub repository: public until you delete it or make it private"
        hub = chip(hub_txt, S.GREY, size=24).move_to([0, 1.2, 0]).set_x(CHIP_L, LEFT)
        plate = RoundedRectangle(width=0.62, height=0.66, corner_radius=0.1, stroke_color=S.GREY,
                                 stroke_width=2.5).set_fill(S.BG, 1)
        lock = VGroup(plate, lock_glyph(0.46, S.GREY).move_to(plate)).move_to(shelf)
        u_public = uline(words(hub.text, "public"), TURN)
        u_private = uline(words(hub.text, "make it private"), TURN)

        lap = laptop(1.45, LAPTOP).move_to([ICON_X, -0.55, 0])
        scr = lap.screen
        used = Rectangle(width=scr.width - 0.34, height=0.22, stroke_width=0).set_fill(IMAGE, 0.8)
        used.move_to(scr).align_to(scr, LEFT).shift(RIGHT * 0.17 + DOWN * 0.08)
        used_frame = Rectangle(width=scr.width - 0.3, height=0.3, stroke_color=S.GREY_DARK, stroke_width=1.5)
        used_frame.move_to(used).align_to(scr, LEFT).shift(RIGHT * 0.15)
        freed = used.copy().stretch_to_fit_width(0.08).align_to(used, LEFT)
        prune = chip("docker system prune -a", S.GREY, size=24, font=MONO)
        prune.move_to([0, lap.screen.get_y() + 0.1, 0]).set_x(CHIP_L, LEFT)
        prune_cap = label("frees the laptop's disk · said, not typed here", 22, S.GREY)
        prune_cap.next_to(prune, DOWN, buff=0.16).align_to(prune, LEFT).shift(RIGHT * 0.1)

        small = VGroup()
        for cmd, note in (("docker buildx rm multi-arch", "if you ran the push script"),
                          ("docker logout", "optional")):
            small.add(VGroup(chip(cmd, S.GREY, size=20, font=MONO), label(note, 20, S.GREY)).arrange(RIGHT, buff=0.2))
        small.arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([0, -2.45, 0]).set_x(CHIP_L, LEFT)
        assert hub.get_right()[0] < 6.5 and prune_cap.get_right()[0] < 6.5, "chores too wide"
        lref73 = lecture_ref(2, "73")                    # standard top right, "And to reclaim" to beat 2's end
        assert lref73.get_bottom()[1] > hub.get_top()[1] + 0.3 and lref73.get_left()[0] > tr.get_right()[0] + 0.3

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(check, yt, dial_g)), track(tr, extra=True), run_time=0.6)
            self.play(FadeIn(opt, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("Your Docker Hub repository")
            self.play(FadeIn(shelf, shift=RIGHT * 0.15), FadeIn(hub, shift=RIGHT * 0.2), run_time=0.6)
            vo.wait_until("stays public")
            self.play(Create(u_public), words(hub.text, "public").animate.set_color(TURN), run_time=0.5)
            vo.wait_until("or make it private")
            self.play(FadeIn(lock, shift=DOWN * 0.3), Create(u_private), run_time=0.6)
            self.play(pulse(lock, 1.3), run_time=0.6)
            vo.wait_until("And to reclaim the space")
            self.play(FadeIn(lap, shift=RIGHT * 0.15), FadeIn(used_frame), FadeIn(lref73), run_time=0.5)
            self.play(GrowFromEdge(used, LEFT), run_time=0.6)
            vo.wait_until("run docker system prune")
            self.play(FadeIn(prune, shift=RIGHT * 0.2), run_time=0.5)
            self.play(Transform(used, freed), FadeIn(prune_cap, shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in small], lag_ratio=0.3), run_time=0.7)
        self.wait(3.0)                                # (the small print, ~12 words, is read on a pause)

        # ========================================================== 3 · V1: the closing picture
        nest = Nest(vm_w=6.6, vm_h=3.8, size=24).move_to([0, 0.15, 0])
        tag_l1 = tag("L1", S.GREY)
        tag_l1.move_to(nest.vm.frame.get_corner(UR) + np.array([-tag_l1.width / 2 - 0.25, -0.32, 0]))
        slot = nest.slot()
        solid = nest.solid()
        vlab = nest.venv_label()

        # the end of the route: the same nest, shapes smaller, labels the same size; the container is
        # centred in the smaller VM (L1's layout keeps the left half free for the venv, now moved in)
        NEST_TO = np.array([4.2, 0.25, 0])
        ns = Nest(vm_w=4.0, vm_h=2.9, size=24).move_to(NEST_TO)
        ns_solid = ns.solid()
        centre = np.array([ns.vm.frame.get_x() - ns_solid[0].get_x(), 0, 0])
        ns_solid.shift(centre)
        ns.venv.move_to(ns.venv_spot() + centre)
        ns_vlab = ns.venv_label().shift(centre)
        # the container's outline keeps its dashes (a fresh outline_box has fewer, and the Transform
        # would open gaps on the way): the same outline, stretched to the new size
        ctr_to = solid[0].copy()
        ctr_to.stretch_to_fit_width(ns_solid[0].width).stretch_to_fit_height(ns_solid[0].height)
        ctr_to.move_to(ns_solid[0])
        base_y = ns.vm.frame.get_bottom()[1]          # laptop, shelf and VM stand on one line
        lap2 = laptop(2.0, LAPTOP)
        lap2.move_to([-4.95, base_y + lap2.height / 2, 0])
        img = mini_stack(glyph_w=0.8, slab_h=0.13).move_to(lap2.screen)
        hub2 = shelf_glyph(1.5)
        hub2.move_to([-0.95, base_y + hub2.height / 2, 0])
        hub_t = label("Docker Hub", 22, CLOUD).next_to(hub2, UP, buff=0.15)
        y_lab = base_y - 0.42
        l_build = label("build", 26, INK).move_to([lap2.get_x(), y_lab, 0])
        l_push = label("push", 26, INK).move_to([hub2.get_x(), y_lab, 0])
        l_run = label("run", 26, INK).move_to([NEST_TO[0], y_lab, 0])
        y_r = hub2.get_y() + 0.15
        r1 = route(np.array([lap2.get_right()[0] + 0.08, y_r, 0]), np.array([hub2.get_left()[0] - 0.08, y_r, 0]),
                   arc=-0.45)
        r2 = route(np.array([hub2.get_right()[0] + 0.08, y_r, 0]),
                   np.array([ns.vm.frame.get_left()[0] - 0.08, y_r, 0]), arc=-0.45)
        assert l_run.get_bottom()[1] > -3.5

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(opt, shelf, hub, lock, u_public, u_private, lap, used_frame, used,
                                     prune, prune_cap, small, tr, lref73)), run_time=0.6)
            self.play(FadeIn(nest.vm, scale=0.96), FadeIn(tag_l1), run_time=0.6)
            self.play(FadeIn(nest.venv, shift=UP * 0.2), run_time=0.5)
            vo.wait_until("Today a container")
            self.play(FadeIn(slot, scale=1.06), run_time=0.8)
            self.play(ReplacementTransform(slot, solid), run_time=0.7)
            vo.wait_until("the venv now lives")
            self.play(nest.venv.animate.move_to(nest.venv_spot()), run_time=0.9)
            cue(self, vo, "at slash dot venv", -0.35)       # measured: 8.05 s (8.41)
            self.play(FadeIn(vlab, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(vlab, color=VENV, scale_factor=1.2), run_time=0.6)
            vo.wait_until("You built it")
            self.play(Transform(nest.vm.frame, ns.vm.frame), Transform(nest.vm.title, ns.vm.title),
                      Transform(solid[0], ctr_to), Transform(solid[1], ns_solid[1]),
                      Transform(nest.venv, ns.venv), Transform(vlab, ns_vlab), FadeOut(tag_l1), run_time=0.9)
            self.play(FadeIn(lap2, shift=RIGHT * 0.2), FadeIn(img, scale=0.6), FadeIn(l_build, shift=UP * 0.1),
                      run_time=0.6)
            vo.wait_until("pushed it to a registry")
            self.play(FadeIn(hub2), FadeIn(hub_t), Create(r1), run_time=0.6)
            rider = img.copy()
            self.play(travel(rider, r1, run_time=0.7), FadeIn(l_push, shift=UP * 0.1))
            self.play(rider.animate.move_to(hub2.get_center() + UP * 0.05).scale(0.8).set_opacity(0),
                      Indicate(hub2, color=CLOUD, scale_factor=1.08), run_time=0.35)
            self.remove(rider)
            vo.wait_until("and ran it on a VM")
            self.play(Create(r2), run_time=0.4)
            rider2 = img.copy()
            self.play(travel(rider2, r2, run_time=0.7), FadeIn(l_run, shift=UP * 0.1))
            self.play(rider2.animate.move_to(solid[0].get_center()).scale(0.8).set_opacity(0),
                      run_time=0.3)
            self.remove(rider2)
            vo.wait_until("with one command")
            self.play(Indicate(solid[0], color=IMAGE, scale_factor=1.06), pulse(l_run, 1.25), run_time=0.8)

        # ========================================================== 4 · Test yourself: Q1, Q2
        title = label("Test yourself", 36, INK).move_to([0, 3.13, 0]).set_x(-6.4, LEFT)
        t_ul = Line(title.get_corner(DL) + DOWN * 0.1, title.get_corner(DR) + DOWN * 0.1, color=TURN, stroke_width=4)
        q1 = question(1)
        ic1 = icon_glass()
        route_pic = VGroup(nest.vm.frame, nest.vm.title, solid, nest.venv, vlab, lap2, img, hub2, hub_t,
                           l_build, l_push, l_run, r1, r2)

        def demote(q_old, i_old, ic_old, *extra):
            """Question i_old files itself into list row i_old: its words fold into its badge (its icon
            leaves), the badge drops down the left margin, clear of the rows above, and steps into its
            slot, and the row's label unfolds from it. `extra` animations join that last step.
            Returns the row (on the scene)."""
            row = list_row(i_old)
            b = q_old.badge
            self.play(q_old.text.animate.scale(0.04, about_point=b.get_center()).set_opacity(0),
                      FadeOut(ic_old, shift=RIGHT * 0.25), run_time=0.35)
            self.remove(q_old.text, *ic_old.family_members_with_points())
            self.play(b.animate.move_to([b.get_x(), row.badge.get_y(), 0]), run_time=0.35)
            self.play(Transform(b, row.badge), GrowFromPoint(row.text, b.get_center()), *extra, run_time=0.5)
            self.remove(b, row.text)
            self.add(row)
            return row

        def step(q_old, i_old, ic_old, q_new, ic_new):
            """Question i_old becomes list row i_old while question i_old + 1 and its icon come in."""
            return demote(q_old, i_old, ic_old, FadeIn(q_new, shift=UP * 0.15), FadeIn(ic_new, shift=LEFT * 0.2))


        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(route_pic), run_time=0.6)
            self.remove(nest, ns)
            self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.5)
            self.play(Create(t_ul), run_time=0.5)
            vo.wait_until("One:")
            self.play(FadeIn(q1, shift=UP * 0.15), run_time=0.6)
            self.play(FadeIn(ic1, shift=LEFT * 0.2), run_time=0.5)
            cue(self, vo, "an image", -0.4)                 # measured: about 4.3 s (4.69)
            self.play(Indicate(ic1.slabs, color=IMAGE, scale_factor=1.06), run_time=0.45)
            cue(self, vo, "and a container", -0.6)          # measured: about 4.7 s (5.28)
            self.play(FadeIn(ic1.glass, shift=DOWN * 0.5), run_time=0.5)
            ic1.add(ic1.glass)
            cue(self, vo, "and what does dash dash rm", -0.55)   # measured: 5.84 s (6.39)
            rm_span = q_span(q1, "--rm")
            self.play(rm_span.animate.set_color(TURN), run_time=0.4)
            self.play(FadeOut(ic1.glass, shift=UP * 0.4), run_time=0.8)
            ic1.remove(ic1.glass)
            self.play(Indicate(ic1.slabs, color=IMAGE, scale_factor=1.04), run_time=0.6)

            q2, ic2 = question(2), icon_card()
            cue(self, vo, "Two:", -0.4)                       # the fold starts in the pause before it
            rows = [step(q1, 1, ic1, q2, ic2)]
            vo.wait_until("what does our container run")
            self.play(*[TransformFromCopy(ic2.tiles[k], ic2.words[k]) for k in range(2)], run_time=0.9)
            vo.wait_until("and what happens")
            self.play(q_span(q2, "python cli.py").animate.set_color(TURN), FadeIn(ic2.new, shift=LEFT * 0.3),
                      run_time=0.5)
            old = ic2.tiles[1]
            knock = old.copy()
            self.remove(old)
            ic2.tiles.remove(old)
            self.add(knock)
            self.play(ic2.new.animate.move_to(old.get_center()),
                      Rotate(knock, -0.9, about_point=knock.get_corner(DR)), run_time=0.45)
            self.play(knock.animate.shift(DOWN * 1.1 + RIGHT * 0.5).set_opacity(0), run_time=0.5)
            self.remove(knock)
            self.play(Transform(ic2.words[1], ic2.new_word), run_time=0.5)
            ic2.add(ic2.words, ic2.new)

        # ========================================================== 5 · Q3, Q4, Q5
        with self.voiceover(SAY[5]) as vo:
            q3, ic3 = question(3), icon_versions()
            rows.append(step(q2, 2, ic2, q3, ic3))
            cue(self, vo, "Python 3.12", -0.4)              # measured: about 2.3 s (2.70)
            ic3.orange.shift(UP * 0.9).set_opacity(0)
            self.play(ic3.orange.animate.shift(DOWN * 0.9).set_opacity(1), run_time=0.6,
                      rate_func=rate_functions.ease_in_quad)
            self.play(q_span(q3, "python:3.12").animate.set_color(SYSTEM), run_time=0.4)
            cue(self, vo, "so why does python report", -0.4)     # measured: 3.65 s (4.05)
            self.play(GrowFromEdge(ic3.band, LEFT), run_time=0.7)
            self.play(FadeIn(ic3.green, shift=DOWN * 0.6), run_time=0.5)
            cue(self, vo, "or 3.14", -0.95)                 # measured: 6.65 s (7.60)
            self.play(FadeIn(ic3.green2, shift=DOWN * 0.6), run_time=0.5)
            ic3.add(ic3.band, ic3.orange, ic3.green, ic3.green2)

            q4, ic4 = question(4), icon_dominoes()
            cue(self, vo, "Four:", -0.4)                       # the fold starts in the pause before it
            rows.append(step(q3, 3, ic3, q4, ic4))
            self.play(FadeIn(ic4.file, shift=DOWN * 0.3), run_time=0.5)
            cue(self, vo, "which steps rerun", 0.85)        # measured: 11.79 s (10.93)
            fallen = [ic4.dominoes[k] for k in (2, 3)]
            self.play(*[ic4.boxes[k].animate.set_stroke(ERR) for k in (2, 3)], run_time=0.3)
            self.play(LaggedStart(*[Topple(d, -1.2, ERR) for d in fallen], lag_ratio=0.4), run_time=0.9)
            cue(self, vo, "and how would you reorder", 0.8)  # measured: 13.15 s (12.36)
            self.play(Create(ic4.swap[0]), Create(ic4.swap[1]), run_time=0.7)
            ic4.add(ic4.file, ic4.swap)

            q5, ic5 = question(5), icon_platforms()
            cue(self, vo, "Five:", -0.4)                       # the fold starts in the pause before it
            rows.append(step(q4, 4, ic4, q5, ic5))
            vo.wait_until("two ways")
            self.play(LaggedStart(Create(ic5.routes[0]), Create(ic5.routes[1]), lag_ratio=0.5), run_time=1.0)
            self.play(FadeIn(ic5.qs, scale=0.6), run_time=0.4)
            vo.wait_until("run on a default VM")
            self.play(Indicate(ic5.amd, color=CLOUD, scale_factor=1.1), run_time=0.7)
            ic5.add(ic5.routes, ic5.qs)

        # ========================================================== 6 · answers, guide, next
        right_w = RIGHT_R - RIGHT_L
        c1 = card(VGroup(label("Answers:", 28, INK), mono("exercises.md", 26, INK)).arrange(RIGHT, buff=0.2), right_w)
        g_body = VGroup(label("Study guide + every command:", 28, INK), mono(GUIDE_REPO, 22, INK),
                        mono(GUIDE_FILE, 22, INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        c2 = card(g_body, right_w)
        nx = teaser(right_w)
        # the two "where" cards at the top, the L3 card lower down (a separate thought)
        VGroup(c1, c2).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        VGroup(c1, c2).shift(np.array([RIGHT_L - c1.get_left()[0], 3.0 - c1.get_top()[1], 0]))
        nx.shift(np.array([RIGHT_L - nx.get_left()[0], -2.85 - nx.get_bottom()[1], 0]))
        assert nx.get_top()[1] < c2.get_bottom()[1] - 0.25, (nx.get_top(), c2.get_bottom())
        assert nx.body.get_right()[0] < nx.frame.get_right()[0] - 0.2, "teaser wider than its card"
        ul_g = uline(VGroup(g_body[1], g_body[2]), TURN, stroke=3, dy=0.06)
        # the Answers card holds the top right: the tag sits under the Next card, right-aligned with it,
        # from "Next time" until the card leaves in the final fade
        lref_nx = lecture_ref(2, "42–51, 78–79")
        lref_nx.next_to(nx.frame, DOWN, buff=0.15).align_to(nx.frame, RIGHT)
        assert lref_nx.get_bottom()[1] > -3.6, lref_nx.get_bottom()

        with self.voiceover(SAY[6]) as vo:
            rows.append(demote(q5, 5, ic5, FadeIn(c1, shift=UP * 0.15)))
            vo.wait_until("every command")
            self.play(FadeIn(c2, shift=UP * 0.15), run_time=0.5)
            self.play(Create(ul_g), run_time=0.6)
            vo.wait_until("Next time")
            self.play(Create(nx.frame), FadeIn(nx.head, shift=RIGHT * 0.15), FadeIn(lref_nx), run_time=0.6)
            cue(self, vo, "five containers", 0.65)          # measured: 7.37 s (6.70)
            self.play(LaggedStart(*[FadeIn(b, scale=0.6) for b in nx.five], lag_ratio=0.18), run_time=0.8)
            self.play(Create(nx.links), run_time=0.4)
            cue(self, vo, "a working directory", 0.4)       # measured: 9.38 s (8.95)
            self.play(FadeIn(nx.workdir, shift=UP * 0.1), run_time=0.45)
            cue(self, vo, "a non-root user", 0.4)           # measured: 10.80 s (10.38)
            self.play(FadeIn(nx.user, shift=UP * 0.1), run_time=0.45)
            cue(self, vo, "and your laptop's folder", 0.75)  # measured: 12.32 s (11.53)
            self.play(FadeIn(nx.folder, shift=RIGHT * 0.1), FadeIn(nx.ctr), run_time=0.5)
            self.play(Create(nx.arrow), FadeIn(nx.mounted, shift=UP * 0.1), run_time=0.6)
            self.play(FadeIn(nx.ctr_f, shift=RIGHT * 0.3), run_time=0.5)

        self.wait(0.4)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.9)
        self.wait(0.2)
