"""Run the speciesot package on tiny fake data and record the first error at each stage.

Usage:  python error_trail.py <dir containing the speciesot package> <output.json>

Nothing here edits the package. Each stage builds a fresh Experiment from a toy config
(same shape as Tests/config.yaml, with the cluster paths swapped for toy .h5ad files) and
records what happens. A stage that needs an earlier error "fixed" applies the smallest
possible in-memory patch and says so, so the next error can be seen.

`scgen` is replaced by a stub module (FakeVAEArith) so the stages run without TensorFlow;
the stub records its constructor arguments. Every result says whether the stub was involved.
"""
import json
import sys
import tempfile
import traceback
import types
from pathlib import Path

import anndata as ad
import numpy as np
import yaml

PKG_PARENT = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2])
sys.path.insert(0, str(PKG_PARENT))

# --- a stub `scgen` so scGenModel.setup() can import something ------------------------------
fake = types.ModuleType("scgen")


class FakeVAEArith:
    def __init__(self, **kwargs):
        self.kwargs = kwargs


fake.VAEArith = FakeVAEArith
sys.modules["scgen"] = fake

import speciesot  # noqa: E402
from speciesot import speciesot_core as core  # noqa: E402

work = Path(tempfile.mkdtemp(prefix="speciesot-toy-"))
rng = np.random.default_rng(0)


def toy(name, n_cells, n_genes=4, shift=0.0):
    a = ad.AnnData(rng.normal(shift, 1.0, size=(n_cells, n_genes)).astype(np.float32))
    a.var_names = [f"gene{i}" for i in range(n_genes)]
    path = work / f"{name}.h5ad"
    a.write_h5ad(path)
    return str(path)


paths = {
    "src_train": toy("mouse_train", 6), "tgt_train": toy("human_train", 6, shift=1.0),
    "src_test": toy("mouse_test", 5), "tgt_test": toy("human_test", 5, shift=1.0),
    "tgt_test_uneven": toy("human_test_uneven", 7, shift=1.0),
}

FULL = {
    "experiment": {"experiment_export_path": str(work / "export")},
    "training_data": {"source_training_data_path": paths["src_train"],
                      "target_training_data_path": paths["tgt_train"]},
    "test_data": {"source_test_data_path": paths["src_test"],
                  "target_test_data_path": paths["tgt_test"]},
    "models": {"IdentityModel": None,
               "scGenModel": {"random_state": 0, "hidden_units": [256, 256], "lr": 0.001,
                              "use_all_genes": True, "x_dimension": 1000, "z_dimension": 50,
                              "alpha": 0.5, "dropout_rate": 0.2}},
    "evaluations": ["R2Evaluation", "MMDEvaluation"],
}


def write_cfg(name, cfg):
    p = work / f"{name}.yaml"
    p.write_text(yaml.safe_dump(cfg, sort_keys=False))
    return str(p)


def err(e):
    tb = traceback.extract_tb(e.__traceback__)
    frames = [f"{Path(f.filename).name}:{f.lineno} in {f.name}" for f in tb
              if "speciesot" in f.filename]
    return {"type": type(e).__name__, "message": str(e), "speciesot_frames": frames}


results = []


def stage(name, note, fn, stub=False):
    try:
        value = fn()
        results.append({"stage": name, "note": note, "ok": True, "value": value, "stub_scgen": stub})
    except Exception as e:  # noqa: BLE001 - recording is the point
        results.append({"stage": name, "note": note, "ok": False, "error": err(e), "stub_scgen": stub})


# 0. YAML facts
stage("yaml_none", "What does `IdentityModel: None` (Tests/config.yaml line 31) load as?",
      lambda: repr(yaml.safe_load("models:\n  IdentityModel: None\n  Other: null\n")["models"]))

# 1. An abstract class cannot be instantiated
stage("abstract", "AbstractModel() directly", lambda: repr(core.AbstractModel()))

# 2. toy_config.yaml as committed (paths swapped for toy files): no `experiment:` section
TOY = {"training_data": FULL["training_data"], "test_data": FULL["test_data"],
       "models": {"IdentityModel": "None",
                  "scGenModel": {"random_state": 0, "hidden_units": [256, 256], "lr": 0.001,
                                 "use_all_genes": True, "x_dimensions": 1000}},
       "evaluations": ["R2Evaluation", "MMDEvaluation"]}
stage("toy_config_setup", "Tests/toy_config.yaml shape -> Experiment.setup()",
      lambda: core.Experiment(write_cfg("toy_config", TOY)).setup(), stub=True)

# 3. toy_config with the experiment section added: scGenModel.__init__ looks for x_dimension
TOY2 = {"experiment": FULL["experiment"], **TOY}
stage("toy_config_plus_experiment", "toy_config + experiment section -> setup()",
      lambda: core.Experiment(write_cfg("toy_config2", TOY2)).setup(), stub=True)

# 4. config.yaml shape: __init__ succeeds; what does the dict look like after setup's edit?
def config_after_init():
    e = core.Experiment(write_cfg("config", FULL))
    try:
        e.setup()
    finally:
        snap = {k: v for k, v in e.experiment_spec["models"]["scGenModel"].items()}
    return snap
stage("config_setup", "Tests/config.yaml shape -> setup()", config_after_init, stub=True)

def config_dict_snapshot():
    e = core.Experiment(write_cfg("config_b", FULL))
    try:
        e.setup()
    except Exception:
        pass
    m = e.models[1] if len(e.models) > 1 else None
    return {"config_dict_after_setup": e.experiment_spec["models"]["scGenModel"],
            "x_dimension_attribute": getattr(m, "x_dimension", None),
            "has_x_dimensions_attribute": hasattr(m, "x_dimensions")}
stage("config_snapshot", "after the failed setup: the dict vs the object", config_dict_snapshot, stub=True)

# 5. Identity-only experiment, end to end
ID_ONLY = {**FULL, "models": {"IdentityModel": None}}
def identity_run():
    e = core.Experiment(write_cfg("identity", ID_ONLY))
    e.setup(); e.train(); e.predict()
    returned = e.evaluate()
    direct = {type(ev).__name__: ev.evaluate(e.predictions[0], e.test_data.target_adata)
              for ev in e.evaluations}
    return {"evaluate_returned": returned, "direct_scores": direct,
            "n_predictions": len(e.predictions)}
stage("identity_end_to_end", "IdentityModel only: setup/train/predict/evaluate", identity_run)

# 6. Identity-only, but the human test set has a different number of cells than the mouse one
UNEVEN = {**ID_ONLY, "test_data": {"source_test_data_path": paths["src_test"],
                                   "target_test_data_path": paths["tgt_test_uneven"]}}
def uneven_run():
    e = core.Experiment(write_cfg("uneven", UNEVEN))
    e.setup(); e.train(); e.predict()
    return {type(ev).__name__: ev.evaluate(e.predictions[0], e.test_data.target_adata)
            for ev in e.evaluations}
stage("r2_uneven_cells", "5 mouse test cells vs 7 human test cells", uneven_run)

def uneven_mmd():
    e = core.Experiment(write_cfg("uneven2", UNEVEN))
    e.setup(); e.predict()
    return core.MMDEvaluation().evaluate(e.predictions[0], e.test_data.target_adata)
stage("mmd_uneven_cells", "MMD alone with 5 vs 7 cells", uneven_mmd)

# 7. With scGen: pretend the setup attribute name is fixed, then train
def patched_setup(self):
    import scgen
    self.network = scgen.VAEArith(x_dimension=self.x_dimension, z_dimension=self.z_dimension,
                                  alpha=float(self.alpha), dropout_rate=float(self.dropout_rate),
                                  learning_rate=self.lr, model_path=self.model_path)

def with_scgen(step):
    original = core.scGenModel.setup
    core.scGenModel.setup = patched_setup
    try:
        e = core.Experiment(write_cfg("with_scgen", FULL))
        e.setup()
        if step == "setup":
            return {"x_dimension_passed": e.models[1].network.kwargs["x_dimension"]}
        if step == "train":
            e.train()
        if step == "predict":
            e.models[1].predict(e.test_data)
    finally:
        core.scGenModel.setup = original
stage("scgen_setup_patched", "setup() with self.x_dimension (one-word patch)", lambda: with_scgen("setup"), stub=True)
stage("scgen_train", "Experiment.train() with scGenModel present", lambda: with_scgen("train"), stub=True)
stage("scgen_predict", "scGenModel.predict(test_data)", lambda: with_scgen("predict"), stub=True)

# 8. scGenModel built straight from toy_config.yaml's model section (still spelled x_dimensions)
stage("toy_model_section", "scGenModel(toy_config['models']['scGenModel'] + model_path)",
      lambda: core.scGenModel({**TOY["models"]["scGenModel"], "model_path": "x"}))

# 9. Known answers for E3: MMD vs shift, R2 perfect vs shuffled (rng seed 1, 40 cells x 3 genes)
def known_answers():
    r = np.random.default_rng(1)
    base = r.normal(0, 1, size=(40, 3))
    mmd = core.MMDEvaluation()
    out = {"mmd_vs_shift": {}}
    for s in (0.0, 0.5, 1.0, 2.0):
        out["mmd_vs_shift"][str(s)] = round(float(mmd.evaluate(ad.AnnData(base.copy()), ad.AnnData(base + s))), 4)
    r2 = core.R2Evaluation()
    truth = ad.AnnData(base.copy())
    out["r2_perfect"] = r2.evaluate(ad.AnnData(base.copy()), truth)
    out["r2_shuffled_rows"] = round(r2.evaluate(ad.AnnData(base[r.permutation(40)]), truth), 4)
    x = np.array([[0., 0.], [1., 1.], [2., 2.]])
    out["josh_test_mmd_identical"] = core.MMDEvaluation(gamma=0.5).evaluate(ad.AnnData(x.copy()), ad.AnnData(x.copy()))
    return out
stage("known_answers", "MMD grows with shift; R2 of a perfect prediction", known_answers)

OUT.write_text(json.dumps({"package_dir": str(PKG_PARENT), "python": sys.version.split()[0],
                           "anndata": ad.__version__, "results": results}, indent=1, default=str))
for r in results:
    flag = "ok " if r["ok"] else "ERR"
    detail = r.get("value") if r["ok"] else f'{r["error"]["type"]}: {r["error"]["message"]}  @ {r["error"]["speciesot_frames"][-1:] }'
    print(f"[{flag}] {r['stage']:28s} {str(detail)[:160]}")
