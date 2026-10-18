"""Shared code for AC215 L4 (Containers II-b: build or pull, ports and Compose): paths, narration,
the semantic colours of BRIEF.md, the README trackers, loaders for the real captures in assets/,
terminal / panel / card helpers, and the video's recurring pictures V1-V8 of BRIEF.md.
Tested on screen by build/common_test.py (explainer.check / explainer.preview: clean).

Notes for scene authors
=======================

    from common import *      # every scene: SAY = NARRATION["S07"]; assert len(SAY) == n;
                              # one `with self.voiceover(SAY[i]) as vo:` per SAY line, in order
Everything below draws text at 20-22 pt. Never .scale() a group that holds text below 1.0: use
piece.rescale(k) (shapes shrink, text keeps its size). Frame budget: the tracker band is y 2.92..3.5
(x -6.5..-0.1 at most); a 3-row strip's top is STRIP_TOP (-1.44), so a picture above a strip has
y -1.3..2.8 (4.1 tall); a 6-row terminal's top is strip_top(6) (-0.2); keep x in [-6.6, 6.6].

Data and sources
    NARRATION["S01"] ... ["S16"]   SAY lines from script.md (all 16 load)
    TITLES[cls], SPEC              scene titles / video.yaml
    capture(name, folder) -> Capture       assets/terminal/<folder>/<name>.txt; name may be the
        number alone ("12" -> 12-a-docker-shell.txt, never the .plain logs unless you name them:
        "12-a-docker-shell.plain"), or "folder/name" as one argument. Tabs are expanded (8).
        Folders: mega-laptop, mega-l03-laptop, mega-transcribe_audio, mega-generate_text,
        mega-synthesis_audio_en, mega-translate_text, mega-synthesis_audio, gcloud-laptop,
        port-laptop, expected (line 1 '#' header; mega-*: line 2 '$', output from 3; port_toy-*:
        output from 2). capture-only/ is plumbing: never shown.
        .cmd (the `$` line without "$ ") .lines (output) .exit .first (file line of .lines[0])
        .line(n) one FILE line   .at(9, (11, 12), "…", 52)  lines BY FILE LINE NUMBER, "…" inserted
        .join(64, 65) two terminal-wrapped lines joined   .typed(n) the command on prompt line n
        .json(n) parse a JSON reply line (port-laptop/14 line 2)   .pick() L1-compatible (= file line - 1)
    source_text(path)  excerpt(path, a, b, cut_comments=False)   files in assets/source
        (paths start with mega-pipeline/, mega-pipeline-main/, mega-pipeline-pipenv-flexible-workflow/,
        port_toy/). cut_comment(line): a line > 65 chars loses its trailing comment, shown "# …".
    build_row(row) -> (text, time|None)   a BuildKit live row cut at 65 + its time field ("44.7s")
    column_view(lines, ("IMAGE", "DISK USAGE"))   docker images rows sliced to those columns
    split_prompt(line) -> (prompt, cmd) | None   for session captures

Colours (BRIEF.md, binding)
    LAPTOP GREY · CLOUD (= HUB) BLUE · CTR (= IMAGE) TEAL · SYSTEM ORANGE · VENV (= GIT_OWNED)
    GREEN · TOOL PURPLE · ERR RED · TURN YELLOW · COST (= KEY) GOLD · LOOKUP PINK · INK white
Running example
    P_HOME P_WS P_REPO p_comp(c) P_L03 P_L03_REPO p_l03(c) P_TOY   (laptop prompts)
    CTR_PROMPT[component] P_RUN_LOCAL P_STALE P_SH="#"              (container prompts)
    COMPONENTS (5 folders, README order)  VALUES (placeholders)  GROUP "group-01"
    PREFIXES (README.md:152-158, 7 drawers; the last is the bonus)

README tracker (top-left, YELLOW)
    tracker(key, step=None)   keys F L B K R QA QB QC QD QE Y U (mega-pipeline) and
        P0 P1 P2 P3 P4 PH (port_toy: head reads "port_toy README"); SECTIONS[key] = (title, steps)
    self.play(tr.goto(k))     caption_extra(tr, on) -> Transform " · extra"
    tr = switch_section(self, tr, "QB", 1)   old tracker lifts away, new one drops in

Terminal helpers (Terminal from explainer.devops: .type .print .run .clear .find .last)
    term(prompt=P_REPO, rows=12, title="laptop", component=None, top=None)  12.6 wide, 22 pt,
        65 chars a row, bottom at BOTTOM (or its top edge at `top`); component="gateway" or a
        folder: title "container · …", TEAL frame, prompt CTR_PROMPT[...] unless given
    enter_container(t, component, prompt=None) / leave_container(t, prompt) -> list of animations
    resize(scene, t, rows, keep=None, anchor="bottom")   grow/shrink with the bottom (or top)
                             edge fixed; keeps the last lines (or exactly the listed ones)
    bare_prompt(scene, t)    a prompt line with nothing typed (the prompt returns)
    type_cmd(scene, t, cmd)  type at the prompt (replaces a bare prompt line). When prompt +
                             command exceed 65 chars, the command starts on the row under the
                             prompt, indented 4, if it fits there whole or has no early space;
                             otherwise it folds with " \\". Returns the line (or VGroup .rows)
    cd_prompt(scene, t, new_prompt, color=CLOUD)  prompt changes, the new path part flashes
    second_terminal(scene, prompt, rows=7, top=2.75, title=...)  opens on P_HOME, "~" flashes
                             YELLOW + caption "new terminal: cd here first", then shows `prompt`
    session(scene, t, cap, *spec, wrap=False, colors=None)  replay an interactive capture:
                             prompt lines set the prompt and type their command; other lines
                             print (spec as .at). Returns {file line: mobject} (printed lines
                             only when wrap=False)
    print_build(scene, t, rows)  BuildKit rows printed cut at 65; each line gets .time_tag (a GREY
                             tag at the row's right end, part of the row) or None
    beside(mob, t, line) / pin(scene, line, mob) / unpin(scene, line, mob)   a tag that scrolls
                             with its terminal line;  under(mob, color) strike(mob)
    col_box(line, a, b, color=TURN, dashed=False)  box over character columns a..b of a line
                             (works on blank cells: the processor's empty PORTS cell)
    bracket(mobs, text, color=ERR)  a bracket + numbered badge at the terminal's left margin

Panels and cards
    src_panel(path, a, b, cut_comments=False, focus=None, size=22, width=None, shown=None,
              suffix=None, wrap=None, language=None)   code_panel from assets/source with header
              "shown · lines a–b"; shown defaults to the path without its first folder (and
              "pipenv-flexible-workflow · …" / "main · …" for the other branches); wrap={66:
              ["--push", "-f Dockerfile"]} breaks file line 66 before those substrings (↪ rows,
              " · line 66 wrapped"); .bar(file_line, color) -> line bars; .rows_of(file_line)
    log_panel(lines, header, width=12.6)   PANEL: plain mono rows on a dark panel (.rows)
    readme_chip(where, phrase)  one-line README chip (<= 9 wide)   readme_card(where, lines)
    excerpt_chip(sub, header, color=INK, line=None)   exact sub-string chip (checked against `line`)
    cmd_chip(cmd, note=None)    a command shown, not typed     editor_inset(panel, title)
    note(text, color=GREY) GREY caption (20 pt serif)   sans(text) CMU Sans   fix_chip(text)
    turn_card(rows, width=None, header="your turn")  static GREY "your turn" card; rows: a str
              (command, mono; "\\n" for README rows), (cmd, "extra") or (cmd, note), Prose("…");
              the ▶ your turn tag sits on its top-right corner (.tag)
    LookFor(items, title="with your key, look for")  items (text, "cli.py line 44"); frame for
              all rows from the start; self.play(lf.write_item(i))
    card_rows(items, width=None, header=None)  a GREY card of rows: str (serif) or "`mono`" or
              (str, colour); .rows   table_card(headers, rows, col_w)  two/three-column card
    ReplyStrip(text, color=OUTPUT, width=12.6, tag_=True)  REPLY: the captured reply line in a
              GREY strip (wraps at its width, 2 rows for a JSON reply), tag "captured reply ·
              curl stood in for the Send button" above it; .rows .span(sub)
    PortPage(port=8090, reply=None, compact=False, ports=None)  PAGE (illustration tag on its
              top-right): full 6.6 x 4.9 (address bar, input + Send, reply card, port card,
              glyph-only diagram); compact 7.0 x 2.3 (address bar + reply card), compact with
              ports=True 7.0 x 3.6. .fill(reply) -> [anims] (fade in, or numbers transform on
              the next send) .click() -> anim .clear_reply() -> [anims] .value(key) -> the
              mobject of a JSON key (upper, gateway_out_port, listen_port, sender_port)
              page_reply(cap) -> dict (cap.json())
    page_diagram(host_port="8090", out=None, dst=None)  the page's diagram, readable, 10.6 x 2.0;
              .host (the host-port glyphs, to colour YELLOW) .boxes .labels

Tags (22 pt, keep their size in rescale): your_turn() extra_tag() illustration_tag(note=None)
    expected_tag() recorded_tag(s) nokey_tag() erratum_tag(note=None) standin_tag()
    differ_tag() cost_tag(s="your project pays") preview_tag() reply_tag() notrun_tag(s)
    grey_tag(s) build_badge(k) stamp(text, color) cached_stamp() time_tag(t) token_tag()

Glyphs (small, mostly no text; sizes w x h)
    key_glyph(h=0.3, name=None) GOLD key (+ mono name) · key_outline() dashed GOLD outline ·
    clock_glyph() · padlock() (.body .shackle) · toggle(on) API switch 0.56 x 0.3 (.knob) ·
    signpost(lines, color=LOOKUP) PINK board on a post (.board .text .root()) · shelf(caption,
    w, color) · sealed_box(w, color) TEAL box with tape (.front .lid .tape) · recipe_card(files,
    color=VENV, caption=None) GREEN card 2.7 x 1.4 · person(color) teammate 0.5 x 0.7 · pencil()
    · gear() · thought(text) bubble · envelope(text) · keycaps("Ctrl", "C") · machine_glyph()
    · shield(name) · file_row(name) / ghost_file(name) · drawer(label, w) BLUE drawer ·
    loop_glyph(r) a localhost loop · door(w, h, color) · Stopwatch(caption) .sweep(secs)

Set pieces: Piece = VGroup + named parts (as in lecture 3)
    Every piece is built centred at ORIGIN (except ComposeMap, a full-frame layout); move it with
    .move_to(...) before showing it. A part not shown yet is a member at opacity 0: it moves and
    scales with the piece, and the piece's size never jumps. show=(...) in the constructor names
    the parts visible at first. self.play(*piece.parts_in("a", "b")) fades parts in (it returns
    animations; call it inside the play; parts_in("a", anim=Create) draws instead),
    self.play(*piece.parts_out("a")) fades them back to 0 (they stay members); piece.reveal(scene,
    *names) / piece.hide(scene, *names) do the same with their own play. piece.attach(scene, *mobs)
    / detach(scene, *mobs) make scene mobjects members (or not). self.play(piece.dim_to(0.3)) /
    self.play(piece.undim()). Never piece.set_opacity(...), never FadeOut a member (it would snap
    back: FadeOut the whole piece). rescale(k) via self.play(piece.animate.rescale(k).move_to(...)):
    shapes shrink, text keeps its size. piece.glyph_only() -> a text-free copy (thumbnails, icons;
    scale it freely). Methods return ANIMATIONS (play them) or MOBJECTS (not added: FadeIn them;
    "scene-owned" = FadeOut them yourself); geometry is read from members, so it follows moves.

    V1 BuildOrPull(tag_name="dlops/mega-pipeline-transcribe-audio:latest", image_label=
       "Python 3.14.8 · uv", show=ALL)   12.6 x 3.3. Left (.left): GREY shelf "Git" with the GREEN
       recipe card (.card) | PURPLE arrow `docker build` (.build) | GREY laptop (.laptop) holding
       the TEAL image (.image) and its label. Right (.right): BLUE shelf "Docker Hub" + the
       illustration tag, a sealed TEAL box (.box) at its right end, the PINK two-line signpost
       board (.post) above it and its pointer (.pointer) aiming at the box.
       Parts: git, card, build, local, hub, hub_tag, box, post, pointer.
       .teammates(n=3) -> VGroup of person+laptop glyphs under the piece (positioned, not added)
       .build_arrow(target) -> PURPLE Arrow from the card; .pull_arrow(target, src=None) -> BLUE
            Arrow from the box (not added; GrowArrow them)
       .push_box() -> (box2, anim)  a second sealed box rises onto the shelf left of the first
       .aim(target) -> anim  the pointer swings to target (box2, then back to .box)
       .open_box(labels) -> (labels VGroup, [anims])  the lid swings open, the labels rise into a
            column left of the box: [("2025-02-18", INK), ("Python 3.8.17", TURN),
            ("pipenv shell", INK), ("user: root", ERR)] (scene-owned)
       .old_card(files=("Pipfile", "Dockerfile"), caption="branch pipenv-flexible-workflow") ->
            older GREY card on a GREY shelf (not positioned, not added)
       BuildOrPull.dashed_link(a, b, text="?") -> dashed GREY line between two mobjects
       .drop_file(name="Pipfile", badge="root") -> (file, anim)  falls from the box to the laptop
    V2 ThreePiles()   12.6 x 3.6 incl. walls and the waiting files (frames 3.2 wide each).
       Piles (.piles["tracked"|"untracked"|"ignored"]: .frame .kind .folder .rows): tracked GREEN
       transcribe_audio/ cli.py + YELLOW pencil "edited" (.pencil); untracked GREY generate_text/
       Dockerfile, uv.lock; ignored GREY dashed transcribe_audio/ Dockerfile, pyproject.toml,
       uv.lock, secrets/ + GOLD key (.key). A stash column at the right (two boxes, hidden).
       Parts: wall1, wall2 (RED bars + numbered badges above tracked / untracked), incoming (the
       branch's files + "flexible-workflow", waiting above the frame), stash1, stash2, standin.
       .row(pile, name) -> a file row (.glyph .text)
       .slide_in() -> anim  (parts_in("incoming") first) the files slide down, stop at the walls
       .stash(1) -> [anims]  cli.py lifts into stash box 1 (shown), wall 1 falls;
       .stash(2) -> [anims]  the untracked pair lifts into stash box 2, wall 2 falls
       .land() -> [anims]  the branch's files land inside the emptied tracked/untracked frames
       .flip_card(pile, name, color=TURN) -> anim  a file card flips over (replaced silently)
       .relabel(i, "stash@{0}") -> anim  a stash box's label
    V3 ThreeGates(show=("container", "doors", "laptop", "route", "gate1", "gate2", "gate3"))
       12.6 x 3.6. Laptop secrets/ + GOLD key (.key) | PINK route (.route) | container (TEAL) with
       a dashed /secrets slot (.slot) and a `google.auth` stamp (.stamp) | five BLUE API doors
       (API_DOORS: Storage, Speech-to-Text, Vertex AI, Translation, Text-to-Speech), each with a
       dashed lock slot (gate 2; "no role" for Text-to-Speech) and an API switch (gate 3).
       Parts: container, doors, laptop, route, ghost (GOLD key outline in the slot), token,
       gate1 "who?", gate2 "may?", gate3 "switched on?", lock0..lock3 (padlocks: Storage,
       Speech-to-Text, Vertex AI, Translation).
       .pulse() -> anim  the route pulses and the outline appears in the slot at the same instant
       .mint() -> [anims]  the stamp presses the outline into the GOLD token (token shown)
       .fly(i) -> anim  token to the gates of door i;  .home() -> anim  back under the stamp
       .open_door(i, color=VENV) -> anim  door i flashes (the call went through)
       .bounce(i, text="permission error · from Google") -> (chip, [anims])  RED bounce off
            door i's lock; chip under the doors (scene-owned)
       .fail_gate1(text="DefaultCredentialsError", note_="inside the container") -> (chips,
            [anims])  slot flashes RED, the outline vanishes, chips under the container
       .fill_lock(i, src=None) -> anim  padlock i appears (flies from src) in its slot
       .switch(i, on=True) -> anim  .tick("gate1" | ("lock", i) | ("switch", i)) -> white tick
            (positioned, not added)   .lock(i) -> a fresh padlock in slot i (not added)
       .doors[i] (.frame .name .slot .toggle)
    V4 Switchboard(labels=True)   6.6 x 3.1. PURPLE input "first word" and four PURPLE tracks to
       stations (MODES): (no argument) "build, then run" :71–76 + :79–96 · dev "build only"
       :71–76 · run "run only" :79–96 · prod "build two architectures, push" :51–68.
       labels=False: silhouette (parts input_label, words, descs, chips hidden).
       .light(mode, color=TURN) / .unlight(mode) -> anim  (mode: "", "dev", "run", "prod")
       .dim_modes(*modes, k=0.3) / .undim_modes(*modes) -> anim
       .tracks[mode] .stations[mode] (.word .desc .chip .dot)
       RunDecision()  5.9 x 2.0: PINK diamond "local image?" (.diamond); yes (.yes) -> TEAL box
           "local image"; no (.no) -> BLUE shelf "Docker Hub" $DOCKER_USERNAME/….
           .take("yes"|"no", color=TURN) -> anim
    V5 TwoWindows(show=ALL, l03=False)   12.6 x 3.6. Laptop panel (GREY): ~/AC215/ ·
       mega-pipeline/ · transcribe_audio/ · secrets/ + GOLD key (.rows["home"|"repo"|"comp"|
       "secrets"], .key). Container (TEAL): /app (.app) and /secrets (.secrets_area) windows, GREEN
       /home/app/.venv box (.venv_box), PINK signpost /secrets/ mega-pipeline.json pointing into
       /secrets; a TEAL "image" slab under it (.image_slab). l03=True: ~/AC215-l03/ with secrets/
       INSIDE transcribe_audio/ (S09; don't show route_secrets then).
       Parts: laptop, container, venv, route_app, route_secrets, post, ghost (key outline in
       /secrets), image, never ("never in here" across the slab), clock ("docker run").
       .walk() -> (group, [5 anims])  play them in turn: a YELLOW walker climbs ".." and
            "../.." then enters secrets/, and $(pwd)/../../secrets/ writes itself (scene-owned)
       .pulse("secrets"|"app") -> anim  a route pulses; "secrets" also shows the key outline
       .blink("app"|"secrets") -> anim  the folder and its window blink at once (no travel)
       .pack() -> (copies, [anims])  (l03=True) folder, secrets/ and key glyphs ride into the slab
    V6+V7 ToyNet(show=("outline", "laptop_label", "zone", "boxes"), book_lines=(...),
       door_label="127.0.0.1:8090", door2_label="0.0.0.0:8091", rooms=(":9100", ":9200"),
       aim_label="processor : 9200")   12.6 x 2.9 (outline x -5.85..6.3, y -1.5..1.4 before
       moving). Laptop zone at left: browser glyph, the laptop's own localhost loop, a dashed wall
       with the street doors (labels left of them). Docker side: TEAL boxes gateway / processor
       (.boxes[name]: .frame .name .strip .cells .loop .loop_label), each with a room door on
       its LEFT wall (.rooms[name]: .frame .label), a port strip "1 … 65535" and its own
       localhost loop; the TEAL rail toynet (.rail) with plugs (.plugs[name]); the PINK phone
       book between the boxes (.book_lines[0/1]).
       Parts: outline, laptop_label, zone, boxes, rail, rail_label, plug_gateway, plug_processor,
       book, book0, book1, dns_gateway (+ "127.0.0.11"), dns_processor, door, door2, outside
       (machines left of the outline + dashed route to door2), room_gateway, room_processor,
       map (PINK: browser -> along the top -> down the wall -> street door -> the gateway's
       room), aim (dashed gateway -> chip "processor : 9200" on the rail: the destination).
       .cell(box, port) -> strip cell   .light_port(box, port) -> (number, [anims])  the cell
            glows, its number shows under it (scene-owned)   .unlight_port(box, port) -> anim
       .open_room(box, port=None) -> anim  the strip cell becomes the room (TransformFromCopy)
       .packet(dest=None) -> PINK packet at the gateway's plug (scene-owned; .body)
       .travel(packet, "gateway", "processor") -> anim  down to the rail, along, into the room
       .loopback(box) -> (dot, [anims])  a dot circles the box's own loop, which glows YELLOW;
            .unloop(box) -> anim
       .bounce_from_laptop() -> (group, [anim1, anim2])  dashed ":9200 ?" arrow from the
            browser stops at the wall, then turns RED with a cross (scene-owned)
       .set_door(text, which="door") .set_room(box, text) .set_aim(text=None, color) -> anim
       .stop_box(box) / .start_box(box) -> anim (GREY "exited" / TEAL)   .reform(box) -> anim
    V8 ComposeMap(panel="gateway")   full frame, do not move: left (x -6.5..-0.3, top 2.75):
       COMPOSE_CMDS (Step 1's five commands, README spelling) as GREY chips folded at <= 36
       chars (fold_cmd), .chips[i].rows (mono_lines); right (top-right corner): src_panel of
       docker-compose.yml lines 11–25 at 20 pt, comments cut (.panel; "processor": 27–39).
       .flag(i, sub) -> glyphs in chip i   .yaml(line) -> code row of a file line
       .fly(i, sub, line, sub_yaml=None) -> (copy, [anims])  the flag's copy flies to that YAML
            line and fades as the line gets a GREEN bar (kept in .bars)
       .dim_flag(i, sub) -> anim   .swap("processor"|"gateway") -> [anims] (bars leave too)
       .outline(first, last, text) -> VGroup  GREEN outline over YAML lines + tag under the
            panel (not added)   .collapse() -> (chip, [anims])  chips fold into `docker compose up`
    Cabinet(prefixes=PREFIXES, sub="group-01/", title="your-team-bucket", show_subs=False)
       BLUE cabinet 5.9 x 3.6 (add illustration_tag()): one drawer per prefix (.drawers[i]:
       .frame .label .handle; the bonus dashed + "bonus"); parts sub1..sub5: PINK `group-01/`
       beside each drawer but the first. .drawer(name) .light(name) -> anim
       .receive(mob, name) -> anim (mob slides into the drawer)
    MiniRelay()  glyph-only lecture 3 picture, 6.0 x 1.9: 5 TEAL boxes over 6 BLUE drawers
       (.boxes .drawers); .hop() -> (token, [anim]) box -> drawer -> next box (scene-owned)
    VersionLine(first=10, last=16, lo=14, label_=True)   11 wide axis, GREEN band from 3.lo
       (label_ writes requires-python = ">=3.14" above it); .dot(14.3, "3.14.8", SYSTEM) ->
       dot + label just right of 3.14 (not added); rescale it
    PortPage / ReplyStrip / page_diagram: see "Panels and cards".

Capture folder names (assets/terminal): mega-laptop, mega-l03-laptop, mega-transcribe_audio,
mega-generate_text, mega-synthesis_audio_en, mega-translate_text, mega-synthesis_audio,
gcloud-laptop, port-laptop, expected (never: capture-only).
"""

from __future__ import annotations

import json
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
    AnimationGroup,
    Arc,
    Arrow,
    Circle,
    Create,
    DashedLine,
    DashedVMobject,
    Dot,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    Line,
    MoveAlongPath,
    Polygon,
    Rectangle,
    RoundedRectangle,
    Succession,
    Text,
    Transform,
    TransformFromCopy,
    ValueTracker,
    VGroup,
    VMobject,
    Write,
    always_redraw,
    linear,
)

from explainer import style as S
from explainer.devops import (  # noqa: F401  (LABEL, SMALL, cloud, code_block … are re-exported for the scenes)
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
LAPTOP = S.GREY          # your laptop, ~/AC215, the clones, secrets/ beside the repo, street doors
CLOUD = S.BLUE           # Google Cloud: project, bucket, APIs, IAM; Docker Hub (a registry shelf)
HUB = CLOUD
CTR = S.TEAL             # containers and images, gateway / processor, rooms, the toynet rail
IMAGE = CTR
SYSTEM = S.ORANGE        # system parts of an image: Debian base, apt layer, the base's Python
VENV = S.GREEN           # project-owned and committed: recipe card, tracked files, the venv, compose
GIT_OWNED = VENV
TOOL = S.PURPLE          # tools: docker, buildx, Compose, git, gcloud, uv; docker-shell.sh
ERR = S.RED              # errors and "avoid this"
TURN = S.YELLOW          # your turn, the tracker, look here now
COST = S.GOLD            # money; the key glyph
KEY = COST
LOOKUP = S.PINK          # routes, signposts, the run diamond, the phone book, packets, tickets
INK = S.WHITE
DIMMED = S.GREY

# ------------------------------------------------------------------ the running example
USER, HOST = "student", "laptop"
GROUP = "group-01"
VALUES = {"gcp_project": "your-project-id", "bucket_name": "your-team-bucket", "group_name": GROUP}
COMPONENTS = ["transcribe_audio", "generate_text", "synthesis_audio_en", "translate_text",
              "synthesis_audio"]
P_HOME = f"{USER}@{HOST}:~$"
P_WS = f"{USER}@{HOST}:~/AC215$"
P_REPO = f"{USER}@{HOST}:~/AC215/mega-pipeline$"
P_L03 = f"{USER}@{HOST}:~/AC215-l03$"
P_L03_REPO = f"{USER}@{HOST}:~/AC215-l03/mega-pipeline$"
P_TOY = f"{USER}@{HOST}:~/AC215/port_toy$"


def p_comp(component: str) -> str:
    """The laptop prompt in a component folder: p_comp("generate_text")."""
    return f"{USER}@{HOST}:~/AC215/mega-pipeline/{component}$"


def p_l03(component: str) -> str:
    """The prompt in a component folder of the switched lecture 3 clone."""
    return f"{USER}@{HOST}:~/AC215-l03/mega-pipeline/{component}$"


CTR_PROMPT = {"transcribe_audio": "app@0ceffb272288:/app$", "generate_text": "app@45263bb6ca36:/app$",
              "synthesis_audio_en": "app@ba0b1df0eadc:/app$", "translate_text": "app@40d7497c50f2:/app$",
              "synthesis_audio": "app@6172f2cd7728:/app$", "gateway": "#"}
P_RUN_LOCAL = "app@631fac50f92b:/app$"         # S08: ./docker-shell.sh run with the local image
P_STALE = "(app) root@36615ab6e34b:/app#"      # S08: the dlops/* image's pipenv shell
P_SH = "#"                                     # sh inside the gateway

# the bucket's prefixes, README.md:152-158 order; the last one is the ElevenLabs bonus
PREFIXES = ["input_audios/", "text_prompts/", "text_paragraphs/", "text_translated/",
            "text_audios/", "output_audios/", "output_audios_pp/"]

# ------------------------------------------------------------------ layout
BOTTOM = -3.5                    # terminal bottom edge (fixed when it grows or shrinks)
TRACK_LEFT, TRACK_TOP = -6.5, 3.5
TERM_W, TERM_PT = 12.6, 22

# ------------------------------------------------------------------ README trackers
SECTIONS = {
    # mega-pipeline (flexible-workflow) README.md
    "F": ("Get the Code · starting fresh", ["Clone branch", "cd"]),
    "L": ("Get the Code · already have the repo", ["cd", "Fetch", "Checkout", "Stash, retry",
                                                    "Confirm branch"]),
    "B": ("Before you run", ["Secrets folder", "Set cli.py", "Your bucket"]),
    "K": ("Service Account & Secrets", ["Create account", "Grant roles", "JSON key", "Save key",
                                        "Set project", "Enable APIs"]),
    "R": ("How to Run a Component", ["Build and run", "dev", "run", "prod", "chmod +x", "winpty"]),
    "QA": ("transcribe_audio", ["Check --help", "Download", "Transcribe", "Upload"]),
    "QB": ("generate_text", ["Check --help", "Download", "Generate", "Upload", "Other model"]),
    "QC": ("synthesis_audio_en", ["Check --help", "Download", "Synthesize"]),
    "QD": ("translate_text", ["Check --help", "Download", "Translate", "Upload"]),
    "QE": ("synthesis_audio", ["Check --help", "Download", "Synthesize"]),
    "Y": ("Python packages", ["Add a package"]),
    "U": ("Publish the container", ["docker login", "prod"]),
    # port_toy README.md
    "P0": ("Prerequisites", ["Check Docker"]),
    "P1": ("Step 1: Set up the network by hand", ["Get the code", "Create network", "Build images",
                                                  "Start processor", "Start gateway", "Check logs",
                                                  "Send a message"]),
    "P2": ("Step 2: Check the ports", ["Read PORTS", "From the laptop", "From the gateway"]),
    "P3": ("Step 3: Change the ports", ["Host port", "Processor port", "Update gateway", "Clean up"]),
    "P4": ("Step 4: Run with Compose", ["Start the app", "Compare commands", "Apply changes",
                                        "Rebuild", "Stop and remove"]),
    "PH": ("Handy commands", ["Shell inside", "Follow logs", "Compose shell", "List networks",
                              "Inspect network"]),
}
PORT_TOY_KEYS = {"P0", "P1", "P2", "P3", "P4", "PH"}


def place_tracker(tr):
    tr.shift(np.array([TRACK_LEFT - tr.get_left()[0], TRACK_TOP - tr.get_top()[1], 0]))
    return tr


def tracker(key: str, step: int | None = None):
    """The README tracker for section `key` (see SECTIONS), top-left, at `step`. Part 2's
    trackers read "port_toy README › …"."""
    from explainer.devops import ReadmeTracker
    section, steps = SECTIONS[key]
    t = ReadmeTracker(section, steps)
    if key in PORT_TOY_KEYS:
        old = t.head
        new = VGroup(mono("port_toy README", t.size, S.GREY), label("›", t.size, S.GREY),
                     label(section, t.size, INK)).arrange(RIGHT, buff=0.12)
        new.move_to(old, aligned_edge=LEFT).align_to(old, DOWN)
        t.remove(old)
        t.add(new)
        t.head = new
    if step:
        t.set_step(step)
    t.key = key
    return place_tracker(t)


def caption_extra(tr, on: bool = True):
    """Transform: the tracker caption with (or without) ' · extra' while a command the README
    doesn't have is on screen."""
    k = tr.k
    s = f"step {k} of {len(tr.steps)}: {tr.steps[k - 1]}"
    new = label(s + " · extra", tr.size, tr.hi_color, t2c={"· extra": S.GREY}) if on else \
        label(s, tr.size, tr.hi_color)
    new.next_to(tr.dots, RIGHT, buff=0.25)
    return Transform(tr.caption, new)


def switch_section(scene, old, key: str, step: int | None = 1, run_time: float = 0.8):
    """The tracker switches to another README section: the old one lifts away, the new one drops
    in. Returns the new tracker (on screen)."""
    new = tracker(key, step)
    scene.play(FadeOut(old, shift=UP * 0.25), FadeIn(new, shift=DOWN * 0.25), run_time=run_time)
    return new


# ------------------------------------------------------------------ captures and sources
class Capture:
    """One captured command. .cmd (as typed, without "$ "), .lines (its output), .exit (status),
    .first (file line number of .lines[0]), .header (the '#' provenance line of expected/*)."""

    def __init__(self, name: str, cmd: str, lines: list[str], exit_code: int, first: int = 2,
                 header: str = ""):
        self.name, self.cmd, self.lines, self.exit = name, cmd, lines, exit_code
        self.first, self.header = first, header

    def line(self, n: int) -> str:
        """File line n (1-based, as in the script's TERM(file: n))."""
        i = n - self.first
        if not 0 <= i < len(self.lines):
            raise IndexError(f"{self.name}: line {n} is not output (output is lines "
                             f"{self.first}–{self.first + len(self.lines) - 1})")
        return self.lines[i]

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
        e.g. join(64, 65)); print it with wrap=True."""
        return "".join(self.line(n) for n in ns)

    def typed(self, n: int) -> str:
        """The command typed on prompt line n ('app@…:/app$ which python' -> 'which python')."""
        sp = split_prompt(self.line(n))
        if sp is None:
            raise ValueError(f"{self.name}: line {n} is not a prompt line: {self.line(n)!r}")
        return sp[1]

    def json(self, n: int | None = None) -> dict:
        """A JSON reply line parsed (default: the first output line)."""
        return json.loads(self.line(n if n is not None else self.first))

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
            out += self.lines[a - 1:b]
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
    """assets/terminal/<folder>/<name>.txt parsed; capture("12", "mega-laptop") finds
    12-a-docker-shell.txt; capture("port-laptop/23") works too. Fails loudly if missing: never
    show an output that wasn't captured."""
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
    """'app@0ceffb272288:/app$ python cli.py --help' -> ('app@0ceffb272288:/app$', 'python cli.py
    --help'); '# hostname' -> ('#', 'hostname'); not a prompt line -> None."""
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
    """A line longer than `limit` loses its trailing comment, shown as '# …' (script rule)."""
    if len(line) <= limit:
        return line
    i = _comment_at(line)
    if i < 0:
        return line
    code = line[:i]
    return code.rstrip() + "  # …" if code.strip() else code + "# …"


def excerpt(name: str, first: int, last: int, cut_comments: bool = False) -> str:
    """Lines first..last (1-based, inclusive) of a tutorial file in assets/source, for
    code_panel(..., first_line=first). cut_comments: see cut_comment()."""
    lines = source_text(name).split("\n")
    if last > len(lines):
        raise IndexError(f"{name} has {len(lines)} lines")
    out = lines[first - 1:last]
    if cut_comments:
        out = [cut_comment(s) for s in out]
    return "\n".join(out)


_TIME = re.compile(r"^\d+(\.\d+)?s$")


def build_row(row: str, width: int = 65) -> tuple[str, str | None]:
    """A BuildKit live-view row -> (the row without its time field, cut to `width` with '…',
    the time, e.g. '44.7s', or None). '[+] Building 99.5s (10/10) FINISHED  docker:default'
    loses the builder name and keeps its time in the text."""
    r = row.rstrip()
    parts = r.rsplit(None, 1)
    time = None
    if len(parts) == 2 and _TIME.match(parts[1]) and r.lstrip().startswith("=>"):
        r, time = parts[0].rstrip(), parts[1]
    elif len(parts) == 2 and r.startswith("[+]") and parts[1].startswith("docker:"):
        r = parts[0].rstrip()
    if len(r) > width:
        r = r[:width - 1] + "…"
    return r, time


def column_view(lines: list[str], cols=("IMAGE", "DISK USAGE"), gap: int = 3) -> list[str]:
    """`docker images` lines (header first) sliced to the named columns, as the script's
    "column view": each field is the capture's own text, cut at the header's column bounds
    (right-aligned values keep their alignment), joined with `gap` spaces."""
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


# ------------------------------------------------------------------ small text helpers
def sans(s: str, size: float = CAPTION, color: str = INK, **kw) -> Text:
    """CMU Sans Serif text (box and drawer labels, card lines)."""
    return label(s, size, color, font=SANS, **kw)


def note(s: str, color: str = S.GREY, size: float = CAPTION) -> Text:
    """A GREY caption (serif, 20 pt)."""
    return label(s, size, color)


def _keep(m):
    """Mark a group (chip, tag, labelled glyph) to keep its size in Piece.rescale()."""
    m.keep_size = True
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
    """A rounded outline around `mob` (a circled `<`, a boxed word)."""
    r = RoundedRectangle(width=mob.width + 2 * buff, height=mob.height + 2 * buff,
                         corner_radius=min(0.12, (mob.height + 2 * buff) / 2), stroke_color=color,
                         stroke_width=stroke).set_fill(opacity=0)
    return r.move_to(mob)


# ------------------------------------------------------------------ terminal helpers
def term(prompt: str = P_REPO, rows: int = 12, title: str | None = None,
         component: str | None = None, top: float | None = None, width: float = TERM_W,
         size: float = TERM_PT) -> Terminal:
    """The house terminal (full width, 22 pt, 65 characters a row), bottom edge at BOTTOM, or its
    top edge at `top`. component="transcribe_audio" (or "gateway"): inside that container (title
    "container · …", TEAL frame; prompt CTR_PROMPT[component] unless `prompt` is given)."""
    if component and prompt == P_REPO:
        prompt = CTR_PROMPT.get(component, prompt)
    ttl = title or (f"container · {component}" if component else "laptop")
    t = Terminal(prompt=prompt, width=width, rows=rows, size=size, title=ttl)
    if component:
        t.box.set_stroke(CTR, 3)
        t.title.set_color(CTR)
    y = (top - t.box.get_top()[1]) if top is not None else (BOTTOM - t.box.get_bottom()[1])
    t.shift(np.array([-t.box.get_center()[0], y, 0]))
    return t


def strip_top(rows: int = 3) -> float:
    """y of the top edge of a `rows`-row house terminal sitting on BOTTOM."""
    return BOTTOM + Terminal(rows=rows, width=TERM_W, size=TERM_PT, title="x").box.height


STRIP_TOP = strip_top(3)


def enter_container(t: Terminal, component: str = "transcribe_audio", prompt: str | None = None) -> list:
    """Animations: the frame turns TEAL, the title becomes "container · <component>"; the prompt
    becomes `prompt` (default CTR_PROMPT[component]) for the next typed line."""
    t.set_prompt(prompt or CTR_PROMPT[component])
    new = mono(f"container · {component}", CAPTION, CTR).move_to(t.title)
    return [t.box.animate.set_stroke(CTR, 3), Transform(t.title, new)]


def leave_container(t: Terminal, prompt: str, title: str = "laptop") -> list:
    """Animations: back on the laptop (GREY frame, title `title`, prompt `prompt`)."""
    t.set_prompt(prompt)
    new = mono(title, CAPTION, S.GREY).move_to(t.title)
    return [t.box.animate.set_stroke(S.GREY_DARK, 2), Transform(t.title, new)]


def retitle(t: Terminal, title: str, color: str = S.GREY) -> Transform:
    """Animation: the terminal's title text changes (e.g. 'laptop · lecture 3 clone')."""
    return Transform(t.title, mono(title, CAPTION, color).move_to(t.title))


def resize(scene, t: Terminal, rows: int, keep=None, run_time: float = 0.8, extra=(),
           anchor: str = "bottom") -> Terminal:
    """Grow or shrink the terminal to `rows` (bottom edge fixed; anchor="top" keeps the top edge,
    for a second terminal placed with term(top=...)). It keeps its last lines (at most `keep` of
    them), or, when `keep` is a list of line mobjects, exactly those lines. The frame keeps its
    colour (TEAL inside a container)."""
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


def _first_break(text: str, start: int) -> int:
    """Index of the first space outside quotes at or after `start` (len(text) if none)."""
    quote = None
    for i in range(start, len(text)):
        ch = text[i]
        if quote:
            quote = None if ch == quote else quote
        elif ch in "\"'":
            quote = ch
        elif ch == " ":
            return i
    return len(text)


def type_cmd(scene, t: Terminal, cmd: str, type_time: float | None = None):
    """Type `cmd` at the waiting prompt (replacing a bare prompt line if there is one). When
    prompt + command don't fit a row, the command starts on the row under the prompt, indented
    4 spaces, if it has no space early enough (script rule) or fits that row whole; otherwise
    Terminal.type folds it with " \\". Returns the line (or a VGroup with .rows)."""
    _drop_bare(scene, t)
    p = t.prompt + (" " if t.prompt and not t.prompt.endswith(" ") else "")
    full = p + cmd
    fits_under = len(cmd) + 4 <= t.max_chars
    if len(full) <= t.max_chars or (not fits_under and _first_break(full, len(p)) <= t.max_chars - 2):
        return t.type(scene, cmd, type_time)
    # the prompt alone, then the command on the next row(s)
    texts = [p.rstrip()] + t.fold("    " + cmd, first_prefix=4)
    t._make_room(scene, len(texts))
    rows = []
    for k, s in enumerate(texts):
        ln = mono_line(s, t.size, INK, t2c=t._prompt_colors(t.prompt) if k == 0 else None)
        t._place(ln, len(t.lines))
        t.lines.add(ln)
        rows.append(ln)
    scene.add(rows[0])
    typed = VGroup(*[g for r in rows[1:] for g in glyph_range(r, 0)])
    from manim import ShowIncreasingSubsets
    rt = type_time if type_time is not None else min(2.4, max(0.4, 0.045 * len(cmd)))
    scene.play(ShowIncreasingSubsets(typed, rate_func=linear), run_time=rt)
    for r in rows:
        scene.add(r)
    g = VGroup(*rows)
    g.rows, g.text = rows, " ".join(r.text.strip() for r in rows)
    return g


def cd_prompt(scene, t: Terminal, new_prompt: str, color: str = CLOUD, run_time: float = 0.8):
    """After a `cd`: the prompt becomes `new_prompt` (a bare prompt line) and the path part that
    changed flashes in `color` (the whole path when it got shorter). Returns the bare line."""
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


def second_terminal(scene, prompt: str, rows: int = 7, top: float = 2.75,
                    title: str = "laptop · second terminal", run_time: float = 0.6) -> Terminal:
    """A second terminal slides in with its top at `top`: it opens in the home folder
    (P_HOME, the "~" flashing YELLOW, GREY caption "new terminal: cd here first"), then the
    prompt reads `prompt` (a bare prompt line). Returns the terminal (on screen)."""
    t = term(P_HOME, rows=rows, title=title, top=top)
    scene.play(FadeIn(t, shift=DOWN * 0.3), run_time=run_time)
    ln = bare_prompt(scene, t)
    tilde = glyph_range(ln, P_HOME.index("~"), P_HOME.index("~") + 1)
    cap = note("new terminal: cd here first")
    beside(cap, t, ln, buff=0.5)
    scene.play(Indicate(tilde, color=TURN, scale_factor=1.4), FadeIn(cap), run_time=0.8)
    scene.wait(0.6)
    _drop_bare(scene, t)
    t.set_prompt(prompt)
    ln2 = bare_prompt(scene, t)
    scene.play(FadeOut(cap), Indicate(glyph_range(ln2, prompt.index(":") + 1, len(prompt) - 1),
                                      color=TURN, scale_factor=1.05), run_time=0.6)
    return t


def session(scene, t: Terminal, cap: Capture, *spec, wrap: bool = False, type_time=None,
            colors: dict | None = None, out_time: float = 0.5):
    """Replay an interactive capture: `spec` as in Capture.at (file lines, ranges, "…"). A line
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
    """Print BuildKit rows (raw capture lines, or "…") cut at 65 chars; a row's time field
    becomes a GREY time tag at the row's right end, part of the row (.time_tag; None when the
    row has no time). (text, colour) items are accepted. Returns the new lines."""
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
    processor's empty PORTS cell). Not added.
    The columns are measured from the glyphs (grid_x0): the strut's left edge sits about 0.6 of a
    cell left of column 0, which put every box short of its text (Bugbot, PR #29)."""
    cw = cell_width(line.pt)
    x0 = grid_x0(line) + a * cw
    r = box((b - a) * cw + 2 * pad, line.strut.height + 2 * pad, color, fill_opacity=0.0,
            radius=0.06, dashed=dashed, stroke=3)
    r.move_to([x0 + (b - a) * cw / 2, line.strut.get_center()[1], 0])
    return r


def bracket(mobs, text: str, color: str = ERR, x: float | None = None) -> VGroup:
    """A vertical bracket spanning `mobs` (terminal lines) at the terminal's left margin (or at
    x), with a numbered badge centred on it. Not added. .line .badge"""
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
def your_turn() -> VGroup:
    """YELLOW '▶ your turn' tag: put it next to a command the viewer should run now."""
    return _keep(tag("▶ your turn", TURN))


def grey_tag(s: str) -> VGroup:
    return _keep(tag(s, S.GREY))


def extra_tag() -> VGroup:
    return grey_tag("extra")


def illustration_tag(note_: str | None = None) -> VGroup:
    return grey_tag("illustration" + (f" · {note_}" if note_ else ""))


def expected_tag() -> VGroup:
    return grey_tag("expected")


def recorded_tag(s: str = "at the time of recording") -> VGroup:
    return grey_tag(s)


def nokey_tag() -> VGroup:
    return grey_tag("recorded without a key")


def erratum_tag(note_: str | None = None) -> VGroup:
    return grey_tag("erratum" + (f" · {note_}" if note_ else ""))


def standin_tag() -> VGroup:
    return grey_tag("stand-in file · not a real key")


def differ_tag() -> VGroup:
    return grey_tag("your numbers will differ")


def cost_tag(s: str = "your project pays") -> VGroup:
    return _keep(tag(s, COST))


def preview_tag() -> VGroup:
    return grey_tag("preview")


def reply_tag() -> VGroup:
    return grey_tag("captured reply · curl stood in for the Send button")


def notrun_tag(s: str = "not run here") -> VGroup:
    return grey_tag(s)


def build_badge(k: int, words: bool = True) -> VGroup:
    """TEAL badge for BuildKit's [k/5]: a circled k, and with words=True "build step k"."""
    b = step_badge(k, CTR)
    if not words:
        return _keep(b)
    return _keep(VGroup(b, sans(f"build step {k}", CAPTION, CTR)).arrange(RIGHT, buff=0.12))


def stamp(text: str, color: str = ERR, size: float = TAG, angle: float = 0.08) -> VGroup:
    """An outlined, slightly rotated stamp ("CACHED", "kill")."""
    t = sans(text, size, color, weight="BOLD")
    r = RoundedRectangle(width=t.width + 0.3, height=t.height + 0.22, corner_radius=0.06,
                         stroke_color=color, stroke_width=3).set_fill(S.BG, 0.85)
    t.move_to(r)
    g = VGroup(r, t).rotate(angle)
    g.frame, g.text = r, t
    return _keep(g)


def cached_stamp() -> VGroup:
    return stamp("CACHED", VENV, CAPTION)


def fix_chip(text: str, color: str = VENV, font: str | None = None) -> VGroup:
    """A GREEN "the fix" chip (serif text; font=MONO for code)."""
    return _keep(chip(text, color, size=CAPTION, font=font))


# ------------------------------------------------------------------ panels and cards
_LANG = {".py": "python", ".toml": "toml", ".sh": "bash", ".md": "markdown", ".yaml": "yaml",
         ".yml": "yaml", ".json": "json", ".html": "html", ".txt": "text"}


def _lang(path: str) -> str:
    p = Path(path)
    if p.name == "Dockerfile" or p.suffix == ".Dockerfile":
        return "docker"
    if p.name in (".gitignore", ".dockerignore", "Pipfile"):
        return "text"
    return _LANG.get(p.suffix, "text")


def shown_path(name: str) -> str:
    """The path as the viewer sees it in their clone: mega-pipeline/transcribe_audio/cli.py ->
    transcribe_audio/cli.py; other branches carry the branch ("pipenv-flexible-workflow · …",
    "main · …")."""
    first, _, rest = name.partition("/")
    if first == "mega-pipeline-pipenv-flexible-workflow":
        return f"pipenv-flexible-workflow · {rest}"
    if first == "mega-pipeline-main":
        return f"main · {rest}"
    return rest


def _header_text(text: str, size: float = CAPTION) -> VGroup:
    """'transcribe_audio/docker-shell.sh · lines 6–14' -> mono path + serif rest. A branch
    prefix ('main · README.md · line 97') keeps the branch serif and the path mono."""
    parts = text.split(" · ")
    mobs = []
    path_done = False
    for i, p in enumerate(parts):
        s = p if i == 0 else f"· {p}"
        looks_path = ("/" in p or re.search(r"\.\w+$", p.split(" ")[0] or "")) and " " not in p
        if looks_path and not path_done:
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


def src_panel(name: str, first: int, last: int | None = None, cut_comments: bool = False,
              focus=None, size: float = 22, width: float | None = None,
              shown: str | None = None, suffix: str | None = None, wrap: dict | None = None,
              language: str | None = None) -> VGroup:
    """code_panel quoting assets/source/<name> lines first..last, header "shown · lines a–b"
    (+ " · comment cut" when a comment was cut, + " · line N wrapped", + " · suffix").
    wrap={66: ["--push", "-f Dockerfile"]}: file line 66 breaks before those substrings into
    ↪ rows (GREY ↪). .rows_of(file_line) -> code row indices; .bar(file_line, colour) -> VGroup
    of line bars (not added); .span(file_line, sub) -> glyphs; .source_name .first"""
    last = first if last is None else last
    raw = excerpt(name, first, last)
    lines = (excerpt(name, first, last, True) if cut_comments else raw).split("\n")
    cut = cut_comments and lines != raw.split("\n")
    rows, rows_of = [], {}
    for k, ln in enumerate(lines):
        n = first + k
        parts = _wrap_line(ln, wrap[n]) if wrap and n in wrap else [ln]
        rows_of[n] = list(range(len(rows), len(rows) + len(parts)))
        rows += parts
    shown = shown or shown_path(name)
    p = code_panel("\n".join(rows), shown, first, language or _lang(name), font_size=size,
                   width=width)
    where = f"line {first}" if first == last else f"lines {first}–{last}"
    extra = []
    if cut:
        extra.append("comment cut")
    if wrap:
        extra += [f"line {n} wrapped" for n in sorted(wrap)]
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
    """PANEL: plain mono rows (a full build log line, an expected block, docker inspect) on a
    dark rounded panel with a GREY header above. Rows longer than the panel are cut with '…'.
    .rows (mono_lines: substring() colours a part) .frame .header"""
    max_chars = int((width - 0.5) / cell_width(size))
    rows = VGroup()
    pitch = line_pitch(size)
    for i, s in enumerate(lines):
        s = s if len(s) <= max_chars else s[:max_chars - 1] + "…"
        ln = mono_line(s, size, color)
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
    line, headed `header` ("generate_text/cli.py · line 53 (excerpt)"). Pass the full `line`
    (excerpt(...) or cap.line(n)) to check the sub-string. .chip .text .header"""
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


class Prose(str):
    """A prose row for turn_card / card_rows (serif, not a command)."""


def _cell(s, size: float = CAPTION, color: str = INK):
    """A card cell: "`code`" -> mono (without backticks), Prose / str -> serif."""
    if isinstance(s, str) and len(s) > 1 and s.startswith("`") and s.endswith("`"):
        return mono(s[1:-1], size, color)
    return label(str(s), size, color)


def turn_card(rows, width: float | None = None, header: str | None = "your turn",
              size: float = CAPTION) -> VGroup:
    """The static GREY "your turn" card (a ▶ that stays readable when paused). rows: a str is a
    command typed exactly as on screen (mono; "\\n" splits the README's rows, continuation rows
    as written), (cmd, "extra") adds the extra tag, (cmd, note) a GREY note, Prose("…") a serif
    row. The YELLOW ▶ your turn tag sits on the top-right corner (.tag). .frame .rows .tag"""
    items = VGroup()
    for r in rows:
        if isinstance(r, Prose):
            items.add(label(str(r), size, INK))
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
    "`mono`" in backticks), or (str, colour). .frame .rows .header; rows write in with
    self.play(FadeIn(card.rows[i]))."""
    rows = VGroup()
    for it in items:
        s, col = (it, INK) if isinstance(it, str) else it
        rows.add(_cell(s, size, col))
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
    """A two- or three-column card (the README's comparison table; S02's L03 | L04). headers:
    column titles; rows: lists of cells (str, "`mono`", or a mobject). .cells[r][c] .heads
    .frame. Not added; write rows in with FadeIn(VGroup(*card.cells[r]))."""
    ncol = len(headers)
    header_colors = header_colors or [S.GREY] * ncol
    heads = [label(h, size, c) for h, c in zip(headers, header_colors)]
    cells = [[c if not isinstance(c, str) else _cell(c, size) for c in r] for r in rows]
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
    """The "with your key, look for" card: a GREY caption card (never terminal-styled), one row
    per item: (text, where) -> "text · where" (where in GREY, e.g. "cli.py line 44"). The frame
    is built for every row from the start; rows are invisible until write_item(i).
    .frame .rows .title"""

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


class ReplyStrip(VGroup):
    """REPLY: a captured reply line in a small GREY strip (12.6 wide by default; wraps at the
    strip's width like a terminal), with the tag "captured reply · curl stood in for the Send
    button" above its right end. .rows (mono_lines) .frame .tag"""

    def __init__(self, text: str, color: str = OUTPUT, width: float = TERM_W, tag_: bool = True,
                 size: float = CAPTION, **kw):
        super().__init__(**kw)
        n = int((width - 0.5) / cell_width(size))
        chunks = [text[i:i + n] for i in range(0, max(len(text), 1), n)]
        rows = VGroup()
        pitch = line_pitch(size)
        for i, s in enumerate(chunks):
            ln = mono_line(s, size, color)
            ln.shift(np.array([0, -i * pitch, 0]) - ln.strut.get_corner(UP + LEFT))
            rows.add(ln)
        fr = RoundedRectangle(width=width, height=len(chunks) * pitch + 0.3, corner_radius=0.12,
                              stroke_color=S.GREY, stroke_width=2).set_fill(TERM_BG, 1)
        fr.move_to(rows).align_to(rows, LEFT).shift(LEFT * 0.25)
        self.add(fr, rows)
        self.frame, self.rows, self.tag = fr, rows, None
        if tag_:
            tg = reply_tag().next_to(fr, UP, buff=0.08).align_to(fr, RIGHT)
            self.add(tg)
            self.tag = tg
        self.move_to(ORIGIN)

    def span(self, sub: str) -> VGroup:
        """Glyphs of `sub` (must sit within one row)."""
        for r in self.rows:
            if sub in r.text:
                return substring(r, sub)
        raise KeyError(sub)


def page_reply(cap: Capture, n: int | None = None) -> dict:
    """The JSON reply of a page capture (port-laptop/14, 15, 32, 43, 49, 59 line 2)."""
    return cap.json(n)


_PORT_LABELS = [("gateway sent from port", "gateway_out_port"),
                ("processor listening on port", "listen_port"),
                ("processor saw it arrive from", "sender_port")]


# ------------------------------------------------------------------ glyphs
def key_glyph(h: float = 0.3, color: str = KEY, name: str | None = None) -> VGroup:
    """The service-account key: a GOLD key (its content is never drawn). name="mega-pipeline.json"
    adds the file name (mono 20, GOLD) to its right. .key .name"""
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
    """A dashed GOLD key outline: the same file seen through a window (not a copy)."""
    k = key_glyph(h, color)
    out = VGroup(*[DashedVMobject(m, num_dashes=10, dashed_ratio=0.6).set_stroke(color, 2.5)
                   for m in (k[0], k[2], k[3], k[4])])
    return _keep(out)


def clock_glyph(r: float = 0.13, color: str = COST) -> VGroup:
    c = Circle(radius=r, stroke_color=color, stroke_width=2.5)
    h1 = Line(ORIGIN, UP * r * 0.65, color=color, stroke_width=2.5)
    h2 = Line(ORIGIN, RIGHT * r * 0.5, color=color, stroke_width=2.5)
    return VGroup(c, h1, h2)


def token_tag(text: str = "token") -> VGroup:
    """The short-lived access token: a GOLD tag with a small clock."""
    t = sans(text, CAPTION, COST)
    ck = clock_glyph(0.12)
    row = VGroup(ck, t).arrange(RIGHT, buff=0.1)
    fr = RoundedRectangle(width=row.width + 0.34, height=row.height + 0.18, corner_radius=0.1,
                          stroke_color=COST, stroke_width=2.5).set_fill(COST, 0.12).move_to(row)
    g = VGroup(fr, row)
    g.frame, g.text = fr, t
    return _keep(g)


def padlock(h: float = 0.36, color: str = CLOUD) -> VGroup:
    """A padlock (an IAM role). .body .shackle"""
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
    .board .text .post .foot .root() (the point where it is planted) .tip() (the board's point)"""
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
    """A shelf (a registry, Git): a board on two short legs, caption under it. .board .caption"""
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


def sealed_box(w: float = 1.3, color: str = CTR) -> VGroup:
    """An image as a sealed shipping box: front, lid (.lid, can open), side, a tape strip.
    .front .lid .tape"""
    h = w * 0.62
    front = Rectangle(width=w, height=h, stroke_color=color, stroke_width=3).set_fill(color, 0.14)
    d = w * 0.18
    lid = Polygon(front.get_corner(UP + LEFT), front.get_corner(UP + RIGHT),
                  front.get_corner(UP + RIGHT) + np.array([d, d, 0]),
                  front.get_corner(UP + LEFT) + np.array([d, d, 0]),
                  stroke_color=color, stroke_width=3).set_fill(color, 0.25)
    side = Polygon(front.get_corner(UP + RIGHT), front.get_corner(DOWN + RIGHT),
                   front.get_corner(DOWN + RIGHT) + np.array([d, d, 0]),
                   front.get_corner(UP + RIGHT) + np.array([d, d, 0]),
                   stroke_color=color, stroke_width=3).set_fill(color, 0.07)
    tape = Line(front.get_top() + DOWN * 0.02, front.get_center() + DOWN * h * 0.15, color=color,
                stroke_width=7, stroke_opacity=0.8)
    g = VGroup(front, side, lid, tape)
    g.front, g.lid, g.side, g.tape = front, lid, side, tape
    return g


def recipe_card(files=("Dockerfile", "pyproject.toml", "uv.lock"), color: str = VENV,
                caption: str | None = None, size: float = CAPTION, title: str | None = None) -> VGroup:
    """The recipe card: a card with a folded corner, its files in mono (GREEN; GREY for an older
    branch). .frame .rows .caption"""
    rows = VGroup(*[mono(f, size, INK) for f in files]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    if title:
        rows = VGroup(sans(title, size, color), *rows).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    w, h = rows.width + 0.6, rows.height + 0.45
    c = 0.22
    fr = Polygon([-w / 2, h / 2, 0], [w / 2 - c, h / 2, 0], [w / 2, h / 2 - c, 0], [w / 2, -h / 2, 0],
                 [-w / 2, -h / 2, 0], stroke_color=color, stroke_width=3).set_fill(color, 0.12)
    fold = VMobject(stroke_color=color, stroke_width=2).set_points_as_corners(
        [[w / 2 - c, h / 2, 0], [w / 2 - c, h / 2 - c, 0], [w / 2, h / 2 - c, 0]])
    rows.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.25)
    g = VGroup(fr, fold, rows)
    g.caption = None
    if caption:
        cp = label(caption, size, color).next_to(fr, DOWN, buff=0.1)
        g.add(cp)
        g.caption = cp
    g.frame, g.rows = fr, rows
    return _keep(g)


def person(color: str = S.GREY, h: float = 0.62) -> VGroup:
    """A teammate glyph: a head over shoulders."""
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
    """A small gear (the operating system picks the port)."""
    teeth = VGroup(*[Rectangle(width=r * 0.38, height=r * 0.42, stroke_width=0).set_fill(color, 1)
                     .move_to(UP * r * 0.98).rotate(k * TAU / 8, about_point=ORIGIN) for k in range(8)])
    ring_ = Circle(radius=r * 0.8, stroke_width=0).set_fill(color, 1)
    hole = Circle(radius=r * 0.32, stroke_width=0).set_fill(S.BG, 1)
    return _keep(VGroup(teeth, ring_, hole))


def thought(text: str = "?", color: str = S.GREY, size: float = CAPTION) -> VGroup:
    """A thought bubble with text (and two small trailing circles at its bottom-left)."""
    t = label(text, size, INK)
    b = RoundedRectangle(width=t.width + 0.5, height=t.height + 0.36, corner_radius=0.2,
                         stroke_color=color, stroke_width=2.5).set_fill(S.BG, 0.95).move_to(t)
    c1 = Circle(radius=0.08, stroke_color=color, stroke_width=2).move_to(b.get_corner(DOWN + LEFT) + np.array([0.15, -0.16, 0]))
    c2 = Circle(radius=0.05, stroke_color=color, stroke_width=2).move_to(c1.get_center() + np.array([-0.14, -0.14, 0]))
    g = VGroup(b, t, c1, c2)
    g.frame, g.text = b, t
    return _keep(g)


def envelope(text: str | None = "stop", color: str = S.GREY, w: float = 0.7) -> VGroup:
    """An envelope (a polite signal), an optional word under it."""
    h = w * 0.62
    fr = Rectangle(width=w, height=h, stroke_color=color, stroke_width=2.5).set_fill(S.BG, 0.9)
    flap = VMobject(stroke_color=color, stroke_width=2.5).set_points_as_corners(
        [fr.get_corner(UP + LEFT), fr.get_center() + DOWN * h * 0.1, fr.get_corner(UP + RIGHT)])
    g = VGroup(fr, flap)
    if text:
        g.add(label(text, CAPTION, color).next_to(fr, DOWN, buff=0.06))
    g.frame = fr
    return _keep(g)


def keycaps(*keys: str, color: str = INK) -> VGroup:
    """Key caps, e.g. keycaps("Ctrl", "C"), joined by '+'."""
    caps = []
    for k in keys:
        t = sans(k, CAPTION + 2, color)
        fr = RoundedRectangle(width=max(0.55, t.width + 0.3), height=0.55, corner_radius=0.08,
                              stroke_color=color, stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
        caps.append(VGroup(fr, t.move_to(fr)))
    parts = []
    for i, c in enumerate(caps):
        if i:
            parts.append(sans("+", CAPTION + 2, S.GREY))
        parts.append(c)
    return _keep(VGroup(*parts).arrange(RIGHT, buff=0.12))


def machine_glyph(color: str = S.GREY, w: float = 0.5) -> VGroup:
    """A small monitor (another machine on your network)."""
    scr = RoundedRectangle(width=w, height=w * 0.68, corner_radius=0.04, stroke_color=color,
                           stroke_width=2.5).set_fill(color, 0.12)
    st = Line(scr.get_bottom(), scr.get_bottom() + DOWN * w * 0.18, color=color, stroke_width=2.5)
    base = Line(st.get_end() + LEFT * w * 0.22, st.get_end() + RIGHT * w * 0.22, color=color, stroke_width=2.5)
    return _keep(VGroup(scr, st, base))


def shield(name: str = "/secrets", color: str = S.GREY, h: float = 0.9) -> VGroup:
    """A shield (an ignore rule protecting one thing), its mono label under it. .body .name"""
    w = h * 0.8
    body = VMobject(stroke_color=color, stroke_width=3).set_fill(color, 0.15)
    body.set_points_smoothly([[-w / 2, h / 2, 0], [0, h / 2 + 0.05, 0], [w / 2, h / 2, 0],
                              [w / 2 * 0.9, -h * 0.05, 0], [0, -h / 2, 0], [-w / 2 * 0.9, -h * 0.05, 0],
                              [-w / 2, h / 2, 0]])
    n = mono(name, CAPTION, color).next_to(body, DOWN, buff=0.08)
    g = VGroup(body, n)
    g.body, g.name = body, n
    return _keep(g)


def file_row(name: str, color: str = INK, glyph_color: str = S.GREY, size: float = CAPTION) -> VGroup:
    """A file (or folder, name ending in '/') glyph + its mono name. .glyph .text .name"""
    g = folder_glyph(0.22, glyph_color) if name.endswith("/") else file_glyph(0.28, glyph_color)
    t = mono(name, size, color).next_to(g, RIGHT, buff=0.12)
    row = VGroup(g, t)
    row.glyph, row.text, row.name = g, t, name
    return _keep(row)


def ghost_file(name: str = "mega-pipeline.json", color: str = S.GREY) -> VGroup:
    """A dashed GREY file that doesn't exist yet."""
    g = DashedVMobject(file_glyph(0.28, color)[0], num_dashes=18).set_stroke(color, 2)
    t = mono(name, CAPTION, color).next_to(g, RIGHT, buff=0.12)
    row = VGroup(g, t)
    row.glyph, row.text, row.name = g, t, name
    return _keep(row)


def drawer(text: str, w: float = 3.4, color: str = CLOUD, size: float = CAPTION,
           dashed: bool = False) -> VGroup:
    """A BLUE bucket drawer with a mono label and a handle. .frame .label .handle"""
    fr = box(w, 0.42, color, fill_opacity=0.12, radius=0.06, dashed=dashed)
    t = mono(text, size, INK).move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.18)
    hd = RoundedRectangle(width=0.3, height=0.08, corner_radius=0.04, stroke_width=0).set_fill(color, 0.9)
    hd.move_to(fr).align_to(fr, RIGHT).shift(LEFT * 0.18)
    g = VGroup(fr, t, hd)
    g.frame, g.label, g.handle = fr, t, hd
    return _keep(g)


def loop_glyph(r: float = 0.2, color: str = CTR) -> VGroup:
    """A localhost loop: a circular arrow that comes back to where it started."""
    a = Arc(radius=r, start_angle=PI * 0.6, angle=TAU * 0.86, stroke_color=color, stroke_width=3.5)
    end = a.get_end()
    d = a.point_from_proportion(1) - a.point_from_proportion(0.97)
    d = d / (np.linalg.norm(d) + 1e-9)
    n = np.array([-d[1], d[0], 0])
    head = Polygon(end + d * 0.11, end - n * 0.07, end + n * 0.07, stroke_width=0).set_fill(color, 1)
    return VGroup(a, head)


def door(w: float = 0.34, h: float = 0.56, color: str = LAPTOP) -> VGroup:
    """A door glyph (a published port on the laptop, or a room's door): frame + knob. .frame"""
    fr = RoundedRectangle(width=w, height=h, corner_radius=0.04, stroke_color=color,
                          stroke_width=3).set_fill(color, 0.18)
    knob = Dot(fr.get_right() + LEFT * 0.08, radius=0.035, color=color)
    g = VGroup(fr, knob)
    g.frame = fr
    return g


class Stopwatch(VGroup):
    """A GREY stopwatch: the hand sweeps once while .sweep() plays; the caption (e.g. "≈ 20 s")
    is shown under it. .tracker .hand .caption"""

    def __init__(self, caption: str | None = "≈ 20 s", r: float = 0.4, color: str = S.GREY, **kw):
        super().__init__(**kw)
        face = Circle(radius=r, stroke_color=color, stroke_width=3).set_fill(color, 0.08)
        crown = Rectangle(width=0.12, height=0.1, stroke_width=0).set_fill(color, 1).next_to(face, UP, buff=0.02)
        ticks = VGroup(*[Line(UP * r * 0.78, UP * r * 0.95, color=color, stroke_width=2)
                         .rotate(-k * TAU / 12, about_point=ORIGIN) for k in range(12)])
        self.tracker = ValueTracker(0.0)

        def make_hand():
            h = Line(ORIGIN, UP * r * 0.72, color=INK, stroke_width=3)
            h.rotate(-self.tracker.get_value() * TAU, about_point=ORIGIN)
            return h.shift(face.get_center())

        self.hand = always_redraw(make_hand)
        self.face = face
        self.add(face, crown, ticks, self.hand)
        self.caption = None
        if caption:
            self.caption = label(caption, CAPTION, color).next_to(face, DOWN, buff=0.12)
            self.add(self.caption)

    def sweep(self, turns: float = 1.0, run_time: float = 3.0):
        return self.tracker.animate(rate_func=linear, run_time=run_time).increment_value(turns)

    def freeze(self):
        self.hand.clear_updaters()
        return self


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

    def _visible_now(self):
        """Mark the opacity every member has now as its 'shown' opacity (for parts never hidden)."""
        for p in self.parts.values():
            if not getattr(p, "hidden", False):
                _save_op(p)

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
        """A copy without any text (a thumbnail / miniature: shapes, colours; scale freely)."""
        c = self.copy()

        def strip(m):
            for s in list(m.submobjects):
                if isinstance(s, Text) or hasattr(s, "pt"):
                    m.remove(s)
                else:
                    strip(s)
        strip(c)
        return c


def _tick(color: str = INK, h: float = 0.28) -> VMobject:
    return check_mark(h, color)


def _hidden(m):
    """Make m invisible now but remember its opacities, so Piece.parts_in() can bring it back."""
    _save_op(m)
    _set_op(m, 0)
    m.hidden = True
    return m


# ------------------------------------------------------------------ V1 · recipe card or frozen meal
class BuildOrPull(Piece):
    """V1 (S01 teaser, S02, S08, S16 icon). 12.6 x 3.3 (captions included), centred at ORIGIN.
    Left (.left): GREY shelf "Git" with the GREEN recipe card (Dockerfile, pyproject.toml,
    uv.lock) | PURPLE arrow `docker build` | GREY laptop holding a TEAL image, label
    `Python 3.14.8 · uv`. Right (.right): BLUE shelf "Docker Hub" (+ illustration tag) with a
    sealed TEAL box at its right end, and a PINK two-line signpost (the tag) whose pointer aims at
    the box from above.

        v1 = BuildOrPull(show=("git", "card", "hub", "box", "hub_tag"))   # the rest hidden
        self.play(FadeIn(v1)); self.play(*v1.parts_in("build", "local"))
        mates = v1.teammates(3); arrows = [v1.build_arrow(m) for m in mates]
        box2, anim = v1.push_box(); self.play(anim); self.play(v1.aim(box2)); self.play(v1.aim(v1.box))
        labels, anims = v1.open_box([("2025-02-18", INK), ("Python 3.8.17", TURN),
                                     ("pipenv shell", INK), ("user: root", ERR)])
    Parts: git (shelf + caption), card, build (arrow + label), local (laptop, image, label),
    hub (shelf + caption), hub_tag, box, post (signpost board), pointer.
    .card .box .post .pointer .laptop .image .image_label .git_shelf .hub_shelf .left .right"""

    ALL = ("git", "card", "build", "local", "hub", "hub_tag", "box", "post", "pointer")

    def __init__(self, tag_name: str = "dlops/mega-pipeline-transcribe-audio:latest",
                 image_label: str = "Python 3.14.8 · uv", show=ALL, **kw):
        super().__init__(**kw)
        base_y = -0.75
        # left: Git shelf + card
        gs = shelf("Git", 3.0, LAPTOP).move_to([-4.95, base_y, 0], aligned_edge=UP)
        gs.shift(UP * (base_y - gs.board.get_center()[1]))
        card = recipe_card()
        card.next_to(gs.board, UP, buff=0.06)
        # laptop with the local image
        lp = laptop(1.75, LAPTOP)
        lp.shift(np.array([-0.2 - lp.get_center()[0], base_y - lp.get_bottom()[1], 0]))
        img = sealed_box(0.85, CTR)
        img.remove(img.tape)                      # a built image: no tape
        img.move_to(lp.screen)
        il = sans(image_label, CAPTION, CTR).next_to(lp, DOWN, buff=0.12)
        local = VGroup(lp, img, il)
        a0 = card.frame.get_right() + RIGHT * 0.12
        a1 = np.array([lp.get_left()[0] - 0.12, a0[1], 0])
        ar = Arrow(a0, a1, buff=0, color=TOOL, stroke_width=5, max_tip_length_to_length_ratio=0.18)
        al = mono("docker build", CAPTION, TOOL).next_to(ar, UP, buff=0.1)
        build = VGroup(ar, al)
        # right: Docker Hub shelf, box, signpost
        hs = shelf("Docker Hub", 4.7, HUB)
        hs.shift(np.array([3.95 - hs.board.get_center()[0], base_y - hs.board.get_center()[1], 0]))
        bx = sealed_box(1.3, CTR)
        bx.next_to(hs.board, UP, buff=0.04).align_to(hs.board, RIGHT).shift(LEFT * 0.2)
        ht = illustration_tag().next_to(hs.caption, RIGHT, buff=0.25)
        i = tag_name.find("/") + 1
        j = tag_name.find("-", tag_name.find("-", i) + 1) + 1   # after "mega-pipeline-"
        post = signpost([tag_name[:j], tag_name[j:]], post_h=0.0)
        post.remove(post.post, post.foot)
        post.board_only = True
        post.move_to([0, 0, 0])
        post.shift(np.array([hs.board.get_right()[0] - 0.05 - post.board.get_right()[0],
                             bx.get_top()[1] + 0.75 + post.board.height / 2 - post.board.get_center()[1], 0]))
        stick = Line([post.board.get_left()[0] + 0.2, post.board.get_bottom()[1], 0],
                     [post.board.get_left()[0] + 0.2, base_y, 0], color=LOOKUP, stroke_width=4)
        post.add(stick)
        pointer = self._pointer_to(post, bx)
        # parts
        self.git_shelf, self.card, self.laptop, self.image, self.image_label = gs, card, lp, img, il
        self.hub_shelf, self.box, self.post, self.pointer, self.build = hs, bx, post, pointer, build
        for name, mob in (("git", gs), ("card", card), ("build", build), ("local", local), ("hub", hs),
                          ("hub_tag", ht), ("box", bx), ("post", post), ("pointer", pointer)):
            self.part(name, mob, shown=name in show)
        self.left = VGroup(gs, card, build, local)
        self.right = VGroup(hs, ht, bx, post, pointer)
        self.base_y = base_y

    def _pointer_to(self, post, target) -> Arrow:
        tip = post.tip()
        tgt = target.get_top() if hasattr(target, "get_top") else target
        tgt = np.array(tgt) + UP * 0.08
        return Arrow(tip + RIGHT * 0.02, tgt, buff=0.02, color=LOOKUP, stroke_width=4,
                     max_tip_length_to_length_ratio=0.35, max_stroke_width_to_length_ratio=12)

    def aim(self, target, run_time: float = 0.8):
        """Animation: the signpost's pointer swings to `target` (a box)."""
        new = self._pointer_to(self.post, target)
        return Transform(self.pointer, new, run_time=run_time)

    def teammates(self, n: int = 3, color: str = LAPTOP) -> VGroup:
        """n teammate glyphs (each with a small laptop) in a row under the piece (not added)."""
        mates = VGroup()
        for _ in range(n):
            p = person(color, 0.5)
            lp = laptop(0.6, color).next_to(p, RIGHT, buff=0.08).align_to(p, DOWN)
            g = VGroup(p, lp)
            g.person, g.laptop = p, lp
            mates.add(g)
        mates.arrange(RIGHT, buff=0.9)
        mates.next_to(VGroup(self.git_shelf, self.hub_shelf), DOWN, buff=0.55)
        return mates

    def build_arrow(self, target, color: str = TOOL) -> Arrow:
        """A PURPLE build arrow from the recipe card to `target` (not added)."""
        return Arrow(self.card.frame.get_bottom(), target.get_top(), buff=0.12, color=color,
                     stroke_width=4, max_tip_length_to_length_ratio=0.12)

    def pull_arrow(self, target, src=None, color: str = HUB) -> Arrow:
        """A BLUE pull arrow from the box on the shelf (or `src`) down to `target` (not added)."""
        s = (src or self.box).get_bottom()
        return Arrow(s + DOWN * 0.2, target.get_top(), buff=0.1, color=color, stroke_width=4,
                     max_tip_length_to_length_ratio=0.12)

    def push_box(self, run_time: float = 0.8):
        """A second sealed box slides onto the shelf, left of the first. Returns (box2, anim);
        box2 is scene-owned (FadeOut it when done)."""
        b2 = sealed_box(1.3, CTR)
        b2.align_to(self.box, DOWN).next_to(self.box, LEFT, buff=0.35)
        start = b2.copy().shift(DOWN * 1.2)
        b2.save_state()
        b2.move_to(start)
        b2.set_opacity(0)
        anim = b2.animate(run_time=run_time).restore()
        return b2, anim

    def open_box(self, labels, run_time: float = 1.6):
        """The sealed box opens (lid swings up, tape gone) and the labels rise out of it to a
        column left of the box, above the shelf. labels: [(text, colour), ...] (mono 20).
        Returns (VGroup of labels, [anims]); the labels are scene-owned."""
        bx = self.box
        col = VGroup(*[mono(t, CAPTION, c) for t, c in labels]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        col.next_to(bx, LEFT, buff=0.35).align_to(bx, DOWN).shift(UP * 0.05)
        if col.get_top()[1] > self.post.board.get_bottom()[1] - 0.08:
            col.shift(DOWN * (col.get_top()[1] - self.post.board.get_bottom()[1] + 0.08))
        hinge = bx.lid.get_corner(UP + RIGHT)
        lid_anim = bx.lid.animate.rotate(-PI * 0.55, about_point=bx.front.get_corner(UP + RIGHT))
        anims = [lid_anim, bx.tape.animate.set_opacity(0)]
        rise = []
        for m in col:
            target = m.get_center()
            m.move_to(bx.front.get_center())
            m.set_opacity(0)
            rise.append(m.animate.move_to(target).set_opacity(1))
        anims.append(LaggedStart(*rise, lag_ratio=0.35, run_time=run_time))
        del hinge
        return col, anims

    def old_card(self, files=("Pipfile", "Dockerfile"), caption: str = "branch pipenv-flexible-workflow") -> VGroup:
        """An older GREY recipe card on a second GREY shelf, captioned (not added; place it, e.g.
        .next_to(v1.card, DOWN)). .card .shelf"""
        c = recipe_card(files, color=S.GREY)
        sh = shelf(caption, max(3.1, c.width + 0.4), S.GREY)
        c.next_to(sh.board, UP, buff=0.06)
        g = VGroup(sh, c)
        g.card, g.shelf = c, sh
        return g

    @staticmethod
    def dashed_link(a, b, text: str | None = "?", color: str = S.GREY) -> VGroup:
        """A dashed GREY line between two mobjects with a label at its middle (not added)."""
        ln = DashedLine(a.get_center(), b.get_center(), color=color, stroke_width=3, dash_length=0.12)
        ln.put_start_and_end_on(*_edge_points(a, b))
        g = VGroup(ln)
        if text:
            t = label(text, CAPTION + 4, color).move_to(ln.get_center()).shift(UP * 0.25)
            g.add(t)
        return g

    def drop_file(self, name: str = "Pipfile", badge: str = "root", run_time: float = 1.2):
        """A small GREY file glyph `name` with a RED `badge` drops from the box to the laptop.
        Returns (file group, anim); scene-owned."""
        f = file_row(name, INK, S.GREY)
        b = tag(badge, ERR, size=CAPTION)
        b.next_to(f, RIGHT, buff=0.1)
        g = _keep(VGroup(f, b))
        g.move_to(self.laptop.screen.get_center() + DOWN * 0.05)
        g.save_state()
        g.move_to(self.box.get_center())
        g.set_opacity(0)
        from manim import Restore
        return g, Restore(g, run_time=run_time)


def _edge_points(a, b):
    """Start/end points on the bounding boxes of a and b along the line between their centres."""
    ca, cb = a.get_center(), b.get_center()
    d = cb - ca
    n = np.linalg.norm(d) + 1e-9
    u = d / n

    def exit_pt(m, c, v):
        hw, hh = m.width / 2 + 0.06, m.height / 2 + 0.06
        tx = hw / abs(v[0]) if abs(v[0]) > 1e-6 else 1e9
        ty = hh / abs(v[1]) if abs(v[1]) > 1e-6 else 1e9
        return c + v * min(tx, ty)
    return exit_pt(a, ca, u), exit_pt(b, cb, -u)


# ------------------------------------------------------------------ V2 · three piles at a branch switch
class ThreePiles(Piece):
    """V2 (S03; S09 glyph-only miniature). ≈ 12.4 x 3.6 with walls and incoming files, centred.
    Three piles (3.2 wide each): tracked (GREEN, transcribe_audio/: cli.py with a YELLOW pencil
    "edited"), untracked (GREY, generate_text/: Dockerfile, uv.lock), ignored (GREY dashed,
    transcribe_audio/: Dockerfile, pyproject.toml, uv.lock, secrets/ with the GOLD key); a stash
    column at the right (two boxes, hidden).

        v2 = ThreePiles(); self.play(FadeIn(v2))              # piles shown; walls etc. hidden
        self.play(*v2.parts_in("incoming")); self.play(v2.slide_in())
        self.play(*v2.parts_in("wall1", "wall2"))
        self.play(*v2.stash(1)); ... self.play(*v2.stash(2)); self.play(*v2.land())
        self.play(v2.flip_card("ignored", "Dockerfile")); self.play(v2.relabel(2, "stash@{0}"))
    .row(pile, name) -> the row (glyph + name); .piles[pile] (.frame .kind .folder .rows);
    .key (the GOLD key in secrets/); .pencil. Parts: "wall1", "wall2", "incoming", "stash1",
    "stash2", "standin" (stand-in tag under the key)."""

    def __init__(self, **kw):
        super().__init__(**kw)
        spec = [("tracked", "transcribe_audio/", ["cli.py"], VENV, False),
                ("untracked", "generate_text/", ["Dockerfile", "uv.lock"], S.GREY, False),
                ("ignored", "transcribe_audio/", ["Dockerfile", "pyproject.toml", "uv.lock", "secrets/"],
                 S.GREY, True)]
        pw, pitch = 3.2, 0.44
        fh = 4 * pitch + 0.3
        xs = [-4.85, -1.45, 1.95]
        top = 0.55                                     # frame tops
        self.piles = {}
        for (kind, folder, files, col, dashed), x in zip(spec, xs):
            fr = box(pw, fh, col, fill_opacity=0.06 if not dashed else 0, dashed=dashed)
            fr.move_to([x, top - fh / 2, 0])
            kd = sans(kind, CAPTION, col if col != S.GREY else INK)
            fd = mono(folder, CAPTION, S.GREY)
            hd = VGroup(kd, fd).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            hd.next_to(fr, UP, buff=0.1).align_to(fr, LEFT).shift(RIGHT * 0.15)
            rows = VGroup()
            for k, f in enumerate(files):
                r = file_row(f, INK, col if col != S.GREY else S.GREY)
                r.move_to(fr.get_corner(UP + LEFT) + np.array([0.2, -0.15 - (k + 0.5) * pitch, 0]),
                          aligned_edge=LEFT)
                rows.add(r)
            pile = VGroup(fr, hd, rows)
            pile.frame, pile.kind, pile.folder, pile.rows = fr, kd, fd, rows
            self.piles[kind] = pile
            self.add(pile)
        # the edited cli.py: a pencil + "edited"
        cli = self.row("tracked", "cli.py")
        pen = pencil(0.42)
        pen.next_to(cli, RIGHT, buff=0.2)
        ed = sans("edited", CAPTION, TURN).next_to(pen, RIGHT, buff=0.1)
        cli.add(pen, ed)
        self.pencil = VGroup(pen, ed)
        # the key in secrets/
        sec = self.row("ignored", "secrets/")
        k = key_glyph(0.24).next_to(sec, RIGHT, buff=0.18)
        sec.add(k)
        self.key = k
        st = standin_tag()             # sits on the ignored frame's bottom edge (opaque tag)
        st.move_to(self.piles["ignored"].frame.get_bottom() + DOWN * 0.08)
        self.part("standin", st, shown=False)
        # walls (above the tracked and untracked piles' headers)
        wy = self.piles["tracked"].kind.get_top()[1] + 0.22
        self.wall_y = wy
        for i, kind in ((1, "tracked"), (2, "untracked")):
            fr = self.piles[kind].frame
            bar = Rectangle(width=pw, height=0.12, stroke_width=0).set_fill(ERR, 0.9)
            bar.move_to([fr.get_center()[0], wy, 0])
            badge = step_badge(i, ERR, radius=0.19).next_to(bar, RIGHT, buff=-0.02)
            badge.move_to([bar.get_right()[0] - 0.25, wy + 0.0, 0])
            w = VGroup(bar, badge)
            w.bar, w.badge = bar, badge
            setattr(self, f"wall{i}", w)
            self.part(f"wall{i}", w, shown=False)
        # incoming: the branch's files, waiting above the frame
        files = VGroup(*[file_glyph(0.34, VENV) for _ in range(6)]).arrange(RIGHT, buff=0.26)
        bl = mono("flexible-workflow", CAPTION, VENV)
        inc = VGroup(files, bl).arrange(RIGHT, buff=0.35)
        inc.move_to([(xs[0] + xs[1]) / 2, wy + 0.42, 0])
        # invisible anchors (they move with the piece): where incoming stops, where it lands
        self._stop = Dot(inc.get_center(), radius=0.01).set_opacity(0)
        land_y = self.piles["tracked"].frame.get_center()[1]
        self._land = Dot([inc.get_center()[0], land_y, 0], radius=0.01).set_opacity(0)
        self.add(self._stop, self._land)
        self.incoming = inc
        self.part("incoming", inc, shown=False)
        inc.shift(UP * 1.6)
        # stash column
        sx = 5.05
        self.stash_boxes = {}
        for i, n_rows, y in ((1, 1, top + 0.35), (2, 2, top - 0.85)):
            h = n_rows * pitch + 0.3
            fr = box(2.4, h, S.GREY, fill_opacity=0.08, radius=0.1).move_to([sx, y - h / 2, 0])
            lb = sans("stash", CAPTION, S.GREY).next_to(fr, UP, buff=0.06).align_to(fr, LEFT)
            g = VGroup(fr, lb)
            g.frame, g.label = fr, lb
            self.stash_boxes[i] = g
            self.part(f"stash{i}", g, shown=False)

    def row(self, pile: str, name: str):
        for r in self.piles[pile].rows:
            if r.name == name:
                return r
        raise KeyError(f"{name} not in the {pile} pile")

    def slide_in(self, run_time: float = 1.0):
        """Animation: the branch's files slide down from above and stop at the walls (show the
        "incoming" part first)."""
        return self.incoming.animate(run_time=run_time).move_to(self._stop.get_center())

    def stash(self, i: int, run_time: float = 1.0) -> list:
        """i=1: the edited cli.py lifts into stash box 1 and wall 1 falls; i=2: the untracked pair
        lifts into stash box 2 and wall 2 falls. Shows the box if hidden. Returns animations."""
        bx = self.stash_boxes[i]
        anims = []
        if getattr(bx, "hidden", False):
            anims += self.parts_in(f"stash{i}")
        rows = [self.row("tracked", "cli.py")] if i == 1 else list(self.piles["untracked"].rows)
        for k, r in enumerate(rows):
            target = bx.frame.get_corner(UP + LEFT) + np.array([0.2, -0.15 - (k + 0.5) * 0.44, 0])
            anims.append(r.animate.move_to(target, aligned_edge=LEFT))
        if i == 1:
            anims.append(self.pencil.animate.set_opacity(0))
        w = getattr(self, f"wall{i}")
        if not getattr(w, "hidden", False):
            _save_op(w)
            anims.append(w.animate.shift(DOWN * 0.35).set_opacity(0))
            self._flag(w, True)
        return [AnimationGroup(*anims, run_time=run_time)]

    def land(self, run_time: float = 1.0) -> list:
        """The branch's files land inside the (emptied) tracked and untracked frames."""
        return [self.incoming.animate(run_time=run_time).move_to(self._land.get_center()),
                Indicate(self.piles["tracked"].frame, color=VENV, scale_factor=1.0, run_time=run_time),
                Indicate(self.piles["untracked"].frame, color=VENV, scale_factor=1.0, run_time=run_time)]

    def flip_card(self, pile: str, name: str, color: str = TURN, run_time: float = 1.0):
        """Animation: a file card flips over (the branch replaced it) and flashes `color`."""
        from manim import Rotate
        r = self.row(pile, name)
        return Succession(Rotate(r, TAU, axis=UP, about_point=r.get_center(), run_time=run_time * 0.6),
                          Indicate(r.text, color=color, scale_factor=1.1, run_time=run_time * 0.4))

    def relabel(self, i: int, text: str, run_time: float = 0.6):
        """Animation: stash box i's label becomes `text` (mono, e.g. "stash@{0}")."""
        lb = self.stash_boxes[i].label
        new = mono(text, CAPTION, S.GREY).move_to(lb, aligned_edge=LEFT)
        return Transform(lb, new, run_time=run_time)


# ------------------------------------------------------------------ V3 · three gates
API_DOORS = ["Storage", "Speech-to-Text", "Vertex AI", "Translation", "Text-to-Speech"]


class ThreeGates(Piece):
    """V3 (S05; S07 glyph-only; S16 icon). 12.6 x 3.6, centred. Left: your laptop's secrets/ with
    the GOLD key, a PINK route to the container's dashed /secrets slot. The container (TEAL)
    holds a `google.auth` stamp. Right: five BLUE API doors (API_DOORS order) in a column; left of
    each, a dashed lock slot (gate 2, may?) and a switch (gate 3, switched on?); Text-to-Speech has
    no lock slot. Gate labels: "who?" (at the slot), "may?", "switched on?".

        v3 = ThreeGates(show=("container", "doors"))
        self.play(FadeIn(v3)); self.play(*v3.parts_in("laptop", "route")); self.play(v3.pulse())
        self.play(*v3.mint()); self.play(v3.fly(1)); self.play(*v3.parts_in("gate1", "gate2", "gate3"))
        chip, anims = v3.fail_gate1(); self.play(*anims)
        self.play(v3.fill_lock(0, src=console_row)); self.play(v3.switch(0))
        chip, anims = v3.bounce(2, "permission error · from Google")
    Parts: container (box, slot, stamp), doors (rows), laptop, route, ghost, token, gate1, gate2,
    gate3, lock0..lock3 (padlocks: Storage, Speech-to-Text, Vertex AI, Translation).
    .slot .stamp .token .doors[i] (.frame .name .slot (None for Text-to-Speech) .toggle)"""

    ALL = ("container", "doors", "laptop", "route", "gate1", "gate2", "gate3")

    def __init__(self, show=ALL, **kw):
        super().__init__(**kw)
        # laptop: secrets/ + key
        fg = folder_glyph(0.28, LAPTOP)
        fn = mono("secrets/", CAPTION, LAPTOP).next_to(fg, RIGHT, buff=0.12)
        k = key_glyph(0.26).next_to(VGroup(fg, fn), DOWN, buff=0.22)
        cap = label("your laptop", CAPTION, LAPTOP)
        lap = VGroup(VGroup(fg, fn), k, cap)
        cap.next_to(VGroup(fg, fn, k), DOWN, buff=0.25)
        lap.move_to([-5.45, 0.1, 0])
        self.key = k
        # container
        cf = box(3.3, 3.0, CTR, fill_opacity=0.05).move_to([-1.95, 0.0, 0])
        ct = sans("container", CAPTION, CTR).move_to(cf.get_corner(UP + RIGHT) + np.array([-0.2, -0.27, 0]),
                                                       aligned_edge=RIGHT)
        slot = box(0.95, 0.6, CTR, fill_opacity=0, dashed=True, radius=0.08)
        slot.move_to([cf.get_left()[0] + 0.7, 0.45, 0])
        sl = mono("/secrets", CAPTION, CTR).next_to(slot, DOWN, buff=0.1).align_to(slot, LEFT)
        st_t = mono("google.auth", CAPTION, INK)
        st_b = box(st_t.width + 0.4, 0.55, S.GREY, fill_opacity=0.15, radius=0.08)
        st_b.move_to([cf.get_center()[0], -0.6, 0])
        st_t.move_to(st_b)
        stamp_ = VGroup(st_b, st_t)
        container = VGroup(cf, ct, slot, sl, stamp_)
        self.slot, self.stamp, self.container_frame = slot, stamp_, cf
        # route
        a = fn.get_right() + RIGHT * 0.1
        b = slot.get_left() + LEFT * 0.06
        route = VMobject(stroke_color=LOOKUP, stroke_width=5)
        route.set_points_as_corners([a, [a[0] + 0.35, a[1], 0], [a[0] + 0.35, b[1], 0], b])
        self.route = route
        ghost = key_outline(0.26).move_to(slot)
        # token (at the stamp's lower right)
        tok = token_tag("token")
        tok.next_to(stamp_, DOWN, buff=0.15)
        self.token = tok
        self._home = Dot(tok.get_center(), radius=0.01).set_opacity(0)
        self.add(self._home)
        # doors
        doors = VGroup()
        self.doors = []
        y0, pitch = 1.08, 0.6
        for i, name in enumerate(API_DOORS):
            y = y0 - i * pitch
            fr = box(2.75, 0.5, CLOUD, fill_opacity=0.12, radius=0.06).move_to([4.75, y, 0])
            nm = sans(name, CAPTION, INK).move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.2)
            knob = Dot(fr.get_right() + LEFT * 0.16, radius=0.04, color=CLOUD)
            tg = toggle(False).move_to([2.55, y, 0])
            row = VGroup(fr, nm, knob, tg)
            sl_ = None
            if name != "Text-to-Speech":
                sl_ = box(0.42, 0.42, CLOUD, fill_opacity=0, dashed=True, radius=0.06).move_to([1.3, y, 0])
                row.add(sl_)
            else:
                nt = label("no role", CAPTION, S.GREY).move_to([1.3, y, 0])
                row.add(nt)
            stop = Dot([0.45, y, 0], radius=0.01).set_opacity(0)      # where the token waits
            row.add(stop)
            row.frame, row.name, row.slot, row.toggle, row.knob, row.stop = fr, nm, sl_, tg, knob, stop
            self.doors.append(row)
            doors.add(row)
        # gate labels
        g1 = sans("who?", CAPTION, TURN).next_to(slot, UP, buff=0.12)
        g2 = sans("may?", CAPTION, TURN).move_to([1.3, y0 + 0.5, 0])
        g3 = sans("switched on?", CAPTION, TURN).move_to([2.55, y0 + 0.5, 0])
        # padlocks (one per lock slot)
        locks = {}
        for i, d in enumerate(self.doors):
            if d.slot is not None:
                p = padlock(0.32).move_to(d.slot)
                locks[i] = p
        self.locks = locks
        for name, mob in (("container", container), ("doors", doors), ("laptop", lap), ("route", route),
                          ("ghost", ghost), ("token", tok), ("gate1", g1), ("gate2", g2), ("gate3", g3)):
            self.part(name, mob, shown=name in show)
        for i, p in locks.items():
            self.part(f"lock{i}", p, shown=False)
        self.ghost = ghost

    def pulse(self, run_time: float = 1.0):
        """Animation: the route pulses and the GOLD key outline appears in /secrets at the same
        instant (one file seen from both sides: nothing travels)."""
        anims = [Indicate(self.route, color=TURN, scale_factor=1.0)]
        if getattr(self.ghost, "hidden", False):
            anims += self.parts_in("ghost")
        return AnimationGroup(*anims, run_time=run_time)

    def mint(self, run_time: float = 1.0) -> list:
        """The stamp presses the key outline into the GOLD token (shows the token)."""
        anims = [Indicate(self.stamp, color=COST, scale_factor=1.1)]
        if getattr(self.token, "hidden", False):
            _set_op(self.token)
            self._flag(self.token, False)
            anims.append(TransformFromCopy(self.ghost, self.token))
        return [AnimationGroup(*anims, lag_ratio=0.4, run_time=run_time)]

    def _door_point(self, i: int):
        return self.doors[i].stop.get_center()

    def fly(self, i: int, run_time: float = 1.0):
        """Animation: the token flies to the gates of door i (it stops left of the lock slot)."""
        return self.token.animate(run_time=run_time).move_to(self._door_point(i))

    def home(self, run_time: float = 0.6):
        return self.token.animate(run_time=run_time).move_to(self._home.get_center())

    def open_door(self, i: int, color: str = VENV, run_time: float = 0.8):
        """Animation: the call goes through: door i's frame flashes `color`."""
        return Indicate(self.doors[i].frame, color=color, scale_factor=1.06, run_time=run_time)

    def bounce(self, i: int, text: str = "permission error · from Google", run_time: float = 1.0):
        """The token hits door i's (empty) lock slot and bounces back, the slot flashes RED, and a
        RED chip appears under the doors. Returns (chip, [anims]); chip is scene-owned."""
        d = self.doors[i]
        hit = (d.slot or d.frame).get_left() + LEFT * 0.1
        back = self._door_point(i)
        chip_ = chip(text, ERR, size=CAPTION)
        chip_.next_to(VGroup(*self.doors), DOWN, buff=0.25).align_to(self.doors[0].frame, RIGHT)
        anims = [Succession(self.token.animate(run_time=run_time * 0.4).move_to(hit),
                            self.token.animate(run_time=run_time * 0.4).move_to(back)),
                 Indicate(d.slot or d.frame, color=ERR, scale_factor=1.2, run_time=run_time),
                 FadeIn(chip_, run_time=run_time)]
        return chip_, anims

    def fail_gate1(self, text: str = "DefaultCredentialsError", note_: str = "inside the container",
                   run_time: float = 0.8):
        """Gate 1 refuses: the slot flashes RED, the ghost key vanishes, a RED chip + GREY note
        appear under the container. Returns (chip group, [anims]); chip is scene-owned."""
        c = chip(text, ERR, size=CAPTION, font=MONO)
        n = note(note_)
        g = VGroup(c, n).arrange(DOWN, buff=0.08)
        g.next_to(self.container_frame, DOWN, buff=0.15)
        anims = [Indicate(self.slot, color=ERR, scale_factor=1.15), FadeIn(g)]
        anims += self.parts_out("ghost")
        return g, [AnimationGroup(*anims, run_time=run_time)]

    def lock(self, i: int) -> VGroup:
        """A padlock positioned in door i's slot (a fresh one, not added)."""
        return padlock(0.32).move_to(self.doors[i].slot)

    def fill_lock(self, i: int, src=None, run_time: float = 0.8):
        """Animation: door i's padlock appears in its slot (flying from `src`, a mobject or
        point, when given)."""
        p = self.locks[i]
        _set_op(p)
        self._flag(p, False)
        if src is None:
            return FadeIn(p, scale=1.4, run_time=run_time)
        target = p.get_center().copy()
        p.move_to(src.get_center() if hasattr(src, "get_center") else src)
        return p.animate(run_time=run_time).move_to(target)

    def switch(self, i: int, on: bool = True, run_time: float = 0.5):
        """Animation: door i's API switch flips on (BLUE) or off (GREY)."""
        old = self.doors[i].toggle
        new = toggle(on).move_to(old)
        old.on = on
        return Transform(old, new, run_time=run_time)

    def tick(self, where, color: str = INK) -> VMobject:
        """A white tick: where="gate1" (by the slot), ("lock", i) or ("switch", i). Not added."""
        t = _tick(color)
        if where == "gate1":
            return t.next_to(self.slot, RIGHT, buff=0.06).align_to(self.slot, UP)
        kind, i = where
        d = self.doors[i]
        ref = d.slot if kind == "lock" else d.toggle
        return t.next_to(ref, RIGHT, buff=0.08)


# ------------------------------------------------------------------ V4 · the switchboard
MODES = {"": ("(no argument)", "build, then run", ":71–76 + :79–96"),
         "dev": ("dev", "build only", ":71–76"),
         "run": ("run", "run only", ":79–96"),
         "prod": ("prod", "build two architectures, push", ":51–68")}


class Switchboard(Piece):
    """V4 (S02 silhouette, S06, S08, S09). ≈ 6.4 x 3.4, centred. The script's `case "$1"` as a
    railway switch: an input line with the label "first word" (PURPLE) and four PURPLE tracks
    fanning out to stations; each station: the mode word (mono), what it does (serif), and the
    script lines it runs (a GREY mono chip under it).

        sw = Switchboard(labels=False)        # glyph-only silhouette: words/descs/chips hidden
        self.play(FadeIn(sw)); self.play(*sw.parts_in("words", "descs", "chips"))
        self.play(sw.light("")); self.play(sw.dim_modes("dev", "run", "prod"))
    .tracks[mode] (a polyline) .stations[mode] (.word .desc .chip .dot) .input .junction;
    modes are "", "dev", "run", "prod". Parts: "input_label", "words", "descs", "chips"."""

    def __init__(self, labels: bool = True, **kw):
        super().__init__(**kw)
        jx, jy = -2.4, 0.0
        inp = Line([-2.95, jy, 0], [jx, jy, 0], color=TOOL, stroke_width=6)
        jd = Dot([jx, jy, 0], radius=0.09, color=TOOL)
        il = sans("first word", CAPTION, TOOL).next_to(inp, UP, buff=0.12)
        il.shift(RIGHT * (jx + 0.15 - il.get_right()[0]))
        self.input, self.junction = inp, jd
        self.tracks, self.stations = {}, {}
        words, descs, chips_ = VGroup(), VGroup(), VGroup()
        ys = [1.2, 0.4, -0.4, -1.2]
        sx = -1.35
        for (mode, (w, d, c)), y in zip(MODES.items(), ys):
            tr = VMobject(stroke_color=TOOL, stroke_width=5)
            tr.set_points_as_corners([[jx, jy, 0], [jx + 0.25, jy, 0], [sx - 0.4, y, 0], [sx - 0.1, y, 0]])
            dot = Dot([sx - 0.1, y, 0], radius=0.07, color=TOOL)
            wm = mono(w, CAPTION, TOOL).move_to([sx, y + 0.17, 0], aligned_edge=LEFT)
            dm = label(d, CAPTION, INK).next_to(wm, RIGHT, buff=0.25).align_to(wm, DOWN)
            cm = mono(c, CAPTION, S.GREY).move_to([sx, y - 0.2, 0], aligned_edge=LEFT)
            st = VGroup(dot)
            st.word, st.desc, st.chip, st.dot = wm, dm, cm, dot
            self.tracks[mode], self.stations[mode] = tr, st
            words.add(wm)
            descs.add(dm)
            chips_.add(cm)
            self.add(tr, st)
        self.add(inp, jd)
        self.part("input_label", il, shown=labels)
        self.part("words", words, shown=labels)
        self.part("descs", descs, shown=labels)
        self.part("chips", chips_, shown=labels)
        self.move_to(ORIGIN)

    def light(self, mode: str, color: str = TURN, run_time: float = 0.6):
        """Animation: track `mode` glows (its line and station dot turn `color`, the word
        flashes)."""
        st = self.stations[mode]
        return AnimationGroup(self.tracks[mode].animate.set_stroke(color, 7),
                              st.dot.animate.set_color(color),
                              Indicate(st.word, color=color, scale_factor=1.12), run_time=run_time)

    def unlight(self, mode: str, run_time: float = 0.4):
        st = self.stations[mode]
        return AnimationGroup(self.tracks[mode].animate.set_stroke(TOOL, 5),
                              st.dot.animate.set_color(TOOL), run_time=run_time)

    def dim_modes(self, *modes, k: float = 0.3, run_time: float = 0.5):
        """Animation: the named tracks and their stations fade to k (labels included if shown)."""
        anims = []
        for m in modes:
            st = self.stations[m]
            mobs = [self.tracks[m], st.dot] + [x for x in (st.word, st.desc, st.chip)
                                               if not getattr(x, "hidden", False)]
            for x in mobs:
                anims.append(x.animate.set_opacity(k))
        return AnimationGroup(*anims, run_time=run_time)

    def undim_modes(self, *modes, run_time: float = 0.5):
        anims = []
        for m in modes:
            st = self.stations[m]
            for x in [self.tracks[m], st.dot, st.word, st.desc, st.chip]:
                anims.append(x.animate.set_opacity(1))
        return AnimationGroup(*anims, run_time=run_time)


class RunDecision(Piece):
    """V4's diamond on the run track (S08), 4.8 x 2.0, centred: a PINK diamond "local image?";
    yes -> a TEAL box "local image (however old)"; no -> a BLUE shelf "Docker Hub ·
    $DOCKER_USERNAME/…".  self.play(rd.take("no")).  .diamond .yes .no (.arrow .target .label)"""

    def __init__(self, **kw):
        super().__init__(**kw)
        d = Polygon([0, 0.42, 0], [0.55, 0, 0], [0, -0.42, 0], [-0.55, 0, 0], stroke_color=LOOKUP,
                    stroke_width=4).set_fill(LOOKUP, 0.12).move_to([-1.75, 0, 0])
        dl = sans("local image?", CAPTION, LOOKUP).next_to(d, UP, buff=0.12)
        self.diamond = VGroup(d, dl)
        branches = {}
        for word, y, mk, lab, col in (("yes", 0.6, "box", "local image", CTR),
                                      ("no", -0.65, "hub", None, HUB)):
            tgt = sealed_box(0.55, CTR) if mk == "box" else shelf(None, 0.75, HUB)
            tgt.move_to([0.0, y, 0])
            ar = Arrow(d.get_right() if word == "yes" else d.get_bottom(),
                       tgt.get_left() + LEFT * 0.05, buff=0.05, color=LOOKUP, stroke_width=4,
                       max_tip_length_to_length_ratio=0.2)
            wl = sans(word, CAPTION, LOOKUP).next_to(ar, UP if word == "yes" else DOWN, buff=0.04)
            if word == "no":
                lb = VGroup(sans("Docker Hub", CAPTION, col), mono("$DOCKER_USERNAME/…", CAPTION, col))
                lb.arrange(DOWN, aligned_edge=LEFT, buff=0.06)
            else:
                lb = sans(lab, CAPTION, col)
            lb.next_to(tgt, RIGHT, buff=0.15)
            g = VGroup(ar, wl, tgt, lb)
            g.arrow, g.word, g.target, g.label = ar, wl, tgt, lb
            branches[word] = g
            self.add(g)
        self.add(self.diamond)
        self.yes, self.no = branches["yes"], branches["no"]
        self.move_to(ORIGIN)

    def take(self, branch: str, color: str = TURN, run_time: float = 0.8):
        """Animation: the diamond answers: the `branch` arrow glows, its target flashes."""
        g = self.yes if branch == "yes" else self.no
        return AnimationGroup(Indicate(self.diamond[0], color=color, scale_factor=1.1),
                              g.arrow.animate.set_color(color),
                              Indicate(g.target, color=color, scale_factor=1.15), lag_ratio=0.3,
                              run_time=run_time)


# ------------------------------------------------------------------ V5 · two windows into the laptop
class TwoWindows(Piece):
    """V5 (S06; glyph-only in S08; contrast in S09). 12.6 x 3.6, centred. Left: your laptop
    (GREY) as a tree: ~/AC215/ · mega-pipeline/ · transcribe_audio/ · secrets/ (with the GOLD
    key). Right: the container (TEAL): /app and /secrets windows (left), the GREEN
    /home/app/.venv box (outside both, top right) and the PINK signpost
    /secrets/mega-pipeline.json pointing left into /secrets (bottom right). Under the container,
    a TEAL image slab. l03=True draws lecture 3's clone instead: ~/AC215-l03/ · mega-pipeline/ ·
    transcribe_audio/ · secrets/ INSIDE the component (with the key), for S09's pack().

        v5 = TwoWindows(show=("laptop", "container"))
        self.play(FadeIn(v5)); walker, steps = v5.walk(); for a in steps: self.play(a)
        self.play(*v5.parts_in("route_app", anim=Create)) ... self.play(*v5.parts_in("post"))
        self.play(*v5.parts_in("image", "clock")); self.play(v5.pulse("secrets")); ...
        self.play(*v5.parts_in("never"))
        copies, anims = v5.pack()          # l03=True: the folder and the key ride into the image
    Parts: laptop, container, venv, route_app, route_secrets, post, ghost, image, never, clock.
    .rows {"home", "repo", "comp", "secrets"} (file rows) .key .app .secrets_area .venv_box
    .image_slab"""

    ALL = ("laptop", "container", "venv", "route_app", "route_secrets", "post", "ghost", "image",
           "never", "clock")

    def __init__(self, show=ALL, l03: bool = False, **kw):
        super().__init__(**kw)
        self.l03 = l03
        # laptop panel
        lf = box(4.45, 3.0, LAPTOP, fill_opacity=0.04).move_to([-4.1, 0.25, 0])
        lt = sans("your laptop", CAPTION, LAPTOP).move_to(lf.get_corner(UP + LEFT) + np.array([0.2, -0.27, 0]),
                                                           aligned_edge=LEFT)
        names = ([("~/AC215-l03/", 0, "home"), ("mega-pipeline/", 1, "repo"), ("transcribe_audio/", 2, "comp"),
                  ("secrets/", 3, "secrets")] if l03 else
                 [("~/AC215/", 0, "home"), ("mega-pipeline/", 1, "repo"), ("transcribe_audio/", 2, "comp"),
                  ("secrets/", 1, "secrets")])
        self.rows = {}
        rows = VGroup()
        for k, (n, lvl, key) in enumerate(names):
            r = file_row(n, INK, LAPTOP)
            r.move_to(lf.get_corner(UP + LEFT) + np.array([0.25 + lvl * 0.38, -0.8 - k * 0.5, 0]),
                      aligned_edge=LEFT)
            r.level = lvl
            self.rows[key] = r
            rows.add(r)
        k_ = key_glyph(0.24).next_to(self.rows["secrets"], RIGHT, buff=0.18)
        self.key = k_
        laptop_g = VGroup(lf, lt, rows, k_)
        self.laptop_frame = lf
        # container
        cf = box(6.0, 2.6, CTR, fill_opacity=0.05).move_to([3.25, 0.45, 0])
        ctt = sans("container", CAPTION, CTR).move_to(cf.get_corner(UP + LEFT) + np.array([0.2, -0.27, 0]),
                                                      aligned_edge=LEFT)
        app = box(1.85, 0.8, CTR, fill_opacity=0.08, radius=0.08)
        app.move_to([cf.get_left()[0] + 0.25 + 0.925, 0.6, 0])
        app_l = mono("/app", CAPTION, INK).move_to(app)
        sec = box(1.85, 0.8, CTR, fill_opacity=0.08, radius=0.08)
        sec.move_to([app.get_center()[0], -0.4, 0])
        sec_l = mono("/secrets", CAPTION, INK).move_to(sec)
        container = VGroup(cf, ctt, app, app_l, sec, sec_l)
        self.app, self.secrets_area, self.container_frame = app, sec, cf
        # venv (GREEN, outside both windows)
        vb = box(3.55, 0.6, VENV, fill_opacity=0.15, radius=0.08)
        vb.move_to([cf.get_right()[0] - 0.2 - 1.775, 0.6, 0])
        vl = mono("/home/app/.venv", CAPTION, VENV).move_to(vb)
        venv = VGroup(vb, vl)
        self.venv_box = vb
        # signpost pointing left into /secrets
        post = signpost(["/secrets/", "mega-pipeline.json"], post_h=0.0, point=LEFT)
        post.remove(post.post, post.foot)
        post.move_to([cf.get_right()[0] - 0.2 - post.width / 2, -0.4, 0])
        self.post = post
        ghost = key_outline(0.22).move_to(sec.get_center() + DOWN * 0.18)
        sec_l.shift(UP * 0.14)
        # routes
        r_app = self._route(self.rows["comp"], app)
        r_sec = self._route(self.rows["secrets"], sec, via=k_)
        # image slab under the container
        slab = box(6.0, 0.5, CTR, fill_opacity=0.25, radius=0.06).next_to(cf, DOWN, buff=0.12)
        sl_l = sans("image", CAPTION, CTR).move_to(slab).align_to(slab, LEFT).shift(RIGHT * 0.2)
        image = VGroup(slab, sl_l)
        self.image_slab = slab
        nv_line = Line(slab.get_left() + RIGHT * 1.3, slab.get_right() + LEFT * 0.2, color=S.GREY,
                       stroke_width=3)
        nv_t = label("never in here", CAPTION, S.GREY).set_fill(S.GREY).move_to(nv_line)
        nv_bg = Rectangle(width=nv_t.width + 0.3, height=nv_t.height + 0.1, stroke_width=0).set_fill(S.BG, 1)
        nv_bg.move_to(nv_t)
        never = VGroup(nv_line, nv_bg, nv_t)
        ck = clock_glyph(0.16, S.GREY)
        ck_l = mono("docker run", CAPTION, S.GREY).next_to(ck, RIGHT, buff=0.1)
        clock = VGroup(ck, ck_l).move_to(cf.get_corner(UP + RIGHT) + np.array([-1.3, -0.27, 0]))
        for name, mob in (("laptop", laptop_g), ("container", container), ("venv", venv),
                          ("route_app", r_app), ("route_secrets", r_sec), ("post", post), ("ghost", ghost),
                          ("image", image), ("never", never), ("clock", clock)):
            self.part(name, mob, shown=name in show)
        self.ghost, self.route_app, self.route_secrets = ghost, r_app, r_sec

    @staticmethod
    def _route(row, area, via=None) -> VMobject:
        a = (via or row).get_right() + RIGHT * 0.12
        b = area.get_left() + LEFT * 0.06
        mx = max(a[0] + 0.25, -1.5)
        r = VMobject(stroke_color=LOOKUP, stroke_width=5)
        r.set_points_as_corners([a, [mx, a[1], 0], [mx + 0.3, b[1], 0], b])
        return r

    def walk(self, run_time: float = 0.8):
        """The walk of $(pwd)/../../secrets/: a YELLOW walker starts at transcribe_audio/, steps up
        to mega-pipeline/ ("..") and ~/AC215/ ("../.."), then into secrets/; the path writes
        itself (mono PINK) at the bottom of the laptop panel. Returns (group, [anims]); the group
        is scene-owned (FadeOut it after)."""
        rows = self.rows
        w = Dot(radius=0.09, color=TURN)
        x = rows["comp"].glyph.get_left()[0] - 0.18
        w.move_to([x, rows["comp"].get_center()[1], 0])
        up1 = mono("..", CAPTION, TURN).next_to(rows["repo"], RIGHT, buff=0.3)
        up2 = mono("../..", CAPTION, TURN).next_to(rows["home"], RIGHT, buff=0.3)
        path = mono("$(pwd)/../../secrets/", CAPTION, LOOKUP)
        path.move_to(self.laptop_frame.get_bottom() + UP * 0.3).align_to(self.laptop_frame, LEFT).shift(RIGHT * 0.25)
        steps = [FadeIn(w, scale=1.5, run_time=0.4),
                 AnimationGroup(w.animate.move_to([rows["repo"].glyph.get_left()[0] - 0.18,
                                                   rows["repo"].get_center()[1], 0]), FadeIn(up1), run_time=run_time),
                 AnimationGroup(w.animate.move_to([rows["home"].glyph.get_left()[0] - 0.18,
                                                   rows["home"].get_center()[1], 0]), FadeIn(up2), run_time=run_time),
                 w.animate(run_time=run_time).move_to([rows["secrets"].glyph.get_left()[0] - 0.18,
                                                        rows["secrets"].get_center()[1], 0]),
                 Write(path, run_time=run_time * 1.5)]
        return VGroup(w, up1, up2, path), steps

    def pulse(self, which: str = "secrets", run_time: float = 1.0):
        """Animation: a route pulses ("app" or "secrets"); for "secrets" the GOLD key outline
        appears in /secrets at the same instant (the laptop's key stays where it is)."""
        r = self.route_secrets if which == "secrets" else self.route_app
        anims = [Indicate(r, color=TURN, scale_factor=1.0)]
        if which == "secrets" and getattr(self.ghost, "hidden", False):
            anims += self.parts_in("ghost")
        return AnimationGroup(*anims, run_time=run_time)

    def blink(self, which: str = "app", color: str = TURN, run_time: float = 0.8):
        """Animation: one folder seen from both sides blinks at once: "app" (transcribe_audio/ and
        /app) or "secrets" (secrets/ and /secrets); the route pulses (nothing travels)."""
        row, area, r = ((self.rows["comp"], self.app, self.route_app) if which == "app" else
                        (self.rows["secrets"], self.secrets_area, self.route_secrets))
        return AnimationGroup(Indicate(row, color=color, scale_factor=1.12),
                              Indicate(area, color=color, scale_factor=1.06),
                              Indicate(r, color=color, scale_factor=1.0), run_time=run_time)

    def pack(self, run_time: float = 1.6):
        """S09 (l03=True): COPY . ./ — copies of the component folder's glyph, its secrets/ glyph
        and the key fly down into the image slab, in a row after its label (here the key really is
        copied). Returns (copies, [anims]); the copies are scene-owned."""
        src = [self.rows["comp"].glyph, self.rows["secrets"].glyph, self.key]
        copies = VGroup(*[m.copy() for m in src])
        slab = self.image_slab
        x0 = slab.get_left()[0] + 1.6
        targets = [np.array([x0 + k * 0.7, slab.get_center()[1], 0]) for k in range(3)]
        anims = [LaggedStart(*[c.animate.move_to(t) for c, t in zip(copies, targets)], lag_ratio=0.2,
                             run_time=run_time),
                 Indicate(self.key, color=ERR, scale_factor=1.3, run_time=run_time)]
        return copies, anims


# ------------------------------------------------------------------ V6 + V7 · little computers, doors and rooms
class ToyNet(Piece):
    """V6 + V7 (S10-S16). 12.6 x 2.9 (outline -5.85..6.3; the "outside" machines sit left of it),
    centred. A GREY outline is the laptop (label "your laptop" on its top edge). Its own zone at
    left: a browser glyph, the laptop's localhost loop, and a dashed GREY wall holding the street
    doors (labels left of the doors). The Docker side: TEAL boxes "gateway" and "processor", each
    with its name, a room door on its LEFT wall (label right of it), a port strip "1 … 65535"
    (cells), a row under the strip for lit port numbers, and its own localhost loop. The TEAL
    rail (toynet) runs under them; a PINK phone book (a glyph on the rail, two entries above it)
    sits between the boxes.

        net = ToyNet()                                   # shown: outline, laptop_label, zone, boxes
        self.play(FadeIn(net))
        n1, a1 = net.light_port("gateway", 9100); n2, a2 = net.light_port("processor", 9100)
        self.play(*a1, *a2)                              # FadeOut(n1, n2) later
        self.play(*net.parts_in("rail", "rail_label", "book")); self.play(*net.parts_in("plug_processor"))
        self.play(net.open_room("processor"))            # strip cell -> door ":9200"
        self.play(*net.parts_in("door")); self.play(net.open_room("gateway"))
        self.play(*net.parts_in("map", anim=Create)); self.play(*net.parts_in("aim"))
        p = net.packet(); self.play(FadeIn(p)); self.play(net.travel(p)); self.play(FadeOut(p))
        mob, (a, b) = net.bounce_from_laptop(); self.play(a); self.play(b)
        self.play(net.set_door("127.0.0.1:8095")); self.play(net.set_room("processor", ":9300"))
        self.play(net.set_aim(None, ERR)); self.play(net.set_aim("processor : 9300"))
    Parts: outline, laptop_label, zone (browser + loop + wall), boxes (both), rail, rail_label,
    plug_gateway, plug_processor, book (glyph), book0, book1 (entries), dns_gateway (line +
    "127.0.0.11"), dns_processor, door (127.0.0.1:8090), door2 (0.0.0.0:8091), outside (two
    machines + dashed route to door2), room_gateway (:9100), room_processor (:9200), map (PINK
    arrow browser -> street door -> the gateway's room), aim (PINK dashed gateway -> chip
    "processor : 9200" on the rail; the chip is the packet's destination tag).
    .boxes[name] (.frame .name .strip .cells .loop .loop_label) .doors["door"/"door2"] (.frame
    .label) .rooms[name] (.frame .label) .browser .laptop_loop .wall .rail .plugs[name]
    .book_lines[0/1] .aim_chip .aim_arrow"""

    ALL = ("outline", "laptop_label", "zone", "boxes", "rail", "rail_label", "plug_gateway",
           "plug_processor", "book", "book0", "book1", "dns_gateway", "dns_processor", "door", "door2",
           "outside", "room_gateway", "room_processor", "map", "aim")
    PORT_CELLS = 8

    def __init__(self, show=("outline", "laptop_label", "zone", "boxes"),
                 book_lines=("processor → 172.19.0.2", "gateway → 172.19.0.3"),
                 door_label: str = "127.0.0.1:8090", door2_label: str = "0.0.0.0:8091",
                 rooms=(":9100", ":9200"), aim_label: str = "processor : 9200", **kw):
        super().__init__(**kw)
        H_TOP, H_BOT, X_L, X_R = 1.4, -1.5, -5.85, 6.3
        room_y, rail_y = 0.5, -1.12
        outline = box(X_R - X_L, H_TOP - H_BOT, LAPTOP, fill_opacity=0.02, radius=0.18)
        outline.move_to([(X_L + X_R) / 2, (H_TOP + H_BOT) / 2, 0])
        ll = label("your laptop", CAPTION, LAPTOP)
        ll_bg = Rectangle(width=ll.width + 0.3, height=ll.height + 0.12, stroke_width=0).set_fill(S.BG, 1)
        ll_g = VGroup(ll_bg, ll).move_to([X_L + 1.2, H_TOP, 0])
        # laptop zone: browser, loop, wall
        wall_x = -2.75
        brw = RoundedRectangle(width=0.55, height=0.42, corner_radius=0.05, stroke_color=LAPTOP,
                               stroke_width=2.5).set_fill(PANEL, 1)
        brw_bar = Line(brw.get_corner(UP + LEFT) + DOWN * 0.11, brw.get_corner(UP + RIGHT) + DOWN * 0.11,
                       color=LAPTOP, stroke_width=2)
        browser = VGroup(brw, brw_bar).move_to([X_L + 0.45, 0.95, 0])
        b_l = label("browser", CAPTION, LAPTOP).next_to(browser, RIGHT, buff=0.12)
        lp_loop = loop_glyph(0.17, LAPTOP).move_to([X_L + 0.45, -1.0, 0])
        lp_ll = mono("localhost", CAPTION, LAPTOP).next_to(lp_loop, RIGHT, buff=0.12)
        wall = DashedLine([wall_x, H_TOP - 0.25, 0], [wall_x, H_BOT + 0.25, 0], color=LAPTOP,
                          stroke_width=3, dash_length=0.12)
        zone = VGroup(browser, b_l, lp_loop, lp_ll, wall)
        self.browser, self.browser_label = browser, b_l
        self.laptop_loop, self.wall = VGroup(lp_loop, lp_ll), wall
        # street doors on the wall, labels left of them
        self.doors = {}
        for key, txt, y in (("door", door_label, room_y), ("door2", door2_label, -0.35)):
            d = door(0.34, 0.56, LAPTOP).move_to([wall_x, y, 0])
            dl = mono(txt, CAPTION, INK).next_to(d, LEFT, buff=0.12)
            g = VGroup(d, dl)
            g.frame, g.label = d, dl
            self.doors[key] = g
        # boxes
        self.boxes, self.rooms = {}, {}
        for name, x0, x1 in (("gateway", -2.45, -0.15), ("processor", 3.9, 6.2)):
            top, bot = 1.15, -0.8
            fr = box(x1 - x0, top - bot, CTR, fill_opacity=0.07).move_to([(x0 + x1) / 2, (top + bot) / 2, 0])
            nm = mono(name, CAPTION, CTR).move_to([x0 + 0.18, top - 0.24, 0], aligned_edge=LEFT)
            one = mono("1", CAPTION, S.GREY).move_to([x0 + 0.25, 0.05, 0])
            hi = mono("65535", CAPTION, S.GREY).move_to([x1 - 0.15, 0.05, 0], aligned_edge=RIGHT)
            cx0, cx1 = one.get_right()[0] + 0.1, hi.get_left()[0] - 0.1
            cw = (cx1 - cx0) / self.PORT_CELLS
            cells = VGroup(*[Rectangle(width=cw * 0.82, height=0.2, stroke_color=CTR, stroke_width=1.5)
                             .set_fill(CTR, 0.12).move_to([cx0 + (k + 0.5) * cw, 0.05, 0])
                             for k in range(self.PORT_CELLS)])
            strip = VGroup(one, cells, hi)
            lo = loop_glyph(0.17, CTR).move_to([x0 + 0.3, -0.55, 0])
            lol = mono("localhost", CAPTION, CTR).next_to(lo, RIGHT, buff=0.1)
            b = VGroup(fr, nm, strip, lo, lol)
            b.frame, b.name, b.strip, b.cells, b.loop, b.loop_label = fr, nm, strip, cells, lo, lol
            self.boxes[name] = b
            rd = door(0.3, 0.46, CTR).move_to([x0, room_y, 0])
            rl = mono(rooms[0] if name == "gateway" else rooms[1], CAPTION, CTR).next_to(rd, RIGHT, buff=0.08)
            rg = VGroup(rd, rl)
            rg.frame, rg.label = rd, rl
            self.rooms[name] = rg
        boxes = VGroup(*self.boxes.values())
        g_box, p_box = self.boxes["gateway"], self.boxes["processor"]
        # rail, plugs, label
        rail = Line([-2.55, rail_y, 0], [X_R - 0.05, rail_y, 0], color=CTR, stroke_width=7)
        rl_ = mono("toynet", CAPTION, CTR).next_to(rail, DOWN, buff=0.08).align_to(rail, LEFT)
        self.plugs = {}
        for name in ("gateway", "processor"):
            fb = self.boxes[name].frame
            px = fb.get_left()[0] + 0.5 if name == "processor" else fb.get_center()[0] + 0.6
            self.plugs[name] = Line([px, fb.get_bottom()[1], 0], [px, rail_y, 0], color=CTR, stroke_width=5)
        # phone book between the boxes: a glyph on the rail, the entries above it
        mid = (g_box.frame.get_right()[0] + p_box.frame.get_left()[0]) / 2
        book = VGroup(Rectangle(width=0.42, height=0.32, stroke_color=LOOKUP, stroke_width=2.5).set_fill(LOOKUP, 0.2),
                      Line([0, 0.16, 0], [0, -0.16, 0], color=LOOKUP, stroke_width=2))
        book.move_to([mid, rail_y + 0.3, 0])
        bl0 = mono(book_lines[0], CAPTION, LOOKUP).move_to([mid - 0.1, 0.82, 0])
        bl1 = mono(book_lines[1], CAPTION, LOOKUP).move_to([mid - 0.1, 0.42, 0])
        bl1.align_to(bl0, LEFT)
        self.book_lines = [bl0, bl1]
        dns = {}
        for name in ("gateway", "processor"):
            fb = self.boxes[name].frame
            sx = fb.get_right()[0] if name == "gateway" else fb.get_left()[0]
            dns[name] = DashedLine([sx, -0.35, 0], book.get_center() + (LEFT if name == "gateway" else RIGHT) * 0.25,
                                   color=LOOKUP, stroke_width=2.5, dash_length=0.08)
        dns_l = mono("127.0.0.11", CAPTION, LOOKUP).move_to([mid, -0.12, 0])
        dns["gateway"] = VGroup(dns["gateway"], dns_l)
        # other machines outside the laptop (left of the outline), a dashed route to door2
        outside = VGroup(machine_glyph(), machine_glyph()).arrange(DOWN, buff=0.25).move_to([X_L - 0.42, -0.35, 0])
        d2 = self.doors["door2"].frame
        o_route = VMobject(stroke_color=LAPTOP, stroke_width=2.5)
        o_route.set_points_as_corners([[X_L - 0.12, -0.72, 0], [wall_x - 0.32, -0.72, 0],
                                       [wall_x - 0.32, d2.get_center()[1], 0],
                                       [d2.get_left()[0] - 0.04, d2.get_center()[1], 0]])
        outside.add(DashedVMobject(o_route, num_dashes=30))
        # the -p mapping arrow: browser -> along the top -> down the wall -> through the door -> room
        rg_d = self.rooms["gateway"].frame
        y_b = browser.get_center()[1]
        mp = VMobject(stroke_color=LOOKUP, stroke_width=5)
        mp.set_points_as_corners([[b_l.get_right()[0] + 0.12, y_b, 0], [wall_x, y_b, 0],
                                  [wall_x, room_y, 0], [rg_d.get_left()[0] - 0.3, room_y, 0]])
        tip = Arrow([rg_d.get_left()[0] - 0.35, room_y, 0], [rg_d.get_left()[0] + 0.02, room_y, 0], buff=0,
                    color=LOOKUP, stroke_width=5, max_tip_length_to_length_ratio=0.5)
        mp_g = VGroup(mp, tip)
        # aim: the gateway's dashed arrow to the chip "processor : 9200" on the rail
        ac = mono(aim_label, CAPTION, LOOKUP)
        ac_b = box(ac.width + 0.3, ac.height + 0.18, LOOKUP, fill=S.BG, fill_opacity=0.95, radius=0.08)
        ac_g = VGroup(ac_b, ac.move_to(ac_b)).move_to([mid + 0.25, rail_y, 0])
        gx = self.plugs["gateway"].get_start()[0] + 0.3
        aa = DashedLine([gx, g_box.frame.get_bottom()[1] - 0.04, 0], ac_g.get_left() + LEFT * 0.05,
                        color=LOOKUP, stroke_width=3, dash_length=0.1)
        aim = VGroup(aa, ac_g)
        self.aim_chip, self.aim_arrow = ac_g, aa
        self.rail = rail
        for name, mob in (("outline", outline), ("laptop_label", ll_g), ("zone", zone), ("boxes", boxes),
                          ("rail", rail), ("rail_label", rl_), ("plug_gateway", self.plugs["gateway"]),
                          ("plug_processor", self.plugs["processor"]), ("book", book), ("book0", bl0),
                          ("book1", bl1), ("dns_gateway", dns["gateway"]), ("dns_processor", dns["processor"]),
                          ("door", self.doors["door"]), ("door2", self.doors["door2"]), ("outside", outside),
                          ("room_gateway", self.rooms["gateway"]), ("room_processor", self.rooms["processor"]),
                          ("map", mp_g), ("aim", aim)):
            self.part(name, mob, shown=name in show)

    # -- geometry (always read from members, so it follows the piece when it moves)
    def cell(self, box_name: str, port: int):
        """The strip cell that holds `port` (1..65535) in a box."""
        k = min(self.PORT_CELLS - 1, int((port - 1) / 65535 * self.PORT_CELLS))
        return self.boxes[box_name].cells[k]

    def light_port(self, box_name: str, port: int, color: str = TURN):
        """The strip cell holding `port` glows and its number appears under it. Returns
        (number label, [anims]); the label is scene-owned."""
        c = self.cell(box_name, port)
        n = mono(str(port), CAPTION, color).next_to(c, DOWN, buff=0.06)
        b = self.boxes[box_name]
        if n.get_left()[0] < b.frame.get_left()[0] + 0.1:
            n.align_to(b.frame, LEFT).shift(RIGHT * 0.12)
        return n, [c.animate.set_fill(color, 0.9).set_stroke(color), FadeIn(n, shift=DOWN * 0.1)]

    def unlight_port(self, box_name: str, port: int):
        return self.cell(box_name, port).animate.set_fill(CTR, 0.12).set_stroke(CTR)

    def open_room(self, box_name: str, port: int | None = None, run_time: float = 1.0):
        """Animation: the strip cell lifts out and becomes the box's room door + label
        (TransformFromCopy; shows the room part)."""
        room = self.rooms[box_name]
        _set_op(room)
        self._flag(room, False)
        c = self.cell(box_name, port or (9100 if box_name == "gateway" else 9200))
        return TransformFromCopy(c, room, run_time=run_time)

    def _path(self, src: str, dst: str):
        """gateway -> processor: from the gateway's plug down to the rail, along it, up beside the
        processor and into its room door. processor -> gateway: the reverse."""
        rail_y = self.rail.get_center()[1]
        gp = self.plugs["gateway"].get_start()
        rd = self.rooms["processor"].frame
        up_x = rd.get_center()[0] - 0.3
        pts = [gp + UP * 0.05, [gp[0], rail_y, 0], [up_x, rail_y, 0], [up_x, rd.get_center()[1], 0],
               rd.get_center()]
        pts = [np.array(p, dtype=float) for p in pts]
        return pts if src == "gateway" else pts[::-1]

    def packet(self, dest: str | None = None) -> VGroup:
        """A PINK packet at the gateway's plug (optionally with a destination tag above it; the
        aim chip on the rail usually says it). Scene-owned. .body .dest"""
        body = RoundedRectangle(width=0.36, height=0.24, corner_radius=0.05, stroke_color=LOOKUP,
                                stroke_width=2.5).set_fill(LOOKUP, 0.5)
        g = VGroup(body)
        g.body, g.dest = body, None
        if dest:
            t = mono(dest, CAPTION, LOOKUP).next_to(body, UP, buff=0.08)
            g.add(t)
            g.dest = t
        g.shift(self._path("gateway", "processor")[0] - body.get_center())
        return _keep(g)

    def travel(self, packet, src: str = "gateway", dst: str = "processor", run_time: float = 2.0):
        """Animation: the packet travels from src down to the rail, along it, and into dst."""
        path = VMobject().set_points_as_corners(self._path(src, dst))
        path.shift(packet.get_center() - packet.body.get_center())
        return MoveAlongPath(packet, path, run_time=run_time, rate_func=linear)

    def loopback(self, box_name: str = "gateway", color: str = TURN, run_time: float = 1.4):
        """A packet loops back into the same box: a dot circles its localhost loop, which glows.
        Returns (dot, [anims]); the dot is scene-owned."""
        b = self.boxes[box_name]
        d = Dot(radius=0.07, color=LOOKUP).move_to(b.loop[0].get_start())
        return d, [AnimationGroup(MoveAlongPath(d, b.loop[0]), b.loop.animate.set_color(color),
                                  b.loop_label.animate.set_color(color), run_time=run_time)]

    def unloop(self, box_name: str = "gateway"):
        b = self.boxes[box_name]
        return AnimationGroup(b.loop.animate.set_color(CTR), b.loop_label.animate.set_color(CTR))

    def bounce_from_laptop(self, color: str = ERR, run_time: float = 0.8):
        """A dashed PINK arrow ":9200 ?" from the browser toward the processor stops at the
        laptop's wall where no street door leads there, and turns RED with a cross. Returns
        (group, [anim1, anim2]): play them one after the other; the group is scene-owned."""
        d1, d2 = self.doors["door"].frame, self.doors["door2"].frame
        y = (d1.get_bottom()[1] + d2.get_top()[1]) / 2
        wx = self.wall.get_center()[0]
        a = np.array([self.browser.get_center()[0], y, 0])
        b = np.array([wx - 0.06, y, 0])
        ar = DashedLine(a, b, color=LOOKUP, stroke_width=4, dash_length=0.12)
        cr = VGroup(Line([-0.13, -0.13, 0], [0.13, 0.13, 0]), Line([-0.13, 0.13, 0], [0.13, -0.13, 0]))
        cr.set_stroke(color, 5).move_to(b + RIGHT * 0.06)
        lb = mono(":9200 ?", CAPTION, LOOKUP).next_to(ar, DOWN, buff=0.06).align_to(ar, LEFT).shift(RIGHT * 0.3)
        g = VGroup(ar, lb, cr)
        cr.set_opacity(0)
        return g, [AnimationGroup(Create(ar), FadeIn(lb), run_time=run_time),
                   AnimationGroup(ar.animate.set_color(color), lb.animate.set_color(color),
                                  cr.animate.set_stroke(color, 5, opacity=1), run_time=run_time * 0.6)]

    # -- edits
    def set_door(self, text: str, which: str = "door", color: str = INK, run_time: float = 0.8):
        """Animation: a street door's label becomes `text` (the door flashes): 8090 -> 8095."""
        d = self.doors[which]
        new = mono(text, CAPTION, color).move_to(d.label, aligned_edge=RIGHT)
        return AnimationGroup(Transform(d.label, new), Indicate(d.frame, color=TURN, scale_factor=1.2),
                              run_time=run_time)

    def set_room(self, box_name: str, text: str, color: str = CTR, run_time: float = 0.8):
        """Animation: a room's label changes (":9200" -> ":9300")."""
        r = self.rooms[box_name]
        new = mono(text, CAPTION, color).move_to(r.label, aligned_edge=LEFT)
        return AnimationGroup(Transform(r.label, new), Indicate(r.frame, color=TURN, scale_factor=1.2),
                              run_time=run_time)

    def set_aim(self, text: str | None = None, color: str = LOOKUP, run_time: float = 0.6):
        """Animation: the gateway's aim (dashed arrow + chip) recolours (RED when it misses) and
        optionally changes its text ("processor : 9300")."""
        ac = self.aim_chip
        anims = [self.aim_arrow.animate.set_color(color), ac[0].animate.set_stroke(color)]
        if text:
            anims.append(Transform(ac[1], mono(text, CAPTION, color).move_to(ac[1])))
        else:
            anims.append(ac[1].animate.set_color(color))
        return AnimationGroup(*anims, run_time=run_time)

    def stop_box(self, box_name: str, color: str = S.GREY, run_time: float = 0.6):
        """Animation: a box is stopped (exited): its frame and labels turn GREY; it stays."""
        b = self.boxes[box_name]
        return AnimationGroup(b.frame.animate.set_stroke(color).set_fill(color, 0.05),
                              b.name.animate.set_color(color), b.loop.animate.set_color(color),
                              b.loop_label.animate.set_color(color), run_time=run_time)

    def start_box(self, box_name: str, run_time: float = 0.6):
        b = self.boxes[box_name]
        return AnimationGroup(b.frame.animate.set_stroke(CTR).set_fill(CTR, 0.07),
                              b.name.animate.set_color(CTR), b.loop.animate.set_color(CTR),
                              b.loop_label.animate.set_color(CTR), run_time=run_time)

    def reform(self, box_name: str, run_time: float = 1.0):
        """Animation: a box is recreated (it fades and re-forms with a flash); the others keep
        glowing. (Its room, if shown, stays.)"""
        b = self.boxes[box_name]
        back = b.copy()
        _save_op(back, "_rop")
        faded = back.copy()
        _set_op(faded, 0.12, "_rop")
        return Succession(Transform(b, faded, run_time=run_time * 0.4),
                          Transform(b, back, run_time=run_time * 0.4),
                          Indicate(b.frame, color=CTR, scale_factor=1.04, run_time=run_time * 0.4))


# ------------------------------------------------------------------ V8 · commands become one file
COMPOSE_CMDS = [
    "docker network create toynet",
    "docker build -t toy-processor ./processor",
    "docker build -t toy-gateway ./gateway",
    "docker run -d --name processor --network toynet -e PORT=9200 toy-processor",
    ("docker run -d --name gateway --network toynet -p 127.0.0.1:8090:9100 "
     "-e PROCESSOR_HOST=processor -e PROCESSOR_PORT=9200 toy-gateway"),
]
COMPOSE_PANELS = {"gateway": (11, 25), "processor": (27, 39)}     # docker-compose.yml lines


def fold_cmd(cmd: str, limit: int = 36) -> list[str]:
    """Fold a command at spaces into rows of <= limit chars, keeping an option with its value
    ("-p 127.0.0.1:8090:9100") on one row. Display only (no backslashes)."""
    toks = cmd.split()
    units, i = [], 0
    while i < len(toks):
        t = toks[i]
        if t.startswith("-") and i + 1 < len(toks) and not toks[i + 1].startswith("-") and t not in ("-d",):
            units.append(t + " " + toks[i + 1])
            i += 2
        else:
            units.append(t)
            i += 1
    rows, cur = [], ""
    for u in units:
        if cur and len(cur) + 1 + len(u) > limit:
            rows.append(cur)
            cur = u
        else:
            cur = f"{cur} {u}" if cur else u
    rows.append(cur)
    return rows


class ComposeMap(Piece):
    """V8 (S15, S16). Left (x -6.5..-0.1, top under the tracker at y 2.75): Step 1's five by-hand
    commands (COMPOSE_CMDS) as GREY mono chips, folded at <= 36 chars a row (≈ 6.2 tall).
    Right (x 0.2..6.5, top at 3.45): docker-compose.yml lines 11–25 at 20 pt, comments cut
    (panel="processor": lines 27–39).

        cm = ComposeMap(); self.play(FadeIn(cm))
        cp, anims = cm.fly(4, "--name gateway", 13); self.play(*anims)
        self.play(*cm.swap("processor")) ...; out = cm.outline(17, 18, "live-mount the gateway's folder")
        chip, anims = cm.collapse(); self.play(*anims)
    .chips[i] (.rows: mono_lines) .panel (src_panel: .bar(n) .span(n, sub) .rows_of(n)) .bars"""

    def __init__(self, panel: str = "gateway", **kw):
        super().__init__(**kw)
        chips_ = VGroup()
        for c in COMPOSE_CMDS:
            rows = VGroup(*[mono_line(r, CAPTION, INK) for r in fold_cmd(c)])
            pitch = line_pitch(CAPTION)
            for k, r in enumerate(rows):
                r.shift(np.array([0, -k * pitch, 0]) - r.strut.get_corner(UP + LEFT))
            fr = box(rows.width + 0.4, len(rows) * pitch + 0.16, S.GREY, fill_opacity=0.1, radius=0.1)
            fr.move_to(rows).align_to(rows, LEFT).shift(LEFT * 0.2)
            fr.shift(UP * (rows.get_top()[1] + 0.08 - fr.get_top()[1]))
            g = VGroup(fr, rows)
            g.frame, g.rows, g.cmd = fr, rows, c
            chips_.add(g)
        chips_.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        chips_.move_to([-6.5, 2.75, 0], aligned_edge=UP + LEFT)
        self.chips = chips_
        self.add(chips_)
        self.panels = {k: self._panel(k) for k in COMPOSE_PANELS}
        self.which = panel
        self.panel = self.panels[panel]
        self.add(self.panel)
        self.bars = VGroup()
        self.add(self.bars)

    def _panel(self, which: str) -> VGroup:
        a, b = COMPOSE_PANELS[which]
        p = src_panel("port_toy/docker-compose.yml", a, b, cut_comments=True, size=20)
        p.move_to([6.5, 3.45, 0], aligned_edge=UP + RIGHT)
        return p

    def flag(self, i: int, sub: str) -> VGroup:
        """The glyphs of `sub` in chip i (it must sit within one row)."""
        for r in self.chips[i].rows:
            if sub in r.text:
                return substring(r, sub)
        raise KeyError(f"{sub!r} not in chip {i}")

    def yaml(self, line: int):
        """The code row (glyphs) of docker-compose.yml file line `line` on the current panel."""
        return self.panel.code.code_lines[self.panel.rows_of(line)[0]]

    def fly(self, i: int, sub: str, line: int, sub_yaml: str | None = None, color: str = VENV,
            run_time: float = 1.2):
        """A copy of flag `sub` (chip i) lifts and flies to YAML line `line` (or to `sub_yaml` on
        it), fading as it lands; the line gets a GREEN bar (kept in .bars). Returns (copy,
        [anims]); the copy is scene-owned and gone at the end."""
        src = self.flag(i, sub)
        cp = src.copy()
        tgt = self.panel.span(line, sub_yaml) if sub_yaml else self.yaml(line)
        bar = self.panel.bar(line, color, 0.22)
        self.bars.add(bar)
        anims = [AnimationGroup(Succession(cp.animate(run_time=run_time * 0.75).move_to(tgt).set_color(color),
                                           FadeOut(cp, run_time=run_time * 0.25)),
                                FadeIn(bar, run_time=run_time * 0.4), lag_ratio=0.62)]
        return cp, anims

    def dim_flag(self, i: int, sub: str, k: float = 0.35):
        return self.flag(i, sub).animate.set_opacity(k)

    def swap(self, which: str, run_time: float = 0.8) -> list:
        """The panel becomes the other service's lines (the bars go with the old panel)."""
        old, new = self.panel, self.panels[which]
        old_bars = VGroup(*self.bars.submobjects)
        self.remove(old)
        for b in old_bars:
            self.bars.remove(b)
        self.panel, self.which = new, which
        self.add(new)
        return [FadeOut(VGroup(old, old_bars), run_time=run_time * 0.5),
                FadeIn(new, run_time=run_time)]

    def outline(self, first: int, last: int, text: str, color: str = VENV) -> VGroup:
        """A GREEN outline around YAML lines first..last, a tag under it at the panel's left.
        Not added (FadeIn it; FadeOut later)."""
        ks = self.panel.rows_of(first) + self.panel.rows_of(last)
        rows = VGroup(*[self.panel.code.code_lines[k] for k in range(min(ks), max(ks) + 1)])
        bg = self.panel.code.background
        fr = RoundedRectangle(width=bg.width - 0.2, height=rows.height + 0.18, corner_radius=0.08,
                              stroke_color=color, stroke_width=3).set_fill(opacity=0)
        fr.move_to([bg.get_center()[0], rows.get_center()[1], 0])
        tg = _keep(tag(text, color))
        tg.next_to(self.panel, DOWN, buff=0.25 + 0.55 * len(getattr(self, "_out_tags", []))).align_to(bg, RIGHT)
        ln = Line(fr.get_corner(DOWN + RIGHT) + LEFT * 0.4, [fr.get_right()[0] - 0.4, tg.get_top()[1], 0],
                  color=color, stroke_width=2)
        g = VGroup(fr, ln, tg)
        g.frame, g.tag, g.line = fr, tg, ln
        return g

    def collapse(self, run_time: float = 1.2):
        """Every chip folds into one PURPLE chip `docker compose up` (left column centre). The old
        chips leave the piece. Returns (new chip, [anims]); the new chip joins the piece."""
        c = chip("docker compose up", TOOL, size=CAPTION + 2, font=MONO)
        c.move_to(self.chips.get_center())
        old = list(self.chips.submobjects)
        self.remove(self.chips)
        anims = [FadeOut(o, target_position=c.get_center(), scale=0.6) for o in old]
        self.chips = VGroup()
        self.add(c)
        self.compose_chip = c
        return c, [AnimationGroup(*anims, run_time=run_time * 0.7),
                   FadeIn(c, scale=1.3, run_time=run_time * 0.5)]


# ------------------------------------------------------------------ the bucket, lecture 3's relay, versions
class Cabinet(Piece):
    """The bucket as a BLUE cabinet (S04, S07), 5.9 x 3.9, centred: title `your-team-bucket`,
    one drawer per prefix (PREFIXES; the last, the bonus, dashed with a GREY "bonus"); every
    drawer but the first has a PINK sub-drawer label `group-01/` (parts "sub1".."sub6", hidden).
    Tag it illustration_tag(). .drawers[i] (.frame .label .handle) .drawer(name) .subs[i]
        self.play(*cab.parts_in("sub1", "sub2")); self.play(cab.receive(mob, "input_audios/"))"""

    def __init__(self, prefixes=PREFIXES, sub: str = "group-01/", title: str = "your-team-bucket",
                 show_subs: bool = False, **kw):
        super().__init__(**kw)
        t = mono(title, CAPTION, CLOUD)
        drawers = VGroup()
        for p in prefixes:
            dashed = p == "output_audios_pp/"
            drawers.add(drawer(p, 3.7, CLOUD, dashed=dashed))
        drawers.arrange(DOWN, buff=0.1)
        fr = box(drawers.width + 2.15, drawers.height + 0.9, CLOUD, fill_opacity=0.04)
        fr.move_to(drawers).shift(RIGHT * 0.95 + UP * 0.2)
        drawers.align_to(fr, LEFT).shift(RIGHT * 0.2)
        t.move_to(fr.get_corner(UP + LEFT) + np.array([0.2, -0.24, 0]), aligned_edge=LEFT)
        self.add(fr, t, drawers)
        self.frame, self.title, self.drawers = fr, t, drawers
        self.subs = {}
        for i, d in enumerate(drawers):
            if i == 0:
                continue
            if prefixes[i] == "output_audios_pp/":
                b = label("bonus", CAPTION, S.GREY).next_to(d, RIGHT, buff=0.15)
                self.add(b)
                continue
            s = mono(sub, CAPTION, LOOKUP).next_to(d, RIGHT, buff=0.15)
            self.subs[i] = s
            self.part(f"sub{i}", s, shown=show_subs)

    def drawer(self, name: str):
        for d in self.drawers:
            if d.label.text == name.replace(" ", ""):
                return d
        for d in self.drawers:
            if getattr(d.label, "original_text", None) == name:
                return d
        raise KeyError(name)

    def receive(self, mob, name: str, run_time: float = 0.8):
        """Animation: `mob` slides into drawer `name` (it ends on the drawer's handle side)."""
        d = self.drawer(name)
        return mob.animate(run_time=run_time).move_to(d.frame.get_center() + RIGHT * 1.0).scale(0.8)

    def light(self, name: str, color: str = TURN, run_time: float = 0.8):
        return Indicate(self.drawer(name), color=color, scale_factor=1.06, run_time=run_time)


class MiniRelay(VGroup):
    """Lecture 3's picture in miniature, glyph-only (no text): five TEAL boxes over six BLUE
    drawers, 6.0 x 1.9, centred. .boxes .drawers; .hop() -> (token, [anims]): a white token rises
    from drawer 0 into box 0, drops into drawer 1, rises into box 1 … (scene-owned token)."""

    def __init__(self, **kw):
        super().__init__(**kw)
        self.boxes = VGroup(*[box(0.8, 0.6, CTR, fill_opacity=0.15, radius=0.08) for _ in range(5)])
        self.boxes.arrange(RIGHT, buff=0.35).shift(UP * 0.55)
        self.drawers = VGroup(*[box(0.8, 0.3, CLOUD, fill_opacity=0.2, radius=0.05) for _ in range(6)])
        self.drawers.arrange(RIGHT, buff=0.22).shift(DOWN * 0.6)
        cab = box(self.drawers.width + 0.3, 0.55, CLOUD, fill_opacity=0.04, radius=0.08).move_to(self.drawers)
        self.add(cab, self.drawers, self.boxes)
        self.move_to(ORIGIN)

    def hop(self, n: int = 5, run_time: float = 3.0):
        tok = Dot(radius=0.08, color=INK).move_to(self.drawers[0])
        per = run_time / (2 * min(n, 5))
        steps = []
        for j in range(min(n, 5)):
            steps.append(tok.animate(run_time=per).move_to(self.boxes[j]))
            steps.append(tok.animate(run_time=per).move_to(self.drawers[j + 1]))
        return tok, [Succession(*steps)]


class VersionLine(Piece):
    """Python 3.x versions on a number line (positions by MINOR version: 14 means 3.14) with the
    GREEN `>= 3.lo` band running off the right end; label=True writes `requires-python =
    ">=3.lo"` above the band (label_=False: the scene puts a code panel there). 11 wide.
        vl = VersionLine(10, 16, lo=14, label_=False); d = vl.dot(14.8, "3.14.8", SYSTEM)"""

    def __init__(self, first: int = 10, last: int = 16, lo: int = 14, width: float = 11.0,
                 size: float = 22, label_: bool = True, **kw):
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
        self.add(self.band, self.axis, self.ticks)
        if label_:
            bl = mono(f'requires-python = ">=3.{lo}"', size, VENV)
            bl.next_to(self.band, UP, buff=0.3).align_to(self.band, LEFT)
            self.band_label = bl
            self.add(bl)

    def _x(self, minor: float) -> float:
        return -self.line_w / 2 + (minor - self.first + 0.5) / (self.last - self.first + 1) * self.line_w

    def point(self, minor: float, dy: float = 0.0):
        """A point on the (possibly moved/rescaled) axis above minor version `minor`."""
        a, b = self.axis.get_start(), self.axis.get_end()
        f = (self._x(minor) + self.line_w / 2) / self.line_w
        return a + f * (b - a) + np.array([0, dy, 0])

    def dot(self, minor: float, text: str, color: str, above: bool = True, size: float = 22) -> VGroup:
        """A dot on the axis at `minor` with a mono label (not added). Ticks sit at whole minors;
        a patch release sits just right of its tick: dot(14.3, "3.14.8", SYSTEM). .dot .text"""
        d = Dot(self.point(minor), radius=0.11, color=color)
        t = mono(text, size, color)
        t.next_to(d, UP if above else DOWN, buff=0.3 if above else 0.75)
        g = VGroup(d, t)
        g.dot, g.text = d, t
        return g


# ------------------------------------------------------------------ the port_toy page
def _send_button() -> VGroup:
    t = sans("Send", CAPTION, INK)
    b = RoundedRectangle(width=t.width + 0.5, height=0.46, corner_radius=0.08, stroke_width=0).set_fill(S.GREY_DARK, 1)
    return VGroup(b, t.move_to(b))


class PortPage(Piece):
    """The port_toy page (index.html), a schematic browser window tagged illustration.
    Full: 6.6 x 4.9 — address bar `localhost:<port>`, the input "hello from the laptop" + Send,
    the "Processor's reply" card, the "Which ports were used" card (three lines padded to 30 as
    index.html:84 does) and a glyph-only diagram. compact=True: 7.0 x 2.3 (address bar + reply
    card); compact=True, ports=True adds the three port lines (7.0 x 3.6).
        pg = PortPage(8090); self.play(FadeIn(pg)); self.play(pg.click())
        self.play(*pg.fill(page_reply(capture("14", "port-laptop"))))   # values write in
        self.play(*pg.fill(page_reply(capture("15", "port-laptop"))))   # 55620 -> 55634
    .value(key) -> the mobject showing a JSON key ("upper", "gateway_out_port", "listen_port",
    "sender_port"); .port_lines[i] (mono_lines) .reply_value .address .send .frame .tag
    Parts: "reply" (the reply card), "ports" (port card content), "diagram" (full page only)."""

    def __init__(self, port: int = 8090, reply: dict | None = None, compact: bool = False,
                 ports: bool | None = None, text: str = "hello from the laptop", **kw):
        super().__init__(**kw)
        ports = (not compact) if ports is None else ports
        width = 7.0 if compact else 6.6
        inner = width - 0.5
        # pieces of content, top to bottom
        content = []
        inp = None
        if not compact:
            fld = RoundedRectangle(width=inner - 1.25, height=0.46, corner_radius=0.08, stroke_color=S.GREY,
                                   stroke_width=1.5).set_fill(TERM_BG, 1)
            ft = mono(text, CAPTION, INK).move_to(fld).align_to(fld, LEFT).shift(RIGHT * 0.15)
            send = _send_button()
            inp = VGroup(VGroup(fld, ft), send).arrange(RIGHT, buff=0.2)
            self.send = send
            content.append(inp)
        # reply card
        rc_h = sans("PROCESSOR'S REPLY", CAPTION, S.GREY)
        rv = mono_line(reply["upper"] if reply else "—", CAPTION, INK)
        rc_body = VGroup(rc_h, rv).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        rc_fr = box(inner, rc_body.height + 0.36, S.GREY, fill_opacity=0.05, radius=0.1)
        rc_body.move_to(rc_fr).align_to(rc_fr, LEFT).shift(RIGHT * 0.22)
        reply_card = VGroup(rc_fr, rc_h, rv)
        content.append(reply_card)
        self.reply_value = rv
        port_card = None
        self.port_lines = []
        if ports:
            ph = sans("WHICH PORTS WERE USED", CAPTION, S.GREY)
            lines = VGroup(*[mono_line(self._port_text(k, reply), CAPTION, INK) for k in range(3)])
            pitch = line_pitch(CAPTION)
            for k, ln in enumerate(lines):
                ln.shift(np.array([0, -k * pitch, 0]) - ln.strut.get_corner(UP + LEFT))
            pb = VGroup(ph, lines).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
            p_fr = box(inner, pb.height + 0.36, S.GREY, fill_opacity=0.05, radius=0.1)
            pb.move_to(p_fr).align_to(p_fr, LEFT).shift(RIGHT * 0.22)
            port_card = VGroup(p_fr, ph, lines)
            self.port_lines = list(lines)
            self.port_box = lines
            content.append(port_card)
        diag = None
        if not compact:
            diag = page_diagram_glyph(inner)
            content.append(diag)
        stack = VGroup(*content).arrange(DOWN, buff=0.16)
        height = stack.height + 0.55 + 0.35
        win = browser_window(f"localhost:{port}", width=width, height=height)
        stack.move_to(win.content).align_to(win.content, UP).shift(DOWN * 0.08)
        self.frame, self.address = win, win.address
        tg = illustration_tag().next_to(win, UP, buff=0.08).align_to(win, RIGHT)
        self.tag = tg
        self.add(win, tg)
        if inp is not None:
            self.add(inp)
        else:
            self.send = None
        self.part("reply", reply_card, shown=reply is not None)
        if port_card is not None:
            self.part("ports", port_card, shown=reply is not None)
        if diag is not None:
            self.part("diagram", diag, shown=True)
        self.reply = reply

    @staticmethod
    def _port_text(k: int, reply: dict | None) -> str:
        lab, key = _PORT_LABELS[k]
        return lab.ljust(30) + (str(reply[key]) if reply else "—")

    def fill(self, reply: dict, run_time: float = 0.8) -> list:
        """Animations: the reply card and port lines show `reply` (fade in the first time,
        transform the numbers after)."""
        anims = []
        rv = self.reply_value
        new_v = mono_line(reply["upper"], CAPTION, INK)
        new_v.shift(rv.strut.get_corner(UP + LEFT) - new_v.strut.get_corner(UP + LEFT))
        first = getattr(self.parts["reply"], "hidden", False)
        if first:
            rv.become(new_v)
            rv.text, rv.strut = new_v.text, rv.submobjects[0]
            rv.glyphs = VGroup(*rv.submobjects[1:])
            anims += self.parts_in("reply")
        else:
            anims.append(Transform(rv, new_v))
            rv.text = new_v.text
        for k, ln in enumerate(self.port_lines):
            new = mono_line(self._port_text(k, reply), CAPTION, INK)
            new.shift(ln.strut.get_corner(UP + LEFT) - new.strut.get_corner(UP + LEFT))
            if first:
                ln.become(new)
                ln.text = new.text
                ln.glyphs = VGroup(*ln.submobjects[1:])
                ln.strut = ln.submobjects[0]
            else:
                anims.append(Transform(ln, new))
                ln.text = new.text
        if first and self.port_lines:
            anims += self.parts_in("ports")
        self.reply = reply
        return [AnimationGroup(*anims, run_time=run_time)]

    def clear_reply(self) -> list:
        """Animations: the reply card (and port lines) fade back out."""
        names = [n for n in ("reply", "ports") if n in self.parts]
        return self.parts_out(*names)

    def click(self, run_time: float = 0.5):
        """Animation: the Send button is pressed (full page only)."""
        tgt = self.send if self.send is not None else self.address
        return Indicate(tgt, color=TURN, scale_factor=1.15, run_time=run_time)

    def value(self, key: str):
        """The mobject that shows JSON key `key` on the page."""
        if key == "upper":
            return self.reply_value
        k = [kk for _, kk in _PORT_LABELS].index(key)
        return glyph_range(self.port_lines[k], 30)


def page_diagram_glyph(width: float = 6.1) -> VGroup:
    """The page's diagram as a glyph-only miniature (3 boxes, two arrows, no text)."""
    bw, bh = 1.1, 0.5
    bxs = VGroup(*[RoundedRectangle(width=bw, height=bh, corner_radius=0.08, stroke_color=S.GREY,
                                    stroke_width=2).set_fill(S.GREY, 0.1) for _ in range(3)])
    bxs.arrange(RIGHT, buff=(width - 3 * bw - 0.4) / 2)
    ars = VGroup(*[Arrow(bxs[i].get_right(), bxs[i + 1].get_left(), buff=0.08, color=S.GREY, stroke_width=3,
                         max_tip_length_to_length_ratio=0.12) for i in range(2)])
    return VGroup(bxs, ars)


def page_diagram(host_port="8090", out=None, dst=None, listen=None) -> VGroup:
    """The page's diagram, readable (10.6 x 2.0): "your browser" -> "gateway · listens :9100" ->
    "processor · listens :<listen>", labels "localhost:<host_port> → :9100" and "out :<out> →
    dst :<dst>" above the arrows (values from a reply; "—" before Send). .host (the host-port
    glyphs, e.g. to colour YELLOW) .boxes .labels"""
    out, dst = out or "—", dst or "—"
    listen = listen or dst
    names = [("your browser", "you type here"), ("gateway", "listens :9100"),
             ("processor", f"listens :{listen}")]
    bxs = VGroup()
    for n, s in names:
        a = sans(n, CAPTION + 2, INK)
        b = label(s, CAPTION, S.GREY)
        tx = VGroup(a, b).arrange(DOWN, buff=0.06)
        fr = RoundedRectangle(width=2.4, height=1.0, corner_radius=0.1, stroke_color=S.GREY,
                              stroke_width=2).set_fill(S.GREY, 0.08)
        bxs.add(VGroup(fr, tx.move_to(fr)))
    bxs.arrange(RIGHT, buff=1.7)
    ars = VGroup(*[Arrow(bxs[i].get_right(), bxs[i + 1].get_left(), buff=0.08, color=LOOKUP,
                         stroke_width=4, max_tip_length_to_length_ratio=0.12) for i in range(2)])
    l1 = mono_line(f"localhost:{host_port} → :9100", CAPTION, LOOKUP)
    l2 = mono_line(f"out :{out} → dst :{dst}", CAPTION, LOOKUP)
    l1.move_to(ars[0].get_center() + UP * 0.85)
    l2.move_to(ars[1].get_center() + UP * 0.85)
    g = VGroup(bxs, ars, l1, l2)
    g.host = glyph_range(l1, len("localhost:"), len("localhost:") + len(str(host_port)))
    g.boxes, g.labels = bxs, VGroup(l1, l2)
    g.move_to(ORIGIN)
    return g
