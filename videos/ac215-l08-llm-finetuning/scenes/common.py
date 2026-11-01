"""Shared code for AC215 L8 (LLM: Finetuning; follow-along: dlops-io/llm-finetuning @ 44ef6f0 and the
course Colab "Tutorial - Finetuning with QLoRA"): paths, narration, the semantic colours of BRIEF.md,
the README / Colab trackers, loaders for the real captures in assets/ (the persona masked, the full
name refused, the capture laptop's world-writable modes refused), terminal / panel / card helpers
(ported unchanged from L07's tested common.py, incl. its QA fixes), and this video's set pieces
V1-V8 of BRIEF.md. Tested on screen by build/common_test.py (CommonTest, PieceTest: explainer.check
OK, preview sheets read).

Notes for scene authors
=======================

    from common import *      # every scene: SAY = NARRATION["S07"]; assert len(SAY) == n;
                              # one `with self.voiceover(SAY[i]) as vo:` per SAY line, in order
All text here is 20-34 pt. Never .scale() a group that holds text below 1.0: Piece set pieces have
.rescale(k) (shapes shrink, text keeps its size). Methods return ANIMATIONS (play them) or MOBJECTS
(placed, not added: FadeIn them) unless they say "plays". Set pieces are built centred at ORIGIN
unless they say "in place" (then they already sit where the script wants them: above a 3-row strip).

Frame budget. Tracker top left (x -6.5.., y 2.93..3.5), lecture_ref top right (y 3.13..3.6). A
one-line chip in the top band: top_chip(...) (y 2.66). Terminals: full width 12.6, 22 pt, 65
characters a row, bottom at BOTTOM (-3.5), at most 13 rows (12 rows: top 2.19). A 3-row strip's top
is STRIP_TOP (-1.44): an "in place" piece above a strip spans y -1.3..2.8. The laptop prompts are
long (P_DC is 55 characters): term()/type_cmd() fold a command onto the row under the prompt.

Names. unname(s): the persona name (any case) -> PERSONA "‹instructor›", drawn GREY by every panel,
terminal row, card (mtext, grey_masks). The full name never appears: its lines (NEVER_SOURCE:
dataset-creator/cli.py 133, 140; README.md 118, 119, 167) raise, and every shown line is checked
(guard_names). Other masks: HF_USER, PROJECT_NO, ENDPOINT_ID (ENDPOINT_REDACTED is the whole path).
persona_chip() / mask_chip(HF_USER) are the GREY chips. The key is key_glyph() / key_outline(),
never a value.

Data and sources
    NARRATION["S01"] … ["S16"]   SAY lines from script.md      TITLES[cls], SPEC (video.yaml)
    capture(name, folder) -> Capture: assets/terminal/<folder>/<name>.txt; name may be the number
        alone ("05" -> 05-generate.txt) or "folder/name" ("dataset-creator/09",
        "expected/colab-c75-train", "expected/readme-cost-table").
        CAPTURE FOLDERS: laptop, dataset-creator, gemini-finetuner, expected (line 1 of an expected/
        file is a '#' provenance header; in expected/colab-cNN the cell's code follows the `$` and is
        .cmd, never output). Never: capture-only/ (scripted data: scripted_text()), the .plain build
        logs, laptop/09 line 4 and laptop/19 line 5 (the capture's base image), any `ls -la` row with
        rw-rw-rw- / drwxrwxrwx modes (use .names_sizes).
      .cmd .lines .exit .first (file line of .lines[0]) .header
      .line(n) FILE line n (emoji stripped)   .color(n) (🔵 GREY, 🟢 ✅ GREEN, ❌ ⚠ RED)
      .at(2, (5, 7), "…", 33) lines by file number   .out(*spec) -> [(text, colour)] for t.print
      .cut(n, "x") line n through "x", then " …"   .cut_before(n, " exit") (laptop/07, /18 line 27)
      .squeeze(n) BuildKit padding -> two spaces   .names_sizes(5, (6, 9)) `ls -la` rows as
      "size  name"   .fold(a, b, "X … Y")  .join(..)  .split_at(n, col)  .typed(n)  .pick() (L1)
    source_text(path)  excerpt(path, a, b)  source_line(path, n)  readme(a, b) (README.md rows)
        paths as in the repo ("dataset-creator/cli.py", "gemini-finetuner/cli.py" = the redacted copy,
        "env.dev", "README.md"); Colab cells "colab/cell-70.py".
        shown_path(path): "gemini-finetuner/cli.py", "QLoRA notebook · 4.2 · cell 70"
        colab_where(70) "QLoRA notebook · 4.2 · cell 70" (COLAB_SECTION: the notebook's own
        heading numbers; Part B cells read "Part B · 1")   cell_title(path)
    expected_where("readme-chat-example") -> "README.md · lines 288–301"
    scripted_text("cheese_qa_0") -> lines; scripted_pairs() -> the 20 scripted {question, answer}
    loss_points() -> [(50, 2.007381) … (450, 1.350437)] (c75)   eval_table() -> {"Base (4-bit)":
        (2.6498, 14.15), "Fine-tuned (4-bit + LoRA)": (1.3872, 4.0)} (c80)
    Numbers: TRAINABLE 1,146,880  ALL_PARAMS_4BIT 375,848,960  QWEN_LAYERS 28  HIDDEN 1024  Q_OUT
        2048  KV_OUT 1024  LORA_R 8  LORA_ALPHA 16  ABSMAX_X (slide 45)  NF4_LEVELS (16)
    Names: TEACHER "gemini-3.1-flash-lite"  BASE_QWEN  KEY_FILE "llm-service-account.json"
        BUCKET_TEMPLATE "gs://<your-bucket>"  DATASET_PREFIX "llm-finetune-dataset-small"  GUIDE

Colours (BRIEF.md "Colours", binding)
    LAPTOP GREY · CLOUD (= MODEL: everything a model writes) BLUE · CTR TEAL · SYSTEM ORANGE ·
    OWN (= DATA = VENV = ADAPTER: your files, uv.lock, A and B) GREEN · TOOL PURPLE · ERR RED ·
    TURN (= PULSE, the backward pass) YELLOW · COST (= KEY) GOLD · LOOKUP PINK · FROZEN (W₀, the
    persona chip; FUTURE = lecture-only, dashed) GREY · INK white · BIT_SIGN / BIT_EXP / BIT_FRAC
    white / pink / green outlines (bit strips only). dtype tags are white: dtype_tag("NF4").
Running example
    P_HOME P_WS "student@laptop:~/AC215$"  P_REPO ".../AC215/llm-finetuning$"  P_DC ".../dataset-creator$"
    P_GF ".../gemini-finetuner$"  P_CTR_DC "app@6f5113cdb660:/app$"  P_CTR_GF "app@2a2550dec953:/app$"
    CTR_DC_TITLE "container · llm-dataset-creator"  CTR_GF_TITLE "container · gemini-finetuner"
    LAPTOP_TITLE "laptop"  SECOND "laptop · second terminal"  COLAB_TITLE "QLoRA notebook · Colab"

Trackers (top left, YELLOW)
    tracker(key, step=None)  keys = script.md's TRACKER names: Prereq DsRun DsGen DsSamples DsPrep
        DsUp FtRun FtModel FtCost FtChat ColabA ColabB Qwen Data Tune Eval Save Down (SECTIONS:
        head "README" or "Colab", section, steps; EXTRA_STEPS = the steps the README lacks).
        self.play(tr.goto(k))   self.play(caption_extra(tr)) / caption_extra(tr, on=False)
    tr = switch_section(self, tr, "DsGen", 1)  (plays: old lifts away, new drops in)
    lref("7–8") = lecture_ref(8, ...) top right;  lr = lref_swap(self, lr, "68–69") (plays; old may be None)
    swap_text(parent, old, new) -> anims: the house sequential text swap (never Transform text)

Terminal helpers (term() masks and greys "…" and the masks on every line it places)
    term(prompt=P_WS, rows=12, title=None, container=None|"dc"|"gf", top=None): container -> TEAL
        frame, title and prompt of that container
    type_cmd(scene, t, cmd)  every typed command (folds at spaces, quote-aware, " \\" + indent 4)
    show(scene, t, cap, *spec, wrap=False) = t.print(scene, cap.out(*spec))   print_build(scene, t,
        [cap.line(3), …]) BuildKit rows with GREY time tags   bare_prompt(scene, t)
    cd_prompt(scene, t, P_DC)  enter_container(t, "dc"|"gf") / leave_container(t, P_DC) -> anims
    resize(scene, t, rows, keep=None)  strip_top(rows)  second_terminal(scene, P_DC, rows=7, top=2.75)
    retitle(t, title) -> anim  session(scene, t, cap, …) replays a capture with prompt lines
    frame_tags(t, nokey_tag(), billed_tag()) on the title bar (before the terminal shows)
    beside(tag, t, line) + pin(scene, line, tag) (raises if it would cover text)  unpin
    col_box(line, a, b)  bracket(mobs, text)  under(mob) strike(mob) ring(mob)  at_bottom(mob)
    item_rows / wrapped_glyphs / wrapped_at (find text across a wrap=True fold)

Panels and cards
    src_panel(path, a, b=None, wrap=True|{n: [...]}, focus=, join=, cut_comments=, subtitle=True,
        max_rows=12) CODE(): header "path · lines a–b" (Colab: "QLoRA notebook · 4.2 · cell 70 ·
        lines 2–13"); folded: src_panel(path, [2, (5, 9)]); raises when > 12 rows or > 12.9 wide.
        .bar(n, colour) .span(n, sub) .rows_of(n)
    quote_card("readme-cost-table", (4, 11), wrap=88)  QUOTE(): GREY card, header from the file's
        README lines, tag `expected` (fence lines refused); quote_card(144, 145) quotes README.md.
    recorded_box("colab-c75-train", (5, 15), tag_at="auto"|"down"|"top")  RECORDED(): output box
        (never a terminal), header "QLoRA notebook · 4.4 · cell 75 · saved output", tag
        `recorded · the staff's saved Colab run (A100)`
    log_panel(lines, header)  output_box(lines, header)  readme_chip(where, phrase)  top_chip(text)
    excerpt_chip(sub, header, line=source_line(...))  cmd_chip(cmd, note_)  readme_card(where, lines)
    turn_card(rows) the static "your turn" card (str = command, (cmd, "extra"), (cmd, note),
        Prose("…"), (Prose("billed · …"), COST) last)   extra_card(purpose)  card_rows(items, header)
    table_card(headers, rows)  LookFor(items, title="with your key, look for") .write_item(i)
    ponder_at(scene, "question\\nsecond row", seconds=8, hide=(strip,)) plays the card; FadeOut it
        at the next SAY block   colab_frame() BLUE notebook frame + illustration tag (in place, 12.9
        x 6.25)   menu_path(["Runtime", "Change runtime type"]) .light(i)   Counter(text, value)
    question_card("Why is the sky blue?")  answer_card(rows, colour=MODEL, title=, width=5.6,
        dashed=) (rows broken to fit; persona GREY)   card_glyph(title, sub, colour, w)
    shape_card(lines, colour=OWN, header=, dashed=) mono rows in a card (V4's shapes)
Tags (GREY unless said): your_turn() (YELLOW) extra_tag() illustration_tag(note_) expected_tag()
    recorded_tag() scripted_tag() nokey_tag() billed_tag()/cost_tag() (GOLD) free_tag() (GREEN)
    estimate_tag() differ_tag() ("your id will differ") erratum_tag(note_) harmless_tag()
    recording_tag() ("at the time of recording") concept_tag() (dashed, "concept · lecture only")
    template_tag() dtype_tag("FP16") (white) stamp(text, colour) fix_chip(text) concept_box(text)
Glyphs: key_glyph(name=KEY_FILE) key_outline() snowflake() spark() x_mark() tick_mark() file_row(name)
    ghost_file(name) model_box(name, sub=) container_box(title) laptop_zone() cost_tick() json_card()

Set pieces (Piece = VGroup with named parts: piece.reveal(scene, *names) / .hide plays;
    self.play(*piece.parts_in("a")); a part not shown yet is a member at opacity 0 (never FadeOut a
    part, FadeOut the whole piece); Piece(show=(...)) starts with only those parts visible)
    V1 ThreeDials()  6.5 x 4.2: BLUE model box with a grid of weight cells, dials prompt / context /
       weights. .turn(name) -> anims (needle turns, dial + wire YELLOW) .settle(name) .shimmer() ->
       anim (the weights change) .input_point() .output_point() .dials[name] .cells
       AdapterSwitch(on=True)  2.8 x 1.3: "adapter on/off" + disable_adapter(); .flip(on) -> anims
       NextTokenBars(tokens, probs, width=5.0)  5.0 x 1.5 (+ prompt row): .morph(tokens, probs,
       colour) -> anims (tag it illustration_tag())
    V2 Stage(show=None)  in place, 12.8 x 4.0 (y -1.25..2.75): laptop (rows "ws" "repo" "dc" "gf"
       "env" "secrets", dashed key), containers dc / gf with /app and /secrets, PINK mounts, the BLUE
       cloud with pins global / bucket / us-central1 / us. Parts: laptop key dc gf mounts_dc
       mounts_gf cloud pin_global pin_bucket pin_tune pin_us. .route("--generate"|"--upload"|
       "--train"|"--chat") -> Arrow  .blocked(cmd) -> stub + RED "no key" stamp  .job_arrow()
       (bucket -> us-central1)  .key_in() -> anims  .light(part) -> anims  .row(name)
    V3 Teacher(show=None)  in place, 12.6 x 4.0 (y -1.37..2.65): cards (system instruction ·
       cli.py lines 36–145, input prompt · line 169), BLUE teacher gemini-3.1-flash-lite (location =
       global), mould response_schema, the net `except Exception` (part "net"), the pile (five
       slots, NUM_ITERATIONS = 5). .pour(scene, i, scripted=False) plays a brick to slot i
       .spark(scene, i) plays a RED spark into the net  .exit_label() "exit status 0"
       .keyerror() RED stamp (both not added)   brick(scripted) one Q·A brick
       InstructionCard()  4.2 x 1.6: instruction / context / output; .to_pair(scene) plays it
       into question / answer
    V4 Conveyor(STATIONS[:3], width=12.0)  12.0 x 0.7 (belt at y 0 before moving): station labels
       (STATIONS = instruct-dataset.csv, train.csv, train.jsonl, chat template, tokens); .put(i,
       card) .carry(mob, i) -> anims .light(i) -> anim (cards kept inside the frame)
       splitter(17, 2)  4.6 x 1.6 (input at its left end, not centred): 90/10 fork to train.jsonl ·
       17, test.jsonl · 2   ChatRibbon(rows of (text, is_marker))  <= 12.4 wide (raises): markers
       YELLOW chips, text GREY chips; .tokenize() -> anims (chips -> token cells, no numbers)
       .sweep() -> anim (YELLOW highlighter over every token; FadeOut ribbon.highlighter after)
    V5 MemoryColumn(blocks, total=, total_label=, title=, scale=0.035, labels=True)  base at y 0
       (not centred: move it), blocks bottom to top (name, gb, colour, dtype[, frozen]);
       .restack({name: gb}) -> anims (several blocks at once; labels follow) .shrink(name, gb)
       ladder_column("full"|"lora"|"qlora", labels=True) the lecture's 10 B columns (20+20+80 =
       120 GB; 20 GB base + A,B, outline ~40 GB; NF4 base ~5 GB + A,B, outline ~12 GB; LADDER,
       LADDER_TOTALS)   memory_ladder()  7.8 x 5.1: the three bare columns, 120 -> ~40 -> ~12 GB,
       .cols[kind]   gpu_tiles(5, 24)  dashed 24 GB tiles from y 0 (same scale; + concept_tag())
       For S14's 0.6 B column pass your own blocks and scale (e.g. scale=3.0) + estimate_tag().
    V6 NumberRow(0, 100, step=10)  11.3 x 0.6: .dot(v, text) .snap(dots, values) -> anims
       AbsmaxRow()  11.8 x 3.6: X (FP32) / Int8 (19 … 127, computed, rounded) / back / c rows,
       chip "c = 127 / 10.2 = 12.4509"; .x_cells .q_cells .d_cells .errors((0, 4)) RED rings
       BlockRow()  11.0 x 1.8: bars with one RED outlier; .split() -> anims (separators + absmax
       knobs) .quantize_knobs() -> anims (double quantization)
       NF4Bell()  10.2 x 3.1: .even() -> anims (16 lines) .to_nf4() -> anims (quantile positions)
       .weights(n) -> dots (not added) .snap(dots) -> anims
       inflate_pair()  4.3 x 1.2: .small (NF4) .big (FP16); TransformFromCopy(small, big) and back
    V7 rank_product(5, r)  6.1 x 1.8: 5x5 = 5xr · rx5 with counts   real_size()  7.3 x 3.8: q_proj
       2048 x 1024 vs B 2048 x 8 and A 8 x 1024 (strips drawn at a 0.06 minimum: say so)
       LoraEquation()  6.2 x 0.5: .sym("W0"|"dW"|"W0b"|"alpha"|"r"|"B"|"A") .light(name) -> anim
       LoraBlock(show=None)  7.5 x 4.9: parts x w0 ab notes sum h wires; .forward() -> anims
       .backward() -> anims (YELLOW pulse down, W₀ greys, A and B glow) .merge_into(target) ->
       anims (S16)   LayerTower()  6.8 x 5.1: 28 rows x 7 cells; .light_qv() .count() -> anims;
       .counter.freeze() before it leaves
    V8 CheckpointChain()  10.6 x 2.2: X h₁ h₂ h₃ ŷ + activation-memory meter; .store(i) .drop(i)
       .recompute(src, dst) -> anims   Paging(n=6)  9.0 x 2.6: GPU / CPU boxes, PINK arrows;
       .page_out(k) .page_in() -> anims   BitStrips()  10.8 x 2.5: FP32 / FP16 / BF16, .rows[name]
       .sign .exp .frac, .legend   LossCurve()  7.8 x 4.3 (c75's table): .axes .curve .dots
       .create() -> anim (add recorded_tag())
    S16 ship_cards()  12.3 x 1.0: .adapter (GREEN) .merged (GREY) .endpoint (BLUE)

Capture folder names (assets/terminal): laptop, dataset-creator, gemini-finetuner, expected
(never: capture-only; the scripted stand-in data is read with scripted_text()).
"""

from __future__ import annotations

import json
import re
import subprocess
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
    ArcBetweenPoints,
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
    rush_into,
    smooth,
    squish_rate_func,
)

from explainer import style as S
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
    ReadmeTracker,
    Terminal,
    box,
    browser_window,
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
    form_rows,
    glyph_range,
    label,
    laptop,
    lecture_ref,
    line_bar,
    line_pitch,
    mono,
    mono_line,
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
TERMINAL = ASSETS / "terminal"
SOURCE = ASSETS / "source"
SCRIPTED = TERMINAL / "capture-only" / "scripted"

SPEC = yaml.safe_load((PROJECT / "video.yaml").read_text())
TITLES = {s["cls"]: s["title"] for s in SPEC["scenes"]}
_script = PROJECT / "script.md"
NARRATION = load_narration(_script) if _script.exists() else {}

# ------------------------------------------------------------------ semantic colours (BRIEF.md "Colours")
LAPTOP = S.GREY          # your laptop: ~/AC215, the clone, secrets/, data/ seen from the host, the laptop terminal
CLOUD = S.BLUE           # Google Cloud (global / us-central1 / us), the bucket, the job, the endpoint, the Colab VM + GPU
MODEL = CLOUD            # ... and everything a model writes (the teacher's Q&A pairs, generated answers)
CTR = S.TEAL             # the containers / images llm-dataset-creator and gemini-finetuner: /app, /.venv, the build
SYSTEM = S.ORANGE        # the base image's own Python and apt packages (S04 only)
OWN = S.GREEN            # what you own: uv.lock, your dataset files, the LoRA adapters A and B
DATA = OWN
VENV = OWN
ADAPTER = OWN
TOOL = S.PURPLE          # tools and libraries: Docker, uv, google-genai, bitsandbytes, peft, trl, transformers
ERR = S.RED              # missing-key errors, KeyError, source: not found, quantization error, OOM, wrong physics
TURN = S.YELLOW          # your turn, trackers, look here now; the gradient pulse of the backward pass
PULSE = TURN
COST = S.GOLD            # money; the service-account key glyph (never a value)
KEY = COST
LOOKUP = S.PINK          # bind mounts, gs:// URIs, the three hosts, the endpoint path, GPU <-> CPU paging arrows
FROZEN = S.GREY          # frozen pretrained weights W0 (solid, with a snowflake); persona chip; lecture-only (dashed)
FUTURE = S.GREY          # dashed: lecture-only scale (10 B model, 24 GB tiles), future lectures (L10)
INK = S.WHITE
DIMMED = S.GREY
# bit strips (S14): sign / exponent (range) / fraction (precision) outlines, not semantic colours
BIT_SIGN, BIT_EXP, BIT_FRAC = S.WHITE, S.PINK, S.GREEN

# ------------------------------------------------------------------ names on screen (BRIEF.md "Names")
# The persona is the instructor's first name: masked on screen as the GREY chip ‹instructor›; the
# narration says "the instructor". The full name never appears: the surname is read from the
# never-shown source lines at import (never written here) and every line that goes on screen is
# checked against it.
PERSONA = "‹instructor›"
HF_USER = "‹hf-user›"
PROJECT_NO = "‹instructor-project-number›"
ENDPOINT_ID = "‹endpoint-id›"
MASKS = (PERSONA, HF_USER, PROJECT_NO, ENDPOINT_ID)
MASK = PERSONA
_PERSONA_RE = re.compile(r"pavlos", re.IGNORECASE)
NEVER_SOURCE = {      # file lines never quoted, even masked (they hold the full name)
    "dataset-creator/cli.py": {133, 140},
    "README.md": {118, 119, 167},
}


def _surname_tokens() -> tuple[str, ...]:
    toks = set()
    for name, nums in NEVER_SOURCE.items():
        try:
            rows = (SOURCE / name).read_text(encoding="utf-8").split("\n")
        except OSError:
            continue
        for n in nums:
            if n <= len(rows):
                for m in re.finditer(r"pavlos\s+([A-Za-z]{3,})", rows[n - 1], re.IGNORECASE):
                    toks.add(m.group(1).lower())
    return tuple(sorted(toks))


_NAME_TOKENS = _surname_tokens()
_NAME_RE = re.compile(r"\b(" + "|".join(re.escape(t) for t in _NAME_TOKENS) + r")\b", re.IGNORECASE) \
    if _NAME_TOKENS else None


def guard_names(s: str) -> str:
    """Raise ValueError if s holds the instructor's full name (never on screen)."""
    if _NAME_RE is not None and _NAME_RE.search(s):
        raise ValueError("this line holds a person's full name: it is never shown (BRIEF.md 'Names')")
    return s


def unname(s: str) -> str:
    """The persona name (any case) -> ‹instructor› (drawn GREY by every panel / terminal / card).
    capture(), excerpt(), src_panel(), quote_card() and the cards do it for you. Raises on the full
    name."""
    out = _PERSONA_RE.sub(PERSONA, s)
    guard_names(out)
    return out


def persona_chip(size: float = CAPTION) -> VGroup:
    """The GREY mono chip ‹instructor› (the persona, wherever its name would be)."""
    return _keep(chip(PERSONA, S.GREY, size=size, font=MONO))


def mask_chip(which: str = PERSONA, size: float = CAPTION) -> VGroup:
    """A GREY chip for any mask (PERSONA, HF_USER, PROJECT_NO, ENDPOINT_ID)."""
    return _keep(chip(which, S.GREY, size=size, font=MONO))


# ------------------------------------------------------------------ the running example
USER, HOST = "student", "laptop"
P_HOME = f"{USER}@{HOST}:~$"
P_WS = f"{USER}@{HOST}:~/AC215$"
P_REPO = f"{USER}@{HOST}:~/AC215/llm-finetuning$"
P_DC = f"{USER}@{HOST}:~/AC215/llm-finetuning/dataset-creator$"
P_GF = f"{USER}@{HOST}:~/AC215/llm-finetuning/gemini-finetuner$"
DC_ID = "6f5113cdb660"                        # laptop/07 line 27 (changes every run)
GF_ID = "2a2550dec953"                        # laptop/18 line 27
P_CTR_DC = f"app@{DC_ID}:/app$"
P_CTR_GF = f"app@{GF_ID}:/app$"
P_CTR = P_CTR_DC
CTR_DC_TITLE = "container · llm-dataset-creator"
CTR_GF_TITLE = "container · gemini-finetuner"
CTR_TITLE = CTR_DC_TITLE
LAPTOP_TITLE = "laptop"
SECOND = "laptop · second terminal"
COLAB_TITLE = "QLoRA notebook · Colab"
NOTEBOOK = "QLoRA notebook"
TEACHER = "gemini-3.1-flash-lite"            # dataset-creator/cli.py:17-25 (location="global")
BASE_QWEN = "Qwen/Qwen3-0.6B"
KEY_FILE = "llm-service-account.json"
BUCKET_TEMPLATE = "gs://<your-bucket>"
DATASET_PREFIX = "llm-finetune-dataset-small"
ENDPOINT_REDACTED = f"projects/{PROJECT_NO}/locations/us/endpoints/{ENDPOINT_ID}"
GUIDE = "MLOps_Learning · guides/L08-llm-finetuning.md"
# numbers the scenes draw (each from a capture / the brief; never typed elsewhere)
TRAINABLE = 1_146_880                         # expected/colab-c72
ALL_PARAMS_4BIT = 375_848_960                 # expected/colab-c48
QWEN_LAYERS, HIDDEN, Q_OUT, KV_OUT = 28, 1024, 2048, 1024   # Qwen3-0.6B shapes (c42; digest)
LORA_R, LORA_ALPHA = 8, 16                    # colab/cell-67.py:2,4
ABSMAX_X = (1.5, 2.3, 3.7, 4.1, 5.6, 6.8, 7.9, 8.4, 9.2, 10.2)   # lecture slide 45
NF4_LEVELS = (-1.0, -0.6961928, -0.5250731, -0.39491748, -0.28444138, -0.18477343, -0.09105003, 0.0,
              0.0795803, 0.1609302, 0.2461123, 0.33791524, 0.44070983, 0.562617, 0.72295684, 1.0)

# ------------------------------------------------------------------ layout
BOTTOM = -3.5                    # terminal bottom edge (fixed when it grows or shrinks)
TRACK_LEFT, TRACK_TOP = -6.5, 3.5
TERM_W, TERM_PT = 12.6, 22
TOPCHIP_Y = 2.66                 # a one-line top-band chip: centre y
TOPCHIP_TALL_Y = 2.87            # with a 13-row terminal
CHIP_RIGHT = 6.55

# ------------------------------------------------------------------ README / notebook trackers (script.md "Trackers")
SECTIONS = {
    # dlops-io/llm-finetuning README.md @ 44ef6f0 (head "README") and the course Colab (head "Colab")
    "Prereq": ("README", "Prerequisites", ["Clone repo", "Service account", "Secrets folder", "Edit env.dev"]),
    "DsRun": ("README", "Dataset › Run Container", ["Go to folder", "Run script", "Check key", "Test CLI"]),
    "DsGen": ("README", "Dataset › Generate Text", ["Generate", "System prompt", "Input prompt", "Iterations"]),
    "DsSamples": ("README", "Dataset › Samples", ["Sample answers"]),
    "DsPrep": ("README", "Dataset › Prepare", ["Prepare data", "Gemini format"]),
    "DsUp": ("README", "Dataset › Upload", ["Upload data"]),
    "FtRun": ("README", "Fine-tune › Run Container", ["Go to folder", "Run script", "Test CLI"]),
    "FtModel": ("README", "Fine-tune › Fine-tune Model", ["Start tuning", "Watch console"]),
    "FtCost": ("README", "Fine-tune › Cost", ["Read costs"]),
    "FtChat": ("README", "Fine-tune › Chat", ["Paste endpoint", "Chat", "Hosted demo", "Training monitor"]),
    "ColabA": ("Colab", "Part A · Setup", ["Copy notebook", "GPU runtime", "§3 Install", "§4 HF token",
                                          "§5 Imports, Drive", "§6 Download"]),
    "ColabB": ("Colab", "Part B · 4-bit", ["Load OPT", "§1 Verify", "§2 Generate"]),
    "Qwen": ("Colab", "Step 1–2 · Qwen", ["1.3 Load", "2.1 Params", "2.2 Config", "2.3 Baseline", "2.4 Trainable"]),
    "Data": ("Colab", "Step 3 · Dataset", ["3.1 Download", "3.2 Sample", "3.5 Template", "3.6 Split", "3.7 Verify"]),
    "Tune": ("Colab", "Step 4 · Fine-tune", ["4.1 LoRA config", "4.2 Train args", "4.3 Trainer", "4.4 Train",
                                             "4.5 TensorBoard"]),
    "Eval": ("Colab", "Step 5 · Evaluate", ["5.1 Loss table", "5.2 Side by side"]),
    "Save": ("Colab", "Step 6 · Save", ["6.1 Adapters", "6.2 Merge", "6.3 Push"]),
    # not in the README: every step is an extra (the section name says so)
    "Down": ("README", "Teardown · extra", ["Exit", "Remove images", "Cloud cleanup", "Colab runtime"]),
}
# steps the README does not have: tracker(key, k) then caption_extra(tr) while they are on screen
EXTRA_STEPS = {("Prereq", 1), ("Prereq", 4), ("FtChat", 1)}


def lref(slides: str) -> VGroup:
    """The GREY "Lecture 8 · slides 7–8" tag, top right (lecture_ref(8, slides))."""
    return lecture_ref(8, slides)


# ------------------------------------------------------------------ captures: folders and guards
FOLDERS = ("laptop", "dataset-creator", "gemini-finetuner", "expected")
NEVER_FILES = {"laptop/07-docker-shell-dataset-creator.plain.txt",      # the build logs: proxy / CA lines
               "laptop/18-docker-shell-gemini-finetuner.plain.txt"}
NEVER_CAPTURE = {   # file lines the script never shows (BRIEF.md "Things never to do")
    "laptop/09-x-docker-images.txt": {4},             # the capture's rebuilt python:3.12-slim-bookworm base
    "laptop/19-x-docker-images.txt": {5},
}
CUT_OK: dict = {}
# a world-writable mode column (rw-rw-rw- / drwxrwxrwx) is a capture-laptop artefact: such an `ls -la`
# line prints only through Capture.names_sizes(n) (size and name columns)
_WORLD_W = re.compile(r"^[dl-]rw[xsS-]rw[xsS-]rw[xtT-]\s")
_LS_ROW = re.compile(r"^[dlcbps-][rwxsStT-]{9}[.+@]?\s+\d+\s+\S+\s+\S+\s+(\d+)\s+\w{3}\s+\d+\s+[\d:]+\s+(.*)$")


def _colab_cmd_lines(fname: str) -> int | None:
    """expected/colab-cNN-…: the number of `$`/continuation lines = the cell's source line count."""
    m = re.match(r"colab-c(\d+)", fname)
    if not m:
        return None
    hits = sorted((SOURCE / "colab").glob(f"cell-{int(m.group(1)):02d}.*"))
    if not hits:
        return None
    return len(hits[0].read_text(encoding="utf-8").rstrip("\n").split("\n"))


# ------------------------------------------------------------------ the Colab's own section numbers
def _colab_sections() -> dict[int, str]:
    """Cell index -> the notebook's own heading number in force at that cell ("3", "1.3", "4.2";
    in Part B "Part B · 1"), read from the markdown cells in order."""
    out: dict[int, str] = {}
    part, cur = "", ""
    head = re.compile(r"^#+\s*(?:<font[^>]*>)?\s*\**\s*(?:Step\s+)?(\d+(?:\.\d+)?)[.:]?\s")
    for k in range(0, 100):
        hits = sorted((SOURCE / "colab").glob(f"cell-{k:02d}.*"))
        if not hits:
            continue
        p = hits[0]
        if p.suffix == ".md":
            for ln in p.read_text(encoding="utf-8").split("\n"):
                if re.match(r"^#\s", ln) and "Part B" in ln:
                    part, cur = "B", ""
                elif re.match(r"^#\s", ln) and ("Part C" in ln or "Part A" in ln):
                    part, cur = "", ""
                m = head.match(ln)
                if m:
                    cur = m.group(1)
        out[k] = (f"Part B · {cur}" if cur else "Part B") if part == "B" else cur
    return out


COLAB_SECTION = _colab_sections()


def colab_where(cell: int) -> str:
    """"QLoRA notebook · 4.2 · cell 70" (the notebook's heading number, then our 0-based index)."""
    sec = COLAB_SECTION.get(cell, "")
    return f"{NOTEBOOK} · {sec} · cell {cell}" if sec else f"{NOTEBOOK} · cell {cell}"


# ------------------------------------------------------------------ sources
def src_path(name: str) -> str:
    """Resolve a source name under assets/source (the repo's own relative paths; Colab cells as
    "colab/cell-NN.py|.md"; "gemini-finetuner/cli.py" means the redacted copy). Raises for files
    never shown (Colab cell 0)."""
    if name == "gemini-finetuner/cli.py":
        name = "gemini-finetuner/cli.redacted.py"
    if not (SOURCE / name).is_file():
        raise FileNotFoundError(f"assets/source/{name} not found")
    if re.match(r"colab/cell-00\b", name):
        raise ValueError(f"{name}: the Colab's cell 0 (the course header) is never shown")
    return name


def source_text(name: str) -> str:
    """A tutorial file, the persona masked (never-shown lines are refused line by line by
    excerpt / src_panel; do not print source_text() whole)."""
    return _PERSONA_RE.sub(PERSONA, (SOURCE / src_path(name)).read_text(encoding="utf-8"))


def _source_lines(name: str, nums, strip_emoji_: bool = False) -> dict[int, str]:
    path = src_path(name)
    lines = source_text(name).split("\n")
    bad = NEVER_SOURCE.get(path, set()) & set(nums)
    if bad:
        raise ValueError(f"{path}: lines {sorted(bad)} are never shown (they hold the full name)")
    out = {}
    for n in nums:
        if not 1 <= n <= len(lines):
            raise IndexError(f"{path} has {len(lines)} lines (asked for {n})")
        s = lines[n - 1].expandtabs(4)
        guard_names(s)
        out[n] = _emoji_guard(s, f"{path} line {n}", strip_emoji_)
    return out


def shown_path(name: str) -> str:
    """The path as the viewer sees it: the repo's own relative path; cli.redacted.py ->
    "gemini-finetuner/cli.py"; a Colab cell "colab/cell-70.py" -> "QLoRA notebook · 4.2 · cell 70"."""
    p = src_path(name)
    m = re.match(r"colab/cell-(\d+)", p)
    if m:
        return colab_where(int(m.group(1)))
    return p.replace("cli.redacted.py", "cli.py")


def scripted_text(name: str) -> list[str]:
    """The hand-written stand-in data (capture-only/scripted/cheese_qa_N.txt) as lines, for a panel
    tagged `scripted` (BLUE dashed seat). name: "cheese_qa_0" or "cheese_qa_0.txt"."""
    p = SCRIPTED / (name if name.endswith(".txt") else f"{name}.txt")
    return [unname(s) for s in p.read_text(encoding="utf-8").rstrip("\n").split("\n")]


def scripted_pairs() -> list[dict]:
    """All 20 scripted {question, answer} pairs, in file order (cheese_qa_0 … _4)."""
    out = []
    for k in range(5):
        out += json.loads("\n".join(scripted_text(f"cheese_qa_{k}")))
    return out


def capture(name: str, folder: str | None = None) -> Capture:
    """assets/terminal/<folder>/<name>.txt parsed, the persona masked; capture("05", "dataset-creator")
    finds 05-generate.txt; capture("dataset-creator/05") works too; expected files by name:
    capture("expected/colab-c75-train"), capture("expected/readme-cost-table"). Folders: laptop,
    dataset-creator, gemini-finetuner, expected (never capture-only). Fails loudly if missing."""
    if folder is None:
        folder, _, name = name.rpartition("/")
        if not folder:
            raise ValueError("capture(name, folder): name the folder")
    if folder.startswith("capture-only"):
        raise ValueError("capture-only/ is plumbing: never shown (scripted data: scripted_text())")
    if folder not in FOLDERS:
        raise ValueError(f"unknown capture folder {folder!r} (folders: {FOLDERS})")
    p = _find_capture(name, folder)
    key = f"{folder}/{p.name}"
    if key in NEVER_FILES:
        raise ValueError(f"{key} is never shown (BRIEF.md 'Things never to do')")
    cmd, raw, code, off, header = _load_capture(folder, p.name)
    return Capture(key, cmd, list(raw), code, off, header)


def _load_capture(folder: str, fname: str) -> tuple:
    """(cmd, output lines, exit code, file line number of the first output line, '#' header).
    expected/colab-cNN files: the cell's source lines follow the `$ ` (as many as the cell has) and
    are the cmd (joined by newlines), never output."""
    return _load_capture_cached(folder, fname)


@lru_cache(maxsize=None)
def _load_capture_cached(folder: str, fname: str) -> tuple:
    p = TERMINAL / folder / fname
    text = p.read_bytes().decode("utf-8")
    raw = [unname(ln.rstrip("\r").split("\r")[-1].expandtabs(8)) for ln in text.rstrip("\n").split("\n")]
    header = ""
    if raw and raw[0].startswith("# "):
        header, raw = raw[0], raw[1:]
    off = 2 if header else 1
    cmd = ""
    if raw and raw[0].startswith("$ "):
        n = _colab_cmd_lines(fname) if folder == "expected" else None
        n = n or 1
        cmd = "\n".join([raw[0][2:]] + [r[2:] for r in raw[1:n]])
        raw, off = raw[n:], off + n
    code = 0
    if raw and re.fullmatch(r"\[exit -?\d+\]", raw[-1]):
        code = int(raw[-1][6:-1])
        raw = raw[:-1]
    return cmd, tuple(raw), code, off, header


def expected_where(name: str) -> str:
    """The README lines an expected/readme-… file quotes, from its '#' header: "README.md · lines
    288–301"."""
    c = capture(name if "/" in name else f"expected/{name}")
    m = re.search(r"README\.md:(\d+)(?:-(\d+))?", c.header)
    if not m:
        raise ValueError(f"{c.name}: no README lines in its header")
    a, b = m.group(1), m.group(2)
    return f"README.md · line {a}" if not b or a == b else f"README.md · lines {a}–{b}"


# ------------------------------------------------------------------ emoji of the Colab outputs
EMOJI = frozenset("📊📝🔵🟢✅✓❌⚠🧀🤖" + chr(0xFE0F))
# a captured line's leading emoji becomes its colour: 🔵 Base Model GREY, 🟢 Fine-Tuned GREEN
EMOJI_COLORS = (("❌", ERR), ("⚠", ERR), ("🟢", OWN), ("✅", OWN), ("🔵", S.GREY))


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


def emoji_color(raw: str, default: str = OUTPUT) -> str:
    """The colour a captured line prints in, from the emoji it starts with: ❌ / ⚠️ RED, ✅ GREEN,
    🤖 (a model call) BLUE, anything else `default` (output grey)."""
    head = raw.lstrip()
    for e, col in EMOJI_COLORS:
        if head.startswith(e):
            return col
    return default


def _looks_code(s: str) -> bool:
    return " " not in s and bool(re.search(r"[-_.]", s))


def place_tracker(tr):
    tr.shift(np.array([TRACK_LEFT - tr.get_left()[0], TRACK_TOP - tr.get_top()[1], 0]))
    return tr


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


def _swap_caption(tr, new, steady: bool) -> list:
    """Cross-fade tr's caption into the Text `new`, in place next to tr.dots, and make `new`
    tr.caption at once (it takes the old caption's slot in tr; the old one leaves tr after its
    FadeOut takes it off the scene for good; built early, the swap shows the old caption until it
    plays: _stage_swap). Ported from L05: a Transform between two captions of
    different lengths scrambled the letters for 0.3-0.6 s (QA: "its caption morphs glyph by
    glyph"). steady=True (the same step, ' · extra' on or off): the new caption, its shared
    'step k of N: …' exactly on the old glyphs, fades in over the first half, then the old one
    fades out, so the shared text never dims. steady=False (another step): the old one fades out,
    then the new one in, with a short gap. Returns the two animations (the caller wraps them)."""
    old = tr.caption
    inked = any(m.has_points() for m in old.get_family())
    new.next_to(tr.dots, RIGHT, buff=0.25)
    if steady and inked:
        new.align_to(old, LEFT)          # the shared prefix exactly on the old one's glyphs
    _stage_swap(tr, old, new)
    tr.caption = new
    if not inked:                        # from the blank caption: the label fades in where it stays
        return [_SwapOut(old, tr), _SwapIn(new)]
    if steady:
        return [_SwapIn(new, rate_func=_in_first_half), _SwapOut(old, tr, rate_func=_out_second_half)]
    return [_SwapOut(old, tr, rate_func=_out_early), _SwapIn(new, rate_func=_in_late)]


class CrossFadeTracker(ReadmeTracker):
    """explainer.devops.ReadmeTracker whose goto(k) cross-fades the caption in place (see
    _swap_caption) instead of Transforming it; the dots move as before. Same contract: goto
    returns one AnimationGroup (run_time 0.5 by default); tr.k, tr.caption (the new Text right
    after the call), tr.dots, tr._caption(k) as before."""

    def goto(self, k: int, run_time: float = 0.5):
        anims = []
        for i, d in enumerate(self.dots, start=1):
            col = self.hi_color if i == k else (S.GREY if i < k else S.GREY_DARK)
            anims.append(d.animate.set_color(col).scale((1.5 if i == k else 1.0) / (d.width / 0.12)))
        anims += _swap_caption(self, self._caption(k), steady=(k == self.k))
        self.k = k
        return AnimationGroup(*anims, run_time=run_time)


def tracker(key: str, step: int | None = None):
    """The tracker for `key` (see SECTIONS), top-left: "<source> › <section>", one dot per step,
    "step k of N: <title>" (step None: no step lit yet, an empty caption). A CrossFadeTracker:
    goto() and caption_extra() swap the caption in place (old out, then new in)."""
    src, section, steps = SECTIONS[key]
    t = CrossFadeTracker(section, steps)
    head = t.head
    new_src = mono(src, t.size, S.GREY) if _looks_code(src) else label(src, t.size, S.GREY)
    new_sec = mono(section, t.size, INK) if _looks_code(section) else label(section, t.size, INK)
    left = head.get_left()
    head.submobjects[0] = new_src
    head.submobjects[2] = new_sec
    head.arrange(RIGHT, buff=0.12)
    head.shift(left - head.get_left())
    if step:
        t.set_step(step)
    t.key = key
    return place_tracker(t)


def caption_extra(tr, on: bool = True):
    """The tracker caption with (or without) ' · extra' while a command the README doesn't have
    is on screen: one AnimationGroup that cross-fades the caption in place (the shared 'step k of
    N: …' stays put and never dims; see _swap_caption) and makes the new Text tr.caption at once.
    .target_mobject is the new caption, placed (as the Transform this returned before: S07 and
    S09 measure it)."""
    k = tr.k
    s = f"step {k} of {len(tr.steps)}: {tr.steps[k - 1]}" if k else ""
    if on:
        new = label((s + " · extra") if s else "extra", tr.size, tr.hi_color,
                    t2c={"· extra": S.GREY, "extra": S.GREY} if not s else {"· extra": S.GREY})
    else:
        new = label(s or " ", tr.size, tr.hi_color)
    g = AnimationGroup(*_swap_caption(tr, new, steady=True))
    g.target_mobject = new
    return g


def switch_section(scene, old, key: str, step: int | None = 1, run_time: float = 0.8):
    """The tracker switches to another section: the old one lifts away, then the new one drops in
    (as lref_swap), in the same run_time, one half each. Returns the new tracker (on screen). old
    may be None. Faded at once, both headers read together mid-swap (L05 final review)."""
    new = tracker(key, step)
    if old is None:
        scene.play(FadeIn(new, shift=DOWN * 0.25), run_time=run_time)
    else:
        scene.play(Succession(FadeOut(old, shift=UP * 0.25), FadeIn(new, shift=DOWN * 0.25)),
                   run_time=run_time)
    return new


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


class Capture:
    """One captured command. .cmd (as typed, without "$ "), .lines (its output, IDs masked; emoji
    kept: the line methods strip them), .exit (status), .first (file line number of .lines[0]),
    .header (the '#' provenance line of expected/*)."""

    def __init__(self, name: str, cmd: str, lines: list[str], exit_code: int, first: int = 2,
                 header: str = ""):
        self.name, self.cmd, self.lines, self.exit = name, cmd, lines, exit_code
        self.first, self.header = first, header

    def _guard(self, n: int):
        if n in NEVER_CAPTURE.get(self.name, ()):
            raise ValueError(f"{self.name}: line {n} is never shown (BRIEF.md 'Things never to do')")
        if _WORLD_W.match(self._raw(n)):
            raise ValueError(f"{self.name}: line {n} has the capture laptop's world-writable modes: "
                             "print it with .names_sizes(n) (script.md 'names+sizes')")

    def _raw(self, n: int) -> str:
        i = n - self.first
        if not 0 <= i < len(self.lines):
            raise IndexError(f"{self.name}: line {n} is not output (output is lines "
                             f"{self.first}–{self.first + len(self.lines) - 1})")
        return self.lines[i]

    def line(self, n: int, strip_emoji: bool = True) -> str:
        """File line n (1-based, as in the script's TERM(file: n)), emoji removed."""
        self._guard(n)
        return _emoji_guard(self._raw(n), f"{self.name} line {n}", strip_emoji)

    def color(self, n: int, default: str = OUTPUT) -> str:
        """The colour line n prints in (its leading emoji: ❌ ⚠️ RED, ✅ GREEN, 🤖 BLUE)."""
        return emoji_color(self._raw(n), default)

    def out(self, *spec, default: str = OUTPUT) -> list:
        """Lines ready for t.print(...): [(text, colour)], emoji stripped and coloured by their
        emoji. spec as in at(): file line numbers, (a, b) ranges, "…" (or "") an ellipsis row; a
        str of your own (cut/fold/as401 results) or a (text, colour) pair passes through."""
        res = []
        for s in spec:
            if isinstance(s, int):
                res.append((self.line(s), self.color(s, default)))
            elif isinstance(s, str):
                res.append((s or "…", S.GREY if s in ("", "…") else default))
            elif isinstance(s[0], str):
                res.append((s[0], s[1]))
            else:
                res += [(self.line(n), self.color(n, default)) for n in range(s[0], s[1] + 1)]
        return res

    def cut(self, n: int, marker: str, ellipsis: bool = True, strip_emoji: bool = True) -> str:
        """File line n up to and including the first `marker`, then " …" (script: 'N cut after
        "x"'; the '…' prints GREY). ellipsis=False: no ' …'."""
        ok = CUT_OK.get((self.name, n))
        if ok is None:
            self._guard(n)
        elif ok != marker:
            raise ValueError(f"{self.name}: line {n} may only be cut after {ok!r}")
        s = self._raw(n)
        i = s.find(marker)
        if i < 0:
            raise ValueError(f"{marker!r} not in {self.name} line {n}")
        out = s[:i + len(marker)]
        if ellipsis and out.rstrip() != s.rstrip():
            out = out + " …"
        return _emoji_guard(out, f"{self.name} line {n}", strip_emoji)

    def cut_before(self, n: int, marker: str) -> str:
        """File line n up to (not including) `marker`, no ellipsis (laptop/07 line 27: the prompt,
        cut before ' exit')."""
        self._guard(n)
        s = self._raw(n)
        i = s.find(marker)
        if i < 0:
            raise ValueError(f"{marker!r} not in {self.name} line {n}")
        return strip_emoji(s[:i])


    def names_sizes(self, *ns) -> list[str]:
        """`ls -la` lines as "size  name" (the size and name columns joined by two spaces; script.md
        'names+sizes'): the mode / owner / date columns never print. ns: FILE line numbers or (a, b)."""
        out = []
        for s in ns:
            for n in ([s] if isinstance(s, int) else range(s[0], s[1] + 1)):
                if n in NEVER_CAPTURE.get(self.name, ()):
                    raise ValueError(f"{self.name}: line {n} is never shown")
                m = _LS_ROW.match(self._raw(n))
                if not m:
                    raise ValueError(f"{self.name}: line {n} is not an ls -la row: {self._raw(n)!r}")
                out.append(f"{m.group(1)}  {m.group(2)}")
        return out

    def squeeze(self, n: int) -> str:
        """Line n with every run of 3+ spaces collapsed to two (BuildKit pads its rows for an
        80-column terminal: laptop/07, laptop/12; whitespace only)."""
        return re.sub(r" {3,}", "  ", self.line(n))

    def at(self, *spec, ellipsis: str = "…", strip_emoji: bool = True) -> list[str]:
        """Output lines by FILE line number: at(2, (11, 12), "…", 52) -> line 2, lines 11-12, a
        '…' line, line 52. A string is inserted as is ("" means the ellipsis)."""
        res: list[str] = []
        for s in spec:
            if isinstance(s, str):
                res.append(s or ellipsis)
            elif isinstance(s, int):
                res.append(self.line(s, strip_emoji))
            else:
                a, b = s
                res += [self.line(k, strip_emoji) for k in range(a, b + 1)]
        return res

    def join(self, *ns: int, width: int | None = 80) -> str:
        """File lines joined into one (one output line the capture shows over several rows: laptop/12
        lines 2-3, wrapped at 80 columns). A row the terminal wrapped at `width` columns is padded
        back to `width` first; a row whose successor starts with spaces joins with one space.
        width=None: plain concatenation."""
        rows = [self.line(k) for k in ns]
        if not width:
            return "".join(rows)
        res = rows[0]
        for nxt in rows[1:]:
            if nxt.startswith(" "):
                res = res.rstrip() + " " + nxt.lstrip()
            else:
                tail = len(res) - res.rfind("\n") - 1 if "\n" in res else len(res)
                res = res + " " * max(0, (width - tail % width) % width if tail % width else 0) + nxt
        return res

    def split_at(self, n: int, col: int) -> list[str]:
        """Line n as two rows: [:col] and [col:] (laptop/08 lines 2-3 at column 56, a column
        boundary of `docker ps`: the table reads as two stacked halves). Trailing spaces trimmed."""
        s = self.line(n)
        return [s[:col].rstrip(), s[col:].rstrip()]

    def fold(self, a: int, b: int, text: str) -> str:
        """The script's "a–b folded to X": X stands for lines a..b and is made of their own text,
        with '…' for what it leaves out. Checks every piece between the '…'s against the lines
        (joined with spaces, whitespace normalised), in order, and returns X."""
        norm = lambda s: re.sub(r"\s+", " ", s).strip()     # noqa: E731
        whole = norm(" ".join(self.line(k) for k in range(a, b + 1)))
        pos = 0
        for frag in text.split("…"):
            f = norm(frag)
            if not f:
                continue
            i = whole.find(f, pos)
            if i < 0:
                raise ValueError(f"{self.name} {a}-{b}: {f!r} is not their text (after position {pos})")
            pos = i + len(f)
        return text

    def typed(self, n: int) -> str:
        """The command typed on prompt line n ('app@…:/app$ exit' -> 'exit')."""
        sp = split_prompt(self.line(n))
        if sp is None:
            raise ValueError(f"{self.name}: line {n} is not a prompt line: {self.line(n)!r}")
        return sp[1]

    def pick(self, *ranges, ellipsis: str = "…") -> list[str]:
        """L1-compatible: output lines by 1-based inclusive ranges of .lines (pick index = file
        line - 1 for a normal capture). Prefer .at() / .out(), which take file line numbers."""
        n = len(self.lines)
        res: list[str] = []
        last = None
        for r in ranges:
            a, b = (r, r) if isinstance(r, int) else r
            a = a if a > 0 else n + a + 1
            b = b if b > 0 else n + b + 1
            if last is not None and a > last + 1:
                res.append(ellipsis)
            res += [self.line(k - 1 + self.first) for k in range(a, b + 1)]
            last = b
        return res


def _find_capture(name: str, folder: str) -> Path:
    d = TERMINAL / folder
    p = d / (name if name.endswith(".txt") else f"{name}.txt")
    if p.exists():
        return p
    hits = sorted(q for q in d.glob(f"{name}-*.txt") if ".plain" not in q.name)
    if len(hits) == 1:
        return hits[0]
    if not hits:
        raise FileNotFoundError(f"capture {folder}/{name} is missing (see ASSETS.md)")
    raise FileNotFoundError(f"capture {folder}/{name} is ambiguous: {[h.name for h in hits]}")


_PROMPT = re.compile(r"^((?:\(\w+\) )?[\w.-]+@[\w.-]+:[^\s$#]*[$#])(?: (.*))?$")


_PROMPT_ANY = re.compile(r"((?:\(\w+\) )?[\w.-]+@[\w.-]+:[^\s$#]*[$#])(?: (.*))?$")


def split_prompt(line: str):
    """'app@13a6188396ca:/app$ exit' -> ('app@13a6188396ca:/app$', 'exit'); not a prompt -> None."""
    m = _PROMPT.match(line.rstrip())
    if not m:
        return None
    return m.group(1), (m.group(2) or "").strip()


def split_prompt_inside(line: str):
    """A line where a prompt follows other text (laptop/12 line 11: 'OpenAI API key: app@…:/app$
    export OPENAI_API_KEY') -> (before, prompt, cmd); None when no prompt follows text."""
    m = _PROMPT_ANY.search(line.rstrip())
    if not m or m.start() == 0:
        return None
    return line[:m.start()], m.group(1), (m.group(2) or "").strip()


def cell_title(name: str) -> str | None:
    """A Colab cell's '# @title …' (the GREY subtitle of its panel), or None."""
    first = source_text(name).split("\n", 1)[0]
    m = re.match(r"#\s*@title\s+(.*)", first)
    return m.group(1).strip() if m else None


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


def readme(a: int, b: int | None = None) -> list[str]:
    """README.md lines a..b (1-based, inclusive) as a list, stripped of Markdown list/quote marks
    only where they lead ('- ', '> '): the words of a QUOTE card. b=None: one line."""
    rows = excerpt("README.md", a, a if b is None else b).split("\n")
    return [re.sub(r"^\s*(?:[-*>]\s+)", "", r).rstrip() for r in rows]


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


def item_rows(printed, k: int) -> list:
    """The rows that _L8Terminal.print printed for item k of its `lines` (one row, or the rows a
    wrap=True line folded into), in order."""
    rows = [r for r in printed if getattr(r, "src_item", None) == k]
    if not rows:
        raise IndexError(f"no printed rows for item {k}")
    return rows


def _src_find(rows, sub: str, occurrence: int = 0) -> tuple[int, int]:
    full = rows[0].src
    i = -1
    for _ in range(occurrence + 1):
        i = full.find(sub, i + 1)
    if i < 0:
        raise ValueError(f"{sub!r} not in {full!r}")
    return i, i + len(sub)


def wrapped_glyphs(rows, sub: str, occurrence: int = 0) -> VGroup:
    """The glyphs of `sub` in ONE printed line, across the rows it folded into (rows: that line's
    rows, e.g. item_rows(printed, k), or the whole return of a one-line print)."""
    i, j = _src_find(rows, sub, occurrence)
    out = VGroup()
    for r in rows:
        a, b = r.src_span
        lo, hi = max(i, a), min(j, b)
        if lo < hi:
            out.add(*glyph_range(r, lo - a + r.src_indent, hi - a + r.src_indent))
    return out


def wrapped_at(rows, sub: str, occurrence: int = 0):
    """(row, column) of `sub` in ONE printed line: the row that holds all of it and the column it
    starts at in that row's text (for col_box / glyph_range). Raises if the fold split it."""
    i, j = _src_find(rows, sub, occurrence)
    for r in rows:
        a, b = r.src_span
        if a <= i and j <= b:
            return r, i - a + r.src_indent
    raise ValueError(f"{sub!r} is split across rows: {[r.text for r in rows]}")


class _L8Terminal(Terminal):
    """The house Terminal; every line it places has the masks and '…' drawn GREY; print(wrap=True)
    folds at word boundaries (wrap_output); scrolling never crosses the title bar (_make_room)."""

    def _place(self, line, i):
        super()._place(line, i)
        grey_masks(line)
        return line

    def _make_room(self, scene, n_new: int, run_time: float = 0.35) -> None:
        """Terminal._make_room with the same signature, run_time and end state. explainer/devops.py
        fades the scrolled-off lines out WHILE shifting them up a row, so for 2-5 frames they
        cross the title bar and the top border (L05 final review). Here they fade out in place in
        the first 40% of the same single play, then the staying lines shift up (ported from L05's
        _l05_make_room): nothing crosses the top border, no row is drawn over a fading one."""
        overflow = len(self.lines) + n_new - self.rows
        if overflow <= 0:
            return
        gone = VGroup(*self.lines.submobjects[:overflow])
        stay = VGroup(*self.lines.submobjects[overflow:])
        split = 0.4 if len(stay) else 1.0
        anims = [FadeOut(gone, rate_func=squish_rate_func(smooth, 0.0, split))]
        if len(stay):
            anims.append(stay.animate(rate_func=squish_rate_func(smooth, split, 1.0))
                         .shift(UP * self.pitch * overflow))
        scene.play(*anims, run_time=run_time)
        for m in gone:
            self.lines.remove(m)

    def print(self, scene, lines, color: str = OUTPUT, run_time: float = 0.5, wrap: bool = False,
              lag: float = 0.15) -> VGroup:
        """Terminal.print (same arguments, one play, returns the new rows), but wrap=True folds a
        long line with wrap_output (at a space or after , / _ - . within reach of the column, a
        hanging indent on continuation rows) instead of at the fixed column. Every row carries
        .src (its line's full text), .src_item (the line's index in `lines`), .src_span (a, b) and
        .src_indent: item_rows / wrapped_glyphs / wrapped_at find text across folded rows."""
        items = []
        for k, x in enumerate([lines] if isinstance(lines, (str, tuple)) else lines):
            s, col = (x, color) if isinstance(x, str) else x
            if wrap and len(s) > self.max_chars:
                items += [(row, col, k, s, a, b, ind) for row, a, b, ind in wrap_output(s, self.max_chars)]
            else:
                c = self._cut(s)
                items.append((c, col, k, s, 0, len(c) if c == s else len(c) - 1, 0))
        if not items:
            return VGroup()
        self._make_room(scene, len(items))
        new = VGroup()
        for row, col, k, s, a, b, ind in items:
            ln = mono_line(row, self.size, col)
            self._place(ln, len(self.lines))
            ln.src, ln.src_item, ln.src_span, ln.src_indent = s, k, (a, b), ind
            self.lines.add(ln)
            new.add(ln)
        scene.play(LaggedStart(*[FadeIn(m) for m in new], lag_ratio=lag), run_time=run_time)
        return new


def strip_top(rows: int = 3) -> float:
    """y of the top edge of a `rows`-row house terminal sitting on BOTTOM."""
    return BOTTOM + Terminal(rows=rows, width=TERM_W, size=TERM_PT, title="x").box.height


def _strip_top_at_import(rows: int = 3, tries: int = 4) -> float:
    """strip_top() at import time, retried: Manim's text cache can race when several scenes
    import this module at once (FileNotFoundError on a shared .svg)."""
    import time
    for k in range(tries):
        try:
            return strip_top(rows)
        except FileNotFoundError:
            if k == tries - 1:
                raise
            time.sleep(0.3 * (k + 1))
    raise RuntimeError("unreachable")


STRIP_TOP = _strip_top_at_import(3)


def _swap_title(t: Terminal, new) -> list:
    """The terminal's title text swaps in place, old out then new in (_swap_text); t.title is the
    new Text afterwards (a Transform between the two titles scrambled the letters)."""
    old = t.title
    t.title = new
    return _swap_text(t, old, new)


def retitle(t: Terminal, title: str, color: str = S.GREY) -> AnimationGroup:
    """Animation: the terminal's title text changes (old out, then new in)."""
    return AnimationGroup(*_swap_title(t, mono(title, CAPTION, color).move_to(t.title)))


def resize(scene, t: Terminal, rows: int, keep=None, run_time: float = 0.8, extra=(),
           anchor: str = "bottom") -> Terminal:
    """Grow or shrink the terminal to `rows` (bottom edge fixed; anchor="top" keeps the top edge).
    It keeps its last lines (at most `keep` of them), or, when `keep` is a list of line mobjects,
    exactly those lines. The frame keeps its colour (TEAL inside the container)."""
    ref = Terminal(prompt=t.prompt, width=t.box.width, rows=rows, size=t.size, title="x")
    dy = (t.box.get_top()[1] - ref.box.get_top()[1]) if anchor == "top" else \
        (t.box.get_bottom()[1] - ref.box.get_bottom()[1])
    ref.shift(np.array([t.box.get_center()[0] - ref.box.get_center()[0], dy, 0]))
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


def _drop_bare(scene, t: Terminal):
    if len(t.lines) and getattr(t.lines[-1], "bare", False):
        last = t.lines[-1]
        scene.remove(last, *last.submobjects)
        t.lines.remove(last)


def _space_levels(text: str) -> dict[int, int]:
    """For every space of a shell line: 0 outside quotes, 1 inside a "double-quoted" string but
    outside any inner '...' literal, 2 anywhere else (a '...' string)."""
    out, outer, inner = {}, None, None
    for i, ch in enumerate(text):
        if outer is None:
            if ch in "\"'":
                outer = ch
            elif ch == " ":
                out[i] = 0
        elif outer == "'":
            if ch == "'":
                outer = None
            elif ch == " ":
                out[i] = 2
        elif inner:
            if ch == inner:
                inner = None
            elif ch == " ":
                out[i] = 2
        elif ch == "'":
            inner = ch
        elif ch == '"' and text[i - 1] != "\\":
            outer = None
        elif ch == " ":
            out[i] = 1
    return out


def fold_cmd(text: str, limit: int = 65, first_prefix: int = 0) -> tuple[list[str], bool]:
    """Fold a typed line (prompt included) into rows of at most `limit` characters (" \\" at the
    end of a row, the next row indented 4), quote-aware: it breaks at the last space outside
    quotes that fits (before an option when one is in the row's last quarter), else at a space
    inside a "double-quoted" shell string outside any inner '...' literal, else inside a '...'
    string, and only with no space in reach mid-token (hard = True). Returns (rows, hard)."""
    if len(text) <= limit:
        return [text], False
    levels = _space_levels(text)
    rows, pos, prefix, hard = [], 0, "", False
    while len(prefix) + len(text) - pos > limit:
        room = limit - 2 - len(prefix)               # characters of text on this row
        lo_start = first_prefix if not rows else pos
        cand = [j for j in levels if lo_start < j <= pos + room]
        ok = [j for j in cand if levels[j] == 0]
        opt = [j for j in ok if j + 1 < len(text) and text[j + 1] == "-"]
        if opt and opt[-1] >= pos + room * 0.75:
            ok = opt
        for lv in (1, 2):
            if not ok:
                ok = [j for j in cand if levels[j] == lv]
        j = ok[-1] if ok else None
        if j is not None and j - pos < room * 0.4 and len(text) - j + 3 > limit and \
                not [k for k in levels if j + 1 < k <= j + 1 + limit - 6]:
            j = None          # a near-empty row before a token that must break anyway: fill it
        if j is not None:
            rows.append(prefix + text[pos:j] + " \\")
            pos = j + 1
        else:
            hard = True
            rows.append(prefix + text[pos:pos + room] + " \\")
            pos += room
        prefix = "    "
    rows.append(prefix + text[pos:])
    return rows, hard


def _type_rows(scene, t: Terminal, texts: list[str], n_prompt: int, type_time: float | None,
               n_typed: int):
    """Add the rows `texts` (row 0 starts with the prompt: its first n_prompt characters are not
    typed) and type the rest, as Terminal.type does. Returns the line or a VGroup with .rows."""
    t._make_room(scene, len(texts))
    rows = []
    for k, s in enumerate(texts):
        ln = mono_line(s, t.size, INK, t2c=t._prompt_colors(t.prompt) if k == 0 else None)
        t._place(ln, len(t.lines))
        t.lines.add(ln)
        rows.append(ln)
    scene.add(glyph_range(rows[0], 0, n_prompt))
    typed = VGroup(*[g for g in glyph_range(rows[0], n_prompt)] +
                   [g for r in rows[1:] for g in glyph_range(r, 0)])
    if len(typed):
        from manim import ShowIncreasingSubsets
        rt = type_time if type_time is not None else min(2.4, max(0.4, 0.045 * n_typed))
        scene.play(ShowIncreasingSubsets(typed, rate_func=linear), run_time=rt)
    for r in rows:
        scene.add(r)
    if len(rows) == 1:
        return rows[0]
    g = VGroup(*rows)
    g.rows, g.text = rows, " ".join(r.text.strip() for r in rows)
    return g


def type_cmd(scene, t: Terminal, cmd: str, type_time: float | None = None):
    """Type `cmd` at the waiting prompt (replacing a bare prompt line if there is one). A line
    that doesn't fit folds with fold_cmd (at spaces, quote-aware, " \\" + 4-space indent): after
    the prompt when that needs no hard break, else the command starts on the row under the
    prompt (indented 4) and folds there. Returns the line (or a VGroup with .rows)."""
    _drop_bare(scene, t)
    p = t.prompt + (" " if t.prompt and not t.prompt.endswith(" ") else "")
    full = p + cmd
    if len(full) <= t.max_chars:
        return t.type(scene, cmd, type_time)
    fits_under = len(cmd) + 4 <= t.max_chars
    rows_a, hard_a = fold_cmd(full, t.max_chars, len(p))
    rows_b, hard_b = fold_cmd("    " + cmd, t.max_chars, 4)
    first_ok = len(rows_a) > 1 and len(rows_a[0]) - 2 > len(p) + 8   # a real start on row 0
    if not fits_under and first_ok and (not hard_a or hard_b):
        return _type_rows(scene, t, rows_a, len(p), type_time, len(cmd))
    return _type_rows(scene, t, [p.rstrip()] + rows_b, len(p.rstrip()), type_time, len(cmd))


def cd_prompt(scene, t: Terminal, new_prompt: str, color: str = LAPTOP, run_time: float = 0.8):
    """After a `cd`: the prompt becomes `new_prompt` (a bare prompt line) and the path part that
    changed flashes in `color`. Returns the bare line."""
    old = t.prompt
    t.set_prompt(new_prompt)
    ln = bare_prompt(scene, t)
    a = new_prompt.index(":") + 1
    b = len(new_prompt.rstrip("$# "))
    k = 0
    while k < min(len(old), len(new_prompt)) and old[k] == new_prompt[k]:
        k += 1
    start = k if len(new_prompt) > len(old) else a
    start = max(a, min(start, b - 1))
    part = glyph_range(ln, start, b)
    scene.play(Indicate(part, color=color, scale_factor=1.12), run_time=run_time)
    return ln


def second_terminal(scene, prompt: str = P_REPO, rows: int = 7, top: float = 2.75,
                    title: str = SECOND, intro: bool = False, run_time: float = 0.6) -> Terminal:
    """A second terminal slides in with its top at `top`, prompt `prompt` (a bare prompt line).
    intro=True first shows it in the home folder (P_HOME, the "~" flashing YELLOW, caption "new
    terminal: cd here first"). Returns the terminal (on screen)."""
    t = term(P_HOME if intro else prompt, rows=rows, title=title, top=top)
    scene.play(FadeIn(t, shift=DOWN * 0.3), run_time=run_time)
    if intro:
        ln = bare_prompt(scene, t)
        tilde = glyph_range(ln, P_HOME.index("~"), P_HOME.index("~") + 1)
        cap = note("new terminal: cd here first")
        beside(cap, t, ln, buff=0.5)
        scene.play(Indicate(tilde, color=TURN, scale_factor=1.4), FadeIn(cap), run_time=0.8)
        scene.wait(0.6)
        scene.play(FadeOut(cap), run_time=0.3)
        _drop_bare(scene, t)
        t.set_prompt(prompt)
    bare_prompt(scene, t)
    return t


def session(scene, t: Terminal, cap: Capture, *spec, wrap: bool = False, type_time=None,
            colors: dict | None = None, out_time: float = 0.5, answer_pause: float = 0.6):
    """Replay an interactive capture (laptop/12): `spec` as in Capture.at (file line numbers,
    ranges, "…"). A line that starts with a prompt sets t's prompt and types its command (exactly
    as captured); a prompt line with no command makes a bare prompt; a line where a prompt follows
    other text (laptop/12 line 11, "OpenAI API key: app@…:/app$ export OPENAI_API_KEY": the hidden
    read's prompt, then the next prompt) prints the text, waits `answer_pause`, then types the
    command at that prompt on the next row; other lines print in their emoji colour (or
    colors[file line]). Returns {file line: the mobject printed or typed for it}."""
    out = {}
    pending: list = []
    pend_nums: list = []

    def flush():
        if pending:
            new = t.print(scene, list(pending), wrap=wrap, run_time=out_time)
            if not wrap:
                for n, m in zip(pend_nums, new):
                    if n is not None:
                        out[n] = m
            pending.clear()
            pend_nums.clear()

    items = []
    for s in spec:
        if isinstance(s, str):
            items.append((None, s or "…"))
        elif isinstance(s, int):
            items.append((s, cap.line(s)))
        else:
            items += [(n, cap.line(n)) for n in range(s[0], s[1] + 1)]
    for n, text in items:
        sp = split_prompt(text) if n is not None else None
        inside = split_prompt_inside(text) if (n is not None and not sp) else None
        if sp:
            flush()
            t.set_prompt(sp[0])
            out[n] = type_cmd(scene, t, sp[1], type_time) if sp[1] else bare_prompt(scene, t)
        elif inside:
            before, prompt, cmd = inside
            pending.append((before.rstrip() + " ", (colors or {}).get(n, OUTPUT)))
            pend_nums.append(n)
            flush()
            scene.wait(answer_pause)
            t.set_prompt(prompt)
            out[(n, "cmd")] = type_cmd(scene, t, cmd, type_time) if cmd else bare_prompt(scene, t)
        else:
            col = (colors or {}).get(n, cap.color(n) if n is not None else S.GREY)
            pending.append((text, col))
            pend_nums.append(n)
    flush()
    return out


def show(scene, t: Terminal, cap: Capture, *spec, wrap: bool = False, run_time: float = 0.5,
         default: str = OUTPUT) -> VGroup:
    """Print capture lines in their emoji colours: t.print(scene, cap.out(*spec), wrap=wrap).
    spec as in Capture.out (file lines, ranges, "…", your own cut/fold/as401 results). Returns the
    printed rows (with wrap=True a line may fold into several rows: item_rows(rows, k))."""
    return t.print(scene, cap.out(*spec, default=default), wrap=wrap, run_time=run_time)


def type_after(scene, t: Terminal, row, word: str, color: str = TURN, pause: float = 0.6,
               type_time: float = 0.5):
    """Type `word` (YELLOW: a human decision) after the text of a printed row, as an answer typed
    at an input prompt (container/33 line 28 cut after "decline: ", then `approve`). The glyphs
    become part of the row (they scroll with it). Returns the typed Text."""
    row = _row_of(row)
    cw = cell_width(row.pt)
    w = mono_line(word, row.pt, color)
    x0 = grid_x0(row) + len(row.text) * cw
    w.shift(np.array([x0 - grid_x0(w), row.strut.get_center()[1] - w.strut.get_center()[1], 0]))
    if pause:
        scene.wait(pause)
    from manim import ShowIncreasingSubsets
    scene.play(ShowIncreasingSubsets(w.glyphs, rate_func=linear), run_time=type_time)
    scene.remove(w.glyphs)
    row.add(w)
    scene.add(row)
    return w


def frame_tags(t: Terminal, *tags, buff: float = 0.12) -> VGroup:
    """Place tags on the terminal's title bar, right-aligned from its right edge (`no key`, the
    GOLD `live · billed per token` when the typed command fills its row, `scripted`, `offline ·
    free`): they straddle the bar (clear of row 0). When they would reach the centred title, the
    title moves left next to the window dots (call this BEFORE the terminal is on screen). Returns
    them as one VGroup (placed, not added; FadeIn it; it does not scroll; resize() does not move
    it: place it again)."""
    g = VGroup(*tags).arrange(LEFT, buff=buff)
    g.move_to([t.box.get_right()[0] - 0.15 - g.width / 2, t.box.get_top()[1] - t.bar_h / 2, 0])
    if t.title is not None and g.get_left()[0] < t.title.get_right()[0] + 0.15:
        # the centred title moves left, next to the window dots (do this before the terminal is
        # on screen, or the title jumps)
        t.title.next_to(t.dots, RIGHT, buff=0.35)
        if g.get_left()[0] < t.title.get_right()[0] + 0.15:
            raise ValueError("frame_tags: the tags would cover the terminal's title")
    return g


def _row_of(line):
    """The row a tag belongs to: the line itself, or the last row of a folded command."""
    return line.rows[-1] if hasattr(line, "rows") else line


def beside(mob, t: Terminal, line, buff: float = 0.3):
    """Position `mob` (a tag, a check mark ...) right after the text of terminal line `line` (its
    last row when folded), centred on that row; if it would cross the terminal's right edge it
    sits at the right end of the row instead, where it may cover the end of a full row: callers
    may probe and fall back, and pin() refuses a tag that covers its row's text. Returns mob
    (not added)."""
    row = _row_of(line)
    ref = row.glyphs if len(getattr(row, "glyphs", [])) else row.strut
    mob.next_to(ref, RIGHT, buff=buff)
    mob.set_y(row.strut.get_center()[1])
    if mob.get_right()[0] > t.box.get_right()[0] - 0.12:
        mob.align_to(t.box, RIGHT).shift(LEFT * 0.12)
    return mob


def covers_text(mob, line) -> bool:
    """True when `mob` would hide the text of terminal line `line` (its last row when folded): it
    carries text or a filled box (a tag, a check mark) and crosses the row's glyphs. An outline drawn
    around the text hides nothing."""
    hides = any(type(m).__name__ in ("Text", "MarkupText", "Paragraph")
                or (isinstance(m, Rectangle) and m.get_fill_opacity() > 0.3) for m in mob.get_family())
    g = getattr(_row_of(line), "glyphs", None)
    if not hides or g is None or not len(g):
        return False
    l, r, b, t = mob.get_left()[0], mob.get_right()[0], mob.get_bottom()[1], mob.get_top()[1]
    return any(l < ch.get_right()[0] + 0.03 and r > ch.get_left()[0] - 0.03
               and b < ch.get_top()[1] and t > ch.get_bottom()[1]
               for ch in g.family_members_with_points())   # per character: a tag in a gap is fine


def pin(scene, line, mob, run_time: float = 0.4, anim=None):
    """Show `mob` (positioned, e.g. with beside()) and make it part of the terminal line (its
    last row when folded), so it scrolls and fades with it. A tag that would cover the row's text
    is an error: put it on an output row or under the terminal."""
    row = _row_of(line)
    if covers_text(mob, row):
        raise ValueError(f"pin(): this {mob.width:.2f}-wide tag would cover the text of its row "
                         f"(the text ends at x={row.glyphs.get_right()[0]:.2f}). "
                         "Put the tag on an output row or under the terminal.")
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


_TIME = re.compile(r"^\d+(\.\d+)?s$")


def build_row(row: str, width: int = 58) -> tuple[str, str | None]:
    """A BuildKit "=>" row or a Compose "✔" row -> (the row without its time field, cut to
    `width` with '…', the time, e.g. '20.2s', or None)."""
    r = row.rstrip()
    parts = r.rsplit(None, 1)
    time = None
    head = r.lstrip()
    if len(parts) == 2 and _TIME.match(parts[1]) and (head.startswith("=>") or head.startswith("✔")):
        r, time = parts[0].rstrip(), parts[1]
    if len(r) > width:
        r = r[:width - 1] + "…"
    return r, time


def time_tag(time: str) -> VGroup:
    """The GREY tag holding a BuildKit row's time (see build_row). Its pill is 0.08 shorter than
    the terminal's row pitch, so the tags of neighbouring rows don't touch (the shared tag() pill,
    0.47 tall, overlapped the next row's by 0.06; S05 critic). .box .text as tag()."""
    g = tag(time, S.GREY)
    h = line_pitch(TERM_PT) - 0.08
    if g.box.height > h:
        b = RoundedRectangle(width=g.box.width, height=h, corner_radius=h / 2, stroke_color=S.GREY,
                             stroke_width=2).set_fill(S.BG, 0.92).move_to(g.box)
        g.submobjects[g.submobjects.index(g.box)] = b
        g.box = b
        g.text.move_to(b)
    return _keep(g)


def place_time(tg, t: Terminal, line) -> VGroup:
    """Put a time tag at the right end of terminal line `line`, inside the frame."""
    return tg.move_to(line.strut).align_to(t.box, RIGHT).shift(LEFT * 0.12)


def print_build(scene, t: Terminal, rows: list, run_time: float = 0.6, color: str = OUTPUT,
                lag: float = 0.12) -> VGroup:
    """Print BuildKit / Compose rows (raw capture lines, or "…") cut at 58 chars; a row's time
    field becomes a GREY time tag at the row's right end, part of the row (.time_tag; None when
    the row has no time). (text, colour) items are accepted. Returns the new lines."""
    items = []
    for r in rows:
        s, col = (r, color) if isinstance(r, str) else r
        txt, tm = build_row(s, t.max_chars - 7) if s != "…" else ("…", None)
        items.append((txt, col, tm))
    t._make_room(scene, len(items))
    new = VGroup()
    for txt, col, tm in items:
        ln = mono_line(txt, t.size, col)
        t._place(ln, len(t.lines))
        ln.time_tag = None
        if tm:
            tg = time_tag(tm)
            place_time(tg, t, ln)
            ln.add(tg)
            ln.time_tag = tg
        t.lines.add(ln)
        new.add(ln)
    scene.play(LaggedStart(*[FadeIn(m) for m in new], lag_ratio=lag), run_time=run_time)
    return new


def grid_x0(line) -> float:
    """The x of column 0's left edge in a mono_line, measured from its glyphs (the median over
    non-space characters of glyph centre − (k + 0.5) · cell width). Falls back to the strut."""
    cw = cell_width(line.pt)
    offs, gi = [], 0
    for k, ch in enumerate(line.text):
        if ch.isspace():
            continue
        if gi >= len(line.glyphs):
            break
        offs.append(line.glyphs[gi].get_center()[0] - (k + 0.5) * cw)
        gi += 1
    return float(np.median(offs)) if offs else line.strut.get_left()[0]


def col_box(line, a: int, b: int, color: str = TURN, dashed: bool = False, pad: float = 0.04):
    """A box over character columns a..b (exclusive) of a mono_line, blank cells included. Not
    added."""
    cw = cell_width(line.pt)
    x0 = grid_x0(line) + a * cw
    r = box((b - a) * cw + 2 * pad, line.strut.height + 2 * pad, color, fill_opacity=0.0,
            radius=0.06, dashed=dashed, stroke=3)
    r.move_to([x0 + (b - a) * cw / 2, line.strut.get_center()[1], 0])
    return r


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


def your_turn() -> VGroup:
    """YELLOW '▶ your turn' tag: put it next to a command the viewer should run now."""
    return _keep(tag("▶ your turn", TURN))


def extra_tag() -> VGroup:
    return grey_tag("extra")


def illustration_tag(note_: str | None = None) -> VGroup:
    """GREY 'illustration' (every schematic: Colab, the browser, the editor, the rings, the
    turnstile, the jar, the shelf, the "what if" variants); note_="what if" -> 'illustration · what if'."""
    return grey_tag("illustration" + (f" · {note_}" if note_ else ""))


def recording_tag() -> VGroup:
    """'at the time of recording' (next to versions)."""
    return grey_tag("at the time of recording")


def expected_tag() -> VGroup:
    """README text about live output (a QUOTE card), never styled as output."""
    return grey_tag("expected")


def nokey_tag() -> VGroup:
    """On every terminal that runs a live command here (it stops at OpenAI's 401)."""
    return grey_tag("no key")


no_key_tag = nokey_tag


def scripted_tag() -> VGroup:
    """On every --fixture run: real program output, scripted proposals, never the model's answer."""
    return grey_tag("scripted")


def cost_chip(s: str) -> VGroup:
    """A GOLD chip counting live runs ("2 runs", "12 runs", "4 runs")."""
    return _keep(chip(s, COST, size=CAPTION))


def template_tag() -> VGroup:
    return grey_tag("a template")


def erratum_tag(note_: str | None = None) -> VGroup:
    return grey_tag("erratum" + (f" · {note_}" if note_ else ""))


def harmless_tag() -> VGroup:
    return grey_tag("harmless")


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


def top_chip(text: str, where: str | None = None, color: str = TURN, expected: bool = False,
             tall: bool = False) -> VGroup:
    """A one-line chip in the top band (script: "a one-line chip in the top band right of the
    tracker"): a YELLOW chip ("step 4 · run k times"), or, with `where`, a README chip
    ("README.md · line 248" + the phrase in quotes; expected=True adds the GREY `expected` tag).
    Right edge at CHIP_RIGHT. Default: centred on TOPCHIP_Y (2.66), between the tracker (bottom
    2.925) and a terminal of up to 12 rows (top 2.19), so it may run left under the tracker: up to
    13.0 wide. tall=True (a 13-row terminal, top 2.59): centred on 2.87, right of the tracker
    (x >= -1.9) and under the lecture tag: at most 8.4 wide. Placed, not added; raises if too wide
    (keep the phrase <= 40 characters)."""
    max_w = 8.4 if tall else 13.0
    if where:
        g = readme_chip(where, text, max_w=max_w, expected=expected)
    else:
        g = _keep(chip(text, color, size=CAPTION))
        if g.width > max_w:
            raise ValueError(f"top chip {text!r} is {g.width:.1f} wide (> {max_w})")
    return g.move_to([CHIP_RIGHT - g.width / 2, TOPCHIP_TALL_Y if tall else TOPCHIP_Y, 0])


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
    if expected:
        tg = expected_tag().next_to(fr, RIGHT, buff=0.15)
        g.add(tg)
        g.tag = tg
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


def turn_card(rows, width: float | None = None, header: str | None = None,
              size: float = CAPTION) -> VGroup:
    """The static GREY "your turn" card (a ▶ that stays readable when paused). rows: a str is a
    command typed exactly as on screen (mono; "\\n" splits it into rows), (cmd, "extra") adds the
    extra tag, (cmd, note) a GREY note, Prose("…") a serif row, (Prose("…"), colour) a coloured
    serif row (the GOLD cost line last), a list ["`uv sync`", "in the repo root"] one row mixing
    mono ("`code`") and serif pieces on one baseline. The YELLOW ▶ your turn tag sits on the
    top-right corner (.tag). header: an optional GREY line above the card; None by default (QA:
    a GREY "your turn" header only repeated the YELLOW tag). .frame .rows .tag"""
    items = VGroup()
    for r in rows:
        if isinstance(r, Prose):
            items.add(label(str(r), size, INK))
            continue
        if isinstance(r, list):
            items.add(_mixed_row(r, size))
            continue
        if isinstance(r, tuple) and isinstance(r[0], Prose):
            items.add(label(str(r[0]), size, r[1]))
            continue
        cmd, extra = (r, None) if isinstance(r, str) else r
        lines = VGroup(*[mono(s, size, INK) for s in cmd.split("\n")])
        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        if extra:
            t = extra_tag() if extra == "extra" else note(extra)
            t.next_to(lines[-1], RIGHT, buff=0.3)
            lines.add(t)
        items.add(lines)
    items.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    w = max(width or 0, items.width + 0.6)
    fr = box(w, items.height + 0.6, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.14)
    items.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.3)
    g = VGroup(fr, items)
    if header:
        h = note(header).next_to(fr, UP, buff=0.08).align_to(fr, LEFT).shift(RIGHT * 0.12)
        g.add(h)
    tg = your_turn().move_to(fr.get_corner(UP + RIGHT)).shift(LEFT * 1.0)
    g.add(tg)
    g.frame, g.rows, g.tag = fr, items, tg
    return g


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


def extra_card(purpose: str, title: str = "an extra check · in the study guide") -> VGroup:
    """The GREY card standing for an extra script or a long plumbing command (its code is never
    shown): the `extra` tag and `title` as its header, the one-line purpose in quotes inside.
    .frame .rows .header .tag"""
    c = card_rows([f"“{purpose}”"])
    tg = extra_tag()
    t = note(title)
    hd = VGroup(tg, t).arrange(RIGHT, buff=0.2)
    hd.next_to(c.frame, UP, buff=0.08).align_to(c.frame, LEFT).shift(RIGHT * 0.1)
    c.add(hd)
    c.header, c.tag = hd, tg
    return c


check_card = extra_card


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


class LookFor(VGroup):
    """The "with your key, look for" card (and "if it fails with your key"): a GREY caption card
    (never terminal-styled), one row per item: (text, where) -> "text · where" (where in GREY,
    e.g. "cli.py · line 454"); text in backticks is mono. The frame is built for every row from
    the start; rows are invisible until write_item(i). .frame .rows .title"""

    def __init__(self, items, title: str = "with your key, look for", width: float | None = None,
                 size: float = CAPTION, **kw):
        super().__init__(**kw)
        rows = VGroup()
        for it in items:
            text, where = (it, None) if isinstance(it, str) else it
            parts = [_cell(text, size)]
            if where:
                parts.append(label(f"· {where}", size, S.GREY))
            rows.add(VGroup(*parts).arrange(RIGHT, buff=0.15))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        ttl = label(title, size, S.GREY)
        w = max(width or 0, rows.width + 0.6, ttl.width + 0.6)
        fr = box(w, rows.height + ttl.height + 0.75, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.14)
        ttl.move_to(fr.get_corner(UP + LEFT) + np.array([0.3, -0.3, 0]), aligned_edge=LEFT)
        rows.next_to(ttl, DOWN, buff=0.2, aligned_edge=LEFT)
        for r in rows:
            r.set_opacity(0)
        self.frame, self.rows, self.title = fr, rows, ttl
        self.add(fr, ttl, rows)

    def write_item(self, i: int, run_time: float = 0.5):
        r = self.rows[i]
        r.set_opacity(1)
        return FadeIn(r, shift=RIGHT * 0.15, run_time=run_time)


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


def json_card(lines, color: str = DATA, size: float = CAPTION, header: str | None = None) -> VGroup:
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


# ================================================================== L08: tags, terminals, cards
def recorded_tag(s: str = "recorded · the staff's saved Colab run (A100)") -> VGroup:
    """The tag of every RECORDED box (the staff's saved Colab outputs, an A100 run; never a T4
    measurement)."""
    return grey_tag(s)


def differ_tag() -> VGroup:
    """On container ids (app@6f5113cdb660): "your id will differ"."""
    return grey_tag("your id will differ")


def estimate_tag() -> VGroup:
    """On our own 0.6 B memory figures (S14)."""
    return grey_tag("estimate")


def billed_tag(s: str = "billed") -> VGroup:
    """GOLD, on --generate, --upload, --train, --chat (and the Colab runtime card)."""
    return _keep(tag(s, COST))


cost_tag = billed_tag


def free_tag(s: str = "free") -> VGroup:
    """GREEN: nothing is billed."""
    return _keep(tag(s, OWN))


def dtype_tag(s: str, size: float = CAPTION) -> VGroup:
    """A small neutral white dtype label (NF4, FP16, FP32, BF16) on whatever it describes."""
    return _keep(tag(s, INK, size=size))


def term(prompt: str = P_WS, rows: int = 12, title: str | None = None, container: str | bool | None = None,
         top: float | None = None, width: float = TERM_W, size: float = TERM_PT) -> Terminal:
    """The house terminal (full width 12.6, 22 pt, 65 characters a row, at most 13 rows), bottom
    edge at BOTTOM, or its top edge at `top`. Laptop: title "laptop", prompt P_WS by default.
    container="dc" (or True): inside llm-dataset-creator (TEAL frame, title CTR_DC_TITLE, prompt
    P_CTR_DC); container="gf": gemini-finetuner (CTR_GF_TITLE, P_CTR_GF)."""
    if rows > 13:
        raise ValueError("a house terminal has at most 13 rows (script.md 'Terminal width')")
    which = "dc" if container is True else container
    if which:
        dflt_p, dflt_t = (P_CTR_DC, CTR_DC_TITLE) if which == "dc" else (P_CTR_GF, CTR_GF_TITLE)
        if prompt == P_WS:
            prompt = dflt_p
        ttl = title or dflt_t
    else:
        ttl = title or LAPTOP_TITLE
    t = _L8Terminal(prompt=prompt, width=width, rows=rows, size=size, title=ttl)
    if which:
        t.box.set_stroke(CTR, 3)
        t.title.set_color(CTR)
    y = (top - t.box.get_top()[1]) if top is not None else (BOTTOM - t.box.get_bottom()[1])
    t.shift(np.array([-t.box.get_center()[0], y, 0]))
    return t


def enter_container(t: Terminal, which: str = "dc") -> list:
    """Animations: the frame turns TEAL, the title becomes "container · llm-dataset-creator" (or
    "container · gemini-finetuner" with which="gf"), old title out, then the new one in; the
    prompt becomes P_CTR_DC / P_CTR_GF for the next typed line."""
    prompt, title = (P_CTR_DC, CTR_DC_TITLE) if which == "dc" else (P_CTR_GF, CTR_GF_TITLE)
    t.set_prompt(prompt)
    new = mono(title, CAPTION, CTR).move_to(t.title)
    return [t.box.animate.set_stroke(CTR, 3), *_swap_title(t, new)]


def leave_container(t: Terminal, prompt: str = P_DC, title: str = LAPTOP_TITLE) -> list:
    """Animations: back on the laptop (GREY frame, title `title`, prompt `prompt`)."""
    t.set_prompt(prompt)
    new = mono(title, CAPTION, S.GREY).move_to(t.title)
    return [t.box.animate.set_stroke(S.GREY_DARK, 2), *_swap_title(t, new)]


def quote_card(src, *spec, wrap: int = 88, width: float | None = None, expected: bool = True,
               header: str | None = None) -> VGroup:
    """QUOTE(expected/readme-…: lines): README text about what a working run prints, as a GREY
    quote card (never a terminal), headed with its README lines (from the file's '#' header, e.g.
    "README.md · lines 288–301"), the GREY `expected` tag beside the header. src: the expected file
    ("readme-cost-table" or "expected/readme-cost-table"); spec: its FILE line numbers / (a, b)
    ranges / "…" as in Capture.at (``` fence lines are refused). src may instead be an int a with
    spec (b,): README.md lines a..b directly. Inline `code` is mono, the persona GREY; rows wrap at
    `wrap` characters. .frame .rows .header .tag"""
    if isinstance(src, int):
        b = spec[0] if spec else src
        where = header or (f"README.md · line {src}" if b == src else f"README.md · lines {src}–{b}")
        src_rows = readme(src, b)
    else:
        name = src if "/" in src else f"expected/{src}"
        c = capture(name)
        where = header or expected_where(name)
        src_rows = c.at(*spec) if spec else list(c.lines)
        if any(r.strip().startswith("```") for r in src_rows):
            raise ValueError("quote_card: leave out the ``` fence lines")
    rows_txt = [r for ln in src_rows if ln.strip() for r in _wrap_words(ln, wrap)]
    rows = VGroup(*[_md_text(r) for r in rows_txt]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    w = max(width or 0, rows.width + 0.5)
    fr = box(w, rows.height + 0.4, S.GREY, fill=S.BG, fill_opacity=0.92, radius=0.12)
    rows.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.25)
    head = _header_text(where).next_to(fr, UP, buff=0.08).align_to(fr, LEFT).shift(RIGHT * 0.1)
    g = VGroup(fr, rows, head)
    g.frame, g.rows, g.header, g.tag = fr, rows, head, None
    if expected:
        tg = expected_tag().next_to(head, RIGHT, buff=0.25)
        g.add(tg)
        g.tag = tg
    if g.width > 12.9:
        raise ValueError(f"quote card {g.width:.1f} wide: lower wrap=")
    return g


def recorded_box(name: str, *spec, header: str | None = None, width: float | None = None,
                 tag_: bool = True, tag_at: str = "auto") -> VGroup:
    """RECORDED(expected/colab-cNN-…: lines): the staff's saved Colab output as an output box (never
    a terminal frame), emoji stripped and coloured (🔵 GREY, 🟢 GREEN), names masked; header
    "QLoRA notebook · 4.4 · cell 75 · saved output" (from the file name) unless given; the GREY tag
    `recorded · the staff's saved Colab run (A100)` above its right end (below when the header is
    in the way; tag_at="down" always below, "top" above the header, right-aligned: use it when the
    box sits low on the frame; tag_=False: none). spec as in Capture.out (FILE line numbers; the cell's code lines
    are never output). .frame .rows .header .tag"""
    c = capture(name if "/" in name else f"expected/{name}")
    m = re.search(r"colab-c(\d+)", c.name)
    hd = header if header is not None else (f"{colab_where(int(m.group(1)))} · saved output" if m else None)
    g = output_box(c.out(*spec), hd, width=width)
    g.tag = None
    if tag_:
        tg = recorded_tag()
        tg.next_to(g.frame, UP, buff=0.08).align_to(g.frame, RIGHT)
        clash = g.header is not None and tg.get_left()[0] < g.header.get_right()[0] + 0.2
        if tag_at == "down" or (clash and tag_at == "auto"):
            tg.next_to(g.frame, DOWN, buff=0.08).align_to(g.frame, RIGHT)
        elif tag_at == "top" and g.header is not None:
            tg.next_to(g.header, UP, buff=0.08).align_to(g.frame, RIGHT)
        g.add(tg)
        g.tag = tg
    return g


def colab_frame(title: str = COLAB_TITLE, width: float = 12.9, top: float = 2.75, bottom: float = -3.5,
                size: float = 22) -> VGroup:
    """The Colab notebook drawn schematically: a BLUE rounded frame (Google's VM) with "QLoRA
    notebook · Colab" in a tab on the top border and the `illustration` tag at the top right. Built
    in place (centred on x = 0, y from `bottom` to `top`). .frame .title .tag"""
    fr = RoundedRectangle(width=width, height=top - bottom, corner_radius=0.2, stroke_color=CLOUD,
                          stroke_width=3).set_fill(CLOUD, 0.03).move_to([0, (top + bottom) / 2, 0])
    t = label(title, size, CLOUD)
    tab = RoundedRectangle(width=t.width + 0.5, height=t.height + 0.24, corner_radius=0.12,
                           stroke_color=CLOUD, stroke_width=2).set_fill(S.BG, 1)
    tab.move_to(fr.get_corner(UP + LEFT) + np.array([0.4 + tab.width / 2, 0, 0]))
    t.move_to(tab)
    tg = illustration_tag()
    tg.move_to(fr.get_corner(UP + RIGHT) + np.array([-0.35 - tg.width / 2, 0, 0]))
    g = VGroup(fr, tab, t, tg)
    g.frame, g.title, g.tag = fr, VGroup(tab, t), tg
    return g


# ================================================================== facts read from the captures
def loss_points() -> list[tuple[int, float]]:
    """The training-loss table of the staff's run (expected/colab-c75 'Step  Training Loss'):
    [(50, 2.007381), …, (450, 1.350437)]."""
    c = capture("expected/colab-c75-train")
    out = []
    for s in c.lines:
        m = re.fullmatch(r"\s*(\d+)\s+(\d+\.\d+)\s*", s)
        if m:
            out.append((int(m.group(1)), float(m.group(2))))
    return out


def eval_table() -> dict[str, tuple[float, float]]:
    """expected/colab-c80's loss / perplexity rows: {"Base (4-bit)": (2.6498, 14.15),
    "Fine-tuned (4-bit + LoRA)": (1.3872, 4.0)}."""
    c = capture("expected/colab-c80-eval-loss-perplexity")
    out = {}
    for s in c.lines:
        m = re.fullmatch(r"(Base \(4-bit\)|Fine-tuned \(4-bit \+ LoRA\))\s+([\d.]+)\s+([\d.]+)\s*", s)
        if m:
            out[m.group(1)] = (float(m.group(2)), float(m.group(3)))
    return out


# ================================================================== small glyphs
def snowflake(r: float = 0.16, color: str = FROZEN, stroke: float = 2.5) -> VGroup:
    """The frozen-weights mark: six spokes with small twigs."""
    g = VGroup()
    for k in range(6):
        ang = k * TAU / 6
        spoke = Line(ORIGIN, UP * r, stroke_width=stroke, color=color)
        tw1 = Line(UP * r * 0.55, UP * r * 0.55 + (UP + RIGHT) * r * 0.25, stroke_width=stroke * 0.8, color=color)
        tw2 = Line(UP * r * 0.55, UP * r * 0.55 + (UP + LEFT) * r * 0.25, stroke_width=stroke * 0.8, color=color)
        g.add(VGroup(spoke, tw1, tw2).rotate(ang, about_point=ORIGIN))
    return _keep(g)


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


def answer_card(rows: list[str], color: str = MODEL, title: str | None = None, width: float = 5.6,
                size: float = CAPTION, dashed: bool = False) -> VGroup:
    """An answer card (S01, S15: what a model wrote): rows of serif text (`code` mono, the persona
    GREY) in a box of `color` (BLUE: a model wrote it); rows longer than the box are broken at spaces
    (fit_rows). title: a GREY line above ("base Qwen3-0.6B"). .frame .rows .title"""
    body = VGroup(*[fit_rows(unname(r), width - 0.5, size) for r in rows]).arrange(DOWN, aligned_edge=LEFT,
                                                                                  buff=0.14)
    fr = box(width, body.height + 0.45, color, fill=S.BG, fill_opacity=0.95, radius=0.14, dashed=dashed)
    tint = RoundedRectangle(width=width, height=fr.height, corner_radius=0.14, stroke_width=0) \
        .set_fill(color, 0.07).move_to(fr)
    body.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.25)
    g = VGroup(tint, fr, body)
    g.frame, g.rows, g.title = fr, body, None
    if title:
        t = note(title).next_to(fr, UP, buff=0.08).align_to(fr, LEFT).shift(RIGHT * 0.1)
        g.add(t)
        g.title = t
    return g


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


# ================================================================== V1 · three dials (S02, S15)
class Dial(VGroup):
    """A dial: a circle with ticks, a needle and a serif label under it. .turn(angle) -> anim;
    .light(colour) -> anims. .face .needle .label .center_point()"""

    def __init__(self, text: str, color: str = S.GREY, r: float = 0.42, size: float = CAPTION, **kw):
        super().__init__(**kw)
        self.r = r
        self.face = Circle(radius=r, stroke_color=color, stroke_width=3).set_fill(S.BG, 1)
        self.ticks = VGroup(*[Line(UP * r * 0.75, UP * r * 0.95, color=color, stroke_width=2)
                              .rotate(a, about_point=ORIGIN) for a in np.linspace(-2.2, 2.2, 7)])
        self.needle = Line(ORIGIN, UP * r * 0.7, color=INK, stroke_width=4).rotate(1.6, about_point=ORIGIN)
        self.hub = Dot(radius=0.05, color=INK)
        self.label = label(text, size, color).next_to(self.face, DOWN, buff=0.12)
        self.add(self.face, self.ticks, self.needle, self.hub, self.label)

    def center_point(self):
        return self.face.get_center()

    def turn(self, angle: float = -1.6, run_time: float = 0.8):
        return Rotate(self.needle, angle=angle, about_point=self.center_point(), run_time=run_time)

    def light(self, color: str = TURN) -> list:
        return [self.face.animate.set_stroke(color, 4), self.label.animate.set_color(color)]


class ThreeDials(Piece):
    """V1 (S02, S15): a BLUE model box holding a grid of weight cells, three dials under it —
    prompt, context, weights — and an input point (left) and output point (right). Built centred
    at ORIGIN: 7.4 wide x 3.9 tall (box 3.6 x 2.2).

        td = ThreeDials()
        self.play(*td.turn("prompt"))           # needle turns, dial lights YELLOW
        self.play(td.shimmer())                 # the weights change (only the weights dial does this)
        td.input_point() / td.output_point()    # where input cards / answer cards attach
    .box .cells (VGroup of squares) .dials {"prompt", "context", "weights"} .wire (dial -> target lines)
    """

    def __init__(self, box_w: float = 3.6, box_h: float = 2.2, name: str = "model", **kw):
        super().__init__(**kw)
        self.box = box(box_w, box_h, MODEL, fill_opacity=0.08, stroke=3)
        self.title = label(name, CAPTION, MODEL).next_to(self.box, UP, buff=0.1)
        rng = np.random.default_rng(8)
        self.cells = VGroup(*[Rectangle(width=0.26, height=0.26, stroke_width=0)
                              .set_fill(MODEL, float(rng.uniform(0.15, 0.75))) for _ in range(6 * 9)])
        self.cells.arrange_in_grid(6, 9, buff=0.08).move_to(self.box)
        self.part("box", VGroup(self.box, self.title, self.cells))
        d = {n: Dial(n) for n in ("prompt", "context", "weights")}
        row = VGroup(*d.values()).arrange(RIGHT, buff=1.4).next_to(self.box, DOWN, buff=0.5)
        self.dials = d
        self.part("dials", row)
        # wires: prompt and context feed the input; weights feeds the box itself
        x_in = self.box.get_left()[0] - 1.6
        self.in_pt = np.array([x_in, self.box.get_center()[1], 0])
        w_p = _poly([d["prompt"].face.get_top(), [d["prompt"].face.get_top()[0], self.in_pt[1] - 0.6, 0],
                     [x_in, self.in_pt[1] - 0.6, 0]], S.GREY_DARK, 2)
        w_c = _poly([d["context"].face.get_top(), [d["context"].face.get_top()[0], self.box.get_bottom()[1] - 0.15, 0],
                     [x_in + 0.25, self.box.get_bottom()[1] - 0.15, 0], [x_in + 0.25, self.in_pt[1] - 0.6, 0]],
                    S.GREY_DARK, 2)
        w_w = Line(d["weights"].face.get_top(), [d["weights"].face.get_top()[0], self.box.get_bottom()[1], 0],
                   color=S.GREY_DARK, stroke_width=2)
        self.wire = {"prompt": w_p, "context": w_c, "weights": w_w}
        self.part("wires", VGroup(w_p, w_c, w_w))
        self.arrow_in = _arrow(self.in_pt, self.box.get_left(), S.GREY, 3)
        self.arrow_out = _arrow(self.box.get_right(), self.box.get_right() + RIGHT * 1.4, S.GREY, 3)
        self.part("arrows", VGroup(self.arrow_in, self.arrow_out))
        self.move_to(ORIGIN)

    def input_point(self):
        return self.arrow_in.get_start()

    def output_point(self):
        return self.arrow_out.get_end()

    def turn(self, name: str, angle: float = -1.6) -> list:
        """Animations: dial `name` turns, lights YELLOW, and its wire lights."""
        dl = self.dials[name]
        return [dl.turn(angle), *dl.light(TURN), self.wire[name].animate.set_stroke(TURN, 3)]

    def settle(self, name: str) -> list:
        """Animations: dial `name` back to GREY (its needle stays where it is)."""
        dl = self.dials[name]
        return [dl.face.animate.set_stroke(S.GREY, 3), dl.label.animate.set_color(S.GREY),
                self.wire[name].animate.set_stroke(S.GREY_DARK, 2)]

    def shimmer(self, seed: int = 3, run_time: float = 1.2):
        """Animation: every weight cell takes a new brightness (the weights changed)."""
        rng = np.random.default_rng(seed)
        target = self.cells.copy()
        for c in target:
            c.set_fill(MODEL, float(rng.uniform(0.15, 0.75)))
        return Transform(self.cells, target, run_time=run_time)


class AdapterSwitch(VGroup):
    """V1's weights dial as the disable_adapter() switch (S15): a GREEN pill switch "adapter on" /
    GREY "adapter off" with the mono caption "disable_adapter()" under it. .flip(on) -> anims.
    1.9 x 1.1. .track .knob .state .caption .on"""

    def __init__(self, on: bool = True, **kw):
        super().__init__(**kw)
        self.track = RoundedRectangle(width=1.2, height=0.5, corner_radius=0.25, stroke_width=3)
        self.knob = Circle(radius=0.19, stroke_width=0)
        self.caption = mono("disable_adapter()", CAPTION, S.GREY).next_to(self.track, DOWN, buff=0.15)
        self.state = label("adapter on" if on else "adapter off", CAPTION, OWN if on else S.GREY)
        self.state.next_to(self.track, UP, buff=0.12)
        self.on = on
        self._paint(on)
        self.add(self.track, self.knob, self.state, self.caption)

    def _paint(self, on: bool):
        col = OWN if on else S.GREY
        self.track.set_stroke(col, 3).set_fill(col, 0.25 if on else 0.08)
        self.knob.set_fill(col, 1).move_to(self.track.get_center() + RIGHT * (0.33 if on else -0.33))

    def flip(self, on: bool, run_time: float = 0.6) -> list:
        col = OWN if on else S.GREY
        new = label("adapter on" if on else "adapter off", CAPTION, col).move_to(self.state)
        old, self.state = self.state, new
        self.on = on
        return [self.track.animate(run_time=run_time).set_stroke(col, 3).set_fill(col, 0.25 if on else 0.08),
                self.knob.animate(run_time=run_time).set_fill(col, 1).move_to(
                    self.track.get_center() + RIGHT * (0.33 if on else -0.33)),
                AnimationGroup(*_swap_text(self, old, new), run_time=run_time)]


class NextTokenBars(VGroup):
    """S15's illustrative next-token bar chart (tag it `illustration`): one bar per token, mono
    token labels under the bars, after a GREY mono prompt "<|im_start|>assistant". .morph(tokens,
    probs) -> anims (bars grow / shrink, labels swap old-out new-in). Built centred: width x
    (max_h + 1.2). .bars .labels .prompt"""

    def __init__(self, tokens, probs, width: float = 5.0, max_h: float = 2.0, color: str = MODEL,
                 prompt: str | None = "<|im_start|>assistant", **kw):
        super().__init__(**kw)
        self.max_h, self.hi_color = max_h, color
        n = len(tokens)
        bw = min(1.0, width / n * 0.6)
        xs = np.linspace(-width / 2 + width / (2 * n), width / 2 - width / (2 * n), n)
        self.base = Line([-width / 2, 0, 0], [width / 2, 0, 0], color=S.GREY, stroke_width=2)
        self.bars = VGroup()
        self.labels = VGroup()
        for x, tkn, p in zip(xs, tokens, probs):
            b = Rectangle(width=bw, height=max(0.02, p * max_h), stroke_color=color, stroke_width=2) \
                .set_fill(color, 0.45)
            b.move_to([x, b.height / 2, 0])
            self.bars.add(b)
            self.labels.add(mono(tkn, CAPTION, INK).move_to([x, -0.25, 0]))
        self.add(self.base, self.bars, self.labels)
        self.prompt = None
        if prompt:
            self.prompt = mono(prompt, CAPTION, S.GREY).next_to(self.labels, DOWN, buff=0.25)
            self.add(self.prompt)
        self.move_to(ORIGIN)

    def morph(self, tokens, probs, color: str | None = None, run_time: float = 1.2) -> list:
        col = color or self.hi_color
        y0 = self.base.get_center()[1]
        anims = []
        for b, p in zip(self.bars, probs):
            tgt = b.copy().stretch_to_fit_height(max(0.02, p * self.max_h)).set_fill(col, 0.45).set_stroke(col)
            tgt.move_to([b.get_center()[0], y0 + tgt.height / 2, 0])
            anims.append(Transform(b, tgt, run_time=run_time))
        for k, (old, tkn) in enumerate(zip(list(self.labels), tokens)):
            new = mono(tkn, CAPTION, INK).move_to(old)
            anims.append(AnimationGroup(*_swap_text(self.labels, old, new), run_time=run_time))
        return anims


# ================================================================== V2 · the stage (S03, S04, S07-S09)
class Stage(Piece):
    """V2, built in place above a 3-row strip (x -6.4..6.4, y -1.25..2.75): the GREY laptop
    (~/AC215 with llm-finetuning/ and secrets/ side by side, a dashed GOLD key outline in secrets/),
    two TEAL containers built from one recipe (llm-dataset-creator, gemini-finetuner) with PINK bind
    mounts (dataset-creator/ -> /app, secrets/ -> /secrets; gemini-finetuner/ -> /app, secrets/ ->
    /secrets), and the BLUE cloud with four pins: global (the Gemini teacher), the bucket,
    us-central1 (the tuning job), us (the endpoint). No port arrows.

    Parts (Piece: reveal(scene, *names) / hide / parts_in / parts_out): "laptop", "key" (the
    outline), "dc", "gf", "mounts_dc", "mounts_gf", "cloud", "pin_global", "pin_bucket",
    "pin_tune", "pin_us". Stage(show=None) shows every part; show=("laptop",) only those.
    .row(name) laptop rows: "ws" "repo" "dc" "gf" "env" "secrets"
    .route(cmd) -> a PINK arrow (not added) from the container to the pin of "--generate" (global),
        "--upload" (bucket), "--train" (us-central1), "--chat" (us)
    .blocked(cmd) -> VGroup (not added): a short PINK stub out of the container wall and a RED
        "no key" stamp just inside the wall (the capture: every route stops there)
    .job_arrow() -> PINK curved arrow bucket -> us-central1 (the job reads your bucket itself)
    .key_in() -> anims: a solid GOLD key replaces the dashed outline (with a key)
    .light(name, colour) -> anims (a part's frame lights)
    """

    ROUTES = {"--generate": ("dc", "pin_global"), "--upload": ("dc", "pin_bucket"),
              "--train": ("gf", "pin_tune"), "--chat": ("gf", "pin_us")}

    def __init__(self, show=None, top: float = 2.75, bottom: float = -1.25, **kw):
        super().__init__(**kw)
        h = top - bottom
        cy = (top + bottom) / 2
        # -- laptop
        lap = box(3.9, h, LAPTOP, fill_opacity=0.04, radius=0.2).move_to([-6.4 + 1.95, cy, 0])
        cap = label("your laptop", CAPTION, LAPTOP).move_to(lap.get_corner(DOWN + LEFT), aligned_edge=DOWN + LEFT) \
            .shift(np.array([0.2, 0.12, 0]))
        names = [("ws", "~/AC215/"), ("repo", "  llm-finetuning/"), ("dc", "    dataset-creator/"),
                 ("gf", "    gemini-finetuner/"), ("env", "    env.dev"), ("secrets", "  secrets/")]
        rows = VGroup(*[mono(s.strip(), CAPTION, LAPTOP if k != "env" else INK) for k, s in names])
        rows.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        for r, (k, s) in zip(rows, names):
            lead = len(s) - len(s.lstrip(" "))
            r.shift(RIGHT * lead * cell_width(CAPTION))
        rows.move_to(lap).align_to(lap, LEFT).shift(RIGHT * 0.2 + UP * 0.25)
        self._rows = {k: r for (k, _), r in zip(names, rows)}
        self.part("laptop", VGroup(lap, cap, rows))
        sec = self._rows["secrets"]
        self.key_out = key_outline(0.26).next_to(sec, RIGHT, buff=0.25)
        self.part("key", self.key_out)
        # -- containers
        x_c = -6.4 + 3.9 + 0.45 + 1.75
        self.boxes = {}
        for k, title, y in (("dc", "llm-dataset-creator", cy + h / 4), ("gf", "gemini-finetuner", cy - h / 4)):
            c = container_box(title, 3.5, h / 2 - 0.15)
            c.move_to([x_c, y, 0])
            pts = VGroup(mono("/app", CAPTION, CTR), mono("/secrets", CAPTION, CTR)).arrange(DOWN, buff=0.18,
                                                                                         aligned_edge=LEFT)
            pts.next_to(c.title, DOWN, buff=0.18).align_to(c.frame, LEFT).shift(RIGHT * 0.3)
            g = VGroup(c, pts)
            g.frame, g.title, g.app, g.secrets = c.frame, c.title, pts[0], pts[1]
            self.boxes[k] = g
            self.part(k, g)
        # -- mounts
        for k in ("dc", "gf"):
            g = self.boxes[k]
            m1 = _arrow(self._rows[k].get_right() + RIGHT * 0.08, g.app.get_left() + LEFT * 0.08, LOOKUP, 2.5)
            m2 = _arrow(self.key_out.get_right() + RIGHT * 0.08, g.secrets.get_left() + LEFT * 0.08, LOOKUP, 2.5)
            self.part(f"mounts_{k}", VGroup(m1, m2))
        # -- cloud
        x0 = x_c + 1.75 + 0.45
        cl = box(6.4 - x0, h, CLOUD, fill_opacity=0.05, radius=0.3).move_to([(x0 + 6.4) / 2, cy, 0])
        ct = label("Google Cloud", CAPTION, CLOUD).move_to(cl.get_corner(UP + LEFT), aligned_edge=UP + LEFT) \
            .shift(np.array([0.2, -0.12, 0]))
        self.part("cloud", VGroup(cl, ct))
        self.cloud_frame = cl
        pins = [("pin_global", "global", "Gemini teacher"),
                ("pin_bucket", "gs://<your-bucket>", "your data"),
                ("pin_tune", "us-central1", "tuning job"),
                ("pin_us", "us", "endpoint")]
        self.pins = {}
        ys = np.linspace(cy + h / 2 - 0.95, cy - h / 2 + 0.45, 4)
        for (k, where, what), y in zip(pins, ys):
            d = Dot(radius=0.09, color=CLOUD).move_to([cl.get_left()[0] + 0.3, y, 0])
            w = mono(where, CAPTION, LOOKUP if k == "pin_bucket" else INK)
            t = label(what, CAPTION, CLOUD)
            txt = VGroup(w, t).arrange(DOWN, buff=0.06, aligned_edge=LEFT).next_to(d, RIGHT, buff=0.18)
            g = VGroup(d, txt)
            g.dot, g.where, g.what = d, w, t
            self.pins[k] = g
            self.part(k, g)
        if show is not None:
            for name in list(self.parts):
                if name not in show:
                    _save_op(self.parts[name])
                    _set_op(self.parts[name], 0)
                    self.parts[name].hidden = True

    def row(self, name: str):
        return self._rows[name]

    def _wall(self, which: str):
        f = self.boxes[which].frame
        return np.array([f.get_right()[0], f.get_center()[1], 0])

    def route(self, cmd: str) -> Arrow:
        which, pin = self.ROUTES[cmd]
        return _arrow(self._wall(which), self.pins[pin].dot.get_center() + LEFT * 0.12, LOOKUP, 3.5)

    def blocked(self, cmd: str) -> VGroup:
        which, _ = self.ROUTES[cmd]
        a = self._wall(which)
        stub = Line(a + LEFT * 0.05, a + RIGHT * 0.35, color=LOOKUP, stroke_width=3.5)
        st = stamp("no key", ERR, angle=0.0)
        st.move_to(a + LEFT * (st.width / 2 + 0.12))
        g = VGroup(stub, st)
        g.stub, g.stamp = stub, st
        return g

    def job_arrow(self) -> VMobject:
        a = self.pins["pin_bucket"].dot.get_center()
        b = self.pins["pin_tune"].dot.get_center()
        return _arrow(a + DOWN * 0.1, b + UP * 0.1, LOOKUP, 3).set_stroke(LOOKUP, 3)

    def key_in(self) -> list:
        k = key_glyph(0.26).move_to(self.key_out)
        self.key_solid = k
        return [FadeOut(self.key_out), FadeIn(k)]

    def light(self, name: str, color: str = TURN) -> list:
        m = self.parts[name]
        fr = getattr(m, "frame", None) or (m[0] if isinstance(m[0], VMobject) else m)
        return [Indicate(fr, color=color, scale_factor=1.03)]


# ================================================================== V3 · teacher, mould and bricks (S05, S06)
def brick(scripted: bool = False, w: float = 1.25, text: str = "Q · A") -> VGroup:
    """One {question, answer} brick (BLUE: a model wrote it; scripted=True: BLUE dashed, the
    hand-written stand-in). .frame .text"""
    fr = box(w, 0.42, MODEL, fill_opacity=0.0 if scripted else 0.25, radius=0.06, dashed=scripted)
    t = label(text, CAPTION, INK).move_to(fr)
    g = VGroup(fr, t)
    g.frame, g.text = fr, t
    return _keep(g)


class InstructionCard(VGroup):
    """The lecture's three-part instruction-dataset card (slide 5): rows instruction / context /
    output. .to_pair(scene) plays (1.2 s): the context row and its rule fade, the card closes up, and
    the labels become the tutorial's question / answer (old out, then new in). 4.2 x 1.9.
    .rows .frame .seps"""

    def __init__(self, width: float = 4.2, **kw):
        super().__init__(**kw)
        rows = VGroup(*[label(s, CAPTION, c) for s, c in (("instruction", INK), ("context", S.GREY),
                                                           ("output", INK))]).arrange(DOWN, buff=0.22,
                                                                                     aligned_edge=LEFT)
        fr = box(width, rows.height + 0.6, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.14)
        rows.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.35)
        seps = VGroup(*[Line([fr.get_left()[0] + 0.15, (rows[i].get_bottom()[1] + rows[i + 1].get_top()[1]) / 2, 0],
                             [fr.get_right()[0] - 0.15, (rows[i].get_bottom()[1] + rows[i + 1].get_top()[1]) / 2, 0],
                             color=S.GREY_DARK, stroke_width=2) for i in range(2)])
        self.frame, self.rows, self.seps = fr, rows, seps
        self.add(fr, seps, rows)

    def to_pair(self, scene, run_time: float = 1.2) -> None:
        fr, rows, seps = self.frame, self.rows, self.seps
        pitch = rows[2].get_center()[1] - rows[1].get_center()[1]       # < 0
        q = label("question", CAPTION, INK).move_to(rows[0], aligned_edge=LEFT)
        a = label("answer", CAPTION, INK).move_to(rows[1], aligned_edge=LEFT)
        new_fr = box(fr.width, fr.height + pitch, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.14)
        new_fr.align_to(fr, UP).align_to(fr, LEFT)
        new_sep = seps[0].copy()
        # take everything out of the card: the plays below work on top-level mobjects
        old = [fr, seps[0], seps[1], rows[0], rows[1], rows[2]]
        self.remove(*self.submobjects)
        scene.remove(self)
        scene.add(*old)
        scene.play(FadeOut(rows[1]), FadeOut(seps[1]), FadeOut(rows[0]), FadeOut(rows[2]),
                   Transform(fr, new_fr), run_time=run_time * 0.5)
        scene.play(FadeIn(q), FadeIn(a), run_time=run_time * 0.5)
        scene.remove(fr, seps[0], q, a)
        self.frame, self.rows, self.seps = fr, VGroup(q, a), VGroup(seps[0])
        self.add(fr, self.seps, self.rows)
        scene.add(self)
        del new_sep


class Teacher(Piece):
    """V3 (S05, S06), built in place above a 3-row strip (x -6.4..6.4, y -1.3..2.8): two GREY cards
    on the left (system instruction · cli.py lines 36–145, input prompt · line 169), the BLUE
    teacher (gemini-3.1-flash-lite · global), a mould labelled response_schema, the net labelled
    `except Exception` under it (hidden until shown), and a pile with five batch slots
    (NUM_ITERATIONS = 5) on the right.

    Parts: "cards", "teacher", "mould", "net", "pile". Teacher(show=("cards", "teacher", "mould",
    "pile")) leaves the net hidden; td.reveal(self, "net").
    .pour(scene, i, scripted=False, run_time=0.8) plays: a brick drops from the mould onto slot i
        (returns it; it joins the piece)
    .spark(scene, i, run_time=0.8) plays: a RED spark flies out and is caught in the net (stays);
        returns it
    .exit_label() -> GREY "exit status 0" under the pile (not added)
    .keyerror() -> RED stamp "KeyError: 'question'" on the empty pile (not added)
    .slot(i) -> the point where batch i's brick lands
    """

    def __init__(self, show=None, top: float = 2.8, bottom: float = -1.3, **kw):
        super().__init__(**kw)
        cy = (top + bottom) / 2
        c1 = card_glyph("system instruction", "cli.py · lines 36–145", w=3.4)
        c2 = card_glyph("input prompt", "cli.py · line 169", w=3.4)
        cards = VGroup(c1, c2).arrange(DOWN, buff=0.45).move_to([-4.6, cy + 0.4, 0])
        self.cards = cards
        self.part("cards", cards)
        tb = model_box("teacher", w=2.6, h=1.1, sub=TEACHER)
        tb.move_to([-0.4, cy + 1.0, 0])
        gl = label("location = global", CAPTION, S.GREY).next_to(tb, UP, buff=0.1)
        arrows = VGroup(_arrow(c1.get_right(), tb.frame.get_left() + UP * 0.15, S.GREY, 2.5),
                        _arrow(c2.get_right(), tb.frame.get_left() + DOWN * 0.25, S.GREY, 2.5))
        self.teacher = VGroup(tb, gl, arrows)
        self.teacher_box = tb
        self.part("teacher", self.teacher)
        mtop = tb.frame.get_bottom()[1] - 0.3
        mould = Polygon([-0.9, mtop, 0], [0.9, mtop, 0], [0.35, mtop - 0.9, 0], [-0.35, mtop - 0.9, 0],
                        stroke_color=INK, stroke_width=3).set_fill(S.BG, 1).shift(RIGHT * tb.get_center()[0])
        ml = mono("response_schema", CAPTION, INK).next_to(mould, RIGHT, buff=0.15)
        self.mould_shape = mould
        self.part("mould", VGroup(mould, ml))
        ny = mould.get_bottom()[1] - 0.45
        nx = mould.get_center()[0]
        net = VGroup()
        for k in range(7):
            x = nx - 1.2 + k * 0.4
            net.add(Line([x, ny + 0.18, 0], [x + 0.25, ny - 0.18, 0], color=S.GREY, stroke_width=1.8))
            net.add(Line([x + 0.25, ny + 0.18, 0], [x, ny - 0.18, 0], color=S.GREY, stroke_width=1.8))
        rim = Line([nx - 1.3, ny + 0.2, 0], [nx + 1.35, ny + 0.2, 0], color=S.GREY, stroke_width=3)
        nl = mono("except Exception", CAPTION, S.GREY).next_to(rim, LEFT, buff=0.2)
        self.net_y = ny
        self.part("net", VGroup(net, rim, nl))
        # pile: five slots on a shelf, right
        shelf = Line([2.6, bottom + 0.35, 0], [6.3, bottom + 0.35, 0], color=OWN, stroke_width=4)
        cap = mono("NUM_ITERATIONS = 5", CAPTION, S.GREY).next_to(shelf, UP, buff=1.5).align_to(shelf, RIGHT)
        self.slots = [np.array([2.6 + 0.37 + k * 0.74, bottom + 0.35 + 0.23, 0]) for k in range(5)]
        nums = VGroup(*[label(str(k), CAPTION, S.GREY).move_to(self.slots[k] + DOWN * 0.55) for k in range(5)])
        self.part("pile", VGroup(shelf, cap, nums))
        self.shelf = shelf
        self.bricks = VGroup()
        self.sparks = VGroup()
        self.add(self.bricks, self.sparks)
        if show is not None:
            for name in list(self.parts):
                if name not in show:
                    _save_op(self.parts[name])
                    _set_op(self.parts[name], 0)
                    self.parts[name].hidden = True

    def slot(self, i: int):
        return self.slots[i]

    def pour(self, scene, i: int, scripted: bool = False, run_time: float = 0.8) -> VGroup:
        b = brick(scripted, w=0.66, text="Q·A")
        b.move_to(self.mould_shape.get_bottom() + DOWN * 0.25)
        scene.play(FadeIn(b, shift=DOWN * 0.2), run_time=run_time * 0.3)
        scene.play(b.animate.move_to(self.slot(i)), run_time=run_time * 0.7)
        scene.remove(b)
        self.bricks.add(b)
        return b

    def spark(self, scene, i: int, run_time: float = 0.8) -> VGroup:
        s = spark().move_to(self.mould_shape.get_bottom() + DOWN * 0.15)
        tgt = np.array([self.mould_shape.get_center()[0] - 1.0 + 0.5 * i, self.net_y, 0])
        scene.play(FadeIn(s, scale=0.5), run_time=run_time * 0.25)
        scene.play(s.animate.move_to(tgt), run_time=run_time * 0.75, rate_func=rush_into)
        scene.remove(s)
        self.sparks.add(s)
        return s

    def exit_label(self) -> Text:
        return label("exit status 0", CAPTION, S.GREY).next_to(self.shelf, DOWN, buff=0.55)

    def keyerror(self) -> VGroup:
        st = stamp("KeyError: 'question'", ERR, angle=0.06)
        return st.move_to([self.shelf.get_center()[0], self.shelf.get_center()[1] + 0.85, 0])


# ================================================================== V4 · one pair, five shapes (S06, S07, S12)
STATIONS = ("instruct-dataset.csv", "train.csv", "train.jsonl", "chat template", "tokens")


class Conveyor(VGroup):
    """V4: a belt with labelled station slots (mono names under the belt). Built centred at ORIGIN,
    `width` wide; the belt sits at y = 0 before you move it.

        cv = Conveyor(STATIONS[:3])               # stations 1-3 (S06/S07)
        card = shape_card([...]); cv.put(i, card) # place a card above station i (returns it)
        self.play(cv.light(i))                    # station i lights YELLOW
        self.play(*cv.carry(mob, i))              # move a brick / card to above station i
    .belt .marks .labels .slot(i) (point on the belt over station i)
    """

    def __init__(self, stations=STATIONS[:3], width: float = 12.0, color: str = S.GREY, **kw):
        super().__init__(**kw)
        n = len(stations)
        self.belt = Line([-width / 2, 0, 0], [width / 2, 0, 0], color=color, stroke_width=5)
        rollers = VGroup(*[Circle(radius=0.08, stroke_color=color, stroke_width=2).move_to([x, -0.14, 0])
                           for x in np.linspace(-width / 2 + 0.2, width / 2 - 0.2, 14)])
        self.xs = list(np.linspace(-width / 2 + width / (2 * n), width / 2 - width / (2 * n), n))
        self.marks = VGroup(*[Line([x, 0.08, 0], [x, -0.08, 0], color=INK, stroke_width=3) for x in self.xs])
        self.labels = VGroup(*[mono(s, CAPTION, OWN if s.endswith((".csv", ".jsonl")) else INK)
                               .move_to([x, -0.5, 0]) for s, x in zip(stations, self.xs)])
        self.add(self.belt, rollers, self.marks, self.labels)

    def slot(self, i: int):
        return np.array([self.xs[i], self.belt.get_center()[1], 0]) + RIGHT * self.belt.get_center()[0] * 0

    @staticmethod
    def _clamp(x: float, w: float) -> float:
        """Centre x moved so a mobject `w` wide stays inside x in [-6.5, 6.5]."""
        return float(min(max(x, -6.5 + w / 2), 6.5 - w / 2))

    def put(self, i: int, mob, buff: float = 0.2):
        """Place mob above station i, standing `buff` over the belt (kept inside the frame)."""
        x = self._clamp(self.marks[i].get_center()[0], mob.width)
        mob.move_to([x, self.belt.get_center()[1] + buff + mob.height / 2, 0])
        return mob

    def carry(self, mob, i: int, buff: float = 0.2) -> list:
        x = self._clamp(self.marks[i].get_center()[0], mob.width)
        return [mob.animate.move_to([x, self.belt.get_center()[1] + buff + mob.height / 2, 0])]

    def light(self, i: int, color: str = TURN):
        return AnimationGroup(self.labels[i].animate.set_color(color), self.marks[i].animate.set_color(color))


def shape_card(lines, color: str = OWN, header: str | None = None, size: float = CAPTION,
               dashed: bool = False) -> VGroup:
    """One shape of the pair: mono rows (persona masked) in a card of `color` (GREEN: your file;
    BLUE dashed + scripted for the stand-in), optional GREY header. .frame .rows .header"""
    g = json_card(lines, color, size, header)
    if dashed:
        d = box(g.frame.width, g.frame.height, color, dashed=True).move_to(g.frame)
        g.remove(g.frame)
        g.add_to_back(d)
        g.frame = d
    return g


def splitter(n_train: int = 17, n_test: int = 2, w: float = 2.6) -> VGroup:
    """The 90/10 splitter of --prepare: a fork from one input point into two GREEN bins
    "train.jsonl · 17" and "test.jsonl · 2" (the counts from dataset-creator/10), a GREY "90 / 10"
    left of the fork. 4.6 x 1.6. .bins .fork .input_point()"""
    a = ORIGIN
    up = np.array([w * 0.5, 0.6, 0])
    dn = np.array([w * 0.5, -0.6, 0])
    fork = VGroup(Line(a, a + RIGHT * 0.5, color=S.GREY, stroke_width=3),
                  _arrow(a + RIGHT * 0.5, up, S.GREY, 3), _arrow(a + RIGHT * 0.5, dn, S.GREY, 3))
    b1 = chip(f"train.jsonl · {n_train}", OWN, size=CAPTION, font=MONO).next_to(up, RIGHT, buff=0.1)
    b2 = chip(f"test.jsonl · {n_test}", OWN, size=CAPTION, font=MONO).next_to(dn, RIGHT, buff=0.1)
    ratio = label("90 / 10", CAPTION, S.GREY).next_to(fork[0], LEFT, buff=0.15)
    g = VGroup(fork, b1, b2, ratio)
    g.bins, g.fork = VGroup(b1, b2), fork
    g.input_point = lambda: fork[0].get_start()
    return g


class ChatRibbon(VGroup):
    """V4 station 4-5 (S12): Qwen3's chat template as a ribbon of segments: the markers
    (<|im_start|>user, <|im_end|>, <|im_start|>assistant, <think></think> …) bright YELLOW-outlined
    chips, the text pieces GREY-outlined chips (pass short excerpts of c63's lines). rows: list of
    rows, each a list of (text, is_marker). .tokenize() -> anims (each chip becomes a row of token
    cells, no numbers: illustration); .sweep(run_time) -> anim (a YELLOW highlighter crosses every
    token, question included: loss on all tokens). .chips .cells"""

    def __init__(self, rows, size: float = CAPTION, max_w: float = 12.4, **kw):
        super().__init__(**kw)
        lines = VGroup()
        self.chips = []
        for row in rows:
            r = VGroup()
            for text, marker in row:
                c = chip(unname(text), TURN if marker else S.GREY, size=size, font=MONO,
                         fill_opacity=0.18 if marker else 0.06)
                if any(m in c.text.text for m in MASKS):
                    new = mtext(text, size, INK).move_to(c.text)
                    c.remove(c.text)
                    c.add(new)
                    c.text = new
                c.marker = marker
                c.src_text = unname(text)
                r.add(c)
                self.chips.append(c)
            r.arrange(RIGHT, buff=0.06)
            lines.add(r)
        lines.arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        if lines.width > max_w:
            raise ValueError(f"ChatRibbon {lines.width:.1f} wide (> {max_w}): shorten the pieces or add a row")
        self.lines = lines
        self.cells = VGroup()
        self.add(lines)

    def tokenize(self, run_time: float = 1.2) -> list:
        """Animations: every chip becomes a strip of small token cells (about one per 4 characters)
        of its own width; .cells holds them afterwards."""
        anims = []
        for c in self.chips:
            n = max(1, round(len(c.src_text) / 4))
            w = c.width
            cw = (w - 0.04 * (n - 1)) / n
            strip = VGroup(*[Rectangle(width=cw, height=0.3, stroke_width=1.5,
                                       stroke_color=TURN if c.marker else S.GREY)
                             .set_fill(TURN if c.marker else S.GREY, 0.3) for _ in range(n)])
            strip.arrange(RIGHT, buff=0.04).move_to(c)
            self.cells.add(strip)
            anims.append(Transform(c, strip))
        return [AnimationGroup(*anims, run_time=run_time)]

    def sweep(self, run_time: float = 2.0):
        """Animation: a YELLOW translucent highlighter bar sweeps each row left to right (returned
        as one Succession; the bar is left at the end of the last row: FadeOut ribbon.highlighter)."""
        rows = list(self.lines)
        hl = Rectangle(width=0.35, height=rows[0].height + 0.16, stroke_width=0).set_fill(TURN, 0.35)
        hl.move_to(rows[0].get_left() + RIGHT * 0.17)
        self.highlighter = hl
        steps = [FadeIn(hl, run_time=0.2)]
        for k, r in enumerate(rows):
            if k:
                steps.append(hl.animate(run_time=0.1).move_to(r.get_left() + RIGHT * 0.17))
            steps.append(hl.animate(run_time=run_time / len(rows), rate_func=linear)
                         .stretch_to_fit_width(r.width + 0.1).move_to(r))
            steps.append(hl.animate(run_time=0.05).stretch_to_fit_width(0.35).move_to(r.get_right()))
        return Succession(*steps)


# ================================================================== V5 · the memory column (S10, S14, S16)
class MemoryColumn(VGroup):
    """V5: a GPU-memory column, blocks stacked from the bottom in proportion (`scale` units per GB).
    blocks: list of (name, gb, colour, dtype[, frozen]) bottom to top — dtype a small white tag
    ("FP16", drawn when the block is >= 0.45 tall) or None; frozen=True adds a snowflake. total: the
    outline height in GB (a GREY dashed box above the blocks when they don't sum to it: the
    lecture's ~40 / ~12 GB are not itemized) and total_label under it ("120 GB"); title above.
    labels=True puts each block's name right of the column (leaders when moved); labels=False keeps
    the column bare (the ladder).

        full = ladder_column("full")
        self.play(*full.restack({"Gradients (FP16)": 0.5, "Optimizer states (FP32)": 0.5}))
    .blocks {name: Rectangle} .parts {name: VGroup(rect, tag, flake)} .tags {name: Text}
    .outline .total .heading .stack"""

    MIN_H = 0.12

    def __init__(self, blocks, total: float | None = None, total_label: str | None = None,
                 title: str | None = None, scale: float = 0.035, col_w: float = 1.4,
                 labels: bool = True, size: float = CAPTION, **kw):
        super().__init__(**kw)
        self.scale_k, self.col_w, self.size, self.labelled = scale, col_w, size, labels
        self.blocks, self.parts, self.tags, self.leads = {}, {}, {}, {}
        self.order = []
        self.stack = VGroup()
        y = 0.0
        for b in blocks:
            name, gb, color, dtype = b[:4]
            frozen = len(b) > 4 and b[4]
            h = max(self.MIN_H, gb * scale)
            r = Rectangle(width=col_w, height=h, stroke_color=color, stroke_width=2.5).set_fill(color, 0.35)
            r.move_to([0, y + h / 2, 0])
            r.gb = gb
            y += h
            g = VGroup(r)
            if frozen:
                fl = snowflake(min(0.16, h * 0.35))
                fl.move_to(r.get_corner(UP + LEFT) + np.array([0.22, -min(0.22, h / 2), 0]))
                g.add(fl)
            if dtype and h >= 0.45:
                g.add(dtype_tag(dtype).move_to(r))
            self.blocks[name], self.parts[name] = r, g
            self.order.append(name)
            self.stack.add(g)
        self.add(self.stack)
        if labels:
            for name in self.order:
                t = label(name, size, INK)
                self.tags[name] = t
                self.add(t)
            for name, t in self._label_spots().items():
                self.tags[name].move_to(t)
                lead = Line(self.blocks[name].get_right(), self.tags[name].get_left() + LEFT * 0.05,
                            color=S.GREY, stroke_width=1.5)
                self.leads[name] = lead
                self.add(lead)
        top = y
        self.outline = None
        if total is not None and total * scale > y + 0.01:
            top = total * scale
            o = DashedVMobject(Rectangle(width=col_w, height=top - y), num_dashes=24, dashed_ratio=0.5)
            o.set_stroke(S.GREY, 2).move_to([0, (y + top) / 2, 0])
            self.outline = o
            self.add(o)
        self.top_y = top
        self.total = None
        if total_label:
            self.total = label(total_label, 26, INK).move_to([0, -0.35, 0])
            self.add(self.total)
        self.heading = None
        if title:
            self.heading = label(title, size, S.GREY).move_to([0, top + 0.3, 0])
            self.add(self.heading)

    def _label_spots(self, heights: dict | None = None) -> dict:
        """Label centres right of the column for the given block heights (bottom to top, no overlap)."""
        heights = heights or {n: self.blocks[n].height for n in self.order}
        base = self.blocks[self.order[0]].get_bottom()[1]
        x0 = self.blocks[self.order[0]].get_right()[0] + 0.35
        out, y, last = {}, base, -1e9
        for n in self.order:
            t = self.tags[n]
            cy = max(y + heights[n] / 2, last + 0.06 + t.height / 2)
            out[n] = np.array([x0 + t.width / 2, cy, 0])
            last = cy + t.height / 2
            y += heights[n]
        return out

    def restack(self, gbs: dict, run_time: float = 1.0) -> list:
        """Animations: the named blocks change to their new sizes in GB (the others keep theirs),
        everything above moves with them, labels and leaders follow. One play."""
        heights = {n: (max(self.MIN_H, gbs[n] * self.scale_k) if n in gbs else self.blocks[n].height)
                   for n in self.order}
        anims = []
        y = self.blocks[self.order[0]].get_bottom()[1]
        for n in self.order:
            r, g = self.blocks[n], self.parts[n]
            tgt = r.copy().stretch_to_fit_height(heights[n]).move_to([r.get_center()[0], y + heights[n] / 2, 0])
            anims.append(Transform(r, tgt, run_time=run_time))
            for m in g[1:]:
                if heights[n] < 0.45 and m is not g[0]:
                    anims.append(m.animate(run_time=run_time).set_opacity(0))
                else:
                    anims.append(m.animate(run_time=run_time).shift(tgt.get_center() - r.get_center()))
            if n in gbs:
                r.gb = gbs[n]
            y += heights[n]
        if self.labelled:
            spots = self._label_spots(heights)
            y = self.blocks[self.order[0]].get_bottom()[1]
            for n in self.order:
                t = self.tags[n]
                anims.append(t.animate(run_time=run_time).move_to(spots[n]))
                end = np.array([self.blocks[n].get_right()[0], y + heights[n] / 2, 0])
                anims.append(self.leads[n].animate(run_time=run_time).put_start_and_end_on(
                    end, spots[n] + LEFT * (t.width / 2 + 0.05)))
                y += heights[n]
        if self.outline is not None or self.heading is not None:
            top = max(y, self.top_y if self.outline is not None else y)
            if self.heading is not None:
                anims.append(self.heading.animate(run_time=run_time).move_to(
                    [self.heading.get_center()[0], top + 0.3, 0]))
        return anims

    def shrink(self, name: str, gb: float, run_time: float = 1.0) -> list:
        """restack({name: gb}) (one block; for several at once use restack)."""
        return self.restack({name: gb}, run_time)


LADDER = {
    # lecture slides 14 (10 B model): FP16 params and grads, FP32 Adam momentum + variance
    # (bottom to top; parameters GREY, gradients YELLOW like the backward pulse, Adam states PURPLE)
    "full": [("Parameters (FP16)", 20, S.GREY, "FP16"),
             ("Gradients (FP16)", 20, PULSE, "FP16"),
             ("Optimizer states (FP32)", 80, S.PURPLE, "FP32")],
    # slides 37-39: the 20 GB base stays (frozen, needed for the forward pass); A and B are small
    "lora": [("Base model (FP16)", 20, FROZEN, "FP16", True), ("A, B + their states", 0.5, OWN, None)],
    # slide 72: the base in 4 bits (~5 GB for 10 B), adapters, optimizer pages that can go to the CPU
    "qlora": [("Base model (NF4)", 5, FROZEN, "NF4", True), ("A, B + their states", 0.5, OWN, None)],
}
LADDER_TOTALS = {"full": (120, "120 GB"), "lora": (40, "~40 GB"), "qlora": (12, "~12 GB")}
LADDER_TITLES = {"full": "full fine-tuning", "lora": "LoRA", "qlora": "QLoRA"}


def ladder_column(kind: str, labels: bool = True, scale: float = 0.035, **kw) -> MemoryColumn:
    """The lecture's column for a 10 B model: kind "full" (20 + 20 + 80 = 120 GB), "lora" (the 20 GB
    base + A/B, outline to ~40 GB: the rest is not itemized on the slides), "qlora" (NF4 base ~5 GB
    + A/B, outline to ~12 GB). Tag it concept_tag() (lecture-only scale)."""
    tot, tl = LADDER_TOTALS[kind]
    return MemoryColumn(LADDER[kind], total=tot, total_label=tl, title=LADDER_TITLES[kind], labels=labels,
                        scale=scale, **kw)


def memory_ladder(scale: float = 0.035, gap: float = 1.6) -> VGroup:
    """The three columns side by side, bare (no block labels), totals under them, GREY arrows
    between: 120 -> ~40 -> ~12 GB. 8.0 x 4.9 at the default scale. .cols {"full", "lora", "qlora"}"""
    cols = {k: ladder_column(k, labels=False, scale=scale) for k in ("full", "lora", "qlora")}
    row = VGroup(*cols.values()).arrange(RIGHT, buff=gap, aligned_edge=DOWN)
    arrows = VGroup(*[_arrow(cols[a].total.get_right() + RIGHT * 0.15, cols[b].total.get_left() + LEFT * 0.15,
                             S.GREY, 2.5) for a, b in (("full", "lora"), ("lora", "qlora"))])
    g = VGroup(row, arrows)
    g.cols, g.arrows = cols, arrows
    return g.move_to(ORIGIN)


def gpu_tiles(n: int = 5, gb: float = 24, scale: float = 0.035, w: float = 1.6) -> VGroup:
    """n GREY dashed GPU tiles of `gb` each, stacked from y = 0 (to stand beside a MemoryColumn at
    the same scale), each labelled "24 GB" inside. Lecture-only scale: add concept_tag()."""
    g = VGroup()
    for k in range(n):
        r = DashedVMobject(Rectangle(width=w, height=gb * scale - 0.06), num_dashes=26, dashed_ratio=0.55)
        r.set_stroke(S.GREY, 2).move_to([0, k * gb * scale + gb * scale / 2, 0])
        t = label(f"{gb:g} GB", CAPTION, S.GREY).move_to(r)
        g.add(VGroup(r, t))
    return g


# ================================================================== V6 · buckets (S11)
class NumberRow(VGroup):
    """A number line from lo to hi, `width` wide, centred at ORIGIN, GREY ticks every `step` with
    labels every `label_every` ticks. .x(v) -> point on the line; .dot(v, text=None, colour) ->
    a dot (and mono label above) at v (not added); .snap(dots, values) -> anims moving each dot (and
    its label: text swaps) to new values."""

    def __init__(self, lo: float = 0, hi: float = 100, width: float = 11.0, step: float = 10,
                 label_every: int = 1, size: float = CAPTION, color: str = S.GREY, **kw):
        super().__init__(**kw)
        self.lo, self.hi, self.line_w = lo, hi, width
        self.axis = Line(LEFT * width / 2, RIGHT * width / 2, color=color, stroke_width=3)
        self.ticks = VGroup()
        k = 0
        v = lo
        while v <= hi + 1e-9:
            x = self.x(v)[0]
            t = VGroup(Line([x, -0.1, 0], [x, 0.1, 0], color=color, stroke_width=2))
            if k % label_every == 0:
                t.add(mono(f"{v:g}", size, color).move_to([x, -0.38, 0]))
            self.ticks.add(t)
            v += step
            k += 1
        self.add(self.axis, self.ticks)

    def x(self, v: float):
        left = self.axis.get_start()
        return left + RIGHT * (v - self.lo) / (self.hi - self.lo) * self.line_w

    def dot(self, v: float, text: str | None = None, color: str = MODEL, size: float = CAPTION) -> VGroup:
        d = Dot(self.x(v) + UP * 0.0, radius=0.1, color=color)
        g = VGroup(d)
        g.dot, g.text, g.value = d, None, v
        if text is not None:
            t = mono(text, size, color).next_to(d, UP, buff=0.18)
            g.add(t)
            g.text = t
        return g

    def snap(self, dots, values, fmt: str = "{:g}", run_time: float = 0.8) -> list:
        anims = []
        for g, v in zip(dots, values):
            shift = self.x(v) - g.dot.get_center()
            shift[1] = 0
            anims.append(g.dot.animate(run_time=run_time).shift(shift))
            if g.text is not None:
                new = mono(fmt.format(v), CAPTION, g.dot.get_color()).next_to(g.dot.get_center() + shift, UP, buff=0.18)
                anims.append(AnimationGroup(*_swap_text(g, g.text, new), run_time=run_time))
                g.text = new
            g.value = v
        return anims


class AbsmaxRow(VGroup):
    """V6 (b), slides 45–51 corrected: three rows of ten cells. Row 1: X (FP32) = 1.5 … 10.2;
    row 2: round(c · X) with c = 127 / 10.2 = 12.4509 -> 19, 29, 46, 51, 70, 85, 98, 105, 115, 127
    (computed here, rounded, never floored); row 3: dequantized values / c (3 decimals). Built
    centred: 12.2 wide, 3.3 tall. .x_cells .q_cells .d_cells (each VGroup of VGroup(box, text)), .c_chip
    (GOLD-free white chip "c = 127 / 10.2 = 12.4509"), .q (ints), .dq (floats).
    .errors(idx=(0, 4)) -> VGroup of RED rings around the dequantized cells that differ (not added).
    Reveal rows with FadeIn / TransformFromCopy(x_cells, q_cells)."""

    def __init__(self, values=ABSMAX_X, cell_w: float = 1.05, size: float = CAPTION, **kw):
        super().__init__(**kw)
        amax = max(abs(v) for v in values)
        self.c = 127 / amax
        self.q = [int(np.floor(v * self.c + 0.5)) for v in values]
        self.dq = [q / self.c for q in self.q]

        def row(texts, color):
            cells = VGroup()
            for s in texts:
                b = Rectangle(width=cell_w, height=0.55, stroke_color=color, stroke_width=2).set_fill(color, 0.08)
                cells.add(VGroup(b, mono(s, size, INK).move_to(b)))
            return cells.arrange(RIGHT, buff=0.0)

        self.x_cells = row([f"{v:g}" for v in values], MODEL)
        self.q_cells = row([str(q) for q in self.q], OWN)
        self.d_cells = row([f"{d:.3f}" for d in self.dq], S.GREY)
        names = [label("X (FP32)", size, S.GREY), label("Int8", size, S.GREY), label("back / c", size, S.GREY)]
        rows = VGroup(self.x_cells, self.q_cells, self.d_cells).arrange(DOWN, buff=0.55)
        for nm, r in zip(names, rows):
            nm.next_to(r, LEFT, buff=0.2)
        self.names = VGroup(*names)
        c4 = np.floor(self.c * 1e4) / 1e4          # 12.4509 as the lecture writes it (4 decimals, cut)
        self.c_chip = chip(f"c = 127 / {amax:g} = {c4:.4f}", INK, size=size, font=MONO)
        self.c_chip.next_to(rows, UP, buff=0.3)
        self.add(rows, self.names, self.c_chip)
        self.move_to(ORIGIN)

    def errors(self, idx=(0, 4)) -> VGroup:
        return VGroup(*[ring(self.d_cells[i], ERR, buff=0.04) for i in idx])


class BlockRow(Piece):
    """V6 (c) + (e): a long row of weights (thin GREY bars, one RED outlier) split into `n_blocks`
    blocks, each with its own small absmax knob (a white circle) above it. Built centred: `width`
    wide, 1.65 tall; separators and knobs are hidden parts until .split().
    .split() -> anims (separators and knobs appear); .quantize_knobs() -> anims (double
    quantization: every knob becomes a smaller square). .bars .outlier .seps .knobs"""

    def __init__(self, n_blocks: int = 4, per: int = 12, width: float = 11.0, outlier: int = 5, **kw):
        super().__init__(**kw)
        rng = np.random.default_rng(4)
        n = n_blocks * per
        bw = width / n
        self.bars = VGroup()
        for k in range(n):
            h = 1.1 if k == outlier else float(abs(rng.normal(0, 0.25))) + 0.05
            b = Rectangle(width=bw * 0.7, height=h, stroke_width=0).set_fill(ERR if k == outlier else S.GREY, 0.8)
            b.move_to([-width / 2 + bw * (k + 0.5), h / 2, 0])
            self.bars.add(b)
        self.outlier = self.bars[outlier]
        self.base = Line([-width / 2, 0, 0], [width / 2, 0, 0], color=S.GREY, stroke_width=2)
        self.part("row", VGroup(self.base, self.bars))
        self.seps = VGroup(*[DashedLine([-width / 2 + k * per * bw, -0.15, 0], [-width / 2 + k * per * bw, 1.3, 0],
                                        color=INK, stroke_width=2) for k in range(1, n_blocks)])
        self.knobs = VGroup(*[Circle(radius=0.14, stroke_color=INK, stroke_width=2.5).set_fill(INK, 0.3)
                              .move_to([-width / 2 + (k + 0.5) * per * bw, 1.5, 0]) for k in range(n_blocks)])
        self.part("seps", self.seps, shown=False)
        self.part("knobs", self.knobs, shown=False)
        self.move_to(ORIGIN)

    def split(self) -> list:
        return self.parts_in("seps", "knobs")

    def quantize_knobs(self) -> list:
        return [Transform(k, Rectangle(width=0.16, height=0.16, stroke_color=INK, stroke_width=2.5)
                          .set_fill(INK, 0.3).move_to(k)) for k in self.knobs]


class NF4Bell(Piece):
    """V6 (d), slides 54–55: a bell-shaped weight histogram (a smooth GREY curve over [-1, 1]) and 16
    vertical YELLOW level lines (a hidden part). .even() -> anims: the 16 lines appear evenly spaced;
    .to_nf4() -> anims sliding them to NF4's quantile positions (crowded near 0); .weights(n) ->
    VGroup of BLUE dots on the axis (deterministic, not added); .snap(dots) -> anims moving each dot
    onto its nearest NF4 line. Built centred: `width` x (`height` + 0.5). .curve .axis .lines .x(v)"""

    def __init__(self, width: float = 10.0, height: float = 2.6, **kw):
        super().__init__(**kw)
        self.w, self.h = width, height
        self.axis = Line([-width / 2, 0, 0], [width / 2, 0, 0], color=S.GREY, stroke_width=2)
        xs = np.linspace(-1, 1, 81)
        pts = [np.array([v * width / 2, height * np.exp(-(v / 0.4) ** 2 / 2), 0]) for v in xs]
        self.curve = VMobject(stroke_color=S.GREY, stroke_width=3).set_points_smoothly(pts)
        ends = VGroup(*[mono(t, CAPTION, S.GREY).move_to([v * width / 2, -0.3, 0])
                        for t, v in (("-1", -1), ("0", 0), ("1", 1))])
        self.part("bell", VGroup(self.axis, self.curve, ends))
        self.lines = VGroup(*[Line([v * width / 2, 0, 0], [v * width / 2, height * 1.05, 0], color=TURN,
                                   stroke_width=2) for v in np.linspace(-1, 1, 16)])
        self.part("lines", self.lines, shown=False)
        self.move_to(ORIGIN)

    def x(self, v: float):
        return self.axis.get_center() + RIGHT * v * self.w / 2

    def even(self) -> list:
        return self.parts_in("lines")

    def to_nf4(self, run_time: float = 1.5) -> list:
        return [ln.animate(run_time=run_time).set_x(self.x(v)[0]) for ln, v in zip(self.lines, NF4_LEVELS)]

    def weights(self, n: int = 14, seed: int = 5) -> VGroup:
        rng = np.random.default_rng(seed)
        vals = np.clip(rng.normal(0, 0.4, n), -0.98, 0.98)
        g = VGroup(*[Dot(self.x(float(v)) + UP * 0.12, radius=0.07, color=MODEL) for v in vals])
        g.values = [float(v) for v in vals]
        return g

    def snap(self, dots, run_time: float = 1.0) -> list:
        anims = []
        for d, v in zip(dots, dots.values):
            q = min(NF4_LEVELS, key=lambda L: abs(L - v))
            anims.append(d.animate(run_time=run_time).set_x(self.x(q)[0]).set_color(TURN))
        return anims


def inflate_pair(w4: float = 0.9, w16: float = 2.4, h: float = 1.2) -> VGroup:
    """V6 (f), slides 68–69: a small GREY block tagged NF4 (stored) and a big GREY dashed block
    tagged FP16 (computed, for one matrix multiply). Animate with TransformFromCopy(small, big) and
    back. .small .big (each VGroup(rect, tag))"""
    s = VGroup(Rectangle(width=w4, height=h * 0.5, stroke_color=FROZEN, stroke_width=2.5).set_fill(FROZEN, 0.35))
    s.add(dtype_tag("NF4").next_to(s[0], DOWN, buff=0.1))
    big = VGroup(Rectangle(width=w16, height=h, stroke_color=FROZEN, stroke_width=2.5).set_fill(FROZEN, 0.2))
    big.add(dtype_tag("FP16").move_to(big[0]))
    g = VGroup(s, big).arrange(RIGHT, buff=1.0)
    g.small, g.big = s, big
    return g


# ================================================================== V7 · the LoRA block (S13, S14, S16)
def cell_grid(rows: int, cols: int, cell: float = 0.3, color: str = FROZEN, fill: float = 0.3) -> VGroup:
    """A rows x cols grid of square cells (the lecture's counted cells, slides 23–25)."""
    g = VGroup(*[Rectangle(width=cell, height=cell, stroke_color=color, stroke_width=2).set_fill(color, fill)
                 for _ in range(rows * cols)])
    return g.arrange_in_grid(rows, cols, buff=0.0)


def rank_product(n: int = 5, r: int = 1, cell: float = 0.3) -> VGroup:
    """Slides 23–25: "W (n x n) = B (n x r) · A (r x n)": a GREY n x n grid "= " a GREEN n x r grid
    "·" a GREEN r x n grid, with counts under each (25 = 5 + 5 -> 10 numbers at r = 1; 20 at r = 2).
    .w .b .a .counts"""
    w = cell_grid(n, n, cell, FROZEN)
    b = cell_grid(n, r, cell, OWN)
    a = cell_grid(r, n, cell, OWN)
    eq, dot = label("=", 30, INK), label("·", 36, INK)
    row = VGroup(w, eq, b, dot, a).arrange(RIGHT, buff=0.3)
    cw = label(f"{n * n}", CAPTION, S.GREY).next_to(w, DOWN, buff=0.15)
    cb = label(f"{n * r}", CAPTION, S.GREY).next_to(b, DOWN, buff=0.15).align_to(cw, DOWN)
    ca = label(f"{r * n}", CAPTION, S.GREY).next_to(a, DOWN, buff=0.15).align_to(cw, DOWN)
    tot = label(f"= {n * r + r * n} numbers", CAPTION, OWN).next_to(VGroup(cb, ca), RIGHT, buff=0.3)
    g = VGroup(row, cw, cb, ca, tot)
    g.w, g.b, g.a, g.counts = w, b, a, VGroup(cw, cb, ca, tot)
    return g.move_to(ORIGIN)


def real_size(scale: float = 1.0 / 680) -> VGroup:
    """V7 at real proportions: q_proj as a GREY 2048 x 1024 rectangle (2,097,152) beside two thin
    GREEN strips 2048 x 8 and 8 x 1024 (24,576); the strips get a 0.06 minimum thickness (drawn
    thicker than true: say so). Counts in mono under each. .w .b .a"""
    W = Rectangle(width=HIDDEN * scale, height=Q_OUT * scale, stroke_color=FROZEN, stroke_width=2.5).set_fill(FROZEN, 0.25)
    B = Rectangle(width=max(0.06, LORA_R * scale), height=Q_OUT * scale, stroke_color=OWN, stroke_width=2).set_fill(OWN, 0.6)
    A = Rectangle(width=HIDDEN * scale, height=max(0.06, LORA_R * scale), stroke_color=OWN, stroke_width=2).set_fill(OWN, 0.6)
    pair = VGroup(B, A).arrange(RIGHT, buff=0.3, aligned_edge=UP)
    row = VGroup(W, pair).arrange(RIGHT, buff=1.2, aligned_edge=UP)
    tw = VGroup(mono("q_proj  2048 × 1024", CAPTION, INK), mono(f"{Q_OUT * HIDDEN:,}", CAPTION, S.GREY)) \
        .arrange(DOWN, buff=0.08).next_to(W, DOWN, buff=0.2)
    tp = VGroup(mono("B 2048 × 8 · A 8 × 1024", CAPTION, OWN),
                mono(f"{LORA_R * (Q_OUT + HIDDEN):,}", CAPTION, S.GREY)).arrange(DOWN, buff=0.08)
    tp.next_to(pair, DOWN, buff=0.2).align_to(pair, LEFT)
    g = VGroup(row, tw, tp)
    g.w, g.b, g.a = W, B, A
    return g.move_to(ORIGIN)


class LoraEquation(VGroup):
    """The equation of slide 26 as separate symbols so each can light as it is named:
    "W₀ + ΔW = W₀ + (α/r) · B · A". .sym(name) for name in "W0", "dW", "W0b", "alpha", "r", "B", "A"
    (the second W₀ is "W0b"); .light(name, colour) -> anim. 30 pt serif."""

    PIECES = (("W0", "W₀"), (None, "+"), ("dW", "ΔW"), (None, "="), ("W0b", "W₀"), (None, "+"),
              (None, "("), ("alpha", "α"), (None, "/"), ("r", "r"), (None, ")"), (None, "·"), ("B", "B"),
              (None, "·"), ("A", "A"))

    def __init__(self, size: float = 34, **kw):
        super().__init__(**kw)
        self._sym = {}
        colors = {"W0": FROZEN, "W0b": FROZEN, "B": OWN, "A": OWN, "dW": OWN}
        for key, s in self.PIECES:
            t = label(s, size, colors.get(key, INK))
            if key:
                self._sym[key] = t
            self.add(t)
        self.arrange(RIGHT, buff=0.12)

    def sym(self, name: str):
        return self._sym[name]

    def light(self, name: str, color: str = TURN):
        return Indicate(self._sym[name], color=color, scale_factor=1.25)


class LoraBlock(Piece):
    """V7's block diagram (slide 28), built centred at ORIGIN, 6.0 x 4.6: input `x` at the bottom,
    the GREY frozen W₀ (with a snowflake, "frozen") on the left, the GREEN A -> B hourglass on the
    right (A wide -> r narrow -> B wide; "A random", "B = 0" labels; the width r in the middle), a ⊕
    above both and the output `h` at the top. Parts: "x", "w0", "ab", "sum", "h", "notes" (the A/B
    labels). LoraBlock(show=...) as Piece.
    .forward() -> anims: both branches light YELLOW from x to h (the forward pass)
    .backward(run_time) -> list of Successions: a YELLOW pulse runs down from h, through W₀ (which
        greys further, unchanged) and into B and A (which glow GREEN)
    .merge_into(target) -> anims: a copy of the hourglass slides onto `target` (a fresh FP16 W₀
        copy) and fuses into it (S16)
    .w0 .a .b .x_node .h_node .plus"""

    def __init__(self, show=None, **kw):
        super().__init__(**kw)
        xn = VGroup(Circle(radius=0.28, stroke_color=INK, stroke_width=2.5).set_fill(S.BG, 1))
        xn.add(label("x", 28, INK).move_to(xn[0]))
        xn.move_to([0, -2.0, 0])
        self.x_node = xn
        self.part("x", xn)
        w0 = Rectangle(width=2.2, height=1.6, stroke_color=FROZEN, stroke_width=3).set_fill(FROZEN, 0.25)
        w0.move_to([-1.6, 0, 0])
        w0t = label("W₀", 30, INK).move_to(w0)
        sf = snowflake(0.18).move_to(w0.get_corner(UP + RIGHT) + np.array([-0.3, -0.3, 0]))
        frozen = label("frozen", CAPTION, S.GREY).next_to(w0, LEFT, buff=0.15)
        self.w0 = w0
        self.part("w0", VGroup(w0, w0t, sf, frozen))
        cx = 1.6
        A = Polygon([cx - 1.0, -0.85, 0], [cx + 1.0, -0.85, 0], [cx + 0.25, -0.1, 0], [cx - 0.25, -0.1, 0],
                    stroke_color=OWN, stroke_width=3).set_fill(OWN, 0.3)
        B = Polygon([cx - 0.25, 0.1, 0], [cx + 0.25, 0.1, 0], [cx + 1.0, 0.85, 0], [cx - 1.0, 0.85, 0],
                    stroke_color=OWN, stroke_width=3).set_fill(OWN, 0.3)
        at = label("A", 28, INK).move_to(A).shift(DOWN * 0.15)
        bt = label("B", 28, INK).move_to(B).shift(UP * 0.15)
        rt = label("r", CAPTION, OWN).move_to([cx - 0.62, 0, 0])
        self.a, self.b = A, B
        self.part("ab", VGroup(A, B, at, bt, rt))
        na = label("A random", CAPTION, S.GREY).next_to(A, RIGHT, buff=0.15)
        nb = label("B = 0", CAPTION, S.GREY).next_to(B, RIGHT, buff=0.15)
        self.part("notes", VGroup(na, nb))
        plus = VGroup(Circle(radius=0.22, stroke_color=INK, stroke_width=2.5).set_fill(S.BG, 1))
        plus.add(label("+", 28, INK).move_to(plus[0]))
        plus.move_to([0, 1.55, 0])
        self.plus = plus
        self.part("sum", plus)
        hn = VGroup(Circle(radius=0.28, stroke_color=INK, stroke_width=2.5).set_fill(S.BG, 1))
        hn.add(label("h", 28, INK).move_to(hn[0]))
        hn.move_to([0, 2.3, 0])
        self.h_node = hn
        self.part("h", hn)
        # wires
        self.w_in_l = _poly([xn.get_top(), [0, -1.35, 0], [-1.6, -1.35, 0], w0.get_bottom()], S.GREY, 2.5)
        self.w_in_r = _poly([[0, -1.35, 0], [cx, -1.35, 0], A.get_bottom()], S.GREY, 2.5)
        self.w_out_l = _poly([w0.get_top(), [-1.6, 1.55, 0], plus.get_left()], S.GREY, 2.5)
        self.w_out_r = _poly([B.get_top(), [cx, 1.55, 0], plus.get_right()], S.GREY, 2.5)
        self.w_h = Line(plus.get_top(), hn.get_bottom(), color=S.GREY, stroke_width=2.5)
        self.part("wires", VGroup(self.w_in_l, self.w_in_r, self.w_out_l, self.w_out_r, self.w_h))
        self.move_to(ORIGIN)
        if show is not None:
            for name in list(self.parts):
                if name not in show:
                    _save_op(self.parts[name])
                    _set_op(self.parts[name], 0)
                    self.parts[name].hidden = True

    def forward(self, run_time: float = 1.6) -> list:
        paths = [self.w_in_l, self.w_in_r, self.w_out_l, self.w_out_r, self.w_h]
        return [ShowPassingFlash(p.copy().set_stroke(TURN, 6), time_width=0.6, run_time=run_time) for p in paths]

    def backward(self, run_time: float = 2.0) -> list:
        rev = [VMobject().set_points(p.get_points()[::-1]) for p in (self.w_h, self.w_out_l, self.w_out_r)]
        flashes = [ShowPassingFlash(p.copy().set_stroke(PULSE, 7), time_width=0.7, run_time=run_time)
                   for p in rev]
        return flashes + [self.w0.animate(run_time=run_time).set_fill(FROZEN, 0.12),
                          Indicate(self.a, color=OWN, run_time=run_time),
                          Indicate(self.b, color=OWN, run_time=run_time)]

    def merge_into(self, target, run_time: float = 1.5) -> list:
        g = VGroup(self.a, self.b).copy()
        return [Succession(g.animate(run_time=run_time * 0.6).move_to(target).scale(0.5),
                           FadeOut(g, run_time=run_time * 0.4, scale=0.3)),
                Indicate(target, color=OWN, run_time=run_time)]


class LayerTower(VGroup):
    """V7's 28-layer tower (S13): 28 thin rows, each with seven small cells (q k v o gate up down);
    q_proj and v_proj light GREEN in every block; a Counter beside it ticks to 1,146,880 (c72).
    .rows .q .v (VGroups of cells) .light_qv(run_time) -> anim (lagged, bottom to top);
    .counter (Counter "trainable") .count(run_time) -> anim. Built centred: 6.4 x 5.0."""

    NAMES = ("q", "k", "v", "o", "gate", "up", "down")

    def __init__(self, layers: int = QWEN_LAYERS, cell_w: float = 0.42, row_h: float = 0.13, **kw):
        super().__init__(**kw)
        self.rows = VGroup()
        self.q, self.v = VGroup(), VGroup()
        for k in range(layers):
            r = VGroup(*[Rectangle(width=cell_w, height=row_h, stroke_color=S.GREY_DARK, stroke_width=1)
                         .set_fill(FROZEN, 0.25) for _ in self.NAMES]).arrange(RIGHT, buff=0.05)
            r.move_to([0, k * (row_h + 0.04), 0])
            self.q.add(r[0])
            self.v.add(r[2])
            self.rows.add(r)
        heads = VGroup(*[mono(n, CAPTION, S.GREY) for n in ("q", "v")])
        heads[0].next_to(self.rows[-1][0], UP, buff=0.12)
        heads[1].next_to(self.rows[-1][2], UP, buff=0.12)
        self.heads = heads
        cap = label(f"{layers} blocks", CAPTION, S.GREY).next_to(self.rows, LEFT, buff=0.25)
        self.counter = Counter("trainable", 0, OWN, size=26)
        self.counter.next_to(self.rows, RIGHT, buff=0.5)
        self.add(self.rows, heads, cap, self.counter)
        self.move_to(ORIGIN)

    def light_qv(self, run_time: float = 2.0):
        return LaggedStart(*[AnimationGroup(q.animate.set_fill(OWN, 0.8).set_stroke(OWN),
                                            v.animate.set_fill(OWN, 0.8).set_stroke(OWN))
                             for q, v in zip(self.q, self.v)], lag_ratio=0.15, run_time=run_time)

    def count(self, n: int = TRAINABLE, run_time: float = 2.0):
        return self.counter.count_to(n, run_time)


# ================================================================== V8 · memory under pressure (S14)
class CheckpointChain(VGroup):
    """V8, slides 58–64: X -> h₁ -> h₂ -> h₃ -> ŷ as five circles with arrows, and a memory meter
    (a GREY frame filling YELLOW) under them. Built centred: 10.4 x 2.6.
    .store(i) -> anims (node i fills: its activation is kept; the meter rises one notch)
    .drop(i) -> anims (node i empties; the meter falls one notch)
    .recompute(src, dst) -> anims (a small PINK replay arc from node src to dst, dst fills again)
    .nodes .arrows .meter .level"""

    def __init__(self, names=("X", "h₁", "h₂", "h₃", "ŷ"), r: float = 0.42, gap: float = 1.6, **kw):
        super().__init__(**kw)
        self.nodes = VGroup()
        for s in names:
            c = Circle(radius=r, stroke_color=INK, stroke_width=3).set_fill(TURN, 0.0)
            g = VGroup(c, label(s, 28, INK).move_to(c))
            g.circle = c
            self.nodes.add(g)
        self.nodes.arrange(RIGHT, buff=gap)
        self.arrows = VGroup(*[_arrow(a.get_right(), b.get_left(), S.GREY, 3) for a, b in zip(self.nodes, self.nodes[1:])])
        n = len(names)
        self.meter_frame = Rectangle(width=self.nodes.width, height=0.32, stroke_color=S.GREY, stroke_width=2)
        self.meter_frame.next_to(self.nodes, DOWN, buff=0.7)
        self.meter_label = label("activation memory", CAPTION, S.GREY).next_to(self.meter_frame, DOWN, buff=0.12)
        self.step_w = self.meter_frame.width / n
        self.fill = Rectangle(width=0.001, height=0.3, stroke_width=0).set_fill(TURN, 0.6)
        self.fill.align_to(self.meter_frame, LEFT).align_to(self.meter_frame, DOWN).shift(UP * 0.01)
        self.level = 0
        self.add(self.nodes, self.arrows, self.meter_frame, self.meter_label, self.fill)
        self.move_to(ORIGIN)

    def _meter(self, level: int):
        tgt = Rectangle(width=max(0.001, level * self.step_w), height=0.3, stroke_width=0).set_fill(TURN, 0.6)
        tgt.move_to(self.meter_frame).align_to(self.meter_frame, LEFT)
        self.level = level
        return Transform(self.fill, tgt)

    def store(self, i: int) -> list:
        return [self.nodes[i].circle.animate.set_fill(TURN, 0.5), self._meter(self.level + 1)]

    def drop(self, i: int) -> list:
        return [self.nodes[i].circle.animate.set_fill(TURN, 0.0), self._meter(max(0, self.level - 1))]

    def recompute(self, src: int, dst: int) -> list:
        a, b = self.nodes[src].get_top(), self.nodes[dst].get_top()
        arc = ArcBetweenPoints(a + UP * 0.05, b + UP * 0.05, angle=-PI / 2, color=LOOKUP, stroke_width=3)
        self.replay = arc
        return [Create(arc), self.nodes[dst].circle.animate.set_fill(TURN, 0.5), self._meter(self.level + 1)]


class Paging(VGroup):
    """V8, slide 65: a GPU box (BLUE, the Colab GPU) and a CPU box (GREY), `n` optimizer pages
    (small GOLD-free white sheets) in the GPU; .page_out(k) -> anims (k pages slide along PINK arrows
    to the CPU), .page_in(k) -> anims (back). Built centred: 9.0 x 2.6. .gpu .cpu .pages .arrows"""

    def __init__(self, n: int = 6, **kw):
        super().__init__(**kw)
        self.gpu = VGroup(box(3.4, 2.2, CLOUD, fill_opacity=0.06), label("GPU", CAPTION, CLOUD))
        self.gpu[1].next_to(self.gpu[0], UP, buff=0.1)
        self.cpu = VGroup(box(3.4, 2.2, S.GREY, fill_opacity=0.04), label("CPU memory", CAPTION, S.GREY))
        self.cpu[1].next_to(self.cpu[0], UP, buff=0.1)
        VGroup(self.gpu, self.cpu).arrange(RIGHT, buff=2.2)
        self.arrows = VGroup(_arrow(self.gpu[0].get_right() + UP * 0.3, self.cpu[0].get_left() + UP * 0.3, LOOKUP, 3),
                             _arrow(self.cpu[0].get_left() + DOWN * 0.3, self.gpu[0].get_right() + DOWN * 0.3, LOOKUP, 3))
        self.pages = VGroup(*[file_glyph(0.5, INK) for _ in range(n)]).arrange_in_grid(2, (n + 1) // 2, buff=0.25)
        self.pages.move_to(self.gpu[0])
        self.out = []
        self.add(self.gpu, self.cpu, self.arrows, self.pages)
        self.move_to(ORIGIN)

    def page_out(self, k: int = 2, run_time: float = 1.2) -> list:
        anims = []
        for j in range(k):
            p = self.pages[len(self.pages) - 1 - j - len(self.out)]
            tgt = self.cpu[0].get_center() + np.array([-0.8 + 0.8 * (len(self.out) + j), 0, 0])
            anims.append(p.animate(run_time=run_time).move_to(tgt))
        self.out += [None] * k
        return anims

    def page_in(self, run_time: float = 1.2) -> list:
        n = len(self.pages)
        k = len(self.out)
        grid = self.pages.copy().arrange_in_grid(2, (n + 1) // 2, buff=0.25).move_to(self.gpu[0])
        self.out = []
        return [self.pages[n - 1 - j].animate(run_time=run_time).move_to(grid[n - 1 - j]) for j in range(k)]


class BitStrips(VGroup):
    """V8, slides 66–67: FP32 (1/8/23), FP16 (1/5/10), BF16 (1/8/7) as rows of bit cells, sign /
    exponent / fraction outlined WHITE / PINK / GREEN (exponent = range, fraction = precision), the
    name of each format at the left. Built centred: about 12.0 wide (cell 0.3). .rows {name: row}
    with row.sign .exp .frac; .legend"""

    FORMATS = (("FP32", 1, 8, 23), ("FP16", 1, 5, 10), ("BF16", 1, 8, 7))

    def __init__(self, cell: float = 0.3, **kw):
        super().__init__(**kw)
        self.rows = {}
        rows = VGroup()
        for name, s, e, f in self.FORMATS:
            def seg(n, col):
                return VGroup(*[Rectangle(width=cell, height=cell * 1.3, stroke_color=col, stroke_width=2)
                                .set_fill(col, 0.12) for _ in range(n)]).arrange(RIGHT, buff=0.0)
            sg, eg, fg = seg(s, BIT_SIGN), seg(e, BIT_EXP), seg(f, BIT_FRAC)
            bits = VGroup(sg, eg, fg).arrange(RIGHT, buff=0.06)
            nm = mono(name, 24, INK)
            row = VGroup(nm, bits).arrange(RIGHT, buff=0.35)
            row.sign, row.exp, row.frac, row.name_text = sg, eg, fg, nm
            self.rows[name] = row
            rows.add(row)
        rows.arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        leg = VGroup(label("sign", CAPTION, BIT_SIGN), label("exponent = range", CAPTION, BIT_EXP),
                     label("fraction = precision", CAPTION, BIT_FRAC)).arrange(RIGHT, buff=0.6)
        leg.next_to(rows, DOWN, buff=0.35)
        self.legend = leg
        self.add(rows, leg)
        self.move_to(ORIGIN)


class LossCurve(VGroup):
    """S14: the staff's training-loss table (expected/colab-c75) drawn as a curve: x = step 0..450,
    y = loss 1.2..2.1, GREY axes with a few mono tick labels (no LaTeX), BLUE-free GREEN curve of
    the adapters' training (the run is recorded: add recorded_tag()). .axes .curve .dots .create()
    -> anim. Built centred: width x height."""

    def __init__(self, points=None, width: float = 7.0, height: float = 3.2, y_lo: float = 1.2,
                 y_hi: float = 2.1, x_hi: int = 450, **kw):
        super().__init__(**kw)
        pts = points or loss_points()
        self.w, self.h, self.y_lo, self.y_hi, self.x_hi = width, height, y_lo, y_hi, x_hi
        o = np.array([-width / 2, -height / 2, 0])
        self.origin = o
        xa = Line(o, o + RIGHT * width, color=S.GREY, stroke_width=2)
        ya = Line(o, o + UP * height, color=S.GREY, stroke_width=2)
        ticks = VGroup()
        for s in (0, 150, 300, 450):
            p = self.pt(s, y_lo)
            ticks.add(Line(p, p + DOWN * 0.08, color=S.GREY, stroke_width=2),
                      mono(str(s), CAPTION, S.GREY).next_to(p, DOWN, buff=0.12))
        for v in (1.4, 1.8, 2.0):
            p = self.pt(0, v)
            ticks.add(Line(p, p + LEFT * 0.08, color=S.GREY, stroke_width=2),
                      mono(f"{v:.1f}", CAPTION, S.GREY).next_to(p, LEFT, buff=0.12))
        xl = label("step", CAPTION, S.GREY).next_to(xa, DOWN, buff=0.5)
        yl = label("training loss", CAPTION, S.GREY).next_to(ya, UP, buff=0.12).align_to(ya, LEFT)
        self.axes = VGroup(xa, ya, ticks, xl, yl)
        self.curve = VMobject(stroke_color=OWN, stroke_width=4).set_points_as_corners(
            [self.pt(s, v) for s, v in pts])
        self.dots = VGroup(*[Dot(self.pt(s, v), radius=0.05, color=OWN) for s, v in pts])
        self.add(self.axes, self.curve, self.dots)
        self.move_to(ORIGIN)

    def pt(self, step: float, loss: float):
        return self.origin + np.array([step / self.x_hi * self.w, (loss - self.y_lo) / (self.y_hi - self.y_lo) * self.h, 0])

    def create(self, run_time: float = 2.0):
        return AnimationGroup(Create(self.curve, run_time=run_time), LaggedStart(*[FadeIn(d) for d in self.dots],
                                                                                 lag_ratio=0.2, run_time=run_time))


# ================================================================== S16 · three things you can ship
def ship_cards() -> VGroup:
    """S16: three cards side by side — a GREEN "adapter · about 4.6 MB · needs the base", a GREY
    "merged model · FP16 · stands alone", a BLUE "endpoint · no weights in your hands". 12.0 x 1.5.
    .adapter .merged .endpoint"""
    a = card_glyph("adapter", "about 4.6 MB · needs the base", OWN, w=3.8)
    m = card_glyph("merged model", "FP16 · stands alone", FROZEN, w=3.8)
    e = card_glyph("endpoint", "no weights in your hands", CLOUD, w=3.8)
    g = VGroup(a, m, e).arrange(RIGHT, buff=0.3)
    g.adapter, g.merged, g.endpoint = a, m, e
    return g
