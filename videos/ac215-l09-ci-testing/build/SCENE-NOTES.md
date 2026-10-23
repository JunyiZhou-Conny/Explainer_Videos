# L09 scene contract — `scenes/common.py` (read this, your script section, your BRIEF row, common.py)

Reference scene: `scenes/s01_hook.py` (check clean, contact sheet read: `build/sheets/s01_hook_Hook/`).
Every set piece is exercised by `build/common_test.py` (`Bench`); its sheets
`build/sheets/common_test_Bench/sheet_0{1,2,3}.png` show what each piece looks like. Run it
before you change how you call a piece:
`python -m explainer.check videos/ac215-l09-ci-testing/build/common_test.py Bench --tts silent`.
**Do not edit `common.py`** (shared; agents run in parallel): put requests in your report.

## Setup, checks, scene skeleton

```bash
cd /home/user/Explainer_Videos && source .venv/bin/activate
export PYTHONPATH=/home/user/Explainer_Videos EXPLAINER_TTS=kokoro EXPLAINER_VOICE=af_heart EXPLAINER_SPEED=0.9 PYTHONHASHSEED=0
python -m explainer.check   videos/ac215-l09-ci-testing/scenes/sNN_x.py Cls          # must print OK
python -m explainer.preview videos/ac215-l09-ci-testing/scenes/sNN_x.py Cls --every 3 # read every sheet
python -m explainer.preview ... --at 12.5,30 -q m                                      # exact frames
```
480p only, one render at a time, foreground with a long timeout. First run synthesizes the voice.

```python
import numpy as np  # noqa: I001  (manim first, then common: common must win)
from manim import *
from explainer.scene import VoiceScene
from explainer import style as S
from common import (...)            # name what you use (or `from common import *`)

SAY = NARRATION["S07"]              # SAY lines verbatim from script.md, in order
class TestsInImage(VoiceScene):
    def construct(self):
        assert len(SAY) == 6, len(SAY)
        with self.voiceover(SAY[0]) as vo:     # exactly one block per SAY line, in order
            ...; vo.wait_until("exact phrase from the SAY"); ...
        ...
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)   # end on an empty frame
        self.remove(*self.mobjects)
```
SAY counts: S02 5 · S03 7 · S04 6 · S05 8 · S06 6 · S07 6 · S08 8 · S09 8 · S10 5 · S11 6 · S12 7 ·
S13 6 · S14 5 · S15 4. A PONDER goes right after its SAY block:
`card = pause_and_ponder(self, "question\nlines", seconds=8)`; FadeOut it at the start of the next block.

## Binding rules (skill "Scene-code pitfalls"; each cost time before)

- No `print()` left anywhere (check reports `PRINT`; `t.print(...)` is fine). Deterministic: no
  unseeded randomness, no `always_redraw` on big groups, clear updaters.
- Text ≥ 20 pt, inside x ∈ [−6.6, 6.6], y ∈ [−3.6, 3.6]. Never `.scale()` anything holding text
  below 1.0 (SMALL): strip the texts first (S01 fades the envelope/vault words, removes them from
  their parents, then shrinks the bare gate), or build the piece at the size you need.
- ≤ 3 visual groups at once; something moves every ~4 s (except ponder timers); scenes end empty.
- Never assign `width/height/color/depth` on a VGroup subclass. `capture(...).pick()` is 0-based
  (pick index = file line − 1); prefer `.at()` with the script's FILE line numbers.
- Terminals: full width (`term`, 12.6 wide, 65 chars at 22 pt) or a 3-row strip at the bottom
  under a picture (`resize(self, t, 3)`); never half width; a full terminal and a picture never
  share the frame. Commands are never cut: `type_cmd` folds at a space with ` \`.
- `FadeOut(g)` takes the family off the scene and restores opacity: a faded child that stays in
  its parent snaps back when the parent is animated. Remove it from the parent (`unpin`, or
  `parent.remove(child)` as S01 does) or fade the parent.
- **NEW (hit here): never play `FadeIn(piece)` and `Indicate(piece.part)` (or any animation of a
  part) in the same `play()`.** FadeIn's begin() fades the part first, Indicate captures that faded
  state and "restores" it invisible for good (GateTable's first header vanished). Two plays.
- Prefer transforms that show what became what (S01: the code panel FadeTransforms into the
  commit envelope).

## Colours (BRIEF table; names in common.py)

`LAPTOP` GREY (clone, working tree, staging, host shell) · `CLOUD` BLUE · `IMAGE` TEAL (images,
containers, baked slabs) · `SYSTEM` = `HOST` ORANGE (host pip installs, host PATH) · `VENV` =
`HERMETIC` = `PASS` GREEN · `TOOL` PURPLE · `ERR` RED · `TURN` YELLOW (your turn, tracker, row being
filled) · `MODIFIED` = YELLOW (black's "files were modified"; the script's "amber") · `ROUTE` PINK ·
`FUTURE` / `SKIP` GREY (+ dashed) · `COST` GOLD (unused on screen) · `INK` white.
Test kinds by what runs: `UNIT` GREEN · `INTEG` TEAL · `SYSTEM_TEST` BLUE (`KIND[kind]`).
Arch/dot states `STATE`: idle GREY, pass GREEN, fail RED, modified YELLOW, skip GREY dashed.
A skipped/deselected test is never GREEN; the system row/dot never sits inside the hermetic border.

## Data, captures, sources

| export | purpose |
| --- | --- |
| `NARRATION["Snn"]`, `TITLES[cls]`, `SPEC` | SAY lines from script.md; titles; video.yaml |
| `capture(name, folder=None) -> Capture` | `capture("part4-07")` (laptop), `capture("s05a-08", BABYKEV_DIR)`, `capture("babykev/07")`; a prefix must match one file; `capture-only/` refused |
| `Capture.cmd .lines .exit .raw .path` | command as typed; output body (no `[exit N]`); every file line (tabs → 8 spaces) |
| `.at(2, (5, 7), "…", 33)` | lines by FILE number (line 1 = `$ cmd`, refused); `"…"` items add a `…` row |
| `.line(n)` · `.pick(...)` · `.istep(n)` | one file line · L1 picker (body index = file line − 1, adds `…`) · `(prompt, typed)` of an istep line |
| `split_prompt(s)` | `'app@44b7…:/app$ uvicorn …' → (prompt, typed)` |
| `hash12 cut ask squeeze cols` | sha256 → 12 hex + `…`; cut after a marker; cut a `[y/N]` question; re-align a docker table (drop empty columns); keep named columns |
| `readme(n)`, `walk(n)` | cheese README / babykev-walk walk.md line n, stripped (assert `cap.cmd == readme(106)`) |
| `source_text(path)`, `excerpt(path, a, b)` | assets/source files (`cheese-app-ci-cd/…`, `cheese-app-ci-cd-history/…`, `babykev/…`, `babykev-history/…`, `babykev-walk/…`) |
| `code(path, a, b=None, language=None, focus=None, font_size=22, shown=None, max_lines=12)` | CODE panel, header `shown_path(path) · lines a–b` (repo-relative; `c3b227f · service.py`; `step-05 · model.py`). `.code .header`; highlight with `code_span(p.code, k, "sub")`, `line_bar(p.code, k, colour)`, k = file line − a. Refuses > 12 lines: show long files as successive ≤12-line windows (S09's 7–44, S11's 5–24) |
| `readme_card(lines, body, quote=False, card_w=None, size=22, file="README.md")` | GREY README quote card `README.md · line n` |
| `P_LAPTOP_HOME P_LAPTOP P_BABYKEV_HOME P_BABYKEV T_LAPTOP T_BABYKEV` | `student@laptop:~$`, `…:~/cheese-app-ci-cd$`, `…:~/babykev$`; titles `laptop`, `laptop · babykev` |
| `REQUEST RESPONSE APP_CHAIN` | `GET /euclidean_distance/?x=3&y=4`, `{"distance": 5.0}`, routing/validation/handler/power() |

Captures whose command is the README line verbatim (laptop): part1-01/opt3-01 = 73/210 ·
part2-01/opt1-01/opt2-01 = 106/169/190 · part2-02 = 109 · part2-03 = 112 · part2-04 = 118 ·
part2-05 = 121 · part2-06 = 124 · opt1-02..05 = 172/175/178/181 · opt2-02 = 193 · opt2-05/07 = 196 ·
opt2-06 = 199 · part4-01 = 240 · 02 = 246 · 03/07 = 255 · 04 = 262 · 08 = 265. Cleanup
(571/573/574) and clone are inline/in prose in the README: type the capture's `.cmd`.

## Trackers and the lecture tag

- `tracker(key, step=None, extra=False)` (`"A".."F"`; aliases `tracker_a … tracker_f`) → placed
  top-left (left −6.5, top 3.5, bottom ≈ 2.9; up to 6.7 wide). `SECTIONS`, `STEPS` hold the
  BRIEF's titles/steps. E's head reads `guest lecture › babykev walk, steps 00–05b` (script S10).
- `track(tr, k=None, extra=False)` → Animation: move to step k and set/clear " · extra". Never
  `tr.goto()` (SMALL). Show " · extra" while a non-README command is on screen.
- `swap_tracker(scene, old, new, *anims)` plays one tracker turning into another in place.
- `lref("87–90")` → GREY `Lecture 9 · slides 87–90` tag top right (one per scene, BRIEF span).
- Free band for pictures: y from −3.5 (or `STRIP_TOP` −1.44 + 0.15 above a 3-row strip,
  `strip_top(rows)`) up to 2.8 under the tracker.

## Terminals and tags

| export | purpose |
| --- | --- |
| `term(prompt=P_LAPTOP, rows=10, title=T_LAPTOP, width=12.6, size=22, place=True)` | house terminal, bottom edge at `BOTTOM` −3.5; height = rows × 0.403 + 0.85 |
| `laptop_term(rows, prompt)`, `babykev_term(rows, prompt)` | the two laptops |
| `resize(scene, t, rows, keep=None, extra=())` | grow/shrink, bottom fixed (3 = the strip) |
| `type_cmd(scene, t, cmd)` | type at the prompt (replaces a bare prompt; folds long commands; returns the line or a group with `.rows`) |
| `bare_prompt(scene, t)`, `cd_prompt(scene, t, new_prompt)`, `istep(scene, t, line)` | prompt returns; prompt changes after `cd` (path flashes); a container line from an istep capture |
| `t.print(scene, lines, wrap=False)`, `t.find("sub")`, `substring(line, "sub")` | print output (`wrap=True` for pip/pre-commit warnings, SKIPPED lines, coverage Missing); find a row; its glyphs |
| `beside(mob, line)` + `pin(scene, line, mob, anim=None)` / `unpin(scene, line, mob)` | a tag right of a row that scrolls with it; `pin` refuses a tag covering text |
| `turn_row()` `extra_row()` `time_row()` `row_tag(parts, color)` | row-sized tags (0.36 tall): `▶ your turn` YELLOW, `extra`, `at the time of recording` |
| `your_turn() extra_tag() recorded_tag("recorded · walk.md") recording_tag() erratum_tag() illustration_tag() preview_tag() expected_tag()` | house-size tags (beside cards/panels, not inside rows) |
| `grey_chip(s, mono_font=False)` `dashed_chip(s)` `tool_chip(s)` `finding_chip("F401", "'os' imported but unused")` `file_card(path, color, dashed=False)` | notes; future/never-matched; PURPLE tools; RED lint finding; a file as a card |
| `note(s, color=GREY, size=20)` `steady(s, size, color, mono_font)` | caption line (**2nd positional arg is the colour**); text that morphs safely (counters, captions) |
| `under ring hl_bar strike outline_box arrow route travel bounce lock_glyph` | underline; outline box (fine over text); translucent bar; strike; dashed↔solid box; grey arrow; PINK route; ride a path; go-and-return; padlock |

## Set pieces (all text ≥ 20 pt; nothing is added to the scene for you unless a method says "plays")

**V1 · gate and vault** — `CommitGate(n=5, names=None, arch_w=.7, arch_h=1.5, gap=.22, with_tray=False)`
(S01, S09; S11/S14 variants). Floor at the group's y=0 line; 5 arches ≈ 9.1 wide, 9 + tray ≈ 12.9 ×
3.5 with labels (centre it at x=0). `.envelope .turnstile .arches .vault .tray .floor .home` (home follows the group).
`drop_in()` / `approach()` / `go_home()` / `open()` / `shut()` → Animations; `refuse(scene, i, "fail"|"modified")`
plays: passes 0..i−1 GREEN, arch i flashes, envelope back to the tray; `pass_through(scene, states)`
plays: arches take states (`"pass"`, `"skip"` = GREY dashed `(no files to check)`), door opens,
envelope goes in and is **removed from the group** (`gate.envelope is None`; `new_envelope()` makes
one to FadeIn). Arch names: `gate.turnstile.labels` (built, not added; alternate below/above).
`Turnstile(n, names, arch_w, arch_h, gap)`: `.arches .labels .mark(i, state) .mark_all(states)`;
`Arch.to(state)`. `envelope() vault() tray()` glyphs. `CHEESE_HOOKS` (9 short names, config order),
`BABYKEV_HOOKS` (4), `SHARED_HOOKS`.

**V1 · gate table** — `GateTable(keys=(), filled=(), rows=None)`: build it with the rows THIS scene
ends with; `filled` show at once, the rest are empty slots. `fill(scene, key)` plays the row in
YELLOW; `settle(scene, key)` plays its final colours (verdict GREEN; outside rows all GREY in a
dashed outline below the frame). `header_pulse(i)` → Animation (not with the table's FadeIn!).
`GateTable()` = S03's empty table. Rows (`GATE_ROWS`, order `GATE_ORDER`): tests (S07, script
text) · system (S08, outside) · format · docs · config · types. Columns size to the longest
text: 11.8 wide with tests only, 12.8 with tests + system, 13.1 with all six: centre at x=0, never
scale it. Height: 1.55 (one row), 2.3 (tests + system), 4.35 (all six); the empty table 7.0 × 2.1.

**V2 · one request** — `RequestToken()` (PINK pill, `.text`); `kind_box(kind, title, box_w, box_h)`;
`app_chain(names)` (chips + arrows); `TestPyramid()` (`.layers["unit"|"integration"|"system"]`,
`.extra_rows()` smoke/acceptance, 7.2 × 2.7); `HermeticBorder(w, h)` / `HermeticBorder.around(mob)`;
`NestedKinds()` (unit ⊂ integration ⊂ hermetic border ⊂ system box reaching past the border to
`server :9000` over a PINK wire; 9.5 × 3.8; `.unit .integration .border .system .wire .server`);
`TestDots(n, colours, cols)` + `.to(indices, "pass"|"skip"|"fail"|"idle")`; skip = GREY dashed
ring with an `s`.

**V3 · collector and fixtures** — `Collector()` (three columns from the real def lines: 11 + 10 +
6 tiles, `is_api_running` stays dark; 10.9 × 3.4): `sweep(scene, run_time, again=False)` plays the
scanner, tiles light GREEN, counter `collected 26`; `extra("broken", "unit")` → a dark chip (not
added). `COLLECT` holds the names. `FixtureWiring()` (conftest.py box with `client`, three test
cards, "asks for" arrows; `.ask_label` not added): `session()` / `per_test()` → (mobjects,
animations). `Parametrize()` (`.cards`, `.fold()` → animations; cases from test_utils.py:15–18).

**V4 · ribbon and funnel** — `Ribbon()` (service.py:15 as 95 cells, left edge fixed at x=−5.8:
move it only vertically): `post(w)` → a width post (not added), `fold()` / `unfold()` /
`move_post(post, w)` → Animations. `FindingsFunnel(counts, notes)` + `.step()`. Babykev counts
70 → 69 → 37 (s02-12/14/15); 79 is `recorded · walk.md`. Cheese: digest:190 measured 8 findings
in 8eb63fc's service.py at width 120 → 2 after black — not a terminal capture; the script only
names the 2 survivors (use `finding_chip`).

**V5 · hand-over chain** — `HandoverChain("cheese"|"babykev")`: column git commit ↓
.git/hooks/pre-commit ↓ pre-commit ↓ .pre-commit-config.yaml → turnstile (9 or 4 arches; labels
built not added). 12.7 × 4.2 (cheese), 10.7 × 4.2 (babykev). `.links` (chips and arrows interleaved, for a
LaggedStart), `.drop`, `.turnstile`, `.hook_note()` (GREY "machine-specific · never committed").

**V6 · mask grid** — `MaskGrid(seg=SEG_SIX, rule="want"|"ones"|"wrong_fix"|"siblings", cell=.5)`
(6×6 ≈ 3.2 × 3.7; 4×4 at cell .7 ≈ 3.0 × 3.5). `MaskGrid.from_rows(cap.at((2, 7)), SEG_SIX)` (s05-04),
`field=1` for the built column of the checker captures. `.cells[i][j]` (0-based) · `flash_rows(rows)` ·
`retarget(rule)` · `diff("want")` → wrong cells · `cell_box(i, j)` / `row_box(i)` · `overlap(sib)` →
allowed ∩ siblings (`[(3, 1)]` for SEG_FOUR wrong fix) · `light(cells)` · `wrong_fix_marks()` →
(RED boxes on correctly blocked adjacent cells, YELLOW boxes on wrongly open two-back cells; needs
SEG_FOUR). Helpers: `segment_ids(state, qs)`, `mask_rows(seg, rule)` (equals the walk's prints:
tested for s05-04, slide 79/81 rows), `shape_text(1, [1,1,1])` → `shape = (1, [1, 1, 1])`,
`shape_caption(1, [1,1,1])` → `state 1 · questions 1, 1, 1`, `SEG_SIX`, `SEG_FOUR`,
`SHRINK_PATH` (illustrative shapes ending at hypothesis's real answer: tag it `illustration` if
you show the intermediate steps), `sequence_bar(seg)` (packed request), `Dice(v).roll(v)`,
`coverage_sweep(panel)` → (bars, animation).

**V7 · baked-in code** — `LayerStack(stack_w=4.6)` + `Slab`; `CHEESE_LAYERS` = Dockerfile:32–41
(thin pyproject.toml GREY, fat pip install ORANGE, four thin COPY GREY; TEAL outlines).
`make(text, fill, h)` → placed slab; `drop(scene, *slabs)` plays it in; `brace(slabs, text)`;
`rebuild(scene, slabs)` plays only those slabs being replaced ("packages before code").

## Traps found while building common.py and S01

- Emoji lines render with missing glyphs and shift `substring()` indices: never print
  part2-03:41, part2-06:39 (`Oh no! 💥 💔 💥`), part4-04:15, part4-11:15 (`All done! ✨ 🍰 ✨`).
- `Capture.line()` refuses `[exit N]` lines and `clean-03:5` (the capture-only base-image row).
  Tabs are expanded (diff headers in part2-03, `git status` rows in part4-12, s05a-03:31).
- `code()` width: 22 pt fits ≤ ~66 characters per line (S01's 38–48 reaches x ±6.52); 20 pt
  ≤ ~72. c3b227f-service.py:49 is 78 characters, so S01 shows 38–48, not 38–50.
- The `words count mismatch` warnings from manim's Text (t2c captions) are harmless; check still OK.
- Anchors: `vo.wait_until()` needs the SAY's exact words (punctuation too, e.g. `"a gate,"`);
  timing is interpolated by characters inside a sentence. A miss prints
  `voiceover anchor not found` — fix it, never ignore it.
- `from common import *` brings lowercase helpers (`code`, `note`, `ring`, `arrow`, `tray`, `vault`,
  `envelope`, `cut`, `cols`, `ask`): don't shadow them with local variable names.
- A set piece moved after construction keeps working (`CommitGate.home`, `GateTable` slots are
  carried by invisible markers); scaling a piece with text does not (SMALL).
- Script gap for the coordinator: the BRIEF puts the format+lint gate-table row in S09, but S09's
  script never shows it; S14 expects six rows. Until decided, S14 builds the table with all six
  `GATE_ORDER` keys filled.
- Agents never kill processes they did not start; scratch files only under `build/`; delete only
  files you created, by exact path.

## Traps added during scene builds (coordinator)
- `TestPyramid.extra_rows().set_opacity(x)` fills the dashed boxes solid. To fade those rows, fade
  their stroke and text instead (S03). In general prefer `fade()` over `set_opacity` on groups that
  carry glows or chip fills: `set_opacity` makes fills stronger, not fainter.
- Scaling a group that contains text below 1.0 trips the SMALL check; build it at the larger size
  and Transform into the normal-size version instead (S03's gate table).
- VoiceScene has no moving camera: "zoom" beats are done by swelling/fading the content (S03).
- The curl captures laptop/part1-02/03/04 have no newline before `[exit 0]`, so `[exit 0]` is glued
  to the JSON line. Only S04 prints them and strips it locally (with an assert); `capture()` is
  left unchanged on purpose. Any other scene quoting these files must strip it the same way.
- 20 pt terminals (72 chars/row) are fine where 22 pt (65 chars) would cut needed names (S04's
  `ls -la`); `strip_top()` assumes 22 pt, so size 20 pt strips by hand.
- `Indicate(hermetic_border.text)` recolours the text's BG mask too, hiding the word: indicate
  `.text[1]` (the word only). Same caution for any masked label (S03 critic).
- Morphing a labelled box into a small chip with FadeTransform stretches its text across the frame
  for ~1 s: fade the words first, transform the bare shapes, then fade the new label in (S03 critic's
  `park()` pattern).
- A `Succession` of two `.animate` builders on the SAME mobject silently does nothing (S02's arrow
  never moved). Use separate `self.play` calls for there-and-back moves.
- `TransformFromCopy` between differently shaped text smears into a blob mid-morph: fly a copy of
  the text, then draw the box around it (S02 critic).
- Removing a printed row from `t.lines` right before animating it makes it vanish for a few frames:
  animate a `.copy()` out of the terminal and fade the terminal instead (S04 critic).
- `FixtureWiring.per_test()` fades its copies in one at a time and adds each to the scene: removing
  only the returned group leaves them behind. Remove/fade each copy (S06).
- `pin()`/`attach()` re-add rows to the scene, which splits the parent terminal in the scene list. A
  later bare `FadeOut(t)` then redraws `t` on top of overlays (rings, `hl_bar`) and they flicker
  out for a few frames. Fade terminal and overlays together: `FadeOut(VGroup(t, bar, ring))` (S05
  critic).
- Ponder cards point with YELLOW (look here), never RED: a RED flash on the candidate answer hints
  the wrong answer and breaks the RED-only-for-failure rule (S06 critic).
- `FixtureWiring.session()` builds its recolour animations at call time: dimming the arrows first
  leaves them faint after it plays. Re-light them in your own play (S06 critic).
- `Parametrize.fold()` cross-fades text over text; S06 places the merged card ABOVE the cards and
  flies each card's own glyphs into its chip — copy that pattern instead (S06 critic).
