"""Shared scene code for AC215 L15 (ML workflows: deploy one model on SageMaker, then automate the
workflow with SageMaker Pipelines; follow-along of dlops-io/model-deployment-aws @ 077f4db and
dlops-io/ml-workflow-aws @ f165c6e).

Paths, narration (SAY lines straight from script.md), the semantic colours of BRIEF.md, the running
example (placeholders only), the eleven README trackers, loaders for the real captures in
assets/terminal/laptop (multi-line commands split off, container prompts masked), the RECORDED
quote of assets/terminal/expected, source panels from assets/source/<repo>, terminal helpers, tags,
chips, cards, small glyphs, the schematic AWS console form, the Vertex ↔ AWS bridge card, and the
video's set pieces V1-V8. Generic helpers come from L14's common.py (tested there); the set pieces
are new. build/common_test.py plays every helper and set piece once.

    from manim import *          # first
    from common import *         # second (common's names win), then:
    SAY = NARRATION["S07"]; assert len(SAY) == SAY_COUNT["S07"]   # one voiceover block per SAY

Notes for scene authors
=======================
Rules. Every text here is >= 20 pt: never .scale() a group that holds text below 1.0 (pieces take
size / width parameters instead; text-free glyphs exist for small copies). Never set width / height
/ color / depth on a VGroup subclass (Manim properties): these classes use box_w, plate_w, slot_list
… Methods marked PLAYS take the scene first, play their own animation and then keep the new
mobjects inside the piece, so a later FadeOut(piece) takes them all. Methods marked ANIM return an
animation you play. To take one part away use piece.drop(self, part) (Piece.drop: fades it and
takes it off the piece); never FadeOut a member of a piece directly (it snaps back when the piece is
next drawn). Pieces are built centred near ORIGIN in the layout noted below; place them (shift /
move_to / next_to) BEFORE their first PLAYS call, or between calls: every PLAYS method builds its
new parts at the piece's current position (piece.p(x, y) = layout point (x, y)).
Split trap: animating a group that is not itself on the scene (substring(), glyph_range(),
code_span(), a VGroup you just made of existing parts) makes Manim split every parent holding
those members into loose top-level pieces. Re-seat the parent right after with self.add(parent) (a
piece: piece.heal(self)), or animate the members one by one.
Lecture tags: lref("11–12") lives exactly as long as the picture it cites (FadeIn with it, FadeOut
with it; script.md LECTURE marks). Never carry one into the next beat.

Frame budget. Safe frame x in [-6.6, 6.6], y in [-3.6, 3.6]. Tracker top-left (left -6.5, top 3.5,
lowest point TRACK_BOTTOM 2.9); lecture tag top right; pictures stay below PIC_TOP 2.8. Terminals:
term() is 12.6 wide, bottom edge at BOTTOM -3.5; a 3-row strip's top is STRIP_TOP (-1.44), so a
picture over a strip lives in y in [-1.3, 2.8] (shift a piece up to fit, never scale it).

Data
    NARRATION["S01"] .. ["S16"]  SAY_COUNT  TITLES[cls]  SPEC (video.yaml)
    Names: BUCKET_A_PH 'your-models-bucket-placeholder' · ROLE_A_PH (placeholder ARN, account
    000000000000) · KEY_PH / SECRET_PH (laptop/55) · README_ACCOUNT '123456789012' (README A:43, AWS's
    documentation placeholder: README card only) · BUCKET_A 'cheese-app-models-demo' · BUCKET_B
    'cheese-app-ml-workflow-demo' · REGION · USER_A / USER_B · ROLE_A 'SageMakerExecutionRole' ·
    ROLE_SM / ROLE_LAMBDA · IMAGE_A · STEP_NAMES (the five pipeline steps) · STEP_VARS (cli.py:322) ·
    STAGE_TILES (slides 20-21) · LABELS (cli.py:41-42: 0 parmigiano … 3 gouda) · INSTANCE_A
    'ml.m5.xlarge' · ENDPOINT_B 'cheese-app-endpoint' · TARBALL · S3_URI_A · FLOATS 150528 ·
    BRIDGE_ROWS (the seven Vertex → AWS rows) · DLC_MASK '<aws-dlc-account>'.
    Prompts: P_HOME 'student@laptop:~$', P_MD '…:~/model-deployment-aws$', P_MW '…:~/ml-workflow-aws$',
    P_SRC(stage) '…:~/ml-workflow-aws/src/<stage>$' (stage in STAGES: data-collector,
    data-processor, model-training, workflow), P_APP '(app) app@<id>:/app$', P_ROOT
    'root@<id>:/app#'; terminal title T_LAPTOP 'laptop'.

Trackers (script.md conventions; placed top-left, 'README A › Setup Environments' …)
    tracker(key, step=None, extra=False) with key in TRACKER_KEYS 'A1'..'A4', 'B1'..'B7'; factories
    tracker_a1 … tracker_a4, tracker_b1 … tracker_b7 (step=None, extra=False). extra: False | True
    (' · extra') | one of EXTRA_KINDS 'check', 'capture stub', 'local stand-in, not SageMaker',
    'built offline, not sent' (' · extra · …') | any other str (appended after ' · ').
    track(tr, k, extra) ANIM (caption cross-fades; k=None keeps the step) · swap_tracker(scene, old,
    new) PLAYS (one section to the next; 'README A' stays, or cross-fades to 'README B') ·
    lref(slides) the GREY 'Lecture 15 · slides a–b' tag (top right).

Captures (assets/terminal/laptop/NN-*.txt; the only capture folder is laptop/)
    c = capture("27")  (or capture("laptop/27"))
    c.cmd_lines  the typed lines (line 1 without '$ '; 16, 53, 57, 80, 81 keep their own rows)
    c.cmd        the same joined with '\\n'     c.k  how many file lines the command takes
    c.at(*spec)  output lines by FILE line numbers (script.md's TERM numbers): ints, (a, b) ranges,
                 '…' items; refuses the command lines, the [exit N] line and container-prompt lines
    c.typed(n)   the text typed at a container prompt on file line n (istep files 25, 27-30, 60, 68,
                 73, 90): type_cmd(scene, t, c.typed(35)) with t's prompt P_APP / P_ROOT
    c.line(n)    one file line   c.pick(*ranges) L1-style, 1-based over the output body
    c.lines (output body) c.exit c.raw c.path. Container ids read '<id>', 763104351884 reads
    '<aws-dlc-account>' everywhere (unname()).
    Line tools: cut(s, after) ('to "…"') / cut(s, n=65) ('cut') · from_phrase(s, phrase) ('from "…"')
    · soft(lines, n) ('wrap') · unbox(s) (rich-traceback borders off: '│ ❱  73 │ … │' -> '❱  73 │ …').
    type_capture(scene, t, c, type_time=None) PLAYS: types c's command lines exactly as captured
        (a row after a trailing '\\' continues without a prompt; separate commands get the prompt).
    recorded(*nums) -> lines of expected/md-predict-readme.txt by FILE line (7-10 = the brie answer;
        lines 1-4 refused) · recorded_card(nums, source='README A:137–147') mono card + tag.

Sources (assets/source/<repo> at the pinned commits; header '<repo-relative path> · lines a–b')
    Paths start with 'A/' (model-deployment-aws) or 'B/' (ml-workflow-aws): 'A/cli.py',
    'A/Pipfile', 'A/.gitignore', 'B/src/workflow/cli.py', 'B/src/model-training/package/trainer/task.py'.
    code(path, a, b=None, focus=, font_size=22, cuts={line: 'cut after'}) CODE() panel, <= 12 lines,
        must fit the frame (22 pt ~66 chars a line, 20 pt ~74); .code .header; highlight with
        code_span(p.code, k, "sub") / line_bar(p.code, k, colour), k = file line - a.
    excerpt(path, a, b) · source_text(path) · shown_path(path) · readme(n, 'A'|'B') (stripped) ·
    readme_rows(a, b, 'A'|'B') (command rows for type_lines(), fences dropped) ·
    readme_card(lines, body, repo='A', quote=False) GREY card 'README.md · lines a–b' + chip A/B.

Terminals (house: 12.6 wide, 22 pt = 65 chars a row; 20 pt = 72)
    term(prompt=P_MD, rows=10, title='laptop') · laptop_term(rows, prompt) · strip_term(prompt, rows=3)
    resize(scene, t, rows) PLAYS · retitle(t, title) ANIM · room · bare_prompt · type_cmd(scene, t, cmd,
    type_time, prompt=True, soft=None) · type_lines(scene, t, rows) · out(scene, t, lines, wrap=,
    color=) · cd_prompt(scene, t, prompt) (also for entering a container: P_APP / P_ROOT) ·
    rows_of / beside / covers_text / attach / pin / unpin / on_bar / under_term for tags at a row ·
    row_tag, turn_row, extra_row(kind), time_row, cost_row (sized for a terminal row) ·
    no_panel_chip() (GREY 'needs your account · no output shown').

Tags and chips (GREY unless said; tags 22 pt, chips 20 pt)
    your_turn() YELLOW · extra_tag(kind=None) · check_tag() · stub_tag() · standin_tag() ·
    offline_tag() · illustration_tag() · recorded_tag(source='README A:137–147') · recording_tag()
    'at the time of recording' · erratum_tag() · cost_tag(text) GOLD (no money amounts: raises) ·
    grey_chip · dashed_chip (past/future, Vertex words) · tool_chip PURPLE · err_chip RED · ok_chip
    GREEN · differ_chip · version_chip('Docker 29.8.2') (+ 'at the time of recording' under it) ·
    file_card(path) · card(lines, head=) · question_card(text) YELLOW · ponder(scene, q, seconds)
    PLAYS (opaque pause_and_ponder card; FadeOut it at the next block) · flash_tag(scene, tg) ·
    bridge_card(rows=3 S02 rows) the Vertex ↔ AWS card (.heads .rows[i] .left .arrow .right) ·
    bridge_chip(i) the mini-legend chip for BRIDGE_ROWS[i] (S07: 2, S10: 4, S13: 5, S15: 6) ·
    duty_card([(text, True|False|None)], head=) slide 22 / 37 duty cards (.rows[i] .mark .text).
    Marks: under / hl_bar / ring(g, colour, dashed=) / strike / each(pieces, colour) ANIM.

Glyphs (text-free unless named; sizes in scene units)
    rack(h) BLUE machine · instance(box_w, box_h) · image_block(name, box_w) TEAL · outline_box(w, h,
    colour, solid=) (.fill .frame) · role_badge(name) BLUE hard-hat badge (.frame .hat .text) ·
    key_card(text='access key' | None) GREY key card · key_glyph / crossed_key · env_card(name,
    prefix='export ') · drawer('~/.aws') (.slot(i)) · bucket(name, box_w) BLUE pail · folder_icon ·
    file_icon(name) · disk · you(text) GREY person · bolt · cloud_shape(text) · lambda_icon(side,
    text='Lambda') BLUE λ tile (never AWS's logo) · gear(r) PURPLE · cube(side) TEAL array cube ·
    bars(values, hi=) output bars ('?' = dashed stub) · meter_icon · check_glyph / cross_glyph ·
    arrow / route (PINK) / travel / bounce / pulse_dot · laptop_glyph(width) (explainer.devops).
    CostDial(radius, caption='cost') GOLD dial, no digits: .run(scene, turns, secs) PLAYS ·
    .sweep(turns) ANIM · .freeze() (the endpoint is gone).
    endpoint_plate(name, machine='ml.m5.xlarge × 1', meter=True) BLUE address plate + rack + dial
        (.plate .text .rack .machine .dial): S09's two timestamped endpoints.
    step_box(name) pipeline step (pending WHITE) · step_state(b, 'pending'|'running'|'succeeded'|
        'failed'|'cached') ANIM · steps_list(order=STEP_VARS) the cli.py:322 list as one mono_line
        (.items, for the shuffle) · json_sheet(lines) GREEN JSON sheet.

Console (CONSOLE beats; tag them with illustration_tag(); first form: grey_chip("labels from the
README · if yours differ, look for the same field"))
    f = console_form(title, rows, form_w=8.6, path='IAM › Users')  rows: ("User name",
        "model-deployment") | ("button", "Create user") | ("check", "AmazonS3FullAccess", True) |
        ("radio", "Command Line Interface (CLI)", True) | ("note", "…")
    f.rows[i] has .label .field .value (fields) / .box .text (buttons) / .mark .tick .text ·
    f.fill(i, value) ANIM (the value types in) · f.press(i) ANIM · f.title_text. README text only;
    no ARNs with ids, no account numbers, no prices.

Set pieces (V numbers = BRIEF; all built centred, layout x/y relative to the piece's anchor)
    V1 IdentityBadges(parts=('laptop', 'cloud'))  laptop (x -5.25, y 0.15) + ~/.aws drawer (y -1.75),
        border at x 0.25, BLUE cloud x 0.6..6.4 with badge slots (x 3.5; y 1.55 / 0.85 / 0.15) and a
        job slot (3.5, -1.45); container x -3.95..-0.15, y -2.6..0.9 (six inside rows). parts=() + build(scene) for an empty start. PLAYS: add_key · remove_key ·
        add_config(text='config') · role(scene, name, i) · request(scene, text) · endpoint(scene,
        text, dashed) · wear(scene, i) · key_stays(scene) · container(scene, name) TEAL box x -1.75 ·
        mount(scene, text='-v ~/.aws:/home/app/.aws') · exports(scene, names) -> cards ·
        env_pass(scene, names) · fall_off(scene, cards) · pass_key(scene, text='-e AWS_ACCESS_KEY_ID').
        .laptop .drawer .border .cloud .badges .key .config .box_c (.inside) .job .arrows
    V2 StarVsPin()  version line y 1.2 (2.x x -6.0..-0.45 | 3.x x 0.45..6.0), ticks under it.
        Labels y 2.3. PLAYS: star(scene) · resolve(scene, v, color=ERR) (dot + version; again = jump) ·
        jump(scene, v) · shelves(scene) (captions y 0.25, chips y -0.05..-1.6) · imports(scene,
        ok=False) (from a 'cli.py:21-23' chip at y -2.2; RED 'No module named …' under it, or GREEN
        ticks) · pin(scene, to='2.257.7') GREEN wall + 'sagemaker = "<3"' · caption(scene, text)
        (y -2.95). x_of(v).
        .axis .ticks .band .dot .shelf2 .shelf3 (.items) .wall .src
    V3 TwoPipes(built=False)  client zone x -6.45..-0.45 (photo, gears 'resize 224×224' / '÷ 255',
        cube '224 × 224 × 3', x -1.6), PINK wire, BLUE endpoint x 2.55..5.25 with the YELLOW front door, bars
        x 5.5..6.4; y -1.55..1.75. PLAYS: client · gears(scene, i=None) · light(scene, i) · to_cube ·
        send · label_door(scene, text) · out(scene, values, hi, color) · count(scene, to=FLOATS) ·
        inside(scene, ops) (the right pipe: gears into the endpoint, ops under it, 'serving_default'
        over it, the cube's label becomes 'JPEG bytes').
        client_cards() the S05 web app / phone app / notebook trio (4.4 wide each).
    V4 ArtifactTrip()  five nodes in a row (y 0, x -5.2 + 2.6 (i-1), 2.15 × 1.15): 1 GitHub release
        v1.0, 2 container, 3 SavedModel, 4 model.tar.gz, 5 S3 bucket; node 0 'create bucket' (RED,
        drawn by stop()) sits above node 1 (y 1.75) with an arrow down into it.
        PLAYS: build(scene, upto=5, lag) · marks(scene) · stop(scene) · resume(scene) · wall(scene,
        text) · unfold(scene) (card under node 3) · version(scene) · uri(scene, text=S3_URI_A).
        .nodes[i] (.frame .text) .arrows[i]
    V5 ThreeObjects(slots=True)  slots 3.4 × 1.4 at y 0.9, x -4.3 / 0 / 4.3 (captions y -0.1).
        PLAYS: slots · lane · zero · meter · run(scene, turns, secs) · model_card (x -6.45..1.85) ·
        fill_role(scene, name) · solidify · registry / unregistry · deploy(scene, name) (config card
        x 4.25 y 1.35; plate y -0.55, rack + dial under it, down to y -2.4) · delete(scene, 'endpoint'|'config'|'model'|
        'artifact') · swap_config(scene, text). .slot_list .slot_caps .card .sub .config .ep .dial .lane_g
    V6 ManualToPipeline(people=True, names=STAGE_TILES)  tiles 2.8 × 1.0 at y 1.0, x ±1.6 / ±4.8,
        people + 'CLI' chips at y -0.5 / -1.15, headline y 2.35. PLAYS: headline(scene, text) (again:
        rewrites) · people_in · orchestrator(scene, text) (BLUE box x -1.4 y -1.0; people go) ·
        vertex(scene) · notes(scene, texts) (chips y 0.12) · chain(scene) PINK edges · frame(scene,
        text) BLUE frame · tick(scene, i) · light(scene, i). .tiles .links .people .box_o .box_v
    V7 CallableImage(name='cheese-app-data-collector', built=True)  input chip x -5.5, TEAL image
        x -2.45 (3.6 × 2.2), cards x 3.75 (5.0 wide): dev y 1.05 (GREY), prod y -1.05 (BLUE).
        PLAYS: build · choose(scene, 'dev'|'prod') · plug(scene, cmd, by='SageMaker') ·
        badge(scene, name=ROLE_SM). .image .switch .input .cards .branches .cmd_chip .badge_g
    V8 ReferenceDAG(layout='pile')  five step boxes (2.2 × 0.62, label font); 'pile' (column slots
        shuffled, x 1.4..4.0), 'column' (x 2.5, y 2.2 - 1.1 i; chips right of the boxes to x 6.55),
        'row' (y 0.6, x -5.2 + 2.6 i). Code panels at 22 pt are near full width: put them above or
        below the graph (shift the piece), or a short 20 pt excerpt beside it.
        PLAYS: edge(scene, i, j=i+1) (boxes settle into the column, PINK edge) · relayout(scene,
        'row'|'column') · cache(scene, which, none=3) · uncache · states(scene, {i: state}) · pulse ·
        drawer(scene) (row only: bucket y -2.65..-0.85, trays y -1.2) · files(scene, names) ·
        unknown(scene, i, text) · note(scene, text). ANIM: state(i, s).
        .boxes .edges {(i, j)} .chips .bucket_g .files_g .layout

Capture folder names: assets/terminal/laptop (every captured command: a fresh docker:29.8.2-dind
engine standing in for the laptop; containers inside it), assets/terminal/expected (the RECORDED
README output, md-predict-readme.txt); assets/terminal/helpers and capture-only plumbing are refused.
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import yaml
from manim import (DL, DOWN, DR, LEFT, ORIGIN, PI, RIGHT, TAU, UL, UP, UR, AnimationGroup, Arc,  # noqa: F401
                   Arrow, Circle, Create, DashedLine, DashedVMobject, Dot, FadeIn, FadeOut, GrowArrow,
                   GrowFromCenter, Indicate, LaggedStart, Line, MoveAlongPath, Polygon, Rectangle,
                   ReplacementTransform, RoundedRectangle, Rotate, ShowIncreasingSubsets, Succession, Text,
                   Transform, TransformFromCopy, UpdateFromAlphaFunc, ValueTracker, VGroup, VMobject,
                   always_redraw, linear, there_and_back)

from explainer import style as S
from explainer.components import pause_and_ponder, person_icon, ponder_card  # noqa: F401 (re-export)
from explainer.devops import (CAPTION, LABEL, MONO, OUTPUT, PANEL, SMALL, TAG, TERM_BG,  # noqa: F401
                              PROMPT_PATH, ReadmeTracker, Terminal, box, browser_window, cell_width, chip, code_block,
                              code_panel, code_span, file_glyph, folder_glyph, glyph_range, label,
                              lecture_ref, line_bar, line_pitch, mono, mono_line, server, substring, tag)
from explainer.devops import laptop as laptop_glyph  # noqa: F401
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
# SAY lines per scene (script.md v2, after the four-lens review merge); every scene asserts its own:
#   SAY = NARRATION["S07"]; assert len(SAY) == SAY_COUNT["S07"]
SAY_COUNT = {"S01": 6, "S02": 8, "S03": 10, "S04": 13, "S05": 7, "S06": 7, "S07": 8, "S08": 9,
             "S09": 7, "S10": 9, "S11": 9, "S12": 10, "S13": 7, "S14": 8, "S15": 13, "S16": 8}

# ------------------------------------------------------------------ semantic colours (BRIEF.md)
LAPTOP = S.GREY          # your laptop, its terminal, ~/.aws, the IAM user's access key, the four people
YOU = LAPTOP
KEY = LAPTOP             # the user's access key card (it lives on your disk)
CLOUD = S.BLUE           # S3, SageMaker (Model, config, endpoint, jobs, pipeline), ECR, Lambda, console
ROLE = CLOUD             # the role badges (BLUE hard hats)
IMAGE = S.TEAL           # model-deployment-cli-aws, the cheese-app-* images, AWS prebuilt TF images,
CONTAINER = IMAGE        #   the TF Serving stand-in
SHARED = S.ORANGE        # PyPI's newest release that "*" lets in, AWS-managed policies, the scraped web,
SYSTEM = SHARED          #   root-owned folders Docker made for you
OWN = S.GREEN            # what you own and pin: "<3", committed locks, the model artifact, TFRecords,
PIN = OWN                #   the pipeline definition; also a pass / a tick / a succeeded step
PASS = S.GREEN
TOOL = S.PURPLE          # aws CLI, docker, pipenv, git, boto3, the SageMaker SDK, TensorFlow
ERR = S.RED              # exec format error, ModuleNotFoundError, NoCredentialsError, the forgotten endpoint
TURN = S.YELLOW          # your turn, the tracker, look here now, the ponder timer, a running step
COST = S.GOLD            # endpoints, jobs, S3/ECR storage, Lambda, the clean-up card
ROUTE = S.PINK           # S3 URIs, the request and its JSON, -v / -e arrows, property references (DAG edges)
EDGE = ROUTE
PAST = S.GREY            # past / future (L1, L13, L14, L23) and the slides' Vertex AI words: dashed
FUTURE = PAST
VERTEX = PAST
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


# ------------------------------------------------------------------ series rules: no names, no ids
_NAME_RE = re.compile(r"Pavlos(?:[ _]Protopapas)?|Protopapas", re.IGNORECASE)
_CID_RE = re.compile(r"\b(app@|root@)[0-9a-f]{12}\b")
DLC_ACCOUNT = "763104351884"         # AWS's deep-learning-container registry account (laptop/92:191, 251)
DLC_MASK = "<aws-dlc-account>"


def unname(s: str) -> str:
    """s with the instructor's name masked ('‹instructor›'), container ids as '<id>' and AWS's DLC
    account number as '<aws-dlc-account>'. capture(), recorded() and source_text() apply it."""
    s = _NAME_RE.sub("‹instructor›", s)
    s = _CID_RE.sub(lambda m: m.group(1) + "<id>", s)
    return s.replace(DLC_ACCOUNT, DLC_MASK)


# ------------------------------------------------------------------ captures
CAPTURE_FOLDERS = ("laptop",)
# commands that take several file lines without ending in '\' (script.md "TERM" conventions)
CMD_LINES = {("laptop", "16"): 4, ("laptop", "53"): 2, ("laptop", "57"): 2, ("laptop", "80"): 6,
             ("laptop", "81"): 2}
# a line typed at a container prompt inside an istep capture (25, 27-30, 60, 68, 73, 90)
_TYPED_RE = re.compile(r"^(?:\(app\) )?(?:app|root)@(?:<id>|[0-9a-f]{12}):/app[$#] ")


class Capture:
    """One captured command (assets/terminal/<folder>/<file>). .cmd_lines (typed rows) .cmd (joined
    with '\\n') .k (file lines of the command) .lines (output body, no [exit N]) .exit .raw (every
    file line, tabs expanded, masked by unname()) .path"""

    def __init__(self, cmd_lines, lines, exit_code, raw, path):
        self.cmd_lines, self.lines, self.exit, self.raw, self.path = cmd_lines, lines, exit_code, raw, path
        self.k = len(cmd_lines)
        self.cmd = "\n".join(cmd_lines)

    def line(self, n: int) -> str:
        """File line n (1-based). Refuses the command lines (typed, never printed), a line typed at a
        container prompt (use .typed(n)) and the [exit N] line."""
        if not 1 <= n <= len(self.raw):
            raise IndexError(f"{self.path.name} has {len(self.raw)} lines, not {n}")
        if n <= self.k:
            raise ValueError(f"{self.path.name}:{n} is part of the typed command (lines 1-{self.k}): "
                             "type it with type_capture(), never print it")
        s = self.raw[n - 1]
        if re.fullmatch(r"\[exit -?\d+\]", s):
            raise ValueError(f"{self.path.name}:{n} is the [exit N] line: never printed")
        if _TYPED_RE.match(s):
            raise ValueError(f"{self.path.name}:{n} was typed at a container prompt: "
                             f"type_cmd(scene, t, c.typed({n})) with the prompt P_APP / P_ROOT")
        return s

    def typed(self, n: int) -> str:
        """The text typed at a container prompt on file line n (prompt and id stripped), e.g.
        capture("27").typed(35) == 'python cli.py --prepare'. Type it after P_APP / P_ROOT."""
        s = self.raw[n - 1]
        m = _TYPED_RE.match(s)
        if not m:
            raise ValueError(f"{self.path.name}:{n} is not a line typed at a container prompt: {s[:60]!r}")
        return s[m.end():]

    def at(self, *spec) -> list[str]:
        """Lines by FILE line numbers, as script.md writes them: ints, (a, b) inclusive ranges and
        '…' items (a literal '…' line). at(3, (5, 7), '…', 15). Never adds '…' by itself. Blank lines
        inside a range are kept (drop them with [s for s in … if s.strip()])."""
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
    """capture("laptop/27") or capture("27") (= laptop/): the one file assets/terminal/laptop/NN-*.txt.
    Fails loudly when missing: never show an uncaptured output. The command takes lines 1..k: k from
    CMD_LINES (16, 53, 57, 80, 81), else line 1 plus every row that follows a trailing '\\'."""
    folder, _, stem = name.rpartition("/")
    folder = folder or "laptop"
    if "capture-only" in name or "helpers" in name:
        raise ValueError("helpers/ and capture-only/ are plumbing: never shown")
    if folder not in CAPTURE_FOLDERS:
        raise ValueError(f"capture folder {folder!r}: one of {CAPTURE_FOLDERS} (expected/: recorded())")
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


def recorded(*nums, file: str = "md-predict-readme.txt") -> list[str]:
    """RECORDED(expected/md-predict-readme.txt: nums): lines by FILE line number (ints or (a, b)
    ranges), right-stripped. The '#' provenance lines (1-3) and the '$' command (4) are refused.
    recorded((7, 10)) = Image: data/brie-2.jpg … Label:    brie"""
    p = EXPECTED / file
    raw = p.read_text(encoding="utf-8").rstrip("\n").split("\n")
    out_ = []
    for r in nums:
        a, b = (r, r) if isinstance(r, int) else r
        for n in range(a, b + 1):
            s = raw[n - 1]
            if s.startswith("#") or s.startswith("$ "):
                raise ValueError(f"{p.name}:{n} is provenance or the command, never printed as output")
            out_.append(unname(s.rstrip()))
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


def cut(s: str, after: str | None = None, n: int | None = None, ellipsis: str = "…") -> str:
    """script.md's `to "…"`: the line cut right after `after` (first occurrence), ending in '…'.
    With n (no `after`): script.md's `cut`, the first n-1 characters + '…' (unchanged if it fits)."""
    if after is None:
        assert n is not None, "cut(s, after) or cut(s, n=65)"
        return s if len(s) <= n else s[:n - 1] + ellipsis
    i = s.index(after) + len(after)
    return s[:i] + ellipsis


def from_phrase(s: str, phrase: str, ellipsis: str = "…") -> str:
    """script.md's `from "…"`: the line from `phrase` on, after a '…' ("…NoCredentialsError …")."""
    i = s.index(phrase)
    return ellipsis + s[i:] if i else s


def unbox(s: str) -> str:
    """A rich-traceback line without its box borders ('│', '╭', '╰', '─' runs), as script.md asks:
    '│ ❱  73 │   s3_client.create_bucket(…) │' -> '❱  73 │   s3_client.create_bucket(…)'."""
    s = s.strip()
    s = re.sub(r"^[│╭╰]\s?", "", s)
    s = re.sub(r"\s?[│╮╯]$", "", s)
    s = re.sub(r"─{3,}", "", s)
    return s.rstrip()


# ------------------------------------------------------------------ the running example
USER = "student"
P_HOME = "student@laptop:~$"
P_MD = "student@laptop:~/model-deployment-aws$"           # Part A (README A)
P_MW = "student@laptop:~/ml-workflow-aws$"                # Part B (README B)
P_LAPTOP = P_HOME
STAGES = ("data-collector", "data-processor", "model-training", "workflow")


def P_SRC(stage: str) -> str:  # noqa: N802 (script.md's name)
    """'student@laptop:~/ml-workflow-aws/src/<stage>$' for stage in STAGES."""
    assert stage in STAGES, stage
    return f"student@laptop:~/ml-workflow-aws/src/{stage}$"


P_APP = "(app) app@<id>:/app$"       # inside the Part A, training and workflow containers (ids masked)
P_ROOT = "root@<id>:/app#"           # inside the collector and processor containers
T_LAPTOP = "laptop"

BUCKET_A_PH = "your-models-bucket-placeholder"                       # laptop/17
ROLE_A_PH = "arn:aws:iam::000000000000:role/SageMakerExecutionRole"  # laptop/17 (placeholder account)
KEY_PH = "PLACEHOLDER_NOT_A_REAL_ACCESS_KEY"                         # laptop/55
SECRET_PH = "PLACEHOLDER_NOT_A_REAL_SECRET_KEY_000000000000"         # laptop/55
README_ACCOUNT = "123456789012"     # README A:43, AWS's documentation placeholder (README card only)
BUCKET_A = "cheese-app-models-demo"          # README A:51 (+ "[REPLACE WITH YOUR UNIQUE BUCKET NAME]")
BUCKET_B = "cheese-app-ml-workflow-demo"     # README B:28
REGION = "us-east-1"
USER_A, USER_B = "model-deployment", "ml-workflow-user"
ROLE_A = "SageMakerExecutionRole"
ROLE_SM, ROLE_LAMBDA = "CheeseAppSageMakerExecutionRole", "CheeseAppLambdaExecutionRole"
IMAGE_A = "model-deployment-cli-aws"
STEP_NAMES = ("DataCollector", "DataProcessor", "ModelTraining", "CreateModel", "DeployModel")
STEP_VARS = ("step_collect", "step_process", "step_train", "step_create_model", "step_deploy_lambda")
STAGE_TILES = ("Data Collector", "Data Processor", "Model Training", "Model Deploy")
LABELS = ("parmigiano", "gruyere", "brie", "gouda")      # cli.py:41-42, index 0..3
INSTANCE_A = "ml.m5.xlarge"
ENDPOINT_B = "cheese-app-endpoint"
TARBALL = "model.tar.gz"
S3_URI_A = "s3://<bucket>/model-mobilenetv2_train_base_True.v1/model.tar.gz"
FLOATS = 224 * 224 * 3          # 150,528


# ------------------------------------------------------------------ sources
REPO_A, REPO_B = "model-deployment-aws", "ml-workflow-aws"
_REPO_ALIAS = {"A": REPO_A, "B": REPO_B}


def _src(path: str) -> Path:
    """'A/cli.py', 'B/src/workflow/cli.py' or the full 'model-deployment-aws/cli.py'."""
    head, _, rest = path.partition("/")
    if head in _REPO_ALIAS:
        path = f"{_REPO_ALIAS[head]}/{rest}"
    p = SOURCE / path
    if p.exists() and p.is_file():
        return p
    raise FileNotFoundError(f"assets/source/{path} (paths start with A/ or B/)")


def shown_path(path: str) -> str:
    """The repo-relative path a panel header shows: 'B/src/workflow/cli.py' -> 'src/workflow/cli.py'."""
    return str(_src(path).relative_to(SOURCE)).split("/", 1)[1]


def source_text(path: str) -> str:
    """An assets/source file: 'A/cli.py', 'A/README.md', 'B/src/model-training/package/trainer/task.py'."""
    return unname(_src(path).read_text(encoding="utf-8"))


def excerpt(path: str, first: int, last: int) -> str:
    """Lines first..last (1-based, inclusive) of assets/source/<path>."""
    return "\n".join(source_text(path).split("\n")[first - 1:last])


def readme(n: int, repo: str = "A") -> str:
    """README line n (repo 'A' = model-deployment-aws, 'B' = ml-workflow-aws), stripped. A README
    command often sits in a fence: compare with `in`."""
    return excerpt(f"{repo}/README.md", n, n).strip()


def readme_rows(a: int, b: int, repo: str = "B") -> list[str]:
    """README lines a..b as command rows (verbatim, right-stripped; blank rows and ``` fences dropped)
    for type_lines(): e.g. readme_rows(159, 162, "B") is the Docker Hub block."""
    rows = [s.rstrip() for s in excerpt(f"{repo}/README.md", a, b).split("\n")]
    return [s for s in rows if s.strip() and not s.strip().startswith("```")]


_LANG = {".py": "python", ".toml": "toml", ".sh": "bash", ".md": "markdown", ".yaml": "yaml",
         ".yml": "yaml", ".txt": "text", ".json": "json", ".lock": "json", ".cfg": "ini"}


def _lang(name: str) -> str:
    if name.startswith("Dockerfile"):
        return "docker"
    if name == "Pipfile":
        return "toml"
    if name == ".gitignore":
        return "text"
    return _LANG.get(Path(name).suffix, "text")


def code(path: str, first: int, last: int | None = None, language: str | None = None, focus=None,
         font_size: float = 22, shown: str | None = None, max_lines: int = 12, cuts: dict | None = None,
         dedent: bool = False):
    """CODE(path: first–last) of script.md: a code_panel quoting assets/source/<path> ('A/cli.py',
    'B/src/workflow/cli.py'), header '<repo-relative path> · lines a–b'. <= 12 lines. The panel must
    fit the frame (22 pt holds ~66 characters a line, 20 pt ~74); a wider panel raises: cut a line
    with cuts={file_line: 'text it ends after'} (the house '…', GREY) or use font_size=20.
    .code .header; highlight with code_span(p.code, k, "x") / line_bar(p.code, k, colour),
    k = file line - first. dedent=True removes the common leading indentation."""
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
    p = code_panel("\n".join(lines), shown or shown_path(path), first, language, focus=focus,
                   font_size=font_size)
    if p.width > 2 * SAFE_X - 0.1:
        longest = max(range(len(lines)), key=lambda i: len(lines[i].expandtabs(4)))
        raise ValueError(f"CODE {path}: {p.width:.2f} wide at {font_size} pt leaves the frame (line "
                         f"{first + longest}, {len(lines[longest])} characters): cuts={{{first + longest}: "
                         f"'...'}} or font_size=20")
    for n in cuts:
        code_span(p.code, n - first, "…").set_color(S.GREY)
    return p


def readme_card(lines, body, repo: str = "A", quote: bool = False, card_w: float | None = None,
                size: float = 22) -> VGroup:
    """A GREY README card: header 'README.md · line n' (or 'lines a–b' for a tuple) + a small chip
    'A' / 'B' (which README), and the README's own words (str: '\\n' separates rows, label font,
    markdown stripped by you; or any mobject). quote=True adds a quote bar. .frame .head .body .repo"""
    where = f"line {lines}" if isinstance(lines, int) else f"lines {lines[0]}–{lines[1]}"
    rc = chip(repo, S.GREY, size=CAPTION)
    head = VGroup(mono("README.md", CAPTION, S.GREY), label(f"· {where}", CAPTION, S.GREY), rc) \
        .arrange(RIGHT, buff=0.12)
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
    g.frame, g.head, g.body, g.repo = frame, head, body, rc
    return g


# ------------------------------------------------------------------ trackers (script.md, eleven)
SECTIONS = {
    "A1": "A › Setup Environments",
    "A2": "A › Run Container",
    "A3": "A › Prepare, deploy, predict",
    "A4": "A › Clean Up",
    "B1": "B › Setup Environments",
    "B2": "B › Data Collector",
    "B3": "B › Data Processor",
    "B4": "B › Model Training",
    "B5": "B › Build & Push",
    "B6": "B › Automate Collector",
    "B7": "B › SageMaker Pipelines",
}
STEPS = {
    "A1": ["Clone repo", "Enable services", "IAM user", "Execution role", "S3 bucket"],
    "A2": ["aws configure", "Env variables", "Edit config", "chmod +x", "docker-shell"],
    "A3": ["Prepare model", "Deploy endpoint", "Test predictions"],
    "A4": ["Console delete", "AWS CLI", "CLI script"],
    "B1": ["Clone repo", "AWS services", "S3 bucket", "IAM user", "Access keys", "Install CLI",
           "Configure CLI", "Test config", "IAM roles"],
    "B2": ["docker-shell", "Run search", "Check bucket"],
    "B3": ["docker-shell", "Run clean", "Check bucket", "Run prepare", "Check bucket"],
    "B4": ["docker-shell", "Local training", "Package trainer", "Remote training", "Monitor jobs"],
    "B5": ["Hub login", "Hub build", "Hub push", "ECR variables", "Pull image", "Create repo", "ECR login",
           "Tag image", "Push image", "Verify push", "Print URI"],
    "B6": ["docker-shell", "Processing job", "Check console"],
    "B7": ["Run pipeline", "Check Studio", "Test components"],
}
TRACKER_KEYS = tuple(SECTIONS)
# script.md's tracker variants: '· extra · check' (22, 23, 85-87), '· extra · capture stub' (40),
# '· extra · local stand-in, not SageMaker' (45-48), '· extra · built offline, not sent' (92)
EXTRA_KINDS = ("check", "capture stub", "local stand-in, not SageMaker", "built offline, not sent")


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
    """Tracker `key` (TRACKER_KEYS: 'A1'..'A4', 'B1'..'B7') at `step` (1-based; None = no step lit
    yet), placed top-left: 'README A › <section>', one dot per step, 'step k of N: <step>' + the extra
    suffix (GREY). extra: False | True (' · extra') | one of EXTRA_KINDS (' · extra · check' …) | any
    other str (appended after ' · ')."""
    tr = ReadmeTracker(SECTIONS[key].split(" › ", 1)[1], STEPS[key])
    tr.key = key
    old = tr.head[0]                       # 'README' -> 'README A' / 'README B' (which tutorial)
    new = mono(f"README {key[0]}", tr.size, S.GREY).move_to(old, aligned_edge=LEFT)
    tr.head.submobjects[0] = new
    tr.head.arrange(RIGHT, buff=0.12).align_to(old, LEFT)
    tr.dots.align_to(tr.head, LEFT)
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
    make.__doc__ = f"tracker('{key}', step, extra): README {SECTIONS[key]}"
    return make


tracker_a1, tracker_a2, tracker_a3, tracker_a4, tracker_b1, tracker_b2, tracker_b3, tracker_b4, \
    tracker_b5, tracker_b6, tracker_b7 = map(_tracker_factory, TRACKER_KEYS)


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
    same = getattr(old, "key", "?")[:1] == getattr(new, "key", "!")[:1]
    keep = VGroup(old.head[0], old.head[1]) if same else VGroup(old.head[1])   # 'README A ›' stays put
    scene.remove(old)
    olds = [old.head[2], old.dots, old.caption] + ([] if same else [old.head[0]])
    scene.add(*keep, *olds)
    moves = [FadeTransform(old.head[2], new.head[2]), ReplacementTransform(old.dots, new.dots),
             FadeTransform(old.caption, new.caption)]
    if not same:
        moves.append(FadeTransform(old.head[0], new.head[0]))
    scene.play(*moves, *anims, run_time=run_time)
    scene.remove(*keep, *new.head, new.dots, new.caption, *olds)
    scene.add(new)
    return new


def lref(slides: str) -> VGroup:
    """The GREY 'Lecture 15 · slides 11–12' tag, top right (script.md LECTURE 15 · …). It lives exactly
    as long as the picture it cites: FadeIn with the redrawn slide idea, FadeOut with it."""
    return lecture_ref(15, slides)


# ------------------------------------------------------------------ terminals
def term(prompt: str = P_MD, rows: int = 10, title: str | None = T_LAPTOP, width: float = 12.6,
         size: float = 22, place: bool = True) -> Terminal:
    """The house terminal: 12.6 wide, 22 pt, 65 characters a row, centred, bottom edge at BOTTOM.
    Height = rows x 0.403 + 0.85. Full width, or a 3-row strip (rows=3) under a picture. size=20
    gives 72 characters a row."""
    t = Terminal(prompt=prompt, width=width, rows=rows, size=size, title=title)
    if place:
        t.shift(np.array([-t.box.get_center()[0], BOTTOM - t.box.get_bottom()[1], 0]))
    return t


def laptop_term(rows: int = 10, prompt: str = P_MD) -> Terminal:
    """Title 'laptop' (every capture is from the laptop/ folder; inside a container only the prompt
    changes: cd_prompt(scene, t, P_APP) / P_ROOT)."""
    return term(prompt, rows, T_LAPTOP)


def strip_term(prompt: str = P_MD, rows: int = 3) -> Terminal:
    """A 3-row strip (bottom of the frame, top edge STRIP_TOP) under a picture."""
    return term(prompt, rows, T_LAPTOP)


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
    """ANIM: the terminal's title changes in place (e.g. 'laptop' -> 'laptop · second terminal')."""
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
    the same continuation rule as type_capture(). For the README blocks with no output panel (Docker Hub, ECR push)."""
    out_, cont = [], False
    for row in rows:
        out_.append(type_cmd(scene, t, row, type_time, prompt=not cont))
        cont = row.rstrip().endswith("\\")
    return out_


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
    """PLAYS: after `cd` (or entering a container: P_APP / P_ROOT), the prompt changes; a bare prompt
    line appears and its path flashes."""
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


def no_panel_chip(s: str = "needs your account · no output shown") -> VGroup:
    """The GREY chip under a command typed with no output panel (script.md "No output panel")."""
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
    """GREY 'extra' tag; kind one of EXTRA_KINDS ('check', 'capture stub', 'local stand-in, not
    SageMaker', 'built offline, not sent') or any short str -> 'extra · <kind>'."""
    return tag("extra" + (f" · {kind}" if kind else ""), S.GREY)


def check_tag() -> VGroup:
    """'extra · check': the resolver / import checks (laptop/22, 23, 85, 86, 87)."""
    return extra_tag("check")


def stub_tag() -> VGroup:
    """'extra · capture stub': laptop/40 (S3 replaced by a stub that sends nothing)."""
    return extra_tag("capture stub")


def standin_tag() -> VGroup:
    """'extra · local stand-in, not SageMaker': the TF Serving stand-in (laptop/45-48, S01 hook)."""
    return extra_tag("local stand-in, not SageMaker")


def offline_tag() -> VGroup:
    """'extra · built offline, not sent': the pipeline JSON (laptop/92)."""
    return extra_tag("built offline, not sent")


def illustration_tag(s: str = "illustration") -> VGroup:
    """On every CONSOLE form and the V-pictures of cloud machinery (schematic; never a screenshot)."""
    return tag(s, S.GREY)


def recorded_tag(source: str | None = "README A:137–147") -> VGroup:
    """'recorded · README A:137–147': the README's own --predict output (expected/)."""
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
    """A dashed chip: past/future things and the slides' Vertex AI words (L14 Cloud Run, L23). .box .text"""
    t = mono(s, size, color) if mono_font else label(s, size, color)
    ob = outline_box(t.width + 0.48, mono("|", size).height + 0.24, color, solid=False)
    t.move_to(ob)
    g = VGroup(ob, t)
    g.box, g.text = ob, t
    return g


def tool_chip(s: str, size: float = 20) -> VGroup:
    """A tool as a PURPLE mono chip (never a logo): aws, docker, pipenv, boto3, sagemaker …"""
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
    """A YELLOW-outlined question card ('What is behind an endpoint?', the parked question,
    'Test yourself'); '\\n' breaks rows. .frame .body"""
    rows = VGroup(*[label(s, size, INK) for s in text.split("\n")]).arrange(DOWN, buff=0.14)
    w = card_w or rows.width + 0.8
    frame = RoundedRectangle(width=w, height=rows.height + 0.6, corner_radius=0.16, stroke_color=color,
                             stroke_width=3).set_fill(S.BG, 1)
    rows.move_to(frame)
    g = VGroup(frame, rows)
    g.frame, g.body = frame, rows
    return g


def recorded_card(nums, source: str = "README A:137–147", size: float = 22, card_w: float | None = None,
                  color=INK, wrap: int = 64) -> VGroup:
    """RECORDED(expected/md-predict-readme.txt: nums): a GREY-outlined panel quoting those lines in
    mono, with the tag 'recorded · README A:137–147' on its top edge (right). nums: an int, a range
    tuple, or a list of them. Long lines wrap at `wrap` characters. .frame .body .tag .rows"""
    nums = [nums] if isinstance(nums, (int, tuple)) else list(nums)
    lines = soft(recorded(*nums), wrap)
    body = VGroup(*[mono(s, size, color) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    w = card_w or body.width + 0.7
    frame = box(w, body.height + 0.75, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
    body.move_to(frame).align_to(frame, LEFT).shift(RIGHT * 0.35 + DOWN * 0.1)
    tg = recorded_tag(source)
    tg.move_to(frame.get_corner(UR) + np.array([-tg.width / 2 - 0.2, 0, 0]))
    g = VGroup(frame, body, tg)
    g.frame, g.body, g.tag, g.rows = frame, body, tg, list(body)
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
    """A machine: a SOLID rack (BLUE): an endpoint instance, a job's machine."""
    return server(height=h, units=units, color=color)


def instance(box_w: float = 1.2, box_h: float = 0.75, color=CLOUD, inner: bool = True, dashed: bool = True,
             inner_color=IMAGE) -> VGroup:
    """A managed instance: a DASHED outline (BLUE) with a TEAL inner box (the container).
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

def key_glyph(key_w: float = 0.8, color=KEY, dashed: bool = False) -> VGroup:
    """A key (bow, shaft, two teeth); GREY solid: the IAM user's access key (key_card() wraps it)."""
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
    """The GREY key with a RED cross over it: 'no key'. .key .cross"""
    k = key_glyph(key_w)
    x = cross_glyph(key_w * 0.7).move_to(k)
    g = VGroup(k, x)
    g.key, g.cross = k, x
    return g

def bucket(name: str | None = None, box_w: float = 1.0, color=CLOUD, size: float = 20,
           mono_font: bool = True) -> VGroup:
    """An S3 bucket (BLUE pail) with an optional name under it. .pail .text"""
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


def disk(w: float = 0.42, color=S.GREY) -> VGroup:
    """A small disk (cylinder) icon: an instance's local disk, the laptop's disk."""
    top = Circle(radius=w / 2, stroke_color=color, stroke_width=2.5).stretch(0.35, 1)
    bot = top.copy().shift(DOWN * w * 0.45)
    sides = VGroup(Line(top.get_left(), bot.get_left()), Line(top.get_right(), bot.get_right()))
    sides.set_stroke(color, 2.5)
    return VGroup(sides, bot, top.set_fill(color, 0.3))


def you(text: str | None = "you", color=YOU, h: float = 0.6, size: float = 20) -> VGroup:
    """A GREY person ('you'; the four people at four CLIs) with a label under it. .figure .text"""
    fig = person_icon(color, h)
    g = VGroup(fig)
    g.figure, g.text = fig, None
    if text:
        t = label(text, size, color).next_to(fig, DOWN, buff=0.1)
        g.add(t)
        g.text = t
    return g


def bolt(h: float = 0.6, color=ROUTE) -> VMobject:
    """A lightning bolt (a Lambda call)."""
    pts = [[0.1, 0.5], [-0.2, 0.0], [0.05, 0.0], [-0.15, -0.5], [0.25, 0.08], [0.0, 0.08], [0.18, 0.5]]
    m = Polygon(*[[x * h, y * h, 0] for x, y in pts], stroke_color=color, stroke_width=2.5)
    return m.set_fill(color, 0.45)


def cloud_shape(text: str | None = None, color=CLOUD, cloud_w: float = 2.4, size: float = 20,
                dashed: bool = False) -> VGroup:
    """A cloud outline (AWS BLUE; the scraped web ORANGE) with up to two rows of text
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

def meter_icon(w: float = 0.9, color=COST) -> VGroup:
    """A text-free GOLD meter (a bar half full in a frame) for recap cards and the clean-up icon. .fill_bar"""
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
    """A schematic AWS console form (no AWS branding, no smile logo, no orange header bar, never a
    screenshot; tag it illustration_tag()). title: the page title ('Create user'). path: an optional
    breadcrumb above it ('IAM › Users'). rows (README field labels and values only):
        ("User name", "model-deployment")            label + field (value '' = an empty field)
        ("button", "Create user")                    a button (BLUE outline)
        ("check", "AmazonS3FullAccess", True)        a checkbox row (policies, services)
        ("radio", "Command Line Interface (CLI)", True)
        ("note", "labels from the README · if yours differ, look for the same field")  a GREY note
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


# ------------------------------------------------------------------ set-piece base
class Piece(VGroup):
    """A set piece. PLAYS methods add their new mobjects to the piece after playing them, and take
    parts away with drop(); the piece itself stays one top-level mobject on the scene."""

    def _ensure(self, scene):
        if self not in scene.mobjects:
            scene.add(self)

    def heal(self, scene):
        """Re-seat the piece as ONE top-level mobject. Animating a group that is not itself on the
        scene (a glyph_range, a code_span) makes Manim split every parent that holds its members into
        top-level pieces; scene.add(piece) undoes that. The PLAYS methods call it for you."""
        scene.add(self)

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




# ------------------------------------------------------------------ L15 glyphs and cards
def role_badge(name: str = ROLE_A, color=ROLE, dashed: bool = False, size: float = 20,
               mono_font: bool = False) -> VGroup:
    """A BLUE hard-hat badge: an IAM role, a cloud principal (SageMakerExecutionRole,
    CheeseAppSageMakerExecutionRole, CheeseAppLambdaExecutionRole). The name is set in the label
    font (4.8 wide for the longest; mono_font=True: 6.1). .frame .hat .text"""
    dome = Arc(radius=0.15, start_angle=0, angle=PI, color=color, stroke_width=3).set_fill(color, 0.6)
    brim = Line(LEFT * 0.22, RIGHT * 0.22, color=color, stroke_width=4).next_to(dome, DOWN, buff=0.0)
    hat = VGroup(dome, brim)
    t = (mono if mono_font else label)(name, size, INK)
    row = VGroup(hat, t).arrange(RIGHT, buff=0.14)
    fr = outline_box(row.width + 0.4, max(0.56, row.height + 0.26), color, solid=not dashed,
                     fill_opacity=0.15, radius=0.1)
    row.move_to(fr)
    g = VGroup(fr, row)
    g.frame, g.hat, g.text = fr, hat, t
    return g


def key_card(text: str = "access key", color=KEY, size: float = 20) -> VGroup:
    """The GREY key card: the IAM user's access key (it lives on your laptop, in ~/.aws).
    text=None draws the card without words (0.9 wide). .frame .glyph .text"""
    kg = key_glyph(0.55, color)
    parts = [kg]
    t = None
    if text:
        t = label(text, size, INK)
        parts.append(t)
    row = VGroup(*parts).arrange(RIGHT, buff=0.14)
    fr = RoundedRectangle(width=row.width + 0.36, height=0.56, corner_radius=0.08, stroke_color=color,
                          stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
    row.move_to(fr)
    g = VGroup(fr, row)
    g.frame, g.glyph, g.text = fr, kg, t
    return g


def env_card(name: str, color=LAPTOP, size: float = 20, prefix: str = "export ") -> VGroup:
    """A GREY card for one shell variable ('export AWS_ACCESS_KEY_ID'); prefix='-e ' for a docker
    flag (draw it PINK). .frame .text"""
    t = mono(prefix + name, size, INK)
    fr = RoundedRectangle(width=t.width + 0.34, height=0.5, corner_radius=0.08, stroke_color=color,
                          stroke_width=2.5).set_fill(S.BG, 1)
    t.move_to(fr)
    g = VGroup(fr, t)
    g.frame, g.text = fr, t
    return g


def lambda_icon(side: float = 0.62, color=CLOUD, text: str | None = "Lambda", size: float = 20) -> VGroup:
    """A BLUE Lambda tile (a λ in a rounded square, never AWS's logo) with an optional name under it.
    .tile .text"""
    sq = RoundedRectangle(width=side, height=side, corner_radius=0.1, stroke_color=color,
                          stroke_width=3).set_fill(color, 0.18)
    lam = label("λ", 30, color).move_to(sq)
    tile = VGroup(sq, lam)
    g = VGroup(tile)
    g.tile, g.text = tile, None
    if text:
        t = label(text, size, INK).next_to(sq, DOWN, buff=0.1)
        g.add(t)
        g.text = t
    return g


def gear(r: float = 0.24, color=TOOL, teeth: int = 8) -> VGroup:
    """A text-free gear glyph (a preprocessing operation)."""
    body = Circle(radius=r, stroke_color=color, stroke_width=3).set_fill(color, 0.25)
    hole = Circle(radius=r * 0.35, stroke_color=color, stroke_width=2.5).set_fill(S.BG, 1)
    ts = VGroup(*[Rectangle(width=r * 0.34, height=r * 0.38, stroke_width=0).set_fill(color, 0.9)
                  .move_to(UP * (r + r * 0.12)).rotate(k * TAU / teeth, about_point=ORIGIN)
                  for k in range(teeth)])
    return VGroup(ts, body, hole)


def cube(side: float = 0.9, color=IMAGE, depth: float = 0.32) -> VGroup:
    """A text-free pseudo-3D cube outline (the 224×224×3 array of floats). .front"""
    front = Rectangle(width=side, height=side, stroke_color=color, stroke_width=3).set_fill(color, 0.15)
    d = np.array([depth, depth, 0])
    tl, tr, br = front.get_corner(UL), front.get_corner(UR), front.get_corner(DR)
    top = Polygon(tl, tr, tr + d, tl + d, stroke_color=color, stroke_width=3).set_fill(color, 0.3)
    side_ = Polygon(tr, br, br + d, tr + d, stroke_color=color, stroke_width=3).set_fill(color, 0.08)
    g = VGroup(side_, top, front)
    g.front = front
    return g.move_to(ORIGIN)


def bars(values, bar_w: float = 0.2, max_h: float = 1.0, color=OWN, hi: int | None = None,
         hi_color=TURN, buff: float = 0.08) -> VGroup:
    """Text-free output bars standing on a common baseline (one per class probability; values in
    0..1, a '?' value draws a dashed GREY stub). hi: index drawn in hi_color. .bar_list"""
    bs = []
    for i, v in enumerate(values):
        if v == "?":
            b = outline_box(bar_w, max_h * 0.5, S.GREY, solid=False, radius=0.02)
        else:
            h = max(0.04, float(v) * max_h)
            col = hi_color if i == hi else color
            b = Rectangle(width=bar_w, height=h, stroke_color=col, stroke_width=2).set_fill(col, 0.6)
        bs.append(b)
    g = VGroup(*bs).arrange(RIGHT, buff=buff, aligned_edge=DOWN)
    g.bar_list = bs
    return g


def drawer(text: str = "~/.aws", drawer_w: float = 2.6, drawer_h: float = 1.95, color=LAPTOP,
           size: float = 20) -> VGroup:
    """The GREY ~/.aws drawer on the laptop (cards go inside: .slot(i) is the centre of row i, top
    row 0). .frame .text"""
    fr = RoundedRectangle(width=drawer_w, height=drawer_h, corner_radius=0.08, stroke_color=color,
                          stroke_width=3).set_fill(S.GREY_DARKER, 1)
    handle = RoundedRectangle(width=0.5, height=0.08, corner_radius=0.04, stroke_color=color,
                              stroke_width=2).move_to(fr.get_bottom() + UP * 0.12)
    t = mono(text, size, color).move_to(fr.get_corner(UL) + np.array([0.12, -0.22, 0]), aligned_edge=LEFT)
    g = VGroup(fr, handle, t)
    g.frame, g.text = fr, t

    def slot(i: int):
        return fr.get_top() + DOWN * (0.72 + 0.62 * i)

    g.slot = slot
    return g


def version_chip(s: str, color=TOOL, size: float = 20) -> VGroup:
    """'Docker 29.8.2' / 'AWS CLI 2.34.63' with a small 'at the time of recording' under it.
    .chip .note"""
    c = chip(s, color, size=size, font=MONO)
    n = label("at the time of recording", 20, S.GREY).next_to(c, DOWN, buff=0.1)
    g = VGroup(c, n)
    g.chip, g.note = c, n
    return g


BRIDGE_ROWS = (
    ("GCS bucket", "S3 bucket"),
    ("service-account key", "IAM user + access key (laptop) / role (cloud)"),
    ("Model Registry", "SageMaker Model"),
    ("Online prediction endpoint", "endpoint configuration + endpoint"),
    ("Vertex AI Pipelines (Kubeflow, KFP DSL)", "SageMaker Pipelines (SDK step classes)"),
    ("Artifact Registry", "ECR"),
    ("Cloud Functions", "Lambda"),
)


def bridge_card(rows=BRIDGE_ROWS[:2] + BRIDGE_ROWS[3:4], size: float = 22, col_gap: float = 0.5,
                header: bool = True) -> VGroup:
    """S02's Vertex ↔ AWS bridge: two columns, 'the lecture · Vertex AI' (GREY dashed words) and
    'this tutorial · AWS' (BLUE words), one row per (vertex_word, aws_word). Default rows: the three
    S02 says (bucket, key/role, endpoint); BRIDGE_ROWS has all seven. Build it, then FadeIn
    .heads and each .rows[i] on its phrase. .frame .heads .rows (each .left .arrow .right)"""
    lefts = [label(a, size, S.GREY) for a, _ in rows]
    rights = [label(b, size, INK) for _, b in rows]
    hl = dashed_chip("the lecture · Vertex AI", PAST, size=20)
    hr = chip("this tutorial · AWS", CLOUD, size=20)
    lw = max([m.width for m in lefts] + [hl.width])
    max([m.width for m in rights] + [hr.width])  # (the right column grows freely)
    xr = lw + col_gap                      # the right column's left edge (the left column starts at 0)
    rws = VGroup()
    y = 0.0
    for a, b in zip(lefts, rights):
        a.move_to([a.width / 2, y, 0])
        ar = label("→", size, S.GREY).move_to([lw + col_gap / 2, y, 0])
        b.move_to([xr + b.width / 2, y, 0])
        r = VGroup(a, ar, b)
        r.left, r.arrow, r.right = a, ar, b
        rws.add(r)
        y -= max(a.height, b.height) + 0.26
    heads = VGroup()
    if header:
        top = rws.get_top()[1] + 0.45
        hl.move_to([hl.width / 2, top, 0])
        hr.move_to([xr + hr.width / 2, top, 0])
        heads = VGroup(hl, hr)
    inner = VGroup(heads, rws)
    fr = box(inner.width + 0.7, inner.height + 0.6, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
    fr.move_to(inner)
    g = VGroup(fr, heads, rws)
    g.frame, g.heads, g.rows = fr, heads, list(rws)
    return g.move_to(ORIGIN)


def bridge_chip(i: int | None = None, left: str | None = None, right: str | None = None,
                size: float = 20) -> VGroup:
    """The S02 mini-legend chip for one bridge row: 'Model Registry → SageMaker Model' (left GREY,
    right WHITE, a GREY dashed outline). bridge_chip(2) = BRIDGE_ROWS[2]. Park it lower right:
    .to_corner(DR, buff=0.4) (or above a strip). .box .text"""
    if i is not None:
        left, right = BRIDGE_ROWS[i]
    t = VGroup(label(left, size, S.GREY), label("→", size, S.GREY), label(right, size, INK)).arrange(RIGHT, buff=0.14)
    ob = outline_box(t.width + 0.44, t.height + 0.3, PAST, solid=False)
    t.move_to(ob)
    g = VGroup(ob, t)
    g.box, g.text = ob, t
    return g


def duty_card(items, size: float = 22, head: str | None = None) -> VGroup:
    """Slide 22's duty card / slide 37's duty cards: rows (text, ok) with ok True (GREEN ✓), False
    (GREY dashed ✗ row) or None (no mark). .frame .rows (each .mark .text)"""
    rws = []
    for text, ok in items:
        t = label(text, size, INK if ok is not False else S.GREY)
        if ok is True:
            mk = check_glyph(0.28, OWN)
        elif ok is False:
            mk = cross_glyph(0.24, S.GREY, 4)
        else:
            mk = Dot(radius=0.05, color=S.GREY)
        r = VGroup(mk, t).arrange(RIGHT, buff=0.2)
        r.mark, r.text = mk, t
        rws.append(r)
    body = VGroup(*rws).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    parts = [body]
    hd = None
    if head:
        hd = label(head, 20, S.GREY)
        parts.insert(0, hd)
    inner = VGroup(*parts).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
    fr = box(inner.width + 0.7, inner.height + 0.55, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
    inner.move_to(fr)
    g = VGroup(fr, inner)
    g.frame, g.rows, g.head = fr, rws, hd
    return g


class CostDial(VGroup):
    """The GOLD cost dial: a needle that sweeps while a billable thing exists, no digits (no prices).
    It never rewinds. .run(scene, turns, seconds) PLAYS a sweep · .freeze() stops it where it is
    (the endpoint is deleted: call it, then the dial may stay on screen as 'stopped').
    .face .needle .tracker (angle in turns) .caption"""

    def __init__(self, radius: float = 0.5, caption: str | None = "cost", **kw):
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
            self.caption = label(caption, 20, COST).next_to(face, DOWN, buff=0.1)
            self.add(self.caption)

    def run(self, scene, turns: float = 0.5, seconds: float = 2.0, extra=()):
        scene.play(self.tracker.animate(rate_func=linear).increment_value(turns), *extra, run_time=seconds)

    def sweep(self, turns: float = 0.5):
        """ANIM: the needle sweeps on by `turns` (play it alongside a voiceover beat)."""
        return self.tracker.animate(rate_func=linear).increment_value(turns)

    def freeze(self):
        """Stop the needle where it is (the thing that billed is gone)."""
        self.needle.clear_updaters()
        return self


def endpoint_plate(name: str = "…-endpoint-<timestamp>", machine: str = f"{INSTANCE_A} × 1",
                   meter: bool = True, plate_w: float = 3.4, size: float = 20) -> VGroup:
    """An endpoint drawn as an address plate (BLUE, mono name; 4.1 wide for the default name) with a
    machine (rack + mono 'ml.m5.xlarge × 1') slid under it and its GOLD dial under the rack (total
    height ~2.3). machine=None leaves the machine (and dial) out. .plate .text .rack .machine .dial
    (CostDial, or None)"""
    t = mono(name, size, INK)
    pl = RoundedRectangle(width=max(plate_w, t.width + 0.4), height=0.62, corner_radius=0.1,
                          stroke_color=CLOUD, stroke_width=3).set_fill(CLOUD, 0.18)
    t.move_to(pl)
    g = VGroup(pl, t)
    g.plate, g.text, g.rack, g.machine, g.dial = pl, t, None, None, None
    if machine:
        rk = rack(0.62, CLOUD, units=2).next_to(pl, DOWN, buff=0.18).align_to(pl, LEFT).shift(RIGHT * 0.2)
        mt = mono(machine, size, INK).next_to(rk, RIGHT, buff=0.18)
        g.add(rk, mt)
        g.rack, g.machine = rk, mt
        if meter:
            d = CostDial(0.36, caption=None).next_to(rk, DOWN, buff=0.12)
            g.add(d)
            g.dial = d
    return g


def step_box(name: str, box_w: float = 2.2, size: float = 20, mono_font: bool = False) -> VGroup:
    """A pipeline step box (pending: WHITE outline; the name in the label font, so five fit in a row:
    mono_font=True is 2.5 wide). Change its state with
    step_state(b, state) (ANIM). .frame .text .state .badge (the ✓ / ✗ / 'cached' mark, or None)"""
    t = (mono if mono_font else label)(name, size, INK)
    fr = RoundedRectangle(width=max(box_w, t.width + 0.4), height=0.62, corner_radius=0.1,
                          stroke_color=INK, stroke_width=2.5).set_fill(S.BG, 1)
    t.move_to(fr)
    g = VGroup(fr, t)
    g.frame, g.text, g.state, g.badge, g.name = fr, t, "pending", None, name
    return g


_STATE = {"pending": (INK, S.BG, 1.0), "running": (TURN, TURN, 0.3), "succeeded": (OWN, OWN, 0.15),
          "failed": (ERR, ERR, 0.18), "cached": (S.GREY, S.BG, 1.0)}


def step_state(b, state: str, run_time: float = 0.4):
    """ANIM: step box `b` takes `state` (pending WHITE · running YELLOW fill · succeeded GREEN ✓ badge
    at the right end · failed RED · cached GREY dashed look + 'cached' chip). The old badge goes."""
    stroke, fill, op = _STATE[state]
    anims = [b.frame.animate.set_stroke(stroke).set_fill(fill, op),
             b.text.animate.set_color(S.GREY if state == "cached" else INK)]   # after the frame: stays on top
    if b.badge is not None:
        old = b.badge
        b.remove(old)
        anims.append(FadeOut(old))
        b.badge = None
    new = None
    if state == "succeeded":
        dot = Circle(radius=0.19, stroke_color=OWN, stroke_width=2.5).set_fill(S.BG, 1)
        new = VGroup(dot, check_glyph(0.2, OWN)).move_to(b.frame.get_corner(UR) + np.array([-0.05, 0.02, 0]))
    elif state == "failed":
        dot = Circle(radius=0.19, stroke_color=ERR, stroke_width=2.5).set_fill(S.BG, 1)
        new = VGroup(dot, cross_glyph(0.16, ERR, 4)).move_to(b.frame.get_corner(UR) + np.array([-0.05, 0.02, 0]))
    elif state == "cached":
        new = chip("cached", S.GREY, size=20).next_to(b.frame, DOWN, buff=0.08).align_to(b.frame, RIGHT)
    if new is not None:
        b.add(new)
        b.badge = new
        anims.append(FadeIn(new))
    b.state = state
    return AnimationGroup(*anims, run_time=run_time)


def steps_list(order=STEP_VARS, size: float = 20, color=INK, split: int = 3) -> VGroup:
    """'steps=[step_collect, step_process, step_train,' / '       step_create_model, step_deploy_lambda]'
    (cli.py:322 spelling) as two mono_lines (one line would be 14 wide); the first `split` names on
    line 1. order: any permutation of STEP_VARS (the shuffle beat). .lines .items (the five names'
    glyph groups, in `order`)"""
    a = "steps=[" + ", ".join(order[:split]) + ","
    b = " " * 7 + ", ".join(order[split:]) + "]"
    l1, l2 = mono_line(a, size, color), mono_line(b, size, color)
    l2.next_to(l1, DOWN, buff=0.12, aligned_edge=LEFT)
    g = VGroup(l1, l2)
    g.lines = [l1, l2]
    g.items = [substring(l1, v) for v in order[:split]] + [substring(l2, v) for v in order[split:]]
    return g


def json_sheet(lines, size: float = 20, color=OWN, title: str = "pipeline definition · JSON") -> VGroup:
    """A GREEN sheet of JSON lines (laptop/92 lines as given), a folded corner, a GREY title.
    .frame .body .title"""
    body = VGroup(*[mono(s, size, INK) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    hd = label(title, 20, S.GREY)
    inner = VGroup(hd, body).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    w, h = inner.width + 0.7, inner.height + 0.55
    fr = Polygon([-w / 2, h / 2, 0], [w / 2 - 0.3, h / 2, 0], [w / 2, h / 2 - 0.3, 0], [w / 2, -h / 2, 0],
                 [-w / 2, -h / 2, 0], stroke_color=color, stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
    inner.move_to(fr)
    g = VGroup(fr, inner)
    g.frame, g.body, g.title = fr, body, hd
    return g


# ------------------------------------------------------------------ V1 · IdentityBadges
class IdentityBadges(_Anchored):
    """V1 · a key on the laptop, roles in the cloud (S03 built; S10, S11, S14 reprise). Full frame,
    built centred: laptop glyph (x -5.25, y 0.15), the ~/.aws drawer under it (y -1.75, 2.4 × 1.95),
    a dashed GREY border at x 0.25 (top y 2.45; 'laptop' | 'AWS' flank it just above the cloud's top edge), the BLUE cloud region
    (x 0.6..6.4, y -2.7..2.3) with three badge slots (x 3.5; y 1.55, 0.85, 0.15) and a job/endpoint
    slot (3.5, -1.45); the TEAL container (when added) x -3.95..-0.15, y -2.6..0.9 with six rows
    inside (mount: 3, env_pass: 3, pass_key: 1); export cards at the top left (y 2.6..1.0). Built with parts=() for an empty start, or the default ('laptop', 'cloud').
    PLAYS: add_key(scene) the GREY key card drops into the drawer · add_config(scene, text) ·
    role(scene, name, i=0) a BLUE badge forms in slot i · request(scene, text) a PINK arrow
    laptop→cloud carrying a small key card · remove_key(scene) · endpoint(scene, text, dashed) a BLUE box in the job
    slot · wear(scene, i=0) a copy of badge i settles on that box · key_stays(scene) a key copy
    bounces off the border · container(scene, name) the TEAL container (x -1.75) on the laptop side ·
    mount(scene, text) PINK -v arrow: the drawer's cards copy into the container · exports(scene,
    names) GREY 'export …' cards above the laptop · env_pass(scene, names) PINK '-e' arrows into the
    container, names listed inside · fall_off(scene, cards) cards hit the wall, turn RED, drop ·
    pass_key(scene, text) Part B: the key travels into the container as '-e AWS_ACCESS_KEY_ID'.
    .laptop .drawer .border .cloud .badges .key .config .box_c .job .arrows"""

    LAPTOP_XY = (-5.25, 0.15)
    DRAWER_XY = (-5.25, -1.75)
    BOX_XY = (-2.05, -0.85)
    BOX_W, BOX_H = 3.8, 3.5
    BORDER_X = 0.25
    CLOUD_X = 3.5
    JOB_XY = (3.5, -1.45)
    BADGE_Y = (1.55, 0.85, 0.15)

    def __init__(self, parts=("laptop", "cloud"), **kw):
        super().__init__(**kw)
        self.badges, self.arrows = [], []
        self.key = self.config = self.box_c = self.job = None
        lg = laptop_glyph(1.9, LAPTOP).move_to(self.p(*self.LAPTOP_XY))
        dr = drawer(drawer_w=2.4).move_to(self.p(*self.DRAWER_XY))
        self.laptop = VGroup(lg, dr)
        self.drawer = dr
        bx = self.BORDER_X
        border = DashedLine(self.p(bx, -2.75), self.p(bx, 2.45), color=S.GREY, stroke_width=2.5,
                            dash_length=0.12)
        cl = outline_box(5.8, 5.0, CLOUD, solid=True, fill_opacity=0.05, radius=0.3)
        cl.move_to(self.p(self.CLOUD_X, -0.2))
        # 'laptop' | 'AWS' sit on one line just above the cloud's top edge (y 2.3), flanking the
        # border's top: inside the corner they would collide with the request arrow and badge 0
        bl = label("laptop", 20, S.GREY).next_to(border.get_top(), LEFT, buff=0.1)
        br = label("AWS", 20, CLOUD).next_to(border.get_top(), RIGHT, buff=0.1)
        br.align_to(cl, DOWN).shift(UP * (cl.height + 0.12))
        bl.align_to(br, UP)                       # same cap line ('laptop' has a descender)
        self.border = VGroup(border, bl, br)
        self.cloud = VGroup(cl)
        if "laptop" in parts:
            self.add(self.laptop, self.border)
        if "cloud" in parts:
            self.add(self.cloud)

    def build(self, scene, run_time: float = 0.8):
        """PLAYS: the laptop, the border and the cloud appear (when built with parts=())."""
        mobs = [m for m in (self.laptop, self.border, self.cloud) if m not in self.submobjects]
        if mobs:
            self.show(scene, *mobs, run_time=run_time)

    def remove_key(self, scene, run_time: float = 0.4):
        """PLAYS: the key card leaves the drawer (no keys typed: only config exists)."""
        if self.key is not None:
            self.drop(scene, self.key, shift=UP * 0.4, run_time=run_time)
            self.key = None

    def add_key(self, scene, text: str = "access key", run_time: float = 0.7):
        k = key_card(text).move_to(self.drawer.slot(1 if self.config is not None else 0))
        start = k.copy().shift(UP * 1.2).set_opacity(0)
        self.show(scene, k, anims=[ReplacementTransform(start, k)], run_time=run_time)
        self.key = k
        return k

    def add_config(self, scene, text: str = "config", run_time: float = 0.6):
        """PLAYS: a GREY 'config' file card appears in the drawer's top row (a key card already
        there moves down a row)."""
        c = _small_file(text).move_to(self.drawer.slot(0))
        if self.key is not None:
            scene.play(self.key.animate.move_to(self.drawer.slot(1)), run_time=0.3)
        self.config = c
        return self.show(scene, c, anims=[FadeIn(c, shift=DOWN * 0.3)], run_time=run_time)

    def role(self, scene, name: str = ROLE_A, i: int = 0, run_time: float = 0.7):
        b = role_badge(name).move_to(self.p(self.CLOUD_X, self.BADGE_Y[i]))
        self.badges.append(b)
        return self.show(scene, b, anims=[GrowFromCenter(b)], run_time=run_time)

    def request(self, scene, text: str = "signed by the user", y: float = 1.7, run_time: float = 1.0):
        a = route(self.p(-4.0, y), self.p(1.4, y))
        cap = label(text, 20, ROUTE).next_to(a, DOWN, buff=0.08)
        k = key_card(None).scale(0.8).move_to(a.get_start() + RIGHT * 0.5)
        self.show(scene, a, cap, k, anims=[GrowArrow(a), FadeIn(cap), FadeIn(k)], run_time=run_time * 0.5)
        scene.play(k.animate.shift(RIGHT * (a.get_length() - 1.6)), run_time=run_time * 0.5)
        self.arrows.append(VGroup(a, cap, k))
        return VGroup(a, cap, k)

    def endpoint(self, scene, text: str = "endpoint · later", dashed: bool = True, run_time: float = 0.6):
        t = label(text, 22, INK)
        fr = outline_box(max(3.0, t.width + 0.6), 1.25, CLOUD, solid=not dashed, fill_opacity=0.1)
        fr.move_to(self.p(*self.JOB_XY))
        t.move_to(fr).shift(DOWN * 0.22)
        g = VGroup(fr, t)
        g.frame, g.text = fr, t
        if self.job is not None:
            self.drop(scene, self.job, run_time=0.2)
        self.job = g
        return self.show(scene, g, run_time=run_time)

    def wear(self, scene, i: int = 0, run_time: float = 0.8):
        """PLAYS: a copy of badge i settles on the job box's top edge."""
        b = self.badges[i]
        c = b.copy()
        target = c.copy().next_to(self.job.frame, UP, buff=0.06)
        self.show(scene, c, anims=[c.animate.move_to(target)], run_time=run_time)
        return c

    def key_stays(self, scene, run_time: float = 1.0):
        """PLAYS: a copy of the key card travels to the border and bounces back, then goes."""
        src = self.key if self.key is not None else self.drawer
        k = key_card(None).move_to(src.get_center())
        scene.add(k)
        scene.play(bounce(k, self.p(self.BORDER_X - 0.5, src.get_center()[1] - self.ref.get_center()[1]), run_time))
        scene.play(FadeOut(k), run_time=0.2)
        scene.remove(k)

    def container(self, scene, name: str = "container", run_time: float = 0.6):
        fr = outline_box(self.BOX_W, self.BOX_H, IMAGE, solid=True, fill_opacity=0.08)
        fr.move_to(self.p(*self.BOX_XY))
        t = label(name, 22, IMAGE).move_to(fr.get_top() + DOWN * 0.3)
        g = VGroup(fr, t)
        g.frame, g.text, g.inside = fr, t, VGroup()
        g.add(g.inside)
        self.box_c = g
        self.rows_used = 0
        return self.show(scene, g, run_time=run_time)

    def _inside_slot(self, k: int):
        return self.box_c.frame.get_top() + DOWN * (0.78 + 0.47 * k)

    def mount(self, scene, text: str = "-v ~/.aws:/home/app/.aws", run_time: float = 1.2):
        """PLAYS: a PINK arrow from the drawer into the container; the drawer's cards copy inside,
        under a mono '/home/app/.aws'."""
        a = route(self.drawer.frame.get_right(), self.box_c.frame.get_left() + DOWN * 0.9, arc=0.5)
        cap = mono(text, 20, ROUTE).next_to(self.box_c.frame, DOWN, buff=0.15)
        cap.align_to(self.box_c.frame, RIGHT).shift(RIGHT * 0.1)
        r0 = self.rows_used
        dest = mono("/home/app/.aws", 20, INK).move_to(self._inside_slot(r0))
        cards = [m for m in (self.config, self.key) if m is not None]
        copies = [m.copy() for m in cards]
        targets = [(key_card("key") if m is self.key else _small_file("config")).move_to(self._inside_slot(r0 + j + 1))
                   for j, m in enumerate(cards)]
        self.rows_used = r0 + 1 + len(cards)
        self.show(scene, a, cap, anims=[GrowArrow(a), FadeIn(cap)], run_time=run_time * 0.4)
        anims = [FadeIn(dest)] + [ReplacementTransform(c, t) for c, t in zip(copies, targets)]
        scene.add(*copies)
        scene.play(*anims, run_time=run_time * 0.6)
        scene.remove(*copies, *targets, dest)
        self.box_c.inside.add(dest, *targets)
        self.arrows.append(VGroup(a, cap))
        self.heal(scene)
        return VGroup(a, cap)

    def exports(self, scene, names=("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_REGION"),
                run_time: float = 0.8):
        cards = VGroup(*[env_card(n) for n in names]).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
        cards.move_to(self.p(-6.45, 2.6), aligned_edge=UL)
        keep_inside(cards)
        self.show(scene, *cards, anims=[LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cards],
                                                    lag_ratio=0.3)], run_time=run_time)
        return list(cards)

    def env_pass(self, scene, names=("AWS_REGION", "S3_MODELS_BUCKET_NAME", "SAGEMAKER_ROLE"),
                 run_time: float = 1.0):
        """PLAYS: PINK '-e' arrows come down through the container's top wall (its right end, under
        the export cards' reach); the names list inside it, in the next free rows."""
        arrs, labs = [], []
        r0 = self.rows_used
        self.rows_used = r0 + len(names)
        top = self.box_c.frame.get_top()[1]
        x_r = self.box_c.frame.get_right()[0]
        for j, n in enumerate(names):
            y = self._inside_slot(r0 + j)[1]
            x = x_r - 0.35 - 0.45 * (len(names) - 1 - j)
            arrs.append(route(np.array([x, top + 0.65, 0]), np.array([x, top - 0.12, 0]), stroke=4))
            labs.append(mono(n, 20, INK).move_to([self.box_c.frame.get_center()[0], y, 0]))
        tag_e = mono("-e", 22, ROUTE).next_to(arrs[0], LEFT, buff=0.12)
        self.show(scene, *arrs, tag_e, anims=[LaggedStart(*[GrowArrow(a) for a in arrs], lag_ratio=0.25),
                                              FadeIn(tag_e)], run_time=run_time * 0.5)
        self.show(scene, *labs, into=self.box_c.inside, run_time=run_time * 0.5)
        self.arrows.append(VGroup(*arrs, tag_e))
        return VGroup(*arrs, *labs, tag_e)

    def fall_off(self, scene, cards, run_time: float = 1.0):
        """PLAYS: the cards drop onto the container's top wall, turn RED and fall away to the left."""
        top = self.box_c.frame.get_top()[1] + 0.05
        moves = [c.animate.shift(DOWN * (c.get_bottom()[1] - top - 0.06 * k)) for k, c in enumerate(cards)]
        scene.play(*moves, run_time=run_time * 0.4)
        scene.play(*[c.frame.animate.set_stroke(ERR) for c in cards], run_time=run_time * 0.2)
        self.drop(scene, *cards, shift=DOWN * 1.0 + LEFT * 1.0, run_time=run_time * 0.4)

    def pass_key(self, scene, text: str = "-e AWS_ACCESS_KEY_ID", run_time: float = 1.2):
        """PLAYS (Part B): the key card copies out of the drawer and rides a PINK arrow into the
        container, where it lands under the mono flag."""
        src = self.key if self.key is not None else self.drawer
        a = route(src.get_right() + RIGHT * 0.1, self.box_c.frame.get_left() + DOWN * 0.6, arc=0.3)
        cap = mono(text, 20, ROUTE).next_to(self.box_c.frame, DOWN, buff=0.15)
        cap.align_to(self.box_c.frame, RIGHT).shift(RIGHT * 0.1)
        k = key_card(None).move_to(src.get_center())
        target = key_card("key").move_to(self._inside_slot(self.rows_used))
        self.rows_used += 1
        self.show(scene, a, cap, anims=[GrowArrow(a), FadeIn(cap)], run_time=run_time * 0.4)
        scene.add(k)
        scene.play(ReplacementTransform(k, target), run_time=run_time * 0.6)
        scene.remove(k, target)
        self.box_c.inside.add(target)
        self.arrows.append(VGroup(a, cap))
        self.heal(scene)
        return target


# ------------------------------------------------------------------ V2 · StarVsPin
class StarVsPin(_Anchored):
    """V2 · the version line for `sagemaker` (S04 built, S14 reprise). Echoes L1's V4. Full width,
    built centred: the line at y 1.2 (2.x on x -6.0..-0.45, a break at 0, 3.x on 0.45..6.0), ticks
    '2.200' '2.257' | '3.0' '3.13' '3.29' under it (y 0.75). x_of('3.13.1') places any version.
    PLAYS: star(scene) the whole line ORANGE + 'sagemaker = "*"' (y 2.3, left) · resolve(scene, v,
    color=ERR) a PURPLE 'resolver' arrow drops a dot + its version at v (again: the dot jumps; also
    jump(scene, v): GREEN on 2.x, RED on 3.x) ·
    shelves(scene) module chips under each half (rows from y -0.05 down to about -1.6, captions y
    0.25) · imports(scene, ok=False) three PURPLE arrows from a 'cli.py:21-23' chip (y -2.2) into the
    3.x shelf (RED + 'No module named …' under the chip, y -2.85) or, ok=True, the 2.x shelf (GREEN
    ticks) · pin(scene) GREEN wall at 3.0 + 'sagemaker = "<3"' (y 2.3, right of the wall), the band turns GREEN on 2.x only, the
    dot jumps to 2.257.7 · caption(scene, text) a GREEN chip at the bottom (y -2.95; drop the error
    chip first). .axis .ticks .band .dot .shelf2 .shelf3 (.items
    {name: chip}) .wall .src"""

    LO2, HI2, LO3, HI3 = 2.200, 2.2577, 3.0, 3.29
    MODS2 = ("tensorflow", "serializers", "processing", "workflow", "get_execution_role")
    MODS3 = ("ai_registry", "core", "lineage", "mlops", "serve", "train")

    def __init__(self, **kw):
        super().__init__(**kw)
        self.dot = self.band = self.wall = self.src = self.star_label = self.pin_label = None
        self.shelf2 = self.shelf3 = None
        self.import_arrows = None
        y = 1.2
        a2 = Line(self.p(-6.0, y), self.p(-0.45, y), color=S.GREY, stroke_width=3)
        a3 = Line(self.p(0.45, y), self.p(6.0, y), color=S.GREY, stroke_width=3)
        brk = VGroup(Line(self.p(-0.25, y - 0.18), self.p(-0.05, y + 0.18)),
                     Line(self.p(0.05, y - 0.18), self.p(0.25, y + 0.18))).set_stroke(S.GREY, 3)
        self.axis = VGroup(a2, brk, a3)
        self.ticks = VGroup()
        for v in ("2.200", "2.257", "3.0", "3.13", "3.29"):
            x = self._x(float(v) if v != "2.257" else 2.257)
            self.ticks.add(VGroup(Line(self.p(x, y - 0.1), self.p(x, y + 0.1), color=S.GREY, stroke_width=2),
                                  mono(v, 20, S.GREY).move_to(self.p(x, y - 0.42))))
        self.add(self.axis, self.ticks)

    def _x(self, v: float) -> float:
        if v < 3:
            return -6.0 + (v - self.LO2) / (self.HI2 - self.LO2) * 5.55 * 0.97
        return 0.45 + (v - self.LO3) / (self.HI3 - self.LO3) * 5.55

    @staticmethod
    def _num(v: str) -> float:
        parts = v.split(".")
        if parts[0] == "2":
            return 2 + int(parts[1]) / 1000 + (int(parts[2]) / 10000 if len(parts) > 2 else 0)
        return 3 + int(parts[1]) / 100

    def x_of(self, v: str) -> np.ndarray:
        """The point on the line for version string v ('3.13.1', '2.257.7')."""
        return self.p(self._x(self._num(v)), 1.2)

    def star(self, scene, run_time: float = 0.8):
        band = Rectangle(width=12.1, height=0.3, stroke_width=0).set_fill(SHARED, 0.35).move_to(self.p(0, 1.2))
        lab = mono('sagemaker = "*"', 22, SHARED).move_to(self.p(-6.0, 2.3), aligned_edge=LEFT)
        self.band, self.star_label = band, lab
        self.show(scene, band, lab, anims=[FadeIn(band), FadeIn(lab)], run_time=run_time)
        self.submobjects.remove(band)
        self.submobjects.insert(0, band)          # under the axis
        return band

    def resolve(self, scene, v: str = "3.13.1", color=ERR, run_time: float = 1.0):
        pt = self.x_of(v)
        d = Dot(pt, radius=0.13, color=color)
        t = mono(v, 22, color).next_to(d, UP, buff=0.42)
        keep_inside(t)
        g = VGroup(d, t)
        if self.dot is None:
            arr = Arrow(pt + UP * 1.5, pt + UP * 0.2, buff=0, color=TOOL, stroke_width=4, tip_length=0.18)
            rl = label("resolver", 20, TOOL).next_to(arr, LEFT, buff=0.1)
            self.show(scene, arr, rl, anims=[GrowArrow(arr), FadeIn(rl)], run_time=run_time * 0.5)
            self.show(scene, g, anims=[FadeIn(d, scale=0.5), FadeIn(t)], run_time=run_time * 0.5)
            self.drop(scene, arr, rl, run_time=0.3)
        else:
            self.swap(scene, self.dot, g, run_time=run_time)
        self.dot = g
        return g

    def _shelf(self, names, x0: float, x1: float, caption: str, color=S.GREY):
        chips = [chip(n, color, size=20, font=MONO) for n in names]
        rows, cur, w = [], [], 0.0
        for c in chips:
            if cur and w + 0.14 + c.width > x1 - x0:
                rows.append(cur)
                cur, w = [], 0.0
            cur.append(c)
            w += (0.14 if len(cur) > 1 else 0) + c.width
        rows.append(cur)
        rg = VGroup(*[VGroup(*r).arrange(RIGHT, buff=0.14) for r in rows]).arrange(DOWN, buff=0.14)
        rg.move_to(self.p((x0 + x1) / 2, 0)).align_to(self.p(0, -0.05), UP)
        cap = label(caption, 20, S.GREY).move_to(self.p((x0 + x1) / 2, 0.25))
        board = Line(self.p(x0, rg.get_bottom()[1] - self.ref.get_center()[1] - 0.1),
                     self.p(x1, rg.get_bottom()[1] - self.ref.get_center()[1] - 0.1), color=S.GREY, stroke_width=4)
        g = VGroup(cap, rg, board)
        g.items = dict(zip(names, chips))
        g.caption = cap
        return g

    def shelves(self, scene, run_time: float = 0.8):
        self.shelf2 = self._shelf(self.MODS2, -6.0, -0.45, "version 2 · modules")
        self.shelf3 = self._shelf(self.MODS3, 0.45, 6.0, "version 3 · modules")
        self.show(scene, self.shelf2, self.shelf3, run_time=run_time)
        return self.shelf2, self.shelf3

    def imports(self, scene, ok: bool = False, run_time: float = 1.2):
        if self.src is None:
            self.src = chip("cli.py:21-23", TOOL, size=20, font=MONO).move_to(self.p(0, -2.2))
            self.show(scene, self.src, run_time=0.3)
        if self.import_arrows is not None:
            self.drop(scene, self.import_arrows, run_time=0.25)
        o = self.src.get_top()
        if ok:
            targets = [self.shelf2.items[n] for n in ("tensorflow", "serializers", "get_execution_role")]
            ends = [t.get_bottom() for t in targets]
        else:
            ends = [self.shelf3.items[n].get_bottom() + DOWN * 0.05 + RIGHT * dx
                    for n, dx in (("core", -0.4), ("serve", 0.0), ("train", 0.4))]
        arrs = VGroup(*[Arrow(o, e, buff=0.08, color=TOOL, stroke_width=3, tip_length=0.16) for e in ends])
        self.show(scene, arrs, anims=[LaggedStart(*[GrowArrow(a) for a in arrs], lag_ratio=0.2)],
                  run_time=run_time * 0.5)
        if ok:
            ticks = VGroup(*[check_glyph(0.24, OWN).next_to(t, UP, buff=0.04) for t in targets])
            self.show(scene, ticks, extra=[a.animate.set_color(OWN) for a in arrs], run_time=run_time * 0.5)
            res = VGroup(arrs, ticks)
        else:
            err = err_chip("No module named 'sagemaker.tensorflow'", size=20)
            err.next_to(self.src, DOWN, buff=0.15)
            keep_inside(err)
            self.show(scene, err, extra=[a.animate.set_color(ERR) for a in arrs], run_time=run_time * 0.5)
            res = VGroup(arrs, err)
        self.remove(arrs)
        self.remove(*res[1:])
        self.add(res)
        self.import_arrows = res
        return res

    def pin(self, scene, to: str = "2.257.7", run_time: float = 1.4):
        wall = Rectangle(width=0.14, height=1.0, stroke_width=0).set_fill(OWN, 0.9).move_to(self.p(0, 1.2))
        lab = mono('sagemaker = "<3"', 22, OWN).move_to(self.p(0.35, 2.3), aligned_edge=LEFT)
        self.show(scene, wall, lab, anims=[FadeIn(wall, shift=DOWN * 0.4), FadeIn(lab)], run_time=run_time * 0.4)
        self.wall, self.pin_label = wall, lab
        anims = []
        if self.band is not None:
            green = Rectangle(width=5.75, height=0.3, stroke_width=0).set_fill(OWN, 0.35).move_to(self.p(-3.225, 1.2))
            anims.append(Transform(self.band, green))
        if self.star_label is not None:
            anims.append(self.star_label.animate.set_opacity(0.35))
        if anims:
            scene.play(*anims, run_time=run_time * 0.3)
        self.jump(scene, to, run_time * 0.3)
        return wall

    def jump(self, scene, v: str, run_time: float = 0.5):
        """PLAYS: the dot jumps to version v (GREEN on 2.x, RED on 3.x)."""
        col = OWN if v.startswith("2") else ERR
        return self.resolve(scene, v, col, run_time=run_time)

    def caption(self, scene, text: str = "a constraint is not a pin (L1)", run_time: float = 0.5):
        c = ok_chip(text, size=22).move_to(self.p(0, -2.95))
        return self.show(scene, c, run_time=run_time)


# ------------------------------------------------------------------ V3 · TwoPipes
class TwoPipes(_Anchored):
    """V3 · where does preprocessing live? (S05 built, S08 reprise, S12). One horizontal pipe, built
    centred (y -1.55..1.75 around the anchor): the GREY dashed client zone (x -6.45..-0.45, 'your
    laptop · the client') with the photo (x -5.75), two PURPLE gears (x -4.25 'resize 224×224',
    x -2.85 '÷ 255', labels above) and the TEAL cube (x -1.35, label under); the PINK wire
    (x -0.45..2.55); the BLUE endpoint (x 2.55..5.25) with its front door on the left edge; output
    bars to its right (x 5.5..6.4). Built empty (built=False) or whole (built=True: S08).
    PLAYS: client(scene) zone + photo · gears(scene, i=None) both gears (or gear i) · to_cube(scene)
    · send(scene) wire + endpoint + door, the cube rides to the door · label_door(scene, text) a label
    under the door ('inputs[…] · floats …') · out(scene, values, hi, color) bars out of the back ·
    count(scene, to=150528) the cube's counter counts up (YELLOW, mono) · inside(scene) the right
    pipe: the gears move into the door, relabelled decode_jpeg → float32 → resize, the cube becomes
    'JPEG bytes' and the door 'serving_default' · light(scene, i) flash gear i (ANIM-like PLAYS).
    .zone .photo .gear_list .gear_labels .cube_g .wire .ep .door .door_label .bar_g .counter"""

    def __init__(self, built: bool = False, **kw):
        super().__init__(**kw)
        zf = outline_box(6.0, 2.85, LAPTOP, solid=False).move_to(self.p(-3.45, 0.12))
        zt = label("your laptop · the client", 20, LAPTOP).move_to(self.p(-6.3, 1.3), aligned_edge=LEFT)
        self.zone = VGroup(zf, zt)
        ph = VGroup(file_glyph(0.62, INK), label("photo.jpg", 20, INK))
        ph[1].next_to(ph[0], DOWN, buff=0.12)
        self.photo = ph.move_to(self.p(-5.75, -0.1))
        self.gear_list, self.gear_labels = [], []
        for x, s in ((-4.35, "resize 224×224"), (-2.75, "÷ 255")):
            gg = gear(0.3).move_to(self.p(x, 0.05))
            gl = label(s, 20, TOOL).next_to(gg, UP, buff=0.22)
            self.gear_list.append(gg)
            self.gear_labels.append(gl)
        cb = cube(0.85).move_to(self.p(-1.6, 0.1))
        cl = label("224 × 224 × 3", 20, IMAGE).next_to(cb, DOWN, buff=0.2)
        self.cube_g = VGroup(cb, cl)
        self.wire = Line(self.p(-0.45, 0.05), self.p(2.55, 0.05), color=ROUTE, stroke_width=5)
        ep = RoundedRectangle(width=2.7, height=2.2, corner_radius=0.14, stroke_color=CLOUD,
                              stroke_width=3).set_fill(CLOUD, 0.1).move_to(self.p(3.9, 0.05))
        et = label("endpoint", 22, CLOUD).move_to(ep.get_top() + DOWN * 0.3)
        mdl = label("the model", 20, INK).move_to(ep).shift(RIGHT * 0.25 + DOWN * 0.15)
        self.ep = VGroup(ep, et, mdl)
        self.door = RoundedRectangle(width=0.32, height=1.1, corner_radius=0.06, stroke_color=TURN,
                                     stroke_width=3).set_fill(S.BG, 1).move_to(ep.get_left() + RIGHT * 0.2)
        self.door_label = self.bar_g = self.counter = None
        if built:
            self.add(self.zone, self.photo, *self.gear_list, *self.gear_labels, self.cube_g, self.wire,
                     self.ep, self.door)

    def client(self, scene, run_time: float = 0.7):
        return self.show(scene, self.zone, self.photo, run_time=run_time)

    def gears(self, scene, i: int | None = None, run_time: float = 0.6):
        idx = [0, 1] if i is None else [i]
        mobs = [m for k in idx for m in (self.gear_list[k], self.gear_labels[k])]
        anims = [FadeIn(m) if m in self.gear_labels else GrowFromCenter(m) for m in mobs]
        self.show(scene, *mobs, anims=anims, run_time=run_time)

    def light(self, scene, i: int, color=TURN, run_time: float = 0.6):
        scene.play(Indicate(self.gear_labels[i], color=color, scale_factor=1.1),
                   Rotate(self.gear_list[i], PI / 2), run_time=run_time)

    def to_cube(self, scene, run_time: float = 0.8):
        src = self.photo[0].copy()
        scene.add(src)
        scene.play(src.animate.move_to(self.gear_list[0]), run_time=run_time * 0.3)
        scene.play(src.animate.move_to(self.gear_list[1]), Rotate(self.gear_list[0], PI / 2),
                   run_time=run_time * 0.3)
        scene.remove(src)
        self.show(scene, self.cube_g, anims=[ReplacementTransform(src, self.cube_g[0]), FadeIn(self.cube_g[1]),
                                             Rotate(self.gear_list[1], PI / 2)], run_time=run_time * 0.4)

    def send(self, scene, run_time: float = 1.2):
        self.show(scene, self.wire, self.ep, self.door,
                  anims=[Create(self.wire), FadeIn(self.ep), FadeIn(self.door)], run_time=run_time * 0.5)
        c = self.cube_g[0].copy()
        scene.add(c)
        scene.play(c.animate.scale(0.5).move_to(self.door.get_center()), run_time=run_time * 0.5)
        scene.play(FadeOut(c), self.door.animate.set_fill(TURN, 0.3), run_time=0.25)
        scene.remove(c)

    def label_door(self, scene, text: str = "inputs['input'] · floats (-1, 224, 224, 3)", run_time: float = 0.6):
        """PLAYS: a label under the endpoint names the front door (mono, YELLOW)."""
        t = mono(text, 20, TURN)
        t.next_to(self.ep[0], DOWN, buff=0.35).align_to(self.ep[0], RIGHT)
        keep_inside(t)
        if self.door_label is not None:
            return self.swap(scene, self.door_label, t, run_time=run_time)
        self.door_label = t
        return self.show(scene, t, run_time=run_time)

    def out(self, scene, values=(0.1, 0.1, 0.7, 0.1), hi: int | None = None, color=OWN,
            run_time: float = 0.6):
        b = bars(values, 0.16, 1.0, color, hi).move_to(self.p(5.95, 0.05))
        b.align_to(self.p(0, -0.45), DOWN)
        if self.bar_g is not None:
            return self.swap(scene, self.bar_g, b, run_time=run_time)
        self.bar_g = b
        return self.show(scene, b, anims=[GrowFromCenter(m) for m in b], run_time=run_time)

    def count(self, scene, to: int = FLOATS, run_time: float = 2.0):
        t = mono("0", 26, TURN).next_to(self.cube_g[0], UP, buff=0.25)
        self.counter = t
        self.show(scene, t, run_time=0.2)
        anchor = t.get_center().copy()

        def upd(m, a):
            m.become(mono(f"{int(round(a * to)):,}", 26, TURN).move_to(anchor))

        scene.play(UpdateFromAlphaFunc(t, upd), run_time=run_time, rate_func=linear)
        return t

    def inside(self, scene, ops=("decode_jpeg", "float32", "resize"), run_time: float = 1.6):
        """PLAYS: the right pipe. The gears cross the wire into the door (three, mono labels under the
        endpoint), the door becomes GREEN 'serving_default', the cube becomes 'JPEG bytes'."""
        g3 = [gear(0.2) for _ in ops]
        VGroup(*g3).arrange(RIGHT, buff=0.42).move_to(self.ep[0].get_center() + DOWN * 0.5 + RIGHT * 0.15)
        labs = VGroup(*[mono(o, 20, TOOL) for o in ops]).arrange(RIGHT, buff=0.08)
        arrows_ = []
        row = VGroup()
        for k, lb in enumerate(labs):
            row.add(lb)
            if k < len(labs) - 1:
                ar = label("→", 20, TOOL)
                row.add(ar)
                arrows_.append(ar)
        row.arrange(RIGHT, buff=0.1).next_to(self.ep[0], DOWN, buff=0.18).align_to(self.ep[0], RIGHT)
        keep_inside(row)
        olds = self.gear_list + self.gear_labels
        if self.door_label is not None:
            olds.append(self.door_label)
            self.door_label = None
        for m in olds:
            self._detach(m)
        scene.add(*olds)
        anims = [ReplacementTransform(self.gear_list[0], g3[0]), ReplacementTransform(self.gear_list[1], g3[1]),
                 FadeIn(g3[2]), ReplacementTransform(VGroup(*self.gear_labels, *olds[4:]), row)]
        scene.play(*anims, run_time=run_time * 0.6)
        scene.remove(*olds)
        self.add(*g3, row)
        self.gear_list, self.gear_labels = g3, [row]
        sd = mono("serving_default", 20, OWN).next_to(self.ep[0], UP, buff=0.12)
        jb = label("JPEG bytes", 20, IMAGE).move_to(self.cube_g[1])
        self.show(scene, sd, extra=[self.door.animate.set_stroke(OWN), self.ep[2].animate.set_opacity(0),
                                    Transform(self.cube_g[1], jb)], run_time=run_time * 0.4)
        self.door_label = sd
        self.heal(scene)
        return row


def client_cards(size: float = 20) -> VGroup:
    """V3's 'client-side brittleness' trio (S05): 'web app' (GREY, both gears), 'phone app' (the
    ÷ 255 gear missing: RED), 'notebook' (another resize: ORANGE). One column, 4.4 wide each.
    .cards (each .frame .text .gears)"""
    specs = (("web app · resize + ÷ 255", INK, (TOOL, TOOL)),
             ("phone app · no ÷ 255", ERR, (TOOL, None)),
             ("notebook · another resize", SHARED, (SHARED, TOOL)))
    cards = []
    for text, col, gs in specs:
        t = label(text, size, col)
        gl = VGroup(*[gear(0.16, c) if c else cross_glyph(0.22, ERR, 4) for c in gs]).arrange(RIGHT, buff=0.18)
        row = VGroup(gl, t).arrange(RIGHT, buff=0.22)
        fr = outline_box(max(4.6, row.width + 0.4), 0.62, LAPTOP, solid=True, fill_opacity=0.06)
        row.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.2)
        c = VGroup(fr, row)
        c.frame, c.text, c.gears = fr, t, gl
        cards.append(c)
    g = VGroup(*cards).arrange(DOWN, buff=0.14)
    g.cards = cards
    return g


# ------------------------------------------------------------------ V4 · ArtifactTrip
class ArtifactTrip(_Anchored):
    """V4 · slide 12's steps 1–3 on AWS (S06). Five nodes in one row (y 0 at the anchor, x -5.2 +
    2.6·i, each 2.15 × 1.15): 1 GREY dashed 'GitHub release · v1.0', 2 TEAL 'container · cli.py',
    3 GREEN 'SavedModel', 4 GREEN 'model.tar.gz', 5 BLUE 'S3 bucket'; arrows 1→2 … 4→5 (GREY; 4→5
    PINK). Node 0, RED 'create bucket', sits ABOVE node 1 (y 1.6) with an arrow down into it: the
    real --prepare's first step, drawn only by stop(). The row spans y -0.6..0.6 (2.2 with node 0).
    PLAYS: build(scene, upto=5, lag) nodes 1..upto with their arrows (call again to go on) ·
    marks(scene) PINK step numbers '1' (over 1→2) and '3' (over 4→5), GREY-struck '2 · signature' over
    node 3 (all at y 0.95) · stop(scene) node 0 + its arrow + a RED cross, nodes 1-5 dim · resume(scene)
    undims, the cross goes · wall(scene, text='not sent') a RED wall across 4→5 · unfold(scene) a
    GREEN card under node 3: saved_model.pb (the graph · named entry points · serving_default),
    variables/ (the weights), fingerprint.pb, assets/ · version(scene) chips '1/' under nodes 3 and 4 +
    a GREY 'TF Serving: <name>/<version>/' chip under node 4 (under the card if it is up) ·
    uri(scene) the PINK dashed S3 URI under the row, right-aligned (10.5 wide).
    .nodes[i] (.frame .text) .arrows[i] (i→i+1; 0 = node 0 → node 1) .card .uri_text"""

    XS = (-5.2, -5.2, -2.6, 0.0, 2.6, 5.2)
    YS = (1.75, 0, 0, 0, 0, 0)
    SPECS = (("create bucket", ERR, True), ("GitHub release\nv1.0", PAST, False),
             ("container\ncli.py", IMAGE, True), ("SavedModel", OWN, True), ("model.tar.gz", OWN, True),
             ("S3 bucket", CLOUD, True))

    def __init__(self, **kw):
        super().__init__(**kw)
        self.nodes, self.arrows = [], {}
        for i, (text, col, solid) in enumerate(self.SPECS):
            fr = outline_box(2.15, 1.15 if i else 0.62, col, solid=solid, fill_opacity=0.1)
            fr.move_to(self.p(self.XS[i], self.YS[i]))
            rows = text.split("\n")
            mk = mono if i == 4 else label
            t = VGroup(*[mk(r, 20, INK if k == 0 else S.GREY) for k, r in enumerate(rows)]).arrange(DOWN, buff=0.08)
            t.move_to(fr)
            n = VGroup(fr, t)
            n.frame, n.text = fr, t
            self.nodes.append(n)
        for i in range(1, 5):
            a = arrow(self.nodes[i].frame.get_right(), self.nodes[i + 1].frame.get_left(),
                      ROUTE if i == 4 else S.GREY, stroke=3, buff=0.05)
            self.arrows[i] = a
        self.arrows[0] = arrow(self.nodes[0].frame.get_bottom(), self.nodes[1].frame.get_top(), ERR, stroke=3,
                               buff=0.05)
        self.cross = self.card = self.uri_text = self.wall_g = self.step_marks = self.version_g = None
        self.built = 0

    def build(self, scene, upto: int = 5, lag: float = 0.6):
        for i in range(max(1, self.built + 1), upto + 1):
            mobs = [self.nodes[i]] + ([self.arrows[i - 1]] if i >= 2 else [])
            self.show(scene, *mobs, anims=[FadeIn(self.nodes[i], shift=RIGHT * 0.2)]
                      + ([GrowArrow(self.arrows[i - 1])] if i >= 2 else []), run_time=lag)
            self.built = i

    def marks(self, scene, run_time: float = 0.6):
        def num(s):
            c = Circle(radius=0.2, stroke_color=ROUTE, stroke_width=3).set_fill(S.BG, 1)
            return VGroup(c, label(s, 20, ROUTE).move_to(c))
        m1 = num("1").move_to(self.arrows[1].get_center() + UP * 0.95)
        m3 = num("3").move_to(self.arrows[4].get_center() + UP * 0.95)
        st = grey_chip("2 · signature").move_to(self.nodes[3].frame.get_top() + UP * 0.38)
        stk = strike(st, S.GREY)
        g = VGroup(m1, m3, st, stk)
        self.step_marks = g
        return self.show(scene, g, run_time=run_time)

    def _dim(self, op: float) -> list:
        fam = self.get_family()
        anims = []
        for n in self.nodes[1:6]:
            if n in fam:
                anims += [n.text.animate.set_opacity(op), n.frame.frame.animate.set_stroke(opacity=op)]
        anims += [self.arrows[k].animate.set_opacity(op) for k in range(1, 5) if self.arrows[k] in fam]
        return anims

    def stop(self, scene, run_time: float = 0.8):
        a0 = self.arrows[0]
        x = cross_glyph(0.3, ERR).move_to(a0).shift(RIGHT * 0.3)
        self.cross = x
        self.show(scene, self.nodes[0], a0, x, anims=[FadeIn(self.nodes[0], shift=DOWN * 0.2), GrowArrow(a0),
                                                       FadeIn(x)], extra=self._dim(0.3), run_time=run_time)

    def resume(self, scene, run_time: float = 0.6):
        anims = self._dim(1.0)
        if self.cross is not None:
            self.drop(scene, self.cross, extra=anims, run_time=run_time)
            self.cross = None
        elif anims:
            scene.play(*anims, run_time=run_time)

    def wall(self, scene, text: str = "not sent", run_time: float = 0.6):
        a = self.arrows[4]
        w = Rectangle(width=0.12, height=1.2, stroke_width=0).set_fill(ERR, 0.9).move_to(a.get_center())
        t = label(text, 20, ERR).next_to(w, DOWN, buff=0.12)
        self.wall_g = VGroup(w, t)
        return self.show(scene, w, t, run_time=run_time)

    def unfold(self, scene, run_time: float = 1.0):
        rows = [("saved_model.pb", "the graph · named entry points · serving_default"),
                ("variables/", "the weights"), ("fingerprint.pb", ""), ("assets/", "")]
        items = VGroup()
        for name, what in rows:
            r = VGroup(file_glyph(0.3, OWN), mono(name, 20, INK))
            if what:
                r.add(label(what, 20, S.GREY))
            r.arrange(RIGHT, buff=0.16)
            items.add(r)
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        fr = outline_box(items.width + 0.6, items.height + 0.45, OWN, solid=True, fill_opacity=0.06)
        items.move_to(fr)
        c = VGroup(fr, items).next_to(self.nodes[3].frame, DOWN, buff=0.5)
        keep_inside(c)
        link = DashedLine(self.nodes[3].frame.get_bottom(), c.get_top(), color=OWN, stroke_width=2.5)
        self.card = VGroup(link, c)
        return self.show(scene, self.card, anims=[Create(link), FadeIn(c, shift=DOWN * 0.2)], run_time=run_time)

    def version(self, scene, run_time: float = 0.8):
        c3 = chip("1/", OWN, size=20, font=MONO).next_to(self.nodes[3].frame, DOWN, buff=0.06)
        c3.align_to(self.nodes[3].frame, RIGHT)
        c4 = chip("1/ inside", OWN, size=20, font=MONO).next_to(self.nodes[4].frame, DOWN, buff=0.06)
        c4.align_to(self.nodes[4].frame, LEFT)
        n = grey_chip("TF Serving: <name>/<version>/", mono_font=True)
        n.next_to(self.card if self.card is not None else self.nodes[4].frame, DOWN, buff=0.25)
        if self.card is None:
            n.align_to(self.nodes[4].frame, RIGHT)
        keep_inside(n)
        g = VGroup(c3, c4, n)
        self.version_g = g
        return self.show(scene, g, anims=[FadeIn(c3, shift=DOWN * 0.15), FadeIn(c4, shift=DOWN * 0.15),
                                          FadeIn(n)], run_time=run_time)

    def uri(self, scene, text: str = S3_URI_A, run_time: float = 0.6):
        t = mono(text, 20, ROUTE).next_to(self.nodes[5].frame, DOWN, buff=0.3).align_to(self.nodes[5].frame, RIGHT)
        keep_inside(t)
        ul = DashedLine(t.get_corner(DL) + DOWN * 0.06, t.get_corner(DR) + DOWN * 0.06, color=ROUTE, stroke_width=2)
        self.uri_text = VGroup(t, ul)
        return self.show(scene, self.uri_text, run_time=run_time)


# ------------------------------------------------------------------ V5 · ThreeObjects
class ThreeObjects(_Anchored):
    """V5 · Model, endpoint configuration, endpoint (S01 preview, S07 built, S09 clean-up, S15
    reprise). Built centred: three dashed slots (3.4 × 1.4) at y 0.9, x -4.3 / 0 / 4.3 ('artifact ·
    which model' GREEN, 'container · what runs it' TEAL, 'machine · where it runs' BLUE; captions at
    y -0.1). slots=False starts empty (call slots()).
    PLAYS: slots(scene, i=None) · lane(scene) a PINK dashed request lane above the slots (y 2.05; after
    deploy(): into the endpoint plate, y -0.55) · zero(scene) a GREY '0 requests' chip on the lane ·
    meter(scene) a GOLD CostDial under the machine slot (after deploy(): right of the plate) ·
    run(scene, turns, secs) sweeps it · model_card(scene) slots 0-1 become a GREY dashed
    'TensorFlowModel' card (x -6.45..1.85, y -0.4..2.3) with sub-slots artifact (PINK
    's3://…/model.tar.gz') and container (TEAL 'TF Serving 2.13') on top, role (empty, full width)
    under them · fill_role(scene, name) the BLUE badge drops in · solidify(scene) the card turns into
    the BLUE 'Model · in SageMaker' card · registry(scene) / unregistry(scene) the GREY dashed 'Model
    Registry (the lecture)' box above it (y 2.75: no tracker on screen then, or shift the piece down)
    · deploy(scene) the machine slot becomes the endpoint configuration card (x 4.25, y 1.35, 4.1
    wide) + the endpoint plate (y -0.55) with its machine and dial under it (down to y -2.4) · delete(scene, which) 'endpoint' (the dial freezes, the plate goes) | 'config'
    | 'model' | 'artifact' · swap_config(scene, text) a new configuration slides in behind the same
    plate (S15's update_endpoint). .slot_list .slot_caps .card .sub (dict artifact/container/role)
    .config .ep (endpoint_plate) .dial .lane_g .registry_g"""

    XS = (-4.3, 0.0, 4.3)
    Y = 0.9
    SPECS = (("artifact · which model", OWN), ("container · what runs it", IMAGE),
             ("machine · where it runs", CLOUD))

    def __init__(self, slots: bool = True, **kw):
        super().__init__(**kw)
        self.slot_list, self.slot_caps = [], []
        for x, (cap, col) in zip(self.XS, self.SPECS):
            s = outline_box(3.4, 1.4, col, solid=False).move_to(self.p(x, self.Y))
            c = label(cap, 22, col).next_to(s, DOWN, buff=0.15)
            self.slot_list.append(s)
            self.slot_caps.append(c)
        self.card = self.config = self.ep = self.dial = self.lane_g = self.registry_g = None
        self.sub = {}
        if slots:
            self.add(*self.slot_list, *self.slot_caps)

    def slots(self, scene, i: int | None = None, run_time: float = 0.6):
        idx = range(3) if i is None else [i]
        mobs = [m for k in idx for m in (self.slot_list[k], self.slot_caps[k]) if m not in self.submobjects]
        return self.show(scene, *mobs, run_time=run_time)

    def _drop_lane(self, scene):
        olds = [m for m in (self.lane_g, getattr(self, "zero_chip", None)) if m is not None]
        if olds:
            self.drop(scene, *olds, run_time=0.3)
        self.lane_g = self.zero_chip = None

    def lane(self, scene, run_time: float = 0.6):
        """PLAYS (a lane already up is replaced)."""
        self._drop_lane(scene)
        if self.ep is not None:
            y = self.ep.plate.get_center()[1] - self.ref.get_center()[1]
            ln = DashedLine(self.p(-6.3, y), self.ep.plate.get_left() + LEFT * 0.1, color=ROUTE, stroke_width=3)
            t = label("requests", 20, ROUTE).next_to(ln.get_start(), DOWN, buff=0.1).align_to(ln, LEFT)
        else:
            ln = DashedLine(self.p(-6.3, 2.05), self.p(6.2, 2.05), color=ROUTE, stroke_width=3)
            t = label("requests", 20, ROUTE).next_to(ln.get_start(), UP, buff=0.08).align_to(ln, LEFT)
        self.lane_g = VGroup(ln, t)
        return self.show(scene, self.lane_g, anims=[Create(ln), FadeIn(t)], run_time=run_time)

    def zero(self, scene, run_time: float = 0.5):
        c = grey_chip("0 requests").move_to(self.lane_g[0].get_center())
        self.zero_chip = c
        self.show(scene, c, run_time=run_time * 0.5)
        scene.play(Indicate(c.text, color=S.GREY), run_time=run_time * 0.5)
        return c

    def meter(self, scene, run_time: float = 0.5):
        if self.ep is not None and self.ep.dial is not None:
            self.dial = self.ep.dial
            return self.dial
        d = CostDial(0.5).move_to(self.p(self.XS[2], -1.05))
        self.dial = d
        return self.show(scene, d, run_time=run_time)

    def run(self, scene, turns: float = 0.5, seconds: float = 2.0, extra=()):
        self.dial.run(scene, turns, seconds, extra=extra)

    def model_card(self, scene, run_time: float = 1.2):
        """PLAYS (the S01 request lane, if still up, goes first: the card covers its row)."""
        self._drop_lane(scene)
        fr = outline_box(8.3, 2.75, S.GREY, solid=False).move_to(self.p(-2.3, 0.95))
        tt = mono("TensorFlowModel", 22, INK).move_to(fr.get_corner(UL) + np.array([0.25, -0.3, 0]), aligned_edge=LEFT)
        specs = (("artifact", ROUTE, 3.75, (-4.35, 1.15)), ("container", IMAGE, 3.75, (-0.25, 1.15)),
                 ("role", ROLE, 7.85, (-2.3, 0.0)))
        boxes, caps = [], []
        for nm, col, w, (x, y) in specs:
            b = outline_box(w, 0.95, col, solid=False).move_to(self.p(x, y))
            c = label(nm, 20, S.GREY).move_to(b.get_corner(UL) + np.array([0.15, -0.2, 0]), aligned_edge=LEFT)
            boxes.append(b)
            caps.append(c)
        art = mono("s3://…/model.tar.gz", 20, ROUTE).move_to(boxes[0]).shift(DOWN * 0.13)
        ctr = label("TF Serving 2.13", 22, IMAGE).move_to(boxes[1]).shift(DOWN * 0.13)
        olds = [self.slot_list[0], self.slot_list[1], self.slot_caps[0], self.slot_caps[1]]
        for m in olds:
            self._detach(m)
        scene.add(*olds)
        scene.play(ReplacementTransform(self.slot_list[0], boxes[0]), ReplacementTransform(self.slot_list[1], boxes[1]),
                   ReplacementTransform(self.slot_caps[0], caps[0]), ReplacementTransform(self.slot_caps[1], caps[1]),
                   FadeIn(fr), FadeIn(tt), FadeIn(boxes[2]), FadeIn(caps[2]), run_time=run_time * 0.6)
        scene.remove(*boxes, *caps, fr, tt)
        card = VGroup(fr, tt, *boxes, *caps)
        card.frame, card.title = fr, tt
        self.add(card)
        self.show(scene, art, ctr, anims=[FadeIn(art, shift=DOWN * 0.2), FadeIn(ctr, shift=DOWN * 0.2)],
                  into=card, run_time=run_time * 0.4)
        self.card = card
        self.sub = {"artifact": VGroup(boxes[0], caps[0], art), "container": VGroup(boxes[1], caps[1], ctr),
                    "role": VGroup(boxes[2], caps[2])}
        return card

    def fill_role(self, scene, name: str = ROLE_A, run_time: float = 0.7):
        b = role_badge(name).move_to(self.sub["role"][0])
        start = b.copy().shift(UP * 1.0).set_opacity(0)
        self.show(scene, b, anims=[ReplacementTransform(start, b)], into=self.card, run_time=run_time)
        self.sub["role"].add(b)
        return b

    def solidify(self, scene, run_time: float = 0.8):
        fr = self.card.frame
        new = outline_box(fr.width, fr.height, CLOUD, solid=True, fill_opacity=0.08).move_to(fr)
        tt = label("Model · in SageMaker", 22, CLOUD).move_to(self.card.title, aligned_edge=LEFT)
        self.swap(scene, fr, new, run_time=run_time * 0.5, extra=[])
        self.swap(scene, self.card.title, tt, run_time=run_time * 0.5)
        self.card.frame, self.card.title = new, tt
        return new

    def registry(self, scene, run_time: float = 0.6):
        t = label("Model Registry (the lecture)", 22, PAST)
        fr = outline_box(t.width + 0.6, 0.7, PAST, solid=False)
        fr.move_to(self.p(-2.3, 2.75))
        t.move_to(fr)
        a = arrow(fr.get_bottom(), self.card.frame.get_top(), PAST, buff=0.05)
        self.registry_g = VGroup(fr, t, a)
        return self.show(scene, self.registry_g, run_time=run_time)

    def unregistry(self, scene, run_time: float = 0.4):
        if self.registry_g is not None:
            self.drop(scene, self.registry_g, run_time=run_time)
            self.registry_g = None

    def deploy(self, scene, name: str = "…-endpoint-<timestamp>", run_time: float = 1.6):
        rows = VGroup(label("endpoint configuration", 22, CLOUD), mono("variant AllTraffic", 20, INK),
                      mono(f"{INSTANCE_A} · count 1", 20, INK), mono("weight 1", 20, INK))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        fr = outline_box(max(4.1, rows.width + 0.45), rows.height + 0.4, CLOUD, solid=True,
                         fill_opacity=0.08).move_to(self.p(4.25, 1.35))
        rows.move_to(fr)
        cfg = VGroup(fr, rows)
        cfg.frame, cfg.rows = fr, rows
        ep = endpoint_plate(name, meter=True, plate_w=4.1)
        ep.shift(self.p(4.25, -0.55) - ep.plate.get_center())
        old, oc = self.slot_list[2], self.slot_caps[2]
        prev_dial = self.dial
        gone = [m for m in (old, oc, prev_dial) if m is not None]
        if prev_dial is not None:
            prev_dial.freeze()
        for m in gone:
            self._detach(m)
        scene.add(*gone)
        scene.play(ReplacementTransform(old, fr), FadeOut(oc), FadeIn(rows),
                   *([FadeOut(prev_dial)] if prev_dial is not None else []), run_time=run_time * 0.5)
        scene.remove(*gone, fr, rows)
        self.add(cfg)
        self.config = cfg
        self.show(scene, ep, anims=[FadeIn(ep.plate, shift=DOWN * 0.2), FadeIn(ep.text),
                                    FadeIn(ep.rack, shift=UP * 0.3), FadeIn(ep.machine), FadeIn(ep.dial)],
                  run_time=run_time * 0.5)
        self.ep, self.dial = ep, ep.dial
        return cfg, ep

    def delete(self, scene, which: str, run_time: float = 0.6):
        if which == "endpoint":
            if self.dial is not None:
                self.dial.freeze()
            parts = [m for m in (self.ep.plate, self.ep.text, self.ep.rack, self.ep.machine) if m is not None]
            for m in parts:
                self._detach(m)
            scene.add(*parts)
            scene.play(*[FadeOut(m) for m in parts], self.dial.face.animate.set_stroke(S.GREY),
                       run_time=run_time)
            scene.remove(*parts)
            self.heal(scene)
        elif which == "config":
            self.drop(scene, self.config, shift=DOWN * 0.3, run_time=run_time)
            self.config = None
        elif which == "model":
            keep = self.sub.get("artifact")
            parts = [m for m in self.card.submobjects if keep is None or m not in keep.submobjects]
            self.drop(scene, *parts, shift=DOWN * 0.3, run_time=run_time)
        elif which == "artifact":
            a = self.sub["artifact"]
            s_ = strike(a[2], ERR)
            scene.play(Create(s_), run_time=run_time * 0.4)
            self.drop(scene, *a, run_time=run_time * 0.6)
            scene.remove(s_)
        else:
            raise ValueError(which)

    def swap_config(self, scene, text: str = "new configuration", run_time: float = 0.8):
        rows = VGroup(label("endpoint configuration", 22, CLOUD), label(text, 20, TURN))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        fr = outline_box(3.9, self.config.frame.height, CLOUD, solid=True, fill_opacity=0.08).move_to(self.config)
        rows.move_to(fr)
        new = VGroup(fr, rows)
        new.frame, new.rows = fr, rows
        self.drop(scene, self.config, shift=RIGHT * 0.5, run_time=run_time * 0.5)
        self.show(scene, new, anims=[FadeIn(new, shift=RIGHT * 0.5)], run_time=run_time * 0.5)
        self.config = new
        return new


# ------------------------------------------------------------------ V6 · ManualToPipeline
class ManualToPipeline(_Anchored):
    """V6 · four people, four terminals (S10; small reprise in S01 and S09). Built centred: a
    headline (y 2.35, built empty), four GREY stage tiles (2.8 × 1.0) at y 1.0, x -4.8 / -1.6 / 1.6 /
    4.8 (STAGE_TILES), GREY two-headed arrows between them; people=True adds a GREY person + 'CLI'
    chip under each tile (y -0.55 / -1.25).
    PLAYS: headline(scene, text) types or rewrites the headline · people_in(scene) · orchestrator(scene,
    text) one BLUE 'SageMaker Pipelines' box (x -1.4, y -1.0) replaces the people · vertex(scene) a
    GREY dashed 'Vertex AI Pipelines · Kubeflow' box (x 3.9) beside it with '≈' · notes(scene, texts)
    one chip under each tile (y 0.15; ≤ 2.9 wide) · chain(scene) PINK edges replace the GREY arrows ·
    frame(scene, text='pipeline') a BLUE frame closes around the four tiles · tick(scene, i) a GREEN
    tick on tile i · light(scene, i, color) (PLAYS) tile i pulses. .tiles .links .people .head_text
    .box_o .box_v .frame_g .note_chips"""

    XS = (-4.8, -1.6, 1.6, 4.8)

    def __init__(self, people: bool = True, names=STAGE_TILES, **kw):
        super().__init__(**kw)
        self.tiles = []
        for x, n in zip(self.XS, names):
            fr = outline_box(2.8, 1.0, LAPTOP, solid=True, fill_opacity=0.08).move_to(self.p(x, 1.0))
            t = label(n, 22, INK).move_to(fr)
            tl = VGroup(fr, t)
            tl.frame, tl.text = fr, t
            self.tiles.append(tl)
        self.links = VGroup(*[DoubleArrowLike(self.tiles[i].frame.get_right(), self.tiles[i + 1].frame.get_left())
                              for i in range(3)])
        self.people = VGroup()
        for x in self.XS:
            pr = person_icon(LAPTOP, 0.5).move_to(self.p(x, -0.5))
            c = chip("CLI", LAPTOP, size=20, font=MONO).next_to(pr, DOWN, buff=0.15)
            self.people.add(VGroup(pr, c))
        self.head_text = self.box_o = self.box_v = self.frame_g = self.edges = None
        self.note_chips = []
        self.add(*self.tiles, self.links)
        if people:
            self.add(self.people)

    def headline(self, scene, text: str = "How do we execute these steps?", run_time: float = 0.8):
        t = label(text, 28, INK).move_to(self.p(0, 2.35))
        if self.head_text is None:
            self.head_text = t
            return self.show(scene, t, anims=[ShowIncreasingSubsets(t, rate_func=linear)], run_time=run_time)
        new = self.swap(scene, self.head_text, t, run_time=run_time)
        self.head_text = new
        return new

    def people_in(self, scene, run_time: float = 0.8):
        if self.people not in self.submobjects:
            self.show(scene, self.people, anims=[LaggedStart(*[FadeIn(p, shift=UP * 0.2) for p in self.people],
                                                             lag_ratio=0.2)], run_time=run_time)

    def orchestrator(self, scene, text: str = "SageMaker Pipelines", run_time: float = 1.0):
        t = label(text, 26, CLOUD)
        fr = outline_box(max(4.6, t.width + 0.8), 0.95, CLOUD, solid=True, fill_opacity=0.12)
        fr.move_to(self.p(-1.4, -1.0))
        t.move_to(fr)
        self.box_o = VGroup(fr, t)
        if self.people in self.submobjects:
            self.drop(scene, self.people, run_time=run_time * 0.4)
        return self.show(scene, self.box_o, anims=[FadeIn(self.box_o, shift=UP * 0.3)], run_time=run_time * 0.6)

    def vertex(self, scene, text: str = "Vertex AI Pipelines · Kubeflow", run_time: float = 0.6):
        t = label(text, 22, PAST)
        fr = outline_box(t.width + 0.5, 0.8, PAST, solid=False)
        fr.move_to(self.p(4.0, -1.0))
        t.move_to(fr)
        if self.box_o is not None and fr.get_left()[0] < self.box_o[0].get_right()[0] + 0.5:
            dx = self.box_o[0].get_right()[0] + 0.55 - fr.get_left()[0]
            VGroup(fr, t).shift(RIGHT * dx)
        approx = label("≈", 28, S.GREY).move_to((fr.get_left() + self.box_o[0].get_right()) / 2)
        self.box_v = VGroup(fr, t, approx)
        keep_inside(self.box_v)
        return self.show(scene, self.box_v, run_time=run_time)

    def notes(self, scene, texts, run_time: float = 0.8):
        cs = []
        for x, s in zip(self.XS, texts):
            c = grey_chip(s).move_to(self.p(x, 0.12))
            cs.append(c)
        self.note_chips = cs
        return self.show(scene, *cs, anims=[LaggedStart(*[FadeIn(c) for c in cs], lag_ratio=0.2)], run_time=run_time)

    def chain(self, scene, run_time: float = 0.8):
        es = VGroup(*[Arrow(self.tiles[i].frame.get_right(), self.tiles[i + 1].frame.get_left(), buff=0.04,
                            color=ROUTE, stroke_width=5, tip_length=0.16, max_tip_length_to_length_ratio=0.5)
                      for i in range(3)])
        self.edges = es
        self.swap(scene, self.links, es, run_time=run_time)
        return es

    def frame(self, scene, text: str = "pipeline", run_time: float = 0.8):
        g = VGroup(*self.tiles, *self.note_chips)
        fr = outline_box(g.width + 0.5, g.height + 0.75, CLOUD, solid=True, fill_opacity=0.04, radius=0.2)
        fr.move_to(g).shift(UP * 0.17)
        t = label(text, 22, CLOUD).move_to(fr.get_corner(UL) + np.array([0.2, -0.2, 0]), aligned_edge=LEFT)
        self.frame_g = VGroup(fr, t)
        self.show(scene, self.frame_g, anims=[Create(fr.frame), FadeIn(fr.fill), FadeIn(t)], run_time=run_time)
        self.submobjects.remove(self.frame_g)
        self.submobjects.insert(1, self.frame_g)
        return self.frame_g

    def tick(self, scene, i: int, run_time: float = 0.4):
        c = check_glyph(0.3, OWN).next_to(self.tiles[i].frame, UP, buff=0.06)
        return self.show(scene, c, anims=[Create(c)], run_time=run_time)

    def light(self, scene, i: int, color=TURN, run_time: float = 0.6):
        scene.play(self.tiles[i].frame.frame.animate(rate_func=there_and_back).set_stroke(color, 5),
                   Indicate(self.tiles[i].text, color=color, scale_factor=1.06), run_time=run_time)


def DoubleArrowLike(a, b, color=S.GREY):  # noqa: N802
    """A thin GREY two-headed arrow between two points (V6's manual hand-offs)."""
    from manim import DoubleArrow
    return DoubleArrow(a, b, buff=0.05, color=color, stroke_width=3, tip_length=0.14,
                       max_tip_length_to_length_ratio=0.5)


# ------------------------------------------------------------------ V7 · CallableImage
class CallableImage(_Anchored):
    """V7 · one image, two modes (S11 built, S14 reprise). Built centred (y -1.1..1.1; plug() and
    badge() add down to y -2.3): the input chip 'arguments?' (left edge x -6.45), a YELLOW switch at
    the image's left edge, the TEAL image (x -1.8, 4.5 × 2.2) named `name` with
    'docker-entrypoint.sh' inside, two branch arrows to the cards on the right (x 4.15, 4.6 wide):
    GREY 'development · exec bash' / 'a shell (you are here)' at y 1.05 and BLUE 'production ·
    exec "$@"' / 'run the command, exit' at y -1.05.
    PLAYS: build(scene) (when built=False) · choose(scene, 'dev'|'prod') the switch points at a
    branch, its card lights · plug(scene, cmd, by) a BLUE arrow labelled `by` comes down onto the input
    and a mono command chip replaces 'arguments?', the switch goes to production · badge(scene, name)
    a BLUE role badge under the production card. .image .switch .input .cards {'dev','prod'} .branches
    .cmd_chip .badge_g"""

    def __init__(self, name: str = "cheese-app-data-collector", built: bool = True, **kw):
        super().__init__(**kw)
        fr = RoundedRectangle(width=4.5, height=2.2, corner_radius=0.14, stroke_color=IMAGE,
                              stroke_width=3).set_fill(IMAGE, 0.12).move_to(self.p(-1.8, 0))
        nt = mono(name, 20, INK).move_to(fr.get_top() + DOWN * 0.35)
        ep = mono("docker-entrypoint.sh", 20, IMAGE).move_to(fr).shift(DOWN * 0.15)
        self.image = VGroup(fr, nt, ep)
        self.image.frame = fr
        self.pivot = fr.get_left() + RIGHT * 0.05
        self.switch = Line(self.pivot + LEFT * 0.55, self.pivot, color=TURN, stroke_width=5)
        self.input = grey_chip("arguments?").next_to(self.switch, LEFT, buff=0.08)
        self.cards, self.branches = {}, {}
        for key, y, col, a, b in (("dev", 1.05, LAPTOP, "development · exec bash", "a shell (you are here)"),
                                  ("prod", -1.05, CLOUD, 'production · exec "$@"', "run the command, exit")):
            rows = VGroup(label(a, 22, col), label(b, 20, INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            cf = outline_box(4.6, rows.height + 0.4, col, solid=True, fill_opacity=0.06).move_to(self.p(4.15, y))
            rows.move_to(cf).align_to(cf, LEFT).shift(RIGHT * 0.25)
            c = VGroup(cf, rows)
            c.frame, c.rows = cf, rows
            self.cards[key] = c
            self.branches[key] = arrow(fr.get_right() + UP * 0.25 * np.sign(y), cf.get_left(), col, stroke=3)
        self.cmd_chip = self.badge_g = None
        self.mode = None
        self.parts = VGroup(self.input, self.switch, self.image, *self.branches.values(), *self.cards.values())
        if built:
            self.add(self.parts)

    def build(self, scene, run_time: float = 1.2):
        if self.parts in self.submobjects:
            return
        self.show(scene, self.parts, anims=[LaggedStart(FadeIn(self.image), FadeIn(self.input), FadeIn(self.switch),
                                                        *[GrowArrow(b) for b in self.branches.values()],
                                                        *[FadeIn(c) for c in self.cards.values()], lag_ratio=0.15)],
                  run_time=run_time)

    def choose(self, scene, mode: str = "dev", run_time: float = 0.6):
        other = "prod" if mode == "dev" else "dev"
        ang = 0.45 if mode == "dev" else -0.45
        target = Line(self.pivot + LEFT * 0.55, self.pivot, color=TURN, stroke_width=5).rotate(ang, about_point=self.pivot)
        col = self.cards[mode].frame.frame.get_stroke_color()
        scene.play(Transform(self.switch, target),
                   self.cards[mode].frame.fill.animate.set_fill(opacity=0.22),
                   self.cards[other].frame.fill.animate.set_fill(opacity=0.03),
                   self.branches[mode].animate.set_stroke(width=5),
                   self.branches[other].animate.set_stroke(width=2), run_time=run_time)
        scene.play(Indicate(self.cards[mode].rows[0], color=col, scale_factor=1.05), run_time=0.4)
        self.mode = mode

    def plug(self, scene, cmd: str = "python3 /app/cli.py …", by: str = "SageMaker", run_time: float = 1.4):
        """PLAYS: a BLUE command chip (mono) appears under the image's left end, a BLUE arrow labelled
        `by` runs from it to the switch, 'arguments?' fades, and the switch flips to production."""
        c = chip(cmd, CLOUD, size=20, font=MONO)
        c.next_to(self.image.frame, DOWN, buff=0.45).align_to(self.input, LEFT)
        keep_inside(c)
        a = Arrow(c.get_top() + RIGHT * 0.3, self.switch.get_start() + DOWN * 0.05, buff=0.08, color=CLOUD,
                  stroke_width=4, tip_length=0.18)
        t = label(by, 22, CLOUD).next_to(c, RIGHT, buff=0.2)
        keep_inside(t)
        self.show(scene, c, anims=[FadeIn(c, shift=UP * 0.3)], run_time=run_time * 0.3)
        self.show(scene, a, t, anims=[GrowArrow(a), FadeIn(t)], run_time=run_time * 0.3)
        self.drop(scene, self.input, run_time=0.2)
        self.input = c
        self.cmd_chip = VGroup(c, a, t)
        self.choose(scene, "prod", run_time=run_time * 0.3)
        return self.cmd_chip

    def badge(self, scene, name: str = ROLE_SM, run_time: float = 0.6):
        b = role_badge(name).next_to(self.cards["prod"].frame, DOWN, buff=0.15)
        keep_inside(b)
        self.badge_g = b
        return self.show(scene, b, anims=[GrowFromCenter(b)], run_time=run_time)


# ------------------------------------------------------------------ V8 · ReferenceDAG
class ReferenceDAG(_Anchored):
    """V8 · a pipeline drawn by references (S15 built, S16 recap). Five step boxes (STEP_NAMES,
    pending: WHITE outline, 2.2 × 0.62, names in the label font). layout: 'pile' (the column's slots
    shuffled and pushed right: x 1.4..4.0), 'column' (x 2.5, y 2.2 - 1.1·i, PINK edges downward;
    chips to the right of the boxes reach x 6.55) or 'row' (y 0.6, x -5.2 + 2.6·i). All positions are relative to
    the anchor: shift the piece to make room (code panels are near full width at 22 pt: put them
    above or below, or use font_size=20 and a short excerpt).
    PLAYS: edge(scene, i, j=i+1) boxes i and j settle into their column slots (a box in the way swaps
    out) and a PINK solid edge draws i→j (after the 4th edge the pile is a column) · relayout(scene, layout) re-lays the boxes and edges ('column' | 'row') · cache(scene,
    which=(0, 1, 2, 4), none=3) a 'cached · 30d' chip settles on box 0 and copies to the others; box
    `none` gets 'no cache_config' · states(scene, {i: state}) step_state for several boxes ·
    pulse(scene) the edges flash · drawer(scene) (row layout) the BLUE bucket under the row (y -2.65
    ..-0.85): empty dashed trays under steps 0-2 (declared outputs, y -1.2) + GREY chip 'declared
    outputs · empty' (y -0.42); then files(scene) GREY dashed raw.zip, clean.zip, tfrecords.zip drop
    into the bucket root by name (y -2.05, x 0.2..5.6) ·
    unknown(scene, i=2) a GREY '?' chip on box i's input · note(scene, text) a chip under the drawer.
    ANIM: state(i, s) (= step_state(boxes[i], s)). .boxes .edges {(i, j): Arrow} .chips .bucket_g
    .files_g .layout"""

    PERM = (2, 4, 0, 3, 1)                      # pile: box i sits in column slot PERM[i] ...
    JITTER = (0.4, 0.1, 0.35, 0.2, 0.3)        # ... pushed right by JITTER[i] (never left: code panels)
    COL_X = 2.5
    ROW_X0, ROW_DX, ROW_Y = -5.2, 2.6, 0.6

    def __init__(self, layout: str = "pile", names=STEP_NAMES, **kw):
        super().__init__(**kw)
        self.boxes = [step_box(n) for n in names]
        self.edges = {}
        self.bucket_g = self.files_g = None
        self.layout = layout
        self.slot_of = list(self.PERM) if layout == "pile" else list(range(len(self.boxes)))
        self.chips = []
        for i, b in enumerate(self.boxes):
            b.move_to(self.pos(i, layout))
        self.add(*self.boxes)

    def pos(self, i: int, layout: str | None = None) -> np.ndarray:
        layout = layout or self.layout
        if layout == "pile":
            k = self.slot_of[i]
            if k == i and getattr(self, "_settled", None) and i in self._settled:
                return self.p(self.COL_X, 2.2 - 1.1 * i)
            return self.p(self.COL_X + self.JITTER[i], 2.2 - 1.1 * k)
        if layout == "column":
            return self.p(self.COL_X, 2.2 - 1.1 * i)
        if layout == "row":
            return self.p(self.ROW_X0 + self.ROW_DX * i, self.ROW_Y)
        raise ValueError(layout)

    def _edge(self, i: int, j: int) -> Arrow:
        a, b = self.boxes[i].frame, self.boxes[j].frame
        if self.layout == "row":
            s, e = a.get_right(), b.get_left()
        else:
            s, e = a.get_bottom(), b.get_top()
        return Arrow(s, e, buff=0.04, color=EDGE, stroke_width=5,
                     tip_length=0.16, max_tip_length_to_length_ratio=0.5)

    def _settle(self, i: int) -> list:
        """Animations that bring box i to column slot i; the box sitting there swaps to i's old slot."""
        self._settled = getattr(self, "_settled", set())
        anims = []
        if self.slot_of[i] != i:
            k = self.slot_of.index(i)
            self.slot_of[k], self.slot_of[i] = self.slot_of[i], i
            anims += self._to(k, self.pos(k, "pile"))
        self._settled.add(i)
        anims += self._to(i, self.p(self.COL_X, 2.2 - 1.1 * i))
        return anims

    def _to(self, i: int, pt) -> list:
        """Animations moving box i (by its frame's centre) to pt; its chips travel with it."""
        d = pt - self.boxes[i].frame.get_center()
        return [self.boxes[i].animate.shift(d)] + [c.animate.shift(d) for c in self.chips if c.owner == i]

    def edge(self, scene, i: int, j: int | None = None, run_time: float = 1.0):
        j = i + 1 if j is None else j
        if self.layout == "pile":
            moves = self._settle(i) + self._settle(j)
            if len(getattr(self, "_settled", ())) == len(self.boxes):
                self.layout = "column"
        else:
            moves = self._to(j, self.pos(j))
        if moves and any(np.linalg.norm(self.boxes[k].frame.get_center() - self.pos(k)) > 0.01 for k in (i, j)):
            scene.play(*moves, run_time=run_time * 0.5)
        e = self._edge(i, j)
        self.edges[(i, j)] = e
        return self.show(scene, e, anims=[GrowArrow(e)], run_time=run_time * 0.5)

    def _chip_owner(self):
        return [(c.owner, c) for c in self.chips]

    def relayout(self, scene, layout: str = "row", run_time: float = 1.0):
        self.layout = layout
        anims = [b.animate.shift(self.pos(i) - b.frame.get_center()) for i, b in enumerate(self.boxes)]
        targets = {}
        for (i, j), e in self.edges.items():
            a, b = self.boxes[i].frame.copy().move_to(self.pos(i)), self.boxes[j].frame.copy().move_to(self.pos(j))
            if layout == "row":
                s, t = a.get_right(), b.get_left()
            else:
                s, t = a.get_bottom(), b.get_top()
            ne = Arrow(s, t, buff=0.04, color=EDGE, stroke_width=5, tip_length=0.16, max_tip_length_to_length_ratio=0.5)
            targets[(i, j)] = ne
            anims.append(Transform(e, ne))
        for c in self.chips:
            fr = self.boxes[c.owner].frame.copy().move_to(self.pos(c.owner))
            tgt = c.copy()
            if layout == "row":
                tgt.next_to(fr, UP, buff=0.1)
            else:
                tgt.next_to(fr, RIGHT, buff=0.12)
            anims.append(c.animate.move_to(tgt))
        scene.play(*anims, run_time=run_time)
        self.heal(scene)

    def _chip_place(self, c, i):
        if self.layout == "row":
            c.next_to(self.boxes[i].frame, UP, buff=0.1)
        else:
            c.next_to(self.boxes[i].frame, RIGHT, buff=0.12)
        return c

    def cache(self, scene, which=(0, 1, 2, 4), none: int | None = 3, run_time: float = 1.4):
        first = self._chip_place(ok_chip("cached · 30d"), which[0])
        first.owner = which[0]
        self.show(scene, first, run_time=run_time * 0.3)
        copies = []
        for i in which[1:]:
            c = self._chip_place(ok_chip("cached · 30d"), i)
            c.owner = i
            copies.append(c)
        anims = [TransformFromCopy(first, c) for c in copies]
        nc = None
        if none is not None:
            nc = self._chip_place(grey_chip("no cache_config"), none)
            nc.owner = none
            anims.append(FadeIn(nc))
        self.show(scene, *copies, *([nc] if nc else []), anims=[LaggedStart(*anims, lag_ratio=0.25)],
                  run_time=run_time * 0.7)
        self.chips = [first] + copies + ([nc] if nc else [])
        return self.chips

    def uncache(self, scene, run_time: float = 0.4):
        """PLAYS: the cache chips go."""
        if self.chips:
            self.drop(scene, *self.chips, run_time=run_time)
            self.chips = []

    def state(self, i: int, s: str, run_time: float = 0.4):
        return step_state(self.boxes[i], s, run_time)

    def states(self, scene, mapping: dict, run_time: float = 0.5):
        scene.play(*[self.state(i, s) for i, s in mapping.items()], run_time=run_time)
        self.heal(scene)

    def pulse(self, scene, run_time: float = 0.8):
        es = list(self.edges.values())
        scene.play(*[e.animate(rate_func=there_and_back).set_stroke(TURN, 8) for e in es], run_time=run_time)
        for e in es:
            e.set_stroke(EDGE, 5)
            e.tip.set_fill(EDGE).set_stroke(EDGE)

    def drawer(self, scene, run_time: float = 0.8):
        if self.layout != "row":
            raise ValueError("drawer(): relayout(scene, 'row') first")
        fr = RoundedRectangle(width=12.8, height=1.8, corner_radius=0.16, stroke_color=CLOUD,
                              stroke_width=3).set_fill(CLOUD, 0.08).move_to(self.p(0, -1.75))
        t = label("S3 bucket · root", 22, CLOUD).move_to(fr.get_corner(DL) + np.array([0.25, 0.3, 0]),
                                                        aligned_edge=LEFT)
        xs = [self.ROW_X0 + self.ROW_DX * i for i in range(3)]
        trays = VGroup(*[outline_box(1.5, 0.42, S.GREY, solid=False).move_to(self.p(x, -1.2)) for x in xs])
        lk = VGroup(*[DashedLine(self.boxes[i].frame.get_bottom(), trays[i].get_top(), color=S.GREY, stroke_width=2)
                      for i in range(3)])
        nc = grey_chip("declared outputs · empty").move_to(self.p(2.6, -0.42))
        self.bucket_g = VGroup(fr, t, trays, lk, nc)
        self.bucket_g.frame, self.bucket_g.trays = fr, trays
        return self.show(scene, self.bucket_g, run_time=run_time)

    def files(self, scene, names=("raw.zip", "clean.zip", "tfrecords.zip"), run_time: float = 1.2):
        fs = VGroup(*[dashed_chip(n, S.GREY, mono_font=True) for n in names]).arrange(RIGHT, buff=0.2)
        fs.move_to(self.p(2.9, -2.05))
        self.files_g = fs
        return self.show(scene, *fs, anims=[LaggedStart(*[FadeIn(f, shift=DOWN * 0.8) for f in fs], lag_ratio=0.3)],
                         run_time=run_time)

    def unknown(self, scene, i: int = 2, text: str = "? not verified here", run_time: float = 0.5):
        c = grey_chip(text)
        if self.layout == "row":
            c.next_to(self.boxes[i].frame, UP, buff=0.12)
        else:
            c.next_to(self.boxes[i].frame, LEFT, buff=0.12)
        keep_inside(c)
        self.unknown_chip = c
        return self.show(scene, c, run_time=run_time)

    def note(self, scene, text: str, color=S.GREY, run_time: float = 0.5):
        c = chip(text, color, size=20)
        ref = self.bucket_g if self.bucket_g is not None else VGroup(*self.boxes)
        c.next_to(ref, DOWN, buff=0.18)
        keep_inside(c)
        return self.show(scene, c, run_time=run_time)


def _small_file(name: str = "config") -> VGroup:
    """A compact GREY file card (glyph + mono name) that fits the ~/.aws drawer."""
    t = mono(name, 20, INK)
    g0 = file_glyph(0.3, LAPTOP)
    row = VGroup(g0, t).arrange(RIGHT, buff=0.12)
    fr = RoundedRectangle(width=row.width + 0.3, height=0.5, corner_radius=0.08, stroke_color=LAPTOP,
                          stroke_width=2).set_fill(S.GREY_DARKER, 1)
    row.move_to(fr)
    g = VGroup(fr, row)
    g.frame, g.text = fr, t
    return g
