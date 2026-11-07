"""Shared scene code for AC215 L20 (Deployment: the cheese app on one VM by hand, then Pulumi to a single
VM; follow-along of dlops-io/cheese-app-v3 @ 3ecef56 = main on 2026-11-05, README sections "Deployment
to GCP (Manual)", "Deployment to GCP (Single VM Instance)" and "Delete the Compute Instance /
Persistent disk").

Paths, narration (SAY lines straight from script.md), the semantic colours of BRIEF.md, the running
example (placeholders only: your-gcp-project, <instance_ip>, sa_000…), the two README trackers,
loaders for the real captures in assets/terminal/{vm,laptop} (masked on load), the README's own
OS Login snippet in assets/terminal/expected, source panels from assets/source, terminal helpers,
tags, chips, cards and the video's set pieces V1-V8. Generic helpers come from L18's common.py
(tested there); the set pieces are new. build/common_test.py plays every helper and piece once
(Bench*: explainer.check clean).

    from manim import *          # first
    from common import *         # second (common's names win), then:
    SAY = NARRATION["S07"]; assert len(SAY) == SAY_COUNT["S07"]   # one voiceover block per SAY

Notes for scene authors
=======================
Rules. Every text here is >= 20 pt and nothing scales text: never .scale() a group that holds text
below 1.0 (pieces take size / width parameters; where a picture must be smaller, use the compact
variant or a text-free glyph). Never set width / height / color / depth on a VGroup subclass (Manim
properties): these classes use box_w, win_w, cw … Methods marked PLAYS take the scene first, play
their own animation and keep the new mobjects inside the piece, so a later FadeOut(piece) takes them
all. ANIM methods return an animation you play. To take one part away use piece.drop(self, part):
never FadeOut a member of a piece directly (it snaps back when the piece is next drawn). Place a piece
(shift / move_to) BEFORE its first PLAYS call or between calls: PLAYS methods build new parts at the
piece's current position. Split trap: animating a group that is not itself on the scene (substring(),
code_span(), a VGroup of existing parts) splits every parent holding those members; re-seat with
piece.heal(self) (PLAYS methods do it) or self.add(parent). Opaque fills: boxes use tint(colour).
No prices on screen except S14's one GOLD line (cost_tag allows an amount only with '≈' and 'roughly').

Frame budget. Safe frame x in [-6.6, 6.6], y in [-3.6, 3.6]. Tracker top-left (left -6.5, top 3.5,
lowest point TRACK_BOTTOM 2.9); lecture tag lref("21–24") top right; pictures stay below PIC_TOP 2.8.
Terminals: term() is 12.6 wide, bottom edge at BOTTOM -3.5; a 3-row strip's top is STRIP_TOP
(about -1.44), so a picture over a strip lives in y in [-1.3, 2.8].

Data
    NARRATION["S01"] .. ["S16"]  SAY_COUNT  TITLES[cls]  SPEC (video.yaml)
    Prompts P_VM 'student@cheese-app-vm:~$' · P_LAPTOP 'student@laptop:~$' (= P_HOME) · P_REPO ·
    P_FRONTEND …/src/frontend-react$ · P_API · P_VDB · P_DEPLOY …/src/deployment$ · P_TOOLBOX read from
    b02d:77 ('root@<id>:/app#', the id never read aloud) · toolbox_prompt(path) swaps the path
    ('/secrets', '/app/deploy_images', '/app/deploy_single_vm'). Titles T_VM 'cheese-app-vm',
    T_LAPTOP 'laptop', T_TOOLBOX 'laptop · toolbox', T_NEW 'laptop · new terminal'.
    Names PROJECT_PH 'your-gcp-project' · PROJECT_README 'ac215-project' (always with default_tag) ·
    IP_PH '<instance_ip>' · VM_IP_PH '<Your VM IP Address>' · SA_MASK 'sa_000000000000000000000' ·
    SA_SHORT 'sa_000…' · NETWORK 'cheese-app-network' · APPNET 'appnetwork' · C_VDB C_API C_FRONT
    C_NGINX C_LOADER C_TOOLBOX · PORTS{vdb 8000, api 9000, front 3000, nginx 80} · CHUNKS 14356 ·
    BOOK_CHUNKS (the eleven 'Finished inserting' numbers) · BOOK_LINES (their vm/27 file lines) ·
    STAMP_1 '20261105233500' (b34:42) · STAMP_2 '20261105233939' (b35b:17) · STAGES_MANUAL (slide 8) ·
    SIX_STEPS / SIX_FILES (slide 19) · PROVIDERS · EXPORTS (__main__.py:29-34) · DOMINOES · LAMPS ·
    ENV_NAMES · MOUNTS (docker-shell.sh:35-43) · ROLES_DEPLOY (README:241-246) · ROLES_SERVICE (253-255).
    unname(s) / mask(s): instructor → '‹instructor›', staff branch → 'work/…', sa_<digits> → SA_MASK.

Trackers (script.md conventions; placed top-left)
    tracker_m(step=None, extra=False) README › Deployment to GCP (Manual), 15 steps · tracker_p(...)
    README › Deployment to GCP (Single VM Instance), 14 steps (Destroy included) · tracker(key, …)
    key 'M' | 'P'. extra: True (' · extra') | 'our spelling' | 'not for you' | 'recording only' |
    'or edit the file' (' · extra · …') | any other str (appended after ' · ').
    track(tr, k, extra) ANIM (never tr.goto) · lref("7"), lref("8, 24"), lref("19–20, 25") the GREY
    'Lecture 20 · slide(s) …' tag, top right.

Captures (assets/terminal/<folder>/<id>-*.txt; capture-only/ is refused; masked on load)
    c = capture("b02d") (laptop: a*, b*, p*) · capture("vm/58") or capture("58") (vm: names starting
    with a digit) · capture("vm/30b") · capture("b19-2") / capture("b41-3") (the config-set triples).
    c.cmd_lines (typed rows) c.cmd c.k · c.at(*spec) output by FILE line numbers (ints, (a, b), '…');
    refuses the command lines and [exit N] · c.crop(n, "404  Not Found") (script.md's crop "…") ·
    c.line(n) · c.pick(*ranges) L1-style (body index = file line − k) · c.lines c.exit c.raw c.path c.key.
    CMD_LINES: vm/44 is one 58-row command (the echo '…' of nginx.conf: rows 2.. are typed as quoted
    continuation rows, no prompt, soft-wrapped); b10 holds three commands, b14 two.
    type_capture(scene, t, c, prompts=None) PLAYS types them right; prompts=[p1, p2, p3] sets the
    prompt before each command row (b10: toolbox_prompt('/app'), …('/secrets'), …('/secrets')).
    type_at(scene, t, cap, n) types a command at the container prompt printed on file line n.
    recorded("oslogin-ssh-keys-add", (2, 10), plain=False) lines of expected/<file> (the '# …'
    provenance line refused) · quote_card(file, nums, kind='expected', source='README:306–314',
    mono_font=True) (verbatim YAML, indentation kept; .body[i] is row i, e.g. the 'username:' row).
    Folders: assets/terminal/vm (the Debian 12 VM stand-in: 00-60), assets/terminal/laptop (a01-a06
    Docker Hub, p01-p05 clone/secrets, b01-b22 the README's Pulumi steps, b30-b46 extras on Pulumi's
    local backend), assets/terminal/expected (oslogin-ssh-keys-add.txt only).

Sources (assets/source/<path> = cheese-app-v3 @ 3ecef56; header '<path> · lines a–b')
    code(path, a, b=None, focus=, font_size=22, cuts={line: 'cut after'}, elide={line: 'middle'},
        dedent=False, shown='short/header/path') CODE() panel, <= 12 lines, must fit (22 pt ~66
        characters, 20 pt ~74; a wider panel raises and names the line). e.g.
        code("src/deployment/nginx-conf/nginx/nginx.conf", 35, 44). .code .header; highlight with
        code_span(p.code, k, "x") / line_bar(p.code, k, colour), k = file line - a. Refuses a range
        that includes src/vector-db/cli.py:75 or :440 (they name the instructor).
    excerpt(path, a, b) / source_text(path) / readme(n) / readme_lines(a, b) (card text) ·
    readme_rows(a, b) (command rows for type_lines) · readme_card((a, b), body).

Terminals (house: 12.6 wide, 22 pt = 65 characters a row; 20 pt = 72)
    term(prompt, rows, title) · vm_term(rows=10) · laptop_term(rows=10, prompt) · toolbox_term(rows,
    path='/app') · new_term(rows, prompt=P_FRONTEND) · resize(scene, t, rows) PLAYS · retitle(t, title)
    ANIM · room · bare_prompt · type_cmd(scene, t, cmd, soft=None) · type_capture · type_at ·
    type_lines(scene, t, readme_rows(a, b)) · out(scene, t, lines, wrap=) · cd_prompt(scene, t, prompt)
    · beside / pin / unpin / attach / on_bar / under_term for tags at a row · row_tag, turn_row,
    extra_row(kind), time_row, cost_row, default_row (tags sized for a terminal row) · no_panel_chip().

Tags and chips (GREY unless said; all 20-22 pt)
    your_turn() YELLOW · extra_tag(kind) ('extra · our spelling', 'extra · not for you', 'extra ·
    recording only', 'extra · not in the README') · illustration_tag(s) · expected_tag(source) ·
    recorded_tag(source) · recording_tag() 'at the time of recording' · erratum_tag(s) ·
    default_tag() "the README's default · change to yours" · cost_tag(text) GOLD (raises on an amount
    unless the text has '≈' and 'roughly') · disk_chip(text) GOLD-outlined · grey_chip · editor_chip ·
    dashed_chip (past/future) · tool_chip PURPLE · err_chip RED · ok_chip GREEN · route_chip PINK ·
    box_chip TEAL · differ_chip · file_card(path) · card(lines, head=) · question_card(text) YELLOW ·
    sticky(text) YELLOW sticky note · ponder(scene, q, seconds) PLAYS (opaque pause_and_ponder card;
    FadeOut it at the next block) · flash_tag(scene, tg) · console_form(title, fields) (schematic
    console page with its 'illustration' tag; fields (label, value[, colour])) · Checklist(title,
    items, color, tag_text, dashed) .tick(scene, i) (S10's APIs, S16's teardown, GOLD with color=COST).

Glyphs (text-free unless named; sizes in scene units)
    tint(colour, k) · cbox(rows, box_w, box_h) · svc_box(name, port, box_w, box_h, dashed) V1 box ·
    door(port) PINK plate (.plate .text) · mini_browser(url, win_w=3.3) one-bar browser · Browser(url,
    win_w, win_h) (PLAYS goto / fill(rows) / reload / clear; ANIM flash) for the illustration windows ·
    browser_icon · disk_cyl(w) · pail(w, colour, rim, dashed) · bucket · disk · key_icon('deploy' |
    'service' | 'ssh', name=True) · key_glyph · padlock(h, colour, text) · scissors(h) · crate(name)
    TEAL image crate · lamp(state) 'off'|'green'|'amber'|'red'|'dashed' · envelope(text) · image_block ·
    file_icon / folder_icon · cloud_shape · you() · check_glyph / cross_glyph · arrow / route /
    travel / bounce / pulse_dot · ring / under / strike / hl_bar · outline_box · keep_inside(m).
    CostDial(radius, caption) GOLD needle meter: .run(scene, turns, seconds) · .freeze().

Set pieces (V numbers = BRIEF; each class doc gives its exact layout and every method)
    SixSteps(current=0, files=True) / six_steps(current) slide 19's strip, 12.6 x ~1.35 (chips y 0.35,
        files under them): ANIM goto(k) (earlier ticked GREEN, k YELLOW) · light(k); PLAYS
        shrink_away(). .chips .files .checks
    V1 MasterDiagram(manual=False, built=()) full frame (laptop x -6.45 .. -3.35 top-left, GCP
        x -2.7 .. 6.45 / y -3.3 .. 1.45, VM x 0.6 .. 6.25, browser over it at y 1.95). PLAYS laptop(title)
        · gcp · registry (Docker Hub when manual) · gcr_note · models · state · vm · disk(text) ·
        box('front'|'api'|'vdb'|'nginx') · door(on='vm'|'nginx') · browser(url) · push · pull · hollow
        · routes · loader(pour, leave) · front_port_fix · stage_chips (manual, y -3.35) · build(*keys)
        · stage21..stage24, stage27(url), teaser(url). ANIM light(key, c) · normal(key) ·
        light_stage(k). .parts{key} .slot{key} .stage_row
    V2 NamePhoneBook(title=T_VM, built=False) the VM inside, x -4.05 .. 5.75 / y -1.7 .. 1.7 (+ title,
        fence, tags, outsider: x -6.45 .. 5.95, y -2.75 .. 2.5). PLAYS cable_on · plug(key) · loader ·
        pour(n) · unload · clear_loader_line · stop(key) · start(key) · routes · nginx_fail(at) ·
        nginx_ok · fence(labels) · gate_labels · tags · outsider(kind) · knock(port, ok, text) ·
        question(key) · unquestion. ANIM light_entry(key) · light(key) · normal(key).
        Keys 'vdb' 'loader' 'api' 'front' 'nginx'.
    V3 ProxyRoute(gates=False) x -3.2 .. 3.0 (gates: from -4.3), y -2.35 .. 2.0. PLAYS enter(path) ·
        match('api'|'front') · snip() · arrive() · reply(text) · reset() · run(path, branch, reply).
        ANIM light_sign(branch) · light_target(branch).
    V4 EngineLoop(cards=('Network','Firewall','Disk','Instance'), compact=False) full: x -6.2 .. 6.2,
        y -3.35 .. 2.6; compact: x -3.05 .. 3.05, y -1.35 .. 1.0 (trees only). PLAYS machine · run ·
        trees(stale=1) · refresh · diff(glyphs) · apply · banner · footnote(text) · preview_stop ·
        in_sync · unknown(i) · backwards · clear_glyphs.
    V5 ControlRoom() x -3.6 .. 3.6, y -2.6 .. 2.6 (laptop holding the TEAL toolbox). PLAYS env(names,
        extra) · wire(i) / wires() · bricks() · brick(name, state) · lamps() · lamp_set(i, state) ·
        clear(phase). Phases 'env' 'wires' 'bricks' 'lamps' (one text phase at a time).
    V6 TimestampPipe() x -6.3 .. 6.4, y -2.4 .. 2.25. PLAYS files · shelf_on · crates_up · stamp(stamp)
        · refused(i, keep=False) · shelve · ticket · pipe · second_run(stamp) · retain.
    V7a VmFences() x -6.3 .. 2.2 (+ plan to 6.4), y -2.85 .. 2.6. PLAYS vpc · gate(port) / gates_all ·
        vm · wear_tags · disk · envelope · open_envelope · caption(text) · plan_rows(rows) · tick(i,
        glyph) · fail(i).
    V7b ProvisionDominoes(labels=DOMINOES, rows=(5, 4)) x -5.0 .. 5.0, y -1.45 .. 1.25; S15:
        ProvisionDominoes(('upload', 'move', 'restart'), rows=(3,)). PLAYS fall(upto, per) · stand ·
        refuse(i, note) · disk(labels) · wipe · restore · replay(indices).
    V8 KeyRing() card x -3.6 .. 3.6, y -1.85 .. 1.85 (+ your_project line under it; role chips left
        of it: shift the card right ~2.6). PLAYS roles(row, roles, at) · key(row) · your_project().
        SshKey() x -3.3 .. 3.5, y -1.4 .. 1.7 (S12). PLAYS appear · cut · upload · username.

Capture folder names: assets/terminal/vm (the Debian 12 stand-in for the console-made VM, user
student, host cheese-app-vm), assets/terminal/laptop (a fresh Docker 29.8.2 engine standing in for
the laptop; b02d on is inside the toolbox) and assets/terminal/expected (the README's OS Login
snippet only); capture-only/ folders are plumbing and refused.
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import yaml
from manim import (DL, DOWN, DR, LEFT, ORIGIN, PI, RIGHT, TAU, UL, UP, UR, AnimationGroup, Arc,  # noqa: F401
                   Arrow, Circle, Create, CurvedArrow, DashedLine, DashedVMobject, DecimalNumber, Dot, FadeIn,
                   FadeOut, GrowArrow, GrowFromCenter, Indicate, LaggedStart, Line, MoveAlongPath, Polygon,
                   Rectangle, ReplacementTransform, RoundedRectangle, Rotate, ShowIncreasingSubsets, Square,
                   Succession, Text, Transform, UpdateFromAlphaFunc, ValueTracker, VGroup, VMobject,
                   always_redraw, interpolate_color, linear, there_and_back)

from explainer import style as S
from explainer.components import pause_and_ponder, person_icon, ponder_card  # noqa: F401 (re-export)
from explainer.devops import (CAPTION, LABEL, MONO, OUTPUT, PANEL, SMALL, TAG, TERM_BG,  # noqa: F401
                              PROMPT_PATH, ReadmeTracker, Terminal, box, cell_width, chip, code_block,
                              code_panel, code_span, file_glyph, folder_glyph, glyph_range, label,
                              lecture_ref, line_bar, line_pitch, mono, mono_line, server, step_badge,
                              substring, tag)
from explainer.script import load_narration

# ------------------------------------------------------------------ paths and data
HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
ASSETS = PROJECT / "assets"
TERMINAL = ASSETS / "terminal"
SOURCE = ASSETS / "source"
EXPECTED = TERMINAL / "expected"

SPEC = yaml.safe_load((PROJECT / "video.yaml").read_text())
TITLES = {s["cls"]: s["title"] for s in SPEC["scenes"]}
_script = PROJECT / "script.md"
NARRATION = load_narration(_script) if _script.exists() else {}
# SAY lines per scene (script.md v2, 2026-11-06); every scene asserts its own count
SAY_COUNT = {"S01": 8, "S02": 7, "S03": 9, "S04": 9, "S05": 9, "S06": 8, "S07": 13, "S08": 7,
             "S09": 11, "S10": 7, "S11": 11, "S12": 7, "S13": 11, "S14": 12, "S15": 14, "S16": 12}

# ------------------------------------------------------------------ semantic colours (BRIEF.md)
LAPTOP = S.GREY          # the laptop: browser, secrets/ on the host, the host's Docker, the toolbox's outline
BROWSER = LAPTOP
YOU = LAPTOP
CLOUD = S.BLUE           # GCP, the VM, the VPC, the disk, Artifact Registry, Docker Hub, the state bucket
CONTAINER = S.TEAL       # containers and images (api-service, frontend, vector-db, loader, nginx, toolbox)
IMAGE = CONTAINER
SHARED = S.ORANGE        # OS-owned / shared: apt pools, Google's apt repo, default builder, 0777 folders
SYSTEM = SHARED
AMBER = S.ORANGE
OWN = S.GREEN            # project-owned and pinned: Pulumi.yaml, config, state, stamps, cheese-app-network
NET = OWN
PASS = OWN
TOOL = S.PURPLE          # Docker/buildx, gcloud, Pulumi and its providers, kubectl, uv, ssh-keygen
ERR = S.RED              # every honest first error, the mangled log_format, broken README steps
TURN = S.YELLOW          # your turn, the tracker, the thing to look at now, the current six-step chip
COST = S.GOLD            # the VM, disks, IP, registry storage, state bucket
ROUTE = S.PINK           # URLs, ports, -p doors, request arrows, firewall gates, tags, SSH tunnel, the pipe
PAST = S.GREY            # the past and the future, slide items the repo does not use: dashed
FUTURE = PAST
INK = S.WHITE
DIMMED = S.GREY

# ------------------------------------------------------------------ layout
TRACK_LEFT, TRACK_TOP = -6.5, 3.5
TRACK_BOTTOM = 2.9           # the tracker's lowest point
BOTTOM = -3.5                # a terminal's bottom edge (kept when it grows or shrinks)
PIC_TOP = 2.8                # pictures stay below this (tracker / lecture_ref above)
SAFE_X, SAFE_Y = 6.6, 3.6


def strip_top(rows: int = 3, size: float = 22) -> float:
    """Top edge of a `rows`-row terminal standing on BOTTOM."""
    return BOTTOM + rows * line_pitch(size) + 0.85


STRIP_TOP = strip_top(3)     # about -1.44: a picture over a 3-row strip lives in y in [-1.3, 2.8]


def steady(s: str, size: float = 20, color=INK, mono_font: bool = False, **kw) -> Text:
    """Text with a fixed vertical extent (an invisible '|' strut), so a Transform between two
    steady texts keeps the size the check tool computes. Use it for anything that morphs."""
    t = (mono if mono_font else label)("|" + s, size, color, **kw)
    pipe = t[0]
    if len(t) > 1:
        pipe.move_to([t[1].get_center()[0], pipe.get_center()[1], 0])
    pipe.set_opacity(0)
    return t


def note(s: str, color=S.GREY, size: float = 20, **kw) -> Text:
    """A caption line (label font, GREY by default). The 2nd positional arg is the colour."""
    return label(s, size, color, **kw)


# ------------------------------------------------------------------ series rules: no names, no ids
_NAME_RE = re.compile(r"Pavlos(?:[ _]Protopapas)?|Protopapas", re.IGNORECASE)
_BRANCH_RE = re.compile(r"work/[a-z]+")          # the unmerged staff branch: never named
_SA_RE = re.compile(r"sa_\d{6,}")                # the OS Login user: always masked
SA_MASK = "sa_000000000000000000000"
SA_SHORT = "sa_000…"


def unname(s: str) -> str:
    """s with the instructor's name masked ('‹instructor›'), the staff branch cropped ('work/…') and
    every 'sa_' + digits OS Login user replaced by SA_MASK. capture(), recorded(), source_text() and
    readme() apply it, so no scene ever sees the real values."""
    s = _NAME_RE.sub("‹instructor›", s)
    s = _BRANCH_RE.sub("work/…", s)
    return _SA_RE.sub(SA_MASK, s)


mask = unname


# ------------------------------------------------------------------ captures
CAPTURE_FOLDERS = ("laptop", "vm")
# captures whose command takes several file lines that are NOT joined by a trailing '\':
#   vm/44     the README's echo '…' > conf/nginx/nginx.conf (58 rows: one command, the rest are the
#             quoted text, typed as continuation rows without a prompt, soft-wrapped)
#   laptop/b10  cd /secrets · ssh-keygen -f ssh-key-deployment · cd /app (three commands)
#   laptop/b14  cd deploy_images · pulumi stack init dev (two commands)
CMD_LINES = {"vm/44": 58, "laptop/b10": 3, "laptop/b14": 2}
QUOTED = ("vm/44",)          # rows 2.. are the inside of one quoted argument
_ALIAS = re.compile(r"^(b19|b41)-([123])$")     # b19-2 = b19-vm-config-set-2, b41-1 = b41-x-vm-config-set-1


class Capture:
    """One captured command (assets/terminal/<folder>/<file>). .cmd_lines (typed rows) .cmd (joined
    with '\\n') .k (file lines of the command) .lines (output body, no [exit N]) .exit .raw (every
    file line, tabs expanded, masked) .path .key ('vm/44', 'laptop/b02d')"""

    def __init__(self, cmd_lines, lines, exit_code, raw, path, key):
        self.cmd_lines, self.lines, self.exit, self.raw, self.path = cmd_lines, lines, exit_code, raw, path
        self.k = len(cmd_lines)
        self.cmd = "\n".join(cmd_lines)
        self.key = key

    def line(self, n: int) -> str:
        """File line n (1-based). Refuses the command lines (typed, never printed) and [exit N]."""
        if not 1 <= n <= len(self.raw):
            raise IndexError(f"{self.path.name} has {len(self.raw)} lines, not {n}")
        if n <= self.k:
            raise ValueError(f"{self.path.name}:{n} is part of the typed command (lines 1-{self.k}): "
                             "type it with type_capture(), never print it")
        s = self.raw[n - 1]
        if re.fullmatch(r"\[exit -?\d+\]", s):
            raise ValueError(f"{self.path.name}:{n} is the [exit N] line: never printed")
        return s

    def at(self, *spec) -> list[str]:
        """Lines by FILE line numbers, as script.md's TERM(...) writes them: ints, (a, b) inclusive
        ranges and '…' items (a literal '…' line). at(3, (5, 7), '…', 15). Never adds '…' itself."""
        out_: list[str] = []
        for r in spec:
            if isinstance(r, str):
                out_.append(r)
                continue
            a, b = (r, r) if isinstance(r, int) else r
            out_ += [self.line(n) for n in range(a, b + 1)]
        return out_

    def crop(self, n: int, after: str, ellipsis: str = "") -> str:
        """script.md's `crop "…"`: file line n printed only up to and including `after`
        (b02's 404 lines lose the proxy column: c.crop(135, "404  Not Found"))."""
        s = self.line(n)
        i = s.index(after) + len(after)
        return s[:i] + ellipsis

    def pick(self, *ranges, ellipsis: str = "…") -> list[str]:
        """L1-style: output lines by 1-based inclusive ranges over the OUTPUT body (pick(1) = the
        first output line = file line k+1); a gap inserts '…'. Negative numbers count from the end.
        Prefer .at() with the script's file line numbers."""
        n = len(self.lines)
        out_: list[str] = []
        last = None
        for r in ranges:
            a, b = (r, r) if isinstance(r, int) else r
            a = a if a > 0 else n + a + 1
            b = b if b > 0 else n + b + 1
            if last is not None and a > last + 1:
                out_.append(ellipsis)
            out_ += self.lines[a - 1:b]
            last = b
        return out_


def capture(name: str) -> Capture:
    """capture("b02d") / capture("a01") / capture("p05") (laptop/) · capture("vm/58") or capture("58")
    (a name starting with a digit is vm/) · capture("b19-2") / capture("b41-3") (the three config-set
    files) · capture("vm/30b"). The one file assets/terminal/<folder>/<name>-*.txt (or <name>.txt).
    Fails loudly when missing or ambiguous: never show an uncaptured output. The command takes file
    lines 1..k: k from CMD_LINES, else line 1 plus every row that follows a trailing '\\'.
    capture-only/ is plumbing and refused. Text is masked on load (unname)."""
    if "capture-only" in name:
        raise ValueError("capture-only/ is plumbing (CA builds, placeholder keys): never shown")
    folder, _, stem = name.rpartition("/")
    stem = stem[:-4] if stem.endswith(".txt") else stem
    folder = folder or ("vm" if stem[:1].isdigit() else "laptop")
    if folder not in CAPTURE_FOLDERS:
        raise ValueError(f"capture folder {folder!r}: one of {CAPTURE_FOLDERS} (expected/ → recorded())")
    d = TERMINAL / folder
    p = d / f"{stem}.txt"
    if not p.exists():
        m = _ALIAS.match(stem)
        hits = sorted(d.glob(f"{m.group(1)}-*-{m.group(2)}.txt")) if m else sorted(d.glob(f"{stem}-*.txt"))
        if len(hits) != 1:
            raise FileNotFoundError(f"capture {folder}/{stem}: {len(hits)} matches {[h.name for h in hits]} "
                                    "(see ASSETS.md)")
        p = hits[0]
    with open(p, encoding="utf-8", newline="") as f:
        text = f.read()
    raw = [unname(s.rstrip("\r").expandtabs(8)) for s in text.rstrip("\n").split("\n")]
    if not raw[0].startswith("$ "):
        raise ValueError(f"{p.name}: line 1 is not a '$ …' command")
    key = f"{folder}/{p.name.split('-')[0]}"
    if key in CMD_LINES:
        k = CMD_LINES[key]
    else:
        k = 1
        while k < len(raw) and raw[k - 1].rstrip().endswith("\\"):
            k += 1
    cmd_lines = [raw[0][2:]] + raw[1:k]
    body = raw[k:]
    code_ = 0
    if body and re.fullmatch(r"\[exit -?\d+\]", body[-1]):
        code_ = int(body[-1][6:-1])
        body = body[:-1]
    return Capture(cmd_lines, body, code_, raw, p, key)


_CPROMPT = re.compile(r"^(\S+@[0-9a-f]+:\S*[$#]|[0-9a-f]{12}:\S*#)\s(.*)$")


def at_prompt(cap, n: int) -> tuple[str, str]:
    """A command typed INSIDE a container, as the capture recorded it on file line n:
    'app@20a4…:/app$ uvicorn …' -> ('app@20a4…:/app$', 'uvicorn …'). Use it with type_at()."""
    cap = capture(cap) if isinstance(cap, str) else cap
    s = cap.line(n)
    m = _CPROMPT.match(s)
    if not m:
        raise ValueError(f"{cap.path.name}:{n} is not a container prompt line: {s!r}")
    return m.group(1), m.group(2)


def container_prompt(cap, n: int) -> str:
    """Only the prompt of file line n (a bare prompt line like 'app@…:/app$' works too)."""
    cap = capture(cap) if isinstance(cap, str) else cap
    s = cap.line(n).rstrip()
    if re.fullmatch(r"\S+@[0-9a-f]+:\S*[$#]|[0-9a-f]{12}:\S*#", s):
        return s
    return at_prompt(cap, n)[0]


def md_plain(s: str) -> str:
    """Markdown stripped for a card: '**', backticks and link brackets go, list bullets become '•',
    a table row '| a | b |' becomes 'a · b'."""
    s = s.rstrip()
    if s.lstrip().startswith("|"):
        cells = [c.strip() for c in s.strip().strip("|").split("|")]
        s = " · ".join(c for c in cells if c)
    s = s.replace("**", "").replace("`", "")
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    s = re.sub(r"^(\s*)[*-] ", r"\1• ", s)
    s = re.sub(r"^#+\s*", "", s)
    return s


def recorded(file: str, *nums, plain: bool = True) -> list[str]:
    """Lines of assets/terminal/expected/<file> ('oslogin-ssh-keys-add', 'oslogin')
    by FILE line number (ints or (a, b) ranges). The '# …' provenance header lines are refused;
    plain=True strips the markdown (md_plain). For EXPECTED(...) and RECORDED(...) panels."""
    stem = file[:-4] if file.endswith(".txt") else file
    p = EXPECTED / f"{stem}.txt"
    if not p.exists():
        hits = sorted(EXPECTED.glob(f"{stem}-*.txt"))
        if len(hits) != 1:
            raise FileNotFoundError(f"expected/{stem}: {[h.name for h in hits]}")
        p = hits[0]
    raw = p.read_text(encoding="utf-8").rstrip("\n").split("\n")
    out_ = []
    for r in nums:
        a, b = (r, r) if isinstance(r, int) else r
        for n in range(a, b + 1):
            s = raw[n - 1]
            if s.startswith("# "):
                raise ValueError(f"{p.name}:{n} is a provenance header, never shown")
            s = s.expandtabs(4)
            out_.append(unname(md_plain(s) if plain else s))
    return out_

def soft(lines, n: int = 65) -> list:
    """Long lines broken at their last space that fits `n` characters (the text is unchanged, only
    the row break moves; a token longer than a row breaks at the edge). Items may be (text, colour)."""
    out_ = []
    for x in lines:
        s, c = (x, None) if isinstance(x, str) else x
        while len(s) > n:
            k = s.rfind(" ", 0, n + 1)
            if k > 0 and s[:k].strip():
                out_.append((s[:k].rstrip(), c))
                s = s[k + 1:]
            else:
                out_.append((s[:n], c))
                s = s[n:]
        out_.append((s, c))
    return [s if c is None else (s, c) for s, c in out_]


def cut(s: str, after: str, ellipsis: str = "…") -> str:
    """The line cut right after `after` (first occurrence), ending in '…'."""
    i = s.index(after) + len(after)
    return s[:i] + ellipsis


def from_phrase(s: str, phrase: str, ellipsis: str = "…") -> str:
    """script.md's `from "…"`: the line from `phrase` on, after a '…' ("…(ModuleNotFoundError …")."""
    i = s.index(phrase)
    return ellipsis + s[i:] if i else s


# ------------------------------------------------------------------ the running example
USER = "student"
P_VM = "student@cheese-app-vm:~$"                                 # vm/00: the Debian 12 stand-in
P_LAPTOP = "student@laptop:~$"
P_HOME = P_LAPTOP
P_REPO = "student@laptop:~/cheese-app-v3$"
P_FRONTEND = "student@laptop:~/cheese-app-v3/src/frontend-react$"
P_API = "student@laptop:~/cheese-app-v3/src/api-service$"
P_VDB = "student@laptop:~/cheese-app-v3/src/vector-db$"
P_DEPLOY = "student@laptop:~/cheese-app-v3/src/deployment$"
T_VM = "cheese-app-vm"
T_LAPTOP = "laptop"
T_TOOLBOX = "laptop · toolbox"
T_NEW = "laptop · new terminal"


def _toolbox_prompt() -> str:
    """The toolbox prompt exactly as b02d:77 printed it ('root@<id>:/app#'): never typed by hand."""
    try:
        return capture("b02d").raw[76].rstrip()
    except Exception:                                           # noqa: BLE001 (keeps imports working)
        return "root@toolbox:/app#"


P_TOOLBOX = _toolbox_prompt()                                    # root@<12 hex>:/app#  (id never read)


def toolbox_prompt(path: str = "/app") -> str:
    """P_TOOLBOX with its path swapped: toolbox_prompt('/secrets'), toolbox_prompt('/app/deploy_images'),
    toolbox_prompt('/app/deploy_single_vm') (the cd's of S12-S16)."""
    user_host = P_TOOLBOX.split(":", 1)[0]
    return f"{user_host}:{path}#"


PROJECT_PH = "your-gcp-project"            # b01, b02d, b07 (never a real id)
PROJECT_README = "ac215-project"           # the README's default: show it with default_tag()
IP_PH = "<instance_ip>"                    # Pulumi's output, never digits
VM_IP_PH = "<Your VM IP Address>"          # README:222
NETWORK = "cheese-app-network"             # part 1's Docker network (and part 2's VPC: same name)
APPNET = "appnetwork"                      # part 2's Docker network (setup_containers.py)
C_VDB = "cheese-app-vector-db"
C_API = "api-service"
C_FRONT = "frontend"
C_NGINX = "nginx"
C_LOADER = "vector-db-cli"                 # the one-shot loader (--rm, no name)
C_TOOLBOX = "cheese-app-deployment"
PORTS = {"vdb": "8000", "api": "9000", "front": "3000", "nginx": "80"}
CHUNKS = 14356                             # vm/27: the eleven 'Finished inserting' lines
BOOK_CHUNKS = (923, 714, 3569, 926, 2623, 1198, 1146, 678, 2147, 269, 163)
BOOK_LINES = (37, 50, 69, 82, 99, 113, 127, 140, 156, 168, 180)   # their vm/27 file lines
assert sum(BOOK_CHUNKS) == CHUNKS
STAMP_1 = "20261105233500"                 # b34:42, the preview's tag
STAMP_2 = "20261105233939"                 # b35b:17, the up's tag (a later run: a new stamp)
STAGES_MANUAL = ("1 Push", "2 Setup VM", "3 Deploy containers", "4 Web server")       # slide 8
SIX_STEPS = ("Setup", "Images", "VM", "Provision", "Containers", "Web server")         # slide 19
SIX_FILES = ("docker-shell.sh", "deploy_images/", "create_instance.py", "provision_instance.py",
             "setup_containers.py", "setup_webserver.py")
PROVIDERS = ("gcp", "docker-build", "docker", "command")                               # b34 plugins
EXPORTS = ("instance_name", "instance_ip", "zone", "persistent_disk_name", "ssh_user", "ssh_command")
DOMINOES = ("format", "mkdir", "mount", "timers", "upgrade", "packages", "Docker", "pip", "group")
LAMPS = ("activate key", "set project", "registry helper", "state bucket", "pulumi login")  # entrypoint 10-27
ENV_NAMES = ("GCP_PROJECT", "GCP_REGION", "GCP_ZONE", "GOOGLE_APPLICATION_CREDENTIALS", "PULUMI_BUCKET")
MOUNTS = (("Docker daemon", "/var/run/docker.sock"), ("src/deployment", "/app"),
          ("../../../secrets", "/secrets"), ("docker_config.json", "/root/.docker/config.json"),
          ("../api-service", "/api-service"), ("../frontend-react", "/frontend-react"),
          ("../vector-db", "/vector-db"))                                             # docker-shell.sh:35-43
ROLES_DEPLOY = ("Compute Admin", "Compute OS Login", "Artifact Registry Administrator",
                "Kubernetes Engine Admin", "Service Account User", "Storage Admin")      # README:241-246
ROLES_SERVICE = ("Storage Object Viewer", "Vertex AI Administrator", "Artifact Registry Reader")  # README:253-255

# ------------------------------------------------------------------ sources
# assets/source/<path> = dlops-io/cheese-app-v3 @ 3ecef56 (README.md, src/…), unchanged
NAMED_LINES = {"src/vector-db/cli.py": (75, 440)}     # name the instructor: never in a panel's range


def _src(path: str) -> Path:
    p = SOURCE / path
    if p.exists() and p.is_file():
        return p
    raise FileNotFoundError(f"assets/source/{path}")


def source_text(path: str) -> str:
    """An assets/source file ('README.md', 'src/deployment/deploy_images/__main__.py' …), masked."""
    return unname(_src(path).read_text(encoding="utf-8"))


def excerpt(path: str, first: int, last: int) -> str:
    """Lines first..last (1-based, inclusive) of assets/source/<path>."""
    return "\n".join(source_text(path).split("\n")[first - 1:last])


def readme(n: int) -> str:
    """README.md line n, stripped."""
    return excerpt("README.md", n, n).strip()


def readme_lines(a: int, b: int, plain: bool = True) -> str:
    """README lines a..b as card text ('\\n' joined, blank lines and fences dropped, markdown
    stripped): readme_card((10, 16), readme_lines(10, 16))."""
    rows = excerpt("README.md", a, b).split("\n")
    rows = [r for r in rows if r.strip() and not r.strip().startswith("```")]
    return "\n".join(md_plain(r) if plain else r for r in rows)


_LANG = {".py": "python", ".toml": "toml", ".sh": "bash", ".md": "markdown", ".yaml": "yaml",
         ".yml": "yaml", ".txt": "text", ".json": "json", ".lock": "toml", ".html": "html",
         ".js": "javascript", ".jsx": "jsx", ".css": "css", ".template": "nginx", ".conf": "nginx"}


def _lang(name: str) -> str:
    if name.startswith("Dockerfile"):
        return "docker"
    return _LANG.get(Path(name).suffix, "text")


def code(path: str, first: int, last: int | None = None, language: str | None = None, focus=None,
         font_size: float = 22, shown: str | None = None, max_lines: int = 12, cuts: dict | None = None,
         dedent: bool = False, elide: dict | None = None):
    """CODE(path: first–last) of script.md: a code_panel quoting assets/source/<path>, header
    '<path> · lines a–b'. <= 12 lines. The panel must fit the frame (22 pt holds ~66 characters a
    line, 20 pt ~74); a wider panel raises and names the line: cut it with cuts={file_line: 'text it
    ends after'} (a GREY '…' follows) or elide={file_line: 'middle text'} (replaced by a GREY '…'), or
    font_size=20. .code .header; highlight with code_span(p.code, k, "x") / line_bar(p.code, k,
    colour), k = file line - first. dedent=True removes the common leading indentation.
    shown='deploy_images/__main__.py' shortens the header path."""
    last = first if last is None else last
    if last - first + 1 > max_lines:
        raise ValueError(f"CODE {path}: {last - first + 1} lines; never more than {max_lines} on screen")
    for n in NAMED_LINES.get(path, ()):
        if first <= n <= last:
            raise ValueError(f"CODE {path}: line {n} names the instructor; keep it out of the range")
    text = excerpt(path, first, last)
    if dedent:
        import textwrap
        text = textwrap.dedent(text)
    lines = text.split("\n")
    cuts = cuts or {}
    for n, after in cuts.items():
        lines[n - first] = cut(lines[n - first], after)
    elide = elide or {}
    for n, mid in elide.items():
        if mid not in lines[n - first]:
            raise ValueError(f"CODE {path}:{n}: {mid!r} not in the line")
        lines[n - first] = lines[n - first].replace(mid, "…", 1)
    language = language or _lang(Path(path).name)
    p = code_panel("\n".join(lines), shown or path, first, language, focus=focus, font_size=font_size)
    if p.width > 2 * SAFE_X - 0.1:
        longest = max(range(len(lines)), key=lambda i: len(lines[i].expandtabs(4)))
        raise ValueError(f"CODE {path}: {p.width:.2f} wide at {font_size} pt leaves the frame (line "
                         f"{first + longest}, {len(lines[longest])} characters): cuts={{{first + longest}: "
                         f"'...'}} or font_size=20 (74 characters fit at 20 pt)")
    for n in list(cuts) + list(elide):
        code_span(p.code, n - first, "…").set_color(S.GREY)
    return p


def readme_card(lines, body, quote: bool = False, card_w: float | None = None, size: float = 22,
                name: str = "README.md") -> VGroup:
    """A GREY README card: header 'README.md · line n' (or 'lines a–b' for a tuple) and the README's
    own words (str: '\\n' separates rows, label font; or any mobject). quote=True adds a quote bar.
    .frame .head .body"""
    where = f"line {lines}" if isinstance(lines, int) else f"lines {lines[0]}–{lines[1]}"
    head = VGroup(mono(name, CAPTION, S.GREY), label(f"· {where}", CAPTION, S.GREY)).arrange(RIGHT, buff=0.12)
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


# ------------------------------------------------------------------ trackers (BRIEF / script.md)
SECTIONS = {
    "M": "Deployment to GCP (Manual)",
    "P": "Deployment to GCP (Single VM Instance)",
}
STEPS = {
    "M": ["Local check", "Docker login", "Push images", "Create VM", "Install Docker", "Make folders",
          "Secret file", "Docker network", "Vector DB", "Load vectors", "API service", "Frontend",
          "nginx.conf", "Run nginx", "Open site"],
    "P": ["Enable APIs", "Service accounts", "Run toolbox", "Check tools", "OS Login", "SSH key",
          "Upload key", "Inventory (skip)", "Images stack", "Images up", "VM stack", "VM up", "Check VM",
          "Destroy"],
}
assert len(STEPS["M"]) == 15 and len(STEPS["P"]) == 14
TRACKER_KEYS = tuple(SECTIONS)
EXTRA_KINDS = ("our spelling", "not for you", "recording only", "or edit the file")


def place_tracker(tr: ReadmeTracker) -> ReadmeTracker:
    """Pin a tracker to the house corner (left edge -6.5, top 3.5)."""
    tr.shift(np.array([TRACK_LEFT - tr.get_left()[0], TRACK_TOP - tr.get_top()[1], 0]))
    return tr


def _suffix(extra) -> str:
    if not extra:
        return ""
    if extra is True:
        return " · extra"
    if extra in EXTRA_KINDS:
        return f" · extra · {extra}"
    if isinstance(extra, str):
        return " · " + extra
    raise ValueError(f"extra={extra!r}")


def _caption(tr: ReadmeTracker, k: int, extra) -> Text:
    if not k:
        return steady("", tr.size, tr.hi_color).next_to(tr.dots, RIGHT, buff=0.25)
    s = f"step {k} of {len(tr.steps)}: {tr.steps[k - 1]}"
    suf = _suffix(extra)
    t = steady(s + suf, tr.size, tr.hi_color, t2c={suf.strip(" ·"): S.GREY} if suf else None)
    return t.next_to(tr.dots, RIGHT, buff=0.25)


def tracker(key: str, step: int | None = None, extra=False) -> ReadmeTracker:
    """Tracker `key` ('M' manual, 'P' Pulumi) at `step` (1-based; None = no step lit yet), placed
    top-left: 'README › <section>', one dot per step, 'step k of N: <step>' + the GREY extra suffix
    (extra=True ' · extra'; 'our spelling' / 'not for you' / 'recording only' → ' · extra · …')."""
    tr = ReadmeTracker(SECTIONS[key], STEPS[key])
    tr.key = key
    if step:
        tr.set_step(step)
    tr.remove(tr.caption)
    tr.caption = _caption(tr, step or 0, extra)
    tr.extra = extra
    tr.add(tr.caption)
    return place_tracker(tr)


def tracker_m(step: int | None = None, extra=False) -> ReadmeTracker:
    """README › Deployment to GCP (Manual), 15 steps (S02-S07)."""
    return tracker("M", step, extra)


def tracker_p(step: int | None = None, extra=False) -> ReadmeTracker:
    """README › Deployment to GCP (Single VM Instance), 14 steps, Destroy included (S10-S16)."""
    return tracker("P", step, extra)


def track(tr: ReadmeTracker, k: int | None = None, extra=False, run_time: float = 0.5):
    """ANIM: move the tracker to step k (None: stay) and set/clear the extra suffix (see tracker()).
    Use this, never tr.goto(). The caption cross-fades in place."""
    k = tr.k if k is None else k
    anims = []
    if k != tr.k:
        for i, d in enumerate(tr.dots, start=1):
            col = tr.hi_color if i == k else (S.GREY if i < k else S.GREY_DARK)
            anims.append(d.animate.set_color(col).scale((1.5 if i == k else 1.0) / (d.width / 0.12)))
    old, new = tr.caption.copy(), _caption(tr, k, extra)

    def fade_swap(m, a):
        src, f = (old if a < 0.5 else new), abs(1 - 2 * a)
        c = src.copy()
        for g, g0 in zip(c.family_members_with_points(), src.family_members_with_points()):
            g.set_fill(opacity=g0.get_fill_opacity() * f).set_stroke(opacity=g0.get_stroke_opacity() * f)
        m.become(c)

    anims.append(UpdateFromAlphaFunc(tr.caption, fade_swap))
    tr.k, tr.extra = k, extra
    return AnimationGroup(*anims, run_time=run_time)


def lref(slides: str) -> VGroup:
    """The GREY 'Lecture 20 · slides 21–24' tag, top right (one slide: 'slide 7'), only while that
    slide's picture or idea is on screen: lref("7"), lref("7–8"), lref("8, 24"), lref("19–20, 25")."""
    return lecture_ref(20, slides)


# ------------------------------------------------------------------ terminals
def term(prompt: str = P_LAPTOP, rows: int = 10, title: str | None = T_LAPTOP, width: float = 12.6,
         size: float = 22, place: bool = True) -> Terminal:
    """The house terminal: 12.6 wide, 22 pt, 65 characters a row, centred, bottom edge at BOTTOM.
    Height = rows x 0.403 + 0.85. Full width, or a 3-row strip (rows=3) under a picture. size=20
    gives 72 characters a row."""
    t = Terminal(prompt=prompt, width=width, rows=rows, size=size, title=title)
    if place:
        t.shift(np.array([-t.box.get_center()[0], BOTTOM - t.box.get_bottom()[1], 0]))
    return t


def vm_term(rows: int = 10, prompt: str = P_VM) -> Terminal:
    """Title 'cheese-app-vm', prompt student@cheese-app-vm:~$ (the Debian 12 stand-in, vm/ captures)."""
    return term(prompt, rows, T_VM)


def laptop_term(rows: int = 10, prompt: str = P_LAPTOP) -> Terminal:
    """Title 'laptop' (a01-a06, p01-p05, b01-b02d before the toolbox prompt)."""
    return term(prompt, rows, T_LAPTOP)


def toolbox_term(rows: int = 10, path: str = "/app") -> Terminal:
    """Title 'laptop · toolbox', prompt read from b02d:77 with `path` (b03-b46)."""
    return term(toolbox_prompt(path), rows, T_TOOLBOX)


def new_term(rows: int = 10, prompt: str = P_FRONTEND) -> Terminal:
    """Title 'laptop · new terminal' (S03: 'a new terminal · not a docker shell')."""
    return term(prompt, rows, T_NEW)


def type_at(scene, t: Terminal, cap, n: int, type_time: float | None = None):
    """PLAYS: a command typed at a CONTAINER prompt, as file line n of the capture recorded it: the
    terminal's prompt becomes that container prompt (printed from the file, never invented), then the
    command types. Returns the typed line."""
    p, cmd = at_prompt(cap, n)
    t.set_prompt(p)
    return type_cmd(scene, t, cmd, type_time)

def resize(scene, t: Terminal, rows: int, keep=None, extra=(), run_time: float = 0.8) -> Terminal:
    """PLAYS: grow or shrink terminal `t` to `rows` (bottom edge kept). It keeps its last lines (at
    most `keep`), or exactly the line mobjects in `keep` (a list). `extra`: animations alongside."""
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
    if gone:
        for ln in gone:
            t.lines.remove(ln)
        scene.play(FadeOut(VGroup(*gone)), run_time=0.25)
        scene.remove(*gone)
    anims = [Transform(t.box, ref.box), Transform(t.bar, ref.bar), t.dots.animate.move_to(ref.dots)]
    if t.title is not None:
        anims.append(t.title.animate.move_to(ref.title))
    for i, ln in enumerate(kept):
        anims.append(ln.animate.shift(ref._slot(i) - ln.strut.get_corner(UL)))
    scene.play(*anims, *extra, run_time=run_time)
    t.rows = rows
    return t


def retitle(t: Terminal, title: str):
    """ANIM: the terminal's title changes in place (e.g. 'laptop' -> 'laptop · second tab')."""
    new = mono(title, CAPTION, S.GREY).move_to(t.title)
    return Transform(t.title, new)


def room(scene, t: Terminal, n: int, run_time: float = 0.3) -> None:
    """PLAYS: make room for n new rows the gentle way: the oldest rows fade where they are, then the
    rest slide up (the toolkit's own scroll sails old rows over the tracker)."""
    over = len(t.lines) + n - t.rows
    if over <= 0:
        return
    gone = VGroup(*t.lines.submobjects[:over])
    stay = VGroup(*t.lines.submobjects[over:])
    for m in gone:
        t.lines.remove(m)
    scene.play(FadeOut(gone), run_time=run_time * 0.4)
    scene.remove(gone, *gone.get_family())
    if len(stay):
        scene.play(stay.animate.shift(UP * t.pitch * over), run_time=run_time * 0.6)


def bare_prompt(scene, t: Terminal):
    """PLAYS: the prompt returns (no output): a prompt line with nothing typed yet."""
    room(scene, t, 1)
    ln = t.type(scene, "", type_time=0)
    ln.bare = True
    return ln


def _soft_fold(t: Terminal):
    def fold(text: str, first_prefix: int = 0) -> list[str]:
        n = t.max_chars
        return [text[i:i + n] for i in range(0, len(text), n)] or [text]
    return fold


def type_cmd(scene, t: Terminal, cmd: str, type_time: float | None = None, prompt: bool = True,
             soft: bool | None = None):
    """PLAYS: type at the waiting prompt (replacing a bare prompt line if there is one; room is made
    first). A long command folds at a space outside quotes with ' \\' (Terminal.fold). soft=True
    soft-wraps at the row edge instead, like a real terminal (no ' \\'; the rows join back to the
    exact command): the default (None) picks it when a single token is too long to fold cleanly
    (the IMAGE / WEB_EMAIL exports, gs:// URIs). prompt=False types a continuation row with no
    prompt (a README row after a trailing '\\'). Returns the line, or a VGroup with .rows."""
    if len(t.lines) and getattr(t.lines[-1], "bare", False):
        last = t.lines[-1]
        t.lines.remove(last)
        scene.remove(last, *last.submobjects)
    keep = t.prompt
    if not prompt:
        t.set_prompt("")
    if soft is None:
        soft = any(len(tok) > t.max_chars - 8 for tok in cmd.split(" "))
    if soft:
        t.fold = _soft_fold(t)
    try:
        p = t.prompt + (" " if t.prompt else "")
        room(scene, t, len(t.fold(p + cmd, first_prefix=len(p))))
        ln = t.type(scene, cmd, type_time)
    finally:
        t.set_prompt(keep)
        if soft:
            del t.fold
    if soft and hasattr(ln, "rows"):
        assert "".join(r.text for r in ln.rows) == p + cmd, "soft wrap must join back to the command"
    return ln


def type_capture(scene, t: Terminal, cap, type_time: float | None = None, prompts=None) -> list:
    """PLAYS: type a capture's command exactly as its file lines spell it (cap: a Capture or a
    capture name). A row that follows a trailing '\\' is a continuation (no prompt); every other row
    is a separate command at the prompt (b10's three, b14's two). vm/44 (QUOTED) types rows 2.. as
    continuation rows of one quoted argument, soft-wrapped, never folded with ' \\'. prompts: a list
    with the prompt to set before each command row (None keeps the terminal's). type_time: per row.
    Returns the list of typed lines (each a line or a folded VGroup)."""
    cap = capture(cap) if isinstance(cap, str) else cap
    out_, cont = [], False
    quoted = cap.key in QUOTED
    k = 0
    for i, row in enumerate(cap.cmd_lines):
        if quoted and i > 0:
            out_.append(type_cmd(scene, t, row, type_time, prompt=False, soft=True))
            continue
        if not cont and prompts is not None and k < len(prompts) and prompts[k]:
            t.set_prompt(prompts[k])
        if not cont:
            k += 1
        out_.append(type_cmd(scene, t, row, type_time, prompt=not cont))
        cont = row.rstrip().endswith("\\")
    return out_


def type_lines(scene, t: Terminal, rows, type_time: float | None = None) -> list:
    """PLAYS: type a README command block given as its rows (verbatim, ' \\' continuations kept):
    the same continuation rule as type_capture(). For README rows typed with no capture."""
    out_, cont = [], False
    for row in rows:
        out_.append(type_cmd(scene, t, row, type_time, prompt=not cont))
        cont = row.rstrip().endswith("\\")
    return out_


def readme_rows(a: int, b: int) -> list[str]:
    """README lines a..b as command rows (verbatim, right-stripped; blank rows and code fences
    dropped) for type_lines(): e.g. readme_rows(389, 389) is the destroy line."""
    rows = [s.rstrip() for s in excerpt("README.md", a, b).split("\n")]
    rows = [s for s in rows if not s.strip().startswith("```")]
    return [s for s in rows if s.strip()]


def out(scene, t: Terminal, lines, wrap: bool = False, run_time: float = 0.6, lag: float = 0.08,
        chunk: int | None = None, color=OUTPUT) -> VGroup:
    """PLAYS: print capture lines (text or (text, colour)) in chunks that fit the box (`chunk` rows,
    default all rows), making room the gentle way. wrap=True breaks long lines at their last space
    that fits (soft()); otherwise a long line is refused (cut it, or wrap). Returns the new rows."""
    items = soft(lines, t.max_chars) if wrap else list(lines)
    for x in items:
        s = x if isinstance(x, str) else x[0]
        if len(s) > t.max_chars:
            raise ValueError(f"out(): {len(s)} > {t.max_chars} characters: wrap=True or cut it: {s!r}")
    items = [(x, color) if isinstance(x, str) else x for x in items]
    k = max(1, min(t.rows, chunk or t.rows))
    chunks = [items[i:i + k] for i in range(0, len(items), k)]
    rows = VGroup()
    for ch in chunks:
        room(scene, t, len(ch))
        rows.add(*t.print(scene, ch, run_time=run_time / len(chunks) + 0.1, lag=lag))
    return rows


def cd_prompt(scene, t: Terminal, new_prompt: str, color=LAPTOP, run_time: float = 0.6):
    """PLAYS: after `cd`, the prompt changes; a bare prompt line appears and its path flashes."""
    t.set_prompt(new_prompt)
    ln = bare_prompt(scene, t)
    path = new_prompt.split(":", 1)[1].rstrip("$# ")
    scene.play(*[g.animate.set_color(color) for g in substring(ln, path)], run_time=run_time * 0.5)
    scene.play(*[g.animate.set_color(PROMPT_PATH) for g in substring(ln, path)], run_time=run_time * 0.5)
    scene.add(t)                             # re-seat the terminal as one mobject
    return ln


def rows_of(line) -> list:
    """The rows of a typed line (a folded command has several)."""
    return list(line.rows) if hasattr(line, "rows") else [line]


def _row_of(line):
    """A terminal line, or the last row of a folded command."""
    return line.rows[-1] if hasattr(line, "rows") else line


def beside(mob, line, buff: float = 0.45, min_x: float | None = None):
    """Put `mob` right of terminal row `line` (a folded command: its last row), centred on it."""
    row = _row_of(line)
    x = row.strut.get_right()[0] + buff
    if min_x is not None:
        x = max(x, min_x)
    return mob.move_to([x + mob.width / 2, row.strut.get_center()[1], 0])


def covers_text(mob, line) -> bool:
    """True when `mob` (a tag, a chip) would hide glyphs of terminal row `line`."""
    hides = any(type(m).__name__ in ("Text", "MarkupText", "Paragraph")
                or (isinstance(m, Rectangle) and m.get_fill_opacity() > 0.3) for m in mob.get_family())
    g = getattr(_row_of(line), "glyphs", None)
    if not hides or g is None or not len(g):
        return False
    l_, r, b, tp = mob.get_left()[0], mob.get_right()[0], mob.get_bottom()[1], mob.get_top()[1]
    return any(l_ < ch.get_right()[0] + 0.03 and r > ch.get_left()[0] - 0.03
               and b < ch.get_top()[1] and tp > ch.get_bottom()[1]
               for ch in g.family_members_with_points())


def attach(scene, line, mob):
    """Make `mob` part of terminal row `line` (it scrolls and fades with it)."""
    row = _row_of(line)
    scene.remove(mob)
    row.add(mob)
    scene.add(row)
    return mob


def pin(scene, line, mob, run_time: float = 0.4, anim=None):
    """PLAYS: show `mob` (placed with beside()) and make it part of the row, so it scrolls with it.
    Refuses a tag that would cover the row's text."""
    row = _row_of(line)
    if covers_text(mob, row):
        raise ValueError(f"pin(): this {mob.width:.2f}-wide tag would cover the text of its row; "
                         "use a row_tag, put it on an output row, on the title bar, or under the terminal")
    scene.play(anim or FadeIn(mob, shift=LEFT * 0.1), run_time=run_time)
    return attach(scene, row, mob)


def unpin(scene, line, mob, *extra, run_time: float = 0.3):
    """PLAYS: fade a pinned mark out and take it off its row (so it never snaps back)."""
    row = _row_of(line)
    if mob in row.submobjects:
        row.remove(mob)
    scene.play(FadeOut(mob), *extra, run_time=run_time)
    scene.remove(mob)


def on_bar(t: Terminal, mob, buff: float = 0.15):
    """Put a row-sized tag (turn_row(), extra_row() …) on terminal t's title bar, at its right end:
    for a command row too long to hold a tag beside it. Add/FadeIn it yourself (it does not scroll)."""
    return mob.move_to([t.box.get_right()[0] - buff - mob.width / 2, t.box.get_top()[1] - t.bar_h / 2, 0])


def under_term(t: Terminal, mob, buff: float = 0.12):
    """Put `mob` just above terminal t's top edge, right-aligned (chips 'about' the terminal)."""
    return mob.next_to(t.box, UP, buff=buff).align_to(t.box, RIGHT)


def row_tag(parts, color=S.GREY, size: float = 20) -> VGroup:
    """A tag that fits inside one 22 pt terminal row (0.36 tall; the house tag is taller).
    parts: a string, or (text, 'mono'|'label') pairs. .box .text"""
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


def turn_row() -> VGroup:
    """'▶ your turn' sized for a terminal row (YELLOW): beside(turn_row(), line); pin(...)."""
    return row_tag("▶ your turn", TURN)


def extra_row(kind=None) -> VGroup:
    """'extra' sized for a terminal row (GREY); kind 'recording only' -> 'extra · recording only'."""
    return row_tag("extra" + (f" · {kind}" if kind else ""), S.GREY)


def time_row() -> VGroup:
    """'at the time of recording' sized for a terminal row (GREY)."""
    return row_tag("at the time of recording", S.GREY)


def cost_row(s: str) -> VGroup:
    """A GOLD cost tag sized for a terminal row (never an amount: see cost_tag())."""
    return row_tag(_no_amount(s), COST)


def no_panel_chip(s: str = "shown without output · not captured") -> VGroup:
    """The GREY chip under a command typed with no output panel (S14's cd ../deploy_single_vm)."""
    return grey_chip(s)


def flash_tag(scene, tg, color=None, scale: float = 1.12, run_time: float = 0.8, *extra) -> None:
    """PLAYS: flash a tag's words and pulse an unfilled copy of its outline (then drops the copy).
    Never Indicate a whole tag, and never animate tg.box itself (the filled box hides its word)."""
    color = color or tg.text.get_color()
    edge = tg.box.copy().set_fill(opacity=0)
    scene.play(Indicate(tg.text, color=color, scale_factor=scale),
               edge.animate(rate_func=there_and_back).set_stroke(width=4), *extra, run_time=run_time)
    scene.remove(edge)


def each(pieces, color, scale: float = 1.08, lag: float = 0.15):
    """ANIM: flash scattered pieces one by one."""
    return LaggedStart(*[Indicate(p, color=color, scale_factor=scale) for p in pieces], lag_ratio=lag)


def under(g, color, stroke: float = 4, pad: float = 0.03, y: float | None = None) -> Line:
    """A line under glyphs `g`."""
    y = g.get_bottom()[1] - 0.06 if y is None else y
    return Line([g.get_left()[0] - pad, y, 0], [g.get_right()[0] + pad, y, 0], color=color,
                stroke_width=stroke)


def hl_bar(g, color=TURN, opacity: float = 0.25, buff: float = 0.05) -> Rectangle:
    """A translucent bar behind glyphs `g` (insert it behind: row.submobjects.insert(0, bar))."""
    return Rectangle(width=g.width + 2 * buff, height=g.height + 2 * buff, stroke_width=0) \
        .set_fill(color, opacity).move_to(g)


def ring(g, color=TURN, buff: float = 0.08, stroke: float = 3, dashed: bool = False):
    """An outline box around `g` (hides nothing: fine over terminal text)."""
    r = RoundedRectangle(width=g.width + 2 * buff, height=g.height + 2 * buff,
                         corner_radius=0.08, stroke_color=color, stroke_width=stroke).move_to(g)
    if dashed:
        d = DashedVMobject(r, num_dashes=max(12, int((r.width + r.height) * 7)), dashed_ratio=0.55)
        return d.set_stroke(color, stroke)
    return r


def strike(g, color=ERR, stroke: float = 4) -> Line:
    """A strike-through line over `g`."""
    return Line(g.get_left() + LEFT * 0.06, g.get_right() + RIGHT * 0.06, color=color, stroke_width=stroke)


# ------------------------------------------------------------------ tags and chips (>= 20 pt)
_AMOUNT_RE = re.compile(r"[$€£¢]|\d\s*(cents?|dollars?|USD)\b|free tier", re.I)


def _no_amount(s: str) -> str:
    """Cost text never carries a money amount or a free-tier figure, except an approximation said
    as one (S14: '≈ $2/day … roughly: check the pricing calculator')."""
    if _AMOUNT_RE.search(s) and not ("≈" in s and "roughly" in s):
        raise ValueError(f"cost tag {s!r}: no prices or free-tier figures on screen")
    return s


def your_turn() -> VGroup:
    """YELLOW '▶ your turn' tag (house size: beside a card or panel, not inside a terminal row)."""
    return tag("▶ your turn", TURN)


def extra_tag(kind: str | None = None) -> VGroup:
    """GREY 'extra' tag; kind 'our spelling' / 'not for you' / 'recording only' / 'not in the README'
    -> 'extra · our spelling' …"""
    return tag("extra" + (f" · {kind}" if kind else ""), S.GREY)


def illustration_tag(s: str = "illustration") -> VGroup:
    """On every browser drawing, the prerequisites card and lecture redrawings of cloud machinery
    (schematic; never a screenshot): illustration_tag('illustration · README:13–18')."""
    return tag(s, S.GREY)


def expected_tag(source: str | None = None) -> VGroup:
    """'expected · README:306–314': the README's own OS Login snippet (the only expected panel)."""
    return tag("expected" + (f" · {source}" if source else ""), S.GREY)


def recorded_tag(source: str | None = None) -> VGroup:
    """'recorded · <source>' (kept for symmetry; this video quotes no recorded output)."""
    return tag("recorded" + (f" · {source}" if source else ""), S.GREY)


def recording_tag(s: str = "at the time of recording") -> VGroup:
    """Beside versions on first show."""
    return tag(s, S.GREY)


def erratum_tag(s: str = "erratum") -> VGroup:
    """On every README/slide slip (the narration says 'a small slip' or 'a small note'):
    erratum_tag('erratum · add src/')."""
    return tag(s, S.GREY)


def cost_tag(s: str) -> VGroup:
    """The GOLD money tag ('billed while it runs · the disk while it exists'). Raises on an amount
    unless it says '≈' and 'roughly' (S14's one price line)."""
    return tag(_no_amount(s), COST)


def disk_chip(s: str = "disk · about 5 GB on the VM disk") -> VGroup:
    """The GOLD-outlined 'disk' chip (S06: the 5.07 GB API image). .box .text"""
    return chip(s, COST, size=20)


def grey_chip(s: str, size: float = 20, mono_font: bool = False, color=S.GREY) -> VGroup:
    """A GREY chip for a short note ('your editor', 'extra arguments · none here'). .box .text"""
    return chip(s, color, size=size, font=MONO if mono_font else None)


def editor_chip() -> VGroup:
    """'your editor': stands for an edit typed in the viewer's editor (b01's alternative)."""
    return grey_chip("your editor")


def dashed_chip(s: str, color=PAST, size: float = 20, mono_font: bool = False) -> VGroup:
    """A dashed chip: past/future things (Lecture 5, L19–L22, the Agent Chat group). .box .text"""
    t = mono(s, size, color) if mono_font else label(s, size, color)
    ob = outline_box(t.width + 0.48, mono("|", size).height + 0.24, color, solid=False)
    t.move_to(ob)
    g = VGroup(ob, t)
    g.box, g.text = ob, t
    return g


def tool_chip(s: str, size: float = 20, mono_font: bool = True) -> VGroup:
    """A tool as a PURPLE chip (never a logo): uvicorn, FastAPI, Vite, nginx, http-server …"""
    return chip(s, TOOL, size=size, font=MONO if mono_font else None)


def err_chip(s: str, size: float = 20, mono_font: bool = True) -> VGroup:
    """A RED error chip: err_chip('422'), err_chip('502'). .box .text"""
    return chip(s, ERR, size=size, font=MONO if mono_font else None, fill_opacity=0.14)


def ok_chip(s: str, size: float = 20, mono_font: bool = False) -> VGroup:
    """A GREEN chip (a pass, '26 passed', 'start the API first'). .box .text"""
    return chip(s, OWN, size=size, font=MONO if mono_font else None)


def route_chip(s: str, size: float = 20, mono_font: bool = True) -> VGroup:
    """A PINK chip for a path, header or origin part: route_chip('/api'), route_chip('x=2'). .box .text"""
    return chip(s, ROUTE, size=size, font=MONO if mono_font else None)


def box_chip(s: str, size: float = 20, mono_font: bool = True) -> VGroup:
    """A TEAL chip for a container or image name. .box .text"""
    return chip(s, CONTAINER, size=size, font=MONO if mono_font else None)


def differ_chip(s: str = "yours will differ") -> VGroup:
    """GREY chip for container ids, network ids, UUIDs, timestamps (never read aloud)."""
    return grey_chip(s)


def file_card(path: str, color=LAPTOP, size: float = 20, dashed: bool = False) -> VGroup:
    """A file as a card: file glyph + mono path. .box .glyph .text"""
    g0 = file_glyph(0.34, color)
    t = mono(path, size, INK)
    row = VGroup(g0, t).arrange(RIGHT, buff=0.16)
    w, h = row.width + 0.45, row.height + 0.32
    b = outline_box(w, h, color, solid=not dashed, fill_opacity=0.1)
    row.move_to(b)
    g = VGroup(b, row)
    g.box, g.glyph, g.text = b, g0, t
    return g


def card(lines, color=S.GREY, size: float = 22, card_w: float | None = None, dashed: bool = False,
         head: str | None = None, buff: float = 0.16) -> VGroup:
    """A plain card of short lines (label font; an item may be a mobject), e.g. the erratum and
    honest-note cards. head: a GREY first line. .frame .body .head"""
    items = [label(s, size, INK) if isinstance(s, str) else s for s in lines]
    hd = label(head, CAPTION, S.GREY) if head else None
    body = VGroup(*items).arrange(DOWN, aligned_edge=LEFT, buff=buff)
    inner = VGroup(*([hd] if hd else []), body).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    w = card_w or inner.width + 0.6
    frame = outline_box(w, inner.height + 0.5, color, solid=not dashed, fill_opacity=0.08)
    if not dashed:
        frame.fill.set_fill(S.GREY_DARKER, 1)
    inner.move_to(frame).align_to(frame, LEFT).shift(RIGHT * 0.3)
    g = VGroup(frame, inner)
    g.frame, g.body, g.head = frame, body, hd
    return g


def question_card(text: str, size: float = 26, color=TURN, card_w: float | None = None) -> VGroup:
    """A YELLOW-outlined question card ('The page talks to 3000. …', the parked question, 'Test
    yourself'); '\\n' breaks rows. .frame .body"""
    rows = VGroup(*[label(s, size, INK) for s in text.split("\n")]).arrange(DOWN, buff=0.14)
    w = card_w or rows.width + 0.8
    frame = RoundedRectangle(width=w, height=rows.height + 0.6, corner_radius=0.16, stroke_color=color,
                             stroke_width=3).set_fill(S.BG, 1)
    rows.move_to(frame)
    g = VGroup(frame, rows)
    g.frame, g.body = frame, rows
    return g


def quote_card(file: str, nums, kind: str = "expected", source: str | None = None, size: float = 22,
               card_w: float | None = None, color=INK, width_chars: int = 60, mono_font: bool = False) -> VGroup:
    """EXPECTED(expected/<file>: nums) or RECORDED(…): a GREY-outlined panel quoting those lines
    (markdown stripped), with the tag '<kind> · <source>' on its top edge (right). kind 'expected' |
    'recorded' | 'illustration'. nums: an int, a range tuple, or a list. Long lines wrap at
    `width_chars`. mono_font=True keeps the file verbatim (no markdown stripping, indentation kept,
    mono 20 pt rows; long rows break at the edge): the OS Login YAML snippet,
    quote_card("oslogin-ssh-keys-add", (2, 10), source="README:306–314", mono_font=True, width_chars=60).
    .frame .body (.body[i] = row i) .tag"""
    nums = [nums] if isinstance(nums, (int, tuple)) else list(nums)
    if mono_font:
        raw = [s for s in recorded(file, *nums, plain=False) if s.strip()]
        lines = []
        for s_ in raw:
            while len(s_) > width_chars:
                lines.append(s_[:width_chars])
                s_ = "  " + s_[width_chars:]
            lines.append(s_)
        size = min(size, 20)
        body = VGroup(*[mono_line(s_, size, color) for s_ in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    else:
        lines = soft([s for s in recorded(file, *nums) if s.strip()], width_chars)
        body = VGroup(*[label(s, size, color) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    w = card_w or body.width + 0.7
    frame = box(w, body.height + 0.65, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
    body.move_to(frame).align_to(frame, LEFT).shift(RIGHT * 0.35 + DOWN * 0.06)
    tg = tag(kind + (f" · {source}" if source else ""), S.GREY)
    tg.move_to(frame.get_corner(UR) + np.array([-tg.width / 2 - 0.2, 0, 0]))
    g = VGroup(frame, body, tg)
    g.frame, g.body, g.tag = frame, body, tg
    return g


def ponder(scene, question: str, seconds: float = 8, center=None, width: float = 9.5) -> VGroup:
    """PLAYS a PONDER card (YELLOW timer drains over `seconds`). center=(x, y) moves it (default:
    the frame's centre). The frame is opaque, so the card may sit over a set piece. Returns the card
    (still on screen): FadeOut it at the start of the next block."""
    c = ponder_card(question, width=width)
    c[0].set_fill(S.BG, 1)        # opaque: at 0.96 the words of a set piece behind it ghost through
    if center is not None:
        c.move_to([center[0], center[1], 0])
    scene.play(FadeIn(c, scale=0.95), run_time=0.6)
    bar = c[3]
    target = bar.copy().scale(0.001, about_point=bar.get_start())
    scene.play(bar.animate(rate_func=linear).become(target), run_time=seconds)
    return c


# ------------------------------------------------------------------ small glyphs and motion
def outline_box(box_w: float, box_h: float, color, solid: bool = False, fill_opacity: float = 0.1,
                radius: float = 0.14, stroke: float = 2.5) -> VGroup:
    """A box whose outline is made of dashes: dashed (solid=False) or closed (solid=True, faint
    fill). A dashed one Transforms cleanly into a solid one of the same size. .fill .frame"""
    r = RoundedRectangle(width=box_w, height=box_h, corner_radius=min(radius, box_h / 2, box_w / 2))
    n = max(12, int((box_w + box_h) * 7))
    frame = DashedVMobject(r.copy(), num_dashes=n, dashed_ratio=0.999 if solid else 0.55)
    frame.set_stroke(color, stroke)
    fill = r.copy().set_stroke(width=0).set_fill(color, fill_opacity if solid else 0)
    g = VGroup(fill, frame)
    g.fill, g.frame = fill, frame
    return g


def arrow(a, b, color=S.GREY, stroke: float = 3, buff: float = 0.12, arc: float = 0.0) -> Arrow:
    """A plain thin arrow between two mobjects or points (curved by `arc` radians)."""
    pa = a if isinstance(a, np.ndarray) else a.get_center()
    pb = b if isinstance(b, np.ndarray) else b.get_center()
    return Arrow(pa, pb, buff=buff if not isinstance(a, np.ndarray) else 0, color=color, path_arc=arc,
                 stroke_width=stroke, tip_length=0.18, max_tip_length_to_length_ratio=0.25)


def route(a, b, arc: float = 0.0, color=ROUTE, stroke: float = 4) -> Arrow:
    """A PINK route arrow (curved by `arc` radians) from a to b (points or mobjects)."""
    pa = a if isinstance(a, np.ndarray) else a.get_center()
    pb = b if isinstance(b, np.ndarray) else b.get_center()
    return Arrow(pa, pb, buff=0.15 if not isinstance(a, np.ndarray) else 0, path_arc=arc, color=color,
                 stroke_width=stroke, tip_length=0.2, max_tip_length_to_length_ratio=0.2)


def travel(mob, path, run_time: float = 1.2):
    """ANIM: `mob` rides along `path` (a Line/Arrow/VMobject)."""
    return MoveAlongPath(mob, path, run_time=run_time)


def bounce(mob, point, run_time: float = 0.9):
    """ANIM: `mob` goes to `point` and comes back."""
    back = mob.get_center().copy()
    return Succession(mob.animate(run_time=run_time * 0.5).move_to(point),
                      mob.animate(run_time=run_time * 0.5).move_to(back))


def pulse_dot(color=ROUTE, r: float = 0.09) -> Dot:
    """A request pulse (PINK dot)."""
    return Dot(radius=r, color=color)


def check_glyph(h: float = 0.3, color=OWN, stroke: float = 5) -> VMobject:
    m = VMobject(stroke_color=color, stroke_width=stroke)
    m.set_points_as_corners([[-0.5 * h, 0.05 * h, 0], [-0.15 * h, -0.4 * h, 0], [0.55 * h, 0.45 * h, 0]])
    return m


def cross_glyph(h: float = 0.3, color=ERR, stroke: float = 5) -> VGroup:
    a = h / 2
    return VGroup(Line([-a, -a, 0], [a, a, 0]), Line([-a, a, 0], [a, -a, 0])).set_stroke(color, stroke)


def image_block(name: str | None = "image", box_w: float = 2.2, box_h: float = 0.8, color=IMAGE,
                size: float = 20, mono_font: bool = False) -> VGroup:
    """The image (TEAL block, solid) with an optional name inside (20 pt). .block .text"""
    b = RoundedRectangle(width=box_w, height=box_h, corner_radius=0.1, stroke_color=color,
                         stroke_width=3).set_fill(color, 0.22)
    g = VGroup(b)
    g.block, g.text = b, None
    if name:
        t = (mono if mono_font else label)(name, size, INK).move_to(b)
        g.add(t)
        g.text = t
    return g

def ear(text: str | None = "0.0.0.0:8080", color=ROUTE, h: float = 0.36, size: float = 20) -> VGroup:
    """A listening ear (PINK half-ring) + its mono address to the left. .glyph .text"""
    a = Arc(radius=h / 2, start_angle=PI / 2, angle=PI, color=color, stroke_width=5)
    a2 = Arc(radius=h / 4, start_angle=PI / 2, angle=PI, color=color, stroke_width=3)
    gl = VGroup(a, a2)
    g = VGroup(gl)
    g.glyph, g.text = gl, None
    if text:
        t = mono(text, size, color).next_to(gl, LEFT, buff=0.12)
        g.add(t)
        g.text = t
    return g


def envelope(text: str = "PORT=8080", color=S.GREY, size: float = 20, env_w: float | None = None) -> VGroup:
    """An envelope with a mono line on it (an env var handed in). .body .flap .text"""
    t = mono(text, size, INK)
    w = env_w or t.width + 0.5
    h = 0.62
    body = Rectangle(width=w, height=h, stroke_color=color, stroke_width=2.5).set_fill(S.BG, 1)
    flap = VMobject(stroke_color=color, stroke_width=2.5).set_points_as_corners(
        [body.get_corner(UL), body.get_center() + UP * 0.14, body.get_corner(UR)])
    t.move_to(body).shift(DOWN * 0.12)
    g = VGroup(body, flap, t)
    g.body, g.flap, g.text = body, flap, t
    return g

def key_glyph(key_w: float = 0.8, color=COST, dashed: bool = True) -> VGroup:
    """A key (bow, shaft, two teeth): L3's JSON key file; GOLD dashed by default."""
    r = key_w * 0.2
    bow = Circle(radius=r, stroke_color=color, stroke_width=4)
    shaft = Line([r, 0, 0], [key_w - r, 0, 0], color=color, stroke_width=5)
    t1 = Line([key_w * 0.62, 0, 0], [key_w * 0.62, -r * 0.8, 0], color=color, stroke_width=5)
    t2 = Line([key_w * 0.78, 0, 0], [key_w * 0.78, -r * 0.6, 0], color=color, stroke_width=5)
    g = VGroup(bow, shaft, t1, t2)
    if dashed:
        g = VGroup(*[DashedVMobject(m, num_dashes=8).set_stroke(color, 4) for m in g])
    return g.move_to(ORIGIN)

def folder_icon(h: float = 0.4, color=CLOUD) -> VGroup:
    return folder_glyph(h, color)


def file_icon(name: str | None = None, color=INK, h: float = 0.36, size: float = 20) -> VGroup:
    """A file glyph with an optional mono name to its right. .glyph .text"""
    gl = file_glyph(h, color)
    g = VGroup(gl)
    g.glyph, g.text = gl, None
    if name:
        t = mono(name, size, INK).next_to(gl, RIGHT, buff=0.12)
        g.add(t)
        g.text = t
    return g

def disk(w: float = 0.42, color=S.GREY) -> VGroup:
    """A small disk (cylinder) icon: an instance's local disk, the laptop's disk."""
    top = Circle(radius=w / 2, stroke_color=color, stroke_width=2.5).stretch(0.35, 1)
    bot = top.copy().shift(DOWN * w * 0.45)
    sides = VGroup(Line(top.get_left(), bot.get_left()), Line(top.get_right(), bot.get_right()))
    sides.set_stroke(color, 2.5)
    return VGroup(sides, bot, top.set_fill(color, 0.3))


def you(text: str | None = "you", color=YOU, h: float = 0.6, size: float = 20) -> VGroup:
    """A GREY person ('you', the deployer) with a label under it. .figure .text"""
    fig = person_icon(color, h)
    g = VGroup(fig)
    g.figure, g.text = fig, None
    if text:
        t = label(text, size, color).next_to(fig, DOWN, buff=0.1)
        g.add(t)
        g.text = t
    return g

def cloud_shape(text: str | None = None, color=CLOUD, cloud_w: float = 2.4, size: float = 20,
                dashed: bool = False) -> VGroup:
    """A cloud outline (Agent Platform BLUE, googletrans' endpoint ORANGE) with up to two rows of text
    ('\\n'). .shape .text"""
    h = cloud_w * 0.5
    blobs = [Circle(radius=h * 0.42).shift([-cloud_w * 0.25, -h * 0.08, 0]),
             Circle(radius=h * 0.55).shift([0, h * 0.08, 0]),
             Circle(radius=h * 0.42).shift([cloud_w * 0.25, -h * 0.08, 0])]
    base = RoundedRectangle(width=cloud_w * 0.85, height=h * 0.55, corner_radius=h * 0.27).shift(DOWN * h * 0.2)
    from manim import Union
    shape = Union(*blobs, base).set_stroke(color, 3).set_fill(color, 0.12)
    if dashed:
        shape = DashedVMobject(shape, num_dashes=40).set_stroke(color, 3)
    g = VGroup(shape)
    g.shape, g.text = shape, None
    if text:
        t = VGroup(*[label(s, size, INK) for s in text.split("\n")]).arrange(DOWN, buff=0.06)
        t.move_to(shape).shift(DOWN * 0.08)
        g.add(t)
        g.text = t
    return g


def bucket(name: str | None = None, box_w: float = 1.0, color=CLOUD, size: float = 20,
           mono_font: bool = True) -> VGroup:
    """A storage bucket (BLUE pail) with an optional name under it. .pail .text"""
    h = box_w * 0.8
    pail = Polygon([-box_w / 2, h / 2, 0], [box_w / 2, h / 2, 0], [box_w * 0.38, -h / 2, 0],
                   [-box_w * 0.38, -h / 2, 0], stroke_color=color, stroke_width=3).set_fill(color, 0.18)
    rim = Line([-box_w / 2 - 0.05, h / 2, 0], [box_w / 2 + 0.05, h / 2, 0], color=color, stroke_width=5)
    g = VGroup(pail, rim)
    g.pail, g.text = VGroup(pail, rim), None
    if name:
        t = (mono if mono_font else label)(name, size, INK).next_to(pail, DOWN, buff=0.12)
        g.add(t)
        g.text = t
    return g


# ------------------------------------------------------------------ set-piece base
class Piece(VGroup):
    """A set piece. PLAYS methods add their new mobjects to the piece after playing them, and take
    parts away with drop(); the piece itself stays one top-level mobject on the scene."""

    owner = None            # a piece inside another piece (V1's laptop is a V5) plays through its owner

    def root(self):
        """The outermost piece that holds this one (itself when it stands alone)."""
        p = self
        while getattr(p, "owner", None) is not None:
            p = p.owner
        return p

    def _ensure(self, scene):
        r = self.root()
        if r not in scene.mobjects:
            scene.add(r)

    def heal(self, scene):
        """Re-seat the piece (its outermost owner) as ONE top-level mobject. Animating a group that is
        not itself on the scene (a glyph_range, a code_span) makes Manim split every parent that holds
        its members into top-level pieces; scene.add(piece) undoes that. The PLAYS methods call it."""
        scene.add(self.root())

    def show(self, scene, *mobs, anims=None, run_time: float = 0.6, extra=(), into=None):
        """PLAYS: FadeIn (or `anims`) of new mobjects, then they become parts of the piece (of the
        sub-group `into` when given). Returns the first mobject (or all, as a tuple)."""
        self._ensure(scene)
        a = list(anims) if anims is not None else [FadeIn(m) for m in mobs]
        scene.play(*a, *extra, run_time=run_time)
        scene.remove(*mobs)
        (into if into is not None else self).add(*mobs)
        self.heal(scene)
        return mobs[0] if len(mobs) == 1 else mobs

    def _detach(self, m):
        """Take m off the piece; a wrapper group that was never added itself (VGroup(a, b) of parts
        shown separately) has its members taken off instead."""
        found = False
        for sub in self.get_family():
            if m in sub.submobjects:
                sub.remove(m)
                found = True
        if not found:
            for c in list(m.submobjects):
                self._detach(c)

    def drop(self, scene, *mobs, run_time: float = 0.4, extra=(), shift=None):
        """PLAYS: fade parts of the piece out and take them off it (they never snap back)."""
        mobs = [m for m in mobs if m is not None]
        for m in mobs:
            self._detach(m)
        anims = [FadeOut(m, shift=shift) if shift is not None else FadeOut(m) for m in mobs]
        scene.play(*anims, *extra, run_time=run_time)
        scene.remove(*mobs)
        self.heal(scene)

    def swap(self, scene, old, new, run_time: float = 0.6, extra=(), into=None):
        """PLAYS: `old` (a part) morphs into `new` (not yet shown); afterwards `new` is the part."""
        parent = into
        if parent is None:
            for sub in self.get_family():
                if old in sub.submobjects:
                    parent = sub
                    break
        self._detach(old)
        scene.add(old)
        scene.play(ReplacementTransform(old, new), *extra, run_time=run_time)
        scene.remove(old, new)
        (parent if parent is not None else self).add(new)
        self.heal(scene)
        return new


def keep_inside(m, margin: float = 0.05):
    """Shift `m` (no scaling) so that it sits inside the safe frame x in [-6.6, 6.6], y in [-3.6, 3.6]."""
    dx = max(0.0, -SAFE_X + margin - m.get_left()[0]) - max(0.0, m.get_right()[0] - SAFE_X + margin)
    dy = max(0.0, -SAFE_Y + margin - m.get_bottom()[1]) - max(0.0, m.get_top()[1] - SAFE_Y + margin)
    return m.shift(np.array([dx, dy, 0]))


def _morph_anims(olds, news):
    return [Transform(o, n) for o, n in zip(olds, news)]


class _Anchored(Piece):
    """A piece laid out from an invisible anchor dot (its origin): self.p(x, y) is the point (x, y)
    of the layout wherever the piece has moved to."""

    def __init__(self, **kw):
        super().__init__(**kw)
        self.ref = Dot(radius=0.001).set_opacity(0)
        self.add(self.ref)

    def p(self, x: float, y: float) -> np.ndarray:
        return self.ref.get_center() + np.array([x, y, 0.0])


def browser_icon(icon_w: float = 1.0, color=LAPTOP, name: str | None = "browser", size: float = 20) -> VGroup:
    """A small GREY browser window glyph (no logo) with an optional name under it. .window .text"""
    h = icon_w * 0.7
    fr = RoundedRectangle(width=icon_w, height=h, corner_radius=0.08, stroke_color=color,
                          stroke_width=3).set_fill(PANEL, 1)
    bar = Line(fr.get_corner(UL) + DOWN * 0.18, fr.get_corner(UR) + DOWN * 0.18, color=color, stroke_width=2)
    win = VGroup(fr, bar)
    g = VGroup(win)
    g.window, g.text = win, None
    if name:
        t = label(name, size, color).next_to(fr, DOWN, buff=0.1)
        g.add(t)
        g.text = t
    return g


# ------------------------------------------------------------------ L18 glyphs
def tint(color, k: float = 0.16) -> str:
    """An OPAQUE fill colour: `color` mixed into the background (boxes that may sit over lines)."""
    from manim import ManimColor
    return ManimColor(S.BG).interpolate(ManimColor(color), k)


def cbox(rows, box_w: float = 3.0, box_h: float = 0.84, color=CONTAINER, size: float = 20,
         dashed: bool = False, name_color=INK, mono_font: bool = True) -> VGroup:
    """A container box: opaque tinted fill, outline in `color`, a name of one or two rows at its
    left ('cheese-app-' / 'api-service'). rows: a str ('\\n' splits) or a list. .frame .name"""
    rows = rows.split("\n") if isinstance(rows, str) else list(rows)
    name = VGroup(*[(mono if mono_font else label)(r, size, name_color) for r in rows]).arrange(
        DOWN, aligned_edge=LEFT, buff=0.06)
    fr = RoundedRectangle(width=box_w, height=box_h, corner_radius=0.1, stroke_color=color,
                          stroke_width=3).set_fill(tint(color), 1)
    if dashed:
        fr.set_stroke(opacity=0)
        d = DashedVMobject(fr.copy().set_fill(opacity=0), num_dashes=max(12, int((box_w + box_h) * 7)),
                           dashed_ratio=0.55).set_stroke(color, 3)
        fr = VGroup(fr, d)
    if name.width > box_w - 0.25:
        raise ValueError(f"cbox: name {rows} ({name.width:.2f}) does not fit a {box_w:.2f}-wide box")
    name.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.15)
    g = VGroup(fr, name)
    g.frame, g.name = fr, name
    return g


def door(port: str, color=ROUTE, size: float = 20, door_w: float | None = None, mono_font: bool = True) -> VGroup:
    """A published-port door: a PINK plate with the host port ('9000'), sitting on a wall (also V3's
    socket and plates: door('lo · 127.0.0.1', S.GREY, mono_font=False)). .plate .text"""
    t = (mono if mono_font else label)(port, size, INK)
    w = door_w or max(0.85, t.width + 0.3)
    p = RoundedRectangle(width=w, height=0.46, corner_radius=0.08, stroke_color=color,
                         stroke_width=3).set_fill(tint(color, 0.22), 1)
    t.move_to(p)
    g = VGroup(p, t)
    g.plate, g.text = p, t
    return g


def lamp(state: str = "off", r: float = 0.28) -> VGroup:
    """A probe lamp: 'off' (GREY outline), 'green', 'amber', 'red', 'dashed' (GREY dashed, S14)."""
    col = {"off": S.GREY, "green": OWN, "amber": AMBER, "red": ERR, "dashed": S.GREY}[state]
    c = Circle(radius=r, stroke_color=col, stroke_width=3).set_fill(col, 0 if state in ("off", "dashed") else 0.85)
    if state == "dashed":
        c = DashedVMobject(c, num_dashes=12).set_stroke(col, 3)
    glow = Circle(radius=r * 1.45, stroke_width=0).set_fill(col, 0 if state in ("off", "dashed") else 0.18)
    return VGroup(glow, c)


# ------------------------------------------------------------------ Browser (V1, V7, drawings)
class Browser(Piece):
    """A schematic GREY browser window (no logo, tag it illustration_tag()): title bar, an address
    field with the URL in PINK (label font, 20 pt; a URL that does not fit raises: widen win_w),
    an empty page area. Built centred at ORIGIN.
        .frame .address .page (invisible page rectangle) .rows (page content, a VGroup)
    PLAYS goto(scene, url) the address changes · fill(scene, rows, mono_font=False, color=INK)
    page rows (str or mobjects; replaces the old rows; must fit) · reload(scene) a GREY sweep over the
    page (rows stay) · clear(scene). ANIM flash(color) the page rows pulse."""

    def __init__(self, url: str = "localhost:3000", win_w: float = 4.6, win_h: float = 3.2,
                 size: float = 20, **kw):
        super().__init__(**kw)
        self.win_w, self.win_h, self.size = win_w, win_h, size
        fr = RoundedRectangle(width=win_w, height=win_h, corner_radius=0.12, stroke_color=LAPTOP,
                              stroke_width=2.5).set_fill(PANEL, 1)
        bar_h = 0.52
        bar = Line(fr.get_corner(UL) + DOWN * bar_h, fr.get_corner(UR) + DOWN * bar_h, color=LAPTOP,
                   stroke_width=2)
        dots = VGroup(*[Dot(radius=0.045, color=S.GREY_DARK) for _ in range(3)]).arrange(RIGHT, buff=0.08)
        dots.move_to(fr.get_corner(UL) + np.array([0.3, -bar_h / 2, 0]))
        field = RoundedRectangle(width=win_w - 0.67, height=0.38, corner_radius=0.19, stroke_width=0)
        field.set_fill(TERM_BG, 1).move_to(fr.get_top() + DOWN * bar_h / 2).align_to(fr, RIGHT).shift(LEFT * 0.12)
        self.frame, self.bar, self.field = fr, VGroup(bar, dots), field
        self.address = self._addr(url)
        self.page = Rectangle(width=win_w - 0.3, height=win_h - bar_h - 0.25, stroke_width=0,
                              fill_opacity=0).move_to(fr.get_bottom() + UP * (win_h - bar_h) / 2)
        self.rows = VGroup()
        self.url = url
        self.add(fr, self.bar, field, self.address, self.page, self.rows)

    def _addr(self, url: str) -> Text:
        t = label(url, self.size, ROUTE)
        if t.width > self.field.width - 0.24:
            raise ValueError(f"Browser: '{url}' ({t.width:.2f}) does not fit win_w={self.win_w}: widen it")
        return t.move_to(self.field).align_to(self.field, LEFT).shift(RIGHT * 0.12)

    def goto(self, scene, url: str, run_time: float = 0.5):
        """PLAYS: the address field shows `url`."""
        new = self._addr(url)
        self.url = url
        self.address = self.swap(scene, self.address, new, run_time=run_time)
        return self.address

    def _rows(self, rows, mono_font: bool, color, buff: float):
        items = [(mono if mono_font else label)(s, self.size, color) if isinstance(s, str) else s for s in rows]
        g = VGroup(*items).arrange(DOWN, aligned_edge=LEFT, buff=buff)
        if g.width > self.page.width - 0.2 or g.height > self.page.height - 0.2:
            raise ValueError(f"Browser.fill: {g.width:.2f} x {g.height:.2f} does not fit the page "
                             f"{self.page.width - 0.2:.2f} x {self.page.height - 0.2:.2f}")
        return g.move_to(self.page).align_to(self.page, UL).shift(np.array([0.15, -0.15, 0]))

    def fill(self, scene, rows, mono_font: bool = False, color=INK, buff: float = 0.14, run_time: float = 0.5):
        """PLAYS: the page shows `rows` (replacing what it showed). Returns the new rows group."""
        g = self._rows(rows, mono_font, color, buff)
        old = list(self.rows.submobjects)
        if old:
            self.drop(scene, *old, run_time=0.25)
        self.show(scene, *g.submobjects, run_time=run_time, into=self.rows)
        return self.rows

    def clear(self, scene, run_time: float = 0.3):
        """PLAYS: an empty page."""
        if len(self.rows):
            self.drop(scene, *list(self.rows.submobjects), run_time=run_time)

    def reload(self, scene, run_time: float = 0.7):
        """PLAYS: a GREY sweep runs down the page (a full page reload)."""
        sw = Rectangle(width=self.page.width, height=0.25, stroke_width=0).set_fill(S.GREY, 0.45)
        sw.move_to(self.page.get_top() + DOWN * 0.12)
        scene.add(sw)
        scene.play(sw.animate.move_to(self.page.get_bottom() + UP * 0.12), run_time=run_time, rate_func=linear)
        scene.remove(sw)

    def flash(self, color=TURN):
        """ANIM: the window's outlines flash `color` and back (text keeps its colours)."""
        return self.animate(rate_func=there_and_back).set_stroke(color)

    def at(self, fx: float, fy: float) -> np.ndarray:
        """A point in the page area: fx, fy in [-1, 1] (0, 0 = page centre)."""
        c = self.page.get_center()
        return c + np.array([fx * self.page.width / 2, fy * self.page.height / 2, 0])


# ------------------------------------------------------------------ L20 tags, glyphs, small pieces
def default_tag(s: str = "the README's default · change to yours") -> VGroup:
    """GREY tag beside the README's `ac215-project` (b15, b19, b32, b41, b42, vm/27, vm/30 …)."""
    return tag(s, S.GREY)


def default_row() -> VGroup:
    """default_tag sized for a terminal row: 'README default · change it'."""
    return row_tag("README default · change it", S.GREY)


def sticky(text: str, color=TURN, size: float = 20) -> VGroup:
    """A small YELLOW sticky note ('hold that thought: S13'; '\\n' breaks rows). .frame .body"""
    rows = VGroup(*[label(s, size, INK) for s in text.split("\n")]).arrange(DOWN, buff=0.08)
    fr = Polygon([-0.5, 0.5, 0], [0.5, 0.5, 0], [0.5, -0.32, 0], [0.32, -0.5, 0], [-0.5, -0.5, 0],
                 stroke_color=color, stroke_width=2.5).set_fill(tint(color, 0.18), 1)
    fr.stretch_to_fit_width(rows.width + 0.5).stretch_to_fit_height(rows.height + 0.4)
    rows.move_to(fr)
    g = VGroup(fr, rows)
    g.frame, g.body = fr, rows
    return g


def scissors(h: float = 0.5, color=ROUTE) -> VGroup:
    """Text-free PINK scissors (V3's prefix cut), blades pointing right."""
    r = h * 0.2
    ring1 = Circle(radius=r, stroke_color=color, stroke_width=4).move_to([-h * 0.55, h * 0.22, 0])
    ring2 = Circle(radius=r, stroke_color=color, stroke_width=4).move_to([-h * 0.55, -h * 0.22, 0])
    b1 = Line([-h * 0.38, h * 0.15, 0], [h * 0.55, -h * 0.12, 0], color=color, stroke_width=5)
    b2 = Line([-h * 0.38, -h * 0.15, 0], [h * 0.55, h * 0.12, 0], color=color, stroke_width=5)
    return VGroup(ring1, ring2, b1, b2)


def padlock(h: float = 0.4, color=ERR, text: str | None = None, size: float = 20) -> VGroup:
    """A padlock (RED: push refused; GOLD: retain_on_delete; YELLOW 'unknown' in a preview), with an
    optional label to its right. .glyph .text"""
    body = RoundedRectangle(width=h * 0.8, height=h * 0.6, corner_radius=h * 0.08, stroke_color=color,
                            stroke_width=3).set_fill(tint(color, 0.3), 1)
    shackle = Arc(radius=h * 0.25, start_angle=0, angle=PI, color=color, stroke_width=4)
    shackle.next_to(body, UP, buff=-0.01)
    gl = VGroup(shackle, body)
    g = VGroup(gl)
    g.glyph, g.text = gl, None
    if text:
        t = label(text, size, color).next_to(gl, RIGHT, buff=0.1)
        g.add(t)
        g.text = t
    return g


def key_icon(kind: str = "deploy", name: bool | str = True, key_w: float = 0.9, size: float = 20) -> VGroup:
    """V8's keys, coloured by power: 'deploy' = deployment.json (BLUE, RED rim: admin), 'service' =
    gcp-service.json (GREEN: read and run), 'ssh' = ssh-key-deployment (PURPLE: a shell on the VM).
    name=True writes the file name under it (label font 20), a str writes that. .glyph .text .kind"""
    col, rim, fname = {"deploy": (CLOUD, ERR, "deployment.json"), "service": (OWN, OWN, "gcp-service.json"),
                       "ssh": (TOOL, TOOL, "ssh-key-deployment")}[kind]
    r = key_w * 0.2
    bow = Circle(radius=r, stroke_color=rim, stroke_width=5).set_fill(col, 0.55)
    hole = Circle(radius=r * 0.35, stroke_width=0).set_fill(S.BG, 1)
    shaft = Line([r, 0, 0], [key_w - r * 0.3, 0, 0], color=col, stroke_width=6)
    t1 = Line([key_w * 0.62, 0, 0], [key_w * 0.62, -r * 0.8, 0], color=col, stroke_width=6)
    t2 = Line([key_w * 0.8, 0, 0], [key_w * 0.8, -r * 0.6, 0], color=col, stroke_width=6)
    gl = VGroup(shaft, t1, t2, bow, hole).move_to(ORIGIN)
    g = VGroup(gl)
    g.glyph, g.text, g.kind = gl, None, kind
    if name:
        t = label(fname if name is True else name, size, col if kind != "deploy" else INK)
        t.next_to(gl, DOWN, buff=0.12)
        g.add(t)
        g.text = t
    return g


def crate(name: str, crate_w: float = 1.9, crate_h: float = 0.62, color=IMAGE, size: float = 20,
          dashed: bool = False) -> VGroup:
    """A TEAL image crate (V6, S03) with a label-font name. .box .text"""
    b = RoundedRectangle(width=crate_w, height=crate_h, corner_radius=0.06, stroke_color=color,
                         stroke_width=3).set_fill(tint(color, 0.2), 1)
    if dashed:
        b = VGroup(b.set_stroke(opacity=0), DashedVMobject(b.copy().set_fill(opacity=0).set_stroke(opacity=1),
                                                           num_dashes=28).set_stroke(color, 3))
    t = label(name, size, INK)
    if t.width > crate_w - 0.2:
        raise ValueError(f"crate: '{name}' ({t.width:.2f}) does not fit crate_w={crate_w}")
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def console_form(title: str, fields, form_w: float = 6.4, size: float = 20, kind: str = "illustration") -> VGroup:
    """A schematic console page (GREY, no logo) with its `illustration` tag on the top edge: title,
    then rows (label, value[, colour]); value '☑ …' for ticks. Every text 20 pt, never scaled: a row
    that does not fit raises. .frame .title .rows (each row .label .value) .tag"""
    tt = label(title, 22, INK)
    rows = VGroup()
    for f in fields:
        lab, val = f[0], f[1]
        col = f[2] if len(f) > 2 else INK
        lt = label(lab, size, S.GREY)
        vt = label(val, size, col)
        row = VGroup(lt, vt).arrange(RIGHT, buff=0.3)
        row.label, row.value = lt, vt
        rows.add(row)
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    inner = VGroup(tt, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    if inner.width > form_w - 0.5:
        raise ValueError(f"console_form: {inner.width:.2f} wide does not fit form_w={form_w}")
    fr = box(form_w, inner.height + 0.75, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
    inner.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.3 + DOWN * 0.08)
    tg = tag(kind, S.GREY)
    tg.move_to(fr.get_corner(UR) + np.array([-tg.width / 2 - 0.2, 0, 0]))
    g = VGroup(fr, inner, tg)
    g.frame, g.title, g.rows, g.tag = fr, tt, rows, tg
    return g


class Checklist(Piece):
    """A GREY card of rows, each with an empty box that ticks: S10's 'APIs & Services' (illustration),
    S16's GOLD teardown list. Checklist(title, items, color=S.GREY, tag_text='illustration' or None,
    dashed=(indices drawn GREY-dashed), card_w=None). PLAYS tick(scene, i, color=OWN) · tick_all(scene).
    .frame .head .rows (row .box .text) .tag"""

    def __init__(self, title: str, items, color=S.GREY, tag_text: str | None = "illustration",
                 dashed=(), card_w: float | None = None, size: float = 20, **kw):
        super().__init__(**kw)
        hd = label(title, 22, INK)
        rows = VGroup()
        for i, it in enumerate(items):
            dash = i in dashed
            bx = Rectangle(width=0.3, height=0.3, stroke_color=S.GREY, stroke_width=2.5)
            if dash:
                bx = DashedVMobject(bx, num_dashes=8).set_stroke(S.GREY, 2.5)
            t = label(it, size, S.GREY if dash else INK) if isinstance(it, str) else it
            r = VGroup(bx, t).arrange(RIGHT, buff=0.2)
            r.box, r.text = bx, t
            rows.add(r)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        inner = VGroup(hd, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        w = card_w or inner.width + 0.7
        fr = box(w, inner.height + 0.7, color, fill=S.GREY_DARKER, fill_opacity=1)
        inner.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.32 + DOWN * 0.06)
        self.frame, self.head, self.rows = fr, hd, rows
        self.add(fr, inner)
        self.tag = None
        if tag_text:
            tg = tag(tag_text, S.GREY)
            tg.move_to(fr.get_corner(UR) + np.array([-tg.width / 2 - 0.2, 0, 0]))
            self.tag = tg
            self.add(tg)
        self.ticks = VGroup()
        self.add(self.ticks)

    def tick(self, scene, i: int, color=OWN, run_time: float = 0.4):
        """PLAYS: row i's box gets a tick (and lights `color` briefly)."""
        r = self.rows[i]
        ck = check_glyph(0.3, color).move_to(r.box).shift(UP * 0.04 + RIGHT * 0.03)
        self.show(scene, ck, anims=[Create(ck)], run_time=run_time, into=self.ticks,
                  extra=[Indicate(r.text, color=color, scale_factor=1.04)])
        return ck

    def tick_all(self, scene, color=OWN, lag: float = 0.3):
        for i in range(len(self.rows)):
            self.tick(scene, i, color, run_time=lag)


class SixSteps(Piece):
    """Slide 19's six-step strip: six numbered chips '1 Setup' … '6 Web server', each with its file
    under it in two label-font rows ('provision_' / 'instance.py'). Width 12.6 (x -6.3 .. 6.3 at ORIGIN),
    height ~1.35. current=k: chips < k ticked GREEN, chip k YELLOW; files=False leaves the files off.
    ANIM goto(k) (ticks earlier chips, lights chip k) · light(k, colour). PLAYS shrink_away(scene).
    .chips[i] (.box .text) .files[i] .checks[i] (i = 0..5)"""

    _SPLIT = ("docker-|shell.sh", "deploy_|images/", "create_|instance.py", "provision_|instance.py",
              "setup_|containers.py", "setup_|webserver.py")

    def __init__(self, current: int = 0, files: bool = True, strip_w: float = 12.6, **kw):
        super().__init__(**kw)
        n = len(SIX_STEPS)
        pitch = strip_w / n
        self.chips, self.files, self.checks = VGroup(), VGroup(), VGroup()
        for i, name in enumerate(SIX_STEPS):
            x = -strip_w / 2 + pitch * (i + 0.5)
            c = chip(f"{i + 1} {name}", S.GREY, size=20, pad_x=0.14)
            if c.width > pitch - 0.1:
                raise ValueError(f"SixSteps: chip {name!r} wider than {pitch:.2f}")
            c.move_to([x, 0.35, 0])
            self.chips.add(c)
            a, b = self._SPLIT[i].split("|")
            f = VGroup(label(a, 20, S.GREY), label(b, 20, S.GREY)).arrange(DOWN, buff=0.06)
            if f.width > pitch - 0.1:
                raise ValueError(f"SixSteps: file {self._SPLIT[i]!r} wider than {pitch:.2f}")
            f.next_to(c, DOWN, buff=0.14)
            self.files.add(f)
            ck = check_glyph(0.26, OWN).next_to(c, UP, buff=0.06)
            ck.set_opacity(0)
            self.checks.add(ck)
        self.add(self.chips, self.checks)
        if files:
            self.add(self.files)
        self.k = 0
        if current:
            self._apply(current)

    def _col(self, i: int, k: int):
        return TURN if i + 1 == k else (OWN if i + 1 < k else S.GREY)

    def _apply(self, k: int):
        for i, (c, ck) in enumerate(zip(self.chips, self.checks)):
            c.box.set_stroke(self._col(i, k))
            ck.set_opacity(1 if i + 1 < k else 0)
        self.k = k
        return self

    def goto(self, k: int, run_time: float = 0.5):
        """ANIM: chips before k ticked GREEN, chip k YELLOW (k=0: all GREY; k=7: all ticked)."""
        anims = []
        for i, (c, ck) in enumerate(zip(self.chips, self.checks)):
            anims += [c.box.animate.set_stroke(self._col(i, k)), ck.animate.set_opacity(1 if i + 1 < k else 0)]
        self.k = k
        return AnimationGroup(*anims, run_time=run_time)

    def light(self, k: int, color=TURN):
        """ANIM: chip k's outline flashes `color`."""
        return Indicate(self.chips[k - 1], color=color, scale_factor=1.06)

    def shrink_away(self, scene, run_time: float = 0.5):
        """PLAYS: the strip fades up and off (it is never pinned)."""
        scene.play(FadeOut(self, shift=UP * 0.3), run_time=run_time)
        scene.remove(self)


def six_steps(current: int = 0, files: bool = True) -> SixSteps:
    """The slide-19 strip (see SixSteps)."""
    return SixSteps(current, files)


class CostDial(VGroup):
    """The GOLD cost meter (from L1): a dial whose needle sweeps while something bills, with no
    digits. .run(scene, turns, seconds) sweeps it on; .freeze() stops it (on Delete). .needle
    .tracker .caption; radius 0.55 + caption under."""

    def __init__(self, radius: float = 0.55, caption: str | None = "cost", **kw):
        super().__init__(**kw)
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
        self.needle.clear_updaters()
        return self


# ------------------------------------------------------------------ shared drawing bits for V1-V3
def _dotted_rect(w: float, h: float, color, dash_ratio: float = 0.35, stroke: float = 3) -> VMobject:
    r = RoundedRectangle(width=w, height=h, corner_radius=0.18)
    return DashedVMobject(r, num_dashes=max(20, int((w + h) * 9)), dashed_ratio=dash_ratio).set_stroke(color, stroke)


def _panel(w: float, h: float, color=CLOUD, fill: float = 0.07, stroke: float = 3) -> RoundedRectangle:
    return RoundedRectangle(width=w, height=h, corner_radius=0.14, stroke_color=color,
                            stroke_width=stroke).set_fill(tint(color, fill), 1)


def svc_box(name: str, port: str | None = None, box_w: float = 1.9, box_h: float = 0.72, color=CONTAINER,
            dashed: bool = False, size: float = 20) -> VGroup:
    """V1's container box: opaque TEAL box, label-font name, optional PINK mono port row under it.
    .frame .name .port (None without a port)"""
    fr = RoundedRectangle(width=box_w, height=box_h, corner_radius=0.1, stroke_color=color,
                          stroke_width=3).set_fill(tint(color, 0.18), 1)
    if dashed:
        d = DashedVMobject(fr.copy().set_fill(opacity=0), num_dashes=max(12, int((box_w + box_h) * 7)),
                           dashed_ratio=0.55).set_stroke(color, 3)
        fr.set_stroke(opacity=0)
        fr = VGroup(fr, d)
    nm = label(name, size, INK)
    rows = [nm]
    pt = None
    if port:
        pt = mono(port, size, ROUTE)
        rows.append(pt)
    content = VGroup(*rows).arrange(DOWN, buff=0.04)
    if content.width > box_w - 0.2 or content.height > box_h - 0.06:
        raise ValueError(f"svc_box: {name!r}/{port!r} does not fit {box_w}x{box_h}")
    content.move_to(fr)
    g = VGroup(fr, content)
    g.frame, g.name, g.port = fr, nm, pt
    return g


def mini_browser(url: str, win_w: float | None = None, color=LAPTOP, size: float = 20) -> VGroup:
    """A one-bar GREY browser (three dots + PINK address), 0.62 tall: V1's test window. win_w=None
    fits the URL (at least 3.3); a given win_w raises when the URL does not fit. .frame .address"""
    if win_w is None:
        win_w = max(3.3, label(url, size).width + 0.85)
    fr = RoundedRectangle(width=win_w, height=0.62, corner_radius=0.12, stroke_color=color,
                          stroke_width=2.5).set_fill(PANEL, 1)
    dots = VGroup(*[Dot(radius=0.045, color=S.GREY_DARK) for _ in range(3)]).arrange(RIGHT, buff=0.08)
    dots.move_to(fr.get_left() + RIGHT * 0.3)
    t = label(url, size, ROUTE)
    if t.width > win_w - 0.75:
        raise ValueError(f"mini_browser: '{url}' ({t.width:.2f}) does not fit win_w={win_w}")
    t.move_to(fr).align_to(dots, LEFT).shift(RIGHT * 0.38)
    g = VGroup(fr, dots, t)
    g.frame, g.address = fr, t
    return g


def disk_cyl(w: float = 0.6, color=CLOUD) -> VGroup:
    """A BLUE persistent-disk cylinder (V1, V7) 0.6 wide."""
    top = Circle(radius=w / 2, stroke_color=color, stroke_width=3).stretch(0.32, 1)
    bot = top.copy().shift(DOWN * w * 0.5)
    body = Rectangle(width=w, height=w * 0.5, stroke_width=0).set_fill(tint(color, 0.25), 1).move_to(
        (top.get_center() + bot.get_center()) / 2)
    sides = VGroup(Line(top.get_left(), bot.get_left()), Line(top.get_right(), bot.get_right())).set_stroke(color, 3)
    bot_fill = bot.copy().set_stroke(width=0).set_fill(tint(color, 0.25), 1)
    return VGroup(bot_fill, body, sides, bot, top.set_fill(tint(color, 0.4), 1))


def pail(w: float = 0.9, color=CLOUD, rim=None, dashed: bool = False) -> VGroup:
    """A storage-bucket pail (state bucket: BLUE with a GREEN rim; models: GREY dashed)."""
    h = w * 0.8
    body = Polygon([-w / 2, h / 2, 0], [w / 2, h / 2, 0], [w * 0.38, -h / 2, 0], [-w * 0.38, -h / 2, 0],
                   stroke_color=color, stroke_width=3).set_fill(tint(color, 0.22), 1)
    rl = Line([-w / 2 - 0.05, h / 2, 0], [w / 2 + 0.05, h / 2, 0], color=rim or color, stroke_width=6)
    if dashed:
        body = DashedVMobject(body.set_fill(opacity=0), num_dashes=16).set_stroke(color, 3)
        rl = DashedLine(rl.get_start(), rl.get_end(), color=color, stroke_width=4)
    return VGroup(body, rl)


# ------------------------------------------------------------------ V1 · MasterDiagram
class MasterDiagram(_Anchored):
    """V1 · the lecture's deployment picture (slides 7, 21-24, 26, 27), grown step by step. Full frame,
    built around ORIGIN (place it there; over a 3-row strip it does not fit). Layout (scene units):
        laptop box  x -6.45 .. -3.35, y 0.35 .. 2.65 ('Your Machine', 'IDE / CLI' bar, 'Containers'
                    and six dashed TEAL squares); state bucket at (-5.6, -0.9) 'state' under it
        GCP outline x -2.7 .. 6.45, y -3.3 .. 1.45, dotted BLUE ('GCP' top-left)
                    manual=True: x 0.3 .. 6.45, y -3.05 .. 1.45 ('GCP' bottom-left) and the BLUE 'Docker Hub' panel outside
                    it (x -2.95 .. -0.35, y -2.4 .. -0.2); slide-8 stage chips along y -3.35
        registry    x -2.45 .. 0.25, y -2.95 .. -0.75 ('Artifact Registry', three image bars);
                    gcr_note '(GCR on the slides)' just above it
        models      GREY-dashed pail at (-1.1, 0.9) + 'v3 downloads its model / from GitHub'
        VM panel    x 0.6 .. 6.25, y -2.4 .. 1.15, 'Compute Instance (VM)' top-left; slots (centres):
                    nginx (4.65, 0.3) · front (1.95, -0.62) · api (4.95, -0.62) · vdb (4.95, -1.85) ·
                    loader (1.95, -1.85); disk cylinder (3.85, -2.75) on a cable, label to its right
        browser     one-bar window centred (4.65, 1.95), PINK address (width fits the URL, >= 3.3)
        door        PINK 'HTTP 80' plate at (4.65, 1.15) on the VM's top edge, or sitting on nginx (y 0.84)
    Keys of .parts: laptop state gcp hub registry gcr models vm disk front api vdb nginx door80 browser
    push pull hollow routes stages loader.
    PLAYS (each shows its part once; re-calling an existing part is a no-op returning it):
        laptop(title='Your Machine' | 'Local Computer') · gcp() · registry() (Docker Hub when manual) ·
        gcr_note() · models() · state() · vm() · disk(text='/mnt/disk-1') · box(key) for
        'front'|'api'|'vdb'|'nginx' · door(on='vm'|'nginx', text='HTTP 80') (moves onto nginx when it
        exists already) · browser(url) · push() laptop→registry arrow · pull() registry→VM arrow ·
        hollow() teaser's GREY hollow arrow laptop→VM · routes() request arrows browser→door→nginx→
        front/api, api→vdb (only between parts that exist) · loader(pour=True) the dashed loader pours
        dots into vdb and leaves · front_port_fix() slide 23's 'HTTP 80' ghost on frontend flips to 3000 ·
        stage_chips() (manual) · build(*keys).
        Stage shortcuts: stage21() stage22() stage23() stage24() stage27(url) teaser().
    ANIM light(key, colour) (outline) · normal(key) · light_stage(k) (manual chips: k YELLOW).
    .stage_row (VGroup of the four chips) · .slot[key] (centre points)."""

    SLOTS = {"nginx": (4.65, 0.3), "front": (1.95, -0.62), "api": (4.95, -0.62), "vdb": (4.95, -1.85),
             "loader": (1.95, -1.85)}

    def __init__(self, manual: bool = False, built=(), **kw):
        super().__init__(**kw)
        self.manual = manual
        self.parts = {}
        self.stage_row = None
        self.slot = {k: self.p(*v) for k, v in self.SLOTS.items()}
        for key in built:
            m = self._make(key)
            self.parts[key] = m
            self.add(m)

    # ---- builders (all positions through self.p)
    def _make(self, key: str, **kw):
        p = self.p
        if key == "laptop":
            title = kw.get("title", "Your Machine")
            fr = _panel(3.1, 2.3, LAPTOP, 0.06).move_to(p(-4.9, 1.5))
            t = label(title, 20, LAPTOP).move_to(p(-6.25, 2.42), aligned_edge=LEFT)
            bar = RoundedRectangle(width=2.7, height=0.4, corner_radius=0.08, stroke_color=LAPTOP,
                                   stroke_width=2).set_fill(PANEL, 1).move_to(p(-4.9, 1.92))
            bt = label("IDE / CLI", 20, INK).move_to(bar)
            ct = label("Containers", 20, INK).move_to(p(-6.25, 1.08), aligned_edge=LEFT)
            sq = VGroup(*[DashedVMobject(Square(0.36), num_dashes=10).set_stroke(CONTAINER, 2.5)
                          for _ in range(6)]).arrange_in_grid(2, 3, buff=0.14).move_to(p(-4.25, 1.06))
            g = VGroup(fr, t, bar, bt, ct, sq)
            g.frame, g.title, g.squares = fr, t, sq
            return g
        if key == "state":
            pl = pail(0.9, CLOUD, rim=OWN).move_to(p(-5.6, -0.8))
            t = label("state", 20, OWN).next_to(pl, DOWN, buff=0.12)
            g = VGroup(pl, t)
            g.frame = pl[0]
            return g
        if key == "gcp":
            if self.manual:
                fr = _dotted_rect(6.15, 4.5, CLOUD).move_to(p(3.375, -0.8))
            else:
                fr = _dotted_rect(9.15, 4.75, CLOUD).move_to(p(1.875, -0.925))
            corner = fr.get_corner(DL) + np.array([0.2, 0.3, 0]) if self.manual else \
                fr.get_corner(UL) + np.array([0.2, -0.3, 0])
            t = label("GCP", 22, CLOUD).move_to(corner, aligned_edge=LEFT)
            g = VGroup(fr, t)
            g.frame = fr
            return g
        if key == "registry":
            if self.manual:
                fr = _panel(2.6, 2.2, CLOUD).move_to(p(-1.65, -1.3))
                title = "Docker Hub"
                names = ("api-service", "frontend-react", "vector-db-cli")
            else:
                fr = _panel(2.7, 2.2, CLOUD).move_to(p(-1.1, -1.85))
                title = "Artifact Registry"
                names = ("Cheese App Image", "API Service Image", "Vector DB CLI")
            t = label(title, 20, CLOUD).move_to(fr.get_top() + DOWN * 0.28)
            bars = VGroup()
            for n in names:
                b = RoundedRectangle(width=fr.width - 0.3, height=0.42, corner_radius=0.06,
                                     stroke_color=CONTAINER, stroke_width=2).set_fill(tint(CONTAINER, 0.15), 1)
                bars.add(VGroup(b, label(n, 20, INK).move_to(b)))
            bars.arrange(DOWN, buff=0.1).next_to(t, DOWN, buff=0.16)
            g = VGroup(fr, t, bars)
            g.frame, g.title, g.bars = fr, t, bars
            return g
        if key == "gcr":
            reg = self.parts.get("registry") or self._make("registry")
            return label("(GCR on the slides)", 20, S.GREY).next_to(reg, UP, buff=0.1)
        if key == "models":
            pl = pail(0.8, PAST, dashed=True).move_to(p(-1.1, 0.9))
            cap = VGroup(label("v3 downloads its model", 20, S.GREY), label("from GitHub", 20, S.GREY))
            cap.arrange(DOWN, buff=0.06).next_to(pl, DOWN, buff=0.12)
            nm = label("Models", 20, S.GREY).next_to(pl, RIGHT, buff=0.12)
            g = VGroup(pl, nm, cap)
            g.frame = pl[0]
            return g
        if key == "vm":
            fr = _panel(5.65, 3.55, CLOUD, 0.05).move_to(p(3.425, -0.625))
            t = label("Compute Instance (VM)", 20, CLOUD).move_to(p(0.78, 0.9), aligned_edge=LEFT)
            g = VGroup(fr, t)
            g.frame, g.title = fr, t
            return g
        if key == "disk":
            text = kw.get("text", "/mnt/disk-1" if not self.manual else "50 GB disk")
            cyl = disk_cyl(0.6).move_to(p(3.85, -2.78))
            cable = Line(p(3.85, -2.4), cyl.get_top(), color=CLOUD, stroke_width=4)
            t = (mono if text.startswith("/") else label)(text, 20, INK).next_to(cyl, RIGHT, buff=0.2)
            g = VGroup(cable, cyl, t)
            g.frame, g.text = cyl, t
            return g
        if key in ("front", "api", "vdb", "nginx"):
            name = {"front": "frontend", "api": "api-service", "vdb": "vector-db", "nginx": "nginx"}[key]
            port = None if key == "nginx" else PORTS[key]
            b = svc_box(name, port, box_w=1.8 if key == "nginx" else 1.9,
                        box_h=0.6 if key == "nginx" else 0.72).move_to(self.slot[key])
            return b
        if key == "loader":
            return svc_box("loader", None, 1.9, 0.6, dashed=True).move_to(self.slot["loader"])
        if key == "door80":
            d = door(kw.get("text", "HTTP 80"), mono_font=False)
            on = kw.get("on", "vm")
            y = 1.15 if on == "vm" else 0.84
            return d.move_to(p(4.65, y))
        if key == "browser":
            return mini_browser(kw.get("url", "http://<VM IP>/")).move_to(p(4.65, 1.95))
        if key == "push":
            if self.manual:
                return arrow(p(-3.9, 0.35), p(-2.2, -0.2), LAPTOP, stroke=4, buff=0)
            return arrow(p(-4.0, 0.35), p(-2.45, -1.95), LAPTOP, stroke=4, buff=0, arc=0.5)
        if key == "pull":
            a = p(-0.35, -1.3) if self.manual else p(0.25, -1.95)
            return arrow(a, p(0.6, -1.1), LAPTOP, stroke=4, buff=0)
        if key == "hollow":
            a = Arrow(p(-3.35, 0.9), p(0.6, 0.0), buff=0, stroke_width=10, color=LAPTOP,
                      max_tip_length_to_length_ratio=0.15)
            inner = Arrow(p(-3.35, 0.9), p(0.6, 0.0), buff=0, stroke_width=4, color=S.BG,
                          max_tip_length_to_length_ratio=0.0)
            return VGroup(a, inner)
        if key == "routes":
            return self._routes()
        raise KeyError(key)

    def _routes(self) -> VGroup:
        g = VGroup()
        P = self.parts
        if "browser" in P:
            target = P.get("door80") or P.get("nginx")
            if target is not None:
                g.add(route(P["browser"].get_bottom(), target.get_top() + UP * 0.02))
        if "door80" in P and "nginx" in P and P["door80"].get_bottom()[1] > P["nginx"].get_top()[1] + 0.25:
            g.add(route(P["door80"].get_bottom(), P["nginx"].frame.get_top()))
        if "nginx" in P:
            nb = P["nginx"].frame
            if "front" in P:
                g.add(route(nb.get_bottom() + LEFT * 0.5, P["front"].frame.get_top() + RIGHT * 0.3))
            if "api" in P:
                g.add(route(nb.get_bottom() + RIGHT * 0.5, P["api"].frame.get_top() + LEFT * 0.3))
        if "api" in P and "vdb" in P:
            g.add(route(P["api"].frame.get_bottom(), P["vdb"].frame.get_top()))
        for a in g:
            a.set_stroke(width=4)
        return g

    # ---- generic show
    def part(self, scene, key: str, anim=None, run_time: float = 0.6, **kw):
        """PLAYS: show part `key` (no-op if shown). anim: a function mob -> animation."""
        if key in self.parts:
            return self.parts[key]
        m = self._make(key, **kw)
        self.parts[key] = m
        a = anim(m) if anim else (GrowArrow(m) if isinstance(m, Arrow) else FadeIn(m))
        self.show(scene, m, anims=[a], run_time=run_time)
        return m

    def build(self, scene, *keys, per: float = 0.5):
        for k in keys:
            self.part(scene, k, run_time=per)

    def laptop(self, scene, title: str = "Your Machine"):
        return self.part(scene, "laptop", title=title)

    def gcp(self, scene):
        return self.part(scene, "gcp", anim=lambda m: Create(m[0]), run_time=0.8) if "gcp" not in self.parts \
            else self.parts["gcp"]

    def registry(self, scene):
        return self.part(scene, "registry", anim=lambda m: FadeIn(m, shift=UP * 0.2))

    def gcr_note(self, scene):
        return self.part(scene, "gcr")

    def models(self, scene):
        return self.part(scene, "models")

    def state(self, scene):
        return self.part(scene, "state", anim=lambda m: FadeIn(m, shift=DOWN * 0.2))

    def vm(self, scene):
        return self.part(scene, "vm", anim=lambda m: FadeIn(m, scale=0.95), run_time=0.7)

    def disk(self, scene, text: str | None = None):
        return self.part(scene, "disk", **({"text": text} if text else {}))

    def box(self, scene, key: str):
        return self.part(scene, key, anim=lambda m: GrowFromCenter(m))

    def push(self, scene):
        return self.part(scene, "push", anim=lambda m: Create(m), run_time=0.8)

    def pull(self, scene):
        return self.part(scene, "pull", anim=lambda m: GrowArrow(m), run_time=0.6)

    def hollow(self, scene):
        return self.part(scene, "hollow", anim=lambda m: FadeIn(m, shift=RIGHT * 0.3), run_time=0.8)

    def browser(self, scene, url: str = "http://<VM IP>/"):
        return self.part(scene, "browser", anim=lambda m: FadeIn(m, shift=DOWN * 0.3), url=url)

    def door(self, scene, on: str = "vm", text: str = "HTTP 80", run_time: float = 0.6):
        """PLAYS: the PINK door. on='nginx': it lands on nginx's top edge (moving there if it already
        sits on the VM's edge, or dropping in from above)."""
        y = 1.15 if on == "vm" else 0.84
        if "door80" in self.parts:
            d = self.parts["door80"]
            scene.play(d.animate.move_to(self.p(4.65, y)), run_time=run_time)
            self.heal(scene)
            return d
        d = self._make("door80", on=on, text=text)
        self.parts["door80"] = d
        start = d.copy().shift(UP * 0.8).set_opacity(0)
        self.show(scene, d, anims=[ReplacementTransform(start, d)], run_time=run_time)
        return d

    def routes(self, scene, run_time: float = 1.0):
        """PLAYS: the PINK request arrows between the parts that exist (old ones replaced)."""
        if "routes" in self.parts:
            self.drop(scene, self.parts.pop("routes"), run_time=0.2)
        g = self._routes()
        self.parts["routes"] = g
        self.show(scene, g, anims=[LaggedStart(*[GrowArrow(a) for a in g], lag_ratio=0.4)], run_time=run_time)
        return g

    def loader(self, scene, pour: bool = True, leave: bool = True, n: int = 8):
        """PLAYS: the dashed TEAL loader appears in its slot, pours a stream of TEAL dots into the
        vector DB (they stay inside it as .data) and leaves (--rm)."""
        ld = self._make("loader")
        self.parts["loader"] = ld
        self.show(scene, ld, anims=[FadeIn(ld, shift=UP * 0.2)], run_time=0.5)
        if pour and "vdb" in self.parts:
            vb = self.parts["vdb"].frame
            dots = VGroup(*[Dot(radius=0.04, color=CONTAINER) for _ in range(n)])
            for d in dots:
                d.move_to(ld.get_right())
            targets = [vb.get_center() + np.array([0.66 + 0.09 * (i % 3), -0.2 + 0.11 * (i // 3), 0])
                       for i in range(n)]
            scene.add(dots)
            scene.play(LaggedStart(*[d.animate.move_to(t) for d, t in zip(dots, targets)], lag_ratio=0.12),
                       run_time=1.2)
            scene.remove(dots)
            self.add(dots)
            self.parts["data"] = dots
            self.heal(scene)
        if leave:
            self.drop(scene, self.parts.pop("loader"), run_time=0.4)

    def front_port_fix(self, scene, run_time: float = 0.8):
        """PLAYS: slide 23's 'HTTP 80' as a GREY ghost on the frontend box, flipping to its real port
        3000 (the box's port row flashes PINK); the ghost is dropped."""
        fb = self.parts["front"]
        ghost = label("HTTP 80", 20, S.GREY).next_to(fb.frame, LEFT, buff=0.1)
        if ghost.get_left()[0] < self.p(0.65, 0)[0]:
            ghost.next_to(fb.frame, DOWN, buff=0.08)
        self.show(scene, ghost, run_time=0.4)
        tgt = fb.port.copy()
        scene.play(ReplacementTransform(ghost, tgt), Indicate(fb.port, color=ROUTE), run_time=run_time)
        scene.remove(tgt, ghost)
        self._detach(ghost)
        self.heal(scene)

    def stage_chips(self, scene, run_time: float = 0.6):
        """PLAYS (manual): slide 8's four stage chips along y -3.35."""
        if self.stage_row is None:
            row = VGroup(*[chip(s, S.GREY, size=20) for s in STAGES_MANUAL]).arrange(RIGHT, buff=0.25)
            row.move_to(self.p(0, -3.35))
            self.stage_row = row
            self.show(scene, row, anims=[LaggedStart(*[FadeIn(c) for c in row], lag_ratio=0.2)],
                      run_time=run_time)
        return self.stage_row

    def light_stage(self, k: int):
        """ANIM: stage chip k (1-4) YELLOW, the earlier ones GREEN, later GREY."""
        return AnimationGroup(*[c.box.animate.set_stroke(TURN if i + 1 == k else (OWN if i + 1 < k else S.GREY))
                                for i, c in enumerate(self.stage_row)])

    def light(self, key: str, color=TURN):
        """ANIM: part `key`'s outline turns `color`."""
        m = self.parts[key]
        fr = getattr(m, "frame", m)
        return fr.animate.set_stroke(color)

    def normal(self, key: str):
        col = {"laptop": LAPTOP, "state": CLOUD, "gcp": CLOUD, "registry": CLOUD, "vm": CLOUD, "disk": CLOUD,
               "models": PAST}.get(key, CONTAINER)
        return self.light(key, col)

    # ---- the deck's build order
    def stage21(self, scene):
        """Slide 21: laptop, GCP, the registry, the developers' push arrow."""
        self.laptop(scene)
        self.gcp(scene)
        self.registry(scene)
        self.push(scene)

    def stage22(self, scene):
        """Slide 22: the empty VM and its disk."""
        self.vm(scene)
        self.disk(scene)

    def stage23(self, scene, fix: bool = True, loader: bool = True):
        """Slide 23: frontend 3000, api-service 9000, vector-db 8000 (+ the port fix, the loader)."""
        for k in ("front", "api", "vdb"):
            self.box(scene, k)
        if fix:
            self.front_port_fix(scene)
        if loader:
            self.loader(scene)

    def stage24(self, scene):
        """Slide 24: nginx on top, the HTTP 80 door lands on it, request arrows."""
        self.box(scene, "nginx")
        self.door(scene, on="nginx")
        self.routes(scene)

    def stage27(self, scene, url: str = f"http://{IP_PH}/"):
        """Slide 27: the browser on top, the routes redrawn from it."""
        self.browser(scene, url)
        self.routes(scene)

    def teaser(self, scene, url: str = "http://<VM IP>/"):
        """S01: slide 7 in ten seconds: 'Local Computer', GCP, the VM, the hollow arrow, four boxes,
        the door on the VM's top edge, the browser and its arrow."""
        self.laptop(scene, "Local Computer")
        self.gcp(scene)
        self.vm(scene)
        self.hollow(scene)
        for k in ("nginx", "api", "front", "vdb"):
            self.box(scene, k)
        self.door(scene, on="vm")
        self.browser(scene, url)
        self.routes(scene)


# ------------------------------------------------------------------ V2 · NamePhoneBook
class NamePhoneBook(_Anchored):
    """V2 · the VM from the inside: containers find each other by name (S04-S07). Built around ORIGIN;
    extents x -6.5 .. 5.95, y -2.75 .. 2.5 with everything shown (VM alone: x -3.75 .. 5.75,
    y -1.7 .. 1.7, title above it at y 2.3). Over a 3-row strip: md.shift(UP * 0.55) and keep the
    fence/tags/outsider off (then y -1.15 .. 2.55).
        VM outline  BLUE x -3.75 .. 5.75, y -1.7 .. 1.7; title 'cheese-app-vm' (mono) above, left
        slots       box centres x -2.85 (vdb) · -1.33 (api; the loader borrows it first) · 0.19 (front) ·
                    1.71 (nginx), y 0.15; boxes 1.46 x 1.0 (label-font names, two rows for the vector
                    DB; .data dots along its bottom)
        doors       PINK '-p' plates on the VM's top wall (y 1.7) above each box: 8000 9000 3000 80
        cable       GREEN y -1.2, x -3.5 .. 2.45, 'cheese-app-network' under it (left)
        phone book  x 2.75 .. 5.55, y -1.25 .. 1.35: 'names on' / 'this network', up to 5 entries
        fence       dotted PINK x -4.35 .. 5.95, y -2.0 .. 2.0; gates on its LEFT edge: 80 (y 0.9),
                    443 (0.15), 22 (-0.6, GREY), the closed spot for any other port (-1.45)
        tags        PINK chips 'http-server' 'https-server' under the fence (y -2.35), tied to their gates
                    by thin dashed lines that run outside the fence's left edge
        outsider    GREY laptop (or a browser glyph) at (-5.95, -0.3), outside the fence
    Keys: 'vdb' 'loader' 'api' 'front' 'nginx'.
    PLAYS cable_on() (cable + label + empty book) · plug(key) (box drops in, plug line, door opens,
        name written in the book) · loader() then pour(n) (knocks on 'cheese-app-vector-db:8000' by
        name, dots flow into the vector DB: .data) then unload() (--rm: box leaves, its book line is
        struck GREY) · stop(key) (box GREY, book line erased) · start(key) · routes() nginx → front /
        api arcs · nginx_fail(at=None) (lookup arrow to the book comes back empty, RED stamp '[emerg]
        host not found in upstream "frontend"' under the piece, nginx RED, its door barred, routes fade)
        · nginx_ok() · fence(labels=True) · gate_labels() · tags() · outsider(kind='laptop'|'browser') ·
        knock(port, ok=None) (arrow from the outsider: an open gate → GREEN gate + arrow on to the
        nginx box; a closed one → bounces off, RED) · question(key) YELLOW '?' over a box (.qmark) ·
        unquestion().
    ANIM light_entry(key, colour) · light(key, colour) · normal(key).
    .boxes{key} .doors{key} .entries{key} .gates{port} .book .cable .vm .fence_line .data"""

    SLOT_X = {"vdb": -2.85, "loader": -1.33, "api": -1.33, "front": 0.19, "nginx": 1.71}
    NAMES = {"vdb": ("cheese-app-", "vector-db"), "loader": ("vector-db-", "cli"),
             "api": ("api-service",), "front": ("frontend",), "nginx": ("nginx",)}
    BOOK = {"vdb": C_VDB, "loader": C_LOADER, "api": C_API, "front": C_FRONT, "nginx": C_NGINX}
    GATE_Y = {"80": 0.9, "443": 0.15, "22": -0.6}
    CLOSED_Y = -1.45

    def __init__(self, title: str = T_VM, built: bool = False, **kw):
        super().__init__(**kw)
        p = self.p
        self.vm = _panel(9.5, 3.4, CLOUD, 0.04).move_to(p(1.0, 0))
        self.title = mono(title, 20, CLOUD).move_to(p(-4.35, 2.3), aligned_edge=LEFT)
        self.add(self.vm, self.title)
        self.boxes, self.doors, self.entries, self.plugs, self.gates = {}, {}, {}, {}, {}
        self.routes_g = None
        self.fence_line = None
        self.tag_chips = None
        self.outside = None
        self.data = VGroup()
        self.qmark = None
        self.cable = VGroup(Line(p(-3.5, -1.2), p(2.45, -1.2), color=OWN, stroke_width=6),
                            mono(NETWORK, 20, OWN).move_to(p(-3.5, -1.48), aligned_edge=LEFT))
        bk = _panel(2.8, 2.6, OWN, 0.05, 2.5).move_to(p(4.15, 0.05))
        hd = VGroup(label("names on", 20, S.GREY), label("this network", 20, S.GREY)).arrange(DOWN, buff=0.04)
        hd.move_to(bk.get_top() + DOWN * 0.38)
        rule = Line(bk.get_left() + RIGHT * 0.15, bk.get_right() + LEFT * 0.15, color=S.GREY_DARK,
                    stroke_width=2).move_to(p(4.15, 0.62))
        self.book = VGroup(bk, hd, rule)
        self._rows = []
        if built:
            self.add(self.cable, self.book)

    # ---- helpers
    def _row_y(self, i: int) -> float:
        return 0.38 - 0.32 * i

    def _box(self, key: str, color=CONTAINER):
        rows = self.NAMES[key]
        fr = RoundedRectangle(width=1.46, height=1.0, corner_radius=0.1, stroke_color=color,
                              stroke_width=3).set_fill(tint(color, 0.18), 1)
        if key == "loader":
            d = DashedVMobject(fr.copy().set_fill(opacity=0), num_dashes=20).set_stroke(color, 3)
            fr.set_stroke(opacity=0)
            fr = VGroup(fr, d)
        nm = VGroup(*[label(r, 20, INK) for r in rows]).arrange(DOWN, buff=0.04)
        if nm.width > 1.38:
            raise ValueError(f"NamePhoneBook: {rows} too wide")
        g = VGroup(fr, nm.move_to(fr).shift(UP * 0.1)).move_to(self.p(self.SLOT_X[key], 0.15))
        g.frame, g.name = fr, nm
        return g

    # ---- PLAYS
    def cable_on(self, scene, run_time: float = 0.8):
        if self.cable not in self.submobjects:
            self.show(scene, self.cable, self.book, anims=[Create(self.cable[0]), FadeIn(self.cable[1]),
                                                           FadeIn(self.book)], run_time=run_time)
        return self.cable

    def plug(self, scene, key: str, door_on: bool = True, run_time: float = 0.7):
        """PLAYS: box `key` drops into its slot, plugs into the cable, its door opens on the wall
        (not for the loader), and its name is written in the phone book."""
        self.cable_on(scene)
        b = self._box(key)
        x = self.SLOT_X[key]
        pl = Line(self.p(x, -0.35), self.p(x, -1.2), color=OWN, stroke_width=4)
        new = [b, pl]
        anims = [FadeIn(b, shift=DOWN * 0.4), Create(pl)]
        if door_on and key != "loader":
            d = door(PORTS[key]).move_to(self.p(x, 1.7))
            self.doors[key] = d
            new.append(d)
            anims.append(GrowFromCenter(d))
        i = len(self._rows)
        if key in self._rows:
            raise ValueError(f"NamePhoneBook.plug({key!r}): already plugged")
        if i > 4:
            raise ValueError("NamePhoneBook: the book holds five names")
        e = label(self.BOOK[key], 20, INK).move_to(self.p(2.95, self._row_y(i)), aligned_edge=LEFT)
        self._rows.append(key)
        self.entries[key] = e
        new.append(e)
        anims.append(FadeIn(e, shift=RIGHT * 0.1))
        self.boxes[key], self.plugs[key] = b, pl
        self.show(scene, *new, anims=anims, run_time=run_time)
        return b

    def loader(self, scene):
        """PLAYS: the dashed loader (vector-db-cli) plugs into the api slot, with its book line."""
        return self.plug(scene, "loader", door_on=False)

    def pour(self, scene, n: int = 12, run_time: float = 1.6):
        """PLAYS: the loader knocks on 'cheese-app-vector-db:8000' (PINK arc + label, the book entry
        flashes), then a stream of TEAL dots (n <= 12) flows into a row along the bottom of the
        vector-DB box (kept as .data)."""
        lb, vb = self.boxes["loader"], self.boxes["vdb"]
        knock = route(lb.frame.get_top() + LEFT * 0.2, vb.frame.get_top() + RIGHT * 0.2, arc=0.9)
        kt = label(f"{C_VDB}:8000", 20, ROUTE).move_to(self.p(-2.05, 1.12))
        self.show(scene, knock, kt, anims=[Create(knock), FadeIn(kt)], run_time=0.6,
                  extra=[Indicate(self.entries["vdb"], color=ROUTE)])
        dots = VGroup(*[Dot(radius=0.05, color=CONTAINER) for _ in range(n)])
        for d in dots:
            d.move_to(lb.frame.get_left())
        c = vb.frame.get_center()
        n = min(n, 12)
        tg = [c + np.array([-0.55 + 0.1 * i, -0.36, 0]) for i in range(n)]
        scene.add(dots)
        scene.play(LaggedStart(*[d.animate.move_to(t) for d, t in zip(dots, tg)], lag_ratio=0.1),
                   run_time=run_time)
        scene.remove(dots)
        self.data.add(*dots)
        if self.data not in self.submobjects:
            self.add(self.data)
        self.heal(scene)
        self.drop(scene, knock, kt, run_time=0.3)
        return self.data

    def unload(self, scene, run_time: float = 0.6):
        """PLAYS: the loader leaves (--rm): its box and plug fade, its book line is struck GREY."""
        e = self.entries["loader"]
        st = Line(e.get_left() + LEFT * 0.05, e.get_right() + RIGHT * 0.05, color=S.GREY, stroke_width=3)
        self.drop(scene, self.boxes.pop("loader"), self.plugs.pop("loader"), run_time=run_time,
                  extra=[e.animate.set_color(S.GREY)])
        self.show(scene, st, anims=[Create(st)], run_time=0.3)
        e.strike = st
        return st

    def clear_loader_line(self, scene):
        """PLAYS: the struck loader line leaves the book (before the api plugs into that row's slot)."""
        e = self.entries.pop("loader")
        self._rows.remove("loader")
        self.drop(scene, e, getattr(e, "strike", None), run_time=0.3)

    def stop(self, scene, key: str, run_time: float = 0.6):
        """PLAYS: container `key` stops: its box GREY, its door dims, its book line is erased."""
        b, e = self.boxes[key], self.entries.get(key)
        anims = [b.frame.animate.set_stroke(S.GREY).set_fill(tint(S.GREY, 0.1), 1)]
        if key in self.doors:
            anims.append(self.doors[key].animate.set_opacity(0.35))
        if e is not None:
            self._detach(e)
            anims.append(FadeOut(e, shift=RIGHT * 0.2))
        scene.play(*anims, run_time=run_time)
        if e is not None:
            scene.remove(e)
            self.entries[key + "_gone"] = e
        self.heal(scene)

    def start(self, scene, key: str, run_time: float = 0.6):
        """PLAYS: the box turns TEAL again, its door brightens, its book line is written again."""
        b = self.boxes[key]
        anims = [b.frame.animate.set_stroke(CONTAINER).set_fill(tint(CONTAINER, 0.18), 1)]
        if key in self.doors:
            anims.append(self.doors[key].animate.set_opacity(1))
        e = self.entries.pop(key + "_gone", None)
        if e is not None:
            e.set_opacity(1)
            self.entries[key] = e
            self.show(scene, e, anims=[FadeIn(e)] + anims, run_time=run_time)
        else:
            scene.play(*anims, run_time=run_time)
            self.heal(scene)

    def routes(self, scene, run_time: float = 0.8):
        """PLAYS: PINK arcs nginx → frontend and nginx → api-service (over the boxes)."""
        n = self.boxes["nginx"].frame
        g = VGroup()
        for k, arc in (("front", 0.9), ("api", 0.75)):
            if k in self.boxes:
                g.add(route(n.get_top() + LEFT * 0.3, self.boxes[k].frame.get_top() + RIGHT * 0.25, arc=arc))
        self.routes_g = g
        self.show(scene, g, anims=[Create(a) for a in g], run_time=run_time)
        return g

    def nginx_fail(self, scene, at=None, run_time: float = 0.8):
        """PLAYS the hook's answer: a lookup arrow nginx → book comes back with a RED '?', the RED
        stamp (label font) appears under the piece (or at `at`), nginx turns RED, its door gets a RED
        bar, the routes fade. Returns the stamp."""
        nb = self.boxes["nginx"].frame
        look = route(nb.get_right(), self.book[0].get_left() + UP * 0.1, color=ROUTE)
        self.show(scene, look, anims=[GrowArrow(look)], run_time=0.5)
        q = label("?", 26, ERR).next_to(look, UP, buff=0.05)
        self.show(scene, q, run_time=0.3)
        stamp = mono('[emerg] host not found in upstream "frontend"', 20, ERR)
        stamp.move_to(self.p(0.85, -2.35) if at is None else at)
        anims = [nb.animate.set_stroke(ERR).set_fill(tint(ERR, 0.2), 1)]
        bar = None
        if "nginx" in self.doors:
            d = self.doors["nginx"]
            bar = Line(d.get_left() + LEFT * 0.05, d.get_right() + RIGHT * 0.05, color=ERR, stroke_width=7)
        new = [stamp] + ([bar] if bar is not None else [])
        self.show(scene, *new, anims=[FadeIn(stamp, shift=UP * 0.1)] + ([Create(bar)] if bar else []),
                  extra=anims, run_time=run_time)
        self._fail = [look, q, stamp] + ([bar] if bar else [])
        if self.routes_g is not None:
            self.drop(scene, self.routes_g, run_time=0.4)
            self.routes_g = None
        return stamp

    def nginx_ok(self, scene, run_time: float = 0.6):
        """PLAYS: the failure marks leave, nginx is TEAL again (call routes() to redraw the arrows)."""
        self.drop(scene, *getattr(self, "_fail", []), run_time=0.3)
        self._fail = []
        scene.play(self.boxes["nginx"].frame.animate.set_stroke(CONTAINER).set_fill(tint(CONTAINER, 0.18), 1),
                   run_time=run_time)
        self.heal(scene)

    def fence(self, scene, labels: bool = True, run_time: float = 0.9):
        """PLAYS: the dotted PINK firewall fence around the VM with three gate plates on its left
        edge (80, 443, PINK; 22 GREY). labels=False draws empty plates (S07's '?' beat)."""
        fl = _dotted_rect(10.3, 4.0, ROUTE, 0.4, 2.5).move_to(self.p(0.8, 0))
        self.fence_line = fl
        gs = []
        for port, y in self.GATE_Y.items():
            col = S.GREY if port == "22" else ROUTE
            g = door(port if labels else " ", col, door_w=0.8).move_to(self.p(-4.35, y))
            g.port = port
            self.gates[port] = g
            gs.append(g)
        spot = Line(self.p(-4.35, self.CLOSED_Y + 0.2), self.p(-4.35, self.CLOSED_Y - 0.2), color=ROUTE,
                    stroke_width=7)
        self.gates["closed"] = spot
        self.show(scene, fl, *gs, spot, anims=[Create(fl)] + [FadeIn(g) for g in gs] + [FadeIn(spot)],
                  run_time=run_time)
        return fl

    def gate_labels(self, scene, run_time: float = 0.6):
        """PLAYS: the empty gate plates get their port numbers."""
        news = []
        for port in self.GATE_Y:
            g = self.gates[port]
            col = S.GREY if port == "22" else ROUTE
            new = door(port, col, door_w=0.8).move_to(g)
            new.port = port
            news.append((g, new))
        for g, new in news:
            self.swap(scene, g, new, run_time=run_time / 3)
            self.gates[new.port] = new

    def tags(self, scene, run_time: float = 0.8):
        """PLAYS: the network tags 'http-server' / 'https-server' (PINK chips under the fence), each
        tied to its gate (80 / 443) by a thin dashed line outside the fence."""
        t1 = route_chip("http-server").move_to(self.p(-2.8, -2.4))
        t2 = route_chip("https-server").next_to(t1, RIGHT, buff=0.25)
        g80, g443 = self.gates.get("80"), self.gates.get("443")
        ties = VGroup()
        if g80 is not None:
            pts = [t1.get_left(), self.p(-4.95, t1.get_left()[1] - self.p(0, 0)[1]),
                   self.p(-4.95, 0.9), g80.get_left()]
            ties.add(VMobject().set_points_as_corners(pts))
        if g443 is not None:
            yb = t2.get_bottom()[1] - self.p(0, 0)[1] - 0.12
            pts = [t2.get_bottom(), self.p(t2.get_center()[0] - self.p(0, 0)[0], yb), self.p(-5.1, yb),
                   self.p(-5.1, 0.15), g443.get_left()]
            ties.add(VMobject().set_points_as_corners(pts))
        ties = VGroup(*[DashedVMobject(t, num_dashes=40).set_stroke(ROUTE, 2) for t in ties])
        self.tag_chips = VGroup(t1, t2)
        self.ties = ties
        self.show(scene, self.tag_chips, ties, anims=[FadeIn(self.tag_chips, shift=UP * 0.2), Create(ties)],
                  run_time=run_time)
        return self.tag_chips

    def outsider(self, scene, kind: str = "laptop", run_time: float = 0.5):
        """PLAYS: a GREY laptop ('laptop') or a small browser glyph outside the fence (-5.95, -0.3)."""
        if kind == "laptop":
            from explainer.devops import laptop as _laptop
            gl = _laptop(1.0, LAPTOP)
            t = label("laptop", 20, LAPTOP).next_to(gl, DOWN, buff=0.1)
            g = VGroup(gl, t).move_to(self.p(-5.95, -0.3))
        else:
            g = browser_icon(1.0, LAPTOP, "browser").move_to(self.p(-5.95, -0.3))
        self.outside = g
        self.show(scene, g, run_time=run_time)
        return g

    def knock(self, scene, port: str, ok: bool | None = None, text: str | None = None, run_time: float = 0.7):
        """PLAYS: a PINK arrow from the outsider to the gate of `port` (or the closed spot), labelled
        text (default ':<port>', written above the outsider). An open gate (80/443/22 by default; ok
        overrides) glows GREEN and the
        arrow continues to the nginx box (port 80); a closed one: the arrow turns RED and bounces back.
        Returns the arrows and label as one group: piece.drop(self, it) before the next knock."""
        gate = self.gates.get(port, self.gates.get("closed"))
        ok = (port in self.GATE_Y) if ok is None else ok
        start = self.outside.get_right() + RIGHT * 0.05
        a = route(start, gate.get_left() + LEFT * 0.05)
        t = mono(text or f":{port}", 20, ROUTE).next_to(self.outside, UP, buff=0.12)
        self.show(scene, a, t, anims=[GrowArrow(a), FadeIn(t)], run_time=run_time)
        out_ = [a, t]
        if ok:
            scene.play(gate.plate.animate.set_stroke(OWN) if hasattr(gate, "plate") else gate.animate.set_color(OWN),
                       run_time=0.3)
            if port == "80" and "nginx" in self.boxes:
                b = route(gate.get_right(), self.boxes["nginx"].frame.get_top(), arc=-0.3)
                self.show(scene, b, anims=[Create(b)], run_time=0.6)
                out_.append(b)
        else:
            scene.play(a.animate.set_color(ERR), t.animate.set_color(ERR), run_time=0.25)
            scene.play(a.animate.shift(LEFT * 0.25), run_time=0.2)
            scene.play(a.animate.shift(RIGHT * 0.12), run_time=0.15)
        self.heal(scene)
        return VGroup(*out_)

    def question(self, scene, key: str = "vdb"):
        """PLAYS: a YELLOW '?' over box `key` (its inside not drawn)."""
        q = label("?", 36, TURN).move_to(self.boxes[key].frame)
        self.qmark = q
        self.show(scene, q, anims=[FadeIn(q, scale=1.3)], run_time=0.4)
        return q

    def unquestion(self, scene):
        if self.qmark is not None:
            self.drop(scene, self.qmark, shift=UP * 0.3)
            self.qmark = None

    # ---- ANIM
    def light_entry(self, key: str, color=TURN):
        return Indicate(self.entries[key], color=color, scale_factor=1.08)

    def light(self, key: str, color=TURN):
        return self.boxes[key].frame.animate.set_stroke(color)

    def normal(self, key: str):
        return self.light(key, CONTAINER)


# ------------------------------------------------------------------ V3 · ProxyRoute
class ProxyRoute(_Anchored):
    """V3 · one public door and the prefix scissors (nginx.conf:35-55; S07, S15). Built around ORIGIN,
    x -3.2 .. 3.0, y -2.35 .. 2.0 (gates=True adds a gate column at x -3.85: then x -4.3 .. 3.0):
        tile lane   y 1.7 (a URL tile starts at the left)
        nginx       TEAL box (0, 0.75)
        signposts   y -0.2: '^~ /api-service/' (x -1.55) and '/' (x 1.6), GREY plates, mono
        work lane   y -1.0 (where the scissors cut)
        targets     y -1.95: 'api-service:9000' (x -1.55) and 'frontend:3000' (x 1.6)
    PLAYS enter(path='/api-service/status') the PINK tile (mono) slides in and stops over nginx
        (through gate 80 when gates=True) · match('api'|'front') its signpost lights YELLOW and the
        tile moves under it · snip() PINK scissors cut '/api-service' off (the cut part falls away GREY)
        and the rest re-centres ('/status') · arrive() the tile walks into its target, which flashes ·
        reply(text='{"message":"Welcome to AC215"}') the tile gives way to a GREEN reply on the work
        lane, which rides back up to the tile lane ·
        reset() clears tile and reply · run(path, branch, reply=None) all of the above.
    ANIM light_sign(branch, colour) · light_target(branch, colour).
    .nginx .signs{branch} .targets{branch} .gates{port} .tile (current) .last_slash (unused hook)"""

    def __init__(self, gates: bool = False, **kw):
        super().__init__(**kw)
        p = self.p
        self.nginx = svc_box("nginx", None, 2.2, 0.62).move_to(p(0, 0.75))
        s_api = self._sign("^~ /api-service/").move_to(p(-1.55, -0.2))
        s_front = self._sign("/").move_to(p(1.6, -0.2))
        self.signs = {"api": s_api, "front": s_front}
        t_api = svc_box("api-service:9000", None, 2.95, 0.6).move_to(p(-1.55, -1.95))
        t_front = svc_box("frontend:3000", None, 2.45, 0.6).move_to(p(1.6, -1.95))
        self.targets = {"api": t_api, "front": t_front}
        legs = VGroup(*[Line(self.nginx.frame.get_bottom(), s.get_top(), color=S.GREY_DARK, stroke_width=2)
                        for s in (s_api, s_front)],
                      *[Line(s.get_bottom(), t.frame.get_top(), color=S.GREY_DARK, stroke_width=2)
                        for s, t in ((s_api, t_api), (s_front, t_front))])
        self.legs = legs
        self.add(legs, self.nginx, s_api, s_front, t_api, t_front)
        self.gates = {}
        if gates:
            for port, y, open_ in (("80", 1.7, True), ("3000", 0.75, False), ("9000", -0.2, False)):
                d = door(port, ROUTE if open_ else S.GREY, door_w=1.0).move_to(p(-3.85, y))
                if not open_:
                    d.add(Line(d.get_left(), d.get_right(), color=ERR, stroke_width=6))
                self.gates[port] = d
                self.add(d)
        self.tile = None
        self.reply_m = None

    def _sign(self, text: str) -> VGroup:
        t = mono(text, 20, INK)
        pl = RoundedRectangle(width=t.width + 0.35, height=0.44, corner_radius=0.06, stroke_color=S.GREY,
                              stroke_width=2.5).set_fill(PANEL, 1)
        g = VGroup(pl, t.move_to(pl))
        g.plate, g.text = pl, t
        return g

    def _tile(self, parts) -> VGroup:
        full = mono("".join(parts), 20, INK)
        ts, k = VGroup(), 0
        for s_ in parts:
            ts.add(VGroup(*full[k:k + len(s_)]))
            k += len(s_)
        bg = RoundedRectangle(width=ts.width + 0.3, height=0.44, corner_radius=0.08, stroke_color=ROUTE,
                              stroke_width=3).set_fill(tint(ROUTE, 0.25), 1)
        ts.move_to(bg)
        g = VGroup(bg, ts)
        g.bg, g.parts, g.strs = bg, ts, list(parts)
        return g

    def enter(self, scene, path: str = "/api-service/status", run_time: float = 0.9):
        """PLAYS: the URL tile slides in along the top lane (through gate 80 when there are gates)
        and stops over nginx."""
        if self.tile is not None:
            self.reset(scene)
        parts = ["/api-service", path[len("/api-service"):]] if path.startswith("/api-service/") else [path]
        tl = self._tile(parts)
        start_x = (-3.35 + 0.1 if self.gates else -3.2) + tl.width / 2
        tl.move_to(self.p(start_x, 1.7))
        self.tile = tl
        self.show(scene, tl, anims=[FadeIn(tl, shift=RIGHT * (0.8 if self.gates else 0.3))], run_time=0.4)
        if self.gates:
            scene.play(self.gates["80"].plate.animate.set_stroke(OWN), run_time=0.3)
        scene.play(tl.animate.move_to(self.p(0, 1.45)), run_time=run_time)
        self.heal(scene)
        return tl

    def match(self, scene, branch: str = "api", run_time: float = 0.8):
        """PLAYS: signpost `branch` lights YELLOW and the tile moves down to the work lane under it."""
        s = self.signs[branch]
        scene.play(s.plate.animate.set_stroke(TURN), Indicate(s.text, color=TURN, scale_factor=1.05),
                   run_time=0.5)
        scene.play(self.tile.animate.move_to(self.p(s.get_center()[0] - self.p(0, 0)[0], -1.0)), run_time=run_time)
        self.heal(scene)
        self.branch = branch

    def snip(self, scene, run_time: float = 0.9):
        """PLAYS: the scissors cut '/api-service' off the tile; the rest re-centres as a new tile."""
        tl = self.tile
        if len(tl.parts) < 2:
            raise ValueError("snip(): this tile has no /api-service prefix")
        pre, rest = tl.parts[0], tl.parts[1]
        sc = scissors(0.5).move_to([pre.get_right()[0], tl.get_top()[1] + 0.3, 0])
        self.show(scene, sc, anims=[FadeIn(sc, shift=DOWN * 0.2)], run_time=0.3)
        scene.play(sc.animate.shift(DOWN * 0.35), run_time=0.3)
        new = self._tile([tl.strs[1]])
        new.move_to(rest.get_center())
        self._detach(tl)
        scene.add(tl)
        gone = VGroup(tl.bg, pre)
        scene.play(gone.animate.shift(DOWN * 0.35 + LEFT * 0.2).set_opacity(0).set_color(S.GREY),
                   ReplacementTransform(rest, new.parts[0]), FadeIn(new.bg),
                   FadeOut(sc), run_time=run_time)
        scene.remove(tl, gone, sc, new, *new.submobjects, rest)
        self._detach(sc)
        self.tile = new
        self.add(new)
        self.heal(scene)
        scene.play(new.animate.move_to(self.p(self.signs[self.branch].get_center()[0] - self.p(0, 0)[0], -1.0)),
                   run_time=0.3)
        return new

    def arrive(self, scene, run_time: float = 0.7):
        """PLAYS: the tile walks into its target box, which flashes PINK."""
        t = self.targets[self.branch]
        scene.play(self.tile.animate.move_to(t.frame.get_top() + UP * 0.32), run_time=run_time)
        scene.play(t.frame.animate(rate_func=there_and_back).set_stroke(ROUTE, 6), run_time=0.5)
        self.heal(scene)

    def reply(self, scene, text: str = '{"message":"Welcome to AC215"}', run_time: float = 1.0):
        """PLAYS: a GREEN reply (mono 20) rides from the target back up to the tile lane."""
        r = chip(text, OWN, size=20, font=MONO)
        r.move_to(self.p(0, -1.0))
        self.reply_m = r
        old = [self.tile] if self.tile is not None else []
        if old:
            self._detach(self.tile)
            self.tile = None
        self.show(scene, r, anims=[FadeIn(r, shift=UP * 0.3)] + [FadeOut(o) for o in old], run_time=0.4)
        scene.remove(*old)
        scene.play(r.animate.move_to(self.p(0, 1.7)), run_time=run_time)
        self.heal(scene)
        return r

    def reset(self, scene):
        """PLAYS: the tile and the reply leave; signs and targets back to GREY/TEAL."""
        gone = [m for m in (self.tile, self.reply_m) if m is not None]
        anims = [s.plate.animate.set_stroke(S.GREY) for s in self.signs.values()]
        if gone:
            self.drop(scene, *gone, extra=anims, run_time=0.3)
        self.tile = self.reply_m = None

    def run(self, scene, path: str = "/api-service/status", branch: str = "api", reply: str | None = None):
        self.enter(scene, path)
        self.match(scene, branch)
        if branch == "api" and path.startswith("/api-service/"):
            self.snip(scene)
        self.arrive(scene)
        if reply:
            self.reply(scene, reply)

    def light_sign(self, branch: str, color=TURN):
        return self.signs[branch].plate.animate.set_stroke(color)

    def light_target(self, branch: str, color=ROUTE):
        return self.targets[branch].frame.animate(rate_func=there_and_back).set_stroke(color, 6)


# ------------------------------------------------------------------ V4 · EngineLoop
GLYPH_COL = {"+": OWN, "~": TURN, "-": ERR, "+-": ERR}


class EngineLoop(_Anchored):
    """V4 · Pulumi's loop (slide 14): program → desired; state (+ --refresh: reality) → diff → plan →
    provider calls. Built around ORIGIN.
    Full (compact=False): x -6.2 .. 6.2, y -3.35 .. 2.6.
        machine   GREY box x -6.2 .. 6.2, y 1.6 .. 2.6: 'Your Machine', PURPLE 'pulumi CLI' chip, the
                  file card '__main__.py' (x -0.6 .. 1.9)
        trees     y -1.05 .. 1.25: 'desired' (GREEN, x -4.0) · 'state' (GREEN, x 0, a small BLUE
                  bucket beside its header) · 'reality' (BLUE, x 4.0); four cards each (cards=), 2.6 wide
        glyphs    + ~ - +- left of the desired cards (x -5.55)
        plan box  x -6.2 .. -2.4, y -2.35 .. -1.6 ('plan' + the glyph row)
        providers four PURPLE plugs y -1.95, x -1.6 .. 6.2 (gcp, docker-build, docker, command)
        banner    y -3.1: 'Pulumi manages infrastructure through cloud APIs' (+ footnote to its right)
    Compact (compact=True): only the three trees, x -3.05 .. 3.05 (cards 1.8 wide at x -2.05 / 0 /
        2.05), y -1.35 .. 1.0; glyphs at x -3.3; for S09's strip beat and S13/S16's small replays.
    PLAYS machine() · run() (the CLI pulses, desired cards drop in) · trees() (state + reality slide in)
        · refresh(stale=1) (PINK sweep reality → state; the stale state card updates) · diff(glyphs)
        (e.g. ('+', '~', '-', '+-'), one per card, None = no glyph; plan row fills) · apply() (PINK
        arrow plan → plugs, plugs light, BLUE arrow up into reality, reality cards flash) · banner() ·
        footnote(text='… and SSH, for the inside of the VM') · preview_stop() (GREY stop sign
        'nothing applied' on the plan) · in_sync() (all trees GREEN, 'no changes' in the plan) ·
        unknown(i=0) (YELLOW padlock 'unknown' on desired card i) · backwards() (RED '-' on every
        card, reality cards fade bottom-up) · clear_glyphs().
    .cards['desired'|'state'|'reality'][i] (.box .text) .glyphs .plan .plugs .banner_m .cli .file"""

    def __init__(self, cards=("Network", "Firewall", "Disk", "Instance"), compact: bool = False, **kw):
        super().__init__(**kw)
        self.compact = compact
        self.names = list(cards)
        p = self.p
        if compact:
            xs, cw, top = {"desired": -2.05, "state": 0.0, "reality": 2.05}, 1.8, 0.8
        else:
            xs, cw, top = {"desired": -4.0, "state": 0.0, "reality": 4.0}, 2.6, 1.05
        self.xs, self.cw = xs, cw
        cols = {"desired": OWN, "state": OWN, "reality": CLOUD}
        self.heads, self.cards = {}, {}
        for key in xs:
            h = label(key, 22, cols[key]).move_to(p(xs[key], top))
            self.heads[key] = h
            row = VGroup()
            for i, n in enumerate(cards):
                b = RoundedRectangle(width=cw, height=0.4, corner_radius=0.06, stroke_color=cols[key],
                                     stroke_width=2.5).set_fill(tint(cols[key], 0.15), 1)
                t = label(n, 20, INK)
                if t.width > cw - 0.2:
                    raise ValueError(f"EngineLoop: card {n!r} too wide")
                c = VGroup(b, t.move_to(b)).move_to(p(xs[key], top - 0.55 - 0.5 * i))
                c.box, c.text = b, t
                row.add(c)
            self.cards[key] = row
        self.glyphs = VGroup()
        self.add(self.glyphs)
        self.bucket = None
        self.plan = self.plugs = self.banner_m = self.cli = self.file = self.mbox = None
        self.extras = VGroup()

    # ---- PLAYS
    def machine(self, scene, run_time: float = 0.6):
        if self.compact:
            raise ValueError("EngineLoop(compact=True) has no machine box")
        p = self.p
        fr = _panel(12.4, 1.0, LAPTOP, 0.05).move_to(p(0, 2.1))
        t = label("Your Machine", 20, LAPTOP).move_to(p(-6.0, 2.1), aligned_edge=LEFT)
        cli = tool_chip("pulumi CLI").move_to(p(-2.6, 2.1))
        f = file_card("__main__.py", OWN).move_to(p(0.65, 2.1))
        self.mbox, self.cli, self.file = fr, cli, f
        self.show(scene, fr, t, cli, f, run_time=run_time)

    def run(self, scene, run_time: float = 1.2):
        """PLAYS: the program runs: desired header + cards drop in (from the file card if shown)."""
        d = self.cards["desired"]
        src = self.file if self.file is not None else self.heads["desired"]
        extra = [Indicate(self.cli, color=TOOL)] if self.cli is not None else []
        self.show(scene, self.heads["desired"], run_time=0.3, extra=extra)
        starts = [c.copy().move_to(src).set_opacity(0) for c in d]
        self.show(scene, *d, anims=[LaggedStart(*[ReplacementTransform(s, c) for s, c in zip(starts, d)],
                                                lag_ratio=0.25)], run_time=run_time)

    def trees(self, scene, stale: int | None = 1, run_time: float = 0.8):
        """PLAYS: the state tree (a GREEN scroll, from a small BLUE bucket) and reality (BLUE) slide
        in. stale=i: state card i shows a GREY '(old)' look until refresh()."""
        s, r = self.cards["state"], self.cards["reality"]
        if stale is not None:
            s[stale].box.set_stroke(S.GREY).set_fill(tint(S.GREY, 0.12), 1)
            s[stale].text.set_color(S.GREY)
        self.stale = stale
        self.bucket = pail(0.45, CLOUD, rim=OWN).next_to(self.heads["state"], RIGHT, buff=0.18)
        self.show(scene, self.heads["state"], self.bucket, *s, anims=[FadeIn(VGroup(self.heads["state"],
                                                                                   self.bucket, *s), shift=LEFT * 0.3)],
                  run_time=run_time)
        self.show(scene, self.heads["reality"], *r, anims=[FadeIn(VGroup(self.heads["reality"], *r),
                                                                  shift=LEFT * 0.3)], run_time=run_time)

    def refresh(self, scene, run_time: float = 1.0):
        """PLAYS: --refresh: a PINK sweep from reality to state; the stale card lines up."""
        s, r = self.cards["state"], self.cards["reality"]
        band = Rectangle(width=0.18, height=r.height + 0.3, stroke_width=0).set_fill(ROUTE, 0.5)
        band.move_to(r.get_center())
        scene.add(band)
        anims = []
        if getattr(self, "stale", None) is not None:
            c = s[self.stale]
            anims = [c.box.animate.set_stroke(OWN).set_fill(tint(OWN, 0.15), 1), c.text.animate.set_color(INK)]
        scene.play(band.animate.move_to(s.get_center()), run_time=run_time)
        scene.play(FadeOut(band), *anims, run_time=0.4)
        scene.remove(band)
        self.stale = None
        self.heal(scene)

    def diff(self, scene, glyphs=("+", "~", "-", "+-"), run_time: float = 1.0):
        """PLAYS: glyphs pop left of the desired cards (None skips a card); the plan row fills."""
        self.clear_glyphs(scene)
        d = self.cards["desired"]
        gx = (-3.3 if self.compact else -5.55)
        new = []
        for c, gch in zip(d, glyphs):
            if gch is None:
                continue
            g = mono(gch, 24, GLYPH_COL[gch]).move_to([self.p(gx, 0)[0], c.get_center()[1], 0])
            new.append(g)
        self.show(scene, *new, anims=[LaggedStart(*[FadeIn(g, scale=1.5) for g in new], lag_ratio=0.25)],
                  run_time=run_time, into=self.glyphs)
        if not self.compact:
            self._plan([g for g in glyphs if g])
        return new

    def _plan(self, glyphs, scene=None):
        p = self.p
        if self.plan is None:
            fr = _panel(3.8, 0.75, S.GREY, 0.05).move_to(p(-4.3, -1.98))
            t = label("plan", 20, S.GREY).move_to(p(-6.0, -1.98), aligned_edge=LEFT)
            self.plan = VGroup(fr, t)
            self.plan.row = VGroup()
            self.plan.add(self.plan.row)
            self.add(self.plan)
        self.plan.remove(self.plan.row)
        row = VGroup(*[mono(gch, 22, GLYPH_COL[gch]) for gch in glyphs]).arrange(RIGHT, buff=0.3)
        if not glyphs:
            row = VGroup(label("no changes", 20, S.GREY))
        row.move_to(self.plan[0]).align_to(self.plan[0], LEFT).shift(RIGHT * 1.0)
        self.plan.row = row
        self.plan.add(row)

    def apply(self, scene, run_time: float = 1.2):
        """PLAYS: the plan travels down a PINK arrow to the four PURPLE provider plugs, which light;
        a BLUE arrow carries the calls up into the reality tree, whose cards flash."""
        if self.compact:
            raise ValueError("EngineLoop(compact=True) has no providers")
        p = self.p
        if self.plugs is None:
            plugs = VGroup(*[tool_chip(n) for n in PROVIDERS]).arrange(RIGHT, buff=0.22)
            plugs.move_to(p(2.3, -1.98))
            self.plugs = plugs
            a = route(self.plan[0].get_right(), plugs.get_left())
            up = arrow(plugs[0].get_top() + RIGHT * 0.0, self.cards["reality"][-1].get_bottom(), CLOUD,
                       stroke=4, buff=0.05)
            up.put_start_and_end_on(p(4.0, -1.62), self.cards["reality"][-1].get_bottom() + DOWN * 0.04)
            self.flow = VGroup(a, up)
            self.show(scene, plugs, a, anims=[FadeIn(plugs), GrowArrow(a)], run_time=0.6)
            self.show(scene, up, anims=[GrowArrow(up)], run_time=0.4)
        scene.play(LaggedStart(*[Indicate(pl, color=TOOL) for pl in self.plugs], lag_ratio=0.2),
                   run_time=run_time * 0.6)
        scene.play(LaggedStart(*[Indicate(c, color=CLOUD, scale_factor=1.05) for c in self.cards["reality"]],
                               lag_ratio=0.15), run_time=run_time * 0.4)
        self.heal(scene)

    def banner(self, scene, run_time: float = 0.6):
        if self.compact:
            raise ValueError("EngineLoop(compact=True) has no banner")
        b = label("Pulumi manages infrastructure through cloud APIs", 20, INK).move_to(self.p(-2.0, -3.1))
        self.banner_m = b
        self.show(scene, b, anims=[FadeIn(b, shift=UP * 0.1)], run_time=run_time)
        return b

    def footnote(self, scene, text: str = "… and SSH, for the inside of the VM", run_time: float = 0.6):
        f = label(text, 20, S.GREY).next_to(self.banner_m, RIGHT, buff=0.25)
        keep_inside(f)
        self.show(scene, f, run_time=run_time)
        return f

    def preview_stop(self, scene, run_time: float = 0.5):
        """PLAYS: a GREY stop sign 'nothing applied' on the plan (preview ends there)."""
        oct_ = Circle(radius=0.22, stroke_color=S.GREY, stroke_width=3).set_fill(tint(S.GREY, 0.3), 1)
        bar = Line(LEFT * 0.12, RIGHT * 0.12, color=INK, stroke_width=5)
        t = label("nothing applied", 20, S.GREY)
        g = VGroup(VGroup(oct_, bar), t).arrange(RIGHT, buff=0.12)
        anchor = self.plan[0] if self.plan is not None else self.cards["desired"]
        g.next_to(anchor, DOWN, buff=0.15)
        self.show(scene, g, run_time=run_time, into=self.extras)
        if self.extras not in self.submobjects:
            self.add(self.extras)
        return g

    def in_sync(self, scene, run_time: float = 0.8):
        """PLAYS: desired = state = reality: every card glows GREEN, the plan says 'no changes'."""
        anims = [c.box.animate.set_stroke(OWN) for k in self.cards for c in self.cards[k]]
        scene.play(*anims, run_time=run_time)
        if not self.compact:
            self._plan([])
        self.heal(scene)

    def unknown(self, scene, i: int = 0, run_time: float = 0.5):
        """PLAYS: a YELLOW padlock 'unknown' right of desired card i (an Output not known in a preview)."""
        c = self.cards["desired"][i]
        pk = padlock(0.34, TURN, "unknown").next_to(c, RIGHT, buff=0.1)
        self.show(scene, pk, run_time=run_time, into=self.extras)
        if self.extras not in self.submobjects:
            self.add(self.extras)
        return pk

    def backwards(self, scene, per: float = 0.4):
        """PLAYS: destroy: RED '-' on every desired card, reality cards fade bottom-up."""
        self.diff(scene, ["-"] * len(self.names), run_time=0.8)
        for c in reversed(list(self.cards["reality"])):
            self.drop(scene, c, run_time=per)

    def clear_glyphs(self, scene):
        if len(self.glyphs):
            self.drop(scene, *list(self.glyphs.submobjects), run_time=0.2)


# ------------------------------------------------------------------ V5 · ControlRoom
class ControlRoom(_Anchored):
    """V5 · the deployment toolbox and its wires (S11). Built around ORIGIN, x -3.6 .. 3.6,
    y -2.6 .. 2.6 (place it left: md.move_to([-2.9, -0.3, 0]); a code panel beside it then has ~5.9
    units: font_size=20 and cuts=). One phase at a time fills the container below its name; take a
    phase away with clear(phase) before the next unless both fit (bricks sit at the bottom and
    coexist with lamps or env).
        laptop     GREY outline (full size), 'your laptop' top-left
        container  TEAL x -0.85 .. 3.4, y -2.4 .. 2.0, 'cheese-app-deployment' (mono) on top
        host side  labels x -3.45 .. -1.15 (label font), one row per mount (y 1.25, pitch 0.42)
        env        rows from x -0.7, y 1.3, pitch 0.31 (down to about -1.45 with the chip); the two
                   long names break after their last '_' into an indented second row
                   ('GOOGLE_APPLICATION_' / 'CREDENTIALS')
        bricks     two rows of three at y -1.65 / -2.1 · lamps x -0.55, y 1.2 .. -0.8
    PLAYS env(names=ENV_NAMES, extra=True) env names one per row inside the container (extra adds
        'PULUMI_CONFIG_PASSPHRASE=""' with its source chip 'Dockerfile:51'); env_one(i) for one row ·
        wire(i) mount i of MOUNTS (0 socket, 1 /app, 2 /secrets, 3 docker_config, 4-6 build contexts):
        host label + coloured wire + container path · wires() all · bricks() a wall of six Dockerfile
        bricks at the container's base ('line 4', 'lines 29–30' named) · brick(name, state)
        state 'red'|'green'|'grey' · lamps() the entrypoint's five lamps with labels (LAMPS) ·
        lamp_set(i, state) 'green'|'red'|'off' · clear(phase) phase 'env'|'wires'|'bricks'|'lamps'.
    .container .name .phases{phase: VGroup} .brick_map{'line 4', 'lines 29–30'} .lamp_list"""

    WIRE_COL = (LAPTOP, OWN, COST, TOOL, CONTAINER, CONTAINER, CONTAINER)

    def __init__(self, **kw):
        super().__init__(**kw)
        p = self.p
        self.laptop_fr = _panel(7.2, 5.2, LAPTOP, 0.04).move_to(p(0, 0))
        self.laptop_t = label("your laptop", 20, LAPTOP).move_to(p(-3.4, 2.32), aligned_edge=LEFT)
        self.container = _panel(4.25, 4.4, CONTAINER, 0.12).move_to(p(1.275, -0.2))
        self.name = mono(C_TOOLBOX, 20, INK).move_to(p(1.275, 1.72))
        self.add(self.laptop_fr, self.laptop_t, self.container, self.name)
        self.phases = {}
        self.brick_map = {}
        self.lamp_list = []

    def _rows_y(self, n: int, top: float = 1.25, pitch: float = 0.4):
        return [top - pitch * i for i in range(n)]

    def _phase(self, name: str) -> VGroup:
        if name not in self.phases:
            self.phases[name] = VGroup()
            self.add(self.phases[name])
        return self.phases[name]

    def env(self, scene, names=ENV_NAMES, extra: bool = True, run_time: float = 0.8):
        """PLAYS: the env names (label font, 20 pt) as rows inside the container (with the
        PULUMI_CONFIG_PASSPHRASE row and its 'Dockerfile:51' chip when extra)."""
        items = [(n, INK) for n in names] + ([('PULUMI_CONFIG_PASSPHRASE=""', S.GREY)] if extra else [])
        rows, y, avail = [], 1.3, self.container.get_right()[0] - self.p(-0.7, 0)[0] - 0.1
        for n, col in items:
            parts = [n]
            if label(n, 20).width > avail:
                k = n.rfind("_", 0, len(n) - 1) + 1
                parts = [n[:k], n[k:]]
            for j, part in enumerate(parts):
                rows.append(label(part, 20, col).move_to(self.p(-0.7 + 0.3 * j, y), aligned_edge=LEFT))
                y -= 0.31
        if extra:
            src = grey_chip("Dockerfile:51").next_to(rows[-1], DOWN, buff=0.08).align_to(self.container, RIGHT)
            src.shift(LEFT * 0.12)
            rows.append(src)
        for r in rows:
            if r.get_right()[0] > self.container.get_right()[0] - 0.1:
                raise ValueError(f"ControlRoom.env: a row is wider than the container: {r}")
        self.show(scene, *rows, anims=[LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows],
                                                   lag_ratio=0.15)], run_time=run_time, into=self._phase("env"))
        return rows

    def wire(self, scene, i: int, run_time: float = 0.6):
        """PLAYS: mount i: host label left (in the laptop), a coloured wire, the container path."""
        host, inside = MOUNTS[i]
        y = self._rows_y(len(MOUNTS), top=1.25, pitch=0.42)[i]
        col = self.WIRE_COL[i]
        h = label(host, 20, INK).move_to(self.p(-3.45, y), aligned_edge=LEFT)
        c = label(inside, 20, INK).move_to(self.p(-0.7, y), aligned_edge=LEFT)
        if h.get_right()[0] > self.p(-1.05, 0)[0] or c.get_right()[0] > self.container.get_right()[0] - 0.08:
            raise ValueError(f"ControlRoom.wire({i}): a label is too wide")
        w = Line(h.get_right() + RIGHT * 0.08, c.get_left() + LEFT * 0.08, color=col, stroke_width=5)
        self.show(scene, h, w, c, anims=[FadeIn(h), Create(w), FadeIn(c)], run_time=run_time,
                  into=self._phase("wires"))
        return VGroup(h, w, c)

    def wires(self, scene, per: float = 0.4):
        return [self.wire(scene, i, per) for i in range(len(MOUNTS))]

    def bricks(self, scene, run_time: float = 0.8):
        """PLAYS: six Dockerfile bricks along the container's base (two rows of three); bricks
        'line 4' and 'lines 29–30' are named. .brick_map[name]"""
        p = self.p
        bricks = []
        names = ("line 4", "", "lines 29–30", "", "", "")
        spots = ((-0.2, 1.1), (0.95, 1.1), (2.4, 1.6), (0.0, 1.25), (1.3, 1.25), (2.6, 1.25))
        for i, n in enumerate(names):
            r = i // 3
            x, w = spots[i]
            b = RoundedRectangle(width=w, height=0.4, corner_radius=0.04, stroke_color=S.GREY,
                                 stroke_width=2).set_fill(tint(S.GREY, 0.15), 1)
            b.move_to(p(x, -1.68 - 0.45 * r))
            g = VGroup(b)
            if n:
                g.add(label(n, 20, INK).move_to(b))
                self.brick_map[n] = g
            bricks.append(g)
        self.show(scene, *bricks, anims=[LaggedStart(*[FadeIn(b, shift=UP * 0.15) for b in bricks],
                                                     lag_ratio=0.1)], run_time=run_time, into=self._phase("bricks"))
        return bricks

    def brick(self, scene, name: str, state: str = "red", run_time: float = 0.5):
        """PLAYS: brick `name` turns RED (broke), GREEN (fixed) or GREY."""
        col = {"red": ERR, "green": OWN, "grey": S.GREY}[state]
        b = self.brick_map[name][0]
        scene.play(b.animate.set_stroke(col).set_fill(tint(col, 0.25), 1), run_time=run_time)
        self.heal(scene)

    def lamps(self, scene, run_time: float = 0.8):
        """PLAYS: the entrypoint's chain of five lamps (docker-entrypoint.sh:10-27) with their labels."""
        ys = self._rows_y(len(LAMPS), top=1.2, pitch=0.5)
        items = []
        for n, y in zip(LAMPS, ys):
            lp = lamp("off", 0.17).move_to(self.p(-0.55, y))
            t = label(n, 20, INK).next_to(lp, RIGHT, buff=0.2)
            g = VGroup(lp, t)
            g.lamp, g.text = lp, t
            items.append(g)
            self.lamp_list.append(g)
        chain = VGroup(*[Line(items[i].lamp.get_bottom(), items[i + 1].lamp.get_top(), color=S.GREY_DARK,
                              stroke_width=2) for i in range(len(items) - 1)])
        self.show(scene, chain, *items, anims=[FadeIn(chain)] + [FadeIn(g) for g in items], run_time=run_time,
                  into=self._phase("lamps"))
        return items

    def lamp_set(self, scene, i: int, state: str = "green", run_time: float = 0.4):
        """PLAYS: lamp i (0-4) turns 'green' / 'red' / 'off'."""
        g = self.lamp_list[i]
        new = lamp(state, 0.17).move_to(g.lamp)
        old = g.lamp
        self.swap(scene, old, new, run_time=run_time)
        g.lamp = new
        return new

    def clear(self, scene, phase: str, run_time: float = 0.4):
        """PLAYS: phase 'env' | 'wires' | 'bricks' | 'lamps' leaves the picture."""
        g = self.phases.pop(phase, None)
        if g is not None and len(g):
            self.drop(scene, g, run_time=run_time)
        if phase == "lamps":
            self.lamp_list = []
        if phase == "bricks":
            self.brick_map = {}


# ------------------------------------------------------------------ V6 · TimestampPipe
class TimestampPipe(_Anchored):
    """V6 · three Dockerfiles become stamped crates, shelved in Artifact Registry; the stamp rides a
    ticket through the StackReference pipe (S13, S15, S16). Built around ORIGIN, x -6.3 .. 6.4,
    y -2.4 .. 2.25:
        files     x -6.3 .. -4.4: file glyph + 'api-service' / 'frontend-react' / 'vector-db' at
                  y 1.2 / 0.3 / -0.6
        conveyor  crates x -3.9 .. -2.0 (1.9 x 0.62) on the same rows
        shelf     BLUE 'Artifact Registry' x -1.3 .. 3.0 (two columns: run 1 x -0.25, run 2 x 1.95)
        ticket    GREEN x 3.55 .. 6.35, y 1.2: 'pulumi.export' + the stamp (mono)
        pipe      PINK, x 4.95 from the ticket down to the 'deploy-single-vm' card (y -1.95);
                  'StackReference' over 'organization/deploy-images/dev' (mono) at its left (x -1.6 .. 3.4)
    PLAYS files() · shelf_on() · crates_up() (files become crates) · stamp(stamp=STAMP_1) (a YELLOW 'tag' badge on
        each crate; .stamp_text) · shelve() (crates of the current run move to the shelf column) ·
        ticket() (pulumi.export: the stamp is copied onto the ticket) · pipe() (pipe + card + name;
        the ticket slides down it to the card 'deploy-single-vm') · refused(i=1) (crate i bounces off a RED padlock at
        the shelf: the 403) · second_run(stamp=STAMP_2) (three new crates on the conveyor, stamped
        with a later stamp, shelved in column 2) · retain() (GOLD padlocks on every shelved crate).
    .shelf .crates[run] (lists) .ticket_m .pipe_m .card"""

    NAMES = ("api-service", "frontend-react", "vector-db")
    ROW_Y = (1.2, 0.3, -0.6)

    def __init__(self, **kw):
        super().__init__(**kw)
        p = self.p
        fr = _panel(4.3, 3.15, CLOUD, 0.05).move_to(p(0.85, 0.25))
        t = label("Artifact Registry", 20, CLOUD).move_to(p(0.85, 2.0))
        self.shelf = VGroup(fr, t)
        self.shelf.frame = fr
        self.crates = {}
        self.run_n = 0
        self.files_m = None
        self.ticket_m = self.pipe_m = self.card = None
        self.stamp_text = STAMP_1
        self.badges = VGroup()
        self.add(self.badges)

    def files(self, scene, run_time: float = 0.6):
        rows = []
        for n, y in zip(self.NAMES, self.ROW_Y):
            g = VGroup(file_glyph(0.34, LAPTOP), label(n, 20, INK)).arrange(RIGHT, buff=0.12)
            g.move_to(self.p(-6.3, y), aligned_edge=LEFT)
            rows.append(g)
        self.files_m = VGroup(*rows)
        hd = label("Dockerfiles", 20, S.GREY).next_to(self.files_m, UP, buff=0.2).align_to(self.files_m, LEFT)
        self.files_head = hd
        self.show(scene, hd, *rows, run_time=run_time)
        return self.files_m

    def crates_up(self, scene, run_time: float = 0.9):
        """PLAYS: each Dockerfile row sends a TEAL crate onto the conveyor (run 1)."""
        self.run_n = 1
        cr = [crate(n).move_to(self.p(-2.95, y)) for n, y in zip(self.NAMES, self.ROW_Y)]
        srcs = [c.copy().move_to(f).set_opacity(0) for c, f in zip(cr, self.files_m or cr)]
        self.crates[1] = cr
        self.show(scene, *cr, anims=[ReplacementTransform(s, c) for s, c in zip(srcs, cr)], run_time=run_time)
        return cr

    def stamp(self, scene, stamp: str = STAMP_1, run: int | None = None, run_time: float = 0.6):
        """PLAYS: a YELLOW 'tag' badge stamps each crate of the run (the stamp string is kept for
        the ticket: datetime.now().strftime('%Y%m%d%H%M%S'), b34/b35b)."""
        run = run or self.run_n
        self.stamp_text = stamp
        bs = []
        for c in self.crates[run]:
            b = chip("tag", TURN, size=20).move_to(c.get_corner(UR) + np.array([-0.05, 0.05, 0]))
            b.crate = c
            bs.append(b)
            c.badge = b
        self.show(scene, *bs, anims=[LaggedStart(*[FadeIn(b, scale=1.6) for b in bs], lag_ratio=0.2)],
                  run_time=run_time, into=self.badges)
        return bs

    def shelve(self, scene, run: int | None = None, run_time: float = 0.8):
        """PLAYS: the run's crates (with badges) move onto the shelf (column 1 or 2)."""
        run = run or self.run_n
        x = -0.25 if run == 1 else 1.95
        anims = []
        for c, y in zip(self.crates[run], self.ROW_Y):
            dx = self.p(x, y) - c.get_center()
            anims.append(c.animate.shift(dx))
            if hasattr(c, "badge"):
                anims.append(c.badge.animate.shift(dx))
        self.shelf_on(scene)
        scene.play(*anims, run_time=run_time)
        self.heal(scene)

    def shelf_on(self, scene, run_time: float = 0.4):
        """PLAYS: the BLUE 'Artifact Registry' shelf appears behind everything (shelve() calls it)."""
        if self.shelf not in self.submobjects:
            self.show(scene, self.shelf, run_time=run_time)
            self.remove(self.shelf)
            self.submobjects.insert(0, self.shelf)
            self.heal(scene)
        return self.shelf

    def ticket(self, scene, run_time: float = 0.8):
        """PLAYS: pulumi.export: a GREEN ticket with the stamp (copied from a badge)."""
        hd = mono("pulumi.export", 20, OWN)
        st = mono(self.stamp_text, 20, TURN)
        inner = VGroup(hd, st).arrange(DOWN, buff=0.1)
        fr = RoundedRectangle(width=inner.width + 0.4, height=inner.height + 0.3, corner_radius=0.08,
                              stroke_color=OWN, stroke_width=3).set_fill(tint(OWN, 0.15), 1)
        tk = VGroup(fr, inner.move_to(fr)).move_to(self.p(4.95, 1.2))
        tk.frame, tk.stamp = fr, st
        if self.ticket_m is not None:
            self.drop(scene, self.ticket_m, run_time=0.2)
        self.ticket_m = tk
        src = self.badges[-1].copy() if len(self.badges) else tk.copy().set_opacity(0)
        scene.add(src)
        self.show(scene, tk, anims=[ReplacementTransform(src, tk)], run_time=run_time)
        scene.remove(src)
        return tk

    def pipe(self, scene, run_time: float = 1.2):
        """PLAYS: the PINK StackReference pipe and the 'deploy-single-vm' card; the ticket
        slides down to the card."""
        p = self.p
        card = VGroup(label("deploy-single-vm", 20, INK))
        cfr = RoundedRectangle(width=card.width + 0.4, height=0.55, corner_radius=0.08, stroke_color=OWN,
                               stroke_width=3).set_fill(tint(OWN, 0.12), 1)
        card = VGroup(cfr, card[0].move_to(cfr)).move_to(p(4.95, -1.95))
        tube = VGroup(Line(p(4.8, 0.55), p(4.8, -1.68), color=ROUTE, stroke_width=4),
                      Line(p(5.1, 0.55), p(5.1, -1.68), color=ROUTE, stroke_width=4))
        nm = mono("organization/deploy-images/dev", 20, ROUTE).move_to(p(0.9, -1.95))
        sr = label("StackReference", 20, ROUTE).next_to(nm, UP, buff=0.08)
        self.card, self.pipe_m = card, VGroup(tube, nm, sr)
        self.show(scene, tube, card, nm, sr, anims=[Create(tube), FadeIn(card), FadeIn(nm), FadeIn(sr)],
                  run_time=0.8)
        if self.ticket_m is not None:
            scene.play(self.ticket_m.animate.move_to(p(4.95, -1.05)), run_time=run_time)
            scene.play(Indicate(card, color=OWN, scale_factor=1.05), run_time=0.4)
        self.heal(scene)

    def refused(self, scene, i: int = 1, run_time: float = 0.9, keep: bool = False):
        """PLAYS: crate i of the current run heads for the shelf and bounces off a RED padlock (403);
        the padlock then leaves (keep=True leaves it: .refused_lock)."""
        c = self.crates[self.run_n][i]
        lock = padlock(0.42, ERR).move_to(self.p(-1.3, self.ROW_Y[i]))
        self.show(scene, lock, run_time=0.3)
        parts = [c] + ([c.badge] if hasattr(c, "badge") else [])
        dx = RIGHT * (lock.get_left()[0] - c.get_right()[0] - 0.05)
        scene.play(*[m.animate.shift(dx) for m in parts], run_time=run_time * 0.5)
        scene.play(*[m.animate.shift(-dx) for m in parts], Indicate(lock, color=ERR), run_time=run_time * 0.5)
        self.refused_lock = lock
        if not keep:
            self.drop(scene, lock, run_time=0.3)
            self.refused_lock = None
        self.heal(scene)
        return lock

    def second_run(self, scene, stamp: str = STAMP_2):
        """PLAYS: a second `up`: three new crates on the conveyor, stamped later, shelved in column 2."""
        self.run_n = 2
        cr = [crate(n).move_to(self.p(-2.95, y)) for n, y in zip(self.NAMES, self.ROW_Y)]
        self.crates[2] = cr
        self.show(scene, *cr, anims=[FadeIn(c, shift=RIGHT * 0.3) for c in cr], run_time=0.6)
        self.stamp(scene, stamp, run=2)
        self.shelve(scene, run=2)

    def retain(self, scene, run_time: float = 0.6):
        """PLAYS: a small GOLD padlock on every shelved crate (retain_on_delete)."""
        locks = []
        for run, cr in self.crates.items():
            for c in cr:
                locks.append(padlock(0.3, COST).move_to(c.get_corner(DL) + np.array([0.18, 0.05, 0])))
        self.show(scene, *locks, anims=[LaggedStart(*[FadeIn(lk, scale=1.4) for lk in locks], lag_ratio=0.1)],
                  run_time=run_time)
        return locks


# ------------------------------------------------------------------ V7a · VmFences
class VmFences(_Anchored):
    """V7a · the VPC, its gates and the disk (create_instance.py; S14). Built around ORIGIN,
    x -6.3 .. 2.2 without the plan, x -6.3 .. 6.4 with it; y -2.85 .. 2.6.
        VPC        BLUE outline x -4.1 .. 2.2, y -2.2 .. 2.2; 'VPC · cheese-app-network' above it (y 2.42)
        gates      PINK plates on its left edge (x -4.1) at y 1.0 (80), 0.0 (443), -1.0 (22), each with
                   its rule outside to the left (right-aligned at x -4.6): 'http-server', 'https-server',
                   'every VM'
        VM         BLUE box x -2.9 .. 0.5, y -0.85 .. 0.85, 'VM' + tag chips inside (wear_tags)
        envelope   sealed PINK envelope '<instance_ip>' above the VM (y 1.5)
        disk       cylinder (-1.2, -1.6) on a cable; caption row y -2.6 under the VPC
        plan       x 2.7 .. 6.4: rows (glyph + resource) at y 1.6 … -1.4 (plan_rows)
    PLAYS vpc() · gate(port) one of '80' '443' '22' (or gates() all three) · vm() · wear_tags() ·
        disk() · envelope() · open_envelope(text=IP_PH) · caption(text) (replaces the last one) ·
        plan_rows(rows=PLAN_ROWS) the plan list, GREY until ticked · tick(i, glyph='+') · fail(i)
        (row i RED + RED cross: b43's get_image).
    .gates{port} .vm_box .tags .disk_m .env .plan"""

    PLAN_ROWS = ("Disk", "Network", "Firewall · allow-http", "Firewall · allow-https", "Firewall · allow-ssh",
                 "get_image")
    GATES = {"80": (1.0, "http-server"), "443": (0.0, "https-server"), "22": (-1.0, "every VM")}

    def __init__(self, **kw):
        super().__init__(**kw)
        self.gates, self.plan = {}, None
        self.vm_box = self.tags = self.disk_m = self.env = self.cap = None

    def vpc(self, scene, run_time: float = 0.8):
        p = self.p
        fr = _panel(6.3, 4.4, CLOUD, 0.03).move_to(p(-0.95, 0))
        t = VGroup(label("VPC ·", 20, CLOUD), mono(NETWORK, 20, CLOUD)).arrange(RIGHT, buff=0.12)
        t.move_to(p(-4.1, 2.42), aligned_edge=LEFT)
        self.frame = fr
        self.show(scene, fr, t, anims=[Create(fr), FadeIn(t)], run_time=run_time)
        return fr

    def gate(self, scene, port: str, run_time: float = 0.5):
        y, rule = self.GATES[port]
        d = door(port, ROUTE, door_w=0.85).move_to(self.p(-4.1, y))
        r = (mono if "-" in rule else label)(rule, 20, ROUTE if port != "22" else S.GREY)
        r.move_to(self.p(-4.6, y), aligned_edge=RIGHT)
        g = VGroup(d, r)
        g.plate, g.rule = d, r
        self.gates[port] = g
        self.show(scene, g, anims=[GrowFromCenter(d), FadeIn(r, shift=RIGHT * 0.2)], run_time=run_time)
        return g

    def gates_all(self, scene, per: float = 0.4):
        for port in self.GATES:
            self.gate(scene, port, per)

    def vm(self, scene, run_time: float = 0.6):
        fr = _panel(3.4, 1.7, CLOUD, 0.1).move_to(self.p(-1.2, 0))
        t = label("VM", 22, CLOUD).move_to(fr.get_corner(UL) + np.array([0.2, -0.25, 0]), aligned_edge=LEFT)
        self.vm_box = VGroup(fr, t)
        self.vm_box.frame = fr
        self.show(scene, self.vm_box, anims=[FadeIn(self.vm_box, scale=0.95)], run_time=run_time)
        return self.vm_box

    def wear_tags(self, scene, run_time: float = 0.6):
        """PLAYS: the VM wears 'http-server' and 'https-server' (PINK chips inside it)."""
        tags = VGroup(route_chip("http-server"), route_chip("https-server")).arrange(DOWN, buff=0.1)
        tags.move_to(self.vm_box.frame).shift(RIGHT * 0.35 + DOWN * 0.12)
        self.tags = tags
        anims = [FadeIn(tags, shift=DOWN * 0.1)]
        for port in ("80", "443"):
            if port in self.gates:
                anims.append(Indicate(self.gates[port].plate, color=ROUTE))
        self.show(scene, tags, anims=anims, run_time=run_time)
        return tags

    def disk(self, scene, run_time: float = 0.6):
        cyl = disk_cyl(0.6).move_to(self.p(-1.2, -1.65))
        cable = Line(self.p(-1.2, -0.85), cyl.get_top(), color=CLOUD, stroke_width=4)
        t = mono("/mnt/disk-1", 20, INK).next_to(cyl, RIGHT, buff=0.2)
        self.disk_m = VGroup(cable, cyl, t)
        self.disk_m.cyl = cyl
        self.show(scene, self.disk_m, anims=[Create(cable), FadeIn(cyl, shift=UP * 0.2), FadeIn(t)], run_time=run_time)
        return self.disk_m

    def envelope(self, scene, run_time: float = 0.6):
        """PLAYS: the sealed PINK envelope '<instance_ip>' (an Output) above the VM."""
        e = envelope(IP_PH, ROUTE).move_to(self.p(-1.2, 1.45))
        self.env = e
        self.show(scene, e, anims=[FadeIn(e, shift=DOWN * 0.2)], run_time=run_time)
        return e

    def open_envelope(self, scene, run_time: float = 0.6):
        """PLAYS: the VM turns GREEN and the envelope's flap opens (the value stays a placeholder)."""
        fl = self.env.flap
        new = VMobject(stroke_color=ROUTE, stroke_width=2.5).set_points_as_corners(
            [self.env.body.get_corner(UL), self.env.body.get_top() + UP * 0.3, self.env.body.get_corner(UR)])
        scene.play(Transform(fl, new), self.vm_box.frame.animate.set_stroke(OWN), run_time=run_time)
        self.heal(scene)

    def caption(self, scene, text: str, color=S.GREY, run_time: float = 0.5):
        """PLAYS: a caption row under the VPC (y -2.6), replacing the previous one."""
        c = label(text, 20, color).move_to(self.p(-0.95, -2.6))
        if self.cap is not None:
            self.swap(scene, self.cap, c, run_time=run_time)
        else:
            self.show(scene, c, run_time=run_time)
        self.cap = c
        return c

    def plan_rows(self, scene, rows=None, run_time: float = 0.8):
        """PLAYS: the plan list right of the VPC: one GREY row per resource (glyph slot empty)."""
        rows = rows or self.PLAN_ROWS
        g = VGroup()
        for i, r in enumerate(rows):
            t = label(r, 20, S.GREY).move_to(self.p(3.1, 1.6 - 0.6 * i), aligned_edge=LEFT)
            if t.get_right()[0] > self.p(6.4, 0)[0]:
                raise ValueError(f"VmFences.plan_rows: {r!r} too wide")
            g.add(t)
        hd = label("plan", 20, S.GREY).move_to(self.p(2.7, 2.2), aligned_edge=LEFT)
        self.plan = g
        self.plan_glyphs = {}
        self.show(scene, hd, g, run_time=run_time)
        return g

    def tick(self, scene, i: int, glyph: str = "+", run_time: float = 0.35):
        """PLAYS: plan row i gets its glyph (GREEN '+') and lights up."""
        r = self.plan[i]
        gl = mono(glyph, 22, GLYPH_COL.get(glyph, OWN)).next_to(r, LEFT, buff=0.15)
        self.plan_glyphs[i] = gl
        self.show(scene, gl, anims=[FadeIn(gl, scale=1.4)], extra=[r.animate.set_color(INK)], run_time=run_time)
        return gl

    def fail(self, scene, i: int, run_time: float = 0.5):
        """PLAYS: plan row i turns RED with a RED cross (the first call that needs Google)."""
        r = self.plan[i]
        x = cross_glyph(0.24).next_to(r, LEFT, buff=0.18)
        self.show(scene, x, anims=[Create(x)], extra=[r.animate.set_color(ERR)], run_time=run_time)
        return x


# ------------------------------------------------------------------ V7b · ProvisionDominoes
class ProvisionDominoes(_Anchored):
    """V7b · provision_instance.py's remote.Commands as numbered tiles in their depends_on chain
    (S14), or any short chain (S15: labels=('upload', 'move', 'restart'), rows=(3,)). Built around
    ORIGIN. Default: 9 tiles snaking 5 + 4 (row 1 left→right at y 0.75, row 2 right→left at y -0.95),
    tile 1.55 x 1.0 (number 22 pt + label 20 pt, labels ≤ 8 characters), pitch 2.05: x -4.1 .. 4.1
    plus the tiles' half widths, y -1.45 .. 1.25. depends_on arrows between tiles (a curved one at the turn).
    PLAYS fall(upto=None, per=0.25) tiles tip over in order (GREY, rotated) · stand() all upright ·
        refuse(i=0, note='has a filesystem') tile i wobbles and stays up with a GREEN check ·
        disk(labels=('chat history', 'model')) a disk cylinder under tile 1 with GREY labels ·
        wipe() a GREY ghost of tile 1 falls onto the disk, whose labels turn RED and vanish ·
        restore() the disk's labels come back GREEN · replay(indices) only those tiles flash and tip.
    .tiles[i] (.frame .num .text) .arrows"""

    def __init__(self, labels=DOMINOES, rows=(5, 4), pitch: float = 2.05, **kw):
        super().__init__(**kw)
        self.tiles, self.arrows = VGroup(), VGroup()
        pos = []
        ys = [0.75, -0.95] if len(rows) == 2 else [0.0]
        k = 0
        for r, n in enumerate(rows):
            xs = [-(n - 1) * pitch / 2 + pitch * j for j in range(n)] if len(rows) == 1 else \
                 [-2 * pitch + pitch * j for j in range(n)]
            if r == 1:
                xs = list(reversed([-2 * pitch + pitch * j + pitch for j in range(n)]))
            for x in xs:
                pos.append((x, ys[r]))
                k += 1
        for i, (lab, (x, y)) in enumerate(zip(labels, pos)):
            fr = RoundedRectangle(width=1.55, height=1.0, corner_radius=0.08, stroke_color=TOOL,
                                  stroke_width=3).set_fill(tint(TOOL, 0.15), 1)
            num = label(str(i + 1), 22, TURN)
            t = label(lab, 20, INK)
            if t.width > 1.4:
                raise ValueError(f"ProvisionDominoes: label {lab!r} too wide")
            VGroup(num, t).arrange(DOWN, buff=0.08).move_to(fr)
            g = VGroup(fr, num, t).move_to(self.p(x, y))
            g.frame, g.num, g.text = fr, num, t
            self.tiles.add(g)
        for a, b in zip(self.tiles[:-1], self.tiles[1:]):
            if abs(a.get_center()[1] - b.get_center()[1]) < 0.1:
                d = RIGHT if b.get_center()[0] > a.get_center()[0] else LEFT
                ar = arrow(a.get_edge_center(d), b.get_edge_center(-d), S.GREY, stroke=3, buff=0.05)
            else:
                ar = arrow(a.get_bottom(), b.get_top(), S.GREY, stroke=3, buff=0.05)
            self.arrows.add(ar)
        self.add(self.arrows, self.tiles)
        self.disk_m = None
        self._fallen = set()
        self._pivot = {}

    def fall(self, scene, upto: int | None = None, per: float = 0.25):
        """PLAYS: tiles 1..upto tip over in order (rotate, GREY): the scripts run."""
        upto = len(self.tiles) if upto is None else upto
        for i in range(upto):
            if i in self._fallen:
                continue
            t = self.tiles[i]
            self._pivot[i] = t.frame.get_corner(DR).copy()
            scene.play(Rotate(t, -PI / 9, about_point=self._pivot[i]), t.frame.animate.set_stroke(S.GREY),
                       run_time=per)
            self._fallen.add(i)
        self.heal(scene)

    def stand(self, scene, run_time: float = 0.6):
        """PLAYS: every fallen tile stands up again (PURPLE)."""
        anims = []
        for i in sorted(self._fallen):
            t = self.tiles[i]
            anims += [Rotate(t, PI / 9, about_point=self._pivot[i]), t.frame.animate.set_stroke(TOOL)]
        if anims:
            scene.play(*anims, run_time=run_time)
        self._fallen = set()
        self.heal(scene)

    def refuse(self, scene, i: int = 0, note: str = "has a filesystem", run_time: float = 0.8):
        """PLAYS: tile i wobbles and stays up; a GREEN check and the note appear above it."""
        t = self.tiles[i]
        scene.play(Rotate(t, -PI / 30, about_point=t.get_bottom()), run_time=run_time * 0.3)
        scene.play(Rotate(t, PI / 30, about_point=t.get_bottom()), run_time=run_time * 0.3)
        ck = VGroup(check_glyph(0.3), label(note, 20, OWN)).arrange(RIGHT, buff=0.12).next_to(t, UP, buff=0.15)
        keep_inside(ck)
        self.show(scene, ck, run_time=run_time * 0.4)
        return ck

    def disk(self, scene, labels=("chat history", "model"), run_time: float = 0.6):
        """PLAYS: a disk cylinder under tile 1 (between the rows' left ends) with GREY labels."""
        t = self.tiles[0]
        cyl = disk_cyl(0.7).next_to(t, DOWN, buff=0.35)
        labs = VGroup(*[label(s, 20, S.GREY) for s in labels]).arrange(DOWN, buff=0.06).next_to(cyl, LEFT, buff=0.15)
        keep_inside(labs)
        self.disk_m = VGroup(cyl, labs)
        self.disk_m.labels = labs
        self.show(scene, self.disk_m, run_time=run_time)
        return self.disk_m

    def wipe(self, scene, run_time: float = 1.0):
        """PLAYS: a GREY ghost of tile 1 (no guard) falls onto the disk; its labels go RED and vanish."""
        t = self.tiles[0]
        ghost = t.copy().set_opacity(0.35).set_color(S.GREY)
        scene.add(ghost)
        scene.play(Rotate(ghost, -PI / 2.2, about_point=ghost.get_corner(DR)),
                   ghost.animate.move_to(self.disk_m[0].get_center() + UP * 0.2), run_time=run_time * 0.5)
        labs = self.disk_m.labels
        scene.play(labs.animate.set_color(ERR), run_time=run_time * 0.2)
        scene.play(FadeOut(labs), FadeOut(ghost), run_time=run_time * 0.3)
        scene.remove(ghost)
        self._detach(labs)
        scene.remove(labs)
        self.heal(scene)

    def restore(self, scene, run_time: float = 0.5):
        """PLAYS: the disk's labels come back GREEN (the guarded run)."""
        labs = self.disk_m.labels.copy().set_color(OWN).set_opacity(1)
        self.disk_m.labels = labs
        self.show(scene, labs, run_time=run_time, into=self.disk_m)

    def replay(self, scene, indices, per: float = 0.3):
        """PLAYS: only tiles `indices` flash YELLOW and tip (S15's checksum trigger)."""
        for i in indices:
            t = self.tiles[i]
            scene.play(Indicate(t.frame, color=TURN, scale_factor=1.05), run_time=per)
        for i in indices:
            t = self.tiles[i]
            pv = t.frame.get_corner(DR).copy()
            scene.play(Rotate(t, -PI / 9, about_point=pv), run_time=per)
            scene.play(Rotate(t, PI / 9, about_point=pv), run_time=per * 0.6)
        self.heal(scene)


# ------------------------------------------------------------------ V8 · KeyRing
class KeyRing(_Anchored):
    """V8 · two keys, two kinds of doors (slide 25; S10, S15). Built around ORIGIN, card x -3.6 .. 3.6,
    y -1.85 .. 1.85:
        row 0  y 0.85: GREY header 'builds things' above three doors 'create' / 'SSH' / 'delete'
               (x -3.3 .. 1.45), the key hook at x 2.5 (deployment.json: BLUE, RED rim)
        row 1  y -0.95: 'runs things': 'read' 'images' · 'read stored' 'files' · 'use' 'Vertex AI';
               hook for gcp-service.json (GREEN)
    PLAYS roles(row, roles=None, at=None) the README's roles as chips in a column (top-left at `at`;
        default: right-aligned just left of the card, so shift the card right by ~2.6) that fly into the
        row's doors (the doors open, tinted) · key(row) the key glyph + file name hangs on its hook ·
        your_project(text=...) a GREY line under the card with 'your' YELLOW and a struck
        'ac215-project' beside it.
    .doors[row][i] .hooks[row] .keys[row] .frame"""

    DOORS = ((("create",), ("SSH",), ("delete",)),
             (("read", "images"), ("read stored", "files"), ("use", "Vertex AI")))
    HEADS = ("builds things", "runs things")

    def __init__(self, **kw):
        super().__init__(**kw)
        self.frame = _panel(7.2, 3.7, S.GREY, 0.04).move_to(self.p(0, 0))
        self.doors, self.hooks, self.keys, self.heads = [[], []], [None, None], [None, None], []
        self.add(self.frame)
        for r, y in enumerate((0.55, -1.25)):
            hd = label(self.HEADS[r], 20, S.GREY).move_to(self.p(-3.3, y + 0.85), aligned_edge=LEFT)
            self.heads.append(hd)
            self.add(hd)
            for i, rows in enumerate(self.DOORS[r]):
                fr = RoundedRectangle(width=1.5, height=0.95, corner_radius=0.06, stroke_color=S.GREY,
                                      stroke_width=2.5).set_fill(PANEL, 1)
                t = VGroup(*[label(s, 20, INK) for s in rows]).arrange(DOWN, buff=0.04)
                if t.width > 1.42:
                    raise ValueError(f"KeyRing door {rows} too wide")
                d = VGroup(fr, t.move_to(fr)).move_to(self.p(-2.55 + 1.62 * i, y))
                d.frame, d.text = fr, t
                self.doors[r].append(d)
                self.add(d)
            hook = Dot(radius=0.06, color=S.GREY).move_to(self.p(2.5, y + 0.4))
            self.hooks[r] = hook
            self.add(hook)

    def roles(self, scene, row: int, roles=None, at=None, run_time: float = 1.2):
        """PLAYS: the role chips (GREY, label font) appear in a column (at=(x, y) of its top-left,
        default left of the card), then fly into the row's doors, which open (BLUE/GREEN tint)."""
        roles = roles or (ROLES_DEPLOY if row == 0 else ROLES_SERVICE)
        col = CLOUD if row == 0 else OWN
        chips = VGroup(*[grey_chip(r) for r in roles]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        if at is not None:
            chips.move_to([at[0], at[1], 0], aligned_edge=UL)
        else:
            chips.move_to(self.frame.get_corner(UL) + LEFT * 0.25, aligned_edge=UR)
        keep_inside(chips)
        self.show(scene, *chips, anims=[LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in chips],
                                                    lag_ratio=0.12)], run_time=run_time * 0.5)
        doors = self.doors[row]
        moves = [c.animate.move_to(doors[i % len(doors)].frame).set_opacity(0) for i, c in enumerate(chips)]
        scene.play(LaggedStart(*moves, lag_ratio=0.1),
                   *[d.frame.animate.set_stroke(col).set_fill(tint(col, 0.2), 1) for d in doors],
                   run_time=run_time * 0.5)
        for c in chips:
            self._detach(c)
        scene.remove(*chips)
        self.heal(scene)

    def key(self, scene, row: int, run_time: float = 0.6):
        """PLAYS: the row's key (deployment.json / gcp-service.json) hangs on its hook."""
        k = key_icon("deploy" if row == 0 else "service", True, 0.9)
        k.next_to(self.hooks[row], DOWN, buff=0.05)
        self.keys[row] = k
        self.show(scene, k, anims=[FadeIn(k, shift=DOWN * 0.3)], run_time=run_time)
        return k

    def your_project(self, scene, run_time: float = 0.6):
        """PLAYS: 'admin on your group's project' under the card, 'your' YELLOW, with a struck GREY
        'ac215-project' beside it."""
        line = VGroup(label("admin on", 20, S.GREY), label("your", 20, TURN), label("group's project", 20, S.GREY))
        line.arrange(RIGHT, buff=0.12)
        old = mono(PROJECT_README, 20, S.GREY)
        g = VGroup(line, old).arrange(RIGHT, buff=0.5).next_to(self.frame, DOWN, buff=0.2)
        st = strike(old, S.GREY)
        self.show(scene, g, st, anims=[FadeIn(g), Create(st)], run_time=run_time,
                  extra=[Indicate(line[1], color=TURN)])
        return g


class SshKey(_Anchored):
    """V8 in S12 · the PURPLE key cut in two; its public half goes up to the service account's OS Login
    profile, which hands back the Linux user name. Built around ORIGIN, x -3.3 .. 3.5, y -1.4 .. 1.7:
        key      PURPLE 'ssh-key-deployment' at (-2.2, -0.6) (key_icon('ssh'))
        halves   'private' stays at (-2.6, -0.6); '.pub' goes to (-1.2, -0.6)
        profile  BLUE card 'deployment · OS Login profile' at (1.5, 1.2)
        name tag YELLOW 'sa_000…' (mono) handed back to (1.5, -0.6)
    PLAYS appear() · cut() (the key splits; 'private' / '.pub' labels) · upload() (.pub flies up into
        the profile card) · username() (the YELLOW tag comes back down). .key .halves .profile .name_tag"""

    def __init__(self, **kw):
        super().__init__(**kw)
        self.key = key_icon("ssh", True, 1.1).move_to(self.p(-2.2, -0.6))
        self.halves = self.profile = self.name_tag = None

    def appear(self, scene, run_time: float = 0.6):
        self.show(scene, self.key, anims=[FadeIn(self.key, shift=UP * 0.2)], run_time=run_time)
        return self.key

    def cut(self, scene, run_time: float = 0.8):
        """PLAYS: the key splits into two PURPLE halves labelled 'private' and '.pub'."""
        left = key_icon("ssh", "private", 0.8).move_to(self.p(-2.7, -0.6))
        right = key_icon("ssh", ".pub", 0.8).move_to(self.p(-1.1, -0.6))
        old = self.key
        self._detach(old)
        scene.add(old)
        scene.play(ReplacementTransform(old, VGroup(left, right)), run_time=run_time)
        scene.remove(old, left, right)
        self.halves = VGroup(left, right)
        self.add(self.halves)
        self.heal(scene)
        return self.halves

    def upload(self, scene, run_time: float = 0.9):
        """PLAYS: the BLUE OS Login profile card appears; '.pub' flies up into it."""
        t = VGroup(label("deployment", 20, INK), label("OS Login profile", 20, CLOUD)).arrange(DOWN, buff=0.06)
        fr = _panel(t.width + 0.5, t.height + 0.35, CLOUD, 0.12)
        prof = VGroup(fr, t.move_to(fr)).move_to(self.p(1.5, 1.2))
        self.profile = prof
        self.show(scene, prof, run_time=0.4)
        pub = self.halves[1]
        scene.play(pub.animate.move_to(prof.get_bottom() + DOWN * 0.45), run_time=run_time)
        self.heal(scene)

    def username(self, scene, run_time: float = 0.7):
        """PLAYS: the profile hands back the YELLOW name tag 'sa_000…' (masked)."""
        tg = chip(SA_SHORT, TURN, size=20, font=MONO)
        tg.next_to(self.profile, RIGHT, buff=0.15)
        self.name_tag = tg
        self.show(scene, tg, anims=[FadeIn(tg)], run_time=0.3)
        scene.play(tg.animate.move_to(self.p(1.5, -0.6)), run_time=run_time)
        self.heal(scene)
        return tg
