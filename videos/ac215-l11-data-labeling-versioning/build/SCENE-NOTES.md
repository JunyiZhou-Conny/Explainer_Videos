# L11 scene contract — `scenes/common.py` (read this, your script section, your BRIEF row, common.py)

Reference scene: `scenes/s01_hook.py` (`Hook`; check OK, no anchor warnings; sheets read:
`build/sheets/s01_hook_Hook/`). Every set piece is exercised by `build/common_test.py` (`Bench`); its
sheets `build/sheets/common_test_Bench/sheet_0{1..5}.png` show what each piece looks like. Run it
before you change how you call a piece:
`python -m explainer.check videos/ac215-l11-data-labeling-versioning/build/common_test.py Bench --tts silent`.
**Do not edit `common.py`** (shared; agents run in parallel): work around locally, put requests in
your report.

## Setup, checks, scene skeleton

```bash
cd /home/user/Explainer_Videos && source .venv/bin/activate
export PYTHONPATH=/home/user/Explainer_Videos EXPLAINER_TTS=kokoro EXPLAINER_VOICE=af_heart EXPLAINER_SPEED=0.9 PYTHONHASHSEED=0
D=videos/ac215-l11-data-labeling-versioning
python -m explainer.check   $D/scenes/sNN_x.py Cls            # must print OK
python -m explainer.preview $D/scenes/sNN_x.py Cls --every 3  # read every sheet
python -m explainer.preview $D/scenes/sNN_x.py Cls --at 12.5,30 -q m   # exact frames
```
480p only, one render at a time, foreground with a long timeout. First run synthesizes the voice.
Importing common takes ~25 s on a busy CPU (it reads script.md, video.yaml and the captures).

```python
from manim import *  # noqa: I001  (manim first, then common: common must win)
from explainer.scene import VoiceScene
from explainer import style as S
from common import (...)            # name what you use (or `from common import *`)

SAY = NARRATION["S07"]              # SAY lines verbatim from script.md, in order
class LabelsAndTokens(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S07"] == 8, len(SAY)
        with self.voiceover(SAY[0]) as vo:     # exactly one block per SAY line, in order
            ...; vo.wait_until("exact phrase from the SAY"); ...
        ...
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)   # end on an empty frame
        self.remove(*self.mobjects)
```

### Scenes (video.yaml) and what each needs

| id | file | class | trackers | lref (`lref("…")`) | set pieces | ponder |
| --- | --- | --- | --- | --- | --- | --- |
| S01 | `s01_hook.py` | `Hook` | none (A–L preview) | 20, 24 | — | — |
| S02 | `s02_map.py` | `TwoStations` | A1→A2 | 4–6, 8–12 | V7 built | 8 s |
| S03 | `s03_photos.py` | `KeyAndPhotos` | A3→A6 | 5–6, 11 | V7 | QUICK 4 s |
| S04 | `s04_studio.py` | `StudioInABox` | B1→B4 | 7, 13–14 | V1 build | 6 s |
| S05 | `s05_storage.py` | `WhoTouchesBytes` | B5→B6 | 6–7, 13 | V2 (+ V3 teaser) | 8 s |
| S06 | `s06_cors.py` | `CorsOnTheBucket` | C1→C4 | 13 | V3, V1, V7 | 8 s |
| S07 | `s07_labels.py` | `LabelsAndTokens` | C5→D3 | 4, 6, 10, 13 | V2 envelope, V1 calls, V7 | 6 s |
| S08 | `s08_compose.py` | `ComposeAndClean` | E1→F4 | 12 | V1 compose, V7 (part-1 end) | 6 s |
| S09 | `s09_repo.py` | `YourOwnRepo` | G1→G5 (opening: none) | 20, 23, 26 (`low=True`) | V6 silhouette, V7 | — |
| S10 | `s10_bucket.py` | `BucketAsFolder` | H1→I1 | 21, 27–34 | V4 + MountLayers, V7 | — |
| S11 | `s11_build.py` | `StarterFix` | I2→I3 (+ extra row) | 26, 29–32 | V4 broken, MountLayers | 8 s |
| S12 | `s12_fingerprints.py` | `Fingerprints` | J1→J3 | 20, 23, 25 | V5 (prediction), MountLayers, V7 | 8 s |
| S13 | `s13_pointer.py` | `PointerAndBytes` | J4→J6 | 22–23, 25, 33 | V6 build | — |
| S14 | `s14_v21.py` | `SecondVersion` | K1→K4 | 20 | V5 second, V6 v21 | 8 s |
| S15 | `s15_colab.py` | `TimeTravel` | J6, K5 | 22, 26 | V6 pull + failures | 6 s |
| S16 | `s16_recap.py` | `Recap` | L1→L3 (monitoring/recap: none) | 25, 35–36, 38–40 | V7 complete → dark, recap marks | QUICK 4 s |

The script is the source of truth for the exact trackers, tags and ponder texts; this table is a map.
SAY counts (`SAY_COUNT`): S01 5 · S02 7 · S03 7 · S04 8 · S05 6 · S06 8 · S07 8 · S08 7 · S09 6 ·
S10 8 · S11 6 · S12 11 · S13 6 · S14 7 · S15 6 · S16 7. A PONDER goes right after its SAY block:
`card = ponder(self, "question\nlines", seconds=8)` (6 where the script says 6); `QUICK(4 s, …)` is
`quick_predict(self, "…")`. FadeOut the card at the start of the next block. The card is opaque
(it may sit over a set piece); `center=(x, y)` / `width=` move or narrow it. Ponder texts are in
script.md (`PONDER(...)`), not in common.py.

**Name collision (binding):** no common.py export is named like a scene class (checked). Never
define a module-level name that shadows a common.py export either (S01 renamed its question string
to `HOOK_QUESTION`: `CAPTION` is common's 20-pt size constant).

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
  never cut: `type_cmd` folds at a space with ` \` (or `soft=True`, see traps).
- `FadeOut(g)` takes the family off the scene and restores opacity: a faded child that stays in its
  parent snaps back when the parent is animated. Remove it from the parent or fade the parent.
- Never play `FadeIn(piece)` and an animation of one of its parts in the same `play()`.
- No invented numbers, outputs, task counts, expiry times, object names, file sizes, accuracy,
  key/token/JWT material — not even under `illustration`. Every number is from a capture, a source
  file or ASSETS.md; schematic ideas use symbols (the signed URL's hourglass has no value; the
  token field is drawn blank). Stand-in numbers carry their tag ("ours: 3 · yours: 21").
- Prefer transforms that show what became what.

### Names, personal data and quotes (binding; series rule)

- **The instructor's name never appears on screen.** `capture()` and `source_text()` /
  `excerpt()` / `code()` / `readme()` / `source_rows()` already mask it: `unname()` turns
  "Pavlos", "Pavlos Protopapas", "Protopapas" (any case) and the Colab extracts' `<course
  instructor>` into `‹instructor›`; `mask()` turns every e-mail but the placeholder into
  `student@example.com` (so `docker-shell.sh:19`, `docker-compose.yml:31`, README:109/204/206 render
  the placeholder) and a GitHub user in a data-versioning URL into `YOUR_GITHUB_USERNAME`. Never
  read a file with `open()`/`Path.read_text()` for on-screen text, never type a name or an e-mail
  into a label, a card or a chip; the narration says "the instructor".
- Placeholders only: user `student`, login `LOGIN` (`student@example.com` / `awesome`), bucket
  `BUCKET` (`your-bucket-placeholder`), project `PROJECT_ID` (`your-gcp-project`), GitHub user
  `GH_USER`, token `TOKEN` (`student-demo-token-not-a-secret`, always with `fake_chip()`). The
  README's `ac215-project` and the class bucket `cheese-app-data-versioning` (`CLASS_BUCKET`) appear
  only inside quoted source/README lines and RED class-repo beats, never highlighted alone, never as
  ours. Commit metadata, tagger names and the notebook's run dates are never shown.
- No slide images, console/Label Studio/Colab screenshots, logos; schematic windows carry
  `illustration_tag()`; one `lref(...)` per scene (table above).

## Colours (BRIEF table; names in common.py)

`LAPTOP` GREY (host shell, host filesystem, the browser, the host's dark `cheese_dataset/`,
`.dvc/cache`) · `CLOUD` BLUE (both buckets, storage.googleapis.com, `dvc_store/`, Colab, the
signed-URL ticket) · `IMAGE` = `CONTAINER` TEAL (data-label-studio, data-label-cli,
data-version-cli, the compose one-off) · `SYSTEM` = `ROOT` ORANGE (root-owned folders, uid 1001 vs
root, git's ownership check, apt, `--privileged`, `/dev/fuse`) · `OWNED` = `SECRET` = `KEY` =
`POINTER` GREEN (the secrets/ key, `.dvc/config`, `cheese_dataset.dvc`, tags/flags) · `PASS` GREEN
(a check that passed) · `TOOL` PURPLE (docker, compose, git, dvc, gcsfuse, gcloud, uv, the SDK) ·
`ERR` RED (400/401, Exited (1), the failed build, the entrypoint's failure chain, refusals, the
empty-folder version) · `TURN` YELLOW (your turn, tracker, look-here, ponder pointers; never RED for
pointing) · `COST` GOLD (money only: storage, the second copy in dvc_store/, what keeps billing) ·
`ROUTE` = `HASH` PINK (the Docker street + DNS, mount pipes, md5 strings and shelf paths, the
tag → blob rope) · `FUTURE` GREY dashed (L13, lakeFS/Delta/Iceberg, monitoring, the class bucket) ·
`DOOR` GREY (an open published port: never GREEN) · `NOTE` = `INK` WHITE (an annotation envelope).
Episode-local: two buckets, always two BLUE shapes; the signed URL is a BLUE ticket with a wax seal
and an unlabelled hourglass; an annotation is a WHITE envelope with only its label word; the CORS
bouncer stands at the browser's door facing the page, the rule card sits on the bucket.

## Data, captures, sources

| export | purpose |
| --- | --- |
| `NARRATION["Snn"]`, `SAY_COUNT`, `TITLES[cls]`, `SPEC` | SAY lines from script.md; titles; video.yaml |
| `capture("41")` / `capture("41-docker-shell-CLI")` / `capture("laptop/41")` / `capture("C13")` → `Capture` | the one file `assets/terminal/laptop/NN-*.txt` (`C…` → `colab/`); `capture-only/` and `119` refused; names masked |
| `Capture.cmd .lines .exit .raw .path` | command as typed; output body (no `[exit N]`); every file line (tabs → 8 spaces) |
| `.at(2, (5, 7), "…", 33)` · `.line(n)` · `.istep(n)` | lines by FILE number; one file line; `(prompt, typed)` of an istep line |
| inline `[exit N]` | split off automatically (`20:2`, `27:2`) |
| crops (`NEVER`, `NEVER_RE`) | refused by `.line()`: `19:8–9`, `63:5–6`, `72:5–6`, `152:6–7`; every `Added environment …` line, every `172.17.0.1` line, every gcsfuse JSON `"severity":"INFO"` line (33–38 and 40 of 88/90/93/95/104/115/117; 34–39, 41 of 145) |
| istep captures | `41 42 44 54 88 90 93 95 104 115 117 145` hold prompt + typed line: `istep(scene, t, cap.line(n))` sets the capture's own prompt (`app@…:/app$`, `root@…:/app#`) and types the rest |
| `reenter(scene, t, "93")` + `reentry_chip()` | the DVC-container re-entry (93, 95, 104, 115, 117; 90): types `sh docker-shell.sh`, prints 27–28, `…`, 41–42, sets the container prompt; add the chip "same entrypoint errors as before" yourself |
| `container_note()` | GREY "our capture: a fresh container for each step · stay in yours" (second container prompt of a scene) |
| `split_prompt(s)` | `app@5bf8945fb887:/app$ …`, `root@d5bf95465b66:/app# …` → (prompt, typed) |
| `cut squeeze cols squash soft` | cut after a marker + `…`; re-align a docker table; keep named columns (`cols(capture("11").at((2, 3)), ["STATUS", "PORTS", "NAMES"])`); collapse build/compose padding; break long lines at a space |
| `readme(n, repo="data-labeling")` | README line n, stripped and masked; repo `data-versioning` (pin b240b1a), `data-versioning@data-versioning-ac215` (starter), `data-versioning@2515e5e` (today). README commands sit in prose/backticks: `capture("11").cmd in readme(91)` |
| `source_text(path)`, `excerpt(path, a, b)`, `shown_path(path)` | `data-labeling/…`, `data-versioning/…`, `data-versioning@data-versioning-ac215/…` (header "starter ·"), `data-versioning@2515e5e/…` ("README today · 2515e5e ·"), `colab/notebook-1RRQ1SlH.cells.txt` ("notebook ·") |
| `code(path, a, b=None, language=None, focus=None, font_size=22, shown=None, max_lines=12, cuts=None, dedent=False)` | CODE panel, header `data-labeling · docker-shell.sh · lines 12–23`. Raises on > 12 lines and on a line too long for the frame (> 66 chars at 22 pt, > 73 at 20 pt): `cuts={21: '"/secrets/'}` (house `…`, recoloured GREY) or `font_size=20`; `dedent=True` drops the common indentation only. Highlight with `code_span(p.code, k, "sub")`, `line_bar(p.code, k, colour)`, k = file line − a. Notebook: `code("colab/notebook-1RRQ1SlH.cells.txt", a, b, shown="notebook · cell 15")` |
| `source_rows(path, n, size=20, width=None, indent=4)` | one source line no panel can hold, broken at a space into rows (text unchanged): the starter's `docker-entrypoint.sh:10` (81 chars). `.rows .text` |
| `readme_card(lines, body, quote=False, card_w=None, size=22, repo=None)` | GREY README quote card `README.md · line n` / `lines a–b`; `repo="data-versioning"` names the README |
| `IMAGES MD5 SIZES V20 V21 EMPTY CLASS_V21 HOOK_LINE POINTER_LINES short(h) aisle(h)` | Image_1–5.jpg, their md5s and sizes (09b), the v20/v21/empty pointer fields (95/104/93), the class repo's v21 (C-files), the hook's md5 line (95:59), the six pointer lines (95:58–63); `short()` = first 8 + `…` (+ `.dir`), `aisle()` = `5b/` |
| prompts / titles | `P_LAPTOP_HOME` (= `P_LAPTOP`) `P_LABELING P_VERSIONING P_TODAY P_TODAY_DV P_COLAB` · `T_LAPTOP T_SECOND T_TODAY T_COLAB`; container prompts come from each capture (no P_CLI/P_DVC constants) |
| strings | `PROJECT_ID BUCKET BUCKET1 CLASS_BUCKET GH_USER LOGIN TOKEN SA_NAME KEY_FILE KEY_PATH ENV_VAR NETWORK STORAGE_HOST PAGE_ORIGIN CONTAINERS CHOICES SLIDE6_ROWS STAGES STAGES_2L CORS_RULE ACAO MOUNT_CHIPS COMMITS BEAD_NAMES SLIDE6` |

Every CODE ref of script.md, measured (longest line; tested calls):

| CODE ref | call that works |
| --- | --- |
| `data-labeling/docker-shell.sh: 5–9` (line 6: 107) | `code(p, 5, 9, font_size=20, cuts={6: "|| "})` (YELLOW line 6 keeps `inspect … ||`; the sticky note says "inspect … \|\| create") |
| `data-labeling/docker-shell.sh: 12–24` (13 lines; 21: 74) | two windows `12–23` then `13–24`, each `cuts={21: '"/secrets/'}` (22 pt) — the "scrolls one line at the end" of S04 |
| `data-labeling/docker-shell-CLI.sh: 15–25` (20: 74) | `cuts={20: '"/secrets/'}` (22 pt), or `font_size=20, cuts={20: '"/secrets/data-service-account.json"'}` |
| `data-labeling/cli.py: 22–34` (13 lines; 30: 82) | windows `22–33` / `23–34` with `cuts={30: '"Content-Type",'}` |
| `data-labeling/cli.py: 75–83` (78: 96, 79: 71) | `font_size=20, cuts={78: "SDK: "}` |
| `data-labeling/docker-compose.yml: 13–18` (14: 78) | `dedent=True, font_size=20` (line 17 RED stays whole) |
| `data-versioning@data-versioning-ac215/docker-shell.sh: 5–10` (10: 74) | `cuts={10: '"/secrets/'}` |
| `…ac215/docker-shell.sh: 17–27` (24: 67) | `font_size=20` |
| `…ac215/docker-entrypoint.sh: 8–13` (8: 79, 10: 81) | `font_size=20, cuts={8: "activate-service-account", 10: "$GCS_BUCKET_NAME"}`; where line 10 itself matters (the chips beat), show it whole with `source_rows(p, 10)` and `mount_chips()` over it — never cut `/mnt/gcs_data` off a line you highlight |
| `…ac215/Dockerfile: 36` (68) | `font_size=20` (or `dedent=True` at 22) |
| `docker-shell-CLI.sh: 23`, `docker-shell.sh: 19–20`, `docker-compose.yml: 19–20`, `…ac215/docker-entrypoint.sh: 11`, `…ac215/.gitignore: 3`, `data-versioning@2515e5e/README.md: 76–82` | fit at 22 pt |

All 134 `TERM(...)` refs of script.md load with these loaders (none hits a crop); `86` is 1,126
lines (print 1075–1081 and 1125 cut after `failed to solve:`); `54:126` prints the JSON, then the
prompt and the typed command continue on the same row.

## Trackers and the lecture tag

- `tracker(key, step=None, extra=False)` (`"A".."L"`; `tracker_a … tracker_l`) → top-left (left
  −6.5, top 3.5, bottom ≈ 2.9). `extra` = `True` (" · extra"), `"Linux"`, `"stand-in"`,
  `"local remote"`, or `"row"` for H/I's extra row ("upload the first photos", "Dockerfile:36 fix",
  a hollow dot after the steps). `SECTIONS`, `STEPS` hold the script's titles/steps.
- `track(tr, k=None, extra=False)` → Animation (cross-fades the caption in place). Never `tr.goto()`.
- `swap_tracker(scene, old, new, *anims)` plays one tracker turning into another in place (S01
  cycles A–L and back with it; use it wherever a scene changes section, e.g. C→D, E→F, H→I, J→K).
- `lref("7, 13–14")` → GREY `Lecture 11 · slides …` tag top right. Tracker G's heading reaches
  x 2.35: in S09 use `lref("20, 23, 26", low=True)` (one row lower).
- Free band for pictures: y from −3.5 (or `STRIP_TOP` −1.44 + 0.15 above a 3-row strip) to
  `PIC_TOP` 2.8. Every set piece below is built for the band above a 3-row strip.

## Terminals and tags

| export | purpose |
| --- | --- |
| `term(prompt=P_LAPTOP_HOME, rows=10, title=T_LAPTOP, width=12.6, size=22, place=True)`, `laptop_term(rows, prompt)`, `second_term(rows=3, prompt, title=T_SECOND)`, `colab_term(rows=3)` | house terminal, bottom edge at `BOTTOM` −3.5; height = rows × 0.403 + 0.85; `second_term(3, P_TODAY, T_TODAY)` is the route-T strip, `colab_term` the Colab stand-in (`$`) |
| `resize(scene, t, rows, keep=None, extra=())` | grow/shrink, bottom fixed |
| `type_cmd(scene, t, cmd, type_time=None, soft=False)` | type at the prompt (replaces a bare prompt; makes room; folds long commands with ` \`; `soft=True` soft-wraps at the edge instead — for a command whose spaces are inside quotes, e.g. the `sed` edits of 40/85/87; returns the line or a group with `.rows`) |
| `out(scene, t, lines, wrap=False, chunk=None, color=OUTPUT)` | **use this to print**: chunks that fit the box, gentle scroll; `wrap=True` breaks at the last fitting space (tracebacks, Label Studio JSON, gcsfuse errors, 401s); items may be `(text, colour)`; an over-long line without wrap raises |
| `room(scene, t, n)`, `bare_prompt(scene, t)`, `cd_prompt(scene, t, new_prompt)`, `istep(scene, t, line)` | gentle scroll; prompt returns (→ no output); prompt changes after `cd`; a typed container line from an istep capture |
| `t.find("sub")`, `substring(line, "sub")`, `rows_of(line)` | find a row; its glyphs; rows of a folded command |
| `beside(mob, line, min_x=None)` + `pin(scene, line, mob, anim=None)` / `unpin(scene, line, mob)`, `attach`, `covers_text` | a tag right of a row that scrolls with it; `pin` refuses a tag covering text |
| `on_bar(t, tag)` | a row tag on the terminal's title bar (right end) when the command row is too long; FadeIn/FadeOut it yourself, fade it before `resize()` and place it again after |
| `turn_row() extra_row(kind) standin_row() local_row() time_row() editor_row() cost_row() row_tag(parts, colour)` | row-sized tags (0.36 tall): `▶ your turn` YELLOW, `extra` / `extra · Linux` …, `extra · stand-in`, `extra · local remote`, `at the time of recording`, `our editor; use yours`, GOLD storage tag |
| `your_turn() extra_tag(kind) standin_tag() local_tag() stand_in_label() illustration_tag() recorded_tag("recorded · cli.py:40 + :26–33") recording_tag() erratum_tag() preview_tag() editor_tag() cost_tag(s)` | house-size tags. `cost_tag` refuses an amount (no `$`, cents, USD): sizes and "a fraction of a cent a month" only |
| `flash_tag(scene, tag, colour)` | **plays** a tag flash. Never `Indicate(tag)`, never animate `tag.box` |
| `grey_chip(s) dashed_chip(s) tool_chip(s) err_chip(s) fake_chip() differ_chip() file_card(path, colour) card(lines, head=…) strip_head(call)` | notes; future/elsewhere; PURPLE tools; RED errors (mono); "obviously fake"; "yours will differ" (ids, our hashes); a file as a card; a plain GREY card (honest note, errata); the stand-in strip's heading `POST /api/storages/gcs/validate · stand-in` |
| `note(s, colour=GREY, size=20)` `steady(s, …)` `tag_on(mob, s)` | caption line (**2nd positional arg is the colour**); text that morphs safely; a tag placed next to a mob |
| `under ring(dashed=) hl_bar strike outline_box arrow(arc=) route(arc=) travel bounce each greyed(m)` | underline; outline box; translucent bar; strike; dashed↔solid box; GREY arrow; PINK route; ride a path; go-and-return; flash pieces one by one; a greyed copy for `Transform(m, greyed(m))` |

## Glyphs (all ≥ 20 pt; nothing added for you)

`tile(name, tile_w=0.6, colour, broken=False, filled=False)` a photo as a blank tile (never a photo) ·
`annotation(word="gouda")` WHITE envelope · `drawer(name, colour, glyph=True, dashed=False)` a
folder/prefix · `vault(title, drawers, colour)` a bucket (`.drawers[name]`) · `url_ticket(name)` the
BLUE signed URL (`.glass .seal`) · `hourglass()` · `wax_seal()` · `bouncer()` · `stopwatch("started")`
· `flag(name, colour, dashed=False)` + `flag_at(f, point)` · `bead()` · `sticky(s)` a `-e` note ·
`slip(s)` PINK md5 slip · `blob(h)` a stored file · `machine("md5")` PURPLE hash machine
(`.mouth .chute`) · `task_cards(21)` blank task cards · `window(url, w, h)` / `page_window(url)` /
`browser_glyph(url)` schematic browser (tag `illustration`) · `house(name, house_w, lit, dashed)` +
`lit_house(h)` TEAL container house · `door_glyph()` · `bricks()` · `key_glyph()` GREEN key ·
`lock_glyph()` · `pipe(points, colour, dashed)` a mount tube · `street(a, b, y, laid)` +
`lay_street(st)` · `phone_book(names)` Docker DNS card · `pointer_card(md5, size_, nfiles)` the GREEN
six-line `cheese_dataset.dvc` (blank fields = GREY underscores) · `manifest_card(names, md5s=None)`
the `.dir` manifest (`.names .md5s`) · `mount_chips()` slide 34's four chips (`.chips`, `.implicit`
the dashed `--implicit-dirs`, not in the group).

## Set pieces (`Rig`s: parts built-but-not-shown ride along with shift/move_to/next_to/align_to; place a piece BEFORE it plays — an `.animate` move after does not carry them)

**V1 · `StationMap(laid=False, lit=("studio",), shown=(), size=20)`** — 12.6 × 3.9 at (0, 0.75), the
band above a 3-row strip; never scale it. GREY laptop frame; `.street` (GREY dashed until `lay()`),
`.studio` TEAL house, `.cli` (not added), `.wall`, `.door` (`8080:8080`), `.browser`, `.db` (GREY
'database' drawer = docker-volumes/label-studio), `.secrets` (GREEN), `.pipes['db'|'secrets'|'cli']`,
`.notes['login'|'key path']`. Animations: `lay()`, `light(k)`/`darken(k)` (`'studio'|'cli'`),
`open_door()`, `pipe_on(k)`, `stick(k)`, `tip_over()`/`stand_up()` (Exited (1) / after chown),
`alert(ROOT)` (db drawer ORANGE root-owned) / `alert(LAPTOP)` (fixed), `join_cli()`. Builders (not
added): `call("browser")` (PINK floor → door → house, label `localhost:8080`), `call("name")` (CLI →
studio along the street, `data-label-studio:8080`), `call("local")` (the CLI's own localhost arc;
`.cross` RED, FadeIn it), `phone()`, `blanket()` (`.box .text`), `order()` (`.arrow .watch`),
`ghost()`. Show together: notes + pipes (S04); calls + phone (S07); blanket + order + ghost (S08).
`shown=` pre-adds parts (`("cli", "door", "browser", "db")`). S04 builds it over the docker-shell.sh
windows: alternate panel and picture (a full panel and the map do not share the frame).

**V2 · `SignedTicket(size=20)`** — 12.6 × 3.95 at (0, 0.75). Laptop (TEAL `.studio` with the GREEN
`.key`, `.db`, `.browser`, `.bouncer` not added) and the BLUE vault `.vault` (`.drawers
['cheeses_unlabeled/'|'cheeses_labeled/']`, `.door`, `.host` storage.googleapis.com). `reach(scene)`
plays (returns the arrow); `cards(21)` + `fan(cards)`; `hand()` the 'task 1?' bubble; `relay()`
(`.route` then `.strike`: the crossed-out relay); `stamp(scene)` plays (fade the bubble and the cards
except `cards[:7]` first) → ticket; `walk(scene, ticket)` → (route, tile, check), the tile bounces off
the bouncer (FadeIn `.bouncer` first). S07: `envelope_to_db(scene, "gouda")` → env (stops at the db
drawer), `copy_out(scene, env)` → (copy, thread, photo tile) — the photo never moves.

**V3 · `OriginGate(size=20)`** — ~12.6 × 4.5 at (0, 0.2); no terminal beside it. `.page` (broken
`.tile`), `.origin_l/.parts_l`, `.bucket` (empty dashed `.slot`), `.origin_r/.parts_r`, `.bouncer`.
`differ()` → Animation; `deliver(scene, header=False)` → (pkg, RED cross) / `header=True` → (pkg,
GREEN check, tile fills); `rule()` the GREEN rule card (CORS_RULE = cli.py:26–33's values) +
`stick(scene, card)`; `preflight()` (`.line .knock .max_age .caption`, not added: OPTIONS knock,
'preflights only · a plain GET has none'); `curl_walk(scene)`; `other_bucket()` (Ponder: 'your
other bucket', `.slot`). CORS is a browser rule, never "access control"; the bouncer is GREY.

**V4 · `FuseMount(size=20)`** — 12.6 × 4.0 above a 3-row strip. `.stages[i]` (`STAGES`, slides
29–32), `.bucket` (whole bucket: images/ + dvc_store/), `.box` data-version-cli with `.key`, `.mnt`
+ `.mnt_images`, `.app`, `.dvc` (not added); pipes `.gcsfuse`, `.bind` + labels. `stage(i)`,
`authenticate(scene)` (plays), `mount()`, `bind_on()`, `use()`, `fetch(scene)` (plays; returns the
tile), `side_note()` (line 8: "gcloud's own login · not used by gcsfuse or DVC"), `sign()` (YELLOW 'GCS
bucket mounted'), `inside_only()` (Ponder 7), `broken(scene)` (S11: key crossed, pipe stops short RED
dashed, 'special device does not exist'; returns the marks). The entrypoint panel does not fit
beside it: show the panel, then the picture (or the 3-row strip under it).
**`MountLayers(size=20)`** — 12.5 × 3.25 (+ a label line above and below) above a 3-row strip:
`.laptop`, `.host` (data-versioning/ with the dark `.host_data` row), `.box` (TEAL container) with
the `/app` window `.app` (`.app_data`) and `.mnt`; `.bucket` outside. `light_v()` (GREY `-v` pipe +
label above), `light_fuse()`, `light_inner()` (PINK `mount --bind` + label below), `photos(4)`
(blank tiles in /app/cheese_dataset, `illustration`), `dark()` (the host row dims), `absent()` (the
inner bind GREY dashed: nothing mounted, S12). The host's `cheese_dataset/` is never drawn holding
photos.

**V5 · `HashShelf(size=20)`** — 12.6 × 4.0 above a 3-row strip. `.tiles[name]` (Image_5 waits, not
added), `.machine`, `.rack` ('.dvc/cache', rows per aisle appear when used). `hash_photo(scene, n)`
(plays; the real md5 from 09b on its aisle — `5b/` twice), `manifest()` (fade the tiles first),
`hash_manifest(scene, card, predict=True)` (`????????….dir` on `??/`) / `predict=False`
(`89db50de….dir` on `89/`), `pointer(predict=True)` + `confirm(scene, card)` (95:59–61 fill the
fields), `git_box(card)`, `empty_run(scene)` (the `d7/` empty version, RED; recolour GREY later),
`second(scene)` (S14: Image_5 → `54/`, old aisles 'already on the shelf', v21 manifest `6b/`),
`rename(card)` (Ponder 8: Image_2.jpg → brie_2.jpg). Played in S12 **as a prediction before any
`dvc add` output**.

**V6 · `TagRope(size=20)`** — 12.6 × 4.0 above a 3-row strip. `.line` with `.beads[0..2]`
(`BEAD_NAMES`; 1–2 not added), `.flags['dataset_v20'|'dataset_v21']`, `.card` (pointer, not added),
`.store` dvc_store/ with `.dirs['v20'|'v21']`, `.blobs[name]`. `bead(i)`, `plant(tag)`, `zoom()`,
`rope(v)` (not added: FadeIn the dir and blobs, `Create(rope.main)`, then the `rope.fans`), `hop(tag)`
(`.cursor`), `pull(scene, v)` (S15: Colab `.colab` clones at the tag, `.config` chip, manifest then
blobs, tiles appear), `stop_at_manifest(scene)` (RED 401, C13), `ghost("dataset_v25")`, `burn(scene)`
(recap Q5), `homes()` (the three homes of the bytes; shown alone), `silhouette()` (S09's 2 s sketch).

**V7 · `PipelineMap(secrets=False, lit=(), size=20)`** — 12.9 × 3.7, built in place above a 3-row
strip (body y −1.3 … 2.37, the thin slide-6 strip `.slide6` at 2.38 … 2.9 under the tracker); never
scale it. `PipelineMap.at("S08")` = the map as that scene starts (`MAP_AT`; kw override). Pieces
(`MAP_PIECES` + `labeled`): houses `studio cli dvc`, `street`, `bucket1` (+ `labeled` drawer),
`bucket2`, `repo` (+ `flag_v20`, `flag_v21`), `colab`, links `fuse`, `remote`; `.secrets` + `pipe_on
(k)`; `.bridge` ('not connected in the code · exercise E7'); `.tower` (S16 monitoring, not added);
`.slide6_big` (slide 6 full size: `.unlabeled .question .labeled .training`) + `to_strip()`;
`.cli_caption` (S02: fade it before `pipe_on('cli')`). `light(*keys)` / `unlight(*keys)` /
`all_dark()` → Animations; `mark(k)` recap badges ('door', 'ticket', 'rule', 'bouncer', 'envelope',
'fuse', 'shelf', 'rope'). Each scene lights its own piece; S08 ends part 1 with the labeling half
lit; S16 adds the tower, shows it complete, then `all_dark()`.

## Traps carried over from L09/L10 (general; each cost time there)

- Glyphs: `▶ ✓ ✔ …` render in DejaVu Sans Mono; check before relying on `substring()` indices on rows
  that hold other symbols.
- `words count mismatch` / "of the lines (1/1)" warnings from manim Text are harmless; check still OK.
- Anchors: `vo.wait_until()` needs the SAY's exact words (punctuation too); a miss prints `voiceover
  anchor not found` — fix it, never ignore it. Anchor at clause starts.
- `from common import *` brings lowercase helpers (`code`, `note`, `ring`, `arrow`, `cut`, `cols`,
  `out`, `room`, `card`, `house`, `drawer`, `vault`, `tile`, `flag`, `bead`, `slip`, `blob`, `pipe`,
  `street`, `machine`, `window`, `squash`, `soft`, `short`, `aisle`, `mask`): don't shadow them.
- Scaling a group that contains text below 1.0 trips SMALL; build it at the size you need and
  Transform. VoiceScene has no camera: "zoom" = fade/shrink the old, `FadeIn(new, scale=1.25)`.
- `set_opacity` on groups with fills makes fills stronger; prefer `fade()`. On a tracker use `fade()`.
- Morphing a labelled box into a chip with FadeTransform stretches its text: fade words first,
  transform bare shapes, fade the new label in. `TransformFromCopy` between different texts smears.
- A `Succession` of two `.animate` builders on the SAME mobject does nothing: separate plays.
- Removing a printed row from `t.lines` right before animating it makes it vanish: animate a copy.
- `pin()`/`attach()` re-add rows and split the terminal in the scene list: fade terminal and
  overlays together, `FadeOut(VGroup(t, bar, ring))`. A ring attached to a printed row can stop
  rendering until the next scroll: keep it free until just before the next typed command.
- One `Indicate` on a group of scattered pieces flies the glyphs off their rows: `each(pieces, c)`.
- **Tags:** never `Indicate(tag)`, never animate `tag.box`: `flash_tag(scene, tag, colour)`.
- `Indicate` on any FILLED shape floods it: indicate its text or outline. A masked street name:
  indicate `st.text`, not the group.
- `Terminal.fold` breaks with ` \` even inside quotes: a command whose spaces are inside quotes
  (the `sed` edits) uses `type_cmd(..., soft=True)`; rows join back to the exact command.
- `Text.text` drops spaces: index `label()`/`mono()` Text via `original_text`. No `Scene.add_to_back`:
  insert behind a row with `row.submobjects.insert(0, bar)`.
- `Create` on a VGroup draws its children one after another: never put invisible helpers first.
- `Rig` riders follow placement only; after a piece is on screen, move parts with explicit animations.
  A rider is not a child: `FadeOut(piece)` leaves a shown rider on screen — fade it with the piece.
- A `track()` played inside `unpin(...)` can split the tracker into parts on the scene; keep the whole
  tracker family when clearing.
- Animating slices of a Text splits the parent: remove the parent and animate explicit pieces.
- Delete only your own preview folders (`build/preview_l/<stem>`, `build/preview_m/<stem>`), never
  the whole `build/preview_*`: other agents render there at the same time.

## Traps, facts and decisions new in L11 (building common.py, the Bench and S01)

- `MountLayers`: the `/app` window used to stick out of the container box onto the host repo; it now
  sits inside (container x −2.3 … 3.3, `/app` −2.15 … 2.84, photo tiles 0.3 wide). Don't move `.app`.
- `ponder()` cards are opaque now (the 0.96 fill let a set piece's words ghost through in L10 S08).
- The starter's `docker-entrypoint.sh:10` (81 chars) fits no panel line: cut it in the panel, show it
  whole with `source_rows()` where it matters (see the CODE table).
- Faint 15-px dark bars beside card edges in preview frames are h264 artefacts of the low-quality
  preview (a still render of the same frame is clean): don't chase them.
- Stand-in panels (23, 24, 27, 28, 30–33, 43) are output-only strips: never type their curl lines;
  head them with `strip_head("POST /api/storages/gcs/validate · stand-in")` and tag `extra · stand-in`.
- `git push` (83, 100, 109) and the SSH clone (73): typed, **no output panel**.
- Our v21 manifest `6b342844….dir` (V21) differs from the class's `3280f8f9….dir` (CLASS_V21): never
  compared as "should match"; only v20 matches (121).
- S01: the checklist's GOLD tag reads "storage: a few MB, a fraction of a cent a month"; the recorded
  chip of the layout preview is the plain `recorded_tag()`.
