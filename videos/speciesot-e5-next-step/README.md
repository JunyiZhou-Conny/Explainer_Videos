# speciesOT E5 · What next? Follow the errors

speciesOT 第五集 · 下一步做什么？跟着报错走

A method for choosing the next step: the walking skeleton, the measured error trail as a to-do board, the data card behind it, the first experiment to replicate (M1 v08) with its golden numbers, SOLID as a compass, and the ordered list of next cards.

Watch with the code open. Times are from the rendered cut; `src/speciesot/` is Josh's
package as attached on 2026-10-14; "speciesOT repo" is JunyiZhou-Conny/speciesOT at `109bf12`.

| Time | Scene | Open | What to look at |
| --- | --- | --- | --- |
| 00:00 | Monday morning | — | — |
| 00:22 | The skeleton already walks | Josh's `src/speciesot/`: `speciesot_core.py` 131–145 | the skeleton's last three verbs |
| 00:56 | The error trail | Josh's `src/speciesot/`: `speciesot_core.py` 253 · 133 · 288 · 313 | the four measured errors, in program order |
| 01:59 | The card behind the code | Josh's `src/speciesot/`: `Tests/e24_replica.ipynb` cells 3 and 6 | 18,024 and 61,759 genes |
|  |  | speciesOT repo: `specs/m1_modern.yaml` · `docs/hub_usage.md` 239 | one table + a split recipe |
| 02:40 | Pick one golden number | speciesOT repo: `AGENTS.md` 41 | the frozen benchmark |
|  |  | speciesOT repo: `speciesOT/baseline/analysis/22_v08_results.ipynb` cells 1, 3 | the notebook that writes the scorecard; cell 1 maps "m1 v08 scGen" to its cluster run folder |
|  |  | speciesOT repo: `cellot/cellot_gpu/scripts/extended_metrics.py` 154–166 | `_r2_means`; `r2_identity = _r2_means(control, treated)` |
|  |  | Josh's `src/speciesot/`: `speciesot_core.py` 161–186 | the pasted M1 settings |
|  |  | speciesOT repo: `speciesOT/baseline/analysis/v08_scorecard_dual.csv` | `r2_identity` 0.5542 · scGen R2 0.927 |
| 04:18 | SOLID as a compass | Josh's `src/speciesot/`: `speciesot_core.py` 20–33 · 107–115 · 43, 155, 133 · 54–57 | S · O · L · I |
|  |  | Josh's `src/speciesot/`: `speciesot_core.py` 247–248 | D: the only `import scgen` that runs is inside `scGenModel.setup` |
| 05:32 | The Monday loop | — | — |

Then do the [exercises](exercises.md). Evidence for every claim: [SOURCES.md](SOURCES.md).
Review record: [REVIEW.md](REVIEW.md). Series plan: [../speciesot-series/SERIES.md](../speciesot-series/SERIES.md).
