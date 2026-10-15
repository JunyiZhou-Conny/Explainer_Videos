# Exercises · E1 Four verbs and a contract

Work in Josh's `src/speciesot/` with the package installed in editable mode (`pip install -e .`
from the folder that holds `pyproject.toml`). Hints only; the typing is yours.

1. **Label the five jobs.** Above every `class` line in `speciesot_core.py`, write a one-word
   comment: data, contract, conductor, model or metric. Check yourself against the table at the
   end of the video (data 20–33, contract 35–57, conductor 67–146, model 151–294, metric 300–335).
2. **Break the contract on purpose.** In a notebook:
   ```python
   from speciesot.speciesot_core import AbstractModel
   class Half(AbstractModel):
       def setup(self): pass
   Half()
   ```
   Read the TypeError: which methods does it list? Now add `train` and `predict` — but give
   `train` *no* `training_data` argument. Does Python complain? What does that tell you about
   what an abstract class checks? (E5 comes back to this.)
3. **Two objects, two selves.** Build `a = IdentityModel()` and `b = IdentityModel()`. Set
   `a.note = "first"`. What is `b.note`? Explain the answer using the word *self*.
4. **Find the polymorphism.** Line 137 calls `model.predict(self.test_data)`. List every class
   whose `predict` can run there today, and what each returns.
5. **Josh's note (line 19).** Remove `abc.ABC` from `TrainingData` and `TestData`. Does anything
   change when you build an `Experiment`? Why not?
