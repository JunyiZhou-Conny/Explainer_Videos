# Review record: E4 · scGen as arithmetic, behind one adapter

Produced 2026-10-14/15 by a Claude Code cloud session (PR #17, branch
`claude/clever-wozniak-3ocis0`) for Conny. Verified facts and unclaimed reviews are kept
separate.

## Content gates (AGENTS.md)

1. **Hook**: s01 asks whether a human cell can be predicted from a mouse cell with one
   subtraction and one addition. A mouse gene bar becomes a predicted human bar by
   arithmetic. ✔
2. **Intuition before formalism, with an animated mechanism per idea**:
   - The autoencoder squeezes a gene bar into a 50-number code and rebuilds it. Mouse and human
     share one code space (a 2-D sketch, labelled "really 50-D").
   - The arithmetic: mean crosses, the δ arrow, then encode → +δ → decode. A second cell type
     whose own arrow differs shows the assumption, with "a map: each type gets its own arrow".
   - Three methods, three jobs: setup / train / predict lanes. The predict lane ends in an
     AnnData scored by `evaluate` against the human test cells. Josh's stubs, with the
     measured `NameError` at line 288.
   - Three things called scgen: the project frame, with each one's evidence. Josh's class is
     ticked to all three (helpers ①, import ②, settings ③).
   - One adapter: the package as a circle with one door. The four cellot calls, and a
     `FakeAutoEncoder` in tests. ✔
3. **Ponder moments and recap**:
   - s03 ≈ 1:17 asks "what must be true for one arrow to work for every type?" (`pause_after`
     4 s).
   - s06's closing ponder asks how many files change on a switch; its thinking time is the
     scene tail.
   - s07 recaps the arrow, the three methods, the three scgens and the one doorway, then sets
     the exercise. ✔
4. **Written for the ear; anchored cues**:
   - Identifiers are spoken through the lexicon.
   - Every reveal is tied to a `wait_until` phrase, and `check_anchors.py` checks both
     presence and spoken order. ✔
5. **Simulated-viewer QA over the full draft**: findings and fixes are below. ✔
6. **Measured checks**: see Verified. **Conny's listening sign-off: pending.** ✘ (not yet)

## Whole-video QA (first full cut, 5:04, 2026-10-14)

A simulated-Conny pass checked every path, line and number against the speciesOT repo at
`109bf12`, Josh's attached `src/`, and `checks/`. It found **four wrong facts**; all were
confirmed in the code before fixing:

**Wrong**

- "Predict ends by handing back the mouse cells untouched": predict never reaches its last
  line. Line 288 raises `NameError: name '_dense' is not defined` (MEASURED, `scgen_predict`).
  FIX: the narration says so; 288–289 carry a MEASURED chip; 292 is marked "never reached".
- "So those numbers would go nowhere": `z_dimension` (254) and `lr` (257) do reach VAEArith,
  and only the layer sizes are unused. FIX: "the layer sizes would go nowhere". Only the
  hidden_units row has the "nowhere" path, and the TF 2 × 800 chip is greyed, not struck.
- The helpers range: Josh's lines match `02_eval_metrics.py` 152–168, not 151–171. FIX: the
  screen, SOURCES.md and the production note say 152–168, with 169–171 (the predict step)
  "not copied".
- Provenance: the `speciesot_core.py` lines on screen came from Josh's attached 346-line copy
  but sat inside the "repo @109bf12" frame. The repo holds an older 128-line file at that
  path. FIX: every such panel reads "Josh's src (attached 10-14)" and sits outside the repo
  frame. SERIES.md explains the two files.

**Confusing**

- Conny's question ("do I need the original scgen code?") was never answered in one sentence.
  FIX: "So, to your question: no, you don't need the original scgen code", with an answer
  card.
- The "handful of calls" was misleading:
  - `train_auto_encoder` already computes the shift (train.py 250–252) and takes a cellot
    config plus an `.h5ad` path.
  - `model.eval()` is required before encoding.
  - `transport_scgen` (transport.py 61–69) is the whole predict step.
  - Conny's repo already makes all of these calls in `scripts/predict_new_input.sh` 623–663.

  FIX: the box lists exactly those four calls and points to the script with "start here". The
  exercise and exercises.md use the same four.
- Why "exactly one" was not said. FIX: "Josh's class mixes all three", ticked on screen. His
  commented scgen 2.x attempt (232–244) is shown.
- The predict lane stopped before evaluate. FIX: "AnnData with the human test genes, in the
  same order, so evaluate can score it".
- The test fake mimicked the wrong scgen. FIX: the measured stand-in is labelled as such, and a
  `FakeAutoEncoder` (EXAMPLE) is added.
- "1 file changes" understated a switch. FIX: "one code file + its config section + the
  dependency it needs" (INFERRED).
- The ponder had 2.4 s of silence, and s05 ended on 6.3 s of static. FIX: `pause_after` on
  the s03 ponder. The length is fitted with 4.5% slack (s05 runs 87 s).

**Layout / polish**:
- The Indicate flash no longer fills the adapter chip.
- Tie lines no longer cross.
- The helpers path sits under its label.
- The decode arrow starts from the shifted cloud.
- The type-B map arrow is labelled.
- The red highlight follows the door wire.
- The exercise panel shows step 1 only.
- The tags are completed: "scgen 2.1.0 (latest)", and "your edits" is cited (ae.py 180;
  train.py 174, 220).

**Chinese**:
- Calques rewritten: scGen 赌的就是这一点, 存成对象属性 self.delta, 占位代码（stub）, 根本用不上,
  只通过你定义的接口打交道, 测试时根本不用安装它.
- Misaligned cue pairs re-split.

**Bot review**: Bugbot caught two issues on intermediate commits, and both are fixed:
- an anchor order reversed by the narration rewrite (and `check_anchors.py` now checks order);
- a "real human B" label sitting nearer the predicted cluster than its own cloud (moved under
  it, and verified in a re-render).

## Verified (final render)

- **Encode**: 341.000 s, 1920×1080 @ 30 fps, H.264 + AAC; seven scenes. The narration minimum
  is 326.6 s; nothing was clipped.
- **Captions**: 86 bilingual cues, ordered, non-overlapping and inside the runtime. The widest
  lines are 1421 px (zh) and 1247 px (en), within the 1740 px caption area.
- **Mix**: voice −16.0 LUFS; music −22.0 LUFS in gaps and −32.11 under speech; mix −16.18
  LUFS; true peak −1.21 dBTP. The Swiss style check passed.
- **Render log**: no BUDGET, CODEPANEL, missing-anchor or traceback lines in any scene.
- **Silences**: at most 5.4 s, at the s05→s06 cut. The s03 ponder holds 4.3 s (1:17), and so
  does the s06 ponder (4:57).
- **ASR round trip** (faster-whisper small.en on the clean narration vs `script.json`; 841
  script words, 841 heard, similarity 0.962): differences are tokenization ("set up",
  "cell ot", "vae arith", digits). Two places to listen for: "AnnData" at 1:54 was heard as
  "and data", and "git-ignored" at 2:38 as "get-ignored". Both have the word on screen.
- **Evidence**:
  - The scgen 2.1.0 wheel contents are in `checks/scgen_package.txt`.
  - The predict `NameError` is in `checks/error_trail.json` (`scgen_predict`).
  - Every repo path and line number on screen was checked at `109bf12`: `.gitignore` 44–47,
    `m2_v08.yaml` 27/44/46–48, `02_eval_metrics.py` 152–168, `ae.py` 22/33/175,
    `train.py` 173/250–252, `transport.py` 61–69, `predict_new_input.sh` 623–663, and
    `specs/m1_modern.yaml` 33–37.

## Not claimed

- **No human listening review yet.** Conny's sign-off belongs here before merge.
- The Chinese translation was self-reviewed only.
- Josh has not reviewed the description of his code. Which `scgen` his environment imports
  is INFERRED: Josh's environment was not inspected; only the scgen 2.1.0 wheel was checked
  (`checks/scgen_package.txt`).
- The recommendation to wrap the cellot autoencoder is ours (INFERRED). The narration says to
  settle it with Josh.
- Nothing was trained or run on the cluster.
