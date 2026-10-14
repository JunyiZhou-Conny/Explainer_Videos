# Sources and evidence

All paths are relative to the named source. "Josh's src" = the `src/` folder Conny attached on
2026-10-14 (sha256 per file in `../speciesot-series/excerpts.py`, `SOURCE_SHA256`). "Repo" =
JunyiZhou-Conny/speciesOT at `109bf12` (2026-09-08). "Checks" = `../speciesot-series/checks/`,
produced in this session (Python 3.12.3, anndata 0.13.4, scikit-learn 1.9.1, pytest 9.1.1).

| Claim on screen | Evidence | Kind |
| --- | --- | --- |
| 346 lines (editor count; `wc -l` 345, no final newline); 83 notebooks; results since February | Josh's src; `find` over the repo (excluding checkpoints); Conny's request | READ IN CODE |
| Identity skeleton runs end to end; `evaluate` returns `None` | Checks `error_trail.json`, stage `identity_end_to_end` | MEASURED |
| Error trail: 253 AttributeError, 133 TypeError, 288 NameError, 313 ValueError | stages `config_setup`, `scgen_train`, `scgen_predict`, `r2_uneven_cells` (each run separately, smallest patch, stand-in scgen) | MEASURED |
| 18,024 / 61,759 genes in the training files | Josh's src `Tests/e24_replica.ipynb` cell 3 and cell 6 outputs | READ IN NOTEBOOK |
| Test files hold 1,000 genes | mouse: repo `e22_batch_correction.ipynb` cell 47 output (`n_obs=251, n_vars=1000`); human: repo `tb/tb2_human_setup.ipynb` projects the BCG cells onto the 1,000 atlas genes (cell 14 "Genes for scANVI … 1000"; cell 17 `combined` 729 × 1000 = 230 control + 392 treated + 107 atlas) | READ IN NOTEBOOK |
| M1 v08: ~8,054 cells × 1,000 genes, one table + split recipe | repo `docs/hub_usage.md` 239; `logs/research_logs/agent_plans_2026-07-21/DELIVERABLE_C_vae_atlas_design.md` 40; `specs/m1_modern.yaml` | READ IN CODE |
| Frozen benchmark | repo `AGENTS.md` (north-star section) | READ IN CODE |
| Josh pasted the model settings into the core file | Josh's src 161–186 vs `specs/m1_modern.yaml` 31–55 | READ IN CODE |
| identity R² of means 0.5542 (full clouds, no sampling) | repo `speciesOT/baseline/analysis/v08_scorecard_dual.csv` row `m1 v08 scGen`, column `r2_identity`; `cellot/cellot_gpu/scripts/extended_metrics.py` 154–166 | READ IN CODE |
| scGen R² 0.927 (80-cell samples) | same file, row `m1 v08 scGen`, column `R2` | READ IN CODE |
| SOLID mapping; card order | our recommendation | INFERRED |
| `MODELS = {…}` registry sketch | written for this video | EXAMPLE |
| Held-out split picture (no proportions; the real split halves held-out cells into ignore / ood) | `specs/m1_modern.yaml` 28 (`toggle_ood`); repo `cellot/cellot_gpu/cellot/data/cell.py` 330–340 (50/50 ignore/ood) | INFERRED (schematic, tagged) |
| The scorecard is written by `22_v08_results.ipynb`; the scGen run lives under `cellot/cellot_gpu/results/hvg_pearson_residuals_m1_v08_ood/scgen/` (on the cluster, not in git) | repo `speciesOT/baseline/analysis/22_v08_results.ipynb` cell 3 (`dual.to_csv(… v08_scorecard_dual.csv)`), cell 1 (`MODELS`: "m1 v08 scGen" → `hvg_pearson_residuals_m1_v08_ood/scgen`) | READ IN NOTEBOOK |
| Identity R² of means 0.5542 is the same on every M1 v08 row: it describes the data | repo `v08_scorecard_dual.csv` rows 4 and 5 (`r2_identity` 0.5542 for IMPACT and scGen); `cellot/cellot_gpu/scripts/extended_metrics.py` 165 (`r2_identity = _r2_means(control, treated)`) | READ IN CODE |
| Comparing means, not cells, removes the line-313 crash | `_r2_means` averages each set over cells before correlating (extended_metrics.py 154–157), so unequal cell counts are fine; Josh's `R2Evaluation` multiplies row i by row i (core 311–313) | READ IN CODE |
| "open only the few calls your adapter makes" | E4's adapter list (`ae.py` 33, 149, 152, 175; `train.py` 173) | INFERRED (our recommendation) |
