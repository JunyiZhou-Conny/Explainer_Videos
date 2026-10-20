"""Shared code for AC215 L5 (Introduction to RAG, follow-along: dlops-io/llm-rag): paths, narration,
the semantic colours of BRIEF.md, the README trackers, loaders for the real captures in assets/,
terminal / panel / card helpers, and the video's recurring pictures V1-V8 of BRIEF.md.
Tested on screen by build/common_test.py (explainer.check / explainer.preview).

Notes for scene authors
=======================

    from common import *      # every scene: SAY = NARRATION["S07"]; assert len(SAY) == n;
                              # one `with self.voiceover(SAY[i]) as vo:` per SAY line, in order
Everything below draws text at 20-26 pt. Never .scale() a group that holds text below 1.0: use
piece.rescale(k) (shapes shrink, text keeps its size). Frame budget: the tracker band is y 2.90..3.5
(x -6.5..-0.1 at most), lecture_ref top right; a 3-row strip's top is STRIP_TOP (-1.44), so a
picture above a strip has y -1.3..2.8 (4.1 tall); a 6-row terminal's top is strip_top(6); keep
x in [-6.6, 6.6]. The V1 mini-map (3.3 x 1.45) sits at MINI_CENTER (bottom right, y -3.52..-2.07)
when nothing else is down there, at MINI_ABOVE_STRIP (y -1.33..0.13) while the 3-row strip is up;
hide it while a terminal taller than the strip or a code panel of more than 5 lines is up.

Data and sources
    NARRATION["S01"] ... ["S16"]   SAY lines from script.md      TITLES[cls], SPEC (video.yaml)
    capture(name, folder) -> Capture   assets/terminal/<folder>/<name>.txt; name may be the number
        alone ("10" -> 10-chunk-char-split.txt; "07" never picks the .plain log; "05b", "11b",
        "12b", "17b" are their own names), or "folder/name" as one argument. Tabs expanded (8).
        Folders: laptop, cli-container, recorded-embeddings, gotchas, expected (line 1 is a '#'
        header; out-txt-agent-run.txt: output from file line 2). capture-only/ is plumbing: never.
        .cmd (the `$` line without "$ "; a heredoc's first line only) .lines .exit .first
        .line(n) one FILE line   .at(2, (5, 7), "…", 33)  lines BY FILE LINE NUMBER, "…" inserted
        .join(7, 8) two terminal-wrapped lines joined   .cut(6, "origin/HEAD)") line 6 up to and
        including the marker   .typed(n) the command on prompt line n   .pick() (= file line - 1)
        Lines the script never shows (names) raise ValueError: cli-container/10:36, 13:36, 15:3,
        recorded-embeddings/01:145, 02:156, 07:12-21, 08:6, 08:12, laptop/05:6-7 (6 only via
        .cut(6, "origin/HEAD)")), recorded-embeddings/05:6 and cli-container/70:6 (only via
        .cut(6, "]")), expected/out-txt-agent-run.txt except 65 and 74.
    source_text(path)  excerpt(path, a, b)   files in assets/source: cli.py, docker-compose.yml,
        docker-shell.sh, Dockerfile, docker-entrypoint.sh, .gitignore, README.md, semantic_splitter.py,
        pyproject.toml, out.txt, input-datasets/books/Tolminc Cheese.txt (= STORY_PATH),
        pipenv-branch/cli.py, tolminc-before-85bba32/input-datasets/books/Tolminc Cheese.txt.
        Never-shown source lines raise (Tolminc line 1, cli.py 61-71 and 435, README 263,
        semantic_splitter.py 102-105).
    build_row(row) -> (text, time|None)   a BuildKit "=>" / Compose "✔" row cut at 58 + its time
    column_view(lines, ("PORTS", "NAMES"))   docker ps / docker images rows sliced to columns
    split_prompt(line) -> (prompt, cmd) | None
    STORY_TEXT (7,808 chars)  SENTENCES (108, from "The first thing")  CHAR_SPANS (24 windows)
    RECURSIVE_SPANS (35, a faithful re-implementation of RecursiveCharacterTextSplitter: count and
    first chunks match cli-container/13 and 15)  COUNTS {...}  QUESTION  QUESTION_CHAT  BOOK
    FIRST_ID  STANDIN_ID  EMBED_MODEL  LLM_MODEL  PROJECT_ID  KEY_FILE

Colours (BRIEF.md, binding)
    LAPTOP GREY · CLOUD (= GOOGLE = HUB) BLUE · CTR TEAL · SYSTEM ORANGE · DATA (= VENV) GREEN ·
    TOOL PURPLE · ERR RED · TURN YELLOW · COST (= KEY) GOLD · LOOKUP PINK · INK white ·
    FUTURE GREY (dashed: L06/L08 and S15's concepts)
Running example
    P_HOME P_WS P_REPO P_ZIP P_ZIP_REPO (laptop)   P_CTR (part 1) P_CTR2 (part 2) P_G5 (the G5 demo)
    CTR_TITLE "container · llm-rag-cli"

README tracker (top-left, YELLOW)
    tracker(key, step=None)  keys Prereq Account Run Chunk Embed Load Query Chat Semantic Agents;
        step None = no step lit yet ("TRACKER Embed (no step lit yet)"). SECTIONS[key]
    self.play(tr.goto(k))     caption_extra(tr, on) -> anim (" · extra" on/off); both cross-fade
        the caption in place (tracker() returns a CrossFadeTracker) and rebind tr.caption
    tr = switch_section(self, tr, "Chunk", 1)   old tracker lifts away, new one drops in
    lref("A16–A19") = lecture_ref(5, ...) top right;  lref_swap(scene, old, "A19–A22") -> new

Terminal helpers (Terminal from explainer.devops: .type .print .run .clear .find .last)
    term(prompt=P_REPO, rows=12, title=None, container=False, top=None)  12.6 wide, 22 pt, 65
        chars a row, bottom at BOTTOM (or top edge at `top`); container=True: TEAL frame, title
        "container · llm-rag-cli", prompt P_CTR unless given
    enter_container(t, prompt=P_CTR) / leave_container(t, prompt=P_REPO) -> list of animations
    resize(scene, t, rows, keep=None, anchor="bottom")   grow/shrink, bottom (or top) edge fixed
    bare_prompt(scene, t)   type_cmd(scene, t, cmd): use it for every typed command. A long line
        folds with fold_cmd(text, 65, first_prefix) -> (rows, hard): " \\" + 4-space indent, at
        the last space outside quotes, else inside a "..." string (python -c one-liners stay
        valid), never mid-word unless a token is longer than a row (URLs); the command starts
        under the prompt when that folds better
    cd_prompt(scene, t, new_prompt, color=LAPTOP)  second_terminal(scene, prompt, rows=7, top=2.75)
    session(scene, t, cap, *spec, wrap=False, colors=None) -> {file line: mobject}
    print_build(scene, t, rows)  BuildKit / Compose rows, times as GREY tags (.time_tag)
    beside(mob, t, line) / pin(scene, line, mob) / unpin(scene, line, mob)   tags that scroll
    col_box(line, a, b) box over character columns  bracket(mobs, text) left-margin bracket
    under(mob) strike(mob) ring(mob)

Panels and cards
    src_panel(path, a, b, focus=None, size=22, shown=None, suffix=None, wrap=None)  code_panel from
        assets/source, header "shown · lines a–b"; shown: "pipenv · cli.py", "96d5fd7 · Tolminc
        Cheese.txt", "Tolminc Cheese.txt"; wrap=True breaks every line > 65 chars at spaces into
        GREY ↪ rows (" · line N wrapped"), wrap={41: ["of cheese"]} breaks before substrings.
        .bar(file_line, colour) -> line bars (not added) .span(file_line, sub) .rows_of(n)
    log_panel(lines, header, width=12.6)  PANEL: plain mono rows (.rows)
    readme_chip(where, phrase) one line (<= 9 wide)   readme_card(where, lines)
    excerpt_chip(sub, header, line=None)  exact sub-string chip   cmd_chip(cmd, note_=None)
    editor_inset(panel)  note(text) GREY caption  sans(text)  fix_chip(text)
    turn_card(rows, header="your turn")  rows: "cmd" (mono), (cmd, "extra"), (cmd, note), Prose("…")
    card_rows(items, header=None)  LookFor(items, title="with your key, look for") .write_item(i)
    table_card(headers, rows)   check_card(purpose) GREY "an extra Python check · …" card
    what_if_frame(width=12.9, top=2.6, bottom=-3.58) RED dashed frame "what if · just watch", built
        in place (holds a full-width terminal of <= 12 rows; tracker band stays free) (.frame .title .note)
    ponder_at(scene, question, seconds=8, y=-2.2) the ponder card in the lower third (returns it;
        FadeOut it at the start of the next block)
    Counter(text="chunks", value=0) .count_to(n, run_time) -> anim  .freeze()
    at_bottom(mob, y=BOTTOM)   puts a panel's bottom on the terminal line (a code strip)

Tags (keep their size in rescale): your_turn() extra_tag() illustration_tag(note_=None)
    our_illustration_tag(note_=None) recording_tag() ("at the time of recording") recorded_tag(s)
    staff_tag() ("recorded · the staff's vectors (68e0bde)") nokey_tag() ("real run · no key")
    standin_tag() example_tag() ("lecture example") concept_tag() (GREY dashed) preview_tag()
    ("preview · L06") erratum_tag(note_=None) fix_tag() ("fix · not in the repo") differ_tag()
    cost_tag(s="your project pays · per use") harmless_tag() expected_tag() grey_tag(s)
    build_badge(k) time_tag(t) stamp(text, color)

Glyphs (small; sizes w x h)
    key_glyph(h=0.3, name=None) GOLD key (+ mono name) · key_outline() dashed · padlock() ·
    toggle(on) API switch · signpost(lines) PINK board · shelf(caption, w) · file_row(name) ·
    ghost_file(name) · person() · pencil() · gear(r, color) · door() · clock_glyph() ·
    coin_glyph(r) GOLD coin · calendar_glyph() · cylinder(w, h, color=CTR) database (.top .body) ·
    page_stack(w, h) GREEN pages · chunk_card(w, h) GREEN card · vec_glyph(n, color) fan of
    arrows · ruler_glyph(w) · scissors_glyph(h) · seismo_glyph(w) (the three chunkers, PURPLE) ·
    gears_glyph() "RAG code" · model_box(name, w, h, color=CLOUD, sub=None) (grows to fit name +
    mono sub-label; "\n" splits the name) · answer_bars(n, w) ·
    question_card(text=QUESTION) PINK · table_glyph() SQL table · chat_window(url, w, h)
    (.field .answer) · prompt_card(n=10) PINK question + GREEN chunk rows (.question .cards)

Set pieces: Piece = VGroup + named parts (as in L03/L04)
    Sizes below are W x H at scale 1. RagMap, ComposeView, what_if_frame and PromptStack are built
    in place (frame coordinates, laid out for the full frame): show them where they are (their
    bounding box includes hidden parts, so .move_to() would shift them off-centre; use .shift() or
    ComposeView.fit_top()). The others are built centred near ORIGIN: .move_to(...) them. A part
    not shown yet is a member at opacity 0: it moves and scales with the piece. show=(...) names
    the parts visible at first (default: all). self.play(*piece.parts_in("a", "b")) fades parts
    in; self.play(*piece.parts_out("a")) fades them back to 0 (they stay members);
    piece.reveal(scene, *names) / piece.hide(scene, *names) do the same with their own play.
    self.play(piece.dim_to(0.3)) / self.play(piece.undim()). Never piece.set_opacity(...), never
    FadeOut a member: FadeOut the whole piece. rescale(k): self.play(piece.animate.rescale(k)).
    Methods return ANIMATIONS (play them) or MOBJECTS (not added: FadeIn them yourself).
    Geometry is read from members, so it follows moves. piece.attach(scene, *mobs) fades mobs in
    and makes them members (they move with the piece); piece.detach(scene, *mobs) fades them out;
    piece.glyph_only() -> a text-free copy (a thumbnail you may .scale() freely).

    V1 RagMap(show=ALL)  the two lanes, in place: boxes, arrows and labels x -6.33..6.29,
       y -2.41..2.05; lane cards reach y 3.23 (lane1, x -4.6..0.8) and -3.55 (lane2, x -4.4..1.8).
       Boxes (.item(name), names in RagMap.BOXES): books (knowledge base), chunking (PURPLE ruler
       box), embedding (tall BLUE box across both lanes), vectors (GREEN arrows), database (TEAL
       cylinder across both lanes), user, query (PINK arrow), prompt (GREEN "prompt + query +
       context"), llm (BLUE), answer (BLUE chip). Arrows: a_books a_chunks a_embed a_vectors (top),
       a_question a_query a_qdb a_context a_prompt a_answer (bottom); label parts lab_<box>.
       Groups: RagMap.TOP RagMap.BOTTOM RagMap.LABELS. Regions: reg_indexing reg_retrieval
       reg_generation (dashed outlines) + tab_indexing tab_retrieval tab_generation (tags in the
       gap between the lanes, at their region's edge; hide the tabs before the flags appear: they
       share that gap; tab_generation is two rows "Augmentation & / Generation").
       lane1 / lane2 (README.md line 5 / line 9 cards). Flags: flag_chunk flag_embed flag_load
       (in the gap under the top lane) flag_query flag_chat (above the bottom lane).
       Locations: loc_cli (TEAL frame "CLI container"), loc_google (two BLUE dashed outlines,
       tags "Google · Vertex AI" under the embedding box and "Google" over the LLM), loc_chroma
       (TEAL frame "Chroma container"), loc_disk (GREY folder "on your laptop" + PINK route under
       the cylinder). Show the locations without the labels/lanes (they share space).
       .light(name, color=TURN) / .unlight(name) -> anim   .tick(name) -> GREEN tick (not added)
       .pulse_lane("top"|"bottom", color) -> anim (a flash along the lane, lit on its arrows only)
    MiniMap(center=MINI_CENTER)  glyph-only copy, 3.3 x 1.45 (a plain VGroup: FadeIn/FadeOut it,
       mm.animate.move_to(MINI_ABOVE_STRIP)). .light(name) -> anim (unlights the previous; names
       as RagMap.BOXES) .unlight() -> anim .tick(name) -> GREEN tick (not added: FadeIn it, then
       mm.add(tick) so it moves with the map) .items[name] .frame
    V2 ComposeView(show=ALL)   in place, 12.9 x 5.1 (x -6.35..6.51, y -2.33..2.79): laptop zone (GREY,
       rows llm-rag/ secrets/ docker-volumes/ chromadb/, the GOLD key under secrets/, the street
       door :8000), CLI box (TEAL: /app and /secrets windows, GREEN /.venv, two `$` slots, GREEN
       `build: .` chip), Chroma box (TEAL: cylinder, /data window, :8000 port chip, name tag
       llm-rag-chromadb above it), the TEAL rail llm-rag-network, PINK routes (app, secrets, data,
       port "8000:8000"), PINK phone book llm-rag-chromadb → 172.19.0.2, BLUE Vertex AI cloud +
       dashed line with the riding key, BLUE Docker Hub shelf with an empty llm-rag-cli slot and
       the chromadb/chroma:latest image chip.
       Parts: zone row_repo row_secrets row_volumes key door cli venv slots build chroma name
       port_chip rail plug_cli plug_chroma depends route_app route_secrets route_data route_port
       book cloud vertex key_ride hub hub_slot image
       .pulse(route) -> anim ("app" | "secrets" | "data" | "port"; nothing travels)
       .blink(route) -> anim (folder and window blink at once)
       .fill_slots() / .empty_slots() -> [anims]   .light(box) / .unlight(box) -> anim
       .remove_cli() / .remove_chroma() / .new_boxes() -> [anims]   .row(name) .window(name)
       .fit_top(k=0.84) -> self: squeezes the shapes to k of the height (text, windows, chips and
       glyphs keep their size, so the width stays) and re-lays what touches, to x -6.38..6.48,
       y -1.38..3.07, just above the 3-row strip or a 3-line code strip (S04's "V2 owns the
       top"): cv.fit_top() before showing it, or self.play(cv.animate.fit_top()).
    V3 Ribbon(view=(STORY_START, STORY_START + 1000), width=12.4, breaks=False, blocks=True)
       the story as GREEN word blocks (no text), 12.4 x 0.24 at ORIGIN; ~1,000 chars span 12.4
       (350 chars ≈ 4.34, 20 ≈ 0.25). STORY_START = 27 (line 3; lines 1-2 never shown).
       blocks=False: one solid bar (the whole story: Ribbon(view=(0, 7808), blocks=False)).
       breaks=True: GREY ticks at paragraph gaps (tall) and line breaks (short).
       .x_of(i) .ruler(a, b) PURPLE window with ticks .band(a, b, color=TURN) .cut(i) cut line
       .callout(a, b) mono text of the story (<= 60 chars; never before char 27) in a card
       .span_card(a, b, color=DATA) a chunk card spanning a..b (recursive chunks)
    V4 VectorSketch(r=1.6, sphere=True)  2r x 2r: a 2-D drawing of a sphere (circle + dashed equator) with
       an origin dot. .point(deg, length) .arrow(deg, length=0.85, color=DATA) .cluster(deg, n,
       spread=10, length=0.8) .arc(a, b, radius=0.45) .unit_circle(frac=1.0) dashed .sector(a, b)
       PINK beam — all return mobjects (not added). sphere=False: only the origin (2-D sketches).
       CellBar(width=11)  11 x 1.3: 3,072 cells (48 groups of 64) with the first 256 GREEN (part keep);
       labels part "labels"; .cut() -> [anims] the other 2,816 fall away
    V5 RecordTable(n=3, ids=None)  12 x 2.24 (n=3; +0.62 per row): header + rows of four cells
       id / document / metadata / embedding; parts header, row0..; .cell(i, col) .column(col)
       .col_box(col) (not added)
       collection_glyph(name, count=None)  3.5 x 1.6 GREEN slabs + mono name (+ count) (.stack
       .name .count)   ScanColumn(n=28)  3.9 x 3.8 (rows, PINK pointer, "rows read" Counter):
       .walk(to=8248, run_time) -> [anims]; .counter.freeze() before it leaves
       HnswGraph(layers=(3, 7, 15), width=6.4)  6.4 x 2.35, layered graph (our illustration of
       HNSW: tag it); parts layer0.. links; .hop(target=None) -> (pointer, [anims]): FadeIn the
       pointer, play the anims one by one, FadeOut the pointer (scene-owned)
    V6 RankColumn(scores=(0.57, 0.77, 0.43, 0.93))  5.2 x 2.7: GREEN cards + scores (mono 24),
       header "similarity (lecture)", "bigger = closer" arrow; .scores_in() -> [anims, one per
       row] .sort() -> anim .k_line(k=2) -> YELLOW line + "top K" (not added; reaches 1.1 left of
       the cards) .flip() -> [anims] (1 − s, header "cosine distance (Chroma)", arrow turns over)
       DotCloud(n=1000)  9.9 x 3.4 (our illustration: tag it): .mask("all"|"book"|"italian") ->
       [anims] .nearest(k, level=None) -> dots .beam(dots) -> PINK lines (not added); parts dots,
       standin, tolminc_label
       StageStrip(stages=STAGES_A32, dashed=False)  11.9 x 1.7: boxes in a row; part filter;
       .slide_filter(before=2) -> anim   .boxes[i] .arrows
    V7 PromptStack()  in place, x -6.3..6.07, y -1.36..1.31: system / query / context blocks
       (4.3 wide, 22 pt) + brace "final prompt", BLUE LLM box with its model chip, a feed arrow,
       cables. Parts: system query context brace llm model feed ghost cable_loose cable_in lock
       (the last four hidden unless named in show=). .ghost() -> [anims] (system block -> dashed
       SYSTEM_INSTRUCTION ghost) .unplug() / .plug() -> [anims]   .block(name) .llm_box
    V8 Seismograph(start=8, n=9)  12.4 x 2.5 (tiles 0.95 tall at y 0, spikes above): sentence
       tiles (number + first words), gaps' distances (our illustration: GAP_VALUES, chapter
       headings spike; tag it); parts tiles spikes curve threshold (YELLOW dashed line at the
       95th percentile GAP_THRESHOLD of the whole story, label at the free end).
       .bracket(i) -> ±1 window bracket (not added) .spikes_in() -> anim .rise(scene)
       .above() -> gap indices .cuts() -> [anims] (tiles part at spikes above the line; spikes
       and curve follow; .cut_marks scene-owned) .sentence_card(i) -> GREY card (not added)
    CostDial(radius=0.55, caption="cost") 1.1 x 1.4 (from L01; GOLD dial without digits)
       .run(scene, turns, seconds) .freeze() before it leaves

Capture folder names (assets/terminal): laptop, cli-container, recorded-embeddings, gotchas,
expected (never: capture-only).
"""

from __future__ import annotations

import re
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
    Animation,
    AnimationGroup,
    Arc,
    Arrow,
    Brace,
    Circle,
    Create,
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
    Polygon,
    Rectangle,
    RoundedRectangle,
    Sector,
    ShowPassingFlash,
    Square,
    Succession,
    Text,
    Transform,
    ValueTracker,
    VGroup,
    VMobject,
    always_redraw,
    linear,
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
LAPTOP = S.GREY          # your laptop: ~/AC215, llm-rag/, secrets/, outputs/, docker-volumes/, browser, :8000
CLOUD = S.BLUE           # Google Cloud: project, IAM, Vertex AI; the embedding model, the LLM, its answer
GOOGLE = CLOUD
HUB = CLOUD              # Docker Hub
CTR = S.TEAL             # containers and images, the cylinder, the llm-rag-network rail, container ports
SYSTEM = S.ORANGE        # the image's system parts (Debian base, apt, Python 3.12.15)
DATA = S.GREEN           # chunk cards, vectors, records, collections; the recipe files, /.venv
VENV = DATA
TOOL = S.PURPLE          # docker, Compose, git, uv, docker-shell.sh; ruler, scissors, seismograph
ERR = S.RED              # errors and "avoid this"
TURN = S.YELLOW          # your turn, the tracker, look here now, the top-K line, the threshold line
COST = S.GOLD            # every Vertex AI call; the key glyph
KEY = COST
LOOKUP = S.PINK          # the question and its vector, beams, filter edges, name lookup, routes
INK = S.WHITE
DIMMED = S.GREY
FUTURE = S.GREY          # dashed: L06 agents, L08 fine-tuning, S15's concepts

# ------------------------------------------------------------------ the running example
USER, HOST = "student", "laptop"
P_HOME = f"{USER}@{HOST}:~$"
P_WS = f"{USER}@{HOST}:~/AC215$"
P_REPO = f"{USER}@{HOST}:~/AC215/llm-rag$"
P_ZIP = f"{USER}@{HOST}:~/AC215-zip$"
P_ZIP_REPO = f"{USER}@{HOST}:~/AC215-zip/llm-rag-main$"
P_CTR = "app@92c5bfd26089:/app$"           # part 1 (laptop/07)
P_CTR2 = "app@390fe47a277a:/app$"          # part 2, after the restart (laptop/23)
P_G5 = "app@2af936bbf5b9:/app$"            # the G5 demo (gotchas/01)
CTR_TITLE = "container · llm-rag-cli"

PROJECT_ID = "your-project-id"
KEY_FILE = "llm-service-account.json"
QUESTION = "How is tolminc cheese made?"              # cli.py:318, README.md:184
QUESTION_CHAT = "How is tolminc cheese made??"        # cli.py:372 (two question marks)
BOOK = "The Complete Book of Cheese"
STORY_PATH = "input-datasets/books/Tolminc Cheese.txt"
FIRST_ID = "1021665fac86c5a5-0"
STANDIN_ID = "8440accaceb0ce96-6"
EMBED_MODEL = "gemini-embedding-001"
LLM_MODEL = "gemini-3.1-flash-lite"
DIM, FULL_DIM = 256, 3072
CHUNK_SIZE, CHUNK_OVERLAP, RECURSIVE_OVERLAP = 350, 20, 200
COUNTS = {"books": 11, "story_chars": 7808, "char-split": 8248, "recursive-split": 14228,
          "tolminc_char": 24, "tolminc_recursive": 35, "book": 1355, "italian": 64,
          "italian_tolminc": 0, "tolminc_word": 3}

# ------------------------------------------------------------------ layout
BOTTOM = -3.5                    # terminal bottom edge (fixed when it grows or shrinks)
TRACK_LEFT, TRACK_TOP = -6.5, 3.5
TERM_W, TERM_PT = 12.6, 22
MINI_CENTER = np.array([4.88, -2.8, 0])          # bottom right, nothing else down there
MINI_ABOVE_STRIP = np.array([4.88, -0.6, 0])     # bottom right, above a 3-row strip (bottom -1.33)

# ------------------------------------------------------------------ README trackers
SECTIONS = {
    # README.md of dlops-io/llm-rag @ e17a39f (script.md "TRACKER")
    "Prereq": ("Prerequisites", ["Docker installed", "Clone repo"]),
    "Account": ("Service Account", ["Open console", "Create account", "Grant roles", "Keys tab",
                                    "Add JSON key", "Rename, save"]),
    "Run": ("Run Container", ["cd llm-rag", "Set GCP_PROJECT", "Run script"]),
    "Chunk": ("Chunk", ["Visualizer", "Char split", "Recursive split"]),
    "Embed": ("Embed", ["Embed char", "Embed recursive"]),
    "Load": ("Load", ["Load char", "Load recursive", "Chroma UI"]),
    "Query": ("Query", ["Query char", "Query recursive"]),
    "Chat": ("Chat", ["Chat char", "Chat recursive", "Chat tool"]),
    "Semantic": ("Semantic Chunking", ["Semantic run"]),
    "Agents": ("Agents (L06)", ["Run agent"]),
}


def place_tracker(tr):
    tr.shift(np.array([TRACK_LEFT - tr.get_left()[0], TRACK_TOP - tr.get_top()[1], 0]))
    return tr


def _in_first_half(t: float) -> float:
    return smooth(min(1.0, 2 * t))


def _out_second_half(t: float) -> float:
    return smooth(max(0.0, 2 * t - 1))


def _out_early(t: float) -> float:
    return smooth(min(1.0, t / 0.55))


def _in_late(t: float) -> float:
    return smooth(max(0.0, (t - 0.45) / 0.55))


def _swap_caption(tr, new, steady: bool) -> list:
    """Cross-fade tr's caption into the Text `new`, in place next to tr.dots, and make `new`
    tr.caption at once (it takes the old caption's slot in tr; the old one leaves tr, so its
    FadeOut takes it off the scene for good). A Transform between two captions of different
    lengths scrambled the letters for 0.3-0.6 s, and from the blank caption the label flew in from
    a point. steady=True (the same step, ' · extra' on or off): the new caption fades in over the
    first half on top of the old one, then the old one fades out, so the shared 'step k of N: …'
    never dims. steady=False (another step): the old one fades out, then the new one in, with a
    short overlap, so the two never show at full strength together. Returns the two animations
    (the caller wraps them)."""
    old = tr.caption
    inked = any(m.has_points() for m in old.get_family())
    new.next_to(tr.dots, RIGHT, buff=0.25)
    if steady and inked:
        new.align_to(old, LEFT)          # the shared prefix exactly on the old one's glyphs
    if old in tr.submobjects:
        i = tr.submobjects.index(old)
        tr.remove(old)
        tr.insert(i, new)
    else:
        tr.add(new)
    tr.caption = new
    if not inked:                        # from the blank caption: the label fades in where it stays
        return [FadeOut(old), FadeIn(new)]
    if steady:
        return [FadeIn(new, rate_func=_in_first_half), FadeOut(old, rate_func=_out_second_half)]
    return [FadeOut(old, rate_func=_out_early), FadeIn(new, rate_func=_in_late)]


class CrossFadeTracker(ReadmeTracker):
    """explainer.devops.ReadmeTracker whose goto(k) cross-fades the caption in place (see
    _swap_caption) instead of Transforming it; the dots move as before. Same contract: goto
    returns one AnimationGroup, tr.k / tr.caption / tr.dots / tr._caption(k) as before (S13's
    tracker_to builds on them)."""

    def goto(self, k: int, run_time: float = 0.5):
        anims = []
        for i, d in enumerate(self.dots, start=1):
            col = self.hi_color if i == k else (S.GREY if i < k else S.GREY_DARK)
            anims.append(d.animate.set_color(col).scale((1.5 if i == k else 1.0) / (d.width / 0.12)))
        anims += _swap_caption(self, self._caption(k), steady=(k == self.k))
        self.k = k
        return AnimationGroup(*anims, run_time=run_time)


def tracker(key: str, step: int | None = None):
    """The README tracker for section `key` (see SECTIONS), top-left, at `step` (None: no step
    lit yet, an empty caption). A CrossFadeTracker: its captions cross-fade."""
    section, steps = SECTIONS[key]
    t = CrossFadeTracker(section, steps)
    if step:
        t.set_step(step)
    t.key = key
    return place_tracker(t)


def caption_extra(tr, on: bool = True):
    """The tracker caption with (or without) ' · extra' while a command the README doesn't have
    is on screen: one AnimationGroup that cross-fades the caption in place (the shared
    'step k of N: …' stays put and never dims; see _swap_caption) and makes the new Text
    tr.caption."""
    k = tr.k
    s = f"step {k} of {len(tr.steps)}: {tr.steps[k - 1]}" if k else ""
    if on:
        new = label((s + " · extra") if s else "extra", tr.size, tr.hi_color,
                    t2c={"· extra": S.GREY, "extra": S.GREY} if not s else {"· extra": S.GREY})
    else:
        new = label(s or " ", tr.size, tr.hi_color)
    return AnimationGroup(*_swap_caption(tr, new, steady=True))


def switch_section(scene, old, key: str, step: int | None = 1, run_time: float = 0.8):
    """The tracker switches to another README section: the old one lifts away, the new one drops
    in. Returns the new tracker (on screen)."""
    new = tracker(key, step)
    scene.play(FadeOut(old, shift=UP * 0.25), FadeIn(new, shift=DOWN * 0.25), run_time=run_time)
    return new


def lref(slides: str) -> VGroup:
    """The GREY 'Lecture 5 · slides A16–A19' tag, top right (A = main deck, B = supplement). One
    slide reads 'slide B78': lecture_ref's single-slide test only knows digits, so lettered slide
    numbers are handled here (explainer/ waits until L02–L04 are released)."""
    if re.fullmatch(r"[A-Z]\d+", slides.split("·")[0].strip()):
        g = tag(f"Lecture 5 · slide {slides}", S.GREY)
        return g.move_to([6.6 - g.width / 2, 3.6 - g.height / 2, 0])
    return lecture_ref(5, slides)


def lref_swap(scene, old, slides: str, run_time: float = 0.5) -> VGroup:
    """Replace the lecture tag (old may be None). Returns the new tag (on screen). The old tag
    fades out, then the new one fades in (as S02 does), in the same run_time: faded at once,
    the two texts overlapped mid-swap (final review: "Lecture 55 · slides A86 A17")."""
    new = lref(slides)
    if old is None:
        scene.play(FadeIn(new), run_time=run_time)
    else:
        scene.play(Succession(FadeOut(old), FadeIn(new)), run_time=run_time)
    return new


# ------------------------------------------------------------------ captures and sources
NEVER_CAPTURE = {   # file lines the script never shows (a real person's name)
    "cli-container/10-chunk-char-split.txt": {36},
    "cli-container/13-chunk-recursive-split.txt": {36},
    "cli-container/15-x-recursive-chunks.txt": {3},
    "recorded-embeddings/01-load-char-split.txt": {145},
    "recorded-embeddings/02-load-recursive-split.txt": {156},
    "recorded-embeddings/07-x-metadata-per-book.txt": set(range(12, 22)),
    "recorded-embeddings/08-x-filter-counts.txt": {6, 12},
    "laptop/05-x-ls.txt": {6, 7},
    "recorded-embeddings/05-x-get.txt": {6},
    "cli-container/70-x-get-after-restart.txt": {6},
}
ONLY_CAPTURE = {"expected/out-txt-agent-run.txt": {65, 74}}     # every other line is never shown
CUT_OK = {("laptop/05-x-ls.txt", 6): "origin/HEAD)",
          ("recorded-embeddings/05-x-get.txt", 6): "]",
          ("cli-container/70-x-get-after-restart.txt", 6): "]"}
NEVER_SOURCE = {STORY_PATH: {1}, "cli.py": set(range(61, 72)) | {435}, "README.md": {263},
                "semantic_splitter.py": set(range(102, 106))}


class Capture:
    """One captured command. .cmd (as typed, without "$ "), .lines (its output), .exit (status),
    .first (file line number of .lines[0]), .header (the '#' provenance line of expected/*)."""

    def __init__(self, name: str, cmd: str, lines: list[str], exit_code: int, first: int = 2,
                 header: str = ""):
        self.name, self.cmd, self.lines, self.exit = name, cmd, lines, exit_code
        self.first, self.header = first, header

    def _guard(self, n: int):
        if n in NEVER_CAPTURE.get(self.name, ()) or \
                (self.name in ONLY_CAPTURE and n not in ONLY_CAPTURE[self.name]):
            raise ValueError(f"{self.name}: line {n} is never shown (script.md 'Names on screen')")

    def _raw(self, n: int) -> str:
        i = n - self.first
        if not 0 <= i < len(self.lines):
            raise IndexError(f"{self.name}: line {n} is not output (output is lines "
                             f"{self.first}–{self.first + len(self.lines) - 1})")
        return self.lines[i]

    def line(self, n: int) -> str:
        """File line n (1-based, as in the script's TERM(file: n))."""
        self._guard(n)
        return self._raw(n)

    def cut(self, n: int, marker: str) -> str:
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
        return s[:i + len(marker)]

    def at(self, *spec, ellipsis: str = "…") -> list[str]:
        """Output lines by FILE line number: at(2, (11, 12), "…", 52) -> line 2, lines 11-12, a
        '…' line, line 52. A string is inserted as is ("" means the ellipsis)."""
        out: list[str] = []
        for s in spec:
            if isinstance(s, str):
                out.append(s or ellipsis)
            elif isinstance(s, int):
                out.append(self.line(s))
            else:
                a, b = s
                out += [self.line(n) for n in range(a, b + 1)]
        return out

    def join(self, *ns: int) -> str:
        """File lines joined into one (a long line the capture terminal wrapped at 80 columns,
        e.g. join(7, 8)); print it with wrap=True."""
        return "".join(self.line(n) for n in ns)

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
            for k in range(a, b + 1):
                self._guard(k - 1 + self.first)
            out += self.lines[a - 1:b]
            last = b
        return out


FOLDERS = ("laptop", "cli-container", "recorded-embeddings", "gotchas", "expected")


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
    """assets/terminal/<folder>/<name>.txt parsed; capture("10", "cli-container") finds
    10-chunk-char-split.txt; capture("laptop/07") works too. Fails loudly if missing: never show
    an output that wasn't captured."""
    if folder is None:
        folder, _, name = name.rpartition("/")
        if not folder:
            raise ValueError("capture(name, folder): name the folder")
    if folder == "capture-only":
        raise ValueError("capture-only/ is plumbing: never shown")
    p = _find_capture(name, folder)
    text = p.read_bytes().decode("utf-8")              # no newline translation: lines as sed counts them
    raw = [ln.rstrip("\r").split("\r")[-1].expandtabs(8) for ln in text.rstrip("\n").split("\n")]
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
    return Capture(f"{folder}/{p.name}", cmd, raw, code, off, header)


_PROMPT = re.compile(r"^((?:\(\w+\) )?[\w.-]+@[\w.-]+:[^\s$#]*[$#]|#)(?: (.*))?$")


def split_prompt(line: str):
    """'app@92c5bfd26089:/app$ exit' -> ('app@92c5bfd26089:/app$', 'exit'); not a prompt -> None."""
    m = _PROMPT.match(line.rstrip())
    if not m:
        return None
    return m.group(1), (m.group(2) or "").strip()


def source_text(name: str) -> str:
    return (SOURCE / name).read_text(encoding="utf-8")


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


def excerpt(name: str, first: int, last: int, cut_comments: bool = False) -> str:
    """Lines first..last (1-based, inclusive) of a tutorial file in assets/source, for
    code_panel(..., first_line=first). Never-shown lines raise."""
    lines = source_text(name).split("\n")
    if last > len(lines):
        raise IndexError(f"{name} has {len(lines)} lines")
    bad = NEVER_SOURCE.get(name, set()) & set(range(first, last + 1))
    if bad:
        raise ValueError(f"{name}: lines {sorted(bad)} are never shown (script.md 'Names on screen')")
    out = [ln.expandtabs(4) for ln in lines[first - 1:last]]
    if cut_comments:
        out = [cut_comment(s) for s in out]
    return "\n".join(out)


_TIME = re.compile(r"^\d+(\.\d+)?s$")


def build_row(row: str, width: int = 58) -> tuple[str, str | None]:
    """A BuildKit "=>" row or a Compose "✔" row -> (the row without its time field, cut to
    `width` with '…', the time, e.g. '20.2s', or None). '[+] Building 81.5s (13/13) FINISHED'
    keeps its time in the text."""
    r = row.rstrip()
    parts = r.rsplit(None, 1)
    time = None
    head = r.lstrip()
    if len(parts) == 2 and _TIME.match(parts[1]) and (head.startswith("=>") or head.startswith("✔")):
        r, time = parts[0].rstrip(), parts[1]
    if len(r) > width:
        r = r[:width - 1] + "…"
    return r, time


def column_view(lines: list[str], cols=("PORTS", "NAMES"), gap: int = 3) -> list[str]:
    """`docker ps` / `docker images` lines (header first) sliced to the named columns (the
    script's "column view"): each field is the capture's own text, cut at the header's column
    bounds (right-aligned values keep their alignment), joined with `gap` spaces."""
    head = lines[0]
    names = [m.group(0) for m in re.finditer(r"\S+(?: \S+)*", head)]
    starts = [head.index(n) for n in names]
    spans = {}
    for k, n in enumerate(names):
        a = starts[k]
        b = starts[k + 1] if k + 1 < len(names) else max(len(s) for s in lines)
        spans[n] = (a, b)
    out = []
    for s in lines:
        fields = []
        for c in cols:
            a, b = spans[c]
            if c != names[0]:          # right-aligned numbers may start before the header
                prev_end = spans[names[names.index(c) - 1]][0]
                a2 = a
                while a2 > prev_end and s[a2 - 1:a2] not in ("", " "):
                    a2 -= 1
                a = a2
            fields.append(s[a:b].rstrip())
        out.append((" " * gap).join(f.ljust(spans[c][1] - spans[c][0]) if i == 0 else f
                                    for i, (f, c) in enumerate(zip(fields, cols))).rstrip())
    return out


# ------------------------------------------------------------------ the story and its chunks
STORY_TEXT = source_text(STORY_PATH)                     # 7,808 characters
STORY_START = STORY_TEXT.index("\n", STORY_TEXT.index("\n") + 1) + 1   # after line 2: never show line 1
SENTENCES = re.split(r"(?<=[.?!])\s+", STORY_TEXT[STORY_TEXT.index("The first thing"):])


def _char_spans(n: int, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[tuple[int, int]]:
    """CharacterTextSplitter(separator='', strip_whitespace=False): windows of `size`, stride
    size - overlap (cli.py:184-189). 24 for the story."""
    out, a = [], 0
    while True:
        out.append((a, min(a + size, n)))
        if a + size >= n:
            return out
        a += size - overlap


def _recursive_chunks(text: str, size: int = CHUNK_SIZE, overlap: int = RECURSIVE_OVERLAP) -> list[str]:
    """Our re-implementation of RecursiveCharacterTextSplitter(chunk_size=350) with the library's
    defaults (separators \\n\\n, \\n, space, ''; keep_separator at the start; overlap 200; strip).
    Not the tutorial's code: it reproduces its count (35) and first chunks (cli-container/15)."""

    def split(t, sep):
        if not sep:
            return list(t)
        parts = re.split(f"({re.escape(sep)})", t)
        out = [parts[i] + parts[i + 1] for i in range(1, len(parts), 2)]
        if len(parts) % 2 == 0:
            out += parts[-1:]
        return [s for s in [parts[0], *out] if s]

    def merge(splits):
        docs, cur, total = [], [], 0
        for d in splits:
            if total + len(d) > size:
                if cur:
                    j = "".join(cur).strip()
                    if j:
                        docs.append(j)
                    while total > overlap or (total + len(d) > size and total > 0):
                        total -= len(cur[0])
                        cur = cur[1:]
            cur.append(d)
            total += len(d)
        j = "".join(cur).strip()
        if j:
            docs.append(j)
        return docs

    def rec(t, seps):
        out, good = [], []
        sep, new = seps[-1], []
        for i, s in enumerate(seps):
            if s == "":
                sep = s
                break
            if s in t:
                sep, new = s, seps[i + 1:]
                break
        for s in split(t, sep):
            if len(s) < size:
                good.append(s)
            else:
                if good:
                    out += merge(good)
                    good = []
                out += rec(s, new) if new else [s]
        if good:
            out += merge(good)
        return out

    return rec(text, ["\n\n", "\n", " ", ""])


def _spans_of(text: str, chunks: list[str]) -> list[tuple[int, int]]:
    out, pos = [], 0
    for c in chunks:
        a = text.find(c, pos)
        out.append((a, a + len(c)))
        pos = a + 1
    return out


CHAR_SPANS = _char_spans(len(STORY_TEXT))
RECURSIVE_SPANS = _spans_of(STORY_TEXT, _recursive_chunks(STORY_TEXT))

# ------------------------------------------------------------------ small text helpers
def sans(s: str, size: float = CAPTION, color: str = INK, **kw) -> Text:
    """CMU Sans Serif text (box labels, card lines)."""
    return label(s, size, color, font=SANS, **kw)


def note(s: str, color: str = S.GREY, size: float = CAPTION) -> Text:
    """A GREY caption (serif, 20 pt)."""
    return label(s, size, color)


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
def _l05_make_room(self, scene, n_new: int, run_time: float = 0.35) -> None:
    """Terminal._make_room for L05 (rebound below; same signature, run_time and end state).
    explainer/devops.py fades the scrolled-off lines out WHILE shifting them up a row, so for
    2-5 frames they are drawn over the title bar and above the top border (final review F1:
    8:11.95 in S05, 26:41.2 in S14). Here they fade out in place in the first 40% of the same
    single play, then the staying lines shift up: nothing crosses the top border and no row is
    drawn over a fading one. explainer/ stays untouched this round (its fix is planned apart)."""
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


Terminal._make_room = _l05_make_room


def term(prompt: str = P_REPO, rows: int = 12, title: str | None = None, container: bool = False,
         top: float | None = None, width: float = TERM_W, size: float = TERM_PT) -> Terminal:
    """The house terminal (full width, 22 pt, 65 characters a row), bottom edge at BOTTOM, or its
    top edge at `top`. container=True: inside the CLI container (TEAL frame, title
    "container · llm-rag-cli", prompt P_CTR unless `prompt` is given)."""
    if container and prompt == P_REPO:
        prompt = P_CTR
    ttl = title or (CTR_TITLE if container else "laptop")
    t = Terminal(prompt=prompt, width=width, rows=rows, size=size, title=ttl)
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
    """Fold a typed line (prompt included) into rows of at most `limit` characters, as
    Terminal.fold does (" \" at the end of a row, the next row indented 4), but quote-aware:
    it breaks at the last space outside quotes that fits (before an option when one is in the
    row's last quarter), else at a space inside a "double-quoted" shell string outside any
    inner '...' literal (bash drops the backslash-newline there, so a python -c one-liner stays
    valid), else at a space inside a '...' string, and only with no space at all in reach
    mid-token (hard = True). Returns (rows, hard)."""
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
                    title: str = "laptop · second terminal", run_time: float = 0.6) -> Terminal:
    """A second terminal slides in with its top at `top`: it opens in the home folder (P_HOME,
    the "~" flashing YELLOW, GREY caption "new terminal: cd here first"), then the prompt reads
    `prompt` (a bare prompt line). Returns the terminal (on screen)."""
    t = term(P_HOME, rows=rows, title=title, top=top)
    scene.play(FadeIn(t, shift=DOWN * 0.3), run_time=run_time)
    ln = bare_prompt(scene, t)
    tilde = glyph_range(ln, P_HOME.index("~"), P_HOME.index("~") + 1)
    cap = note("new terminal: cd here first")
    beside(cap, t, ln, buff=0.5)
    scene.play(Indicate(tilde, color=TURN, scale_factor=1.4), FadeIn(cap), run_time=0.8)
    scene.wait(0.6)
    scene.play(FadeOut(cap), run_time=0.3)
    _drop_bare(scene, t)
    t.set_prompt(prompt)
    ln2 = bare_prompt(scene, t)
    scene.play(Indicate(glyph_range(ln2, prompt.index(":") + 1, len(prompt) - 1),
                        color=TURN, scale_factor=1.05), run_time=0.6)
    return t


def session(scene, t: Terminal, cap: Capture, *spec, wrap: bool = False, type_time=None,
            colors: dict | None = None, out_time: float = 0.5):
    """Replay an interactive capture (laptop/07, 23, gotchas/01): `spec` as in Capture.at. A line
    that starts with a prompt sets t's prompt and types its command (exactly as captured); a
    prompt line with no command makes a bare prompt; other lines print. colors: {file line:
    colour}. Returns {file line: the mobject printed or typed for it}."""
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
    around the text (glyph_box) hides nothing."""
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
    """The x of column 0's left edge in a mono_line, measured from its glyphs: the median over
    non-space characters of (glyph centre − (k + 0.5) · cell width). Falls back to the strut."""
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
    """A box over character columns a..b (exclusive) of a mono_line, blank cells included (the
    CLI container's empty PORTS cell). Not added.
    The columns are measured from the glyphs (grid_x0): the strut's left edge sits about 0.6 of a
    cell left of column 0, which put every box short of its text (Bugbot, PR #29)."""
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


def our_illustration_tag(note_: str | None = None) -> VGroup:
    """'our illustration' (pictures that look like data but are not measurements); note_="of
    HNSW" -> 'our illustration of HNSW'."""
    return grey_tag("our illustration" + (f" {note_}" if note_ else ""))


def recording_tag() -> VGroup:
    return grey_tag("at the time of recording")


def recorded_tag(s: str = "recorded") -> VGroup:
    return grey_tag(s)


def staff_tag() -> VGroup:
    return grey_tag("recorded · the staff's vectors (68e0bde)")


def nokey_tag() -> VGroup:
    return grey_tag("real run · no key")


def standin_tag() -> VGroup:
    return grey_tag("stand-in query · a stored story chunk's vector")


def example_tag() -> VGroup:
    return grey_tag("lecture example")


def concept_tag(s: str = "concept · not in the tutorial's code") -> VGroup:
    """The GREY dashed tag of S15 (and of any concept with no code here)."""
    g = tag(s, S.GREY)
    dashed = DashedVMobject(g.box, num_dashes=int(g.box.width * 9), dashed_ratio=0.55)
    dashed.set_stroke(S.GREY, 2)
    fill = g.box.copy().set_stroke(width=0)
    out = VGroup(fill, dashed, g.text)
    out.box, out.text = fill, g.text
    return _keep(out)


def preview_tag() -> VGroup:
    return grey_tag("preview · L06")


def erratum_tag(note_: str | None = None) -> VGroup:
    return grey_tag("erratum" + (f" · {note_}" if note_ else ""))


def fix_tag() -> VGroup:
    return grey_tag("fix · not in the repo")


def differ_tag() -> VGroup:
    return grey_tag("your numbers will differ")


def cost_tag(s: str = "your project pays · per use") -> VGroup:
    return _keep(tag(s, COST))


def harmless_tag() -> VGroup:
    return grey_tag("harmless")


def expected_tag() -> VGroup:
    return grey_tag("expected")


def build_badge(k: int, words: bool = True) -> VGroup:
    """TEAL badge for BuildKit's [k/6]: a circled k, and with words=True "build step k"."""
    b = step_badge(k, CTR)
    if not words:
        return _keep(b)
    return _keep(VGroup(b, sans(f"build step {k}", CAPTION, CTR)).arrange(RIGHT, buff=0.12))


def stamp(text: str, color: str = ERR, size: float = TAG, angle: float = 0.08) -> VGroup:
    """An outlined, slightly rotated stamp."""
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


# ------------------------------------------------------------------ panels and cards
_LANG = {".py": "python", ".toml": "toml", ".sh": "bash", ".md": "markdown", ".yaml": "yaml",
         ".yml": "yaml", ".json": "json", ".html": "html", ".txt": "text", ".lock": "toml"}


def _lang(path: str) -> str:
    p = Path(path)
    if p.name == "Dockerfile":
        return "docker"
    if p.name in (".gitignore", ".dockerignore"):
        return "text"
    return _LANG.get(p.suffix, "text")


def shown_path(name: str) -> str:
    """The path as the viewer sees it: pipenv-branch/cli.py -> "pipenv · cli.py"; the old story
    -> "96d5fd7 · Tolminc Cheese.txt"; the story -> "Tolminc Cheese.txt"."""
    if name.startswith("pipenv-branch/"):
        return f"pipenv · {name.split('/', 1)[1]}"
    if name.startswith("tolminc-before-85bba32/"):
        return f"96d5fd7 · {Path(name).name}"
    if name.startswith("input-datasets/books/"):
        return Path(name).name
    return name


def _looks_path(p: str) -> bool:
    return bool(re.search(r"\.[A-Za-z]\w*$", p)) or ("/" in p and " " not in p)


def _header_text(text: str, size: float = CAPTION) -> VGroup:
    """'cli.py · lines 183–194' -> mono path + serif rest. A prefix ('pipenv · cli.py · lines
    62–64') keeps the prefix serif and the path mono."""
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


def _with_header(panel: VGroup, text: str, size: float = CAPTION) -> VGroup:
    """Replace a code_panel's header with `text`."""
    header = _header_text(text, size)
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


def src_panel(name: str, first: int, last: int | None = None, cut_comments: bool = False,
              focus=None, size: float = 22, width: float | None = None,
              shown: str | None = None, suffix: str | None = None, wrap=None,
              language: str | None = None) -> VGroup:
    """code_panel quoting assets/source/<name> lines first..last, header "shown · lines a–b"
    (+ " · comment cut", + " · line N wrapped", + " · suffix"). wrap=True: every line longer
    than 65 chars breaks at spaces into GREY ↪ rows; wrap={41: ["of cheese"]}: line 41 breaks
    before those substrings. .rows_of(file_line) -> code row indices; .bar(file_line, colour)
    -> VGroup of line bars (not added); .span(file_line, sub) -> glyphs; .source_name .first"""
    last = first if last is None else last
    raw = excerpt(name, first, last)
    lines = (excerpt(name, first, last, True) if cut_comments else raw).split("\n")
    cut = cut_comments and lines != raw.split("\n")
    rows, rows_of, wrapped = [], {}, []
    for k, ln in enumerate(lines):
        n = first + k
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
    shown = shown or shown_path(name)
    p = code_panel("\n".join(rows), shown, first, language or _lang(name), font_size=size,
                   width=width)
    where = f"line {first}" if first == last else f"lines {first}–{last}"
    extra = []
    if cut:
        extra.append("comment cut")
    extra += [f"line {n} wrapped" for n in wrapped]
    if suffix:
        extra.append(suffix)
    _with_header(p, " · ".join([shown, where, *extra]))
    for n, ks in rows_of.items():          # GREY ↪ marks
        for k in ks[1:]:
            try:
                code_span(p.code, k, "↪").set_color(S.GREY)
            except (ValueError, IndexError):
                pass
    if focus is not None:
        keep = {focus} if isinstance(focus, int) else set(focus)
        for n, ks in rows_of.items():
            if n not in keep:
                for k in ks:
                    if k < len(p.code.code_lines):
                        p.code.code_lines[k].set_opacity(0.3)
    p.source_name, p.first, p.rows_map = name, first, rows_of
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


def log_panel(lines: list[str], header: str, width: float = TERM_W, size: float = CAPTION,
              color: str = OUTPUT) -> VGroup:
    """PANEL: plain mono rows (a recorded line, a diff) on a dark rounded panel with a GREY
    header above. Rows longer than the panel are cut with '…'. .rows (mono_lines) .frame .header"""
    max_chars = int((width - 0.5) / cell_width(size))
    rows = VGroup()
    pitch = line_pitch(size)
    for i, s in enumerate(lines):
        s, col = (s, color) if isinstance(s, str) else s
        s = s if len(s) <= max_chars else s[:max_chars - 1] + "…"
        ln = mono_line(s, size, col)
        ln.shift(np.array([0, -i * pitch, 0]) - ln.strut.get_corner(UP + LEFT))
        rows.add(ln)
    h = len(lines) * pitch + 0.4
    frame = RoundedRectangle(width=width, height=h, corner_radius=0.15, stroke_color=S.GREY_DARK,
                             stroke_width=2).set_fill(PANEL, 1)
    frame.move_to(rows.get_center()).align_to(rows, LEFT).shift(LEFT * 0.25)
    frame.shift(UP * (rows.get_top()[1] + 0.2 - frame.get_top()[1]))
    head = _header_text(header).next_to(frame, UP, buff=0.1).align_to(frame, LEFT).shift(RIGHT * 0.12)
    g = VGroup(frame, rows, head)
    g.frame, g.rows, g.header = frame, rows, head
    return g.move_to(ORIGIN)


def readme_chip(where: str, phrase: str | None = None, size: float = CAPTION,
                max_w: float = 9.0) -> VGroup:
    """A one-line README chip: GREY `where` ("README.md · line 48") and the quoted phrase in
    white. Fails if wider than max_w (shorten the phrase). .frame .where .phrase"""
    w = _header_text(where, size)
    parts = [w]
    ph = None
    if phrase:
        ph = label(f"“{phrase}”", size, INK)
        parts.append(ph)
    row = VGroup(*parts).arrange(RIGHT, buff=0.25)
    fr = box(row.width + 0.4, row.height + 0.24, S.GREY, fill=S.BG, fill_opacity=0.92, radius=0.1)
    fr.move_to(row)
    g = VGroup(fr, row)
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
        return mono(s[1:-1], size, color)
    return label(str(s), size, color)


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
    line, headed `header` ("cli.py · line 178 (excerpt)"). Pass the full `line` (excerpt(...) or
    cap.line(n)) to check the sub-string. .chip .text .header"""
    if line is not None and sub not in line:
        raise ValueError(f"{sub!r} is not in {line!r}")
    c = chip(sub, frame, size=size, text_color=color, font=MONO, fill_opacity=0.1)
    h = _header_text(header, size).next_to(c, UP, buff=0.08).align_to(c, LEFT).shift(RIGHT * 0.08)
    g = VGroup(c, h)
    g.chip, g.text, g.header = c, c.text, h
    return _keep(g)


def editor_inset(panel, title: str = "in your editor") -> VGroup:
    """A GREY editor window (title bar + frame) around a code panel. .frame .title .panel"""
    pad, bar_h = 0.18, 0.42
    w, h = panel.width + 2 * pad, panel.height + 2 * pad + bar_h
    fr = RoundedRectangle(width=w, height=h, corner_radius=0.12, stroke_color=S.GREY,
                          stroke_width=2).set_fill(S.BG, 1)
    fr.move_to(panel).shift(UP * bar_h / 2)
    bar = Line(fr.get_corner(UP + LEFT) + DOWN * bar_h, fr.get_corner(UP + RIGHT) + DOWN * bar_h,
               color=S.GREY, stroke_width=1.5)
    t = label(title, CAPTION, S.GREY).move_to(fr.get_top() + DOWN * bar_h / 2)
    g = VGroup(fr, bar, t, panel)
    g.frame, g.title, g.panel = fr, t, panel
    return g


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
    serif row. The YELLOW ▶ your turn tag sits on the top-right corner (.tag). .frame .rows .tag"""
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
    """A GREY card of rows (fix cards, clean-up cards, checklists): each item is a str (serif;
    "`mono`" in backticks), (str, colour), or a mobject. .frame .rows .header; rows write in with
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


def check_card(purpose: str, title: str = "an extra Python check · in the study guide") -> VGroup:
    """The GREY card that stands for a multi-line Python extra (its code is never shown):
    header `title`, one row with its purpose. .frame .rows .header"""
    return card_rows([purpose], header=title)


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
    """The "with your key, look for" card (and "if it fails (with your key)"): a GREY caption card
    (never terminal-styled), one row per item: (text, where) -> "text · where" (where in GREY,
    e.g. "cli.py · line 240"); text in backticks is mono. The frame is built for every row from
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
    """S05's RED dashed frame around a "what if" demo, so it never looks like the viewer's own
    terminal. Built in place (frame coordinates, centred on x = 0): y from `bottom` to `top`, so
    the tracker band above stays free and a full-width terminal of up to 12 rows (top at
    strip_top(12) = 2.19) fits inside. The title tag straddles the top border at the left, an
    optional GREY note at the right. .frame .title .note"""
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
              width: float = 10.2) -> VGroup:
    """The ponder card (pause_and_ponder's look) in the lower third, opaque, its timer draining
    over `seconds`. The picture above stays visible. Returns the card (FadeOut it at the start
    of the next SAY block)."""
    card = ponder_card(question, width=width).move_to([0, y, 0])
    card[0].set_fill(S.BG, 1)
    if card.get_bottom()[1] < -3.55:
        card.shift(UP * (-3.55 - card.get_bottom()[1]))
    scene.play(FadeIn(card, scale=0.95), run_time=0.6)
    bar = card[3]
    scene.play(bar.animate(rate_func=linear).become(bar.copy().scale(0.001, about_point=bar.get_start())),
               run_time=seconds)
    return card


class Counter(VGroup):
    """A counter "chunks: 24": a label and a number (with thousands commas) driven by a
    ValueTracker. .count_to(n, run_time) -> animation; .freeze() before it leaves. .num .label"""

    def __init__(self, text: str | None = "chunks", value: float = 0, color: str = INK,
                 size: float = 26, **kw):
        super().__init__(**kw)
        self.tracker = ValueTracker(value)
        self.num = DecimalNumber(value, num_decimal_places=0, group_with_commas=True,
                                 font_size=size, color=color)
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


# ------------------------------------------------------------------ glyphs
def key_glyph(h: float = 0.3, color: str = KEY, name: str | None = None) -> VGroup:
    """The service-account key: a GOLD key (its content is never drawn). name=KEY_FILE adds the
    file name (mono 20, GOLD) to its right. .key .name"""
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


def clock_glyph(r: float = 0.13, color: str = COST) -> VGroup:
    c = Circle(radius=r, stroke_color=color, stroke_width=2.5)
    h1 = Line(ORIGIN, UP * r * 0.65, color=color, stroke_width=2.5)
    h2 = Line(ORIGIN, RIGHT * r * 0.5, color=color, stroke_width=2.5)
    return _keep(VGroup(c, h1, h2))


def coin_glyph(r: float = 0.12, color: str = COST) -> VGroup:
    """A GOLD coin (embedded, stored, paid for); no digits."""
    c = Circle(radius=r, stroke_color=color, stroke_width=2.5).set_fill(color, 0.35)
    inner = Circle(radius=r * 0.6, stroke_color=color, stroke_width=1.5)
    return _keep(VGroup(c, inner))


def calendar_glyph(h: float = 0.42, color: str = S.GREY) -> VGroup:
    """A small calendar (trained before this story)."""
    w = h * 1.0
    page = RoundedRectangle(width=w, height=h, corner_radius=0.04, stroke_color=color,
                            stroke_width=2.5).set_fill(color, 0.1)
    band = Rectangle(width=w, height=h * 0.24, stroke_width=0).set_fill(color, 0.6)
    band.align_to(page, UP)
    rings = VGroup(*[Line(UP * 0.0, UP * h * 0.16, color=color, stroke_width=3)
                     .move_to(page.get_top() + RIGHT * dx * w) for dx in (-0.25, 0.25)])
    grid = VGroup(*[Dot(radius=0.025, color=color).move_to(page.get_center() + np.array([(i - 1) * w * 0.25, (j - 0.7) * h * 0.22, 0]))
                    for i in range(3) for j in range(2)])
    return _keep(VGroup(page, band, rings, grid))


def padlock(h: float = 0.36, color: str = CLOUD) -> VGroup:
    """A padlock (weights unchanged; an IAM role). .body .shackle"""
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


def toggle(on: bool = False, color: str = CLOUD, w: float = 0.56) -> VGroup:
    """An "API enabled" switch: a pill with a knob (left = off, GREY; right = on, BLUE). .knob .pill"""
    h = w * 0.52
    pill = RoundedRectangle(width=w, height=h, corner_radius=h / 2, stroke_color=color if on else S.GREY,
                            stroke_width=2.5).set_fill(color if on else S.GREY, 0.35 if on else 0.1)
    knob = Circle(radius=h * 0.36, stroke_width=0).set_fill(INK if on else S.GREY, 1)
    knob.move_to(pill.get_center() + RIGHT * (w / 2 - h / 2) * (1 if on else -1))
    g = VGroup(pill, knob)
    g.pill, g.knob, g.on = pill, knob, on
    return _keep(g)


def signpost(lines: list[str], color: str = LOOKUP, size: float = CAPTION,
             post_h: float = 0.45, point=RIGHT) -> VGroup:
    """A PINK signpost: an arrow-shaped board (mono text) on a post, pointing RIGHT (or LEFT).
    .board .text .post .foot .root() .tip()"""
    txt = VGroup(*[mono(s, size, color) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    w, h, tipw = txt.width + 0.4, txt.height + 0.26, 0.3
    x0, y0 = -w / 2, -h / 2
    board = Polygon([x0, y0, 0], [x0 + w, y0, 0], [x0 + w + tipw, 0, 0], [x0 + w, -y0, 0], [x0, -y0, 0],
                    stroke_color=color, stroke_width=2.5).set_fill(S.BG, 0.95)
    txt.move_to(board).align_to(board, LEFT).shift(RIGHT * 0.2)
    px = x0 + 0.3
    post = Line([px, y0, 0], [px, y0 - post_h, 0], color=color, stroke_width=4)
    foot = Line([px - 0.18, y0 - post_h, 0], [px + 0.18, y0 - post_h, 0], color=color, stroke_width=4)
    g = VGroup(post, foot, board, txt)
    if np.allclose(point, LEFT):
        board.flip(UP, about_point=board.get_center())
        post.shift(RIGHT * (w + tipw - 0.6))
        foot.shift(RIGHT * (w + tipw - 0.6))
    g.board, g.text, g.post, g.foot = board, txt, post, foot
    g.root = lambda: foot.get_center()
    g.tip = lambda: board.get_right() if not np.allclose(point, LEFT) else board.get_left()
    return _keep(g)


def shelf(caption: str | None = "Docker Hub", w: float = 2.6, color: str = HUB,
          size: float = CAPTION) -> VGroup:
    """A shelf (a registry): a board on two short legs, caption under it. .board .caption"""
    b = Line(LEFT * w / 2, RIGHT * w / 2, color=color, stroke_width=5)
    legs = VGroup(Line(LEFT * (w / 2 - 0.15), LEFT * (w / 2 - 0.15) + DOWN * 0.22, color=color, stroke_width=3),
                  Line(RIGHT * (w / 2 - 0.15), RIGHT * (w / 2 - 0.15) + DOWN * 0.22, color=color, stroke_width=3))
    g = VGroup(b, legs)
    g.caption = None
    if caption:
        c = label(caption, size, color).next_to(legs, DOWN, buff=0.08)
        g.add(c)
        g.caption = c
    g.board = b
    return _keep(g)


def person(color: str = S.GREY, h: float = 0.62) -> VGroup:
    """A person glyph (you, the user, a librarian): a head over shoulders."""
    head = Circle(radius=h * 0.2, stroke_color=color, stroke_width=3).set_fill(color, 0.25)
    body = Arc(radius=h * 0.38, start_angle=0, angle=PI, stroke_color=color, stroke_width=3)
    body.close_path()
    body.set_fill(color, 0.2)
    head.next_to(body, UP, buff=0.04)
    return _keep(VGroup(body, head))


def pencil(h: float = 0.55, color: str = TURN) -> VGroup:
    """A pencil glyph (an edit in your editor), tip at bottom-left."""
    w = h * 0.22
    shaft = Rectangle(width=w, height=h, stroke_color=color, stroke_width=2.5).set_fill(color, 0.25)
    tip = Polygon(shaft.get_corner(DOWN + LEFT), shaft.get_corner(DOWN + RIGHT),
                  shaft.get_bottom() + DOWN * w * 1.1, stroke_color=color, stroke_width=2.5).set_fill(color, 0.6)
    g = VGroup(shaft, tip).rotate(-PI / 4)
    g.tip_point = lambda: tip.get_vertices()[2]
    return _keep(g)


def gear(r: float = 0.24, color: str = S.GREY) -> VGroup:
    """A small gear."""
    teeth = VGroup(*[Rectangle(width=r * 0.38, height=r * 0.42, stroke_width=0).set_fill(color, 1)
                     .move_to(UP * r * 0.98).rotate(k * TAU / 8, about_point=ORIGIN) for k in range(8)])
    ring_ = Circle(radius=r * 0.8, stroke_width=0).set_fill(color, 1)
    hole = Circle(radius=r * 0.32, stroke_width=0).set_fill(S.BG, 1)
    return _keep(VGroup(teeth, ring_, hole))


def gears_glyph(color: str = TOOL, r: float = 0.24) -> VGroup:
    """Three gears in a cluster (A12's "RAG code")."""
    g1 = gear(r, color)
    g2 = gear(r * 0.75, color).move_to(g1.get_center() + np.array([r * 1.55, r * 0.75, 0]))
    g3 = gear(r * 0.65, color).move_to(g1.get_center() + np.array([r * 1.35, -r * 1.05, 0]))
    return _keep(VGroup(g1, g2, g3).move_to(ORIGIN))


def file_row(name: str, color: str = INK, glyph_color: str = S.GREY, size: float = CAPTION) -> VGroup:
    """A file (or folder, name ending in '/') glyph + its mono name. .glyph .text .name"""
    g = folder_glyph(0.22, glyph_color) if name.endswith("/") else file_glyph(0.28, glyph_color)
    t = mono(name, size, color).next_to(g, RIGHT, buff=0.12)
    row = VGroup(g, t)
    row.glyph, row.text, row.name = g, t, name
    return _keep(row)


def ghost_file(name: str = KEY_FILE, color: str = S.GREY) -> VGroup:
    """A dashed GREY file that doesn't exist (yet)."""
    g = DashedVMobject(file_glyph(0.28, color)[0], num_dashes=18).set_stroke(color, 2)
    t = mono(name, CAPTION, color).next_to(g, RIGHT, buff=0.12)
    row = VGroup(g, t)
    row.glyph, row.text, row.name = g, t, name
    return _keep(row)


def door(w: float = 0.34, h: float = 0.56, color: str = LAPTOP) -> VGroup:
    """A door glyph (the published host port on the laptop): frame + knob. .frame"""
    fr = RoundedRectangle(width=w, height=h, corner_radius=0.04, stroke_color=color,
                          stroke_width=3).set_fill(color, 0.18)
    knob = Dot(fr.get_right() + LEFT * 0.08, radius=0.035, color=color)
    g = VGroup(fr, knob)
    g.frame = fr
    return g


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
    g.frame = VGroup(bottom, sides, disks, top)      # the strokes (light() recolours these)
    return g


def page_stack(w: float = 0.72, h: float = 0.92, color: str = DATA, n: int = 3) -> VGroup:
    """A stack of GREEN pages (the knowledge base). .front"""
    pages = VGroup()
    for k in range(n):
        p = RoundedRectangle(width=w, height=h, corner_radius=0.05, stroke_color=color,
                             stroke_width=2.5).set_fill(_mix(color, 0.16), 1)
        p.shift(np.array([(n - 1 - k) * 0.09, (n - 1 - k) * 0.09, 0]))
        pages.add(p)
    front = pages[-1]
    lines = VGroup(*[Line(LEFT * w * 0.32, RIGHT * w * (0.32 if i % 3 else 0.12), color=color,
                          stroke_width=2, stroke_opacity=0.7).move_to(front.get_center() + UP * (h * 0.3 - i * h * 0.15))
                     for i in range(5)])
    for ln in lines:
        ln.align_to(front, LEFT).shift(RIGHT * w * 0.14)
    g = VGroup(pages, lines).move_to(ORIGIN)
    g.front = front
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


def ruler_glyph(w: float = 1.0, color: str = TOOL) -> VGroup:
    """char-split's tool: a PURPLE ruler with ticks."""
    h = w * 0.24
    body = RoundedRectangle(width=w, height=h, corner_radius=0.03, stroke_color=color,
                            stroke_width=2.5).set_fill(color, 0.25)
    ticks = VGroup(*[Line(UP * 0, DOWN * h * (0.5 if k % 2 else 0.3), color=color, stroke_width=2)
                     .move_to(body.get_corner(UP + LEFT) + RIGHT * w * (k + 1) / 9, aligned_edge=UP)
                     for k in range(8)])
    return _keep(VGroup(body, ticks))


def scissors_glyph(h: float = 0.5, color: str = TOOL) -> VGroup:
    """recursive-split's tool: PURPLE scissors, blades to the right."""
    r = h * 0.2
    c1 = Circle(radius=r, stroke_color=color, stroke_width=3).move_to(np.array([-h * 0.55, h * 0.24, 0]))
    c2 = Circle(radius=r, stroke_color=color, stroke_width=3).move_to(np.array([-h * 0.55, -h * 0.24, 0]))
    b1 = Line(c1.get_right() + DOWN * r * 0.3, np.array([h * 0.6, -h * 0.12, 0]), color=color, stroke_width=4)
    b2 = Line(c2.get_right() + UP * r * 0.3, np.array([h * 0.6, h * 0.12, 0]), color=color, stroke_width=4)
    pivot = Dot(radius=0.03, color=color).move_to(np.array([-h * 0.08, 0, 0]))
    return _keep(VGroup(c1, c2, b1, b2, pivot))


def seismo_glyph(w: float = 1.0, color: str = TOOL) -> VGroup:
    """semantic-split's tool: a PURPLE seismograph (a framed trace with one tall spike)."""
    h = w * 0.55
    fr = RoundedRectangle(width=w, height=h, corner_radius=0.05, stroke_color=color,
                          stroke_width=2.5).set_fill(color, 0.12)
    ys = [0, 0.1, -0.08, 0.06, 0.42, -0.3, 0.05, -0.06, 0.08, 0]
    pts = [np.array([-w * 0.42 + i * w * 0.84 / (len(ys) - 1), y * h, 0]) for i, y in enumerate(ys)]
    trace = VMobject(stroke_color=color, stroke_width=2.5).set_points_as_corners(pts)
    return _keep(VGroup(fr, trace))


def model_box(name: str = "LLM", w: float = 1.3, h: float = 0.9, color: str = CLOUD,
              sub: str | None = None, size: float = CAPTION) -> VGroup:
    """A model box (the embedding model, the LLM): BLUE rounded box, sans name ("\\n" splits
    rows), optional mono sub-label inside under it. .frame .name .sub"""
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
    g.frame, g.name = fr, nm
    return g


def answer_bars(n: int = 3, w: float = 2.4, color: str = S.GREY, h: float = 0.12) -> VGroup:
    """Placeholder answer bars (no words): n rounded bars, the last one shorter."""
    bars = VGroup(*[RoundedRectangle(width=w * (0.55 if k == n - 1 else (1.0 - 0.08 * (k % 2))), height=h,
                                     corner_radius=h / 2, stroke_width=0).set_fill(color, 0.75)
                    for k in range(n)])
    bars.arrange(DOWN, aligned_edge=LEFT, buff=h * 1.1)
    return bars


def question_card(text: str = QUESTION, color: str = LOOKUP, font: str | None = MONO,
                  size: float = CAPTION) -> VGroup:
    """The PINK question card (made of words). .box .text"""
    return _keep(chip(text, color, size=size, font=font, fill_opacity=0.12))


def table_glyph(rows: int = 4, cols: int = 3, w: float = 1.7, h: float = 1.1,
                color: str = S.GREY) -> VGroup:
    """A SQL table glyph: a grid with a filled header row."""
    fr = Rectangle(width=w, height=h, stroke_color=color, stroke_width=2.5).set_fill(color, 0.06)
    head = Rectangle(width=w, height=h / rows, stroke_width=0).set_fill(color, 0.35).align_to(fr, UP)
    hl = VGroup(*[Line(fr.get_left(), fr.get_right(), color=color, stroke_width=1.5)
                  .shift(UP * (h / 2 - k * h / rows)) for k in range(1, rows)])
    vl = VGroup(*[Line(fr.get_top(), fr.get_bottom(), color=color, stroke_width=1.5)
                  .shift(RIGHT * (-w / 2 + k * w / cols)) for k in range(1, cols)])
    return VGroup(fr, head, hl, vl)


def chat_window(url: str = "a chat with an LLM", width: float = 7.0, height: float = 3.8) -> VGroup:
    """A schematic chat page in a GREY browser frame (tag it illustration): an input field at the
    bottom (.field; type the question with a mono text placed in it) and an answer area above
    (.answer, an invisible rectangle). .frame .address .content"""
    w = browser_window(url, width=width, height=height)
    c = w.content
    field = RoundedRectangle(width=c.width - 0.6, height=0.5, corner_radius=0.12,
                             stroke_color=S.GREY, stroke_width=2).set_fill(TERM_BG, 1)
    field.move_to(c.get_bottom() + UP * 0.45)
    ans = Rectangle(width=c.width - 0.6, height=c.height - 1.2, stroke_width=0, fill_opacity=0)
    ans.next_to(field, UP, buff=0.2)
    w.add(field, ans)
    w.field, w.answer = field, ans
    return w


def prompt_card(n: int = 10, w: float = 3.2, color: str = DATA) -> VGroup:
    """V7's one prompt card in the shape of cli.py:388-391: a PINK question row on top, then n
    thin GREEN chunk rows (no text), in a GREEN frame. .frame .question .cards"""
    q = RoundedRectangle(width=w - 0.3, height=0.22, corner_radius=0.08, stroke_width=0).set_fill(LOOKUP, 0.8)
    cards = VGroup(*[RoundedRectangle(width=(w - 0.3) * (0.92 if k % 3 else 1.0), height=0.13,
                                      corner_radius=0.05, stroke_width=0).set_fill(color, 0.65)
                     for k in range(n)])
    col = VGroup(q, *cards).arrange(DOWN, aligned_edge=LEFT, buff=0.07)
    fr = RoundedRectangle(width=w, height=col.height + 0.3, corner_radius=0.12, stroke_color=color,
                          stroke_width=2.5).set_fill(_mix(color, 0.08), 1).move_to(col)
    g = VGroup(fr, col)
    g.frame, g.question, g.cards = fr, q, cards
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
        """show=None/ALL -> every name; a tuple -> those names."""
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


def _tick(color: str = DATA, h: float = 0.28) -> VMobject:
    return check_mark(h, color)


def _restroke(mobs, color, width=None) -> list:
    """Animations recolouring the strokes of `mobs` (lighting a box)."""
    out = []
    for m in mobs:
        out.append(m.animate.set_stroke(color, width) if width else m.animate.set_stroke(color))
    return out


def _tab(text: str, color: str = S.GREY, dashed: bool = False) -> VGroup:
    return concept_tag(text) if dashed else _keep(tag(text, color))


def _tab2(lines, color: str = S.GREY, size: float = TAG) -> VGroup:
    """A tag of two (or more) centred rows (a long phase name). .box .text"""
    t = VGroup(*[label(s, size, color) for s in lines]).arrange(DOWN, buff=0.06)
    b = RoundedRectangle(width=t.width + 0.4, height=t.height + 0.2, corner_radius=0.16,
                         stroke_color=color, stroke_width=2).set_fill(S.BG, 0.92)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return _keep(g)


class _LaneFlash(Animation):
    """ShowPassingFlash along a broken path: `segs` [(start, end), …] in order, the gaps between
    them part of the path's length but never drawn. The flash (time_width of the whole length)
    runs at an even speed; on each segment it shows the part of its window that lies there."""

    def __init__(self, segs, color: str, time_width: float = 0.5, stroke: float = 8, **kw):
        lines = VGroup(*[Line(a, b).set_stroke(color, stroke) for a, b in segs])
        pts = np.array([p for ab in segs for p in ab], dtype=float)
        acc = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))])
        acc = acc / max(acc[-1], 1e-6)
        self.spans = [(acc[2 * i], acc[2 * i + 1]) for i in range(len(segs))]
        self.time_width = time_width
        super().__init__(lines, introducer=True, remover=True, **kw)

    def interpolate_mobject(self, alpha: float) -> None:
        upper = self.rate_func(alpha) * (1 + self.time_width)
        lower = upper - self.time_width
        for seg, start, (s0, s1) in zip(self.mobject.submobjects, self.starting_mobject.submobjects,
                                        self.spans):
            span = max(s1 - s0, 1e-6)
            a = float(np.clip((lower - s0) / span, 0, 1))
            b = float(np.clip((upper - s0) / span, 0, 1))
            if b - a < 1e-4:
                seg.clear_points()            # the window is elsewhere: nothing on this arrow
            else:
                seg.pointwise_become_partial(start, a, b)


# ------------------------------------------------------------------ V1 · two lanes, one database
class RagMap(Piece):
    """V1: the lecture's naïve-RAG pipeline (A16, B5) redrawn with the README's steps.

        m = RagMap(show=RagMap.TOP + RagMap.BOTTOM + RagMap.LABELS).move_to(DOWN * 0.3)
        self.play(*m.parts_in("reg_indexing", "tab_indexing")); self.play(m.light("embedding"))
    """

    BOXES = ("books", "chunking", "embedding", "vectors", "database", "user", "query", "prompt",
             "llm", "answer")
    TOP = ("books", "chunking", "embedding", "vectors", "database",
           "a_books", "a_chunks", "a_embed", "a_vectors")
    BOTTOM = ("user", "query", "prompt", "llm", "answer",
              "a_question", "a_query", "a_qdb", "a_context", "a_prompt", "a_answer")
    LABELS = ("lab_books", "lab_chunking", "lab_embedding", "lab_vectors", "lab_database",
              "lab_user", "lab_query", "lab_question")
    REGIONS = ("reg_indexing", "reg_retrieval", "reg_generation")
    TABS = ("tab_indexing", "tab_retrieval", "tab_generation")
    FLAGS = ("flag_chunk", "flag_embed", "flag_load", "flag_query", "flag_chat")
    LANES = ("lane1", "lane2")
    LOCATIONS = ("loc_cli", "loc_google", "loc_chroma", "loc_disk")

    YT, YB = 1.15, -1.15
    X = {"books": -5.45, "chunking": -3.75, "embedding": -1.75, "vectors": 0.2, "query": 0.2,
         "database": 2.0, "user": -5.45, "prompt": 3.85, "llm": 5.65, "answer": 5.65}

    def __init__(self, show=None, **kw):
        super().__init__(**kw)
        yt, yb, X = self.YT, self.YB, self.X
        names = (self.TOP + self.BOTTOM + self.LABELS + self.REGIONS + self.TABS + self.FLAGS +
                 self.LANES + self.LOCATIONS)
        vis = self._show_set(show, names)
        self._col, self._frames = {}, {}

        def add(name, mob, frames, color):
            self.part(name, mob, name in vis)
            self._frames[name] = frames
            self._col[name] = color
            return mob

        # -- boxes
        books = page_stack(0.72, 0.92).move_to([X["books"], yt, 0])
        add("books", books, [books[0]], DATA)
        ch_box = box(1.15, 0.8, TOOL, fill_opacity=0.12, radius=0.1, stroke=3)
        chunking = VGroup(ch_box, ruler_glyph(0.8)).move_to([X["chunking"], yt, 0])
        chunking[1].move_to(ch_box)
        add("chunking", chunking, [ch_box], TOOL)
        em = box(1.25, 3.3, CLOUD, fill_opacity=0.12, radius=0.14, stroke=3).move_to([X["embedding"], 0, 0])
        add("embedding", em, [em], CLOUD)
        vecs = vec_glyph(3, DATA, 0.55).move_to([X["vectors"], yt, 0])
        add("vectors", vecs, [vecs], DATA)
        db = cylinder(1.25, 2.55).move_to([X["database"], 0, 0])
        add("database", db, [db.frame], CTR)
        user = person(LAPTOP, 0.7).move_to([X["user"], yb, 0])
        add("user", user, [user], LAPTOP)
        q = vec_glyph(1, LOOKUP, 0.6, base=15).move_to([X["query"], yb, 0])
        add("query", q, [q], LOOKUP)
        pr_box = box(1.25, 1.0, DATA, fill_opacity=0.12, radius=0.1, stroke=3)
        pr_txt = VGroup(*[sans(s, CAPTION, INK) for s in ("prompt +", "query +", "context")]) \
            .arrange(DOWN, buff=0.04)
        prompt = VGroup(pr_box, pr_txt.move_to(pr_box)).move_to([X["prompt"], yb, 0])
        add("prompt", prompt, [pr_box], DATA)
        llm = model_box("LLM", 1.05, 0.8).move_to([X["llm"], yb, 0])
        add("llm", llm, [llm.frame], CLOUD)
        ans = _keep(chip("answer", CLOUD, size=CAPTION)).move_to([X["answer"], yb - 1.0, 0])
        add("answer", ans, [ans.box], CLOUD)
        self.boxes = {n: self.parts[n] for n in self.BOXES}

        # -- arrows
        def arr(a, b, color, name):
            m = Arrow(a, b, buff=0.08, color=color, stroke_width=4, max_tip_length_to_length_ratio=0.3,
                      tip_length=0.18)
            self.part(name, m, name in vis)
            return m

        em_l, em_r = em.get_left()[0], em.get_right()[0]
        db_l, db_r = db.get_left()[0], db.get_right()[0]
        arr([books.get_right()[0], yt, 0], [ch_box.get_left()[0], yt, 0], DATA, "a_books")
        arr([ch_box.get_right()[0], yt, 0], [em_l, yt, 0], DATA, "a_chunks")
        arr([em_r, yt, 0], [vecs.get_left()[0], yt, 0], DATA, "a_embed")
        arr([vecs.get_right()[0], yt, 0], [db_l, yt, 0], DATA, "a_vectors")
        arr([user.get_right()[0], yb, 0], [em_l, yb, 0], LOOKUP, "a_question")
        arr([em_r, yb, 0], [q.get_left()[0], yb, 0], LOOKUP, "a_query")
        arr([q.get_right()[0], yb, 0], [db_l, yb, 0], LOOKUP, "a_qdb")
        arr([db_r, yb, 0], [pr_box.get_left()[0], yb, 0], DATA, "a_context")
        arr([pr_box.get_right()[0], yb, 0], [llm.frame.get_left()[0], yb, 0], DATA, "a_prompt")
        arr([X["llm"], llm.frame.get_bottom()[1], 0], [X["answer"], ans.get_top()[1], 0], CLOUD, "a_answer")

        # -- labels (top lane above its boxes, bottom lane under)
        ly_t, ly_b = yt + 0.74, yb - 0.74
        labs = {"lab_books": ("knowledge base", X["books"], ly_t),
                "lab_chunking": ("chunking", X["chunking"], ly_t),
                "lab_embedding": ("embedding model", X["embedding"], 1.92),
                "lab_vectors": ("vectors", X["vectors"], ly_t),
                "lab_database": ("vector database", X["database"], 1.92),
                "lab_user": ("you", X["user"], ly_b),
                "lab_query": ("query vector", X["query"], ly_b)}
        for name, (s, x, y) in labs.items():
            self.part(name, sans(s, CAPTION, S.GREY).move_to([x, y, 0]), name in vis)
        qlab = sans("question", CAPTION, LOOKUP).move_to([(user.get_right()[0] + em_l) / 2, yb + 0.3, 0])
        self.part("lab_question", qlab, "lab_question" in vis)

        # -- regions (B5's three phases) and their tabs, which sit in the gap between the lanes
        #    (just under / over their region's border, never on a box)
        def region(name, x0, x1, y0, y1, tab, tab_at):
            r = box(x1 - x0, y1 - y0, S.GREY, dashed=True, stroke=2.5, radius=0.18)
            r.move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])
            self.part(name, r, name in vis)
            tab.move_to(tab_at(r, tab))
            self.part("tab_" + name[4:], tab, "tab_" + name[4:] in vis)

        region("reg_indexing", -6.45, db_r + 0.45, yt - 0.6, yt + 1.0, _tab("Indexing"),
               lambda r, t: np.array([r.get_left()[0] + 0.2 + t.width / 2,
                                      r.get_bottom()[1] - 0.03 - t.height / 2, 0]))
        region("reg_retrieval", em_l - 0.15, db_r + 0.25, yb - 0.85, yb + 0.6, _tab("Retrieval"),
               lambda r, t: np.array([(em_r + db_l) / 2, r.get_top()[1] + 0.03 + t.height / 2, 0]))
        gtab = _tab2(("Augmentation &", "Generation"))
        region("reg_generation", llm.get_left()[0] - 0.2, llm.get_right()[0] + 0.2, yb - 0.6, yb + 0.6,
               gtab, lambda r, t: np.array([min(r.get_center()[0], 6.45 - t.width / 2),
                                            r.get_top()[1] + 0.03 + t.height / 2, 0]))

        # -- the README's two step titles (lane labels)
        l1 = readme_card("README.md · line 5", ["`Step 1: Chunk -> Embed -> Load`"])
        l1.move_to([-1.9, yt + 1.6, 0])
        self.part("lane1", l1, "lane1" in vis)
        l2 = readme_card("README.md · line 9", ["`Step 2: Query -> Embed -> Retrieve`",
                                                "`-> LLM -> Generate Answer`"])
        l2.move_to([-1.3, yb - 1.75, 0])
        self.part("lane2", l2, "lane2" in vis)

        # -- the README's five steps as flags (YELLOW chips, opaque)
        def flag(name, word, flag_, x, y):
            row = VGroup(sans(word, CAPTION, TURN), mono(flag_, CAPTION, INK)).arrange(RIGHT, buff=0.14)
            fr = box(row.width + 0.36, row.height + 0.22, TURN, fill=S.BG, fill_opacity=0.95, radius=0.12)
            g = _keep(VGroup(fr, row.move_to(fr))).move_to([x, y, 0])
            self.part(name, g, name in vis)

        gy_t, gy_b = yt - 0.83, yb + 0.83
        flag("flag_chunk", "Chunk", "--chunk", X["chunking"] - 0.45, gy_t)
        flag("flag_embed", "Embed", "--embed", X["embedding"] + 0.15, gy_t)
        flag("flag_load", "Load", "--load", X["database"] - 0.1, gy_t)
        flag("flag_query", "Query", "--query", X["query"] + 0.1, gy_b)
        flag("flag_chat", "Chat", "--chat", (X["prompt"] + X["llm"]) / 2, gy_b)

        # -- where each box runs
        cli = box(1.6, 1.55, CTR, dashed=True, stroke=3).move_to([X["chunking"], yt + 0.3, 0])
        cli_t = _keep(tag("CLI container", CTR)).move_to(cli.get_top())
        self.part("loc_cli", VGroup(cli, cli_t), "loc_cli" in vis)
        g1 = box(em.width + 0.4, em.height + 0.35, CLOUD, dashed=True, stroke=3).move_to(em)
        g2 = box(llm.width + 0.35, llm.height + 0.35, CLOUD, dashed=True, stroke=3).move_to(llm.frame)
        g1t = _keep(tag("Google · Vertex AI", CLOUD)).move_to(g1.get_bottom())
        g2t = _keep(tag("Google", CLOUD)).move_to(g2.get_top())
        self.part("loc_google", VGroup(g1, g2, g1t, g2t), "loc_google" in vis)
        chf = box(db.width + 0.4, db.height + 0.4, CTR, dashed=True, stroke=3).move_to(db)
        cht = _keep(tag("Chroma container", CTR)).move_to(chf.get_top())
        self.part("loc_chroma", VGroup(chf, cht), "loc_chroma" in vis)
        fold = folder_glyph(0.34, LAPTOP)
        fl = sans("on your laptop", CAPTION, LAPTOP)
        disk = VGroup(fold, fl).arrange(RIGHT, buff=0.12).move_to([X["database"] + 0.6, yb - 1.25, 0])
        route = DashedLine(db.get_bottom() + DOWN * 0.05, fold.get_left() + LEFT * 0.05, color=LOOKUP,
                           stroke_width=3)
        self.part("loc_disk", VGroup(route, disk), "loc_disk" in vis)

    # -- lighting
    def item(self, name: str):
        return self.parts[name]

    def light(self, name: str, color: str = TURN, width: float = 5):
        return AnimationGroup(*_restroke(self._frames[name], color, width))

    def unlight(self, name: str, width: float = 3):
        return AnimationGroup(*_restroke(self._frames[name], self._col[name], width))

    def tick(self, name: str, color: str = DATA) -> VMobject:
        b = self.parts[name]
        return _tick(color, 0.32).move_to(b.get_corner(UP + RIGHT) + np.array([0.05, 0.05, 0]))

    def pulse_lane(self, lane: str = "top", color: str = TURN, run_time: float = 1.2):
        """A flash running along the lane's arrows (nothing stays behind). It runs the lane at an
        even speed but lights only the arrows: between two arrows it passes behind the box (one
        path through the arrows' end points drew a thick bar across the boxes, through the text
        of the 'prompt + query + context' card). One Animation, as before."""
        names = ("a_books", "a_chunks", "a_embed", "a_vectors") if lane == "top" else \
            ("a_question", "a_query", "a_qdb", "a_context", "a_prompt")
        segs = [(self.parts[n].get_start(), self.parts[n].get_end()) for n in names]
        return _LaneFlash(segs, color, time_width=0.5, run_time=run_time)


class MiniMap(VGroup):
    """V1's glyph-only copy for the corner (3.3 x 1.45), placed at MINI_CENTER.
        mm = MiniMap(); self.play(FadeIn(mm)); self.play(mm.light("chunking"))
    Names as RagMap.BOXES. .light(name) unlights the previous box; .tick(name) -> GREEN tick."""

    def __init__(self, center=MINI_CENTER, **kw):
        super().__init__(**kw)
        k = 0.25
        X, yt, yb = RagMap.X, RagMap.YT * k, RagMap.YB * k
        fr = RoundedRectangle(width=3.3, height=1.45, corner_radius=0.12, stroke_color=S.GREY_DARK,
                              stroke_width=2).set_fill(S.BG, 0.92)
        self.frame = fr
        self.add(fr)
        self.items, self._col = {}, {}

        def put(name, mob, color):
            self.items[name] = mob
            self._col[name] = color
            self.add(mob)

        def at(x, y):
            return np.array([x * k, y, 0])

        put("books", Rectangle(width=0.2, height=0.24, stroke_color=DATA, stroke_width=2.5)
            .set_fill(DATA, 0.3).move_to(at(X["books"], yt)), DATA)
        put("chunking", Rectangle(width=0.29, height=0.2, stroke_color=TOOL, stroke_width=2.5)
            .set_fill(TOOL, 0.25).move_to(at(X["chunking"], yt)), TOOL)
        put("embedding", Rectangle(width=0.31, height=0.83, stroke_color=CLOUD, stroke_width=2.5)
            .set_fill(CLOUD, 0.2).move_to(at(X["embedding"], 0)), CLOUD)
        put("vectors", Rectangle(width=0.2, height=0.16, stroke_color=DATA, stroke_width=2.5)
            .set_fill(DATA, 0.5).move_to(at(X["vectors"], yt)), DATA)
        put("database", cylinder(0.31, 0.62, stroke=2).move_to(at(X["database"], 0)), CTR)
        put("user", Circle(radius=0.08, stroke_color=LAPTOP, stroke_width=2.5).set_fill(LAPTOP, 0.3)
            .move_to(at(X["user"], yb)), LAPTOP)
        put("query", Rectangle(width=0.2, height=0.16, stroke_color=LOOKUP, stroke_width=2.5)
            .set_fill(LOOKUP, 0.5).move_to(at(X["query"], yb)), LOOKUP)
        put("prompt", Rectangle(width=0.39, height=0.25, stroke_color=DATA, stroke_width=2.5)
            .set_fill(DATA, 0.25).move_to(at(X["prompt"], yb)), DATA)
        put("llm", Rectangle(width=0.26, height=0.2, stroke_color=CLOUD, stroke_width=2.5)
            .set_fill(CLOUD, 0.25).move_to(at(X["llm"], yb)), CLOUD)
        put("answer", Rectangle(width=0.22, height=0.1, stroke_color=CLOUD, stroke_width=2)
            .set_fill(CLOUD, 0.5).move_to(at(X["answer"], yb - 0.25)), CLOUD)
        links = VGroup()
        chain_t = ["books", "chunking", "embedding", "vectors", "database"]
        chain_b = ["user", "embedding", "query", "database", "prompt", "llm"]
        for chain, y in ((chain_t, yt), (chain_b, yb)):
            for a, b in zip(chain, chain[1:]):
                links.add(Line([self.items[a].get_right()[0], y, 0], [self.items[b].get_left()[0], y, 0],
                               color=S.GREY, stroke_width=1.5))
        links.add(Line(self.items["llm"].get_bottom(), self.items["answer"].get_top(), color=S.GREY,
                       stroke_width=1.5))
        self.links = links
        self.add_to_back(links)
        self.add_to_back(fr)
        self.lit = None
        self.move_to(center)

    def _strokes(self, name):
        m = self.items[name]
        return [m.frame] if hasattr(m, "frame") else [m]

    def light(self, name: str, color: str = TURN):
        anims = []
        if self.lit and self.lit != name:
            anims += _restroke(self._strokes(self.lit), self._col[self.lit], 2.5)
        anims += _restroke(self._strokes(name), color, 4)
        self.lit = name
        return AnimationGroup(*anims)

    def unlight(self):
        if not self.lit:
            return AnimationGroup()
        anims = _restroke(self._strokes(self.lit), self._col[self.lit], 2.5)
        self.lit = None
        return AnimationGroup(*anims)

    def tick(self, name: str, color: str = DATA) -> VMobject:
        return _tick(color, 0.2).move_to(self.items[name].get_top() + UP * 0.14)


# ------------------------------------------------------------------ V2 · two containers, one network, three windows
class ComposeView(Piece):
    """V2: the laptop folders, the two containers on llm-rag-network, the three bind mounts, the
    published port, the phone book, Vertex AI with the riding key, Docker Hub.

        cv = ComposeView(show=("zone", "row_repo", "row_secrets", "row_volumes")).move_to(UP * 0.4)
        self.play(*cv.parts_in("rail")); self.play(cv.pulse("app"))
    """

    PARTS = ("zone", "row_repo", "row_secrets", "row_volumes", "key", "door", "cli", "venv", "slots",
             "build", "chroma", "name", "port_chip", "rail", "plug_cli", "plug_chroma", "depends",
             "route_app", "route_secrets", "route_data", "route_port", "book", "cloud", "vertex",
             "key_ride", "hub", "hub_slot", "image")

    def __init__(self, show=None, **kw):
        super().__init__(**kw)
        vis = self._show_set(show, self.PARTS)

        def add(name, mob):
            return self.part(name, mob, name in vis)

        # -- the laptop zone
        zf = box(3.1, 4.5, LAPTOP, fill_opacity=0.05, radius=0.16).move_to([-4.8, 0.0, 0])
        zt = sans("laptop · ~/AC215", CAPTION, LAPTOP).move_to([-4.8, 1.98, 0])
        add("zone", VGroup(zf, zt))
        x0 = -6.15
        r1 = file_row("llm-rag/").move_to([0, 1.35, 0], aligned_edge=LEFT).shift(RIGHT * x0)
        r2 = file_row("secrets/").move_to([0, 0.4, 0], aligned_edge=LEFT).shift(RIGHT * x0)
        r3a = file_row("docker-volumes/").move_to([0, -0.6, 0], aligned_edge=LEFT).shift(RIGHT * x0)
        r3b = file_row("chromadb/").move_to([0, -1.1, 0], aligned_edge=LEFT).shift(RIGHT * (x0 + 0.42))
        add("row_repo", r1)
        add("row_secrets", r2)
        add("row_volumes", VGroup(r3a, r3b))
        self.rows = {"repo": r1, "secrets": r2, "volumes": r3a, "chromadb": r3b}
        k = key_glyph(0.28).move_to([x0 + 0.75, 0.0, 0])
        add("key", k)
        dr = door(0.34, 0.56, LAPTOP).move_to([zf.get_right()[0], -1.75, 0])
        dl = mono(":8000", CAPTION, LAPTOP).next_to(dr, LEFT, buff=0.12)
        add("door", VGroup(dr, dl))
        self.door_glyph = dr

        # -- the CLI container
        cb = box(2.9, 2.35, CTR, fill_opacity=0.08, radius=0.16, stroke=3).move_to([-1.2, 1.025, 0])
        ct = sans("CLI container", CAPTION, CTR).move_to(cb.get_corner(UP + LEFT) + np.array([0.15, -0.25, 0]),
                                                         aligned_edge=LEFT)
        w_app = self._window("/app").move_to([-1.85, 1.3, 0])
        w_sec = self._window("/secrets").move_to([-1.85, 0.5, 0])
        cli = VGroup(cb, ct, w_app, w_sec)
        cli.frame = cb
        add("cli", cli)
        venv = VGroup(box(1.0, 0.5, VENV, fill_opacity=0.15, radius=0.08), mono("/.venv", CAPTION, VENV))
        venv[1].move_to(venv[0])
        add("venv", _keep(venv).move_to([-0.42, 1.3, 0]))
        slots = VGroup()
        for x in (-0.65, -0.1):
            sq = Square(0.42).set_fill(LOOKUP, 0).set_stroke(width=0)
            dsh = DashedVMobject(Square(0.42), num_dashes=12).set_stroke(LOOKUP, 2)
            d = mono("$", CAPTION, LOOKUP)
            s = VGroup(sq, dsh, d).move_to([x, 0.5, 0])
            s.fill_sq = sq
            slots.add(_keep(s))
        add("slots", slots)
        self.slot_list = slots
        bld = _keep(chip("build: .", VENV, size=CAPTION, font=MONO, fill_opacity=0.9))
        bld.box.set_fill(_mix(VENV, 0.15), 1)
        add("build", bld.move_to([-1.75, cb.get_bottom()[1], 0]))

        # -- the Chroma container
        hb = box(2.5, 2.35, CTR, fill_opacity=0.08, radius=0.16, stroke=3).move_to([2.7, 1.025, 0])
        ht = sans("Chroma container", CAPTION, CTR).move_to(hb.get_corner(UP + LEFT) + np.array([0.15, -0.25, 0]),
                                                            aligned_edge=LEFT)
        w_data = self._window("/data", w=1.05).move_to([2.05, 0.55, 0])
        cyl = cylinder(0.72, 0.7).move_to([3.3, 0.6, 0])
        chroma = VGroup(hb, ht, w_data, cyl)
        chroma.frame = hb
        add("chroma", chroma)
        self.cyl = cyl
        nm = mono("llm-rag-chromadb", CAPTION, CTR).move_to([2.7, hb.get_top()[1] + 0.19, 0])
        add("name", nm)
        pc = _keep(chip(":8000", CTR, size=CAPTION, font=MONO, fill_opacity=0.9))
        pc.box.set_fill(_mix(CTR, 0.15), 1)
        add("port_chip", pc.move_to([3.45, hb.get_bottom()[1], 0]))
        self.windows = {"app": w_app, "secrets": w_sec, "data": w_data}

        # -- the network
        rail_y = -0.7
        rail = Line([-2.65, rail_y, 0], [3.8, rail_y, 0], color=CTR, stroke_width=7)
        rl = mono("llm-rag-network", CAPTION, CTR).move_to([-1.35, rail_y - 0.28, 0])
        add("rail", VGroup(rail, rl))
        self.rail_line = rail
        add("plug_cli", Line([-0.5, cb.get_bottom()[1], 0], [-0.5, rail_y, 0], color=CTR, stroke_width=4))
        add("plug_chroma", Line([2.75, hb.get_bottom()[1], 0], [2.75, rail_y, 0], color=CTR, stroke_width=4))
        dep = DashedLine([cb.get_right()[0] + 0.05, 1.55, 0], [hb.get_left()[0] - 0.05, 1.55, 0],
                         color=CTR, stroke_width=3)
        dtip = Arrow(dep.get_end() + LEFT * 0.3, dep.get_end(), buff=0, color=CTR, stroke_width=3,
                     tip_length=0.15, max_tip_length_to_length_ratio=0.6)
        dlab = VGroup(sans("depends", CAPTION, CTR), sans("on", CAPTION, CTR)).arrange(DOWN, buff=0.04)
        dlab.move_to([(cb.get_right()[0] + hb.get_left()[0]) / 2, 1.0, 0])
        add("depends", VGroup(dep, dtip, dlab))

        # -- the mounts and the published port (PINK routes)
        self.routes = {}
        ra = _poly([(r1.get_right()[0] + 0.1, 1.35), (w_app.get_left()[0] - 0.02, 1.3)])
        rs = _poly([(r2.get_right()[0] + 0.1, 0.4), (w_sec.get_left()[0] - 0.02, 0.5)])
        rd = _poly([(r3b.get_right()[0] + 0.1, -1.1), (2.05, -1.1), (2.05, w_data.get_bottom()[1] - 0.02)])
        rp_y = -1.95
        rp = _poly([(dr.get_right()[0] + 0.02, rp_y), (3.45, rp_y), (3.45, pc.get_bottom()[1] - 0.02)])
        rp_tip = Arrow([3.45, pc.get_bottom()[1] - 0.4, 0], [3.45, pc.get_bottom()[1] - 0.02, 0], buff=0,
                       color=LOOKUP, stroke_width=4, tip_length=0.16, max_tip_length_to_length_ratio=0.5)
        rp_lab = mono("8000:8000", CAPTION, LOOKUP).move_to([0.6, rp_y - 0.27, 0])
        add("route_app", ra)
        add("route_secrets", rs)
        add("route_data", rd)
        add("route_port", VGroup(rp, rp_tip, rp_lab))
        for r in (ra, rs, rd):          # behind the windows: a route ends under its window
            self.remove(r)
            self.add_to_back(r)
        self.routes = {"app": ra, "secrets": rs, "data": rd, "port": rp}
        self._ends = {"app": (r1, w_app), "secrets": (r2, w_sec), "data": (r3b, w_data),
                      "port": (dr, pc)}

        # -- the phone book on the rail
        bt = mono("llm-rag-chromadb → 172.19.0.2", CAPTION, LOOKUP)
        bf = box(bt.width + 0.4, bt.height + 0.26, LOOKUP, fill=S.BG, fill_opacity=0.95, radius=0.1)
        book = VGroup(bf, bt.move_to(bf)).move_to([0, -1.45, 0])
        book.shift(RIGHT * (3.2 - book.get_right()[0]))
        add("book", book)

        # -- Google: Vertex AI and the key riding the dashed line
        cl = cloud(2.0, CLOUD).move_to([5.4, 1.55, 0])
        clt = sans("Vertex AI", CAPTION, INK).move_to(cl)
        add("cloud", VGroup(cl, clt))
        vx = 4.85
        vy = 2.68
        vline = VGroup(DashedLine([-1.1, cb.get_top()[1], 0], [-1.1, vy, 0], color=CLOUD, stroke_width=3),
                       DashedLine([-1.1, vy, 0], [vx, vy, 0], color=CLOUD, stroke_width=3),
                       DashedLine([vx, vy, 0], [vx, cl.get_top()[1] - 0.15, 0], color=CLOUD, stroke_width=3))
        add("vertex", vline)
        add("key_ride", key_glyph(0.26).move_to([0.35, vy, 0]))

        # -- Docker Hub
        hub = shelf("Docker Hub", w=2.3, color=HUB).move_to([5.3, -1.1, 0])
        add("hub", hub)
        st = mono("llm-rag-cli", CAPTION, S.GREY)
        sf = DashedVMobject(RoundedRectangle(width=st.width + 0.3, height=0.42, corner_radius=0.06),
                            num_dashes=24).set_stroke(S.GREY, 2)
        slot = _keep(VGroup(sf, st.move_to(sf))).next_to(hub.board, UP, buff=0.05)
        add("hub_slot", slot)
        it = VGroup(mono("chromadb/chroma", CAPTION, CTR), mono(":latest", CAPTION, CTR)) \
            .arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        ib = box(it.width + 0.36, it.height + 0.24, CTR, fill=S.BG, fill_opacity=0.95, radius=0.1)
        img = _keep(VGroup(ib, it.move_to(ib))).move_to([5.1, -1.85, 0])
        add("image", img)

    @staticmethod
    def _window(name: str, w: float = 1.45, h: float = 0.5) -> VGroup:
        fr = box(w, h, CTR, fill=S.BG, fill_opacity=0.95, radius=0.08, stroke=2)
        t = mono(name, CAPTION, INK).move_to(fr)
        g = VGroup(fr, t)
        g.frame, g.text = fr, t
        return _keep(g)

    def fit_top(self, k: float = 0.84, bottom: float | None = None):
        """Squeeze to k of the height and sit with the bottom edge at `bottom` (default just above
        the 3-row strip / a 3-line code strip): x -6.38..6.48, y -1.38..3.07 for S16's parts (the
        name tag on top, right of the tracker band; the Vertex AI line above it). Returns self:
        self.play(cv.animate.fit_top()) or cv.fit_top() before showing it.

        Only the shapes squeeze, and only in height: every text, window, chip and glyph keeps its
        size (text >= 20 pt), and they need the boxes' full width (shrunk by k both ways, the
        titles touched their box's edge, docker-volumes/ ran out of the laptop zone, /.venv
        overlapped /app and the windows stuck out of the CLI box). Then the parts that the squeeze
        pulled together move apart, every label >= 0.1 inside its box, and the routes are redrawn
        to their moved ends (the recipe of S04's fit_v2). Not laid out for it: the phone book (it
        would sit on the lowered data route; no caller shows it with fit_top)."""
        bottom = STRIP_TOP + 0.06 if bottom is None else bottom
        units: list = []

        def walk(m):
            if getattr(m, "keep_size", False) or isinstance(m, Text) or hasattr(m, "pt"):
                units.append(m)
                return
            for s in m.submobjects:
                walk(s)

        for s in self.submobjects:
            walk(s)
        self.stretch(k, 1, about_point=self.get_center())
        P = self.parts
        for u in units + [P["door"][0]]:             # the door glyph keeps its shape too
            u.stretch(1 / k, 1)
        self._relayout_fit()
        self.shift(np.array([0.05 - self.get_center()[0], bottom - self.get_bottom()[1], 0]))
        return self

    def _relayout_fit(self, pad: float = 0.1):
        """After fit_top's squeeze: move apart what touches, redraw the routes."""
        P = self.parts
        zf, zt = P["zone"][0], P["zone"][1]
        # the zone's title >= 0.12 under the zone's top edge
        zt.shift(UP * min(0.0, zf.get_top()[1] - 0.12 - zt.get_top()[1]))
        # the folder rows centred across the zone (docker-volumes/, the widest, is 0.11 from both
        # edges; it ended 0.02 from the right edge); docker-volumes/ and chromadb/ a little lower,
        # so the data route from chromadb/ passes >= 0.1 under the rail's label
        r1, r2, r3a, r3b = (self.rows[n] for n in ("repo", "secrets", "volumes", "chromadb"))
        widest = max(r.width for r in (r1, r2, r3a))
        x0 = zf.get_left()[0] + max(pad, (zf.width - widest) / 2)
        for r in (r1, r2):
            r.shift(RIGHT * (x0 - r.get_left()[0]))
        P["row_volumes"].shift(RIGHT * (x0 - r3a.get_left()[0]))
        rl = P["rail"][1]
        P["row_volumes"].shift(UP * min(0.0, rl.get_bottom()[1] - 0.12 - r3b.get_center()[1]))
        # the CLI box: its windows >= 0.12 inside the left edge; /app (a short name) gives up 0.09
        # of width on its right, /secrets widens to its text + 2 pad; the /.venv box fits its text
        # + 2 pad and sits centred between /app and the box's right edge (its "/" sat on the border
        # of a 1.0-wide box)
        cb = P["cli"].frame
        w_app, w_sec, w_data = self.windows["app"], self.windows["secrets"], self.windows["data"]
        for w in (w_app, w_sec):
            w.shift(RIGHT * max(0.0, cb.get_left()[0] + 0.125 - w.get_left()[0]))
        w_app.frame.stretch_to_fit_width(w_app.frame.width - 0.09, about_edge=LEFT)
        w_app.text.move_to(w_app.frame)
        w_sec.frame.stretch_to_fit_width(max(w_sec.frame.width, w_sec.text.width + 2 * pad), about_edge=LEFT)
        w_sec.text.move_to(w_sec.frame)
        venv = P["venv"]
        venv[0].stretch_to_fit_width(venv[1].width + 2 * pad)
        venv.move_to([(w_app.frame.get_right()[0] + cb.get_right()[0]) / 2, w_app.get_center()[1], 0])
        venv[1].move_to(venv[0])
        P["build"].shift(RIGHT * max(0.0, cb.get_left()[0] + 0.18 - P["build"].get_left()[0]) + DOWN * 0.06)
        # the titles >= 0.1 inside their box (left and top)
        hb = P["chroma"].frame
        for title, frame in ((P["cli"][1], cb), (P["chroma"][1], hb)):
            title.shift(RIGHT * max(0.0, frame.get_left()[0] + 0.15 - title.get_left()[0])
                        + DOWN * max(0.0, title.get_top()[1] - (frame.get_top()[1] - 0.1)))
        # the Chroma box: /data >= 0.12 inside, the cylinder clear of the :8000 chip, the chip back
        # inside the box's right edge (with its route's tip), the name 0.1 above the box
        w_data.shift(RIGHT * max(0.0, hb.get_left()[0] + 0.125 - w_data.get_left()[0]))
        pc = P["port_chip"]
        dx = min(0.0, hb.get_right()[0] - 0.03 - pc.get_right()[0])
        pc.shift(RIGHT * dx)
        tip = P["route_port"][1]                     # its point 0.02 under the chip, as before
        tip.shift(RIGHT * dx + UP * (pc.get_bottom()[1] - 0.02 - tip.get_top()[1]))
        self.cyl.shift(UP * max(0.0, pc.get_top()[1] + 0.15 - self.cyl.get_bottom()[1]))
        plug = P["plug_chroma"]                      # the plug clear of the chip's left end
        plug.shift(RIGHT * min(0.0, pc.get_left()[0] - 0.12 - plug.get_center()[0]))
        nm = P["name"]
        nm.shift(UP * (hb.get_top()[1] + 0.1 - nm.get_bottom()[1]))
        # the Vertex AI line (and the riding key) >= 0.12 above the name
        vl = P["vertex"]
        lift = max(0.0, nm.get_top()[1] + 0.12 - vl[1].get_center()[1])
        if lift:
            vl[1].shift(UP * lift)
            for v in (vl[0], vl[2]):
                v.stretch_to_fit_height(v.height + lift, about_edge=DOWN)
            P["key_ride"].shift(UP * lift)
        # "depends" / "on": the squeeze pulled the two lines into each other
        dlab = P["depends"][2]
        dc = dlab.get_center()
        dlab.arrange(DOWN, buff=0.08).move_to(dc)
        # Docker Hub: the shelf's board and the image chip clear of the rail and of each other
        P["image"].shift(DOWN * 0.1)
        VGroup(P["hub"], P["image"]).shift(DOWN * 0.2)
        # the routes to their moved ends
        self.routes["app"].set_points_as_corners([[r1.get_right()[0] + 0.1, r1.get_center()[1], 0],
                                                  [w_app.get_left()[0] - 0.02, w_app.get_center()[1], 0]])
        self.routes["secrets"].set_points_as_corners([[r2.get_right()[0] + 0.1, r2.get_center()[1], 0],
                                                      [w_sec.get_left()[0] - 0.02, w_sec.get_center()[1], 0]])
        yd, xd = r3b.get_center()[1], w_data.get_center()[0]
        self.routes["data"].set_points_as_corners([[r3b.get_right()[0] + 0.1, yd, 0], [xd, yd, 0],
                                                   [xd, w_data.get_bottom()[1] - 0.02, 0]])
        rp = self.routes["port"]
        a, xp = rp.get_start(), pc.get_center()[0]
        rp.set_points_as_corners([a, [xp, a[1], 0], [xp, pc.get_bottom()[1] - 0.02, 0]])

    def row(self, name: str):
        return self.rows[name]

    def window(self, name: str):
        return self.windows[name]

    def pulse(self, route: str, color: str = LOOKUP, run_time: float = 1.0):
        """The route pulses (a flash runs along it; nothing travels, nothing stays)."""
        return ShowPassingFlash(self.routes[route].copy().set_stroke(color, 9), time_width=0.6,
                                run_time=run_time)

    def blink(self, route: str, color: str = TURN):
        """Both ends of a mount blink at once: one folder seen from two sides."""
        a, b = self._ends[route]
        return AnimationGroup(Indicate(a, color=color, scale_factor=1.08),
                              Indicate(b, color=color, scale_factor=1.08))

    def fill_slots(self, color: str = LOOKUP) -> list:
        return [s.fill_sq.animate.set_fill(color, 0.55) for s in self.slot_list]

    def empty_slots(self, color: str = ERR) -> list:
        return [Succession(s.fill_sq.animate(run_time=0.3).set_fill(color, 0.6),
                           s.fill_sq.animate(run_time=0.3).set_fill(color, 0.0),
                           s.fill_sq.animate(run_time=0.3).set_fill(color, 0.6),
                           s.fill_sq.animate(run_time=0.3).set_fill(color, 0.0))
                for s in self.slot_list]

    def light(self, name: str = "cli", color: str = TURN):
        return self.parts[name].frame.animate.set_stroke(color, 5)

    def unlight(self, name: str = "cli"):
        return self.parts[name].frame.animate.set_stroke(CTR, 3)

    def remove_cli(self) -> list:
        """exit (--rm): the CLI box and everything only it had leave; Chroma stays."""
        return self.parts_out("cli", "venv", "slots", "build", "plug_cli", "depends", "route_app",
                              "route_secrets", "vertex", "key_ride")

    def remove_chroma(self) -> list:
        """docker compose down: the Chroma box, its port, the rail and the phone book leave; the
        GREY folder stays."""
        return self.parts_out("chroma", "name", "port_chip", "plug_chroma", "route_data", "route_port",
                              "book", "rail")

    def new_boxes(self) -> list:
        """sh docker-shell.sh again: new boxes over the same folder (no pull, no build)."""
        names = ("rail", "chroma", "name", "port_chip", "plug_chroma", "route_data", "route_port",
                 "cli", "venv", "slots", "plug_cli", "route_app", "route_secrets")
        return self.parts_in(*[n for n in names if not self.is_shown(n)])



# ------------------------------------------------------------------ V3 · ruler and scissors
class Ribbon(Piece):
    """V3: the story as a ribbon of GREEN word blocks (no text), positions computed on the whole
    file; the view (chars a..b) spans `width`. Char 27 is where line 3 starts: the author line
    stays off-screen left.

        rb = Ribbon().move_to(UP * 0.5)
        win = rb.ruler(*CHAR_SPANS[0]); band = rb.band(330, 350)
    """

    def __init__(self, view=(STORY_START, STORY_START + 1000), width: float = 12.4,
                 row_h: float = 0.24, breaks: bool = False, blocks: bool = True,
                 color: str = DATA, show=None, **kw):
        super().__init__(**kw)
        self.v0, self.v1 = view
        self.unit = width / (self.v1 - self.v0)
        self.row_h = row_h
        x0 = -width / 2
        self.p0 = _ref([x0, 0, 0])
        self.p1 = _ref([x0 + width, 0, 0])
        self.add(self.p0, self.p1)
        vis = self._show_set(show, ("blocks", "breaks"))
        bl = VGroup()
        if blocks:
            for m in re.finditer(r"\S+", STORY_TEXT):
                a, b = max(m.start(), self.v0), min(m.end(), self.v1)
                if b <= a:
                    continue
                w = (b - a) * self.unit
                r = Rectangle(width=max(0.012, w - 0.2 * self.unit), height=row_h, stroke_width=0)
                r.set_fill(color, 0.6).move_to([x0 + (a - self.v0) * self.unit + w / 2, 0, 0])
                bl.add(r)
        else:
            bl.add(Rectangle(width=width, height=row_h, stroke_width=0).set_fill(color, 0.6))
        self.part("blocks", bl, "blocks" in vis)
        self.blocks = bl
        br = VGroup()
        if breaks:
            for m in re.finditer(r"\n+", STORY_TEXT):
                if not self.v0 <= m.start() < self.v1:
                    continue
                tall = len(m.group(0)) >= 2
                h = row_h + (0.5 if tall else 0.26)
                x = x0 + (m.start() + 0.5 - self.v0) * self.unit
                br.add(Line([x, -h / 2, 0], [x, h / 2, 0], color=S.GREY, stroke_width=3 if tall else 2))
        self.part("breaks", br, "breaks" in vis)

    def x_of(self, i: float) -> float:
        a, b = self.p0.get_center()[0], self.p1.get_center()[0]
        return a + (i - self.v0) / (self.v1 - self.v0) * (b - a)

    def _y(self) -> float:
        return self.p0.get_center()[1]

    def _h(self) -> float:
        return self.row_h * (self.p1.get_center()[0] - self.p0.get_center()[0]) / (self.unit * (self.v1 - self.v0))

    def ruler(self, a: int, b: int, color: str = TOOL) -> VGroup:
        """A PURPLE ruler window over chars a..b (outline, faint fill, ticks every 50 chars along
        its top edge). Not added. .frame .ticks"""
        x0, x1, h = self.x_of(a), self.x_of(b), self._h() + 0.32
        fr = Rectangle(width=x1 - x0, height=h, stroke_color=color, stroke_width=3).set_fill(color, 0.1)
        fr.move_to([(x0 + x1) / 2, self._y(), 0])
        ticks = VGroup(*[Line(UP * 0, UP * (0.14 if (k % 2) else 0.22), color=color, stroke_width=2)
                         .move_to([self.x_of(a + k * 50), fr.get_top()[1], 0], aligned_edge=DOWN)
                         for k in range(0, (b - a) // 50 + 1)])
        g = VGroup(fr, ticks)
        g.frame, g.ticks = fr, ticks
        return g

    def band(self, a: int, b: int, color: str = TURN, opacity: float = 0.4) -> Rectangle:
        """A translucent band over chars a..b (the overlap). Not added."""
        x0, x1 = self.x_of(a), self.x_of(b)
        return Rectangle(width=max(0.03, x1 - x0), height=self._h() + 0.14, stroke_width=0) \
            .set_fill(color, opacity).move_to([(x0 + x1) / 2, self._y(), 0])

    def cut(self, i: int, color: str = TOOL, h: float | None = None) -> Line:
        """A cut line at char i. Not added."""
        h = h or self._h() + 0.5
        x = self.x_of(i)
        return Line([x, self._y() - h / 2, 0], [x, self._y() + h / 2, 0], color=color, stroke_width=4)

    def span_card(self, a: int, b: int, color: str = DATA, dy: float = 0.0, h: float = 0.2) -> RoundedRectangle:
        """A chunk drawn as a thin card over chars a..b, dy above the ribbon. Not added."""
        x0, x1 = self.x_of(a), self.x_of(b)
        return RoundedRectangle(width=max(0.05, x1 - x0), height=h, corner_radius=min(0.06, h / 2),
                                stroke_color=color, stroke_width=2).set_fill(color, 0.25) \
            .move_to([(x0 + x1) / 2, self._y() + dy, 0])

    def callout(self, a: int, b: int, color: str = INK, size: float = CAPTION, prefix: str = "",
                suffix: str = "") -> VGroup:
        """The story's own characters a..b (<= 60, never before char 27, line breaks shown as
        spaces) in a mono card above the range. Not added. .text .frame .s (the string)"""
        if a < STORY_START:
            raise ValueError("the first two lines of the story are never shown")
        if b - a > 60:
            raise ValueError("a callout holds at most 60 characters")
        s = prefix + STORY_TEXT[a:b].replace("\n", " ") + suffix
        t = mono_line(s, size, color)
        fr = box(t.strut.width + 0.36, t.strut.height + 0.22, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.1)
        t.move_to(fr)
        g = VGroup(fr, t)
        g.text, g.frame, g.s = t, fr, s
        x = (self.x_of(a) + self.x_of(b)) / 2
        g.move_to([x, self._y() + self._h() / 2 + 0.25 + g.height / 2, 0])
        if g.get_right()[0] > 6.5:
            g.shift(LEFT * (g.get_right()[0] - 6.5))
        if g.get_left()[0] < -6.5:
            g.shift(RIGHT * (-6.5 - g.get_left()[0]))
        return _keep(g)


# ------------------------------------------------------------------ V4 · meaning as direction
class VectorSketch(Piece):
    """V4: a 2-D drawing of a sphere (circle + dashed equator ellipse) with an origin dot; arrows
    are 2-D projections (VoiceScene is not a ThreeDScene). sphere=False: only the origin.

        vs = VectorSketch(r=1.6).move_to(LEFT * 3)
        a = vs.arrow(35, 0.85); cl = vs.cluster(60, 5); arc = vs.arc(35, 60)
    """

    def __init__(self, r: float = 1.6, sphere: bool = True, show=None, **kw):
        super().__init__(**kw)
        vis = self._show_set(show, ("circle", "equator", "origin"))
        c = Circle(radius=r, stroke_color=S.GREY, stroke_width=2.5).set_fill(S.GREY, 0.04)
        eq = DashedVMobject(Ellipse(width=2 * r, height=0.55 * r), num_dashes=40, dashed_ratio=0.5) \
            .set_stroke(S.GREY, 2)
        self.part("circle", c, sphere and "circle" in vis)
        self.part("equator", eq, sphere and "equator" in vis)
        self.part("origin", Dot(ORIGIN, radius=0.06, color=INK), "origin" in vis)
        self.o = _ref(ORIGIN)
        self.e = _ref(RIGHT * r)
        self.add(self.o, self.e)

    def r(self) -> float:
        return float(np.linalg.norm(self.e.get_center() - self.o.get_center()))

    def point(self, deg: float, length: float = 1.0):
        """The tip of an arrow at `deg` degrees with `length` (1 = the circle's radius)."""
        d = np.array([np.cos(np.radians(deg)), np.sin(np.radians(deg)), 0])
        return self.o.get_center() + d * length * self.r()

    def arrow(self, deg: float, length: float = 0.85, color: str = DATA, stroke: float = 5) -> Arrow:
        return Arrow(self.o.get_center(), self.point(deg, length), buff=0, color=color,
                     stroke_width=stroke, tip_length=0.2, max_tip_length_to_length_ratio=0.25)

    def cluster(self, deg: float, n: int = 5, spread: float = 10.0, length: float = 0.8,
                color: str = DATA, seed: int = 0, stroke: float = 4) -> VGroup:
        """n arrows around `deg` (± spread degrees, lengths ± 8 %), seeded."""
        rng = np.random.default_rng(seed)
        return VGroup(*[self.arrow(deg + float(rng.uniform(-spread, spread)),
                                   length * float(rng.uniform(0.92, 1.08)), color, stroke) for _ in range(n)])

    def arc(self, a: float, b: float, radius: float = 0.45, color: str = TURN, stroke: float = 4) -> Arc:
        """An angle arc between directions a and b (degrees), radius as a fraction of r."""
        lo, hi = min(a, b), max(a, b)
        return Arc(radius=radius * self.r(), start_angle=np.radians(lo), angle=np.radians(hi - lo),
                   arc_center=self.o.get_center(), stroke_color=color, stroke_width=stroke)

    def unit_circle(self, frac: float = 1.0, color: str = S.GREY) -> VMobject:
        """A dashed circle of radius frac * r (length 1)."""
        return DashedVMobject(Circle(radius=frac * self.r()).move_to(self.o.get_center()),
                              num_dashes=48, dashed_ratio=0.5).set_stroke(color, 2)

    def sector(self, a: float, b: float, color: str = LOOKUP, opacity: float = 0.22,
               frac: float = 1.0) -> VMobject:
        """A translucent beam (a sector) between directions a and b."""
        lo, hi = min(a, b), max(a, b)
        return Sector(radius=frac * self.r(), start_angle=np.radians(lo), angle=np.radians(hi - lo),
                      arc_center=self.o.get_center()).set_fill(color, opacity).set_stroke(width=0)


class CellBar(Piece):
    """3,072 numbers drawn as 48 groups of 64 cells; the first 4 groups (256 numbers) are the
    GREEN part `keep`. Parts bar, keep, labels ("the model's full output · 3,072 numbers" above,
    "output_dimensionality = 256" under keep). .cut() -> [anims]: the other 2,816 fall away."""

    def __init__(self, width: float = 11.0, h: float = 0.42, show=None, **kw):
        super().__init__(**kw)
        vis = self._show_set(show, ("bar", "keep", "labels"))
        n, kept = FULL_DIM // 64, DIM // 64
        cw = width / n
        segs = VGroup(*[Rectangle(width=cw, height=h, stroke_color=CLOUD, stroke_width=1.2)
                        .set_fill(CLOUD, 0.22).move_to([-width / 2 + (i + 0.5) * cw, 0, 0]) for i in range(n)])
        self.segs = segs
        self.part("bar", segs, "bar" in vis)
        keep = VGroup(*[Rectangle(width=cw, height=h, stroke_color=DATA, stroke_width=1.5)
                        .set_fill(DATA, 0.55).move_to(segs[i]) for i in range(kept)])
        self.part("keep", keep, "keep" in vis)
        top = label("the model's full output · 3,072 numbers", CAPTION, CLOUD).next_to(segs, UP, buff=0.18)
        bot = mono("output_dimensionality = 256", CAPTION, DATA).next_to(keep, DOWN, buff=0.18).align_to(keep, LEFT)
        self.part("labels", VGroup(top, bot), "labels" in vis)

    def cut(self) -> list:
        rest = VGroup(*self.segs[DIM // 64:])
        return [rest.animate.shift(DOWN * 0.6).set_opacity(0)]


# ------------------------------------------------------------------ V5 · records, an index, a folder
class RecordTable(Piece):
    """V5's rows: four cells id / document / metadata / embedding (11.6 wide). Parts header,
    row0 … row{n-1}. .cell(i, col) .column(col) (header + cells) .col_box(col, color) (not added)."""

    COLS = (("id", 3.4), ("document", 2.5), ("metadata", 3.9), ("embedding", 1.5))

    def __init__(self, n: int = 3, ids=None, show=None, row_h: float = 0.5, **kw):
        super().__init__(**kw)
        ids = ids or [FIRST_ID[:-1] + str(i) for i in range(n)]
        names = ("header",) + tuple(f"row{i}" for i in range(n))
        vis = self._show_set(show, names)
        total = sum(w for _, w in self.COLS) + 0.15 * (len(self.COLS) - 1)
        xs, x = {}, -total / 2
        for c, w in self.COLS:
            xs[c] = (x, x + w)
            x += w + 0.15
        self.xs = xs
        head = VGroup(*[sans(c, CAPTION, S.GREY).move_to([(xs[c][0] + xs[c][1]) / 2, 0, 0])
                        for c, _ in self.COLS])
        self.part("header", head, "header" in vis)
        self.head = {c: head[i] for i, (c, _) in enumerate(self.COLS)}
        self.cells = []
        for i in range(n):
            y = -(i + 1) * (row_h + 0.12)
            fr = box(total + 0.2, row_h, DATA, fill_opacity=0.06, radius=0.08, stroke=1.5).move_to([0, y, 0])
            cid = mono(ids[i], CAPTION, INK)
            doc = VGroup(*[RoundedRectangle(width=w, height=0.07, corner_radius=0.03, stroke_width=0)
                           .set_fill(S.GREY, 0.55) for w in (2.0, 1.6)]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            meta = mono("{book, author, year}", CAPTION, DATA)
            emb = vec_glyph(1, DATA, 0.45, base=25)
            cells = {"id": cid, "document": doc, "metadata": meta, "embedding": emb}
            for c, m in cells.items():
                m.move_to([(xs[c][0] + xs[c][1]) / 2, y, 0])
            row = VGroup(fr, *cells.values())
            row.frame = fr
            self.part(f"row{i}", row, f"row{i}" in vis)
            self.cells.append(cells)

    def cell(self, i: int, col: str):
        return self.cells[i][col]

    def column(self, col: str) -> VGroup:
        return VGroup(self.head[col], *[c[col] for c in self.cells])

    def col_box(self, col: str, color: str = TURN) -> VMobject:
        """An outline around a column (header + cells). Not added."""
        g = self.column(col)
        return box(g.width + 0.3, g.height + 0.25, color, fill_opacity=0.0, radius=0.1, stroke=3).move_to(g)


def collection_glyph(name: str = "char-split-collection", count: str | None = None,
                     color: str = DATA) -> VGroup:
    """A collection: a GREEN stack of slabs, its mono name under it, an optional count under
    the name ("8,248"). .stack .name .count"""
    slabs = VGroup(*[RoundedRectangle(width=2.0, height=0.16, corner_radius=0.05, stroke_color=color,
                                      stroke_width=1.5).set_fill(_mix(color, 0.3), 1).shift(UP * k * 0.13)
                     for k in range(6)])
    n = mono(name, CAPTION, color).next_to(slabs, DOWN, buff=0.15)
    g = VGroup(slabs, n)
    g.stack, g.name, g.count = slabs, n, None
    if count:
        c = sans(count, CAPTION + 2, INK).next_to(n, DOWN, buff=0.1)
        g.add(c)
        g.count = c
    return _keep(g)


class ScanColumn(Piece):
    """The slow scan (A33-A36): n thin GREEN rows, a PINK pointer at their left and a counter
    "rows read". .walk(to=8248, run_time=3) -> [anims] (pointer to the bottom, counter ticks)."""

    def __init__(self, n: int = 28, w: float = 1.6, show=None, **kw):
        super().__init__(**kw)
        rows = VGroup(*[RoundedRectangle(width=w, height=0.09, corner_radius=0.03, stroke_width=0)
                        .set_fill(DATA, 0.6) for _ in range(n)]).arrange(DOWN, buff=0.045)
        self.rows = rows
        self.add(rows)
        ptr = Polygon([0, 0.12, 0], [0, -0.12, 0], [0.2, 0, 0], stroke_width=0).set_fill(LOOKUP, 1)
        ptr.next_to(rows[0], LEFT, buff=0.12)
        self.pointer = ptr
        self.add(ptr)
        self.counter = Counter("rows read", 0, LOOKUP, size=CAPTION + 2)
        self.counter.next_to(rows, RIGHT, buff=0.4).align_to(rows, UP)
        self.add(self.counter)

    def walk(self, to: int = 8248, run_time: float = 3.0) -> list:
        end = self.pointer.copy().next_to(self.rows[-1], LEFT, buff=0.12)
        return [self.pointer.animate(rate_func=linear, run_time=run_time).move_to(end),
                self.counter.count_to(to, run_time)]


class HnswGraph(Piece):
    """Our illustration of HNSW (A37-A38): layers of nodes, sparse on top, dense at the bottom;
    every upper node also lives in the layers below (dashed GREY links). Edges join neighbours.
    .hop(target=None) -> (pointer, [anims]): play the anims one by one (Succession); the pointer
    is scene-owned (FadeOut it)."""

    def __init__(self, layers=(3, 7, 15), width: float = 6.4, gap: float = 1.05, seed: int = 4,
                 show=None, **kw):
        super().__init__(**kw)
        rng = np.random.default_rng(seed)
        n_bot = layers[-1]
        xs = np.sort(rng.uniform(-width / 2 + 0.3, width / 2 - 0.3, n_bot))
        sets = [list(range(n_bot))]
        for n in reversed(layers[:-1]):
            prev = sets[0]
            pick = sorted(rng.choice(prev, n, replace=False).tolist())
            sets.insert(0, pick)
        self.sets, self.xs = sets, xs
        self.layer_y = [((len(layers) - 1) / 2 - k) * gap for k in range(len(layers))]
        names = tuple(f"layer{k}" for k in range(len(layers))) + ("links",)
        vis = self._show_set(show, names)
        self.nodes = []
        for k, ids in enumerate(sets):
            y = self.layer_y[k]
            floor = DashedLine([-width / 2, y - 0.18, 0], [width / 2, y - 0.18, 0], color=S.GREY_DARK,
                               stroke_width=2)
            dots = {i: Dot([xs[i], y, 0], radius=0.07, color=DATA) for i in ids}
            edges = VGroup()
            for a, b in zip(ids, ids[1:]):
                edges.add(Line(dots[a].get_center(), dots[b].get_center(), color=S.GREY, stroke_width=2,
                               stroke_opacity=0.7))
            for a, b in zip(ids, ids[2:]):
                if k == len(sets) - 1 and (a + b) % 3 == 0:
                    edges.add(_arc_between(dots[a].get_center(), dots[b].get_center()))
            self.part(f"layer{k}", VGroup(floor, edges, *dots.values()), f"layer{k}" in vis)
            self.nodes.append(dots)
        links = VGroup()
        for k in range(len(sets) - 1):
            for i in sets[k]:
                links.add(DashedLine(self.nodes[k][i].get_center(), self.nodes[k + 1][i].get_center(),
                                     color=S.GREY_DARK, stroke_width=1.5, dash_length=0.06))
        self.part("links", links, "links" in vis)

    def hop(self, target: int | None = None, color: str = LOOKUP, step_time: float = 0.45):
        target = self.sets[-1][-3] if target is None else target
        tx = self.xs[target]
        cur = self.sets[0][0]
        ptr = Dot(self.nodes[0][cur].get_center(), radius=0.12, color=color)
        anims = []
        for k, ids in enumerate(self.sets):
            if k > 0:
                anims.append(ptr.animate(run_time=step_time).move_to(self.nodes[k][cur].get_center()))
            best = min(ids, key=lambda i: abs(self.xs[i] - tx))
            if k == len(self.sets) - 1:
                best = target
            if best != cur:
                anims.append(ptr.animate(run_time=step_time).move_to(self.nodes[k][best].get_center()))
                cur = best
        return ptr, anims


def _arc_between(a, b, color=S.GREY):
    """A curved edge for the dense layer of HnswGraph."""
    return Arc(radius=np.linalg.norm(b - a) * 0.75, start_angle=0, angle=0.6).put_start_and_end_on(a, b) \
        .set_stroke(color, 1.5, opacity=0.5)


# ------------------------------------------------------------------ V6 · rank, cut, filter first
STAGES_A32 = ("Indexing", "Vector Database", "Querying", "Post Processing")


class RankColumn(Piece):
    """V6, first half (A48-A53): GREEN cards with similarity scores (the lecture's example
    numbers), a header and an arrow "bigger = closer". Parts cards header arrow; scores are
    written in with .scores_in(). Rows sit in input order; .sort() re-sorts by score.

        rc = RankColumn(); self.play(*rc.parts_in("cards", "header"))
        for a in rc.scores_in(): self.play(a)
        self.play(rc.sort()); line = rc.k_line(2); self.play(Create(line))
        self.play(*rc.flip())
    """

    def __init__(self, scores=(0.57, 0.77, 0.43, 0.93), pitch: float = 0.62, show=None, **kw):
        super().__init__(**kw)
        vis = self._show_set(show, ("cards", "header", "arrow"))
        self.values = list(scores)
        self.pitch = pitch
        n = len(scores)
        self.slots = [np.array([0, ((n - 1) / 2 - k) * pitch, 0]) for k in range(n)]
        cards = VGroup()
        self.scores = []
        for k, s in enumerate(scores):
            c = chunk_card(1.3, 0.42, DATA, rows=2).move_to(self.slots[k] + LEFT * 0.7)
            cards.add(c)
            t = mono(f"{s:.2f}", SMALL, INK).move_to(self.slots[k] + RIGHT * 0.75)
            self.scores.append(t)
        self.cards = cards
        self.part("cards", cards, "cards" in vis)
        for k, t in enumerate(self.scores):
            self.part(f"score{k}", t, False)
        self.order = list(range(n))
        top = self.slots[0][1] + pitch * 0.75
        self.part("header", sans("similarity (lecture)", CAPTION, S.GREY).move_to([0.2, top, 0]),
                  "header" in vis)
        ax = Arrow(self.slots[-1] + RIGHT * 1.75, self.slots[0] + RIGHT * 1.75, buff=0, color=S.GREY,
                   stroke_width=4, tip_length=0.2)
        al = label("bigger = closer", CAPTION, S.GREY).next_to(ax, RIGHT, buff=0.15)
        self.part("arrow", VGroup(ax, al), "arrow" in vis)
        self.ax, self.al = ax, al

    def scores_in(self) -> list:
        return [AnimationGroup(*self.parts_in(f"score{k}")) for k in range(len(self.values))]

    def sort(self, run_time: float = 1.0):
        new = sorted(range(len(self.values)), key=lambda k: -self.values[k])
        anims = []
        for slot, k in enumerate(new):
            dy = self.slots[slot] - self.slots[self.order.index(k)]
            anims += [self.cards[k].animate.shift(dy), self.scores[k].animate.shift(dy)]
        self.order = new
        return AnimationGroup(*anims, run_time=run_time)

    def k_line(self, k: int = 2, color: str = TURN) -> VGroup:
        """A YELLOW line under the k-th row of the current order, with "top K" at its left."""
        a = self.cards[self.order[k - 1]]
        b = self.cards[self.order[k]]
        y = (a.get_bottom()[1] + b.get_top()[1]) / 2
        x0 = a.get_left()[0] - 0.3
        x1 = self.scores[0].get_right()[0] + 0.3
        ln = Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=5)
        t = sans("top K", CAPTION, color).next_to(ln, LEFT, buff=0.15)
        return VGroup(ln, t)

    def flip(self, header: str = "cosine distance (Chroma)", arrow_label: str = "bigger = farther") -> list:
        """Each score becomes 1 − score; the header changes; the arrow turns over."""
        anims = []
        for k, s in enumerate(self.values):
            old = self.scores[k]
            new = mono(f"{1 - s:.2f}", SMALL, INK).move_to(old)
            anims.append(Transform(old, new))
        h = self.parts["header"]
        anims.append(Transform(h, sans(header, CAPTION, S.GREY).move_to(h)))
        anims.append(self.ax.animate.rotate(PI))
        anims.append(Transform(self.al, label(arrow_label, CAPTION, S.GREY).move_to(self.al, aligned_edge=LEFT)))
        self.values = [1 - s for s in self.values]
        return anims


class DotCloud(Piece):
    """V6, second half: the char-split collection as n GREEN dots ("1 dot ≈ 8 chunks"; our
    illustration of the layout). A Tolminc cluster (upper left, 12 dots) holds the PINK stand-in
    point; "book" = 170 dots spread over the right of the cloud (1,355 / 8); "italian" = 64 of
    them. Parts dots, standin, tolminc_label.
    .mask("all" | "book" | "italian") -> [anims] (what the filter removes dims to GREY)
    .nearest(k, level="all") -> list of dots nearest the stand-in among what survives
    .beam(dots) -> VGroup of PINK lines from the stand-in (not added)"""

    def __init__(self, n: int = 1000, width: float = 10.0, height: float = 3.4, seed: int = 7,
                 show=None, **kw):
        super().__init__(**kw)
        vis = self._show_set(show, ("dots", "standin", "tolminc_label"))
        rng = np.random.default_rng(seed)
        pts = []
        while len(pts) < n - 12:
            p = rng.uniform(-1, 1, 2)
            if p @ p <= 1:
                pts.append([p[0] * width / 2, p[1] * height / 2, 0])
        tc = np.array([-width * 0.3, height * 0.22, 0])
        clus = [tc + np.array([*rng.normal(0, 0.16, 2), 0]) for _ in range(12)]
        pts = [np.array(p) for p in pts if np.linalg.norm(np.array(p) - tc) > 0.55][:n - 12]
        self.tolminc_ids = list(range(len(pts), len(pts) + 12))
        pts += clus
        dots = VGroup(*[Dot(p, radius=0.035, color=DATA) for p in pts])
        right = [i for i, p in enumerate(pts) if p[0] > -0.5 and i not in self.tolminc_ids]
        self.book_ids = sorted(rng.choice(right, 170, replace=False).tolist())
        self.italian_ids = sorted(rng.choice(self.book_ids, 64, replace=False).tolist())
        self.dots = dots
        self.part("dots", dots, "dots" in vis)
        sp = Dot(tc, radius=0.09, color=LOOKUP)
        self.part("standin", sp, "standin" in vis)
        self.standin_dot = sp
        tl = sans("Tolminc story", CAPTION, LOOKUP).next_to(Dot(tc), UP, buff=0.42)
        self.part("tolminc_label", tl, "tolminc_label" in vis)
        self.level = "all"

    def _keep_ids(self, level: str) -> set:
        if level == "book":
            return set(self.book_ids)
        if level == "italian":
            return set(self.italian_ids)
        return set(range(len(self.dots)))

    def mask(self, level: str = "book", dim: float = 0.12) -> list:
        """What the filter removes dims to GREY at low opacity; survivors are GREEN, full."""
        keep = self._keep_ids(level)
        off = VGroup(*[d for i, d in enumerate(self.dots) if i not in keep])
        on = VGroup(*[d for i, d in enumerate(self.dots) if i in keep])
        self.level = level
        anims = []
        if len(off):
            anims.append(off.animate.set_fill(S.GREY, dim))
        if len(on):
            anims.append(on.animate.set_fill(DATA, 1))
        return anims

    def nearest(self, k: int = 10, level: str | None = None) -> list:
        keep = self._keep_ids(level or self.level)
        c = self.standin_dot.get_center()
        ids = sorted(keep, key=lambda i: np.linalg.norm(self.dots[i].get_center() - c))
        return [self.dots[i] for i in ids[:k]]

    def beam(self, dots, color: str = LOOKUP) -> VGroup:
        c = self.standin_dot.get_center()
        return VGroup(*[Line(c, d.get_center(), color=color, stroke_width=2, stroke_opacity=0.8)
                        for d in dots])


class StageStrip(Piece):
    """A strip of stages (A32: Indexing → Vector Database → Querying → Post Processing), GREY
    boxes with arrows; part `filter` (a PINK-edged "metadata filter" box under Post Processing).
    .slide_filter(before=2) -> anim: the filter moves to just before stage 2 (Querying).
    dashed=True draws the boxes dashed (S15's concepts). .boxes[i] .arrows"""

    def __init__(self, stages=STAGES_A32, box_w: float = 2.55, h: float = 0.7, gap: float = 0.55,
                 dashed: bool = False, color: str = S.GREY, show=None, **kw):
        super().__init__(**kw)
        vis = self._show_set(show, ("boxes", "filter"))
        n = len(stages)
        total = n * box_w + (n - 1) * gap
        bxs = VGroup()
        for k, s in enumerate(stages):
            fr = box(box_w, h, color, fill_opacity=0.08, radius=0.1, dashed=dashed)
            t = sans(s, CAPTION, INK).move_to(fr)
            bxs.add(VGroup(fr, t).move_to([-total / 2 + box_w / 2 + k * (box_w + gap), 0, 0]))
        arrows = VGroup(*[Arrow(bxs[k].get_right(), bxs[k + 1].get_left(), buff=0.06, color=color,
                                stroke_width=3, tip_length=0.15) for k in range(n - 1)])
        self.boxes, self.arrows = bxs, arrows
        self.part("boxes", VGroup(bxs, arrows), "boxes" in vis)
        ft = sans("metadata filter", CAPTION, INK)
        ff = box(ft.width + 0.4, h * 0.85, LOOKUP, fill=S.BG, fill_opacity=0.95, radius=0.1, stroke=3)
        filt = VGroup(ff, ft.move_to(ff)).move_to(bxs[-1].get_center() + DOWN * (h + 0.35))
        self.part("filter", filt, "filter" in vis)

    def slide_filter(self, before: int = 2, run_time: float = 1.2):
        a, b = self.boxes[before - 1], self.boxes[before]
        x = (a.get_right()[0] + b.get_left()[0]) / 2
        f = self.parts["filter"]
        return f.animate(run_time=run_time).move_to([x, f.get_center()[1], 0])


# ------------------------------------------------------------------ V7 · the final prompt
class PromptStack(Piece):
    """V7 (A57-A59): three blocks stacked at the left (system GREY · query PINK · context GREEN)
    with a brace "final prompt", the BLUE LLM box at the right with its model chip, a feed arrow.
    Parts system query context brace llm model feed ghost cable_loose cable_in lock (the last
    four hidden by default unless named in show).
        ps = PromptStack(); self.play(*ps.ghost()); self.play(*ps.unplug()); self.play(*ps.plug())
    """

    def __init__(self, show=("system", "query", "context", "brace", "llm", "model", "feed"), **kw):
        super().__init__(**kw)
        vis = set(show) if show is not None else {"system", "query", "context", "brace", "llm", "model",
                                                  "feed", "ghost", "cable_loose", "cable_in", "lock"}
        bw, bh, bx = 4.3, 0.72, -2.75
        spec = (("system", "system prompt · how to behave", S.GREY),
                ("query", "query · the user's input", LOOKUP),
                ("context", "context · retrieved text", DATA))
        blocks = {}
        for k, (name, text, col) in enumerate(spec):
            fr = box(bw, bh, col, fill_opacity=0.12, radius=0.1, stroke=3)
            t = sans(text, CAPTION + 2, INK).move_to(fr)
            g = VGroup(fr, t).move_to([bx, 0.95 - k * (bh + 0.22), 0])
            g.frame, g.text = fr, t
            blocks[name] = g
            self.part(name, g, name in vis)
        self.blocks = blocks
        stack = VGroup(*blocks.values())
        br = Brace(stack, LEFT, color=S.GREY)
        bl = VGroup(sans("final", CAPTION, S.GREY), sans("prompt", CAPTION, S.GREY)).arrange(DOWN, buff=0.04)
        bl.next_to(br, LEFT, buff=0.12)
        self.part("brace", VGroup(br, bl), "brace" in vis)
        llm = model_box("LLM", 1.9, 1.3).move_to([3.6, blocks["query"].get_center()[1], 0])
        self.part("llm", llm, "llm" in vis)
        self.llm_box = llm
        mc = _keep(chip(LLM_MODEL, CLOUD, size=CAPTION, font=MONO)).next_to(llm, DOWN, buff=0.2)
        self.part("model", mc, "model" in vis)
        feed = Arrow([stack.get_right()[0] + 0.15, llm.get_center()[1], 0], llm.frame.get_left(), buff=0.1,
                     color=DATA, stroke_width=5, tip_length=0.2)
        self.part("feed", feed, "feed" in vis)
        # the ghost: SYSTEM_INSTRUCTION, dashed GREY over the system block
        sb = blocks["system"]
        gf = box(bw, bh, S.GREY, dashed=True, stroke=3).move_to(sb)
        gt = mono("SYSTEM_INSTRUCTION", CAPTION + 2, S.GREY).move_to(gf)
        ghost = VGroup(gf, gt)
        self.part("ghost", ghost, "ghost" in vis)
        self.ghost_card = ghost
        # cables: from the system block's right edge toward the LLM's top-left
        start = sb.get_right() + RIGHT * 0.05
        plug_at = llm.frame.get_corner(UP + LEFT) + np.array([0.3, 0, 0])
        loose = VMobject(stroke_color=ERR, stroke_width=5)
        mid = start + np.array([1.0, 0.05, 0])
        end = start + np.array([1.7, -0.42, 0])
        loose.set_points_smoothly([start, mid, end])
        plug = Rectangle(width=0.2, height=0.3, stroke_color=ERR, stroke_width=3).set_fill(ERR, 0.5).move_to(end + DOWN * 0.12)
        self.part("cable_loose", VGroup(loose, plug), "cable_loose" in vis)
        cin = VMobject(stroke_color=DATA, stroke_width=5)
        cin.set_points_smoothly([start, start + np.array([2.4, 0.35, 0]), plug_at + UP * 0.35, plug_at])
        self.part("cable_in", cin, "cable_in" in vis)
        lk = padlock(0.42, CLOUD).next_to(llm, UP, buff=0.15)
        lt = sans("weights unchanged", CAPTION, CLOUD).next_to(lk, RIGHT, buff=0.12)
        self.part("lock", VGroup(lk, lt), "lock" in vis)

    def block(self, name: str):
        return self.blocks[name]

    def ghost(self) -> list:
        """The system block becomes the GREY dashed ghost card labelled SYSTEM_INSTRUCTION."""
        return self.parts_out("system") + self.parts_in("ghost")

    def unplug(self) -> list:
        return self.parts_out("cable_in") + self.parts_in("cable_loose")

    def plug(self) -> list:
        return self.parts_out("cable_loose") + self.parts_in("cable_in", anim=Create)


# ------------------------------------------------------------------ V8 · a seismograph of meaning
def _gap_values(seed: int = 11) -> list[float]:
    """Our illustration of the distances between consecutive ±1 windows (one per gap between
    SENTENCES): low noise, a spike before each chapter heading, a few medium bumps. Not a
    measurement (nothing was embedded here)."""
    rng = np.random.default_rng(seed)
    vals = []
    for i in range(1, len(SENTENCES)):
        v = 0.16 + 0.12 * float(rng.random())
        if SENTENCES[i].startswith("##"):
            v = 0.72 + 0.12 * float(rng.random())
        elif i % 17 == 9:
            v = 0.42 + 0.1 * float(rng.random())
        vals.append(v)
    return vals


GAP_VALUES = _gap_values()
GAP_THRESHOLD = float(np.percentile(GAP_VALUES, 95))   # the code's rule: the 95th percentile


class Seismograph(Piece):
    """V8: n sentence tiles (SENTENCES[start:start+n]: number + first words, 20 pt) in a row; the
    distance between consecutive windows rises as a PINK spike over each gap (our illustration),
    a curve joins the spikes, the YELLOW threshold line sits at the 95th percentile of ALL gaps of
    the story; spikes above it become cuts. Parts tiles spikes curve threshold.

        sg = Seismograph(show=("tiles",)).move_to(DOWN * 0.5)
        br = sg.bracket(1); self.play(FadeIn(br)); self.play(br.animate.become(sg.bracket(2)))
        self.play(sg.spikes_in()); sg.rise(self); self.play(*sg.cuts())
    """

    def __init__(self, start: int = 8, n: int = 9, width: float = 12.4, tile_h: float = 0.95,
                 spike_h: float = 1.7, show=None, **kw):
        super().__init__(**kw)
        vis = self._show_set(show, ("tiles", "spikes", "curve", "threshold"))
        self.start, self.n = start, n
        gap = 0.16
        tw = (width - (n - 1) * gap) / n
        tiles = VGroup()
        for k in range(n):
            i = start + k
            fr = box(tw, tile_h, DATA, fill_opacity=0.14, radius=0.1, stroke=2.5)
            num = sans(str(i + 1), CAPTION, S.GREY)
            words = SENTENCES[i].replace("\n", " ").split()
            txt = None
            for m in (3, 2, 1):
                t = label(" ".join(words[:m]) + ("…" if len(words) > m else ""), CAPTION, INK)
                if t.width <= tw - 0.2:
                    txt = t
                    break
            col = VGroup(num, txt).arrange(DOWN, buff=0.08) if txt is not None else VGroup(num)
            col.move_to(fr)
            g = VGroup(fr, col).move_to([-width / 2 + tw / 2 + k * (tw + gap), 0, 0])
            g.frame, g.num, g.words = fr, num, txt
            tiles.add(g)
        self.tiles = tiles
        self.part("tiles", tiles, "tiles" in vis)
        base = tile_h / 2 + 0.2
        self.base_y = base
        self.spike_h = spike_h
        vals = GAP_VALUES[start:start + n - 1]
        self.vals = vals
        spikes = VGroup()
        tops = []
        for k, v in enumerate(vals):
            x = (tiles[k].get_right()[0] + tiles[k + 1].get_left()[0]) / 2
            top = np.array([x, base + v * spike_h, 0])
            spikes.add(Line([x, base, 0], top, color=LOOKUP, stroke_width=4))
            tops.append(top)
        self.spikes = spikes
        self.part("spikes", spikes, "spikes" in vis)
        curve = VMobject(stroke_color=LOOKUP, stroke_width=2.5, stroke_opacity=0.7)
        curve.set_points_as_corners(tops) if len(tops) > 1 else curve.set_points_as_corners([tops[0], tops[0]])
        self.part("curve", curve, "curve" in vis)
        ty = base + GAP_THRESHOLD * spike_h
        th = DashedLine([-width / 2, ty, 0], [width / 2, ty, 0], color=TURN, stroke_width=4)
        tl = mono("95th percentile", CAPTION, TURN).next_to(th, UP, buff=0.08)
        left_free = not vals or vals[0] <= GAP_THRESHOLD
        right_free = not vals or vals[-1] <= GAP_THRESHOLD
        tl.align_to(th, LEFT if left_free or not right_free else RIGHT)
        self.part("threshold", VGroup(th, tl), "threshold" in vis)
        self.baseline = _ref([0, base, 0])
        self.add(self.baseline)

    def above(self) -> list[int]:
        """Gap indices k (between tile k and k+1) whose spike is above the threshold."""
        return [k for k, v in enumerate(self.vals) if v > GAP_THRESHOLD]

    def bracket(self, i: int, color: str = TURN) -> VGroup:
        """A ±1 window bracket over tiles i-1..i+1 (clipped to the row). Not added."""
        a, b = self.tiles[max(0, i - 1)], self.tiles[min(self.n - 1, i + 1)]
        x0, x1 = a.get_left()[0] - 0.05, b.get_right()[0] + 0.05
        y = a.get_bottom()[1] - 0.12
        ln = VMobject(stroke_color=color, stroke_width=4)
        ln.set_points_as_corners([[x0, y + 0.18, 0], [x0, y, 0], [x1, y, 0], [x1, y + 0.18, 0]])
        t = mono("±1", CAPTION, color).next_to(ln, DOWN, buff=0.06)
        return VGroup(ln, t)

    def spikes_in(self, run_time: float = 2.0):
        """The spikes grow left to right (and the curve with them)."""
        for n in ("spikes", "curve"):
            if self.parts[n].hidden:
                _set_op(self.parts[n])
                self._flag(self.parts[n], False)
        return AnimationGroup(LaggedStart(*[Create(s) for s in self.spikes], lag_ratio=0.5),
                              Create(self.parts["curve"]), run_time=run_time)

    def rise(self, scene, run_time: float = 1.2):
        """The threshold line rises from the baseline to the 95th percentile."""
        th = self.parts["threshold"]
        target = th.get_center()
        th.move_to([target[0], self.baseline.get_center()[1], 0])
        scene.play(*self.parts_in("threshold"), run_time=0.3)
        scene.play(th.animate.move_to(target), run_time=run_time)

    def cuts(self, color: str = TURN, shift: float = 0.3) -> list:
        """Tiles part at every gap above the threshold: the groups after each cut move right by
        `shift` per cut, the row re-centres, spikes and curve move with their gaps; a YELLOW dashed
        cut mark appears in each cut gap (.cut_marks: scene-owned, FadeOut it yourself)."""
        ks = self.above()
        anims, marks = [], VGroup()
        total = shift * len(ks)

        def dx_tile(j):
            return sum(1 for k in ks if k < j) * shift - total / 2

        def dx_gap(k):                       # gap k sits between tile k and tile k + 1
            return (dx_tile(k) + dx_tile(k + 1)) / 2

        for j, t in enumerate(self.tiles):
            anims.append(t.animate.shift(RIGHT * dx_tile(j)))
        tops = []
        for k, sp in enumerate(self.spikes):
            anims.append(sp.animate.shift(RIGHT * dx_gap(k)))
            tops.append(sp.get_end() + RIGHT * dx_gap(k))
        if len(tops) > 1 and not self.parts["curve"].hidden:
            anims.append(self.parts["curve"].animate.set_points_as_corners(tops))
        for k in ks:
            x = (self.tiles[k].get_right()[0] + self.tiles[k + 1].get_left()[0]) / 2 + dx_gap(k)
            marks.add(DashedLine([x, self.tiles[0].get_bottom()[1] - 0.15, 0],
                                 [x, self.tiles[0].get_top()[1] + 0.15, 0], color=color, stroke_width=4))
        self.cut_marks = marks
        return anims + [FadeIn(marks)]

    def sentence_card(self, i: int, size: float = CAPTION + 2, width_chars: int = 52) -> VGroup:
        """Sentence i's full text (line breaks as spaces), wrapped, in a GREY card. Not added."""
        words = SENTENCES[i].replace("\n", " ").split()
        rows, cur = [], ""
        for w in words:
            if len(cur) + len(w) + 1 > width_chars and cur:
                rows.append(cur)
                cur = w
            else:
                cur = (cur + " " + w).strip()
        rows.append(cur)
        return card_rows(rows, header=f"sentence {i + 1}", size=size, buff=0.08)


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

