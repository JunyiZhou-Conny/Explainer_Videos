# speciesOT E2 · One name, five places

speciesOT 第二集 · 一个名字，五个地方

Why editing scGenModel's init means bouncing between files: a config value passes through five places, each needs the same spelling, and one fixed crash can hide a quiet bug. KeyError vs AttributeError, reading a traceback, and four rules for names.

Watch with the code open. Times are from the rendered cut; `src/speciesot/` is Josh's
package as attached on 2026-10-14; "speciesOT repo" is JunyiZhou-Conny/speciesOT at `109bf12`.

| Time | Scene | Open | What to look at |
| --- | --- | --- | --- |
| 00:00 | The error is gone. The bug is not. | Josh's `src/speciesot/`: `speciesot_core.py` 247–258 | `scGenModel.setup`; line 253 asks for `x_dimensions` |
| 00:33 | Three windows, two wires | Josh's `src/speciesot/`: `Tests/e24_replica.ipynb` cells 0–3 | `pip install -e .`, `%autoreload 2`, `Experiment(...)` |
|  |  | Josh's `src/speciesot/`: `speciesot_core.py` 68–82 | `Experiment` reads the YAML with `yaml.safe_load` |
|  |  | speciesOT repo: `pyproject.toml` | what `pip install -e .` installs |
| 01:15 | One value, five places | Josh's `src/speciesot/`: `Tests/config.yaml` 32–40 | hop 1: `z_dimension: 50` (line 38) |
|  |  | Josh's `src/speciesot/`: `speciesot_core.py` 112–115 | hop 3: setup hands the section to the class |
|  |  | Josh's `src/speciesot/`: `speciesot_core.py` 221, 254 | hop 3–4 and the reader in `setup` |
| 02:16 | Two lookups, two errors | Josh's `src/speciesot/`: `Tests/toy_config.yaml` 12–19 | the plural spelling (line 19) |
|  |  | Josh's `src/speciesot/`: `speciesot_core.py` 220, 253 | KeyError site and AttributeError site |
|  |  | Josh's `src/speciesot/`: `speciesot_core.py` 119 → 253 | the traceback's path: `Experiment.setup` calls `scGenModel.setup` |
| 03:39 | The silent twin | Josh's `src/speciesot/`: `speciesot_core.py` 97–104 | the `use_all_genes` override writes `x_dimensions` (104) |
|  |  | Josh's `src/speciesot/`: `Tests/e24_replica.ipynb` cell 3 output | `'x_dimensions': 18024` |
| 04:39 | Four rules for names | Josh's `src/speciesot/`: `speciesot_core.py` 86 | where the toy config stops (`KeyError: 'experiment'`) |
|  |  | Josh's `src/speciesot/`: `Tests/config.yaml` 31 | `IdentityModel: None` (a string) |
|  |  | Josh's `src/speciesot/`: `speciesot_core.py` 101 | the `isinstance(..., dict)` guard |
| 05:40 | Recap: follow the name | Josh's `src/speciesot/`: `Tests/config.yaml` 37 · `speciesot_core.py` 220 | already singular: keep `x_dimension` |
|  |  | Josh's `src/speciesot/`: `speciesot_core.py` 104 · 253 (right-hand side) · `Tests/toy_config.yaml` 19 | the three edits; `x_dimension=` on 253 is scgen's own parameter, leave it |
|  |  | Josh's `src/speciesot/`: `Tests/e24_replica.ipynb` | rerun, then print `experiment.models[1].x_dimension` |

Then do the [exercises](exercises.md). Evidence for every claim: [SOURCES.md](SOURCES.md).
Review record: [REVIEW.md](REVIEW.md). Series plan: [../speciesot-series/SERIES.md](../speciesot-series/SERIES.md).
