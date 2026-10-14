# Sources

Checked against `origin/main` of JunyiZhou-Conny/speciesOT at `109bf12648ec48ea679a3fbd7646752f1cf7cde4`.

- `pyproject.toml` lines 19-20, `where = ["src"]`, commit `7bb193ea0bab998e85b01326e60363c1f7cc445e`.
- `src/speciesot/__init__.py` lines 1-3, commit `cebd1465717f4b97d39d3cb5747bac7efc5597fb`.
- `src/speciesot/speciesot_core.py` is 128 lines at `109bf12648ec48ea679a3fbd7646752f1cf7cde4`. `Experiment` starts at line 48. `train` at lines 81-83 calls `model.train()` with no arguments. That file has no `scGenModel`.
- The 346-line file with `scGenModel` is the upload `src_aa1d.zip` dated 2026-10-14. It is not a commit. On-screen cards that say "upload" mean that file.
