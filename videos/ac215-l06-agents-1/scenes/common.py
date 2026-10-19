"""Shared code for AC215 L6 (LLM: Agents I; follow-along: dlops-io/llm-rag "Agents",
dlops-io/llm-agent-google-adk and three Colab notebooks): paths, narration, the semantic colours of
BRIEF.md, the README / notebook trackers, loaders for the real captures in assets/ (the
instructor's name masked on the way in), terminal / panel / card helpers, and the video's recurring
pictures V1-V8 of BRIEF.md. Built from L05's common.py (generic helpers kept) with L06's set pieces.
Tested on screen by build/common_test.py (explainer.check / explainer.preview).

Notes for scene authors
=======================

    from common import *      # every scene: SAY = NARRATION["S07"]; assert len(SAY) == n;
                              # one `with self.voiceover(SAY[i]) as vo:` per SAY line, in order
Everything below draws text at 20-26 pt. Never .scale() a group that holds text below 1.0: use
piece.rescale(k) (shapes shrink, text keeps its size). Frame budget: the tracker band is y 2.85..3.5
(x -6.5..-0.1 at most), lecture_ref top right; the call strip (S04 end - S07) sits under the
tracker, y 2.25..2.75; a 3-row strip's top is STRIP_TOP (-1.44), so a picture above a strip has
y -1.3..2.2 (or ..2.8 without the call strip); keep x in [-6.6, 6.6]. The V1 mini-map (3.2 x 1.6)
sits at MINI_CENTER (bottom right, y -3.55..-1.95) when nothing else is down there, at
MINI_ABOVE_STRIP (y -1.35..0.25) while the 3-row strip is up; hide it while a code panel or a
terminal taller than the strip is up (script.md: it never flickers within a beat).

The instructor's name is never on screen. capture(), excerpt(), src_panel(), log_panel(),
output_box() and every term() line mask it on the way in: unname(s) turns "Pavlos Protopapas",
"Protopapas", "Pavlos", "pavlos", "PAVLOS" into MASK = "‹instructor›", drawn GREY. Text you build
yourself from a capture or source line goes through unname() too (mtext() does it and greys the
mask). The captured files stay unchanged. Emoji the mono font drops raise ValueError: leave the
line out, or pass strip_emoji=True (script.md: cell-57 line 11 only).

Data and sources
    NARRATION["S01"] ... ["S16"]   SAY lines from script.md      TITLES[cls], SPEC (video.yaml)
    capture(name, folder) -> Capture   assets/terminal/<folder>/<name>.txt; name may be the number
        alone ("07" -> 07-uv-sync.txt; "06" never picks the .plain log), or "folder/name" as one
        argument. Folders (CAPTURE FOLDERS): laptop, cli-container, adk-laptop, mcp-remote,
        expected (line 1 is a '#' provenance header; out-txt-agent-run.txt = out.txt from file
        line 2, so out.txt's own line = file line - 1). Never: capture-only/, laptop/04 (a user
        name), adk-laptop/11 (capture plumbing).
        .cmd (the `$` line without "$ "; a heredoc's first line only) .lines .exit .first
        .line(n) one FILE line   .at(2, (5, 7), "…", 33) lines BY FILE LINE NUMBER, "…" inserted
        .join(7, 8, 9) lines the capture wrapped at 80 columns, joined (the spaces lost at a row's
        end restored)   .cut(6, "x") line 6 up to and including "x"
        .fold(21, 31, 'X … Y') the script's "a–b folded to X": checks that every piece of X
        between the '…'s is the lines' own text, in order (whitespace-normalised); returns X
        .typed(n) the command on prompt line n   .pick() L1-style (pick index = file line - 1)
        Lines the script never shows raise ValueError: laptop/09:2 (only via .cut(2,
        "2026-09-22")) and :7, cli-container/34:16-25, adk-laptop/12:5-7 and :140.
    source_text(path)  excerpt(path, a, b)   files in assets/source; a bare name resolves to
        llm-rag/ first, then llm-agent-google-adk/ ("cli.py", "agent_tools.py",
        "1-baseline/agent.py", "pyproject.toml" = llm-rag's: say "llm-agent-google-adk/
        pyproject.toml" for ADK's), colab cells as "colab/<notebook>/cell-NN.py" (notebooks:
        cheese-quiz, travel-planner, cheese-newsletter; the USERS cell is only ever
        "colab/cheese-newsletter/cell-16.redacted.py"). Never shown (raise): any cell-00, Tolminc
        line 1 (both versions).   cell_title(path) the cell's "# @title" (or None)
    split_prompt(line) -> (prompt, cmd) | None    strip_emoji(s)   apps(line) -> list (a JSON list)
    QUESTION (masked, cli.py:435)  CQ_QUESTION (Cheese Quiz cell 37)  ENUM_AUTHORS (9, masked)
    BOOKS (11 titles, cli-container/20)  STATE_KEYS  ADK_AGENTS  RENAMES  WHEEL_TAGS  MCP_TOOLS (14)
    MCP_KEPT  BUDGET (5 (key, dollars) from c27)  BUDGET_TOTAL  BUDGET_CAP  COUNTS  MODEL_RAG
    MODEL_CQ  MODEL_NL  MODEL_ADK  PROJECT_ID  KEY_FILE  API_KEY_PLACEHOLDER  DEV_UI

Colours (BRIEF.md, binding; the colour of a card says who wrote it)
    LAPTOP GREY · CLOUD (= MODEL = GOOGLE) BLUE · CTR TEAL · SYSTEM ORANGE · DATA (= VENV =
    CHECKED) GREEN · TOOL (= FRAMEWORK) PURPLE · ERR RED · TURN YELLOW · COST (= KEY) GOLD ·
    LOOKUP PINK · INK white · FUTURE GREY (dashed: lecture-only concepts, L07)
Running example
    P_HOME P_WS ("student@laptop:~/AC215$") P_REPO (…/llm-rag$) P_ADK (…/llm-agent-google-adk$)
    P_CTR "app@abcf218747d0:/app$"  CTR_TITLE "container · llm-rag-cli"  SECOND "laptop · second
    terminal"

Trackers (top-left, YELLOW; the head names the source: "llm-rag", "ADK", "Colab · Cheese Quiz")
    tracker(key, step=None)  keys = script.md's TRACKER names: Prereq Run Load Agents (llm-rag);
        Start RunAg Base Mcp (ADK); CQ-Pre CQ-Agent CQ-Inputs CQ-Tools CQ-Guild TP NL (Colab).
        SECTIONS[key] = (source, section, steps). step None = no step lit yet.
    self.play(tr.goto(k))     caption_extra(tr, on) -> Transform " · extra"
    tr = switch_section(self, tr, "Load", 1)   old tracker lifts away, new one drops in
    lref("20–22") = lecture_ref(6, ...) top right;  lref_swap(scene, old, "35–40") -> new
    CallStrip()  "call 1 → your code → call 2" under the tracker (y 2.25..2.75, x from -6.5);
        .light(i) -> anim (0, 1, 2; None = all GREY)

Terminal helpers (term() returns a Terminal that greys MASK and '…' on every line it places)
    term(prompt=P_REPO, rows=12, title=None, container=False, top=None)  12.6 wide, 22 pt, 65
        chars a row, bottom at BOTTOM (or top edge at `top`); container=True: TEAL frame, title
        CTR_TITLE, prompt P_CTR unless given
    enter_container(t, prompt=P_CTR) / leave_container(t, prompt=P_REPO) -> list of animations
    resize(scene, t, rows, keep=None, anchor="bottom")   strip_top(rows)  STRIP_TOP
    bare_prompt(scene, t)   type_cmd(scene, t, cmd): use it for every typed command (folds a long
        line at spaces, quote-aware, " \\" + 4-space indent)   cd_prompt(scene, t, new_prompt)
    second_terminal(scene, prompt=P_REPO, rows=7, top=2.75, intro=False) slides one in (title SECOND)
    session(scene, t, cap, *spec, wrap=False, colors=None) -> {file line: mobject} (laptop/06)
    print_build(scene, t, rows)  Compose / BuildKit rows, times as GREY tags
    beside(mob, t, line) / pin(scene, line, mob) / unpin(scene, line, mob)   tags that scroll
    col_box(line, a, b) box over character columns  bracket(mobs, text) left-margin bracket
    under(mob) strike(mob) ring(mob)  grey_masks(line)  at_bottom(mob)

Panels and cards
    src_panel(path, a, b=None, focus=None, size=22, shown=None, suffix=None, wrap=None,
        join=None, subtitle=None)  code_panel from assets/source, header "shown · lines a–b".
        Folded: src_panel(path, [95, (96, 100), (103, 107)]) shows only those lines, a GREY '…'
        row at each gap, header "lines 95–107 (folded)". join=[(470, 472)] makes lines 470-472
        one row (stripped, concatenated). wrap=True breaks lines > 65 chars at spaces into GREY
        ↪ rows; wrap={33: ["Expand"]} breaks before substrings. Colab cells get the header
        "Cheese Quiz · cell 12 · lines 3–4"; subtitle=True adds the cell's @title in GREY quotes
        after the header, subtitle="your copy: baseline/agent.py" any GREY text. At most 12 rows.
        .bar(file_line, colour) -> line bars (not added) .span(file_line, sub) .rows_of(n)
    your_copy(path) -> "your copy: baseline/agent.py" (after S10's rename)
    log_panel(lines, header, width=12.6)  PANEL: plain mono rows (.rows .frame .header)
    output_box(lines, header=None, width=None)  RECORDED: a notebook cell's saved output (never a
        terminal frame): GREY left rule, mono rows; tag it saved_run_tag()
    readme_chip(where, phrase, expected=False) one line (<= 9 wide)   readme_card(where, lines)
    excerpt_chip(sub, header, line=None)  exact sub-string chip   cmd_chip(cmd, note_=None)
    note(text) GREY caption  sans(text)  mtext(s, size, colour, font=MONO) masked text  fix_chip(text)
    turn_card(rows, header="your turn")  rows: "cmd" (mono), (cmd, "extra"), (cmd, note),
        Prose("…"), (Prose("paid per call"), COST) for the GOLD last line
    card_rows(items, header=None)  LookFor(items) .write_item(i)  table_card(headers, rows)
    extra_card(purpose) the GREY "extra · an extra check · in the study guide" card (code never
        shown)  what_if_frame() RED dashed "what if · just watch" (built in place)
    ponder_at(scene, question, seconds=8, y=-2.2, hide=()) the ponder card in the lower third
        (FadeOut it at the start of the next block; `hide` fades those mobjects out with it)
    Counter(text, value) .count_to(n) .freeze()   CallCounter(n=0) GOLD "N calls" .count_to(n,
        run_time) (ticks one by one) .with_time("39.34 s") -> anim
    colab_frame(title, width=12.9, top=2.75, bottom=-3.5) BLUE notebook frame + illustration tag
        (built in place; .frame .title .tag)   menu_path(["File", "Save a copy in Drive"])
        .light(i) -> anim   definition_card() slide 26's definition (.until = "until the task
        is done")   pick_card(text) BLUE "top pick" card; repick(card, text) -> anim
    Dropdown(entries, title="Select an agent") .row(name) .pick(name, colour) -> anim

Tags (keep their size in rescale): your_turn() extra_tag() illustration_tag(note_=None)
    recorded_tag(s="recorded") staff_run_tag() ("recorded · the staff's run, September 22, 2026",
    old_book=True adds " · old book") saved_run_tag() ("recorded · the staff's last saved run")
    expected_tag() standin_tag() (PINK) nokey_tag() placeholder_tag() notsent_tag()
    ("built, not sent") recording_tag() ("at the time of recording") erratum_tag(note_=None)
    fix_tag() ("fix · not in the README") differ_tag() concept_tag(s="concept · lecture only")
    (GREY dashed) cost_tag(s="paid · per call") (GOLD) harmless_tag() preview_tag() grey_tag(s)
    stamp(text, colour) fix_chip(text) concept_box(text) (GREY dashed box)

Glyphs (small; built at ORIGIN)
    key_glyph(h=0.3, name=None) GOLD key · key_outline() · padlock() · person() (= person_icon
    look) · pencil(colour) (the model's pen: pencil(color=CLOUD)) · gear(r, colour) · file_row(name)
    · ghost_file(name) · cylinder(w, h) TEAL database (.top .body .frame) · chunk_card(w, h) ·
    vec_glyph(n) · model_box(name, sub=None) BLUE · model_chip("gpt-4o") · question_card(text)
    PINK · menu_card(sig) GREEN mono · answer_bars(n) · seal(r) BLUE thought signature · diamond(text)
    decision · calculator_glyph(h) · sticky_note(text) · receipt_token(path) GREEN · notebook_glyph()
    · container_box(title, w, h) TEAL · laptop_zone(w, h) GREY · wheel_glyph(r) · cost_tick() GOLD
    · mini_envelope(text) · call_card(rows) BLUE {name, args} card with .seal · response_card(text,
    note=None) TEAL · json_card(lines, colour) · one_lap_row() S08's llm-rag lap (.steps)

Set pieces: Piece = VGroup + named parts (as in L05). A part not shown yet is a member at
    opacity 0: it moves and scales with the piece. show=(...) names the parts visible at first
    (default: all). self.play(*piece.parts_in("a", "b")) fades parts in; parts_out() back to 0;
    piece.reveal(scene, *names) / piece.hide(scene, *names) play it themselves; dim_to(k)/undim().
    Never piece.set_opacity(...), never FadeOut a member: FadeOut the whole piece. Methods return
    ANIMATIONS (play them) or MOBJECTS (not added: FadeIn them yourself). Built centred at ORIGIN
    unless "in place" is said: .move_to(...) them; rescale(k) shrinks shapes, keeps text.

    V1 Anatomy(box_w=7.4, block_h=1.0, bar_h=0.72, ends=True, show=ALL)  slide 27 redrawn,
       12.2 x 4.1 (box 7.4 x 4.1; ends: "Task / Goal" chip -> box -> dashed "Task completion").
       Parts: task a_in box head core instructions control tools memory a_out done (+ inside
       control: control_dash, control_fill). core BLUE, the others GREY outlines, control dashed.
       .light(name, colour=TURN) -> anim (unlights the previous) .unlight() -> anim
       .fill_control(colour=TOOL) -> [anims] (dashed -> solid PURPLE: the framework writes it)
       .fill(name, items) -> (chips, [anims]) chips ("`mono`" or serif, or mobjects) in rows under
       the block's name (control: one row after its name); raises if they don't fit (S16:
       Anatomy(box_w=11.8, block_h=1.75, ends=False) holds the recap's chips)
       .block(name) .frames[name] .names[name]. Compact: Anatomy(box_w=4.6, block_h=0.8,
       ends=False, size=20) is 4.6 x 3.5 (S11's labelled map).
       definition_card(): slide 26's sentence (S02, S08)
    AnatomyMini(center=MINI_CENTER)  the mini-map, 3.2 x 1.6, glyph only (a plain VGroup:
       FadeIn/FadeOut it, mm.animate.move_to(MINI_ABOVE_STRIP)). .light(name) .unlight()
       .fill_control() -> anims. Names as Anatomy.BLOCKS.
    V2 Envelope(width=4.6, slots=7, pitch=0.5)  4.6 x 4.4 (slots=3: 2.4 tall): body, flap (closed
       V in the top margin), pocket V (bottom margin); sheets stack as rows inside (never crossed
       by a line). .sheet(text, colour=GREY, mono_=False, seal=False) -> a sheet (not added)
       .add_sheet(scene, sheet, start=None) plays it into the next slot (from `start`, default
       2.5 left; a sheet already on screen flies from where it is) and makes it a member
       .remove_sheet(scene, sheet, shift=RIGHT*2.5) slides it out, restacks the rest
       .slot_point(i) .sheets (list) .open() / .close() -> anims (flap) .seal_on(sheet) -> seal
    V3 MenuColumn(show=ALL)  in place, 8.4 x 5.9 (y -3.13..2.57): strip (slide 8: question ->
       Retrieval -> LLM -> Response, y 2.3), column (BLUE llm_top, six GREY dashed technique boxes box0..box5 =
       MenuColumn.TECHNIQUES, BLUE llm_bot), chooses (YELLOW), agentic (GREY), menu0 menu1 (GREEN
       menu cards). .fly_in(i, start=None) -> anim  .to_menu() -> [anims] (the five other boxes
       fade, the two menu cards appear, "retrieval decision" stays under them)
       .cross_decision() -> RED line (not added)
       TrustStage(compact=False, show=ALL)  in place, 12.7 x 4.3 (x -6.35..6.4, y -2.0..2.3): BLUE
       cloud "Google Cloud" + model_box "Gemini · location global" | dashed boundary, PINK "HTTPS"
       | GREY laptop with TEAL llm-rag-cli (cli.py, agent_tools.py) and TEAL llm-rag-chromadb
       (cylinder, char-split-collection, book · author · year). compact=True: 12.7 x 2.25 (y
       -1.32..0.93; the containers hold only their names, a small cylinder): shift it up for the
       upper half above a panel (don't rescale: the text would overflow its boxes). Parts: cloud
       model boundary https laptop cli chroma, hidden: lock gear hl_cli hl_chroma hl_model.
       .send(mob, to="laptop"|"cloud", y=None) -> anim (to that side of the boundary)
       .dip() -> PINK arrow cli -> cylinder (not added) .chunk_cards(n=10) -> GREEN cards under
       the CLI box (not added) .light(name) / .unlight(name) -> [anims] (a YELLOW outline over
       "cli", "chroma" or "model")
    V4 HubSpokes(show=ALL) 7.3 x 5.1: core (BLUE "LLM core") + sheet (GREY "instructions") over
       hub ("decision maker"), nodes planner / tools / memory (GREY), spokes sp_planner sp_tools
       sp_memory (two-way arrows). .merge() -> [anims] (core and sheet sink into the hub)
       .spokes() -> [anims]
       LoopTrack(cap=12) 7.6 x 3.9: a clockwise track, BLUE "model" station (top), PURPLE "tools"
       (bottom), YELLOW token, counter "turn 0 / 12", an exit to a Gate "final response" (.gate).
       .lap(run_time=1.6) -> anim (one lap, then the counter ticks) .set_count(k)
       .reply_card() -> GREY "text · no function call" card at the exit (not added)
       one_lap_row(): llm-rag's run, call 1 -> your code -> call 2 -> end (.steps)
    V5 VersionLine(first=10, last=16, lo=10, width=11.0)  11.25 x 1.6: Python 3.x ticks, the GREEN
       band >=3.10 off the right end + its label. .point(minor) .dot(minor, text, colour)
       .drop(minor, text, colour=TOOL) -> arrow + dot + label (not added) .collapse(minor,
       text=None) -> [anims]
       WheelShelf()  9.5 x 1.7: onnxruntime 1.31.0's wheels cp311 … cp314t + an empty dashed cp315
       slot. .wheel(tag) .missing() -> [anims] (cp315 turns RED) .click(tag="cp313") -> [anims]
    V6 Whiteboard(keys=STATE_KEYS)  6.8 x 3.55: GREEN "session state" board with three cells
       (mono key + dashed slot) and a GREY "events" column. .slot(i) .blank_card(i) -> GREEN card
       sized to cell i (not added) .fill(i, card) -> anim (card into slot i) .event_block(text)
       -> the next event block, placed (not added; FadeIn it)
       AgentCard(name, instruction, hole=None)  BLUE mono name chip over a GREY instruction card
       (mono, masked); hole="{itinerary_validation}" draws a PINK hole around it (.hole).
       .fill_hole(card) -> [anims] (.model .card .line)
    V7 ToolBins()  12.6 x 2.75: bins data / action / orchestration (BINS), each titled name over
       what (GREY).
       .drop(chip, "data") -> anim (stacks top-down; at most 3, chip <= 3.7 wide) .bin(name)
       mini_bin(text="orchestration") small GREY bin glyph (S13)
       ServiceFan(show=…)  in place, 12.6 x 5.0: agent box (4 tool pills), ten GREY wires to ten
       service boxes (SERVICES, slide 52's labels), hidden customs ("custom code" blocks), host
       (title "MCP host" + client ports), trunk (PINK "same protocol"), adapters ("MCP server").
       .custom_in(i) -> anim .to_mcp() -> [anims]
       Sieve()  11 x 2.6: the 14 MCP tools as GREY chips (5 named, 9 blank pills) over a
       `tool_filter` sieve. .fall() -> [anims] .sift() -> [anims] (3 pass GREEN, write_file and
       edit_file bounce RED, the rest dim)
       plug_line(a, b, text) PINK transport line + label; mini_envelope(text) a small envelope
    V8 Gate(text="FINAL", colour=TURN, gate_w=1.4, gate_h=1.7, slot=False)  one look for S08's
       "final response" / MaxTurnsExceeded, S14's turnstile and S15's SUCCESS door. .open()
       .close() -> anim (the bar swings) .slam(colour=ERR, text=None) -> anim .relabel(text,
       colour) -> anim .stamp_on(card, text, colour) -> stamp (not added) .slot (slot=True)
       BudgetTape()  S14's calculator: 880 + 1,000 + 600 + 150 + 60 = 2,690 of 6,000 (c27).
       .row_anims() -> [anims] one per row, then the total
    CostDial(radius=0.55) GOLD dial without digits (.run(scene, turns, secs) .freeze())

Capture folder names (assets/terminal): laptop, cli-container, adk-laptop, mcp-remote, expected
(never: capture-only).
"""

from __future__ import annotations

import ast
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
    Arrow,
    Circle,
    CurvedArrow,
    DashedLine,
    DashedVMobject,
    DecimalNumber,
    Dot,
    Ellipse,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    Line,
    ManimColor,
    Mobject,
    Polygon,
    Rectangle,
    ReplacementTransform,
    Rotate,
    RoundedRectangle,
    Succession,
    Text,
    Transform,
    ValueTracker,
    VGroup,
    VMobject,
    always_redraw,
    linear,
    rush_into,
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
LAPTOP = S.GREY          # your laptop: ~/AC215, the clones, the terminal, the browser, .env as a file, the human
CLOUD = S.BLUE           # every model and what it writes; hosted web_search, the remote MCP server, Colab's VM
MODEL = CLOUD
GOOGLE = CLOUD
CTR = S.TEAL             # llm-rag-cli, llm-rag-chromadb and the collection; the function response llm-rag builds
SYSTEM = S.ORANGE        # a Python that was already on the machine (none on the ADK laptop)
DATA = S.GREEN           # declarations (menu cards), chunks, state cells, .python-version, what a harness checked
VENV = DATA
CHECKED = DATA
TOOL = S.PURPLE          # docker/Compose, uv, Node/npx, ADK, the Agents SDK, FastMCP; the loop a framework runs
FRAMEWORK = TOOL
ERR = S.RED              # errors and "avoid this"
TURN = S.YELLOW          # your turn, the trackers, look here now, the block in focus, PENDING
COST = S.GOLD            # every paid call (a GOLD tick), the three keys
KEY = COST
LOOKUP = S.PINK          # the question, search_content, routes, transports, ports, {key} holes, the nearest .env
INK = S.WHITE
DIMMED = S.GREY
FUTURE = S.GREY          # dashed: lecture-only concepts, L07

# ------------------------------------------------------------------ the instructor's name
MASK = "‹instructor›"
_NAME = re.compile(r"pavlos\s+protopapas|protopapas|pavlos", re.IGNORECASE)


def unname(s: str) -> str:
    """The instructor's name (any case, with or without the surname) -> MASK. Every panel line goes
    through this (capture(), excerpt() and the panels do it for you)."""
    return _NAME.sub(MASK, s)


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
    """s without the characters the mono font drops (and the space they leave)."""
    bad = dropped_chars(s)
    if not bad:
        return s
    out = "".join(ch for ch in s if ch not in bad)
    return re.sub(r"(?<=\S) {2,}(?=\S)", " ", out).lstrip() if out.strip() else out


def _emoji_guard(s: str, where: str, strip: bool) -> str:
    if strip:
        return strip_emoji(s)
    bad = dropped_chars(s)
    if bad:
        raise ValueError(f"{where}: {bad!r} would vanish (the mono font has no glyph): leave the line "
                         "out, or pass strip_emoji=True (script.md: print it without its emoji)")
    return s


# ------------------------------------------------------------------ the running example
USER, HOST = "student", "laptop"
P_HOME = f"{USER}@{HOST}:~$"
P_WS = f"{USER}@{HOST}:~/AC215$"
P_REPO = f"{USER}@{HOST}:~/AC215/llm-rag$"
P_ADK = f"{USER}@{HOST}:~/AC215/llm-agent-google-adk$"
P_CTR = "app@abcf218747d0:/app$"           # laptop/06 line 41
CTR_TITLE = "container · llm-rag-cli"
SECOND = "laptop · second terminal"

PROJECT_ID = "your-project-id"
KEY_FILE = "llm-service-account.json"
API_KEY_PLACEHOLDER = "your_google_ai_api_key_here"
DEV_UI = "localhost:8000/dev-ui/"
MODEL_RAG = "gemini-3.1-flash-lite"         # llm-rag's GENERATIVE_MODEL; the model the video recommends for ADK
MODEL_ADK = "gemini-2.5-flash"              # .env.example's GEMINI_MODEL
MODEL_CQ = "gpt-4o"                         # Cheese Quiz
MODEL_NL = "gpt-5.6-luna"                   # Cheese Newsletter
STATE_KEYS = ("itinerary_validation", "travel_plan", "trip_summary")      # adk-laptop/31
ADK_AGENTS = ("ItineraryValidator", "TravelPlanner", "TripSummarizer")
RENAMES = {"1-baseline": "baseline", "3-mcp-tools": "mcp_tools", "5-custom-agent": "custom_agent"}
WHEEL_TAGS = ("cp311", "cp312", "cp313", "cp313t", "cp314", "cp314t")    # adk-laptop/07 lines 9-11
MCP_KEPT = ("list_directory", "read_file", "search_files")                # 3-mcp-tools/agent.py:28
COUNTS = {"books": 11, "chunks": 8248, "story": 24, "enum": 9, "cottage": 178, "womans": 1505,
          "response_chars": 3509, "tokens_call1": 247, "tokens_call2": 1269, "mcp_offered": 14,
          "mcp_seen": 3, "max_turns": 12, "max_iterations": 16, "reasoning_calls": 11,
          "packages": 189}

# ------------------------------------------------------------------ layout
BOTTOM = -3.5                    # terminal bottom edge (fixed when it grows or shrinks)
TRACK_LEFT, TRACK_TOP = -6.5, 3.5
TERM_W, TERM_PT = 12.6, 22
CALL_TOP = 2.75                  # the call strip's top edge, under the tracker
MINI_CENTER = np.array([4.98, -2.75, 0])         # bottom right, nothing else down there
MINI_ABOVE_STRIP = np.array([4.98, -0.55, 0])    # bottom right, above a 3-row strip

# ------------------------------------------------------------------ README / notebook trackers
SECTIONS = {
    # dlops-io/llm-rag README.md @ e17a39f (script.md "Trackers")
    "Prereq": ("llm-rag", "Prerequisites", ["Clone repo"]),
    "Run": ("llm-rag", "Run Container", ["cd llm-rag", "Set GCP_PROJECT", "Run script"]),
    "Load": ("llm-rag", "Load (L05)", ["Load char-split"]),
    "Agents": ("llm-rag", "Agents", ["Run agent", "Agent tool"]),
    # dlops-io/llm-agent-google-adk README.md @ f89faa7 (+ two module READMEs)
    "Start": ("ADK", "Getting Started", ["Clone repo", "cd folder", "Copy .env", "Add API key",
                                         "AI Studio key", "uv sync"]),
    "RunAg": ("ADK", "Running Agents", ["adk web", "Open UI"]),
    "Base": ("ADK", "1-baseline", ["Pick baseline"]),
    "Mcp": ("ADK", "3-mcp-tools", ["Install Node", "Ask agent"]),
    # the Colab notebooks' own headings
    "CQ-Pre": ("Colab · Cheese Quiz", "Prerequisites", ["Copy notebook", "Add key", "Install",
                                                        "Download"]),
    "CQ-Agent": ("Colab · Cheese Quiz", "LLM to Agent", ["Base LLM", "Reasoning LLM", "Agent"]),
    "CQ-Inputs": ("Colab · Cheese Quiz", "Managing LLM Inputs",
                  ["Basic prompt", "Prompt engineering", "RAG documents", "Short-term memory",
                   "Long-term memory", "Tool outputs", "Structured output"]),
    "CQ-Tools": ("Colab · Cheese Quiz", "Tools, MCP", ["Fun-fact tool", "Remote MCP", "Own MCP"]),
    "CQ-Guild": ("Colab · Cheese Quiz", "Cheese Quiz Guild", ["Guild members", "Orchestrator",
                                                              "Run guild"]),
    "TP": ("Colab", "Travel Planner", ["Copy, add key", "Install", "Define tools", "Turn 1", "Turn 2",
                                       "Turn 3", "Turn 4", "Chat loop"]),
    "NL": ("Colab", "Cheese Newsletter", ["Copy, add key", "Install", "Edit USERS", "Define agents",
                                          "Run demo", "View outputs"]),
}


def _looks_code(s: str) -> bool:
    return " " not in s and bool(re.search(r"[-_.]", s))


def place_tracker(tr):
    tr.shift(np.array([TRACK_LEFT - tr.get_left()[0], TRACK_TOP - tr.get_top()[1], 0]))
    return tr


def tracker(key: str, step: int | None = None):
    """The tracker for `key` (see SECTIONS), top-left: "<source> › <section>", one dot per step,
    "step k of N: <title>" (step None: no step lit yet, an empty caption)."""
    from explainer.devops import ReadmeTracker
    src, section, steps = SECTIONS[key]
    t = ReadmeTracker(section, steps)
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
    """Transform: the tracker caption with (or without) ' · extra' while a command the README
    doesn't have is on screen."""
    k = tr.k
    s = f"step {k} of {len(tr.steps)}: {tr.steps[k - 1]}" if k else ""
    if on:
        new = label((s + " · extra") if s else "extra", tr.size, tr.hi_color,
                    t2c={"· extra": S.GREY, "extra": S.GREY} if not s else {"· extra": S.GREY})
    else:
        new = label(s or " ", tr.size, tr.hi_color)
    new.next_to(tr.dots, RIGHT, buff=0.25)
    return Transform(tr.caption, new)


def switch_section(scene, old, key: str, step: int | None = 1, run_time: float = 0.8):
    """The tracker switches to another section: the old one lifts away, the new one drops in.
    Returns the new tracker (on screen). old may be None."""
    new = tracker(key, step)
    if old is None:
        scene.play(FadeIn(new, shift=DOWN * 0.25), run_time=run_time)
    else:
        scene.play(FadeOut(old, shift=UP * 0.25), FadeIn(new, shift=DOWN * 0.25), run_time=run_time)
    return new


def lref(slides: str) -> VGroup:
    """The GREY 'Lecture 6 · slides 20–22' tag, top right."""
    return lecture_ref(6, slides)


def lref_swap(scene, old, slides: str, run_time: float = 0.5) -> VGroup:
    """Replace the lecture tag (old may be None). Returns the new tag (on screen)."""
    new = lref(slides)
    if old is None:
        scene.play(FadeIn(new), run_time=run_time)
    else:
        scene.play(FadeOut(old), FadeIn(new), run_time=run_time)
    return new


# ------------------------------------------------------------------ captures and sources
FOLDERS = ("laptop", "cli-container", "adk-laptop", "mcp-remote", "expected")
NEVER_FILES = {"laptop/04-x-git-log.txt",                       # a GitHub user name
               "adk-laptop/11-x-capture-only-uv-config.txt"}    # capture plumbing
NEVER_CAPTURE = {   # file lines the script never shows
    "laptop/09-x-book-changed.txt": {2, 7},           # the commit subject (2: only cut), the author line
    "cli-container/34-x-authors.txt": set(range(16, 26)),
    "adk-laptop/12-uv-sync.txt": {5, 6, 7, 140},      # the capture-only CPU index's numbers
}
CUT_OK = {("laptop/09-x-book-changed.txt", 2): "2026-09-22"}


class Capture:
    """One captured command. .cmd (as typed, without "$ "), .lines (its output, name masked),
    .exit (status), .first (file line number of .lines[0]), .header (the '#' line of expected/*)."""

    def __init__(self, name: str, cmd: str, lines: list[str], exit_code: int, first: int = 2,
                 header: str = ""):
        self.name, self.cmd, self.lines, self.exit = name, cmd, lines, exit_code
        self.first, self.header = first, header

    def _guard(self, n: int):
        if n in NEVER_CAPTURE.get(self.name, ()):
            raise ValueError(f"{self.name}: line {n} is never shown (script.md 'Names on screen')")

    def _raw(self, n: int) -> str:
        i = n - self.first
        if not 0 <= i < len(self.lines):
            raise IndexError(f"{self.name}: line {n} is not output (output is lines "
                             f"{self.first}–{self.first + len(self.lines) - 1})")
        return self.lines[i]

    def line(self, n: int, strip_emoji: bool = False) -> str:
        """File line n (1-based, as in the script's TERM(file: n))."""
        self._guard(n)
        return _emoji_guard(self._raw(n), f"{self.name} line {n}", strip_emoji)

    def cut(self, n: int, marker: str, strip_emoji: bool = False) -> str:
        """File line n up to and including the first `marker` (script: "6 cut after 'x'")."""
        ok = CUT_OK.get((self.name, n))
        if ok is None:
            self._guard(n)
        elif ok != marker:
            raise ValueError(f"{self.name}: line {n} may only be cut after {ok!r}")
        s = self._raw(n)
        i = s.find(marker)
        if i < 0:
            raise ValueError(f"{marker!r} not in {self.name} line {n}")
        return _emoji_guard(s[:i + len(marker)], f"{self.name} line {n}", strip_emoji)

    def at(self, *spec, ellipsis: str = "…", strip_emoji: bool = False) -> list[str]:
        """Output lines by FILE line number: at(2, (11, 12), "…", 52) -> line 2, lines 11-12, a
        '…' line, line 52. A string is inserted as is ("" means the ellipsis)."""
        out: list[str] = []
        for s in spec:
            if isinstance(s, str):
                out.append(s or ellipsis)
            elif isinstance(s, int):
                out.append(self.line(s, strip_emoji))
            else:
                a, b = s
                out += [self.line(n, strip_emoji) for n in range(a, b + 1)]
        return out

    def join(self, *ns: int, width: int | None = 80) -> str:
        """File lines joined into one (one output line the capture shows over several rows, e.g.
        join(7, 8, 9)); print it with wrap=True. A row the terminal wrapped at `width` columns is
        padded back to `width` first (the capture dropped the spaces at the end of a wrapped row:
        laptop/06 line 7 is 79 characters, "…does not exist" + " " + "or may require…"); a row
        whose successor starts with spaces was wrapped by the program itself with a hanging indent
        (uv's error, adk-laptop/07 lines 5-7): they join with one space. width=None: plain
        concatenation."""
        rows = [self.line(n) for n in ns]
        if not width:
            return "".join(rows)
        out = rows[0]
        for nxt in rows[1:]:
            if nxt.startswith(" "):
                out = out.rstrip() + " " + nxt.lstrip()
            else:
                tail = len(out) - out.rfind("\n") - 1 if "\n" in out else len(out)
                out = out + " " * max(0, (width - tail % width) % width if tail % width else 0) + nxt
        return out

    def fold(self, a: int, b: int, text: str) -> str:
        """The script's "a–b folded to X": X stands for lines a..b and is made of their own text,
        with '…' for what it leaves out. Checks every piece between the '…'s against the lines
        (joined with spaces, whitespace normalised), in order, and returns X."""
        norm = lambda s: re.sub(r"\s+", " ", s).strip()     # noqa: E731
        whole = norm(" ".join(self.line(n) for n in range(a, b + 1)))
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
        line - 1 for a normal capture). Prefer .at(), which takes file line numbers."""
        n = len(self.lines)
        out: list[str] = []
        last = None
        for r in ranges:
            a, b = (r, r) if isinstance(r, int) else r
            a = a if a > 0 else n + a + 1
            b = b if b > 0 else n + b + 1
            if last is not None and a > last + 1:
                out.append(ellipsis)
            out += [self.line(k - 1 + self.first) for k in range(a, b + 1)]
            last = b
        return out


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


def capture(name: str, folder: str | None = None) -> Capture:
    """assets/terminal/<folder>/<name>.txt parsed, the instructor's name masked;
    capture("07", "adk-laptop") finds 07-uv-sync.txt; capture("adk-laptop/07") works too. Fails
    loudly if missing: never show an output that wasn't captured."""
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
        raise ValueError(f"{key} is never shown (script.md 'Never shown')")
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
    return Capture(key, cmd, raw, code, off, header)


_PROMPT = re.compile(r"^((?:\(\w+\) )?[\w.-]+@[\w.-]+:[^\s$#]*[$#])(?: (.*))?$")


def split_prompt(line: str):
    """'app@abcf218747d0:/app$ exit' -> ('app@abcf218747d0:/app$', 'exit'); not a prompt -> None."""
    m = _PROMPT.match(line.rstrip())
    if not m:
        return None
    return m.group(1), (m.group(2) or "").strip()


def apps(line: str) -> list[str]:
    """A captured JSON list (adk-laptop/17, 25, 30 line 2) -> its entries."""
    return list(json.loads(line))


NOTEBOOKS = {"cheese-quiz": "Cheese Quiz", "travel-planner": "Travel Planner",
             "cheese-newsletter": "Cheese Newsletter"}
NEVER_SOURCE = {"llm-rag/input-datasets/books/Tolminc Cheese.txt": {1},
                "llm-rag-tolminc-before-85bba32/input-datasets/books/Tolminc Cheese.txt": {1}}


def src_path(name: str) -> str:
    """Resolve a source name: as given under assets/source, else under llm-rag/, else under
    llm-agent-google-adk/. Raises for files never shown (cell-00, the unredacted USERS cell)."""
    for cand in (name, f"llm-rag/{name}", f"llm-agent-google-adk/{name}"):
        if (SOURCE / cand).is_file():
            break
    else:
        raise FileNotFoundError(f"assets/source/{name} not found (also tried llm-rag/, llm-agent-google-adk/)")
    if re.search(r"colab/[^/]+/cell-00\.", cand):
        raise ValueError(f"{cand}: a notebook's cell 00 (the course header) is never shown")
    if cand.startswith("colab/cheese-newsletter/cell-16.") and "redacted" not in cand:
        raise ValueError("the USERS cell is shown only as cell-16.redacted.py")
    return cand


def source_text(name: str) -> str:
    """A tutorial file, the instructor's name masked."""
    return unname((SOURCE / src_path(name)).read_text(encoding="utf-8"))


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
        raise ValueError(f"{path}: lines {sorted(bad)} are never shown (script.md 'Names on screen')")
    out = {}
    for n in nums:
        if not 1 <= n <= len(lines):
            raise IndexError(f"{path} has {len(lines)} lines (asked for {n})")
        out[n] = _emoji_guard(lines[n - 1].expandtabs(4), f"{path} line {n}", strip_emoji_)
    return out


def excerpt(name: str, first: int, last: int, cut_comments: bool = False,
            strip_emoji: bool = False) -> str:
    """Lines first..last (1-based, inclusive) of a tutorial file in assets/source (name masked).
    Never-shown lines raise."""
    d = _source_lines(name, range(first, last + 1), strip_emoji)
    out = [d[n] for n in range(first, last + 1)]
    if cut_comments:
        out = [cut_comment(s) for s in out]
    return "\n".join(out)


def _quoted(line: str) -> str:
    m = re.search(r'"([^"]+)"', line)
    return m.group(1) if m else line.strip()


QUESTION = _quoted(excerpt("cli.py", 435, 435))                       # masked: ‹instructor›'s book
CQ_QUESTION = _quoted(excerpt("colab/cheese-quiz/cell-37.py", 2, 2))
ENUM_AUTHORS = [_quoted(s) for s in excerpt("agent_tools.py", 20, 28).split("\n")]


def _books() -> list[str]:
    c = capture("20", "cli-container")
    out = []
    for n in range(c.first, c.first + len(c.lines)):
        m = re.search(r"embeddings-char-split-(.*)\.jsonl", c._raw(n))
        if m and m.group(1) not in out:
            out.append(m.group(1))
    return out


BOOKS = _books()


def _budget():
    c = capture("expected/colab-travel-planner-c27-turn4-yes.txt")
    lines = c.lines
    i = next(k for k, s in enumerate(lines) if '"costs_usd"' in s)
    items = []
    for s in lines[i + 1:]:
        m = re.match(r'\s*"(\w+)":\s*([\d.]+),?$', s)
        if not m:
            break
        items.append((m.group(1), int(float(m.group(2)))))
    total = int(float(re.search(r'"total_usd":\s*([\d.]+)', "\n".join(lines)).group(1)))
    cap = int(float(re.search(r'"budget_usd":\s*([\d.]+)', "\n".join(lines)).group(1)))
    return tuple(items), total, cap


BUDGET, BUDGET_TOTAL, BUDGET_CAP = _budget()


def _mcp_tools() -> list[str]:
    s = capture("35", "adk-laptop").line(31)
    return list(ast.literal_eval(s[s.index("["):]))


MCP_TOOLS = _mcp_tools()


def your_copy(path: str) -> str:
    """'1-baseline/agent.py' -> 'your copy: baseline/agent.py' (after S10's rename)."""
    p = path.replace("llm-agent-google-adk/", "")
    head, _, rest = p.partition("/")
    return f"your copy: {RENAMES.get(head, head)}/{rest}" if rest else f"your copy: {RENAMES.get(head, head)}"


# ------------------------------------------------------------------ small text helpers
def sans(s: str, size: float = CAPTION, color: str = INK, **kw) -> Text:
    """CMU Sans Serif text (box labels, card lines)."""
    return label(s, size, color, font=SANS, **kw)


def note(s: str, color: str = S.GREY, size: float = CAPTION) -> Text:
    """A GREY caption (serif, 20 pt)."""
    return label(s, size, color)


def mtext(s: str, size: float = CAPTION, color: str = INK, font: str = MONO) -> Text:
    """Text through unname(), the mask drawn GREY (mono by default; font=SANS or S.FONT)."""
    s = unname(s)
    t2c = {MASK: S.GREY} if MASK in s else {}
    return S.text(s, size, color, font=font, t2c=t2c)


def grey_masks(line, ellipses: bool = True, color: str = S.GREY):
    """Colour every MASK (and every '…', the sign of something left out) in a mono_line GREY; a
    folded command (a VGroup with .rows) is handled row by row. Returns line."""
    rows = line.rows if hasattr(line, "rows") else [line]
    for r in rows:
        s = getattr(r, "text", None)
        if not s or not hasattr(r, "glyphs"):
            continue
        for sub in ([MASK, "…"] if ellipses else [MASK]):
            i = s.find(sub)
            while i >= 0:
                glyph_range(r, i, i + len(sub)).set_color(color)
                i = s.find(sub, i + len(sub))
    return line


def _keep(m):
    """Mark a group (chip, tag, labelled glyph) to keep its size in Piece.rescale()."""
    m.keep_size = True
    return m


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
class _L6Terminal(Terminal):
    """The house Terminal; every line it places has MASK and '…' drawn GREY."""

    def _place(self, line, i):
        super()._place(line, i)
        grey_masks(line)
        return line


def term(prompt: str = P_REPO, rows: int = 12, title: str | None = None, container: bool = False,
         top: float | None = None, width: float = TERM_W, size: float = TERM_PT) -> Terminal:
    """The house terminal (full width, 22 pt, 65 characters a row), bottom edge at BOTTOM, or its
    top edge at `top`. container=True: inside the CLI container (TEAL frame, title CTR_TITLE,
    prompt P_CTR unless `prompt` is given)."""
    if container and prompt == P_REPO:
        prompt = P_CTR
    ttl = title or (CTR_TITLE if container else "laptop")
    t = _L6Terminal(prompt=prompt, width=width, rows=rows, size=size, title=ttl)
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


def enter_container(t: Terminal, prompt: str = P_CTR, title: str = CTR_TITLE) -> list:
    """Animations: the frame turns TEAL, the title becomes "container · llm-rag-cli"; the prompt
    becomes `prompt` for the next typed line."""
    t.set_prompt(prompt)
    new = mono(title, CAPTION, CTR).move_to(t.title)
    return [t.box.animate.set_stroke(CTR, 3), Transform(t.title, new)]


def leave_container(t: Terminal, prompt: str = P_REPO, title: str = "laptop") -> list:
    """Animations: back on the laptop (GREY frame, title `title`, prompt `prompt`)."""
    t.set_prompt(prompt)
    new = mono(title, CAPTION, S.GREY).move_to(t.title)
    return [t.box.animate.set_stroke(S.GREY_DARK, 2), Transform(t.title, new)]


def retitle(t: Terminal, title: str, color: str = S.GREY) -> Transform:
    """Animation: the terminal's title text changes."""
    return Transform(t.title, mono(title, CAPTION, color).move_to(t.title))


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
            colors: dict | None = None, out_time: float = 0.5):
    """Replay an interactive capture (laptop/06): `spec` as in Capture.at. A line that starts with
    a prompt sets t's prompt and types its command (exactly as captured); a prompt line with no
    command makes a bare prompt; other lines print. colors: {file line: colour}. Returns
    {file line: the mobject printed or typed for it}."""
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
        if sp:
            flush()
            t.set_prompt(sp[0])
            out[n] = type_cmd(scene, t, sp[1], type_time) if sp[1] else bare_prompt(scene, t)
        else:
            col = (colors or {}).get(n, OUTPUT)
            pending.append((text, col))
            pend_nums.append(n)
    flush()
    return out


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
    """The GREY tag holding a BuildKit row's time (see build_row)."""
    return _keep(tag(time, S.GREY))


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
    return grey_tag("illustration" + (f" · {note_}" if note_ else ""))


def recording_tag() -> VGroup:
    return grey_tag("at the time of recording")


def recorded_tag(s: str = "recorded") -> VGroup:
    return grey_tag(s)


def staff_run_tag(old_book: bool = False) -> VGroup:
    """The staff's --agent run (out.txt); old_book=True from S07 on."""
    return grey_tag("recorded · the staff's run, September 22, 2026" + (" · old book" if old_book else ""))


def saved_run_tag() -> VGroup:
    """A notebook's saved output."""
    return grey_tag("recorded · the staff's last saved run")


def expected_tag() -> VGroup:
    return grey_tag("expected")


def standin_tag(s: str = "stand-in") -> VGroup:
    """PINK: cli-container/33's stored chunk vector standing in for Google's embedding."""
    return _keep(tag(s, LOOKUP))


def nokey_tag() -> VGroup:
    return grey_tag("real run · no key")


def placeholder_tag() -> VGroup:
    return grey_tag("real run · placeholder key")


def notsent_tag() -> VGroup:
    return grey_tag("built, not sent")


def erratum_tag(note_: str | None = None) -> VGroup:
    return grey_tag("erratum" + (f" · {note_}" if note_ else ""))


def fix_tag() -> VGroup:
    return grey_tag("fix · not in the README")


def differ_tag() -> VGroup:
    return grey_tag("your numbers will differ")


def harmless_tag() -> VGroup:
    return grey_tag("harmless")


def preview_tag() -> VGroup:
    return grey_tag("preview")


def concept_tag(s: str = "concept · lecture only") -> VGroup:
    """The GREY dashed tag of a lecture idea with no code here."""
    g = tag(s, S.GREY)
    dashed = DashedVMobject(g.box, num_dashes=int(g.box.width * 9), dashed_ratio=0.55)
    dashed.set_stroke(S.GREY, 2)
    fill = g.box.copy().set_stroke(width=0)
    out = VGroup(fill, dashed, g.text)
    out.box, out.text = fill, g.text
    return _keep(out)


def cost_tag(s: str = "paid · per call") -> VGroup:
    return _keep(tag(s, COST))


def stamp(text: str, color: str = ERR, size: float = TAG, angle: float = 0.08) -> VGroup:
    """An outlined, slightly rotated stamp (PENDING, APPROVED …). .frame .text"""
    t = sans(text, size, color, weight="BOLD")
    r = RoundedRectangle(width=t.width + 0.3, height=t.height + 0.22, corner_radius=0.06,
                         stroke_color=color, stroke_width=3).set_fill(S.BG, 0.85)
    t.move_to(r)
    g = VGroup(r, t).rotate(angle)
    g.frame, g.text = r, t
    return _keep(g)


def fix_chip(text: str, color: str = VENV, font: str | None = None) -> VGroup:
    """A GREEN "the fix" chip (serif text; font=MONO for code)."""
    return _keep(chip(text, color, size=CAPTION, font=font))


def concept_box(text: str, size: float = CAPTION, color: str = S.GREY, min_w: float = 0.0,
                text_color: str = INK) -> VGroup:
    """A GREY dashed box holding a lecture concept (pre-retrieval, Self-RAG, handoffs …). .box .text"""
    t = label(text, size, text_color)
    h = mono("|", size).height + 0.26
    b = box(max(min_w, t.width + 0.5), h, color, dashed=True, radius=h / 2.6)
    bg = RoundedRectangle(width=b.width, height=h, corner_radius=h / 2.6, stroke_width=0).set_fill(S.BG, 0.9)
    t.move_to(b)
    g = VGroup(bg, b, t)
    g.box, g.text = b, t
    return _keep(g)


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
    """The path as the viewer sees it: llm-rag/cli.py -> "cli.py"; llm-agent-google-adk/1-baseline/
    agent.py -> "1-baseline/agent.py"; colab/cheese-quiz/cell-12.py -> "Cheese Quiz · cell 12"."""
    p = src_path(name)
    m = re.match(r"colab/([^/]+)/cell-(\d+)", p)
    if m:
        return f"{NOTEBOOKS[m.group(1)]} · cell {int(m.group(2))}"
    for pre in ("llm-rag/", "llm-agent-google-adk/"):
        if p.startswith(pre):
            return p[len(pre):]
    if p.startswith("llm-rag-tolminc-before-85bba32/"):
        return f"96d5fd7 · {Path(p).name}"
    return p


def _looks_path(p: str) -> bool:
    return bool(re.search(r"\.[A-Za-z]\w*$", p)) or ("/" in p and " " not in p)


def _header_text(text: str, size: float = CAPTION) -> VGroup:
    """'cli.py · lines 183–194' -> mono path + serif rest; 'Cheese Quiz · cell 12 · lines 3–4' all
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
    for k in range(len(code_rows)):                 # GREY ↪ marks, '…' gap rows and the mask
        for sub in ("↪", "…", MASK):
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
    p.bar = lambda n, color=TURN, opacity=0.18: VGroup(*[line_bar(p.code, k, color, opacity)
                                                         for k in rows_of[n]])

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
        s = unname(s)
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
    header above. Rows longer than the panel are cut with '…'; MASK and '…' GREY. .rows .frame
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


def excerpt_chip(sub: str, header: str, color: str = INK, frame: str = S.GREY,
                 line: str | None = None, size: float = CAPTION) -> VGroup:
    """An excerpt chip: a mono chip holding the exact sub-string `sub` of one source or capture
    line, headed `header` ("cli.py · line 459 (excerpt)"). Pass the full `line` (excerpt(...) or
    cap.line(n)) to check the sub-string. .chip .text .header"""
    sub = unname(sub)
    if line is not None and sub not in unname(line):
        raise ValueError(f"{sub!r} is not in {line!r}")
    c = chip(sub, frame, size=size, text_color=color, font=MONO, fill_opacity=0.1)
    if MASK in sub:
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


def turn_card(rows, width: float | None = None, header: str | None = "your turn",
              size: float = CAPTION) -> VGroup:
    """The static GREY "your turn" card (a ▶ that stays readable when paused). rows: a str is a
    command typed exactly as on screen (mono; "\\n" splits it into rows), (cmd, "extra") adds the
    extra tag, (cmd, note) a GREY note, Prose("…") a serif row, (Prose("…"), colour) a coloured
    serif row (the GOLD cost line last). The YELLOW ▶ your turn tag sits on the top-right corner
    (.tag). .frame .rows .tag"""
    items = VGroup()
    for r in rows:
        if isinstance(r, Prose):
            items.add(label(str(r), size, INK))
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
        steps = list(range(self.n + 1, n + 1)) or [n]
        anims = []
        for k in steps:
            new = self._make(k).move_to(self.text, aligned_edge=LEFT)
            anims.append(Transform(self.text, new, run_time=run_time / len(steps)))
        self.n = n
        return Succession(*anims)

    def with_time(self, text: str):
        t = label(f"· {text}", self.size, self.hi_color).next_to(self.text, RIGHT, buff=0.15)
        self.time = t
        self.add(t)
        return FadeIn(t, shift=LEFT * 0.1)


def colab_frame(title: str, width: float = 12.9, top: float = 2.75, bottom: float = -3.5,
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


def definition_card(size: float = 24, header: str | None = None) -> VGroup:
    """Slide 26's definition in our words, two rows: "an LLM, given instructions and tools," /
    "that runs on its own until the task is done". .until (the last words, to underline) .frame"""
    r1 = label("an LLM, given instructions and tools,", size, INK)
    a = label("that runs on its own", size, INK)
    u = label("until the task is done", size, INK)
    r2 = VGroup(a, u).arrange(RIGHT, buff=0.14, aligned_edge=DOWN)
    rows = VGroup(r1, r2).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    fr = box(rows.width + 0.6, rows.height + 0.5, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.14)
    rows.move_to(fr)
    g = VGroup(fr, rows)
    g.frame, g.rows, g.until = fr, rows, u
    if header:
        h = note(header).next_to(fr, UP, buff=0.08).align_to(fr, LEFT).shift(RIGHT * 0.12)
        g.add(h)
    return g


def pick_card(text: str, header: str = "top pick", size: float = 22, width: float = 4.2) -> VGroup:
    """The BLUE answer card beside V2's envelope (the model wrote it): a GREY header and the pick
    (serif; "`mono`" in backticks). Change it with repick(card, text). .frame .text .header"""
    fr = box(width, 1.05, CLOUD, fill=S.BG, fill_opacity=0.95, radius=0.14)
    h = note(header).move_to(fr.get_top() + DOWN * 0.24)
    t = _cell(text, size).move_to(fr.get_center() + DOWN * 0.14)
    if t.width > width - 0.3:
        raise ValueError(f"pick {text!r} is {t.width:.1f} wide: widen the card (width=)")
    g = VGroup(fr, h, t)
    g.frame, g.header, g.text = fr, h, t
    return g


def repick(card, text: str, size: float = 22):
    """Animation: the pick card's text becomes `text` (card.text is the new text afterwards)."""
    t = _cell(text, size).move_to(card.frame.get_center() + DOWN * 0.14)
    if t.width > card.frame.width - 0.3:
        raise ValueError(f"pick {text!r} is {t.width:.1f} wide: widen the card")
    old, card.text = card.text, t
    return ReplacementTransform(old, t)


class Dropdown(VGroup):
    """A schematic agent dropdown in the ADK dev UI (illustration): a field with `title` and a ▾,
    and the entries (mono, from a capture: apps(cap.line(2))) listed under it.
    .row(name) .pick(name, colour=TURN) -> anim (a bar behind the row, its text coloured)
    .field .rows"""

    def __init__(self, entries, title: str = "Select an agent", size: float = CAPTION,
                 min_w: float = 3.6, **kw):
        super().__init__(**kw)
        rows = VGroup(*[mono(e, size, INK) for e in entries]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        w = max(min_w, rows.width + 0.6)
        head = label(title, size, S.GREY)
        caret = label("▾", size, S.GREY)
        field = RoundedRectangle(width=w, height=head.height + 0.3, corner_radius=0.08,
                                 stroke_color=S.GREY, stroke_width=2).set_fill(TERM_BG, 1)
        head.move_to(field).align_to(field, LEFT).shift(RIGHT * 0.2)
        caret.move_to(field).align_to(field, RIGHT).shift(LEFT * 0.2)
        lst = RoundedRectangle(width=w, height=rows.height + 0.36, corner_radius=0.08,
                               stroke_color=S.GREY_DARK, stroke_width=2).set_fill(PANEL, 1)
        lst.next_to(field, DOWN, buff=0.06)
        rows.move_to(lst).align_to(lst, LEFT).shift(RIGHT * 0.3)
        self.field, self.list_box, self.rows, self.entries = VGroup(field, head, caret), lst, rows, list(entries)
        self.add(self.field, lst, rows)

    def row(self, name: str):
        return self.rows[self.entries.index(name)]

    def pick(self, name: str, color: str = TURN):
        r = self.row(name)
        bar = Rectangle(width=self.list_box.width - 0.16, height=r.height + 0.12, stroke_width=0) \
            .set_fill(color, 0.2).move_to([self.list_box.get_center()[0], r.get_center()[1], 0])
        self.submobjects.insert(self.submobjects.index(self.rows), bar)   # above the list, under the rows
        return AnimationGroup(FadeIn(bar), r.animate.set_color(color))


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
    """A padlock (the collection stays on the laptop). .body .shackle"""
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
    """A person glyph (the human of S14): a head over shoulders."""
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


def cylinder(w: float = 1.1, h: float = 1.3, color: str = CTR, fill: float = 0.18,
             stroke: float = 3) -> VGroup:
    """The vector database: a TEAL cylinder with two disk lines (opaque fill). .top .body .frame"""
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


def chunk_card(w: float = 0.55, h: float = 0.34, color: str = DATA, rows: int = 2,
               fill: float = 0.22) -> VGroup:
    """A GREEN chunk card (no text): a rounded card with `rows` short text marks. .frame"""
    fr = RoundedRectangle(width=w, height=h, corner_radius=min(0.06, h / 3), stroke_color=color,
                          stroke_width=2).set_fill(_mix(color, fill), 1)
    marks = VGroup()
    for i in range(rows):
        y = (i - (rows - 1) / 2) * h / (rows + 1) * 1.2
        ln = Line(LEFT * w * 0.32, RIGHT * w * (0.32 if i < rows - 1 else 0.1), color=color,
                  stroke_width=2, stroke_opacity=0.8)
        ln.move_to(fr.get_center() + UP * -y).align_to(fr, LEFT).shift(RIGHT * w * 0.16)
        marks.add(ln)
    g = VGroup(fr, marks)
    g.frame = fr
    return g


def vec_glyph(n: int = 3, color: str = DATA, size: float = 0.55, spread: float = 28.0,
              base: float = 20.0, stroke: float = 4) -> VGroup:
    """A small fan of n arrows from one point (vectors; n=1 for the query vector)."""
    arrows = VGroup()
    for k in range(n):
        deg = base + (k - (n - 1) / 2) * spread / max(1, n - 1) * (1 if n > 1 else 0)
        d = np.array([np.cos(np.radians(deg)), np.sin(np.radians(deg)), 0])
        arrows.add(Arrow(ORIGIN, d * size, buff=0, color=color, stroke_width=stroke,
                         max_tip_length_to_length_ratio=0.35, tip_length=0.14))
    return arrows.move_to(ORIGIN)


def model_box(name: str = "Gemini", w: float = 1.3, h: float = 0.9, color: str = CLOUD,
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


def model_chip(name: str = MODEL_CQ, size: float = CAPTION) -> VGroup:
    """A BLUE mono chip naming a model (gpt-4o, gemini-3.1-flash-lite …)."""
    return _keep(chip(name, CLOUD, size=size, font=MONO))


def question_card(text: str = QUESTION, color: str = LOOKUP, font: str | None = MONO,
                  size: float = CAPTION) -> VGroup:
    """The PINK question card (masked). .box .text"""
    c = chip(unname(text), color, size=size, font=font, fill_opacity=0.12)
    if MASK in unname(text):
        new = mtext(text, size, INK, font=font or S.FONT).move_to(c.text)
        c.remove(c.text)
        c.add(new)
        c.text = new
    return _keep(c)


def menu_card(sig: str, color: str = DATA, size: float = CAPTION) -> VGroup:
    """A GREEN menu card: one function declaration as its signature, mono
    (`get_book_by_author(author, search_content)`). .box .text"""
    return _keep(chip(sig, color, size=size, font=MONO, fill_opacity=0.14))


def answer_bars(n: int = 3, w: float = 2.4, color: str = S.GREY, h: float = 0.12) -> VGroup:
    """Placeholder answer bars (no words): n rounded bars, the last one shorter."""
    bars = VGroup(*[RoundedRectangle(width=w * (0.55 if k == n - 1 else (1.0 - 0.08 * (k % 2))), height=h,
                                     corner_radius=h / 2, stroke_width=0).set_fill(color, 0.75)
                    for k in range(n)])
    bars.arrange(DOWN, aligned_edge=LEFT, buff=h * 1.1)
    return bars


def seal(r: float = 0.16, color: str = CLOUD) -> VGroup:
    """A small wax seal (the model's thought signature): a scalloped disc with a ring."""
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


def calculator_glyph(h: float = 0.8, color: str = DATA) -> VGroup:
    """A calculator (Python does the arithmetic): body, display, 3 x 4 keys."""
    w = h * 0.72
    body = RoundedRectangle(width=w, height=h, corner_radius=0.06, stroke_color=color,
                            stroke_width=2.5).set_fill(color, 0.12)
    disp = Rectangle(width=w * 0.76, height=h * 0.2, stroke_color=color, stroke_width=1.5) \
        .set_fill(color, 0.35).move_to(body.get_top() + DOWN * h * 0.2)
    keys = VGroup(*[RoundedRectangle(width=w * 0.18, height=h * 0.1, corner_radius=0.02, stroke_width=0)
                    .set_fill(color, 0.7) for _ in range(12)])
    keys.arrange_in_grid(4, 3, buff=(w * 0.07, h * 0.06)).next_to(disp, DOWN, buff=h * 0.08)
    return _keep(VGroup(body, disp, keys))


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
    """The GREEN receipt (S15): a slip with a zig-zag bottom edge and the file path (mono, masked).
    .frame .text"""
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


def wheel_glyph(r: float = 0.22, color: str = S.GREY) -> VGroup:
    """A Python wheel (a built package for one Python version): a rim with six spokes."""
    rim = Circle(radius=r, stroke_color=color, stroke_width=3).set_fill(color, 0.12)
    hub = Dot(radius=r * 0.18, color=color)
    spokes = VGroup(*[Line(ORIGIN, UP * r * 0.92, color=color, stroke_width=2)
                      .rotate(k * TAU / 6, about_point=ORIGIN) for k in range(6)])
    return VGroup(rim, spokes, hub)


def cost_tick(r: float = 0.1, color: str = COST) -> VGroup:
    """A GOLD tick per paid call: a small coin."""
    c = Circle(radius=r, stroke_color=color, stroke_width=2.5).set_fill(color, 0.45)
    inner = Circle(radius=r * 0.55, stroke_color=color, stroke_width=1.5)
    return _keep(VGroup(c, inner))


def mini_envelope(text: str | None = None, color: str = LOOKUP, w: float = 0.5,
                  size: float = CAPTION) -> VGroup:
    """A small envelope (an MCP request: initialize, tools/list, tools/call), mono label under it.
    .shape .caption"""
    h = w * 0.66
    body = Rectangle(width=w, height=h, stroke_color=color, stroke_width=2.5).set_fill(S.BG, 1)
    flap = VMobject(stroke_color=color, stroke_width=2.5).set_points_as_corners(
        [[-w / 2, h / 2, 0], [0, 0, 0], [w / 2, h / 2, 0]])
    shape = VGroup(body, flap)
    g = VGroup(shape)
    g.shape, g.caption = shape, None
    if text:
        c = mono(text, size, color).next_to(shape, DOWN, buff=0.08)
        g.add(c)
        g.caption = c
    return _keep(g)


def json_card(lines, color: str = DATA, size: float = CAPTION, header: str | None = None) -> VGroup:
    """A card of mono rows (masked) in `color` (the GREEN plan card, a BLUE call): .frame .rows
    .header"""
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


def call_card(rows=("{name: get_book_by_author,", " args: {author,", "        search_content}}"),
              color: str = CLOUD, size: float = CAPTION, with_seal: bool = True) -> VGroup:
    """V3's BLUE function-call card (the model wrote it), with the small BLUE seal (its thought
    signature) on the top-right corner. .frame .rows .seal"""
    g = json_card(list(rows), color, size)
    g.seal = None
    if with_seal:
        s = seal(0.17, color).move_to(g.frame.get_corner(UP + RIGHT) + np.array([-0.05, -0.05, 0]))
        g.add(s)
        g.seal = s
    return g


def response_card(text: str = '{"content": …}', note_: str | None = None, color: str = CTR,
                  size: float = CAPTION) -> VGroup:
    """The TEAL function-response card llm-rag's code builds (optionally a GREY note row such as
    "3,509 characters"). .frame .rows .note"""
    lines = [text] + ([(note_, S.GREY)] if note_ else [])
    g = json_card(lines, color, size)
    g.note = g.rows[1] if note_ else None
    return g


def staple(card, onto, buff: float = 0.06):
    """Animation: `card` moves under `onto`, left edges aligned (V3's response stapled to the
    call)."""
    target = card.copy().next_to(onto, DOWN, buff=buff).align_to(onto, LEFT)
    return card.animate.move_to(target.get_center())


def one_lap_row(size: float = CAPTION) -> VGroup:
    """S08: llm-rag's run as one short line: BLUE "call 1 · forced tool call" -> TEAL "your code
    runs it" -> BLUE "call 2 · answer" -> GREY "end". .steps (the four chips) .arrows"""
    specs = [("call 1 · forced tool call", CLOUD), ("your code runs it", CTR), ("call 2 · answer", CLOUD),
             ("end", S.GREY)]
    steps = [chip(t, c, size=size) for t, c in specs]
    row = []
    arrows = []
    for k, c in enumerate(steps):
        if k:
            a = Arrow(LEFT * 0.25, RIGHT * 0.25, buff=0, color=S.GREY, stroke_width=3,
                      max_tip_length_to_length_ratio=0.4)
            arrows.append(a)
            row.append(a)
        row.append(c)
    g = VGroup(*row).arrange(RIGHT, buff=0.12)
    g.steps, g.arrows = steps, arrows
    return g


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


# ------------------------------------------------------------------ V1 · the anatomy (slide 27)
class Anatomy(Piece):
    """V1: slide 27's agent redrawn in the series colours. Task / Goal -> the agent box (top row:
    LLM core BLUE, Instructions; a wide Dynamic Control bar, dashed until a framework fills it;
    bottom row: Tools, Memory) -> Task completion. See the module notes."""

    BLOCKS = ("core", "instructions", "control", "tools", "memory")
    NAMES = {"core": "LLM core", "instructions": "Instructions", "control": "Dynamic Control",
             "tools": "Tools", "memory": "Memory"}
    PARTS = ("task", "a_in", "box", "head", "core", "instructions", "control", "tools", "memory",
             "a_out", "done")

    def __init__(self, box_w: float = 7.2, block_h: float = 1.0, bar_h: float = 0.72,
                 ends: bool = True, size: float = 24, head: str = "Agent", show=None, **kw):
        super().__init__(**kw)
        shown = self._show_set(show, self.PARTS)
        gap, head_h = 0.22, 0.5
        bw = (box_w - 3 * gap) / 2
        H = head_h + 2 * block_h + bar_h + 4 * gap
        self.box_w, self.box_h, self.block_w, self.block_h, self.size = box_w, H, bw, block_h, size
        self.bar_h = bar_h
        top = H / 2
        y_top = top - head_h - block_h / 2
        y_bar = y_top - block_h / 2 - gap - bar_h / 2
        y_bot = y_bar - bar_h / 2 - gap - block_h / 2
        xl, xr = -(gap + bw) / 2, (gap + bw) / 2
        frame = RoundedRectangle(width=box_w, height=H, corner_radius=0.25, stroke_color=S.GREY,
                                 stroke_width=3).set_fill(S.BG, 1)
        self.part("box", frame, "box" in shown)
        hd = sans(head, size, INK).move_to([0, top - head_h / 2 - 0.02, 0])
        self.part("head", hd, "head" in shown)
        self.frames, self.names, self.base = {}, {}, {}
        specs = {"core": (xl, y_top, bw, block_h, CLOUD), "instructions": (xr, y_top, bw, block_h, S.GREY),
                 "control": (0.0, y_bar, box_w - 2 * gap, bar_h, S.GREY),
                 "tools": (xl, y_bot, bw, block_h, S.GREY), "memory": (xr, y_bot, bw, block_h, S.GREY)}
        for name, (x, y, w, h, col) in specs.items():
            nm = sans(self.NAMES[name], size, INK)
            if block_h >= 1.4 and name != "control":
                nm.move_to([x, y + h / 2 - 0.12 - nm.height / 2, 0])
            else:
                nm.move_to([x, y, 0])
            if nm.width > w - 0.2:
                raise ValueError(f"Anatomy: {self.NAMES[name]!r} does not fit a {w:.2f}-wide block "
                                 f"(box_w={box_w}, size={size})")
            if name == "control":
                dash = box(w, h, col, dashed=True, stroke=3).move_to([x, y, 0])
                fill = box(w, h, TOOL, fill_opacity=0.18, stroke=3).move_to([x, y, 0])
                blk = VGroup()
                self.part("control_dash", dash, True, into=blk)
                self.part("control_fill", fill, False, into=blk)
                blk.add(nm)
                fr = dash
            else:
                fr = box(w, h, col, fill_opacity=0.15 if name == "core" else 0.05, stroke=3).move_to([x, y, 0])
                blk = VGroup(fr, nm)
            self.frames[name], self.names[name], self.base[name] = fr, nm, col
            self.part(name, blk, name in shown)
        self.lit = None
        self.control_filled = False
        if ends:
            task = _keep(chip("Task / Goal", S.GREY, size=CAPTION))
            task.next_to(frame, LEFT, buff=0.42)
            dn = concept_box("Task completion", CAPTION)
            dn.next_to(frame, RIGHT, buff=0.42)
            self.part("task", task, "task" in shown)
            self.part("a_in", _arrow(task.get_right(), frame.get_left()), "a_in" in shown)
            self.part("a_out", _arrow(frame.get_right(), dn.get_left()), "a_out" in shown)
            self.part("done", dn, "done" in shown)
        self.move_to(ORIGIN)

    def block(self, name: str):
        return self.parts[name]

    def _strokes(self, name):
        if name == "control":
            return [self.parts["control_fill"] if self.control_filled else self.parts["control_dash"]]
        return [self.frames[name]]

    def _base_col(self, name):
        return TOOL if (name == "control" and self.control_filled) else self.base[name]

    def light(self, name: str, color: str = TURN):
        """Animation: block `name` lights (border and name in `color`); the previous one unlights."""
        anims = []
        if self.lit and self.lit != name:
            anims += self._unlight_anims(self.lit)
        anims += _restroke(self._strokes(name), color, 4)
        anims.append(self.names[name].animate.set_color(color))
        self.lit = name
        return AnimationGroup(*anims)

    def _unlight_anims(self, name):
        return _restroke(self._strokes(name), self._base_col(name), 3) + \
            [self.names[name].animate.set_color(INK)]

    def unlight(self):
        if not self.lit:
            return AnimationGroup()
        anims = self._unlight_anims(self.lit)
        self.lit = None
        return AnimationGroup(*anims)

    def fill_control(self, color: str = TOOL) -> list:
        """Animations: the dashed Dynamic Control bar becomes a solid PURPLE block (the framework
        writes this part)."""
        fill, dash = self.parts["control_fill"], self.parts["control_dash"]
        anims = [dash.animate.set_stroke(opacity=0),
                 fill.animate.set_stroke(color, 3, opacity=1).set_fill(color, 0.18)]
        fill.hidden, dash.hidden = False, True
        if self.lit == "control":
            self.lit = None
        anims.append(self.names["control"].animate.set_color(INK))
        self.control_filled = True
        return anims

    def _item_chip(self, it, size):
        if not isinstance(it, str):
            return it
        if len(it) > 1 and it.startswith("`") and it.endswith("`"):
            return _keep(chip(it[1:-1], S.GREY, size=size, font=MONO))
        return _keep(chip(it, S.GREY, size=size))

    def fill(self, name: str, items, size: float = CAPTION, buff: float = 0.1):
        """(chips, anims): the items (a "`mono`" str, a serif str, or a mobject) laid out in rows
        under the block's name (which moves to the block's top). Raises if they don't fit: build
        the Anatomy with a larger block_h / box_w. The chips are not members (attach them if the
        piece will move)."""
        fr, nm = self.frames[name], self.names[name]
        chips = [self._item_chip(it, size) for it in items]
        if name == "control":                  # the wide bar: name at the left, one row after it
            target = nm.copy().move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.25)
            row = VGroup(*chips).arrange(RIGHT, buff=buff)
            row.next_to(target, RIGHT, buff=0.35)
            if row.get_right()[0] > fr.get_right()[0] - 0.15 or row.height > fr.height - 0.06:
                raise ValueError(f"Anatomy.fill('control'): the items need a wider box (box_w) "
                                 f"or a taller bar (bar_h >= {row.height + 0.1:.2f})")
            anims = [nm.animate.move_to(target)] + [FadeIn(c, shift=DOWN * 0.08) for c in chips]
            return VGroup(*chips), anims
        avail = fr.width - 0.3
        target = nm.copy().move_to(fr).align_to(fr, UP).shift(DOWN * 0.1)
        rows, cur, cw = [], [], 0.0
        for c in chips:
            if c.width > avail:
                raise ValueError(f"Anatomy.fill({name!r}): an item is {c.width:.2f} wide (> {avail:.2f})")
            if cur and cw + buff + c.width > avail:
                rows.append(cur)
                cur, cw = [], 0.0
            cw += (buff if cur else 0) + c.width
            cur.append(c)
        if cur:
            rows.append(cur)
        y = target.get_bottom()[1] - 0.1
        for r in rows:
            g = VGroup(*r).arrange(RIGHT, buff=buff)
            g.move_to([fr.get_center()[0], y - g.height / 2, 0])
            y -= g.height + 0.08
        if y + 0.08 < fr.get_bottom()[1] + 0.04:
            need = self.block_h + (fr.get_bottom()[1] + 0.04 - (y + 0.08))
            raise ValueError(f"Anatomy.fill({name!r}): {len(chips)} items need block_h >= {need:.2f}")
        anims = []
        if np.linalg.norm(target.get_center() - nm.get_center()) > 0.01:
            anims.append(nm.animate.move_to(target))
        anims += [FadeIn(c, shift=DOWN * 0.08) for c in chips]
        return VGroup(*chips), anims


class AnatomyMini(VGroup):
    """V1's glyph-only copy for the corner (3.2 x 1.6), placed at `center`.
        mm = AnatomyMini(); self.play(FadeIn(mm)); self.play(mm.light("tools"))
    Names as Anatomy.BLOCKS. .light(name) unlights the previous block; .fill_control() -> anim."""

    def __init__(self, center=MINI_CENTER, **kw):
        super().__init__(**kw)
        bg = RoundedRectangle(width=3.2, height=1.6, corner_radius=0.12, stroke_color=S.GREY_DARK,
                              stroke_width=2).set_fill(S.BG, 0.92)
        bx = RoundedRectangle(width=2.3, height=1.32, corner_radius=0.1, stroke_color=S.GREY,
                              stroke_width=2)
        a_in = Line([-1.5, 0, 0], [-1.17, 0, 0], color=S.GREY, stroke_width=2)
        a_out = Line([1.17, 0, 0], [1.5, 0, 0], color=S.GREY, stroke_width=2)
        dot_in = Dot([-1.5, 0, 0], radius=0.05, color=S.GREY)
        dot_out = Dot([1.5, 0, 0], radius=0.05, color=S.GREY)
        gap, bw, bh, barh = 0.09, 1.0, 0.3, 0.2
        y_top, y_bar, y_bot = 0.36, 0.0, -0.36
        xl, xr = -(gap + bw) / 2, (gap + bw) / 2

        def blk(x, y, w, h, col, fill):
            return Rectangle(width=w, height=h, stroke_color=col, stroke_width=2.5).set_fill(col, fill).move_to([x, y, 0])

        self.items = {
            "core": blk(xl, y_top, bw, bh, CLOUD, 0.45),
            "instructions": blk(xr, y_top, bw, bh, S.GREY, 0.1),
            "tools": blk(xl, y_bot, bw, bh, S.GREY, 0.1),
            "memory": blk(xr, y_bot, bw, bh, S.GREY, 0.1),
        }
        solid = blk(0, y_bar, 2.1, barh, TOOL, 0.4)
        solid.set_stroke(opacity=0).set_fill(opacity=0)
        dash = DashedVMobject(Rectangle(width=2.1, height=barh), num_dashes=24).set_stroke(S.GREY, 2.5)
        dash.move_to([0, y_bar, 0])
        self.items["control"] = dash
        self._solid, self._dash = solid, dash
        self._col = {"core": CLOUD, "instructions": S.GREY, "tools": S.GREY, "memory": S.GREY,
                     "control": S.GREY}
        self.frame = bg
        self.add(bg, bx, a_in, a_out, dot_in, dot_out, solid, *self.items.values())
        self.lit = None
        self.filled = False
        self.move_to(center)

    def light(self, name: str, color: str = TURN):
        anims = []
        if self.lit and self.lit != name:
            anims += _restroke([self.items[self.lit]], self._col[self.lit], 2.5)
        anims += _restroke([self.items[name]], color, 4)
        self.lit = name
        return AnimationGroup(*anims)

    def unlight(self):
        if not self.lit:
            return AnimationGroup()
        anims = _restroke([self.items[self.lit]], self._col[self.lit], 2.5)
        self.lit = None
        return AnimationGroup(*anims)

    def fill_control(self, color: str = TOOL):
        """Animation: the dashed bar becomes a solid PURPLE bar."""
        self.filled = True
        self._col["control"] = color
        self.items["control"] = self._solid
        if self.lit == "control":
            self.lit = None
        return AnimationGroup(self._dash.animate.set_stroke(opacity=0),
                              self._solid.animate.set_stroke(color, 2.5, opacity=1).set_fill(color, 0.4))


class CallStrip(VGroup):
    """The one-line GREY call strip under the tracker (end of S04 to S07): "call 1 → your code →
    call 2"; .light(i) lights step i YELLOW (None: all GREY). .steps"""

    STEPS = ("call 1", "your code", "call 2")

    def __init__(self, size: float = CAPTION, top: float = CALL_TOP, left: float = TRACK_LEFT, **kw):
        super().__init__(**kw)
        self.steps = [label(s, size, S.GREY) for s in self.STEPS]
        row = []
        for k, s in enumerate(self.steps):
            if k:
                row.append(label("→", size, S.GREY_DARK))
            row.append(s)
        r = VGroup(*row).arrange(RIGHT, buff=0.18)
        fr = RoundedRectangle(width=r.width + 0.4, height=r.height + 0.22, corner_radius=0.12,
                              stroke_color=S.GREY_DARK, stroke_width=2).set_fill(S.BG, 0.9).move_to(r)
        self.frame = fr
        self.add(fr, r)
        self.shift(np.array([left - fr.get_left()[0], top - fr.get_top()[1], 0]))
        self.lit = None
        _keep(self)

    def light(self, i: int | None):
        anims = [s.animate.set_color(TURN if k == i else S.GREY) for k, s in enumerate(self.steps)]
        self.lit = i
        return AnimationGroup(*anims)


# ------------------------------------------------------------------ V2 · the envelope
class Envelope(Piece):
    """V2: every call is a fresh envelope. The sheets stack as rows inside the body; the closed
    flap's V lives in the top margin and the pocket's V in the bottom margin, so no line crosses a
    sheet. See the module notes."""

    def __init__(self, width: float = 4.6, slots: int = 7, pitch: float = 0.5, color: str = S.GREY,
                 margin: float = 0.42, show=None, **kw):
        super().__init__(**kw)
        shown = self._show_set(show, ("body", "flap", "flap_open", "pocket"))
        self.env_w, self.slots, self.pitch, self.margin = width, slots, pitch, margin
        h = slots * pitch + 2 * margin
        self.env_h = h
        body = RoundedRectangle(width=width, height=h, corner_radius=0.1, stroke_color=color,
                                stroke_width=3).set_fill(_mix(color, 0.08), 1)
        top, bot = h / 2, -h / 2
        flap = VMobject(stroke_color=color, stroke_width=3).set_points_as_corners(
            [[-width / 2, top, 0], [0, top - margin * 0.85, 0], [width / 2, top, 0]])
        flap_open = Polygon([-width / 2, top, 0], [0, top + margin * 1.6, 0], [width / 2, top, 0],
                            stroke_color=color, stroke_width=3).set_fill(_mix(color, 0.12), 1)
        pocket = VMobject(stroke_color=color, stroke_width=2.5).set_points_as_corners(
            [[-width / 2, bot, 0], [0, bot + margin * 0.8, 0], [width / 2, bot, 0]])
        self.part("flap_open", flap_open, "flap_open" in shown if show is not None else False)
        self.part("body", body, "body" in shown)
        self.part("pocket", pocket, "pocket" in shown)
        self.part("flap", flap, "flap" in shown)
        self.sheet_group = VGroup()
        self.add(self.sheet_group)
        self.sheets: list = []
        self.is_open = False
        self._ref = _ref(ORIGIN)
        self.add(self._ref)

    def slot_point(self, i: int):
        c = self._ref.get_center()
        return c + np.array([0, self.env_h / 2 - self.margin - self.pitch * (i + 0.5), 0])

    def sheet(self, text: str, color: str = S.GREY, size: float = CAPTION, mono_: bool = False,
              with_seal: bool = False) -> VGroup:
        """A sheet for this envelope (not added): a tinted strip with a coloured left edge and its
        label (serif, or mono with mono_=True; masked). .frame .text .seal"""
        w, h = self.env_w - 0.5, self.pitch - 0.1
        fr = RoundedRectangle(width=w, height=h, corner_radius=0.06, stroke_color=color,
                              stroke_width=2).set_fill(_mix(color, 0.2), 1)
        edge = Rectangle(width=0.1, height=h - 0.08, stroke_width=0).set_fill(color, 1) \
            .move_to(fr.get_left() + RIGHT * 0.12)
        t = mtext(text, size, INK, font=MONO if mono_ else S.FONT)
        t.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.3)
        g = VGroup(fr, edge, t)
        g.frame, g.text, g.seal = fr, t, None
        if with_seal:
            s = seal(min(0.16, h * 0.42)).move_to(fr.get_right() + LEFT * 0.3)
            g.add(s)
            g.seal = s
        if t.width > w - (0.75 if with_seal else 0.45):
            raise ValueError(f"sheet {text!r} is too long for a {self.env_w}-wide envelope")
        return g

    def add_sheet(self, scene, sheet, start=None, run_time: float = 0.6, extra=()):
        """Play `sheet` into the next free slot and make it a member. A sheet already on screen
        flies from where it is; otherwise it slides in from `start` (default 2.5 to the left)."""
        if len(self.sheets) >= self.slots:
            raise ValueError("the envelope is full (slots=)")
        target = self.slot_point(len(self.sheets))
        on = sheet in scene.get_mobject_family_members()
        if on:
            anim = sheet.animate.move_to(target)
        else:
            src = np.array(start) if start is not None else target + LEFT * 2.5
            sheet.move_to(target)
            anim = FadeIn(sheet, shift=target - src)
        scene.play(anim, *extra, run_time=run_time)
        if sheet in scene.mobjects:
            scene.remove(sheet)
        self.sheet_group.add(sheet)
        self.sheets.append(sheet)
        self._ensure(scene)
        return sheet

    def restack(self) -> list:
        """Animations moving every sheet to its slot (after one left)."""
        return [s.animate.move_to(self.slot_point(i)) for i, s in enumerate(self.sheets)]

    def remove_sheet(self, scene, sheet, shift=RIGHT * 2.5, run_time: float = 0.6, extra=()):
        """Slide `sheet` out (it leaves the scene) and restack the others."""
        self.sheets.remove(sheet)
        self.sheet_group.remove(sheet)
        scene.add(sheet)
        scene.play(FadeOut(sheet, shift=shift), *self.restack(), *extra, run_time=run_time)

    def open(self) -> list:
        """Animations: the flap opens (a triangle above the top edge)."""
        if self.is_open:
            return []
        self.is_open = True
        return self.parts_out("flap") + self.parts_in("flap_open")

    def close(self) -> list:
        if not self.is_open:
            return []
        self.is_open = False
        return self.parts_out("flap_open") + self.parts_in("flap")


# ------------------------------------------------------------------ V3 · the menu and the stage
class MenuColumn(Piece):
    """V3, first half (S04; small again in S06): slide 8's strip, slides 9-12's techniques in
    slide 13's column between two LLMs, then llm-rag's two GREEN menu cards. See the module notes."""

    TECHNIQUES = ("pre-retrieval", "post-retrieval", "retrieval decision", "document grading",
                  "query rewrite", "web search")
    MENU = ("get_book_by_author(author, search_content)", "get_book_by_search_content(search_content)")
    DECISION = 2

    def __init__(self, show=None, size: float = CAPTION, **kw):
        super().__init__(**kw)
        names = ("strip", "llm_top", "llm_bot", "chooses", "agentic", "menu0", "menu1") + \
            tuple(f"box{i}" for i in range(6))
        shown = self._show_set(show, names)
        q = chip("question", LOOKUP, size=size)
        r = chip("Retrieval", DATA, size=size)
        m = chip("LLM", CLOUD, size=size)
        a = chip("Response", S.GREY, size=size)
        row = VGroup(q, r, m, a).arrange(RIGHT, buff=0.9).move_to([0, 2.3, 0])
        arrows = VGroup(*[_arrow(x.get_right(), y.get_left(), buff=0.08) for x, y in zip(row[:-1], row[1:])])
        strip = VGroup(row, arrows)
        strip.boxes = row
        self.part("strip", strip, "strip" in shown)
        col_x = 0.0
        self.part("llm_top", model_box("LLM", w=2.6, h=0.55).move_to([col_x, 1.5, 0]), "llm_top" in shown)
        pitch = 0.6
        self.slot_y = [0.85 - k * pitch for k in range(6)]
        for k, t in enumerate(self.TECHNIQUES):
            b = concept_box(t, size, min_w=3.6).move_to([col_x, self.slot_y[k], 0])
            self.part(f"box{k}", b, f"box{k}" in shown)
        self.part("llm_bot", model_box("LLM", w=2.6, h=0.55).move_to([col_x, self.slot_y[-1] - 0.7, 0]),
                  "llm_bot" in shown)
        ch = label("chooses", size, TURN).next_to(self.parts["llm_top"], RIGHT, buff=0.3)
        self.part("chooses", ch, "chooses" in shown)
        ag = note("agentic RAG").next_to(self.parts["llm_top"], LEFT, buff=0.3)
        self.part("agentic", ag, "agentic" in shown)
        m0 = menu_card(self.MENU[0]).move_to([col_x, self.slot_y[0], 0])
        m1 = menu_card(self.MENU[1]).move_to([col_x, self.slot_y[1], 0])
        self.part("menu0", m0, "menu0" in shown)
        self.part("menu1", m1, "menu1" in shown)
        self._dec_target = _ref([col_x, self.slot_y[3], 0])
        self.add(self._dec_target)

    def fly_in(self, i: int, start=None):
        """Animation: technique box i flies into its slot (from `start`, default the strip's
        Retrieval box) and appears."""
        b = self.parts[f"box{i}"]
        src = np.array(start) if start is not None else self.parts["strip"].boxes[1].get_center()
        return self.parts_in(f"box{i}", anim=lambda m: FadeIn(m, shift=m.get_center() - src))[0]

    def to_menu(self) -> list:
        """Animations: the five other boxes fade, the two GREEN menu cards appear at the column's
        top, "retrieval decision" moves under them (dashed: it stays, for S06)."""
        others = [f"box{k}" for k in range(6) if k != self.DECISION and self.is_shown(f"box{k}")]
        dec = self.parts[f"box{self.DECISION}"]
        anims = self.parts_out(*others) + self.parts_in("menu0", "menu1")
        anims.append(dec.animate.move_to(self._dec_target.get_center()))
        return anims

    def cross_decision(self) -> Line:
        """A RED line through "retrieval decision" (not added)."""
        return strike(self.parts[f"box{self.DECISION}"].box, ERR, 5)


class TrustStage(Piece):
    """V3's stage, in place: Google's cloud | the trust boundary (HTTPS) | your laptop with the
    two TEAL containers. compact=True: the containers hold only their names (and the gear / a
    small cylinder), 12.7 x 2.25, for a picture above a panel. See the module notes."""

    PARTS = ("cloud", "model", "boundary", "https", "laptop", "cli", "chroma", "lock", "gear",
             "hl_cli", "hl_chroma", "hl_model")
    HIDDEN = ("lock", "gear", "hl_cli", "hl_chroma", "hl_model")

    def __init__(self, compact: bool = False, show=None, size: float = CAPTION, **kw):
        super().__init__(**kw)
        shown = set(show) if show is not None else set(self.PARTS) - set(self.HIDDEN)
        self.compact = compact
        bx, cx_cli, cx_ch, cli_w, ch_w = -1.6, 0.45, 4.33, 3.0, 3.85
        lap_top = 0.95 if compact else 1.95
        y_t = lap_top - 0.22
        ch_t = mono("llm-rag-chromadb", size, CTR)
        cli_t = mono("llm-rag-cli", size, CTR)
        if compact:
            cy = cylinder(0.42, 0.26, stroke=2)
            row = VGroup(cy, ch_t).arrange(RIGHT, buff=0.2).move_to([cx_ch, y_t - 0.33, 0])
            cli_t.move_to([cx_cli, y_t - 0.33, 0])
            coll = VGroup()
            y_b = y_t - 0.66
        else:
            ch_t.move_to([cx_ch, y_t - 0.28, 0])
            cy = cylinder(0.95, 0.7).next_to(ch_t, DOWN, buff=0.2)
            cl1 = mono("char-split-collection", size, CTR).next_to(cy, DOWN, buff=0.12)
            cl2 = label("book · author · year", size, S.GREY).next_to(cl1, DOWN, buff=0.06)
            coll = VGroup(cl1, cl2)
            cli_t.move_to([cx_cli, y_t - 0.28, 0])
            y_b = cl2.get_bottom()[1] - 0.16
        box_h, yc = y_t - y_b, (y_t + y_b) / 2

        def cbox(x, w):
            fr = box(w, box_h, CTR, fill=S.BG, fill_opacity=1.0, radius=0.14, stroke=3).move_to([x, yc, 0])
            tint = RoundedRectangle(width=w, height=box_h, corner_radius=0.14, stroke_width=0) \
                .set_fill(CTR, 0.06).move_to(fr)
            return fr, tint

        fr, tint = cbox(cx_cli, cli_w)
        cli = VGroup(fr, tint, cli_t)
        cli.frame, cli.title, cli.files = fr, cli_t, VGroup()
        if not compact:
            files = VGroup(file_row("cli.py"), file_row("agent_tools.py")).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
            files.next_to(cli_t, DOWN, buff=0.22).align_to(fr, LEFT).shift(RIGHT * 0.3)
            cli.add(files)
            cli.files = files
        self.part("cli", cli, "cli" in shown)
        fr2, tint2 = cbox(cx_ch, ch_w)
        chroma = VGroup(fr2, tint2, ch_t, cy, coll)
        chroma.frame, chroma.title, chroma.cyl, chroma.coll = fr2, ch_t, cy, coll
        self.part("chroma", chroma, "chroma" in shown)
        lap_bot = y_b - (0.62 if compact else 0.8)
        lz = laptop_zone(7.5, lap_top - lap_bot, corner=DOWN + RIGHT).move_to([2.6, (lap_top + lap_bot) / 2, 0])
        self.part("laptop", lz, "laptop" in shown)
        self.add_to_back(lz)
        yc_all = (lap_top + lap_bot) / 2
        cl = cloud(width=3.3 if compact else 4.1, color=CLOUD, fill_opacity=0.08)
        if compact:
            cl.move_to([-4.3, yc_all, 0])
            cl_l = label("Google Cloud", size, CLOUD).move_to(cl.get_bottom() + UP * 0.32)
            md = model_box("Gemini", w=1.3, h=0.55).move_to(cl.get_center() + UP * 0.12)
        else:
            cl.move_to([-4.3, yc_all + 0.2, 0])
            cl_l = label("Google Cloud", size, CLOUD).next_to(cl, DOWN, buff=0.12)
            md = model_box("Gemini", w=1.5, h=0.8, sub="location global").move_to(cl.get_center() + DOWN * 0.1)
        self.part("cloud", VGroup(cl, cl_l), "cloud" in shown)
        self.part("model", md, "model" in shown)
        bd = DashedLine([bx, lap_bot, 0], [bx, lap_top - 0.1, 0], color=S.GREY, stroke_width=3, dash_length=0.12)
        self.part("boundary", bd, "boundary" in shown)
        hs = label("HTTPS", size, LOOKUP).next_to(bd, UP, buff=0.08)
        self.part("https", hs, "https" in shown)
        lk = padlock(0.34 if compact else 0.42, S.GREY)
        lk.next_to(cy, RIGHT, buff=0.12) if not compact else lk.next_to(ch_t, RIGHT, buff=0.15)
        self.part("lock", lk, "lock" in shown)
        gr = gear(0.17 if compact else 0.24, CTR)
        if compact:
            gr.next_to(cli_t, RIGHT, buff=0.3)
        else:
            gr.move_to(fr.get_corner(DOWN + RIGHT) + np.array([-0.45, 0.45, 0]))
        self.part("gear", gr, "gear" in shown)
        for nm, frm in (("cli", fr), ("chroma", fr2), ("model", md.frame)):
            hl = frm.copy().set_fill(opacity=0).set_stroke(TURN, 5)
            self.part(f"hl_{nm}", hl, f"hl_{nm}" in shown)
        self._bx = _ref([bx, 0, 0])
        self._bottom = _ref([0, lap_bot, 0])
        self.add(self._bx, self._bottom)

    def send(self, mob, to: str = "laptop", y: float | None = None):
        """Animation: `mob` moves to that side of the boundary (its edge 0.2 from the line), at
        height y (relative to the stage's centre; default: the upper part)."""
        x = self._bx.get_center()[0]
        yc = self.get_center()[1] + (y if y is not None else (0.3 if self.compact else 0.9))
        if to == "cloud":
            p = np.array([x - 0.2 - mob.width / 2, yc, 0])
        elif to == "laptop":
            p = np.array([x + 0.2 + mob.width / 2, yc, 0])
        else:
            raise ValueError("to='cloud' or 'laptop'")
        return mob.animate.move_to(p)

    def dip(self, color: str = LOOKUP) -> Arrow:
        """A PINK arrow from the CLI container into the cylinder (not added)."""
        cli, cy = self.parts["cli"], self.parts["chroma"].cyl
        return _arrow(cli.frame.get_right() + DOWN * (0.0 if self.compact else 0.1), cy.get_left(),
                      color=color, stroke=4)

    def chunk_cards(self, n: int = 10) -> VGroup:
        """n small GREEN chunk cards in two rows in the laptop's bottom margin, under the CLI box
        (not added)."""
        cards = VGroup(*[chunk_card(0.42, 0.2) for _ in range(n)])
        cards.arrange_in_grid(2, (n + 1) // 2, buff=(0.1, 0.05))
        cli = self.parts["cli"].frame
        cards.next_to(cli, DOWN, buff=0.08)
        return cards

    def light(self, name: str, color: str = TURN) -> list:
        """Animations: a YELLOW outline over "cli", "chroma" or "model" (the box itself is not
        restroked: its opaque fill would cover its contents while it moves)."""
        hl = self.parts[f"hl_{name}"]
        if getattr(hl, "hidden", False):
            _set_op(hl)
            _save_op(hl)
            _set_op(hl, 0)
        hl.set_stroke(color)
        return self.parts_in(f"hl_{name}")

    def unlight(self, name: str) -> list:
        return self.parts_out(f"hl_{name}")


# ------------------------------------------------------------------ V4 · the hub and the loop
class HubSpokes(Piece):
    """V4, first half (slides 35-40): the LLM core and the prompt "become" a decision maker with
    two-way spokes to a planner, tools and memory. See the module notes."""

    PARTS = ("core", "sheet", "becomes", "hub", "planner", "tools", "memory", "sp_planner", "sp_tools",
             "sp_memory")

    def __init__(self, show=None, size: float = 22, **kw):
        super().__init__(**kw)
        shown = self._show_set(show, self.PARTS)
        core = _keep(chip("LLM core", CLOUD, size=size))
        core.move_to([-1.3, 2.05, 0])
        sheet = _keep(chip("instructions", S.GREY, size=size))
        sheet.move_to([1.3, 2.05, 0])
        self.part("core", core, "core" in shown)
        self.part("sheet", sheet, "sheet" in shown)
        bec = label("becomes", CAPTION, S.GREY).move_to([0, 1.45, 0])
        self.part("becomes", bec, "becomes" in shown)
        hub_c = Circle(radius=0.85, stroke_color=CLOUD, stroke_width=3).set_fill(CLOUD, 0.12).move_to([0, 0.1, 0])
        ht = VGroup(sans("decision", size), sans("maker", size)).arrange(DOWN, buff=0.06).move_to(hub_c)
        hub = VGroup(hub_c, ht)
        hub.circle = hub_c
        self.part("hub", hub, "hub" in shown)
        pos = {"planner": [3.35, -0.5, 0], "tools": [-3.35, -0.5, 0], "memory": [0, -2.45, 0]}
        for nm, p in pos.items():
            t = sans(nm, size)
            fr = box(max(1.9, t.width + 0.5), 0.72, S.GREY, fill=S.BG, fill_opacity=1.0, stroke=3).move_to(p)
            t.move_to(fr)
            node = VGroup(fr, t)
            node.frame = fr
            self.part(nm, node, nm in shown)
            a, b = hub_c, fr
            v = b.get_center() - a.get_center()
            u = v / np.linalg.norm(v)
            perp = np.array([-u[1], u[0], 0]) * 0.13
            p0 = a.get_center() + u * 0.9
            p1 = b.get_center() - u * (0.5 if nm == "memory" else 1.05)
            out = Arrow(p0 + perp, p1 + perp, buff=0, color=S.GREY, stroke_width=3,
                        max_tip_length_to_length_ratio=0.12, tip_length=0.16)
            back = Arrow(p1 - perp, p0 - perp, buff=0, color=S.GREY, stroke_width=3,
                         max_tip_length_to_length_ratio=0.12, tip_length=0.16)
            self.part(f"sp_{nm}", VGroup(out, back), f"sp_{nm}" in shown)

    def merge(self) -> list:
        """Animations: the core chip and the instructions sheet sink into the hub, which appears."""
        hub = self.parts["hub"]
        anims = []
        for n in ("core", "sheet"):
            m = self.parts[n]
            if getattr(m, "hidden", False):
                continue
            _save_op(m)
            anims.append(m.animate.move_to(hub.circle.get_center()).set_opacity(0))
            self._flag(m, True)
        return anims + self.parts_in("hub")

    def spokes(self) -> list:
        """Animations: the three nodes and their two-way spokes appear."""
        return self.parts_in("planner", "tools", "memory") + \
            self.parts_in("sp_planner", "sp_tools", "sp_memory")


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

    def relabel(self, text: str, color: str | None = None):
        """Animation: the label above the gate changes (.caption is the new label afterwards)."""
        col = color or self.bar.get_color()
        new = sans(text, self.size, col, weight="BOLD").move_to(self.caption)
        old, self.caption = self.caption, new
        return ReplacementTransform(old, new)

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
        return s.move_to(card.get_corner(UP + RIGHT) + np.array([-s.width / 2 - 0.1, -s.height / 2 - 0.05, 0]))


class LoopTrack(Piece):
    """V4, second half: the agent loop as a clockwise track, model (top, BLUE) -> tools (bottom,
    PURPLE) -> model; a YELLOW token runs laps, a counter ticks against the cap; an exit from the
    model station leads to a Gate "final response". See the module notes."""

    PARTS = ("track", "model", "tools", "token", "counter", "exit", "gate")

    def __init__(self, cap: int = 12, radius: float = 1.35, show=None, size: float = 22, **kw):
        super().__init__(**kw)
        shown = self._show_set(show, self.PARTS)
        self.cap, self.count, self.size = cap, 0, size
        c = np.array([-1.9, -0.15, 0])
        self._c = _ref(c)
        self.add(self._c)
        tr = Circle(radius=radius, stroke_color=S.GREY, stroke_width=4).move_to(c)
        tips = VGroup()
        for ang in (0.0, PI):                     # clockwise: down on the right, up on the left
            p = c + radius * np.array([np.cos(ang), np.sin(ang), 0])
            d = np.array([0, -1, 0]) if ang == 0.0 else np.array([0, 1, 0])
            tips.add(Arrow(p - d * 0.25, p + d * 0.25, buff=0, color=S.GREY, stroke_width=4,
                           max_tip_length_to_length_ratio=0.5, tip_length=0.2))
        self.part("track", VGroup(tr, tips), "track" in shown)
        self.radius = radius
        st_m = box(1.6, 0.62, CLOUD, fill=S.BG, fill_opacity=1.0, stroke=3).move_to(c + UP * radius)
        st_m_t = sans("model", size).move_to(st_m)
        st_t = box(1.6, 0.62, TOOL, fill=S.BG, fill_opacity=1.0, stroke=3).move_to(c + DOWN * radius)
        st_t_t = sans("tools", size).move_to(st_t)
        self.part("model", VGroup(st_m, st_m_t), "model" in shown)
        self.part("tools", VGroup(st_t, st_t_t), "tools" in shown)
        tok = Dot(c + radius * np.array([np.cos(PI * 0.75), np.sin(PI * 0.75), 0]), radius=0.13, color=TURN)
        self.part("token", tok, "token" in shown)
        cnt = self._counter_text(0).move_to(c + RIGHT * 0.0 + DOWN * 0.0)
        self.part("counter", cnt, "counter" in shown)
        ex = _arrow(st_m.get_right(), st_m.get_right() + RIGHT * 2.9, color=S.GREY)
        self.part("exit", ex, "exit" in shown)
        g = Gate("final response", TURN, gate_w=1.2, gate_h=1.5)
        g.shift(ex.get_end() + RIGHT * 0.12 - g.pivot())
        self.gate = g
        self.part("gate", g, "gate" in shown)
        self.move_to(ORIGIN)

    def _counter_text(self, k: int) -> VGroup:
        n = mono(f"{k} / {self.cap}", self.size + 4, INK)
        t = label("turns", CAPTION, S.GREY).next_to(n, DOWN, buff=0.08)
        return VGroup(n, t)

    def lap(self, run_time: float = 1.6):
        """Animation: the token runs one clockwise lap, then the counter ticks (k / cap)."""
        self.count += 1
        cnt = self.parts["counter"]
        new = self._counter_text(self.count).move_to(cnt)
        return Succession(Rotate(self.parts["token"], angle=-TAU, about_point=self._c.get_center(),
                                 run_time=run_time, rate_func=linear),
                          Transform(cnt, new, run_time=0.25))

    def set_count(self, k: int):
        """Jump the counter to k (no animation; for the replay)."""
        self.count = k
        cnt = self.parts["counter"]
        cnt.become(self._counter_text(k).move_to(cnt))
        return self

    def reply_card(self, text: str = "text · no function call") -> VGroup:
        """A GREY card at the exit (the model's reply with no function call; not added)."""
        c = _keep(chip(text, S.GREY, size=CAPTION))
        ex = self.parts["exit"]
        return c.next_to(ex, UP, buff=0.12).align_to(ex, LEFT)


# ------------------------------------------------------------------ V5 · which Python, which wheel
class VersionLine(Piece):
    """V5: Python 3.x versions on a number line (positions by MINOR version: 10 means 3.10), the
    `>= 3.lo` interval glowing GREEN off the right end (from L01). See the module notes."""

    def __init__(self, first: int = 10, last: int = 16, lo: int = 10, width: float = 11.0,
                 size: float = 22, **kw):
        super().__init__(**kw)
        self.first, self.last, self.lo, self.line_w = first, last, lo, width
        self.axis = Line(LEFT * width / 2, RIGHT * width / 2, color=S.GREY, stroke_width=3)
        self.ticks = VGroup()
        for m in range(first, last + 1):
            x = self._x(m)
            self.ticks.add(VGroup(Line([x, -0.12, 0], [x, 0.12, 0], color=S.GREY, stroke_width=2),
                                  mono(f"3.{m}", size, S.GREY).move_to([x, -0.45, 0])))
        right = width / 2 + 0.25
        self.band = Rectangle(width=right - self._x(lo), height=0.3, stroke_width=0).set_fill(VENV, 0.3)
        self.band.move_to([(self._x(lo) + right) / 2, 0, 0])
        self.band_label = mono(f'requires-python = ">=3.{lo}"', size, VENV)
        self.band_label.next_to(self.band, UP, buff=0.3).align_to(self.band, LEFT)
        self.part("band", self.band)
        self.part("axis", self.axis)
        self.part("ticks", self.ticks)
        self.part("band_label", self.band_label)

    def _x(self, minor: float) -> float:
        return -self.line_w / 2 + (minor - self.first + 0.5) / (self.last - self.first + 1) * self.line_w

    def point(self, minor: float, dy: float = 0.0):
        """A point on the (possibly moved) axis above minor version `minor`."""
        left = self.axis.get_start()
        return left + np.array([self._x(minor) + self.line_w / 2, dy, 0])

    def dot(self, minor: float, text: str, color: str, above: bool = True, size: float = 22) -> VGroup:
        d = Dot(self.point(minor), radius=0.11, color=color)
        t = mono(text, size, color)
        t.next_to(d, UP if above else DOWN, buff=0.3 if above else 0.75)
        g = VGroup(d, t)
        g.dot, g.text = d, t
        return g

    def drop(self, minor: float, text: str, color: str = TOOL, size: float = 22) -> VGroup:
        """A download arrow dropping onto `minor`, with a dot and a label above the arrow (not
        added): "CPython 3.15.0" at 15. .arrow .dot .text"""
        p = self.point(minor)
        d = Dot(p, radius=0.12, color=color)
        a = Arrow(p + UP * 1.1, p + UP * 0.15, buff=0, color=color, stroke_width=5,
                  max_tip_length_to_length_ratio=0.3)
        t = mono(text, size, color).next_to(a, UP, buff=0.08)
        if t.get_right()[0] > self.axis.get_end()[0] + 0.3:
            t.align_to(a, RIGHT).shift(RIGHT * 0.3)
        g = VGroup(a, d, t)
        g.arrow, g.dot, g.text = a, d, t
        return g

    def collapse(self, minor: float, text: str | None = None) -> list:
        """Animations: the band shrinks to one point at `minor` (a GREEN marker); the band label
        becomes `text` when given (e.g. "uv python pin 3.13")."""
        p = self.point(minor)
        mark = RoundedRectangle(width=0.36, height=0.36, corner_radius=0.08, stroke_color=VENV,
                                stroke_width=3).set_fill(VENV, 0.5).move_to(p)
        anims = [Transform(self.band, mark)]
        if text:
            new = mono(text, 22, VENV)
            new.next_to(mark, UP, buff=0.3)
            anims.append(Transform(self.band_label, new))
        return anims


class WheelShelf(Piece):
    """V5's shelf of wheels for onnxruntime 1.31.0 (adk-laptop/07 lines 9-11): one wheel per ABI
    tag, and an empty dashed slot for cp315. See the module notes."""

    def __init__(self, tags=WHEEL_TAGS, missing: str = "cp315",
                 title: str = "onnxruntime 1.31.0 · wheels", slot_w: float = 1.25, size: float = CAPTION, **kw):
        super().__init__(**kw)
        n = len(tags) + 1
        w = n * slot_w
        self.wheels = {}
        xs = [-w / 2 + slot_w * (k + 0.5) for k in range(n)]
        for k, tg in enumerate(tags):
            wh = wheel_glyph(0.24).move_to([xs[k], 0.35, 0])
            t = mono(tg, size, S.GREY).move_to([xs[k], -0.2, 0])
            g = VGroup(wh, t)
            g.glyph, g.text = wh, t
            self.wheels[tg] = g
            self.part(f"w_{tg}", g)
        ring_ = DashedVMobject(Circle(radius=0.24), num_dashes=14).set_stroke(S.GREY, 2.5).move_to([xs[-1], 0.35, 0])
        mt = mono(missing, size, S.GREY).move_to([xs[-1], -0.2, 0])
        miss = VGroup(ring_, mt)
        miss.glyph, miss.text = ring_, mt
        self.miss = miss
        self.part("missing", miss)
        board = Line([-w / 2 - 0.1, 0.06, 0], [w / 2 + 0.1, 0.06, 0], color=S.GREY, stroke_width=5)
        self.part("board", board)
        tt = mono(title, size, S.GREY).next_to(board, UP, buff=0.62).align_to(board, LEFT)
        self.part("title", tt)

    def wheel(self, tag_: str):
        return self.wheels[tag_]

    def missing(self) -> list:
        """Animations: the cp315 slot turns RED, with a cross."""
        x = cross_mark(0.26, ERR).move_to(self.miss.glyph)
        self.miss.add(x)
        x.set_opacity(0)
        return [self.miss.glyph.animate.set_stroke(ERR), self.miss.text.animate.set_color(ERR),
                x.animate.set_opacity(1)]

    def click(self, tag_: str = "cp313", color: str = DATA) -> list:
        """Animations: that wheel turns GREEN and clicks (a pulse)."""
        g = self.wheels[tag_]
        return [g.glyph.animate.set_color(color).scale(1.15), g.text.animate.set_color(color)]


# ------------------------------------------------------------------ V6 · the shared whiteboard
class Whiteboard(Piece):
    """V6: the session as a GREEN whiteboard with one cell per output_key, and the events column
    beside it (what adk web's Events tab lists). See the module notes."""

    def __init__(self, keys=STATE_KEYS, board_w: float = 3.9, cell_pitch: float = 0.95,
                 events_w: float = 2.6, size: float = CAPTION, title: str = "session state", **kw):
        super().__init__(**kw)
        self.keys = list(keys)
        n = len(keys)
        h = 0.55 + n * cell_pitch + 0.15
        bd = box(board_w, h, DATA, fill=S.BG, fill_opacity=1.0, stroke=3, radius=0.16)
        tint = RoundedRectangle(width=board_w, height=h, corner_radius=0.16, stroke_width=0).set_fill(DATA, 0.05)
        bd_t = label(title, 22, DATA).move_to(bd.get_corner(UP + LEFT) + np.array([0.25, -0.3, 0]), aligned_edge=LEFT)
        self.part("board", VGroup(bd, tint, bd_t))
        self.board_frame = bd
        self.slots, self.cells = [], []
        top = bd.get_top()[1] - 0.6
        for i, k in enumerate(keys):
            kt = mono(k, size, S.GREY).move_to([bd.get_left()[0] + 0.3, top - i * cell_pitch - 0.14, 0], aligned_edge=LEFT)
            sl = box(board_w - 0.5, cell_pitch - 0.45, DATA, dashed=True, stroke=2)
            sl.move_to([bd.get_center()[0], kt.get_bottom()[1] - 0.06 - sl.height / 2, 0])
            cell = VGroup(kt, sl)
            cell.key, cell.slot = kt, sl
            self.part(f"cell{i}", cell)
            self.slots.append(sl)
            self.cells.append(cell)
        ev = box(events_w, h, S.GREY, fill=S.BG, fill_opacity=1.0, stroke=2.5, radius=0.16)
        ev.next_to(bd, RIGHT, buff=0.3)
        ev_t = label("events", 22, S.GREY).move_to(ev.get_top() + DOWN * 0.3)
        self.part("events", VGroup(ev, ev_t))
        self.events_frame = ev
        self.n_events = 0
        self.size = size
        self.move_to(ORIGIN)

    def slot(self, i: int):
        return self.slots[i]

    def blank_card(self, i: int = 0, color: str = DATA) -> VGroup:
        """A blank GREEN reply card sized to cell i (no text: no model output was recorded)."""
        sl = self.slots[i]
        return chunk_card(sl.width * 0.8, sl.height * 0.78, color, rows=2)

    def fill(self, i: int, card):
        """Animation: `card` moves into cell i's slot."""
        return card.animate.move_to(self.slots[i].get_center())

    def event_block(self, text: str, color: str = S.GREY) -> VGroup:
        """The next event block in the events column, placed (not added: FadeIn it)."""
        ev = self.events_frame
        w = ev.width - 0.3
        t = sans(text, self.size, INK)
        if t.width > w - 0.12:
            raise ValueError(f"event {text!r} is too wide for the events column (events_w=)")
        b = box(w, 0.42, color, fill=S.BG, fill_opacity=1.0, stroke=2, radius=0.08)
        y = ev.get_top()[1] - 0.72 - self.n_events * 0.5
        b.move_to([ev.get_center()[0], y, 0])
        t.move_to(b)
        self.n_events += 1
        g = VGroup(b, t)
        g.frame, g.text = b, t
        return g


class AgentCard(VGroup):
    """V6's LlmAgent: a BLUE mono name chip over a GREY instruction card (mono, masked). hole=
    "{itinerary_validation}" draws a PINK hole around that placeholder. .model .card .line .hole
    .fill_hole(card) -> [anims] (the cell's card flies into the hole before the call)"""

    def __init__(self, agent: str, instruction: str, hole: str | None = None, size: float = CAPTION, **kw):
        super().__init__(**kw)
        self.model = _keep(chip(agent, CLOUD, size=size, font=MONO))
        ln = mono_line(unname(instruction), size, INK)
        grey_masks(ln)
        self.line = ln
        cd = box(ln.width + 0.5, ln.strut.height + 0.36, S.GREY, fill=S.BG, fill_opacity=1.0, radius=0.1)
        ln.move_to(cd)
        self.card = VGroup(cd, ln)
        self.card.next_to(self.model, DOWN, buff=0.1).align_to(self.model, LEFT)
        self.add(self.model, self.card)
        self.hole = None
        if hole:
            g = substring(ln, hole)
            hl = RoundedRectangle(width=g.width + 0.14, height=ln.strut.height + 0.06, corner_radius=0.08,
                                  stroke_color=LOOKUP, stroke_width=2.5).set_fill(LOOKUP, 0.12)
            hl.move_to([g.get_center()[0], ln.strut.get_center()[1], 0])
            self.hole = hl
            self.card.submobjects.insert(1, hl)      # behind the text
        self.agent = agent

    def fill_hole(self, card) -> list:
        h = self.hole
        if h is None:
            raise ValueError("this AgentCard has no hole")
        return [card.animate.move_to(h.get_center()).scale_to_fit_height(h.height * 0.8),
                h.animate.set_fill(LOOKUP, 0.28)]


# ------------------------------------------------------------------ V7 · one protocol, one plug per server
BINS = (("data", "fetch"), ("action", "change something"), ("orchestration", "hand work to an agent"))
SERVICES = ("email · SMTP/IMAP", "calendar · CalDAV", "search · REST", "database · SQL/NoSQL",
            "an API · REST", "files · File I/O", "drive · Drive API", "maps · Maps API",
            "chat · chat API", "messages · messaging API")


def _bin_shape(w: float, h: float, color: str = S.GREY) -> VMobject:
    m = VMobject(stroke_color=color, stroke_width=4)
    m.set_points_as_corners([[-w / 2, h / 2, 0], [-w / 2, -h / 2, 0], [w / 2, -h / 2, 0], [w / 2, h / 2, 0]])
    return m


class ToolBins(Piece):
    """V7's three tool families (slide 51) as open bins. See the module notes."""

    def __init__(self, bin_w: float = 4.0, bin_h: float = 1.95, gap: float = 0.3, size: float = CAPTION, **kw):
        super().__init__(**kw)
        self.bin_w, self.bin_h = bin_w, bin_h
        self.bins, self.fill_count = {}, {}
        for k, (nm, what) in enumerate(BINS):
            x = (k - 1) * (bin_w + gap)
            sh = _bin_shape(bin_w, bin_h).move_to([x, 0, 0])
            t = VGroup(label(nm, 22, INK), label(what, size, S.GREY)).arrange(DOWN, buff=0.08)
            t.next_to(sh, UP, buff=0.12)
            if t.width > bin_w + gap - 0.05:
                raise ValueError(f"bin title {nm!r} wider than its bin")
            g = VGroup(sh, t)
            g.shape, g.title = sh, t
            self.bins[nm] = g
            self.fill_count[nm] = 0
            self.part(nm, g)

    def bin(self, name: str):
        return self.bins[name]

    def drop(self, chip_, name: str):
        """Animation: chip_ drops into the bin's next row (top-down; at most 3)."""
        g = self.bins[name]
        k = self.fill_count[name]
        if k >= 3:
            raise ValueError(f"bin {name!r} is full")
        if chip_.width > self.bin_w - 0.25:
            raise ValueError(f"a {chip_.width:.2f}-wide chip does not fit the {name!r} bin")
        top = g.shape.get_top()[1] - 0.12
        y = top - 0.3 - k * 0.58
        self.fill_count[name] = k + 1
        return chip_.animate.move_to([g.shape.get_center()[0], y, 0])


def mini_bin(text: str = "orchestration", color: str = S.GREY, w: float = 2.2, h: float = 0.8) -> VGroup:
    """A small open bin with its name under it (S13's orchestration bin). .shape .caption"""
    sh = _bin_shape(w, h, color)
    c = label(text, CAPTION, color).next_to(sh, DOWN, buff=0.1)
    g = VGroup(sh, c)
    g.shape, g.caption = sh, c
    return _keep(g)


class ServiceFan(Piece):
    """V7, slides 52-53, in place: one agent wired to ten services, each with its own protocol;
    then the MCP host, one PINK trunk "same protocol", and an MCP-server adapter on each service.
    See the module notes."""

    PARTS = ("agent", "pills", "services", "wires", "customs", "host", "trunk", "adapters")

    def __init__(self, services=SERVICES, pitch: float = 0.5, show=("agent", "pills", "services", "wires"),
                 size: float = CAPTION, **kw):
        super().__init__(**kw)
        shown = self._show_set(show, self.PARTS)
        n = len(services)
        ys = [(n - 1) / 2 * pitch - k * pitch for k in range(n)]
        ag = box(2.6, 3.4, S.GREY, fill=S.BG, fill_opacity=1.0, stroke=3).move_to([-5.0, 0, 0])
        ag_t = sans("agent", 22).move_to(ag.get_top() + DOWN * 0.32)
        self.part("agent", VGroup(ag, ag_t), "agent" in shown)
        self.agent_frame = ag
        pills = VGroup(*[_keep(chip(f"Tool {k + 1}", S.GREY, size=size)) for k in range(4)])
        pills.arrange(DOWN, buff=0.14).move_to(ag.get_center() + DOWN * 0.25)
        self.part("pills", pills, "pills" in shown)
        sv = VGroup()
        for k, s in enumerate(services):
            t = label(s, size, INK)
            b = box(3.4, 0.42, S.GREY, fill=S.BG, fill_opacity=1.0, stroke=2, radius=0.08)
            b.move_to([4.85, ys[k], 0])
            t.move_to(b)
            if t.width > b.width - 0.15:
                raise ValueError(f"service label {s!r} too wide")
            sv.add(VGroup(b, t))
        self.part("services", sv, "services" in shown)
        cx = 2.2
        x0 = ag.get_right()[0]
        wires = VGroup()
        for k in range(n):
            y0 = (ys[k] / ys[0]) * 1.2 if ys[0] else 0
            wires.add(Line([x0, y0, 0], [sv[k][0].get_left()[0], ys[k], 0], color=S.GREY, stroke_width=2))
        self.part("wires", wires, "wires" in shown)
        customs = VGroup()
        for k in range(n):
            b = box(1.65, 0.38, S.GREY, fill=S.BG, fill_opacity=1.0, stroke=2, radius=0.08).move_to([cx, ys[k], 0])
            customs.add(VGroup(b, label("custom code", size, S.GREY).move_to(b)))
        self.part("customs", customs, False)
        for k in range(n):
            self.parts[f"custom{k}"] = customs[k]
        ht = sans("MCP host", 22, INK).move_to(ag_t)
        ports = VGroup(*[Dot(radius=0.07, color=LOOKUP).move_to([x0, y, 0]) for y in (0.8, 0.27, -0.27, -0.8)])
        pl = label("clients", size, LOOKUP).next_to(ports, RIGHT, buff=0.12).shift(UP * 1.25)
        cover = Rectangle(width=ag_t.width + 0.2, height=ag_t.height + 0.1, stroke_width=0).set_fill(S.BG, 1).move_to(ag_t)
        self.part("host", VGroup(cover, ht, ports, pl), False)
        tx = 0.6
        trunk = Line([x0, 0, 0], [tx, 0, 0], color=LOOKUP, stroke_width=9)
        tl = label("same protocol", size, LOOKUP).next_to(trunk, UP, buff=0.12)
        branches = VGroup(*[Line([tx, 0, 0], [cx - 0.83, ys[k], 0], color=LOOKUP, stroke_width=2.5) for k in range(n)])
        self.part("trunk", VGroup(trunk, branches, tl), False)
        adapters = VGroup()
        for k in range(n):
            b = box(1.65, 0.38, TOOL, fill=S.BG, fill_opacity=1.0, stroke=2.5, radius=0.08).move_to([cx, ys[k], 0])
            adapters.add(VGroup(b, label("MCP server", size, TOOL).move_to(b)))
        self.part("adapters", adapters, False)

    def custom_in(self, i: int):
        """Animation: a "custom code" block grows on wire i."""
        m = self.parts["customs"][i]
        if getattr(self.parts["customs"], "hidden", False):
            _set_op(self.parts["customs"])
            for k, c in enumerate(self.parts["customs"]):
                if k != i:
                    _save_op(c)
                    _set_op(c, 0)
            self.parts["customs"].hidden = False
        else:
            _set_op(m)
        return FadeIn(m, scale=0.6)

    def to_mcp(self) -> list:
        """Animations: wires and custom blocks fade, the agent becomes the MCP host with client
        ports, the PINK trunk "same protocol" and its branches appear, an "MCP server" adapter
        clicks onto each service."""
        anims = []
        for nm in ("wires", "customs"):
            m = self.parts[nm]
            if not getattr(m, "hidden", False):
                _save_op(m)
                anims.append(m.animate.set_opacity(0))
                m.hidden = True
        return anims + self.parts_in("host", "trunk", "adapters")


class Sieve(Piece):
    """V7's `tool_filter`: the filesystem server's 14 tools as GREY chips (the five the script
    names labelled, the rest blank pills) over a sieve; three pass. See the module notes."""

    NAMED = ("list_directory", "read_file", "search_files", "write_file", "edit_file")

    def __init__(self, names=None, keep=MCP_KEPT, named=NAMED, size: float = CAPTION, **kw):
        super().__init__(**kw)
        names = list(names or MCP_TOOLS)
        self.keep, self.named = tuple(keep), tuple(named)
        chips = []
        for nm in names:
            if nm in named:
                c = _keep(chip(nm, S.GREY, size=size, font=MONO))
            else:
                c = RoundedRectangle(width=0.85, height=0.42, corner_radius=0.2, stroke_color=S.GREY,
                                     stroke_width=2).set_fill(S.GREY, 0.15)
            c.tool = nm
            chips.append(c)
        half = (len(chips) + 1) // 2
        r1 = VGroup(*chips[:half]).arrange(RIGHT, buff=0.15)
        r2 = VGroup(*chips[half:]).arrange(RIGHT, buff=0.15)
        rows = VGroup(r1, r2).arrange(DOWN, buff=0.22).move_to([0, 1.3, 0])
        self.chips = {c.tool: c for c in chips}
        self.part("chips", rows)
        w = max(rows.width + 0.6, 6.0)
        mesh = VGroup(Line([-w / 2, 0, 0], [w / 2, 0, 0], color=TURN, stroke_width=4))
        for k in range(int(w / 0.5)):
            x = -w / 2 + 0.25 + k * 0.5
            mesh.add(Line([x, -0.08, 0], [x, 0.08, 0], color=TURN, stroke_width=3))
        mesh.move_to([0, 0.15, 0])
        lab = mono("tool_filter", 22, TURN).next_to(mesh, RIGHT, buff=0.2)
        if lab.get_right()[0] > 6.4:
            lab.next_to(mesh, DOWN, buff=0.12).align_to(mesh, RIGHT)
        self.part("sieve", VGroup(mesh, lab))
        self.mesh = mesh
        self.move_to(ORIGIN)

    def fall(self) -> list:
        """Animations: the chips drop onto the sieve."""
        rows = self.parts["chips"]
        dy = (self.mesh.get_top()[1] + 0.12) - rows.get_bottom()[1]
        return [rows.animate.shift(UP * dy)]

    def sift(self) -> list:
        """Animations: the kept tools fall through (GREEN, in a row under the sieve), write_file and
        edit_file bounce off (RED border), the others dim."""
        anims = []
        kept = [self.chips[n] for n in self.keep]
        row = VGroup(*[k.copy() for k in kept]).arrange(RIGHT, buff=0.3)
        row.move_to([self.mesh.get_center()[0], self.mesh.get_bottom()[1] - 0.6, 0])
        for k, tgt in zip(kept, row):
            anims.append(k.animate.move_to(tgt.get_center()).set_color(DATA))
        for nm, c in self.chips.items():
            if nm in self.keep:
                continue
            if nm in self.named:
                anims.append(c.animate.shift(UP * 0.25).set_stroke(ERR))
            else:
                anims.append(c.animate.set_opacity(0.3))
        return anims


def plug_line(a, b, text: str | None = None, color: str = LOOKUP, size: float = CAPTION,
              stroke: float = 4, dashed: bool = False) -> VGroup:
    """A transport line between two points (a PINK stdio pipe, an HTTPS line), its label above the
    middle. .line .caption"""
    a, b = np.array(a, dtype=float), np.array(b, dtype=float)
    ln = (DashedLine(a, b, color=color, stroke_width=stroke) if dashed
          else Line(a, b, color=color, stroke_width=stroke))
    g = VGroup(ln)
    g.line, g.caption = ln, None
    if text:
        t = label(text, size, color).next_to(ln.get_center(), UP, buff=0.12)
        g.add(t)
        g.caption = t
    return g


# ------------------------------------------------------------------ V8 · the harness
class BudgetTape(Piece):
    """V8's calculator (S14): Python builds the budget line by line from the saved run's costs_usd
    (c27): 880 + 1,000 + 600 + 150 + 60 = 2,690 of 6,000. Rows hidden until row_anims().
    .rows .total .glyph"""

    def __init__(self, items=BUDGET, total: int = BUDGET_TOTAL, cap: int = BUDGET_CAP,
                 size: float = CAPTION, **kw):
        super().__init__(**kw)
        if sum(v for _, v in items) != total:
            raise ValueError("the budget lines do not add up to the total (check c27)")
        gl = calculator_glyph(0.9)
        self.part("glyph", gl)
        texts = [f"{'+' if k else ' '} {v:>6,}  {key}" for k, (key, v) in enumerate(items)]
        rows = VGroup(*[mono(t, size, INK) for t in texts]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        rows.next_to(gl, RIGHT, buff=0.4).align_to(gl, UP)
        self.rows = rows
        for k, r in enumerate(rows):
            self.part(f"row{k}", r, False)
        rule = Line(rows.get_corner(DOWN + LEFT) + DOWN * 0.1, rows.get_corner(DOWN + LEFT) + DOWN * 0.1 + RIGHT * 2.2,
                    color=S.GREY, stroke_width=2)
        tot = mono(f"= {total:>6,}  of {cap:,}", 24, DATA).next_to(rule, DOWN, buff=0.12).align_to(rows, LEFT)
        self.part("rule", rule, False)
        self.part("total", tot, False)
        self.total = tot
        self.move_to(ORIGIN)

    def row_anims(self) -> list:
        """One animation per row in order, then the rule + total."""
        out = [self.parts_in(f"row{k}")[0] for k in range(len(self.rows))]
        out.append(AnimationGroup(*self.parts_in("rule", "total")))
        return out


# ------------------------------------------------------------------ cost dial (from L01)
class CostDial(VGroup):
    """A GOLD dial whose needle sweeps (no digits: no invented price). .run(scene, turns, secs);
    .freeze() before it leaves. .needle .tracker"""

    def __init__(self, radius: float = 0.55, caption: str | None = "cost", **kw):
        super().__init__(**kw)
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
