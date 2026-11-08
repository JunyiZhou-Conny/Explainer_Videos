"""Shared scene code for AC215 L22 (Scaling: Kubernetes in the cloud; follow-along of dlops-io/cheese-app-v3
@ 3ecef56 = main on 2026-11-07, README sections "Create Simple Kubernetes Cluster Tutorial" (done first,
as the lecture does), "Deployment with Scaling using Kubernetes", "Create & Deploy Cluster" and the
Kubernetes half of "Debugging Containers").

Paths, narration (SAY lines straight from script.md), the semantic colours of BRIEF.md, the running
example (placeholders only: your-gcp-project, <IP>, sa_000…), the four README trackers, loaders for
the real captures in assets/terminal/{laptop,kind} (masked on load), the README's Outputs block in
assets/terminal/expected, source panels from assets/source, terminal helpers, tags, chips, cards and
the video's set pieces V1-V8 plus AsksChecklist, KubectlGrammar, StackPipe and DoorsStrip. Generic
helpers come from L20's common.py (tested there); the set pieces are new. build/common_test.py plays
every helper and piece once (Bench*: explainer.check clean).

    from manim import *          # first
    from common import *         # second (common's names win), then:
    SAY = NARRATION["S07"]; assert len(SAY) == SAY_COUNT["S07"]   # one voiceover block per SAY

Notes for scene authors
=======================
Rules. Every text here is >= 20 pt and nothing scales text: never .scale() a group that holds text
below 1.0 (pieces take size / width parameters). Never set width / height / color / depth / name on a
VGroup subclass (Manim properties) and never give a piece a method or attribute named like a Mobject
method (add, remove, restore, center, clear, owner …). Methods marked PLAYS take the scene first, play
their own animation and keep the new mobjects inside the piece, so a later FadeOut(piece) takes them
all. ANIM methods return an animation you play. To take one part away use piece.drop(self, part):
never FadeOut a member of a piece directly (it snaps back when the piece is next drawn). Place a piece
(shift / move_to) BEFORE its first PLAYS call or between calls: PLAYS methods build new parts at the
piece's current position. Split trap: animating a group that is not itself on the scene splits every
parent holding those members; re-seat with piece.heal(self) (PLAYS methods do it) or self.add(parent).
Piece.swap() cross-fades (FadeTransform); swap(..., morph=True) for a point-by-point morph.
No prices on screen except S09's one GOLD line (cost_tag allows an amount only with '≈' and 'roughly').
Staff branch: Capture.line()/at()/pick() refuse any line naming a work/ branch, type_capture() refuses
a command that names one: p02 is typed as capture("p02").typed("%s'") and only p02:2 is printed.

Frame budget. Safe frame x in [-6.6, 6.6], y in [-3.6, 3.6]. Tracker top-left (left -6.5, top 3.5,
lowest point TRACK_BOTTOM 2.9); lecture tag lref("22–26") top right (bottom LREF_BOTTOM ~3.13);
pictures stay below PIC_TOP 2.8. The small AsksChecklist sits top right x 3.77 .. 6.55, y 1.55 ..
3.05: while it is on screen keep that corner free (ControllerLoop and RequestJourney already do).
Terminals: term() is 12.6 wide, bottom edge at BOTTOM -3.5; a 3-row strip's top is STRIP_TOP
(about -1.44), so a picture over a strip lives in y in [-1.3, 2.8] (V1, V4, V6, StackPipe are built
for exactly that band).

Data
    NARRATION["S01"] .. ["S16"]  SAY_COUNT  TITLES[cls]  SPEC (video.yaml)
    Prompts P_LAPTOP 'student@laptop:~$' (= P_HOME) · P_REPO · P_SRC …/cheese-app-v3/src$ (the README's
    `cd deployment` starts here) · P_DEPLOY …/src/deployment$ · P_TOOLBOX read from b03:77
    ('root@<id>:/app#', the id never read aloud) · toolbox_prompt(path) ('/app/deploy_images',
    '/app/deploy_k8s'). Titles T_LAPTOP 'laptop', T_TOOLBOX 'laptop · toolbox', T_TB_STANDIN
    'laptop · toolbox · stand-in' (kubectl on kind), T_LAPTOP_STANDIN 'laptop · stand-in' (k01, k81).
    Names PROJECT_PH 'your-gcp-project' · PROJECT_README 'ac215-project' (always with default_tag) ·
    IP_PH '<IP>' · EXT_IP '<EXTERNAL-IP>' · HOST_PH '<IP>.sslip.io' · APP_URL 'http://<IP>.sslip.io' ·
    SA_MASK 'sa_000000000000000000000' · NAMESPACE 'cheese-app-namespace' · OLD_NAMESPACE
    'cheese-app-cluster-namespace' · CLUSTER · TEST_CLUSTER · ZONE_TEST 'us-east1-c' · REGION
    'us-central1' · VPC · SUBNET_RANGE · INGRESS 'cheese-app-ingress' · HELM_RELEASE 'nginx-f5' · KSA
    'api-ksa' · STACK_REF 'organization/deploy-images/dev' · MACHINE 'n2d-standard-2' · C_TOOLBOX ·
    PORTS{front 3000, api 9000, vdb 8000, lb 80} · SVC_NAMES{front, api, vdb} · the stand-in's
    tic-tac-toe: RS_HASH '5cd9789488', POD_SUFFIXES ('5h48s', 'bmkj5'), NEW_SUFFIX 'lmk52',
    SCALE_SUFFIXES ('gmbqz', 'grq79'), SVC_IP, ENDPOINTS, NEW_POD_IP, DNS_NAME · VERSIONS{…} ·
    ASKS / ASK_NOTES / ASK_ANSWERS (slide 12, S16) · PARTS / CALLOUTS (V1, slides 25-26) ·
    BLUEPRINT_ROWS (V5's L20 → L22 table) · TREE_GROUPS / TREE_READS (V6, c20's 22 + the stack = 23)
    · REQUESTS (V8) · STATUS_COL (Pod status words).
    unname(s) / mask(s): instructor → '‹instructor›', staff branch → 'work/…', sa_<digits> → SA_MASK.

Colours (BRIEF "Colours"): LAPTOP / BROWSER / YOU / STANDIN GREY · CLOUD / NODE BLUE · CONTAINER /
    IMAGE / POD TEAL · SHARED / SYSTEM ORANGE · OWN / DECLARED GREEN · TOOL PURPLE · ERR RED · TURN
    YELLOW · COST GOLD · ROUTE / SVC PINK · PAST / FUTURE GREY dashed · INK WHITE.

Trackers (script.md conventions; placed top-left)
    tracker_w(step=None, extra=False) README › Create Simple Kubernetes Cluster Tutorial, 11 steps ·
    tracker_d(...) README › Deployment with Scaling using Kubernetes, 7 · tracker_c(...) README ›
    Create & Deploy Cluster, 8 · tracker_g(...) README › Debugging Containers, 4 · tracker(key, …) key
    'W' | 'D' | 'C' | 'G'. extra: True (' · extra') | 'our spelling' | 'not for you' | 'recording
    only' | 'stand-in' (' · extra · …') | any other str (appended after ' · ').
    track(tr, k, extra) ANIM (never tr.goto) · lref("7"), lref("22–26"), lref("7, 18, 30, 36, 39") the
    GREY 'Lecture 22 · slide(s) …' tag, top right.

Captures (assets/terminal/<folder>/<id>-*.txt; capture-only/ is refused; masked on load)
    Folders: assets/terminal/laptop (a fresh Docker 29.8.2 engine standing in for the laptop: p01-p05
    clone/secrets, b01-b52 the README's commands in the toolbox, c00-c23 extras on Pulumi's local
    backend), assets/terminal/kind (the kind stand-in cluster, NOT GKE: k00-k81; every panel from it
    carries standin_tag / standin_row) and assets/terminal/expected (readme-pulumi-outputs.txt only,
    via recorded() / quote_card()).
    c = capture("b03") (laptop: b*, c*, p*) · capture("k50") (kind: 'k' + digits) · capture("b31-2") /
    capture("c11-3") (the config-set triples) · capture("kind/k51").
    c.cmd_lines (typed rows) c.cmd c.k · c.at(*spec) output by FILE line numbers (ints, (a, b), '…');
    refuses the command lines, [exit N] and staff-branch lines · c.crop(n, "404  Not Found") ·
    c.typed(upto) (script.md's `typed crop "…"`: line 1 up to `upto`) · c.line(n) · c.pick(*ranges)
    L1-style (body index = file line − k) · c.lines c.exit c.raw c.path c.key.
    CMD_LINES: kind/k51 holds two commands (kubectl exec …, then 'hostname; ls; exit' at the Pod's $):
    type_capture(self, t, "k51", prompts=[toolbox_prompt(), "$"]).
    type_capture(scene, t, c, prompts=None) PLAYS types the command right (continuation rows after a
    trailing '\\' have no prompt) · type_at(scene, t, cap, n) types a command at the container prompt
    printed on file line n · recorded("readme-pulumi-outputs", (2, 9), plain=False) ·
    quote_card("readme-pulumi-outputs", (2, 9), source="README:497–506", mono_font=True) (S14's
    EXPECTED panel; line 1 is provenance and refused).

Sources (assets/source/<path> = cheese-app-v3 @ 3ecef56; header '<path> · lines a–b')
    code(path, a, b=None, focus=, font_size=22, cuts={line: 'cut after'}, elide={line: 'middle'},
        dedent=False, shown='short/header/path') CODE() panel, <= 12 lines, must fit (22 pt ~66
        characters, 20 pt ~74; a wider panel raises and names the line), e.g.
        code("src/deployment/deploy-k8s-tic-tac-toe.yml", 24, 35). .code .header; highlight with
        code_span(p.code, k, "x") / line_bar(p.code, k, colour), k = file line - a. Refuses a range
        that includes src/vector-db/cli.py:75 or :440 (they name the instructor).
    excerpt(path, a, b) / source_text(path) / readme(n) / readme_lines(a, b) (card text) ·
    readme_rows(a, b) (command rows for type_lines) · readme_card((a, b), body).

Terminals (house: 12.6 wide, 22 pt = 65 characters a row; 20 pt = 72)
    term(prompt, rows, title) · laptop_term(rows=10, prompt=P_LAPTOP, standin=False) ·
    toolbox_term(rows, path='/app', standin=False) · standin_term(rows, path) (= toolbox_term(…,
    standin=True); put on_bar(t, standin_row()) on it) · resize(scene, t, rows) PLAYS · retitle(t,
    title) ANIM · room · bare_prompt · type_cmd(scene, t, cmd, soft=None) · type_capture · type_at ·
    type_lines(scene, t, readme_rows(a, b)) · out(scene, t, lines, wrap=) · cd_prompt(scene, t, prompt)
    · beside / pin / unpin / attach / on_bar / under_term for tags at a row · row_tag, turn_row,
    extra_row(kind), time_row, cost_row, default_row, standin_row (tags sized for a terminal row) ·
    no_panel_chip().

Tags and chips (GREY unless said; all 20-22 pt)
    your_turn() YELLOW · extra_tag(kind) · standin_tag() 'stand-in: kind, not GKE' · placeholder_tag()
    'placeholder image tags · nothing built' (c20, c21) · illustration_tag(s) · expected_tag(source) ·
    recorded_tag(source) · recording_tag() 'at the time of recording' · erratum_tag(s) · default_tag()
    "the README's default · change to yours" · cost_tag(text) GOLD (raises on an amount unless the text
    has '≈' and 'roughly') · dont_forget_card(sub=None) GOLD 'Don't forget to delete' (S08, S16) ·
    scene_chip(s) · grey_chip · dashed_chip (past/future) · tool_chip PURPLE · err_chip RED · ok_chip
    GREEN · route_chip PINK · box_chip TEAL · two_row_chip(top, bottom, colour) · differ_chip ·
    file_card(path) · card(lines, head=) · question_card(text) YELLOW · sticky(text) · ponder(scene, q,
    seconds) PLAYS (opaque pause_and_ponder card; FadeOut it at the next block) · flash_tag(scene, tg) ·
    console_form(title, fields) · console_view(path, rows) (schematic console: breadcrumb crumbs
    .crumbs[i] + BLUE rows, 'illustration' tag) · Checklist(title, items, color, tag_text, dashed)
    .tick(scene, i) (S04/S10's APIs, S16's audit).

Glyphs (text-free unless named; sizes in scene units)
    pod_glyph(name=None, status=None, r=0.26, dots=2, side=DOWN) TEAL Pod (.circle .dots .name .status)
    · pod_name(name) the three-colour 'web-5cd9789488-5h48s' (.hash ringed GREEN) · pod_status(word)
    · node_box(title, box_w, box_h) BLUE node (.frame .title) · frame_box(w, h, colour, dashed=) opaque
    box (.fill .edge) · boxed(rows, colour, box_w, box_h, mono_font=, dashed=) labelled box (.frame
    .text; raises when the text does not fit) · dns_card(name, ip) PINK · port_path() S06's three PINK
    ports · ttt_grid() the game's 3 x 3 · browser_window(url, rows) Browser + 'illustration' tag above
    it (PLAYS goto / fill / reload / clear) · l20_vm(box_w, box_h) L20's VM, GREY dashed (.boxes{nginx,
    api, front, vdb, loader}) · hourglass · clock_face(r, colour, hour) · lever_glyph(h, colour, on) ·
    phone_glyph · ring_arrows(radius, colour) · tint · cbox · svc_box · door(port) · mini_browser ·
    disk_cyl(w) · pail · bucket · disk · key_icon · padlock(h, colour, text) · scissors(h) ·
    crate(name) · lamp(state) · envelope · image_block · file_icon / folder_icon · cloud_shape · you() ·
    check_glyph / cross_glyph · arrow / route / travel / bounce / pulse_dot · ring / under / strike /
    hl_bar · outline_box · keep_inside(m). CostDial(radius, caption) GOLD needle meter:
    .run(scene, turns, seconds) · .freeze().

Set pieces (V numbers = BRIEF; each class doc gives its exact layout and every method)
    AsksChecklist(small=False, ticked=(), notes=None, center=None) full ~5.6 x 3.3 at ORIGIN; small:
        top right x 3.77 .. 6.55, y 1.55 .. 3.05. PLAYS light(i) · tick(i, dashed=False, note=None) ·
        note(i, text, colour) · answer(i) (ASK_ANSWERS, GREEN) · shrink · grow(center). .card .ticks
    KubectlGrammar(size=22) ~12.4 x 2.1 at ORIGIN (example y 0.65, slots y -0.15, slot labels y -0.85).
        PLAYS fill(command, TYPE, NAME, flags) · flag(s, colour=ROUTE) · name_note(text).
    V1 MasterDiagram(standin=False, workers=None, built=()) x -6.45 .. 6.45, y -1.25 .. 2.75 (left
        column: cloud provider API over 'your laptop' + toolbox chips; cluster box x -3.35 ..: control
        plane x -3.2 .. 0.3, workers x 0.6 .. 6.3); callout slot under it at slot_y (S03 shifts it
        down ~0.6). built=('laptop', 'cluster', 'plane', 'parts', 'beat23') draws those at once.
        PLAYS laptop_box(chips) · add_chips(names) · cluster(source=None) · beat22 · beat23 · part(key)
        · beat24 · callout(key, text=None) · clear_slot · pulse(keys) · wish(text) · pick(nodes) ·
        pods(node, n, status) · loop · watch_arrows · docker_crossed · lamp(key, colour|None) ·
        blink_lamps · cloud_arrow(colour, text=None) · to_standin. ANIM light(key, colour).
        Keys 'api' 'etcd' 'scheduler' 'controllers' 'kubelet' 'proxy' 'runtime' 'cloud' 'cloud_arrow'
        'kubectl' 'node0..2' 'plane'. .parts{key} .chips{name} .nodes .slot_y
    V2 FleetMorph() full frame x -6.4 .. 6.4, y -3.2 .. 2.7 (S01, S02). PLAYS one_vm · browser
        (.win .req) · question (.q) · clock(text) (.clock_g) · crash(key) · app_owner (.owner_g) ·
        operator(key) (.op .tunnel) · heal_box(key) · l20_chip (.l20) · three_vms (.vms .say) ·
        glow_backups · vm_down(i) · lever(i) · docker_host · to_cluster · deployment_note · fade_all.
    V3 LabelLink() strip x -6.3 .. 6.3, y -1.0 .. 0.9 (endpoints row to y -1.55). PLAYS deployment ·
        make_pods(n) · stickers · service · lasso · build (all five) · endpoints(items, note) ·
        swap_endpoint(i, new) · replace_pod(i). ANIM flash_labels(). .card .pods .tags .svc .lasso_g
        .eps. port_path() and dns_card() go with it.
    V4 ControllerLoop() x -6.3 .. 6.45, y -1.25 .. 2.75 (cards row, two worker lanes, controllers
        ring column x 3.6 .., caption row y -1.1). PLAYS deployment(src) · replicaset(src) · pod(suffix,
        lane, status, src) · pods(srcs) · loop · spin · needle · count(desired, actual) · caption(text)
        · clear_caption · kill(suffix) · respawn(suffix, lane, status) · status(suffix, word) ·
        remove_pod(suffix). Job cousin: ControllerLoop(job=True, name='vector-db-loader', api=True)
        x -4.9 .. 4.6, y -0.75 .. 0.95: PLAYS job_card · run_job · hourglass · release.
    V5 CheeseBlueprint() full frame, picture x -6.3 .. 0.3 (table x 0.75 .. 6.5), y -3.0 .. 2.45.
        PLAYS l20 · dissolve · row(i) (i = 0..7, BLUEPRINT_ROWS; each also changes the picture) ·
        drop_table · slide_center · vpc · private_nodes · nat · namespace · lb · chip(key, text).
        .parts{nginx, ingress, front, api, vdb, job, svc_*, pvc1, pvc2, wi, pool} .extras
    StackPipe() x -6.2 .. 6.35, y -1.2 .. 2.6 (S10: images · to_registry · pipe; S11: bucket ·
        break_pipe · fill_outputs · join).
    V6 ResourceTree() x -6.3 .. 6.3, y -1.25 .. 2.75 (row A y 2.15, row B y 0.75, bottom line y -0.45).
        PLAYS group(key) · grow · expand(key) · collapse · counter(n) · reads · fill_member(key, name)
        · fill(key) · fail(key, name) · clock · empty · ghosts. Keys network cluster provider identity
        storage app ingress.
    V7 RequestJourney() x -6.35 .. 6.35, y -3.15 .. 0.95 (routing card above nginx to y ~2.4).
        PLAYS build · loader_arrow · send(text, hops, keep) · dns · routing_card · reject(packet) →
        new RED '404' bubble · reply(at, text) · page_spawn · scissors_crossed(at) · drop_packet(p).
        Hops browser lb nginx front api vdb job. DoorsStrip() three panels x -6.3 .. 6.3,
        y -1.25 .. 1.25: PLAYS build(lag).
    V8 BinPacking() x -6.3 .. 6.4, y -2.65 .. 2.6 (shelves x -6.3 .. 1.0; Pending spot x 1.3 .. 3.0;
        levers / ghost node / legend x 3.4 .. 6.4). PLAYS node(i) · fill · add_block(key, node) ·
        land(block, node) · disk · multi_attach · ghost_node · levers · legend.
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import yaml
from manim import (DL, DOWN, DR, LEFT, ORIGIN, PI, RIGHT, TAU, UL, UP, UR, AnimationGroup, Arc,  # noqa: F401
                   Arrow, Circle, Create, FadeTransform, GrowFromPoint, CurvedArrow, DashedLine, DashedVMobject, DecimalNumber, Dot, FadeIn,
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
# SAY lines per scene (script.md v2, 2026-11-07); every scene asserts its own count
SAY_COUNT = {"S01": 8, "S02": 9, "S03": 9, "S04": 11, "S05": 9, "S06": 10, "S07": 10, "S08": 10,
             "S09": 7, "S10": 10, "S11": 9, "S12": 10, "S13": 11, "S14": 8, "S15": 11, "S16": 9}

# ------------------------------------------------------------------ semantic colours (BRIEF.md)
LAPTOP = S.GREY          # the laptop: Docker Desktop, the browser, the toolbox's outline, the kind stand-in
BROWSER = LAPTOP
YOU = LAPTOP
STANDIN = LAPTOP         # the kind stand-in cluster: GREY dashed outline + standin_tag()
CLOUD = S.BLUE           # GCP, GKE, control plane, nodes, node pool, VPC, NAT, LB, disks, registry, bucket
NODE = CLOUD
CONTAINER = S.TEAL       # containers, images and Pods (TEAL circles), the toolbox, dlops/tic-tac-toe
IMAGE = CONTAINER
POD = CONTAINER
SHARED = S.ORANGE        # cluster- or OS-owned: kube-system, default namespace, service/kubernetes, apt repo
SYSTEM = SHARED
AMBER = S.ORANGE
OWN = S.GREEN            # declared, project-owned: manifests, Pulumi programs/config, desired state,
NET = OWN                #   Deployment / ReplicaSet / Job / PVC cards, cheese-app-namespace, image tags
PASS = OWN
DECLARED = OWN
TOOL = S.PURPLE          # kubectl, gcloud, helm, pulumi and providers, docker, kind, gke-gcloud-auth-plugin
ERR = S.RED              # every honest first error, wrong README lines, Pending forever, Multi-Attach
TURN = S.YELLOW          # your turn, the tracker, the thing to look at now, ponder timers, the asks' ticks
COST = S.GOLD            # cluster fee, nodes, LB, NAT, disks, registry storage, "Don't forget to delete"
ROUTE = S.PINK           # Services, labels/selectors, endpoints, DNS names, ports, Ingress rules, sslip.io
SVC = ROUTE
PAST = S.GREY            # the past, the future, possible-but-not-configured (L20's VM, L23, HPA): dashed
FUTURE = PAST
INK = S.WHITE
DIMMED = S.GREY
# Pod status words (Pods stay TEAL whatever their state)
STATUS_COL = {"Running": INK, "ContainerCreating": TURN, "Pending": ERR, "Completed": S.GREY}

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
_SA_RE = re.compile(r"sa_\d{6,}")                # the leftover ssh_user key (c12:8): always masked
SA_MASK = "sa_000000000000000000000"
SA_SHORT = "sa_000…"


def unname(s: str) -> str:
    """s with the instructor's name masked ('‹instructor›'), the staff branch cropped ('work/…') and
    every 'sa_' + digits user replaced by SA_MASK. capture(), recorded(), source_text() and readme()
    apply it, so no scene ever sees the real values. (The captures already write the staff branch as
    'work/‹staff›'; Capture.line() refuses any line that names a work/ branch at all.)"""
    s = _NAME_RE.sub("‹instructor›", s)
    s = _BRANCH_RE.sub("work/…", s)
    return _SA_RE.sub(SA_MASK, s)


mask = unname


# ------------------------------------------------------------------ captures
CAPTURE_FOLDERS = ("laptop", "kind")
# captures whose command takes several file lines that are NOT joined by a trailing '\':
#   kind/k51  kubectl exec … deployment/web -- /bin/sh, then 'hostname; ls; exit' typed at the Pod's '$'
#             (type_capture(self, t, "k51", prompts=[toolbox_prompt(), "$"]))
CMD_LINES = {"kind/k51": 2}
QUOTED = ()                  # no capture types a quoted multi-row argument in this video
_ALIAS = re.compile(r"^(b31|c11)-([123])$")     # b31-2 = b31-k8s-config-set-2, c11-1 = c11-x-k8s-config-set-1

class Capture:
    """One captured command (assets/terminal/<folder>/<file>). .cmd_lines (typed rows) .cmd (joined
    with '\\n') .k (file lines of the command) .lines (output body, no [exit N]) .exit .raw (every
    file line, tabs expanded, masked) .path .key ('kind/k51', 'laptop/b03')"""

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
        if "work/" in s:
            raise ValueError(f"{self.path.name}:{n} names the staff branch: never printed (crop the list)")
        return s

    def typed(self, upto: str | None = None) -> str:
        """script.md's `typed crop "…"`: line 1 of the command up to and including `upto` (None: the
        whole first row). p02 must be cropped (its tail names the staff branch):
        type_cmd(self, t, capture("p02").typed("%s'"))."""
        s = self.cmd_lines[0]
        if upto is not None:
            s = s[:s.index(upto) + len(upto)]
        if "work/" in s:
            raise ValueError(f"{self.path.name}: the typed command names the staff branch; crop it")
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
        if any("work/" in x for x in out_):
            raise ValueError(f"{self.path.name}: a picked line names the staff branch; never printed")
        return out_


def capture(name: str) -> Capture:
    """capture("b03") / capture("c20") / capture("p05") (laptop/) · capture("k50") (a name 'k' + digits
    is kind/; or capture("kind/k50")) · capture("b31-2") / capture("c11-3") (the config-set triples)
    · capture("b02a"). The one file assets/terminal/<folder>/<name>-*.txt (or <name>.txt).
    Fails loudly when missing or ambiguous: never show an uncaptured output. The command takes file
    lines 1..k: k from CMD_LINES, else line 1 plus every row that follows a trailing '\\'.
    capture-only/ is plumbing and refused. Text is masked on load (unname)."""
    if "capture-only" in name:
        raise ValueError("capture-only/ is plumbing (CA builds, placeholder keys): never shown")
    folder, _, stem = name.rpartition("/")
    stem = stem[:-4] if stem.endswith(".txt") else stem
    folder = folder or ("kind" if re.match(r"k\d", stem) else "laptop")
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
    cmd_lines = [raw[0][2:]] + [r[2:] if r.startswith("$ ") else r for r in raw[1:k]]
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
    """Lines of assets/terminal/expected/<file> ('readme-pulumi-outputs')
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
P_LAPTOP = "student@laptop:~$"                                    # k01, k81 (kind itself), p01-p05
P_HOME = P_LAPTOP
P_REPO = "student@laptop:~/cheese-app-v3$"
P_SRC = "student@laptop:~/cheese-app-v3/src$"                     # where the README's `cd deployment` starts
P_DEPLOY = "student@laptop:~/cheese-app-v3/src/deployment$"
T_LAPTOP = "laptop"
T_TOOLBOX = "laptop · toolbox"
T_TB_STANDIN = "laptop · toolbox · stand-in"                     # kubectl beats on the kind stand-in
T_LAPTOP_STANDIN = "laptop · stand-in"                           # k01, k81


def _toolbox_prompt() -> str:
    """The toolbox prompt exactly as b03:77 printed it ('root@<id>:/app# exit' -> 'root@<id>:/app#')."""
    try:
        s = capture("b03").raw[76]
        return s[:s.index("#") + 1]
    except Exception:                                           # noqa: BLE001 (keeps imports working)
        return "root@toolbox:/app#"


P_TOOLBOX = _toolbox_prompt()                                    # root@<12 hex>:/app#  (id never read)


def toolbox_prompt(path: str = "/app") -> str:
    """P_TOOLBOX with its path swapped: toolbox_prompt('/app/deploy_images'),
    toolbox_prompt('/app/deploy_k8s')."""
    user_host = P_TOOLBOX.split(":", 1)[0]
    return f"{user_host}:{path}#"


PROJECT_PH = "your-gcp-project"            # b01, b03, b14, b52 (never a real id)
PROJECT_README = "ac215-project"           # the README's default: show it with default_tag()
IP_PH = "<IP>"                             # every public IP (expected/ writes <IP>)
EXT_IP = "<EXTERNAL-IP>"                   # S06's browser bar
HOST_PH = "<IP>.sslip.io"
APP_URL = "http://<IP>.sslip.io"
NAMESPACE = "cheese-app-namespace"
OLD_NAMESPACE = "cheese-app-cluster-namespace"   # README:618-657's stale name (k30-k43)
CLUSTER = "cheese-app-cluster"
TEST_CLUSTER = "test-cluster"
ZONE_TEST = "us-east1-c"
REGION = "us-central1"
VPC = "cheese-app-vpc"
SUBNET_RANGE = "10.0.0.0/19"
INGRESS = "cheese-app-ingress"
HELM_RELEASE = "nginx-f5"
KSA = "api-ksa"
STACK_REF = "organization/deploy-images/dev"
MACHINE = "n2d-standard-2"
C_TOOLBOX = "cheese-app-deployment"
PORTS = {"front": "3000", "api": "9000", "vdb": "8000", "lb": "80"}
SVC_NAMES = {"front": "frontend", "api": "api", "vdb": "vector-db"}      # setup_containers.py:94, :328
# the stand-in's tic-tac-toe objects (k50-k56; private addresses of a deleted cluster, never read aloud)
RS_HASH = "5cd9789488"
POD_SUFFIXES = ("5h48s", "bmkj5")          # k50:10-11
NEW_SUFFIX = "lmk52"                       # k53, k54
SCALE_SUFFIXES = ("gmbqz", "grq79")        # k55:9-10
SVC_IP = "10.96.52.79"                     # k11:4, k52:5
ENDPOINTS = ("10.244.1.2:8080", "10.244.2.2:8080")   # k50:19
NEW_POD_IP = "10.244.1.7"                  # k54:4
DNS_NAME = "web.default.svc.cluster.local"
VERSIONS = {"gcloud": "Google Cloud SDK 592.0.0", "plugin": "gke-gcloud-auth-plugin 0.5.21",
            "kubectl": "v1.35.9-dispatcher", "kubectl_kind": "v1.34.12-gke", "helm": "Helm v3.22.1",
            "pulumi": "Pulumi v3.274.1", "kind": "kind v0.31.0", "k8s_kind": "v1.34.11"}

# slide 12: the three asks (AsksChecklist), their one-liners (S01) and what did each job (S16)
ASKS = ("Failover", "Load balancing", "Scaling")
ASK_NOTES = ("a working copy takes over", "requests spread across copies", "more copies when busy")
ASK_ANSWERS = ("ReplicaSet · node auto-repair", "cloud LB · nginx Ingress · Services",
               "node autoscaler · kubectl scale")
# V1: the cluster's parts (MasterDiagram keys) and the lecture's one-line callouts (slides 25-26)
PARTS = ("api", "etcd", "scheduler", "controllers", "kubelet", "proxy", "runtime", "cloud")
CALLOUTS = {
    "api": "API server · the single entry point",
    "etcd": "etcd · the cluster's memory: state and config",
    "scheduler": "scheduler · picks a node for each Pod",
    "controllers": "controllers · keep watching, fix the difference",
    "kubelet": "kubelet · the API server's hands on this node",
    "proxy": "kube-proxy · routes Service traffic",
    "runtime": "container runtime · runs the containers",
    "cloud": "cloud provider API · nodes, load-balancer IP",
}
# V5: L20 -> L22, one row each (BRIEF V5)
BLUEPRINT_ROWS = (
    ("container", "Deployment + Pods"),
    ("loader", "Job"),
    ("Docker network names", "Services + DNS"),
    ("/mnt/disk-1 folders", "2 PVCs on cloud disks"),
    ("nginx container", "Ingress controller + Ingress"),
    ("gcp-service.json", "Workload Identity · no key"),
    ("restart policy", "ReplicaSet"),
    ("one VM", "node pool · 1–2 nodes"),
)
# V6: c20's 22 resources (+ the stack itself = 23) in seven groups, dependency order (digest Step 7)
TREE_GROUPS = (
    ("network", "network", CLOUD, ("cheese-app-vpc", "cheese-app-subnet", "cheese-app-router",
                                   "cheese-app-nat")),
    ("cluster", "cluster + pool", CLOUD, ("cheese-app-cluster", "cheese-app-pool")),
    ("provider", "provider", TOOL, ("gke_k8s_v2", "connect-k8s-command")),
    ("identity", "identity", OWN, ("cheese-app-namespace", "api-ksa", "api-gsa-wi-user")),
    ("storage", "storage", OWN, ("persistent-pvc", "chromadb-pvc")),
    ("app", "app", OWN, ("frontend", "frontend-service", "vector-db", "vector-db-service",
                         "vector-db-loader", "api", "api-service")),
    ("ingress", "ingress", OWN, ("nginx-f5", "cheese-app-ingress")),
)
assert sum(len(g[3]) for g in TREE_GROUPS) == 22          # + pulumi:pulumi:Stack = c20:45's 23
TREE_READS = ("StackReference organization/deploy-images/dev", "nginx-ingress-service")
# V8: requests (setup_containers.py:79-82, :154-155; setup_loadbalancer.py:26-30; the API has none)
REQUESTS = {"frontend": "250m / 2Gi", "vector-db": "100m / 128Mi", "nginx": "100m / 128Mi", "api": "none"}

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
    "W": "Create Simple Kubernetes Cluster Tutorial",          # README:517-581 (done first, as the lecture)
    "D": "Deployment with Scaling using Kubernetes",           # README:392-434
    "C": "Create & Deploy Cluster",                            # README:436-512
    "G": "Debugging Containers",                               # README:618-657, its Kubernetes half
}
STEPS = {
    "W": ["Enable APIs", "Run toolbox", "Check tools", "Auth check", "Create cluster", "See console",
          "Try kubectl", "Deploy app", "Get IP", "View app", "Delete cluster"],
    "D": ["Enable APIs", "Run toolbox", "Check tools", "Auth check", "Images stack", "Images preview",
          "Images up"],
    "C": ["Cluster stack", "Config keys", "Preview", "Pulumi up", "Try kubectl", "Shell into Pod",
          "View app", "Delete cluster"],
    "G": ["Job logs", "Find pod", "Pod logs", "API logs"],
}
assert [len(STEPS[k]) for k in "WDCG"] == [11, 7, 8, 4]
TRACKER_KEYS = tuple(SECTIONS)
EXTRA_KINDS = ("our spelling", "not for you", "recording only", "stand-in")


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
        return steady(_suffix(extra).lstrip(" ·"), tr.size, S.GREY).next_to(tr.dots, RIGHT, buff=0.25)
    s = f"step {k} of {len(tr.steps)}: {tr.steps[k - 1]}"
    suf = _suffix(extra)
    t = steady(s + suf, tr.size, tr.hi_color, t2c={suf.strip(" ·"): S.GREY} if suf else None)
    return t.next_to(tr.dots, RIGHT, buff=0.25)


def tracker(key: str, step: int | None = None, extra=False) -> ReadmeTracker:
    """Tracker `key` ('W' warm-up, 'D' deployment, 'C' cluster, 'G' debugging) at `step` (1-based;
    None = no step lit yet), placed top-left: 'README › <section>', one dot per step, 'step k of N:
    <step>' + the GREY extra suffix (extra=True ' · extra'; 'our spelling' / 'not for you' /
    'recording only' / 'stand-in' → ' · extra · …'; any other str is appended after ' · ')."""
    tr = ReadmeTracker(SECTIONS[key], STEPS[key])
    tr.key = key
    if step:
        tr.set_step(step)
    tr.remove(tr.caption)
    tr.caption = _caption(tr, step or 0, extra)
    tr.extra = extra
    tr.add(tr.caption)
    return place_tracker(tr)


def tracker_w(step: int | None = None, extra=False) -> ReadmeTracker:
    """README › Create Simple Kubernetes Cluster Tutorial, 11 steps (S04-S08)."""
    return tracker("W", step, extra)


def tracker_d(step: int | None = None, extra=False) -> ReadmeTracker:
    """README › Deployment with Scaling using Kubernetes, 7 steps (S10)."""
    return tracker("D", step, extra)


def tracker_c(step: int | None = None, extra=False) -> ReadmeTracker:
    """README › Create & Deploy Cluster, 8 steps (S11-S14, S16)."""
    return tracker("C", step, extra)


def tracker_g(step: int | None = None, extra=False) -> ReadmeTracker:
    """README › Debugging Containers (Kubernetes half), 4 steps (S15)."""
    return tracker("G", step, extra)


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
    """The GREY 'Lecture 22 · slides 22–26' tag, top right (one slide: 'slide 7'), only while that
    slide's picture or idea is on screen: lref("7"), lref("22–26"), lref("7, 18, 30, 36, 39")."""
    return lecture_ref(22, slides)


LREF_BOTTOM = 3.6 - tag("x").height      # the lecture tag's lowest point (AsksChecklist sits below it)

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


def laptop_term(rows: int = 10, prompt: str = P_LAPTOP, standin: bool = False) -> Terminal:
    """Title 'laptop' (p01-p05, b01-b03 before the toolbox prompt); standin=True: title
    'laptop · stand-in' (k01, k81: kind itself)."""
    return term(prompt, rows, T_LAPTOP_STANDIN if standin else T_LAPTOP)


def toolbox_term(rows: int = 10, path: str = "/app", standin: bool = False) -> Terminal:
    """Title 'laptop · toolbox', prompt from b03:77 with `path` (b10-b52, c00-c23); standin=True: title
    'laptop · toolbox · stand-in' (the kubectl beats on kind: k02-k80)."""
    return term(toolbox_prompt(path), rows, T_TB_STANDIN if standin else T_TOOLBOX)


def standin_term(rows: int = 10, path: str = "/app") -> Terminal:
    """toolbox_term(rows, path, standin=True): pin standin_tag() on its bar (on_bar)."""
    return toolbox_term(rows, path, standin=True)

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
    is a separate command at the prompt (k51's two: prompts=[toolbox_prompt(), '$']). QUOTED captures type rows 2.. as
    continuation rows of one quoted argument, soft-wrapped, never folded with ' \\'. prompts: a list
    with the prompt to set before each command row (None keeps the terminal's). type_time: per row.
    Returns the list of typed lines (each a line or a folded VGroup)."""
    cap = capture(cap) if isinstance(cap, str) else cap
    if any("work/" in r for r in cap.cmd_lines):
        raise ValueError(f"{cap.path.name}: its command names the staff branch; type cap.typed(upto) instead")
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
    """The GREY chip under a command typed with no output panel (S11's cd /app/deploy_k8s typed with no output)."""
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
    as one (S09: '≈ $5–8 per day · our estimate … roughly')."""
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
    """'expected · README:497–506': the README's Outputs block (S14, the only expected panel)."""
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
    unless it says '≈' and 'roughly' (S09's one price line)."""
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
    mono 20 pt rows; long rows break at the edge): S14's Outputs block,
    quote_card("readme-pulumi-outputs", (2, 9), source="README:497–506", mono_font=True, width_chars=60).
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

    def swap(self, scene, old, new, run_time: float = 0.6, extra=(), into=None, morph: bool = False):
        """PLAYS: `old` (a part) cross-fades into `new` in place (not yet shown; nothing is stretched, so
        texts never shrink below their size mid-way; morph=True: a point-by-point ReplacementTransform,
        for shapes of the same kind); afterwards `new` is the part."""
        parent = into
        if parent is None:
            for sub in self.get_family():
                if old in sub.submobjects:
                    parent = sub
                    break
        self._detach(old)
        scene.add(old)
        if morph:
            scene.play(ReplacementTransform(old, new), *extra, run_time=run_time)
        else:
            scene.play(FadeOut(old), FadeIn(new), *extra, run_time=run_time)
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
    """GREY tag beside the README's `ac215-project` (b21, b31-1..3, c02, c11-1..3, c12, c03, c21)."""
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



# ------------------------------------------------------------------ L22 tags, glyphs and small pieces
def standin_tag(s: str = "stand-in: kind, not GKE") -> VGroup:
    """GREY tag on every kind/ panel (top right of the terminal: on_bar(t, standin_row()) or
    under_term(t, standin_tag())) and on the V1 cluster drawn on the laptop."""
    return tag(s, S.GREY)


def standin_row() -> VGroup:
    """standin_tag sized for a terminal row / title bar: on_bar(t, standin_row())."""
    return row_tag("stand-in: kind, not GKE", S.GREY)


def placeholder_tag(s: str = "placeholder image tags · nothing built") -> VGroup:
    """GREY tag on c20 / c21 (the capture-only stand-in image stack)."""
    return tag(s, S.GREY)


def scene_chip(s: str) -> VGroup:
    """A small GREY chip naming where an idea returns ('Ingress → S13', 'S07')."""
    return grey_chip(s)


def dont_forget_card(sub: str | None = None, size: float = 32) -> VGroup:
    """The GOLD 'Don't forget to delete' card (slide 44's message, no meme); sub: a GREY line under it.
    .frame .title .sub"""
    t = label("Don't forget to delete", size, COST)
    rows = [t]
    st = None
    if sub:
        st = label(sub, 22, S.GREY)
        rows.append(st)
    inner = VGroup(*rows).arrange(DOWN, buff=0.2)
    fr = RoundedRectangle(width=inner.width + 0.9, height=inner.height + 0.7, corner_radius=0.16,
                          stroke_color=COST, stroke_width=4).set_fill(tint(COST, 0.12), 1)
    inner.move_to(fr)
    g = VGroup(fr, inner)
    g.frame, g.title, g.sub = fr, t, st
    return g


def frame_box(box_w: float, box_h: float, color, k: float = 0.16, dashed: bool = False, stroke: float = 3,
              radius: float = 0.12) -> VGroup:
    """An OPAQUE rounded box (tinted fill) with a solid or dashed outline. .fill .edge"""
    fill = RoundedRectangle(width=box_w, height=box_h, corner_radius=min(radius, box_h / 2, box_w / 2),
                            stroke_width=0).set_fill(tint(color, k), 1)
    edge = RoundedRectangle(width=box_w, height=box_h, corner_radius=min(radius, box_h / 2, box_w / 2),
                            stroke_color=color, stroke_width=stroke).set_fill(opacity=0)
    if dashed:
        edge = DashedVMobject(edge, num_dashes=max(12, int((box_w + box_h) * 7)), dashed_ratio=0.55)
        edge.set_stroke(color, stroke)
    g = VGroup(fill, edge)
    g.fill, g.edge = fill, edge
    return g


def boxed(rows, color, box_w: float | None = None, box_h: float | None = None, size: float = 20,
          mono_font: bool = False, dashed: bool = False, text_color=INK, k: float = 0.16,
          buff: float = 0.06, pad: float = 0.2) -> VGroup:
    """A labelled box: rows of text (str with '\\n', or a list) centred in an opaque box in `color`
    (fits the text when box_w/box_h are None; raises when given and too small). .frame .text
    .rows (each row a Text)"""
    rows = rows.split("\n") if isinstance(rows, str) else list(rows)
    txt = VGroup(*[(mono if mono_font else label)(r, size, text_color) for r in rows]).arrange(DOWN, buff=buff)
    w = box_w or txt.width + 2 * pad
    h = box_h or txt.height + 2 * pad * 0.8
    if txt.width > w - 0.12 or txt.height > h - 0.06:
        raise ValueError(f"boxed: {rows} ({txt.width:.2f} x {txt.height:.2f}) does not fit {w:.2f} x {h:.2f}")
    fr = frame_box(w, h, color, k=k, dashed=dashed)
    txt.move_to(fr)
    g = VGroup(fr, txt)
    g.frame, g.text, g.rows = fr, txt, list(txt)
    return g


def two_row_chip(top: str, bottom: str, color=TOOL, size: float = 20) -> VGroup:
    """A chip whose name breaks over two rows ('gke-gcloud-' / 'auth-plugin'). .box .text"""
    t = VGroup(label(top, size, INK), label(bottom, size, INK)).arrange(DOWN, buff=0.04)
    b = box(t.width + 0.36, t.height + 0.2, color, fill_opacity=0.16, radius=0.16)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def pod_name(name: str, size: float = 20, hash_ring: bool = True) -> VGroup:
    """A Pod name drawn in its three parts (BRIEF V4): GREEN Deployment name, the ReplicaSet's
    pod-template-hash GREEN with a thin GREEN outline, TEAL suffix: pod_name('web-5cd9789488-5h48s').
    A name without two dashes is plain TEAL. .text .hash (glyphs of the hash, or None) .ring"""
    parts = name.split("-")
    g = VGroup()
    if len(parts) >= 3 and len(parts[-2]) >= 8:
        dep = "-".join(parts[:-2])
        hsh = parts[-2]
        t = mono(name, size, POD)
        n0, n1 = len(dep) + 1, len(dep) + 1 + len(hsh)
        t[:n0].set_color(OWN)
        t[n0:n1].set_color(OWN)
        t[n1:n1 + 1].set_color(OWN)
        g.add(t)
        g.text, g.hash = t, t[n0:n1]
        g.ring = None
        if hash_ring:
            rg = RoundedRectangle(width=g.hash.width + 0.1, height=mono("|", size).height + 0.04,
                                  corner_radius=0.05, stroke_color=OWN, stroke_width=1.5).move_to(g.hash)
            g.add(rg)
            g.ring = rg
    else:
        t = mono(name, size, POD)
        g.add(t)
        g.text, g.hash, g.ring = t, None, None
    return g


def pod_status(status: str, size: float = 20) -> Text:
    """A Pod's status word, coloured by STATUS_COL (Running WHITE, ContainerCreating YELLOW, Pending
    RED, Completed GREY; anything else GREY)."""
    return steady(status, size, STATUS_COL.get(status, S.GREY))


def pod_glyph(name: str | None = None, status: str | None = None, r: float = 0.26, dots: int = 2,
              side=DOWN, size: float = 20, dashed: bool = False) -> VGroup:
    """A Pod: a TEAL circle with container dots inside (Pods are always TEAL); optional name
    (pod_name(), at `side` of the circle) and status word (under the name, or under the circle).
    .circle .dots .name .status"""
    c = Circle(radius=r, stroke_color=POD, stroke_width=3).set_fill(tint(POD, 0.3), 1)
    if dashed:
        c = VGroup(c.set_stroke(opacity=0), DashedVMobject(c.copy().set_fill(opacity=0).set_stroke(opacity=1),
                                                           num_dashes=12).set_stroke(POD, 3))
    d = VGroup(*[Square(side_length=r * 0.42, stroke_width=0).set_fill(POD, 0.95) for _ in range(dots)])
    d.arrange(RIGHT, buff=r * 0.18).move_to(c)
    g = VGroup(c, d)
    g.circle, g.dots, g.name, g.status = c, d, None, None
    anchor = c
    if name:
        nm = pod_name(name, size)
        nm.next_to(c, side, buff=0.12)
        g.add(nm)
        g.name = nm
        anchor = nm
    if status:
        st = pod_status(status, size)
        st.next_to(anchor, DOWN, buff=0.08)
        if name and side is RIGHT:
            st.align_to(anchor, LEFT)
        g.add(st)
        g.status = st
    return g


def node_box(title: str | None = "worker node (VM)", box_w: float = 4.0, box_h: float = 1.0, color=NODE,
             dashed: bool = False, size: float = 20) -> VGroup:
    """A worker node: opaque BLUE box with its title at the top-left (20 pt). .frame .title"""
    fr = frame_box(box_w, box_h, color, k=0.1, dashed=dashed)
    g = VGroup(fr)
    g.frame, g.title = fr, None
    if title:
        t = label(title, size, color if color != NODE else INK)
        t.move_to(fr).align_to(fr, UL).shift(np.array([0.14, -0.08, 0]))
        g.add(t)
        g.title = t
    return g


def dns_card(name: str = DNS_NAME, ip: str = SVC_IP, size: float = 20) -> VGroup:
    """S08's PINK DNS card: 'web.default.svc.cluster.local → 10.96.52.79' (k52:4-5). .name .ip .frame"""
    n = mono(name, size, INK)
    a = label("→", size, ROUTE)
    i = mono(ip, size, ROUTE)
    row = VGroup(n, a, i).arrange(RIGHT, buff=0.14)
    fr = frame_box(row.width + 0.45, row.height + 0.36, ROUTE, k=0.14)
    row.move_to(fr)
    g = VGroup(fr, row)
    g.frame, g.name, g.ip = fr, n, i
    return g


def console_view(path, rows=(), card_w: float | None = None, size: float = 20, kind: str = "illustration",
                 row_color=CLOUD) -> VGroup:
    """A schematic console page (GREY, no logo, tag `kind` on its top edge): a breadcrumb `path`
    (list of crumbs, shown 'a › b › c') and rows (str, drawn as BLUE outlined lines; or (text, colour)).
    Light one crumb at a time with Indicate(cv.crumbs[i]). .frame .crumbs .rows .tag"""
    crumbs = [label(c, size, INK) for c in path]
    seps = [label("›", size, S.GREY) for _ in path[1:]]
    items = []
    for i, c in enumerate(crumbs):
        items.append(c)
        if i < len(seps):
            items.append(seps[i])
    crumb_row = VGroup(*items).arrange(RIGHT, buff=0.12)
    rws = VGroup()
    for r in rows:
        txt, col = (r, row_color) if isinstance(r, str) else r
        t = label(txt, size, INK)
        b = RoundedRectangle(width=max(t.width + 0.5, 3.0), height=t.height + 0.26, corner_radius=0.06,
                             stroke_color=col, stroke_width=2).set_fill(tint(col, 0.12), 1)
        t.move_to(b).align_to(b, LEFT).shift(RIGHT * 0.2)
        rr = VGroup(b, t)
        rr.box, rr.text = b, t
        rws.add(rr)
    if len(rws):
        rws.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    inner = VGroup(crumb_row, *([rws] if len(rws) else [])).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    w = card_w or inner.width + 0.8
    if inner.width > w - 0.4:
        raise ValueError(f"console_view: {inner.width:.2f} wide does not fit card_w={w}")
    fr = box(w, inner.height + 0.85, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
    inner.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.35 + DOWN * 0.08)
    tg = tag(kind, S.GREY)
    tg.move_to(fr.get_corner(UR) + np.array([-tg.width / 2 - 0.2, 0, 0]))
    g = VGroup(fr, inner, tg)
    g.frame, g.crumbs, g.rows, g.tag = fr, crumbs, rws, tg
    return g


def ttt_grid(cell: float = 0.42, color=S.GREY) -> VGroup:
    """The tic-tac-toe page: a 3 x 3 grid of empty squares (text-free)."""
    return VGroup(*[Square(side_length=cell, stroke_color=color, stroke_width=2.5) for _ in range(9)]).arrange_in_grid(
        3, 3, buff=0.08)


def browser_window(url: str, rows=None, win_w: float = 5.6, win_h: float = 3.4, mono_font: bool = False,
                   with_tag: bool = True) -> Browser:
    """A schematic browser (the house Browser piece, no logo) at `url` ('http://<EXTERNAL-IP>',
    APP_URL), its page pre-filled with `rows` (str or mobjects, not animated) and the GREY
    'illustration' tag just above its top-right corner (.tag). FadeIn it like any mobject; PLAYS goto/fill/reload
    as Browser."""
    b = Browser(url, win_w, win_h)
    if rows:
        g = b._rows(rows, mono_font, INK, 0.14)
        b.rows.add(*g.submobjects)
    b.tag = None
    if with_tag:
        tg = illustration_tag()
        tg.next_to(b.frame, UP, buff=0.06).align_to(b.frame, RIGHT)
        b.add(tg)
        b.tag = tg
    return b


def hourglass(h: float = 0.5, color=TURN) -> VGroup:
    """A text-free YELLOW hourglass (Pulumi waits for the Job)."""
    w = h * 0.62
    top = Polygon([-w / 2, h / 2, 0], [w / 2, h / 2, 0], [0, 0, 0], stroke_color=color, stroke_width=3)
    bot = Polygon([-w / 2, -h / 2, 0], [w / 2, -h / 2, 0], [0, 0, 0], stroke_color=color, stroke_width=3)
    sand = Polygon([-w * 0.3, -h / 2, 0], [w * 0.3, -h / 2, 0], [0, -h * 0.18, 0], stroke_width=0).set_fill(color, 0.8)
    caps = VGroup(Line([-w * 0.6, h / 2, 0], [w * 0.6, h / 2, 0]), Line([-w * 0.6, -h / 2, 0], [w * 0.6, -h / 2, 0]))
    caps.set_stroke(color, 4)
    return VGroup(top, bot, sand, caps)


def clock_face(r: float = 0.32, color=S.GREY, hour: float = 2.0) -> VGroup:
    """A text-free clock face showing `hour` (hand angles only). .hands"""
    c = Circle(radius=r, stroke_color=color, stroke_width=3).set_fill(S.BG, 1)
    hh = Line(ORIGIN, UP * r * 0.5, color=color, stroke_width=4).rotate(-hour / 12 * TAU, about_point=ORIGIN)
    mh = Line(ORIGIN, UP * r * 0.8, color=color, stroke_width=3)
    g = VGroup(c, hh, mh)
    g.hands = VGroup(hh, mh)
    return g


def lever_glyph(h: float = 0.8, color=S.GREY, on: bool = False) -> VGroup:
    """A text-free lever (S01's 'switch: by hand', S15's two levers): base + handle; on=True tilts
    it right. .handle"""
    base = RoundedRectangle(width=h * 0.7, height=h * 0.18, corner_radius=0.04, stroke_color=color,
                            stroke_width=3).set_fill(tint(color, 0.2), 1)
    handle = Line(ORIGIN, UP * h * 0.75, color=color, stroke_width=5)
    knob = Dot(UP * h * 0.75, radius=h * 0.08, color=color)
    hand = VGroup(handle, knob).rotate((-1 if on else 1) * 0.45, about_point=ORIGIN)
    hand.shift(base.get_top())
    g = VGroup(base, hand)
    g.handle = hand
    return g


def phone_glyph(h: float = 0.55, color=S.GREY) -> VGroup:
    """A text-free phone (the app owner's)."""
    b = RoundedRectangle(width=h * 0.55, height=h, corner_radius=h * 0.1, stroke_color=color,
                         stroke_width=3).set_fill(tint(color, 0.15), 1)
    s = RoundedRectangle(width=h * 0.42, height=h * 0.66, corner_radius=0.03, stroke_width=0).set_fill(color, 0.35)
    s.move_to(b).shift(UP * h * 0.04)
    return VGroup(b, s)


def ring_arrows(radius: float = 0.9, color=TURN, stroke: float = 4) -> VGroup:
    """Three arcs with tips in a circle (observe → compare → act), centred at ORIGIN."""
    g = VGroup()
    for k in range(3):
        a = Arc(radius=radius, start_angle=PI / 2 - k * TAU / 3 - 0.18, angle=-(TAU / 3 - 0.5), color=color,
                stroke_width=stroke)
        a.add_tip(tip_length=0.16, tip_width=0.16)
        g.add(a)
    return g


def l20_vm(box_w: float = 6.2, box_h: float = 4.6, title: str = "L20 · one VM") -> VGroup:
    """L20's VM as a memory (GREY dashed): nginx on top, api-service, frontend, vector-db in a row,
    the dashed one-shot loader under them. Centred at ORIGIN. .frame .title .boxes{nginx, api, front,
    vdb, loader}"""
    fr = frame_box(box_w, box_h, PAST, k=0.05, dashed=True)
    t = label(title, 20, PAST).move_to(fr).align_to(fr, UL).shift(np.array([0.18, -0.12, 0]))
    bw = min(1.85, (box_w - 0.8) / 3)
    nginx = boxed("nginx", CONTAINER, box_w=bw, box_h=0.6, mono_font=True)
    api = boxed("api-service", CONTAINER, box_w=bw, box_h=0.6, mono_font=False)
    front = boxed("frontend", CONTAINER, box_w=bw, box_h=0.6)
    vdb = boxed("vector-db", CONTAINER, box_w=bw, box_h=0.6)
    loader = boxed("loader", CONTAINER, box_w=bw, box_h=0.6, dashed=True)
    nginx.move_to(fr.get_center() + UP * box_h * 0.2)
    row = VGroup(front, api, vdb).arrange(RIGHT, buff=0.22).move_to(fr.get_center() + DOWN * box_h * 0.06)
    loader.move_to([vdb.get_center()[0], fr.get_center()[1] - box_h * 0.32, 0])
    g = VGroup(fr, t, nginx, row, loader)
    g.frame, g.title = fr, t
    g.boxes = {"nginx": nginx, "api": api, "front": front, "vdb": vdb, "loader": loader}
    return g


# ------------------------------------------------------------------ AsksChecklist (slides 12, 15)
class AsksChecklist(Piece):
    """Slide 12's three asks, Failover · Load balancing · Scaling, as a card with tick boxes.

        ac = AsksChecklist()                       # full card, ~5.6 x 3.3, centred at ORIGIN (S01, S16)
        ac = AsksChecklist(small=True, ticked=(0,)) # corner card, ~2.6 x 1.55, top right under the
                                                   # lecture tag (x .. 6.55, top LREF_BOTTOM - 0.08)
    Full: title 'What we want automated' (24 pt), item rows 26 pt, a GREY one-liner (20 pt) under each
    (ASK_NOTES, or the note given to tick()/note()). Small: the three items at 20 pt, no notes.
    PLAYS light(scene, i) the row flashes YELLOW · tick(scene, i, dashed=False, note=None) a YELLOW
    tick (dashed=True: a GREY-dashed half tick, S15's Pod level; a second tick() on the same row with
    dashed=False adds the solid one) and, on the full card, note replaces row i's one-liner ·
    note(scene, i, text, color=S.GREY) · answer(scene, i) S16's ASK_ANSWERS[i] in GREEN ·
    shrink(scene) full → small, into the corner · grow(scene, center=(0, 0)) small → full at center.
    Ticks and notes survive shrink/grow. .card (the current card group) .small .ticks{i: kind}"""

    def __init__(self, small: bool = False, ticked=(), notes: dict | None = None, center=None, **kw):
        super().__init__(**kw)
        self.small = small
        self.ticks = {i: "solid" for i in ticked}
        self.notes = {i: (ASK_NOTES[i], S.GREY) for i in range(3)}
        for i, v in (notes or {}).items():
            self.notes[i] = v if isinstance(v, tuple) else (v, S.GREY)
        self.card = self._build(small, center)
        self.add(self.card)

    @staticmethod
    def corner(card):
        top = LREF_BOTTOM - 0.08
        return card.move_to([6.55 - card.width / 2, top - card.height / 2, 0])

    def _tickmark(self, kind: str, h: float):
        if kind == "dashed":
            m = check_glyph(h, S.GREY)
            return DashedVMobject(m, num_dashes=6).set_stroke(S.GREY, 4)
        return check_glyph(h, TURN)

    def _build(self, small: bool, center=None) -> VGroup:
        size = 20 if small else 26
        bh = 0.26 if small else 0.34
        rows = VGroup()
        for i, name in enumerate(ASKS):
            bx = Square(side_length=bh, stroke_color=S.GREY, stroke_width=2.5)
            t = label(name, size, INK)
            r = VGroup(bx, t).arrange(RIGHT, buff=0.18)
            marks = VGroup()
            kinds = self.ticks.get(i)
            for kd in ([] if kinds is None else (["dashed", "solid"] if kinds == "both" else [kinds])):
                mk = self._tickmark(kd, bh).move_to(bx).shift(UP * 0.04 + RIGHT * 0.03)
                if kd == "dashed" and kinds == "both":
                    mk.next_to(bx, LEFT, buff=0.06)
                marks.add(mk)
            r.add(marks)
            r.box, r.text, r.marks, r.note = bx, t, marks, None
            if not small:
                txt, col = self.notes[i]
                nt = label(txt, 20, col)
                nt.next_to(t, DOWN, buff=0.08).align_to(t, LEFT)
                r.add(nt)
                r.note = nt
            rows.add(r)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16 if small else 0.26)
        parts = [rows]
        hd = None
        if not small:
            hd = label("What we want automated", 24, S.GREY)
            parts = [hd, rows]
        inner = VGroup(*parts).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        w = inner.width + (0.5 if small else 0.8)
        fr = RoundedRectangle(width=w, height=inner.height + (0.4 if small else 0.7), corner_radius=0.14,
                              stroke_color=TURN if not small else S.GREY, stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
        inner.move_to(fr)
        card = VGroup(fr, inner)
        card.frame, card.rows, card.head = fr, rows, hd
        if small:
            self.corner(card)
        else:
            c = (0, 0) if center is None else center
            card.move_to([c[0], c[1], 0])
        return card

    def light(self, scene, i: int, run_time: float = 0.6):
        """PLAYS: row i's name flashes YELLOW."""
        self._ensure(scene)
        scene.play(Indicate(self.card.rows[i].text, color=TURN, scale_factor=1.08), run_time=run_time)
        self.heal(scene)

    def tick(self, scene, i: int, dashed: bool = False, note: str | None = None, run_time: float = 0.5):
        """PLAYS: a tick on row i (YELLOW; dashed=True a GREY-dashed half tick); note: the row's new
        one-liner (full card only)."""
        old = self.ticks.get(i)
        kind = "dashed" if dashed else "solid"
        self.ticks[i] = "both" if old and old != kind else kind
        if note is not None:
            self.notes[i] = (note, S.GREY)
        r = self.card.rows[i]
        bh = r.box.width
        mk = self._tickmark(kind, bh).move_to(r.box).shift(UP * 0.04 + RIGHT * 0.03)
        if self.ticks[i] == "both" and kind == "dashed":
            mk.next_to(r.box, LEFT, buff=0.06)
        anims = [Create(mk), Indicate(r.text, color=TURN, scale_factor=1.06)]
        self.show(scene, mk, anims=anims, run_time=run_time, into=r.marks)
        if note is not None and r.note is not None:
            self._swap_note(scene, i, note, S.GREY)
        return mk

    def _swap_note(self, scene, i, text, color):
        r = self.card.rows[i]
        nt = label(text, 20, color).move_to(r.note, aligned_edge=LEFT)
        r.note = self.swap(scene, r.note, nt, run_time=0.4, into=r)

    def note(self, scene, i: int, text: str, color=S.GREY):
        """PLAYS: row i's one-liner becomes `text` (full card only)."""
        self.notes[i] = (text, color)
        if self.card.rows[i].note is not None:
            self._swap_note(scene, i, text, color)

    def answer(self, scene, i: int):
        """PLAYS: row i's one-liner becomes what did that job in the cheese app (GREEN, S16)."""
        self.note(scene, i, ASK_ANSWERS[i], OWN)

    def _morph(self, scene, small: bool, center=None, run_time: float = 0.7):
        new = self._build(small, center)
        self._ensure(scene)
        old = self.card
        self.remove(old)
        scene.add(old)
        shift = new.get_center() - old.get_center()
        scene.play(FadeOut(old, shift=shift * 0.5), FadeIn(new, shift=shift * 0.5), run_time=run_time)
        scene.remove(old, new)
        self.card, self.small = new, small
        self.add(new)
        self.heal(scene)

    def shrink(self, scene, run_time: float = 0.7):
        """PLAYS: the full card becomes the small corner card."""
        self._morph(scene, True, run_time=run_time)

    def grow(self, scene, center=(0, 0), run_time: float = 0.7):
        """PLAYS: the corner card becomes the full card at `center` (ticks and notes kept)."""
        self._morph(scene, False, center, run_time=run_time)


# ------------------------------------------------------------------ KubectlGrammar (slide 27)
class KubectlGrammar(Piece):
    """Slide 27's grammar: 'kubectl' then four PURPLE slots command · TYPE · NAME · flags, with an
    example line typed above them. ~12.4 x 2.1, centred at ORIGIN (example row y +0.65, slot labels
    y -0.85, slots y -0.15).
        kg = KubectlGrammar(); self.play(FadeIn(kg))
        kg.fill(self, "get", "pods", None, "--all-namespaces")   # PLAYS: example + slot values
        kg.name_note(self)                                      # PLAYS: 'optional · one object' chip
        kg.flag(self, "-n cheese-app-namespace", ROUTE)          # PLAYS: drops into the flags slot
    An empty slot shows a GREY '—'. .slots[k] (frames, k 0..3) .values[k] .example .heads"""

    WIDTHS = (1.6, 2.0, 2.6, 4.2)
    HEADS = ("command", "TYPE", "NAME", "flags")

    def __init__(self, size: float = 22, **kw):
        super().__init__(**kw)
        self.size = size
        k = chip("kubectl", TOOL, size=size, font=MONO)
        slots, heads, vals = VGroup(), VGroup(), []
        for w, h in zip(self.WIDTHS, self.HEADS):
            fr = frame_box(w, 0.62, TOOL, k=0.1)
            slots.add(fr)
            heads.add(label(h, 20, TOOL))
        row = VGroup(k, *slots).arrange(RIGHT, buff=0.12)
        row.move_to([0, -0.15, 0])
        for hd, fr in zip(heads, slots):
            hd.next_to(fr, DOWN, buff=0.12)
        for fr in slots:
            v = label("—", size, S.GREY).move_to(fr)
            vals.append(v)
        self.kubectl, self.slots, self.heads, self.values = k, slots, heads, vals
        self.example = steady("", size, INK, mono_font=True).move_to([0, 0.65, 0])
        self.add(row, heads, *vals, self.example)
        self.note_chip = None
        self.current = [None, None, None, None]

    def _val(self, k: int, s: str | None, color=INK):
        fr = self.slots[k]
        if not s:
            return label("—", self.size, S.GREY).move_to(fr)
        t = mono(s, self.size, color)
        if t.width > fr.width - 0.16:
            t = mono(s, 20, color)
        if t.width > fr.width - 0.12:
            raise ValueError(f"KubectlGrammar: {s!r} does not fit slot {self.HEADS[k]}")
        return t.move_to(fr)

    def fill(self, scene, command: str, type_: str | None = None, name: str | None = None,
             flags: str | None = None, run_time: float = 0.8):
        """PLAYS: the example line 'kubectl …' writes above, and each part drops into its slot."""
        parts = [command, type_, name, flags]
        self.current = parts
        ex = self._example(parts)
        self._ensure(scene)
        new_vals = [self._val(k, p, TURN if k == 0 else INK) for k, p in enumerate(parts)]
        anims = [Transform(self.example, ex)]
        for k in range(4):
            anims += [FadeOut(self.values[k]), FadeIn(new_vals[k], shift=DOWN * 0.15)]
        scene.play(*anims, run_time=run_time)
        self.remove(*self.values)
        scene.remove(*self.values)
        self.values = new_vals
        self.add(*new_vals)
        self.heal(scene)

    def _example(self, parts):
        line = "kubectl " + " ".join(p for p in parts if p)
        ex = steady(line, self.size, INK, mono_font=True).move_to(self.example)
        if ex.width > 12.6:
            raise ValueError(f"KubectlGrammar: example {line!r} too wide")
        return ex

    def flag(self, scene, s: str, color=ROUTE, run_time: float = 0.8):
        """PLAYS: `s` drops from above into the flags slot (replacing what was there); the example
        line above follows."""
        new = self._val(3, s, color)
        self.current = self.current[:3] + [s]
        ex = self._example(self.current)
        self._ensure(scene)
        old = self.values[3]
        scene.play(FadeOut(old), FadeIn(new, shift=DOWN * 0.6), Transform(self.example, ex), run_time=run_time)
        self.remove(old)
        scene.remove(old)
        self.values[3] = new
        self.add(new)
        self.heal(scene)

    def name_note(self, scene, text: str = "optional · one object"):
        """PLAYS: a GREY chip under the NAME slot's label."""
        c = grey_chip(text).next_to(self.heads[2], DOWN, buff=0.1)
        self.note_chip = c
        return self.show(scene, c)


# ------------------------------------------------------------------ V1 · MasterDiagram
class MasterDiagram(_Anchored):
    """V1 · the lecture's cluster (slides 22-26), redrawn for GKE. One layout, 12.9 x 4.0: x -6.45 .. 6.45,
    y -1.25 .. 2.75 where it is built (fits above a 3-row terminal strip, under the tracker). Move it
    (shift) BEFORE the first PLAYS call or between calls; S03 (no strip) shifts it down ~0.7 and uses
    the callout slot under it (self.slot_y = bottom - 0.42).
      left column x -6.45 .. -3.55: 'cloud provider API' (BLUE box, y 1.95 .. 2.75; shown by
        part('cloud')) over 'your laptop' (GREY, y -1.25 .. 1.75) holding the TEAL toolbox with PURPLE
        chips gcloud docker / pulumi helm / kubectl (largest) / gke-gcloud-auth-plugin (two rows);
      cluster box x -3.35 .. 6.45 (BLUE dashed; GREY dashed with standin=True), title top right;
        control plane panel x -3.2 .. 0.3 (scheduler, controllers above, API server centre, etcd
        below); worker nodes x 0.6 .. 6.3: node 0 tall (kubelet, kube-proxy, runtime strip with Pod
        slots), nodes 1, 2 short (kubelet chip + Pod slots). standin=True: two workers, no 'run by Google'.
    MasterDiagram(built=('laptop', 'cluster', 'plane', 'parts', 'beat23')) starts with those already
    drawn (no animation): S05-S15 reuse it that way.
    Keys for light/lamp/callout/part: 'api' 'etcd' 'scheduler' 'controllers' 'kubelet' (node 0) 'proxy'
    'runtime' 'cloud' (box), 'cloud_arrow', 'kubectl' (the chip), 'node0' 'node1' 'node2', 'plane'.

    PLAYS (build)  laptop_box(scene, chips=('gcloud','docker','pulumi')) · add_chips(scene, names)
        (kubectl flashes YELLOW) · cluster(scene, source=None) the dashed outline (source: a mobject
        that fades out as the outline draws, e.g. l20_vm() at the cluster box) · beat22(scene) laptop + cluster + plane +
        workers + fan arrows (whatever is missing) · beat23(scene) 'run by Google' caption + notes in
        the slot ('slides: master nodes' dashed; the node pool line) · part(scene, key) one inner part
        (api, etcd, scheduler, controllers, cloud, kubelet, proxy, runtime) · beat24(scene) all parts.
    PLAYS (story)  callout(scene, key) the part flashes YELLOW and its CALLOUTS line writes in the slot
        (replacing the last) · clear_slot(scene) · pulse(scene, keys, color=TURN) a dot travels
        part to part · wish(scene, text='desired state') a GREEN card rides kubectl → API → etcd ·
        pick(scene, nodes=(0, 1)) scheduler lights, those nodes flash · pods(scene, node, n=1,
        status=None) TEAL Pods grow in node's slots (returns them) · loop(scene) a ring turns at the
        controllers · watch_arrows(scene) scheduler and kubelets → API 'watch' · docker_crossed(scene)
        the slide's 'Docker' crossed over containerd (erratum tag) · lamp(scene, key, color=TURN) a
        lamp by that part (color None: off) · blink_lamps(scene) the four symptom lamps once ·
        cloud_arrow(scene, color, text=None) the controllers→cloud arrow recolours (RED on the
        stand-in, GREEN on GKE) with an optional chip · to_standin(scene) outline GREY dashed,
        standin_tag, 'a container you can see', worker 2 leaves.
    ANIM light(key, color=TURN) · normal(key).  .parts{key} .nodes .slot_y .standin"""

    def __init__(self, standin: bool = False, workers: int | None = None, built: tuple = (), **kw):
        super().__init__(**kw)
        self.standin = standin
        self.n_workers = workers or (2 if standin else 3)
        self.parts: dict = {}
        self.lamps: dict = {}
        self.slot = None
        self.pod_slots: dict = {i: [] for i in range(self.n_workers)}
        self._layout()
        self._static(built)

    def _static(self, built):
        """Build parts without animation: 'laptop' (all six chips), 'cluster', 'plane' (plane + workers +
        fan), 'parts' (every inner part, as beat24), 'beat23' (the plane's caption only)."""
        for b in built:
            if b == "laptop":
                self.add(self._mk_laptop(()))
                for n in ("gcloud", "docker", "pulumi", "kubectl", "helm", "gke-gcloud-auth-plugin"):
                    c = self._chip(n).move_to(self._chip_pos(n))
                    self.chips[n] = c
                    self.add(c)
                self.parts["kubectl"] = self.chips["kubectl"]
            elif b == "cluster":
                self.add(self._mk_cluster())
            elif b == "plane":
                self.add(self._mk_plane(), self._mk_nodes())
                self.add(self._mk_fan())
            elif b == "parts":
                for k in ("api", "etcd", "scheduler", "controllers", "cloud", "cloud_arrow", "kubelet", "proxy",
                          "runtime"):
                    self.add(self._mk_part(k))
                self.add(self._links())
            elif b == "beat23":
                cap = label("a container you can see" if self.standin else "run by Google", 20, S.GREY)
                cap.next_to(self.parts["plane"].title, DOWN, buff=0.04)
                self.parts["plane_cap"] = cap
                self.add(cap)
            else:
                raise ValueError(f"MasterDiagram built={b!r}: laptop, cluster, plane, parts, beat23")

    # ---- geometry
    @property
    def slot_y(self) -> float:
        return self.ref.get_center()[1] - 1.25 - 0.42

    def _layout(self):
        p = self.p
        self.G = {
            "cloud": (p(-5.0, 2.35), 2.9, 0.8),
            "laptop": (p(-5.0, 0.25), 2.9, 3.0),
            "toolbox": (p(-5.0, 0.05), 2.62, 2.45),
            "cluster": (p(1.55, 0.75), 9.8, 4.0),
            "plane": (p(-1.45, 0.575), 3.5, 3.35),
            "scheduler": (p(-2.4, 1.2), 1.45, 0.56),
            "controllers": (p(-0.7, 1.2), 1.7, 0.56),
            "api": (p(-1.45, 0.22), 2.3, 0.58),
            "etcd": (p(-1.45, -0.62), 1.15, 0.0),
        }
        ys = [(1.375, 1.85), (0.075, 0.75), (-0.775, 0.75)] if self.n_workers == 3 else [(1.375, 1.85), (-0.35, 1.5)]
        self.node_geo = [(p(3.45, y), 5.7, h) for y, h in ys]

    # ---- builders (no animation)
    def _mk_laptop(self, chips):
        c, w, h = self.G["laptop"]
        fr = frame_box(w, h, LAPTOP, k=0.06)
        fr.move_to(c)
        t = label("your laptop", 20, LAPTOP).move_to(fr).align_to(fr, UL).shift(np.array([0.14, -0.06, 0]))
        tc, tw, th = self.G["toolbox"]
        tb = frame_box(tw, th, CONTAINER, k=0.1).move_to(tc + DOWN * 0.1)
        tn = tag("toolbox", CONTAINER, size=20).move_to(tb.get_top())
        self.parts["laptop"], self.parts["toolbox"] = VGroup(fr, t), VGroup(tb, tn)
        self.chips = {}
        return VGroup(fr, t, tb, tn)

    def _chip(self, name):
        if name == "kubectl":
            return chip("kubectl", TOOL, size=24, pad_x=0.2, pad_y=0.08)
        if name in ("gke-gcloud-auth-plugin", "auth plugin"):
            return two_row_chip("gke-gcloud-", "auth-plugin")
        return chip(name, TOOL, size=20, pad_x=0.14, pad_y=0.06)

    def _chip_pos(self, name):
        tc, tw, th = self.G["toolbox"]
        top = tc[1] - 0.1 + th / 2
        cx = tc[0]
        pos = {"gcloud": (cx - 0.6, top - 0.42), "docker": (cx + 0.6, top - 0.42),
               "pulumi": (cx - 0.6, top - 0.9), "helm": (cx + 0.6, top - 0.9),
               "kubectl": (cx, top - 1.42), "gke-gcloud-auth-plugin": (cx, top - 2.0)}
        x, y = pos["gke-gcloud-auth-plugin" if name == "auth plugin" else name]
        return np.array([x, y, 0])

    def _mk_cluster(self):
        c, w, h = self.G["cluster"]
        col = STANDIN if self.standin else CLOUD
        fr = frame_box(w, h, col, k=0.03, dashed=True).move_to(c)
        if self.standin:
            t = standin_tag()
        else:
            t = label("Kubernetes cluster", 20, CLOUD)
        t.move_to(fr).align_to(fr, UR).shift(np.array([-0.15, -0.07, 0]))
        g = VGroup(fr, t)
        g.frame, g.title = fr, t
        self.parts["cluster"] = g
        return g

    def _mk_plane(self):
        c, w, h = self.G["plane"]
        fr = frame_box(w, h, CLOUD, k=0.14).move_to(c)
        t = label("control plane", 20, INK).move_to(fr).align_to(fr, UP).shift(DOWN * 0.08)
        g = VGroup(fr, t)
        g.frame, g.title = fr, t
        self.parts["plane"] = g
        return g

    def _mk_nodes(self):
        nodes = VGroup()
        for i, (c, w, h) in enumerate(self.node_geo):
            nb = node_box("worker node (VM)", w, h, dashed=False).move_to(c)
            nodes.add(nb)
            self.parts[f"node{i}"] = nb
        self.nodes = nodes
        return nodes

    def _mk_fan(self):
        api_c = self.G["api"][0]
        src = api_c + RIGHT * 1.15
        fan = VGroup(*[arrow(src, nb.frame.get_left() + RIGHT * 0.02, S.GREY, stroke=3) for nb in self.nodes])
        self.parts["fan"] = fan
        return fan

    def _mk_part(self, key):
        if key in ("scheduler", "api"):
            c, w, h = self.G[key]
            g = boxed("scheduler" if key == "scheduler" else "API server", CLOUD, box_w=w, box_h=h, k=0.3)
            g.move_to(c)
        elif key == "controllers":
            c, w, h = self.G[key]
            back = VGroup(*[frame_box(w, h, CLOUD, k=0.22).move_to(c + np.array([0.07 * j, 0.07 * j, 0]))
                            for j in (2, 1)])
            front = boxed("controllers", CLOUD, box_w=w, box_h=h, k=0.3).move_to(c)
            g = VGroup(back, front)
            g.frame, g.text = front.frame, front.text
        elif key == "etcd":
            c = self.G["etcd"][0]
            cyl = disk_cyl(1.15, CLOUD).move_to(c)
            t = label("etcd", 20, INK).move_to(cyl).shift(DOWN * 0.04)
            g = VGroup(cyl, t)
            g.frame, g.text = cyl, t
        elif key == "cloud":
            c, w, h = self.G["cloud"]
            g = boxed("cloud provider API", CLOUD, box_w=w, box_h=h, k=0.18).move_to(c)
        elif key == "kubelet":
            g = VGroup()
            for i, nb in enumerate(self.nodes):
                ch = chip("kubelet", CLOUD, size=20, pad_x=0.14, pad_y=0.05)
                if i == 0:
                    ch.move_to(nb.frame.get_center()).align_to(nb.frame, LEFT).shift(RIGHT * 0.2)
                    ch.set_y(nb.frame.get_center()[1] + 0.12)
                else:
                    ch.move_to(nb.frame.get_center()).shift(RIGHT * 0.25)
                g.add(ch)
            g.frame = g[0].box
        elif key == "proxy":
            nb = self.nodes[0]
            g = chip("kube-proxy", CLOUD, size=20, pad_x=0.14, pad_y=0.05)
            g.next_to(self.parts["kubelet"][0] if "kubelet" in self.parts else nb.frame.get_left(), RIGHT, buff=0.2)
            g.set_y(nb.frame.get_center()[1] + 0.12)
            g.frame = g.box
        elif key == "runtime":
            nb = self.nodes[0]
            fr = nb.frame
            strip = frame_box(fr.width - 0.3, 0.56, CONTAINER, k=0.12).move_to(fr.get_bottom() + UP * 0.38)
            t = label("container runtime: containerd", 20, INK).move_to(strip).align_to(strip, LEFT).shift(RIGHT * 0.14)
            g = VGroup(strip, t)
            g.frame, g.text = strip, t
        elif key == "cloud_arrow":
            ctrl = self.G["controllers"][0]
            cl = self.G["cloud"]
            a = ctrl + np.array([0.2, 0.28, 0])
            b = np.array([a[0], cl[0][1] + 0.12, 0])
            cpt = np.array([cl[0][0] + cl[1] / 2, b[1], 0])
            path = VMobject(stroke_color=ROUTE, stroke_width=4).set_points_as_corners([a, b, cpt + RIGHT * 0.22])
            tip = Arrow(cpt + RIGHT * 0.6, cpt, buff=0, color=ROUTE, stroke_width=4, tip_length=0.2,
                        max_tip_length_to_length_ratio=0.5)
            t = label("nodes, load-balancer IP", 20, ROUTE)
            t.move_to([a[0] + 0.15 + t.width / 2, b[1], 0])
            line = VGroup(path, tip)
            g = VGroup(line, t)
            g.frame, g.text, g.line = line, t, line
        else:
            raise KeyError(key)
        self.parts[key] = g
        return g

    def _links(self):
        """Lines joining scheduler / controllers / etcd to the API server (GREY)."""
        api = self.parts["api"].frame
        out_ = VGroup()
        for k in ("scheduler", "controllers"):
            if k in self.parts and f"link_{k}" not in self.parts:
                fr = self.parts[k].frame
                ln = Line(fr.get_bottom(), [fr.get_center()[0], api.get_top()[1], 0], color=S.GREY, stroke_width=3)
                self.parts[f"link_{k}"] = ln
                out_.add(ln)
        if "etcd" in self.parts and "link_etcd" not in self.parts:
            ln = Line(api.get_bottom(), self.parts["etcd"].frame.get_top() + DOWN * 0.08, color=S.GREY, stroke_width=3)
            self.parts["link_etcd"] = ln
            out_.add(ln)
        return out_

    # ---- PLAYS: build
    def laptop_box(self, scene, chips=("gcloud", "docker", "pulumi"), run_time: float = 0.8):
        """PLAYS: the GREY laptop box with the TEAL toolbox and these PURPLE chips."""
        lap = self._mk_laptop(chips)
        self.show(scene, lap, run_time=run_time)
        if chips:
            self.add_chips(scene, chips, flash=False)
        return lap

    def add_chips(self, scene, names, flash: bool = True, run_time: float = 0.6):
        """PLAYS: tool chips arrive in the toolbox; 'kubectl' flashes YELLOW."""
        new = []
        for n in names:
            c = self._chip(n).move_to(self._chip_pos(n))
            self.chips[n] = c
            new.append(c)
        self.show(scene, *new, anims=[FadeIn(c, shift=DOWN * 0.15) for c in new], run_time=run_time)
        if flash and "kubectl" in names:
            scene.play(Indicate(self.chips["kubectl"], color=TURN, scale_factor=1.15), run_time=0.6)
            self.heal(scene)
        self.parts["kubectl"] = self.chips.get("kubectl", self.parts.get("kubectl"))
        return new

    def cluster(self, scene, source=None, run_time: float = 0.9):
        """PLAYS: the dashed cluster outline (`source`, a mobject on the scene, fades out meanwhile)."""
        g = self._mk_cluster()
        if source is not None:
            scene.play(FadeOut(source), Create(g.frame.edge), FadeIn(g.frame.fill), FadeIn(g.title),
                       run_time=run_time)
            scene.remove(source, g)
            self.add(g)
            self.heal(scene)
            return g
        return self.show(scene, g, anims=[Create(g.frame.edge), FadeIn(g.frame.fill), FadeIn(g.title)],
                         run_time=run_time)

    def beat22(self, scene, run_time: float = 1.0):
        """PLAYS: slide 22 - whatever is missing of laptop (+ all chips), cluster outline, the control
        plane panel, the worker nodes and the fan of arrows from the plane to the workers."""
        if "laptop" not in self.parts:
            self.laptop_box(scene, chips=("gcloud", "docker", "pulumi", "kubectl", "helm", "gke-gcloud-auth-plugin"))
        if "cluster" not in self.parts:
            self.cluster(scene)
        plane = self._mk_plane()
        nodes = self._mk_nodes()
        self.show(scene, plane, *nodes, anims=[FadeIn(plane), LaggedStart(*[FadeIn(n, shift=LEFT * 0.2) for n in nodes],
                                                                          lag_ratio=0.25)], run_time=run_time)
        fan = self._mk_fan()
        self.show(scene, fan, anims=[LaggedStart(*[GrowArrow(a) for a in fan], lag_ratio=0.2)], run_time=0.7)

    def beat23(self, scene, run_time: float = 0.8):
        """PLAYS: slide 23 - the plane gets 'run by Google' (GREY; 'a container you can see' on the
        stand-in) and the slot under the diagram gets the dashed 'slides: master nodes' chip and the
        node-pool line."""
        plane = self.parts["plane"]
        cap = label("a container you can see" if self.standin else "run by Google", 20, S.GREY)
        cap.next_to(plane.title, DOWN, buff=0.04)
        self.parts["plane_cap"] = cap
        self.show(scene, cap, run_time=run_time * 0.5)
        if not self.standin:
            a = dashed_chip("slides: master nodes")
            b = label(f"worker nodes · node pool: 1–2 × {MACHINE} · {REGION}-a", 20, CLOUD)
            row = VGroup(a, b).arrange(RIGHT, buff=0.5).move_to([self.ref.get_center()[0], self.slot_y, 0])
            self._set_slot(scene, row, run_time=run_time * 0.5)

    def part(self, scene, key: str, run_time: float = 0.6):
        """PLAYS: one inner part grows in (its links to the API server draw with it)."""
        if key == "cloud_arrow" and "cloud" not in self.parts:
            self.part(scene, "cloud")
        g = self._mk_part(key)
        anims = [GrowFromCenter(g)] if key not in ("cloud_arrow",) else [Create(g.line), FadeIn(g.text)]
        mobs = [g]
        if "api" in self.parts:
            links = self._links()
            if len(links):
                mobs.append(links)
                anims.append(Create(links))
        self.show(scene, *mobs, anims=anims, run_time=run_time)
        return g

    def beat24(self, scene, lag: float = 0.4):
        """PLAYS: slide 24 - every inner part that is missing, in the deck's order."""
        for k in ("api", "etcd", "scheduler", "controllers", "cloud", "cloud_arrow", "kubelet", "proxy", "runtime"):
            if k not in self.parts:
                self.part(scene, k, run_time=lag)

    # ---- PLAYS: story
    def _target(self, key):
        g = self.parts[key]
        return getattr(g, "frame", g)

    def light(self, key: str, color=TURN):
        """ANIM: the part's outline flashes `color`."""
        return Indicate(self.parts[key], color=color, scale_factor=1.05)

    def normal(self, key: str):
        """ANIM: no-op-sized wiggle back (kept for symmetry with L20)."""
        return Indicate(self.parts[key], color=INK, scale_factor=1.0)

    def _set_slot(self, scene, mob, run_time: float = 0.5):
        if self.slot is not None:
            self.drop(scene, self.slot, run_time=0.25)
        keep_inside(mob)
        self.slot = mob
        self.show(scene, mob, run_time=run_time)

    def callout(self, scene, key: str, text: str | None = None, run_time: float = 0.6):
        """PLAYS: the part flashes YELLOW and its callout (CALLOUTS[key] or `text`) writes in the slot
        under the diagram, replacing the previous one."""
        t = label(text or CALLOUTS[key], 24, INK).move_to([self.ref.get_center()[0], self.slot_y, 0])
        self._set_slot(scene, t, run_time=run_time * 0.6)
        scene.play(self.light("cloud_arrow" if key == "cloud" and "cloud_arrow" in self.parts else key),
                   run_time=run_time)
        self.heal(scene)
        return t

    def clear_slot(self, scene):
        """PLAYS: the slot under the diagram empties."""
        if self.slot is not None:
            self.drop(scene, self.slot, run_time=0.3)
            self.slot = None

    def _point(self, key):
        if key == "kubectl":
            return self.chips["kubectl"].get_center()
        return self._target(key).get_center()

    def pulse(self, scene, keys, color=TURN, run_time: float = 1.2):
        """PLAYS: a dot travels from part to part (keys, e.g. ['kubectl', 'api', 'etcd'])."""
        d = Dot(self._point(keys[0]), radius=0.11, color=color)
        scene.add(d)
        per = run_time / max(1, len(keys) - 1)
        for k in keys[1:]:
            scene.play(d.animate.move_to(self._point(k)), run_time=per)
        scene.play(FadeOut(d), run_time=0.2)
        scene.remove(d)
        self.heal(scene)

    def wish(self, scene, text: str = "desired state", run_time: float = 1.6):
        """PLAYS: a GREEN card rides kubectl → API server → into etcd and stays there (small)."""
        c = boxed(text, OWN, size=20, k=0.25).move_to(self._point("kubectl"))
        scene.add(c)
        scene.play(c.animate.move_to(self._point("api")), run_time=run_time * 0.45)
        scene.play(c.animate.move_to(self._point("etcd")).set_opacity(0), run_time=run_time * 0.45)
        scene.remove(c)
        scene.play(Indicate(self.parts["etcd"], color=OWN, scale_factor=1.08), run_time=0.4)
        self.heal(scene)

    def pick(self, scene, nodes=(0, 1), run_time: float = 0.8):
        """PLAYS: the scheduler lights, then the chosen nodes flash."""
        scene.play(self.light("scheduler"), run_time=run_time * 0.5)
        scene.play(*[Indicate(self.nodes[i].frame, color=TURN, scale_factor=1.02) for i in nodes],
                   run_time=run_time * 0.5)
        self.heal(scene)

    def _slot_point(self, node: int, j: int):
        nb = self.nodes[node].frame
        if node == 0 and "runtime" in self.parts:
            strip = self.parts["runtime"].frame
            x0 = strip.get_right()[0] - 0.35
            return np.array([x0 - j * 0.6, strip.get_center()[1], 0])
        x0 = nb.get_right()[0] - 0.4
        return np.array([x0 - j * 0.6, nb.get_center()[1] - (0.05 if node else 0.0), 0])

    def pods(self, scene, node: int, n: int = 1, status: str | None = None, run_time: float = 0.6):
        """PLAYS: n TEAL Pods grow in node `node`'s slots (right to left). Returns the list."""
        out_ = []
        for _ in range(n):
            j = len(self.pod_slots[node])
            pg = pod_glyph(r=0.2).move_to(self._slot_point(node, j))
            self.pod_slots[node].append(pg)
            out_.append(pg)
        self.show(scene, *out_, anims=[GrowFromCenter(p) for p in out_], run_time=run_time)
        return out_

    def loop(self, scene, run_time: float = 1.2):
        """PLAYS: a YELLOW ring turns once around the controllers box, then goes."""
        fr = self.parts["controllers"].frame
        r = ring_arrows(0.55).move_to(fr)
        scene.play(FadeIn(r), run_time=0.2)
        scene.play(Rotate(r, -TAU / 3), run_time=run_time)
        scene.play(FadeOut(r), run_time=0.2)
        scene.remove(r)
        self.heal(scene)

    def watch_arrows(self, scene, run_time: float = 0.8):
        """PLAYS: arrows from the scheduler and from each kubelet to the API server, labelled 'watch'."""
        api = self.parts["api"].frame
        arrs = VGroup()
        arrs.add(arrow(self.parts["scheduler"].frame.get_bottom() + RIGHT * 0.25, api.get_top() + LEFT * 0.4,
                       TURN, stroke=3, buff=0.02))
        if "kubelet" in self.parts:
            for ch in self.parts["kubelet"]:
                arrs.add(arrow(ch.get_left(), api.get_right(), TURN, stroke=3, buff=0.04))
        t = label("watch", 20, TURN).next_to(api, RIGHT, buff=0.12).shift(DOWN * 0.3)
        g = VGroup(arrs, t)
        self.parts["watch"] = g
        return self.show(scene, g, anims=[LaggedStart(*[GrowArrow(a) for a in arrs], lag_ratio=0.2), FadeIn(t)],
                         run_time=run_time)

    def docker_crossed(self, scene, run_time: float = 0.8):
        """PLAYS: the slide's 'Docker' (GREY) appears just above the word containerd and is crossed
        out, with an erratum tag beside it."""
        strip = self.parts["runtime"]
        cd = strip.text[-len("containerd"):]
        w = label("Docker", 20, S.GREY).next_to(cd, UP, buff=0.2)
        st = strike(w, S.GREY)
        et = erratum_tag().next_to(w, RIGHT, buff=0.2)
        self.parts["docker_x"] = VGroup(w, st, et)
        self.show(scene, w, et, run_time=run_time * 0.5)
        self.show(scene, st, anims=[Create(st)], run_time=run_time * 0.5)

    def lamp(self, scene, key: str, color=TURN, run_time: float = 0.4):
        """PLAYS: a small lamp beside that part, filled `color` (None: the lamp goes out)."""
        if key in self.lamps:
            self.drop(scene, self.lamps.pop(key), run_time=0.2)
        if color is None:
            return None
        tgt = self._target(key) if key != "cloud_arrow" else self.parts["cloud_arrow"].line
        c = Circle(radius=0.12, stroke_color=color, stroke_width=3).set_fill(color, 0.85)
        glow = Circle(radius=0.2, stroke_width=0).set_fill(color, 0.25)
        lp = VGroup(glow, c)
        if key == "cloud_arrow":
            lp.move_to(tgt.get_corner(UR) + np.array([-0.5, 0.0, 0]))
        else:
            lp.move_to(tgt.get_corner(UR) + np.array([-0.05, -0.02, 0]))
        self.lamps[key] = lp
        return self.show(scene, lp, anims=[GrowFromCenter(lp)], run_time=run_time)

    def blink_lamps(self, scene, keys=("scheduler", "controllers", "cloud_arrow", "kubelet")):
        """PLAYS: the four symptom lamps blink once, unlabelled (S03), then go out."""
        for k in keys:
            self.lamp(scene, k, TURN, run_time=0.2)
        scene.wait(0.4)
        for k in keys:
            self.lamp(scene, k, None)

    def cloud_arrow(self, scene, color, text: str | None = None, run_time: float = 0.6):
        """PLAYS: the controllers → cloud provider arrow recolours (RED on the stand-in, GREEN on GKE);
        text: replaces the arrow's label ('no cloud here'), in the same colour. color=ROUTE and
        text=CALLOUTS-style label restore it."""
        ca = self.parts["cloud_arrow"]
        anims = [ca.line.animate.set_color(color)]
        if not text:
            anims.append(ca.text.animate.set_color(color))
        self._ensure(scene)
        scene.play(*anims, run_time=run_time)
        self.heal(scene)
        if text:
            nt = label(text, 20, color).move_to(ca.text, aligned_edge=LEFT)
            ca.text = self.swap(scene, ca.text, nt, run_time=run_time, into=ca)

    def to_standin(self, scene, run_time: float = 0.9):
        """PLAYS: the GKE cluster becomes the kind stand-in: GREY dashed outline, standin_tag as its
        title, the plane's caption 'a container you can see', the third worker leaves."""
        old = self.parts["cluster"]
        self.standin = True
        new = self._mk_cluster()
        self.swap(scene, old, new, run_time=run_time * 0.5)
        if "plane_cap" in self.parts:
            cap = label("a container you can see", 20, S.GREY).move_to(self.parts["plane_cap"])
            self.parts["plane_cap"] = self.swap(scene, self.parts["plane_cap"], cap, run_time=run_time * 0.3)
        if self.n_workers == 3 and hasattr(self, "nodes"):
            gone = [self.nodes[2], self.parts["fan"][2]]
            if "kubelet" in self.parts and len(self.parts["kubelet"]) == 3:
                gone.append(self.parts["kubelet"][2])
            gone += self.pod_slots.get(2, [])
            self.drop(scene, *gone, run_time=run_time * 0.3)
            self.n_workers = 2
        if self.slot is not None:
            self.clear_slot(scene)


# ------------------------------------------------------------------ V2 · FleetMorph
class FleetMorph(_Anchored):
    """V2 · one box, three boxes, a fleet (slides 4-13, 19; S01-S02). Full frame, built at ORIGIN
    (no tracker in S01/S02): pictures in x -6.4 .. 6.4, y -3.2 .. 2.7.
    Slide 5   PLAYS one_vm(scene) a BLUE 'VM' (x -2.8 .. 2.8, y -2.2 .. 0.9): TEAL nginx on top, Frontend /
              API 1 / API 2 under it with PINK lines, a PINK 'HTTP 80' door on its top edge · browser(scene)
              GREY browser above (y 2.1, .win) with a PINK arrow (.req) to the door · question(scene) YELLOW '?' right
              of the VM (drop it with fm.drop(scene, fm.q)).
    Slide 7   clock(scene, text='2:00 a.m.') GREY clock top left · crash(scene, key='api1') the box cracks
              RED, the request bounces with a RED × · app_owner(scene) a ringing phone 'the app owner' right
              of the VM · operator(scene) 'the operator' slides along a PINK 'SSH' tunnel from the left ·
              heal_box(scene, key) the box is TEAL again · l20_chip(scene) the dashed L20 chip under the VM.
    Slide 9   three_vms(scene) the VM becomes three VMs (x centres -4.3, 0, 4.3; y -2.3 .. 0.5) with
              slide 9's layout and a GREY speech card 'put it on several servers' (y 1.35) ·
              glow_backups(scene) · vm_down(scene, i=1) VM i goes dark RED with both copies ·
              lever(scene, i=2) a GREY lever + 'switch: by hand' beside VM i.
    Slide 19  docker_host(scene) left: one BLUE machine with a long GREY 'Docker' bar and five TEAL boxes,
              caption 'container deployment' (x -6.2 .. -0.6) · to_cluster(scene) a copy of it transforms
              into the right side: three nodes each with its own runtime strip and the trio spread
              over them, lines up to one BLUE-greyed 'control plane', caption 'Kubernetes deployment'
              (x 0.6 .. 6.3) · deployment_note(scene) the dashed note under the right caption.
    fade_all(scene) fades the piece and takes it off. .boxes{nginx, front, api1, api2} .vm .vms[i] .q"""

    def __init__(self, **kw):
        super().__init__(**kw)
        self.boxes = {}
        self.vm = None
        self.vms = []
        self.q = None

    def one_vm(self, scene, run_time: float = 1.0):
        p = self.p
        vm = frame_box(5.6, 3.1, CLOUD, k=0.08).move_to(p(0, -0.65))
        t = label("VM", 22, CLOUD).move_to(vm).align_to(vm, UL).shift(np.array([0.18, -0.1, 0]))
        nginx = boxed("nginx", CONTAINER, box_w=1.7, box_h=0.6, mono_font=True).move_to(p(0, 0.05))
        trio = VGroup(*[boxed(n, CONTAINER, box_w=1.5, box_h=0.6) for n in ("Frontend", "API 1", "API 2")])
        trio.arrange(RIGHT, buff=0.3).move_to(p(0, -1.45))
        lines = VGroup(*[Line(nginx.get_bottom(), b.get_top(), color=ROUTE, stroke_width=3) for b in trio])
        dr = door("HTTP 80").move_to(vm.get_top())
        self.vm = VGroup(vm, t)
        self.boxes = {"nginx": nginx, "front": trio[0], "api1": trio[1], "api2": trio[2]}
        self.links, self.door = lines, dr
        self.show(scene, self.vm, nginx, trio, lines, dr, run_time=run_time)

    def browser(self, scene, run_time: float = 0.6):
        b = browser_icon(1.0, name=None).move_to(self.p(0, 2.15))
        a = route(b.get_bottom(), self.door.get_top() + UP * 0.02)
        self.win, self.req = b, a
        self.show(scene, b, run_time=run_time * 0.5)
        self.show(scene, a, anims=[GrowArrow(a)], run_time=run_time * 0.5)

    def question(self, scene):
        self.q = label("?", 48, TURN).move_to(self.p(3.4, -0.4))
        return self.show(scene, self.q, anims=[FadeIn(self.q, scale=1.5)], run_time=0.5)

    def clock(self, scene, text: str = "2:00 a.m."):
        c = clock_face(0.36).move_to(self.p(-5.6, 2.2))
        t = label(text, 22, S.GREY).next_to(c, RIGHT, buff=0.18)
        self.clock_g = VGroup(c, t)
        return self.show(scene, self.clock_g, run_time=0.6)

    def crash(self, scene, key: str = "api1"):
        b = self.boxes[key]
        crack = VMobject(stroke_color=ERR, stroke_width=4).set_points_as_corners(
            [b.get_top() + LEFT * 0.1, b.get_center() + RIGHT * 0.12, b.get_center() + LEFT * 0.08,
             b.get_bottom() + RIGHT * 0.06])
        x = cross_glyph(0.3).move_to(self.door.get_top() + UP * 0.45 + RIGHT * 0.45)
        self.crack, self.x = crack, x
        self._ensure(scene)
        scene.play(b.frame.edge.animate.set_stroke(ERR), Create(crack), run_time=0.5)
        self.add(crack)
        if hasattr(self, "req"):
            scene.play(bounce(self.req.copy().set_opacity(0), self.req.get_start()),
                       Indicate(self.req, color=ERR), run_time=0.5)
        self.show(scene, x, run_time=0.3)

    def app_owner(self, scene):
        ph = phone_glyph().move_to(self.p(4.0, 0.55))
        t = label("the app owner", 20, S.GREY).next_to(ph, DOWN, buff=0.1)
        self.owner_g = VGroup(ph, t)
        self.show(scene, self.owner_g, run_time=0.4)
        scene.play(Rotate(ph, 0.25, rate_func=there_and_back), run_time=0.25)
        scene.play(Rotate(ph, -0.25, rate_func=there_and_back), run_time=0.25)
        self.heal(scene)

    def operator(self, scene, key: str = "api1", run_time: float = 1.4):
        tun = DashedLine(self.p(-6.0, -1.45), np.array([self.vm[0].get_left()[0], self.p(0, -1.45)[1], 0]), color=ROUTE,
                         stroke_width=4, dash_length=0.12)
        st = label("SSH", 20, ROUTE).next_to(tun, UP, buff=0.08).set_x(self.p(-4.3, 0)[0])
        op = you("the operator").move_to(self.p(-5.6, -0.55))
        self.tunnel, self.op = VGroup(tun, st), op
        self.show(scene, self.tunnel, op, anims=[Create(tun), FadeIn(st), FadeIn(op)], run_time=run_time * 0.4)
        scene.play(op.animate.move_to(self.p(-3.4, -0.55)), run_time=run_time * 0.6)
        self.heal(scene)

    def heal_box(self, scene, key: str = "api1"):
        b = self.boxes[key]
        gone = [m for m in (getattr(self, "crack", None), getattr(self, "x", None)) if m is not None]
        self._ensure(scene)
        scene.play(b.frame.edge.animate.set_stroke(CONTAINER), run_time=0.4)
        if gone:
            self.drop(scene, *gone, run_time=0.3)
            self.crack = self.x = None

    def l20_chip(self, scene):
        c = dashed_chip("L20 · one VM · Docker restarts containers · nobody restarts the VM")
        c.move_to(self.p(0, -2.75))
        self.l20 = c
        return self.show(scene, c, run_time=0.5)

    def three_vms(self, scene, run_time: float = 1.2):
        p = self.p
        vms = []
        spec = [("Frontend", None), ("API 1", "API 1 · backup"), ("API 2", "API 2 · backup")]
        for i, (main, backup) in enumerate(spec):
            cx = -4.3 + 4.3 * i
            fr = frame_box(3.9, 2.8, CLOUD, k=0.08).move_to(p(cx, -0.9))
            t = label(f"VM {i + 1}", 20, CLOUD).move_to(fr).align_to(fr, UL).shift(np.array([0.15, -0.08, 0]))
            g = VGroup(fr, t)
            g.frame = fr
            if backup is None:
                b = boxed(main, CONTAINER, box_w=2.0, box_h=0.62).move_to(p(cx, -1.15))
                d = door("HTTP 80").move_to(fr.get_top())
                g.add(b, d)
                g.main, g.backup = b, None
            else:
                ng = boxed("nginx", CONTAINER, box_w=1.6, box_h=0.5, mono_font=True).move_to(p(cx, -0.05))
                b = boxed(main, CONTAINER, box_w=1.4, box_h=0.55).move_to(p(cx - 1.05, -1.35))
                bk = boxed(backup, CONTAINER, box_w=2.1, box_h=0.55, dashed=True).move_to(p(cx + 0.75, -1.35))
                g.add(ng, b, bk)
                g.main, g.backup = b, bk
            vms.append(g)
        say = card(["put it on several servers"], S.GREY, size=22).move_to(p(0, 1.35))
        old = [m for m in (self.vm, *self.boxes.values(), getattr(self, "links", None), getattr(self, "door", None))
               if m is not None]
        for m in old:
            self._detach(m)
        src = VGroup(*old)
        scene.add(src)
        scene.play(FadeTransform(src, VGroup(*vms)), run_time=run_time)
        scene.remove(src, *vms)
        self.vms = vms
        self.add(*vms)
        self.say = say
        self.show(scene, say, run_time=0.4)

    def glow_backups(self, scene):
        self._ensure(scene)
        bks = [v.backup for v in self.vms if v.backup is not None]
        scene.play(*[b.frame.edge.animate(rate_func=there_and_back).set_stroke(TURN, 6) for b in bks],
                   *[Indicate(b.text, color=TURN, scale_factor=1.1) for b in bks], run_time=0.9)
        self.heal(scene)

    def vm_down(self, scene, i: int = 1):
        v = self.vms[i]
        self._ensure(scene)
        scene.play(v.animate.set_opacity(0.35), run_time=0.4)
        scene.play(v.frame.edge.animate.set_stroke(ERR, opacity=1), run_time=0.3)
        self.heal(scene)

    def lever(self, scene, i: int = 2):
        v = self.vms[i]
        lv = lever_glyph(0.7)
        hand = person_icon(S.GREY, 0.5)
        t = label("switch: by hand", 20, S.GREY)
        g = VGroup(lv, hand).arrange(RIGHT, buff=0.12)
        t.next_to(g, DOWN, buff=0.08)
        g = VGroup(g, t).next_to(v.frame, DOWN, buff=0.08)
        keep_inside(g)
        self.lever_g = g
        self.show(scene, g, run_time=0.5)
        scene.play(Rotate(lv.handle, -0.9, about_point=lv[0].get_top()), run_time=0.5)
        self.heal(scene)

    def docker_host(self, scene, run_time: float = 1.0):
        p = self.p
        m = frame_box(5.6, 3.0, CLOUD, k=0.08).move_to(p(-3.4, -0.2))
        bar = boxed("Docker", S.GREY, box_w=5.2, box_h=0.5, k=0.25).move_to(p(-3.4, -1.3))
        boxes = VGroup(*[image_block(None, 0.85, 0.85) for _ in range(5)]).arrange(RIGHT, buff=0.15)
        boxes.next_to(bar, UP, buff=0.12)
        cap = label("container deployment", 22, INK).next_to(m, DOWN, buff=0.2)
        self.host = VGroup(m, bar, boxes)
        self.host_cap = cap
        self.show(scene, self.host, cap, run_time=run_time)

    def to_cluster(self, scene, run_time: float = 1.4):
        p = self.p
        plane = boxed("control plane", CLOUD, box_w=2.8, box_h=0.6, k=0.3).move_to(p(3.45, 1.55))
        nodes = VGroup()
        for i in range(3):
            n = frame_box(1.75, 2.2, CLOUD, k=0.08)
            strip = frame_box(1.55, 0.3, S.GREY, k=0.25).move_to(n.get_bottom() + UP * 0.25)
            n = VGroup(n, strip)
            nodes.add(n)
        nodes.arrange(RIGHT, buff=0.25).move_to(p(3.45, -0.65))
        spread = [("Frontend", "API 1"), ("API 2", "Frontend"), ("API 1", "API 2")]
        apps = VGroup()
        for n, names in zip(nodes, spread):
            col = VGroup(*[boxed(s, CONTAINER, box_w=1.45, box_h=0.5) for s in names]).arrange(DOWN, buff=0.12)
            col.move_to(n[0]).shift(UP * 0.25)
            apps.add(col)
        lines = VGroup(*[Line(plane.get_bottom(), n[0].get_top(), color=S.GREY, stroke_width=2) for n in nodes])
        cap = label("Kubernetes deployment", 22, INK).next_to(nodes, DOWN, buff=0.2)
        right = VGroup(plane, nodes, apps, lines)
        src = self.host.copy()
        scene.add(src)
        scene.play(FadeTransform(src, right), run_time=run_time)
        scene.remove(src, right)
        self.cluster_g, self.cluster_cap = right, cap
        self.add(right)
        self.show(scene, cap, run_time=0.4)

    def deployment_note(self, scene):
        a = label("deployment = a way of deploying ·", 20, S.GREY)
        b = label("≠", 20, S.GREY)
        c = mono("Deployment", 20, OWN)
        d = label(", the object (S06)", 20, S.GREY)
        row = VGroup(a, b, c, d).arrange(RIGHT, buff=0.1)
        ob = outline_box(row.width + 0.4, row.height + 0.3, PAST, solid=False)
        row.move_to(ob)
        g = VGroup(ob, row).next_to(self.cluster_cap, DOWN, buff=0.15)
        keep_inside(g)
        self.note_g = g
        self.show(scene, g, run_time=0.5)
        scene.play(Indicate(c, color=OWN, scale_factor=1.12), run_time=0.6)
        self.heal(scene)

    def fade_all(self, scene, run_time: float = 0.5):
        scene.play(FadeOut(self), run_time=run_time)
        scene.remove(self)


# ------------------------------------------------------------------ V3 · LabelLink
class LabelLink(_Anchored):
    """V3 · two objects, one sticker (slide 39 made honest; S06, S08). A horizontal strip, built at
    ORIGIN: x -6.3 .. 6.3, y -1.0 .. 0.9 (endpoints row to y -1.55).
        GREEN card 'Deployment · web' / 'keep 2' (x -6.3 .. -3.5) emits two TEAL Pods (x -1.7 and 0.3)
        that each get a PINK sticker 'run: web'; a PINK 'Service · web · :80' door (x 3.3 .. 6.3) throws
        a dashed PINK lasso around every Pod wearing the sticker.
    PLAYS deployment(scene) · make_pods(scene, n=2) (from the card) · stickers(scene) (fly from the card) ·
        service(scene) · lasso(scene) · build(scene) all five · endpoints(scene, items=ENDPOINTS,
        note=None) the lasso's endpoints list under it (PINK mono) · swap_endpoint(scene, i, new) one
        address becomes another (S08's illustration) · replace_pod(scene, i, new_name=None) Pod i fades,
        a new one grows with a fresh sticker.
    ANIM flash_labels() stickers + lasso Indicate together.
    .card .pods[i] .tags[i] (stickers) .svc .lasso_g (ring, arrow) .eps (.items)"""

    def __init__(self, **kw):
        super().__init__(**kw)
        self.pods, self.tags = [], []
        self.card = self.svc = self.lasso_g = self.eps = None

    def _pod_xy(self, i):
        return self.p(-1.7 + 2.0 * i, 0.25)

    def deployment(self, scene):
        c = boxed(["Deployment · web", "keep 2"], OWN, box_w=2.8, box_h=1.0, size=22, k=0.18)
        c.move_to(self.p(-4.9, 0.0))
        self.card = c
        return self.show(scene, c, run_time=0.5)

    def make_pods(self, scene, n: int = 2):
        """PLAYS: n Pods grow out of the Deployment card."""
        new = []
        for i in range(n):
            pg = pod_glyph(r=0.32).move_to(self._pod_xy(len(self.pods)))
            self.pods.append(pg)
            new.append(pg)
        src = self.card.get_center()
        anims = [GrowFromPoint(pg, src) for pg in new]
        return self.show(scene, *new, anims=anims, run_time=0.7)

    def _sticker(self, i):
        s = route_chip("run: web", size=20)
        return s.next_to(self.pods[i], DOWN, buff=0.12)

    def stickers(self, scene):
        new = []
        for i in range(len(self.pods)):
            s = self._sticker(i)
            self.tags.append(s)
            new.append(s)
        src = self.card.get_center()
        starts = [s.copy().move_to(src).set_opacity(0) for s in new]
        self._ensure(scene)
        scene.add(*starts)
        scene.play(*[Transform(st, s) for st, s in zip(starts, new)], run_time=0.7)
        scene.remove(*starts)
        self.add(*new)
        self.heal(scene)
        return new

    def service(self, scene):
        s = boxed("Service · web · :80", ROUTE, box_w=3.0, box_h=0.8, size=22, k=0.18)
        s.move_to(self.p(4.8, 0.0))
        self.svc = s
        return self.show(scene, s, run_time=0.5)

    def _lasso_shape(self):
        grp = VGroup(*self.pods, *self.tags)
        return ring(grp, ROUTE, buff=0.18, stroke=3, dashed=True)

    def lasso(self, scene):
        ls = self._lasso_shape()
        a = route(self.svc.get_left(), ls.get_right() + RIGHT * 0.02)
        self.lasso_g = VGroup(ls, a)
        return self.show(scene, self.lasso_g, anims=[Create(ls), GrowArrow(a)], run_time=0.8)

    def build(self, scene):
        self.deployment(scene)
        self.make_pods(scene)
        self.stickers(scene)
        self.service(scene)
        self.lasso(scene)

    def flash_labels(self):
        return AnimationGroup(*[Indicate(t, color=ROUTE, scale_factor=1.12) for t in self.tags],
                              Indicate(self.lasso_g[0], color=ROUTE, scale_factor=1.03))

    def endpoints(self, scene, items=ENDPOINTS, note: str | None = None):
        row = VGroup(*[mono(s, 20, ROUTE) for s in items]).arrange(RIGHT, buff=0.3)
        lab = label("endpoints:", 20, S.GREY)
        g = VGroup(lab, row).arrange(RIGHT, buff=0.2).next_to(self.lasso_g[0], DOWN, buff=0.12)
        g.items = row
        parts = [g]
        if note:
            ch = grey_chip(note).next_to(g, RIGHT, buff=0.25)
            parts.append(ch)
        self.eps = VGroup(*parts)
        self.eps.items = row
        keep_inside(self.eps)
        return self.show(scene, self.eps, run_time=0.5)

    def swap_endpoint(self, scene, i: int, new: str):
        old = self.eps.items[i]
        nw = mono(new, 20, ROUTE).move_to(old)
        self.swap(scene, old, nw, run_time=0.6, into=self.eps.items)
        subs = self.eps.items.submobjects
        subs.insert(i, subs.pop())                     # keep the order of the list
        return nw

    def replace_pod(self, scene, i: int):
        old_p, old_t = self.pods[i], self.tags[i]
        self.drop(scene, old_p, old_t, run_time=0.4)
        pg = pod_glyph(r=0.32).move_to(self._pod_xy(i))
        self.pods[i] = pg
        self.show(scene, pg, anims=[GrowFromCenter(pg)], run_time=0.4)
        s = self._sticker(i)
        self.tags[i] = s
        self.show(scene, s, run_time=0.3)


def port_path(size: float = 20) -> VGroup:
    """S06's PINK path of three ports: 'port: 80' → 'targetPort: 8080' → 'containerPort: 8080'
    (deploy-k8s-tic-tac-toe.yml:30, :32, :21). ~8.4 wide, centred at ORIGIN. .chips[i] .arrows"""
    chips = VGroup(*[route_chip(s, size=size) for s in ("port: 80", "targetPort: 8080", "containerPort: 8080")])
    chips.arrange(RIGHT, buff=0.7)
    arrs = VGroup(*[route(chips[i].get_right(), chips[i + 1].get_left(), stroke=3) for i in range(2)])
    g = VGroup(chips, arrs)
    g.chips, g.arrows = chips, arrs
    return g


# ------------------------------------------------------------------ V4 · ControllerLoop
class ControllerLoop(_Anchored):
    """V4 · desired state, kept (S07; the Job cousin in S12, S15).

    Deployment mode, ControllerLoop(): built at ORIGIN in x -6.3 .. 6.45, y -1.25 .. 2.75 (fits over a
    3-row strip, under the tracker and beside the small AsksChecklist).
        cards row y 1.85 .. 2.75: GREEN 'deployment.apps/web' / 'replicas: 2' (x -6.3 .. -2.6) →
        GREEN 'replicaset.apps/' / 'web-5cd9789488' (x -2.2 .. 1.0); two worker lanes y -0.85 .. 1.45
        ('node: worker2' x -6.3 .. -1.6, 'node: worker' x -1.4 .. 3.3), two Pod rows each (pod_name in
        three colours, status under it); right column x 3.6 .. 6.45: BLUE-greyed 'controllers' with
        the YELLOW ring, 'observe → compare → act', the counter 'desired 2 · actual 2' + a small dial;
        caption row y -1.1 (x -3.1 .. 3.1). Right column: 'controllers' at (4.95, 0.55) inside a ring
        (y -0.3 .. 1.4: clear of the small AsksChecklist, which ends at y 1.55), the words at y -0.55,
        the counter at y -0.95.
      PLAYS deployment(scene, src=None) · replicaset(scene, src=None) (src: a mobject, e.g. terminal
        glyphs, to TransformFromCopy from) · pod(scene, suffix, lane, status='Running', src=None) one
        Pod (returns it; lanes 0 = worker2, 1 = worker) · pods(scene, srcs=None) the two k50 Pods ·
        loop(scene) ring + 'observe → compare → act' + counter · spin(scene) the ring turns once ·
        count(scene, desired, actual) counter (RED when they differ) · needle(scene) the dial swings
        back · caption(scene, text) the caption row · kill(scene, suffix) Pod struck, fades, counter
        drops · respawn(scene, suffix=NEW_SUFFIX, lane=None, status='ContainerCreating') a new Pod in the
        first free slot · status(scene, suffix, status) a Pod's status word changes · remove_pod(scene,
        suffix) a Pod fades without a strike · clear_caption(scene).
      .dep .rs .lanes[i] .pods{suffix} .ring .counter

    Job mode, ControllerLoop(job=True, name='vector-db-loader', api=True): built at ORIGIN in
    x -4.9 .. 4.6, y -0.75 .. 0.95: GREEN 'Job' / name card (x -3.4), its one Pod (x -0.9, status under
    it), and with api=True a YELLOW hourglass (x 1.3, caption 'Pulumi waits for Complete' above it)
    before a dashed GREEN 'api' card (x 3.65). S15: ControllerLoop(job=True, name='hello-job', api=False).
      PLAYS job_card(scene) · run_job(scene, pod_name=None) the Pod grows 'Running', turns 'Completed'
        GREY and is not replaced · hourglass(scene) · release(scene) the api card turns solid."""

    def __init__(self, job: bool = False, name: str = "vector-db-loader", api: bool = True, **kw):
        super().__init__(**kw)
        self.job = job
        self.job_name = name
        self.api = api
        self.pod_map: dict = {}
        self.slots = {0: [], 1: []}
        self.dep = self.rs = self.ring = self.counter = self.cap = None
        self.desired, self.actual = 2, 2
        if not job:
            p = self.p
            self.lanes = VGroup()
            for i, (x0, x1, nm) in enumerate(((-6.3, -1.6, "node: worker2"), (-1.4, 3.3, "node: worker"))):
                ln = node_box(nm, x1 - x0, 2.3).move_to(p((x0 + x1) / 2, 0.3))
                self.lanes.add(ln)
            ctl = boxed("controllers", CLOUD, box_w=1.75, box_h=0.5, k=0.3).move_to(p(4.95, 0.55))
            self.ctl = ctl
            self.add(self.lanes, ctl)

    # ---- deployment mode
    def _from(self, scene, new, src, run_time=0.8):
        if src is None:
            return self.show(scene, new, run_time=run_time * 0.6)
        cp = src.copy()
        scene.add(cp)
        scene.play(cp.animate.move_to(new).set_opacity(0), FadeIn(new, target_position=src.get_center()),
                   run_time=run_time)
        scene.remove(cp, new)
        self.add(new)
        self.heal(scene)
        return new

    def deployment(self, scene, src=None, replicas: int = 2):
        c = boxed(["deployment.apps/web", f"replicas: {replicas}"], OWN, box_w=3.7, box_h=0.9,
                  mono_font=True, k=0.18).move_to(self.p(-4.45, 2.3))
        self.dep = c
        return self._from(scene, c, src)

    def replicaset(self, scene, src=None):
        c = boxed(["replicaset.apps/", f"web-{RS_HASH}"], OWN, box_w=3.2, box_h=0.9, mono_font=True,
                  k=0.18).move_to(self.p(-0.6, 2.3))
        self.rs = c
        r = self._from(scene, c, src)
        a = arrow(self.dep.get_right(), c.get_left(), OWN, buff=0.08)
        self.show(scene, a, anims=[GrowArrow(a)], run_time=0.3)
        self.rs_arrow = a
        return r

    def _slot_xy(self, lane: int, j: int):
        ln = self.lanes[lane].frame
        return np.array([ln.get_left()[0] + 0.45, ln.get_top()[1] - 0.72 - j * 0.9, 0])

    def pod(self, scene, suffix: str, lane: int, status: str = "Running", src=None, run_time: float = 0.6):
        j = len(self.slots[lane])
        if j >= 2:
            raise ValueError(f"ControllerLoop: lane {lane} is full")
        pg = pod_glyph(f"web-{RS_HASH}-{suffix}", status, r=0.22, side=RIGHT)
        pg.shift(self._slot_xy(lane, j) - pg.circle.get_center())
        self.slots[lane].append(suffix)
        self.pod_map[suffix] = pg
        if src is not None:
            return self._from(scene, pg, src, run_time)
        return self.show(scene, pg, anims=[GrowFromCenter(pg)], run_time=run_time)

    def pods(self, scene, srcs=None):
        """PLAYS: k50's two Pods: -5h48s on worker2 (lane 0), -bmkj5 on worker (lane 1)."""
        srcs = srcs or (None, None)
        self.pod(scene, POD_SUFFIXES[0], 0, src=srcs[0])
        self.pod(scene, POD_SUFFIXES[1], 1, src=srcs[1])

    def _counter(self, desired, actual):
        col = OWN if desired == actual else ERR
        return steady(f"desired {desired} · actual {actual}", 22, col).move_to(self.p(4.75, -0.95))

    def loop(self, scene):
        r = ring_arrows(0.85).move_to(self.ctl)
        words = label("observe → compare → act", 20, TURN).move_to(self.p(4.95, -0.55))
        self.ring = r
        self.words = words
        self.counter = self._counter(self.desired, self.actual)
        dial = VGroup(Arc(radius=0.2, start_angle=0, angle=PI, color=S.GREY, stroke_width=3),
                      Line(ORIGIN, UP * 0.17, color=TURN, stroke_width=3)).next_to(self.counter, RIGHT, buff=0.15)
        dial.align_to(self.counter, DOWN)
        self.dial = dial
        self.show(scene, r, words, anims=[Create(r), FadeIn(words)], run_time=0.8)
        self.show(scene, self.counter, dial, run_time=0.4)

    def spin(self, scene, run_time: float = 1.0):
        self._ensure(scene)
        scene.play(Rotate(self.ring, -TAU / 3), run_time=run_time)
        self.heal(scene)

    def needle(self, scene):
        nd = self.dial[1]
        piv = self.dial[0].get_bottom() + UP * 0.0
        piv = np.array([self.dial[0].get_center()[0], self.dial[0].get_bottom()[1], 0])
        self._ensure(scene)
        scene.play(Rotate(nd, 0.8, about_point=piv), run_time=0.4)
        scene.play(Rotate(nd, -0.8, about_point=piv), run_time=0.6)
        self.heal(scene)

    def count(self, scene, desired: int, actual: int):
        self.desired, self.actual = desired, actual
        new = self._counter(desired, actual)
        self._ensure(scene)
        scene.play(Transform(self.counter, new), run_time=0.4)
        self.heal(scene)

    def caption(self, scene, text: str = "you set the number; the controller keeps it true"):
        c = label(text, 22, S.GREY).move_to(self.p(0, -1.1))
        if self.cap is not None:
            self.drop(scene, self.cap, run_time=0.2)
        self.cap = c
        return self.show(scene, c, run_time=0.5)

    def clear_caption(self, scene):
        if self.cap is not None:
            self.drop(scene, self.cap, run_time=0.3)
            self.cap = None

    def kill(self, scene, suffix: str):
        pg = self.pod_map.pop(suffix)
        st = Line(pg.circle.get_left() + LEFT * 0.1, pg.name.get_right() + RIGHT * 0.05, color=ERR, stroke_width=4)
        scene.play(Create(st), run_time=0.3)
        scene.remove(st)
        for lane in self.slots.values():
            if suffix in lane:
                lane[lane.index(suffix)] = None
        self.drop(scene, pg, run_time=0.4)
        self.count(scene, self.desired, self.actual - 1)

    def remove_pod(self, scene, suffix: str):
        pg = self.pod_map.pop(suffix)
        for lane in self.slots.values():
            if suffix in lane:
                lane[lane.index(suffix)] = None
        self.drop(scene, pg, run_time=0.4)

    def respawn(self, scene, suffix: str = NEW_SUFFIX, lane: int | None = None, status: str = "ContainerCreating"):
        """PLAYS: a new Pod grows in the first free slot (same hash, new suffix)."""
        for ln in ([lane] if lane is not None else [0, 1]):
            if None in self.slots[ln]:
                j = self.slots[ln].index(None)
                pg = pod_glyph(f"web-{RS_HASH}-{suffix}", status, r=0.22, side=RIGHT)
                pg.shift(self._slot_xy(ln, j) - pg.circle.get_center())
                self.slots[ln][j] = suffix
                self.pod_map[suffix] = pg
                return self.show(scene, pg, anims=[GrowFromCenter(pg)], run_time=0.6)
        raise ValueError("ControllerLoop.respawn: no free slot")

    def status(self, scene, suffix: str, status: str):
        pg = self.pod_map[suffix]
        new = pod_status(status).move_to(pg.status, aligned_edge=LEFT)
        pg.status = self.swap(scene, pg.status, new, run_time=0.4, into=pg)

    # ---- job mode
    def job_card(self, scene):
        c = boxed(["Job", self.job_name], OWN, box_w=3.0, box_h=0.95, k=0.18).move_to(self.p(-3.4, 0.0))
        self.jcard = c
        self.show(scene, c, run_time=0.5)
        if self.api:
            a = boxed(["api", "Deployment"], OWN, box_w=1.9, box_h=0.95, dashed=True, k=0.06).move_to(self.p(3.65, 0.0))
            self.api_card = a
            self.show(scene, a, run_time=0.4)
        return c

    def run_job(self, scene, pod_name: str | None = None):
        pg = pod_glyph(None, "Running", r=0.3)
        pg.shift(self.p(-0.9, 0.12) - pg.circle.get_center())
        self.jpod = pg
        self.show(scene, pg, anims=[GrowFromPoint(pg, self.jcard.get_center())], run_time=0.6)
        scene.wait(0.4)
        new = pod_status("Completed").move_to(pg.status)
        pg.status = self.swap(scene, pg.status, new, run_time=0.4, into=pg)
        self._ensure(scene)
        scene.play(pg.circle.animate.set_fill(opacity=0.25), pg.dots.animate.set_opacity(0.4), run_time=0.4)
        self.heal(scene)

    def hourglass(self, scene):
        h = hourglass(0.55).move_to(self.p(1.3, 0.0))
        t = label("Pulumi waits for Complete", 20, TURN).next_to(h, UP, buff=0.15)
        self.glass = VGroup(h, t)
        self.show(scene, self.glass, run_time=0.5)
        scene.play(Rotate(h, PI), run_time=0.6)
        self.heal(scene)

    def release(self, scene):
        a = self.api_card
        solid = boxed(["api", "Deployment"], OWN, box_w=1.9, box_h=0.95, k=0.18).move_to(a)
        self.api_card = self.swap(scene, a, solid, run_time=0.5)


# ------------------------------------------------------------------ V5 · CheeseBlueprint
class CheeseBlueprint(_Anchored):
    """V5 · the whole cheese app on GKE (digest §1; S09). Built at ORIGIN, full frame (no tracker):
    the picture lives at the left, x -6.3 .. 0.3, y -3.0 .. 2.45 (table on the right, x 0.7 .. 6.5);
    after the table, slide_center() slides it to x -3.3 .. 3.3 and the VPC pieces go around it.
      L20 VM (GREY dashed, l20_vm()) → cluster outline 'cheese-app-cluster' (BLUE dashed); inside it:
      ingress row y 1.6 (nginx box → 'nginx-f5' controller + 'cheese-app-ingress' rule card),
      Deployment cards row y 0.42 (frontend, api, vector-db: GREEN cards with a TEAL Pod), Service tags
      row y -0.42 (PINK 'frontend :3000', 'api :9000', 'vector-db :8000'), PVC row y -1.25 (BLUE disks
      'persistent-pvc 5Gi', 'chromadb-pvc 10Gi'), Job + Workload Identity row y -2.05, node pool strip
      y -2.65.
    PLAYS l20(scene) the L20 VM · dissolve(scene) it becomes the cluster with the containers in place ·
        row(scene, i) table row i (BLUEPRINT_ROWS) writes on the right AND the picture changes
        (0 cards+Pods, 1 Job, 2 Service tags, 3 PVC disks, 4 Ingress, 5 WI badge, 6 ReplicaSet rings,
        7 node pool) · drop_table(scene) · slide_center(scene) · vpc(scene) BLUE 'cheese-app-vpc · subnet
        10.0.0.0/19' frame (x -3.75 .. 3.75, y -3.35 .. 2.8) · private_nodes(scene) the nodes' public-IP
        badges peel off · nat(scene) BLUE 'Cloud NAT' funnel at the right edge, 'outbound only' ·
        namespace(scene) GREEN dashed 'cheese-app-namespace' frame around the app (label top-left) · lb(scene) BLUE
        load-balancer box at the left edge with a PINK arrow to nginx · chip(scene, key, text) a GREY
        scene chip in a column right of the VPC (x 4.05 .., from y 2.0 down), a thin line to the part.
    .parts{nginx, ingress, front, api, vdb, job, svc_front, svc_api, svc_vdb, pvc1, pvc2, wi, pool} .table"""

    def __init__(self, **kw):
        super().__init__(**kw)
        self.parts: dict = {}
        self.table = VGroup()
        self.vm = None
        self.cluster_box = None
        self.extras: dict = {}

    def l20(self, scene, run_time: float = 0.8):
        vm = l20_vm(6.4, 5.3).move_to(self.p(-3.0, -0.25))
        self.vm = vm
        return self.show(scene, vm, run_time=run_time)

    def _cards(self):
        out_ = {}
        for key, name, x in (("front", "frontend", -5.05), ("api", "api", -3.0), ("vdb", "vector-db", -0.95)):
            c = boxed([name, "Deployment"], OWN, box_w=1.95, box_h=0.85, k=0.16).move_to(self.p(x, 0.42))
            c.text.align_to(c.frame, LEFT).shift(RIGHT * 0.12)
            pg = pod_glyph(r=0.15, dots=1).move_to(c.frame.get_right() + LEFT * 0.25)
            g = VGroup(c, pg)
            g.card, g.pod = c, pg
            out_[key] = g
        return out_

    def dissolve(self, scene, run_time: float = 1.2):
        vm = self.vm
        fr = frame_box(6.6, 5.45, CLOUD, k=0.04, dashed=True).move_to(self.p(-3.0, -0.27))
        t = label(CLUSTER, 20, CLOUD).move_to(fr).align_to(fr, UL).shift(np.array([0.15, -0.08, 0]))
        cl = VGroup(fr, t)
        self.cluster_box = cl
        b = vm.boxes
        for k in b:
            self._detach(b[k])
        self._detach(vm)
        scene.add(vm)
        keep = VGroup(*[b[k] for k in ("nginx", "front", "api", "vdb", "loader")])
        scene.remove(*keep)
        rest = VGroup(vm.frame, vm.title)
        targets = {"nginx": self.p(-3.0, 1.6), "front": self.p(-5.05, 0.42), "api": self.p(-3.0, 0.42),
                   "vdb": self.p(-0.95, 0.42), "loader": self.p(-1.15, -2.05)}
        scene.play(ReplacementTransform(rest, cl), *[b[k].animate.move_to(targets[k]) for k in targets],
                   run_time=run_time)
        scene.remove(rest, cl, *keep)
        self.add(cl, *keep)
        self.parts.update({"nginx": b["nginx"], "front": b["front"], "api": b["api"], "vdb": b["vdb"],
                           "loader": b["loader"]})
        self.heal(scene)

    def _table_row(self, i):
        a, b = BLUEPRINT_ROWS[i]
        la = label(a, 20, S.GREY)
        ar = label("→", 20, S.GREY)
        lb = label(b, 20, OWN)
        r = VGroup(la, ar, lb).arrange(RIGHT, buff=0.14)
        y = 2.25 - i * 0.62
        r.move_to(self.p(0.75, y), aligned_edge=LEFT)
        if r.get_right()[0] > self.p(6.5, 0)[0]:
            raise ValueError(f"CheeseBlueprint table row {i} is {r.width:.2f} wide")
        return r

    def row(self, scene, i: int, run_time: float = 0.8):
        r = self._table_row(i)
        self.show(scene, r, run_time=0.4, into=self.table)
        if self.table not in self.submobjects:
            self.add(self.table)
        getattr(self, f"_row{i}")(scene, run_time)
        return r

    def _row0(self, scene, rt):
        cards = self._cards()
        for k in ("front", "api", "vdb"):
            old = self.parts[k]
            self.parts[k] = self.swap(scene, old, cards[k], run_time=rt * 0.4)

    def _row1(self, scene, rt):
        j = boxed(["Job", "vector-db-loader"], OWN, box_w=2.3, box_h=0.75, k=0.16).move_to(self.p(-1.15, -2.05))
        self.parts["job"] = self.swap(scene, self.parts.pop("loader"), j, run_time=rt * 0.5)
        a = arrow(j.get_corner(UR) + LEFT * 0.25, self.p(-0.25, -0.0), OWN, buff=0.04)
        self.parts["job_arrow"] = a
        self.show(scene, a, anims=[GrowArrow(a)], run_time=0.3)

    def _row2(self, scene, rt):
        new = []
        for k, x in (("front", -5.05), ("api", -3.0), ("vdb", -0.95)):
            t = chip(f"{SVC_NAMES[k]} :{PORTS[k]}", ROUTE, size=20, pad_x=0.12, pad_y=0.05)
            t.move_to(self.p(x, -0.42))
            self.parts[f"svc_{k}"] = t
            new.append(t)
        self.show(scene, *new, anims=[FadeIn(t, shift=UP * 0.15) for t in new], run_time=rt * 0.5)

    def _row3(self, scene, rt):
        new = []
        for key, name, x in (("pvc1", "persistent-pvc 5Gi", -4.95), ("pvc2", "chromadb-pvc 10Gi", -1.95)):
            d = disk_cyl(0.42).move_to(self.p(x - 0.95, -1.25))
            t = label(name, 20, INK).next_to(d, RIGHT, buff=0.1)
            g = VGroup(d, t)
            self.parts[key] = g
            new.append(g)
        self.show(scene, *new, run_time=rt * 0.5)

    def _row4(self, scene, rt):
        ng = boxed(["nginx-f5", "Ingress controller"], CONTAINER, box_w=2.6, box_h=0.75, k=0.18)
        ng.move_to(self.p(-4.55, 1.6))
        ing = boxed([INGRESS, "the rule"], ROUTE, box_w=2.6, box_h=0.75, k=0.14).move_to(self.p(-1.55, 1.6))
        self.parts["nginx"] = self.swap(scene, self.parts["nginx"], ng, run_time=rt * 0.4)
        self.parts["ingress"] = ing
        self.show(scene, ing, run_time=rt * 0.3)

    def _row5(self, scene, rt):
        w = chip("api: Workload Identity", OWN, size=20, pad_x=0.14, pad_y=0.05).move_to(self.p(-4.6, -2.05))
        self.parts["wi"] = w
        self.show(scene, w, run_time=rt * 0.4)

    def _row6(self, scene, rt):
        rings = VGroup()
        for k in ("front", "api", "vdb"):
            c = self.parts[k].card.frame
            r = ring_arrows(0.13, OWN, stroke=2.5).move_to(c.get_corner(UR) + np.array([-0.2, -0.18, 0]))
            rings.add(r)
        self.parts["rings"] = rings
        self.show(scene, rings, run_time=rt * 0.4)

    def _row7(self, scene, rt):
        strip = frame_box(6.1, 0.42, CLOUD, k=0.2).move_to(self.p(-3.0, -2.67))
        t = label(f"node pool · 1–2 × {MACHINE}", 20, INK).move_to(strip).align_to(strip, LEFT).shift(RIGHT * 0.15)
        badges = chip("public IPs", S.GREY, size=20, pad_x=0.1, pad_y=0.02)
        badges.move_to(strip).align_to(strip, RIGHT).shift(LEFT * 0.1)
        pool = VGroup(strip, t)
        self.parts["pool"], self.parts["badges"] = pool, badges
        self.show(scene, pool, badges, run_time=rt * 0.5)

    def drop_table(self, scene):
        rows = list(self.table.submobjects)
        if rows:
            self.drop(scene, *rows, run_time=0.4)

    def slide_center(self, scene, run_time: float = 0.8):
        self._ensure(scene)
        scene.play(self.animate.shift(RIGHT * 3.0), run_time=run_time)
        self.heal(scene)

    def _c(self, x, y):
        """A point relative to the picture's own centre (after slide_center(): the frame's centre)."""
        return self.cluster_box[0].get_center() + np.array([x, y, 0])

    def vpc(self, scene):
        fr = frame_box(7.4, 6.2, CLOUD, k=0.0, stroke=3).move_to(self._c(0, 0.1))
        fr.fill.set_fill(opacity=0)
        t = label(f"{VPC} · subnet {SUBNET_RANGE}", 20, CLOUD).move_to(fr).align_to(fr, UL).shift(np.array([0.15, -0.06, 0]))
        t.set_y(fr.get_top()[1] - 0.2)
        g = VGroup(fr, t)
        self.extras["vpc"] = g
        return self.show(scene, g, run_time=0.6)

    def private_nodes(self, scene):
        b = self.parts.pop("badges")
        cap = label("private nodes", 20, CLOUD).move_to(b)
        self.drop(scene, b, run_time=0.5, shift=UP * 0.4)
        self.extras["private"] = cap
        self.show(scene, cap, run_time=0.3)

    def nat(self, scene):
        edge = self.extras["vpc"][0].get_right()[0] if "vpc" in self.extras else self._c(3.3, 0)[0]
        f = Polygon([0, 0.35, 0], [0, -0.35, 0], [0.55, -0.12, 0], [0.55, 0.12, 0], stroke_color=CLOUD,
                    stroke_width=3).set_fill(tint(CLOUD, 0.3), 1)
        f.move_to([edge + 0.05, self._c(0, -1.6)[1], 0])
        t = VGroup(label("Cloud NAT", 20, CLOUD), label("outbound only", 20, S.GREY)).arrange(DOWN, buff=0.04,
                                                                                             aligned_edge=LEFT)
        t.next_to(f, RIGHT, buff=0.12)
        g = VGroup(f, t)
        keep_inside(g)
        self.extras["nat"] = g
        return self.show(scene, g, run_time=0.5)

    def namespace(self, scene):
        grp = VGroup(*[self.parts[k] for k in ("front", "api", "vdb", "svc_front", "svc_api", "svc_vdb",
                                                   "pvc1", "pvc2", "job") if k in self.parts])
        top = self.parts["nginx"].get_bottom()[1] - 0.07
        bot = grp.get_bottom()[1] - 0.1
        fr = DashedVMobject(RoundedRectangle(width=grp.width + 0.24, height=top - bot, corner_radius=0.12),
                            num_dashes=60, dashed_ratio=0.6).set_stroke(OWN, 3)
        fr.move_to([grp.get_center()[0], (top + bot) / 2, 0])
        t = label(NAMESPACE, 20, OWN).move_to(fr).align_to(fr, UL).shift(np.array([0.12, -0.04, 0]))
        g = VGroup(fr, t)
        self.extras["ns"] = g
        return self.show(scene, g, anims=[Create(fr), FadeIn(t)], run_time=0.7)

    def lb(self, scene):
        edge = self.extras["vpc"][0].get_left()[0] if "vpc" in self.extras else self._c(-3.3, 0)[0]
        lb_ = VGroup(boxed("load balancer", CLOUD, box_w=2.0, box_h=0.6, k=0.25))
        lb_.move_to([edge - 1.05, self.parts["nginx"].get_center()[1], 0])
        a = route(lb_.get_right(), self.parts["nginx"].get_left())
        g = VGroup(lb_, a)
        keep_inside(g)
        self.extras["lb"] = g
        return self.show(scene, g, run_time=0.5)

    def chip(self, scene, key: str, text: str):
        """PLAYS: a GREY scene chip ('Ingress → S13': split at ' → ' into two rows) in a column right
        of the VPC (x from 4.05, from y 2.0 down, 0.95 apart; call after slide_center()), joined to part
        `key` ('wi', 'ingress', 'pvc1', 'job', …) by a thin GREY line."""
        n = len([k for k in self.extras if k.startswith("chip_")])
        if " → " in text:
            a, b = text.split(" → ", 1)
            c = two_row_chip(a, "→ " + b, S.GREY)
        else:
            c = scene_chip(text)
        c.move_to(np.array([4.05 + c.width / 2, 2.0 - n * 0.95, 0]))
        keep_inside(c)
        tgt = self.parts[key]
        ln = Line(c.get_left(), tgt.get_right(), color=S.GREY, stroke_width=1.5)
        g = VGroup(ln, c)
        self.extras[f"chip_{key}"] = g
        return self.show(scene, g, anims=[Create(ln), FadeIn(c)], run_time=0.5)


# ------------------------------------------------------------------ StackPipe (S10, S11)
class StackPipe(_Anchored):
    """The two Pulumi stacks and the StackReference between them (S10's 'V5 mini', S11's bucket).
    Built at ORIGIN, x -6.2 .. 6.2, y -1.2 .. 2.6 (fits above a 3-row strip).
    S10  PLAYS images(scene) three TEAL image crates (x -4.9) · to_registry(scene) they move into a BLUE
         'Artifact Registry' box (x -2.95 .. -0.25) and three PINK '-tags' chips appear right of it ·
         pipe(scene) the tags merge into one PINK pipe to a GREEN 'deploy_k8s' box (x 4.05 .. 6.25),
         labelled 'StackReference organization/deploy-images/dev' under the tags (y ~ -0.1).
    S11  PLAYS bucket(scene) a BLUE state bucket holding 'deploy_images' (with an empty GREY outputs
         box, 'init + preview only, no up') and 'deploy_k8s' · break_pipe(scene) the pipe reaches the
         empty box and breaks RED · fill_outputs(scene) a 'pulumi up' stamp fills the box with three
         tags · join(scene) the pipe joins GREEN, caption 'same bucket · up finished'."""

    NAMES = ("api-service", "frontend", "vector-db")

    def __init__(self, **kw):
        super().__init__(**kw)
        self.crates = VGroup()
        self.tags_ = VGroup()

    def images(self, scene):
        cr = VGroup(*[crate(n, 2.1, 0.55) for n in self.NAMES]).arrange(DOWN, buff=0.18).move_to(self.p(-4.9, 0.8))
        self.crates = cr
        return self.show(scene, cr, run_time=0.6)

    def to_registry(self, scene):
        reg = boxed("Artifact Registry", CLOUD, box_w=2.7, box_h=2.1, k=0.12).move_to(self.p(-1.6, 0.8))
        reg.text.align_to(reg.frame, UP).shift(DOWN * 0.12)
        self.reg = reg
        self.show(scene, reg, run_time=0.4)
        small = [crate(n, 2.3, 0.42, size=20) for n in self.NAMES]
        VGroup(*small).arrange(DOWN, buff=0.08).move_to(reg.frame).shift(DOWN * 0.2)
        self._ensure(scene)
        scene.play(LaggedStart(*[Transform(c, s_) for c, s_ in zip(self.crates, small)], lag_ratio=0.3),
                   run_time=1.0)
        self.heal(scene)
        tg = VGroup(*[route_chip(f"{n}-tags", size=20) for n in ("api", "frontend", "vector-db")])
        tg.arrange(DOWN, buff=0.12, aligned_edge=LEFT).next_to(reg, RIGHT, buff=0.3)
        self.tags_ = tg
        self.show(scene, *tg, run_time=0.5)

    def pipe(self, scene):
        k8s = boxed("deploy_k8s", OWN, box_w=2.2, box_h=0.8, mono_font=True).move_to(self.p(5.15, 0.8))
        self.k8s = k8s
        self.show(scene, k8s, run_time=0.4)
        start = self.tags_.get_right() + RIGHT * 0.25
        ln = Line(start, k8s.get_left(), color=ROUTE, stroke_width=8)
        t = VGroup(label("StackReference", 20, ROUTE), mono(STACK_REF, 20, ROUTE)).arrange(RIGHT, buff=0.2)
        t.next_to(self.tags_, DOWN, buff=0.25).set_x(self.p(2.9, 0)[0])
        keep_inside(t)
        self.pipe_g = VGroup(ln, t)
        merges = [Line(c.get_right(), start, color=ROUTE, stroke_width=3) for c in self.tags_]
        self.show(scene, *merges, ln, t, anims=[*[Create(m) for m in merges], Create(ln), FadeIn(t)], run_time=0.8)

    # ---- S11
    def bucket(self, scene):
        b = frame_box(11.8, 3.5, CLOUD, k=0.06).move_to(self.p(0, 0.85))
        bt = label("state bucket (gs://…)", 20, CLOUD).move_to(b).align_to(b, UL).shift(np.array([0.18, -0.08, 0]))
        di = boxed("deploy_images", OWN, box_w=2.8, box_h=0.7, mono_font=True).move_to(self.p(-3.9, 1.85))
        out = frame_box(3.6, 1.3, S.GREY, k=0.06, dashed=True).move_to(self.p(-3.9, 0.65))
        ot = label("outputs: empty", 20, S.GREY).move_to(out).align_to(out, UP).shift(DOWN * 0.1)
        on = label("init + preview only, no up", 20, S.GREY).next_to(out, DOWN, buff=0.1)
        k8 = boxed("deploy_k8s", OWN, box_w=2.6, box_h=0.7, mono_font=True).move_to(self.p(4.1, 0.65))
        self.bk = VGroup(b, bt)
        self.di, self.out, self.k8 = di, VGroup(out, ot), k8
        self.out_note = on
        self.show(scene, self.bk, di, self.out, on, k8, run_time=0.8)

    def break_pipe(self, scene):
        a = self.k8.get_left()
        b = self.out.get_right()
        ln = DashedLine(a, b + RIGHT * 0.05, color=ROUTE, stroke_width=6)
        t = label("StackReference", 20, ROUTE).next_to(ln, UP, buff=0.1)
        self.ref_line = VGroup(ln, t)
        self.show(scene, self.ref_line, anims=[Create(ln), FadeIn(t)], run_time=0.7)
        x = cross_glyph(0.36).move_to(b + RIGHT * 0.6)
        self.brk = x
        self._ensure(scene)
        scene.play(ln.animate.set_color(ERR), run_time=0.3)
        self.show(scene, x, run_time=0.3)

    def fill_outputs(self, scene):
        st = boxed("pulumi up", TURN, size=22, k=0.2).rotate(0.15).move_to(self.out[0].get_center() + UP * 0.15)
        self.show(scene, st, anims=[FadeIn(st, scale=1.6)], run_time=0.4)
        rows = VGroup(*[mono(f"{n}-tags", 20, OWN) for n in ("api", "frontend", "vector-db")]).arrange(
            DOWN, buff=0.06, aligned_edge=LEFT).move_to(self.out[0]).shift(DOWN * 0.12)
        self.drop(scene, st, self.out[1], run_time=0.3)
        self.out_rows = rows
        self.show(scene, rows, run_time=0.5)

    def join(self, scene):
        ln = self.ref_line[0]
        self.drop(scene, self.brk, run_time=0.2)
        solid = Line(ln.get_start(), ln.get_end(), color=OWN, stroke_width=6)
        self.swap(scene, ln, solid, run_time=0.5)
        cap = label("same bucket · up finished", 22, OWN).next_to(self.bk[0], DOWN, buff=0.1)
        keep_inside(cap)
        self.cap = cap
        self.show(scene, cap, run_time=0.4)


# ------------------------------------------------------------------ V6 · ResourceTree
class ResourceTree(_Anchored):
    """V6 · the plan grows in dependency order (S11 plan, S12 fill, S16 empty). Built at ORIGIN in
    x -6.3 .. 6.3, y -1.25 .. 2.75 (above a 3-row strip). Seven group boxes (2.6 x 0.66, 22 pt
    'network ×4' …, coloured by provider: BLUE gcp, PURPLE provider, GREEN kubernetes):
        row A (y 2.15): network → cluster + pool → provider → ingress
        row B (y 0.75): '+1 · the stack itself' chip | identity → storage → app (provider ↘ identity)
        bottom (y -0.45): the counter '+ n to create' (left) and the two PINK dashed reads.
    Keys: 'network' 'cluster' 'provider' 'identity' 'storage' 'app' 'ingress' (TREE_GROUPS).
    PLAYS group(scene, key) one group box appears (with its arrow in) · grow(scene, lag) all of them in
        order + the stack chip · expand(scene, key) an opaque card listing the group's members (mono 20,
        a tick box each) opens over the tree · collapse(scene) · counter(scene, n=23) the YELLOW counter
        ('+ n to create'; call again to count on) · reads(scene) the two PINK dashed reads blink in ·
        fill_member(scene, key, name, color=None) a member's box fills (card must be open) ·
        fill(scene, key) the whole group fills solid (members too) · fail(scene, key, name) member and
        group turn RED · clock(scene) GOLD-ringed clock + '15–25 min · our estimate' on the cluster
        group · empty(scene, lag) every filled group unfills in reverse order · ghosts(scene) three
        ghost icons under the tree (forwarding rule, pvc-… disk, registry images with a padlock
        'retain_on_delete') — the counter and reads leave first.
    .groups{key} (.box .text .badge) .card (open card or None) .filled{key: set(names)}"""

    POS = {"network": (-4.9, 2.15), "cluster": (-1.65, 2.15), "provider": (1.6, 2.15), "ingress": (4.85, 2.15),
           "identity": (-1.65, 0.75), "storage": (1.6, 0.75), "app": (4.85, 0.75)}
    EDGES = (("network", "cluster"), ("cluster", "provider"), ("provider", "ingress"), ("provider", "identity"),
             ("identity", "storage"), ("storage", "app"))

    def __init__(self, **kw):
        super().__init__(**kw)
        self.groups: dict = {}
        self.spec = {g[0]: g for g in TREE_GROUPS}
        self.filled = {g[0]: set() for g in TREE_GROUPS}
        self.card = None
        self.card_key = None
        self.count_mob = None
        self.reads_g = None
        self.arrows: dict = {}

    def _group_mob(self, key, state="empty"):
        _, title, col, members = self.spec[key]
        k = {"empty": 0.06, "full": 0.45, "fail": 0.3}[state]
        edge_col = ERR if state == "fail" else col
        fr = frame_box(2.6, 0.66, edge_col, k=k)
        t = label(f"{title} ×{len(members)}", 22, INK).move_to(fr)
        g = VGroup(fr, t)
        g.box, g.text = fr, t
        g.move_to(self.p(*self.POS[key]))
        return g

    def group(self, scene, key: str, run_time: float = 0.5):
        g = self._group_mob(key)
        self.groups[key] = g
        mobs, anims = [g], [FadeIn(g, shift=RIGHT * 0.15)]
        for a, b in self.EDGES:
            if b == key and a in self.groups:
                ar = arrow(self.groups[a].box.get_center(), g.box.get_center(), S.GREY, stroke=3, buff=0)
                ar.put_start_and_end_on(self._edge_pt(self.groups[a], g), self._edge_pt(g, self.groups[a]))
                self.arrows[(a, b)] = ar
                mobs.insert(0, ar)
                anims.insert(0, GrowArrow(ar))
        return self.show(scene, *mobs, anims=anims, run_time=run_time)

    @staticmethod
    def _edge_pt(g, other):
        c, o = g.box.get_center(), other.box.get_center()
        if abs(c[1] - o[1]) < 0.1:
            return np.array([g.box.get_right()[0] if o[0] > c[0] else g.box.get_left()[0], c[1], 0])
        return np.array([c[0] + (0.0 if abs(c[0] - o[0]) < 0.1 else (0.5 if o[0] > c[0] else -0.5)),
                         g.box.get_bottom()[1] if o[1] < c[1] else g.box.get_top()[1], 0])

    def grow(self, scene, lag: float = 0.35):
        for key in ("network", "cluster", "provider", "identity", "storage", "app", "ingress"):
            if key not in self.groups:
                self.group(scene, key, run_time=lag)
        st = chip("+1 · the stack itself", S.GREY, size=20).move_to(self.p(-4.9, 0.75))
        self.stack_chip = st
        self.show(scene, st, run_time=lag)

    def _card(self, key):
        _, title, col, members = self.spec[key]
        rows = VGroup()
        for m in members:
            done = m in self.filled[key]
            bx = Square(side_length=0.26, stroke_color=col, stroke_width=2.5).set_fill(col, 0.85 if done else 0)
            t = mono(m, 20, INK)
            r = VGroup(bx, t).arrange(RIGHT, buff=0.16)
            r.box, r.text, r.member = bx, t, m
            rows.add(r)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        hd = label(title, 20, col)
        inner = VGroup(hd, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        fr = RoundedRectangle(width=max(inner.width + 0.5, 2.6), height=inner.height + 0.4, corner_radius=0.12,
                              stroke_color=col, stroke_width=3).set_fill(S.GREY_DARKER, 1)
        inner.move_to(fr)
        c = VGroup(fr, inner)
        c.rows = rows
        g = self.groups[key]
        c.next_to(g.box, DOWN, buff=0.08).align_to(g.box, LEFT)
        top_lim, bot_lim = self.p(0, 2.75)[1], self.p(0, -1.25)[1]
        if c.get_bottom()[1] < bot_lim:
            c.shift(UP * (bot_lim - c.get_bottom()[1]))
        if c.get_top()[1] > top_lim:
            c.shift(DOWN * (c.get_top()[1] - top_lim))
        keep_inside(c)
        return c

    def expand(self, scene, key: str, run_time: float = 0.5):
        if self.card is not None:
            self.collapse(scene)
        c = self._card(key)
        self.card, self.card_key = c, key
        return self.show(scene, c, anims=[FadeIn(c, scale=0.9)], run_time=run_time)

    def collapse(self, scene, run_time: float = 0.3):
        if self.card is not None:
            self.drop(scene, self.card, run_time=run_time)
            self.card = self.card_key = None

    def counter(self, scene, n: int = 23):
        t = steady(f"+ {n} to create", 24, TURN).move_to(self.p(-4.9, -0.45))
        if self.count_mob is None:
            self.count_mob = t
            return self.show(scene, t, run_time=0.4)
        self._ensure(scene)
        scene.play(Transform(self.count_mob, t), run_time=0.3)
        self.heal(scene)
        return self.count_mob

    def reads(self, scene):
        a = dashed_chip("StackReference · deploy-images/dev", ROUTE).move_to(self.p(-1.0, -0.45))
        b = dashed_chip("nginx-ingress-service", ROUTE, mono_font=True).move_to(self.p(3.7, -0.45))
        hd = label("reads", 20, ROUTE).next_to(a, LEFT, buff=0.15)
        if hd.get_left()[0] < (self.count_mob.get_right()[0] + 0.1 if self.count_mob is not None else -9):
            hd = VGroup()
        self.reads_g = VGroup(hd, a, b)
        self.show(scene, self.reads_g, run_time=0.4)
        scene.play(Indicate(a, color=ROUTE, scale_factor=1.06), Indicate(b, color=ROUTE, scale_factor=1.06),
                   run_time=0.6)
        self.heal(scene)

    def fill_member(self, scene, key: str, name: str, color=None, run_time: float = 0.35):
        col = color or self.spec[key][2]
        self.filled[key].add(name)
        if self.card is None or self.card_key != key:
            return
        r = next(r for r in self.card.rows if r.member == name)
        self._ensure(scene)
        scene.play(r.box.animate.set_fill(col, 0.85).set_stroke(col), r.text.animate.set_color(col), run_time=run_time)
        self.heal(scene)

    def _restyle(self, scene, key, state, run_time=0.4):
        old = self.groups[key]
        new = self._group_mob(key, state)
        self.groups[key] = self.swap(scene, old, new, run_time=run_time)

    def fill(self, scene, key: str, run_time: float = 0.4):
        self.filled[key] = set(self.spec[key][3])
        self._restyle(scene, key, "full", run_time)

    def fail(self, scene, key: str, name: str):
        if self.card is not None and self.card_key == key:
            r = next(r for r in self.card.rows if r.member == name)
            self._ensure(scene)
            scene.play(r.box.animate.set_fill(ERR, 0.85).set_stroke(ERR), r.text.animate.set_color(ERR), run_time=0.4)
            self.heal(scene)
        self._restyle(scene, key, "fail")

    def clock(self, scene):
        g = self.groups["cluster"]
        c = clock_face(0.2, COST, hour=4).move_to(g.box.get_corner(UR) + np.array([-0.05, 0.0, 0]))
        rg = Circle(radius=0.27, stroke_color=COST, stroke_width=3).move_to(c)
        t = label("15–25 min · our estimate", 20, COST).next_to(g.box, DOWN, buff=0.08)
        self.clock_g = VGroup(rg, c, t)
        self.show(scene, self.clock_g, run_time=0.5)
        scene.play(Rotate(c.hands[1], -TAU, about_point=c[0].get_center()), run_time=1.0)
        self.heal(scene)

    def empty(self, scene, lag: float = 0.3):
        if self.card is not None:
            self.collapse(scene)
        for key in ("ingress", "app", "storage", "identity", "provider", "cluster", "network"):
            if key in self.groups:
                self.filled[key] = set()
                self._restyle(scene, key, "empty", lag)

    def ghosts(self, scene):
        gone = [m for m in (self.count_mob, self.reads_g, getattr(self, "clock_g", None)) if m is not None]
        if gone:
            self.drop(scene, *gone, run_time=0.3)
            self.count_mob = self.reads_g = None
        fwd = VGroup(arrow(np.array([-0.35, 0, 0]), np.array([0.35, 0, 0]), CLOUD, stroke=3, buff=0),
                     label("forwarding rule", 20, CLOUD)).arrange(RIGHT, buff=0.12)
        dk = VGroup(disk_cyl(0.42), mono("pvc-…", 20, CLOUD)).arrange(RIGHT, buff=0.12)
        imgs = VGroup(crate("registry images", 2.3, 0.5), padlock(0.4, COST, "retain_on_delete")).arrange(RIGHT, buff=0.15)
        row = VGroup(fwd, dk, imgs).arrange(RIGHT, buff=0.6).move_to(self.p(0, -0.5))
        for m in (fwd, dk):
            m.set_opacity(0.85)
        self.ghost_g = row
        self.show(scene, row, run_time=0.5)
        scene.play(*[Indicate(m, color=COST, scale_factor=1.06) for m in row], run_time=0.8)
        self.heal(scene)


# ------------------------------------------------------------------ V7 · RequestJourney
class RequestJourney(_Anchored):
    """V7 · one click, every hop (README:457-474 redrawn as lanes; S13). Built at ORIGIN in
    x -6.35 .. 6.35, y -3.15 .. 0.95 (+ the routing card above nginx up to y 2.4, packets' labels up to
    y 1.6): the top-right corner stays free for the small AsksChecklist.
        browser (GREY, x -5.6) → 'LoadBalancer' / 'Service' (BLUE, x -3.6) → 'nginx Ingress' /
        'Controller' (TEAL, x -1.3) → 'frontend' / 'ClusterIP 3000' (PINK, x 1.6, y 0.35, path '/') and
        'api' / 'ClusterIP 9000' (PINK, x 1.6, y -1.45, path '/api-service') → 'vector-db' /
        'ClusterIP 8000' (PINK, x 4.85, y -1.45); GREEN 'vector-db-loader' Job (x 4.85, y -2.75).
    Hop keys: 'browser' 'lb' 'nginx' 'front' 'api' 'vdb' 'job'.
    PLAYS build(scene, lag=0.3) the lanes left to right · loader_arrow(scene) the README's dotted
        arrow (GREY ghost, vdb → job, erratum tag) flips into a GREEN dotted job → vdb 'one-time load' ·
        send(scene, text, hops, color=ROUTE, keep=True) a PINK bubble with `text` rides hop to hop
        (returns it; keep=False fades it at the end) · dns(scene) a PINK bubble '<IP>.sslip.io → <IP>'
        beside the browser · routing_card(scene) above nginx: PINK 'host: <IP>.sslip.io' and the two
        rules · reject(scene, packet) the card's host flashes RED, the packet is replaced by a RED
        '404' bubble that goes back to the browser (returns the new bubble; drop that one) · reply(scene, at, text) a bubble from hop `at` back to the browser
        · page_spawn(scene) a GREY page returns to the browser and a new packet '/api-service/…'
        leaves the browser itself · scissors_crossed(scene, at='api') L20's scissors, crossed out, under the api box ·
        drop_packet(scene, packet). Path labels: '/' left of the nginx → frontend arrow,
    '/api-service' left of the api box, below the arrow.
    .hops{key} (each .frame .text) .card .paths"""

    LAYOUT = {"browser": (-5.6, -0.55, 1.4, ["Browser"], LAPTOP),
              "lb": (-3.55, -0.55, 2.0, ["LoadBalancer", "Service"], CLOUD),
              "nginx": (-1.25, -0.55, 2.0, ["nginx Ingress", "Controller"], CONTAINER),
              "front": (1.65, 0.35, 2.25, ["frontend", "ClusterIP 3000"], ROUTE),
              "api": (1.65, -1.45, 2.25, ["api", "ClusterIP 9000"], ROUTE),
              "vdb": (4.85, -1.45, 2.4, ["vector-db", "ClusterIP 8000"], ROUTE),
              "job": (4.85, -2.75, 2.6, ["vector-db-loader", "Job"], OWN)}

    def __init__(self, **kw):
        super().__init__(**kw)
        self.hops: dict = {}
        self.paths: dict = {}
        self.card = None

    def _hop(self, key):
        x, y, w, rows, col = self.LAYOUT[key]
        g = boxed(rows, col, box_w=w, box_h=0.8 if len(rows) == 2 else 0.6, k=0.16)
        return g.move_to(self.p(x, y))

    def _pt(self, key):
        return self.hops[key].get_center()

    def build(self, scene, lag: float = 0.3):
        order = ["browser", "lb", "nginx", "front", "api", "vdb", "job"]
        links = [("browser", "lb", None), ("lb", "nginx", None), ("nginx", "front", "/"),
                 ("nginx", "api", "/api-service"), ("api", "vdb", None)]
        for k in order:
            self.hops[k] = self._hop(k)
        for a, b, path in links:
            ar = route(self.hops[a].get_right(), self.hops[b].get_left(), stroke=3)
            g = VGroup(ar)
            if path:
                t = mono(path, 20, ROUTE)
                if b == "front":
                    t.next_to(ar.get_center(), LEFT, buff=0.12).shift(UP * 0.12)
                else:
                    t.next_to(self.hops[b], LEFT, buff=0.12).shift(DOWN * 0.3)
                g.add(t)
            self.paths[(a, b)] = g
        for k in order:
            mobs = [self.hops[k]] + [g for (a, b), g in self.paths.items() if b == k]
            self.show(scene, *mobs, run_time=lag)

    def loader_arrow(self, scene):
        v, j = self.hops["vdb"], self.hops["job"]
        ghost = DashedLine(v.get_bottom(), j.get_top(), color=S.GREY, stroke_width=3, dash_length=0.08)
        ghost.add_tip(tip_length=0.16, tip_width=0.16)
        et = erratum_tag().next_to(ghost, RIGHT, buff=0.15)
        self.show(scene, ghost, et, run_time=0.5)
        good = DashedLine(j.get_top(), v.get_bottom(), color=OWN, stroke_width=3, dash_length=0.08)
        good.add_tip(tip_length=0.16, tip_width=0.16)
        self.loader = self.swap(scene, ghost, good, run_time=0.7)
        t = label("one-time load", 20, OWN).next_to(good, LEFT, buff=0.15)
        self.drop(scene, et, run_time=0.2)
        self.loader_t = t
        self.show(scene, t, run_time=0.3)

    def _bubble(self, text, color=ROUTE):
        t = mono(text, 20, INK)
        b = RoundedRectangle(width=t.width + 0.3, height=t.height + 0.2, corner_radius=0.12,
                             stroke_color=color, stroke_width=2.5).set_fill(tint(color, 0.25), 1)
        t.move_to(b)
        g = VGroup(b, t)
        g.box, g.text = b, t
        return g

    def send(self, scene, text: str, hops, color=ROUTE, keep: bool = True, per: float = 0.45):
        pk = self._bubble(text, color)
        pk.next_to(self.hops[hops[0]], UP, buff=0.12)
        keep_inside(pk)
        scene.play(FadeIn(pk, shift=DOWN * 0.1), run_time=0.3)
        for k in hops[1:]:
            scene.play(pk.animate.move_to(self._above(k, pk)), run_time=per)
        if not keep:
            scene.play(FadeOut(pk), run_time=0.25)
            scene.remove(pk)
        self.heal(scene)
        return pk

    def _above(self, key, pk):
        """Where a packet sits above hop `key` (kept inside the safe frame)."""
        ghost = pk.copy().move_to(self.hops[key].get_top() + UP * (pk.height / 2 + 0.12))
        return keep_inside(ghost).get_center()

    def drop_packet(self, scene, packet):
        scene.play(FadeOut(packet), run_time=0.25)
        scene.remove(packet)

    def dns(self, scene):
        b = self._bubble(f"{HOST_PH} → {IP_PH}")
        b.next_to(self.hops["browser"], DOWN, buff=0.25).align_to(self.hops["browser"], LEFT)
        keep_inside(b)
        self.dns_b = b
        return self.show(scene, b, run_time=0.4)

    def routing_card(self, scene):
        hd = mono(f"host: {HOST_PH}", 20, ROUTE)
        r1 = VGroup(mono("/api-service", 20, TURN), label("→", 20, S.GREY), mono("api:9000", 20, INK)).arrange(RIGHT, buff=0.12)
        r2 = VGroup(mono("/", 20, TURN), label("→", 20, S.GREY), mono("frontend:3000", 20, INK)).arrange(RIGHT, buff=0.12)
        inner = VGroup(hd, r1, r2).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        fr = RoundedRectangle(width=inner.width + 0.45, height=inner.height + 0.35, corner_radius=0.12,
                              stroke_color=ROUTE, stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
        inner.move_to(fr)
        c = VGroup(fr, inner)
        c.next_to(self.hops["nginx"], UP, buff=0.75)
        keep_inside(c)
        c.head, c.rules = hd, VGroup(r1, r2)
        self.card = c
        return self.show(scene, c, run_time=0.6)

    def reject(self, scene, packet):
        self._ensure(scene)
        if self.card is not None:
            scene.play(Indicate(self.card.head, color=ERR, scale_factor=1.1), run_time=0.6)
        nw = self._bubble("404", ERR).move_to(packet)
        scene.play(FadeOut(packet), FadeIn(nw), run_time=0.3)
        scene.remove(packet)
        scene.play(nw.animate.move_to(self._above("browser", nw)), run_time=0.8)
        self.heal(scene)
        return nw

    def reply(self, scene, at: str, text: str):
        pk = self._bubble(text)
        pk.next_to(self.hops[at], UP, buff=0.12)
        keep_inside(pk)
        scene.play(FadeIn(pk), run_time=0.3)
        scene.play(pk.animate.move_to(self._above("browser", pk)), run_time=0.9)
        self.heal(scene)
        return pk

    def page_spawn(self, scene):
        pg = file_glyph(0.4, S.GREY).next_to(self.hops["nginx"], UP, buff=0.2)
        scene.play(FadeIn(pg), run_time=0.2)
        scene.play(pg.animate.next_to(self.hops["browser"], UP, buff=0.15), run_time=0.7)
        pk = self.send(scene, "/api-service/…", ["browser", "lb", "nginx", "api"], keep=True)
        scene.play(FadeOut(pg), run_time=0.2)
        scene.remove(pg)
        return pk

    def scissors_crossed(self, scene, at: str = "api"):
        sc = scissors(0.5, PAST).next_to(self.hops[at], DOWN, buff=0.2)
        x = cross_glyph(0.45).move_to(sc)
        self.sc = VGroup(sc, x)
        self.show(scene, sc, run_time=0.3)
        self.show(scene, x, anims=[Create(x)], run_time=0.3)


class DoorsStrip(_Anchored):
    """S13's comparison strip: three GREY panels (4.0 x 2.5), built at ORIGIN x -6.3 .. 6.3,
    y -1.25 .. 1.25: 'L20 · one nginx container in front' (GREY dashed, a VM with an nginx box),
    'tic-tac-toe · one LoadBalancer per app' (two apps, a BLUE door each), 'cheese app · one door
    with a receptionist' (one BLUE door, an nginx figure, three PINK paths). PLAYS build(scene, lag).
    .panels[i]"""

    def __init__(self, **kw):
        super().__init__(**kw)
        self.panels = VGroup()

    def _panel(self, i):
        x = -4.2 + 4.2 * i
        dashed = i == 0
        fr = frame_box(4.0, 2.5, PAST if dashed else S.GREY, k=0.05, dashed=dashed).move_to(self.p(x, 0))
        titles = (("L20 · one nginx", "container in front"), ("tic-tac-toe · one", "LoadBalancer per app"),
                  ("cheese app · one door", "with a receptionist"))[i]
        t = VGroup(*[label(s, 20, INK if not dashed else PAST) for s in titles]).arrange(DOWN, buff=0.04)
        t.move_to(fr).align_to(fr, UP).shift(DOWN * 0.12)
        g = VGroup(fr, t)
        c = self.p(x, -0.45)
        if i == 0:
            vm = frame_box(2.6, 1.1, PAST, k=0.05, dashed=True).move_to(c)
            ng = boxed("nginx", CONTAINER, box_w=1.2, box_h=0.45, mono_font=True).move_to(vm.get_top() + DOWN * 0.35)
            g.add(vm, ng)
        elif i == 1:
            for dx in (-0.85, 0.85):
                app = image_block(None, 1.2, 0.55).move_to(c + np.array([dx, -0.2, 0]))
                d = RoundedRectangle(width=0.5, height=0.3, corner_radius=0.06, stroke_color=CLOUD,
                                     stroke_width=3).set_fill(tint(CLOUD, 0.3), 1).next_to(app, UP, buff=0.08)
                g.add(app, d)
        else:
            d = RoundedRectangle(width=0.6, height=0.32, corner_radius=0.06, stroke_color=CLOUD,
                                 stroke_width=3).set_fill(tint(CLOUD, 0.3), 1).move_to(c + np.array([-1.4, 0, 0]))
            fig = person_icon(CONTAINER, 0.5).move_to(c + np.array([-0.55, 0, 0]))
            tips = [c + np.array([1.2, y, 0]) for y in (0.45, 0.0, -0.45)]
            paths = VGroup(*[route(fig.get_right(), tp, stroke=3) for tp in tips])
            g.add(d, fig, paths)
        return g

    def build(self, scene, lag: float = 0.5):
        for i in range(3):
            p_ = self._panel(i)
            self.show(scene, p_, run_time=lag, into=self.panels)
        if self.panels not in self.submobjects:
            self.add(self.panels)


# ------------------------------------------------------------------ V8 · BinPacking
class BinPacking(_Anchored):
    """V8 · two levels of scaling (S15; slides 12, 15, 18, 39, 43). Built at ORIGIN in x -6.3 .. 3.1
    (levers to 6.4), y -2.65 .. 2.6. Node shelves are BLUE rectangles 7.3 x 1.0 (x -6.3 .. 1.0):
    node 1 at y 0.65 .. 1.65 with its caption above ('node 1 · allocatable: less than its 8 GB'),
    node 2 at y -2.2 .. -1.2 (caption at y -0.95). Blocks are sized by their requests (labels inside,
    20 pt): frontend 1.6 wide (fat), vector-db 1.3, nginx 0.95, api 1.15 dashed 'api ?' (no request).
    A block that does not fit hovers RED 'Pending' right of node 1's shelf (x 1.3 .. 3.0).
    PLAYS node(scene, i=0) a shelf (i=1 slides in from the right, a GREY chip 'cluster autoscaler
        · max 2' under it) · fill(scene) node 1's first four blocks · add_block(scene, key='frontend', node=None)
        a new block drops: onto `node` (or the first with room); none has room → it hovers 'Pending'
        (returns it) · land(scene, block, node) a hovering block moves into node · disk(scene) a BLUE
        disk 'persistent-pvc' chained to node 1 under the api block, the PINK chip 'ReadWriteOnce · one
        node at a time' under the disk · multi_attach(scene) a second api block on node 2 reaches for the disk; the
        RED chain snaps 'Multi-Attach', the block stays 'ContainerCreating' · ghost_node(scene) a third
        GREY-dashed node (x 1.25 .. 3.65, y -2.2 .. -1.2) crossed RED 'more nodes don't help' ·
        levers(scene) two labelled levers on the right (x 3.4 .. 6.4, y -0.6 .. 1.5): 'Pods' (you: kubectl scale; dashed 'HPA: not configured · needs
        requests') and 'nodes' (GKE autoscaler · 1–2: on) · legend(scene) a card of REQUESTS.
    .nodes[i] .blocks[i] (list per node) .pending (list)"""

    SIZES = {"frontend": 1.6, "vector-db": 1.3, "nginx": 0.95, "api": 1.15}
    SHELF_W = 7.3

    def __init__(self, **kw):
        super().__init__(**kw)
        self.nodes, self.blocks, self.pending = [], [], []
        self.cursor = []

    def _node_y(self, i):
        return (1.15, -1.7)[i]

    def node(self, scene, i: int = 0):
        y = self._node_y(i)
        fr = frame_box(self.SHELF_W, 1.0, CLOUD, k=0.08).move_to(self.p(-2.65, y))
        cap = label(f"node {i + 1}" + (" · allocatable: less than its 8 GB" if i == 0 else ""), 20, CLOUD)
        cap.next_to(fr, UP, buff=0.08).align_to(fr, LEFT)
        g = VGroup(fr, cap)
        g.frame = fr
        self.nodes.append(g)
        self.blocks.append([])
        self.cursor.append(fr.get_left()[0] + 0.1)
        if i == 0:
            self.show(scene, g, run_time=0.5)
            self.remove(g)
            self.add_to_back(g)
            return g
        start = g.copy().shift(RIGHT * 6)
        ch = grey_chip("cluster autoscaler · max 2").next_to(fr, DOWN, buff=0.1).align_to(fr, LEFT)
        keep_inside(ch)
        self.autoscaler_chip = ch
        scene.add(start)
        scene.play(ReplacementTransform(start, g), run_time=0.8)
        scene.remove(start, g)
        self.add_to_back(g)                      # blocks that land on it stay in front
        self.heal(scene)
        self.show(scene, ch, run_time=0.3)
        return g

    def _block(self, key):
        w = self.SIZES[key]
        dashed = key == "api"
        g = boxed("api ?" if dashed else key, CONTAINER, box_w=w, box_h=0.7, dashed=dashed, k=0.2)
        g.key = key
        return g

    def _fits(self, i, key):
        fr = self.nodes[i].frame
        return self.cursor[i] + self.SIZES[key] <= fr.get_right()[0] - 0.08

    def _slot(self, i, key):
        fr = self.nodes[i].frame
        x = self.cursor[i] + self.SIZES[key] / 2
        self.cursor[i] += self.SIZES[key] + 0.08
        return np.array([x, fr.get_bottom()[1] + 0.45, 0])

    def fill(self, scene):
        for key in ("frontend", "vector-db", "nginx", "api"):
            self.add_block(scene, key, 0, run_time=0.35)

    def add_block(self, scene, key: str = "frontend", node: int | None = None, run_time: float = 0.6):
        """PLAYS: the block drops in (see class doc). Returns it."""
        b = self._block(key)
        cands = [node] if node is not None else list(range(len(self.nodes)))
        dest = next((i for i in cands if self._fits(i, key)), None)
        if dest is None:
            fr0 = self.nodes[0].frame
            tgt = np.array([fr0.get_right()[0] + 0.3 + b.width / 2, fr0.get_center()[1] + 0.25 + 0.0 * len(self.pending), 0])
            if self.pending:
                tgt = tgt + DOWN * 0.95 * len(self.pending)
            b.move_to(tgt + UP * 1.2)
            st = pod_status("Pending").next_to(tgt, DOWN, buff=0.4)
            st.set_y(tgt[1] - 0.55)
            self._ensure(scene)
            scene.add(b)
            scene.play(b.animate.move_to(tgt), run_time=run_time)
            scene.play(b.frame.edge.animate.set_stroke(ERR), FadeIn(st), run_time=0.3)
            scene.remove(b, st)
            b.add(st)
            b.pend = st
            self.add(b)
            self.pending.append(b)
            self.heal(scene)
            return b
        tgt = self._slot(dest, key)
        b.move_to(tgt)
        scene.play(FadeIn(b, shift=DOWN * 1.2), run_time=run_time)
        scene.remove(b)
        b.node = dest
        self.blocks[dest].append(b)
        self.add(b)
        self.heal(scene)
        return b

    def land(self, scene, block, node: int):
        if not self._fits(node, block.key):
            raise ValueError("BinPacking.land: no room")
        tgt = self._slot(node, block.key)
        st = getattr(block, "pend", None)
        self._ensure(scene)
        anims = [block.animate.move_to(tgt + (np.array([0, (block.get_center() - block.frame.get_center())[1], 0])
                                              if st is not None else 0))]
        scene.play(*anims, run_time=0.7)
        if st is not None:
            block.remove(st)
            scene.remove(st)
            self.remove(st)
            scene.play(block.frame.edge.animate.set_stroke(CONTAINER), run_time=0.2)
            block.shift(tgt - block.frame.get_center())
        self.pending.remove(block)
        self.blocks[node].append(block)
        self.heal(scene)
        return block

    def disk(self, scene):
        api = next(b for b in self.blocks[0] if b.key == "api")
        d = disk_cyl(0.5).next_to(self.nodes[0].frame, DOWN, buff=0.25).set_x(api.get_center()[0])
        t = label("persistent-pvc", 20, CLOUD).next_to(d, RIGHT, buff=0.12)
        ch = Line(api.get_bottom(), d.get_top(), color=CLOUD, stroke_width=5)
        rw = route_chip("ReadWriteOnce · one node at a time", size=20, mono_font=False).next_to(d, DOWN, buff=0.12)
        rw.align_to(d, LEFT)
        keep_inside(rw)
        self.disk_g = VGroup(ch, d, t, rw)
        self.disk_g.cyl, self.disk_g.rwo = d, rw
        self.show(scene, self.disk_g, run_time=0.6)

    def multi_attach(self, scene):
        b = self._block("api")
        tgt = self._slot(1, "api")
        b.move_to(tgt)
        self.show(scene, b, anims=[FadeIn(b, shift=DOWN * 0.3)], run_time=0.4)
        self.blocks[1].append(b)
        ch = Line(b.get_top(), self.disk_g.cyl.get_bottom(), color=ERR, stroke_width=5)
        self.show(scene, ch, anims=[Create(ch)], run_time=0.5)
        x = cross_glyph(0.35).move_to(ch.get_center())
        t = label("Multi-Attach", 22, ERR).next_to(x, RIGHT, buff=0.15)
        st = pod_status("ContainerCreating").next_to(b, RIGHT, buff=0.15)
        self.snap = VGroup(ch, x, t, st)
        self.show(scene, x, t, st, run_time=0.4)
        self.drop(scene, ch, run_time=0.3)

    def ghost_node(self, scene):
        fr = frame_box(2.4, 1.0, PAST, k=0.03, dashed=True).move_to(self.p(2.45, -1.7))
        t = label("node 3", 20, PAST).move_to(fr)
        x = cross_glyph(0.5).move_to(fr)
        c = label("more nodes don't help", 20, ERR).next_to(fr, DOWN, buff=0.1)
        keep_inside(c)
        self.ghost = VGroup(fr, t, x, c)
        self.show(scene, fr, t, run_time=0.4)
        self.show(scene, x, c, anims=[Create(x), FadeIn(c)], run_time=0.4)

    def levers(self, scene):
        rows = VGroup()
        for name, lines, on in (("Pods", ["you: kubectl scale"], False), ("nodes", ["GKE autoscaler", "1–2: on"], True)):
            lv = lever_glyph(0.6, TURN if on else S.GREY, on=on)
            txt = VGroup(label(name, 22, INK), *[label(s, 20, S.GREY) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.04)
            r = VGroup(lv, txt).arrange(RIGHT, buff=0.2)
            rows.add(r)
        hpa = dashed_chip("HPA: not configured · needs requests")
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        g = VGroup(rows, hpa).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        g.move_to(self.p(4.9, 0.55))
        keep_inside(g)
        self.levers_g = g
        return self.show(scene, g, run_time=0.6)

    def legend(self, scene):
        rows = [VGroup(mono(k, 20, INK), label(v, 20, S.GREY)).arrange(RIGHT, buff=0.2) for k, v in REQUESTS.items()]
        c = card(rows, S.GREY, head="requests (cpu / memory)")
        c.move_to(self.p(4.9, -1.6))
        keep_inside(c)
        self.legend_g = c
        return self.show(scene, c, run_time=0.5)

