# Sources and evidence

All paths are relative to the named source. "Josh's src" = the `src/` folder Conny attached on
2026-10-14 (sha256 per file in `../speciesot-series/excerpts.py`, `SOURCE_SHA256`). "Repo" =
JunyiZhou-Conny/speciesOT at `109bf12` (2026-09-08). "Checks" = `../speciesot-series/checks/`,
produced in this session (Python 3.12.3, anndata 0.13.4, scikit-learn 1.9.1, pytest 9.1.1).

| Claim on screen | Evidence | Kind |
| --- | --- | --- |
| `AttributeError: 'scGenModel' object has no attribute 'x_dimensions'` at line 253 | Checks `error_trail.json`, stage `config_setup` (stand-in scgen) | MEASURED |
| After `x_dimensions → x_dimension` at 253, setup runs and the stand-in receives `x_dimension = 1000` on 4-gene data | stage `scgen_setup_patched` | MEASURED |
| `pip install -e .` and `%autoreload 2` | Josh's src `Tests/e24_replica.ipynb` cells 0–1; repo `pyproject.toml` | READ IN NOTEBOOK |
| `yaml.safe_load` on every new Experiment | Josh's src `speciesot_core.py` 68–82 | READ IN CODE |
| Four hops for `z_dimension` (config.yaml 38 → dict → line 221 → line 254) | Josh's src | READ IN CODE |
| `KeyError: 'x_dimension'` at line 220 from the toy config's model section | stage `toy_model_section` | MEASURED |
| `Did you mean: 'x_dimension'?` | `checks/scgen_package.txt` (python3.12) | MEASURED |
| On the cluster a different scgen error may come first | Josh's comment lines 10–11 + `checks/scgen_package.txt` (scgen 2.1.0 has no VAEArith) | INFERRED |
| Dict holds `x_dimension: 1000` and `x_dimensions: 4` after setup | stage `config_snapshot` | MEASURED |
| `'x_dimensions': 18024` | Josh's src `Tests/e24_replica.ipynb` cell 3 output (older config) | READ IN NOTEBOOK |
| toy_config stops at line 86: `KeyError: 'experiment'` | stage `toy_config_setup` | MEASURED |
| `IdentityModel: None` loads as the string `'None'`; `null` → `None` | stage `yaml_none` | MEASURED |
