"""S15 · Clean up, recap, and what's next (after the README; the end of part 2).

Beats (script.md "## S15", one voiceover block each):
 0  No tracker: a GREY caption top-left "after the README · clean up". V1 (common.Relay: five TEAL
    boxes with their letters over the BLUE cabinet, every drawer holding its token) appears at full
    width and zooms out to the top of the frame; a checklist card below: "cloud: nothing to delete",
    GREY sub-items "no VM", "no bucket", "no service account" (a GREEN tick as each is named; the
    cabinet pulses BLUE on "In the cloud"), then "your outputs stay in the bucket, under group-01"
    (the drawers' tokens pulse).
 1  V1 shrinks into the top-right corner (letters only); the card goes; a 13-row terminal (title
    laptop, prompt .../mega-pipeline/transcribe_audio$). `cd ..` (extra) -> (no output), the prompt
    becomes .../mega-pipeline$. The five-filter `docker image ls` (extra; Terminal.type folds it
    onto six rows, one filter a row) -> laptop/70-images-all.txt lines 2-7. On "transcribe audio
    at" 1.48GB gets a YELLOW bar and box A pulses; on "the other four" the four 84xMB sizes get
    bars and boxes B-E pulse.
 2  V1 fades; the terminal shrinks to 10 rows; `git status` (extra) -> 71-git-status.txt lines
    5-9, 11-14 (tabs shown as a terminal shows them, 8 columns). Line 9 gets a YELLOW bar on "your
    edited cli.py files" and the GREY caption "we set group_name only in transcribe_audio: yours
    also lists the other four cli.py and, / with your key, generate_text's text_prompts/ and
    text_paragraphs/" appears above the terminal; lines 8, 13, 14 get bars on "the files in
    generate text". On "but the other four folders hide" the caption goes, the terminal shrinks to
    a 3-row strip (`git status`, lines 13-14), CODE(transcribe_audio/.gitignore: 3-9, lines 5-7 in
    focus) slides in top right and four GREY dashed ghost chips, the other four Dockerfiles
    (`transcribe_audio/Dockerfile` ...), appear top left under "missing from git status:" and are
    struck through; on "and project files" lines 5-7 get YELLOW bars and the note "and their
    pyproject.toml, uv.lock" appears.
 3  Tag `erratum` beside the ghosts' heading. "add those Dockerfiles": the ghosts and lines 5-7
    pulse; "with git add dash f": a GREEN chip `git add -f` ("in your own repo") under the ghosts,
    the strikes retract and the ghosts turn solid GREY. "but not the data folders": lines 8-9
    (/input_audios, /text_prompts) come into focus with GREY crosses, "not these". "never stop
    ignoring secrets": line 3 (/secrets) comes into focus with a RED padlock, "keep ignoring this".
 4  The panel and the chips go, the terminal grows back to 13 rows and V1 returns to its corner.
    `docker image rm transcribe_audio generate_text synthesis_audio_en translate_text
    synthesis_audio` (extra; folds onto three rows) with `extra` and `▶ your turn` -> 72-cleanup.txt
    lines 2-11, printed pair by pair while V1's boxes A-E dissolve one by one (the cabinet stays).
    "Older builds stay behind untagged": the terminal shrinks to the strip (the last pair) and
    four dashed TEAL "older builds · untagged" boxes appear above it, each with a GOLD key (they
    pulse on "each holding your key"). `docker image prune -f` (extra; no output: not captured), the
    GREY caption "removes the untagged older builds · each held your key", and the dashed boxes
    dissolve. Then the GREY caption "still on disk: the base image (L4 uses it again) and the build
    cache · docker builder prune frees it" and a GREEN check "no containers left: every run used
    --rm"; a short hold.
 5  Everything goes. "Test yourself" (YELLOW underline). Q1 (26 pt, YELLOW badge) with a text-free
    thumbnail of V1 (box D pulses on "translate text", the cabinet on "who wrote it"); Q1 shrinks to
    22 pt GREY and Q2 comes in below (thumbnail: V3's window, the image block with its /app cavity,
    the GREEN venv box outside it and the PINK route from the laptop folder; the cavity pulses on
    "the mount", the venv box on "uv project environment").
 6  Q3 (thumbnail: V4's dashed writable sheet with a GREEN shelf of package chips; it pulses on "what
    survives"), Q4 (a text-free PINK signpost, a GOLD key at its tip; `/app` YELLOW on "why only
    from slash app"), Q5 (a sieve with the GOLD key on it over a TEAL box; the key pulses on "a
    git-ignored key", the sieve on "and the fix").
 7  The thumbnail goes; the five questions reflow to full width at the top; footer cards "Answers:
    exercises.md" and "Study guide + every command:" with the MLOps_Learning link and the guide's
    path; on "Next lecture" a dashed GREY card "next: L4 · branch flexible-workflow" whose three
    lines appear as they are said. Everything fades to an empty frame (end of part 2).

Terminal output comes only from assets/terminal/laptop/70-72 (capture()); the .gitignore panel quotes
assets/source/transcribe_audio/.gitignore with its real line numbers. The question text helpers are
the pilot's (videos/ac215-l01-vms-venvs/scenes/s15_recap.py), copied so the two recaps look alike.
"""

import re
from functools import lru_cache

import numpy as np
from manim import *

from explainer import style as S
from explainer.devops import (MONO, box, check_mark, chip, cross_mark, folder_glyph, label, mono,
                              mono_line, step_badge, substring)
from explainer.scene import VoiceScene

from common import (CLOUD, CTR, ERR, GROUP, INK, KEY, LAPTOP, LETTERS, LOOKUP, NARRATION, P_A, P_REPO,
                    TRACK_LEFT, TRACK_TOP, TURN, VENV, Relay, _set_op, beside, capture, erratum_tag,
                    extra_tag, key_glyph, padlock, pin, pkg_dots, resize, source_text, src_panel,
                    strike, strip_top, term, your_turn)

SAY = NARRATION["S15"]
assert len(SAY) == 8, len(SAY)

# ------------------------------------------------------------------ commands and real outputs
CD = "cd .."
IMG = capture("70-images-all")
assert IMG.cmd == ("docker image ls --filter reference=transcribe_audio --filter reference=generate_text "
                   "--filter reference=synthesis_audio_en --filter reference=translate_text "
                   "--filter reference=synthesis_audio"), IMG.cmd
IMG_OUT = IMG.at((2, 7))
IMG_SIZES = {"generate_text": "846MB", "synthesis_audio": "842MB", "synthesis_audio_en": "842MB",
             "transcribe_audio": "1.48GB", "translate_text": "845MB"}
for _ln in IMG_OUT[1:]:
    _name = _ln.split(":")[0]
    assert IMG_SIZES[_name] in _ln, _ln

GST = capture("71-git-status")
assert GST.cmd == "git status", GST.cmd
GST_OUT = [s.expandtabs(8) for s in GST.at((5, 9), (11, 14))]   # a terminal shows a tab as 8 columns
assert GST_OUT[3].endswith("modified:   generate_text/pyproject.toml"), GST_OUT[3]
assert GST_OUT[4].endswith("modified:   transcribe_audio/cli.py"), GST_OUT[4]
assert GST_OUT[7].strip() == "generate_text/Dockerfile" and GST_OUT[8].strip() == "generate_text/uv.lock"

RM = capture("72-cleanup")
assert RM.cmd == "docker image rm transcribe_audio generate_text synthesis_audio_en translate_text synthesis_audio"
RM_OUT = RM.at((2, 11))
assert all(RM_OUT[2 * j].startswith("Untagged: ") for j in range(5)), RM_OUT
PRUNE = "docker image prune -f"                  # extra, not captured: typed, no output

GITIGNORE = "transcribe_audio/.gitignore"
_GI = source_text(GITIGNORE).split("\n")
assert _GI[2:9] == ["/secrets", "docker-shell.sh", "Dockerfile", "pyproject.toml", "uv.lock",
                    "/input_audios", "/text_prompts"], _GI

OTHER_FOUR = ["transcribe_audio", "synthesis_audio_en", "translate_text", "synthesis_audio"]
GUIDE_REPO = "github.com/JunyiZhou-Conny/MLOps_Learning"
GUIDE_PATH = "guides/L03-containers-2-mega-pipeline.md"
NBSP = " "                                  # keeps a code span such as `uv add` on one line

# the five questions (script.md S15, on screen); spans in the code font
QUESTIONS = [
    ("Which prefix does translate_text read, and which stage wrote it?", ["translate_text"]),
    ("Why doesn't the mount hide the packages? What breaks without UV_PROJECT_ENVIRONMENT?",
     ["UV_PROJECT_ENVIRONMENT"]),
    ("After uv add in a --rm container: what survives, what is lost, what makes it permanent?",
     ["uv add", "--rm"]),
    ("Which variable tells the libraries where the key is, and why only from /app?", ["/app"]),
    ("How can an image contain a git-ignored key? The fix?", []),
]

# ------------------------------------------------------------------ layout
EDGE = 6.45
ROWS_FULL, ROWS_GIT = 13, 10           # 13 rows: `cd ..` + the six-row ls + 6 lines; rm (3) + 10
TOP_FULL = strip_top(ROWS_FULL)        # 2.59: V1's corner and the scene caption sit above it
TOP_GIT = strip_top(ROWS_GIT)          # 1.38: the git-status caption sits above it
STRIP = strip_top(3)                   # -1.44
CORNER_TOP = 3.52                      # V1 in the top-right corner: y 2.70..3.52
# questions (beats 5-7), as the pilot
Q_X = -5.72
Q_W = 7.0
Q_TOP = 2.35
Q_BIG, Q_SMALL, Q_FINAL = 26, 22, 21
THUMB_X, THUMB_W = 4.15, 4.7


# ------------------------------------------------------------------ small helpers
def place(m, left=None, right=None, top=None, bottom=None, cx=None, cy=None):
    if left is not None:
        m.shift(RIGHT * (left - m.get_left()[0]))
    if right is not None:
        m.shift(RIGHT * (right - m.get_right()[0]))
    if top is not None:
        m.shift(UP * (top - m.get_top()[1]))
    if bottom is not None:
        m.shift(UP * (bottom - m.get_bottom()[1]))
    if cx is not None:
        m.set_x(cx)
    if cy is not None:
        m.set_y(cy)
    return m


def words(*parts, size: float = 20, color=S.GREY, code_color=None) -> VGroup:
    """A caption row: plain strings in serif, 1-tuples in mono. A part that starts with
    punctuation hugs the part before it."""
    ms, gaps = [], []
    for p in parts:
        if isinstance(p, tuple):
            ms.append(mono(p[0], size, code_color or color))
            gaps.append(0.12)
        else:
            ms.append(label(p, size, color))
            gaps.append(0.04 if p[:1] in ",.:;'’" else 0.12)
    g = VGroup(ms[0])
    for m, gap in zip(ms[1:], gaps[1:]):
        m.next_to(g, RIGHT, buff=gap)
        m.align_to(ms[0], DOWN)
        g.add(m)
    g.parts = ms
    return g


def make_room(scene, t, n: int):
    """Room for n new rows: the oldest rows fade where they are, then the rest move up."""
    over = min(max(len(t.lines) + n - t.rows, 0), len(t.lines))
    if over <= 0:
        return
    gone = t.lines.submobjects[:over]
    stay = VGroup(*t.lines.submobjects[over:])
    scene.play(FadeOut(VGroup(*gone)), run_time=0.2)
    for m in gone:
        t.lines.remove(m)
        scene.remove(m)
    if len(stay):
        scene.play(stay.animate.shift(UP * t.pitch * over), run_time=0.25)


def n_rows(t, cmd: str) -> int:
    p = t.prompt + ("" if t.prompt.endswith(" ") else " ")
    return len(t.fold(p + cmd, first_prefix=len(p)))


def type_in(scene, t, cmd: str, type_time: float | None = None):
    """Type at the prompt (replacing a waiting bare prompt), scrolling the house way first."""
    if len(t.lines) and getattr(t.lines[-1], "bare", False):
        last = t.lines[-1]
        scene.remove(last, *last.submobjects)
        t.lines.remove(last)
    make_room(scene, t, n_rows(t, cmd))
    return t.type(scene, cmd, type_time)


def print_in(scene, t, lines, run_time: float = 0.4):
    make_room(scene, t, len(lines))
    return t.print(scene, lines, run_time=run_time, lag=0.12)


def bare(scene, t):
    """The prompt returns (no output)."""
    make_room(scene, t, 1)
    ln = t.type(scene, "", type_time=0)
    ln.bare = True
    return ln


def seed(t, text: str):
    """A bare prompt line on t, without animation (the terminal fades in with it)."""
    ln = mono_line(text, t.size, INK, t2c=t._prompt_colors(t.prompt))
    t._place(ln, len(t.lines))
    t.lines.add(ln)
    ln.bare = True
    return ln


def last_row(line):
    return line.rows[-1] if hasattr(line, "rows") else line


def sbar(line, sub: str | None, color=TURN, opacity: float = 0.3) -> Rectangle:
    """A translucent bar over substring `sub` of a terminal row (the row's text when None)."""
    g = substring(line, sub) if sub else line.glyphs
    return Rectangle(width=g.width + 0.14, height=line.strut.height * 0.95, stroke_width=0) \
        .set_fill(color, opacity).move_to([g.get_center()[0], line.strut.get_center()[1], 0])


def bars_on(scene, pairs, run_time: float = 0.4, extra=()):
    """Bars over (row, sub) pairs, faded in together, each made part of its row (it scrolls with it)."""
    bars = [sbar(r, s) for r, s in pairs]
    scene.play(*[FadeIn(b) for b in bars], *extra, run_time=run_time)
    for (r, _), b in zip(pairs, bars):
        scene.remove(b)
        r.add(b)
        scene.add(r)
    return bars


def pin_tags(scene, t, line, *tags, run_time: float = 0.3):
    """Tags beside a typed command (its last row when folded), side by side, part of that row."""
    row = last_row(line)
    prev = None
    for tg in tags:
        if prev is None:
            beside(tg, t, line)
        else:
            tg.next_to(prev, RIGHT, buff=0.15).set_y(row.strut.get_center()[1])
        prev = tg
    assert prev.get_right()[0] < t.box.get_right()[0] - 0.1, prev.get_right()
    scene.play(*[FadeIn(tg, shift=LEFT * 0.1) for tg in tags], run_time=run_time)
    for tg in tags:
        scene.remove(tg)
        row.add(tg)
    scene.add(row)


# ------------------------------------------------------------------ V1 in three sizes
def _show(piece, name: str):
    """A hidden part of a piece that is not on screen yet, made visible (no animation)."""
    m = piece.parts[name]
    if getattr(m, "hidden", False):
        _set_op(m)
    piece._flag(m, False)


def relay_at(width: float, box_h: float, drawer_h: float, gap: float, letter_pt: float = 34,
             icons: bool = True) -> Relay:
    """V1 with letters centred in their boxes (and each drawer's token when icons=True). The three
    sizes share one structure, so one Transform turns any of them into another."""
    r = Relay(width=width, labels=False, bonus=False, box_h=box_h, drawer_h=drawer_h, gap=gap)
    _show(r, "letters")
    for let, b in zip(r.letters, r.boxes):
        if letter_pt != 34:
            let.scale(letter_pt / 34)
        let.move_to(b)
    if icons:
        _show(r, "icons")
    return r


def relay_big() -> Relay:
    return place(relay_at(12.4, 1.0, 1.25, 0.8), cx=0, cy=0.2)


def relay_mid() -> Relay:
    return place(relay_at(7.4, 0.62, 0.8, 0.45), cx=0, top=2.55)


def relay_corner() -> Relay:
    return place(relay_at(4.4, 0.32, 0.3, 0.12, letter_pt=22, icons=False), right=EDGE, top=CORNER_TOP)


# ------------------------------------------------------------------ pictures for beats 0-4
def checklist_card() -> VGroup:
    """Beat 0: "cloud: nothing to delete", three GREY items with GREEN ticks, the outputs line.
    .frame .title .items[i] (.tick .text) .outputs .group (the mono group-01)"""
    title = words("cloud:", "nothing to delete", size=28, color=INK)
    title.parts[0].set_color(CLOUD)
    items = VGroup()
    for s in ("no VM", "no bucket", "no service account"):
        tk = check_mark(0.26, VENV)
        tx = label(s, 24, S.GREY)
        it = VGroup(tk, tx).arrange(RIGHT, buff=0.14)
        it.tick, it.text = tk, tx
        items.add(it)
    items.arrange(RIGHT, buff=0.6)
    outs = words("your outputs stay in the bucket, under", (GROUP,), size=22, color=INK, code_color=LOOKUP)
    body = VGroup(title, items, outs).arrange(DOWN, buff=0.36, aligned_edge=LEFT)
    items.shift(RIGHT * 0.3)
    fr = box(body.width + 0.9, body.height + 0.7, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
    fr.move_to(body)
    g = VGroup(fr, body)
    g.frame, g.title, g.items, g.outputs = fr, title, items, outs
    g.group = outs.parts[-1]
    return g


def ghost_chips() -> VGroup:
    """Beat 2: the other four Dockerfiles as GREY dashed chips (all one width), the heading above,
    a note below. .head .chips[i] (.dashed .solid .text .strike) .note"""
    head = label("missing from git status:", 22, S.GREY)
    texts = [mono(f"{c}/Dockerfile", 20, S.GREY) for c in OTHER_FOUR]
    w = max(t.width for t in texts) + 0.5
    h = 0.44
    chips = VGroup()
    for t in texts:
        dashed = box(w, h, S.GREY, dashed=True, stroke=2)
        t.move_to(dashed).align_to(dashed, LEFT).shift(RIGHT * 0.25)
        c = VGroup(dashed, t)
        c.dashed, c.text = dashed, t
        chips.add(c)
    chips.arrange(DOWN, buff=0.12, aligned_edge=LEFT)
    note = words("and their", ("pyproject.toml",), ",", ("uv.lock",), size=20)
    g = VGroup(head, chips, note)
    head.next_to(chips, UP, buff=0.22).align_to(chips, LEFT)
    note.next_to(chips, DOWN, buff=0.2).align_to(chips, LEFT)
    g.head, g.chips, g.note = head, chips, note
    return g


def finish_ghosts(g: VGroup) -> VGroup:
    """After the ghosts are placed: each chip's solid twin (.solid) and strike line (.strike)."""
    for c in g.chips:
        c.solid = box(c.dashed.width, c.dashed.height, S.GREY, fill_opacity=0.16, stroke=2.5,
                      radius=0.12).move_to(c.dashed)
        c.strike = strike(c.text, S.GREY, 3)
    return g


def older_builds(n: int = 4) -> VGroup:
    """Beat 4: n dashed TEAL image boxes, each with a GOLD key, and a GREY label under them.
    .boxes[i] (.frame .key) .label"""
    boxes = VGroup()
    for _ in range(n):
        fr = box(1.15, 0.72, CTR, dashed=True, stroke=2.5)
        k = key_glyph(0.26).move_to(fr)
        b = VGroup(fr, k)
        b.frame, b.key = fr, k
        boxes.add(b)
    boxes.arrange(RIGHT, buff=0.3)
    lab = label("older builds · untagged", 22, S.GREY).next_to(boxes, DOWN, buff=0.16)
    g = VGroup(boxes, lab)
    g.boxes, g.label = boxes, lab
    return g


# ------------------------------------------------------------------ question text (the pilot's)
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
    """One sentence per line group when that costs no extra line, otherwise a balanced wrap. A
    code span is never split."""
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


# ------------------------------------------------------------------ thumbnails (text-free shapes)
def thumb_frame(content: VGroup, h: float | None = None) -> VGroup:
    """A small dark card holding a thumbnail. .frame .content"""
    h = h or content.height + 0.6
    frame = box(THUMB_W, h, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
    content.move_to(frame)
    g = VGroup(frame, content)
    g.frame, g.content = frame, content
    return g


def thumb_cabinet() -> VGroup:
    """Q1 · V1: five TEAL boxes over a BLUE cabinet of six drawers (no letters, no edges)."""
    w, p = 3.9, 3.9 / 6
    drawers = VGroup()
    for i in range(6):
        fr = RoundedRectangle(width=p - 0.1, height=0.62, corner_radius=0.07, stroke_color=CLOUD,
                              stroke_width=2.5).set_fill(CLOUD, 0.1)
        fr.move_to([-w / 2 + (i + 0.5) * p, -0.31, 0])
        hd = RoundedRectangle(width=0.22, height=0.06, corner_radius=0.03, stroke_width=0).set_fill(CLOUD, 0.9)
        hd.move_to(fr.get_top() + DOWN * 0.12)
        drawers.add(VGroup(fr, hd))
    cab = RoundedRectangle(width=w + 0.14, height=0.76, corner_radius=0.1, stroke_color=CLOUD,
                           stroke_width=1.5, stroke_opacity=0.6).move_to(drawers)
    boxes = VGroup(*[RoundedRectangle(width=p - 0.18, height=0.6, corner_radius=0.08, stroke_color=CTR,
                                      stroke_width=2.5).set_fill(CTR, 0.1).move_to([-w / 2 + (j + 1) * p, 0.75, 0])
                     for j in range(5)])
    g = thumb_frame(VGroup(cab, drawers, boxes))
    g.cab, g.drawers, g.boxes = cab, drawers, boxes
    return g


def thumb_window() -> VGroup:
    """Q2 · V3: the laptop folder, the PINK route, the TEAL image with its dashed /app cavity and
    the GREEN venv box outside the cavity, the dashed writable sheet under it."""
    fold = folder_glyph(0.5, LAPTOP)
    img = RoundedRectangle(width=2.5, height=1.3, corner_radius=0.1, stroke_color=CTR,
                           stroke_width=3).set_fill(CTR, 0.1)
    img.next_to(fold, RIGHT, buff=0.75)
    cav = box(1.05, 0.85, LAPTOP, dashed=True, stroke=2).move_to(img).align_to(img, LEFT).shift(RIGHT * 0.22)
    venv = RoundedRectangle(width=0.85, height=0.5, corner_radius=0.06, stroke_color=VENV,
                            stroke_width=2.5).set_fill(VENV, 0.3)
    venv.move_to(img).align_to(img, RIGHT).shift(LEFT * 0.22)
    sheet = box(2.5, 0.2, CTR, dashed=True, stroke=2).next_to(img, DOWN, buff=0.1)
    route = Line(fold.get_right() + RIGHT * 0.08, cav.get_left() + LEFT * 0.04, color=LOOKUP, stroke_width=4)
    g = thumb_frame(VGroup(fold, route, img, cav, venv, sheet))
    g.fold, g.route, g.img, g.cav, g.venv = fold, route, img, cav, venv
    return g


def thumb_shelf() -> VGroup:
    """Q3 · V4: the container's dashed writable sheet with a GREEN shelf of package chips on it."""
    sheet = box(3.4, 1.35, CTR, dashed=True, stroke=2.5)
    shelf = Line(LEFT * 1.25, RIGHT * 1.25, color=VENV, stroke_width=5).move_to(sheet).shift(DOWN * 0.25)
    dots = pkg_dots(12, cols=6, w=0.22, buff=0.07).next_to(shelf, UP, buff=0.06)
    g = thumb_frame(VGroup(sheet, shelf, dots))
    g.sheet, g.shelf, g.dots = sheet, shelf, dots
    return g


def thumb_signpost() -> VGroup:
    """Q4 · V5: a text-free PINK signpost (board pointing right, post, foot), a GOLD key at its tip."""
    w, h, tip = 2.2, 0.62, 0.36
    board = Polygon([-w / 2, -h / 2, 0], [w / 2, -h / 2, 0], [w / 2 + tip, 0, 0], [w / 2, h / 2, 0],
                    [-w / 2, h / 2, 0], stroke_color=LOOKUP, stroke_width=3).set_fill(LOOKUP, 0.12)
    bars = VGroup(*[Line(LEFT * 0.75, RIGHT * (0.75 if k == 0 else 0.35), color=LOOKUP, stroke_width=3)
                    for k in range(2)]).arrange(DOWN, buff=0.14, aligned_edge=LEFT).move_to(board).shift(LEFT * 0.12)
    px = -w / 2 + 0.35
    post = Line([px, -h / 2, 0], [px, -h / 2 - 0.6, 0], color=LOOKUP, stroke_width=5)
    foot = Line([px - 0.22, -h / 2 - 0.6, 0], [px + 0.22, -h / 2 - 0.6, 0], color=LOOKUP, stroke_width=5)
    k = key_glyph(0.34).next_to(board, RIGHT, buff=0.22)
    g = thumb_frame(VGroup(post, foot, board, bars, k))
    g.board, g.key = VGroup(board, bars), k
    return g


def thumb_sieve() -> VGroup:
    """Q5 · V6: a GREY sieve with the GOLD key resting on it, over a TEAL image box."""
    w = 2.4
    bowl = Polygon([-w / 2, 0.18, 0], [w / 2, 0.18, 0], [w * 0.38, -0.18, 0], [-w * 0.38, -0.18, 0],
                   stroke_color=S.GREY, stroke_width=3).set_fill(S.GREY, 0.08)
    mesh = VGroup(*[Line([x, 0.18, 0], [x * 0.78, -0.18, 0], color=S.GREY, stroke_width=1.5)
                    for x in np.linspace(-w * 0.42, w * 0.42, 9)])
    sv = VGroup(bowl, mesh)
    k = key_glyph(0.32).next_to(bowl, UP, buff=0.06)
    crate = RoundedRectangle(width=1.7, height=0.75, corner_radius=0.06, stroke_color=CTR,
                             stroke_width=3).set_fill(CTR, 0.12).next_to(bowl, DOWN, buff=0.3)
    g = thumb_frame(VGroup(k, sv, crate))
    g.sieve, g.key, g.crate = sv, k, crate
    return g


class Recap(VoiceScene):
    # ------------------------------------------------------------- question helpers (the pilot's)
    def place_q(self, q: VGroup, top: float) -> VGroup:
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
        th.shift(np.array([THUMB_X, y, 0]) - th.frame.get_center())
        return th

    def demote(self, q: VGroup, i: int, top: float, width: float = Q_W, size: float = Q_SMALL):
        small = self.place_q(question(i, size, S.GREY, S.GREY, width), top)
        return Transform(q.flat, small.flat), small

    def swap_in(self, q_old, new):
        self.remove(q_old.flat, q_old, *[ln.strut for ln in q_old.text.lines])
        self.add(new)

    # ------------------------------------------------------------- the scene
    def construct(self):
        cap = label("after the README · clean up", 22, S.GREY)
        place(cap, left=TRACK_LEFT, top=TRACK_TOP)

        # ========================================================== 0 · nothing to delete in the cloud
        relay = relay_big()
        mid = relay_mid()
        card = checklist_card()
        place(card, cx=0, top=mid.get_bottom()[1] - 0.55)
        assert card.get_bottom()[1] > -3.4, card.get_bottom()

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(cap, shift=DOWN * 0.15), FadeIn(relay), run_time=0.6)
            self.play(Transform(relay, mid), run_time=1.0)                     # V1 zooms out
            vo.wait_until("In the cloud")
            self.play(FadeIn(card.frame), FadeIn(card.title, shift=UP * 0.1),
                      Indicate(relay.cabinet, color=CLOUD, scale_factor=1.03), run_time=0.6)
            for it, anchor in zip(card.items, ("machine", "bucket", "or account")):
                vo.wait_until(anchor)
                self.play(FadeIn(it.text, shift=UP * 0.1), Create(it.tick), run_time=0.4)
            self.play(FadeIn(card.outputs, shift=UP * 0.1), run_time=0.5)
            self.play(LaggedStart(*[Indicate(ic, color=INK, scale_factor=1.25) for ic in relay.icons],
                                  lag_ratio=0.12),
                      Indicate(card.group, color=LOOKUP, scale_factor=1.1), run_time=1.0)

        # ========================================================== 1 · cd .., the five images
        t = term(P_A, rows=ROWS_FULL)
        seed(t, P_A)
        corner = relay_corner()
        assert corner.get_bottom()[1] > TOP_FULL + 0.06 and corner.get_left()[0] > cap.get_right()[0] + 0.5

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(card, shift=DOWN * 0.2), Transform(relay, corner), run_time=0.8)
            self.play(FadeIn(t), run_time=0.4)
            vo.wait_until("cd dot dot")
            c_cd = type_in(self, t, CD, 0.3)
            pin_tags(self, t, c_cd, extra_tag())
            t.set_prompt(P_REPO)
            bare(self, t)
            vo.wait_until("An extra command")
            c_ls = type_in(self, t, IMG.cmd, 2.2)
            pin_tags(self, t, c_ls, extra_tag())
            out = print_in(self, t, IMG_OUT, run_time=0.5)
            rows = {ln.text.split(":")[0]: ln for ln in out[1:]}
            vo.wait_until("transcribe audio at")
            bars_on(self, [(rows["transcribe_audio"], "1.48GB")],
                    extra=[Indicate(relay.boxes[0], color=TURN, scale_factor=1.15)])
            vo.wait_until("the other four")
            others = ["generate_text", "synthesis_audio_en", "translate_text", "synthesis_audio"]
            bars_on(self, [(rows[n], IMG_SIZES[n]) for n in others], run_time=0.5,
                    extra=[Indicate(relay.boxes[j], color=TURN, scale_factor=1.15) for j in (1, 2, 3, 4)])

        # ========================================================== 2 · git status
        gcap = VGroup(
            words("we set", ("group_name",), "only in", ("transcribe_audio",), ": yours also lists the other four",
                  ("cli.py",), "and,"),
            words("with your key,", ("generate_text",), "'s", ("text_prompts/",), "and", ("text_paragraphs/",)),
        ).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        place(gcap, left=-6.3, bottom=TOP_GIT + 0.2)
        assert gcap.get_top()[1] < cap.get_bottom()[1] - 0.15 and gcap.get_right()[0] < EDGE, (gcap.get_top(), gcap.get_right())

        ghosts = ghost_chips()
        place(ghosts, left=-6.4, top=2.95)
        finish_ghosts(ghosts)
        panel = src_panel(GITIGNORE, 3, 9, focus=[2, 3, 4])
        place(panel, left=ghosts.chips.get_right()[0] + 0.45, top=2.95)
        assert panel.get_right()[0] < EDGE and ghosts.get_bottom()[1] > STRIP + 1.0, \
            (panel.get_right(), ghosts.get_bottom())
        assert panel.get_bottom()[1] > STRIP + 0.25, panel.get_bottom()
        code = panel.code
        g_bars = [Rectangle(width=code.background.width - 0.12, height=code.code_lines[k].height + 0.14,
                            stroke_width=0).set_fill(TURN, 0.2).move_to([code.background.get_center()[0],
                                                                          code.code_lines[k].get_center()[1], 0])
                  for k in (2, 3, 4)]

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(relay), run_time=0.4)
            resize(self, t, ROWS_GIT, run_time=0.5)
            c_gs = type_in(self, t, GST.cmd, 0.45)
            pin_tags(self, t, c_gs, extra_tag())
            g_out = print_in(self, t, GST_OUT, run_time=0.5)
            l8, l9, l13, l14 = g_out[3], g_out[4], g_out[7], g_out[8]
            vo.wait_until("your edited cli.py files")
            bars_on(self, [(l9, "transcribe_audio/cli.py")])
            self.play(FadeIn(gcap, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("and the files in generate text")
            bars_on(self, [(l8, "generate_text/pyproject.toml"), (l13, "generate_text/Dockerfile"),
                           (l14, "generate_text/uv.lock")])
            vo.wait_until("but the other four folders hide")
            self.play(FadeOut(gcap), run_time=0.3)
            resize(self, t, 3, keep=[c_gs, l13, l14], run_time=0.6)
            self.play(FadeIn(panel, shift=DOWN * 0.3), FadeIn(ghosts.head), FadeIn(ghosts.chips, shift=RIGHT * 0.2),
                      run_time=0.6)
            self.play(*[Create(c.strike) for c in ghosts.chips], run_time=0.5)
            vo.wait_until("and project files")
            self.play(*[FadeIn(b) for b in g_bars], FadeIn(ghosts.note, shift=UP * 0.1), run_time=0.5)

        # ========================================================== 3 · erratum: git add -f, not data, never secrets
        err = erratum_tag().next_to(ghosts.head, RIGHT, buff=0.3)
        addf = chip("git add -f", VENV, size=22, font=MONO)
        addf_note = label("in your own repo", 20, S.GREY)
        addf_g = VGroup(addf, addf_note).arrange(RIGHT, buff=0.2)
        place(addf_g, left=ghosts.get_left()[0], top=ghosts.note.get_bottom()[1] - 0.25)
        assert addf_g.get_bottom()[1] > STRIP + 0.1, addf_g.get_bottom()
        right_of = code.background.get_right()[0] + 0.25
        y89 = (code.code_lines[5].get_center()[1] + code.code_lines[6].get_center()[1]) / 2
        crosses = VGroup(*[cross_mark(0.22, S.GREY, 4).move_to([right_of + 0.12, code.code_lines[k].get_center()[1], 0])
                           for k in (5, 6)])
        not_these = label("not these", 22, S.GREY).move_to([0, y89, 0])
        place(not_these, left=right_of + 0.45)
        lock = padlock(0.42, ERR).move_to([right_of + 0.2, code.code_lines[0].get_center()[1], 0])
        keep_ig = label("keep ignoring this", 22, ERR).next_to(lock, RIGHT, buff=0.15)
        assert keep_ig.get_right()[0] < EDGE and not_these.get_right()[0] < EDGE, (keep_ig.get_right(), not_these.get_right())
        bar3 = Rectangle(width=code.background.width - 0.12, height=code.code_lines[0].height + 0.14,
                         stroke_width=0).set_fill(ERR, 0.22).move_to([code.background.get_center()[0],
                                                                      code.code_lines[0].get_center()[1], 0])

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeIn(err, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("add those Dockerfiles")
            self.play(LaggedStart(*[Indicate(c, color=INK, scale_factor=1.04) for c in ghosts.chips], lag_ratio=0.15),
                      *[b.animate(rate_func=there_and_back).set_fill(opacity=0.5) for b in g_bars], run_time=0.9)
            vo.wait_until("with git add dash f")
            self.play(FadeIn(addf_g, shift=UP * 0.15), run_time=0.45)
            self.play(*[Uncreate(c.strike) for c in ghosts.chips],
                      *[FadeTransform(c.dashed, c.solid) for c in ghosts.chips],
                      *[c.text.animate.set_color(INK) for c in ghosts.chips], run_time=0.7)
            for c in ghosts.chips:
                c.remove(c.dashed)
                c.add_to_back(c.solid)
            vo.wait_until("but not the data folders")
            self.play(*[code.code_lines[k].animate.set_opacity(1) for k in (5, 6)],
                      *[Create(x) for x in crosses], FadeIn(not_these, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("and never stop ignoring secrets")
            self.play(code.code_lines[0].animate.set_opacity(1), FadeIn(bar3), FadeIn(lock, scale=0.6),
                      FadeIn(keep_ig, shift=LEFT * 0.1), run_time=0.6)
            self.play(Indicate(lock, color=ERR, scale_factor=1.2), run_time=0.6)

        # ========================================================== 4 · remove the images; prune
        olds = older_builds()
        place(olds, cx=0, top=1.95)
        pr_cap = words("removes the untagged older builds · each held your key", size=22)
        place(pr_cap, cx=0, bottom=olds.boxes.get_top()[1] + 0.25)
        disk = words("still on disk: the base image (L4 uses it again) and the build cache ·", ("docker builder prune",),
                     "frees it", size=20)
        place(disk, cx=0, top=olds.label.get_bottom()[1] - 0.45)
        nocon = VGroup(check_mark(0.26, VENV), words("no containers left: every run used", ("--rm",), size=22, color=INK))
        nocon.arrange(RIGHT, buff=0.15)
        place(nocon, cx=0, top=disk.get_bottom()[1] - 0.3)
        assert disk.get_right()[0] < EDGE and disk.get_left()[0] > -EDGE, disk.get_left()
        assert nocon.get_bottom()[1] > STRIP + 0.1, nocon.get_bottom()
        assert pr_cap.get_top()[1] < corner.get_bottom()[1] - 0.1, pr_cap.get_top()

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(panel, ghosts, err, addf_g, crosses, not_these, lock, keep_ig, *g_bars, bar3)),
                      run_time=0.5)
            for b in g_bars + [bar3]:
                self.remove(b)
            resize(self, t, ROWS_FULL, run_time=0.6, extra=[FadeIn(relay)])
            c_rm = type_in(self, t, RM.cmd, 1.8)
            pin_tags(self, t, c_rm, extra_tag(), your_turn())
            for j in range(5):                               # one pair a box: A..E dissolve
                print_in(self, t, RM_OUT[2 * j:2 * j + 2], run_time=0.3)
                self.play(relay.boxes[j].animate.scale(0.3).set_opacity(0),
                          relay.letters[j].animate.scale(0.3).set_opacity(0), run_time=0.3)
            vo.wait_until("Older builds stay behind untagged")
            resize(self, t, 3, keep=list(t.lines.submobjects[-2:]), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.15) for b in olds.boxes], lag_ratio=0.15),
                      FadeIn(olds.label), run_time=0.7)
            vo.wait_until("each holding your key")
            self.play(*[Indicate(b.key, color=KEY, scale_factor=1.4) for b in olds.boxes], run_time=0.7)
            vo.wait_until("so docker image prune")
            c_pr = type_in(self, t, PRUNE, 0.8)
            pin_tags(self, t, c_pr, extra_tag())
            self.play(FadeIn(pr_cap, shift=DOWN * 0.1), run_time=0.4)
            self.play(LaggedStart(*[b.animate.scale(0.3).set_opacity(0) for b in olds.boxes], lag_ratio=0.12),
                      olds.label.animate.set_opacity(0.35), run_time=0.8)
            self.play(FadeIn(disk, shift=UP * 0.1), run_time=0.5)
            self.play(Create(nocon[0]), FadeIn(nocon[1], shift=UP * 0.1), run_time=0.5)
            self.wait(1.6)                                    # the teardown checklist, before the recap

        # ========================================================== 5 · Test yourself: Q1, Q2
        title = label("Test yourself", 40, INK)
        place(title, left=-6.35, cy=3.1)
        t_ul = Line(title.get_corner(DL) + DOWN * 0.1, title.get_corner(DR) + DOWN * 0.1, color=TURN, stroke_width=4)
        q1 = self.place_q(question(1, Q_BIG, INK, TURN, Q_W), Q_TOP)
        th1 = self.thumb_at(thumb_cabinet(), q1)

        def step(q_cur, i_cur, top_cur, th_old, th_new_fn):
            """Demote the current question, bring question i_cur + 1 in below it, swap thumbnails."""
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
            self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
            self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.5)
            self.play(Create(t_ul), run_time=0.5)
            vo.wait_until("One")
            self.play(FadeIn(q1, shift=UP * 0.15), FadeIn(th1, shift=LEFT * 0.2), run_time=0.6)
            vo.wait_until("translate text")
            span = q_span(q1, "translate_text")
            self.play(span.animate.set_color(TURN), Indicate(th1.boxes[3], color=TURN, scale_factor=1.25), run_time=0.6)
            vo.wait_until("who wrote it")
            self.play(Indicate(q_span(q1, "whichstagewroteit"), color=TURN, scale_factor=1.05),
                      Indicate(th1.drawers, color=CLOUD, scale_factor=1.06), run_time=0.8)
            vo.wait_until("Two")
            s1, q2, th2, top2 = step(q1, 1, Q_TOP, th1, thumb_window)
            smalls.append(s1)
            vo.wait_until("the mount hide")
            self.play(Indicate(th2.route, color=LOOKUP, scale_factor=1.15),
                      Indicate(th2.cav, color=LAPTOP, scale_factor=1.12), run_time=0.7)
            vo.wait_until("uv project environment")
            env = q_span(q2, "UV_PROJECT_ENVIRONMENT")
            self.play(env.animate.set_color(TURN), Indicate(th2.venv, color=VENV, scale_factor=1.3), run_time=0.7)

        # ========================================================== 6 · Q3, Q4, Q5
        with self.voiceover(SAY[6]) as vo:
            s2, q3, th3, top3 = step(q2, 2, top2, th2, thumb_shelf)
            smalls.append(s2)
            vo.wait_until("what survives")
            self.play(Indicate(th3.dots, color=VENV, scale_factor=1.15), run_time=0.7)
            vo.wait_until("what makes it permanent")
            self.play(Indicate(th3.sheet, color=CTR, scale_factor=1.06), run_time=0.7)
            vo.wait_until("Four")
            s3, q4, th4, top4 = step(q3, 3, top3, th3, thumb_signpost)
            smalls.append(s3)
            vo.wait_until("which variable points")
            self.play(Indicate(th4.board, color=LOOKUP, scale_factor=1.1), run_time=0.7)
            vo.wait_until("why only from slash app")
            self.play(q_span(q4, "/app").animate.set_color(TURN), Indicate(th4.key, color=KEY, scale_factor=1.3),
                      run_time=0.7)
            vo.wait_until("Five")
            s4, q5, th5, top5 = step(q4, 4, top4, th4, thumb_sieve)
            smalls.append(s4)
            vo.wait_until("git-ignored key")
            self.play(Indicate(th5.key, color=KEY, scale_factor=1.35), run_time=0.7)
            vo.wait_until("and the fix")
            self.play(Indicate(th5.sieve, color=INK, scale_factor=1.1), run_time=0.7)

        # ========================================================== 7 · shrink to the top; where next
        title2 = label("Test yourself", 32, INK)
        place(title2, left=-6.35, cy=3.25)
        t_ul2 = Line(title2.get_corner(DL) + DOWN * 0.08, title2.get_corner(DR) + DOWN * 0.08, color=TURN,
                     stroke_width=3)
        finals, top = [], title2.get_bottom()[1] - 0.35
        for i in range(1, 6):
            f = self.place_q(question(i, Q_FINAL, S.GREY, S.GREY, 12.15), top)
            finals.append(f)
            top = self.q_bottom(f) - 0.2
        ans = VGroup(label("Answers:", 26, INK), mono("exercises.md", 24, INK)).arrange(RIGHT, buff=0.2)
        ans_box = box(ans.width + 0.7, ans.height + 0.45, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
        ans.move_to(ans_box)
        card1 = VGroup(ans_box, ans)
        g_head = label("Study guide + every command:", 26, INK)
        g_url = VGroup(mono(GUIDE_REPO, 20, INK), mono(GUIDE_PATH, 20, INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        g_body = VGroup(g_head, g_url).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        g_box = box(g_body.width + 0.7, g_body.height + 0.45, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
        g_body.move_to(g_box)
        card2 = VGroup(g_box, g_body)
        place(card1, left=-6.35, top=top - 0.25)
        card2.next_to(card1, RIGHT, buff=0.3, aligned_edge=UP)
        n_head = VGroup(label("next:", 24, S.GREY), label("L4 · branch", 24, INK), mono("flexible-workflow", 22, INK))
        n_head.arrange(RIGHT, buff=0.14)
        for m in n_head[1:]:
            m.align_to(n_head[0], DOWN)
        n_items = VGroup(
            words("your own bucket + service account", size=22, color=INK),
            words("· the key outside the repo", size=22, color=INK),
            words("·", ("docker-shell.sh",), "builds and runs for you", size=22, color=INK),
        ).arrange(RIGHT, buff=0.16)
        for m in n_items[1:]:
            m.align_to(n_items[0], DOWN)
        n_body = VGroup(n_head, n_items).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        n_box = box(12.7, n_body.height + 0.5, S.GREY, dashed=True)
        n_body.move_to(n_box).align_to(n_box, LEFT).shift(RIGHT * 0.35)
        nxt = VGroup(n_box, n_body)
        place(nxt, left=-6.35, top=card2.get_bottom()[1] - 0.3)
        assert card2.get_right()[0] < EDGE and nxt.get_bottom()[1] > -3.5, (card2.get_right(), nxt.get_bottom())
        assert n_items.get_right()[0] < n_box.get_right()[0] - 0.2, n_items.get_right()
        assert finals[-1].get_bottom()[1] > card1.get_top()[1] + 0.15

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
            self.play(FadeIn(card1, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("every command is in the study guide")
            self.play(FadeIn(card2, shift=UP * 0.15), run_time=0.5)
            self.play(Indicate(g_url, color=TURN, scale_factor=1.04), run_time=0.7)
            vo.wait_until("Next lecture")
            self.play(FadeIn(n_box), FadeIn(n_head, shift=LEFT * 0.15), run_time=0.5)
            for it, anchor in zip(n_items, ("your own bucket", "the key outside", "a script that builds")):
                vo.wait_until(anchor)
                self.play(FadeIn(it, shift=UP * 0.1), run_time=0.4)

        self.wait(0.8)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.9)
        self.wait(0.3)
