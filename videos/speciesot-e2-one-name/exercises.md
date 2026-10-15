# Exercises · E2 One name, five places

1. **Find every spelling.** From the folder above `speciesot/`:
   `grep -rn "x_dimension" .` — you should find both spellings in five places
   (`Tests/config.yaml:37`, `Tests/toy_config.yaml:19`, `speciesot_core.py` 104, 220, 253).
2. **One name.** Pick a spelling and make all five agree. Before rerunning, *predict* what
   `experiment.models[1].x_dimension` will hold when `use_all_genes: True`. Then rerun the
   `e24_replica` cell and check.
3. **A test for `__init__`, without data or scgen.** `__init__` never imports scgen — only
   `setup()` does. Write `test_scgen_model_reads_config()` that builds `scGenModel` from a
   small dict and asserts a few attributes. Hint: the dict needs every key `__init__` reads,
   including `model_path`.
4. **A config-alignment test.** Load both YAML files with `yaml.safe_load` and build each model
   section with its class (no `setup()`). Which errors does it catch today? (Expect
   `KeyError: 'experiment'` from the toy config at line 86 if you go through `Experiment`.)
5. **YAML's empty value.** Change `IdentityModel: None` to `IdentityModel: null` and print
   `experiment_spec['models']`. What is the value now, and does the `isinstance(..., dict)`
   check at line 101 still do the right thing?
6. **Read a traceback.** Put a typo back, rerun, and mark two lines in the output: the WHAT line
   (the last one) and the WHERE line (the last `File "…", line N` entry).
