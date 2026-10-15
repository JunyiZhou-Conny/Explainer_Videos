"""Shared look for AC215 L3 (Containers II: five containers, one bucket): paths, narration, the
semantic colours of BRIEF.md, loaders for the real captures in assets/, terminal and tracker
helpers, and the video's recurring pictures (V1-V8 of BRIEF.md). Tested on screen by
build/common_test.py (python -m explainer.check / explainer.preview on it: clean).

Notes for scene authors
=======================

    from common import *      # or name what you use; every scene: SAY = NARRATION["Snn"];
                              # assert len(SAY) == n; one `with self.voiceover(SAY[i])` per line
Everything below draws text at 20-22 pt. Never .scale() a group that holds text below 1.0: use
Piece.rescale(k) (shapes shrink, text keeps its size). Frame budget: the tracker band is
y 2.92..3.5 (x -6.5..-0.1 at most); a 3-row strip's top is STRIP_TOP = -1.44, so a picture
above a strip has y -1.3..2.8 (4.1 tall); keep x in [-6.6, 6.6] (to_edge buffs >= 0.5).

Data and sources
    NARRATION["S01"] ...      SAY lines from script.md (15 scenes, all loaded)
    TITLES[cls], SPEC         scene titles / video.yaml
    capture(name, folder="laptop") -> Capture        assets/terminal/<folder>/<name>.txt
        folders: "laptop" (everything typed on the laptop), "transcribe_audio", "generate_text",
        "synthesis_audio_en", "translate_text", "synthesis_audio" (typed inside that container),
        "expected" (README --help blocks for C, D, E; line 1 is a '#' header, never printed).
        "files" holds the student's Dockerfiles / pyproject.toml: use file_panel(), asset_lines().
        .cmd (the `$` line without "$ ") .lines (output) .exit .first (file line of .lines[0])
        .at(9, 23, "…", (148, 149))  output lines BY FILE LINE NUMBER (the script's TERM notation:
                                     ints, inclusive (a, b) ranges, a literal "…")
        .line(n)  .typed(n) (the command on a prompt line, e.g. 01-docker-run-tty.txt line 2)
        .pick((1, 3), (-2, -1))      L1-compatible: body index = file line - 1 (prefer .at)
    source_text(path)  excerpt(path, a, b, cut_comments=False)   tutorial files in assets/source
        cut_comment(line): a line > 70 chars loses its trailing comment, shown as "# …"
    asset_lines(rel, a, b)        raw lines a..b of a file under assets/terminal
    live_split(row) -> (text, time)   a BuildKit live-view row cut at 65 + its time field
    history_row(line)             a `docker history` row sliced to CREATED BY + SIZE (line[32:90])

Colours (BRIEF.md, binding)
    LAPTOP GREY · CLOUD BLUE · CTR (= IMAGE) TEAL · SYSTEM ORANGE · VENV GREEN · TOOL (= UV)
    PURPLE · ERR RED · TURN YELLOW · COST (= KEY) GOLD · LOOKUP PINK · INK white · DIMMED GREY
Running example
    P_HOME "student@laptop:~$"  P_REPO ".../mega-pipeline$"  p_comp(c), P_A (component folders)
    P_CTR "app@5b4d4981ec25:/app$"  GROUP "group-01"  COMPONENTS (A-E folders)  LETTERS "ABCDE"
    PREFIXES (6 drawers, pipeline order)  README_PREFIXES (README.md:74-80 order, 7)  BONUS_PREFIX
    DRAWER_KIND (token per drawer)  READS / WRITES (drawer index per box)  OUT_KIND
Layout constants: BOTTOM -3.5 (terminal bottom edge), TRACK_LEFT/TRACK_TOP, TERM_W 12.6, TERM_PT
22, STRIP_TOP (strip_top(rows) for other heights: 10 rows -> 1.38, 12 rows -> 2.19).

README tracker (top-left, YELLOW)
    tracker(key, step=None)              keys R A B C D E H X (SECTIONS: 2, 13, 13, 12, 13, 12, 3, 3)
    self.play(tr.goto(k))                next step;  caption_extra(tr, on) -> Transform " · extra"
    tr = switch_section(self, tr, "B", 1)   the old tracker lifts away, the new one drops in

Terminal helpers (Terminal from explainer.devops: .type .print .run .clear .find .last)
    term(prompt=P_A, rows=12, component=None)  12.6 wide, 22 pt, 65 chars a row, bottom at BOTTOM;
                        title "laptop", or component="…": "container · …", TEAL frame, P_CTR prompt
    enter_container(t, component) / leave_container(t, prompt=P_A) -> list of animations
    resize(scene, t, rows, keep=None)    grow/shrink, bottom fixed, keeps the last lines (or the
                                         listed line mobjects)
    bare_prompt(scene, t) / type_cmd(scene, t, cmd)   prompt with nothing typed / type after it
    beside(mob, t, line)   positions a tag right after a typed line's text (its last row if
                           folded), or at the row's right end if it wouldn't fit
    pin(scene, line, mob, anim=None) / unpin(scene, line, mob)   show a tag/underline AS PART of
                           the line, so it scrolls and fades with it:
                           ln = t.type(self, cmd); pin(self, ln, beside(your_turn(), t, ln))
                           u = under(ln, ERR); pin(self, ln, u, anim=Create(u))
    under(mob, color=TURN) / strike(mob)  underline / strike-through Line
    time_tag(time) + place_time(tag, t, line)   GREY live-view time tag at a row's right end

Panels and cards
    src_panel(path, a, b, cut_comments=False, focus=None, size=22, width=None, shown_path=None,
              suffix=None)   code_panel from assets/source, header "path · lines a–b" (+ " · comment
                             cut" when a comment was cut, + " · suffix")
    file_panel(rel, a, b, path)   the same for assets/terminal/<rel>, e.g.
                  file_panel("files/transcribe_audio.Dockerfile", 1, 3, "transcribe_audio/Dockerfile")
    log_panel(lines, header, width=12.6)   plain mono rows on a dark panel (full logs, docker
                  history); .rows[i] are mono_lines (substring() colours a part)
    readme_chip(where, phrase)   one-line README chip, ~0.45 tall, <= 9 wide (raises if wider)
    readme_card(where, lines, width=None)   multi-line GREY README card
    editor_inset(panel, title="VS Code · on your laptop")   a GREY editor window around a panel
    cmd_chip(cmd, note=None)     a command shown, not typed (mono chip + GREY note)
    LookFor(items, fail=None)    "with your key, look for" card: items (text, "line 30"); frame
                  built for all, ~0.75 + 0.44 per row tall; .write_item(scene, i), .write_fail(scene)
Tags (22 pt, keep their size in rescale): your_turn() extra_tag() illustration_tag(note=None)
    expected_tag() recorded_tag(s) nokey_tag() erratum_tag() cost_tag(s) standin_tag()
    preview_tag() optional_tag() build_badge(k, words=True) (TEAL "build step k")
    stamp(text, color=ERR) (rotated outline) cached_stamp() time_tag(t) token_tag() (GOLD, clock)
Small text: sans(s, size=20, color) (CMU Sans), two_lines(name) (split after the first "_")

Glyphs (no text unless named; sizes w x h)
    key_glyph(h=0.3, name=None) GOLD key (name="mega-pipeline.json": 3.7 x 0.3) · wave_token()
    page_token(long=False, fr=False) · token(kind) kind in wave|page|long|fr · signpost(lines)
    PINK board on a post (2 lines: 5.8 x 1.4; .board .text .post .foot .root()) · clock_glyph()
    padlock() (.body .shackle) · stub_glyph(text) ticket stub 1.6 x 0.56 · parcel_glyph() ·
    builder_box() PURPLE · sieve(name) 3.5 x 0.3 (.bowl .name) · book_glyph() 1.6 x 1.35 ·
    ship_box() TEAL 2.0 x 1.7 (.front) · hub_shelf() 2.2 x 1.3 (.board) · pkg_dots(n, cols)
    GREEN package chips · file_row(name) (folder glyph when name ends in "/"; .glyph .text
    .name) · ghost_file(name) dashed

Set pieces: Piece = VGroup + named parts
    A part not shown yet is a member at opacity 0: it moves and scales with the piece, and the
    piece's size never jumps. piece.reveal(scene, *names, anim=FadeIn) / piece.hide(scene, *names).
    piece.attach(scene, *mobs, anims=None, into=None): play (FadeIn by default), then the mobs
    become members (they move with the piece); piece.detach(scene, *mobs) the reverse (FadeOut).
    self.play(piece.dim_to(0.3)) / self.play(piece.undim()): never piece.set_opacity (it would
    show hidden parts), never FadeOut a member (it splits the piece). rescale(k): via
    self.play(piece.animate.rescale(k).to_edge(...)); don't combine it in one play with another
    animation of the same members.
    V1 Relay(width=12.4, labels=True, edges=False, bonus=True)   12.6 x 4.7. Five TEAL boxes over
       six BLUE drawers (+ dashed bonus drawer). Parts "letters", "names", "drawer_labels",
       "icons", "edges", "bonus", "bonus_tag". .boxes[j] .drawers[i] .read_edges[j]
       .write_edges[j] .slot(i) .center_of(j) .token_at(i, kind) -> token (not added);
       relay.run(scene, [(tok, j), ...]) -> new tokens (scene-owned): each rises into box j,
       becomes OUT_KIND[j], drops into WRITES[j]; routes play together (the C/D split).
       .center_letters() -> anims (letters to box centres when names stay hidden). Small relay:
       Relay(width=8, labels=False) + reveal("letters") + center_letters(); labels need width
       >= 11.6. Too tall for a strip: use it without a terminal, or hidden labels + rescale.
       SubDrawers(prefix, groups) 10.4 x 1.2 (tag it illustration): .drawers[i] .default
         .slot(i) .flash(i, ERR) -> animation
       Leaderboard(groups, stages) 11.1 x 1.9 (illustration): .light(r, c) -> animation
    V2 LayerStack(slab_w=3.6)   floor + slabs bottom-up, 4.1 x 2.0 with the five SLABS ("base",
       "apt", "workdir", "copy", "sync"; STEP_OF -> build step). Place it by its floor:
       st.move_to([x, -3.45, 0], aligned_edge=DOWN). st.drop(scene, name, src=None) -> slab
       (.box .label .h); st.grow(name, h, label_top=False) -> anims (above moves too);
       positioned helpers to st.attach: .badge(name) [left] .stamp(name) [right]
       .size_label(name, "842MB", after=stamp) .top_label(text) .brace(text, note, side)
       .chips(name, 26) (grow(name, 0.8, label_top=True) first) .files("copy", key=True).
       Needs ~0.6 free left, ~2.6 right (stamp + size).
       ConfigCard(width=8.4, rows=4)   8.4 x 2.2, lecture 2's TEAL card: lines flow in rows;
         card.write(scene, text, color, key, src=None) -> line; self.play(card.restyle(key,
         text, color)) reflows; ValueError when full
    V3+V4 Window(files, rows=None, key=False, mounted=False)   12.6 x 3.5 for 4 rows (+0.4 a
       row): laptop folder | PINK -v route | image (/app cavity, GREEN /home/app/.venv) + dashed
       writable sheet with a GREEN shelf. Fits above a strip: win.move_to([0, 0.75, 0]). Don't
       rescale. .mount(scene) .blink(name) -> anim .add_file(scene, name, color) .fill_shelf(scene,
       26) .tmp_page(scene) .evaporate(scene) .new_sheet(scene) .cover_to(a) / .venv_to_cavity()
       / .venv_home() -> anims; .row(name, "laptop"|"cover"|"copied"). Parts "route",
       "route_label", "cover", "sheet".
    V5 AdcChain(show=ALL)   13.1 x 3.9: laptop (secrets/, GOLD key mega-pipeline.json) | dashed
       PINK window | container (signpost at /app, storage.Client(), google.auth) | Google Cloud
       (gate 1 authentication, gate 2 IAM authorization, bucket door). chain.move_to([0, 0.75,
       0]) above a strip; don't rescale. Parts laptop window ctr post root client auth google
       (+ nested "secrets", "key"). .ask(scene) .follow(scene) / .unfollow(scene) .mint(scene) ->
       token .request(scene, token) .check(scene, 1|2) .fail(scene) / .unfail(scene)
       .reroot(scene, "/tmp") / .reroot(scene, None) .reaim(scene, "mega-pipeline/") /
       .reaim(scene, None)
    V6 TwoFilters()   12.6 x 4.8: folder with the key | Git book (top) | image box + Docker Hub
       shelf (bottom). .lower(scene, "git"|"image") .pour(scene, "git"|"image") -> key copy (it
       rides with its book/box/sieve) .to_hub(scene) .warn(scene, "would publish the key")
       .empty_box(scene). .crate is the box (.front), .sieves {"git", "image"}.
    V7 VersionLine(10, 16, lo=11)   11 wide axis; ~3.3 tall with dot labels and an arrow.
       .dot(minor, text, color, above=True) -> dot + label (positioned; minor may be 12.15)
       .move_lo(lo) -> anims .download_arrow(minor, text) -> PURPLE arrow (positioned)
    V8 ApiCall(api, ctr, drawers=None)   11.9 x 2.4 (4.2 with drawers): container | BLUE API
       cloud. .send(scene, payload) .stub(scene) -> stub .ring(scene, stub, "up to 90 s") ->
       ring .reply(scene, mob) .deliver(scene, mob, i); payloads/stubs/rings are scene-owned.

Capture folder names (assets/terminal): laptop, transcribe_audio, generate_text,
synthesis_audio_en, translate_text, synthesis_audio, expected, files.
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
    if i < 0:
        return line
    code = line[:i]
    return code.rstrip() + "  # …" if code.strip() else code + "# …"


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


def _row_of(line):
    """The row of a typed line that a tag belongs to: the line itself, or the last row of a
    folded command (Terminal.type returns a VGroup with .rows then)."""
    return line.rows[-1] if hasattr(line, "rows") else line


def beside(mob, t: Terminal, line, buff: float = 0.3):
    """Position `mob` (your_turn(), extra_tag(), a check mark ...) right after the text of terminal
    line `line` (its last row when folded), centred on that row; if it would cross the frame's
    right edge it sits at the right end of the row instead. Returns mob (not added)."""
    row = _row_of(line)
    ref = row.glyphs if len(getattr(row, "glyphs", [])) else row.strut
    mob.next_to(ref, RIGHT, buff=buff)
    mob.set_y(row.strut.get_center()[1])
    if mob.get_right()[0] > t.box.get_right()[0] - 0.12:
        mob.align_to(t.box, RIGHT).shift(LEFT * 0.12)
    return mob


def pin(scene, line, mob, run_time: float = 0.4, anim=None):
    """Show `mob` (already positioned, e.g. with beside()) and make it part of the terminal line
    (its last row when folded), so it scrolls and fades with it."""
    row = _row_of(line)
    scene.play(anim or FadeIn(mob, shift=LEFT * 0.1), run_time=run_time)
    scene.remove(mob)
    row.add(mob)
    scene.add(row)
    return mob


def unpin(scene, line, mob, run_time: float = 0.3):
    row = _row_of(line)
    if mob in row.submobjects:
        row.remove(mob)
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
def _save_op(m, attr: str = "_hop"):
    """Remember the fill/stroke opacity of every member of m (attr "_hop" for hide/reveal,
    "_dop" for dim/undim)."""
    for f in m.get_family():
        if isinstance(f, VMobject):
            setattr(f, attr, (f.get_fill_opacity(), f.get_stroke_opacity()))


def _set_op(m, k: float | None = None, attr: str = "_hop"):
    """Opacity of every member: k * saved (k=None: back to the saved opacities)."""
    for f in m.get_family():
        op = getattr(f, attr, None)
        if isinstance(f, VMobject) and op is not None:
            a = 1.0 if k is None else k
            f.set_fill(opacity=op[0] * a, family=False)
            f.set_stroke(opacity=op[1] * a, family=False)


def _drop_groups(scene, anims):
    """Remove the wrapper group an AnimationGroup / LaggedStart adds to the scene (it would keep
    its members on screen after they join a piece)."""
    for a in anims:
        if isinstance(a, AnimationGroup) and a.group in scene.mobjects:
            scene.remove(a.group)


class Piece(VGroup):
    """A set piece: a VGroup with named parts (self.parts) and helpers that keep the scene clean.

    A part that is not shown yet is still a member, at opacity 0, so it moves and scales with the
    piece and the piece's size never jumps; reveal() fades it in, hide() fades it back to 0.
    Never FadeOut a part (a FadeOut removes it from the scene and splits the piece); never
    set_opacity on the whole piece (it would show hidden parts): use dim_to()/undim()."""

    def __init__(self, **kw):
        super().__init__(**kw)
        self.parts: dict[str, object] = {}

    # -- parts
    def part(self, name: str, mob, shown: bool = True):
        """Register and add a named part (invisible until reveal() when shown=False)."""
        self.parts[name] = mob
        if not shown:
            _save_op(mob)
            _set_op(mob, 0)
        mob.hidden = not shown
        self.add(mob)
        return mob

    def reveal(self, scene, *names, run_time: float = 0.6, anim=None, extra=()):
        """Fade in (or anim(mob), e.g. Create, Write) the named hidden parts. Returns the part
        (or a list of them)."""
        mobs = [self.parts[n] for n in names]
        for m in mobs:
            if getattr(m, "hidden", False):
                _set_op(m)
            self._flag(m, False)
        self._ensure(scene)
        scene.play(*[(anim or FadeIn)(m) for m in mobs], *extra, run_time=run_time)
        return mobs[0] if len(mobs) == 1 else mobs

    def hide(self, scene, *names, run_time: float = 0.4, extra=()):
        """Fade the named parts to opacity 0 (they stay members; reveal() brings them back)."""
        mobs = [self.parts[n] for n in names if not getattr(self.parts[n], "hidden", False)]
        for m in mobs:
            _save_op(m)
        anims = [m.animate.set_opacity(0) for m in mobs] + list(extra)
        if anims:
            scene.play(*anims, run_time=run_time)
        for m in mobs:
            self._flag(m, True)

    def _flag(self, m, hidden: bool):
        """Mark part m and every part nested in it shown/hidden."""
        fam = set(m.get_family())
        for p in self.parts.values():
            if p is m or p in fam:
                p.hidden = hidden

    def dim_to(self, k: float = 0.3) -> Transform:
        """Animation: everything shown fades to k of its opacity (hidden parts stay hidden)."""
        _save_op(self, "_dop")
        target = self.copy()
        _set_op(target, k, "_dop")
        return Transform(self, target)

    def undim(self) -> Transform:
        """Animation: back to the opacities saved by dim_to()."""
        target = self.copy()
        _set_op(target, None, "_dop")
        return Transform(self, target)

    # -- adding and removing mobjects
    def _ensure(self, scene):
        if self not in scene.get_mobject_family_members():
            scene.add(self)

    def _unparent(self, m):
        for f in self.get_family():
            if m in f.submobjects:
                f.remove(m)

    def attach(self, scene, *mobs, anims=None, run_time: float = 0.5, extra=(), into=None):
        """Play `anims` (default: FadeIn of each mob), then make the mobs members of this piece
        (or of `into`, a member group), so moving the piece moves them. Returns the first mob (or
        a list of them)."""
        anims = list(anims) if anims is not None else [FadeIn(m) for m in mobs]
        scene.play(*anims, *extra, run_time=run_time)
        _drop_groups(scene, anims)
        fam = set(self.get_family())
        for m in mobs:
            if m in scene.mobjects:
                scene.remove(m)
            if m not in fam:
                (into if into is not None else self).add(m)
        self._ensure(scene)
        return mobs[0] if len(mobs) == 1 else list(mobs)

    def detach(self, scene, *mobs, anims=None, run_time: float = 0.5, extra=()):
        """Take the mobs out of the piece and play `anims` (default: FadeOut of each)."""
        for m in mobs:
            self._unparent(m)
        scene.add(*mobs)
        scene.play(*(list(anims) if anims is not None else [FadeOut(m) for m in mobs]), *extra,
                   run_time=run_time)
        fam = scene.get_mobject_family_members()
        for m in mobs:
            if m in fam:
                scene.remove(m)

    def rescale(self, k: float, about_point=None):
        """Scale every shape by k but keep every text (and every chip, tag, labelled glyph) at
        its own size, so text stays >= 20 pt. Use via self.play(piece.animate.rescale(k))."""
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
    """V1. Five TEAL boxes A-E along the top, the bucket as six BLUE drawers along the bottom in
    pipeline order (PREFIXES), a small dashed bonus drawer under the sixth. Box j sits above the
    gap after drawer j; it reads READS[j] and writes WRITES[j]. 12.4 x 4.6 (width=12.4).

        relay = Relay(labels=False)                 # S01 teaser: nothing written yet
        tok = relay.token_at(0, "wave"); self.play(FadeIn(relay), FadeIn(tok))
        [tok] = relay.run(self, [(tok, 0)])         # A: wave -> page, into text_prompts/
        [tok] = relay.run(self, [(tok, 1)])         # B: -> long page, into text_paragraphs/
        tc, td = relay.run(self, [(tok, 2), (tok.copy(), 3)])     # the split: C and D together
        [te] = relay.run(self, [(td, 4)])
        relay.reveal(self, "drawer_labels", "icons")    # parts below; "letters", "names" for A-E
    Parts (all built; labels=True shows letters, names, drawer_labels, icons): "letters" (A-E,
    34 pt), "names" (two-line folder names), "drawer_labels" (two-line prefixes), "icons" (what
    each drawer holds), "edges" (reads + writes), "bonus_tag" (GREY "bonus").
    .boxes[j] .drawers[i] (.frame .handle) .bonus .letters[j] .names[j] .drawer_labels[i]
    .icons[i] .read_edges[j] .write_edges[j] .cabinet; .slot(i) where a token rests in drawer i,
    .center_of(j) box centre. Tokens are not part of the piece: the scene owns (and fades) them.
    Width: labels need width >= 11.6 (a 20 pt "paragraphs/" in each drawer); a small relay is
    Relay(width=8, labels=False) + reveal("letters"), or hide the labels before rescale(< 0.95)."""

    def __init__(self, width: float = 12.4, labels: bool = True, edges: bool = False,
                 bonus: bool = True, box_h: float = 1.3, drawer_h: float = 1.45, gap: float = 1.05,
                 **kw):
        super().__init__(**kw)
        p = width / 6
        self.pitch = p
        dw, bw = p - 0.12, p - 0.22
        self.drawers = VGroup()
        for i in range(6):
            x = -width / 2 + (i + 0.5) * p
            fr = RoundedRectangle(width=dw, height=drawer_h, corner_radius=0.1, stroke_color=CLOUD,
                                  stroke_width=2.5).set_fill(CLOUD, 0.1)
            fr.move_to([x, -drawer_h / 2, 0])
            handle = RoundedRectangle(width=min(0.42, dw * 0.4), height=0.08, corner_radius=0.04,
                                      stroke_width=0).set_fill(CLOUD, 0.9)
            handle.move_to(fr.get_top() + DOWN * 0.16)
            d = VGroup(fr, handle)
            d.frame, d.handle = fr, handle
            self.drawers.add(d)
        self.cabinet = RoundedRectangle(width=width + 0.16, height=drawer_h + 0.16, corner_radius=0.14,
                                        stroke_color=CLOUD, stroke_width=1.5, stroke_opacity=0.6)
        self.cabinet.move_to([0, -drawer_h / 2, 0])
        self.boxes = VGroup()
        y_b = gap + box_h / 2
        for j in range(5):
            fr = RoundedRectangle(width=bw, height=box_h, corner_radius=0.12, stroke_color=CTR,
                                  stroke_width=3).set_fill(CTR, 0.1)
            self.boxes.add(fr.move_to([-width / 2 + (j + 1) * p, y_b, 0]))
        self.add(self.cabinet, self.drawers, self.boxes)
        # the bonus drawer (dashed, under the sixth)
        bf = box(dw, 0.72, CLOUD, dashed=True).next_to(self.drawers[5].frame, DOWN, buff=0.16)
        bl = two_lines(BONUS_PREFIX, CAPTION, CLOUD).move_to(bf)
        self.bonus = VGroup(bf, bl)
        self.bonus.frame, self.bonus.text = bf, bl
        self.part("bonus", self.bonus, shown=bonus)
        self.part("bonus_tag", _keep(tag("bonus", S.GREY).next_to(bf, LEFT, buff=0.2)), shown=False)
        # labels
        self.drawer_labels, self.icons = VGroup(), VGroup()
        for i, d in enumerate(self.drawers):
            t = two_lines(PREFIXES[i], CAPTION, INK)
            t.move_to(d.frame.get_top() + DOWN * (0.3 + t.height / 2))
            self.drawer_labels.add(t)
            self.icons.add(token(DRAWER_KIND[i]).move_to(self.slot(i)))
        self.letters, self.names = VGroup(), VGroup()
        for j, b in enumerate(self.boxes):
            let = sans(LETTERS[j], 34, CTR, weight="BOLD")
            nm = two_lines(COMPONENTS[j], CAPTION, INK)
            VGroup(let, nm).arrange(DOWN, buff=0.08).move_to(b)
            self.letters.add(let)
            self.names.add(nm)
        for name, mob in (("drawer_labels", self.drawer_labels), ("icons", self.icons),
                          ("letters", self.letters), ("names", self.names)):
            self.part(name, mob, shown=labels)
        # edges: drawer -> box (read), box -> drawer (write)
        self.read_edges, self.write_edges = VGroup(), VGroup()
        for j, b in enumerate(self.boxes):
            r, w = self.drawers[READS[j]].frame, self.drawers[WRITES[j]].frame
            self.read_edges.add(self._edge(r.get_top() + RIGHT * 0.38, b.get_bottom() + LEFT * 0.32))
            self.write_edges.add(self._edge(b.get_bottom() + RIGHT * 0.32, w.get_top() + LEFT * 0.38))
        self.edges = VGroup(self.read_edges, self.write_edges)
        self.part("edges", self.edges, shown=edges)
        self.move_to(ORIGIN)

    @staticmethod
    def _edge(a, b, color=S.GREY):
        return Arrow(a, b, buff=0.06, stroke_width=2.5, color=color, max_tip_length_to_length_ratio=0.18,
                     max_stroke_width_to_length_ratio=10)

    def slot(self, i: int):
        """Where a token rests in drawer i (the lower part, where its content icon sits)."""
        return self.drawers[i].frame.get_bottom() + UP * 0.32

    def center_of(self, j: int):
        return self.boxes[j].get_center()

    def token_at(self, i: int, kind: str | None = None) -> VGroup:
        """A new token (not on screen) resting in drawer i; kind defaults to what drawer i holds."""
        return token(kind or DRAWER_KIND[i]).move_to(self.slot(i))

    def center_letters(self) -> list:
        """Animations: the letters move to their boxes' centres (when the names stay hidden)."""
        return [let.animate.move_to(b) for let, b in zip(self.letters, self.boxes)]

    def run(self, scene, routes, run_time: float = 2.4, flash: bool = True) -> list:
        """Each route (token, j[, kind]): the token rises from its drawer into box j, becomes
        OUT_KIND[j] (or kind) and drops into drawer WRITES[j]. Routes play in parallel.
        Returns the new tokens (on screen, owned by the scene)."""
        t1, t2, t3 = run_time * 0.38, run_time * 0.24, run_time * 0.38
        scene.play(*[rt[0].animate.move_to(self.center_of(rt[1])) for rt in routes], run_time=t1)
        news, anims = [], []
        for rt in routes:
            tok, j = rt[0], rt[1]
            new = token(rt[2] if len(rt) > 2 else OUT_KIND[j]).move_to(self.center_of(j))
            news.append(new)
            anims.append(Transform(tok, new))
            if flash:
                anims.append(Indicate(self.boxes[j], color=CTR, scale_factor=1.06))
        scene.play(*anims, run_time=t2)
        for rt, new in zip(routes, news):
            scene.remove(rt[0])
            scene.add(new)
        scene.play(*[n.animate.move_to(self.slot(WRITES[rt[1]])) for n, rt in zip(news, routes)],
                   run_time=t3)
        return news


class SubDrawers(Piece):
    """V1 detail: one drawer (`prefix`, mono PINK title) opened into group sub-drawers in a row;
    the last is the "default group" (flash it RED when a box with the unchanged group_name
    writes there). Tag it illustration. 5 groups: 10.5 x 1.3.
    .title .drawers[i] (.frame .text .name) .default (index) .slot(i) .flash(i, color) -> anim"""

    def __init__(self, prefix: str = "text_prompts/",
                 groups=("group-01/", "group-02/", "group-03/", "…", "default group"),
                 w: float = 1.95, h: float = 0.82, buff: float = 0.15, **kw):
        super().__init__(**kw)
        self.drawers = VGroup()
        for g in groups:
            t = mono(g, CAPTION, INK) if g.endswith("/") else label(g, CAPTION, INK)
            fr = RoundedRectangle(width=max(w, t.width + 0.3), height=h, corner_radius=0.08,
                                  stroke_color=CLOUD, stroke_width=2.5).set_fill(CLOUD, 0.1)
            t.move_to(fr.get_top() + DOWN * 0.24)
            d = VGroup(fr, t)
            d.frame, d.text, d.name = fr, t, g
            self.drawers.add(d)
        self.drawers.arrange(RIGHT, buff=buff)
        self.title = mono(prefix, CAPTION, LOOKUP).next_to(self.drawers, UP, buff=0.15)
        self.title.align_to(self.drawers, LEFT)
        self.default = len(groups) - 1
        self.add(self.title, self.drawers)

    def slot(self, i: int):
        return self.drawers[i].frame.get_bottom() + UP * 0.22

    def flash(self, i: int, color: str = ERR, run_time: float = 0.8):
        fr = self.drawers[i].frame
        return AnimationGroup(Indicate(fr, color=color, scale_factor=1.08),
                              fr.animate.set_stroke(color, 3.5).set_fill(color, 0.2), run_time=run_time)


class Leaderboard(Piece):
    """A schematic leaderboard (tag it illustration; caption it "ac215-mega-pipeline.dlops.io ·
    README.md line 54"): rows of groups, columns of stages; .light(r, c) fills a cell GREEN.
    3 groups: 11.4 x 2.0. .cells[r][c] .row_names .col_names"""

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
    """V2. The image's layers as translucent slabs, bottom-up, on a GREY floor line. Empty it is
    just the floor (slab_w + 0.5 wide); the five default slabs make it ~1.9 tall.

        st = LayerStack().move_to([4.4, -3.4, 0], aligned_edge=DOWN)   # the floor is its bottom
        st.drop(self, "base")                           # ORANGE "Debian 12 + Python 3.12"
        st.drop(self, "apt", src=keyword_copy)          # a mobject that turns into the slab
        self.play(*st.grow("apt", 1.0))                 # S06: the apt layer swells
        self.play(*st.grow("sync", 0.8, label_top=True)); st.attach(self, st.chips("sync"))
        st.attach(self, st.badge("copy"))               # TEAL build-step badge, left of the slab
        st.attach(self, st.stamp("apt"))                # GREEN "CACHED", right of the slab
        st.attach(self, st.size_label("apt", "842MB", after=st_stamp))   # right of the stamp
    Slab names and defaults: SLABS (text, colour, height, build step); any other name makes a
    TEAL slab (pass text/colour/h). A slab's text must fit inside slab_w - 0.2 (20 pt sans: ~0.15
    per character) or make() raises: pass a shorter text= or text="". .slabs[name] (.box .label
    .h) .order .floor .top_y(). Positioned helpers (not added: animate them in, then st.attach
    them so they move with the stack): .badge(name) [left] .stamp(name) [right] .size_label(name,
    text, after=None) [right, or right of `after`] .top_label(text) [above] .brace(text, note,
    side=RIGHT) .chips(name, n=26) [inside] .files(name="copy", key=True) [inside]. Room needed
    beside slab_w: ~0.6 left (badges), ~2.6 right (stamp + size), ~2.2 for a brace label."""

    def __init__(self, slab_w: float = 3.6, gap: float = 0.035, **kw):
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
        lab = VGroup()
        if text and h >= 0.3:
            lab = sans(text, CAPTION, INK).move_to(b)
            if lab.width > self.slab_w - 0.2:
                raise ValueError(f"slab text {text!r} is {lab.width:.2f} wide; the slab holds "
                                 f"{self.slab_w - 0.2:.2f}: shorten it or widen slab_w")
        s = VGroup(b, lab)
        s.box, s.label, s.h, s.name, s.hue = b, lab, h, name, color
        return s

    def drop(self, scene, name: str, text: str | None = None, color: str | None = None,
             h: float | None = None, src=None, run_time: float = 0.7, extra=()) -> VGroup:
        """Drop a new slab onto the stack (from `src`, a mobject that transforms into it, or from
        above). Returns the slab."""
        s = self.make(name, text, color, h)
        anims = [Transform(src, s)] if src is not None else [FadeIn(s, shift=DOWN * 0.5)]
        scene.play(*anims, *extra, run_time=run_time)
        if src is not None:
            scene.remove(src)
        self.slabs[name] = s
        self.order.append(name)
        self.add(s)
        self._ensure(scene)
        return s

    def grow(self, name: str, h: float, label_top: bool = False) -> list:
        """Animations: slab `name` takes height h; the slabs above (and anything attached at
        their height: badges, stamps, labels) move with it. label_top=True keeps its label at
        the top of the slab (room for chips() under it: h >= 0.8)."""
        s = self.slabs[name]
        dh = h - s.h
        nb = box(self.slab_w, h, s.hue, fill_opacity=0.25, radius=min(0.06, h / 2))
        nb.move_to(s.box.get_bottom() + UP * h / 2)
        anims = [Transform(s.box, nb)]
        if len(s.label):
            y = nb.get_top()[1] - 0.06 - s.label.height / 2 if label_top else nb.get_center()[1]
            anims.append(s.label.animate.move_to([nb.get_center()[0], y, 0]))
        y_bot, y_top = s.box.get_bottom()[1], s.box.get_top()[1]
        for m in self.submobjects:
            if m is s or m is self.floor:
                continue
            y = m.get_center()[1]
            if y > y_top - 1e-3:                       # above the slab: moves by dh
                anims.append(m.animate.shift(UP * dh))
            elif y > y_bot:                            # beside it (badge, stamp): by dh / 2
                anims.append(m.animate.shift(UP * dh / 2))
        s.h = h
        return anims

    def badge(self, name: str, words: bool = False) -> VGroup:
        """TEAL build-step badge (circled k) left of the slab (positioned)."""
        return build_badge(STEP_OF.get(name, 0), words=words).next_to(self.slabs[name].box, LEFT,
                                                                       buff=0.15)

    def stamp(self, name: str, text: str = "CACHED", color: str = VENV) -> VGroup:
        """A stamp right of the slab (positioned)."""
        return stamp(text, color, CAPTION).next_to(self.slabs[name].box, RIGHT, buff=0.15)

    def size_label(self, name: str, text: str, color: str | None = None, after=None) -> Text:
        """Mono size ("842MB") right of the slab, or right of `after` (e.g. its stamp)."""
        s = self.slabs[name]
        t = mono(text, CAPTION, color or s.hue)
        t.next_to(after if after is not None else s.box, RIGHT, buff=0.15)
        return t.set_y(s.box.get_center()[1])

    def top_label(self, text: str = "start: bash, venv on", color: str = CTR) -> Text:
        return sans(text, CAPTION, color).next_to(VGroup(*[self.slabs[n].box for n in self.order]),
                                                   UP, buff=0.12)

    def brace(self, text: str, note: str | None = None, color: str = S.GREY, side=RIGHT) -> VGroup:
        """A brace along all the slabs (side RIGHT or LEFT) with `text` (and a GREY note)."""
        slabs = VGroup(*[self.slabs[n].box for n in self.order])
        br = Brace(slabs, side, color=color)
        t = sans(text, CAPTION, INK)
        g = VGroup(t)
        if note:
            g.add(label(note, CAPTION, S.GREY))
            g.arrange(DOWN, buff=0.08, aligned_edge=LEFT if np.array_equal(side, RIGHT) else RIGHT)
        g.next_to(br, side, buff=0.1)
        out = VGroup(br, g)
        out.brace, out.text = br, t
        return out

    def chips(self, name: str, n: int = 26, color: str = VENV) -> VGroup:
        """n tiny package chips in slab `name` (positioned): under its label when the label sits
        at the top (grow(name, 0.8, label_top=True) first), else over the whole slab."""
        s = self.slabs[name]
        sb = s.box
        cols = max(1, int((sb.width - 0.3) / 0.2))
        d = pkg_dots(n, cols=min(cols, 13), color=color)
        lab_bottom = s.label.get_bottom()[1] if len(s.label) else None
        if lab_bottom is not None and lab_bottom - sb.get_bottom()[1] > d.height * 0.6 + 0.08 \
                and s.label.get_center()[1] > sb.get_center()[1] + 0.05:
            room = lab_bottom - sb.get_bottom()[1] - 0.08
            if d.height > room:
                d.scale_to_fit_height(room)
            return d.move_to([sb.get_center()[0], (lab_bottom + sb.get_bottom()[1]) / 2, 0])
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
    """Lecture 2's TEAL config card: ARG / ENV / USER / CMD write lines here, no layers. Lines
    flow left to right in rows (gap 0.45) and wrap to the next row when a line doesn't fit;
    restyle() reflows the lines after the one that changed. Default 8.4 x 2.2 (4 rows).

        card = ConfigCard().move_to([-2.0, -2.4, 0])
        card.write(self, "DEBIAN_PACKAGES · build time only", SYSTEM, key="arg")
        card.write(self, "no apt questions", key="e1", src=keyword_copy)   # a mobject turns into it
        self.play(card.restyle("uv", "the venv lives in /home/app/.venv · outside /app", VENV))
    More lines than the rows hold raise ValueError (make it wider, or rows=5: +0.4 tall).
    .lines (key -> text mobject, in writing order) .frame .title"""

    def __init__(self, width: float = 8.4, rows: int = 4, title: str = "image config · no layers",
                 pitch: float = 0.4, gap: float = 0.45, **kw):
        super().__init__(**kw)
        self.rows, self.card_w, self.pitch, self.gap = rows, width, pitch, gap
        h = 0.42 + rows * pitch + 0.18
        self.frame = box(width, h, CTR, fill_opacity=0.06)
        self.title = sans(title, CAPTION, CTR).move_to(
            self.frame.get_corner(UP + LEFT) + np.array([0.2, -0.24, 0]), aligned_edge=LEFT)
        self.lines: dict = {}
        self.add(self.frame, self.title)

    def _row_y(self, r: int) -> float:
        return self.frame.get_top()[1] - 0.62 - r * self.pitch

    def _layout(self, mobs: list) -> list:
        """Left-centre points for `mobs` in order (flow layout)."""
        x0 = self.frame.get_left()[0] + 0.2
        x1 = self.frame.get_right()[0] - 0.2
        pts, x, r = [], x0, 0
        for m in mobs:
            if m.width > x1 - x0:
                raise ValueError(f"config line {getattr(m, 'text', '?')!r} is {m.width:.2f} wide; "
                                 f"the card holds {x1 - x0:.2f}")
            if x > x0 and x + m.width > x1:
                x, r = x0, r + 1
            if r >= self.rows:
                raise ValueError("config card is full: make it wider or give it more rows")
            pts.append(np.array([x, self._row_y(r), 0]))
            x += m.width + self.gap
        return pts

    @staticmethod
    def _text(text: str, color: str, font: str) -> Text:
        return mono(text, CAPTION, color) if font == "mono" else sans(text, CAPTION, color)

    def line(self, text: str, color: str = INK, key=None, font: str = "sans") -> Text:
        """A positioned line (not added) after the last one; registered under `key`."""
        t = self._text(text, color, font)
        t.move_to(self._layout(list(self.lines.values()) + [t])[-1], aligned_edge=LEFT)
        self.lines[key if key is not None else text] = t
        return t

    def write(self, scene, text: str, color: str = INK, key=None, font: str = "sans",
              run_time: float = 0.5, src=None, extra=()) -> Text:
        """Write a line on the card (from `src`, a mobject that turns into it, if given)."""
        t = self.line(text, color, key, font)
        if src is not None:
            scene.play(Transform(src, t), *extra, run_time=run_time)
            scene.remove(src)
            self.add(t)
            self._ensure(scene)
            return t
        return self.attach(scene, t, anims=[Write(t)], run_time=run_time, extra=extra)

    def restyle(self, key, text: str | None = None, color: str | None = None,
                font: str = "sans") -> AnimationGroup:
        """Animation: line `key` gets new text and/or colour; the lines after it move if the
        flow changes. (The stored mobject stays the same object.)"""
        old = self.lines[key]
        t = self._text(text or old.text, color or old.get_color(), font)
        keys = list(self.lines)
        mobs = [t if k == key else self.lines[k] for k in keys]
        anims = []
        for k, m, p in zip(keys, mobs, self._layout(mobs)):
            if k == key:
                t.move_to(p, aligned_edge=LEFT)
                anims.append(Transform(old, t))
            elif np.linalg.norm(m.get_left() - p) > 1e-3:
                anims.append(m.animate.move_to(p, aligned_edge=LEFT))
        return AnimationGroup(*anims)


# ------------------------------------------------------------------ V3 + V4 · the window
class Window(Piece):
    """V3 (+ V4). Left: your laptop's component folder (GREY). Right: the image (TEAL) with an
    /app cavity holding the copied files and a GREEN /home/app/.venv box OUTSIDE it; on top, the
    container's dashed TEAL writable sheet with a GREEN shelf above the venv (uv add's packages
    land there). Between them the PINK -v "$(pwd):/app" route. 12.6 x 3.5 with 4 rows (each
    extra row +0.4 tall). Don't rescale it (its file names are 20 pt): it fits above a 3-row
    strip at full size.

        win = Window()                          # unmounted; Window(mounted=True) starts mounted
        self.play(FadeIn(win)); win.mount(self)          # route + the laptop sheet covers /app
        self.play(win.blink("cli.py"))                   # the same file blinks on both sides
        win.add_file(self, "uv.lock", VENV)              # appears on both sides at once
        chips = win.fill_shelf(self, 26)                 # packages on the writable sheet
        win.evaporate(self); win.new_sheet(self)         # exit: sheet + chips vanish; a new run
    files: names, or (name, colour); "secrets/" gets a tiny GOLD key with key=True; rows=n
    reserves room for add_file. .laptop (.frame .folder .area .rows .caption) .image (.frame
    .cavity .app .copied .caption) .venv (.frame .label) .sheet (.frame .caption .shelf [.chips])
    .route .route_label .cover (.frame .rows); .row(name, side="laptop"|"cover"|"copied").
    Parts: "route", "route_label", "cover" (the laptop sheet), "sheet"."""

    def __init__(self, files=("cli.py", "Dockerfile", "pyproject.toml", "secrets/"), copied=None,
                 rows: int | None = None, component: str = "transcribe_audio", key: bool = False,
                 mounted: bool = False, sheet: bool = True, **kw):
        super().__init__(**kw)
        copied = list(copied if copied is not None else files)
        files = list(files)
        self.capacity = max(len(files), len(copied), rows or 0)
        self.pitch, self.key = 0.4, key
        area_w, area_h = 3.0, self.capacity * 0.4 + 0.2
        lap_w, gap, venv_w = area_w + 0.3, 2.95, 2.7
        img_w = area_w + venv_w + 0.6
        blk_h = 0.5 + area_h + 0.2
        x_lap = -(lap_w + gap + img_w) / 2
        # laptop
        lap_fr = box(lap_w, blk_h, LAPTOP, fill_opacity=0.05).move_to([x_lap + lap_w / 2, blk_h / 2, 0])
        folder = mono(f"{component}/", CAPTION, LAPTOP)
        folder.move_to(lap_fr.get_corner(UP + LEFT) + np.array([0.15, -0.27, 0]), aligned_edge=LEFT)
        lap_area = self._area(area_w, area_h).move_to(lap_fr.get_bottom() + UP * (0.15 + area_h / 2))
        lap_rows = self._rows(files, lap_area)
        lap_cap = label("your laptop", CAPTION, LAPTOP).next_to(lap_fr, DOWN, buff=0.12)
        self.laptop = VGroup(lap_fr, folder, lap_area, lap_rows, lap_cap)
        L = self.laptop
        L.frame, L.folder, L.area, L.rows, L.caption = lap_fr, folder, lap_area, lap_rows, lap_cap
        # image
        x_img = x_lap + lap_w + gap
        img_fr = box(img_w, blk_h, CTR, fill_opacity=0.06).move_to([x_img + img_w / 2, blk_h / 2, 0])
        cav = self._area(area_w, area_h, color=CTR, fill=S.BG)
        cav.move_to([x_img + 0.2 + area_w / 2, lap_area.get_center()[1], 0])
        app = mono("/app", CAPTION, INK).next_to(cav, UP, buff=0.1).align_to(cav, LEFT)
        copied_rows = self._rows(copied, cav)
        img_cap = sans(f"image · {component}", CAPTION, CTR).next_to(img_fr, DOWN, buff=0.12)
        self.image = VGroup(img_fr, cav, app, copied_rows, img_cap)
        I = self.image
        I.frame, I.cavity, I.app, I.copied, I.caption = img_fr, cav, app, copied_rows, img_cap
        self.copied = copied_rows
        venv_fr = box(venv_w - 0.1, 0.9, VENV, fill_opacity=0.12)
        venv_fr.move_to([cav.get_right()[0] + 0.2 + (venv_w - 0.1) / 2, cav.get_center()[1], 0])
        venv_lab = mono("/home/app/.venv", CAPTION, VENV).next_to(venv_fr, UP, buff=0.1)
        self.venv = VGroup(venv_fr, venv_lab)
        self.venv.frame, self.venv.label = venv_fr, venv_lab
        self._venv_home = Dot(venv_fr.get_center(), radius=0.01).set_opacity(0)
        self.add(self.laptop, self.image, self.venv, self._venv_home)
        # the writable sheet
        self.sheet = self._sheet()
        self.part("sheet", self.sheet, shown=sheet)
        # the mount
        self.route = Line(lap_area.get_right() + RIGHT * 0.12, cav.get_left() + LEFT * 0.12,
                          color=LOOKUP, stroke_width=5)
        self.route_label = mono('-v "$(pwd):/app"', CAPTION, LOOKUP).next_to(self.route, UP, buff=0.14)
        cov = self._area(area_w, area_h, color=LAPTOP, fill=PANEL).move_to(lap_area)
        self.cover = VGroup(cov, self._rows(files, cov))
        self.cover.frame, self.cover.rows = cov, self.cover[1]
        if mounted:
            self.cover.move_to(cav)
            self.copied.set_opacity(0.3)
        self.part("route", self.route, shown=mounted)
        self.part("route_label", self.route_label, shown=mounted)
        self.part("cover", self.cover, shown=mounted)
        self.mounted = mounted
        self.move_to(ORIGIN)

    # -- building blocks
    @staticmethod
    def _area(w, h, color=LAPTOP, fill=None):
        r = RoundedRectangle(width=w, height=h, corner_radius=0.1, stroke_color=color, stroke_width=2)
        return r.set_fill(fill or color, 1 if fill else 0.08)

    def _row_pos(self, area, i: int):
        return area.get_corner(UP + LEFT) + np.array([0.18, -0.1 - (i + 0.5) * self.pitch, 0])

    def _rows(self, names, area) -> VGroup:
        rows = VGroup()
        for i, n in enumerate(names):
            name, col = (n, INK) if isinstance(n, str) else n
            r = file_row(name, col)
            if self.key and name == "secrets/":
                r.add(key_glyph(0.2).next_to(r, RIGHT, buff=0.15))
            rows.add(r.move_to(self._row_pos(area, i), aligned_edge=LEFT))
        return rows

    def _sheet(self) -> VGroup:
        img_fr = self.image.frame
        fr = box(img_fr.width, 0.52, CTR, dashed=True).next_to(img_fr, UP, buff=0.06)
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
        self.cover.move_to(self.laptop.area)
        for m in (self.route, self.route_label):
            _set_op(m)
            m.hidden = False
        self._ensure(scene)
        scene.play(Create(self.route), FadeIn(self.route_label), run_time=run_time * 0.35)
        self.reveal(scene, "cover", run_time=run_time * 0.15)
        scene.play(self.cover.animate.move_to(self.image.cavity), self.copied.animate.set_opacity(0.3),
                   run_time=run_time * 0.5)
        self.mounted = True

    def cover_to(self, alpha: float):
        """Animation: the laptop sheet slides to `alpha` along the route (0 laptop, 1 over /app)."""
        a, b = self.laptop.area.get_center(), self.image.cavity.get_center()
        return self.cover.animate.move_to(a + alpha * (b - a))

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
        r1 = self._rows([(name, color)], self.laptop.area)[0]
        r1.move_to(self._row_pos(self.laptop.area, i), aligned_edge=LEFT)
        r2 = None
        if self.mounted:
            r2 = self._rows([(name, color)], self.cover.frame)[0]
            r2.move_to(self._row_pos(self.cover.frame, i), aligned_edge=LEFT)
        scene.play(*[FadeIn(m, scale=1.2) for m in (r1, r2) if m is not None], run_time=run_time)
        scene.remove(*[m for m in (r1, r2) if m is not None])
        self.laptop.rows.add(r1)
        if r2 is not None:
            self.cover.rows.add(r2)
        self._ensure(scene)
        return r1, r2

    def tmp_page(self, scene, run_time: float = 0.6) -> VGroup:
        """A page written outside /app (say /tmp) lands on the dashed writable sheet (and dies
        with it)."""
        pg = page_token().scale_to_fit_height(0.4)
        pg.move_to(self.sheet.frame.get_center() + RIGHT * 0.4)
        return self.attach(scene, pg, anims=[FadeIn(pg, shift=DOWN * 0.4)], run_time=run_time,
                           into=self.sheet)

    def fill_shelf(self, scene, n: int = 26, run_time: float = 1.2) -> VGroup:
        """n GREEN package chips drop onto the shelf on the writable sheet (they are part of the
        sheet: evaporate() takes them away). Returns them."""
        sh = self.sheet.shelf
        d = pkg_dots(n, cols=13)
        if d.width > sh.get_length() - 0.1:
            d.scale_to_fit_width(sh.get_length() - 0.1)
        d.next_to(sh, UP, buff=0.03)
        self.attach(scene, d, anims=[LaggedStart(*[FadeIn(c, shift=DOWN * 0.3) for c in d],
                                                 lag_ratio=0.05)], run_time=run_time, into=self.sheet)
        self.sheet.chips = d
        return d

    def evaporate(self, scene, run_time: float = 1.0):
        """Exit with --rm: the writable sheet (and whatever is on it) floats up and vanishes."""
        self.parts.pop("sheet", None)
        self.detach(scene, self.sheet, anims=[FadeOut(self.sheet, shift=UP * 0.5)], run_time=run_time)

    def new_sheet(self, scene, run_time: float = 0.6) -> VGroup:
        """A new container from the same image: a fresh, empty writable sheet settles on top."""
        self.sheet = self._sheet()
        self.parts["sheet"] = self.sheet
        return self.attach(scene, self.sheet, anims=[FadeIn(self.sheet, shift=DOWN * 0.3)],
                           run_time=run_time)

    def venv_to_cavity(self):
        """Animation (ponder 3): the venv box slides into the /app cavity (lecture 2's layout)."""
        return self.venv.animate.shift(self.image.cavity.get_center() + DOWN * 0.15
                                       - self.venv.frame.get_center())

    def venv_home(self):
        """Animation: the venv box back to its place outside /app."""
        return self.venv.animate.shift(self._venv_home.get_center() - self.venv.frame.get_center())


# ------------------------------------------------------------------ V5 · who is calling?
class AdcChain(Piece):
    """V5. Left: your laptop's transcribe_audio/ folder with secrets/ and the GOLD key
    mega-pipeline.json. Middle: the container (TEAL): the PINK signpost
    GOOGLE_APPLICATION_CREDENTIALS=secrets/mega-pipeline.json planted at /app, the
    storage.Client() machine and the google.auth box; a dashed PINK window joins /app to the
    laptop. Right: Google Cloud (BLUE): gate 1 (authentication · who is calling?), gate 2 (IAM
    padlock; authorization · may it do this?) and the bucket door. 13.1 x 3.95 (captions
    included): it fits above a 3-row strip with chain.move_to([0, 0.75, 0]). Don't rescale it.

        chain = AdcChain(show=("ctr", "client", "auth"))   # parts shown at first, rest hidden
        self.play(FadeIn(chain)); chain.reveal(self, "post", "root"); chain.ask(self)
        chain.reveal(self, "laptop", "window"); chain.follow(self); tok = chain.mint(self)
        chain.reveal(self, "google"); chain.request(self, tok); chain.check(self, 1); chain.check(self, 2)
        chain.unfollow(self); chain.fail(self) / chain.unfail(self)     # S09 error variants:
        chain.reroot(self, "/tmp") / chain.reroot(self)                 # cd away from /app, back
        chain.reaim(self, "mega-pipeline/") / chain.reaim(self)         # run from the wrong folder
    Parts: laptop, window, ctr, post, root, client, auth, google; nested: "secrets" (row),
    "key" (glyph + name). .key .key_name .secrets .folder .post (.board .text .post .foot)
    .root_dot .root_label .client .auth .gates[0..1] (.bar .word .question .badge) .padlock
    .door .token .arrow .path. Methods return what they add (on screen, part of the piece)."""

    ALL = ("laptop", "window", "ctr", "post", "root", "client", "auth", "google")

    def __init__(self, show=ALL, component: str = "transcribe_audio", **kw):
        super().__init__(**kw)
        H = 3.5
        # laptop
        lf = box(3.2, H, LAPTOP, fill_opacity=0.05).move_to([-4.95, 0, 0])
        self.folder = mono(f"{component}/", CAPTION, LAPTOP)
        self.folder.move_to(lf.get_corner(UP + LEFT) + np.array([0.15, -0.3, 0]), aligned_edge=LEFT)
        self.secrets = file_row("secrets/").move_to(lf.get_corner(UP + LEFT) + np.array([0.3, -0.95, 0]),
                                                   aligned_edge=LEFT)
        self.key = key_glyph(0.3).move_to(lf.get_center() + DOWN * 0.15)
        self.key_name = mono("mega-pipeline.json", CAPTION, KEY).next_to(self.key, DOWN, buff=0.15)
        lcap = label("your laptop", CAPTION, LAPTOP).next_to(lf, DOWN, buff=0.12)
        laptop = VGroup(lf, lcap, self.folder)
        self.laptop_frame = lf
        # container
        cf = box(6.15, H, CTR, fill_opacity=0.05).move_to([-0.025, 0, 0])
        ccap = sans(f"container · {component}", CAPTION, CTR).next_to(cf, DOWN, buff=0.12)
        self.ctr_frame = cf
        post = signpost(["GOOGLE_APPLICATION_CREDENTIALS=", "secrets/mega-pipeline.json"], post_h=0.5)
        post.move_to(cf.get_corner(UP + LEFT) + np.array([0.15, -0.2, 0]), aligned_edge=UP + LEFT)
        self.post = post
        self.root_dot = Dot(post.root(), radius=0.07, color=LOOKUP)
        self.root_label = mono("/app", CAPTION, LOOKUP).next_to(self.root_dot, RIGHT, buff=0.15)
        self.root_label.shift(DOWN * 0.05)
        y_row = -0.85
        ct = mono("storage.Client()", CAPTION, CTR)
        self.client = VGroup(box(ct.width + 0.3, 0.66, CTR, fill_opacity=0.15).move_to(ct), ct)
        self.client.move_to([cf.get_left()[0] + 0.2 + self.client.width / 2, y_row, 0])
        at = mono("google.auth", CAPTION, INK)
        self.auth = VGroup(box(at.width + 0.3, 0.66, S.GREY, fill_opacity=0.12).move_to(at), at)
        self.auth.move_to([cf.get_right()[0] - 0.2 - self.auth.width / 2, y_row, 0])
        # the window (PINK, dashed) from /app out to the laptop
        wy = self.root_dot.get_center()[1]
        self.window = DashedLine([cf.get_left()[0], wy, 0], [lf.get_right()[0], wy, 0], color=LOOKUP,
                                 stroke_width=4, dash_length=0.1)
        # Google Cloud
        gf = box(3.0, H, CLOUD, fill_opacity=0.05).move_to([5.05, 0, 0])
        gic = cloud(0.62).move_to(gf.get_corner(UP + LEFT) + np.array([0.45, -0.32, 0]))
        gt = sans("Google Cloud", CAPTION, CLOUD).next_to(gic, RIGHT, buff=0.12)
        x0 = gf.get_left()[0]
        self.gates = [self._gate(1, x0 + 0.7, y_row, "authentication", "who is calling?"),
                      self._gate(2, x0 + 1.6, y_row, "authorization", "may it do this?")]
        y = gt.get_bottom()[1] - 0.2
        for g in self.gates:
            g.text.move_to([x0 + 0.2, y, 0], aligned_edge=UP + LEFT)
            y = g.text.get_bottom()[1] - 0.14
        self.padlock = padlock(0.36).move_to(self.gates[1].bar.get_center())
        self.gates[1].add(self.padlock)
        door = Rectangle(width=0.36, height=0.8, stroke_color=CLOUD, stroke_width=3).set_fill(CLOUD, 0.3)
        door.move_to([gf.get_right()[0] - 0.5, y_row, 0])
        dl = label("bucket", CAPTION, CLOUD).next_to(door, DOWN, buff=0.12)
        self.door = VGroup(door, dl)
        self.door.leaf = door
        self.google_frame = gf
        google = VGroup(gf, gic, gt, *self.gates, self.door)
        # parts
        P = {"laptop": laptop, "window": self.window, "ctr": VGroup(cf, ccap), "post": post,
             "root": VGroup(self.root_dot, self.root_label), "client": self.client,
             "auth": self.auth, "google": google}
        for n in self.ALL:
            self.part(n, P[n], shown=n in show)
        self.part("secrets", self.secrets, shown="laptop" in show, into=laptop)
        self.part("key", VGroup(self.key, self.key_name), shown="laptop" in show, into=laptop)
        self.token = self.arrow = self.path = None

    def part(self, name, mob, shown=True, into=None):
        mob = super().part(name, mob, shown)
        if into is not None:
            self.remove(mob)
            into.add(mob)
        return mob

    @staticmethod
    def _gate(i, x, y, word, question):
        bar = Line([x, y + 0.42, 0], [x, y - 0.42, 0], color=CLOUD, stroke_width=6)
        badge = step_badge(i, CLOUD, size=CAPTION, radius=0.17)
        w = label(word, CAPTION, CLOUD)
        q = label(question, CAPTION, S.GREY)
        head = VGroup(badge.copy(), w).arrange(RIGHT, buff=0.12)
        q.next_to(w, DOWN, buff=0.06, aligned_edge=LEFT)
        txt = VGroup(head, q)
        badge.next_to(bar, DOWN, buff=0.08)
        g = VGroup(bar, badge, txt)
        g.bar, g.badge, g.word, g.question, g.text = bar, badge, w, q, txt
        return g

    # -- the working chain
    def ask(self, scene, text: str = "who am I?", run_time: float = 0.8) -> VGroup:
        """Arrow client -> google.auth with the question above it."""
        a = Arrow(self.client.get_right(), self.auth.get_left(), buff=0.08, stroke_width=3, color=S.GREY,
                  max_tip_length_to_length_ratio=0.3)
        q = label(text, CAPTION, INK).next_to(VGroup(self.client, self.auth), UP, buff=0.12)
        q.set_x(a.get_center()[0])
        g = VGroup(a, q)
        self.asked = self.attach(scene, g, anims=[GrowArrow(a), FadeIn(q)], run_time=run_time)
        return g

    def follow(self, scene, run_time: float = 2.4, found: bool = True) -> VMobject:
        """google.auth reads the signpost: a PINK path from google.auth up under the board, down
        the post to the root, out through the window, to secrets/ on the laptop; the key glows
        (found=True). Returns the path (part of the piece; unfollow() removes it)."""
        board, px = self.post.board, self.post.post.get_center()[0]
        yb = board.get_bottom()[1] - 0.15
        root = self.root_dot.get_center()
        pts = [self.auth.get_top(), [self.auth.get_center()[0], yb, 0], [px, yb, 0], root,
               [self.ctr_frame.get_left()[0], root[1], 0], [self.laptop_frame.get_right()[0], root[1], 0],
               self.secrets.get_right() + RIGHT * 0.1]
        path = VMobject(stroke_color=LOOKUP, stroke_width=3).set_points_as_corners([np.array(p) for p in pts])
        dot = Dot(pts[0], radius=0.08, color=LOOKUP)
        scene.add(dot)
        scene.play(Create(path), MoveAlongPath(dot, path), run_time=run_time, rate_func=smooth)
        scene.remove(dot, path)
        self.add(path)
        if found:
            scene.play(Indicate(self.key, color=KEY, scale_factor=1.4), run_time=0.6)
        self.path = path
        return path

    def unfollow(self, scene, run_time: float = 0.4):
        if self.path is not None:
            self.detach(scene, self.path, run_time=run_time)
            self.path = None

    def mint(self, scene, run_time: float = 0.8) -> VGroup:
        """The key stamps out a GOLD token tag (short-lived) above google.auth. Returns it."""
        tok = token_tag().next_to(self.auth, UP, buff=0.15).align_to(self.auth, RIGHT)
        src = self.key.copy()
        scene.play(Transform(src, tok), run_time=run_time)
        scene.remove(src)
        self.add(tok)
        self.token = tok
        return tok

    def request(self, scene, tok=None, run_time: float = 1.0) -> Arrow:
        """A request arrow from google.auth to gate 1; the token (if given) rides above it."""
        g1 = self.gates[0].bar
        y = self.auth.get_center()[1]
        a = Arrow(self.auth.get_right(), [g1.get_center()[0] - 0.08, y, 0], buff=0.05, stroke_width=4,
                  color=INK, max_tip_length_to_length_ratio=0.15)
        anims = [GrowArrow(a)]
        if tok is not None:
            anims.append(tok.animate.next_to(a, UP, buff=0.1))
        self.attach(scene, a, anims=anims, run_time=run_time)
        self.arrow = a
        return a

    def check(self, scene, i: int, run_time: float = 0.8):
        """Gate i (1 or 2) passes: its bar turns GREEN, a GREEN check beside its word. Gate 2
        also opens its padlock and the bucket door. Returns the check."""
        from explainer.devops import check_mark
        g = self.gates[i - 1]
        ck = check_mark(0.28, VENV).next_to(g.word, RIGHT, buff=0.15)
        anims = [g.bar.animate.set_color(VENV), FadeIn(ck)]
        if i == 2:
            anims += [self.padlock.shackle.animate.shift(UP * 0.1),
                      self.door.leaf.animate.stretch(0.25, 0, about_edge=RIGHT)]
        return self.attach(scene, ck, anims=anims, run_time=run_time)

    # -- the error variants (S09)
    def fail(self, scene, run_time: float = 0.8):
        """The key isn't there: key + name fade, a RED cross where the key was. Returns it."""
        from explainer.devops import cross_mark
        x = cross_mark(0.36, ERR).move_to(self.key)
        self.hide(scene, "key", run_time=run_time * 0.5)
        self.cross = self.attach(scene, x, run_time=run_time * 0.5)
        return x

    def unfail(self, scene, run_time: float = 0.6):
        self.detach(scene, self.cross, run_time=run_time * 0.5)
        self.reveal(scene, "key", run_time=run_time * 0.5)

    def reroot(self, scene, text: str | None = "/tmp", dx: float = 1.9, run_time: float = 1.0):
        """cd away from /app: the root slides right by dx and reads `text`; the post leans to
        it, so the signpost no longer meets the window. reroot(scene, None) moves it back."""
        top = self.post.post.get_start()
        dot = top + DOWN * 0.5 + (RIGHT * dx if text is not None else 0)
        new_post = Line(top, dot, color=LOOKUP, stroke_width=4)
        new_foot = self.post.foot.copy().move_to(dot)
        new_label = mono(text or "/app", CAPTION, LOOKUP).next_to(Dot(dot), RIGHT, buff=0.15)
        new_label.shift(DOWN * 0.05)
        scene.play(self.root_dot.animate.move_to(dot), Transform(self.post.post, new_post),
                   Transform(self.post.foot, new_foot), Transform(self.root_label, new_label),
                   run_time=run_time)

    def reaim(self, scene, folder: str | None = "mega-pipeline/", run_time: float = 0.8):
        """docker run from the wrong laptop folder: the folder name becomes `folder` and
        secrets/ and the key vanish. reaim(scene, None) brings the component folder back."""
        if folder is None:
            t = mono(self._folder_text, CAPTION, LAPTOP)
        else:
            self._folder_text = getattr(self, "_folder_text", None) or self.folder.text
            t = mono(folder, CAPTION, ERR)
        t.move_to(self.folder, aligned_edge=LEFT)
        if folder is None:
            self.reveal(scene, "secrets", "key", run_time=run_time,
                        extra=[Transform(self.folder, t)])
        else:
            self.hide(scene, "secrets", "key", run_time=run_time, extra=[Transform(self.folder, t)])


# ------------------------------------------------------------------ V6 · two filters, two boxes
class TwoFilters(Piece):
    """V6. Left: the GREY component folder with the GOLD key in secrets/. Right, top: Git's
    history book; bottom: the image as a TEAL shipping box, the Docker Hub shelf to its right.
    Each sieve appears over its box when lowered. 13.0 x 4.6.

        v6 = TwoFilters(); self.play(FadeIn(v6))
        v6.lower(self, "git"); v6.pour(self, "git")      # .gitignore catches the key over the book
        v6.pour(self, "image")                           # no sieve: the key lands in the box (RED ring)
        v6.to_hub(self); v6.warn(self)                   # slides to the shelf; RED stamp above it
        v6.empty_box(self); v6.lower(self, "image"); v6.pour(self, "image")   # .dockerignore
    .folder (.frame .rows) .key .book .crate (the box) .hub .sieves {"git", "image"}; parts
    "sieve_git", "sieve_image". Keys poured into the box ride with it."""

    def __init__(self, files=("cli.py", "Dockerfile", "pyproject.toml", "secrets/"),
                 component: str = "transcribe_audio", **kw):
        super().__init__(**kw)
        fr = box(3.4, 2.7, LAPTOP, fill_opacity=0.05).move_to([-4.7, 0.3, 0])
        t = mono(f"{component}/", CAPTION, LAPTOP)
        t.move_to(fr.get_corner(UP + LEFT) + np.array([0.15, -0.27, 0]), aligned_edge=LEFT)
        rows = VGroup(*[file_row(f) for f in files]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        rows.next_to(t, DOWN, buff=0.22, aligned_edge=LEFT).shift(RIGHT * 0.1)
        sec = [r for r in rows if r.name == "secrets/"][0]
        self.key = key_glyph(0.24).next_to(sec, RIGHT, buff=0.15)
        cap = label("your laptop", CAPTION, LAPTOP).next_to(fr, DOWN, buff=0.12)
        self.folder = VGroup(fr, t, rows, self.key, cap)
        self.folder.frame, self.folder.rows = fr, rows
        self.book = book_glyph().move_to([1.4, 1.35, 0])
        self.crate = ship_box().move_to([0.3, -1.45, 0])
        self.hub = hub_shelf().move_to([5.1, -1.35, 0])
        self.add(self.folder, self.book, self.hub, self.crate)
        self.sieves = {"git": sieve(".gitignore"), "image": sieve(".dockerignore")}
        self.part("sieve_git", self.sieves["git"], shown=False)
        self.part("sieve_image", self.sieves["image"], shown=False)
        self._place_sieve("git")
        self._place_sieve("image")
        self.lowered: set = set()
        self.in_box: list = []

    def _target(self, which: str):
        return VGroup(*self.book[:3]) if which == "git" else self.crate.front

    def _place_sieve(self, which: str):
        sv, tg = self.sieves[which], self._target(which)
        top = self.book.get_top() if which == "git" else self.crate.get_top()
        sv.shift(np.array([tg.get_center()[0], top[1] + 0.3, 0]) - sv.bowl.get_center())

    def lower(self, scene, which: str, run_time: float = 0.7):
        """The sieve ("git": .gitignore over the book, "image": .dockerignore over the box)
        comes down over its target. Returns it."""
        self._place_sieve(which)
        sv = self.sieves[which]
        _set_op(sv)
        sv.hidden = False
        scene.play(FadeIn(sv, shift=DOWN * 0.5), run_time=run_time)
        self.lowered.add(which)
        return sv

    def pour(self, scene, which: str, run_time: float = 1.6):
        """Copies of the folder's files fly into the book ("git") or the box ("image"). With that
        sieve lowered, the key copy stays on the sieve; without, it lands inside (in the box it
        gets a RED ring). Returns the key copy (part of the piece, riding with its target)."""
        target = self._target(which)
        files = VGroup(*[r.glyph.copy() for r in self.folder.rows])
        k = self.key.copy()
        dest = target.get_center()
        caught = which in self.lowered
        k_dest = self.sieves[which].bowl.get_center() + UP * 0.12 if caught else dest + DOWN * 0.05
        scene.add(files, k)
        lag = LaggedStart(*[f.animate.move_to(dest).set_opacity(0) for f in files], lag_ratio=0.1)
        scene.play(lag, k.animate.move_to(k_dest), run_time=run_time)
        _drop_groups(scene, [lag])
        scene.remove(files, k)
        holder = self.sieves[which] if caught else (self.book if which == "git" else self.crate)
        holder.add(k)
        self._ensure(scene)
        if which == "image" and not caught:
            ring = Circle(radius=0.26, stroke_color=ERR, stroke_width=3).move_to(k)
            self.attach(scene, ring, anims=[Create(ring)], run_time=0.4, into=self.crate)
            k.ring = ring
            self.in_box += [k, ring]
        return k

    def to_hub(self, scene, run_time: float = 1.0):
        """The box slides right until it stands just left of the Docker Hub shelf."""
        dx = self.hub.get_left()[0] - 0.3 - self.crate.get_right()[0]
        scene.play(self.crate.animate.shift(RIGHT * dx), run_time=run_time)

    def warn(self, scene, text: str = "would publish the key", run_time: float = 0.5) -> VGroup:
        """A RED stamp above the box (it rides with the box). Returns it."""
        st = stamp(text, ERR).next_to(self.crate, UP, buff=0.25)
        self.warning = self.attach(scene, st, anims=[FadeIn(st, scale=1.3)], run_time=run_time,
                                   into=self.crate)
        self.in_box.append(st)
        return st

    def empty_box(self, scene, run_time: float = 0.5):
        """The rebuild: the key (its ring, the stamp) leave the box."""
        if self.in_box:
            self.detach(scene, *self.in_box, run_time=run_time)
            self.in_box = []


# ------------------------------------------------------------------ V7 · requires-python interval
class VersionLine(Piece):
    """Python 3.x versions on a number line (positions by MINOR version: 12 means 3.12, 12.15
    sits just right of it), the `>= 3.lo` interval GREEN, running off the right end. Levels:
    tick labels 0.45 below; dot labels 0.3 above (or 0.75 below with above=False); the interval
    label 1.05 above, left of the interval when it fits there, else over its start; a download
    arrow comes from 1.6 above. 11 x ~2.6 (width=11).

        vl = VersionLine(10, 16, lo=11)
        d = vl.dot(11, "laptop · 3.11.2", LAPTOP)           # dot + label above the line
        d2 = vl.dot(12.15, "image · 3.12.15", SYSTEM, above=False)
        self.play(*vl.move_lo(13))                          # the interval's start slides to 3.13
        arr = vl.download_arrow(15, "3.15.0 · uv-managed · 35.9 MiB")
    .axis .ticks .band .band_label .point(minor, dy) .lo"""

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
        """x of a minor version relative to the axis's left end, minus half the width."""
        return -self.line_w / 2 + (minor - self.first + 0.5) / (self.last - self.first + 1) * self.line_w

    def point(self, minor: float, dy: float = 0.0):
        """A point on the (possibly moved) axis at minor version `minor`, dy above it."""
        return self.axis.get_start() + np.array([self._x(minor) + self.line_w / 2, dy, 0])

    def _band(self, lo):
        left = self.point(lo)[0]
        right = self.axis.get_end()[0] + 0.25
        b = Rectangle(width=right - left, height=0.3, stroke_width=0).set_fill(VENV, 0.3)
        return b.move_to([(left + right) / 2, self.axis.get_center()[1], 0])

    def _band_label(self, lo):
        t = mono(f'requires-python = ">=3.{lo}"', self.size, VENV)
        start = self.point(lo, 1.05)
        if start[0] - 0.3 - t.width >= self.axis.get_start()[0] - 0.2:
            return t.move_to(start + LEFT * 0.3, aligned_edge=RIGHT)
        return t.move_to(start, aligned_edge=LEFT)

    def dot(self, minor: float, text: str, color: str, above: bool = True, size: float = 22) -> VGroup:
        """A dot on the line at `minor` and its mono label (positioned, not added). .dot .text"""
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
        """A PURPLE arrow dropping onto 3.minor from 1.6 above, its label on top (positioned)."""
        p = self.point(minor, 0.12)
        a = Arrow(p + UP * 1.6, p, buff=0, stroke_width=4, color=color, max_tip_length_to_length_ratio=0.15)
        g = VGroup(a)
        if text:
            g.add(mono(text, CAPTION, color).next_to(a, UP, buff=0.1))
        g.arrow = a
        return g


# ------------------------------------------------------------------ V8 · ticket stubs
class ApiCall(Piece):
    """V8. A container (TEAL) on the left, a BLUE API cloud on the right, a GREY line between
    them, and optionally bucket drawers along the bottom. 12.5 x 2.6 (x 4.5 with drawers).

        api = ApiCall("Speech-to-Text", "A · transcribe_audio")
        api.send(self, page_token())             # the payload rides to the cloud
        stub = api.stub(self)                     # a ticket stub comes back at once
        ring = api.ring(self, stub, "up to 90 s") # a small ring beside it fills
        api.reply(self, page_token())             # the result comes back to the container
        api2 = ApiCall("Text-to-Speech · long audio", "C · synthesis_audio_en",
                       drawers=["text_audios/group-01/"])
        api2.deliver(self, wave_token(), 0)       # the cloud writes straight into a drawer
    Payloads, stubs and rings belong to the scene (fade them yourself).
    .ctr (.frame .title) .inside() .api (.shape .title) .link .drawers[i] (.frame .text)"""

    def __init__(self, api: str = "Speech-to-Text", ctr: str = "A · transcribe_audio", drawers=None,
                 **kw):
        super().__init__(**kw)
        cf = box(3.6, 2.0, CTR, fill_opacity=0.06).move_to([-4.4, 0.6, 0])
        ct = sans(ctr, CAPTION, CTR).next_to(cf, UP, buff=0.12)
        self.ctr = VGroup(cf, ct)
        self.ctr.frame, self.ctr.title = cf, ct
        cl = cloud(3.2).move_to([4.3, 0.6, 0])
        at = sans(api, CAPTION, CLOUD).next_to(cl, UP, buff=0.12)
        self.api = VGroup(cl, at)
        self.api.shape, self.api.title = cl, at
        self.link = Line(cf.get_right() + RIGHT * 0.1, cl.get_left() + LEFT * 0.1, color=S.GREY,
                         stroke_width=2.5)
        self.add(self.ctr, self.api, self.link)
        self.drawers = VGroup()
        for name in drawers or []:
            t = mono(name, CAPTION, INK)
            fr = RoundedRectangle(width=max(3.4, t.width + 0.4), height=0.8, corner_radius=0.08,
                                  stroke_color=CLOUD, stroke_width=2.5).set_fill(CLOUD, 0.1)
            t.move_to(fr.get_top() + DOWN * 0.22)
            d = VGroup(fr, t)
            d.frame, d.text = fr, t
            self.drawers.add(d)
        if len(self.drawers):
            self.drawers.arrange(RIGHT, buff=0.3)
            self.drawers.move_to([0, -1.8, 0]).align_to(cl, RIGHT)
            self.add(self.drawers)

    def inside(self):
        """The centre of the container frame (where payloads start and results land)."""
        return self.ctr.frame.get_center()

    def send(self, scene, payload, run_time: float = 1.2):
        """The payload appears in the container and rides into the cloud. Returns it."""
        payload.move_to(self.inside())
        scene.play(FadeIn(payload), run_time=0.3)
        scene.play(payload.animate.move_to(self.api.shape.get_center()), run_time=run_time)
        return payload

    def stub(self, scene, text: str | None = "operation", run_time: float = 0.8) -> VGroup:
        """A ticket stub comes back from the cloud into the container at once. Returns it."""
        s = stub_glyph(text).move_to(self.api.shape.get_center())
        scene.play(FadeIn(s, scale=0.6), run_time=0.3)
        scene.play(s.animate.move_to(self.inside() + LEFT * 0.35 + UP * 0.15), run_time=run_time)
        return s

    def ring(self, scene, stub, text: str = "up to 90 s", run_time: float = 2.0, color: str = CTR) -> VGroup:
        """A small ring right of the stub fills over run_time (the wait); `text` under both.
        Returns ring + label."""
        arc = Arc(radius=0.24, start_angle=PI / 2, angle=-TAU, stroke_color=color, stroke_width=4)
        arc.next_to(stub, RIGHT, buff=0.18)
        base = Circle(radius=0.24, stroke_color=color, stroke_width=1.5, stroke_opacity=0.35).move_to(arc)
        t = label(text, CAPTION, color).next_to(VGroup(stub, arc), DOWN, buff=0.15)
        scene.play(FadeIn(t), FadeIn(base), run_time=0.3)
        scene.play(Create(arc), run_time=run_time, rate_func=linear)
        return VGroup(base, arc, t)

    def reply(self, scene, mob, run_time: float = 1.0):
        """`mob` appears at the cloud and travels back into the container. Returns it."""
        mob.move_to(self.api.shape.get_center())
        scene.play(FadeIn(mob), run_time=0.3)
        scene.play(mob.animate.move_to(self.inside() + DOWN * 0.2), run_time=run_time)
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
    "if it fails" line. Never terminal-styled. The frame is built for every item; items write
    in one at a time (on the word that names them).

        lf = LookFor([("download", "line 30"), ("one object name per recording", "line 41")],
                     fail="if it fails: DefaultCredentialsError").move_to([0, 1.2, 0])
        self.play(FadeIn(lf)); lf.write_item(self, 0); lf.write_item(self, 1); lf.write_fail(self)
    Parts "item0", "item1", ..., "fail". .rows[i] (.text .cite) .fail_row .frame .title.
    Height 0.75 + 0.44 per row; width fits the longest row."""

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
        self.title = label(title, CAPTION, S.GREY)
        inner = max(inner, self.title.width)
        w = max(width or 0, inner + 0.5)
        pitch = 0.44
        n = len(rows) + (1 if fail else 0)
        h = 0.55 + n * pitch + 0.2 + (0.1 if fail else 0)
        self.frame = box(w, h, S.GREY, fill=S.BG, fill_opacity=0.92, radius=0.12)
        self.title.move_to(self.frame.get_corner(UP + LEFT) + np.array([0.25, -0.3, 0]), aligned_edge=LEFT)
        self.add(self.frame, self.title)
        for i, r in enumerate(rows):
            y = self.frame.get_top()[1] - 0.72 - i * pitch
            r.text.move_to([self.frame.get_left()[0] + 0.25, y, 0], aligned_edge=LEFT)
            if len(r.cite):
                r.cite.move_to([self.frame.get_right()[0] - 0.25, y, 0], aligned_edge=RIGHT)
            self.part(f"item{i}", r, shown=False)
        if self.fail_row is not None:
            y = self.frame.get_top()[1] - 0.72 - len(rows) * pitch - 0.08
            self.fail_row.move_to([self.frame.get_left()[0] + 0.25, y, 0], aligned_edge=LEFT)
            self.part("fail", self.fail_row, shown=False)
        self.rows = rows

    def write_item(self, scene, i: int, run_time: float = 0.5):
        return self.reveal(scene, f"item{i}", run_time=run_time)

    def write_fail(self, scene, run_time: float = 0.5):
        return self.reveal(scene, "fail", run_time=run_time)


__all__ = [n for n in dir() if not n.startswith("_") and n not in {"annotations", "re", "np", "yaml",
                                                                    "Path"}]
