"""Shared scene code for AC215 L14 (serverless deployment: a function, a service and a job on Cloud
Run; follow-along of dlops-io/serverless-deployment @ 46cc62f).

Paths, narration (SAY lines straight from script.md), the semantic colours of BRIEF.md, the running
example (README placeholders only), the sixteen README trackers, loaders for the real captures in
assets/terminal (multi-line commands split off), the RECORDED quotes of assets/terminal/expected,
source panels from assets/source, terminal helpers, tags, chips, cards, small glyphs, the schematic
console form, and the video's set pieces V1-V8 (+ helpers). Generic helpers come from L11's
common.py (tested); the set pieces are new. build/common_test.py (Bench) plays every helper once.

    from manim import *          # first
    from common import *         # second (common's names win), then:
    SAY = NARRATION["S07"]; assert len(SAY) == SAY_COUNT["S07"]   # one voiceover block per SAY

Notes for scene authors
=======================
Rules. Every text here is >= 20 pt: never .scale() a group that holds text below 1.0 (pieces take
size / width parameters instead; text-free icons exist for small copies). Never set width / height
/ color / depth on a VGroup subclass (Manim properties): these classes use cell_w, box_w ...
Methods marked PLAYS take the scene first, play their own animation (pass `extra=[...]` to run other
animations alongside, `run_time=` to time them) and then keep the new mobjects inside the piece,
so a later FadeOut(piece) takes them all. Methods marked ANIM return an animation you play. To take
one part away use piece.drop(self, part): never FadeOut a member of a piece directly (it snaps back
when the piece is next drawn). Pieces are built centred near ORIGIN in the layout noted below; place
them (shift / move_to / next_to) BEFORE their first PLAYS call, or between calls: every PLAYS
method builds its new parts at the piece's current position.

Frame budget. Safe frame x in [-6.6, 6.6], y in [-3.6, 3.6]. Tracker top-left (left -6.5, top 3.5,
lowest point TRACK_BOTTOM 2.9); lecture tag lref("10–11") top right; pictures stay below PIC_TOP
2.8. Terminals: term() is 12.6 wide, bottom edge at BOTTOM -3.5; a 3-row strip's top is STRIP_TOP
(-1.44), so a picture over a strip lives in y in [-1.3, 2.8].

Data
    NARRATION["S01"] .. ["S16"]  SAY_COUNT  TITLES[cls]  SPEC (video.yaml)
    Names (README's own placeholders, read from captures/README where they appear there):
    IMAGE_REF (the public image, verbatim) IMAGE_TAG DIGEST DIGEST_SHORT digest_short(head, tail)
    FUNCTION SERVICE JOB RUNTIME_SA JOB_SA WEB_EMAIL JOB_EMAIL ENTRY PROJECT_PH STANDIN_PROJECT
    IN_BUCKET OUT_BUCKET DEV_EMAIL REGION REGION_CITY SPEECH_LOCATION FUNCTION_URL SERVICE_URL
    QUERY (README:163) ARGS (the eleven argument chips, README:755-765) ARGS_SHORT (gs:// elided)
    EXEC_ID ATTEMPT JOB_STEPS WORKSHEET (the worksheet names, README:46-55) TTS_MODEL
    Prompts P_HOME, P_REPO, P_APP, P_FUNC; titles T_LAPTOP 'laptop', T_DEV 'laptop · dev shell',
    T_GCLOUD 'laptop · gcloud', T_TAB 'laptop · second tab'.

Trackers (script.md conventions; placed top-left)
    tracker(key, step=None, extra=False) with key in TRACKER_KEYS: "BB", "1.1", "1.2", "1.3", "2.1",
    "2.2", "3.1", "3.2", "3.3", "4.1" .. "4.6", "CU"; factories tracker_bb, tracker_11 ...
    tracker_46, tracker_cu (step=None, extra=False). extra: False | True (' · extra') | "local
    stand-in" | "Docker's analogue" (' · extra · …') | "gcloud" (' · gcloud alternative') |
    "gcloud · local stand-in" | any other str (appended verbatim after ' · ').
    track(tr, k, extra) ANIM (caption cross-fades; k=None keeps the step) ·
    swap_tracker(scene, old, new) PLAYS (one subsection to the next) · lref(slides) lecture tag.

Captures (assets/terminal/<folder>/NN-*.txt; folders laptop, dev, gcloud, dev/provider-timeout)
    c = capture("laptop/10")  (or capture("10") for laptop/, capture("dev/provider-timeout/28"))
    c.cmd_lines  the typed lines (line 1 without '$ '; a multi-line command keeps its own rows)
    c.cmd        the same joined with '\\n'     c.k  how many file lines the command takes
    c.at(*spec)  output lines by FILE line numbers: ints, (a, b) ranges, '…' items; refuses the
                 command lines and the [exit N] line      c.line(n)  one file line
    c.pick(*ranges)  L1-style: 1-based ranges over the OUTPUT body (pick(1) = first output line)
    c.lines (output body) c.exit c.raw c.path
    type_capture(scene, t, c, type_time=None) PLAYS: types c's command lines exactly as captured
        (a row after a trailing '\\' continues without a prompt; separate commands get the prompt)
    recorded(file, *nums) -> list[str]: lines of assets/terminal/expected/<file> (the bracketed
        source column dropped)   recorded_card(file, nums, source) -> card + 'recorded · source' tag
    task_log_lines() -> the JSON shape of expected/part4-task-log-shape.txt (an illustration)

Sources (assets/source at 46cc62f; header 'path · lines a–b')
    code(path, a, b=None, focus=, font_size=22, cuts={line: 'cut after'}) CODE() panel, <= 12
        lines, must fit the frame (22 pt ~66 chars a line, 20 pt ~74: main.py:12 needs 20 pt);
        .code .header; highlight with code_span(p.code, k, "sub") / line_bar(p.code, k, colour), k = file line - a.
    excerpt(path, a, b) / source_text(path) / readme(n) (README line n, stripped)
    readme_card(lines, body, quote=False) GREY card 'README.md · lines a–b' + the README's words.

Terminals (house: 12.6 wide, 22 pt = 65 chars a row; 20 pt = 72)
    term(prompt, rows, title) · laptop_term / dev_term / gcloud_term / tab_term(rows=3)
    resize(scene, t, rows) PLAYS · room · bare_prompt · type_cmd(scene, t, cmd) · out(scene, t, lines,
    wrap=) · cd_prompt(scene, t, prompt) · beside / pin / unpin / on_bar for tags at a row ·
    row_tag, turn_row, extra_row(kind), time_row, cost_row (tags sized for a terminal row) ·
    no_panel_chip() (GREY 'needs your project · no output shown').

Tags and chips (GREY unless said)
    your_turn() YELLOW · extra_tag(kind=None) ('extra · local stand-in' / "extra · Docker's
    analogue" / 'extra · or write your own') · standin_tag() · analogue_tag() · illustration_tag() ·
    recorded_tag(source) ('recorded · function GIF') · recording_tag() 'at the time of recording' ·
    erratum_tag() · cost_tag(text) GOLD (no money amounts: raises) · grey_chip · dashed_chip ·
    tool_chip PURPLE · err_chip RED · ok_chip GREEN · differ_chip 'yours will differ' ·
    file_card(path) · card(lines, head=) · question_card(text) YELLOW · ponder(scene, q, seconds)
    PLAYS (opaque pause_and_ponder card; FadeOut it at the next block) · flash_tag(scene, tg).

Glyphs (text-free unless named; sizes in scene units)
    rack(h) solid BLUE VM · instance(box_w, box_h, inner=True) dashed BLUE + TEAL inner box ·
    image_block(name, box_w) TEAL · puff() cold-start puff · ear(port_text) PINK ear + label ·
    envelope(text, color) · badge(name, color, dashed) BLUE service-account badge · ticket() ·
    key_glyph() / crossed_key() GOLD dashed key with a RED cross · bucket(name, box_w) BLUE ·
    folder_icon() · file_icon(name) · receipt() GREEN ribbon · disk() · you(text) GREY person ·
    bolt() lightning · cloud_shape(text, color) · region_pin(text, dashed) · worksheet_card(name,
    kind) BLUE · worksheet_strip() · check_glyph / cross_glyph · arrow / route / travel / bounce ·
    ring / under / strike / hl_bar · grid_icon(cell) V1 icon (text-free 2x2) · meter_icon().

Console (CONSOLE beats; tag them with illustration_tag())
    f = console_form(title, rows, form_w=8.6)  rows: ("Label", "value") | ("button", "Create") |
        ("check", "Execute job immediately", False) | ("radio", "Deploy one revision …", True) |
        ("note", "leave the image's command and arguments unchanged") | ("path", "Cloud Run → Services")
    f.rows[i] has .label .field .value (fields) / .box .text (buttons) · f.fill(i, value) ANIM (the
    value types in) · f.press(i) ANIM (a button pulses) · f.title_text. Values: README text only.
    chip_row(values, max_w=11.6, size=20) WHITE-outlined argument chips, gs:// values PINK and the
        bucket placeholders YELLOW; wraps into rows; .chips (list).

Set pieces (V numbers = BRIEF)
    V1 DeployGrid(built=True, sketch=False)   the lecture's 2x2. Layout: sketch card x -6.45..-3.65,
        row headers -3.45..-1.25, cells (2.6 x 1.5) at x 0.25 / 3.15, rows y 1.2 / -0.45, column
        headers y 2.45, part chips from y -1.45 down, 'today' chip right of row 1 (to x 6.5).
        built=False starts with the sketch only (S02). PLAYS: fan(scene) arrows fan out from the
        sketch and the four cells appear · headers(scene, which="cols"|"rows") · tick_vm(scene) L1/L2
        ticks · today(scene) · parts(scene) the README's four parts as chips · open_lid(scene) TEAL
        box in the file cell + 'Google built one' · split_job(scene) container cell -> service | job ·
        cons(scene) three RED con cards (drops the part chips) · answer(scene, i, text) GREEN chip
        under con i. ANIM: light(r, c, colour) / unlight(r, c) / pulse_part(i). .cells[r][c] .sketch
    V2 InstanceStrip(rows=("vm", "serverless"), axis_w=8.4, times=("evening", "night", "morning"))
        time axis per row from x -3.0 to 5.4 (label + glyph on the left), rows 2.0 apart. .x(t)
        PLAYS: pulses(scene, row, ts) · vm_run(scene) solid bar + constant GOLD meter · idle(scene,
        spans) GOLD shading 'idle, still billed' · serve(scene, t0, t1, pulses, lane=0,
        billing="request"|"instance", cold=True) a dashed instance lives t0..t1, the meter moves under
        the pulses only (request) or the whole life (instance) · always_on(scene) min instances 1:
        a faint instance over the whole axis with its own GOLD drip · instance_billing(scene, on)
        every meter of the row covers whole lives (or back).
    V2 SlotPool(max_instances=2, slots=4)  S08's slots view: dashed instances with 4 thread slots.
        PLAYS: line_up(scene, n, text) PINK request dots at the left · spawn(scene) · fill(scene)
        dots fly into free slots, spawning up to max, returns the dots left over · ceiling(scene)
        YELLOW 'max = 2' · queue(scene, dots) GREY waiting box · refuse(scene, dot) · counter(scene,
        text) · dissolve(scene) (scale to zero).
    Slider(text, values=(0, 1)) .to(v) ANIM · Switch(text, on=True) .flip(on) ANIM (public access,
        request/instance-based).
    V3 BuildLine(entry=ENTRY)  inputs x -5.4 (main.py, requirements.txt, entry tag) -> PURPLE Cloud
        Build x -2.2 -> BLUE Artifact Registry shelf x 1.2 -> dashed revision x 4.6, around y 0.
        PLAYS: feed(scene) · stamp(scene, text) · publish(scene) TEAL image onto the shelf ·
        start(scene) the revision starts · lookup(scene) the entry name reaches into main.py (GREEN
        tick, or RED snap + 'revision not ready' when entry != hello_http) · set_entry(scene, name) ·
        skip_build(scene) GREY-dashed build + 'no build this time' · shelf_tag(scene, text) GOLD.
        registry_shelf(with_image=True) the shelf alone (S16).
    V3 FunctionInside()  the zoom: dashed revision > PURPLE functions-framework > Flask app >
        gunicorn with a PINK ear '0.0.0.0:$PORT'; a GREEN main.py card (lines 7-8). PLAYS:
        request(scene) · lookup(scene, name) (answer flows back, or RED 'no such def').
    V4 QueryToArgs(url=FUNCTION_URL, query=QUERY)  base URL row + PINK query row (mono 24).
        PLAYS: type_query(scene) · split(scene) at '?' and '&' into three pairs (rows at the left) ·
        melt(scene) '%20' -> spaces · into(scene, panel) pairs fly into a code(main.py, 9, 12) panel,
        each default greys · join(scene) the pairs join back into one query string ·
        provider(scene, src) ORANGE hop to googletrans' public endpoint and back.
        defaults(panel) ANIM: with no query string the three defaults light.
    V5 CommandSlots(slot_w=8.8)  TEAL image block with ENTRYPOINT: [] / CMD: [python -m
        translation_demo serve] (laptop/16:11-12); used in S07 and S13/S15 (V7 command vs args).
        PLAYS: ghost_args(scene) · set_command(scene, "python") · clear_cmd(scene) · add_args(scene,
        values=ARGS, lag) · conveyor(scene) one argv row · one_chip(scene) the fat chip ·
        no_command(scene) '-m' becomes the program (RED) · swap_args(scene, values, hi=) ·
        reset(scene). .entry_slot .cmd_slot .arg_chips
    V5 PortEnvelope()  TEAL container (5.0 x 2.8) with a PURPLE process box; wall + door on the left.
        PLAYS: start(scene) 'python' · execvp(scene) -> 'gunicorn' (same box) · envelope(scene,
        port="8080", writer="image"|"cloud"|"you") + PINK ear '0.0.0.0:<port>' · threads(scene, 4) ·
        wall(scene, host="8086", target="8080") laptop wall, PINK door, pipe · knock(scene, port, ok)
        · move_ear(scene, "9090") · repipe(scene) · sigint(scene).
    V6 IdentityDoors(name=SERVICE)  browser x -5.6, BLUE service box (4.6 x 3.0) at x -0.7 with two
        doors, Agent Platform cloud x 5.2; switch 'Allow public access' under the left door.
        PLAYS: call(scene, allowed=True) · set_public(scene, on) · call_out(scene, ok) ·
        default_badge(scene) · add_badge(scene) · pin_badge(scene) · roles(scene, *texts) ·
        no_key(scene) · you(scene, text) · token(scene) · revision(scene, text).
    V6 ImpersonationRibbon()  you + 'your Google account' (left), laptop disk (bottom left), the
        runtime badge (right). PLAYS: sign_in · ribbon · tickets(n) · adc_file · empty_slot · no_key.
    V6 BadgeBoard()  web badge (top) + job badge (bottom) with ORANGE project roles, input / output
        buckets on the right. PLAYS: job_badge(scene) · grant(scene, "input"|"output") ·
        web_note(scene, text).
    V7 LifecycleStrips()  TEAL image block with 'serve' / 'batch' (top left), service strip y 0.9,
        job strip y -0.9 (x -3.0 .. 6.0). PLAYS: serve(scene) · run_job(scene, fail_at=None) ·
        set_exit(scene, code) · endless(scene) the job that never finishes hits 'task timeout 5 min'
        · buckets(scene) · disk_gone(scene).
    V8 AttemptFolders(prefix="run-001/")  BLUE output bucket (9.6 x 4.2) with a prefix tab.
        PLAYS: attempt(scene, name) a folder drops in · files(scene, i=-1, fail_after=None) text and
        audio with GREEN 'create only' stamps, manifest last + receipt (or RED 'not a success') ·
        shield(scene, i) · prefix(scene, text) · flash_receipt(scene, i).
    WhereToLook()  the three-slot 'where do you look?' card. PLAYS: fill(scene, i, text) ·
        glow(i) ANIM.
    TranslatePage(url="localhost:8086", url_color=ROUTE, speech=False)  the drawn page of laptop/11
        (illustration). PLAYS: type_in(scene, text) · set_dest(scene, code) · translate(scene,
        answer) · enable_speech(scene). ANIM: press(button) (button = "translate" | "audio").

Capture folder names: assets/terminal/laptop (Docker engine, the app), dev (Debian 12 + uv: the
function stand-in and Part 3.3), dev/provider-timeout (the recorded 500), gcloud (no account: every
gcloud box to its first honest error), expected (RECORDED quotes and the task-log shape);
capture-only/ folders are plumbing and refused.
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import yaml
from manim import (DL, DOWN, DR, LEFT, ORIGIN, PI, RIGHT, UL, UP, UR, AnimationGroup, Arc, Arrow,
                   Circle, Create, DashedLine, DashedVMobject, Dot, FadeIn, FadeOut, GrowArrow,
                   GrowFromCenter, Indicate, LaggedStart, Line, MoveAlongPath, Polygon, Rectangle,
                   RoundedRectangle, Rotate, ShowIncreasingSubsets, Succession, Text, Transform,
                   UpdateFromAlphaFunc, VGroup, VMobject, linear, there_and_back)

from explainer import style as S
from explainer.components import pause_and_ponder, person_icon, ponder_card  # noqa: F401 (re-export)
from explainer.devops import (CAPTION, LABEL, MONO, OUTPUT, PANEL, SMALL, TAG, TERM_BG,  # noqa: F401
                              ReadmeTracker, Terminal, box, browser_window, cell_width, chip, code_block,
                              code_panel, code_span, file_glyph, folder_glyph, glyph_range, label,
                              lecture_ref, line_bar, line_pitch, mono, mono_line, server, substring, tag)
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
# SAY lines per scene (script.md v2, review merge 2026-11-04); every scene asserts its own count
SAY_COUNT = {"S01": 7, "S02": 8, "S03": 8, "S04": 10, "S05": 9, "S06": 11, "S07": 13, "S08": 13,
             "S09": 9, "S10": 9, "S11": 9, "S12": 8, "S13": 13, "S14": 11, "S15": 7, "S16": 14}

# ------------------------------------------------------------------ semantic colours (BRIEF.md)
LAPTOP = S.GREY          # your laptop, the browser, "you" the deployer, the local ADC file
YOU = LAPTOP
CLOUD = S.BLUE           # Cloud Run, Cloud Build, Artifact Registry, buckets, Agent Platform, the badges
BADGE = CLOUD
IMAGE = S.TEAL           # the image and its containers, an instance's inner box
CONTAINER = IMAGE
SHARED = S.ORANGE        # project-wide role chips, the default compute account, googletrans' endpoint
SYSTEM = SHARED
OWN = S.GREEN            # what you own and pin: main.py + requirements, hello_http, --frozen, the digest,
PIN = OWN                #   the per-bucket grants; also a pass / a tick
PASS = S.GREEN
TOOL = S.PURPLE          # gcloud, docker, uv, functions-framework, gunicorn, run_job.py
ERR = S.RED              # placeholder rejection, sign-in error, MissingTargetException, 4xx/5xx, exit 1/127
TURN = S.YELLOW          # your turn, the tracker, today's two grid cells, the ponder timer
COST = S.GOLD            # Cloud Build, request-based billing, min instances, TTS, storage, clean-up
ROUTE = S.PINK           # URLs, the query string, ports and -p doors, JSON POSTs, gs:// URIs, argv
PAST = S.GREY            # the past and the future (L1 VM, L2, L3 key, L13 job, L15): dashed
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


STRIP_TOP = strip_top(3)     # -1.44: a picture over a 3-row strip lives in y in [-1.3, 2.8]


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


# ------------------------------------------------------------------ series rule: no names
_NAME_RE = re.compile(r"Pavlos(?:[ _]Protopapas)?|Protopapas", re.IGNORECASE)


def unname(s: str) -> str:
    """s with the instructor's name masked ('‹instructor›'). capture() and source_text() apply it."""
    return _NAME_RE.sub("‹instructor›", s)


# ------------------------------------------------------------------ captures
CAPTURE_FOLDERS = ("laptop", "dev", "gcloud", "dev/provider-timeout")
# commands that take several file lines without ending in '\' (script.md "TERM" conventions)
CMD_LINES = {("laptop", "05"): 8, ("laptop", "16"): 6, ("dev", "10"): 2, ("dev", "24"): 4,
             ("gcloud", "09"): 4, ("gcloud", "18"): 5}


class Capture:
    """One captured command (assets/terminal/<folder>/<file>). .cmd_lines (typed rows) .cmd (joined
    with '\\n') .k (file lines of the command) .lines (output body, no [exit N]) .exit .raw (every
    file line, tabs expanded) .path"""

    def __init__(self, cmd_lines, lines, exit_code, raw, path):
        self.cmd_lines, self.lines, self.exit, self.raw, self.path = cmd_lines, lines, exit_code, raw, path
        self.k = len(cmd_lines)
        self.cmd = "\n".join(cmd_lines)

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
        """Lines by FILE line numbers, as script.md writes them: ints, (a, b) inclusive ranges and
        '…' items (a literal '…' line). at(3, (5, 7), '…', 15). Never adds '…' by itself."""
        out_: list[str] = []
        for r in spec:
            if isinstance(r, str):
                out_.append(r)
                continue
            a, b = (r, r) if isinstance(r, int) else r
            out_ += [self.line(n) for n in range(a, b + 1)]
        return out_

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
    """capture("laptop/10") / capture("10") (= laptop) / capture("dev/22") / capture("gcloud/05") /
    capture("dev/provider-timeout/28"): the one file assets/terminal/<folder>/NN-*.txt. Fails loudly
    when missing: never show an uncaptured output. The command takes lines 1..k: k from CMD_LINES,
    else line 1 plus every row that follows a trailing '\\'."""
    folder, _, stem = name.rpartition("/")
    folder = folder or "laptop"
    if "capture-only" in name:
        raise ValueError("capture-only/ is plumbing (CA bundle builds, stand-in images): never shown")
    if folder not in CAPTURE_FOLDERS:
        raise ValueError(f"capture folder {folder!r}: one of {CAPTURE_FOLDERS}")
    d = TERMINAL / folder
    stem = stem[:-4] if stem.endswith(".txt") else stem
    p = d / f"{stem}.txt"
    if not p.exists():
        hits = sorted(d.glob(f"{stem}-*.txt"))
        if len(hits) != 1:
            raise FileNotFoundError(f"capture {folder}/{stem}: {len(hits)} matches "
                                    f"{[h.name for h in hits]} (see ASSETS.md)")
        p = hits[0]
    with open(p, encoding="utf-8", newline="") as f:
        text = f.read()
    raw = [unname(s.rstrip("\r").expandtabs(8)) for s in text.rstrip("\n").split("\n")]
    if not raw[0].startswith("$ "):
        raise ValueError(f"{p.name}: line 1 is not a '$ …' command")
    key = (folder, p.name.split("-")[0])
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
    return Capture(cmd_lines, body, code_, raw, p)


_SOURCE_COL = re.compile(r"\s+\[[^\[\]]*\]\s*$")


def recorded(file: str, *nums) -> list[str]:
    """Lines of assets/terminal/expected/<file> (name with or without .txt, or its first word:
    'part1' -> part1-function-recorded.txt) by FILE line number (ints or (a, b) ranges), the
    bracketed source column dropped and the line stripped. Line 1 is the file's header: refused."""
    stem = file[:-4] if file.endswith(".txt") else file
    p = EXPECTED / f"{stem}.txt"
    if not p.exists():
        hits = sorted(EXPECTED.glob(f"{stem}-*.txt"))
        if len(hits) > 1:
            hits = [h for h in hits if h.name.endswith("-recorded.txt")]
        if len(hits) != 1:
            raise FileNotFoundError(f"expected/{stem}: {[h.name for h in hits]}")
        p = hits[0]
    raw = p.read_text(encoding="utf-8").rstrip("\n").split("\n")
    out_ = []
    for r in nums:
        a, b = (r, r) if isinstance(r, int) else r
        for n in range(a, b + 1):
            if n == 1:
                raise ValueError(f"{p.name}:1 is the provenance header, never shown")
            out_.append(unname(_SOURCE_COL.sub("", raw[n - 1]).strip()))
    return out_


def task_log_lines() -> list[str]:
    """The JSON shape of expected/part4-task-log-shape.txt, lines 2-12 (an ILLUSTRATION: tag it so)."""
    raw = (EXPECTED / "part4-task-log-shape.txt").read_text(encoding="utf-8").rstrip("\n").split("\n")
    return raw[1:12]


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
P_HOME = "student@laptop:~$"
P_REPO = "student@laptop:~/serverless-deployment$"
P_APP = "student@laptop:~/serverless-deployment/tutorial/app$"
P_FUNC = "student@laptop:~/serverless-deployment/tutorial/function$"
P_LAPTOP = P_REPO
T_LAPTOP = "laptop"
T_DEV = "laptop · dev shell"
T_GCLOUD = "laptop · gcloud"
T_TAB = "laptop · second tab"

_exports = capture("laptop/05")
IMAGE_REF = _exports.cmd_lines[2].split("=", 1)[1]          # the public image, verbatim (README:248)
IMAGE_TAG = ":" + IMAGE_REF.split(":", 1)[1]
WEB_EMAIL, JOB_EMAIL = _exports.line(9), _exports.line(10)   # as the echo printed them
DIGEST = capture("laptop/10").line(16).split("Digest: ", 1)[1]   # = README:1069


def digest_short(head: int = 12, tail: int = 6) -> str:
    """'sha256:c17b6db09f74…dbe72e' (head hex digits, '…', tail hex digits)."""
    h = DIGEST.split(":", 1)[1]
    return f"sha256:{h[:head]}…{h[-tail:]}"


DIGEST_SHORT = digest_short()
FUNCTION, SERVICE, JOB = "translate-function", "translation-demo", "translation-audio"
RUNTIME_SA, JOB_SA = "translation-demo-runtime", "translation-audio-job"
ENTRY = "hello_http"
PROJECT_PH = "YOUR_PROJECT_ID"
STANDIN_PROJECT = "your-project-id"            # gcloud/18-20 only, tagged extra
IN_BUCKET, OUT_BUCKET = "YOUR_INPUT_BUCKET", "YOUR_OUTPUT_BUCKET"
DEV_EMAIL = "YOUR_GOOGLE_ACCOUNT_EMAIL"
REGION, REGION_CITY, SPEECH_LOCATION = "northamerica-northeast2", "Toronto", "us-central1"
FUNCTION_URL = "https://translate-function-…run.app"     # drawn elided, tag illustration
SERVICE_URL = "https://translation-demo-…run.app"
TTS_MODEL = "gemini-2.5-flash-tts"
EXEC_ID = "translation-audio-hq9f5"            # README:859
ATTEMPT = "de2f41…"                            # README:860
JOB_STEPS = ("take input", "translate", "speak", "save")      # __main__.py:52-57
WORKSHEET = (("function", FUNCTION), ("web service", SERVICE), ("web account", RUNTIME_SA),
             ("job", JOB), ("job account", JOB_SA))           # README:46-55 (+ two bucket names)
LOCAL_URL = "localhost:8086"


# ------------------------------------------------------------------ sources
def _src(path: str) -> Path:
    p = SOURCE / path
    if p.exists() and p.is_file():
        return p
    raise FileNotFoundError(f"assets/source/{path}")


def source_text(path: str) -> str:
    """An assets/source file ('README.md', 'tutorial/function/main.py', 'at-4eaf343/README.md' …)."""
    return unname(_src(path).read_text(encoding="utf-8"))


def excerpt(path: str, first: int, last: int) -> str:
    """Lines first..last (1-based, inclusive) of assets/source/<path>."""
    return "\n".join(source_text(path).split("\n")[first - 1:last])


def readme(n: int, path: str = "README.md") -> str:
    """README.md line n (1-based), stripped. A README command often sits in a fence or in prose:
    compare with `in`, e.g. capture("laptop/10").cmd_lines[0] in readme(246)."""
    return excerpt(path, n, n).strip()


QUERY = readme(163)                                        # ?text=Good%20afternoon%20everyone&src=en&dest=fr
ARGS = tuple(readme(n) for n in range(755, 766))           # the eleven argument chips
assert QUERY.startswith("?text=") and ARGS[0] == "-m" and len(ARGS) == 11, (QUERY, ARGS)


def _elide_gs(v: str) -> str:
    if not v.startswith("gs://"):
        return v
    rest = v[5:].split("/", 1)[1]
    return "gs://…/" + (rest.split("/", 1)[1] if rest.count("/") >= 1 and rest.endswith(".txt") else rest)


ARGS_SHORT = tuple(_elide_gs(v) for v in ARGS)             # gs://…/passage.txt , gs://…/run-001/

_LANG = {".py": "python", ".toml": "toml", ".sh": "bash", ".md": "markdown", ".yaml": "yaml",
         ".yml": "yaml", ".txt": "text", ".json": "json", ".lock": "toml", ".html": "html"}


def _lang(name: str) -> str:
    if name.startswith("Dockerfile"):
        return "docker"
    if name == "requirements.txt":
        return "text"
    return _LANG.get(Path(name).suffix, "text")


def code(path: str, first: int, last: int | None = None, language: str | None = None, focus=None,
         font_size: float = 22, shown: str | None = None, max_lines: int = 12, cuts: dict | None = None,
         dedent: bool = False):
    """CODE(path: first–last) of script.md: a code_panel quoting assets/source/<path>, header
    '<path> · lines a–b'. <= 12 lines. The panel must fit the frame (22 pt holds ~66 characters a
    line, 20 pt ~74: main.py:12 needs font_size=20); a wider panel raises: cut a line with cuts={file_line: 'text it ends after'} (the house '…', GREY) or use
    font_size=20. .code .header; highlight with code_span(p.code, k, "x") / line_bar(p.code, k,
    colour), k = file line - first. dedent=True removes the common leading indentation."""
    last = first if last is None else last
    if last - first + 1 > max_lines:
        raise ValueError(f"CODE {path}: {last - first + 1} lines; never more than {max_lines} on screen")
    text = excerpt(path, first, last)
    if dedent:
        import textwrap
        text = textwrap.dedent(text)
    lines = text.split("\n")
    cuts = cuts or {}
    for n, after in cuts.items():
        lines[n - first] = cut(lines[n - first], after)
    language = language or _lang(Path(path).name)
    p = code_panel("\n".join(lines), shown or path, first, language, focus=focus, font_size=font_size)
    if p.width > 2 * SAFE_X - 0.1:
        longest = max(range(len(lines)), key=lambda i: len(lines[i].expandtabs(4)))
        raise ValueError(f"CODE {path}: {p.width:.2f} wide at {font_size} pt leaves the frame (line "
                         f"{first + longest}, {len(lines[longest])} characters): cuts={{{first + longest}: "
                         f"'...'}} or font_size=20 (main.py:12, 74 characters, fits at 20 pt)")
    for n in cuts:
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


# ------------------------------------------------------------------ trackers (script.md, sixteen)
SECTIONS = {
    "BB": "Before you begin",
    "1.1": "1.1 Create the function",
    "1.2": "1.2 Supply the code",
    "1.3": "1.3 Call the endpoint",
    "2.1": "2.1 Try it locally",
    "2.2": "2.2 Deploy the same image",
    "3.1": "3.1 API and identity",
    "3.2": "3.2 Attach and speak",
    "3.3": "3.3 Develop locally · optional",
    "4.1": "4.1 Two buckets",
    "4.2": "4.2 Job identity",
    "4.3": "4.3 Create the job",
    "4.4": "4.4 Execute, collect",
    "4.5": "4.5 From the terminal",
    "4.6": "4.6 The helper",
    "CU": "Clean up",
}
STEPS = {
    "BB": ["Select project", "Billing, permissions", "Choose region", "Clone repo", "Terminal setup"],
    "1.1": ["Write a function", "Enable APIs", "Name, region", "Python 3.12", "Public access", "Source editor"],
    "1.2": ["Replace main.py", "Replace requirements", "Entry point", "Save and redeploy"],
    "1.3": ["Copy URL", "Default call", "Query string", "Other languages", "Check logs"],
    "2.1": ["docker run", "Open localhost", "Translate", "Ctrl+C"],
    "2.2": ["Deploy container", "Image URL", "Name, region", "Public, request-based", "Scaling 0–2",
            "Container settings", "Request settings", "Create", "Open URL", "Revisions, logs"],
    "3.1": ["Enable API", "Create account", "Name and ID", "Two roles", "Record email"],
    "3.2": ["Open service", "Security tab", "Three variables", "View diff", "Wait rollout", "Play audio",
            "Read logs"],
    "3.3": ["Token Creator", "ADC login", "uv sync", "Run serve", "cd ../.."],
    "4.1": ["Create bucket", "Unique name", "Wizard settings", "Output bucket", "Upload passage", "Copy URI"],
    "4.2": ["Create account", "Project roles", "Input: Viewer", "Output: Creator", "Web unchanged"],
    "4.3": ["Deploy container", "Same image", "Name, 1 task", "Command python", "Eleven arguments",
            "Three variables", "Timeout, retries", "Service account", "Create"],
    "4.4": ["Execute", "View logs", "Attempt folder", "Three files", "Download"],
    "4.5": ["Bucket variables", "Upload passage", "Execute overrides", "Download results"],
    "4.6": ["Run helper", "Open results"],
    "CU": ["Download results", "Delete services, job", "Buckets, accounts", "Function image"],
}
TRACKER_KEYS = tuple(SECTIONS)
EXTRA_KINDS = ("local stand-in", "Docker's analogue")


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
    if extra == "gcloud":
        return " · gcloud alternative"
    if extra == "gcloud · local stand-in":
        return " · gcloud alternative · extra · local stand-in"
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
    """Tracker `key` (TRACKER_KEYS) at `step` (1-based; None = no step lit yet), placed top-left:
    'README › <section>', one dot per step, 'step k of N: <step>' + the extra suffix (GREY)."""
    tr = ReadmeTracker(SECTIONS[key], STEPS[key])
    tr.key = key
    if step:
        tr.set_step(step)
    tr.remove(tr.caption)
    tr.caption = _caption(tr, step or 0, extra)
    tr.extra = extra
    tr.add(tr.caption)
    return place_tracker(tr)


def _tracker_factory(key):
    def make(step=None, extra=False):
        return tracker(key, step, extra)
    make.__name__ = "tracker_" + key.lower().replace(".", "")
    make.__doc__ = f"tracker('{key}', step, extra): README › {SECTIONS[key]}"
    return make


tracker_bb, tracker_11, tracker_12, tracker_13, tracker_21, tracker_22, tracker_31, tracker_32, \
    tracker_33, tracker_41, tracker_42, tracker_43, tracker_44, tracker_45, tracker_46, tracker_cu = \
    map(_tracker_factory, TRACKER_KEYS)


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


def swap_tracker(scene, old: ReadmeTracker, new: ReadmeTracker, *anims, run_time: float = 0.6):
    """PLAYS: tracker `old` becomes `new` in place (section name and caption cross-fade, the dots
    regroup). `new` ends on the scene as one piece; `old` is gone."""
    from manim import FadeTransform, ReplacementTransform
    keep = VGroup(old.head[0], old.head[1])          # 'README ›' stays put
    scene.remove(old)
    olds = [old.head[2], old.dots, old.caption]
    scene.add(*keep, *olds)
    moves = [FadeTransform(old.head[2], new.head[2]), ReplacementTransform(old.dots, new.dots),
             FadeTransform(old.caption, new.caption)]
    scene.play(*moves, *anims, run_time=run_time)
    scene.remove(*keep, *new.head, new.dots, new.caption, *olds)
    scene.add(new)
    return new


def lref(slides: str) -> VGroup:
    """The GREY 'Lecture 14 · slides 10–11' tag, top right (one per beat; script.md LECTURE 14 · …)."""
    return lecture_ref(14, slides)


# ------------------------------------------------------------------ terminals
def term(prompt: str = P_REPO, rows: int = 10, title: str | None = T_LAPTOP, width: float = 12.6,
         size: float = 22, place: bool = True) -> Terminal:
    """The house terminal: 12.6 wide, 22 pt, 65 characters a row, centred, bottom edge at BOTTOM.
    Height = rows x 0.403 + 0.85. Full width, or a 3-row strip (rows=3) under a picture. size=20
    gives 72 characters a row."""
    t = Terminal(prompt=prompt, width=width, rows=rows, size=size, title=title)
    if place:
        t.shift(np.array([-t.box.get_center()[0], BOTTOM - t.box.get_bottom()[1], 0]))
    return t


def laptop_term(rows: int = 10, prompt: str = P_REPO) -> Terminal:
    """Title 'laptop' (laptop/ captures)."""
    return term(prompt, rows, T_LAPTOP)


def dev_term(rows: int = 10, prompt: str = P_REPO) -> Terminal:
    """Title 'laptop · dev shell' (dev/ captures: the function stand-in, Part 3.3)."""
    return term(prompt, rows, T_DEV)


def gcloud_term(rows: int = 10, prompt: str = P_REPO) -> Terminal:
    """Title 'laptop · gcloud' (gcloud/ captures and every README gcloud box)."""
    return term(prompt, rows, T_GCLOUD)


def tab_term(rows: int = 3, prompt: str = P_REPO) -> Terminal:
    """Title 'laptop · second tab': the strip for extras while a server holds the foreground."""
    return term(prompt, rows, T_TAB)


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
    """ANIM: the terminal's title changes in place (e.g. 'laptop' -> 'laptop · gcloud')."""
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


def type_capture(scene, t: Terminal, cap, type_time: float | None = None) -> list:
    """PLAYS: type a capture's command exactly as its file lines spell it (cap: a Capture or a
    capture name). A row that follows a trailing '\\' is a continuation (no prompt); every other row
    is a separate command at the prompt (laptop/05's exports). type_time: per row. Returns the list
    of typed lines (each a line or a folded VGroup)."""
    cap = capture(cap) if isinstance(cap, str) else cap
    out_, cont = [], False
    for row in cap.cmd_lines:
        out_.append(type_cmd(scene, t, row, type_time, prompt=not cont))
        cont = row.rstrip().endswith("\\")
    return out_


def type_lines(scene, t: Terminal, rows, type_time: float | None = None) -> list:
    """PLAYS: type a README command block given as its rows (verbatim, ' \\' continuations kept):
    the same continuation rule as type_capture(). For the gcloud boxes with no output panel."""
    out_, cont = [], False
    for row in rows:
        out_.append(type_cmd(scene, t, row, type_time, prompt=not cont))
        cont = row.rstrip().endswith("\\")
    return out_


def readme_rows(a: int, b: int) -> list[str]:
    """README lines a..b as command rows (verbatim, right-stripped; blank rows dropped) for
    type_lines(): e.g. readme_rows(195, 198) is the Part 1 deploy box."""
    rows = [s.rstrip() for s in excerpt("README.md", a, b).split("\n")]
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
    scene.play(Indicate(substring(ln, path), color=color, scale_factor=1.04), run_time=run_time)
    scene.add(ln)
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
    """'extra' sized for a terminal row (GREY); kind 'local stand-in' -> 'extra · local stand-in'."""
    return row_tag("extra" + (f" · {kind}" if kind else ""), S.GREY)


def time_row() -> VGroup:
    """'at the time of recording' sized for a terminal row (GREY)."""
    return row_tag("at the time of recording", S.GREY)


def cost_row(s: str) -> VGroup:
    """A GOLD cost tag sized for a terminal row (never an amount: see cost_tag())."""
    return row_tag(_no_amount(s), COST)


def no_panel_chip(s: str = "needs your project · no output shown") -> VGroup:
    """The GREY chip under a gcloud box typed with no output panel (script.md conventions)."""
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
    """Cost text never carries a money amount or a free-tier figure."""
    if _AMOUNT_RE.search(s):
        raise ValueError(f"cost tag {s!r}: no prices or free-tier figures on screen ('check the pricing page')")
    return s


def your_turn() -> VGroup:
    """YELLOW '▶ your turn' tag (house size: beside a card or panel, not inside a terminal row)."""
    return tag("▶ your turn", TURN)


def extra_tag(kind: str | None = None) -> VGroup:
    """GREY 'extra' tag; kind 'local stand-in' / "Docker's analogue" / 'or write your own' ->
    'extra · local stand-in' …"""
    return tag("extra" + (f" · {kind}" if kind else ""), S.GREY)


def standin_tag() -> VGroup:
    """'extra · local stand-in': the function stand-in (dev/20-29, provider-timeout)."""
    return extra_tag("local stand-in")


def analogue_tag() -> VGroup:
    """"extra · Docker's analogue": laptop/45 (never called Cloud Run's error)."""
    return extra_tag("Docker's analogue")


def illustration_tag(s: str = "illustration") -> VGroup:
    """On every CONSOLE form, the drawn page, the classmate laptop, the V-pictures of cloud machinery
    and the task-log shape (schematic; never a screenshot)."""
    return tag(s, S.GREY)


def recorded_tag(source: str | None = None) -> VGroup:
    """'recorded · function GIF' / 'recorded · README:182-183': every cloud success (expected/)."""
    return tag("recorded" + (f" · {source}" if source else ""), S.GREY)


def recording_tag(s: str = "at the time of recording") -> VGroup:
    """Beside versions on first show."""
    return tag(s, S.GREY)


def erratum_tag(s: str = "erratum") -> VGroup:
    """On every README/slide slip (the narration says 'a small note' or 'a small gap')."""
    return tag(s, S.GREY)


def cost_tag(s: str) -> VGroup:
    """The GOLD money tag: what bills + 'check the pricing page'. Raises on '$', 'cents', 'free tier'."""
    return tag(_no_amount(s), COST)


def grey_chip(s: str, size: float = 20, mono_font: bool = False, color=S.GREY) -> VGroup:
    """A GREY chip for a short note. .box .text"""
    return chip(s, color, size=size, font=MONO if mono_font else None)


def dashed_chip(s: str, color=PAST, size: float = 20, mono_font: bool = False) -> VGroup:
    """A dashed chip: past/future things (L1, L2, L3 key, L13 job, L15). .box .text"""
    t = mono(s, size, color) if mono_font else label(s, size, color)
    ob = outline_box(t.width + 0.48, mono("|", size).height + 0.24, color, solid=False)
    t.move_to(ob)
    g = VGroup(ob, t)
    g.box, g.text = ob, t
    return g


def tool_chip(s: str, size: float = 20) -> VGroup:
    """A tool as a PURPLE mono chip (never a logo): gcloud, docker, uv, functions-framework …"""
    return chip(s, TOOL, size=size, font=MONO)


def err_chip(s: str, size: float = 20, mono_font: bool = True) -> VGroup:
    """A RED error chip: err_chip('403'), err_chip('exit 127'). .box .text"""
    return chip(s, ERR, size=size, font=MONO if mono_font else None, fill_opacity=0.14)


def ok_chip(s: str, size: float = 20, mono_font: bool = False) -> VGroup:
    """A GREEN chip (a pin you own, a pass, an answer). .box .text"""
    return chip(s, OWN, size=size, font=MONO if mono_font else None)


def differ_chip(s: str = "yours will differ") -> VGroup:
    """GREY chip for run ids, container ids, timestamps (never read aloud)."""
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
    """A YELLOW-outlined question card ('Can this page have a public URL …', the parked question,
    'Test yourself'); '\\n' breaks rows. .frame .body"""
    rows = VGroup(*[label(s, size, INK) for s in text.split("\n")]).arrange(DOWN, buff=0.14)
    w = card_w or rows.width + 0.8
    frame = RoundedRectangle(width=w, height=rows.height + 0.6, corner_radius=0.16, stroke_color=color,
                             stroke_width=3).set_fill(S.BG, 1)
    rows.move_to(frame)
    g = VGroup(frame, rows)
    g.frame, g.body = frame, rows
    return g


def recorded_card(file: str, nums, source: str, size: float = 22, card_w: float | None = None,
                  color=INK) -> VGroup:
    """RECORDED(expected/<file>: nums): a GREY-outlined panel quoting those lines (source column
    dropped), with the tag 'recorded · <source>' on its top edge (right). nums: an int, a range
    tuple, or a list of them. Long lines wrap at 60 characters. .frame .body .tag"""
    nums = [nums] if isinstance(nums, (int, tuple)) else list(nums)
    lines = soft(recorded(file, *nums), 60)
    body = VGroup(*[label(s, size, color) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    w = card_w or body.width + 0.7
    frame = box(w, body.height + 0.6, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
    body.move_to(frame).align_to(frame, LEFT).shift(RIGHT * 0.35 + DOWN * 0.05)
    tg = recorded_tag(source)
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


def rack(h: float = 1.0, color=CLOUD, units: int = 3) -> VGroup:
    """A VM: a SOLID rack (BLUE)."""
    return server(height=h, units=units, color=color)


def instance(box_w: float = 1.2, box_h: float = 0.75, color=CLOUD, inner: bool = True, dashed: bool = True,
             inner_color=IMAGE) -> VGroup:
    """A serverless instance: a DASHED outline (BLUE) with a TEAL inner box (the container).
    .frame .inner (None when inner=False)"""
    fr = outline_box(box_w, box_h, color, solid=not dashed, fill_opacity=0.08)
    g = VGroup(fr)
    g.frame, g.inner = fr, None
    if inner:
        ib = RoundedRectangle(width=box_w * 0.55, height=box_h * 0.5, corner_radius=0.06,
                              stroke_color=inner_color, stroke_width=2.5).set_fill(inner_color, 0.25)
        ib.move_to(fr)
        g.add(ib)
        g.inner = ib
    return g


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


def puff(r: float = 0.2, color=S.GREY) -> VGroup:
    """The small grey 'cold start' puff (three circles)."""
    cs = VGroup(*[Circle(radius=r * k, stroke_width=0).set_fill(color, 0.55) for k in (0.7, 1.0, 0.8)])
    cs[0].shift(LEFT * r * 0.9)
    cs[2].shift(RIGHT * r * 0.95 + DOWN * r * 0.1)
    return cs


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
        [body.get_corner(UL), body.get_center() + DOWN * 0.05, body.get_corner(UR)])
    t.move_to(body).shift(DOWN * 0.1)
    g = VGroup(body, flap, t)
    g.body, g.flap, g.text = body, flap, t
    return g


def badge(name: str = RUNTIME_SA, color=BADGE, dashed: bool = False, size: float = 20,
          mono_font: bool = True) -> VGroup:
    """A service-account badge: a clip hole on top, the account name inside (BLUE; ORANGE dashed for
    the default compute account). .frame .text"""
    t = (mono if mono_font else label)(name, size, INK)
    w, h = t.width + 0.6, 0.62
    fr = outline_box(w, h, color, solid=not dashed, fill_opacity=0.15, radius=0.1)
    hole = RoundedRectangle(width=0.32, height=0.09, corner_radius=0.04, stroke_color=color,
                            stroke_width=2).move_to(fr.get_top() + DOWN * 0.11)
    t.move_to(fr).shift(DOWN * 0.05)
    g = VGroup(fr, hole, t)
    g.frame, g.text = fr, t
    return g


def ticket(color=CLOUD, w: float = 0.5) -> VGroup:
    """A short-lived token: a small ticket with a notch (never a key)."""
    b = RoundedRectangle(width=w, height=w * 0.5, corner_radius=0.05, stroke_color=color,
                         stroke_width=2.5).set_fill(color, 0.3)
    n = Circle(radius=w * 0.08, stroke_width=0).set_fill(S.BG, 1).move_to(b.get_left())
    return VGroup(b, n)


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


def crossed_key(key_w: float = 0.8) -> VGroup:
    """The dashed GOLD key with a RED cross over it: 'no key file'. .key .cross"""
    k = key_glyph(key_w)
    x = cross_glyph(key_w * 0.7).move_to(k)
    g = VGroup(k, x)
    g.key, g.cross = k, x
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


def receipt(text: str = "complete", color=OWN, size: float = 20) -> VGroup:
    """The GREEN receipt ribbon of manifest.json ('status: complete')."""
    t = label(text, size, color)
    b = Polygon([-t.width / 2 - 0.35, 0.2, 0], [t.width / 2 + 0.2, 0.2, 0], [t.width / 2 + 0.35, 0, 0],
                [t.width / 2 + 0.2, -0.2, 0], [-t.width / 2 - 0.35, -0.2, 0],
                stroke_color=color, stroke_width=2.5).set_fill(S.BG, 1)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
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


def bolt(h: float = 0.6, color=ROUTE) -> VMobject:
    """A lightning bolt (an event trigger)."""
    pts = [[0.1, 0.5], [-0.2, 0.0], [0.05, 0.0], [-0.15, -0.5], [0.25, 0.08], [0.0, 0.08], [0.18, 0.5]]
    m = Polygon(*[[x * h, y * h, 0] for x, y in pts], stroke_color=color, stroke_width=2.5)
    return m.set_fill(color, 0.45)


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


def region_pin(text: str, color=CLOUD, dashed: bool = False, size: float = 20) -> VGroup:
    """A map pin with a label to its right ('northamerica-northeast2 · Toronto'; dashed for the
    speech model's us-central1). .pin .text"""
    head = Circle(radius=0.16, stroke_color=color, stroke_width=3).set_fill(color, 0 if dashed else 0.5)
    tip = Polygon([-0.12, -0.08, 0], [0.12, -0.08, 0], [0, -0.36, 0], stroke_color=color,
                  stroke_width=3).set_fill(color, 0 if dashed else 0.5)
    pin_ = VGroup(tip, head)
    if dashed:
        pin_ = VGroup(*[DashedVMobject(m, num_dashes=10).set_stroke(color, 3) for m in pin_])
    t = mono(text, size, INK).next_to(pin_, RIGHT, buff=0.15)
    g = VGroup(pin_, t)
    g.pin, g.text = pin_, t
    return g


def worksheet_card(name: str | None, kind: str | None = None, color=CLOUD, size: float = 20) -> VGroup:
    """A worksheet name card (BLUE; README:46-55): mono name, small GREY kind above; kind
    'account' adds a badge outline; name None = a blank bucket card 'you choose · part 4'. .box .text"""
    if name is None:
        t = label("you choose · part 4", size, S.GREY)
    else:
        t = mono(name, size, INK)
    parts = [t]
    if kind:
        parts.insert(0, label(kind, size, S.GREY))
    inner = VGroup(*parts).arrange(DOWN, buff=0.06)
    b = outline_box(inner.width + 0.4, inner.height + 0.3, color, solid=name is not None, fill_opacity=0.1)
    inner.move_to(b)
    g = VGroup(b, inner)
    g.box, g.text = b, t
    if kind and "account" in kind:
        hole = RoundedRectangle(width=0.28, height=0.08, corner_radius=0.04, stroke_color=color,
                                stroke_width=2).move_to(b.get_top() + DOWN * 0.07)
        g.add(hole)
    return g


def worksheet_strip(max_w: float = 12.8) -> VGroup:
    """The seven worksheet cards in a row (two rows if needed): the five names + two blank bucket
    cards. .cards (dict: 'function', 'web service', 'web account', 'job', 'job account', 'input',
    'output')"""
    cards = {k: worksheet_card(n, k) for k, n in WORKSHEET}
    cards["input"] = worksheet_card(None, "input bucket")
    cards["output"] = worksheet_card(None, "output bucket")
    rows, cur, w = [], [], 0.0
    for c in cards.values():
        if cur and w + 0.18 + c.width > max_w:
            rows.append(cur)
            cur, w = [], 0.0
        cur.append(c)
        w += (0.18 if len(cur) > 1 else 0) + c.width
    rows.append(cur)
    VGroup(*[VGroup(*r).arrange(RIGHT, buff=0.18) for r in rows]).arrange(DOWN, buff=0.18)
    g = VGroup(*cards.values())
    g.cards = cards
    return g


def grid_icon(cell: float = 0.42, color=CLOUD) -> VGroup:
    """V1's text-free 2x2 icon (corner icon, recap): top row solid (VM), bottom row dashed
    (serverless). .cells[r][c] (light one with icon.cells[1][1].animate.set_stroke(TURN))"""
    cells = []
    for r in range(2):
        row = []
        for c in range(2):
            fr = outline_box(cell, cell * 0.8, color, solid=(r == 0), fill_opacity=0.12, radius=0.05)
            fr.move_to([c * (cell + 0.08), -r * (cell * 0.8 + 0.08), 0])
            row.append(fr)
        cells.append(row)
    g = VGroup(*[m for row in cells for m in row]).move_to(ORIGIN)
    g.cells = cells
    return g


def meter_icon(w: float = 0.9, color=COST) -> VGroup:
    """A text-free GOLD meter (a bar half full in a frame) for recap cards. .fill_bar"""
    fr = RoundedRectangle(width=w, height=0.22, corner_radius=0.06, stroke_color=color, stroke_width=2.5)
    fb = Rectangle(width=w * 0.5, height=0.14, stroke_width=0).set_fill(color, 0.8)
    fb.align_to(fr, LEFT).shift(RIGHT * 0.04)
    g = VGroup(fr, fb)
    g.fill_bar = fb
    return g


# ------------------------------------------------------------------ console form and argument chips
def _field_box(w: float, size: float) -> RoundedRectangle:
    return RoundedRectangle(width=w, height=mono("|", size).height + 0.2, corner_radius=0.06,
                            stroke_color=S.GREY_DARK, stroke_width=1.5).set_fill(TERM_BG, 1)


def console_form(title: str, rows, form_w: float = 8.6, size: float = 20, label_w: float | None = None,
                 path: str | None = None) -> VGroup:
    """A schematic console form (no branding, no logo). title: the page title ('Create service').
    path: an optional breadcrumb above it ('Cloud Run → Services'). rows (README field labels and
    values only):
        ("Service name", "translate-function")       label + field (value '' = an empty field)
        ("button", "Create")                         a button (BLUE outline)
        ("check", "Execute job immediately", False)  a checkbox row
        ("radio", "Deploy one revision from an existing container image", True)
        ("note", "leave the image's command and arguments unchanged")  a GREY note row
    Texts are never scaled: a value wider than its field widens the form (check the frame).
    .rows[i] (.label .field .value for fields; .box .text for buttons; .mark for check/radio)
    .frame .title_text .path_text. fill(i, value) ANIM types a value · press(i) ANIM pulses a button."""
    items = VGroup()
    lw = label_w or max([label(r[0], size).width for r in rows if r[0] not in ("button", "check", "radio",
                                                                               "note", "path")] + [1.5]) + 0.3
    fw = form_w - lw - 0.6
    for r in rows:
        kind = r[0]
        if kind == "button":
            t = label(r[1], size, INK)
            b = RoundedRectangle(width=t.width + 0.5, height=t.height + 0.28, corner_radius=0.08,
                                 stroke_color=CLOUD, stroke_width=2.5).set_fill(CLOUD, 0.15)
            t.move_to(b)
            row = VGroup(b, t)
            row.box, row.text, row.kind = b, t, kind
        elif kind in ("check", "radio"):
            on = r[2] if len(r) > 2 else True
            if kind == "check":
                mk = Rectangle(width=0.26, height=0.26, stroke_color=S.GREY, stroke_width=2).set_fill(S.BG, 1)
                tick = check_glyph(0.22, OWN, 4).move_to(mk)
            else:
                mk = Circle(radius=0.13, stroke_color=S.GREY, stroke_width=2).set_fill(S.BG, 1)
                tick = Dot(radius=0.07, color=CLOUD).move_to(mk)
            tick.set_opacity(1 if on else 0)
            t = label(r[1], size, INK).next_to(mk, RIGHT, buff=0.18)
            row = VGroup(mk, tick, t)
            row.mark, row.tick, row.text, row.kind = mk, tick, t, kind
        elif kind == "note":
            t = label(r[1], size, S.GREY)
            row = VGroup(t)
            row.text, row.kind = t, kind
        else:
            lt = label(kind, size, S.GREY)
            val = r[1] if len(r) > 1 else ""
            vt = mono(val or "|", size, INK)
            w = max(fw, vt.width + 0.4)
            field = _field_box(w, size)
            lt.move_to(ORIGIN, aligned_edge=LEFT)
            field.move_to([lw + w / 2, 0, 0])
            vt.move_to(field).align_to(field, LEFT).shift(RIGHT * 0.15)
            if not val:
                vt.set_opacity(0)
            row = VGroup(lt, field, vt)
            row.label, row.field, row.value, row.kind = lt, field, vt, "field"
        items.add(row)
    items.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
    tt = label(title, 24, INK)
    head = VGroup(tt)
    pt = None
    if path:
        pt = label(path, size, S.GREY)
        head = VGroup(pt, tt).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    body = VGroup(head, items).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    w = max(form_w, body.width + 0.6)
    frame = RoundedRectangle(width=w, height=body.height + 0.6, corner_radius=0.14, stroke_color=S.GREY_DARK,
                             stroke_width=2).set_fill(PANEL, 1)
    body.move_to(frame).align_to(frame, LEFT).shift(RIGHT * 0.3)
    sep = Line(frame.get_left() + RIGHT * 0.15, frame.get_right() + LEFT * 0.15, color=S.GREY_DARK,
               stroke_width=1.5).move_to([frame.get_center()[0], head.get_bottom()[1] - 0.15, 0])
    g = VGroup(frame, sep, head, items)
    g.frame, g.rows, g.title_text, g.path_text = frame, items, tt, pt
    g.size = size

    def fill(i: int, value: str, color=INK, run_time: float = 0.6):
        row = items[i]
        new = mono(value, size, color)
        new.move_to(row.field).align_to(row.field, LEFT).shift(RIGHT * 0.15)
        old = row.value
        row.remove(old)
        row.value = new
        row.add(new)
        return AnimationGroup(FadeOut(old, run_time=0.01),
                              ShowIncreasingSubsets(new, rate_func=linear, run_time=run_time))

    def press(i: int, color=TURN):
        row = items[i]
        return Indicate(row.text if hasattr(row, "text") else row, color=color, scale_factor=1.08)

    g.fill, g.press = fill, press
    return g


def chip_row(values, max_w: float = 11.6, size: float = 20, color=INK, hi=(), buff: float = 0.14,
             placeholders: bool = True) -> VGroup:
    """Argument chips (WHITE outline; gs:// values PINK; with placeholders=True the bucket
    placeholders YOUR_… YELLOW): one chip per value, wrapped into rows no wider than max_w,
    left-aligned. hi: indices drawn YELLOW (S15's run-002 / es). .chips (list) .rows"""
    chips = []
    for i, v in enumerate(values):
        col = TURN if i in hi else (ROUTE if v.startswith("gs://") else color)
        t2c = {}
        if placeholders and v.startswith("gs://"):
            for ph in (IN_BUCKET, OUT_BUCKET):
                if ph in v:
                    t2c[ph] = TURN
        t = mono(v, size, col, t2c=t2c) if t2c else mono(v, size, col)
        h = mono("|", size).height + 0.22
        b = RoundedRectangle(width=t.width + 0.36, height=h, corner_radius=0.08,
                             stroke_color=TURN if i in hi else INK, stroke_width=2).set_fill(S.BG, 1)
        t.move_to(b)
        c = VGroup(b, t)
        c.box, c.text, c.value = b, t, v
        chips.append(c)
    rows, cur, w = [], [], 0.0
    for c in chips:
        if cur and w + buff + c.width > max_w:
            rows.append(cur)
            cur, w = [], 0.0
        cur.append(c)
        w += (buff if len(cur) > 1 else 0) + c.width
    if cur:
        rows.append(cur)
    rg = VGroup(*[VGroup(*r).arrange(RIGHT, buff=buff) for r in rows]).arrange(DOWN, buff=0.14,
                                                                               aligned_edge=LEFT)
    g = VGroup(*chips)
    g.chips, g.rows = chips, rg
    return g


# ------------------------------------------------------------------ set-piece base
class Piece(VGroup):
    """A set piece. PLAYS methods add their new mobjects to the piece after playing them, and take
    parts away with drop(); the piece itself stays one top-level mobject on the scene."""

    def _ensure(self, scene):
        if self not in scene.mobjects:
            scene.add(self)

    def show(self, scene, *mobs, anims=None, run_time: float = 0.6, extra=(), into=None):
        """PLAYS: FadeIn (or `anims`) of new mobjects, then they become parts of the piece (of the
        sub-group `into` when given). Returns the first mobject (or all, as a tuple)."""
        self._ensure(scene)
        a = list(anims) if anims is not None else [FadeIn(m) for m in mobs]
        scene.play(*a, *extra, run_time=run_time)
        scene.remove(*mobs)
        (into if into is not None else self).add(*mobs)
        return mobs[0] if len(mobs) == 1 else mobs

    def _detach(self, m):
        for sub in self.get_family():
            if m in sub.submobjects:
                sub.remove(m)

    def drop(self, scene, *mobs, run_time: float = 0.4, extra=(), shift=None):
        """PLAYS: fade parts of the piece out and take them off it (they never snap back)."""
        mobs = [m for m in mobs if m is not None]
        for m in mobs:
            self._detach(m)
        anims = [FadeOut(m, shift=shift) if shift is not None else FadeOut(m) for m in mobs]
        scene.play(*anims, *extra, run_time=run_time)
        scene.remove(*mobs)

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
        scene.play(Transform(old, new), *extra, run_time=run_time)
        scene.remove(old)
        (parent if parent is not None else self).add(new)
        return new


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


def sketch_card(size: float = 20) -> VGroup:
    """The faded GREEN 'lecture sketch' card of slide 10: 'Simple Translate' and three comment lines
    (never the slide's positional call). .frame .title .lines .head"""
    hd = label("lecture sketch", size, S.GREY)
    ti = label("Simple Translate", 22, OWN)
    lines = VGroup(*[mono(s, size, S.GREY) for s in ("# set up the translator", "# translate",
                                                      "# return the text")]).arrange(DOWN, aligned_edge=LEFT,
                                                                                     buff=0.12)
    inner = VGroup(hd, ti, lines).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    fr = outline_box(inner.width + 0.5, inner.height + 0.45, OWN, solid=True, fill_opacity=0.06)
    fr.frame.set_stroke(opacity=0.6)
    inner.move_to(fr)
    g = VGroup(fr, inner)
    g.frame, g.title, g.lines, g.head = fr, ti, lines, hd
    return g


# ------------------------------------------------------------------ V1 · DeployGrid
class DeployGrid(_Anchored):
    """V1 · the lecture's 2x2 (slide 10): what you hand over (a file / a container) x where it runs
    (a rented machine / serverless). Built centred for the full frame; with sketch=False the sketch
    card is left out (move the grid where you like). built=False (S02) starts with the sketch only:
    then fan(), headers('cols'), headers('rows'), tick_vm(), today(), parts().
    .sketch .cells[r][c] (.frame .glyph) .cols .rows_ .part_chips .con_cards"""

    CX = (1.65, 4.45)
    RY = (1.2, -0.45)
    CELL_W, CELL_H = 2.5, 1.5
    COLH_Y = 2.45
    ROWH_X = -0.95
    SK = (-4.4, 0.4)

    def __init__(self, built: bool = True, sketch: bool = True, size: float = 20, **kw):
        super().__init__(**kw)
        self.size = size
        self.sketch = None
        if sketch:
            self.sketch = sketch_card(size).move_to(self.p(*self.SK))
            self.add(self.sketch)
        self.cells = [[None, None], [None, None]]
        self.cols = self.rows_ = None
        self.marks, self.part_chips, self.con_cards, self.answers = VGroup(), [], [], {}
        self.today_chip = self.lid = self.split = None
        if built:
            for r in range(2):
                for c in range(2):
                    self.cells[r][c] = self._cell(r, c)
                    self.add(self.cells[r][c])
            self.cols, self.rows_ = self._cols(), self._rows()
            self.add(self.cols, self.rows_)

    # -- parts
    def _cell(self, r: int, c: int) -> VGroup:
        fr = RoundedRectangle(width=self.CELL_W, height=self.CELL_H, corner_radius=0.12,
                              stroke_color=S.GREY_DARK, stroke_width=2).set_fill(S.BG, 0)
        fr.move_to(self.p(self.CX[c], self.RY[r]))
        if r == 0:
            gl = rack(0.8)
            what = file_glyph(0.4, OWN) if c == 0 else image_block(None, 0.5, 0.36)
            g = VGroup(gl, what).arrange(RIGHT, buff=0.18)
        else:
            gl = instance(1.3, 0.85, inner=False)
            what = file_glyph(0.4, OWN) if c == 0 else image_block(None, 0.5, 0.36)
            what.move_to(gl)
            g = VGroup(gl, what)
        g.move_to(fr).shift(DOWN * 0.12)
        cell = VGroup(fr, g)
        cell.frame, cell.glyph, cell.what = fr, g, what
        return cell

    def _cols(self) -> VGroup:
        a = VGroup(label("a file ·", 22, INK), mono("main.py", 22, OWN)).arrange(RIGHT, buff=0.12)
        b = label("a container", 22, INK)
        a.move_to(self.p(self.CX[0], self.COLH_Y))
        b.move_to(self.p(self.CX[1], self.COLH_Y))
        return VGroup(a, b)

    def _rows(self) -> VGroup:
        a = VGroup(label("rented machine", 22, INK), label("dedicated hardware", 20, S.GREY)).arrange(
            DOWN, buff=0.08)
        b = label("serverless", 22, INK)
        a.move_to(self.p(self.ROWH_X, self.RY[0]))
        b.move_to(self.p(self.ROWH_X, self.RY[1] + 0.2))
        return VGroup(a, b)

    # -- S02 build
    def fan(self, scene, run_time: float = 1.6):
        """PLAYS: four PINK arrows fan out of the sketch card to the four cells; the cells draw; the
        arrows fade (the 2x2 is left)."""
        src = self.sketch.get_right() if self.sketch is not None else self.p(-2.4, 0.4)
        cells = [self._cell(r, c) for r in range(2) for c in range(2)]
        arrows = [Arrow(src, cl.frame.get_left() + RIGHT * 0.05, buff=0.1, color=ROUTE, stroke_width=4,
                        tip_length=0.2) for cl in cells]
        self.show(scene, *arrows, anims=[LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.15)],
                  run_time=run_time * 0.5)
        self.show(scene, *cells, anims=[LaggedStart(*[FadeIn(cl, scale=0.9) for cl in cells], lag_ratio=0.1)],
                  run_time=run_time * 0.3)
        for k, cl in enumerate(cells):
            self.cells[k // 2][k % 2] = cl
        self.drop(scene, *arrows, run_time=run_time * 0.2)

    def headers(self, scene, which: str = "cols", run_time: float = 0.7):
        """PLAYS: the column headers ('a file · main.py', 'a container') or the row headers ('rented
        machine / dedicated hardware', 'serverless') write in."""
        if which == "cols":
            self.cols = self._cols()
            self.show(scene, self.cols, anims=[LaggedStart(*[FadeIn(m, shift=DOWN * 0.15) for m in self.cols],
                                                           lag_ratio=0.3)], run_time=run_time)
        else:
            self.rows_ = self._rows()
            self.show(scene, self.rows_, anims=[LaggedStart(*[FadeIn(m, shift=RIGHT * 0.15) for m in self.rows_],
                                                            lag_ratio=0.3)], run_time=run_time)

    def tick_vm(self, scene, run_time: float = 0.8):
        """PLAYS: the two rented-machine cells tick in GREY-dashed, chips 'L1' and 'L2'."""
        new = []
        for c, lec in enumerate(("L1", "L2")):
            fr = self.cells[0][c].frame
            ch = dashed_chip(lec, PAST)
            ch.move_to(fr.get_corner(UR) + np.array([-ch.width / 2 - 0.08, -ch.height / 2 - 0.06, 0]))
            tk = check_glyph(0.26, S.GREY, 4).next_to(ch, LEFT, buff=0.1)
            new += [ch, tk]
        self.show(scene, *new, anims=[LaggedStart(*[FadeIn(m, scale=0.8) for m in new], lag_ratio=0.2)],
                  run_time=run_time, into=self.marks)
        self._ensure_marks()

    def _ensure_marks(self):
        if self.marks not in self.submobjects:
            self.add(self.marks)

    def today(self, scene, run_time: float = 0.8):
        """PLAYS: the two serverless cells glow YELLOW and a YELLOW 'today' chip sits under the row
        header 'serverless'."""
        ch = tag("today", TURN).next_to(self.rows_[1] if self.rows_ is not None else self.p(self.ROWH_X, -0.45),
                                        DOWN, buff=0.15)
        self.today_chip = ch
        self.show(scene, ch, run_time=run_time,
                  extra=[self.light(1, 0), self.light(1, 1)])

    def light(self, r: int, c: int, color=TURN):
        """ANIM: a cell's frame lights (YELLOW by default)."""
        return self.cells[r][c].frame.animate.set_stroke(color, 4)

    def unlight(self, r: int, c: int):
        """ANIM: a cell's frame back to plain."""
        return self.cells[r][c].frame.animate.set_stroke(S.GREY_DARK, 2)

    def parts(self, scene, run_time: float = 1.2):
        """PLAYS: the README's four parts as chips: '1 Deploy a function' under the file cell, '2
        Deploy a web app', '3 Add speech', '4 Run a job' stacked under the container cell.
        .part_chips[0..3]"""
        texts = ("1 Deploy a function", "2 Deploy a web app", "3 Add speech", "4 Run a job")
        chips = [chip(t, CLOUD, size=20) for t in texts]
        top = self.cells[1][0].frame.get_bottom()[1] - 0.18
        chips[0].move_to([self.cells[1][0].frame.get_center()[0], top - chips[0].height / 2, 0])
        y = top
        for ch in chips[1:]:
            ch.move_to([self.cells[1][1].frame.get_center()[0], y - ch.height / 2, 0])
            y -= ch.height + 0.1
        self.part_chips = chips
        self.show(scene, *chips, anims=[LaggedStart(*[FadeIn(m, shift=UP * 0.2) for m in chips], lag_ratio=0.2)],
                  run_time=run_time)

    def pulse_part(self, i: int, color=TURN):
        """ANIM: flash part chip i (0-3)."""
        return Indicate(self.part_chips[i].text, color=color, scale_factor=1.1)

    # -- later scenes
    def open_lid(self, scene, text: str = "Google built one", run_time: float = 1.0):
        """PLAYS (S05, S16): the file·serverless cell's outline 'lid' lifts and a TEAL box shows inside,
        beside main.py, with a GREY chip at the cell's top."""
        cl = self.cells[1][0]
        inst = cl.glyph[0]
        lid = Line(inst.get_corner(UL), inst.get_corner(UR), color=CLOUD, stroke_width=4)
        box_ = image_block(None, 0.42, 0.32).next_to(cl.what, RIGHT, buff=0.08)
        ch = grey_chip(text).move_to(cl.frame.get_top() + DOWN * 0.24)
        if ch.width > cl.frame.width - 0.1:
            ch.next_to(cl.frame, UP, buff=0.06)
        self.show(scene, lid, run_time=0.2)
        self.lid = VGroup(box_, ch)
        scene.play(Rotate(lid, angle=0.5, about_point=lid.get_start()), run_time=run_time * 0.4)
        self.show(scene, box_, ch, anims=[GrowFromCenter(box_), FadeIn(ch)], run_time=run_time * 0.4)
        self.drop(scene, lid, run_time=0.2)

    def split_job(self, scene, run_time: float = 1.0):
        """PLAYS (S12, S16): the container·serverless cell splits into 'service | job': a dashed divider,
        a service instance (left) and a job instance with a hard right edge (right), labels under."""
        cl = self.cells[1][1]
        fr = cl.frame
        div = DashedLine(fr.get_top() + DOWN * 0.1, fr.get_bottom() + UP * 0.1, color=S.GREY, stroke_width=2)
        lx, rx = fr.get_center()[0] - fr.width / 4, fr.get_center()[0] + fr.width / 4
        s_inst = instance(0.9, 0.55).move_to([lx, fr.get_center()[1] + 0.12, 0])
        j_inst = instance(0.9, 0.55).move_to([rx - 0.08, fr.get_center()[1] + 0.12, 0])
        edge = Line(j_inst.get_corner(UR) + RIGHT * 0.1, j_inst.get_corner(DR) + RIGHT * 0.1, color=INK,
                    stroke_width=4)
        ls = label("service", 20, INK).move_to([lx, fr.get_bottom()[1] + 0.25, 0])
        lj = label("job", 20, INK).move_to([rx, fr.get_bottom()[1] + 0.25, 0])
        new = VGroup(div, s_inst, j_inst, edge, ls, lj)
        old = cl.glyph
        cl.remove(old)
        self.show(scene, new, anims=[FadeOut(old), FadeIn(new)], run_time=run_time, into=cl)
        self.split = new
        self.split.service, self.split.job = VGroup(s_inst, ls), VGroup(j_inst, edge, lj)

    def cons(self, scene, texts=("cold starts", "limited control\nand debugging", "vendor lock-in"),
             run_time: float = 1.2):
        """PLAYS (S16): slide 16's three cons hang under the serverless row as RED cards (the part
        chips leave first). .con_cards[0..2]"""
        if self.part_chips:
            self.drop(scene, *self.part_chips)
            self.part_chips = []
        left = self.p(self.ROWH_X - 1.1, 0)[0]
        right = self.cells[1][1].frame.get_right()[0]
        w = (right - left - 0.3) / 3
        top = self.cells[1][0].frame.get_bottom()[1] - 0.25
        cards = []
        for i, t in enumerate(texts):
            cd = card(t.split("\n"), ERR, size=20, card_w=w)
            cd.move_to([left + w / 2 + i * (w + 0.15), top - cd.height / 2, 0])
            cards.append(cd)
        self.con_cards = cards
        self.show(scene, *cards, anims=[LaggedStart(*[FadeIn(c, shift=DOWN * 0.2) for c in cards], lag_ratio=0.25)],
                  run_time=run_time)

    def answer(self, scene, i: int, text: str, run_time: float = 0.6):
        """PLAYS: a GREEN answer card ('\\n' for two rows) under con card i, inside the frame."""
        cd = card(text.split("\n"), OWN, size=20)
        con = self.con_cards[i]
        cd.next_to(con, DOWN, buff=0.12)
        dx = min(0, SAFE_X - cd.get_right()[0]) + max(0, -SAFE_X - cd.get_left()[0])
        cd.shift(RIGHT * dx)
        self.answers[i] = cd
        self.show(scene, cd, anims=[FadeIn(cd, shift=UP * 0.15)], run_time=run_time)
        return cd


# ------------------------------------------------------------------ V2 · InstanceStrip, SlotPool
class InstanceStrip(_Anchored):
    """V2 · scale to zero, scale out, cold start, the meter. One time axis per row (x -3.0 .. 5.4 of
    the layout), its glyph + label on the left (x -5.4), rows 2.2 apart (centred on the origin).
    Above each axis: instance lives (lane 0 at +0.35, lane 1 at +0.9); under it: the GOLD meter.
    rows: names from ("vm", "serverless"). No prices: the meter is a picture of WHICH time is billed.
    .x(t) (t in [0, 1]) .axis[row] .label_[row] .meters[row] (list of segments)"""

    X0, X1 = -3.0, 5.4
    LABELS = {"vm": "VM · lecture 1", "serverless": "serverless"}

    def __init__(self, rows=("vm", "serverless"), times=("evening", "night", "morning"), row_gap: float = 2.2,
                 labels: dict | None = None, **kw):
        super().__init__(**kw)
        self.row_names = tuple(rows)
        n = len(rows)
        self.y = {r: (n - 1) / 2 * row_gap - i * row_gap for i, r in enumerate(rows)}
        self.axis, self.label_, self.meters, self.spans = {}, {}, {}, {}
        labels = {**self.LABELS, **(labels or {})}
        for r in rows:
            y = self.y[r]
            ax = Line(self.p(self.X0, y), self.p(self.X1, y), color=S.GREY, stroke_width=2)
            gl = rack(0.7) if r == "vm" else instance(1.0, 0.6)
            gl.move_to(self.p(-5.4, y + 0.25))
            lt = label(labels[r], 20, INK).next_to(gl, DOWN, buff=0.12)
            if r == "vm":
                ch = dashed_chip("L1", PAST).next_to(gl, RIGHT, buff=0.15)
                lt = VGroup(lt, ch)
            self.axis[r], self.label_[r] = ax, VGroup(gl, lt)
            self.meters[r], self.spans[r] = [], []
            self.add(ax, self.label_[r])
        self.times = None
        if times:
            ys = self.y[rows[-1]] - 0.75
            ts = VGroup(*[label(s, 20, S.GREY) for s in times])
            for k, t in enumerate(ts):
                t.move_to(self.p(self.X0 + (self.X1 - self.X0) * (k + 0.5) / len(times), ys))
            arrows = VGroup(*[label("→", 20, S.GREY).move_to((ts[k].get_right() + ts[k + 1].get_left()) / 2)
                              for k in range(len(ts) - 1)])
            self.times = VGroup(ts, arrows)
            self.add(self.times)

    def x(self, t: float) -> float:
        return self.p(self.X0 + (self.X1 - self.X0) * t, 0)[0]

    def _pt(self, row: str, t: float, dy: float = 0.0) -> np.ndarray:
        return np.array([self.x(t), self.p(0, self.y[row] + dy)[1], 0])

    def _bar(self, row, t0, t1, lane=0, solid=False, faint=False) -> VGroup:
        h = 0.42
        dy = 0.35 + 0.55 * lane
        w = max(0.12, self.x(t1) - self.x(t0))
        if solid:
            b = Rectangle(width=w, height=h, stroke_color=CLOUD, stroke_width=2.5).set_fill(CLOUD, 0.18)
            g = VGroup(b)
        else:
            b = outline_box(w, h, CLOUD, solid=False, radius=0.08)
            inner = Rectangle(width=max(0.06, w - 0.14), height=h * 0.4, stroke_width=0).set_fill(IMAGE, 0.35)
            g = VGroup(b, inner)
        g.move_to(self._pt(row, (t0 + t1) / 2, dy) + RIGHT * 0)
        g.move_to([(self.x(t0) + self.x(t1)) / 2, self._pt(row, 0, dy)[1], 0])
        if faint:
            g.set_opacity(0.4)
        return g

    def _meter(self, row, t0, t1, lane=0) -> Rectangle:
        w = max(0.08, self.x(t1) - self.x(t0))
        m = Rectangle(width=w, height=0.14, stroke_width=0).set_fill(COST, 0.85)
        return m.move_to([(self.x(t0) + self.x(t1)) / 2, self._pt(row, 0, -0.3 - 0.22 * lane)[1], 0])

    def pulses(self, scene, row: str, ts, lane: int = 0, run_time: float = 0.8) -> VGroup:
        """PLAYS: PINK request pulses drop onto the row's axis at times ts. Returns them."""
        dots = [pulse_dot().move_to(self._pt(row, t, 0.35 + 0.55 * lane + 0.42)) for t in ts]
        self.show(scene, *dots, anims=[LaggedStart(*[FadeIn(d, shift=DOWN * 0.25) for d in dots], lag_ratio=0.3)],
                  run_time=run_time)
        return VGroup(*dots)

    def vm_run(self, scene, row: str = "vm", run_time: float = 3.0):
        """PLAYS: the VM's solid life over the whole axis and its GOLD meter, both rising at a constant
        rate from left to right."""
        from manim import GrowFromEdge
        bar = self._bar(row, 0, 1, solid=True)
        m = self._meter(row, 0, 1)
        self.meters[row].append(m)
        self.show(scene, bar, m, anims=[GrowFromEdge(bar, LEFT, rate_func=linear),
                                        GrowFromEdge(m, LEFT, rate_func=linear)], run_time=run_time)

    def idle(self, scene, spans, row: str = "vm", text: str = "idle, still billed", run_time: float = 0.8):
        """PLAYS: GOLD shading over the idle stretches (t0, t1) of a row, labelled once above it."""
        shades = []
        for t0, t1 in spans:
            r = Rectangle(width=self.x(t1) - self.x(t0), height=1.0, stroke_width=0).set_fill(COST, 0.16)
            r.move_to([(self.x(t0) + self.x(t1)) / 2, self._pt(row, 0, 0.1)[1], 0])
            shades.append(r)
        lab = label(text, 20, COST).next_to(shades[0], UP, buff=0.08)
        self.show(scene, *shades, lab, run_time=run_time)

    def serve(self, scene, t0: float, t1: float, pulses=(), row: str = "serverless", lane: int = 0,
              billing: str = "request", cold: bool = True, run_time: float = 2.0):
        """PLAYS: a serverless instance lives from t0 to t1 on `lane` (dashed BLUE + TEAL): a grey puff
        at t0 (cold start), its life grows left to right with the PINK pulses, the GOLD meter moves
        only under the pulses (billing='request') or over the whole life ('instance'), then the
        instance dissolves (its life stays as a faint trace)."""
        from manim import GrowFromEdge
        bar = self._bar(row, t0, t1, lane)
        dots = [pulse_dot().move_to(self._pt(row, t, 0.35 + 0.55 * lane + 0.42)) for t in pulses]
        if billing == "instance":
            segs = [self._meter(row, t0, t1, lane)]
        else:
            segs = [self._meter(row, t - 0.012, t + 0.012, lane) for t in pulses]
        self.meters[row] += segs
        self.spans[row].append((t0, t1, tuple(pulses), lane, segs))
        if cold:
            pf = puff().move_to(self._pt(row, t0, 0.35 + 0.55 * lane) + LEFT * 0.25)
            self.show(scene, pf, anims=[FadeIn(pf, scale=0.5)], run_time=0.3)
            self.drop(scene, pf, run_time=0.25, extra=[GrowFromEdge(bar, LEFT, run_time=0.25)])
            self.add(bar)
        else:
            self.show(scene, bar, anims=[GrowFromEdge(bar, LEFT)], run_time=0.25)
        anims = []
        if dots:
            anims.append(LaggedStart(*[FadeIn(d, shift=DOWN * 0.2) for d in dots], lag_ratio=0.5))
        if segs:
            anims.append(LaggedStart(*[GrowFromEdge(s, LEFT) for s in segs], lag_ratio=0.5))
        if anims:
            self.show(scene, *dots, *segs, anims=anims, run_time=run_time)
        scene.play(bar.animate.set_opacity(0.3), run_time=0.4)

    def always_on(self, scene, row: str = "serverless", lane: int = 1, run_time: float = 2.0):
        """PLAYS: min instances 1: a faint instance over the whole axis on `lane`, with its own GOLD
        drip running the whole time (it has joined the VM row). Returns (life, drip)."""
        from manim import GrowFromEdge
        bar = self._bar(row, 0, 1, lane, faint=True)
        drip = self._meter(row, 0, 1, lane + 1)
        self.show(scene, bar, drip, anims=[FadeIn(bar), GrowFromEdge(drip, LEFT, rate_func=linear)],
                  run_time=run_time)
        return bar, drip

    def instance_billing(self, scene, on: bool = True, row: str = "serverless", run_time: float = 0.8):
        """PLAYS: every served life of the row is billed whole (on) or only under its pulses (off)."""
        anims = []
        for t0, t1, pulses, lane, segs in self.spans[row]:
            if on:
                tgt = self._meter(row, t0, t1, lane)
                anims += [Transform(s, tgt) for s in segs]
            else:
                for s, t in zip(segs, pulses):
                    anims.append(Transform(s, self._meter(row, t - 0.012, t + 0.012, lane)))
        if anims:
            scene.play(*anims, run_time=run_time)


class SlotPool(_Anchored):
    """V2 · S08's slots view: dashed BLUE instances, each with a TEAL box of `slots` thread slots
    (gunicorn's 4 threads = concurrency 4), at most `max_instances` (x 0.0 and 3.3 of the layout);
    PINK request dots line up at the left (x -5.6 .. -4.4); the waiting queue sits at x -2.6.
    .instances .slots (one list of slot squares per instance) .filled"""

    def __init__(self, max_instances: int = 2, slots: int = 4, **kw):
        super().__init__(**kw)
        self.max, self.nslots = max_instances, slots
        self.instances, self.slots, self.filled, self.waiting = [], [], [], []
        self.xs = [0.0 + 3.3 * i for i in range(max_instances)]

    def _instance(self, i: int) -> VGroup:
        inst = instance(2.8, 1.5, inner=False).move_to(self.p(self.xs[i], 0.2))
        ib = RoundedRectangle(width=2.2, height=0.8, corner_radius=0.08, stroke_color=IMAGE,
                              stroke_width=2.5).set_fill(IMAGE, 0.18).move_to(inst)
        sl = VGroup(*[Square(0.36, S.GREY) for _ in range(self.nslots)]).arrange(RIGHT, buff=0.14).move_to(ib)
        g = VGroup(inst, ib, sl)
        g.slots = list(sl)
        return g

    def line_up(self, scene, n: int = 10, text: str | None = "Translate ×10", run_time: float = 0.8):
        """PLAYS: n PINK request dots line up at the left edge (2 columns), with a YELLOW label."""
        dots = [pulse_dot(r=0.11).move_to(self.p(-5.6 + 0.45 * (k % 2), 1.0 - 0.45 * (k // 2))) for k in range(n)]
        new = list(dots)
        if text:
            lab = label(text, 20, TURN).move_to(self.p(-5.4, 1.6))
            new.append(lab)
            self.req_label = lab
        self.waiting = list(dots)
        self.show(scene, *new, anims=[LaggedStart(*[FadeIn(m) for m in new], lag_ratio=0.08)], run_time=run_time)
        return VGroup(*dots)

    def spawn(self, scene, run_time: float = 0.6):
        """PLAYS: the next instance appears (the second one splits off the first)."""
        i = len(self.instances)
        if i >= self.max:
            raise ValueError("SlotPool.spawn(): already at max instances")
        g = self._instance(i)
        anims = [FadeIn(g, scale=0.9)] if i == 0 else [FadeIn(g, shift=RIGHT * 0.8)]
        self.instances.append(g)
        self.slots.append(g.slots)
        self.filled.append([None] * self.nslots)
        self.show(scene, g, anims=anims, run_time=run_time)
        return g

    def fill(self, scene, dots=None, run_time: float = 1.6) -> list:
        """PLAYS: dots (default: the lined-up ones) fly into free slots in order, spawning instances up
        to max as needed. Returns the dots left over (no free slot)."""
        dots = list(self.waiting if dots is None else dots)
        moves, left = [], []
        for d in dots:
            spot = None
            for i, f in enumerate(self.filled):
                if None in f:
                    spot = (i, f.index(None))
                    break
            if spot is None and len(self.instances) < self.max:
                self.spawn(scene, run_time=0.4)
                spot = (len(self.instances) - 1, 0)
            if spot is None:
                left.append(d)
                continue
            i, k = spot
            self.filled[i][k] = d
            moves.append(d.animate.move_to(self.slots[i][k]))
        if moves:
            scene.play(LaggedStart(*moves, lag_ratio=0.12), run_time=run_time)
        self.waiting = left
        return left

    def ceiling(self, scene, text: str = "max = 2", run_time: float = 0.6):
        """PLAYS: the hard YELLOW ceiling line over the instance places, labelled."""
        y = 0.2 + 0.75 + 0.3
        ln = Line(self.p(self.xs[0] - 1.6, y), self.p(self.xs[-1] + 1.6, y), color=TURN, stroke_width=5)
        lab = label(text, 20, TURN).next_to(ln, UP, buff=0.08).align_to(ln, RIGHT)
        self.ceiling_line = ln
        self.show(scene, ln, lab, anims=[Create(ln), FadeIn(lab)], run_time=run_time)
        return ln

    def queue(self, scene, dots=None, text: str = "waiting", run_time: float = 0.8):
        """PLAYS: dots (default: the left-over ones) move into a GREY dashed waiting box at x -2.6."""
        dots = list(self.waiting if dots is None else dots)
        bx = outline_box(1.3, 0.8, S.GREY, solid=False).move_to(self.p(-2.6, 0.2))
        lab = label(text, 20, S.GREY).next_to(bx, DOWN, buff=0.1)
        self.show(scene, bx, lab, run_time=0.3)
        tg = [bx.get_center() + RIGHT * (k - (len(dots) - 1) / 2) * 0.4 for k in range(len(dots))]
        scene.play(*[d.animate.move_to(p) for d, p in zip(dots, tg)], run_time=run_time)
        return bx

    def refuse(self, scene, dot, text: str = "may be refused", run_time: float = 0.8):
        """PLAYS: a waiting dot flashes RED with a RED chip under the queue."""
        ch = err_chip(text, mono_font=False).next_to(dot, DOWN, buff=0.75)
        self.show(scene, ch, run_time=run_time, extra=[dot.animate.set_color(ERR),
                                                       Indicate(dot, color=ERR, scale_factor=1.6)])
        return ch

    def counter(self, scene, text: str = "8 in flight, at most", run_time: float = 0.5):
        """PLAYS: a label under the instances."""
        lab = label(text, 22, INK).move_to(self.p((self.xs[0] + self.xs[-1]) / 2, -1.05))
        self.show(scene, lab, run_time=run_time)
        return lab

    def dissolve(self, scene, run_time: float = 0.8):
        """PLAYS: the instances and their dots fade away (scale to zero)."""
        dots = [d for f in self.filled for d in f if d is not None]
        self.drop(scene, *self.instances, *dots, run_time=run_time)
        self.instances, self.slots, self.filled = [], [], []


def Square(s: float, color) -> Rectangle:  # noqa: N802  (a slot square; shadows manim's Square here)
    return Rectangle(width=s, height=s, stroke_color=color, stroke_width=2).set_fill(S.BG, 1)


class Slider(VGroup):
    """A small slider 'minimum instances  0 — 1': .to(v) ANIM moves the knob and the value. .value"""

    def __init__(self, text: str = "min instances", values=(0, 1), track_w: float = 1.6, color=COST,
                 size: float = 20, **kw):
        super().__init__(**kw)
        self.values = list(values)
        lab = label(text, size, INK)
        tr = Line(ORIGIN, RIGHT * track_w, color=S.GREY, stroke_width=4).next_to(lab, RIGHT, buff=0.3)
        ticks = VGroup(*[mono(str(v), size, S.GREY).next_to(tr.point_from_proportion(k / max(1, len(values) - 1)),
                                                           DOWN, buff=0.12) for k, v in enumerate(values)])
        knob = Circle(radius=0.12, stroke_color=color, stroke_width=3).set_fill(color, 1).move_to(tr.get_start())
        self.track, self.knob, self.ticks, self.text = tr, knob, ticks, lab
        self.value = values[0]
        self.add(lab, tr, ticks, knob)

    def to(self, v, run_time: float = 0.8):
        k = self.values.index(v)
        self.value = v
        pt = self.track.point_from_proportion(k / max(1, len(self.values) - 1))
        return AnimationGroup(self.knob.animate.move_to(pt),
                              Indicate(self.ticks[k], color=COST, scale_factor=1.2), run_time=run_time)


class Switch(VGroup):
    """A toggle 'Allow public access [● ]': .flip(on) ANIM; .on. off_text: the other setting's name
    shown instead of the label when off (e.g. Switch('Request-based', off_text='Instance-based'))."""

    def __init__(self, text: str = "Allow public access", on: bool = True, color=OWN, size: float = 20,
                 off_text: str | None = None, **kw):
        super().__init__(**kw)
        self.on, self.hi, self.size, self.on_text, self.off_text = on, color, size, text, off_text
        self.text = steady(text if on or not off_text else off_text, size, INK)
        tr = RoundedRectangle(width=0.7, height=0.34, corner_radius=0.17, stroke_color=S.GREY,
                              stroke_width=2).set_fill(color if on else S.GREY_DARK, 0.5)
        tr.next_to(self.text, RIGHT, buff=0.25)
        knob = Circle(radius=0.12, stroke_width=0).set_fill(INK, 1)
        knob.move_to(tr.get_right() + LEFT * 0.18 if on else tr.get_left() + RIGHT * 0.18)
        self.track, self.knob = tr, knob
        self.add(self.text, tr, knob)

    def flip(self, on: bool | None = None, run_time: float = 0.5):
        on = (not self.on) if on is None else on
        self.on = on
        pt = self.track.get_right() + LEFT * 0.18 if on else self.track.get_left() + RIGHT * 0.18
        anims = [self.knob.animate.move_to(pt),
                 self.track.animate.set_fill(self.hi if on else S.GREY_DARK, 0.5)]
        if self.off_text:
            new = steady(self.on_text if on else self.off_text, self.size, INK)
            new.move_to(self.text, aligned_edge=RIGHT)
            anims.append(Transform(self.text, new))
        return AnimationGroup(*anims, run_time=run_time)


# ------------------------------------------------------------------ V3 · BuildLine, FunctionInside
def entry_tag(name: str = ENTRY, ok: bool = True, size: float = 20) -> VGroup:
    """The GREEN name tag 'entry point: hello_http' (WHITE outline when it is any other name). .box .text"""
    col = OWN if ok else INK
    t = VGroup(label("entry point:", size, S.GREY), mono(name, size, col)).arrange(RIGHT, buff=0.12)
    h = mono("|", size).height + 0.26
    b = RoundedRectangle(width=t.width + 0.4, height=h, corner_radius=0.1, stroke_color=col,
                         stroke_width=2.5).set_fill(S.BG, 1)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text, g.name = b, t[1], name
    return g


def registry_shelf(with_image: bool = True, shelf_w: float = 2.4, size: float = 20) -> VGroup:
    """The BLUE 'Artifact Registry' shelf (a board + its name) with the function's TEAL image on it.
    .board .text .image"""
    board = Line(LEFT * shelf_w / 2, RIGHT * shelf_w / 2, color=CLOUD, stroke_width=6)
    t = label("Artifact Registry", size, CLOUD).next_to(board, DOWN, buff=0.15)
    g = VGroup(board, t)
    g.board, g.text, g.image = board, t, None
    if with_image:
        im = image_block("image", 1.4, 0.6).next_to(board, UP, buff=0.04)
        g.add(im)
        g.image = im
    return g


class BuildLine(_Anchored):
    """V3 · a function is a container you did not write. Inputs (x -4.9: main.py, requirements.txt,
    the entry tag) -> PURPLE Cloud Build (x -1.5) -> BLUE Artifact Registry shelf (x 1.6) -> dashed
    BLUE revision (x 4.7); around y 0. .inputs (.main .req .entry) .build .shelf .revision .image"""

    def __init__(self, entry: str = ENTRY, size: float = 20, **kw):
        super().__init__(**kw)
        self.size = size
        main = file_card("main.py", OWN)
        req = file_card("requirements.txt", OWN)
        ent = entry_tag(entry, ok=(entry == ENTRY))
        self.inputs = VGroup(main, req, ent).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        self.inputs.move_to(self.p(-4.9, 0.1))
        self.inputs.main, self.inputs.req, self.inputs.entry = main, req, ent
        bb = RoundedRectangle(width=2.6, height=1.9, corner_radius=0.14, stroke_color=TOOL,
                              stroke_width=3).set_fill(TOOL, 0.12).move_to(self.p(-1.5, 0.1))
        bt = VGroup(label("Cloud Build", 22, INK), label("buildpacks ·", 20, S.GREY),
                    VGroup(label("base", 20, S.GREY), mono("python312", 20, S.GREY)).arrange(RIGHT, buff=0.1))
        bt.arrange(DOWN, buff=0.1).move_to(bb)
        self.build = VGroup(bb, bt)
        self.build.frame, self.build.text = bb, bt
        self.shelf = registry_shelf(False).move_to(self.p(1.6, -0.35))
        self.revision = instance(2.0, 1.3, inner=False).move_to(self.p(4.7, 0.1))
        self.rev_label = label("revision", 20, CLOUD).next_to(self.revision, UP, buff=0.12)
        self.a1 = arrow(self.inputs.get_right() + RIGHT * 0.1, bb.get_left(), S.GREY, buff=0.05)
        self.a2 = arrow(bb.get_right(), self.shelf.board.get_left() + UP * 0.35, S.GREY, buff=0.08)
        self.add(self.inputs, self.build, self.shelf, self.revision, self.rev_label, self.a1, self.a2)
        self.image = self.a3 = self.inner = self.stamp_ = self.look = None

    def feed(self, scene, run_time: float = 1.2):
        """PLAYS: copies of the three inputs slide into the Cloud Build box and vanish there."""
        cps = [m.copy() for m in self.inputs]
        scene.add(*cps)
        scene.play(*[c.animate.move_to(self.build.frame).set_opacity(0) for c in cps],
                   Indicate(self.build.frame, color=TOOL, scale_factor=1.04), run_time=run_time)
        scene.remove(*cps)

    def stamp(self, scene, text: str = "pip install · build time, not per request", color=OWN,
              run_time: float = 0.5):
        """PLAYS: a chip under the build box (GREEN by default)."""
        ch = chip(text, color, size=20).next_to(self.build.frame, DOWN, buff=0.25)
        if self.stamp_ is not None:
            self.drop(scene, self.stamp_, run_time=0.2)
        self.stamp_ = ch
        self.show(scene, ch, anims=[FadeIn(ch, scale=1.2)], run_time=run_time)
        return ch

    def publish(self, scene, run_time: float = 0.9):
        """PLAYS: the TEAL image drops out of the build box onto the Artifact Registry shelf."""
        im = image_block("image", 1.4, 0.6).next_to(self.shelf.board, UP, buff=0.04)
        start = im.copy().move_to(self.build.frame)
        self.image = im
        self.show(scene, im, anims=[Transform(start, im)], run_time=run_time)
        scene.remove(start)

    def start(self, scene, run_time: float = 0.8):
        """PLAYS: an arrow from the shelf starts the revision (its TEAL inner box lights)."""
        self.a3 = arrow(self.shelf.board.get_right() + UP * 0.35, self.revision.get_left(), S.GREY, buff=0.08)
        ib = RoundedRectangle(width=1.1, height=0.65, corner_radius=0.06, stroke_color=IMAGE,
                              stroke_width=2.5).set_fill(IMAGE, 0.25).move_to(self.revision)
        self.inner = ib
        self.show(scene, self.a3, ib, anims=[GrowArrow(self.a3), FadeIn(ib, scale=0.8)], run_time=run_time)

    def set_entry(self, scene, name: str, run_time: float = 0.6):
        """PLAYS: the entry tag's name changes (GREEN for hello_http, a plain WHITE outline otherwise)."""
        new = entry_tag(name, ok=(name == ENTRY)).move_to(self.inputs.entry, aligned_edge=LEFT)
        old = self.inputs.entry
        self.swap(scene, old, new, run_time=run_time)
        self.inputs.entry = new

    def lookup(self, scene, run_time: float = 1.2):
        """PLAYS: the revision starts and looks the entry name up in main.py: an arrow labelled by the
        name reaches back into the main.py card. hello_http: a GREEN tick. Any other name: the arrow
        snaps RED, a RED cross on main.py, the revision RED + 'revision not ready'."""
        name = self.inputs.entry.name
        ok = name == ENTRY
        col = OWN if ok else ERR
        start = self.revision.get_bottom() + DOWN * 0.05
        end = self.inputs.main.get_bottom() + DOWN * 0.05
        path = _poly([start, start + DOWN * 1.35, [end[0], start[1] - 1.35, 0], end], col, stroke=3)
        lab = mono(name, 20, col).move_to([(start[0] + end[0]) / 2, start[1] - 1.6, 0])
        self.look = VGroup(path, lab)
        self.show(scene, path, lab, anims=[Create(path.line), FadeIn(path.tip_arrow), FadeIn(lab)],
                  run_time=run_time * 0.6)
        if ok:
            mk = check_glyph(0.32, OWN).next_to(self.inputs.main, RIGHT, buff=0.12)
            self.show(scene, mk, anims=[Create(mk)], run_time=run_time * 0.4)
        else:
            mk = cross_glyph(0.3).next_to(self.inputs.main, RIGHT, buff=0.12)
            nr = label("revision not ready", 20, ERR).next_to(self.revision, DOWN, buff=0.15)
            self.show(scene, mk, nr, anims=[Create(mk), FadeIn(nr)], run_time=run_time * 0.4,
                      extra=[self.revision.frame.animate.set_stroke(ERR)])
        return self.look

    def skip_build(self, scene, text: str = "no build this time", run_time: float = 0.8):
        """PLAYS (S08): the Cloud Build box turns GREY-dashed with a GREY cross and a label."""
        bb = self.build.frame
        dash = outline_box(bb.width, bb.height, S.GREY, solid=False).move_to(bb)
        x = cross_glyph(0.9, S.GREY, 5).move_to(bb)
        lab = label(text, 20, S.GREY).next_to(bb, DOWN, buff=0.2)
        self.show(scene, dash, x, lab, run_time=run_time,
                  extra=[bb.animate.set_stroke(opacity=0).set_fill(opacity=0),
                         self.build.text.animate.set_opacity(0.35)])

    def shelf_tag(self, scene, text: str = "stays after you delete the service · clean up at the end",
                  run_time: float = 0.5):
        """PLAYS: a GOLD cost chip under the shelf (no amounts)."""
        ch = chip(_no_amount(text), COST, size=20).next_to(self.shelf, DOWN, buff=0.15)
        if ch.get_right()[0] > SAFE_X:
            ch.shift(LEFT * (ch.get_right()[0] - SAFE_X))
        self.show(scene, ch, run_time=run_time)
        return ch


class FunctionInside(_Anchored):
    """V3 · the zoom into a function's revision: a dashed BLUE instance (12.4 x 4.2) holding PURPLE
    'functions-framework' > 'Flask app' > 'gunicorn' (with its PINK address '0.0.0.0:$PORT' and an
    ear on the instance's left edge), the GREEN entry tag, and a GREEN main.py card (lines 7-8) on
    the right. .outer .framework .flask .gunicorn .ear .entry .card (.deco .defline)"""

    def __init__(self, entry: str = ENTRY, **kw):
        super().__init__(**kw)
        self.outer = instance(12.4, 4.2, inner=False).move_to(self.p(0, 0))
        self.olabel = label("revision", 20, CLOUD).move_to(self.outer.get_corner(UL) + np.array([0.75, -0.3, 0]))

        def nest(w, h, text, x, y):
            b = RoundedRectangle(width=w, height=h, corner_radius=0.12, stroke_color=TOOL,
                                 stroke_width=2.5).set_fill(TOOL, 0.08).move_to(self.p(x, y))
            t = (mono if "-" in text else label)(text, 20, INK)
            t.move_to(b.get_corner(UL) + np.array([t.width / 2 + 0.2, -0.25, 0]))
            g = VGroup(b, t)
            g.frame, g.text = b, t
            return g

        self.framework = nest(6.6, 3.3, "functions-framework", -2.6, -0.15)
        self.flask = nest(5.0, 2.3, "Flask app", -2.6, -0.45)
        gb = RoundedRectangle(width=3.4, height=1.15, corner_radius=0.1, stroke_color=TOOL,
                              stroke_width=2.5).set_fill(TOOL, 0.15).move_to(self.p(-2.6, -0.8))
        gt = VGroup(label("gunicorn", 20, INK), mono("0.0.0.0:$PORT", 20, ROUTE)).arrange(DOWN, buff=0.06).move_to(gb)
        self.gunicorn = VGroup(gb, gt)
        self.gunicorn.frame, self.gunicorn.addr = gb, gt[1]
        self.ear = ear(None).move_to(self.outer.get_left() + np.array([0.15, 0, 0]))
        self.ear.move_to([self.outer.get_left()[0] + 0.12, gb.get_center()[1], 0])
        self.wire = Line(self.ear.get_right(), gb.get_left(), color=ROUTE, stroke_width=3)
        self.entry = entry_tag(entry, ok=(entry == ENTRY)).move_to(self.p(-1.3, 0.85))
        deco, dfn = excerpt("tutorial/function/main.py", 7, 8).split("\n")
        rows = VGroup(mono_line(deco, 20, S.GREY), mono_line(dfn, 20, INK)).arrange(DOWN, buff=0.18,
                                                                                    aligned_edge=LEFT)
        cf = outline_box(rows.width + 0.5, rows.height + 0.9, OWN, solid=True, fill_opacity=0.06)
        ct = mono("main.py", 20, OWN)
        cardg = VGroup(cf, rows, ct)
        rows.move_to(cf).shift(DOWN * 0.15)
        ct.move_to(cf.get_corner(UL) + np.array([ct.width / 2 + 0.2, -0.25, 0]))
        cardg.move_to(self.p(3.35, -0.2))
        self.card = cardg
        self.card.deco, self.card.defline = rows[0], rows[1]
        self.add(self.outer, self.olabel, self.framework, self.flask, self.gunicorn, self.ear, self.wire,
                 self.entry, self.card)

    def request(self, scene, run_time: float = 1.0):
        """PLAYS: a PINK request enters the ear and reaches gunicorn. Returns the dot."""
        d = pulse_dot(r=0.11).move_to(self.ear.get_left() + LEFT * 0.3)
        self.show(scene, d, run_time=0.2)
        scene.play(d.animate.move_to(self.gunicorn.frame.get_left() + RIGHT * 0.2), run_time=run_time)
        self.dot = d
        return d

    def lookup(self, scene, name: str | None = None, run_time: float = 1.4):
        """PLAYS: an arrow labelled by the entry name reaches into main.py. hello_http: `def
        hello_http` lights GREEN and the answer flows back out of the ear. Another name: the arrow
        snaps RED, 'no such def'. (Change the tag first with name='translate'.)"""
        if name is not None and name != self.entry.name:
            new = entry_tag(name, ok=(name == ENTRY)).move_to(self.entry)
            self.swap(scene, self.entry, new, run_time=0.5)
            self.entry = new
        name = self.entry.name
        ok = name == ENTRY
        col = OWN if ok else ERR
        tgt = substring(self.card.defline, ENTRY)
        a = arrow(self.entry.get_right(), tgt.get_left() + LEFT * 0.05 if ok else self.card.get_left(),
                  col, stroke=4, buff=0.08)
        self.show(scene, a, anims=[GrowArrow(a)], run_time=run_time * 0.4)
        if ok:
            back = pulse_dot(OWN, r=0.11).move_to(tgt)
            scene.play(tgt.animate.set_color(OWN), Indicate(tgt, color=OWN, scale_factor=1.15),
                       run_time=run_time * 0.3)
            self.show(scene, back, run_time=0.1)
            scene.play(back.animate.move_to(self.ear.get_left() + LEFT * 0.3), run_time=run_time * 0.4)
            self.drop(scene, back, run_time=0.2)
        else:
            nd = label("no such def", 20, ERR).next_to(a, DOWN, buff=0.12)
            self.show(scene, nd, run_time=run_time * 0.3, extra=[Indicate(a, color=ERR)])
        return a


def _poly(points, color, stroke: float = 3, tip: bool = True, dashed: bool = False) -> VGroup:
    """A polyline route through `points` ending in an arrow tip. .path (the whole route, for
    travel()) .line .tip_arrow"""
    pts = [np.array(p, dtype=float) for p in points]
    line = VMobject(stroke_color=color, stroke_width=stroke).set_points_as_corners(pts)
    if dashed:
        line = DashedVMobject(line, num_dashes=max(8, int(sum(np.linalg.norm(b - a) for a, b in
                                                            zip(pts, pts[1:])) * 5)))
        line.set_stroke(color, stroke)
    g = VGroup(line)
    g.path = VMobject().set_points_as_corners(pts)
    g.line, g.tip_arrow = line, None
    if tip:
        a, b = pts[-2], pts[-1]
        d = (b - a) / max(1e-6, np.linalg.norm(b - a))
        ta = Arrow(b - d * 0.3, b, buff=0, color=color, stroke_width=stroke, tip_length=0.18,
                   max_tip_length_to_length_ratio=0.9)
        g.add(ta)
        g.tip_arrow = ta
    return g


# ------------------------------------------------------------------ V4 · QueryToArgs
class QueryToArgs(_Anchored):
    """V4 · one URL, many inputs. The base URL (mono 22, GREY) on one row (y 2.2 of the layout, left
    edge x -6.2) and the PINK query string under it (mono 24, y 1.5). split() takes it apart at '?'
    and '&' into three key=value rows (x -6.2, y 0.6 / -0.1 / -0.8). .base .query .pairs (after
    split) .keys ('text', 'src', 'dest')"""

    KEYS = ("text", "src", "dest")
    DEFAULTS = ('"Welcome to AC215"', '"en"', '"es"')

    def __init__(self, url: str = FUNCTION_URL, query: str = QUERY, size: float = 24, show_query: bool = True,
                 **kw):
        super().__init__(**kw)
        self.size, self.qtext = size, query
        self.base = mono_line(url, 22, S.GREY)
        self.base.shift(self.p(-6.2, 2.2) - self.base.strut.get_left())
        self.query = mono_line(query, size, ROUTE)
        self.query.shift(self.p(-6.2, 1.5) - self.query.strut.get_left())
        self.pairs = None
        self.add(self.base)
        if show_query:
            self.add(self.query)

    def type_query(self, scene, run_time: float = 1.6):
        """PLAYS: the query string types in after the URL (PINK)."""
        self._ensure(scene)
        if self.query in self.submobjects:
            self.remove(self.query)
        scene.play(ShowIncreasingSubsets(self.query.glyphs if hasattr(self.query, "glyphs") else self.query,
                                         rate_func=linear), run_time=run_time)
        scene.remove(self.query)
        self.add(self.query)

    def _segments(self):
        q = self.qtext
        cuts = [0] + [i for i, ch in enumerate(q) if ch in "?&"] + [len(q)]
        segs, hinges = [], []
        for a, b in zip(cuts, cuts[1:]):
            if q[a] in "?&":
                hinges.append(glyph_range(self.query, a, a + 1))
                a += 1
            segs.append((a, b))
        return [glyph_range(self.query, a, b) for a, b in segs if b > a], [q[a:b] for a, b in segs if b > a], hinges

    def split(self, scene, run_time: float = 1.4, hinge_time: float = 0.6):
        """PLAYS: the '?' and each '&' flash (PINK hinges), then the three key=value pairs move apart
        into rows. .pairs (mono_line rows, PINK)"""
        segs, texts, hinges = self._segments()
        self._ensure(scene)
        scene.play(*[Indicate(h, color=TURN, scale_factor=1.5) for h in hinges], run_time=hinge_time)
        news = []
        for k, s in enumerate(texts):
            ln = mono_line(s, self.size, ROUTE)
            ln.shift(self.p(-6.2, 0.6 - 0.7 * k) - ln.strut.get_left())
            news.append(ln)
        cps = [VGroup(*[g.copy() for g in seg]) for seg in segs]
        self.remove(self.query)
        scene.add(*cps)
        scene.play(*[Transform(c, n) for c, n in zip(cps, news)], run_time=run_time)
        scene.remove(*cps)
        self.pairs = VGroup(*news)
        self.add(self.pairs)
        return self.pairs

    def melt(self, scene, run_time: float = 1.0):
        """PLAYS: in the text pair, each '%20' melts into a space ('text=Good afternoon everyone')."""
        old = self.pairs[0]
        s = old.text.replace("%20", " ")
        new = mono_line(s, self.size, ROUTE)
        new.shift(old.strut.get_left() - new.strut.get_left())
        spots = [glyph_range(old, m.start(), m.end()) for m in re.finditer("%20", old.text)]
        scene.play(*[Indicate(sp, color=TURN, scale_factor=1.3) for sp in spots], run_time=run_time * 0.4)
        self.swap(scene, old, new, run_time=run_time * 0.6, into=self.pairs)
        self.pairs.submobjects.insert(0, self.pairs.submobjects.pop())

    def into(self, scene, panel, run_time: float = 1.6):
        """PLAYS: each pair flies onto its request.args.get line of a code(main.py, 9, 12) panel; the
        key flashes PINK and that line's default greys out. The pairs leave the piece."""
        if self.pairs is None:
            raise ValueError("QueryToArgs.into(): split() first")
        for k, (pair, key, dflt) in enumerate(zip(list(self.pairs), self.KEYS, self.DEFAULTS)):
            ksp = code_span(panel.code, k, f'"{key}"')
            dsp = code_span(panel.code, k, dflt)
            self.pairs.remove(pair)
            scene.add(pair)
            scene.play(pair.animate.next_to(ksp, UP, buff=0.08).set_opacity(0.0), Indicate(ksp, color=ROUTE),
                       run_time=run_time / 3 * 0.6)
            scene.remove(pair)
            scene.play(dsp.animate.set_color(S.GREY).set_opacity(0.45), run_time=run_time / 3 * 0.4)
        self.pairs = None

    def defaults(self, panel, color=TURN):
        """ANIM: with no query string the three defaults of a code(main.py, 9, 12) panel light up."""
        return LaggedStart(*[Indicate(code_span(panel.code, k, d), color=color, scale_factor=1.1)
                             for k, d in enumerate(self.DEFAULTS)], lag_ratio=0.3)

    def join(self, scene, run_time: float = 1.2):
        """PLAYS: the pairs join back into one query string (with '?', '&' and '%20') on the query row."""
        if self.pairs is None:
            raise ValueError("QueryToArgs.join(): split() first")
        new = mono_line(self.qtext, self.size, ROUTE)
        new.shift(self.p(-6.2, 1.5) - new.strut.get_left())
        old = self.pairs
        self.pairs = None
        self.swap(scene, old, new, run_time=run_time)
        self.query = new

    def provider(self, scene, src, text: str = "googletrans'\npublic endpoint", run_time: float = 1.4,
                 cloud_at=None):
        """PLAYS: a dashed BLUE 'Google Cloud' outline around `src` (a mobject: the handler), an
        ORANGE cloud for googletrans' endpoint (right of src, or at cloud_at=(x, y)), an ORANGE arrow
        out and a dashed one back. Returns VGroup(outline, cloud, out_arrow, back_arrow)."""
        ol = outline_box(src.width + 0.4, src.height + 0.6, CLOUD, solid=False).move_to(src).shift(UP * 0.12)
        olab = label("Google Cloud", 20, CLOUD).move_to(ol.get_corner(UL) + np.array([0.95, -0.2, 0]))
        cl = cloud_shape(text, SHARED, 2.6)
        if cloud_at is not None:
            cl.move_to([cloud_at[0], cloud_at[1], 0])
        else:
            cl.next_to(ol, RIGHT, buff=0.9)
            if cl.get_right()[0] > SAFE_X:
                cl.shift(LEFT * (cl.get_right()[0] - SAFE_X))
        a_out = Arrow(ol.get_right() + UP * 0.15, cl.get_left() + UP * 0.15, buff=0.05, color=SHARED,
                      stroke_width=4, tip_length=0.2)
        a_back = DashedLine(cl.get_left() + DOWN * 0.2, ol.get_right() + DOWN * 0.2, color=SHARED,
                            stroke_width=3).add_tip(tip_length=0.18)
        self.show(scene, ol, olab, cl, run_time=run_time * 0.4)
        self.show(scene, a_out, anims=[GrowArrow(a_out)], run_time=run_time * 0.3)
        self.show(scene, a_back, anims=[Create(a_back)], run_time=run_time * 0.3)
        g = VGroup(VGroup(ol, olab), cl, a_out, a_back)
        g.outline, g.cloud, g.out_arrow, g.back_arrow = g[0], cl, a_out, a_back
        return g


# ------------------------------------------------------------------ V5 · CommandSlots, PortEnvelope
class CommandSlots(_Anchored):
    """V5 (S07) / V7 (S13, S15) · the image's two startup slots (laptop/16:11-12) on a TEAL block:
    'ENTRYPOINT:' [] and 'CMD:' [python -m translation_demo serve]. Block (slot_w + 2.6) wide,
    centred on the origin; the CMD slot grows downward when argument chips wrap.
    .block .entry_slot .cmd_slot .entry_content .cmd_content .arg_chips (VGroup or None)
    .command_chip (or None)"""

    def __init__(self, slot_w: float = 8.6, size: float = 20, **kw):
        super().__init__(**kw)
        self.slot_w, self.size = slot_w, size
        bw = slot_w + 2.6
        self.block = RoundedRectangle(width=bw, height=2.0, corner_radius=0.14, stroke_color=IMAGE,
                                      stroke_width=3).set_fill(IMAGE, 0.1).move_to(self.p(0, 0))
        self.blabel = label("the image", 20, IMAGE).move_to(self.block.get_corner(UL) + np.array([0.8, -0.25, 0]))
        x_slot = self.block.get_left()[0] + 2.3 + slot_w / 2
        self.entry_slot = self._slot(slot_w, 0.52).move_to([x_slot, self.p(0, 0.25)[1], 0])
        self.cmd_slot = self._slot(slot_w, 0.52).move_to([x_slot, self.p(0, -0.5)[1], 0])
        self.entry_name = mono("ENTRYPOINT:", size, S.GREY).next_to(self.entry_slot, LEFT, buff=0.2)
        self.cmd_name = mono("CMD:", size, S.GREY).next_to(self.cmd_slot, LEFT, buff=0.2).align_to(self.entry_name, LEFT)
        self.entry_content = self._in_slot(mono("[]", size, S.GREY), self.entry_slot)
        self.cmd_content = self._in_slot(mono("[python -m translation_demo serve]", size, IMAGE), self.cmd_slot)
        self.arg_chips = self.command_chip = None
        self.add(self.block, self.blabel, self.entry_slot, self.cmd_slot, self.entry_name, self.cmd_name,
                 self.entry_content, self.cmd_content)

    @staticmethod
    def _slot(w, h):
        return RoundedRectangle(width=w, height=h, corner_radius=0.08, stroke_color=S.GREY_DARK,
                                stroke_width=2).set_fill(TERM_BG, 1)

    @staticmethod
    def _in_slot(m, slot):
        return m.move_to(slot).align_to(slot, LEFT).shift(RIGHT * 0.15)

    def _grow_to(self, scene, rows_h: float, run_time: float = 0.4):
        need = max(0.52, rows_h + 0.24)
        if abs(need - self.cmd_slot.height) < 1e-3:
            return
        top = self.cmd_slot.get_top()[1]
        new_slot = self._slot(self.slot_w, need).move_to([self.cmd_slot.get_center()[0], top - need / 2, 0])
        btop = self.block.get_top()[1]
        bh = (btop - (top - need)) + 0.35
        new_block = RoundedRectangle(width=self.block.width, height=bh, corner_radius=0.14, stroke_color=IMAGE,
                                     stroke_width=3).set_fill(IMAGE, 0.1)
        new_block.move_to([self.block.get_center()[0], btop - bh / 2, 0])
        scene.play(Transform(self.cmd_slot, new_slot), Transform(self.block, new_block), run_time=run_time)

    def ghost_args(self, scene, text: str = "your arguments", run_time: float = 1.6):
        """PLAYS (S07): a GREY ghost chip slides into the CMD slot and pushes the old CMD out to the
        right, then everything reverts."""
        g = dashed_chip(text, S.GREY)
        self._in_slot(g, self.cmd_slot)
        g.shift(LEFT * 1.5).set_opacity(0)
        self.show(scene, g, anims=[g.animate.shift(RIGHT * 1.5).set_opacity(1),
                                   self.cmd_content.animate.shift(RIGHT * 1.2).set_opacity(0.15)],
                  run_time=run_time * 0.5)
        scene.play(self.cmd_content.animate.shift(LEFT * 1.2).set_opacity(1), run_time=run_time * 0.3)
        self.drop(scene, g, run_time=run_time * 0.2)

    def set_command(self, scene, value: str = "python", run_time: float = 0.7):
        """PLAYS: the console's Container command chip drops into the ENTRYPOINT slot (the '[]' goes)."""
        ch = chip_row([value], size=self.size).chips[0]
        self._in_slot(ch, self.entry_slot)
        self.command_chip = ch
        old = self.entry_content
        self.entry_content = ch
        self.remove(old)
        self.show(scene, ch, anims=[FadeIn(ch, shift=DOWN * 0.4), FadeOut(old)], run_time=run_time)

    def clear_cmd(self, scene, run_time: float = 0.6):
        """PLAYS: the image's old CMD lifts out of its slot as one piece and fades GREY."""
        old = self.cmd_content
        self.cmd_content = None
        self.drop(scene, old, run_time=run_time, shift=UP * 0.5,
                  extra=[old.animate.set_color(S.GREY)])

    def add_args(self, scene, values=ARGS, lag: float = 0.25, run_time: float | None = None):
        """PLAYS: the argument chips fill the CMD slot one at a time (wrapping into rows; the slot and
        the block grow). Clears the old CMD first if it is still there. .arg_chips"""
        if self.cmd_content is not None:
            self.clear_cmd(scene, run_time=0.4)
        cr = chip_row(values, max_w=self.slot_w - 0.3, size=self.size)
        self._grow_to(scene, cr.rows.height)
        cr.rows.move_to(self.cmd_slot).align_to(self.cmd_slot, LEFT).shift(RIGHT * 0.15)
        self.arg_chips = VGroup(*cr.chips)
        rt = run_time if run_time is not None else lag * len(cr.chips) + 0.4
        self.show(scene, *cr.chips, anims=[LaggedStart(*[FadeIn(c, shift=DOWN * 0.2) for c in cr.chips],
                                                       lag_ratio=0.6)], run_time=rt)
        return self.arg_chips

    def conveyor(self, scene, run_time: float = 1.2, text: str = "argv"):
        """PLAYS: ENTRYPOINT's chip and the argument chips slide together into one argv row (wrapped,
        a PINK belt under each row) inside the block; the slot names fade. Returns the chip row."""
        vals = ([self.command_chip.value] if self.command_chip is not None else []) + \
            [c.value for c in self.arg_chips]
        cr = chip_row(vals, max_w=self.block.width - 0.5, size=self.size)
        cr.rows.move_to(self.block).shift(DOWN * 0.1)
        belts = VGroup(*[Line(r.get_corner(DL) + DOWN * 0.08, r.get_corner(DR) + DOWN * 0.08, color=ROUTE,
                              stroke_width=4) for r in cr.rows])
        lab = mono(text, 20, ROUTE).move_to(self.blabel).align_to(self.blabel, LEFT).shift(RIGHT * (self.blabel.width + 0.3))
        olds = ([self.command_chip] if self.command_chip is not None else []) + list(self.arg_chips)
        for o in olds:
            self._detach(o)
        scene.add(*olds)
        fade = [self.entry_slot, self.cmd_slot, self.entry_name, self.cmd_name]
        for m in fade:
            self.remove(m)
        scene.play(*[Transform(o, n) for o, n in zip(olds, cr.chips)], *[FadeOut(m) for m in fade],
                   FadeIn(belts), FadeIn(lab), run_time=run_time)
        scene.remove(*olds, *fade, belts, lab)
        self.add(*cr.chips, belts, lab)
        self.arg_chips, self.command_chip, self.argv = VGroup(*cr.chips), None, cr
        return cr

    def one_chip(self, scene, run_time: float = 1.0) -> VGroup:
        """PLAYS (S13): the argument chips melt into ONE fat chip holding the whole block (README:
        'do not paste the whole block into one argument field'). Returns it (.box .rows)."""
        vals = [c.value for c in self.arg_chips]
        n = int((self.slot_w - 0.6) / cell_width(self.size))
        rows = VGroup(*[mono(s, self.size, INK) for s in soft([" ".join(vals)], n)]).arrange(
            DOWN, buff=0.1, aligned_edge=LEFT)
        b = RoundedRectangle(width=rows.width + 0.4, height=rows.height + 0.3, corner_radius=0.1,
                             stroke_color=INK, stroke_width=3).set_fill(S.BG, 1)
        rows.move_to(b)
        fat = VGroup(b, rows)
        fat.box, fat.rows = b, rows
        self._grow_to(scene, fat.height)
        self._in_slot(fat, self.cmd_slot).align_to(self.cmd_slot, UP).shift(DOWN * 0.12)
        olds = list(self.arg_chips)
        for o in olds:
            self._detach(o)
        scene.add(*olds)
        scene.play(*[Transform(o, fat.copy()) for o in olds], run_time=run_time)
        scene.remove(*olds)
        self.add(fat)
        self.arg_chips, self.fat = None, fat
        return fat

    def no_command(self, scene, run_time: float = 1.0):
        """PLAYS (S13 ponder answer): with ENTRYPOINT empty, the first argument chip ('-m') slides into
        the program position (the ENTRYPOINT slot) and turns RED, label 'program?'."""
        first = self.arg_chips[0]
        tgt = first.copy()
        self._in_slot(tgt, self.entry_slot)
        tgt.shift(RIGHT * 0.6)
        lab = label("program?", 20, ERR).next_to(self.entry_slot, RIGHT, buff=-1.6)
        lab.move_to([self.entry_slot.get_right()[0] - lab.width / 2 - 0.2, self.entry_slot.get_center()[1], 0])
        self.show(scene, lab, run_time=run_time,
                  extra=[first.animate.move_to(tgt).set_color(ERR)])
        self.program_label = lab
        return first

    def swap_args(self, scene, values, hi=(), run_time: float = 1.2):
        """PLAYS (S15): the whole row of argument chips lifts out of the CMD slot and a new row drops in
        (indices in `hi` YELLOW). The block's slots must still be there (not after conveyor())."""
        olds = list(self.arg_chips) if self.arg_chips is not None else []
        if olds:
            self.drop(scene, *olds, run_time=run_time * 0.4, shift=UP * 0.6)
        cr = chip_row(values, max_w=self.slot_w - 0.3, size=self.size, hi=hi)
        self._grow_to(scene, cr.rows.height, run_time=0.2)
        cr.rows.move_to(self.cmd_slot).align_to(self.cmd_slot, LEFT).shift(RIGHT * 0.15)
        self.arg_chips = VGroup(*cr.chips)
        self.show(scene, *cr.chips, anims=[FadeIn(VGroup(*cr.chips), shift=DOWN * 0.5)], run_time=run_time * 0.6)
        return self.arg_chips

    def reset(self, scene, values=ARGS, run_time: float = 0.8):
        """PLAYS (S13): back to ENTRYPOINT [] (empty) with the argument chips in the CMD slot (no
        command chip, no fat chip, no program label)."""
        gone = [m for m in (self.command_chip, getattr(self, "fat", None), getattr(self, "program_label", None))
                if m is not None and m in self.get_family()]
        if self.arg_chips is not None:
            gone += list(self.arg_chips)
        if self.entry_content is not None and self.entry_content is not self.command_chip:
            gone.append(self.entry_content)
        self.drop(scene, *gone, run_time=run_time * 0.4)
        self.command_chip = self.fat = self.program_label = None
        cr = chip_row(values, max_w=self.slot_w - 0.3, size=self.size)
        self._grow_to(scene, cr.rows.height, run_time=0.2)
        cr.rows.move_to(self.cmd_slot).align_to(self.cmd_slot, LEFT).shift(RIGHT * 0.15)
        self.entry_content = self._in_slot(mono("[]", self.size, S.GREY), self.entry_slot)
        self.arg_chips = VGroup(*cr.chips)
        self.show(scene, self.entry_content, *cr.chips, run_time=run_time * 0.6)


class PortEnvelope(_Anchored):
    """V5 · the container contract. A TEAL container (5.0 x 2.8, x -1.5 .. 3.5 of the layout) with a
    PURPLE process box (2.6 x 1.1); its ear on the container's left edge; a GREY laptop wall at x -3.9
    with a PINK door and a pipe to the ear (wall()). Extent x -4.9 .. 3.5 once the wall shows.
    .box .proc (.frame .text) .ear_ .pipe .door .wall_"""

    def __init__(self, size: float = 20, **kw):
        super().__init__(**kw)
        self.size = size
        self.box = RoundedRectangle(width=5.0, height=2.8, corner_radius=0.14, stroke_color=IMAGE,
                                    stroke_width=3).set_fill(IMAGE, 0.08).move_to(self.p(1.0, 0))
        self.blabel = label("container", 20, IMAGE).move_to(self.box.get_corner(UL) + np.array([0.75, -0.25, 0]))
        self.add(self.box, self.blabel)
        self.proc = self.ear_ = self.env = self.pipe = self.door = self.wall_ = self.slots = None
        self.ear_y = self.p(0, -0.2)[1]

    def _proc(self, text: str) -> VGroup:
        fr = RoundedRectangle(width=2.6, height=1.1, corner_radius=0.1, stroke_color=TOOL,
                              stroke_width=3).set_fill(TOOL, 0.15).move_to(self.p(1.4, -0.2))
        t = steady(text, 22, INK, mono_font=True).move_to(fr).shift(UP * 0.18)
        g = VGroup(fr, t)
        g.frame, g.text = fr, t
        return g

    def start(self, scene, text: str = "python", run_time: float = 0.6):
        """PLAYS: the CMD starts a PURPLE 'python' process."""
        self.proc = self._proc(text)
        self.show(scene, self.proc, anims=[FadeIn(self.proc, scale=0.9)], run_time=run_time)

    def execvp(self, scene, text: str = "gunicorn", run_time: float = 0.9):
        """PLAYS: os.execvp: the process becomes gunicorn in the same box (same outline, same place)."""
        new = steady(text, 22, INK, mono_font=True).move_to(self.proc.text)
        scene.play(Indicate(self.proc.frame, color=TOOL, scale_factor=1.04), Transform(self.proc.text, new),
                   run_time=run_time)

    def envelope(self, scene, port: str = "8080", writer: str = "image", run_time: float = 1.0):
        """PLAYS: an envelope 'PORT=<port>' arrives over the process (writer 'image' TEAL 'image ENV',
        'cloud' BLUE 'Cloud Run', 'you' GREY 'you'), opens, and the PINK ear '0.0.0.0:<port>' grows on
        the container's left edge."""
        col, who = {"image": (IMAGE, "image ENV"), "cloud": (CLOUD, "Cloud Run"), "you": (YOU, "you")}[writer]
        env = envelope(f"PORT={port}", col).move_to(self.p(1.4, 0.95))
        wl = label(who, 20, col).next_to(env, RIGHT, buff=0.15)
        if self.env is not None:
            self.drop(scene, self.env, run_time=0.2)
        self.env = VGroup(env, wl)
        self.show(scene, self.env, anims=[FadeIn(env, shift=DOWN * 0.3), FadeIn(wl)], run_time=run_time * 0.5)
        e = ear(f"0.0.0.0:{port}", size=self.size)
        e.glyph.move_to([self.box.get_left()[0] + 0.12, self.ear_y, 0])
        e.text.next_to(e.glyph, DOWN, buff=0.12).align_to(self.box, LEFT).shift(RIGHT * 0.15)
        if self.ear_ is not None:
            self.drop(scene, self.ear_, run_time=0.2)
        self.ear_ = e
        wire = Line(e.glyph.get_right(), self.proc.frame.get_left(), color=ROUTE, stroke_width=3) \
            if self.proc is not None else VGroup()
        self.show(scene, e, wire, anims=[FadeIn(e, scale=0.6), Create(wire) if self.proc is not None else
                                         FadeIn(wire)], run_time=run_time * 0.5)
        self.wire = wire

    def threads(self, scene, n: int = 4, run_time: float = 0.6):
        """PLAYS: n thread slots appear in the process box (gunicorn --threads 4)."""
        sl = VGroup(*[Square(0.26, OWN) for _ in range(n)]).arrange(RIGHT, buff=0.1)
        sl.move_to(self.proc.frame).shift(DOWN * 0.27)
        self.slots = sl
        self.show(scene, sl, anims=[LaggedStart(*[FadeIn(s, scale=0.5) for s in sl], lag_ratio=0.2)],
                  run_time=run_time)

    def wall(self, scene, host: str = "8086", target: str = "8080", run_time: float = 1.0):
        """PLAYS: the GREY laptop wall (x -3.9) with a PINK door 'host' and a PINK pipe to the ear,
        labelled '-p host:target'."""
        wx = self.p(-3.9, 0)[0]
        w = Line([wx, self.ear_y + 1.4, 0], [wx, self.ear_y - 1.4, 0], color=LAPTOP, stroke_width=8)
        wl = label("laptop", 20, LAPTOP).next_to(w, UP, buff=0.1)
        door = Rectangle(width=0.22, height=0.5, stroke_width=0).set_fill(ROUTE, 0.9).move_to([wx, self.ear_y, 0])
        dl = mono(host, 20, ROUTE).next_to(door, LEFT, buff=0.12)
        end = self.ear_.glyph.get_left() if self.ear_ is not None else np.array([self.box.get_left()[0], self.ear_y, 0])
        pipe = Line(door.get_right(), end, color=ROUTE, stroke_width=5)
        pl = mono(f"-p {host}:{target}", 20, ROUTE).next_to(pipe, UP, buff=0.12)
        self.wall_, self.door, self.pipe, self.pipe_label = VGroup(w, wl), VGroup(door, dl), pipe, pl
        self.show(scene, self.wall_, self.door, run_time=run_time * 0.5)
        self.show(scene, pipe, pl, anims=[Create(pipe), FadeIn(pl)], run_time=run_time * 0.5)

    def knock(self, scene, port: str = "8080", ok: bool = False, run_time: float = 1.0):
        """PLAYS: a PINK knock from outside the laptop: ok=True goes through the door and the pipe to
        the ear; ok=False knocks on the wall at a spot labelled `port` and bounces RED 'refused'."""
        wx = self.wall_[0].get_center()[0]
        if ok:
            d = pulse_dot(r=0.11).move_to([wx - 0.9, self.ear_y, 0])
            self.show(scene, d, run_time=0.15)
            scene.play(d.animate.move_to(self.ear_.glyph), run_time=run_time * 0.7)
            self.drop(scene, d, run_time=0.2)
            return None
        y = self.ear_y - 0.85
        spot = mono(port, 20, ERR).move_to([wx - 0.55, y + 0.3, 0])
        d = pulse_dot(r=0.11).move_to([wx - 1.0, y, 0])
        self.show(scene, spot, d, run_time=0.2)
        scene.play(bounce(d, np.array([wx - 0.12, y, 0]), run_time=run_time * 0.6))
        ch = err_chip("refused", mono_font=False).next_to(spot, DOWN, buff=0.35)
        self.show(scene, ch, run_time=run_time * 0.2, extra=[d.animate.set_color(ERR)])
        return ch

    def move_ear(self, scene, port: str = "9090", run_time: float = 0.8):
        """PLAYS: PORT changes: the ear moves down and reads '0.0.0.0:<port>'; the pipe still ends at
        the old spot (a gap)."""
        dy = -0.75
        new_t = mono(f"0.0.0.0:{port}", self.size, ROUTE)
        new_t.move_to(self.ear_.text).shift(DOWN * 0.0)
        new_t.align_to(self.ear_.text, LEFT)
        scene.play(self.ear_.glyph.animate.shift(UP * dy), Transform(self.ear_.text, new_t.shift(UP * dy)),
                   run_time=run_time)
        if getattr(self, "wire", None) is not None and len(self.wire.get_points()):
            scene.play(self.wire.animate.put_start_and_end_on(self.ear_.glyph.get_right(),
                                                              self.proc.frame.get_left() + UP * dy * 0.5),
                       run_time=0.3)
        self.ear_dy = dy

    def repipe(self, scene, host: str = "8086", target: str = "9090", run_time: float = 0.8):
        """PLAYS: the pipe reattaches to the moved ear; its label reads '-p host:target'."""
        door = self.door[0]
        mid = np.array([self.box.get_left()[0] - 0.6, door.get_center()[1], 0])
        new = VMobject(stroke_color=ROUTE, stroke_width=5).set_points_as_corners(
            [door.get_right(), mid, [mid[0], self.ear_.glyph.get_center()[1], 0], self.ear_.glyph.get_left()])
        nl = mono(f"-p {host}:{target}", 20, ROUTE).move_to(self.pipe_label)
        old = self.pipe
        self.swap(scene, old, new, run_time=run_time, extra=[Transform(self.pipe_label, nl)])
        self.pipe = new

    def sigint(self, scene, run_time: float = 1.0):
        """PLAYS: Ctrl+C: a 'SIGINT' arrow goes straight into the process (the container's main
        process gets the signal) and the process folds away cleanly."""
        top = self.proc.frame.get_top()
        a = Arrow(top + UP * 0.9 + RIGHT * 1.6, top + RIGHT * 0.6, buff=0.05, color=INK, stroke_width=3,
                  tip_length=0.18)
        lab = mono("SIGINT", 20, INK).next_to(a.get_start(), UP, buff=0.08)
        self.show(scene, a, lab, anims=[GrowArrow(a), FadeIn(lab)], run_time=run_time * 0.4)
        parts = [self.proc] + ([self.slots] if self.slots is not None else [])
        self.drop(scene, *parts, a, lab, run_time=run_time * 0.6)
        self.proc = self.slots = None


# ------------------------------------------------------------------ V6 · IdentityDoors and friends
def _door(color=S.GREY, door_h: float = 0.75) -> VGroup:
    fr = Rectangle(width=0.4, height=door_h, stroke_color=color, stroke_width=3).set_fill(S.BG, 1)
    knob = Dot(fr.get_right() + LEFT * 0.09, radius=0.035, color=color)
    g = VGroup(fr, knob)
    g.frame = fr
    return g


class IdentityDoors(_Anchored):
    """V6 · who may call it (left door) and who it runs as (right door). Browser x -5.7; BLUE service
    box (5.4 x 2.4) centred (-0.6, 0.6); left door at its left edge, right door at its right edge;
    Agent Platform cloud (5.2, 1.4); the switch 'Allow public access' under the box (x -3.0, y -1.2);
    a badge hangs below the right door at (3.0, -1.0), its role chips under it.
    .browser .service .left_door .right_door .cloud .switch .badge_ (or None) .role_chips"""

    def __init__(self, name: str = SERVICE, public: bool = True, **kw):
        super().__init__(**kw)
        self.browser = browser_icon(1.0).move_to(self.p(-5.7, 0.45))
        sb = RoundedRectangle(width=5.4, height=2.4, corner_radius=0.14, stroke_color=CLOUD,
                              stroke_width=3).set_fill(CLOUD, 0.08).move_to(self.p(-0.6, 0.6))
        st = mono(name, 20, INK).move_to(sb.get_top() + DOWN * 0.3)
        self.service = VGroup(sb, st)
        self.service.frame = sb
        self.left_door = _door(S.GREY).move_to(sb.get_left())
        self.right_door = _door(S.GREY).move_to(sb.get_right())
        self.ll = label("who may call it", 20, INK).next_to(self.left_door, RIGHT, buff=0.2).shift(DOWN * 0.55)
        self.rl = VGroup(label("who it is when", 20, INK), label("it calls out", 20, INK)).arrange(DOWN, buff=0.06)
        self.rl.next_to(self.right_door, LEFT, buff=0.2).shift(DOWN * 0.6)
        self.cloud = cloud_shape("Agent Platform", CLOUD, 2.5).move_to(self.p(5.2, 1.4))
        self.switch = Switch("Allow public access", on=public).move_to(self.p(-3.0, -1.2))
        self.badge_ = self.default_ = None
        self.role_chips = []
        self.add(self.browser, self.service, self.left_door, self.right_door, self.ll, self.rl, self.cloud,
                 self.switch)

    def call(self, scene, allowed: bool = True, run_time: float = 1.0):
        """PLAYS: a PINK request from the browser to the left door: it passes in (allowed) or bounces
        back RED with a RED '403' chip by the door. Returns the chip (or None)."""
        d = pulse_dot(r=0.11).move_to(self.browser.window.get_right() + RIGHT * 0.15)
        self.show(scene, d, run_time=0.15)
        door = self.left_door.frame.get_center()
        if allowed:
            scene.play(d.animate.move_to(door + RIGHT * 0.9), run_time=run_time * 0.7)
            self.drop(scene, d, run_time=0.2)
            return None
        scene.play(bounce(d, door + LEFT * 0.25, run_time=run_time * 0.6))
        ch = err_chip("403").next_to(self.left_door, UP, buff=0.25).shift(LEFT * 0.5)
        self.show(scene, ch, run_time=run_time * 0.2, extra=[d.animate.set_color(ERR)])
        self.drop(scene, d, run_time=0.2)
        return ch

    def set_public(self, scene, on: bool, run_time: float = 0.5):
        """PLAYS: the 'Allow public access' switch flips."""
        self._ensure(scene)
        scene.play(self.switch.flip(on), run_time=run_time)

    def call_out(self, scene, ok: bool = False, run_time: float = 1.0):
        """PLAYS: a PINK call leaves through the right door toward Agent Platform: ok=True reaches the
        cloud; ok=False stops at the door, RED, with a RED cross. Returns the arrow."""
        start = self.right_door.frame.get_center() + LEFT * 0.6
        end = self.cloud.get_left() + RIGHT * 0.1 if ok else self.right_door.frame.get_center()
        a = Arrow(start, end, buff=0, color=ROUTE if ok else ERR, stroke_width=4, tip_length=0.2,
                  max_tip_length_to_length_ratio=0.4)
        new = [a]
        if not ok:
            new.append(cross_glyph(0.3).next_to(self.right_door, RIGHT, buff=0.12))
        self.show(scene, *new, anims=[GrowArrow(a)] + [FadeIn(m) for m in new[1:]], run_time=run_time)
        self.out_arrow = VGroup(*new)
        return self.out_arrow

    def _badge_spot(self, b):
        return b.move_to(self.p(3.0, -1.0))

    def default_badge(self, scene, run_time: float = 0.6):
        """PLAYS: a dashed ORANGE badge 'default compute account' hangs below the right door."""
        b = badge("default compute account", SHARED, dashed=True, mono_font=False)
        self._badge_spot(b)
        hook = DashedLine(self.right_door.frame.get_bottom(), b.get_top(), color=SHARED, stroke_width=2)
        self.default_ = VGroup(b, hook)
        self.show(scene, self.default_, run_time=run_time)

    def add_badge(self, scene, name: str = RUNTIME_SA, run_time: float = 0.7):
        """PLAYS: the BLUE runtime badge forms at the badge spot (not yet pinned: no hook line)."""
        b = self._badge_spot(badge(name))
        self.badge_ = b
        anims = [FadeIn(b, scale=0.8)]
        if self.default_ is not None:
            self.drop(scene, self.default_, run_time=0.3)
            self.default_ = None
        self.show(scene, b, anims=anims, run_time=run_time)

    def pin_badge(self, scene, run_time: float = 0.6):
        """PLAYS: the badge pins onto the right door (a BLUE hook line; the door turns BLUE)."""
        hook = Line(self.right_door.frame.get_bottom(), self.badge_.get_top(), color=CLOUD, stroke_width=3)
        self.hook = hook
        self.show(scene, hook, anims=[Create(hook)], run_time=run_time,
                  extra=[self.right_door.frame.animate.set_stroke(CLOUD)])

    def roles(self, scene, *texts, color=SHARED, run_time: float = 0.8):
        """PLAYS: role chips hang under the badge (ORANGE: project-wide). Returns them."""
        base = self.badge_ if self.badge_ is not None else self.default_
        chips = []
        y = (self.role_chips[-1] if self.role_chips else base).get_bottom()[1] - 0.12
        for t in texts:
            c = chip(t, color, size=20)
            c.move_to([base.get_center()[0], y - c.height / 2, 0])
            if c.get_right()[0] > SAFE_X:
                c.shift(LEFT * (c.get_right()[0] - SAFE_X))
            y -= c.height + 0.1
            chips.append(c)
        self.role_chips += chips
        self.show(scene, *chips, anims=[LaggedStart(*[FadeIn(c, shift=DOWN * 0.15) for c in chips], lag_ratio=0.3)],
                  run_time=run_time)
        return chips

    def no_key(self, scene, run_time: float = 0.7):
        """PLAYS: a dashed GOLD key, crossed out RED, above the badge's right end ('no key file')."""
        k = crossed_key(0.7)
        k.move_to([min(self.badge_.get_right()[0] + 0.55, SAFE_X - 0.4), self.badge_.get_top()[1] + 0.45, 0])
        self.show(scene, k.key, run_time=run_time * 0.5)
        self.show(scene, k.cross, anims=[Create(k.cross)], run_time=run_time * 0.5)
        return k

    def you(self, scene, text: str = "Service Account User", run_time: float = 0.8):
        """PLAYS: a GREY 'you' figure (bottom left) and a thin GREY arrow to the badge, labelled."""
        y_ = you().move_to(self.p(-5.6, -2.4))
        tgt = self.badge_ if self.badge_ is not None else self.right_door
        a = arrow(y_.figure.get_right(), tgt.get_left(), S.GREY, stroke=2.5, buff=0.1)
        lab = label(text, 20, S.GREY).next_to(a.get_center(), DOWN, buff=0.12)
        self.you_ = VGroup(y_, a, lab)
        self.show(scene, y_, run_time=run_time * 0.4)
        self.show(scene, a, lab, anims=[GrowArrow(a), FadeIn(lab)], run_time=run_time * 0.6)
        return self.you_

    def token(self, scene, run_time: float = 0.9):
        """PLAYS: the badge hands a short-lived ticket (never a key) up to the outbound call."""
        t = ticket().move_to(self.badge_.get_top() + UP * 0.2)
        self.show(scene, t, anims=[FadeIn(t, scale=0.5)], run_time=0.2)
        scene.play(t.animate.move_to(self.right_door.frame.get_right() + RIGHT * 0.45 + UP * 0.35),
                   run_time=run_time)
        self.ticket_ = t
        return t


class ImpersonationRibbon(_Anchored):
    """V6 · S11's impersonation ribbon: 'you' (x -5.4, y 1.0) signs in, a PINK ribbon 'Token Creator'
    runs to the BLUE runtime badge (x 3.4, y 1.0); short-lived tickets flow back and drop an 'ADC file'
    on the GREY laptop disk (x -4.8, y -1.7). .you_ .badge_ .disk_ .ribbon_ .file_"""

    def __init__(self, name: str = RUNTIME_SA, **kw):
        super().__init__(**kw)
        self.you_ = you().move_to(self.p(-5.4, 1.0))
        self.badge_ = badge(name).move_to(self.p(3.4, 1.0))
        dk = disk(0.6).move_to(self.p(-4.8, -1.6))
        self.disk_ = VGroup(dk, label("your laptop", 20, LAPTOP).next_to(dk, DOWN, buff=0.12))
        self.add(self.you_, self.badge_, self.disk_)
        self.ribbon_ = self.file_ = None

    def sign_in(self, scene, text: str = "your Google account", run_time: float = 0.6):
        """PLAYS: a GREY card beside 'you'."""
        c = grey_chip(text).next_to(self.you_, UP, buff=0.15)
        self.show(scene, c, run_time=run_time)
        return c

    def ribbon(self, scene, text: str = "Token Creator", run_time: float = 1.0):
        """PLAYS: the PINK ribbon from you to the badge, labelled."""
        a = Line(self.you_.figure.get_right() + RIGHT * 0.15, self.badge_.get_left() + LEFT * 0.1,
                 color=ROUTE, stroke_width=6)
        lab = label(text, 22, ROUTE).next_to(a, UP, buff=0.12)
        self.ribbon_ = VGroup(a, lab)
        self.show(scene, a, lab, anims=[Create(a), FadeIn(lab)], run_time=run_time)

    def tickets(self, scene, n: int = 3, run_time: float = 1.4):
        """PLAYS: n short-lived tickets flow back along the ribbon and down to the laptop disk."""
        line = self.ribbon_[0]
        ts = [ticket(CLOUD).move_to(line.get_end()) for _ in range(n)]
        self.show(scene, *ts, run_time=0.2)
        scene.play(LaggedStart(*[Succession(t.animate(run_time=run_time * 0.4).move_to(line.get_start()),
                                            t.animate(run_time=run_time * 0.3).move_to(self.disk_[0].get_top() + UP * 0.2))
                                 for t in ts], lag_ratio=0.25), run_time=run_time)
        self.drop(scene, *ts, run_time=0.3)

    def adc_file(self, scene, run_time: float = 0.6):
        """PLAYS: an 'ADC file' card lands beside the laptop disk."""
        f = file_card("ADC file", LAPTOP).next_to(self.disk_[0], RIGHT, buff=0.4)
        self.file_ = f
        self.show(scene, f, anims=[FadeIn(f, shift=DOWN * 0.3)], run_time=run_time)
        return f

    def empty_slot(self, scene, text: str = "no ADC file", run_time: float = 0.6):
        """PLAYS: the ADC file slot beside the disk is empty (a dashed outline + GREY label)."""
        if self.file_ is not None:
            self.drop(scene, self.file_, run_time=0.3)
            self.file_ = None
        ref = file_card("ADC file", LAPTOP)
        ob = outline_box(ref.width, ref.height, S.GREY, solid=False).next_to(self.disk_[0], RIGHT, buff=0.4)
        lab = label(text, 20, S.GREY).move_to(ob)
        self.show(scene, ob, lab, run_time=run_time)
        return VGroup(ob, lab)

    def no_key(self, scene, text: str = "no private key downloaded", run_time: float = 0.8):
        """PLAYS: a dashed GOLD key crossed out under the badge, labelled."""
        k = crossed_key(0.7).next_to(self.badge_, DOWN, buff=0.45)
        lab = label(text, 20, COST).next_to(k, DOWN, buff=0.12)
        self.show(scene, k, lab, run_time=run_time)
        return VGroup(k, lab)


class BadgeBoard(_Anchored):
    """V6 · S13's badges: the web badge (x -3.2, y 1.7) with its two ORANGE project roles, then the
    job badge (x -3.2, y -0.6) with the same two; input / output buckets on the right (x 3.6, y 1.1 /
    -1.5) take GREEN bucket-scoped grants. .web .job (or None) .buckets {'input', 'output'}"""

    ROLES = ("Agent Platform User", "Service Usage Consumer")

    def __init__(self, **kw):
        super().__init__(**kw)
        self.web = self._badge_with_roles(RUNTIME_SA, self.p(-3.2, 1.7))
        bi = bucket(IN_BUCKET, 0.9).move_to(self.p(3.6, 1.1))
        bo = bucket(OUT_BUCKET, 0.9).move_to(self.p(3.6, -1.5))
        self.buckets = {"input": bi, "output": bo}
        self.job = None
        self.grants = {}
        self.add(self.web, bi, bo)

    def _badge_with_roles(self, name, at):
        b = badge(name).move_to(at)
        cs = VGroup(*[chip(r, SHARED, size=20) for r in self.ROLES]).arrange(RIGHT, buff=0.12)
        cs.next_to(b, DOWN, buff=0.12)
        g = VGroup(b, cs)
        g.badge, g.roles = b, cs
        return g

    def job_badge(self, scene, run_time: float = 0.8):
        """PLAYS: the job's badge forms with the same two ORANGE project roles."""
        self.job = self._badge_with_roles(JOB_SA, self.p(-3.2, -0.6))
        self.show(scene, self.job, anims=[FadeIn(self.job.badge, scale=0.8),
                                          LaggedStart(*[FadeIn(c, shift=DOWN * 0.15) for c in self.job.roles],
                                                      lag_ratio=0.3)], run_time=run_time)

    def grant(self, scene, which: str = "input", run_time: float = 0.8):
        """PLAYS: a GREEN bucket-scoped grant from the job badge to one bucket: 'Viewer → input' or
        'Creator → output', tied to that bucket only."""
        text = {"input": "Viewer → input", "output": "Creator → output"}[which]
        bk = self.buckets[which]
        src = self.job.badge.get_right()
        line = Line(src, bk.pail.get_left(), color=OWN, stroke_width=3)
        ch = chip(text, OWN, size=20).move_to(line.get_center()).shift(UP * 0.3 if which == "input" else DOWN * 0.3)
        self.grants[which] = VGroup(line, ch)
        self.show(scene, line, ch, anims=[Create(line), FadeIn(ch)], run_time=run_time)
        return ch

    def web_note(self, scene, text: str = "no bucket chip · its audio goes straight to the browser",
                 run_time: float = 0.5):
        """PLAYS: a GREY chip under the web badge's roles."""
        c = grey_chip(text).next_to(self.web.roles, DOWN, buff=0.12).align_to(self.web.roles, LEFT)
        self.show(scene, c, run_time=run_time)
        return c


# ------------------------------------------------------------------ V7 · LifecycleStrips
class LifecycleStrips(_Anchored):
    """V7 · one image, two programs. A TEAL image block (x -4.9, y 2.0) with two startup commands:
    'serve' on the service strip (y 0.6) and 'batch' on the job strip (y -1.0); strips run x -2.2 ..
    5.4. Service: an instance with a PINK ear, pulses, no right edge. Job: four segments (take input
    → translate → speak → save), a hard right edge 'exit 0' (or RED 'exit 1'); no ear, no URL.
    .image .serve_strip .job_strip (.inst .segs .edge .exit_label .disk) .wall (after endless())"""

    SY, JY = 0.6, -1.0
    X0, X1 = -2.2, 5.4

    def __init__(self, steps=JOB_STEPS, show=("service", "job"), **kw):
        super().__init__(**kw)
        self.image = image_block("image", 2.0, 0.7).move_to(self.p(-4.9, 2.0))
        self.add(self.image)
        cs = mono("serve", 20, IMAGE).move_to(self.p(-4.9, self.SY))
        cb = mono("batch", 20, IMAGE).move_to(self.p(-4.9, self.JY))
        sx = cs.get_left()[0] - 0.3
        hang = VGroup(Line([sx, self.image.get_bottom()[1], 0], [sx, cb.get_center()[1], 0], color=IMAGE,
                           stroke_width=2),
                      Line([sx, cs.get_center()[1], 0], cs.get_left() + LEFT * 0.08, color=IMAGE, stroke_width=2),
                      Line([sx, cb.get_center()[1], 0], cb.get_left() + LEFT * 0.08, color=IMAGE, stroke_width=2))
        self.cmds = VGroup(cs, cb)
        # service strip
        si = instance(1.0, 0.62).move_to(self.p(self.X0 - 0.75, self.SY))
        se = ear(None).move_to(si.get_left() + LEFT * 0.12)
        sline = Line(self.p(self.X0, self.SY), self.p(self.X1, self.SY), color=S.GREY, stroke_width=3)
        fade = VGroup(*[Dot(self.p(self.X1 + 0.25 + 0.22 * k, self.SY), radius=0.04, color=S.GREY)
                        for k in range(3)])
        self.serve_strip = VGroup(si, se, sline, fade)
        self.serve_strip.inst, self.serve_strip.ear, self.serve_strip.line = si, se, sline
        # job strip
        ji = instance(1.0, 0.62).move_to(self.p(self.X0 - 0.75, self.JY))
        dk = disk(0.3).move_to(ji.get_corner(DR) + np.array([-0.1, 0.2, 0]))
        n = len(steps)
        sw = (self.X1 - self.X0 - 0.1 * (n - 1)) / n
        segs = VGroup()
        for k, s in enumerate(steps):
            r = RoundedRectangle(width=sw, height=0.55, corner_radius=0.08, stroke_color=S.GREY,
                                 stroke_width=2).set_fill(S.BG, 1)
            r.move_to(self.p(self.X0 + sw / 2 + k * (sw + 0.1), self.JY))
            t = label(s, 20, S.GREY).move_to(r)
            seg = VGroup(r, t)
            seg.frame, seg.text = r, t
            segs.add(seg)
        edge = Line(self.p(self.X1 + 0.15, self.JY + 0.45), self.p(self.X1 + 0.15, self.JY - 0.45), color=INK,
                    stroke_width=6)
        el = mono("exit 0", 20, INK).next_to(edge, DOWN, buff=0.12)
        self.job_strip = VGroup(ji, dk, segs, edge, el)
        self.job_strip.inst, self.job_strip.disk, self.job_strip.segs = ji, dk, segs
        self.job_strip.edge, self.job_strip.exit_label = edge, el
        self.wall = None
        parts = [self.cmds]
        if "service" in show:
            parts.append(self.serve_strip)
        if "job" in show:
            parts.append(self.job_strip)
        self.hang = hang
        self.add(*parts, hang)

    def show_strip(self, scene, which: str = "job", run_time: float = 0.8):
        """PLAYS: a strip that was left out (show=...) appears."""
        m = self.job_strip if which == "job" else self.serve_strip
        self.show(scene, m, run_time=run_time)

    def serve(self, scene, n: int = 4, run_time: float = 2.0):
        """PLAYS: PINK pulses enter the service strip's ear and travel along it (answered), on and on."""
        st = self.serve_strip
        dots = [pulse_dot().move_to(st.ear.get_left() + LEFT * 0.2) for _ in range(n)]
        self.show(scene, *dots, run_time=0.1)
        scene.play(LaggedStart(*[d.animate(rate_func=linear).move_to(st.line.get_end()) for d in dots],
                               lag_ratio=0.3), run_time=run_time)
        self.drop(scene, *dots, run_time=0.2)

    def run_job(self, scene, fail_at: int | None = None, run_time: float = 2.0):
        """PLAYS: the job's segments light one by one (TEAL) and it reaches its edge: 'exit 0'. With
        fail_at=k, segment k turns RED, the rest stay dark, and the edge reads 'exit 1' (RED)."""
        segs = self.job_strip.segs
        n = len(segs) if fail_at is None else fail_at + 1
        anims = []
        for k in range(n):
            bad = fail_at is not None and k == fail_at
            col = ERR if bad else IMAGE
            anims.append(AnimationGroup(segs[k].frame.animate.set_stroke(col).set_fill(col, 0.25),
                                        segs[k].text.animate.set_color(INK)))
        self._ensure(scene)
        scene.play(LaggedStart(*anims, lag_ratio=0.8), run_time=run_time)
        self.set_exit(scene, 0 if fail_at is None else 1)

    def set_exit(self, scene, code_: int = 0, run_time: float = 0.5):
        """PLAYS: the edge reads 'exit 0' (WHITE) or 'exit 1' (RED)."""
        col = INK if code_ == 0 else ERR
        new = mono(f"exit {code_}", 20, col).move_to(self.job_strip.exit_label)
        scene.play(Transform(self.job_strip.exit_label, new), self.job_strip.edge.animate.set_color(col),
                   run_time=run_time)

    def reset_job(self, scene, run_time: float = 0.4):
        """PLAYS: the segments go dark again (GREY)."""
        scene.play(*[AnimationGroup(s.frame.animate.set_stroke(S.GREY).set_fill(S.BG, 1),
                                    s.text.animate.set_color(S.GREY)) for s in self.job_strip.segs],
                   run_time=run_time)

    def endless(self, scene, text: str = "task timeout 5 min", run_time: float = 2.4):
        """PLAYS (S13): both slots at the image default: the job strip grows an ear, its segments go,
        a band runs on and never reaches the edge, and hits a RED wall 'task timeout 5 min'."""
        js = self.job_strip
        e = ear(None).move_to(js.inst.get_left() + LEFT * 0.12)
        self.drop(scene, js.segs, js.edge, js.exit_label, run_time=0.4)
        wx = self.X1 - 0.3
        wall = Line(self.p(wx, self.JY + 0.6), self.p(wx, self.JY - 0.6), color=ERR, stroke_width=8)
        wl = label(text, 20, ERR).next_to(wall, DOWN, buff=0.12)
        band = Line(self.p(self.X0, self.JY), self.p(wx - 0.1, self.JY), color=IMAGE, stroke_width=6)
        self.show(scene, e, wall, wl, run_time=0.5)
        self.show(scene, band, anims=[Create(band, rate_func=linear)], run_time=run_time - 0.9)
        self.wall = VGroup(wall, wl, band, e)
        return self.wall

    def buckets(self, scene, run_time: float = 1.2):
        """PLAYS: a BLUE input bucket under the job's instance feeds a PINK 'gs://… in' arrow into it;
        a BLUE output bucket under the edge receives three file icons."""
        js = self.job_strip
        bi = bucket(None, 0.8).move_to(js.inst.get_center() + DOWN * 1.55)
        ai = Arrow(bi.get_top(), js.inst.get_bottom(), buff=0.08, color=ROUTE, stroke_width=4, tip_length=0.18)
        li = mono("gs://…", 20, ROUTE).next_to(ai, RIGHT, buff=0.12)
        bo = bucket(None, 0.8).move_to([js.edge.get_center()[0] - 0.6, bi.get_center()[1], 0])
        files = VGroup(*[file_glyph(0.3, INK) for _ in range(3)]).arrange(RIGHT, buff=0.08).next_to(bo, LEFT, buff=0.2)
        self.show(scene, bi, ai, li, bo, run_time=run_time * 0.5)
        self.show(scene, files, anims=[LaggedStart(*[FadeIn(f, shift=DOWN * 0.3) for f in files], lag_ratio=0.3)],
                  run_time=run_time * 0.5)
        self.io = VGroup(bi, ai, li, bo, files)
        return self.io

    def disk_gone(self, scene, text: str = "local disk gone", run_time: float = 0.6):
        """PLAYS: the job instance's little disk vanishes (at exit), a GREY chip says so."""
        ch = grey_chip(text).next_to(self.job_strip.inst, UP, buff=0.12)
        self.drop(scene, self.job_strip.disk, run_time=run_time * 0.5)
        self.show(scene, ch, run_time=run_time * 0.5)
        return ch


# ------------------------------------------------------------------ V8 · AttemptFolders
class AttemptFolders(_Anchored):
    """V8 · a result you can prove. The BLUE output bucket (9.6 x 4.2, centred) titled
    YOUR_OUTPUT_BUCKET, a PINK prefix tab 'run-001/' (yours, from the arguments); attempt folders
    drop in as columns (x -3.0, 0.3, 3.4 of the layout), each with its files and, when complete, the
    GREEN receipt. .frame .tabs .attempts (list of VGroups: .folder .name .files .receipt)"""

    COLS = (-3.0, 0.3, 3.4)
    FILES = ("translated.txt", "speech.wav", "manifest.json")

    def __init__(self, prefix: str = "run-001/", bucket_name: str = OUT_BUCKET, **kw):
        super().__init__(**kw)
        self.frame = outline_box(9.6, 4.2, CLOUD, solid=True, fill_opacity=0.06).move_to(self.p(0, 0))
        hd = VGroup(bucket(None, 0.45), mono(bucket_name, 20, INK)).arrange(RIGHT, buff=0.15)
        hd.move_to(self.frame.get_corner(UL) + np.array([hd.width / 2 + 0.3, -0.35, 0]))
        self.head = hd
        self.tabs = VGroup()
        self.add(self.frame, hd, self.tabs)
        self.attempts = []
        self._tab(prefix, add=True)

    def _tab(self, text, add=False):
        t = mono(text, 20, ROUTE)
        b = RoundedRectangle(width=t.width + 0.4, height=0.42, corner_radius=0.08, stroke_color=ROUTE,
                             stroke_width=2).set_fill(S.BG, 1)
        t.move_to(b)
        tab = VGroup(b, t)
        tab.box, tab.text = b, t
        x = (self.tabs.get_right()[0] + 0.15 + tab.width / 2) if len(self.tabs) else \
            self.frame.get_left()[0] + 0.3 + tab.width / 2
        tab.move_to([x, self.frame.get_top()[1] - 0.95, 0])
        if add:
            self.tabs.add(tab)
        return tab

    def prefix(self, scene, text: str, run_time: float = 0.6):
        """PLAYS: another prefix tab appears beside the others (S15: 'run-<timestamp>-<hex>/')."""
        tab = self._tab(text)
        self.show(scene, tab, anims=[FadeIn(tab, shift=DOWN * 0.2)], run_time=run_time, into=self.tabs)
        return tab

    def attempt(self, scene, name: str = ATTEMPT + "/", run_time: float = 0.7):
        """PLAYS: a new attempt folder drops into the next column. Returns it (.folder .name)."""
        i = len(self.attempts)
        if i >= len(self.COLS):
            raise ValueError("AttemptFolders: three attempt columns at most")
        fg = folder_glyph(0.42, CLOUD)
        nm = mono(name, 20, INK).next_to(fg, RIGHT, buff=0.12)
        col = VGroup(fg, nm)
        col.move_to(self.p(self.COLS[i], 0.55))
        col.folder, col.name, col.files, col.receipt = fg, nm, VGroup(), None
        self.attempts.append(col)
        self.show(scene, col, anims=[FadeIn(col, shift=DOWN * 0.5)], run_time=run_time)
        return col

    def files(self, scene, i: int = -1, fail_after: int | None = None, run_time: float = 2.0):
        """PLAYS: the files land in attempt i in the program's order: translated.txt, speech.wav (each
        with a GREEN 'create only' lock tick), then manifest.json LAST with the GREEN receipt
        'complete'. fail_after=2: only the first two land, no receipt; the folder turns RED and a RED
        label says 'not a success'."""
        col = self.attempts[i]
        names = self.FILES if fail_after is None else self.FILES[:fail_after]
        x0 = col.folder.get_left()[0] + 0.15
        y = col.folder.get_bottom()[1] - 0.35
        rows = []
        for k, nm in enumerate(names):
            fi = file_icon(nm, OWN if nm == "manifest.json" else INK)
            fi.move_to([x0 + fi.width / 2, y - 0.5 * k, 0])
            tick = check_glyph(0.22, OWN, 4).next_to(fi, RIGHT, buff=0.1)
            row = VGroup(fi, tick)
            rows.append(row)
        for row in rows:
            self.show(scene, row, anims=[FadeIn(row, shift=DOWN * 0.3)], run_time=run_time / (len(rows) + 1),
                      into=col.files)
        if col.files not in col.submobjects:
            col.add(col.files)
        if fail_after is None:
            rc = receipt().next_to(col.files, DOWN, buff=0.15).align_to(col.files, LEFT)
            col.receipt = rc
            self.show(scene, rc, anims=[FadeIn(rc, scale=1.3)], run_time=run_time / (len(rows) + 1), into=col)
        else:
            bad = label("not a success", 20, ERR).next_to(col.files, DOWN, buff=0.15).align_to(col.files, LEFT)
            col.bad = bad
            self.show(scene, bad, run_time=run_time / (len(rows) + 1), into=col,
                      extra=[col.folder.animate.set_color(ERR)])
        return col

    def clear(self, scene, i: int = -1, run_time: float = 0.4):
        """PLAYS: empty attempt i's column again (files, receipt, RED marks) for a replay."""
        col = self.attempts[i]
        gone = list(col.files.submobjects) + [m for m in (col.receipt, getattr(col, "bad", None)) if m is not None]
        self.drop(scene, *gone, run_time=run_time, extra=[col.folder.animate.set_color(CLOUD)])
        col.receipt = None
        col.bad = None

    def shield(self, scene, i: int = 0, text: str = "create only", run_time: float = 0.6):
        """PLAYS: a GREEN shield over attempt i's files with a chip (nothing overwrites them)."""
        col = self.attempts[i]
        sh = Polygon([0, 0.25, 0], [0.22, 0.15, 0], [0.18, -0.15, 0], [0, -0.28, 0], [-0.18, -0.15, 0],
                     [-0.22, 0.15, 0], stroke_color=OWN, stroke_width=3).set_fill(OWN, 0.25)
        sh.next_to(col.folder, LEFT, buff=0.15)
        ch = ok_chip(text).next_to(col, DOWN, buff=0.15)
        self.show(scene, sh, ch, run_time=run_time)
        return VGroup(sh, ch)

    def flash_receipt(self, scene, i: int = -1, run_time: float = 0.8):
        """PLAYS: attempt i's receipt flashes (the helper found a complete manifest)."""
        rc = self.attempts[i].receipt
        flash_tag(scene, rc, OWN, run_time=run_time)


# ------------------------------------------------------------------ WhereToLook, TranslatePage
class WhereToLook(VGroup):
    """The 'where do you look?' card (slide 16's limited control and debugging): a title and three
    numbered slots (5.6 wide). fill(scene, i, text) PLAYS; glow(i) ANIM. .slots .texts"""

    def __init__(self, card_w: float = 5.6, title: str = "where do you look?", **kw):
        super().__init__(**kw)
        tt = label(title, 22, INK)
        rows = VGroup()
        for k in range(3):
            n = VGroup(Circle(radius=0.17, stroke_color=S.GREY, stroke_width=2),
                       label(str(k + 1), 20, S.GREY))
            n[1].move_to(n[0])
            sl = outline_box(card_w - 1.0, 0.46, S.GREY, solid=False)
            r = VGroup(n, sl).arrange(RIGHT, buff=0.2)
            rows.add(r)
        rows.arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        inner = VGroup(tt, rows).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        fr = box(card_w, inner.height + 0.5, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
        inner.move_to(fr)
        self.frame, self.title, self.rows = fr, tt, rows
        self.slots = [r[1] for r in rows]
        self.texts = [None, None, None]
        self.add(fr, inner)

    def fill(self, scene, i: int, text: str, color=INK, run_time: float = 0.6):
        t = label(text, 20, color).move_to(self.slots[i]).align_to(self.slots[i], LEFT).shift(RIGHT * 0.2)
        if t.width > self.slots[i].width - 0.3:
            raise ValueError(f"WhereToLook.fill(): {text!r} is too long for a slot")
        if self not in scene.mobjects:
            scene.add(self)
        scene.play(FadeIn(t, shift=RIGHT * 0.15), self.slots[i].frame.animate.set_stroke(TURN), run_time=run_time)
        scene.remove(t)
        self.add(t)
        self.texts[i] = t
        return t

    def glow(self, i: int, color=TURN):
        return Indicate(self.rows[i], color=color, scale_factor=1.04)


class TranslatePage(_Anchored):
    """The drawn translation page (laptop/11; tag it illustration): a window (8.0 x 4.0) with its
    address (mono 20, never scaled), title 'Translate · AC215', two text boxes, the src / dest
    selectors, a Translate button and the speech button ('Play audio · enable in part 3', GREY,
    disabled; speech=True: 'Play audio'). .url .left .right .src .dest .translate_btn .audio_btn"""

    def __init__(self, url: str = LOCAL_URL, url_color=ROUTE, speech: bool = False, page_w: float = 8.0,
                 **kw):
        super().__init__(**kw)
        u = mono(url, 20, url_color)
        w = max(page_w, u.width + 1.6)
        h = 4.0
        fr = RoundedRectangle(width=w, height=h, corner_radius=0.14, stroke_color=S.GREY_DARK,
                              stroke_width=2).set_fill(PANEL, 1).move_to(self.p(0, 0))
        bar = Line(fr.get_corner(UL) + DOWN * 0.5, fr.get_corner(UR) + DOWN * 0.5, color=S.GREY_DARK, stroke_width=2)
        dots = VGroup(*[Dot(radius=0.05, color=S.GREY_DARK) for _ in range(3)]).arrange(RIGHT, buff=0.09)
        dots.move_to(fr.get_corner(UL) + np.array([0.35, -0.25, 0]))
        u.move_to(fr.get_top() + DOWN * 0.25).align_to(dots, LEFT).shift(RIGHT * 0.55)
        self.url = u
        title = label("Translate · AC215", 24, INK).move_to(fr.get_top() + DOWN * 0.95)
        bw = (w - 1.0) / 2
        lb = RoundedRectangle(width=bw, height=0.9, corner_radius=0.08, stroke_color=S.GREY,
                              stroke_width=2).set_fill(TERM_BG, 1)
        rb = lb.copy()
        VGroup(lb, rb).arrange(RIGHT, buff=0.3).move_to(fr).shift(UP * 0.05)
        self.src = self._sel("en").next_to(lb, DOWN, buff=0.15).align_to(lb, LEFT)
        self.dest = self._sel("es").next_to(rb, DOWN, buff=0.15).align_to(rb, LEFT)
        tb = self._btn("Translate", CLOUD, INK)
        ab = self._btn("Play audio" if speech else "Play audio · enable in part 3",
                       CLOUD if speech else S.GREY_DARK, INK if speech else S.GREY)
        VGroup(tb, ab).arrange(RIGHT, buff=0.3).next_to(VGroup(self.src, self.dest), DOWN, buff=0.25)
        VGroup(tb, ab).align_to(lb, LEFT)
        self.frame, self.left, self.right, self.translate_btn, self.audio_btn = fr, lb, rb, tb, ab
        self.left_text = self.right_text = None
        self.add(fr, bar, dots, u, title, lb, rb, self.src, self.dest, tb, ab)

    @staticmethod
    def _sel(code_: str) -> VGroup:
        t = mono(code_, 20, INK)
        b = RoundedRectangle(width=max(0.9, t.width + 0.5), height=0.42, corner_radius=0.06, stroke_color=S.GREY,
                             stroke_width=2).set_fill(S.BG, 1)
        t.move_to(b).align_to(b, LEFT).shift(RIGHT * 0.15)
        g = VGroup(b, t)
        g.box, g.text = b, t
        return g

    @staticmethod
    def _btn(text, color, tcolor) -> VGroup:
        t = label(text, 20, tcolor)
        b = RoundedRectangle(width=t.width + 0.4, height=0.48, corner_radius=0.08, stroke_color=color,
                             stroke_width=2.5).set_fill(color, 0.15)
        t.move_to(b)
        g = VGroup(b, t)
        g.box, g.text = b, t
        return g

    def _boxtext(self, box_, text):
        t = label(text, 20, INK)
        if t.width > box_.width - 0.3:
            rows = soft([text], max(8, int(len(text) * (box_.width - 0.3) / t.width)))
            t = VGroup(*[label(s, 20, INK) for s in rows]).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        return t.move_to(box_).align_to(box_, LEFT).shift(RIGHT * 0.15)

    def type_in(self, scene, text: str = "Good afternoon everyone", run_time: float = 1.2):
        """PLAYS: text types into the left box."""
        t = self._boxtext(self.left, text)
        self.left_text = t
        self.show(scene, t, anims=[ShowIncreasingSubsets(t, rate_func=linear)], run_time=run_time)

    def set_dest(self, scene, code_: str = "fr", run_time: float = 0.5):
        """PLAYS: the right selector flips to `code_`."""
        new = self._sel(code_).move_to(self.dest)
        self.swap(scene, self.dest, new, run_time=run_time)
        self.dest = new

    def press(self, which: str = "translate", color=TURN):
        """ANIM: a button pulses ('translate' or 'audio')."""
        b = self.translate_btn if which == "translate" else self.audio_btn
        return Indicate(b.text, color=color, scale_factor=1.12)

    def translate(self, scene, answer: str = "Bonjour à tous", run_time: float = 1.0):
        """PLAYS: Translate pulses and the answer fills the right box."""
        t = self._boxtext(self.right, answer)
        if self.right_text is not None:
            self.drop(scene, self.right_text, run_time=0.2)
        self.right_text = t
        self._ensure(scene)
        scene.play(self.press("translate"), run_time=run_time * 0.4)
        self.show(scene, t, run_time=run_time * 0.6)

    def enable_speech(self, scene, run_time: float = 0.6):
        """PLAYS: the page reloads with speech on: the button reads 'Play audio' (BLUE)."""
        new = self._btn("Play audio", CLOUD, INK).move_to(self.audio_btn, aligned_edge=LEFT)
        self.swap(scene, self.audio_btn, new, run_time=run_time)
        self.audio_btn = new
