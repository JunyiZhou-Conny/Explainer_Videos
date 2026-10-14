# Sources

Checked against `origin/main` of JunyiZhou-Conny/speciesOT at `109bf12648ec48ea679a3fbd7646752f1cf7cde4`.

- `speciesOT/baseline/analysis/02_scgen_training_analysis.ipynb` opens by saying it examines HDF5 `scalars`. `load_scalars` reads `{result_dir}/cache/scalars`.
- `specs/m2_baseline.yaml` lines 1-2 at `8a9a10368e31d9bf05db28a5e81b2e0b36af9b3a` set `experiment_tag: hvg_pearson_residuals_m2_v08_ood`.
- `speciesOT/hub/spec.py` lines 388-409 at `abf75d2091b4fcf9b55ee71f23910c92c3523024` render a config whose `name` is `scgen`. The hub does not submit the sbatch.
- `speciesOT/hub/prep.py` lines 1-7 at `780970ab2444cf8b4a23bef168d4038dbb9a2c5e` say the procedure is ported from `01.5_data_prep_all_holdouts_hvg_flavors.ipynb`.
