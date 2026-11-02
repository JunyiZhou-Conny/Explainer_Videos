"""Shared code for AC215 L15 exam edition (ML Workflows with Vertex AI; a concept-first review for
Quiz 4, no captures, no README walkthrough): paths, narration, the semantic colours of BRIEF.md,
source / README panels quoting assets/source/<repo>/<path>, tags and cards (the generic helpers
ported unchanged from L08's tested common.py, incl. guard()), and this video's set pieces V1–V6 of
BRIEF.md plus the multiple-choice ponder and the takeaway card. Tested on screen by
build/common_test.py (CommonTest, PieceTest: explainer.check OK, preview sheets read).

Notes for scene authors
=======================

    from common import *      # every scene: SAY = NARRATION["S03"]; assert len(SAY) == n;
                              # one `with self.voiceover(SAY[i]) as vo:` per SAY line, in order
All text here is 20–30 pt. Never .scale() a group that holds text below 1.0: Piece set pieces have
.rescale(k) (shapes shrink, text keeps its size). Methods return ANIMATIONS (play them) or MOBJECTS
(placed, not added: FadeIn them) unless they say "plays". Set pieces are built centred at ORIGIN
unless they say "in place". Layout checks use guard() (raises here, only warns on the GitHub
release runner); content checks (sources, names, arithmetic) raise everywhere.

Frame budget. Safe frame x ∈ [−6.6, 6.6], y ∈ [−3.6, 3.6]. The lecture tag lref("28–29") sits top
right (y 3.13..3.6): keep the top-right corner free. No tracker, no terminals, no captures in this
video: code and README panels are evidence beside the diagrams. A code panel at 22 pt fits 65
characters a row and at most 12 rows (src_panel raises beyond); 12 rows ≈ 5.2 tall.

Data and sources
    NARRATION["S01"] … ["S08"]  SAY lines from script.md      TITLES[cls], SPEC (video.yaml)
    Sources are named by repo + path: "ml-workflow/src/workflow/cli.py",
        "ml-workflow/src/workflow/sample-pipeline1.yaml", "ml-workflow/src/workflow/pipeline.yaml",
        "ml-workflow/src/workflow/model.py", "ml-workflow/src/model-training/package/trainer/task.py",
        "ml-workflow/README.md", "model-deployment/cli.py", "model-deployment/README.md",
        "ml-workflow-aws/src/workflow/cli.py".
    source_text(path) excerpt(path, a, b) source_line(path, n) readme(repo, a, b) (plain text rows)
        md_plain(line) (README markdown -> plain text)
    NEVER shown (they raise): model-deployment/cli.py 71–83 (W&B entity), model-deployment/README.md
        136 (a person's name), sample-pipeline1.yaml 80/108/136/164/248 (old python:3.7 / kfp-2.3.0),
        model.py 4, 53, 66 (stale comments: light line 62 `sync=True,`, never 53). Every shown line is
        checked for a person's name (guard_names).
    Names / numbers: TOY ("square", "square-2", "add", "square-root") TOY_VALUES {"square": "9.0", …}
        CHEESE (the four display names) CHEESE_FILES (raw.zip, clean.zip, model/) SAGEMAKER (five
        step names) COLLECTOR_IMAGE PROCESSOR_IMAGE ENDPOINT_NAME "cheese-app-endpoint" ENDPOINT_ID
        "<ENDPOINT_ID>" (GREY) BUCKET "gs://my-bucket" (invented examples) README_PROBS KFP_ERROR
        V3_TIMES P2_MIN V4_TRAIN 50 V4_DEPLOY 10 V4_ROLLS (40, 75, 55) STEP_VARS (the five step
        variables of ml-workflow-aws/src/workflow/cli.py:322)

Colours (BRIEF.md "Colours", binding)
    LAPTOP GREY · CLOUD BLUE · CTR TEAL · CLOCK (= SYSTEM: cron, &) ORANGE · OWN (= VALUE: a task's
    value, a fresh model, the YAML, the ✓) GREEN · TOOL (kfp, aiplatform, SageMaker SDK) PURPLE · ERR
    RED · TURN (wavefront, running, ponder, takeaway) YELLOW · COST GOLD · EDGE (= LOOKUP: solid data
    wire, dashed .after() wire, the request route) PINK · STALE (dashed: last run's leftovers,
    never-run) GREY · INK white. Task states: pending WHITE outline; running YELLOW fill; succeeded
    GREEN ✓ badge at the right end; failed RED; never-run GREY dashed.

Panels and cards
    src_panel(path, a, b=None, wrap=True|{n: [...]}, focus=, join=, cut_comments=, max_rows=12)
        CODE(): header "repo/path · lines a–b"; folded: src_panel(path, [(303, 304), (311, 318)])
        (GREY '…' rows, header "(folded)"); raises when > 12 rows or > 12.9 wide.
        .bar(n, colour) (VGroup of line bars, not added) .span(n, sub) glyphs .rows_of(n)
    readme_panel(repo, a, b=None, clip={n: (start, end)}, chars=62, hi={phrase: colour})
        PANEL(): README text as plain text in the code-panel frame, header "repo/README.md · line 70
        (excerpt)"; .span(phrase) glyphs across rows, .bar(phrase, colour) bars (not added)
    excerpt_chip(sub, header, line=source_line(...)) (checks the sub-string)  readme_chip(where,
        phrase)  readme_card(where, lines)  cmd_chip(cmd, note_)  card_rows(items, header)
        table_card(headers, rows)  concept_box(text)  question_card(text)  card_glyph(title, sub)
        json_card(lines, colour)  fit_rows(text, width) (serif rows, `code` mono)  Counter(text, v)
    illustration_card(lines, title=None) invented code: mono rows, GREY card, `illustration` tag on
        its corner, never a path header; .bar(i)
    mcq_ponder(self, question, options, seconds=8, figure=None, cols=1) PLAYS the multiple-choice
        ponder (MCQ card, bottom at -3.5, timer drains) and returns it: card.reveal(i, note_) /
        card.reason(i, text) -> anims, then FadeOut(card). Options and reasons: serif, `code` mono;
        a reason must fit one row (raises). MCQ(...) builds the card without playing it.
    takeaway(text, y=-1.4) the YELLOW takeaway card, one row per " · " segment (≤ 4 rows):
        self.play(*card.write()); FadeOut(card) before the empty frame.
    ponder_at(scene, question) (L08's plain ponder card, kept)
Tags (GREY unless said): illustration_tag(note_) readme_example_tag() concept_tag() grey_tag(s)
    kfp_chip() (PURPLE "kfp 2.14.6 · read, not run") baked_chip() ("value baked in at compile time")
    cost_tag() (GOLD) free_tag() (GREEN) stamp(text, colour) fix_chip(text) lref("28–29") /
    lref_swap(self, old, "34")  swap_text(parent, old, new) (the house text swap; never Transform text)
Glyphs: ok_badge() fail_badge() value_token("9.0") sticky_note('"gs://my-bucket/clean.csv"')
    yaml_sheet("sample-pipeline1.yaml") machine_glyph(w, colour, text) bucket_glyph(text)
    clock_badge("1:00") endpoint_plate() registry_card() gold_meter() envelope() signature_chain()
    file_row(name) ghost_file(name) model_box(name) container_box(title) laptop_zone() laptop()
    x_mark() tick_mark() spark() under(m) strike(m) ring(m) bracket(mobs, text)

Nodes, wires, graphs (every DAG of the video)
    TaskNode(title, outputs=(".output",), flow="right"|"down", socket_labels=False, font=MONO,
        size=22, h=0.62) a task: WHITE box + GREEN output socket(s) + state badges. .run() .succeed(v)
        .fail() .skip() .reset() .set_value(v) .show_labels() -> anims; .out_point(i) .in_point(k, n)
        .token(v) (a value_token on the socket, not added; a long one overhangs along the wire).
        Size: box = name + 0.8 (min 1.3) x 0.62; a socket adds 0.95 to the right (flow "right") or
        0.42 below (flow "down"); "square" ≈ 2.85 x 0.85 with its (hidden) label.
    Wire(a, b, kind="data"|"order"|"pending", out=0, slot=0, slots=1, note=None) PINK solid / PINK
        dashed / GREY dotted, an S-curve from a's socket to b's input; .draw() .restyle(kind)
        .ride(token) .light() -> anims; .path (an invisible member: it moves with the wire)
    Dag(nodes {name: (x, y)}, edges [(a, b[, kind[, out]])], flow, titles, outputs, show, node_kw)
        a Piece: parts "node:<name>" "wire:<a>-><b>"; .node[n] .wire[(a, b)] .run(*n) .succeed(n, v)
        .fail(n) .skip(n) .restyle(a, b, kind) -> anims; .send(scene, a, b, value) PLAYS a token
        riding a -> b (returns it, on screen); .halo(names) (not added); .longest(durations); .topo()
    toy_dag(kind="pending") the sample_pipeline Y (flow down, YAML task names), 5.3 x 4.5
    fork_join_dag() prep -> train_a, train_b -> compare, 11.2 x 2.5
    p2_dag() P2's six tasks, minutes in the titles, no sockets, 12.0 x 2.0 (MCQ figure);
        p2_dag().longest(P2_MIN) == (16, ['ingest', 'clean', 'train_cnn', 'compare'])

Set pieces (Piece = VGroup with named parts: piece.reveal(scene, *names) / .hide plays;
    self.play(*piece.parts_in("a")); a part not shown yet is a member at opacity 0 (never FadeOut a
    part, FadeOut the whole piece); Piece(show=(...)) starts with only those parts visible). Sizes
    include hidden parts. Geometry follows the piece when you move it (no stale coordinates).
    V1 Tracer(show=())  5.3 x 5.1: the toy Dag with every node hidden; .drop(name) .connect()
       (GREY dotted wires + a "?" note) .stamp() (PURPLE "component: square") -> anims; the Dag
       methods (.restyle("square", "add", "data"), .run, .succeed("square", "9.0"), .send ...);
       .machines() TEAL glyphs left of the sockets (not added)
       press(scene, graph, sheet) PLAYS the PURPLE compiler roller sweeping over graph while graph
       shrinks into sheet (a placed yaml_sheet), 1.4 s; graph leaves the scene   compiler_roller(h)
       SubmitBridge(top=2.8, bottom=-1.2, split=-1.4) in place, 12.8 x 4.0: GREY laptop zone, BLUE
       Vertex zone, PURPLE `aiplatform` arrow; parts laptop / vertex / arrow; .carry(sheet) -> anim
       (rides the arrow into Vertex); .laptop_spot .vertex_spot .vertex_frame
    V2 WirePlug(mode="wire"|"after"|"note")  5.7 wide; wire 0.9 / after 1.0 / note 3.4 tall:
       prep -> train; parts prep train wire after_label note bucket old; .start() .finish_prep(v)
       .stale_read() (RED arrow + "stale" stamp, train ✓ outlined RED) .fresh_lands() -> anims;
       .prep .train .wire_ (ride a long token: tk = wp.prep.token(path); FadeIn; wp.wire_.ride(tk))
    V3 Gantt(rows [(name, a, b)], t_max, width=9.0, row_h=0.46, unit="min")  ~width x 2.3 (4 rows):
       bars hidden; .grow(name, run_time) -> anim (YELLOW, linear) .done(name) .fail(name)
       .set_span(name, a, b) -> anims; .guide(t) PINK dashed line, .total(t, text) YELLOW label under
       the axis (not added); .x_of(t) .row_y(name)    Wavefront(height, x, y) YELLOW band; .to(x)
    V4 FourLanes(lanes=("cron","amp","tracker","edges"), prep=40, top=2.8, names=None) in place,
       x -6.3..6.45, y -2.13..2.71 (one lane: 1.5 tall): parts "axis" "lane:<k>" "mark:<k>" (marks
       hidden); .set_prep(p) -> anims (lane_spans() rules: cron 0/60/120, amp all at 0, tracker
       fires at min(p, 60) and is never right, edges chain) .bar(lane, task) .flag(lane, task,
       text=None) RED ring + reason, left of the bar when its sub-row has room (not added) .ok
       .ticks .lane_y(lane) .x_of(minutes). Nothing ends after 3:15, so x > 1.9 is free in every
       lane: put the Leaderboard on the tracker lane at x ≈ 3.65.
       ClockFace(r=1.0, hour=1) ORANGE, 2.0 x 2.0; .set_time(h, m) -> anims
       Die(value=None) 1.1 x 1.1 (pips, or "40 / min"); .roll(v) -> anims
       Leaderboard(rows=(("model · run 12 · acc 0.91", True),), slots=2) BLUE, 4.6 x 1.3;
       .add_row(text, index=1) -> anims .pick(i) RED ring + "not this run" above its right end
       Launcher()  8.9 x 2.4: rows train · step / training job · another machine / deploy; parts
       rows step job edge deploy pick; .sync() .job_fails() -> anims
    V5 RegistryEndpoint(show=None)  12.0 x 4.9 (slide 12's layout; .rescale(k) beside a panel):
       parts cli gcp bucket folder vertex step1..step5 card callable plate machine meter;
       .register() .create_endpoint() .deploy() .cleanup() -> anims (card + folder stay);
       .meter_run(t) .meter_stop() -> anim; .route(start) PINK arrow to the plate (not added)
       ScoreBars(README_PROBS) 5.6 x 2.4, base line at y 0 before you move it (+ readme_example_tag());
       .argmax() -> anims    envelope() 5.0 x 0.6   signature_chain() 7.4 x 0.5
    V6 TwoClouds(show=None)  in place, 12.8 x 5.0, y -2.28..2.75: .chain (Dag of CHEESE, sans,
       dashed edges; keys collector processor training deploy) region board file:<name> sm
       (SageMaker Dag, SAGEMAKER, solid edges, hidden); .chalk(file) .to_sagemaker() -> anims;
       .reach(file, key) PINK arrow (not added); .steps_list() `steps=[` + STEP_VARS chips + `]`,
       11.0 x 1.2 in two rows (not added); .shuffle(row, order) -> anims
"""

from __future__ import annotations

import os
import re
import subprocess
import warnings
from functools import lru_cache
from pathlib import Path

import numpy as np
import yaml
from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    PI,
    RIGHT,
    TAU,
    UP,
    AnimationGroup,
    Arrow,
    Circle,
    Create,
    DashedLine,
    DashedVMobject,
    DecimalNumber,
    Dot,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    Line,
    ManimColor,
    MoveAlongPath,
    Polygon,
    Rectangle,
    Rotate,
    RoundedRectangle,
    ShowPassingFlash,
    Succession,
    Text,
    Transform,
    ValueTracker,
    VGroup,
    VMobject,
    linear,
    smooth,
    squish_rate_func,
)

from explainer import style as S


def guard(ok, msg=""):
    """Layout guard for positions and sizes. Raises locally like an assert; on the GitHub release
    runner, whose fonts set text up to ~1% wider, a miss is only warned about, so a sub-pixel
    difference cannot stop the release render of an already reviewed layout. Content checks
    (captures, narration, arithmetic) stay plain asserts and fail everywhere."""
    if ok:
        return
    if os.environ.get("GITHUB_ACTIONS") == "true":
        warnings.warn(f"layout guard tolerated on CI: {msg}", stacklevel=2)
        return
    raise AssertionError(msg)


from explainer.components import ponder_card  # noqa: F401  (re-exported for the scenes)
from explainer.devops import (  # noqa: F401  (re-exported for the scenes)
    CAPTION,
    LABEL,
    MONO,
    OUTPUT,
    PANEL,
    SANS,
    SMALL,
    TAG,
    TERM_BG,
    box,
    cell_width,
    check_mark,
    chip,
    cloud,
    code_block,
    code_panel,
    code_span,
    cross_mark,
    file_glyph,
    folder_glyph,
    glyph_range,
    label,
    laptop,
    lecture_ref,
    line_bar,
    line_pitch,
    mono,
    mono_line,
    server,
    step_badge,
    substring,
    tag,
    warning_sign,
)
from explainer.script import load_narration

# ------------------------------------------------------------------ paths and data
HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
ASSETS = PROJECT / "assets"
SOURCE = ASSETS / "source"          # assets/source/<repo>/<path>, unchanged at video.yaml's commits

SPEC = yaml.safe_load((PROJECT / "video.yaml").read_text())
TITLES = {s["cls"]: s["title"] for s in SPEC["scenes"]}
_script = PROJECT / "script.md"
NARRATION = load_narration(_script) if _script.exists() else {}

# ------------------------------------------------------------------ semantic colours (BRIEF.md "Colours")
LAPTOP = S.GREY          # your laptop, the workflow container that compiles and submits, the people at four CLIs
CLOUD = S.BLUE           # Vertex AI Pipelines, the run, step machines, the bucket, Model Registry, endpoint; SageMaker
CTR = S.TEAL             # step containers and images (cheese-app-data-collector / -processor, python:3.10)
CLOCK = S.ORANGE         # OS-owned scheduling that knows nothing about data: cron, `&` background jobs
SYSTEM = CLOCK
OWN = S.GREEN            # what this run produces: a task's output value, a fresh model, the YAML; the ✓ badge
VALUE = OWN
TOOL = S.PURPLE          # kfp (dsl, compiler), google-cloud-aiplatform (the SDK), the SageMaker SDK
ERR = S.RED              # races, stale reads, the wrong model, a failed task, the reason under a wrong option
TURN = S.YELLOW          # look here now: the wavefront, a running task, the ponder card, the takeaway cards
COST = S.GOLD            # the endpoint's machine and its hourly meter
EDGE = S.PINK            # edges and routes: .output solid + token, .after() dashed, the prediction route
LOOKUP = EDGE
STALE = S.GREY           # dashed: last run's leftovers, the previous model version, never-run tasks
INK = S.WHITE
DIMMED = S.GREY

# ------------------------------------------------------------------ names on screen (BRIEF.md "Things never to do")
# The sources hold the instructor's first name once (model-deployment/README.md:136) and no full
# name; no person's name is ever shown: that line is refused, and every shown line is checked.
MASKS = ("<ENDPOINT_ID>",)          # placeholders drawn GREY in panels and cards
_NAME_RE = re.compile(r"pavlos|protopapas", re.IGNORECASE)
NEVER_SOURCE = {        # file lines never quoted (BRIEF.md "Things never to do"; script.md "Notes")
    "model-deployment/cli.py": set(range(71, 84)),                        # the W&B entity
    "model-deployment/README.md": {136},                                  # a person's name
    "ml-workflow/src/workflow/sample-pipeline1.yaml": {80, 108, 136, 164, 248},   # old kfp / python:3.7
    "ml-workflow/src/workflow/model.py": {4, 53, 66},                     # stale comments
}


def guard_names(s: str) -> str:
    """Raise ValueError if s holds a person's name (never on screen). Returns s."""
    if _NAME_RE.search(s):
        raise ValueError("this line holds a person's name: it is never shown (BRIEF.md)")
    return s


def unname(s: str) -> str:
    """Kept for the ported helpers: no masking is needed here; refuses a person's name."""
    return guard_names(s)


# ------------------------------------------------------------------ the running example
TOY = ("square", "square-2", "add", "square-root")        # sample-pipeline1.yaml task names
TOY_VALUES = {"square": "9.0", "square-2": "16.0", "add": "25.0", "square-root": "5.0"}
CHEESE = ("Data Collector", "Data Processor", "Model Training", "Model Deploy")   # pipeline.yaml taskInfo
CHEESE_FILES = ("raw.zip", "clean.zip", "model/")          # ml-workflow/README.md:70
SAGEMAKER = ("DataCollector", "DataProcessor", "ModelTraining", "CreateModel", "DeployModel")
COLLECTOR_IMAGE = "dlops/cheese-app-data-collector"        # ml-workflow/src/workflow/cli.py:27
PROCESSOR_IMAGE = "dlops/cheese-app-data-processor"        # cli.py:28
ENDPOINT_NAME = "cheese-app-endpoint"                      # model-deployment/cli.py:197-203
ENDPOINT_ID = "<ENDPOINT_ID>"
BUCKET = "gs://my-bucket"                                  # invented examples only
README_PROBS = (0.0591, 0.1099, 0.6348, 0.1962)            # model-deployment/README.md:211
KFP_ERROR = "The task has multiple outputs. Please reference the output by its name."  # kfp 2.14.6
GUIDE = "MLOps_Learning · guides/L15-vertex-ml-workflows.md"
# V3 / P2 / V4 timings (script.md "Notes for scene authors"; illustration)
V3_TIMES = {"prep": (0, 2), "train_a": (2, 8), "train_b": (2, 6), "compare": (8, 9)}
P2_MIN = {"ingest": 2, "clean": 3, "train_cnn": 10, "train_tree": 4, "compare": 1, "report": 2}
V4_TRAIN, V4_DEPLOY, V4_ROLLS = 50, 10, (40, 75, 55)

# ------------------------------------------------------------------ layout
BOTTOM = -3.5
SAFE_X, SAFE_Y = 6.6, 3.6
LREF_BOTTOM = 3.13               # the lecture tag's bottom edge (top right)


def lref(slides: str) -> VGroup:
    """The GREY "Lecture 15 · slides 28–29" tag, top right (lecture_ref(15, slides))."""
    return lecture_ref(15, slides)


# ------------------------------------------------------------------ sources
def src_path(name: str) -> str:
    """A source under assets/source, named by its repo-relative path with the repo first
    ("ml-workflow/src/workflow/cli.py", "model-deployment/README.md"). Raises if missing."""
    if not (SOURCE / name).is_file():
        raise FileNotFoundError(f"assets/source/{name} not found")
    return name


@lru_cache(maxsize=None)
def source_text(name: str) -> str:
    """A tutorial file as text (never-shown lines are refused line by line by excerpt / src_panel /
    readme_panel; do not print source_text() whole)."""
    return (SOURCE / src_path(name)).read_text(encoding="utf-8")


def _source_lines(name: str, nums, strip_emoji_: bool = False) -> dict[int, str]:
    path = src_path(name)
    lines = source_text(name).split("\n")
    bad = NEVER_SOURCE.get(path, set()) & set(nums)
    if bad:
        raise ValueError(f"{path}: lines {sorted(bad)} are never shown (BRIEF.md / script.md)")
    out = {}
    for n in nums:
        if not 1 <= n <= len(lines):
            raise IndexError(f"{path} has {len(lines)} lines (asked for {n})")
        s = lines[n - 1].expandtabs(4)
        guard_names(s)
        out[n] = _emoji_guard(s, f"{path} line {n}", strip_emoji_)
    return out


def shown_path(name: str) -> str:
    """The path as the viewer sees it: the repo name first, then the repo's own path."""
    return src_path(name)


def cell_title(name: str) -> str | None:
    """No notebook cells in this video (src_panel(subtitle=True) shows nothing)."""
    return None


# ================================================================== generic helpers (from L07, tested there)
@lru_cache(maxsize=None)
def _mono_has(ch: str) -> bool:
    """True when the house mono font (or, failing that check, the system) has a glyph for ch."""
    try:
        out = subprocess.run(["fc-list", f":charset={ord(ch):x}", "family"], capture_output=True,
                             text=True, timeout=5).stdout
    except (OSError, subprocess.SubprocessError):
        return True
    return any("DejaVu Sans Mono" in f for f in out.splitlines())


def dropped_chars(s: str) -> list[str]:
    """Characters of s the house mono font cannot draw (emoji): they would vanish silently."""
    return sorted({ch for ch in s if ord(ch) > 0x2000 and not _mono_has(ch)})


def strip_emoji(s: str) -> str:
    """s without its emoji (EMOJI, and any other character the mono font drops) and the space they
    leave; the words stay exactly as captured (script.md "Emoji")."""
    bad = set(dropped_chars(s))
    if not bad:
        return s
    lead = len(s) - len(s.lstrip(" "))
    out = "".join(ch for ch in s if ch not in bad)
    body = re.sub(r"(?<=\S) {2,}(?=\S)", " ", out).lstrip()
    return (" " * lead + body) if body.strip() else out


def _emoji_guard(s: str, where: str, strip: bool) -> str:
    if strip:
        return strip_emoji(s)
    bad = dropped_chars(s)
    if bad:
        raise ValueError(f"{where}: {bad!r} would vanish (the mono font has no glyph): leave the line "
                         "out, or pass strip_emoji=True (script.md: print it without its emoji)")
    return s


def _out_early(t: float) -> float:
    """rate_func: done in the first 45% of the run (the old text of a swap leaves first)."""
    return smooth(min(1.0, t / 0.45))


def _in_late(t: float) -> float:
    """rate_func: starts at 55% of the run (the new text of a swap, after a short gap)."""
    return smooth(max(0.0, (t - 0.55) / 0.45))


def _in_first_half(t: float) -> float:
    return smooth(min(1.0, 2 * t))


def _out_second_half(t: float) -> float:
    return smooth(max(0.0, 2 * t - 1))


class _SwapOut(FadeOut):
    """The FadeOut of a text a swap replaces: the text stays a member of `parent` (and visible)
    until this fade is over, then leaves it for good (a member left behind at full opacity would
    snap back when the parent is next added or animated)."""

    def __init__(self, mob, parent, **kw):
        super().__init__(mob, **kw)
        self.swap_parent = parent

    def clean_up_from_scene(self, scene) -> None:
        super().clean_up_from_scene(scene)
        if self.mobject in self.swap_parent.submobjects:
            self.swap_parent.remove(self.mobject)


class _SwapIn(FadeIn):
    """The FadeIn of the text a swap brings: a member from the moment the swap is built, but at
    opacity 0 until this animation begins (a swap built early, e.g. passed as resize(extra=...),
    whose caller plays something else first, showed the new text in that play: S10 at 28.4 s)."""

    def begin(self) -> None:
        _set_op(self.mobject, attr="_swop")
        super().begin()


def _stage_swap(parent, old, new) -> None:
    """`new` joins `parent` right after `old` (so it takes old's slot once old leaves), invisible
    until its _SwapIn begins; `old` stays until its _SwapOut is over."""
    _save_op(new, "_swop")
    _set_op(new, 0, "_swop")
    if old in parent.submobjects:
        parent.insert(parent.submobjects.index(old) + 1, new)
    else:
        parent.add(new)


def _swap_text(parent, old, new) -> list:
    """Sequential text swap in ONE play (L05 final review: faded at once, both texts were
    half-readable mid-swap; a Transform between different strings scrambled the letters): `old`
    fades out in the first 45% of the run, `new` fades in from 55% (rate_funcs inside the same
    run_time, so the caller's timing is unchanged). `new` joins `parent` now (invisible until the
    swap plays) and `old` leaves it when its fade is over. Returns the two animations."""
    _stage_swap(parent, old, new)
    return [_SwapOut(old, parent, rate_func=_out_early), _SwapIn(new, rate_func=_in_late)]


def swap_text(parent, old, new) -> list:
    """Public: the sequential swap of two texts at one place (old fades out in the first 45% of the
    play, new fades in from 55%); `new` joins `parent` at once (invisible until the play), `old`
    leaves it after its fade. self.play(*swap_text(card, card.text, new_text)). Never Transform one
    string into another (the letters scramble)."""
    return _swap_text(parent, old, new)


def lref_swap(scene, old, slides: str, run_time: float = 0.5) -> VGroup:
    """Replace the lecture tag (old may be None). Returns the new tag (on screen). The old tag
    fades out, then the new one fades in, in the same run_time (faded at once, the two texts
    overlapped mid-swap: L05 final review)."""
    new = lref(slides)
    if old is None:
        scene.play(FadeIn(new), run_time=run_time)
    else:
        scene.play(Succession(FadeOut(old), FadeIn(new)), run_time=run_time)
    return new


def _comment_at(line: str) -> int:
    """Index of the '#' that starts a comment (outside quotes, not inside a word), or -1."""
    quote = None
    for i, ch in enumerate(line):
        if quote:
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
        elif ch == "#" and (i == 0 or line[i - 1] in " \t"):
            return i
    return -1


def cut_comment(line: str, limit: int = 65) -> str:
    """A line longer than `limit` loses its trailing comment, shown as '# …'."""
    if len(line) <= limit:
        return line
    i = _comment_at(line)
    if i < 0:
        return line
    code = line[:i]
    return code.rstrip() + "  # …" if code.strip() else code + "# …"


def sans(s: str, size: float = CAPTION, color: str = INK, **kw) -> Text:
    """CMU Sans Serif text (box labels, card lines)."""
    return label(s, size, color, font=SANS, **kw)


def note(s: str, color: str = S.GREY, size: float = CAPTION) -> Text:
    """A GREY caption (serif, 20 pt)."""
    return label(s, size, color)


def mtext(s: str, size: float = CAPTION, color: str = INK, font: str = MONO) -> Text:
    """Text through unname(), the masks drawn GREY (mono by default; font=SANS or S.FONT)."""
    s = unname(s)
    t2c = {m: S.GREY for m in MASKS if m in s}
    return S.text(s, size, color, font=font, t2c=t2c)


def grey_masks(line, ellipses: bool = True, color: str = S.GREY):
    """Colour every customer mask (and every '…', the sign of something left out) in a mono_line
    GREY; a folded command (a VGroup with .rows) is handled row by row. Returns line."""
    rows = line.rows if hasattr(line, "rows") else [line]
    for r in rows:
        s = getattr(r, "text", None)
        if not s or not hasattr(r, "glyphs"):
            continue
        for sub in ([*MASKS, "…"] if ellipses else list(MASKS)):
            i = s.find(sub)
            while i >= 0:
                glyph_range(r, i, i + len(sub)).set_color(color)
                i = s.find(sub, i + len(sub))
    return line


def _keep(m):
    """Mark a group (chip, tag, labelled glyph) to keep its size in Piece.rescale()."""
    m.keep_size = True
    return m


def keep_size(m):
    """Public: mark a group you built (a chip, a tag, a labelled glyph) to keep its size when a set
    piece it joins is rescaled (Piece.rescale shrinks shapes, never text). Returns m."""
    return _keep(m)


def _mix(color, k: float) -> ManimColor:
    """An opaque colour k of the way from the background to `color`."""
    return ManimColor(S.BG).interpolate(ManimColor(color), k)


def _poly(points, color: str = LOOKUP, stroke: float = 4) -> VMobject:
    """A polyline through `points` (elbow routes)."""
    m = VMobject(stroke_color=color, stroke_width=stroke)
    m.set_points_as_corners([np.array([p[0], p[1], 0.0]) for p in points])
    return m


def under(mob, color: str = TURN, stroke: float = 4, buff: float = 0.05) -> Line:
    """A Line under `mob` (a terminal line, a substring of one, a code span)."""
    return Line(mob.get_corner(DOWN + LEFT) + DOWN * buff, mob.get_corner(DOWN + RIGHT) + DOWN * buff,
                color=color, stroke_width=stroke)


def strike(mob, color: str = ERR, stroke: float = 4) -> Line:
    """A Line through the middle of `mob` (a struck-through name or chip)."""
    return Line(mob.get_left() + LEFT * 0.06, mob.get_right() + RIGHT * 0.06, color=color,
                stroke_width=stroke)


def ring(mob, color: str = ERR, buff: float = 0.08, stroke: float = 3) -> VMobject:
    """A rounded outline around `mob`."""
    r = RoundedRectangle(width=mob.width + 2 * buff, height=mob.height + 2 * buff,
                         corner_radius=min(0.12, (mob.height + 2 * buff) / 2), stroke_color=color,
                         stroke_width=stroke).set_fill(opacity=0)
    return r.move_to(mob)


def at_bottom(mob, y: float = BOTTOM, x: float = 0.0):
    """Put mob's bottom edge on y (the terminal line) and centre it at x (a code strip)."""
    return mob.shift(np.array([x - mob.get_center()[0], y - mob.get_bottom()[1], 0]))


WRAP_REACH = 20          # wrap_output: a break may come up to this many characters before the column


WRAP_HANG = 2            # wrap_output: continuation rows hang this far under the line's own indent


def wrap_output(s: str, width: int, reach: int = WRAP_REACH, hang: int = WRAP_HANG) -> list:
    """Fold one output line for a `width`-column terminal at a word boundary (QA: the fixed-column
    fold cut words and identifiers, "ad|k telemetry disable", "H|TTP/1.1", "itine|rary_validation"):
    at the last space within `reach` characters of the column, else after the last ',' there, else
    after the last '/', else after the last '_', '-' or '.', and at the column only when none is
    in reach. Continuation rows hang `hang` spaces under the line's own indent. Returns
    [(row, a, b, indent)] with row == " " * indent + s[a:b] (the spaces at a break are dropped)."""
    if len(s) <= width:
        return [(s, 0, len(s), 0)]
    lead = len(s) - len(s.lstrip(" "))
    ind = min(lead + hang, width // 3)
    out, pos, indent = [], 0, 0
    while len(s) - pos + indent > width:
        room = width - indent
        lo = pos + max(1, room - reach)                 # the earliest row end allowed
        hi = pos + room                                 # the latest: a full row
        cut = nxt = None
        spaces = [j for j in range(lo, min(hi, len(s) - 1) + 1) if s[j] == " " and s[j - 1] != " "]
        if spaces:
            cut = nxt = spaces[-1]
            while nxt < len(s) and s[nxt] == " ":
                nxt += 1
        else:
            for seps in (",", "/", "_-."):
                after = [j + 1 for j in range(lo - 1, hi) if s[j] in seps and j + 1 < len(s)]
                if after:
                    cut = nxt = after[-1]
                    break
        if cut is None:                                 # nothing in reach: at the column
            cut = nxt = hi
        out.append((" " * indent + s[pos:cut], pos, cut, indent))
        pos, indent = nxt, ind
    out.append((" " * indent + s[pos:], pos, len(s), indent))
    return out


def bracket(mobs, text: str, color: str = ERR, x: float | None = None) -> VGroup:
    """A vertical bracket spanning `mobs` (terminal lines) at their left margin (or at x), with a
    numbered badge centred on it. Not added. .line .badge"""
    g = VGroup(*mobs) if isinstance(mobs, (list, tuple)) else mobs
    top, bot = g.get_top()[1] + 0.02, g.get_bottom()[1] - 0.02
    x = g.get_left()[0] - 0.16 if x is None else x
    ln = VMobject(stroke_color=color, stroke_width=4)
    ln.set_points_as_corners([[x + 0.08, top, 0], [x, top, 0], [x, bot, 0], [x + 0.08, bot, 0]])
    b = step_badge(text, color, radius=0.19).move_to([x - 0.04, (top + bot) / 2, 0])
    out = VGroup(ln, b)
    out.line, out.badge = ln, b
    return _keep(out)


def grey_tag(s: str) -> VGroup:
    return _keep(tag(s, S.GREY))


def illustration_tag(note_: str | None = None) -> VGroup:
    """GREY 'illustration' (every schematic: Colab, the browser, the editor, the rings, the
    turnstile, the jar, the shelf, the "what if" variants); note_="what if" -> 'illustration · what if'."""
    return grey_tag("illustration" + (f" · {note_}" if note_ else ""))


def concept_tag(s: str = "concept · lecture only") -> VGroup:
    """The GREY dashed tag of a lecture idea with no code here (LLM as judge, MCP, peer handoffs,
    skill scripts/, Think and Reason inside the model)."""
    g = tag(s, S.GREY)
    dashed = DashedVMobject(g.box, num_dashes=int(g.box.width * 9), dashed_ratio=0.55)
    dashed.set_stroke(S.GREY, 2)
    fill = g.box.copy().set_stroke(width=0)
    res = VGroup(fill, dashed, g.text)
    res.box, res.text = fill, g.text
    return _keep(res)


def stamp(text: str, color: str = ERR, size: float = TAG, angle: float = 0.08) -> VGroup:
    """An outlined, slightly rotated stamp (BLOCKED, data, not instructions …). Opaque dark fill:
    put it where it covers nothing you need to read. .frame .text"""
    t = sans(text, size, color, weight="BOLD")
    r = RoundedRectangle(width=t.width + 0.3, height=t.height + 0.22, corner_radius=0.06,
                         stroke_color=color, stroke_width=3).set_fill(S.BG, 0.85)
    t.move_to(r)
    g = VGroup(r, t).rotate(angle)
    g.frame, g.text = r, t
    return _keep(g)


def fix_chip(text: str, color: str = OWN, font: str | None = None) -> VGroup:
    """A GREEN "the fix" chip (serif text; font=MONO for code)."""
    return _keep(chip(text, color, size=CAPTION, font=font))


def concept_box(text: str, size: float = CAPTION, color: str = S.GREY, min_w: float = 0.0,
                text_color: str = INK, h: float | None = None) -> VGroup:
    """A GREY dashed box holding a lecture concept (MCP, LLM as judge, handoffs …). .box .text"""
    t = label(text, size, text_color)
    h = h or mono("|", size).height + 0.26
    b = box(max(min_w, t.width + 0.5), h, color, dashed=True, radius=h / 2.6)
    bg = RoundedRectangle(width=b.width, height=h, corner_radius=h / 2.6, stroke_width=0).set_fill(S.BG, 0.9)
    t.move_to(b)
    g = VGroup(bg, b, t)
    g.box, g.text = b, t
    return _keep(g)


_LANG = {".py": "python", ".toml": "toml", ".sh": "bash", ".md": "markdown", ".yaml": "yaml",
         ".yml": "yaml", ".json": "json", ".html": "html", ".txt": "text", ".lock": "toml"}


def _lang(path: str) -> str:
    p = Path(path)
    if p.name == "Dockerfile":
        return "docker"
    if p.name in (".gitignore", ".dockerignore") or p.name.startswith(".env"):
        return "text"
    return _LANG.get(p.suffix, "text")


def _looks_path(p: str) -> bool:
    return bool(re.search(r"\.[A-Za-z]\w*$", p)) or ("/" in p and " " not in p)


def _header_text(text: str, size: float = CAPTION) -> VGroup:
    """'cli.py · lines 183–194' -> mono path + serif rest; 'Agent Harness · cell 10 · lines 3–6' all
    serif."""
    parts = text.split(" · ")
    mobs = []
    path_done = False
    for i, p in enumerate(parts):
        s = p if i == 0 else f"· {p}"
        if _looks_path(p) and not path_done:
            mobs.append(mono(s, size, S.GREY))
            path_done = True
        else:
            mobs.append(label(s, size, S.GREY))
    return VGroup(*mobs).arrange(RIGHT, buff=0.12)


def _with_header(panel: VGroup, text: str, size: float = CAPTION, subtitle: str | None = None) -> VGroup:
    """Replace a code_panel's header with `text` (+ a GREY quoted subtitle after it)."""
    header = _header_text(text, size)
    if subtitle:
        header.add(label(f"“{subtitle}”" if not subtitle.startswith("your copy") else subtitle,
                         size, S.GREY))
        header.arrange(RIGHT, buff=0.12)
        header[-1].shift(RIGHT * 0.15)
    header.next_to(panel.code, UP, buff=0.1).align_to(panel.code, LEFT).shift(RIGHT * 0.12)
    panel.remove(panel.header)
    panel.header = header
    panel.add(header)
    return panel


def _wrap_line(line: str, breaks: list[str]) -> list[str]:
    """Break a code line before each substring in `breaks` (in order); continuation rows keep
    the line's indent plus '  ↪ '."""
    indent = line[:len(line) - len(line.lstrip())]
    rows, rest = [], line
    for b in breaks:
        i = rest.find(b, 1)
        if i < 0:
            raise ValueError(f"{b!r} not in {rest!r}")
        rows.append(rest[:i].rstrip())
        rest = rest[i:]
    rows.append(rest)
    return [rows[0]] + [f"{indent}  ↪ {r.strip()}" for r in rows[1:]]


def _auto_wrap(line: str, limit: int = 65) -> list[str]:
    """Break a line longer than `limit` at spaces; continuation rows: indent + '  ↪ '."""
    if len(line) <= limit:
        return [line]
    indent = line[:len(line) - len(line.lstrip())]
    pre = indent + "  ↪ "
    rows, rest, first = [], line, True
    while len(rest) > (limit if first else limit - len(pre)):
        lim = limit if first else limit - len(pre)
        i = rest.rfind(" ", len(indent) + 1 if first else 1, lim)
        if i <= 0:
            i = lim
        rows.append(rest[:i].rstrip() if first else pre + rest[:i].strip())
        rest = rest[i:].lstrip()
        first = False
    rows.append(rest if first else pre + rest.strip())
    return rows


def _lex_whole(code, code_rows, whole, spots, language: str, size: float) -> None:
    """Colour the rows of each wrapped line as the lexer colours the WHOLE line (S03, S11, S13
    critics: src_panel wrapped before lexing, so a wrapped string's continuation row was lexed as
    code and came out half-coloured). `whole` is the panel's rows with every wrapped line in one
    piece; spots = {file line: (its row in `whole`, its rows in the panel)}. A reference
    code_block of `whole` (same language and style, lexed in context) lends its glyph colours to
    the wrapped rows, the ↪ marks skipped (they turn GREY afterwards). A line whose glyphs don't
    pair up one to one is left as it was."""
    ref = code_block("\n".join(whole), language, size)
    for r, ks in spots.values():
        src = [g for g in ref.code_lines[r]]
        dst = []
        for k in ks:
            txt = "".join(code_rows[k].split())
            glyphs = list(code.code_lines[k]) if k < len(code.code_lines) else []
            if len(glyphs) != len(txt):
                dst = None
                break
            dst += [g for c, g in zip(txt, glyphs) if not (c == "↪" and k != ks[0])]
        if dst is None or len(dst) != len(src):
            continue
        for d, g in zip(dst, src):
            d.set_color(g.get_color())


def _line_bars(code, ks, color, opacity) -> VGroup:
    """src_panel's .bar(n): a VGroup of line bars over rows ks; the rows of ONE wrapped line get a
    single bar from the first row's top to the last row's bottom (one bar per row overlapped in a
    brighter seam: S12 critic)."""
    bars = [line_bar(code, k, color, opacity) for k in ks]
    if len(bars) < 2:
        return VGroup(*bars)
    top = max(b.get_top()[1] for b in bars)
    bot = min(b.get_bottom()[1] for b in bars)
    one = Rectangle(width=bars[0].width, height=top - bot, stroke_width=0).set_fill(color, opacity)
    return VGroup(one.move_to([bars[0].get_center()[0], (top + bot) / 2, 0]))


def _spec_lines(spec) -> list[int]:
    out: list[int] = []
    for s in spec:
        if isinstance(s, int):
            out.append(s)
        else:
            out += list(range(s[0], s[1] + 1))
    if out != sorted(set(out)):
        raise ValueError(f"folded lines must increase: {spec}")
    return out


def src_panel(name: str, first, last: int | None = None, cut_comments: bool = False,
              focus=None, size: float = 22, width: float | None = None,
              shown: str | None = None, suffix: str | None = None, wrap=None, join=None,
              subtitle=None, language: str | None = None, strip_emoji: bool = False,
              max_rows: int = 12) -> VGroup:
    """code_panel quoting assets/source/<name> (name masked), header "shown · lines a–b" (+ " ·
    comment cut", " · line N wrapped", " · suffix"). `first` may be a list (folded: only those file
    lines, a GREY '…' row at each gap, header "lines a–b (folded)"). join=[(a, b)]: lines a..b as
    one row. wrap=True / {n: ["sub", …]} as in L05. subtitle=True: the Colab cell's @title in GREY
    quotes; a str: that text. focus: file line(s) kept bright, the rest dimmed.
    .rows_of(file_line) -> code row indices; .bar(file_line, colour) -> VGroup of line bars (not
    added); .span(file_line, sub) -> glyphs; .source_name .first"""
    folded = isinstance(first, (list, tuple))
    nums = _spec_lines(first) if folded else list(range(first, (first if last is None else last) + 1))
    lo, hi = nums[0], nums[-1]
    lines = _source_lines(name, nums, strip_emoji)
    if cut_comments:
        lines = {n: cut_comment(s) for n, s in lines.items()}
    joined_into: dict[int, int] = {}
    for a, b in (join or []):
        if not all(n in lines for n in range(a, b + 1)):
            raise ValueError(f"join {a}-{b}: every line must be shown")
        lines[a] = lines[a].rstrip() + "".join(lines[n].strip() for n in range(a + 1, b + 1))
        for n in range(a + 1, b + 1):
            joined_into[n] = a
    rows, rows_of, wrapped, gap_rows = [], {}, [], []
    whole, whole_row = [], {}          # the same rows with each wrapped line whole (lexed in context)
    prev = None
    for n in nums:
        if n in joined_into:
            rows_of[n] = rows_of[joined_into[n]]
            prev = n
            continue
        ln = lines[n]
        if prev is not None and n > prev + 1:
            indent = ln[:len(ln) - len(ln.lstrip())]
            gap_rows.append(len(rows))
            rows.append(indent + "…")
            whole.append(indent + "…")
        if isinstance(wrap, dict) and n in wrap:
            parts = _wrap_line(ln, wrap[n])
        elif wrap is True:
            parts = _auto_wrap(ln)
        else:
            parts = [ln]
        if len(parts) > 1:
            wrapped.append(n)
        rows_of[n] = list(range(len(rows), len(rows) + len(parts)))
        rows += parts
        whole_row[n] = len(whole)
        whole.append(ln)
        prev = n
    if len(rows) > max_rows:
        raise ValueError(f"{name} {lo}-{hi}: {len(rows)} rows (at most {max_rows} on screen): "
                         "show it in windows, or fold it")
    shown = shown or shown_path(name)
    p = code_panel("\n".join(rows), shown, lo, language or _lang(src_path(name)), font_size=size,
                   width=width)
    if p.code.width > 12.95:
        raise ValueError(f"{name} {lo}-{hi}: the panel is {p.code.width:.1f} wide (> 12.9): "
                         "wrap=True, or wrap={line: [break before …]}")
    where = f"line {lo}" if lo == hi else f"lines {lo}–{hi}"
    if folded:
        where += " (folded)"
    extra = []
    if cut_comments and any(cut_comment(s) != s for s in _source_lines(name, nums, strip_emoji).values()):
        extra.append("comment cut")
    extra += [f"line {n} wrapped" for n in wrapped]
    if suffix:
        extra.append(suffix)
    if subtitle is True:
        subtitle = cell_title(name)
    _with_header(p, " · ".join([shown, where, *extra]), subtitle=subtitle or None)
    code_rows = p.code.source.split("\n")
    if wrapped:
        _lex_whole(p.code, code_rows, whole, {n: (whole_row[n], rows_of[n]) for n in wrapped},
                   language or _lang(src_path(name)), size)
    for k in range(len(code_rows)):                 # GREY ↪ marks, '…' gap rows and the mask
        for sub in ("↪", "…", *MASKS):
            if sub == "↪" and k not in [r for ks in rows_of.values() for r in ks[1:]]:
                continue
            if sub == "…" and k not in gap_rows:
                continue
            occ = 0
            while True:
                try:
                    code_span(p.code, k, sub, occ).set_color(S.GREY)
                except (ValueError, IndexError):
                    break
                occ += 1
    if focus is not None:
        keep = {focus} if isinstance(focus, int) else set(focus)
        for n, ks in rows_of.items():
            if n not in keep:
                for k in ks:
                    if k < len(p.code.code_lines):
                        p.code.code_lines[k].set_opacity(0.3)
    p.source_name, p.first, p.rows_map = name, lo, rows_of
    p.rows_of = lambda n: rows_of[n]
    p.bar = lambda n, color=TURN, opacity=0.18: _line_bars(p.code, rows_of[n], color, opacity)

    def span(n, sub, occurrence=0):
        for k in rows_of[n]:
            try:
                return code_span(p.code, k, sub, occurrence)
            except ValueError:
                continue
        raise ValueError(f"{sub!r} not in line {n} of {name}")
    p.span = span
    return p


def _mono_rows(lines, size: float, color: str, max_chars: int | None = None) -> VGroup:
    rows = VGroup()
    pitch = line_pitch(size)
    for i, s in enumerate(lines):
        s, col = (s, color) if isinstance(s, str) else s
        s = strip_emoji(unname(s))
        if max_chars and len(s) > max_chars:
            s = s[:max_chars - 1] + "…"
        ln = mono_line(s, size, col)
        grey_masks(ln)
        ln.shift(np.array([0, -i * pitch, 0]) - ln.strut.get_corner(UP + LEFT))
        rows.add(ln)
    return rows


def readme_chip(where: str, phrase: str | None = None, size: float = CAPTION,
                max_w: float = 12.4, expected: bool = False) -> VGroup:
    """A one-line README chip: GREY `where` ("README.md · line 244 (excerpt)") and the quoted
    phrase in white (expected=True adds the GREY `expected` tag after it). Fails if wider than
    max_w: in the top band right of the tracker pass max_w=6.4 (shorten the phrase). .frame
    .where .phrase .tag"""
    w = _header_text(where, size)
    parts = [w]
    ph = None
    if phrase:
        ph = mtext(f"“{phrase}”", size, INK, font=S.FONT)
        parts.append(ph)
    row = VGroup(*parts).arrange(RIGHT, buff=0.25)
    fr = box(row.width + 0.4, row.height + 0.24, S.GREY, fill=S.BG, fill_opacity=0.92, radius=0.1)
    fr.move_to(row)
    g = VGroup(fr, row)
    g.tag = None
    guard(not expected, "readme_chip: no `expected` tags in this video (it shows no outputs)")
    if g.width > max_w:
        raise ValueError(f"README chip {g.width:.1f} wide (> {max_w}): shorten {phrase!r}")
    g.frame, g.where, g.phrase = fr, w, ph
    return _keep(g)


class Prose(str):
    """A prose row for turn_card / card_rows (serif, not a command)."""


def _cell(s, size: float = CAPTION, color: str = INK):
    """A card cell: "`code`" -> mono (without backticks), Prose / str -> serif, a mobject as is."""
    if not isinstance(s, str):
        return s
    if len(s) > 1 and s.startswith("`") and s.endswith("`"):
        return mtext(s[1:-1], size, color)
    return mtext(str(s), size, color, font=S.FONT)


def readme_card(where: str, lines: list[str], width: float | None = None,
                size: float = CAPTION) -> VGroup:
    """A multi-line GREY README card: header `where` above, the README's words inside (a line in
    backticks is mono). .frame .rows .header"""
    rows = VGroup(*[_cell(s, size) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    w = max(width or 0, rows.width + 0.5)
    fr = box(w, rows.height + 0.4, S.GREY, fill=S.BG, fill_opacity=0.92, radius=0.12)
    rows.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.25)
    head = _header_text(where, size).next_to(fr, UP, buff=0.08).align_to(fr, LEFT).shift(RIGHT * 0.1)
    g = VGroup(fr, rows, head)
    g.frame, g.rows, g.header = fr, rows, head
    return g


def _md_text(s: str, size: float = CAPTION, color: str = INK) -> Text:
    """One README line as ONE Text: inline `code` in mono (backticks dropped, spacing kept), the rest
    serif; masks GREY."""
    s = unname(s)
    parts = s.split("`")
    plain, spans, pos = "", [], 0
    for k, p in enumerate(parts):
        if k % 2:
            spans.append((len(plain), len(plain) + len(p)))
        plain += p
    t2c = {m: S.GREY for m in MASKS if m in plain}
    return S.text(plain, size, color, t2f={f"[{a}:{b}]": MONO for a, b in spans if b > a}, t2c=t2c)


def _wrap_words(s: str, limit: int) -> list[str]:
    """Break prose at spaces into rows of at most `limit` characters (a long word stays whole)."""
    rows, cur = [], ""
    for w in s.split(" "):
        if cur and len(cur) + 1 + len(w) > limit:
            rows.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}" if cur else w
    rows.append(cur)
    return rows


def excerpt_chip(sub: str, header: str, color: str = INK, frame: str = S.GREY,
                 line: str | None = None, size: float = CAPTION) -> VGroup:
    """An excerpt chip: a mono chip holding the exact sub-string `sub` of one source or capture
    line, headed `header` ("cli.py · line 459 (excerpt)"). Pass the full `line` (excerpt(...) or
    cap.line(n)) to check the sub-string. .chip .text .header"""
    sub = unname(sub)
    if line is not None and sub not in unname(line):
        raise ValueError(f"{sub!r} is not in {line!r}")
    c = chip(sub, frame, size=size, text_color=color, font=MONO, fill_opacity=0.1)
    if any(m in sub for m in MASKS):
        new = mtext(sub, size, color).move_to(c.text)
        c.remove(c.text)
        c.add(new)
        c.text = new
    h = _header_text(header, size).next_to(c, UP, buff=0.08).align_to(c, LEFT).shift(RIGHT * 0.08)
    g = VGroup(c, h)
    g.chip, g.text, g.header = c, c.text, h
    return _keep(g)


def cmd_chip(cmd: str, note_: str | None = None, color: str = S.GREY, size: float = CAPTION,
             note_color: str = S.GREY) -> VGroup:
    """A command shown, not typed: a mono chip, and an optional note under it. .chip .note"""
    c = chip(cmd, color, size=size, font=MONO)
    if not note_:
        c.chip, c.note = c, None
        return _keep(c)
    n = label(note_, size, note_color).next_to(c, DOWN, buff=0.1).align_to(c, LEFT)
    g = VGroup(c, n)
    g.chip, g.note = c, n
    return _keep(g)


def _mixed_row(parts, size: float = CAPTION, color: str = INK) -> Text:
    """One row mixing mono ("`code`") and serif pieces as ONE Text (one baseline), pieces joined
    by a space (none before a piece that starts with , . : ? ; or ·…)."""
    s, spans = "", []
    for p in parts:
        code = len(p) > 1 and p.startswith("`") and p.endswith("`")
        txt = unname(p[1:-1] if code else p)
        if s and (code or txt[0] not in ",.:?;"):
            s += " "
        if code:
            spans.append((len(s), len(s) + len(txt)))
        s += txt
    t2c = {m: S.GREY for m in MASKS if m in s}
    return S.text(s, size, color, t2f={f"[{a}:{b}]": MONO for a, b in spans}, t2c=t2c)


def card_rows(items, width: float | None = None, header: str | None = None,
              size: float = CAPTION, frame_color: str = S.GREY, buff: float = 0.16) -> VGroup:
    """A GREY card of rows (fix cards, checklists): each item is a str (serif; "`mono`" in
    backticks), (str, colour), or a mobject. .frame .rows .header; rows write in with
    self.play(FadeIn(card.rows[i]))."""
    rows = VGroup()
    for it in items:
        if isinstance(it, tuple):
            rows.add(_cell(it[0], size, it[1]))
        else:
            rows.add(_cell(it, size, INK))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=buff)
    w = max(width or 0, rows.width + 0.6)
    fr = box(w, rows.height + 0.5, frame_color, fill=S.BG, fill_opacity=0.95, radius=0.14)
    rows.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.3)
    g = VGroup(fr, rows)
    g.header = None
    if header:
        h = note(header).next_to(fr, UP, buff=0.08).align_to(fr, LEFT).shift(RIGHT * 0.12)
        g.add(h)
        g.header = h
    g.frame, g.rows = fr, rows
    return g


def table_card(headers, rows, col_w=None, size: float = CAPTION, header_colors=None,
               buff: float = 0.16) -> VGroup:
    """A two- or three-column card. headers: column titles; rows: lists of cells (str, "`mono`",
    or a mobject). .cells[r][c] .heads .frame. Not added; write rows in with
    FadeIn(VGroup(*card.cells[r]))."""
    ncol = len(headers)
    header_colors = header_colors or [S.GREY] * ncol
    heads = [label(h, size, c) for h, c in zip(headers, header_colors)]
    cells = [[_cell(c, size) for c in r] for r in rows]
    widths = col_w or [max([heads[c].width] + [r[c].width for r in cells]) + 0.4 for c in range(ncol)]
    pitch_rows = [max(m.height for m in r) for r in cells]
    hh = max(h.height for h in heads)
    total_h = hh + sum(pitch_rows) + buff * (len(rows) + 1) + 0.5
    total_w = sum(widths) + 0.4
    fr = box(total_w, total_h, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.14)
    x0, y = fr.get_left()[0] + 0.2, fr.get_top()[1] - 0.25
    xs = [x0 + sum(widths[:c]) for c in range(ncol)]
    for c, h in enumerate(heads):
        h.move_to([xs[c], y - hh / 2, 0], aligned_edge=LEFT)
    y -= hh + buff
    sep = Line([fr.get_left()[0] + 0.15, y + buff / 2, 0], [fr.get_right()[0] - 0.15, y + buff / 2, 0],
               color=S.GREY_DARK, stroke_width=2)
    for r, row in enumerate(cells):
        for c, m in enumerate(row):
            m.move_to([xs[c], y - pitch_rows[r] / 2, 0], aligned_edge=LEFT)
        y -= pitch_rows[r] + buff
    g = VGroup(fr, sep, *heads, *[m for r in cells for m in r])
    g.frame, g.heads, g.cells = fr, heads, cells
    return g


def ponder_at(scene, question: str, seconds: float = 8.0, y: float = -2.2,
              width: float = 10.2, hide=()) -> VGroup:
    """The ponder card (pause_and_ponder's look) in the lower third, opaque, its timer draining
    over `seconds`; its bottom never goes below -3.55. `hide` (e.g. a 3-row strip) fades out as
    the card arrives (bring it back yourself). Returns the card (FadeOut it at the start of the
    next SAY block)."""
    card = ponder_card(question, width=width).move_to([0, y, 0])
    card[0].set_fill(S.BG, 1)
    if card.get_bottom()[1] < -3.55:
        card.shift(UP * (-3.55 - card.get_bottom()[1]))
    scene.play(FadeIn(card, scale=0.95), *[FadeOut(m) for m in hide], run_time=0.6)
    bar = card[3]
    scene.play(bar.animate(rate_func=linear).become(bar.copy().scale(0.001, about_point=bar.get_start())),
               run_time=seconds)
    return card


class Counter(VGroup):
    """A counter "chunks: 8,248": a label and a number (with thousands commas) driven by a
    ValueTracker. .count_to(n, run_time) -> animation; .freeze() before it leaves. .num .label"""

    def __init__(self, text: str | None = "chunks", value: float = 0, color: str = INK,
                 size: float = 26, **kw):
        super().__init__(**kw)
        self.tracker = ValueTracker(value)
        self.num = DecimalNumber(value, num_decimal_places=0, group_with_commas=True,
                                 font_size=size * 1.3, color=color)
        self.num.add_updater(lambda m: m.set_value(self.tracker.get_value()))
        self.label = None
        if text:
            self.label = label(f"{text}:", size, color)
            self.num.next_to(self.label, RIGHT, buff=0.15).align_to(self.label, DOWN)
            self.add(self.label)
        self.add(self.num)
        _keep(self)

    def count_to(self, n: float, run_time: float = 1.0):
        return self.tracker.animate(rate_func=linear, run_time=run_time).set_value(n)

    def freeze(self):
        self.num.clear_updaters()
        return self


def file_row(name: str, color: str = INK, glyph_color: str = S.GREY, size: float = CAPTION) -> VGroup:
    """A file (or folder, name ending in '/') glyph + its mono name. .glyph .text .fname"""
    g = folder_glyph(0.22, glyph_color) if name.endswith("/") else file_glyph(0.28, glyph_color)
    t = mono(name, size, color).next_to(g, RIGHT, buff=0.12)
    row = VGroup(g, t)
    row.glyph, row.text, row.fname = g, t, name
    return _keep(row)


def ghost_file(name: str, color: str = S.GREY) -> VGroup:
    """A dashed GREY file that doesn't exist (uv.lock, a missing systemInstruction …)."""
    g = DashedVMobject(file_glyph(0.28, color)[0], num_dashes=18).set_stroke(color, 2)
    t = mono(name, CAPTION, color).next_to(g, RIGHT, buff=0.12)
    row = VGroup(g, t)
    row.glyph, row.text, row.fname = g, t, name
    return _keep(row)


def model_box(name: str = "LLM", w: float = 1.3, h: float = 0.9, color: str = CLOUD,
              sub: str | None = None, size: float = CAPTION) -> VGroup:
    """A model box: BLUE rounded box, sans name ("\\n" splits rows), optional mono sub-label
    inside under it. .frame .title .sub"""
    nm = VGroup(*[sans(s, size, INK) for s in name.split("\n")]).arrange(DOWN, buff=0.06)
    sb = mono(sub, size, color).next_to(nm, DOWN, buff=0.1) if sub else None
    content = VGroup(nm, sb) if sb is not None else nm
    fr = box(max(w, content.width + 0.3), max(h, content.height + 0.24), color, fill_opacity=0.14,
             radius=0.12, stroke=3)
    content.move_to(fr)
    g = VGroup(fr, nm)
    g.sub = None
    if sb is not None:
        g.add(sb)
        g.sub = sb
    g.frame, g.title = fr, nm
    return g


def container_box(title: str, w: float = 3.0, h: float = 2.0, color: str = CTR,
                  size: float = CAPTION) -> VGroup:
    """A container: TEAL rounded box with its mono name at the top. .frame .title .body_top()"""
    fr = box(w, h, color, fill=S.BG, fill_opacity=1.0, radius=0.14, stroke=3)
    tint = RoundedRectangle(width=w, height=h, corner_radius=0.14, stroke_width=0).set_fill(color, 0.06)
    t = mono(title, size, color).move_to(fr.get_top() + DOWN * 0.28)
    g = VGroup(fr, tint, t)
    g.frame, g.title = fr, t
    g.body_top = lambda: t.get_bottom()[1] - 0.12
    return g


def laptop_zone(w: float = 7.0, h: float = 3.8, caption: str | None = "your laptop",
                color: str = LAPTOP, size: float = CAPTION, corner=DOWN + LEFT) -> VGroup:
    """The GREY laptop as a zone (things inside it run on your machine); the caption sits in
    `corner` (DOWN + LEFT or DOWN + RIGHT). .frame .caption"""
    fr = box(w, h, color, fill_opacity=0.04, radius=0.2, stroke=2.5)
    g = VGroup(fr)
    g.frame, g.caption = fr, None
    if caption:
        c = label(caption, size, color).move_to(fr.get_corner(corner), aligned_edge=corner) \
            .shift(np.array([0.2 if corner[0] < 0 else -0.2, 0.12, 0]))
        g.add(c)
        g.caption = c
    return g


def cost_tick(r: float = 0.1, color: str = COST) -> VGroup:
    """A GOLD tick per paid call: a small coin."""
    c = Circle(radius=r, stroke_color=color, stroke_width=2.5).set_fill(color, 0.45)
    inner = Circle(radius=r * 0.55, stroke_color=color, stroke_width=1.5)
    return _keep(VGroup(c, inner))


def json_card(lines, color: str = OWN, size: float = CAPTION, header: str | None = None) -> VGroup:
    """A card of mono rows (masked, emoji stripped) in `color` (a BLUE tool request, a GREEN
    result, a GREEN capsule): .frame .rows .header"""
    rows = _mono_rows(lines, size, INK)
    fr = box(rows.width + 0.5, rows.height + 0.4, color, fill=S.BG, fill_opacity=0.95, radius=0.12, stroke=2.5)
    tint = RoundedRectangle(width=fr.width, height=fr.height, corner_radius=0.12, stroke_width=0) \
        .set_fill(color, 0.08).move_to(fr)
    rows.move_to(fr)
    g = VGroup(fr, tint, rows)
    g.frame, g.rows, g.header = fr, rows, None
    if header:
        h = note(header).next_to(fr, UP, buff=0.08).align_to(fr, LEFT).shift(RIGHT * 0.1)
        g.add(h)
        g.header = h
    return g


def _save_op(m, attr: str = "_hop"):
    """Remember the fill/stroke opacity of every member of m ("_hop" for hide/reveal, "_dop"
    for dim/undim)."""
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
    """Remove the wrapper group an AnimationGroup / LaggedStart adds to the scene."""
    for a in anims:
        if isinstance(a, AnimationGroup) and a.group in scene.mobjects:
            scene.remove(a.group)


def _ref(point) -> Dot:
    """An invisible reference point (geometry that follows moves and rescales)."""
    return Dot(point, radius=0.01).set_fill(opacity=0).set_stroke(width=0, opacity=0)


class Piece(VGroup):
    """A set piece: a VGroup with named parts (self.parts) and helpers that keep the scene clean.

    A part that is not shown yet is a member at opacity 0, so it moves and scales with the piece
    and the piece's size never jumps; parts_in() / reveal() fade it in, parts_out() / hide() fade it
    back to 0. Never FadeOut a part (a FadeOut removes it from the scene and splits the piece);
    never set_opacity on the whole piece (it would show hidden parts): use dim_to()/undim()."""

    def __init__(self, **kw):
        super().__init__(**kw)
        self.parts: dict[str, object] = {}

    # -- parts
    def part(self, name: str, mob, shown: bool = True, into=None):
        """Register and add a named part (invisible until shown when shown=False)."""
        self.parts[name] = mob
        if not shown:
            _save_op(mob)
            _set_op(mob, 0)
        mob.hidden = not shown
        (into if into is not None else self).add(mob)
        return mob

    def _show_set(self, show, names):
        """show=None -> every name; a tuple -> those names."""
        return set(names) if show is None else set(show)

    def parts_in(self, *names, anim=None) -> list:
        """Animations that fade in (or anim(mob): Create, Write, GrowArrow …) the named hidden
        parts. Use inside self.play(*piece.parts_in("a", "b"))."""
        out = []
        for n in names:
            m = self.parts[n]
            if getattr(m, "hidden", False):
                _set_op(m)
            self._flag(m, False)
            out.append((anim or FadeIn)(m))
        return out

    def parts_out(self, *names) -> list:
        """Animations that fade the named parts to opacity 0 (they stay members)."""
        out = []
        for n in names:
            m = self.parts[n]
            if getattr(m, "hidden", False):
                continue
            _save_op(m)
            out.append(m.animate.set_opacity(0))
            self._flag(m, True)
        return out

    def reveal(self, scene, *names, run_time: float = 0.6, anim=None, extra=()):
        """parts_in() with its own play. Returns the part (or a list of them)."""
        self._ensure(scene)
        scene.play(*self.parts_in(*names, anim=anim), *extra, run_time=run_time)
        mobs = [self.parts[n] for n in names]
        return mobs[0] if len(mobs) == 1 else mobs

    def hide(self, scene, *names, run_time: float = 0.4, extra=()):
        anims = self.parts_out(*names) + list(extra)
        if anims:
            scene.play(*anims, run_time=run_time)

    def is_shown(self, name: str) -> bool:
        return not getattr(self.parts[name], "hidden", False)

    def _flag(self, m, hidden: bool):
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
        (or of `into`), so moving the piece moves them. Returns the first mob (or a list)."""
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

    def glyph_only(self) -> VGroup:
        """A copy without any text (a thumbnail: shapes, colours; scale freely)."""
        c = self.copy()

        def strip(m):
            for s in list(m.submobjects):
                if isinstance(s, Text) or hasattr(s, "pt") or isinstance(s, DecimalNumber):
                    m.remove(s)
                else:
                    strip(s)
        strip(c)
        return c


def _restroke(mobs, color, width=None) -> list:
    """Animations recolouring the strokes of `mobs` (lighting a box)."""
    out = []
    for m in mobs:
        out.append(m.animate.set_stroke(color, width) if width else m.animate.set_stroke(color))
    return out


def _arrow(a, b, color: str = S.GREY, stroke: float = 3, buff: float = 0.06) -> Arrow:
    return Arrow(a, b, buff=buff, color=color, stroke_width=stroke, max_tip_length_to_length_ratio=0.3,
                 tip_length=0.16)


class _Reveal(FadeIn):
    """FadeIn of a member kept at opacity 0 (Piece.part(shown=False), or staged): its saved
    opacities come back when the animation BEGINS, not when it is built (a reveal built early and
    played later must not show the member in between)."""

    def __init__(self, mob, attr: str = "_hop", **kw):
        self._attr = attr
        super().__init__(mob, **kw)

    def begin(self) -> None:
        _set_op(self.mobject, attr=self._attr)
        super().begin()


def _stage_hidden(parent, mob, attr: str = "_swop"):
    """Add `mob` to `parent` at opacity 0 (its opacities saved under `attr`) for a _Reveal."""
    parent.add(mob)
    _save_op(mob, attr)
    _set_op(mob, 0, attr)
    return mob


def _rich(s: str, size: float = CAPTION, color: str = INK) -> Text:
    """Serif text with `code` spans in mono (backticks dropped); masks GREY."""
    return _md_text(s, size, color)


def fit_rows(text: str, width: float, size: float = CAPTION, color: str = INK, buff: float = 0.08,
             align=LEFT) -> VGroup:
    """`text` as rows that fit `width`: it breaks at " · " first (the separator stays at a row's
    end), then at spaces; a lone word wider than `width` raises. Rows are serif with `code` mono.
    Returns a VGroup of rows (arranged, aligned)."""
    def bal(r: str, carry: bool) -> tuple[str, bool]:
        """r as one row that starts inside a `code` span when carry: the span is closed at the
        row's end and reopened on the next row (a span broken across rows stays mono)."""
        r = ("`" + r) if carry else r
        odd = r.count("`") % 2 == 1
        return (r + "`" if odd else r).replace("``", ""), odd

    def wide(r: str, carry: bool) -> float:
        return _rich(bal(r, carry)[0], size).width

    segs = text.split(" · ")
    rows: list[str] = []
    cur = ""
    for k, seg in enumerate(segs):
        piece = seg + (" ·" if k < len(segs) - 1 else "")
        trial = f"{cur} {piece}" if cur else piece
        if cur and wide(trial, False) > width:
            rows.append(cur)
            cur = piece
        else:
            cur = trial
    rows.append(cur)
    out: list[str] = []
    carry = False
    for r in rows:                                   # a segment still too wide: break at spaces
        if wide(r, carry) <= width:
            row, carry = bal(r, carry)
            out.append(row)
            continue
        line = ""
        for w in r.split(" "):
            t = f"{line} {w}" if line else w
            if line and wide(t, carry) > width:
                row, carry = bal(line, carry)
                out.append(row)
                line = w
            else:
                line = t
        row, carry = bal(line, carry)
        out.append(row)
    g = VGroup(*[_rich(r, size, color) for r in out]).arrange(DOWN, aligned_edge=align, buff=buff)
    if g.width > width + 0.01:
        raise ValueError(f"fit_rows: {text!r} does not fit {width:.2f} at {size} pt")
    g.row_texts = out
    return g


def spark(r: float = 0.14, color: str = ERR) -> VGroup:
    """A small RED spark (an error flying)."""
    g = VGroup(*[Line(ORIGIN, UP * r, color=color, stroke_width=3).rotate(k * TAU / 8, about_point=ORIGIN)
                 for k in range(8)])
    g.add(Dot(radius=r * 0.3, color=color))
    return _keep(g)


def x_mark(h: float = 0.3) -> VGroup:
    """The RED ✗ on a wrong physics claim."""
    return _keep(cross_mark(h, ERR))


def tick_mark(h: float = 0.3) -> VMobject:
    """The GREEN tick on the voice (S01)."""
    return _keep(check_mark(h, OWN))


def question_card(text: str, size: float = 26, color: str = INK) -> VGroup:
    """A question card (S01's "Why is the sky blue?"): GREY frame, larger serif text. .frame .text"""
    t = label(text, size, color)
    fr = box(t.width + 0.7, t.height + 0.5, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.16)
    t.move_to(fr)
    g = VGroup(fr, t)
    g.frame, g.text = fr, t
    return g


def card_glyph(title: str, sub: str | None = None, color: str = S.GREY, w: float = 3.2,
               size: float = CAPTION, dashed: bool = False) -> VGroup:
    """A small card: serif title, optional GREY mono sub-line ("cli.py · lines 36–145"). .frame
    .title .sub"""
    t = label(title, size, INK)
    parts = [t]
    s = None
    if sub:
        s = _header_text(sub, size)
        parts.append(s)
    body = VGroup(*parts).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
    fr = box(max(w, body.width + 0.4), body.height + 0.36, color, fill=S.BG, fill_opacity=0.95,
             radius=0.12, dashed=dashed)
    body.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.2)
    g = VGroup(fr, body)
    g.frame, g.title, g.sub = fr, t, s
    return g


# ================================================================== README panels
def excerpt(name: str, first: int, last: int, cut_comments: bool = False,
            strip_emoji: bool = False) -> str:
    """Lines first..last (1-based, inclusive) of a tutorial file in assets/source. Never-shown
    lines raise."""
    d = _source_lines(name, range(first, last + 1), strip_emoji)
    res = [d[n] for n in range(first, last + 1)]
    if cut_comments:
        res = [cut_comment(s) for s in res]
    return "\n".join(res)


def source_line(name: str, n: int, strip_emoji: bool = False) -> str:
    """One line of a tutorial file (for excerpt_chip(..., line=...))."""
    return _source_lines(name, [n], strip_emoji)[n]


_MD_LINK = re.compile(r"!?\[([^\]]*)\]\([^)]*\)")


def md_plain(s: str) -> str:
    """A README line as plain text (script.md PANEL): '**' and backticks stripped, link targets
    dropped ([text](url) -> text), a leading list / quote / heading mark removed."""
    s = _MD_LINK.sub(r"\1", s)
    s = s.replace("**", "").replace("`", "")
    s = re.sub(r"(?<![\w*])\*(?=\S)([^*]+?)(?<=\S)\*(?![\w*])", r"\1", s)      # *emphasis*
    return re.sub(r"^\s*(?:[-*>]\s+|#+\s+)", "", s).rstrip()


def readme(repo: str, a: int, b: int | None = None) -> list[str]:
    """<repo>/README.md lines a..b (1-based, inclusive) as plain text rows (md_plain). b=None: one
    line. readme("ml-workflow", 218) -> ['This chains all four steps (…)'] ."""
    name = f"{repo}/README.md"
    rows = excerpt(name, a, a if b is None else b).split("\n")
    return [md_plain(r) for r in rows]


def _clip(s: str, start: str | None, end: str | None) -> str:
    """s from `start` (included) to `end` (included), '…' where something is left out."""
    i = 0 if start is None else s.find(start)
    if i < 0:
        raise ValueError(f"{start!r} not in {s!r}")
    j = len(s) if end is None else s.find(end, i)
    if j < 0:
        raise ValueError(f"{end!r} not in {s!r} after {start!r}")
    j = j if end is None else j + len(end)
    out = s[i:j].strip()
    return ("… " if i > 0 else "") + out + (" …" if j < len(s.rstrip()) else "")


def readme_panel(repo: str, first: int, last: int | None = None, clip: dict | None = None,
                 chars: int = 62, size: float = 22, width: float | None = None,
                 hi: dict | None = None) -> VGroup:
    """PANEL(<repo>/README.md: a–b): README text in the code-panel frame, as plain text (md_plain),
    line numbers kept in the header "repo/README.md · lines a–b" (+ " (excerpt)" when clipped).
    Blank lines are skipped. clip={n: (start, end)}: only that part of line n, '…' (GREY) where
    text is left out (start/end None = from the beginning / to the end). Rows wrap at `chars`
    characters (word boundaries; continuation rows under the line). hi={sub: colour} lights those
    phrases at once (.span(sub) finds them later). .frame .rows .header .span(sub, occurrence=0)
    -> glyphs across rows .bar(sub, colour) -> translucent bars behind the phrase (not added)."""
    last = first if last is None else last
    name = f"{repo}/README.md"
    raw = _source_lines(name, range(first, last + 1))
    texts = []
    for n in range(first, last + 1):
        s = md_plain(raw[n])
        if not s.strip():
            continue
        if clip and n in clip:
            s = _clip(s, *clip[n])
        texts.append(s)
    if not texts:
        raise ValueError(f"{name} {first}-{last}: nothing to show")
    rows = VGroup()
    pitch = line_pitch(size)
    for s in texts:
        for row, a, b, ind in wrap_output(s, chars, reach=chars // 3, hang=0):
            ln = mono_line(row, size, INK)
            ln.src, ln.src_span, ln.src_indent = s, (a, b), ind
            for sub in ("…", *MASKS):
                i = row.find(sub)
                while i >= 0:
                    glyph_range(ln, i, i + len(sub)).set_color(S.GREY)
                    i = row.find(sub, i + len(sub))
            ln.shift(np.array([0, -len(rows) * pitch, 0]) - ln.strut.get_corner(UP + LEFT))
            rows.add(ln)
    w = width or rows.width + 0.6
    if w > 12.95:
        raise ValueError(f"readme_panel {name}: {w:.1f} wide (> 12.9): lower chars=")
    h = len(rows) * pitch + 0.4
    fr = RoundedRectangle(width=w, height=h, corner_radius=0.15, stroke_color=S.GREY_DARK,
                          stroke_width=2).set_fill(PANEL, 1)
    fr.move_to(rows.get_center()).align_to(rows, LEFT).shift(LEFT * 0.3)
    fr.shift(UP * (rows.get_top()[1] + 0.2 - fr.get_top()[1]))
    where = f"line {first}" if first == last else f"lines {first}–{last}"
    if clip:
        where += " (excerpt)"
    head = _header_text(f"{name} · {where}").next_to(fr, UP, buff=0.1).align_to(fr, LEFT).shift(RIGHT * 0.12)
    g = VGroup(fr, rows, head)
    g.frame, g.rows, g.header, g.source_name = fr, rows, head, name

    def span(sub, occurrence=0):
        for r in rows:
            if sub in r.src:
                try:
                    return wrapped_glyphs([q for q in rows if q.src is r.src], sub, occurrence)
                except ValueError:
                    continue
        raise ValueError(f"{sub!r} not in {name} {first}-{last}")

    def bar(sub, color=TURN, opacity=0.22, occurrence=0):
        gl = span(sub, occurrence)
        out = VGroup()
        for r in rows:
            mine = [c for c in gl if c in r.glyphs.submobjects] if hasattr(r, "glyphs") else []
            if mine:
                part = VGroup(*mine)
                out.add(Rectangle(width=part.width + 0.1, height=r.strut.height + 0.06, stroke_width=0)
                        .set_fill(color, opacity).move_to([part.get_center()[0], r.strut.get_center()[1], 0]))
        return out

    g.span, g.bar = span, bar
    for sub, col in (hi or {}).items():
        span(sub).set_color(col)
    return g.move_to(ORIGIN)


def wrapped_glyphs(rows, sub: str, occurrence: int = 0) -> VGroup:
    """The glyphs of `sub` in ONE wrapped line, across the rows it folded into (rows carry .src,
    .src_span, .src_indent, as readme_panel's rows do)."""
    full = rows[0].src
    i = -1
    for _ in range(occurrence + 1):
        i = full.find(sub, i + 1)
    if i < 0:
        raise ValueError(f"{sub!r} not in {full!r}")
    j = i + len(sub)
    out = VGroup()
    for r in rows:
        a, b = r.src_span
        lo, hi = max(i, a), min(j, b)
        if lo < hi:
            out.add(*glyph_range(r, lo - a + r.src_indent, hi - a + r.src_indent))
    return out


# ================================================================== L15: tags, chips, small glyphs
def readme_example_tag() -> VGroup:
    """GREY 'README example' (the four probabilities of model-deployment/README.md:211)."""
    return grey_tag("README example")


def kfp_chip(s: str = "kfp 2.14.6 · read, not run") -> VGroup:
    """The PURPLE chip next to the quoted kfp error message (P1's reveal)."""
    return _keep(chip(s, TOOL, size=CAPTION))


def baked_chip(s: str = "value baked in at compile time") -> VGroup:
    """The GREY chip beside pipeline.yaml's constants (the bucket name)."""
    return _keep(chip(s, S.GREY, size=CAPTION))


def cost_tag(s: str = "billed per hour") -> VGroup:
    """GOLD tag: a machine is billing."""
    return _keep(tag(s, COST))


def free_tag(s: str = "costs nothing") -> VGroup:
    """GREEN tag: nothing is billed (the registry card)."""
    return _keep(tag(s, OWN))


def ok_badge(r: float = 0.17, color: str = OWN) -> VGroup:
    """The GREEN ✓ badge of a succeeded task (slide 37): a filled circle with a tick."""
    c = Circle(radius=r, stroke_color=color, stroke_width=2.5).set_fill(color, 0.9)
    t = check_mark(r * 1.25, S.BG, stroke=4).move_to(c)
    return _keep(VGroup(c, t))


def fail_badge(r: float = 0.17, color: str = ERR) -> VGroup:
    """The RED ✗ badge of a failed task."""
    c = Circle(radius=r, stroke_color=color, stroke_width=2.5).set_fill(color, 0.9)
    t = cross_mark(r * 1.0, S.BG, stroke=4).move_to(c)
    return _keep(VGroup(c, t))


def value_token(text: str, color: str = OWN, size: float = CAPTION) -> VGroup:
    """A value riding a wire / sitting in a socket: a GREEN pill with mono text ("9.0", a path).
    .box .text"""
    t = mono(text, size, INK)
    h = mono("|", size).height + 0.1
    b = RoundedRectangle(width=t.width + 0.24, height=h, corner_radius=h / 2, stroke_color=color,
                         stroke_width=2.5).set_fill(_mix(color, 0.35), 1)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return _keep(g)


def sticky_note(text: str, size: float = CAPTION, angle: float = 0.04) -> VGroup:
    """A GREY sticky note holding a hard-coded value (mono): no wire, no dependency. .frame .text"""
    t = mono(text, size, INK)
    fr = RoundedRectangle(width=t.width + 0.36, height=t.height + 0.32, corner_radius=0.05,
                          stroke_color=S.GREY, stroke_width=2).set_fill(_mix(S.GREY, 0.25), 1)
    t.move_to(fr)
    fold = Polygon(fr.get_corner(DOWN + RIGHT) + LEFT * 0.22, fr.get_corner(DOWN + RIGHT) + UP * 0.22,
                   fr.get_corner(DOWN + RIGHT), stroke_width=0).set_fill(S.GREY, 0.6)
    g = VGroup(fr, fold, t).rotate(angle)
    g.frame, g.text = fr, t
    return _keep(g)


def yaml_sheet(name: str = "sample-pipeline1.yaml", h: float = 0.9, color: str = OWN) -> VGroup:
    """The compiled pipeline: a GREEN file glyph with its mono name under it. .glyph .title"""
    gl = file_glyph(h, color)
    rows = VGroup(*[Line(LEFT * h * 0.22, RIGHT * h * 0.22, color=color, stroke_width=2)
                    for _ in range(3)]).arrange(DOWN, buff=h * 0.12).move_to(gl).shift(DOWN * h * 0.06)
    t = mono(name, CAPTION, color).next_to(gl, DOWN, buff=0.1)
    g = VGroup(gl, rows, t)
    g.glyph, g.title = VGroup(gl, rows), t
    return _keep(g)


def machine_glyph(w: float = 0.8, color: str = CTR, text: str | None = None) -> VGroup:
    """A small step machine (TEAL: a container on Google's machines; BLUE / GOLD for others):
    a rounded slab with two vents and a light; optional mono label under it. .slab .title"""
    h = w * 0.42
    slab = RoundedRectangle(width=w, height=h, corner_radius=0.06, stroke_color=color,
                            stroke_width=2.5).set_fill(_mix(color, 0.2), 1)
    vents = VGroup(*[Line(UP * h * 0.22, DOWN * h * 0.22, color=color, stroke_width=1.5) for _ in range(3)])
    vents.arrange(RIGHT, buff=w * 0.07).move_to(slab.get_left() + RIGHT * w * 0.25)
    light = Dot(radius=0.04, color=color).move_to(slab.get_right() + LEFT * w * 0.15)
    g = VGroup(slab, vents, light)
    g.slab, g.title = slab, None
    if text:
        t = mono(text, CAPTION, color).next_to(slab, DOWN, buff=0.08)
        g.add(t)
        g.title = t
    return _keep(g)


def bucket_glyph(text: str = BUCKET, w: float = 3.0, h: float = 1.1, color: str = CLOUD) -> VGroup:
    """A BLUE bucket: a rounded tub with its mono name on the rim; .inside() is a point inside.
    .frame .title"""
    body = Polygon([-w / 2, h / 2, 0], [w / 2, h / 2, 0], [w / 2 - 0.15, -h / 2, 0], [-w / 2 + 0.15, -h / 2, 0],
                   stroke_color=color, stroke_width=2.5).set_fill(color, 0.08)
    rim = Line([-w / 2 - 0.06, h / 2, 0], [w / 2 + 0.06, h / 2, 0], color=color, stroke_width=4)
    t = mono(text, CAPTION, color).next_to(rim, UP, buff=0.08)
    g = VGroup(body, rim, t)
    g.frame, g.title = body, t
    g.inside = lambda: body.get_center()
    return _keep(g)


def clock_badge(text: str, color: str = CLOCK) -> VGroup:
    """An ORANGE time chip ("1:00", "at 2:00")."""
    return _keep(chip(text, color, size=CAPTION, font=MONO))


# ================================================================== task nodes and wires (every DAG)
NODE_H = 0.62
SOCKET_W, SOCKET_H = 0.95, 0.42


class TaskNode(VGroup):
    """One task (a node): a WHITE-outlined rounded box with its mono name, an output socket per
    output (GREEN outline, empty until the task succeeds) and the state badges at the right end.

        n = TaskNode("square")                      # one socket ".output" on the right (flow="right")
        n = TaskNode("add", flow="down")            # the socket under the box (the toy's Y layout)
        n = TaskNode("split", outputs=("train_uri", "test_uri"), socket_labels=True)
        n = TaskNode("prep", outputs=())            # no socket: wires leave the box itself
    States (each returns a list of animations; play them): .run() YELLOW fill; .succeed(value=None)
    GREEN ✓ badge (+ the value token in the socket); .fail() RED; .skip() GREY dashed "never runs";
    .reset() pending. .show_labels() -> anims (the socket labels, hidden unless socket_labels=True).
    Points: .out_point(i=0) (socket i, or the box edge) .in_point(k=0, n=1) (k-th of n inputs).
    .token(value, i=0) -> a value_token placed on socket i (not added). Parts: .frame .title
    .sockets .socket_labels .ok .bad .ghost .values {i: token}. Size: name + 0.8 wide (min 1.3),
    0.62 tall (+0.42 per extra output); a socket adds 0.95 (right) or 0.42 (down)."""

    def __init__(self, title: str, outputs=(".output",), flow: str = "right", w: float | None = None,
                 h: float = NODE_H, size: float = 22, font: str = MONO, socket_labels: bool = False,
                 title_color: str = INK, **kw):
        super().__init__(**kw)
        self.flow, self.task = flow, title
        self.outputs = tuple(outputs)
        self.title = mono(title, size, title_color) if font == MONO else label(title, size, title_color)
        nout = len(self.outputs)
        h = max(h, nout * SOCKET_H + (nout - 1) * 0.08 + 0.2) if flow == "right" else h
        bw = max(w or 0, self.title.width + 0.8, 1.3)
        self.frame = RoundedRectangle(width=bw, height=h, corner_radius=0.12, stroke_color=INK,
                                      stroke_width=2.5).set_fill(S.BG, 1)
        self.title.move_to(self.frame).shift(LEFT * 0.14)
        self.add(self.frame, self.title)
        self.sockets = VGroup()
        self.socket_labels = VGroup()
        for i, name in enumerate(self.outputs):
            s = RoundedRectangle(width=SOCKET_W, height=SOCKET_H, corner_radius=0.08, stroke_color=OWN,
                                 stroke_width=2.5).set_fill(S.BG, 1)
            if flow == "right":
                ys = (nout - 1) / 2 - i
                s.move_to(self.frame.get_right() + RIGHT * (SOCKET_W / 2 - 0.02) + UP * ys * (SOCKET_H + 0.08))
            else:
                xs = (nout - 1) / 2 - i
                s.move_to(self.frame.get_bottom() + DOWN * (SOCKET_H / 2 - 0.02) + LEFT * xs * (SOCKET_W + 0.1))
            self.sockets.add(s)
            lb = mono(name, CAPTION, S.GREY)
            if flow == "right":
                lb.next_to(s, DOWN if nout == 1 else RIGHT, buff=0.08)
            else:
                lb.next_to(s, RIGHT, buff=0.1)
            self.socket_labels.add(lb)
        if len(self.sockets):
            self.add(self.sockets)
            self.add(self.socket_labels)
            if not socket_labels:
                _save_op(self.socket_labels, "_nop")
                _set_op(self.socket_labels, 0, "_nop")
        self._labels_shown = socket_labels
        anchor = self.frame.get_right() + LEFT * 0.27
        self.ok = _stage_hidden(self, ok_badge().move_to(anchor), "_nop")
        self.bad = _stage_hidden(self, fail_badge().move_to(anchor), "_nop")
        self.ghost = _stage_hidden(self, box(bw, h, STALE, dashed=True, radius=0.12, stroke=2.5)
                                   .move_to(self.frame), "_nop")
        self.values: dict = {}
        self.state = "pending"

    # -- points
    def out_point(self, i: int = 0):
        if len(self.sockets):
            s = self.sockets[i]
            return s.get_right() if self.flow == "right" else s.get_bottom()
        return self.frame.get_right() if self.flow == "right" else self.frame.get_bottom()

    def in_point(self, k: int = 0, n: int = 1):
        f = self.frame
        if self.flow == "right":
            span = min(f.height - 0.2, 0.3 * (n - 1))
            y = f.get_center()[1] + (span / 2 - (span / (n - 1) * k if n > 1 else 0))
            return np.array([f.get_left()[0], y, 0])
        span = min(f.width - 0.4, 0.8 * (n - 1))
        x = f.get_center()[0] - span / 2 + (span / (n - 1) * k if n > 1 else 0)
        return np.array([x, f.get_top()[1], 0])

    # -- states
    def _hide(self, *mobs) -> list:
        return [m.animate.set_opacity(0) for m in mobs if m.get_stroke_opacity() > 0 or m.get_fill_opacity() > 0]

    def run(self) -> list:
        self.state = "running"
        return [self.frame.animate.set_fill(_mix(TURN, 0.35), 1).set_stroke(TURN, 3),
                *self._hide(self.ok, self.bad, self.ghost)]

    def succeed(self, value: str | None = None, i: int = 0) -> list:
        self.state = "succeeded"
        out = [self.frame.animate.set_fill(S.BG, 1).set_stroke(INK, 2.5), _Reveal(self.ok, attr="_nop"),
               *self._hide(self.bad, self.ghost)]
        if value is not None:
            out += self.set_value(value, i)
        return out

    def fail(self) -> list:
        self.state = "failed"
        return [self.frame.animate.set_fill(_mix(ERR, 0.22), 1).set_stroke(ERR, 3),
                _Reveal(self.bad, attr="_nop"), *self._hide(self.ok, self.ghost)]

    def skip(self) -> list:
        self.state = "skipped"
        return [self.frame.animate.set_fill(S.BG, 1).set_stroke(opacity=0), self.title.animate.set_color(STALE),
                _Reveal(self.ghost, attr="_nop"), *self._hide(self.ok, self.bad)]

    def reset(self) -> list:
        self.state = "pending"
        out = [self.frame.animate.set_fill(S.BG, 1).set_stroke(INK, 2.5, opacity=1),
               self.title.animate.set_color(INK), *self._hide(self.ok, self.bad, self.ghost)]
        for tok in self.values.values():
            out += self._hide(tok)
        return out

    def token(self, value: str, i: int = 0) -> VGroup:
        """A value token on socket i (not added): the copy that rides a wire."""
        tok = value_token(value)
        if len(self.sockets):
            tok.move_to(self.sockets[i])
            if tok.width > SOCKET_W + 0.1 and self.flow == "right":     # a long value: overhang along the wire
                tok.align_to(self.sockets[i], LEFT)
        else:
            tok.move_to(self.out_point(i))
        return tok

    def set_value(self, value: str, i: int = 0) -> list:
        """Animations: `value` appears in socket i (a GREEN token; a long value overhangs it)."""
        tok = _stage_hidden(self, self.token(value, i), "_nop")
        old = self.values.get(i)
        self.values[i] = tok
        return [_Reveal(tok, attr="_nop")] + (self._hide(old) if old is not None else [])

    def show_labels(self) -> list:
        if self._labels_shown or not len(self.socket_labels):
            return []
        self._labels_shown = True
        return [_Reveal(self.socket_labels, attr="_nop")]


def _bezier(p0, p1, d) -> VMobject:
    """A smooth S-curve from p0 to p1 leaving and entering along direction d (unit vector)."""
    k = max(0.3, 0.45 * abs(np.dot(p1 - p0, d)))
    m = VMobject()
    m.set_points([p0, p0 + d * k, p1 - d * k, p1])
    return m


class Wire(VGroup):
    """An edge from a's output to b's input. kind: "data" (PINK solid: a .output wire, tokens ride
    it), "order" (PINK dashed: .after(), nothing rides it), "pending" (GREY dotted: a call's
    argument before the wire is drawn). The tip sits on b's input.

        w = Wire(a, b, "data", out=0, slot=0, slots=2)    # b's first of two inputs
        self.play(w.draw())                               # Create
        self.play(*w.restyle("data"))                     # pending -> solid (old out, new in)
        self.play(w.ride(tok))                            # MoveAlongPath (tok: a.token("9.0"))
    start=/end= override the two points; note="?" puts a GREY label at the midpoint (.note).
    .path (reference curve, not drawn) .line .tip .kind"""

    def __init__(self, a, b, kind: str = "data", out: int = 0, slot: int = 0, slots: int = 1,
                 start=None, end=None, note: str | None = None, flow: str | None = None, **kw):
        super().__init__(**kw)
        p0 = np.array(start if start is not None else a.out_point(out), dtype=float)
        p1 = np.array(end if end is not None else b.in_point(slot, slots), dtype=float)
        fl = flow or getattr(a, "flow", "right")
        d = RIGHT if fl == "right" else DOWN
        self.d = d
        self.path = _bezier(p0, p1, d)
        self.kind = kind
        self.path.set_stroke(width=0, opacity=0)          # an invisible member: it moves with the wire
        self.line, self.tip = self._build(kind)
        self.add(self.path, self.line, self.tip)
        self.note = None
        if note:
            self.note = label(note, CAPTION, S.GREY).move_to(self.path.point_from_proportion(0.5)) \
                .shift((UP if fl == "right" else RIGHT) * 0.25 + (RIGHT * 0.15 if fl != "right" else ORIGIN))
            self.add(self.note)

    def _build(self, kind: str):
        p1 = self.path.get_end()
        body = _bezier(self.path.get_start(), p1 - self.d * 0.14, self.d)
        if kind == "data":
            ln = body.set_stroke(EDGE, 4)
            col = EDGE
        elif kind == "order":
            ln = DashedVMobject(body.set_stroke(EDGE, 4), num_dashes=max(6, int(body.get_arc_length() * 5)),
                                dashed_ratio=0.55).set_stroke(EDGE, 4)
            col = EDGE
        else:
            ln = DashedVMobject(body.set_stroke(S.GREY, 2), num_dashes=max(8, int(body.get_arc_length() * 9)),
                                dashed_ratio=0.35).set_stroke(S.GREY, 2)
            col = S.GREY
        s = 0.17 if kind != "pending" else 0.13
        tip = Polygon(p1, p1 - self.d * s + _perp(self.d) * s * 0.55, p1 - self.d * s - _perp(self.d) * s * 0.55,
                      stroke_width=0).set_fill(col, 1)
        return ln, tip

    def draw(self, run_time: float = 0.6) -> AnimationGroup:
        return AnimationGroup(Create(self.line), FadeIn(self.tip), run_time=run_time)

    def restyle(self, kind: str) -> list:
        """Animations: the wire becomes `kind` in place (old fades out, then the new one in)."""
        line, tip = self._build(kind)
        anims = _swap_text(self, self.line, line) + _swap_text(self, self.tip, tip)
        self.line, self.tip, self.kind = line, tip, kind
        return anims

    def ride(self, token, run_time: float = 1.0):
        """MoveAlongPath of `token` (already on screen at the wire's start) to the wire's end."""
        return MoveAlongPath(token, self.path, run_time=run_time, rate_func=smooth)

    def light(self, color: str = TURN, run_time: float = 0.8):
        """A flash of `color` running along the wire."""
        return ShowPassingFlash(self.path.copy().set_stroke(color, 7, opacity=1), time_width=0.4, run_time=run_time)


def _perp(d):
    return np.array([-d[1], d[0], 0.0])


class Dag(Piece):
    """A DAG of TaskNodes and Wires, built at the positions given (a Piece: parts "node:<name>",
    "wire:<a>-><b>"; Dag(show=(...)) starts with only those parts visible).

        g = Dag({"prep": (-4, 0), "train_a": (0, 1), "train_b": (0, -1), "compare": (4, 0)},
                [("prep", "train_a"), ("prep", "train_b"), ("train_a", "compare"), ("train_b", "compare")])
    nodes: {name: (x, y)} (built in this order); edges: (a, b) or (a, b, kind) or (a, b, kind, out)
    with kind "data" / "order" / "pending". A target's inputs are ordered top to bottom (flow
    "right") or left to right (flow "down"). node_kw: TaskNode arguments for every node (titles=
    {name: shown title}; outputs={name: (...)} per node).
    .node[name] .wire[(a, b)] .run(*names) .succeed(name, value) .fail(name) .skip(name) -> anims
    .send(scene, a, b, value=None, run_time=1.0) plays a token riding a -> b (returns the token,
    on screen; FadeOut it or keep it) .restyle(a, b, kind) -> anims  .halo(names) -> VGroup of
    YELLOW outlines + wire copies (not added)  .longest(durations) -> (total, [names])
    .topo() -> names in topological order"""

    def __init__(self, nodes: dict, edges=(), flow: str = "right", titles: dict | None = None,
                 outputs: dict | None = None, show=None, node_kw: dict | None = None, **kw):
        super().__init__(**kw)
        self.flow = flow
        self.node: dict = {}
        self.wire: dict = {}
        self.edges = []
        for name, (x, y) in nodes.items():
            kwn = dict(node_kw or {})
            if outputs and name in outputs:
                kwn["outputs"] = outputs[name]
            n = TaskNode((titles or {}).get(name, name), flow=flow, **kwn)
            n.move_to([x, y, 0]).shift(-(n.frame.get_center() - np.array([x, y, 0])))
            self.node[name] = n
            self.part(f"node:{name}", n)
        norm = []
        for e in edges:
            a, b = e[0], e[1]
            kind = e[2] if len(e) > 2 else "data"
            out = e[3] if len(e) > 3 else 0
            norm.append((a, b, kind, out))
        for a, b, kind, out in norm:
            ins = [x for x in norm if x[1] == b]
            key = (lambda t: -self.node[t[0]].get_center()[1]) if flow == "right" else \
                (lambda t: self.node[t[0]].get_center()[0])
            ins.sort(key=key)
            k = [x[0] for x in ins].index(a)
            w = Wire(self.node[a], self.node[b], kind, out=out, slot=k, slots=len(ins))
            self.wire[(a, b)] = w
            self.edges.append((a, b, kind))
            self.part(f"wire:{a}->{b}", w)
        for n in self.node.values():             # nodes above wires (a wire never crosses a box)
            self.remove(n)
            self.add(n)
        if show is not None:
            for name in list(self.parts):
                if name not in show:
                    _save_op(self.parts[name])
                    _set_op(self.parts[name], 0)
                    self.parts[name].hidden = True

    def run(self, *names) -> list:
        return [a for n in names for a in self.node[n].run()]

    def succeed(self, name: str, value: str | None = None) -> list:
        return self.node[name].succeed(value)

    def fail(self, name: str) -> list:
        return self.node[name].fail()

    def skip(self, name: str) -> list:
        return self.node[name].skip()

    def restyle(self, a: str, b: str, kind: str) -> list:
        self.edges = [(x, y, kind if (x, y) == (a, b) else k) for x, y, k in self.edges]
        return self.wire[(a, b)].restyle(kind)

    def send(self, scene, a: str, b: str, value: str | None = None, run_time: float = 1.0):
        """Plays: a token (`value`, or the value in a's socket) appears on a's socket and rides
        the wire into b. Returns the token (on screen, not a member)."""
        src = self.node[a]
        if value is None:
            tok0 = src.values.get(0)
            value = tok0.text.text if tok0 is not None else "·"
        tok = src.token(value)
        scene.play(FadeIn(tok, scale=0.8), run_time=0.25)
        scene.play(self.wire[(a, b)].ride(tok, run_time=run_time))
        return tok

    def halo(self, names, color: str = TURN) -> VGroup:
        g = VGroup()
        for n in names:
            g.add(ring(self.node[n].frame, color, buff=0.1, stroke=4))
        for a, b in zip(names, names[1:]):
            if (a, b) in self.wire:
                g.add(self.wire[(a, b)].path.copy().set_stroke(color, 7, opacity=0.55))
        return g

    def topo(self) -> list:
        indeg = {n: 0 for n in self.node}
        for a, b, _ in self.edges:
            indeg[b] += 1
        order, ready = [], [n for n in self.node if indeg[n] == 0]
        while ready:
            n = ready.pop(0)
            order.append(n)
            for a, b, _ in self.edges:
                if a == n:
                    indeg[b] -= 1
                    if indeg[b] == 0:
                        ready.append(b)
        assert len(order) == len(self.node), "the graph has a cycle"
        return order

    def longest(self, durations: dict) -> tuple:
        """(total, path) of the longest path when each task takes durations[name]."""
        best = {}
        for n in self.topo():
            preds = [a for a, b, _ in self.edges if b == n]
            p = max(preds, key=lambda a: best[a][0]) if preds else None
            t0 = best[p][0] if p else 0
            best[n] = (t0 + durations[n], (best[p][1] if p else []) + [n])
        end = max(best, key=lambda n: best[n][0])
        return best[end]


def toy_dag(kind: str = "pending", show=None, socket_labels: bool = False) -> Dag:
    """The repo's sample_pipeline as slides 28–29's Y (flow "down"): square, square-2 on top, add,
    square-root under them; wires of `kind`. 5.0 x 4.6, centred at ORIGIN. Node names = the YAML
    task names (TOY)."""
    g = Dag({"square": (-1.35, 1.75), "square-2": (1.35, 1.75), "add": (0, 0.0), "square-root": (0, -1.75)},
            [("square", "add", kind), ("square-2", "add", kind), ("add", "square-root", kind)],
            flow="down", show=show, node_kw={"socket_labels": socket_labels})
    return g.move_to(ORIGIN)


def fork_join_dag(kind: str = "data", show=None) -> Dag:
    """V3's invented DAG (tag it illustration): prep -> train_a, train_b -> compare, flow right,
    three topological columns. 10.6 x 2.5, centred at ORIGIN."""
    g = Dag({"prep": (-4.2, 0), "train_a": (0, 0.8), "train_b": (0, -0.8), "compare": (4.2, 0)},
            [("prep", "train_a", kind), ("prep", "train_b", kind), ("train_a", "compare", kind),
             ("train_b", "compare", kind)], show=show)
    return g.move_to(ORIGIN)


def p2_dag(show=None) -> Dag:
    """P2's DAG (tag illustration): ingest → clean → train_cnn, train_tree, report; both trainings →
    compare; titles carry the minutes ("ingest · 2"); no sockets. 11.4 x 2.2, centred at ORIGIN.
    p2_dag().longest(P2_MIN) == (16, ['ingest', 'clean', 'train_cnn', 'compare'])."""
    t = {k: f"{k} · {v}" for k, v in P2_MIN.items()}
    g = Dag({"ingest": (-4.9, 0), "clean": (-2.2, 0), "train_cnn": (1.0, 0.75), "train_tree": (1.0, 0),
             "report": (1.0, -0.75), "compare": (4.6, 0.38)},
            [("ingest", "clean"), ("clean", "train_cnn"), ("clean", "train_tree"), ("clean", "report"),
             ("train_cnn", "compare"), ("train_tree", "compare")],
            titles=t, show=show, node_kw={"outputs": (), "h": 0.5, "size": CAPTION})
    return g.move_to(ORIGIN)


# ================================================================== V1 · the tracer (S02)
class Tracer(Dag):
    """V1: the toy graph (toy_dag layout, flow "down", 5.0 x 4.6 centred at ORIGIN) whose nodes
    start hidden and drop in one by one as the cursor steps through sample_pipeline's body.
    .drop(name) -> anims (the node falls 0.4 into place, its socket empty); .connect() -> anims
    (the GREY dotted "pending" connections draw; Wire.note "?" on square -> add when note=True);
    .stamp() -> anims (a PURPLE chip "component: square" above both square nodes; part "stamp");
    .machines() -> VGroup of TEAL machine glyphs under each node (not added; part of nothing);
    every Dag method (.run .succeed .restyle .send …)."""

    def __init__(self, show=(), note: bool = True, **kw):
        super().__init__({"square": (-1.35, 1.75), "square-2": (1.35, 1.75), "add": (0, 0.0),
                          "square-root": (0, -1.75)},
                         [("square", "add", "pending"), ("square-2", "add", "pending"),
                          ("add", "square-root", "pending")], flow="down", show=show, **kw)
        st = chip("component: square", TOOL, size=CAPTION)
        top = max(self.node["square"].get_top()[1], self.node["square-2"].get_top()[1])
        st.move_to([0, top + 0.35, 0])
        self.part("stamp", _keep(st), shown=False)
        if note:
            w = self.wire[("square", "add")]
            q = label("?", 26, S.GREY).move_to(w.path.point_from_proportion(0.5) + LEFT * 0.3)
            self.part("note", q, shown=False)
        self.move_to(ORIGIN)

    def drop(self, name: str) -> list:
        n = self.node[name]
        self._flag(n, False)
        _set_op(n)
        for m in (n.ok, n.bad, n.ghost, *n.values.values()):
            _set_op(m, 0, "_nop")
        if not n._labels_shown:
            _set_op(n.socket_labels, 0, "_nop")
        return [FadeIn(n, shift=DOWN * 0.4)]

    def connect(self) -> list:
        out = []
        for (a, b), w in self.wire.items():
            self._flag(w, False)
            _set_op(w)
            out.append(w.draw())
        if "note" in self.parts:
            out += self.parts_in("note")
        return out

    def stamp(self) -> list:
        return self.parts_in("stamp")

    def machines(self) -> VGroup:
        return VGroup(*[machine_glyph(0.6).next_to(n.sockets[0] if len(n.sockets) else n.frame, LEFT, buff=0.12)
                        for n in self.node.values()])


def compiler_roller(height: float = 4.8) -> VGroup:
    """V1's PURPLE compiler: a rounded bar `height` tall with the mono label "compiler" above.
    .bar .title"""
    bar = RoundedRectangle(width=0.32, height=height, corner_radius=0.16, stroke_color=TOOL,
                           stroke_width=3).set_fill(TOOL, 0.35)
    t = mono("compiler", CAPTION, TOOL).next_to(bar, UP, buff=0.1)
    g = VGroup(bar, t)
    g.bar, g.title = bar, t
    return _keep(g)


def press(scene, graph, sheet, run_time: float = 1.4):
    """Plays V1's compile: a PURPLE roller sweeps over `graph` left to right while the graph turns
    into `sheet` (a yaml_sheet placed where it should end up; under 1.5 s). The roller leaves;
    graph is gone from the scene, sheet stays."""
    r = compiler_roller(graph.height + 0.3).move_to(graph.get_left() + LEFT * 0.3)
    r.align_to(graph, DOWN).shift(DOWN * 0.15)
    scene.play(FadeIn(r), run_time=0.25)
    scene.play(r.animate.shift(RIGHT * (graph.width + 0.6)),
               FadeOut(graph, target_position=sheet.get_center(), scale=0.3,
                       rate_func=squish_rate_func(smooth, 0.15, 0.75)),
               FadeIn(sheet, scale=0.6, rate_func=squish_rate_func(smooth, 0.5, 1.0)),
               run_time=run_time)
    scene.play(FadeOut(r), run_time=0.25)


class SubmitBridge(Piece):
    """V1 (S02): the GREY laptop zone (left, "your laptop · compiles and submits") and the BLUE
    Vertex AI Pipelines zone (right) separated by a dashed border; a PURPLE arrow labelled
    `aiplatform` crosses it. Built in place: x -6.4..6.4, y from `bottom` to `top`.
    Parts: "laptop" "vertex" "arrow". .carry(sheet, run_time) -> anim (the sheet rides the arrow
    into the Vertex zone) .laptop_spot / .vertex_spot (points where things sit) .vertex_frame"""

    def __init__(self, top: float = 2.8, bottom: float = -1.2, split: float = -1.4, show=None, **kw):
        super().__init__(**kw)
        h, cy = top - bottom, (top + bottom) / 2
        lap = box(split + 6.4 - 0.25, h, LAPTOP, fill_opacity=0.04, radius=0.2).move_to(
            [(-6.4 + split - 0.25) / 2, cy, 0])
        lc = label("your laptop · compiles and submits", CAPTION, LAPTOP)
        lc.move_to(lap.get_corner(DOWN + LEFT), aligned_edge=DOWN + LEFT).shift(np.array([0.2, 0.12, 0]))
        if lc.width > lap.width - 0.3:
            lc = fit_rows("your laptop · compiles and submits", lap.width - 0.4, color=LAPTOP)
            lc.move_to(lap.get_corner(DOWN + LEFT), aligned_edge=DOWN + LEFT).shift(np.array([0.2, 0.12, 0]))
        self.part("laptop", VGroup(lap, lc))
        vx = box(6.4 - split - 0.25, h, CLOUD, fill_opacity=0.05, radius=0.25).move_to([(split + 0.25 + 6.4) / 2, cy, 0])
        vc = label("Vertex AI Pipelines · executes", CAPTION, CLOUD)
        vc.move_to(vx.get_corner(UP + RIGHT), aligned_edge=UP + RIGHT).shift(np.array([-0.2, -0.12, 0]))
        self.part("vertex", VGroup(vx, vc))
        self.vertex_frame = vx
        a = _arrow([split - 1.2, cy, 0], [split + 1.2, cy, 0], TOOL, 5)
        at = mono("aiplatform", CAPTION, TOOL).next_to(a, UP, buff=0.1)
        self.part("arrow", VGroup(a, at))
        self.arrow = a
        self.laptop_spot = np.array([(-6.4 + split - 1.2) / 2, cy + 0.2, 0])
        self.vertex_spot = np.array([(split + 1.2 + 6.4) / 2, cy, 0])
        if show is not None:
            for name in list(self.parts):
                if name not in show:
                    _save_op(self.parts[name])
                    _set_op(self.parts[name], 0)
                    self.parts[name].hidden = True

    def carry(self, sheet, run_time: float = 1.0):
        end = self.arrow.get_end() + RIGHT * (sheet.width / 2 + 0.2)
        return sheet.animate(run_time=run_time).move_to(end)


# ================================================================== V2 · the wire, and the no-wire contrast (S03)
class WirePlug(Piece):
    """V2's contrast row (tag it illustration): `prep` -> `train` (flow right), 6.0 x 3.6, built
    centred at ORIGIN. mode="wire": a PINK solid data wire; "after": a PINK dashed order wire
    (label "train(...).after(prep)" under it); "note": no wire, `train` holds a GREY sticky note
    `"gs://my-bucket/clean.csv"`, and a BLUE bucket below holds last week's GREY dashed file.
    Parts: "prep" "train" "wire" (wire / after) "note" "bucket" "old" (note mode).
    .start() -> anims (wire/after: prep runs; note: prep AND train run at once)
    .finish_prep(value=None) -> anims (prep ✓ [+ value in its socket])
    .stale_read() -> anims (note: a RED arrow from the old file into train, RED stamp "stale"; train ✓
        outlined RED) .fresh_lands() -> anims (prep's GREEN clean.csv lands on the old file, too late)
    .prep .train .wire_ (Wire or None) .old_file .bucket"""

    def __init__(self, mode: str = "wire", show=None, **kw):
        super().__init__(**kw)
        self.mode = mode
        self.prep = TaskNode("prep")
        self.train = TaskNode("train", outputs=())
        self.prep.shift(np.array([-1.9, 1.0, 0]) - self.prep.frame.get_center())
        self.train.shift(np.array([2.2, 1.0, 0]) - self.train.frame.get_center())
        self.wire_ = None
        self.part("prep", self.prep)
        self.part("train", self.train)
        if mode in ("wire", "after"):
            self.wire_ = Wire(self.prep, self.train, "data" if mode == "wire" else "order")
            self.part("wire", self.wire_)
            if mode == "after":
                lb = mono("train(...).after(prep)", CAPTION, EDGE).next_to(self.wire_, DOWN, buff=0.35)
                lb.set_x(0.15)
                self.part("after_label", lb)
        else:
            note_ = sticky_note(f'"{BUCKET}/clean.csv"')
            note_.next_to(self.train.frame, DOWN, buff=0.25).align_to(self.train.frame, RIGHT)
            self.part("note", note_)
            b = bucket_glyph(BUCKET, w=3.6, h=0.95).move_to([-0.6, -1.4, 0])
            self.bucket = b
            self.part("bucket", b)
            old = ghost_file("clean.csv · last week").move_to(b.inside() + UP * 0.02)
            self.old_file = old
            self.part("old", old)
        self.move_to(ORIGIN)
        if show is not None:
            for name in list(self.parts):
                if name not in show:
                    _save_op(self.parts[name])
                    _set_op(self.parts[name], 0)
                    self.parts[name].hidden = True

    def start(self) -> list:
        out = self.prep.run()
        if self.mode == "note":
            out += self.train.run()
        return out

    def finish_prep(self, value: str | None = None) -> list:
        return self.prep.succeed(value)

    def stale_read(self) -> list:
        a = _arrow(self.old_file.get_top() + UP * 0.05, self.train.frame.get_bottom() + DOWN * 0.05 + LEFT * 0.3, ERR, 4)
        st = stamp("stale", ERR).next_to(self.old_file, LEFT, buff=0.2)
        self._stale = VGroup(a, st)
        self.add(self._stale)
        _save_op(self._stale, "_nop")
        _set_op(self._stale, 0, "_nop")
        out = [_Reveal(self._stale, attr="_nop")]
        out += self.train.succeed()
        out.append(self.train.frame.animate.set_stroke(ERR, 3))
        return out

    def fresh_lands(self) -> list:
        new = file_row("clean.csv", OWN, OWN).move_to(self.old_file).align_to(self.old_file, LEFT)
        _stage_hidden(self, new, "_nop")
        self.fresh = new
        return [_Reveal(new, attr="_nop", shift=DOWN * 0.6), self.old_file.animate.set_opacity(0)]


# ================================================================== V3 · the wavefront and the Gantt chart (S04)
class Gantt(Piece):
    """V3's Gantt chart (S04; also P2's reveal): one row per task, bars on a time axis 0..t_max.
    Built centred at ORIGIN: width x (rows * row_h + 0.8); names (mono 20) right-aligned left of
    the axis start, inside `width`. Bars start hidden.

        gt = Gantt([("prep", 0, 2), ("train_a", 2, 8), ("train_b", 2, 6), ("compare", 8, 9)], 14)
        self.play(gt.grow("prep", run_time=1.0))     # a YELLOW bar grows left to right (linear)
        self.play(*gt.done("prep"))                  # it turns GREEN
    .grow(name, run_time=None) -> anim  .done(name) / .fail(name) -> anims  .set_span(name, a, b) ->
    anims (the bar moves / resizes)  .x_of(t)  .guide(t) -> PINK dashed vertical line (not added)
    .total(t, text=None) -> a YELLOW label under the axis at t (not added)  .bar[name] .names
    .axis  .row_y(name). unit: the axis caption ("min")."""

    def __init__(self, rows, t_max: float, width: float = 9.0, row_h: float = 0.46, unit: str = "min",
                 tick: float | None = None, name_w: float | None = None, **kw):
        super().__init__(**kw)
        self.t_max = t_max
        names = [mono(r[0], CAPTION, INK) for r in rows]
        nw = name_w or max(n.width for n in names) + 0.25
        x0, x1 = -width / 2 + nw, width / 2 - 0.15
        n = len(rows)
        top = (n * row_h) / 2 + 0.3
        self._axline = Line([x0, top - n * row_h - 0.05, 0], [x1, top - n * row_h - 0.05, 0], color=S.GREY,
                            stroke_width=2)
        self._y = {}
        self.bar: dict = {}
        self.spans = {}
        self.names = VGroup()
        for k, ((nm, a, b), t) in enumerate(zip(rows, names)):
            y = top - (k + 0.5) * row_h
            self._y[nm] = y
            t.move_to([x0 - 0.15 - t.width / 2, y, 0])
            self.names.add(t)
            bar = self._rect(a, b, y, TURN)
            self.bar[nm] = bar
            self.spans[nm] = (a, b)
        self.part("names", self.names)
        ay = top - n * row_h - 0.05
        ax = self._axline
        tick = tick or (1 if t_max <= 12 else 2 if t_max <= 24 else 5 if t_max <= 60 else 30)
        ticks = VGroup()
        labels = VGroup()
        t = 0.0
        while t <= t_max + 1e-6:
            x = self.x_of(t)
            ticks.add(Line([x, ay, 0], [x, ay - 0.08, 0], color=S.GREY, stroke_width=2))
            if t_max / tick <= 10 or round(t / tick) % 2 == 0:
                labels.add(mono(f"{t:g}", CAPTION, S.GREY).move_to([x, ay - 0.27, 0]))
            t += tick
        cap = label(unit, CAPTION, S.GREY).next_to(labels[-1] if len(labels) else ax, RIGHT, buff=0.2)
        if cap.get_right()[0] > width / 2:
            cap.next_to(ax, DOWN, buff=0.1).align_to(ax, RIGHT).shift(DOWN * 0.22)
        self.axis = VGroup(ax, ticks, labels, cap)
        self.part("axis", self.axis)
        for nm in self.bar:
            self.part(f"bar:{nm}", self.bar[nm], shown=False)
        self.move_to(ORIGIN)

    @property
    def ay(self) -> float:
        return self._axline.get_center()[1]

    def x_of(self, t: float) -> float:
        a, b = self._axline.get_start()[0], self._axline.get_end()[0]
        return a + (b - a) * t / self.t_max

    def row_y(self, name: str) -> float:
        return self.names[list(self._y).index(name)].get_center()[1]

    def _rect(self, a, b, y, color, h: float = 0.3):
        w = max(0.02, self.x_of(b) - self.x_of(a))
        return Rectangle(width=w, height=h, stroke_color=color, stroke_width=2).set_fill(color, 0.45) \
            .move_to([self.x_of(a) + w / 2, y, 0])

    def grow(self, name: str, run_time: float | None = None):
        bar = self.bar[name]
        a, b = self.spans[name]
        y = self.row_y(name)
        self._flag(bar, False)

        def upd(m, alpha):
            m.become(self._rect(a, a + (b - a) * max(alpha, 0.002), y, TURN))
        from manim import UpdateFromAlphaFunc
        return UpdateFromAlphaFunc(bar, upd, run_time=run_time or max(0.4, 0.25 * (b - a)), rate_func=linear)

    def done(self, name: str, color: str = OWN) -> list:
        return [self.bar[name].animate.set_fill(color, 0.45).set_stroke(color)]

    def fail(self, name: str) -> list:
        return self.done(name, ERR)

    def set_span(self, name: str, a: float, b: float) -> list:
        self.spans[name] = (a, b)
        bar = self.bar[name]
        tgt = self._rect(a, b, self.row_y(name), TURN)
        tgt.set_fill(bar.get_fill_color(), bar.get_fill_opacity()).set_stroke(bar.get_stroke_color(),
                                                                             opacity=bar.get_stroke_opacity())
        return [Transform(bar, tgt)]

    def guide(self, t: float, color: str = EDGE) -> VMobject:
        x = self.x_of(t)
        top = self.names.get_top()[1] + 0.05
        return DashedLine([x, top, 0], [x, self.ay, 0], color=color, stroke_width=3, dash_length=0.08)

    def total(self, t: float, text: str | None = None, color: str = TURN) -> VGroup:
        t_ = mono(text or f"{t:g}", CAPTION, color)
        return _keep(t_.move_to([self.x_of(t), self.ay - 0.62, 0]))


class Wavefront(VGroup):
    """V3's YELLOW wavefront: a translucent vertical band with a bright edge, `height` tall,
    centred on x. .to(x, run_time) -> anim (it slides)."""

    def __init__(self, height: float = 3.0, x: float = 0.0, y: float = 0.0, **kw):
        super().__init__(**kw)
        self.band = Rectangle(width=0.5, height=height, stroke_width=0).set_fill(TURN, 0.12)
        self.edge = Line(UP * height / 2, DOWN * height / 2, color=TURN, stroke_width=4)
        self.edge.move_to(self.band.get_right())
        self.add(self.band, self.edge)
        self.move_to([x, y, 0])

    def to(self, x: float, run_time: float = 1.0):
        return self.animate(run_time=run_time, rate_func=linear).shift(RIGHT * (x - self.edge.get_center()[0]))


# ================================================================== V4 · four ways to say "then" (S01, S05)
class ClockFace(VGroup):
    """An ORANGE clock (S01; tag illustration): face, 12 ticks, 12/3/6/9 in mono 20, hour and
    minute hands. ClockFace(r=1.0, hour=1, minute=0). .set_time(h, m, run_time) -> anims (the hands
    turn forward to h:m). .face .hands .time (h, m)"""

    def __init__(self, r: float = 1.0, hour: int = 1, minute: int = 0, color: str = CLOCK, **kw):
        super().__init__(**kw)
        self.r = r
        self.face = Circle(radius=r, stroke_color=color, stroke_width=4).set_fill(S.BG, 1)
        ticks = VGroup(*[Line(UP * r * (0.86 if k % 3 else 0.78), UP * r * 0.97, color=color,
                              stroke_width=3 if k % 3 == 0 else 2).rotate(-k * TAU / 12, about_point=ORIGIN)
                         for k in range(12)])
        nums = VGroup(*[mono(str(n), CAPTION, color).move_to(
            np.array([np.sin(a), np.cos(a), 0]) * r * 0.6) for n, a in ((12, 0), (3, PI / 2), (6, PI), (9, 1.5 * PI))])
        self.h_hand = Line(ORIGIN, UP * r * 0.45, color=INK, stroke_width=6)
        self.m_hand = Line(ORIGIN, UP * r * 0.72, color=INK, stroke_width=4)
        hub = Dot(radius=0.06, color=INK)
        self.hands = VGroup(self.h_hand, self.m_hand)
        self.add(self.face, ticks, nums, self.hands, hub)
        self.time = (0, 0)
        self._turn_to(hour, minute)

    def _angles(self, h, m):
        return -TAU * ((h % 12) / 12 + m / 720), -TAU * m / 60

    def _turn_to(self, h, m):
        ah, am = self._angles(h, m)
        c = self.face.get_center()
        self.m_hand.put_start_and_end_on(c, c + np.array([np.sin(-am), np.cos(-am), 0]) * self.r * 0.72)
        self.h_hand.put_start_and_end_on(c, c + np.array([np.sin(-ah), np.cos(-ah), 0]) * self.r * 0.45)
        self.time = (h, m)

    def set_time(self, h: int, m: int = 0, run_time: float = 1.0) -> list:
        h0, m0 = self.time
        dm = ((h * 60 + m) - (h0 * 60 + m0)) % 720 or 0
        c = self.face.get_center()
        self.time = (h, m)
        return [Rotate(self.m_hand, angle=-TAU * dm / 60, about_point=c, run_time=run_time, rate_func=smooth),
                Rotate(self.h_hand, angle=-TAU * dm / 720, about_point=c, run_time=run_time, rate_func=smooth)]


class Die(VGroup):
    """V4's die (tag illustration): a GREY rounded square showing the rolled minutes ("40" over
    "min"). .roll(value, run_time) -> anims (a quarter turn while the number swaps). .face .num"""

    def __init__(self, value: int | None = None, side: float = 1.1, **kw):
        super().__init__(**kw)
        self.face = RoundedRectangle(width=side, height=side, corner_radius=0.18, stroke_color=INK,
                                     stroke_width=3).set_fill(S.GREY_DARKER, 1)
        self.num = self._num(value)
        self.add(self.face, self.num)

    def _num(self, value):
        if value is None:
            pips = VGroup(*[Dot(radius=0.07, color=INK).move_to(self.face.get_center() + np.array([dx, dy, 0]))
                            for dx, dy in ((-0.25, 0.25), (0, 0), (0.25, -0.25))])
            return pips
        n = mono(str(value), 30, INK)
        u = label("min", CAPTION, S.GREY)
        return VGroup(n, u).arrange(DOWN, buff=0.04).move_to(self.face)

    def roll(self, value: int, run_time: float = 0.9) -> list:
        new = self._num(value)
        anims = _swap_text(self, self.num, new)
        self.num = new
        return [Rotate(self.face, angle=PI / 2, run_time=run_time, rate_func=smooth),
                AnimationGroup(*anims, run_time=run_time)]


class Leaderboard(VGroup):
    """V4's experiment-tracker leaderboard (tag illustration): a BLUE card titled "tracker · best
    first" with mono rows; rows=[(text, old)] (old=True: GREY dashed, a previous run). Room for
    `slots` rows from the start. .add_row(text, index, old=False) -> anims (the new row slides in;
    the rows below move down) .pick(i) -> VGroup (RED ring + "not this run", not added) .rows"""

    def __init__(self, rows=(("model · run 12 · acc 0.91", True),), title: str = "tracker · best first",
                 slots: int = 2, width: float = 4.6, **kw):
        super().__init__(**kw)
        self.pitch = 0.44
        self.w = width
        h = 0.16 + slots * self.pitch
        self.frame = box(width, h, CLOUD, fill=S.BG, fill_opacity=0.95, radius=0.12)
        self.title = label(title, CAPTION, CLOUD).next_to(self.frame, UP, buff=0.08).align_to(self.frame, LEFT) \
            .shift(RIGHT * 0.1)
        self.add(self.frame, self.title)
        self.rows = VGroup()
        for k, (t, old) in enumerate(rows):
            r = self._row(t, old).move_to(self._slot(k))
            self.rows.add(r)
        self.add(self.rows)

    def _slot(self, k: int):
        return self.frame.get_top() + DOWN * (0.08 + (k + 0.5) * self.pitch)

    def _row(self, text: str, old: bool):
        t = mono(text, CAPTION, S.GREY if old else INK)
        fr = box(self.w - 0.2, 0.38, STALE if old else OWN, fill_opacity=0.0 if old else 0.1, radius=0.08,
                 dashed=old)
        t.move_to(fr)
        g = VGroup(fr, t)
        g.frame, g.text = fr, t
        return g

    def add_row(self, text: str, index: int = 1, old: bool = False) -> list:
        r = self._row(text, old).move_to(self._slot(index))
        anims = [m.animate.move_to(self._slot(k + 1)) for k, m in enumerate(self.rows) if k >= index]
        _stage_hidden(self, r, "_nop")
        self.rows.insert(index, r)
        self.remove(r)
        return anims + [_Reveal(r, attr="_nop", shift=LEFT * 0.2)]

    def pick(self, i: int, text: str = "not this run") -> VGroup:
        rg = ring(self.rows[i].frame, ERR, buff=0.05, stroke=4)
        t = label(text, CAPTION, ERR).next_to(self.frame, UP, buff=0.08).align_to(self.frame, RIGHT)
        return _keep(VGroup(rg, t))


LANES = {
    "cron": ("cron offsets", CLOCK),
    "amp": ("background &", CLOCK),
    "tracker": ("event + tracker", INK),
    "edges": ("pipeline edges", EDGE),
}
TASKS3 = ("prep", "train", "deploy")


def lane_spans(lane: str, prep: float, train: float = V4_TRAIN, deploy: float = V4_DEPLOY,
               first_file: float = 60.0) -> tuple[dict, bool, dict]:
    """V4's rules (minutes after 1:00): ({task: (start, end)}, ok, flags {task: reason}).
    cron: prep 0, train 60, deploy 120 (ok while prep <= 60); amp: all start at 0 (never ok);
    tracker: the event fires on prep's first file (min(prep, first_file)), deploy takes the
    tracker's top row (never this run); edges: each starts at its predecessor's end (always ok)."""
    sp = {"prep": (0, prep)}
    flags: dict = {}
    if lane == "cron":
        sp["train"] = (60, 60 + train)
        sp["deploy"] = (120, 120 + deploy)
        ok = prep <= 60
        if not ok:
            flags["train"] = "half-written file"
    elif lane == "amp":
        sp["train"] = (0, train)
        sp["deploy"] = (0, deploy)
        ok = False
        flags["train"] = "nothing waits"
    elif lane == "tracker":
        fire = min(prep, first_file)
        sp["train"] = (fire, fire + train)
        sp["deploy"] = (fire + train, fire + train + deploy)
        ok = False
        if fire < prep:
            flags["train"] = "half-written"
        flags["deploy"] = "not this run"
    else:
        sp["train"] = (prep, prep + train)
        sp["deploy"] = (prep + train, prep + train + deploy)
        ok = True
    return sp, ok, flags


class FourLanes(Piece):
    """V4 (S05; one lane of it in S01): lanes that share one clock 1:00 → 5:00, each a mini Gantt
    with three sub-rows prep / train / deploy. Built in place: lane names x -6.4..-4.75 (sans 20,
    ≤ 2 rows), sub-row names to x -3.45, the timeline x -3.3..5.9 (axis labels on top at y `top`),
    the outcome mark at x 6.25. 4 lanes span y 2.8 .. -2.3 (lane_h 1.12).
        fl = FourLanes(prep=40)                     # lanes ("cron", "amp", "tracker", "edges")
        self.play(*fl.parts_in("lane:cron"))        # parts: "axis", "lane:<key>", "mark:<key>"
        self.play(*fl.set_prep(75))                 # every bar moves by its lane's rule; marks swap
    .bar(lane, task) .flag(lane, task, text=None) -> VGroup (RED outline + RED label, not added)
    .ok {lane: bool} .ticks (the cron lane's ORANGE ticks at 1:00 / 2:00 / 3:00) .x_of(minutes)
    .lane_y(lane)"""

    def __init__(self, lanes=("cron", "amp", "tracker", "edges"), prep: float = 40, top: float = 2.8,
                 lane_h: float = 1.12, x0: float = -3.3, x1: float = 5.9, hours: int = 4, show=None,
                 names: dict | None = None, **kw):
        super().__init__(**kw)
        self.lanes, self.t_max = tuple(lanes), hours * 60
        self.prep = prep
        ax_y = top - 0.2
        self._ref = Line([x0, ax_y, 0], [x1, ax_y, 0]).set_stroke(width=0, opacity=0)   # moves with the piece
        self.add(self._ref)
        self._lane_bg: dict = {}
        ax = VGroup()
        for k in range(hours + 1):
            x = self.x_of(k * 60)
            ax.add(mono(f"{1 + k}:00", CAPTION, S.GREY).move_to([x, ax_y, 0]))
            ax.add(DashedLine([x, ax_y - 0.22, 0], [x, ax_y - 0.22 - len(lanes) * lane_h, 0], color=S.GREY_DARK,
                              stroke_width=1.5, dash_length=0.06))
        self.part("axis", ax)
        self._bars: dict = {}
        self._lane_y: dict = {}
        self.ok: dict = {}
        self._marks: dict = {}
        y = ax_y - 0.3
        for lane in self.lanes:
            name, col = (names or {}).get(lane, LANES[lane][0]), LANES[lane][1]
            cy = y - lane_h / 2
            self._lane_y[lane] = cy
            grp = VGroup()
            bg = Rectangle(width=x1 - x0 + 0.2, height=lane_h - 0.1, stroke_width=0).set_fill(S.GREY_DARKER, 0.6)
            bg.move_to([(x0 + x1) / 2, cy, 0])
            self._lane_bg[lane] = bg
            nm = fit_rows(name, 1.65, color=col, buff=0.04).move_to([-5.6, cy, 0])
            grp.add(bg, nm)
            sub = 0.32
            spans, ok, _ = lane_spans(lane, prep)
            self.ok[lane] = ok
            for k, t in enumerate(TASKS3):
                ry = cy + sub * (1 - k)
                grp.add(mono(t, CAPTION, S.GREY).move_to([-3.45, ry, 0], aligned_edge=RIGHT))
                b = self._rect(*spans[t], ry)
                self._bars[(lane, t)] = b
                grp.add(b)
            if lane == "cron":
                self.ticks = VGroup(*[Line([self.x_of(m), cy + lane_h / 2 - 0.02, 0],
                                           [self.x_of(m), cy + sub * (1 - k) + 0.13, 0], color=CLOCK, stroke_width=4)
                                      for k, m in enumerate((0, 60, 120))])
                grp.add(self.ticks)
            self.part(f"lane:{lane}", grp)
            mk = self._mark(ok).move_to([6.25, cy, 0])
            self._marks[lane] = mk
            self.part(f"mark:{lane}", mk, shown=False)
            y -= lane_h
        if show is not None:
            for nm_ in list(self.parts):
                if nm_ not in show and not getattr(self.parts[nm_], "hidden", False):
                    _save_op(self.parts[nm_])
                    _set_op(self.parts[nm_], 0)
                    self.parts[nm_].hidden = True

    def x_of(self, minutes: float) -> float:
        a, b = self._ref.get_start()[0], self._ref.get_end()[0]
        return a + (b - a) * minutes / self.t_max

    def lane_y(self, lane: str) -> float:
        return self._lane_bg[lane].get_center()[1]

    def _rect(self, a, b, y, color=INK):
        w = max(0.04, self.x_of(b) - self.x_of(a))
        return RoundedRectangle(width=w, height=0.24, corner_radius=0.06, stroke_color=color,
                                stroke_width=2).set_fill(color, 0.3).move_to([self.x_of(a) + w / 2, y, 0])

    def _mark(self, ok: bool) -> VGroup:
        return ok_badge(0.2) if ok else fail_badge(0.2)

    def bar(self, lane: str, task: str):
        return self._bars[(lane, task)]

    def set_prep(self, prep: float, run_time: float = 1.0) -> list:
        """Animations: every lane re-lays its bars for this prep length; the shown marks swap to the
        new outcome."""
        self.prep = prep
        anims = []
        for lane in self.lanes:
            spans, ok, _ = lane_spans(lane, prep)
            for t in TASKS3:
                b = self._bars[(lane, t)]
                tgt = self._rect(*spans[t], b.get_center()[1])
                tgt.set_fill(b.get_fill_color(), b.get_fill_opacity()).set_stroke(b.get_stroke_color(),
                                                                                   opacity=b.get_stroke_opacity())
                anims.append(Transform(b, tgt, run_time=run_time))
            if ok != self.ok[lane]:
                old = self._marks[lane]
                new = self._mark(ok).move_to(old)
                if getattr(old, "hidden", False):
                    self._replace_hidden(lane, new)
                else:
                    anims += _swap_text(self, old, new)
                    self._marks[lane] = new
                    self.parts[f"mark:{lane}"] = new
                self.ok[lane] = ok
        return anims

    def _replace_hidden(self, lane, new):
        old = self._marks[lane]
        self.remove(old)
        self._marks[lane] = new
        self.part(f"mark:{lane}", new, shown=False)

    def flag(self, lane: str, task: str, text: str | None = None) -> VGroup:
        """A RED outline around one bar and its RED reason (default: the lane rule's flag) right of
        the bar (not added)."""
        b = self._bars[(lane, task)]
        _, _, flags = lane_spans(lane, self.prep)
        txt = text or flags.get(task, "")
        g = VGroup(ring(b, ERR, buff=0.05, stroke=3))
        if txt:                                   # left of the bar when its sub-row has room there
            t = label(txt, CAPTION, ERR).next_to(b, LEFT, buff=0.15)
            if t.get_left()[0] < self.x_of(0) + 0.05:
                t.next_to(b, RIGHT, buff=0.15)
            g.add(t)
        return _keep(g)


class Launcher(Piece):
    """V4's coda (S05, P3's reveal; tag illustration): a step that only launches work elsewhere.
    Three rows, not to scale: `train · step` (a short bar, its ✓ at its end), `training job ·
    another machine` (a long BLUE bar), `deploy` (starts at the step's ✓ along a PINK dashed edge,
    picking a GREY dashed "previous model"). 10.0 x 2.6, centred at ORIGIN.
    .sync() -> anims (sync=True: the step's bar stretches over the job, ✓ and deploy follow; deploy
    picks GREEN "this run's model") .job_fails() -> anims (the job ends RED, the step's badge turns
    RED, deploy turns GREY dashed: never runs). Parts: "rows" "step" "job" "edge" "deploy" "pick"."""

    def __init__(self, show=None, **kw):
        super().__init__(**kw)
        names = ("train · step", "training job · another machine", "deploy")
        self.ys = (0.85, 0.0, -0.85)
        lab = VGroup(*[label(n, CAPTION, c).move_to([-2.0, y, 0], aligned_edge=RIGHT)
                       for n, y, c in zip(names, self.ys, (INK, CLOUD, INK))])
        self.part("rows", lab)
        self.xa, self.x_step, self.x_job = -1.7, -0.9, 3.2
        self.step_bar = self._bar(self.xa, self.x_step, self.ys[0], INK)
        self.badge = ok_badge(0.16).move_to([self.x_step + 0.22, self.ys[0], 0])
        self.part("step", VGroup(self.step_bar, self.badge))
        self.job_bar = self._bar(self.x_step - 0.1, self.x_job, self.ys[1], CLOUD)
        self.part("job", self.job_bar)
        self.edge = DashedLine([self.x_step + 0.22, self.ys[0] - 0.18, 0], [self.x_step + 0.35, self.ys[2] + 0.16, 0],
                               color=EDGE, stroke_width=4, dash_length=0.08)
        self.part("edge", self.edge)
        self.dep_bar = self._bar(self.x_step + 0.35, self.x_step + 1.25, self.ys[2], INK)
        self.part("deploy", self.dep_bar)
        self.pick = ghost_file("previous model").next_to(self.dep_bar, DOWN, buff=0.12).align_to(self.dep_bar, LEFT)
        self.pick.shift(LEFT * 0.4)
        self.part("pick", self.pick)
        self.move_to(ORIGIN)
        if show is not None:
            for name in list(self.parts):
                if name not in show:
                    _save_op(self.parts[name])
                    _set_op(self.parts[name], 0)
                    self.parts[name].hidden = True

    def _bar(self, a, b, y, color):
        return RoundedRectangle(width=b - a, height=0.3, corner_radius=0.06, stroke_color=color,
                                stroke_width=2).set_fill(color, 0.3).move_to([(a + b) / 2, y, 0])

    def sync(self) -> list:
        dx = self.job_bar.get_right()[0] - self.step_bar.get_right()[0]
        sb = self.step_bar
        tgt = RoundedRectangle(width=sb.width + dx, height=sb.height, corner_radius=0.06, stroke_color=INK,
                               stroke_width=2).set_fill(INK, 0.3)
        tgt.move_to(sb.get_left() + RIGHT * tgt.width / 2)
        new_pick = file_row("this run's model", OWN, OWN).move_to(self.pick)
        new_pick.align_to(self.dep_bar, RIGHT).shift(RIGHT * dx)
        anims = [Transform(self.step_bar, tgt), self.badge.animate.shift(RIGHT * dx),
                 self.edge.animate.shift(RIGHT * dx), self.dep_bar.animate.shift(RIGHT * dx)]
        anims += _swap_text(self, self.pick, new_pick)
        self.pick = new_pick
        return anims

    def job_fails(self) -> list:
        bad = fail_badge(0.16).move_to(self.badge)
        x = fail_badge(0.16).move_to(self.job_bar.get_right() + RIGHT * 0.25)
        ghost = box(self.dep_bar.width, self.dep_bar.height, STALE, dashed=True, radius=0.06).move_to(self.dep_bar)
        _stage_hidden(self, x, "_nop")
        _stage_hidden(self, ghost, "_nop")
        anims = [self.job_bar.animate.set_stroke(ERR).set_fill(ERR, 0.3), _Reveal(x, attr="_nop")]
        anims += _swap_text(self.parts["step"], self.badge, bad)
        self.badge = bad
        anims += [self.dep_bar.animate.set_opacity(0), _Reveal(ghost, attr="_nop"), self.pick.animate.set_opacity(0)]
        return anims


# ================================================================== V5 · bucket → registry → endpoint → traffic (S06)
def gold_meter(r: float = 0.42, text: str = "$ / hour") -> VGroup:
    """The GOLD hourly meter: a half dial with a needle and a caption under it. .needle .center_
    .run(run_time) -> anim (the needle sweeps once, linear) .stop() -> anim (needle back to 0)."""
    arc = VMobject(stroke_color=COST, stroke_width=4)
    pts = [np.array([np.cos(a), np.sin(a), 0]) * r for a in np.linspace(PI, 0, 24)]
    arc.set_points_smoothly(pts)
    ticks = VGroup(*[Line(np.array([np.cos(a), np.sin(a), 0]) * r * 0.78, np.array([np.cos(a), np.sin(a), 0]) * r,
                          color=COST, stroke_width=2) for a in np.linspace(PI, 0, 6)])
    needle = Line(ORIGIN, np.array([-r * 0.8, 0, 0]), color=COST, stroke_width=4)
    hub = Dot(radius=0.05, color=COST)
    cap = label(text, CAPTION, COST).next_to(arc, DOWN, buff=0.12)
    g = VGroup(arc, ticks, needle, hub, cap)
    g.needle, g.hub = needle, hub
    g.run = lambda run_time=2.0: Rotate(needle, angle=-PI, about_point=hub.get_center(), run_time=run_time,
                                        rate_func=linear)
    g.stop = lambda run_time=0.6: Transform(needle, Line(hub.get_center(), hub.get_center() + LEFT * r * 0.8,
                                                         color=COST, stroke_width=4), run_time=run_time)
    return _keep(g)


def endpoint_plate(name: str = ENDPOINT_NAME, color: str = CLOUD) -> VGroup:
    """The endpoint as an address plate (BLUE, mono name). .frame .title"""
    t = mono(name, CAPTION, INK)
    fr = RoundedRectangle(width=t.width + 0.4, height=t.height + 0.26, corner_radius=0.06, stroke_color=color,
                          stroke_width=3).set_fill(_mix(color, 0.18), 1)
    t.move_to(fr)
    bolts = VGroup(*[Dot(radius=0.035, color=color).move_to(fr.get_corner(c) + (-c) * 0.09)
                     for c in (UP + LEFT, UP + RIGHT, DOWN + LEFT, DOWN + RIGHT)])
    g = VGroup(fr, bolts, t)
    g.frame, g.title = fr, t
    return _keep(g)


def registry_card(color: str = CLOUD) -> VGroup:
    """A Model Registry catalog card: two serif rows "where the files are" / "which container
    serves it" on a BLUE-outlined card. .frame .rows"""
    rows = VGroup(label("where the files are", CAPTION, INK), label("which container serves it", CAPTION, INK))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    fr = box(rows.width + 0.4, rows.height + 0.3, color, fill=S.BG, fill_opacity=1, radius=0.08)
    rows.move_to(fr)
    g = VGroup(fr, rows)
    g.frame, g.rows = fr, rows
    return g


class RegistryEndpoint(Piece):
    """V5 (S06): slide 12's layout redrawn, 9.6 x 4.9, centred at ORIGIN (use .rescale(k) beside a
    code panel; text keeps its size). Left: the GREY "Model Deployment CLI" container; right: the
    dashed BLUE GCP box with the bucket (GREEN model folder inside) and the Vertex AI panel holding
    "Model Registry" (top) and "Endpoints" (bottom).
    Parts: "cli" "gcp" "bucket" "folder" "vertex" "step1".."step5" (PINK numbered labels: get the
    saved model, update its signature, upload, register, deploy) "card" (+ PINK pointer to the
    folder) "callable" ("callable?" + RED ✗) "plate" "machine" "meter".
    .register() / .create_endpoint() / .deploy() -> anims (the card slides in; the plate rises; the
    machine slides under the plate, the GOLD meter appears)  .meter_run(run_time) -> anim
    .cleanup() -> anims (machine out, meter stops and goes, plate removed; card + folder stay)
    .route(start) -> PINK arrow from `start` to the plate (not added)  .plate_point()"""

    def __init__(self, show=None, **kw):
        super().__init__(**kw)
        cli = box(2.4, 1.3, LAPTOP, fill_opacity=0.06, radius=0.14, stroke=3).move_to([-4.6, -1.5, 0])
        cli_t = VGroup(label("Model Deployment", CAPTION, LAPTOP), label("CLI container", CAPTION, LAPTOP)) \
            .arrange(DOWN, buff=0.05).move_to(cli)
        self.part("cli", VGroup(cli, cli_t))
        self.cli_frame = cli
        gcp = box(7.2, 4.9, CLOUD, dashed=True, radius=0.25, stroke=2.5).move_to([1.4, 0, 0])
        gcp_t = label("GCP", CAPTION, CLOUD).move_to(gcp.get_corner(UP + LEFT), aligned_edge=UP + LEFT) \
            .shift(np.array([0.2, -0.12, 0]))
        self.part("gcp", VGroup(gcp, gcp_t))
        bk = bucket_glyph("bucket", w=1.8, h=0.95).move_to([-0.9, -1.45, 0])
        self.bucket = bk
        self.part("bucket", bk)
        fol = VGroup(folder_glyph(0.34, OWN), mono("model/", CAPTION, OWN)).arrange(RIGHT, buff=0.1).move_to(bk.inside())
        self.folder = _keep(fol)
        self.part("folder", fol, shown=False)
        vx = box(4.4, 4.5, CLOUD, fill_opacity=0.05, radius=0.16).move_to([2.6, -0.05, 0])
        vx_t = label("Vertex AI", CAPTION, CLOUD).move_to(vx.get_corner(UP + RIGHT), aligned_edge=UP + RIGHT) \
            .shift(np.array([-0.15, -0.08, 0]))
        reg = box(4.1, 1.75, CLOUD, fill_opacity=0.04, radius=0.12).move_to([2.6, 0.95, 0])
        reg_t = label("Model Registry", CAPTION, INK).move_to(reg.get_corner(UP + LEFT), aligned_edge=UP + LEFT) \
            .shift(np.array([0.12, -0.08, 0]))
        ep = box(4.1, 1.6, CLOUD, fill_opacity=0.04, radius=0.12).move_to([2.6, -1.45, 0])
        ep_t = label("Endpoints", CAPTION, INK).move_to(ep.get_corner(UP + LEFT), aligned_edge=UP + LEFT) \
            .shift(np.array([0.12, -0.08, 0]))
        self.reg_frame, self.ep_frame = reg, ep
        self.part("vertex", VGroup(vx, vx_t, reg, reg_t, ep, ep_t))
        # the catalog card, its pointer, "callable?"
        card = registry_card().move_to(reg.get_center() + UP * 0.05)
        ptr = _arrow(card.frame.get_left() + DOWN * 0.1, fol.get_top() + UP * 0.05, EDGE, 3)
        self.card = card
        self.part("card", VGroup(card, ptr), shown=False)
        cl = VGroup(label("callable?", CAPTION, INK), x_mark(0.24)).arrange(RIGHT, buff=0.15)
        cl.next_to(card, DOWN, buff=0.06).align_to(card, RIGHT)
        self.part("callable", cl, shown=False)
        # the endpoint plate, the machine, the meter
        plate = endpoint_plate().move_to(ep.get_center() + UP * 0.05)
        self.plate = plate
        self.part("plate", plate, shown=False)
        mach = VGroup(machine_glyph(0.9, CLOUD), mono("n1-standard-2", CAPTION, CLOUD)).arrange(RIGHT, buff=0.15)
        mach.next_to(plate, DOWN, buff=0.12).align_to(plate, LEFT)
        self.machine = _keep(mach)
        self.part("machine", mach, shown=False)
        meter = gold_meter(0.3, "$ / hour")
        meter.next_to(gcp, RIGHT, buff=0.15).set_y(ep.get_center()[1])
        self.meter = meter
        self.part("meter", meter, shown=False)
        # the five numbered steps (PINK)
        specs = [
            (1, "get the saved model", cli.get_top() + UP * 0.45),
            (2, "update its signature", cli.get_top() + UP * 1.05),
            (3, "upload", None),
            (4, "register", None),
            (5, "deploy", None),
        ]
        arrows = {
            3: _arrow(cli.get_right(), bk.frame.get_left() + RIGHT * 0.05, EDGE, 3),
            4: _arrow(bk.title.get_top() + UP * 0.05, reg.get_left() + DOWN * 0.4, EDGE, 3),
            5: _arrow(reg.get_bottom() + LEFT * 1.3, ep.get_top() + LEFT * 1.3, EDGE, 3),
        }
        for n, text, at in specs:
            b = step_badge(n, EDGE, radius=0.19)
            t = label(text, CAPTION, EDGE)
            g = VGroup(b, t).arrange(RIGHT, buff=0.12)
            g.add_to_back(RoundedRectangle(width=g.width + 0.2, height=g.height + 0.1, corner_radius=0.1,
                                           stroke_width=0).set_fill(S.BG, 0.92).move_to(g))   # over the dashed GCP line
            if at is not None:
                g.move_to(at).align_to(cli, LEFT)
                self.part(f"step{n}", _keep(g), shown=False)
                continue
            a = arrows[n]
            if n == 3:
                g.next_to(a, DOWN, buff=0.12)
            elif n == 4:
                g.next_to(a.get_center(), LEFT, buff=0.15)
            else:
                g.next_to(a, RIGHT, buff=0.12)
            self.part(f"step{n}", VGroup(a, _keep(g)), shown=False)
        self.move_to(ORIGIN)
        if show is not None:
            for name in list(self.parts):
                if name not in show and not getattr(self.parts[name], "hidden", False):
                    _save_op(self.parts[name])
                    _set_op(self.parts[name], 0)
                    self.parts[name].hidden = True

    def register(self) -> list:
        self._flag(self.parts["card"], False)
        _set_op(self.parts["card"])
        return [FadeIn(self.parts["card"], shift=RIGHT * 0.4)]

    def create_endpoint(self) -> list:
        self._flag(self.plate, False)
        _set_op(self.plate)
        return [FadeIn(self.plate, shift=UP * 0.3)]

    def deploy(self) -> list:
        for n in ("machine", "meter"):
            self._flag(self.parts[n], False)
            _set_op(self.parts[n])
        return [FadeIn(self.machine, shift=RIGHT * 0.6), FadeIn(self.meter)]

    def meter_run(self, run_time: float = 2.0):
        return self.meter.run(run_time)

    def meter_stop(self, run_time: float = 0.6):
        """Animation: the meter's needle drops back to zero (play it before cleanup())."""
        return self.meter.stop(run_time)

    def cleanup(self) -> list:
        _save_op(self.machine)
        anims = [self.machine.animate.shift(RIGHT * 0.6).set_opacity(0)]
        self._flag(self.machine, True)
        return anims + self.parts_out("meter", "plate")

    def plate_point(self):
        return self.plate.get_left()

    def route(self, start) -> Arrow:
        return _arrow(np.array(start, dtype=float), self.plate.get_left() + LEFT * 0.05, EDGE, 4)


def envelope(size: float = CAPTION) -> VGroup:
    """V5's prediction request: a PINK-outlined envelope card holding the mono JSON
    `{"bytes_inputs": {"b64": …}}` (… GREY). .frame .text"""
    t = mono('{"bytes_inputs": {"b64": …}}', size, INK, t2c={"…": S.GREY})
    fr = box(t.width + 0.4, t.height + 0.32, EDGE, fill=S.BG, fill_opacity=1, radius=0.08)
    t.move_to(fr)
    flap = VMobject(stroke_color=EDGE, stroke_width=2).set_points_as_corners(
        [fr.get_corner(UP + LEFT) + RIGHT * 0.06, fr.get_top() + DOWN * 0.12, fr.get_corner(UP + RIGHT) + LEFT * 0.06])
    g = VGroup(fr, flap, t)
    g.frame, g.text = fr, t
    return g


def signature_chain(steps=("decode", "float", "resize 224×224", "model"), color: str = TOOL) -> VGroup:
    """V5's serving signature unfolded (slides 13–14; cli.py 101–114): chips joined by '→'. The
    last chip (the model) is BLUE. .chips"""
    chips = []
    for k, s in enumerate(steps):
        chips.append(chip(s, CLOUD if k == len(steps) - 1 else color, size=CAPTION))
    row = []
    for k, c in enumerate(chips):
        if k:
            row.append(label("→", CAPTION, S.GREY))
        row.append(c)
    g = VGroup(*row).arrange(RIGHT, buff=0.15)
    g.chips = chips
    return _keep(g)


class ScoreBars(VGroup):
    """V5's four scores (tag README example: README_PROBS, model-deployment/README.md:211): BLUE
    bars over "class 0".."class 3" with the value above each; .argmax() -> anims (the tallest
    lights YELLOW, "argmax" under it). width x (max_h + 0.9), base at y 0 before moving."""

    def __init__(self, values=README_PROBS, width: float = 5.6, max_h: float = 1.8, **kw):
        super().__init__(**kw)
        n = len(values)
        self.values = values
        xs = np.linspace(-width / 2 + width / (2 * n), width / 2 - width / (2 * n), n)
        self.bars, self.nums, self.names = VGroup(), VGroup(), VGroup()
        top = max(values)
        for k, (x, v) in enumerate(zip(xs, values)):
            b = Rectangle(width=width / n * 0.55, height=max(0.03, v / top * max_h), stroke_color=CLOUD,
                          stroke_width=2).set_fill(CLOUD, 0.4)
            b.move_to([x, b.height / 2, 0])
            self.bars.add(b)
            self.nums.add(mono(f"{v:.4f}", CAPTION, INK).next_to(b, UP, buff=0.08))
            self.names.add(label(f"class {k}", CAPTION, S.GREY).move_to([x, -0.25, 0]))
        self.base = Line([-width / 2, 0, 0], [width / 2, 0, 0], color=S.GREY, stroke_width=2)
        self.add(self.base, self.bars, self.nums, self.names)

    def argmax(self) -> list:
        k = int(np.argmax(self.values))
        t = label("argmax", CAPTION, TURN).next_to(self.names[k], DOWN, buff=0.08)
        self.add(t)
        _save_op(t, "_nop")
        _set_op(t, 0, "_nop")
        return [self.bars[k].animate.set_fill(TURN, 0.6).set_stroke(TURN), _Reveal(t, attr="_nop")]


# ================================================================== V6 · one graph, two clouds (S07)
STEP_VARS = tuple(re.findall(r"\w+", source_line("ml-workflow-aws/src/workflow/cli.py", 322)
                                .split("[", 1)[1].split("]")[0]))     # step_collect … step_deploy_lambda


def _flow(mobs, width: float, buff: float = 0.12, gap: float = 0.16) -> list:
    """Centres for `mobs` laid out left to right in rows at most `width` wide (row 0 at y 0, x
    from 0)."""
    pts, x, y = [], 0.0, 0.0
    h = max(m.height for m in mobs)
    for m in mobs:
        if x > 0 and x + m.width > width:
            x, y = 0.0, y - h - gap
        pts.append(np.array([x + m.width / 2, y, 0.0]))
        x += m.width + buff
    return pts


class TwoClouds(Piece):
    """V6 (S07): the Cheese App chain as slide 37's zig-zag of four nodes (CHEESE, sans 22, no
    sockets) on a BLUE "Vertex AI Pipelines" region, PINK dashed .after() edges, and the bucket as
    a shared blackboard underneath (raw.zip, clean.zip, model/ hidden until chalked in). Built in
    place: x -6.4..6.4, y -2.4..2.75.
    Parts: "region" "chain" (Dag, .chain) "board" "file:raw.zip" "file:clean.zip" "file:model/"
    "sm" (the SageMaker Dag: SAGEMAKER, mono, solid PINK edges; hidden).
    .chain.run / .succeed / .restyle (Dag)  .chalk(file) -> anims  .reach(file, node) -> PINK
    arrow from the node down to the file (not added)  .to_sagemaker() -> anims (the four nodes
    and the board fade, the five SageMaker steps fade in in their place, the region's title swaps)
    .steps_list(order=STEP_VARS) -> `steps=[` + mono chips (step_collect … step_deploy_lambda, line 322)
    + `]`, flowed into ≤ 12.4-wide rows (not added; .chips by name) .shuffle(row, order) -> anims (the
    chips swap places; the graph does not move)."""

    def __init__(self, show=None, **kw):
        super().__init__(**kw)
        reg = box(12.8, 2.95, CLOUD, fill_opacity=0.04, radius=0.25).move_to([0, 1.27, 0])
        self.region_title = label("Vertex AI Pipelines", CAPTION, CLOUD).move_to(
            reg.get_corner(UP + LEFT), aligned_edge=UP + LEFT).shift(np.array([0.2, -0.1, 0]))
        self.part("region", VGroup(reg, self.region_title))
        self.region = reg
        xs, ys = (-4.75, -1.6, 1.6, 4.75), (1.75, 0.55, 1.75, 0.55)
        keys = ("collector", "processor", "training", "deploy")
        self.keys = keys
        nodes = {k: (x, y) for k, x, y in zip(keys, xs, ys)}
        self.chain = Dag(nodes, [(a, b, "order") for a, b in zip(keys, keys[1:])],
                         titles=dict(zip(keys, CHEESE)), node_kw={"outputs": (), "font": SANS})
        self.part("chain", self.chain)
        board = box(12.8, 1.35, CLOUD, fill=S.GREY_DARKER, fill_opacity=1, radius=0.18).move_to([0, -1.6, 0])
        bt = label("bucket · a shared blackboard", CAPTION, CLOUD).move_to(board.get_corner(UP + LEFT),
                                                                           aligned_edge=UP + LEFT).shift(np.array([0.2, -0.08, 0]))
        self.part("board", VGroup(board, bt))
        self.files = {}
        for name, x in zip(CHEESE_FILES, xs[:3]):
            f = file_row(name, OWN, OWN) if not name.endswith("/") else file_row(name, OWN, OWN)
            f.move_to([x, -1.75, 0])
            self.files[name] = f
            self.part(f"file:{name}", f, shown=False)
        sxs, sys_ = (-4.75, -2.375, 0.0, 2.375, 4.75), (1.75, 0.55, 1.75, 0.55, 1.75)
        sk = SAGEMAKER
        self.sm = Dag({k: (x, y) for k, x, y in zip(sk, sxs, sys_)}, [(a, b, "data") for a, b in zip(sk, sk[1:])],
                      node_kw={"outputs": (), "size": CAPTION})
        self.part("sm", self.sm, shown=False)
        if show is not None:
            for name in list(self.parts):
                if name not in show and not getattr(self.parts[name], "hidden", False):
                    _save_op(self.parts[name])
                    _set_op(self.parts[name], 0)
                    self.parts[name].hidden = True

    def node(self, key: str) -> TaskNode:
        return self.chain.node[key]

    def chalk(self, name: str) -> list:
        return self.parts_in(f"file:{name}")

    def reach(self, name: str, key: str, color: str = EDGE) -> Arrow:
        n = self.chain.node[key]
        return _arrow(n.frame.get_bottom(), self.files[name].get_top() + UP * 0.05, color, 3)

    def to_sagemaker(self) -> list:
        new_t = label("SageMaker Pipelines", CAPTION, CLOUD).move_to(self.region_title, aligned_edge=LEFT)
        anims = self.parts_out("chain", "board", *[f"file:{f}" for f in CHEESE_FILES])
        anims += self.parts_in("sm")
        anims += _swap_text(self.parts["region"], self.region_title, new_t)
        self.region_title = new_t
        return anims

    def steps_list(self, order=None, width: float = 12.4) -> VGroup:
        """The `steps=[…]` list of ml-workflow-aws/src/workflow/cli.py:322 as mono chips (STEP_VARS,
        or `order`), flowed into rows at most `width` wide, centred at ORIGIN (not added). .chips
        {name: chip} .order"""
        order = list(order or STEP_VARS)
        chips = {k: _keep(chip(k, CLOUD, size=CAPTION, font=MONO, pad_x=0.14)) for k in order}
        head = mono("steps=[", CAPTION, INK)
        tail = mono("]", CAPTION, INK)
        row = VGroup(head, *chips.values(), tail)
        row.chips, row.head, row.tail, row.flow_w = chips, head, tail, width
        for m, p in zip([head, *chips.values(), tail], _flow([head, *chips.values(), tail], width)):
            m.move_to(p)
        row.order = order
        return row.move_to(ORIGIN)

    def shuffle(self, row, order) -> list:
        """Animations: the chips take the places of the new `order` (the graph does not move)."""
        mobs = [row.head, *[row.chips[k] for k in order], row.tail]
        pts = _flow(mobs, row.flow_w)
        off = row.head.get_center() - pts[0]
        row.order = list(order)
        return [m.animate.move_to(p + off) for m, p in zip(mobs[1:-1], pts[1:-1])] + \
            [row.tail.animate.move_to(pts[-1] + off)]


# ================================================================== cards: invented code, ponders, takeaways
def illustration_card(lines, title: str | None = None, size: float = 22, color: str = S.GREY,
                      tag_: bool = True) -> VGroup:
    """Invented code (the hook's jobs, the sticky notes' snippets, the ponder snippets): mono rows
    on a GREY-outlined card with the `illustration` tag on its top-right corner; never a
    `path · lines` header (an optional GREY serif title above instead). .frame .rows .tag .title
    .bar(i, colour) -> a translucent bar behind row i (not added)."""
    rows = _mono_rows(list(lines), size, INK)
    fr = box(rows.width + 0.6, rows.height + 0.45, color, fill=S.BG, fill_opacity=0.96, radius=0.12)
    rows.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.3)
    g = VGroup(fr, rows)
    g.frame, g.rows, g.tag, g.title = fr, rows, None, None
    if tag_:
        tg = illustration_tag()
        tg.move_to(fr.get_corner(UP + RIGHT) + np.array([-0.2 - tg.width / 2, 0, 0]))
        g.add(tg)
        g.tag = tg
    if title:
        t = note(title).next_to(fr, UP, buff=0.08).align_to(fr, LEFT).shift(RIGHT * 0.1)
        if g.tag is not None and t.get_right()[0] > g.tag.get_left()[0] - 0.15:
            t.next_to(g.tag, UP, buff=0.08).align_to(fr, LEFT).shift(RIGHT * 0.1)
        g.add(t)
        g.title = t

    def bar(i, color=TURN, opacity=0.2):
        r = rows[i]
        return Rectangle(width=fr.width - 0.2, height=r.strut.height + 0.08, stroke_width=0) \
            .set_fill(color, opacity).move_to([fr.get_center()[0], r.strut.get_center()[1], 0])
    g.bar = bar
    return g


def _strip_md(s: str) -> str:
    return s.replace("**", "")


class MCQ(VGroup):
    """A multiple-choice ponder card (script.md PONDER): YELLOW frame, "Pause and ponder" and the
    `illustration` tag on top, the question (serif 22, `code` mono, wrapped to the card), an
    optional figure under it (e.g. p2_dag(), centred), four option rows (a YELLOW letter in a
    circle + the option, `code` mono) each with an empty reason slot under it, and the YELLOW
    timer bar. cols=2 lays the options out 2 x 2 (short options). width ≤ 12.8.
        card = mcq_ponder(self, question, ["`train(…)`", …], seconds=8)   # plays: in + timer
        self.play(*card.reveal(1, "named output → this run's file + the edge"))   # GREEN note
        self.play(*card.reason(0, "no edge → may start at once, reads last run's file"))   # RED
        self.play(FadeOut(card))
    .options[i] (.letter .text .bg) .slots[i] (centre of the reason slot) .timer .figure
    .reveal(i, note=None) -> anims (row fills YELLOW, ✓; optional GREEN note in its slot)
    .reason(i, text, colour=ERR) -> anims (the reason writes in under option i; raises if it would
    not fit one row) .drain(seconds) -> anim."""

    LETTERS = "ABCD"

    def __init__(self, question: str, options, figure=None, cols: int = 1, width: float = 12.6,
                 size: float = 22, **kw):
        super().__init__(**kw)
        inner = width - 0.7
        head = sans("Pause and ponder", 24, TURN, weight="BOLD")
        tg = illustration_tag()
        q = fit_rows(_strip_md(question), inner, size)
        parts = [q]
        self.figure = figure
        if figure is not None:
            parts.append(figure)
        col_w = inner if cols == 1 else (inner - 0.4) / 2
        self.options = []
        opt_rows = VGroup()
        slot_h = line_pitch(CAPTION) + 0.02
        for k, opt in enumerate(options):
            circ = Circle(radius=0.2, stroke_color=TURN, stroke_width=2.5).set_fill(S.BG, 1)
            let = sans(self.LETTERS[k], CAPTION, TURN, weight="BOLD").move_to(circ)
            letter = VGroup(circ, let)
            txt = fit_rows(_strip_md(opt), col_w - 0.75, size)
            row = VGroup(letter, txt).arrange(RIGHT, buff=0.22, aligned_edge=UP)
            letter.shift(DOWN * max(0.0, (txt[0].height - letter.height) / 2))
            slot = Rectangle(width=col_w - 0.6, height=slot_h, stroke_width=0).set_fill(opacity=0)
            slot.next_to(txt, DOWN, buff=0.04).align_to(txt, LEFT)
            cell = VGroup(row, slot)
            row.letter, row.text, row.slot = letter, txt, slot
            self.options.append(row)
            opt_rows.add(cell)
        if cols == 1:
            opt_rows.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        else:
            opt_rows.arrange_in_grid(rows=(len(options) + 1) // 2, cols=2, buff=(0.4, 0.08), flow_order="rd",
                                     col_alignments="ll")
        parts.append(opt_rows)
        body = VGroup(*parts).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        if figure is not None:
            figure.set_x(body.get_center()[0])
        frame_h = body.height + head.height + 0.95
        self.frame = RoundedRectangle(width=width, height=frame_h, corner_radius=0.2, stroke_color=TURN,
                                      stroke_width=3).set_fill(S.BG, 1)
        head.move_to(self.frame.get_corner(UP + LEFT), aligned_edge=UP + LEFT).shift(np.array([0.35, -0.22, 0]))
        tg.move_to(self.frame.get_corner(UP + RIGHT) + np.array([-0.3 - tg.width / 2, -0.22 - tg.height / 2, 0]))
        body.next_to(head, DOWN, buff=0.22).align_to(head, LEFT)
        self.timer = Line(self.frame.get_corner(DOWN + LEFT) + RIGHT * 0.3 + UP * 0.22,
                          self.frame.get_corner(DOWN + RIGHT) + LEFT * 0.3 + UP * 0.22, color=TURN, stroke_width=4)
        self.head, self.tag, self.question, self.body = head, tg, q, body
        self.slots = [o.slot.get_center() for o in self.options]
        self.add(self.frame, head, tg, body, self.timer)
        guard(self.frame.width <= 12.85, f"MCQ card {self.frame.width:.2f} wide (> 12.8)")

    def drain(self, seconds: float = 8.0):
        bar = self.timer
        return bar.animate(rate_func=linear, run_time=seconds).become(bar.copy().scale(0.001, about_point=bar.get_start()))

    def _slot_text(self, i: int, text: str, color: str):
        o = self.options[i]
        t = _rich(text, CAPTION, color)
        if t.width > o.slot.width + 0.6:
            raise ValueError(f"MCQ reason {text!r}: {t.width:.2f} wide (> {o.slot.width + 0.6:.2f}): shorten it")
        t.move_to(o.slot).align_to(o.slot, LEFT)
        return t

    def reveal(self, i: int, note_: str | None = None) -> list:
        o = self.options[i]
        bg = RoundedRectangle(width=o.width + 0.4, height=o.height + 0.14, corner_radius=0.1, stroke_width=0) \
            .set_fill(TURN, 0.22).move_to(o)
        tick = tick_mark(0.3).next_to(o, RIGHT, buff=0.2)
        o.bg = bg
        self.body.add_to_back(bg)
        _save_op(bg, "_nop")
        _set_op(bg, 0, "_nop")
        self.add(tick)
        _save_op(tick, "_nop")
        _set_op(tick, 0, "_nop")
        anims = [_Reveal(bg, attr="_nop"), _Reveal(tick, attr="_nop"), o.letter[0].animate.set_fill(TURN, 1),
                 o.letter[1].animate.set_color(S.BG)]
        if note_:
            anims += self.reason(i, note_, OWN)
        return anims

    def reason(self, i: int, text: str, color: str = ERR) -> list:
        t = self._slot_text(i, text, color)
        self.add(t)
        _save_op(t, "_nop")
        _set_op(t, 0, "_nop")
        return [_Reveal(t, attr="_nop", shift=RIGHT * 0.1)]


def mcq_ponder(scene, question: str, options, seconds: float = 8.0, figure=None, cols: int = 1,
               width: float = 12.6, bottom: float = -3.5, hide=()) -> MCQ:
    """Plays a multiple-choice ponder: the MCQ card fades in with its bottom at `bottom` (lower two
    thirds), `hide` mobjects fade out, then the timer drains over `seconds` (nothing else moves).
    Returns the card (on screen): reveal / reason it in the next SAY blocks, then FadeOut it."""
    card = MCQ(question, options, figure=figure, cols=cols, width=width)
    card.move_to([0, bottom + card.frame.height / 2, 0])
    guard(card.get_top()[1] <= LREF_BOTTOM - 0.05, f"MCQ card reaches y {card.get_top()[1]:.2f}: "
          "it would cover the lecture tag (shorten the question)")
    scene.play(FadeIn(card, scale=0.97), *[FadeOut(m) for m in hide], run_time=0.6)
    scene.play(card.drain(seconds))
    return card


def takeaway(text: str, width: float = 11.6, y: float = -1.4, size: float = 22) -> VGroup:
    """The YELLOW takeaway card (script.md TAKEAWAY): one row per " · " segment (a long segment
    wraps), serif `size` pt with `code` mono, at most 4 rows, centred on (0, y). Built with every
    row visible; write it with self.play(*card.write()) (rows in one by one) or FadeIn(card).
    .frame .rows .head .write(lag=0.6) -> [frame + head in, rows in]"""
    rows = VGroup()
    for seg in text.split(" · "):
        rows.add(*fit_rows(seg.strip(), width - 0.8, size, INK))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    guard(len(rows) <= 4, f"takeaway {text!r}: {len(rows)} rows (> 4): shorten it")
    head = sans("takeaway", CAPTION, TURN, weight="BOLD")
    fr = RoundedRectangle(width=max(width, rows.width + 0.8), height=rows.height + head.height + 0.75,
                          corner_radius=0.18, stroke_color=TURN, stroke_width=3).set_fill(_mix(TURN, 0.08), 1)
    head.move_to(fr.get_corner(UP + LEFT), aligned_edge=UP + LEFT).shift(np.array([0.35, -0.2, 0]))
    rows.next_to(head, DOWN, buff=0.18).align_to(head, LEFT)
    g = VGroup(fr, head, rows)
    g.frame, g.rows, g.head = fr, rows, head
    g.move_to([0, y, 0])
    guard(abs(g.get_left()[0]) <= SAFE_X and g.get_top()[1] <= SAFE_Y and g.get_bottom()[1] >= -SAFE_Y,
          f"takeaway card out of the frame ({g.get_left()[0]:.2f}, {g.get_top()[1]:.2f})")

    def write(lag: float = 0.6):
        return [FadeIn(VGroup(fr, head)),
                LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=lag)]
    g.write = write
    return g
