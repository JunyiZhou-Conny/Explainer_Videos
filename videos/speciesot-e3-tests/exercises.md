# Exercises · E3 A test is a question with a known answer

Run tests with `pytest -q` from the folder that holds `speciesot/`. Keep test data tiny and
build it inside the test.

1. **Run Josh's test alone.** `pytest -q src/speciesot/Tests/test_evaluation.py` — one dot, one
   pass. Then run the whole folder and watch `test_model.py` stop collection.
2. **Known answers, as tests.** Write one test each:
   - MMD of a cloud against itself is 0 (Josh's test, already there).
   - MMD grows with shift: `mmd(x, x + 0.5) < mmd(x, x + 2.0)`.
   - `R2Evaluation` of a perfect prediction is 1.
   - R² *of means* (write a tiny helper first): gene means `[1, 2, 3]` vs `[1, 3, 2]` give
     r = 0.5, so R² = 0.25. Shuffling the rows must not change it.
3. **Turn `test_model.py` into a test.** Wrap its body in `def test_experiment_runs_on_toy(tmp_path):`.
   Build four tiny AnnData files under `tmp_path`, write a toy YAML with `yaml.safe_dump`, then
   run `setup()` with only `IdentityModel`. Hints: `ad.AnnData(np.random.default_rng(0).normal(size=(6, 4)))`,
   `.write_h5ad(tmp_path / "mouse_train.h5ad")`.
4. **Decide the R².** One paragraph in your own notes: which R² does the M1 v08 replication
   need, and why? Read `docs/conceptual_framework.md` §5.2 and
   `cellot/cellot_gpu/scripts/decoded_frame_metrics.py` lines 68–71 in the speciesOT repo.
5. **The loop.** For the next week, before opening the `e24_replica` notebook, run `pytest -q`.
   Note how often it catches something first.
