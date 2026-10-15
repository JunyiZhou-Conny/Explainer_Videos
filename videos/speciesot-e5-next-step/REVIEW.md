# Review record: E5 · Your next step

Produced 2026-10-14/15 by a Claude Code cloud session (PR #17, branch
`claude/clever-wozniak-3ocis0`) for Conny. Verified facts and unclaimed reviews are kept
separate.

## Content gates (AGENTS.md)

1. **Hook**: s01 sets up "Monday morning" with a file of almost 350 lines (346 on screen), 83
   notebooks, and results since February. Where does the next hour go? ✔
2. **Intuition before formalism, with an animated mechanism per idea**:
   - Walking skeleton: an identity token walks four stage boxes (MEASURED ✓ each), and
     evaluate's dropped scores become card 1.
   - Error trail: a measured run stops at each stage. The cards slide onto a board with
     scGen's path (253 → 133 → 288); the identity run's 313 is "fixed by R² of means".
   - Cards behind the code: the gene-count bars shrink to the shared 1,000, and the M1 v08 table
     splits by the spec's recipe.
   - Golden number: "not a notebook". The 83 tiles strike out to "a spec + a scorecard row".
     The CSV row's numbers fly out with their source notebook. `_r2_means` is shown with
     control and treated labelled, and a ladder runs data → identity → scGen.
   - SOLID: each letter lands on its lines in the file's shape.
   - Monday loop: a token goes around write → run → read → change → commit. ✔
3. **Ponder moments and recap**:
   - s03 asks which stage breaks first; s05 asks which of 83 notebooks to replicate first. Both
     carry `pause_after` 4 s.
   - s07 lists the cards in order, with a test sketch for card 3, and recaps the episode. ✔
4. **Written for the ear; anchored cues**:
   - Every reveal is tied to a `wait_until` phrase.
   - `check_anchors.py` checks both presence and spoken order. ✔
5. **Simulated-viewer QA over the full draft**: findings and fixes are below. ✔
6. **Measured checks**: see Verified. **Conny's listening sign-off: pending.** ✘ (not yet)

## Whole-video QA (first full cut, 5:37, 2026-10-14)

A simulated-Conny pass verified every code line, the four error messages, the scorecard row
(both numbers stay on screen after they fly out), the yaml lines and the metric code.
Problems and fixes:

**Wrong**

- An on-screen note said "one name, four places" after E2 was retitled. FIX: "five places".
- "A three hundred and fifty line file" against "346" on screen. FIX: "a file of almost three
  hundred and fifty lines".

**Confusing / blocking**

- Conny's question 2 got an arbitrary red tile, implying the answer is some notebook. FIX: "Not
  a notebook". The tiles strike out to "a spec + a scorecard row", the row names the notebook
  that writes it (`22_v08_results.ipynb`, cell 3), and the scGen run's cluster folder is
  shown (cell 1).
- "The program hands you the order" contradicted s07's card order. FIX:
  - The program orders the errors along scGen's path, and you choose which path to walk first.
  - The board groups 253 → 133 → 288.
  - s07 walks identity's path first, because it has an exact answer.
- Identity's 0.5542 sat on a row named "scGen" without explanation. FIX: it is the same on
  every M1 v08 row (rows 4 and 5 shown), because it describes the data. control = mouse test
  cells (what IdentityModel returns), treated = human. "Comparing means, not cells, also
  removes the crash at line 313."
- Question 3 was only implied. FIX: "You don't need to trace all of cellot: open only the few
  calls your adapter makes (E4). Your own scorecard is the check." (INFERRED)
- "Never to scgen directly" sounded like the model. FIX: "It never imports the scgen library;
  only scGenModel does, at line 248."
- "Reads the first thing that breaks" vs "the last line of the traceback". FIX: "Read the first
  error it hits: its message is the last line of the traceback."
- The gene bars stretched as if genes were added. FIX: they shrink to the shared 1,000, with
  "done in M1 v08".
- Card 3 counted up as if identity converges. FIX: it snaps ≠ → = 0.5542 ✓, beside a three-line
  test sketch (EXAMPLE).
- The ponders had 3.3 s of silence. FIX: `pause_after` 4 s each.

**Polish**:
- "~8,054 cells".
- yaml shown with "…" rows and `test_size`.
- "≈ exact (no training)", and the sampling picture is tagged EXAMPLE.
- READ IN CODE tags on 346 / 83.
- Scores spaced away from "returned None".

**Chinese**: calques rewritten (代码开始难改、难测的时候, 定义在 train 内部, 人类训练文件), and
dash splits removed.

**Bot review**:
- Bugbot's "glyph group detaches the scorecard digits" was checked by a Manim dry run and in
  frames, and was not real.
- Its "stale assertion survives the transform" did not show in frames either. The swap was
  made whole-object anyway.

## Verified (final render)

FILLED AFTER THE FINAL BUILD.

## Not claimed

- **No human listening review yet.** Conny's sign-off belongs here before merge.
- The Chinese translation was self-reviewed only.
- The card order and the SOLID mapping are our recommendation (INFERRED, tagged).
- The toy-data error trail used a stand-in scgen; the cluster may stop earlier, at line 252
  (E4).
- Nothing was run on the cluster. 0.5542 and 0.927 are read from the scorecard CSV, not
  reproduced here.
