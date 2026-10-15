# speciesOT E4 · scGen as arithmetic, behind one adapter

speciesOT 第四集 · scGen 是一道算术题，藏在一个适配器后面

scGen in one picture (encode, add one species arrow, decode), mapped onto setup, train and predict; the three different things called scgen in the speciesOT project; and why your scGenModel should be an adapter around exactly one of them.

Watch with the code open. Times are from the rendered cut; `src/speciesot/` is Josh's
package as attached on 2026-10-14; "speciesOT repo" is JunyiZhou-Conny/speciesOT at `109bf12`.

| Time | Scene | Open | What to look at |
| --- | --- | --- | --- |
| 00:00 | Prediction by arithmetic | — | — |
| 00:19 | Squeeze, then rebuild | Josh's `src/speciesot/`: `Tests/config.yaml` 38 | `z_dimension: 50` |
|  |  | speciesOT repo: `atlas-paper-vae/scripts/01_train_vae.py` 121–122 | both species train one network |
| 00:51 | The arithmetic | speciesOT repo: `atlas-paper-vae/scripts/02_eval_metrics.py` 166–171 | δ and the prediction |
|  |  | speciesOT repo: `cellot/cellot_gpu/cellot/transport.py` 61–69 | `transport_scgen`: the same arithmetic |
|  |  | speciesOT repo: `docs/conceptual_framework.md` §1.4 | scGen's additive assumption |
| 01:35 | Three methods, three jobs | Josh's `src/speciesot/`: `speciesot_core.py` 247–294 | the `setup` / `train` / `predict` stubs: δ computed then lost (282, 285) |
|  |  | Josh's `src/speciesot/`: `speciesot_core.py` 287–292 | predict stops at 288 (`NameError: _dense`, measured); 292 is never reached |
|  |  | Josh's `src/speciesot/`: `speciesot_core.py` 141–145 | where predict's AnnData goes: `evaluate` against the human test cells |
| 02:23 | Three things called scgen | speciesOT repo: `.gitignore` 44–47 · `atlas-paper-vae/configs/m2_v08.yaml` 44, 46–48 | the TF clone and its env |
|  |  | speciesOT repo: `atlas-paper-vae/scripts/02_eval_metrics.py` 152–168 | what Josh's helpers (265–282, 288–289) were copied from |
|  |  | Josh's `src/speciesot/`: `speciesot_core.py` 232–244 | Josh's own commented scgen 2.x attempt |
|  |  | Josh's `src/speciesot/`: `speciesot_core.py` 10–14 | Josh's note on `import scgen` |
|  |  | speciesOT repo: `cellot/cellot_gpu/cellot/models/ae.py` 21–22, 175–187 | cellot's `scgen` = AutoEncoder + shift |
|  |  | speciesOT repo: `specs/m1_modern.yaml` 33–37 · `atlas-paper-vae/configs/m2_v08.yaml` 27 | 256×2 vs 800×2 |
| 03:54 | One adapter, one choice | speciesOT repo: `cellot/cellot_gpu/cellot/models/ae.py` 33 | `load_autoencoder_model` |
|  |  | speciesOT repo: `cellot/cellot_gpu/cellot/train/train.py` 173, 250–252 | `train_auto_encoder`, which also computes the shift |
|  |  | speciesOT repo: `cellot/cellot_gpu/cellot/transport.py` 61–69 | `transport_scgen` (calls `model.eval()` at 62) |
|  |  | speciesOT repo: `scripts/predict_new_input.sh` 623–663 | your repo already makes these calls: start here |
| 05:01 | Recap: one arrow, one doorway | — | — |

Then do the [exercises](exercises.md). Evidence for every claim: [SOURCES.md](SOURCES.md).
Review record: [REVIEW.md](REVIEW.md). Series plan: [../speciesot-series/SERIES.md](../speciesot-series/SERIES.md).
