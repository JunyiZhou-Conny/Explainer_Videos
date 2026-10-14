# Sources and evidence

All paths are relative to the named source. "Josh's src" = the `src/` folder Conny attached on
2026-10-14 (sha256 per file in `../speciesot-series/excerpts.py`, `SOURCE_SHA256`). "Repo" =
JunyiZhou-Conny/speciesOT at `109bf12` (2026-09-08). "Checks" = `../speciesot-series/checks/`,
produced in this session (Python 3.12.3, anndata 0.13.4, scikit-learn 1.9.1, pytest 9.1.1).

| Claim on screen | Evidence | Kind |
| --- | --- | --- |
| Four calls setup/train/predict/evaluate | Repo `e24_src_example.ipynb` cell 1 (written; no recorded execution) | READ IN CODE |
| 345 lines; the five jobs and their line ranges | Josh's src `speciesot_core.py` (20–33, 35–57, 67–146, 151–294, 300–335) | READ IN CODE |
| Line 115 builds `scGenModel(config)`; `__init__` lines 214–225 | Josh's src `speciesot_core.py` | READ IN CODE |
| Attribute values on the object card | Josh's src `Tests/config.yaml` 32–40; `model_path` set at line 114 | READ IN CODE |
| `TypeError: Can't instantiate abstract class AbstractModel without an implementation for abstract methods 'predict', 'setup', 'train'` | Checks `error_trail.json`, stage `abstract` (Python 3.12 wording) | MEASURED |
| ABCs check method names at construction, not signatures | Python `abc` semantics; `IdentityModel.train(self)` (line 155) is accepted although the contract's `train` takes `training_data` (line 43) | READ IN CODE |
| `abc.ABC` can be dropped from data classes | Josh's comment, line 19 | READ IN CODE |
| `evaluate` drops its results (line 145) | Checks `error_trail.json`, stage `identity_end_to_end`: `evaluate_returned: null` | MEASURED |
| Identity returns the mouse cells (line 159); setup's if-chain (107–115) | Josh's src | READ IN CODE |
| The `x.xxx` grid numbers | placeholders, not results | — |
