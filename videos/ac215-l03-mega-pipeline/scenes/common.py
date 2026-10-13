"""Shared look for AC215 L3 (Containers II: five containers, one bucket): paths, narration, the
semantic colours of BRIEF.md, loaders for the real captures in assets/, terminal and tracker
helpers, and the video's recurring pictures (V1-V8 of BRIEF.md).

Notes for scene authors
=======================

Import what you need:  from common import (NARRATION, TEAL..., capture, term, Relay, ...)
Every scene: SAY = NARRATION["Snn"]; assert len(SAY) == n. Text >= 20 pt everywhere (all helpers
below draw at 20-22 pt; never .scale() a group with text below 1.0, use Piece.rescale(k)).

Data and sources
    NARRATION["S01"]...      SAY lines from script.md (one voiceover block each)
    TITLES[cls]              scene titles from video.yaml
    capture(name, folder="laptop") -> Capture   assets/terminal/<folder>/<name>.txt
        folders: "laptop" (everything typed on the laptop), "transcribe_audio", "generate_text",
        "synthesis_audio_en", "translate_text", "synthesis_audio" (typed inside that container),
        "expected" (README --help blocks for C, D, E; line 1 is a '#' header). "files/" holds the
        student's Dockerfiles: read them with asset_lines()/file_panel(), not capture().
        .cmd (the `$` line, without "$ "), .lines (output), .exit, .first (file line of .lines[0])
        .at(9, 23, "…", (148, 149))   output lines BY FILE LINE NUMBER (the script's TERM notation;
                                      an int, an (a, b) inclusive range, or a literal "…")
        .line(n)                      one file line;  .typed(n): the command on a prompt line
        .pick((1, 3), (-2, -1))       L1-compatible: body index = file line - 1 (avoid; use .at)
    source_text(path)  excerpt(path, a, b, cut_comments=False)   assets/source (tutorial files)
        cut_comments: a line > 70 chars loses its trailing comment, shown as "# …" (script rule)
    asset_lines(rel, a, b)   raw lines a..b of any file under assets/terminal (e.g. a Dockerfile)
    live_split(row) -> (text, time)   a BuildKit live-view row without its time field (cut at 65)
    history_row(line)        a `docker history` row sliced to CREATED BY + SIZE (line[32:90])

Colours (BRIEF.md, binding)
    LAPTOP GREY · CLOUD BLUE · CTR (=IMAGE) TEAL · SYSTEM ORANGE · VENV GREEN · TOOL (=UV) PURPLE
    ERR RED · TURN YELLOW · COST (=KEY) GOLD · LOOKUP PINK · INK white
Running example
    P_HOME "student@laptop:~$"  P_REPO ".../mega-pipeline$"  p_comp(c) / P_A (component folders)
    P_CTR "app@5b4d4981ec25:/app$"  GROUP "group-01"  COMPONENTS (A-E folder names)  LETTERS "ABCDE"
    PREFIXES (6 drawers, pipeline order)  README_PREFIXES (README.md:74-80 order)  BONUS_PREFIX

Layout constants: BOTTOM = -3.5 (terminal bottom edge), TRACK_LEFT/TRACK_TOP (tracker corner),
STRIP_TOP = top edge of the 3-row strip (strip_top(rows) for other sizes); full-width items are
<= 12.6 wide; keep everything inside x in [-6.6, 6.6], y in [-3.6, 3.6].

Tracker and terminal helpers
    tracker(key, step=None)            placed ReadmeTracker; keys R A B C D E H X (SECTIONS)
    switch_section(scene, tr, key, step=1)  fade the old tracker into a new section, returns it
    caption_extra(tr, on=True)         Transform: caption gets/loses " · extra"
    term(prompt=P_A, rows=12, component=None)   house terminal (12.6 wide, 22 pt, 65 chars a row),
                                       placed with its bottom at BOTTOM; title "laptop", or with a
                                       component: title "container · <c>" and a TEAL frame
    enter_container(t, component) / leave_container(t, prompt)   -> list of animations
    resize(scene, t, rows, keep=None)  grow/shrink with the bottom fixed (keeps the last lines)
    bare_prompt(scene, t)  type_cmd(scene, t, cmd)   a prompt with no command / type after it
    pin(scene, line, mob) / unpin(scene, line, mob)  a tag that scrolls with a terminal line
    under(mob, color)  strike(mob, color)            underline / strike-through Line
    time_tag(time) + place_time(tag, t, line)        the GREY live-view time tag at a row's end

Panels and cards
    src_panel(path, a, b, cut_comments=False, focus=None, size=22, width=None, shown_path=None,
              suffix=None)      code_panel from assets/source with "path · lines a–b" (+" · comment
                                cut" when a comment was cut); language from the extension
    file_panel(rel, a, b, path, ...)   the same for assets/terminal/<rel> (the student's Dockerfile:
                                file_panel("files/transcribe_audio.Dockerfile", 1, 3,
                                "transcribe_audio/Dockerfile"))
    log_panel(lines, header, width=12.6, size=20)  plain mono rows on a dark panel (full logs,
                                docker history); .rows[i] are mono_lines (use substring())
    readme_chip(where, phrase)  one-line README chip (header GREY mono + the phrase), ~0.45 tall
    readme_card(where, lines, width=None)  multi-line GREY README card
    editor_inset(panel, title="VS Code · on your laptop")  a GREY editor window around a panel
    cmd_chip(cmd, note=None)    a command shown, not typed (mono 20 chip + GREY note)
    LookFor(items, fail=None)   the "with your key, look for" card; items are (text, "line 30");
                                .reveal(scene, i) writes item i in, .reveal_fail(scene)
Tags (all 22 pt): your_turn() extra_tag() illustration_tag(note=None) expected_tag()
    recorded_tag(s) nokey_tag() erratum_tag() cost_tag() standin_tag() preview_tag() optional_tag()
    build_badge(k, words=True) (TEAL "build step k")  stamp(text, color)  cached_stamp()

Glyphs (no text unless named): key_glyph(h, name=None) GOLD · wave_token() page_token(long, fr)
    token(kind) · signpost(lines) PINK · clock_glyph() · token_tag() GOLD · padlock() · stub_glyph()
    · parcel_glyph() · builder_box() · sieve(name) · book_glyph() · ship_box() · hub_shelf()
    · pkg_dots(n, cols) (tiny GREEN package chips) · file_row(name, color) · ghost_file(name)

Set pieces (all are Piece = VGroup + .attach/.detach/.reveal/.rescale)
    Piece.attach(scene, *mobs, anims=None)  play (FadeIn by default), then make mobs part of the
          piece (so moving the piece moves them; never leaves strays). .detach(scene, *mobs)
          the reverse (FadeOut by default). .reveal(scene, *part_names) / .hide(...) for named
          parts built but not shown. .rescale(k): scale shapes by k, keep every text at its size
          (use self.play(piece.animate.rescale(0.8).to_edge(UP))).
    V1 Relay(width=12.4, labels=True, edges=False)   five TEAL boxes over six BLUE drawers
          (+ dashed bonus drawer). ~12.4 x 4.5. .boxes[j] .drawers[i] .bonus .box_labels[j]
          .drawer_labels[i] .read_edges[j] .write_edges[j]; parts "drawer_labels", "box_labels",
          "edges", "bonus_tag". relay.token_at(i, kind) -> a token resting in drawer i;
          relay.run(scene, [(token, j), ...]) -> new tokens: each token goes from its drawer up
          into box j, becomes OUT_KIND[j], and drops into WRITES[j] (parallel routes allowed).
          READS = [0, 1, 2, 2, 4], WRITES = [1, 2, 3, 4, 5].
       SubDrawers(groups) a drawer opened into group sub-drawers; .slots[i], .flash(i, color)
       Leaderboard(groups, stages)  schematic grid (tag it illustration); .light(r, c)
    V2 LayerStack(slab_w=3.4)   slabs bottom-up: drop(scene, name) with name in SLABS
          ("base", "apt", "workdir", "copy", "sync"; STEP_OF gives the build step 1-5);
          .slabs[name] (.box .label) .grow(name, h) -> anims .badge(name) .stamp(name)
          .size_label(name, "842MB") .top_label(text) .brace(text) .chips(name, n) .files(name)
       ConfigCard(width=8.6, rows=4, cols=2)   lecture 2's TEAL config card (no layers);
          .write(scene, text, color, key) .restyle(key, text, color) -> Transform
    V3+V4 Window(files, copied=None, rows=None, key=False)   laptop folder <- PINK -v route ->
          image block (/app cavity + GREEN /home/app/.venv) + dashed writable sheet with a GREEN
          shelf. ~12.4 x 3.3 with 4 files. .mount(scene) .cover_to(alpha) .blink(name)
          .add_file(scene, name) .fill_shelf(scene, n=26) .tmp_page(scene) .evaporate(scene)
          .new_sheet(scene) .venv_to_cavity() / .venv_home()
    V5 AdcChain(show=...)   laptop secrets/ + key <- window <- container (signpost at /app,
          storage.Client(), google.auth) -> Google Cloud (2 gates, bucket door). ~12.8 x 4.2.
          .ask(scene) .follow(scene) .mint(scene) .request(scene, token) .check(scene, i)
          .fail(scene)
    V6 TwoFilters()   folder with the key; Git history book; image box + Docker Hub shelf.
          .lower(scene, "git"|"image") .pour(scene, "git"|"image") .to_hub(scene)
    V7 VersionLine(10, 16, lo=11)   L1's number line; .dot(minor, text, color) .move_lo(lo) -> anims
          .download_arrow(minor, text)
    V8 ApiCall(api, ctr, drawers=None)   container <-> BLUE API cloud (+ drawers below).
          .send(scene, payload) .stub(scene) .ring(scene, stub, "up to 90 s") .reply(scene, mob)
          .deliver(scene, mob, i)

Capture folder names (assets/terminal): laptop, transcribe_audio, generate_text, synthesis_audio_en,
translate_text, synthesis_audio, expected, files.
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import yaml
from manim import (DOWN, LEFT, ORIGIN, PI, RIGHT, TAU, UP, AnimationGroup, Arc, Arrow, Brace,
                   Circle, Create, DashedLine, DashedVMobject, Dot, FadeIn, FadeOut, GrowArrow,
                   Indicate, LaggedStart, Line, MoveAlongPath, Polygon, Rectangle,
                   RoundedRectangle, Text, Transform, VGroup, VMobject, Write, linear, smooth)

from explainer import style as S
from explainer.devops import (CAPTION, LABEL, MONO, OUTPUT, PANEL, SANS, SMALL, TAG, TERM_BG,
                              Terminal, box, chip, cloud, code_block, code_panel, file_glyph,
                              folder_glyph, label, line_pitch, mono, mono_line, step_badge, tag)
from explainer.script import load_narration

# ------------------------------------------------------------------ paths and data
HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
ASSETS = PROJECT / "assets"
TERMINAL = ASSETS / "terminal"
SOURCE = ASSETS / "source"
FILES = TERMINAL / "files"

SPEC = yaml.safe_load((PROJECT / "video.yaml").read_text())
TITLES = {s["cls"]: s["title"] for s in SPEC["scenes"]}
_script = PROJECT / "script.md"
NARRATION = load_narration(_script) if _script.exists() else {}

# ------------------------------------------------------------------ semantic colours (BRIEF.md)
LAPTOP = S.GREY          # your laptop, the clone, the files the mount shows inside
CLOUD = S.BLUE           # Google Cloud: bucket, drawers, APIs, IAM
CTR = S.TEAL             # containers and images: boxes A-E, layer stack, writable sheet
IMAGE = CTR
SYSTEM = S.ORANGE        # the base image's system parts: Debian, apt packages, Python 3.12
VENV = S.GREEN           # project-owned: pyproject.toml, uv.lock, the venv, requires-python
TOOL = S.PURPLE          # tools you install: uv, Docker
UV = TOOL
ERR = S.RED              # errors, the key inside an image, the default group drawer
TURN = S.YELLOW          # your turn, the tracker, look here now
COST = S.GOLD            # billed to the course project; the key glyph
KEY = COST
LOOKUP = S.PINK          # routes and paths: the -v mount, the credentials signpost, object names
INK = S.WHITE
DIMMED = S.GREY

# ------------------------------------------------------------------ the running example
USER, HOST, CID = "student", "laptop", "5b4d4981ec25"
GROUP = "group-01"
COMPONENTS = ["transcribe_audio", "generate_text", "synthesis_audio_en", "translate_text",
              "synthesis_audio"]
LETTERS = "ABCDE"
P_HOME = f"{USER}@{HOST}:~$"
P_REPO = f"{USER}@{HOST}:~/mega-pipeline$"


def p_comp(component: str) -> str:
    """The laptop prompt inside a component folder, e.g. p_comp("generate_text")."""
    return f"{USER}@{HOST}:~/mega-pipeline/{component}$"


P_A = p_comp("transcribe_audio")
P_CTR = f"app@{CID}:/app$"

# the bucket's prefixes: pipeline order (V1 drawers, left to right) and the README's order
PREFIXES = ["input_audios/", "text_prompts/", "text_paragraphs/", "text_audios/",
            "text_translated/", "output_audios/"]
README_PREFIXES = ["input_audios/", "text_prompts/", "text_paragraphs/", "text_translated/",
                   "text_audios/", "output_audios/", "output_audios_pp/"]
BONUS_PREFIX = "output_audios_pp/"
DRAWER_KIND = ["wave", "page", "long", "wave", "fr", "wave"]     # what each drawer holds
READS = [0, 1, 2, 2, 4]          # box j reads drawer READS[j]
WRITES = [1, 2, 3, 4, 5]         # and writes drawer WRITES[j]
OUT_KIND = [DRAWER_KIND[w] for w in WRITES]

# ------------------------------------------------------------------ layout
BOTTOM = -3.5                    # terminal bottom edge (fixed when it grows or shrinks)
TRACK_LEFT, TRACK_TOP = -6.5, 3.5
TERM_W, TERM_PT = 12.6, 22

# ------------------------------------------------------------------ README tracker
_STEPS_13 = ["cd folder", "Key in secrets", "uv init", "Write Dockerfile", "Build image",
             "Run container", "uv add", "Group name", "Check --help", "Download", "Transcribe",
             "Upload", "Exit, rebuild"]


def _steps(step11: str, upload: bool = True) -> list[str]:
    s = _STEPS_13[:10] + [step11] + (["Upload"] if upload else []) + ["Exit, rebuild"]
    return s


SECTIONS = {
    "R": ("Clone this Repository", ["Clone", "cd"]),
    "A": ("transcribe_audio", _steps("Transcribe")),
    "B": ("generate_text", _steps("Generate")),
    "C": ("synthesis_audio_en", _steps("Synthesize", upload=False)),
    "D": ("translate_text", _steps("Translate")),
    "E": ("synthesis_audio", _steps("Synthesize", upload=False)),
    "H": ("Push to Docker Hub", ["Login", "Tag", "Push"]),
    "X": ("ElevenLabs bonus", ["Key file", "uv add requests", "Run cli_11"]),
}
assert len(SECTIONS["A"][1]) == 13 and len(SECTIONS["C"][1]) == 12


def place_tracker(tr):
    tr.shift(np.array([TRACK_LEFT - tr.get_left()[0], TRACK_TOP - tr.get_top()[1], 0]))
    return tr


def tracker(key: str, step: int | None = None):
    """The README tracker for section `key` (R A B C D E H X, see SECTIONS), top-left, at `step`."""
    from explainer.devops import ReadmeTracker
    section, steps = SECTIONS[key]
    t = ReadmeTracker(section, steps)
    if step:
        t.set_step(step)
    t.key = key
    return place_tracker(t)


def caption_extra(tr, on: bool = True):
    """Transform: the tracker caption with (or without) ' · extra' while a command the README
    doesn't have is on screen."""
    k = tr.k
    s = f"step {k} of {len(tr.steps)}: {tr.steps[k - 1]}"
    new = label(s + " · extra", tr.size, tr.hi_color, t2c={"· extra": S.GREY}) if on else \
        label(s, tr.size, tr.hi_color)
    new.next_to(tr.dots, RIGHT, buff=0.25)
    return Transform(tr.caption, new)


def switch_section(scene, old, key: str, step: int | None = 1, run_time: float = 0.8):
    """The tracker switches to another README section: the old one lifts away, the new one
    drops in. Returns the new tracker (on screen)."""
    new = tracker(key, step)
    scene.play(FadeOut(old, shift=UP * 0.25), FadeIn(new, shift=DOWN * 0.25), run_time=run_time)
    return new


# ------------------------------------------------------------------ captures and sources
class Capture:
    """One captured command. .cmd (as typed, without "$ "), .lines (its output), .exit (status),
    .first (the file line number of .lines[0]: 2, or 3 for expected/*.txt), .header ('#' line)."""

    def __init__(self, name: str, cmd: str, lines: list[str], exit_code: int, first: int = 2,
                 header: str = ""):
        self.name, self.cmd, self.lines, self.exit = name, cmd, lines, exit_code
        self.first, self.header = first, header

    def line(self, n: int) -> str:
        """File line n (1-based, as in the script's TERM(file: n))."""
        i = n - self.first
        if not 0 <= i < len(self.lines):
            raise IndexError(f"{self.name}: line {n} is not output (output is lines "
                             f"{self.first}–{self.first + len(self.lines) - 1})")
        return self.lines[i]

    def at(self, *spec, ellipsis: str = "…") -> list[str]:
        """Output lines by FILE line number: at(9, 23, "…", (148, 149)) -> lines 9, 23, a '…'
        line, 148 and 149. A string is inserted as is ("…" or "" for the ellipsis)."""
        out: list[str] = []
        for s in spec:
            if isinstance(s, str):
                out.append(s or ellipsis)
            elif isinstance(s, int):
                out.append(self.line(s))
            else:
                a, b = s
                out += [self.line(n) for n in range(a, b + 1)]
        return out

    def typed(self, n: int) -> str:
        """The command typed on prompt line n (e.g. 'app@…:/app$ which python' -> 'which python')."""
        s = self.line(n)
        if "$ " not in s:
            raise ValueError(f"{self.name}: line {n} is not a prompt line: {s!r}")
        return s.split("$ ", 1)[1]

    def pick(self, *ranges, ellipsis: str = "…") -> list[str]:
        """L1-compatible: body lines by 1-based inclusive ranges (body index = file line - 1 for
        a normal capture). Prefer .at(), which takes file line numbers."""
        n = len(self.lines)
        out: list[str] = []
        last = None
        for r in ranges:
            a, b = (r, r) if isinstance(r, int) else r
            a = a if a > 0 else n + a + 1
            b = b if b > 0 else n + b + 1
            if last is not None and a > last + 1:
                out.append(ellipsis)
            out += self.lines[a - 1:b]
            last = b
        return out


def capture(name: str, folder: str = "laptop") -> Capture:
    """assets/terminal/<folder>/<name>.txt (name with or without .txt), parsed. Fails loudly if
    missing: never show an output that wasn't captured."""
    p = TERMINAL / folder / (name if name.endswith(".txt") else f"{name}.txt")
    if not p.exists():
        raise FileNotFoundError(f"capture {p.relative_to(PROJECT)} is missing (see ASSETS.md)")
    raw = [ln.rstrip("\r") for ln in p.read_text(encoding="utf-8").rstrip("\n").split("\n")]
    header = ""
    if raw and raw[0].startswith("# "):           # expected/*.txt: a provenance header first
        header, raw = raw[0], raw[1:]
    first = 3 if header else 2
    cmd = raw[0][2:] if raw[0].startswith("$ ") else ""
    body = raw[1:]
    code = 0
    if body and re.fullmatch(r"\[exit -?\d+\]", body[-1]):
        code = int(body[-1][6:-1])
        body = body[:-1]
    return Capture(f"{folder}/{p.name}", cmd, body, code, first, header)


def asset_lines(rel: str, first: int, last: int) -> str:
    """Lines first..last (1-based, inclusive) of any file under assets/terminal, e.g.
    asset_lines("files/transcribe_audio.Dockerfile", 5, 10)."""
    lines = (TERMINAL / rel).read_text(encoding="utf-8").split("\n")
    if last > len(lines):
        raise IndexError(f"{rel} has {len(lines)} lines")
    return "\n".join(lines[first - 1:last])


def source_text(name: str) -> str:
    return (SOURCE / name).read_text(encoding="utf-8")


def _comment_at(line: str) -> int:
    """Index of the '#' that starts a comment (outside quotes), or -1."""
    quote = None
    for i, ch in enumerate(line):
        if quote:
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
        elif ch == "#":
            return i
    return -1


def cut_comment(line: str, limit: int = 70) -> str:
    """A line longer than `limit` loses its trailing comment, shown as '# …' (script rule)."""
    if len(line) <= limit:
        return line
    i = _comment_at(line)
    return line if i < 0 else line[:i].rstrip() + ("  # …" if line[:i].strip() else
                                                     line[:i] + "# …")[0:0] + (
        "  # …" if line[:i].strip() else "# …") if False else (
        line[:i].rstrip() + "  # …" if line[:i].strip() else line[:i] + "# …")


def excerpt(name: str, first: int, last: int, cut_comments: bool = False) -> str:
    """Lines first..last (1-based, inclusive) of a tutorial file in assets/source, for
    code_panel(..., first_line=first). cut_comments: see cut_comment()."""
    lines = source_text(name).split("\n")
    if last > len(lines):
        raise IndexError(f"{name} has {len(lines)} lines")
    out = lines[first - 1:last]
    if cut_comments:
        out = [cut_comment(s) for s in out]
    return "\n".join(out)


def live_split(row: str, width: int = 65) -> tuple[str, str]:
    """A BuildKit live-view row (79 chars) -> (the row without its last field, cut to `width`
    with '…', and the last field, e.g. '2.9s'). The time goes into time_tag()."""
    r = row.rstrip()
    i = r.rfind(" ")
    text, time = r[:i].rstrip(), r[i + 1:]
    if len(text) > width:
        text = text[:width - 1] + "…"
    return text, time


def history_row(line: str) -> str:
    """A `docker history` row (laptop/17-history.txt) sliced to CREATED BY + SIZE: line[32:90]."""
    return line[32:90].rstrip()


# ------------------------------------------------------------------ small text helpers
def sans(s: str, size: float = CAPTION, color: str = INK, **kw) -> Text:
    """CMU Sans Serif text (drawer and box labels, card lines)."""
    return label(s, size, color, font=SANS, **kw)


def _split_us(name: str) -> list[str]:
    """'synthesis_audio_en' -> ['synthesis_', 'audio_en'] (split after the first underscore)."""
    i = name.find("_")
    return [name] if i < 0 else [name[:i + 1], name[i + 1:]]


def two_lines(name: str, size: float = CAPTION, color: str = INK) -> VGroup:
    """A name on two lines split after its first underscore, centred (20 pt sans)."""
    return VGroup(*[sans(p, size, color) for p in _split_us(name)]).arrange(DOWN, buff=0.07)


def _keep(m):
    """Mark a group (chip, tag, labelled glyph) to keep its size in Piece.rescale()."""
    m.keep_size = True
    return m


def under(mob, color: str = TURN, stroke: float = 4, buff: float = 0.05) -> Line:
    """A Line under `mob` (a terminal line, a substring of one, a code span)."""
    return Line(mob.get_corner(DOWN + LEFT) + DOWN * buff, mob.get_corner(DOWN + RIGHT) + DOWN * buff,
                color=color, stroke_width=stroke)


def strike(mob, color: str = S.GREY, stroke: float = 4) -> Line:
    """A Line through the middle of `mob` (a struck-through name or chip)."""
    return Line(mob.get_left() + LEFT * 0.06, mob.get_right() + RIGHT * 0.06, color=color,
                stroke_width=stroke)


# ------------------------------------------------------------------ terminal helpers
def term(prompt: str = P_A, rows: int = 12, component: str | None = None,
         title: str | None = None, width: float = TERM_W, size: float = TERM_PT) -> Terminal:
    """The house terminal (full width, 22 pt, 65 characters a row), bottom edge at BOTTOM.
    component=None: the laptop (title "laptop"); component="transcribe_audio": inside that
    container (title "container · transcribe_audio", TEAL frame; prompt defaults to P_CTR)."""
    if component and prompt == P_A:
        prompt = P_CTR
    ttl = title or (f"container · {component}" if component else "laptop")
    t = Terminal(prompt=prompt, width=width, rows=rows, size=size, title=ttl)
    if component:
        t.box.set_stroke(CTR, 3)
        t.title.set_color(CTR)
    t.shift(np.array([-t.box.get_center()[0], BOTTOM - t.box.get_bottom()[1], 0]))
    return t


def strip_top(rows: int = 3) -> float:
    """y of the top edge of a `rows`-row house terminal sitting on BOTTOM."""
    return BOTTOM + Terminal(rows=rows, width=TERM_W, size=TERM_PT, title="x").box.height


STRIP_TOP = strip_top(3)


def enter_container(t: Terminal, component: str = "transcribe_audio", prompt: str = P_CTR) -> list:
    """Animations: the terminal's frame turns TEAL, its title becomes "container · <c>"; the
    prompt becomes `prompt` for the next typed line."""
    t.set_prompt(prompt)
    new = mono(f"container · {component}", CAPTION, CTR).move_to(t.title)
    return [t.box.animate.set_stroke(CTR, 3), Transform(t.title, new)]


def leave_container(t: Terminal, prompt: str = P_A) -> list:
    """Animations: back on the laptop (GREY frame, title "laptop", prompt `prompt`)."""
    t.set_prompt(prompt)
    new = mono("laptop", CAPTION, S.GREY).move_to(t.title)
    return [t.box.animate.set_stroke(S.GREY_DARK, 2), Transform(t.title, new)]


def resize(scene, t: Terminal, rows: int, keep=None, run_time: float = 0.8, extra=()) -> Terminal:
    """Grow or shrink the terminal to `rows` (bottom edge fixed). It keeps its last lines (at
    most `keep` of them), or, when `keep` is a list of line mobjects, exactly those lines.
    The frame keeps its colour (TEAL inside a container)."""
    ref = Terminal(prompt=t.prompt, width=t.box.width, rows=rows, size=t.size, title="x")
    ref.shift(np.array([t.box.get_center()[0] - ref.box.get_center()[0],
                        t.box.get_bottom()[1] - ref.box.get_bottom()[1], 0]))
    ref.box.set_stroke(t.box.get_stroke_color(), t.box.get_stroke_width())
    if isinstance(keep, (list, tuple)):
        assert len(keep) <= rows
        kept = [ln for ln in t.lines.submobjects if ln in keep]
    else:
        n_keep = min(len(t.lines), rows, len(t.lines) if keep is None else keep)
        kept = t.lines.submobjects[len(t.lines) - n_keep:]
    gone = [ln for ln in t.lines.submobjects if ln not in kept]
    if gone:                       # first the lines that go (nothing slides through them)
        scene.play(FadeOut(VGroup(*gone)), run_time=0.25)
        for ln in gone:
            t.lines.remove(ln)
            scene.remove(ln)
    anims = [Transform(t.box, ref.box), Transform(t.bar, ref.bar), t.dots.animate.move_to(ref.dots)]
    if t.title is not None:
        anims.append(t.title.animate.move_to(ref.title))
    for i, ln in enumerate(kept):
        anims.append(ln.animate.shift(ref._slot(i) - ln.strut.get_corner(UP + LEFT)))
    scene.play(*anims, *extra, run_time=run_time)
    t.rows = rows
    return t


def bare_prompt(scene, t: Terminal):
    """The prompt returns (no output): a prompt line with nothing typed yet."""
    ln = t.type(scene, "", type_time=0)
    ln.bare = True
    return ln


def type_cmd(scene, t: Terminal, cmd: str, type_time: float | None = None):
    """Type at the waiting prompt (replacing a bare prompt line if there is one)."""
    if len(t.lines) and getattr(t.lines[-1], "bare", False):
        last = t.lines[-1]
        scene.remove(last, *last.submobjects)
        t.lines.remove(last)
    return t.type(scene, cmd, type_time)


def pin(scene, line, mob, run_time: float = 0.4, anim=None):
    """Show `mob` beside a terminal line and make it part of that line (it scrolls with it)."""
    scene.play(anim or FadeIn(mob, shift=LEFT * 0.1), run_time=run_time)
    scene.remove(mob)
    line.add(mob)
    scene.add(line)
    return mob


def unpin(scene, line, mob, run_time: float = 0.3):
    if mob in line.submobjects:
        line.remove(mob)
    scene.add(mob)
    scene.play(FadeOut(mob), run_time=run_time)


def time_tag(time: str) -> VGroup:
    """The GREY tag holding a live-view row's time (see live_split)."""
    return _keep(tag(time, S.GREY))


def place_time(tg, t: Terminal, line) -> VGroup:
    """Put a time tag at the right end of terminal line `line`, inside the frame."""
    return tg.move_to(line.strut).align_to(t.box, RIGHT).shift(LEFT * 0.12)


# ------------------------------------------------------------------ tags and badges
def your_turn() -> VGroup:
    """YELLOW '▶ your turn' tag: put it next to a command the viewer should run now."""
    return _keep(tag("▶ your turn", TURN))


def extra_tag() -> VGroup:
    return _keep(tag("extra", S.GREY))


def illustration_tag(note: str | None = None) -> VGroup:
    return _keep(tag("illustration" + (f" · {note}" if note else ""), S.GREY))


def expected_tag() -> VGroup:
    return _keep(tag("expected", S.GREY))


def recorded_tag(s: str = "at the time of recording") -> VGroup:
    return _keep(tag(s, S.GREY))


def nokey_tag() -> VGroup:
    return _keep(tag("recorded without the key", S.GREY))


def erratum_tag() -> VGroup:
    return _keep(tag("erratum", S.GREY))


def cost_tag(s: str = "billed to the course project") -> VGroup:
    return _keep(tag(s, COST))


def standin_tag() -> VGroup:
    return _keep(tag("stand-in file · not a real key", S.GREY))


def preview_tag() -> VGroup:
    return _keep(tag("preview", S.GREY))


def optional_tag() -> VGroup:
    return _keep(tag("optional", S.GREY))


def build_badge(k: int, words: bool = True) -> VGroup:
    """TEAL badge for BuildKit's [k/5]: a circled k, and with words=True "build step k"."""
    b = step_badge(k, CTR)
    if not words:
        return _keep(b)
    g = VGroup(b, sans(f"build step {k}", CAPTION, CTR)).arrange(RIGHT, buff=0.12)
    return _keep(g)


def stamp(text: str, color: str = ERR, size: float = TAG, angle: float = 0.08) -> VGroup:
    """An outlined, slightly rotated stamp ("CACHED", "would publish the key")."""
    t = sans(text, size, color, weight="BOLD")
    r = RoundedRectangle(width=t.width + 0.3, height=t.height + 0.22, corner_radius=0.06,
                         stroke_color=color, stroke_width=3).set_fill(S.BG, 0.85)
    t.move_to(r)
    g = VGroup(r, t).rotate(angle)
    g.frame, g.text = r, t
    return _keep(g)


def cached_stamp() -> VGroup:
    return stamp("CACHED", VENV, CAPTION)


# ------------------------------------------------------------------ panels and cards
_LANG = {".py": "python", ".toml": "toml", ".sh": "bash", ".md": "markdown", ".yaml": "yaml",
         ".json": "json", ".Dockerfile": "docker", ".txt": "text"}


def _lang(path: str) -> str:
    p = Path(path)
    if p.name == "Dockerfile" or p.suffix == ".Dockerfile":
        return "docker"
    if p.name in (".gitignore", ".dockerignore"):
        return "text"
    return _LANG.get(p.suffix, "text")


def _with_header(panel: VGroup, text: str, size: float = CAPTION) -> VGroup:
    """Replace a code_panel's header with `text` (path part mono, '· …' parts serif)."""
    path, _, rest = text.partition(" · ")
    head = mono(path, size, S.GREY)
    parts = [head]
    if rest:
        parts.append(label(f"· {rest}", size, S.GREY))
    header = VGroup(*parts).arrange(RIGHT, buff=0.14)
    header.next_to(panel.code, UP, buff=0.1).align_to(panel.code, LEFT).shift(RIGHT * 0.12)
    panel.remove(panel.header)
    panel.header = header
    panel.add(header)
    return panel


def src_panel(name: str, first: int, last: int | None = None, cut_comments: bool = False,
              focus=None, size: float = 22, width: float | None = None,
              shown_path: str | None = None, suffix: str | None = None,
              language: str | None = None) -> VGroup:
    """code_panel quoting assets/source/<name> lines first..last, header "path · lines a–b"
    (+ " · comment cut" when cut_comments removed a comment, + " · <suffix>").
    shown_path: the path printed in the header (default `name`; e.g. for solution-branch/...)."""
    last = first if last is None else last
    raw = excerpt(name, first, last)
    src = excerpt(name, first, last, cut_comments) if cut_comments else raw
    p = code_panel(src, shown_path or name, first, language or _lang(name), focus=focus,
                   font_size=size, width=width)
    extra = []
    if src != raw:
        extra.append("comment cut")
    if suffix:
        extra.append(suffix)
    if extra:
        where = f"line {first}" if first == last else f"lines {first}–{last}"
        _with_header(p, " · ".join([shown_path or name, where, *extra]))
    p.source_name, p.first = name, first
    return p


def file_panel(rel: str, first: int, last: int | None, path: str, focus=None, size: float = 22,
               width: float | None = None, language: str | None = None) -> VGroup:
    """code_panel quoting assets/terminal/<rel> (the student's Dockerfile in files/), headed
    "<path> · lines a–b"."""
    last = first if last is None else last
    return code_panel(asset_lines(rel, first, last), path, first, language or _lang(rel),
                      focus=focus, font_size=size, width=width)


def log_panel(lines: list[str], header: str, width: float = TERM_W, size: float = CAPTION,
              color: str = OUTPUT) -> VGroup:
    """Plain mono rows (a full build log, docker history) on a dark rounded panel with a GREY
    header above (path part mono). Rows longer than the panel are cut with '…'.
    .rows (mono_lines: use substring() to colour parts) .frame .header"""
    from explainer.devops import cell_width
    max_chars = int((width - 0.5) / cell_width(size))
    rows = VGroup()
    pitch = line_pitch(size)
    for i, s in enumerate(lines):
        s = s if len(s) <= max_chars else s[:max_chars - 1] + "…"
        ln = mono_line(s, size, color)
        ln.shift(np.array([0, -i * pitch, 0]) - ln.strut.get_corner(UP + LEFT))
        rows.add(ln)
    h = len(lines) * pitch + 0.4
    frame = RoundedRectangle(width=width, height=h, corner_radius=0.15, stroke_color=S.GREY_DARK,
                             stroke_width=2).set_fill(PANEL, 1)
    frame.move_to(rows.get_center()).align_to(rows, LEFT).shift(LEFT * 0.25)
    frame.shift(UP * (rows.get_top()[1] + 0.2 - frame.get_top()[1]))
    path, _, rest = header.partition(" · ")
    hp = [mono(path, CAPTION, S.GREY)] + ([label(f"· {rest}", CAPTION, S.GREY)] if rest else [])
    head = VGroup(*hp).arrange(RIGHT, buff=0.14).next_to(frame, UP, buff=0.1).align_to(frame, LEFT)
    head.shift(RIGHT * 0.12)
    g = VGroup(frame, rows, head)
    g.frame, g.rows, g.header = frame, rows, head
    return g


def readme_chip(where: str, phrase: str | None = None, size: float = CAPTION,
                max_w: float = 9.0) -> VGroup:
    """A one-line README chip: GREY mono `where` ("transcribe_audio/README.md · line 95") and the
    quoted phrase in white. Fails if wider than max_w (shorten the phrase). .where .phrase"""
    path, _, rest = where.partition(" · ")
    w = VGroup(mono(path, size, S.GREY), *([label(f"· {rest}", size, S.GREY)] if rest else []))
    w.arrange(RIGHT, buff=0.12)
    parts = [w]
    ph = None
    if phrase:
        ph = label(f"“{phrase}”", size, INK)
        parts.append(ph)
    row = VGroup(*parts).arrange(RIGHT, buff=0.25)
    for p in row:
        p.align_to(w, DOWN) if p is not w else None
    fr = box(row.width + 0.4, row.height + 0.24, S.GREY, fill=S.BG, fill_opacity=0.92, radius=0.1)
    fr.move_to(row)
    g = VGroup(fr, row)
    if g.width > max_w:
        raise ValueError(f"README chip {g.width:.1f} wide (> {max_w}): shorten {phrase!r}")
    g.frame, g.where, g.phrase = fr, w, ph
    return _keep(g)


def readme_card(where: str, lines: list[str], width: float | None = None,
                size: float = CAPTION) -> VGroup:
    """A multi-line GREY README card: header `where` above, the README's words inside.
    .frame .header .rows"""
    rows = VGroup(*[label(s, size, INK) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    w = max(width or 0, rows.width + 0.5)
    fr = box(w, rows.height + 0.4, S.GREY, fill=S.BG, fill_opacity=0.92, radius=0.12)
    rows.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.25)
    path, _, rest = where.partition(" · ")
    head = VGroup(mono(path, size, S.GREY), *([label(f"· {rest}", size, S.GREY)] if rest else []))
    head.arrange(RIGHT, buff=0.12).next_to(fr, UP, buff=0.08).align_to(fr, LEFT).shift(RIGHT * 0.1)
    g = VGroup(fr, rows, head)
    g.frame, g.rows, g.header = fr, rows, head
    return g


def editor_inset(panel, title: str = "VS Code · on your laptop") -> VGroup:
    """A GREY editor window (title bar + frame) around a code panel. .frame .title .panel"""
    pad = 0.18
    bar_h = 0.42
    w, h = panel.width + 2 * pad, panel.height + 2 * pad + bar_h
    fr = RoundedRectangle(width=w, height=h, corner_radius=0.12, stroke_color=S.GREY,
                          stroke_width=2).set_fill(S.BG, 1)
    fr.move_to(panel).shift(UP * bar_h / 2)
    bar = Line(fr.get_corner(UP + LEFT) + DOWN * bar_h, fr.get_corner(UP + RIGHT) + DOWN * bar_h,
               color=S.GREY, stroke_width=1.5)
    t = label(title, CAPTION, S.GREY).move_to(fr.get_top() + DOWN * bar_h / 2)
    g = VGroup(fr, bar, t, panel)
    g.frame, g.title, g.panel = fr, t, panel
    return g


def cmd_chip(cmd: str, note: str | None = None, color: str = S.GREY, size: float = CAPTION) -> VGroup:
    """A command shown, not typed: a mono chip, and an optional GREY note under it."""
    c = chip(cmd, color, size=size, font=MONO)
    if not note:
        return _keep(c)
    n = label(note, size, S.GREY).next_to(c, DOWN, buff=0.1)
    g = VGroup(c, n)
    g.chip, g.note = c, n
    return _keep(g)


# ------------------------------------------------------------------ glyphs
def key_glyph(h: float = 0.3, color: str = KEY, name: str | None = None) -> VGroup:
    """The service-account key: a GOLD key (its content is never drawn). name="mega-pipeline.json"
    adds the file name (mono 20, GOLD) to its right. .key .name"""
    bow = Circle(radius=h * 0.42, stroke_color=color, stroke_width=3).set_fill(color, 0.3)
    hole = Circle(radius=h * 0.12, stroke_color=color, stroke_width=2).set_fill(S.BG, 1).move_to(bow)
    a = bow.get_right()
    shaft = Line(a, a + RIGHT * h * 1.25, color=color, stroke_width=4)
    t1 = Line(a + RIGHT * h * 0.8, a + RIGHT * h * 0.8 + DOWN * h * 0.3, color=color, stroke_width=4)
    t2 = Line(a + RIGHT * h * 1.12, a + RIGHT * h * 1.12 + DOWN * h * 0.3, color=color, stroke_width=4)
    k = VGroup(bow, hole, shaft, t1, t2)
    if not name:
        k.key, k.name = k, None
        return _keep(k)
    n = mono(name, CAPTION, color).next_to(k, RIGHT, buff=0.14)
    g = VGroup(k, n)
    g.key, g.name = k, n
    return _keep(g)


def wave_token(h: float = 0.42, color: str = INK) -> VGroup:
    """A small waveform (audio): bars of different heights."""
    hs = [0.3, 0.65, 1.0, 0.5, 0.85, 0.4, 0.7, 0.3]
    bars = VGroup(*[Line(UP * h * f / 2, DOWN * h * f / 2, color=color, stroke_width=4) for f in hs])
    bars.arrange(RIGHT, buff=h * 0.13)
    bars.kind = "wave"
    return _keep(bars)


def page_token(long: bool = False, fr: bool = False, color: str = INK) -> VGroup:
    """A page of text: short (a transcript) or long (a podcast script); fr=True adds a small
    "FR" chip (a French page). Lines are bars, never real text."""
    h = 0.62 if long else 0.44
    pg = file_glyph(h, color)
    n = 6 if long else 3
    w = pg.width
    bars = VGroup(*[Line(LEFT * w * 0.28, RIGHT * w * (0.28 if i < n - 1 else 0.05), color=color,
                         stroke_width=2) for i in range(n)])
    bars.arrange(DOWN, buff=h * 0.07, aligned_edge=LEFT).move_to(pg).shift(DOWN * h * 0.06)
    g = VGroup(pg, bars)
    if fr:
        c = chip("FR", S.GREY, size=CAPTION, font=MONO, pad_x=0.1, pad_y=0.04)
        c.next_to(pg, RIGHT, buff=0.06).align_to(pg, DOWN)
        g.add(c)
    g.kind = "fr" if fr else ("long" if long else "page")
    return _keep(g)


def token(kind: str) -> VGroup:
    """A data token: 'wave', 'page' (short transcript), 'long' (podcast script), 'fr'."""
    return {"wave": wave_token, "page": page_token, "long": lambda: page_token(long=True),
            "fr": lambda: page_token(fr=True)}[kind]()


def signpost(lines: list[str], color: str = LOOKUP, size: float = CAPTION,
             post_h: float = 0.55) -> VGroup:
    """A PINK signpost: an arrow-shaped board (mono text, pointing right) on a post.
    .board .text .post .root (the point where it is planted)"""
    txt = VGroup(*[mono(s, size, color) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    w, h, tip = txt.width + 0.4, txt.height + 0.26, 0.28
    x0, y0 = -w / 2, -h / 2
    board = Polygon([x0, y0, 0], [x0 + w, y0, 0], [x0 + w + tip, 0, 0], [x0 + w, -y0, 0], [x0, -y0, 0],
                    stroke_color=color, stroke_width=2.5).set_fill(S.BG, 0.95)
    txt.move_to(board).align_to(board, LEFT).shift(RIGHT * 0.2)
    px = x0 + 0.3
    post = Line([px, y0, 0], [px, y0 - post_h, 0], color=color, stroke_width=4)
    foot = Line([px - 0.18, y0 - post_h, 0], [px + 0.18, y0 - post_h, 0], color=color, stroke_width=4)
    g = VGroup(post, foot, board, txt)
    g.board, g.text, g.post, g.foot = board, txt, post, foot
    g.root = lambda: foot.get_center()
    return _keep(g)


def clock_glyph(r: float = 0.13, color: str = COST) -> VGroup:
    c = Circle(radius=r, stroke_color=color, stroke_width=2.5)
    h1 = Line(ORIGIN, UP * r * 0.65, color=color, stroke_width=2.5)
    h2 = Line(ORIGIN, RIGHT * r * 0.5, color=color, stroke_width=2.5)
    return VGroup(c, h1, h2)


def token_tag(text: str = "token") -> VGroup:
    """The short-lived access token: a GOLD tag with a small clock."""
    t = sans(text, CAPTION, COST)
    ck = clock_glyph(0.12)
    row = VGroup(ck, t).arrange(RIGHT, buff=0.1)
    fr = RoundedRectangle(width=row.width + 0.34, height=row.height + 0.18, corner_radius=0.1,
                          stroke_color=COST, stroke_width=2.5).set_fill(COST, 0.12).move_to(row)
    g = VGroup(fr, row)
    g.frame, g.text = fr, t
    return _keep(g)


def padlock(h: float = 0.42, color: str = CLOUD) -> VGroup:
    """A padlock (IAM). .body .shackle"""
    body = RoundedRectangle(width=h * 0.9, height=h * 0.62, corner_radius=h * 0.08,
                            stroke_color=color, stroke_width=2.5).set_fill(color, 0.25)
    sh = Arc(radius=h * 0.27, start_angle=0, angle=PI, stroke_color=color, stroke_width=3.5)
    sh.next_to(body, UP, buff=0)
    legs = VGroup(Line(sh.get_start(), sh.get_start() + DOWN * h * 0.08, color=color, stroke_width=3.5),
                  Line(sh.get_end(), sh.get_end() + DOWN * h * 0.08, color=color, stroke_width=3.5))
    shackle = VGroup(sh, legs)
    g = VGroup(shackle, body)
    g.body, g.shackle = body, shackle
    return g


def stub_glyph(text: str | None = "operation", color: str = CTR) -> VGroup:
    """A ticket stub (a long-running operation): TEAL outline, a perforation, an optional word."""
    w, h = 1.6, 0.56
    fr = RoundedRectangle(width=w, height=h, corner_radius=0.08, stroke_color=color,
                          stroke_width=2.5).set_fill(color, 0.08)
    perf = DashedLine(fr.get_corner(UP + LEFT) + RIGHT * 0.3, fr.get_corner(DOWN + LEFT) + RIGHT * 0.3,
                      color=color, stroke_width=2, dash_length=0.05)
    g = VGroup(fr, perf)
    if text:
        t = sans(text, CAPTION, color).move_to(fr).shift(RIGHT * 0.15)
        g.add(t)
    g.frame = fr
    return _keep(g)


def parcel_glyph(h: float = 0.7, caption: str | None = "build context") -> VGroup:
    """Lecture 2's parcel (the build context): a taped box, GREY caption under it."""
    b = RoundedRectangle(width=h * 1.3, height=h, corner_radius=0.06, stroke_color=S.GREY,
                         stroke_width=2.5).set_fill(S.GREY, 0.15)
    tape = VGroup(Line(b.get_top(), b.get_bottom(), color=S.GREY, stroke_width=3),
                  Line(b.get_left(), b.get_right(), color=S.GREY, stroke_width=3))
    g = VGroup(b, tape)
    if caption:
        g.add(label(caption, CAPTION, S.GREY).next_to(b, DOWN, buff=0.1))
    g.frame = b
    return _keep(g)


def builder_box(text: str = "builder") -> VGroup:
    """Docker's builder (a tool: PURPLE)."""
    t = sans(text, CAPTION, TOOL)
    fr = box(t.width + 0.6, 0.62, TOOL, fill_opacity=0.12).move_to(t)
    g = VGroup(fr, t)
    g.frame = fr
    return _keep(g)


def sieve(name: str = ".gitignore", w: float = 1.8, color: str = S.GREY) -> VGroup:
    """A sieve: a shallow bowl with a mesh, its file name (mono 20) to its left. .bowl .name"""
    bowl = Polygon([-w / 2, 0.16, 0], [w / 2, 0.16, 0], [w * 0.38, -0.16, 0], [-w * 0.38, -0.16, 0],
                   stroke_color=color, stroke_width=3).set_fill(color, 0.08)
    mesh = VGroup(*[Line([x, 0.16, 0], [x * 0.78, -0.16, 0], color=color, stroke_width=1.5)
                    for x in np.linspace(-w * 0.42, w * 0.42, 9)])
    n = mono(name, CAPTION, color).next_to(bowl, LEFT, buff=0.15)
    g = VGroup(bowl, mesh, n)
    g.bowl, g.name = VGroup(bowl, mesh), n
    return _keep(g)


def book_glyph(caption: str = "Git history", w: float = 1.6, color: str = S.GREY) -> VGroup:
    """An open book (Git's history), caption under it."""
    h = w * 0.62
    left = Polygon([-w / 2, -h / 2, 0], [0, -h / 2 + 0.06, 0], [0, h / 2, 0], [-w / 2, h / 2 - 0.06, 0],
                   stroke_color=color, stroke_width=2.5).set_fill(color, 0.12)
    right = left.copy().flip(UP, about_point=ORIGIN)
    lines = VGroup(*[Line([-w * 0.4, y, 0], [-w * 0.08, y + 0.02, 0], color=color, stroke_width=1.5)
                     for y in np.linspace(h * 0.25, -h * 0.25, 4)])
    lines.add(*[ln.copy().flip(UP, about_point=ORIGIN) for ln in list(lines)])
    g = VGroup(left, right, lines)
    if caption:
        g.add(label(caption, CAPTION, color).next_to(g, DOWN, buff=0.1))
    return _keep(g)


def ship_box(caption: str = "image", w: float = 1.7, color: str = CTR) -> VGroup:
    """The image as a shipping box (TEAL): front, lid, caption under it. .front"""
    h = w * 0.62
    front = Rectangle(width=w, height=h, stroke_color=color, stroke_width=3).set_fill(color, 0.12)
    d = w * 0.18
    lid = Polygon(front.get_corner(UP + LEFT), front.get_corner(UP + RIGHT),
                  front.get_corner(UP + RIGHT) + np.array([d, d, 0]),
                  front.get_corner(UP + LEFT) + np.array([d, d, 0]),
                  stroke_color=color, stroke_width=3).set_fill(color, 0.2)
    side = Polygon(front.get_corner(UP + RIGHT), front.get_corner(DOWN + RIGHT),
                   front.get_corner(DOWN + RIGHT) + np.array([d, d, 0]),
                   front.get_corner(UP + RIGHT) + np.array([d, d, 0]),
                   stroke_color=color, stroke_width=3).set_fill(color, 0.06)
    g = VGroup(front, side, lid)
    if caption:
        g.add(label(caption, CAPTION, color).next_to(front, DOWN, buff=0.1))
    g.front = front
    return _keep(g)


def hub_shelf(caption: str = "Docker Hub", w: float = 2.2, color: str = S.GREY) -> VGroup:
    """A public shelf (Docker Hub; no logo): two boards on uprights, caption under it."""
    b1 = Line(LEFT * w / 2, RIGHT * w / 2, color=color, stroke_width=4)
    b2 = b1.copy().shift(UP * 0.7)
    ups = VGroup(Line(LEFT * w / 2 + DOWN * 0.05, LEFT * w / 2 + UP * 0.95, color=color, stroke_width=3),
                 Line(RIGHT * w / 2 + DOWN * 0.05, RIGHT * w / 2 + UP * 0.95, color=color, stroke_width=3))
    g = VGroup(b1, b2, ups)
    if caption:
        g.add(label(caption, CAPTION, color).next_to(b1, DOWN, buff=0.12))
    g.board = b1
    return _keep(g)


def pkg_dots(n: int, cols: int = 13, color: str = VENV, w: float = 0.15, buff: float = 0.05) -> VGroup:
    """n tiny package chips (no names) in rows of `cols`: the 26 packages of uv add."""
    dots = VGroup(*[RoundedRectangle(width=w, height=w * 0.75, corner_radius=w * 0.2, stroke_width=1.5,
                                     stroke_color=color).set_fill(color, 0.75) for _ in range(n)])
    dots.arrange_in_grid(cols=cols, buff=buff)
    return dots


def file_row(name: str, color: str = INK, glyph_color: str = S.GREY, size: float = CAPTION) -> VGroup:
    """A file (or folder, name ending in '/') glyph + its mono name. .glyph .text .name"""
    g = folder_glyph(0.22, glyph_color) if name.endswith("/") else file_glyph(0.28, glyph_color)
    t = mono(name, size, color).next_to(g, RIGHT, buff=0.12)
    row = VGroup(g, t)
    row.glyph, row.text, row.name = g, t, name
    return _keep(row)


def ghost_file(name: str = "Dockerfile", color: str = S.GREY) -> VGroup:
    """A dashed GREY file that doesn't exist yet ("you write it")."""
    g = file_glyph(0.28, color)
    g = DashedVMobject(g[0], num_dashes=18).set_stroke(color, 2)
    t = mono(name, CAPTION, color).next_to(g, RIGHT, buff=0.12)
    row = VGroup(g, t)
    row.glyph, row.text, row.name = g, t, name
    return _keep(row)


# ------------------------------------------------------------------ the set-piece base
class Piece(VGroup):
    """A set piece: a VGroup with named parts that can be shown later, and helpers that keep the
    scene clean (no strays at the end). Subclasses fill self.parts and add the visible ones."""

    def __init__(self, **kw):
        super().__init__(**kw)
        self.parts: dict[str, object] = {}

    def attach(self, scene, *mobs, anims=None, run_time: float = 0.5, extra=()):
        """Play `anims` (default: FadeIn of each mob), then make the mobs part of this piece.
        Returns the first mob (or all of them as a VGroup)."""
        anims = list(anims) if anims is not None else [FadeIn(m) for m in mobs]
        scene.play(*anims, *extra, run_time=run_time)
        for m in mobs:
            if m in scene.mobjects:
                scene.remove(m)
            if m not in self.submobjects:
                self.add(m)
        if self not in scene.mobjects:
            scene.add(self)
        return mobs[0] if len(mobs) == 1 else VGroup(*mobs)

    def detach(self, scene, *mobs, anims=None, run_time: float = 0.5, extra=()):
        """The reverse: take the mobs out of the piece and play `anims` (default FadeOut)."""
        for m in mobs:
            if m in self.submobjects:
                self.remove(m)
            scene.add(m)
        scene.play(*(list(anims) if anims is not None else [FadeOut(m) for m in mobs]), *extra,
                   run_time=run_time)
        for m in mobs:
            if m in scene.mobjects:
                scene.remove(m)

    def reveal(self, scene, *names, run_time: float = 0.6, anim=None, extra=()):
        """Show named parts built but not yet shown (FadeIn, or anim(mob)). Returns them."""
        mobs = [self.parts[n] for n in names]
        anims = [(anim or FadeIn)(m) for m in mobs]
        return self.attach(scene, *mobs, anims=anims, run_time=run_time, extra=extra)

    def hide(self, scene, *names, run_time: float = 0.4):
        self.detach(scene, *[self.parts[n] for n in names], run_time=run_time)

    def rescale(self, k: float, about_point=None):
        """Scale every shape by k but keep every text (and every chip, tag, labelled glyph) at
        its own size, so text stays >= 20 pt. Use via .animate.rescale(k)."""
        units: list = []

        def walk(m):
            if getattr(m, "keep_size", False) or isinstance(m, Text) or hasattr(m, "pt"):
                units.append(m)
                return
            for s in m.submobjects:
                walk(s)

        for s in self.submobjects:
            walk(s)
        self.scale(k, about_point=self.get_center() if about_point is None else about_point)
        for u in units:
            u.scale(1 / k)
        return self


# ------------------------------------------------------------------ V1 · the relay through the bucket
class Relay(Piece):
    """V1. Five TEAL boxes A-E along the top, the bucket as six BLUE drawers along the bottom (in
    pipeline order, PREFIXES) and a small dashed bonus drawer under the sixth. Box j sits above
    the gap after drawer j; it reads READS[j] and writes WRITES[j]. ~12.4 x 4.5.

        relay = Relay(labels=False)                 # S01 teaser: no labels
        tok = relay.token_at(0, "wave"); self.play(FadeIn(relay), FadeIn(tok))
        [tok] = relay.run(self, [(tok, 0)])         # A: wave -> page, into text_prompts/
        [tok] = relay.run(self, [(tok, 1)])         # B: -> long page
        tc, td = relay.run(self, [(tok, 2), (tok.copy(), 3)])     # the split: C and D together
        [te] = relay.run(self, [(td, 4)])
        relay.reveal(self, "drawer_labels")        # parts: drawer_labels, box_labels, edges, bonus_tag
    .boxes[j] (frame) .drawers[i] (.frame .handle) .bonus .box_labels[j] (letter + two-line
    folder name) .drawer_labels[i] (two-line prefix + content icon) .read_edges[j] .write_edges[j]
    .slot(i) (where a token rests in drawer i) .center_of(j) (box centre). Tokens are not part
    of the piece: the scene owns (and fades) them."""

    def __init__(self, width: float = 12.4, labels: bool = True, edges: bool = False,
                 bonus: bool = True, box_h: float = 1.3, drawer_h: float = 1.45, gap: float = 1.05,
                 **kw):
        super().__init__(**kw)
        p = width / 6
        self.pitch = p
        dw, bw = p - 0.12, p - 0.22
        y_d = 0.0                                  # drawers' top edge (shifted at the end)
        self.drawers = VGroup()
        for i in range(6):
            x = -width / 2 + (i + 0.5) * p
            fr = RoundedRectangle(width=dw, height=drawer_h, corner_radius=0.1, stroke_color=CLOUD,
                                  stroke_width=2.5).set_fill(CLOUD, 0.1)
            fr.move_to([x, y_d - drawer_h / 2, 0])
            handle = RoundedRectangle(width=0.42, height=0.08, corner_radius=0.04, stroke_width=0) \
                .set_fill(CLOUD, 0.9).move_to(fr.get_top() + DOWN * 0.16)
            d = VGroup(fr, handle)
            d.frame, d.handle = fr, handle
            self.drawers.add(d)
        cab = RoundedRectangle(width=width + 0.16, height=drawer_h + 0.16, corner_radius=0.14,
                               stroke_color=CLOUD, stroke_width=1.5, stroke_opacity=0.6)
        cab.move_to([0, y_d - drawer_h / 2, 0])
        self.cabinet = cab
        self.boxes = VGroup()
        y_b = y_d + gap + box_h / 2
        for j in range(5):
            x = -width / 2 + (j + 1) * p
            fr = RoundedRectangle(width=bw, height=box_h, corner_radius=0.12, stroke_color=CTR,
                                  stroke_width=3).set_fill(CTR, 0.1)
            self.boxes.add(fr.move_to([x, y_b, 0]))
        self.add(cab, self.drawers, self.boxes)
        # the bonus drawer (dashed, under the sixth)
        d5 = self.drawers[5].frame
        bf = box(dw, 0.72, CLOUD, dashed=True).next_to(d5, DOWN, buff=0.16)
        bl = two_lines(BONUS_PREFIX, CAPTION, CLOUD).move_to(bf)
        self.bonus = VGroup(bf, bl)
        self.bonus.frame, self.bonus.text = bf, bl
        if bonus:
            self.add(self.bonus)
        bt = tag("bonus", S.GREY).next_to(bf, LEFT, buff=0.2)
        self.parts["bonus_tag"] = _keep(bt)
        # labels (built always; shown now or later with reveal)
        self.drawer_labels = VGroup()
        for i, d in enumerate(self.drawers):
            t = two_lines(PREFIXES[i], CAPTION, INK)
            t.move_to(d.frame.get_top() + DOWN * (0.3 + t.height / 2))
            ic = token(DRAWER_KIND[i]).move_to(self.slot(i))
            g = VGroup(t, ic)
            g.text, g.icon = t, ic
            self.drawer_labels.add(g)
        self.box_labels = VGroup()
        for j, b in enumerate(self.boxes):
            let = sans(LETTERS[j], 34, CTR, weight="BOLD")
            nm = two_lines(COMPONENTS[j], CAPTION, INK)
            g = VGroup(let, nm).arrange(DOWN, buff=0.08).move_to(b)
            g.letter, g.name = let, nm
            self.box_labels.add(g)
        self.parts["drawer_labels"] = self.drawer_labels
        self.parts["box_labels"] = self.box_labels
        if labels:
            self.add(self.drawer_labels, self.box_labels)
        # edges: drawer -> box (read), box -> drawer (write)
        self.read_edges, self.write_edges = VGroup(), VGroup()
        for j, b in enumerate(self.boxes):
            r, w = self.drawers[READS[j]].frame, self.drawers[WRITES[j]].frame
            self.read_edges.add(self._edge(r.get_top() + RIGHT * 0.38, b.get_bottom() + LEFT * 0.32))
            self.write_edges.add(self._edge(b.get_bottom() + RIGHT * 0.32, w.get_top() + LEFT * 0.38))
        self.edges = VGroup(self.read_edges, self.write_edges)
        self.parts["edges"] = self.edges
        if edges:
            self.add(self.edges)
        self.move_to(ORIGIN)

    @staticmethod
    def _edge(a, b, color=S.GREY):
        return Arrow(a, b, buff=0.06, stroke_width=2.5, color=color, max_tip_length_to_length_ratio=0.18,
                     max_stroke_width_to_length_ratio=10)

    def slot(self, i: int):
        """Where a token rests in drawer i (the lower part, where its content icon sits)."""
        fr = self.drawers[i].frame
        return fr.get_bottom() + UP * 0.32

    def center_of(self, j: int):
        return self.boxes[j].get_center()

    def token_at(self, i: int, kind: str | None = None) -> VGroup:
        """A new token (not on screen) resting in drawer i; kind defaults to what drawer i holds."""
        return token(kind or DRAWER_KIND[i]).move_to(self.slot(i))

    def run(self, scene, routes, run_time: float = 2.4, flash: bool = True) -> list:
        """Each route (token, j): the token rises from its drawer into box j, becomes OUT_KIND[j]
        (or route[2] if given) and drops into drawer WRITES[j]. Routes play in parallel.
        Returns the new tokens (on screen, owned by the scene)."""
        t1, t2, t3 = run_time * 0.38, run_time * 0.24, run_time * 0.38
        scene.play(*[tok.animate.move_to(self.center_of(r[1])).scale(0.85) for tok, *r in
                     [(rt[0], *rt[1:]) for rt in routes]], run_time=t1)
        news, anims = [], []
        for rt in routes:
            tok, j = rt[0], rt[1]
            kind = rt[2] if len(rt) > 2 else OUT_KIND[j]
            new = token(kind).scale(0.85).move_to(self.center_of(j))
            news.append(new)
            anims.append(Transform(tok, new))
            if flash:
                anims.append(Indicate(self.boxes[j], color=CTR, scale_factor=1.06))
        scene.play(*anims, run_time=t2)
        for tok, new in zip([rt[0] for rt in routes], news):
            scene.remove(tok)
            scene.add(new)
        scene.play(*[n.animate.scale(1 / 0.85).move_to(self.slot(WRITES[rt[1]]))
                     for n, rt in zip(news, routes)], run_time=t3)
        return news


class SubDrawers(Piece):
    """V1 detail: one drawer (`prefix`) opened into group sub-drawers in a row, the last one
    the "default group" (flash it RED when a box with the unchanged group_name writes there).
    Tag it illustration. ~ (2.1 per group) x 1.4.
    .title (mono prefix) .drawers[i] (frame + name) .slot(i) .flash(i, color) -> animation"""

    def __init__(self, prefix: str = "text_prompts/",
                 groups=("group-01/", "group-02/", "group-03/", "…", "default group"),
                 w: float = 1.95, h: float = 0.82, buff: float = 0.15, **kw):
        super().__init__(**kw)
        self.drawers = VGroup()
        for g in groups:
            fr = RoundedRectangle(width=w, height=h, corner_radius=0.08, stroke_color=CLOUD,
                                  stroke_width=2.5).set_fill(CLOUD, 0.1)
            t = (mono(g, CAPTION, INK) if g.endswith("/") else label(g, CAPTION, INK))
            t.move_to(fr.get_top() + DOWN * 0.24)
            d = VGroup(fr, t)
            d.frame, d.text, d.name = fr, t, g
            self.drawers.add(d)
        self.drawers.arrange(RIGHT, buff=buff)
        self.title = mono(prefix, CAPTION, CLOUD).next_to(self.drawers, UP, buff=0.15)
        self.title.align_to(self.drawers, LEFT)
        self.default = len(groups) - 1
        self.add(self.title, self.drawers)

    def slot(self, i: int):
        return self.drawers[i].frame.get_bottom() + UP * 0.25

    def flash(self, i: int, color: str = ERR, run_time: float = 0.8):
        fr = self.drawers[i].frame
        return AnimationGroup(Indicate(fr, color=color, scale_factor=1.08),
                              fr.animate.set_stroke(color, 3.5).set_fill(color, 0.2), run_time=run_time)


class Leaderboard(Piece):
    """A schematic leaderboard (tag it illustration; caption it with README.md line 54): rows of
    groups, columns of stages; .light(r, c) fills a cell GREEN. ~11.3 x 2.4.
    .cells[r][c] .row_names .col_names"""

    def __init__(self, groups=("group-01", "group-02", "group-03"),
                 stages=("Transcribe", "Generate", "Synthesize EN", "Translate", "Synthesize FR"),
                 col_w: float = 1.95, row_h: float = 0.5, name_w: float = 1.6, **kw):
        super().__init__(**kw)
        self.col_names = VGroup(*[label(s, CAPTION, S.GREY).move_to([name_w + (c + 0.5) * col_w, 0, 0])
                                  for c, s in enumerate(stages)])
        self.row_names = VGroup()
        self.cells = []
        grid = VGroup()
        for r, g in enumerate(groups):
            y = -(r + 1) * row_h - 0.05
            self.row_names.add(mono(g, CAPTION, INK).move_to([name_w / 2, y, 0]))
            row = []
            for c in range(len(stages)):
                cell = RoundedRectangle(width=col_w - 0.12, height=row_h - 0.1, corner_radius=0.06,
                                        stroke_color=S.GREY_DARK, stroke_width=2).set_fill(S.GREY_DARKER, 1)
                cell.move_to([name_w + (c + 0.5) * col_w, y, 0])
                row.append(cell)
                grid.add(cell)
            self.cells.append(row)
        self.grid = grid
        self.add(self.col_names, self.row_names, grid)
        self.move_to(ORIGIN)

    def light(self, r: int, c: int, color: str = VENV):
        return self.cells[r][c].animate.set_fill(color, 0.55).set_stroke(color, 2)


# ------------------------------------------------------------------ V2 · Dockerfile -> layer stack
# name: (default text, colour, height, build step)
SLABS = {
    "base": ("Debian 12 + Python 3.12", SYSTEM, 0.46, 1),
    "apt": ("RUN · apt, pip, uv, user app", SYSTEM, 0.6, 2),
    "workdir": (None, CTR, 0.07, 3),
    "copy": (None, LAPTOP, 0.3, 4),
    "sync": ("venv · /home/app/.venv", VENV, 0.38, 5),
}
STEP_OF = {k: v[3] for k, v in SLABS.items()}


class LayerStack(Piece):
    """V2. The image's layers as translucent slabs, bottom-up, on a GREY floor line.

        st = LayerStack().move_to([4.6, -3.0, 0], aligned_edge=DOWN)   # place it (floor = bottom)
        st.drop(self, "base")                           # ORANGE "Debian 12 + Python 3.12"
        st.drop(self, "apt", src=keyword_copy)          # a mobject that turns into the slab
        self.play(*st.grow("apt", 1.0))                 # S06: the apt layer swells
        self.play(FadeIn(st.badge("copy")))             # TEAL [4]; st.stamp("apt") GREEN CACHED
    Slab names and defaults: SLABS (text, colour, height, build step). The slab_w default 3.4
    fits 20 pt sans text of ~3 units. .slabs[name] (.box .label .h) .floor .top_y()
    Positioned helpers (not added: animate them in, then st.attach or pin them yourself):
    .badge(name) .stamp(name) .size_label(name, text) .top_label(text) .brace(text)
    .chips(name, n=26) .files(name="copy", key=True)."""

    def __init__(self, slab_w: float = 3.4, gap: float = 0.035, **kw):
        super().__init__(**kw)
        self.slab_w, self.gap = slab_w, gap
        self.floor = Line(LEFT * (slab_w / 2 + 0.25), RIGHT * (slab_w / 2 + 0.25), color=S.GREY,
                          stroke_width=3)
        self.slabs: dict[str, VGroup] = {}
        self.order: list[str] = []
        self.add(self.floor)

    def top_y(self) -> float:
        if not self.order:
            return self.floor.get_center()[1]
        return self.slabs[self.order[-1]].box.get_top()[1]

    def make(self, name: str, text: str | None = None, color: str | None = None,
             h: float | None = None, dashed: bool = False) -> VGroup:
        """A slab positioned on top of the stack (not added)."""
        d_text, d_col, d_h, _ = SLABS.get(name, (None, CTR, 0.4, None))
        text = d_text if text is None else text
        color, h = color or d_col, h or d_h
        b = box(self.slab_w, h, color, fill_opacity=0.25, radius=min(0.06, h / 2), dashed=dashed,
                stroke=2.5 if h > 0.12 else 2)
        b.move_to([self.floor.get_center()[0], self.top_y() + self.gap + h / 2, 0])
        lab = sans(text, CAPTION, INK).move_to(b) if text and h >= 0.3 else VGroup()
        s = VGroup(b, lab)
        s.box, s.label, s.h, s.name, s.color = b, lab, h, name, color
        return s

    def drop(self, scene, name: str, text: str | None = None, color: str | None = None,
             h: float | None = None, src=None, run_time: float = 0.7, extra=()) -> VGroup:
        """Drop a new slab onto the stack (from `src`, a mobject that transforms into it, or from
        above). Returns the slab."""
        s = self.make(name, text, color, h)
        if src is not None:
            anims = [Transform(src, s)]
        else:
            anims = [FadeIn(s, shift=DOWN * 0.5)]
        scene.play(*anims, *extra, run_time=run_time)
        if src is not None:
            scene.remove(src)
        self.slabs[name] = s
        self.order.append(name)
        self.add(s)
        if self not in scene.mobjects:
            scene.add(self)
        return s

    def grow(self, name: str, h: float) -> list:
        """Animations: slab `name` takes height h; the slabs above move with it."""
        s = self.slabs[name]
        dh = h - s.h
        nb = box(self.slab_w, h, s.color, fill_opacity=0.25, radius=min(0.06, h / 2))
        nb.move_to(s.box.get_bottom() + UP * h / 2)
        anims = [Transform(s.box, nb)]
        if len(s.label):
            anims.append(s.label.animate.move_to(nb))
        above = self.order[self.order.index(name) + 1:]
        for n in above:
            anims.append(self.slabs[n].animate.shift(UP * dh))
        s.h = h
        return anims

    def badge(self, name: str, words: bool = False) -> VGroup:
        """TEAL build-step badge [k] at the slab's left (positioned)."""
        b = build_badge(STEP_OF.get(name, 0), words=words)
        return b.next_to(self.slabs[name].box, LEFT, buff=0.15)

    def stamp(self, name: str, text: str = "CACHED", color: str = VENV) -> VGroup:
        st = stamp(text, color, CAPTION)
        sb = self.slabs[name].box
        return st.move_to(sb.get_right() + LEFT * (st.width / 2 + 0.1))

    def size_label(self, name: str, text: str, color: str | None = None) -> Text:
        s = self.slabs[name]
        return mono(text, CAPTION, color or s.color).next_to(s.box, RIGHT, buff=0.15)

    def top_label(self, text: str = "start: bash, venv on", color: str = CTR) -> Text:
        return sans(text, CAPTION, color).next_to(VGroup(*[self.slabs[n] for n in self.order]),
                                                   UP, buff=0.12)

    def brace(self, text: str, note: str | None = None, color: str = S.GREY) -> VGroup:
        slabs = VGroup(*[self.slabs[n].box for n in self.order])
        br = Brace(slabs, RIGHT, color=color)
        t = sans(text, CAPTION, INK).next_to(br, RIGHT, buff=0.1)
        g = VGroup(br, t)
        if note:
            g.add(label(note, CAPTION, S.GREY).next_to(t, DOWN, buff=0.08, aligned_edge=LEFT))
        return g

    def chips(self, name: str, n: int = 26, color: str = VENV) -> VGroup:
        """n tiny package chips filling slab `name` (positioned)."""
        sb = self.slabs[name].box
        cols = max(1, int((sb.width - 0.3) / 0.2))
        d = pkg_dots(n, cols=min(cols, 13), color=color)
        if d.height > sb.height - 0.06:
            d.scale_to_fit_height(sb.height - 0.06)
        return d.move_to(sb)

    def files(self, name: str = "copy", key: bool = True) -> VGroup:
        """Tiny GREY file glyphs (and a tiny GOLD key) inside slab `name` (positioned)."""
        sb = self.slabs[name].box
        h = max(0.12, sb.height - 0.1)
        g = VGroup(*[file_glyph(h, LAPTOP) for _ in range(5)])
        if key:
            g.add(key_glyph(h * 0.6))
        g.arrange(RIGHT, buff=0.12)
        return g.move_to(sb)


class ConfigCard(Piece):
    """Lecture 2's TEAL config card: ARG / ENV / USER / CMD write lines here, no layers.
    Slots fill column by column (rows per column). Default 8.6 x ~2.1 (2 columns of 4 lines).

        card = ConfigCard().to_corner(...)
        card.write(self, "DEBIAN_PACKAGES · build time", SYSTEM, key="arg")
        self.play(card.restyle("uv", "venv in /home/app/.venv", VENV))
    A line wider than its column raises ValueError (shorten it, or use cols=1).
    .lines (key -> text mobject) .frame .title"""

    def __init__(self, width: float = 8.6, rows: int = 4, cols: int = 2,
                 title: str = "image config · no layers", **kw):
        super().__init__(**kw)
        self.rows, self.cols, self.card_w = rows, cols, width
        self.pitch = 0.4
        h = 0.42 + rows * self.pitch + 0.18
        self.frame = box(width, h, CTR, fill_opacity=0.06)
        self.title = sans(title, CAPTION, CTR).move_to(self.frame.get_corner(UP + LEFT) + np.array([0.2, -0.24, 0]),
                                                       aligned_edge=LEFT)
        self.col_w = (width - 0.4) / cols
        self.lines: dict = {}
        self.used = 0
        self.add(self.frame, self.title)

    def slot(self, i: int):
        c, r = divmod(i, self.rows)
        return self.frame.get_corner(UP + LEFT) + np.array([0.2 + c * self.col_w, -0.62 - r * self.pitch, 0])

    def line(self, text: str, color: str = INK, key=None, slot: int | None = None,
             font: str = "sans") -> Text:
        """A positioned line (not added) in the next free slot (or `slot`)."""
        i = self.used if slot is None else slot
        if i >= self.rows * self.cols:
            raise ValueError("config card is full")
        t = mono(text, CAPTION, color) if font == "mono" else sans(text, CAPTION, color)
        if t.width > self.col_w - 0.1:
            raise ValueError(f"config line {text!r} is {t.width:.2f} wide; a column holds "
                             f"{self.col_w - 0.1:.2f}")
        t.move_to(self.slot(i), aligned_edge=LEFT)
        if slot is None:
            self.used += 1
        t.slot_index = i
        self.lines[key if key is not None else text] = t
        return t

    def write(self, scene, text: str, color: str = INK, key=None, slot: int | None = None,
              font: str = "sans", run_time: float = 0.5, src=None, extra=()) -> Text:
        """Write a line on the card (from `src`, a mobject that turns into it, if given)."""
        t = self.line(text, color, key, slot, font)
        if src is not None:
            scene.play(Transform(src, t), *extra, run_time=run_time)
            scene.remove(src)
            self.add(t)
            return t
        return self.attach(scene, t, anims=[Write(t)], run_time=run_time, extra=extra)

    def restyle(self, key, text: str | None = None, color: str | None = None, font: str = "sans"):
        """Transform: line `key` gets new text and/or colour in the same slot."""
        old = self.lines[key]
        t = (mono if font == "mono" else sans)(text or old.text, CAPTION, color or old.get_color())
        if t.width > self.card_w - 0.4 - (old.slot_index // self.rows) * self.col_w:
            raise ValueError(f"config line {text!r} is too wide for the card")
        t.move_to(self.slot(old.slot_index), aligned_edge=LEFT)
        return Transform(old, t)


# ------------------------------------------------------------------ V3 + V4 · the window
class Window(Piece):
    """V3 (+ V4). Left: your laptop's component folder (GREY). Right: the image (TEAL) with an
    /app cavity holding the copied files and a GREEN /home/app/.venv box OUTSIDE it; on top, the
    container's dashed TEAL writable sheet with a GREEN shelf above the venv (uv add's packages
    land there). Between them the PINK `-v "$(pwd):/app"` route (after mount()). ~12.4 x 3.4
    with 4 files.

        win = Window()                          # unmounted; Window(mounted=True) starts mounted
        self.play(FadeIn(win)); win.mount(self)          # route + the laptop sheet covers /app
        self.play(win.blink("cli.py"))                   # the same file blinks on both sides
        win.add_file(self, "uv.lock", VENV)              # appears on both sides at once
        chips = win.fill_shelf(self, 26)                 # packages on the writable sheet
        win.evaporate(self)                              # exit: sheet + chips vanish
    .laptop (.frame .folder .rows) .image (.frame .cavity .copied .venv) .sheet (.frame .shelf
    .caption) .route .route_label .cover (.rows) — names: .row(name, side="laptop"|"cover"|"copied").
    """

    def __init__(self, files=("cli.py", "Dockerfile", "pyproject.toml", "secrets/"), copied=None,
                 rows: int | None = None, component: str = "transcribe_audio", key: bool = False,
                 mounted: bool = False, sheet: bool = True, **kw):
        super().__init__(**kw)
        copied = list(copied if copied is not None else files)
        files = list(files)
        self.capacity = max(len(files), len(copied), rows or 0)
        self.pitch = 0.4
        self.key = key
        area_w, area_h = 3.15, self.capacity * self.pitch + 0.2
        lap_w, gap, venv_w = area_w + 0.3, 2.65, 2.85
        img_w = area_w + venv_w + 0.6
        head = 0.5
        blk_h = head + area_h + 0.2
        x_lap = -(lap_w + gap + img_w) / 2
        # laptop
        lap_fr = box(lap_w, blk_h, LAPTOP, fill_opacity=0.05)
        lap_fr.move_to([x_lap + lap_w / 2, blk_h / 2, 0])
        folder = mono(f"{component}/", CAPTION, LAPTOP).move_to(lap_fr.get_corner(UP + LEFT) +
                                                                  np.array([0.15, -0.27, 0]),
                                                                  aligned_edge=LEFT)
        lap_area = self._area(area_w, area_h).move_to(lap_fr.get_bottom() + UP * (0.15 + area_h / 2))
        lap_rows = self._rows(files, lap_area)
        lap_cap = label("your laptop", CAPTION, LAPTOP).next_to(lap_fr, DOWN, buff=0.12)
        self.laptop = VGroup(lap_fr, folder, lap_area, lap_rows, lap_cap)
        self.laptop.frame, self.laptop.folder, self.laptop.area, self.laptop.rows = lap_fr, folder, lap_area, lap_rows
        # image
        x_img = x_lap + lap_w + gap
        img_fr = box(img_w, blk_h, CTR, fill_opacity=0.06)
        img_fr.move_to([x_img + img_w / 2, blk_h / 2, 0])
        cav = self._area(area_w, area_h, color=CTR, fill=S.BG)
        cav.move_to([x_img + 0.2 + area_w / 2, lap_area.get_center()[1], 0])
        cav_lab = mono("/app", CAPTION, INK).next_to(cav, UP, buff=0.1).align_to(cav, LEFT)
        copied_rows = self._rows(copied, cav)
        venv_fr = box(venv_w - 0.1, 0.9, VENV, fill_opacity=0.12)
        venv_fr.move_to([cav.get_right()[0] + 0.2 + (venv_w - 0.1) / 2, cav.get_center()[1], 0])
        venv_lab = mono("/home/app/.venv", CAPTION, VENV).next_to(venv_fr, UP, buff=0.1)
        venv = VGroup(venv_fr, venv_lab)
        venv.frame, venv.label = venv_fr, venv_lab
        img_cap = sans(f"image · {component}", CAPTION, CTR).next_to(img_fr, DOWN, buff=0.12)
        self.image = VGroup(img_fr, cav, cav_lab, copied_rows, img_cap)
        self.image.frame, self.image.cavity, self.image.copied, self.image.caption = img_fr, cav, copied_rows, img_cap
        self.copied = copied_rows
        self.venv = venv
        self.venv_home_pos = venv.get_center()
        self.add(self.laptop, self.image, self.venv)
        # the writable sheet
        self.sheet = self._sheet(img_fr)
        if sheet:
            self.add(self.sheet)
        # the mount (built always; mount() shows it)
        a = lap_area.get_right() + RIGHT * 0.12
        b = cav.get_left() + LEFT * 0.12
        self.route = Line(a, b, color=LOOKUP, stroke_width=5)
        self.route_label = mono('-v "$(pwd):/app"', CAPTION, LOOKUP).next_to(self.route, UP, buff=0.14)
        cov = self._area(area_w, area_h, color=LAPTOP, fill=PANEL, fill_opacity=1).move_to(lap_area)
        cov_rows = self._rows(files, cov)
        self.cover = VGroup(cov, cov_rows)
        self.cover.frame, self.cover.rows = cov, cov_rows
        self.cover_home, self.cover_mounted = lap_area.get_center(), cav.get_center()
        self.parts.update(route=VGroup(self.route, self.route_label), cover=self.cover)
        self.mounted = False
        if mounted:
            self.cover.move_to(self.cover_mounted)
            self.copied.set_opacity(0.3)
            self.add(self.route, self.route_label, self.cover)
            self.mounted = True
        self.move_to(ORIGIN)
        self.files = files

    # -- building blocks
    def _area(self, w, h, color=LAPTOP, fill=None, fill_opacity=0.08):
        return RoundedRectangle(width=w, height=h, corner_radius=0.1, stroke_color=color,
                                stroke_width=2).set_fill(fill or color, fill_opacity if fill is None else 1)

    def _row_pos(self, area, i: int):
        return area.get_corner(UP + LEFT) + np.array([0.18, -0.1 - (i + 0.5) * self.pitch, 0])

    def _rows(self, names, area) -> VGroup:
        rows = VGroup()
        for i, n in enumerate(names):
            name, col = (n, INK) if isinstance(n, str) else n
            r = file_row(name, col)
            if self.key and name == "secrets/":
                r.add(key_glyph(0.2).next_to(r, RIGHT, buff=0.15))
            r.move_to(self._row_pos(area, i), aligned_edge=LEFT)
            rows.add(r)
        return rows

    def _sheet(self, img_fr) -> VGroup:
        w, h = img_fr.width, 0.52
        fr = box(w, h, CTR, dashed=True)
        fr.next_to(img_fr, UP, buff=0.06)
        cap = sans("writable layer", CAPTION, CTR).move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.2)
        vx = self.venv.frame
        shelf = Line([vx.get_left()[0] + 0.1, fr.get_bottom()[1] + 0.1, 0],
                     [vx.get_right()[0] - 0.1, fr.get_bottom()[1] + 0.1, 0], color=VENV, stroke_width=3)
        g = VGroup(fr, cap, shelf)
        g.frame, g.caption, g.shelf = fr, cap, shelf
        return g

    def row(self, name: str, side: str = "laptop"):
        rows = {"laptop": self.laptop.rows, "cover": self.cover.rows, "copied": self.copied}[side]
        for r in rows:
            if r.name == name:
                return r
        raise KeyError(f"{name} not in the {side} rows")

    # -- actions
    def mount(self, scene, run_time: float = 1.8):
        """The PINK route draws, the copied files dim, and a GREY sheet carrying the laptop's
        files slides along the route and covers /app."""
        self.cover.move_to(self.cover_home)
        self.attach(scene, self.route, self.route_label,
                    anims=[Create(self.route), FadeIn(self.route_label)], run_time=run_time * 0.35)
        self.attach(scene, self.cover, anims=[FadeIn(self.cover)], run_time=run_time * 0.15)
        scene.play(self.cover.animate.move_to(self.cover_mounted), self.copied.animate.set_opacity(0.3),
                   run_time=run_time * 0.5)
        self.mounted = True

    def cover_to(self, alpha: float):
        """Animation: the laptop sheet slides to `alpha` along the route (0 laptop, 1 over /app)."""
        p = self.cover_home + alpha * (self.cover_mounted - self.cover_home)
        return self.cover.animate.move_to(p)

    def blink(self, name: str, color: str = TURN):
        """The same file blinks on both sides at once (nothing travels); the route pulses."""
        anims = [Indicate(self.row(name, "laptop"), color=color, scale_factor=1.15)]
        if self.mounted:
            anims += [Indicate(self.row(name, "cover"), color=color, scale_factor=1.15),
                      Indicate(self.route, color=LOOKUP, scale_factor=1.0)]
        return AnimationGroup(*anims)

    def add_file(self, scene, name: str, color: str = INK, run_time: float = 0.6):
        """A new file written under /app: it appears on the laptop and on the sheet at the same
        instant. Returns (laptop row, cover row or None)."""
        i = len(self.laptop.rows)
        if i >= self.capacity:
            raise ValueError(f"Window holds {self.capacity} rows: build it with rows={i + 1}")
        r1 = self._rows([(name, color)], self.laptop.area)[0].move_to(self._row_pos(self.laptop.area, i),
                                                                       aligned_edge=LEFT)
        mobs = [r1]
        r2 = None
        if self.mounted:
            r2 = self._rows([(name, color)], self.cover.frame)[0].move_to(
                self._row_pos(self.cover.frame, i), aligned_edge=LEFT)
            mobs.append(r2)
        scene.play(*[FadeIn(m, scale=1.2) for m in mobs], run_time=run_time)
        for m in mobs:
            scene.remove(m)
        self.laptop.rows.add(r1)
        if r2 is not None:
            self.cover.rows.add(r2)
        if self not in scene.mobjects:
            scene.add(self)
        return r1, r2

    def tmp_page(self, scene, run_time: float = 0.6) -> VGroup:
        """A page written outside /app (say /tmp) lands on the dashed writable sheet."""
        pg = page_token().scale(0.7)
        pg.move_to(self.sheet.frame.get_center() + LEFT * 0.2)
        self.sheet.add(pg)                         # it lives (and dies) with the sheet
        scene.add(self) if self not in scene.mobjects else None
        self.sheet.remove(pg)
        self.attach(scene, pg, anims=[FadeIn(pg, shift=DOWN * 0.4)], run_time=run_time)
        self.remove(pg)
        self.sheet.add(pg)
        return pg

    def fill_shelf(self, scene, n: int = 26, run_time: float = 1.2) -> VGroup:
        """n GREEN package chips drop onto the shelf on the writable sheet (they are part of the
        sheet: evaporate() takes them away)."""
        sh = self.sheet.shelf
        cols = 13
        d = pkg_dots(n, cols=cols)
        d.next_to(sh, UP, buff=0.02)
        if d.height > self.sheet.frame.height - 0.15:
            d.scale_to_fit_height(self.sheet.frame.height - 0.15).next_to(sh, UP, buff=0.02)
        scene.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.3) for c in d], lag_ratio=0.05),
                   run_time=run_time)
        scene.remove(*d)
        self.sheet.add(d)
        self.sheet.chips = d
        return d

    def evaporate(self, scene, run_time: float = 1.0):
        """Exit with --rm: the writable sheet (and whatever is on it) floats up and vanishes."""
        sh = self.sheet
        self.detach(scene, sh, anims=[FadeOut(sh, shift=UP * 0.5)], run_time=run_time)

    def new_sheet(self, scene, run_time: float = 0.6) -> VGroup:
        """A new container from the same image: a fresh, empty writable sheet settles on top."""
        self.sheet = self._sheet(self.image.frame)
        return self.attach(scene, self.sheet, anims=[FadeIn(self.sheet, shift=DOWN * 0.3)],
                           run_time=run_time)

    def venv_to_cavity(self):
        """Animation (ponder 3): the venv box slides into the /app cavity (lecture 2's layout)."""
        return self.venv.animate.move_to(self.image.cavity.get_center() + DOWN * 0.1)

    def venv_home(self):
        return self.venv.animate.move_to(self.venv_home_pos)


# ------------------------------------------------------------------ V5 · who is calling?
class AdcChain(Piece):
    """V5. Left: your laptop's secrets/ folder with the GOLD key. Middle: the container (TEAL)
    with the PINK signpost planted at /app (GOOGLE_APPLICATION_CREDENTIALS=secrets/...), the
    storage.Client() machine and the google.auth box; a PINK window joins /app to the laptop.
    Right: Google Cloud (BLUE) with gate 1 (authentication · who?), gate 2 (IAM padlock,
    authorization · may it?) and the bucket door. ~12.9 x 4.3.

        chain = AdcChain(show=("ctr", "client", "auth", "post"))    # parts to show at first
        self.play(FadeIn(chain)); chain.reveal(self, "laptop", "window")
        chain.ask(self); chain.follow(self); tok = chain.mint(self)
        chain.reveal(self, "google"); chain.request(self, tok); chain.check(self, 1); chain.check(self, 2)
    Parts: laptop, window, ctr, root, post, client, auth, google (cloud box + gates + door).
    .key (the GOLD key in secrets/) .gates[0..1] .door .padlock"""

    ALL = ("laptop", "window", "ctr", "root", "post", "client", "auth", "google")

    def __init__(self, show=ALL, **kw):
        super().__init__(**kw)
        P = self.parts
        # laptop: secrets/ with the key
        lf = box(2.3, 2.2, LAPTOP, fill_opacity=0.05).move_to([-5.45, -0.2, 0])
        lcap = label("your laptop", CAPTION, LAPTOP).next_to(lf, DOWN, buff=0.1)
        sec = file_row("secrets/").move_to(lf.get_center() + UP * 0.45)
        self.key = key_glyph(0.3).next_to(sec, DOWN, buff=0.3)
        kname = mono("mega-pipeline.json", CAPTION, KEY)
        kname.scale_to_fit_width(min(kname.width, 2.15)) if False else None
        self.key_name = mono("mega-…json", CAPTION, KEY).next_to(self.key, DOWN, buff=0.12)
        P["laptop"] = VGroup(lf, lcap, sec, self.key, self.key_name)
        self.secrets = sec
        # container
        cf = box(6.2, 4.0, CTR, fill_opacity=0.05).move_to([-0.95, 0.05, 0])
        ccap = sans("container · transcribe_audio", CAPTION, CTR).next_to(cf, DOWN, buff=0.1)
        P["ctr"] = VGroup(cf, ccap)
        self.ctr_frame = cf
        post = signpost(["GOOGLE_APPLICATION_CREDENTIALS=", "secrets/mega-pipeline.json"], post_h=0.5)
        post.move_to(cf.get_top() + DOWN * (0.3 + post.height / 2)).align_to(cf, LEFT).shift(RIGHT * 0.3)
        P["post"] = post
        root_dot = Dot(post.root(), radius=0.07, color=LOOKUP)
        root_t = mono("/app", CAPTION, LOOKUP).next_to(root_dot, DOWN, buff=0.1)
        P["root"] = VGroup(root_dot, root_t)
        self.root_dot = root_dot
        client_t = mono("storage.Client()", CAPTION, CTR)
        client = VGroup(box(client_t.width + 0.4, 0.66, CTR, fill_opacity=0.15).move_to(client_t), client_t)
        client.move_to(cf.get_corner(DOWN + LEFT) + np.array([0.25 + client.width / 2, 0.6, 0]))
        P["client"] = client
        auth_t = mono("google.auth", CAPTION, INK)
        auth = VGroup(box(auth_t.width + 0.4, 0.66, S.GREY, fill_opacity=0.12).move_to(auth_t), auth_t)
        auth.move_to(cf.get_corner(DOWN + RIGHT) + np.array([-0.25 - auth.width / 2, 0.6, 0]))
        P["auth"] = auth
        self.client, self.auth, self.post = client, auth, post
        # the window (PINK) from /app out to the laptop's secrets folder
        wy = root_dot.get_center()[1]
        win = DashedLine([cf.get_left()[0], wy, 0], [lf.get_right()[0], wy, 0], color=LOOKUP,
                         stroke_width=4, dash_length=0.12)
        P["window"] = win
        self.window = win
        # Google Cloud
        gf = box(3.9, 4.0, CLOUD, fill_opacity=0.05).move_to([4.6, 0.05, 0])
        gic = cloud(0.9).move_to(gf.get_corner(UP + LEFT) + np.array([0.6, -0.4, 0]))
        gt = sans("Google Cloud", CAPTION, CLOUD).next_to(gic, RIGHT, buff=0.15)
        g1 = self._gate(gf.get_left()[0] + 0.85, gf, "authentication", "who is calling?")
        g2 = self._gate(gf.get_left()[0] + 2.55, gf, "authorization", "may it do this?")
        self.padlock = padlock(0.4).move_to(g2.bar.get_center() + UP * 0.1)
        g2.add(self.padlock)
        door = VGroup(Rectangle(width=0.36, height=1.0, stroke_color=CLOUD, stroke_width=3).set_fill(CLOUD, 0.3))
        door.move_to([gf.get_right()[0] - 0.35, g1.bar.get_center()[1], 0])
        dl = label("bucket", CAPTION, CLOUD).next_to(door, UP, buff=0.1)
        self.door = VGroup(door, dl)
        self.gates = [g1, g2]
        P["google"] = VGroup(gf, gic, gt, g1, g2, self.door)
        self.google_frame = gf
        for n in self.ALL:
            if n in show:
                self.add(P[n])

    def _gate(self, x, gf, word, question):
        bar = Line([x, gf.get_center()[1] + 0.75, 0], [x, gf.get_center()[1] - 0.45, 0], color=CLOUD,
                   stroke_width=6)
        w = label(word, CAPTION, CLOUD)
        q = label(question, CAPTION, S.GREY)
        txt = VGroup(w, q).arrange(DOWN, buff=0.06).next_to(bar, DOWN, buff=0.15)
        g = VGroup(bar, txt)
        g.bar, g.word, g.question = bar, w, q
        return g

    def ask(self, scene, text: str = "who am I?", run_time: float = 0.8) -> VGroup:
        """Arrow client -> google.auth with the question above it."""
        a = Arrow(self.client.get_right(), self.auth.get_left(), buff=0.1, stroke_width=3, color=S.GREY,
                  max_tip_length_to_length_ratio=0.15)
        q = label(text, CAPTION, INK).next_to(a, UP, buff=0.08)
        g = VGroup(a, q)
        self.attach(scene, g, anims=[GrowArrow(a), FadeIn(q)], run_time=run_time)
        self.asked = g
        return g

    def follow(self, scene, run_time: float = 2.0, found: bool = True) -> VMobject:
        """google.auth follows the signpost: a PINK path from google.auth to the board, down the
        post to /app, out through the window to secrets/; the key glows if found. Returns path."""
        pts = [self.auth.get_top(), self.post.board.get_right() + DOWN * 0.05,
               self.root_dot.get_center(), self.window.get_end(), self.secrets.get_right() + RIGHT * 0.05]
        path = VMobject(stroke_color=LOOKUP, stroke_width=3).set_points_as_corners(pts)
        dot = Dot(pts[0], radius=0.08, color=LOOKUP)
        scene.add(dot)
        scene.play(Create(path), MoveAlongPath(dot, path), run_time=run_time, rate_func=smooth)
        scene.remove(dot)
        self.add(path)
        if found:
            scene.play(Indicate(self.key, color=KEY, scale_factor=1.4), run_time=0.6)
        self.path = path
        return path

    def mint(self, scene, run_time: float = 0.7) -> VGroup:
        """The key stamps out a GOLD token tag (short-lived) next to google.auth. Returns it."""
        tok = token_tag().next_to(self.auth, UP, buff=0.2)
        src = self.key.copy()
        scene.play(Transform(src, tok), run_time=run_time)
        scene.remove(src)
        self.add(tok)
        self.token = tok
        return tok

    def request(self, scene, tok=None, run_time: float = 1.0) -> Arrow:
        """A request arrow from the container to gate 1; the token rides on it. Returns arrow."""
        g1 = self.gates[0].bar
        a = Arrow(self.auth.get_right() + RIGHT * 0.05, [g1.get_center()[0] - 0.1, self.auth.get_center()[1], 0],
                  buff=0.05, stroke_width=4, color=INK, max_tip_length_to_length_ratio=0.12)
        anims = [GrowArrow(a)]
        if tok is not None:
            anims.append(tok.animate.next_to(a, UP, buff=0.08))
        scene.play(*anims, run_time=run_time)
        self.add(a)
        self.arrow = a
        return a

    def check(self, scene, i: int, run_time: float = 0.8):
        """Gate i (1 or 2) passes: GREEN. Gate 2 opens its padlock and the bucket door."""
        from explainer.devops import check_mark
        g = self.gates[i - 1]
        ck = check_mark(0.3, VENV).next_to(g.bar, UP, buff=0.1)
        anims = [g.bar.animate.set_color(VENV), FadeIn(ck)]
        if i == 2:
            anims += [self.padlock.shackle.animate.shift(UP * 0.12),
                      self.door[0].animate.stretch(0.25, 0, about_edge=RIGHT)]
        self.attach(scene, ck, anims=anims, run_time=run_time)
        return ck

    def fail(self, scene, run_time: float = 0.8):
        """The key isn't there: the key fades, a RED cross at the end of the path."""
        from explainer.devops import cross_mark
        x = cross_mark(0.35, ERR).next_to(self.secrets, DOWN, buff=0.25)
        self.detach(scene, self.key, self.key_name, run_time=run_time * 0.5)
        self.attach(scene, x, run_time=run_time * 0.5)
        return x


# ------------------------------------------------------------------ V6 · two filters, two boxes
class TwoFilters(Piece):
    """V6. Left: the GREY component folder with the GOLD key in secrets/. Right, top: Git's
    history book; right, bottom: the image as a TEAL shipping box, the Docker Hub shelf behind
    it. Two sieves wait off-screen above (lower() brings each over its box). ~12.4 x 5.

        v6 = TwoFilters(); self.play(FadeIn(v6))
        v6.lower(self, "git"); v6.pour(self, "git")          # the key is caught over the book
        k = v6.pour(self, "image")                           # no sieve: the key lands in the box
        v6.to_hub(self)                                      # slides toward the shelf
        v6.lower(self, "image"); v6.pour(self, "image")      # .dockerignore catches it
    .folder (.rows) .key .book .box .hub .sieves {"git", "image"}"""

    def __init__(self, files=("cli.py", "Dockerfile", "pyproject.toml", "secrets/"), **kw):
        super().__init__(**kw)
        fr = box(3.6, 2.6, LAPTOP, fill_opacity=0.05).move_to([-4.6, 0, 0])
        t = mono("transcribe_audio/", CAPTION, LAPTOP).move_to(fr.get_corner(UP + LEFT) + np.array([0.15, -0.27, 0]),
                                                               aligned_edge=LEFT)
        rows = VGroup(*[file_row(f) for f in files]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        rows.next_to(t, DOWN, buff=0.2, aligned_edge=LEFT).shift(RIGHT * 0.1)
        sec = [r for r in rows if r.name == "secrets/"][0]
        self.key = key_glyph(0.24).next_to(sec, RIGHT, buff=0.15)
        self.folder = VGroup(fr, t, rows, self.key)
        self.folder.frame, self.folder.rows = fr, rows
        self.book = book_glyph().move_to([3.2, 1.75, 0])
        self.hub = hub_shelf().move_to([5.2, -1.3, 0])
        self.box = ship_box().move_to([2.3, -1.75, 0])
        self.add(self.folder, self.book, self.hub, self.box)
        self.sieves = {"git": sieve(".gitignore").move_to(self.book.get_top() + UP * 0.45),
                       "image": sieve(".dockerignore").move_to(self.box.front.get_top() + UP * 0.6)}
        self.lowered = set()

    def lower(self, scene, which: str, run_time: float = 0.7):
        sv = self.sieves[which]
        sv.shift(UP * 0.6)
        self.attach(scene, sv, anims=[FadeIn(sv), sv.animate.shift(DOWN * 0.6)], run_time=run_time)
        self.lowered.add(which)
        return sv

    def pour(self, scene, which: str, run_time: float = 1.6):
        """Copies of the folder's files fly into the book ("git") or the box ("image"). With that
        sieve lowered, the key copy stays on the sieve; without, it lands inside (in the box it
        gets a RED outline). Returns the key copy (on screen, part of the piece)."""
        target = self.book if which == "git" else self.box.front
        files = VGroup(*[r.glyph.copy() for r in self.folder.rows])
        k = self.key.copy()
        dest = target.get_center()
        anims = [LaggedStart(*[f.animate.move_to(dest).set_opacity(0) for f in files], lag_ratio=0.1)]
        if which in self.lowered:
            anims.append(k.animate.move_to(self.sieves[which].bowl.get_center() + UP * 0.12))
        else:
            anims.append(k.animate.move_to(dest + DOWN * 0.05))
        scene.add(files, k)
        scene.play(*anims, run_time=run_time)
        scene.remove(files)
        scene.remove(k)
        self.add(k)
        if which == "image" and which not in self.lowered:
            ring = Circle(radius=0.28, stroke_color=ERR, stroke_width=3).move_to(k)
            self.attach(scene, ring, anims=[Create(ring)], run_time=0.4)
            k.ring = ring
        return k

    def to_hub(self, scene, frac: float = 0.55, run_time: float = 1.0):
        """The box slides toward the Docker Hub shelf (and stops part way)."""
        d = (self.hub.board.get_center() + UP * 0.45 - self.box.front.get_center()) * frac
        scene.play(self.box.animate.shift(d), run_time=run_time)


# ------------------------------------------------------------------ V7 · requires-python interval
class VersionLine(Piece):
    """Python 3.x versions on a number line (positions by MINOR version: 12 means 3.12), with the
    `>= 3.lo` interval GREEN, running off the right end. ~11 x 1.6.

        vl = VersionLine(10, 16, lo=11)
        d = vl.dot(11, "laptop · 3.11.2", LAPTOP)           # dot + label above the line
        self.play(*vl.move_lo(13))                          # the interval's start slides to 3.13
        arr = vl.download_arrow(15, "3.15.0 · uv-managed · 35.9 MiB")
    .axis .ticks .band .band_label .point(minor)"""

    def __init__(self, first: int = 10, last: int = 16, lo: int = 11, width: float = 11.0,
                 size: float = 22, **kw):
        super().__init__(**kw)
        self.first, self.last, self.lo, self.line_w, self.size = first, last, lo, width, size
        self.axis = Line(LEFT * width / 2, RIGHT * width / 2, color=S.GREY, stroke_width=3)
        self.ticks = VGroup()
        for m in range(first, last + 1):
            x = self._x(m)
            self.ticks.add(VGroup(Line([x, -0.12, 0], [x, 0.12, 0], color=S.GREY, stroke_width=2),
                                  mono(f"3.{m}", size, S.GREY).move_to([x, -0.45, 0])))
        self.band = self._band(lo)
        self.band_label = self._band_label(lo)
        self.add(self.band, self.axis, self.ticks, self.band_label)

    def _x(self, minor: float) -> float:
        return -self.line_w / 2 + (minor - self.first + 0.5) / (self.last - self.first + 1) * self.line_w

    def _band(self, lo):
        left = self.axis.get_start()[0] + self._x(lo) + self.line_w / 2
        right = self.axis.get_end()[0] + 0.25
        b = Rectangle(width=right - left, height=0.3, stroke_width=0).set_fill(VENV, 0.3)
        return b.move_to([(left + right) / 2, self.axis.get_center()[1], 0])

    def _band_label(self, lo):
        t = mono(f'requires-python = ">=3.{lo}"', self.size, VENV)
        b = self._band(lo)
        return t.next_to(b, UP, buff=0.3).align_to(b, LEFT)

    def point(self, minor: float, dy: float = 0.0):
        """A point on the (possibly moved) axis above minor version `minor`."""
        left = self.axis.get_start()
        return left + np.array([self._x(minor) + self.line_w / 2, dy, 0])

    def dot(self, minor: float, text: str, color: str, above: bool = True, size: float = 22) -> VGroup:
        d = Dot(self.point(minor), radius=0.11, color=color)
        t = mono(text, size, color)
        t.next_to(d, UP if above else DOWN, buff=0.3 if above else 0.75)
        g = VGroup(d, t)
        g.dot, g.text = d, t
        return g

    def move_lo(self, lo: int) -> list:
        """Animations: the interval's start (and its label) moves to 3.lo."""
        self.lo = lo
        return [Transform(self.band, self._band(lo)), Transform(self.band_label, self._band_label(lo))]

    def download_arrow(self, minor: float, text: str | None = None, color: str = TOOL) -> VGroup:
        """A PURPLE arrow dropping onto 3.minor from above, with an optional label at its top."""
        p = self.point(minor, 0.12)
        a = Arrow(p + UP * 1.3, p, buff=0, stroke_width=4, color=color, max_tip_length_to_length_ratio=0.2)
        g = VGroup(a)
        if text:
            g.add(mono(text, CAPTION, color).next_to(a, UP, buff=0.1))
        g.arrow = a
        return g


# ------------------------------------------------------------------ V8 · ticket stubs
class ApiCall(Piece):
    """V8. A container (TEAL) on the left, a BLUE API cloud on the right, a request arrow
    between them, and optionally bucket drawers along the bottom. ~12.4 x 4.

        api = ApiCall("Speech-to-Text", "A · transcribe_audio")
        api.send(self, page_token())            # the payload rides to the cloud
        stub = api.stub(self)                    # a ticket stub comes back at once
        api.ring(self, stub, "up to 90 s")       # its ring fills
        api.reply(self, page_token())            # the result comes back to the container
        api2 = ApiCall("Text-to-Speech · long audio", "C · synthesis_audio_en", drawers=["text_audios/group-01/"])
        api2.deliver(self, wave_token(), 0)      # the cloud writes straight into a drawer
    .ctr (.frame .title .inside) .api (.shape .title) .arrow .drawers[i]"""

    def __init__(self, api: str = "Speech-to-Text", ctr: str = "A · transcribe_audio", drawers=None,
                 **kw):
        super().__init__(**kw)
        cf = box(3.6, 2.0, CTR, fill_opacity=0.06).move_to([-4.3, 0.6, 0])
        ct = sans(ctr, CAPTION, CTR).next_to(cf, UP, buff=0.1)
        self.ctr = VGroup(cf, ct)
        self.ctr.frame, self.ctr.title, self.ctr.inside = cf, ct, cf.get_center()
        cl = cloud(3.2).move_to([4.2, 0.6, 0])
        at = sans(api, CAPTION, CLOUD).next_to(cl, UP, buff=0.12)
        self.api = VGroup(cl, at)
        self.api.shape, self.api.title = cl, at
        self.arrow = Line(cf.get_right() + RIGHT * 0.1, cl.get_left() + LEFT * 0.1, color=S.GREY,
                          stroke_width=2.5)
        self.add(self.ctr, self.api, self.arrow)
        self.drawers = VGroup()
        for i, name in enumerate(drawers or []):
            fr = RoundedRectangle(width=3.4, height=0.8, corner_radius=0.08, stroke_color=CLOUD,
                                  stroke_width=2.5).set_fill(CLOUD, 0.1)
            t = mono(name, CAPTION, INK).move_to(fr.get_top() + DOWN * 0.22)
            d = VGroup(fr, t)
            d.frame, d.text = fr, t
            self.drawers.add(d)
        if len(self.drawers):
            self.drawers.arrange(RIGHT, buff=0.3).move_to([4.2 - (len(self.drawers) - 1) * 1.85, -2.5, 0])
            self.add(self.drawers)

    def send(self, scene, payload, run_time: float = 1.2):
        """The payload starts in the container and rides the arrow into the cloud (stays there,
        part of the scene). Returns it."""
        payload.move_to(self.ctr.inside)
        scene.play(FadeIn(payload), run_time=0.3)
        scene.play(payload.animate.move_to(self.api.shape.get_center()), run_time=run_time)
        return payload

    def stub(self, scene, text: str | None = "operation", run_time: float = 0.8) -> VGroup:
        """A ticket stub comes back from the cloud into the container at once. Returns it."""
        s = stub_glyph(text).move_to(self.api.shape.get_center())
        scene.play(FadeIn(s, scale=0.6), run_time=0.3)
        scene.play(s.animate.move_to(self.ctr.inside), run_time=run_time)
        return s

    def ring(self, scene, stub, text: str = "up to 90 s", run_time: float = 2.0, color: str = CTR) -> VGroup:
        """A ring around the stub fills over run_time (the wait). Returns ring + label."""
        r = max(stub.width, stub.height) / 2 + 0.18
        arc = Arc(radius=r, start_angle=PI / 2, angle=-TAU, stroke_color=color, stroke_width=4)
        arc.move_to(stub)
        t = label(text, CAPTION, color).next_to(arc, DOWN, buff=0.1)
        scene.play(FadeIn(t), run_time=0.3)
        scene.play(Create(arc), run_time=run_time, rate_func=linear)
        return VGroup(arc, t)

    def reply(self, scene, mob, run_time: float = 1.0):
        """`mob` appears at the cloud and travels back into the container. Returns it."""
        mob.move_to(self.api.shape.get_center())
        scene.play(FadeIn(mob), run_time=0.3)
        scene.play(mob.animate.move_to(self.ctr.inside + DOWN * 0.2), run_time=run_time)
        return mob

    def deliver(self, scene, mob, i: int = 0, run_time: float = 1.2):
        """`mob` leaves the cloud and drops straight into drawer i (never through the container)."""
        mob.move_to(self.api.shape.get_center())
        scene.play(FadeIn(mob), run_time=0.3)
        scene.play(mob.animate.move_to(self.drawers[i].frame.get_bottom() + UP * 0.25), run_time=run_time)
        return mob


# ------------------------------------------------------------------ "with your key, look for"
class LookFor(Piece):
    """The GREY caption card for Google calls that couldn't be recorded: a title and one short
    line per item, each with the cli.py line it cites (GREY, right); an optional RED-bordered
    "if it fails" line. Never terminal-styled. Items write in one at a time.

        lf = LookFor([("download", "line 30"), ("one object name per recording", "line 41")],
                     fail="if it fails: ...").to_edge(UP)
        self.play(FadeIn(lf)); lf.reveal(self, 0); lf.reveal(self, 1); lf.reveal_fail(self)
    .rows[i] (.text .cite) .fail_row .frame .title"""

    def __init__(self, items, fail: str | None = None, title: str = "with your key, look for",
                 width: float | None = None, **kw):
        super().__init__(**kw)
        rows = VGroup()
        for text, cite in items:
            t = label(text, CAPTION, INK)
            c = label(cite, CAPTION, S.GREY) if cite else VGroup()
            r = VGroup(t, c)
            r.text, r.cite = t, c
            rows.add(r)
        tw = max([r.text.width for r in rows] + [1.0])
        cw = max([r.cite.width for r in rows] + [0.0])
        inner = tw + cw + 0.6
        self.fail_row = None
        if fail:
            ft = label(fail, CAPTION, INK)
            ff = box(ft.width + 0.3, ft.height + 0.2, ERR, fill_opacity=0.08, radius=0.08).move_to(ft)
            self.fail_row = VGroup(ff, ft)
            inner = max(inner, self.fail_row.width)
        w = max(width or 0, inner + 0.5)
        self.title = label(title, CAPTION, S.GREY)
        n = len(rows) + (1 if fail else 0)
        pitch = 0.44
        h = 0.55 + n * pitch + 0.2 + (0.1 if fail else 0)
        self.frame = box(w, h, S.GREY, fill=S.BG, fill_opacity=0.92, radius=0.12)
        self.title.move_to(self.frame.get_corner(UP + LEFT) + np.array([0.25, -0.3, 0]), aligned_edge=LEFT)
        for i, r in enumerate(rows):
            y = self.frame.get_top()[1] - 0.72 - i * pitch
            r.text.move_to([self.frame.get_left()[0] + 0.25, y, 0], aligned_edge=LEFT)
            if r.cite:
                r.cite.move_to([self.frame.get_right()[0] - 0.25, y, 0], aligned_edge=RIGHT)
        if self.fail_row is not None:
            y = self.frame.get_top()[1] - 0.72 - len(rows) * pitch - 0.08
            self.fail_row.move_to([self.frame.get_left()[0] + 0.25, y, 0], aligned_edge=LEFT)
        self.rows = rows
        self.add(self.frame, self.title)

    def reveal(self, scene, i: int, run_time: float = 0.5):
        return self.attach(scene, self.rows[i], anims=[FadeIn(self.rows[i], shift=RIGHT * 0.15)],
                           run_time=run_time)

    def reveal_fail(self, scene, run_time: float = 0.5):
        return self.attach(scene, self.fail_row, anims=[FadeIn(self.fail_row)], run_time=run_time)


__all__ = [n for n in dir() if not n.startswith("_") and n not in {"annotations", "re", "np", "yaml",
                                                                    "Path"}]
