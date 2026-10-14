# Sources

Checked against `origin/main` of JunyiZhou-Conny/speciesOT at `109bf12648ec48ea679a3fbd7646752f1cf7cde4`.

- No notebook in that checkout contains `import scgen` or `from scgen`. That search was run on the files.
- Pipe B. `cellot/cellot_gpu/scripts/train.py` lines 49-50 at `c3423310ee1a122c905cac5e686e9c55a40f59b4` call `train_auto_encoder` when `model.name` is `scgen`.
- `cellot/cellot_gpu/cellot/transport.py` lines 61-68, same commit, `transport_scgen` returns `decode(encode(x) + shift)`.
- `cellot/cellot_gpu/cellot/models/ae.py` line 175 at `af7a2c7b74d6b85f6d87734c81e44b6bba9f2a51` defines `compute_scgen_shift`.
- `speciesOT/hub/spec.py` lines 403-409 at `abf75d2091b4fcf9b55ee71f23910c92c3523024` write `name: scgen`.
- Pipe A that actually trains. `atlas-paper-vae/scripts/01_train_vae.py` lines 142-153 at `4244985eb01bbd3dbc137eabed6b74cc64f3ed7b` construct `scgen.VAEArith` and call `network.train`.
- The stub that imports scgen and ends in `pass` is `src_aa1d.zip` `speciesot_core.py` lines 247-292. That file is not a commit.
