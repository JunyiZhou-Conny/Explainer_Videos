"""Shared scene code for AC215 L23 (Final Deployment and Review; follow-along of
dlops-io/cheese-app-aws @ 5950118: the README top to bottom, then .github/workflows/ci_cd_aws.yml).

Paths, narration (SAY lines straight from script.md), the semantic colours of BRIEF.md, the running
example (placeholders only), the three trackers (A, B, C), loaders for the real captures in
assets/terminal/laptop (laptop and toolbox files), source panels from assets/source, terminal helpers,
tags, chips, small glyphs and the video's set pieces V1-V8. Generic helpers come from L21's
common.py (tested there); the toolbox loader, the recap row, the console drawing and every set piece
are new. build/common_test.py plays every helper and piece once.

    from manim import *          # first
    from common import *         # second (common's names win), then:
    SAY = NARRATION["S07"]; assert len(SAY) == SAY_COUNT["S07"]   # one voiceover block per SAY

Notes for scene authors
=======================
Rules. Every text here is >= 20 pt: never .scale() a group that holds text below 1.0 (pieces take
size / width parameters instead; text-free glyphs exist for small copies: badge_glyph, key_glyph,
cube_glyph, disk_glyph, runner_icon, laptop_icon, broom_glyph, hand_glyph). Never set width / height
/ color / depth on a VGroup subclass (Manim properties): these classes use box_w, card_w, ... Methods
marked PLAYS take the scene first, play their own animation and keep any new mobject inside the piece
(a later FadeOut(piece) takes it too). Methods marked ANIM return an animation you play. Place a
piece (shift / move_to) BEFORE its first PLAYS call or between calls: PLAYS methods build new parts
at the piece's current position. To take one part away, piece.drop(scene, part) (fades it and
removes it from the piece; never FadeOut a member of a piece directly: it snaps back when the piece
is next animated). Nothing here prints a key, an id or an address: out() refuses the placeholder
key strings, 'AKIA', PEM text and the capture-only AWS_CA_BUNDLE line.

Frame budget. Safe frame x in [-6.6, 6.6], y in [-3.6, 3.6]. Tracker top-left (left -6.5, top 3.5,
lowest point TRACK_BOTTOM 2.9); lref("19") top right (y 3.25 .. 3.6). Pictures stay below PIC_TOP
2.8. Terminals: term() is 12.6 wide, 22 pt = 65 characters a row, bottom edge at BOTTOM -3.5; a
3-row strip's top is STRIP_TOP (-1.44), so a picture over a 3-row strip lives in y in [-1.3, 2.8].

Data
    NARRATION["S01"] .. ["S16"]  SAY_COUNT  TITLES[cls]  SPEC (video.yaml)
    Prompts P_HOME 'student@laptop:~$', P_REPO 'student@laptop:~/cheese-app-aws$', P_LAPTOP
    'student@laptop:~/cheese-app-aws/src/deployment$'; toolbox prompts come from the capture
    (toolbox_prompt("40") -> 'root@1a21d2c749ab:/app#'). Titles T_LAPTOP 'laptop', T_TOOLBOX
    'cheese-app-deployment'. Names: REPO, COURSE_REPO, COURSE_URL, YOUR_REPO_URL, PIN '5950118',
    ACCOUNT 'YOUR_ACCOUNT_ID', REGION 'us-east-1', REGISTRY, EXTERNAL_IP '<EXTERNAL_IP>', HOST_PH
    'EXTERNAL_IP', KEY_ID '<aws-access-key-id>', SECRET_KEY '<aws-secret-access-key>', CSV_ROW,
    CSV_NAME, PEM_README 'cheese-app-ac215-key-pair.pem', PEM_CODE 'ac215_2024.pem', KEYPAIR_README,
    KEYPAIR_CODE 'ac215_2024', POLICY 'CheeseAppECRPolicy', IAM_USER 'deployment-ac215-user',
    MANAGED_POLICIES (3), IMAGES / ECR_REPOS (3 names), CONTAINERS {key: (name, port)},
    TAG_FMT 'YYYYmmddHHMMSS', TAG_CI '20261108011909' (laptop/51), TAG_COMMITTED '20241121211313',
    NEXTAUTH '<nextauth-secret>', SECRETS (the four repository secret names), MASKED '***',
    KEYWORD '/run-deploy-app', JOB_KEY '/run-', BACKSLASH '\\run-deploy-app', SLIDES_KEYWORD
    '/deploy-app', SG_PORTS (22, 80, 443), PLAYBOOKS (five files), VERSIONS{tool: 'x.y.z'}
    (all 'at the time of recording'), RIBBONS (S12's four messages), INSTANCE 'cheese-app-demo'.

Trackers (script.md conventions; placed top-left)
    tracker_a(step=None, extra=False) 'README › Before you deploy' 6 steps;
    tracker_b(step=None, extra=False) 'README › Deployment Steps' 15 steps;
    tracker_c(step=None) 'workflow › ci_cd_aws.yml' 7 steps, caption always ' · not in the README'.
    extra: True -> ' · extra'; a string -> ' · <string>'. track(tr, k, extra) ANIM (use it, never
    tr.goto) · swap_tracker(scene, old, new) PLAYS · lref("19") / lref("21–37") the GREY 'Lecture 23 ·
    slide(s) …' tag (top right; only while that slide's picture is on screen).

Captures (assets/terminal/laptop/NN-*.txt; capture-only/ refused)
    c = capture("40") / capture("laptop/40"): .cmd_lines .cmd .k .lines .exit .raw .path .nn ·
        c.at(*spec) output by FILE line numbers (ints, (a, b), '…'), refuses the command lines ·
        c.line(n) · c.pick(*ranges) L1-style (body index = file line - k). 51-53 are the workflow's
        own run: scripts: c.typed is False and type_capture() refuses them (put_heading() instead).
    Toolbox files (28, 31-38, 40, 42, 44, 46-48): x = toolbox_capture("40") ->
        x.prompt 'root@…:/app#' (line 35) · x.cmds [(file line, typed command)] (32 has six) · x.cmd
        (the first) · x.at(*spec, crypto=False, warnings=False) like Capture.at but refuses the build
        log (lines 1-34) and prompt lines, drops BY TEXT the CryptographyDeprecationWarning pair
        (crypto=True keeps it), the community.general block (warnings=True keeps it) and the
        capture-only AWS_CA_BUNDLE line; every line goes through ansible_line() (the '****' after
        PLAY / TASK headings dropped, RECAP columns squeezed: still ~90 characters, so cut() it or
        show a PlayRecap) · x.msg(n) the 'fatal: [host]: FAILED! =>' / 'UNREACHABLE! =>' head of
        FILE line n plus its stderr_lines (or msg) text, one item per line (out(..., wrap=True)) ·
        x.recap() -> (host, {ok, changed, unreachable, failed, skipped, ...}).
        tbx_lines(name, *spec, **kw) = toolbox_capture(name).at(...) · toolbox_prompt(name).
        e.g. 42 line 45 (the AuthFailure exception): cut(x.at(45)[0], "access credentials").
    task_names(playbook) the task list of laptop/37 for one playbook (docker-images 11, create 9,
        provision 38, setup-containers 25, setup-webserver 4).
    crop(s) 40/64-hex ids -> 7 characters + '…' · cut(s, after) · from_phrase(s, phrase) ·
    soft(lines, n) · strip_ansi(s) · squeeze_spaces(s) · guard(s) (raises on secrets).

Sources (assets/source/ = the repo at 5950118, repo-relative paths; masked copies)
    code(path, a, b=None, font_size=22, focus=, trim=None) CODE() panel, <= 12 lines, must fit
        12.6 (22 pt ~65 characters, 20 pt ~72; a wider one raises and names the line). Tabs are
        expanded to 4 (nginx.conf). trim=N cuts lines longer than N to N-1 + '…' (inventory.yml:7 is
        118 characters: code("src/deployment/inventory.yml", 1, 11, font_size=20, trim=70); nginx.conf
        36: trim=60). '<value not copied: see ASSETS.md>' shows as '<nextauth-secret>'. .code .header;
        highlight with line_bar(p.code, k, colour) or code_span(p.code, k, "x"), k = file line - a.
    code_strip(path, line) a one-line panel · excerpt(path, a, b) · source_text(path) · readme(n) ·
    readme_lines(a, b) · readme_panel(a, b, lines=None, card_w=None, colors=None) the GREY README
    card ('README.md · lines a–b'); .frame .head .body .rows{n: row}.
    console_drawing(title, fields, where='aws'|'github', form_w=None) the schematic console page:
        BLUE frame, a top label 'AWS · us-east-1' or 'GitHub', the GREY breadcrumb `title`, rows,
        and its 'illustration' tag on the top edge. fields: ('Name', 'value') a field, ('button',
        'Download .csv file'), ('check', 'AmazonS3FullAccess', True), ('chip', 'text', colour), a
        plain string = a GREY note. Width = its content + 0.8 (one field ~6.3 x 2.3; +0.55 per row).
        .frame .where .crumb .rows .tag; .rows[i] has .value (fields) / .box (buttons) / .text.
    browser(url='http://<EXTERNAL_IP>/', page_w=7.0, page_h=4.2) a schematic browser with its
        'illustration' tag (.frame .address .content .tag).

Terminals (house: 12.6 wide, 22 pt = 65 characters a row)
    term(prompt=P_LAPTOP, rows=10, title='laptop') / laptop_term(rows, prompt) /
    toolbox_term(name_or_prompt, rows) (title 'cheese-app-deployment') · resize(scene, t, rows)
    PLAYS · room · bare_prompt · type_cmd(scene, t, cmd) · type_capture(scene, t, cap) (a toolbox
    capture types x.cmd at the toolbox prompt) · out(scene, t, lines, wrap=) (refuses rows that do
    not fit unless wrap; refuses secrets) · cd_prompt(scene, t, prompt) · set_toolbox(scene, t,
    name) PLAYS (prompt = the capture's 'root@…:/app#', title 'cheese-app-deployment') ·
    retitle(scene, t, title) PLAYS (back: t.set_prompt(P_LAPTOP); retitle(self, t, T_LAPTOP)) ·
    put_heading(scene, t, text) PLAYS a GREY 20 pt heading row ('ci_cd_aws.yml · lines 47–50 · run
    by hand') · beside / pin / unpin / on_bar / under_term for tags at a row · row_tag, turn_row,
    extra_row, time_row, standin_row (tags sized for a 22 pt row). At P_LAPTOP a typed line is
    long (the prompt is 48 characters): put its tag with on_bar(t, extra_row()), not beside().

Tags and chips (GREY unless said; 20-22 pt)
    your_turn() YELLOW · extra_tag(kind) · illustration_tag(s) · recording_tag() 'at the time of
    recording' · erratum_tag(s) · standin_tag() 'extra · stand-in on the laptop' · byhand_tag()
    "the workflow's own commands, run by hand" · shown_tag() 'written out, not run' ·
    not_tested_tag() · expected_tag(source) · cost_tag(text) GOLD (raises on '$', 'cents', 'free
    tier') · grey_chip · dashed_chip (GCP words, the future, skipped) · tool_chip PURPLE · ok_chip
    GREEN · err_chip RED · route_chip PINK · image_chip TEAL · shared_chip ORANGE · cloud_chip BLUE ·
    label_box(lines, colour, dashed=False, box_w=None, mono_font=False, pad=0.22) a box holding 1-3
    centred lines ('one EC2 server\nDocker containers') · question_card(text) YELLOW ·
    ponder(scene, q, seconds=8) PLAYS (pause_and_ponder; FadeOut the card at the next block) ·
    flash_tag(scene, tg) · each / under / hl_bar / ring / strike.

Glyphs (text-free unless named; sizes in scene units)
    badge_glyph(h=0.42) the WHITE access-key badge · key_glyph(h=0.42) the WHITE key-pair key ·
    cube_glyph(side) TEAL image · disk_glyph(h, colour) GREEN disk · runner_icon(h, lit=) BLUE
    machine · laptop_icon(w) · broom_glyph(h, colour) · hand_glyph(h) GREY hand pointing down ·
    release_button(size) RED pill 'RELEASE' (.frame .text) · auto_ring(r) GREEN ring with an arrow
    + 'auto' (.ring .text) · ribbon(text, colour) a commit-message ribbon (.frame .text .msg) ·
    tag_card(text, colour) the GREEN timestamp card (.frame .text .hole) · crate(name, box_w, box_h,
    sub=None) a TEAL container box, mono name (+ GREY sub-line) (.frame .text .sub) · aws_box(text=
    'AWS · us-east-1', box_w, box_h) BLUE (.frame .text .body) · github_box(text='GitHub') BLUE ·
    vault_glyph(h) BLUE · door_glyph(text, colour) · key_file(h) · spark(colour) · state_mark(state,
    h) · dot(colour) · outline_box(w, h, colour, solid=) · arrow / route(a, b, arc, dashed=) / travel
    / bounce · dashed_copy(group) · CostDial(radius, caption) the GOLD dial (no digits; .run .freeze).
    Animating ONE member of a filled box (Indicate(box.frame) …) re-adds it on top of its text and
    hides the text: animate the whole box, or Circumscribe + Indicate(text).

Small pieces (each a Piece: .drop(scene, part))
    PlayRecap(counts=None|dict|RECAP line, host=None, size=20) V4's counters 'ok=N changed=N
        unreachable=N failed=N skipped=N', centred (~9.9 x 0.5; with host 11.9). Colours: failed /
        unreachable > 0 RED, == 0 GREEN; ok > 0 GREEN; changed > 0 YELLOW; else GREY.
        play_recap(line_or_capture_name) builds one from a real RECAP line (play_recap("40")).
        PLAYS set(scene, name, n). ANIM flash(name). .cells{name} .host .row .counts
    Checklist(title, items, color=S.GREY, tag_text='illustration'|None, dashed=(), card_w=None,
        mono_items=False) the clean-up card (color=COST), S05's 'your edits', S14's commit list.
        PLAYS tick(scene, i, colour) · add_row(scene, text) · strike_row(scene, i).
        .frame .head .rows (.box .text) .tag
    ScoreCards(items=AUTOMATION, card_w=2.4) slide 6's five cards (12.4 x 1.0). PLAYS mark(scene, i,
        ok, note=None) (GREEN check on the corner, or GREY cross + dashed card + dashed note chip) ·
        bracket(scene, i, j, text) (a brace over cards i..j). .cards
    BeadChain(items=CHAIN_ITEMS, size=20, max_w=12.4) S14's '&&' chain: beads joined by '&&',
        wrapped into rows no wider than max_w (CHAIN_ITEMS: two rows, 9.8 x 1.4). ANIM light(i,
        colour) · PLAYS state(scene, i, 'ok'|'fail'|'never'). .beads (.frame .text) .links

Set pieces (V numbers = BRIEF; each class doc gives its exact layout and every method). Sizes are
width x height, measured as built.
    V1 KeywordSieves(teaser=False) full: 11.2 x 4.2 (x -5.1 .. 6.1, y -2.6 .. 1.6; ribbons appear at
        y 2.3); teaser: 8.2 x 3.1 (x -3.9 .. 4.3, y -2.2 .. 0.9; ribbons at (-1.6, 2.0)). PLAYS
        hover(scene, text) (a ribbon waits above sieve 1; returns it) · drop(scene, text_or_ribbon,
        stop, miss='bounce'|'slide') stop 0 = stopped by sieve 1 (job skipped), 1 = passes sieve 1,
        three cubes to ECR, stopped by sieve 2, 2 = passes both, the server's containers are
        recreated · stream(scene, n=33, run_time=3.0) (teaser: n small dots pass, the server lights)
        · images(scene) (three cubes onto the ECR shelf; the GOLD tag is the scene's). ANIM flash(i,
        ok). .sieves[i] (.rim .mesh .text) .job .tiles .ecr .server .containers .entry .ecr_items
    V2 TermMap() slide 19 in series style, built EMPTY at the origin, 12.7 x 5.6 once drawn (y -2.9
        .. 2.7). Do not move or scale it (hidden words keep their built positions; text < 20 pt):
        fade it and draw what follows. PLAYS draw_flow(scene) · draw_chain(scene) · source(scene)
        (1st call: GREY 'slides: Google Cloud · cheese-app-v4', top right y 2.5; 2nd: -> BLUE 'this
        video: AWS · cheese-app-aws · as in L15') · gcp(scene, key) (shows a GCP word not drawn by
        default: 'registry', 'pulumi', 'key', 'keyword', 'ingress') · relabel(scene, key) (GCP word
        -> AWS word, TERM_PAIRS; also 'kubernetes') · fade_ml(scene). .flow{dev github actions cloud
        users} .chain[6] .labels{key} .flow_arrows .chain_arrows .cloud_rows .src_chip
    V3 KeyJourney(places=None) the snake of places SNAKE (8 boxes, 12.2 x 3.0, rows y +1.0 / -1.0);
        places=(keys…) <= 4 keys in one row (PLACES also has 'runner_ssh', 'toolbox_ssh'). PLAYS
        start(scene) (badge + key appear in ~/secrets/) · send(scene, which, src, dst, leave=True,
        arc=0) ('badge' | 'key'; a PINK arrow, the glyph rides it, a copy stays at dst) ·
        counter(scene, text) (GREY caption above the piece) · overlay(scene, 'role'|'oidc') (GREY
        dashed boxes, label below; the badge copies they cover fade). .places{key} .copies{key}
        .arrows .caption .overlays
    V4 AnsibleMachine() inventory tree (left) + two play cards (middle) + a right column 'AWS ·
        us-east-1' / toolbox / server (x 3.8 .. 6.2); 12.7 x 5.2 (x -6.5 .. 6.2, y -2.8 .. 2.4).
        PLAYS fire(scene, card, tile, state='changed') (localhost: PURPLE spark in the toolbox, a
        PINK dot up to AWS; appserver: the dot rides the SSH arrow down into the server) ·
        ssh(scene) (the SSH arrow + chip 'ubuntu + your key' under the server).
        .tree .cards[0..1] .toolbox .aws .server .ssh_arrow .api_arrow
    V4 InventoryTree(host=EXTERNAL_IP, dashed_host=False) GREEN tree all -> appserver -> host
        (2.7 x 3.1). .all .group .leaf .edges. PLAYS set_host(scene, text, dashed).
    V4 PlayCard(file, title, hosts, tiles, cols=2, tile_w=None, card_w=None, mono_tiles=False) a
        playbook card: GREY file name, the play title, a hosts chip (localhost TEAL, appserver
        BLUE), task tiles (str or (name, sub) with a GREY mono sub-line such as a when: line);
        tile_w=None (all as wide as the widest), a number, or 'fit' (each its own width; one row
        when cols >= len(tiles)). 11 task_names in 2 cols: ~7.4 x 3.4. ANIM set_state(i, state)
        ('changed' YELLOW, 'ok' GREEN, 'failed' / 'unreachable' RED, 'skipped' GREY dashed, 'idle').
        PLAYS skip(scene, i) · light_all(scene, state, lag) · chip(scene, i, text, colour,
        side=RIGHT) (right of the card at tile i's height: leave room; side=DOWN/UP: by the tile).
        .tiles (.frame .text .sub .state) .hosts_chip .head .title .frame
    V5 SiblingContainers(host='laptop'|'runner') 9.0 x 5.2: the host frame, its folders (left,
        each at its mount point's height), the TEAL crate (x -0.2 .. 3.9, top) with its mount points,
        the PINK socket under the crate's left edge down to the 'Docker engine' shelf (y -1.95) that
        holds the toolbox's own image. PLAYS mount(scene, key) · mounts(scene, keys=None) ·
        hover_spark(scene) · build(scene, spark=None) (spark down the socket, a TEAL cube lands on
        the shelf + GREEN chip 'sibling') · prune_ghost(scene) (RED 'docker system prune -a' down the
        socket, a broom sweeps a ghost, undone) · dash(scene, keys) (mounts + folders turn GREY) ·
        badge_in(scene) (badge glyph from the secrets folder into the crate). Keys: laptop 'socket'
        'app' 'secrets' 'api' 'frontend' 'vectordb'; runner 'socket' 'deployment' 'ssh' (+ the app
        folders, GREY, never mounted). .frame .title .folders{key} .mpoints{key} (mount points)
        .lines{key} .socket .crate .shelf .images
    V6 TimestampTrail(mode='build'|'deploy', tag_text=TAG_FMT) build: 12.9 x 4.9 (x -6.4 .. 6.5, y
        -2.4 .. 2.5: stamp chip, card, three image chips, the ECR box with three named shelves,
        .docker-tag file, the registry line). PLAYS stamp(scene) · clip(scene, i) · push(scene, i) ·
        push_all(scene) · save(scene, text=None) (the committed tag struck GREY, the card's copy
        GREEN under it). deploy (tag_text=TAG_CI): 12.2 x 4.7 (y -2.6 .. 2.1; stations on top:
        runner 'date', DOCKER_TAG, toolbox, ansible-playbook; ECR and the server below; the card
        rises to ~2.7). PLAYS stamp(scene) · ride(scene) · pull(scene) · recreate(scene, i=None,
        gap_chip=True) (old blinks out, a dashed gap + 'short gap', new in with ':new').
        .card .images .ecr .shelves .file .stations{key} .server .containers
    V7 VmLayout() the EC2 server, box 7.0 x 4.4 at x -3.0 .. 4.0, y -2.3 .. 2.1, built EMPTY (frame +
        title); with wall(), '0.0.0.0/0' sits outside at x ~-5.6; meter() puts the GOLD dial right
        at x ~4.8 (10.7 x 4.6 in all). PLAYS wall(scene) · engine(scene) · disk(scene) ·
        network(scene) · container(scene, key, chip=None) key in 'nginx' 'frontend' 'api' 'vectordb'
        'loader' · version(scene, key, text, colour) (chip under the container; a second call swaps
        it) · request(scene, src, dst, path, result, ok) (rides between the two, turns into the
        answer, kept as .answer) · loader_run(scene) · route(scene, path, cut=None, dst='api') (a
        browser request through door 80 to nginx; `cut` falls away RED; kept as .req) · door(scene,
        port, state) 'open' ORANGE 'used' GREEN 'shut' GREY · recreate(scene, key) · meter(scene) ·
        meter_run(scene, turns, secs) (freeze with v.dial.freeze()) · ports_inside(scene) (':3000
        :8000 :9000' painted inside the wall, no hole) · badge_on(scene, target, text, colour=TURN)
        (S16; a tag on a container / 'box' / 'disk' / 'wall', returned NOT kept: FadeOut it
        yourself) · ssh_arrow(start) (a PINK arrow mobject to door 22). .frame .title .doors{port}
        .sg (the wall) .slots{key} .containers{key} .disk_box (.folders{name}) .net .dial
    V8 ReleaseLoop(release=False) slide 7's loop, 12.6 x 3.7 (x -6.2 .. 6.4, y -1.8 .. 1.9; chips
        go down to ~-1.0). PLAYS add_release(scene) (Release slides in between Test and Deploy,
        everything re-lays out) · go_around(scene) · this_repo(scene) · ms5(scene) · chip(scene,
        key, text, colour, dashed=False, level=0) (under the box, level k is 0.48 lower; replaced
        per key). ANIM light(key, colour). .boxes{key} .devs .notify .brackets .commits .chips
    V8 ReleaseToggle() slide 12's conveyor: belt and cards 6.8 x 1.0 (x -4.6 .. 2.2); the button
        sits at x 3.4 (ends(): button 3.1, ring 5.2), the hand 1.0 above it. PLAYS delivery(scene) ·
        deployment(scene) · ends(scene) (both ends side by side, unlabelled) · hover_ribbon(scene,
        text) · into_hand(scene) · label_end(scene, text, at='button'|'ring').
        .belt .cards .button .hand .ring .names

Capture folder names: assets/terminal/laptop (every README command and the extras, on a fresh
Ubuntu 24.04.5 'laptop' with Docker Engine 29.9.3, user student; toolbox files start with the
`bash docker-shell.sh` build log, line 35 = the toolbox prompt + the typed command). laptop/
capture-only/ is plumbing and refused. Sources: assets/source/ (README.md, .github/workflows/
ci_cd_aws.yml, src/...). The workbench build/common_test.py plays every helper and piece.
"""

from __future__ import annotations

import re
import subprocess
from functools import lru_cache
from pathlib import Path

import numpy as np
import yaml
from manim import (DL, DOWN, DR, LEFT, ORIGIN, PI, RIGHT, TAU, UL, UP, UR, AnimationGroup, Arc,  # noqa: F401
                   Arrow, Brace, Circle, Circumscribe, Create, DashedLine, DashedVMobject, Dot, FadeIn,
                   FadeOut, FadeTransform, GrowArrow, Indicate, LaggedStart, Line, MoveAlongPath,
                   Polygon, Rectangle, ReplacementTransform, RoundedRectangle, Square, Succession, Text,
                   Transform, UpdateFromAlphaFunc, ValueTracker, VGroup, VMobject, always_redraw, linear,
                   there_and_back)

from explainer import style as S
from explainer.components import pause_and_ponder, person_icon  # noqa: F401 (re-export)
from explainer.devops import (CAPTION, LABEL, MONO, OUTPUT, PANEL, SMALL, TAG, TERM_BG,  # noqa: F401
                              PROMPT_PATH, ReadmeTracker, Terminal, box, browser_window, cell_width,
                              check_mark, chip, code_panel, code_span, cross_mark, file_glyph,
                              folder_glyph, label, laptop, lecture_ref, line_bar, line_pitch, mono,
                              mono_line, substring, tag)
from explainer.script import load_narration

# ------------------------------------------------------------------ paths and data
HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
ASSETS = PROJECT / "assets"
TERMINAL = ASSETS / "terminal"
LAPTOP_DIR = TERMINAL / "laptop"
SOURCE = ASSETS / "source"

SPEC = yaml.safe_load((PROJECT / "video.yaml").read_text())
TITLES = {s["cls"]: s["title"] for s in SPEC["scenes"]}
_script = PROJECT / "script.md"
NARRATION = load_narration(_script) if _script.exists() else {}
SAY_COUNT = {k: len(v) for k, v in NARRATION.items()}

# ------------------------------------------------------------------ semantic colours (BRIEF.md)
LAPTOP = S.GREY          # the laptop: your terminal, your clone, ~/secrets/ (CSV, .pem), the browser
LOCAL = LAPTOP
CLOUD = S.BLUE           # AWS us-east-1, EC2, EBS, ECR, IAM; GitHub and its runner
AWS = CLOUD
GITHUB = CLOUD
IMAGE = S.TEAL           # the toolbox, the three app images, the five containers, the loader
CONTAINER = IMAGE
SHARED = S.ORANGE        # not yours: the course's committed values, Docker Hub images, 0.0.0.0/0, managed policies
OWN = S.GREEN            # project-owned, pinned: inventory.yml, playbooks, nginx.conf, the tag, failed=0, ✓
PASS = OWN
TOOL = S.PURPLE          # Ansible, the AWS CLI, Docker, GitHub Actions, configure-aws-credentials
ERR = S.RED              # first errors, failed=1, UNREACHABLE!, exit != 0, HTTP 410, the delete that fails
TURN = S.YELLOW          # your turn, the tracker, the loop's current box, the ponder timer
COST = S.GOLD            # instance, disks, public IPv4, ECR storage, Bedrock tokens, Actions minutes
ROUTE = S.PINK           # SSH arrows, the socket line, HTTP routes, lookup('env'), the ribbon, the tag's trail
PAST = S.GREY            # GCP words before they turn AWS, the future (MS5, role, OIDC), skipped: dashed
FUTURE = PAST
SKIP = PAST
INK = S.WHITE
DIMMED = S.GREY
STATE_COLOR = {"ok": PASS, "changed": TURN, "failed": ERR, "unreachable": ERR, "skipped": SKIP,
               "idle": S.GREY, "success": PASS, "failure": ERR, "running": TURN}

# ------------------------------------------------------------------ layout
TRACK_LEFT, TRACK_TOP = -6.5, 3.5
TRACK_BOTTOM = 2.9           # the tracker's lowest point
BOTTOM = -3.5                # a terminal's bottom edge (kept when it grows or shrinks)
PIC_TOP = 2.8                # pictures stay below this (tracker / lecture_ref above)


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


# the instructor's name never appears (series rule): every loader runs through unname()
_NAME_RE = re.compile(r"Pavlos(?:[ _]Protopapas)?|Protopapas", re.IGNORECASE)


def unname(s: str) -> str:
    return _NAME_RE.sub("‹instructor›", s)


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
    return sorted({ch for ch in s if ord(ch) > 0x2000 and ch not in "…‹›·→←↔≈≠×⊘▶☑✓✗"
                   and not _mono_has(ch)})


def disp_len(s: str) -> int:
    return len(s)


# ------------------------------------------------------------------ the running example
USER = "student"
P_HOME = "student@laptop:~$"
P_REPO = "student@laptop:~/cheese-app-aws$"
P_LAPTOP = "student@laptop:~/cheese-app-aws/src/deployment$"
T_LAPTOP = "laptop"
T_TOOLBOX = "cheese-app-deployment"
REPO = "cheese-app-aws"
COURSE_REPO = "dlops-io/cheese-app-aws"
COURSE_URL = "https://github.com/dlops-io/cheese-app-aws.git"
YOUR_REPO_URL = "https://github.com/<your-user>/cheese-app-aws.git"
PIN = "5950118"
ACCOUNT = "YOUR_ACCOUNT_ID"
REGION = "us-east-1"
REGISTRY = f"{ACCOUNT}.dkr.ecr.{REGION}.amazonaws.com"
EXTERNAL_IP = "<EXTERNAL_IP>"
HOST_PH = "EXTERNAL_IP"
KEY_ID = "<aws-access-key-id>"
SECRET_KEY = "<aws-secret-access-key>"
CSV_ROW = f"{KEY_ID},{SECRET_KEY}"
CSV_NAME = "deployment-ac215-user_accessKeys.csv"
KEYPAIR_README = "cheese-app-ac215-key-pair"
KEYPAIR_CODE = "ac215_2024"
PEM_README = KEYPAIR_README + ".pem"
PEM_CODE = KEYPAIR_CODE + ".pem"
POLICY = "CheeseAppECRPolicy"
IAM_USER = "deployment-ac215-user"
MANAGED_POLICIES = ("AmazonS3FullAccess", "AmazonEC2FullAccess", "AmazonBedrockFullAccess")
IMAGES = ("cheese-app-frontend-react", "cheese-app-api-service", "cheese-app-vector-db-cli")
ECR_REPOS = ("cheese-app-vector-db-cli", "cheese-app-api-service", "cheese-app-frontend-react")  # README 81-85 order
SHORT_IMAGES = ("frontend-react", "api-service", "vector-db-cli")
CONTAINERS = {"nginx": ("nginx", ":80 :443"), "frontend": ("frontend", ":3000"),
              "api": ("api-service", ":9000"), "vectordb": ("vector-db", ":8000"),
              "loader": ("loader", "--rm")}
INSTANCE = "cheese-app-demo"
TAG_FMT = "YYYYmmddHHMMSS"
TAG_CI = "20261108011909"            # laptop/51
TAG_COMMITTED = "20241121211313"     # src/deployment/.docker-tag (the author's last deploy)
NEXTAUTH = "<nextauth-secret>"
SECRETS = ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_ACCOUNT_ID", "AWS_SSH_KEY")
MASKED = "***"
KEYWORD = "/run-deploy-app"
JOB_KEY = "/run-"
BACKSLASH = "\\run-deploy-app"
SLIDES_KEYWORD = "/deploy-app"
RIBBONS = (("update readme", 0), ("fix typo /run-tests", 1), (KEYWORD, 2), (BACKSLASH, 0))
SG_PORTS = (22, 80, 443)
PLAYBOOKS = ("deploy-docker-images.yml", "deploy-create-instance.yml", "deploy-provision-instance.yml",
             "deploy-setup-containers.yml", "deploy-setup-webserver.yml")
VERSIONS = {"docker (laptop)": "29.9.3", "aws-cli": "2.39.6", "ansible": "6.7.0",
            "ansible-core": "2.13.13", "python (toolbox)": "3.8.10", "docker cli (toolbox)": "28.1.1",
            "kubectl": "v1.28.15", "nginx:stable": "1.30.6", "chromadb/chroma:latest": "1.0.0",
            "chroma pin": "0.5.18", "ubuntu (laptop)": "24.04.5"}
AUTOMATION = ("data pipeline\njobs", "model training\n& deployment", "frontend\ndeployment",
              "backend\ndeployment", "building &\npushing containers")       # slide 6
CHAIN_ITEMS = ("cd /deployment", "permissions", "ls", "ECR login", "setup-containers", "setup-webserver")

# ------------------------------------------------------------------ trackers (script.md)
SECTIONS = {"A": "Before you deploy", "B": "Deployment Steps", "C": "ci_cd_aws.yml"}
STEPS = {
    "A": ["APIs to enable", "ECR policy", "IAM user", "Access key", "Key pair", "Deployment setup"],
    "B": ["Go to folder", "Edit CSV path", "docker-shell.sh", "ECR repositories", "Build and push",
          "Create instance", "Copy the IP", "Provision", "Key line", "Setup containers", "Server checks",
          "Nginx config", "Setup webserver", "Open the site", "Delete instance"],
    "C": ["Trigger", "Repo secrets", "AWS login", "Build and push", "SSH key", "Deploy step", "Commit, push"],
}
C_SUFFIX = "not in the README"


def place_tracker(tr: ReadmeTracker) -> ReadmeTracker:
    """Pin a tracker to the house corner (left edge -6.5, top 3.5)."""
    tr.shift(np.array([TRACK_LEFT - tr.get_left()[0], TRACK_TOP - tr.get_top()[1], 0]))
    return tr


def _suffix(tr, extra) -> str:
    if getattr(tr, "key", None) == "C":
        return f" · {C_SUFFIX}"
    if not extra:
        return ""
    return " · extra" if extra is True else f" · {extra}"


def _caption(tr: ReadmeTracker, k: int, extra) -> Text:
    if not k:
        return steady("", tr.size, tr.hi_color).next_to(tr.dots, RIGHT, buff=0.25)
    s = f"step {k} of {len(tr.steps)}: {tr.steps[k - 1]}"
    suf = _suffix(tr, extra)
    if suf:
        t = steady(s + suf, tr.size, tr.hi_color, t2c={suf[3:]: S.GREY, "·": S.GREY})
    else:
        t = steady(s, tr.size, tr.hi_color)
    return t.next_to(tr.dots, RIGHT, buff=0.25)


def tracker(key: str, step: int | None = None, extra=False) -> ReadmeTracker:
    """Tracker `key` ('A', 'B', 'C') at `step` (1-based; None = no step lit yet), placed top-left.
    extra: True -> ' · extra' in GREY; a string -> ' · <string>'. 'C' always says ' · not in the
    README' and its head reads 'workflow › ci_cd_aws.yml'."""
    tr = ReadmeTracker(SECTIONS[key], STEPS[key])
    tr.key, tr.extra = key, extra
    if key == "C":
        old = tr.head[0]
        new = mono("workflow", tr.size, S.GREY).move_to(old).align_to(old, LEFT)
        tr.head.remove(old)
        tr.head.submobjects.insert(0, new)
        tr.head.arrange(RIGHT, buff=0.12)
        tr.head.next_to(tr.dots, UP, buff=0.14, aligned_edge=LEFT)
    if step:
        tr.set_step(step)
    tr.remove(tr.caption)
    tr.caption = _caption(tr, step or 0, extra)
    tr.add(tr.caption)
    return place_tracker(tr)


def tracker_a(step=None, extra=False): return tracker("A", step, extra)   # noqa: E704
def tracker_b(step=None, extra=False): return tracker("B", step, extra)   # noqa: E704
def tracker_c(step=None): return tracker("C", step, False)                # noqa: E704


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
    """PLAYS: tracker `old` cross-fades into `new` in place (A -> B in S05, B -> C in S12). Returns `new`."""
    scene.play(FadeOut(old), FadeIn(new), run_time=run_time)
    return new


def lref(slides: str) -> VGroup:
    """The GREY 'Lecture 23 · slides 19' tag, top right (only while that slide's picture or idea
    is on screen). lref("19") reads 'slide 19'. Slide numbers = the PDF pages of SLIDES.md."""
    return lecture_ref(23, slides)


# ------------------------------------------------------------------ captures
_EXIT_RE = re.compile(r"^(.*?)\[exit (-?\d+)\]$")
_RUN_BY_HAND = ("51", "52", "53")   # the workflow's own run: scripts (never typed)
_SECRET_RE = re.compile(r"PLACEHOLDER_NOT_A_REAL|AKIA[0-9A-Z]{8,}|BEGIN [A-Z ]*PRIVATE KEY|AWS_CA_BUNDLE|"
                        r"capture-only")


def guard(s: str) -> str:
    """Refuse a line that would put a key, the placeholder key strings or the capture plumbing on
    screen (returns s unchanged otherwise)."""
    if _SECRET_RE.search(s):
        raise ValueError(f"never on screen: {s[:60]!r}")
    return s


class Capture:
    """One captured command. .cmd_lines (typed rows, line 1 without '$ ') .cmd (joined '\\n') .k
    (file lines of the command) .lines (output body, no [exit N]) .exit .raw (every file line, the
    exit marker removed) .path .nn ('40') .typed (False for 51-53: never typed)"""

    def __init__(self, cmd_lines, lines, exit_code, raw, path, k):
        self.cmd_lines, self.lines, self.exit, self.raw, self.path, self.k = \
            cmd_lines, lines, exit_code, raw, path, k
        self.cmd = "\n".join(cmd_lines)
        self.nn = path.name.split("-")[0]
        self.typed = self.nn not in _RUN_BY_HAND

    def line(self, n: int) -> str:
        """File line n (1-based). Refuses the command lines (typed, never printed)."""
        if not 1 <= n <= len(self.raw):
            raise IndexError(f"{self.path.name} has {len(self.raw)} lines, not {n}")
        if n <= self.k:
            raise ValueError(f"{self.path.name}:{n} is part of the command (lines 1-{self.k}): "
                             "it is typed, never printed")
        return self.raw[n - 1]

    def at(self, *spec) -> list[str]:
        """Lines by FILE line numbers, as script.md writes them: ints, (a, b) inclusive ranges and
        '…' items (a literal '…' line). at(2, (4, 5), '…', 20). Never adds '…' by itself."""
        res: list[str] = []
        for r in spec:
            if isinstance(r, str):
                res.append(r)
                continue
            a, b = (r, r) if isinstance(r, int) else r
            res += [self.line(n) for n in range(a, b + 1)]
        return [guard(crop(s)) if s != "…" else s for s in res]

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
        return [guard(crop(s)) if s != ellipsis else s for s in res]


def _resolve(name: str) -> Path:
    parts = [p for p in name.split("/") if p]
    if "capture-only" in parts:
        raise ValueError("capture-only/ is plumbing: never shown")
    if parts[0] == "laptop":
        parts = parts[1:]
    if len(parts) != 1:
        raise ValueError(f"capture {name!r}: 'NN' or 'laptop/NN'")
    stem = parts[0][:-4] if parts[0].endswith(".txt") else parts[0]
    p = LAPTOP_DIR / f"{stem}.txt"
    if not p.exists():
        hits = sorted(LAPTOP_DIR.glob(f"{stem}-*.txt"))
        if len(hits) != 1:
            raise FileNotFoundError(f"capture {name}: {len(hits)} matches {[h.name for h in hits]} "
                                    "(see ASSETS.md)")
        p = hits[0]
    return p


@lru_cache(maxsize=None)
def _read(p: Path) -> tuple:
    with open(p, encoding="utf-8", newline="") as f:
        text = f.read()
    return tuple(unname(s.rstrip("\r").expandtabs(8)) for s in text.rstrip("\n").split("\n"))


def capture(name: str) -> Capture:
    """capture("40") / capture("laptop/40"). Fails loudly when missing or ambiguous: never show an
    uncaptured output. The command takes line 1 plus every row after a trailing '\\'.
    An '[exit N]' glued to the last output line (laptop/67) is split off."""
    p = _resolve(name)
    raw = list(_read(p))
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
    while k < len(raw) and raw[k - 1].rstrip().endswith("\\"):
        k += 1
    cmd_lines = [raw[0][2:]] + raw[1:k]
    return Capture(cmd_lines, raw[k:], code_, raw, p, k)


# ---- toolbox files (the build log, then 'root@<id>:/app# <cmd>' at line 35)
_PROMPT_RE = re.compile(r"^(root@[0-9a-f]{12}:/app#) ?(.*)$")
_CRYPTO_RE = re.compile(r"CryptographyDeprecationWarning")
_CRYPTO2 = "from cryptography.exceptions import InvalidSignature"
_WARN_RE = re.compile(r"^\[WARNING\]: Collection community\.general|^\[DEPRECATION WARNING\]: community\.general|"
                      r"^will be removed in community\.general|^Deprecation warnings can be disabled")
_RECAP_RE = re.compile(r"^(\S+)\s+:\s+(.*)$")


class ToolboxCapture(Capture):
    """A toolbox capture (see toolbox_capture). .prompt .cmds [(file line, cmd)] .cmd (first
    command) .start (file line of the first prompt). at(*spec, crypto=False, warnings=False) ·
    msg(n) · recap()."""

    def __init__(self, cap: Capture):
        super().__init__(cap.cmd_lines, cap.lines, cap.exit, cap.raw, cap.path, cap.k)
        self.cmds = []
        for n, s in enumerate(self.raw, start=1):
            m = _PROMPT_RE.match(s)
            if m:
                self.cmds.append((n, m.group(2)))
                if len(self.cmds) == 1:
                    self.prompt, self.start = m.group(1), n
        if not self.cmds:
            raise ValueError(f"{self.path.name}: no toolbox prompt (not a toolbox capture)")
        self.cmds = [(n, c) for n, c in self.cmds if c != "exit"] or self.cmds
        self.cmd = self.cmds[0][1]

    def _drop(self, n: int, crypto: bool, warnings: bool) -> bool:
        s = self.raw[n - 1]
        if "AWS_CA_BUNDLE" in s:
            return True
        if not crypto and (_CRYPTO_RE.search(s) or (s.strip() == _CRYPTO2 and n > 1
                                                    and _CRYPTO_RE.search(self.raw[n - 2]))):
            return True
        if not warnings and _WARN_RE.search(s):
            return True
        return _PROMPT_RE.match(s) is not None and s.endswith("# exit")

    def line(self, n: int) -> str:
        if n < self.start:
            raise ValueError(f"{self.path.name}:{n} is the build log (lines 1-{self.start - 1}): "
                             "after S05 it is never printed")
        if _PROMPT_RE.match(self.raw[n - 1]):
            raise ValueError(f"{self.path.name}:{n} is a prompt line: type it (type_cmd), never print it")
        return self.raw[n - 1]

    def at(self, *spec, crypto: bool = False, warnings: bool = False) -> list[str]:
        """Lines by FILE line numbers (ints, (a, b), '…'). Drops, by text: the cryptography pair
        (unless crypto=True), the community.general block (unless warnings=True), AWS_CA_BUNDLE."""
        res: list[str] = []
        for r in spec:
            if isinstance(r, str):
                res.append(r)
                continue
            a, b = (r, r) if isinstance(r, int) else r
            for n in range(a, b + 1):
                if self._drop(n, crypto, warnings):
                    continue
                res.append(self.line(n))
        return [guard(crop(ansible_line(s))) if s != "…" else s for s in res]

    def msg(self, n: int) -> list[str]:
        """FILE line n is a 'fatal: [host]: FAILED! => {json}' or 'UNREACHABLE! => {json}' line:
        returns [head, text lines…] where the text is its stderr_lines (non-empty ones) or its msg
        (split at newlines, the first paragraph only). Request ids and headers never come along."""
        import json
        s = self.line(n)
        i = s.index("=> ") + 3
        head, data = s[:i].rstrip(), json.loads(s[i:])
        lines = [x for x in data.get("stderr_lines", []) if x.strip()]
        if not lines:
            lines = [x for x in str(data.get("msg", "")).split("\n\n")[0].split("\n") if x.strip()]
        return [guard(head)] + [guard(crop(x)) for x in lines]

    def recap(self) -> tuple:
        """(host, {name: int}) from the line after 'PLAY RECAP'."""
        for n, s in enumerate(self.raw):
            if s.startswith("PLAY RECAP"):
                return parse_recap(self.raw[n + 1])
        raise ValueError(f"{self.path.name}: no PLAY RECAP")


def toolbox_capture(name: str) -> ToolboxCapture:
    """A toolbox capture (28, 31-38, 40, 42, 44, 46-48): .prompt .cmds .at() .msg() .recap()."""
    return ToolboxCapture(capture(name))


_STARS_RE = re.compile(r"\s\*{3,}\s*$")


def ansible_line(s: str) -> str:
    """An Ansible output line for a 65-cell row: the '****' padding after PLAY / TASK headings is
    dropped, and the PLAY RECAP's padded columns are squeezed to two spaces."""
    s = _STARS_RE.sub("", s.rstrip())
    if _RECAP_RE.match(s.strip()) and "ok=" in s:
        s = re.sub(r"\s{2,}", "  ", s)
    return s


def tbx_lines(name: str, *spec, **kw) -> list[str]:
    """toolbox_capture(name).at(*spec, **kw)."""
    return toolbox_capture(name).at(*spec, **kw)


def toolbox_prompt(name: str = "40") -> str:
    """The toolbox prompt of a capture ('root@1a21d2c749ab:/app#'; the id changes every start)."""
    return toolbox_capture(name).prompt


def parse_recap(line: str) -> tuple:
    """'localhost   : ok=0 changed=0 …' -> ('localhost', {'ok': 0, …})."""
    m = _RECAP_RE.match(line.strip())
    if not m:
        raise ValueError(f"not a PLAY RECAP line: {line!r}")
    counts = {k: int(v) for k, v in re.findall(r"(\w+)=(\d+)", m.group(2))}
    return m.group(1), counts


@lru_cache(maxsize=None)
def _task_lists() -> dict:
    raw = _read(_resolve("37"))
    res, cur = {}, None
    for s in raw:
        m = re.match(r"^playbook: (\S+)$", s)
        if m:
            cur = m.group(1)
            res[cur] = []
            continue
        m = re.match(r"^ {6}(\S.*?)\s+TAGS: \[\]$", s)
        if m and cur:
            res[cur].append(m.group(1))
    return res


def task_names(playbook: str) -> list[str]:
    """The task names of one playbook from laptop/37 (`--list-tasks`, in order)."""
    return list(_task_lists()[playbook])


# ---- line transforms (script.md conventions)
_HEX_RE = re.compile(r"\b([0-9a-f]{7})(?:[0-9a-f]{57}|[0-9a-f]{33})\b")
_ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")


def crop(s: str) -> str:
    """Every 40- or 64-character hex id cut to 7 characters + '…'."""
    return _HEX_RE.sub(r"\1…", s)


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
        while len(s) > n:
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
    """Runs of 3+ spaces inside a line become `keep` spaces (padded columns)."""
    return re.sub(r"(?<=\S) {3,}(?=\S)", " " * keep, s)


def md_plain(s: str) -> str:
    """Markdown stripped for a card: '**', backticks and link brackets go, list bullets become '•',
    headings lose their '#'."""
    s = s.rstrip()
    s = s.replace("**", "").replace("`", "")
    s = re.sub(r"!?\[([^\]]+)\]\([^)]+\)", r"\1", s)
    s = re.sub(r"^(\s*)[*-] ", r"\1• ", s)
    s = re.sub(r"^#+\s*", "", s)
    return s


# ------------------------------------------------------------------ sources
_LANG = {".py": "python", ".toml": "toml", ".sh": "bash", ".md": "markdown", ".yaml": "yaml",
         ".yml": "yaml", ".ini": "ini", ".cfg": "ini", ".txt": "text", ".json": "json", ".conf": "nginx",
         ".js": "javascript"}


def _src(path: str) -> Path:
    p = SOURCE / path
    if not p.exists():
        raise FileNotFoundError(f"source {path} is not in assets/source (see ASSETS.md)")
    return p


def source_text(path: str) -> str:
    return unname(_src(path).read_text(encoding="utf-8"))


def excerpt(path: str, first: int, last: int) -> str:
    """Lines first..last (1-based, inclusive) of a source file (masked copies, as committed here)."""
    return "\n".join(source_text(path).split("\n")[first - 1:last]).replace(
        "<value not copied: see ASSETS.md>", NEXTAUTH)


def readme(n: int) -> str:
    """README.md line n, stripped (assert cap.cmd == readme(89))."""
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
         font_size: float = 22, shown: str | None = None, max_lines: int = 12, panel_w: float = 12.6,
         trim: int | None = None):
    """CODE(path: first–last): a code_panel quoting the source file, header '<path> · lines a–b'.
    ≤ 12 lines; raises when a line would make the panel wider than panel_w (22 pt ~65 characters,
    20 pt ~72). trim=N cuts every line longer than N characters to N-1 + '…' and drops trailing
    blanks (inventory.yml:7 is 118 characters: code('src/deployment/inventory.yml', 1, 11,
    font_size=20, trim=70)). .code .header; code_span(p.code, k, "x"), line_bar(p.code, k, colour),
    k = file line - first."""
    last = first if last is None else last
    if last - first + 1 > max_lines:
        raise ValueError(f"CODE {path}: {last - first + 1} lines; never more than {max_lines} on screen")
    name = Path(path).name
    if language is None:
        language = "docker" if name.startswith("Dockerfile") else _LANG.get(Path(name).suffix, "text")
        if name.startswith(".env"):
            language = "bash"
    src = excerpt(path, first, last).expandtabs(4)     # nginx.conf is tab-indented
    if trim:
        src = "\n".join((r.rstrip() if len(r.rstrip()) <= trim else r.rstrip()[:trim - 1] + "…")
                        for r in src.split("\n"))
    guard(src)
    p = code_panel(src, shown or path, first, language, focus=focus, font_size=font_size)
    if p.width > panel_w + 1e-6:
        rows = src.split("\n")
        k = max(range(len(rows)), key=lambda i: len(rows[i]))
        raise ValueError(f"CODE {path}:{first + k} makes the panel {p.width:.2f} wide (> {panel_w}): "
                         "use font_size=20, trim=N or a narrower window")
    return p


def code_strip(path: str, line: int, font_size: float = 22) -> VGroup:
    """A one-line code panel. Swap it with Transform."""
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


def toolbox_term(name_or_prompt: str = "40", rows: int = 10) -> Terminal:
    """A terminal already inside the toolbox: prompt from the capture ('40') or given, title
    'cheese-app-deployment'."""
    p = name_or_prompt if name_or_prompt.startswith("root@") else toolbox_prompt(name_or_prompt)
    return term(p, rows, T_TOOLBOX)


def set_toolbox(scene, t: Terminal, name_or_prompt: str = "40", run_time: float = 0.5) -> None:
    """PLAYS: the terminal enters the toolbox: its prompt becomes the capture's 'root@…:/app#' and
    the title bar reads 'cheese-app-deployment'. (Back out: t.set_prompt(P_LAPTOP) + retitle.)"""
    p = name_or_prompt if name_or_prompt.startswith("root@") else toolbox_prompt(name_or_prompt)
    t.set_prompt(p)
    retitle(scene, t, T_TOOLBOX, run_time)


def retitle(scene, t: Terminal, title: str, run_time: float = 0.5) -> None:
    """PLAYS: the terminal's title bar text changes ('laptop' <-> 'cheese-app-deployment')."""
    if t.title is None:
        return
    new = mono(title, CAPTION, S.GREY).move_to(t.title)
    scene.play(Transform(t.title, new), run_time=run_time)


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
    guard(cmd)
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
    after a trailing '\\' are continuations. Toolbox captures type their first toolbox command
    (x.cmd) at the toolbox prompt (set_toolbox first). 51-53 are refused (put_heading instead).
    Returns the typed lines."""
    cap = capture(cap) if isinstance(cap, str) else cap
    if not cap.typed:
        raise ValueError(f"{cap.path.name}: the workflow's own run: script is never typed; "
                         "use put_heading(scene, t, 'ci_cd_aws.yml · lines a–b · run by hand')")
    if isinstance(cap, ToolboxCapture):
        return [type_cmd(scene, t, cap.cmd, type_time)]
    res, cont = [], False
    for row in cap.cmd_lines:
        res.append(type_cmd(scene, t, row, type_time, prompt=not cont))
        cont = row.rstrip().endswith("\\")
    return res


def out(scene, t: Terminal, lines, wrap: bool = False, run_time: float = 0.6, lag: float = 0.08,
        chunk: int | None = None, color=OUTPUT) -> VGroup:
    """PLAYS: print capture lines (text or (text, colour)) in chunks that fit the box, making room the
    gentle way. wrap=True breaks long lines at their last space that fits (soft()); otherwise a line
    longer than the row is refused (cut it, crop it, or wrap). Secrets and glyphs the mono font
    lacks are refused."""
    items = soft(lines, t.max_chars) if wrap else list(lines)
    for x in items:
        s = x if isinstance(x, str) else x[0]
        guard(s)
        if len(s) > t.max_chars:
            raise ValueError(f"out(): {len(s)} > {t.max_chars} cells: wrap=True or cut it: {s!r}")
        bad = dropped_chars(s)
        if bad:
            raise ValueError(f"out(): {bad!r} would vanish (the mono font has no glyph): {s!r}")
    items = [(x, color) if isinstance(x, str) else x for x in items]
    k = max(1, min(t.rows, chunk or t.rows))
    chunks = [items[i:i + k] for i in range(0, len(items), k)]
    rows = VGroup()
    for ch in chunks:
        room(scene, t, len(ch))
        new = VGroup()
        for s, col in ch:
            ln = mono_line(s, t.size, col)
            t._place(ln, len(t.lines))
            t.lines.add(ln)
            new.add(ln)
        scene.play(LaggedStart(*[FadeIn(m) for m in new], lag_ratio=lag),
                   run_time=run_time / len(chunks) + 0.1)
        rows.add(*new)
    return rows


def put_heading(scene, t: Terminal, text: str, run_time: float = 0.4) -> VGroup:
    """PLAYS: a GREY 20 pt heading row in the terminal (not a command, not output): the run-by-hand
    captures 51-53, 'ci_cd_aws.yml · lines 47–50 · run by hand', and the versions block. Returns it."""
    room(scene, t, 1)
    ln = mono_line(text, 20, S.GREY)
    t._place(ln, len(t.lines))
    t.lines.add(ln)
    scene.play(FadeIn(ln), run_time=run_time)
    return ln


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
    """Put a row-sized tag on terminal t's title bar, at its right end. FadeIn it yourself."""
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


def standin_row() -> VGroup:
    """'extra · stand-in on the laptop' sized for a terminal row."""
    return row_tag("extra · stand-in on the laptop", S.GREY)


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
    """A translucent bar behind glyphs `g` (add it behind)."""
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
    """GREY 'extra' tag; kind 'stand-in on the laptop' -> 'extra · stand-in on the laptop'."""
    return tag("extra" + (f" · {kind}" if kind else ""), S.GREY)


def illustration_tag(s: str = "illustration") -> VGroup:
    """On every console drawing, the server's screen, the browser, every GitHub page, the clean-up card."""
    return tag(s, S.GREY)


def recording_tag(s: str = "at the time of recording") -> VGroup:
    """Beside versions on first show."""
    return tag(s, S.GREY)


def erratum_tag(s: str = "erratum") -> VGroup:
    """On a README / code slip (the narration says 'a small slip', 'a small gap', 'a kind note')."""
    return tag(s, S.GREY)


def standin_tag(s: str = "extra · stand-in on the laptop") -> VGroup:
    """On laptop/62-65 (never presented as the server)."""
    return tag(s, S.GREY)


def byhand_tag(s: str = "the workflow's own commands, run by hand") -> VGroup:
    """On laptop/51-53."""
    return tag(s, S.GREY)


def shown_tag(s: str = "written out, not run") -> VGroup:
    """On command lines we write out but do not run (git remote set-url, the S14 git lines)."""
    return tag(s, S.GREY)


def not_tested_tag(s: str = "not tested") -> VGroup:
    return tag(s, S.GREY)


def expected_tag(source: str | None = None) -> VGroup:
    return tag("expected" + (f" · {source}" if source else ""), S.GREY)


def cost_tag(s: str) -> VGroup:
    """The GOLD money tag (names the meter only). Raises on '$', 'cents', 'free tier': no price."""
    return tag(_no_amount(s), COST)


def grey_chip(s: str, size: float = 20, mono_font: bool = False, color=S.GREY) -> VGroup:
    """A chip for a short note. .box .text"""
    return chip(s, color, size=size, font=MONO if mono_font else None)


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


def dashed_chip(s: str, color=PAST, size: float = 20, mono_font: bool = False) -> VGroup:
    """A dashed chip: the lecture's GCP words, the future (MS5, OIDC), skipped things. .box .text"""
    t = mono(s, size, color) if mono_font else label(s, size, color)
    ob = outline_box(t.width + 0.48, mono("|", size).height + 0.24, color, solid=False)
    t.move_to(ob)
    g = VGroup(ob, t)
    g.box, g.text = ob, t
    return g


def tool_chip(s: str, size: float = 20) -> VGroup:
    """A tool as a PURPLE mono chip (never a logo): ansible-playbook, aws, docker …"""
    return chip(s, TOOL, size=size, font=MONO)


def ok_chip(s: str, size: float = 20, mono_font: bool = False) -> VGroup:
    return chip(s, PASS, size=size, font=MONO if mono_font else None)


def err_chip(s: str, size: float = 20, mono_font: bool = False) -> VGroup:
    return chip(s, ERR, size=size, font=MONO if mono_font else None)


def route_chip(s: str, size: float = 20, mono_font: bool = True) -> VGroup:
    """PINK: routes, requests, the keyword ('/api/newsletters', '/run-deploy-app')."""
    return chip(s, ROUTE, size=size, font=MONO if mono_font else None)


def image_chip(s: str, size: float = 20) -> VGroup:
    """TEAL mono chip: an image or a container."""
    return chip(s, IMAGE, size=size, font=MONO)


def shared_chip(s: str, size: float = 20, mono_font: bool = False) -> VGroup:
    """ORANGE: committed values, Docker Hub images, managed policies, 0.0.0.0/0."""
    return chip(s, SHARED, size=size, font=MONO if mono_font else None)


def cloud_chip(s: str, size: float = 20, mono_font: bool = False) -> VGroup:
    """BLUE: AWS, ECR, the EC2 server, GitHub, a runner."""
    return chip(s, CLOUD, size=size, font=MONO if mono_font else None)


def label_box(lines, color=INK, dashed: bool = False, size: float = 20, box_w: float | None = None,
              mono_font: bool = False, fill_opacity: float = 0.1, pad: float = 0.22) -> VGroup:
    """A rounded box holding 1-3 centred lines ('Data\\nCollector'): text in `color` (dashed boxes
    GREY text). .frame .text"""
    if isinstance(lines, str):
        lines = lines.split("\n")
    f = mono if mono_font else label
    t = VGroup(*[f(s, size, color) for s in lines]).arrange(DOWN, buff=0.08)
    w = box_w or t.width + 2 * pad + 0.1
    h = t.height + 2 * pad
    fr = outline_box(w, h, color, solid=False) if dashed else box(w, h, color, fill_opacity=fill_opacity)
    t.move_to(fr)
    g = VGroup(fr, t)
    g.frame, g.text = fr, t
    return g


def question_card(text: str, size: float = 24, card_w: float | None = None) -> VGroup:
    """A YELLOW-outlined card holding a question ('\\n' separates lines): S01's question, S16's
    test-yourself cards. .frame .text"""
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


def dot(color=ROUTE, r: float = 0.11) -> Dot:
    """A small dot (a message, a request, a commit)."""
    return Dot(radius=r, color=color)


def state_mark(state: str = "idle", h: float = 0.3) -> VGroup:
    """A status mark: 'ok'/'success' GREEN check in a ring, 'failed'/'failure' RED cross,
    'skipped' GREY dashed ring + slash, 'running'/'changed' YELLOW dot, 'idle' GREY ring."""
    col = STATE_COLOR.get(state, S.GREY)
    r = h / 2
    if state == "skipped":
        c = DashedVMobject(Circle(radius=r), num_dashes=10).set_stroke(col, 2.5)
        inner = Line([-r * 0.6, -r * 0.6, 0], [r * 0.6, r * 0.6, 0], color=col, stroke_width=2.5)
    else:
        c = Circle(radius=r, stroke_color=col, stroke_width=2.5).set_fill(col, 0.15 if state != "idle" else 0)
        if state in ("ok", "success"):
            inner = check_mark(h * 0.62, col, stroke=3.5)
        elif state in ("failed", "failure", "unreachable"):
            inner = cross_mark(h * 0.5, col, stroke=3.5)
        elif state in ("running", "changed"):
            inner = Dot(radius=r * 0.45, color=col)
        else:
            inner = VMobject()
    inner.move_to(c)
    g = VGroup(c, inner)
    g.state = state
    return g


def spark(color=TOOL, r: float = 0.28, n: int = 8) -> VGroup:
    """A burst of short rays (a task fires, a build starts)."""
    return VGroup(*[Line(RIGHT * r * 0.45, RIGHT * r, color=color, stroke_width=3)
                    .rotate(k * TAU / n, about_point=ORIGIN) for k in range(n)])


def runner_icon(h: float = 0.5, lit: bool = False, color=CLOUD) -> VGroup:
    """A small BLUE machine (GitHub's runner). lit=True fills it."""
    w = h * 1.3
    b = RoundedRectangle(width=w, height=h, corner_radius=0.06, stroke_color=color if lit else S.GREY,
                         stroke_width=2.5).set_fill(color if lit else S.GREY, 0.45 if lit else 0.08)
    lines = VGroup(*[Line(LEFT * w * 0.3, RIGHT * w * 0.3, stroke_width=2,
                          color=color if lit else S.GREY) for _ in range(2)]).arrange(DOWN, buff=h * 0.22)
    lines.move_to(b)
    return VGroup(b, lines)


def laptop_icon(w: float = 1.0) -> VGroup:
    """A GREY laptop glyph (devops.laptop)."""
    return laptop(w, LAPTOP)


def cube_glyph(side: float = 0.5, color=IMAGE) -> VGroup:
    """A TEAL cube (an image)."""
    d = side * 0.3
    front = Square(side_length=side, stroke_color=color, stroke_width=2.5).set_fill(color, 0.35)
    top = Polygon(front.get_corner(UL), front.get_corner(UL) + np.array([d, d, 0]),
                  front.get_corner(UR) + np.array([d, d, 0]), front.get_corner(UR),
                  stroke_color=color, stroke_width=2.5).set_fill(color, 0.55)
    sidep = Polygon(front.get_corner(UR), front.get_corner(UR) + np.array([d, d, 0]),
                    front.get_corner(DR) + np.array([d, d, 0]), front.get_corner(DR),
                    stroke_color=color, stroke_width=2.5).set_fill(color, 0.2)
    return VGroup(front, top, sidep).move_to(ORIGIN)


def badge_glyph(h: float = 0.42, color=INK) -> VGroup:
    """The access key: a WHITE ID badge (photo disc + two lines). Text-free."""
    w = h * 1.45
    fr = RoundedRectangle(width=w, height=h, corner_radius=h * 0.14, stroke_color=color,
                          stroke_width=2.5).set_fill(S.BG, 1)
    photo = Circle(radius=h * 0.2, stroke_color=color, stroke_width=2).set_fill(color, 0.5)
    photo.move_to(fr.get_left() + RIGHT * h * 0.36)
    ls = VGroup(*[Line(LEFT * w * 0.2, RIGHT * w * 0.2, color=color, stroke_width=2.5) for _ in range(2)])
    ls.arrange(DOWN, buff=h * 0.18).move_to(fr.get_center() + RIGHT * w * 0.16)
    clip = RoundedRectangle(width=h * 0.36, height=h * 0.14, corner_radius=0.03, stroke_width=0) \
        .set_fill(color, 1).move_to(fr.get_top())
    return VGroup(fr, photo, ls, clip)


def key_glyph(h: float = 0.42, color=INK) -> VGroup:
    """The key pair: a WHITE key (bow, shaft, two teeth). Text-free."""
    bow = Circle(radius=h * 0.3, stroke_color=color, stroke_width=3).set_fill(S.BG, 1)
    shaft = Line(ORIGIN, RIGHT * h * 1.1, color=color, stroke_width=3.5).next_to(bow, RIGHT, buff=0)
    t1 = Line(ORIGIN, DOWN * h * 0.24, color=color, stroke_width=3.5).move_to(
        shaft.get_end() + LEFT * h * 0.08 + DOWN * h * 0.12)
    t2 = t1.copy().shift(LEFT * h * 0.26)
    return VGroup(bow, shaft, t1, t2)


def disk_glyph(h: float = 0.5, color=OWN) -> VGroup:
    """A disk (an EBS volume): a short cylinder. Text-free."""
    w = h * 1.2
    from manim import Ellipse
    top = Ellipse(width=w, height=h * 0.32, stroke_color=color, stroke_width=2.5).set_fill(color, 0.35)
    body = Rectangle(width=w, height=h * 0.62, stroke_width=0).set_fill(color, 0.18)
    body.next_to(top.get_center(), DOWN, buff=0)
    sides = VGroup(Line(body.get_corner(UL), body.get_corner(DL), color=color, stroke_width=2.5),
                   Line(body.get_corner(UR), body.get_corner(DR), color=color, stroke_width=2.5))
    bot = Arc(radius=1, start_angle=PI, angle=PI, color=color, stroke_width=2.5).stretch_to_fit_width(w) \
        .stretch_to_fit_height(h * 0.16).move_to(body.get_bottom() + DOWN * h * 0.08)
    g = VGroup(body, sides, bot, top)
    return g.move_to(ORIGIN)


def broom_glyph(h: float = 0.8, color=ERR) -> VGroup:
    """A broom (prune -a sweeps; S16's teardown)."""
    stick = Line(UP * h * 0.5, DOWN * h * 0.1, color=color, stroke_width=4)
    head = Polygon([-h * 0.22, -h * 0.1, 0], [h * 0.22, -h * 0.1, 0], [h * 0.32, -h * 0.5, 0],
                   [-h * 0.32, -h * 0.5, 0], stroke_color=color, stroke_width=2.5).set_fill(color, 0.35)
    bristles = VGroup(*[Line([x, -h * 0.18, 0], [x * 1.4, -h * 0.48, 0], color=color, stroke_width=1.5)
                        for x in np.linspace(-h * 0.16, h * 0.16, 4)])
    return VGroup(stick, head, bristles).rotate(-0.35)


def hand_glyph(h: float = 0.7, color=S.GREY) -> VGroup:
    """A hand pointing down (a person about to press RELEASE): a sleeve, a palm with three folded
    knuckles, a thumb and a long index finger. Text-free."""
    sleeve = Rectangle(width=h * 0.46, height=h * 0.22, stroke_color=color, stroke_width=2.5).set_fill(color, 0.5)
    palm = RoundedRectangle(width=h * 0.56, height=h * 0.42, corner_radius=h * 0.12, stroke_color=color,
                            stroke_width=2.5).set_fill(color, 0.25)
    palm.next_to(sleeve, DOWN, buff=0)
    knuckles = VGroup(*[Circle(radius=h * 0.07, stroke_color=color, stroke_width=2).set_fill(color, 0.25)
                        for _ in range(3)]).arrange(RIGHT, buff=h * 0.01)
    knuckles.next_to(palm, DOWN, buff=-h * 0.07).align_to(palm, RIGHT).shift(LEFT * h * 0.03)
    finger = RoundedRectangle(width=h * 0.14, height=h * 0.48, corner_radius=h * 0.06, stroke_color=color,
                              stroke_width=2.5).set_fill(color, 0.25)
    finger.next_to(palm, DOWN, buff=-h * 0.1).align_to(palm, LEFT).shift(RIGHT * h * 0.04)
    thumb = RoundedRectangle(width=h * 0.12, height=h * 0.3, corner_radius=h * 0.05, stroke_color=color,
                             stroke_width=2.5).set_fill(color, 0.25).rotate(0.5)
    thumb.next_to(palm, LEFT, buff=-h * 0.06).shift(DOWN * h * 0.05)
    return VGroup(sleeve, thumb, palm, knuckles, finger)


def release_button(size: float = 22, color=ERR) -> VGroup:
    """The RED 'RELEASE' pill (slide 12: continuous delivery). .frame .text"""
    t = label("RELEASE", size, INK)
    fr = RoundedRectangle(width=t.width + 0.6, height=t.height + 0.42, corner_radius=(t.height + 0.42) / 2,
                          stroke_color=color, stroke_width=3).set_fill(color, 0.55)
    t.move_to(fr)
    g = VGroup(fr, t)
    g.frame, g.text = fr, t
    return g


def auto_ring(r: float = 0.45, color=PASS, size: float = 20) -> VGroup:
    """A ring with an arrow and 'auto' inside (slide 12: continuous deployment). .ring .text"""
    a = Arc(radius=r, start_angle=PI / 2, angle=-TAU * 0.85, color=color, stroke_width=4)
    a.add_tip(tip_length=0.16, tip_width=0.16)
    t = label("auto", size, color)
    g = VGroup(a, t)
    g.ring, g.text = a, t
    return g


def ribbon(text: str, color=ROUTE, size: float = 20) -> VGroup:
    """A commit-message ribbon: mono text on a banner with notched ends. .frame .text"""
    t = mono(text, size, INK)
    w, h, n = t.width + 0.6, t.height + 0.3, 0.16
    pts = [[-w / 2, h / 2, 0], [w / 2, h / 2, 0], [w / 2 - n, 0, 0], [w / 2, -h / 2, 0],
           [-w / 2, -h / 2, 0], [-w / 2 + n, 0, 0]]
    fr = Polygon(*pts, stroke_color=color, stroke_width=2.5).set_fill(color, 0.22)
    t.move_to(fr)
    g = VGroup(fr, t)
    g.frame, g.text, g.msg = fr, t, text
    return g


def tag_card(text: str = TAG_FMT, color=OWN, size: float = 20) -> VGroup:
    """The GREEN timestamp tag card: a luggage tag with a hole and the tag text. .frame .text .hole"""
    t = mono(text, size, INK)
    w, h = t.width + 0.75, t.height + 0.3
    fr = Polygon([-w / 2 + 0.22, h / 2, 0], [w / 2, h / 2, 0], [w / 2, -h / 2, 0], [-w / 2 + 0.22, -h / 2, 0],
                 [-w / 2, 0, 0], stroke_color=color, stroke_width=2.5).set_fill(color, 0.22)
    hole = Circle(radius=0.06, stroke_color=color, stroke_width=2).move_to([-w / 2 + 0.2, 0, 0])
    t.move_to(fr).shift(RIGHT * 0.12)
    g = VGroup(fr, hole, t)
    g.frame, g.text, g.hole = fr, t, hole
    return g


def crate(name: str = T_TOOLBOX, box_w: float | None = None, box_h: float = 0.8, size: float = 20,
          color=IMAGE, sub: str | None = None) -> VGroup:
    """A TEAL container box with its mono name (and an optional GREY sub-line). .frame .text .sub"""
    t = mono(name, size, color)
    st = mono(sub, size, S.GREY) if sub else None
    txt = VGroup(t, st).arrange(DOWN, buff=0.08) if st is not None else VGroup(t)
    w = box_w or txt.width + 0.5
    h = max(box_h, txt.height + 0.3)
    fr = box(w, h, color, fill_opacity=0.14)
    txt.move_to(fr)
    g = VGroup(fr, txt)
    g.frame, g.text, g.sub = fr, t, st
    return g


def aws_box(text: str = "AWS · us-east-1", box_w: float = 2.6, box_h: float = 1.2, size: float = 20,
            color=CLOUD) -> VGroup:
    """AWS as a BLUE rounded box with its name at the top (never a logo). .frame .text .body (centre
    point area below the label)"""
    fr = box(box_w, box_h, color, fill_opacity=0.1, radius=0.18)
    t = label(text, size, color).move_to(fr.get_top() + DOWN * 0.3)
    body = Rectangle(width=box_w - 0.3, height=max(0.1, box_h - 0.7), stroke_width=0, fill_opacity=0)
    body.move_to(fr.get_bottom() + UP * (box_h - 0.55) / 2)
    g = VGroup(fr, t, body)
    g.frame, g.text, g.body = fr, t, body
    return g


def github_box(text: str = "GitHub", box_w: float = 2.2, box_h: float = 1.0, size: float = 22) -> VGroup:
    """GitHub as a BLUE rounded box with its name (never a logo). .frame .text"""
    fr = box(box_w, box_h, CLOUD, fill_opacity=0.12, radius=0.2)
    t = label(text, size, CLOUD).move_to(fr)
    g = VGroup(fr, t)
    g.frame, g.text = fr, t
    return g


def vault_glyph(h: float = 1.0, color=CLOUD) -> VGroup:
    """A BLUE vault (repository secrets)."""
    b = RoundedRectangle(width=h * 1.1, height=h, corner_radius=0.1, stroke_color=color,
                         stroke_width=3).set_fill(color, 0.12)
    dial = Circle(radius=h * 0.22, stroke_color=color, stroke_width=3)
    spokes = VGroup(*[Line(ORIGIN, UP * h * 0.2, color=color, stroke_width=2.5).rotate(k * TAU / 4, about_point=ORIGIN)
                      for k in range(4)])
    VGroup(dial, spokes).move_to(b)
    return VGroup(b, dial, spokes)


def door_glyph(text: str = "80", color=SHARED, door_h: float = 0.6, size: float = 20) -> VGroup:
    """A door with a number plate left of it (a port in the security group). .frame .text"""
    fr = RoundedRectangle(width=door_h * 0.55, height=door_h, corner_radius=0.05, stroke_color=color,
                          stroke_width=3).set_fill(color, 0.15)
    knob = Dot(fr.get_right() + LEFT * door_h * 0.12, radius=0.035, color=color)
    t = mono(text, size, color).next_to(fr, LEFT, buff=0.1)
    g = VGroup(fr, knob, t)
    g.frame, g.text = fr, t
    return g


def key_file(h: float = 0.6, color=S.GREY) -> VGroup:
    """A file with a key on it (a private key file; never its content)."""
    f = file_glyph(h, color)
    k = key_glyph(h * 0.32, color).move_to(f).shift(DOWN * h * 0.08)
    return VGroup(f, k)


def dashed_copy(group, color=S.GREY, stroke: float = 3, n: int = 5) -> VGroup:
    """A dashed copy of every stroked piece of `group` (a skipped tile, a ghost)."""
    return VGroup(*[DashedVMobject(m.copy(), num_dashes=n).set_stroke(color, stroke)
                    for m in group.family_members_with_points() if not isinstance(m, Text)])


def browser(url: str = "http://<EXTERNAL_IP>/", page_w: float = 7.0, page_h: float = 4.2) -> VGroup:
    """A schematic browser (no logos) with its 'illustration' tag on the top edge.
    .frame .address .content .tag"""
    g = browser_window(url, page_w, page_h)
    tg = illustration_tag()
    tg.move_to(g.frame.get_corner(UR) + np.array([-tg.width / 2 - 0.2, 0, 0]))
    g.add(tg)
    g.tag = tg
    return g


def _field_box(w: float, size: float) -> RoundedRectangle:
    return RoundedRectangle(width=w, height=mono("|", size).height + 0.22, corner_radius=0.06,
                            stroke_color=S.GREY_DARK, stroke_width=1.5).set_fill(TERM_BG, 1)


def console_drawing(title: str, fields=(), where: str = "aws", form_w: float | None = None,
                    size: float = 20) -> VGroup:
    """CONSOLE(title; fields): a schematic console page (never a screenshot, no logo): a BLUE frame,
    a BLUE top label ('AWS · us-east-1' or 'GitHub'), the GREY breadcrumb `title`, then rows:
        ('Name', 'value')               a field: GREY label, input box with the value in mono
        ('button', 'Download .csv file') a BLUE-outlined button
        ('check', 'AmazonS3FullAccess', True)  a checkbox row
        ('chip', 'CheeseAppECRPolicy', OWN)    a chip (policies, repositories)
        'a note'                        a GREY note line
    The 'illustration' tag sits on the top edge. Texts are never scaled: a wide value widens the page.
    .frame .where .crumb .rows (.value / .box / .text) .tag"""
    top = label("AWS · us-east-1" if where == "aws" else "GitHub", size, CLOUD)
    crumb = label(title, size, S.GREY)
    rows = VGroup()
    lw = max([label(f[0], size).width for f in fields if isinstance(f, tuple)
              and f[0] not in ("button", "check", "chip")] + [0]) + 0.3
    for f in fields:
        if isinstance(f, str):
            r = VGroup(label(f, size, S.GREY))
            r.text = r[0]
        elif f[0] == "button":
            t = label(f[1], size, INK)
            b = RoundedRectangle(width=t.width + 0.5, height=t.height + 0.28, corner_radius=0.08,
                                 stroke_color=CLOUD, stroke_width=2.5).set_fill(CLOUD, 0.15)
            t.move_to(b)
            r = VGroup(b, t)
            r.box, r.text = b, t
        elif f[0] == "check":
            on = f[2] if len(f) > 2 else True
            b = Square(side_length=0.28, stroke_color=S.GREY, stroke_width=2.5).set_fill(TERM_BG, 1)
            tick = check_mark(0.24, OWN, stroke=3.5).move_to(b) if on else VMobject()
            t = mono(f[1], size, INK).next_to(b, RIGHT, buff=0.18)
            r = VGroup(b, tick, t)
            r.box, r.tick, r.text = b, tick, t
        elif f[0] == "chip":
            r = chip(f[1], f[2] if len(f) > 2 else S.GREY, size=size, font=MONO)
        else:
            lt = label(f[0], size, S.GREY)
            vt = mono(f[1], size, f[2] if len(f) > 2 else INK)
            fb = _field_box(vt.width + 0.4, size)
            vt.move_to(fb).align_to(fb, LEFT).shift(RIGHT * 0.2)
            lt.next_to(fb, LEFT, buff=0.25)
            lt.shift(LEFT * (lw - lt.width - 0.25))
            r = VGroup(lt, fb, vt)
            r.label, r.field, r.value, r.text = lt, fb, vt, vt
        rows.add(r)
    if len(rows):
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    inner = VGroup(top, crumb, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
    w = max(form_w or 0, inner.width + 0.8)
    fr = RoundedRectangle(width=w, height=inner.height + 0.75, corner_radius=0.16, stroke_color=CLOUD,
                          stroke_width=2.5).set_fill(PANEL, 1)
    inner.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.4 + DOWN * 0.05)
    sep = Line([fr.get_left()[0], crumb.get_bottom()[1] - 0.11, 0],
               [fr.get_right()[0], crumb.get_bottom()[1] - 0.11, 0], color=S.GREY_DARK, stroke_width=2)
    tg = illustration_tag()
    tg.move_to(fr.get_corner(UR) + np.array([-tg.width / 2 - 0.2, 0, 0]))
    g = VGroup(fr, sep, inner, tg)
    g.frame, g.where, g.crumb, g.rows, g.tag = fr, top, crumb, rows, tg
    return g


# ================================================================== pieces
class Piece(VGroup):
    """Base of the set pieces: drop(scene, *parts) fades parts out AND removes them from the piece
    (so they never snap back); keep(scene, *mobs) makes new mobjects members (after a PLAYS)."""

    def drop(self, scene, *parts, run_time: float = 0.4):
        scene.play(*[FadeOut(p) for p in parts], run_time=run_time)
        self._gone(scene, *parts)

    def keep(self, scene, *mobs):
        for m in mobs:
            self.add(m)
        self._reseat(scene)

    def _gone(self, scene, *mobs):
        """Remove mobjects (already faded) from the piece and the scene, silently."""
        for p in mobs:
            for owner in [self, *self.get_family()]:
                if p in owner.submobjects:
                    owner.remove(p)
        gone = {x for p in mobs for x in p.get_family()}
        scene.mobjects = [m for m in scene.mobjects if m not in gone]
        self._reseat(scene)

    def _reseat(self, scene):
        """Put the piece back on the scene as ONE top-level mobject: fragments (members an animation
        introduced or a FadeOut split off, wrappers holding members) are taken off the top level, and
        the piece takes the place of the first one. A top-level group that holds the piece stays."""
        fam = set(self.get_family())
        new, placed = [], False
        for m in scene.mobjects:
            mf = m.get_family()
            if m is self or (self in mf and m is not self):
                if not placed or m is not self:
                    new.append(m)
                placed = True
                continue
            if m in fam or any(x in fam for x in mf):
                if not placed:
                    new.append(self)
                    placed = True
                continue
            new.append(m)
        if not placed:
            new.append(self)
        scene.mobjects = new


# ------------------------------------------------------------------ V4 helpers: recap, cards, tree
RECAP_KEYS = ("ok", "changed", "unreachable", "failed", "skipped")


def _recap_color(k: str, n: int):
    if k in ("failed", "unreachable"):
        return ERR if n else PASS
    if k == "ok":
        return PASS if n else S.GREY
    if k == "changed":
        return TURN if n else S.GREY
    return S.GREY


class PlayRecap(Piece):
    """V4's PLAY RECAP: five counters 'ok=N changed=N unreachable=N failed=N skipped=N', each a mono
    chip in its colour (failed / unreachable: RED when > 0, GREEN at 0; ok > 0 GREEN; changed > 0
    YELLOW; else GREY), optional host name in front. counts: None (all zero), a dict, or a RECAP line.
    PLAYS set(scene, name, n). ANIM flash(name). .cells{name} .host .counts"""

    def __init__(self, counts=None, host: str | None = None, size: float = 20, **kw):
        super().__init__(**kw)
        if isinstance(counts, str):
            host_, counts = parse_recap(counts)
            host = host if host is not None else host_
        self.counts = {k: int((counts or {}).get(k, 0)) for k in RECAP_KEYS}
        self.size = size
        self.cells = {k: self._cell(k, self.counts[k]) for k in RECAP_KEYS}
        row = VGroup(*self.cells.values()).arrange(RIGHT, buff=0.14)
        self.host = None
        if host:
            self.host = mono(f"{host} :", size, S.GREY)
            self.host.next_to(row, LEFT, buff=0.25)
            self.add(self.host)
        self.add(row)
        self.row = row
        self.move_to(ORIGIN)

    def _cell(self, k, n):
        return chip(f"{k}={n}", _recap_color(k, n), size=self.size, font=MONO)

    def set(self, scene, name: str, n: int, run_time: float = 0.5):
        new = self._cell(name, n).move_to(self.cells[name])
        scene.play(Transform(self.cells[name], new), run_time=run_time)
        self.counts[name] = n

    def flash(self, name: str, color=None):
        c = self.cells[name]
        return AnimationGroup(Circumscribe(c, color=color or _recap_color(name, self.counts[name]), buff=0.06),
                              Indicate(c.text, color=color or _recap_color(name, self.counts[name])))


def play_recap(src, host: bool = True, size: float = 20) -> PlayRecap:
    """PlayRecap from a real RECAP line, or from a toolbox capture name ('40')."""
    if isinstance(src, str) and not re.match(r"^\S+\s+:", src.strip()):
        h, counts = toolbox_capture(src).recap()
    else:
        h, counts = parse_recap(src)
    return PlayRecap(counts, h if host else None, size)


class InventoryTree(Piece):
    """V4: the inventory as a GREEN tree, top to bottom: 'all' (a small card 'vars') -> 'appserver'
    -> one host leaf (EXTERNAL_IP by default, mono 20). ~2.6 x 2.6, centred. PLAYS set_host(scene,
    text, dashed=False). .all .group .leaf .edges"""

    def __init__(self, host: str = EXTERNAL_IP, dashed_host: bool = False, size: float = 20, **kw):
        super().__init__(**kw)
        self.size = size
        self.all = label_box(["all", "vars"], OWN, size=size)
        self.all.text[1].set_color(S.GREY)
        self.group = label_box("appserver", OWN, size=size, mono_font=True)
        self.leaf = self._leaf(host, dashed_host)
        col = VGroup(self.all, self.group, self.leaf).arrange(DOWN, buff=0.45)
        self.edges = VGroup(Line(self.all.get_bottom(), self.group.get_top(), color=OWN, stroke_width=3),
                            Line(self.group.get_bottom(), self.leaf.get_top(), color=OWN, stroke_width=3))
        self.add(self.edges, self.all, self.group, self.leaf)
        del col

    def _leaf(self, text, dashed):
        return label_box(text, S.GREY if dashed else OWN, dashed=dashed, size=self.size, mono_font=True)

    def set_host(self, scene, text: str, dashed: bool = False, run_time: float = 0.6):
        new = self._leaf(text, dashed).move_to(self.leaf)
        scene.play(Transform(self.leaf, new), run_time=run_time)


TILE_STYLE = {"idle": (S.GREY, 0.06), "changed": (TURN, 0.2), "ok": (PASS, 0.2), "failed": (ERR, 0.25),
              "unreachable": (ERR, 0.25), "skipped": (SKIP, 0.0)}


class PlayCard(Piece):
    """V4: one playbook card. Top: the file name (GREY mono 20); the play title (label 20); a hosts
    chip ('hosts: localhost' TEAL, 'hosts: appserver' BLUE); then task tiles in `cols` columns.
    tiles: names (str) or (name, sub) pairs: sub is a GREY mono 20 second line (a module, a when:
    line). Card width = tiles + 0.5 (or card_w). ANIM set_state(i, state) ('changed' YELLOW, 'ok'
    GREEN, 'failed' / 'unreachable' RED, 'skipped' GREY dashed, 'idle'). PLAYS skip(scene, i) ·
    chip(scene, i, text, colour) (a chip under tile i) · light_all(scene, state, lag).
    .tiles (.frame .text .sub .state) .hosts_chip .head .title .frame"""

    def __init__(self, file: str, title: str, hosts: str, tiles, cols: int = 2, tile_w: float | None = None,
                 card_w: float | None = None, size: float = 20, mono_tiles: bool = False, **kw):
        super().__init__(**kw)
        self.size = size
        self.head = mono(file, size, S.GREY)
        self.title = label(title, size, INK)
        self.hosts_chip = chip(f"hosts: {hosts}", IMAGE if hosts == "localhost" else CLOUD, size=size, font=MONO)
        items = [(t, None) if isinstance(t, str) else t for t in tiles]
        texts = []
        for name, sub in items:
            tt = mono(name, size, INK) if mono_tiles else label(name, size, INK)
            st = mono(sub, size, S.GREY) if sub else None
            texts.append((tt, st))
        fit = tile_w == "fit"
        tw = None if fit else (tile_w or max(max(a.width, b.width if b is not None else 0) for a, b in texts) + 0.4)
        self.tiles = VGroup()
        for tt, st in texts:
            txt = VGroup(tt, st).arrange(DOWN, buff=0.06, aligned_edge=LEFT) if st is not None else VGroup(tt)
            fr = box(txt.width + 0.4 if fit else tw, txt.height + 0.26, S.GREY, fill_opacity=0.06, radius=0.08)
            txt.move_to(fr)
            if st is not None:
                txt.align_to(fr, LEFT).shift(RIGHT * 0.18)
            t = VGroup(fr, txt)
            t.frame, t.text, t.sub, t.state = fr, tt, st, "idle"
            self.tiles.add(t)
        rows = (len(self.tiles) + cols - 1) // cols
        if fit and rows == 1:
            self.tiles.arrange(RIGHT, buff=0.14)
        else:
            self.tiles.arrange_in_grid(rows=rows, cols=cols, buff=(0.14, 0.12), flow_order="rd" if cols > 1 else "dr")
        inner = VGroup(self.head, self.title, self.hosts_chip, self.tiles).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        w = max(card_w or 0, inner.width + 0.5)
        self.frame = box(w, inner.height + 0.45, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
        inner.move_to(self.frame).align_to(self.frame, LEFT).shift(RIGHT * 0.25)
        self.add(self.frame, inner)

    def _tile_target(self, i, state):
        t = self.tiles[i]
        col, op = TILE_STYLE[state]
        if state == "skipped":
            fr = outline_box(t.frame.width, t.frame.height, SKIP, solid=False).move_to(t.frame)
        else:
            fr = box(t.frame.width, t.frame.height, col, fill_opacity=op, radius=0.08).move_to(t.frame)
        return fr

    def set_state(self, i: int, state: str, run_time: float = 0.4):
        t = self.tiles[i]
        anims = [Transform(t.frame, self._tile_target(i, state))]
        tc = S.GREY if state == "skipped" else (TILE_STYLE[state][0] if state in ("failed", "unreachable") else INK)
        anims.append(t.text.animate.set_color(tc))
        t.state = state
        return AnimationGroup(*anims, run_time=run_time)

    def skip(self, scene, i: int, run_time: float = 0.4):
        scene.play(self.set_state(i, "skipped"), run_time=run_time)

    def light_all(self, scene, state: str = "ok", lag: float = 0.25):
        scene.play(LaggedStart(*[self.set_state(i, state) for i in range(len(self.tiles))], lag_ratio=lag))

    def chip(self, scene, i: int, text: str, color=S.GREY, run_time: float = 0.4, side=RIGHT):
        c = chip(text, color, size=self.size, font=MONO)
        if side is RIGHT or (isinstance(side, np.ndarray) and np.allclose(side, RIGHT)):
            c.next_to(self.frame, RIGHT, buff=0.15).set_y(self.tiles[i].get_y())
        else:
            c.next_to(self.tiles[i], side, buff=0.08)
        scene.play(FadeIn(c, shift=UP * 0.1), run_time=run_time)
        self.keep(scene, c)
        return c


# ------------------------------------------------------------------ small pieces
class Checklist(Piece):
    """A card of rows, each with an empty box that ticks: S05's 'your edits', S14's commit list, S15's
    GOLD clean-up card (color=COST, tag 'illustration'). Checklist(title, items, color=S.GREY,
    tag_text='illustration' or None, dashed=(indices GREY-dashed), card_w=None, mono_items=False).
    PLAYS tick(scene, i, colour=OWN) · add_row(scene, text) · strike_row(scene, i).
    .frame .head .rows (row .box .text) .tag"""

    def __init__(self, title: str, items, color=S.GREY, tag_text: str | None = "illustration",
                 dashed=(), card_w: float | None = None, size: float = 20, mono_items: bool = False, **kw):
        super().__init__(**kw)
        self.size, self.mono_items, self.edge_color = size, mono_items, color
        self.head = label(title, 22, INK)
        self.rows = VGroup(*[self._row(it, i in dashed) for i, it in enumerate(items)])
        self.rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        inner = VGroup(self.head, self.rows).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        self.card_w = card_w or inner.width + 0.7
        self.frame = box(self.card_w, inner.height + 0.7, color, fill=S.GREY_DARKER, fill_opacity=1)
        inner.move_to(self.frame).align_to(self.frame, LEFT).shift(RIGHT * 0.32 + DOWN * 0.06)
        self.inner = inner
        self.add(self.frame, inner)
        self.tag = None
        if tag_text:
            tg = tag(tag_text, S.GREY)
            tg.move_to(self.frame.get_corner(UR) + np.array([-tg.width / 2 - 0.2, 0, 0]))
            self.tag = tg
            self.add(tg)

    def _row(self, it, dash=False):
        bx = Rectangle(width=0.3, height=0.3, stroke_color=S.GREY, stroke_width=2.5)
        if dash:
            bx = DashedVMobject(bx, num_dashes=8).set_stroke(S.GREY, 2.5)
        if isinstance(it, str):
            t = (mono if self.mono_items else label)(it, self.size, S.GREY if dash else INK)
        else:
            t = it
        r = VGroup(bx, t).arrange(RIGHT, buff=0.2)
        r.box, r.text = bx, t
        return r

    def tick(self, scene, i: int, color=OWN, run_time: float = 0.4):
        r = self.rows[i]
        ck = check_mark(0.3, color, stroke=4).move_to(r.box).shift(UP * 0.04 + RIGHT * 0.03)
        scene.play(Create(ck), Indicate(r.text, color=color, scale_factor=1.04), run_time=run_time)
        r.add(ck)
        r.tick = ck
        self._reseat(scene)
        return ck

    def add_row(self, scene, text, run_time: float = 0.5):
        """PLAYS: a new row slides in at the bottom; the card grows."""
        r = self._row(text)
        r.next_to(self.rows, DOWN, buff=0.16).align_to(self.rows, LEFT)
        grow = r.height + 0.16
        w = max(self.card_w, r.get_right()[0] - self.frame.get_left()[0] + 0.4)
        new_fr = box(w, self.frame.height + grow, self.edge_color, fill=S.GREY_DARKER, fill_opacity=1)
        new_fr.align_to(self.frame, UP).align_to(self.frame, LEFT)
        anims = [Transform(self.frame, new_fr), FadeIn(r, shift=UP * 0.1)]
        if self.tag is not None:
            anims.append(self.tag.animate.move_to(new_fr.get_corner(UR) + np.array([-self.tag.width / 2 - 0.2, 0, 0])))
        scene.play(*anims, run_time=run_time)
        self.card_w = w
        self.rows.add(r)
        self._reseat(scene)
        return r

    def strike_row(self, scene, i: int, color=S.GREY, run_time: float = 0.4):
        r = self.rows[i]
        s = strike(r.text, color)
        scene.play(Create(s), r.text.animate.set_opacity(0.55), run_time=run_time)
        r.add(s)
        self._reseat(scene)
        return s


class ScoreCards(Piece):
    """Slide 6's five things to automate, as cards in a row (two-line labels, 20 pt): ~12.4 x 1.1.
    PLAYS mark(scene, i, ok, note=None) (GREEN check top-right, or a GREY dashed cross with the card
    turning dashed; `note` as a chip under the card) · bracket(scene, i, j, text) (a brace over
    cards i..j with a 20 pt label). .cards"""

    def __init__(self, items=AUTOMATION, card_w: float = 2.4, size: float = 20, **kw):
        super().__init__(**kw)
        self.cards = VGroup(*[label_box(s, INK, size=size, box_w=card_w) for s in items])
        h = max(c.height for c in self.cards)
        for c in self.cards:
            fr = box(card_w, h, INK, fill_opacity=0.06)
            fr.move_to(c)
            c.remove(c.frame)
            c.frame = fr
            c.add_to_back(fr)
        self.cards.arrange(RIGHT, buff=0.1)
        self.add(self.cards)
        self.size = size

    def mark(self, scene, i: int, ok: bool, note: str | None = None, run_time: float = 0.5):
        c = self.cards[i]
        anims = []
        disc = Circle(radius=0.22, stroke_width=0).set_fill(S.BG, 1).move_to(c.frame.get_corner(UR) + np.array([-0.1, 0.05, 0]))
        anims.append(FadeIn(disc))
        if ok:
            m = VGroup(disc, check_mark(0.3, PASS, stroke=5).move_to(disc))
            anims += [Create(m[1]), c.frame.animate.set_stroke(PASS)]
        else:
            m = VGroup(disc, cross_mark(0.26, S.GREY, stroke=4).move_to(disc))
            dashed = outline_box(c.frame.width, c.frame.height, S.GREY).move_to(c.frame)
            anims += [Create(m[1]), Transform(c.frame, dashed), c.text.animate.set_color(S.GREY)]
        new = [m]
        if note:
            n = (ok_chip if ok else dashed_chip)(note, size=self.size)
            n.next_to(c, DOWN, buff=0.12)
            anims.append(FadeIn(n, shift=UP * 0.1))
            new.append(n)
        scene.play(*anims, run_time=run_time)
        self.keep(scene, *new)
        return new

    def bracket(self, scene, i: int, j: int, text: str, color=PASS, run_time: float = 0.5):
        g = VGroup(*self.cards[i:j + 1])
        br = Brace(g, UP, color=color, buff=0.08)
        t = label(text, self.size, color).next_to(br, UP, buff=0.08)
        scene.play(Create(br), FadeIn(t), run_time=run_time)
        self.keep(scene, br, t)
        return VGroup(br, t)


class BeadChain(Piece):
    """S14's '&&' chain: one bead (a small box, mono 20) per command, joined by GREY '&&' links.
    ~11.6 x 0.55 for CHAIN_ITEMS. ANIM light(i, colour) · PLAYS state(scene, i, 'ok'|'fail'|'never')
    ('never' turns the bead GREY dashed). .beads (.frame .text) .links"""

    def __init__(self, items=CHAIN_ITEMS, size: float = 20, color=TOOL, max_w: float = 12.4, **kw):
        super().__init__(**kw)
        self.beads = VGroup(*[crate(s, size=size, color=color, box_h=0.5) for s in items])
        parts = []
        self.links = VGroup()
        for i, b in enumerate(self.beads):
            parts.append(b)
            if i < len(self.beads) - 1:
                ln = mono("&&", size, S.GREY)
                self.links.add(ln)
                parts.append(ln)
        rows, cur, w = [], [], 0.0
        for m in parts:
            if cur and w + m.width + 0.1 > max_w:
                rows.append(VGroup(*cur).arrange(RIGHT, buff=0.1))
                cur, w = [], 0.0
            cur.append(m)
            w += m.width + 0.1
        rows.append(VGroup(*cur).arrange(RIGHT, buff=0.1))
        VGroup(*rows).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(ORIGIN)
        self.add(self.beads, self.links)
        self.size = size

    def light(self, i: int, color=TURN, run_time: float = 0.5):
        b = self.beads[i]
        return AnimationGroup(Circumscribe(b, color=color, buff=0.05), Indicate(b.text, color=color),
                              run_time=run_time)

    def state(self, scene, i: int, st: str, run_time: float = 0.4):
        b = self.beads[i]
        if st == "never":
            new = outline_box(b.frame.width, b.frame.height, S.GREY).move_to(b.frame)
            scene.play(Transform(b.frame, new), b.text.animate.set_color(S.GREY), run_time=run_time)
        else:
            col = PASS if st == "ok" else ERR
            new = box(b.frame.width, b.frame.height, col, fill_opacity=0.2).move_to(b.frame)
            scene.play(Transform(b.frame, new), b.text.animate.set_color(col if st == "fail" else INK),
                       run_time=run_time)


# ================================================================== V1 · two sieves
def _sieve(sieve_w: float, text: str, size: float = 20, color=TOOL) -> VGroup:
    """A sieve: a PURPLE rim with a mesh of short ticks under it and a mono label. .rim .mesh .text"""
    rim = Line(LEFT * sieve_w / 2, RIGHT * sieve_w / 2, color=color, stroke_width=6)
    n = max(5, int(sieve_w / 0.28))
    mesh = VGroup(*[Line(UP * 0.0, DOWN * 0.16, color=color, stroke_width=2).move_to([x, -0.1, 0])
                    for x in np.linspace(-sieve_w / 2 + 0.12, sieve_w / 2 - 0.12, n)])
    t = mono(text, size, color)
    g = VGroup(rim, mesh, t)
    g.rim, g.mesh, g.text = rim, mesh, t
    return g


class KeywordSieves(Piece):
    """V1: a commit message (a PINK ribbon) meets two sieves, both reading head_commit.message.

    Full (S12): sieve 1 (rim 5.6 wide at (-1.0, 1.45), label "if: … '/run-'" right of it) over a BLUE
    job box (x -3.8 .. 1.8, y -1.25 .. 0.95, title 'job · GitHub runner') with four tiles 'AWS login'
    'build images' 'push to ECR' 'deploy'; sieve 2 (small, over the 'deploy' tile, label
    "'/run-deploy-app'" right of the job box); an ECR shelf under the job box (y -2.2) and a BLUE
    server with three TEAL containers at the right (x 3.3 .. 6.1). Overall ~12.2 x 5.3.
    Teaser (S01): sieve 1 only (rim 4.6 at (-1.6, 0.7), label right of it) and a small BLUE server
    under it at (-1.6, -1.55); ~8.6 x 3.6 (x -3.9 .. 4.7).

    PLAYS hover(scene, text) a ribbon waits above sieve 1 (returns it) · drop(scene, ribbon_or_text,
    stop, miss='bounce') stop 0: stopped by sieve 1 (RED flash; 'bounce' = up and away RED, 'slide' =
    slides off GREY); 1: passes sieve 1 (GREEN flash), the first three tiles light, three cubes land
    on the ECR shelf, a PINK dot stops at sieve 2 (RED flash); 2: passes both, 'deploy' lights, the
    server's containers blink out and in. The ribbon fades at the end. stream(scene, n=33,
    run_time=3.0) n small PINK dots fall through sieve 1 and light the server (teaser). images(scene)
    three cubes onto the ECR shelf. ANIM flash(i, ok). .sieves .job .tiles .ecr .server .containers
    .entry (point where ribbons appear) .ecr_items"""

    def __init__(self, teaser: bool = False, size: float = 20, **kw):
        super().__init__(**kw)
        self.teaser, self.size = teaser, size
        self.sieves = VGroup()
        self.ecr_items = VGroup()
        if teaser:
            s1 = _sieve(4.6, "contains(…, '/run-')", size)
            s1.move_to([-1.6, 0.7, 0])
            s1.text.next_to(s1.rim, RIGHT, buff=0.3)
            self.sieves.add(s1)
            self.server = self._server(2.6, 1.3).move_to([-1.6, -1.55, 0])
            self.entry = np.array([-1.6, 2.0, 0])
            self.job = self.tiles = self.ecr = None
            self.add(s1, self.server)
            return
        s1 = _sieve(5.6, "if: … '/run-'", size)
        s1.move_to([-1.0, 1.45, 0])
        s1.text.next_to(s1.rim, RIGHT, buff=0.3)
        self.sieves.add(s1)
        names = ("AWS login", "build images", "push to ECR", "deploy")
        tiles = VGroup(*[label_box(n, INK, size=size, fill_opacity=0.06) for n in names]).arrange(RIGHT, buff=0.14)
        tiles.move_to([-1.0, -0.65, 0])
        self.tiles = tiles
        jw = max(5.6, tiles.width + 0.4)
        jf = box(jw, 2.2, CLOUD, fill_opacity=0.06).move_to([-1.0, -0.15, 0])
        jt = label("job · GitHub runner", size, CLOUD).move_to(jf.get_corner(UL) + np.array([0, -0.3, 0]))
        jt.align_to(jf, LEFT).shift(RIGHT * 0.25)
        self.job = VGroup(jf, jt)
        self.job.frame, self.job.text = jf, jt
        last = tiles[-1]
        s2 = _sieve(last.width + 0.3, "'/run-deploy-app'", size)
        s2.move_to([last.get_center()[0], 0.05, 0])
        s2.text.next_to(jf, RIGHT, buff=0.2).set_y(0.05)
        self.sieves.add(s2)
        ef = box(5.6, 0.8, CLOUD, fill_opacity=0.08).move_to([-1.0, -2.25, 0])
        et = label("ECR", size, CLOUD).next_to(ef.get_left(), RIGHT, buff=0.25)
        board = Line(ef.get_left() + RIGHT * 1.1 + DOWN * 0.22, ef.get_right() + LEFT * 0.2 + DOWN * 0.22,
                     color=CLOUD, stroke_width=3)
        self.ecr = VGroup(ef, et, board)
        self.ecr.frame, self.ecr.text, self.ecr.board = ef, et, board
        self.server = self._server(2.8, 1.7).move_to([4.7, -1.6, 0])
        self.entry = np.array([-1.0, 2.3, 0])
        self.add(self.job, tiles, s1, s2, self.ecr, self.server)

    def _server(self, w, h):
        fr = box(w, h, CLOUD, fill_opacity=0.08)
        t = label("EC2 server", self.size, CLOUD).move_to(fr.get_top() + DOWN * 0.28)
        cs = VGroup(*[RoundedRectangle(width=0.5, height=0.42, corner_radius=0.06, stroke_color=IMAGE,
                                       stroke_width=2.5).set_fill(IMAGE, 0.3) for _ in range(3)]).arrange(RIGHT, buff=0.18)
        cs.move_to(fr.get_center() + DOWN * 0.2)
        g = VGroup(fr, t, cs)
        g.frame, g.text = fr, t
        self.containers = cs
        return g

    def flash(self, i: int, ok: bool, run_time: float = 0.5):
        s = self.sieves[i]
        col = PASS if ok else ERR
        return AnimationGroup(Indicate(s.rim, color=col, scale_factor=1.04), s.mesh.animate(rate_func=there_and_back).set_color(col),
                              run_time=run_time)

    def _rib(self, x):
        return x if isinstance(x, VGroup) else ribbon(x, ROUTE, self.size)

    def hover(self, scene, text, run_time: float = 0.5):
        r = self._rib(text).move_to(self.entry)
        scene.play(FadeIn(r, shift=DOWN * 0.3), run_time=run_time)
        return r

    def images(self, scene, src=None, run_time: float = 0.9):
        cubes = VGroup(*[cube_glyph(0.36) for _ in range(3)]).arrange(RIGHT, buff=0.18)
        n = len(self.ecr_items)
        x0 = self.ecr.board.get_left()[0] + 0.35 + n * 0.62
        for k, c in enumerate(cubes):
            c.move_to([x0 + k * 0.62, 0, 0]).align_to(self.ecr.board, DOWN).shift(UP * 0.04)
        start = (src.get_center() if src is not None else self.ecr.frame.get_top() + UP * 0.6)
        starts = [c.copy().move_to(start) for c in cubes]
        scene.play(LaggedStart(*[Transform(s, c) for s, c in zip(starts, cubes)], lag_ratio=0.25), run_time=run_time)
        scene.remove(*starts)
        self.ecr_items.add(*cubes)
        self.keep(scene, *cubes)
        return cubes

    def _recreate(self, scene, run_time: float = 0.9):
        ghosts = VGroup(*[outline_box(c.width, c.height, S.GREY).move_to(c) for c in self.containers])
        scene.play(self.containers.animate.set_fill(opacity=0).set_stroke(opacity=0), FadeIn(ghosts),
                   run_time=run_time * 0.45)
        scene.play(self.containers.animate.set_fill(IMAGE, 0.3).set_stroke(opacity=1), FadeOut(ghosts),
                   run_time=run_time * 0.55)
        scene.remove(ghosts)

    def stream(self, scene, n: int = 33, run_time: float = 3.0):
        s1 = self.sieves[0]
        dots = VGroup(*[dot(ROUTE, 0.06).move_to(self.entry + RIGHT * ((k * 0.37) % 3.0 - 1.5)) for k in range(n)])
        dots.set_x(s1.rim.get_x())
        target = self.server.frame.get_top() + DOWN * 0.1
        anims = [Succession(FadeIn(d, run_time=0.1),
                            d.animate(run_time=0.5, rate_func=linear).move_to([d.get_x(), s1.rim.get_y() - 0.3, 0]),
                            d.animate(run_time=0.4).move_to(target).set_opacity(0)) for d in dots]
        scene.play(LaggedStart(*anims, lag_ratio=0.08),
                   Indicate(self.server.frame, color=CLOUD, scale_factor=1.03), run_time=run_time)
        scene.remove(*dots)

    def drop(self, scene, text, stop: int, miss: str = "bounce", run_time: float = 1.0):
        r = text if isinstance(text, VGroup) else None
        if r is None or r not in scene.mobjects:
            r = self.hover(scene, text if r is None else r, run_time=0.4)
        s1 = self.sieves[0]
        scene.play(r.animate.move_to([s1.rim.get_center()[0], s1.rim.get_y() + 0.35, 0]), run_time=run_time * 0.4)
        if stop == 0:
            col = ERR if miss == "bounce" else S.GREY
            if miss == "bounce":
                scene.play(self.flash(0, False), r.frame.animate.set_stroke(ERR).set_fill(ERR, 0.25), run_time=0.5)
                scene.play(r.animate.shift(UP * 0.7 + RIGHT * 1.2).set_opacity(0), run_time=run_time * 0.6)
            else:
                scene.play(self.flash(0, False), r.frame.animate.set_stroke(col), run_time=0.4)
                scene.play(r.animate.shift(RIGHT * 3.5 + DOWN * 0.3).set_opacity(0), run_time=run_time * 0.7)
            scene.remove(r)
            return None
        scene.play(self.flash(0, True), run_time=0.5)
        d = dot(ROUTE).move_to(r.get_bottom())
        if self.teaser:
            scene.play(d.animate.move_to(self.server.frame.get_top() + DOWN * 0.15), run_time=run_time * 0.5)
            scene.play(Indicate(self.server.frame, color=CLOUD, scale_factor=1.03), FadeOut(d), FadeOut(r), run_time=0.5)
            scene.remove(d, r)
            return None
        scene.play(d.animate.move_to(self.job.text.get_right() + RIGHT * 0.3), run_time=run_time * 0.4)
        scene.play(LaggedStart(*[Circumscribe(self.tiles[i], color=CLOUD, buff=0.05) for i in range(3)],
                               lag_ratio=0.4), run_time=0.9)
        self.images(scene, self.tiles[2])
        s2 = self.sieves[1]
        scene.play(d.animate.move_to([s2.rim.get_center()[0], s2.rim.get_y() + 0.22, 0]), run_time=0.5)
        if stop == 1:
            scene.play(self.flash(1, False), d.animate.set_color(ERR), run_time=0.5)
            scene.play(FadeOut(d), FadeOut(r), run_time=0.4)
            scene.remove(d, r)
            return None
        scene.play(self.flash(1, True), run_time=0.5)
        scene.play(d.animate.move_to(self.tiles[3]), Circumscribe(self.tiles[3], color=CLOUD, buff=0.05), run_time=0.6)
        path = route(self.tiles[3].get_right(), self.server.frame.get_left(), arc=-0.3)
        scene.play(GrowArrow(path), run_time=0.5)
        self._recreate(scene)
        scene.play(FadeOut(d), FadeOut(r), FadeOut(path), run_time=0.4)
        scene.remove(d, r, path)
        return None


# ================================================================== V2 · slide 19's map in AWS words
TERM_PAIRS = {   # key: (GCP word (GREY dashed), AWS word lines (BLUE unless said))
    "kubernetes": ("Kubernetes", ("one EC2 server", "Docker containers")),
    "registry": ("Artifact Registry", ("ECR · 3 repositories",)),
    "pulumi": ("Pulumi (L20)", ("Ansible playbooks",)),
    "key": ("service-account key", None),
    "keyword": (SLIDES_KEYWORD, (KEYWORD,)),
    "ingress": ("ingress", ("nginx container",)),
}


class TermMap(Piece):
    """V2 (S02): slide 19 redrawn. Bottom flow (y -0.9): 'Dev Team' -> PINK 'Commits' -> GitHub
    (Code · Branches · Actions) -> 'GitHub Actions' (Build → Deploy) -> a BLUE cloud box (rows
    'Storage', 'Artifact Registry' (hidden until gcp('registry')), 'Vertex AI', 'Kubernetes',
    'ingress' (hidden)) -> 'Users'. Top chain (y 1.6): Data Collector → Data Processor → Model
    Training → Model Deploy → Backend API → Frontend. Everything starts hidden: draw_flow / draw_chain
    reveal it. ~12.7 x 5.0.
    PLAYS draw_flow(scene, per=0.5) · draw_chain(scene, per=0.35) · source(scene) the top-right chip
    'slides: Google Cloud · cheese-app-v4' -> 'this video: AWS · cheese-app-aws · as in L15' (first
    call shows the GREY one, second transforms) · gcp(scene, key) shows a GCP word that is not drawn
    by default ('registry' in the cloud, 'pulumi' under Actions, 'key' above Actions, 'keyword'
    above Commits, 'ingress' in the cloud) · relabel(scene, key) GCP word -> AWS word (TERM_PAIRS;
    'key' becomes the badge + key glyphs with 'IAM access key' / 'EC2 key pair') · fade_ml(scene)
    the four ML boxes and Vertex AI turn GREY dashed + 'not in this repo · the AWS ML pipeline was
    L15' (top left, y 2.5); the Model Deploy → Backend API arrow goes dashed + a chip above the chain
    (y 2.5; the source chip leaves). .flow{dev github actions cloud
    users} .chain[0..5] .chain_arrows .flow_arrows .labels{key} .cloud_rows{key} .src_chip"""

    CHAIN = ("Data\nCollector", "Data\nProcessor", "Model\nTraining", "Model\nDeploy", "Backend\nAPI", "Frontend")

    def __init__(self, size: float = 20, **kw):
        super().__init__(**kw)
        self.size = size
        y = -0.9
        icons = VGroup(person_icon(LAPTOP, 0.42), person_icon(LAPTOP, 0.42)).arrange(RIGHT, buff=0.1)
        dev = VGroup(icons, label("Dev Team", size, LAPTOP)).arrange(DOWN, buff=0.1).move_to([-5.75, y, 0])
        gh = VGroup(*[label(s, size, c) for s, c in (("GitHub", CLOUD), ("Code", INK), ("Branches", INK),
                                                       ("Actions", INK))]).arrange(DOWN, buff=0.08)
        ghf = box(1.75, gh.height + 0.35, CLOUD, fill_opacity=0.08)
        gh.move_to(ghf)
        github = VGroup(ghf, gh).move_to([-3.3, y, 0])
        at = label("GitHub Actions", size, CLOUD)
        ab = VGroup(label("Build", size, INK), label("→", size, S.GREY), label("Deploy", size, INK)).arrange(RIGHT, buff=0.12)
        acts_in = VGroup(at, ab).arrange(DOWN, buff=0.2)
        af = box(2.3, acts_in.height + 0.4, CLOUD, fill_opacity=0.08)
        acts_in.move_to(af)
        actions = VGroup(af, acts_in).move_to([-0.9, y, 0])
        actions.deploy = ab[2]
        rows = {}
        names = (("storage", "Storage"), ("registry", "Artifact Registry"), ("vertex", "Vertex AI"),
                 ("kubernetes", "Kubernetes"), ("ingress", "ingress"))
        col = VGroup()
        for k, s in names:
            r = dashed_chip(s, PAST, size)
            rows[k] = r
            col.add(r)
        slots = (0.5, 0.5, 0.5, 0.86, 0.5)               # Kubernetes gets room for two lines
        cf = box(3.2, sum(slots) + 0.4 + 0.5, CLOUD, fill_opacity=0.06).move_to([2.55, y - 0.2, 0])
        ct = label("cloud", size, CLOUD).move_to(cf.get_top() + DOWN * 0.25)
        yy = ct.get_bottom()[1] - 0.12
        for (k, _s), h in zip(names, slots):
            rows[k].move_to([cf.get_x(), yy - h / 2, 0])
            yy -= h + 0.1
        cloud = VGroup(cf, ct, col)
        self.cloud_rows = rows
        users = VGroup(person_icon(LAPTOP, 0.42), label("Users", size, LAPTOP)).arrange(DOWN, buff=0.1).move_to([5.75, y, 0])
        self.flow = {"dev": dev, "github": github, "actions": actions, "cloud": cloud, "users": users}
        order = [dev, github, actions, cloud, users]
        self.flow_arrows = VGroup(*[arrow(a.get_right(), b.get_left(), ROUTE if i == 0 else S.GREY, 3)
                                    for i, (a, b) in enumerate(zip(order, order[1:]))])
        self.commits_label = label("Commits", size, ROUTE).next_to(self.flow_arrows[0], UP, buff=0.12)
        self.chain = VGroup(*[label_box(s, INK, size=size, box_w=1.62) for s in self.CHAIN])
        hmax = max(c.height for c in self.chain)
        for i, c in enumerate(self.chain):
            c.move_to([-5.4 + i * 2.15, 1.6, 0])
            if abs(c.height - hmax) > 0.01:
                fr = box(1.62, hmax, INK, fill_opacity=0.1).move_to(c)
                c.remove(c.frame)
                c.frame = fr
                c.add_to_back(fr)
        self.chain_arrows = VGroup(*[arrow(a.get_right(), b.get_left(), S.GREY, 2.5)
                                     for a, b in zip(self.chain, self.chain[1:])])
        # hidden GCP words
        self.labels = {}
        self.labels["pulumi"] = dashed_chip("Pulumi (L20)", PAST, size).next_to(actions, DOWN, buff=0.15)
        self.labels["key"] = dashed_chip("service-account key", PAST, size).move_to([-1.2, 0.4, 0])
        self.labels["keyword"] = dashed_chip(SLIDES_KEYWORD, ROUTE, size, mono_font=True).move_to([-5.1, 0.35, 0])
        self.labels["registry"] = rows["registry"]
        self.labels["ingress"] = rows["ingress"]
        self.labels["kubernetes"] = rows["kubernetes"]
        self.src_chip = None
        self._hidden = {"registry", "ingress", "pulumi", "key", "keyword"}

    # -- reveal
    def draw_flow(self, scene, per: float = 0.5):
        order = ["dev", "github", "actions", "cloud", "users"]
        for i, k in enumerate(order):
            g = self.flow[k]
            if k == "cloud":
                parts = [g[0], g[1]] + [r for kk, r in self.cloud_rows.items() if kk not in self._hidden]
                anims = [FadeIn(VGroup(*parts), shift=RIGHT * 0.1)]
            else:
                anims = [FadeIn(g, shift=RIGHT * 0.1)]
            if i:
                anims.insert(0, GrowArrow(self.flow_arrows[i - 1]))
                if i == 1:
                    anims.append(FadeIn(self.commits_label))
            scene.play(*anims, run_time=per)
        self.add(*[self.flow[k][:2] if k == "cloud" else self.flow[k] for k in order], self.flow_arrows,
                 self.commits_label)
        for kk, r in self.cloud_rows.items():
            if kk not in self._hidden:
                self.add(r)
        self._reseat(scene)

    def draw_chain(self, scene, per: float = 0.35):
        for i, c in enumerate(self.chain):
            anims = [FadeIn(c, shift=RIGHT * 0.1)]
            if i:
                anims.insert(0, GrowArrow(self.chain_arrows[i - 1]))
            scene.play(*anims, run_time=per)
        self.add(self.chain, self.chain_arrows)
        self._reseat(scene)

    def source(self, scene, run_time: float = 0.7):
        if self.src_chip is None:
            c = dashed_chip("slides: Google Cloud · cheese-app-v4", PAST, self.size)
            c.move_to([6.4 - c.width / 2, 2.5, 0])
            scene.play(FadeIn(c), run_time=run_time * 0.6)
            self.src_chip = c
            self.keep(scene, c)
            return c
        new = cloud_chip("this video: AWS · cheese-app-aws · as in L15", self.size)
        new.move_to([6.4 - new.width / 2, 2.5, 0])
        scene.play(Transform(self.src_chip, new), run_time=run_time)
        return self.src_chip

    def gcp(self, scene, key: str, run_time: float = 0.5):
        g = self.labels[key]
        scene.play(FadeIn(g, scale=0.9), run_time=run_time)
        self._hidden.discard(key)
        self.keep(scene, g)
        return g

    def relabel(self, scene, key: str, run_time: float = 0.8):
        old = self.labels[key]
        if key in self._hidden:
            self.gcp(scene, key)
        if key == "key":
            a = VGroup(badge_glyph(0.36), label("IAM access key", self.size, INK)).arrange(RIGHT, buff=0.14)
            b = VGroup(key_glyph(0.36), label("EC2 key pair", self.size, INK)).arrange(RIGHT, buff=0.14)
            new = VGroup(a, b).arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to(old)
        elif key == "keyword":
            new = route_chip(KEYWORD, self.size).move_to(old)
        else:
            lines = TERM_PAIRS[key][1]
            color = IMAGE if key == "ingress" else CLOUD
            new = label_box(list(lines), color, size=self.size, pad=0.1).move_to(old)
        scene.play(ReplacementTransform(old, new), run_time=run_time)
        for owner in [self, *self.get_family()]:
            if old in owner.submobjects:
                owner.remove(old)
        self.labels[key] = new
        if key in self.cloud_rows:
            self.cloud_rows[key] = new
        self.keep(scene, new)
        return new

    def fade_ml(self, scene, run_time: float = 0.9):
        targets = list(self.chain[:4])
        anims = []
        for c in targets:
            d = outline_box(c.frame.width, c.frame.height, S.GREY).move_to(c.frame)
            anims += [Transform(c.frame, d), c.text.animate.set_color(S.GREY)]
        v = self.cloud_rows["vertex"]
        anims.append(v.animate.set_opacity(0.45))
        a = self.chain_arrows[3]
        da = DashedLine(a.get_start(), a.get_end(), color=S.GREY, stroke_width=2.5, dash_length=0.08)
        anims.append(Transform(a, da))
        note_ = label("not in this repo · the AWS ML pipeline was L15", self.size, S.GREY)
        note_.move_to([-6.3 + note_.width / 2, 2.5, 0])
        ch = grey_chip("a fixed model file, not a pipeline", self.size)
        ch.move_to([a.get_center()[0] + 0.6, 2.5, 0])
        anims += [FadeIn(note_), FadeIn(ch, shift=DOWN * 0.1)]
        if self.src_chip is not None and self.src_chip in self.get_family():
            anims.append(FadeOut(self.src_chip))
        scene.play(*anims, run_time=run_time)
        if self.src_chip is not None and self.src_chip in self.get_family():
            self._gone(scene, self.src_chip)
            self.src_chip = None
        self.ml_note, self.ml_chip = note_, ch
        self.keep(scene, note_, ch)
        return VGroup(note_, ch)


# ================================================================== V3 · two secrets, every copy
PLACES = {   # key: (text lines, colour)
    "secrets": (("~/secrets/", "CSV · .pem"), LAPTOP),
    "shell": (("docker-shell.sh", "lines 13–15"), LAPTOP),
    "toolbox": (("toolbox", "environment"), IMAGE),
    "ansible": (("lookup('env', …)", "inventory.yml 9–11"), TOOL),
    "server_cfg": (("server", "aws configure"), CLOUD),
    "server_file": (("/srv/secrets", "mode 0600"), CLOUD),
    "api_env": (("api-service", "environment"), IMAGE),
    "vault": (("GitHub", "repository secrets"), CLOUD),
    "runner_ssh": (("runner", "~/.ssh/ac215_2024.pem"), CLOUD),
    "toolbox_ssh": (("toolbox", "/root/.ssh"), IMAGE),
}
SNAKE = ("secrets", "shell", "toolbox", "ansible", "server_cfg", "server_file", "api_env", "vault")


class KeyJourney(Piece):
    """V3: the access-key badge and the key-pair key, and every place a copy ends up. Places are
    boxes (2.8 x 1.0, two 20 pt lines) in PLACES colours. Default: SNAKE (8 places): top row
    left->right secrets, shell, toolbox, ansible; bottom row right->left server_cfg, server_file,
    api_env, vault (12.3 x 3.6, rows at y +1.0 / -1.0). places=(keys…): <= 4 keys in one row.
    PLAYS start(scene) (badge and key appear in 'secrets'; the place must exist) · send(scene, which,
    src, dst, leave=True, arc=0.0) ('badge' or 'key': a PINK arrow src -> dst, the glyph rides it,
    a copy stays at dst (top-right corner; several copies sit side by side)) · counter(scene, text)
    a GREY caption ABOVE the piece (replaced on the next call) · overlay(scene, 'role'|'oidc') a
    GREY dashed box over the server places ('instance role · short-lived credentials') or the
    vault ('GitHub OIDC · no stored AWS keys'), its label under it for the bottom row; the badge
    copies inside fade. Boxes widen for long texts (runner_ssh ~3.5).
    .places{key} (.frame .text) .copies{key: VGroup} .arrows"""

    def __init__(self, places=None, place_w: float = 2.8, size: float = 20, **kw):
        super().__init__(**kw)
        keys = tuple(places) if places else SNAKE
        self.size, self.place_w = size, place_w
        self.places, self.copies = {}, {}
        for k in keys:
            lines, col = PLACES[k]
            tw = max(label(x, size).width for x in lines)
            p = label_box(list(lines), col, size=size, box_w=max(place_w, tw + 0.35), mono_font=False)
            p.text[0].set_color(col)
            p.text[1].set_color(S.GREY)
            self.places[k] = p
            self.copies[k] = VGroup()
        if len(keys) <= 4:
            VGroup(*[self.places[k] for k in keys]).arrange(RIGHT, buff=0.45).move_to(ORIGIN)
        else:
            top, bot = keys[:4], keys[4:]
            xs = [-4.725, -1.575, 1.575, 4.725]
            for k, x in zip(top, xs):
                self.places[k].move_to([x, 1.0, 0])
            for k, x in zip(bot, xs[::-1]):
                self.places[k].move_to([x, -1.0, 0])
        hmax = max(p.height for p in self.places.values())
        for p in self.places.values():
            if abs(p.frame.height - hmax) > 0.01:
                fr = box(p.frame.width, hmax, p.text[0].get_color(), fill_opacity=0.1).move_to(p)
                p.remove(p.frame)
                p.frame = fr
                p.add_to_back(fr)
        self.arrows = VGroup()
        self.add(*self.places.values(), self.arrows)
        self.caption = None
        self.overlays = {}

    def _glyph(self, which):
        return badge_glyph(0.3) if which == "badge" else key_glyph(0.3)

    def _slot(self, key, n):
        p = self.places[key]
        return p.frame.get_corner(UR) + np.array([-0.32 - 0.62 * n, 0.0, 0])

    def start(self, scene, run_time: float = 0.6):
        b, k = self._glyph("badge"), self._glyph("key")
        b.move_to(self._slot("secrets", 0))
        k.move_to(self._slot("secrets", 1))
        scene.play(FadeIn(b, scale=1.4), FadeIn(k, scale=1.4), run_time=run_time)
        b.kind, k.kind = "badge", "key"
        self.copies["secrets"].add(b, k)
        self.keep(scene, b, k)
        return b, k

    def send(self, scene, which: str, src: str, dst: str, leave: bool = True, arc: float = 0.0,
             run_time: float = 1.0):
        a, b = self.places[src].frame, self.places[dst].frame
        if abs(a.get_y() - b.get_y()) < 0.1:
            p, q = (a.get_right(), b.get_left()) if a.get_x() < b.get_x() else (a.get_left(), b.get_right())
        else:
            p, q = (a.get_bottom(), b.get_top()) if a.get_y() > b.get_y() else (a.get_top(), b.get_bottom())
        ar = route(p, q, arc=arc, stroke=3)
        g = self._glyph(which).move_to(p)
        scene.play(GrowArrow(ar), FadeIn(g), run_time=run_time * 0.4)
        n = len(self.copies[dst])
        scene.play(MoveAlongPath(g, ar.copy()), run_time=run_time * 0.4)
        scene.play(g.animate.move_to(self._slot(dst, n)), run_time=run_time * 0.2)
        g.kind = which
        self.arrows.add(ar)
        self._reseat(scene)
        if leave:
            self.copies[dst].add(g)
            self.keep(scene, g)
        else:
            scene.play(FadeOut(g), run_time=0.2)
            scene.remove(g)
        scene.add(self)
        return g

    def counter(self, scene, text: str, run_time: float = 0.4):
        t = label(text, self.size, S.GREY)
        t.next_to(VGroup(*self.places.values()), UP, buff=0.45)
        if self.caption is None:
            scene.play(FadeIn(t), run_time=run_time)
        else:
            t.move_to(self.caption)
            scene.play(Transform(self.caption, t), run_time=run_time)
            return self.caption
        self.caption = t
        self.keep(scene, t)
        return t

    def overlay(self, scene, kind: str = "role", run_time: float = 0.8):
        keys = [k for k in (("server_cfg", "server_file", "api_env") if kind == "role" else ("vault",))
                if k in self.places]
        g = VGroup(*[self.places[k] for k in keys])
        ob = outline_box(g.width + 0.3, g.height + 0.3, S.GREY).move_to(g)
        t = label("instance role · short-lived credentials" if kind == "role" else "GitHub OIDC · no stored AWS keys",
                  self.size, S.GREY)
        t.next_to(ob, DOWN if ob.get_y() < VGroup(*self.places.values()).get_y() - 0.1 else UP, buff=0.08)
        if t.get_left()[0] < -6.5:
            t.shift(RIGHT * (-6.5 - t.get_left()[0]))
        if t.get_right()[0] > 6.5:
            t.shift(LEFT * (t.get_right()[0] - 6.5))
        gone = [c for k in keys for c in self.copies[k] if getattr(c, "kind", "") == "badge"]
        bg = Rectangle(width=t.width + 0.2, height=t.height + 0.1, stroke_width=0).set_fill(S.BG, 0.9).move_to(t)
        scene.play(Create(ob.frame), FadeIn(bg), FadeIn(t), *[FadeOut(c) for c in gone], run_time=run_time)
        self._gone(scene, *gone)
        grp = VGroup(ob, bg, t)
        self.overlays[kind] = grp
        self.keep(scene, grp)
        return grp


# ================================================================== V4 · Ansible in one picture
class AnsibleMachine(Piece):
    """V4 (S04): left the InventoryTree (x -6.5 .. -3.9); middle two PlayCards stacked
    ('deploy-create-instance.yml' / 'Create App Application Machine' / localhost / ec2_group ec2_vol
    ec2_instance; 'deploy-provision-instance.yml' / 'Configure app server instance' / appserver /
    apt mount shell), x ~-3.6 .. 3.1; right column (x 3.8 .. 6.2): a BLUE 'AWS · us-east-1' box
    (top), the small TEAL toolbox (middle; PINK API arrow up), a BLUE server (bottom; PINK SSH arrow
    down). ~12.8 x 5.0.
    PLAYS fire(scene, card, tile, state='changed') · ssh(scene) (the PINK SSH arrow toolbox ->
    server + chip 'ubuntu + your key'; fire() on the appserver card calls it if needed).
    .tree .cards .toolbox .aws .server .ssh_arrow .ssh_chip .api_arrow"""

    def __init__(self, size: float = 20, **kw):
        super().__init__(**kw)
        self.size = size
        self.tree = InventoryTree(size=size).move_to([-5.2, -0.2, 0])
        c1 = PlayCard("deploy-create-instance.yml", "Create App Application Machine", "localhost",
                      ("ec2_group", "ec2_vol", "ec2_instance"), cols=3, tile_w="fit", mono_tiles=True, size=size)
        c2 = PlayCard("deploy-provision-instance.yml", "Configure app server instance", "appserver",
                      ("apt", "mount", "shell"), cols=3, tile_w="fit", mono_tiles=True, card_w=c1.frame.width, size=size)
        self.cards = VGroup(c1, c2).arrange(DOWN, buff=0.25).move_to([-0.25, -0.2, 0])
        self.toolbox = crate("toolbox", size=size, box_h=0.8).move_to([5.0, -0.2, 0])
        self.aws = aws_box("AWS · us-east-1", 2.4, 1.0, size).move_to([5.0, 1.75, 0])
        sv = aws_box("server", 2.4, 1.2, size).move_to([5.0, -2.2, 0])
        server_glyph = VGroup(*[RoundedRectangle(width=1.2, height=0.16, corner_radius=0.04, stroke_color=CLOUD,
                                                 stroke_width=2).set_fill(PANEL, 1) for _ in range(2)])
        server_glyph.arrange(DOWN, buff=0.06).move_to(sv.body)
        sv.add(server_glyph)
        sv.glyph = server_glyph
        self.server = sv
        self.api_arrow = route(self.toolbox.get_top(), self.aws.frame.get_bottom(), stroke=3)
        self.ssh_arrow = None
        self.ssh_chip = None
        self.add(self.tree, self.cards, self.toolbox, self.aws, self.server)

    def ssh(self, scene, run_time: float = 0.6):
        if self.ssh_arrow is not None:
            return self.ssh_arrow
        ar = route(self.toolbox.get_bottom(), self.server.frame.get_top(), stroke=3)
        ch = grey_chip("ubuntu + your key", self.size).next_to(self.server, DOWN, buff=0.1)
        scene.play(GrowArrow(ar), FadeIn(ch), run_time=run_time)
        self.ssh_arrow, self.ssh_chip = ar, ch
        self.keep(scene, ar, ch)
        return ar

    def fire(self, scene, card: int, tile: int, state: str = "changed", run_time: float = 1.2):
        c = self.cards[card]
        sp = spark(TOOL, 0.3).move_to(self.toolbox.frame)
        scene.play(c.set_state(tile, state), FadeIn(sp, scale=0.5), run_time=run_time * 0.3)
        d = dot(ROUTE).move_to(self.toolbox.frame.get_top())
        if card == 0:
            if self.api_arrow not in self.submobjects:
                scene.play(GrowArrow(self.api_arrow), run_time=0.3)
                self.keep(scene, self.api_arrow)
            path, target = self.api_arrow, self.aws.frame
        else:
            path, target = self.ssh(scene), self.server.frame
        scene.play(FadeOut(sp), MoveAlongPath(d, path.copy()), run_time=run_time * 0.5)
        scene.play(Indicate(target, color=CLOUD, scale_factor=1.03), FadeOut(d), run_time=run_time * 0.2)
        scene.remove(sp, d)


# ================================================================== V5 · one crate, the laptop's Docker
_MOUNTS = {
    "laptop": [("app", "src/deployment", "/app"), ("secrets", "secrets", "/secrets"),
               ("api", "api-service", "/api-service"), ("frontend", "frontend-react", "/frontend-react"),
               ("vectordb", "vector-db", "/vector-db")],
    "runner": [("deployment", "src/deployment", "/deployment"), ("ssh", "…/secrets", "/root/.ssh"),
               ("api", "api-service", "/api-service"), ("frontend", "frontend-react", "/frontend-react"),
               ("vectordb", "vector-db", "/vector-db")],
}


class SiblingContainers(Piece):
    """V5: one crate, the host's Docker. Host frame (9.0 x 5.2; GREY 'laptop' or BLUE 'GitHub
    runner'); its folders as mono chips down the left (x ~-3.0); the TEAL crate
    'cheese-app-deployment' top right (x -0.2 .. 3.9, y -0.2 .. 2.4) listing its mount points; under
    its left edge the PINK socket line '/var/run/docker.sock' down to the 'Docker engine' shelf (a
    board across the frame, y -1.95), which holds the toolbox's own image (a cube +
    'cheese-app-deployment', left); build() puts each new image right of it. Runner: the three app folders
    start GREY dashed ('the runner built them already') and their mount lines are never drawn.
    PLAYS mount(scene, key) · mounts(scene, keys=None) · hover_spark(scene) · build(scene,
    spark=None) · prune_ghost(scene) · dash(scene, keys) · badge_in(scene).
    .frame .title .folders{key} .mpoints{key} (mount points in the crate) .lines{key} .socket .crate
    .shelf .images"""

    def __init__(self, host: str = "laptop", size: float = 20, **kw):
        super().__init__(**kw)
        self.host, self.size = host, size
        col = LAPTOP if host == "laptop" else CLOUD
        self.frame = box(9.0, 5.2, col, fill_opacity=0.04)
        self.title = label("laptop" if host == "laptop" else "GitHub runner", size, col)
        self.title.move_to(self.frame.get_corner(UL) + np.array([0, -0.3, 0])).align_to(self.frame, LEFT).shift(RIGHT * 0.25)
        spec = _MOUNTS[host]
        self.folders, self.mpoints, self.lines = {}, {}, {}
        dashed_keys = ("api", "frontend", "vectordb") if host == "runner" else ()
        fcol = VGroup()
        for k, src, _dst in spec:
            fc = S.GREY if k in dashed_keys else (LAPTOP if host == "laptop" else CLOUD)
            c = VGroup(folder_glyph(0.24, fc), mono(src, size, S.GREY if k in dashed_keys else INK)).arrange(RIGHT, buff=0.12)
            c.text = c[1]
            self.folders[k] = c
            fcol.add(c)
        ct = mono(T_TOOLBOX, size, IMAGE)
        pts = VGroup()
        for k, _src, dst in spec:
            p = mono(dst, size, S.GREY if k in dashed_keys else INK)
            self.mpoints[k] = p
            pts.add(p)
        pts.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        inner = VGroup(ct, pts).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        cf = box(4.1, inner.height + 0.4, IMAGE, fill_opacity=0.1)
        cf.move_to([1.85, 2.4 - cf.height / 2, 0])
        inner.move_to(cf).align_to(cf, LEFT).shift(RIGHT * 0.25)
        self.crate = VGroup(cf, inner)
        self.crate.frame, self.crate.text = cf, ct
        for k, _src, _dst in spec:
            self.folders[k].set_y(self.mpoints[k].get_y())
            self.folders[k].align_to(self.frame, LEFT).shift(RIGHT * 0.35)
        board = Line([-3.9, -1.95, 0], [4.2, -1.95, 0], color=LAPTOP if host == "laptop" else CLOUD, stroke_width=4)
        cap = label("Docker engine", size, S.GREY).next_to(board, DOWN, buff=0.1).align_to(board, LEFT)
        self.shelf = VGroup(board, cap)
        self.shelf.board, self.shelf.text = board, cap
        own = cube_glyph(0.42)
        own.next_to(board, UP, buff=0.04).align_to(board, LEFT).shift(RIGHT * 0.3)
        own_t = mono(T_TOOLBOX, size, IMAGE).next_to(own, RIGHT, buff=0.15)
        self.images = VGroup(VGroup(own, own_t))
        sock_top = np.array([cf.get_left()[0] + 0.45, cf.get_bottom()[1], 0])
        sock_bot = np.array([cf.get_left()[0] + 0.45, board.get_y() + 0.75, 0])
        self.socket = Line(sock_top, sock_bot, color=ROUTE, stroke_width=8)
        self.socket_label = mono("/var/run/docker.sock", size, ROUTE).next_to(self.socket, RIGHT, buff=0.15)
        self.socket_on = False
        self.add(self.frame, self.title, fcol, self.crate, self.shelf, self.images)
        self.dashed_keys = dashed_keys

    def mount(self, scene, key: str, run_time: float = 0.5):
        if key == "socket":
            scene.play(Create(self.socket), FadeIn(self.socket_label), run_time=run_time)
            self.socket_on = True
            self.keep(scene, self.socket, self.socket_label)
            return self.socket
        if key in self.dashed_keys:
            return None
        f, p = self.folders[key], self.mpoints[key]
        ln = Line(f.get_right() + RIGHT * 0.05, p.get_left() + LEFT * 0.1, color=ROUTE, stroke_width=3)
        scene.play(Create(ln), Indicate(p, color=ROUTE, scale_factor=1.05), run_time=run_time)
        self.lines[key] = ln
        self.keep(scene, ln)
        return ln

    def mounts(self, scene, keys=None, per: float = 0.4):
        keys = keys or ["socket"] + [k for k, _a, _b in _MOUNTS[self.host]]
        for k in keys:
            self.mount(scene, k, per)

    def hover_spark(self, scene, run_time: float = 0.5):
        sp = VGroup(spark(TOOL, 0.3), label("docker build", self.size, TOOL))
        sp[1].next_to(sp[0], RIGHT, buff=0.1)
        sp.move_to(self.crate.frame.get_bottom() + UP * 0.35 + RIGHT * 0.9)
        scene.play(FadeIn(sp, scale=0.6), run_time=run_time)
        self.spark = sp
        return sp

    def build(self, scene, spark_=None, run_time: float = 1.6):
        """PLAYS: the build travels down the socket; a TEAL cube lands on the engine shelf beside the
        toolbox's image, GREEN chip 'sibling'. Returns (cube, chip)."""
        if not self.socket_on:
            self.mount(scene, "socket")
        sp = spark_ or getattr(self, "spark", None) or self.hover_spark(scene)
        d = spark(TOOL, 0.25).move_to(self.socket.get_start())
        scene.play(FadeOut(sp), FadeIn(d), run_time=0.3)
        scene.play(MoveAlongPath(d, self.socket.copy()), run_time=run_time * 0.4)
        cube = cube_glyph(0.42)
        cube.next_to(self.shelf.board, UP, buff=0.04).align_to(self.images[-1], LEFT).shift(RIGHT * (self.images[-1].width + 0.5))
        sib = ok_chip("sibling", self.size).next_to(cube, UP, buff=0.12)
        scene.play(ReplacementTransform(d, cube), run_time=run_time * 0.3)
        scene.play(FadeIn(sib, shift=DOWN * 0.1), run_time=0.3)
        self.spark = None
        self._gone(scene, sp)
        g = VGroup(cube, sib)
        self.images.add(g)
        self.keep(scene, g)
        return cube, sib

    def prune_ghost(self, scene, run_time: float = 2.0):
        """PLAYS: a RED dashed 'docker system prune -a' spark runs down the socket; a broom sweeps
        the shelf and the images turn to dashed ghosts, then everything comes back (undone)."""
        if not self.socket_on:
            self.mount(scene, "socket")
        t = mono("docker system prune -a", self.size, ERR).next_to(self.socket, LEFT, buff=0.15)
        d = spark(ERR, 0.25).move_to(self.socket.get_start())
        scene.play(FadeIn(t), FadeIn(d), run_time=0.3)
        scene.play(MoveAlongPath(d, self.socket.copy()), run_time=run_time * 0.25)
        br = broom_glyph(0.8).next_to(self.shelf.board, UP, buff=0.0).align_to(self.shelf.board, LEFT)
        cover = Rectangle(width=self.images.width + 0.3, height=self.images.height + 0.2, stroke_width=0)
        cover.set_fill(S.BG, 0.85).move_to(self.images)
        ghosts = dashed_copy(self.images, S.GREY)
        scene.play(FadeOut(d), FadeIn(br), run_time=0.2)
        scene.play(br.animate.shift(RIGHT * 4.2), FadeIn(cover), FadeIn(ghosts), run_time=run_time * 0.35)
        scene.play(FadeOut(br), FadeOut(ghosts), FadeOut(cover), FadeOut(t), run_time=run_time * 0.25)
        scene.remove(br, ghosts, t, d, cover)

    def dash(self, scene, keys, run_time: float = 0.5):
        anims = []
        for k in keys:
            f = self.folders[k]
            anims.append(f.animate.set_color(S.GREY))
            if k in self.lines:
                ln = self.lines[k]
                anims.append(Transform(ln, DashedLine(ln.get_start(), ln.get_end(), color=S.GREY, stroke_width=2.5)))
            anims.append(self.mpoints[k].animate.set_color(S.GREY))
        scene.play(*anims, run_time=run_time)

    def badge_in(self, scene, run_time: float = 0.8):
        """PLAYS: the badge glyph flies from the secrets folder into the crate's top-right corner."""
        src = self.folders.get("secrets", self.folders.get("ssh"))
        b = badge_glyph(0.32).move_to(src)
        scene.play(FadeIn(b, scale=1.3), run_time=0.3)
        scene.play(b.animate.move_to(self.crate.frame.get_corner(DR) + np.array([-0.45, 0.32, 0])), run_time=run_time)
        self.keep(scene, b)
        self.badge = b
        return b


# ================================================================== V6 · one tag, date -> container
class TimestampTrail(Piece):
    """V6: one timestamp tag. mode='build' (S07, 12.6 x 5.2): a GREEN stamp chip
    'date +%Y%m%d%H%M%S' (top left, y 2.2) and the tag card (hidden until stamp()); three TEAL image
    chips (middle column, x ~-0.9, y 1.2 / 0.2 / -0.8); the BLUE ECR box (x 1.9 .. 6.5, y -1.6 .. 2.5)
    with three named shelves; the '.docker-tag' file (bottom left, committed text TAG_COMMITTED); the
    registry line under it all (y -2.3). PLAYS stamp(scene) · clip(scene, i) (a copy of the card
    clips onto image i) · push(scene, i) (image i with its tag flies to shelf i) · push_all(scene) ·
    save(scene, text=None) (the committed value struck GREY, the card's copy GREEN beside it).
    mode='deploy' (S14, 12.6 x 5.0): stations on top (y 1.6): 'runner · date' BLUE, 'DOCKER_TAG'
    PINK, 'toolbox' TEAL, 'ansible · docker_tag=' PURPLE; ECR (x -6.1 .. -1.5, y -2.4 .. -0.4) and
    the server (x 0.4 .. 6.1) with three TEAL containers below. PLAYS stamp(scene) (card above the
    runner) · ride(scene) (card through the stations) · pull(scene) · recreate(scene, i=None,
    gap_chip=True). .card .images .ecr .shelves .file .stations{key} .server .containers"""

    def __init__(self, mode: str = "build", tag_text: str = TAG_FMT, size: float = 20, **kw):
        super().__init__(**kw)
        self.mode, self.tag_text, self.size = mode, tag_text, size
        self.card = None
        if mode == "build":
            self._build_layout()
        else:
            self._deploy_layout()

    def _ecr(self, w, h, names, at, boards: bool = True):
        fr = box(w, h, CLOUD, fill_opacity=0.06).move_to(at)
        t = label("ECR" if not boards else "ECR · private repositories", self.size, CLOUD)
        t.move_to(fr.get_top() + DOWN * 0.28)
        shelves = VGroup()
        for n in names:
            if boards:
                bd = Line(LEFT * (w - 0.4) / 2, RIGHT * (w - 0.4) / 2, color=CLOUD, stroke_width=3)
                nm = mono(n, self.size, S.GREY).next_to(bd, DOWN, buff=0.08).align_to(bd, LEFT)
                sh = VGroup(bd, nm)
                sh.caption, sh.board = nm, bd
            else:
                sh = image_chip(n + ":<tag>", self.size)
                sh.caption, sh.board = sh.text, sh.box
            shelves.add(sh)
        shelves.arrange(DOWN, buff=0.85 if boards else 0.12)
        shelves.next_to(t, DOWN, buff=0.62 if boards else 0.15)
        g = VGroup(fr, t, shelves)
        g.frame, g.text = fr, t
        return g, shelves

    def _build_layout(self):
        sz = self.size
        self.stamp_chip = ok_chip("date +%Y%m%d%H%M%S", sz, mono_font=True).move_to([-4.2, 2.2, 0])
        self.images = VGroup(*[image_chip(n, sz) for n in SHORT_IMAGES])
        for i, im in enumerate(self.images):
            im.move_to([-0.9, 1.2 - i * 1.0, 0])
        self.ecr, self.shelves = self._ecr(4.6, 4.1, IMAGES, [4.2, 0.45, 0])
        f = file_glyph(0.42, OWN)
        ft = mono(".docker-tag", sz, OWN)
        val = mono(TAG_COMMITTED, sz, INK)
        self.file = VGroup(f, ft, val).arrange(RIGHT, buff=0.18).move_to([-4.0, -1.3, 0])
        self.file.value = val
        self.registry = mono(REGISTRY, sz, S.GREY).move_to([0, -2.3, 0])
        self.add(self.stamp_chip, self.images, self.ecr, self.file, self.registry)
        self.clips = {}

    def stamp(self, scene, run_time: float = 0.7):
        c = tag_card(self.tag_text, OWN, self.size)
        if self.mode == "build":
            c.next_to(self.stamp_chip, DOWN, buff=0.35)
            src = self.stamp_chip
        else:
            c.next_to(self.stations["runner"], UP, buff=0.12)
            src = self.stations["runner"]
        scene.play(FadeIn(c, shift=DOWN * 0.3, scale=0.8), Indicate(src, color=OWN, scale_factor=1.04), run_time=run_time)
        self.card = c
        self.keep(scene, c)
        return c

    def clip(self, scene, i: int, run_time: float = 0.6):
        im = self.images[i]
        mini = mono(":<tag>", self.size, OWN)
        mini.next_to(im, RIGHT, buff=0.08)
        src = self.card.copy()
        scene.play(ReplacementTransform(src, mini), run_time=run_time)
        self.clips[i] = mini
        self.keep(scene, mini)
        return mini

    def push(self, scene, i: int, run_time: float = 0.8):
        if i not in self.clips:
            self.clip(scene, i)
        g = VGroup(self.images[i], self.clips[i])
        sh = self.shelves[i]
        tgt = g.copy().next_to(sh.board, UP, buff=0.04).align_to(sh.board, LEFT).shift(RIGHT * 0.1)
        scene.play(g.animate.move_to(tgt), run_time=run_time)
        scene.add(self)

    def push_all(self, scene, lag: float = 0.3):
        for i in range(3):
            if i not in self.clips:
                self.clip(scene, i, 0.4)
        for i in range(3):
            self.push(scene, i, 0.6)

    def save(self, scene, text: str | None = None, run_time: float = 0.8):
        old = self.file.value
        s = strike(old, S.GREY)
        new = mono(text or "<your tag>", self.size, OWN).next_to(self.file, DOWN, buff=0.15).align_to(old, LEFT)
        src = self.card.copy()
        scene.play(Create(s), old.animate.set_color(S.GREY), run_time=run_time * 0.4)
        scene.play(ReplacementTransform(src, new), run_time=run_time * 0.6)
        self.keep(scene, s, new)
        self.saved = new
        return new

    # -- deploy mode
    def _deploy_layout(self):
        sz = self.size
        spec = (("runner", ("GitHub runner", "date"), CLOUD), ("env", ("DOCKER_TAG", "in $GITHUB_ENV"), ROUTE),
                ("toolbox", ("toolbox", "-e DOCKER_TAG"), IMAGE), ("ansible", ("ansible-playbook", "docker_tag=…"), TOOL))
        self.stations = {}
        xs = [-4.725, -1.575, 1.575, 4.725]
        for (k, lines, col), x in zip(spec, xs):
            b = label_box(list(lines), col, size=sz, box_w=2.8, mono_font=True)
            b.text[0].set_color(col)
            b.text[1].set_color(S.GREY)
            b.move_to([x, 1.6, 0])
            self.stations[k] = b
        self.st_arrows = VGroup(*[arrow(self.stations[a].get_right(), self.stations[b].get_left(), ROUTE, 3)
                                  for a, b in zip(("runner", "env", "toolbox"), ("env", "toolbox", "ansible"))])
        self.ecr, self.shelves = self._ecr(4.6, 2.4, SHORT_IMAGES, [-3.8, -1.4, 0], boards=False)
        sf = box(5.6, 2.4, CLOUD, fill_opacity=0.06).move_to([3.3, -1.4, 0])
        st = label("EC2 server", sz, CLOUD).move_to(sf.get_top() + DOWN * 0.28)
        self.containers = VGroup(*[crate(n, box_w=1.65, box_h=0.75, size=sz, sub=":old") for n in ("frontend", "api", "vector-db")])
        self.containers.arrange(RIGHT, buff=0.15).move_to(sf.get_center() + DOWN * 0.2)
        self.server = VGroup(sf, st, self.containers)
        self.server.frame, self.server.text = sf, st
        self.add(*self.stations.values(), self.st_arrows, self.ecr, self.server)

    def ride(self, scene, per: float = 0.6):
        for k in ("env", "toolbox", "ansible"):
            tgt = self.card.copy().next_to(self.stations[k], UP, buff=0.12)
            scene.play(self.card.animate.move_to(tgt), Indicate(self.stations[k].text[0], color=OWN), run_time=per)

    def pull(self, scene, run_time: float = 0.9):
        arrows = VGroup(*[route(self.shelves[i].get_right() + RIGHT * 0.2, self.containers[i].get_top(), arc=-0.4, stroke=3)
                          for i in range(3)])
        scene.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2), run_time=run_time)
        self.pulls = arrows
        self.keep(scene, arrows)
        return arrows

    def recreate(self, scene, i: int | None = None, gap_chip: bool = True, run_time: float = 1.2):
        idx = range(3) if i is None else [i]
        for j in idx:
            c = self.containers[j]
            ghost = outline_box(c.frame.width, c.frame.height, S.GREY).move_to(c)
            new = crate(("frontend", "api", "vector-db")[j], box_w=1.65, box_h=0.75, size=self.size, sub=":new").move_to(c)
            new.sub.set_color(OWN)
            anims = [FadeOut(c), FadeIn(ghost)]
            ch = None
            if gap_chip and j == idx[0]:
                ch = grey_chip("short gap", self.size).next_to(self.server.frame, DOWN, buff=0.1)
                anims.append(FadeIn(ch))
            scene.play(*anims, run_time=run_time * 0.4)
            scene.wait(run_time * 0.15)
            scene.play(FadeOut(ghost), FadeIn(new, scale=1.1), run_time=run_time * 0.45)
            self._gone(scene, c, ghost)
            self.containers.submobjects.insert(j, new)
            if ch is not None:
                self.add(ch)
            self._reseat(scene)


# ================================================================== V7 · one server, one front door
_SLOTS = {"nginx": (-1.85, -0.55), "frontend": (0.25, 1.1), "api": (0.25, -0.55),
          "vectordb": (2.3, -0.55), "loader": (2.3, 1.1)}


class CostDial(VGroup):
    """A GOLD dial whose needle sweeps while the server exists, with no digits (no price).
    .run(scene, turns, secs) · .freeze(). .tracker"""

    def __init__(self, radius: float = 0.45, caption: str | None = "cost", **kw):
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
        if caption:
            self.caption = label(caption, CAPTION, COST).next_to(face, DOWN, buff=0.1)
            self.add(self.caption)

    def run(self, scene, turns: float = 0.5, seconds: float = 2.0):
        scene.play(self.tracker.animate(rate_func=linear).increment_value(turns), run_time=seconds)

    def freeze(self):
        self.needle.clear_updaters()
        return self


class VmLayout(Piece):
    """V7: the EC2 server. Box x -3.0 .. 4.0, y -2.3 .. 2.1 (7.0 x 4.4, centred at (0.5, -0.1)),
    title 'EC2 · t2.large · cheese-app-demo' (top left inside). Built EMPTY (frame + title); reveal:
    wall(scene) the security group: a thick BLUE wall on the left edge with three ORANGE doors 22, 80,
    443 (y 1.0 / 0 / -1.0) and an ORANGE '0.0.0.0/0' chip outside; engine(scene) a GREY 'Docker'
    label (top right inside); disk(scene) the GREEN '/mnt/disk-1' band (y -1.9) with slots
    'persistent', 'chromadb' (y -1.9); network(scene) the PINK 'appnetwork' line (y 0.3, label under its left end); container(scene, key,
    chip=None) a TEAL box (1.9 x 1.0: name + port, mono 20) at its slot: 'nginx' (-1.85, -0.55),
    'frontend' (0.25, 1.1), 'api' (0.25, -0.55), 'vectordb' (2.3, -0.55), 'loader' (2.3, 1.1).
    PLAYS version(scene, key, text, colour) (chip under the container; replaces the last one) ·
    request(scene, src, dst, path, result, ok) (the chip rides between the two containers, then turns
    into the coloured answer, kept as .answer) · loader_run(scene) · route(scene, path, cut=None,
    dst='api') (a PINK request from outside through door 80 to nginx; `cut` falls away RED; the rest
    goes to dst) · door(scene, port, state) ('open' ORANGE, 'used' GREEN, 'shut' GREY, 'idle') ·
    recreate(scene, key) · meter(scene) (the GOLD CostDial right of the box) · meter_run(scene,
    turns, secs) · badge_on(scene, target, text, colour=TURN) (a tag on a container / 'box' / 'disk'
    / 'wall'; returns it; drop it yourself) · ports_inside(scene) (':3000 :8000 :9000' painted on
    the inner wall, no hole). ssh_arrow(start) -> a PINK arrow from `start` to door 22 (a mobject).
    .frame .title .doors{port} .sg (the wall) .slots{key} .containers{key} .disk_box .net .dial .ip_chip"""

    def __init__(self, size: float = 20, title: str = "EC2 · t2.large · cheese-app-demo", **kw):
        super().__init__(**kw)
        self.size = size
        self.frame = box(7.0, 4.4, CLOUD, fill_opacity=0.05).move_to([0.5, -0.1, 0])
        self.title = label(title, size, CLOUD)
        self.title.move_to(self.frame.get_corner(UL) + np.array([0, -0.3, 0])).align_to(self.frame, LEFT).shift(RIGHT * 0.3)
        self.add(self.frame, self.title)
        self.slots = {k: np.array([x, y, 0]) for k, (x, y) in _SLOTS.items()}
        self.containers, self.doors, self.ver = {}, {}, {}
        self.sg = self.disk_box = self.net = self.dial = self.ip_chip = None

    def _o(self):
        """Offset of the piece (its frame centre minus the design centre)."""
        return self.frame.get_center() - np.array([0.5, -0.1, 0])

    def wall(self, scene, run_time: float = 0.8):
        o = self._o()
        x = self.frame.get_left()[0]
        wl = Line([x, self.frame.get_top()[1], 0], [x, self.frame.get_bottom()[1], 0], color=CLOUD, stroke_width=9)
        doors = VGroup()
        for port, y in zip(SG_PORTS, (1.0, 0.0, -1.0)):
            d = door_glyph(str(port), SHARED, 0.6, self.size)
            d.frame.move_to([x, y + o[1], 0])
            d[1].move_to(d.frame.get_right() + LEFT * 0.08)
            d.text.next_to(d.frame, LEFT, buff=0.1)
            self.doors[port] = d
            doors.add(d)
        cidr = shared_chip("0.0.0.0/0", self.size, mono_font=True)
        cidr.next_to(doors, LEFT, buff=0.15).set_y(1.75 + o[1])
        sg = label("security group", self.size, S.GREY).next_to(cidr, DOWN, buff=0.12).align_to(cidr, RIGHT)
        self.sg = VGroup(wl, doors, cidr, sg)
        self.sg.line, self.sg.cidr = wl, cidr
        scene.play(Create(wl), LaggedStart(*[FadeIn(d) for d in doors], lag_ratio=0.2), FadeIn(cidr), FadeIn(sg),
                   run_time=run_time)
        self.keep(scene, self.sg)
        return self.sg

    def engine(self, scene, run_time: float = 0.4):
        t = label("Docker", self.size, S.GREY)
        t.move_to(self.frame.get_corner(UR) + np.array([0, -0.3, 0])).align_to(self.frame, RIGHT).shift(LEFT * 0.3)
        scene.play(FadeIn(t), run_time=run_time)
        self.engine_label = t
        self.keep(scene, t)
        return t

    def disk(self, scene, run_time: float = 0.6):
        o = self._o()
        t = mono("/mnt/disk-1", self.size, OWN)
        f1 = VGroup(folder_glyph(0.22, OWN), mono("persistent", self.size, INK)).arrange(RIGHT, buff=0.08)
        f2 = VGroup(folder_glyph(0.22, OWN), mono("chromadb", self.size, INK)).arrange(RIGHT, buff=0.08)
        fs = VGroup(f1, f2).arrange(RIGHT, buff=0.25)
        row = VGroup(t, fs).arrange(RIGHT, buff=0.3)
        fr = box(row.width + 0.4, 0.6, OWN, fill_opacity=0.12)
        fr.move_to([self.frame.get_x() + 0.1, -1.9 + o[1], 0])
        row.move_to(fr)
        self.disk_box = VGroup(fr, t, fs)
        self.disk_box.frame, self.disk_box.folders = fr, {"persistent": f1, "chromadb": f2}
        scene.play(FadeIn(fr), FadeIn(t), run_time=run_time * 0.6)
        scene.play(FadeIn(fs), run_time=run_time * 0.4)
        self.keep(scene, self.disk_box)
        return self.disk_box

    def network(self, scene, run_time: float = 0.6):
        o = self._o()
        ln = Line(np.array([-2.6, 0.32, 0]) + o, np.array([3.7, 0.32, 0]) + o, color=ROUTE, stroke_width=3)
        t = mono("appnetwork", self.size, ROUTE).next_to(ln.get_start(), DOWN, buff=0.06).align_to(ln, LEFT)
        self.net = VGroup(ln, t)
        self.net.line, self.net.text = ln, t
        scene.play(Create(ln), FadeIn(t), run_time=run_time)
        self.keep(scene, self.net)
        return self.net

    def _box(self, key, sub=None):
        name, port = CONTAINERS[key]
        return crate(name, box_w=1.9, box_h=0.9, size=self.size, sub=sub or port)

    def container(self, scene, key: str, chip: str | None = None, run_time: float = 0.5):
        c = self._box(key).move_to(self.slots[key] + self._o())
        scene.play(FadeIn(c, scale=0.9), run_time=run_time)
        self.containers[key] = c
        self.keep(scene, c)
        if chip:
            self.version(scene, key, chip)
        return c

    def version(self, scene, key: str, text: str, color=SHARED, run_time: float = 0.5):
        c = chip(text, color, size=self.size, font=MONO).next_to(self.containers[key], DOWN, buff=0.06)
        if key in self.ver:
            old = self.ver[key]
            c.move_to(old)
            scene.play(FadeOut(old, shift=UP * 0.15), FadeIn(c, shift=UP * 0.15), run_time=run_time)
            self._gone(scene, old)
        else:
            scene.play(FadeIn(c, shift=UP * 0.1), run_time=run_time)
        self.ver[key] = c
        self.keep(scene, c)
        return c

    def request(self, scene, src: str, dst: str, path: str, result: str, ok: bool, run_time: float = 1.4):
        a, b = self.containers[src], self.containers[dst]
        q = route_chip(path, self.size)
        mid = (a.get_center() + b.get_center()) / 2
        q.move_to(mid)
        q.shift(RIGHT * min(0.0, self.frame.get_right()[0] - 0.1 - q.get_right()[0]))
        start = q.get_center() + (a.get_center() - mid) * 0.5
        q.move_to(start)
        scene.play(FadeIn(q, scale=0.8), run_time=run_time * 0.15)
        scene.play(q.animate.move_to(start + (b.get_center() - a.get_center()) * 0.5), run_time=run_time * 0.35)
        col = PASS if ok else ERR
        ans = chip(result, col, size=self.size, font=MONO).move_to(q)
        scene.play(ReplacementTransform(q, ans), run_time=run_time * 0.2)
        scene.play(ans.animate.move_to(start), run_time=run_time * 0.3)
        self.answer = ans
        self.keep(scene, ans)
        return ans

    def loader_run(self, scene, run_time: float = 2.0):
        if "loader" not in self.containers:
            self.container(scene, "loader", run_time=0.4)
        ld, vd = self.containers["loader"], self.containers["vectordb"]
        ar = route(ld.get_bottom(), vd.get_top(), stroke=3)
        scene.play(GrowArrow(ar), run_time=run_time * 0.3)
        anims = [Indicate(vd.text, color=ROUTE)]
        if self.disk_box is not None:
            anims.append(Indicate(self.disk_box.folders["chromadb"], color=OWN))
        scene.play(*anims, run_time=run_time * 0.35)
        scene.play(FadeOut(ar), FadeOut(ld), run_time=run_time * 0.35)
        self._gone(scene, ar, ld)
        del self.containers["loader"]

    def door(self, scene, port: int, state: str = "used", run_time: float = 0.4):
        d = self.doors[port]
        col = {"open": SHARED, "used": PASS, "shut": S.GREY, "idle": SHARED}[state]
        op = {"open": 0.15, "used": 0.5, "shut": 0.0, "idle": 0.15}[state]
        scene.play(d.frame.animate.set_stroke(col).set_fill(col, op), d.text.animate.set_color(col), run_time=run_time)

    def route(self, scene, path: str = "/api/newsletters", cut: str | None = "/api", dst: str = "api",
              run_time: float = 2.4):
        d80, ng = self.doors[80], self.containers["nginx"]
        q = route_chip(path, self.size)
        q.next_to(d80.text, LEFT, buff=0.2)
        if q.get_left()[0] < -6.5:
            q.shift(RIGHT * (-6.5 - q.get_left()[0]) + UP * 0.5)
        scene.play(FadeIn(q, shift=RIGHT * 0.3), run_time=run_time * 0.15)
        scene.play(q.animate.move_to(ng.get_left() + RIGHT * q.width / 2 + UP * 0.6), run_time=run_time * 0.25)
        rest = path[len(cut):] if cut and path.startswith(cut) else path
        if cut and path.startswith(cut):
            gone = err_chip(cut, self.size, mono_font=True).move_to(q).align_to(q, LEFT)
            keep_ = route_chip(rest, self.size).move_to(q).align_to(q, RIGHT)
            pair = VGroup(gone, keep_)
            scene.play(ReplacementTransform(q, pair), run_time=run_time * 0.15)
            scene.remove(pair)
            scene.add(gone, keep_)
            scene.play(gone.animate.shift(DOWN * 0.8).set_opacity(0), run_time=run_time * 0.15)
            scene.remove(gone)
            q = keep_
        tgt = self.containers[dst]
        scene.play(q.animate.move_to(tgt.get_top() + UP * 0.25), run_time=run_time * 0.3)
        self.req = q
        self.keep(scene, q)
        return q

    def recreate(self, scene, key: str, run_time: float = 1.0):
        c = self.containers[key]
        ghost = outline_box(c.frame.width, c.frame.height, S.GREY).move_to(c)
        new = self._box(key).move_to(c)
        scene.play(FadeOut(c), FadeIn(ghost), run_time=run_time * 0.4)
        scene.play(FadeOut(ghost), FadeIn(new, scale=1.1), run_time=run_time * 0.6)
        self._gone(scene, c, ghost)
        self.containers[key] = new
        self.keep(scene, new)
        return new

    def meter(self, scene, run_time: float = 0.5):
        d = CostDial(0.42, "cost")
        d.next_to(self.frame, RIGHT, buff=0.3).align_to(self.frame, UP)
        scene.play(FadeIn(d), run_time=run_time)
        self.dial = d
        self.keep(scene, d)
        return d

    def meter_run(self, scene, turns: float = 0.5, seconds: float = 2.0):
        if self.dial is None:
            self.meter(scene)
        self.dial.run(scene, turns, seconds)

    def ports_inside(self, scene, run_time: float = 0.5):
        x = self.frame.get_left()[0] + 0.4
        t = VGroup(*[mono(p, self.size, S.GREY) for p in (":3000", ":8000", ":9000")]).arrange(DOWN, buff=0.02)
        t.move_to([x + t.width / 2, self.slots["frontend"][1] + self._o()[1] + 0.05, 0])
        scene.play(FadeIn(t), run_time=run_time)
        self.inner_ports = t
        self.keep(scene, t)
        return t

    def badge_on(self, scene, target: str, text: str, color=TURN, run_time: float = 0.4):
        m = {"box": self.frame, "disk": self.disk_box, "wall": self.sg}.get(target)
        if m is None:
            m = self.containers[target]
        t = tag(text, color)
        t.move_to(m.get_top() + UP * 0.05)
        if target == "box":
            t.move_to(self.frame.get_top())
        scene.play(FadeIn(t, shift=DOWN * 0.1), run_time=run_time)
        return t

    def ssh_arrow(self, start) -> VMobject:
        return route(start, self.doors[22].frame.get_left() if self.doors else self.frame.get_left(), arc=-0.2, stroke=3)


# ================================================================== V8 · the release loop
LOOP_KEYS = ("codebase", "build", "test", "release", "deploy", "monitor")
LOOP_NAMES = {"codebase": "Codebase", "build": "Build", "test": "Test", "release": "Release",
              "deploy": "Deploy", "monitor": "Monitor"}


class ReleaseLoop(Piece):
    """V8 (S11, S14, S16): slide 7's loop: a row of boxes (y 0.9) Codebase → Build → Test → Deploy →
    Monitor (5 boxes, x -4.4 .. 6.4 evenly; with release=True or after add_release(): six, Release
    between Test and Deploy); 'Developers' bottom left (-5.6, -1.4) with a PINK 'Commits' arrow up into
    Codebase; dashed PINK notification lines from each box after Codebase down to a GREY
    'Notifications' bar (y -1.4); brackets 'CI' over Codebase..Test and 'CD' over the rest (y 1.75).
    ~12.6 x 4.6.
    PLAYS add_release(scene) · go_around(scene, colour=ROUTE) (a dot runs the row) · this_repo(scene)
    (Codebase, Build, Release, Deploy light BLUE; Test becomes a GREY dashed outline + chip 'L21';
    Monitor chip 'the run's color + your own check'; Release chip 'tagged images land in ECR') ·
    ms5(scene) (Test solid GREEN + chip 'L21 tests') · chip(scene, key, text, colour) (under the box;
    replaced per key). ANIM light(key, colour). .boxes{key} .devs .notify .brackets .commits .chips"""

    def __init__(self, release: bool = False, size: float = 20, **kw):
        super().__init__(**kw)
        self.size = size
        self.has_release = release
        self.boxes = {k: self._box(k) for k in LOOP_KEYS}
        icons = VGroup(person_icon(LAPTOP, 0.42), person_icon(LAPTOP, 0.42)).arrange(RIGHT, buff=0.1)
        self.devs = VGroup(icons, label("Developers", size, LAPTOP)).arrange(DOWN, buff=0.08).move_to([-5.55, -1.45, 0])
        self.chips = {}
        self._place(self._keys())
        self.decor = self._decor()
        self.add(*[self.boxes[k] for k in self._keys()], self.devs, self.decor)

    def _keys(self):
        return [k for k in LOOP_KEYS if k != "release" or self.has_release]

    def _box(self, k):
        b = label_box(LOOP_NAMES[k], INK, size=self.size, box_w=1.55, fill_opacity=0.06)
        b.key = k
        return b

    def _o(self):
        return self.devs.get_center() - np.array([-5.55, -1.45, 0])

    def _positions(self, keys):
        n = len(keys)
        xs = np.linspace(-4.5, 5.6, n)
        o = self._o()
        return {k: np.array([x, 0.9, 0]) + o for k, x in zip(keys, xs)}

    def _place(self, keys):
        for k, p in self._positions(keys).items():
            self.boxes[k].move_to(p)

    def _decor(self, keys=None):
        keys = keys or self._keys()
        pos = self._positions(keys)
        bw, bh = 1.55, self.boxes["codebase"].height
        arrows = VGroup(*[Arrow(pos[a] + RIGHT * bw / 2, pos[b] + LEFT * bw / 2, buff=0.06, color=S.GREY,
                                stroke_width=2.5, tip_length=0.15, max_tip_length_to_length_ratio=0.3)
                          for a, b in zip(keys, keys[1:])])
        bar_l, bar_r = pos[keys[1]][0] - bw / 2, pos[keys[-1]][0] + bw / 2
        bar = RoundedRectangle(width=bar_r - bar_l, height=0.5, corner_radius=0.1, stroke_color=S.GREY,
                               stroke_width=2.5).set_fill(S.GREY, 0.1).move_to([(bar_l + bar_r) / 2, self.devs.get_y(), 0])
        nt = label("Notifications", self.size, S.GREY).move_to(bar).align_to(bar, LEFT).shift(RIGHT * 0.2)
        drops = VGroup(*[DashedLine(pos[k] + DOWN * bh / 2, [pos[k][0], bar.get_top()[1], 0], color=ROUTE,
                                    stroke_width=2.5, dash_length=0.1) for k in keys[1:]])
        back = DashedLine(bar.get_left(), [self.devs.get_right()[0] + 0.05, bar.get_y(), 0], color=ROUTE, stroke_width=2.5,
                          dash_length=0.1)
        c_from = self.devs.get_top() + UP * 0.05
        c_to = pos["codebase"] + DOWN * bh / 2
        yb = pos["codebase"][1]
        cpath = VMobject().set_points_as_corners([c_from, [c_from[0], yb, 0], [pos["codebase"][0] - bw / 2, yb, 0]])
        cpath.set_stroke(ROUTE, 3.5)
        tip = Arrow([pos["codebase"][0] - bw / 2 - 0.35, yb, 0], [pos["codebase"][0] - bw / 2, yb, 0], buff=0,
                    color=ROUTE, stroke_width=3.5, tip_length=0.16, max_tip_length_to_length_ratio=0.6)
        del c_to
        ct = label("Commits", self.size, ROUTE).next_to(cpath, RIGHT, buff=0.1).set_y((c_from[1] + yb) / 2)
        ci_keys = keys[:3]
        cd_keys = keys[3:]
        top = pos["codebase"][1] + bh / 2 + 0.12

        def brk(ks, text):
            l_, r_ = pos[ks[0]][0] - bw / 2, pos[ks[-1]][0] + bw / 2
            ln = VMobject().set_points_as_corners([[l_, top, 0], [l_, top + 0.15, 0], [r_, top + 0.15, 0], [r_, top, 0]])
            ln.set_stroke(S.GREY, 2.5)
            t = label(text, self.size, S.GREY).move_to([(l_ + r_) / 2, top + 0.42, 0])
            return VGroup(ln, t)

        brackets = VGroup(brk(ci_keys, "CI"), brk(cd_keys, "CD"))
        g = VGroup(arrows, bar, nt, drops, back, cpath, tip, ct, brackets)
        g.arrows, g.bar, g.drops, g.brackets, g.commits = arrows, bar, drops, brackets, VGroup(cpath, tip, ct)
        g.cpath = cpath
        return g

    @property
    def notify(self):
        return VGroup(self.decor.bar, self.decor[2])

    @property
    def brackets(self):
        return self.decor.brackets

    @property
    def commits(self):
        return self.decor.commits

    def light(self, key: str, color=TURN, run_time: float = 0.6):
        b = self.boxes[key]
        return AnimationGroup(Circumscribe(b, color=color, buff=0.06), Indicate(b.text, color=color, scale_factor=1.06),
                              run_time=run_time)

    def add_release(self, scene, run_time: float = 1.0):
        if self.has_release:
            return self.boxes["release"]
        self.has_release = True
        keys = self._keys()
        pos = self._positions(keys)
        r = self.boxes["release"].move_to(pos["release"] + UP * 1.4)
        new_decor = self._decor(keys)
        anims = [self.boxes[k].animate.move_to(pos[k]) for k in keys if k != "release"]
        for k, c in self.chips.items():
            anims.append(c.animate.shift(pos[k] - self.boxes[k].get_center()))
        anims.append(Transform(self.decor, new_decor))
        scene.play(*anims, run_time=run_time * 0.6)
        scene.play(r.animate.move_to(pos["release"]), run_time=run_time * 0.4)
        self.keep(scene, r)
        return r

    def go_around(self, scene, color=ROUTE, run_time: float = 2.5):
        d = dot(color).move_to(self.decor.cpath.get_start())
        scene.play(FadeIn(d), run_time=0.2)
        scene.play(MoveAlongPath(d, self.decor.cpath.copy()), run_time=run_time * 0.3)
        keys = self._keys()
        per = run_time * 0.6 / len(keys)
        for k in keys:
            scene.play(d.animate.move_to(self.boxes[k].get_top() + UP * 0.12), run_time=per)
        scene.play(FadeOut(d), run_time=0.2)
        scene.remove(d)

    def chip(self, scene, key: str, text: str, color=S.GREY, run_time: float = 0.4, dashed: bool = False,
             level: int = 0):
        c = (dashed_chip(text, color, self.size) if dashed else chip(text, color, size=self.size))
        c.next_to(self.boxes[key], DOWN, buff=0.15 + level * 0.48)
        if c.get_right()[0] > 6.5:
            c.shift(LEFT * (c.get_right()[0] - 6.5))
        if key in self.chips:
            old = self.chips[key]
            c.move_to(old) if level == 0 else None
            scene.play(Transform(old, c), run_time=run_time)
            return old
        scene.play(FadeIn(c, shift=UP * 0.1), run_time=run_time)
        self.chips[key] = c
        self.keep(scene, c)
        return c

    def _set_box(self, key, color, dashed=False, fill=0.15):
        b = self.boxes[key]
        if dashed:
            fr = outline_box(b.frame.width, b.frame.height, color).move_to(b.frame)
        else:
            fr = box(b.frame.width, b.frame.height, color, fill_opacity=fill).move_to(b.frame)
        return [Transform(b.frame, fr), b.text.animate.set_color(S.GREY if dashed else INK)]

    def this_repo(self, scene, run_time: float = 1.2):
        self.add_release(scene) if not self.has_release else None
        anims = []
        for k in ("codebase", "build", "release", "deploy"):
            anims += self._set_box(k, CLOUD)
        anims += self._set_box("test", S.GREY, dashed=True)
        scene.play(*anims, run_time=run_time * 0.5)
        self.chip(scene, "test", "L21", S.GREY, dashed=True)
        self.chip(scene, "release", "tagged images land in ECR", CLOUD, level=1)
        self.chip(scene, "monitor", "the run's color + your own check", S.GREY, level=2)

    def ms5(self, scene, run_time: float = 0.8):
        scene.play(*self._set_box("test", PASS, fill=0.2), run_time=run_time * 0.6)
        self.chip(scene, "test", "L21 tests", PASS)


class ReleaseToggle(Piece):
    """V8's toggle (slide 12): a conveyor belt (x -4.6 .. 2.2, y 0) carrying three code cards; at its
    right end either the RED RELEASE button with a GREY hand above it (delivery) or the GREEN 'auto'
    ring (deployment). ~10 x 2.6. Built with the belt and cards only.
    PLAYS delivery(scene) · deployment(scene) (button + hand swap for the ring; the cards stream
    off the end) · ends(scene) (button+hand and ring side by side, no names) · hover_ribbon(scene,
    text=KEYWORD) (a PINK ribbon above the two ends) · into_hand(scene) (the ribbon drops into the
    hand; the button pulses) · label_end(scene, text, at='button'|'ring') (a 20 pt label under that end).
    .belt .cards .button .hand .ring .names"""

    def __init__(self, size: float = 20, **kw):
        super().__init__(**kw)
        self.size = size
        belt = VGroup(Line([-4.6, -0.35, 0], [2.2, -0.35, 0], color=S.GREY, stroke_width=4),
                      *[Circle(radius=0.14, stroke_color=S.GREY, stroke_width=2.5).move_to([x, -0.55, 0])
                        for x in np.linspace(-4.4, 2.0, 7)])
        self.belt = belt
        self.cards = VGroup(*[self._card() for _ in range(3)]).arrange(RIGHT, buff=0.7)
        self.cards.move_to([-2.0, 0.05, 0])
        self.button = release_button(self.size).move_to([3.4, -0.2, 0])
        self.hand = hand_glyph(1.0).next_to(self.button, UP, buff=0.08)
        self.ring = auto_ring(0.45, PASS, self.size).move_to([3.4, -0.1, 0])
        self.names = VGroup()
        self.mode = None
        self.add(belt, self.cards)

    def _card(self):
        fr = RoundedRectangle(width=0.7, height=0.55, corner_radius=0.06, stroke_color=INK,
                              stroke_width=2).set_fill(PANEL, 1)
        ls = VGroup(*[Line(LEFT * 0.22, RIGHT * 0.22, color=S.GREY, stroke_width=2) for _ in range(3)]).arrange(DOWN, buff=0.08)
        ls.move_to(fr)
        return VGroup(fr, ls)

    def delivery(self, scene, run_time: float = 0.8):
        scene.play(FadeIn(self.button, scale=0.8), FadeIn(self.hand, shift=DOWN * 0.2), run_time=run_time)
        self.keep(scene, self.button, self.hand)
        self.mode = "delivery"

    def deployment(self, scene, run_time: float = 1.6):
        anims = [FadeIn(self.ring)]
        gone = [m for m in (self.button, self.hand) if m in self.submobjects]
        anims += [FadeOut(m) for m in gone]
        scene.play(*anims, run_time=run_time * 0.35)
        self._gone(scene, *gone)
        self.keep(scene, self.ring)
        scene.play(self.cards.animate.shift(RIGHT * 1.6), Rotate_safe(self.ring.ring), run_time=run_time * 0.65)
        self.mode = "deployment"

    def ends(self, scene, run_time: float = 0.6):
        self.button.move_to([3.1, -0.2, 0])
        self.hand.next_to(self.button, UP, buff=0.08)
        self.ring.move_to([5.2, -0.1, 0])
        scene.play(FadeIn(self.button), FadeIn(self.hand), FadeIn(self.ring), run_time=run_time)
        self.keep(scene, self.button, self.hand, self.ring)

    def hover_ribbon(self, scene, text: str = KEYWORD, run_time: float = 0.5):
        r = ribbon(text, ROUTE, self.size)
        r.move_to([(self.button.get_x() + (self.ring.get_x() if self.ring in self.submobjects else self.button.get_x())) / 2, 1.6, 0])
        scene.play(FadeIn(r, shift=DOWN * 0.2), run_time=run_time)
        self.rib = r
        self.keep(scene, r)
        return r

    def into_hand(self, scene, run_time: float = 0.8):
        r = self.rib
        scene.play(r.animate.next_to(self.hand, UP, buff=0.08), run_time=run_time * 0.6)
        scene.play(Indicate(self.button.text, color=INK), self.button.frame.animate(rate_func=there_and_back).set_fill(ERR, 0.9),
                   run_time=run_time * 0.4)

    def label_end(self, scene, text: str, at: str = "button", run_time: float = 0.4):
        target = self.button if at == "button" else self.ring
        t = label(text, self.size, INK).next_to(target, DOWN, buff=0.25)
        scene.play(FadeIn(t), run_time=run_time)
        self.names.add(t)
        self.keep(scene, t)
        return t


def Rotate_safe(mob, angle: float = -TAU / 3):
    from manim import Rotate
    return Rotate(mob, angle=angle)
