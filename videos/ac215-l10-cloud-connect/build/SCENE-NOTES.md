# L10 scene contract — `scenes/common.py` (read this, your script section, your BRIEF row, common.py)

Reference scene: `scenes/s01_hook.py` (check clean, no anchor warnings; sheets read:
`build/sheets/s01_hook_Hook/`). Every set piece is exercised by `build/common_test.py` (`Bench`); its
sheets `build/sheets/common_test_Bench/sheet_0{1..5}.png` show what each piece looks like. Run it
before you change how you call a piece:
`python -m explainer.check videos/ac215-l10-cloud-connect/build/common_test.py Bench --tts silent`.
**Do not edit `common.py`** (shared; agents run in parallel): work around locally, put requests in
your report.

## Setup, checks, scene skeleton

```bash
cd /home/user/Explainer_Videos && source .venv/bin/activate
export PYTHONPATH=/home/user/Explainer_Videos EXPLAINER_TTS=kokoro EXPLAINER_VOICE=af_heart EXPLAINER_SPEED=0.9 PYTHONHASHSEED=0
python -m explainer.check   videos/ac215-l10-cloud-connect/scenes/sNN_x.py Cls          # must print OK
python -m explainer.preview videos/ac215-l10-cloud-connect/scenes/sNN_x.py Cls --every 3 # read every sheet
python -m explainer.preview ... --at 12.5,30 -q m                                        # exact frames
```
480p only, one render at a time, foreground with a long timeout. First run synthesizes the voice.

```python
from manim import *  # noqa: I001  (manim first, then common: common must win)
from explainer.scene import VoiceScene
from explainer import style as S
from common import (...)            # name what you use (or `from common import *`)

SAY = NARRATION["S07"]              # SAY lines verbatim from script.md, in order
class AdcToToken(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S07"] == 6, len(SAY)
        with self.voiceover(SAY[0]) as vo:     # exactly one block per SAY line, in order
            ...; vo.wait_until("exact phrase from the SAY"); ...
        ...
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)   # end on an empty frame
        self.remove(*self.mobjects)
```
SAY counts (`SAY_COUNT`): S01 4 · S02 5 · S03 5 · S04 7 · S05 6 · S06 7 · S07 6 · S08 6 · S09 8 ·
S10 6 · S11 6 · S12 9 · S13 4 · S14 5 · S15 6. A PONDER goes right after its SAY block:
`card = pause_and_ponder(self, "question\nlines", seconds=8)` (S14: 6); FadeOut it at the start of
the next block. Ponder texts are in script.md (`PONDER(...)`), not in common.py.

**Name collision (binding):** your scene class is named by video.yaml (`SecretsPortal`, `IamGrid`,
`TwoAddresses` …). The set pieces therefore are `SecretsPortalRig` and `IamGridRig`; never define a
module-level name that shadows a common.py export (`from common import *` then your class wins).

## Binding rules (skill "Scene-code pitfalls"; each cost time before)

- No `print()` left anywhere (check reports `PRINT`; `t.print(...)` is fine). Deterministic: no
  unseeded randomness, no `always_redraw` on big groups, clear updaters.
- Text ≥ 20 pt, inside x ∈ [−6.6, 6.6], y ∈ [−3.6, 3.6]. Never `.scale()` anything holding text below
  1.0 (SMALL): build at the size you need (set pieces take size parameters).
- ≤ 3 visual groups at once; something moves every ~4 s (except ponder timers); scenes end empty.
- Never assign `width/height/color/depth` on a VGroup subclass. `capture(...).at()` takes FILE line
  numbers (line 1 = `$ cmd`, refused; `[exit N]` refused; crops refused).
- Terminals: full width (`term`, 12.6 wide, 65 chars at 22 pt) or a 3-row strip at the bottom under a
  picture; never half width; a full terminal and a picture never share the frame. Commands are
  never cut: `type_cmd` folds at a space with ` \`.
- `FadeOut(g)` takes the family off the scene and restores opacity: a faded child that stays in its
  parent snaps back when the parent is animated. Remove it from the parent or fade the parent.
- Never play `FadeIn(piece)` and an animation of one of its parts in the same `play()` (the part's
  Indicate captures the faded state and keeps it invisible).
- No invented numbers, outputs, prices, answer text, embedding values or key material, not even under
  `illustration`. Every number is from a capture/source/ASSETS.md; schematic ideas use symbols.
  Project id on screen is always `your-gcp-project`; `ac215-project`, `129349313346` and "Pavlos"
  only inside quoted repo content and RED story beats. No GCP logos, console screenshots, slide images.
- Prefer transforms that show what became what.

## Colours (BRIEF table; names in common.py)

`LAPTOP` GREY (host shell, host filesystem, the browser's home) · `CLOUD` BLUE (Google's building,
Vertex AI, GCS, token desk, bearer ticket) · `IMAGE` = `CONTAINER` TEAL (containers/images, the
houses) · `SYSTEM` ORANGE (Docker Desktop itself; barely used) · `SECRET` = `KEY` GREEN (secrets/,
the JSON key, /secrets; RED when the key lands inside a repo) · `PASS` GREEN (an allowed cell, a
CORS pass) · `TOOL` PURPLE · `ERR` RED (DefaultCredentialsError, 403, 500, the aborted script, the
missing CORS header) · `TURN` YELLOW (your turn, tracker, look-here, ponder pointers; never RED for
pointing) · `COST` GOLD (every Vertex AI call the student's run makes; S14's storage rule) · `ROUTE`
PINK (Docker networks = streets, Docker DNS, ADC's lookup walk, published-port tunnels, the three
browser calls) · `FUTURE` GREY dashed (hosted deployment, L11 buckets, metadata server, federation)
· `DOOR` GREY (an open, unprefixed published door: never GREEN) · `INK` white.
Episode-local: the key is GREEN, the bearer token a small BLUE `Ticket` with a timer; streets are
PINK when created, GREY dashed while planned; houses TEAL hollow (not running) / lit (running).

## Data, captures, sources

| export | purpose |
| --- | --- |
| `NARRATION["Snn"]`, `SAY_COUNT`, `TITLES[cls]`, `SPEC` | SAY lines from script.md; titles; video.yaml |
| `capture("21")` / `capture("21-docker-shell")` / `capture("laptop/21") -> Capture` | the one file `assets/terminal/laptop/NN-*.txt`; `capture-only/` refused |
| `Capture.cmd .lines .exit .raw .path` | command as typed; output body (no `[exit N]`); every file line (tabs → 8 spaces) |
| `.at(2, (5, 7), "…", 33)` · `.line(n)` · `.istep(n)` | lines by FILE number; one file line; `(prompt, typed)` of an istep line |
| inline `[exit N]` | split off automatically: `capture("23").at(2) == ['"1.0.0"']` (also 34:2, 37:8, 63:2, 74:2) |
| `NEVER` crops | refused by `.line()`: 33:42, 33:164, 51:54, 51:55 |
| `split_prompt(s)` | `app@…:/app$`, `(app) app@…:/app$`, root `6c23fe52ca92:/app#` → (prompt, typed) |
| `cut squeeze cols squash soft` | cut after a marker + `…`; re-align a docker table; keep named columns (54/46: never CREATED/STATUS: `cols(cap.at((2, 3)), ["IMAGE", "PORTS", "NAMES"])`); collapse compose/build padding (`squash(cap.at((3, 5)))`: the `✔ … Pulled <80 spaces> 10.3s` rows are 110 wide); break long lines at a space |
| `readme(n)` | cheese-app-v0/README.md line n, stripped (`capture("10").cmd == readme(74)`, `capture("21").cmd == readme(88)`) |
| `source_text(path)`, `excerpt(path, a, b)` | `cheese-app-v0/…` (prefix optional) or `llm-finetuning/…`, `mega-pipeline/…`, `llm-rag/README.md` |
| `code(path, a, b=None, language=None, focus=None, font_size=22, shown=None, max_lines=12, cuts=None, dedent=False)` | CODE panel, header `api-service/docker-shell.sh · lines 6–11` (repo-relative) or `llm-finetuning · gemini-finetuner/cli.py · lines 89–96`. Raises on > 12 lines and on a line too long for the frame (> 66 chars at 22 pt, > 73 at 20 pt): cut it with `cuts={22: "projects/129349313346/"}` (house `…`, recoloured GREY automatically) or `font_size=20`; `dedent=True` drops the excerpt's common indentation only. Highlight with `code_span(p.code, k, "sub")`, `line_bar(p.code, k, colour)`, k = file line − a |
| `readme_card(lines, body, quote=False, card_w=None, size=22)` | GREY README quote card `README.md · line n` |
| `P_LAPTOP_HOME P_REPO P_LLMRAG P_API P_FRONTEND` · `T_LAPTOP T_SECOND` | prompts `student@laptop:~$` … `…/frontend-ai-chatbot$`; titles `laptop`, `laptop · second terminal` |
| `PROJECT_ID SA_NAME SA_EMAIL KEY_PATH ENV_VAR TOKEN_URI TOKEN_DESK QUESTION CHROMA_DNS STREETS PORTS CONTAINERS KEY_FIELDS RIDDLES KNOCK` | the running example's strings (QUESTION = README:215 as written, lowercase "tolminc") |

Every CODE ref of script.md, measured (longest line; > 12 lines = show successive windows):

| CODE ref | needs |
| --- | --- |
| api-service/docker-shell.sh 6–11 (73), 19–27 (67), 1–16 (73, 16 lines) | `font_size=20`; 1–16 in two windows |
| llm-rag/docker-shell.sh 6–12 (73) · gemini-finetuner/cli.py 89–96 (73) · next.config.js 19–25 (67) | `font_size=20` |
| llm-rag/docker-compose.yml 13–15 (75) | `dedent=True, font_size=20` |
| rag.py 14–27 (118; 14 lines: lines 19, 21, 22 are the long ones), 110–113 (80), 150–171 (22 lines), 190–203 (86) | windows + `cuts=` (e.g. `cuts={22: "projects/129349313346/"}`) |
| docker-entrypoint.sh 6–9 (104) · frontend docker-shell.sh 8–11 (112) · DataService.js 34–43 (143), 45–47 (95) · ChatComponent.jsx 22–28 (130), 161–173 (142, 13 lines) | `cuts=` on the long lines (keep the highlighted token visible) |
| llm-rag/cli.py 184–200 (105, 17 lines), 280–288 (77) · dataset-creator/cli.py 276–294 (84, 19 lines) | windows + `cuts=` / 20 pt |
| everything else the script cites | fits at 22 pt |

## Trackers and the lecture tag

- `tracker(key, step=None, extra=False)` (`"A".."F"`; `tracker_a … tracker_f`) → top-left (left
  −6.5, top 3.5, bottom ≈ 2.9; up to ~8 wide with A2's caption + " · extra"). `SECTIONS`, `STEPS` hold
  the BRIEF's titles/steps ('README › Prerequisites & Service Account' … 'README › Shut down').
- `track(tr, k=None, extra=False)` → Animation (cross-fades the caption in place). Never `tr.goto()`.
- `swap_tracker(scene, old, new, *anims)` plays one tracker turning into another in place (S01
  cycles A–F and back with it).
- `lref("4, 11–13")` → GREY `Lecture 10 · slides …` tag top right (one per scene, BRIEF span).
- Free band for pictures: y from −3.5 (or `STRIP_TOP` −1.44 + 0.15 above a 3-row strip) to 2.8.

## Terminals and tags

| export | purpose |
| --- | --- |
| `term(prompt=P_LAPTOP_HOME, rows=10, title=T_LAPTOP, width=12.6, size=22, place=True)`, `laptop_term(rows, prompt)`, `second_term(rows, prompt=P_API)` | house terminal, bottom edge at `BOTTOM` −3.5; height = rows × 0.403 + 0.85 |
| `resize(scene, t, rows, keep=None, extra=())` | grow/shrink, bottom fixed |
| `type_cmd(scene, t, cmd)` | type at the prompt (replaces a bare prompt; makes room the gentle way; folds long commands; returns the line or a group with `.rows`) |
| `out(scene, t, lines, wrap=False, chunk=None)` | **use this to print**: chunks that fit the box, gentle scroll (old rows fade in place, never sail over the tracker); `wrap=True` breaks at the last fitting space; an over-long line without wrap raises |
| `room(scene, t, n)` | the gentle scroll on its own |
| `bare_prompt`, `cd_prompt(scene, t, new_prompt)`, `istep(scene, t, line)` | prompt returns; prompt changes after `cd`; a container line from an istep capture (sets the capture's own prompt) |
| `t.find("sub")`, `substring(line, "sub")`, `rows_of(line)` | find a row; its glyphs; rows of a folded command |
| `beside(mob, line, min_x=None)` + `pin(scene, line, mob, anim=None)` / `unpin(scene, line, mob)` | a tag right of a row that scrolls with it; `pin` refuses a tag covering text |
| `on_bar(t, tag)` | a row tag on the terminal's title bar (right end) when the command row is too long for a tag beside it (P_LLMRAG + `sh docker-shell.sh` already reaches x ≈ 5). Not part of a row: FadeIn/FadeOut it yourself, and fade it before `resize()` (it does not move) |
| `turn_row() extra_row() time_row() editor_row() cost_row() row_tag(parts, colour)` | row-sized tags (0.36 tall): `▶ your turn` YELLOW, `extra`, `at the time of recording`, `our editor; use yours`, GOLD `this bills your project` |
| `your_turn() extra_tag() illustration_tag() recorded_tag("recorded · rag.py:218–223") recording_tag() erratum_tag() preview_tag() editor_tag() cost_tag(s) future_cost_tag(s)` | house-size tags; GOLD `cost_tag`; S14's GOLD-on-GREY-dashed `future_cost_tag` |
| `flash_tag(scene, tag, colour)` | **plays** a tag flash (word + an unfilled outline copy). Never `Indicate(tag)` and never animate `tag.box` (see traps) |
| `grey_chip(s) dashed_chip(s) tool_chip(s) err_chip(s) file_card(path, colour) card(lines, head=…)` | notes; future/elsewhere; PURPLE tools; RED errors (mono); a file as a card; a plain GREY card (honest note, errata) |
| `note(s, colour=GREY, size=20)` `steady(s, …)` | caption line (**2nd positional arg is the colour**); text that morphs safely |
| `under ring(dashed=) hl_bar strike outline_box arrow(arc=) route(arc=) travel bounce each greyed(m)` | underline; outline box (dashed for "container's view"/"no pass"); translucent bar; strike; dashed↔solid box; GREY arrow; PINK route; ride a path; go-and-return; flash pieces one by one; a greyed copy for `Transform(m, greyed(m))` |

## Glyphs (all ≥ 20 pt; nothing added for you)

`key_glyph()` GREEN key · `magnifier()` PINK glass · `envelope("JWT", sealed=True)` (`.seal` GREEN) ·
`desk_glyph()` BLUE token desk · `Ticket(ticket_w=1.5, text="token", timer=True)` (BLUE, `.life`
arc, `≈ 60 min`; `.run_out()`, `.expire()` animations; ticket_w ≥ 1.45 with the default text) ·
`badge(SA_EMAIL)` the GREEN service-account badge (email on two rows) · `key_card()` the zeroed JSON
key (always tag it `illustration`; `.rows["private_key"]` / `.private_key` to glow RED) ·
`house(name, house_w, house_h, lit=False)` + `lit_house(h, lit)` TEAL container house (base at its
y = 0: `.move_to(p, aligned_edge=DOWN)`) · `door_glyph()` GREY door · `bricks()` ·
`browser_glyph(url=None, glyph_w, name="browser", glyph_h=None)` · `google_building(bw, bh, door,
meter_, text_y)` (columns never cross its name) · `meter()` + `meter_tick(m)` GOLD meter ·
`lock_glyph()` · `EmbeddingBars(256, bars_w, bar_h)` 256 EQUAL BLUE bars (never values) + `.grow()` ·
`riddle_card(i)` / `riddle_label(i)` S01's riddles (S15 brings the labels back).

## Set pieces (`Rig`s: parts built-but-not-shown ride along with shift/move_to/next_to; place a piece BEFORE it plays — an `.animate` move after does not carry them)

**V1 · auth chain** — `AuthChain(teaser=False)` 12.5 × 1.85, centre x = 0. Five slots (`.slots[i]`:
`.frame .glyph .text`): key file → ADC → signed JWT → token desk → bearer token; `.arrows[j]`;
`.url` (`oauth2.googleapis.com/token`, not added: place above slot 3). States 'lit' | 'hollow' |
'grey': `to(i, state)`, `arrow_to(j, state)`, `reveal(i)`, `light_all()`, `grey_out()` →
Animations. `break_at(scene, 0)` plays: the glass finds nothing, the key fades, a RED cross, the chain
greys (returns the cross; fade it yourself). `mint(scene)` plays: timer runs out, ticket greys, a
fresh one mints. `staple(3)` → requests `HTTPS · Authorization: Bearer …` each with a ticket (a
column; place it under the chain). `teaser=True` = S06/S09: key slot lit, four hollow unlabelled
slots. S09's "→ 200" and the 256 bars are scene-level (`EmbeddingBars`, tag `recorded · rag.py:218–223`).

**V1 (S07) · ADC's three places** — `AdcPlaces()` ~9.3 × 3.4 incl. the glass (centre ≈ x 0.3):
rows (`.rows[i]`: `.frame .badge .title .sub`) 1 the file named by GOOGLE_APPLICATION_CREDENTIALS
(GREEN) · 2 `gcloud auth application-default login` (GREY) · 3 the metadata server (GREY dashed,
chip `L13–L15`). `.glass` (not added; FadeIn it). `visit(i)` → Animation; `stop(scene, i)` plays a
RED flash; `enclose()` → (outline, Animation) TEAL "inside a container"; `empty((1, 2))` → rows fade
to empty boxes.

**V2 · IAM grid** — `IamGridRig()` 12.9 × 3.5, centre x = 0. Rows `you`, `llm-service-account`;
columns `your-gcp-project`, `ac215-project`, `project 129349313346`; GREY captions principals /
resources. `token(text, colour, dashed, mono_font)` → chip; `drop(tok, r, c, slot, of)` → Animation
(stacked tokens: SA × your project holds `roles/aiplatform.user` GREEN + `Storage Admin` GREY, `of=2`);
`fire(scene, r, c, ok, text)` plays a PINK request chip under column c, its arrow up into the cell,
the verdict (GREEN check / RED `403` pill, top-right of the cell); returns (request, mark).
Requests need ~0.8 below the grid. `pulse_col(c)` → Animation. Only fire into the bottom row (the
arrow would cross the SA row otherwise). No 403 body text is ever drawn.

**V3 · secrets portal** — `SecretsPortalRig(key_inside=False)` ~12.6 × 3.9: `.tree` (`AC215/` >
`cheese-app-v0/` > three folders; `secrets/` GREEN beside the repo with the key; `.tree.row(name)`),
`.caption` ('your course folder · here: ~'), `.box` (TEAL container: `.title .mount` `/secrets/`
`.file` (key; absent with key_inside) `.lib` 'Google library'), `.host_cap` / `.cont_cap` (not added).
`climb(scene, start="api-service/")` plays `$(pwd)` → `..` → `..` → secrets/ (ring turns GREEN;
returns the ring); `start="llm-rag/"` for the compose beat. `connect()` → the GREEN tube (a staircase
right of the tree: never crosses tree rows); `snap(scene)` plays a dot through the tube, the env var
(2 mono rows) in the box and a PINK pointer onto the file (returns them). key_inside=True (Ponder 1):
the key is RED inside the repo, `climb` ends on `AC215/`, `pop_empty(scene)` plays the empty GREEN
folder + chip 'created by Docker, empty', and `snap` points at the empty `/secrets/`. Move `.tree`
or `.box` freely before `connect()` (the tube is built from where they are). The code panels of S04
do not fit beside it: alternate panel and portal, or show the tree with a panel then the box.

**V4 · two addresses** — `TwoArrows()` ~7.6 × 3.9 (S10): PINK street with loader + chroma, wall door
`8000→8000`, browser on the floor; `dial()` (PINK `llm-rag-chromadb:8000`) / `ring_()` (GREY
`localhost:8000` through the door) → Animations. `PortDoor("3200", "3000", "frontend")` ~10.4 × 2.6
(S11): `tunnel(scene)` plays a GREY `3200` chip that becomes a TEAL `3000` at the door; `brick()` →
Animation. `PortLine()` ~12.4 × 2.4: three bands (schematic widths, not to scale) `0–1023 · system`,
`1024–49151 · registered · pick yours here`, `49152–65535 · dynamic`; `drop(0)` (22, 80, 443),
`drop(1)` (3000, 3200, 8000, 9000), `note_in()` (the dynamic note + `65535`).

**V5 · browser integrator + CORS bouncer** — `CorsBouncer(origin="3200")` ~12.8 × 4.0 (centre
(0, 0.4)): page `localhost:3200` + bouncer at its edge; API house + door `:9000` + guest list `*`;
chroma house + door `:8000` + its two-line guest list (the course's hosted site ·
`http://localhost:3200`, compose :26; it never travels); Google top right. `send(scene, k)` plays
route k (captions `CALLS[k]`; it does not redraw a route already on screen) and packet k; `cloud(scene)`
plays the BLUE ticket to Google and 256 bars back to the page; `preflight(scene, origin)` plays the
OPTIONS knock with its Origin stamp, the list check, and a GREEN pass back to the bouncer — or a RED
dashed "nothing" — and returns True/False; `admit(scene)` (GREEN check, packet ②, ten chunk cards
back) / `refuse(scene)` (packet ② RED at the bouncer); `never_sent(scene)` (route ③ GREY dashed,
'awaits call 2 · ChatComponent.jsx:163–171'); `curl_walk(scene)` (a curl figure straight to door
8000, an answer back); `restamp("3300")` → Animation (address cross-fades in place).
`PacketReplay("3300").replay(scene)` plays the whole :3300 answer of Ponder 4. Tag the flow
`recorded · README.md:217–222 · ChatComponent.jsx:161–173` (script S12).

**V6 · the running map** — `AppMap(laid=(), lit=(), doors=(), drawer=False, tubes=(), gone=(),
folder=False)` 12.75 × 4.05, centred at (0, 0.75) above a 3-row strip (fits exactly between the
strip and the tracker); `AppMap.at("S05")` = the map as the scene starts (`MAP_AT`; kw override).
Laptop frame 'your laptop'; streets `.streets["llm-rag" | "cheese-app"]` (planned GREY dashed /
laid PINK; masked names); houses `.houses["chroma" | "loader" | "frontend" | "api"]` (TEAL, hollow/lit);
inner wall with doors `.doors["8000" | "3200" | "9000"]` (`.glyph .text`, GREY); floor: `.browser`,
`.loop` ('localhost · 127.0.0.1'); `.drawer` (GREEN `secrets/`, top) + `.tubes["loader" | "api"]`;
`.public` street; `.google` (`.door .guard` IAM `.meter`); `.folder` (GREEN docker-volumes/ where
chroma stood). Animations: `lay(k)`, `unlay(k)`, `light(k)`, `darken(k)`, `open_door(p)`,
`brick(p)`, `tube_on(k)`; arrows (not added): `call("browser", house)` (PINK, to its door),
`call("loader", "chroma")` (PINK, along the street), `call(house, "google")` (thin BLUE, up to a lane
over the roofs and across to the IAM door); `.path` for `travel()`. Extras (not added):
`house_loop(k)` (S10's own localhost per house), `phone_book(k, names)` (S10's Docker DNS),
`wifi()` (S11: a Wi-Fi street under the laptop + `.reach[port]` dashed lines; needs ~0.7 below the
map, so not with a strip). Never draw an API ↔ chroma arrow (README:127), never a GREEN door.

**The chat page** — `ChatWireframe(url="localhost:3200/chat", question=QUESTION, picker=None,
row_head=None, fun_fact=False)` 9.6 × 6.0 (centre (0, −0.35) leaves room for an `illustration`
tag above): `.shell` (everything but the question), `type_question()`, `grow_bars()` (five GREY
skeleton bars, no glyphs), `open_drawer()` (ten empty rows; `row_head='book · author · dist'` for
S12); `picker='char-split-collection ▾'` (S12/S13); `fun_fact=True` (S13: last bar is a YELLOW box
"Pavlos' fun fact", README:239). No answer text, ever.

## Traps carried over from L09 (general; each cost time there)

- Emoji/odd glyphs: check that `▲ ✓ ○ ✔` render in DejaVu Sans Mono before relying on
  `substring()` indices on those rows (51: `▲ Next.js 14.2.4`, `✓ Ready`; 21: `✔`). The Bench
  printed `✔` rows fine.
- `words count mismatch` warnings from manim Text (t2c) are harmless; check still OK.
- Anchors: `vo.wait_until()` needs the SAY's exact words (punctuation too); a miss prints
  `voiceover anchor not found` — fix it, never ignore it. Timing is interpolated inside a sentence:
  anchor at clause starts.
- `from common import *` brings lowercase helpers (`code`, `note`, `ring`, `arrow`, `cut`, `cols`,
  `out`, `room`, `card`, `house`, `badge`, `meter`, `envelope`, `squash`, `soft`): don't shadow them.
- Scaling a group that contains text below 1.0 trips SMALL; build it at the size you need and
  Transform. VoiceScene has no camera: "zoom" = fade/shrink the old, `FadeIn(new, scale=1.25)` (S01).
- `set_opacity` on groups with fills makes fills stronger; prefer `fade()`. On a tracker (steady
  text) `set_opacity` reveals the hidden '|' strut: use `fade()`.
- Morphing a labelled box into a chip with FadeTransform stretches its text: fade words first,
  transform bare shapes, fade the new label in. `TransformFromCopy` between different texts smears.
- A `Succession` of two `.animate` builders on the SAME mobject does nothing: separate plays.
- Removing a printed row from `t.lines` right before animating it makes it vanish: animate a copy.
- `pin()`/`attach()` re-add rows and split the terminal in the scene list: fade terminal and
  overlays together, `FadeOut(VGroup(t, bar, ring))`.
- Ponder cards point with YELLOW, never RED.
- One `Indicate` on a group of scattered pieces flies the glyphs off their rows: `each(pieces, c)`.
- **Tags:** never `Indicate(tag)`, never wrap text+box flashes in an AnimationGroup, and (new in L10)
  never animate `tag.box` either — the scene re-adds the box above its own word and the filled box
  hides the word for good (S01's GOLD tag went blank). Use `flash_tag(scene, tag, colour)`.
- `Indicate` on any FILLED shape floods it: indicate its text or outline. A masked label (street
  names have a BG mask): indicate the word (`st.text`), not the group.
- `Terminal.fold` breaks with ` \` even inside quotes; a command whose spaces are all inside quotes
  (the `python -c "…"` probes of 29/41/43/44) should soft-wrap instead, rows joining back to the exact
  command (assert it).
- `Text.text` drops spaces: index `label()`/`mono()` Text via `original_text`. No `Scene.add_to_back`:
  insert behind a row with `row.submobjects.insert(0, bar)`.

## Traps and facts new in L10 (found building common.py and S01)

- Scene-class names collide with set-piece names (fixed: `SecretsPortalRig`, `IamGridRig`).
- `Create` on a VGroup draws its children one after another (lag 1): never put invisible helpers
  first in a group you Create. `_poly` keeps its travel path as an invisible rider, not a child.
- Compose/build progress rows (21, 33, 50) are padded to 110 columns: `squash()` them (whitespace
  only) or `wrap=True` breaks them oddly; `out()` refuses an over-long line.
- Long prompts: `P_LLMRAG`/`P_FRONTEND` + a command leaves no room for a row tag beside it; use
  `on_bar()` or pin the tag to an output row. P_FRONTEND alone is 51 characters.
- The root prompt `6c23fe52ca92:/app#` has no `user@`: it prints uncoloured (`split_prompt` handles it).
- `code()` refuses lines that would leave the frame (66 at 22 pt, 73 at 20 pt): use `cuts=`.
- A pygments CODE panel paints a house `…` pink-red: `code(..., cuts=…)` recolours it GREY; if you
  build a panel yourself, do it with `code_span(p.code, k, "…").set_color(S.GREY)`.
- `Rig` riders follow placement (shift/move_to/next_to/align_to) only; after a piece is on screen,
  move parts with explicit animations.
- Two items that share a route (CorsBouncer ① and ③) are offset (③ starts 0.22 lower); captions of
  ① are faded when ③ or the never-sent caption takes their place.
- Map arrows to Google run in a lane at y ≈ 1.28 (local) over the roofs; the secrets tubes in a
  lane at 1.43. Don't put labels in those lanes.
- Placeholder key: never highlight 06:5 / 21:47's byte size (421), never show the placeholder file.

## Script gaps and decisions taken in common.py / S01 (for the coordinator)

- S01 SHOW says "PINK street stubs" in the V6 skeleton; S02/S05 say streets are GREY dashed
  ("planned") until created. The map uses GREY dashed in S01 too (one rule for the whole video).
- V3's env label "slides along the tube and snaps onto the file": with a 64-character label at
  20 pt it cannot ride a short tube; `snap()` sends a GREEN dot through the tube, then the label
  appears inside the box and a PINK pointer snaps onto the file.
- The BRIEF lists three principals for V2 (incl. the instructor's SA); script S08 (the source of
  truth) has two rows: `you`, `llm-service-account`. The grid follows the script.
- S01's 2-row preview strip types laptop/01's `git clone https://github.com/dlops-io/cheese-app-v0`
  (your turn) and laptop/22's `docker ps` (extra): the script names the tags, not the commands.
- S01's "Python server" / "database" labels before the map are our words for the SAY's; the map
  then names them API / chroma.
- Housekeeping: delete only your own scene's preview folders (`build/preview_l/<stem>`,
  `build/preview_m/<stem>`), never the whole `build/preview_*` — other agents render there at the
  same time (coordinator).
- `on_bar()` places a tag where the terminal is at that moment: after `resize()`, place it again
  (S02; the review bot caught it).
- Terminal rows keep their words verbatim. Only whitespace may change, the house way: table
  gutters via `squeeze`/`squash` (S02 re-spaced `ls -la` columns the same way, asserting the words);
  anything else over-wide gets the house `cut()` "…", or use 20 pt (72 columns).
- Pending common.py changes (coordinator, after the scene builds): `key_card()` drops the comma
  after its last field (S03); `AppMap.call("browser", k)`
  starts all three browser arrows at one point, so the frontend/API arrows nearly overlap; their
  start points will be spread across the browser's top edge. Don't work around it locally.
