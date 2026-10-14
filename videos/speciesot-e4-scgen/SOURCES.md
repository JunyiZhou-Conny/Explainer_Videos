# Sources and evidence

All paths are relative to the named source. "Josh's src" = the `src/` folder Conny attached on
2026-10-14 (sha256 per file in `../speciesot-series/excerpts.py`, `SOURCE_SHA256`). "Repo" =
JunyiZhou-Conny/speciesOT at `109bf12` (2026-09-08). "Checks" = `../speciesot-series/checks/`,
produced in this session (Python 3.12.3, anndata 0.13.4, scikit-learn 1.9.1, pytest 9.1.1).

| Claim on screen | Evidence | Kind |
| --- | --- | --- |
| scGen: δ = mean(z_human) − mean(z_mouse) on training cells; predict = decode(encode(x) + δ) | repo `docs/conceptual_framework.md` §1.4; `atlas-paper-vae/scripts/02_eval_metrics.py` 166–171; `cellot/cellot_gpu/cellot/transport.py` 61–69 | READ IN CODE |
| 50 latent numbers | Josh's src `Tests/config.yaml` 38 (`z_dimension: 50`) | READ IN CODE |
| Both species train one network | repo `atlas-paper-vae/scripts/01_train_vae.py` 121–122; `cellot/cellot_gpu/cellot/train/train.py` 250–252 | READ IN CODE |
| Stubs: δ local (282), training commented (284), `pass` (285), predict returns mouse cells (292) | Josh's src | READ IN CODE |
| TF scgen = git-ignored nested clone on `sys.path`, env `scgen_tf1` (TF 1.15) | repo `atlas-paper-vae/configs/m2_v08.yaml` 44, 46–48; `.gitignore` 44–47; `01_train_vae.py` 86, 107–108 | READ IN CODE |
| Josh's helpers match the atlas scripts | Josh's src 265–282 and 288–289 vs repo `02_eval_metrics.py` 151–167 (169–171, the predict step, is not copied) | READ IN CODE |
| scgen 2.x (scvi-tools) exports `SCGEN`, `SCGENVAE`; no `VAEArith` | `checks/scgen_package.txt` (scgen 2.1.0 wheel) | READ IN PACKAGE |
| Josh's environment loads that package | Josh's comment lines 10–11 ("pulls in scvi-tools/torch") | INFERRED |
| cellot is a vendored copy of bunnech/cellot; its `scgen` is `AutoEncoder` + `compute_scgen_shift` | repo `cellot/cellot_gpu/setup.py`, `LICENSE`, `cellot/models/ae.py` 21–22, 175–187 | READ IN CODE |
| The benchmark scGen numbers came from the cellot autoencoder | repo `logs/research_logs/agent_plans_2026-07-21/DELIVERABLE_A_atlas_memory.md` 20 | READ IN CODE |
| Config hidden 256×2, latent 50, lr 0.001 = cellot AE spec; TF fixes 2 × 800 | Josh's src `Tests/config.yaml` 34–38; repo `specs/m1_modern.yaml` 33–37; `atlas-paper-vae/configs/m2_v08.yaml` 27 | READ IN CODE |
| Adapter calls: `load_autoencoder_model` (ae.py 33), `train_auto_encoder` (train/train.py 173), `encode`/`decode` (ae.py 149/152), `compute_scgen_shift` (ae.py 175) | repo `cellot/cellot_gpu/cellot/` | READ IN CODE |
| Wrap the cellot autoencoder | our recommendation | INFERRED |
| A 3-line fake stands in for the library | `checks/error_trail.py` (`FakeVAEArith`) | MEASURED |
| The latent-space picture | a 2-D sketch of a 50-D space | — |
| Predict never reaches its last line: line 288 raises `NameError: name '_dense' is not defined` | Checks `error_trail.json`, stage `scgen_predict`; Josh's src 287–292 (`_dense`, `mouse_ood`, `human_ood` exist only in `train` / the atlas script) | MEASURED |
| Only the layer sizes go nowhere: `z_dimension` and `lr` do reach VAEArith | Josh's src 252–258 (`z_dimension=self.z_dimension`, `learning_rate = self.lr`); `hidden_units` is never passed | READ IN CODE |
| Josh's class mixes all three scgens: helpers (#1), import (#2), settings (#3) | Josh's src 265–273 (`sess.run`, `mu`: TF VAEArith), 248 + comment 10–11 (`import scgen`, scvi-tools), `Tests/config.yaml` 34–38 (cellot spec); also his commented scgen 2.x setup, 232–244 | READ IN CODE |
| The adapter's calls for the cellot autoencoder | repo `cellot/cellot_gpu/cellot/models/ae.py` 33 (`load_autoencoder_model`), 149/152 (`encode`/`decode`), 175 (`compute_scgen_shift`); `train/train.py` 173 (`train_auto_encoder`, which already calls `compute_scgen_shift` at 250–252); `transport.py` 61–69 (`transport_scgen`, calls `model.eval()`); config template `configs/models/scgen.yaml` | READ IN CODE |
| `model.eval()` is required before encoding (dropout) | repo `scripts/bake_model_artifacts.py` 119–120 | READ IN CODE |
| Your repo already makes these calls | repo `scripts/predict_new_input.sh` 623–663 (load, eval, shift, encode, decode) | READ IN CODE |
| On-screen `src/speciesot/speciesot_core.py` panels are Josh's attached copy (346 lines), not the 128-line file at that path in the repo at 109bf12 | `wc -l` of both | READ IN CODE |
