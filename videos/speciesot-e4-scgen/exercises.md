# Exercises · E4 scGen as arithmetic, behind one adapter

1. **Draw it with shapes.** On paper: mouse train (cells × genes) → encode → (cells × 50) →
   column mean → δ (50,) ← human train likewise. Then held-out mouse (cells × genes) → encode →
   + δ → decode → predicted (cells × genes). Which arrays must share a gene axis?
2. **Read only the doorway.** In the speciesOT repo, open the four calls your adapter makes and
   write one line each (inputs → outputs), all under `cellot/cellot_gpu/cellot/`:
   - `models/ae.py` 33 · `load_autoencoder_model`
   - `train/train.py` 173 · `train_auto_encoder` (it takes a cellot config plus an `.h5ad` path,
     not an AnnData, and already calls `compute_scgen_shift`, `models/ae.py` 175, at 250–252;
     config template `cellot/cellot_gpu/configs/models/scgen.yaml`)
   - `model.eval()` (why it must come before encoding: `scripts/bake_model_artifacts.py` 119–120)
   - `transport.py` 61–69 · `transport_scgen` (uses `encode` / `decode`, `models/ae.py` 149 / 152)

   Then read `scripts/predict_new_input.sh` 623–663: your repo already makes these calls there.
3. **Comments before code.** In `scGenModel`, write `train` and `predict` as numbered comments
   only. Where does δ live after `train` returns? What exactly does `predict` return (an AnnData
   with which `var_names`)?
4. **Bring the table to Josh.** The three scgens (TF VAEArith clone · scvi-tools `scgen` ·
   cellot's AutoEncoder): which one does `import scgen` load in his environment
   (`python -c "import scgen; print(scgen.__version__, hasattr(scgen, 'VAEArith'))"`), and
   which one should the adapter wrap?
5. **A fake with a known answer.** Write a `FakeAutoEncoder` whose `encode` and `decode` do
   nothing (return their input). With it, `predict` must return exactly
   `mouse + (mean(human) − mean(mouse))`. Turn that into a test of your adapter's arithmetic —
   no library needed.
