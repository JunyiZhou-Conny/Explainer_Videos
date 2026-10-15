# Exercises · E5 What next? Follow the errors

These are the cards, in the order the video recommends (our recommendation; adjust with Josh).
For each: write the failing test first, run it, read the last traceback line, make the smallest
change, commit.

1. **Card 1 — evaluate returns a table.** Test: identity on toy data with two metrics returns
   two numbers keyed by model and metric (a dict `{(model, metric): value}` or a pandas
   DataFrame). Today `evaluate()` returns `None` (line 145 never stores results).
2. **Card 2 — split M1 v08.** The file is one table (~8,054 cells × 1,000 genes) plus a split
   recipe (`specs/m1_modern.yaml`): `toggle_ood`, holdout `CL:0000875`, `random_state: 0`,
   `test_size: 0.2`, stratified by `condition`. Reproduce it with
   `cellot/cellot_gpu/cellot/data/cell.py:330` (`split_cell_data_toggle_ood`) and write the
   four files the data classes expect. Check: the OOD human set has 183 cells
   (`speciesOT/baseline/analysis/m1_atlas_ood_investigation/human_ood_cell_table_m1_v08.csv`).
3. **Card 3 — identity = 0.554.** Add an R²-of-means evaluation. Identity on the M1 v08 OOD
   cells must give `r2_identity = 0.5542` (`v08_scorecard_dual.csv`, row `m1 v08 scGen`) to
   about three decimals. No training, no sampling: a mismatch means the data or split differ.
4. **Card 4 — scGen ≈ 0.927.** Wrap the cellot autoencoder (E4). Before training anything, load
   the existing M1 v08 checkpoint on the cluster
   (`cellot/cellot_gpu/results/hvg_pearson_residuals_m1_v08_ood/scgen/cache/model.pt`) and check
   the plumbing; the 0.927 averages R² of means over 80-cell samples, so compute it the same way.
   Then train and aim within a tolerance.
5. **When the third model arrives.** Replace the if-chain in `setup` (lines 107–115) with a
   dictionary from names to classes. Not before.
6. **Keep a loop log.** One line per card: the call you wanted, the last traceback line, the
   change, the test. It is the "what next?" answer for the following Monday.
