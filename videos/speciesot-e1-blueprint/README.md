# speciesOT E1 · Four verbs and a contract

speciesOT 第一集 · 四个动词和一份契约

How to read speciesot_core.py: every class does one of five jobs. Classes, objects, init and self; abstract classes as contracts that check names, not inputs; the Experiment that conducts models and metrics. For a researcher who has never designed a Python package.

Watch with the code open. Times are from the rendered cut; `src/speciesot/` is Josh's
package as attached on 2026-10-14; "speciesOT repo" is JunyiZhou-Conny/speciesOT at `109bf12`.

| Time | Scene | Open | What to look at |
| --- | --- | --- | --- |
| 00:00 | Four calls, one experiment | speciesOT repo: `e24_src_example.ipynb`, cell 1 | the four calls |
|  |  | Josh's `src/speciesot/`: `speciesot_core.py` | the whole file: 346 lines, five jobs |
| 00:29 | A class is a blueprint | Josh's `src/speciesot/`: `speciesot_core.py` 115 | `scGenModel(...)` builds an object |
|  |  | Josh's `src/speciesot/`: `speciesot_core.py` 212–225 | `__init__` writes one fact per line |
|  |  | Josh's `src/speciesot/`: `Tests/config.yaml` 32–40 | where those facts come from |
| 01:13 | A contract with blanks | Josh's `src/speciesot/`: `speciesot_core.py` 35–48 | `AbstractModel`: the contract |
|  |  | Josh's `src/speciesot/`: `speciesot_core.py` 54–57 | `AbstractEvaluation`: a one-method contract |
|  |  | Josh's `src/speciesot/`: `speciesot_core.py` 151, 212 | `IdentityModel(AbstractModel)`, `scGenModel(AbstractModel)` sign it |
|  |  | Josh's `src/speciesot/`: `speciesot_core.py` 43 vs 155 | contract `train(self, training_data)` vs `train(self)`: names, not inputs |
|  |  | Josh's `src/speciesot/`: `speciesot_core.py` 19–20 | `abc.ABC` on data classes; Josh's note |
| 02:27 | The Experiment conducts | Josh's `src/speciesot/`: `speciesot_core.py` 67–77 | `Experiment.__init__` |
|  |  | Josh's `src/speciesot/`: `speciesot_core.py` 84–128 | `setup` fills `self.models` and `self.evaluations` |
|  |  | Josh's `src/speciesot/`: `speciesot_core.py` 131–145 | `train`, `predict`, `evaluate`; line 145 drops the scores |
|  |  | Josh's `src/speciesot/`: `Tests/config.yaml` 30–45 | the `models` and `evaluations` sections |
| 03:12 | Why the contract pays | Josh's `src/speciesot/`: `speciesot_core.py` 135–138 | one call, `model.predict`, line 137 |
|  |  | Josh's `src/speciesot/`: `speciesot_core.py` 158–159 | `IdentityModel.predict` returns the mouse cells |
|  |  | Josh's `src/speciesot/`: `speciesot_core.py` 106–115 | the if-chain that names each model |
| 03:56 | Recap: five jobs | Josh's `src/speciesot/`: `speciesot_core.py` | data 20–33 · contract 35–57 · conductor 67–146 · model 151–294 · metric 300–335 |

Then do the [exercises](exercises.md). Evidence for every claim: [SOURCES.md](SOURCES.md).
Review record: [REVIEW.md](REVIEW.md). Series plan: [../speciesot-series/SERIES.md](../speciesot-series/SERIES.md).
