# Building a speciesOT episode's scenes

For whoever writes `videos/speciesot-eN-*/scenes.py`. The reference implementation is
`videos/speciesot-e1-blueprint/scenes.py`; copy its patterns, not its diagrams.

## Inputs (read these first)

- `script.json` of the episode: narration per scene (`lines[i].en` is spoken and captioned).
  Never put narration text in scene code; use `self.say(i)`.
- `storyboard.md` of the episode: what each scene must show, anchored to phrases.
- `production_notes` in `script.json`: which claims are MEASURED / READ IN CODE / INFERRED.
- `excerpts.py` (this folder): Josh's code with real line numbers (`CORE`, `CONFIG`,
  `TOY_CONFIG`, `TEST_EVALUATION`, `TEST_MODEL`, `E24_CELLS`, `E24_OUTPUTS`; `rows(src, a, b)`).
- `checks/`: the measured facts (`error_trail.json`, `pytest_run.txt`, `scgen_package.txt`).

## Kit (`speciesot_kit.py`)

| Helper | Use |
|---|---|
| `EpisodeScene` (subclass as `Ep` with `episode="E2"`, `total="07"`) | `self.header()` · `with self.say(i) as vo:` · `self.cue(vo, frac, *anims)` · `vo.wait_until("phrase")` · `self.dim_rest()` · `self.content()` · `self.finish()` (always last) |
| `code_panel(rows, title, x, y, width, size)` | real lines + numbers; one font size per panel (shrinks to fit; a `CODEPANEL WARNING` in the log means widen it or show fewer lines). `panel.row(n)`, `panel.mark(n, …)`, `highlight(scene, panel, n, …)` |
| `obj_card(title, rows, x, y, width, size, row_gap)` | an object with attribute rows; `card.rows[i]` |
| `class_card(name, methods, x, y, width, abstract, parent)` | a class (dashed when abstract) |
| `error_card(etype, message_or_lines, where, x, y, width, tag)` | a traceback's last line; z-index above code |
| `source_tag(kind)` / `tag_at(kind, x, y)` | READ IN CODE · READ IN NOTEBOOK · READ IN PACKAGE · MEASURED · INFERRED · EXAMPLE |
| `ponder(zh, en, y)` | pause-and-ponder card; pair it with `self.dim_rest()` |
| `chip`, `drawer`, `terminal`, `cloud`, `bracket`, `strike`, `mono`, `mono_left` | small parts |
| Swiss: `PAPER INK RED GRAY FAINT`, `label at left line card folder arrow` | palette and text |

## Layout contract (the style check and the reviewers hold you to it)

- Teaching area: x in [-6.3, 6.3], y in [-2.45, 2.05]. The header sits above; the caption band
  (bottom 170 px, y < -2.74) stays empty. Leave the frame mostly paper (style check: background
  dominance).
- One red accent: it follows the current point. Code ≥ font size 16 after shrinking; labels ≥ 17.
- Long code lines may be elided with `…` (never rewritten). Show the file path on every panel.
- Illustrative code we wrote ourselves carries the `EXAMPLE` tag. Cartoons say so on screen.
- Every scene needs an explanatory change (a mechanism moving), not only text appearing.

## Timing

- Anchors are substring matches on the English line; inside a sentence they are interpolated by
  character count, so anchor at clause starts. A missing anchor fails the full build.
- In a sample render the scene budget is narration + ~1 s: if the log prints
  `BUDGET WARNING`, your animations overrun the narration; shorten run_times or waits.
- Ponder time: give the ponder line `"pause_after": 4.0` in script.json and call
  `self.hold(i)` after its `say(i)` block. The engine adds the pause to that scene's minimum,
  so the thinking time is paid by the scene (samples included), not spread as episode slack.
- `LaggedStart` over an object's parts leaves Manim's helper `Group` holding those parts.
  `content()` handles a later fade, but a `ReplacementTransform`/`Restore` of the whole object
  can leave the parts behind: re-add the whole object (`self.remove(group); self.add(whole)`)
  right after the lagged play, as E3's `settle()` does. Never `self.remove(ls.group)` alone —
  that takes the parts off screen.

## Render and inspect (from the repository root)

```bash
python3 skill-library/conny-explainer-video/scripts/render.py videos/<slug> --sample s03
grep -E "BUDGET|CODEPANEL|anchor not found|Traceback|rror:" outputs/<slug>/build/s03/render.log
# (plain "Error" also matches on-screen Text('…Error') in the progress bar)
# frames: ffmpeg -ss <t> -i outputs/<slug>/sample-s03.mp4 -frames:v 1 frame.png
```

Read the frames at full size: overlaps, clipping, text below y = -2.45, code too small, a
highlight on the wrong line, an anchor firing early or late against the caption.

**Cache caveat.** The engine reuses a scene when `scenes.py`, the scene's plan entry, the voice
and the shared toolkit are unchanged. It does **not** see `speciesot_kit.py` or `excerpts.py`.
After changing either, delete `outputs/<slug>/build/*/render-input.json` for every episode
before the next full build, or a stale scene will be stitched in.
