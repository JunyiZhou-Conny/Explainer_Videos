"""Shared code for AC215 L13 · Advanced Training Workflows, EXAM EDITION (concept-first, no README
tracker, no captures; code panels quote dlops-io/model-training @ b9aee1c and cell 38 of the
course notebook "Experiment Tracking using Weights & Bias", copied unchanged into assets/source/):
paths, narration, the semantic colours of BRIEF.md, source panels, tags, the multiple-choice ponder
card, and this video's set pieces V1-V5 of BRIEF.md (+ the S01/S08 miniatures and the data
version pair). The generic helpers (panels, cards, swap_text, Piece, fit_rows, guard) are ported
unchanged from L08's tested common.py; L08's captures, terminals, trackers and persona masks are
dropped (no person's name occurs in this lecture's quoted sources). Tested on screen by
build/common_test.py (CommonTest, LedgerTest, PackageTest, MirrorTest, BatchTest, JobTest,
MiniTest: explainer.check OK, preview sheets read).

Notes for scene authors
=======================

    from common import *      # every scene: SAY = NARRATION["S03"]; assert len(SAY) == n;
                              # one `with self.voiceover(SAY[i]) as vo:` per SAY line, in order
All text here is 20-34 pt (labels 20-24, takeaways 28). Never .scale() a group that holds text
below 1.0: Piece set pieces have .rescale(k) (shapes shrink, text keeps its size); keep_size(m)
marks your own chips. Methods return ANIMATIONS (play them) or MOBJECTS (placed, not added:
FadeIn them) unless they say "plays". Set pieces are built centred at ORIGIN unless they say "in
place". Layout asserts use guard() (raises locally, only warns on GitHub Actions); content
checks (option length, slices, narration) raise everywhere. Every piece computes positions from
its members at call time, so move it freely before or after building.

Frame budget. Safe frame x in [-6.6, 6.6], y in [-3.6, 3.6]; the lecture tag sits top right, y
3.13..3.6 (LREF_BOTTOM): keep anything wide below y 3.0. <= 3 visual groups at once.

Data and sources
    NARRATION["S01"] … ["S08"] (SAY lines of script.md)   TITLES[cls]   SPEC (video.yaml)
    src_path / source_text / excerpt(path, a, b) / source_line(path, n): paths under
        assets/source; "model-training/" may be left out ("package/trainer/task.py", "cli.sh",
        "colab/L13_wandb_tracking/cell-38.py").  shown_path(): the repo path without
        "model-training/"; the notebook cell -> NOTEBOOK_CELL "Experiment Tracking notebook ·
        training cell".
    Names: WB_PROJECT "cheese-training-vertex-ai"  RUN_NAME "mobilenetv2_train_base_True"
        CONFIG_KEYS (learning_rate, epochs, batch_size, model_name)  EXEC_KEY "execution_time"
        WANDB_PIN "wandb==0.15.11"  WANDB_VERSION "wandb 0.15.11"  ERR_LOG (65 chars: 10.9 wide
        in mono 20 pt, put version_chip() UNDER it, not beside)  ERR_LOGGER  BUCKET
        "$GCS_BUCKET_URI"  TARBALL  PACKAGE_URI  MODULE "trainer.task"  IMAGE_CPU
        "tf-cpu.2-17.py310"  IMAGE_GPU "tf-gpu.2-14.py310"  MACHINE_MULTI "n1-standard-32"
        GPU_NAME "T4"  SHIPPED_LIBS  JOB_STATES  PACKAGE_TREE
    Placeholders (drawn GREY by every panel and card): JOB_ID "‹job-id›", MACHINE_0, MACHINE_1.
        No real key, project id, bucket or job id ever: the W&B key is key_glyph().

Colours (BRIEF.md "Colours", binding)
    LAPTOP GREY (= SEALED: a finished run) · CLOUD BLUE (Vertex, the job VM, bucket, GPUs, wandb.ai
    rows) · CTR TEAL (model-training-cli, the prebuilt image) · SHIPPED ORANGE (= SYSTEM: what the
    image ships) · OWN GREEN (package/, trainer/, setup.py, tarball, replica weights, history
    ticks) · TOOL PURPLE (wandb SDK, the pen, pip, gcloud, tf.distribute, the pin) · ERR RED ·
    TURN YELLOW (active run, look here, ponder card, right option, takeaways) · COST GOLD (= KEY)
    · LOOKUP PINK (wandb.run, all-reduce, TF_CONFIG cable, batch-split arrows, gs:// paths,
    import search) · CONCEPT GREY dashed (lecture-only / made-up) · INK white.  SHADES: six
    GREEN replica-weight shades (one shade = in sync).

Panels and cards (code panels come AFTER the picture they prove)
    src_panel(path, a, b=None, wrap=True|{n: ["break before", …]}, focus=, join=, suffix=,
        max_rows=12) CODE(): header "path · lines a–b"; folded: src_panel(path, [42, 49, (55, 61)])
        -> "lines 42–61 (folded)" (pass suffix= or build the header text you need);
        raises when > 12 rows or > 12.9 wide. .bar(n, colour) .span(n, sub) .rows_of(n).
        Tested ranges: task.py 21–22, 96–100 (wrap=True), 152–153, 312–322, 324–331, 335–338;
        task_multi_gpu.py 286–289, 291–301, [(303, 306), (314, 315), (320, 321)] (wrap=True);
        setup.py [1, 5, (7, 13)]; package-trainer.sh 1–4; cli.sh 10–11, 30–37 (wrap=True),
        [(5, 10), 14] (wrap=True; 5–14 whole is 13 rows: too many); cli-multi-gpu.sh 6–12
        (wrap=True); cell-38.py [42, 49, (55, 61)] (wrap=True: line 60 is 69 characters).
    excerpt_chip(sub, "cli.sh · line 31 (excerpt)", line=source_line("cli.sh", 31))
    cmd_chip(cmd, note_)  card_rows(items, header=)  table_card(headers, rows)
    log_panel(lines, header)  output_box(lines | [(text, colour)], header=None) (schematic pip
    log lines: tag them illustration_tag())  question_card(text)  card_glyph(title, sub, colour)
    flow(["init", "fit · 2 epochs", "finish"]) GREY chips joined by → ; .items .light(i) -> anim
    lref("23–24") = lecture_ref(13, ...) top right;  lr = lref_swap(self, lr, "29") (plays; old may
    be None)   swap_text(parent, old, new) -> anims (never Transform one string into another)
    Counter(text, value) .count_to(n) / .freeze()   menu_path(items)   fit_rows(text, width)
Tags (GREY unless said): illustration_tag(note_) example_tag() ("example · not in the repo")
    concept_tag() (dashed "concept · lecture only") grey_tag(s) version_chip() (PURPLE "wandb
    0.15.11") cost_tag() (GOLD "$ while running") stamp(text) fix_chip(text) concept_box(text)
Glyphs: key_glyph() key_outline() padlock() x_mark() tick_mark() spark() file_row(name)
    ghost_file(name) container_box(title) laptop_zone() model_box() json_card() cost_tick()
    under(mob) strike(mob) ring(mob)

Exam frame
    takeaway("If the question says X, think Y.")  YELLOW, 28 pt, rows broken to fit 12.0,
        centred at ORIGIN (one group); the scene's closing line, then an empty frame.
    mcq_card(question_rows (1-2), options (4, <= 46 characters, `code` mono), answer=False)
        12.4 wide, centred, 4.6-5.0 high: "Pause and ponder" header, question 24 pt, options A-D
        22 pt with letter badges, timer bar card[3]. ponder_mcq(self, card, seconds=10) plays the
        fade-in and the silent drain (FadeOut the card yourself). The answer: a NEW card with
        answer=True (header "Answer", no timer) faded in at the same place, then
        self.play(*card.mark_right(i)) (YELLOW outline) and self.play(*card.reason(i, "a name
        labels the row, logs nothing")) per wrong option (RED reason swaps in place; <= ~10.5
        wide). .options[i] (.badge .text) .dim_option(i)

Set pieces (Piece = VGroup with named parts: piece.reveal(scene, *names) / .hide plays;
    self.play(*piece.parts_in("a")); a part not shown yet is a member at opacity 0 (never FadeOut
    a part, FadeOut the whole piece))
  V1 the run ledger (S01-S03, S07 miniature)
    Ledger(slots=2, full=False, width=9.6)  9.6 x (0.9 + slots·(row_h + 0.2)): BLUE frame,
       "wandb.ai · project cheese-training-vertex-ai", illustration tag, dashed row places.
       .slot(i) .new_row(i, name) -> LedgerRow placed in place i (FadeIn(row, shift=LEFT)).
       full=True rows are 2.3 high (1 slot: 9.6 x 3.4); compact rows 1.15 (2 slots: 9.6 x 3.6).
    LedgerRow(name=RUN_NAME, width=9.0, full=True, slots=6): name, (full) 2 rows of config-chip
       slots + system tile, the "history" strip with 6 tick slots. Parts (hidden): "finished"
       "lock" "cfg:<key>" "system" "traces" (reveal with anim=Create) "empty" (RED dashed strip).
       .clip(key) .tick(k) (1-based) .set_count("6 entries · 1 run") .activate() .seal() -> anims;
       .slot_point(k) .pointer_point() .ticks
    RunPointer(tail, none_at=None)  PINK `wandb.run` label (right end at tail) + arrow + GREY
       dashed `None` slot (default 1.0 below the label). .point_to(row.pointer_point()) /
       .to_none() -> anims.  Leave ~2 units left of the ledger for it.
    Pen(name="callback")  1.4 x 1.0, PURPLE; .tip() .move_tip(point) -> anim (e.g.
       row.slot_point(k) + UP * 0.25, then row.tick(k)); .wear("created during row 1") -> anims
       (a GREY tag right of the name, rides along)
    EpochBar(n, width=4.0, caption="fit · 2 epochs")  .run(i) -> anim (segment i fills) .end(i)
    BracketTimeline(lines=(init, fit · 2, finish, init, fit · 4, finish, fit))  1.5 x 3.3:
       YELLOW brackets per init…finish span, RED ✗ on the stray fit; .tick_points(i, n) (where
       row i's ticks go: put history_tick() there) .rows .brackets .cross
    empty_chart("loss" | "accuracy")  3.6 x 2.0 RED dashed outline, "no data logged";
       curve_in(chart, kind) -> the schematic curve (Create it; fade chart.caption)
  V2 what pip unwraps (S04)
    PackageTree()  4.4 x 3.8 (8 rows at 22 pt): .row(name) .row_point(level, after) .pitch
    ghost_module("augment.py")  GREY dashed, 22 pt (+ illustration_tag(), example_tag())
    Scanner(width)  PINK bar + `find_packages()` at its right end; place the bar over the
       tree, then self.play(*scanner.sweep(tree, lit=("trainer/",), dim=("setup.cfg",
       "PKG-INFO"))) (also accepts a ghost_module-extended tree's rows via tree.tree)
    shopping_list()  4.2 x 1.4: "install_requires · from PyPI" + PURPLE `wandb==0.15.11` chip
    pypi_cloud()  2.2 GREY cloud "PyPI";  tarball("trainer.tar.gz") 2.3 x 1.1 GREEN;
    bucket(BUCKET) 2.5 x 1.7 BLUE pail + PINK path (.mouth())
    JobVM(image=IMAGE_CPU)  7.0 x 3.8: BLUE VM, TEAL prebuilt image, ORANGE shelf "in the
       image" (TensorFlow, scikit-learn, requests), GREEN shelf "installed by pip"; parts
       "wandb" "trainer" hidden: .install(name) -> anims; .search() -> anims (PINK beam over
       the shelves; FadeOut vm.beam after) .log_point() (under the VM: the pip log's top)
  V3 mirrors vs islands (S05)
    StrategyLadder()  12.8 x 2.3 (slide 27): .rows[i] (.left .right .frame); part "pin"
       (YELLOW "the repo is here", hidden: ladder.reveal(self, "pin")); .light(i) -> anims
    Machine(n_gpus=2, title=MACHINE_MULTI, subtitle=None, width=5.4, height=3.4 (>= 3.4 with a
       strategy), strategy="MirroredStrategy", shard=None)  BLUE box with T4 chips; parts
       "replicas" "strategy" "ring" "shard" hidden. .step(shade) -> ONE animation (gradients
       rise, all-reduce, the same update back down) .drift(shade) -> anims (no ring)
       .replicas .gpus .ring_center()   Two machines side by side: width 5.0 at x ±3.25.
    gpu_chip()  Replica(shade) .set_shade(c)  cable(a, b) (PINK)  no_wire(a, b) (GREY dashed +
       RED ✗)  span_ring(a, b) (one PINK ring over all replicas)  delta_mark() (RED Δ +
       "different weights")  tf_config_card(i) 5.5 x 2.4 GREY dashed (placeholders; +
       illustration_tag("plain TF example") and concept_tag()); two fit under two machines.
  V4 the batch splitter (S06)
    BatchTray(n, cols=None, cell=0.2) GREEN tray of n squares, caption `dataset.batch(n)`;
       .slices(k) .split_to(points, k) -> anims (lands slices on gpu_grid slots)
    gpu_grid(k, per_row=4)  BLUE chips in a PURPLE MirroredStrategy frame, .slot(i) .chips
    BatchDial(n)  2.5 wide knob + `batch(n)`; .turn_to(n) -> anims
  V5 request clock vs job ticket (S07)
    handler_box("POST /retrain")  2.6 x 1.5 (illustration_tag() it)
    LifetimeRings()  in place, centred (0, -0.35): request 6.4 x 2.9 / server 9.6 x 4.0 / job
       12.8 x 5.4; parts "request" "server" "job" hidden; .ring(name) .inner_center()
    TrainingBar(width=3.0) "training · ~1 hour": .grow(frac) -> anim .snap() -> anims (RED +
       crack) .track .fill
    JobTicket()  2.6 x 0.95 BLUE ticket "custom job" + ‹job-id›   StateChips() 8.1 wide,
       .light(i) -> anims (SUCCEEDED lights GREEN)   CostMeter() 1.9 x 0.8 GOLD "$ while
       running"; .run(run_time) / .stop() -> anim
  S02 / S08
    DataVersion()  6.7 x 1.2: "snapshot" (BLUE bucket) — PINK "content hash" — GREEN "version
       record"; part "link" hidden; .flash() -> anim
    Miniature(kind) / miniature(kind)  kind in MINI_KINDS (run, package, gpus, batch, job,
       data), <= 1.8 x 1.5 with its 22 pt caption; .crack() -> anims (RED crack) .replay() -> ONE
       animation (~1 s).  miniature_row(kinds=MINI_KINDS[:5]) 10.5 wide; .items[kind]
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
    Arc,
    Arrow,
    Circle,
    Create,
    DashedLine,
    DashedVMobject,
    DecimalNumber,
    Dot,
    FadeIn,
    FadeOut,
    GrowArrow,
    GrowFromEdge,
    Indicate,
    LaggedStart,
    Line,
    ManimColor,
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
    Wait,
    linear,
    rush_into,
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
from explainer.components import connect, pause_and_ponder, ponder_card  # noqa: F401,E402
from explainer.devops import (  # noqa: F401,E402  (re-exported for the scenes)
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
    file_tree,
    folder_glyph,
    glyph_range,
    label,
    laptop,
    lecture_ref,
    line_bar,
    line_pitch,
    machine_box,
    mono,
    mono_line,
    server,
    step_badge,
    substring,
    tag,
    warning_sign,
)
from explainer.script import load_narration  # noqa: E402

# ------------------------------------------------------------------ paths and data
HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
ASSETS = PROJECT / "assets"
SOURCE = ASSETS / "source"

SPEC = yaml.safe_load((PROJECT / "video.yaml").read_text())
TITLES = {s["cls"]: s["title"] for s in SPEC["scenes"]}
_script = PROJECT / "script.md"
NARRATION = load_narration(_script) if _script.exists() else {}

# ------------------------------------------------------------------ semantic colours (BRIEF.md "Colours")
LAPTOP = S.GREY          # your laptop, the notebook tab
SEALED = S.GREY          # a finished (sealed) W&B run's outline
CLOUD = S.BLUE           # Vertex AI, the job VM, the bucket, the job machine's GPUs, wandb.ai and its run rows
CTR = S.TEAL             # model-training-cli, the prebuilt training image tf-cpu.2-17.py310 / tf-gpu.2-14.py310
SHIPPED = S.ORANGE       # what the prebuilt image already ships (TensorFlow, scikit-learn, requests)
SYSTEM = SHIPPED
OWN = S.GREEN            # package/, trainer/, setup.py, the tarball; replica weights; history ticks
TOOL = S.PURPLE          # the wandb SDK and its callback (the pen), gcloud, pip, tf.distribute, the wandb pin
ERR = S.RED              # ModuleNotFoundError, wandb.errors.Error, a cut request, diverged weights, wrong options
TURN = S.YELLOW          # the active run's outline, look here now, ponder card, right option, takeaways
COST = S.GOLD            # money: the "$ while running" meter; the W&B key glyph (never a value)
KEY = COST
LOOKUP = S.PINK          # wandb.run pointer, all-reduce wires, TF_CONFIG cable, batch-split arrows, gs:// paths, import search
CONCEPT = S.GREY         # dashed: lecture-only or hypothetical (One Device / Multi Worker, TF_CONFIG, augment.py)
INK = S.WHITE
DIMMED = S.GREY

# ------------------------------------------------------------------ placeholders (drawn GREY, never real values)
JOB_ID = "‹job-id›"
MACHINE_0, MACHINE_1 = "‹machine-0›", "‹machine-1›"
PLACEHOLDERS = (JOB_ID, MACHINE_0, MACHINE_1)
EMOJI: frozenset = frozenset()


def _ph(s) -> str:
    """Text as shown (this lecture's sources hold no person's name: nothing is masked; the
    placeholders above are drawn GREY by every panel and card)."""
    return str(s)


# ------------------------------------------------------------------ the running example (script.md)
WB_PROJECT = "cheese-training-vertex-ai"          # task.py:314
RUN_NAME = "mobilenetv2_train_base_True"          # task.py:263 + cli.sh:19 (--model_name=mobilenetv2,--train_base)
CONFIG_KEYS = ("learning_rate", "epochs", "batch_size", "model_name")   # task.py:316-319
EXEC_KEY = "execution_time"                       # task.py:336
WANDB_PIN = "wandb==0.15.11"                      # setup.py:5
WANDB_VERSION = "wandb 0.15.11"
ERR_LOG = "wandb.errors.Error: You must call wandb.init() before wandb.log()"
ERR_LOGGER = "You must call `wandb.init()` before WandbMetricsLogger()"
BUCKET = "$GCS_BUCKET_URI"
TARBALL = "cheese-app-trainer.tar.gz"
PACKAGE_URI = f"{BUCKET}/{TARBALL}"
MODULE = "trainer.task"
IMAGE_CPU = "tf-cpu.2-17.py310"                   # cli.sh:31
IMAGE_GPU = "tf-gpu.2-14.py310"                   # cli-multi-gpu.sh:8
MACHINE_MULTI = "n1-standard-32"                  # cli-multi-gpu.sh:6
GPU_NAME = "T4"
SHIPPED_LIBS = ("TensorFlow", "scikit-learn", "requests")
JOB_STATES = ("QUEUED", "PENDING", "RUNNING", "SUCCEEDED")   # digest §3.4
NOTEBOOK_CELL = "Experiment Tracking notebook · training cell"
PACKAGE_TREE = ("package/", "  setup.py", "  setup.cfg", "  PKG-INFO", "  trainer/", "    __init__.py",
                "    task.py", "    task_multi_gpu.py")

# ------------------------------------------------------------------ layout
FRAME_X, FRAME_Y = 6.6, 3.6       # the safe frame (explainer.check)
TERM_W = 12.6                     # full panel width (log_panel default)
BOTTOM = -3.5                     # at_bottom() default: the lowest text baseline area
LREF_BOTTOM = 3.13                # the lecture tag spans y 3.13..3.6 (top right)
CARD_W = 12.4                     # mcq_card width


def lref(slides: str) -> VGroup:
    """The GREY "Lecture 13 · slides 23–24" tag, top right (lecture_ref(13, ...))."""
    return lecture_ref(13, slides)


# ------------------------------------------------------------------ sources (assets/source, unchanged)
def src_path(name: str) -> str:
    """A file under assets/source: "model-training/package/trainer/task.py" (or the same without
    "model-training/"), "colab/L13_wandb_tracking/cell-38.py". Returns the path under SOURCE."""
    for cand in (name, f"model-training/{name}"):
        if (SOURCE / cand).is_file():
            return cand
    raise FileNotFoundError(f"assets/source/{name} not found")


def source_text(name: str) -> str:
    return (SOURCE / src_path(name)).read_text(encoding="utf-8")


def _source_lines(name: str, nums, strip_emoji_: bool = False) -> dict[int, str]:
    path = src_path(name)
    lines = source_text(name).split("\n")
    out = {}
    for n in nums:
        if not 1 <= n <= len(lines):
            raise IndexError(f"{path} has {len(lines)} lines (asked for {n})")
        s = lines[n - 1].expandtabs(4)
        out[n] = _emoji_guard(s, f"{path} line {n}", strip_emoji_)
    return out


def shown_path(name: str) -> str:
    """The path in a panel header: the repo path without "model-training/"
    ("package/trainer/task.py", "cli.sh"); the notebook cell -> NOTEBOOK_CELL."""
    p = src_path(name)
    if p.startswith("colab/"):
        return NOTEBOOK_CELL
    return p.removeprefix("model-training/")



# ================================================================== generic helpers (from L08, tested there)
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
    bad = set(dropped_chars(s)) | {ch for ch in s if ch in EMOJI}
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


def excerpt(name: str, first: int, last: int, cut_comments: bool = False,
            strip_emoji: bool = False) -> str:
    """Lines first..last (1-based, inclusive) of a tutorial file in assets/source (IDs masked).
    Never-shown lines raise."""
    d = _source_lines(name, range(first, last + 1), strip_emoji)
    res = [d[n] for n in range(first, last + 1)]
    if cut_comments:
        res = [cut_comment(s) for s in res]
    return "\n".join(res)


def source_line(name: str, n: int, strip_emoji: bool = False) -> str:
    """One line of a tutorial file (for excerpt_chip(..., line=...))."""
    return _source_lines(name, [n], strip_emoji)[n]


def sans(s: str, size: float = CAPTION, color: str = INK, **kw) -> Text:
    """CMU Sans Serif text (box labels, card lines)."""
    return label(s, size, color, font=SANS, **kw)


def note(s: str, color: str = S.GREY, size: float = CAPTION) -> Text:
    """A GREY caption (serif, 20 pt)."""
    return label(s, size, color)


def mtext(s: str, size: float = CAPTION, color: str = INK, font: str = MONO) -> Text:
    """Text with the placeholders (‹job-id›) drawn GREY (mono by default; font=SANS or S.FONT)."""
    s = _ph(s)
    t2c = {m: S.GREY for m in PLACEHOLDERS if m in s}
    return S.text(s, size, color, font=font, t2c=t2c)


def grey_masks(line, ellipses: bool = True, color: str = S.GREY):
    """Colour every customer mask (and every '…', the sign of something left out) in a mono_line
    GREY; a folded command (a VGroup with .rows) is handled row by row. Returns line."""
    rows = line.rows if hasattr(line, "rows") else [line]
    for r in rows:
        s = getattr(r, "text", None)
        if not s or not hasattr(r, "glyphs"):
            continue
        for sub in ([*PLACEHOLDERS, "…"] if ellipses else list(PLACEHOLDERS)):
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
        raise ValueError("subtitle=True: pass the subtitle text")
    _with_header(p, " · ".join([shown, where, *extra]), subtitle=subtitle or None)
    code_rows = p.code.source.split("\n")
    if wrapped:
        _lex_whole(p.code, code_rows, whole, {n: (whole_row[n], rows_of[n]) for n in wrapped},
                   language or _lang(src_path(name)), size)
    for k in range(len(code_rows)):                 # GREY ↪ marks, '…' gap rows and the mask
        for sub in ("↪", "…", *PLACEHOLDERS):
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
        s = strip_emoji(_ph(s))
        if max_chars and len(s) > max_chars:
            s = s[:max_chars - 1] + "…"
        ln = mono_line(s, size, col)
        grey_masks(ln)
        ln.shift(np.array([0, -i * pitch, 0]) - ln.strut.get_corner(UP + LEFT))
        rows.add(ln)
    return rows


def log_panel(lines: list[str], header: str, width: float = TERM_W, size: float = CAPTION,
              color: str = OUTPUT) -> VGroup:
    """PANEL: plain mono rows (a recorded line, a diff, out.txt) on a dark rounded panel with a GREY
    header above. Rows longer than the panel are cut with '…'; masks and '…' GREY. .rows .frame
    .header"""
    max_chars = int((width - 0.5) / cell_width(size))
    rows = _mono_rows(lines, size, color, max_chars)
    h = len(lines) * line_pitch(size) + 0.4
    frame = RoundedRectangle(width=width, height=h, corner_radius=0.15, stroke_color=S.GREY_DARK,
                             stroke_width=2).set_fill(PANEL, 1)
    frame.move_to(rows.get_center()).align_to(rows, LEFT).shift(LEFT * 0.25)
    frame.shift(UP * (rows.get_top()[1] + 0.2 - frame.get_top()[1]))
    head = _header_text(header).next_to(frame, UP, buff=0.1).align_to(frame, LEFT).shift(RIGHT * 0.12)
    g = VGroup(frame, rows, head)
    g.frame, g.rows, g.header = frame, rows, head
    return g.move_to(ORIGIN)


def output_box(lines: list[str], header: str | None = None, width: float | None = None,
               size: float = CAPTION, color: str = OUTPUT) -> VGroup:
    """RECORDED: a notebook cell's saved output, drawn as an output area under a cell (never a
    terminal frame): mono rows on a dark panel with a GREY rule at the left; an optional GREY
    header above. Width fits the longest row (or `width`, rows cut with '…'). .rows .frame .rule
    .header (None)"""
    max_chars = int((width - 0.6) / cell_width(size)) if width else None
    rows = _mono_rows(lines, size, color, max_chars)
    w = width or rows.width + 0.6
    h = len(lines) * line_pitch(size) + 0.36
    frame = RoundedRectangle(width=w, height=h, corner_radius=0.1, stroke_color=S.GREY_DARK,
                             stroke_width=1.5).set_fill(TERM_BG, 1)
    frame.move_to(rows.get_center()).align_to(rows, LEFT).shift(LEFT * 0.35)
    frame.shift(UP * (rows.get_top()[1] + 0.18 - frame.get_top()[1]))
    rule = Line(frame.get_corner(UP + LEFT) + np.array([0.14, -0.12, 0]),
                frame.get_corner(DOWN + LEFT) + np.array([0.14, 0.12, 0]), color=S.GREY, stroke_width=4)
    g = VGroup(frame, rule, rows)
    g.frame, g.rule, g.rows, g.header = frame, rule, rows, None
    if header:
        hd = _header_text(header).next_to(frame, UP, buff=0.1).align_to(frame, LEFT).shift(RIGHT * 0.12)
        g.add(hd)
        g.header = hd
    return g.move_to(ORIGIN)


class Prose(str):
    """A prose row for turn_card / card_rows (serif, not a command)."""


def _cell(s, size: float = CAPTION, color: str = INK):
    """A card cell: "`code`" -> mono (without backticks), Prose / str -> serif, a mobject as is."""
    if not isinstance(s, str):
        return s
    if len(s) > 1 and s.startswith("`") and s.endswith("`"):
        return mtext(s[1:-1], size, color)
    return mtext(str(s), size, color, font=S.FONT)



def _md_text(s: str, size: float = CAPTION, color: str = INK) -> Text:
    """One README line as ONE Text: inline `code` in mono (backticks dropped, spacing kept), the rest
    serif; masks GREY."""
    s = _ph(s)
    parts = s.split("`")
    plain, spans, pos = "", [], 0
    for k, p in enumerate(parts):
        if k % 2:
            spans.append((len(plain), len(plain) + len(p)))
        plain += p
    t2c = {m: S.GREY for m in PLACEHOLDERS if m in plain}
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
    sub = _ph(sub)
    if line is not None and sub not in _ph(line):
        raise ValueError(f"{sub!r} is not in {line!r}")
    c = chip(sub, frame, size=size, text_color=color, font=MONO, fill_opacity=0.1)
    if any(m in sub for m in PLACEHOLDERS):
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
        txt = _ph(p[1:-1] if code else p)
        if s and (code or txt[0] not in ",.:?;"):
            s += " "
        if code:
            spans.append((len(s), len(s) + len(txt)))
        s += txt
    t2c = {m: S.GREY for m in PLACEHOLDERS if m in s}
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


def menu_path(items, size: float = CAPTION) -> VGroup:
    """A schematic menu path: GREY chips joined by '›' (File › Save a copy in Drive). .items
    .light(i, colour=TURN) -> anim (that chip's border and text)"""
    chips = [chip(s, S.GREY, size=size) for s in items]
    row = []
    for k, c in enumerate(chips):
        if k:
            row.append(label("›", size, S.GREY))
        row.append(c)
    g = VGroup(*row).arrange(RIGHT, buff=0.15)
    g.items = chips

    def light(i, color=TURN):
        c = chips[i]
        return AnimationGroup(c.box.animate.set_stroke(color, 3), c.text.animate.set_color(color))
    g.light = light
    return _keep(g)


def key_glyph(h: float = 0.3, color: str = KEY, name: str | None = None) -> VGroup:
    """A GOLD key (its content is never drawn). name adds a GOLD mono name to its right. .key .name"""
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


def key_outline(h: float = 0.3, color: str = KEY) -> VGroup:
    """A dashed GOLD key outline: where your key would be."""
    k = key_glyph(h, color)
    out = VGroup(*[DashedVMobject(m, num_dashes=10, dashed_ratio=0.6).set_stroke(color, 2.5)
                   for m in (k[0], k[2], k[3], k[4])])
    return _keep(out)


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
    segs = text.split(" · ")
    rows: list[str] = []
    cur = ""
    for k, seg in enumerate(segs):
        piece = seg + (" ·" if k < len(segs) - 1 else "")
        trial = f"{cur} {piece}" if cur else piece
        if cur and _rich(trial, size).width > width:
            rows.append(cur)
            cur = piece
        else:
            cur = trial
    rows.append(cur)
    out: list[str] = []
    for r in rows:                                   # a segment still too wide: break at spaces
        if _rich(r, size).width <= width:
            out.append(r)
            continue
        line = ""
        for w in r.split(" "):
            t = f"{line} {w}" if line else w
            if line and _rich(t, size).width > width:
                out.append(line)
                line = w
            else:
                line = t
        out.append(line)
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



# ================================================================== L13 exam: tags, takeaway, ponder card
def example_tag(s: str = "example · not in the repo") -> VGroup:
    """GREY tag on the made-up module augment.py (always next to illustration_tag())."""
    return grey_tag(s)


def version_chip(s: str = WANDB_VERSION) -> VGroup:
    """The PURPLE `wandb 0.15.11` tag next to every quoted W&B error message."""
    return _keep(tag(s, TOOL))


def cost_tag(s: str = "$ while running") -> VGroup:
    """GOLD tag (the job's billing; no granularity is claimed)."""
    return _keep(tag(s, COST))


def x_mark(h: float = 0.3) -> VGroup:
    """RED ✗."""
    return _keep(cross_mark(h, ERR))


def tick_mark(h: float = 0.3, color: str = OWN) -> VMobject:
    """GREEN ✓."""
    return _keep(check_mark(h, color))


def takeaway(text: str, width: float = 12.0, size: float = 28, color: str = TURN) -> VGroup:
    """The scene's closing line "If the question says X, think Y." in YELLOW: rows broken to fit
    `width` (at " · " first, then spaces), centred, `code` in backticks mono. One visual group,
    centred at ORIGIN. .rows (the Text rows)"""
    rows = fit_rows(text, width, size, color, buff=0.16, align=ORIGIN)
    g = VGroup(*rows)
    g.rows = rows
    guard(g.width <= 12.6 and g.height <= 4.0, f"takeaway {g.width:.1f} x {g.height:.1f}")
    return _keep(g.move_to(ORIGIN))


MCQ_LETTERS = "ABCD"
MCQ_MAX_CHARS = 46


class MCQCard(VGroup):
    """mcq_card(): the multiple-choice ponder card. Built like ponder_card (YELLOW frame, header,
    question, timer bar) so card[3] is the timer bar and a pause_and_ponder-style drain works:
    ponder_mcq(scene, card). card[4] is the options group.

    .frame .header .question (rows) .bar .options (4 rows; each .badge .text .letter)
    .mark_right(i) -> anims: YELLOW outline around option i, its badge YELLOW
    .reason(i, text) -> anims: option i's text swaps IN PLACE for its RED one-line reason, the
        badge turns RED (the reason row may be up to the card's inner width)
    .dim_option(i, k=0.4) -> anim"""

    def __init__(self, question_rows, options, answer: bool = False, width: float = CARD_W,
                 q_size: float = 24, o_size: float = 22, **kw):
        super().__init__(**kw)
        if len(options) != 4:
            raise ValueError("mcq_card: four options A-D")
        if not 1 <= len(question_rows) <= 2:
            raise ValueError("mcq_card: the question in 1 or 2 rows")
        for o in options:
            if len(o.replace("`", "")) > MCQ_MAX_CHARS:
                raise ValueError(f"mcq option over {MCQ_MAX_CHARS} characters: {o!r}")
        self.width_ = width
        self.o_size = o_size
        head = S.text("Answer" if answer else "Pause and ponder", 26, TURN, weight="BOLD")
        q = VGroup(*[_rich(r, q_size, INK) for r in question_rows]).arrange(DOWN, buff=0.12)
        opts = VGroup()
        for letter, o in zip(MCQ_LETTERS, options):
            badge = step_badge(letter, S.GREY, size=TAG, radius=0.22)
            t = _rich(o, o_size, INK)
            row = VGroup(badge, t)
            t.next_to(badge, RIGHT, buff=0.25)
            row.badge, row.text, row.letter = badge, t, letter
            opts.add(row)
        opts.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        body = VGroup(head, q, opts).arrange(DOWN, buff=0.34)
        opts.align_to(body, LEFT)
        frame = RoundedRectangle(width=width, height=body.height + 1.0, corner_radius=0.2,
                                 stroke_color=TURN, stroke_width=3).set_fill(S.BG, 0.96)
        body.move_to(frame).shift(UP * 0.1)
        opts.shift(np.array([frame.get_left()[0] + 1.2 - opts.get_left()[0], 0, 0]))
        bar = Line(frame.get_corner(DOWN + LEFT) + RIGHT * 0.3 + UP * 0.25,
                   frame.get_corner(DOWN + RIGHT) + LEFT * 0.3 + UP * 0.25, color=TURN, stroke_width=4)
        if answer:
            bar.set_stroke(opacity=0)
        self.add(frame, head, q, bar, opts)
        self.frame, self.header, self.question, self.bar, self.options = frame, head, q, bar, opts
        inner = width - 0.6
        guard(q.width <= inner and opts.width <= inner, f"mcq card text wider than {inner:.1f}")
        guard(self.height <= 7.0, f"mcq card {self.height:.1f} high")
        self.move_to(ORIGIN)

    def _text_room(self) -> float:
        return self.frame.get_right()[0] - 0.3 - self.options[0].text.get_left()[0]

    def mark_right(self, i: int) -> list:
        row = self.options[i]
        r = RoundedRectangle(width=self.frame.width - 0.8, height=row.height + 0.22, corner_radius=0.12,
                             stroke_color=TURN, stroke_width=3).set_fill(opacity=0)
        r.move_to([self.frame.get_center()[0], row.get_center()[1], 0])
        _stage_hidden(self, r, "_mcq")
        self.right_box = r
        return [_Reveal(r, "_mcq"), row.badge[0].animate.set_stroke(TURN),
                row.badge[1].animate.set_color(TURN)]

    def reason(self, i: int, text: str) -> list:
        row = self.options[i]
        new = _rich(text, self.o_size, ERR)
        guard(new.width <= self._text_room() + 0.01,
              f"reason {text!r} is {new.width:.1f} wide (> {self._text_room():.1f})")
        new.move_to(row.text, aligned_edge=LEFT)
        out = swap_text(row, row.text, new)
        row.text = new
        return out + [row.badge[0].animate.set_stroke(ERR), row.badge[1].animate.set_color(ERR)]

    def dim_option(self, i: int, k: float = 0.4):
        return self.options[i].animate.set_opacity(k)


def mcq_card(question_rows: list[str], options: list[str], answer: bool = False,
             width: float = CARD_W) -> MCQCard:
    """The multiple-choice ponder card (script.md PONDER): YELLOW frame, "Pause and ponder" (or
    "Answer" with answer=True: no timer), the question in 1-2 rows at 24 pt, four option rows A-D
    at 22 pt (<= 46 characters each, `code` mono), letter badge left; 12.4 wide, centred at ORIGIN.
    card[3] is the timer bar. See MCQCard for .mark_right(i) / .reason(i, text)."""
    return MCQCard(question_rows, options, answer=answer, width=width)


def ponder_mcq(scene, card: MCQCard, seconds: float = 10.0) -> MCQCard:
    """Plays: the card fades in, then its timer bar drains over `seconds` (silent). Returns the
    card (on screen; FadeOut it yourself)."""
    scene.play(FadeIn(card, scale=0.95), run_time=0.6)
    bar = card[3]
    scene.play(bar.animate(rate_func=linear).become(bar.copy().scale(0.001, about_point=bar.get_start())),
               run_time=seconds)
    return card


def flow(items, size: float = CAPTION, colors=None, arrow: str = "→", font: str | None = MONO) -> VGroup:
    """A row of GREY chips joined by arrows ("init" → "fit · 2 epochs" → "finish"); colors: one
    per item (default GREY). .items (the chips) .light(i, colour=TURN) -> anim"""
    colors = colors or [S.GREY] * len(items)
    chips = [chip(s, c, size=size, font=font) for s, c in zip(items, colors)]
    row = []
    for k, c in enumerate(chips):
        if k:
            row.append(label(arrow, size, S.GREY))
        row.append(c)
    g = VGroup(*row).arrange(RIGHT, buff=0.15)
    g.items = chips

    def light(i, color=TURN):
        c = chips[i]
        return AnimationGroup(c.box.animate.set_stroke(color, 3), c.text.animate.set_color(color))
    g.light = light
    return _keep(g)


# ================================================================== V1 · the run ledger (S01-S03, S07, S08)
def padlock(h: float = 0.36, color: str = SEALED) -> VGroup:
    """A padlock glyph (a sealed run)."""
    body = RoundedRectangle(width=h * 0.9, height=h * 0.62, corner_radius=h * 0.08, stroke_color=color,
                            stroke_width=2.5).set_fill(color, 0.35)
    shackle = Arc(radius=h * 0.28, start_angle=0, angle=PI, stroke_color=color, stroke_width=3)
    shackle.next_to(body, UP, buff=-0.02)
    legs = VGroup(Line(shackle.get_start(), shackle.get_start() + DOWN * 0.05),
                  Line(shackle.get_end(), shackle.get_end() + DOWN * 0.05)).set_stroke(color, 3)
    hole = Dot(body.get_center(), radius=h * 0.06, color=S.BG)
    return _keep(VGroup(body, shackle, legs, hole))


class Pen(VGroup):
    """The callback as a PURPLE pen (S03): a slanted barrel with a nib, the mono name under it.
    1.4 x 1.0 (+ a worn tag ~3 wide to the right). .tip() the nib's point; .move_tip(point) ->
    anim; .wear(text) -> anims (a GREY tag right of the name that rides on the pen from now on,
    e.g. "created during row 1"); .barrel .name .badge (None until wear)."""

    def __init__(self, name: str | None = "callback", h: float = 0.9, color: str = TOOL, **kw):
        super().__init__(**kw)
        w = h * 0.24
        barrel = RoundedRectangle(width=w, height=h, corner_radius=w * 0.3, stroke_color=color,
                                  stroke_width=3).set_fill(color, 0.35)
        nib = Polygon(barrel.get_corner(DOWN + LEFT) + RIGHT * 0.01, barrel.get_corner(DOWN + RIGHT) + LEFT * 0.01,
                      barrel.get_bottom() + DOWN * h * 0.3, stroke_color=color, stroke_width=3).set_fill(color, 0.8)
        band = Line(barrel.get_left() + UP * h * 0.2, barrel.get_right() + UP * h * 0.2, color=color, stroke_width=3)
        pen = VGroup(barrel, band, nib).rotate(-0.5, about_point=nib.get_vertices()[2])
        self.add(pen)
        self._nib = nib
        self.barrel, self.name, self.badge = pen, None, None
        if name:
            n = mono(name, CAPTION, color).next_to(pen, RIGHT, buff=0.12).shift(UP * 0.15)
            self.add(n)
            self.name = n
        _keep(self)

    def tip(self):
        return self._nib.get_vertices()[2].copy()

    def move_tip(self, point, **kw):
        return self.animate(**kw).shift(np.array(point) - self.tip())

    def wear(self, text: str) -> list:
        anchor = self.name if self.name is not None else self.barrel
        t = grey_tag(text).next_to(anchor, RIGHT, buff=0.15)
        _stage_hidden(self, t, "_wear")
        self.badge = t
        return [_Reveal(t, "_wear")]


class LedgerRow(Piece):
    """One W&B run as a BLUE ledger row (schematic: put illustration_tag() near the ledger).

    LedgerRow(name=RUN_NAME, width=9.0, full=True, slots=6)
      full=True  (S01, S02): 9.0 x 2.3: name, 2 rows of config-chip slots, the system tile,
                 the history strip;  full=False (S03, S07): 9.0 x 1.15: name + history strip.
    Parts (hidden until revealed): "finished" (GREEN chip, top right), "lock" (padlock),
      "cfg:<key>" for CONFIG_KEYS + EXEC_KEY (full only), "system" (tile: frame + label),
      "traces" (its two recorded lines, reveal with anim=Create), "empty" (RED dashed outline
      over the strip).
    .clip(key) -> anims (a config chip drops into its slot)
    .tick(k) -> anims (GREEN tick k, 1-based, drops into the strip); .ticks (dict k -> mob)
    .set_count(text) -> anims (GREY count right of the strip, "6 entries · 1 run")
    .activate() / .seal() -> anims (outline YELLOW / padlock + outline GREY)
    .slot_point(k) the strip slot's centre; .pointer_point() left edge middle (wandb.run)"""

    def __init__(self, name: str = RUN_NAME, width: float = 9.0, full: bool = True, slots: int = 6,
                 color: str = CLOUD, **kw):
        super().__init__(**kw)
        self.full, self.n_slots = full, slots
        h = 2.3 if full else 1.15
        frame = RoundedRectangle(width=width, height=h, corner_radius=0.16, stroke_color=color,
                                 stroke_width=3).set_fill(color, 0.07)
        self.frame = self.part("frame", frame)
        left, top = frame.get_left()[0] + 0.3, frame.get_top()[1] - 0.3
        nm = mono(name, 22, INK)
        nm.move_to([left, top, 0], aligned_edge=LEFT)
        self.name_text = self.part("name", nm)
        fin = chip("finished", OWN, size=CAPTION)
        fin.move_to([frame.get_right()[0] - 0.25 - fin.width / 2, top, 0])
        self.part("finished", fin, shown=False)
        lock = padlock().next_to(fin, LEFT, buff=0.25)
        self.part("lock", lock, shown=False)
        # history strip (bottom)
        strip_y = frame.get_bottom()[1] + 0.38
        hl = label("history", CAPTION, S.GREY).move_to([left, strip_y, 0], aligned_edge=LEFT)
        self.strip_label = self.part("strip_label", hl)
        self.pitch = 0.42
        rail_w = slots * self.pitch + 0.12
        rail = RoundedRectangle(width=rail_w, height=0.46, corner_radius=0.08, stroke_color=S.GREY,
                                stroke_width=2).set_fill(S.BG, 0.6)
        rail.move_to([hl.get_right()[0] + 0.25 + rail_w / 2, strip_y, 0])
        self.rail = self.part("rail", rail)
        emp = DashedVMobject(RoundedRectangle(width=rail_w + 0.12, height=0.58, corner_radius=0.1),
                             num_dashes=36, dashed_ratio=0.55).set_stroke(ERR, 3).move_to(rail)
        self.part("empty", emp, shown=False)
        self.count = None
        self.ticks: dict[int, VMobject] = {}
        if full:
            tile = RoundedRectangle(width=1.6, height=1.05, corner_radius=0.1, stroke_color=S.GREY,
                                    stroke_width=2).set_fill(S.BG, 0.6)
            tile.move_to([frame.get_right()[0] - 0.25 - 0.8, frame.get_center()[1] + 0.02, 0])
            tl = label("system", CAPTION, S.GREY).move_to(tile.get_top() + DOWN * 0.22)
            self.part("system", VGroup(tile, tl), shown=False)
            x0, x1 = tile.get_left()[0] + 0.15, tile.get_right()[0] - 0.15
            y0 = tile.get_bottom()[1] + 0.15
            rng = np.random.default_rng(13)
            traces = VGroup()
            for k, col in enumerate((CLOUD, S.GREY)):
                ys = y0 + 0.08 + 0.12 * k + np.clip(rng.normal(0.18, 0.07, 9), 0.02, 0.4)
                traces.add(_poly([(x, y) for x, y in zip(np.linspace(x0, x1, 9), ys)], col, 2.5))
            self.part("traces", traces, shown=False)
            # config chip slots: two rows left of the tile
            chips = [chip(k, OWN, size=CAPTION, font=MONO) for k in (*CONFIG_KEYS, EXEC_KEY)]
            rows = [chips[:3], chips[3:]]
            y = nm.get_bottom()[1] - 0.35
            for r in rows:
                x = left
                for c in r:
                    c.move_to([x + c.width / 2, y, 0])
                    x += c.width + 0.18
                y -= 0.5
            for k, c in zip((*CONFIG_KEYS, EXEC_KEY), chips):
                self.part(f"cfg:{k}", c, shown=False)
            guard(max(c.get_right()[0] for c in chips) < tile.get_left()[0] - 0.1,
                  "config chips run into the system tile")
        guard(rail.get_right()[0] + 0.3 + 2.2 <= frame.get_right()[0] - 0.1,
              "no room for the count label right of the strip")

    def clip(self, key: str) -> list:
        return self.parts_in(f"cfg:{key}", anim=lambda mob: FadeIn(mob, shift=DOWN * 0.25))

    def slot_point(self, k: int):
        r = self.rail
        return np.array([r.get_left()[0] + 0.06 + (k - 0.5) * self.pitch, r.get_center()[1], 0])

    def pointer_point(self):
        return self.frame.get_left().copy()

    def tick(self, k: int) -> list:
        if not 1 <= k <= self.n_slots:
            raise IndexError(f"tick {k}: the strip has {self.n_slots} slots")
        t = RoundedRectangle(width=0.14, height=0.32, corner_radius=0.05, stroke_color=OWN,
                             stroke_width=2).set_fill(OWN, 0.85).move_to(self.slot_point(k))
        _stage_hidden(self, t, "_tick")
        self.ticks[k] = t
        return [_Reveal(t, "_tick", shift=DOWN * 0.3)]

    def set_count(self, text: str, color: str = S.GREY) -> list:
        new = label(text, CAPTION, color)
        new.move_to([self.rail.get_right()[0] + 0.3, self.rail.get_center()[1], 0], aligned_edge=LEFT)
        if self.count is None:
            _stage_hidden(self, new, "_cnt")
            self.count = new
            return [_Reveal(new, "_cnt")]
        old, self.count = self.count, new
        return swap_text(self, old, new)

    def activate(self, color: str = TURN) -> list:
        return [self.frame.animate.set_stroke(color, 4)]

    def seal(self) -> list:
        return [*self.parts_in("lock"), self.frame.animate.set_stroke(SEALED, 3)]


class Ledger(Piece):
    """wandb.ai drawn as a ledger (schematic, no logo): a BLUE frame, the header "wandb.ai ·
    project" + WB_PROJECT (mono), the `illustration` tag, `slots` empty GREY dashed row places.
    Ledger(slots=2, full=False, width=9.6): row places 1.15 high (full=True: 2.3).
    .slot(i) centre of row place i (0-based); .new_row(i, name=RUN_NAME, **kw) -> a LedgerRow
    placed there (not added: FadeIn(row, shift=LEFT) it, or self.attach(scene, row));
    parts "places" (the dashed places), "tag". 9.6 x (0.9 + slots * (h + 0.2))"""

    def __init__(self, slots: int = 2, full: bool = False, width: float = 9.6, project: str = WB_PROJECT,
                 **kw):
        super().__init__(**kw)
        self.row_w = width - 0.6
        self.row_h = 2.3 if full else 1.15
        self.full = full
        h = 0.9 + slots * (self.row_h + 0.2)
        frame = RoundedRectangle(width=width, height=h, corner_radius=0.2, stroke_color=CLOUD,
                                 stroke_width=2.5).set_fill(CLOUD, 0.03)
        self.part("frame", frame)
        head = VGroup(label("wandb.ai · project", CAPTION, CLOUD), mono(project, CAPTION, INK)) \
            .arrange(RIGHT, buff=0.18)
        head.move_to(frame.get_corner(UP + LEFT) + np.array([0.3 + head.width / 2, -0.4, 0]))
        self.part("head", head)
        tg = illustration_tag().move_to(frame.get_corner(UP + RIGHT) + np.array([-0.3, -0.4, 0]),
                                         aligned_edge=RIGHT)
        self.part("tag", tg)
        places = VGroup()
        for i in range(slots):
            r = DashedVMobject(RoundedRectangle(width=self.row_w, height=self.row_h, corner_radius=0.16),
                               num_dashes=60, dashed_ratio=0.5).set_stroke(S.GREY_DARK, 2)
            places.add(r.move_to(self.slot(i)))
        self.part("places", places)
        guard(head.get_right()[0] < tg.get_left()[0] - 0.2, "ledger header runs into its tag")

    def slot(self, i: int):
        fr = self.parts["frame"]
        top = fr.get_top()[1] - 0.8
        return np.array([fr.get_center()[0], top - self.row_h / 2 - i * (self.row_h + 0.2), 0])

    def new_row(self, i: int, name: str = RUN_NAME, **kw) -> LedgerRow:
        r = LedgerRow(name, width=self.row_w, full=self.full, **kw)
        return r.move_to(self.slot(i))


class RunPointer(VGroup):
    """The PINK `wandb.run` pointer: a mono label at a fixed tail point and an arrow that swings to
    whatever it points at; a GREY dashed `None` slot under the label. RunPointer(tail, none_at=None)
    tail: the label's right end; none_at: the None slot's centre (default 1.0 below the label).
    .point_to(point) -> anims (the arrow swings; the target is usually row.pointer_point())
    .to_none() -> anims (the arrow drops into the None slot) .arrow .label .none_slot .target"""

    def __init__(self, tail, none_at=None, **kw):
        super().__init__(**kw)
        tail = np.array(tail, dtype=float)
        self.label = mono("wandb.run", 22, LOOKUP)
        self.label.move_to(tail, aligned_edge=RIGHT)
        nb = mono("None", CAPTION, S.GREY)
        fr = DashedVMobject(RoundedRectangle(width=nb.width + 0.4, height=0.5, corner_radius=0.1),
                            num_dashes=20).set_stroke(S.GREY, 2)
        none_at = np.array(none_at if none_at is not None else self.label.get_center() + DOWN * 1.0)
        self.none_slot = VGroup(fr.move_to(none_at), nb.move_to(none_at))
        self.arrow = self._make(self.none_slot.get_top() + UP * 0.02)
        self.target = None
        self.add(self.label, self.none_slot, self.arrow)
        _keep(self)

    def _make(self, point):
        return Arrow(self.label.get_right() + RIGHT * 0.08, np.array(point), buff=0.04, color=LOOKUP, stroke_width=4,
                     max_tip_length_to_length_ratio=0.25, tip_length=0.2)

    def point_to(self, point) -> list:
        self.target = np.array(point)
        return [Transform(self.arrow, self._make(point))]

    def to_none(self) -> list:
        self.target = None
        return [Transform(self.arrow, self._make(self.none_slot.get_top() + UP * 0.02)),
                Indicate(self.none_slot, color=S.GREY, scale_factor=1.08)]


class _GrowIn(GrowFromEdge):
    """GrowFromEdge of a member kept at fill opacity 0 until the animation begins."""

    def begin(self) -> None:
        self.mobject.set_fill(opacity=0.55)
        super().begin()


class EpochBar(VGroup):
    """A training progress bar of n epochs (GREY segments) with an optional caption above
    ("fit · 2 epochs"). .run(i) -> anim (segment i, 0-based, fills left to right) .end(i) the
    right end of segment i (where the pen drops its tick) .segments .fills .caption"""

    def __init__(self, n: int, width: float = 4.0, caption: str | None = None, color: str = S.GREY, **kw):
        super().__init__(**kw)
        seg_w = (width - 0.08 * (n - 1)) / n
        segs, fills = VGroup(), VGroup()
        for i in range(n):
            s = RoundedRectangle(width=seg_w, height=0.26, corner_radius=0.06, stroke_color=color,
                                 stroke_width=2).set_fill(S.BG, 0)
            s.move_to([i * (seg_w + 0.08), 0, 0])
            f = Rectangle(width=seg_w - 0.06, height=0.2, stroke_width=0).set_fill(INK, 0.55).move_to(s)
            segs.add(s)
            fills.add(f)
        fills.set_fill(opacity=0)
        self.segments, self.fills = segs, fills
        self.add(segs, fills)
        self.caption = None
        if caption:
            c = mono(caption, CAPTION, S.GREY).next_to(segs, UP, buff=0.12).align_to(segs, LEFT)
            self.add(c)
            self.caption = c
        _keep(self)

    def run(self, i: int, run_time: float = 0.8):
        return _GrowIn(self.fills[i], LEFT, run_time=run_time, rate_func=linear)

    def end(self, i: int):
        return self.segments[i].get_right().copy()


class BracketTimeline(VGroup):
    """S03's takeaway picture: code lines top to bottom (default init, fit · 2, finish, init, fit · 4,
    finish, fit), a YELLOW bracket on the left over each init…finish span, a RED ✗ right of a fit
    outside every span. .rows .brackets (one per span) .cross (or None) .tick_points(i, n) -> n
    points right of row i (where that fit's ticks land) .span_of(i) -> bracket index or None"""

    def __init__(self, lines=("init", "fit · 2", "finish", "init", "fit · 4", "finish", "fit"),
                 size: float = 22, pitch: float = 0.5, **kw):
        super().__init__(**kw)
        rows = VGroup(*[mono(s, size, INK) for s in lines])
        for i, r in enumerate(rows):
            r.move_to([0, -i * pitch, 0], aligned_edge=LEFT)
        self.rows = rows
        self.add(rows)
        spans, start = [], None
        for i, s in enumerate(lines):
            if s.startswith("init"):
                start = i
            elif s.startswith("finish") and start is not None:
                spans.append((start, i))
                start = None
        self.spans = spans
        self.brackets = VGroup()
        x = rows.get_left()[0] - 0.25
        for a, b in spans:
            top, bot = rows[a].get_top()[1] + 0.06, rows[b].get_bottom()[1] - 0.06
            ln = VMobject(stroke_color=TURN, stroke_width=4)
            ln.set_points_as_corners([[x + 0.12, top, 0], [x, top, 0], [x, bot, 0], [x + 0.12, bot, 0]])
            self.brackets.add(ln)
        self.add(self.brackets)
        self.cross = None
        for i, s in enumerate(lines):
            if s.startswith("fit") and self.span_of(i) is None:
                c = x_mark(0.3).next_to(rows[i], RIGHT, buff=0.3)
                self.cross = c
                self.add(c)
        _keep(self)

    def span_of(self, i: int):
        for k, (a, b) in enumerate(self.spans):
            if a < i < b:
                return k
        return None

    def tick_points(self, i: int, n: int, x0: float | None = None):
        r = self.rows[i]
        x0 = (self.rows.get_right()[0] + 0.4) if x0 is None else x0
        return [np.array([x0 + 0.3 * k, r.get_center()[1], 0]) for k in range(n)]


def history_tick(color: str = OWN) -> VMobject:
    """One history entry: the GREEN tick bar of the ledger's strip (for BracketTimeline etc.)."""
    return _keep(RoundedRectangle(width=0.14, height=0.32, corner_radius=0.05, stroke_color=color,
                                  stroke_width=2).set_fill(color, 0.85))


def empty_chart(title: str = "loss", w: float = 3.6, h: float = 2.0) -> VGroup:
    """A RED dashed chart outline where a loss / accuracy chart would be, mono title on top,
    GREY caption "no data logged" inside (put illustration_tag() near it). 3.6 x 2.0.
    .frame .title .caption (fade the caption out when curve_in() draws the fix)"""
    fr = DashedVMobject(RoundedRectangle(width=w, height=h, corner_radius=0.14), num_dashes=44,
                        dashed_ratio=0.55).set_stroke(ERR, 3)
    t = mono(title, CAPTION, INK).move_to(fr.get_top() + DOWN * 0.3)
    c = label("no data logged", CAPTION, S.GREY).move_to(fr.get_center() + DOWN * 0.15)
    g = VGroup(fr, t, c)
    g.frame, g.title, g.caption = fr, t, c
    return g


def curve_in(chart: VGroup, kind: str = "loss", color: str = OWN) -> VMobject:
    """A schematic curve inside an empty_chart (S03's fix: illustration): falling for loss,
    rising for accuracy. Not added: Create it."""
    fr = chart.frame
    x0, x1 = fr.get_left()[0] + 0.35, fr.get_right()[0] - 0.35
    y0, y1 = fr.get_bottom()[1] + 0.3, fr.get_top()[1] - 0.65
    xs = np.linspace(0, 1, 12)
    ys = np.exp(-3 * xs) if kind == "loss" else 1 - np.exp(-3 * xs)
    return _poly([(x0 + (x1 - x0) * x, y0 + (y1 - y0) * y) for x, y in zip(xs, ys)], color, 3.5)


# ================================================================== V2 · what pip unwraps (S04)
class PackageTree(Piece):
    """The repo's package/ folder (PACKAGE_TREE) as a GREEN file tree at 22 pt, `__init__.py` with
    the GREY note "empty". 4.6 x 3.3. .tree (file_tree) .row(name) (e.g. "trainer/", "setup.py")
    .row_point(level, after) -> where a new row's glyph-left goes: one pitch under row `after`
    at indent `level` (0 = beside package/, 1 = inside package/, 2 = inside trainer/)
    .pitch (the row pitch)"""

    def __init__(self, entries=PACKAGE_TREE, size: float = 22, **kw):
        super().__init__(**kw)
        cols = {"package/": OWN, "trainer/": OWN}
        t = file_tree(list(entries), size=size, colors=cols, notes={"__init__.py": "empty"})
        self.tree = self.part("tree", t)
        self.size = size
        self.pitch = line_pitch(size) + 0.1
        self.indent = 0.42

    def row(self, name: str):
        return self.tree.row(name)

    def row_point(self, level: int, after: str):
        r = self.row(after)
        x0 = self.tree.rows[0].glyph.get_left()[0]
        return np.array([x0 + level * self.indent, r.name_text.strut.get_center()[1] - self.pitch, 0])


def ghost_module(name: str = "augment.py", size: float = 22) -> VGroup:
    """The made-up team module: a GREY dashed file + mono name (22 pt); put illustration_tag()
    and example_tag() beside it the first time. .glyph .text .fname; place by .glyph's left."""
    g = DashedVMobject(file_glyph(0.3, CONCEPT)[0], num_dashes=18).set_stroke(CONCEPT, 2)
    t = mono(name, size, CONCEPT).next_to(g, RIGHT, buff=0.14)
    row = VGroup(g, t)
    row.glyph, row.text, row.fname = g, t, name
    return _keep(row)


class Scanner(VGroup):
    """find_packages() as a PINK scanner bar with its mono label at its right end (2.5 wide).
    Scanner(width=4.8). .sweep(tree, lit=("trainer/",), dim=(), run_time=1.6) -> anims: the bar
    runs down the tree's rows (top to bottom, linear); as it passes, each row in `lit` turns bright
    GREEN (name and glyph), each in `dim` drops to 40 %. Leaves the bar under the last row.
    .bar .label"""

    def __init__(self, width: float = 4.8, **kw):
        super().__init__(**kw)
        bar = Rectangle(width=width, height=0.08, stroke_width=0).set_fill(LOOKUP, 0.9)
        glow = Rectangle(width=width, height=0.34, stroke_width=0).set_fill(LOOKUP, 0.14)
        lab = mono("find_packages()", CAPTION, LOOKUP).next_to(bar, RIGHT, buff=0.2)
        self.bar = VGroup(glow, bar)
        self.label = lab
        self.add(self.bar, lab)
        _keep(self)

    def sweep(self, tree, lit=("trainer/",), dim=(), run_time: float = 1.6) -> list:
        rows = list(tree.tree.rows if hasattr(tree, "tree") else tree.rows)
        y_top = rows[0].get_top()[1] + 0.1
        y_bot = rows[-1].get_bottom()[1] - 0.1
        start = self.copy().shift(UP * (y_top - self.bar.get_center()[1]))
        self.become(start)
        anims = [self.animate(rate_func=linear, run_time=run_time).shift(DOWN * (y_top - y_bot))]
        for r in rows:
            name = r.name.strip()
            a = (y_top - r.get_center()[1]) / (y_top - y_bot)
            win = (max(0.0, a - 0.05), min(1.0, a + 0.1))
            if name in lit or name.rstrip("/") in [s.rstrip("/") for s in lit]:
                anims.append(AnimationGroup(r.name_text.glyphs.animate.set_color(OWN), r.glyph.animate.set_color(OWN),
                                            run_time=run_time, rate_func=squish_rate_func(smooth, *win)))
            elif name in dim:
                anims.append(AnimationGroup(r.name_text.glyphs.animate.set_opacity(0.4),
                                            r.glyph.animate.set_stroke(opacity=0.4).set_fill(opacity=0.1),
                                            run_time=run_time, rate_func=squish_rate_func(smooth, *win)))
        return anims


def shopping_list(pin: str = WANDB_PIN) -> VGroup:
    """install_requires as a shopping list: a GREY card headed "install_requires · from PyPI",
    one PURPLE mono chip (the pin). .frame .chip .header"""
    c = chip(pin, TOOL, size=22, font=MONO)
    fr = box(c.width + 0.6, c.height + 0.5, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.14)
    c.move_to(fr)
    hd = VGroup(mono("install_requires", CAPTION, S.GREY), label("· from PyPI", CAPTION, S.GREY)) \
        .arrange(RIGHT, buff=0.12).next_to(fr, UP, buff=0.08).align_to(fr, LEFT)
    g = VGroup(fr, c, hd)
    g.frame, g.chip, g.header = fr, c, hd
    return _keep(g)


def pypi_cloud(width: float = 2.2) -> VGroup:
    """The Python Package Index as a GREY cloud labelled "PyPI". .cloud .label"""
    c = cloud(width, S.GREY, 0.08)
    t = label("PyPI", 24, S.GREY).move_to(c)
    g = VGroup(c, t)
    g.cloud, g.label = c, t
    return _keep(g)


def tarball(name: str = "trainer.tar.gz", color: str = OWN, w: float = 1.0) -> VGroup:
    """A GREEN archive glyph (a box with straps) and its mono name under it. .glyph .text"""
    b = RoundedRectangle(width=w, height=w * 0.72, corner_radius=0.08, stroke_color=color,
                         stroke_width=3).set_fill(color, 0.25)
    straps = VGroup(*[Line(b.get_top() + RIGHT * dx, b.get_bottom() + RIGHT * dx, color=color, stroke_width=3)
                      for dx in (-w * 0.18, w * 0.18)])
    glyph = VGroup(b, straps)
    t = mono(name, CAPTION, color).next_to(glyph, DOWN, buff=0.1)
    g = VGroup(glyph, t)
    g.glyph, g.text = glyph, t
    return _keep(g)


def bucket(name: str | None = BUCKET, w: float = 1.4, color: str = CLOUD) -> VGroup:
    """A BLUE GCS bucket (a pail) with an optional mono PINK path under it. .glyph .mouth() .text"""
    top = Arc(radius=w / 2, start_angle=0, angle=TAU, stroke_color=color, stroke_width=3)
    top.stretch(0.28, 1)
    body = Polygon([-w / 2, 0, 0], [w / 2, 0, 0], [w * 0.38, -w * 0.8, 0], [-w * 0.38, -w * 0.8, 0],
                   stroke_color=color, stroke_width=3).set_fill(color, 0.18)
    glyph = VGroup(body, top)
    g = VGroup(glyph)
    g.glyph, g.text = glyph, None
    g.mouth = lambda: top.get_center().copy()
    if name:
        t = mono(name, CAPTION, LOOKUP).next_to(glyph, DOWN, buff=0.12)
        g.add(t)
        g.text = t
    return _keep(g)


class JobVM(Piece):
    """The job's BLUE VM (schematic) holding Google's TEAL prebuilt image with two stacked shelves:
    ORANGE "in the image" (SHIPPED_LIBS) above GREEN "installed by pip" (slots "wandb", "trainer",
    hidden). JobVM(image=IMAGE_CPU, width=7.0, height=3.8): 7.0 x 3.8.
    Parts: "vm" "image" "shipped" (the ORANGE shelf + chips) "installed" (the GREEN shelf frame)
      "wandb" "trainer" (chips, hidden) ;  .install(name) -> anims (chip drops onto the shelf)
    .search(run_time=1.5) -> anims (a PINK beam sweeps both shelves left to right; FadeOut
      vm.beam afterwards) .shelves (VGroup of both shelf frames) .log_point() (just under the VM's
      bottom edge, centre: put the pip log there with its top on it)"""

    def __init__(self, image: str = IMAGE_CPU, width: float = 7.0, height: float = 3.8, **kw):
        super().__init__(**kw)
        vm = machine_box("job VM", "Vertex AI · its own machine", width=width, height=height, color=CLOUD,
                         title_size=24, sub_size=CAPTION)
        self.vm = self.part("vm", vm)
        iw, ih = width - 0.5, height - 1.0
        img = box(iw, ih, CTR, fill_opacity=0.05, radius=0.14, stroke=3)
        img.move_to(vm.body).shift(DOWN * 0.05)
        it = VGroup(label("prebuilt training image ·", CAPTION, CTR), mono(image, CAPTION, CTR)) \
            .arrange(RIGHT, buff=0.12).move_to(img.get_top() + DOWN * 0.28)
        self.part("image", VGroup(img, it))
        self.image_box, self.image_title = img, it
        shw = iw - 0.4
        sh1 = box(shw, 0.6, SHIPPED, fill_opacity=0.08, radius=0.1)
        l1 = label("in the image", CAPTION, SHIPPED)
        l1.move_to([img.get_left()[0] + 0.2, it.get_bottom()[1] - 0.3, 0], aligned_edge=LEFT)
        sh1.next_to(l1, DOWN, buff=0.08).align_to(l1, LEFT)
        libs = VGroup(*[chip(s, SHIPPED, size=CAPTION) for s in SHIPPED_LIBS]).arrange(RIGHT, buff=0.12)
        libs.move_to(sh1)
        l2 = label("installed by pip", CAPTION, OWN).next_to(sh1, DOWN, buff=0.14).align_to(sh1, LEFT)
        sh2 = box(shw, 0.6, OWN, fill_opacity=0.06, radius=0.1).next_to(l2, DOWN, buff=0.08).align_to(sh1, LEFT)
        self.part("shipped", VGroup(sh1, l1, libs))
        self.part("installed", VGroup(sh2, l2))
        w_c = chip("wandb", TOOL, size=CAPTION, font=MONO)
        t_c = chip("trainer", OWN, size=CAPTION, font=MONO)
        VGroup(w_c, t_c).arrange(RIGHT, buff=0.2).move_to(sh2)
        self.part("wandb", w_c, shown=False)
        self.part("trainer", t_c, shown=False)
        self.libs, self.shelves = libs, VGroup(sh1, sh2)
        self.beam = None
        guard(libs.width <= shw - 0.1 and libs.height <= 0.6, "shipped chips overflow the shelf")
        guard(sh2.get_bottom()[1] >= img.get_bottom()[1] + 0.1, "shelves overflow the image box")
        guard(it.width <= iw - 0.2, "image title wider than the image box")

    def install(self, name: str) -> list:
        return self.parts_in(name, anim=lambda m: FadeIn(m, shift=DOWN * 0.3))

    def log_point(self):
        return self.vm.frame.get_bottom() + DOWN * 0.15

    def search(self, run_time: float = 1.5) -> list:
        sh = self.shelves
        beam = Rectangle(width=0.35, height=sh.height + 0.3, stroke_width=0).set_fill(LOOKUP, 0.35)
        beam.move_to([sh.get_left()[0], sh.get_center()[1], 0])
        self.beam = beam
        return [FadeIn(beam, run_time=0.2),
                beam.animate(run_time=run_time, rate_func=linear).move_to([sh.get_right()[0], sh.get_center()[1], 0])]


# ================================================================== V3 · mirrors vs islands (S05)
SHADES = ("#83C167", "#4FA86A", "#B5D86A", "#2F8F6F", "#D2E68A", "#5FBF9A")   # replica weights (all GREEN)


def gpu_chip(name: str = GPU_NAME, w: float = 0.9, color: str = CLOUD) -> VGroup:
    """A BLUE GPU chip with pins and its name (sans 20 pt). .body .text"""
    b = RoundedRectangle(width=w, height=w * 0.62, corner_radius=0.06, stroke_color=color,
                         stroke_width=3).set_fill(color, 0.18)
    pins = VGroup(*[Line(UP * 0.07, DOWN * 0.07, color=color, stroke_width=2)
                    .move_to(b.get_bottom() + DOWN * 0.07 + RIGHT * dx)
                    for dx in np.linspace(-w * 0.35, w * 0.35, 5)])
    t = label(name, CAPTION, INK).move_to(b)
    g = VGroup(b, pins, t)
    g.body, g.text = b, t
    return _keep(g)


class Replica(VGroup):
    """A model replica: a small rounded block of 3 layer bars filled in its weight shade (GREEN;
    one shade = in sync). .set_shade(colour) -> anim .shade"""

    def __init__(self, shade: str = SHADES[0], w: float = 0.8, **kw):
        super().__init__(**kw)
        fr = RoundedRectangle(width=w, height=w * 0.7, corner_radius=0.08, stroke_color=shade,
                              stroke_width=2.5).set_fill(S.BG, 0.6)
        bars = VGroup(*[RoundedRectangle(width=w * 0.7, height=w * 0.12, corner_radius=0.03, stroke_width=0)
                        .set_fill(shade, 0.9) for _ in range(3)]).arrange(DOWN, buff=w * 0.07).move_to(fr)
        self.frame, self.bars, self.shade = fr, bars, shade
        self.add(fr, bars)

    def set_shade(self, shade: str, run_time: float = 0.6):
        self.shade = shade
        return AnimationGroup(self.frame.animate.set_stroke(shade), self.bars.animate.set_fill(shade, 0.9),
                              run_time=run_time)


class Machine(Piece):
    """One BLUE machine with n GPUs, a GREEN replica above each, an optional PURPLE strategy
    frame and the PINK all-reduce ring. Machine(n_gpus=2, title=MACHINE_MULTI, subtitle=None,
    width=5.4, height=3.4, strategy="MirroredStrategy", shard=None).
    Parts: "box" "gpus" "replicas" (hidden) "strategy" (hidden: PURPLE dashed-free frame inside
      the box + mono label) "ring" (hidden: PINK ellipse over the replicas + "all-reduce")
      "shard" (hidden: GREY chip "shard 1" under the box, when shard is given)
    .step(shade, run_time=2.4) -> ONE animation (a Succession: a gradient arrow grows on each
      replica, the arrows rise into the ring and merge, one averaged arrow splits back down,
      every replica turns `shade`; the arrows leave the scene)
    .drift(shade) -> anims (every replica to `shade`, no ring: an island's own update)
    .gpus .replicas (lists) .ring_center()"""

    def __init__(self, n_gpus: int = 2, title: str = MACHINE_MULTI, subtitle: str | None = None,
                 width: float = 5.4, height: float = 3.4, strategy: str | None = "MirroredStrategy",
                 shard: str | None = None, shade: str = SHADES[0], **kw):
        super().__init__(**kw)
        mb = machine_box(title, subtitle, width=width, height=height, color=CLOUD, title_size=22,
                         sub_size=CAPTION)
        self.box = self.part("box", mb)
        body = mb.body
        gw = min(0.9, (width - 0.8) / n_gpus - 0.2)
        gpus = VGroup(*[gpu_chip(GPU_NAME, w=gw) for _ in range(n_gpus)]).arrange(RIGHT, buff=0.35)
        gpus.move_to([body.get_center()[0], body.get_bottom()[1] + 0.45, 0])
        reps = VGroup(*[Replica(shade, w=min(0.8, gw)) for _ in range(n_gpus)])
        for r, g in zip(reps, gpus):
            r.next_to(g, UP, buff=0.22)
        self.gpus, self.replicas = list(gpus), list(reps)
        self.part("gpus", gpus)
        self.part("replicas", reps, shown=False)
        sl = None
        if strategy:
            fr = RoundedRectangle(width=width - 0.3, height=body.height + 0.05, corner_radius=0.12,
                                  stroke_color=TOOL, stroke_width=2.5).set_fill(opacity=0).move_to(body)
            sl = mono(strategy, CAPTION, TOOL).move_to(fr.get_top() + DOWN * 0.24)
            self.part("strategy", VGroup(fr, sl), shown=False)
        ring_y = reps.get_top()[1] + 0.3
        ring_w = max(reps.width + 0.5, 1.6)
        ring = Circle(radius=0.5, stroke_color=LOOKUP, stroke_width=3).stretch_to_fit_width(ring_w) \
            .stretch_to_fit_height(0.4).move_to([reps.get_center()[0], ring_y, 0])
        rl = label("all-reduce", CAPTION, LOOKUP)
        rbg = RoundedRectangle(width=rl.width + 0.16, height=rl.height + 0.08, corner_radius=0.06,
                               stroke_width=0).set_fill(S.BG, 1)
        rl.move_to(ring.get_top())
        rbg.move_to(rl)
        self.part("ring", VGroup(ring, rbg, rl), shown=False)
        self.ring = ring
        if shard:
            sc = chip(shard, S.GREY, size=CAPTION).next_to(mb.frame, DOWN, buff=0.15)
            self.part("shard", sc, shown=False)
        guard(rl.get_top()[1] < body.get_top()[1] + 0.1, "the ring label reaches the machine title")
        if sl is not None:
            guard(rl.get_top()[1] < sl.get_bottom()[1] - 0.03,
                  f"the ring label runs into the strategy label: height >= 3.4 (now {height})")

    def ring_center(self):
        return self.ring.get_center().copy()

    def step(self, shade: str, run_time: float = 2.4):
        grads = [Arrow(r.get_top(), r.get_top() + UP * 0.45, buff=0, color=INK, stroke_width=4,
                       max_tip_length_to_length_ratio=0.35) for r in self.replicas]
        c = self.ring_center()
        merged = Arrow(c + DOWN * 0.18, c + UP * 0.18, buff=0, color=TURN, stroke_width=5,
                       max_tip_length_to_length_ratio=0.4)
        back = [Arrow(c, r.get_top() + UP * 0.05, buff=0.05, color=TURN, stroke_width=4,
                      max_tip_length_to_length_ratio=0.25) for r in self.replicas]
        return Succession(
            AnimationGroup(*[GrowArrow(a) for a in grads], run_time=run_time * 0.25),
            AnimationGroup(*[Transform(a, merged.copy()) for a in grads], run_time=run_time * 0.25),
            AnimationGroup(*[FadeOut(a) for a in grads], *[GrowArrow(b) for b in back],
                           run_time=run_time * 0.25),
            AnimationGroup(*[FadeOut(b) for b in back], *[r.set_shade(shade) for r in self.replicas],
                           run_time=run_time * 0.25),
        )

    def drift(self, shade: str, run_time: float = 0.8) -> list:
        return [r.set_shade(shade, run_time=run_time) for r in self.replicas]


def cable(a: Machine, b: Machine, color: str = LOOKUP, label_: str | None = None) -> VGroup:
    """The wire between two machines (PINK; GREY dashed + RED ✗ via no_wire()). Runs from a's
    right edge to b's left edge at the ring height. .line .label"""
    y = a.ring_center()[1]
    p, q = np.array([a.box.frame.get_right()[0], y, 0]), np.array([b.box.frame.get_left()[0], y, 0])
    ln = Line(p, q, color=color, stroke_width=5)
    g = VGroup(ln)
    g.line, g.label = ln, None
    if label_:
        t = mono(label_, CAPTION, color).next_to(ln, UP, buff=0.1)
        g.add(t)
        g.label = t
    return g


def no_wire(a: Machine, b: Machine) -> VGroup:
    """The missing wire between two islands: a GREY dashed line with a RED ✗ on it."""
    y = a.ring_center()[1]
    p, q = np.array([a.box.frame.get_right()[0], y, 0]), np.array([b.box.frame.get_left()[0], y, 0])
    ln = DashedLine(p + RIGHT * 0.05, q + LEFT * 0.05, color=S.GREY, stroke_width=3, dash_length=0.1)
    x = x_mark(0.28).move_to(ln)
    return VGroup(ln, x)


def span_ring(a: Machine, b: Machine, color: str = LOOKUP) -> VMobject:
    """One PINK all-reduce ring over every replica of both machines (Multi Worker)."""
    reps = VGroup(*a.replicas, *b.replicas)
    y = a.ring_center()[1]
    return Circle(radius=0.5, stroke_color=color, stroke_width=3).stretch_to_fit_width(reps.width + 0.6) \
        .stretch_to_fit_height(0.46).move_to([reps.get_center()[0], y, 0])


def delta_mark(color: str = ERR) -> VGroup:
    """The RED Δ between diverged replicas (a triangle glyph + "different weights")."""
    t = S.text("Δ", 40, color)
    c = label("different weights", CAPTION, color).next_to(t, DOWN, buff=0.08)
    return _keep(VGroup(t, c))


def tf_config_card(index: int, size: float = CAPTION) -> VGroup:
    """A schematic TF_CONFIG card (GREY dashed, plain TF example: values are placeholders):
    "cluster": {"worker": [‹machine-0›, ‹machine-1›]} and "task": {"type": "worker", "index": i}.
    3.9 x 1.9; header `TF_CONFIG`. Put illustration_tag("plain TF example") near it.
    .frame .rows .header"""
    lines = ['"cluster": {"worker":', f'  [{MACHINE_0}, {MACHINE_1}]}},',
             '"task": {"type": "worker",', f'         "index": {index}}}']
    rows = _mono_rows(lines, size, INK)
    fr = DashedVMobject(RoundedRectangle(width=rows.width + 0.5, height=rows.height + 0.4, corner_radius=0.12),
                        num_dashes=50, dashed_ratio=0.55).set_stroke(CONCEPT, 2.5)
    bg = RoundedRectangle(width=rows.width + 0.5, height=rows.height + 0.4, corner_radius=0.12,
                          stroke_width=0).set_fill(S.BG, 0.92)
    fr.move_to(rows)
    bg.move_to(rows)
    hd = mono("TF_CONFIG", CAPTION, S.GREY).next_to(fr, UP, buff=0.08).align_to(fr, LEFT)
    g = VGroup(bg, fr, rows, hd)
    g.frame, g.rows, g.header = fr, rows, hd
    return _keep(g)


class StrategyLadder(Piece):
    """Slide 27 redrawn: three rows "one machine · one GPU → One Device Strategy" (GREY dashed),
    "one machine · several GPUs → Mirrored Strategy" (PURPLE), "several machines → Multi Worker
    Mirrored Strategy" (GREY dashed); concept_tag() on rows 0 and 2. 12.8 x 2.3 (rows 9.4 wide,
    the tags right of them).
    .rows[i] (.left .right .frame) ; parts "pin" (hidden: YELLOW tag "the repo is here" right of
    row 1) ; .light(i) -> anims"""

    ROWS = (("one machine · one GPU", "One Device Strategy", False),
            ("one machine · several GPUs", "Mirrored Strategy", True),
            ("several machines", "Multi Worker Mirrored Strategy", False))

    def __init__(self, width: float = 9.4, **kw):
        super().__init__(**kw)
        rows = VGroup()
        for left_t, right_t, real in self.ROWS:
            col = TOOL if real else CONCEPT
            lt = label(left_t, 22, INK)
            ar = label("→", 22, S.GREY)
            rt = label(right_t, 22, col if real else INK)
            line = VGroup(lt, ar, rt)
            lt.move_to([-width / 2 + 0.3, 0, 0], aligned_edge=LEFT)
            ar.move_to([-width / 2 + 4.45, 0, 0])
            rt.move_to([-width / 2 + 4.85, 0, 0], aligned_edge=LEFT)
            guard(lt.get_right()[0] < ar.get_left()[0] - 0.1, f"ladder: {left_t!r} reaches the arrow")
            fr = box(width, 0.66, col, fill_opacity=0.06 if real else 0.0, radius=0.12, dashed=not real)
            r = VGroup(fr, line)
            r.left, r.right, r.frame = lt, rt, fr
            rows.add(r)
        rows.arrange(DOWN, buff=0.18)
        self.rows = rows
        self.part("rows", rows)
        for i in (0, 2):
            ct = concept_tag().next_to(rows[i].frame, RIGHT, buff=0.15)
            self.part(f"concept{i}", ct)
        pin = _keep(tag("the repo is here", TURN)).next_to(rows[1].frame, RIGHT, buff=0.15)
        self.part("pin", pin, shown=False)
        for r in rows:
            guard(r.right.get_right()[0] < r.frame.get_right()[0] - 0.15, f"ladder row text overflows: {r.right}")

    def light(self, i: int, color: str = TURN) -> list:
        return [Indicate(self.rows[i].right, color=color, scale_factor=1.06)]


# ================================================================== V4 · the batch splitter (S06)
class BatchTray(VGroup):
    """dataset.batch(n) as a GREEN tray of n image squares (cols x rows), the mono caption
    `dataset.batch(n)` above (caption=None: none). BatchTray(n, cols=None, cell=0.2).
    .squares .frame .caption .slices(k) -> k VGroups of n/k squares (column blocks, left to
    right; raises if k does not divide n) .split_to(points, k, cols=4, max_h=0.7) -> anims
    (each slice regroups into `cols` columns, shrinks to max_h if taller, and lands with its
    bottom on its point, e.g. gpu_grid(...).slot(i); the frame fades)"""

    def __init__(self, n: int, cols: int | None = None, cell: float = 0.2, caption: str | None = "auto",
                 color: str = OWN, **kw):
        super().__init__(**kw)
        cols = cols or min(n, 16)
        rows_n = -(-n // cols)
        sq = VGroup(*[Square_(cell, color) for _ in range(n)])
        sq.arrange_in_grid(rows=rows_n, cols=cols, buff=cell * 0.25, flow_order="dr")
        fr = RoundedRectangle(width=sq.width + 0.3, height=sq.height + 0.3, corner_radius=0.1,
                              stroke_color=color, stroke_width=3).set_fill(color, 0.05).move_to(sq)
        self.n, self.cols, self.rows_n = n, cols, rows_n
        self.squares, self.frame = sq, fr
        self.add(fr, sq)
        self.caption = None
        if caption:
            text = f"dataset.batch({n})" if caption == "auto" else caption
            c = mono(text, 22, INK).next_to(fr, UP, buff=0.12)
            self.add(c)
            self.caption = c

    def slices(self, k: int) -> list:
        if self.n % k:
            raise ValueError(f"{self.n} does not split into {k} equal slices")
        per = self.n // k
        order = sorted(range(self.n), key=lambda i: (i // self.rows_n, i % self.rows_n))  # column blocks
        return [VGroup(*[self.squares[j] for j in order[s * per:(s + 1) * per]]) for s in range(k)]

    def split_to(self, points, k: int, run_time: float = 1.2, cols: int = 4, max_h: float = 0.7) -> list:
        sl = self.slices(k)
        out = [FadeOut(self.frame)]
        for g, p in zip(sl, points):
            tgt = g.copy().arrange_in_grid(cols=min(len(g), cols), buff=0.05)
            if tgt.height > max_h:
                tgt.scale_to_fit_height(max_h)
            out.append(Transform(g, tgt.move_to(p, aligned_edge=DOWN)))
        return [AnimationGroup(*out, run_time=run_time)]


def Square_(side: float, color: str) -> VMobject:
    """One image of a batch (a small GREEN tile)."""
    return RoundedRectangle(width=side, height=side, corner_radius=side * 0.15, stroke_color=color,
                            stroke_width=1.5).set_fill(color, 0.55)


def gpu_grid(k: int, per_row: int = 4, w: float = 0.8, buff: float = 0.45, strategy: bool = True) -> VGroup:
    """k BLUE GPU chips (rows of `per_row`) in an optional PURPLE strategy frame (mono label
    "MirroredStrategy"). 4 per row: 5.2 x 2.2 (one row) / 5.2 x 3.9 (two rows) with the frame.
    .chips .frame (or None) .slot(i) -> the point just above chip i where its slice's bottom
    lands (room for 0.7 above each chip)"""
    chips = VGroup(*[gpu_chip(GPU_NAME, w=w) for _ in range(k)])
    chips.arrange_in_grid(rows=-(-k // per_row), cols=min(k, per_row), buff=(buff, 1.0))
    g = VGroup(chips)
    g.chips, g.frame = chips, None
    if strategy:
        fr = RoundedRectangle(width=chips.width + 0.6, height=chips.height + 1.55, corner_radius=0.14,
                              stroke_color=TOOL, stroke_width=2.5).set_fill(opacity=0)
        fr.move_to(chips).shift(UP * 0.175)
        sl = mono("MirroredStrategy", CAPTION, TOOL).move_to(fr.get_corner(DOWN + LEFT) + np.array([0.2, 0.22, 0]),
                                                              aligned_edge=LEFT)
        g.add(fr, sl)
        g.frame = VGroup(fr, sl)
    g.slot = lambda i: chips[i].get_top() + UP * 0.12
    return g


class BatchDial(VGroup):
    """The dial on the tray: a GREY knob with a needle and the mono `batch(n)` beside it.
    .turn_to(n) -> anims (needle turns, the label swaps) .n .text"""

    def __init__(self, n: int, r: float = 0.32, **kw):
        super().__init__(**kw)
        self.n = n
        face = Circle(radius=r, stroke_color=S.GREY, stroke_width=3).set_fill(S.BG, 1)
        ticks = VGroup(*[Line(UP * r * 0.8, UP * r, color=S.GREY, stroke_width=2).rotate(a, about_point=ORIGIN)
                         for a in np.linspace(-2.2, 2.2, 7)])
        needle = Line(ORIGIN, UP * r * 0.75, color=TURN, stroke_width=4).rotate(1.6, about_point=ORIGIN)
        knob = VGroup(face, ticks, needle)
        self.text = mono(f"batch({n})", 24, INK).next_to(knob, RIGHT, buff=0.2)
        self.face, self.needle, self._angle = face, needle, 1.6
        self.add(knob, self.text)
        _keep(self)

    def turn_to(self, n: int, angle: float = -3.0) -> list:
        new = mono(f"batch({n})", 24, INK).move_to(self.text, aligned_edge=LEFT)
        self.n = n
        out = [Rotate(self.needle, angle, about_point=self.face.get_center())]
        out += swap_text(self, self.text, new)
        self.text = new
        return out


# ================================================================== V5 · request clock vs job ticket (S07)
def handler_box(route: str = "POST /retrain", w: float = 2.6) -> VGroup:
    """The schematic web server (GREY) with its handler route in mono (illustration_tag() it).
    .frame .route .glyph"""
    srv = server(0.8, 2, S.GREY)
    r = mono(route, CAPTION, INK)
    body = VGroup(srv, r).arrange(DOWN, buff=0.14)
    fr = box(max(w, body.width + 0.4), body.height + 0.35, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.14)
    body.move_to(fr)
    g = VGroup(fr, srv, r)
    g.frame, g.route, g.glyph = fr, r, srv
    return g


class LifetimeRings(Piece):
    """Three nested lifetimes around the server (schematic): "request" (inner, GREY), "server
    instance" (middle, GREY), "job" (outer, BLUE), each a rounded ring with a two-part label
    (name + GREY lifetime; the inner one in two rows) inside its top edge. In place: centred at
    (0, -0.35); request 6.4 x 2.9, server 9.6 x 4.0, job 12.8 x 5.4 (y -3.05..2.35).
    Parts (hidden): "request" "server" "job"; .ring(name) the frame; .inner_center() where the
    handler_box goes (2.6 x 1.5 fits there)"""

    RINGS = (("request", "seconds–minutes · set by the server and proxies", S.GREY, (6.4, 2.9)),
             ("server instance", "until the platform recycles it", S.GREY, (9.6, 4.0)),
             ("job", "until it finishes or fails · on its own VM", CLOUD, (12.8, 5.4)))

    def __init__(self, center=(0, -0.35, 0), **kw):
        super().__init__(**kw)
        c = np.array(center, dtype=float)
        self._rings = {}
        for key, (name, life, col, (w, h)) in zip(("request", "server", "job"), self.RINGS):
            fr = RoundedRectangle(width=w, height=h, corner_radius=min(0.6, h / 4), stroke_color=col,
                                  stroke_width=3).set_fill(opacity=0).move_to(c)
            nm = label(name, CAPTION, col if col != S.GREY else INK)
            lf = label(f"· {life}", CAPTION, S.GREY)
            lab = VGroup(nm, lf).arrange(RIGHT, buff=0.12)
            if lab.width > w - 0.5:                      # the inner ring: two rows
                lf = label(life, CAPTION, S.GREY)
                lab = VGroup(nm, lf).arrange(DOWN, buff=0.06)
            lab.move_to(fr.get_top() + DOWN * (0.12 + lab.height / 2))
            guard(lab.width < w - 0.3, f"ring label {name!r} is wider than its ring")
            self._rings[key] = fr
            self.part(key, VGroup(fr, lab), shown=False)
        guard(self.ring("job").get_top()[1] <= LREF_BOTTOM - 0.1 and self.ring("job").get_bottom()[1] >= -3.6,
              "the job ring leaves the frame (keep the default centre)")

    def ring(self, name: str):
        return self._rings[name]

    def inner_center(self):
        return self.ring("request").get_center() + DOWN * 0.35


class TrainingBar(VGroup):
    """The ~1 hour of training as a bar: a GREY track of `width` and a GREEN fill that grows; the
    caption "training · ~1 hour" above. .grow(frac, run_time) -> anim .snap() -> anims (the fill
    turns RED and a crack appears) .vanish() -> anims .track .fill .caption"""

    def __init__(self, width: float = 3.0, caption: str | None = "training · ~1 hour", **kw):
        super().__init__(**kw)
        tr = RoundedRectangle(width=width, height=0.34, corner_radius=0.08, stroke_color=S.GREY,
                              stroke_width=2).set_fill(S.BG, 0.8)
        fill = Rectangle(width=0.02, height=0.24, stroke_width=0).set_fill(OWN, 0.9)
        fill.move_to(tr.get_left() + RIGHT * 0.06, aligned_edge=LEFT)
        self.track, self.fill, self.w = tr, fill, width
        self.add(tr, fill)
        self.caption = None
        if caption:
            c = label(caption, CAPTION, INK).next_to(tr, UP, buff=0.1)
            self.add(c)
            self.caption = c
        _keep(self)

    def grow(self, frac: float, run_time: float = 1.5):
        w = max(0.02, (self.w - 0.12) * frac)
        left = self.track.get_left() + RIGHT * 0.06
        return self.fill.animate(run_time=run_time, rate_func=linear).stretch_to_fit_width(w) \
            .move_to(left, aligned_edge=LEFT)

    def snap(self) -> list:
        f = self.fill
        crack = _poly([(f.get_right()[0] - 0.05, f.get_top()[1] + 0.12), (f.get_right()[0] + 0.05, f.get_center()[1]),
                       (f.get_right()[0] - 0.05, f.get_bottom()[1] - 0.12)], ERR, 4)
        _stage_hidden(self, crack, "_crk")
        return [self.fill.animate.set_fill(ERR, 0.9), _Reveal(crack, "_crk")]


class JobTicket(VGroup):
    """The job ticket: a BLUE ticket (notched sides) "custom job" with the GREY mono id JOB_ID.
    .frame .title .id_text"""

    def __init__(self, title: str = "custom job", w: float = 2.4, **kw):
        super().__init__(**kw)
        h = 0.95
        fr = RoundedRectangle(width=w, height=h, corner_radius=0.1, stroke_color=CLOUD,
                              stroke_width=3).set_fill(CLOUD, 0.15)
        notches = VGroup(*[Circle(radius=0.12, stroke_color=CLOUD, stroke_width=3).set_fill(S.BG, 1)
                           .move_to(fr.get_left() if s < 0 else fr.get_right()) for s in (-1, 1)])
        t = label(title, CAPTION, INK)
        i = mono(JOB_ID, CAPTION, S.GREY)
        VGroup(t, i).arrange(DOWN, buff=0.08).move_to(fr)
        self.frame, self.title, self.id_text = fr, t, i
        self.add(fr, notches, t, i)
        _keep(self)


class StateChips(VGroup):
    """The job's state machine QUEUED → PENDING → RUNNING → SUCCEEDED as GREY mono chips joined by
    arrows. .light(i) -> anims (chip i lights BLUE, SUCCEEDED GREEN; the earlier ones go GREY)
    .chips"""

    def __init__(self, states=JOB_STATES, size: float = CAPTION, **kw):
        super().__init__(**kw)
        self.chips = [chip(s, S.GREY_DARK, size=size, font=MONO, text_color=S.GREY) for s in states]
        row = []
        for k, c in enumerate(self.chips):
            if k:
                row.append(label("→", size, S.GREY))
            row.append(c)
        self.add(*row)
        self.arrange(RIGHT, buff=0.12)
        _keep(self)

    def light(self, i: int) -> list:
        out = []
        for k, c in enumerate(self.chips):
            if k == i:
                col = OWN if k == len(self.chips) - 1 else CLOUD
                out += [c.box.animate.set_stroke(col, 3).set_fill(col, 0.18), c.text.animate.set_color(INK)]
            elif k < i:
                out += [c.box.animate.set_stroke(S.GREY_DARK, 2).set_fill(S.GREY_DARK, 0.1),
                        c.text.animate.set_color(S.GREY)]
        return out


class CostMeter(VGroup):
    """The GOLD meter on the job's VM: a half dial whose needle sweeps while the job runs, the
    label "$ while running". .run(run_time) -> anim .stop() -> anim (needle back to rest)"""

    def __init__(self, r: float = 0.42, **kw):
        super().__init__(**kw)
        arc = Arc(radius=r, start_angle=0, angle=PI, stroke_color=COST, stroke_width=4)
        base = Line(LEFT * r, RIGHT * r, color=COST, stroke_width=2)
        needle = Line(ORIGIN, UP * r * 0.85, color=COST, stroke_width=4).rotate(1.2, about_point=ORIGIN)
        coin = cost_tick(0.08).move_to(ORIGIN)
        t = label("$ while running", CAPTION, COST).next_to(base, DOWN, buff=0.12)
        self.needle, self._base = needle, base
        self.add(arc, base, needle, coin, t)
        _keep(self)

    def run(self, run_time: float = 2.0):
        return Rotate(self.needle, -2.4, about_point=self._base.get_center(), run_time=run_time, rate_func=linear)

    def stop(self, run_time: float = 0.5):
        return Rotate(self.needle, 2.4, about_point=self._base.get_center(), run_time=run_time)


# ================================================================== S02 data version + S01/S08 miniatures
class DataVersion(Piece):
    """A data version as a pair (S02 aside, S08 rule 6): a BLUE bucket object "snapshot" and a
    GREEN record card "version record", joined by a PINK link "content hash". 7.0 x 1.6.
    Parts: "snapshot" "record" "link" (hidden); .flash() -> anim (the link pulses)"""

    def __init__(self, gap: float = 2.6, **kw):
        super().__init__(**kw)
        b = bucket(None, w=0.9)
        st = label("snapshot", CAPTION, CLOUD).next_to(b, DOWN, buff=0.1)
        snap = VGroup(b, st)
        rec = card_glyph("version record", None, OWN, w=2.6)
        snap.move_to(LEFT * (gap / 2 + 1.0))
        rec.move_to(RIGHT * (gap / 2 + 1.3))
        ln = Line(b.get_right() + RIGHT * 0.15, rec.frame.get_left() + LEFT * 0.1, color=LOOKUP, stroke_width=4)
        lt = label("content hash", CAPTION, LOOKUP).next_to(ln, UP, buff=0.1)
        self.part("snapshot", snap)
        self.part("record", rec)
        self.part("link", VGroup(ln, lt), shown=False)
        self.link_line = ln

    def flash(self, run_time: float = 0.8):
        return ShowPassingFlash(self.link_line.copy().set_stroke(TURN, 8), time_width=0.5, run_time=run_time)


MINI_KINDS = ("run", "package", "gpus", "batch", "job", "data")
MINI_CAPTIONS = {"run": "the run", "package": "the package", "gpus": "the GPUs", "batch": "the batch",
                 "job": "the job", "data": "the data"}


class Miniature(VGroup):
    """A thumbnail of one set piece (S01's map, S08's recap), ~1.8 x 1.2 plus its caption (sans
    22 pt) under it: "run" (a ledger row with ticks), "package" (a box labelled setup.py), "gpus"
    (two chips joined by a ring), "batch" (a tray cut into slices), "job" (a ticket with a clock),
    "data" (a bucket linked to a record card). .glyph .caption .kind
    .crack() -> anims (a RED crack over the glyph: "where it quietly breaks"; .crack_line)
    .replay() -> ONE animation (~1 s: a tick drops, the package lights, the ring pulses, the
    slices part, the ticket returns an id, the link flashes)"""

    def __init__(self, kind: str, caption: bool = True, **kw):
        super().__init__(**kw)
        if kind not in MINI_KINDS:
            raise ValueError(f"miniature kind {kind!r} (one of {MINI_KINDS})")
        self.kind = kind
        g = VGroup()
        self._extra = None
        if kind == "run":
            fr = RoundedRectangle(width=1.8, height=0.75, corner_radius=0.1, stroke_color=TURN,
                                  stroke_width=3).set_fill(CLOUD, 0.12)
            rail = RoundedRectangle(width=1.4, height=0.24, corner_radius=0.05, stroke_color=S.GREY,
                                    stroke_width=1.5).move_to(fr).shift(DOWN * 0.12)
            ticks = VGroup(*[RoundedRectangle(width=0.08, height=0.18, corner_radius=0.03, stroke_width=0)
                             .set_fill(OWN, 0.9).move_to(rail.get_left() + RIGHT * (0.15 + 0.22 * k))
                             for k in range(3)])
            name = Line(fr.get_corner(UP + LEFT) + np.array([0.15, -0.18, 0]),
                        fr.get_corner(UP + LEFT) + np.array([1.0, -0.18, 0]), color=INK, stroke_width=3)
            g.add(fr, rail, ticks, name)
            self._extra = (rail, ticks[0])
        elif kind == "package":
            b = RoundedRectangle(width=1.5, height=1.0, corner_radius=0.08, stroke_color=OWN,
                                 stroke_width=3).set_fill(OWN, 0.15)
            t = mono("setup.py", CAPTION, INK).move_to(b)
            g.add(b, t)
            self._extra = b
        elif kind == "gpus":
            c1 = RoundedRectangle(width=0.6, height=0.4, corner_radius=0.05, stroke_color=CLOUD,
                                  stroke_width=3).set_fill(CLOUD, 0.2).shift(LEFT * 0.5 + DOWN * 0.2)
            c2 = c1.copy().shift(RIGHT * 1.0)
            rg = Circle(radius=0.5, stroke_color=LOOKUP, stroke_width=3).stretch_to_fit_width(1.6) \
                .stretch_to_fit_height(0.36).shift(UP * 0.3)
            g.add(c1, c2, rg)
            self._extra = rg
        elif kind == "batch":
            tray = VGroup(*[Square_(0.16, OWN) for _ in range(16)]).arrange_in_grid(rows=2, cols=8, buff=0.04)
            fr = RoundedRectangle(width=tray.width + 0.2, height=tray.height + 0.2, corner_radius=0.06,
                                  stroke_color=OWN, stroke_width=2.5).move_to(tray)
            cuts = VGroup(*[DashedLine(fr.get_top() + RIGHT * dx, fr.get_bottom() + RIGHT * dx, color=LOOKUP,
                                       stroke_width=2, dash_length=0.05) for dx in (-0.4, 0, 0.4)])
            g.add(fr, tray, cuts)
            self._extra = tray
        elif kind == "job":
            t = RoundedRectangle(width=1.3, height=0.7, corner_radius=0.08, stroke_color=CLOUD,
                                 stroke_width=3).set_fill(CLOUD, 0.15)
            ck = Circle(radius=0.26, stroke_color=INK, stroke_width=2.5).set_fill(S.BG, 1).move_to(t.get_right())
            hands = VGroup(Line(ORIGIN, UP * 0.17), Line(ORIGIN, RIGHT * 0.12)).set_stroke(INK, 2.5).move_to(ck)
            hands.shift(ck.get_center() - hands[0].get_start())
            g.add(t, ck, hands)
            self._extra = t
        else:   # data
            b = bucket(None, w=0.6)
            card = RoundedRectangle(width=0.7, height=0.5, corner_radius=0.06, stroke_color=OWN,
                                    stroke_width=3).set_fill(OWN, 0.15).shift(RIGHT * 0.65)
            b.move_to(LEFT * 0.6)
            ln = Line(b.get_right() + RIGHT * 0.05, card.get_left() + LEFT * 0.05, color=LOOKUP, stroke_width=3)
            g.add(b, card, ln)
            self._extra = ln
        self.glyph = g
        self.add(g)
        self.caption = None
        if caption:
            c = label(MINI_CAPTIONS[kind], 22, INK).next_to(g, DOWN, buff=0.18)
            self.add(c)
            self.caption = c
        self.crack_line = None
        _keep(self)

    def crack(self) -> list:
        g = self.glyph
        a, b = g.get_corner(UP + RIGHT) + np.array([-0.25, 0.05, 0]), g.get_corner(DOWN + LEFT) + np.array([0.3, -0.05, 0])
        pts = [a + (b - a) * t + np.array([0.1 * (-1) ** k, 0, 0]) for k, t in enumerate(np.linspace(0, 1, 6))]
        c = _poly([(p[0], p[1]) for p in pts], ERR, 3.5)
        _stage_hidden(self, c, "_crack")
        self.crack_line = c
        return [_Reveal(c, "_crack")]

    def replay(self, run_time: float = 1.0):
        k, e = self.kind, self._extra
        if k == "run":
            rail, t0 = e
            t = t0.copy().move_to(rail.get_left() + RIGHT * (0.15 + 0.22 * 3) * rail.width / 1.4)
            return Succession(FadeIn(t, shift=DOWN * 0.2, run_time=run_time * 0.6), FadeOut(t, run_time=run_time * 0.4))
        if k == "batch":
            return Indicate(e, color=LOOKUP, scale_factor=1.08, run_time=run_time)
        if k == "data":
            return ShowPassingFlash(e.copy().set_stroke(TURN, 6), time_width=0.6, run_time=run_time)
        return Indicate(e, color=TURN, scale_factor=1.1, run_time=run_time)


def miniature(kind: str, caption: bool = True) -> Miniature:
    """Miniature(kind): see the class. kind in MINI_KINDS."""
    return Miniature(kind, caption)


def miniature_row(kinds=MINI_KINDS[:5], gap: float = 0.55) -> VGroup:
    """The miniatures in a row, centred (5 kinds: 12.0 wide). .items {kind: Miniature}"""
    ms = [Miniature(k) for k in kinds]
    g = VGroup(*ms).arrange(RIGHT, buff=gap, aligned_edge=UP)
    guard(g.width <= 13.0, f"miniature row {g.width:.1f} wide")
    g.items = dict(zip(kinds, ms))
    return g
