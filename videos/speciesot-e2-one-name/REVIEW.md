# Review record: E2 · One name, five places

Produced 2026-10-14/15 by a Claude Code cloud session (PR #17, branch
`claude/clever-wozniak-3ocis0`) for Conny. Verified facts and unclaimed reviews are kept
separate.

## Content gates (AGENTS.md)

1. **Hook**: s01 opens on a broken thing. Setup crashes with an AttributeError; deleting one
   letter makes the crash disappear, but the network would be built for 1000 genes, not 4
   (MEASURED · toy data, stand-in scgen). ✔
2. **Intuition before formalism, with an animated mechanism per idea**:
   - Five places: one value (`z_dimension: 50`) travels as a token from the YAML line, to a
     dictionary drawer, to `__init__` (line 221), to the object, to the setup that reads it
     (line 254). Copies of the token move, so the 50 stays in its drawer.
   - Two lookups, two errors: a missing drawer raises KeyError; a probe on an object card
     finds no attribute and raises AttributeError. Both are defined before the ponder.
   - Reading a traceback: tint bands mark WHAT (the last line) and WHERE (the frame above it),
     and the two frames are labelled `Experiment.setup · 119` and `scGenModel.setup · 253`.
   - The silent twin: line 104's write adds a new `x_dimensions` drawer that nobody reads.
     ✔
3. **Ponder moments and recap**:
   - Two ponders: s04 ≈ 2:38, KeyError or AttributeError (4.3 s of silence); s05 ≈ 4:31, should
     the gene count be typed or read from data (9.1 s, the scene's last beat).
   - Both lines carry `pause_after: 4.0`, so their own scene pays for the thinking time.
   - s07 recaps the five places and the two errors, and ends on the exercise: keep the
     singular, the three edits, and what a good rerun prints. ✔
4. **Written for the ear; anchored cues**: identifiers are spoken as words through the
   lexicon. Every reveal is tied to a `wait_until` phrase, and `check_anchors.py` checks both
   presence and spoken order. ✔
5. **Simulated-viewer QA over the full draft**: findings and fixes are below. ✔
6. **Measured checks**: see Verified. **Conny's listening sign-off: pending.** ✘ (not yet)

## Whole-video QA (first full cut, 5:55, 2026-10-14)

A simulated-Conny pass sampled a frame every 2 s plus 60 full-size frames. Code, line
numbers, error texts and the measured dict all matched their sources. Problems and fixes:

**Wrong / blocking**

- [3:06] WHERE was drawn half a second before the scene cut, as an invisible recolour. FIX:
  tint bands; WHERE fires on "Just above it"; the full traceback holds to the end of the line.
- [5:31] "Pick one spelling" gave no guidance, and `x_dimension=` on line 253 is scgen's own
  parameter, not ours. FIX:
  - The narration says to keep the singular.
  - s03 labels "scgen's parameter name" against "ours".
  - The exercise lists the three edits and marks `x_dimension=` "leave it".
- [5:43] After the fix, the cluster rerun may still stop at line 252. FIX: the exercise says
  what success looks like (`experiment.models[1].x_dimension` is the real gene count) and that
  line 252 is E4's topic.

**Confusing**

- Two methods were both just "setup". FIX: `Experiment.setup` and `scGenModel.setup` are
  named in the narration and the frames; line 115 is shown at hop 3.
- Why the twin is silent was never said. FIX: one sentence (writing a missing key adds a
  drawer), with the drawer appearing on the write.
- The token left its drawer empty. FIX: copies travel.
- "Four places" against a five-place exercise. FIX: five places throughout (title, hook,
  station ⑤, recap).
- The toy config lacks more than `experiment:`. FIX: "also missing z_dimension, alpha,
  dropout_rate".
- The ponder asked about AttributeError before defining it. FIX: both errors are defined in
  s04 L0. The ponder card also covered row 19; it now sits clear of it.
- YAML `None` had no stated consequence. FIX: "harmless today; any `is None` check breaks".

**Polish**:
- Provenance tags on s02 and on the 18,024 (Josh's real data).
- "would be built for", with the stand-in tag kept.
- `speciesot_core.py` in the loop subtitle.
- "scvi-tools scgen (2.1.0 on PyPI)".
- Rule 1 adds the writer (104) and reader (253).
- Several small nudges.

**Chinese**: calques rewritten (少了属性, 不报错的 bug, 已经和代码对不上了, 看起来改一个字母就能修好,
模拟的 scgen（stub）), the traceback cues re-split, and the dash split removed.

**Second pass (rebuilt cut)**: contact sheets of every scene confirm each fix on screen.
Bugbot's stale-anchor findings on the intermediate commit are resolved: `check_anchors.py`
passes, and it now also checks spoken order.

## Verified (final render)

- **Encode**: 399.033 s, 1920×1080 @ 30 fps, H.264 + AAC; seven scenes. The narration
  minimum is 375.0 s, including two 4 s ponder pauses; nothing was clipped.
- **Captions**: 95 bilingual cues, ordered, non-overlapping and inside the runtime. The
  widest lines are 1384 px (zh) and 1307 px (en), within the 1740 px caption area.
- **Mix**: voice −16.06 LUFS; music −22.06 LUFS in gaps and −31.56 under speech; mix −16.32
  LUFS; true peak −1.0 dBTP. The Swiss style check passed.
- **Render log**: no BUDGET, CODEPANEL, missing-anchor or traceback lines in any scene.
- **Silences**: 3.4–6.5 s at scene cuts, 4.3 s at the s04 ponder, and 9.1 s at the s05
  ponder, which is the scene's last beat.
- **ASR round trip** (faster-whisper small.en on the clean narration vs `script.json`; 946
  script words, 954 heard, similarity 0.947): almost all differences are tokenization
  ("set up", "scgen model", "in it" for `init`, digits for spoken numbers). Two places to
  listen for: at 2:04, "Ours is the one after self dot" was heard as "hours…" with "dot"
  dropped, and "experiment's" was heard as "experiment" three times. Neither changes the
  meaning against the on-screen labels; Conny's listen decides.
- **Evidence**: error texts, frames 119/253 and the dict `{x_dimension: 1000, x_dimensions:
  4}` are measured in `../speciesot-series/checks/error_trail.json`. 18,024 is read from
  `Tests/e24_replica.ipynb` cell 3.

## Not claimed

- **No human listening review yet.** Conny's sign-off belongs here before merge.
- The Chinese translation was self-reviewed only.
- Josh has not reviewed the description of his code.
- Nothing was run on the cluster: the cluster's line-252 stop is INFERRED from the scgen 2.1.0
  wheel, and Josh's environment was not inspected.
