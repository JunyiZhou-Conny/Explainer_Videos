# Sources and evidence

All paths are relative to the named source. "Josh's src" = the `src/` folder Conny attached on
2026-10-14 (sha256 per file in `../speciesot-series/excerpts.py`, `SOURCE_SHA256`). "Repo" =
JunyiZhou-Conny/speciesOT at `109bf12` (2026-09-08). "Checks" = `../speciesot-series/checks/`,
produced in this session (Python 3.12.3, anndata 0.13.4, scikit-learn 1.9.1, pytest 9.1.1).

| Claim on screen | Evidence | Kind |
| --- | --- | --- |
| Toy MMD 0.326 (identity prediction vs toy human cells) | Checks `error_trail.json`, stage `identity_end_to_end` | MEASURED |
| Josh's MMD test: three cells, two genes, identical → 0 | Josh's src `Tests/test_evaluation.py` 14–22; stage `known_answers.josh_test_mmd_identical = 0.0` | READ IN CODE / MEASURED |
| Kernel values for the three points (γ = 0.5): e⁻¹ ≈ 0.368, e⁻⁴ ≈ 0.018 | arithmetic of `rbf_kernel` | — |
| pytest discovery rules | pytest defaults (`test_*.py` / `*_test.py`, `test*` functions) | — |
| `1 passed in 1.45s`; `test_model.py` collection error `FileNotFoundError` | Checks `pytest_run.txt` | MEASURED |
| On the cluster `test_model.py` loads the full files and fails in setup during collection | Josh's src `Tests/test_model.py` 5–8 + code path | INFERRED |
| MMD vs shift 0 / 0.080 / 0.292 / 0.847; R² perfect 1.0, shuffled 0.020 | stage `known_answers` (40 cells × 3 genes, seed 1) | MEASURED |
| `ValueError … shapes (5,4) (7,4)` at line 313 | stage `r2_uneven_cells` | MEASURED |
| `R2Evaluation` = the per-gene formula of `_pergene_r2` (reconstruction) | Josh's src 305–316; repo `atlas-paper-vae/scripts/02_eval_metrics.py` 47–53, used at 208/210 | READ IN CODE |
| The benchmark uses R² of means | repo `cellot/cellot_gpu/scripts/decoded_frame_metrics.py` 68–71; `extended_metrics.py` 154–166; `docs/conceptual_framework.md` §5.2 | READ IN CODE |
| Test sketches in s04 | written for this video | EXAMPLE |
