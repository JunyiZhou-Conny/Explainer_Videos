r"""S16 · Edit, apply, tear down, recap (port_toy README › Step 4 steps 3–5 and Handy commands; V6 + V8
coda; the five test-yourself questions; the L05 teaser). The end of part 2.

Beats (script.md "## S16", one voiceover block each):
 0  TRACKER P4/3. Terminal (full width, 12 rows, `laptop`, student@laptop:~/AC215/port_toy$). It types
    `docker compose up -d` -> port-laptop/55 lines 2–5 (each `✔` row's time is a GREY tag at the row's
    end); the prompt returns at once with the GREY tag "in the background"; the prompt flashes on "and
    returns your prompt".
 1  TRACKER PH/2 (the tracker switches section). The terminal shrinks to 6 rows. `docker compose logs -f
    gateway` -> 56b line 2 (the banner); a compact PAGE (localhost:8090) at the top right; its address
    bar is clicked (Send) and 56b line 3, the `POST` line, prints while the page fills with 56c's reply
    ("POST" YELLOW). On "Control C" 56b line 4 (`^C`) with the GREY tag "stops following · the app
    keeps running"; the prompt returns. TRACKER PH/3: the page leaves; `docker compose exec gateway sh`
    -> the frame turns TEAL (`container · gateway`), 56d lines 2–5 replayed (`#` prompt; `hostname`,
    `echo $PROCESSOR_HOST $PROCESSOR_PORT` typed). On "where the environment shows" `processor 9200`
    turns PINK and CODE(port_toy/docker-compose.yml: 19–21) drops in at the top right, its three lines
    barred PINK, a PINK link from the output line to it; `processor` and `"9200"` flash. The link goes,
    `exit` (56d line 6) is typed and the terminal is back on the laptop.
 2  TRACKER P4/3 (the tracker switches back). One-line README chip `README.md · line 487` "repeat the
    port experiments in docker-compose.yml" under the tracker; a small GREY editor ("in your editor")
    with CODE(port_toy/docker-compose.yml: 15–16, comment cut). TRACKER P4/3 · extra: a YELLOW pencil
    turns line 16's 8090 into 8095 (the edited line is the capture's own `+` line); `git diff` (extra)
    -> 57 lines 10–11 (cut), `-` RED, `+` GREEN, `8095` boxed YELLOW. TRACKER P4/3: the editor and the
    chip go, the terminal shrinks to a 4-row strip and V6 (the ToyNet as S14 left it: door
    127.0.0.1:8090, rooms :9100 / :9200, the toynet rail) appears above it. The strip types `docker
    compose up -d` -> 58 lines 2–4: `processor Running` GREEN, `gateway Started` and its `10.5s` YELLOW.
    On "Compose recreates only the gateway": a TEAL halo stays on the processor while the gateway box
    re-forms (fades, comes back, flashes) and the street door's label turns 127.0.0.1:8095.
 3  V6 leaves; a compact PAGE(59) (localhost:8095, the reply filled) at the centre, its address flashes.
    On "change it back": the page goes, the editor returns and the pencil turns 8095 back into 8090
    (the file's own line 16). On "and apply again": the strip types `docker compose up -d` -> 60 lines
    2–4 (same colours); the editor goes, V6 returns and the gateway re-forms with door 127.0.0.1:8090.
 4  TRACKER P4/4 · extra. V6 leaves; a GREY editor with processor/processor.py · line 45 and the GREY
    caption "edit: add `# edited` at the end · remove it when you're done" under it; the pencil writes
    lines 46–47 (a blank line and `# edited`, the capture's `+` lines; the header becomes "lines
    45–47"). The strip types `git diff` (extra) -> 61 lines 10–11, GREEN. On "We added a comment" the
    `+# edited` row flashes. TRACKER P4/4: the editor goes, the terminal grows to 13 rows and types
    `docker compose up -d --build` -> 62 lines 3, …, 21–24, …, 43–47 (BuildKit rows, times as GREY
    tags; the CACHED rows GREEN). On "only the copy layer is new" line 24 `[processor 4/4] COPY . .`
    and its time turn YELLOW, GREY tag "not CACHED"; on "and only the processor is recreated" line 46
    `gateway Running` GREEN, line 47 `processor Started` and `10.4s` YELLOW.
 5  The terminal shrinks to the 3-row strip. Tag `illustration · what if` (top band, right). Left
    column: CODE(port_toy/docker-compose.yml: 17–18, comment cut; line 18 barred PINK) and, under it,
    the excerpt chip `with open("index.html", "rb") as f:` (gateway/gateway.py · line 20 (excerpt)).
    Right column: the laptop (GREY frame "your laptop": `gateway/` · `index.html`, a browser glyph
    labelled "browser") above the gateway (TEAL frame "gateway": an `/app` window with `index.html` and
    `gateway.py`); the frames' names sit on their top edges. A PINK mount route runs from `gateway/`
    straight down to the `/app` window (it pulses; nothing travels). On "and it rereads its page on
    each load" the chip's `"index.html"` turns YELLOW. On "edits show on the next reload": a pencil
    edits the laptop's `index.html`, and both `index.html` rows blink YELLOW at once while the route
    pulses; the browser's reload arrow turns and a PINK request runs down to the gateway's `/app`. On
    "without a rebuild" the page's first line turns YELLOW and the GREY caption "no rebuild" appears
    beside the route (held 1.6 s).
 6  TRACKER P4/5. The picture goes; the terminal grows to 10 rows. `docker compose down` -> 64 lines
    2–5 (the two containers' `Removed` rows and `10.2s` tags turn YELLOW), `docker compose ps -a` -> 65
    line 2 (GREY tag "empty" beside the command). TRACKER P4/5 · extra: README chip `README.md · line
    515` "The built images remain." in the top band; `docker image ls` (extra) -> 66 lines 2–8 as the
    column view (GREY tag "2 of 5 columns" on its header row); `port_toy-*` and `toy-*` turn YELLOW and
    their `198MB` too, a GREY bracket "shared
    layers · ≈ 200 MB in all". On "remove them to free space" the GREY note "docker image rm <name> ·
    if you want the space" and the GREY command-only chip "hello-world's exited container: docker ps
    -a, then docker rm <its ID>" (tag `extra`); on "Port toy costs nothing" the GREEN chip "port_toy
    costs nothing". On "Pause and shut it down" the terminal goes and the static GREY your-turn card
    (`docker compose down`, `docker compose ps -a`, `docker image ls` extra) takes its place.
 7  Everything goes (the tracker too). "Test yourself" (40 pt, YELLOW underline) at the top. Q1 writes
    in at 26 pt in the centre with a YELLOW number badge and, at its left, a glyph-only icon of V1 (the
    BLUE shelf, the sealed TEAL box, the PINK signpost whose pointer aims at it). On "which files
    define" the box flashes; on "and what does run use" `run` turns YELLOW and the pointer flashes.
 8  Q1 slides up and fades as Q2 writes in (icon: V3's three gates, a key outline in a dashed slot, a
    padlock, a switch, then a BLUE door, a PINK route through them): the gates pulse in turn, then
    flash RED in turn ("where does each one fail"). Q3 (icon: V5's COPY arrow carrying the GOLD key
    from a GREY folder into a TEAL image slab): the key rides the arrow into the slab and turns RED;
    on "and what's the fix" the folder and the key flash.
 9  Q4 (icon: V7's street door in the dashed wall, a PINK arrow through it into a TEAL box's room
    door): `-p 127.0.0.1:8095:9100`'s three numbers flash as they are read; then the flag (with the
    icon's street door), `gateway.py` (with the room door) and the second `127.0.0.1` flash as each
    question part is asked. Q5 (icon: V6's two boxes with
    their localhost loops and the PINK phone book on the rail): the loops glow YELLOW on "what is
    localhost", the phone book pulses on "which name reaches the processor".
10  The last question and the title fade. A GREY dashed teaser (tag "L05 · llm-rag"): a TEAL box "CLI"
    and a TEAL box "ChromaDB" on a dashed TEAL rail "Compose network"; a PINK arrow "by name" from CLI
    to ChromaDB; a GREY `secrets/` folder with the GOLD key at the left, a PINK `../secrets` route to
    the CLI box pulses and a GOLD key outline appears inside it (the key stays where it is). Two
    footer cards: "Answers: exercises.md" and "Study guide + every command:" with the MLOps_Learning
    link and the guide's path. Everything fades to an empty frame (end of part 2).

Deviations from SHOW (and why):
- Beats 1–2: the 12-row terminal of beat 0 shrinks to 6 rows: the compact page, the docker-compose.yml
  chip, the README chip and the editor need the frame above it (a 12-row terminal leaves 0.7 units).
- `✔` rows (Compose's progress rows, 79–82 characters) are printed like BuildKit rows: the text
  without its time field, the time as a GREY tag at the row's end (it is the tag that highlights).
  build_row() only splits `=>` rows, so this scene splits `✔` rows itself (row_split).
- Beats 2–3: the strip under V6 has 4 rows, not 3: `docker compose up -d` and its three output lines
  stay together (with 3 rows the command scrolls away the moment its output prints).
- Beat 3: the page, the editor and V6 take turns above the strip (each needs the full width).
- Beat 4: the terminal grows to 13 rows, not 12: the build command and its 12 listed rows stay on
  screen together; the prompt does not return after the build (it would scroll the command away).
  A GREY tag "not CACHED" names why line 24 is YELLOW.
- Beat 5: gateway.py line 20 is an excerpt chip (the line without its 8-space indent) under the
  docker-compose.yml panel, not a code panel beside it: the two panels side by side are 12.9 wide
  (the panel headers), wider than the frame. The picture is drawn vertically (laptop above the
  gateway) in the right column.
- Beat 6: the `▶ your turn` sits on a static your-turn card (script conventions: the down command has
  scrolled away under `docker image ls` by the time the SAY says "pause"). The image list's slicing is
  named by a GREY tag "2 of 5 columns" on its header row (a longer tag does not fit beside it). The
  `docker compose ps -a` header fills all 65 columns, so its "empty" tag sits beside the command.
- Beats 7–9: each question has a YELLOW number badge (the narration counts "One", "Two", …), and each
  icon sits in a small dark card. Highlights follow the words being said and never mark an answer.
  The old question slides up and has mostly left before the next one writes in (lagged, so the two
  never overlap).
- Beat 10: the TEAL boxes and the rail are dashed (a future thing: GREY dashed in the colour table).
"""

import re

import numpy as np
from common import (
    CTR,
    ERR,
    HUB,
    INK,
    LAPTOP,
    LOOKUP,
    NARRATION,
    P_TOY,
    STRIP_TOP,
    TURN,
    VENV,
    PortPage,
    ToyNet,
    _header_text,
    _hidden,
    _keep,
    bare_prompt,
    beside,
    build_row,
    caption_extra,
    capture,
    column_view,
    cut_comment,
    door,
    editor_inset,
    enter_container,
    excerpt,
    excerpt_chip,
    extra_tag,
    fix_chip,
    grey_tag,
    illustration_tag,
    key_glyph,
    key_outline,
    leave_container,
    loop_glyph,
    note,
    padlock,
    page_reply,
    pencil,
    pin,
    place_time,
    readme_chip,
    resize,
    sans,
    sealed_box,
    session,
    src_panel,
    strip_top,
    switch_section,
    term,
    time_tag,
    toggle,
    tracker,
    turn_card,
    type_cmd,
    unpin,
)
from manim import (
    DOWN,
    LEFT,
    PI,
    RIGHT,
    UL,
    UP,
    AnimationGroup,
    Arc,
    Arrow,
    Create,
    DashedLine,
    FadeIn,
    FadeOut,
    Group,
    Indicate,
    LaggedStart,
    Line,
    Polygon,
    Rectangle,
    RoundedRectangle,
    Transform,
    VGroup,
    VMobject,
    Write,
)

from explainer import style as S
from explainer.devops import (
    MONO,
    OUTPUT,
    box,
    code_panel,
    file_glyph,
    folder_glyph,
    label,
    mono,
    mono_line,
    step_badge,
    substring,
)
from explainer.scene import VoiceScene

SAY = NARRATION["S16"]
assert len(SAY) == 11, len(SAY)

# ------------------------------------------------------------------ captures (file line numbers)
PL = "port-laptop"
TOY = "port_toy/README.md"
COMPOSE = "port_toy/docker-compose.yml"
GW_PY = "port_toy/gateway/gateway.py"
PROC_PY = "port_toy/processor/processor.py"
C55, C56B, C56C, C56D, C57, C58 = (capture(n, PL) for n in ("55", "56b", "56c", "56d", "57", "58"))
C59, C60, C61, C62, C64, C65, C66 = (capture(n, PL) for n in ("59", "60", "61", "62", "64", "65", "66"))

UP_D = C55.cmd
assert UP_D == "docker compose up -d" == excerpt(TOY, 492, 492) == C58.cmd == C60.cmd
UP_BUILD = C62.cmd
assert UP_BUILD == "docker compose up -d --build" == excerpt(TOY, 500, 500)
LOGS_F, EXEC_SH = C56B.cmd, C56D.cmd
assert f"`{LOGS_F}`" in excerpt(TOY, 572, 572) and LOGS_F == "docker compose logs -f gateway"
assert f"`{EXEC_SH}`" in excerpt(TOY, 573, 573) and EXEC_SH == "docker compose exec gateway sh"
DOWN_CMD, PS_A = C64.cmd, C65.cmd
assert DOWN_CMD == "docker compose down" == excerpt(TOY, 512, 512)
assert PS_A == "docker compose ps -a" == excerpt(TOY, 524, 524)
DIFF = C57.cmd
assert DIFF == "git diff" == C61.cmd
IMG_LS = C66.cmd
assert IMG_LS == "docker image ls"
assert C56B.line(4) == "^C" and '"POST / HTTP/1.1"' in C56B.line(3)
assert C56D.line(5) == "processor 9200"
R56, R59 = page_reply(C56C, 2), page_reply(C59, 2)
assert R56["upper"] == R59["upper"] == "HELLO FROM THE LAPTOP"
assert "repeat the port experiments in `docker-compose.yml`" in excerpt(TOY, 487, 487)
assert "The built images remain." in excerpt(TOY, 515, 515)

# the editors: docker-compose.yml lines 15–16 before / after (the capture's own `+` line)
E_BEFORE = excerpt(COMPOSE, 15, 16, cut_comments=True).split("\n")
assert C57.line(10)[1:] == excerpt(COMPOSE, 16, 16)
E_AFTER = [E_BEFORE[0], cut_comment(C57.line(11)[1:])]
assert E_AFTER[1] == E_BEFORE[1].replace("8090", "8095"), E_AFTER
# processor/processor.py: line 45, then the two lines the capture's diff adds
P_LINE45 = excerpt(PROC_PY, 45, 45)
assert C61.line(9)[1:] == P_LINE45 and C61.line(10) == "+" and C61.line(11) == "+# edited"
P_AFTER = [P_LINE45, C61.line(10)[1:], C61.line(11)[1:]]
# docker compose up -d --build: the listed rows
B_ROWS = [C62.line(3), "…", *C62.at((21, 24)), "…", *C62.at((43, 47))]
assert "[processor 4/4] COPY . ." in C62.line(24) and "CACHED" not in C62.line(24)
assert all("CACHED" in C62.line(n) for n in (21, 22, 23))
assert "gateway" in C62.line(46) and "Running" in C62.line(46) and "Started" in C62.line(47)
# the mount
VOL = excerpt(COMPOSE, 17, 18, cut_comments=True).split("\n")
assert VOL[1].strip().startswith("- ./gateway:/app")
L20 = excerpt(GW_PY, 20, 20)
OPEN20 = 'with open("index.html", "rb") as f:'
assert OPEN20 == L20.strip()
# docker image ls, column view
IMG_ROWS = column_view(C66.at((2, 8)))
assert IMG_ROWS[0].startswith("IMAGE") and IMG_ROWS[0].endswith("DISK USAGE")
SHARED = {2: "port_toy-gateway", 3: "port_toy-processor", 5: "toy-gateway", 6: "toy-processor"}
for _k, _n in SHARED.items():
    assert IMG_ROWS[_k].startswith(_n + ":latest") and IMG_ROWS[_k].endswith("198MB"), IMG_ROWS[_k]
assert IMG_ROWS[4].startswith("python:3.14-slim") and IMG_ROWS[1].startswith("hello-world")

GUIDE_REPO = "github.com/JunyiZhou-Conny/MLOps_Learning"
GUIDE_PATH = "guides/L04-containers-2b-flexible-workflow-ports.md"

# the five questions (script.md S16 SHOW, on screen); code spans in the code font
QUESTIONS = [
    ("Which files define a mega-pipeline image? What does run use when there's no local image?", ["run"]),
    ("Which three gates must a call to your bucket pass, and where does each one fail?", []),
    ("How does a git-ignored key end up in an image? The fix?", []),
    (("In -p 127.0.0.1:8095:9100: which number does the browser use, which does gateway.py bind, "
      "and what does 127.0.0.1 restrict?"), ["-p 127.0.0.1:8095:9100", "gateway.py", "127.0.0.1"]),
    ("Inside the gateway, what is localhost, and which name reaches the processor?", ["localhost"]),
]

# ------------------------------------------------------------------ layout
TOP = 2.84                        # top of anything under the tracker (its bottom is 2.905)
T6, T10 = strip_top(6), strip_top(10)
STRIP4 = strip_top(4)             # -1.04: V6 sits on it
BAND_Y = 3.2                      # the top band, right of the tracker (its right edge is -0.48)
X_L, X_R = -6.45, 6.45
Q_SIZE, Q_W = 26, 8.4             # questions
THUMB_W, THUMB_H = 2.6, 1.9
NBSP = " "


# ------------------------------------------------------------------ small helpers
def flash(m, color: str = TURN, k: float = 1.12, run_time: float = 0.7):
    return Indicate(m, color=color, scale_factor=k, run_time=run_time)


def glyph_box(line, sub: str, color: str = TURN, pad: float = 0.04, occurrence: int = 0):
    """A box around the glyphs of `sub` in a mono line, as tall as the row (not added)."""
    g = substring(line, sub, occurrence)
    r = box(g.width + 2 * pad + 0.04, line.strut.height + 0.04, color, fill_opacity=0.0, radius=0.06,
            stroke=3)
    return r.move_to([g.get_center()[0], line.strut.get_center()[1], 0])


def text_span(txt, s: str, sub: str) -> VGroup:
    """The glyphs of `sub` in a one-line Text `txt` built from string `s` (spaces have no glyphs)."""
    i = s.index(sub)
    a = len("".join(s[:i].split()))
    return VGroup(*txt.submobjects[a:a + len("".join(sub.split()))])


def type_extra(scene, t, cmd: str, type_time: float | None = None):
    """Type an extra command (not in the README) with a GREY `extra` tag pinned beside it."""
    ln = type_cmd(scene, t, cmd, type_time=type_time)
    tg = beside(extra_tag(), t, ln, buff=0.4)
    pin(scene, ln, tg, run_time=0.25)
    return ln


_DONE = re.compile(r"^( ✔ .*?)\s+(\d+(?:\.\d+)?s)$")


def row_split(s: str, width: int):
    """A progress row -> (text, time | None). Compose's `✔` rows (' ✔ Container gateway   Started
    …   10.5s') lose their time field as BuildKit's `=>` rows do (build_row); others are cut."""
    m = _DONE.match(s.rstrip())
    if m:
        txt = m.group(1).rstrip()
        return (txt if len(txt) <= width else txt[:width - 1] + "…"), m.group(2)
    if s.lstrip().startswith("=>"):
        return build_row(s, width)
    return (s if len(s) <= width + 7 else s[:width + 6] + "…"), None


def print_rows(scene, t, rows: list, run_time: float = 0.6, lag: float = 0.12) -> VGroup:
    """Print progress rows (raw capture lines, "…", or (line, colour)); a row's time becomes a GREY
    time tag at the row's right end, part of the row (.time_tag; None without a time)."""
    items = []
    for r in rows:
        s, col = (r, OUTPUT) if isinstance(r, str) else r
        txt, tm = ("…", None) if s == "…" else row_split(s, t.max_chars - 7)
        items.append((txt, col, tm))
    t._make_room(scene, len(items))
    new = VGroup()
    for txt, col, tm in items:
        ln = mono_line(txt, t.size, col)
        t._place(ln, len(t.lines))
        ln.time_tag = None
        if tm:
            tg = time_tag(tm)
            place_time(tg, t, ln)
            ln.add(tg)
            ln.time_tag = tg
        t.lines.add(ln)
        new.add(ln)
    scene.play(LaggedStart(*[FadeIn(m) for m in new], lag_ratio=lag), run_time=run_time)
    return new


def paint(row, color: str):
    """Animations: a printed row's glyphs (and its time tag) turn `color`."""
    anims = [row.glyphs.animate.set_color(color)]
    if getattr(row, "time_tag", None) is not None:
        anims += [row.time_tag.box.animate.set_stroke(color), row.time_tag.text.animate.set_color(color)]
    return anims


def place(m, left=None, right=None, top=None, bottom=None, cx=None, cy=None):
    if left is not None:
        m.shift(RIGHT * (left - m.get_left()[0]))
    if right is not None:
        m.shift(RIGHT * (right - m.get_right()[0]))
    if cx is not None:
        m.shift(RIGHT * (cx - m.get_center()[0]))
    if top is not None:
        m.shift(UP * (top - m.get_top()[1]))
    if bottom is not None:
        m.shift(UP * (bottom - m.get_bottom()[1]))
    if cy is not None:
        m.shift(UP * (cy - m.get_center()[1]))
    return m


def mixed(parts, size: float = 20, color: str = S.GREY):
    """A one-line caption of serif and mono pieces on one baseline: parts = [(text, "mono"|"serif"),
    …], joined by spaces (no space before a piece starting with "," or ".")."""
    s = ""
    for txt, _ in parts:
        s += txt if (not s or txt[0] in ",.") else " " + txt
    t2f = {txt: MONO for txt, kind in parts if kind == "mono"}
    return _keep(S.text(s, size, color, t2f=t2f))


def mixed_chip(parts, color: str = S.GREY, size: float = 20) -> VGroup:
    """A GREY chip holding a mixed caption (serif + mono). .box .text"""
    t = mixed(parts, size, INK)
    h = mono("|", size).height + 0.24
    b = box(t.width + 0.48, h, color, fill_opacity=0.12, radius=h / 2.6)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return _keep(g)


def editor(rows: list[str], path: str, first: int, header: str, language: str = "yaml") -> VGroup:
    """A GREY editor ("in your editor") around a code panel of `rows` (file lines from `first`),
    headed `header`. .panel (.code .header) .frame"""
    p = code_panel("\n".join(rows), path, first, language, font_size=20)
    hd = _header_text(header)
    hd.next_to(p.code, UP, buff=0.1).align_to(p.code, LEFT).shift(RIGHT * 0.12)
    p.remove(p.header)
    p.header = hd
    p.add(hd)
    ed = editor_inset(p)
    ed.panel = p
    return ed


def pen_to(pen, target, run_time: float = 0.45):
    """Animation: the pencil's tip moves to just above-right of `target`'s right end."""
    tip = target.get_right() + np.array([0.04, 0.06, 0])
    return pen.animate(run_time=run_time).shift(tip - pen.tip_point())


# ------------------------------------------------------------------ question text (L01/L03's helpers)
def text_line(s: str, size: float, color: str, code=()) -> VGroup:
    """One line of house-font text whose code spans use the code font, with a FIXED vertical
    extent (built with a leading '|' that is dropped, as mono_line does). .glyphs .strut"""
    spans: list[tuple[int, int]] = []                  # every occurrence, longest first, no overlaps
    for c in sorted(code, key=len, reverse=True):
        i = s.find(c)
        while i >= 0:
            if all(i + len(c) <= a or i >= b for a, b in spans):
                spans.append((i, i + len(c)))
            i = s.find(c, i + 1)
    t2f = {f"[{a + 1}:{b + 1}]": MONO for a, b in spans}   # +1: the leading '|'
    t = S.text("|" + s, size, color, t2f=t2f)
    pipe = t.submobjects[0]
    strut = Rectangle(width=max(0.01, t.width), height=pipe.height, stroke_width=0, fill_opacity=0)
    strut.move_to(pipe.get_center()).align_to(t, LEFT)
    gl = VGroup(*t.submobjects[1:])
    strut.stretch_to_fit_width(max(0.01, gl.width)).align_to(gl, LEFT)
    g = VGroup(strut, *gl.submobjects)
    g.glyphs, g.strut = VGroup(*gl.submobjects), strut
    return g


def _line_width(s: str, size: float, code: tuple) -> float:
    return text_line(s, size, INK, code).glyphs.width


def wrap_lines(s: str, size: float, width: float, code=()) -> list:
    """Greedy-balanced wrap at spaces; a code span (its spaces made non-breaking) is never split;
    a new sentence starts a new line when that costs no extra line."""
    code = tuple(code)
    for c in code:
        s = s.replace(c, c.replace(" ", NBSP))

    def layout(text):
        words = text.split(" ")
        lines, cur = [], ""
        for w in words:
            trial = f"{cur} {w}" if cur else w
            if cur and _line_width(trial.replace(NBSP, " "), size, code) > width:
                lines.append(cur)
                cur = w
            else:
                cur = trial
        return lines + [cur]

    whole = layout(s)
    sentences = re.split(r"(?<=[.?]) (?=[A-Z0-9])", s)
    if len(sentences) > 1:
        per = [ln for sen in sentences for ln in layout(sen)]
        if len(per) <= len(whole):
            whole = per
    return [ln.replace(NBSP, " ") for ln in whole]


def question(i: int, width: float = Q_W) -> VGroup:
    """Question i (1-based) at 26 pt: wrapped rows, the YELLOW number badge left of the first row.
    The text's top-left is at the origin. .badge .lines .strs .text"""
    s, code = QUESTIONS[i - 1]
    strs = wrap_lines(s, Q_SIZE, width, code)
    assert " ".join(strs) == s, (strs, s)
    rows = [text_line(ln, Q_SIZE, INK, code) for ln in strs]
    pitch = rows[0].strut.height * 1.25
    for k, r in enumerate(rows):
        r.shift(np.array([-r.strut.get_left()[0], -k * pitch - r.strut.get_top()[1], 0]))
    txt = VGroup(*rows)
    b = step_badge(i, TURN, size=22, radius=0.24)
    b.move_to([-0.25 - 0.24, rows[0].strut.get_center()[1], 0])
    g = VGroup(b, txt)
    g.badge, g.text, g.lines, g.strs = b, txt, rows, strs
    return g


LIGATURES = ("ff", "fi", "fl")            # the serif font joins these into one glyph


def q_span(q: VGroup, sub: str, occurrence: int = 0) -> VGroup:
    """The glyphs of `sub` in question q (a span never crosses a line break). A ligature before the
    span shifts the count, so a span is counted from the line's end when the line has one (asserting
    no ligature follows it in that line)."""
    key = "".join(sub.split())
    seen = 0
    for r, s in zip(q.lines, q.strs):
        flat = "".join(s.split())
        i = flat.find(key)
        while i >= 0 and seen < occurrence:
            seen += 1
            i = flat.find(key, i + 1)
        if i < 0:
            continue
        n = len(r.glyphs)
        if n == len(flat):
            return VGroup(*r.glyphs[i:i + len(key)])
        tail = flat[i + len(key):]
        assert not any(lg in tail for lg in LIGATURES), (sub, s)
        j = n - len(tail) - len(key)
        return VGroup(*r.glyphs[j:j + len(key)])
    raise AssertionError((sub, q.strs))


# ------------------------------------------------------------------ icons (glyph-only, no text)
def thumb(content: VGroup) -> VGroup:
    """A small dark card holding a text-free icon (scaled to fit). .frame .content"""
    fr = box(THUMB_W, THUMB_H, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
    k = min((THUMB_W - 0.45) / content.width, (THUMB_H - 0.45) / content.height, 1.0)
    content.scale(k).move_to(fr)
    g = VGroup(fr, content)
    g.frame, g.content = fr, content
    return g


def icon_build_pull() -> VGroup:
    """Q1 · V1: the BLUE shelf, a sealed TEAL box on it, the PINK signpost board (two bars, no text)
    on its stick, its pointer aiming at the box. .box .pointer .board"""
    shelf = Line(LEFT * 1.25, RIGHT * 1.25, color=HUB, stroke_width=5)
    legs = VGroup(*[Line([x, 0, 0], [x, -0.2, 0], color=HUB, stroke_width=3) for x in (-1.1, 1.1)])
    bx = sealed_box(0.95, CTR).next_to(shelf, UP, buff=0.03).align_to(shelf, RIGHT).shift(LEFT * 0.2)
    w, h, tip = 1.15, 0.46, 0.24
    board = Polygon([0, 0, 0], [w, 0, 0], [w + tip, h / 2, 0], [w, h, 0], [0, h, 0],
                    stroke_color=LOOKUP, stroke_width=3).set_fill(LOOKUP, 0.12)
    bars = VGroup(Line(LEFT * 0.4, RIGHT * 0.4), Line(LEFT * 0.4, RIGHT * 0.1)).set_stroke(LOOKUP, 3)
    bars.arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to(board).shift(LEFT * 0.1)
    sign = VGroup(board, bars).move_to([-0.55, 1.45, 0])
    stick = Line([board.get_left()[0] + 0.22, board.get_bottom()[1], 0], [board.get_left()[0] + 0.22, 0, 0],
                 color=LOOKUP, stroke_width=4)
    pointer = Arrow(board.get_right() + RIGHT * 0.02, bx.get_top() + UP * 0.06, buff=0.02, color=LOOKUP,
                    stroke_width=4, max_tip_length_to_length_ratio=0.3)
    g = VGroup(shelf, legs, stick, sign, bx, pointer)
    g.box, g.pointer, g.board = bx, pointer, sign
    return g


def icon_gates() -> VGroup:
    """Q2 · V3: a dashed TEAL slot holding a GOLD key outline (who?), a BLUE padlock (may?), a BLUE
    switch (switched on?), then a BLUE door; a PINK route runs under them to the door. .gates"""
    slot = box(0.7, 0.55, CTR, fill_opacity=0, dashed=True, radius=0.08)
    ko = key_outline(0.24).move_to(slot)
    g1 = VGroup(slot, ko)
    g2 = padlock(0.5)
    g3 = toggle(True, w=0.62)
    dr = RoundedRectangle(width=0.55, height=0.85, corner_radius=0.06, stroke_color=HUB,
                          stroke_width=3).set_fill(HUB, 0.2)
    row = VGroup(g1, g2, g3, dr).arrange(RIGHT, buff=0.35)
    y = row.get_bottom()[1] - 0.22
    route = Arrow([row.get_left()[0] - 0.1, y, 0], [dr.get_center()[0], y, 0], buff=0, color=LOOKUP,
                  stroke_width=4, max_tip_length_to_length_ratio=0.08)
    g = VGroup(row, route)
    g.gates = [g1, g2, g3]
    g.door = dr
    return g


def icon_copy_key() -> VGroup:
    """Q3 · V5 (S09): a GREY folder with the GOLD key beside it, a GREY COPY arrow down into a TEAL
    image slab; the key sits on the arrow's start. .key .slab .arrow .folder"""
    fold = folder_glyph(0.5, LAPTOP)
    slab = box(2.4, 0.5, CTR, fill_opacity=0.25, radius=0.06).next_to(fold, DOWN, buff=1.0)
    slab.align_to(fold, LEFT).shift(LEFT * 0.3)
    ar = Arrow(fold.get_bottom() + DOWN * 0.05, [fold.get_center()[0], slab.get_top()[1] + 0.04, 0],
               buff=0, color=S.GREY, stroke_width=5, max_tip_length_to_length_ratio=0.25)
    k = key_glyph(0.3).next_to(fold, RIGHT, buff=0.2)
    g = VGroup(fold, slab, ar, k)
    g.key, g.slab, g.arrow, g.folder = k, slab, ar, fold
    return g


def icon_door_room() -> VGroup:
    """Q4 · V7: the laptop's dashed GREY wall with a GREY street door; a PINK arrow through it into
    the TEAL room door on a TEAL box's left wall. .street .room .arrow"""
    wall = DashedLine([0, 0.75, 0], [0, -0.75, 0], color=LAPTOP, stroke_width=3, dash_length=0.12)
    st = door(0.32, 0.52, LAPTOP).move_to([0, 0, 0])
    bx = box(1.35, 1.35, CTR, fill_opacity=0.08).move_to([1.6, 0, 0])
    rm = door(0.28, 0.46, CTR).move_to([bx.get_left()[0], 0, 0])
    ar = Arrow([-1.2, 0, 0], [rm.get_left()[0] - 0.02, 0, 0], buff=0, color=LOOKUP, stroke_width=4,
               max_tip_length_to_length_ratio=0.12)
    g = VGroup(wall, bx, ar, st, rm)
    g.street, g.room, g.arrow = st, rm, ar
    return g


def icon_loops_book() -> VGroup:
    """Q5 · V6: two TEAL boxes, each with its own localhost loop, on a TEAL rail with the PINK phone
    book between them. .loops .book"""
    bxs = VGroup(*[box(1.05, 0.9, CTR, fill_opacity=0.08).move_to([x, 0.35, 0]) for x in (-1.0, 1.0)])
    loops = VGroup(*[loop_glyph(0.2, CTR).move_to(b) for b in bxs])
    rail = Line([-1.6, -0.45, 0], [1.6, -0.45, 0], color=CTR, stroke_width=6)
    plugs = VGroup(*[Line(b.get_bottom(), [b.get_center()[0], -0.45, 0], color=CTR, stroke_width=4) for b in bxs])
    book = VGroup(Rectangle(width=0.42, height=0.32, stroke_color=LOOKUP, stroke_width=2.5).set_fill(LOOKUP, 0.25),
                  Line([0, 0.16, 0], [0, -0.16, 0], color=LOOKUP, stroke_width=2)).move_to([0, -0.2, 0])
    g = VGroup(rail, plugs, bxs, loops, book)
    g.loops, g.book, g.boxes = loops, book, bxs
    return g


# ------------------------------------------------------------------ the beat-5 picture (illustration)
def browser_glyph(w: float = 1.5, h: float = 1.0) -> VGroup:
    """A text-free browser: frame, bar, a reload arrow in the bar, three page lines. .lines .reload"""
    fr = RoundedRectangle(width=w, height=h, corner_radius=0.08, stroke_color=LAPTOP,
                          stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
    bar_y = fr.get_top()[1] - 0.24
    bar = Line([fr.get_left()[0], bar_y, 0], [fr.get_right()[0], bar_y, 0], color=LAPTOP, stroke_width=2)
    rl = Arc(radius=0.07, start_angle=PI * 0.3, angle=PI * 1.5, stroke_color=LAPTOP, stroke_width=2.5)
    rl.add_tip(tip_length=0.06, tip_width=0.06)
    rl.move_to([fr.get_left()[0] + 0.18, fr.get_top()[1] - 0.12, 0])
    lines = VGroup(*[Line(LEFT * (w * 0.36), RIGHT * (w * 0.36 - (0.25 if k == 2 else 0)), color=S.GREY,
                          stroke_width=4) for k in range(3)]).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
    lines.move_to([fr.get_center()[0], (bar_y + fr.get_bottom()[1]) / 2, 0])
    g = VGroup(fr, bar, rl, lines)
    g.frame, g.lines, g.reload = fr, lines, rl
    return g


def file_mark(name: str, color: str = INK, glyph_color: str = S.GREY, folder: bool = False) -> VGroup:
    gl = folder_glyph(0.22, glyph_color) if folder else file_glyph(0.28, glyph_color)
    t = mono(name, 20, color).next_to(gl, RIGHT, buff=0.12)
    g = VGroup(gl, t)
    g.glyph, g.text = gl, t
    return g


def edge_label(txt, frame, x: float) -> VGroup:
    """A frame's name sitting on its top edge (on a background patch), left end at x."""
    bg = Rectangle(width=txt.width + 0.3, height=txt.height + 0.12, stroke_width=0).set_fill(S.BG, 1)
    g = VGroup(bg, txt.move_to(bg))
    return g.move_to([x + g.width / 2, frame.get_top()[1], 0])


def mount_picture(x0: float, x1: float, top: float) -> VGroup:
    """Beat 5 (illustration), drawn inside x0..x1 from `top` down (3.8 tall): the laptop (GREY frame
    "your laptop": gateway/ with its index.html, a browser glyph labelled under it) above the
    gateway container (TEAL frame "gateway": an /app window holding index.html and gateway.py), a
    PINK mount route from gateway/ straight down to /app. Frame names sit on the top edges.
    .lap .ctr .lap_html .ctr_html .route .browser .browser_label .app .gap_y"""
    w, cx = x1 - x0, (x0 + x1) / 2
    lap_h, gap, ctr_h = 1.6, 0.6, 1.6
    lf = box(w, lap_h, LAPTOP, fill_opacity=0.04).move_to([cx, top - lap_h / 2, 0])
    lt = edge_label(sans("your laptop", 20, LAPTOP), lf, x0 + 0.3)
    fx = x0 + 1.0
    fg = file_mark("gateway/", INK, LAPTOP, folder=True).move_to([fx, top - 0.5, 0], aligned_edge=LEFT)
    fh = file_mark("index.html", INK, LAPTOP).move_to([fx + 0.42, top - 1.0, 0], aligned_edge=LEFT)
    brw = browser_glyph(1.3, 0.85).move_to([x1 - 0.95, top - 0.6, 0])
    bl = sans("browser", 20, LAPTOP).next_to(brw, DOWN, buff=0.08)
    lap = VGroup(lf, fg, fh, brw, bl, lt)
    c_top = top - lap_h - gap
    cf = box(w, ctr_h, CTR, fill_opacity=0.05).move_to([cx, c_top - ctr_h / 2, 0])
    ct = edge_label(mono("gateway", 20, CTR), cf, x0 + 3.2)
    app = box(w - 0.4, ctr_h - 0.45, CTR, fill_opacity=0.08, radius=0.08)
    app.move_to([cx, c_top - 0.25 - app.height / 2, 0])
    at = mono("/app", 20, CTR).move_to(app.get_corner(UL) + np.array([0.18, -0.24, 0]), aligned_edge=LEFT)
    ch = file_mark("index.html", INK, CTR).move_to([fx, app.get_center()[1] - 0.15, 0], aligned_edge=LEFT)
    cg = file_mark("gateway.py", INK, CTR).move_to([x0 + 3.3, ch.get_center()[1], 0], aligned_edge=LEFT)
    ctr = VGroup(cf, app, at, ch, cg, ct)
    rx = fg.glyph.get_center()[0]
    route = Line([rx, fg.glyph.get_bottom()[1] - 0.04, 0], [rx, app.get_top()[1], 0], color=LOOKUP,
                 stroke_width=5)
    g = VGroup(lap, ctr, route)
    g.lap, g.ctr, g.lap_html, g.ctr_html, g.route, g.browser = lap, ctr, fh, ch, route, brw
    g.browser_label, g.lap_frame, g.ctr_frame, g.app = bl, lf, cf, app
    g.gap_y = top - lap_h - gap / 2
    return g


# ------------------------------------------------------------------ the L05 teaser and the footer
def teaser() -> VGroup:
    """Beat 10: the GREY dashed teaser (tag "L05 · llm-rag"): the laptop's secrets/ with the GOLD key,
    a PINK ../secrets route into a dashed TEAL box "CLI", a PINK "by name" arrow to a dashed TEAL box
    "ChromaDB", both on a dashed TEAL rail "Compose network". .frame .tag .cli .db .rail .route
    .call .ghost .secrets"""
    fr = box(11.6, 3.2, S.GREY, dashed=True, stroke=2.5)
    tg = grey_tag("L05 · llm-rag").move_to(fr.get_corner(UL) + np.array([1.2, 0, 0]))
    sec_g = folder_glyph(0.3, LAPTOP)
    sec_t = mono("secrets/", 20, LAPTOP).next_to(sec_g, RIGHT, buff=0.12)
    k = key_glyph(0.26).next_to(VGroup(sec_g, sec_t), DOWN, buff=0.22).align_to(sec_g, LEFT)
    secrets = VGroup(sec_g, sec_t, k).move_to([fr.get_left()[0] + 1.25, 0.25, 0])
    cli = box(2.5, 1.5, CTR, fill_opacity=0, dashed=True, stroke=3).move_to([-0.25, 0.35, 0])
    cli_t = sans("CLI", 22, CTR).move_to(cli.get_corner(UL) + np.array([0.3, -0.28, 0]), aligned_edge=LEFT)
    db = box(2.8, 1.5, CTR, fill_opacity=0, dashed=True, stroke=3).move_to([4.05, 0.35, 0])
    db_t = sans("ChromaDB", 22, CTR).move_to(db.get_corner(UL) + np.array([0.3, -0.28, 0]), aligned_edge=LEFT)
    rail_y = -0.85
    rail = DashedLine([cli.get_left()[0] - 0.2, rail_y, 0], [db.get_right()[0] + 0.2, rail_y, 0], color=CTR,
                      stroke_width=5, dash_length=0.16)
    rail_t = sans("Compose network", 20, CTR).next_to(rail, DOWN, buff=0.1).align_to(rail, RIGHT)
    plugs = VGroup(*[DashedLine([b.get_center()[0], b.get_bottom()[1], 0], [b.get_center()[0], rail_y, 0],
                                color=CTR, stroke_width=3, dash_length=0.08) for b in (cli, db)])
    call = Arrow(cli.get_right() + RIGHT * 0.05, db.get_left() + LEFT * 0.05, buff=0, color=LOOKUP,
                 stroke_width=5, max_tip_length_to_length_ratio=0.15)
    call_t = sans("by name", 20, LOOKUP).next_to(call, UP, buff=0.1)
    slot_c = cli.get_center() + np.array([0.0, -0.2, 0])
    a = sec_t.get_right() + RIGHT * 0.12
    route = VMobject(stroke_color=LOOKUP, stroke_width=5)
    route.set_points_as_corners([a, [cli.get_left()[0] - 0.02, a[1], 0]])
    route_t = mono("../secrets", 20, LOOKUP).next_to(route, UP, buff=0.08)
    ghost = key_outline(0.28).move_to(slot_c)
    g = VGroup(fr, tg, secrets, rail, rail_t, plugs, cli, cli_t, db, db_t, call, call_t, route, route_t, ghost)
    g.frame, g.tag, g.secrets, g.rail, g.rail_label, g.plugs = fr, tg, secrets, rail, rail_t, plugs
    g.cli, g.cli_label, g.db, g.db_label, g.call, g.call_label = cli, cli_t, db, db_t, call, call_t
    g.route, g.route_label, g.ghost = route, route_t, ghost
    return g


def footer_cards() -> VGroup:
    """Beat 10: "Answers: exercises.md" and "Study guide + every command:" (the MLOps_Learning link
    and the guide's path), side by side. .answers .guide"""
    a_body = VGroup(label("Answers:", 24, INK), mono("exercises.md", 22, INK)).arrange(DOWN, aligned_edge=LEFT,
                                                                                       buff=0.14)
    g_body = VGroup(label("Study guide + every command:", 24, INK), mono(GUIDE_REPO, 20, INK),
                    mono(GUIDE_PATH, 20, INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    h = max(a_body.height, g_body.height) + 0.5
    a_box = box(a_body.width + 0.7, h, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
    g_box = box(g_body.width + 0.7, h, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
    a_body.move_to(a_box).align_to(a_box, LEFT).shift(RIGHT * 0.35)
    g_body.move_to(g_box).align_to(g_box, LEFT).shift(RIGHT * 0.35)
    ans, guide = VGroup(a_box, a_body), VGroup(g_box, g_body)
    row = VGroup(ans, guide).arrange(RIGHT, buff=0.3)
    row.answers, row.guide, row.url = ans, guide, VGroup(*g_body[1:])
    return row


class Recap(VoiceScene):
    def construct(self):
        # ============================================================ shared pieces, built once
        net = ToyNet(show=("outline", "laptop_label", "zone", "boxes", "rail", "rail_label", "plug_gateway",
                           "plug_processor", "door", "room_gateway", "room_processor", "map"))
        net.shift(UP * (STRIP4 + 0.08 - net.parts["outline"].get_bottom()[1]))
        assert net.parts["laptop_label"].get_top()[1] < TOP, net.parts["laptop_label"].get_top()[1]
        pr_frame = net.boxes["processor"].frame
        halo = pr_frame.copy().set_fill(opacity=0).set_stroke(CTR, 12, opacity=0.35)

        # ============================================================ 0 · up -d: in the background
        tr = tracker("P4", 3)
        t = term(P_TOY, rows=12, title="laptop")
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.1), FadeIn(t), run_time=0.6)
            bare_prompt(self, t)
            vo.wait_until("up dash d starts the app")
            type_cmd(self, t, UP_D, type_time=0.8)
            print_rows(self, t, C55.at((2, 5)), run_time=0.6)
            vo.wait_until("in the background")
            bp = bare_prompt(self, t)
            bg = beside(grey_tag("in the background"), t, bp, buff=0.4)
            pin(self, bp, bg)
            vo.wait_until("and returns your prompt")
            self.play(flash(bp.glyphs, TURN, 1.06), run_time=0.7)

        # ============================================================ 1 · handy: logs -f, exec sh
        pg1 = PortPage(8090, reply=R56, compact=True, ports=False)    # built filled, the reply hidden:
        _hidden(pg1.parts["reply"])                                   # PortPage.fill()'s first call drops glyphs
        pg1.shift([X_R - pg1.frame.get_right()[0], TOP - pg1.frame.get_top()[1], 0])   # placed by its frame
        assert pg1.frame.get_bottom()[1] > T6 + 0.15, pg1.frame.get_bottom()[1]
        c19 = src_panel(COMPOSE, 19, 21, size=20)
        place(c19, right=X_R, top=TOP - 0.05)
        assert c19.get_bottom()[1] > T6 + 0.15
        with self.voiceover(SAY[1]) as vo:
            unpin(self, bp, bg)
            tr = switch_section(self, tr, "PH", 2, run_time=0.6)
            resize(self, t, 6, run_time=0.6)
            vo.wait_until("Compose logs dash f")
            type_cmd(self, t, LOGS_F, type_time=0.9)
            t.print(self, [C56B.line(2)], run_time=0.35)
            self.play(FadeIn(pg1, shift=LEFT * 0.15), run_time=0.5)
            self.play(pg1.click(), run_time=0.5)
            post = t.print(self, [C56B.line(3)], run_time=0.35)[0]
            self.play(*pg1.parts_in("reply"), substring(post, "POST").animate.set_color(TURN), run_time=0.5)
            vo.wait_until("Control C stops only the following")
            cc = t.print(self, [C56B.line(4)], run_time=0.3)[0]
            ct = beside(grey_tag("stops following · the app keeps running"), t, cc, buff=0.4)
            pin(self, cc, ct)
            bare_prompt(self, t)
            vo.wait_until("Compose exec gateway sh")
            self.play(FadeOut(pg1), tr.goto(3), run_time=0.5)
            type_cmd(self, t, EXEC_SH, type_time=0.9)
            self.play(*enter_container(t, "gateway", prompt="#"), run_time=0.4)
            out = session(self, t, C56D, (2, 5), type_time=0.5, out_time=0.3)
            env = out[5]
            vo.wait_until("where the environment shows")
            bars = VGroup(*[c19.bar(n, LOOKUP, 0.2) for n in (19, 20, 21)])
            self.play(env.glyphs.animate.set_color(LOOKUP), FadeIn(c19, shift=DOWN * 0.1), run_time=0.5)
            a = env.glyphs.get_right() + RIGHT * 0.15
            x_r = 6.05
            b = np.array([x_r, c19.code.background.get_bottom()[1] - 0.03, 0])
            link = VMobject(stroke_color=LOOKUP, stroke_width=3)
            link.set_points_as_corners([a, [x_r, a[1], 0], b])
            tip = Polygon(b, b + np.array([-0.09, -0.16, 0]), b + np.array([0.09, -0.16, 0]),
                          stroke_width=0).set_fill(LOOKUP, 1)
            self.play(FadeIn(bars), Create(link), run_time=0.6)
            self.play(FadeIn(tip), run_time=0.2)
            vo.wait_until("processor and 9200")
            self.play(flash(c19.span(20, "processor"), LOOKUP, 1.15), flash(c19.span(21, '"9200"'), LOOKUP, 1.15),
                      flash(env.glyphs, LOOKUP, 1.08), run_time=0.8)
            self.play(FadeOut(VGroup(link, tip)), run_time=0.3)
            session(self, t, C56D, 6, type_time=0.3)
            self.play(*leave_container(t, P_TOY), run_time=0.4)
            bare_prompt(self, t)

        # ============================================================ 2 · Step 3: repeat the port experiments
        rc487 = readme_chip("README.md · line 487", "repeat the port experiments in docker-compose.yml", max_w=10.0)
        place(rc487, left=X_L, top=TOP - 0.02)
        ed = editor(E_BEFORE, "docker-compose.yml", 15, "docker-compose.yml · lines 15–16 · comment cut")
        place(ed, left=X_L, top=rc487.get_bottom()[1] - 0.12)
        assert ed.get_bottom()[1] > T6 + 0.06, ed.get_bottom()[1]
        ed_after = editor(E_AFTER, "docker-compose.yml", 15, "docker-compose.yml · lines 15–16 · comment cut")
        ed_after.move_to(ed)
        ed_orig = ed.panel.code.code_lines[1].copy()
        pen = pencil(0.5, TURN)
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(c19, bars)), run_time=0.4)
            tr = switch_section(self, tr, "P4", 3, run_time=0.6)
            self.play(FadeIn(rc487, shift=DOWN * 0.1), FadeIn(ed, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("Change 8090 to 8095")
            self.play(caption_extra(tr, True), run_time=0.3)
            line16 = ed.panel.code.code_lines[1]
            pen.move_to(line16.get_right() + RIGHT * 0.9 + UP * 0.3)
            self.play(FadeIn(pen), run_time=0.2)
            self.play(pen_to(pen, line16), run_time=0.4)
            self.play(Transform(line16, ed_after.panel.code.code_lines[1]), run_time=0.5)
            self.play(pen.animate.shift(RIGHT * 0.4 + UP * 0.3).set_opacity(0), run_time=0.3)
            self.remove(pen)
            type_extra(self, t, DIFF, type_time=0.4)
            d = t.print(self, [(C57.line(10), ERR), (C57.line(11), VENV)], run_time=0.45)
            b95 = glyph_box(d[1], "8095", TURN)
            pin(self, d[1], b95, anim=Create(b95), run_time=0.4)
            vo.wait_until("and run up dash d")
            self.play(FadeOut(VGroup(rc487, ed)), caption_extra(tr, False), run_time=0.4)
            resize(self, t, 4, run_time=0.6, extra=[FadeIn(net)])
            type_cmd(self, t, UP_D, type_time=0.7)
            r58 = print_rows(self, t, C58.at((2, 4)), run_time=0.5)
            self.play(*paint(r58[1], VENV), *paint(r58[2], TURN), run_time=0.5)
            vo.wait_until("Compose recreates only the gateway")
            self.play(FadeIn(halo), run_time=0.4)
            self.play(net.reform("gateway", run_time=1.2), net.set_door("127.0.0.1:8095", run_time=1.2),
                      flash(halo, CTR, 1.0, 1.2))

        # ============================================================ 3 · the page on 8095; change it back
        pg3 = PortPage(8095, reply=R59, compact=True, ports=False)
        pg3.shift([0 - pg3.frame.get_center()[0], (TOP - 0.25) - pg3.frame.get_top()[1], 0])
        assert pg3.frame.get_bottom()[1] > STRIP4 + 0.2
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(net), FadeOut(halo), FadeIn(pg3, shift=UP * 0.1), run_time=0.6)
            self.play(flash(pg3.address, TURN, 1.12), flash(pg3.reply_value.glyphs, TURN, 1.05), run_time=0.7)
            vo.wait_until("change it back")
            self.play(FadeOut(pg3), FadeIn(ed), run_time=0.5)
            line16 = ed.panel.code.code_lines[1]
            pen = pencil(0.5, TURN).move_to(line16.get_right() + RIGHT * 0.9 + UP * 0.3)
            self.play(FadeIn(pen), pen_to(pen, line16), run_time=0.4)
            self.play(Transform(line16, ed_orig), run_time=0.5)
            self.play(pen.animate.shift(RIGHT * 0.4 + UP * 0.3).set_opacity(0), run_time=0.3)
            self.remove(pen)
            vo.wait_until("and apply again")
            type_cmd(self, t, UP_D, type_time=0.5)
            r60 = print_rows(self, t, C60.at((2, 4)), run_time=0.4)
            self.play(*paint(r60[1], VENV), *paint(r60[2], TURN), FadeOut(ed), FadeIn(net), FadeIn(halo),
                      run_time=0.5)
            self.play(net.reform("gateway", run_time=1.0), net.set_door("127.0.0.1:8090", run_time=1.0),
                      flash(halo, CTR, 1.0, 1.0))

        # ============================================================ 4 · --build: only the processor
        edp = editor(P_AFTER, "processor/processor.py", 45, "processor/processor.py · line 45", "python")
        added = VGroup(*edp.panel.code.code_lines[2])                 # "# edited"
        cap_p = mixed([("edit: add", "serif"), ("# edited", "mono"),
                       ("at the end · remove it when you're done", "serif")])
        place(edp, cx=0, top=TOP - 0.1)
        hd_after = _header_text("processor/processor.py · lines 45–47").move_to(edp.panel.header, aligned_edge=LEFT)
        place(cap_p, cx=0, top=edp.get_bottom()[1] - 0.18)
        assert cap_p.get_bottom()[1] > STRIP4 + 0.15, cap_p.get_bottom()[1]
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(net), FadeOut(halo), tr.goto(4), run_time=0.5)
            for m in added:
                m.set_opacity(0)
            self.play(caption_extra(tr, True), FadeIn(edp, shift=DOWN * 0.1), FadeIn(cap_p), run_time=0.5)
            for m in added:
                m.set_opacity(1)
            self.remove(*added)
            pen = pencil(0.5, TURN).move_to(edp.panel.code.code_lines[0].get_right() + RIGHT * 0.6 + UP * 0.2)
            self.play(FadeIn(pen), run_time=0.2)
            self.play(pen_to(pen, VGroup(*added)), Transform(edp.panel.header, hd_after), run_time=0.4)
            self.add(*added)
            for m in added:
                m.set_opacity(0)
            self.play(*[m.animate.set_opacity(1) for m in added], pen_to(pen, VGroup(*added), run_time=0.6),
                      run_time=0.6)
            self.play(pen.animate.shift(RIGHT * 0.4 + UP * 0.3).set_opacity(0), run_time=0.3)
            self.remove(pen)
            type_extra(self, t, DIFF, type_time=0.4)
            dp = t.print(self, [(C61.line(10), VENV), (C61.line(11), VENV)], run_time=0.4)
            vo.wait_until("We added a comment")
            self.play(flash(dp[1].glyphs, VENV, 1.15), flash(added, VENV, 1.15), run_time=0.6)
            self.play(FadeOut(VGroup(edp, cap_p)), caption_extra(tr, False), run_time=0.4)
            resize(self, t, 13, run_time=0.6)
            type_cmd(self, t, UP_BUILD, type_time=0.9)
            cols = {21: VENV, 22: VENV, 23: VENV}
            items = [(s, cols.get(n, OUTPUT)) if s != "…" else s
                     for s, n in zip(B_ROWS, [3, 0, 21, 22, 23, 24, 0, 43, 44, 45, 46, 47])]
            br = print_rows(self, t, items, run_time=0.9, lag=0.08)
            assert len(t.lines) == 13, len(t.lines)
            r24, r46, r47 = br[5], br[10], br[11]
            assert "[processor 4/4] COPY" in r24.text and "Running" in r46.text and "Started" in r47.text
            vo.wait_until("only the copy layer is new")
            nc = beside(grey_tag("not CACHED"), t, r24, buff=0.5)
            self.play(*paint(r24, TURN), run_time=0.5)
            pin(self, r24, nc, run_time=0.35)
            vo.wait_until("and only the processor is recreated")
            self.play(*paint(r46, VENV), run_time=0.4)
            self.play(*paint(r47, TURN), run_time=0.5)

        # ============================================================ 5 · the mounted folder: no rebuild
        ill = illustration_tag("what if")
        place(ill, right=X_R, cy=BAND_Y)
        vol = src_panel(COMPOSE, 17, 18, cut_comments=True, size=20)
        place(vol, left=X_L, top=TOP - 0.05)
        och = excerpt_chip(OPEN20, "gateway/gateway.py · line 20 (excerpt)", line=L20)
        place(och, left=X_L, top=vol.get_bottom()[1] - 0.3)
        pic = mount_picture(0.35, X_R, TOP - 0.05)
        assert pic.get_bottom()[1] > STRIP_TOP + 0.08, pic.get_bottom()[1]
        assert vol.get_right()[0] < pic.get_left()[0] - 0.1, (vol.get_right()[0], pic.get_left()[0])
        no_rb = note("no rebuild")
        no_rb.move_to([pic.route.get_center()[0] + 0.25 + no_rb.width / 2, pic.gap_y, 0])
        with self.voiceover(SAY[5]) as vo:
            resize(self, t, 3, run_time=0.5)
            self.play(FadeIn(vol, shift=DOWN * 0.1), FadeIn(pic.lap), FadeIn(pic.ctr), FadeIn(ill), run_time=0.6)
            vbar = vol.bar(18, LOOKUP, 0.22)
            self.play(Create(pic.route), FadeIn(vbar), run_time=0.5)
            self.play(flash(pic.route, TURN, 1.0, 0.5), run_time=0.5)
            vo.wait_until("and it rereads its page on each load")
            self.play(FadeIn(och, shift=DOWN * 0.1), run_time=0.4)
            self.play(text_span(och.text, OPEN20, '"index.html"').animate.set_color(TURN), run_time=0.3)
            vo.wait_until("edits show on the next reload")
            pen = pencil(0.45, TURN).move_to(pic.lap_html.get_right() + RIGHT * 0.7 + UP * 0.3)
            self.play(FadeIn(pen), pen_to(pen, pic.lap_html.text), run_time=0.3)
            self.play(flash(pic.lap_html, TURN, 1.12, 0.6), flash(pic.ctr_html, TURN, 1.12, 0.6),
                      flash(pic.route, TURN, 1.0, 0.6), run_time=0.6)
            brw = pic.browser
            req = Arrow([brw.get_center()[0], pic.browser_label.get_bottom()[1] - 0.04, 0],
                        [brw.get_center()[0], pic.app.get_top()[1] + 0.02, 0], buff=0, color=LOOKUP, stroke_width=4,
                        max_tip_length_to_length_ratio=0.15)
            self.play(pen.animate.shift(RIGHT * 0.3 + UP * 0.3).set_opacity(0), brw.reload.animate.rotate(-PI),
                      run_time=0.35)
            self.remove(pen)
            self.play(Create(req), run_time=0.3)
            vo.wait_until("without a rebuild")
            self.play(brw.lines[0].animate.set_color(TURN), FadeIn(no_rb, shift=LEFT * 0.1), run_time=0.4)
            self.wait(1.6)

        # ============================================================ 6 · down; images remain; costs nothing
        rc515 = readme_chip("README.md · line 515", "The built images remain.")
        place(rc515, right=X_R, cy=BAND_Y)
        assert rc515.get_left()[0] > tr.get_right()[0] + 0.2, (rc515.get_left()[0], tr.get_right()[0])
        note_rm = mixed([("docker image rm <name>", "mono"), ("· if you want the space", "serif")])
        hw = mixed_chip([("hello-world's exited container:", "serif"), ("docker ps -a", "mono"),
                         (", then", "serif"), ("docker rm <its ID>", "mono")])
        hw_tag = extra_tag()
        hw_row = VGroup(hw, hw_tag).arrange(RIGHT, buff=0.25)
        free = fix_chip("port_toy costs nothing")
        place(note_rm, left=X_L, cy=TOP - 0.35)
        place(free, right=X_R, cy=TOP - 0.35)
        place(hw_row, left=X_L, cy=TOP - 0.95)
        assert hw_row.get_bottom()[1] > T10 + 0.1 and hw_row.get_right()[0] < X_R, hw_row.get_right()
        assert note_rm.get_right()[0] < free.get_left()[0] - 0.3
        card = turn_card([DOWN_CMD, PS_A, (IMG_LS, "extra")])
        place(card, cx=0, cy=(T10 + (-3.5)) / 2)
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(vol, vbar, och, pic, ill, no_rb, req)), tr.goto(5), run_time=0.6)
            resize(self, t, 10, run_time=0.6)
            type_cmd(self, t, DOWN_CMD, type_time=0.6)
            r64 = print_rows(self, t, C64.at((2, 5)), run_time=0.5)
            self.play(*paint(r64[1], TURN), *paint(r64[2], TURN), run_time=0.5)
            vo.wait_until("nothing is left in ps dash a")
            ps_ln = type_cmd(self, t, PS_A, type_time=0.6)
            t.print(self, [C65.line(2)], run_time=0.3)
            pin(self, ps_ln, beside(grey_tag("empty"), t, ps_ln, buff=0.4), run_time=0.4)
            vo.wait_until("The images remain")
            self.play(FadeIn(rc515, shift=DOWN * 0.1), caption_extra(tr, True), run_time=0.5)
            type_extra(self, t, IMG_LS, type_time=0.5)
            imgs = t.print(self, IMG_ROWS, run_time=0.6)
            ct = beside(grey_tag("2 of 5 columns"), t, imgs[0], buff=0.45)
            assert ct.get_left()[0] > imgs[0].glyphs.get_right()[0] + 0.2, ct.get_left()[0]
            pin(self, imgs[0], ct, run_time=0.3)
            hl = []
            for k, n in SHARED.items():
                hl += [substring(imgs[k], n).animate.set_color(TURN), substring(imgs[k], "198MB").animate.set_color(TURN)]
            self.play(*hl, run_time=0.6)
            vo.wait_until("sharing about 200 megabytes")
            rows = [imgs[k] for k in (2, 3, 4, 5, 6)]
            x = max(r.glyphs.get_right()[0] for r in rows) + 0.25
            top_y, bot_y = rows[0].strut.get_top()[1], rows[-1].strut.get_bottom()[1]
            br_ = VMobject(stroke_color=S.GREY, stroke_width=3)
            br_.set_points_as_corners([[x, top_y, 0], [x + 0.12, top_y, 0], [x + 0.12, bot_y, 0], [x, bot_y, 0]])
            br_l = label("shared layers · ≈ 200 MB in all", 20, S.GREY)
            br_l.next_to(br_, RIGHT, buff=0.18)
            assert br_l.get_right()[0] < t.box.get_right()[0] - 0.1, br_l.get_right()[0]
            self.play(Create(br_), FadeIn(br_l, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("remove them to free space")
            self.play(FadeIn(note_rm, shift=DOWN * 0.1), run_time=0.4)
            self.play(FadeIn(hw_row, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("Port toy costs nothing")
            self.play(FadeIn(free, shift=LEFT * 0.1), run_time=0.4)
            self.play(flash(free, VENV, 1.08), run_time=0.6)
            vo.wait_until("Pause and shut it down")
            self.play(FadeOut(VGroup(t, br_, br_l)), caption_extra(tr, False), run_time=0.4)
            self.play(FadeIn(card, shift=UP * 0.15), run_time=0.5)

        # ============================================================ 7 · Test yourself: Q1
        title = label("Test yourself", 40, INK)
        place(title, cx=0, cy=2.75)
        t_ul = Line(title.get_corner(DOWN + LEFT) + DOWN * 0.12, title.get_corner(DOWN + RIGHT) + DOWN * 0.12,
                    color=TURN, stroke_width=4)
        Q_CY = 0.15

        def q_with_icon(i: int, content: VGroup):
            q = question(i)
            th = thumb(content)
            g = VGroup(th, q)
            th.move_to([0, 0, 0])
            q.shift(np.array([th.get_right()[0] + 0.55 + 0.48, 0, 0]) - np.array([0, 0, 0]))
            q.shift(UP * (th.get_center()[1] - q.text.get_center()[1]))
            g.shift(RIGHT * (0 - g.get_center()[0]) + UP * (Q_CY - g.get_center()[1]))
            assert g.get_left()[0] > X_L and g.get_right()[0] < X_R, (i, g.get_left()[0], g.get_right()[0])
            g.q, g.th = q, th
            return g

        def q_in(g):
            """The icon card slides in, the badge pops, the words write in (glyphs only: Write would
            draw the rows' invisible struts as outlines)."""
            words = VGroup(*[r.glyphs for r in g.q.lines])
            return AnimationGroup(FadeIn(g.th, shift=RIGHT * 0.2), FadeIn(g.q.badge, scale=0.8), Write(words))

        def q_show(g, run_time: float = 1.1):
            self.play(q_in(g), run_time=run_time)
            self.add(g)

        def q_swap(old, new, run_time: float = 1.4):
            """The old question slides up and fades; the next writes in once it has mostly left."""
            self.play(LaggedStart(FadeOut(old, shift=UP * 1.0), q_in(new), lag_ratio=0.4), run_time=run_time)
            self.add(new)

        i1 = icon_build_pull()
        g1 = q_with_icon(1, i1)
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
            self.play(FadeIn(title, shift=DOWN * 0.15), Create(t_ul), run_time=0.7)
            vo.wait_until("One")
            q_show(g1)
            vo.wait_until("which files define")
            self.play(flash(i1.box, CTR, 1.15, 0.8))
            vo.wait_until("and what does run use")
            self.play(q_span(g1.q, "run").animate.set_color(TURN), flash(i1.pointer, LOOKUP, 1.2, 0.8), run_time=0.8)

        # ============================================================ 8 · Q2, Q3
        i2 = icon_gates()
        g2 = q_with_icon(2, i2)
        i3 = icon_copy_key()
        g3 = q_with_icon(3, i3)
        with self.voiceover(SAY[8]) as vo:
            q_swap(g1, g2)
            vo.wait_until("which three gates")
            self.play(LaggedStart(*[flash(gg, TURN, 1.2, 0.6) for gg in i2.gates], lag_ratio=0.5), run_time=1.4)
            vo.wait_until("and where does each one fail")
            self.play(LaggedStart(*[flash(gg, ERR, 1.2, 0.6) for gg in i2.gates], lag_ratio=0.5), run_time=1.4)
            vo.wait_until("Three")
            q_swap(g2, g3)
            vo.wait_until("how does a git-ignored key end up")
            self.play(i3.key.animate.move_to(i3.slab.get_center() + LEFT * 0.4), run_time=1.0)
            self.play(i3.key.animate.set_color(ERR), run_time=0.4)
            vo.wait_until("and what's the fix")
            self.play(flash(i3.folder, TURN, 1.2, 0.7), flash(i3.key, TURN, 1.3, 0.7))

        # ============================================================ 9 · Q4, Q5
        i4 = icon_door_room()
        g4 = q_with_icon(4, i4)
        i5 = icon_loops_book()
        g5 = q_with_icon(5, i5)
        with self.voiceover(SAY[9]) as vo:
            q_swap(g3, g4)
            self.play(flash(q_span(g4.q, "127.0.0.1"), TURN, 1.12), run_time=0.7)
            vo.wait_until("8095")
            self.play(flash(q_span(g4.q, "8095"), TURN, 1.2), run_time=0.7)
            vo.wait_until("9100")
            self.play(flash(q_span(g4.q, "9100"), TURN, 1.2), run_time=0.7)
            vo.wait_until("Which number does the browser use")
            self.play(flash(q_span(g4.q, "-p127.0.0.1:8095:9100"), TURN, 1.06), flash(i4.street, TURN, 1.25),
                      run_time=0.8)
            vo.wait_until("which does the gateway bind")
            self.play(flash(q_span(g4.q, "gateway.py"), TURN, 1.12), flash(i4.room, TURN, 1.25), run_time=0.8)
            vo.wait_until("and what does 127.0.0.1 restrict")
            self.play(flash(q_span(g4.q, "127.0.0.1", occurrence=1), TURN, 1.12), run_time=0.8)
            vo.wait_until("Five")
            q_swap(g4, g5)
            vo.wait_until("what is localhost")
            self.play(q_span(g5.q, "localhost").animate.set_color(TURN), i5.loops.animate.set_color(TURN), run_time=0.6)
            vo.wait_until("and which name reaches the processor")
            self.play(flash(i5.book, LOOKUP, 1.4, 0.8))

        # ============================================================ 10 · next: L05; answers; the end
        tz = teaser()
        place(tz, cx=0, top=2.75)
        tz.tag.move_to(tz.frame.get_corner(UL) + np.array([tz.tag.width / 2 + 0.3, 0, 0]))
        fc = footer_cards()
        place(fc, cx=0, bottom=-3.45)
        assert fc.get_left()[0] > X_L - 0.05 and fc.get_right()[0] < X_R + 0.05, (fc.get_left(), fc.get_right())
        assert tz.get_bottom()[1] > fc.get_top()[1] + 0.2, (tz.get_bottom()[1], fc.get_top()[1])
        with self.voiceover(SAY[10]) as vo:
            self.play(LaggedStart(AnimationGroup(FadeOut(g5, shift=UP * 1.0), FadeOut(VGroup(title, t_ul))),
                                  AnimationGroup(Create(tz.frame), FadeIn(tz.tag)), lag_ratio=0.5), run_time=1.1)
            vo.wait_until("a command-line container")
            self.play(FadeIn(VGroup(tz.cli, tz.cli_label)), FadeIn(VGroup(tz.db, tz.db_label)),
                      Create(tz.rail), FadeIn(tz.rail_label), FadeIn(tz.plugs), run_time=0.8)
            vo.wait_until("by name on a Compose network")
            self.play(Create(tz.call), FadeIn(tz.call_label), run_time=0.7)
            self.play(flash(tz.rail, CTR, 1.0, 0.6), run_time=0.6)
            vo.wait_until("with the same secrets mount")
            self.play(FadeIn(tz.secrets), run_time=0.4)
            self.play(Create(tz.route), FadeIn(tz.route_label), run_time=0.6)
            self.play(flash(tz.route, TURN, 1.0, 0.8), FadeIn(tz.ghost), run_time=0.8)
            vo.wait_until("parts 1 and 2 together")
            self.play(flash(tz.frame, INK, 1.02, 0.8))
            vo.wait_until("Answers are in the exercises")
            self.play(FadeIn(fc.answers, shift=UP * 0.15), FadeIn(fc.guide, shift=UP * 0.15), run_time=0.6)
            self.play(flash(fc.answers, TURN, 1.06, 0.7))
        self.wait(0.8)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.9)
        self.wait(0.3)
