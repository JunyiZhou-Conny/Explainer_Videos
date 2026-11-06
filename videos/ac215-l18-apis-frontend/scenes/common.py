"""Shared scene code for AC215 L18 (APIs and frontend: follow-along of dlops-io/cheese-app-v1 @ ce03a10
and dlops-io/cheese-app-v2 @ 447b5c3 = main today, with Tutorial 24 from branch 2025 = 14f2a14 and
"Production images" from e98fa55's README).

Paths, narration (SAY lines straight from script.md), the semantic colours of BRIEF.md, the running
example (placeholders only), the twelve README trackers, loaders for the real captures in
assets/terminal/laptop (heredoc edits and multi-command captures split off, container prompts read
from the file), the EXPECTED/RECORDED quotes of assets/terminal/expected, source panels from
assets/source, terminal helpers, tags, chips, cards, small glyphs and the video's set pieces V1-V8.
Generic helpers come from L14's common.py (tested); the glyphs and set pieces are new.
build/common_test.py plays every helper and piece once (Bench*: explainer.check clean).

    from manim import *          # first
    from common import *         # second (common's names win), then:
    SAY = NARRATION["S07"]; assert len(SAY) == SAY_COUNT["S07"]   # one voiceover block per SAY

Notes for scene authors
=======================
Rules. Every text here is >= 20 pt: never .scale() a group that holds text below 1.0 (pieces take
size / width parameters instead; text-free icons exist for small copies: trace_icon, server_app_icon,
slip_glyph, lamp). Never set width / height / color / depth on a VGroup subclass (Manim properties):
these classes use box_w, win_w, cell names. Methods marked PLAYS take the scene first, play their own
animation and then keep the new mobjects inside the piece, so a later FadeOut(piece) takes them all.
Methods marked ANIM return an animation you play. To take one part away use piece.drop(self, part):
never FadeOut a member of a piece directly (it snaps back when the piece is next drawn). A piece
inside another (RequestTrace.net is a TwoLocalhosts, .browser a Browser) plays through its owner:
call tr.net.courier_walk(self) freely. Place a piece (shift / move_to) BEFORE its first PLAYS call or
between calls: every PLAYS method builds its new parts at the piece's current position.
Split trap: animating a group that is not itself on the scene (substring(), code_span(), a VGroup you
just made of existing parts) makes Manim split every parent holding those members; re-seat it with
piece.heal(self) (PLAYS methods do it) or self.add(parent).
Amber = ORANGE (V6's loading lamp). Opaque fills: boxes use tint(colour) so lines behind them hide.

Frame budget. Safe frame x in [-6.6, 6.6], y in [-3.6, 3.6]. Tracker top-left (left -6.5, top 3.5,
lowest point TRACK_BOTTOM 2.9); lecture tag lref("24–26 (Frontend)") top right; pictures stay below
PIC_TOP 2.8. Terminals: term() is 12.6 wide, bottom edge at BOTTOM -3.5; a 3-row strip's top is
STRIP_TOP (-1.44), so a picture over a strip lives in y in [-1.3, 2.8].

Data
    NARRATION["S01"] .. ["S16"]  SAY_COUNT  TITLES[cls]  SPEC (video.yaml)
    Prompts P_LAPTOP (= P_HOME, the folder holding both clones) P_V1 P_V1_API P_V1_FRONT P_V2 P_V2_SRC
    P_V2_VDB P_V2_API P_V2_REACT P_V2_SIMPLE; titles T_LAPTOP 'laptop', T_TAB 'laptop · second tab',
    T_NEW 'laptop · new terminal', T_2025 'laptop · branch 2025'. Container prompts are never typed by
    hand: at_prompt(cap, n) / container_prompt(cap, n) read them from the capture line.
    Names PROJECT_PH 'your-gcp-project' SESSION_ID (never read aloud) NETWORK C_API C_VDB C_CLI C_REACT
    C_SIMPLE VDB_IP '172.19.0.2' CHUNKS 14356 BOOK_CHUNKS (b06's eleven numbers) BOOK_LINES (their
    b06 file lines) CHAT_DIR CHAT_FILE HOP_TEXT{0,1,2,3,3.5,4,5,6} FRAMEWORKS ROUTE_GROUPS.
    Repos V1 'cheese-app-v1', V2 'cheese-app-v2' (447b5c3), V2_2025 'cheese-app-v2-at-14f2a14',
    V2_E98 'cheese-app-v2-at-e98fa55' (README only). NAMED_LINES: the two source lines that name the
    instructor; code() refuses a range that includes them.

Trackers (script.md conventions; placed top-left)
    tracker(key, step=None, extra=False), key in TRACKER_KEYS: "SE", "A", "F", "C1", "V", "B", "R",
    "P", "S", "C2", "T23", "T24"; factories tracker_se, tracker_a, tracker_f, tracker_c1, tracker_v,
    tracker_b, tracker_r, tracker_p, tracker_s, tracker_c2, tracker_t23, tracker_t24 (step=None,
    extra=False). P reads 'README @ e98fa55 › Production images', T23/T24 'README @ branch 2025 › …';
    C1, P, T23, T24 carry a fixed GREY note in the caption ('cheese-app-v1', 'earlier README · extra',
    'branch 2025 · 14f2a14'). extra: True (' · extra') | 'our spelling' | 'branch 2025' (' · extra ·
    …') | any other str (appended after ' · ').
    track(tr, k, extra) ANIM · swap_tracker(scene, old, new) PLAYS · lref("27 (Frontend)") the
    lecture tag (the deck name in brackets is required: APIs or Frontend).

Captures (assets/terminal/laptop/<id>-*.txt; folder 'laptop' only; capture-only/ is refused)
    c = capture("a03") / capture("f04-docker-compose-up") (the f04 files by full name)
    c.cmd_lines (typed rows) c.cmd c.k · c.at(*spec) output by FILE line numbers (ints, (a, b), '…');
    refuses the command lines and [exit N] · c.line(n) · c.pick(*ranges) L1-style (body index) ·
    c.lines c.exit c.raw c.path. The instructor's name is masked '‹instructor›' and the staff branch
    'work/shivas' cropped to 'work/…' on load (c01b:2, c31:4 still: cut after 447b5c3 per script).
    CMD_LINES: a05/a23/b27 are heredoc edits (8/10/15 command lines; HEREDOC), b03/f01 a sed + git
    diff (2). type_capture(scene, t, c) PLAYS types them right: for HEREDOC only the git diff line
    (show editor_chip() for the edit); for b03/f01 both rows as two commands.
    type_at(scene, t, cap, n) PLAYS: the terminal takes the container prompt of file line n and types
    its command (type_at(self, t, "a03", 38) = the uvicorn line; "b21", 37 = api_server).
    recorded(file, *nums) -> lines of expected/<file> ('02', '04-troubleshooting'), markdown stripped,
    the '# …' provenance lines refused · quote_card(file, nums, kind='expected'|'recorded'|
    'illustration', source='docs/contract.md:38–42') the panel with its tag · md_plain(s).

Sources (assets/source/<repo>/…; header 'path · lines a–b')
    code(path, a, b=None, focus=, font_size=22, cuts={line: 'cut after'}, elide={line: 'middle'},
        dedent=False) CODE() panel, <= 12 lines, must fit (22 pt ~66 characters, 20 pt ~74; a wider
        panel raises and names the line). e.g. code(f"{V2}/src/frontend-react/vite.config.js", 7, 15,
        font_size=20, cuts={10: "host: true,"}, elide={13: "process.env.API_URL || "}).
        .code .header; highlight with code_span(p.code, k, "x") / line_bar(p.code, k, colour),
        k = file line - a. Languages by suffix (.jsx, .js, .html, .template/.conf = nginx, Dockerfile).
    excerpt(path, a, b) / source_text(path) / readme(n, repo=V2) / readme_lines(a, b, repo=V2) (card
    text, markdown and fences stripped) · readme_card((a, b), body, name=f"{V1}/README.md").

Terminals (house: 12.6 wide, 22 pt = 65 characters a row; 20 pt = 72)
    term(prompt, rows, title) · laptop_term / new_term (rows=10) / tab_term / branch_term (rows=3) ·
    resize(scene, t, rows) PLAYS · room · bare_prompt · type_cmd(scene, t, cmd) · type_capture ·
    type_at · type_lines(scene, t, readme_rows(a, b, repo)) · out(scene, t, lines, wrap=) ·
    cd_prompt(scene, t, prompt) · beside / pin / unpin / on_bar / under_term for tags at a row ·
    row_tag, turn_row, extra_row(kind), time_row, cost_row (tags sized for a terminal row) ·
    no_panel_chip() ('shown without output · not captured': S15's git stash pop).

Tags and chips (GREY unless said; all 20-22 pt)
    your_turn() YELLOW · extra_tag(kind) ('extra · our spelling', 'extra · branch 2025') ·
    illustration_tag(s) · expected_tag(source) · recorded_tag(source) · recording_tag() 'at the time
    of recording' · erratum_tag(s) · cost_tag(text) GOLD (raises on '$', 'cents', 'free tier') ·
    disk_chip(text) GOLD-outlined 'disk' · grey_chip · editor_chip() 'your editor' · dashed_chip
    (past/future, Agent Chat) · tool_chip PURPLE · err_chip RED · ok_chip GREEN · route_chip PINK ·
    box_chip TEAL · differ_chip · file_card(path) · card(lines, head=) · question_card(text) YELLOW ·
    ponder(scene, q, seconds) PLAYS (opaque pause_and_ponder card; FadeOut it at the next block) ·
    flash_tag(scene, tg).

Glyphs (text-free unless named; sizes in scene units)
    tint(colour, k) opaque fill colour · cbox(rows, box_w, box_h) TEAL container box with a 1-2 row
    mono name (.frame .name) · door(port) PINK published-port plate (.plate .text; mono_font=False for
    words) · courier_chip('?'|'Vite'|'nginx') PURPLE · permission_slip(text) PINK slip with the CORS
    header · slip_glyph() · origin_chips('http', 'localhost', '3000') (.parts .port) · checkpoint(text)
    ORANGE gate + question, open_gate(g) ANIM · lamp(state) 'off'|'green'|'amber'|'red'|'dashed' ·
    lamp_pair(states) the two probe lamps with labels (S14 dashed, S16) · eye_glyph() --reload ·
    restart_glyph() · server_app_icon(h) V3 icon · trace_icon(h, courier=, gate=) V1 icon for small
    panels (S15's side by side, S16) · phone_outline(title, h) slide-29 screens · thought_bubble(mob) ·
    strike_box(g) · browser_icon(w) · bucket · disk · image_block · envelope(text) · key_glyph ·
    file_icon / folder_icon · cloud_shape(text, colour, dashed=) · you() · check_glyph / cross_glyph ·
    arrow / route / travel / bounce / pulse_dot · ring / under / strike / hl_bar · outline_box.

Set pieces (V numbers = BRIEF; each class doc gives its exact layout and every method)
    Browser(url, win_w=4.6, win_h=3.2) GREY window, PINK address (label 20; raises when the URL does
        not fit: 'localhost:3000/chat' needs 3.3, '…/newsletters' 4.1). PLAYS goto(url) · fill(rows,
        mono_font=) (raises if rows do not fit the page; V1's page holds ~2.9 units: split long JSON
        into rows or use the label font) · reload() · clear(). ANIM flash(). .frame .address .page
        .rows · at(fx, fy) a point in the page.
    V5 TwoLocalhosts(rows=("front","api","vdb"), front="react"|"simple"|"prod", courier=None|"?"|
        "Vite"|"nginx", cli=False, cable=True, built=True, doors={row: (host, container)}) the laptop
        (6.5 x 4.0 around the anchor): doors on the left wall x -3.25 (3000/:5173, 8080, 8080/:80, 9000,
        8000), boxes x -2.25 .. 2.55 at rows y 1.12 / 0 / -1.12, GREEN cable x 2.9 'cheese-app-network'
        bottom right, 'your laptop' top right. built=False: add_box(row) one by one, cable_on().
        PLAYS add_box · cable_on · unplug(row) / plug(row) · set_courier(text) · courier_walk(back=,
        fail='502', text=) · localhosts() · phone_book(entries, at=) (default under the laptop, right)
        · book_add(name, addr) · dim_door(row, note, at=) · on_box(row, mob) ('26 passed').
        ANIM light(row, colour) · dark(row) · normal(row) · door_pulse(row) · book_light(i).
    V1 RequestTrace(url, rows=("front","api"), front=, courier=, cloud=False, cli=False, cable=None,
        doors=None, caption=True, browser_w=None) browser from x -6.5 (width fits the URL, >= 3.3),
        dashed divider, a TwoLocalhosts (.net) to its right, optional BLUE 'Vertex AI · Gemini' cloud
        (x 4.65 .. 6.45; then the URL must fit 3.3), hop caption at y -2.4. Full frame: shift(UP * 0.4);
        over a 3-row strip: caption=False, shift(UP * 0.75).
        PLAYS hop(n, target="front"|"api", text=) n = 0 OPTIONS scout + slip under the browser, 1
        arrow to the door, 2 door flash, 3 tunnel arrow, 3.5 courier walk, 4 inner chip flash, 5 back
        arrow (via the courier if it walked), 6 window flash; YELLOW numbered circles, caption =
        HOP_TEXT · trip(target, numbers, per) · clear_hops() · uturn(text='307') · page_call(row,
        dashed=, text=) the page's own call (S05 dashed '?', S15 solid) · gate(text) S15's checkpoint
        on that call (text above the browser) · outside_inside() S12 · dns_miss(name) S11 ·
        set_caption(text). .browser .net .cloud .divider .caption .marks.
    V2 ArchitectureMap(built=False) full frame, layers 'title' 'people' 'tools' 'vertex' 'gcp' 'app'
        'edges' 'bucket' 'registry' 'disk' 'cluster' (cluster x 1.7 .. 6.45 with NGINX / Cheese App /
        API Service / Vector DB and PINK 'HTTP 3000/9000/8000'). PLAYS layer(name) · build(names, per)
        · ghost(keep=("cluster",)) / unghost() · ready() 'App is ready!' at (0.3, 1.0) · not_ready()
        · tick_build() · to_laptop() S02 · to_cloud(future=) S16 · swap_box(key, text) S13. ANIM
        light(key, colour) · dark(key) · normal(key). .boxes{'nginx','app','api','vdb'} .ports{'3000',
        '9000','8000'} (S01: fly V1's port labels onto these) .layers .cluster_frame.
    V3 ServerAppDiagram(name=C_API) 9.0 x 3.9 (eth0 plate overhangs to x -5.0); fits over a strip at
        shift(UP * 0.75). PLAYS plates() · bind(host='0.0.0.0'|'127.0.0.1') · split_target(src=) ·
        watch() · add_route(text) · reload(routes) · walk_in(source='eth0'|'inside', ok=) · note(text).
        ANIM flash_route(i). .container .socket .eth0 .lo .badge .card .chips .routes.
    V4 UrlCall() (S04) URL row y 1.45, signature y 0, body y -1.1; fits over a strip at
        shift(UP * 0.55). PLAYS split() · match() · add_query(q) · fly_args(pairs, body) · result(text)
        · bounce(text, code) · uturn(text) · hints(*targets) · reset(). .tokens .sig .hint(i) .default(i).
    V4 RouteTree(built=False) (S08) x -6.5 .. 6.2, y -1.85 .. 1.85 (+ groups row 2.45). PLAYS
        groups(y) · roots() · branch(key) · stamp() · modes() · probes() · snap() · add_leaf() ·
        leaves() · path_label(key, text) · file_map(). ANIM light(key). .nodes .group_chips.
    V6 ProbeLamps() (S07) x -5.2 .. 5.0, y -1.4 .. 1.4; over a strip: shift(UP * 0.75). PLAYS
        set(which, state, status) · status(which, text) · fill_ring(frac) · heartbeat(beats) ·
        bubble(at). .lamps .labels .statuses .ring .vdb.
    V7 ChatFile() (S09) x -6.5 .. 5.4, y -2.4 .. 1.9. PLAYS post(text, key=, ok=, code=) · open_file()
        · append(*(role, text)) (<= 3 rows) · remember() / forget() · cnn(note) · gemini(ok=, cost=)
        · second_copy() · threads() · images(). .browser .key .api .file .rows.
    V8 OneShell() (S10) x -6.2 .. 6.2, y -2.6 .. 2.3 (address bar on top). PLAYS pages() · reload(i) · notes() ·
        collapse() · frameworks(hi="React") · shell(first) · page(text) · pin_header() ·
        address(path) · outlet() · component().

Capture folder names: assets/terminal/laptop (every live step: p*, a*, b*, c*, d*, e*, f*;
a fresh Docker 29.8.2 engine standing in for the laptop, user student) and assets/terminal/expected
(01-prerequisites, 02-chat-contract, 03-review-the-app, 04-troubleshooting: README / docs quotes,
never captures); capture-only/ folders are plumbing and refused.
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import yaml
from manim import (DL, DOWN, DR, LEFT, ORIGIN, PI, RIGHT, TAU, UL, UP, UR, AnimationGroup, Arc,  # noqa: F401
                   Arrow, Circle, Create, CurvedArrow, DashedLine, DashedVMobject, Dot, FadeIn, FadeOut,
                   GrowArrow, GrowFromCenter, Indicate, LaggedStart, Line, MoveAlongPath, Polygon,
                   Rectangle, ReplacementTransform, RoundedRectangle, Rotate, ShowIncreasingSubsets,
                   Succession, Text, Transform, UpdateFromAlphaFunc, ValueTracker, VGroup, VMobject,
                   interpolate_color, linear, there_and_back)
from manim import ManimColor

from explainer import style as S
from explainer.components import pause_and_ponder, person_icon, ponder_card  # noqa: F401 (re-export)
from explainer.devops import (CAPTION, LABEL, MONO, OUTPUT, PANEL, SMALL, TAG, TERM_BG,  # noqa: F401
                              PROMPT_PATH, ReadmeTracker, Terminal, box, browser_window, cell_width, chip,
                              code_block, code_panel, code_span, file_glyph, folder_glyph, glyph_range, label,
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
# SAY lines per scene (script.md v2, review merge 2026-11-05); every scene asserts its own count
SAY_COUNT = {"S01": 7, "S02": 8, "S03": 13, "S04": 10, "S05": 9, "S06": 11, "S07": 11, "S08": 10,
             "S09": 10, "S10": 11, "S11": 9, "S12": 9, "S13": 10, "S14": 9, "S15": 13, "S16": 9}

# ------------------------------------------------------------------ semantic colours (BRIEF.md)
LAPTOP = S.GREY          # the laptop, the browser, its address bar, the host's ports and DNS, secrets/
BROWSER = LAPTOP
YOU = LAPTOP
CLOUD = S.BLUE           # Vertex AI (Gemini, embeddings), the lecture's GCP boundary, cluster, registry
CONTAINER = S.TEAL       # containers and images (api-service, vector-db, frontend-react, nginx's container)
IMAGE = CONTAINER
SHARED = S.ORANGE        # shared, not yours: default bridge, build cache, node_modules volume, same-origin rule
SYSTEM = SHARED
AMBER = S.ORANGE         # V6's "loading" lamp (amber)
OWN = S.GREEN            # what the project owns: lockfiles, chat JSON files, the collection, cheese-app-network,
NET = OWN                #   docs/contract.md, '26 passed'; also a pass / a tick
PASS = OWN
TOOL = S.PURPLE          # uvicorn, FastAPI, http-server, Vite, nginx, Compose, pytest, npm
ERR = S.RED              # 404/405/422/500/502/503, RefreshError, [emerg], refused git switch, README slips
TURN = S.YELLOW          # your turn, the tracker, the hop being traced now, the ponder timer
COST = S.GOLD            # Gemini / embedding calls with your key, disk (~10 GB, the 4.2 GB API image)
ROUTE = S.PINK           # URLs, paths, query strings, -p doors, request/response arrows, hops, origins, headers
PAST = S.GREY            # the past and the future (L5 RAG, L13 CNN, L15 key; L19-L22 cluster): dashed
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
_BRANCH_RE = re.compile(r"work/shivas")          # a staff member's branch name (BRIEF "Crops")


def unname(s: str) -> str:
    """s with the instructor's name masked ('‹instructor›') and the staff branch name cropped
    ('work/…'). capture(), recorded() and source_text() apply it."""
    return _BRANCH_RE.sub("work/…", _NAME_RE.sub("‹instructor›", s))


# ------------------------------------------------------------------ captures
CAPTURE_FOLDERS = ("laptop",)
# captures whose command takes several file lines (script.md TERM conventions): a heredoc edit or a
# `sed` line followed by its `git diff`. The heredoc rows are never typed (a GREY 'your editor'
# chip stands for them): type only c.cmd_lines[-1] (the git diff line) with type_cmd().
CMD_LINES = {"a05": 8, "a23": 10, "b27": 15, "b03": 2, "f01": 2}
HEREDOC = ("a05", "a23", "b27")

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
    """capture("a03") / capture("f04-docker-compose-up") / capture("laptop/b21"): the one file
    assets/terminal/laptop/<name>-*.txt (or <name>.txt). Fails loudly when missing or ambiguous: never
    show an uncaptured output. The command takes lines 1..k: k from CMD_LINES, else line 1 plus every
    row that follows a trailing '\\'. capture-only/ is plumbing and refused."""
    folder, _, stem = name.rpartition("/")
    folder = folder or "laptop"
    if "capture-only" in name:
        raise ValueError("capture-only/ is plumbing (CA bundle builds, the placeholder key): never shown")
    if folder not in CAPTURE_FOLDERS:
        raise ValueError(f"capture folder {folder!r}: one of {CAPTURE_FOLDERS}")
    d = TERMINAL / folder
    stem = stem[:-4] if stem.endswith(".txt") else stem
    p = d / f"{stem}.txt"
    if not p.exists():
        hits = sorted(d.glob(f"{stem}-*.txt"))
        if len(hits) != 1:
            raise FileNotFoundError(f"capture {folder}/{stem}: {len(hits)} matches "
                                    f"{[h.name for h in hits]} (see ASSETS.md; f04 files are named in full)")
        p = hits[0]
    with open(p, encoding="utf-8", newline="") as f:
        text = f.read()
    raw = [unname(s.rstrip("\r").expandtabs(8)) for s in text.rstrip("\n").split("\n")]
    if not raw[0].startswith("$ "):
        raise ValueError(f"{p.name}: line 1 is not a '$ …' command")
    key = p.name.split("-")[0]
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
    """Lines of assets/terminal/expected/<file> ('02', '02-chat-contract', '04-troubleshooting.txt')
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
P_LAPTOP = "student@laptop:~$"                                   # the folder that holds both clones
P_HOME = P_LAPTOP
P_V1 = "student@laptop:~/cheese-app-v1$"
P_V1_API = "student@laptop:~/cheese-app-v1/src/api-service$"
P_V1_FRONT = "student@laptop:~/cheese-app-v1/src/frontend-simple$"
P_V2 = "student@laptop:~/cheese-app-v2$"
P_V2_SRC = "student@laptop:~/cheese-app-v2/src$"
P_V2_VDB = "student@laptop:~/cheese-app-v2/src/vector-db$"
P_V2_API = "student@laptop:~/cheese-app-v2/src/api-service$"
P_V2_REACT = "student@laptop:~/cheese-app-v2/src/frontend-react$"
P_V2_SIMPLE = "student@laptop:~/cheese-app-v2/src/frontend-simple$"
T_LAPTOP = "laptop"
T_TAB = "laptop · second tab"
T_NEW = "laptop · new terminal"
T_2025 = "laptop · branch 2025"

PROJECT_PH = "your-gcp-project"                                  # b03, f01, c04 (never a real id)
SESSION_ID = "00000000-0000-4000-8000-000000000001"              # the curl captures' session id (never read)
NETWORK = "cheese-app-network"
C_API = "cheese-app-api-service"
C_VDB = "cheese-app-vector-db"
C_CLI = "cheese-app-vector-db-cli"
C_REACT = "cheese-app-frontend-react"
C_SIMPLE = "cheese-app-frontend-simple"
VDB_IP = "172.19.0.2"                                            # b10, the phone book's first entry
CHUNKS = 14356                                                   # b06: the eleven books' chunks
BOOK_CHUNKS = (923, 714, 3569, 926, 2623, 1198, 1146, 678, 2147, 269, 163)   # b06:65 … 208, in order
BOOK_LINES = (65, 78, 97, 110, 127, 141, 155, 168, 184, 196, 208)
assert sum(BOOK_CHUNKS) == CHUNKS
CHAT_DIR = "chat-history/llm-cnn/"                               # b42
CHAT_FILE = "<session>/<chat>.json"
HOP_TEXT = {                                                     # V1 captions (script.md notes)
    0: "0 the browser asks first: OPTIONS",
    1: "1 request",
    2: "2 the laptop forwards it to the published port",
    3: "3 the port is mapped into the container",
    3.5: "3½ a courier carries it on, by name",
    4: "4 the function runs",
    5: "5 the response comes back",
    6: "6 the page shows it",
}
FRAMEWORKS = ("Angular", "React", "Vue", "Svelte")               # Frontend slide 33, no logos
ROUTE_GROUPS = ("Newsletters", "Podcasts", "LLM Chat", "LLM + CNN Chat", "RAG Chat", "Agent Chat")  # APIs slide 44

# ------------------------------------------------------------------ sources
# assets/source/<repo>/…: cheese-app-v1 (ce03a10), cheese-app-v2 (447b5c3 = main today),
# cheese-app-v2-at-14f2a14 (branch 2025), cheese-app-v2-at-e98fa55 (README only: Production images)
V1 = "cheese-app-v1"
V2 = "cheese-app-v2"
V2_2025 = "cheese-app-v2-at-14f2a14"
V2_E98 = "cheese-app-v2-at-e98fa55"
# never in a panel's line range (they name the instructor): source_text() masks them anyway
NAMED_LINES = {f"{V1}/src/frontend-simple/index.html": 57, f"{V2}/src/vector-db/cli.py": 76}


def _src(path: str) -> Path:
    p = SOURCE / path
    if p.exists() and p.is_file():
        return p
    raise FileNotFoundError(f"assets/source/{path}")


def source_text(path: str) -> str:
    """An assets/source file ('cheese-app-v2/src/api-service/api/service.py', 'cheese-app-v1/README.md' …)."""
    return unname(_src(path).read_text(encoding="utf-8"))


def excerpt(path: str, first: int, last: int) -> str:
    """Lines first..last (1-based, inclusive) of assets/source/<path>."""
    return "\n".join(source_text(path).split("\n")[first - 1:last])


def readme(n: int, repo: str = V2) -> str:
    """README.md line n of `repo` (V1, V2, V2_2025, V2_E98), stripped."""
    return excerpt(f"{repo}/README.md", n, n).strip()


def readme_lines(a: int, b: int, repo: str = V2, plain: bool = True) -> str:
    """README lines a..b of `repo` as card text ('\\n' joined, blank lines and fences dropped,
    markdown stripped): readme_card((a, b), readme_lines(a, b, V1), name=f"{V1}/README.md")."""
    rows = excerpt(f"{repo}/README.md", a, b).split("\n")
    rows = [r for r in rows if r.strip() and not r.strip().startswith("```")]
    return "\n".join(md_plain(r) if plain else r for r in rows)


_LANG = {".py": "python", ".toml": "toml", ".sh": "bash", ".md": "markdown", ".yaml": "yaml",
         ".yml": "yaml", ".txt": "text", ".json": "json", ".lock": "toml", ".html": "html",
         ".js": "javascript", ".jsx": "jsx", ".css": "css", ".template": "nginx", ".conf": "nginx"}


def _lang(name: str) -> str:
    if name.startswith("Dockerfile"):
        return "docker"
    if name == "requirements.txt":
        return "text"
    return _LANG.get(Path(name).suffix, "text")


def code(path: str, first: int, last: int | None = None, language: str | None = None, focus=None,
         font_size: float = 22, shown: str | None = None, max_lines: int = 12, cuts: dict | None = None,
         dedent: bool = False, elide: dict | None = None):
    """CODE(path: first–last) of script.md: a code_panel quoting assets/source/<path>, header
    '<path> · lines a–b'. <= 12 lines. The panel must fit the frame (22 pt holds ~66 characters a
    line, 20 pt ~74: a long line needs font_size=20); a wider panel raises: cut a line with cuts={file_line: 'text it ends after'} (the house '…', GREY) or use
    font_size=20. .code .header; highlight with code_span(p.code, k, "x") / line_bar(p.code, k,
    colour), k = file line - first. dedent=True removes the common leading indentation.
    elide={file_line: 'middle text'} replaces that text (first occurrence) with a GREY '…', e.g.
    vite.config.js:13 (83 characters): elide={13: "process.env.API_URL || "}."""
    last = first if last is None else last
    if last - first + 1 > max_lines:
        raise ValueError(f"CODE {path}: {last - first + 1} lines; never more than {max_lines} on screen")
    if path in NAMED_LINES and first <= NAMED_LINES[path] <= last:
        raise ValueError(f"CODE {path}: line {NAMED_LINES[path]} names the instructor; keep it out of the range")
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


# ------------------------------------------------------------------ trackers (script.md, twelve)
SECTIONS = {
    "SE": "Setup Environments · Environment Setup",
    "A": "Backend API Container",
    "F": "Frontend App (Simple) Container",
    "C1": "Docker Cleanup",
    "V": "Tutorial: Vector DB for RAG Setup",
    "B": "Tutorial: Backend APIs",
    "R": "Tutorial: React Frontend Setup",
    "P": "Production images",
    "S": "Tutorial: Setup & Run Cheese App",
    "C2": "Docker Cleanup",
    "T23": "Tutorial (23): Vector DB · Backend APIs",
    "T24": "Tutorial (24): Simple Frontend App",
}
STEPS = {
    "SE": ["Clone v1", "Clone v2", "Local folders", "Project ID"],
    "A": ["Go to folder", "Build & run", "Start uvicorn", "Test root", "Add route", "Try route",
          "Add params", "View docs"],
    "F": ["Go to folder", "Build & run", "http-server", "Test 8080", "Edit index", "Refresh page"],
    "C1": ["Container ls", "Stop containers", "System prune", "Image ls"],
    # V, B, R, S: step k is the README's own step k (the narration reads those numbers aloud), so
    # the README's step 1 'cd + docker-shell' is one step; the unnumbered sub-sections follow it
    "V": ["cd + docker-shell", "Load database", "Try chat", "exit"],
    "B": ["cd + docker-shell", "api_server", "Check probes", "Demo route", "Try route",
          "API docs", "GET newsletters", "Review code", "pytest"],
    "R": ["cd + docker-shell", "npm run dev", "Open 3000", "Review app", "Review code",
          "npm run check"],
    "P": ["Stop dev", "docker build", "docker run", "Open 8080", "Compare sizes"],
    "S": ["Project ID", "Stop containers", "cd src + compose up", "Open app", "compose down"],
    "C2": ["compose down", "system prune"],
    # two sections of the branch-2025 README: each step names its section and README number
    "T23": ["VDB 1: cd vector-db", "VDB 2: docker-shell", "VDB 3: load", "Backend 1: cd api-service",
            "Backend 2: docker-shell", "Backend 4: uvicorn_server", "Verify 9000"],
    "T24": ["cd frontend", "docker-shell", "http-server", "Home page", "Newsletters", "Chat"],
}
# 'README @ <ref> ›' for the trackers that follow another commit's README
REFS = {"P": "@ e98fa55", "T23": "@ branch 2025", "T24": "@ branch 2025"}
# a fixed GREY note after every caption of that tracker
NOTES = {"C1": "cheese-app-v1", "P": "earlier README · extra", "T23": "branch 2025 · 14f2a14",
         "T24": "branch 2025 · 14f2a14"}
TRACKER_KEYS = tuple(SECTIONS)
EXTRA_KINDS = ("our spelling", "branch 2025")


def place_tracker(tr: ReadmeTracker) -> ReadmeTracker:
    """Pin a tracker to the house corner (left edge -6.5, top 3.5)."""
    tr.shift(np.array([TRACK_LEFT - tr.get_left()[0], TRACK_TOP - tr.get_top()[1], 0]))
    return tr


def _suffix(extra, note: str | None = None) -> str:
    s = f" · {note}" if note else ""
    if not extra:
        return s
    if extra is True:
        return s + ("" if note and note.endswith("extra") else " · extra")
    if extra in EXTRA_KINDS:
        return s + f" · extra · {extra}"
    if isinstance(extra, str):
        return s + " · " + extra
    raise ValueError(f"extra={extra!r}")


def _caption(tr: ReadmeTracker, k: int, extra) -> Text:
    if not k:
        return steady("", tr.size, tr.hi_color).next_to(tr.dots, RIGHT, buff=0.25)
    s = f"step {k} of {len(tr.steps)}: {tr.steps[k - 1]}"
    suf = _suffix(extra, NOTES.get(getattr(tr, "key", None)))
    t = steady(s + suf, tr.size, tr.hi_color, t2c={suf.strip(" ·"): S.GREY} if suf else None)
    return t.next_to(tr.dots, RIGHT, buff=0.25)


def tracker(key: str, step: int | None = None, extra=False) -> ReadmeTracker:
    """Tracker `key` (TRACKER_KEYS) at `step` (1-based; None = no step lit yet), placed top-left:
    'README [@ ref] › <section>', one dot per step, 'step k of N: <step>' + the GREY note/extra suffix."""
    tr = ReadmeTracker(SECTIONS[key], STEPS[key])
    tr.key = key
    if key in REFS:                      # 'README @ e98fa55' stays one first part (swap_tracker keeps it)
        h0 = VGroup(mono("README", tr.size, S.GREY), label(REFS[key], tr.size, S.GREY)).arrange(RIGHT, buff=0.12)
        h0.move_to(tr.head[0], aligned_edge=LEFT)
        tr.head.submobjects[0] = h0
        tr.head.arrange(RIGHT, buff=0.12).align_to(tr.dots, LEFT)
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
    make.__name__ = "tracker_" + key.lower()
    make.__doc__ = f"tracker('{key}', step, extra): README › {SECTIONS[key]}"
    return make


tracker_se, tracker_a, tracker_f, tracker_c1, tracker_v, tracker_b, tracker_r, tracker_p, tracker_s, \
    tracker_c2, tracker_t23, tracker_t24 = map(_tracker_factory, TRACKER_KEYS)


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
    regroup; a different 'README @ ref' part cross-fades too). `new` ends on the scene as one piece."""
    from manim import FadeTransform
    same_ref = REFS.get(old.key) == REFS.get(new.key)
    keep = VGroup(old.head[0], old.head[1]) if same_ref else VGroup(old.head[1])
    scene.remove(old)
    olds = [old.head[2], old.dots, old.caption] + ([] if same_ref else [old.head[0]])
    scene.add(*keep, *olds)
    moves = [FadeTransform(old.head[2], new.head[2]), ReplacementTransform(old.dots, new.dots),
             FadeTransform(old.caption, new.caption)]
    if not same_ref:
        moves.append(FadeTransform(old.head[0], new.head[0]))
    scene.play(*moves, *anims, run_time=run_time)
    scene.remove(*keep, *new.head, new.dots, new.caption, *olds)
    scene.add(new)
    return new


def lref(slides: str) -> VGroup:
    """The GREY 'Lecture 18 · slides 24–26 (Frontend)' tag, top right, only while that slide's picture
    or idea is on screen: lref("27 (Frontend)"), lref("34–41 (APIs)"). Deck names: APIs, Frontend."""
    if not slides.rstrip().endswith(("(APIs)", "(Frontend)")):
        raise ValueError(f"lref({slides!r}): name the deck, e.g. '24–26 (Frontend)' or '19–21 (APIs)'")
    if slides.split()[0].isdigit():      # ONE slide: lecture_ref() only sees a bare number as one slide
        g = tag(f"Lecture 18 · slide {slides}", S.GREY)
        return g.move_to([SAFE_X - g.width / 2, SAFE_Y - g.height / 2, 0])
    return lecture_ref(18, slides)


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


def laptop_term(rows: int = 10, prompt: str = P_LAPTOP) -> Terminal:
    """Title 'laptop': the main terminal of each section."""
    return term(prompt, rows, T_LAPTOP)


def tab_term(rows: int = 3, prompt: str = P_LAPTOP) -> Terminal:
    """Title 'laptop · second tab': curl checks while a server holds the foreground."""
    return term(prompt, rows, T_TAB)


def new_term(rows: int = 10, prompt: str = P_LAPTOP) -> Terminal:
    """Title 'laptop · new terminal': where the README says 'in a new terminal'."""
    return term(prompt, rows, T_NEW)


def branch_term(rows: int = 3, prompt: str = P_LAPTOP) -> Terminal:
    """Title 'laptop · branch 2025' (S01's c25 strip)."""
    return term(prompt, rows, T_2025)


def type_at(scene, t: Terminal, cap, n: int, type_time: float | None = None):
    """PLAYS: a command typed at a CONTAINER prompt, as file line n of the capture recorded it: the
    terminal's prompt becomes that container prompt (printed from the file, never invented), then the
    command types. Returns the typed line. E.g. type_at(self, t, "a03", 38) types the uvicorn line."""
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


def type_capture(scene, t: Terminal, cap, type_time: float | None = None) -> list:
    """PLAYS: type a capture's command exactly as its file lines spell it (cap: a Capture or a
    capture name). A row that follows a trailing '\\' is a continuation (no prompt); every other row
    is a separate command at the prompt (b03's sed + git diff). type_time: per row. Returns the list
    of typed lines (each a line or a folded VGroup). For a heredoc edit (HEREDOC: a05, a23, b27)
    only the git diff line is typed (the edit itself is the viewer's editor: editor_chip())."""
    cap = capture(cap) if isinstance(cap, str) else cap
    out_, cont = [], False
    rows = cap.cmd_lines[-1:] if cap.path.name.split("-")[0] in HEREDOC else cap.cmd_lines
    for row in rows:
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


def readme_rows(a: int, b: int, repo: str = V2) -> list[str]:
    """README lines a..b of `repo` as command rows (verbatim, right-stripped; blank rows and code
    fences dropped) for type_lines(): e.g. readme_rows(47, 47, V1) is v1's uvicorn line."""
    rows = [s.rstrip() for s in excerpt(f"{repo}/README.md", a, b).split("\n")]
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
    """'extra' sized for a terminal row (GREY); kind 'local stand-in' -> 'extra · local stand-in'."""
    return row_tag("extra" + (f" · {kind}" if kind else ""), S.GREY)


def time_row() -> VGroup:
    """'at the time of recording' sized for a terminal row (GREY)."""
    return row_tag("at the time of recording", S.GREY)


def cost_row(s: str) -> VGroup:
    """A GOLD cost tag sized for a terminal row (never an amount: see cost_tag())."""
    return row_tag(_no_amount(s), COST)


def no_panel_chip(s: str = "shown without output · not captured") -> VGroup:
    """The GREY chip under a command typed with no output panel (S15's `git stash pop`)."""
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
        raise ValueError(f"cost tag {s!r}: no prices or free-tier figures on screen")
    return s


def your_turn() -> VGroup:
    """YELLOW '▶ your turn' tag (house size: beside a card or panel, not inside a terminal row)."""
    return tag("▶ your turn", TURN)


def extra_tag(kind: str | None = None) -> VGroup:
    """GREY 'extra' tag; kind 'our spelling' / 'branch 2025' -> 'extra · our spelling' …"""
    return tag("extra" + (f" · {kind}" if kind else ""), S.GREY)


def illustration_tag(s: str = "illustration") -> VGroup:
    """On every browser drawing, the prerequisites card and lecture redrawings of cloud machinery
    (schematic; never a screenshot): illustration_tag('illustration · README:13–18')."""
    return tag(s, S.GREY)


def expected_tag(source: str | None = None) -> VGroup:
    """'expected · docs/contract.md:38–42': the documented shape of a success we could not capture."""
    return tag("expected" + (f" · {source}" if source else ""), S.GREY)


def recorded_tag(source: str | None = None) -> VGroup:
    """'recorded · README:223–233': the README's own words (troubleshooting rows)."""
    return tag("recorded" + (f" · {source}" if source else ""), S.GREY)


def recording_tag(s: str = "at the time of recording") -> VGroup:
    """Beside versions on first show."""
    return tag(s, S.GREY)


def erratum_tag(s: str = "erratum") -> VGroup:
    """On every README/slide slip (the narration says 'a small slip' or 'a small note'):
    erratum_tag('erratum · add src/')."""
    return tag(s, S.GREY)


def cost_tag(s: str) -> VGroup:
    """The GOLD money tag: what a call with YOUR key bills. Raises on '$', 'cents', 'free tier'."""
    return tag(_no_amount(s), COST)


def disk_chip(s: str = "disk · about 10 GB") -> VGroup:
    """The GOLD-outlined 'disk' chip (S01, S07 'this image: 4.2 GB', S14, S16). .box .text"""
    return chip(s, COST, size=20)


def grey_chip(s: str, size: float = 20, mono_font: bool = False, color=S.GREY) -> VGroup:
    """A GREY chip for a short note ('your editor', 'extra arguments · none here'). .box .text"""
    return chip(s, color, size=size, font=MONO if mono_font else None)


def editor_chip() -> VGroup:
    """'your editor': stands for a heredoc edit that is never typed (a05, a23, b27)."""
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
               card_w: float | None = None, color=INK, width_chars: int = 60) -> VGroup:
    """EXPECTED(expected/<file>: nums) or RECORDED(…): a GREY-outlined panel quoting those lines
    (markdown stripped), with the tag '<kind> · <source>' on its top edge (right). kind 'expected' |
    'recorded' | 'illustration'. nums: an int, a range tuple, or a list. Long lines wrap at
    `width_chars`. .frame .body .tag"""
    nums = [nums] if isinstance(nums, (int, tuple)) else list(nums)
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


def _spans(s: str, size: float, color) -> VGroup:
    """One row of a markdown cell: prose in the label font, `code` spans in mono, same baseline
    strut (steady), a word gap only where the source has a space."""
    parts = s.split("`")
    pieces, gaps, between = [], [], ""
    for i, p in enumerate(parts):
        if not p.strip():
            between += p
            continue
        if pieces:
            spaced = " " in (between + p[:1])
            gaps.append(0.13 if spaced else 0.03)
        pieces.append(steady(p.strip(), size, color, mono_font=bool(i % 2)))
        between = p[-1:]
    g = VGroup(*pieces)
    for k in range(1, len(pieces)):
        pieces[k].next_to(pieces[k - 1], RIGHT, buff=gaps[k - 1])
        pieces[k].align_to(pieces[k - 1], DOWN)
    return g


FIX_INK = interpolate_color(ManimColor(S.GREY), ManimColor(INK), 0.55)  # the fix line: lighter than GREY on the card fill


def _wrap_spans(s: str, n: int) -> list[str]:
    """`s` broken at its last space that fits `n` characters, never inside a `code` span (the text is
    unchanged, only the row break moves)."""
    out_, cur = [], ""
    for w in s.split(" "):
        if cur and len(cur) + 1 + len(w) > n and cur.count("`") % 2 == 0:
            out_.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}" if cur else w
    return out_ + [cur]


def trouble_card(nums, source: str, size: float = 20, card_w: float | None = 12.4,
                 wrap: int | None = None) -> VGroup:
    """RECORDED(expected/04-troubleshooting.txt: nums) as table rows: each README row is the symptom
    in WHITE, then an indented light-grey '→' and the fix (one sentence per line), code spans in mono, a gap
    between rows. Same frame and tag as quote_card (S07, S09). card_w=None: as wide as the rows + 0.7.
    wrap=n: a fix sentence longer than n characters continues on the next line (at a space, outside code).
    .frame .body (one VGroup per README row) .tag"""
    rows = []
    for raw in recorded("04", *nums, plain=False):
        cells = [c.strip() for c in raw.strip().strip("|").split("|")]
        assert len(cells) == 2, raw
        sym, fix = cells
        sentences = [x for x in re.split(r"(?<=\.) (?=[A-Z])", fix) if x]
        if wrap:
            sentences = [part for x in sentences for part in _wrap_spans(x, wrap)]
        top = _spans(sym, size, INK)
        fx = VGroup(*[_spans(x, size, FIX_INK) for x in sentences]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        arr = label("→", size, FIX_INK)
        arr.next_to(fx[0], LEFT, buff=0.15).set_y(fx[0].get_center()[1])
        fix_g = VGroup(arr, fx)
        fix_g.next_to(top, DOWN, buff=0.12).align_to(top, LEFT).shift(RIGHT * 0.45)
        rows.append(VGroup(top, fix_g))
    body = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.34)
    card_w = card_w or body.width + 0.7
    frame = box(card_w, body.height + 0.75, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
    body.move_to(frame).align_to(frame, LEFT).shift(RIGHT * 0.35 + DOWN * 0.06)
    assert body.width < card_w - 0.6, body.width
    tg = tag("recorded" + f" · {source}", S.GREY)
    tg.move_to(frame.get_corner(UR) + np.array([-tg.width / 2 - 0.2, 0, 0]))
    g = VGroup(frame, body, tg)
    g.frame, g.body, g.tag = frame, body, tg
    return g


VEIL = "#0D1014"                 # ponder(dim=...)'s veil: S.BG #0D0F14 with green + 1 (see ponder)


def ponder(scene, question: str, seconds: float = 8, center=None, width: float = 9.5,
           dim: float = 0.0) -> VGroup:
    """PLAYS a PONDER card (YELLOW timer drains over `seconds`). center=(x, y) moves it (default:
    the frame's centre). The frame is opaque, so the card may sit over a set piece. dim > 0 (0.85
    when the card sits ON a set piece): a full-frame BG veil at that opacity fades in with the card,
    behind it and in front of everything else, so the words around its edges read as dimmed, not
    sliced; the veil is part of the returned group (FadeOut(card) takes it too) and .card is the
    card alone (measure placement on it). Returns the group (still on screen): FadeOut it at the
    start of the next block."""
    c = ponder_card(question, width=width)
    c[0].set_fill(S.BG, 1)        # opaque: at 0.96 the words of a set piece behind it ghost through
    if center is not None:
        c.move_to([center[0], center[1], 0])
    bar = c[3]
    g = c
    if dim:
        # the safe area is the whole set (explainer.check keeps every visible mobject inside it), so a
        # BG veil of exactly that size dims all of it and stays clear of the OUT lint itself
        # VEIL, not S.BG: Cairo's premultiplied blend of BG over BG at 0.85 lands one level darker
        # in green (13,14,20 vs 13,15,20), which shows as a faint box edge; VEIL blends back to BG exactly
        veil = Rectangle(width=2 * SAFE_X, height=2 * SAFE_Y).set_stroke(width=0).set_fill(VEIL, dim)
        g = VGroup(veil, c)
        g.veil = veil
    g.card = c
    scene.play(FadeIn(g, scale=0.95), run_time=0.6)
    target = bar.copy().scale(0.001, about_point=bar.get_start())
    scene.play(bar.animate(rate_func=linear).become(target), run_time=seconds)
    return g


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


def courier_chip(text: str = "?", size: float = 20) -> VGroup:
    """V1's courier (hop 3½) in the frontend box: a PURPLE chip '?' / 'Vite' / 'nginx'. .box .text"""
    return chip(text, TOOL, size=size, fill_opacity=0.3)


def permission_slip(text: str = "access-control-allow-origin: *", size: float = 20, color=ROUTE) -> VGroup:
    """The CORS 'permission slip': a PINK card with a folded corner and the header on it. .card .text"""
    t = mono(text, size, INK)
    w, h = t.width + 0.6, 0.62
    pts = [[-w / 2, h / 2, 0], [w / 2 - 0.2, h / 2, 0], [w / 2, h / 2 - 0.2, 0], [w / 2, -h / 2, 0],
           [-w / 2, -h / 2, 0]]
    body = Polygon(*pts, stroke_color=color, stroke_width=2.5).set_fill(tint(color, 0.2), 1)
    fold = VMobject(stroke_color=color, stroke_width=2).set_points_as_corners(
        [[w / 2 - 0.2, h / 2, 0], [w / 2 - 0.2, h / 2 - 0.2, 0], [w / 2, h / 2 - 0.2, 0]])
    t.move_to(body).shift(LEFT * 0.05)
    g = VGroup(body, fold, t)
    g.card, g.text = VGroup(body, fold), t
    return g


def slip_glyph(h: float = 0.45, color=ROUTE) -> VGroup:
    """A text-free permission slip (small copies: recap icons, S11's struck slip)."""
    w = h * 0.8
    body = Polygon([-w / 2, h / 2, 0], [w / 2 - 0.12, h / 2, 0], [w / 2, h / 2 - 0.12, 0], [w / 2, -h / 2, 0],
                   [-w / 2, -h / 2, 0], stroke_color=color, stroke_width=2.5).set_fill(tint(color, 0.2), 1)
    lines = VGroup(*[Line([-w * 0.3, y, 0], [w * 0.3, y, 0], color=color, stroke_width=2)
                     for y in (h * 0.15, -h * 0.05, -h * 0.25)])
    return VGroup(body, lines)


def origin_chips(scheme: str = "http", host: str = "localhost", port: str = "3000", size: float = 20,
                 color=ROUTE) -> VGroup:
    """An origin as three PINK chips 'http' · 'localhost' · '3000' (scheme + host + port). .parts
    (the three chips) .port (the port chip: ring it RED when two origins differ)."""
    parts = [route_chip(x, size) for x in (scheme, host, port)]
    dots = [label("·", size, S.GREY) for _ in range(2)]
    g = VGroup(parts[0], dots[0], parts[1], dots[1], parts[2]).arrange(RIGHT, buff=0.1)
    g.parts, g.port = parts, parts[2]
    return g


def checkpoint(text: str = "did the server allow this origin?", size: float = 20, color=SHARED) -> VGroup:
    """S15's ORANGE checkpoint on an outgoing arrow: a barrier gate glyph and its question.
    .gate .bar .text; open it with open_gate(g) (ANIM: the bar lifts, GREEN)."""
    post = Line(DOWN * 0.3, UP * 0.3, color=color, stroke_width=5)
    bar = Line(ORIGIN, RIGHT * 0.7, color=color, stroke_width=6).shift(UP * 0.2)
    bar.shift(post.get_top() + DOWN * 0.1 - bar.get_start())
    gate = VGroup(post, bar)
    t = label(text, size, color).next_to(gate, DOWN, buff=0.12)
    g = VGroup(gate, t)
    g.gate, g.bar, g.text = gate, bar, t
    return g


def open_gate(g, color=OWN):
    """ANIM: a checkpoint's bar lifts and turns GREEN."""
    return AnimationGroup(Rotate(g.bar, PI / 2, about_point=g.bar.get_start()),
                          g.bar.animate.set_color(color), g.gate[0].animate.set_color(color))


def lamp(state: str = "off", r: float = 0.28) -> VGroup:
    """A probe lamp: 'off' (GREY outline), 'green', 'amber', 'red', 'dashed' (GREY dashed, S14)."""
    col = {"off": S.GREY, "green": OWN, "amber": AMBER, "red": ERR, "dashed": S.GREY}[state]
    c = Circle(radius=r, stroke_color=col, stroke_width=3).set_fill(col, 0 if state in ("off", "dashed") else 0.85)
    if state == "dashed":
        c = DashedVMobject(c, num_dashes=12).set_stroke(col, 3)
    glow = Circle(radius=r * 1.45, stroke_width=0).set_fill(col, 0 if state in ("off", "dashed") else 0.18)
    return VGroup(glow, c)


def lamp_pair(states=("off", "off"), size: float = 20, buff: float = 1.0) -> VGroup:
    """V6's two lamps without the box (S14 'no probes yet' with states=('dashed','dashed'), S16):
    lamp + mono '/healthz' / '/readyz' under it. .lamps .labels"""
    items = []
    for st, name in zip(states, ("/healthz", "/readyz")):
        lp = lamp(st)
        t = mono(name, size, INK if st != "dashed" else S.GREY).next_to(lp, DOWN, buff=0.12)
        items.append(VGroup(lp, t))
    g = VGroup(*items).arrange(RIGHT, buff=buff, aligned_edge=UP)
    g.lamps, g.labels = [i[0] for i in items], [i[1] for i in items]
    return g


def eye_glyph(h: float = 0.32, color=TOOL) -> VGroup:
    """uvicorn's --reload watcher: an eye."""
    from manim import ArcBetweenPoints
    top = ArcBetweenPoints(LEFT * h, RIGHT * h, angle=-PI / 2.2)
    bot = ArcBetweenPoints(LEFT * h, RIGHT * h, angle=PI / 2.2)
    pupil = Circle(radius=h * 0.28, stroke_width=0).set_fill(color, 1)
    return VGroup(top, bot).set_stroke(color, 3).add(pupil)


def restart_glyph(r: float = 0.22, color=S.GREY) -> VGroup:
    """A circular 'restart' arrow."""
    a = Arc(radius=r, start_angle=PI / 2, angle=-1.6 * PI, color=color, stroke_width=4)
    a.add_tip(tip_length=0.12)
    return a


def server_app_icon(h: float = 0.9) -> VGroup:
    """Text-free V3: TEAL container > PURPLE uvicorn box > PURPLE app card (small copies: S07, S16)."""
    c = RoundedRectangle(width=h * 1.5, height=h, corner_radius=0.06, stroke_color=CONTAINER,
                         stroke_width=3).set_fill(tint(CONTAINER), 1)
    u = RoundedRectangle(width=h * 1.1, height=h * 0.7, corner_radius=0.05, stroke_color=TOOL,
                         stroke_width=2.5).move_to(c).shift(RIGHT * h * 0.12)
    a = RoundedRectangle(width=h * 0.62, height=h * 0.4, corner_radius=0.04, stroke_color=TOOL,
                         stroke_width=2).set_fill(TOOL, 0.3).move_to(u).shift(RIGHT * h * 0.12 + DOWN * h * 0.05)
    sock = Dot(u.get_left(), radius=h * 0.06, color=ROUTE)
    return VGroup(c, u, a, sock)


def trace_icon(h: float = 1.4, courier: bool = False, gate: bool = False, color=ROUTE) -> VGroup:
    """Text-free V1 for small panels (S15's side-by-side, S16's test card): a browser, a laptop with
    two TEAL boxes, PINK arrows; courier=True adds a PURPLE courier between the boxes, gate=True an
    ORANGE checkpoint on the browser's outgoing arrow. Scales freely (no text)."""
    w = h * 0.9
    b = RoundedRectangle(width=w, height=h * 0.75, corner_radius=0.06, stroke_color=LAPTOP,
                         stroke_width=2.5).set_fill(PANEL, 1)
    bar = Line(b.get_corner(UL) + DOWN * h * 0.14, b.get_corner(UR) + DOWN * h * 0.14, color=LAPTOP, stroke_width=2)
    lap = RoundedRectangle(width=w * 1.5, height=h, corner_radius=0.08, stroke_color=LAPTOP,
                           stroke_width=2.5).next_to(b, RIGHT, buff=w * 0.7)
    f = RoundedRectangle(width=w * 1.0, height=h * 0.28, corner_radius=0.04, stroke_color=CONTAINER,
                         stroke_width=2.5).set_fill(tint(CONTAINER), 1).move_to(lap).shift(UP * h * 0.22)
    a = f.copy().shift(DOWN * h * 0.44)
    arr1 = Arrow(b.get_right(), [lap.get_left()[0] + 0.05, f.get_y(), 0], buff=0.05, color=color,
                 stroke_width=3, tip_length=0.12)
    g = VGroup(b, bar, lap, f, a, arr1)
    if courier:
        c = RoundedRectangle(width=w * 0.3, height=h * 0.16, corner_radius=0.03, stroke_color=TOOL,
                             stroke_width=2).set_fill(TOOL, 0.5).move_to(f).shift(RIGHT * w * 0.28)
        hop = Line(c.get_bottom(), [c.get_x(), a.get_top()[1], 0], color=OWN, stroke_width=3)
        g.add(hop, c)
    else:
        arr2 = Arrow(b.get_right() + DOWN * h * 0.15, [lap.get_left()[0] + 0.05, a.get_y(), 0], buff=0.05,
                     color=color, stroke_width=3, tip_length=0.12)
        g.add(arr2)
    if gate:
        gt = VGroup(Line(DOWN * h * 0.12, UP * h * 0.12), Line(ORIGIN, RIGHT * h * 0.2).shift(UP * h * 0.1))
        gt.set_stroke(SHARED, 4).move_to(g[-1].get_center() + UP * h * 0.12)
        g.add(gt)
    return g


def phone_outline(title: str, h: float = 2.2, size: float = 20) -> VGroup:
    """APIs slide 29's wireframe screen: a GREY phone outline with its screen name. .frame .title"""
    t = label(title, size, INK)
    fr = RoundedRectangle(width=max(h * 0.55, t.width + 0.35), height=h, corner_radius=0.16, stroke_color=LAPTOP,
                          stroke_width=3).set_fill(PANEL, 1)
    t.move_to(fr.get_top() + DOWN * 0.35)
    lines = VGroup(*[Line(LEFT * fr.width * 0.32, RIGHT * fr.width * 0.32, color=S.GREY_DARK, stroke_width=6)
                     .shift(UP * (h * 0.1 - i * h * 0.16)) for i in range(3)]).move_to(fr).shift(DOWN * 0.1)
    g = VGroup(fr, t, lines)
    g.frame, g.title = fr, t
    return g


def thought_bubble(content, color=S.GREY, pad: float = 0.35) -> VGroup:
    """A GREY dashed thought bubble around `content` (a mobject), with two small trailing circles at
    its lower left. .frame .content"""
    w, h = content.width + 2 * pad, content.height + 2 * pad
    fr = outline_box(w, h, color, solid=False, radius=0.35).move_to(content)
    tail = VGroup(Circle(radius=0.1), Circle(radius=0.06)).set_stroke(color, 2)
    tail[0].move_to(fr.get_corner(DL) + np.array([0.1, -0.2, 0]))
    tail[1].move_to(fr.get_corner(DL) + np.array([-0.12, -0.42, 0]))
    g = VGroup(fr, tail, content)
    g.frame, g.content = fr, content
    return g


def strike_box(g, color=ERR, stroke: float = 4) -> Line:
    """A diagonal strike over a box or chip (lower left to upper right)."""
    return Line(g.get_corner(DL) + np.array([-0.05, -0.03, 0]), g.get_corner(UR) + np.array([0.05, 0.03, 0]),
                color=color, stroke_width=stroke)


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


# ------------------------------------------------------------------ V5 · TwoLocalhosts
_FRONT_KINDS = {
    "react": (("cheese-app-", "frontend-react"), ("3000", "5173")),
    "simple": (("cheese-app-", "frontend-simple"), ("8080", None)),
    "prod": (("cheese-app-", "frontend-react:prod"), ("8080", "80")),
}
_ROW_NAMES = {"api": ("cheese-app-", "api-service"), "vdb": ("cheese-app-", "vector-db")}
_ROW_DOORS = {"api": ("9000", None), "vdb": ("8000", None)}
_INNER = {"api": "uvicorn", "vdb": "Chroma", "simple": "http-server"}


class TwoLocalhosts(_Anchored):
    """V5 · the laptop and its containers (also V1's right half). A GREY laptop (6.5 x 4.0, centred on
    the anchor) titled 'your laptop'; up to three TEAL container rows, top to bottom:
        'front' y +1.12  frontend box: front='react' (door 3000, :5173, courier slot) | 'simple'
                         (door 8080, 'http-server') | 'prod' (door 8080, :80, courier 'nginx')
        'api'   y  0.00  cheese-app-api-service (door 9000, 'uvicorn')
        'vdb'   y -1.12  cheese-app-vector-db (door 8000, 'Chroma'); cli=True adds the
                         cheese-app-vector-db-cli box beside it (no door)
    Each row: a PINK door on the laptop's left wall (x -3.25) with the host port, a PINK tunnel to
    the box (x -2.25 .. 2.55), the container port above the box's top-left corner when it differs
    (':5173'). 'your laptop' sits top right; the network's name bottom right.
    The GREEN cable 'cheese-app-network' runs down the right (x 2.9) with a stub to each box.

        net = TwoLocalhosts(rows=("front", "api", "vdb"), front="react", courier="?", cable=True,
                            built=True)
    built=False starts with the empty laptop: PLAYS add_box(scene, row) · cable_on(scene).
    .frame .title .boxes{row} .doors{row} .tunnels{row} .ports{row} .stubs{row} .inner{row}
    .courier (front chip or None) .cable .net_label .cli .book .labels (localhost tags)
    PLAYS add_box · cable_on · plug(scene, row) / unplug(scene, row) · set_courier(scene, text) ·
    courier_walk(scene, back=False, fail=None, text=None) · localhosts(scene) · phone_book(scene,
    entries, at=None) · book_add(scene, name, addr=None) · dim_door(scene, row, note=None, at=None) ·
    on_box(scene, row, mob) (a badge on the box's top edge).
    ANIM light(row, color) · normal(row) · dark(row) · door_pulse(row) · book_light(i)."""

    LAP_W, LAP_H = 6.5, 4.0
    ROW_Y = {"front": 1.12, "api": 0.0, "vdb": -1.12}
    BOX_L, BOX_W, BOX_H = -2.25, 4.8, 0.84
    CABLE_X = 2.9

    def __init__(self, rows=("front", "api", "vdb"), front: str | None = "react", courier: str | None = None,
                 cli: bool = False, cable: bool = True, built: bool = True, doors: dict | None = None,
                 size: float = 20, **kw):
        super().__init__(**kw)
        self.size, self.front_kind, self.cli_on = size, front, cli
        self.door_ports = dict(doors or {})
        self.frame = RoundedRectangle(width=self.LAP_W, height=self.LAP_H, corner_radius=0.16,
                                      stroke_color=LAPTOP, stroke_width=3).set_fill(S.BG, 1).move_to(self.p(0, 0))
        self.title = label("your laptop", size, LAPTOP).move_to(self.p(0, 0)).align_to(self.frame, UR).shift(
            np.array([-0.18, -0.12, 0]))
        self.add(self.frame, self.title)
        self.boxes, self.doors, self.tunnels, self.ports, self.stubs, self.inner = {}, {}, {}, {}, {}, {}
        self.courier, self.cable, self.net_label, self.cli, self.book = None, None, None, None, None
        self.labels = VGroup()
        self.courier_text = courier
        if built:
            for r in rows:
                parts = self._row(r)
                self.add(*parts)
            if cable:
                for m in self._cable():
                    self.add(m)

    # -- geometry
    def row_y(self, row: str) -> float:
        return self.p(0, self.ROW_Y[row])[1]

    def wall_x(self) -> float:
        return self.p(-self.LAP_W / 2, 0)[0]

    def door_point(self, row: str) -> np.ndarray:
        """The left edge of a row's door (where V1's arrow 1 lands)."""
        return self.doors[row].get_left()

    # -- parts
    def _row(self, row: str) -> list:
        y = self.ROW_Y[row]
        size = self.size
        if row == "front":
            names, (hp, cp) = _FRONT_KINDS[self.front_kind]
        else:
            names, (hp, cp) = _ROW_NAMES[row], _ROW_DOORS[row]
        hp, cp = self.door_ports.get(row, (hp, cp))
        w = self.BOX_W
        if row == "vdb" and self.cli_on:
            w = 2.25
        bx = cbox(names, w, self.BOX_H, size=size)
        bx.move_to(self.p(self.BOX_L + w / 2, y))
        parts = [bx]
        inner = None
        if row == "front" and self.front_kind in ("react", "prod"):
            text = "nginx" if self.front_kind == "prod" and self.courier_text is None else self.courier_text
            if text is not None:
                inner = courier_chip(text, size)
                self.courier = inner
        elif row == "front" and self.front_kind == "simple":
            inner = tool_chip(_INNER["simple"], size, mono_font=False)
        elif row in _INNER and w == self.BOX_W:
            inner = tool_chip(_INNER[row], size, mono_font=False)
        if inner is not None:
            inner.move_to(bx).align_to(bx.frame, RIGHT).shift(LEFT * 0.15)
            parts.append(inner)
        self.inner[row] = inner
        self.boxes[row] = bx
        if hp:
            d = door(hp, size=size).move_to([self.wall_x(), self.p(0, y)[1], 0])
            tun = Line(d.get_right(), bx.get_left(), color=ROUTE, stroke_width=4)
            self.doors[row], self.tunnels[row] = d, tun
            parts[:0] = [tun, d]
            if cp:                     # the container port, just above the box's top-left corner
                pl = mono(":" + cp, size, ROUTE).next_to(bx.frame.get_corner(UL), UP, buff=0.04)
                pl.align_to(bx.frame, LEFT).shift(RIGHT * 0.12)
                self.ports[row] = pl
                parts.append(pl)
        if row == "vdb" and self.cli_on:
            cl = cbox(("cheese-app-", "vector-db-cli"), 2.4, self.BOX_H, size=size)
            cl.move_to(self.p(self.BOX_L + self.BOX_W - 1.2, y))
            self.cli = cl
            parts.append(cl)
        return parts

    def _stub(self, row: str):
        bx = self.cli if (row == "vdb" and self.cli is not None) else self.boxes[row]
        y = self.row_y(row)
        return Line([bx.get_right()[0], y, 0], [self.p(self.CABLE_X, 0)[0], y, 0], color=NET, stroke_width=5)

    def _cable(self) -> list:
        ys = [self.ROW_Y[r] for r in self.boxes]
        top, bot = (max(ys), min(ys)) if ys else (self.ROW_Y["front"], self.ROW_Y["vdb"])
        self.cable = Line(self.p(self.CABLE_X, top + 0.25), self.p(self.CABLE_X, bot - 0.25), color=NET, stroke_width=6)
        self.net_label = mono(NETWORK, self.size, NET).move_to(self.p(0, -1.8)).align_to(
            self.frame, RIGHT).shift(LEFT * 0.15)
        out_ = [self.cable, self.net_label]
        for r in self.boxes:
            self.stubs[r] = self._stub(r)
            out_.append(self.stubs[r])
        if self.cli is not None and "vdb" in self.boxes:          # the vector-db's own stub runs behind the CLI box
            st = Line(self.boxes["vdb"].get_right(), self.cli.get_left(), color=NET, stroke_width=5)
            out_.append(st)
        return out_

    # -- PLAYS
    def add_box(self, scene, row: str, run_time: float = 0.7):
        """PLAYS: a row's box (and its door, tunnel, port label) appears; a stub too if the cable is on."""
        parts = self._row(row)
        if self.cable is not None:
            self.stubs[row] = self._stub(row)
            parts.append(self.stubs[row])
        # behind-first order: tunnels and stubs under the boxes
        self.show(scene, *parts, anims=[FadeIn(m) for m in parts], run_time=run_time)
        return self.boxes[row]

    def cable_on(self, scene, run_time: float = 1.0):
        """PLAYS: the GREEN cable 'cheese-app-network' draws, with a stub to every box."""
        parts = self._cable()
        anims = [Create(parts[0]), FadeIn(parts[1])] + [Create(m) for m in parts[2:]]
        self.show(scene, *parts, anims=anims, run_time=run_time)
        for b in self.boxes.values():                      # boxes stay on top of the stubs
            self.remove(b)
            self.add(b)
        for c in [self.cli, self.courier, *[i for i in self.inner.values() if i is not None]]:
            if c is not None and c in self.submobjects:
                self.remove(c)
                self.add(c)
        self.heal(scene)
        return self.cable

    def unplug(self, scene, row: str = "api", run_time: float = 0.5):
        """PLAYS: the row's stub leaves the cable (S11's d09: the API off the network)."""
        st = self.stubs.pop(row)
        self.drop(scene, st, run_time=run_time)

    def plug(self, scene, row: str = "api", run_time: float = 0.5):
        """PLAYS: the row's stub joins the cable again."""
        self.stubs[row] = self._stub(row)
        self.show(scene, self.stubs[row], anims=[Create(self.stubs[row])], run_time=run_time)

    def set_courier(self, scene, text: str, run_time: float = 0.5):
        """PLAYS: the courier chip's label changes ('?' -> 'Vite' -> 'nginx'), or it appears."""
        new = courier_chip(text, self.size).move_to(self.boxes["front"]).align_to(
            self.boxes["front"].frame, RIGHT).shift(LEFT * 0.15)
        if self.courier is None:
            self.show(scene, new, anims=[GrowFromCenter(new)], run_time=run_time)
        else:
            self.swap(scene, self.courier, new, run_time=run_time)
        self.courier = self.inner["front"] = new
        return new

    def _walk_path(self, back: bool):
        c = self.courier
        y_f, y_a = self.row_y("front"), self.row_y("api")
        x_c = self.p(self.CABLE_X, 0)[0]
        x_api = self.boxes["api"].get_right()[0] - 0.75
        pts = [c.get_center(), [x_c, y_f, 0], [x_c, y_a, 0], [x_api, y_a, 0]]
        if back:
            pts = pts[::-1]
        path = VMobject().set_points_as_corners([np.array(p, dtype=float) for p in pts])
        return path

    def courier_walk(self, scene, back: bool = False, fail: str | None = None, text: str | None = None,
                     run_time: float = 1.4):
        """PLAYS: a copy of the courier carries a small PINK envelope (text: '/api/…', optional) from
        the frontend box along the cable to the API box (back=True: the other way). fail='502': the
        walk turns round at the cable (the API is unplugged) and comes back with a RED '502' chip and
        an empty envelope, which then fade. The walker never stays on screen."""
        if self.courier is None:
            raise ValueError("courier_walk: no courier (TwoLocalhosts(front='react', courier='?'))")
        walker = self.courier.copy()
        env = envelope(text or "x", ROUTE, env_w=None if text else 0.5)
        if not text:                                   # an empty envelope: no text at all
            env.remove(env.text)
            env.body.stretch_to_fit_height(0.4)
            env.flap.become(VMobject(stroke_color=ROUTE, stroke_width=2.5).set_points_as_corners(
                [env.body.get_corner(UL), env.body.get_center() + UP * 0.08, env.body.get_corner(UR)]))
        env.next_to(walker, UP, buff=0.06)
        grp = VGroup(walker, env)
        path = self._walk_path(back)
        scene.add(grp)
        if fail:
            x_c = self.p(self.CABLE_X, 0)[0]
            half = VMobject().set_points_as_corners([path.get_start(), np.array([x_c, self.row_y("front"), 0.0]),
                                                     np.array([x_c, self.row_y("api") + 0.3, 0.0])])
            scene.play(MoveAlongPath(grp, half), run_time=run_time * 0.6, rate_func=linear)
            bad = err_chip(fail, self.size).next_to(grp, LEFT, buff=0.1)
            off = bad.get_center() - grp.get_center()
            scene.play(FadeIn(bad), env.animate.set_opacity(0.4), run_time=0.3)
            back = half.copy().reverse_points()
            scene.play(MoveAlongPath(grp, back), MoveAlongPath(bad, back.copy().shift(off)),
                       run_time=run_time * 0.6, rate_func=linear)
            scene.play(FadeOut(grp), FadeOut(bad), run_time=0.3)
            scene.remove(grp, bad)
        else:
            scene.play(MoveAlongPath(grp, path), run_time=run_time, rate_func=linear)
            scene.play(FadeOut(grp), run_time=0.25)
            scene.remove(grp)
        self.heal(scene)

    def localhosts(self, scene, run_time: float = 0.6):
        """PLAYS: a GREY 'localhost' tag on each box's top edge (centre), and one before 'your laptop':
        every box has its own localhost."""
        tags = []
        for b in [*self.boxes.values()] + ([self.cli] if self.cli is not None else []):
            t = tag("localhost", S.GREY, size=20)
            t.move_to(b.frame.get_top() + RIGHT * 0.25 * (b.frame.width > 3))
            tags.append(t)
        t0 = tag("localhost", S.GREY, size=20).next_to(self.title, LEFT, buff=0.15)
        tags.append(t0)
        self.show(scene, *tags, into=self.labels, run_time=run_time)
        return self.labels

    def phone_book(self, scene, entries=((C_VDB, VDB_IP),), at=None, run_time: float = 0.6):
        """PLAYS: the network's GREEN phone book card (name → address rows, mono 20) appears below the
        laptop's right half (at=(x, y) places its centre). An entry is (name, addr) or (name, None).
        Returns the card; .book.rows[i] are the entries."""
        rows = VGroup(*[self._book_row(n, a) for n, a in entries])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        hd = label(f"{NETWORK} · names", 20, NET)
        inner = VGroup(hd, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        fr = RoundedRectangle(width=max(inner.width + 0.5, 4.2), height=inner.height + 0.4, corner_radius=0.12,
                              stroke_color=NET, stroke_width=2.5).set_fill(S.BG, 1)
        inner.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.25)
        bk = VGroup(fr, inner)
        bk.frame, bk.rows, bk.head = fr, rows, hd
        if at is not None:
            bk.move_to([at[0], at[1], 0])
        else:
            bk.next_to(self.frame, DOWN, buff=0.15).align_to(self.frame, RIGHT)
        self.book = bk
        self.show(scene, bk, run_time=run_time)
        return bk

    def _book_row(self, name: str, addr: str | None) -> VGroup:
        parts = [mono(name, 20, INK)]
        if addr:
            parts += [label("→", 20, S.GREY), mono(addr, 20, ROUTE)]
        return VGroup(*parts).arrange(RIGHT, buff=0.14)

    def book_add(self, scene, name: str, addr: str | None = None, run_time: float = 0.5):
        """PLAYS: a new entry writes on at the bottom of the phone book (the card grows down)."""
        row = self._book_row(name, addr).next_to(self.book.rows, DOWN, buff=0.12, aligned_edge=LEFT)
        newh = self.book.frame.height + row.height + 0.12
        neww = max(self.book.frame.width, row.width + 0.5)
        fr2 = RoundedRectangle(width=neww, height=newh, corner_radius=0.12, stroke_color=NET,
                               stroke_width=2.5).set_fill(S.BG, 1).align_to(self.book.frame, UL)
        scene.play(Transform(self.book.frame, fr2), run_time=run_time * 0.5)
        self.show(scene, row, run_time=run_time * 0.5, into=self.book.rows)
        return row

    def book_light(self, i: int, color=TURN):
        """ANIM: phone-book entry i flashes."""
        return Indicate(self.book.rows[i], color=color, scale_factor=1.06)

    def dim_door(self, scene, row: str, note: str | None = None, at=None, run_time: float = 0.5):
        """PLAYS: a row's door and tunnel dim (S11: 9000 stays, 'for /api/docs and curl'); the note is
        a GREY chip under the laptop, left-aligned with the door wall (at=(x, y) moves it), joined to
        the door by a thin GREY line. Returns the chip (or None)."""
        anims = [self.doors[row].animate.set_opacity(0.35), self.tunnels[row].animate.set_opacity(0.35)]
        scene.play(*anims, run_time=run_time)
        if note:
            c = grey_chip(note).next_to(self.frame, DOWN, buff=0.15).align_to(self.doors[row], LEFT)
            if at is not None:
                c.move_to([at[0], at[1], 0])
            ln = DashedLine(self.doors[row].get_bottom(), c.get_top(), color=S.GREY, stroke_width=2, dash_length=0.08)
            self.show(scene, ln, c, run_time=0.4)
            return c
        return None

    def on_box(self, scene, row: str, mob, run_time: float = 0.5):
        """PLAYS: `mob` (a chip, '26 passed') settles on a box's top edge (right of centre, clear of the
        name and the inner chip) and stays with the piece. A chip (.box) gets an opaque BG backing, so
        the box's top edge does not strike its text through (S09's badge does the same)."""
        b = self.boxes[row].frame
        if hasattr(mob, "box"):
            mob.add_to_back(mob.box.copy().set_stroke(width=0).set_fill(S.BG, 1))
        mob.move_to(b.get_top() + RIGHT * 0.45)
        return self.show(scene, mob, run_time=run_time)

    # -- ANIM
    def light(self, row: str, color=TURN):
        """ANIM: a box's outline turns `color` (TURN: the one being traced; OWN: up and ready)."""
        return self.boxes[row].animate.set_stroke(color)

    def dark(self, row: str, darkness: float = 0.7):
        """ANIM: a box fades (stopped); normal(row) brings it back."""
        return self.boxes[row].animate.fade(darkness)

    def normal(self, row: str):
        """ANIM: a box back to its built look (TEAL outline, full opacity)."""
        b = self.boxes[row]
        ref = b.copy()
        ref.frame.set_stroke(CONTAINER, opacity=1).set_fill(tint(CONTAINER), 1)
        ref.name.set_opacity(1)
        return Transform(b, ref)

    def door_pulse(self, row: str, color=TURN):
        """ANIM: a row's door swells and its outline flashes `color` (the number stays readable)."""
        return self.doors[row].animate(rate_func=there_and_back).scale(1.15).set_stroke(color)


# ------------------------------------------------------------------ V1 · RequestTrace
class RequestTrace(_Anchored):
    """V1 · the lecture's hop-by-hop request, one layout for the whole video (13.0 x 4.0 + the
    caption row under it; anchor = origin):
        browser   Browser(url, bw x 3.0) from x -6.5; bw = browser_w or max(3.3, the URL + 0.95):
                  3.3 for 'localhost:3000/chat' (x -6.5 .. -3.2), 4.1 for 'localhost:3000/newsletters'
        divider   GREY dashed vertical 0.4 right of the browser (x -2.8 at bw 3.3)
        laptop    a TwoLocalhosts (.net), its door wall 0.8 right of the divider (x -2.0 .. 4.5 at bw 3.3)
        cloud     cloud=True: BLUE dashed 'Vertex AI · Gemini' centred (5.55, 0)   x 4.65 .. 6.45 (then
                  bw must stay 3.3: a longer URL raises)
        caption   the hop caption under it, y -2.4 (caption=False: none)
    Full frame: move_to(UP * 0.4) or leave it; over a 3-row strip use caption=False and
    shift(UP * 0.75) (then it spans y -1.25 .. 2.75).

        tr = RequestTrace("localhost:3000/chat", rows=("front", "api", "vdb"), front="react", courier="?",
                          cloud=True)
    PLAYS hop(scene, n, target="api", text=None): n = 0 (OPTIONS scout + a PINK 'access-control-allow-
        origin' badge back) · 1 request arrow, browser -> the target's door · 2 the door flashes ·
        3 a PINK arrow along the tunnel · 3.5 the courier walks the cable to the API · 4 the target's
        inner chip flashes · 5 the response arrow back to the browser (via the courier when it walked) ·
        6 the page flashes. Each hop adds a YELLOW numbered circle and sets the caption (HOP_TEXT,
        or `text`). Hop marks stay until clear_hops(scene).
    trip(scene, target, numbers=(1, 2, 3, 4, 5, 6), per=0.8) plays several hops in a row.
    clear_hops(scene) · uturn(scene, text="307", target) a PINK U-turn at arrow 1's tip ·
    page_call(scene, row="api", dashed=False, text=None) the page's own JavaScript fires a second
    arrow at a door (S05: dashed + '?'; S15: solid) · gate(scene, text=None) S15's ORANGE checkpoint
    on that arrow (returns it; open_gate(g) opens it) · outside_inside(scene) S12's YELLOW outer ring
    + GREEN 'unchanged' inner ring · dns_miss(scene, name=C_API) S11's envelope to the laptop's DNS
    desk -> RED 'not found' · set_caption(scene, text).
    .browser (a Browser) .net (the TwoLocalhosts: courier_walk, phone_book, dim_door … all work)
    .cloud .divider .caption .marks (hop arrows and circles)."""

    CLOUD_C = (5.55, 0.0)
    CAP_Y = -2.4

    def __init__(self, url: str = "localhost:3000", rows=("front", "api"), front: str | None = "react",
                 courier: str | None = None, cloud: bool = False, cli: bool = False, cable: bool | None = None,
                 doors: dict | None = None, caption: bool = True, browser_w: float | None = None,
                 size: float = 20, **kw):
        super().__init__(**kw)
        self.size = size
        bw = browser_w or max(3.3, label(url, size).width + 0.95)
        right = 6.5 - (1.95 if cloud else 0.0)
        if -6.5 + bw + 1.225 + TwoLocalhosts.LAP_W > right + 1e-6:
            raise ValueError(f"RequestTrace: a {bw:.2f}-wide browser leaves no room for the laptop"
                             + (" and the cloud" if cloud else "") + ": shorten the URL")
        self.BROWSER_C = (-6.5 + bw / 2, 0.0)
        self.DIV_X = -6.5 + bw + 0.4
        self.NET_C = (self.DIV_X + 0.8 + TwoLocalhosts.LAP_W / 2, 0.0)
        self.browser = Browser(url, bw, 3.0, size).move_to(self.p(*self.BROWSER_C))
        self.browser.owner = self
        self.divider = DashedLine(self.p(self.DIV_X, 2.0), self.p(self.DIV_X, -2.0), color=S.GREY_DARK,
                                  stroke_width=2.5, dash_length=0.12)
        if cable is None:
            cable = len(rows) > 1
        self.net = TwoLocalhosts(rows=rows, front=front, courier=courier, cli=cli, cable=cable, doors=doors,
                                 size=size)
        self.net.shift(self.p(*self.NET_C) - self.net.ref.get_center())
        self.net.owner = self
        self.add(self.browser, self.divider, self.net)
        self.cloud = None
        if cloud:
            self.cloud = cloud_shape("Vertex AI\nGemini", CLOUD, cloud_w=1.8, dashed=True).move_to(self.p(*self.CLOUD_C))
            self.add(self.cloud)
        self.with_caption = caption
        self.caption = None
        self.marks = VGroup()
        self.add(self.marks)
        self._walked = False

    # -- helpers
    def _badge(self, n) -> VGroup:
        s = "3½" if n == 3.5 else str(int(n))
        b = step_badge(s, TURN, size=22, radius=0.24 if n == 3.5 else 0.22)
        b[0].set_fill(S.BG, 1)
        return b

    def set_caption(self, scene, text: str, run_time: float = 0.4):
        """PLAYS: the caption under the piece changes (number YELLOW, words WHITE)."""
        if not self.with_caption:
            return None
        num, _, rest = text.partition(" ")
        t = VGroup(label(num, 22, TURN), label(rest, 22, INK)).arrange(RIGHT, buff=0.14)
        t.move_to(self.p(0, self.CAP_Y))
        if self.caption is None:
            self.caption = t
            self.show(scene, t, run_time=run_time)
        else:
            self.caption = self.swap(scene, self.caption, t, run_time=run_time)
        return self.caption

    def _mark(self, scene, mobs, anims, run_time):
        self.show(scene, *mobs, anims=anims, run_time=run_time, into=self.marks)

    def _req_arrow(self, row: str, start=None, dashed: bool = False):
        a = start if start is not None else self.browser.frame.get_right() + np.array(
            [0, (self.net.row_y(row) - self.browser.get_y()) * 0.5, 0])
        b = self.net.door_point(row) + LEFT * 0.03
        arr = Arrow(a, b, buff=0.04, color=ROUTE, stroke_width=4, tip_length=0.18,
                    max_tip_length_to_length_ratio=0.35)
        if dashed:
            arr = DashedVMobject(arr, num_dashes=8).set_stroke(ROUTE, 4)
        return arr

    # -- PLAYS
    def hop(self, scene, n, target: str = "api", text: str | None = None, run_time: float = 0.8):
        """PLAYS hop n (0, 1, 2, 3, 3.5, 4, 5, 6) toward row `target` ('front' or 'api'); see the class
        doc. Returns the hop's main mobject (arrow, badge …)."""
        net = self.net
        cap = text or HOP_TEXT[n]
        main = None
        if n == 0:
            home = self.browser.at(0.45, 0.2)
            sc = route_chip("OPTIONS", 20).move_to(home)
            sc.box.set_fill(S.BG, 1)
            bd = self._badge(0).next_to(sc, LEFT, buff=0.1)
            self.set_caption(scene, cap)
            self._mark(scene, [bd], [FadeIn(bd)], 0.3)
            scene.play(FadeIn(sc), run_time=0.3)
            door_pt = net.door_point(target) + LEFT * 0.5
            scene.play(sc.animate.move_to(door_pt), run_time=run_time * 0.6)
            back = permission_slip("access-control-allow-origin", 20).scale(1.0)
            back.next_to(self.browser.frame, DOWN, buff=0.15).align_to(self.browser.frame, LEFT)
            scene.play(sc.animate.move_to(home), run_time=run_time * 0.6)
            scene.play(FadeOut(sc), FadeIn(back, shift=UP * 0.1), run_time=0.4)
            scene.remove(sc)
            self.marks.add(back)
            self.heal(scene)
            return back
        if n == 1:
            arr = self._req_arrow(target)
            bd = self._badge(1).move_to(arr.get_center() + UP * 0.38)
            self.set_caption(scene, cap)
            self._mark(scene, [arr, bd], [GrowArrow(arr), FadeIn(bd)], run_time)
            main = arr
        elif n == 2:
            d = net.doors[target]
            bd = self._badge(2).next_to(d, UP, buff=0.06)
            self.set_caption(scene, cap)
            scene.play(net.door_pulse(target), run_time=run_time * 0.6)
            self._mark(scene, [bd], [FadeIn(bd)], 0.3)
            main = d
        elif n == 3:
            tun = net.tunnels[target]
            arr = Arrow(tun.get_start(), tun.get_end(), buff=0, color=TURN, stroke_width=5, tip_length=0.16,
                        max_tip_length_to_length_ratio=0.45)
            bd = self._badge(3).next_to(tun, DOWN, buff=0.08)
            self.set_caption(scene, cap)
            self._mark(scene, [arr, bd], [GrowArrow(arr), FadeIn(bd)], run_time)
            main = arr
        elif n == 3.5:
            bd = self._badge(3.5).move_to([net.p(net.CABLE_X, 0)[0] + 0.38, (net.row_y("front") + net.row_y("api")) / 2, 0])
            self.set_caption(scene, cap)
            self._mark(scene, [bd], [FadeIn(bd)], 0.3)
            net.courier_walk(scene, run_time=run_time * 1.6)
            self._walked = True
            main = bd
        elif n == 4:
            inner = net.inner.get(target)
            bx = net.boxes[target]
            bd = self._badge(4).move_to(bx.frame.get_top() + RIGHT * 0.2)
            self.set_caption(scene, cap)
            anims = [Indicate(inner if inner is not None else bx.name, color=TURN, scale_factor=1.12)]
            scene.play(*anims, run_time=run_time * 0.7)
            self._mark(scene, [bd], [FadeIn(bd)], 0.3)
            main = bd
        elif n == 5:
            if self._walked:
                net.courier_walk(scene, back=True, run_time=run_time * 1.6)
                src_row = "front"
            else:
                src_row = target
            tun = net.tunnels[src_row]
            d = pulse_dot(ROUTE, 0.09).move_to(tun.get_end())
            scene.add(d)
            scene.play(d.animate.move_to(tun.get_start()), run_time=run_time * 0.4)
            scene.remove(d)
            a = net.doors[src_row].get_corner(DL) + np.array([0.05, 0.04, 0])
            b = self.browser.frame.get_right() + np.array([0, (a[1] - self.browser.get_y()) * 0.5 - 0.55, 0])
            arr = Arrow(a, b, buff=0.04, color=ROUTE, stroke_width=4, tip_length=0.18, path_arc=-0.6,
                        max_tip_length_to_length_ratio=0.35)
            bd = self._badge(5).move_to(arr.point_from_proportion(0.5) + DOWN * 0.36)
            self.set_caption(scene, cap)
            self._mark(scene, [arr, bd], [GrowArrow(arr), FadeIn(bd)], run_time * 0.6)
            main = arr
        elif n == 6:
            bd = self._badge(6).move_to(self.browser.page.get_corner(UR) + np.array([-0.3, -0.3, 0]))
            self.set_caption(scene, cap)
            scene.play(self.browser.flash(), run_time=run_time * 0.7)
            self._mark(scene, [bd], [FadeIn(bd)], 0.3)
            main = bd
        else:
            raise ValueError(f"hop {n}: one of 0, 1, 2, 3, 3.5, 4, 5, 6")
        return main

    def trip(self, scene, target: str = "api", numbers=(1, 2, 3, 4, 5, 6), per: float = 0.8):
        """PLAYS the hops in `numbers` toward `target` in a row (no voiceover timing)."""
        for n in numbers:
            self.hop(scene, n, target, run_time=per)

    def clear_hops(self, scene, run_time: float = 0.4):
        """PLAYS: every hop arrow, circle and badge, and the caption, fade."""
        mobs = list(self.marks.submobjects) + ([self.caption] if self.caption is not None else [])
        if mobs:
            self.drop(scene, *mobs, run_time=run_time)
        self.caption = None
        self._walked = False

    def uturn(self, scene, text: str = "307", target: str = "api", run_time: float = 0.8):
        """PLAYS: a small PINK U-turn at the door of `target` with `text` ('307' or '307 · /newsletters/')."""
        d = self.net.doors[target].get_left() + LEFT * 0.08
        arc = CurvedArrow(d + UP * 0.12, d + UP * 0.12 + LEFT * 0.55 + DOWN * 0.0, angle=PI * 0.9, color=ROUTE,
                          stroke_width=4, tip_length=0.14)
        arc.shift(UP * 0.12)
        t = label(text, 20, ROUTE).next_to(arc, UP, buff=0.05)
        self._mark(scene, [arc, t], [Create(arc), FadeIn(t)], run_time)
        return VGroup(arc, t)

    def page_call(self, scene, row: str = "api", dashed: bool = False, text: str | None = None,
                  run_time: float = 0.8):
        """PLAYS: the page's own JavaScript fires a PINK arrow from inside the page straight at `row`'s
        door (S15, B24–B26; dashed + text='?' for S05's call that never happens)."""
        start = self.browser.at(0.55, -0.35)
        arr = self._req_arrow(row, start=start, dashed=dashed)
        mobs = [arr]
        if text:
            t = label(text, 22, ROUTE).move_to(arr.get_center() + DOWN * 0.32)
            mobs.append(t)
        self._mark(scene, mobs, [Create(arr)] + [FadeIn(m) for m in mobs[1:]], run_time)
        self.call_arrow = arr
        return arr

    def gate(self, scene, text: str | None = "did the server allow this origin?", run_time: float = 0.5):
        """PLAYS: S15's ORANGE checkpoint on the page_call arrow (just outside the browser). The text
        sits above the browser. Returns it (open_gate(g) is the ANIM that opens it)."""
        g = checkpoint(text or "", 20)
        a = self.call_arrow
        xb = self.browser.frame.get_right()[0] + 0.12
        pts = [a.point_from_proportion(t / 40) for t in range(41)]
        hit = min(pts, key=lambda q: abs(q[0] - xb))
        g.gate.move_to(hit + UP * 0.12)
        if text:
            g.text.next_to(self.browser.frame, UP, buff=0.12).align_to(self.browser.frame, LEFT)
        else:
            g.remove(g.text)
        self._mark(scene, [g], [FadeIn(g)], run_time)
        return g

    def outside_inside(self, scene, run_time: float = 0.8):
        """PLAYS (S12): YELLOW dashed rings round the outside (the browser; the front door + frontend
        box) and a GREEN ring round the API box with 'unchanged'. Returns (outer rings, inner, chip)."""
        net = self.net
        o1 = ring(self.browser.frame, TURN, buff=0.06, dashed=True)
        o2 = ring(VGroup(net.doors["front"], net.boxes["front"]), TURN, buff=0.06, dashed=True)
        i = ring(net.boxes["api"], OWN, buff=0.06)
        c = ok_chip("unchanged").next_to(i, DOWN, buff=0.08).align_to(i, RIGHT)
        o = VGroup(o1, o2)
        self._mark(scene, [o, i, c], [Create(o1), Create(o2), Create(i), FadeIn(c)], run_time)
        return o, i, c

    def dns_miss(self, scene, name: str = C_API, run_time: float = 1.0):
        """PLAYS (S11): an envelope addressed `name` leaves the browser for a GREY 'your laptop's DNS'
        desk under the browser, which has no entry: RED 'not found'. Returns the desk group."""
        desk = card(["your laptop's DNS"], S.GREY, size=20).next_to(self.browser.frame, DOWN, buff=0.7)
        env = envelope(name, ROUTE).scale(1.0)
        if env.width > 4.0:
            env = envelope("cheese-app-api-…", ROUTE)
        env.move_to(self.browser.at(0, 0))
        self._mark(scene, [desk], [FadeIn(desk)], 0.4)
        scene.add(env)
        scene.play(env.animate.next_to(desk, UP, buff=0.05), run_time=run_time * 0.6)
        nf = err_chip("not found", mono_font=False).next_to(desk, RIGHT, buff=0.12)
        if nf.get_right()[0] > self.DIV_X + self.ref.get_x() - 0.05:
            nf.next_to(desk, DOWN, buff=0.1)
        scene.play(FadeIn(nf), env.animate.set_opacity(0.4), run_time=run_time * 0.4)
        scene.remove(env)
        self.marks.add(env, nf)
        self.heal(scene)
        return VGroup(desk, nf)


# ------------------------------------------------------------------ V2 · ArchitectureMap
class ArchitectureMap(_Anchored):
    """V2 · the lecture's technical architecture (APIs slides 7–21), full frame, built one layer at a
    time in series colours. Layers (names for layer() / ghost()), with their places:
        title     chip 'technical architecture · the system's blueprint'      (0, 2.45)
        people    GREY bands 'developers · data scientists' (left, -4.25) and 'users' (right, 4.6), y 1.72
        tools     'Colab notebooks' (-5.45, 0.35) and 'GitHub' (-5.45, -1.2), GREY boxes
        vertex    BLUE 'Vertex AI' panel with a 'Gemini' box               (-2.6, 0.15)
        gcp       BLUE dashed GCP boundary x -4.1 .. 6.5, y -3.3 .. 1.2 ('GCP' bottom left)
        app       GREY 'App' box where the cluster goes                    (4.1, -1.0)
        edges     PINK 'HTTPS 443' (developers -> Colab, -> Vertex AI) and 'HTTP/HTTPS 80' (users -> app)
        bucket    BLUE 'GCS bucket · data & models'                         (-2.6, -1.75)
        registry  BLUE 'Artifact Registry' with image rows                  (0.15, -2.35)
        disk      BLUE 'persistent disk' + 'NFS' edge to the cluster        (0.15, -0.55)
        cluster   box x 1.7 .. 6.45, y -3.15 .. 1.05, 'compute instance / Kubernetes cluster', four TEAL
                  boxes: 'nginx' NGINX (4.1, 0.15), 'app' Cheese App (2.95, -1.0), 'api' API Service
                  (5.2, -1.0), 'vdb' Vector DB (5.2, -2.3); PINK edges 'HTTP 3000', 'HTTP 9000', 'HTTP 8000'
    The 'App is ready!' chip sits left of the cluster at (0.3, 1.0), its caption and tick under it.
    built=True draws every layer but 'app' at once (S01: then ghost(scene, keep=("cluster",))).
    PLAYS layer(scene, name) · build(scene, names, per=1.0) · ghost(scene, keep=(...)) every other shown
    layer fades to a ghost · unghost(scene) restores them · ready(scene) GREEN 'App is ready!' ·
    not_ready(scene) RED strike + 'Well not really, / we need to build it' · tick_build(scene) S16: a
    GREEN tick 'the pieces' under it · to_laptop(scene) S02: the other layers ghost and the cluster frame
    becomes a GREY laptop 'your laptop' (the four boxes keep their ports) · to_cloud(scene, future=
    ("nginx", "registry", "disk")) S16: the cluster again, the other layers back, the `future` parts
    GREY and faded, a GREY dashed chip 'Lectures 19–22' · swap_box(scene, key, text) a cluster box
    re-labels (S13: 'nginx' -> 'vector-db-loader').
    ANIM light(key, color) outline colour · dark(key) · normal(key).
    .layers{name} .boxes{key} .ports{'3000','9000','8000'} (PINK edge labels) .cluster_frame"""

    BOX = {"nginx": (4.1, 0.15), "app": (2.95, -1.0), "api": (5.2, -1.0), "vdb": (5.2, -2.3)}
    BOX_TEXT = {"nginx": "NGINX", "app": "Cheese App", "api": "API Service", "vdb": "Vector DB"}
    READY_C = (0.3, 1.0)

    def __init__(self, built: bool = False, size: float = 20, **kw):
        super().__init__(**kw)
        self.size = size
        self.layers = {}
        self.boxes, self.ports = {}, {}
        self.cluster_frame = None
        self.ready_chip = self.not_ready_mark = None
        self.order = ("title", "people", "tools", "vertex", "gcp", "app", "edges", "bucket", "registry",
                      "disk", "cluster")
        self.shown = []
        self._saved = {}
        if built:
            for n in self.order:
                if n == "app":
                    continue
                g = self._make(n)
                self.layers[n] = g
                self.add(g)
                self.shown.append(n)

    # -- builders
    def _edge_label(self, s: str) -> Text:
        return label(s, self.size, ROUTE)

    def _make(self, name: str) -> VGroup:
        sz, p = self.size, self.p
        if name == "title":
            return chip("technical architecture · the system's blueprint", S.GREY, size=22).move_to(p(0, 2.45))
        if name == "people":
            dev = VGroup(browser_icon(0.55, LAPTOP, None), label("developers · data scientists", sz, INK)).arrange(
                RIGHT, buff=0.2)
            usr = VGroup(browser_icon(0.55, LAPTOP, None), label("users", sz, INK)).arrange(RIGHT, buff=0.2)
            b1 = box(dev.width + 0.4, 0.62, LAPTOP, fill_opacity=0.1).move_to(p(-4.25, 1.72))
            b2 = box(3.4, 0.62, LAPTOP, fill_opacity=0.1).move_to(p(4.6, 1.72))
            dev.move_to(b1)
            usr.move_to(b2)
            g = VGroup(b1, dev, b2, usr)
            g.dev, g.users = b1, b2
            return g
        if name == "tools":
            c = VGroup(box(2.1, 0.62, LAPTOP, fill_opacity=0.1), label("Colab notebooks", sz, INK))
            c[1].move_to(c[0])
            gh = VGroup(box(2.1, 0.62, LAPTOP, fill_opacity=0.1), label("GitHub", sz, INK))
            gh[1].move_to(gh[0])
            c.move_to(p(-5.45, 0.35))
            gh.move_to(p(-5.45, -1.2))
            g = VGroup(c, gh)
            g.colab, g.github = c, gh
            return g
        if name == "vertex":
            fr = box(2.4, 1.25, CLOUD, fill_opacity=0.12)
            t = label("Vertex AI", sz, INK).next_to(fr.get_top(), DOWN, buff=0.12)
            gm = chip("Gemini", CLOUD, size=sz).move_to(fr).shift(DOWN * 0.18)
            g = VGroup(fr, t, gm).move_to(p(-2.6, 0.15))
            g.frame = fr
            return g
        if name == "gcp":
            fr = box(10.6, 4.5, CLOUD, dashed=True).move_to(p(1.2, -1.05))
            t = label("GCP", sz, CLOUD).move_to(fr.get_corner(DL) + np.array([0.4, 0.25, 0]))
            return VGroup(fr, t)
        if name == "app":
            g = VGroup(box(2.0, 0.9, LAPTOP, fill_opacity=0.1), label("App", 22, INK))
            g[1].move_to(g[0])
            return g.move_to(p(4.1, -1.0))
        if name == "edges":
            people = self.layers.get("people") or self._make("people")
            tools = self.layers.get("tools") or self._make("tools")
            vertex = self.layers.get("vertex") or self._make("vertex")
            e1 = arrow(np.array([tools.colab.get_x(), people.dev.get_bottom()[1], 0]), tools.colab.get_top(),
                       S.GREY)
            e2 = arrow(people.dev.get_bottom() + RIGHT * 1.0, vertex.frame.get_top(), S.GREY, buff=0.05)
            target = self.boxes["nginx"] if "nginx" in self.boxes else (self.layers.get("app") or self._make("app"))
            e3 = arrow(people.users.get_bottom(), target.get_top(), S.GREY, buff=0.05)
            l1 = self._edge_label("HTTPS 443").next_to(e1, RIGHT, buff=0.1)
            l2 = self._edge_label("HTTPS 443").next_to(e2, RIGHT, buff=0.1)
            l3 = self._edge_label("HTTP/HTTPS 80").next_to(e3, LEFT, buff=0.1)
            g = VGroup(e1, e2, e3, l1, l2, l3)
            g.users_edge, g.users_label = e3, l3
            return g
        if name == "bucket":
            b = bucket(None, 0.75, CLOUD)
            t = VGroup(label("GCS bucket", sz, INK), label("data & models", sz, S.GREY)).arrange(DOWN, buff=0.04)
            return VGroup(b, t).arrange(RIGHT, buff=0.2).move_to(p(-2.6, -1.75))
        if name == "registry":
            fr = box(2.5, 1.0, CLOUD, fill_opacity=0.1)
            t = label("Artifact Registry", sz, INK).next_to(fr.get_top(), DOWN, buff=0.1)
            imgs = VGroup(*[image_block(None, 0.5, 0.26) for _ in range(3)]).arrange(RIGHT, buff=0.12)
            imgs.next_to(t, DOWN, buff=0.1)
            return VGroup(fr, t, imgs).move_to(p(0.15, -2.35))
        if name == "disk":
            d = disk(0.5, CLOUD)
            t = label("persistent disk", sz, INK).next_to(d, DOWN, buff=0.08)
            g = VGroup(d, t).move_to(p(0.15, -0.55))
            e = Line(d.get_right() + RIGHT * 0.1, p(1.7, d.get_y() - self.ref.get_y()), color=S.GREY, stroke_width=3)
            el = self._edge_label("NFS").next_to(e, UP, buff=0.05)
            return VGroup(g, e, el)
        if name == "cluster":
            fr = RoundedRectangle(width=4.75, height=4.2, corner_radius=0.14, stroke_color=CLOUD,
                                  stroke_width=3).set_fill(tint(CLOUD, 0.06), 1).move_to(p(4.075, -1.05))
            t = VGroup(label("compute instance /", sz, S.GREY), label("Kubernetes cluster", sz, S.GREY)).arrange(
                DOWN, buff=0.04).move_to(fr.get_top() + DOWN * 0.36)
            self.cluster_frame, self.cluster_title = fr, t
            for k, (x, y) in self.BOX.items():
                b = cbox([self.BOX_TEXT[k]], 1.8, 0.58, size=sz, mono_font=False)
                b.name.move_to(b.frame)
                b.move_to(p(x, y))
                self.boxes[k] = b
            bx = self.boxes
            e1 = arrow(bx["nginx"].get_bottom() + LEFT * 0.5, bx["app"].get_top(), ROUTE, buff=0.04)
            e2 = arrow(bx["nginx"].get_bottom() + RIGHT * 0.5, bx["api"].get_top(), ROUTE, buff=0.04)
            e3 = arrow(bx["api"].get_bottom(), bx["vdb"].get_top(), ROUTE, buff=0.04)
            l1 = self._edge_label("HTTP 3000").next_to(e1.get_center(), LEFT, buff=0.12)
            l2 = self._edge_label("HTTP 9000").next_to(e2.get_center(), RIGHT, buff=0.12)
            l3 = self._edge_label("HTTP 8000").next_to(e3, LEFT, buff=0.1)
            self.ports = {"3000": l1, "9000": l2, "8000": l3}
            g = VGroup(fr, t, e1, e2, e3, *bx.values(), l1, l2, l3)
            return g
        raise ValueError(f"layer {name!r}: one of {self.order}")

    # -- PLAYS
    def layer(self, scene, name: str, run_time: float = 0.9):
        """PLAYS: one layer appears (the cluster replaces the GREY 'App' box)."""
        g = self._make(name)
        self.layers[name] = g
        anims = [FadeIn(g, lag_ratio=0.1)]
        if name == "cluster" and "app" in self.layers:
            old = self.layers.pop("app")
            self.shown.remove("app")
            self._detach(old)
            scene.add(old)
            self.show(scene, g, anims=anims + [FadeOut(old)], run_time=run_time)
            scene.remove(old)
            if "edges" in self.layers:                 # the users' arrow now ends on NGINX
                e = self.layers["edges"]
                new = arrow(self.layers["people"].users.get_bottom(), self.boxes["nginx"].get_top(), S.GREY, buff=0.05)
                scene.play(Transform(e.users_edge, new), e.users_label.animate.next_to(new, LEFT, buff=0.1),
                           run_time=0.4)
                self.heal(scene)
        else:
            self.show(scene, g, anims=anims, run_time=run_time)
        self.shown.append(name)
        return g

    def build(self, scene, names=None, per: float = 1.0):
        """PLAYS the layers in `names` (default: every layer, in order)."""
        for n in names or self.order:
            self.layer(scene, n, run_time=per)

    def _fade_anims(self, names, darkness: float):
        anims = []
        for n in names:
            m = self.layers[n]
            if n not in self._saved:
                self._saved[n] = m.copy()
            anims.append(m.animate.fade(darkness))
        return anims

    def _restore_anims(self):
        anims = [Transform(self.layers[n], c) for n, c in self._saved.items() if n in self.layers]
        self._saved = {}
        return anims

    def ghost(self, scene, keep=("cluster",), darkness: float = 0.75, run_time: float = 0.6):
        """PLAYS: every shown layer except `keep` fades to a ghost (unghost() restores it exactly)."""
        anims = self._fade_anims([n for n in self.shown if n not in keep], darkness)
        if anims:
            scene.play(*anims, run_time=run_time)
            self.heal(scene)

    def unghost(self, scene, run_time: float = 0.6):
        """PLAYS: the ghosted layers come back as they were."""
        anims = self._restore_anims()
        if anims:
            scene.play(*anims, run_time=run_time)
            self.heal(scene)

    def ready(self, scene, run_time: float = 0.5):
        """PLAYS: a GREEN 'App is ready!' chip pops up left of the cluster (APIs slide 20)."""
        c = ok_chip("App is ready!", size=22).move_to(self.p(*self.READY_C))
        c.box.set_fill(S.BG, 1)
        self.ready_chip = c
        return self.show(scene, c, anims=[GrowFromCenter(c)], run_time=run_time)

    def not_ready(self, scene, run_time: float = 0.7):
        """PLAYS: a RED line strikes the chip; under it, GREY 'Well not really, / we need to build it'
        (APIs slide 21; no smiley)."""
        st = strike(self.ready_chip, ERR)
        cap = VGroup(label("Well not really,", 20, S.GREY), label("we need to build it", 20, S.GREY)).arrange(
            DOWN, buff=0.06)
        cap.next_to(self.ready_chip, DOWN, buff=0.12)
        self.not_ready_mark = VGroup(st, cap)
        self.show(scene, st, run_time=run_time * 0.4, anims=[Create(st)])
        self.show(scene, cap, run_time=run_time * 0.6)
        return self.not_ready_mark

    def tick_build(self, scene, run_time: float = 0.5):
        """PLAYS (S16): a small GREEN tick and 'the pieces' under the not-ready caption."""
        cap = self.not_ready_mark[1]
        t = VGroup(check_glyph(0.28), label("the pieces", 20, OWN)).arrange(RIGHT, buff=0.08)
        t.next_to(cap, DOWN, buff=0.08)
        return self.show(scene, t, run_time=run_time)

    def to_laptop(self, scene, run_time: float = 1.2):
        """PLAYS (S02): every other layer ghosts; the cluster frame turns into a GREY laptop outline
        titled 'your laptop' (same place; the four boxes keep their ports). Returns the frame."""
        anims = self._fade_anims([n for n in self.shown if n != "cluster"], 0.8)
        anims += [self.cluster_frame.animate.set_stroke(LAPTOP).set_fill(S.BG, 1)]
        scene.play(*anims, run_time=run_time * 0.6)
        self.heal(scene)
        new_t = label("your laptop", 22, LAPTOP).move_to(self.cluster_title)
        self.cluster_title = self.swap(scene, self.cluster_title, new_t, run_time=run_time * 0.4)
        return self.cluster_frame

    def to_cloud(self, scene, future=("nginx", "registry", "disk"), run_time: float = 1.2):
        """PLAYS (S16): the laptop becomes the cluster again (BLUE, its title back), the other layers come
        back, the `future` parts (cluster box keys or layer names) turn GREY and faded, and a GREY dashed
        chip 'Lectures 19–22' appears under the registry. Returns the chip."""
        anims = self._restore_anims()
        anims.append(self.cluster_frame.animate.set_stroke(CLOUD).set_fill(tint(CLOUD, 0.06), 1))
        scene.play(*anims, run_time=run_time * 0.5)
        self.heal(scene)
        fut = [m for m in (self.boxes.get(k) or self.layers.get(k) for k in future) if m is not None]
        if fut:
            scene.play(*[m.animate.set_color(S.GREY).fade(0.5) for m in fut], run_time=run_time * 0.2)
            self.heal(scene)
        new_t = VGroup(label("compute instance /", self.size, S.GREY), label("Kubernetes cluster", self.size, S.GREY)
                       ).arrange(DOWN, buff=0.04).move_to(self.cluster_title)
        self.cluster_title = self.swap(scene, self.cluster_title, new_t, run_time=run_time * 0.3)
        ch = dashed_chip("Lectures 19–22").next_to(self.layers["registry"] if "registry" in self.layers
                                                   else self.cluster_frame, DOWN, buff=0.08)
        return self.show(scene, ch, run_time=0.4)

    def swap_box(self, scene, key: str, text: str, mono_font: bool = True, run_time: float = 0.6):
        """PLAYS: cluster box `key` re-labels (S13: swap_box(self, 'nginx', 'vector-db-loader')); the box
        widens when the new name needs it."""
        b = self.boxes[key]
        new = (mono if mono_font else label)(text, self.size, INK)
        if new.width > b.frame.width - 0.2:
            fr2 = RoundedRectangle(width=new.width + 0.35, height=b.frame.height, corner_radius=0.1,
                                   stroke_color=b.frame.get_stroke_color(), stroke_width=3).set_fill(
                                       tint(CONTAINER), 1).move_to(b.frame)
            scene.play(Transform(b.frame, fr2), run_time=run_time * 0.4)
            self.heal(scene)
        new.move_to(b.frame)
        b.name = self.swap(scene, b.name, new, run_time=run_time)
        return b

    # -- ANIM
    def light(self, key: str, color=TURN):
        """ANIM: a cluster box's outline in `color` (OWN: running; GREY: exited)."""
        return self.boxes[key].animate.set_stroke(color)

    def dark(self, key: str, darkness: float = 0.7):
        """ANIM: a cluster box fades (stopped); normal(key) brings it back."""
        return self.boxes[key].animate.fade(darkness)

    def normal(self, key: str):
        """ANIM: a box back to its built look (TEAL outline, full opacity)."""
        b = self.boxes[key]
        ref = b.copy()
        ref.frame.set_stroke(CONTAINER, opacity=1).set_fill(tint(CONTAINER), 1)
        ref.name.set_opacity(1)
        return Transform(b, ref)


# ------------------------------------------------------------------ V3 · ServerAppDiagram
class ServerAppDiagram(_Anchored):
    """V3 · uvicorn owns the socket, FastAPI is the app (S03, S04). 9.0 x 3.9, centred on the anchor
    (x -4.5 .. 4.5, y -1.95 .. 1.95; the eth0 plate overhangs the left wall to x -5.0). Fits above a
    3-row strip at move_to(UP * 0.75).
        container  TEAL, title 'container · cheese-app-api-service'
        eth0       GREY plate on the left wall (-4.5, 0.55): where the -p tunnel arrives
        lo         GREY plate 'lo · 127.0.0.1' inside (-3.2, -1.25): the container's own loopback
        uvicorn    PURPLE box x -1.9 .. 4.25 'uvicorn · the server'; PINK socket ':9000' on its left edge
        app card   PURPLE 'FastAPI · the app' x -1.0 .. 4.1; left half: the three api.service:app chips;
                   right half (x 1.45 .. 4.0): 'routes' and the route rows (mono 20, <= 14 characters,
                   longer rows switch to the label font: 'GET / → get_index' fits)
    PLAYS plates(scene) eth0 + lo appear · bind(scene, host='0.0.0.0'|'127.0.0.1') the GREEN badge on
    the socket and its line(s) to the plate(s) (flips if already bound) · split_target(scene, src=None)
    the PINK chips 'folder api/', 'file service.py', 'variable app' (fly from `src` if given) ·
    add_route(scene, text) a route row ('GET / → get_index') · reload(scene, routes) the app card slides
    out, a fresh one with `routes` slides in · walk_in(scene, source='eth0'|'inside', ok=True) a PINK
    request: ok -> GREEN tick at the socket, else it stops RED at the plate · watch(scene) an eye
    watches the 'folder api/' chip · note(scene, text) a GREY chip under the container.
    ANIM flash_route(i). .container .eth0 .lo .uvicorn .socket .badge .card .chips .routes"""

    def __init__(self, name: str = C_API, size: float = 20, **kw):
        super().__init__(**kw)
        p = self.p
        self.size = size
        self.container = RoundedRectangle(width=9.0, height=3.9, corner_radius=0.16, stroke_color=CONTAINER,
                                          stroke_width=3).set_fill(tint(CONTAINER, 0.08), 1).move_to(p(0, 0))
        self.title = VGroup(label("container ·", size, CONTAINER), mono(name, size, INK)).arrange(RIGHT, buff=0.12)
        self.title.move_to(p(0, 1.68)).align_to(self.container, LEFT).shift(RIGHT * 0.2)
        self.uvicorn = RoundedRectangle(width=6.15, height=3.15, corner_radius=0.12, stroke_color=TOOL,
                                        stroke_width=3).set_fill(tint(TOOL, 0.08), 1).move_to(p(1.175, -0.2))
        self.u_title = label("uvicorn · the server", size, TOOL).move_to(p(0, 1.15)).align_to(
            self.uvicorn, LEFT).shift(RIGHT * 0.2)
        self.socket = door(":9000", size=size).move_to(p(-1.9, 0.55))
        self.card = self._card([])
        self.add(self.container, self.title, self.uvicorn, self.u_title, self.card, self.socket)
        self.eth0 = self.lo = self.badge = None
        self.binds = VGroup()
        self.chips = VGroup()
        self.add(self.binds, self.chips)
        self.host = None

    def _card(self, routes) -> VGroup:
        p = self.p
        fr = RoundedRectangle(width=5.1, height=2.35, corner_radius=0.1, stroke_color=TOOL,
                              stroke_width=2.5).set_fill(tint(TOOL, 0.14), 1).move_to(p(1.55, -0.45))
        t = label("FastAPI · the app", self.size, TOOL).move_to(fr.get_corner(UL) + np.array([1.05, -0.24, 0]))
        t.align_to(fr, LEFT).shift(RIGHT * 0.18)
        hd = label("routes", self.size, S.GREY).move_to(p(1.55, 0.45))
        hd.set_x(p(1.45, 0)[0] + hd.width / 2)
        rows = VGroup()
        for r in routes:
            rows.add(self._route_row(r))
        g = VGroup(fr, t, hd, rows)
        g.frame, g.title, g.head, g.rows = fr, t, hd, rows
        self._place_rows(g)
        return g

    def _route_row(self, text: str):
        t = mono(text, self.size, INK)
        if t.width > 2.55:
            t = label(text, self.size, INK)
        return t

    def _place_rows(self, card):
        y0 = card.head.get_bottom()[1] - 0.12
        for i, r in enumerate(card.rows):
            r.move_to([0, 0, 0]).set_x(card.head.get_left()[0] + r.width / 2)
            r.set_y(y0 - 0.2 - i * 0.42)

    @property
    def routes(self):
        return self.card.rows

    def plates(self, scene, run_time: float = 0.6):
        """PLAYS: the 'eth0' plate on the container wall and the 'lo · 127.0.0.1' plate inside."""
        self.eth0 = door("eth0", color=S.GREY, size=self.size).move_to(self.p(-4.5, 0.55))
        self.lo = door("lo · 127.0.0.1", color=S.GREY, size=self.size, mono_font=False).move_to(self.p(-3.2, -1.25))
        return self.show(scene, self.eth0, self.lo, run_time=run_time)

    def bind(self, scene, host: str = "0.0.0.0", run_time: float = 0.7):
        """PLAYS: uvicorn binds `host`: a badge next to the socket ('0.0.0.0' GREEN with lines to eth0
        and lo; '127.0.0.1' GREEN with a line to lo only). Calling again flips it."""
        if self.eth0 is None:
            self.plates(scene)
        b = ok_chip(host, mono_font=True).move_to(self.p(-3.05, 0.0))
        b.box.set_fill(S.BG, 1)
        targets = [self.lo] if host.startswith("127.") else [self.eth0, self.lo]
        lines = [Line(b.get_left() if t is self.eth0 else b.get_bottom(),
                      t.get_right() + RIGHT * 0.02 if t is self.eth0 else t.get_top(),
                      color=OWN, stroke_width=3) for t in targets]
        sock_line = Line(b.get_right(), self.socket.get_left(), color=OWN, stroke_width=3)
        old = list(self.binds.submobjects)
        if old:
            self.drop(scene, *old, run_time=0.3)
        self.show(scene, sock_line, b, *lines, anims=[FadeIn(b), Create(sock_line)] + [Create(x) for x in lines],
                  run_time=run_time, into=self.binds)
        self.badge, self.host = b, host
        return b

    def split_target(self, scene, src=None, run_time: float = 0.9):
        """PLAYS: three PINK chips on the app card's left half, top to bottom: 'folder api/', 'file
        service.py', 'variable app' (flying out of `src`, e.g. the typed 'api.service:app', if given)."""
        parts = [("folder", "api/"), ("file", "service.py"), ("variable", "app")]
        chips = []
        for i, (k, v) in enumerate(parts):
            c = VGroup(label(k, self.size, S.GREY), mono(v, self.size, ROUTE)).arrange(RIGHT, buff=0.12)
            c.move_to(self.p(0, 0.15 - i * 0.48)).align_to(self.card.frame, LEFT).shift(RIGHT * 0.25)
            chips.append(c)
        if src is not None:
            anims = [LaggedStart(*[FadeIn(c, target_position=src.get_center()) for c in chips], lag_ratio=0.2)]
        else:
            anims = [LaggedStart(*[FadeIn(c, shift=RIGHT * 0.1) for c in chips], lag_ratio=0.2)]
        self.show(scene, *chips, anims=anims, run_time=run_time, into=self.chips)
        return self.chips

    def watch(self, scene, run_time: float = 0.5):
        """PLAYS: an eye (--reload) watches the 'folder api/' chip."""
        e = eye_glyph().next_to(self.chips[0] if len(self.chips) else self.card.title, RIGHT, buff=0.25)
        return self.show(scene, e, run_time=run_time)

    def add_route(self, scene, text: str, run_time: float = 0.5):
        """PLAYS: a route row writes into the table ('GET / → get_index')."""
        r = self._route_row(text)
        self.card.rows.add(r)
        self._place_rows(self.card)
        self.card.rows.remove(r)
        return self.show(scene, r, run_time=run_time, into=self.card.rows)

    def reload(self, scene, routes, run_time: float = 1.0):
        """PLAYS (StatReload): the app card slides out downwards, a fresh card with `routes` slides in
        from above. The api.service:app chips stay with the card (re-made)."""
        new = self._card(routes)
        keep_chips = len(self.chips) > 0
        old = [self.card] + (list(self.chips.submobjects) if keep_chips else [])
        self.drop(scene, *old, run_time=run_time * 0.45, shift=DOWN * 0.4)
        self.card = new
        self.show(scene, new, anims=[FadeIn(new, shift=DOWN * 0.4)], run_time=run_time * 0.55)
        # restore layering (socket and binds above the card)
        for m in (self.socket, self.binds):
            self.remove(m)
            self.add(m)
        if keep_chips:
            self.chips = VGroup()
            self.add(self.chips)
            self.split_target(scene, run_time=0.4)
        self.heal(scene)
        return new

    def walk_in(self, scene, source: str = "eth0", ok: bool = True, run_time: float = 1.0):
        """PLAYS: a PINK request dot from outside the wall (source='eth0') or from a small terminal
        glyph inside the container (source='inside', near lo). ok=True: it reaches the socket and a
        GREEN tick shows; ok=False: it stops at the plate with a RED cross. Returns the mark."""
        if self.eth0 is None:
            self.plates(scene)
        d = pulse_dot(ROUTE, 0.11)
        if source == "eth0":
            start, plate = self.eth0.get_left() + LEFT * 0.6, self.eth0
        else:
            start, plate = self.lo.get_bottom() + DOWN * 0.0 + LEFT * 1.0, self.lo
        d.move_to(start)
        scene.add(d)
        scene.play(d.animate.move_to(plate.get_center()), run_time=run_time * 0.5)
        if ok:
            scene.play(d.animate.move_to(self.socket.get_center()), run_time=run_time * 0.5)
            m = check_glyph(0.32, OWN).next_to(self.socket, DOWN, buff=0.1)
        else:
            m = cross_glyph(0.3, ERR).next_to(plate, UP, buff=0.08)
            scene.play(d.animate.set_color(ERR), run_time=0.2)
        scene.play(FadeIn(m), FadeOut(d), run_time=0.3)
        scene.remove(d)
        self.add(m)
        self.heal(scene)
        return m

    def note(self, scene, text: str, run_time: float = 0.4):
        """PLAYS: a GREY chip under the container ('extra arguments · none here')."""
        c = grey_chip(text).next_to(self.container, DOWN, buff=0.1).align_to(self.container, RIGHT)
        return self.show(scene, c, run_time=run_time)

    def flash_route(self, i: int, color=TURN):
        """ANIM: route row i flashes."""
        return Indicate(self.card.rows[i], color=color, scale_factor=1.08)


# ------------------------------------------------------------------ V4a · UrlCall
class UrlCall(_Anchored):
    """V4 (S04) · a URL becomes a function call. Centred on the anchor, 9.4 x 3.2 (y -1.45 .. 1.75):
        url        mono 26 'http://localhost:9000/square_root/' at y 1.45 (x from -4.65); the query
                   (add_query) continues it on the right
        captions   'scheme' 'host' 'port' 'path' 'query' under the tokens after split(), y 0.95
        signature  mono 24 'square_root(x: float = 1, y: float = 2)' centred, y 0.0
        body       mono 26 '√(x² + y²)' at y -1.1 (x from -3.2); the result to its right
    PLAYS split(scene) the tokens move apart, captions write · match(scene) the path token finds the
    signature (PINK arrow), the name lights, defaults turn YELLOW · add_query(scene, '?x=2&y=10') ·
    fly_args(scene, pairs=(('x=2', '2'), ('y=10', '10')), body='√(2² + 10²)') each query pair becomes a
    PINK chip under its default (the default dims) and the body row changes · result(scene,
    '10.198039027185569') the GREEN JSON number folds back next to the body · bounce(scene, 'x=abc',
    code='422 · float_parsing') a chip hits the first 'float' hint and bounces RED · uturn(scene, '307 → /square_root/') a PINK U-turn over the
    path · hints(scene, *targets, caption='type hints → validation + docs') the two 'float' hints
    glow and GREEN threads run to `targets` (mobjects) · reset(scene) back to the bare signature.
    .url (mono_line) .tokens{name} .query .sig (mono_line) .hint(i) .default(i) .body .res"""

    URL = "http://localhost:9000/square_root/"
    TOKS = (("scheme", "http://"), ("host", "localhost"), ("port", ":9000"), ("path", "/square_root/"))
    SIG = "square_root(x: float = 1, y: float = 2)"

    def __init__(self, url: str | None = None, size: float = 26, **kw):
        super().__init__(**kw)
        self.size = size
        url = url or self.URL
        self.url = mono_line(url, size, ROUTE)
        self.url.move_to(self.p(0, 1.45)).align_to(self.p(-4.65, 0), LEFT)
        self.url.shift(RIGHT * (self.p(-4.65, 0)[0] - self.url.strut.get_left()[0]))
        self.tokens = {k: substring(self.url, s) for k, s in self.TOKS if s in url}
        self.sig = mono_line(self.SIG, 24, INK, t2c={"float": TOOL})
        self.sig.move_to(self.p(0, 0.0))
        self.body = mono_line("√(x² + y²)", size, S.GREY)
        self.body.move_to(self.p(0, -1.1)).align_to(self.p(-3.2, 0), LEFT)
        self.add(self.url, self.sig, self.body)
        self.query = self.res = None
        self.captions = VGroup()
        self.marks = VGroup()
        self.add(self.captions, self.marks)
        self.split_done = False

    def hint(self, i: int = 0) -> VGroup:
        return substring(self.sig, "float", i)

    def default(self, i: int = 0) -> VGroup:
        return substring(self.sig, "= 1" if i == 0 else "= 2")[1:]

    def split(self, scene, gap: float = 0.32, run_time: float = 0.9):
        """PLAYS: the URL's tokens move apart and a GREY caption writes under each."""
        anims, caps = [], []
        for i, (k, s) in enumerate(self.TOKS):
            if k not in self.tokens:
                continue
            g = self.tokens[k]
            anims.append(g.animate.shift(RIGHT * gap * i))
        scene.play(*anims, run_time=run_time * 0.6)
        self.heal(scene)
        for k, g in self.tokens.items():
            caps.append(label(k, 20, S.GREY).next_to(g, DOWN, buff=0.22))
        self.show(scene, *caps, run_time=run_time * 0.4, into=self.captions)
        self.split_done = True
        return self.captions

    def match(self, scene, run_time: float = 0.9):
        """PLAYS: the path token finds its function: a PINK arrow to the name, the name YELLOW, the
        defaults YELLOW."""
        path = self.tokens["path"]
        name = substring(self.sig, "square_root")
        a = arrow(path.get_bottom() + DOWN * 0.45, name.get_top() + UP * 0.05, ROUTE, stroke=4, buff=0.02)
        self.show(scene, a, anims=[GrowArrow(a)], run_time=run_time * 0.5, into=self.marks)
        scene.play(*[g.animate.set_color(TURN) for g in (name, self.default(0), self.default(1))],
                   run_time=run_time * 0.5)
        self.heal(scene)
        return a

    def add_query(self, scene, q: str = "?x=2&y=10", run_time: float = 0.6):
        """PLAYS: the query string continues the URL (after the path token)."""
        qq = mono_line(q, self.size, ROUTE)
        path = self.tokens["path"]
        qq.next_to(path, RIGHT, buff=0.32 if self.split_done else 0.04)
        qq.shift(UP * (self.url.strut.get_y() - qq.strut.get_y()))
        self.query = qq
        self.show(scene, qq, anims=[FadeIn(qq, shift=LEFT * 0.2)], run_time=run_time)
        if self.split_done:
            c = label("query", 20, S.GREY).next_to(qq, DOWN, buff=0.22).align_to(self.captions[0], DOWN)
            self.show(scene, c, run_time=0.3, into=self.captions)
        return qq

    def fly_args(self, scene, pairs=(("x=2", "2"), ("y=10", "10")), body: str = "√(2² + 10²)",
                 run_time: float = 1.2):
        """PLAYS: each query pair becomes a PINK chip that flies onto its default (the default dims);
        the body row becomes `body`. Returns the chips."""
        chips = []
        for i, (pair, val) in enumerate(pairs):
            src = substring(self.query, pair)
            c = route_chip(f"{pair.split('=')[0]} = {val}", 20)
            c.next_to(self.default(i), DOWN, buff=0.14)
            c.box.set_fill(S.BG, 1)
            chips.append((src, c))
        anims = [FadeIn(c, target_position=src.get_center()) for src, c in chips]
        anims += [self.default(i).animate.set_opacity(0.3) for i in range(len(pairs))]
        self.show(scene, *[c for _, c in chips], anims=anims, run_time=run_time * 0.6, into=self.marks)
        new = mono_line(body, self.size, INK).move_to(self.body).align_to(self.body.strut, LEFT)
        self.body = self.swap(scene, self.body, new, run_time=run_time * 0.4)
        return [c for _, c in chips]

    def result(self, scene, text: str = "10.198039027185569", run_time: float = 0.7):
        """PLAYS: the answer, GREEN, folds back beside the body (an arrow '→' then the number)."""
        r = VGroup(label("→", 26, S.GREY), mono(text, 24, OWN)).arrange(RIGHT, buff=0.18)
        r.next_to(self.body, RIGHT, buff=0.3)
        if self.res is not None:
            self.res = self.swap(scene, self.res, r, run_time=run_time)
        else:
            self.res = r
            self.show(scene, r, anims=[FadeIn(r, shift=LEFT * 0.2)], run_time=run_time)
        return self.res

    def bounce(self, scene, text: str = "x=abc", code: str = "422 · float_parsing", run_time: float = 1.2):
        """PLAYS: a chip `text` flies from the query toward the first 'float' hint, turns RED and
        bounces back down; a RED `code` chip lands under the signature. Returns the RED chip."""
        c = route_chip(text, 20)
        c.box.set_fill(S.BG, 1)
        start = self.query.get_center() if self.query is not None else self.tokens["path"].get_center()
        c.move_to(start)
        scene.add(c)
        hit = self.hint(0).get_top() + UP * 0.25
        scene.play(c.animate.move_to(hit), run_time=run_time * 0.4)
        scene.play(c.animate.set_color(ERR).shift(UP * 0.35 + LEFT * 0.6), Indicate(self.hint(0), color=ERR),
                   run_time=run_time * 0.3)
        e = err_chip(code, 20).next_to(self.sig, DOWN, buff=0.15).align_to(self.hint(0), LEFT)
        scene.play(FadeOut(c), FadeIn(e), run_time=run_time * 0.3)
        scene.remove(c)
        self.marks.add(e)
        self.heal(scene)
        return e

    def uturn(self, scene, text: str = "307 → /square_root/", run_time: float = 0.8):
        """PLAYS: a PINK U-turn over the path token with `text` above it."""
        path = self.tokens["path"]
        a = CurvedArrow(path.get_corner(UR) + UP * 0.12, path.get_corner(UL) + UP * 0.12, angle=PI * 0.6,
                        color=ROUTE, stroke_width=4, tip_length=0.15)
        t = label(text, 20, ROUTE).next_to(a, UP, buff=0.04)
        self.show(scene, a, t, anims=[Create(a), FadeIn(t)], run_time=run_time, into=self.marks)
        return VGroup(a, t)

    def hints(self, scene, *targets, caption: str | None = "type hints → validation + docs",
              run_time: float = 1.0):
        """PLAYS: both 'float' hints glow YELLOW and GREEN threads run from them to `targets`; the
        caption writes under the body. Returns (threads, caption)."""
        scene.play(*[Indicate(self.hint(i), color=TURN) for i in (0, 1)], run_time=run_time * 0.4)
        th = [Line(self.hint(i % 2).get_bottom(), t.get_top() if t.get_y() < self.sig.get_y() else t.get_bottom(),
                   color=OWN, stroke_width=3) for i, t in enumerate(targets)]
        mobs = list(th)
        cap = None
        if caption:
            cap = label(caption, 22, OWN).next_to(self.body, DOWN, buff=0.25).align_to(self.body.strut, LEFT)
            mobs.append(cap)
        self.show(scene, *mobs, anims=[Create(t) for t in th] + ([FadeIn(cap)] if cap else []),
                  run_time=run_time * 0.6, into=self.marks)
        self.heal(scene)
        return th, cap

    def reset(self, scene, run_time: float = 0.4):
        """PLAYS: marks, results and value chips go; defaults back; the body back to √(x² + y²)."""
        mobs = list(self.marks.submobjects) + ([self.res] if self.res is not None else [])
        if mobs:
            self.drop(scene, *mobs, run_time=run_time)
        self.res = None
        scene.play(*[self.default(i).animate.set_opacity(1) for i in (0, 1)], run_time=0.2)
        new = mono_line("√(x² + y²)", self.size, S.GREY).move_to(self.body).align_to(self.body.strut, LEFT)
        self.body = self.swap(scene, self.body, new, run_time=run_time)


# ------------------------------------------------------------------ V4b · RouteTree
class RouteTree(_Anchored):
    """V4 (S08) · routers graft under prefixes. Laid out around the anchor, x -6.5 .. 6.2, y -1.85 ..
    1.85 (the hovering groups row at y 2.45; file_map adds 'chat.py' at y -2.1). Over a 3-row strip:
    shift(UP * 0.6) once the groups have snapped.
        '/api' root PINK (-5.6, 0.0) · '/' root (-6.1, 1.35) with 'healthz' (-4.6, 1.6) and 'readyz'
        (-4.6, 1.1) · stamp 'create_router' PURPLE (-5.2, -1.6)
        branch column x -2.4: 'square_root' 1.25 (add_leaf) · 'newsletters' 0.75 · 'podcasts' 0.25 ·
        'llm' -0.25 · 'llm-cnn' -0.75 · 'llm-rag' -1.25; each chat branch has a 'chats' child (x -0.45)
        and a WHITE mode label (left edge x 1.4, after the leaf dots: Ask / Identify / Cheese books)
        right column, left edge x 3.2: the route-group chips after snap() ('Agent Chat' under them,
        y -1.8), or the file chips of file_map()
    built=True: roots, newsletters, podcasts and the three chat branches at once.
    PLAYS roots(scene) · branch(scene, key) newsletters/podcasts · stamp(scene) the PURPLE stamp prints
    llm / llm-cnn / llm-rag (each with chats) · modes(scene) Ask / Identify / Cheese books ·
    probes(scene) '/' with healthz, readyz · groups(scene, y=2.45) the six slide-44 chips hover in a
    row · snap(scene) five snap onto their branches and turn GREEN, 'Agent Chat' stays GREY dashed
    (returns it) · add_leaf(scene, 'square_root') · leaves(scene) 25 small leaf dots (b32's real
    counts) + a GREY counter '25 operations' · path_label(scene, key, text) a PINK label beside a
    branch ('/api/newsletters') · file_map(scene) the README's file table on the tree (drops the
    groups). ANIM light(key, color).
    .nodes{key} (chips) .edges{key} .group_chips{name} .mode_labels{key}"""

    BR_X = -2.4
    BR_Y = {"square_root": 1.25, "newsletters": 0.75, "podcasts": 0.25, "llm": -0.25, "llm-cnn": -0.75,
            "llm-rag": -1.25}
    MODES = {"llm": "Ask", "llm-cnn": "Identify", "llm-rag": "Cheese books"}
    GROUP_OF = {"Newsletters": "newsletters", "Podcasts": "podcasts", "LLM Chat": "llm",
                "LLM + CNN Chat": "llm-cnn", "RAG Chat": "llm-rag", "Agent Chat": None}
    LEAVES = {"api": 1, "square_root": 1, "newsletters": 3, "podcasts": 3, "llm": 5, "llm-cnn": 5,
              "llm-rag": 5, "healthz": 1, "readyz": 1}                       # b32: 25 operations
    FILES = {"newsletters": "newsletter.py", "podcasts": "podcast.py", "llm": "llm_utils.py",
             "llm-cnn": "llm_cnn_utils.py", "llm-rag": "llm_rag_utils.py"}
    COL_X = 3.2

    def __init__(self, built: bool = False, size: float = 20, **kw):
        super().__init__(**kw)
        self.size = size
        self.nodes, self.edges, self.group_chips, self.mode_labels = {}, {}, {}, {}
        self.extra = VGroup()
        self.add(self.extra)
        if built:
            for m in self._roots():
                self.add(m)
            for k in ("newsletters", "podcasts", "llm", "llm-cnn", "llm-rag"):
                for m in self._branch(k):
                    self.add(m)

    def _node(self, text: str, color=ROUTE) -> VGroup:
        c = chip(text, color, size=self.size, font=MONO, fill_opacity=0.12)
        c.box.set_fill(tint(color, 0.12), 1)
        return c

    def _roots(self) -> list:
        api = self._node("/api").move_to(self.p(-5.6, 0.0))
        self.nodes["api"] = api
        return [api]

    def _branch(self, key: str) -> list:
        n = self._node(key).move_to(self.p(self.BR_X, self.BR_Y[key]))
        api = self.nodes["api"]
        e = Line(api.get_right(), n.get_left(), color=S.GREY, stroke_width=2.5)
        self.nodes[key], self.edges[key] = n, e
        out_ = [e, n]
        if key in self.MODES:
            ch = self._node("chats").move_to(self.p(-0.45, self.BR_Y[key]))
            e2 = Line(n.get_right(), ch.get_left(), color=S.GREY, stroke_width=2.5)
            self.nodes[key + "/chats"], self.edges[key + "/chats"] = ch, e2
            out_ += [e2, ch]
        return out_

    def roots(self, scene, run_time: float = 0.5):
        """PLAYS: the '/api' root appears."""
        return self.show(scene, *self._roots(), run_time=run_time)

    def branch(self, scene, key: str, run_time: float = 0.6):
        """PLAYS: one branch grows from /api ('newsletters', 'podcasts', or a chat key)."""
        parts = self._branch(key)
        anims = [Create(m) if isinstance(m, Line) else FadeIn(m) for m in parts]
        self.show(scene, *parts, anims=anims, run_time=run_time)
        return self.nodes[key]

    def stamp(self, scene, run_time: float = 1.8):
        """PLAYS: a PURPLE 'create_router' stamp under /api prints three identical chat branches
        (llm, llm-cnn, llm-rag, each with 'chats'), one by one. Returns the stamp."""
        st = tool_chip("create_router", self.size).move_to(self.p(-5.2, -1.6))
        self.show(scene, st, run_time=0.4)
        for k in ("llm", "llm-cnn", "llm-rag"):
            parts = self._branch(k)
            scene.play(Indicate(st, color=TURN, scale_factor=1.1), run_time=run_time * 0.12)
            anims = [Create(m) if isinstance(m, Line) else FadeIn(m, target_position=st.get_center())
                     for m in parts]
            self.show(scene, *parts, anims=anims, run_time=run_time * 0.2)
        self.stamp_chip = st
        return st

    def modes(self, scene, run_time: float = 0.9):
        """PLAYS: WHITE 'Ask', 'Identify', 'Cheese books' beside the three chat branches."""
        labs = []
        for k, m in self.MODES.items():
            t = label(m, self.size, INK).move_to(self.p(0, self.BR_Y[k]))
            t.set_x(self.p(1.4, 0)[0] + t.width / 2)
            self.mode_labels[k] = t
            labs.append(t)
        self.show(scene, *labs, anims=[LaggedStart(*[FadeIn(t) for t in labs], lag_ratio=0.3)], run_time=run_time)
        return labs

    def probes(self, scene, run_time: float = 0.7):
        """PLAYS: the '/' root with its two leaves 'healthz' and 'readyz' (top left)."""
        r = self._node("/").move_to(self.p(-6.1, 1.35))
        h = self._node("healthz").move_to(self.p(-4.6, 1.6))
        y = self._node("readyz").move_to(self.p(-4.6, 1.1))
        h.align_to(y, LEFT)
        e1 = Line(r.get_right(), h.get_left(), color=S.GREY, stroke_width=2.5)
        e2 = Line(r.get_right(), y.get_left(), color=S.GREY, stroke_width=2.5)
        self.nodes.update({"root": r, "healthz": h, "readyz": y})
        self.edges.update({"healthz": e1, "readyz": e2})
        return self.show(scene, e1, e2, r, h, y, run_time=run_time)

    def add_leaf(self, scene, key: str = "square_root", run_time: float = 0.6):
        """PLAYS: a new branch under /api (S08 b27: 'square_root', at the top of the column)."""
        return self.branch(scene, key, run_time=run_time)

    def groups(self, scene, y: float = 2.45, run_time: float = 0.9):
        """PLAYS: slide 44's six route groups hover in a row (WHITE-outlined chips). Returns them."""
        cs = []
        for name in ROUTE_GROUPS:
            c = chip(name, INK, size=self.size, fill_opacity=0)
            c.box.set_fill(S.BG, 1)
            cs.append(c)
        row = VGroup(*cs).arrange(RIGHT, buff=0.2).move_to(self.p(0, y))
        if row.width > 12.9:
            raise ValueError("groups row too wide")
        for n, c in zip(ROUTE_GROUPS, cs):
            self.group_chips[n] = c
        self.show(scene, *cs, anims=[LaggedStart(*[FadeIn(c, shift=DOWN * 0.1) for c in cs], lag_ratio=0.15)],
                  run_time=run_time)
        return cs

    def snap(self, scene, run_time: float = 1.2):
        """PLAYS: each group chip flies onto its branch (right column, left edge x 3.2) and turns GREEN;
        'Agent Chat' becomes a GREY dashed chip under them (y -1.8), unattached. Returns it."""
        anims = []
        for name, c in self.group_chips.items():
            key = self.GROUP_OF[name]
            if key is None:
                continue
            tgt = c.copy().set_x(self.p(self.COL_X, 0)[0] + c.width / 2).set_y(self.p(0, self.BR_Y[key])[1])
            anims.append(c.animate.move_to(tgt))
        scene.play(*anims, run_time=run_time * 0.6)
        scene.play(*[c.box.animate.set_stroke(OWN) for n, c in self.group_chips.items() if self.GROUP_OF[n]],
                   run_time=run_time * 0.2)
        old = self.group_chips["Agent Chat"]
        rag = self.group_chips["RAG Chat"]
        new = dashed_chip("Agent Chat", PAST, self.size).next_to(rag, DOWN, buff=0.2).align_to(rag, LEFT)
        self.group_chips["Agent Chat"] = self.swap(scene, old, new, run_time=run_time * 0.2)
        return self.group_chips["Agent Chat"]

    def leaves(self, scene, run_time: float = 1.4):
        """PLAYS: b32's 25 operations as small PINK leaf dots on their nodes, and a GREY counter
        '25 operations' (top right). Returns the counter."""
        dots = []
        for key, n in self.LEAVES.items():
            node = self.nodes.get(key + "/chats") or self.nodes.get(key)
            if node is None:
                continue
            row = VGroup(*[Dot(radius=0.06, color=ROUTE) for _ in range(n)]).arrange(RIGHT, buff=0.08)
            if key == "api":
                row.next_to(node, DOWN, buff=0.08)
            elif key == "readyz":
                row.next_to(node, DOWN, buff=0.08)
            else:
                row.next_to(node, RIGHT, buff=0.12)
            dots.append(row)
        cnt = label(f"{sum(self.LEAVES.values())} operations", 22, S.GREY).move_to(self.p(4.6, 1.6))
        self.show(scene, *dots, anims=[LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.12)],
                  run_time=run_time * 0.8, into=self.extra)
        self.show(scene, cnt, run_time=run_time * 0.2, into=self.extra)
        return cnt

    def path_label(self, scene, key: str, text: str, run_time: float = 0.5):
        """PLAYS: a PINK mono label on a branch's row, right of what the row already shows (node,
        leaf dots, mode label): path_label(self, 'newsletters', '/api/newsletters')."""
        node = self.nodes.get(key + "/chats") or self.nodes[key]
        y = node.get_y()
        right = node.get_right()[0]
        for m in [*self.extra.submobjects, *self.mode_labels.values()]:
            if abs(m.get_y() - y) < 0.15 and m.get_left()[0] >= node.get_left()[0] - 0.01:
                right = max(right, m.get_right()[0])
        t = mono(text, self.size, ROUTE)
        t.move_to([right + 0.2 + t.width / 2, y, 0])
        return self.show(scene, t, run_time=run_time, into=self.extra)

    def file_map(self, scene, run_time: float = 1.2):
        """PLAYS: the README's code table on the tree: the group chips go; GREY file chips appear in the
        right column per branch, 'chat.py' under the stamp
        (if shown), 'service.py' under /api, 'settings.py' top left, and a GREEN 'chat_utils.py · saves
        chats' row under the mode labels. Returns the file chips."""
        if self.group_chips:
            self.drop(scene, *self.group_chips.values(), run_time=0.3)
            self.group_chips = {}
        fs = []
        for k, f in self.FILES.items():
            if k in self.nodes:
                c = grey_chip(f, mono_font=True)
                c.set_x(self.p(self.COL_X, 0)[0] + c.width / 2).set_y(self.p(0, self.BR_Y[k])[1])
                fs.append(c)
        svc = grey_chip("service.py", mono_font=True)
        svc.move_to(self.p(-6.5 + svc.width / 2, -1.0))
        fs.append(svc)
        st = grey_chip("settings.py", mono_font=True)
        st.move_to(self.p(-6.5 + st.width / 2, 2.45))
        fs.append(st)
        if getattr(self, "stamp_chip", None) is not None:
            fs.append(grey_chip("chat.py", mono_font=True).next_to(self.stamp_chip, DOWN, buff=0.1))
        cu = VGroup(folder_glyph(0.3, OWN), mono("chat_utils.py", self.size, OWN),
                    label("saves chats", self.size, S.GREY)).arrange(RIGHT, buff=0.12)
        cu.move_to(self.p(0, -1.85))
        cu.set_x(self.p(0.45, 0)[0] + cu.width / 2)
        fs.append(cu)
        self.show(scene, *fs, anims=[LaggedStart(*[FadeIn(f) for f in fs], lag_ratio=0.1)], run_time=run_time,
                  into=self.extra)
        return fs

    def light(self, key: str, color=TURN):
        """ANIM: a node's outline in `color`."""
        return self.nodes[key].box.animate.set_stroke(color)


# ------------------------------------------------------------------ V6 · ProbeLamps
class ProbeLamps(_Anchored):
    """V6 (S07) · liveness vs readiness on the API container. Centred on the anchor (x -5.2 .. 5.0,
    y -1.4 .. 1.4); fits above a 3-row strip at shift(UP * 0.75).
        API box   TEAL x -5.2 .. 1.6, title 'cheese-app-api-service'
        lamps     '/healthz' (-3.9, 0.2) and '/readyz' (-1.6, 0.2), mono labels under them, a status
                  line under each (y -0.85)
        CNN ring  PURPLE progress ring (0.6, 0.75) 'CNN model' under it, wired to the readiness lamp
        vector DB small TEAL box 'cheese-app-' / 'vector-db' (3.9, -0.6), wired to the readiness lamp
    PLAYS set(scene, which='healthz'|'readyz', state='green'|'amber'|'red'|'off', status=None) ·
    fill_ring(scene, frac, run_time) · heartbeat(scene, beats=2) PINK pulses vector DB -> lamp ·
    bubble(scene, at=(0, -2.45)) the GREY dashed thought bubble 'Kubernetes (Lectures 19, 22) can use
    these': a load balancer sends PINK traffic only to GREEN-ready boxes, and a restart arrow by the
    liveness lamp (returns the bubble) · status(scene, which, text, color).
    .box .lamps{which} .labels{which} .statuses{which} .ring .ring_bg .vdb .wires"""

    LAMP = {"healthz": (-3.9, 0.2), "readyz": (-1.6, 0.2)}

    def __init__(self, size: float = 20, **kw):
        super().__init__(**kw)
        p = self.p
        self.size = size
        self.box = cbox([C_API], 6.8, 2.8, size=size)
        self.box.move_to(p(-1.8, 0))
        self.box.name.align_to(self.box.frame, UL).shift(np.array([0.18, -0.15, 0]))
        self.lamps, self.labels, self.statuses = {}, {}, {}
        for k, (x, y) in self.LAMP.items():
            lp = lamp("off").move_to(p(x, y))
            t = mono("/" + k, size, INK).next_to(lp, DOWN, buff=0.12)
            self.lamps[k], self.labels[k] = lp, t
        self.ring_bg = Circle(radius=0.36, stroke_color=S.GREY_DARK, stroke_width=6).move_to(p(0.6, 0.75))
        self.ring = Arc(radius=0.36, start_angle=PI / 2, angle=-0.001, color=TOOL, stroke_width=6).move_arc_center_to(p(0.6, 0.75))
        self.ring_label = label("CNN model", size, INK).next_to(self.ring_bg, DOWN, buff=0.1)
        self.frac = 0.0
        self.vdb = cbox(("cheese-app-", "vector-db"), 2.2, 0.84, size=size).move_to(p(3.9, -0.6))
        rl = self.lamps["readyz"]
        self.wire_cnn = Line(rl.get_right() + UP * 0.05, self.ring_bg.get_left(), color=S.GREY, stroke_width=2.5)
        self.wire_vdb = Line(rl.get_right() + DOWN * 0.1, self.vdb.get_left(), color=S.GREY, stroke_width=2.5)
        self.wires = VGroup(self.wire_cnn, self.wire_vdb)
        self.add(self.box, self.wires, self.ring_bg, self.ring, self.ring_label, self.vdb,
                 *self.lamps.values(), *self.labels.values())
        self.marks = VGroup()
        self.add(self.marks)

    def set(self, scene, which: str, state: str, status: str | None = None, status_color=None,
            run_time: float = 0.5):
        """PLAYS: a lamp changes state ('green', 'amber', 'red', 'off'); `status` (e.g. '200',
        '503 · CNN model is loading') writes under its label."""
        new = lamp(state).move_to(self.lamps[which])
        self.lamps[which] = self.swap(scene, self.lamps[which], new, run_time=run_time)
        if status is not None:
            col = status_color or {"green": OWN, "amber": AMBER, "red": ERR}.get(state, S.GREY)
            self.status(scene, which, status, col)
        return self.lamps[which]

    def status(self, scene, which: str, text: str, color=INK, run_time: float = 0.4):
        """PLAYS: the status line under a lamp (label 20)."""
        t = label(text, self.size, color).next_to(self.labels[which], DOWN, buff=0.14)
        if which in self.statuses:
            self.statuses[which] = self.swap(scene, self.statuses[which], t, run_time=run_time)
        else:
            self.statuses[which] = t
            self.show(scene, t, run_time=run_time)
        return self.statuses[which]

    def fill_ring(self, scene, frac: float = 1.0, run_time: float = 1.5):
        """PLAYS: the CNN ring fills to `frac` (0..1)."""
        c = self.ring_bg.get_center()
        new = Arc(radius=0.36, start_angle=PI / 2, angle=-TAU * max(frac, 0.001), color=TOOL,
                  stroke_width=6).move_arc_center_to(c)
        scene.play(Transform(self.ring, new), run_time=run_time)
        self.frac = frac
        self.heal(scene)

    def heartbeat(self, scene, beats: int = 2, run_time: float = 1.2):
        """PLAYS: PINK pulses travel from the vector DB to the readiness lamp (Chroma answers)."""
        for _ in range(beats):
            d = pulse_dot(ROUTE, 0.09).move_to(self.wire_vdb.get_end())
            scene.add(d)
            scene.play(MoveAlongPath(d, self.wire_vdb.copy().reverse_points()), run_time=run_time / beats * 0.8,
                       rate_func=linear)
            scene.remove(d)
        self.heal(scene)

    def bubble(self, scene, at=(0.0, -2.45), run_time: float = 1.2):
        """PLAYS: the dashed thought bubble (L19/L22): a PURPLE load-balancer chip sends PINK arrows to
        two GREEN-ready boxes and not to an amber one; a GREY restart arrow by the liveness lamp.
        Returns the bubble."""
        lb = tool_chip("load balancer", self.size, mono_font=False)
        bxs = VGroup(*[RoundedRectangle(width=0.7, height=0.42, corner_radius=0.06, stroke_color=c,
                                        stroke_width=3).set_fill(tint(c, 0.25), 1) for c in (OWN, OWN, AMBER)])
        bxs.arrange(RIGHT, buff=0.3)
        grp = VGroup(lb, bxs).arrange(RIGHT, buff=0.8)
        arrs = VGroup(*[Arrow(lb.get_right(), b.get_left(), buff=0.06, color=ROUTE, stroke_width=3,
                              tip_length=0.12) for b in bxs[:2]])
        arrs[1].put_start_and_end_on(lb.get_right(), bxs[1].get_bottom() + DOWN * 0.02)
        hd = label("Kubernetes (Lectures 19, 22) can use these", self.size, S.GREY)
        content = VGroup(hd, VGroup(grp, arrs)).arrange(DOWN, buff=0.18)
        b = thought_bubble(content).move_to([self.p(*at)[0], self.p(*at)[1], 0])
        rs = restart_glyph().next_to(self.lamps["healthz"], UP, buff=0.12)
        self.show(scene, b, rs, run_time=run_time, into=self.marks)
        return b


# ------------------------------------------------------------------ V7 · ChatFile
class ChatFile(_Anchored):
    """V7 (S09) · a chat is a file, not a memory. Centred on the anchor (x -6.5 .. 5.4, y -2.4 .. 1.9):
        browser   Browser('localhost:3000/chat', 3.3 x 2.4) at (-4.85, 0.55), with a PINK key
                  'X-Session-ID' in its page
        api       TEAL 'cheese-app-' / 'api-service' box (-1.2, 0.55), 2.8 x 1.5, a GREY memory bubble
                  above its right corner (dots = what it holds while answering)
        file      GREEN chat file (3.3, 0.55), 4.2 wide: 'chat-history/llm-cnn/' + '<session>/<chat>.json',
                  appended rows below the path
        copy2     the second API box (second_copy) at (-1.2, -1.45); cnn() puts a PURPLE 'CNN' box at the
                  same place (use one at a time)
        gemini    BLUE dashed 'Vertex AI · Gemini' cloud (3.6, -1.7) (gemini())
        images    'llm-cnn/images/' GREEN folder under the file (images())
    PLAYS post(scene, text='one message', key=True, ok=True, code='422') an envelope from the browser
    to the API (no key or ok=False: it bounces RED with `code`) · open_file(scene) · append(scene,
    *rows) rows like ('user', 'one message'), ('assistant', 'reply') write into the file · forget(scene)
    the memory bubble empties · remember(scene) it fills · cnn(scene, note='a guess') · gemini(scene,
    ok=False, cost='with your key: billed') the PINK arrow API -> cloud stops RED, GOLD cost tag ·
    second_copy(scene) another API box opens the same file · threads(scene) three PURPLE lanes in the
    API box, one held by a slow call · images(scene).
    .browser .key .api .bubble .memory .file .rows .copy2 .cnn_box .cloud .folder"""

    def __init__(self, size: float = 20, **kw):
        super().__init__(**kw)
        p = self.p
        self.size = size
        self.browser = Browser("localhost:3000/chat", 3.3, 2.4, size).move_to(p(-4.85, 0.55))
        self.browser.owner = self
        kg = key_glyph(0.6, ROUTE, dashed=False)
        self.key = VGroup(kg, mono("X-Session-ID", size, ROUTE)).arrange(DOWN, buff=0.1).move_to(self.browser.at(0, -0.1))
        self.api = cbox(("cheese-app-", "api-service"), 2.8, 1.5, size=size).move_to(p(-1.2, 0.55))
        self.api.name.align_to(self.api.frame, UL).shift(np.array([0.15, -0.12, 0]))
        bub = VGroup(Circle(radius=0.32), Circle(radius=0.1).shift(DL * 0.38), Circle(radius=0.06).shift(DL * 0.55))
        bub.set_stroke(S.GREY, 2).move_to(self.api.frame.get_corner(UR) + np.array([0.15, 0.35, 0]))
        self.bubble = bub
        self.memory = VGroup()
        self.file = self._file()
        self.rows = VGroup()
        self.add(self.browser, self.key, self.api, self.bubble, self.memory, self.rows)
        self.copy2 = self.cnn_box = self.cloud = self.folder = None
        self.file_on = False
        self.marks = VGroup()
        self.add(self.marks)

    def _file(self) -> VGroup:
        path = VGroup(mono(CHAT_DIR, self.size, INK), mono(CHAT_FILE, self.size, INK)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06)
        w = max(4.2, path.width + 0.4)
        fr = RoundedRectangle(width=w, height=2.0, corner_radius=0.1, stroke_color=OWN,
                              stroke_width=3).set_fill(tint(OWN, 0.08), 1)
        fr.move_to(self.p(3.3, 0.55))
        path.align_to(fr, UL).shift(np.array([0.2, -0.15, 0]))
        sep = Line(fr.get_left() + RIGHT * 0.1, fr.get_right() + LEFT * 0.1, color=OWN, stroke_width=1.5)
        sep.set_y(path.get_bottom()[1] - 0.1)
        g = VGroup(fr, path, sep)
        g.frame, g.path = fr, path
        return g

    def post(self, scene, text: str = "one message", key: bool = True, ok: bool = True, code: str = "422",
             run_time: float = 1.0):
        """PLAYS: a POST envelope (with a small PINK key when key=True) travels browser -> API. Without a
        key, or ok=False, it bounces back RED with a RED `code` chip under the browser (returned)."""
        env = envelope(text, ROUTE)
        if key:
            env.add(key_glyph(0.35, ROUTE, dashed=False).next_to(env, UP, buff=0.04))
        env.move_to(self.browser.frame.get_right() + RIGHT * 0.05 + UP * 0.6)
        env.shift(RIGHT * env.width / 2)
        scene.add(env)
        tgt = self.api.frame.get_left() + RIGHT * 0.1 + UP * 0.6
        if key and ok:
            scene.play(env.animate.move_to(tgt), run_time=run_time * 0.7)
            scene.play(FadeOut(env), Indicate(self.api.frame, color=TURN, scale_factor=1.03), run_time=run_time * 0.3)
            scene.remove(env)
            self.heal(scene)
            return None
        mid = (env.get_center() + tgt) / 2
        scene.play(env.animate.move_to(mid + RIGHT * 0.2), run_time=run_time * 0.4)
        scene.play(env.animate.set_color(ERR).move_to(env.get_center() + LEFT * 0.4 + DOWN * 0.3), run_time=run_time * 0.3)
        e = err_chip(code).next_to(self.browser.frame, DOWN, buff=0.12)
        scene.play(FadeOut(env), FadeIn(e), run_time=run_time * 0.3)
        scene.remove(env)
        self.marks.add(e)
        self.heal(scene)
        return e

    def open_file(self, scene, run_time: float = 0.7):
        """PLAYS: the GREEN chat file appears with a GREEN arrow API -> file."""
        a = arrow(self.api.frame.get_right(), self.file.frame.get_left(), OWN, stroke=3, buff=0.06)
        if not self.file_on:
            self.file_on = True
            self.show(scene, self.file, a, anims=[FadeIn(self.file), GrowArrow(a)], run_time=run_time)
        else:
            self.show(scene, a, anims=[GrowArrow(a)], run_time=run_time * 0.5, into=self.marks)
        self.file_arrow = a
        return self.file

    def append(self, scene, *rows, run_time: float = 0.8):
        """PLAYS: rows (role, text) write into the file under the path, e.g. ('user', 'one message'),
        ('assistant', 'reply'), ('cnn', 'a guess'). At most 3 rows on the card."""
        new = []
        for role, text in rows:
            col = {"user": INK, "assistant": OWN, "cnn": TOOL}.get(role, INK)
            r = VGroup(mono(role, self.size, col), label(text, self.size, S.GREY)).arrange(RIGHT, buff=0.15)
            new.append(r)
        if len(self.rows) + len(new) > 3:
            raise ValueError("ChatFile.append: at most 3 rows on the card")
        y0 = self.file.path.get_bottom()[1] - 0.38
        for i, r in enumerate(new):
            r.move_to([0, 0, 0]).align_to(self.file.path, LEFT).set_y(y0 - (len(self.rows) + i) * 0.4)
            r.set_x(self.file.path.get_left()[0] + r.width / 2)
        self.show(scene, *new, anims=[LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in new], lag_ratio=0.4)],
                  run_time=run_time, into=self.rows)
        return new

    def remember(self, scene, run_time: float = 0.4):
        """PLAYS: the memory bubble fills with three dots (the API holds the turn while answering)."""
        ds = VGroup(*[Dot(radius=0.05, color=INK) for _ in range(3)]).arrange(RIGHT, buff=0.06).move_to(self.bubble[0])
        self.show(scene, *ds, run_time=run_time, into=self.memory)

    def forget(self, scene, run_time: float = 0.5):
        """PLAYS: the memory bubble empties ('forgets')."""
        if len(self.memory):
            self.drop(scene, *list(self.memory.submobjects), run_time=run_time)

    def cnn(self, scene, note: str = "a guess", run_time: float = 0.6):
        """PLAYS: a PURPLE 'CNN' box under the API answers, with a GREY note chip. Returns the box."""
        b = tool_chip("CNN", 22, mono_font=False).move_to(self.p(-1.2, -1.2))
        a = arrow(self.api.frame.get_bottom(), b.get_top(), TOOL, stroke=3, buff=0.04)
        n = grey_chip(note).next_to(b, RIGHT, buff=0.15)
        self.cnn_box = b
        self.show(scene, a, b, n, run_time=run_time, into=self.marks)
        return b

    def gemini(self, scene, ok: bool = False, cost: str | None = "with your key: billed", run_time: float = 0.9):
        """PLAYS: the BLUE dashed cloud 'Vertex AI · Gemini' and a PINK arrow API -> cloud; ok=False:
        it stops RED at the cloud (a RED cross). A GOLD cost tag on the arrow. Returns the arrow."""
        cl = cloud_shape("Vertex AI\nGemini", CLOUD, cloud_w=2.0, dashed=True).move_to(self.p(3.6, -1.7))
        self.cloud = cl
        a = Arrow(self.api.frame.get_corner(DR) + LEFT * 0.3, cl.get_left() + RIGHT * 0.15, buff=0.05, color=ROUTE,
                  stroke_width=4, tip_length=0.18)
        mobs = [cl, a]
        if not ok:
            mobs.append(cross_glyph(0.3, ERR).move_to(a.get_end() + LEFT * 0.25 + UP * 0.25))
        if cost:
            ct = cost_tag(cost).next_to(a.get_center(), DOWN, buff=0.22)
            mobs.append(ct)
        self.show(scene, *mobs, anims=[FadeIn(cl), GrowArrow(a)] + [FadeIn(m) for m in mobs[2:]],
                  run_time=run_time, into=self.marks)
        return a

    def second_copy(self, scene, run_time: float = 0.9):
        """PLAYS: a second TEAL API box appears under the first and opens the same file (GREEN arrow)."""
        c2 = cbox(("cheese-app-", "api-service"), 2.8, 1.2, size=self.size).move_to(self.p(-1.2, -1.45))
        c2.name.align_to(c2.frame, UL).shift(np.array([0.15, -0.12, 0]))
        a = arrow(c2.frame.get_right(), self.file.frame.get_corner(DL) + UP * 0.3, OWN, stroke=3, buff=0.06)
        t = label("any copy can answer", self.size, OWN).next_to(c2, DOWN, buff=0.1)
        self.copy2 = c2
        self.show(scene, c2, a, t, anims=[FadeIn(c2, shift=DOWN * 0.2), GrowArrow(a), FadeIn(t)], run_time=run_time,
                  into=self.marks)
        return c2

    def threads(self, scene, run_time: float = 1.2):
        """PLAYS: three PURPLE lanes in the API box; lane 1 holds a slow call (a GOLD dot that crawls),
        quick PINK dots pass on lanes 2 and 3."""
        fr = self.api.frame
        lanes = VGroup(*[Line(fr.get_left() + RIGHT * 0.15, fr.get_right() + LEFT * 0.15, color=TOOL, stroke_width=2)
                         .set_y(fr.get_y() - 0.15 - i * 0.22) for i in range(3)])
        self.show(scene, lanes, run_time=0.4, into=self.marks)
        slow = Dot(radius=0.07, color=COST).move_to(lanes[0].get_start())
        fast = [Dot(radius=0.07, color=ROUTE).move_to(lanes[i].get_start()) for i in (1, 2)]
        scene.add(slow, *fast)
        scene.play(slow.animate.move_to(lanes[0].point_from_proportion(0.25)),
                   *[f.animate.move_to(l.get_end()) for f, l in zip(fast, lanes[1:])], run_time=run_time, rate_func=linear)
        scene.remove(*fast)
        self.marks.add(slow)
        self.heal(scene)
        return lanes

    def images(self, scene, run_time: float = 0.6):
        """PLAYS: a GREEN folder 'llm-cnn/images/' under the file, and a photo glyph lands in it."""
        f = VGroup(folder_glyph(0.34, OWN), mono("llm-cnn/images/", self.size, OWN)).arrange(RIGHT, buff=0.12)
        f.next_to(self.file.frame, DOWN, buff=0.2).align_to(self.file.frame, LEFT)
        ph = RoundedRectangle(width=0.36, height=0.28, corner_radius=0.04, stroke_color=INK, stroke_width=2)
        ph.add(Polygon([-0.12, -0.08, 0], [0.0, 0.06, 0], [0.12, -0.08, 0], stroke_color=INK, stroke_width=1.5))
        ph.next_to(f, RIGHT, buff=0.2)
        self.folder = f
        self.show(scene, f, ph, run_time=run_time, into=self.marks)
        return f


# ------------------------------------------------------------------ V8 · OneShell
class OneShell(_Anchored):
    """V8 (S10) · one HTML page per feature vs one app shell (Frontend slides 30–37). Centred on the
    anchor (x -6.2 .. 6.2, y -2.6 .. 2.3 with the address bar and the frameworks row):
        pages   four GREY page outlines 2.7 x 3.2 at x -4.65 / -1.55 / 1.55 / 4.65, y -0.2: each with a
                header strip, its name, and 'JS' / 'CSS' chips (pages(scene))
        shell   one outline 6.0 x 3.6 'single-page app · components' at (0, -0.1) (collapse(scene)),
                then Header ('Header · defined once') / middle block / Footer (shell(scene))
        address PINK address bar above the shell (address(scene, '/newsletters'))
    PLAYS pages(scene) · reload(scene, i) a GREY sweep over page i · notes(scene) GREY chips 'nothing
    shared', 'every page loads separately', 'slow' under the pages · collapse(scene) the four pages
    become one outline · frameworks(scene, hi='React') slide 33's four names as GREY chips, `hi`
    YELLOW (returns the row) · shell(scene) · page(scene, text) the middle block shows `text` ('Home',
    'Newsletters', 'Chat', 'Not found') while the header stays · pin_header(scene) a YELLOW pin on the
    header · address(scene, path) · outlet(scene) the middle block's tag becomes 'Outlet' · component
    (scene) a card 'function → markup (JSX)' left of the shell.
    .page_cards .outline .header .middle .footer .bar .note_chips"""

    NAMES = ("Home", "Newsletters", "Podcasts", "Chat")

    def __init__(self, size: float = 20, **kw):
        super().__init__(**kw)
        self.size = size
        self.page_cards = []
        self.outline = self.header = self.middle = self.footer = self.bar = self.mid_text = self.mid_tag = None
        self.note_chips = []

    def _page(self, name: str) -> VGroup:
        fr = RoundedRectangle(width=2.7, height=3.2, corner_radius=0.1, stroke_color=LAPTOP,
                              stroke_width=2.5).set_fill(PANEL, 1)
        hd = Rectangle(width=2.4, height=0.36, stroke_color=S.GREY, stroke_width=2).set_fill(S.GREY_DARK, 1)
        hd.move_to(fr.get_top() + DOWN * 0.35)
        ht = label("header", self.size, S.GREY).move_to(hd)
        nm = label(name, 22, INK).move_to(fr).shift(UP * 0.15)
        js = chip("JS", TOOL, size=self.size, font=MONO)
        css = chip("CSS", S.GREY, size=self.size, font=MONO)
        cs = VGroup(js, css).arrange(RIGHT, buff=0.15).move_to(fr.get_bottom() + UP * 0.45)
        g = VGroup(fr, hd, ht, nm, cs)
        g.frame = fr
        return g

    def pages(self, scene, run_time: float = 1.0):
        """PLAYS: the four separate pages."""
        ps = [self._page(n).move_to(self.p(x, -0.2)) for n, x in zip(self.NAMES, (-4.65, -1.55, 1.55, 4.65))]
        self.page_cards = ps
        self.show(scene, *ps, anims=[LaggedStart(*[FadeIn(p, shift=UP * 0.1) for p in ps], lag_ratio=0.2)],
                  run_time=run_time)
        return ps

    def reload(self, scene, i: int = 1, run_time: float = 0.7):
        """PLAYS: a GREY sweep over page i (the whole page loads again)."""
        fr = self.page_cards[i].frame
        sw = Rectangle(width=fr.width - 0.1, height=0.3, stroke_width=0).set_fill(S.GREY, 0.45)
        sw.move_to(fr.get_top() + DOWN * 0.2)
        scene.add(sw)
        scene.play(sw.animate.move_to(fr.get_bottom() + UP * 0.2), run_time=run_time, rate_func=linear)
        scene.remove(sw)

    def notes(self, scene, texts=("nothing shared", "every page loads separately", "slow"), run_time: float = 0.9):
        """PLAYS: GREY chips under the pages (y -2.25), one by one. Returns them."""
        cs = [grey_chip(t) for t in texts]
        row = VGroup(*cs).arrange(RIGHT, buff=0.3).move_to(self.p(0, -2.25))
        self.note_chips = cs
        self.show(scene, *cs, anims=[LaggedStart(*[FadeIn(c) for c in cs], lag_ratio=0.4)], run_time=run_time)
        return list(row)

    def collapse(self, scene, run_time: float = 1.0):
        """PLAYS: the four pages (and the notes) become one outline 'single-page app · components'."""
        ol = RoundedRectangle(width=6.0, height=3.6, corner_radius=0.12, stroke_color=LAPTOP,
                              stroke_width=3).set_fill(PANEL, 1).move_to(self.p(0, -0.1))
        t = label("single-page app · components", 22, INK).move_to(ol)
        if self.note_chips:
            self.drop(scene, *self.note_chips, run_time=0.3)
            self.note_chips = []
        olds = self.page_cards
        for o in olds:
            self._detach(o)
        scene.add(*olds)
        copies = [ol.copy() for _ in olds]
        scene.play(*[ReplacementTransform(o, c) for o, c in zip(olds, copies)], run_time=run_time * 0.7)
        scene.remove(*olds, *copies)
        self.page_cards = []
        self.outline = ol
        self.ol_title = t
        self.add(ol)
        self.heal(scene)
        self.show(scene, t, run_time=run_time * 0.3)
        return ol

    def frameworks(self, scene, hi: str = "React", run_time: float = 0.8):
        """PLAYS: slide 33's frameworks as GREY chips under the outline (y -2.35), `hi` YELLOW."""
        cs = [chip(n, TURN if n == hi else S.GREY, size=22) for n in FRAMEWORKS]
        row = VGroup(*cs).arrange(RIGHT, buff=0.3).move_to(self.p(0, -2.35))
        self.fw = row
        self.show(scene, *cs, anims=[LaggedStart(*[FadeIn(c) for c in cs], lag_ratio=0.2)], run_time=run_time)
        return row

    def shell(self, scene, first: str = "Home", run_time: float = 1.0):
        """PLAYS: inside the outline: Header ('Header · defined once'), the middle block (`first`), the
        Footer. The outline's title goes."""
        ol = self.outline
        hd = Rectangle(width=5.6, height=0.6, stroke_color=TOOL, stroke_width=2.5).set_fill(tint(TOOL, 0.15), 1)
        hd.move_to(ol.get_top() + DOWN * 0.5)
        ht = label("Header · defined once", 22, INK).move_to(hd)
        ft = Rectangle(width=5.6, height=0.5, stroke_color=S.GREY, stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
        ft.move_to(ol.get_bottom() + UP * 0.45)
        ftt = label("Footer", 20, S.GREY).move_to(ft)
        md = Rectangle(width=5.6, height=hd.get_bottom()[1] - ft.get_top()[1] - 0.3, stroke_color=S.GREY,
                       stroke_width=2).move_to((hd.get_bottom() + ft.get_top()) / 2)
        mt = label(first, 26, INK).move_to(md)
        self.header, self.footer, self.middle, self.mid_text = VGroup(hd, ht), VGroup(ft, ftt), md, mt
        if getattr(self, "ol_title", None) is not None:
            self.drop(scene, self.ol_title, run_time=0.3)
            self.ol_title = None
        self.show(scene, self.header, md, mt, self.footer, run_time=run_time)
        return self.header

    def page(self, scene, text: str, run_time: float = 0.5):
        """PLAYS: the middle block swaps to `text`; the header does not move."""
        new = label(text, 26, ERR if text == "Not found" else INK).move_to(self.middle)
        self.mid_text = self.swap(scene, self.mid_text, new, run_time=run_time)
        return self.mid_text

    def pin_header(self, scene, run_time: float = 0.4):
        """PLAYS: a YELLOW pin on the header's right end."""
        pin_ = VGroup(Circle(radius=0.13, stroke_color=TURN, stroke_width=3).set_fill(TURN, 0.8),
                      Line(DOWN * 0.13, DOWN * 0.38, color=TURN, stroke_width=4))
        pin_.move_to(self.header[0].get_right() + np.array([-0.35, 0.05, 0]))
        self.pin = pin_
        return self.show(scene, pin_, anims=[FadeIn(pin_, shift=DOWN * 0.2)], run_time=run_time)

    def address(self, scene, path: str = "/", run_time: float = 0.5):
        """PLAYS: a PINK address bar above the shell shows `path` (the first call draws the bar)."""
        t = mono(path, 22, ROUTE)
        if self.bar is None:
            b = RoundedRectangle(width=6.0, height=0.48, corner_radius=0.24, stroke_color=S.GREY,
                                 stroke_width=2).set_fill(TERM_BG, 1)
            b.next_to(self.outline, UP, buff=0.12)
            t.move_to(b).align_to(b, LEFT).shift(RIGHT * 0.25)
            self.bar, self.bar_text = b, t
            self.show(scene, b, t, run_time=run_time)
        else:
            t.move_to(self.bar_text).align_to(self.bar, LEFT).shift(RIGHT * 0.25)
            self.bar_text = self.swap(scene, self.bar_text, t, run_time=run_time)
        return self.bar_text

    def outlet(self, scene, run_time: float = 0.5):
        """PLAYS: a PINK tag 'Outlet' on the middle block's top-left corner."""
        t = tag("<Outlet />", ROUTE, size=20)
        t.move_to(self.middle.get_corner(UL) + np.array([t.width / 2 + 0.1, -0.25, 0]))
        self.mid_tag = t
        return self.show(scene, t, run_time=run_time)

    def component(self, scene, run_time: float = 0.6):
        """PLAYS: a PURPLE-outlined card 'function → markup (JSX)' left of the outline. Returns it."""
        c = card(["function → markup", "(JSX)"], TOOL, size=22)
        c.next_to(self.outline, LEFT, buff=0.25)
        if c.get_left()[0] < -SAFE_X:
            c.next_to(self.outline, UP, buff=0.15)
        return self.show(scene, c, run_time=run_time)
