"""Shared scene code for AC215 L21 (CI/CD with GitHub Actions II: one push, six fresh machines;
follow-along of dlops-io/cheese-app-ci-cd @ b8458ff, README Part 5 + the optional Part 6).

Paths, narration (SAY lines straight from script.md), the semantic colours of BRIEF.md, the running
example (placeholders only), the two README trackers (P5, P6), loaders for the real captures in
assets/terminal (laptop/ and runner/), job-log panels, step lists and run graphs built from those
captures, source panels from assets/source, terminal helpers, tags, chips, small glyphs and the
video's set pieces V1-V8. Generic helpers come from L09's / L18's common.py (tested there); the run
panels, glyphs and set pieces are new. build/common_test.py plays every helper and piece once.

    from manim import *          # first
    from common import *         # second (common's names win), then:
    SAY = NARRATION["S07"]; assert len(SAY) == SAY_COUNT["S07"]   # one voiceover block per SAY

Notes for scene authors
=======================
Rules. Every text here is >= 20 pt: never .scale() a group that holds text below 1.0 (pieces take
size / width parameters instead; text-free icons exist for small copies: runner_icon, cube_glyph,
suitcase_glyph, bell_glyph, laptop_icon, graph_icon). Never set width / height / color / depth on a
VGroup subclass (Manim properties): these classes use box_w, node_w, room_w ... Methods marked PLAYS
take the scene first, play their own animation and keep any new mobject inside the piece (a later
FadeOut(piece) takes it too). Methods marked ANIM return an animation you play. Place a piece
(shift / move_to) BEFORE its first PLAYS call or between calls: PLAYS methods build new parts at the
piece's current position. To take one part away, piece.drop(scene, part) (fades it and removes it
from the piece; never FadeOut a member of a piece directly: it snaps back when the piece is next
animated). Emoji in captures (✅ ❌ 💥 💔 ✨ 🍰 🏁) are drawn by emo_line(): ✅ = GREEN check_mark,
❌ = RED cross_mark, the others GREY one-cell boxes; any other glyph the mono font lacks raises.

Frame budget. Safe frame x in [-6.6, 6.6], y in [-3.6, 3.6]. Tracker top-left (left -6.5, top 3.5,
lowest point TRACK_BOTTOM 2.9); lref("27, 31") top right (y 3.25 .. 3.6). Part 2 strip
(pipeline_strip(current)) under the tracker at y STRIP_Y 2.5 (2.28 .. 2.72); pictures stay below
PIC_TOP 2.8 (Part 1) or PIC_TOP2 2.15 (Part 2, with the strip). Terminals: term() is 12.6 wide,
22 pt = 65 characters a row, bottom edge at BOTTOM -3.5; a 3-row strip's top is STRIP_TOP (-1.44),
so a picture over a 3-row strip lives in y in [-1.3, 2.8] (Part 2: [-1.3, 2.15]).

Data
    NARRATION["S01"] .. ["S16"]  SAY_COUNT  TITLES[cls]  SPEC (video.yaml)
    Prompts P_HOME 'student@laptop:~$' (before the clone), P_LAPTOP 'student@laptop:~/cheese-app-ci-cd$';
    T_LAPTOP 'laptop'. Names: REPO, COURSE_REPO 'dlops-io/cheese-app-ci-cd', YOUR_REPO_URL
    'https://github.com/<you>/cheese-app-ci-cd.git', WEBHOOK_PH 'https://hooks.slack.com/services/
    <your-webhook-path>', SECRET_NAME 'SLACK_WEBHOOK_URL', MASKED '***', CHANNEL '#build-alerts',
    SHA 'b8458ff' (run 1) SHA_RUN2 '2289d89' SHA_RUN3 '2892b1b' SHA_DEMO 'c3b227f', IMAGE_TAG
    'cheese-app-api:b8458ff…', TAR '/tmp/cheese-app-api.tar', TAR_SIZE '≈ 176 MB' (never the bytes).
    JOBS [(id, name)] in ci.yml order, JOB_IDS, JOB_NAME{id: name}, SHORT{id: 'Build'..'Summary'},
    NEEDS{id: [ids]}, MIDDLE (GitHub's middle column order: unit, integration, system, lint),
    STRIP_BOXES (slide 26's five), STRIP_PURPOSE (slide 27's one-liners), SCREENSHOT_TIMES{id: s}
    (README screenshot, recorded), BILLED_MIN{id: 1}, VERSIONS{tool: 'x.y.z'}, HYGIENE (the seven
    hygiene hooks, .pre-commit-config.yaml order), TRIGGER_BRANCHES ('main', 'develop').

Trackers (script.md conventions; placed top-left)
    tracker_p5(step=None, extra=False) 'README › Part 5: GitHub Actions (Remote CI)' 8 steps;
    tracker_p6(step=None, extra=False) 'README › Part 6: Branch Protection (Optional)' 6 steps.
    extra: True -> ' · extra'; a string -> ' · <string>' (tracker_p5(8, PART4) = ' · Part 4 · L09').
    track(tr, k, extra) ANIM (use it, never tr.goto) · swap_tracker(scene, old, new) PLAYS (P5 -> P6
    in S15) · lref("21") / lref("25–28") the GREY 'Lecture 21 · slides …' tag (top right).

Captures (assets/terminal: laptop/NN-*.txt and runner/<run>/<job>/NN-*.txt; capture-only refused)
    c = capture("04") / capture("laptop/04") / capture("run1/lint-and-format/04") /
        capture("noload/x2") / capture("run-demo/test-summary/01")
    c.cmd_lines (line 1 without '$ ', plus '> ' continuation rows or rows after a trailing '\\')
    c.cmd c.k · c.at(*spec) output by FILE line numbers (ints, (a, b), '…'), refuses the command
    lines and [exit N] (an '[exit N]' glued to the last output line is split off on load) ·
    c.line(n) · c.pick(*ranges) L1-style (body index = file line - k) · c.lines c.exit c.raw c.path
    c.run c.job c.nn (runner captures) · c.step_name (from 00-steps.txt; None for x* files).
    crop(s) every 40/64-hex id -> 7 characters + '…'; crop_addr(s) '172.18.0.1:55228' -> '…';
    cut(s, after) · from_phrase(s, phrase) · soft(lines, n) · strip_ansi(s) · squeeze / cols (tables)
    act_lines(*nums) lines of laptop/62 (ANSI stripped, long space runs squeezed to two, ids cropped).
    results(run) {job id: 'success'|'failure'}; steps(run, job) [Step(n, state, name, note, line)];
    job_result(run, job). RUNS = ('run1', 'run2', 'run3', 'run-demo'); noload is a single job.
    recorded(file, *nums) lines of terminal/expected/<file> (provenance '# …' lines refused).

Sources (assets/source/cheese-app-ci-cd/… = REPO_DIR; history files under HIST_DIR)
    code(path, a, b=None, font_size=22, focus=) CODE() panel, <= 12 lines, must fit 12.6 (22 pt ~65
        characters, 20 pt ~72; a wider one raises and names the line). Paths are repo-relative:
        code(".github/workflows/ci.yml", 5, 11); history: code("history/c3b227f-service.py", 38, 44)
        header 'c3b227f · service.py', code("history/199abd9-to-1a5e363-ci.yml.diff", 9, 20) header
        '199abd9 → 1a5e363 · ci.yml (diff)'. .code .header; highlight with line_bar(p.code, k, colour)
        or code_span(p.code, k, "x"), k = file line - a.
    code_strip(path, line) a one-line code panel (S05's needs lines, S08's runs-on lines).
    excerpt(path, a, b) · source_text(path) · readme(n) · readme_lines(a, b) (markdown stripped,
    blank lines dropped) · readme_panel(a, b, lines=None, card_w=None) the GREY README card
    ('README.md · lines a–b'); lines= picks file lines inside it. .frame .head .body .rows{n: row}.

Terminals (house: 12.6 wide, 22 pt = 65 characters a row)
    term(prompt=P_LAPTOP, rows=10, title='laptop') / laptop_term(rows) · resize(scene, t, rows) PLAYS
    · room · bare_prompt · type_cmd(scene, t, cmd) · type_capture(scene, t, cap) (its command rows;
    folds long ones with ' \\') · out(scene, t, lines, wrap=) (emoji-safe; refuses rows that do not
    fit unless wrap) · cd_prompt(scene, t, prompt) · beside / pin / unpin / on_bar / under_term for
    tags at a row · row_tag, turn_row, extra_row, time_row (tags sized for a 22 pt row).

Tags and chips (GREY unless said; 20-22 pt)
    your_turn() YELLOW · extra_tag(kind) · illustration_tag(s) · recorded_tag(source) ('recorded ·
    README screenshot') · recording_tag() 'at the time of recording' · erratum_tag(s) · standin_tag()
    'live · stand-in runner' · shown_tag() 'shown, not run' · expected_tag(source) · cost_tag(text)
    GOLD (raises on '$', 'cents', 'free tier') · grey_chip · dashed_chip (past/future, skipped) ·
    tool_chip PURPLE · ok_chip GREEN · err_chip RED · route_chip PINK · image_chip TEAL · shared_chip
    ORANGE · github_chip BLUE · question_card(text) YELLOW (S01's question) · ponder(scene, q,
    seconds=8) PLAYS (pause_and_ponder; FadeOut the card at the next block) · flash_tag(scene, tg).

Glyphs (text-free unless named; sizes in scene units)
    state_mark(state, h=0.3): 'success' GREEN check in a ring, 'failure' RED cross, 'skipped' GREY
    dashed ring + slash, 'running' YELLOW dot, 'idle' GREY ring · dot(colour) a commit dot ·
    script_glyph() '>_' (run:, 20 pt) · puzzle_glyph() PURPLE (uses:) · spark(colour) PINK burst ·
    runner_icon(h, lit=) BLUE machine · laptop_icon(w) GREY · cube_glyph(side) TEAL image ·
    suitcase_glyph(h) TEAL tar · shelf(w) 'Docker' shelf (label 20) · bell_glyph(h, colour, slashed=)
    · ring_waves(mob, colour) three arcs (ringing / knocking) · hourglass(h) (.sand_top .sand_bot) ·
    key_file(h) · cursor_dot() · door_glyph(text, colour) door + plate (.frame .text) · gate_glyph(
    gate_h, gate_w) posts + bar (.bar .posts) · exit_badge(code) 'exit N' (RED outline when N != 0) ·
    github_box(text='GitHub') BLUE · chat_window(title=CHANNEL, rows, win_w, win_h) GREY (.frame
    .title .body .rows) · vault_glyph(h) BLUE · gh_page(crumb, page_w, page_h) a schematic GitHub page
    (.frame .crumb .body: place rows in .body; tag it illustration_tag()) · checkbox_row(text, on) ·
    field_row(name, value) · actions_tab(row_text, state) S07's Actions list (6.4 x 2.6; .tabs{name}
    .row .mark) · outline_box · dashed_copy(group) · arrow / route(a, b, arc, dashed=) / travel /
    bounce · ArcBetween(a, b, angle, colour) curved arrow · ring / under / strike / hl_bar ·
    emo_line(s, size, colour) an emoji-safe mono_line · disp_len(s) cells incl. emoji.
    Animating ONE member of a filled box (Indicate(box.frame), box.frame.animate…) re-adds it on top
    of its text and hides the text: animate the whole box, or Circumscribe + Indicate(text) (what
    the pieces' pulse / flash / light do).

Run panels (built from the captures; every one carries its tag)
    run_log(cap, lines=(spec…), title=None, heading=None, size=22, colors={file line: colour},
        crop_ids=True, wrap=False, tag_text='live · stand-in runner', badge=True, log_w=None) the
        job-log panel: title 'Job name › Step name' (from 00-steps.txt; x* files and laptop captures
        need title=), heading = the '$' line in GREY mono 20 (a multi-line run: script collapses to the
        step name; heading='…' any text; heading=False none), rows of the picked FILE lines (ids cropped
        to 7, client addresses to '…', emoji drawn), 'exit N' badge on the top edge, tag on the bottom
        edge. Width fits (>= 6, <= 12.6); a row wider than 65 cells (22 pt) raises unless wrap=True or
        size=20. .frame .title .heading .rows .row(n) (by file line) .badge .tag. lines=() shows the
        heading only (S08's save step). Examples: run_log("run1/test-summary/01", ((13, 16),)) ~7.0 x
        3.3; run_log("run1/build/03", (2, (4, 5), "…", 653, 656)) ~11.8 x 4.2.
    steps_list(run, job, lines=None, size=22, tag_text=...) STEPS(): one row per step (state mark,
        name, note chip); 'job result' row when its file line is included; header = the job's name.
        ~10 x 5 for unit-tests (its long note). .rows .row(n) (by 00-steps.txt file line) .marks
        .names .notes{n} .tag; code_chip(n, code) / shunt_arc(n) / bridge(a, b) return mobjects drawn
        on the rows (V6 on the rows: S10, S14); FadeIn / Create them yourself.
    run_graph(run=None, labels='names'|'short'|'ids'|None, col_gap=1.0, gap=False, badge=True) a
        JobGraph (below) coloured from runner/<run>/results.txt (None: all idle). 'names' ~12.4 x 4.6
        (badge and tag included), 'short' ~8.1 (col_gap=0.6: ~7.3).
    recorded_graph(names=False) RECORDED(screenshot): six GREEN nodes with their times, tag 'recorded
        · README screenshot', ~4.7 x 3.2 (fits beside run_graph(run, 'short', col_gap=0.6)). .graph .tag
    graph_icon(h) a text-free graph (small corners, S16's cards).
    pipeline_strip(current=None) V2's thin Part 2 strip (20 pt, 9.7 x 0.44) under the tracker
        (left -6.5, y STRIP_Y); .set_current(name) ANIM. PipelineStrip(full=True) slide 26's row (22
        pt, 11.9 x 0.72) centred on the origin; .purposes() slide 27's lines under the boxes.

Set pieces (V numbers = BRIEF; each class doc gives its exact layout and every method). Every piece
is centred on its anchor unless said; sizes are width x height.
    V1 HookChain(boxes=('hygiene ×7', 'Black', 'Flake8'), title='Git local hooks', size=22) the GREY
        laptop frame, 7.4 x 2.6 (size=20: 6.9; boxes=() an empty frame: the teammate's laptop).
        PLAYS commit() (returns the GREEN dot) · pass_through(dot, stop=None) · bypass(dot) (RED arc
        over the gates; drop the hook tags first) · add_tests() ('Tests' dashed, struck, 'CI runs
        these') · hook_tags() ('pre-commit', 'pre-push') · push(dot, target, arc=-0.5) (PINK arc from
        the right edge; returns the arrow). ANIM flash(i, colour). .frame .title .gates .arrows .tests
        .tags .exit_point
    V1 ServerDoor(name='shared repository', box_w=5.6, box_h=3.0) 8.0 x 3.0: BLUE server, a door in its
        left wall, GREY 'pre-receive' gate outside, GREY 'post-receive' bell inside. PLAYS refuse(dot)
        · enter(dot) · ring(chips=()) (chips in a row under the box) · update_chip() · github()
        ('GitHub.com', pre-receive dashed + 'your own scripts: not on GitHub.com', BLUE 'Actions'
        badge on the bell, GREEN 'branch protection' gate at the door) · protect(shut=True).
        caption() 'Actions on a push is the bell, not the gate.' (place it). .start .landing points.
    V1 SharedRepo() 7.3 x 2.4 BLUE 'Shared Repository' with an empty dashed slot. PLAYS fill() (slide
        16's 'Build Container' TEAL → 'Check Code' → 'Test Summary') · pass_through(dot). .landing
    V2 CiLoop(loop_w=9.0, loop_h=4.4) 8.5 x 4.4, slide 21's loop. PLAYS question() · marks(states) ·
        close() · go_around(colour) · deploy() (S16; adds ~2.2 to the right). ANIM light(key) key in
        'codebase' 'build' 'test' 'devs' 'notify'. .boxes{key} .devs .notify .commits .returns .back
    V2 PipelineStrip / pipeline_strip: see Run panels.
    V3 TriggerLanes(lanes=('main', 'develop', 'feature/login'), lane_w=9.0, pitch=1.15) 8.9 x 3.4 with
        the GOLD 'runs' meter. PLAYS push(lane) (spark + runner lights + tick when the lane triggers;
        returns the dot) · pr(src, dst, fire=True) / pr_fire() · ghost_merge(dst, src) ('github.sha')
        · tick() · reset_runners(). .lanes{name} .runners{name} .dots{name} .meter .count .pr_arrow .ghost
    V4 WorkflowTree() S03's grammar tree, 10.3 x 5.4 once open. PLAYS open_job() (build's five steps)
        · dim_others(). ANIM pulse(layer) 'event' 'workflow' 'jobs' 'steps'. .root .wf .jobs{id} .steps
    V4 JobGraph(states=None|dict|run, labels='names', size=22, pitch=0.8, col_gap=1.0, edges=True,
        gap=False, badge=True, tag_text=..., texts=None) PLAYS reveal(states, order, per) · tokens(
        states, text, keep=False) (PINK result tokens ride the three needs lines into the summary) ·
        draw_edges() · show_gap() (dashed lint → summary, YELLOW '?'). ANIM set_state(job, state)
        (whole node; self.add(graph) after, to re-seat it) · set_badge(state) · pulse(job, colour).
        .nodes{id} (.frame .mark .text) .edges{(src, dst)} .gap .gap_q .badge .tag; stage_labels().
    V4 Gantt(times=SCREENSHOT_TIMES, bar_w=8.0) 9.9 x 3.8 (+0.9 with billed()). PLAYS critical() ·
        billed() (six GOLD '1 min' blocks: a count, not the clock's scale). .bars{id} .labels .times
        .ruler .billed_row. Morph graph nodes into bars: Transform(g.nodes[j], gantt.bars[j]).
    V5 ImageSuitcase(room_w=2.6) 12.4 x 5.1: put it at move_to([0, -0.65, 0]) under the Part 2
        strip. PLAYS build_cube() · fold() · upload() · dissolve_build() · deliver(jobs=MIDDLE) ·
        load(job) · no_load(job). .rooms{id} (.frame .text .shelf) .store .hub .cube .stamp .case
        .copies{id} .cubes{id}
    V6 ExitGates(names=('Checkout', 'Download', 'Load', 'Black', 'Flake8')) 3.8 x 4.4. PLAYS hold(i,
        code) · climb() · skip(indices) · shunt(i, code) · bridge(i) · reset(). .gates .names .codes{i}
        .job_badge .run_badge .failed
    V7 SystemTestRig(rig_w=10.0, rig_h=4.2) built empty. PLAYS server_up() · wait(seconds) · knock(ok)
        · tests_up() · host_net() · arrivals(labels) · stop(). trapdoor() a small 'skipif' hatch
        (mobject). .runner .server .door .tests .bubble .curl .hour .net
    V8 SlackRoute() absolute layout (x -6.0 .. 6.1, y -2.4 .. 2.0; shift it as one): GitHub box at
        (-4.6, 1.2); bottom band runner (-3.9, -1.45) and '#build-alerts' (3.9, -1.45). PLAYS
        outward(targets) · ghost_outward() · inward() · silence() · ring(ok=False). .github .targets
        .out_arrows .runner .slack .slot .bell

Capture folder names: assets/terminal/laptop (every README Part 5 / 6 command and the extras, on
a docker:29.8.2-dind stand-in laptop, user student), assets/terminal/runner/{run1, run2, run3,
run-demo}/<job id>/ (each job of ci.yml on its own fresh stand-in runner: NN-<step>.txt = step NN,
x*.txt = extra checks, 00-steps.txt the step list, results.txt per run), runner/noload/ (x1, x2:
unit tests without docker load) and assets/terminal/expected (README screenshot transcription,
the job graph from ci.yml, README's 'Watch' list). laptop/capture-only/ is plumbing and refused.
"""

from __future__ import annotations

import math
import re
import subprocess
from functools import lru_cache
from pathlib import Path

import numpy as np
import yaml
from manim import (Star, WHITE, ParametricFunction, DL, DOWN, DR, LEFT, ORIGIN, PI, RIGHT, TAU, UL, UP, UR, AnimationGroup, Arc,  # noqa: F401
                   Arrow, Circle, Circumscribe, Create, CurvedArrow, DashedLine, DashedVMobject, Dot, FadeIn, FadeOut,
                   GrowArrow, GrowFromCenter, Indicate, LaggedStart, Line, MoveAlongPath, Polygon,
                   Rectangle, ReplacementTransform, RoundedRectangle, Rotate, ShowIncreasingSubsets,
                   Square, Succession, Text, Transform, UpdateFromAlphaFunc, VGroup, VMobject,
                   linear, there_and_back)

from explainer import style as S
from explainer.components import pause_and_ponder, person_icon, ponder_card  # noqa: F401 (re-export)
from explainer.devops import (CAPTION, LABEL, MONO, OUTPUT, PANEL, SMALL, TAG, TERM_BG,  # noqa: F401
                              PROMPT_PATH, ReadmeTracker, Terminal, box, cell_width, check_mark, chip,
                              code_block, code_panel, code_span, cross_mark, file_glyph, folder_glyph,
                              glyph_range, label, laptop, lecture_ref, line_bar, line_pitch, mono,
                              mono_line, server, step_badge, substring, tag, warning_sign)
from explainer.script import load_narration

# ------------------------------------------------------------------ paths and data
HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
ASSETS = PROJECT / "assets"
TERMINAL = ASSETS / "terminal"
SOURCE = ASSETS / "source"
EXPECTED = TERMINAL / "expected"
RUNNER = TERMINAL / "runner"
REPO_DIR = "cheese-app-ci-cd"
HIST_DIR = "cheese-app-ci-cd-history"

SPEC = yaml.safe_load((PROJECT / "video.yaml").read_text())
TITLES = {s["cls"]: s["title"] for s in SPEC["scenes"]}
_script = PROJECT / "script.md"
NARRATION = load_narration(_script) if _script.exists() else {}
SAY_COUNT = {k: len(v) for k, v in NARRATION.items()}

# ------------------------------------------------------------------ semantic colours (BRIEF.md)
LAPTOP = S.GREY          # the laptop: your clone, your terminal, the local pre-commit hooks
LOCAL = LAPTOP
GITHUB = S.BLUE          # GitHub: your repository, the Actions tab, every runner, artifact store, vault
CLOUD = GITHUB
RUNNER_C = GITHUB
IMAGE = S.TEAL           # the image cheese-app-api:<sha>, the tar suitcase, the containers
CONTAINER = IMAGE
SHARED = S.ORANGE        # not yours: the course's repo (origin), Docker Hub, port 9000 on the runner
COURSE = SHARED
OWN = S.GREEN            # what the project owns and pins: ci.yml, the config; a pass; your branch main
PASS = OWN
TOOL = S.PURPLE          # GitHub Actions, Docker, Buildx, Black, Flake8, pytest, pre-commit, act, Slack action
ERR = S.RED              # failure, exit codes != 0, would reformat, PermissionError, --no-verify's bypass
TURN = S.YELLOW          # your turn, the tracker, the strip's current box, a run in progress, ponder timer
RUNNING = TURN
COST = S.GOLD            # Actions minutes on private repos, artifact storage, protection on private repos
ROUTE = S.PINK           # events and routes: push / PR arrows, webhook POST, localhost:9000, tokens
EVENT = ROUTE
SKIP = S.GREY            # skipped (dashed)
PAST = S.GREY            # the past and the future (L09's hooks, L23's CD, Milestone 5): dashed
FUTURE = PAST
INK = S.WHITE
DIMMED = S.GREY
STATE_COLOR = {"success": PASS, "failure": ERR, "skipped": SKIP, "running": RUNNING, "idle": S.GREY,
               "queued": S.GREY}

# ------------------------------------------------------------------ layout
TRACK_LEFT, TRACK_TOP = -6.5, 3.5
TRACK_BOTTOM = 2.9           # the tracker's lowest point
BOTTOM = -3.5                # a terminal's bottom edge (kept when it grows or shrinks)
PIC_TOP = 2.8                # pictures stay below this (tracker / lecture_ref above)
STRIP_Y = 2.5                # Part 2's pipeline strip, under the tracker
PIC_TOP2 = 2.15              # Part 2 pictures stay below this


def strip_top(rows: int = 3, size: float = 22) -> float:
    """Top edge of a `rows`-row terminal standing on BOTTOM."""
    return BOTTOM + rows * line_pitch(size) + 0.85


STRIP_TOP = strip_top(3)     # -1.44


def steady(s: str, size: float = 20, color=INK, mono_font: bool = False, **kw) -> Text:
    """Text with a fixed vertical extent (an invisible '|' strut), so that a Transform between two
    steady texts keeps the size the check tool computes. Use it for anything that morphs."""
    t = (mono if mono_font else label)("|" + s, size, color, **kw)
    pipe = t[0]
    if len(t) > 1:
        pipe.move_to([t[1].get_center()[0], pipe.get_center()[1], 0])
    pipe.set_opacity(0)
    return t


def note(s: str, color=S.GREY, size: float = 20, **kw) -> Text:
    """A caption line (label font, GREY by default)."""
    return label(s, size, color, **kw)


# the instructor's name never appears (series rule); none is in this lecture's data, but every
# loader runs through unname() anyway
_NAME_RE = re.compile(r"Pavlos(?:[ _]Protopapas)?|Protopapas", re.IGNORECASE)


def unname(s: str) -> str:
    return _NAME_RE.sub("‹instructor›", s)


# ------------------------------------------------------------------ emoji (script.md "Emoji")
EMOJI_GLYPH = {"✅": "check", "❌": "cross", "💥": "burst", "💔": "heart", "✨": "sparkle", "🍰": "cake",
               "🏁": "flag"}


@lru_cache(maxsize=None)
def _mono_has(ch: str) -> bool:
    """True when the house mono font has a glyph for ch (fc-list); True if the check can't run."""
    try:
        res = subprocess.run(["fc-list", f":charset={ord(ch):x}", "family"], capture_output=True,
                             text=True, timeout=5).stdout
    except (OSError, subprocess.SubprocessError):
        return True
    return any("DejaVu Sans Mono" in f for f in res.splitlines())


def dropped_chars(s: str) -> list[str]:
    """Characters of s the house mono font cannot draw (they would vanish silently)."""
    return sorted({ch for ch in s if ord(ch) > 0x2000 and ch not in "…‹›·→←↔≈≠×⊘▶☑"
                   and not _mono_has(ch)})


def emo_line(s: str, size: float = 22, color=OUTPUT, t2c: dict | None = None) -> VGroup:
    """A mono_line that draws the captured emoji: ✅ as a GREEN check_mark, ❌ as a RED cross_mark,
    💥 💔 ✨ 🍰 🏁 as GREY one-cell boxes, each in two character cells (as a terminal does). Any other
    glyph the mono font lacks raises. .text has two spaces where an emoji sits (substring() keeps
    working on the words); .emoji = the drawn glyphs. t2c only for lines without emoji."""
    s = s.replace("️", "")
    bad = [ch for ch in dropped_chars(s) if ch not in EMOJI_GLYPH]
    if bad:
        raise ValueError(f"{s!r}: {bad!r} would vanish (the mono font has no glyph)")
    if not any(ch in EMOJI_GLYPH for ch in s):
        ln = mono_line(s, size, color, t2c=t2c)
        ln.emoji = VGroup()
        return ln
    filler, spots = "", []
    for ch in s:
        if ch in EMOJI_GLYPH:
            spots.append((len(filler), EMOJI_GLYPH[ch]))
            filler += "MM"
        else:
            filler += ch
    ln = mono_line(filler, size, color)
    cw = cell_width(size)
    ref_h = mono("M", size).height
    glyphs = VGroup()
    shown = list(filler)
    for i, kind in spots:
        ms = glyph_range(ln, i, i + 2)
        c = ms.get_center()
        if kind == "check":
            g = check_mark(ref_h * 1.15, PASS, stroke=4)
        elif kind == "cross":
            g = cross_mark(ref_h * 1.0, ERR, stroke=4)
        elif kind == "burst":            # 💥: ORANGE star burst with a YELLOW core (as S09 drew it)
            g = VGroup(Star(n=8, outer_radius=ref_h * 0.58, inner_radius=ref_h * 0.27, stroke_width=0)
                       .set_fill(S.ORANGE, 1),
                       Star(n=8, outer_radius=ref_h * 0.32, inner_radius=ref_h * 0.16, stroke_width=0)
                       .set_fill(S.YELLOW, 1).rotate(PI / 8))
        elif kind == "heart":            # 💔: RED heart with a dark zigzag crack
            def _pt(t):
                return np.array([16 * np.sin(t) ** 3,
                                 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t), 0]) / 32
            heart = ParametricFunction(_pt, t_range=[0, TAU], stroke_width=0).set_fill(ERR, 1)
            heart.scale_to_fit_height(ref_h * 1.0)
            top, bot = heart.get_top()[1] - ref_h * 0.19, heart.get_bottom()[1] + ref_h * 0.05
            cx, dx = heart.get_center()[0], ref_h * 0.1
            crack = VMobject(stroke_color=TERM_BG, stroke_width=3).set_points_as_corners(
                [[cx + (dx if k % 2 else -dx * 0.4), y, 0] for k, y in enumerate(np.linspace(top, bot, 5))])
            g = VGroup(heart, crack)
        elif kind == "sparkle":          # ✨: a small four-point GOLD star (no empty box)
            g = Star(n=4, outer_radius=ref_h * 0.62, inner_radius=ref_h * 0.2, stroke_width=0
                     ).set_fill(S.GOLD, 1)
        elif kind == "cake":             # 🍰: a slice drawn as a wedge with a cream top
            body = Polygon([-cw * 0.7, -ref_h * 0.5, 0], [cw * 0.7, -ref_h * 0.5, 0], [cw * 0.7, ref_h * 0.25, 0],
                           stroke_width=0).set_fill("#E8C9A0", 1)
            top = Polygon([-cw * 0.7, -ref_h * 0.5, 0], [cw * 0.7, ref_h * 0.25, 0], [cw * 0.7, ref_h * 0.45, 0],
                          [-cw * 0.7, -ref_h * 0.3, 0], stroke_width=0).set_fill(WHITE, 1)
            g = VGroup(body, top)
        elif kind == "flag":             # 🏁: a 2x2 chequered flag on a pole
            sq = ref_h * 0.32
            cells = VGroup(*[Square(sq, stroke_width=0).set_fill(WHITE if (r + c) % 2 == 0 else S.GREY, 1)
                             .move_to([c * sq, -r * sq, 0]) for r in range(2) for c in range(2)])
            pole = Line([-sq * 0.5, sq * 0.5, 0], [-sq * 0.5, -ref_h * 0.6, 0], stroke_width=2, color=S.GREY)
            g = VGroup(pole, cells)
        else:
            g = RoundedRectangle(width=cw * 1.5, height=ref_h * 1.1, corner_radius=0.04,
                                 stroke_color=S.GREY, stroke_width=2).set_fill(S.GREY, 0.2)
        g.move_to(c)
        glyphs.add(g)
        shown[i] = shown[i + 1] = "\x00"
    # drop the filler glyphs (both 'M's of every spot) from the line and its .glyphs
    drop = []
    for i, _ in spots:
        drop += list(glyph_range(ln, i, i + 2))
    for m in drop:
        ln.remove(m)
        ln.glyphs.remove(m)
    ln.text = "".join(" " if ch == "\x00" else ch for ch in shown)
    ln.add(*glyphs)
    ln.emoji = glyphs
    return ln


def disp_len(s: str) -> int:
    """Width of s in terminal cells (an emoji takes two)."""
    s = s.replace("️", "")
    return sum(2 if ch in EMOJI_GLYPH else 1 for ch in s)


# ------------------------------------------------------------------ the running example
USER = "student"
P_HOME = "student@laptop:~$"
P_LAPTOP = "student@laptop:~/cheese-app-ci-cd$"
T_LAPTOP = "laptop"
REPO = "cheese-app-ci-cd"
COURSE_REPO = "dlops-io/cheese-app-ci-cd"
COURSE_URL = "https://github.com/dlops-io/cheese-app-ci-cd.git"
YOUR_REPO_URL = "https://github.com/<you>/cheese-app-ci-cd.git"
YOUR_REPO = "<you>/cheese-app-ci-cd"
WEBHOOK_PH = "https://hooks.slack.com/services/<your-webhook-path>"
SECRET_NAME = "SLACK_WEBHOOK_URL"
MASKED = "***"
CHANNEL = "#build-alerts"
SHA, SHA_RUN2, SHA_RUN3, SHA_DEMO = "b8458ff", "2289d89", "2892b1b", "c3b227f"
IMAGE_TAG = "cheese-app-api:b8458ff…"
IMAGE_NAME = "cheese-app-api"
TAR = "/tmp/cheese-app-api.tar"
TAR_SIZE = "≈ 176 MB"
PART4 = "Part 4 · L09"              # tracker caption while README Part 4's fix is on screen (S12)

JOBS = [("build", "Build Docker Image"), ("lint-and-format", "Lint and Format Check"),
        ("unit-tests", "Unit Tests"), ("integration-tests", "Integration Tests"),
        ("system-tests", "System Tests"), ("test-summary", "Test Summary")]
JOB_IDS = tuple(j for j, _ in JOBS)
JOB_NAME = dict(JOBS)
SHORT = {"build": "Build", "lint-and-format": "Lint", "unit-tests": "Unit",
         "integration-tests": "Integration", "system-tests": "System", "test-summary": "Summary"}
NEEDS = {"build": [], "lint-and-format": ["build"], "unit-tests": ["build"],
         "integration-tests": ["build"], "system-tests": ["build"],
         "test-summary": ["unit-tests", "integration-tests", "system-tests"]}
MIDDLE = ("unit-tests", "integration-tests", "system-tests", "lint-and-format")   # screenshot order
TEST_JOBS = ("unit-tests", "integration-tests", "system-tests")
STRIP_BOXES = ("Commit", "Build Container", "Lint and Format", "Test", "Summary")     # slide 26
STRIP_PURPOSE = ("a push triggers it", "one image, same environment", "Black + Flake8",
                 "unit · integration · system", "pass / fail to the developers")      # slide 27
SCREENSHOT_TIMES = {"build": 54, "lint-and-format": 22, "unit-tests": 18, "integration-tests": 20,
                    "system-tests": 39, "test-summary": 4}                            # recorded
BILLED_MIN = {j: math.ceil(t / 60) for j, t in SCREENSHOT_TIMES.items()}             # all 1
VERSIONS = {"docker": "29.8.2", "git": "2.54.0", "pre-commit": "4.7.0", "black (hook)": "24.1.1",
            "flake8 (hook)": "7.0.0", "act": "0.2.97", "python (image)": "3.11.18",
            "black (image)": "26.10.1", "flake8 (image)": "7.5.0", "pytest (image)": "9.2.0",
            "pytest-cov (image)": "7.1.0"}
HYGIENE = ("trailing-whitespace", "end-of-file-fixer", "check-yaml", "check-added-large-files",
           "check-json", "check-merge-conflict", "detect-private-key")
TRIGGER_BRANCHES = ("main", "develop")
RUNS = ("run1", "run2", "run3", "run-demo")


# ------------------------------------------------------------------ trackers (script.md)
SECTIONS = {"P5": "Part 5: GitHub Actions (Remote CI)", "P6": "Part 6: Branch Protection (Optional)"}
STEPS = {
    "P5": ["Pipeline file", "Six jobs", "Key concepts", "git add", "git commit", "git push",
           "Actions tab", "Read results"],
    "P6": ["Add rule", "Pick checks", "New branch", "Break tests", "Commit, push", "Open PR"],
}
TRACKER_KEYS = tuple(SECTIONS)


def place_tracker(tr: ReadmeTracker) -> ReadmeTracker:
    """Pin a tracker to the house corner (left edge -6.5, top 3.5)."""
    tr.shift(np.array([TRACK_LEFT - tr.get_left()[0], TRACK_TOP - tr.get_top()[1], 0]))
    return tr


def _suffix(extra) -> str:
    if not extra:
        return ""
    return " · extra" if extra is True else f" · {extra}"


def _caption(tr: ReadmeTracker, k: int, extra) -> Text:
    if not k:
        return steady("", tr.size, tr.hi_color).next_to(tr.dots, RIGHT, buff=0.25)
    s = f"step {k} of {len(tr.steps)}: {tr.steps[k - 1]}"
    suf = _suffix(extra)
    if suf:
        t = steady(s + suf, tr.size, tr.hi_color, t2c={suf.strip(): S.GREY})
    else:
        t = steady(s, tr.size, tr.hi_color)
    return t.next_to(tr.dots, RIGHT, buff=0.25)


def tracker(key: str, step: int | None = None, extra=False) -> ReadmeTracker:
    """Tracker `key` ("P5", "P6") at `step` (1-based; None = no step lit yet), placed top-left.
    extra: True -> ' · extra' in GREY; a string -> ' · <string>' (PART4 = 'Part 4 · L09')."""
    tr = ReadmeTracker(SECTIONS[key], STEPS[key])
    if step:
        tr.set_step(step)
    tr.remove(tr.caption)
    tr.caption = _caption(tr, step or 0, extra)
    tr.add(tr.caption)
    tr.key, tr.extra = key, extra
    return place_tracker(tr)


def tracker_p5(step=None, extra=False): return tracker("P5", step, extra)   # noqa: E704
def tracker_p6(step=None, extra=False): return tracker("P6", step, extra)   # noqa: E704


def track(tr: ReadmeTracker, k: int | None = None, extra=False, run_time: float = 0.5):
    """ANIM: move the tracker to step k (None: stay) and set/clear the caption suffix.
    Use this, never tr.goto() (its caption morph reads as < 20 pt in the check)."""
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


def swap_tracker(scene, old: ReadmeTracker, new: ReadmeTracker, run_time: float = 0.6):
    """PLAYS: tracker `old` cross-fades into `new` in place (S15: P5 -> P6). Returns `new`."""
    scene.play(FadeOut(old), FadeIn(new), run_time=run_time)
    return new


def lref(slides: str) -> VGroup:
    """The GREY 'Lecture 21 · slides 25–28' tag, top right (only while that slide's idea is on
    screen). lref("21") reads 'slide 21'."""
    return lecture_ref(21, slides)


# ------------------------------------------------------------------ captures
_EXIT_RE = re.compile(r"^(.*?)\[exit (-?\d+)\]$")


class Capture:
    """One captured command. .cmd_lines (typed rows, line 1 without '$ ') .cmd (joined '\\n') .k
    (file lines of the command) .lines (output body, no [exit N]) .exit .raw (every file line, the
    exit marker removed) .path .run .job .nn (runner captures; None elsewhere) .step_name"""

    def __init__(self, cmd_lines, lines, exit_code, raw, path, k):
        self.cmd_lines, self.lines, self.exit, self.raw, self.path, self.k = \
            cmd_lines, lines, exit_code, raw, path, k
        self.cmd = "\n".join(cmd_lines)
        self.run = self.job = self.nn = self.step_name = None

    def line(self, n: int) -> str:
        """File line n (1-based). Refuses the command lines (typed / heading, never printed)."""
        if not 1 <= n <= len(self.raw):
            raise IndexError(f"{self.path.name} has {len(self.raw)} lines, not {n}")
        if n <= self.k:
            raise ValueError(f"{self.path.name}:{n} is part of the command (lines 1-{self.k}): "
                             "it is typed (terminal) or the heading (run log), never printed")
        return self.raw[n - 1]

    def at(self, *spec) -> list[str]:
        """Lines by FILE line numbers, as script.md writes them: ints, (a, b) inclusive ranges and
        '…' items (a literal '…' line). at(2, (4, 5), '…', 653, 656). Never adds '…' by itself."""
        res: list[str] = []
        for r in spec:
            if isinstance(r, str):
                res.append(r)
                continue
            a, b = (r, r) if isinstance(r, int) else r
            res += [self.line(n) for n in range(a, b + 1)]
        return res

    def pick(self, *ranges, ellipsis: str = "…") -> list[str]:
        """L1-style: output lines by 1-based ranges over the OUTPUT body (pick(1) = file line k+1);
        a gap inserts '…'. Negative numbers count from the end. Prefer .at()."""
        n = len(self.lines)
        res: list[str] = []
        last = None
        for r in ranges:
            a, b = (r, r) if isinstance(r, int) else r
            a = a if a > 0 else n + a + 1
            b = b if b > 0 else n + b + 1
            if last is not None and a > last + 1:
                res.append(ellipsis)
            res += self.lines[a - 1:b]
            last = b
        return res


def _resolve(name: str) -> Path:
    parts = [p for p in name.split("/") if p]
    if "capture-only" in parts:
        raise ValueError("capture-only/ is plumbing (the sandbox's own push): never shown")
    if parts[0] == "runner":
        parts = parts[1:]
    if parts[0] == "expected":
        raise ValueError("expected/ files are quotes, not captures: use recorded()")
    if parts[0] in RUNS or parts[0] == "noload":
        d = RUNNER.joinpath(*parts[:-1])
    elif parts[0] == "laptop":
        d = TERMINAL / "laptop"
        parts = parts[1:]
    elif len(parts) == 1:
        d = TERMINAL / "laptop"
    else:
        raise ValueError(f"capture {name!r}: laptop/NN, <run>/<job>/NN or noload/xN")
    stem = parts[-1][:-4] if parts[-1].endswith(".txt") else parts[-1]
    p = d / f"{stem}.txt"
    if not p.exists():
        hits = sorted(d.glob(f"{stem}-*.txt"))
        if len(hits) != 1:
            raise FileNotFoundError(f"capture {name}: {len(hits)} matches {[h.name for h in hits]} "
                                    "(see ASSETS.md)")
        p = hits[0]
    return p


@lru_cache(maxsize=None)
def _steps_file(run: str, job: str) -> tuple:
    p = RUNNER / run / job / "00-steps.txt"
    rows = []
    for n, s in enumerate(p.read_text(encoding="utf-8").rstrip("\n").split("\n"), start=1):
        m = re.match(r"^(\d\d)\s+(\w+)\s{2,}(.+?)(?:\s{2,}\((.+)\))?\s*$", s)
        if m:
            rows.append((n, m.group(2), m.group(3), m.group(4), int(m.group(1)), s))
    return tuple(rows)


class Step:
    """One row of a job's 00-steps.txt: .n (file line) .num (step number) .state .name .note"""

    def __init__(self, n, state, name, note_, num):
        self.n, self.state, self.name, self.note, self.num = n, state, name, note_, num

    def __repr__(self):
        return f"Step({self.num} {self.state} {self.name!r})"


def steps(run: str, job: str) -> list[Step]:
    """The step list of runner/<run>/<job>/00-steps.txt (line 1, the header with the full commit
    id, is never shown)."""
    return [Step(n, st, nm, nt, num) for n, st, nm, nt, num, _ in _steps_file(run, job)]


def job_result(run: str, job: str) -> str:
    s = (RUNNER / run / job / "00-steps.txt").read_text(encoding="utf-8")
    return re.search(r"job result: (\w+)", s).group(1)


@lru_cache(maxsize=None)
def _results(run: str) -> tuple:
    p = RUNNER / run / "results.txt"
    return tuple(tuple(s.split("=", 1)) for s in p.read_text(encoding="utf-8").split() if "=" in s)


def results(run: str) -> dict:
    """{job id: 'success' | 'failure'} from runner/<run>/results.txt."""
    return dict(_results(run))


def capture(name: str) -> Capture:
    """capture("04") / capture("laptop/62") / capture("run1/build/03") / capture("noload/x2").
    Fails loudly when missing or ambiguous: never show an uncaptured output. The command takes
    line 1 plus every '> ' row (a multi-line `run:` script) or row after a trailing '\\'.
    An '[exit N]' glued to the last output line (run1/system-tests/05) is split off."""
    p = _resolve(name)
    with open(p, encoding="utf-8", newline="") as f:
        text = f.read()
    raw = [unname(s.rstrip("\r").expandtabs(8)) for s in text.rstrip("\n").split("\n")]
    if not raw[0].startswith("$ "):
        raise ValueError(f"{p.name}: line 1 is not a '$ …' command")
    code_ = 0
    m = _EXIT_RE.match(raw[-1])
    if m:
        code_ = int(m.group(2))
        if m.group(1):
            raw[-1] = m.group(1)
        else:
            raw = raw[:-1]
    k = 1
    while k < len(raw) and (raw[k].startswith("> ") or raw[k] == ">" or raw[k - 1].rstrip().endswith("\\")):
        k += 1
    cmd_lines = [raw[0][2:]] + [r[2:] if r.startswith("> ") else r.lstrip(">") for r in raw[1:k]]
    c = Capture(cmd_lines, raw[k:], code_, raw, p, k)
    rel = p.relative_to(TERMINAL).parts
    if rel[0] == "runner":
        c.run = rel[1]
        c.job = rel[2] if len(rel) > 3 else "unit-tests"        # noload = the unit-tests job
        c.nn = p.name.split("-")[0]
        if c.nn.isdigit() and len(rel) > 3:
            for st in steps(c.run, c.job):
                if st.num == int(c.nn):
                    c.step_name = st.name
    return c


# ---- line transforms (script.md conventions)
_HEX_RE = re.compile(r"\b([0-9a-f]{7})(?:[0-9a-f]{57}|[0-9a-f]{33})\b")
_ADDR_RE = re.compile(r"\b172\.\d+\.\d+\.\d+:\d+")
_ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")


def crop(s: str) -> str:
    """Every 40- or 64-character hex id cut to 7 characters + '…' (script.md 'crop7')."""
    return _HEX_RE.sub(r"\1…", s)


def crop_addr(s: str) -> str:
    """The client addresses of a server log ('172.18.0.1:55228') become '…'."""
    return _ADDR_RE.sub("…", s)


def strip_ansi(s: str) -> str:
    return _ANSI_RE.sub("", s)


def cut(s: str, after: str, ellipsis: str = "…") -> str:
    """The line cut right after `after` (first occurrence), ending in '…'."""
    i = s.index(after) + len(after)
    return s[:i] + ellipsis


def from_phrase(s: str, phrase: str, ellipsis: str = "…") -> str:
    """The line from `phrase` on, after a '…'."""
    i = s.index(phrase)
    return ellipsis + s[i:] if i else s


def soft(lines, n: int = 65) -> list:
    """Long lines broken at their last space that fits `n` cells (the text is unchanged, only the
    row break moves). Items may be (text, colour)."""
    res = []
    for x in lines:
        s, c = (x, None) if isinstance(x, str) else x
        while disp_len(s) > n:
            k = s.rfind(" ", 0, n + 1)
            if k > 0 and s[:k].strip():
                res.append((s[:k].rstrip(), c))
                s = s[k + 1:]
            else:
                res.append((s[:n], c))
                s = s[n:]
        res.append((s, c))
    return [s if c is None else (s, c) for s, c in res]


def squeeze_spaces(s: str, keep: int = 2) -> str:
    """Runs of 3+ spaces inside a line become `keep` spaces (act's padded columns)."""
    return re.sub(r"(?<=\S) {3,}(?=\S)", " " * keep, s)


def act_lines(*nums) -> list[str]:
    """ACT(…): lines of laptop/62-act-push.txt by FILE line number (ints, (a, b), '…'), ANSI codes
    stripped, act's padding squeezed to two spaces, ids cropped."""
    c = capture("62")
    return [x if x == "…" else crop(squeeze_spaces(strip_ansi(x))) for x in c.at(*nums)]


def _table(lines):
    head = lines[0].rstrip()
    starts = [0] + [m.end() for m in re.finditer(r"\s{2,}", head)]
    ends = starts[1:] + [None]
    names = [head[a:b].strip() if b else head[a:].strip() for a, b in zip(starts, ends)]
    rows = [[(ln[a:b] if b else ln[a:]).strip() for a, b in zip(starts, ends)] for ln in lines]
    return names, rows


def cols(lines: list[str], names: list[str], gutter: int = 2) -> list[str]:
    """Only the named columns of a padded table (header row first), re-aligned: act -l with
    cols(c.at((3, 9)), ["Stage", "Job ID", "Job name"])."""
    heads, rows = _table(lines)
    idx = [heads.index(n) for n in names]
    w = [max(len(r[j]) for r in rows) for j in idx]
    return [(" " * gutter).join(r[j].ljust(w[i]) for i, j in enumerate(idx)).rstrip() for r in rows]


def md_plain(s: str) -> str:
    """Markdown stripped for a card: '**', backticks and link brackets go, list bullets become '•',
    headings lose their '#'."""
    s = s.rstrip()
    s = s.replace("**", "").replace("`", "")
    s = re.sub(r"!?\[([^\]]+)\]\([^)]+\)", r"\1", s)
    s = re.sub(r"^(\s*)[*-] ", r"\1• ", s)
    s = re.sub(r"^#+\s*", "", s)
    return s


def recorded(file: str, *nums, plain: bool = True) -> list[str]:
    """Lines of assets/terminal/expected/<file> ('readme-screenshot-run-graph') by FILE line number
    (ints or (a, b)). The '# …' provenance lines are refused."""
    stem = file[:-4] if file.endswith(".txt") else file
    p = EXPECTED / f"{stem}.txt"
    if not p.exists():
        hits = sorted(EXPECTED.glob(f"{stem}*.txt"))
        if len(hits) != 1:
            raise FileNotFoundError(f"expected/{stem}: {[h.name for h in hits]}")
        p = hits[0]
    raw = p.read_text(encoding="utf-8").rstrip("\n").split("\n")
    res = []
    for r in nums:
        a, b = (r, r) if isinstance(r, int) else r
        for n in range(a, b + 1):
            s = raw[n - 1]
            if s.startswith("# "):
                raise ValueError(f"{p.name}:{n} is a provenance header, never shown")
            res.append(unname(md_plain(s) if plain else s))
    return res


# ------------------------------------------------------------------ sources
_LANG = {".py": "python", ".toml": "toml", ".sh": "bash", ".md": "markdown", ".yaml": "yaml",
         ".yml": "yaml", ".ini": "ini", ".txt": "text", ".json": "json", ".diff": "diff"}


def _src(path: str) -> Path:
    """Repo-relative path ('.github/workflows/ci.yml'), 'history/<file>', or a full
    'cheese-app-ci-cd/…' / 'cheese-app-ci-cd-history/…' path."""
    if path.startswith("history/"):
        return SOURCE / HIST_DIR / path[len("history/"):]
    if path.startswith(REPO_DIR + "/") or path.startswith(HIST_DIR + "/"):
        return SOURCE / path
    return SOURCE / REPO_DIR / path


def source_text(path: str) -> str:
    return unname(_src(path).read_text(encoding="utf-8"))


def excerpt(path: str, first: int, last: int) -> str:
    """Lines first..last (1-based, inclusive) of a source file."""
    return "\n".join(source_text(path).split("\n")[first - 1:last])


def shown_path(path: str) -> str:
    """The header name: repo-relative for the clone; 'c3b227f · service.py' for history files;
    '199abd9 → 1a5e363 · ci.yml (diff)' for the diff."""
    p = _src(path)
    if p.parent.name == HIST_DIR:
        m = re.match(r"([0-9a-f]{7})-to-([0-9a-f]{7})-(.+)\.diff$", p.name)
        if m:
            return f"{m.group(1)} → {m.group(2)} · {m.group(3)} (diff)"
        m = re.match(r"([0-9a-f]{7})-(.+)$", p.name)
        return f"{m.group(1)} · {m.group(2)}" if m else p.name
    return str(p.relative_to(SOURCE / REPO_DIR))


def readme(n: int) -> str:
    """README.md line n, stripped (assert cap.cmd == readme(346))."""
    return excerpt("README.md", n, n).strip()


def readme_lines(a: int, b: int) -> list[tuple[int, str]]:
    """[(file line, text)] of README a..b, markdown stripped, blank lines and fences dropped."""
    rows = source_text("README.md").split("\n")[a - 1:b]
    res = []
    for i, s in enumerate(rows, start=a):
        if not s.strip() or s.strip().startswith("```"):
            continue
        res.append((i, md_plain(s)))
    return res


def code(path: str, first: int, last: int | None = None, language: str | None = None, focus=None,
         font_size: float = 22, shown: str | None = None, max_lines: int = 12, panel_w: float = 12.6):
    """CODE(path: first–last): a code_panel quoting the source file, header '<shown> · lines a–b'.
    ≤ 12 lines; raises when a line would make the panel wider than panel_w (22 pt ~65 characters,
    20 pt ~72). .code .header; code_span(p.code, k, "x"), line_bar(p.code, k, colour), k = file
    line - first."""
    last = first if last is None else last
    if last - first + 1 > max_lines:
        raise ValueError(f"CODE {path}: {last - first + 1} lines; never more than {max_lines} on screen")
    name = Path(path).name
    if language is None:
        language = "docker" if name.startswith("Dockerfile") else _LANG.get(Path(name).suffix, "text")
    p = code_panel(excerpt(path, first, last), shown or shown_path(path), first, language,
                   focus=focus, font_size=font_size)
    if p.width > panel_w + 1e-6:
        src = excerpt(path, first, last).split("\n")
        k = max(range(len(src)), key=lambda i: len(src[i]))
        raise ValueError(f"CODE {path}:{first + k} makes the panel {p.width:.2f} wide (> {panel_w}): "
                         "use font_size=20 or a narrower window")
    return p


def code_strip(path: str, line: int, font_size: float = 22) -> VGroup:
    """A one-line code panel (S05's needs lines, S08's runs-on lines). Swap it with Transform."""
    return code(path, line, line, font_size=font_size)


def readme_panel(a: int, b: int, lines=None, card_w: float | None = None, size: float = 22,
                 colors: dict | None = None) -> VGroup:
    """README(a–b): a GREY README card, header 'README.md · lines a–b' (or 'line a'), the README's
    own words (markdown stripped, list markers kept, blank lines dropped). lines= a subset of file
    lines to show (header still says a–b). colors={file line: colour}. Long lines are soft-wrapped
    to card_w (default: fit, at most 12.4). .frame .head .body .rows{file line: Text or VGroup}"""
    colors = colors or {}
    items = [(n, s) for n, s in readme_lines(a, b) if lines is None or n in lines]
    max_w = (card_w or 12.4) - 0.6
    body, rows = VGroup(), {}
    for n, s in items:
        words, cur, parts = s.split(" "), "", []
        for w in words:
            trial = (cur + " " + w) if cur else w
            if cur and label(trial, size).width > max_w:
                parts.append(cur)
                cur = w
            else:
                cur = trial
        parts.append(cur)
        g = VGroup(*[label(p_, size, colors.get(n, INK)) for p_ in parts]).arrange(DOWN, aligned_edge=LEFT,
                                                                                buff=0.08)
        if len(parts) > 1:
            for p_ in g[1:]:
                p_.shift(RIGHT * 0.3)
        rows[n] = g if len(parts) > 1 else g[0]
        body.add(g)
    body.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    where = f"line {a}" if a == b else f"lines {a}–{b}"
    head = VGroup(mono("README.md", CAPTION, S.GREY), label(f"· {where}", CAPTION, S.GREY)).arrange(RIGHT, buff=0.12)
    inner = VGroup(head, body).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    frame = box(card_w or inner.width + 0.55, inner.height + 0.4, S.GREY, fill=S.GREY_DARKER,
                fill_opacity=1)
    inner.move_to(frame).align_to(frame, LEFT).shift(RIGHT * 0.28)
    g = VGroup(frame, inner)
    g.frame, g.head, g.body, g.rows = frame, head, body, rows
    return g


# ------------------------------------------------------------------ terminals
def term(prompt: str = P_LAPTOP, rows: int = 10, title: str | None = T_LAPTOP, width: float = 12.6,
         size: float = 22, place: bool = True) -> Terminal:
    """The house terminal: 12.6 wide, 22 pt, 65 characters a row, centred, bottom edge at BOTTOM.
    Height = rows x 0.403 + 0.85. Full width, or a 3-row strip (rows=3) under a picture."""
    t = Terminal(prompt=prompt, width=width, rows=rows, size=size, title=title)
    if place:
        t.shift(np.array([-t.box.get_center()[0], BOTTOM - t.box.get_bottom()[1], 0]))
    return t


def laptop_term(rows: int = 10, prompt: str = P_LAPTOP) -> Terminal:
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
        scene.play(FadeOut(VGroup(*gone)), run_time=0.25)
        for ln in gone:
            t.lines.remove(ln)
            scene.remove(ln)
    anims = [Transform(t.box, ref.box), Transform(t.bar, ref.bar), t.dots.animate.move_to(ref.dots)]
    if t.title is not None:
        anims.append(t.title.animate.move_to(ref.title))
    for i, ln in enumerate(kept):
        anims.append(ln.animate.shift(ref._slot(i) - ln.strut.get_corner(UL)))
    scene.play(*anims, *extra, run_time=run_time)
    t.rows = rows
    scene.add(t)
    return t


def room(scene, t: Terminal, n: int, run_time: float = 0.3) -> None:
    """PLAYS: make room for n new rows the gentle way: the oldest rows fade where they are, then the
    rest slide up."""
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


def type_cmd(scene, t: Terminal, cmd: str, type_time: float | None = None, prompt: bool = True):
    """PLAYS: type at the waiting prompt (replacing a bare prompt line if there is one; room is made
    first). A long command folds at a space outside quotes with ' \\' (Terminal.fold). prompt=False
    types a continuation row with no prompt. Returns the line, or a VGroup with .rows."""
    if len(t.lines) and getattr(t.lines[-1], "bare", False):
        last = t.lines[-1]
        t.lines.remove(last)
        scene.remove(last, *last.submobjects)
    keep = t.prompt
    if not prompt:
        t.set_prompt("")
    try:
        p = t.prompt + (" " if t.prompt else "")
        room(scene, t, len(t.fold(p + cmd, first_prefix=len(p))))
        ln = t.type(scene, cmd, type_time)
    finally:
        t.set_prompt(keep)
    return ln


def type_capture(scene, t: Terminal, cap, type_time: float | None = None) -> list:
    """PLAYS: type a capture's command exactly as line 1 spells it (cap: a Capture or a name); rows
    after a trailing '\\' are continuations. Returns the typed lines."""
    cap = capture(cap) if isinstance(cap, str) else cap
    res, cont = [], False
    for row in cap.cmd_lines:
        res.append(type_cmd(scene, t, row, type_time, prompt=not cont))
        cont = row.rstrip().endswith("\\")
    return res


def out(scene, t: Terminal, lines, wrap: bool = False, run_time: float = 0.6, lag: float = 0.08,
        chunk: int | None = None, color=OUTPUT) -> VGroup:
    """PLAYS: print capture lines (text or (text, colour)) in chunks that fit the box, making room the
    gentle way; emoji are drawn (emo_line). wrap=True breaks long lines at their last space that fits
    (soft()); otherwise a line longer than the row is refused (cut it, crop it, or wrap)."""
    items = soft(lines, t.max_chars) if wrap else list(lines)
    for x in items:
        s = x if isinstance(x, str) else x[0]
        if disp_len(s) > t.max_chars:
            raise ValueError(f"out(): {disp_len(s)} > {t.max_chars} cells: wrap=True or cut it: {s!r}")
    items = [(x, color) if isinstance(x, str) else x for x in items]
    k = max(1, min(t.rows, chunk or t.rows))
    chunks = [items[i:i + k] for i in range(0, len(items), k)]
    rows = VGroup()
    for ch in chunks:
        room(scene, t, len(ch))
        new = VGroup()
        for s, col in ch:
            ln = emo_line(s, t.size, col)
            t._place(ln, len(t.lines))
            t.lines.add(ln)
            new.add(ln)
        scene.play(LaggedStart(*[FadeIn(m) for m in new], lag_ratio=lag),
                   run_time=run_time / len(chunks) + 0.1)
        rows.add(*new)
    return rows


def cd_prompt(scene, t: Terminal, new_prompt: str, color=TURN, run_time: float = 0.6):
    """PLAYS: after `cd`, the prompt changes; a bare prompt line appears and its path flashes."""
    t.set_prompt(new_prompt)
    ln = bare_prompt(scene, t)
    path = new_prompt.split(":", 1)[1].rstrip("$# ")
    scene.play(*[g.animate.set_color(color) for g in substring(ln, path)], run_time=run_time * 0.5)
    scene.play(*[g.animate.set_color(PROMPT_PATH) for g in substring(ln, path)], run_time=run_time * 0.5)
    scene.add(t)
    return ln


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
    lft, rgt, bot, top = mob.get_left()[0], mob.get_right()[0], mob.get_bottom()[1], mob.get_top()[1]
    return any(lft < ch.get_right()[0] + 0.03 and rgt > ch.get_left()[0] - 0.03
               and bot < ch.get_top()[1] and top > ch.get_bottom()[1]
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
                         "use on_bar() or under_term()")
    scene.play(anim or FadeIn(mob, shift=LEFT * 0.1), run_time=run_time)
    return attach(scene, row, mob)


def unpin(scene, line, mob, *extra, run_time: float = 0.3):
    """PLAYS: fade a pinned mark out and take it off its row (so it never snaps back)."""
    row = _row_of(line)
    scene.play(FadeOut(mob), *extra, run_time=run_time)
    if mob in row.submobjects:
        row.remove(mob)
    scene.remove(mob)


def on_bar(t: Terminal, mob, buff: float = 0.15):
    """Put a row-sized tag on terminal t's title bar, at its right end (for a row too long to hold
    a tag beside it). FadeIn it yourself (it does not scroll)."""
    return mob.move_to([t.box.get_right()[0] - buff - mob.width / 2, t.box.get_top()[1] - t.bar_h / 2, 0])


def under_term(t: Terminal, mob, buff: float = 0.12):
    """Put `mob` just above terminal t's top edge, right-aligned (chips 'about' the terminal)."""
    return mob.next_to(t.box, UP, buff=buff).align_to(t.box, RIGHT)


def row_tag(parts, color=S.GREY, size: float = 20) -> VGroup:
    """A tag that fits inside one 22 pt terminal row (0.36 tall). parts: a string, or
    (text, 'mono'|'label') pairs. .box .text"""
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
    """'▶ your turn' sized for a terminal row (YELLOW): pin(self, ln, beside(turn_row(), ln))."""
    return row_tag("▶ your turn", TURN)


def extra_row(kind=None) -> VGroup:
    """'extra' sized for a terminal row (GREY)."""
    return row_tag("extra" + (f" · {kind}" if kind else ""), S.GREY)


def time_row() -> VGroup:
    """'at the time of recording' sized for a terminal row (GREY)."""
    return row_tag("at the time of recording", S.GREY)


def flash_tag(scene, tg, color=None, scale: float = 1.12, run_time: float = 0.8) -> None:
    """PLAYS: flash a tag's words and pulse an unfilled copy of its outline (then drops the copy).
    Never Indicate a whole tag (its filled box would hide the word)."""
    color = color or tg.text.get_color()
    edge = tg.box.copy().set_fill(opacity=0)
    scene.play(Indicate(tg.text, color=color, scale_factor=scale),
               edge.animate(rate_func=there_and_back).set_stroke(width=4), run_time=run_time)
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
    """A translucent bar behind glyphs `g` (add it behind: self.add_to_back or insert in a row)."""
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
    """GREY 'extra' tag; kind 'act' -> 'extra · act'."""
    return tag("extra" + (f" · {kind}" if kind else ""), S.GREY)


def illustration_tag(s: str = "illustration") -> VGroup:
    """On every GitHub page drawing, the Slack card, the wish-list card ('illustration · colors from
    our live runs', 'illustration · from our live runs')."""
    return tag(s, S.GREY)


def recorded_tag(source: str | None = "README screenshot") -> VGroup:
    """'recorded · README screenshot': the screenshot's transcription and its timings."""
    return tag("recorded" + (f" · {source}" if source else ""), S.GREY)


def recording_tag(s: str = "at the time of recording") -> VGroup:
    """Beside versions on first show."""
    return tag(s, S.GREY)


def erratum_tag(s: str = "erratum") -> VGroup:
    """On every README / slide slip (the narration says 'a small slip', 'a kind note')."""
    return tag(s, S.GREY)


def standin_tag(s: str = "live · stand-in runner") -> VGroup:
    """On every job-log panel (run_log adds it)."""
    return tag(s, S.GREY)


def shown_tag(s: str = "shown, not run") -> VGroup:
    """On code cards with commands we do not run (set-url with <you>, Part 6's push / PR)."""
    return tag(s, S.GREY)


def expected_tag(source: str | None = None) -> VGroup:
    return tag("expected" + (f" · {source}" if source else ""), S.GREY)


def cost_tag(s: str) -> VGroup:
    """The GOLD money tag (Actions minutes, artifact storage, protection on private repos).
    Raises on '$', 'cents', 'free tier': no price anywhere."""
    return tag(_no_amount(s), COST)


def grey_chip(s: str, size: float = 20, mono_font: bool = False, color=S.GREY) -> VGroup:
    """A chip for a short note. .box .text"""
    return chip(s, color, size=size, font=MONO if mono_font else None)


def dashed_chip(s: str, color=PAST, size: float = 20, mono_font: bool = False) -> VGroup:
    """A dashed chip: the past / future (L09, L23), and things that never ran (skipped). .box .text"""
    t = mono(s, size, color) if mono_font else label(s, size, color)
    ob = outline_box(t.width + 0.48, mono("|", size).height + 0.24, color, solid=False)
    t.move_to(ob)
    g = VGroup(ob, t)
    g.box, g.text = ob, t
    return g


def tool_chip(s: str, size: float = 20) -> VGroup:
    """A tool as a PURPLE mono chip (never a logo): black, flake8, pytest, act, pre-commit …"""
    return chip(s, TOOL, size=size, font=MONO)


def ok_chip(s: str, size: float = 20, mono_font: bool = False) -> VGroup:
    return chip(s, PASS, size=size, font=MONO if mono_font else None)


def err_chip(s: str, size: float = 20, mono_font: bool = False) -> VGroup:
    return chip(s, ERR, size=size, font=MONO if mono_font else None)


def route_chip(s: str, size: float = 20, mono_font: bool = True) -> VGroup:
    """PINK: events, routes, tokens ('success', 'localhost:9000', 'POST')."""
    return chip(s, ROUTE, size=size, font=MONO if mono_font else None)


def image_chip(s: str = IMAGE_TAG, size: float = 20) -> VGroup:
    """TEAL mono chip: the image tag."""
    return chip(s, IMAGE, size=size, font=MONO)


def shared_chip(s: str, size: float = 20, mono_font: bool = False) -> VGroup:
    """ORANGE: the course's repo, Docker Hub, port 9000."""
    return chip(s, SHARED, size=size, font=MONO if mono_font else None)


def github_chip(s: str, size: float = 20, mono_font: bool = False) -> VGroup:
    """BLUE: GitHub, a runner, your repository."""
    return chip(s, GITHUB, size=size, font=MONO if mono_font else None)


def question_card(text: str, size: float = 24, card_w: float | None = None) -> VGroup:
    """A YELLOW-outlined card holding a question ('\\n' separates lines): S01's 'Which machine said
    no …', S16's test-yourself cards. .frame .text"""
    t = VGroup(*[label(s, size, INK) for s in text.split("\n")]).arrange(DOWN, buff=0.12)
    fr = RoundedRectangle(width=card_w or t.width + 0.6, height=t.height + 0.45, corner_radius=0.16,
                          stroke_color=TURN, stroke_width=3).set_fill(S.BG, 0.96)
    t.move_to(fr)
    g = VGroup(fr, t)
    g.frame, g.text = fr, t
    return g


def ponder(scene, question: str, seconds: float = 8.0) -> VGroup:
    """PLAYS: the silent YELLOW ponder timer (pause_and_ponder). FadeOut the card at the next block."""
    return pause_and_ponder(scene, question, seconds=seconds)


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


def _pt(a):
    return a if isinstance(a, np.ndarray) else a.get_center()


def arrow(a, b, color=S.GREY, stroke: float = 3, buff: float = 0.12) -> Arrow:
    """A plain thin arrow between two mobjects or points."""
    return Arrow(_pt(a), _pt(b), buff=buff if not isinstance(a, np.ndarray) else 0, color=color,
                 stroke_width=stroke, tip_length=0.18, max_tip_length_to_length_ratio=0.25)


def route(a, b, arc: float = 0.0, color=ROUTE, stroke: float = 4, dashed: bool = False):
    """A PINK route arrow (curved by `arc` radians) from a to b (points or mobjects)."""
    ar = Arrow(_pt(a), _pt(b), buff=0.15 if not isinstance(a, np.ndarray) else 0, path_arc=arc, color=color,
               stroke_width=stroke, tip_length=0.2, max_tip_length_to_length_ratio=0.2)
    if dashed:
        body = DashedVMobject(VMobject().set_points(ar.get_points()), num_dashes=16).set_stroke(color, stroke)
        return VGroup(body, ar.tip.copy()) if ar.tip is not None else body
    return ar


def travel(mob, path, run_time: float = 1.2):
    """ANIM: `mob` rides along `path` (a Line/Arrow/VMobject)."""
    return MoveAlongPath(mob, path, run_time=run_time)


def bounce(mob, point, run_time: float = 0.9):
    """ANIM: `mob` goes to `point` and comes back."""
    back = mob.get_center().copy()
    return Succession(mob.animate(run_time=run_time * 0.5).move_to(point),
                      mob.animate(run_time=run_time * 0.5).move_to(back))


def dot(color=PASS, r: float = 0.13) -> Dot:
    """A commit dot."""
    return Dot(radius=r, color=color)


def state_mark(state: str = "idle", h: float = 0.3) -> VGroup:
    """GitHub-like status mark: 'success' GREEN check in a ring, 'failure' RED cross in a ring,
    'skipped' GREY dashed ring with a slash, 'running' YELLOW dot in a ring, 'idle' GREY ring."""
    col = STATE_COLOR.get(state, S.GREY)
    r = h / 2
    if state == "skipped":
        c = DashedVMobject(Circle(radius=r), num_dashes=10).set_stroke(col, 2.5)
        inner = Line([-r * 0.6, -r * 0.6, 0], [r * 0.6, r * 0.6, 0], color=col, stroke_width=2.5)
    else:
        c = Circle(radius=r, stroke_color=col, stroke_width=2.5).set_fill(col, 0.15 if state != "idle" else 0)
        if state == "success":
            inner = check_mark(h * 0.62, col, stroke=3.5)
        elif state == "failure":
            inner = cross_mark(h * 0.5, col, stroke=3.5)
        elif state == "running":
            inner = Dot(radius=r * 0.45, color=col)
        else:
            inner = VMobject()
    inner.move_to(c)
    g = VGroup(c, inner)
    g.state = state
    return g


def script_glyph(h: float = 0.4) -> VGroup:
    """A '>_' shell-script glyph (a `run:` step). The text is 20 pt."""
    t = mono(">_", 20, INK)
    b = RoundedRectangle(width=max(h * 1.3, t.width + 0.16), height=h, corner_radius=0.06,
                         stroke_color=S.GREY, stroke_width=2).set_fill(TERM_BG, 1)
    t.move_to(b)
    return VGroup(b, t)


def puzzle_glyph(h: float = 0.36, color=TOOL) -> VGroup:
    """A PURPLE puzzle piece (a `uses:` step: a reusable action)."""
    sq = Square(side_length=h * 0.8, stroke_color=color, stroke_width=2.5).set_fill(color, 0.3)
    k1 = Circle(radius=h * 0.14, stroke_color=color, stroke_width=2.5).set_fill(color, 0.3)
    k1.move_to(sq.get_right() + RIGHT * h * 0.1)
    k2 = k1.copy().move_to(sq.get_top() + UP * h * 0.1)
    return VGroup(sq, k1, k2)


def spark(color=ROUTE, r: float = 0.28, n: int = 8) -> VGroup:
    """A burst of short rays (an event fires)."""
    rays = VGroup(*[Line(RIGHT * r * 0.45, RIGHT * r, color=color, stroke_width=3)
                    .rotate(k * TAU / n, about_point=ORIGIN) for k in range(n)])
    return rays


def runner_icon(h: float = 0.5, lit: bool = False, color=GITHUB) -> VGroup:
    """A small BLUE machine (a GitHub-hosted runner). lit=True fills it."""
    w = h * 1.3
    b = RoundedRectangle(width=w, height=h, corner_radius=0.06, stroke_color=color if lit else S.GREY,
                         stroke_width=2.5).set_fill(color if lit else S.GREY, 0.45 if lit else 0.08)
    lines = VGroup(*[Line(LEFT * w * 0.3, RIGHT * w * 0.3, stroke_width=2,
                          color=color if lit else S.GREY) for _ in range(2)]).arrange(DOWN, buff=h * 0.22)
    lines.move_to(b)
    g = VGroup(b, lines)
    g.lit = lit
    return g


def laptop_icon(w: float = 1.0) -> VGroup:
    """A GREY laptop glyph (devops.laptop)."""
    return laptop(w, LAPTOP)


def cube_glyph(side: float = 0.8, color=IMAGE) -> VGroup:
    """A TEAL cube (the image)."""
    d = side * 0.3
    front = Square(side_length=side, stroke_color=color, stroke_width=2.5).set_fill(color, 0.35)
    top = Polygon(front.get_corner(UL), front.get_corner(UL) + np.array([d, d, 0]),
                  front.get_corner(UR) + np.array([d, d, 0]), front.get_corner(UR),
                  stroke_color=color, stroke_width=2.5).set_fill(color, 0.55)
    sidep = Polygon(front.get_corner(UR), front.get_corner(UR) + np.array([d, d, 0]),
                    front.get_corner(DR) + np.array([d, d, 0]), front.get_corner(DR),
                    stroke_color=color, stroke_width=2.5).set_fill(color, 0.2)
    g = VGroup(front, top, sidep)
    return g.move_to(ORIGIN)


def suitcase_glyph(h: float = 0.6, color=IMAGE) -> VGroup:
    """A TEAL tar 'suitcase' (the saved image)."""
    w = h * 1.45
    body = RoundedRectangle(width=w, height=h, corner_radius=h * 0.14, stroke_color=color,
                            stroke_width=2.5).set_fill(color, 0.35)
    handle = Arc(radius=h * 0.2, start_angle=0, angle=PI, color=color, stroke_width=3)
    handle.next_to(body, UP, buff=0)
    straps = VGroup(*[Line(UP * h / 2, DOWN * h / 2, color=color, stroke_width=2).shift(RIGHT * x)
                      for x in (-w * 0.25, w * 0.25)]).move_to(body)
    return VGroup(body, handle, straps)


def shelf(w: float = 1.6, size: float = 20, text: str | None = "Docker", color=S.GREY) -> VGroup:
    """An (empty) 'Docker' shelf: a board with its caption on the left. .board .text"""
    board = Line(LEFT * w / 2, RIGHT * w / 2, color=color, stroke_width=4)
    g = VGroup(board)
    g.board, g.text = board, None
    if text:
        t = label(text, size, color).next_to(board, LEFT, buff=0.12).align_to(board, DOWN).shift(UP * 0.02)
        g.add(t)
        g.text = t
    return g


def bell_glyph(h: float = 0.6, color=S.GREY, slashed: bool = False) -> VGroup:
    """A bell (post-receive, the Slack bell). slashed=True adds a RED slash (.slash)."""
    w = h * 0.9
    body = VMobject(stroke_color=color, stroke_width=3).set_fill(color, 0.2)
    pts = [[-w * 0.5, -h * 0.3, 0], [-w * 0.35, -h * 0.15, 0], [-w * 0.32, h * 0.2, 0],
           [0, h * 0.42, 0], [w * 0.32, h * 0.2, 0], [w * 0.35, -h * 0.15, 0], [w * 0.5, -h * 0.3, 0]]
    body.set_points_smoothly(pts)
    rim = Line([-w * 0.5, -h * 0.3, 0], [w * 0.5, -h * 0.3, 0], color=color, stroke_width=3)
    clap = Dot([0, -h * 0.42, 0], radius=h * 0.08, color=color)
    g = VGroup(body, rim, clap)
    g.slash = None
    if slashed:
        sl = Line([-w * 0.55, -h * 0.5, 0], [w * 0.55, h * 0.5, 0], color=ERR, stroke_width=4)
        g.add(sl)
        g.slash = sl
    return g


def ring_waves(mob, color=ROUTE, n: int = 3) -> VGroup:
    """Three small arcs right of `mob` (a bell ringing, a door knocked)."""
    c = mob.get_right() + RIGHT * 0.1
    return VGroup(*[Arc(radius=0.15 + 0.13 * k, start_angle=-PI / 4, angle=PI / 2, color=color,
                        stroke_width=3, arc_center=c) for k in range(n)])


def hourglass(h: float = 0.6, color=S.GREY) -> VGroup:
    w = h * 0.7
    top = Polygon([-w / 2, h / 2, 0], [w / 2, h / 2, 0], [0, 0, 0], stroke_color=color, stroke_width=2.5)
    bot = Polygon([-w / 2, -h / 2, 0], [w / 2, -h / 2, 0], [0, 0, 0], stroke_color=color, stroke_width=2.5)
    sand_top = Polygon([-w * 0.35, h * 0.35, 0], [w * 0.35, h * 0.35, 0], [0, 0.02, 0],
                       stroke_width=0).set_fill(TURN, 0.6)
    sand_bot = Polygon([-w * 0.42, -h * 0.45, 0], [w * 0.42, -h * 0.45, 0], [0, -h * 0.2, 0],
                       stroke_width=0).set_fill(TURN, 0.6)
    g = VGroup(top, bot, sand_top, sand_bot)
    g.sand_top, g.sand_bot = sand_top, sand_bot
    return g


def key_file(h: float = 0.6, color=S.GREY) -> VGroup:
    """A file with a key on it (a private key file; no content)."""
    f = file_glyph(h, color)
    k = VGroup(Circle(radius=h * 0.1, stroke_color=color, stroke_width=2.5),
               Line(ORIGIN, RIGHT * h * 0.28, color=color, stroke_width=2.5))
    k[1].next_to(k[0], RIGHT, buff=0)
    k.move_to(f).shift(DOWN * h * 0.08)
    return VGroup(f, k)


def cursor_dot() -> VGroup:
    """A GREY click (cursor) dot with a ring."""
    return VGroup(Dot(radius=0.07, color=S.GREY), Circle(radius=0.16, stroke_color=S.GREY, stroke_width=2))


def door_glyph(text: str = "9000", color=SHARED, door_h: float = 0.8, size: float = 20) -> VGroup:
    """A door with a number plate above it (a published port). .frame .text"""
    fr = RoundedRectangle(width=door_h * 0.55, height=door_h, corner_radius=0.05, stroke_color=color,
                          stroke_width=3).set_fill(color, 0.15)
    knob = Dot(fr.get_right() + LEFT * door_h * 0.12, radius=0.04, color=color)
    t = mono(text, size, color).next_to(fr, UP, buff=0.08)
    g = VGroup(fr, knob, t)
    g.frame, g.text = fr, t
    return g


def gate_glyph(gate_h: float = 0.62, gate_w: float = 0.7, color=S.GREY) -> VGroup:
    """A gate: two posts and a bar. .bar .posts; open: Rotate(g.bar, PI / 2.3, about_point=g.hinge)."""
    pl = Line(DOWN * gate_h / 2, UP * gate_h / 2, color=color, stroke_width=4).shift(LEFT * gate_w / 2)
    pr = pl.copy().shift(RIGHT * gate_w)
    bar = Line(LEFT * gate_w / 2, RIGHT * gate_w / 2, color=color, stroke_width=6)
    g = VGroup(pl, pr, bar)
    g.bar, g.posts = bar, VGroup(pl, pr)
    return g


def dashed_copy(group, color=S.GREY, stroke: float = 3, n: int = 5) -> VGroup:
    """A dashed copy of every stroked piece of `group` (a skipped gate, a ghost)."""
    return VGroup(*[DashedVMobject(m.copy(), num_dashes=n).set_stroke(color, stroke)
                    for m in group.family_members_with_points()])


def exit_badge(code: int, size: float = 20) -> VGroup:
    """'exit N' badge for a run-log panel edge: GREY text; RED outline when N != 0."""
    t = label(f"exit {code}", size, S.GREY)
    h = mono("|", size).height + 0.14
    b = RoundedRectangle(width=t.width + 0.36, height=h, corner_radius=h / 2,
                         stroke_color=ERR if code else S.GREY, stroke_width=2.5).set_fill(S.BG, 1)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text, g.code = b, t, code
    return g


def github_box(text: str = "GitHub", box_w: float = 2.4, box_h: float = 1.2, size: float = 24) -> VGroup:
    """GitHub as a BLUE rounded box with its name (never a logo). .frame .text"""
    fr = box(box_w, box_h, GITHUB, fill_opacity=0.12, radius=0.2)
    t = label(text, size, GITHUB).move_to(fr)
    g = VGroup(fr, t)
    g.frame, g.text = fr, t
    return g


def chat_window(title: str = CHANNEL, rows=(), win_w: float = 4.6, win_h: float = 3.0,
                size: float = 20) -> VGroup:
    """A GREY chat window (never a logo): title bar with the channel name, rows (strings or mobjects)
    stacked from the top. .frame .title .body (the area rectangle) .rows"""
    fr = RoundedRectangle(width=win_w, height=win_h, corner_radius=0.14, stroke_color=S.GREY,
                          stroke_width=2.5).set_fill(PANEL, 1)
    bar_h = 0.48
    sep = Line(fr.get_corner(UL) + DOWN * bar_h, fr.get_corner(UR) + DOWN * bar_h, color=S.GREY_DARK,
               stroke_width=2)
    t = mono(title, size, S.GREY).move_to(fr.get_top() + DOWN * bar_h / 2).align_to(fr, LEFT).shift(RIGHT * 0.25)
    body = Rectangle(width=win_w - 0.3, height=win_h - bar_h - 0.25, stroke_width=0, fill_opacity=0)
    body.move_to(fr.get_bottom() + UP * (win_h - bar_h) / 2)
    rs = VGroup(*[label(r, size, INK) if isinstance(r, str) else r for r in rows])
    if len(rs):
        rs.arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(sep, DOWN, buff=0.2).align_to(body, LEFT)
    g = VGroup(fr, sep, t, body, rs)
    g.frame, g.title, g.body, g.rows = fr, t, body, rs
    return g


def vault_glyph(h: float = 1.0, color=GITHUB) -> VGroup:
    """A BLUE vault (repository secrets)."""
    b = RoundedRectangle(width=h * 1.1, height=h, corner_radius=0.1, stroke_color=color,
                         stroke_width=3).set_fill(color, 0.12)
    dial = Circle(radius=h * 0.22, stroke_color=color, stroke_width=3)
    spokes = VGroup(*[Line(ORIGIN, UP * h * 0.2, color=color, stroke_width=2.5).rotate(k * TAU / 4, about_point=ORIGIN)
                      for k in range(4)])
    VGroup(dial, spokes).move_to(b)
    return VGroup(b, dial, spokes)


def gh_page(crumb: str, page_w: float = 6.0, page_h: float = 4.0, size: float = 20) -> VGroup:
    """A schematic GitHub page (BLUE frame, never a screenshot): a GREY breadcrumb on top
    ('Settings → Branches'), a separator, and .body (the area below) to place rows in.
    Tag it illustration_tag(). .frame .crumb .body"""
    fr = RoundedRectangle(width=page_w, height=page_h, corner_radius=0.16, stroke_color=GITHUB,
                          stroke_width=2.5).set_fill(PANEL, 1)
    cr = label(crumb, size, S.GREY)
    cr.move_to(fr.get_top() + DOWN * 0.32).align_to(fr, LEFT).shift(RIGHT * 0.3)
    sep = Line(fr.get_corner(UL) + DOWN * 0.64, fr.get_corner(UR) + DOWN * 0.64, color=S.GREY_DARK,
               stroke_width=2)
    body = Rectangle(width=page_w - 0.6, height=page_h - 0.9, stroke_width=0, fill_opacity=0)
    body.move_to(fr.get_bottom() + UP * (page_h - 0.64) / 2)
    g = VGroup(fr, cr, sep, body)
    g.frame, g.crumb, g.body = fr, cr, body
    return g


def checkbox_row(text: str, on: bool = True, size: float = 20, color=INK) -> VGroup:
    """☑ / ☐ and a label (Settings → Branches). .box .tick .text"""
    b = Square(side_length=0.28, stroke_color=S.GREY, stroke_width=2.5).set_fill(TERM_BG, 1)
    tick = check_mark(0.24, PASS, stroke=3.5).move_to(b) if on else VMobject()
    t = label(text, size, color).next_to(b, RIGHT, buff=0.18)
    g = VGroup(b, tick, t)
    g.box, g.tick, g.text = b, tick, t
    return g


def field_row(name: str, value: str, size: float = 20, field_w: float | None = None,
              value_color=INK, mono_value: bool = True) -> VGroup:
    """A form field: GREY name above an input box holding the value. .name .field .value"""
    n = label(name, size, S.GREY)
    v = mono(value, size, value_color) if mono_value else label(value, size, value_color)
    fw = field_w or v.width + 0.4
    f = RoundedRectangle(width=fw, height=v.height + 0.24, corner_radius=0.06, stroke_color=S.GREY_DARK,
                         stroke_width=2).set_fill(TERM_BG, 1)
    v.move_to(f).align_to(f, LEFT).shift(RIGHT * 0.18)
    fg = VGroup(f, v)
    g = VGroup(n, fg).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    g.name, g.field, g.value = n, f, v
    return g


def actions_tab(row_text: str = "demo class 1 · CI Pipeline · main", state: str = "running",
                page_w: float = 6.4, page_h: float = 2.6, size: float = 20) -> VGroup:
    """S07's schematic Actions tab (tag it illustration_tag()): the repo tabs 'Code · Issues · Pull
    requests · Actions' (Actions YELLOW), one run row with its status mark. .tabs{name} .row .mark
    .frame. set the mark: Transform(page.mark, state_mark('failure', 0.3).move_to(page.mark))."""
    pg = gh_page(YOUR_REPO, page_w, page_h, size)
    names = ("Code", "Issues", "Pull requests", "Actions")
    tabs = VGroup(*[label(n, size, TURN if n == "Actions" else S.GREY) for n in names]).arrange(RIGHT, buff=0.45)
    tabs.next_to(pg.crumb, DOWN, buff=0.3).align_to(pg.crumb, LEFT)
    pg[2].next_to(tabs, DOWN, buff=0.12).set_x(pg.frame.get_center()[0])
    mk = state_mark(state, 0.3)
    rt = label(row_text, size + 2, INK)
    row = VGroup(mk, rt).arrange(RIGHT, buff=0.2)
    row.next_to(tabs, DOWN, buff=0.45).align_to(tabs, LEFT)
    rb = RoundedRectangle(width=page_w - 0.5, height=row.height + 0.3, corner_radius=0.08,
                          stroke_color=S.GREY_DARK, stroke_width=2).move_to(row).align_to(pg.frame, LEFT).shift(RIGHT * 0.25)
    pg.add(tabs, rb, row)
    pg.tabs = {n: t for n, t in zip(names, tabs)}
    pg.row, pg.mark, pg.row_box = row, mk, rb
    return pg


# ================================================================== run panels (from the captures)
def _fit(s: str, n: int) -> str:
    return s if disp_len(s) <= n else s[:n - 1] + "…"


class RunLog(VGroup):
    """A job-log panel (see run_log). .frame .title .heading .rows .badge .tag .cap; row(n) = the row
    of FILE line n (KeyError if not shown)."""

    def row(self, n: int):
        return self.row_map[n]


def run_log(cap, lines=None, title: str | None = None, heading=None, size: float = 22,
            colors: dict | None = None, crop_ids: bool = True, wrap: bool = False,
            tag_text: str | None = "live · stand-in runner", badge: bool = True,
            log_w: float | None = None, max_w: float = 12.6) -> RunLog:
    """LOG(runX/<job>/NN: lines): a job-log panel quoting a runner capture.

    cap: a Capture or a name ('run1/lint-and-format/04', 'noload/x2', also laptop captures with
    title=). lines: script.md's FILE line spec (ints, (a, b), '…'); None = all output; () = heading
    only. title: default 'Job name › Step name' from 00-steps.txt (x* files: pass title=, e.g.
    'Lint and Format Check · extra: Flake8, if it had run'). heading: None = the '$' command in GREY
    mono (cropped ids, cut with '…' to fit), or the step name for a multi-line run: script; a string
    = that text in GREY mono; False = none. colors: {file line: colour} (default OUTPUT). Every row
    is crop()ped (ids -> 7 characters) and crop_addr()ed. The badge 'exit N' sits on the top edge
    (RED outline when N != 0); the tag on the bottom edge, right. Width fits the widest row (>= 6),
    at most max_w; a wider row raises unless wrap=True (soft-wrapped)."""
    cap = capture(cap) if isinstance(cap, str) else cap
    colors = colors or {}
    spec = ((cap.k + 1, len(cap.raw)),) if lines is None else tuple(lines)
    if cap.k + 1 > len(cap.raw) and lines is None:
        spec = ()
    picked = []
    for r in spec:
        if isinstance(r, str):
            picked.append((None, r))
            continue
        a, b = (r, r) if isinstance(r, int) else r
        for n in range(a, b + 1):
            s = crop_addr(cap.line(n))
            picked.append((n, crop(s) if crop_ids else s))
    max_chars = int((max_w - 0.6) / cell_width(size))
    if title is None:
        if cap.job is None:
            raise ValueError(f"run_log({cap.path.name}): a laptop capture needs title=")
        if cap.step_name:
            title = f"{JOB_NAME[cap.job]} › {cap.step_name}"
        else:
            raise ValueError(f"run_log({cap.path.name}): an extra (x*) capture needs title=")
    # rows
    items = []
    for n, s in picked:
        col = colors.get(n, OUTPUT) if n is not None else S.GREY
        if disp_len(s) > max_chars:
            if not wrap:
                raise ValueError(f"run_log {cap.path.name}:{n}: {disp_len(s)} > {max_chars} cells at "
                                 f"{size} pt; wrap=True, cut() it or size=20: {s!r}")
            for k, part in enumerate(soft([s], max_chars)):
                items.append((n if k == 0 else None, part, col))
        else:
            items.append((n, s, col))
    rows = VGroup(*[emo_line(s, size, col) for _, s, col in items])
    row_map = {}
    for (n, _, _), r in zip(items, rows):
        if n is not None and n not in row_map:
            row_map[n] = r
    pitch = line_pitch(size)
    for i, r in enumerate(rows):
        r.shift(-r.strut.get_corner(UL) + DOWN * i * pitch)
    # heading
    head = None
    if heading is not False:
        if isinstance(heading, str):
            head = mono(_fit(heading, max_chars), 20, S.GREY)
        elif cap.k == 1:
            head = mono(_fit("$ " + crop(cap.cmd_lines[0]), int((max_w - 0.6) / cell_width(20))), 20, S.GREY)
        else:
            head = label(cap.step_name or title.split("›")[-1].strip(), 20, S.GREY)
    tt = label(title, 22, INK)
    parts = [tt] + ([head] if head is not None else []) + ([rows] if len(rows) else [])
    inner_w = max(p.width for p in parts)
    need = tt.width + (exit_badge(cap.exit).width + 0.6 if badge else 0) + 0.7
    w = log_w or min(max_w, max(6.0, inner_w + 0.7, need))
    if inner_w + 0.5 > w + 1e-6:
        raise ValueError(f"run_log {cap.path.name}: content {inner_w:.2f} wider than the panel {w:.2f}")
    body = VGroup(*([head] if head is not None else []) + ([rows] if len(rows) else []))
    if len(body):
        body.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    bar_h = 0.52
    h = bar_h + (body.height + 0.45 if len(body) else 0.25)
    fr = RoundedRectangle(width=w, height=h, corner_radius=0.14, stroke_color=S.GREY_DARK,
                          stroke_width=2).set_fill(TERM_BG, 1)
    sep = Line(fr.get_corner(UL) + DOWN * bar_h, fr.get_corner(UR) + DOWN * bar_h, color=S.GREY_DARK,
               stroke_width=2)
    tt.move_to(fr.get_top() + DOWN * bar_h / 2).align_to(fr, LEFT).shift(RIGHT * 0.3)
    if len(body):
        body.next_to(sep, DOWN, buff=0.22).align_to(fr, LEFT).shift(RIGHT * 0.3)
    g = RunLog(fr, sep, tt)
    if len(body):
        g.add(body)
    g.frame, g.title, g.heading, g.rows, g.cap, g.row_map = fr, tt, head, rows, cap, row_map
    g.badge = g.tag = None
    if badge:
        bd = exit_badge(cap.exit)
        bd.move_to(fr.get_corner(UR) + np.array([-0.35 - bd.width / 2, 0, 0]))
        if bd.get_left()[0] < tt.get_right()[0] + 0.15:
            bd.move_to([tt.get_right()[0] + 0.2 + bd.width / 2, fr.get_top()[1], 0])
            if bd.get_right()[0] > fr.get_right()[0] - 0.1:
                raise ValueError(f"run_log {cap.path.name}: the title leaves no room for the exit "
                                 "badge on the top edge: pass log_w= wider")
        g.add(bd)
        g.badge = bd
    if tag_text:
        tg = tag(tag_text, S.GREY)
        tg.move_to(fr.get_corner(DR) + np.array([-0.3 - tg.width / 2, 0, 0]))
        g.add(tg)
        g.tag = tg
    return g


class StepsList(VGroup):
    """STEPS(runX/<job>: lines): the job's step list as the run page lists it (see steps_list).
    .frame .head .rows .marks .names .notes{file line: chip} .tag; row(n) by FILE line of 00-steps.txt.
    V6 on the rows (S10, S14): code_chip(n, code) a mono chip at the row's right end (after its note); shunt_arc(n)
    a GREY arc jumping past the row on its left; bridge(a, b) a PINK 'always' arc from row a down to
    row b on the left. Each returns a mobject: FadeIn / Create it yourself (it is not added)."""

    def row(self, n: int):
        return self.row_map[n]

    def code_chip(self, n: int, code_: int) -> VGroup:
        r = self.row_map[n]
        c = chip(str(code_), PASS if code_ == 0 else ERR, size=22, font=MONO)
        return c.next_to(r[-1], RIGHT, buff=0.25)

    def shunt_arc(self, n: int) -> VGroup:
        r = self.row_map[n]
        x = r.mark.get_left()[0] - 0.12
        a = np.array([x, r.get_top()[1] + 0.05, 0])
        b = np.array([x, r.get_bottom()[1] - 0.05, 0])
        return ArcBetween(a, b, angle=PI * 0.9, color=S.GREY)

    def bridge(self, a: int, b: int, text: str = "always") -> VGroup:
        ra, rb = self.row_map[a], self.row_map[b]
        x = ra.mark.get_left()[0] - 0.12
        p, q = np.array([x, ra.get_center()[1], 0]), np.array([x, rb.get_center()[1], 0])
        arc = ArcBetween(p, q, angle=PI * 0.7, color=ROUTE)
        t = label(text, 20, ROUTE).next_to(arc, LEFT, buff=0.08)
        return VGroup(arc, t)


def ArcBetween(a, b, angle: float = PI / 2, color=S.GREY, stroke: float = 3, tip: bool = True):
    """A curved arrow from a to b bulging to the left of the a→b direction."""
    from manim import CurvedArrow as _CA
    return _CA(a, b, angle=angle, color=color, stroke_width=stroke, tip_length=0.15) if tip else \
        ArcBetweenPointsNoTip(a, b, angle, color, stroke)


def ArcBetweenPointsNoTip(a, b, angle, color, stroke):
    from manim import ArcBetweenPoints
    return ArcBetweenPoints(a, b, angle=angle, color=color, stroke_width=stroke)


def steps_list(run: str, job: str, lines=None, size: float = 22,
               tag_text: str | None = "illustration · from our live runs", list_w: float | None = None) -> StepsList:
    """STEPS(runX/<job>: a–b): one row per step of runner/<run>/<job>/00-steps.txt within the FILE
    lines (default: every step and the 'job result' line): a state mark (GREEN ✓ success, RED ✗
    failure, GREY dashed ⊘ skipped), the step name (WHITE; GREY when skipped) and the row's
    parenthesised note as a GREY chip; the last line 'job result: X' becomes a 'job result' row.
    The header line (full commit id) is never shown. Header: the job's name."""
    p = RUNNER / run / job / "00-steps.txt"
    raw = p.read_text(encoding="utf-8").rstrip("\n").split("\n")
    want = set(range(2, len(raw) + 1))
    if lines is not None:
        want = set()
        for r in lines:
            a, b = (r, r) if isinstance(r, int) else r
            want |= set(range(a, b + 1))
    if 1 in want:
        raise ValueError("00-steps.txt line 1 (the header with the full commit id) is never shown")
    by_line = {st.n: st for st in steps(run, job)}
    rows, row_map, notes = VGroup(), {}, {}
    for n in sorted(want):
        if n in by_line:
            st = by_line[n]
            mk = state_mark(st.state, 0.32)
            nm = label(st.name, size, S.GREY if st.state == "skipped" else INK)
            r = VGroup(mk, nm).arrange(RIGHT, buff=0.22)
            if st.note:
                ch = grey_chip(st.note, 20, mono_font=st.note.startswith("steps."))
                ch.next_to(nm, RIGHT, buff=0.25)
                r.add(ch)
                notes[n] = ch
        elif raw[n - 1].startswith("job result:"):
            res = raw[n - 1].split(":", 1)[1].strip()
            mk = state_mark(res, 0.32)
            nm = label(f"job result: {res}", size, STATE_COLOR.get(res, INK))
            r = VGroup(mk, nm).arrange(RIGHT, buff=0.22)
        else:
            continue
        r.mark, r.name = mk, nm
        rows.add(r)
        row_map[n] = r
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    head = label(JOB_NAME[job], 22, INK)
    inner = VGroup(head, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
    w = list_w or inner.width + 0.9
    fr = RoundedRectangle(width=w, height=inner.height + 0.6, corner_radius=0.14, stroke_color=GITHUB,
                          stroke_width=2).set_fill(PANEL, 1)
    inner.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.55)
    g = StepsList(fr, inner)
    g.frame, g.head, g.rows, g.row_map, g.notes = fr, head, rows, row_map, notes
    g.marks = VGroup(*[r.mark for r in rows])
    g.names = VGroup(*[r.name for r in rows])
    g.tag = None
    if tag_text:
        tg = tag(tag_text, S.GREY)
        tg.move_to(fr.get_corner(DR) + np.array([-0.3 - tg.width / 2, 0, 0]))
        g.add(tg)
        g.tag = tg
    return g


# ================================================================== V4 · the job graph
def _elbow(p, q, xm=None) -> VMobject:
    xm = (p[0] + q[0]) / 2 if xm is None else xm
    m = VMobject()
    pts = [p, np.array([xm, p[1], 0]), np.array([xm, q[1], 0]), q]
    clean = [pts[0]] + [pt for i, pt in enumerate(pts[1:], 1) if np.linalg.norm(pt - pts[i - 1]) > 1e-6]
    m.set_points_as_corners(clean)
    return m


class JobGraph(VGroup):
    """V4: the run graph in GitHub's layout (build → four side by side → summary), centred on the
    origin (shift it as one). Nodes: rounded boxes with a state mark and the job's label.

        g = JobGraph(states=results("run1"), labels="names")     # or run_graph("run1")
        self.play(FadeIn(g)); self.play(g.set_state("build", "running"))
        g.reveal(self, results("run1"))                          # node by node (YELLOW, then final)

    labels 'names' (ci.yml name:, node ~3.5 wide, graph ~12.3 x 3.9), 'short' ('Build', 'Lint' …,
    graph ~7.7 wide), 'ids' (job ids, mono), None (marks only, graph ~4.2 wide).
    edges=True draws the needs lines; gap=True adds the dashed lint → summary gap with a YELLOW '?'
    (.gap, .gap_q; show it later with show_gap()). badge=True: the run badge (top-left, 'CI Pipeline'
    + mark). tag_text: the GREY tag under the right end (None: no tag).
    PLAYS reveal(states, order=None, per=0.45) · tokens(states=None, text=None) (PINK result tokens
    along the three needs lines into the summary; returns them) · draw_edges() · show_gap().
    ANIM set_state(job, state) · set_badge(state) · pulse(job, colour).
    .nodes{id} (.frame .mark .text) .edges{(src, dst)} .gap .gap_q .badge .tag .states;
    stage_labels() -> three GREY 'stage 0/1/2' labels above the columns (not added)."""

    def __init__(self, states=None, labels: str | None = "names", size: float = 22, pitch: float = 0.8,
                 col_gap: float = 1.0, edges: bool = True, gap: bool = False, badge: bool = True,
                 tag_text: str | None = "illustration · colors from our live runs", middle=MIDDLE,
                 texts: dict | None = None, **kw):
        super().__init__(**kw)
        self.size, self.labels_mode, self.pitch = size, labels, pitch
        self.states = {j: "idle" for j in JOB_IDS}
        if isinstance(states, str):
            states = results(states)
        if states:
            self.states.update(states)
        given, texts = texts or {}, {}
        for j in JOB_IDS:
            if j in given:
                texts[j] = label(given[j], size, INK)
            elif labels == "names":
                texts[j] = label(JOB_NAME[j], size, INK)
            elif labels == "short":
                texts[j] = label(SHORT[j], size, INK)
            elif labels == "ids":
                texts[j] = mono(j, size - 2, INK)
            else:
                texts[j] = None
        def col_w(js):
            tw = max((texts[j].width for j in js if texts[j] is not None), default=0)
            return (tw + 0.9) if labels else 0.75
        self.col_w = {"build": col_w(["build"]), "test-summary": col_w(["test-summary"])}
        mid_w = col_w(list(middle))
        for j in middle:
            self.col_w[j] = mid_w
        self.node_w = mid_w
        self.node_h = max(0.56, mono("|", size).height + 0.3) if labels else min(0.5, pitch * 0.8)
        self.mark_h = min(0.3, self.node_h * 0.7)
        lx = -(mid_w / 2 + col_gap + self.col_w["build"] / 2)
        rx = mid_w / 2 + col_gap + self.col_w["test-summary"] / 2
        pos = {"build": np.array([lx, 0, 0]), "test-summary": np.array([rx, 0, 0])}
        for i, j in enumerate(middle):
            pos[j] = np.array([0, pitch * (1.5 - i), 0])
        self.pos = pos
        self.nodes = {}
        for j in JOB_IDS:
            self.nodes[j] = self._node(j, self.states[j], texts[j]).move_to(pos[j])
        self.shift(-VGroup(*self.nodes.values()).get_center() * np.array([1, 0, 0]))
        self.edges = {}
        for dst, srcs in NEEDS.items():
            for src in srcs:
                p = self.nodes[src].get_right()
                q = self.nodes[dst].get_left()
                self.edges[(src, dst)] = _elbow(p, q).set_stroke(S.GREY, 2.5)
        lint, summ = self.nodes["lint-and-format"], self.nodes["test-summary"]
        p, q = lint.get_right(), summ.get_left()
        xm = p[0] + (q[0] - p[0]) * 0.62
        self.gap = DashedVMobject(_elbow(p, q, xm), num_dashes=18).set_stroke(S.GREY, 2.5)
        self.gap_q = label("?", 28, TURN).move_to([xm + 0.22, (p[1] + q[1]) / 2, 0])
        self.add(*[self.edges[k] for k in self.edges] if edges else [])
        if gap:
            self.add(self.gap, self.gap_q)
        self.add(*self.nodes.values())
        self.badge = None
        if badge:
            self.badge = self._badge("idle" if not states else self._run_state())
            self.badge.next_to(VGroup(*self.nodes.values()), UP, buff=0.3).align_to(self.nodes["build"], LEFT)
            self.add(self.badge)
        self.tag = None
        if tag_text:
            self.tag = tag(tag_text, S.GREY)
            self.tag.next_to(VGroup(*self.nodes.values()), DOWN, buff=0.3).align_to(self.nodes["test-summary"], RIGHT)
            self.add(self.tag)

    def _run_state(self, states=None):
        st = states or self.states
        vals = [st[j] for j in JOB_IDS]
        if any(v == "failure" for v in vals):
            return "failure"
        if all(v == "success" for v in vals):
            return "success"
        if any(v == "running" for v in vals):
            return "running"
        return "idle"

    def _frame(self, state, j=None):
        col = STATE_COLOR.get(state, S.GREY)
        fr = RoundedRectangle(width=self.col_w[j] if j else self.node_w, height=self.node_h, corner_radius=0.12,
                              stroke_color=col if state != "idle" else S.GREY_DARK, stroke_width=2.5)
        fr.set_fill(PANEL, 1)
        return fr

    def _node(self, j, state, text):
        fr = self._frame(state, j)
        mk = state_mark(state, self.mark_h)
        if text is not None:
            mk.move_to(fr.get_left() + RIGHT * 0.38)
            text.next_to(mk, RIGHT, buff=0.2)
            g = VGroup(fr, mk, text)
        else:
            mk.move_to(fr)
            g = VGroup(fr, mk)
        g.frame, g.mark, g.text, g.job = fr, mk, text, j
        return g

    def _badge(self, state):
        mk = state_mark(state, 0.3)
        t = label("CI Pipeline", 22, INK)
        row = VGroup(mk, t).arrange(RIGHT, buff=0.18)
        b = RoundedRectangle(width=row.width + 0.4, height=row.height + 0.26, corner_radius=0.12,
                             stroke_color=STATE_COLOR.get(state, S.GREY) if state != "idle" else S.GREY_DARK,
                             stroke_width=2.5).set_fill(PANEL, 1)
        row.move_to(b)
        g = VGroup(b, row)
        g.frame, g.mark, g.text, g.state = b, mk, t, state
        return g

    def set_state(self, job: str, state: str, run_time: float = 0.4):
        """ANIM: node `job` turns `state` ('running', 'success', 'failure', 'skipped', 'idle'). The
        whole node is transformed (its frame never covers its text); after playing it yourself,
        self.add(graph) re-seats the graph as one piece (reveal() does)."""
        nd = self.nodes[job]
        new = self._node(job, state, nd.text.copy() if nd.text is not None else None).move_to(nd)
        self.states[job] = state
        return Transform(nd, new, run_time=run_time)

    def set_badge(self, state: str, run_time: float = 0.4):
        """ANIM: the run badge turns `state`."""
        b = self.badge
        nb = self._badge(state).move_to(b).align_to(b, LEFT)
        b.state = state
        return Transform(b, nb, run_time=run_time)

    def pulse(self, job: str, color=TURN, run_time: float = 0.6):
        """ANIM: flash one node (frame, mark and label together)."""
        nd = self.nodes[job]
        inner = VGroup(nd.mark, nd.text) if nd.text is not None else nd.mark
        return AnimationGroup(Circumscribe(nd, color=color, buff=0.06), Indicate(inner, color=color,
                              scale_factor=1.06), run_time=run_time)

    def reveal(self, scene, states=None, order=None, per: float = 0.45, running: bool = True,
               badge: bool = True):
        """PLAYS: colour the nodes one by one (YELLOW running first when running=True), then the
        run badge. states: a dict or a run name ('run1')."""
        if isinstance(states, str):
            states = results(states)
        states = states or self.states
        order = order or ["build", "lint-and-format", "unit-tests", "integration-tests", "system-tests",
                          "test-summary"]
        for j in order:
            if running and self.states[j] != "running":
                scene.play(self.set_state(j, "running", per * 0.4))
            scene.play(self.set_state(j, states[j], per * 0.6))
        if badge and self.badge is not None:
            scene.play(self.set_badge(self._run_state(states)))
        scene.add(self)

    def draw_edges(self, scene, run_time: float = 0.8):
        """PLAYS: draw every needs line (for a graph made with edges=False)."""
        new = [e for e in self.edges.values() if e not in self.submobjects]
        scene.play(*[Create(e) for e in new], run_time=run_time)
        for e in new:
            self.add_to_back(e)

    def show_gap(self, scene, run_time: float = 0.6):
        """PLAYS: the dashed lint → summary gap and its YELLOW '?'."""
        scene.play(Create(self.gap), FadeIn(self.gap_q), run_time=run_time)
        self.add_to_back(self.gap)
        self.add(self.gap_q)

    def tokens(self, scene, states=None, text=None, run_time: float = 1.2, keep: bool = False):
        """PLAYS: three PINK result tokens ('success' / 'failure', from states or self.states) ride the
        needs lines from the three test jobs and sink into the summary node's mark (keep=True: they
        stay stacked left of the summary node instead; fade them yourself). Returns them."""
        if isinstance(states, str):
            states = results(states)
        st = states or self.states
        toks, anims = VGroup(), []
        for j in TEST_JOBS:
            e = self.edges[(j, "test-summary")]
            t = route_chip(text or st[j], 20)
            t.move_to(e.get_start())
            toks.add(t)
            anims.append(MoveAlongPath(t, e))
        scene.play(FadeIn(toks), run_time=0.3)
        scene.play(*anims, run_time=run_time)
        summ = self.nodes["test-summary"]
        if keep:
            scene.play(toks.animate.arrange(DOWN, buff=0.08).next_to(summ, LEFT, buff=0.15), run_time=0.4)
        else:
            scene.play(*[FadeOut(t, target_position=summ.mark.get_center(), scale=0.3) for t in toks],
                       Indicate(summ.mark, color=ROUTE), run_time=0.5)
            scene.remove(*toks)
        return toks

    def stage_labels(self, size: float = 20) -> VGroup:
        """Three GREY 'stage 0 / 1 / 2' labels above the columns (act -l), not added."""
        top = max(n.get_top()[1] for n in self.nodes.values()) + 0.3
        if self.badge is not None:
            top = self.badge.get_top()[1] + 0.3
        g = VGroup()
        for k, j in enumerate(("build", MIDDLE[0], "test-summary")):
            g.add(label(f"stage {k}", size, S.GREY).move_to([self.nodes[j].get_center()[0], top, 0]))
        return g


def run_graph(run: str | None = None, labels: str | None = "names", **kw) -> JobGraph:
    """GRAPH(runX): a JobGraph coloured from runner/<run>/results.txt (None: every node idle)."""
    return JobGraph(states=results(run) if run else None, labels=labels, **kw)


def recorded_graph(size: float = 20, col_gap: float = 0.45, names: bool = False) -> VGroup:
    """RECORDED(screenshot): the README screenshot's transcription re-drawn small, in GitHub's
    layout: six GREEN nodes with their times ('54s' … '4s'; names=True: 'Build  54s' …), tag
    'recorded · README screenshot' (the image is never copied). ~5.0 x 3.2 (names: ~8.3 wide):
    it fits beside run_graph(run, labels='short', col_gap=0.6) (~7.2 wide).
    .graph (a JobGraph: .nodes, set_state …) .tag"""
    texts = {j: (f"{SHORT[j]}  " if names else "") + f"{SCREENSHOT_TIMES[j]}s" for j in JOB_IDS}
    g = JobGraph(states={j: "success" for j in JOB_IDS}, labels="short", size=size, pitch=0.62,
                 col_gap=col_gap, badge=False, tag_text=None, texts=texts)
    tg = recorded_tag("README screenshot")
    tg.next_to(g, DOWN, buff=0.25).align_to(g, RIGHT)
    res = VGroup(g, tg)
    res.graph, res.tag = g, tg
    return res


def graph_icon(h: float = 0.9) -> VGroup:
    """A text-free six-node graph glyph (S16's question cards, small corners)."""
    return JobGraph(labels=None, pitch=h / 3.2, col_gap=0.4, badge=False, tag_text=None)


class Gantt(VGroup):
    """V4 S05: the README screenshot's times as a timeline (recorded): one bar per job (build 0-54 s,
    the four checks from 54 s, the summary after the longest, system), short GREY job labels on the
    left, the time at each bar's end, a WHITE ruler 'about 2 min on the clock' under it.
    PLAYS critical() (build → system → summary glow YELLOW) · billed() (a GOLD row of six one-minute
    blocks, one per job, 'about 6 billed minutes': a count of billed minutes, not drawn to the clock's
    scale). .bars{id} .labels{id} .times{id} .ruler .billed_row. ~10.5 x 4.0, centred on the origin."""

    def __init__(self, times=None, bar_w: float = 8.0, row_h: float = 0.42, size: float = 20, **kw):
        super().__init__(**kw)
        times = dict(times or SCREENSHOT_TIMES)
        mid_start = times["build"]
        sum_start = mid_start + max(times[j] for j in MIDDLE)
        total = sum_start + times["test-summary"]
        self.unit = bar_w / total
        start = {"build": 0, "test-summary": sum_start, **{j: mid_start for j in MIDDLE}}
        order = ["build", *MIDDLE, "test-summary"]
        x0 = -bar_w / 2 + 1.0
        self.bars, self.labels, self.times = {}, {}, {}
        for i, j in enumerate(order):
            y = -i * (row_h + 0.14)
            w = max(0.08, times[j] * self.unit)
            b = Rectangle(width=w, height=row_h, stroke_color=GITHUB, stroke_width=2).set_fill(GITHUB, 0.35)
            b.move_to([x0 + start[j] * self.unit + w / 2, y, 0])
            lb = label(SHORT[j], size, S.GREY).move_to([x0 - 0.25, y, 0], aligned_edge=RIGHT)
            tm = label(f"{times[j]}s", size, S.GREY).next_to(b, RIGHT, buff=0.12)
            self.bars[j], self.labels[j], self.times[j] = b, lb, tm
            self.add(b, lb, tm)
        bottom = min(b.get_bottom()[1] for b in self.bars.values()) - 0.25
        self.ruler = VGroup(Line([x0, bottom, 0], [x0 + total * self.unit, bottom, 0], color=INK, stroke_width=3),
                            label("about 2 min on the clock", size, INK))
        self.ruler[1].next_to(self.ruler[0], DOWN, buff=0.1).align_to(self.ruler[0], LEFT)
        self.add(self.ruler)
        self.x0, self.total, self.bar_w, self.size = x0, total, bar_w, size
        self.billed_row = None
        self.center()

    def critical(self, scene, run_time: float = 0.8):
        """PLAYS: the critical path (build → system → summary) glows YELLOW."""
        scene.play(*[self.bars[j].animate.set_stroke(TURN, 4).set_fill(TURN, 0.45)
                     for j in ("build", "system-tests", "test-summary")], run_time=run_time)

    def billed(self, scene, run_time: float = 1.0) -> VGroup:
        """PLAYS: a GOLD row of six one-minute blocks slides in under the ruler. Returns it."""
        n = len(JOB_IDS)
        bw = (self.bar_w - 0.2) / n
        blocks = VGroup(*[VGroup(Rectangle(width=bw - 0.08, height=0.4, stroke_color=COST, stroke_width=2)
                                 .set_fill(COST, 0.25)) for _ in range(n)]).arrange(RIGHT, buff=0.08)
        for b in blocks:
            b.add(label("1 min", 20, COST).move_to(b[0]))
        cap = label("about 6 billed minutes", self.size, COST)
        row = VGroup(blocks, cap).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        row.next_to(self.ruler, DOWN, buff=0.25).align_to(self.ruler[0], LEFT)
        scene.play(FadeIn(row, shift=UP * 0.2), run_time=run_time)
        self.add(row)
        self.billed_row = row
        return row


# ================================================================== V2 · the pipeline strip and the loop
class PipelineStrip(VGroup):
    """V2: slide 26's row 'Commit → Build Container → Lint and Format → Test → Summary' (WHITE outlines;
    the current box fills YELLOW). full=True: slide-size row (22 pt, boxes 0.72 tall, ~11.6 wide);
    full=False: the thin Part 2 strip (20 pt, 0.44 tall, ~10.6 wide; use pipeline_strip(current)).
    ANIM set_current(i | name) (None: no box). purposes(size=20) slide 27's one-liners under the
    boxes (two lines each; not added). .boxes[i] (.frame .text) .names .arrows .current"""

    def __init__(self, current=None, full: bool = False, **kw):
        super().__init__(**kw)
        size = 22 if full else 20
        bh = 0.72 if full else 0.44
        self.full, self.size = full, size
        boxes = VGroup()
        for n in STRIP_BOXES:
            t = label(n, size, INK)
            fr = RoundedRectangle(width=t.width + (0.5 if full else 0.34), height=bh, corner_radius=0.1,
                                  stroke_color=INK, stroke_width=2.5 if full else 2).set_fill(S.BG, 1)
            t.move_to(fr)
            b = VGroup(fr, t)
            b.frame, b.text = fr, t
            boxes.add(b)
        boxes.arrange(RIGHT, buff=0.55 if full else 0.38)
        arrows = VGroup(*[Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.06, color=S.GREY,
                                stroke_width=2.5, tip_length=0.14, max_tip_length_to_length_ratio=0.5)
                          for i in range(len(boxes) - 1)])
        self.boxes, self.arrows = boxes, arrows
        self.names = VGroup(*[b.text for b in boxes])
        self.add(arrows, boxes)
        self.current = None
        if current is not None:
            k = self._k(current)
            boxes[k].frame.set_stroke(TURN).set_fill(TURN, 0.3)
            self.current = k

    def _k(self, cur):
        return STRIP_BOXES.index(cur) if isinstance(cur, str) else cur

    def set_current(self, cur, run_time: float = 0.5):
        """ANIM: the YELLOW fill moves to box `cur` (index or name; None clears)."""
        anims = []
        k = None if cur is None else self._k(cur)
        for i, b in enumerate(self.boxes):
            if i == k:
                nb = b.copy()
                nb[0].set_stroke(TURN).set_fill(TURN, 0.3)
                anims.append(Transform(b, nb))
            elif i == self.current:
                nb = b.copy()
                nb[0].set_stroke(INK).set_fill(S.BG, 1)
                anims.append(Transform(b, nb))
        self.current = k
        return AnimationGroup(*anims, run_time=run_time)

    def purposes(self, size: float = 20) -> VGroup:
        """Slide 27's one-line purposes, each split into two lines under its box (not added)."""
        g = VGroup()
        for b, s in zip(self.boxes, STRIP_PURPOSE):
            if ", " in s:
                a, c = s.split(", ", 1)
                parts = [a + ",", c]
            elif s.count(" · ") == 2:
                parts = s.split(" · ")
            elif " to " in s:
                a, c = s.split(" to ", 1)
                parts = [a, "to " + c]
            else:
                parts = [s]
            t = VGroup(*[label(x, size, S.GREY) for x in parts]).arrange(DOWN, buff=0.06)
            t.next_to(b, DOWN, buff=0.18)
            g.add(t)
        return g


def pipeline_strip(current=None) -> PipelineStrip:
    """STRIP <box>: the thin Part 2 strip under the tracker (left edge -6.5, centre y STRIP_Y), the
    current box YELLOW. FadeIn it at the start of a Part 2 scene; strip.set_current(name) ANIM."""
    s = PipelineStrip(current, full=False)
    s.move_to([TRACK_LEFT + s.width / 2, STRIP_Y, 0])
    return s


# ================================================================== set pieces: shared base
class Piece(VGroup):
    """Base of the set pieces: drop(scene, *parts) fades parts out AND removes them from the piece
    (so they never snap back); keep(scene, *mobs) makes new mobjects members (after a PLAYS)."""

    def drop(self, scene, *parts, run_time: float = 0.4):
        scene.play(*[FadeOut(p) for p in parts], run_time=run_time)
        for p in parts:
            for owner in [self, *self.get_family()]:
                if p in owner.submobjects:
                    owner.remove(p)
            scene.remove(p)

    def keep(self, scene, *mobs):
        for m in mobs:
            scene.remove(m)
            self.add(m)
        scene.add(self)


def _gate_open(g, color=PASS, run_time: float = 0.4):
    """ANIM: a gate_glyph's bar swings up GREEN."""
    tgt = g.bar.copy().rotate(PI / 2.4, about_point=g.bar.get_start()).set_color(color)
    return Transform(g.bar, tgt, run_time=run_time)


def _gate_close(g, color=S.GREY, run_time: float = 0.3):
    """ANIM: an opened gate's bar swings back down (GREY)."""
    tgt = g.bar.copy().rotate(-PI / 2.4, about_point=g.bar.get_start()).set_color(color)
    return Transform(g.bar, tgt, run_time=run_time)


def _gate_shut(g, color=ERR, run_time: float = 0.4):
    """ANIM: a gate_glyph's bar flashes shut in RED."""
    return AnimationGroup(g.bar.animate.set_color(color), Indicate(g.posts, color=color, scale_factor=1.05),
                          run_time=run_time)


# ================================================================== V1 · hooks stay on your laptop
class HookChain(Piece):
    """V1: the GREY laptop frame 'Git local hooks' holding slide 14's chain with this repo's boxes,
    'hygiene ×7' → 'Black' → 'Flake8' (PURPLE outlines, 22 pt), centred on its anchor. frame_w x
    frame_h (default 6.1 x 2.6, widened to fit the chain plus room for the 'Tests' box: ~6.5). boxes=() draws an empty frame
    (S02's teammate laptop: HookChain((), title='no pre-commit install')).
    PLAYS commit(dot=None) a GREEN dot at the frame's left (returns it) · pass_through(dot, stop=None,
        colour) the dot visits each gate, each flashes GREEN (stop=i: gate i flashes RED and the dot
        halts there) · bypass(dot) a RED arc over all the gates, the dot rides it to the right edge ·
        add_tests() a GREY dashed 'Tests' box at the end, struck RED, 'CI runs these' under it ·
        hook_tags() GREY 'pre-commit' (above the chain) and 'pre-push' (on the right edge) ·
        push(dot, target, arc=-0.5) a PINK arc from the right edge to `target` (a point / mobject); the
        dot rides it (returns the arrow, kept in the piece).
    ANIM flash(i, colour). .frame .title .gates (each .frame .text) .arrows .tests .tags .exit_point"""

    def __init__(self, boxes=("hygiene ×7", "Black", "Flake8"), title: str = "Git local hooks",
                 frame_w: float = 6.1, frame_h: float = 2.6, size: float = 22, color=LAPTOP, **kw):
        super().__init__(**kw)
        self.size = size
        self.gates = VGroup()
        for b in boxes:
            t = label(b, size, INK)
            fr = RoundedRectangle(width=t.width + 0.36, height=0.62, corner_radius=0.1, stroke_color=TOOL,
                                  stroke_width=2.5).set_fill(PANEL, 1)
            t.move_to(fr)
            g = VGroup(fr, t)
            g.frame, g.text = fr, t
            self.gates.add(g)
        self.arrows = VGroup()
        tests_w = label("Tests", size).width + 0.36 + 0.42
        if len(self.gates):
            self.gates.arrange(RIGHT, buff=0.42)
            frame_w = max(frame_w, self.gates.width + tests_w + 1.0)
        self.frame = box(frame_w, frame_h, color, fill_opacity=0.06, radius=0.2)
        self.title = label(title, 22, color).next_to(self.frame.get_corner(UL), DR, buff=0.18)
        self.add(self.frame, self.title)
        if len(self.gates):
            self.gates.move_to(self.frame).align_to(self.frame, LEFT).shift(RIGHT * 0.45 + DOWN * 0.2)
            for a, b in zip(self.gates[:-1], self.gates[1:]):
                self.arrows.add(arrow(a.get_right(), b.get_left(), S.GREY, stroke=2.5, buff=0.06))
            self.add(self.arrows, self.gates)
        self.tests, self.tags = None, VGroup()

    @property
    def exit_point(self):
        return self.frame.get_right()

    def flash(self, i: int, color=PASS, run_time: float = 0.35):
        g = self.gates[i]
        return AnimationGroup(Circumscribe(g, color=color, buff=0.06), Indicate(g.text, color=color,
                              scale_factor=1.08), run_time=run_time)

    def commit(self, scene, dot_=None, color=PASS):
        d = dot_ or dot(color)
        y = self.gates[0].get_top()[1] + 0.2 if len(self.gates) else self.frame.get_center()[1]
        d.move_to([self.frame.get_left()[0] + 0.22, y, 0])
        scene.play(FadeIn(d, scale=0.5), run_time=0.3)
        self.dot = d
        return d

    def pass_through(self, scene, dot_, stop: int | None = None, step: float = 0.35, color=PASS):
        for i, g in enumerate(self.gates):
            scene.play(dot_.animate.move_to(g.frame.get_top() + UP * 0.2), run_time=step)
            if stop is not None and i == stop:
                scene.play(self.flash(i, ERR), dot_.animate.set_color(ERR), run_time=0.4)
                return
            scene.play(self.flash(i, color), run_time=0.25)
        end = self.frame.get_right() + LEFT * 0.3
        scene.play(dot_.animate.move_to([end[0], dot_.get_center()[1], 0]), run_time=step)

    def bypass(self, scene, dot_, run_time: float = 1.2):
        """The arc rises from the frame's left inner edge over all the gates (it crosses the title
        line: drop the hook tags first) and lands at the right inner edge."""
        y = self.gates.get_center()[1]
        a = np.array([self.frame.get_left()[0] + 0.2, y, 0])
        b = np.array([self.frame.get_right()[0] - 0.2, y, 0])
        arc = ArcBetweenPointsNoTip(a, b, -PI / 2.6, ERR, 4)
        if np.linalg.norm(dot_.get_center() - a) > 0.05:
            scene.play(dot_.animate.move_to(a), run_time=0.3)
        scene.play(Create(arc), run_time=0.5)
        scene.play(MoveAlongPath(dot_, arc), run_time=run_time)
        self.keep(scene, arc)
        self.bypass_arc = arc
        return arc

    def add_tests(self, scene, run_time: float = 0.6):
        t = label("Tests", self.size, S.GREY)
        ob = outline_box(t.width + 0.36, 0.62, S.GREY)
        t.move_to(ob)
        g = VGroup(ob, t).next_to(self.gates[-1], RIGHT, buff=0.42)
        ar = DashedLine(self.gates[-1].get_right() + RIGHT * 0.06, g.get_left() + LEFT * 0.06, color=S.GREY,
                        stroke_width=2.5, dash_length=0.08)
        scene.play(FadeIn(g, shift=LEFT * 0.3), Create(ar), run_time=run_time)
        st = Line(g.get_corner(DL), g.get_corner(UR), color=ERR, stroke_width=4)
        cap = label("CI runs these", 20, S.GREY).next_to(g, DOWN, buff=0.15)
        if cap.get_right()[0] > self.frame.get_right()[0] - 0.1:
            cap.align_to(g, RIGHT)
        scene.play(Create(st), FadeIn(cap), run_time=0.5)
        self.tests = VGroup(ar, g, st, cap)
        self.keep(scene, self.tests)
        return self.tests

    def hook_tags(self, scene, run_time: float = 0.5):
        pc = tag("pre-commit", S.GREY).next_to(self.gates, UP, buff=0.15).align_to(self.gates, LEFT)
        pc.shift(RIGHT * (self.gates[0].width + 0.05))
        pp = tag("pre-push", S.GREY).move_to(self.frame.get_corner(DR) + LEFT * 0.9)
        scene.play(FadeIn(pc, shift=DOWN * 0.2), run_time=run_time)
        scene.play(FadeIn(pp, shift=LEFT * 0.2), run_time=run_time)
        self.tags = VGroup(pc, pp)
        self.keep(scene, self.tags)
        return self.tags

    def push(self, scene, dot_, target, arc: float = -0.5, run_time: float = 1.0):
        a = self.frame.get_right()
        ar = route(a, target, arc=arc)
        scene.play(dot_.animate.move_to(a), run_time=0.3)
        scene.play(Create(ar), MoveAlongPath(dot_, VMobject().set_points(ar.get_points()[:len(ar.get_points())])),
                   run_time=run_time)
        self.keep(scene, ar)
        return ar


class ServerDoor(Piece):
    """V1 (S02, S04, S15, S16): the remote-hook picture, centred on its anchor (~8.3 x 3.0 with the
    gates). A BLUE server box (box_w x box_h) labelled 'shared repository', a door in its left wall,
    a GREY gate 'pre-receive' in front of the door (outside, left), a GREY bell 'post-receive' inside.
    PLAYS refuse(dot) the dot comes from the left, the gate shuts RED, the dot bounces back ·
        enter(dot) the gate opens, the dot goes through the door and lands inside · ring(chips=())
        three PINK arcs at the bell, then GREY chips under it ('integration tests' …) · update_chip()
        'update: per branch' on the gate · github() the label becomes 'GitHub.com', pre-receive goes
        GREY dashed with the chip 'your own scripts: not on GitHub.com', a BLUE 'Actions' badge docks
        on the bell and a GREEN 'branch protection' gate docks in front of the door · protect(shut)
        the protection gate lights GREEN and shuts (or opens).
    caption() 'Actions on a push is the bell, not the gate.' (GREY 22, not added: place it under).
    .server .name .door .gate (.bar .posts .text) .bell .bell_text .actions .protection; .start and
    .landing are points that follow the piece."""

    def __init__(self, name: str = "shared repository", box_w: float = 5.6, box_h: float = 3.0, **kw):
        super().__init__(**kw)
        self.server = box(box_w, box_h, GITHUB, fill_opacity=0.08, radius=0.2)
        self.name = label(name, 22, GITHUB).next_to(self.server.get_corner(UL), DR, buff=0.2)
        door = Rectangle(width=0.16, height=1.0, stroke_color=S.GREY, stroke_width=2.5).set_fill(S.BG, 1)
        door.move_to(self.server.get_left())
        self.door = door
        gx = self.server.get_left()[0] - 1.5
        self.gate = gate_glyph(0.9, 0.75, S.GREY).move_to([gx, door.get_center()[1], 0])
        self.gate.text = mono("pre-receive", 20, S.GREY).next_to(self.gate, DOWN, buff=0.15)
        self.bell = bell_glyph(0.7, S.GREY).move_to(self.server.get_center() + RIGHT * box_w * 0.22 + UP * 0.2)
        self.bell_text = mono("post-receive", 20, S.GREY).next_to(self.bell, DOWN, buff=0.15)
        self.add(self.server, self.name, self.door, self.gate, self.gate.text, self.bell, self.bell_text)
        self.actions = self.protection = self.update_c = None
        self.box_w = box_w

    @property
    def start(self):
        """Where a dot starts, left of the gates (follows the piece when it moves)."""
        return np.array([self.server.get_left()[0] - 2.8, self.door.get_center()[1], 0])

    @property
    def landing(self):
        """Where an entering dot lands, inside the server."""
        return self.server.get_center() + LEFT * self.box_w * 0.18

    def _dot(self, dot_):
        if dot_ is None:
            dot_ = dot(PASS)
        return dot_

    def refuse(self, scene, dot_=None):
        d = self._dot(dot_)
        d.move_to(self.start)
        scene.play(FadeIn(d), run_time=0.25)
        scene.play(d.animate.move_to(self.gate.get_left() + LEFT * 0.15), run_time=0.5)
        scene.play(_gate_shut(self.gate), d.animate.set_color(ERR), run_time=0.4)
        scene.play(d.animate.move_to(self.start), run_time=0.5)
        scene.play(self.gate.bar.animate.set_color(S.GREY), run_time=0.2)
        return d

    def enter(self, scene, dot_=None, gate=None):
        d = self._dot(dot_)
        g = gate or self.gate
        if d not in scene.mobjects:
            d.move_to(self.start)
            scene.play(FadeIn(d), run_time=0.25)
        scene.play(d.animate.move_to(g.get_left() + LEFT * 0.15), run_time=0.4)
        scene.play(_gate_open(g), run_time=0.35)
        scene.play(d.animate.move_to(self.door), run_time=0.4)
        scene.play(d.animate.move_to(self.landing), run_time=0.4)
        scene.play(_gate_close(g), run_time=0.3)
        return d

    def ring(self, scene, chips=(), run_time: float = 0.6):
        w = ring_waves(self.bell)
        scene.play(LaggedStart(*[Create(a) for a in w], lag_ratio=0.25), Indicate(self.bell, color=ROUTE),
                   run_time=run_time)
        cs = VGroup(*[grey_chip(c) for c in chips])
        if len(cs):
            cs.arrange(RIGHT, buff=0.15).next_to(self.server, DOWN, buff=0.15).align_to(self.server, RIGHT)
            scene.play(LaggedStart(*[FadeIn(c) for c in cs], lag_ratio=0.3), run_time=0.8)
        self.keep(scene, w, cs)
        self.waves, self.chips = w, cs
        return w, cs

    def update_chip(self, scene, text: str = "update: per branch"):
        c = grey_chip(text).next_to(self.gate, UP, buff=0.18)
        if c.get_right()[0] > self.door.get_left()[0] - 0.1:
            c.shift(LEFT * (c.get_right()[0] - self.door.get_left()[0] + 0.1))
        scene.play(FadeIn(c, shift=DOWN * 0.2), run_time=0.4)
        self.update_c = c
        self.keep(scene, c)
        return c

    def github(self, scene, run_time: float = 0.8):
        new_name = label("GitHub.com", 22, GITHUB).move_to(self.name, aligned_edge=LEFT)
        dashed = dashed_copy(VGroup(*self.gate.posts, self.gate.bar), S.GREY)
        note_ = grey_chip("your own scripts: not on GitHub.com").next_to(self.gate.text, DOWN, buff=0.12)
        note_.shift(RIGHT * (self.door.get_left()[0] - 0.15 - note_.get_right()[0]))
        if getattr(self, "update_c", None) is not None:
            self.drop(scene, self.update_c, run_time=0.3)
            self.update_c = None
        scene.play(FadeOut(self.name), FadeIn(new_name), FadeOut(self.gate.posts), FadeOut(self.gate.bar),
                   FadeIn(dashed), FadeIn(note_), run_time=run_time)
        self.remove(self.gate, self.name)
        scene.remove(self.gate, self.name)
        self.name = new_name
        self.gate_dashed = dashed
        act = github_chip("Actions").next_to(self.bell, UP, buff=0.12)
        prot = gate_glyph(0.9, 0.6, PASS).move_to(self.door.get_left() + LEFT * 0.42)
        prot.text = label("branch protection", 20, PASS).next_to(prot, UP, buff=0.12)
        prot.text.shift(LEFT * max(0, prot.text.get_right()[0] - (self.door.get_left()[0] - 0.12)))
        scene.play(FadeIn(act, shift=DOWN * 0.3), FadeIn(prot, shift=RIGHT * 0.3), FadeIn(prot.text), run_time=run_time)
        self.actions, self.protection = act, prot
        self.keep(scene, new_name, dashed, note_, act, prot, prot.text)
        return act, prot

    def protect(self, scene, shut: bool = True):
        p = self.protection
        if shut:
            scene.play(Indicate(p, color=PASS, scale_factor=1.1), p.bar.animate.set_color(PASS), run_time=0.6)
        else:
            scene.play(_gate_open(p), run_time=0.4)

    def caption(self, size: float = 22) -> Text:
        return label("Actions on a push is the bell, not the gate.", size, S.GREY)


class SharedRepo(Piece):
    """V1 (S02, slides 15-16): a BLUE 'Shared Repository' frame (box_w x box_h, at least 6.5 wide so
    the three boxes fit) with an empty GREY
    dashed slot where the checks would be. PLAYS fill() slide 16's three boxes 'Build Container'
    (TEAL inside) → 'Check Code' → 'Test Summary' replace the slot · pass_through(dot) the dot
    visits each box. .frame .title .slot .boxes .landing (a point inside, left)"""

    def __init__(self, box_w: float = 6.0, box_h: float = 2.4, title: str = "Shared Repository", **kw):
        super().__init__(**kw)
        self._bs = self._boxes()
        box_w = max(box_w, self._bs.width + 0.6)
        self.frame = box(box_w, box_h, GITHUB, fill_opacity=0.08, radius=0.2)
        self.title = label(title, 22, GITHUB).next_to(self.frame.get_corner(UL), DR, buff=0.18)
        self.slot = outline_box(box_w - 0.6, 0.8, S.GREY).move_to(self.frame).shift(DOWN * 0.2)
        self.add(self.frame, self.title, self.slot)
        self.boxes = VGroup()

    @property
    def landing(self):
        """A point inside the frame, left (where a pushed dot lands)."""
        return self.frame.get_center() + LEFT * (self.frame.width / 2 - 0.6) + DOWN * 0.2

    def _boxes(self):
        names = ("Build Container", "Check Code", "Test Summary")
        bs = VGroup()
        for n in names:
            t = label(n, 20, INK)
            col = IMAGE if n == "Build Container" else INK
            fr = RoundedRectangle(width=t.width + 0.3, height=0.62, corner_radius=0.1, stroke_color=col,
                                  stroke_width=2.5).set_fill(IMAGE if col == IMAGE else PANEL, 0.25 if col == IMAGE else 1)
            t.move_to(fr)
            b = VGroup(fr, t)
            b.frame, b.text = fr, t
            bs.add(b)
        return bs.arrange(RIGHT, buff=0.32)

    def fill(self, scene, per: float = 0.5):
        bs = self._bs.move_to(self.slot)
        ars = VGroup(*[arrow(a.get_right(), b.get_left(), S.GREY, 2.5, 0.05) for a, b in zip(bs[:-1], bs[1:])])
        scene.play(FadeOut(self.slot), run_time=0.3)
        self.remove(self.slot)
        for i, b in enumerate(bs):
            anims = [FadeIn(b, shift=DOWN * 0.2)]
            if i:
                anims.append(GrowArrow(ars[i - 1]))
            scene.play(*anims, run_time=per)
        self.boxes = bs
        self.keep(scene, ars, bs)
        return bs

    def pass_through(self, scene, dot_, step: float = 0.35, color=PASS):
        for b in self.boxes:
            scene.play(dot_.animate.move_to(b.frame.get_top() + UP * 0.2), run_time=step)
            scene.play(Circumscribe(b, color=color, buff=0.06), Indicate(b.text, color=color), run_time=0.3)


# ================================================================== V2 · the CI loop
class CiLoop(Piece):
    """V2 (slide 21): the CI loop, centred on its anchor, ~loop_w x loop_h (9.0 x 4.4). Top row
    'Codebase' → 'Build' → 'Test' (WHITE outlines in a GREY dashed frame); bottom left 'Developers'
    (two person icons); a PINK 'Commits' arrow up into Codebase; two dashed PINK return lines from
    Build and Test down into a GREY 'Notifications' bar, which leads back (dashed PINK) to the
    developers. PLAYS question() a YELLOW '?' on the return lines · marks(states) state marks on the
    bar (['success', 'failure', …]) · close() the return lines turn solid, the '?' goes · go_around(
    colour) a commit dot travels the loop (back along the returns as a ✓ when colour is GREEN) ·
    deploy() S16: a GREY dashed 'Deploy (CD)' / 'lecture 23' box right of Test (~2.2 more to the
    right: keep the loop's centre at x <= -1.1 before calling it).
    ANIM light(key, colour) key in 'codebase' 'build' 'test' 'devs' 'notify'.
    .boxes{key} .devs .notify .commits .returns .back .row_frame"""

    def __init__(self, loop_w: float = 9.0, loop_h: float = 4.4, size: float = 22, **kw):
        super().__init__(**kw)
        top, bot = loop_h / 2 - 0.45, -loop_h / 2 + 0.55
        self.boxes = {}
        xs = {"codebase": -loop_w / 2 + 3.6, "build": -loop_w / 2 + 5.9, "test": -loop_w / 2 + 8.0}
        for k, n in (("codebase", "Codebase"), ("build", "Build"), ("test", "Test")):
            t = label(n, size, INK)
            fr = RoundedRectangle(width=t.width + 0.5, height=0.7, corner_radius=0.1, stroke_color=INK,
                                  stroke_width=2.5).set_fill(PANEL, 1)
            t.move_to(fr)
            b = VGroup(fr, t).move_to([xs[k], top, 0])
            b.frame, b.text = fr, t
            self.boxes[k] = b
        row = VGroup(*self.boxes.values())
        self.row_frame = outline_box(row.width + 0.5, row.height + 0.4, S.GREY, solid=False).move_to(row)
        self.row_arrows = VGroup(arrow(self.boxes["codebase"], self.boxes["build"], S.GREY, 2.5, 0.08),
                                 arrow(self.boxes["build"], self.boxes["test"], S.GREY, 2.5, 0.08))
        icons = VGroup(person_icon(LAPTOP, 0.5), person_icon(LAPTOP, 0.5)).arrange(RIGHT, buff=0.12)
        dl = label("Developers", size, LAPTOP).next_to(icons, DOWN, buff=0.1)
        self.devs = VGroup(icons, dl).move_to([-loop_w / 2 + 1.0, bot, 0])
        nb_left = self.boxes["codebase"].get_left()[0] + 0.2
        nb_right = self.boxes["test"].get_right()[0]
        bar = RoundedRectangle(width=nb_right - nb_left, height=0.55, corner_radius=0.1, stroke_color=S.GREY,
                               stroke_width=2.5).set_fill(S.GREY, 0.12)
        bar.move_to([(nb_left + nb_right) / 2, bot, 0])
        nt = label("Notifications", 20, S.GREY).move_to(bar).align_to(bar, LEFT).shift(RIGHT * 0.25)
        self.notify = VGroup(bar, nt)
        self.notify.bar, self.notify.text = bar, nt
        c_from = self.devs.get_top() + UP * 0.05
        c_to = self.boxes["codebase"].get_left() + LEFT * 0.05
        path = VMobject().set_points_as_corners([c_from, np.array([c_from[0], c_to[1], 0]), c_to])
        self.commits_path = path.set_stroke(ROUTE, 4)
        tip = Arrow(c_to + LEFT * 0.4, c_to, buff=0, color=ROUTE, stroke_width=4, tip_length=0.2,
                    max_tip_length_to_length_ratio=0.5)
        ct = label("Commits", 20, ROUTE).next_to(path, LEFT, buff=0.12).shift(UP * 0.5)
        if ct.get_left()[0] < -loop_w / 2:
            ct.next_to(np.array([c_from[0], (c_from[1] + c_to[1]) / 2, 0]), RIGHT, buff=0.15)
        self.commits = VGroup(path, tip, ct)
        self.returns = VGroup()
        self.return_paths = []
        for k in ("build", "test"):
            a = self.boxes[k].get_bottom() + DOWN * 0.05
            b = np.array([a[0], bar.get_top()[1] + 0.05, 0])
            ln = Line(a, b)
            self.return_paths.append(ln)
            self.returns.add(DashedLine(a, b, color=ROUTE, stroke_width=3.5, dash_length=0.12))
        bk_a = bar.get_left() + LEFT * 0.05
        bk_b = self.devs.get_right() + RIGHT * 0.05
        self.back = DashedLine(bk_a, [bk_b[0], bk_a[1], 0], color=ROUTE, stroke_width=3.5, dash_length=0.12)
        self.back_path = Line(bk_a, [bk_b[0], bk_a[1], 0])
        self.add(self.row_frame, self.row_arrows, *self.boxes.values(), self.devs, self.notify, self.commits,
                 self.returns, self.back)
        self.q = None
        self.mark_row = VGroup()

    def light(self, key: str, color=TURN, run_time: float = 0.6):
        target = {"devs": self.devs, "notify": self.notify}.get(key)
        target = target if target is not None else self.boxes[key]
        inner = target.text if hasattr(target, "text") else target
        return AnimationGroup(Circumscribe(target, color=color, buff=0.08), Indicate(inner, color=color,
                              scale_factor=1.06), run_time=run_time)

    def question(self, scene):
        mid = (self.returns[0].get_center() + self.returns[1].get_center()) / 2
        self.q = label("?", 32, TURN).move_to(mid)
        scene.play(FadeIn(self.q, scale=1.4), run_time=0.4)
        self.keep(scene, self.q)
        return self.q

    def marks(self, scene, states, run_time: float = 0.6):
        ms = VGroup(*[state_mark(s, 0.3) for s in states]).arrange(RIGHT, buff=0.12)
        ms.move_to(self.notify.bar).align_to(self.notify.bar, RIGHT).shift(LEFT * 0.25)
        scene.play(LaggedStart(*[FadeIn(m, shift=DOWN * 0.3) for m in ms], lag_ratio=0.2), run_time=run_time)
        if len(self.mark_row):
            self.drop(scene, self.mark_row, run_time=0.2)
        self.mark_row = ms
        self.keep(scene, ms)
        return ms

    def close(self, scene, run_time: float = 0.6):
        solid = VGroup(*[Line(r.get_start(), r.get_end(), color=ROUTE, stroke_width=3.5) for r in self.returns])
        back = Line(self.back.get_start(), self.back.get_end(), color=ROUTE, stroke_width=3.5)
        anims = [Transform(self.returns, solid), Transform(self.back, back)]
        if self.q is not None:
            anims.append(FadeOut(self.q))
        scene.play(*anims, run_time=run_time)
        if self.q is not None:
            self.remove(self.q)
            scene.remove(self.q)
            self.q = None

    def go_around(self, scene, color=PASS, run_time: float = 3.0):
        d = dot(color)
        d.move_to(self.commits_path.get_start())
        scene.play(FadeIn(d), run_time=0.2)
        seg = run_time / 5
        scene.play(MoveAlongPath(d, self.commits_path), run_time=seg)
        scene.play(d.animate.move_to(self.boxes["build"].frame.get_top() + UP * 0.15), run_time=seg)
        scene.play(d.animate.move_to(self.boxes["test"].frame.get_top() + UP * 0.15), run_time=seg)
        mk = state_mark("success" if color == PASS else "failure", 0.32).move_to(self.boxes["test"].get_bottom())
        scene.play(FadeTransform_safe(d, mk), run_time=0.2)
        scene.play(mk.animate.move_to(self.return_paths[1].get_end()), run_time=seg * 0.6)
        scene.play(mk.animate.move_to(self.back_path.get_end() + RIGHT * 0.2), run_time=seg * 0.8)
        scene.play(FadeOut(mk), self.light("devs", color), run_time=0.4)
        scene.remove(d, mk)

    def deploy(self, scene, run_time: float = 0.8):
        t = VGroup(label("Deploy (CD)", 20, S.GREY), label("lecture 23", 20, S.GREY)).arrange(DOWN, buff=0.06)
        ob = outline_box(t.width + 0.4, t.height + 0.3, S.GREY)
        t.move_to(ob)
        g = VGroup(ob, t)
        tb = self.boxes["test"]
        g.next_to(tb, RIGHT, buff=0.55)
        a = DashedLine(tb.get_right() + RIGHT * 0.06, g.get_left() + LEFT * 0.06, color=S.GREY, stroke_width=2.5,
                       dash_length=0.08)
        scene.play(Create(a), FadeIn(g, shift=DOWN * 0.2), run_time=run_time)
        self.keep(scene, a, g)
        self.cd = VGroup(a, g)
        return self.cd


def FadeTransform_safe(a, b):
    from manim import FadeTransform
    return FadeTransform(a, b)


# ================================================================== V3 · when the robot wakes up
class TriggerLanes(Piece):
    """V3 (S04, S15): horizontal branch lanes, names on the left (mono 22: main GREEN, others WHITE),
    a GREY runner icon at each lane's right end, a GOLD 'runs' meter under the lanes. ~lane_w x
    (pitch x lanes + 1.3), centred on its anchor. triggers = the branches whose pushes start a run
    (ci.yml:7-9); pr_into = the PR targets (ci.yml:10-11).
    PLAYS push(lane) a commit dot lands on the lane; if the lane triggers: a PINK spark, the lane's
        runner lights BLUE and the meter ticks (returns the dot) · pr(src, dst, fire=True) a dashed PINK
        arc 'PR → main' from src's last dot up to dst (fire=False leaves it unlit; fire it later with
        pr_fire()) · pr_fire() the arc turns solid, a spark at dst's runner, a tick · ghost_merge(dst,
        src) a GREY dashed ghost commit 'github.sha' above dst's lane, joined to both tips; the runner
        arrow re-aims at it · tick() one GOLD block on the meter · reset_runners() all runners GREY.
    .lanes{name} (.line .name) .runners{name} .dots{name: [dots]} .meter .count .pr_arrow .ghost"""

    def __init__(self, lanes=("main", "develop", "feature/login"), triggers=TRIGGER_BRANCHES,
                 pr_into=TRIGGER_BRANCHES, lane_w: float = 9.0, pitch: float = 1.15, meter: bool = True, **kw):
        super().__init__(**kw)
        self.triggers, self.pr_into, self.pitch = tuple(triggers), tuple(pr_into), pitch
        self.lanes, self.runners, self.dots = {}, {}, {}
        n = len(lanes)
        x0 = -lane_w / 2
        names = {ln: mono(ln, 22, OWN if ln == "main" else INK) for ln in lanes}
        name_w = max(t.width for t in names.values())
        lx0, lx1 = x0 + name_w + 0.3, lane_w / 2 - 1.1
        for i, ln in enumerate(lanes):
            y = pitch * ((n - 1) / 2 - i)
            nm = names[ln].move_to([x0, y, 0], aligned_edge=LEFT)
            line = Line([lx0, y, 0], [lx1, y, 0], color=OWN if ln == "main" else S.GREY, stroke_width=3)
            r = runner_icon(0.42).move_to([lane_w / 2 - 0.4, y, 0])
            g = VGroup(nm, line)
            g.line, g.name = line, nm
            self.lanes[ln], self.runners[ln], self.dots[ln] = g, r, []
            self.add(g, r)
        self.lx0, self.lx1 = lx0, lx1
        self.count = 0
        self.meter = VGroup()
        if meter:
            y = -pitch * (n - 1) / 2 - 0.85
            ml = label("runs", 20, COST).move_to([x0, y, 0], aligned_edge=LEFT)
            self.meter = VGroup(ml)
            self.add(self.meter)
        self.pr_arrow = self.ghost = None

    def _next_x(self, lane):
        k = len(self.dots[lane])
        return self.lx0 + 0.6 + k * 0.62

    def _spark(self, scene, lane):
        r = self.runners[lane]
        sp = spark().move_to(r)
        lit = runner_icon(0.42, lit=True).move_to(r)
        scene.play(FadeIn(sp, scale=0.5), Transform(r, lit), run_time=0.35)
        scene.play(FadeOut(sp, scale=1.4), run_time=0.25)
        scene.remove(sp)
        self.tick(scene)

    def push(self, scene, lane: str, color=OWN):
        x = self._next_x(lane)
        y = self.lanes[lane].line.get_center()[1]
        d = dot(color if lane == "main" else INK, 0.12).move_to([x, y + 0.6, 0])
        scene.play(FadeIn(d), run_time=0.15)
        scene.play(d.animate.move_to([x, y, 0]), run_time=0.3)
        self.dots[lane].append(d)
        self.keep(scene, d)
        if lane in self.triggers:
            self._spark(scene, lane)
        return d

    def pr(self, scene, src: str = "feature/login", dst: str = "main", fire: bool = True):
        a = (self.dots[src][-1].get_center() if self.dots[src] else self.lanes[src].line.get_end())
        b = np.array([self.lx1 - 0.3, self.lanes[dst].line.get_center()[1], 0])
        ar = route(a + UP * 0.12, b + DOWN * 0.12, arc=-0.6, dashed=True)
        t = label(f"PR → {dst}", 20, ROUTE)
        t.move_to([ar.get_center()[0] - t.width / 2 - 0.35, (a[1] + b[1]) / 2 + 0.25, 0])
        scene.play(Create(ar), FadeIn(t), run_time=0.6)
        self.pr_arrow, self.pr_label, self.pr_dst = ar, t, dst
        self.pr_a, self.pr_b = a + UP * 0.12, b + DOWN * 0.12
        self.keep(scene, ar, t)
        if fire:
            self.pr_fire(scene)
        return ar

    def pr_fire(self, scene):
        solid = route(self.pr_a, self.pr_b, arc=-0.6)
        scene.play(Transform(self.pr_arrow, solid), run_time=0.3)
        if self.pr_dst in self.pr_into:
            self._spark(scene, self.pr_dst)

    def ghost_merge(self, scene, dst: str = "main", src: str = "feature/login"):
        y = self.lanes[dst].line.get_center()[1] + self.pitch * 0.55
        x = self.lx1 - 0.9
        c = DashedVMobject(Circle(radius=0.16), num_dashes=10).set_stroke(S.GREY, 2.5).move_to([x, y, 0])
        t = mono("github.sha", 20, S.GREY).next_to(c, UP, buff=0.1)
        tip_d = self.dots[dst][-1].get_center() if self.dots[dst] else self.lanes[dst].line.get_end()
        tip_s = self.dots[src][-1].get_center() if self.dots[src] else self.lanes[src].line.get_end()
        l1 = DashedLine(tip_d, c.get_center(), color=S.GREY, stroke_width=2, buff=0.18)
        l2 = DashedLine(tip_s, c.get_center(), color=S.GREY, stroke_width=2, buff=0.18)
        aim = arrow(c, self.runners[dst], ROUTE, 3, 0.2)
        scene.play(Create(l1), Create(l2), FadeIn(c), FadeIn(t), run_time=0.7)
        scene.play(GrowArrow(aim), run_time=0.4)
        self.ghost = VGroup(c, t, l1, l2, aim)
        self.keep(scene, self.ghost)
        return self.ghost

    def tick(self, scene):
        if not len(self.meter):
            return
        b = Square(side_length=0.26, stroke_color=COST, stroke_width=2).set_fill(COST, 0.5)
        last = self.meter[-1]
        b.next_to(last, RIGHT, buff=0.12 if self.count else 0.25)
        scene.play(FadeIn(b, scale=0.5), run_time=0.2)
        self.meter.add(b)
        self.count += 1
        scene.add(self)

    def reset_runners(self, scene):
        scene.play(*[Transform(r, runner_icon(0.42).move_to(r)) for r in self.runners.values()], run_time=0.3)


# ================================================================== V4 · S03's grammar tree
class WorkflowTree(Piece):
    """V4, S03 form: ci.yml as a tree, ~12.4 x 4.6, centred on its anchor. Left: the PINK root
    'on: push · pull_request' → a WHITE 'workflow: CI Pipeline' → a column of six BLUE job ids. Right:
    the build job's five steps (ci.yml:19-38), each with a PURPLE puzzle piece (uses:) or a '>_'
    glyph (run:), joined to `build` by GREY connectors.
    PLAYS open_job() the steps appear one by one · dim_others() the five other jobs dim.
    ANIM pulse(layer) layer in 'event' 'workflow' 'jobs' 'steps'.
    .root .wf .jobs{id} .steps (rows: .glyph .text) .links"""

    BUILD_STEPS = (("Checkout code", "uses"), ("Set up Docker Buildx", "uses"), ("Build Docker image", "run"),
                   ("Save Docker image", "run"), ("Upload Docker image artifact", "uses"))

    def __init__(self, size: float = 22, **kw):
        super().__init__(**kw)
        self.root = route_chip("on: push · pull_request", 22, mono_font=True)
        self.wf = chip("workflow: CI Pipeline", INK, size=22)
        self.jobs = {}
        col = VGroup()
        for j in JOB_IDS:
            c = chip(j, GITHUB, size=22, font=MONO)
            self.jobs[j] = c
            col.add(c)
        col.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        self.root.move_to([-6.2, 2.0, 0], aligned_edge=LEFT)
        self.wf.next_to(self.root, DOWN, buff=0.25).align_to(self.root, LEFT).shift(RIGHT * 0.6)
        col.next_to(self.wf, DOWN, buff=0.25).align_to(self.wf, LEFT).shift(RIGHT * 0.6)
        self.col = col
        self.links = VGroup(
            _elbow(self.root.get_bottom() + LEFT * (self.root.width / 2 - 0.3), self.wf.get_left(),
                   xm=self.root.get_left()[0] + 0.3).set_stroke(S.GREY, 2),
        )
        x = self.wf.get_left()[0] + 0.3
        for c in col:
            self.links.add(_elbow(np.array([x, self.wf.get_bottom()[1], 0]), c.get_left(), xm=x).set_stroke(S.GREY, 2))
        self.steps = VGroup()
        for name, kind in self.BUILD_STEPS:
            gl = puzzle_glyph(0.34) if kind == "uses" else script_glyph(0.4)
            t = label(name, size, INK)
            r = VGroup(gl, t).arrange(RIGHT, buff=0.2)
            r.glyph, r.text, r.kind = gl, t, kind
            self.steps.add(r)
        self.steps.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        self.steps.move_to([col.get_right()[0] + 1.1, 0, 0], aligned_edge=LEFT)
        self.steps.align_to(self.jobs["build"], UP).shift(UP * 0.1)
        self.add(self.links, self.root, self.wf, col)
        self.step_links = VGroup()
        bx = self.jobs["build"].get_right()
        xm = col.get_right()[0] + 0.5
        for r in self.steps:
            self.step_links.add(_elbow(bx, r.get_left() + LEFT * 0.08, xm=xm).set_stroke(S.GREY, 2))
        full = VGroup(self.links, self.root, self.wf, col, self.steps, self.step_links)
        shift = -full.get_center()
        self.shift(shift)
        self.steps.shift(shift)
        self.step_links.shift(shift)

    def open_job(self, scene, per: float = 0.3):
        for r, ln in zip(self.steps, self.step_links):
            scene.play(Create(ln), FadeIn(r, shift=LEFT * 0.2), run_time=per)
        self.keep(scene, self.step_links, self.steps)

    def dim_others(self, scene, run_time: float = 0.5):
        scene.play(*[c.animate.set_opacity(0.3) for j, c in self.jobs.items() if j != "build"], run_time=run_time)

    def pulse(self, layer: str, color=TURN, run_time: float = 0.6):
        target = {"event": self.root, "workflow": self.wf, "jobs": self.col, "steps": self.steps}[layer]
        return Indicate(target, color=color, scale_factor=1.05, run_time=run_time)


# ================================================================== V5 · build once, every job starts empty
class ImageSuitcase(Piece):
    """V5 (S07 inset, S08): six BLUE rooms in the graph's layout, each a fresh machine with an empty
    'Docker' shelf; the artifact store (a BLUE shelf, bottom centre) and an ORANGE 'Docker Hub' door
    (bottom right). Fits y in [-3.45, 2.1] (Part 2, under the strip) when centred at (0, -0.65).
    Build room (left edge at x -6.5 relative to the anchor, ~3.7 wide, 2.1 tall), four check rooms
    (middle column, MIDDLE order, room_w x 0.8), summary room (right).
    PLAYS build_cube() three Dockerfile layers stack into a TEAL cube stamped IMAGE_TAG · fold() the
        cube folds into the tar suitcase ('tar · ≈ 176 MB') · upload() it flies to the store; GOLD
        '1 day' tag · dissolve_build() the build room goes · deliver(jobs=MIDDLE) a suitcase copy flies
        to each shelf (the summary room gets none) · load(job) the copy unfolds into a cube · no_load(
        job) that room's shelf flashes empty, a PINK '?' walks to Docker Hub and is turned away RED.
    .rooms{id} (.frame .text .shelf) .store .hub .cube .stamp .case .copies{id} .cubes{id}"""

    def __init__(self, room_w: float = 2.6, room_h: float = 0.8, size: float = 20, hub: bool = True, **kw):
        super().__init__(**kw)
        self.rooms = {}
        pos = {"build": np.array([-4.6, 0.55, 0]), "test-summary": np.array([4.6, 0.55, 0])}
        for i, j in enumerate(MIDDLE):
            pos[j] = np.array([-0.2, 1.95 - i * (room_h + 0.18), 0])
        build_w = max(room_w + 0.9, mono(IMAGE_TAG, 20).width + 0.5)
        pos["build"] = np.array([-6.5 + build_w / 2, 0.55, 0])
        for j in JOB_IDS:
            w, h = (build_w, 2.1) if j == "build" else (room_w, room_h)
            fr = box(w, h, GITHUB, fill_opacity=0.08, radius=0.12).move_to(pos[j])
            t = label(SHORT[j], size, GITHUB).next_to(fr.get_corner(UL), DR, buff=0.1)
            sh = shelf(1.0, size).next_to(fr.get_corner(DR), UL, buff=0.12)
            if j == "build":
                sh.move_to(fr.get_bottom() + UP * 0.2)
            r = VGroup(fr, t, sh)
            r.frame, r.text, r.shelf = fr, t, sh
            self.rooms[j] = r
            self.add(r)
        st = Line(LEFT * 1.9, RIGHT * 1.9, color=GITHUB, stroke_width=5).move_to([-0.2, -2.45, 0])
        stt = label("artifact store", size, GITHUB).next_to(st, DOWN, buff=0.12)
        self.store = VGroup(st, stt)
        self.store.board, self.store.text = st, stt
        self.add(self.store)
        self.hub = VGroup()
        if hub:
            d = door_glyph("Docker Hub", SHARED, 0.8, size).move_to([4.6, -2.0, 0])
            self.hub = d
            self.add(d)
        self.cube = self.stamp = self.case = self.case_tag = None
        self.copies, self.cubes = {}, {}

    def build_cube(self, scene, per: float = 0.3):
        r = self.rooms["build"]
        layers = VGroup(*[Rectangle(width=1.2, height=0.18, stroke_color=IMAGE, stroke_width=2).set_fill(IMAGE, 0.3)
                          for _ in range(3)]).arrange(UP, buff=0.04)
        layers.move_to(r.frame.get_top() + DOWN * 0.85)
        for ly in layers:
            scene.play(FadeIn(ly, shift=DOWN * 0.4), run_time=per)
        cube = cube_glyph(0.7).move_to(layers)
        stamp = mono(IMAGE_TAG, 20, IMAGE).next_to(cube, DOWN, buff=0.1)
        scene.play(ReplacementTransform(layers, cube), FadeIn(stamp), run_time=0.6)
        self.cube, self.stamp = cube, stamp
        self.keep(scene, cube, stamp)
        return cube

    def fold(self, scene):
        case = suitcase_glyph(0.55).move_to(self.cube)
        t = label("tar · " + TAR_SIZE, 20, IMAGE).next_to(case, DOWN, buff=0.1)
        scene.play(ReplacementTransform(self.cube, case), ReplacementTransform(self.stamp, t), run_time=0.7)
        self.remove(self.cube, self.stamp)
        self.case, self.case_tag, self.cube, self.stamp = case, t, None, None
        self.keep(scene, case, t)
        return case

    def upload(self, scene):
        tgt = self.store.board.get_center() + UP * 0.32
        scene.play(self.case.animate.move_to(tgt), FadeOut(self.case_tag), run_time=0.8)
        self.remove(self.case_tag)
        scene.remove(self.case_tag)
        day = cost_tag("1 day").next_to(self.store.board, RIGHT, buff=0.15)
        scene.play(FadeIn(day), run_time=0.3)
        self.day = day
        self.keep(scene, day)

    def dissolve_build(self, scene):
        self.drop(scene, self.rooms["build"], run_time=0.6)

    def deliver(self, scene, jobs=MIDDLE, run_time: float = 0.9):
        anims = []
        for j in jobs:
            c = suitcase_glyph(0.3).move_to(self.case)
            self.copies[j] = c
            anims.append(c.animate.next_to(self.rooms[j].shelf.board, UP, buff=0.03))
        scene.add(*self.copies.values())
        scene.play(*anims, run_time=run_time)
        self.keep(scene, *[self.copies[j] for j in jobs])

    def load(self, scene, job: str):
        c = self.copies[job]
        cb = cube_glyph(0.3).next_to(self.rooms[job].shelf.board, UP, buff=0.03)
        scene.play(ReplacementTransform(c, cb), run_time=0.5)
        self.remove(c)
        self.cubes[job] = cb
        self.keep(scene, cb)
        return cb

    def no_load(self, scene, job: str = "unit-tests"):
        r = self.rooms[job]
        q = label("?", 26, ROUTE).next_to(r.shelf.board, UP, buff=0.05)
        scene.play(FadeIn(q), Indicate(r.shelf.board, color=S.GREY), run_time=0.5)
        path = _elbow(q.get_center(), self.hub.frame.get_left() + LEFT * 0.15,
                      xm=r.frame.get_right()[0] + 0.4)
        scene.play(MoveAlongPath(q, path), run_time=1.0)
        x = cross_mark(0.35, ERR).move_to(self.hub.frame)
        scene.play(FadeIn(x, scale=1.5), q.animate.set_color(ERR), run_time=0.4)
        scene.play(q.animate.shift(LEFT * 0.5), run_time=0.3)
        self.keep(scene, q, x)
        self.denied = VGroup(q, x)
        return self.denied


# ================================================================== V6 · gates speak in exit codes
class ExitGates(Piece):
    """V6 (S09): a job as a column of step gates, names right-aligned on the left (20 pt), each gate a
    gate_glyph; a 'job' badge and a 'run' badge under the column. Centred on its anchor; ~6.6 wide,
    len(names) x (gate_h + 0.18) + 1.0 tall.
    PLAYS hold(i, code) the gate holds up a mono chip with the exit code: 0 opens GREEN, else shuts RED
        · climb() red climbs gate → job badge → run badge · skip(indices) those gates and names go
        GREY dashed ('skipped') · shunt(i, code) GREY arc around gate i, its code still shows, a small
        YELLOW warning dot on the job badge (continue-on-error) · bridge(i) a PINK 'always' arc from
        the failed gate down to gate i, which opens · reset() everything back to GREY.
    .gates[i] (.bar .posts) .names[i] .codes{i} .job_badge .run_badge .failed (index or None)"""

    def __init__(self, names=("Checkout", "Download", "Load", "Black", "Flake8"), gate_h: float = 0.55,
                 size: float = 20, **kw):
        super().__init__(**kw)
        self.gates, self.names = VGroup(), VGroup()
        pitch = gate_h + 0.2
        for i, n in enumerate(names):
            g = gate_glyph(gate_h, 0.8, S.GREY).move_to([0.6, -i * pitch, 0])
            t = label(n, size, INK).move_to([0.0, -i * pitch, 0], aligned_edge=RIGHT)
            self.gates.add(g)
            self.names.add(t)
        self.add(self.names, self.gates)
        y = -len(names) * pitch - 0.1
        self.job_badge = self._badge("job").move_to([0.2, y, 0])
        self.run_badge = self._badge("run").next_to(self.job_badge, RIGHT, buff=0.6)
        self.add(self.job_badge, self.run_badge)
        self.codes, self.failed, self.extras = {}, None, VGroup()
        self.opened, self.skipped = set(), set()
        self.center()

    def _badge(self, text, state="idle"):
        mk = state_mark(state, 0.28)
        t = label(text, 20, INK)
        row = VGroup(mk, t).arrange(RIGHT, buff=0.15)
        fr = RoundedRectangle(width=row.width + 0.36, height=row.height + 0.22, corner_radius=0.1,
                              stroke_color=S.GREY_DARK if state == "idle" else STATE_COLOR[state],
                              stroke_width=2.5).set_fill(PANEL, 1)
        row.move_to(fr)
        g = VGroup(fr, row)
        g.frame, g.mark, g.text, g.word = fr, mk, t, text
        return g

    def _set_badge(self, b, state):
        nb = self._badge(b.word, state).move_to(b)
        return Transform(b, nb)

    def hold(self, scene, i: int, code_: int):
        g = self.gates[i]
        c = chip(str(code_), PASS if code_ == 0 else ERR, size=22, font=MONO).next_to(g, RIGHT, buff=0.3)
        scene.play(FadeIn(c, shift=UP * 0.2), run_time=0.3)
        if code_ == 0:
            scene.play(_gate_open(g), run_time=0.4)
            self.opened.add(i)
        else:
            scene.play(_gate_shut(g), run_time=0.4)
            self.failed = i
        self.codes[i] = c
        self.keep(scene, c)
        return c

    def climb(self, scene):
        g = self.gates[self.failed if self.failed is not None else 0]
        spot = Dot(g.get_center(), radius=0.1, color=ERR)
        scene.play(FadeIn(spot), run_time=0.15)
        scene.play(spot.animate.move_to(self.job_badge.mark), run_time=0.45)
        scene.play(self._set_badge(self.job_badge, "failure"), run_time=0.3)
        scene.play(spot.animate.move_to(self.run_badge.mark), run_time=0.45)
        scene.play(self._set_badge(self.run_badge, "failure"), FadeOut(spot), run_time=0.3)
        scene.remove(spot)

    def skip(self, scene, indices):
        anims, ghosts = [], []
        for i in indices:
            g = self.gates[i]
            d = dashed_copy(VGroup(*g.posts, g.bar), S.GREY)
            ghosts.append(d)
            anims += [g.animate.set_opacity(0.0), FadeIn(d), self.names[i].animate.set_color(S.GREY)]
            self.skipped.add(i)
        scene.play(*anims, run_time=0.5)
        self.keep(scene, *ghosts)
        self.extras.add(*ghosts)

    def shunt(self, scene, i: int, code_: int = 1):
        g = self.gates[i]
        c = chip(str(code_), ERR, size=22, font=MONO).next_to(g, RIGHT, buff=0.3)
        scene.play(FadeIn(c, shift=UP * 0.2), _gate_shut(g), run_time=0.4)
        x = c.get_right()[0] + 0.12
        arc = ArcBetween(np.array([x, g.get_top()[1] + 0.05, 0]), np.array([x, g.get_bottom()[1] - 0.05, 0]),
                         angle=-PI * 0.9, color=S.GREY)
        warn = Dot(radius=0.07, color=TURN).move_to(self.job_badge.frame.get_corner(UR))
        scene.play(Create(arc), FadeIn(warn), run_time=0.5)
        self.codes[i] = c
        self.keep(scene, c, arc, warn)
        self.extras.add(arc, warn)
        return arc

    def bridge(self, scene, i: int, text: str = "always"):
        src = self.gates[self.failed if self.failed is not None else 0]
        a = np.array([self.names.get_left()[0] - 0.15, src.get_center()[1], 0])
        b = np.array([a[0], self.gates[i].get_center()[1], 0])
        arc = ArcBetween(a, b, angle=PI * 0.6, color=ROUTE)
        t = label(text, 20, ROUTE).next_to(arc, LEFT, buff=0.08)
        scene.play(Create(arc), FadeIn(t), run_time=0.5)
        scene.play(_gate_open(self.gates[i]), run_time=0.4)
        self.opened.add(i)
        self.keep(scene, arc, t)
        self.extras.add(arc, t)
        return VGroup(arc, t)

    def reset(self, scene):
        olds = list(self.codes.values()) + list(self.extras)
        if olds:
            self.drop(scene, *olds, run_time=0.3)
        anims = []
        for i, (g, n) in enumerate(zip(self.gates, self.names)):
            if i in self.opened:
                anims.append(_gate_close(g))
        scene.play(*anims, run_time=0.3) if anims else None
        anims = [g.animate.set_opacity(1).set_color(S.GREY) for g in self.gates]
        anims += [n.animate.set_color(INK) for n in self.names]
        anims += [self._set_badge(self.job_badge, "idle"), self._set_badge(self.run_badge, "idle")]
        scene.play(*anims, run_time=0.5)
        self.codes, self.failed, self.extras = {}, None, VGroup()
        self.opened, self.skipped = set(), set()


# ================================================================== V7 · one runner, two containers, one port
class SystemTestRig(Piece):
    """V7 (S10): one BLUE runner (rig_w x rig_h, title 'runner · ubuntu-latest'), centred on its
    anchor. Built empty; the parts arrive with the PLAYS methods:
    server_up() a TEAL 'api-server' container (left) with the GREY chip '-e DEV=1' and an ORANGE door
        '9000' on its right edge (-p 9000:9000) · wait(seconds=10) a 'sleep 10' hourglass empties (top
        middle) · knock(ok=True) a PINK 'curl -f' arrow knocks on the door; a GREEN check (or RED
        cross) comes back · tests_up() a TEAL 'tests' container (right) inside its own GREY dashed
        network bubble · host_net() the bubble dissolves ('--network host') and a PINK 'localhost:9000'
        arrow reaches the door · arrivals(labels) PINK dots arrive at the door one by one, each with a
        GREY label stacked under the server ('curl', 'skipif probe', 'tests') · stop() the server
        container goes. trapdoor() a small GREY dashed 'skipif' hatch, shut (a mobject, not added).
    .runner .server .door .tests .bubble .curl .hour"""

    def __init__(self, rig_w: float = 10.0, rig_h: float = 4.2, **kw):
        super().__init__(**kw)
        self.runner = box(rig_w, rig_h, GITHUB, fill_opacity=0.06, radius=0.2)
        self.title = label("runner · ubuntu-latest", 22, GITHUB).next_to(self.runner.get_corner(UL), DR, buff=0.18)
        self.add(self.runner, self.title)
        self.rig_w, self.rig_h = rig_w, rig_h
        self.server = self.door = self.tests = self.bubble = self.curl = self.hour = None
        self.n_arr = 0

    def _container(self, name, w=2.8, h=1.3):
        fr = box(w, h, IMAGE, fill_opacity=0.15, radius=0.12)
        t = mono(name, 22, IMAGE).move_to(fr)
        g = VGroup(fr, t)
        g.frame, g.text = fr, t
        return g

    def server_up(self, scene):
        c = self.runner.get_center()
        sv = self._container("api-server").move_to(c + np.array([-self.rig_w * 0.3, -0.35, 0]))
        dev = grey_chip("-e DEV=1", mono_font=True).next_to(sv, DOWN, buff=0.12)
        door = door_glyph("9000", SHARED, 0.8).move_to(sv.frame.get_right() + RIGHT * 0.3)
        door.shift(DOWN * (door.frame.get_center()[1] - sv.get_center()[1]))
        scene.play(FadeIn(sv, scale=0.9), run_time=0.5)
        scene.play(FadeIn(door, shift=LEFT * 0.2), FadeIn(dev), run_time=0.4)
        self.server, self.door, self.dev = sv, door, dev
        self.keep(scene, sv, door, dev)

    def wait(self, scene, seconds: float = 1.2):
        hg = hourglass(0.6).move_to(self.runner.get_center() + np.array([-0.4, self.rig_h / 2 - 0.75, 0]))
        t = mono("sleep 10", 20, S.GREY).next_to(hg, RIGHT, buff=0.15)
        scene.play(FadeIn(hg), FadeIn(t), run_time=0.3)
        top, bot = hg.sand_top, hg.sand_bot
        scene.play(top.animate.stretch(0.05, 1, about_edge=DOWN), bot.animate.stretch(1.6, 1, about_edge=DOWN),
                   run_time=seconds, rate_func=linear)
        self.hour = VGroup(hg, t)
        self.keep(scene, self.hour)

    def knock(self, scene, ok: bool = True):
        t = mono("curl -f", 20, ROUTE).move_to(self.runner.get_center() + np.array([0.2, 0.45, 0]))
        ar = route(t.get_left() + LEFT * 0.1, self.door.frame.get_right() + RIGHT * 0.05, arc=0.35)
        scene.play(FadeIn(t), GrowArrow(ar), run_time=0.5)
        scene.play(Indicate(self.door.frame, color=ROUTE), run_time=0.4)
        mk = (check_mark(0.3, PASS) if ok else cross_mark(0.3, ERR)).next_to(t, RIGHT, buff=0.15)
        scene.play(FadeIn(mk, scale=1.4), run_time=0.3)
        self.curl = VGroup(t, ar, mk)
        self.keep(scene, self.curl)

    def tests_up(self, scene):
        tc = self._container("tests", 2.4, 1.3).move_to(self.runner.get_center() + np.array([self.rig_w * 0.3, -0.35, 0]))
        bub = DashedVMobject(RoundedRectangle(width=tc.width + 0.5, height=tc.height + 0.5, corner_radius=0.3),
                             num_dashes=30).set_stroke(S.GREY, 2.5).move_to(tc)
        scene.play(FadeIn(tc, scale=0.9), Create(bub), run_time=0.6)
        self.tests, self.bubble = tc, bub
        self.keep(scene, tc, bub)

    def host_net(self, scene):
        nt = mono("--network host", 20, S.GREY).next_to(self.bubble, UP, buff=0.1)
        scene.play(FadeIn(nt), run_time=0.3)
        scene.play(FadeOut(self.bubble, scale=1.3), run_time=0.6)
        self.remove(self.bubble)
        scene.remove(self.bubble)
        ar = route(self.tests.frame.get_left(), self.door.frame.get_right() + RIGHT * 0.05, arc=-0.25)
        t = mono("localhost:9000", 20, ROUTE).next_to(ar, DOWN, buff=0.1)
        scene.play(GrowArrow(ar), FadeIn(t), run_time=0.6)
        self.net = VGroup(nt, ar, t)
        self.keep(scene, self.net)

    def arrivals(self, scene, labels=("curl", "skipif probe", "tests"), per: float = 0.4):
        col = VGroup()
        for s in labels:
            d = Dot(radius=0.08, color=ROUTE).move_to(self.door.frame.get_right() + RIGHT * 1.2)
            scene.play(FadeIn(d), run_time=0.1)
            scene.play(d.animate.move_to(self.door.frame), run_time=per)
            t = label(s, 20, S.GREY)
            if len(col):
                t.next_to(col[-1], RIGHT, buff=0.25)
            else:
                t.next_to(self.server, UP, buff=0.15).align_to(self.server, LEFT)
            scene.play(FadeOut(d), FadeIn(t), run_time=0.25)
            scene.remove(d)
            col.add(t)
        self.keep(scene, col)
        self.arr_labels = col
        return col

    def stop(self, scene):
        scene.play(self.server.animate.set_opacity(0.2), run_time=0.5)
        self.drop(scene, self.server, run_time=0.3)

    def trapdoor(self) -> VGroup:
        hatch = DashedVMobject(Rectangle(width=1.2, height=0.3), num_dashes=16).set_stroke(S.GREY, 2.5)
        hinge = Dot(hatch.get_left(), radius=0.05, color=S.GREY)
        t = mono("skipif", 20, S.GREY).next_to(hatch, UP, buff=0.1)
        return VGroup(hatch, hinge, t)


# ================================================================== V8 · who calls whom
class SlackRoute(Piece):
    """V8 (S14): the two directions of a webhook, centred on its anchor, ~12.4 x 4.3.
    Top band (y +0.4 .. +2.0 relative): GitHub's box (left) and the outward targets (right).
    Bottom band (y -2.3 .. -0.6): a BLUE runner (left) whose last test-summary steps POST into the
    GREY Slack window '#build-alerts' (right) with its PINK 'incoming webhook' slot and a GREY bell.
    PLAYS outward(targets=('external CI (Jenkins)', 'deploy server', 'chat')) PINK 'POST' arrows out,
        one per target · ghost_outward() the top band dims, 'the other direction' · inward() the
        bottom band, PINK 'POST' into the slot · silence() the bell slashed RED · ring(ok=False) the
        bell rings and a ✗ (or ✓) card lands in the window.
    .github .targets .out_arrows .runner .slack .slot .bell"""

    def __init__(self, **kw):
        super().__init__(**kw)
        self.github = github_box("GitHub", 2.2, 1.0).move_to([-4.6, 1.2, 0])
        self.targets = VGroup()
        self.out_arrows = VGroup()
        self.top = VGroup(self.github)
        rf = box(4.6, 1.7, GITHUB, fill_opacity=0.08, radius=0.16).move_to([-3.9, -1.45, 0])
        rt = label("runner · test-summary", 20, GITHUB).next_to(rf.get_corner(UL), DR, buff=0.12)
        st = VGroup(label("Check test results", 20, INK), label("Send Slack notification", 20, INK)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).next_to(rt, DOWN, buff=0.15).align_to(rt, LEFT)
        self.runner = VGroup(rf, rt, st)
        self.runner.frame, self.runner.steps = rf, st
        self.slack = chat_window(CHANNEL, (), 4.4, 1.9).move_to([3.9, -1.45, 0])
        slot = RoundedRectangle(width=2.6, height=0.42, corner_radius=0.08, stroke_color=ROUTE,
                                stroke_width=2.5).set_fill(S.BG, 1)
        slot.move_to(self.slack.frame.get_bottom() + UP * 0.38).align_to(self.slack.frame, LEFT).shift(RIGHT * 0.25)
        slt = label("incoming webhook", 20, ROUTE).move_to(slot)
        self.slot = VGroup(slot, slt)
        self.bell = bell_glyph(0.55, S.GREY).move_to(self.slack.frame.get_right() + LEFT * 0.6 + DOWN * 0.2)
        self.bottom = VGroup(self.runner, self.slack, self.slot, self.bell)
        self.add(self.github)

    def outward(self, scene, targets=("external CI (Jenkins)", "deploy server", "chat"), per: float = 0.6):
        ys = np.linspace(1.9, 0.5, len(targets))
        for t, y in zip(targets, ys):
            c = grey_chip(t).move_to([3.6, y, 0])
            ar = route(self.github.frame.get_right(), c.get_left() + LEFT * 0.05)
            pt = label("POST", 20, ROUTE).next_to(c, LEFT, buff=0.25).shift(UP * 0.2)
            scene.play(GrowArrow(ar), FadeIn(pt), FadeIn(c, shift=LEFT * 0.2), run_time=per)
            self.targets.add(c)
            self.out_arrows.add(VGroup(ar, pt))
            self.keep(scene, c, ar, pt)
        self.top = VGroup(self.github, self.targets, self.out_arrows)

    def ghost_outward(self, scene):
        t = label("the other direction", 20, S.GREY).next_to(self.github, DOWN, buff=0.15)
        scene.play(self.top.animate.set_opacity(0.3), FadeIn(t), run_time=0.6)
        self.keep(scene, t)

    def inward(self, scene):
        scene.play(FadeIn(self.runner), FadeIn(self.slack), FadeIn(self.slot), FadeIn(self.bell), run_time=0.6)
        ar = route(self.runner.frame.get_right(), self.slot[0].get_left())
        pt = label("POST", 20, ROUTE).move_to(ar.get_center() + UP * 0.22)
        scene.play(GrowArrow(ar), FadeIn(pt), run_time=0.6)
        self.in_arrow = VGroup(ar, pt)
        self.keep(scene, self.runner, self.slack, self.slot, self.bell, self.in_arrow)

    def silence(self, scene):
        nb = bell_glyph(0.55, S.GREY, slashed=True).move_to(self.bell)
        scene.play(Transform(self.bell, nb), run_time=0.5)

    def ring(self, scene, ok: bool = False):
        nb = bell_glyph(0.55, PASS if ok else ERR).move_to(self.bell)
        scene.play(Transform(self.bell, nb), run_time=0.3)
        w = ring_waves(self.bell, PASS if ok else ERR)
        mk = (check_mark(0.3, PASS) if ok else cross_mark(0.3, ERR))
        card = VGroup(mk, label("CI Pipeline " + ("Passed" if ok else "Failed"), 20, INK)).arrange(RIGHT, buff=0.15)
        card.next_to(self.slack.title, DOWN, buff=0.15).align_to(self.slack.title, LEFT)
        scene.play(LaggedStart(*[Create(a) for a in w], lag_ratio=0.2), FadeIn(card, shift=DOWN * 0.2), run_time=0.7)
        self.keep(scene, w, card)
        return card
