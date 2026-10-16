"""S15 · Clean up, recap, and what's next (after the README; the end of part 2).

Beats (script.md "## S15", one voiceover block each):
 0  No tracker: a GREY caption top-left "after the README · clean up". V1 (common.Relay: five TEAL
    boxes with their letters over the BLUE cabinet, every drawer holding its token) appears at full
    width and zooms out to the top of the frame; a checklist card below: "cloud: nothing to delete"
    (the cabinet pulses BLUE on "In the cloud"); on "nothing to delete" its last row "your outputs
    stay in the bucket, under group-01" (the drawers' tokens pulse), so it is up through the ticks;
    then the GREY sub-items "no VM", "no bucket", "no service account" fill the middle row (a GREEN
    tick as each is named).
 1  V1 shrinks into the top-right corner (letters only); the card goes; a 13-row terminal (title
    laptop, prompt .../mega-pipeline/transcribe_audio$). `cd ..` (extra) -> (no output), the prompt
    becomes .../mega-pipeline$. The five-filter `docker image ls` (extra; Terminal.type folds it
    onto six rows, one filter a row) -> laptop/70-images-all.txt lines 2-7. On "transcribe audio
    at" 1.48GB gets a YELLOW bar and box A pulses; on "the other four" the four 84xMB sizes get
    bars one after another while boxes B-E pulse.
 2  V1 and the old screen fade together (a fresh screen, as `clear`); the terminal shrinks to 10
    rows with the bare prompt at the top; on "An extra git status" it types `git status` (extra) -> 71-git-status.txt lines
    5-9, 11-14 (tabs shown as a terminal shows them, 8 columns). Line 9 gets a YELLOW bar on "your
    edited cli.py files" as the GREY caption "we set group_name only in transcribe_audio: yours
    also lists the other four cli.py / and, with your key, generate_text's text_prompts/ and
    text_paragraphs/ / and the five .dockerignore files you added: commit those (no -f needed)"
    appears above the terminal (the capture removed its .dockerignore; a viewer has five, untracked);
    lines 8, 13, 14 get bars on "the files in generate text". On "but the other four folders hide"
    the terminal shrinks to a 3-row strip (`git status`, lines 13-14), then the caption goes;
    CODE(transcribe_audio/.gitignore: 3-9, 24 pt, lines
    5-7 in focus) slides in top right and four GREY dashed ghost chips, the other four Dockerfiles
    (`transcribe_audio/Dockerfile` ...), appear top left under "missing from git status:" and are
    struck through; on "and project files" lines 5-7 get one YELLOW bar and the note "and their
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
    four dashed TEAL boxes, each with a GOLD key, appear above it over the GREY label "older builds
    · untagged" (the keys pulse RED on "each holding your key": a key inside an image). `docker image prune -f` (extra; no
    output: not captured), the GREY caption "removes the untagged older builds · each held your
    key" above them, and the boxes and their label dissolve. In their place the GREY caption "still
    on disk: the base image (L4 uses it again) and the build cache / docker builder prune frees it"
    and a GREEN check "no containers left: every run used --rm"; a 2.4 s hold (silent) to read them.
 5  Everything goes. "Test yourself" (YELLOW underline). Q1 (26 pt, YELLOW badge) with a text-free
    thumbnail of V1 (box D pulses on "translate text", the cabinet on "who wrote it"); Q1 shrinks to
    22 pt GREY, keeping its line breaks (each glyph only shrinks and slides), and Q2 comes in below (thumbnail: V3's window, the image block with its /app cavity,
    the GREEN venv box outside it and the PINK route from the laptop folder; the cavity pulses on
    "the mount", the venv box on "uv project environment").
 6  Q3 (thumbnail: V4's dashed writable sheet with a GREEN shelf of package chips; it pulses on "what
    survives"), Q4 (a text-free PINK signpost, a GOLD key at its tip; `/app` YELLOW on "why only
    from slash app"), Q5 (a sieve with the GOLD key on it over a TEAL box; the key pulses on "a
    git-ignored key" (RED: a key inside an image), the sieve on "and the fix").
 7  The thumbnail goes; the five questions (Q5 straight from its big form) reflow to full width at
    the top, top to bottom; footer cards "Answers: study guide §8 (exercises.md)" (the file is in this
    video's folder, which the guide's §8 links) and, under it, "Study guide + every command:" with the MLOps_Learning link and the
    guide's path (it pulses on "study guide"); on "Next lecture" a dashed GREY card at the right,
    "next: L4" / "branch flexible-workflow", whose three lines appear as they are said ("your own
    bucket + service account", "the key outside the repo", "docker-shell.sh / builds and runs for
    you"). Everything fades to an empty frame (end of part 2).

Terminal output comes only from assets/terminal/laptop/70-72 (capture()); the .gitignore panel quotes
assets/source/transcribe_audio/.gitignore with its real line numbers. The question text helpers are
the pilot's (videos/ac215-l01-vms-venvs/scenes/s15_recap.py), copied so the two recaps look alike.
"""

import re
from functools import lru_cache

import numpy as np
from manim import *

from explainer import style as S
from explainer.devops import (MONO, OUTPUT, box, check_mark, chip, cross_mark, folder_glyph, label, mono,
                              mono_line, step_badge, substring)
from explainer.scene import VoiceScene

from common import (CLOUD, CTR, ERR, GROUP, INK, KEY, LAPTOP, LOOKUP, NARRATION, P_A, P_REPO,
                    TRACK_LEFT, TRACK_TOP, TURN, VENV, Relay, _set_op, beside, capture, erratum_tag,
                    extra_tag, key_glyph, padlock, pkg_dots, resize, source_text, src_panel,
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
Q_BIG, Q_SMALL, Q_FINAL = 26, 22, 22
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


def words(*parts, size: float = 20, color=S.GREY, code_color=None, t2c=None) -> Text:
    """A caption line as ONE Text (one baseline): plain strings in serif, 1-tuples in the code font
    (and code_color). A plain part that starts with punctuation hugs the part before it (a code
    part such as `.dockerignore` never does). .src"""
    s, code = "", []
    for p in parts:
        txt = p[0] if isinstance(p, tuple) else p
        if isinstance(p, tuple):
            code.append(txt)
        if s and (isinstance(p, tuple) or txt[:1] not in ",.:;'’"):
            s += " "
        s += txt
    cmap = {c: code_color for c in code} if code_color else {}
    cmap.update(t2c or {})
    t = S.text(s, size, color, t2f={c: MONO for c in code}, t2c=cmap)
    t.src = s
    return t


def span(t: Text, sub: str) -> VGroup:
    """The glyphs of `sub` in a words() line (glyphs skip spaces)."""
    i = t.src.find(sub)
    assert i >= 0, (sub, t.src)
    a = len("".join(t.src[:i].split()))
    return VGroup(*t.submobjects[a:a + len("".join(sub.split()))])


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


def print_with(scene, t, lines, extra=(), run_time: float = 0.35):
    """Print output lines the way Terminal.print does (cut at the row, OUTPUT colour), in ONE play
    together with `extra` animations (Terminal.print plays alone). The room must be made first."""
    assert len(t.lines) + len(lines) <= t.rows, (len(t.lines), len(lines), t.rows)
    new = []
    for s in lines:
        ln = mono_line(t._cut(s), t.size, OUTPUT)
        t._place(ln, len(t.lines))
        t.lines.add(ln)
        new.append(ln)
    scene.play(LaggedStart(*[FadeIn(m) for m in new], lag_ratio=0.12), *extra, run_time=run_time)
    return new


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


def bars_on(scene, pairs, run_time: float = 0.4, extra=(), lag: float = 0.0):
    """Bars over (row, sub) pairs, faded in together (one after another with lag > 0, the `extra`
    animations staggered alike), each made part of its row (it scrolls with it)."""
    bars = [sbar(r, s) for r, s in pairs]
    if lag:
        scene.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=lag),
                   LaggedStart(*extra, lag_ratio=lag), run_time=run_time)
    else:
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


def seen(r: Relay) -> VGroup:
    """The parts of V1 that are drawn here (the hidden bonus drawer and labels still take room)."""
    return VGroup(r.cabinet, r.boxes)


def put(r: Relay, **kw) -> Relay:
    """place() by the drawn parts."""
    v = seen(r)
    c0 = v.get_center()
    place(v, **kw)
    d = v.get_center() - c0
    v.shift(-d)
    r.shift(d)
    return r


def relay_big() -> Relay:
    return put(relay_at(12.4, 1.0, 1.25, 0.8), cx=0, cy=0.2)


def relay_mid() -> Relay:
    return put(relay_at(7.4, 0.62, 0.8, 0.45), cx=0, top=2.55)


def relay_corner() -> Relay:
    return put(relay_at(4.4, 0.32, 0.3, 0.12, letter_pt=22, icons=False), right=EDGE, top=CORNER_TOP)


# ------------------------------------------------------------------ pictures for beats 0-4
def checklist_card() -> VGroup:
    """Beat 0: "cloud: nothing to delete", three GREY items with GREEN ticks, the outputs line.
    .frame .title .items[i] (.tick .text) .outputs .group (the mono group-01)"""
    title = words("cloud:", "nothing to delete", size=34, color=INK, t2c={"cloud:": CLOUD})
    items = VGroup()
    for s in ("no VM", "no bucket", "no service account"):
        tk = check_mark(0.3, VENV)
        tx = label(s, 28, S.GREY)
        it = VGroup(tk, tx).arrange(RIGHT, buff=0.14)
        it.tick, it.text = tk, tx
        items.add(it)
    items.arrange(RIGHT, buff=0.7)
    outs = words("your outputs stay in the bucket, under", (GROUP,), size=26, color=INK, code_color=LOOKUP)
    body = VGroup(title, items, outs).arrange(DOWN, buff=0.42, aligned_edge=LEFT)
    items.shift(RIGHT * 0.3)
    fr = box(body.width + 1.0, body.height + 0.8, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
    fr.move_to(body)
    g = VGroup(fr, body)
    g.frame, g.title, g.items, g.outputs = fr, title, items, outs
    g.group = span(outs, GROUP)
    return g


def ghost_chips() -> VGroup:
    """Beat 2: the other four Dockerfiles as GREY dashed chips (all one width), the heading above,
    a note below. .head .chips[i] (.dashed .solid .text .strike) .note"""
    head = label("missing from git status:", 22, S.GREY)
    texts = [mono(f"{c}/Dockerfile", 22, S.GREY) for c in OTHER_FOUR]
    w = max(t.width for t in texts) + 0.4
    h = 0.48
    chips = VGroup()
    for t in texts:
        dashed = box(w, h, S.GREY, dashed=True, stroke=2)
        t.move_to(dashed).align_to(dashed, LEFT).shift(RIGHT * 0.2)
        c = VGroup(dashed, t)
        c.dashed, c.text = dashed, t
        chips.add(c)
    chips.arrange(DOWN, buff=0.12, aligned_edge=LEFT)
    note = words("and their", ("pyproject.toml",), ",", ("uv.lock",), size=22)
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
        fr = box(1.5, 0.95, CTR, dashed=True, stroke=2.5)
        k = key_glyph(0.34).move_to(fr)
        b = VGroup(fr, k)
        b.frame, b.key = fr, k
        boxes.add(b)
    boxes.arrange(RIGHT, buff=0.4)
    lab = label("older builds · untagged", 24, S.GREY).next_to(boxes, DOWN, buff=0.18)
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


def wrapped(s: str, size: float, color: str, width: float, code=(), strs=None) -> VGroup:
    """s wrapped to `width`, or broken exactly as the given line strings `strs`."""
    if strs is None:
        strs = wrap_lines(s, size, width, code)
    assert " ".join(strs) == s, (strs, s)
    rows = [text_line(ln, size, color, code) for ln in strs]
    pitch = rows[0].strut.height * 1.22
    for k, r in enumerate(rows):
        r.shift(np.array([-r.strut.get_left()[0], -k * pitch - r.strut.get_top()[1], 0]))
    g = VGroup(*rows)
    g.lines, g.strs = rows, strs
    g.glyphs = VGroup(*[gl for r in rows for gl in r.glyphs])
    return g


def question(i: int, size: float, color: str, badge_color: str, width: float, strs=None) -> VGroup:
    """Question i (1-based): a numbered badge and the wrapped text (or the line breaks `strs`), the
    text's top-left at the origin. .badge .text .flat (badge + glyphs, for glyph-to-glyph transforms)"""
    s, code = QUESTIONS[i - 1]
    txt = wrapped(s, size, color, width, code, strs)
    r = 0.24 if size >= Q_BIG else 0.19
    b = step_badge(i, badge_color, size=22 if size >= Q_BIG else 20, radius=r)
    first = txt.lines[0].strut
    b.move_to([-0.2 - r, first.get_center()[1], 0])
    g = VGroup(b, txt)
    g.badge, g.text = b, txt
    g.flat = VGroup(b, *txt.glyphs)
    return g


LIGATURES = ("ff", "fi", "fl")            # the serif font joins these into one glyph


def q_span(q: VGroup, sub: str) -> VGroup:
    """The glyphs of `sub` in question q's text (a span never crosses a line break). The serif
    font draws "fi" etc. as one glyph, so a span after such a pair is counted from the line's end
    (asserting no such pair follows it)."""
    key = "".join(sub.split())
    for r, s in zip(q.text.lines, q.text.strs):
        flat = "".join(s.split())
        i = flat.find(key)
        if i < 0:
            continue
        n = len(r.glyphs)
        if n == len(flat):
            return VGroup(*r.glyphs[i:i + len(key)])
        tail = flat[i + len(key):]
        assert not any(lg in tail for lg in LIGATURES), (sub, s)
        j = n - len(tail) - len(key)
        return VGroup(*r.glyphs[j:j + len(key)])
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
        """q made small and GREY with the SAME line breaks, so every glyph only shrinks and slides
        (no word jumps to another line); the one reflow is the final layout (beat 7)."""
        small = self.place_q(question(i, size, S.GREY, S.GREY, width, strs=q.text.strs), top)
        assert len(small.flat) == len(q.flat), (i, len(small.flat), len(q.flat))
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
        place(card, cx=0, top=seen(mid).get_bottom()[1] - 0.55)
        assert card.get_bottom()[1] > -3.4, card.get_bottom()

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(cap, shift=DOWN * 0.15), FadeIn(relay), run_time=0.6)
            self.play(Transform(relay, mid), run_time=1.0)                     # V1 zooms out
            vo.wait_until("In the cloud")
            self.play(FadeIn(card.frame), FadeIn(card.title, shift=UP * 0.1),
                      Indicate(relay.cabinet, color=CLOUD, scale_factor=1.03), run_time=0.6)
            vo.wait_until("nothing to delete")   # what stays comes first: it is up through the three ticks
            self.play(FadeIn(card.outputs, shift=UP * 0.1), run_time=0.5)
            self.play(LaggedStart(*[Indicate(ic, color=INK, scale_factor=1.25) for ic in relay.icons],
                                  lag_ratio=0.12),
                      Indicate(card.group, color=LOOKUP, scale_factor=1.1), run_time=1.0)
            for it, anchor in zip(card.items, ("machine", "bucket", "or account")):
                vo.wait_until(anchor)
                self.play(FadeIn(it.text, shift=UP * 0.1), Create(it.tick), run_time=0.4)

        # ========================================================== 1 · cd .., the five images
        t = term(P_A, rows=ROWS_FULL)
        seed(t, P_A)
        corner = relay_corner()
        assert seen(corner).get_bottom()[1] > TOP_FULL + 0.06 and seen(corner).get_left()[0] > cap.get_right()[0] + 0.5, \
            seen(corner).get_bottom()

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
            bars_on(self, [(rows[n], IMG_SIZES[n]) for n in others], run_time=1.6, lag=0.3,
                    extra=[Indicate(relay.boxes[j], color=TURN, scale_factor=1.15) for j in (1, 2, 3, 4)])

        # ========================================================== 2 · git status
        gcap = VGroup(
            words("we set", ("group_name",), "only in", ("transcribe_audio",), ": yours also lists the other four",
                  ("cli.py",), size=22),
            words("and, with your key,", ("generate_text",), "'s", ("text_prompts/",), "and", ("text_paragraphs/",),
                  size=22),
            # the S14 "your turn": no .gitignore lists .dockerignore, so yours shows five untracked ones
            words("and the five", (".dockerignore",), "files you added: commit those (no", ("-f",), "needed)",
                  size=22),
        ).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
        place(gcap, left=-6.3, cy=(cap.get_bottom()[1] + TOP_GIT) / 2)
        assert gcap.get_top()[1] < cap.get_bottom()[1] - 0.15 and gcap.get_right()[0] < EDGE, (gcap.get_top(), gcap.get_right())

        ghosts = ghost_chips()
        place(ghosts, left=-6.4, top=2.88)
        finish_ghosts(ghosts)
        panel = src_panel(GITIGNORE, 3, 9, focus=[2, 3, 4], size=24)
        place(panel, left=ghosts.chips.get_right()[0] + 0.35, top=2.88)
        assert panel.get_right()[0] < EDGE and ghosts.get_bottom()[1] > STRIP + 1.0, \
            (panel.get_right(), ghosts.get_bottom())
        assert panel.get_bottom()[1] > STRIP + 0.25, panel.get_bottom()
        code = panel.code
        _l5, _l7 = code.code_lines[2], code.code_lines[4]       # one bar over lines 5-7
        g_bars = [Rectangle(width=code.background.width - 0.12, height=_l5.get_top()[1] - _l7.get_bottom()[1] + 0.14,
                            stroke_width=0).set_fill(TURN, 0.2)
                  .move_to([code.background.get_center()[0], (_l5.get_top()[1] + _l7.get_bottom()[1]) / 2, 0])]

        with self.voiceover(SAY[2]) as vo:
            old = list(t.lines.submobjects)               # a fresh screen for the new topic (as `clear`)
            self.play(FadeOut(relay), FadeOut(VGroup(*old)), run_time=0.45)
            for ln in old:
                t.lines.remove(ln)
                self.remove(ln)
            resize(self, t, ROWS_GIT, run_time=0.5)
            bare(self, t)                                 # the prompt waits at the top of the fresh screen
            vo.wait_until("An extra git status")
            c_gs = type_in(self, t, GST.cmd, 0.45)
            pin_tags(self, t, c_gs, extra_tag())
            g_out = print_in(self, t, GST_OUT, run_time=0.5)
            l8, l9, l13, l14 = g_out[3], g_out[4], g_out[7], g_out[8]
            vo.wait_until("your edited cli.py files")
            bars_on(self, [(l9, "transcribe_audio/cli.py")], run_time=0.5, extra=[FadeIn(gcap, shift=DOWN * 0.1)])
            vo.wait_until("and the files in generate text")
            bars_on(self, [(l8, "generate_text/pyproject.toml"), (l13, "generate_text/Dockerfile"),
                           (l14, "generate_text/uv.lock")])
            vo.wait_until("but the other four folders hide")
            resize(self, t, 3, keep=[c_gs, l13, l14], run_time=0.6)    # the caption stays while the terminal shrinks
            self.play(FadeOut(gcap), run_time=0.3)
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
        place(olds.boxes, cx=0, cy=0.85)
        olds.label.next_to(olds.boxes, DOWN, buff=0.18)
        pr_cap = words("removes the untagged older builds · each held your key", size=24)
        place(pr_cap, cx=0, bottom=olds.boxes.get_top()[1] + 0.3)
        disk = VGroup(words("still on disk: the base image (L4 uses it again) and the build cache", size=22),
                      words(("docker builder prune",), "frees it", size=22)).arrange(DOWN, buff=0.14)
        nocon = VGroup(check_mark(0.28, VENV), words("no containers left: every run used", ("--rm",), size=24, color=INK))
        nocon.arrange(RIGHT, buff=0.15)
        VGroup(disk, nocon).arrange(DOWN, buff=0.4).move_to([0, 0.2, 0])
        assert disk.get_right()[0] < EDGE and disk.get_left()[0] > -EDGE, disk.get_left()
        assert nocon.get_bottom()[1] > STRIP + 0.1, nocon.get_bottom()
        assert pr_cap.get_top()[1] < seen(corner).get_bottom()[1] - 0.1, pr_cap.get_top()

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(panel, ghosts, err, addf_g, crosses, not_these, lock, keep_ig, *g_bars, bar3)),
                      run_time=0.5)
            for b in g_bars + [bar3]:
                self.remove(b)
            resize(self, t, ROWS_FULL, run_time=0.6, extra=[FadeIn(relay)])
            c_rm = type_in(self, t, RM.cmd, 1.8)
            pin_tags(self, t, c_rm, extra_tag(), your_turn())
            make_room(self, t, len(RM_OUT))                  # one scroll for the whole output
            for j in range(5):                               # one pair a box: A..E dissolve as it prints
                print_with(self, t, RM_OUT[2 * j:2 * j + 2], run_time=0.38,
                           extra=[relay.boxes[j].animate.scale(0.3).set_opacity(0),
                                  relay.letters[j].animate.scale(0.3).set_opacity(0)])
            vo.wait_until("Older builds stay behind untagged")
            resize(self, t, 3, keep=list(t.lines.submobjects[-2:]), run_time=0.45)
            self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.15) for b in olds.boxes], lag_ratio=0.15),
                      FadeIn(olds.label), run_time=0.6)
            vo.wait_until("each holding your key")            # a key inside an image: RED (semantic table, S14)
            self.play(*[Indicate(b.key, color=ERR, scale_factor=1.4) for b in olds.boxes], run_time=0.6)
            vo.wait_until("so docker image prune")
            c_pr = type_in(self, t, PRUNE, 0.8)
            pin_tags(self, t, c_pr, extra_tag())
            self.play(FadeIn(pr_cap, shift=DOWN * 0.1), run_time=0.4)
            self.play(LaggedStart(*[b.animate.scale(0.3).set_opacity(0) for b in olds.boxes], lag_ratio=0.12),
                      olds.label.animate.set_opacity(0), run_time=0.8)
            self.play(FadeIn(disk, shift=UP * 0.1), run_time=0.5)
            self.play(Create(nocon[0]), FadeIn(nocon[1], shift=UP * 0.1), run_time=0.5)
            self.wait(2.4)                                    # the teardown checklist, before the recap

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
            s4, q5, th5, _ = step(q4, 4, top4, th4, thumb_sieve)
            smalls.append(s4)
            vo.wait_until("git-ignored key")
            self.play(Indicate(th5.key, color=ERR, scale_factor=1.35), run_time=0.7)   # the key inside an image: RED
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
        # exercises.md is in this video's folder, not in the tutorial repo: the study guide's §8 links it
        ans = S.text("Answers: study guide §8 (exercises.md)", 26, INK, t2f={"exercises.md": MONO})
        ans_box = box(ans.width + 0.7, ans.height + 0.45, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
        ans.move_to(ans_box)
        card1 = VGroup(ans_box, ans)
        g_head = label("Study guide + every command:", 26, INK)
        g_url = VGroup(mono(GUIDE_REPO, 20, INK), mono(GUIDE_PATH, 20, INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        g_body = VGroup(g_head, g_url).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        g_box = box(g_body.width + 0.7, g_body.height + 0.45, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
        g_body.move_to(g_box)
        card2 = VGroup(g_box, g_body)
        place(card1, left=-6.35, top=top - 0.2)
        card2.next_to(card1, DOWN, buff=0.25, aligned_edge=LEFT)
        n_head = VGroup(label("next:", 24, S.GREY), label("L4", 24, INK)).arrange(RIGHT, buff=0.14)
        n_head[1].align_to(n_head[0], DOWN)
        n_branch = words("branch", ("flexible-workflow",), size=20)
        n_items = VGroup(
            words("your own bucket + service account", size=20, color=INK),
            words("the key outside the repo", size=20, color=INK),
            VGroup(mono("docker-shell.sh", 20, INK), label("builds and runs for you", 20, INK))
            .arrange(DOWN, aligned_edge=LEFT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        n_body = VGroup(VGroup(n_head, n_branch).arrange(DOWN, aligned_edge=LEFT, buff=0.1), n_items)
        n_body.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        n_items.shift(RIGHT * 0.15)
        n_box = box(EDGE - card2.get_right()[0] - 0.35, n_body.height + 0.5, S.GREY, dashed=True)
        n_body.move_to(n_box).align_to(n_box, LEFT).shift(RIGHT * 0.3)
        nxt = VGroup(n_box, n_body)
        place(nxt, right=EDGE, top=card1.get_top()[1])
        assert card2.get_right()[0] < nxt.get_left()[0] - 0.2 and card2.get_bottom()[1] > -3.5, card2.get_right()
        assert card1.get_right()[0] < nxt.get_left()[0] - 0.2, (card1.get_right(), nxt.get_left())
        assert nxt.get_bottom()[1] > -3.5, nxt.get_bottom()
        assert n_body.get_right()[0] < n_box.get_right()[0] - 0.15, n_body.get_right()
        assert finals[-1].get_bottom()[1] > card1.get_top()[1] + 0.15

        with self.voiceover(SAY[7]) as vo:
            smalls.append(q5)                   # Q5 goes straight from its big form to the final layout
            self.play(FadeOut(th5, shift=RIGHT * 0.2), Transform(title, title2), Transform(t_ul, t_ul2),
                      LaggedStart(*[Transform(s.flat, f.flat) for s, f in zip(smalls, finals)], lag_ratio=0.12),
                      run_time=1.1)
            for s, f in zip(smalls, finals):
                self.swap_in(s, f)
            vo.wait_until("in the exercises")
            self.play(FadeIn(card1, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("every command is in the study guide")
            self.play(FadeIn(card2, shift=UP * 0.15), run_time=0.5)
            self.play(Indicate(g_url, color=TURN, scale_factor=1.04), run_time=0.7)
            vo.wait_until("Next lecture")
            self.play(FadeIn(n_box), FadeIn(n_head, shift=LEFT * 0.15), FadeIn(n_branch), run_time=0.5)
            for it, anchor in zip(n_items, ("your own bucket", "the key outside", "a script that builds")):
                vo.wait_until(anchor)
                self.play(FadeIn(it, shift=UP * 0.1), run_time=0.4)

        self.wait(0.8)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.9)
        self.wait(0.3)
