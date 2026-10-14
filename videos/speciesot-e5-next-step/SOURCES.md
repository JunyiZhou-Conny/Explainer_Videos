# Sources and evidence

All paths are relative to the named source. "Josh's src" = the `src/` folder Conny attached on
2026-10-14 (sha256 per file in `../speciesot-series/excerpts.py`, `SOURCE_SHA256`). "Repo" =
JunyiZhou-Conny/speciesOT at `109bf12` (2026-09-08). "Checks" = `../speciesot-series/checks/`,
produced in this session (Python 3.12.3, anndata 0.13.4, scikit-learn 1.9.1, pytest 9.1.1).

| Claim on screen | Evidence | Kind |
| --- | --- | --- |
| 345 lines; 83 notebooks; results since February | Josh's src; `find` over the repo (excluding checkpoints); Conny's request | READ IN CODE |
| Identity skeleton runs end to end; `evaluate` returns `None` | Checks `error_trail.json`, stage `identity_end_to_end` | MEASURED |
| Error trail: 253 AttributeError, 133 TypeError, 288 NameError, 313 ValueError | stages `config_setup`, `scgen_train`, `scgen_predict`, `r2_uneven_cells` (each run separately, smallest patch, stand-in scgen) | MEASURED |
| 18,024 / 61,759 genes in the training files | Josh's src `Tests/e24_replica.ipynb` cell 3 and cell 6 outputs | READ IN NOTEBOOK |
| Test files hold 1,000 genes | repo `e22_batch_correction.ipynb` recorded output (`n_vars=1000`) | READ IN NOTEBOOK |
| M1 v08: ~8,054 cells × 1,000 genes, one table + split recipe | repo `docs/hub_usage.md` 239; `logs/research_logs/agent_plans_2026-07-21/DELIVERABLE_C_vae_atlas_design.md` 40; `specs/m1_modern.yaml` | READ IN CODE |
| Frozen benchmark | repo `AGENTS.md` (north-star section) | READ IN CODE |
| Josh pasted the model settings into the core file | Josh's src 161–186 vs `specs/m1_modern.yaml` 31–55 | READ IN CODE |
| identity R² of means 0.5542 (full clouds, no sampling) | repo `speciesOT/baseline/analysis/v08_scorecard_dual.csv` row `m1 v08 scGen`, column `r2_identity`; `cellot/cellot_gpu/scripts/extended_metrics.py` 154–166 | READ IN CODE |
| scGen R² 0.927 (80-cell samples) | same file, row `m1 v08 scGen`, column `R2` | READ IN CODE |
| SOLID mapping; card order | our recommendation | INFERRED |
| `MODELS = {…}` registry sketch | written for this video | EXAMPLE |
