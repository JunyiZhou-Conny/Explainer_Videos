# Review record: E1 · Four verbs and a contract

Produced 2026-10-14 by a Claude Code cloud session (PR #17, branch
`claude/clever-wozniak-3ocis0`) for Conny, who asked to learn enough Python design to keep
building speciesOT with Josh. Verified facts and unclaimed reviews are kept separate.

## Content gates (AGENTS.md)

1. **Hook**: s01 opens on Josh's real notebook cell, a whole experiment in four calls, and
   asks the viewer's own question: which of the 346 lines matter, and where do you start
   reading? ✔
2. **Intuition before formalism, with an animated mechanism per idea**:
   - class → object: the object card fills row by row as `__init__` runs (lines 214–225).
     Each highlight is anchored to its spoken word ("learning rate", "latent size", "where to
     save"). A `self` pointer and a second EXAMPLE object follow.
   - abstract = contract: red blanks on the contract card, then the measured `TypeError`
     pulses the blanks it names. IdentityModel's method bodies then drop into the blanks.
     The two `train` signatures (lines 43 and 155) are compared, and the measured
     "IdentityModel() built" shows the contract checks names, not inputs.
   - Experiment conducts: config sections become the two lists; a token cues each model;
     predictions collect; the 2 × 2 grid empties at line 145.
   - polymorphism: one call on line 137 runs down two lanes (`model = models[0]`,
     `models[1]`). ✔
3. **Ponder moments and recap**:
   - Two ponders in 4:35, each under a paper veil and followed by measured silence: s03 ≈
     1:37 ("what happens if you call AbstractModel() directly?", 3.3 s) and s05 ≈ 3:44
     ("adding CellOT: which lines of Experiment should change?", 2.7 s).
   - s06 recaps the three ideas and gives the five-jobs table, which doubles as the answer
     key to the pause-and-label exercise (`exercises.md`). ✔
4. **Written for the ear; anchored cues**:
   - Paths and identifiers are spoken as words ("species O T core dot py", "self dot L R"); the
     speciesOT lexicon entries were added to `explainer/lexicon.yaml`.
   - Every reveal is tied to a `wait_until` phrase, and `check_anchors.py` confirms each one
     against the narration. ✔
5. **Simulated-viewer QA over the full draft**: a separate pass played the target viewer
   (no Python design background, Josh's file open). Findings and fixes are below. ✔
6. **Measured checks**: see Verified. **Conny's listening sign-off: pending.** ✘ (not yet)

## Whole-video QA (first full cut, 2026-10-14)

A simulated-Conny pass sampled a frame every 2 s plus every scene change, against the
captions, `script.json`, the excerpts and Josh's attached file (sha256 `b66554…`). All code
and line numbers on screen matched the source. Problems found, and what changed:

**Wrong**

- [0:26] The hint said "every *line* does one of five jobs"; only classes do. FIX: "every
  class".
- [0:32] "The word you'll see most: class" is false (`self` 114×, `def` 29×, `class` 16×).
  FIX: "the word the whole file is built from".
- [1:50] The scGenModel card showed planned behaviour as if it were code. FIX: the bodies
  are grey with a PLANNED · E4 tag.
- [2:09] Josh's line-19 note was attributed to Experiment. FIX: "…says the data classes can
  drop it, and the same goes for Experiment."
- [2:57] "returns None" sat beside line 145, which returns a float. FIX: the label reads
  `experiment.evaluate() → None` with "line 145 never stores its numbers" (MEASURED).
- [4:20] DummyEvaluation was missing from the recap table, which is the answer key. FIX:
  added.

**Confusing**

- The title said "four lines" over a 5-line cell. FIX: retitled "Four calls, one experiment".
- The init highlight ran at a fixed pace, ahead of the words. FIX: anchored highlights.
- `self` was never linked to the object. FIX: pointer and label on "this particular object".
- The second object had no source. FIX: tagged EXAMPLE and captioned.
- Both ponders had about 0.2 s of thinking time. FIX: `hold()` gives each roughly 3 s, taken
  from the static scene tails (formerly 6–8 s).
- The blanks vanished as Python refused because of them. FIX: they stay and pulse.
- "Fill in the blanks" was not animated. FIX: the method bodies move into the slots.
- "Checks names, not inputs" was asserted only in the recap. FIX: s03 shows it, with a new
  narration line.
- Line 67 was not shown. FIX: added to the note panel.
- The two-model run implied that both models work today. FIX: "today only IdentityModel
  runs end to end → E2, E5" and a placeholder tag.
- The prediction clouds sat under the metric chips. FIX: they sit beside their models.
- `model` as the loop variable was never drawn. FIX: `model = models[0]` and `models[1]`
  labels.
- The "ideally none" payoff was not shown. FIX: "lines 131–145, train · predict · evaluate,
  stay unchanged".
- The exercise asked the viewer to label classes while the table was on screen. FIX: the
  narration now presents the table as the answer key.
- Three Chinese phrasings were literal or ambiguous. FIX: reworded (s05 L4, s06 L1, the
  `self` line).

**Layout**: a label touching a dashed border, slots overlapping text, the TypeError card
covering a row, an "inheritance" label jammed between arrowheads, chip overlap and a table
scaled too small, a tag overlapping the polymorphism line, cloud dots on labels. All were
moved or resized.

**Second pass (rebuilt cut, contact sheets of every scene):**

- A pointer crossed code (now leaves from the end of line 218).
- An EXAMPLE tag touched the caption band (now beside its caption).
- Method bodies spilled over the method names (only the bodies drop in now).
- Side notes touched code panels.
- The recap's "conductor · 指挥" overlapped "Experiment".
- The PLANNED tag overlapped the shifted cloud.

All were fixed and re-checked in scene renders.

## Verified (final render)

- **Encode**: 275.000 s, 1920×1080 @ 30 fps, H.264 + AAC; six scenes. Narration minimums sum
  to 258.5 s; nothing was clipped to fit.
- **Captions**: 70 bilingual cues, ordered, non-overlapping and inside the runtime. The
  widest lines, measured in the burn fonts, are 1462 px (zh, Noto Sans CJK 43) and 1436 px
  (en, Inter 30), within the 1740 px caption area.
- **Mix**: voice −15.98 LUFS; music −21.99 LUFS in gaps and −32.1 under speech; mix −16.2
  LUFS; true peak −1.0 dBTP. The Swiss style check passed on sampled frames.
- **Render log**: no BUDGET, CODEPANEL or missing-anchor warnings in any scene.
- **Static picture with silence**: at most about 4 s, across scene cuts (measured with
  `silencedetect` against the clean track); the two ponders hold 3.3 s and 2.7 s.
- **ASR round trip** (faster-whisper small.en on the clean narration vs `script.json`;
  643 script words, 655 heard, similarity 0.963): all 15 differences are tokenization,
  e.g. "abstractmodel" → "abstract model", "init" → "in it" for the spoken `__init__`,
  "three hundred and fifty" → "350". No missing or garbled sentence.
- **Evidence**: every code excerpt is generated from Josh's attached `src/` by
  `../speciesot-series/make_excerpts.py`, with source hashes recorded. The `TypeError` text,
  the `IdentityModel()` build and `experiment.evaluate()` returning None are measured in
  `../speciesot-series/checks/`.

## Not claimed

- **No human listening review yet.** Conny's sign-off on pronunciation, pacing and music
  belongs here before merge.
- The Chinese translation was self-reviewed by the producing session only.
- Josh has not reviewed the description of his code.
- Nothing was run on the cluster; measured facts come from toy data in this session.
- The English caption line (Inter 30 px) was flagged as small on a laptop. Changing it is a
  toolkit default, outside this episode.
