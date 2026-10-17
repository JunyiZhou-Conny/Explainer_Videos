"""S10 · What's inside the image (extras: docker image ls, docker history, a look inside; V2 real
sizes; V4 coda, two Pythons; V5 coda, no .dockerignore). TRACKER A16 · extra for the whole scene.

Beats (script.md "## S10", one voiceover block each):
 0  Part 1's closing picture returns: the V2 stack (brace "base image", caption
    `python:3.12-slim-bookworm`) and the config card (ENTRYPOINT, CMD), TRACKER A16; a GREY caption
    "part 2 · two extra scenes, then we ship"; on "this scene and the next are extras" the tracker
    caption gets " · extra". The stack shrinks into a small glyph in the free top-right corner (its
    words, brace and the card fade: a full-width terminal leaves no room on the left) as the
    12-row laptop terminal fades in. "First, docker image ls": `docker image ls` (row tag `extra`)
    -> laptop/30 lines 2, 4 squeezed (row 3 never printed), with the GREY tag "Docker Desktop may
    show other columns". `518MB` and `144MB` underline YELLOW as they are said; "at the time": tag
    `at the time of recording`. The terminal shrinks to the 3-row strip. "Content is": the glyph grows
    back into the stack's outline above the strip's 518MB column, and the outlines are copied into a
    small bundle of seven compressed parcels above the 144MB column, "144MB · content"; "travel to
    a registry": a small BLUE registry shelf and a PINK route, a parcel rides up. "disk adds the
    unpacked copy": the shelf goes, the parcels are copied back onto the outlines and unpack into the
    filled slabs; one TEAL brace over stack and bundle reads "518MB · on disk".
 1  The picture parks in the corner glyph; the terminal grows back (12 rows) and types
    `docker history simple-translate` (row tag `extra`) -> laptop/34 lines 2-10, columns CREATED BY,
    SIZE (GREY row tag "columns: CREATED BY · SIZE" above the SIZE column). "Read it bottom-up": a YELLOW arrow climbs beside rows 10 -> 3 and the rows pulse bottom-up.
    Row 7 (`97.5MB`) gets an ORANGE bar on "the apt", row 6 (`250kB`) a GREY bar on "our code",
    row 5 (`125MB`) a GREEN bar on "and uv sync". "The ENV": rows 8-10 and 3-4 turn GREY, row tags
    "config only". The terminal shrinks to the strip (rows 5-7 and their bars); the stack returns
    left of centre and its top three slabs rescale to the real sizes (fat GREEN uv sync, a GREY sliver
    for COPY, its words moving left of it, the ORANGE apt/pip slab); the three sizes are copied up
    from the strip beside their slabs, while the TEAL config card at the right ("config · 0B, no
    layer") lists the 0B rows (three ENV, ENTRYPOINT, CMD, abbreviated); its title pulses on "config
    only"; then the ORANGE slab's name `RUN apt…uv` (S11's name, as in S09's recap) pulses with the
    strip's `apt-get update`; a short hold to read it. GREY `Lecture 2 · slides 34–37, 59`
    (lecture_ref) from "Then docker history" through beat 2 (the history and the stack), left of the
    corner glyph (the glyph blocks the standard spot); it goes with the picture at beat 3.
 2  The picture parks again; the terminal grows back and continues -> laptop/34 "…", lines 14-23
    (rows 11-13 never printed; it scrolls). Row 23 (`debian.sh … 'bookworm'`, `85.3MB`) ORANGE bar on
    "Debian", row 22 (`ENV PATH=/usr/local/bin:…`) PINK bar on "the PATH". The terminal shrinks to
    the strip, keeping rows 18, 22 and 23; the stack returns with S04's list of download sizes
    (3.34MB, 15.97MB, 28.25MB, 249B, "≈ 47.6 MB compressed") at the right, apart from the slabs (its
    sizes pair with none of them). Row 18 (`ENV PYTHON_VERSION=3.12.15`) gets its ORANGE bar in the
    strip on "and Python". The four base slabs grow bottom-up to rows 23, 20, 16, 15 (85.3MB, 9.7MB,
    54.5MB, 16.4kB), each size written beside its slab as it grows, while the list's sizes fade and
    its total becomes the GREY note "≈ 47.6 MB compressed download / → unpacked on disk" right of
    the base (beat 0's content vs disk); a hold on the finished stack.
 3  The picture clears; the terminal grows (12 rows) and shows S09's second run as it was
    in the wide terminal (13.2 wide, 20 pt, 13 rows: the run line fits one row, and the `ls` rows
    need it) (`docker run --rm -ti simple-translate`, `root@1d1fecf6ff8f:/# echo $$`, `1`, `…`); the
    run line pulses on "start a container again"; GREY caption above the terminal "our second run
    from part 1 · yours: docker run --rm -ti simple-translate" on "these are from". The `…` opens up
    just before "There, python": `which python` (line 6) -> line 7 GREEN (why python is 3.15.0);
    on "There, python" `python --version` (line 8) -> line 9 GREEN; on "while the base"
    `/usr/local/bin/python --version` (line 10) -> line 11 ORANGE; on "Most of that"
    `ls /root/.local/share/uv/python` (line 12) -> line 13 GREEN with the GREY row tag "▲ on an
    Intel/AMD machine · Apple Silicon: …linux-aarch64-gnu" in the free row under it, pulsing on
    "this second Python"; the path underlines GREEN on "in uv".
 4  The tag goes and the same run continues: `ls -a /` (line 21) -> lines 22-28 in columns, then the
    prompt. "Beside the system folders": the 19 system folders dim ORANGE; `.git` and `.gitignore`,
    `.vscode`, `README.md`, `Dockerfile` turn YELLOW as they are said; "The COPY line": the five turn
    PINK in PINK boxes; "the whole build context": the rest of the context (`Dockerfile.txt`,
    `cli.py`, `docker-build-push.sh`, `docker-shell.sh`, `pyproject.toml`) turns PINK too, no boxes,
    and the PINK row tag "▲ from the build context" appears at the prompt; `.git` pulses on "your git
    history". `exit` (line 29) -> line 30, the laptop prompt returns.
 5  The terminal fades while `.git` is copied into S06's parcel ("build context", PINK tape), its
    `.git/` item lit YELLOW. "That's a gap": S06's dashed sieve `.dockerignore` hangs under the parcel,
    tag "erratum · no .dockerignore". "In your own projects": a GREY card `.dockerignore` (tag
    "illustration · a file you'd add"); its GREEN lines `.git`, `.venv`, `secrets/` appear as they are
    said; on "dot git" the sieve fills in GREEN and catches `.git/`, which drops onto it. "It matters
    most": a small BLUE registry shelf with the GREY tag "public, soon"; it pulses on "and that's
    soon". Fade to an empty frame.
"""


import re  # noqa: I001  (manim first, then common: common must win)

import numpy as np
from manim import *

from explainer import style as S
from explainer.devops import lecture_ref
from explainer.scene import VoiceScene

from common import (IMAGE, IMAGE_LS, INK, LAPTOP, LAPTOP_DIR, CLOUD, NARRATION, OUTPUT, P_LAPTOP,
                    ROUTE, RUN, STRIP_ROWS, SYSTEM, TURN, VENV, ConfigCard, LayerStack, Parcel, Sieve,
                    attach, bare_prompt, beside, box, capture, cols, erratum_tag, glyph_range,
                    illustration_tag, istep, label, laptop_term, mb_height, mono, mono_line, pin,
                    recorded_tag, resize, row_tag, shelf_glyph, squeeze, substring, tag, track,
                    tracker_a, type_cmd, under, wide_term)

SAY = NARRATION["S10"]

# ------------------------------------------------------------------ real outputs (file line numbers)
C30 = capture("30", LAPTOP_DIR)                          # laptop/30-image-ls.txt
assert C30.cmd == IMAGE_LS, C30.cmd
LS_OUT = squeeze(C30.at(2, 4))                           # header + our image (row 3 never printed)
assert LS_OUT[1].startswith("simple-translate:latest") and LS_OUT[1].endswith("518MB         144MB"), LS_OUT

C34 = capture("34", LAPTOP_DIR)                          # laptop/34-history.txt
HISTORY = C34.cmd
assert HISTORY == "docker history simple-translate", HISTORY
_FILE = [*range(2, 11), *range(14, 24)]                  # never rows 11-13 (capture-only)
H = dict(zip(_FILE, cols(C34.at((2, 10), (14, 23)), ["CREATED BY", "SIZE"])))
SIZE = {n: H[n].split()[-1] for n in _FILE[1:]}
assert (SIZE[5], SIZE[6], SIZE[7]) == ("125MB", "250kB", "97.5MB"), SIZE
assert (SIZE[23], SIZE[20], SIZE[16], SIZE[15]) == ("85.3MB", "9.7MB", "54.5MB", "16.4kB"), SIZE
assert all(SIZE[n] == "0B" for n in (3, 4, 8, 9, 10)), SIZE
assert H[18].startswith("ENV PYTHON_VERSION=3.12.15") and H[22].startswith("ENV PATH=/usr/local/bin:")
assert "'bookworm'" in H[23], H[23]

C33 = capture("33", LAPTOP_DIR)                          # laptop/33-inside.txt (S09's second run)
assert C33.cmd == RUN, C33.cmd
P33, _echo = C33.istep(4)
assert _echo == "echo $$" and C33.at(5) == ["1"], C33.raw[:5]
assert C33.istep(8)[1] == "python --version" and C33.at(9) == ["Python 3.15.0"]
assert C33.istep(10)[1] == "/usr/local/bin/python --version" and C33.at(11) == ["Python 3.12.15"]
assert C33.istep(12)[1] == "ls /root/.local/share/uv/python", C33.line(12)
assert C33.istep(21)[1] == "ls -a /" and C33.istep(29)[1] == "exit", (C33.line(21), C33.line(29))
LS_ROOT = C33.at((22, 28))
UV_DIR = "/root/.local/share/uv/python"

# ------------------------------------------------------------------ the picture's values
ENT = '["/bin/bash"]'                                      # S09's card tiles
CMD_IMG = '["-c", "source … && exec bash"]'
TEXTS = [None] * 4 + ["RUN apt…uv", "COPY . ./", "RUN uv sync"]   # the solution's apt+pip step (S11: [2/4] RUN apt…uv)
TEXTS_S09 = TEXTS                                        # part 1's picture: S09's recap names it the same
FILLS = [SYSTEM] * 4 + [SYSTEM, LAPTOP, VENV]
H_S09 = [0.15] * 4 + [0.46, 0.46, 0.8]                   # part 1's stack (S09's recap)
TOP_MB = [97.5, 0.25, 125.0]                             # rows 7, 6, 5
BASE_MB = [85.3, 9.7, 54.5, 0.0164]                      # rows 23, 20, 16, 15
H_TOP = [0.15] * 4 + [mb_height(x) for x in TOP_MB]
H_ALL = [mb_height(x) for x in BASE_MB + TOP_MB]
TOP_SIZES = [SIZE[7], SIZE[6], SIZE[5]]
BASE_SIZES = [SIZE[23], SIZE[20], SIZE[16], SIZE[15]]
S04_SIZES = ["3.34MB", "15.97MB", "28.25MB", "249B"]       # S04's compressed downloads (laptop/09)
CONFIG_ROWS = ["ENV DEBIAN_FRONTEND=…", "ENV LANG=C.UTF-8", "ENV PYTHONUNBUFFERED=1",
               'ENTRYPOINT ["/bin/bash"]', 'CMD ["-c", "source …"]']   # Dockerfile order, abbreviated
OTHER_CTX = ["Dockerfile.txt", "cli.py", "docker-build-push.sh", "docker-shell.sh", "pyproject.toml"]
# ^ the rest of the build context (laptop/05 + the copied Dockerfile); .venv, uv.lock: made by uv sync
SYSTEM_DIRS = {"bin", "boot", "dev", "etc", "home", "lib", "lib64", "media", "mnt", "opt", "proc",
               "root", "run", "sbin", "srv", "sys", "tmp", "usr", "var"}

# ------------------------------------------------------------------ layout
OPEN_X, OPEN_FLOOR = -3.0, -0.45      # part 1's closing picture (S09)
B0_X, B0_FLOOR = 0.6, -1.1            # beat 0: the stack above the strip's 518MB column
BUNDLE_X, BUNDLE_Y = 4.9, -0.75       # beat 0: the bundle above the 144MB column
SX, SFLOOR = -3.0, -1.15              # beats 1-2: the stack over the strip (top at 2.59 when full)
THUMB_SC, THUMB_X, THUMB_Y0 = 0.3, 5.6, 2.36   # the parked stack: top-right corner, no words
STACK_W = 3.4


# ------------------------------------------------------------------ helpers
def lead(vo, phrase: str, early: float) -> None:
    """Wait until `early` seconds before `phrase` is spoken."""
    dt = vo.time_until(phrase) - early
    if dt > 1 / 60:
        vo.scene.wait(dt)


def make_stack(x: float, floor_y: float, heights, texts=TEXTS):
    """The V2 stack with these slab heights (bottom-up): four unlabelled ORANGE base slabs, then
    `RUN apt…uv` (as in S09's recap: TEXTS_S09 == TEXTS), `COPY . ./`, `RUN uv sync`; a
    slab too thin for its words has them just left of the stack (as LayerStack.restack does). Not
    added. -> (stack, slabs, base brace)"""
    st = LayerStack(stack_w=STACK_W)
    st.floor.move_to([x, floor_y, 0])
    slabs = []
    for txt, fill, h in zip(texts, FILLS, heights):
        s = st.make(txt, fill, h)
        if s.text is not None and h < s.text.height + 0.12:
            s.text.move_to(s.box.get_left() + LEFT * (0.15 + s.text.width / 2))
        slabs.append(s)
    for s in slabs:
        st.slabs.add(s)
    st._pending.clear()
    return st, slabs, st.brace(slabs[:4], "base image")


def first_half(a: float) -> float:
    """Rate function done by halfway: what leaves before the rest arrives."""
    return smooth(min(1.0, a / 0.5))


def last_part(a: float) -> float:
    """Rate function that starts at 60 %: what arrives once a moving object has passed its spot."""
    return smooth(max(0.0, (a - 0.6) / 0.4))


def words(slabs) -> VGroup:
    return VGroup(*[s.text for s in slabs if s.text is not None])


def thumb(heights) -> VGroup:
    """The parked stack: the same slabs at THUMB_SC, no words (nothing under 20 pt)."""
    g, y = VGroup(), THUMB_Y0
    for fill, h in zip(FILLS, heights):
        hh = h * THUMB_SC
        r = RoundedRectangle(width=STACK_W * THUMB_SC, height=hh, corner_radius=min(0.025, hh / 2.5),
                             stroke_color=IMAGE, stroke_width=1.8).set_fill(fill, 0.35)
        g.add(r.move_to([THUMB_X, y + hh / 2, 0]))
        y += hh + 0.015
    return g


def via_below(drop_first: bool, dy: float = 0.8):
    """A path_func for the corner glyph's moves while the lecture tag sits just left of it: straight,
    but through the glyph's spot `dy` lower, so the moving stack passes under the tag, never over it.
    drop_first: the glyph drops out of the corner first (unpark); else it rises into it last (park)."""
    k = 0.25 if drop_first else 0.75

    def f(p0, p1, a):
        mid = (p0 if drop_first else p1) + DOWN * dy
        if a < k:
            return p0 + (mid - p0) * (a / k)
        return mid + (p1 - mid) * ((a - k) / (1 - k))
    return f


def boxes_of(slabs) -> VGroup:
    return VGroup(*[s.box.copy() for s in slabs])


def slab_mid(slab) -> np.ndarray:
    return slab.box.get_center()


def size_at(s: str, slab, color, x: float | None = None) -> Text:
    """A slab's size, written just right of the stack at the slab's height."""
    t = mono(s, 20, color)
    left = slab.box.get_right()[0] + 0.2 if x is None else x
    return t.move_to([left + t.width / 2, slab_mid(slab)[1], 0])


def row_bar(row, color, opacity: float = 0.24) -> Rectangle:
    """A translucent bar the height of terminal row `row`, behind its glyphs."""
    g = row.glyphs
    return Rectangle(width=g.width + 0.16, height=row.strut.height * 0.92, stroke_width=0) \
        .set_fill(color, opacity).move_to([g.get_center()[0], row.strut.get_center()[1], 0])


def attach_back(scene, line, mob):
    """attach(), but drawn behind the row's glyphs."""
    scene.remove(mob)
    line.add_to_back(mob)
    scene.add(line)
    return mob


def make_bundle() -> VGroup:
    """Seven small compressed parcels (one per layer, filled by what it holds) in a TEAL strap.
    .parcels (bottom row: the four base layers) .strap"""
    parcels = VGroup(*[RoundedRectangle(width=0.36, height=0.26, corner_radius=0.04, stroke_color=IMAGE,
                                        stroke_width=2).set_fill(f, 0.45) for f in FILLS])
    low = VGroup(*parcels[:4]).arrange(RIGHT, buff=0.06)
    high = VGroup(*parcels[4:]).arrange(RIGHT, buff=0.06)
    VGroup(high, low).arrange(DOWN, buff=0.06)
    strap = RoundedRectangle(width=low.width + 0.22, height=0.26 * 2 + 0.06 + 0.2, corner_radius=0.1,
                             stroke_color=IMAGE, stroke_width=2.5)
    g = VGroup(strap, parcels)
    strap.move_to(VGroup(low, high))
    g.move_to([BUNDLE_X, BUNDLE_Y, 0])
    g.parcels, g.strap = parcels, strap
    return g


def two(a: str, b: str, color=IMAGE, size: float = 22) -> VGroup:
    """'518MB · on disk': a TEAL mono value and a GREY word."""
    return VGroup(mono(a, size, color), label(b, size, S.GREY)).arrange(RIGHT, buff=0.18)


def config_list() -> VGroup:
    """The config card of the 0B rows: TEAL frame, 'config' + '0B · no layer', one mono row each."""
    title = VGroup(label("config", 22, IMAGE), label("· 0B, no layer", 22, S.GREY)).arrange(RIGHT, buff=0.15)
    rows = VGroup(*[mono(r, 20, INK) for r in CONFIG_ROWS]).arrange(DOWN, aligned_edge=LEFT, buff=0.17)
    body = VGroup(title, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
    frame = box(body.width + 0.5, body.height + 0.45, IMAGE, fill_opacity=0.06)
    body.move_to(frame)
    g = VGroup(frame, body)
    g.frame, g.title, g.rows = frame, title, rows
    return g


def s04_list() -> VGroup:
    """S04's four compressed download sizes, right-aligned, with its rule and total."""
    sz = VGroup(*[mono(s, 20, SYSTEM) for s in S04_SIZES]).arrange(DOWN, buff=0.12, aligned_edge=RIGHT)
    rule = Line(sz.get_corner(DR) + np.array([0.05, -0.1, 0]), sz.get_corner(DR) + np.array([-1.3, -0.1, 0]),
                color=SYSTEM, stroke_width=2)
    total = label("≈ 47.6 MB compressed", 22, SYSTEM).next_to(rule, DOWN, buff=0.12).align_to(sz, RIGHT)
    return VGroup(sz, rule, total)


def replay(t, items) -> VGroup:
    """Put already-typed lines into terminal t at once (S09's run, shown again): items are
    (text, prompt) for a typed line, (text, None) for output. Returns the new rows (not shown)."""
    new = VGroup()
    for text, prompt in items:
        if prompt:
            p = prompt + " "
            rows = t.fold(p + text, first_prefix=len(p))
            colors = t._prompt_colors(prompt)
            lines = [mono_line(r, t.size, INK, t2c=colors if k == 0 else None) for k, r in enumerate(rows)]
        else:
            lines = [mono_line(text, t.size, OUTPUT)]
        for ln in lines:
            t._place(ln, len(t.lines))
            t.lines.add(ln)
            new.add(ln)
    return new


def tokens(row) -> dict:
    """{name: glyphs} for the entries of an `ls` row in columns."""
    return {m.group(0): glyph_range(row, m.start(), m.end()) for m in re.finditer(r"\S+", row.text)}


def widen(scene, t, rows: int, prompt: str, run_time: float = 0.7, keep: int | None = None):
    """The 22 pt terminal becomes the wide one (13.2 wide, 20 pt), keeping its last lines (at most
    `keep`; scaled to 20 pt, so they read the same) and its bottom edge. Returns the new terminal
    (in the scene)."""
    w = wide_term(rows, prompt=prompt)
    olds = list(t.lines)
    n = min(rows, len(olds)) if keep is None else min(rows, keep, len(olds))
    keep = olds[len(olds) - n:]
    gone = olds[:len(olds) - n]
    if gone:
        scene.play(FadeOut(VGroup(*gone)), run_time=0.2)
    anims = [Transform(t.box, w.box), Transform(t.bar, w.bar), t.dots.animate.move_to(w.dots),
             t.title.animate.move_to(w.title)]
    k = w.size / t.size
    for i, ln in enumerate(keep):
        ln.generate_target()
        ln.target.scale(k)
        ln.target.shift(w._slot(i) - ln.target.strut.get_corner(UL))
        anims.append(MoveToTarget(ln))
    scene.play(*anims, run_time=run_time)
    scene.remove(*t.get_family())
    w.remove(w.lines)
    w.lines = VGroup(*keep)
    w.add(w.lines)
    scene.add(w)
    return w


# ------------------------------------------------------------------ the scene
class InsideTheImage(VoiceScene):
    def park(self, st, slabs, *extra, run_time: float = 0.6, also=(), path_func=None) -> VGroup:
        """The stack's slabs shrink into the corner glyph (its words, braces and `extra` fade), with
        `also`; the stack leaves the scene. Returns the glyph."""
        glyph = thumb([s.box.height for s in slabs])
        ghost = boxes_of(slabs)
        self.add(ghost)
        self.play(ReplacementTransform(ghost, glyph, path_func=path_func), FadeOut(words(slabs)),
                  *[FadeOut(m) for m in extra], *also, run_time=run_time)
        self.unstack(st)
        return glyph

    def unpark(self, glyph, st, slabs, *extra, run_time: float = 0.6, also=(), path_func=None) -> None:
        """The corner glyph grows back into stack `st` (its words and `extra` fade in), with `also`."""
        ghost = boxes_of(slabs)
        ws = words(slabs)
        ex = VGroup(*extra)
        self.play(ReplacementTransform(glyph, ghost, path_func=path_func), *also, run_time=run_time)
        self.play(FadeIn(ws), FadeIn(ex), run_time=0.3)
        self.remove(ghost, ws, ex)
        self.add(st, *extra)

    def unstack(self, st) -> None:
        """Take a stack off the scene, including the parts animations split out of it."""
        self.remove(*st.get_family())

    def construct(self):
        assert len(SAY) == 6, f"S10 has {len(SAY)} SAY lines; this scene times 6"

        tr = tracker_a(16)
        t = laptop_term(12)

        # ========================================================== 0 · image ls: disk and content
        st0, slabs0, br0 = make_stack(OPEN_X, OPEN_FLOOR, H_S09, TEXTS_S09)
        base_name = mono("python:3.12-slim-bookworm", 20, S.GREY).next_to(st0.floor, DOWN, buff=0.15)
        card9 = ConfigCard(rows=("ENTRYPOINT", "CMD"), card_w=6.0, inline=False)
        card9.shift(np.array([6.3 - card9.frame.get_right()[0], 2.25 - card9.frame.get_top()[1], 0]))
        card9.place("ENTRYPOINT", card9.tile(ENT))
        card9.place("CMD", card9.tile(CMD_IMG))
        part2 = label("part 2 · two extra scenes, then we ship", 26, S.GREY).move_to([1.4, -2.35, 0])

        st1, slabs1, br1 = make_stack(B0_X, B0_FLOOR, H_S09, TEXTS_S09)
        outline = VGroup(*[s.box.copy().set_fill(opacity=0) for s in slabs1])
        bundle = make_bundle()
        b_label = two("144MB", "content").next_to(bundle, UP, buff=0.22)
        shelf = shelf_glyph(1.1).move_to([BUNDLE_X, 1.5, 0])
        shelf_l = label("registry", 20, CLOUD).next_to(shelf, LEFT, buff=0.2)
        up = Arrow(b_label.get_top() + UP * 0.05, shelf.get_bottom() + DOWN * 0.04, buff=0, color=ROUTE,
                   stroke_width=4, tip_length=0.18, max_tip_length_to_length_ratio=0.3)
        rider = bundle.parcels[6].copy()

        card9_all = card9.everything()       # ONE wrapper: faded in and out as the same object

        with self.voiceover(SAY[0]) as vo:
            opening = VGroup(*slabs0, br0, base_name)
            self.play(FadeIn(tr, shift=DOWN * 0.1), FadeIn(opening), FadeIn(card9_all, shift=LEFT * 0.15),
                      run_time=0.8)
            self.remove(opening)
            self.add(st0, br0, base_name)
            self.play(FadeIn(part2, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("this scene and")
            self.play(track(tr, 16, extra=True), Indicate(part2, color=INK, scale_factor=1.06), run_time=0.7)
            lead(vo, "First, docker", 1.1)
            g = self.park(st0, slabs0, br0, base_name, card9_all, part2)
            self.remove(*card9_all.get_family())
            self.play(FadeIn(t), run_time=0.4)
            vo.wait_until("First, docker")
            c_ls = type_cmd(self, t, IMAGE_LS, 0.7)
            pin(self, c_ls, beside(row_tag("extra"), c_ls), run_time=0.25)
            out = t.print(self, LS_OUT, run_time=0.4)
            data = out[1]
            dd = tag("Docker Desktop may show other columns", S.GREY)
            dd.next_to(data.strut, DOWN, buff=1.15).align_to(data.strut, LEFT)
            self.play(FadeIn(dd, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("518")
            g518 = substring(data, "518MB")
            u518 = under(g518, TURN)
            self.play(Create(u518), Indicate(g518, color=TURN, scale_factor=1.25), run_time=0.7)
            attach(self, data, u518)
            vo.wait_until("144")
            g144 = substring(data, "144MB")
            u144 = under(g144, TURN)
            self.play(Create(u144), Indicate(g144, color=TURN, scale_factor=1.25), run_time=0.7)
            attach(self, data, u144)
            vo.wait_until("at the time")
            rec = recorded_tag()
            rec.next_to(data.strut, DOWN, buff=0.35).align_to(g144, RIGHT)
            self.play(FadeIn(rec, shift=UP * 0.1), run_time=0.4)
            lead(vo, "Content is", 1.1)
            self.play(FadeOut(rec), FadeOut(dd), run_time=0.3)
            resize(self, t, STRIP_ROWS, keep=3, run_time=0.7)
            vo.wait_until("Content is")
            self.play(ReplacementTransform(g, outline), run_time=0.6)
            self.play(TransformFromCopy(outline, bundle.parcels), Create(bundle.strap), run_time=0.8)
            self.play(FadeIn(b_label, shift=UP * 0.1), Indicate(g144, color=TURN, scale_factor=1.2), run_time=0.6)
            vo.wait_until("travel to")
            self.play(FadeIn(shelf, shift=DOWN * 0.1), FadeIn(shelf_l), GrowArrow(up), run_time=0.6)
            rider.move_to(up.get_start())
            self.play(rider.animate.move_to(shelf.get_center()).scale(0.7), run_time=0.6)
            self.play(FadeOut(rider), Indicate(shelf, color=CLOUD, scale_factor=1.1), run_time=0.4)
            vo.wait_until("disk adds")
            fills = boxes_of(slabs1)
            self.play(FadeOut(VGroup(shelf, shelf_l, up)),
                      TransformFromCopy(bundle.parcels, fills), run_time=0.9)
            self.remove(outline, fills)
            self.add(st1)
            self.play(FadeIn(words(slabs1)), FadeIn(br1), run_time=0.3)
            both = Brace(VGroup(*[s.box for s in slabs1], bundle), direction=UP, color=IMAGE, buff=0.15)
            disk = two("518MB", "on disk").next_to(both, UP, buff=0.12)
            self.play(GrowFromCenter(both), FadeIn(disk, shift=DOWN * 0.1),
                      Indicate(g518, color=TURN, scale_factor=1.2), run_time=0.7)
        self.wait(1.0)                       # disk = content + the unpacked copy: a moment to look

        # ========================================================== 1 · docker history: our three layers
        st2, slabs2, br2 = make_stack(SX, SFLOOR, H_S09, TEXTS_S09)
        _, top2, _ = make_stack(SX, SFLOOR, H_TOP)                     # where the slabs land (layout only)
        card = config_list()
        card.move_to([6.3 - card.width / 2, 0.45, 0])
        # the parked glyph holds the top-right spot: the tag sits just left of it, centred on it, through
        # beat 2 (it stays when the glyph leaves; beat 2's glyph has the same left edge)
        lref = lecture_ref(2, "34–37, 59")
        g_at = thumb([s.box.height for s in slabs1])
        lref.move_to([g_at.get_left()[0] - 0.12 - lref.width / 2, g_at.get_center()[1], 0])
        assert lref.get_left()[0] > tr.caption.get_right()[0] + 0.1, (lref.get_left(), tr.caption.get_right())
        t12 = laptop_term(12).get_top()[1]                           # the 12-row terminal of beats 1-2
        assert lref.get_bottom()[1] > t12 + 0.1, (lref.get_bottom(), t12)

        with self.voiceover(SAY[1]) as vo:
            vo.wait_until("Then docker history")
            g = self.park(st1, slabs1, br1, bundle, b_label, both, disk, also=[FadeIn(lref, shift=LEFT * 0.1)],
                          path_func=via_below(False))
            resize(self, t, 12, run_time=0.7)
            c_h = type_cmd(self, t, HISTORY, 0.9)                    # folds: 66 characters with the prompt
            c_h_last = c_h.rows[-1] if hasattr(c_h, "rows") else c_h
            pin(self, c_h_last, beside(row_tag("extra"), c_h_last), run_time=0.25)
            rows = t.print(self, [H[n] for n in range(2, 11)], run_time=0.8, lag=0.08)
            R = dict(zip(range(2, 11), rows))
            colcap = row_tag("columns: CREATED BY · SIZE")         # yours has five: IMAGE … COMMENT
            size_r = max(R[n].glyphs.get_right()[0] for n in range(2, 11))
            colcap.move_to([size_r - colcap.width / 2, c_h_last.strut.get_center()[1], 0])
            pin(self, c_h_last, colcap, run_time=0.4)
            vo.wait_until("Read it")
            x_arrow = max(R[n].glyphs.get_right()[0] for n in range(3, 11)) + 0.45
            climb = Arrow([x_arrow, R[10].strut.get_center()[1], 0], [x_arrow, R[3].strut.get_center()[1], 0],
                          buff=0, color=TURN, stroke_width=5, tip_length=0.22, max_tip_length_to_length_ratio=0.1)
            bu = label("bottom-up", 22, TURN).next_to(climb.get_start(), RIGHT, buff=0.18)
            self.play(GrowArrow(climb), FadeIn(bu, shift=UP * 0.1), run_time=1.0)
            self.play(LaggedStart(*[Indicate(R[n].glyphs, color=INK, scale_factor=1.03) for n in range(10, 2, -1)],
                                  lag_ratio=0.3), run_time=2.2)
            for n, col, phrase, txt in ((7, SYSTEM, "the apt", SYSTEM), (6, LAPTOP, "our code", INK),
                                        (5, VENV, "and uv sync", VENV)):
                vo.wait_until(phrase)
                bar = row_bar(R[n], col)
                gs = substring(R[n], SIZE[n])
                self.play(FadeIn(bar), gs.animate.set_color(txt), run_time=0.4)
                attach_back(self, R[n], bar)
                self.play(Indicate(gs, color=txt, scale_factor=1.3), run_time=0.6)
                self.add(R[n])
            vo.wait_until("The ENV")
            zero = [R[n] for n in (8, 9, 10, 3, 4)]
            co1 = beside(row_tag("config only"), R[4], buff=0.4)
            co2 = beside(row_tag("config only"), R[9], buff=0.4)
            self.play(FadeOut(VGroup(climb, bu)), run_time=0.3)
            self.play(LaggedStart(*[r.glyphs.animate.set_color(S.GREY) for r in zero], lag_ratio=0.25),
                      FadeIn(co1, shift=LEFT * 0.1), FadeIn(co2, shift=LEFT * 0.1), run_time=1.0)
            attach(self, R[4], co1)
            attach(self, R[9], co2)
            lead(vo, "config only", 2.5)     # the card's rows land on "zero bytes: config only"
            resize(self, t, STRIP_ROWS, keep=[R[5], R[6], R[7]], run_time=0.7)
            self.unpark(g, st2, slabs2, br2, also=[FadeIn(card.frame), FadeIn(card.title, shift=UP * 0.1)],
                        path_func=via_below(True))
            sizes2 = [size_at(s, top2[4 + i], c) for i, (s, c) in
                      enumerate(zip(TOP_SIZES, (SYSTEM, LAPTOP, VENV)))]
            src = [substring(R[n], SIZE[n]) for n in (7, 6, 5)]
            self.play(*st2.restack(H_TOP), *[TransformFromCopy(a, b) for a, b in zip(src, sizes2)],
                      LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in card.rows], lag_ratio=0.2), run_time=1.1)
            self.play(Indicate(card.title, color=IMAGE, scale_factor=1.12), run_time=0.7)
            g_apt = substring(R[7], "apt-get update")               # the slab's name is this step's
            self.play(Indicate(slabs2[4].text, color=SYSTEM, scale_factor=1.1),
                      Indicate(g_apt, color=SYSTEM, scale_factor=1.15), run_time=0.8)
            self.add(R[7])
        self.wait(1.0)                       # the card: a moment to read it

        # ========================================================== 2 · the base image's own rows
        st3, slabs3, br3 = make_stack(SX, SFLOOR, H_TOP)
        sizes3 = [size_at(s, slabs3[4 + i], c) for i, (s, c) in enumerate(zip(TOP_SIZES, (SYSTEM, LAPTOP, VENV)))]
        lst = s04_list()                     # a panel apart from the slabs: its sizes pair with none of them
        lst.move_to([4.6 - lst.width / 2, -0.3, 0])
        unz = VGroup(label("≈ 47.6 MB compressed download", 20, S.GREY), label("→ unpacked on disk", 20, S.GREY))
        unz.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        assert len(unz[0]) == len(lst[2]) + len("download"), (len(unz[0]), len(lst[2]))   # glyphs, no spaces

        with self.voiceover(SAY[2]) as vo:
            g = self.park(st2, slabs2, br2, card, *sizes2, path_func=via_below(False))
            resize(self, t, 12, run_time=0.7)
            rows2 = t.print(self, ["…"] + [H[n] for n in range(14, 24)], run_time=0.8, lag=0.06)
            R2 = dict(zip(range(14, 24), rows2[1:]))
            marks = ((23, SYSTEM, "Debian", "bookworm"), (22, ROUTE, "the PATH", "/usr/local/bin"),
                     (18, SYSTEM, "and Python", "3.12.15"))
            for k, (n, col, phrase, sub) in enumerate(marks):
                vo.wait_until(phrase)
                bar = row_bar(R2[n], col)
                gs = substring(R2[n], sub)
                self.play(FadeIn(bar), gs.animate.set_color(col), run_time=0.4)
                attach_back(self, R2[n], bar)
                self.play(Indicate(gs, color=col, scale_factor=1.2), run_time=0.6)
                self.add(R2[n])
                if k == 1:          # the strip keeps rows 18, 22, 23; Python is marked there
                    resize(self, t, STRIP_ROWS, keep=[R2[18], R2[22], R2[23]], run_time=0.7)
                    self.unpark(g, st3, slabs3, br3, *sizes3, also=[FadeIn(lst, shift=LEFT * 0.15)],
                                path_func=via_below(True))
            base_lab = []
            _, full, _ = make_stack(SX, SFLOOR, H_ALL)
            unz.move_to([size_at(BASE_SIZES[0], full[0], SYSTEM).get_right()[0] + 0.5 + unz.width / 2,
                         VGroup(*[s_.box for s_ in full[:4]]).get_center()[1], 0])
            for k in range(4):
                hs = H_ALL[:k + 1] + H_TOP[k + 1:]
                _, ref, new_br = make_stack(SX, SFLOOR, hs)
                lab = size_at(BASE_SIZES[k], ref[k], SYSTEM)
                extra = []
                if k == 0:      # S04's compressed list becomes the note: these are the same layers, unpacked
                    n_tot = len(lst[2])     # its total is the note's first words: each glyph moves, none morphs
                    kept, more = VGroup(*unz[0][:n_tot]), VGroup(*unz[0][n_tot:])
                    extra = [FadeOut(VGroup(lst[0], lst[1]), rate_func=first_half), ReplacementTransform(lst[2], kept),
                             FadeIn(more, shift=RIGHT * 0.1, rate_func=last_part),
                             FadeIn(unz[1], shift=RIGHT * 0.1, rate_func=last_part)]
                moves = [m.animate.set_y(ref[4 + i].box.get_center()[1]) for i, m in enumerate(sizes3)]
                moves += [m.animate.set_y(ref[i].box.get_center()[1]) for i, m in enumerate(base_lab)]
                self.play(*st3.restack(hs), Transform(br3, new_br), FadeIn(lab, shift=LEFT * 0.1), *moves, *extra,
                          run_time=0.8 if k == 0 else 0.5)
                if k == 0:
                    self.remove(kept, more, unz[1])
                    self.add(unz)
                base_lab.append(lab)
        self.wait(1.6)                       # the full stack, real sizes, the note: a moment to read

        # ========================================================== 3 · inside: two Pythons
        cap = VGroup(label("our second run from part 1 · yours:", 20, S.GREY), mono(RUN, 20, S.GREY))
        cap.arrange(RIGHT, buff=0.15).move_to([0, 2.5, 0])
        picture3 = VGroup(*slabs3, br3, *sizes3, *base_lab, unz)

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(picture3), FadeOut(lref), run_time=0.5)      # the history's picture goes
            self.unstack(st3)
            # the wide terminal now (13 rows): the run line fits one row, and a row is left for the tag
            w = widen(self, t, 13, P_LAPTOP, keep=0)
            run_rows = replay(w, [(RUN, P_LAPTOP), ("echo $$", P33), ("1", None), ("…", None)])
            assert len(run_rows) == 4, [r.text for r in run_rows]
            self.play(LaggedStart(*[FadeIn(r) for r in run_rows], lag_ratio=0.15), run_time=0.7)
            dots = run_rows[-1]
            w.set_prompt(P33)
            vo.wait_until("start a container")
            self.play(Indicate(run_rows[0].glyphs, color=IMAGE, scale_factor=1.04), run_time=0.8)
            vo.wait_until("these are from")
            self.play(FadeIn(cap, shift=DOWN * 0.1), run_time=0.5)
            lead(vo, "There, python", 1.0)   # the … opens up: which python (lines 6-7) first
            self.play(FadeOut(dots), run_time=0.2)
            w.lines.remove(dots)
            istep(self, w, C33.line(6), 0.4)
            w.print(self, [(C33.line(7), VENV)], run_time=0.25)
            vo.wait_until("There, python")
            istep(self, w, C33.line(8), 0.6)
            v315 = w.print(self, [(C33.line(9), VENV)], run_time=0.3)[0]
            self.play(Indicate(v315.glyphs, color=VENV, scale_factor=1.15), run_time=0.6)
            vo.wait_until("while the base")
            istep(self, w, C33.line(10), 0.9)
            v312 = w.print(self, [(C33.line(11), SYSTEM)], run_time=0.3)[0]
            self.play(Indicate(v312.glyphs, color=SYSTEM, scale_factor=1.15), run_time=0.6)
            vo.wait_until("Most of that")
            c_uv = istep(self, w, C33.line(12), 0.9)
            uv_out = w.print(self, [(C33.line(13), VENV)], run_time=0.3)[0]
            arm = row_tag([("▲ on an Intel/AMD machine · Apple Silicon:", "label"), ("…linux-aarch64-gnu", "mono")])
            arm.move_to([uv_out.strut.get_left()[0] + arm.width / 2, uv_out.strut.get_center()[1] - w.pitch, 0])
            self.play(FadeIn(arm, shift=UP * 0.1), run_time=0.4)
            self.wait(0.2)
            self.play(Indicate(uv_out.glyphs, color=VENV, scale_factor=1.06), run_time=0.9)
            vo.wait_until("in uv")
            g_uv = substring(c_uv, UV_DIR)
            u_uv = under(g_uv, VENV)
            self.play(Create(u_uv), g_uv.animate.set_color(VENV), run_time=0.6)
            attach(self, c_uv, u_uv)

        # ========================================================== 4 · ls -a /: the whole build context
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(arm), run_time=0.25)                   # its row takes the next command
            istep(self, w, C33.line(21), 0.4)
            ls = w.print(self, LS_ROOT, run_time=0.6, lag=0.08)
            prompt_row = bare_prompt(self, w)
            toks, row_of = {}, {}
            for r in ls:
                for name, gl in tokens(r).items():
                    toks[name], row_of[name] = gl, r
            vo.wait_until("Beside the")
            sysg = VGroup(*[toks[d] for d in sorted(SYSTEM_DIRS)])
            self.play(sysg.animate.set_color(SYSTEM).set_opacity(0.6), run_time=0.7)
            for r in ls:
                self.add(r)
            lit = {}
            for phrase, names in (("the hidden git", [".git", ".gitignore"]), ("the editor", [".vscode"]),
                                  ("the README", ["README.md"]), ("and your Dockerfile", ["Dockerfile"])):
                vo.wait_until(phrase)
                grp = VGroup(*[toks[n] for n in names])
                self.play(grp.animate.set_color(TURN), run_time=0.3)
                self.play(Indicate(grp, color=TURN, scale_factor=1.2), run_time=0.5)
                for n in names:
                    lit[n] = toks[n]
            for r in ls:
                self.add(r)
            vo.wait_until("The COPY")
            frames = {n: SurroundingRectangle(gl, color=ROUTE, buff=0.06, stroke_width=2.5, corner_radius=0.05)
                      for n, gl in lit.items()}
            ctx = beside(row_tag("▲ from the build context", ROUTE), prompt_row, buff=0.4)
            self.play(*[gl.animate.set_color(ROUTE) for gl in lit.values()],
                      *[Create(f) for f in frames.values()], run_time=0.7)
            for n, f in frames.items():
                attach(self, row_of[n], f)
            for r in ls:
                self.add(r)
            vo.wait_until("the whole")       # the rest of the context turns PINK too (no boxes)
            rest = VGroup(*[toks[n] for n in OTHER_CTX])
            self.play(rest.animate.set_color(ROUTE), FadeIn(ctx, shift=LEFT * 0.1), run_time=0.6)
            for r in ls:
                self.add(r)
            vo.wait_until("your git")
            self.play(Indicate(VGroup(lit[".git"], frames[".git"]), color=ROUTE, scale_factor=1.3), run_time=0.8)
            self.play(FadeOut(ctx), run_time=0.25)
            vo.wait_until("Type exit")
            istep(self, w, C33.line(29), 0.3)
            w.print(self, C33.at(30), run_time=0.2)
            w.set_prompt(P_LAPTOP)
            bare_prompt(self, w)

        # ========================================================== 5 · no .dockerignore (erratum)
        parcel = Parcel((".git/", "cli.py", "Dockerfile"), extra=7)
        parcel.scale(1.2).move_to([-3.1, 0.95, 0])                  # names 24 pt
        git_item = parcel.items[".git/"]
        git_item.glyph.set_stroke(TURN).set_fill(TURN, 0.4)
        git_item.name_text.set_color(TURN)
        sieve = Sieve(parcel.frame.width, 0.62)
        mesh = VGroup(sieve.frame, sieve.mesh)
        sieve.shift(np.array([parcel.frame.get_center()[0], -1.85, 0]) - mesh.get_center())
        sieve.title.align_to(mesh, RIGHT)                           # .git/ comes to rest at the left
        err = erratum_tag("erratum · no .dockerignore").next_to(mesh, DOWN, buff=0.3)
        lines5 = VGroup(*[mono(s_, 24, VENV) for s_ in (".git", ".venv", "secrets/")])
        lines5.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head5 = mono(".dockerignore", 24, INK)
        body5 = VGroup(head5, lines5).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        frame5 = box(body5.width + 1.4, body5.height + 0.8, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
        body5.move_to(frame5)
        VGroup(frame5, body5).move_to([3.4, 0.45, 0])
        ill = illustration_tag("illustration · a file you'd add").next_to(frame5, UP, buff=0.2)
        hub = shelf_glyph(1.4).move_to([2.6, -2.45, 0])
        soon = tag("public, soon", S.GREY).next_to(hub, RIGHT, buff=0.35)
        rest = mesh.get_top()[1] + 0.04 + git_item.height / 2       # .git/ comes to rest on the sieve
        caught = [git_item.get_center()[0], rest, 0]

        with self.voiceover(SAY[5]) as vo:
            git_src = toks[".git"].copy()
            self.add(git_src)
            others = VGroup(*[it for n, it in parcel.items.items() if n != ".git/"])
            self.play(FadeOut(w), FadeOut(cap),          # the frames are part of w's rows (attach)
                      FadeIn(VGroup(parcel.frame, parcel.tape, parcel.title, parcel.crowd, others)),
                      ReplacementTransform(git_src, git_item), run_time=1.0)
            self.remove(*w.get_family(), *cap.get_family())
            self.add(parcel)
            vo.wait_until("there's no")
            self.play(FadeIn(mesh, shift=DOWN * 0.2), FadeIn(sieve.title), run_time=0.6)
            self.play(FadeIn(err, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("In your own")
            self.play(FadeIn(frame5), FadeIn(head5), FadeIn(ill, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("dot git")
            self.play(FadeIn(lines5[0], shift=RIGHT * 0.1), sieve.solidify(VENV), FadeOut(err), run_time=0.5)
            self.play(git_item.animate.move_to(caught), run_time=0.6)
            self.play(Indicate(mesh, color=VENV, scale_factor=1.04), run_time=0.4)
            vo.wait_until("dot venv")
            self.play(FadeIn(lines5[1], shift=RIGHT * 0.1), run_time=0.4)
            vo.wait_until("your secrets")
            self.play(FadeIn(lines5[2], shift=RIGHT * 0.1), run_time=0.4)
            vo.wait_until("It matters")
            self.play(FadeIn(hub, shift=UP * 0.1), FadeIn(soon, shift=LEFT * 0.1), run_time=0.5)
            self.play(Indicate(hub, color=CLOUD, scale_factor=1.12), run_time=0.7)
            vo.wait_until("and that")
            self.play(Indicate(hub, color=CLOUD, scale_factor=1.15), Indicate(soon.text, color=TURN, scale_factor=1.15),
                      run_time=0.8)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
