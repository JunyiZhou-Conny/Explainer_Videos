# speciesOT E3 · A test is a question with a known answer

speciesOT 第三集 · 测试是一个答案已知的问题

What a test is, how pytest finds and runs one, where known answers come from, why test_model.py is a script and not a test, and a test that exposes which R-squared the experiment means.

Watch with the code open. Times are from the rendered cut; `src/speciesot/` is Josh's
package as attached on 2026-10-14; "speciesOT repo" is JunyiZhou-Conny/speciesOT at `109bf12`.

| Time | Scene | Open | What to look at |
| --- | --- | --- | --- |
| 00:00 | Is 0.326 right? | Josh's `src/speciesot/`: `speciesot_core.py` 320–335 | `MMDEvaluation` |
| 00:25 | Anatomy of Josh's test | Josh's `src/speciesot/`: `Tests/test_evaluation.py` 14–22 | Josh's known-answer test |
|  |  | Josh's `src/speciesot/`: `speciesot_core.py` 325–331 | `mmd_distance` |
| 01:09 | How pytest runs it | Josh's `src/speciesot/`: `Tests/test_model.py` 1–8 | a script that runs on import |
|  |  | speciesOT repo: `pyproject.toml` | the package must be installed (`pip install -e .`, E2) for the test's import to work |
| 02:07 | Known answers come from meaning | Josh's `src/speciesot/`: `speciesot_core.py` 305–316 | `R2Evaluation` (pairs cell i with cell i) |
| 02:59 | A test that asks a real question | Josh's `src/speciesot/`: `speciesot_core.py` 311–316 | the line-313 broadcast; with 5 vs 5 cells it runs and pairs unrelated cells (R² 0.103, `checks/error_trail.json`) |
|  |  | speciesOT repo: `atlas-paper-vae/scripts/02_eval_metrics.py` 47–53 | `_pergene_r2`, the same formula, used for reconstruction |
|  |  | speciesOT repo: `cellot/cellot_gpu/scripts/decoded_frame_metrics.py` 68–71 | `_r2_means`, the benchmark's R² |
|  |  | speciesOT repo: `docs/conceptual_framework.md` §5.2 | r2-means vs r² |
| 04:07 | Three layers of checks | Josh's `src/speciesot/`: `Tests/toy_config.yaml` | the seed of the middle layer |
|  |  | Josh's `src/speciesot/`: `Tests/e24_replica.ipynb` | the top layer |
| 04:49 | Recap: questions with answers | — | — |

Then do the [exercises](exercises.md). Evidence for every claim: [SOURCES.md](SOURCES.md).
Review record: [REVIEW.md](REVIEW.md). Series plan: [../speciesot-series/SERIES.md](../speciesot-series/SERIES.md).
