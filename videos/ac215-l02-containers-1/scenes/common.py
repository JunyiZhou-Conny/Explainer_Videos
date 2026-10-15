"""Shared scene code for AC215 L2 (Containers I: one image, from laptop to VM).

Paths, narration (SAY lines straight from script.md), the semantic colours of BRIEF.md, the running
example (prompts, titles, README commands), the three README trackers, loaders for the real
captures in assets/, terminal helpers, tags, and the video's set pieces V1-V8.

Notes for scene authors
=======================
``from manim import *`` first, then ``from common import *`` (common's capture() must win), then
``SAY = NARRATION["S07"]`` and ``assert len(SAY) == n``.  ``TITLES[cls]`` is the scene title.
Tested on screen by build/common_test.py (check clean, contact sheets read).

Colours (BRIEF.md, binding; layer slabs: TEAL outline, fill by what they hold)
    LAPTOP GREY · CLOUD BLUE · IMAGE TEAL (images, containers, layer outlines, config card, names)
    SYSTEM ORANGE (base image, apt, /usr/local/bin/python) · VENV GREEN (/.venv, uv.lock, uv's
    CPython, >=3.13) · TOOL PURPLE (docker, dockerd, builder, uv; UV is an alias) · ERR RED ·
    TURN YELLOW · COST GOLD · ROUTE PINK (PATH lookups, build context trip, push/pull, HTTPS;
    LOOKUP is an alias) · ARM = LAPTOP (arm64 · Apple Silicon) · AMD = CLOUD (amd64 · GCP VM) ·
    INK WHITE.  FILL["base"|"system"|"copy"|"venv"|"glass"] = slab fill colours.

Running example
    P_LAPTOP_HOME "student@laptop:~$" · P_LAPTOP "student@laptop:~/simple-translate$" ·
    P_VM "student@ac215-l02:~$" · T_LAPTOP "laptop" · T_VM "ssh · ac215-l02".
    Container prompts come from each capture: use istep() (below).
    README commands, spelled exactly as the README: CONTAINER_LS PRUNE IMAGE_LS CLONE CD BUILD RUN
    TRANSLATE EXIT LOGIN_README TAG_README PUSH_README DOCKER_TAG DOCKER_PUSH (README's line with
    <USER NAME> = student; not called TAG/PUSH: TAG is the toolkit's tag size) APT_DOCKER
    DOCKER_VERSION DEPLOY RUN_CLI.  vm-debian1x/01 and 03 were captured as
    "yes | sudo apt install docker.io": type APT_DOCKER, never that capture's .cmd.
    Extras typed in several scenes: CAT INSPECT_V1 INSPECT_V2 BUILD_PLAIN APT_UPDATE.
    REPO_ENTRIES = the clone's top level (laptop/05).

Trackers (top-left: left -6.5, top 3.5, bottom TRACK_BOTTOM = 2.9; ~8.6 wide with a caption)
    tracker_a(k, extra=False) / tracker_b / tracker_c -> ReadmeTracker already at step k (None:
    no step yet).  track(tr, k=None, extra=False) -> Animation: move to step k (None: stay) and
    set/clear " · extra".  Use track(), never tr.goto() (see "Text that morphs").
    STEPS_A (16) / STEPS_B (4) / STEPS_C (7), SECTION_A/B/C.

Captures (assets/terminal/<folder>/NN-name.txt; folders LAPTOP_DIR "laptop", PUSH_DIR
"laptop-push", VM12 "vm-debian12", VM13 "vm-debian13"; never print anything from "expected")
    cap = capture("21", LAPTOP_DIR)   # "21", "21-build-v4" or "21-build-v4.txt"; an ambiguous
                                      # number fails (vm-debian13 has two 06-…: name it in full)
    cap.cmd  cap.exit  cap.lines (output body)  cap.raw (all file lines)  cap.path
    cap.at(23, (26, 27), "…", 47) -> list[str] by FILE line numbers, as script.md writes them
        (line 1 = the "$ cmd" line, never printed). "…" items insert a "…" line; no automatic "…".
    cap.line(n) -> file line n · cap.istep(n) -> (container prompt, typed) of file line n ·
    cap.pick(...) = L1's body-indexed picker (pick index = file line - 1; adds "…" by itself).
    Captures are read with newline='' and \r is resolved like a terminal (text after \r
    overwrites), so file line numbers are the real ones (vm-debian12/03: 560 "Setting up
    docker.io …", 581 "Processing triggers …").
    Line transforms (script.md conventions): hash12(s) · cut(s, after) · fit(s, width=65) (compact
    build view; also folds line 3's "docker:default") · squeeze(lines) (drops columns empty in every
    row; a header-only table keeps them) · cols(lines, ["CREATED BY", "SIZE"]) · plus_done(lines) ·
    ask(s, "[y/N]") · split_prompt(s) -> (prompt, typed).
    Widths at 22 pt (65 chars): laptop/44 squeezed = 77 chars, too wide even for wide_term (75):
    cols(.., ["IMAGE", "ID", "DISK USAGE"]) = 63.  cut(laptop/29 line 9, "…bookworm") = 66 chars:
    the terminal cuts it again at 65.  vm-debian12/05 and the rate-limit line need wrap=True.

Sources
    code(name, a, b=None, language=None, focus=None, font_size=22, width=None) -> code_panel of
        assets/source/<name> lines a..b, header "<path> · line(s) a–b"; dot-gitignore.txt shows as
        ".gitignore"; Dockerfile.txt -> docker; README.md -> markdown: pass "docker" for its
        Dockerfile blocks, e.g. code("README.md", 135, 136, "docker").  excerpt(), source_text().
        Panel width = longest line x 0.183 + 0.5 (README line 135 alone is ~8.9 wide).
    readme_card(line or (a, b), body str|Mobject, quote=False, card_w=None) -> GREY README card
        (str body: "\n" separates lines, 22 pt serif).

Terminals (22 pt, 65 chars a row, 12.6 wide; placed centred with the bottom edge at BOTTOM = -3.5)
    term(prompt=P_LAPTOP, rows=10, title=T_LAPTOP) · laptop_term(rows) · vm_term(rows) ·
    wide_term(rows, prompt) (13.2 wide, 20 pt, 75 chars: only for the ls-in-columns beats).
    Height = rows x 0.403 + 0.85.  A 3-row strip's top edge is STRIP_TOP (-1.44): a picture over
    a strip lives in y in [STRIP_TOP + 0.15, TRACK_BOTTOM - 0.1] (about 4 units).
    resize(scene, t, rows, keep=None, extra=(), run_time=0.8) grow/shrink, bottom edge fixed.
    bare_prompt(scene, t) · type_cmd(scene, t, cmd) (replaces a bare prompt line) ·
    istep(scene, t, line) (sets the capture's own container prompt, types the rest) ·
    type_answer(scene, t, ln, line_text, key, asked_at) (the "[y/N] y" keystroke; ln = the
    printed ask() row, asked_at = scene.renderer.time when it printed) ·
    pin(scene, line, mob) / attach(scene, line, mob) / unpin(scene, pairs) (marks that scroll
    with a row: anything drawn over a row that later scrolls must be pinned) · beside(mob, line) ·
    row_tag(parts) (a tag that fits one row) · under(g, color) · hl_bar(g, color) · substring()
    and glyph_range() (from explainer.devops) pick glyphs of a row: substring(t.find("x"), "x").
Tags (>= 20 pt): your_turn() extra_tag() short_extra() illustration_tag(s) erratum_tag(s)
    recorded_tag(s) real_capture_tag(s) stand_in_tag() (two lines, 5.8 wide) preview_tag(s)
    cost_tag(s) (GOLD) expected_tag() user_caption() (YELLOW, 8.3 wide at 22 pt).
Glyphs: outline_box(w, h, color, solid=False) (a dashed one Transforms into a solid one by closing
    its dashes: for "absent until now" boxes) · docker_chip() builder_box() vm_glyph() shelf_glyph()
    lock_glyph() mini_stack(fills) sticky(text) fingerprint() figure(word) (L1's walking PINK
    figure) project_tree(new=None) (the clone as a file tree, `ls -a` order) · route(a, b, arc)
    PINK arrow · travel(mob, path) · bounce(mob, point) (animations).

Text that morphs
    Manim's check computes a Text's size from its height, so Transform("VM" -> "container")
    reads as < 20 pt.  steady(s, size, color, mono_font=False) builds text with a fixed height
    (an invisible strut): Transform between steady texts is safe.  Tracker captions, slab and
    tile values, start-up lines, glass and kernel labels already are steady.  Otherwise use
    ReplacementTransform / FadeTransform for text, or mono_line() rows.

Set pieces (sizes are defaults; every text >= 20 pt; widths in frame units)
    V1 Ladder(rung_w=7.6)  8.1 x 4.2 with header; rung 1 at the bottom, all dim at first;
        .rungs[i] .veils[i] .icons{2, 3} .header; .light(i, level=1.0) -> Animation (0 dim,
        0.6 soft, 1 lit)
    V1 Nest(vm_w=5.2, vm_h=3.0)  L1's closing picture: .vm (.frame .title) .venv; .slot() dashed
        "container · L2" · .solid() TEAL "container" (same place; ReplacementTransform(slot, solid))
        · .venv_spot() point · .venv_label() "/.venv" (mobjects are returned, not added)
    V2 Slab(text, fill, slab_w=3.4, slab_h=0.46, dashed=False)  .box .text (labels <= 19 chars)
    V2 LayerStack(stack_w=3.4)  stands on .floor (invisible; place the stack first) .slabs
        .make(text, fill, slab_h=0.46) -> Slab where it will land (several in a row stack up)
        .drop(scene, *slabs, anim=None, extra=()) plays the landing (default: fall in from above;
            or anim=TransformFromCopy(src, slab)), then makes them part of the stack
        .accept(scene, *slabs) (after animating them yourself) · .top_y()
        .brace(slabs, text) -> Brace + label on the left (not added)
        .restack(heights) -> [Animations] new heights bottom-up, floor kept; a slab too thin for its
        text moves the text just left of the stack.  mb_height(mb) (sqrt scale): the real
        docker history sizes (85.3, 9.7, 54.5, 0.016, 97.5, 0.25, 125 MB) stack to ~3.7 units.
        Sizes: 4 base slabs of 0.15 + 0.46 + 0.46 + uv sync 0.8 ~ 2.6 tall.
    V2 Glass(glass_w=3.4, process="main process")  the container's writable layer (dashed,
        glowing TEAL, "writable layer") + process dot, its label above the right end;
        .on(stack) places it on top · .stop(note="stopped") -> Animation · .dissolve() -> Animation
    V2/V3 ConfigCard(rows=("ENTRYPOINT", "CMD", "WorkingDir"), card_w=3.6)  3.6 x 3.6 (3 rows);
        rows ("ENV", "ENTRYPOINT", "CMD", "WorkingDir") for S02.  .frame .title .keys{} .slots{}
        .tile(text, color=IMAGE, dashed=False) -> Tile (.frame .text .value) · .place(row, tile)
        positions + records it (animate it in yourself) · .put(scene, row, tile, anim=None)
        slides/plays it in and records it · .take(scene, row) falls off + fades · .note(row, text)
        GREY value in the slot ("null", '""') · .startup(text, color) -> steady mono line under
        the card (.line; Transform(card.line, card.startup(new)) to change it) · .everything()
        -> VGroup(card, tiles, notes, line) to move or fade together (tiles are NOT children).
        A slot holds (card_w - 0.6) / 0.167 chars: 18 at 3.6; card_w >= 6.0 puts key and slot
        on one line (pass inline=False to keep a wide card stacked).  A tile is 0.167 x chars + 0.3
        wide: '["-c", "source … && exec bash"]' (5.5) needs card_w=6.0, inline=False; the full
        '["-c", "source .venv/bin/activate && exec bash"]' (8.2) needs card_w=8.8, inline=False.
    V4 VersionLine(first=10, last=16, lo=13, line_w=11.0, label_buff=1.0)  .axis .ticks .band
        .band_label; .dot2(minor, top, bottom, color, above=True) two-line labelled dot (.dot
        .top .bottom); below the line it clears the tick labels · .dot(...) as L1 · .point(minor)
    V4 PathDoors(dirs, colors, door_w=0.9, door_h=1.3, gap=0.45)  "…" is a narrow door;
        .knock(scene, word, found) (None: RED "command not found") · .insert_front(scene, dir,
        color) · .remove_front(scene); each door .frame .label .dir .door_color
    V5 CacheChain(steps, box_h=0.95)  "[k/n] INSTR" (GREY "[k/n]" over the instruction, "\n"
        breaks it); 4 steps ~ 9.2 wide x 2.9 tall; .boxes (.frame .text) .badges .dominoes;
        .feeds(i) -> 2 thin arrows into badge i (not added) · .badge(i, color) -> Animation ·
        .stamp(i, "CACHED") -> tag under box i (recorded in .stamps, not added) ·
        .topple(a, b=None) -> Animation (RED wave a..b) · .stand_up() -> Animation
    V5 Parcel(names=(".git/", "cli.py", "Dockerfile"), extra=6)  ~5 wide (6.6 with 4 names);
        .items{name} (.glyph .name_text) .crowd .tape .title; .light(name, color) -> Animation
    V5 Sieve(sieve_w=3.0)  ".dockerignore" mesh, dashed; .solidify(color=None) -> Animation
    V6 NameTags(target, names)  sticky notes right of target, linked (.notes .links) ·
        name_parts(name) -> parts (.parts .seps .captions .ticks; captions alternate below/above;
        9.7 x 1.6) · RegistryShelf(title, shelf_w=4.4, shelf_h=2.4, boards=2, dashed=False)
        .spot(board, k, n=3) point · .door · .shut() -> Animation (door RED + cross)
    V7 platform_chip("arm64"|"amd64") (.chip .glyphs; amd64 5.2 wide) · glyph_row(kind, n) ·
        PlatformMenu(title, rows=[(text, colour or None = dimmed attestation)]) .rows .mark(i, color)
    V8 KernelPicture(n=3)  7.9 x 2.7; .vms[i] (.frame .title .os .kernel); .to_containers() ->
        [Animations]: kernels merge into one GREY bar, VMs shrink into TEAL containers (.bar is set;
        call .desktop_vm() after playing them: dashed "Linux VM · Docker Desktop" under the bar)
        · vm_with_docker() (S14: .frame .title .kernel .dockerd .slot)
    CostDial(radius=0.55, caption="cost")  L1's GOLD dial, no digits: .run(scene, turns, seconds)
        · .freeze() (S16, on Delete)

Pitfalls (from L1): never set width/height/color/depth attributes on a VGroup subclass (these
classes use stack_w, slab_h, card_w …); text >= 20 pt inside x in [-6.6, 6.6], y in [-3.6, 3.6];
after animating a part of a set piece, `self.add(piece)` before adding new children to it.
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import yaml
from manim import (DL, DOWN, DR, LEFT, ORIGIN, RIGHT, UL, UP, UR, AnimationGroup, Arc, Arrow, Brace,
                   Circle, DashedVMobject, Dot, FadeIn, FadeOut, LaggedStart, Line, MoveAlongPath,
                   Polygon, Rectangle, Restore, Rotate, RoundedRectangle, Square, Succession, Text,
                   Transform, Triangle, ValueTracker, VGroup, always_redraw, linear)

from explainer import style as S
from explainer.components import pause_and_ponder, person_icon, ponder_card  # noqa: F401 (re-export)
from explainer.devops import (CAPTION, LABEL, MONO, OUTPUT, PANEL, SMALL, TAG, ReadmeTracker,  # noqa: F401
                              Terminal, box, check_mark, chip, code_panel, cross_mark, file_glyph,
                              file_tree, folder_glyph, glyph_range, label, laptop, line_pitch, mono,
                              mono_line, substring, tag)
from explainer.script import load_narration

# ------------------------------------------------------------------ paths and data
HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
ASSETS = PROJECT / "assets"
TERMINAL = ASSETS / "terminal"
SOURCE = ASSETS / "source"

SPEC = yaml.safe_load((PROJECT / "video.yaml").read_text())
TITLES = {s["cls"]: s["title"] for s in SPEC["scenes"]}
_script = PROJECT / "script.md"
NARRATION = load_narration(_script) if _script.exists() else {}

# ------------------------------------------------------------------ semantic colours
LAPTOP = S.GREY
CLOUD = S.BLUE
IMAGE = S.TEAL
SYSTEM = S.ORANGE
VENV = S.GREEN
TOOL = S.PURPLE
UV = TOOL
ERR = S.RED
TURN = S.YELLOW
COST = S.GOLD
ROUTE = S.PINK
LOOKUP = ROUTE
INK = S.WHITE
DIMMED = S.GREY
ARM = LAPTOP                 # arm64 · Apple Silicon (a laptop)
AMD = CLOUD                  # amd64 · Intel/AMD · default GCP VM
FILL = {"base": SYSTEM, "system": SYSTEM, "copy": LAPTOP, "venv": VENV, "glass": IMAGE}

# ------------------------------------------------------------------ layout
TRACK_LEFT, TRACK_TOP = -6.5, 3.5
BOTTOM = -3.5                # a terminal's bottom edge (kept when it grows or shrinks)
STRIP_ROWS = 3
STRIP_TOP = BOTTOM + STRIP_ROWS * line_pitch(22) + 0.85   # top edge of a 3-row 22 pt strip
TRACK_BOTTOM = 2.9           # the tracker's lowest point (header + dots + caption under y = 3.5)



def steady(s: str, size: float = 20, color=INK, mono_font: bool = False, **kw) -> Text:
    """Text with a fixed vertical extent (an invisible '|' strut under its first glyph), so that a
    Transform between two steady texts keeps the font size the check tool computes from height.
    Use it for anything that morphs into other words (captions, start-up lines, tile values)."""
    t = (mono if mono_font else label)("|" + s, size, color, **kw)
    pipe = t[0]
    if len(t) > 1:
        pipe.move_to([t[1].get_center()[0], pipe.get_center()[1], 0])
    pipe.set_opacity(0)
    return t


# ------------------------------------------------------------------ the running example
USER = "student"
LAPTOP_HOST, VM_HOST = "laptop", "ac215-l02"
P_LAPTOP_HOME = f"{USER}@{LAPTOP_HOST}:~$"
P_LAPTOP = f"{USER}@{LAPTOP_HOST}:~/simple-translate$"
P_VM = f"{USER}@{VM_HOST}:~$"
T_LAPTOP = "laptop"
T_VM = f"ssh · {VM_HOST}"

# README commands, exactly as the README spells them (README.md line in the comment)
CONTAINER_LS = "docker container ls"                                        # 115
PRUNE = "docker system prune"                                               # 117
IMAGE_LS = "docker image ls"                                                # 118
CLONE = "git clone https://github.com/dlops-io/simple-translate.git"        # 50
CD = "cd simple-translate"                                                  # 51
BUILD = "docker build -t simple-translate -f Dockerfile ."                  # 174
RUN = "docker run --rm -ti simple-translate"                                # 180
TRANSLATE = 'python cli.py -t "Good morning" -s "en" -d "es"'               # 182
EXIT = "exit"                                                               # 184
LOGIN_README = "docker login -u <USER NAME> -p <ACCESS TOKEN>"              # 189
TAG_README = "docker tag simple-translate <USER NAME>/simple-translate-ac215"   # 190
PUSH_README = "docker push <USER NAME>/simple-translate-ac215"              # 191
DOCKER_TAG = "docker tag simple-translate student/simple-translate-ac215"   # 190, <USER NAME> = student
DOCKER_PUSH = "docker push student/simple-translate-ac215"                  # 191, <USER NAME> = student
APT_DOCKER = "sudo apt install docker.io"                                   # 210
DOCKER_VERSION = "sudo docker --version"                                    # 213
DEPLOY = "sudo docker run --rm -ti dlops/simple-translate"                  # 215
RUN_CLI = "python cli.py"                                                   # 218
# extras (not in the README) that several scenes type
INSPECT_V1 = ("docker image inspect simple-translate --format 'Entrypoint={{json .Config.Entrypoint}} "
              "Cmd={{json .Config.Cmd}} WorkingDir={{json .Config.WorkingDir}}'")
INSPECT_V2 = ("docker image inspect simple-translate --format 'Entrypoint={{json .Config.Entrypoint}} "
              "Cmd={{json .Config.Cmd}}'")
BUILD_PLAIN = "docker build --progress=plain -t simple-translate -f Dockerfile ."
APT_UPDATE = "sudo apt-get update"
CAT = "cat Dockerfile"

# the repo's top level (laptop/05: `ls -a`, file lines 4-12)
REPO_ENTRIES = [".git/", ".gitignore", ".vscode/", "Dockerfile.txt", "README.md", "cli.py",
                "docker-build-push.sh", "docker-shell.sh", "pyproject.toml"]

# ------------------------------------------------------------------ README trackers (BRIEF.md)
SECTION_A = "Developing App using Containers"
STEPS_A = ["container ls", "Stop containers", "system prune", "image ls", "Clone repo",
           "Create Dockerfile", "FROM (1/5)", "ENTRYPOINT (2/5)", "uv, COPY (3/5)", "uv sync (4/5)",
           "CMD (5/5)", "Solution file", "Build image", "Run container", "Translate", "Exit"]
SECTION_B = "Pushing Docker Image to Docker Hub"
STEPS_B = ["Access token", "Login", "Tag", "Push"]
SECTION_C = "Running App on VM using Docker"
STEPS_C = ["Create VM", "SSH", "Install Docker", "Docker version", "Run image", "Run cli", "Delete VM"]


def place_tracker(tr: ReadmeTracker) -> ReadmeTracker:
    """Pin a tracker to the house corner (left edge -6.5, top 3.5: inside the safe frame)."""
    tr.shift(np.array([TRACK_LEFT - tr.get_left()[0], TRACK_TOP - tr.get_top()[1], 0]))
    return tr


def _caption(tr: ReadmeTracker, k: int, extra: bool) -> Text:
    """The caption 'step k of N: <title>[ · extra]' as a steady text (k = 0: an empty caption)."""
    if not k:
        return steady("", tr.size, tr.hi_color).next_to(tr.dots, RIGHT, buff=0.25)
    s = f"step {k} of {len(tr.steps)}: {tr.steps[k - 1]}"
    if extra:
        t = steady(s + " · extra", tr.size, tr.hi_color, t2c={"· extra": S.GREY})
    else:
        t = steady(s, tr.size, tr.hi_color)
    return t.next_to(tr.dots, RIGHT, buff=0.25)


def _tracker(section, steps, step, extra):
    tr = ReadmeTracker(section, steps)
    if step:
        tr.set_step(step)
    tr.remove(tr.caption)
    tr.caption = _caption(tr, step or 0, extra)
    tr.add(tr.caption)
    return place_tracker(tr)


def tracker_a(step: int | None = None, extra: bool = False) -> ReadmeTracker:
    """README › Developing App using Containers (16 steps), at `step` (1-based)."""
    return _tracker(SECTION_A, STEPS_A, step, extra)


def tracker_b(step: int | None = None, extra: bool = False) -> ReadmeTracker:
    """README › Pushing Docker Image to Docker Hub (4 steps)."""
    return _tracker(SECTION_B, STEPS_B, step, extra)


def tracker_c(step: int | None = None, extra: bool = False) -> ReadmeTracker:
    """README › Running App on VM using Docker (7 steps)."""
    return _tracker(SECTION_C, STEPS_C, step, extra)


def track(tr: ReadmeTracker, k: int | None = None, extra: bool = False, run_time: float = 0.5):
    """Animation: move the tracker to step k (None: stay) with or without the ' · extra' caption.
    Use this, not tr.goto() (its caption morph would read as < 20 pt in the check)."""
    k = tr.k if k is None else k
    anims = []
    if k != tr.k:
        for i, d in enumerate(tr.dots, start=1):
            col = tr.hi_color if i == k else (S.GREY if i < k else S.GREY_DARK)
            anims.append(d.animate.set_color(col).scale((1.5 if i == k else 1.0) / (d.width / 0.12)))
    anims.append(Transform(tr.caption, _caption(tr, k, extra)))
    tr.k = k
    return AnimationGroup(*anims, run_time=run_time)


def caption_extra(tr: ReadmeTracker, on: bool = True):
    """L1 name for track(tr, extra=on)."""
    return track(tr, None, on)


# ------------------------------------------------------------------ captures
LAPTOP_DIR, PUSH_DIR, VM12, VM13 = "laptop", "laptop-push", "vm-debian12", "vm-debian13"


def _resolve_cr(s: str) -> str:
    """What a terminal shows for a line with carriage returns: each segment overwrites from col 0."""
    s = s.rstrip("\r")
    if "\r" not in s:
        return s
    out: list[str] = []
    for seg in s.split("\r"):
        for i, ch in enumerate(seg):
            if i < len(out):
                out[i] = ch
            else:
                out.append(ch)
    return "".join(out)


_PROMPT_RE = re.compile(r"^((?:\([^)]*\) )?[\w.-]+@[\w.-]+:[^#$\s]*[#$])(?: (.*))?$")


def split_prompt(s: str) -> tuple[str, str]:
    """'root@01dca6d0f4d8:/# python cli.py' -> ('root@01dca6d0f4d8:/#', 'python cli.py').
    '(app) root@…:/# exit' keeps '(app) ' in the prompt. A line without a prompt -> ('', s)."""
    m = _PROMPT_RE.match(s)
    if not m:
        return "", s
    return m.group(1), m.group(2) or ""


class Capture:
    """One captured command. .cmd (as typed), .lines (output body), .exit (status), .raw (every
    file line, \\r resolved), .path."""

    def __init__(self, cmd: str, lines: list[str], exit_code: int, raw: list[str], path: Path):
        self.cmd, self.lines, self.exit, self.raw, self.path = cmd, lines, exit_code, raw, path

    def line(self, n: int) -> str:
        """File line n (1-based; line 1 is the '$ …' command)."""
        if not 1 <= n <= len(self.raw):
            raise IndexError(f"{self.path.name} has {len(self.raw)} lines, not {n}")
        return self.raw[n - 1]

    def at(self, *spec) -> list[str]:
        """Lines by FILE line numbers, as script.md writes them: ints, (a, b) inclusive ranges and
        '…' items (a literal '…' line). at(23, (26, 27), '…', 47). Never adds '…' by itself."""
        out: list[str] = []
        for r in spec:
            if isinstance(r, str):
                out.append(r)
                continue
            a, b = (r, r) if isinstance(r, int) else r
            if a < 2:
                raise ValueError("file line 1 is the '$ …' command; it is never printed")
            out += [self.line(n) for n in range(a, b + 1)]
        return out

    def pick(self, *ranges, ellipsis: str = "…") -> list[str]:
        """L1's picker: output BODY lines by 1-based inclusive ranges (pick index = file line - 1),
        a '…' between ranges that skip lines. Prefer .at() with script.md's file line numbers."""
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

    def istep(self, n: int) -> tuple[str, str]:
        """File line n split into (container prompt, typed text)."""
        return split_prompt(self.line(n))


def capture(name: str, folder: str = LAPTOP_DIR) -> Capture:
    """assets/terminal/<folder>/<name>: name = 'NN', 'NN-slug' or 'NN-slug.txt'. A bare number
    must match exactly one file. Fails loudly when missing: never show an output that wasn't
    captured. Reads with newline='' and splits on \\n only, so file line numbers are exact."""
    d = TERMINAL / folder
    stem = name[:-4] if name.endswith(".txt") else name
    p = d / f"{stem}.txt"
    if not p.exists():
        hits = sorted(d.glob(f"{stem}-*.txt"))
        if len(hits) != 1:
            raise FileNotFoundError(f"capture {folder}/{name}: {len(hits)} matches "
                                    f"{[h.name for h in hits]} (see ASSETS.md)")
        p = hits[0]
    with open(p, encoding="utf-8", newline="") as f:
        text = f.read()
    raw = [_resolve_cr(s) for s in text.rstrip("\n").split("\n")]
    cmd = raw[0][2:] if raw[0].startswith("$ ") else ""
    body = raw[1:]
    code = 0
    if body and re.fullmatch(r"\[exit -?\d+\]", body[-1]):
        code = int(body[-1][6:-1])
        body = body[:-1]
    return Capture(cmd, body, code, raw, p)


# ---- line transforms (script.md "Conventions")
def hash12(s: str) -> str:
    """Every long sha256: digest shortened to its first 12 hex digits + '…' (Docker's short ID)."""
    return re.sub(r"(sha256:[0-9a-f]{12})[0-9a-f]{13,}", r"\1…", s)


def cut(s: str, after: str, ellipsis: str = "…") -> str:
    """The line cut right after `after` (first occurrence), ending in '…'."""
    i = s.index(after) + len(after)
    return s[:i] + ellipsis


def ask(s: str, bracket: str = "[Y/n]") -> str:
    """apt's / docker's question cut right after its bracket (the answer is typed separately)."""
    return s[:s.index(bracket) + len(bracket)]


def fit(s: str, width: int = 65) -> str:
    """A line of the compact build view: the padding before the right-hand column (a time, or
    'docker:default' on the first line) collapses to two spaces, and the step text is cut with '…'
    so that column stays visible."""
    m = re.match(r"^(.*?\S)\s{2,}(\S+)\s*$", s)
    if not m:
        return s if len(s) <= width else s[:width - 1] + "…"
    text, t = m.group(1), m.group(2)
    room = width - 2 - len(t)
    if len(text) > room:
        text = text[:room - 1] + "…"
    return f"{text}  {t}"


def _table(lines: list[str]):
    """Split a docker table by its header's column starts. -> (names, rows of cells, right_aligned)"""
    head = lines[0].rstrip()
    starts = [0] + [m.end() for m in re.finditer(r"\s{2,}", head)]
    ends = starts[1:] + [None]
    names = [head[a:b].strip() if b else head[a:].strip() for a, b in zip(starts, ends)]
    rows = []
    for ln in lines:
        rows.append([(ln[a:b] if b else ln[a:]).strip() for a, b in zip(starts, ends)])
    right = []
    for j, (a, b) in enumerate(zip(starts, ends)):
        hend = a + len(names[j])
        data = [ln for ln in lines[1:] if (ln[a:b] if b else ln[a:]).strip()]
        right.append(bool(data) and all(len(ln[:b].rstrip() if b else ln.rstrip()) == hend
                                        for ln in data))
    return names, rows, right


def _align(rows, right, gutter=2) -> list[str]:
    w = [max(len(r[j]) for r in rows) for j in range(len(rows[0]))]
    out = []
    for r in rows:
        cells = [(c.rjust(w[j]) if right[j] else c.ljust(w[j])) for j, c in enumerate(r)]
        out.append((" " * gutter).join(cells).rstrip())
    return out


def squeeze(lines: list[str], gutter: int = 2) -> list[str]:
    """A docker table re-aligned with two-space gutters; columns empty in every row are dropped
    (e.g. EXTRA). Numbers stay right-aligned under their header."""
    names, rows, right = _table(lines)
    keep = list(range(len(names)))
    if len(rows) > 1:
        keep = [j for j in keep if any(r[j] for r in rows[1:])]
    rows = [[r[j] for j in keep] for r in rows]
    return _align(rows, [right[j] for j in keep], gutter)


def cols(lines: list[str], names: list[str], gutter: int = 2) -> list[str]:
    """Only the named columns of a docker table (header row first), re-aligned."""
    heads, rows, right = _table(lines)
    idx = [heads.index(n) for n in names]
    return _align([[r[j] for j in idx] for r in rows], [right[j] for j in idx], gutter)


_DONE = ("Reading package lists...", "Building dependency tree...", "Reading state information...")


def plus_done(lines: list[str]) -> list[str]:
    """apt prints ' Done' after its three progress lines on a terminal (lost without one: ASSETS.md)."""
    return [s + " Done" if s in _DONE else s for s in lines]


# ------------------------------------------------------------------ sources
_DISPLAY = {"dot-gitignore.txt": ".gitignore"}
_LANG = {".py": "python", ".toml": "toml", ".sh": "bash", ".md": "markdown", ".yaml": "yaml"}


def source_text(name: str) -> str:
    return (SOURCE / name).read_text(encoding="utf-8")


def excerpt(name: str, first: int, last: int) -> str:
    """Lines first..last (1-based, inclusive) of a tutorial file in assets/source."""
    lines = source_text(name).split("\n")
    return "\n".join(lines[first - 1:last])


def code(name: str, first: int, last: int | None = None, language: str | None = None, focus=None,
         font_size: float = 22, width: float | None = None):
    """CODE(name: first–last) of script.md: a code_panel with header '<path> · lines a–b'.
    Dockerfile.txt -> docker; README.md -> markdown (pass 'docker'/'bash' for its code blocks).
    focus: 0-based lines of the excerpt to keep bright. .code .header"""
    last = first if last is None else last
    if language is None:
        language = "docker" if name.startswith("Dockerfile") else _LANG.get(Path(name).suffix, "text")
    path = _DISPLAY.get(name, name)
    return code_panel(excerpt(name, first, last), path, first, language, focus=focus,
                      font_size=font_size, width=width)


def readme_card(lines, body, quote: bool = False, card_w: float | None = None,
                size: float = 22) -> VGroup:
    """A GREY README card: header 'README.md · line n' (or 'lines a–b' for a tuple) and the README's
    own words (`body`: a string, '\\n' for new lines, or any mobject). quote=True draws a markdown
    quote bar. .frame .head .body"""
    where = f"line {lines}" if isinstance(lines, int) else f"lines {lines[0]}–{lines[1]}"
    head = VGroup(mono("README.md", CAPTION, S.GREY), label(f"· {where}", CAPTION, S.GREY))
    head.arrange(RIGHT, buff=0.12)
    if isinstance(body, str):
        body = VGroup(*[label(s, size, INK) for s in body.split("\n")]).arrange(DOWN, aligned_edge=LEFT,
                                                                               buff=0.12)
    content = body
    if quote:
        bar = Line(body.get_corner(UL) + np.array([-0.22, 0.04, 0]),
                   body.get_corner(DL) + np.array([-0.22, -0.04, 0]), color=S.GREY, stroke_width=4)
        content = VGroup(bar, body)
    inner = VGroup(head, content).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    frame = box(card_w or inner.width + 0.55, inner.height + 0.4, S.GREY, fill=S.GREY_DARKER,
                fill_opacity=1)
    inner.move_to(frame).align_to(frame, LEFT).shift(RIGHT * 0.28)
    g = VGroup(frame, inner)
    g.frame, g.head, g.body = frame, head, body
    return g


# ------------------------------------------------------------------ terminals
def term(prompt: str = P_LAPTOP, rows: int = 10, title: str | None = T_LAPTOP, width: float = 12.6,
         size: float = 22, place: bool = True) -> Terminal:
    """The house terminal (fixed size; it scrolls). place=True: centred, bottom edge at BOTTOM."""
    t = Terminal(prompt=prompt, width=width, rows=rows, size=size, title=title)
    if place:
        t.shift(np.array([-t.box.get_center()[0], BOTTOM - t.box.get_bottom()[1], 0]))
    return t


def laptop_term(rows: int = 10, prompt: str = P_LAPTOP) -> Terminal:
    return term(prompt, rows, T_LAPTOP)


def vm_term(rows: int = 10, prompt: str = P_VM) -> Terminal:
    return term(prompt, rows, T_VM)


def wide_term(rows: int = 10, prompt: str = P_LAPTOP, title: str = T_LAPTOP) -> Terminal:
    """13.2 wide at 20 pt (75 characters): only for the `ls` listings in columns."""
    return term(prompt, rows, title, width=13.2, size=20)


def resize(scene, t: Terminal, rows: int, keep=None, extra=(), run_time: float = 0.8) -> Terminal:
    """Grow or shrink terminal `t` to `rows` (bottom edge kept where it is). It keeps its last lines
    (at most `keep` of them), or, when `keep` is a list of line mobjects, exactly those lines.
    `extra`: animations to play at the same time (e.g. a picture moving into the freed room)."""
    title = t.title.text if t.title is not None else None
    ref = Terminal(prompt=t.prompt, width=t.box.width, rows=rows, size=t.size, title=title)
    ref.shift(np.array([t.box.get_center()[0] - ref.box.get_center()[0],
                        t.box.get_bottom()[1] - ref.box.get_bottom()[1], 0]))
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
        anims.append(ln.animate.shift(ref._slot(i) - ln.strut.get_corner(UL)))
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


def istep(scene, t: Terminal, line: str, type_time: float | None = None):
    """A typed line at a container prompt, from its capture ('root@01dca6d0f4d8:/# ls -a'): set the
    terminal's prompt to the capture's own, then type the rest."""
    prompt, typed = split_prompt(line)
    if prompt:
        t.set_prompt(prompt)
    return type_cmd(scene, t, typed, type_time)


def attach(scene, line, mob):
    """Make `mob` part of terminal row `line` (it scrolls with it). Re-adds the row, because
    animating a substring of a row splits it out of the scene's list."""
    scene.remove(mob)
    line.add(mob)
    scene.add(line)
    return mob


def pin(scene, line, mob, run_time: float = 0.4, anim=None):
    """Show `mob` beside a terminal line and make it part of that line."""
    scene.play(anim or FadeIn(mob, shift=LEFT * 0.1), run_time=run_time)
    return attach(scene, line, mob)


def unpin(scene, pairs, run_time: float = 0.3, *extra) -> None:
    """Fade out pinned marks [(line, mob), ...] and take them off their lines."""
    scene.play(*[FadeOut(m) for _, m in pairs], *extra, run_time=run_time)
    for line, m in pairs:
        if m in line.submobjects:
            line.remove(m)


def type_answer(scene, t: Terminal, ln, line_text: str, key: str, asked_at: float,
                pause: float = 0.6):
    """The answer keystroke after a question row `ln` (printed with text `line_text` at scene time
    `asked_at`, e.g. ask(...) of apt's '[Y/n]' line): waits until `pause` s after the question,
    then the key appears after it and flashes YELLOW. Returns the key glyph (part of the row)."""
    from manim import Indicate
    left = asked_at + pause - scene.renderer.time
    if left > 1 / 60:
        scene.wait(left)
    y = mono_line(line_text + " " + key, t.size, OUTPUT)
    y.shift(ln.strut.get_corner(UL) - y.strut.get_corner(UL))
    yg = y.glyphs[-1].set_color(TURN)
    scene.play(FadeIn(yg, scale=1.6), run_time=0.2)
    scene.play(Indicate(yg, color=TURN, scale_factor=1.8), run_time=0.5)
    scene.play(yg.animate.set_color(INK), run_time=0.2)
    attach(scene, ln, yg)
    return yg


def beside(mob, line, buff: float = 0.45, min_x: float | None = None):
    """Put `mob` right of terminal row `line`, centred on the row (left edge at least min_x)."""
    x = line.strut.get_right()[0] + buff
    if min_x is not None:
        x = max(x, min_x)
    return mob.move_to([x + mob.width / 2, line.strut.get_center()[1], 0])


def row_tag(parts, color=S.GREY, size: float = 20) -> VGroup:
    """A tag that fits inside one terminal row (the house tag is taller than a row).
    parts: a string, or (text, 'mono'|'label') pairs."""
    if isinstance(parts, str):
        parts = [(parts, "label")]
    t = VGroup(*[mono(x, size, color) if k == "mono" else label(x, size, color) for x, k in parts])
    t.arrange(RIGHT, buff=0.12)
    h = 0.36
    b = RoundedRectangle(width=t.width + 0.34, height=h, corner_radius=h / 2, stroke_color=color,
                         stroke_width=2).set_fill(S.BG, 0.92)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def under(g, color, stroke: float = 4, pad: float = 0.03, y: float | None = None) -> Line:
    """A line under glyphs `g` (at height y, default just under them)."""
    y = g.get_bottom()[1] - 0.06 if y is None else y
    return Line([g.get_left()[0] - pad, y, 0], [g.get_right()[0] + pad, y, 0], color=color,
                stroke_width=stroke)


def hl_bar(g, color=TURN, opacity: float = 0.25, buff: float = 0.05) -> Rectangle:
    """A translucent highlight bar behind glyphs `g` (add it behind: scene.add_to_back or
    bring the glyphs to front)."""
    return Rectangle(width=g.width + 2 * buff, height=g.height + 2 * buff, stroke_width=0) \
        .set_fill(color, opacity).move_to(g)


# ------------------------------------------------------------------ tags
def your_turn() -> VGroup:
    """YELLOW '▶ your turn' tag: next to a command the viewer should run now."""
    return tag("▶ your turn", TURN)


def extra_tag() -> VGroup:
    return tag("extra · not in the README", S.GREY)


def short_extra() -> VGroup:
    return tag("extra", S.GREY)


def illustration_tag(s: str = "illustration") -> VGroup:
    return tag(s, S.GREY)


def erratum_tag(s: str = "erratum") -> VGroup:
    return tag(s, S.GREY)


def expected_tag() -> VGroup:
    return tag("expected output", S.GREY)


def recorded_tag(s: str = "at the time of recording") -> VGroup:
    return tag(s, S.GREY)


def real_capture_tag(s: str = "real capture · 2026-10-13") -> VGroup:
    return tag(s, S.GREY)


def preview_tag(s: str = "preview · you'll run it in part 2") -> VGroup:
    return tag(s, S.GREY)


def cost_tag(s: str = "a VM costs money while it exists") -> VGroup:
    return tag(s, COST)


def stand_in_tag(first: str = "stand-in · local registry, not Docker Hub",
                 second: str = "watch only · don't type", size: float = TAG) -> VGroup:
    """Two-line GREY tag for every laptop-push/04–09 and 13 terminal. .box .lines"""
    lines = VGroup(label(first, size, S.GREY), label(second, size, S.GREY)).arrange(DOWN, buff=0.08)
    b = RoundedRectangle(width=lines.width + 0.45, height=lines.height + 0.24, corner_radius=0.2,
                         stroke_color=S.GREY, stroke_width=2).set_fill(S.BG, 0.92)
    lines.move_to(b)
    g = VGroup(b, lines)
    g.box, g.lines = b, lines
    return g


def user_caption(size: float = 22) -> VGroup:
    """YELLOW caption: '<USER NAME> = your Docker Hub username (here: student)'."""
    g = VGroup(mono("<USER NAME>", size, TURN), label("= your Docker Hub username (here:", size, TURN),
               mono("student", size, TURN), label(")", size, TURN))
    g.arrange(RIGHT, buff=0.1, aligned_edge=DOWN)
    g[3].shift(LEFT * 0.06)
    return g


# ------------------------------------------------------------------ small glyphs
def docker_chip(s: str = "docker", size: float = SMALL) -> VGroup:
    """The docker tool as a PURPLE mono chip (never a logo)."""
    return chip(s, TOOL, size=size, font=MONO)


def builder_box(s: str = "builder", box_w: float = 2.0, box_h: float = 1.0, size: float = 22) -> VGroup:
    """The PURPLE builder (BuildKit) box. .frame .text"""
    f = box(box_w, box_h, TOOL, fill_opacity=0.12)
    t = label(s, size, TOOL).move_to(f)
    g = VGroup(f, t)
    g.frame, g.text = f, t
    return g


def vm_glyph(glyph_w: float = 1.1, text: str = "VM", size: float = 20) -> VGroup:
    """A small BLUE VM: a box with two server slots and a label. .frame .text"""
    h = glyph_w * 0.72
    f = box(glyph_w, h, CLOUD, fill_opacity=0.12, radius=0.08)
    slots = VGroup(*[RoundedRectangle(width=glyph_w * 0.7, height=h * 0.14, corner_radius=0.03,
                                      stroke_color=CLOUD, stroke_width=1.5) for _ in range(2)])
    slots.arrange(DOWN, buff=h * 0.08).move_to(f).shift(UP * h * 0.18)
    t = label(text, size, CLOUD).next_to(slots, DOWN, buff=h * 0.06)
    g = VGroup(f, slots, t)
    g.frame, g.text = f, t
    return g


def mini_stack(fills=(SYSTEM, SYSTEM, LAPTOP, VENV), glyph_w: float = 0.8, slab_h: float = 0.13,
               gap: float = 0.03) -> VGroup:
    """A small image glyph: slabs bottom-up, TEAL outlines, fills by content. .slabs"""
    slabs = VGroup(*[Rectangle(width=glyph_w, height=slab_h, stroke_color=IMAGE, stroke_width=1.8)
                     .set_fill(c, 0.45) for c in fills])
    slabs.arrange(UP, buff=gap)
    g = VGroup(slabs)
    g.slabs = slabs
    return g


def shelf_glyph(glyph_w: float = 1.1) -> VGroup:
    """A small BLUE registry shelf (two boards, small image stacks), no text."""
    h = glyph_w * 0.8
    f = box(glyph_w, h, CLOUD, fill_opacity=0.08, radius=0.06)
    boards = VGroup(*[Line(LEFT * glyph_w * 0.42, RIGHT * glyph_w * 0.42, color=CLOUD, stroke_width=2)
                      .move_to(f).shift(DOWN * h * (0.35 - 0.45 * k)) for k in range(2)])
    stacks = VGroup()
    for b in boards:
        for x in (-0.22, 0.12):
            s = mini_stack((SYSTEM, VENV), glyph_w * 0.22, h * 0.09, 0.015)
            s.move_to(b.get_center() + RIGHT * x * glyph_w, aligned_edge=DOWN)
            stacks.add(s)
    return VGroup(f, boards, stacks)


def lock_glyph(lock_h: float = 0.32, color=S.GREY) -> VGroup:
    """A padlock (read-only, a token, a socket door)."""
    w = lock_h * 0.8
    body = RoundedRectangle(width=w, height=lock_h * 0.6, corner_radius=lock_h * 0.08,
                            stroke_color=color, stroke_width=2.5).set_fill(color, 0.3)
    shackle = Arc(radius=w * 0.32, start_angle=0, angle=np.pi, color=color, stroke_width=3)
    shackle.next_to(body, UP, buff=0)
    return VGroup(shackle, body)


def fingerprint(r: float = 0.17, color=IMAGE) -> VGroup:
    """A small fingerprint badge (the cache key of a build step)."""
    disc = Circle(radius=r, stroke_color=color, stroke_width=2.5).set_fill(S.BG, 1)
    arcs = VGroup(*[Arc(radius=r * k, start_angle=0.5 + k, angle=np.pi * 1.25, stroke_color=color,
                        stroke_width=1.8) for k in (0.25, 0.45, 0.65)])
    return VGroup(disc, arcs)


def sticky(s: str, color=IMAGE, size: float = 20) -> VGroup:
    """A sticky note (an image name / tag): mono text on a note with a folded corner. .note .text"""
    t = mono(s, size, INK)
    w, h, c = t.width + 0.4, t.height + 0.32, 0.14
    note = Polygon([-w / 2, h / 2, 0], [w / 2 - c, h / 2, 0], [w / 2, h / 2 - c, 0], [w / 2, -h / 2, 0],
                   [-w / 2, -h / 2, 0], stroke_color=color, stroke_width=2.5).set_fill(color, 0.16)
    t.move_to(note)
    g = VGroup(note, t)
    g.note, g.text = note, t
    return g


def route(a, b, arc: float = -0.5, color=ROUTE, stroke: float = 4) -> Arrow:
    """A PINK route (an arrow, curved by `arc` radians) from a to b (points or mobjects)."""
    pa = a if isinstance(a, np.ndarray) else a.get_center()
    pb = b if isinstance(b, np.ndarray) else b.get_center()
    return Arrow(pa, pb, buff=0.15 if not isinstance(a, np.ndarray) else 0, path_arc=arc, color=color,
                 stroke_width=stroke, tip_length=0.2, max_tip_length_to_length_ratio=0.2)


def travel(mob, path, run_time: float = 1.2):
    """Animation: `mob` rides along `path` (e.g. a route())."""
    return MoveAlongPath(mob, path, run_time=run_time)


def bounce(mob, point, run_time: float = 0.9):
    """Animation: `mob` goes to `point` and comes back (an 'already exists' bounce)."""
    back = mob.get_center().copy()
    return Succession(mob.animate(run_time=run_time * 0.5).move_to(point),
                      mob.animate(run_time=run_time * 0.5).move_to(back))


def figure(word: str = "python", color=ROUTE, size: float = 24) -> VGroup:
    """L1's walking command: a small PINK figure carrying a word. .person .word"""
    p = person_icon(color, 0.42)
    w = mono(word, size, color)
    g = VGroup(p, w).arrange(RIGHT, buff=0.1, aligned_edge=DOWN)
    g.person, g.word = p, w
    return g


def project_tree(entries=None, size: float = 20, new: str | None = None):
    """The clone as a file tree (GREY files, BLUE folders): REPO_ENTRIES under 'simple-translate/'.
    new='Dockerfile' adds that row (YELLOW). .row(name)"""
    entries = list(REPO_ENTRIES if entries is None else entries)
    if new:
        entries.append(new)
        entries.sort()                      # `ls -a` order in the C locale (dotfiles, capitals first)
    rows = ["simple-translate/"] + ["  " + e for e in entries]
    colors = {new: TURN} if new else None
    return file_tree(rows, size=size, colors=colors)


def outline_box(box_w: float, box_h: float, color, solid: bool = False, fill_opacity: float = 0.1,
                radius: float = 0.14, stroke: float = 2.5) -> VGroup:
    """A box whose outline is made of dashes: dashed (solid=False, no fill) or closed (solid=True,
    gaps of zero width, faint fill). A dashed one Transforms cleanly into a solid one of the same
    size: the dashes grow together (something absent becoming real). .fill .frame"""
    r = RoundedRectangle(width=box_w, height=box_h, corner_radius=min(radius, box_h / 2, box_w / 2))
    n = max(12, int((box_w + box_h) * 7))
    frame = DashedVMobject(r.copy(), num_dashes=n, dashed_ratio=0.999 if solid else 0.55)
    frame.set_stroke(color, stroke)
    fill = r.copy().set_stroke(width=0).set_fill(color, fill_opacity if solid else 0)
    g = VGroup(fill, frame)
    g.fill, g.frame = fill, frame
    return g


# ------------------------------------------------------------------ V1 · the ladder (S01)
LADDER = [("Manual install on the VM", SYSTEM), ("Same VM, but with uv", VENV),
          ("Docker, on your laptop", IMAGE), ("Run the Docker image on a VM", IMAGE)]


class Ladder(VGroup):
    """V1 · README.md lines 9-16: four rungs, rung 1 at the bottom, each dim at first.
        lad = Ladder()                     # .rungs[i] (0-based) .veils[i] .header .rails
        self.play(lad.light(0, 0.6), lad.light(1, 0.6))   # soft; lad.light(2) fully lit
    Rung 3 carries a TEAL box in a GREY laptop, rung 4 a TEAL box in a BLUE VM (.icons[i])."""

    def __init__(self, rung_w: float = 7.6, rung_h: float = 0.66, gap: float = 0.26, size: float = 24,
                 **kw):
        super().__init__(**kw)
        self.rungs, self.veils, self.icons = VGroup(), VGroup(), {}
        for i, (text, col) in enumerate(LADDER):
            f = box(rung_w, rung_h, col, fill_opacity=0.14, radius=0.12)
            n = label(str(i + 1), size, col).move_to(f.get_left() + RIGHT * 0.35)
            t = label(text, size, INK).next_to(n, RIGHT, buff=0.3)
            r = VGroup(f, n, t)
            if i >= 2:
                inner = RoundedRectangle(width=0.32, height=0.22, corner_radius=0.04, stroke_color=IMAGE,
                                         stroke_width=2).set_fill(IMAGE, 0.4)
                if i == 2:
                    host = laptop(0.75, LAPTOP)
                    inner.move_to(host.screen)
                else:
                    host = box(0.75, 0.5, CLOUD, fill_opacity=0.15, radius=0.06)
                    inner.move_to(host)
                ic = VGroup(host, inner).move_to(f.get_right() + LEFT * 0.6)
                r.add(ic)
                self.icons[i] = ic
            r.shift(UP * i * (rung_h + gap))
            self.rungs.add(r)
            veil = Rectangle(width=rung_w + 0.04, height=rung_h + 0.04, stroke_width=0) \
                .set_fill(S.BG, 0.72).move_to(f)
            self.veils.add(veil)
        rail_x = rung_w / 2 + 0.25
        top = self.rungs.get_top()[1] + 0.2
        bot = self.rungs.get_bottom()[1] - 0.2
        self.rails = VGroup(*[Line([s * rail_x, bot, 0], [s * rail_x, top, 0], color=S.GREY_DARK,
                                   stroke_width=5) for s in (-1, 1)])
        self.header = VGroup(mono("README.md", CAPTION, S.GREY), label("· lines 9–16", CAPTION, S.GREY))
        self.header.arrange(RIGHT, buff=0.12).next_to(self.rails, UP, buff=0.15).align_to(self.rails, LEFT)
        self.add(self.rails, self.rungs, self.veils, self.header)

    def light(self, i: int, level: float = 1.0, run_time: float = 0.5):
        """Animation: rung i at `level` (1 lit, 0.6 soft, 0 dim)."""
        return self.veils[i].animate(run_time=run_time).set_fill(S.BG, 0.72 * (1 - level))


# ------------------------------------------------------------------ V1 · L1's nest (S02, S16)
class Nest(VGroup):
    """L1's closing picture: a BLUE VM box holding a GREEN venv box. .vm .venv
    S16: self.play(FadeIn(slot := nest.slot())); self.play(ReplacementTransform(slot, sol := nest.solid()))
         self.play(nest.venv.animate.move_to(nest.venv_spot()), FadeIn(nest.venv_label()))
    slot() and solid() have the same structure (outline_box + steady label), so the dashes close up."""

    def __init__(self, vm_w: float = 5.2, vm_h: float = 3.0, size: float = 22, **kw):
        super().__init__(**kw)
        frame = box(vm_w, vm_h, CLOUD, fill_opacity=0.06)
        title = label("VM", size, CLOUD).move_to(frame.get_corner(UL) + np.array([0.45, -0.3, 0]))
        self.vm = VGroup(frame, title)
        self.vm.frame, self.vm.title = frame, title
        vf = box(1.6, 0.9, VENV, fill_opacity=0.15)
        vt = label("venv", size, VENV).move_to(vf)
        self.venv = VGroup(vf, vt)
        self.venv.move_to(frame.get_center() + LEFT * vm_w * 0.27 + DOWN * 0.15)
        self.size = size
        self.add(self.vm, self.venv)

    def _cbox(self):
        f = self.vm.frame
        return f.get_center() + RIGHT * f.width * 0.18 + DOWN * 0.15, f.width * 0.5, f.height * 0.68

    def slot(self) -> VGroup:
        """The dashed GREY 'container · L2' box between VM and venv (not added)."""
        c, w, h = self._cbox()
        fr = outline_box(w, h, S.GREY).move_to(c)
        t = steady("container · L2", 20, S.GREY).move_to(fr.get_top() + DOWN * 0.3)
        return VGroup(fr, t)

    def solid(self) -> VGroup:
        """The same box, solid TEAL 'container' (not added)."""
        c, w, h = self._cbox()
        fr = outline_box(w, h, IMAGE, solid=True).move_to(c)
        t = steady("container", 20, IMAGE).move_to(fr.get_top() + DOWN * 0.3)
        return VGroup(fr, t)

    def venv_spot(self) -> np.ndarray:
        """Where the venv's centre goes inside the container."""
        c, w, h = self._cbox()
        return c + UP * 0.02

    def venv_label(self) -> Text:
        """'/.venv' under the venv's spot, inside the container (not added)."""
        return steady("/.venv", 20, VENV, mono_font=True).next_to(self.venv_spot(), DOWN, buff=0.55)


# ------------------------------------------------------------------ V2 · the layer stack
class Slab(VGroup):
    """One image layer: a translucent slab with a TEAL outline, filled by what it holds.
        Slab("RUN uv sync", VENV, slab_w=3.4, slab_h=0.8)  -> .box .text (mono, None if no text)
    Labels are the short Dockerfile line (<= 19 characters at 20 pt in a 3.4-wide slab)."""

    def __init__(self, text: str | None = None, fill=SYSTEM, slab_w: float = 3.4, slab_h: float = 0.46,
                 size: float = 20, dashed: bool = False, text_color=INK, **kw):
        super().__init__(**kw)
        self.fill_hex, self.slab_w, self.slab_h, self.size = fill, slab_w, slab_h, size
        r = RoundedRectangle(width=slab_w, height=slab_h, corner_radius=min(0.06, slab_h / 2.5),
                             stroke_color=IMAGE, stroke_width=2.5).set_fill(fill, 0.35)
        if dashed:
            r = DashedVMobject(r.set_fill(fill, 0), num_dashes=40, dashed_ratio=0.55).set_stroke(IMAGE, 2.5)
        self.box = r
        self.add(r)
        self.text = None
        if text:
            self.text = steady(text, size, text_color, mono_font=True).move_to(r)
            self.add(self.text)


def mb_height(mb: float, k: float = 0.08, lo: float = 0.1) -> float:
    """A slab height for `mb` megabytes (square-root scale, so 16 kB and 125 MB both fit)."""
    return max(lo, k * np.sqrt(mb))


class LayerStack(VGroup):
    """V2 · an image as read-only layers, bottom-up, standing on .floor (an invisible line; move
    the stack and the floor moves with it).
        st = LayerStack().move_to([-3.2, -1.0, 0])         # empty; place it first
        base = [st.make(None, SYSTEM, 0.15) for _ in range(4)]
        st.drop(self, *base)                              # they fall in together and join .slabs
        br = st.brace(base, "base image")                  # Brace + label (not added)
        uv = st.make("RUN pip install uv", SYSTEM)
        st.drop(self, uv, anim=TransformFromCopy(code_line, uv))
        self.play(*st.restack([0.83, 0.28, 0.66, 0.1, 0.89, 0.1, 1.0]))   # S10: new heights
    """

    def __init__(self, stack_w: float = 3.4, size: float = 20, gap: float = 0.04, **kw):
        super().__init__(**kw)
        self.stack_w, self.size, self.gap = stack_w, size, gap
        self.floor = Line(LEFT * stack_w / 2, RIGHT * stack_w / 2, stroke_width=0)
        self.slabs = VGroup()
        self._pending: list[Slab] = []
        self.add(self.floor, self.slabs)

    def top_y(self) -> float:
        tops = [s.box.get_top()[1] for s in [*self.slabs, *self._pending]]
        return max(tops) if tops else self.floor.get_center()[1] - self.gap

    def make(self, text: str | None, fill=SYSTEM, slab_h: float = 0.46, dashed: bool = False) -> Slab:
        """A slab placed where it will land (on top of the stack and of slabs made before it)."""
        s = Slab(text, fill, self.stack_w, slab_h, self.size, dashed)
        c = self.floor.get_center()
        s.move_to([c[0], self.top_y() + self.gap + slab_h / 2, 0])
        self._pending.append(s)
        return s

    def accept(self, scene, *slabs) -> None:
        """Make slabs (already shown in the scene) part of the stack."""
        for s in slabs:
            if s in self._pending:
                self._pending.remove(s)
            scene.remove(s)
            self.slabs.add(s)
        scene.add(self)

    def drop(self, scene, *slabs, anim=None, height: float = 1.0, run_time: float = 0.8,
             extra=()) -> list:
        """Play the slabs landing (default: fall in from `height` above, staggered; or `anim`),
        with `extra` animations, then make them part of the stack. Returns the slabs."""
        a = anim or LaggedStart(*[FadeIn(s, shift=DOWN * height) for s in slabs], lag_ratio=0.15)
        scene.play(a, *extra, run_time=run_time)
        self.accept(scene, *slabs)
        return list(slabs)

    def brace(self, slabs, text: str, direction=LEFT, size: float = 20, color=S.GREY) -> VGroup:
        """A brace beside `slabs` with a label (not added). .brace .text"""
        g = VGroup(*[s.box for s in slabs])
        b = Brace(g, direction=direction, color=color, buff=0.12)
        t = label(text, size, color).next_to(b, direction, buff=0.12)
        out = VGroup(b, t)
        out.brace, out.text = b, t
        return out

    def restack(self, heights: list[float]) -> list:
        """Animations: every slab (bottom-up) takes its new height; the floor stays. A slab too thin
        for its text moves the text just left of the stack (right-aligned)."""
        anims, y = [], self.floor.get_center()[1]
        x = self.floor.get_center()[0]
        for s, h in zip(self.slabs, heights):
            nb = RoundedRectangle(width=self.stack_w, height=h, corner_radius=min(0.06, h / 2.5),
                                  stroke_color=IMAGE, stroke_width=2.5).set_fill(s.fill_hex, 0.35)
            nb.move_to([x, y + self.gap + h / 2, 0])
            anims.append(Transform(s.box, nb))
            if s.text is not None:
                if h >= s.text.height + 0.12:
                    anims.append(s.text.animate.move_to(nb))
                else:
                    tgt = nb.get_left() + LEFT * (0.15 + s.text.width / 2)
                    anims.append(s.text.animate.move_to(tgt))
            s.slab_h = h
            y += self.gap + h
        return anims


class Glass(VGroup):
    """V2 · a container's thin writable layer: a dashed, glowing TEAL glass slab with a process dot.
        g = Glass(process="PID 1 · bash").on(stack)       # sits on top of a LayerStack
        self.play(FadeIn(g)) ... self.play(g.stop()) ... self.play(g.dissolve())
    .slab .glow .text .dot .dot_label (the label sits above the slab's right end)"""

    def __init__(self, glass_w: float = 3.4, glass_h: float = 0.48, process: str | None = "main process",
                 text: str = "writable layer", size: float = 20, **kw):
        super().__init__(**kw)
        self.glass_w, self.glass_h, self.size = glass_w, glass_h, size
        base = RoundedRectangle(width=glass_w, height=glass_h, corner_radius=0.08)
        self.glow = base.copy().set_stroke(IMAGE, 10, opacity=0.25).set_fill(IMAGE, 0.08)
        self.slab = DashedVMobject(base.copy().set_stroke(IMAGE, 2.5), num_dashes=44, dashed_ratio=0.6)
        self.text = steady(text, size, IMAGE).move_to(base).align_to(base, LEFT).shift(RIGHT * 0.2)
        self.add(self.glow, self.slab, self.text)
        self.dot = self.dot_label = None
        if process:
            self.dot = Dot(radius=0.09, color=IMAGE).move_to(base.get_right() + LEFT * 0.3)
            self.dot_label = steady(process, size, IMAGE).next_to(base, UP, buff=0.1).align_to(base, RIGHT)
            self.add(self.dot, self.dot_label)

    def on(self, stack: LayerStack, gap: float | None = None) -> "Glass":
        g = stack.gap if gap is None else gap
        c = stack.floor.get_center()
        self.shift(np.array([c[0], stack.top_y() + g + self.glass_h / 2, 0]) - self.slab.get_center())
        return self

    def stop(self, note: str = "stopped", run_time: float = 0.5):
        """Animation: the process dot goes out (GREY), its label becomes `note`."""
        anims = []
        if self.dot is not None:
            anims.append(self.dot.animate.set_color(S.GREY_DARK))
            new = steady(note, self.size, S.GREY).move_to(self.dot_label, aligned_edge=RIGHT)
            anims.append(Transform(self.dot_label, new))
        return AnimationGroup(*anims, run_time=run_time)

    def dissolve(self, run_time: float = 0.7):
        """Animation: the whole container top fades away upward (--rm)."""
        return FadeOut(self, shift=UP * 0.3, run_time=run_time)


# ------------------------------------------------------------------ V2/V3 · the config card
class Tile(VGroup):
    """A value on the config card: mono text in a rounded TEAL box. .frame .text .value"""

    def __init__(self, s: str, color=IMAGE, dashed: bool = False, size: float = 20, **kw):
        super().__init__(**kw)
        t = steady(s, size, INK, mono_font=True)
        f = RoundedRectangle(width=t.width + 0.3, height=t.height + 0.2, corner_radius=0.08,
                             stroke_color=color, stroke_width=2.2).set_fill(color, 0.18)
        if dashed:
            f = DashedVMobject(f.set_fill(color, 0), num_dashes=30, dashed_ratio=0.55).set_stroke(color, 2.2)
        t.move_to(f)
        self.frame, self.text, self.value = f, t, s
        self.add(f, t)


class ConfigCard(VGroup):
    """V2/V3 · the image's config card (TEAL): one row per key, a slot for a value tile.
        card = ConfigCard(["ENTRYPOINT", "CMD", "WorkingDir"])
        t = card.place("CMD", card.tile('["python3"]'))     # positioned; animate it in yourself
        card.put(self, "ENTRYPOINT", card.tile('["/bin/bash"]'))   # plays a slide-in, records it
        card.take(self, "CMD")                               # falls off and fades
        ln = card.startup("/bin/bash")                       # the start-up line under the card
        self.play(FadeOut(card.everything()))
    .frame .title .keys[row] .slots[row] .tiles[row] .notes[row] .line
    Stacked layout (key above slot) below card_w 6.0, key and slot on one line from 6.0 up."""

    def __init__(self, rows=("ENTRYPOINT", "CMD", "WorkingDir"), card_w: float = 3.6,
                 title: str = "config", size: float = 20, inline: bool | None = None, **kw):
        super().__init__(**kw)
        self.card_w, self.size = card_w, size
        inline = card_w >= 6.0 if inline is None else inline
        self.title = label(title, 22, IMAGE)
        self.keys, self.slots, self.tiles, self.notes = {}, {}, {}, {}
        rows_g = VGroup()
        slot_h = mono("|", size).height + 0.22
        key_w = max(mono(r, size).width for r in rows) if rows else 0
        for r in rows:
            k = mono(r, size, S.GREY)
            if inline:
                sw = card_w - key_w - 0.75
                sl = RoundedRectangle(width=sw, height=slot_h, corner_radius=0.08, stroke_color=S.GREY_DARK,
                                      stroke_width=1.5)
                k.move_to(ORIGIN, aligned_edge=LEFT)
                sl.move_to([key_w + 0.2 + sw / 2, 0, 0])
                row = VGroup(k, sl)
            else:
                sl = RoundedRectangle(width=card_w - 0.4, height=slot_h, corner_radius=0.08,
                                      stroke_color=S.GREY_DARK, stroke_width=1.5)
                k.next_to(sl, UP, buff=0.06).align_to(sl, LEFT).shift(RIGHT * 0.05)
                row = VGroup(k, sl)
            self.keys[r], self.slots[r] = k, sl
            rows_g.add(row)
        rows_g.arrange(DOWN, buff=0.14 if inline else 0.16, aligned_edge=LEFT)
        body = VGroup(self.title, rows_g).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        self.frame = box(card_w, body.height + 0.45, IMAGE, fill_opacity=0.06)
        body.move_to(self.frame).align_to(self.frame, LEFT).shift(RIGHT * 0.2)
        self.rows_g = rows_g
        self.line = None
        self.add(self.frame, self.title, rows_g)

    def tile(self, s: str, color=IMAGE, dashed: bool = False) -> Tile:
        return Tile(s, color, dashed, self.size)

    def _spot(self, row: str, tile) -> np.ndarray:
        sl = self.slots[row]
        return sl.get_left() + RIGHT * (0.08 + tile.width / 2)

    def place(self, row: str, tile: Tile) -> Tile:
        """Position `tile` in the slot of `row` (left-aligned) and record it. Not added."""
        tile.move_to(self._spot(row, tile))
        self.tiles[row] = tile
        return tile

    def put(self, scene, row: str, tile: Tile, anim=None, run_time: float = 0.6, extra=()) -> Tile:
        """Play the tile into its slot (default: it slides there from where it is; pass anim= for
        e.g. TransformFromCopy(src, card.place(row, tile))) and record it."""
        if anim is None:
            if tile not in scene.mobjects:
                scene.add(tile)
            anim = tile.animate.move_to(self._spot(row, tile))
        scene.play(anim, *extra, run_time=run_time)
        self.tiles[row] = tile
        return tile

    def take(self, scene, row: str, run_time: float = 0.6, extra=()) -> None:
        """The tile of `row` falls off the card and fades."""
        t = self.tiles.pop(row)
        scene.play(FadeOut(t, shift=DOWN * 0.6), *extra, run_time=run_time)

    def note(self, row: str, s: str, color=S.GREY) -> Text:
        """GREY mono text in the slot (e.g. 'null', '""'), recorded in .notes. Not added."""
        t = steady(s, self.size, color, mono_font=True)
        t.move_to(self._spot(row, t))
        self.notes[row] = t
        return t

    def startup(self, s: str, color=INK, size: float = 22, buff: float = 0.3) -> Text:
        """The command line the container will run, in mono under the card (recorded as .line;
        Transform the old line into a new one to update it). Not added."""
        t = steady(s, size, color, mono_font=True).next_to(self.frame, DOWN, buff=buff)
        self.line = t
        return t

    def everything(self) -> VGroup:
        """The card with its tiles, notes and start-up line (to move or fade together)."""
        g = VGroup(self, *self.tiles.values(), *self.notes.values())
        if self.line is not None:
            g.add(self.line)
        return g


# ------------------------------------------------------------------ V4 · Python versions (L1)
class VersionLine(VGroup):
    """Python 3.x versions on a number line (positions by MINOR version: 12 means 3.12), with the
    `>= 3.lo` interval glowing GREEN and running off the right end. The band's label sits
    `label_buff` (1.0) above the band, clear of dot2() labels above the line (L1 used 0.3).
        vl = VersionLine(10, 16, lo=13, line_w=11.0)
        d = vl.dot2(12, "3.12.15", "base image", SYSTEM)      # dot + two-line label above
    .axis .ticks .band .band_label"""

    def __init__(self, first: int = 10, last: int = 16, lo: int = 13, line_w: float = 11.0,
                 size: float = 22, label_buff: float = 1.0, **kw):
        super().__init__(**kw)
        self.first, self.last, self.lo, self.line_w = first, last, lo, line_w
        self.axis = Line(LEFT * line_w / 2, RIGHT * line_w / 2, color=S.GREY, stroke_width=3)
        self.ticks = VGroup()
        for m in range(first, last + 1):
            x = self._x(m)
            self.ticks.add(VGroup(Line([x, -0.12, 0], [x, 0.12, 0], color=S.GREY, stroke_width=2),
                                  mono(f"3.{m}", size, S.GREY).move_to([x, -0.45, 0])))
        right = line_w / 2 + 0.25
        self.band = Rectangle(width=right - self._x(lo), height=0.3, stroke_width=0).set_fill(VENV, 0.3)
        self.band.move_to([(self._x(lo) + right) / 2, 0, 0])
        self.band_label = mono(f'requires-python = ">=3.{lo}"', size, VENV)
        self.band_label.next_to(self.band, UP, buff=label_buff).align_to(self.band, LEFT)
        self.add(self.band, self.axis, self.ticks, self.band_label)

    def _x(self, minor: float) -> float:
        return -self.line_w / 2 + (minor - self.first + 0.5) / (self.last - self.first + 1) * self.line_w

    def point(self, minor: float, dy: float = 0.0):
        """A point on the (possibly moved) axis above minor version `minor`."""
        left = self.axis.get_start()
        return left + np.array([self._x(minor) + self.line_w / 2, dy, 0])

    def dot(self, minor: float, text: str, color, above: bool = True, size: float = 22) -> VGroup:
        """L1's dot with a one-line label. .dot .text"""
        d = Dot(self.point(minor), radius=0.11, color=color)
        t = mono(text, size, color)
        t.next_to(d, UP if above else DOWN, buff=0.3 if above else 0.75)
        g = VGroup(d, t)
        g.dot, g.text = d, t
        return g

    def dot2(self, minor: float, top: str, bottom: str, color, above: bool = True,
             size: float = 20, buff: float = 0.32) -> VGroup:
        """A dot with a two-line label: the version (mono, in its colour) over a 2-3 word role
        (GREY). Above the line, or below it (clear of the tick labels). .dot .top .bottom .text"""
        d = Dot(self.point(minor), radius=0.11, color=color)
        a = mono(top, size, color)
        b = label(bottom, size, S.GREY)
        t = VGroup(a, b).arrange(DOWN, buff=0.08)
        t.next_to(d, UP if above else DOWN, buff=buff if above else 0.75)
        g = VGroup(d, t)
        g.dot, g.top, g.bottom, g.text = d, a, b, t
        return g


# ------------------------------------------------------------------ V4 · PATH doors (L1)
class PathDoors(VGroup):
    """PATH as a row of doors (left = searched first). Each door: frame + label underneath.
        doors = PathDoors(["/usr/local/bin", "/usr/local/sbin", "…"], colors={"/usr/local/bin": SYSTEM})
        w = doors.knock(scene, "python", found=0)       # walks along, enters door 0
        doors.insert_front(scene, "/.venv/bin", VENV)   # a new door slides in at the left
    Each door: .frame .label .dir .door_color"""

    def __init__(self, dirs: list[str], colors: dict | None = None, door_w: float = 0.9,
                 door_h: float = 1.3, gap: float = 0.45, size: float = 20, **kw):
        super().__init__(**kw)
        self.door_w, self.door_h, self.gap, self.size = door_w, door_h, gap, size
        colors = colors or {}
        self.doors = VGroup(*[self._door(d, colors.get(d, S.GREY)) for d in dirs])
        self.doors.arrange(RIGHT, buff=gap, aligned_edge=UP)
        self.add(self.doors)

    def _door(self, d: str, color) -> VGroup:
        t = mono(d, self.size, color)
        w = max(self.door_w, t.width + 0.2) if d != "…" else self.door_w * 0.6
        frame = RoundedRectangle(width=w, height=self.door_h, corner_radius=0.06,
                                 stroke_color=color, stroke_width=3).set_fill(color, 0.1)
        knob = Dot(radius=0.045, color=color).move_to(frame.get_right() + LEFT * 0.16)
        t.next_to(frame, DOWN, buff=0.12)
        g = VGroup(frame, knob, t)
        g.frame, g.label, g.dir, g.door_color = frame, t, d, color
        return g

    def knock(self, scene, word: str, found: int | None, step_time: float = 0.45, color=ROUTE):
        """`word` appears above the first door and walks right, pausing at each door; it enters
        door `found` (the door lights up) or, with None, ends on a RED 'command not found' under
        the row (w.not_found). Returns the word."""
        w = mono(word, 24, color)
        w.next_to(self.doors[0].frame, UP, buff=0.15)
        scene.play(FadeIn(w, shift=DOWN * 0.2), run_time=0.3)
        stop = found if found is not None else len(self.doors) - 1
        for i in range(1, stop + 1):
            scene.play(w.animate.next_to(self.doors[i].frame, UP, buff=0.15), run_time=step_time)
        if found is not None:
            scene.play(w.animate.move_to(self.doors[found].frame).scale(0.85),
                       self.doors[found].frame.animate.set_fill(self.doors[found].door_color, 0.35),
                       run_time=0.4)
        else:
            nf = label("command not found", 24, ERR).next_to(self.doors, DOWN, buff=0.3)
            scene.play(w.animate.set_color(ERR), FadeIn(nf), run_time=0.4)
            w.not_found = nf
        return w

    def insert_front(self, scene, d: str, color, run_time: float = 0.8) -> VGroup:
        """Slide a new door in at the left; the others make room."""
        new = self._door(d, color)
        first = self.doors[0]
        shift = RIGHT * (new.frame.width + self.gap)
        new.align_to(first.frame, UP).align_to(first.frame, LEFT).shift(UP * 2.0)
        scene.play(self.doors.animate.shift(shift), run_time=run_time * 0.5)
        scene.play(new.animate.shift(DOWN * 2.0), run_time=run_time * 0.5)
        scene.remove(new)
        self.doors.submobjects.insert(0, new)
        scene.add(self)
        return new

    def remove_front(self, scene, run_time: float = 0.8) -> None:
        old = self.doors[0]
        w = old.frame.width + self.gap
        scene.play(old.animate.shift(UP * 2.0).set_opacity(0), run_time=run_time * 0.5)
        self.doors.remove(old)
        scene.remove(old)
        scene.play(self.doors.animate.shift(LEFT * w), run_time=run_time * 0.5)


# ------------------------------------------------------------------ V5 · the build cache
class _Topple(Rotate):
    """Rotate a domino about its bottom-right corner and recolour it on the way."""

    def __init__(self, mob, angle, color, **kw):
        self.to_color = color
        super().__init__(mob, angle=angle, about_point=mob.get_corner(DR), **kw)

    def create_target(self):
        t = super().create_target()
        t.set_fill(self.to_color, 0.6).set_stroke(self.to_color)
        return t


class CacheChain(VGroup):
    """V5 · the build steps as boxes in a row, each with a fingerprint badge above it (its cache
    key) and a domino under it.
        ch = CacheChain(["[1/4] FROM", "[2/4] RUN apt…uv", "[3/4] COPY . ./", "[4/4] RUN uv sync"])
        self.play(FadeIn(ch.feeds(2)))                    # parent + instruction arrows into badge 2
        self.play(FadeIn(ch.stamp(1, "CACHED"), scale=1.3))
        self.play(ch.badge(2, ERR)); self.play(ch.topple(2))   # RED wave from box 2 to the end
        self.play(ch.stand_up(), FadeOut(VGroup(*ch.stamps.values())))
    A step '[k/n] INSTR' prints '[k/n]' GREY over the instruction; '\\n' in INSTR breaks it.
    .boxes[i] (.frame .text) .badges[i] .dominoes[i] .stamps{i: mobject}"""

    def __init__(self, steps: list[str], box_h: float = 0.95, min_w: float = 1.9, gap: float = 0.38,
                 size: float = 20, domino_h: float = 0.62, **kw):
        super().__init__(**kw)
        self.size = size
        self.boxes, self.badges, self.dominoes = VGroup(), VGroup(), VGroup()
        self.stamps: dict[int, VGroup] = {}
        for st in steps:
            m = re.match(r"^(\[\d+/\d+\])\s+(.*)$", st, re.S)
            parts = [mono(m.group(1), size, S.GREY)] if m else []
            body = m.group(2) if m else st
            parts += [mono(x, size, INK) for x in body.split("\n")]
            txt = VGroup(*parts).arrange(DOWN, buff=0.08)
            w = max(min_w, txt.width + 0.4)
            h = max(box_h, txt.height + 0.3)
            f = RoundedRectangle(width=w, height=h, corner_radius=0.1, stroke_color=S.GREY,
                                 stroke_width=2.5).set_fill(PANEL, 1)
            txt.move_to(f)
            b = VGroup(f, txt)
            b.frame, b.text = f, txt
            self.boxes.add(b)
        self.boxes.arrange(RIGHT, buff=gap, aligned_edge=DOWN)
        top = max(b.get_top()[1] for b in self.boxes)
        for b in self.boxes:
            fp = fingerprint().move_to([b.get_center()[0], top + 0.47, 0])
            self.badges.add(fp)
            d = Rectangle(width=0.22, height=domino_h, stroke_color=S.GREY, stroke_width=2).set_fill(S.GREY, 0.45)
            d.next_to(b, DOWN, buff=0.55)
            self.dominoes.add(d)
        self._fallen: set[int] = set()
        self.add(self.boxes, self.badges, self.dominoes)

    def feeds(self, i: int, color=IMAGE) -> VGroup:
        """Thin arrows into badge i: from the previous box (its parent) and from box i's own text
        (its instruction). Not added."""
        bd = self.badges[i]
        arrows = VGroup()
        kw = dict(buff=0.06, stroke_width=2.5, tip_length=0.12, max_tip_length_to_length_ratio=0.35,
                  color=color)
        if i > 0:
            arrows.add(Arrow(self.boxes[i - 1].frame.get_corner(UR) + LEFT * 0.15, bd.get_left(), **kw))
        arrows.add(Arrow(self.boxes[i].frame.get_top(), bd.get_bottom(), **kw))
        return arrows

    def badge(self, i: int, color, run_time: float = 0.4):
        """Animation: badge i turns `color` (RED: it no longer matches)."""
        return self.badges[i].animate(run_time=run_time).set_stroke(color)

    def stamp(self, i: int, s: str = "CACHED", color=IMAGE, size: float = 20) -> VGroup:
        """A stamp tilted over the gap under box i (recorded in .stamps). Not added."""
        t = tag(s, color, size).rotate(0.1)
        t.move_to((self.boxes[i].frame.get_bottom() + self.dominoes[i].get_top()) / 2)
        self.stamps[i] = t
        return t

    def topple(self, a: int, b: int | None = None, color=ERR, lag: float = 0.35,
               angle: float = -1.25, run_time: float | None = None):
        """Animation: dominoes a..b (default: to the end) fall right one after another, RED."""
        b = len(self.dominoes) - 1 if b is None else b
        for k in range(a, b + 1):
            if k not in self._fallen:
                self.dominoes[k].save_state()
                self._fallen.add(k)
        anims = [_Topple(self.dominoes[k], angle, color) for k in range(a, b + 1)]
        rt = run_time or 0.5 + 0.35 * (b - a)
        return LaggedStart(*anims, lag_ratio=lag, run_time=rt)

    def stand_up(self, run_time: float = 0.5):
        """Animation: every fallen domino stands up again, GREY."""
        anims = [Restore(self.dominoes[k]) for k in sorted(self._fallen)]
        self._fallen = set()
        return AnimationGroup(*anims, run_time=run_time)


class Parcel(VGroup):
    """V5 · the build context as a parcel: a GREY box with PINK tape, titled 'build context', holding
    a row of small unnamed file glyphs and the named items (glyph over a mono 20 name).
        p = Parcel(["cli.py", ".git/", "Dockerfile"], extra=6)
        self.play(p.light("cli.py", TURN))
    .frame .title .tape .items{name: VGroup(glyph, name)} .crowd (the unnamed glyphs)"""

    def __init__(self, names=(".git/", "cli.py", "Dockerfile"), extra: int = 6, size: float = 20,
                 title: str = "build context", **kw):
        super().__init__(**kw)
        self.items = {}
        row = VGroup()
        for n in names:
            g = folder_glyph(0.3, S.GREY) if n.endswith("/") else file_glyph(0.36, S.GREY)
            t = mono(n, size, INK)
            it = VGroup(g, t).arrange(DOWN, buff=0.08)
            it.glyph, it.name_text = g, t
            self.items[n] = it
            row.add(it)
        row.arrange(RIGHT, buff=0.35, aligned_edge=DOWN)
        crowd = VGroup(*[file_glyph(0.26, S.GREY) for _ in range(extra)]).arrange(RIGHT, buff=0.12)
        inner = VGroup(crowd, row).arrange(DOWN, buff=0.18) if extra else row
        w, h = inner.width + 0.6, inner.height + 0.5
        self.frame = box(w, h, S.GREY, fill_opacity=0.1)
        inner.move_to(self.frame)
        self.tape = VGroup(Line(self.frame.get_corner(UL) + DOWN * 0.12, self.frame.get_corner(UR) + DOWN * 0.12,
                                color=ROUTE, stroke_width=6),
                           Line(self.frame.get_corner(DL) + UP * 0.12, self.frame.get_corner(DR) + UP * 0.12,
                                color=ROUTE, stroke_width=6))
        self.title = label(title, size, ROUTE).next_to(self.frame, UP, buff=0.1).align_to(self.frame, LEFT)
        self.crowd = crowd
        self.add(self.frame, self.tape, inner, self.title)

    def item(self, name: str) -> VGroup:
        return self.items[name]

    def light(self, name: str, color=TURN, run_time: float = 0.4):
        """Animation: item `name` (glyph and name) turns `color`."""
        it = self.items[name]
        return AnimationGroup(it.glyph.animate.set_stroke(color).set_fill(color, 0.4),
                              it.name_text.animate.set_color(color), run_time=run_time)


class Sieve(VGroup):
    """V5 · '.dockerignore' as a sieve (a mesh), dashed GREY while it doesn't exist.
        sv = Sieve(3.0); self.play(sv.solidify())     # the file exists now
    .frame .mesh .title"""

    def __init__(self, sieve_w: float = 3.0, sieve_h: float = 0.7, title: str = ".dockerignore",
                 color=S.GREY, size: float = 20, dashed: bool = True, **kw):
        super().__init__(**kw)
        self.sieve_w, self.sieve_h, self.hi_color = sieve_w, sieve_h, color
        r = RoundedRectangle(width=sieve_w, height=sieve_h, corner_radius=0.1, stroke_color=color,
                             stroke_width=2.5)
        self.frame = DashedVMobject(r, num_dashes=40, dashed_ratio=0.55 if dashed else 0.999)
        self.frame.set_stroke(color, 2.5)
        mesh = VGroup()
        for k in range(1, 9):
            x = -sieve_w / 2 + k * sieve_w / 9
            mesh.add(Line([x, -sieve_h / 2 + 0.06, 0], [x, sieve_h / 2 - 0.06, 0]))
        for k in (1, 2):
            y = -sieve_h / 2 + k * sieve_h / 3
            mesh.add(Line([-sieve_w / 2 + 0.06, y, 0], [sieve_w / 2 - 0.06, y, 0]))
        mesh.set_stroke(color, 1.5, opacity=0.35 if dashed else 0.8)
        self.mesh = mesh
        self.title = mono(title, size, color).next_to(r, UP, buff=0.1).align_to(r, LEFT)
        self.add(self.frame, self.mesh, self.title)

    def solidify(self, color=None, run_time: float = 0.6):
        """Animation: the dashed frame becomes solid (the file now exists)."""
        col = color or self.hi_color
        r = RoundedRectangle(width=self.sieve_w, height=self.sieve_h, corner_radius=0.1)
        tgt = DashedVMobject(r, num_dashes=40, dashed_ratio=0.999).set_stroke(col, 2.5).move_to(self.frame)
        return AnimationGroup(Transform(self.frame, tgt), self.mesh.animate.set_stroke(col, 1.5, opacity=0.8),
                              self.title.animate.set_color(col), run_time=run_time)


# ------------------------------------------------------------------ V6 · names and the registry
class NameTags(VGroup):
    """V6 · sticky notes beside `target`, each pointing at it (two names, one image).
        nt = NameTags(stack, ["simple-translate:latest", "student/simple-translate-ac215:latest"])
    .notes[i] .links[i] (thin TEAL lines from each note's left edge to the target)"""

    def __init__(self, target, names: list[str], side=RIGHT, buff: float = 0.9, size: float = 20, **kw):
        super().__init__(**kw)
        self.notes = VGroup(*[sticky(n, IMAGE, size) for n in names]).arrange(DOWN, buff=0.3,
                                                                               aligned_edge=LEFT)
        self.notes.next_to(target, side, buff=buff)
        edge = target.get_right() if np.allclose(side, RIGHT) else target.get_left()
        self.links = VGroup(*[Line(n.get_left() if np.allclose(side, RIGHT) else n.get_right(), edge,
                                   color=IMAGE, stroke_width=2) for n in self.notes])
        self.add(self.links, self.notes)


def name_parts(name: str = "docker.io/student/simple-translate-ac215:latest",
               captions=("registry · the default", "account", "repository", "tag"),
               size: float = 24, cap_size: float = 20) -> VGroup:
    """V6 · an image name unfolded: parts in TEAL mono, separators GREY, a GREY caption per part,
    alternately below and above so they don't collide. .parts .seps .captions .ticks"""
    toks = re.split(r"([/:])", name)
    words = VGroup()
    parts, seps = VGroup(), VGroup()
    for tk in toks:
        if tk in "/:" and tk:
            m = mono(tk, size, S.GREY)
            seps.add(m)
        else:
            m = mono(tk, size, IMAGE)
            parts.add(m)
        words.add(m)
    words.arrange(RIGHT, buff=0.06, aligned_edge=DOWN)
    caps, ticks = VGroup(), VGroup()
    for i, (p, c) in enumerate(zip(parts, captions)):
        t = label(c, cap_size, S.GREY)
        d = DOWN if i % 2 == 0 else UP
        t.next_to(p, d, buff=0.45)
        ticks.add(Line(p.get_edge_center(d) + d * 0.06, t.get_edge_center(-d) - d * 0.06,
                       color=S.GREY, stroke_width=1.5))
        caps.add(t)
    g = VGroup(words, ticks, caps)
    g.parts, g.seps, g.captions, g.ticks = parts, seps, caps, ticks
    return g


class RegistryShelf(VGroup):
    """V6 · a registry as a BLUE shelf unit with a door on its left side.
        hub = RegistryShelf("Docker Hub · student/simple-translate-ac215", shelf_w=5.0, boards=1)
        img.move_to(hub.spot(0, 1), aligned_edge=DOWN)     # stands on board 0, position 1 of 3
        self.play(hub.shut())                               # push access denied
    dashed=True: the stand-in registry. .frame .title .boards .door"""

    def __init__(self, title: str = "Docker Hub", shelf_w: float = 4.4, shelf_h: float = 2.4,
                 boards: int = 2, size: float = 20, dashed: bool = False, **kw):
        super().__init__(**kw)
        self.shelf_w, self.shelf_h = shelf_w, shelf_h
        self.frame = box(shelf_w, shelf_h, CLOUD, fill_opacity=0.06, dashed=dashed)
        self.title = label(title, size, CLOUD).next_to(self.frame, UP, buff=0.12)
        if self.title.width > shelf_w:
            self.title.align_to(self.frame, LEFT)
        self.boards = VGroup()
        for k in range(boards):
            y = -shelf_h / 2 + 0.2 + k * (shelf_h - 0.3) / boards
            self.boards.add(Line([-shelf_w / 2 + 0.55, y, 0], [shelf_w / 2 - 0.15, y, 0], color=CLOUD,
                                 stroke_width=3))
        self.door = RoundedRectangle(width=0.16, height=shelf_h * 0.7, corner_radius=0.05,
                                     stroke_color=CLOUD, stroke_width=2.5).set_fill(CLOUD, 0.1)
        self.door.move_to(self.frame.get_left() + RIGHT * 0.25)
        self.add(self.frame, self.boards, self.door, self.title)

    def spot(self, board: int = 0, k: int = 0, n: int = 3) -> np.ndarray:
        """Bottom-centre point of position k (of n) on board `board` (0 = lowest)."""
        b = self.boards[board]
        a, z = b.get_start(), b.get_end()
        return a + (z - a) * (k + 0.5) / n + UP * 0.02

    def shut(self, color=ERR, run_time: float = 0.5):
        """Animation: the door closes RED, with a cross on it."""
        x = cross_mark(0.35, color).move_to(self.door)
        return AnimationGroup(self.door.animate.set_stroke(color).set_fill(color, 0.45), FadeIn(x, scale=1.4),
                              run_time=run_time)


# ------------------------------------------------------------------ V7 · platforms
def glyph_row(kind: str = "amd64", n: int = 7, glyph_h: float = 0.22, color=None) -> VGroup:
    """A row of 'machine instruction' glyphs: amd64 = squares and triangles (BLUE), arm64 =
    circles and diamonds (GREY). Two alphabets that never match."""
    color = color or (AMD if kind == "amd64" else ARM)
    gs = VGroup()
    for k in range(n):
        if kind == "amd64":
            g = Square(glyph_h) if k % 2 == 0 else Triangle().scale_to_fit_height(glyph_h)
        else:
            g = Circle(radius=glyph_h / 2) if k % 2 == 0 else Square(glyph_h * 0.75).rotate(np.pi / 4)
        gs.add(g.set_stroke(color, 2).set_fill(color, 0.4))
    return gs.arrange(RIGHT, buff=glyph_h * 0.5)


def platform_chip(kind: str = "amd64", text: str | None = None, size: float = 20, n: int = 7) -> VGroup:
    """A CPU platform: a chip ('arm64 · Apple Silicon' GREY / 'amd64 · Intel/AMD · default GCP VM'
    BLUE) with its glyph row under it. .chip .glyphs .kind"""
    col = AMD if kind == "amd64" else ARM
    text = text or ("amd64 · Intel/AMD · default GCP VM" if kind == "amd64" else "arm64 · Apple Silicon")
    c = chip(text, col, size=size)
    gl = glyph_row(kind, n).next_to(c, DOWN, buff=0.15)
    g = VGroup(c, gl)
    g.chip, g.glyphs, g.kind = c, gl, kind
    return g


class PlatformMenu(VGroup):
    """V7 · what a tag points at: a card titled with the name, one row per platform image. A row
    given as (text, None) is dimmed (an attestation).
        m = PlatformMenu("python:3.12-slim-bookworm", [("linux/amd64", AMD), ("attestation", None), ...])
        self.play(FadeIn(m.mark(0, AMD)))
    .title .rows[i] (mono 20) .frame"""

    def __init__(self, title: str, rows, size: float = 20, menu_w: float | None = None, **kw):
        super().__init__(**kw)
        self.title = mono(title, size, IMAGE)
        self.rows = VGroup()
        for r in rows:
            s, col = (r, INK) if isinstance(r, str) else r
            dim = col is None
            t = mono(s, size, S.GREY if dim else (col or INK))
            if dim:
                t.set_opacity(0.6)
            self.rows.add(t)
        self.rows.arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        body = VGroup(self.title, self.rows).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        w = menu_w or body.width + 0.6
        self.frame = box(w, body.height + 0.5, IMAGE, fill_opacity=0.06)
        body.move_to(self.frame).align_to(self.frame, LEFT).shift(RIGHT * 0.3)
        self.sep = Line(self.frame.get_left() + RIGHT * 0.15, self.frame.get_right() + LEFT * 0.15,
                        color=IMAGE, stroke_width=1.5, stroke_opacity=0.6)
        self.sep.move_to([self.frame.get_center()[0], (self.title.get_bottom()[1] + self.rows.get_top()[1]) / 2, 0])
        self.add(self.frame, self.sep, self.title, self.rows)

    def mark(self, i: int, color=TURN) -> Rectangle:
        """A highlight frame around row i (not added)."""
        r = self.rows[i]
        return RoundedRectangle(width=self.frame.width - 0.3, height=r.height + 0.16, corner_radius=0.06,
                                stroke_color=color, stroke_width=2.5).move_to(
            [self.frame.get_center()[0], r.get_center()[1], 0])


# ------------------------------------------------------------------ V8 · container ≠ VM
class KernelPicture(VGroup):
    """V8 · VMs, each with its own OS and kernel (BLUE), that become containers on one shared kernel.
        kp = KernelPicture(3)
        self.play(*kp.to_containers())        # kernels merge into one bar, VMs shrink to containers
        self.play(FadeIn(kp.desktop_vm()))      # dashed GREY 'Linux VM · Docker Desktop' under it
    .vms[i] (.frame .title .os .kernel) · after to_containers: .bar (the shared kernel)"""

    def __init__(self, n: int = 3, vm_w: float = 2.4, vm_h: float = 2.7, gap: float = 0.35,
                 size: float = 20, **kw):
        super().__init__(**kw)
        self.n, self.size, self.vm_w, self.vm_h, self.gap = n, size, vm_w, vm_h, gap
        self.vms = VGroup()
        for _ in range(n):
            f = box(vm_w, vm_h, CLOUD, fill_opacity=0.06)
            t = steady("VM", size + 2, CLOUD).move_to(f.get_top() + DOWN * 0.32)
            k = self._bar("kernel", vm_w - 0.3, S.GREY).move_to(f.get_bottom() + UP * 0.38)
            o = self._bar("OS", vm_w - 0.3, SYSTEM).next_to(k, UP, buff=0.1)
            v = VGroup(f, t, o, k)
            v.frame, v.title, v.os, v.kernel = f, t, o, k
            self.vms.add(v)
        self.vms.arrange(RIGHT, buff=gap)
        self.bar = None
        self.add(self.vms)

    def _bar(self, s: str, w: float, col) -> VGroup:
        r = RoundedRectangle(width=w, height=0.46, corner_radius=0.06, stroke_color=col,
                             stroke_width=2).set_fill(col, 0.22)
        t = steady(s, self.size, INK).move_to(r)
        return VGroup(r, t)

    def to_containers(self, bar_text: str = "Linux kernel · shared") -> list:
        """Animations: kernel bars slide down and merge into one GREY bar; each VM shrinks into a
        TEAL 'container' box standing on it (its OS band becomes the container's own files)."""
        total = self.vms.width
        bottom = self.vms.get_bottom()[1]
        bar = self._bar(bar_text, total, S.GREY).move_to([self.vms.get_center()[0], bottom + 0.23, 0])
        anims = []
        for i, v in enumerate(self.vms):
            cw, ch = self.vm_w * 0.8, 1.5
            cf = box(cw, ch, IMAGE, fill_opacity=0.08)
            cf.move_to([v.frame.get_center()[0], bar.get_top()[1] + 0.12 + ch / 2, 0])
            ct = steady("container", self.size, IMAGE).move_to(cf.get_top() + DOWN * 0.3)
            co = self._bar("files", cw - 0.3, SYSTEM).move_to(cf.get_bottom() + UP * 0.35)
            anims += [Transform(v.frame, cf), Transform(v.title, ct), Transform(v.os, co)]
            tgt = bar.copy() if i == 0 else bar.copy().set_opacity(0)
            anims.append(Transform(v.kernel, tgt))
        self.bar = self.vms[0].kernel
        return anims

    def desktop_vm(self, text: str = "Linux VM · Docker Desktop") -> VGroup:
        """Dashed GREY box under the (shared) kernel bar (not added). .frame .text"""
        ref = self.bar if self.bar is not None else self.vms
        f = box(self.vms.width, 0.6, S.GREY, dashed=True)
        f.next_to(ref, DOWN, buff=0.15)
        t = label(text, self.size, S.GREY).move_to(f)
        g = VGroup(f, t)
        g.frame, g.text = f, t
        return g


def vm_with_docker(vm_w: float = 5.2, vm_h: float = 3.2, size: float = 20) -> VGroup:
    """V8 (S14 half): the BLUE VM; inside, PURPLE dockerd sits directly on the VM's own kernel bar,
    an empty dashed TEAL container slot above it. .frame .title .kernel .dockerd .slot"""
    f = box(vm_w, vm_h, CLOUD, fill_opacity=0.06)
    t = label(f"VM · {VM_HOST}", size + 2, CLOUD).move_to(f.get_top() + DOWN * 0.32)
    kr = RoundedRectangle(width=vm_w - 0.4, height=0.46, corner_radius=0.06, stroke_color=S.GREY,
                          stroke_width=2).set_fill(S.GREY, 0.22).move_to(f.get_bottom() + UP * 0.4)
    kt = label("Debian · Linux kernel", size, INK).move_to(kr)
    dk = box(vm_w * 0.5, 0.5, TOOL, fill_opacity=0.18).next_to(kr, UP, buff=0.12)
    dt = mono("dockerd", size, TOOL).move_to(dk)
    sl = box(vm_w * 0.5, 0.9, IMAGE, dashed=True).next_to(dk, UP, buff=0.12)
    st = label("container", size, IMAGE).move_to(sl)
    g = VGroup(f, t, VGroup(kr, kt), VGroup(dk, dt), VGroup(sl, st))
    g.frame, g.title, g.kernel, g.dockerd, g.slot = f, t, g[2], g[3], g[4]
    return g


# ------------------------------------------------------------------ cost dial (L1)
class CostDial(VGroup):
    """The video's cost meter: a GOLD dial whose needle sweeps while the VM exists, with no digits
    (no invented price). It never rewinds; .run(scene, turns, secs) sweeps it on; .freeze() stops
    it where it is (S16, on Delete). .needle .tracker (angle in turns) .face .caption"""

    def __init__(self, radius: float = 0.55, caption: str | None = "cost", **kw):
        super().__init__(**kw)
        from manim import TAU
        self.radius = radius
        face = Circle(radius=radius, stroke_color=COST, stroke_width=3).set_fill(COST, 0.08)
        ticks = VGroup(*[Line(UP * radius * 0.78, UP * radius * 0.95, color=COST, stroke_width=2)
                         .rotate(-k * TAU / 12, about_point=ORIGIN) for k in range(12)])
        self.tracker = ValueTracker(0.0)
        hub = Dot(radius=0.05, color=COST)

        def make_needle():
            n = Line(ORIGIN, UP * radius * 0.75, color=COST, stroke_width=4)
            n.rotate(-self.tracker.get_value() * TAU, about_point=ORIGIN)
            return n.shift(face.get_center())

        self.needle = always_redraw(make_needle)
        self.face, self.ticks, self.hub = face, ticks, hub
        self.add(face, ticks, self.needle, hub)
        self.caption = None
        if caption:
            self.caption = label(caption, CAPTION, COST).next_to(face, DOWN, buff=0.12)
            self.add(self.caption)

    def run(self, scene, turns: float = 0.5, seconds: float = 2.0):
        scene.play(self.tracker.animate(rate_func=linear).increment_value(turns), run_time=seconds)

    def freeze(self):
        """Stop the needle where it is (call after the last run)."""
        self.needle.clear_updaters()
        return self

