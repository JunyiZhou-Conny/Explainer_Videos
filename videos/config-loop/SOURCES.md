# Sources

- Committed contrast. `src/speciesot/speciesot_core.py` lines 70-71 at `109bf12648ec48ea679a3fbd7646752f1cf7cde4` test `'IdentityModel' in self.experiment_spec['models']`. There is no `scGenModel` branch in that commit.
- Upload, not a commit. `src_aa1d.zip` dated 2026-10-14. `speciesot_core.py` line 104 writes `x_dimensions`. Lines 214-225 read `x_dimension`. Lines 252-253 pass `self.x_dimensions` into `VAEArith`. Lines 131-133 call `model.train()` with no arguments. Line 261 defines `train(self, training_data)`.
- `Tests/config.yaml` line 37 uses `x_dimension`. `Tests/toy_config.yaml` line 19 uses `x_dimensions`.
- `Tests/e24_replica.ipynb` stores an output cell whose config shows `x_dimensions: 18024`. This session did not re-run that cell.
