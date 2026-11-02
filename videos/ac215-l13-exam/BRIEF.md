# Brief · AC215 L13 — Advanced Training Workflows (exam edition)

The design of this video, written before the script. Series rules: `docs/AC215_SERIES.md` (colours,
lecture tags, never-do list); scene-code rules: `.claude/skills/ac215-video/SKILL.md`. This is an
**exam edition**, not a follow-along: no README tracker, no `▶ your turn` tags, no captures. It
teaches the mechanisms Quiz 4 tests, each as an animated diagram, with code panels from the demo
repo as evidence.

Sources (read-only): the lecture digest `videos/ac215-l13-training-workflows/SLIDES.md` (slide
numbers = PDF pages of `L13_advanced_training_workflows`, 31 slides); the verified tutorial digest
`videos/ac215-l13-training-workflows/digest.md`; the study guide
`MLOps_Learning/guides/L13-training-workflows.md`; `dlops-io/model-training` at `b9aee1c`; the
course Colab "Experiment Tracking using Weights & Bias" (notebook B). Where the slides and the repo
disagree, the repo decides what the panel shows and the narration says so in one sentence
(SLIDES.md "Conflicts").

## Audience and goal

An AC215 student the day before Quiz 4. They sat Lecture 13 and have at least skimmed the
`model-training` README; they know Keras `model.fit`, what an epoch and a batch are, and what a
GCS bucket is (L10–L11). They have not necessarily run a Vertex AI job or used two GPUs.

After the video they can answer conceptual multiple-choice questions on this lecture **and say why
each wrong option is wrong**, specifically:

1. **W&B runs.** `wandb.init` opens a run and makes it the active run (`wandb.run`); a Keras
   callback (`WandbMetricsLogger`, legacy `WandbCallback`) writes one history entry per epoch to
   **whichever run is active when that epoch ends**; `wandb.finish` / `wandb.run.finish()` closes it.
   Two `fit` calls with no finish in between extend the same run's history; a fresh `init` after a
   finish starts a new run whose history starts empty; a callback with no active run is an error.
   Without a callback (or `wandb.log`), a run has config and system charts but no loss curve.
2. **Packaging for a Vertex AI custom job.** Vertex installs the uploaded source distribution with
   pip and runs `python -m trainer.task`. `install_requires` brings third-party dependencies from
   PyPI; your own team modules arrive **only** if `setup.py` packages them (`find_packages()` finds
   folders with `__init__.py`). A module left out gives `ModuleNotFoundError` even though every pip
   dependency installed.
3. **tf.distribute.** `MirroredStrategy` keeps one replica per GPU of **one machine** in sync
   (all-reduce every step). `MultiWorkerMirroredStrategy` does the same across machines, which find
   each other through `TF_CONFIG`. Two machines each running their own `MirroredStrategy` on
   different shards train two independent models whose weights differ.
4. **Global vs per-replica batch.** Under a strategy, `dataset.batch(n)` makes the **global** batch,
   split across `strategy.num_replicas_in_sync` replicas; per-replica = global / replicas; 64 per
   replica on 4 replicas means `batch(256)`.
5. **Durable jobs.** Training that outlives a request goes to a durable job service (a Vertex AI
   custom job): submit, get a job id back, poll its state. Not inside the request handler, not in a
   background thread of the server, not by raising client timeouts. Experiment trackers record runs;
   they do not execute them.
6. **One beat:** a data version links the archived dataset snapshot to the version record that
   names it (slide 10's "data → DVC, GCS buckets").

## Length

12–15 minutes. One part (no `parts:` key in `video.yaml`). Narration **1,800–2,300 words**, target
**2,100** (the voice runs about 150 wpm in this series by the coordinator's measure, ~174 by the
skill's; 2,100 words is 12–14 min either way, plus three ponder timers of ~10 s). Budgets per scene
below are targets (±15 %).

## Colours (series table, applied to this lecture)

| meaning | colour |
| --- | --- |
| your laptop and the Colab notebook tab; finished (closed) W&B runs once sealed | GREY |
| the cloud: Vertex AI, the custom job's VM, the GCS bucket, the job machine's GPUs, wandb.ai and its run rows | BLUE |
| containers and images: the `model-training-cli` container on the laptop, Google's prebuilt training image `tf-cpu.2-17.py310` / `tf-gpu.2-14.py310` (the box) | TEAL |
| what the prebuilt image already ships (TensorFlow, scikit-learn, requests): shared, not declared by you | ORANGE |
| what you own: the `package/` folder, `trainer/` and its modules, `setup.py`, the tarball's contents; model replicas' weights (one shade = in sync); history entries (epoch ticks) | GREEN |
| tools and libraries: the `wandb` SDK and its callback (the "pen"), `gcloud`, pip, `tf.distribute` strategies, the `wandb==0.15.11` pin chip | PURPLE |
| errors and "avoid this": `ModuleNotFoundError`, `wandb.Error`, a killed request, diverged weights, an empty loss strip, wrong option in a ponder | RED |
| the active run (outline), "look here now", the ponder card and its timer, the right option | YELLOW |
| money: per-minute VM and GPU billing on the job | GOLD |
| routes and lookups: the `wandb.run` pointer, all-reduce wires, the `TF_CONFIG` cable between machines, the batch-split arrows, `gs://` URIs, the `sys.path` search | PINK |
| lecture-only or hypothetical: One Device / Multi Worker strategies not used by the repo, an example team module that is not in the repo (also tagged `illustration`) | GREY dashed |

## Visual set pieces (mechanisms, not cards)

- **V1 · The run ledger (S01–S03).** wandb.ai drawn as a ledger of BLUE run rows (schematic, tagged
  `illustration`, project `cheese-training-vertex-ai`, no logo). `wandb.init(...)` slides a new row
  in; its outline turns YELLOW and a PINK pointer labelled `wandb.run` swings onto it. The `config`
  chips from `task.py:313-322` clip onto the row (`learning_rate`, `epochs`, `batch_size`,
  `model_name`); a small system-chart tile starts wiggling. Each row has a **history strip**: during
  `model.fit` a PURPLE pen (the callback) rides the pointer and drops one GREEN tick per epoch at
  the end of each epoch bar. `wandb.run.finish()` seals the row (padlock, outline to GREY) and the
  pointer falls to a `None` slot. Variants played in S03: (a) no pen → the strip stays empty (the
  hook's broken run); (b) `fit` 3 epochs, `fit` 2 more, no finish → ticks 4–5 land on the same row
  (5 ticks, one run); (c) finish, then `init` again → a second row, its strip starts at tick 1;
  (d) finish, then `fit` with the old pen → the pen follows the pointer to `None` and stops with a
  RED `wandb.Error: You must call wandb.init() before wandb.log()`. Creating `WandbMetricsLogger()`
  with no active run raises at once ("You must call `wandb.init()` before WandbMetricsLogger()").
- **V2 · What pip unwraps (S04).** The `package/` tree from the repo (`setup.py`, `setup.cfg`,
  `PKG-INFO`, `trainer/__init__.py`, `task.py`, `task_multi_gpu.py`). `find_packages()` is a PINK
  scanner that lights only folders holding an `__init__.py`: `trainer/` turns GREEN.
  `install_requires` is a separate shopping list with one PURPLE chip `wandb==0.15.11`. The
  tarball (`package-trainer.sh:1-4`) flies into the BLUE bucket, then onto the job VM inside the
  TEAL prebuilt image, whose ORANGE shelf already holds TensorFlow, scikit-learn, requests. pip
  unwraps: the shopping list fetches wandb from PyPI (✓), `trainer` is installed (✓). Then the
  failure: an example team module (`augment.py`, GREY dashed, `illustration`: not in the repo)
  sat outside `trainer/` (a sibling of `package/`, or a folder with no `__init__.py`), so it never
  entered the installed package; `python -m trainer.task` runs `import augment`, the PINK
  `sys.path` search scans the shelves and finds nothing → RED `ModuleNotFoundError: No module
  named 'augment'` directly under the green "Successfully installed …" line. The fix animates: the
  module slides into `trainer/` (or gets its own `__init__.py`), the scanner lights it, rerun ✓.
- **V3 · Mirrors vs islands (S05).** One BLUE machine (`n1-standard-32`, two T4s as in
  `cli-multi-gpu.sh:6-12`), a GREEN model replica on each GPU. One step: each GPU takes its slice,
  grows a gradient arrow; the two arrows meet in a PINK all-reduce ring, average, split back, both
  replicas change to the same new shade. Then two machines, each with its own `MirroredStrategy`
  and its own shard: inside each machine the ring works, between the machines there is no wire;
  after a few steps the two machines' replicas drift into visibly different shades (RED Δ between
  them): two models, not one. Then `MultiWorkerMirroredStrategy`: a `TF_CONFIG` card appears on each
  machine (`cluster` list of workers + this machine's `task` index, schematic values), a PINK cable
  joins the machines, the ring spans all four GPUs, one shade everywhere. Above it, slide 27's
  three-row ladder (One Device / Mirrored / Multi Worker Mirrored) with "the repo is here" on row 2.
- **V4 · The batch splitter (S06).** `dataset.batch(n)` makes a tray of n images; the strategy's
  splitter (PINK arrows) cuts the tray into `num_replicas_in_sync` equal slices, one per GPU. A
  counter shows `global = per-replica × replicas`. Dial play with 4 replicas: `batch(64)` → 16 each
  (RED against an intended 64); `batch(256)` → 64 each (GREEN). Then the repo's line
  `global_batch_size = args.batch_size * num_workers` (`task_multi_gpu.py:291-301`) lights up as
  the same arithmetic, with the slide-29 caption *Adjust dataset batch size*.
- **V5 · Request clock vs job ticket (S07).** A web request handler (schematic `POST /retrain`,
  tagged `illustration`) with a timeout ring around it. Three wrong designs play fast: (1) `fit`
  inside the handler, the training bar outgrows the ring, the connection is cut, the bar dies RED;
  (2) a background thread inside the server, the server instance is recycled, the thread vanishes
  with it; (3) the client's timeout ring is stretched, but the server and proxy still cut it, and a
  laptop lid closing kills the waiting client. A fourth "design" shows the W&B ledger: it records,
  it has no engine. The right design: the handler drops a ticket to Vertex AI (BLUE) and returns a
  job id at once; the job's state machine `QUEUED → PENDING → RUNNING → SUCCEEDED` (digest §3.4)
  runs on its own VM with a GOLD per-minute meter; the laptop closes; the job keeps going; anyone
  polls the id. Then `cli.sh:30-37` (`gcloud ai custom-jobs create …`) as the repo's ticket.

## Scene plan (final: file, class, title in `video.yaml`)

Every scene stands on lecture ground (grey `lecture_ref(13, "a–b")` top right), quotes code only
from `assets/source/` with real line numbers, and ends on an empty frame after a YELLOW takeaway
line **"If the question says X, think Y."**

| # | file · class | title | words | slides | repo / notebook evidence (file:lines) |
| --- | --- | --- | --- | --- | --- |
| S01 | `s01_hook.py` · `Hook` | The run with no curves | 200 | 6, 8, 15–16 | `model-training/package/trainer/task.py:324-331` (the `fit` call: no `callbacks=`) |
| S02 | `s02_record.py` · `RunRecord` | What a run records | 280 | 9–13, 15 | `task.py:152-153` (login), `task.py:312-322` (init + config), `task.py:335-338` (config update, finish); `task.py:95-100` (data pinned by a release URL) |
| S03 | `s03_callback.py` · `ActiveRun` | The callback writes to the active run | 320 | 15–16 | `colab/L13_wandb_tracking/cell-38.py:41-61` (init, then `fit(..., callbacks=[WandbCallback(...)])`); `task.py:21-22` (imported, unused) |
| S04 | `s04_package.py` · `WhatPipInstalls` | What the package carries | 320 | 23–25 | `model-training/package/setup.py:1-13`; `package/trainer/__init__.py` (empty, shown in the tree); `model-training/package-trainer.sh:1-4`; `model-training/cli.sh:10-11` (package URI, `trainer.task`) |
| S05 | `s05_mirror.py` · `MirrorsAndIslands` | One machine or many | 300 | 26–27, 29–30 | `package/trainer/task_multi_gpu.py:286-289` (strategy, replicas), `:303-321` (scope); `model-training/cli-multi-gpu.sh:6-12` (one `n1-standard-32`, 2 × T4) |
| S06 | `s06_batch.py` · `GlobalBatch` | Global batch, per-replica batch | 230 | 28–29 | `task_multi_gpu.py:291-301`; `task_multi_gpu.py:198` (`train_data.batch(batch_size)`) |
| S07 | `s07_jobs.py` · `DurableJob` | Training that outlives the request | 270 | 22, 24–25 | `model-training/cli.sh:5-14` (worker-pool settings), `cli.sh:30-37` (`gcloud ai custom-jobs create`) |
| S08 | `s08_recap.py` · `Recap` | Six rules for Tuesday | 180 | 5, 10, 15, 24, 27, 29 | none (recap) |
| | | **total** | **2,100** | | |

**S01 · The run with no curves (~200).** Cold open on V1's broken state: a W&B run row
(`illustration`, project `cheese-training-vertex-ai`, run `mobilenetv2_train_base_True`) with its
config chips and wiggling system charts, but the loss and accuracy panels are empty outlines. "The
job succeeded. The run exists. Where are the curves?" The `fit` call from `task.py:324-331`
slides in beside it; leave the answer hanging ("hold that thought: scene three"). One sentence on
slide 6: tracking is set up with the baseline models, this lecture's boxed work. Then the map of
the video: five small mechanisms laid out as the places a training workflow quietly breaks (the run
ledger, the package, the GPUs, the batch, the job), each a miniature of V1–V5. Say: it is an exam
edition, each scene ends with "if the question says X, think Y", and there are three quiz-style
pauses.

**S02 · What a run records (~280).** Slide 9's seven items (environment, code, data, model,
metrics, artifacts, notes) as columns; slide 10's "where do we track what" rows snap into homes
(GitHub, data versioning, `pyproject.toml`/`uv.lock`), the last row "weights, metrics, logs" hangs
on "?" until the ledger catches it. V1 lifecycle with `task.py`: `wandb.login` (152-153; the key is
a GOLD key glyph, never a value), `wandb.init(project=..., config=..., name=...)` (312-322) opens
the row and moves `wandb.run`; `wandb.config.update` (335-336) adds `execution_time`;
`wandb.run.finish()` (337-338) seals it. Point: `init` records config and system metrics; it does
not record loss by itself. **Data-version aside (one beat, ~40 words):** the "data" column's home
is a pair: the archived snapshot (a bucket object) and the version record that names it (a DVC
file / tag in git), linked by a content hash; this trainer instead pins data by a release URL,
`cheese_4_labels.zip` v4.0 (`task.py:95-100`), and does not write it into `config`.
Takeaway: "If the question says *record of a run*, think: init opens it, config describes it,
something must log the metrics, finish closes it." **PONDER 1** at the end (see below).

**S03 · The callback writes to the active run (~320).** Answer PONDER 1 first (each wrong option
why). Notebook B's `cell-38.py:41-61`: `init`, then `fit(..., callbacks=[WandbCallback(save_graph=
False, save_model=False)])`. Mechanism: the callback is a pen that, at the end of every epoch,
calls `wandb.log` — the module-level call, which goes to `wandb.run`, i.e. **the active run, not
the run the callback was "born" with**. One history entry per epoch by default (`log_freq="epoch"`
in `WandbMetricsLogger`; per-batch only if you ask). V1 variants (a)–(d) in that order, each with a
tick counter. Answer the hook: the repo's trainer imports both callbacks (`task.py:21-22`) but
passes none to `fit` (`324-331`), so its run has config and system charts, no curves (SLIDES.md
Conflict 1); slide 15's `callbacks=[WandbCallback()]` is the line that's missing; `WandbCallback`
is deprecated in favour of `WandbMetricsLogger` (the notebook's own warning). Takeaway: "If the
question counts history entries, think: one per epoch, into whichever run is open when the epoch
ends; a finish ends the count; a new init starts a new one."

**S04 · What the package carries (~320).** Slides 23–24: notebook → Python file with arguments →
packaged files → bucket → job. V2 in full with `setup.py:1-13`, `package-trainer.sh:1-4` (tar of
the `package` folder, gzip, `gsutil cp` to `cheese-app-trainer.tar.gz`) and `cli.sh:10-11`
(`PYTHON_PACKAGE_URI`, `PYTHON_MODULE="trainer.task"`). Your Docker image only submits; the job
runs in Google's prebuilt image, and your code reaches it only through the tarball (digest §3.3).
The two lists: `install_requires` = what pip downloads from PyPI; `packages=find_packages()` = which
of your folders get installed. The prebuilt image's ORANGE shelf explains why `sklearn` and
`requests` work although `setup.py` never names them (digest E8/E12) — luck, not declaration.
The failure and the fix (example module, tagged `illustration`). Takeaway: "If the question says
*dependencies installed but ModuleNotFoundError*, think: your own module isn't inside the package
that setup.py builds — move it into `trainer/` or list it; adding it to install_requires is wrong,
it isn't on PyPI."

**S05 · One machine or many (~300).** Slide 27's ladder (One Device / Mirrored / Multi Worker
Mirrored), "the repo is here" on Mirrored. V3: one machine, two T4s (`cli-multi-gpu.sh:6-12`),
`MirroredStrategy()` and `num_replicas_in_sync` (`task_multi_gpu.py:286-289`), model and optimizer
built and compiled inside `strategy.scope()` (`303-321`) so the variables are mirrored. The
all-reduce step. Then the islands: two machines, each its own `MirroredStrategy`, different shards
→ different weights. Then `MultiWorkerMirroredStrategy` + `TF_CONFIG` (schematic, GREY dashed:
lecture-only, not in the repo; on Vertex, extra machines go in a second worker pool and Vertex sets
`TF_CONFIG`, digest §3.7). Note the naming trap: the slide's and repo's `num_workers` counts GPU
replicas on one machine, while the "worker" in Multi Worker is a machine. Takeaway: "If the
question says *several machines must train one model*, think MultiWorkerMirroredStrategy with
TF_CONFIG; a MirroredStrategy never looks past its own machine."

**S06 · Global batch, per-replica batch (~230).** V4. `dataset.batch(n)` under a strategy is the
global batch; per-replica = global / `num_replicas_in_sync`. The repo's three lines
(`task_multi_gpu.py:291-301`, comment "`tf.data.Dataset.batch` expects the global batch size") and
slide 29's call-out. Side note: the repo keeps learning rate 0.001 while the effective batch grows
(digest §3.7) — said once, not tested. **PONDER 2** (below). Takeaway: "If the question says *per
replica*, multiply before you batch: global = per-replica × replicas."

**S07 · Training that outlives the request (~270).** Slide 22 (serverless: GPU only for the
training step, no server to manage) and slide 24 (CLI container → bucket → jobs). V5's three wrong
designs and the tracker non-design, each struck RED with its reason; then the job ticket, its
states, the GOLD meter, the laptop closing. `cli.sh:5-14` (worker pool: machine type, replica
count, image, package, module) and `cli.sh:30-37` (the submission). "Serverless" still means a VM;
you just don't own its lifetime. **PONDER 3** (below). Takeaway: "If the question says *training
takes longer than the request*, think: submit a durable job, return its id, poll; W&B only watches."

**S08 · Six rules for Tuesday (~180).** The five miniatures from S01 return and each turns into a
one-line rule (on screen, ≤ 3 visual groups at a time, two rules per frame):
1. A callback logs one entry per epoch into the active run; `init` opens, `finish` closes.
2. pip installs what `setup.py` packages: dependencies from `install_requires`, your modules only
   inside a found package.
3. `MirroredStrategy` = the GPUs of one machine; across machines = `MultiWorkerMirroredStrategy` +
   `TF_CONFIG`; separate strategies = separate models.
4. `dataset.batch(n)` is the global batch; per-replica = n / `num_replicas_in_sync`.
5. Long training → a durable job with an id; never a request handler, a thread or a longer timeout.
6. A data version = an archived snapshot + the record that points at it.
Close on slide 5's three levers with "faster hardware" lit (this lecture), then empty frame.

## Ponder beats (new questions; never the practice questions)

Format: a YELLOW card with the question and four options A–D on screen, a ~10 s timer (silent
apart from "pause here if you want"), then the right option turns YELLOW and each wrong option gets
a one-line RED reason, spoken. None of these restates or answers practice Q1–Q5 or Q8.

- **P1 (end of S02, answered at the start of S03).** "Your script calls `wandb.init(config=...)`,
  trains with `model.fit`, then calls `wandb.finish()`. The run page shows the config but no loss
  curve. Which change puts a loss curve on that run?" A) pass `name=` to `wandb.init` · B) call
  `wandb.config.update({"loss": ...})` after training · C) pass `WandbMetricsLogger()` in `fit`'s
  `callbacks`, created after `init` · D) call `wandb.login()` again before `fit`. Answer **C**. A
  names the row, logs nothing; B puts one number in config, not a history over epochs; D
  authenticates, logs nothing.
- **P2 (S06).** "A script trained on one GPU with `dataset.batch(32)`. You wrap the model in a
  `MirroredStrategy` on a machine with 4 GPUs and change nothing else. How many examples does each
  GPU see per step?" A) 32 · B) 128 · C) 8 · D) it raises an error. Answer **C**. A and B confuse
  the global batch with the per-replica batch; D: nothing forbids it, the global batch 32 is
  simply split four ways (to keep 32 per GPU, batch by 128).
- **P3 (S07).** "You submitted a Vertex AI custom job from your laptop; it shows RUNNING. You close
  the laptop and go to bed. What happens to the training?" A) it stops, because the CLI container
  that submitted it exits · B) it keeps running on the job's own VM until it finishes or fails ·
  C) it pauses until W&B reconnects · D) it restarts from epoch 1 when you reopen the laptop.
  Answer **B**. A: the CLI container only submits, the job runs on Google's VM; C: W&B records, it
  doesn't drive training; D: nothing on your laptop holds the job's state.

## Things to say carefully (verified, keep exact)

- W&B behaviour is stated for `wandb==0.15.11` (the version `setup.py:5` pins), checked by
  reading its source, not by running it: `WandbMetricsLogger.__init__` raises if `wandb.run is
  None`; its `on_epoch_end` calls module-level `wandb.log`; after `finish`, `wandb.log` raises
  "You must call wandb.init() before wandb.log()". A second `wandb.init` while a run is open
  **depends on context** in that version (a script gets the same run back; a notebook finishes the
  old run first; newer versions add a `reinit` setting). The video does **not** build a claim on a
  double `init`; its rule is "finish explicitly".
- The repo trainers pass no callback (`task.py:324-331`, `task_multi_gpu.py:338-343`); notebook B
  passes `WandbCallback` in one cell only and never calls `wandb.finish()` (digest §4 Part A).
- `find_packages()` finds `trainer` because `trainer/__init__.py` exists; the tarball holds the
  whole `package/` folder, but pip installs only what `setup.py` declares, so "uploaded" is not
  "installed". The `augment` module is a made-up example, always tagged `illustration`.
- `num_workers` in slide 29 and `task_multi_gpu.py:289` counts replicas (GPUs) on one machine.
- `MultiWorkerMirroredStrategy`, `TF_CONFIG` and One Device Strategy are lecture/TF concepts the
  repo does not use: GREY dashed, schematic values only.
- The `POST /retrain` handler is a schematic example, not course code.

## Never

No slide images; no W&B, Google or Vertex logos or console screenshots (schematic drawings tagged
`illustration`); no real person's name; no API key, project id or bucket name that looks real (the
W&B key is a GOLD glyph; the bucket is `$GCS_BUCKET_URI` as the script writes it); no practice
question quoted, paraphrased into a ponder, or answered by letter; no README walk-through and no
terminal capture; no code panel that is not a file in `assets/source/` at its real line numbers.

## Assets

`assets/source/` holds the quoted files unchanged: `model-training/` copied from
`dlops-io/model-training` at `b9aee1cc1923dd1f673093ad3ff5bb023049b4ff` (`package/setup.py`,
`package/trainer/__init__.py`, `package/trainer/task.py`, `package/trainer/task_multi_gpu.py`,
`package-trainer.sh`, `cli.sh`, `cli-multi-gpu.sh`); `colab/L13_wandb_tracking/cell-38.py` is the
source of code cell 38 of the course notebook "Experiment Tracking using Weights & Bias", extracted
verbatim from the notebook JSON (a notebook has no commit; line numbers are the cell's own).
