# Review record: E3 · A test is a question with a known answer

Produced 2026-10-14/15 by a Claude Code cloud session (PR #17, branch
`claude/clever-wozniak-3ocis0`) for Conny. Verified facts and unclaimed reviews are kept
separate.

## Content gates (AGENTS.md)

1. **Hook**: s01 opens on a number nobody can check by eye. Josh's MMD metric gives 0.326 on toy
   cells (MEASURED): is that right? The recap closes it. 0.326 itself can't be checked, but the
   code can be checked where it must give 0, 1 and "more". ✔
2. **Intuition before formalism, with an animated mechanism per idea**:
   - MMD as kernel averages: a kept 3-point plot. The pair at d² = 2 gives e⁻¹ ≈ 0.368 and the
     pair at d² = 8 gives e⁻⁴ ≈ 0.018. Each lights its grid cells; all three averages are equal,
     so "= 0" carries into `approx(0.0)`.
   - How pytest runs a test: the file tree, the `test*` rule, and the run that stops early on a
     script.
   - Known answers from meaning:
     - MMD grows bar by bar as one cloud is shifted (0 / 0.08 / 0.29 / 0.85, MEASURED).
     - The shuffle keeps the same cloud but drops R² from 1.0 to 0.020.
   - A real question: rows lined up cell by cell, the 5-vs-7 crash at line 313, and the 5-vs-5
     run that silently pairs unrelated cells (R² 0.103, MEASURED).
   - Three layers of checks, as a pyramid. ✔
3. **Ponder moments and recap**:
   - Three ponders, each with a `pause_after: 4.0` line and a veil:
     - s03 ≈ 1:32, the whole folder (4.3 s of silence);
     - s04 ≈ 2:17, the shifted cloud (4.4 s);
     - s05 ≈ 3:12, 5 vs 7 cells (4.4 s).
   - s07 recaps:
     - a test is a question with a known answer;
     - known answers come from meaning;
     - a test can expose an assumption;
     - tests come in layers, with the exercises at the end. ✔
4. **Written for the ear; anchored cues**:
   - Numbers are spoken as words, and h5ad is in the lexicon.
   - Every reveal is tied to a `wait_until` phrase.
   - `check_anchors.py` checks both presence and spoken order. ✔
5. **Simulated-viewer QA over the full draft**: findings and fixes are below. ✔
6. **Measured checks**: see Verified. **Conny's listening sign-off: pending.** ✘ (not yet)

## Whole-video QA (first full cut, 5:05, 2026-10-14)

A simulated-Conny pass found **no factual errors**. It recomputed every on-screen number from
the stated seeds with Josh's own classes:
- the MMD decomposition and kernel values;
- MMD against shift;
- the shuffled R²;
- the three example tests, which pass.

Problems and fixes:

**Confusing / blocking**

- [3:07] Only the crash was shown. With equal cell counts, R2Evaluation runs and pairs
  unrelated cells, so the natural "fix" (subsample to equal counts) hides the bug. FIX: a new
  measured beat, "R² 0.103 · it pairs unrelated cells", and the card "needs a true partner for
  every cell".
- [4:32] The recap covered two of five ideas and never closed the hook. FIX: the recap closes
  the 0.326 question, adds "a test can expose an assumption" and "unit tests first, the notebook
  last".
- [0:49] The "= 0" punchline was on screen for 1 s. FIX: it now carries into `approx(0.0)`
  on line 22.
- [0:35] Kernel numbers appeared after the points vanished. FIX: a kept mini plot with the two
  pairs drawn.
- [4:09] The MEASURED KeyError line was on screen for 1.3 s. FIX: it appears at "toy_config"
  and stays.
- [2:59] The R2Evaluation chip was wedged between the matrices. FIX: it now sits below them,
  with arrows.
- [2:10, 3:03] The ponders had 3.4 s of silence, and there was none in the first two minutes.
  FIX: ~4.5 s each, plus a new ponder at the pytest run.

**Polish**:
- "approx: floating-point sums are rarely exactly 0", using the real 0.1 + 0.2 − 0.3.
- The failure note names `speciesot_core.py:331` and "excerpt of real pytest output".
- The install note (`pip install -e .`, E2).
- The notebook is greyed in the Tests/ tree, and the chip reads `test*`.
- "multi-GB atlas files".
- "same cloud · MMD still 0 · R² 1.0 → 0.020".
- Role labels "predicted (mouse) · 5" and "truth (human) · 7".
- 系统测试, and an INFERRED tag on "minutes to hours".
- Labels on the decomposition.

**Chinese and captions**:
- Calques rewritten: 一些模拟的玩具数据, 醒目地报错失败, 已知答案来自指标的含义, 名字以 test_ 开头的文件.
- The cell-i pairing is rephrased as predicted vs truth.
- Cue-splitting phrasing fixed ("A good test runs on your code alone.").

**Bot review**: Bugbot flagged a real scatter-to-mini-plot hand-off fight in an intermediate
commit. It is fixed: the clouds are settled as whole objects first, and the result was
verified in a frame.

## Verified (final render)

- **Encode**: 339.026 s, 1920×1080 @ 30 fps, H.264 + AAC; seven scenes. The narration minimum
  is 318.5 s, including three 4 s ponder pauses; nothing was clipped.
- **Captions**: 79 bilingual cues, ordered, non-overlapping and inside the runtime. The widest
  lines are 1370 px (zh) and 1339 px (en), within the 1740 px caption area.
- **Mix**: voice −16.05 LUFS; music −22.05 LUFS in gaps and −31.71 under speech; mix −16.38
  LUFS; true peak −0.99 dBTP. The Swiss style check passed.
- **Render log**: no BUDGET, CODEPANEL or missing-anchor lines. Grep hits on "Error" are Manim
  progress bars naming on-screen text such as `FileNotFoundError`.
- **Silences**: at most 5.6 s, at a scene cut; the ponders hold 4.3–4.4 s.
- **ASR round trip**: see below.
- **Evidence** (`../speciesot-series/checks/`):
  - Measured:
    - 0.326 and 0.103 (`identity_end_to_end`);
    - the known answers (`known_answers`);
    - the (5,4)/(7,4) ValueError (`r2_uneven_cells`);
    - `1 passed in 1.45s` and the `test_model.py` collection error (`pytest_run.txt`).
  - The failing-test output is real pytest output from a scratch copy with the `2 *` removed,
    tagged EXAMPLE.

## Not claimed

- **No human listening review yet.** Conny's sign-off belongs here before merge.
- The Chinese translation was self-reviewed only.
- Josh has not reviewed the description of his tests.
- `test_model.py`'s behaviour on the cluster (loading the full atlas, then failing in setup)
  is INFERRED from its code; it was not run there.
