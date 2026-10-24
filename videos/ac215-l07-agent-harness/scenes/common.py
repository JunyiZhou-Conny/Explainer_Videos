"""Shared code for AC215 L7 (LLM: Agents II; follow-along: dlops-io/agent-harness @ e25dfe9 and the
course Colab "Agent Harness"): paths, narration, the semantic colours of BRIEF.md, the README /
Colab trackers, loaders for the real captures in assets/ (customer IDs masked, emoji stripped, the
401 folds of script.md), terminal / panel / card helpers, and the video's recurring pictures V1-V8
of BRIEF.md. Built from L06's common.py (generic helpers kept, incl. its three QA fixes: terminal
output wraps at word boundaries, every swap of two texts at one place is sequential, scrolled-off
rows fade in place) with L07's set pieces. Tested on screen by build/common_test.py (CommonTest,
PieceStills: explainer.check clean, preview sheets read).

Notes for scene authors
=======================

    from common import *      # every scene: SAY = NARRATION["S07"]; assert len(SAY) == n;
                              # one `with self.voiceover(SAY[i]) as vo:` per SAY line, in order
All text here is 20-26 pt. Never .scale() a group that holds text below 1.0: build the smaller
variant (mode=/compact=/mini=) or use piece.rescale(k) (shapes shrink, text keeps its size).
Methods return ANIMATIONS (play them) or MOBJECTS (placed, not added: FadeIn them) unless they say
"plays". Paths never cross text: put a card where it will be read, never fly it over a label.

Frame budget. Tracker top left (x -6.5..-2.0, y 2.93..3.5), lecture_ref top right (x >= 3.09, y
3.13..3.6). A one-line chip in the top band: top_chip(...) (y 2.66, above terminals of <= 12 rows;
tall=True with a 13-row terminal: y 2.87, <= 8.4 wide). Terminals: full width 12.6, 22 pt, 65
characters a row, bottom at BOTTOM (-3.5), at most 13 rows (top 2.59; 12 rows: 2.19). A 3-row
strip's top is STRIP_TOP (-1.44): a picture above a strip has y -1.3..2.8. The V1 mini-map (3.2 x
1.9) sits at MINI_CENTER (bottom right) or MINI_ABOVE_STRIP; never with a code panel, a tall
terminal or a ponder card.

Names and emoji. The customer IDs are masked on the way in: unname(s) turns pavlos -> "‹customer 1›"
(MASK1), shivas -> "‹customer 2›" (MASK2), any case, drawn GREY by every panel/terminal; mask_chip(1)
is the chip. The full names (data/customers.json, Colab cells 0 and 16) never appear: every line
that goes on screen is checked (guard_names raises; customers.json "name" lines, Colab cell 0 and
the repo notebooks raise). Capture lines come without emoji (strip_emoji); their meaning is the
colour: Capture.color(n) / .out(...) give ❌ ⚠️ RED, ✅ GREEN, 🤖 (a model call) BLUE.

Data and sources
    NARRATION["S01"] ... ["S16"]   SAY lines from script.md      TITLES[cls], SPEC (video.yaml)
    capture(name, folder) -> Capture: assets/terminal/<folder>/<name>.txt; name may be the number
        alone ("10" -> 10-act1-standard.txt) or "folder/name" ("container/10",
        "expected/colab-c23-agent-harness"). CAPTURE FOLDERS: laptop, container, expected (line 1
        of an expected/ file is a '#' provenance header). Never: capture-only/, laptop/07 .plain,
        laptop/09 lines 2-4 (2 and 3 only via .cut(2, "DISK USAGE") / .cut(3, "1.77GB")),
        laptop/10 line 3 and container/00 line 9 (GCP_PROJECT).
      .cmd (the `$` line without "$ ") .lines .exit .first (file line of .lines[0]) .header
      .line(n) FILE line n, emoji stripped   .color(n) its colour   .at(2, (5, 7), "…", 33) lines
      .out(*spec) -> [(text, colour)] for t.print: file lines, (a, b) ranges, "…", and your own
          str / (str, colour) items (cut/fold/as401 results) in one list
      .cut(n, "x") line n through "x", then " …"   .cut_before(n, " exit") (a prompt line)
      .as401(n) the long 401 fold (wrap=True: 2 rows) / .as401(n, short=True) the 1-row fold /
          .as401(n, until="You can find your API key at") S04's 3 rows -> (text, ERR)
      .fold(a, b, "X … Y") checks X is lines a..b's own text   .join(2, 3) laptop/12's wrapped
          line   .split_at(n, 56) laptop/08's halves   .squeeze(n) BuildKit padding -> 2 spaces
      .typed(n) the command on a prompt line   .pick() L1-style (index = file line - 1)
    source_text(path)  excerpt(path, a, b)  source_line(path, n)  readme(a, b) -> README.md rows
        (paths as in the repo: "formaggio/shop/checkout.py"; Colab cells "colab/cell-10.py")
        cell_title(path) the cell's "# @title"   shown_path(path) ("Agent Harness · cell 10")
    split_prompt(line)  split_prompt_inside(line)  strip_emoji(s)  unname(s)
    C23 (the recorded Act 1 run: per call msgs, requested, tokens_in/out, result, lines{})
    TOKENS_IN (1,942 … 4,540) TOKENS_OUT MSGS (1 … 11) TOOLS_ACT1 (5) PLANNER_TOOLS (9)
    CATALOG CHEESES (12 IDs, catalog order) EXCLUDED {id: reason} SURVIVORS (7) SIEVES
    RESULT_CHIPS  BOUNDARY_* (V1 texts)  RAIL_*  TICKET_FIELDS  DRAWERS  STAIRS  PILLS  EVENTS
    CYCLE_STEPS  JUDGES  JAR_TOKENS JAR_REPLY JAR_INPUT
    MODEL_ID "gpt-5.6-luna"  KEY_VAR  KEY_PLACEHOLDER "YOUR_OPENAI_API_KEY"  KEY_MASKED
    "YOUR_OPE*******_KEY"  VENDOR  RUN_MANAGER  RUN_FAILED  FINGERPRINT16  GUIDE  CTR_ID

Colours (BRIEF.md, binding; the colour of a card says who decided it: BLUE the model proposed it,
GREEN the harness decided it, YELLOW a human decided it)
    LAPTOP GREY · CLOUD (= MODEL = PROPOSED) BLUE · CTR TEAL · SYSTEM ORANGE · HARNESS (= DATA =
    VENV = CHECKED) GREEN · TOOL (= SDK) PURPLE · ERR RED · TURN (= HUMAN) YELLOW · COST (= KEY)
    GOLD · LOOKUP PINK · INK white · FUTURE GREY dashed · AMBER (a rail / tool frozen for a human)
Running example
    P_WS "student@laptop:~/AC215$"  P_REPO ".../AC215/agent-harness$"  P_CTR "app@13a6188396ca:/app$"
    CTR_TITLE "container · agent-harness"  LAPTOP_TITLE "laptop"  SECOND "laptop · second terminal"
    COLAB_TITLE "Agent Harness · Colab"

Trackers (top left, YELLOW)
    tracker(key, step=None)  keys = script.md's TRACKER names: Start Verify Model Notebook Colab
        Agent Context Act3 Act4 Skills Systems Eval1 Eval2 Eval3 Eval4 Res Down (SECTIONS: head
        "README" or "Colab", section, steps; "Down" reads "README › Teardown · extra"). step None:
        no step lit.  self.play(tr.goto(k))  caption_extra(tr, on) -> " · extra" (cross-fade)
    tr = switch_section(self, tr, "Context", 1)  (plays: old lifts away, new drops in)
    lref("20–24") = lecture_ref(7, ...) top right;  lref_swap(scene, old, "22") -> new (plays)
    swap_text(parent, old, new) -> anims: the house sequential text swap (old out, then new in)

Terminal helpers (term() masks and greys "…" on every line it places)
    term(prompt=P_REPO, rows=12, title=None, container=False, top=None)  container=True: TEAL
        frame, title CTR_TITLE, prompt P_CTR
    type_cmd(scene, t, cmd)  every typed command (folds at spaces, quote-aware, " \" + indent 4)
    show(scene, t, cap, *spec, wrap=False) = t.print(scene, cap.out(*spec)) (emoji colours)
    t.print(scene, lines, wrap=True) folds at word boundaries; item_rows(rows, k) the rows of item
        k; wrapped_glyphs(rows, "Error code: 401") / wrapped_at(rows, sub) find text across rows
    session(scene, t, cap, 10, 11, 12) replays laptop/12 (prompt lines typed, "OpenAI API key: "
        printed, then the next prompt)   type_after(scene, t, row, "approve") the YELLOW answer
        typed after a printed "…decline: " row   bare_prompt(scene, t)  cd_prompt(scene, t, p)
    enter_container(t) / leave_container(t) -> anims (frame colour, title swap, prompt)
    resize(scene, t, rows, keep=None)  strip_top(rows)  second_terminal(scene, rows=7, top=2.75)
    frame_tags(t, nokey_tag(), live_tag()) tags on the title bar (when the typed line fills its
        row; call before the terminal shows: the title moves left)  beside(tag, t, line) +
        pin(scene, line, tag) a tag after a line's text (raises if it would cover text)
    print_build(scene, t, rows) BuildKit rows with GREY time tags   col_box(line, a, b) box over
        columns   bracket(mobs, text)  under(mob) strike(mob) ring(mob)  at_bottom(mob)

Panels and cards
    src_panel(path, a, b=None, wrap=True|{n: [...]}, focus=, join=, subtitle=True)  CODE(): header
        "path · lines a–b" (folded: src_panel(path, [209, (215, 224)]) "(folded)"); <= 12 rows;
        .bar(n, colour) .span(n, sub) .rows_of(n)
    quote_card(a, b)  QUOTE(README.md: a–b): GREY card, README words (inline code mono), tag
        `expected`   top_chip(phrase, where="README.md · line 248") the one-line form
    recorded_box("colab-c23-agent-harness", (63, 70))  RECORDED: output box (never a terminal),
        header "Agent Harness · cell 23 · saved output", tag `recorded · the staff's saved Colab run`
    log_panel(lines, header)  PANEL   output_box(lines, header)   readme_chip(where, phrase)
    excerpt_chip(sub, header, line=source_line(...))  exact sub-string chip   cmd_chip(cmd, note)
    turn_card(rows) the static "your turn" card (str = command, (cmd, "extra"), (cmd, note),
        Prose("…"), (Prose("offline · free"), HARNESS) as the last line)   extra_card(purpose)
    card_rows(items, header)  table_card(headers, rows)  LookFor(items)  what_if_frame()
    ponder_at(scene, question, seconds=8, hide=()) plays the ponder card (FadeOut it at the next
        block)   colab_frame() BLUE notebook frame + illustration tag   menu_path([...])
    Counter(text, value).count_to(n)  CallCounter(n).count_to(n) (ticks, sequential swaps)
Tags (GREY unless said): your_turn() (YELLOW) extra_tag() illustration_tag(note_) recording_tag()
    recorded_tag() expected_tag() nokey_tag()/no_key_tag() scripted_tag() live_tag() (GOLD)
    offline_tag() (GREEN) cost_tag(s) cost_chip("12 runs") (GOLD) test_tag() (YELLOW "TEST
    decision") template_tag() erratum_tag(note_) differ_tag() harmless_tag() preview_tag()
    concept_tag() (dashed) mask_chip(i) stamp(text, colour) human_stamp(two_rows) fix_chip(text)
    concept_box(text) (dashed)  keep_size(m) marks your own chips for Piece.rescale
Glyphs: key_glyph(name=) key_outline() padlock() + unlock(lock) hand(colour) person_icon(TURN)
    person() pencil() gear() file_row(name) ghost_file(name) cylinder() (GREEN db) model_box()
    model_chip() seal() broken_seal() diamond() sticky_note() receipt_token(text) notebook_glyph()
    container_box() laptop_zone() cost_tick() json_card(lines, colour) cart_token(items=None,
    dashed=False, scale=1) + recolor_cart(cart, colour) cheese_chip(id) msg_card() gold_meter()
    hash_chip() buffer_stop(text) skill_card(path) skill_tree(root, files) Gate(...)

Set pieces: Piece = VGroup + named parts. A part not shown yet is a member at opacity 0 (it moves
    with the piece); show=(...) names the visible parts; piece.reveal(scene, *names) /
    piece.hide(scene, *names) play; self.play(*piece.parts_in("a")). Never FadeOut a member, never
    piece.set_opacity(...); FadeOut the whole piece. Built centred at ORIGIN unless "in place".
    V1 TwoColumns(height=4.8)  12.4 wide: BLUE "the model proposes" | GREEN "the harness decides",
       dim YELLOW "a human decides" stamp; .slot(side, i, n) card spots; .write_word(i) (the
       loop · its limits · its context · its checks); .human_on(). TwoColumns(height=1.1,
       words=False) is the band (titles left, two-row stamp right).
       ActionBoundary(width=12.6, texts="all", moves=True)  slide 22's table, 12.6 x 6.2 (5.1
       without moves): header + PINK "who decides?", five GREY pills, BLUE cells, GREEN cells,
       Move LEFT / Move RIGHT. Half size: ActionBoundary(width=8.6, row_h=0.55, texts=("context",),
       moves=False) (rows without text are thin; their fills are GREEN bar segments).
       .light(row) .unlight() .fill(row, text) -> (mob, anims) .prefill(act) .fill_recap()
       .slide_phrase("context", "what to remember", "capsule · compaction · host-written
       memory") -> anims (one play, ~1.6 s) .stamp_human(row) -> (stamp, anims) .dim_side("blue")
       .row(name) .cell(name, side). Rows: control tools context verify sub.
       BoundaryMini(center=MINI_CENTER, upto=act)  3.2 x 1.9 glyph-only map: .light(row)
       .unlight() .add_bar(row) .caption(text) (<= 40 chars, left of the map) .flash_green()
       SixSteps() slide 21's strip (11.6 x 0.9, PINK seam between Plan | Execute): .light(step)
       Spectrum() slide 36 (12.2 x 1.4): .stop(i) .above(i, h) .light(i)
       AgentBlock(ends=True) slide 7 (12.0 x 2.9): .block(name) .memory_tag("act 4")
    V2 LoopMeter()  in place (x -6.3..5.9, y -3.3..2.7): model, message stack + "messages: n",
       GOLD meter + one tick per call, five GREEN paddles. .round(scene, k) (k = 0..4, from C23)
       or .send(scene, k) -> card ... .complete(scene, k, card); .answer(scene) (call 6);
       .paddle(name); .freeze() before it leaves.
    V3 HarnessRings(mode="full"|"medium"|"compact", without=(), show=...)  8.8 x 5.5 / 5.7 x 3.9 /
       3.4 x 2.2: core build_agent, padlocked inner ring "admission · tool audit · shop rules",
       rings trace budget context cartcheck. .put(name) / .lift(name) -> anims .glow(name)
       .unglow(name) .label_of(name) .mark(name, "?") .fence() (SDK fallback, +0.95 tall incl.
       its label) .gate_point()
       Turnstile(cap=8)  1.6 x 2.2: .token(colour, text) .admit(token) .lock() (RED, "Maximum of
       8 model calls reached." under it, 5.8 wide) .bounce(token)
    V4 ContextStack(compact=False, title=None)  slide 16: 12.4 x 4.9 with prompt -> six blocks ->
       LLM -> response; compact 3.2 x 3.8 titles only. .light(i) .fill_slots() .slots() .block(i)
       Sieves()  in place above a strip (x -6.4..6.3, y -1.3..2.8): .drop(scene, id) /
       .drop_all(scene, each=0.8) plays; .chip(id) .reason(id) .rejects .tray_chips
       Lanes()  12.4 x 2.9 system / user lanes: .enter(card, lane) .turn_back(card) .count_to(2)
       ShipToggle()  9.6 x 2.0 PA <-> NY: .flip() -> anims (stamp swaps)
    V5 Rail()  U-shaped 12.6 x 3.9 (Rail(mini=True, named="review") 5.2 x 2.2 glyph-only;
       Rail(layout="line", names=("validate", "review", "place")) 9.3 x 0.8): .station(name)
       .edge(i) (act3_workflow.py lines 27-32 order) .start() .spot(name) .move(token, name)
       (routes under stations, never across a label) .revise(token) .count(k) .freeze(name)
       .unfreeze(name) .block_loop() .scripted_seat(). Stations: confirm propose validate
       pairings review place. Tokens: cart_token() (0.8 wide; scale=0.8 on line rails).
       Ticket()  card 5.2 x 3.6 (+ the hidden stock_g chip right of it; place by .frame):
       .fill(i) .show_hash() .show_excluded() .hash_mob   hash_chip(FINGERPRINT16)
       Stopwatch() .run(turns, run_time) .pause_look(on) .freeze()
       StockShelf(items, cap, numbers=True) .set(name, g) -> anims .need(name, g) .bar(name)
    V6 Cabinet(only=None)  7.0 x 4.1, drawers tasks history memory approval audit (Memory has no
       handle; Approval a YELLOW keyhole): .try_open .open .close .write(name, mob) .keyhole()
       .handle_point(name)
       ContextJar(slot_h=0.42)  jar 2.8 x 4.0 + labels (8.0 wide): .pour(scene) .truncate(scene,
       keep=5) (plays) .capsule_card(text) .pin_capsule(scene, card) .unpin_capsule(scene) .mark_y
    V7 Staircase()  in place above a strip (base y -1.0): .step(i) .landing(i, k) .climb(card, i, k)
       skill_card("…/email-template.html") (<= 4.0 wide; long paths break after the first "/")
       skill_tree(root, files, dashed=False, crossed=()) .named[file]   seal() broken_seal()
    V8 ThreePills()  12.4 x 3.8 bands: .start(i, chip) then .drop(i, chip) (slides along its row)
       EventChain() 4.6 x 3.6: .light(i) -> anims   Cycle() 12.5 x 4.4 with number badges:
       .light(i) .attach(i, chip) (inner slots; 4.6 wide inside) .grow_pile() .lap(scene)
       Balance() .load(a, b) .tilt(angle)   Judges() .judge(i) (human | LLM judge dashed | checks)
    S02 Stage(show=...)  12.4 x 4.2 laptop + container + mounts + key + no ports + HTTPS + OpenAI:
       .reveal(scene, *parts) .shrink(scene) / .grow(scene) (plays; texts out before shapes move)
       .badge(width) glyph-only copy for S16

Capture folder names (assets/terminal): laptop, container, expected (never: capture-only).
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
    Arc,
    ArcBetweenPoints,
    Arrow,
    Circle,
    DashedLine,
    DashedVMobject,
    DecimalNumber,
    DoubleArrow,
    Dot,
    Ellipse,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    Line,
    MoveToTarget,
    ManimColor,
    Polygon,
    Rectangle,
    Rotate,
    RoundedRectangle,
    Succession,
    Text,
    Transform,
    ValueTracker,
    VGroup,
    VMobject,
    Wiggle,
    linear,
    rush_into,
    smooth,
    squish_rate_func,
)

from explainer import style as S
from explainer.components import person_icon, ponder_card  # noqa: F401  (re-exported for the scenes)
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

SPEC = yaml.safe_load((PROJECT / "video.yaml").read_text())
TITLES = {s["cls"]: s["title"] for s in SPEC["scenes"]}
_script = PROJECT / "script.md"
NARRATION = load_narration(_script) if _script.exists() else {}

# ------------------------------------------------------------------ semantic colours (BRIEF.md)
# The colour of a card says who decided it: BLUE = the model proposed it, GREEN = the harness
# decided it, YELLOW = a human decided it.
LAPTOP = S.GREY          # your laptop: ~/AC215, the clone, secrets/, the laptop terminal, outputs/ seen from the host
CLOUD = S.BLUE           # OpenAI, gpt-5.6-luna, the HTTPS line, the Colab VM, and everything the model writes
MODEL = CLOUD
PROPOSED = CLOUD
CTR = S.TEAL             # the container and image agent-harness: /app, /.venv, the build
SYSTEM = S.ORANGE        # the base image's own Python and apt packages (S02 only)
HARNESS = S.GREEN        # code we own that decides: layers, counters, validation, the packet, capsule, tickets, traces
DATA = HARNESS
VENV = HARNESS
CHECKED = HARNESS
TOOL = S.PURPLE          # tools you install and the SDK: Docker, uv, Microsoft Agent Framework (request_info, @tool …)
SDK = TOOL
ERR = S.RED              # the 401, Run stopped, cli.py: error, violations, BLOCKED / UNRESOLVED / DECLINED
TURN = S.YELLOW          # your turn, the trackers, look here now, every human decision
HUMAN = TURN
COST = S.GOLD            # OpenAI tokens (a GOLD tick per live call), the OPENAI_API_KEY glyph, live · billed per token
KEY = COST
LOOKUP = S.PINK          # bind mounts, the HTTPS route, outputs/ paths, request_id handles, run IDs, fingerprint compare
INK = S.WHITE
DIMMED = S.GREY
FUTURE = S.GREY          # dashed: lecture concepts with no code here (LLM judge, MCP, handoffs, skill scripts), L08/L09
AMBER = S.ORANGE         # a frozen rail / tool waiting for a human (SDK request_info, approval_mode)

# ------------------------------------------------------------------ names on screen
# Two synthetic customer IDs are staff first names: masked on screen. The full names (the `name`
# fields of data/customers.json, Colab cells 0 and 16, the git author) never appear: every line
# that goes on screen is checked against them (they are read from the data file at import, never
# written here).
MASK1, MASK2 = "‹customer 1›", "‹customer 2›"
MASKS = (MASK1, MASK2)
MASK = MASK1                     # (L06 name, kept for helpers that grey "the mask")
_IDS = {"pavlos": MASK1, "shivas": MASK2}
_ID_RE = re.compile(r"pavlos|shivas", re.IGNORECASE)


def unname(s: str) -> str:
    """The customer IDs (any case) -> the GREY chips' text: pavlos -> ‹customer 1›, shivas ->
    ‹customer 2›. Every panel line goes through this (capture(), excerpt() and the panels do it for
    you). Raises if a line holds a full name (never on screen)."""
    out = _ID_RE.sub(lambda m: _IDS[m.group(0).lower()], s)
    guard_names(out)
    return out


def _full_name_tokens() -> tuple[str, ...]:
    """The words of the customers' full names other than the IDs (read from the data, never shown)."""
    try:
        rows = json.loads((SOURCE / "data" / "customers.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return ()
    toks = set()
    for r in rows if isinstance(rows, list) else []:
        for t in re.split(r"\W+", str(r.get("name", ""))):
            if len(t) >= 3 and t.lower() not in _IDS:
                toks.add(t.lower())
    return tuple(sorted(toks))


_NAME_TOKENS = _full_name_tokens()
_NAME_RE = re.compile(r"\b(" + "|".join(re.escape(t) for t in _NAME_TOKENS) + r")\b", re.IGNORECASE) \
    if _NAME_TOKENS else None


def guard_names(s: str) -> str:
    """Raise ValueError if s holds a word of a customer's full name (never on screen)."""
    if _NAME_RE is not None and _NAME_RE.search(s):
        raise ValueError("this line holds a person's full name: it is never shown (BRIEF.md 'Names')")
    return s


# ------------------------------------------------------------------ emoji (the mono font drops them)
@lru_cache(maxsize=None)
def _mono_has(ch: str) -> bool:
    """True when the house mono font (or, failing that check, the system) has a glyph for ch."""
    try:
        out = subprocess.run(["fc-list", f":charset={ord(ch):x}", "family"], capture_output=True,
                             text=True, timeout=5).stdout
    except (OSError, subprocess.SubprocessError):
        return True
    return any("DejaVu Sans Mono" in f for f in out.splitlines())


# the emoji of the captures (script.md "Emoji"): always removed, even where the font has a glyph
EMOJI = frozenset("🤖📥🧰❌✅🧪👤🔍📊🛡🧾💬📤🔧📋📦⏱🧺🔄⚠💾🧀" + chr(0xFE0F))


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


# The meaning of a captured line's leading emoji moves into its colour (script.md "Emoji").
EMOJI_COLORS = (("❌", ERR), ("⚠", ERR), ("✅", HARNESS), ("🤖", CLOUD))


def emoji_color(raw: str, default: str = OUTPUT) -> str:
    """The colour a captured line prints in, from the emoji it starts with: ❌ / ⚠️ RED, ✅ GREEN,
    🤖 (a model call) BLUE, anything else `default` (output grey)."""
    head = raw.lstrip()
    for e, col in EMOJI_COLORS:
        if head.startswith(e):
            return col
    return default


# ------------------------------------------------------------------ the running example
USER, HOST = "student", "laptop"
P_HOME = f"{USER}@{HOST}:~$"
P_WS = f"{USER}@{HOST}:~/AC215$"
P_REPO = f"{USER}@{HOST}:~/AC215/agent-harness$"
CTR_ID = "13a6188396ca"                       # laptop/07 line 27 (changes every run)
P_CTR = f"app@{CTR_ID}:/app$"
CTR_TITLE = "container · agent-harness"
LAPTOP_TITLE = "laptop"
SECOND = "laptop · second terminal"
COLAB_TITLE = "Agent Harness · Colab"
MODEL_ID = "gpt-5.6-luna"                     # formaggio/config.py:9 (container/06)
KEY_VAR = "OPENAI_API_KEY"
KEY_PLACEHOLDER = "YOUR_OPENAI_API_KEY"       # the README's placeholder (never a real-looking key)
KEY_MASKED = "YOUR_OPE*******_KEY"            # OpenAI's masked echo of it (container/10 line 11)
VENDOR = "vendor@example.com"                 # the recipient allowlist (expected/colab-c14 line 9)
RUN_MANAGER = "7409b343679a457490c94fb7512faa31"   # the manager-approval fixture run (container/71)
RUN_FAILED = "536c6c4812c049c495a9988ed754ee49"    # the first live Act 1 run (container/73)
FINGERPRINT16 = "e8caf06b29df9c58"            # first 16 characters of the approval fingerprint (container/71:46)
GUIDE = "MLOps_Learning · guides/L07-agents-2-harness.md"

# ------------------------------------------------------------------ layout
BOTTOM = -3.5                    # terminal bottom edge (fixed when it grows or shrinks)
TRACK_LEFT, TRACK_TOP = -6.5, 3.5
TERM_W, TERM_PT = 12.6, 22
TOPCHIP_Y = 2.66                 # a one-line top-band chip: centre y (under the tracker, bottom 2.925;
                                 #   above a terminal of up to 12 rows, top 2.19)
TOPCHIP_TALL_Y = 2.87            # with a 13-row terminal (top 2.59): right of the tracker (x >= -1.9),
CHIP_RIGHT = 6.55                #   under the lecture tag (y 3.13..3.6)
MINI_W, MINI_H = 3.2, 1.9        # the V1 mini-map (glyph only)
MINI_CENTER = np.array([4.95, -2.6, 0])          # bottom right, nothing else down there
MINI_ABOVE_STRIP = np.array([4.95, -0.33, 0])    # bottom right, above a 3-row strip (top STRIP_TOP -1.44)

# ------------------------------------------------------------------ README / notebook trackers
SECTIONS = {
    # dlops-io/agent-harness README.md @ e25dfe9 (script.md "Trackers"; head "README" or "Colab")
    "Start": ("README", "Setup › Start container", ["Make secrets", "Export key", "Run script", "Key inside"]),
    "Verify": ("README", "Setup › Verify", ["Check SDK", "Run tests", "Show logs"]),
    "Model": ("README", "Setup › Model", ["Check model"]),
    "Notebook": ("README", "Setup › Notebook path", ["Notebook tests", "Chat-view tests"]),
    "Colab": ("Colab", "Agent Harness", ["Copy notebook", "Add secret", "Setup cells"]),
    "Agent": ("README", "1 · Agent and tools", ["Run Act 1", "Show JSON", "Add harness", "Missing details"]),
    "Context": ("README", "2 · Context", ["Compare modes", "Basic run", "Enriched run", "Override run",
                                          "Act 3 preview", "Evaluate live", "View report",
                                          "Preview context", "Baseline run"]),
    "Act3": ("README", "3 · Harness › Act 3", ["Standard order", "Before: blocked", "After: revised",
                                               "Manager approval", "Out of stock", "Notebook cell"]),
    "Act4": ("README", "3 · Harness › Act 4", ["Run Act 4", "Compaction demo", "Remember preference",
                                               "Second visit", "Notebook cell"]),
    "Skills": ("README", "4 · Skills", ["Run Act 5", "Stock question", "Full sourcing", "Notebook cell"]),
    "Systems": ("README", "5 · Agent systems", ["Notebook cell", "Run Act 6", "Two orders"]),
    "Eval1": ("README", "6 · Evaluation › Step 1", ["List runs", "Inspect run"]),
    "Eval2": ("README", "6 · Evaluation › Step 2", ["Fixture batch", "Read report", "View report",
                                                    "HTML output", "Colab database"]),
    "Eval3": ("README", "6 · Evaluation › Step 3", ["Live batch A", "Copy prompt", "Edit prompt",
                                                    "Live batch B", "Compare"]),
    "Eval4": ("README", "6 · Evaluation › Step 4", ["Human review"]),
    "Res": ("README", "7 · Resources", ["CLI help", "Reflection"]),
    # not in the README: every step is an extra (the section name says so; no caption_extra needed)
    "Down": ("README", "Teardown · extra", ["Exit", "Check Docker", "Outputs", "Remove image"]),
}
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


def lref(slides: str) -> VGroup:
    """The GREY "Lecture 7 · slides 20–24" tag, top right (lecture_ref(7, slides))."""
    return lecture_ref(7, slides)


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



# ------------------------------------------------------------------ captures and sources
FOLDERS = ("laptop", "container", "expected")
NEVER_FILES = {"laptop/07-docker-shell.plain.txt"}     # the build log: the capture's proxy and CA lines
NEVER_CAPTURE = {   # file lines the script never shows (BRIEF.md "Things never to do")
    "laptop/09-x-docker-images.txt": {2, 3, 4},       # 2, 3 only via .cut (no CONTENT SIZE); 4 = the capture's base
    "laptop/10-x-container-env.txt": {3},             # the GCP_PROJECT value
    "container/00-x-whoami.txt": {9},                 # the GCP_PROJECT value
}
CUT_OK = {("laptop/09-x-docker-images.txt", 2): "DISK USAGE",
          ("laptop/09-x-docker-images.txt", 3): "1.77GB"}

# The 401 a placeholder key produces (BRIEF.md "Running example"; script.md "The 401 folds")
_E401_HEAD = "Error code: 401"
_E401_LONG = "Error code: 401 - {'error': {'message': 'Incorrect API key provided: YOUR_OPE*******_KEY."


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

    def as401(self, n: int, short: bool = False, until: str | None = None) -> tuple:
        """Line n (a '❌ Model call 1 failed: …' or 'Run stopped: …' line) folded as the script's
        'N as 401' (long: "Model call 1 failed: (… Error code: 401 - {'error': {'message': 'Incorrect
        API key provided: YOUR_OPE*******_KEY. …", print it with wrap=True: 2 rows) or 'N as 401s'
        (short=True: "Model call 1 failed: (… Error code: 401 …", 1 row). until="You can find your
        API key at" keeps the message up to there (S04: 3 rows). Returns (text, ERR); every piece
        is the line's own text, the '…' print GREY."""
        s = self.line(n)
        head = s.strip()
        k = head.find(": (")
        if k < 0 or _E401_HEAD not in head:
            raise ValueError(f"{self.name} line {n} is not a 401 line: {head[:60]!r}")
        lead = head[:k + 3]                        # "Model call 1 failed: (" / "Run stopped: ("
        if short:
            return f"{lead}… {_E401_HEAD} …", ERR
        if until:
            a = head.find(_E401_HEAD)
            b = head.find(until, a)
            if b < 0:
                raise ValueError(f"{until!r} not in {self.name} line {n}")
            return f"{lead}… {head[a:b + len(until)]} …", ERR
        if _E401_LONG not in head:
            raise ValueError(f"{self.name} line {n}: the long 401 text is not in it")
        return f"{lead}… {_E401_LONG} …", ERR

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


@lru_cache(maxsize=None)
def _load_capture(folder: str, fname: str) -> tuple:
    p = TERMINAL / folder / fname
    text = p.read_bytes().decode("utf-8")              # no newline translation: lines as sed counts them
    raw = [unname(ln.rstrip("\r").split("\r")[-1].expandtabs(8)) for ln in text.rstrip("\n").split("\n")]
    header = ""
    if raw and raw[0].startswith("# "):           # expected/*.txt: a provenance header first
        header, raw = raw[0], raw[1:]
    off = 2 if header else 1                      # file line number of raw[0]
    cmd = ""
    if raw and raw[0].startswith("$ "):
        cmd, raw, off = raw[0][2:], raw[1:], off + 1
    code = 0
    if raw and re.fullmatch(r"\[exit -?\d+\]", raw[-1]):
        code = int(raw[-1][6:-1])
        raw = raw[:-1]
    return cmd, tuple(raw), code, off, header


def capture(name: str, folder: str | None = None) -> Capture:
    """assets/terminal/<folder>/<name>.txt parsed, the customer IDs masked; capture("10",
    "container") finds 10-act1-standard.txt; capture("container/10") works too; expected files by
    name: capture("expected/colab-c23-agent-harness"). Fails loudly if missing: never show an
    output that wasn't captured."""
    if folder is None:
        folder, _, name = name.rpartition("/")
        if not folder:
            raise ValueError("capture(name, folder): name the folder")
    if folder == "capture-only":
        raise ValueError("capture-only/ is plumbing: never shown")
    if folder not in FOLDERS:
        raise ValueError(f"unknown capture folder {folder!r} (folders: {FOLDERS})")
    p = _find_capture(name, folder)
    key = f"{folder}/{p.name}"
    if key in NEVER_FILES:
        raise ValueError(f"{key} is never shown (BRIEF.md 'Things never to do')")
    cmd, raw, code, off, header = _load_capture(folder, p.name)
    return Capture(key, cmd, list(raw), code, off, header)


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


NEVER_SOURCE = {"docker-shell.sh": {10}}          # the GCP_PROJECT value


def src_path(name: str) -> str:
    """Resolve a source name under assets/source (the repo's own relative paths; Colab cells as
    "colab/cell-NN.py|.md"). Raises for files never shown (Colab cell 0, the notebooks folder)."""
    if not (SOURCE / name).is_file():
        raise FileNotFoundError(f"assets/source/{name} not found")
    if re.match(r"colab/cell-00\b", name):
        raise ValueError(f"{name}: the Colab's cell 0 (the course header) is never shown")
    if name.startswith("notebooks/"):
        raise ValueError(f"{name}: the repo notebooks are not shown (cells hold staff names; use the "
                         "README's notebook cells)")
    return name


def source_text(name: str) -> str:
    """A tutorial file, the customer IDs masked."""
    return _ID_RE.sub(lambda m: _IDS[m.group(0).lower()],
                      (SOURCE / src_path(name)).read_text(encoding="utf-8"))


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


def _source_lines(name: str, nums, strip_emoji_: bool = False) -> dict[int, str]:
    path = src_path(name)
    lines = source_text(name).split("\n")
    bad = NEVER_SOURCE.get(path, set()) & set(nums)
    if bad:
        raise ValueError(f"{path}: lines {sorted(bad)} are never shown (BRIEF.md 'Things never to do')")
    out = {}
    for n in nums:
        if not 1 <= n <= len(lines):
            raise IndexError(f"{path} has {len(lines)} lines (asked for {n})")
        s = lines[n - 1].expandtabs(4)
        if path == "data/customers.json" and re.match(r'\s*"name"\s*:', s):
            raise ValueError("data/customers.json: a 'name' line is never shown (BRIEF.md 'Names')")
        guard_names(s)
        out[n] = _emoji_guard(s, f"{path} line {n}", strip_emoji_)
    return out


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


# ------------------------------------------------------------------ facts from the captures
def _c23_trace() -> list[dict]:
    """The staff's recorded Act 1 run (expected/colab-c23 lines 7-56): one dict per model call:
    call, msgs (input messages), requested (tool or None), tokens_in, tokens_out, result (the
    tool's result line, emoji stripped, or None), lines {key: file line}."""
    c = capture("expected/colab-c23-agent-harness")
    calls: list[dict] = []
    for n in range(7, 57):
        s = c.line(n).strip()
        m = re.match(r"Model call (\d+)", s)
        if m:
            calls.append({"call": int(m.group(1)), "msgs": None, "requested": None, "tokens_in": None,
                          "tokens_out": None, "result": None, "lines": {"call": n}})
            continue
        if not calls:
            continue
        d = calls[-1]
        if (m := re.match(r"Input: (\d+) conversation messages", s)):
            d["msgs"], d["lines"]["input"] = int(m.group(1)), n
        elif (m := re.match(r"Requested tools: (\w+)", s)):
            d["requested"], d["lines"]["requested"] = m.group(1), n
        elif s.startswith("Response received"):
            d["lines"]["response"] = n
        elif (m := re.search(r"([\d.]+)s · (\d+) input tokens · (\d+) output tokens", s)):
            d["tokens_in"], d["tokens_out"], d["lines"]["tokens"] = int(m.group(2)), int(m.group(3)), n
        elif (m := re.match(r"Tool call (\d+): (\w+)", s)):
            d["lines"]["tool_call"] = n
        elif (m := re.match(r"Result \([\d.]+s\): (.*)", s)):
            d["result"], d["lines"]["result"] = m.group(1), n
    return calls


C23 = _c23_trace()
TOOLS_ACT1 = tuple(t.strip() for t in capture("container/10").line(10).split(":", 1)[1].split(","))
TOKENS_IN = tuple(d["tokens_in"] for d in C23)          # 1,942 … 4,540 (six calls)
TOKENS_OUT = tuple(d["tokens_out"] for d in C23)
MSGS = tuple(d["msgs"] for d in C23)                    # 1, 3, 5, 7, 9, 11


def _catalog() -> list[dict]:
    return json.loads((SOURCE / "data" / "catalog.json").read_text(encoding="utf-8"))


CATALOG = _catalog()
CHEESES = tuple(p["product_id"] for p in CATALOG)       # the twelve, in catalog order


def _preview_context() -> dict:
    """container/27 (python cli.py --preview-context --scenario standard) parsed as JSON."""
    c = capture("container/27")
    return json.loads("\n".join(c.lines))


_PC = _preview_context()
EXCLUDED = {e["product_id"]: e["reasons"][0] for e in _PC["enriched"]["excluded_products"]}
SURVIVORS = tuple(p["product_id"] for src in _PC["enriched"]["sources"]
                  for p in (src.get("content") or {}).get("candidates", []))
SIEVES = (("stock ≥ 100 g", "insufficient_stock_for_minimum"),
          ("no raw milk → PA", "fictional_shipping_policy"),
          ("no nut allergens", "allergen_conflict"))
PLANNER_TOOLS = tuple(t.strip() for t in capture("container/40").line(8).split(":", 1)[1].split(","))
# ------------------------------------------------------------------ small text helpers
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


# ------------------------------------------------------------------ terminal helpers
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
    """The rows that _L7Terminal.print printed for item k of its `lines` (one row, or the rows a
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


class _L7Terminal(Terminal):
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


def term(prompt: str = P_REPO, rows: int = 12, title: str | None = None, container: bool = False,
         top: float | None = None, width: float = TERM_W, size: float = TERM_PT) -> Terminal:
    """The house terminal (full width, 22 pt, 65 characters a row, at most 13 rows), bottom edge
    at BOTTOM, or its top edge at `top`. container=True: inside the agent-harness container (TEAL
    frame, title CTR_TITLE, prompt P_CTR unless `prompt` is given). Laptop: title "laptop"."""
    if rows > 13:
        raise ValueError("a house terminal has at most 13 rows (script.md 'Terminal width')")
    if container and prompt == P_REPO:
        prompt = P_CTR
    ttl = title or (CTR_TITLE if container else LAPTOP_TITLE)
    t = _L7Terminal(prompt=prompt, width=width, rows=rows, size=size, title=ttl)
    if container:
        t.box.set_stroke(CTR, 3)
        t.title.set_color(CTR)
    y = (top - t.box.get_top()[1]) if top is not None else (BOTTOM - t.box.get_bottom()[1])
    t.shift(np.array([-t.box.get_center()[0], y, 0]))
    return t


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


def enter_container(t: Terminal, prompt: str = P_CTR, title: str = CTR_TITLE) -> list:
    """Animations: the frame turns TEAL, the title becomes "container · agent-harness" (old title
    out, then the new one in); the prompt becomes `prompt` for the next typed line."""
    t.set_prompt(prompt)
    new = mono(title, CAPTION, CTR).move_to(t.title)
    return [t.box.animate.set_stroke(CTR, 3), *_swap_title(t, new)]


def leave_container(t: Terminal, prompt: str = P_REPO, title: str = LAPTOP_TITLE) -> list:
    """Animations: back on the laptop (GREY frame, title `title` swapped in, prompt `prompt`)."""
    t.set_prompt(prompt)
    new = mono(title, CAPTION, S.GREY).move_to(t.title)
    return [t.box.animate.set_stroke(S.GREY_DARK, 2), *_swap_title(t, new)]


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




# ------------------------------------------------------------------ tags and badges
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


def recorded_tag(s: str = "recorded · the staff's saved Colab run") -> VGroup:
    """The tag of every RECORDED box (the staff's saved Colab outputs; only Act 1 has live answers)."""
    return grey_tag(s)


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


def live_tag() -> VGroup:
    """GOLD, beside every typed live command."""
    return _keep(tag("live · billed per token", COST))


def offline_tag(s: str = "offline · free") -> VGroup:
    """GREEN: nothing is billed (tests, --fixture, --preview-context, reports, --compare …)."""
    return _keep(tag(s, HARNESS))


def cost_tag(s: str = "live · billed per token") -> VGroup:
    return _keep(tag(s, COST))


def cost_chip(s: str) -> VGroup:
    """A GOLD chip counting live runs ("2 runs", "12 runs", "4 runs")."""
    return _keep(chip(s, COST, size=CAPTION))


def test_tag() -> VGroup:
    """YELLOW 'TEST decision' (beside a --manager-decision / --email-decision flag, which gets a
    YELLOW outline: col_box(..., color=TURN))."""
    return _keep(tag("TEST decision", TURN))


def template_tag() -> VGroup:
    return grey_tag("a template")


def erratum_tag(note_: str | None = None) -> VGroup:
    return grey_tag("erratum" + (f" · {note_}" if note_ else ""))


def differ_tag() -> VGroup:
    """On run IDs, ticket IDs, container IDs, receipt IDs."""
    return grey_tag("your numbers will differ")


def harmless_tag() -> VGroup:
    return grey_tag("harmless")


def preview_tag() -> VGroup:
    return grey_tag("preview")


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


def human_stamp(two_rows: bool = False, size: float = TAG) -> VGroup:
    """The YELLOW "a human decides" stamp (outlined, opaque dark fill, bold); two_rows=True stacks
    "a human" over "decides" (1.3 wide: fits a cell's end or S01's band). .frame .text"""
    if not two_rows:
        return stamp("a human decides", TURN, size=size, angle=0.0)
    rows = VGroup(sans("a human", size, TURN, weight="BOLD"), sans("decides", size, TURN, weight="BOLD"))
    rows.arrange(DOWN, buff=0.02)
    fr = RoundedRectangle(width=rows.width + 0.24, height=rows.height + 0.14, corner_radius=0.06,
                          stroke_color=TURN, stroke_width=3).set_fill(S.BG, 0.85)
    rows.move_to(fr)
    g = VGroup(fr, rows)
    g.frame, g.text = fr, rows
    return _keep(g)


def fix_chip(text: str, color: str = HARNESS, font: str | None = None) -> VGroup:
    """A GREEN "the fix" chip (serif text; font=MONO for code)."""
    return _keep(chip(text, color, size=CAPTION, font=font))


def mask_chip(which: int = 1, size: float = CAPTION) -> VGroup:
    """The GREY chip standing for a customer ID (‹customer 1› / ‹customer 2›)."""
    return _keep(chip(MASKS[which - 1], S.GREY, size=size, font=MONO))


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
# ------------------------------------------------------------------ panels and cards
_LANG = {".py": "python", ".toml": "toml", ".sh": "bash", ".md": "markdown", ".yaml": "yaml",
         ".yml": "yaml", ".json": "json", ".html": "html", ".txt": "text", ".lock": "toml"}


def _lang(path: str) -> str:
    p = Path(path)
    if p.name == "Dockerfile":
        return "docker"
    if p.name in (".gitignore", ".dockerignore") or p.name.startswith(".env"):
        return "text"
    return _LANG.get(p.suffix, "text")


def shown_path(name: str) -> str:
    """The path as the viewer sees it: the repo's own relative path ("formaggio/shop/checkout.py");
    a Colab cell "colab/cell-10.py" -> "Agent Harness · cell 10" (0-based, as in assets/source)."""
    p = src_path(name)
    m = re.match(r"colab/cell-(\d+)", p)
    if m:
        return f"Agent Harness · cell {int(m.group(1))}"
    return p


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


def quote_card(a: int, b: int | None = None, lines: list[str] | None = None, wrap: int = 88,
               width: float | None = None, expected: bool = True, header: str | None = None) -> VGroup:
    """QUOTE(README.md: a–b): a GREY quote card headed "README.md · lines a–b" with the README's
    words (inline `code` mono), never styled as output; the GREY `expected` tag at the header's
    right (expected=False: none). lines= replaces the words with excerpts of those lines (each a
    sub-string you checked: excerpt chips are stricter); rows wrap at `wrap` characters. Multi-line
    QUOTE cards only above a 3-row strip or with no terminal (one-line: top_chip). .frame .rows
    .header .tag"""
    where = header or (f"README.md · line {a}" if b is None or b == a else f"README.md · lines {a}–{b}")
    src = lines if lines is not None else readme(a, b)
    if lines is not None:
        whole = " ".join(readme(a, b))
        for ln in lines:
            for frag in ln.replace("`", "").split("…"):
                f = re.sub(r"\s+", " ", frag).strip()
                if f and f not in re.sub(r"\s+", " ", whole.replace("`", "")):
                    raise ValueError(f"quote_card: {f!r} is not in README.md {a}-{b}")
    rows_txt = [r for ln in src if ln.strip() for r in _wrap_words(ln, wrap)]
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
                 tag_: bool = True) -> VGroup:
    """RECORDED(expected/colab-…: lines): the staff's saved Colab output as an output box (never a
    terminal frame), emoji stripped and coloured, the customer IDs masked; header "Agent Harness ·
    cell 23 · saved output" (from the file name) unless given; the GREY tag `recorded · the staff's
    saved Colab run` above its right end (tag_=False: none). spec as in Capture.out. .frame .rows
    .header .tag"""
    c = capture(name if "/" in name else f"expected/{name}")
    m = re.search(r"colab-c(\d+)", c.name)
    hd = header if header is not None else (f"Agent Harness · cell {int(m.group(1))} · saved output" if m else None)
    g = output_box(c.out(*spec), hd, width=width)
    g.tag = None
    if tag_:
        tg = recorded_tag()
        tg.next_to(g.frame, UP, buff=0.08).align_to(g.frame, RIGHT)
        if g.header is not None and tg.get_left()[0] < g.header.get_right()[0] + 0.2:
            tg.next_to(g.frame, DOWN, buff=0.08).align_to(g.frame, RIGHT)
        g.add(tg)
        g.tag = tg
    return g


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


def what_if_frame(width: float = 12.9, top: float = 2.6, bottom: float = -3.58,
                  title: str = "what if · just watch", note_: str | None = None) -> VGroup:
    """The RED dashed frame around a "what if" demo, so it never looks like the viewer's own
    terminal. Built in place (centred on x = 0): y from `bottom` to `top`, so the tracker band
    above stays free and a full-width terminal of up to 12 rows fits inside. The title tag
    straddles the top border at the left, an optional GREY note at the right. .frame .title .note"""
    fr = box(width, top - bottom, ERR, dashed=True, stroke=3).move_to([0, (top + bottom) / 2, 0])
    t = _keep(tag(title, ERR))
    t.move_to(fr.get_corner(UP + LEFT) + np.array([0.3 + t.width / 2, 0, 0]))
    g = VGroup(fr, t)
    g.frame, g.title, g.note = fr, t, None
    if note_:
        n = grey_tag(note_)
        n.move_to(fr.get_corner(UP + RIGHT) + np.array([-0.3 - n.width / 2, 0, 0]))
        g.add(n)
        g.note = n
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


class CallCounter(VGroup):
    """The GOLD call counter of S02 ("1 call", ticking to "11 calls"): no updaters, the number
    ticks one by one. .count_to(n, run_time) -> anim  .with_time("39.34 s") -> anim (a GREY
    " · 39.34 s" after it; the text comes from a capture). .text .n"""

    def __init__(self, n: int = 0, unit: str = "call", size: float = 24, color: str = COST, **kw):
        super().__init__(**kw)
        self.unit, self.size, self.hi_color, self.n = unit, size, color, n
        self.text = self._make(n)
        self.add(self.text)
        self.time = None
        _keep(self)

    def _make(self, n: int) -> Text:
        return label(f"{n} {self.unit}{'' if n == 1 else 's'}", self.size, self.hi_color)

    def count_to(self, n: int, run_time: float = 1.0):
        """Animation: the count ticks one by one to n, each text swapped old out, then new in
        (_swap_text; a Transform between two strings scrambles the letters). .text is the last
        new text right after the call."""
        steps = list(range(self.n + 1, n + 1)) or [n]
        anims = []
        old = self.text
        for k in steps:
            new = self._make(k).move_to(old, aligned_edge=LEFT)
            anims.append(AnimationGroup(*_swap_text(self, old, new), run_time=run_time / len(steps)))
            old = new
        self.text = old
        self.n = n
        return Succession(*anims)

    def with_time(self, text: str):
        t = label(f"· {text}", self.size, self.hi_color).next_to(self.text, RIGHT, buff=0.15)
        self.time = t
        self.add(t)
        return FadeIn(t, shift=LEFT * 0.1)


def colab_frame(title: str = COLAB_TITLE, width: float = 12.9, top: float = 2.75, bottom: float = -3.5,
                size: float = 22) -> VGroup:
    """A Colab notebook drawn schematically: a BLUE rounded frame (Google's VM) with the notebook's
    name in a tab on the top border and the `illustration` tag at the top right. Built in place
    (centred on x = 0, y from `bottom` to `top`). .frame .title .tag"""
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


# ------------------------------------------------------------------ glyphs
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


def padlock(h: float = 0.36, color: str = S.GREY) -> VGroup:
    """A padlock (shut). .body .shackle; unlock(lock) -> anim (the shackle lifts and turns)."""
    body = RoundedRectangle(width=h * 0.9, height=h * 0.62, corner_radius=h * 0.08,
                            stroke_color=color, stroke_width=2.5).set_fill(color, 0.3)
    sh = Arc(radius=h * 0.27, start_angle=0, angle=PI, stroke_color=color, stroke_width=3.5)
    sh.next_to(body, UP, buff=0)
    legs = VGroup(Line(sh.get_start(), sh.get_start() + DOWN * h * 0.08, color=color, stroke_width=3.5),
                  Line(sh.get_end(), sh.get_end() + DOWN * h * 0.08, color=color, stroke_width=3.5))
    shackle = VGroup(sh, legs)
    g = VGroup(shackle, body)
    g.body, g.shackle = body, shackle
    return _keep(g)


def person(color: str = S.GREY, h: float = 0.62) -> VGroup:
    """A person glyph (outline): a head over shoulders. The human who decides: person_icon(TURN)
    (explainer.components, filled) with hand(TURN)."""
    head = Circle(radius=h * 0.2, stroke_color=color, stroke_width=3).set_fill(color, 0.25)
    body = Arc(radius=h * 0.38, start_angle=0, angle=PI, stroke_color=color, stroke_width=3)
    body.close_path()
    body.set_fill(color, 0.2)
    head.next_to(body, UP, buff=0.04)
    return _keep(VGroup(body, head))


def pencil(h: float = 0.55, color: str = TURN) -> VGroup:
    """A pencil glyph, tip at bottom-left (the model's pen: pencil(color=CLOUD)). .tip_point()"""
    w = h * 0.22
    shaft = Rectangle(width=w, height=h, stroke_color=color, stroke_width=2.5).set_fill(color, 0.25)
    tip = Polygon(shaft.get_corner(DOWN + LEFT), shaft.get_corner(DOWN + RIGHT),
                  shaft.get_bottom() + DOWN * w * 1.1, stroke_color=color, stroke_width=2.5).set_fill(color, 0.6)
    g = VGroup(shaft, tip).rotate(-PI / 4)
    g.tip_point = lambda: tip.get_vertices()[2]
    return _keep(g)


def gear(r: float = 0.24, color: str = S.GREY) -> VGroup:
    """A small gear (your code runs: gear(color=CTR))."""
    teeth = VGroup(*[Rectangle(width=r * 0.38, height=r * 0.42, stroke_width=0).set_fill(color, 1)
                     .move_to(UP * r * 0.98).rotate(k * TAU / 8, about_point=ORIGIN) for k in range(8)])
    ring_ = Circle(radius=r * 0.8, stroke_width=0).set_fill(color, 1)
    hole = Circle(radius=r * 0.32, stroke_width=0).set_fill(S.BG, 1)
    return _keep(VGroup(teeth, ring_, hole))


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


def cylinder(w: float = 1.1, h: float = 1.3, color: str = HARNESS, fill: float = 0.18,
             stroke: float = 3) -> VGroup:
    """A database: a GREEN cylinder (outputs/observability.sqlite, customer_memory.sqlite) with two
    disk lines (opaque fill). .top .body .frame"""
    e = w * 0.28
    fc = _mix(color, fill)
    bottom = Ellipse(width=w, height=e).set_fill(fc, 1).set_stroke(color, stroke).shift(DOWN * h / 2)
    body = Rectangle(width=w, height=h).set_fill(fc, 1).set_stroke(width=0)
    sides = VGroup(Line([-w / 2, h / 2, 0], [-w / 2, -h / 2, 0]),
                   Line([w / 2, h / 2, 0], [w / 2, -h / 2, 0])).set_stroke(color, stroke)
    disks = VGroup()
    for y in (h / 6, -h / 6):
        a = Ellipse(width=w, height=e).set_fill(opacity=0).set_stroke(color, stroke * 0.6, opacity=0.7)
        a.pointwise_become_partial(a.copy(), 0.5, 1.0)
        disks.add(a.shift(UP * y))
    top = Ellipse(width=w, height=e).set_fill(_mix(color, min(1.0, fill * 1.9)), 1) \
        .set_stroke(color, stroke).shift(UP * h / 2)
    g = VGroup(bottom, body, sides, disks, top)
    g.top, g.body = top, body
    g.frame = VGroup(bottom, sides, disks, top)
    return g


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


def model_chip(name: str = MODEL_ID, size: float = CAPTION) -> VGroup:
    """A BLUE mono chip naming a model (gpt-5.6-luna)."""
    return _keep(chip(name, CLOUD, size=size, font=MONO))


def answer_bars(n: int = 3, w: float = 2.4, color: str = S.GREY, h: float = 0.12) -> VGroup:
    """Placeholder answer bars (no words): n rounded bars, the last one shorter."""
    bars = VGroup(*[RoundedRectangle(width=w * (0.55 if k == n - 1 else (1.0 - 0.08 * (k % 2))), height=h,
                                     corner_radius=h / 2, stroke_width=0).set_fill(color, 0.75)
                    for k in range(n)])
    bars.arrange(DOWN, aligned_edge=LEFT, buff=h * 1.1)
    return bars


def seal(r: float = 0.16, color: str = HARNESS) -> VGroup:
    """A small seal: a scalloped disc with a ring (S12: a skill file's GREEN SHA-256 snapshot;
    broken_seal() is the RED one of an edited copy)."""
    pts = []
    for k in range(24):
        a = k * TAU / 24
        rr = r * (1.0 if k % 2 == 0 else 0.86)
        pts.append([rr * np.cos(a), rr * np.sin(a), 0])
    disc = Polygon(*pts, stroke_color=color, stroke_width=2).set_fill(_mix(color, 0.55), 1)
    ring_ = Circle(radius=r * 0.55, stroke_color=S.BG, stroke_width=2)
    return _keep(VGroup(disc, ring_))


def diamond(text: str | None = None, color: str = S.GREY, w: float = 0.9, size: float = CAPTION) -> VGroup:
    """A decision diamond (who decides the next step); optional caption under it. .shape .caption"""
    sh = Polygon([0, w * 0.45, 0], [w / 2, 0, 0], [0, -w * 0.45, 0], [-w / 2, 0, 0],
                 stroke_color=color, stroke_width=3).set_fill(color, 0.15)
    g = VGroup(sh)
    g.shape, g.caption = sh, None
    if text:
        c = label(text, size, color).next_to(sh, DOWN, buff=0.1)
        g.add(c)
        g.caption = c
    return _keep(g)


def sticky_note(text: str, color: str = S.GREY, size: float = CAPTION, w: float | None = None) -> VGroup:
    """A sticky note (a rule written in a prompt): a square note with a folded corner, serif text
    ("\\n" splits rows). .frame .text"""
    t = VGroup(*[label(s, size, INK) for s in text.split("\n")]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    ww = max(w or 0, t.width + 0.75)
    hh = t.height + 0.5
    c = 0.22
    shape = Polygon([-ww / 2, hh / 2, 0], [ww / 2, hh / 2, 0], [ww / 2, -hh / 2 + c, 0],
                    [ww / 2 - c, -hh / 2, 0], [-ww / 2, -hh / 2, 0], stroke_color=color,
                    stroke_width=2.5).set_fill(_mix(color, 0.25), 1)
    fold = Polygon([ww / 2, -hh / 2 + c, 0], [ww / 2 - c, -hh / 2 + c, 0], [ww / 2 - c, -hh / 2, 0],
                   stroke_color=color, stroke_width=2).set_fill(_mix(color, 0.5), 1)
    t.move_to(shape).shift(LEFT * 0.1 + UP * 0.03)
    g = VGroup(shape, fold, t)
    g.frame, g.text = shape, t
    return _keep(g)


def receipt_token(path: str, color: str = DATA, size: float = CAPTION) -> VGroup:
    """The GREEN receipt: a slip with a zig-zag bottom edge and a mono text (a receipt ID, a path;
    masked). .frame .text"""
    t = mtext(path, size, INK)
    w, h = t.width + 0.5, t.height + 0.55
    pts = [[-w / 2, h / 2, 0], [w / 2, h / 2, 0], [w / 2, -h / 2 + 0.1, 0]]
    n = max(4, int(w / 0.25))
    for k in range(n + 1):
        x = w / 2 - k * w / n
        pts.append([x, -h / 2 + (0.0 if k % 2 else 0.1), 0])
    pts.append([-w / 2, h / 2, 0])
    shape = Polygon(*pts[:-1], stroke_color=color, stroke_width=2.5).set_fill(_mix(color, 0.18), 1)
    t.move_to(shape).shift(UP * 0.04)
    g = VGroup(shape, t)
    g.frame, g.text = shape, t
    return _keep(g)


def notebook_glyph(h: float = 0.7, color: str = CLOUD, check: bool = True) -> VGroup:
    """A notebook (a BLUE frame with cell bars; a GREEN check inside: the harness checked it)."""
    w = h * 1.25
    fr = RoundedRectangle(width=w, height=h, corner_radius=0.06, stroke_color=color,
                          stroke_width=2.5).set_fill(color, 0.08)
    cells = VGroup(*[RoundedRectangle(width=w * 0.5, height=h * 0.1, corner_radius=0.02, stroke_width=0)
                     .set_fill(color, 0.6) for _ in range(3)]).arrange(DOWN, buff=h * 0.1, aligned_edge=LEFT)
    cells.move_to(fr).align_to(fr, LEFT).shift(RIGHT * w * 0.1)
    g = VGroup(fr, cells)
    if check:
        g.add(check_mark(h * 0.4, DATA).move_to(fr.get_right() + LEFT * w * 0.2))
    return _keep(g)


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




def broken_seal(r: float = 0.16, color: str = ERR) -> VGroup:
    """The RED seal of an edited file (S12: a skill file changed during the run): seal + a crack."""
    g = seal(r, color)
    crack = VMobject(stroke_color=S.BG, stroke_width=3)
    crack.set_points_as_corners([[-r * 0.9, r * 0.5, 0], [-r * 0.1, r * 0.05, 0], [r * 0.15, r * 0.35, 0],
                                 [r * 0.9, -r * 0.6, 0]])
    g.add(crack)
    return _keep(g)


def unlock(lock, run_time: float = 0.5):
    """Animation: a padlock() opens (its shackle lifts and swings open)."""
    sh = lock.shackle
    pivot = sh.get_corner(DOWN + RIGHT)
    return Succession(sh.animate(run_time=run_time * 0.4).shift(UP * lock.body.height * 0.35),
                      Rotate(sh, angle=-PI / 2.2, about_point=pivot + UP * lock.body.height * 0.35,
                             run_time=run_time * 0.6))


def hand(color: str = TURN, h: float = 0.5) -> VGroup:
    """A hand glyph (palm, four fingers, a thumb; fingers up): YELLOW = a human decides, BLUE = the
    model reaching (S10: it finds no handle). .palm .tip() -> the fingertips' top centre."""
    w = h * 0.62
    palm = RoundedRectangle(width=w, height=h * 0.5, corner_radius=w * 0.22, stroke_color=color,
                            stroke_width=2.5).set_fill(color, 0.35)
    fingers = VGroup(*[RoundedRectangle(width=w * 0.2, height=h * (0.42 if k in (1, 2) else 0.36),
                                        corner_radius=w * 0.09, stroke_color=color, stroke_width=2)
                       .set_fill(color, 0.35) for k in range(4)]).arrange(RIGHT, buff=w * 0.05, aligned_edge=DOWN)
    fingers.next_to(palm, UP, buff=-0.04)
    thumb = RoundedRectangle(width=w * 0.2, height=h * 0.32, corner_radius=w * 0.09, stroke_color=color,
                             stroke_width=2).set_fill(color, 0.35).rotate(PI / 4)
    thumb.move_to(palm.get_left() + RIGHT * w * 0.02 + UP * h * 0.05)
    g = VGroup(thumb, fingers, palm)
    g.palm = palm
    g.tip = lambda: fingers.get_top()
    return _keep(g)


def cart_token(items=None, color: str = CLOUD, dashed: bool = False, size: float = CAPTION,
               scale: float = 1.0) -> VGroup:
    """A cart token (BLUE: the model proposed this cart; recolor_cart(...) turns it GREEN once the
    harness validated it, RED when rejected): a small cart glyph (0.8 x 0.5) and an optional row of
    item chips under it (["Comté", "Bûcheron", "Époisses"]). dashed=True: a scripted proposal.
    .glyph .items"""
    basket = Polygon([-0.3, 0.12, 0], [0.3, 0.12, 0], [0.22, -0.12, 0], [-0.22, -0.12, 0],
                     stroke_color=color, stroke_width=3).set_fill(color, 0.3)
    handle = Line([-0.3, 0.12, 0], [-0.4, 0.24, 0], color=color, stroke_width=3)
    wheels = VGroup(Dot([-0.14, -0.2, 0], radius=0.05, color=color), Dot([0.14, -0.2, 0], radius=0.05, color=color))
    gl = VGroup(basket, handle, wheels)
    if dashed:
        gl = VGroup(DashedVMobject(basket, num_dashes=14).set_stroke(color, 3), handle, wheels)
    if scale != 1.0:
        gl.scale(scale)
    g = VGroup(gl)
    g.glyph, g.items = gl, None
    if items:
        row = VGroup(*[chip(it, color, size=size, pad_x=0.14, pad_y=0.06) for it in items]).arrange(RIGHT, buff=0.08)
        row.next_to(gl, DOWN, buff=0.1)
        g.add(row)
        g.items = row
    return _keep(g)


def recolor_cart(cart, color: str) -> list:
    """Animations: a cart_token's glyph and item chip borders turn `color` (BLUE -> GREEN when the
    harness validates it, RED when it is rejected); the item names stay white."""
    anims = [m.animate.set_stroke(color) for m in cart.glyph.family_members_with_points()]
    if cart.items is not None:
        anims += [c.box.animate.set_stroke(color).set_fill(color, 0.16) for c in cart.items]
    return anims


def cheese_chip(pid: str, color: str = S.GREY, size: float = CAPTION, wedge: bool = False) -> VGroup:
    """A cheese product chip: the capture's product ID in mono (`comte`, `walnut_chevre`) on an
    opaque rounded chip in `color` (GREY while it falls, RED when a sieve stops it, GREEN in the
    tray); wedge=True adds a small GOLD wedge glyph at the left. .box .text .pid"""
    t = mono(pid, size, INK)
    row = t
    if wedge:
        w = Polygon([0, 0, 0], [0.22, 0, 0], [0.0, 0.14, 0], stroke_color=COST, stroke_width=2).set_fill(COST, 0.45)
        row = VGroup(w, t).arrange(RIGHT, buff=0.08)
    h = mono("|", size).height + 0.1
    b = box(row.width + 0.24, h, color, fill=S.BG, fill_opacity=0.9, radius=h / 2.6)
    row.move_to(b)
    g = VGroup(b, row)
    g.box, g.text, g.pid = b, t, pid
    return _keep(g)


def msg_card(w: float = 0.5, h: float = 0.16, color: str = S.GREY) -> VGroup:
    """A small message card glyph (no text) for message stacks: V2's stack, V6's jar."""
    r = RoundedRectangle(width=w, height=h, corner_radius=min(0.04, h / 3), stroke_color=color,
                         stroke_width=1.5).set_fill(_mix(color, 0.3), 1)
    return VGroup(r)


def gold_meter(label_text: str = "input tokens", value: int = 0, cap: int = 5000, w: float = 3.0,
               size: float = CAPTION) -> VGroup:
    """A GOLD token meter: "input tokens: 1,942" (a Counter) over a bar that fills to value/cap.
    .set_to(v, run_time=1.0) -> anim (bar and number together) .freeze() before it leaves.
    .bar .counter .frame"""
    cnt = Counter(label_text, value, color=COST, size=size)
    frame = RoundedRectangle(width=w, height=0.22, corner_radius=0.08, stroke_color=COST, stroke_width=2)
    frame.next_to(cnt, DOWN, buff=0.12).align_to(cnt, LEFT)
    bar = Rectangle(width=0.01, height=0.16, stroke_width=0).set_fill(COST, 0.75)

    def upd(m):
        k = max(0.002, min(1.0, cnt.tracker.get_value() / cap))
        m.stretch_to_fit_width(max(0.01, (frame.width - 0.06) * k))
        m.move_to([frame.get_left()[0] + 0.03 + m.width / 2, frame.get_center()[1], 0])
    bar.add_updater(upd)
    upd(bar)
    g = VGroup(cnt, frame, bar)
    g.bar, g.counter, g.frame = bar, cnt, frame
    g.set_to = lambda v, run_time=1.0: cnt.count_to(v, run_time)

    def freeze():
        bar.clear_updaters()
        cnt.freeze()
        return g
    g.freeze = freeze
    return _keep(g)
# ------------------------------------------------------------------ the set-piece base
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


class Gate(VGroup):
    """V8's gate, one look for every "is it done?" check: two posts, a bar, a label above. S08's
    "final response" (YELLOW, opens) and MaxTurnsExceeded (slams RED), S14's turnstile (FINAL,
    PENDING stamps, turns), S15's SUCCESS door (slot=True: a receipt slot on the right post).
    .open() .close() -> anim; .slam(colour=ERR, text=None) -> anim; .relabel(text, colour) ->
    anim; .stamp_on(card, text, colour) -> stamp (not added). .bar .lpost .rpost .caption .slot"""

    def __init__(self, text: str = "FINAL", color: str = TURN, gate_w: float = 1.4, gate_h: float = 1.7,
                 slot: bool = False, size: float = CAPTION, post_color: str = S.GREY, **kw):
        super().__init__(**kw)
        w, h = gate_w, gate_h
        py = max(-h / 2 + 0.15, h / 2 - w)        # the bar's height: raised, its tip stays under the label
        self.lpost = Line([-w / 2, -h / 2, 0], [-w / 2, h / 2, 0], color=post_color, stroke_width=6)
        self.rpost = Line([w / 2, -h / 2, 0], [w / 2, h / 2, 0], color=post_color, stroke_width=6)
        base = Line([-w / 2 - 0.22, -h / 2, 0], [w / 2 + 0.22, -h / 2, 0], color=post_color, stroke_width=4)
        self.bar = Line([-w / 2, py, 0], [w / 2, py, 0], color=color, stroke_width=9)
        self.hub = Dot([-w / 2, py, 0], radius=0.08, color=post_color)
        self.caption = sans(text, size, color, weight="BOLD")
        self.caption.move_to([0, max(h / 2, py + w) + 0.14 + self.caption.height / 2, 0])
        self.add(base, self.lpost, self.rpost, self.bar, self.hub, self.caption)
        self.slot = None
        if slot:
            s = RoundedRectangle(width=0.16, height=0.55, corner_radius=0.04, stroke_color=post_color,
                                 stroke_width=2).set_fill(S.BG, 1).move_to(self.rpost.get_center() + RIGHT * 0.2)
            self.slot = s
            self.add(s)
        self.is_open = False
        self.size = size
        _keep(self)

    def pivot(self):
        return self.hub.get_center()

    def open(self, run_time: float = 0.6):
        """Animation: the bar swings up (the gate opens)."""
        if self.is_open:
            return AnimationGroup()
        self.is_open = True
        return Rotate(self.bar, angle=PI / 2, about_point=self.pivot(), run_time=run_time)

    def close(self, run_time: float = 0.4):
        if not self.is_open:
            return AnimationGroup()
        self.is_open = False
        return Rotate(self.bar, angle=-PI / 2, about_point=self.pivot(), run_time=run_time)

    def relabel(self, text: str, color: str | None = None, run_time: float = 1.0):
        """Animation: the label above the gate changes (.caption is the new label afterwards),
        old label out, then the new one in (_swap_text; the glyph morph of a ReplacementTransform
        scrambled the letters). The new label takes the old one's place among the gate's members
        at once (S08 builder: relabel left the gate holding the old label), so it moves and fades
        with the gate. run_time 1.0, as the ReplacementTransform's default."""
        col = color or self.bar.get_color()
        new = sans(text, self.size, col, weight="BOLD").move_to(self.caption)
        old, self.caption = self.caption, new
        return AnimationGroup(*_swap_text(self, old, new), run_time=run_time)

    def slam(self, color: str = ERR, text: str | None = None, run_time: float = 0.35):
        """Animation: the bar turns `color` and slams down (if open); the label becomes `text`."""
        self.bar.set_color(color)
        anims = []
        if self.is_open:
            self.is_open = False
            anims.append(Rotate(self.bar, angle=-PI / 2, about_point=self.pivot(), rate_func=rush_into,
                                run_time=run_time))
        else:
            anims.append(Indicate(self.bar, color=color, scale_factor=1.05, run_time=run_time))
        if text:
            anims.append(self.relabel(text, color))
        return AnimationGroup(*anims)

    def stamp_on(self, card, text: str = "PENDING", color: str = TURN) -> VGroup:
        """A stamp placed on `card`'s top-right area (not added)."""
        s = stamp(text, color)
        return s.move_to(card.get_corner(UP + RIGHT) + np.array([-s.width / 2 - 0.15, 0, 0]))




# ------------------------------------------------------------------ text that fits a box
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


# ------------------------------------------------------------------ V1 · two columns -> the action boundary
class TwoColumns(Piece):
    """V1, first form (S01, the hook): a BLUE column "the model proposes" (left) and a GREEN column
    "the harness decides" (right), a dim YELLOW stamp "a human decides" inside the right column's
    lower right corner. Default 12.4 x 4.8, centred at ORIGIN; TwoColumns(height=1.1, words=False)
    is S01's band at the top (no room for cards).
    Parts: left right human words (words hidden: write them with .write_word(i)).
        .slot(side, i, n=2) -> point: the centre of card i of n stacked in that column ("left" /
            "right"); cards are yours (move them there, then attach them if the piece moves)
        .write_word(i) -> anim: GREEN word i of WORDS ("the loop", "its limits", "its context",
            "its checks") writes in under the GREEN header
        .human_on() -> anim: the stamp to full opacity"""

    WORDS = ("the loop", "its limits", "its context", "its checks")

    def __init__(self, width: float = 12.4, height: float = 4.8, gap: float = 0.4, size: float = 24,
                 words: bool = True, **kw):
        super().__init__(**kw)
        cw = (width - gap) / 2
        self.col_w, self.col_h = cw, height
        cols = {}
        for side, col, title, x in (("left", CLOUD, "the model proposes", -(cw + gap) / 2),
                                    ("right", HARNESS, "the harness decides", (cw + gap) / 2)):
            fr = box(cw, height, col, fill_opacity=0.05, stroke=3).move_to([x, 0, 0])
            hd = sans(title, size, col, weight="BOLD")
            if height > 2.0:
                hd.move_to(fr.get_top() + DOWN * (0.18 + hd.height / 2))
            else:                               # the band: titles at the left, the stamp at the right
                hd.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.3)
            cols[side] = VGroup(fr, hd)
            cols[side].frame, cols[side].title = fr, hd
            self.part(side, cols[side])
        self.cols = cols
        st = human_stamp(two_rows=height <= 2.0)
        if height > 2.0:
            st.move_to(cols["right"][0].get_corner(DOWN + RIGHT) + np.array([-0.2 - st.width / 2, 0.2 + st.height / 2, 0]))
        else:
            st.move_to(cols["right"][0]).align_to(cols["right"][0], RIGHT).shift(LEFT * 0.25)
        st.set_opacity(0.45)
        self.part("human", st)
        self.word_mobs = VGroup()
        if words and height > 2.0:
            ws = [label(w, CAPTION, HARNESS) for w in self.WORDS]
            row = VGroup(*ws).arrange(RIGHT, buff=0.35)
            row.next_to(cols["right"].title, DOWN, buff=0.18)
            self.word_mobs = row
            self.part("words", row, shown=False)
        self.move_to(ORIGIN)

    def _top_free(self, side):
        c = self.cols[side]
        top = c.title.get_bottom()[1] - 0.2
        if side == "right" and len(self.word_mobs):
            top = self.word_mobs.get_bottom()[1] - 0.2
        return top

    def slot(self, side: str, i: int = 0, n: int = 2):
        fr = self.cols[side].frame
        top, bot = self._top_free(side), fr.get_bottom()[1] + 0.2
        if side == "right":
            bot = self.parts["human"].get_top()[1] + 0.1
        h = (top - bot) / n
        return np.array([fr.get_center()[0], top - h * (i + 0.5), 0])

    def write_word(self, i: int, run_time: float = 0.4):
        w = self.word_mobs[i]
        self.parts["words"].hidden = False
        return _Reveal(w, shift=UP * 0.08, run_time=run_time)

    def human_on(self, run_time: float = 0.5):
        st = self.parts["human"]
        return st.animate(run_time=run_time).set_opacity(1.0)


BOUNDARY_ROWS = ("control", "tools", "context", "verify", "sub")
BOUNDARY_NAMES = {"control": "Control flow", "tools": "Tools", "context": "Context & memory",
                  "verify": "Verification", "sub": "Sub agents"}
BOUNDARY_BLUE = {"control": "the plan · when to stop", "tools": "which tool · which arguments",
                 "context": "what to retrieve · which skill · what to remember",
                 "verify": "self-critique · revise from feedback", "sub": "when to delegate"}
# what each act writes into the GREEN cells (script.md "V1 cells"), in order
BOUNDARY_FILLS = (
    (1, "control", "Budget · admission"), (1, "tools", "@tool schemas · counted, audited calls"),
    (1, "verify", "CartCheck"), (2, "context", "the packet in the data lane"),
    (3, "control", "the workflow graph"), (3, "verify", "validate · revalidate at checkout"),
    (4, "tools", "approval on save"), (4, "context", "capsule · compaction · host-written memory"),
    (5, "context", "skills guide, never permit"), (6, "sub", "narrow tools · separate counters · one clock"),
)
# the full table of the recap (S16): the GREEN cells shortened to fit at 20 pt
BOUNDARY_RECAP = {"control": "Budget · admission · the graph", "tools": "@tool schemas · audit · approval on save",
                  "context": "data-lane packet · capsule · host-only memory · skills",
                  "verify": "CartCheck · validate · revalidate",
                  "sub": "narrow tools · separate counters · one clock"}
MOVE_LEFT = ("Move LEFT", "novel goals · a capable model")
MOVE_RIGHT = ("Move RIGHT", "high stakes · irreversible · predictable · audit")


class ActionBoundary(Piece):
    """V1 as slide 22's table (S05 builds it; S07 end and S11 at half size; S08 small; S16 full and
    filled): a header row (BLUE "the model proposes", a PINK double arrow "who decides?", GREEN
    "the harness decides"), five GREY concern pills down the middle (BOUNDARY_NAMES), BLUE cells
    left (BOUNDARY_BLUE), GREEN cells right (empty until .fill), and under it the two move arrows
    (BLUE "Move LEFT" pointing left, GREEN "Move RIGHT" pointing right, each with its reasons).
        ActionBoundary()                        12.6 x 6.2 (moves=True; 5.1 without), built centred
                                                at ORIGIN; a row is as tall as its BLUE text needs
        ActionBoundary(width=8.6, row_h=0.55, texts=("context",), moves=False)   half size: only
            the named rows show their BLUE text (the others are bars, thin), about 8.6 x 3.9
    Parts: heads who pills blue green moves_left moves_right (moves hidden unless shown).
        .row(name) -> VGroup(pill, blue cell, green cell)   .cell(name, "blue"|"green")
        .light(name, color=TURN) -> anim (pill border + name; unlights the previous)  .unlight()
        .fill(name, text, append=False) -> (mob, anims): a text row's GREEN cell writes `text`
            (replacing what it holds: old out, then new in); a row without text gains a GREEN bar
            segment instead. Raises if a text does not fit.
        .prefill(upto) -> self: "as of act k" without animating (latest text / one bar per fill)
        .fill_recap() -> self: the recap's shortened texts (BOUNDARY_RECAP), every row
        .slide_phrase(name, phrase, into_text) -> anims for one play (run_time ~1.6): S11's "what
            to remember" moves out of the BLUE cell into the GREEN one, which then reads `into_text`
        .stamp_human(name) -> (stamp, anims): the GREEN text moves left, a small YELLOW "a human
            decides" stamp fits at the cell's right end (play anims, then FadeIn the stamp)
        .dim_side("blue", k=0.35) -> anims (S16: the BLUE column dims; its header stays)"""

    def __init__(self, width: float = 12.6, row_h: float = 0.84, size: float = CAPTION,
                 head_size: float = 24, pill_w: float = 2.7, gap: float = 0.14, texts="all",
                 moves: bool = True, show=None, **kw):
        super().__init__(**kw)
        shown = self._show_set(show, ("heads", "who", "pills", "blue", "green", "moves_left", "moves_right"))
        if not moves:
            shown -= {"moves_left", "moves_right"}
        self.size, self.row_h = size, row_h
        cell_w = (width - pill_w - 2 * gap) / 2
        self.cell_w = cell_w
        x_blue = -(pill_w / 2 + gap + cell_w / 2)
        x_green = -x_blue
        self.x_blue, self.x_green = x_blue, x_green
        head_h = 0.62
        # header
        for hs in (head_size, 22, 20):              # the header steps down to 20 pt in a narrow table
            hb = sans("the model proposes", hs, CLOUD, weight="BOLD")
            hg = sans("the harness decides", hs, HARNESS, weight="BOLD")
            if max(hb.width, hg.width) <= cell_w:
                break
        else:
            raise ValueError(f"ActionBoundary: the column headers need a wider table (cell {cell_w:.2f} wide)")
        hb.move_to([x_blue, -head_h / 2, 0])
        hg.move_to([x_green, -head_h / 2, 0])
        self.part("heads", VGroup(hb, hg), "heads" in shown)
        self.head_blue, self.head_green = hb, hg
        who_t = label("who decides?", size, LOOKUP)
        arr = DoubleArrow([-pill_w / 2 - gap + 0.05, 0, 0], [pill_w / 2 + gap - 0.05, 0, 0], buff=0,
                          color=LOOKUP, stroke_width=3, tip_length=0.14, max_tip_length_to_length_ratio=0.2)
        arr.move_to([0, -head_h * 0.72, 0])
        who_t.next_to(arr, UP, buff=0.05)
        if who_t.width > pill_w + 2 * gap:
            who_t = label("who?", size, LOOKUP).next_to(arr, UP, buff=0.05)
        self.part("who", VGroup(arr, who_t), "who" in shown)
        # rows
        self.pills, self.blues, self.greens, self.green_texts, self.blue_texts = {}, {}, {}, {}, {}
        self.bar_segs = {n: [] for n in BOUNDARY_ROWS}
        pills, blues, greens = VGroup(), VGroup(), VGroup()
        y = -head_h - 0.08
        show_text = set(BOUNDARY_ROWS) if texts == "all" else set(texts or ())
        self.text_rows = show_text
        self.row_heights = {}
        for name in BOUNDARY_ROWS:
            bt = None
            if name in show_text:
                bt = fit_rows(BOUNDARY_BLUE[name], cell_w - 0.3, size, INK, buff=0.04, align=ORIGIN)
            rh = max(row_h, bt.height + 0.2) if bt is not None else row_h
            if name in show_text:              # room for the longest single GREEN text of this row
                greens_ = [t for _, n_, t in BOUNDARY_FILLS if n_ == name] + [BOUNDARY_RECAP[name]]
                need = max(fit_rows(t, cell_w - 0.3, size, INK, buff=0.04).height for t in greens_)
                rh = max(rh, need + 0.2)
            self.row_heights[name] = rh
            yc = y - rh / 2
            nm = label(BOUNDARY_NAMES[name], size, INK)
            pb = RoundedRectangle(width=pill_w, height=min(rh - 0.12, 0.5), corner_radius=0.2,
                                  stroke_color=S.GREY, stroke_width=2.5).set_fill(S.BG, 1).move_to([0, yc, 0])
            if nm.width > pill_w - 0.2:
                raise ValueError(f"ActionBoundary: {BOUNDARY_NAMES[name]!r} needs pill_w >= {nm.width + 0.2:.2f}")
            nm.move_to(pb)
            pill = VGroup(pb, nm)
            pill.frame, pill.name_text = pb, nm
            bc = RoundedRectangle(width=cell_w, height=rh - 0.1, corner_radius=0.1, stroke_color=CLOUD,
                                  stroke_width=2.5).set_fill(CLOUD, 0.1).move_to([x_blue, yc, 0])
            gc = RoundedRectangle(width=cell_w, height=rh - 0.1, corner_radius=0.1, stroke_color=HARNESS,
                                  stroke_width=2.5).set_fill(HARNESS, 0.06).move_to([x_green, yc, 0])
            bcell = VGroup(bc)
            if bt is not None:
                bt.move_to(bc)
                bcell.add(bt)
                self.blue_texts[name] = bt
            bcell.frame = bc
            gcell = VGroup(gc)
            gcell.frame = gc
            self.pills[name], self.blues[name], self.greens[name] = pill, bcell, gcell
            self.green_texts[name] = None
            pills.add(pill)
            blues.add(bcell)
            greens.add(gcell)
            y -= rh
        self.part("pills", pills, "pills" in shown)
        self.part("blue", blues, "blue" in shown)
        self.part("green", greens, "green" in shown)
        # move arrows
        y_m = y - 0.5
        for side, (title, reasons), col, sgn in (("moves_left", MOVE_LEFT, CLOUD, -1),
                                                 ("moves_right", MOVE_RIGHT, HARNESS, 1)):
            x_c = sgn * (width / 4 + 0.05)
            a = Arrow([x_c - sgn * 1.4, y_m, 0], [x_c + sgn * 1.4, y_m, 0], buff=0, color=col,
                      stroke_width=5, tip_length=0.22, max_tip_length_to_length_ratio=0.2)
            t = sans(title, size, col, weight="BOLD").next_to(a, UP, buff=0.06)
            r = fit_rows(reasons, width / 2 - 0.3, size, INK, align=ORIGIN).next_to(a, DOWN, buff=0.08)
            g = VGroup(a, t, r)
            g.arrow, g.title, g.reasons = a, t, r
            self.part(side, g, side in shown)
        self.lit = None
        self.move_to(ORIGIN)

    def row(self, name: str) -> VGroup:
        return VGroup(self.pills[name], self.blues[name], self.greens[name])

    def cell(self, name: str, side: str = "green") -> VGroup:
        return (self.greens if side == "green" else self.blues)[name]

    def light(self, name: str, color: str = TURN):
        anims = []
        if self.lit and self.lit != name:
            p = self.pills[self.lit]
            anims += [p.frame.animate.set_stroke(S.GREY, 2.5), p.name_text.animate.set_color(INK)]
        p = self.pills[name]
        anims += [p.frame.animate.set_stroke(color, 4), p.name_text.animate.set_color(color)]
        self.lit = name
        return AnimationGroup(*anims, group=self)

    def unlight(self):
        if not self.lit:
            return AnimationGroup(group=self)
        p = self.pills[self.lit]
        self.lit = None
        return AnimationGroup(p.frame.animate.set_stroke(S.GREY, 2.5), p.name_text.animate.set_color(INK), group=self)

    def _green_text(self, name: str, text: str):
        gc = self.greens[name].frame
        t = fit_rows(text, self.cell_w - 0.3, self.size, INK, buff=0.04, align=ORIGIN)
        if t.height > gc.height - 0.06:
            raise ValueError(f"ActionBoundary.fill({name!r}): {text!r} needs a row {t.height + 0.16:.2f} "
                             "high: a larger row_h, texts=(…, name) for that row, or replace=True")
        return t.move_to(gc)

    def fill(self, name: str, text: str | None = None, append: bool = False, run_time: float = 0.6):
        """(mob, anims). A row that shows text (texts=): its GREEN cell writes `text`, replacing what
        it held (old out, then new in; append=True: after it, with " · "; raises if it doesn't fit).
        A row without text: its GREEN cell gains one bar segment instead (text is ignored)."""
        cell = self.greens[name]
        if name not in self.text_rows:
            seg = self._bar_seg(name)
            _stage_hidden(cell, seg)
            return seg, [_Reveal(seg, attr="_swop", shift=RIGHT * 0.1, run_time=run_time)]
        old = self.green_texts[name]
        full = f"{old.src_text} · {text}" if (old is not None and append) else text
        new = self._green_text(name, full)
        new.src_text = full
        self.green_texts[name] = new
        if old is None:
            _stage_hidden(cell, new)
            return new, [_Reveal(new, attr="_swop", shift=RIGHT * 0.1, run_time=run_time)]
        return new, [AnimationGroup(*_swap_text(cell, old, new), run_time=run_time)]

    def _bar_seg(self, name: str):
        gc = self.greens[name].frame
        k = len(self.bar_segs[name])
        m = max(1, sum(1 for _, n_, _t in BOUNDARY_FILLS if n_ == name))
        w = (gc.width - 0.2) / m
        seg = Rectangle(width=w - 0.06, height=min(0.24, gc.height - 0.16), stroke_width=0).set_fill(HARNESS, 0.85)
        seg.move_to(gc.get_left() + RIGHT * (0.1 + w * k + w / 2))
        self.bar_segs[name].append(seg)
        return seg

    def prefill(self, upto: int):
        """No animation: the table "as of act k". A row that shows text holds the latest
        BOUNDARY_FILLS text of acts <= upto; a row without text, one bar segment per fill. Returns
        self."""
        for act, name, text in BOUNDARY_FILLS:
            if act > upto:
                continue
            cell = self.greens[name]
            if name not in self.text_rows:
                cell.add(self._bar_seg(name))
                continue
            old = self.green_texts[name]
            new = self._green_text(name, text)
            new.src_text = text
            if old is not None:
                cell.remove(old)
            cell.add(new)
            self.green_texts[name] = new
        return self

    def fill_recap(self):
        """Write (no animation) the recap's shortened GREEN texts (BOUNDARY_RECAP). Returns self."""
        for name, text in BOUNDARY_RECAP.items():
            old = self.green_texts[name]
            new = self._green_text(name, text)
            new.src_text = text
            if old is not None:
                self.greens[name].remove(old)
            self.greens[name].add(new)
            self.green_texts[name] = new
        return self

    def slide_phrase(self, name: str, phrase: str, into_text: str) -> list:
        """Animations for ONE play (S11; play them with run_time=1.6 or so): `phrase` (a row of the
        BLUE cell's text, e.g. "what to remember") lifts out of the BLUE cell, crosses above the
        pill into the GREEN cell and fades there; the BLUE cell then shows the rest of its text and
        the GREEN cell reads `into_text`. Every text leaves before another arrives in its place."""
        from manim import Wait
        bt = self.blue_texts.get(name)
        if bt is None:
            raise ValueError(f"slide_phrase: row {name!r} shows no BLUE text (texts=)")
        full = BOUNDARY_BLUE[name]
        if phrase not in full:
            raise ValueError(f"{phrase!r} not in {full!r}")
        rest = full.replace(f" · {phrase}", "").replace(f"{phrase} · ", "")
        bc, gc = self.blues[name].frame, self.greens[name].frame
        new_blue = fit_rows(rest, self.cell_w - 0.3, self.size, INK, buff=0.04, align=ORIGIN).move_to(bc)
        mover = label(phrase, self.size, CLOUD)
        rows = getattr(bt, "row_texts", [])
        hit = [k for k, r in enumerate(rows) if r.rstrip(" ·") == phrase]
        mover.move_to(bt[hit[0]] if hit else bt)
        y_top = self.pills[name].frame.get_top()[1] + 0.08 + mover.height / 2
        p1 = np.array([mover.get_center()[0], y_top, 0])
        p2 = np.array([gc.get_center()[0], y_top, 0])
        p3 = gc.get_center()
        old_green = self.green_texts[name]
        new_green = self._green_text(name, into_text)
        new_green.src_text = into_text
        self.green_texts[name] = new_green
        self.blue_texts[name] = new_blue
        _stage_swap(self.blues[name], bt, new_blue)
        anims = [_SwapOut(bt, self.blues[name], rate_func=squish_rate_func(smooth, 0.0, 0.2)),
                 _SwapIn(new_blue, rate_func=squish_rate_func(smooth, 0.55, 0.75)),
                 Succession(FadeIn(mover, run_time=0.05), Wait(run_time=0.15),
                            mover.animate(run_time=0.12).move_to(p1),
                            mover.animate(run_time=0.16).move_to(p2).set_color(HARNESS),
                            mover.animate(run_time=0.1).move_to(p3),
                            FadeOut(mover, run_time=0.12), Wait(run_time=0.3))]
        g = self.greens[name]
        if old_green is None:
            _stage_hidden(g, new_green)
            anims.append(_Reveal(new_green, attr="_swop", rate_func=squish_rate_func(smooth, 0.75, 1.0)))
        else:
            _stage_swap(g, old_green, new_green)
            anims += [_SwapOut(old_green, g, rate_func=squish_rate_func(smooth, 0.0, 0.2)),
                      _SwapIn(new_green, rate_func=squish_rate_func(smooth, 0.75, 1.0))]
        return anims

    def stamp_human(self, name: str) -> tuple:
        """(stamp, anims): a small YELLOW stamp "a human / decides" at the right end of that GREEN
        cell; the cell's text moves left (re-laid narrower, old out, then new in) so the stamp
        covers nothing. Play the anims, then FadeIn the stamp (it is yours: not a member)."""
        gc = self.greens[name].frame
        st = human_stamp(two_rows=True)
        if st.height > gc.height - 0.04:
            raise ValueError(f"stamp_human({name!r}): the row is too low for the stamp")
        st.move_to([gc.get_right()[0] - 0.1 - st.width / 2, gc.get_center()[1], 0])
        anims = []
        old = self.green_texts[name]
        if old is not None:
            w = gc.width - st.width - 0.45
            new = fit_rows(old.src_text, w, self.size, INK, buff=0.04, align=ORIGIN)
            if new.height > gc.height - 0.06:
                raise ValueError(f"stamp_human({name!r}): its text does not fit beside the stamp")
            new.move_to([gc.get_left()[0] + 0.15 + w / 2, gc.get_center()[1], 0])
            new.src_text = old.src_text
            self.green_texts[name] = new
            anims.append(AnimationGroup(*_swap_text(self.greens[name], old, new)))
        return st, anims

    def dim_side(self, side: str = "blue", k: float = 0.35) -> list:
        cells = self.blues if side == "blue" else self.greens
        return [c.animate.set_opacity(k) for c in cells.values()]


class BoundaryMini(VGroup):
    """V1's mini-map (S06-S13): a glyph-only copy of the action boundary, MINI_W x MINI_H (3.2 x
    1.9), placed at `center` (MINI_CENTER bottom right; MINI_ABOVE_STRIP above a 3-row strip). Five
    GREY pills down the middle, BLUE cells left, GREEN cells right. No text: a caption (<= 40
    characters) goes left of it (.caption()).
        BoundaryMini(upto=2)          the GREEN cells already hold one bar segment per fill of
                                      acts <= upto (BOUNDARY_FILLS); upto=0: empty
        .light(name) / .unlight() -> anim (the row's pill and cells outlined YELLOW)
        .add_bar(name) -> anim (that GREEN cell gains one bar segment)
        .caption(text, color=HARNESS) -> a caption left of the map, right-aligned to it, centred
            on the lit row's height (not added; >= 20 pt, <= 40 characters)
        .flash_green() -> anim (S15: the GREEN column flashes)
    Leaves before every ponder card; never shares a beat with a code panel or a tall terminal."""

    def __init__(self, center=MINI_CENTER, upto: int = 0, **kw):
        super().__init__(**kw)
        bg = RoundedRectangle(width=MINI_W, height=MINI_H, corner_radius=0.12, stroke_color=S.GREY_DARK,
                              stroke_width=2).set_fill(S.BG, 0.94)
        self.frame = bg
        self.add(bg)
        n = len(BOUNDARY_ROWS)
        pitch = (MINI_H - 0.3) / n
        cw, pw = 1.05, 0.62
        self.rows, self.cells, self.segs = {}, {}, {}
        self.max_segs = {r: max(1, sum(1 for _, nm, _ in BOUNDARY_FILLS if nm == r)) for r in BOUNDARY_ROWS}
        for i, name in enumerate(BOUNDARY_ROWS):
            y = MINI_H / 2 - 0.15 - pitch * (i + 0.5)
            pill = RoundedRectangle(width=pw, height=pitch * 0.62, corner_radius=pitch * 0.3,
                                    stroke_color=S.GREY, stroke_width=2).set_fill(S.GREY, 0.25).move_to([0, y, 0])
            b = Rectangle(width=cw, height=pitch * 0.66, stroke_color=CLOUD, stroke_width=2).set_fill(CLOUD, 0.35) \
                .move_to([-(pw / 2 + 0.08 + cw / 2), y, 0])
            g = Rectangle(width=cw, height=pitch * 0.66, stroke_color=HARNESS, stroke_width=2).set_fill(HARNESS, 0.05) \
                .move_to([pw / 2 + 0.08 + cw / 2, y, 0])
            self.rows[name] = VGroup(pill, b, g)
            self.cells[name] = g
            self.segs[name] = VGroup()
            self.add(pill, b, g, self.segs[name])
        self.lit = None
        self.move_to(center)
        for act, name, _ in BOUNDARY_FILLS:
            if act <= upto:
                self._seg(name, add=True)

    def _seg(self, name: str, add: bool = False):
        g = self.cells[name]
        k = len(self.segs[name])
        m = self.max_segs[name]
        w = (g.width - 0.08) / m
        seg = Rectangle(width=w - 0.04, height=g.height - 0.08, stroke_width=0).set_fill(HARNESS, 0.85)
        seg.move_to(g.get_left() + RIGHT * (0.04 + w * k + w / 2))
        if add:
            self.segs[name].add(seg)
        return seg

    def add_bar(self, name: str, run_time: float = 0.5):
        if len(self.segs[name]) >= self.max_segs[name]:
            raise ValueError(f"BoundaryMini: row {name!r} is full")
        seg = self._seg(name)
        self.segs[name].add(seg)
        return FadeIn(seg, shift=RIGHT * 0.1, run_time=run_time)

    def light(self, name: str, color: str = TURN):
        anims = []
        if self.lit and self.lit != name:
            anims.append(self.rows[self.lit][0].animate.set_stroke(S.GREY, 2).set_fill(S.GREY, 0.25))
        anims.append(self.rows[name][0].animate.set_stroke(color, 3.5).set_fill(color, 0.35))
        self.lit = name
        return AnimationGroup(*anims, group=self)

    def unlight(self):
        if not self.lit:
            return AnimationGroup(group=self)
        p = self.rows[self.lit][0]
        self.lit = None
        return p.animate.set_stroke(S.GREY, 2).set_fill(S.GREY, 0.25)

    def caption(self, text: str, color: str = HARNESS) -> Text:
        if len(text) > 40:
            raise ValueError(f"mini-map caption {text!r}: at most 40 characters")
        t = label(text, CAPTION, color)
        y = self.rows[self.lit][0].get_center()[1] if self.lit else self.get_center()[1]
        return t.move_to([self.frame.get_left()[0] - 0.2 - t.width / 2, y, 0])

    def flash_green(self, run_time: float = 0.8):
        return LaggedStart(*[Indicate(self.cells[n], color=HARNESS, scale_factor=1.08) for n in BOUNDARY_ROWS],
                           lag_ratio=0.1, run_time=run_time, group=self)


# ------------------------------------------------------------------ the lecture's small diagrams
SIX_STEPS = ("Think", "Reason", "Plan", "Execute", "Verify", "Response")


class SixSteps(VGroup):
    """Slide 21's turn split at the seam, one row: "Think → Reason → Plan | Execute → Verify →
    Response": the first three BLUE (the model), the last three GREEN (the harness), a PINK vertical
    seam between Plan and Execute. About 11.6 x 0.9 (size 20); built centred at ORIGIN.
    .chips[name] .seam .light(name, color=None) -> anim (fill that chip; None: its own colour)
    .unlight() -> anim   .seam_x()"""

    def __init__(self, size: float = CAPTION, **kw):
        super().__init__(**kw)
        self.chips = {}
        row = []
        for k, s in enumerate(SIX_STEPS):
            col = CLOUD if k < 3 else HARNESS
            c = chip(s, col, size=size, fill_opacity=0.08)
            self.chips[s] = c
            if k and k != 3:
                row.append(label("→", size, S.GREY))
            if k == 3:
                row.append(Rectangle(width=0.5, height=0.1, stroke_width=0).set_fill(opacity=0))
            row.append(c)
        r = VGroup(*row).arrange(RIGHT, buff=0.14)
        self.add(r)
        x = (self.chips["Plan"].get_right()[0] + self.chips["Execute"].get_left()[0]) / 2
        self.seam = DashedLine([x, r.get_top()[1] + 0.22, 0], [x, r.get_bottom()[1] - 0.22, 0],
                               color=LOOKUP, stroke_width=4, dash_length=0.08)
        self.add(self.seam)
        self.lit = None
        self.move_to(ORIGIN)

    def seam_x(self) -> float:
        return self.seam.get_center()[0]

    def light(self, name: str, color: str | None = None):
        c = self.chips[name]
        col = color or (CLOUD if SIX_STEPS.index(name) < 3 else HARNESS)
        anims = []
        if self.lit and self.lit != name:
            o = self.chips[self.lit]
            anims.append(o.box.animate.set_fill(opacity=0.08).set_stroke(width=2.5))
        anims.append(c.box.animate.set_fill(col, 0.4).set_stroke(col, 4))
        self.lit = name
        return AnimationGroup(*anims, group=self)

    def unlight(self):
        if not self.lit:
            return AnimationGroup(group=self)
        o = self.chips[self.lit]
        self.lit = None
        return o.box.animate.set_fill(opacity=0.08).set_stroke(width=2.5)


SPECTRUM_STOPS = ("rule-based", "structured output", "hybrid", "full agent autonomy")


class Spectrum(VGroup):
    """Slide 36's autonomy spectrum redrawn: a PINK double arrow with four stops (labels up to two
    rows, 20 pt) and room above each stop for a small picture (a mini Rail, an agent node).
    Default 12.2 x 1.4, centred at ORIGIN; the arrow at y=0, labels under it.
    .stop(i) -> the stop's dot   .above(i, h=1.0) -> the point h above stop i (put a picture there)
    .light(i, color=TURN) -> anim"""

    def __init__(self, width: float = 12.2, size: float = CAPTION, **kw):
        super().__init__(**kw)
        self.arrow = DoubleArrow([-width / 2, 0, 0], [width / 2, 0, 0], buff=0, color=LOOKUP, stroke_width=4,
                                 tip_length=0.2, max_tip_length_to_length_ratio=0.05)
        self.add(self.arrow)
        n = len(SPECTRUM_STOPS)
        self.dots, self.labels = [], []
        for i, s in enumerate(SPECTRUM_STOPS):
            x = -width / 2 + width * (i + 0.5) / n
            d = Dot([x, 0, 0], radius=0.09, color=LOOKUP)
            t = fit_rows(s, width / n - 0.3, size, INK, align=ORIGIN).next_to(d, DOWN, buff=0.18)
            self.dots.append(d)
            self.labels.append(t)
            self.add(d, t)
        self.move_to(ORIGIN)

    def stop(self, i: int):
        return self.dots[i]

    def above(self, i: int, h: float = 1.0):
        return self.dots[i].get_center() + UP * h

    def light(self, i: int, color: str = TURN):
        return AnimationGroup(self.dots[i].animate.set_color(color).scale(1.5),
                              self.labels[i].animate.set_color(color), group=self)


class AgentBlock(Piece):
    """Slide 7's agent redrawn small (S04's recap): a BLUE-outlined box "Agent" holding "LLM core"
    (BLUE), "Instructions" (GREY), a bar "Dynamic control", "Tools" (GREEN outline) and "Memory"
    (GREY dashed, dimmed); a pill "Task / goal" arrows in, a dashed pill "Task completion" arrows
    out. 12.0 x 2.9 with ends; ends=False: the box alone (6.0 x 2.9). Built centred at ORIGIN.
    Parts: task a_in box core instructions control tools memory a_out done.
        .block(name) -> that block (pulse it: Indicate)   .memory_tag(text="act 4") -> a GREY tag
        under the box, below the Memory block (not added)"""

    def __init__(self, ends: bool = True, size: float = CAPTION, show=None, **kw):
        super().__init__(**kw)
        shown = self._show_set(show, ("task", "a_in", "box", "core", "instructions", "control", "tools",
                                      "memory", "a_out", "done"))
        bw, bh, gap = 2.6, 0.62, 0.16
        W = 2 * bw + 3 * gap
        fr = box(W, 2.9, CLOUD, fill_opacity=0.04, stroke=3)
        hd = sans("Agent", size + 2, INK, weight="BOLD").move_to(fr.get_top() + DOWN * 0.26)
        self.part("box", VGroup(fr, hd), "box" in shown)
        y1, y2, y3 = 0.5, -0.25, -0.95
        xl, xr = -(bw + gap) / 2, (bw + gap) / 2
        specs = {"core": ("LLM core", xl, y1, bw, CLOUD, False, 0.2),
                 "instructions": ("Instructions", xr, y1, bw, S.GREY, False, 0.05),
                 "control": ("Dynamic control", 0, y2, W - 2 * gap, S.GREY, False, 0.05),
                 "tools": ("Tools", xl, y3, bw, HARNESS, False, 0.05),
                 "memory": ("Memory", xr, y3, bw, S.GREY, True, 0.0)}
        self.blocks = {}
        for name, (txt, x, y, w, col, dashed, fo) in specs.items():
            b = box(w, bh, col, fill_opacity=fo, dashed=dashed, stroke=2.5).move_to([x, y, 0])
            t = label(txt, size, INK if not dashed else S.GREY).move_to([x, y, 0])
            g = VGroup(b, t)
            if name == "memory":
                g.set_opacity(0.55)
            self.blocks[name] = g
            self.part(name, g, name in shown)
        if ends:
            task = _keep(chip("Task / goal", S.GREY, size=size)).next_to(fr, LEFT, buff=0.5)
            done = concept_box("Task completion", size).next_to(fr, RIGHT, buff=0.5)
            self.part("task", task, "task" in shown)
            self.part("a_in", _arrow(task.get_right(), fr.get_left()), "a_in" in shown)
            self.part("a_out", _arrow(fr.get_right(), done.get_left()), "a_out" in shown)
            self.part("done", done, "done" in shown)
        self.frame = fr
        self.move_to(ORIGIN)

    def block(self, name: str):
        return self.blocks[name]

    def memory_tag(self, text: str = "act 4") -> VGroup:
        """A GREY tag under the agent box, below the Memory block (not added)."""
        t = grey_tag(text)
        m = self.blocks["memory"]
        return t.next_to(self.frame, DOWN, buff=0.1).set_x(m.get_center()[0])


# ------------------------------------------------------------------ V2 · the loop, measured (S04)
# the small result cards of the recorded run (exact sub-strings of each Result line, c23)
RESULT_CHIPS = {"get_catalog": "products: 12 entries", "check_stock": "ok: yes",
                "price_order": "subtotal cents: 6400", "get_pairings": "bucheron: 3 entries",
                "preview_order": "status: unvalidated_proposal; order placed: no"}
for _d in C23:
    if _d["requested"] and RESULT_CHIPS.get(_d["requested"], "") not in (_d["result"] or ""):
        raise ValueError(f"RESULT_CHIPS[{_d['requested']!r}] is not in the recorded result line")


class LoopMeter(Piece):
    """V2 (S04): slide 10's loop driven by the staff's recorded Act 1 run (C23): the BLUE model at
    left (gpt-5.6-luna), its stack of message cards under it with a counter "messages: 1", a GOLD
    meter "input tokens: 1,942" above it with one GOLD tick per model call, and five
    GREEN-outlined tool paddles at right (TOOLS_ACT1). Built in place: x -6.3..5.9, y -3.3..2.7;
    the lane between them (x -3.7..3.0) stays empty for the cards.
    Parts: model meter ticks stack msgs paddles title
        .send(scene, k, run_time=0.8) -> card: call k+1's BLUE request card (C23[k]["requested"])
            leaves the model and stops before its paddle, which lights (k = 0..4)
        .complete(scene, k, card, run_time=1.6): the request goes into the paddle, the GREEN result
            card (RESULT_CHIPS) comes back, fades at the model; the stack gains 2 cards, the
            counter and the meter move to C23[k+1] (messages, input tokens), one more GOLD tick
        .round(scene, k, run_time=2.4) = send + complete
        .answer(scene, run_time=1.6) -> card: call 6: a BLUE answer card instead of a request, the
            paddles dim, the loop stops (meter 4,540, messages 11, six ticks)
        .paddle(name) -> the paddle (VGroup(frame, text))   .freeze() before the piece leaves
    Every number comes from C23 (TOKENS_IN, MSGS)."""

    def __init__(self, tools=TOOLS_ACT1, show=None, **kw):
        super().__init__(**kw)
        shown = self._show_set(show, ("model", "meter", "ticks", "stack", "msgs", "paddles", "title"))
        mb = model_box("model", w=2.4, h=1.1, sub=MODEL_ID)
        mb.move_to([-5.05, 0.35, 0])
        self.model = mb
        self.part("model", mb, "model" in shown)
        meter = gold_meter("input tokens", TOKENS_IN[0], cap=5000, w=3.0)
        meter.move_to([-6.3 + meter.width / 2, 2.25, 0])
        self.meter = meter
        self.part("meter", meter, "meter" in shown)
        self.tick_row = VGroup(cost_tick())
        self.tick_row.next_to(meter.frame, RIGHT, buff=0.3)
        self.part("ticks", self.tick_row, "ticks" in shown)
        self.stack_base = np.array([-5.05, -3.15, 0])
        self.stack = VGroup(msg_card(1.2, 0.13, CLOUD).move_to(self.stack_base))
        self.part("stack", self.stack, "stack" in shown)
        self.msgs = Counter("messages", MSGS[0], color=INK, size=CAPTION)
        self.msgs.move_to([-5.05, -0.65, 0])
        self.part("msgs", self.msgs, "msgs" in shown)
        pads = VGroup()
        self.paddles = {}
        for i, t in enumerate(tools):
            tx = mono(t, CAPTION, INK)
            fr = box(2.7, 0.62, HARNESS, fill=S.BG, fill_opacity=1.0, stroke=3)
            fr.move_to([4.55, 2.0 - i * 1.0, 0])
            tx.move_to(fr)
            p = VGroup(fr, tx)
            p.frame, p.text = fr, tx
            self.paddles[t] = p
            pads.add(p)
        self.part("paddles", pads, "paddles" in shown)
        ttl = label("tools · run by the harness", CAPTION, HARNESS).next_to(pads, DOWN, buff=0.25)
        self.part("title", ttl, "title" in shown)
        self.k_done = 0

    def paddle(self, name: str):
        return self.paddles[name]

    def _stack_cards(self, n_new: int, color: str):
        cards = []
        for j in range(n_new):
            c = msg_card(1.2, 0.13, color)
            c.move_to(self.stack_base + UP * 0.17 * (len(self.stack) + j))
            cards.append(c)
        return cards

    def send(self, scene, k: int, run_time: float = 0.8):
        name = C23[k]["requested"]
        p = self.paddles[name]
        card = json_card([name], CLOUD)
        card.move_to(self.model.get_right() + RIGHT * (0.2 + card.width / 2))
        target = p.frame.get_left() + LEFT * (0.25 + card.width / 2)
        scene.play(FadeIn(card, shift=RIGHT * 0.2), run_time=run_time * 0.3)
        scene.play(card.animate.move_to(target), p.frame.animate.set_stroke(TURN, 4),
                   p.text.animate.set_color(TURN), run_time=run_time * 0.7)
        return card

    def complete(self, scene, k: int, card, run_time: float = 1.6):
        name = C23[k]["requested"]
        p = self.paddles[name]
        res = json_card(RESULT_CHIPS[name].split("; "), HARNESS)
        res.move_to(p.frame.get_left() + LEFT * (0.25 + res.width / 2))
        scene.play(FadeOut(card, shift=RIGHT * 0.3), run_time=run_time * 0.15)      # the request goes in,
        scene.play(FadeIn(res, shift=LEFT * 0.2), run_time=run_time * 0.15)        # then the result comes out
        dest = self.model.get_right() + RIGHT * (0.2 + res.width / 2)
        scene.play(res.animate.move_to(dest), p.frame.animate.set_stroke(HARNESS, 3),
                   p.text.animate.set_color(INK), run_time=run_time * 0.35)
        new_cards = self._stack_cards(2, HARNESS)
        tick = cost_tick().next_to(self.tick_row[-1], RIGHT, buff=0.12)
        scene.play(FadeOut(res, scale=0.6), *[FadeIn(c, shift=DOWN * 0.1) for c in new_cards],
                   self.msgs.count_to(MSGS[k + 1], run_time * 0.35), self.meter.set_to(TOKENS_IN[k + 1], run_time * 0.35),
                   FadeIn(tick, scale=0.5), run_time=run_time * 0.35)
        for c in new_cards:
            scene.remove(c)
            self.stack.add(c)
        scene.remove(tick)
        self.tick_row.add(tick)
        self.k_done = k + 1

    def round(self, scene, k: int, run_time: float = 2.4):
        card = self.send(scene, k, run_time * 0.33)
        self.complete(scene, k, card, run_time * 0.67)

    def answer(self, scene, run_time: float = 1.6):
        """Call 6 (C23[5]): the answer, no tool request; the loop stops. Returns the answer card
        (a member of the piece)."""
        last = C23[-1]
        card = json_card(["answer · no tool request"], CLOUD)
        card.move_to(self.model.get_right() + RIGHT * (0.2 + card.width / 2))
        tick = cost_tick().next_to(self.tick_row[-1], RIGHT, buff=0.12)
        scene.play(FadeIn(card, shift=RIGHT * 0.2), FadeIn(tick, scale=0.5),
                   self.meter.set_to(last["tokens_in"], run_time * 0.5),
                   self.msgs.count_to(last["msgs"], run_time * 0.5), run_time=run_time * 0.5)
        scene.play(card.animate.shift(RIGHT * 1.6), *[p.animate.set_opacity(0.3) for p in self.paddles.values()],
                   run_time=run_time * 0.5)
        scene.remove(tick, card)
        self.tick_row.add(tick)
        self.add(card)
        self.answer_card = card
        return card

    def freeze(self):
        self.meter.freeze()
        self.msgs.freeze()
        return self


# ------------------------------------------------------------------ V3 · rings and a turnstile (S05)
RINGS = ("inner", "trace", "budget", "context", "cartcheck")
RING_LABELS = {"full": {"inner": "admission · tool audit · shop rules", "trace": "`Trace()`",
                        "budget": "`Budget(8, 20, 120 s)`", "context": '`Context("basic")`',
                        "cartcheck": "`CartCheck()`"},
               "medium": {"inner": "", "trace": "`Trace()`", "budget": "`Budget(…)`",
                          "context": "`Context(…)`", "cartcheck": "`CartCheck()`"},
               "compact": {k: "" for k in RINGS}}
_RING_GEOM = {"full": (3.8, 0.9, 0.5, 0.46), "medium": (2.1, 0.62, 0.36, 0.33), "compact": (1.4, 0.5, 0.2, 0.17)}
FENCE_TEXT = "SDK fallback · 40 iterations · no call limits · no overall time budget"


class HarnessRings(Piece):
    """V3 (S05): the BLUE agent core `build_agent` inside a fixed GREEN inner ring (padlocked:
    "admission · tool audit · shop rules"), then four translucent GREEN rings, inside out:
    `Trace()`, `Budget(8, 20, 120 s)`, `Context("basic")`, `CartCheck()`; each ring's label sits in
    the band its ring adds at the top. Concentric rounded rectangles, built centred at ORIGIN:
        HarnessRings()                    "full": 8.8 x 5.5, labels as above (constructor names)
        HarnessRings(mode="medium")       5.7 x 3.9, short labels (`Budget(…)`), inner: padlock only
                                          (two side by side for the ponder: harness and lite)
        HarnessRings(mode="compact")      3.4 x 2.2, no labels (core "agent"): the rings shrunk left
        HarnessRings(without=("trace",))  that ring is left out (its band stays empty): `lite`
        HarnessRings(show=("core", "inner"))   the other rings hidden: slide them on with .put()
    Parts: core, inner, trace, budget, context, cartcheck (each ring: VGroup(frame, label[, lock])).
        .ring(name)  .lift(name, d=0.5) -> anims (ring and label rise and fade; still a member)
        .put(name, d=0.5) -> anims (back down into place, fading in)  .glow(name) / .unglow(name)
        -> anim (its border bright and thick)  .label_of(name) -> the label (TransformFromCopy a
        code line into it)  .mark(name, text="?") -> a YELLOW mark on that ring's band (not added)
        .fence(text=FENCE_TEXT) -> GREY dashed outer fence + its label under it (not added)
        .gate_point() -> the core's right edge (put the Turnstile there)"""

    def __init__(self, mode: str = "full", without=(), show=None, size: float = CAPTION, **kw):
        super().__init__(**kw)
        if mode not in _RING_GEOM:
            raise ValueError(f"mode: one of {tuple(_RING_GEOM)}")
        shown = self._show_set(show, ("core",) + RINGS) - set(without)
        self.mode = mode
        cw, ch, px, py = _RING_GEOM[mode]
        self.px, self.py = px, py
        labels = RING_LABELS[mode]
        self.frames, self.labels = {}, {}
        for k in range(len(RINGS), 0, -1):                   # outer first: inner rings draw on top
            name = RINGS[k - 1]
            w, h = cw + 2 * k * px, ch + 2 * k * py
            inner = name == "inner"
            fr = RoundedRectangle(width=w, height=h, corner_radius=min(0.45, h / 2.6),
                                  stroke_color=HARNESS, stroke_width=4.5 if inner else 3)
            fr.set_fill(HARNESS, 0.12 if inner else 0.05)
            yb = ch / 2 + (k - 0.5) * py                     # the band this ring adds, centre y
            g = VGroup(fr)
            lab = None
            txt = labels[name]
            if txt:
                lab = _rich(txt, size, INK)
                lab.move_to([0, yb, 0])
            if inner:
                lk = padlock(min(0.3, py * 0.8), HARNESS)
                if lab is not None:
                    lk.next_to(lab, LEFT, buff=0.14)
                    VGroup(lk, lab).move_to([0, yb, 0])
                else:
                    lk.move_to([0, yb, 0])
                g.add(lk)
                g.lock = lk
            if lab is not None:
                if VGroup(*g[1:], lab).width > w - 0.2:
                    raise ValueError(f"HarnessRings({mode!r}): the {name} label is wider than its ring")
                g.add(lab)
            g.frame, g.label = fr, lab
            self.frames[name], self.labels[name] = fr, lab
            self.part(name, g, name in shown)
        core = box(cw, ch, CLOUD, fill=S.BG, fill_opacity=1.0, stroke=3)
        core_t = mono("build_agent", size, INK) if mode != "compact" else label("agent", size, INK)
        core_t.move_to(core)
        self.part("core", VGroup(core, core_t), "core" in shown)
        self.core = core
        self.move_to(ORIGIN)

    def ring(self, name: str):
        return self.parts[name]

    def label_of(self, name: str):
        return self.labels[name]

    def lift(self, name: str, d: float = 0.5) -> list:
        m = self.parts[name]
        _save_op(m)
        self._flag(m, True)
        return [m.animate.shift(UP * d).set_opacity(0)]

    def put(self, name: str, d: float = 0.5) -> list:
        m = self.parts[name]
        if not getattr(m, "hidden", False):
            return []
        m.shift(self.core.get_center() - self.frames[name].get_center())    # home (invisible)
        self._flag(m, False)
        return [_Reveal(m, shift=DOWN * d)]

    def glow(self, name: str, color: str = HARNESS):
        return self.frames[name].animate.set_stroke(color, 7)

    def unglow(self, name: str):
        return self.frames[name].animate.set_stroke(HARNESS, 4.5 if name == "inner" else 3)

    def mark(self, name: str, text: str = "?", color: str = TURN) -> Text:
        fr = self.frames[name]
        k = RINGS.index(name) + 1
        y = self.core.get_top()[1] + (k - 0.5) * self.py
        t = sans(text, 24, color, weight="BOLD")
        return t.move_to([fr.get_right()[0] - self.px / 2 - 0.12, y, 0])

    def fence(self, text: str = FENCE_TEXT, color: str = S.GREY) -> VGroup:
        outer = self.frames["cartcheck"]
        fr = box(outer.width + 0.6, outer.height + 0.5, color, dashed=True, stroke=3, radius=0.5)
        fr.move_to(outer)
        lab = fit_rows(text, max(fr.width, 6.0), CAPTION, S.GREY, align=ORIGIN).next_to(fr, DOWN, buff=0.12)
        g = VGroup(fr, lab)
        g.frame, g.label = fr, lab
        return g

    def gate_point(self):
        return self.core.get_right()


class Turnstile(Piece):
    """V3's Budget as a turnstile (S05): a post, a hub with three arms, a counter "k/8" above and,
    once locked, the RED message under it. About 1.6 x 2.2 (the lock message under it is 5.8
    wide: leave room). Built centred at ORIGIN. Tokens run left to right through it at hub height.
        .token(color=CLOUD, text="call") -> a token left of the gate (not added; GREEN "tool")
        .admit(token, run_time=0.8) -> anim: the token passes, the arms turn 1/3, the counter ticks
        .lock(text="Maximum of 8 model calls reached.") -> anims: arms, hub and post RED, a padlock
            on the hub, the message (RED mono) under the base
        .bounce(token, run_time=0.8) -> anim: the token runs at the arms and back (the lock sticks)
        .count, .cap"""

    def __init__(self, cap: int = 8, color: str = HARNESS, size: float = 24, **kw):
        super().__init__(**kw)
        self.cap, self.count, self.size, self.hi_color = cap, 0, size, color
        post = RoundedRectangle(width=0.22, height=1.5, corner_radius=0.08, stroke_color=color,
                                stroke_width=3).set_fill(color, 0.25).move_to([0, -0.35, 0])
        base = Line([-0.8, -1.1, 0], [0.8, -1.1, 0], color=color, stroke_width=4)
        self.hub_pt = np.array([0, 0.15, 0])
        hub = Circle(radius=0.13, stroke_color=color, stroke_width=3).set_fill(S.BG, 1).move_to(self.hub_pt)
        arms = VGroup(*[Line(self.hub_pt, self.hub_pt + 0.75 * np.array([np.cos(a), np.sin(a), 0]),
                             color=color, stroke_width=7) for a in (PI / 2 + 0.0, PI / 2 + TAU / 3, PI / 2 + 2 * TAU / 3)])
        self.post, self.base, self.hub, self.arms = post, base, hub, arms
        self.part("body", VGroup(post, base, arms, hub))
        self.counter = mono(f"0/{cap}", size, color).move_to([0, 1.25, 0])
        self.part("counter", self.counter)
        self.msg = None
        self.locked = False
        self.move_to(ORIGIN)

    def token(self, color: str = CLOUD, text: str = "call") -> VGroup:
        t = chip(text, color, size=CAPTION, pad_x=0.14, pad_y=0.06)
        return _keep(t).move_to(self.hub.get_center() + LEFT * (1.1 + t.width / 2))

    def _counter_anims(self, k: int) -> list:
        new = mono(f"{k}/{self.cap}", self.size, ERR if self.locked else self.hi_color).move_to(self.counter)
        old, self.counter = self.counter, new
        self.parts["counter"] = new
        return _swap_text(self, old, new)

    def admit(self, token, run_time: float = 0.8):
        if self.locked:
            raise ValueError("Turnstile.admit: it is locked (use bounce)")
        self.count += 1
        dest = self.hub.get_center() + RIGHT * (1.1 + token.width / 2)
        return AnimationGroup(token.animate.move_to(dest),
                              Rotate(self.arms, angle=-TAU / 3, about_point=self.hub.get_center()),
                              *self._counter_anims(self.count), run_time=run_time)

    def lock(self, text: str | None = "Maximum of 8 model calls reached.") -> list:
        self.locked = True
        lk = padlock(0.32, ERR).move_to(self.hub)
        anims = [self.arms.animate.set_color(ERR), self.post.animate.set_stroke(ERR).set_fill(ERR, 0.25),
                 self.base.animate.set_color(ERR), self.hub.animate.set_stroke(ERR), FadeIn(lk, scale=0.6)]
        self.add(lk)
        self.lock_glyph = lk
        if text:
            m = mono(text, CAPTION, ERR).next_to(self.base, DOWN, buff=0.18)
            self.msg = m
            self.add(m)
            anims.append(FadeIn(m, shift=UP * 0.1))
        anims.append(self.counter.animate.set_color(ERR))
        return anims

    def bounce(self, token, run_time: float = 0.8):
        hit = self.hub.get_center() + LEFT * (0.85 + token.width / 2)
        back = token.get_center().copy()
        return Succession(token.animate(run_time=run_time * 0.45, rate_func=rush_into).move_to(hit),
                          token.animate(run_time=run_time * 0.55).move_to(back))


# ------------------------------------------------------------------ V4 · the stack, sieves and lanes (S06-S07)
STACK_BLOCKS = (("system prompt", "`prompts/shop_assistant.md` + policies"),
                ("user message", "the confirmed request (JSON)"),
                ("structured output", "`AgentReply`"),
                ("tool definitions", "5 tools"),
                ("retrieved data", "the context packet"),
                ("memory", "saved preferences"))


class ContextStack(Piece):
    """V4, S06: slide 16's stack rebuilt from Act 1's real blocks. A GREY "user prompt" chip arrows
    into a column of six GREEN-outlined blocks (STACK_BLOCKS: title row + detail row), which arrows
    into the BLUE "LLM" and then a BLUE "response". Blocks 5-6 ("retrieved data", "memory") start as
    GREY dashed empty slots (no detail) until .fill_slots().
        ContextStack()                       12.4 x 4.9 with the ends, built centred at ORIGIN
        ContextStack(compact=True, title="basic · act 1")   titles only, no ends: 3.2 x 3.8 (two
                                             side by side: "basic · act 1" and "enriched")
    Parts: prompt a_in blocks llm a_mid response a_out title (compact: blocks title).
        .block(i) -> block i (0-5): VGroup(frame, title[, detail])  .light(i, color=TURN) -> anim
        .fill_slots() -> anims: the two slots fill GREEN (dashed -> solid; full: their details)
        .slots() -> VGroup of the two slot blocks (fold them into one "context packet" card)"""

    def __init__(self, compact: bool = False, title: str | None = None, size: float = CAPTION,
                 show=None, **kw):
        super().__init__(**kw)
        shown = self._show_set(show, ("prompt", "a_in", "blocks", "llm", "a_mid", "response", "a_out", "title"))
        self.compact = compact
        bw, bh, gap = (3.2, 0.5, 0.08) if compact else (6.0, 0.72, 0.1)
        blocks = VGroup()
        self.blocks_list, self.slot_frames = [], []
        n = len(STACK_BLOCKS)
        top = (n * bh + (n - 1) * gap) / 2
        for i, (ttl, det) in enumerate(STACK_BLOCKS):
            y = top - bh / 2 - i * (bh + gap)
            slot = i >= 4
            solid = box(bw, bh, HARNESS, fill_opacity=0.08, stroke=2.5).move_to([0, y, 0])
            dashed = box(bw, bh, S.GREY, dashed=True, stroke=2.5).move_to([0, y, 0])
            t = label(ttl, size, S.GREY if slot else INK)
            g = VGroup()
            if slot:
                solid.set_stroke(opacity=0).set_fill(opacity=0)
                g.add(solid, dashed)
            else:
                g.add(solid)
            d = None
            if not compact:
                d = _rich(det, size, INK)
                rows = VGroup(t, d).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
                rows.move_to(solid).align_to(solid, LEFT).shift(RIGHT * 0.22)
                if rows.width > bw - 0.3:
                    raise ValueError(f"ContextStack: block {ttl!r} is wider than {bw}")
                if slot:
                    d.set_opacity(0)
            else:
                t.move_to(solid)
            g.add(t)
            if d is not None:
                g.add(d)
            g.frame, g.title, g.detail, g.solid, g.dashed = solid, t, d, solid, (dashed if slot else None)
            blocks.add(g)
            self.blocks_list.append(g)
        self.part("blocks", blocks, "blocks" in shown)
        if title:
            tt = label(title, size, INK).next_to(blocks, UP, buff=0.18)
            self.part("title", tt, "title" in shown)
        if not compact:
            pr = _keep(chip("user prompt", S.GREY, size=size)).next_to(blocks, LEFT, buff=0.5)
            llm = model_box("LLM", w=1.0, h=0.8).next_to(blocks, RIGHT, buff=0.5)
            resp = _keep(chip("response", CLOUD, size=size)).next_to(llm, RIGHT, buff=0.45)
            self.part("prompt", pr, "prompt" in shown)
            self.part("a_in", _arrow(pr.get_right(), blocks.get_left()), "a_in" in shown)
            self.part("llm", llm, "llm" in shown)
            self.part("a_mid", _arrow(blocks.get_right(), llm.get_left()), "a_mid" in shown)
            self.part("response", resp, "response" in shown)
            self.part("a_out", _arrow(llm.get_right(), resp.get_left()), "a_out" in shown)
        self.move_to(ORIGIN)

    def block(self, i: int):
        return self.blocks_list[i]

    def light(self, i: int, color: str = TURN):
        return Indicate(self.blocks_list[i].frame, color=color, scale_factor=1.03)

    def fill_slots(self, run_time: float = 0.8) -> list:
        anims = []
        for b in self.blocks_list[4:]:
            anims += [b.dashed.animate.set_stroke(opacity=0),
                      b.solid.animate.set_stroke(HARNESS, 2.5, opacity=1).set_fill(HARNESS, 0.3),
                      b.title.animate.set_color(INK)]
            if b.detail is not None:
                anims.append(b.detail.animate.set_opacity(1))
        return anims

    def slots(self) -> VGroup:
        return VGroup(*self.blocks_list[4:])


SIEVE_Y = (2.05, 1.2, 0.35)       # the three sieves (stock, shipping, allergens), in place
_SIEVE_LANE_X = -2.8
_TRAY_Y = -0.85


class Sieves(Piece):
    """V4, S07: the twelve cheeses (CHEESES, the capture's product IDs) drop one by one down a
    lane through three GREEN sieves (SIEVES: "stock ≥ 100 g", "no raw milk → PA", "no nut
    allergens"). A chip that fails a sieve turns RED, moves right into the excluded list (top right,
    in capture order) and gets its RED reason exactly as in container/27 (EXCLUDED); the seven
    survivors (SURVIVORS) turn GREEN and land in the tray along the bottom. Built in place above a
    3-row strip: x -6.4..6.3, y -1.3..2.8 (the lecture tag's corner stays free).
    Parts: sieves (lines + labels) list_head tray (the tray's outline) — chips are added as they drop.
        .drop(scene, pid, run_time=1.0) plays one chip   .drop_all(scene, each=0.8) all twelve
        .chip(pid) -> the chip (after its drop)   .reason(pid) -> its RED reason text
        .rejects (list of pids, in order)  .tray_chips (dict pid -> chip)
    Paths never cross text: the lane is empty, rejects slide right through an empty gap, and the
    tray fills from its ends inward."""

    def __init__(self, size: float = CAPTION, **kw):
        super().__init__(**kw)
        self.size = size
        sv = VGroup()
        self.sieve_lines = []
        for (txt, _), y in zip(SIEVES, SIEVE_Y):
            ln = DashedLine([-6.4, y, 0], [-1.3, y, 0], color=HARNESS, stroke_width=5, dash_length=0.12,
                            dashed_ratio=0.7)
            t = label(txt, size, HARNESS).next_to(ln, UP, buff=0.06).align_to(ln, LEFT)
            sv.add(ln, t)
            self.sieve_lines.append(ln)
        self.part("sieves", sv)
        lh = mono("excluded_products", size, S.GREY).move_to([-0.9, 2.55, 0], aligned_edge=LEFT)
        self.part("list_head", lh, shown=False)
        tray = box(12.8, 0.62, HARNESS, dashed=True, stroke=2).move_to([0, _TRAY_Y, 0])
        self.part("tray", tray)
        self.rows_y = {}
        k_by_sieve: dict[int, int] = {}
        for pid, reason in EXCLUDED.items():
            si = [r for _, r in SIEVES].index(reason)
            k = k_by_sieve.get(si, 0)
            k_by_sieve[si] = k + 1
            n_here = sum(1 for r in EXCLUDED.values() if r == reason)
            off = 0.0 if n_here == 1 else (0.22 if k == 0 else -0.22)
            self.rows_y[pid] = SIEVE_Y[si] + off
        self.chips, self.reasons, self.rejects, self.tray_chips = {}, {}, [], {}
        self._tray_layout = self._plan_tray()

    def _plan_tray(self) -> dict:
        """Survivor -> x centre, filled ends-first so no chip slides past another."""
        widths = {p: cheese_chip(p).width for p in SURVIVORS}
        n = len(SURVIVORS)
        # slot order left -> right: fill order alternates far-left, far-right, …, by arrival
        order = []
        lo, hi = 0, n - 1
        for k in range(n):
            if k % 2 == 0:
                order.append(lo)
                lo += 1
            else:
                order.append(hi)
                hi -= 1
        slot_of = {p: order[k] for k, p in enumerate(SURVIVORS)}
        by_slot = sorted(SURVIVORS, key=lambda p: slot_of[p])
        gap = 0.16
        total = sum(widths[p] for p in by_slot) + gap * (n - 1)
        x = -total / 2
        xs = {}
        for p in by_slot:
            xs[p] = x + widths[p] / 2
            x += widths[p] + gap
        return xs

    def chip(self, pid: str):
        return self.chips[pid]

    def reason(self, pid: str):
        return self.reasons[pid]

    def drop(self, scene, pid: str, run_time: float = 1.0):
        c = cheese_chip(pid)
        c.move_to([_SIEVE_LANE_X, 2.55, 0])
        self.chips[pid] = c
        scene.play(FadeIn(c, shift=DOWN * 0.15), run_time=run_time * 0.2)
        if pid in EXCLUDED:
            reason = EXCLUDED[pid]
            si = [r for _, r in SIEVES].index(reason)
            rest = np.array([_SIEVE_LANE_X, SIEVE_Y[si] + c.height / 2 + 0.03, 0])
            scene.play(c.animate.move_to(rest), run_time=run_time * 0.3)
            r = mono(reason, self.size, ERR)
            y = self.rows_y[pid]
            dest = np.array([-0.9 + c.width / 2, y, 0])
            r.move_to([-0.9 + c.width + 0.15 + r.width / 2, y, 0])
            c.generate_target()
            c.target.move_to(dest)
            c.target[0].set_stroke(ERR)
            anims = [MoveToTarget(c)]
            if self.parts["list_head"].hidden:
                anims += self.parts_in("list_head")
            scene.play(*anims, run_time=run_time * 0.3)
            scene.play(FadeIn(r, shift=LEFT * 0.1), run_time=run_time * 0.2)
            self.reasons[pid] = r
            self.rejects.append(pid)
            scene.remove(c, r)
            self.add(c, r)
        else:
            low = np.array([_SIEVE_LANE_X, _TRAY_Y, 0])
            scene.play(c.animate.move_to(low), run_time=run_time * 0.45)
            c.generate_target()
            c.target.move_to([self._tray_layout[pid], _TRAY_Y, 0])
            c.target[0].set_stroke(HARNESS)
            scene.play(MoveToTarget(c), run_time=run_time * 0.35)
            self.tray_chips[pid] = c
            scene.remove(c)
            self.add(c)
        return c

    def drop_all(self, scene, each: float = 0.8):
        for pid in CHEESES:
            self.drop(scene, pid, each)


class Lanes(Piece):
    """V4, S07: slide 22's two lanes as a message stream: an upper "system lane" holding a GREY card
    "instructions · shop_assistant.md + policies", a lower "user lane" (empty slots), each titled
    above its left end, and the counter "Input: 1 conversation messages." (the capture's words;
    container/21 and 22 line 10) under the right end. Built centred at ORIGIN, 12.4 x 2.9; a card
    in a lane is at most 0.7 tall (one json_card row).
    Parts: system user counter
        .slot(lane, i, w) -> point: the centre of slot i (0-based) for a card w wide
        .enter(card, lane="user") -> anim: the card moves into the next free slot of that lane
            (add it to the piece yourself if the lanes will move)
        .turn_back(card) -> anim: the card (start it ABOVE the lanes) drops toward the system lane,
            bounces off its top edge and goes back, dimmed
        .count_to(n) -> anims: "Input: n conversation messages." (old out, then new in)"""

    def __init__(self, width: float = 12.4, lane_h: float = 0.85, size: float = CAPTION, **kw):
        super().__init__(**kw)
        self.width, self.lane_h, self.size = width, lane_h, size
        self.lanes = {}
        title_h = 0.32
        for k, (name, title, col) in enumerate((("system", "system lane · instructions", S.GREY),
                                                ("user", "user lane · data, not instructions", HARNESS))):
            y = -k * (lane_h + title_h + 0.08)
            fr = box(width, lane_h, col, fill_opacity=0.04, stroke=2.5).move_to([0, y, 0])
            t = label(title, size, col).next_to(fr, UP, buff=0.06).align_to(fr, LEFT).shift(RIGHT * 0.15)
            g = VGroup(fr, t)
            g.frame, g.title = fr, t
            self.lanes[name] = g
            self.part(name, g)
        self.filled = {"system": [], "user": []}
        inst = json_card(["instructions · shop_assistant.md + policies"], S.GREY)
        inst.move_to(self.slot("system", 0, inst.width))
        self.parts["system"].add(inst)
        self.filled["system"].append(inst)
        self.inst_card = inst
        self.counter = mono("Input: 1 conversation messages.", size, INK)
        self.counter.next_to(self.lanes["user"].frame, DOWN, buff=0.12).align_to(self.lanes["user"].frame, RIGHT)
        self.part("counter", self.counter)
        self.move_to(ORIGIN)

    def slot(self, lane: str, i: int, w: float | None = None):
        fr = self.lanes[lane].frame
        x0 = fr.get_left()[0] + 0.25
        if i > 0 and len(self.filled[lane]) >= i:
            x0 = self.filled[lane][i - 1].get_right()[0] + 0.2
        w = w or 1.0
        return np.array([x0 + w / 2, fr.get_center()[1], 0])

    def enter(self, card, lane: str = "user", run_time: float = 0.8):
        i = len(self.filled[lane])
        dest = self.slot(lane, i, card.width)
        fr = self.lanes[lane].frame
        if dest[0] + card.width / 2 > fr.get_right()[0] - 0.1:
            raise ValueError("Lanes.enter: the lane is full (make the cards narrower)")
        if card.height > fr.height - 0.1:
            raise ValueError("Lanes.enter: the card is taller than the lane")
        self.filled[lane].append(card)
        return card.animate(run_time=run_time).move_to(dest)

    def turn_back(self, card, run_time: float = 1.0):
        fr = self.lanes["system"].frame
        near = np.array([card.get_center()[0], fr.get_top()[1] + card.height / 2 + 0.08, 0])
        back = card.get_center().copy()
        return Succession(card.animate(run_time=run_time * 0.45, rate_func=rush_into).move_to(near),
                          card.animate(run_time=run_time * 0.55).move_to(back).set_opacity(0.4))

    def count_to(self, n: int) -> list:
        new = mono(f"Input: {n} conversation messages.", self.size, INK).move_to(self.counter, aligned_edge=RIGHT)
        old, self.counter = self.counter, new
        self.parts["counter"] = new
        return _swap_text(self, old, new)


class ShipToggle(Piece):
    """V4's coda (S06): the same cart on a GREEN validator while a destination switch flips PA <->
    NY; the stamp flips RED "PA: REJECTED" / GREEN "NY: PASS" (container/29 lines 5, 7). Built
    centred at ORIGIN, about 9.6 x 2.0. The tag "a fictional classroom rule · not a law" is yours.
    Parts: cart validator switch stamp
        .flip(run_time=0.8) -> anims (the switch moves, the stamp swaps: old out, then new in)
        .state ("PA" or "NY")"""

    CART = ("Comté 350 g", "Bûcheron 350 g", "Époisses 300 g")

    def __init__(self, size: float = CAPTION, **kw):
        super().__init__(**kw)
        cart = cart_token(list(self.CART), CLOUD)
        cart.move_to([-3.0, 0.35, 0])
        val = box(cart.width + 0.6, 0.36, HARNESS, fill_opacity=0.25, stroke=3)
        val.next_to(cart, DOWN, buff=0.1)
        vt = label("validator", size, HARNESS).next_to(val, DOWN, buff=0.08)
        self.part("cart", cart)
        self.part("validator", VGroup(val, vt))
        track = RoundedRectangle(width=1.6, height=0.5, corner_radius=0.25, stroke_color=S.GREY,
                                 stroke_width=2.5).set_fill(S.BG, 1).move_to([2.2, 0.35, 0])
        knob = Circle(radius=0.19, stroke_width=0).set_fill(TURN, 1).move_to(track.get_left() + RIGHT * 0.27)
        pa = mono("PA", size, INK).next_to(track, LEFT, buff=0.15)
        ny = mono("NY", size, S.GREY).next_to(track, RIGHT, buff=0.15)
        sw = VGroup(track, knob, pa, ny)
        self.knob, self.pa, self.ny, self.track = knob, pa, ny, track
        self.part("switch", sw)
        self.state = "PA"
        self.stamp_mob = self._stamp("PA")
        self.part("stamp", self.stamp_mob)
        self.move_to(ORIGIN)

    def _stamp(self, st: str):
        g = stamp("PA: REJECTED" if st == "PA" else "NY: PASS", ERR if st == "PA" else HARNESS, angle=0.0)
        return g.move_to(self.track.get_center() + DOWN * 0.95 if hasattr(self, "track") else ORIGIN)

    def flip(self, run_time: float = 0.8) -> list:
        to = "NY" if self.state == "PA" else "PA"
        end = self.track.get_right() + LEFT * 0.27 if to == "NY" else self.track.get_left() + RIGHT * 0.27
        new = self._stamp(to).move_to(self.stamp_mob)
        old, self.stamp_mob = self.stamp_mob, new
        self.parts["stamp"] = new
        self.state = to
        return [self.knob.animate.move_to(end),
                self.pa.animate.set_color(INK if to == "PA" else S.GREY),
                self.ny.animate.set_color(INK if to == "NY" else S.GREY),
                AnimationGroup(*_swap_text(self, old, new), run_time=run_time)]


# ------------------------------------------------------------------ V5 · rails, a ticket and one shelf (S08, S09, S13)
RAIL_STATIONS = ("confirm", "propose", "validate", "pairings", "review", "place")
RAIL_LABELS = {"confirm": "confirm request", "propose": "propose cart", "validate": "validate and price",
               "pairings": "select pairings", "review": "manager review\nif required",
               "place": "revalidate\nand place"}
RAIL_SHORT = {"confirm": "confirm", "propose": "propose", "validate": "validate", "pairings": "pairings",
              "review": "manager review", "place": "revalidate & place"}
# the six edges of acts/act3_workflow.py lines 27-32, in that order
RAIL_EDGES = (("confirm", "propose"), ("propose", "validate"), ("validate", "propose"),
              ("validate", "pairings"), ("pairings", "review"), ("review", "place"))


def buffer_stop(text: str, color: str = ERR, dashed: bool = False, size: float = CAPTION) -> VGroup:
    """A buffer stop at the end of a track (S08: RED "UNRESOLVED", GREY dashed "BLOCKED · live run
    only"): two short posts and a bar, its label under it. Built at ORIGIN. .bar .label"""
    bar = Line([-0.35, 0.18, 0], [0.35, 0.18, 0], color=color, stroke_width=6)
    posts = VGroup(Line([-0.3, 0.18, 0], [-0.3, -0.2, 0]), Line([0.3, 0.18, 0], [0.3, -0.2, 0])).set_stroke(color, 4)
    g = VGroup(bar, posts)
    if dashed:
        g = VGroup(DashedVMobject(bar, num_dashes=5).set_stroke(color, 6),
                   *[DashedVMobject(p, num_dashes=3).set_stroke(color, 4) for p in posts])
    t = label(text, size, color).next_to(g, DOWN, buff=0.1)
    out = VGroup(g, t)
    out.bar, out.label = g, t
    return _keep(out)


class Rail(Piece):
    """V5 (S08, S09, S10, S13): Act 3's workflow as a railway (the README's diagram, README.md
    lines 349-356). Python owns the edges (GREEN track); "propose cart" is the only BLUE station
    ("no tools · structured proposal" under it).
        Rail()                 U-shaped, built centred at ORIGIN, 12.6 x 3.9: top row confirm ->
                               propose -> validate (the revise loop arcs from validate back to
                               propose, with its counter "revisions ≤ 2" above), down the right
                               side, bottom row back: pairings -> review -> place
        Rail(mini=True, named="review")   glyph-only, 5.2 x 2.2; only the named station's label
                               (above or below it)
        Rail(layout="line", names=("validate", "review", "place"))   one straight row (S13's
                               short rails, 9.3 x 0.8; box_w 2.5; gaps 0.9: tokens with
                               cart_token(scale=0.8)), labels RAIL_SHORT
    Parts: stations (each VGroup(frame, label)) edges loop caption counter switch
        .station(name) .edge(i) (RAIL_EDGES order: light it with a code line)
        .spot(name) -> point in the gap AFTER that station (a token waits there; "before" a
            station: .spot of the previous one; .start() before the first)
        .move(token, name, run_time=0.8) -> anim: the token to .spot(name) along the track
        .revise(token, run_time=1.4) -> anim: from the gap before validate, up and back along the
            loop into "propose" (the token fades into it; bring the revised one out with FadeIn at
            .spot("propose"))
        .count(k) -> anims: the loop counter becomes "revisions k/2" (old out, then new in)
        .freeze(name, color=AMBER) -> anims: that station and the track into it turn amber (the SDK
            waits); .unfreeze(name) -> anims
        .block_loop(text="review only") -> RED bar across the loop, its label inside the arc (not
            added)
        .scripted_seat() -> anims: "propose cart" becomes BLUE dashed with a `scripted` tag
    Tokens on the rail are glyph-only cart_token() (0.8 x 0.5): put the items in a chip beside it."""

    def __init__(self, mini: bool = False, named: str | None = None, layout: str = "u",
                 names=None, box_w: float | None = None, size: float = CAPTION, show=None, **kw):
        super().__init__(**kw)
        shown = self._show_set(show, ("stations", "edges", "loop", "caption", "counter", "switch"))
        self.layout, self.mini = layout, mini
        names = tuple(names) if names else RAIL_STATIONS
        self.names = names
        if mini:
            bw, bh, dx, dy = 0.95, 0.42, 1.75, 1.1
        else:
            bw, bh, dx, dy = (box_w or 2.8), 0.8, (box_w or 2.8) + 1.5, 2.0
        self.bw, self.bh = bw, bh
        pos = {}
        if layout == "u":
            top_y, bot_y = dy / 2, -dy / 2
            for i, n in enumerate(("confirm", "propose", "validate")):
                pos[n] = np.array([(i - 1) * dx, top_y, 0])
            for i, n in enumerate(("pairings", "review", "place")):
                pos[n] = np.array([(1 - i) * dx, bot_y, 0])
        else:
            if not mini:
                bw = box_w or 2.5
                self.bw = bw
                dx = bw + 0.9
            for i, n in enumerate(names):
                pos[n] = np.array([(i - (len(names) - 1) / 2) * dx, 0, 0])
        self.pos, self.dx, self.dy = pos, dx, dy
        sts = VGroup()
        self.st = {}
        for n in names:
            col = CLOUD if n == "propose" else HARNESS
            fr = box(bw, bh, col, fill=S.BG, fill_opacity=1.0, stroke=3).move_to(pos[n])
            tint = RoundedRectangle(width=bw, height=bh, corner_radius=0.14, stroke_width=0).set_fill(
                col, 0.12).move_to(pos[n])
            g = VGroup(fr, tint)
            lab = None
            if not mini:
                txt = RAIL_LABELS[n] if layout == "u" else RAIL_SHORT[n]
                lab = VGroup(*[label(r, size, INK) for r in txt.split("\n")]).arrange(DOWN, buff=0.04)
                if lab.width > bw - 0.16:
                    raise ValueError(f"Rail: {txt!r} needs box_w >= {lab.width + 0.16:.2f}")
                lab.move_to(fr)
                g.add(lab)
            elif named == n:
                lab = label(RAIL_SHORT[n], size, INK)
                below = layout == "u" and n in ("pairings", "review", "place")
                lab.next_to(fr, DOWN if below else UP, buff=0.1)
                g.add(lab)
            g.frame, g.label, g.tint = fr, lab, tint
            self.st[n] = g
            sts.add(g)
        # edges
        eds = VGroup()
        self.edges = []
        for a, b in RAIL_EDGES:
            if a not in pos or b not in pos or (a, b) == ("validate", "propose"):
                self.edges.append(None)
                continue
            pa, pb = pos[a], pos[b]
            if abs(pa[1] - pb[1]) < 1e-6:
                sgn = 1 if pb[0] > pa[0] else -1
                s0, s1 = pa + RIGHT * sgn * bw / 2, pb - RIGHT * sgn * bw / 2
            else:
                s0, s1 = pa + DOWN * bh / 2, pb + UP * bh / 2
            e = Arrow(s0, s1, buff=0.04, color=HARNESS, stroke_width=4, tip_length=0.16,
                      max_tip_length_to_length_ratio=0.25)
            self.edges.append(e)
            eds.add(e)
        self.part("edges", eds, "edges" in shown)
        self.part("stations", sts, "stations" in shown)
        self.loop = None
        if layout == "u":
            a0 = pos["validate"] + np.array([-bw * 0.3, bh / 2, 0])
            a1 = pos["propose"] + np.array([bw * 0.3, bh / 2, 0])
            arc = ArcBetweenPoints(a0, a1, angle=PI * 0.55, color=HARNESS, stroke_width=4)
            tip = Arrow(arc.point_from_proportion(0.93), a1, buff=0, color=HARNESS, stroke_width=4,
                        tip_length=0.16, max_tip_length_to_length_ratio=0.9)
            self.loop = VGroup(arc, tip)
            self.loop.arc = arc
            self.edges[2] = self.loop
            self.part("loop", self.loop, "loop" in shown)
            if not mini:
                self.arc_top = arc.get_top()[1]
                cnt = label("revisions ≤ 2", size, HARNESS).move_to([arc.get_center()[0], self.arc_top + 0.42, 0])
                self.counter = cnt
                self.part("counter", cnt, "counter" in shown)
                cap = label("no tools · structured proposal", size, CLOUD)
                cap.next_to(self.st["propose"].frame, DOWN, buff=0.08)
                self.part("caption", cap, "caption" in shown)
                sw = diamond(None, HARNESS, w=0.3).move_to(pos["validate"] + DOWN * (bh / 2 + 0.2))
                self.switch = sw
                self.part("switch", sw, "switch" in shown)
        self.move_to(ORIGIN)

    def station(self, name: str):
        return self.st[name]

    def edge(self, i: int):
        return self.edges[i]

    def _order(self) -> tuple:
        return self.names if self.layout != "u" else RAIL_STATIONS

    def corridor_y(self) -> float:
        """The empty corridor tokens travel along when they must pass a station (U: between the
        rows, under the propose caption; line: under the row)."""
        if self.layout == "u":
            return (self.st["confirm"].frame.get_center()[1] + self.st["place"].frame.get_center()[1]) / 2 - 0.1
        return self.st[self.names[0]].frame.get_center()[1] - (self.bh / 2 + 0.38)

    def spot(self, name: str):
        """The gap after station `name` along the path (on the track; U: after validate it is the
        right side's gap, at corridor height)."""
        order = self._order()
        i = order.index(name)
        p = self.st[name].frame.get_center()
        if i + 1 < len(order):
            q = self.st[order[i + 1]].frame.get_center()
            if abs(p[1] - q[1]) < 1e-3:
                return (p + q) / 2
            return np.array([p[0], self.corridor_y(), 0])
        sgn = 1 if self.layout != "u" else -1
        return p + RIGHT * sgn * (self.bw / 2 + 0.42)

    def start(self):
        p = self.st[self._order()[0]].frame.get_center()
        return p + LEFT * (self.bw / 2 + 0.42)

    def move(self, token, name: str, run_time: float = 0.8):
        """The token to .spot(name): straight along the track when no station is in the way,
        else down into the corridor, along it, and up (never across a station's label)."""
        dest = self.spot(name)
        cur = token.get_center()
        same_row = abs(cur[1] - dest[1]) < 1e-3
        lo, hi = min(cur[0], dest[0]), max(cur[0], dest[0])
        blocked = any(lo < g.frame.get_center()[0] < hi and abs(g.frame.get_center()[1] - cur[1]) < self.bh
                      for g in self.st.values())
        if same_row and not blocked:
            return token.animate(run_time=run_time).move_to(dest)
        cy = self.corridor_y()
        pts = []
        for p in (np.array([cur[0], cy, 0]), np.array([dest[0], cy, 0]), dest):
            if np.linalg.norm(p - (pts[-1] if pts else cur)) > 1e-3:
                pts.append(p)
        lens = [np.linalg.norm(b - a) for a, b in zip([cur] + pts[:-1], pts)]
        tot = sum(lens) or 1.0
        return Succession(*[token.animate(run_time=run_time * L / tot).move_to(p) for p, L in zip(pts, lens)])

    def revise(self, token, run_time: float = 1.4):
        from manim import MoveAlongPath
        arc = self.loop.arc
        start = arc.get_start()
        return Succession(token.animate(run_time=run_time * 0.2).move_to(start),
                          MoveAlongPath(token, arc, run_time=run_time * 0.55),
                          FadeOut(token, scale=0.5, run_time=run_time * 0.25))

    def count(self, k: int, of: int = 2) -> list:
        new = label(f"revisions {k}/{of}", CAPTION, HARNESS).move_to(self.counter)
        old, self.counter = self.counter, new
        self.parts["counter"] = new
        return _swap_text(self, old, new)

    def freeze(self, name: str, color: str = AMBER) -> list:
        g = self.st[name]
        anims = [g.frame.animate.set_stroke(color, 4), g.tint.animate.set_fill(color, 0.2)]
        order = self._order()
        i = order.index(name)
        if i:
            for k, (a, b) in enumerate(RAIL_EDGES):
                if b == name and a == order[i - 1] and self.edges[k] is not None:
                    anims.append(self.edges[k].animate.set_color(color))
        return anims

    def unfreeze(self, name: str) -> list:
        g = self.st[name]
        col = CLOUD if name == "propose" else HARNESS
        anims = [g.frame.animate.set_stroke(col, 3), g.tint.animate.set_fill(col, 0.12)]
        anims += [e.animate.set_color(HARNESS) for e in self.edges if e is not None and e is not self.loop]
        return anims

    def block_loop(self, text: str = "review only") -> VGroup:
        arc = self.loop.arc
        mid = arc.point_from_proportion(0.5)
        bar = Line(mid + DOWN * 0.22, mid + UP * 0.22, color=ERR, stroke_width=8)
        t = label(text, CAPTION, ERR).next_to(bar, DOWN, buff=0.04)
        g = VGroup(bar, t)
        g.bar, g.label = bar, t
        return _keep(g)

    def scripted_seat(self) -> list:
        g = self.st["propose"]
        dashed = DashedVMobject(g.frame.copy(), num_dashes=28).set_stroke(CLOUD, 3)
        tg = scripted_tag().next_to(g.frame, UP, buff=0.08).align_to(g.frame, LEFT)
        self.add(dashed, tg)
        return [g.frame.animate.set_stroke(opacity=0), FadeIn(dashed), FadeIn(tg)]


def hash_chip(h: str = FINGERPRINT16, color: str = LOOKUP, size: float = CAPTION, ell: bool = True) -> VGroup:
    """A PINK hash chip: the first 16 characters of a fingerprint (+ " …")."""
    return _keep(chip(h + (" …" if ell else ""), color, size=size, font=MONO))


TICKET_FIELDS = ("request", "items", "subtotal_cents", "policy", "products")


class Ticket(Piece):
    """V5's approval ticket (S09): a GREEN card "approval ticket" with five empty slots, one per
    fingerprinted field (formaggio/shop/checkout.py lines 31-36: request, items, subtotal_cents,
    policy, products), a "SHA-256" row for the hash and, outside it, the `stock_g` chip crossed
    out (stock is excluded). The card is 5.2 x 3.6; the piece is centred at ORIGIN with the
    (hidden) excluded chip to its right, so place it by its card: tk.shift(p - tk.frame.get_center()).
    Parts: card slots hash excluded (hash and excluded hidden)
        .slot(i) -> slot i's frame   .fill(i) -> anim (a GREEN mono chip writes into slot i)
        .show_hash(h=FINGERPRINT16) -> anims (the PINK hash chip)   .show_excluded() -> anims
        .hash_mob (after show_hash)"""

    def __init__(self, size: float = CAPTION, **kw):
        super().__init__(**kw)
        fr = box(5.2, 3.6, HARNESS, fill=S.BG, fill_opacity=1.0, stroke=3)
        tint = RoundedRectangle(width=5.2, height=3.6, corner_radius=0.14, stroke_width=0).set_fill(HARNESS, 0.06)
        ttl = sans("approval ticket", 22, HARNESS, weight="BOLD").move_to(fr.get_top() + DOWN * 0.3)
        self.part("card", VGroup(fr, tint, ttl))
        self.frame = fr
        slots = VGroup()
        self.slot_frames, self.slot_chips = [], {}
        for i, f in enumerate(TICKET_FIELDS):
            s = box(4.6, 0.4, S.GREY, dashed=True, stroke=1.5).move_to(fr.get_top() + DOWN * (0.8 + i * 0.47))
            slots.add(s)
            self.slot_frames.append(s)
        self.part("slots", slots)
        hl = label("SHA-256", size, LOOKUP)
        hc = hash_chip()
        row = VGroup(hl, hc).arrange(RIGHT, buff=0.2).move_to(fr.get_bottom() + UP * 0.4)
        self.hash_mob = hc
        self.part("hash", row, shown=False)
        ex = _keep(chip("stock_g", S.GREY, size=size, font=MONO))
        ex.next_to(fr, RIGHT, buff=0.3)
        st = strike(ex, ERR)
        ext = label("rechecked, not approved", size, S.GREY).next_to(ex, DOWN, buff=0.1).align_to(ex, LEFT)
        exg = VGroup(ex, st, ext)
        self.part("excluded", exg, shown=False)
        self.move_to(ORIGIN)

    def slot(self, i: int):
        return self.slot_frames[i]

    def fill(self, i: int, run_time: float = 0.5):
        c = _keep(chip(TICKET_FIELDS[i], HARNESS, size=CAPTION, font=MONO, pad_y=0.04))
        c.move_to(self.slot_frames[i])
        self.slot_chips[i] = c
        _stage_hidden(self, c)
        return _Reveal(c, attr="_swop", shift=DOWN * 0.15, run_time=run_time)

    def show_hash(self) -> list:
        return self.parts_in("hash")

    def show_excluded(self) -> list:
        return self.parts_in("excluded")


class Stopwatch(VGroup):
    """S09's "active time" stopwatch (illustration): a face with a crown and a hand driven by a
    ValueTracker (turns). .run(turns=0.5, run_time=2.0) -> anim (the hand sweeps on)
    .pause_look(on=True) -> anim (the face greys while it is stopped)  .freeze() before it leaves.
    1.3 x 1.7 with its label, built at ORIGIN."""

    def __init__(self, text: str = "active time", r: float = 0.5, color: str = HARNESS, **kw):
        super().__init__(**kw)
        self.hi_color = color
        self.face = Circle(radius=r, stroke_color=color, stroke_width=3).set_fill(color, 0.08)
        crown = RoundedRectangle(width=0.2, height=0.12, corner_radius=0.03, stroke_width=0).set_fill(color, 1)
        crown.next_to(self.face, UP, buff=0.02)
        self.tracker = ValueTracker(0.0)
        hub = Dot(radius=0.05, color=color)

        def make_hand():
            h = Line(ORIGIN, UP * r * 0.8, color=color, stroke_width=4)
            h.rotate(-self.tracker.get_value() * TAU, about_point=ORIGIN)
            return h.shift(self.face.get_center())
        from manim import always_redraw
        self.hand_mob = always_redraw(make_hand)
        self.caption = label(text, CAPTION, color).next_to(self.face, DOWN, buff=0.12)
        self.add(self.face, crown, self.hand_mob, hub, self.caption)
        self.crown = crown
        _keep(self)

    def run(self, turns: float = 0.5, run_time: float = 2.0):
        return self.tracker.animate(rate_func=linear, run_time=run_time).increment_value(turns)

    def pause_look(self, on: bool = True):
        col = S.GREY if on else self.hi_color
        return AnimationGroup(self.face.animate.set_stroke(col), self.caption.animate.set_color(col))

    def freeze(self):
        self.hand_mob.clear_updaters()
        return self


class StockShelf(Piece):
    """The shared GREEN shelf (S09 ponder, S13): one bar per cheese, its stock in grams (mono, the
    capture's numbers: c18 stock_g 3000; container/61). Built centred at ORIGIN, about 6.0 wide,
    0.62 per row. StockShelf((("Mimolette", 3000), ("Taleggio", 3000), ("Comté", 6000)), cap=6000);
    numbers=False hides the gram labels (S09: "no numbers yet").
    Parts: rows (name, frame, bar, value)
        .set(name, grams, run_time=0.8) -> anims: the bar drains/fills; the value swaps (old out,
            then new in)
        .need(name, grams) -> a RED dashed outline from the bar's start to `grams` (not added)
        .bar(name) .value(name)"""

    def __init__(self, items=(("Mimolette", 3000), ("Taleggio", 3000)), cap: int = 6000,
                 bar_w: float = 3.4, numbers: bool = True, size: float = CAPTION, **kw):
        super().__init__(**kw)
        self.cap, self.bar_w, self.size, self.numbers = cap, bar_w, size, numbers
        self.rows, self.frames, self.bars, self.values, self.grams = VGroup(), {}, {}, {}, {}
        for i, (name, g) in enumerate(items):
            y = -i * 0.62
            nm = label(name, size, INK).move_to([-bar_w / 2 - 0.2, y, 0], aligned_edge=RIGHT)
            fr = RoundedRectangle(width=bar_w, height=0.34, corner_radius=0.08, stroke_color=HARNESS,
                                  stroke_width=2).move_to([0, y, 0])
            bar = Rectangle(width=max(0.01, bar_w * g / cap), height=0.28, stroke_width=0).set_fill(HARNESS, 0.7)
            bar.move_to(fr.get_left() + RIGHT * (bar.width / 2), aligned_edge=ORIGIN).set_y(y)
            v = mono(f"{g:,} g", size, INK).next_to(fr, RIGHT, buff=0.2)
            if not numbers:
                v.set_opacity(0)
            self.frames[name], self.bars[name], self.values[name], self.grams[name] = fr, bar, v, g
            self.rows.add(VGroup(nm, fr, bar, v))
        self.part("rows", self.rows)
        self.move_to(ORIGIN)

    def bar(self, name: str):
        return self.bars[name]

    def value(self, name: str):
        return self.values[name]

    def set(self, name: str, grams: int, run_time: float = 0.8) -> list:
        fr, bar = self.frames[name], self.bars[name]
        w = max(0.01, self.bar_w * grams / self.cap)
        target = Rectangle(width=w, height=0.28, stroke_width=0).set_fill(HARNESS, 0.7)
        target.move_to([fr.get_left()[0] + w / 2, fr.get_center()[1], 0])
        anims = [Transform(bar, target, run_time=run_time)]
        old = self.values[name]
        new = mono(f"{grams:,} g", self.size, INK).move_to(old, aligned_edge=LEFT)
        row = self.rows[list(self.frames).index(name)]
        self.values[name] = new
        self.grams[name] = grams
        anims.append(AnimationGroup(*_swap_text(row, old, new), run_time=run_time))
        return anims

    def need(self, name: str, grams: int) -> VMobject:
        fr = self.frames[name]
        w = self.bar_w * grams / self.cap
        r = box(w, 0.4, ERR, dashed=True, stroke=2.5).move_to([fr.get_left()[0] + w / 2, fr.get_center()[1], 0])
        return r


# ------------------------------------------------------------------ V6 · drawers, a jar and a capsule (S10-S11)
DRAWERS = (("tasks", "Tasks", "`todos_*`"), ("history", "History", "the conversation"),
           ("memory", "Memory", "`customer_memory.sqlite`"), ("approval", "Approval", "review tickets and decisions"),
           ("audit", "Audit", "SQLite events"))


class Cabinet(Piece):
    """V6 (S10, S11): Act 4's five kinds of state as a cabinet of five GREEN drawers (DRAWERS):
    Tasks · History · Memory · Approval · Audit; every drawer has a handle except Memory (the model
    has no memory tool); only Approval has a YELLOW keyhole. 7.0 x 4.1, built centred at ORIGIN.
    Cabinet(only=("memory", "history")) builds with the other drawers hidden (S10: slides 13/16's
    two memory chips slide into those two, then .reveal(scene, "tasks", "approval", "audit")).
    Parts: frame, and one per drawer name.
        .drawer(name) -> VGroup(face, title, detail[, handle][, keyhole])
        .try_open(name) -> anim (a small shake: it stays shut)
        .open(name, d=0.7) -> anim (the drawer slides out to the right)   .close(name) -> anim
        .keyhole() -> the Approval keyhole (put key_glyph(color=TURN) there)
        .write(name, mob) -> anim: mob slides into the drawer's right end (it becomes a member)
        .handle_point(name) -> where a hand reaches (Memory: the bare spot where a handle would be)"""

    def __init__(self, only=None, size: float = CAPTION, **kw):
        super().__init__(**kw)
        W, dh, gap = 7.0, 0.66, 0.1
        H = len(DRAWERS) * (dh + gap) + 0.3
        fr = box(W, H, HARNESS, fill=S.BG, fill_opacity=1.0, stroke=3)
        self.part("frame", fr)
        self.frame = fr
        self.dr = {}
        top = H / 2 - 0.15
        for i, (key, title, det) in enumerate(DRAWERS):
            y = top - dh / 2 - i * (dh + gap)
            face = box(W - 0.3, dh, HARNESS, fill=S.BG, fill_opacity=1.0, stroke=2.5).move_to([0, y, 0])
            tint = RoundedRectangle(width=W - 0.3, height=dh, corner_radius=0.14, stroke_width=0).set_fill(HARNESS, 0.1).move_to([0, y, 0])
            t = sans(title, size, HARNESS, weight="BOLD")
            d = _rich(det, size, INK)
            row = VGroup(t, label("·", size, S.GREY), d).arrange(RIGHT, buff=0.12)
            row.move_to(face).align_to(face, LEFT).shift(RIGHT * 0.25)
            g = VGroup(face, tint, row)
            g.face, g.title, g.detail, g.handle, g.keyhole = face, t, d, None, None
            hx = face.get_right()[0] - 0.45
            if key != "memory":
                h = RoundedRectangle(width=0.5, height=0.12, corner_radius=0.06, stroke_width=0).set_fill(HARNESS, 0.9)
                h.move_to([hx, y, 0])
                g.add(h)
                g.handle = h
            if key == "approval":
                kh = VGroup(Circle(radius=0.07, stroke_width=0).set_fill(TURN, 1),
                            Polygon([-0.05, 0, 0], [0.05, 0, 0], [0.0, -0.16, 0], stroke_width=0).set_fill(TURN, 1))
                kh.move_to([hx - 0.55, y, 0])
                g.add(kh)
                g.keyhole = kh
            if row.get_right()[0] > hx - (0.85 if key == "approval" else 0.35):
                raise ValueError(f"Cabinet: drawer {title!r} text runs into its handle")
            g.home = np.array([0, y, 0])
            g.spot = np.array([hx, y, 0])
            self.dr[key] = g
            self.part(key, g, only is None or key in only)
        self.move_to(ORIGIN)

    def drawer(self, name: str):
        return self.dr[name]

    def try_open(self, name: str, run_time: float = 0.5):
        return Wiggle(self.dr[name], scale_value=1.0, rotation_angle=0.015 * TAU, n_wiggles=3, run_time=run_time)

    def open(self, name: str, d: float = 0.7, run_time: float = 0.6):
        return self.dr[name].animate(run_time=run_time).shift(RIGHT * d)

    def close(self, name: str, d: float = 0.7, run_time: float = 0.5):
        return self.dr[name].animate(run_time=run_time).shift(LEFT * d)

    def keyhole(self):
        return self.dr["approval"].keyhole

    def handle_point(self, name: str):
        g = self.dr[name]
        return np.array([g.face.get_right()[0] - 0.45, g.face.get_center()[1], 0])

    def write(self, name: str, mob, run_time: float = 0.6):
        g = self.dr[name]
        dest = np.array([g.face.get_right()[0] - 0.2 - mob.width / 2 - (0.6 if g.handle is not None else 0.0),
                         g.face.get_center()[1], 0])
        g.add(mob)
        return mob.animate(run_time=run_time).move_to(dest)


JAR_TOKENS = 16_000          # formaggio/agents/runtime.py line 14
JAR_REPLY = 2_400            # line 15: kept for the reply
JAR_INPUT = JAR_TOKENS - JAR_REPLY          # 13,600: the input budget the marks are on


class ContextJar(Piece):
    """V6's jar (S11, illustration): the context window as a jar of JAR_TOKENS (16,000) tokens, a
    GOLD band at the top "2,400 for the reply" (JAR_REPLY), two marks on its side on the 13,600-token
    input budget: "80 % · trigger" and "50 % · trim to here"; a GREEN dashed capsule slot with a "?"
    at the bottom (slot_h=0.42: one row of capsule text; 0.75: two). Message cards stack upward
    above the slot (no text). A 2.8 x 4.0 jar + its labels (8.0 wide in all), built centred at
    ORIGIN; the full capsule (confirmed request · allergies: nuts · menu …) is a card of yours
    beside the jar, the slot holds its short form.
    Parts: jar band marks title slot
        .pour(scene, n_long=12, n_short=12, run_time=3.0): the notes (GREY, tall) and
            acknowledgements (thin) pour in and stack past the 80 % mark
        .truncate(scene, keep=5, run_time=1.6): the oldest cards slide out over the left rim into a
            GREY heap beside the jar (.heap), the rest drop down: under the 50 % mark
        .capsule_card(text="capsule") -> a GREEN card the size of the slot (not added)
        .pin_capsule(scene, card) / .unpin_capsule(scene) (lifts the old one out)
        .mark_y(frac) -> y of a fraction of the input budget; .cards (the stack)"""

    def __init__(self, h: float = 4.0, w: float = 2.8, slot_h: float = 0.42, size: float = CAPTION,
                 show=None, **kw):
        super().__init__(**kw)
        shown = self._show_set(show, ("jar", "band", "marks", "title", "slot"))
        self.h, self.w, self.size = h, w, size
        self.bottom = -h / 2
        wall = VMobject(stroke_color=S.GREY, stroke_width=4)
        self.wall = wall
        wall.set_points_as_corners([[-w / 2, h / 2, 0], [-w / 2, -h / 2, 0], [w / 2, -h / 2, 0], [w / 2, h / 2, 0]])
        rim = VGroup(Line([-w / 2 - 0.12, h / 2, 0], [-w / 2 + 0.05, h / 2, 0]),
                     Line([w / 2 - 0.05, h / 2, 0], [w / 2 + 0.12, h / 2, 0])).set_stroke(S.GREY, 4)
        self.part("jar", VGroup(wall, rim), "jar" in shown)
        band_h = h * JAR_REPLY / JAR_TOKENS
        band = Rectangle(width=w - 0.1, height=band_h, stroke_width=0).set_fill(COST, 0.25)
        band.move_to([0, h / 2 - band_h / 2, 0])
        bt = label("2,400 for the reply", size, COST).next_to(band, RIGHT, buff=0.25)
        self.part("band", VGroup(band, bt), "band" in shown)
        marks = VGroup()
        for frac, txt in ((0.8, "80 % · trigger"), (0.5, "50 % · trim to here")):
            y = self.mark_y(frac)
            ln = DashedLine([-w / 2, y, 0], [w / 2 + 0.15, y, 0], color=TURN, stroke_width=2.5, dash_length=0.1)
            t = label(txt, size, TURN).next_to(ln, RIGHT, buff=0.12)
            marks.add(VGroup(ln, t))
        self.part("marks", marks, "marks" in shown)
        ttl = VGroup(label("context window", size, INK), mono("16,000 tokens", size, INK)).arrange(DOWN, buff=0.06)
        ttl.next_to(wall, LEFT, buff=0.3).align_to(wall, UP)
        self.part("title", ttl, "title" in shown)
        self.slot_h = slot_h
        slot = box(w - 0.3, self.slot_h, HARNESS, dashed=True, stroke=2.5).move_to([0, -h / 2 + 0.08 + self.slot_h / 2, 0])
        q = sans("?", 24, HARNESS, weight="BOLD").move_to(slot)
        self.slot_box, self.slot_q = slot, q
        self.part("slot", VGroup(slot, q), "slot" in shown)
        self.cards = VGroup()
        self.add(self.cards)
        self.capsule = None
        self.heap = VGroup()
        self.move_to(ORIGIN)

    def mark_y(self, frac: float) -> float:
        return self.wall.get_bottom()[1] + self.h * JAR_INPUT * frac / JAR_TOKENS

    def _stack_top(self) -> float:
        base = self.slot_box.get_top()[1] + 0.06
        return self.cards[-1].get_top()[1] + 0.02 if len(self.cards) else base

    def pour(self, scene, n_long: int = 12, n_short: int = 12, run_time: float = 3.0):
        cw = self.w - 0.4
        cx = self.slot_box.get_center()[0]
        seq = []
        for k in range(n_long + n_short):
            long_ = (k % 2 == 0 and k // 2 < n_long) or k // 2 >= n_short
            c = msg_card(cw, 0.2 if long_ else 0.07, S.GREY if long_ else S.GREY_DARK)
            seq.append(c)
        y = self._stack_top()
        anims = []
        for c in seq:
            c.move_to([cx, y + c.height / 2, 0])
            y += c.height + 0.02
            anims.append(FadeIn(c, shift=DOWN * 1.2))
        scene.play(LaggedStart(*anims, lag_ratio=0.12), run_time=run_time)
        for c in seq:
            scene.remove(c)
            self.cards.add(c)

    def truncate(self, scene, keep: int = 5, run_time: float = 1.6):
        old = list(self.cards.submobjects[:len(self.cards) - keep])
        stay = list(self.cards.submobjects[len(self.cards) - keep:])
        heap_x = self.wall.get_left()[0] - 0.75
        rim = self.wall.get_top()[1] + 0.15
        anims = []
        for k, c in enumerate(old):
            dest = np.array([heap_x + (k % 3) * 0.1, self.wall.get_bottom()[1] + 0.1 + (k // 3) * 0.1, 0])
            anims.append(Succession(c.animate(run_time=0.4).move_to([c.get_center()[0], rim, 0]),
                                    c.animate(run_time=0.6).move_to(dest).scale(0.4).set_opacity(0.5)))
        base = self.slot_box.get_top()[1] + 0.06
        y = base
        drops = []
        for c in stay:
            drops.append(c.animate.move_to([c.get_center()[0], y + c.height / 2, 0]))
            y += c.height + 0.02
        scene.play(LaggedStart(*anims, lag_ratio=0.03), run_time=run_time * 0.7)
        scene.play(*drops, run_time=run_time * 0.3)
        for c in old:
            self.cards.remove(c)
            self.heap.add(c)
        self.add(self.heap)

    def capsule_card(self, text: str = "capsule") -> VGroup:
        fr = box(self.w - 0.3, self.slot_h, HARNESS, fill=S.BG, fill_opacity=1.0, stroke=3)
        tint = RoundedRectangle(width=fr.width, height=fr.height, corner_radius=0.14, stroke_width=0).set_fill(HARNESS, 0.35)
        t = fit_rows(text, fr.width - 0.2, CAPTION, INK, buff=0.04, align=ORIGIN)
        if t.height > fr.height - 0.06:
            raise ValueError(f"capsule card {text!r} needs ContextJar(slot_h >= {t.height + 0.12:.2f})")
        t.move_to(fr)
        g = VGroup(fr, tint, t)
        g.frame = fr
        return _keep(g)

    def pin_capsule(self, scene, card, run_time: float = 0.6):
        card.move_to(self.slot_box)
        anims = [FadeIn(card, shift=UP * 0.3)]
        if self.slot_q.get_fill_opacity() > 0:
            anims.append(self.slot_q.animate.set_opacity(0))
        scene.play(*anims, run_time=run_time)
        scene.remove(card)
        self.add(card)
        self.capsule = card

    def unpin_capsule(self, scene, run_time: float = 0.5):
        if self.capsule is None:
            return
        c = self.capsule
        self.remove(c)
        scene.add(c)
        scene.play(c.animate.shift(UP * 0.6 + LEFT * 2.2).set_opacity(0), run_time=run_time)
        scene.remove(c)
        self.capsule = None


# ------------------------------------------------------------------ V7 · a staircase of skills (S12)
STAIRS = (("Discover", "name + description", "about 100 tokens each"),
          ("Activate", "`load_skill` → `SKILL.md`", "under about 5k"),
          ("Use resources", "`read_skill_resource` →", "`references/`, `assets/` · only what's read"))


class Staircase(Piece):
    """V7 (S12): slide 28 as three steps rising left to right (STAIRS), on a GOLD "token cost"
    axis along the base. Built in place above a 3-row strip: x -6.3..6.3, base y -1.0, tops -0.05,
    0.6, 1.25 (cards stack above the tops, up to y 2.8: step 1 holds 6 cards, step 3 three).
    Parts: steps axis
        .step(i) -> VGroup(frame, rows)   .landing(i, k=0, h=0.46) -> centre of the k-th card
            stacked on step i (cards up to 4.0 wide; make them with skill_card)
        .climb(card, i, k) -> anim (the card moves to .landing(i, k))"""

    def __init__(self, size: float = CAPTION, base: float = -1.0, tops=(-0.05, 0.6, 1.25),
                 step_w: float = 4.15, **kw):
        super().__init__(**kw)
        self.tops, self.base, self.step_w = tops, base, step_w
        steps = VGroup()
        self.steps = []
        for i, ((title, a, b), top) in enumerate(zip(STAIRS, tops)):
            x = (i - 1) * (step_w + 0.05)
            fr = box(step_w, top - base, HARNESS, fill=S.BG, fill_opacity=1.0, stroke=3)
            fr.move_to([x, (top + base) / 2, 0])
            rows = VGroup(sans(title, size, HARNESS, weight="BOLD"),
                          *[r for t in (a, b) for r in fit_rows(t, step_w - 0.3, size, INK)])
            rows.arrange(DOWN, buff=0.06, aligned_edge=LEFT)
            rows.move_to(fr.get_corner(UP + LEFT) + np.array([0.15 + rows.width / 2, -0.1 - rows.height / 2, 0]))
            if rows.get_bottom()[1] < base + 0.04:
                raise ValueError(f"Staircase: step {title!r} is too low for its text (raise its top)")
            g = VGroup(fr, rows)
            g.frame, g.rows = fr, rows
            self.steps.append(g)
            steps.add(g)
        self.part("steps", steps)
        ax = Arrow([steps.get_left()[0], base - 0.02, 0], [steps.get_right()[0] + 0.1, base - 0.02, 0],
                   buff=0, color=COST, stroke_width=5, tip_length=0.2, max_tip_length_to_length_ratio=0.05)
        at = label("token cost", size, COST).next_to(ax, DOWN, buff=0.06).align_to(ax, RIGHT)
        self.part("axis", VGroup(ax, at))

    def step(self, i: int):
        return self.steps[i]

    def landing(self, i: int, k: int = 0, h: float = 0.46):
        fr = self.steps[i].frame
        return np.array([fr.get_center()[0], fr.get_top()[1] + 0.06 + h * (k + 0.5), 0])

    def climb(self, card, i: int, k: int = 0, run_time: float = 0.8):
        return card.animate(run_time=run_time).move_to(self.landing(i, k, card.height + 0.06))


def skill_card(text: str, color: str = HARNESS, size: float = CAPTION, max_w: float = 4.0) -> VGroup:
    """A card naming a loaded skill file (mono: "tasting-planning/SKILL.md",
    "…/references/serving-guide.md"), at most `max_w` wide to sit on a Staircase step: a path too
    wide for one row breaks after its first "/" onto a second row (then 0.75 tall). .frame .rows"""
    rows = [text]
    if mono(text, size).width > max_w - 0.3 and "/" in text:
        k = text.index("/") + 1
        rows = [text[:k], "  " + text[k:]]
    t = VGroup(*[mono(r, size, INK) for r in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
    fr = box(t.width + 0.3, t.height + 0.2, color, fill=S.BG, fill_opacity=0.95, radius=0.12)
    t.move_to(fr)
    g = VGroup(fr, t)
    g.frame, g.rows = fr, t
    if g.width > max_w + 0.01:
        raise ValueError(f"skill card {text!r} is {g.width:.2f} wide (> {max_w}): shorten it with …/")
    return _keep(g)


def skill_tree(root: str, files, dashed: bool = False, crossed=(), size: float = CAPTION) -> VGroup:
    """A skill folder as a small tree: `root` (folder glyph, mono) and its files indented under it
    (folder/file glyphs). dashed=True: the lecture's example (GREY dashed frame + `concept ·
    lecture only` tag above); crossed: names struck through RED (`scripts/lookup.py`). .rows
    (name -> row) .frame .tag"""
    rows = VGroup(file_row(root if root.endswith("/") else root + "/", INK, S.GREY if dashed else HARNESS, size))
    named = {root: rows[0]}
    for f in files:
        r = file_row(f, S.GREY if dashed else INK, S.GREY if dashed else HARNESS, size)
        rows.add(r)
        named[f] = r
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    for r in rows[1:]:
        r.shift(RIGHT * 0.45)
    fr = box(rows.width + 0.5, rows.height + 0.4, S.GREY if dashed else HARNESS, dashed=dashed,
             fill_opacity=0.04, stroke=2.5).move_to(rows)
    g = VGroup(fr, rows)
    g.frame, g.rows, g.tag, g.named = fr, rows, None, named
    for c in crossed:
        g.add(strike(named[c].text, ERR))
    if dashed:
        tg = concept_tag().next_to(fr, UP, buff=0.08).align_to(fr, LEFT)
        g.add(tg)
        g.tag = tg
    return g


# ------------------------------------------------------------------ V8 · evidence (S14-S15)
PILLS = (("Outcome", "did it get the right result?"), ("Trajectory", "did it get there sensibly?"),
         ("Cost", "tokens, turns, latency"))


class ThreePills(Piece):
    """V8 (S14): slide 40's three measures as GREEN bands, top to bottom: Outcome, Trajectory,
    Cost (PILLS: name + question at left), each with a chip area at right where check names drop
    (container/89 lines 39-44: `outcome.proposal`; `process.check_before_action`,
    `process.manager_authority`, `process.no_duplicate_orders`; "model calls · input tokens").
    rows=(1, 3, 1) chips per band; 12.4 x 3.8, built centred at ORIGIN.
    Parts: bands   .slot(i, k) -> centre-left point of chip k in band i
        .start(i, chip) -> chip placed at the right edge on that row (FadeIn it there)
        .drop(i, chip) -> anim (the next free slot of band i, sliding left along its row; the chip
            becomes a member). Never drop a chip from above: it would cross the other bands' text."""

    def __init__(self, rows=(1, 3, 1), width: float = 12.4, size: float = CAPTION, **kw):
        super().__init__(**kw)
        self.rows_n, self.filled = rows, [0] * len(rows)
        bands = VGroup()
        self.bands = []
        y = 0.0
        pitch = 0.52
        for (name, q), n in zip(PILLS, rows):
            h = max(1, n) * pitch + 0.3
            fr = RoundedRectangle(width=width, height=h, corner_radius=min(0.4, h / 2.2), stroke_color=HARNESS,
                                  stroke_width=3).set_fill(HARNESS, 0.06)
            fr.move_to([0, y - h / 2, 0])
            t = sans(name, 24, HARNESS, weight="BOLD")
            qq = label(q, size, INK)
            col = VGroup(t, qq).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
            col.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.35)
            g = VGroup(fr, col)
            g.frame, g.title = fr, col
            self.bands.append(g)
            bands.add(g)
            y -= h + 0.15
        self.chip_left = 4.0          # chips start this far right of a band's left edge
        self.part("bands", bands)
        self.move_to(ORIGIN)

    def slot(self, i: int, k: int):
        fr = self.bands[i].frame
        n = max(1, self.rows_n[i])
        pitch = (fr.height - 0.3) / n
        return np.array([fr.get_left()[0] + self.chip_left, fr.get_top()[1] - 0.15 - pitch * (k + 0.5), 0])

    def start(self, i: int, mob):
        """Put `mob` just right of band i's next free slot, at the frame's right edge (so .drop
        slides it in along its own row, over nothing). Returns mob."""
        p = self.slot(i, self.filled[i])
        return mob.move_to([6.5 - mob.width / 2, p[1], 0])

    def drop(self, i: int, mob, run_time: float = 0.5):
        k = self.filled[i]
        if k >= self.rows_n[i]:
            raise ValueError(f"ThreePills: band {i} is full")
        self.filled[i] += 1
        p = self.slot(i, k)
        dest = p + RIGHT * mob.width / 2
        if dest[0] + mob.width / 2 > self.bands[i].frame.get_right()[0] - 0.15:
            raise ValueError("ThreePills.drop: the chip runs past the band")
        self.bands[i].add(mob)
        return mob.animate(run_time=run_time).move_to(dest)


EVENTS = (("approval.requested", HARNESS), ("approval.decided · human", TURN), ("policy.decision · allow", HARNESS),
          ("order.placed", HARNESS), ("run.finished · completed", HARNESS))


class EventChain(Piece):
    """V8 (S14): the manager-approval run's events as a vertical chain of five cards (EVENTS:
    approval.requested GREEN, approval.decided · human YELLOW, policy.decision · allow, order.placed,
    run.finished · completed GREEN), arrows between. 4.6 x 3.6, built centred at ORIGIN; cards
    hidden at first. Parts: c0..c4, a0..a3
        .card(i)  .light(i) -> anims (card i and the arrow into it fade in, its border thick)"""

    def __init__(self, events=EVENTS, size: float = CAPTION, **kw):
        super().__init__(**kw)
        self.cards = []
        y = 0.0
        for i, (t, col) in enumerate(events):
            c = json_card([t], col)
            c.move_to([0, y - c.height / 2, 0])
            y -= c.height + 0.22
            self.cards.append(c)
            self.part(f"c{i}", c, shown=False)
            if i:
                a = _arrow(self.cards[i - 1].get_bottom(), c.get_top(), color=S.GREY, buff=0.03)
                self.part(f"a{i - 1}", a, shown=False)
        self.move_to(ORIGIN)

    def card(self, i: int):
        return self.cards[i]

    def light(self, i: int) -> list:
        names = [f"c{i}"] + ([f"a{i - 1}"] if i else [])
        return self.parts_in(*names)


CYCLE_STEPS = ("failure observed", "capture a test case", "change one layer", "run the suite k times",
               "compare to baseline · a diff", "merge or iterate · keep the traces")


class Cycle(Piece):
    """V8 (S15): slide 42's improvement loop as six rounded boxes on a closed loop, clockwise from
    the top, each numbered by a badge on its corner: 1 RED "failure observed" … 6 GREEN "merge or
    iterate · keep the traces" (CYCLE_STEPS),
    GREY arrows between; a pile of GREEN test-case cards beside step 2 that grows per lap. 12.5 x
    4.4, built centred at ORIGIN. The loop's inside (4.6 x 2.9) holds one chip slot per box:
    top/bottom boxes centred (y +-0.95), side boxes at their own side (y +-0.45), so two side
    chips on one row share 4.6 (S15: "one prompt line" + `--compare` fit; a 5.8-wide
    `data/agent_evaluation_cases.json` chip does not: put it under the cycle).
    Parts: boxes arrows pile
        .box(i) (0-based)  .light(i, color=TURN) -> anim  .unlight() -> anim
        .anchor(i) -> the inner slot of box i (centre for 0 and 3; the inner edge for side boxes)
        .attach(i, mob) -> anim: mob fades in at its slot (it becomes a member; raises if it
            would leave the inside)
        .grow_pile() -> anim (one more card on the pile)
        .lap(scene, run_time=3.0): every box lights in turn, then the pile grows"""

    def __init__(self, a: float = 4.5, b: float = 1.85, size: float = CAPTION, **kw):
        super().__init__(**kw)
        angles = [PI / 2, PI / 6, -PI / 6, -PI / 2, -5 * PI / 6, 5 * PI / 6]
        self.centers = [np.array([a * np.cos(t), b * np.sin(t), 0]) for t in angles]
        boxes = VGroup()
        self.boxes = []
        for i, (txt, c) in enumerate(zip(CYCLE_STEPS, self.centers)):
            col = ERR if i == 0 else (HARNESS if i == 5 else S.GREY)
            rows = fit_rows(txt, 2.75, size, INK, buff=0.04, align=ORIGIN)
            fr = box(3.15, max(0.72, rows.height + 0.3), col, fill=S.BG, fill_opacity=1.0, stroke=3).move_to(c)
            rows.move_to(fr).shift(RIGHT * 0.1)
            badge = step_badge(i + 1, col if i in (0, 5) else S.GREY, radius=0.17)
            badge.move_to(fr.get_corner(UP + LEFT) + np.array([0.12, -0.05, 0]))
            g = VGroup(fr, rows, badge)
            g.frame, g.text, g.base = fr, rows, col
            self.boxes.append(g)
            boxes.add(g)
        arrows = VGroup()
        for i in range(6):
            p, q = self.boxes[i].frame, self.boxes[(i + 1) % 6].frame
            s0, s1 = self._edge_pts(p, q)
            arrows.add(_arrow(s0, s1, color=S.GREY, buff=0.08))
        self.part("arrows", arrows)
        self.part("boxes", boxes)
        pile = VGroup(*[msg_card(0.55, 0.36, HARNESS) for _ in range(2)])
        for k, c in enumerate(pile):
            c.move_to(self.boxes[1].frame.get_right() + RIGHT * 0.45 + UP * (0.08 * k) + RIGHT * 0.06 * k)
        self.pile = pile
        self.part("pile", pile)
        self.lit = None
        self.move_to(ORIGIN)

    @staticmethod
    def _edge_pts(p, q):
        pc, qc = p.get_center(), q.get_center()
        d = qc - pc
        def exit_pt(m, v):
            hw, hh = m.width / 2, m.height / 2
            k = min(hw / abs(v[0]) if abs(v[0]) > 1e-6 else 1e9, hh / abs(v[1]) if abs(v[1]) > 1e-6 else 1e9)
            return m.get_center() + v * k
        return exit_pt(p, d), exit_pt(q, -d)

    def box(self, i: int):
        return self.boxes[i]

    def light(self, i: int, color: str = TURN):
        anims = []
        if self.lit is not None and self.lit != i:
            o = self.boxes[self.lit]
            anims.append(o.frame.animate.set_stroke(o.base, 3))
        anims.append(self.boxes[i].frame.animate.set_stroke(color, 5))
        self.lit = i
        return AnimationGroup(*anims, group=self)

    def unlight(self):
        if self.lit is None:
            return AnimationGroup(group=self)
        o = self.boxes[self.lit]
        self.lit = None
        return o.frame.animate.set_stroke(o.base, 3)

    def _inner(self):
        """x range and y range of the loop's free inside."""
        xl = self.boxes[4].frame.get_right()[0] + 0.15
        xr = self.boxes[2].frame.get_left()[0] - 0.15
        yt = self.boxes[0].frame.get_bottom()[1] - 0.12
        yb = self.boxes[3].frame.get_top()[1] + 0.12
        return xl, xr, yb, yt

    def anchor(self, i: int):
        xl, xr, yb, yt = self._inner()
        cx, cy = (xl + xr) / 2, (yb + yt) / 2
        if i == 0:
            return np.array([cx, yt - 0.3, 0])
        if i == 3:
            return np.array([cx, yb + 0.3, 0])
        y = cy + (0.45 if i in (1, 5) else -0.45)
        return np.array([xr if i in (1, 2) else xl, y, 0])

    def attach(self, i: int, mob, run_time: float = 0.5):
        p = self.anchor(i)
        if i in (0, 3):
            mob.move_to(p)
        elif i in (1, 2):
            mob.move_to(p + LEFT * mob.width / 2)
        else:
            mob.move_to(p + RIGHT * mob.width / 2)
        xl, xr, yb, yt = self._inner()
        if mob.get_left()[0] < xl - 0.01 or mob.get_right()[0] > xr + 0.01:
            raise ValueError(f"Cycle.attach: a {mob.width:.2f}-wide chip does not fit inside the loop "
                             f"({xr - xl:.2f} wide)")
        self.add(mob)
        return FadeIn(mob, run_time=run_time)

    def grow_pile(self, run_time: float = 0.4):
        last = self.pile[-1]
        c = msg_card(0.55, 0.36, HARNESS).move_to(last.get_center() + UP * 0.08 + RIGHT * 0.06)
        self.pile.add(c)
        return FadeIn(c, shift=DOWN * 0.2, run_time=run_time)

    def lap(self, scene, run_time: float = 3.0):
        per = run_time / 7
        for i in range(6):
            scene.play(self.light(i), run_time=per)
        scene.play(self.unlight(), self.grow_pile(), run_time=per)


class Balance(Piece):
    """V8 (S15, illustration): two batch cards on a balance (A left, B right), level while the
    comparison has no confounders. 6.4 x 2.6, built centred at ORIGIN.
    Parts: stand beam pans   .load(left, right) -> anims (the cards drop onto the pans; members)
        .tilt(angle) -> anim (a confounder would tip it; positive: right side down)"""

    def __init__(self, width: float = 5.6, **kw):
        super().__init__(**kw)
        base = Polygon([-0.5, -1.2, 0], [0.5, -1.2, 0], [0, -0.3, 0], stroke_color=S.GREY, stroke_width=3).set_fill(S.GREY, 0.2)
        post = Line([0, -0.3, 0], [0, 0.35, 0], color=S.GREY, stroke_width=4)
        self.pivot = np.array([0, 0.35, 0])
        beam = Line([-width / 2, 0.35, 0], [width / 2, 0.35, 0], color=S.GREY, stroke_width=5)
        pans = VGroup(*[Line([x - 0.9, 0.35, 0], [x + 0.9, 0.35, 0], color=S.GREY, stroke_width=3).shift(DOWN * 0.02)
                        for x in (-width / 2 + 0.9, width / 2 - 0.9)])
        self.beam_g = VGroup(beam, pans)
        self.part("stand", VGroup(base, post, Dot(self.pivot, radius=0.07, color=S.GREY)))
        self.part("beam", self.beam_g)
        self.width_ = width
        self.move_to(ORIGIN)

    def load(self, left, right, run_time: float = 0.6) -> list:
        anims = []
        for mob, pan in ((left, self.beam_g[1][0]), (right, self.beam_g[1][1])):
            dest = pan.get_center() + UP * (mob.height / 2 + 0.04)
            self.beam_g.add(mob)
            anims.append(mob.animate(run_time=run_time).move_to(dest))
        return anims

    def tilt(self, angle: float = 0.12, run_time: float = 0.8):
        return Rotate(self.beam_g, angle=-angle, about_point=self.stand_pivot(), run_time=run_time)

    def stand_pivot(self):
        return self.parts["stand"][2].get_center()


JUDGES = (("human review", "slow · gold standard", TURN, False),
          ("LLM as judge", "rubric · k samples", S.GREY, True),
          ("deterministic checks", "cheap · auditable", HARNESS, False))


class Judges(Piece):
    """V8 (S15): slide 41's three judges in a row, mirrored to keep the series' sides: left YELLOW
    "human review", middle GREY dashed "LLM as judge" (concept · lecture only: no model judge
    here), right GREEN "deterministic checks". 12.4 x 1.5, built centred at ORIGIN.
    Parts: human llm checks   .judge(i)"""

    def __init__(self, size: float = CAPTION, **kw):
        super().__init__(**kw)
        self.js = []
        for i, (name, sub, col, dashed) in enumerate(JUDGES):
            fr = box(3.9, 1.3, col, dashed=dashed, fill_opacity=0.06, stroke=3).move_to([(i - 1) * 4.2, 0, 0])
            t = sans(name, 24, col if not dashed else S.GREY, weight="BOLD")
            st = label(sub, size, INK)
            col_ = VGroup(t, st).arrange(DOWN, buff=0.1).move_to(fr)
            g = VGroup(fr, col_)
            g.frame = fr
            self.js.append(g)
            self.part(("human", "llm", "checks")[i], g)
        self.move_to(ORIGIN)

    def judge(self, i: int):
        return self.js[i]


# ------------------------------------------------------------------ S02's stage (and S16's badge)
class Stage(Piece):
    """S02's stage (S16 brings it back as a badge): a GREY laptop zone `~/AC215` with two folders
    side by side, `agent-harness/` and `secrets/` (dashed, "empty"); a TEAL container
    `agent-harness` (`user app` · `/.venv`); PINK mounts `agent-harness → /app` and `secrets →
    /secrets`; a GOLD key `-e OPENAI_API_KEY` going in; a GREY crossed-out port "no -p · no ports";
    one PINK "HTTPS" line from the container to a BLUE cloud "OpenAI". 12.4 x 4.2, built centred at
    ORIGIN; parts appear in the script's order with .reveal(scene, …).
    Parts: laptop repo secrets container mount_app mount_secrets key port https cloud
        .shrink(scene, width=3.0, center=None) plays: texts out, then the shapes shrink to a badge
            (top right by default); .grow(scene, center=None) plays it back (S02)
        .badge(width=3.0) -> a glyph-only copy (no text), to FadeIn in a corner (S16)"""

    def __init__(self, size: float = CAPTION, show=None, **kw):
        super().__init__(**kw)
        names = ("laptop", "repo", "secrets", "container", "mount_app", "mount_secrets", "key", "port", "https", "cloud")
        shown = self._show_set(show, names)
        lz = laptop_zone(8.4, 4.2, caption="your laptop · ~/AC215", corner=DOWN + LEFT)
        lz.move_to([-1.9, 0, 0])
        self.part("laptop", lz, "laptop" in shown)
        repo = file_row("agent-harness/", INK, LAPTOP, size)
        repo.move_to([-5.75 + repo.width / 2, 1.3, 0])
        sec_g = folder_glyph(0.22, S.GREY)
        sec_t = mono("secrets/", size, S.GREY)
        sec = VGroup(sec_g, sec_t).arrange(RIGHT, buff=0.12)
        sec_box = box(sec.width + 0.3, sec.height + 0.2, S.GREY, dashed=True, stroke=2).move_to(sec)
        sec_note = label("empty", size, S.GREY).next_to(sec_box, DOWN, buff=0.06)
        secrets = VGroup(sec_box, sec, sec_note)
        secrets.move_to([-5.75 + secrets.width / 2, -0.2, 0])
        self.part("repo", repo, "repo" in shown)
        self.part("secrets", secrets, "secrets" in shown)
        ctr = container_box("agent-harness", w=3.0, h=2.5, color=CTR)
        ctr.move_to([0.6, 0.25, 0])
        rows = VGroup(mono("user app", size, INK), mono("/app", size, INK), mono("/secrets", size, S.GREY),
                      mono("/.venv", size, INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        rows.next_to(ctr.title, DOWN, buff=0.18).align_to(ctr.frame, LEFT).shift(RIGHT * 0.3)
        self.ctr_rows = rows
        self.part("container", VGroup(ctr, rows), "container" in shown)
        m1 = Arrow(repo.get_right() + RIGHT * 0.1, rows[1].get_left() + LEFT * 0.1, buff=0, color=LOOKUP, stroke_width=3,
                   tip_length=0.15, max_tip_length_to_length_ratio=0.1)
        m1t = label("live: your edits show inside", size, LOOKUP).next_to(repo, DOWN, buff=0.12).align_to(repo, LEFT)
        self.part("mount_app", VGroup(m1, m1t), "mount_app" in shown)
        m2 = Arrow(secrets.get_right() + RIGHT * 0.1, rows[2].get_left() + LEFT * 0.1, buff=0, color=LOOKUP,
                   stroke_width=3, tip_length=0.15, max_tip_length_to_length_ratio=0.1)
        self.part("mount_secrets", m2, "mount_secrets" in shown)
        k = key_glyph(0.28, KEY, name="-e OPENAI_API_KEY").move_to([-3.6, -1.35, 0])
        self.part("key", k, "key" in shown)
        port = VGroup(Circle(radius=0.16, stroke_color=S.GREY, stroke_width=3), cross_mark(0.26, S.GREY, 4))
        port_t = label("no -p · no ports", size, S.GREY).next_to(port, DOWN, buff=0.08)
        pg = VGroup(port, port_t).next_to(ctr.frame, DOWN, buff=0.15)
        self.part("port", pg, "port" in shown)
        cl = cloud(2.2, CLOUD).move_to([5.2, 0.9, 0])
        clt = label("OpenAI", size, INK).move_to(cl)
        self.part("cloud", VGroup(cl, clt), "cloud" in shown)
        hl = Line(ctr.frame.get_right(), cl.get_left() + RIGHT * 0.02, color=LOOKUP, stroke_width=3)
        ht = label("HTTPS", size, LOOKUP).next_to(hl, DOWN, buff=0.06)
        self.part("https", VGroup(hl, ht), "https" in shown)
        self.ctr = ctr
        self.move_to(ORIGIN)

    def badge(self, width: float = 3.0) -> VGroup:
        g = self.glyph_only()
        g.scale_to_fit_width(width)
        return g

    def _texts(self) -> list:
        return [m for m in self.get_family() if isinstance(m, Text)]

    def shrink(self, scene, width: float = 3.0, center=None, run_time: float = 1.0):
        """Plays: the texts fade out first (they stay members at opacity 0), then the shapes shrink
        to `width` at `center` (default: the top-right corner, under the lecture tag's row). Never
        Transform the stage into its badge: its text would morph."""
        if center is None:
            center = np.array([6.5 - width / 2, 3.45 - width * self.height / self.width / 2, 0])
        texts = self._texts()
        for t in texts:
            _save_op(t, "_bop")
        self._full = (self.width, self.get_center().copy())
        scene.play(*[t.animate.set_opacity(0) for t in texts], run_time=run_time * 0.35)
        scene.play(self.animate.scale(width / self.width).move_to(center), run_time=run_time * 0.65)

    def grow(self, scene, center=None, run_time: float = 1.0):
        """Plays: back to full size (at `center`, default where it was), then the texts fade in."""
        w, c = getattr(self, "_full", (self.width, ORIGIN))
        scene.play(self.animate.scale(w / self.width).move_to(c if center is None else center),
                   run_time=run_time * 0.65)
        scene.play(*[_Reveal(t, attr="_bop") for t in self._texts()], run_time=run_time * 0.35)
