# speciesOT, building the package — an explainer series

Five short narrated videos for **Conny**, who is turning eight months of speciesOT research
(notebooks, scripts, a `./hub` CLI) into an object-oriented Python package with Josh, and asked
for help "with no knowledge at all" of abstraction, Python packaging or testing. The series is
about *how to think and what to do next*, not a finished library: every exercise is left for
Conny to type.

## Conny's three questions, and where they are answered

| Question (from the request, 2026-10-14) | Answer, in one line | Episode |
| --- | --- | --- |
| **What next?** | Run the code, read the first thing that breaks, fix only that, lock it with a test. The measured error trail is already the ordered to-do list. | E5 (method), E2 + E3 (the skills it needs) |
| **Which notebooks / experiments to replicate first?** | Not a notebook: the first cut of the project's own frozen benchmark, **M1 v08 OOD** (`specs/m1_modern.yaml`). Golden numbers: identity R² of means **0.554**, scGen **0.927** (`speciesOT/baseline/analysis/v08_scorecard_dual.csv`). | E5 |
| **Do I need to trace back into scgen / cellot code?** | Only at the handful of calls your adapter makes. Three different things are called scgen (TF VAEArith clone, the scvi-tools package, cellot's autoencoder); your `scGenModel` wraps exactly one — the cellot autoencoder if the goal is the benchmark numbers. | E4 |

## Episodes (watch in order; ~4½–6 minutes each)

| # | Slug | Title | Teaches | Points at (Josh's `src/speciesot/`) |
| --- | --- | --- | --- | --- |
| E1 | `speciesot-e1-blueprint` | Four verbs and a contract | class vs object, `__init__`, `self`, abstract classes as contracts (names, not inputs), the Experiment as conductor, polymorphism | `speciesot_core.py` 35–57, 67–146, 151–159, 212–225 |
| E2 | `speciesot-e2-one-name` | One name, five places | config.yaml → dict → `__init__` → attribute; KeyError vs AttributeError; reading a traceback; the silent `x_dimension`/`x_dimensions` twin | `speciesot_core.py` 97–104, 214–225, 247–258; `Tests/config.yaml`, `Tests/toy_config.yaml`, `Tests/e24_replica.ipynb` |
| E3 | `speciesot-e3-tests` | A test is a question with a known answer | pytest discovery, known answers from meaning, toy data, test layers, the R² decision | `Tests/test_evaluation.py`, `Tests/test_model.py`, `speciesot_core.py` 305–335 |
| E4 | `speciesot-e4-scgen` | scGen as arithmetic, behind one adapter | encode → +δ → decode; setup/train/predict; the three scgens; adapter with a few calls | `speciesot_core.py` 212–294; speciesOT repo `atlas-paper-vae/scripts/`, `cellot/cellot_gpu/cellot/` |
| E5 | `speciesot-e5-next-step` | What next? Follow the errors | walking skeleton, the error trail as a board, the data card, M1 v08 and its golden numbers, SOLID as a compass | whole file; `specs/m1_modern.yaml`; `v08_scorecard_dual.csv` |

Each episode folder has `README.md` (a code companion: timestamp → file and line to open) and
`exercises.md` (hands-on tasks, hints only, no solutions).

## How we know things (provenance tags on screen)

| Tag | Meaning |
| --- | --- |
| `READ IN CODE` | read in Josh's attached `src/` (sha256 in `excerpts.py`) or in the speciesOT repo at `109bf12` |
| `READ IN NOTEBOOK` | a recorded output cell (e.g. `e24_replica.ipynb`, `e22_batch_correction.ipynb`) |
| `READ IN PACKAGE` | read inside a published package (`checks/scgen_package.txt`) |
| `MEASURED` | we ran it: Josh's package on toy data with a stand-in scgen (`checks/error_trail.py` → `error_trail.json`), pytest on his `Tests/` (`checks/pytest_run.txt`) |
| `INFERRED` | our reasoning or recommendation (the SOLID mapping, the card order, which scgen to wrap); it may be wrong, and the video says what would settle it |
| `EXAMPLE` | code we wrote to illustrate an idea; not from Josh or the repo |

Not run here: anything on the cluster (real atlas files, TensorFlow, the scvi-tools scgen,
model training). Cluster behaviour is marked INFERRED.

## Format

Swiss preset (`style.md` snapshot in each episode), 1920×1080 @ 30 fps, English narration
(Kokoro `af_heart`, 0.95×), Chinese above English captions burned in, composed score. Durations
are fitted per episode to the reviewed narration plus ~12% reading time for on-screen code
(the 300 s default is overridden in each `episode.json`).

## Production

```
videos/speciesot-series/   this plan, the shared kit (speciesot_kit.py), excerpts.py, SCENE_GUIDE.md, checks/
videos/speciesot-eN-*/      episode.json, script.json, storyboard.md, scenes.py, BRIEF.md, SOURCES.md, REVIEW.md,
                            README.md (code companion), exercises.md, delivery/ (captions + validation)
```

```bash
python3 skill-library/conny-explainer-video/scripts/render.py videos/speciesot-e1-blueprint --sample s02
python3 skill-library/conny-explainer-video/scripts/render.py videos/speciesot-e1-blueprint
# re-measure the evidence (needs anndata, scikit-learn, pyyaml; Josh's src/ unpacked somewhere):
python -I videos/speciesot-series/checks/error_trail.py <dir containing speciesot/> out.json
```

Regenerating `excerpts.py` after Josh's file changes: unpack the new `src/`, run
`python3 videos/speciesot-series/make_excerpts.py <path>/src/speciesot`, then re-check every line
number quoted in the five `script.json` files — the hashes in `SOURCE_SHA256` will differ.

## Publication

These episodes show unpublished code by Josh (excerpts) and Conny's research results. They are
made for Conny's personal study. Publishing them anywhere (Bilibili, a public release) is
Conny's decision and needs Josh's agreement first.
