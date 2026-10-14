# Sources

The test files are not in git. They are members of the upload `src_aa1d.zip` dated 2026-10-14.

- `Tests/test_evaluation.py` lines 14-22 define `test_mmd_is_zero_for_identical_distributions` and end with `assert score == pytest.approx(0.0)`.
- `Tests/test_model.py` lines 1-12 construct `Experiment` and call `setup`. It defines no function whose name starts with `test_`.
- `Tests/e24_replica.ipynb` also calls `setup`. It is not a pytest test.
- This session did not run pytest. The command on screen is a command, not a measured result.
