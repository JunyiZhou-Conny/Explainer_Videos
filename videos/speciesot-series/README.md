# speciesOT, building the package

Five narrated Swiss-style videos for Conny, about turning the speciesOT research code into an
object-oriented Python package with Josh: how to read it, how config and `__init__` fit together,
how to test, how scGen plugs in, and what to do next. Plan, evidence rules and the answers to
Conny's three questions: [SERIES.md](SERIES.md). Shared visual kit: `speciesot_kit.py`; code
excerpts: `excerpts.py` (regenerate with `make_excerpts.py`); measurements: [checks/](checks/).

| Episode | What it teaches | Companion |
| --- | --- | --- |
| [E1 · Four verbs and a contract](../speciesot-e1-blueprint/) | classes, objects, `__init__`, `self`, abstract contracts, the Experiment as conductor | [code companion](../speciesot-e1-blueprint/README.md) · [exercises](../speciesot-e1-blueprint/exercises.md) |
| [E2 · One name, four places](../speciesot-e2-one-name/) | config.yaml → `__init__` → attribute; KeyError vs AttributeError; the silent twin | [code companion](../speciesot-e2-one-name/README.md) · [exercises](../speciesot-e2-one-name/exercises.md) |
| [E3 · A test is a question with a known answer](../speciesot-e3-tests/) | pytest, known answers, toy data, test layers, the R² decision | [code companion](../speciesot-e3-tests/README.md) · [exercises](../speciesot-e3-tests/exercises.md) |
| [E4 · scGen as arithmetic, behind one adapter](../speciesot-e4-scgen/) | encode → +δ → decode; the three scgens; the adapter | [code companion](../speciesot-e4-scgen/README.md) · [exercises](../speciesot-e4-scgen/exercises.md) |
| [E5 · What next? Follow the errors](../speciesot-e5-next-step/) | walking skeleton, error trail, M1 v08 golden numbers, SOLID as a compass | [code companion](../speciesot-e5-next-step/README.md) · [exercises](../speciesot-e5-next-step/exercises.md) |

Rendered MP4s are not in Git (release assets only, after review; see `docs/PUBLISHING.md`).
