# AC215 · Lecture 13 — Advanced Training Workflows (exam edition) — narration script & visual plan (v1)

Audience: an AC215 student the day before Quiz 4. They sat Lecture 13 and have at least skimmed the `model-training`
README; they know Keras `model.fit`, what an epoch and a batch are, and what a GCS bucket is (L10–L11). They have not
necessarily run a Vertex AI job or trained on two GPUs. They watch to prepare for conceptual multiple-choice
questions, not to type along.

Goal (BRIEF.md "Audience and goal"): after the video they can answer conceptual questions on this lecture **and say
why each wrong option is wrong**: (1) W&B runs: `wandb.init` opens a run and makes it the active run (`wandb.run`); a
Keras callback writes one history entry per epoch into whichever run is active when that epoch ends; `finish` closes
it; two `fit` calls with no finish extend one run; a new `init` after a finish starts an empty history; a callback
with no active run is an error; without a callback a run has config and system charts but no loss curve. (2)
Packaging for a Vertex AI custom job: `install_requires` brings PyPI dependencies, your own modules arrive only inside
a package that `setup.py` finds; a module left out gives `ModuleNotFoundError` although every dependency installed.
(3) `MirroredStrategy` = the GPUs of one machine; `MultiWorkerMirroredStrategy` + `TF_CONFIG` = across machines;
separate strategies on separate shards = separate models. (4) `dataset.batch(n)` under a strategy is the global
batch; per-replica = n / `num_replicas_in_sync`. (5) Long training goes to a durable job (submit, id, poll), never a
request handler, a server thread or a longer timeout; trackers record, they do not execute. (6) One beat: a data
version = an archived snapshot + the version record that names it.

Sources of truth: `BRIEF.md` (design, binding); the lecture digest `videos/ac215-l13-training-workflows/SLIDES.md`
(slide numbers = PDF pages of the 31-slide deck); the verified tutorial digest
`videos/ac215-l13-training-workflows/digest.md`; the study guide `MLOps_Learning/guides/L13-training-workflows.md`;
`assets/source/` (`dlops-io/model-training` at `b9aee1c`, unchanged, and cell 38 of the course notebook "Experiment
Tracking using Weights & Bias"). Where the slides and the repo differ, the panel shows the repo and the SAY says what
each shows, in one sentence (SLIDES.md "Conflicts" 1, 9; the `num_workers` naming). W&B behaviour is stated for
`wandb==0.15.11` (`setup.py:5`) as BRIEF.md "Things to say carefully" records it; no claim rests on a double `init`.

Conventions
- **Exam edition.** No README tracker, no `▶ your turn`, no terminal captures, no live runs: this lecture's video has
  nothing typed and nothing run. Every mechanism is an animated diagram (V1–V5, BRIEF.md "Visual set pieces"); code
  panels are evidence beside it. Every scene ends with a YELLOW takeaway line **"If the question says X, think Y."**
  (one visual group, centred), spoken as the scene's last SAY or the one before its ponder answer, then an empty frame.
- `SAY:` lines are spoken verbatim by the TTS voice (one `voiceover` block each, 1–3 sentences, at most about 55
  words; ponder answers may run a little longer) and become the subtitles. Plain spoken English: no backticks, no
  symbols, no markdown. Identifiers are on screen and said in words: "wandb dot init", "wandb dot run dot finish",
  "the Wandb Metrics Logger", "the Wandb Callback", "setup dot py", "task dot py", "install requires", "find
  packages", "python dash m trainer dot task", "Module Not Found Error", "Mirrored Strategy", "Multi Worker Mirrored
  Strategy", "TF config", "num replicas in sync", "num workers", "strategy dot scope", "dataset dot batch",
  "gcloud A I custom jobs create". "Weights and Biases" in full the first time, then "W and B". Numbers as digits; a
  number that matters gets its own short sentence ("Batch by 256. Each GPU gets 64."). No decimals spoken (versions
  and the learning rate stay on screen). No "!" after a digit.
- Every spoken sentence starts with a capital letter or a digit (`explainer.voice.split_sentences` splits only there;
  the split drives the TTS gaps, the subtitle cues and the one-to-one Chinese alignment). No sentence opens with an
  identifier in lower case: "The call wandb dot init …", never "wandb dot init …". No `'s` after a digit or on a
  word with a lexicon entry; no article "a" right before a lexicon word.
- **Names.** The instructor's full name never appears, on screen or in the SAY; this script says "the lecture" and
  "the lecture's notebook". The quoted files contain no person's name (checked: `task.py`, `task_multi_gpu.py`,
  `setup.py`, `package-trainer.sh`, `cli.sh`, `cli-multi-gpu.sh`, `cell-38.py`). The W&B key is a GOLD key glyph,
  never a value; the bucket is `$GCS_BUCKET_URI` exactly as the scripts write it; no project id, entity or job id
  that looks real (a job id on screen is the schematic `‹job-id›`).
- `SHOW:` lines describe what is on screen during that SAY, and what moves. ≤ 3 visual groups at once; something
  moves every ~4 s except during ponder timers.
- `Lecture: a–b.` under a scene header lists the slides the scene stands on. `LECTURE a–b` in a SHOW line: from that
  SAY block on, the GRAY `lecture_ref(13, "a–b")` tag sits top right ("Lecture 13 · slides a–b") until a SHOW changes
  it. S01 explains the tag once. The slides are never shown: every lecture picture is our own redrawing in the series
  colours, with the slide's structure and terms (no screenshot of slides 16, 20, 21; no cat from slide 31).
- `CODE(path: a–b)`: `code_panel(...)` quoting `assets/source/path` from line a to b, header `path · lines a–b`
  (paths below are relative to `assets/source/`; the header drops the leading `model-training/`, e.g.
  `package/trainer/task.py · lines 312–322`). At most 12 rows; a longer range is *folded* (only the listed lines, a
  GRAY `…` row between gaps, header suffix `(folded)`). Lines longer than 65 characters wrap (continuation rows
  indented, a GRAY ↪). An *excerpt chip* quotes an exact sub-string of one line, headed `path · line N (excerpt)`.
  `colab/L13_wandb_tracking/cell-38.py` is headed `Experiment Tracking notebook · training cell · lines a–b` (a
  notebook has no commit; the numbers are the cell's own; the SAY says "the lecture's notebook").
- `PONDER(10 s, "question")` + options: after that SAY block, a YELLOW card (lower two thirds) with the question and
  four options A–D, and a silent ~10 s timer (`pause_and_ponder`); nothing on screen during the timer shows the
  answer. The SAY that introduces it ends "Pause here if you want." The answer block redraws the same card: the right
  option turns YELLOW, each wrong option gets a one-line RED reason as the SAY names it. Three ponders (S02 → answered
  at the start of S03; S06; S07). None restates or answers a practice question (BRIEF.md "Never").
- Tags (GRAY unless stated): `illustration` on every schematic (the W&B ledger, the request handler `POST /retrain`,
  the job state machine, the job VM, the prebuilt image's shelf, the `TF_CONFIG` card, the example module
  `augment.py`); `concept · lecture only` (GRAY dashed) on One Device and Multi Worker Mirrored Strategy and
  `TF_CONFIG`, which the repo does not use; `example · not in the repo` on `augment.py`; `wandb 0.15.11` (PURPLE chip)
  next to every quoted W&B error message.
- Semantic colours (BRIEF.md "Colours"; series table applied):

  | meaning | colour |
  | --- | --- |
  | your laptop, the notebook tab; finished (sealed) W&B runs | GREY |
  | the cloud: Vertex AI, the job VM, the bucket, the job machine's GPUs, wandb.ai and its run rows | BLUE |
  | containers and images: `model-training-cli`, the prebuilt `tf-cpu.2-17.py310` / `tf-gpu.2-14.py310` box | TEAL |
  | what the prebuilt image already ships (TensorFlow, scikit-learn, requests) | ORANGE |
  | what you own: `package/`, `trainer/` and its modules, `setup.py`, the tarball's contents; replica weights (one shade = in sync); history ticks | GREEN |
  | tools and libraries: the `wandb` SDK and its callback (the pen), `gcloud`, pip, `tf.distribute` strategies, the `wandb==0.15.11` chip | PURPLE |
  | errors and "avoid this": `ModuleNotFoundError`, `wandb.Error`, a cut request, diverged weights (Δ), the empty loss strip, wrong options | RED |
  | the active run's outline, "look here now", the ponder card and timer, the right option, takeaway lines | YELLOW |
  | money: the per-minute meter on the job | GOLD |
  | routes and lookups: the `wandb.run` pointer, all-reduce wires, the `TF_CONFIG` cable, batch-split arrows, `gs://` paths, the import-path search | PINK |
  | lecture-only or hypothetical: One Device / Multi Worker strategies, the example module | GREY dashed |

- Visual set pieces (BRIEF.md): **V1 the run ledger** (S01–S03, miniature in S08), **V2 what pip unwraps** (S04),
  **V3 mirrors vs islands** (S05), **V4 the batch splitter** (S06), **V5 request clock vs job ticket** (S07). S01
  shows each as a miniature; S08 brings the miniatures back.
- Running example: W&B project `cheese-training-vertex-ai`, run `mobilenetv2_train_base_True` (`task.py:263` builds
  the name `model_name + "_train_base_" + str(train_base)`; `cli.sh:19` passes `--model_name=mobilenetv2,--train_base`);
  config chips `learning_rate`, `epochs`, `batch_size`, `model_name` (`task.py:315-320`), later `execution_time`
  (`task.py:336`).

- Notes for scene authors.
  - Line numbers are file lines of `assets/source/` (`excerpt(file, a, b)`); `task.py:324-331` is the `fit` call
    with no `callbacks=`; the run is opened at `313-322` (the comment on 312).
  - `cli.sh` sets the GPU image on line 9, then line 31 overrides it with `tf-cpu.2-17.py310` before the only
    uncommented submission (32–37); lines 12–13 (accelerator) are used only by the commented-out GPU block (22–27).
    Any panel showing 5–14 dims 12–13 with a GRAY note "used by the GPU block · commented out" (SLIDES.md Conflict 4).
  - `cli-multi-gpu.sh:7` `REPLICA_COUNT=1` counts machines (Vertex worker-pool replicas); `task_multi_gpu.py:289`
    `num_workers` counts GPU replicas on that one machine. S05 puts the two side by side; never call both "workers"
    without the qualifier.
  - The V1 variants in S03 run in order (a) no pen, (b) two fits / no finish, (c) finish then init, (d) finish then
    fit. Tick counters are integers drawn as ticks; the error strings are the ones BRIEF.md "Things to say carefully"
    records for 0.15.11 ("You must call wandb.init() before wandb.log()"; "You must call wandb.init() before
    WandbMetricsLogger()"), each with the PURPLE `wandb 0.15.11` chip. Variant (b): the second `fit` restarts Keras'
    own epoch counter, the ledger keeps counting ticks (4, 5): draw ticks, not epoch labels.
  - The S04 fix changes the import: `from trainer import augment` (with `python -m trainer.task` the import path
    starts at the working directory, not inside `trainer/`, so a bare `import augment` would still fail after the
    move). The alternative fix is `py_modules=["augment"]` in `setup.py` (drawn as a GREEN chip on the `setup(...)`
    call, schematic, `illustration`). Never edit the real `setup.py` panel: the fix is a separate schematic card.
  - Numbers: V4 dial 4 replicas: `batch(64)` → 16 each (RED vs intended 64), `batch(256)` → 64 each (GREEN). PONDER 2:
    `batch(32)` on 4 GPUs → 8 each; keep 32 each → `batch(128)`. Repo: `--batch_size=32` (`cli-multi-gpu.sh:16`) × 2
    replicas = 64 global.
  - Lexicon candidates (merge step, block `# AC215 L13` in `explainer/lexicon.yaml`; check phonemes with
    `explainer/voice.py`): wandb ("wand-B"), Wandb (in "Wandb Callback", "Wandb Metrics Logger"), gcloud, scikit-learn,
    TensorFlow, Keras, n1 (in "n1 standard 32"), tarball, all-reduce, TF config, num, init (as a noun: "the init"),
    "dataset dot batch" (Kokoro flaps "dataset": L08 note; prefer a phrase entry), augment dot py, setup dot py,
    task dot py, "dash m". Checked in L08, no entry: T4, GPU, Colab (has one).
  - i18n `en_display` candidates (spoken → literal): wandb dot init → `wandb.init`; wandb dot run → `wandb.run`;
    wandb dot run dot finish → `wandb.run.finish()`; wandb dot log → `wandb.log`; Wandb Metrics Logger →
    `WandbMetricsLogger`; Wandb Callback → `WandbCallback`; setup dot py → `setup.py`; task dot py → `task.py`;
    augment dot py → `augment.py`; install requires → `install_requires`; find packages → `find_packages()`; python
    dash m trainer dot task → `python -m trainer.task`; from trainer import augment; Module Not Found Error →
    `ModuleNotFoundError`; Mirrored Strategy → `MirroredStrategy`; Multi Worker Mirrored Strategy →
    `MultiWorkerMirroredStrategy`; TF config → `TF_CONFIG`; num replicas in sync → `num_replicas_in_sync`; num workers
    → `num_workers`; strategy dot scope → `strategy.scope()`; dataset dot batch → `dataset.batch`; gcloud A I custom
    jobs create → `gcloud ai custom-jobs create`; n1 standard 32 → `n1-standard-32`.
- Length: narration 2,237 words (`python -m explainer.script`, v1; BRIEF.md: 1,800–2,300, target 2,100; every scene
  within its budget ±15 %). At 150–174 wpm that is ≈ 13–15 min of voice plus three ~10 s ponder timers. One part.
  Any later change must trim, not add.

  | scene | S01 | S02 | S03 | S04 | S05 | S06 | S07 | S08 |
  | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  | budget | 200 | 280 | 320 | 320 | 300 | 230 | 270 | 180 |
  | words | 198 | 314 | 346 | 353 | 305 | 252 | 311 | 158 |

---

## S01 · The run with no curves — `s01_hook.py` · `Hook`

Lecture: 6, 8, 15–16.

SHOW: Cold open, no lecture tag. V1 in its broken state: one BLUE run row (schematic, tag `illustration`) headed
"project · cheese-training-vertex-ai", run name `mobilenetv2_train_base_True`, a GREEN "finished" badge. Under it
four config chips clip on one by one (`learning_rate`, `epochs`, `batch_size`, `model_name`) and a small system-chart
tile (CPU, memory) starts wiggling.
SAY: Here is a training run that finished without a single error. The job succeeded, and the run exists in Weights and Biases. Its config is there, and its system charts are moving.

SHOW: Two larger panels slide in below the row, titled `loss` and `accuracy`: empty outlines, RED dashed, with a GRAY
caption "no data". A YELLOW question mark pulses between them. Then CODE(model-training/package/trainer/task.py:
324–331) slides in on the right (8 rows); the closing parenthesis on line 331 gets a faint YELLOW outline. No
callback is pointed out yet.
SAY: But the loss panel is empty, and so is the accuracy panel. Where are the curves? Here is the line that trained this model. Hold that thought; we come back to it in a few minutes.

SHOW: LECTURE 6. The row and the code shrink to the top-left corner. Our redrawing of slide 6's roadmap: a long arrow
POC → Prototype → MVP and five pastel bars; a YELLOW dashed box (the slide's red box, recoloured) around "Setup
Experiment Tracking" and "Build Baseline Models". An arrow points from the GRAY tag top right to a caption "the
lecture slides behind each idea".
SAY: The gray tag in the corner names the lecture slides behind each idea. On the lecture's roadmap, experiment tracking is set up together with the baseline models, at the very start. A broken run here spoils every comparison after it.

SHOW: The roadmap fades. The map of the video: five miniatures in a row, each a tiny version of V1–V5 with a one-word
caption: "the run" (a ledger row), "the package" (a box with `setup.py` on it), "the GPUs" (two chips joined by a
ring), "the batch" (a tray cut into slices), "the job" (a ticket with a clock). Each lights as named; a thin RED crack
appears on each, "where it quietly breaks".
SAY: This is the exam edition of Lecture 13. It follows five places where a training workflow quietly breaks: the run record, the package, the GPUs, the batch, and the job itself.

SHOW: The miniatures shrink to a strip at the bottom. Above it a sample YELLOW takeaway line "If the question says X,
think Y." and, beside it, a small YELLOW ponder card outline with A B C D rows and a timer ring.
SAY: Each part ends with one rule: if the question says this, think that. Three times, a quiz-style question appears on screen. Pause, pick an answer, and then hear why each wrong option is wrong.

SHOW: LECTURE 8. The strip fades. The first takeaway: two GRAY words from slide 8, "Reproducibility" and
"Accountability", write in; then the YELLOW line "If the question says experiment tracking, think: what produced this
result, and can I repeat it?" Everything fades to an empty frame.
SAY: The lecture names the reason to track at all. If the question says experiment tracking, think: what produced this result, and can I repeat it?

---

## S02 · What a run records — `s02_record.py` · `RunRecord`

Lecture: 9–13, 15.

SHOW: LECTURE 9–10. Seven GRAY column headers write in a row (our redrawing of slide 9): Environment, Code, Data,
Model, Metrics, Artifacts, Notes.
SAY: What should a run record hold? The lecture lists seven things: the environment, the code, the data, the model, the metrics, the artifacts, and your notes.

SHOW: Slide 10's table as four rows that snap into homes: "code → GitHub", "data → data versioning", "environment →
pyproject.toml · uv.lock", each with a GREEN tick; the fourth row "weights · metrics · logs" hangs on a YELLOW "?".
SAY: Most of these already have a home. Code lives in GitHub, data in a versioning system, and the environment in the pyproject file and the lock file. Weights, metrics and logs have no home; the slide leaves a question mark.

SHOW: Data-version aside (one group). The "data" row expands: a BLUE bucket object "snapshot" and a GREEN record card
"version record" joined by a PINK link labelled "content hash". Then an excerpt panel CODE(model-training/package/
trainer/task.py: 96–100) (5 rows) with line 97's URL lighting; a GRAY note "a fixed release · not in config".
SAY: One word on data. A data version is a pair: the archived snapshot in a bucket, and the version record that names it, linked by a content hash. This trainer instead downloads a fixed release of the dataset, and never writes it into the config.

SHOW: LECTURE 11–13. The aside folds away; the "?" row is caught by a BLUE ledger (V1, `illustration`) that slides in
from the right: wandb.ai drawn as a table of empty run rows, no logo. A GRAY chip "W&B · hosted · MLflow if you must
self-host" (slide 12).
SAY: Recording by hand gets forgotten, so the lecture automates it with Weights and Biases. Picture a ledger in which every training run is one row.

SHOW: LECTURE 15. CODE(model-training/package/trainer/task.py: 152–153) at the left (2 rows); a GOLD key glyph flies
from a GRAY `--wandb_key` flag chip into the ledger's lock. No value anywhere.
SAY: The repo trainer, task dot py, talks to that ledger in four calls. First it logs in, with a key passed as a flag; the key never appears in the code.

SHOW: The login panel Transforms into CODE(model-training/package/trainer/task.py: 312–322) (11 rows). On "opens" a
new BLUE row slides into the ledger, project `cheese-training-vertex-ai`, name `mobilenetv2_train_base_True`; its
outline turns YELLOW and a PINK arrow labelled `wandb.run` swings onto it. Lines 315–320 light GREEN one by one as the
four config chips clip onto the row.
SAY: Then wandb dot init opens a new row, with a project, a name, and a config: learning rate, epochs, batch size, and model name. It also makes that row the active run, and the pointer called wandb dot run now points at it.

SHOW: The panel Transforms into CODE(model-training/package/trainer/task.py: 335–338) (4 rows). Line 336 lights: a
fifth chip `execution_time` clips on. Line 338 lights: a padlock closes on the row, its outline turns GREY, and the
PINK `wandb.run` arrow drops into a GRAY slot labelled `None`.
SAY: After training, the script adds one more config value, the execution time. Then wandb dot run dot finish seals the row, and the pointer falls back to nothing.

SHOW: The sealed row enlarges: config chips GREEN ticks, system tile GREEN tick, and the loss strip an empty RED dashed
outline. A GRAY caption: "init records: config + system metrics · not: loss".
SAY: Notice what the init recorded: the config, and system charts such as CPU and memory. It did not record a loss. Something still has to log the metrics.

SHOW: Takeaway, YELLOW: "If the question says record of a run, think: init opens it, config describes it, something
must log the metrics, finish closes it."
SAY: If the question says record of a run, think: init opens it, config describes it, something must log the metrics, and finish closes it.

SHOW: The takeaway fades. PONDER card 1 (YELLOW): "Your script calls `wandb.init(config=...)`, trains with
`model.fit`, then calls `wandb.finish()`. The run page shows the config but no loss curve. Which change puts a loss
curve on that run?" A) pass `name=` to `wandb.init` · B) call `wandb.config.update({"loss": ...})` after training ·
C) pass `WandbMetricsLogger()` in `fit`'s `callbacks`, created after `init` · D) call `wandb.login()` again before
`fit`. After the timer the card fades to an empty frame (the answer opens the next scene).
SAY: First question. The run shows its config but no loss curve. Which change puts a loss curve on it? Pause here if you want.
PONDER(10 s, "Which change puts a loss curve on that run?")

---

## S03 · The callback writes to the active run — `s03_callback.py` · `ActiveRun`

Lecture: 15–16.

SHOW: LECTURE 15. PONDER card 1 is redrawn as it was. C turns YELLOW. RED one-liners appear beside A, B, D as named:
A "a name labels the row, logs nothing"; B "one number in config, not a history"; D "authenticates, logs nothing".
SAY: The answer is C: pass the Wandb Metrics Logger in the callbacks of fit, created after init. A only names the row. B stores one number in the config, not a history over epochs. D logs in again, and logging in records nothing.

SHOW: The card leaves. CODE(colab/L13_wandb_tracking/cell-38.py: 41–61) folded to lines 42, 49, 55–61 (9 lines + 2 gap
rows), header `Experiment Tracking notebook · training cell · lines 41–61 (folded)`. Line 42 (`wandb.init(...)`)
lights BLUE, line 60 (`callbacks=[WandbCallback(...)]`) lights PURPLE.
SAY: The lecture's notebook shows the pattern. It calls init, and then fit, with a callbacks list that holds the Wandb Callback.

SHOW: V1 mechanism. The panel shrinks left. The ledger with one open BLUE row (YELLOW outline, PINK `wandb.run`
arrow). A PURPLE pen (the callback) rides the PINK arrow. An epoch bar runs across under the row; at its end the pen
drops one GREEN tick into the row's history strip. A GRAY label on the pen's path: "`wandb.log` → `wandb.run`".
SAY: A callback is a pen that Keras holds during training. At the end of every epoch it calls wandb dot log, and that call writes to wandb dot run: whichever row is active right now, not the run the pen was created with.

SHOW: Two more epoch bars: two more ticks. A GRAY chip `log_freq="epoch"` (default) beside the pen; a dimmer chip
"per batch: only if you ask".
SAY: By default that is one history entry per epoch. Logging per batch happens only if you ask for it.

SHOW: Variant (a). A fresh row, no pen. A label "fit · 3 epochs"; three epoch bars run; the strip stays an empty RED
dashed outline; tick counter "0". A small GREY copy of the hook's empty loss panel flashes beside it.
SAY: Now four experiments. First, no pen. Fit runs three epochs, and the strip stays empty. That is the run from the start of the video.

SHOW: Variant (b). Labels "init" → "fit · 3 epochs" → "fit · 2 epochs" (no finish between, a GRAY "no finish" chip).
Ticks 1–3 drop, then the second fit's bars run and ticks 4–5 land on the same row; counter "5 entries · 1 run".
SAY: Second: init, fit for three epochs, then fit for two more, with no finish in between. The pointer never moved, so ticks four and five land on the same row. One run, five entries.

SHOW: Variant (c). Labels "init" → "fit · 3" → "finish" → "init" → "fit · 2". After three ticks the padlock seals
row 1 (GREY). The PINK arrow drops to `None`, then the new init slides in row 2 (YELLOW outline) and the arrow swings
onto it; its strip starts empty, then gets ticks 1 and 2. Counters "row 1: 3" and "row 2: 2".
SAY: Third: finish after the first fit, then init again. The first row is sealed with three entries. The new row starts empty, and the next fit writes entries one and two there.

SHOW: Variant (d). Labels "finish" → "fit" (no new init). The pen follows the PINK arrow down into the `None` slot and
stops; a RED error box "wandb.Error: You must call wandb.init() before wandb.log()" with the PURPLE `wandb 0.15.11`
chip. Below it a second, smaller RED line: "WandbMetricsLogger() with no active run → You must call wandb.init()
before WandbMetricsLogger()".
SAY: Fourth: finish, then fit again without a new init. The pen follows the pointer to nothing and stops with an error: you must call init before log. Creating the logger with no active run fails the same way, at once.

SHOW: LECTURE 15–16. Back to the hook: the row `mobilenetv2_train_base_True` with its empty panels. An excerpt panel
CODE(model-training/package/trainer/task.py: 21–22) (both callbacks imported, lines lit GRAY "imported · unused"),
then CODE(model-training/package/trainer/task.py: 324–331) beside our redrawing of slide 15's middle line
`callbacks=[WandbCallback()]`, which slides into the gap before line 330 as a GREEN ghost; the empty panels fill with
two schematic curves (`illustration`).
SAY: Now the hook. The repo trainer imports both callbacks but passes none to fit, so its run has a config and system charts, and no curves. The lecture's middle line, the callback, is the line that is missing.

SHOW: A GRAY chip "the notebook prints: WandbCallback is deprecated → WandbMetricsLogger"; the ghost line's class name
morphs to `WandbMetricsLogger()`.
SAY: One detail: the notebook warns that the Wandb Callback is deprecated. The Wandb Metrics Logger does the same job.

SHOW: Takeaway, YELLOW: "If the question counts history entries, think: one per epoch, into whichever run is open when
the epoch ends; finish ends the count, a new init starts a new one." Fade to an empty frame.
SAY: If the question counts history entries, think: one per epoch, into whichever run is open when the epoch ends. A finish ends the count, and a new init starts a new one.

---

## S04 · What the package carries — `s04_package.py` · `WhatPipInstalls`

Lecture: 23–25.

SHOW: LECTURE 23–24. Our redrawing of slides 23–24 as one strip, left to right: GREY notebook tile → GREEN "Python
file · arguments" tile (three chips `--model_name`, `--epochs`, `--batch_size` push up into it) → GREEN tarball →
BLUE bucket → BLUE "job". Step badges 1, 2, 3 light in turn.
SAY: The lecture moves training to the cloud in three steps. Turn the notebook into a Python file with arguments, package it and upload it to a bucket, then create a training job on Vertex AI.

SHOW: V2. The strip shrinks to the top. The `package/` tree (GREEN): `setup.py`, `setup.cfg`, `PKG-INFO`,
`trainer/` with `__init__.py` (an empty file, GRAY caption "empty"), `task.py`, `task_multi_gpu.py`. Beside it
CODE(model-training/package/setup.py: 1–13) (13 rows → folded to 1, 5, 7–13: 9 lines + 1 gap row).
SAY: Here is the package folder. Setup dot py describes it, and the trainer folder holds an empty init file and the two training scripts.

SHOW: Line 5 and line 10 light PURPLE: a "shopping list" card with one PURPLE chip `wandb==0.15.11` peels off the
panel. Line 11 lights PINK: a PINK scanner bar labelled `find_packages()` sweeps the tree; it lights only `trainer/`
(because of `__init__.py`), which turns bright GREEN; `setup.cfg` and `PKG-INFO` stay dim.
SAY: Setup dot py keeps two separate lists. Install requires is a shopping list that pip downloads from the Python Package Index; here, one pinned wandb version. Find packages decides which of your own folders get installed, and it lights only folders with an init file.

SHOW: CODE(model-training/package-trainer.sh: 1–4) (4 rows) replaces the setup panel. Line 2: the whole `package/`
tree wraps into `trainer.tar`; line 3: it shrinks into `trainer.tar.gz`; line 4: it flies along a PINK path
`$GCS_BUCKET_URI/cheese-app-trainer.tar.gz` into the BLUE bucket. Then CODE(model-training/cli.sh: 10–11) (2 rows):
the package path and `PYTHON_MODULE="trainer.task"` light PINK.
SAY: The packaging script tars the whole package folder, zips it, and copies it into your bucket. The job script then points Vertex AI at that file, and names the module to run: trainer dot task.

SHOW: The bucket hands the tarball down into a BLUE job VM. Inside it a TEAL box "prebuilt training image ·
tf-cpu.2-17.py310" (excerpt chip `cli.sh · line 31 (excerpt)`) with an ORANGE shelf holding TensorFlow, scikit-learn,
requests. Off to the left, a small GREY laptop with a TEAL `model-training-cli` box whose only arrow is "submit".
SAY: Here is the key fact. Your own Docker image only submits the job. The job runs in Google's prebuilt training image, and your code reaches it only through the tarball.

SHOW: The ORANGE shelf glows; GRAY dashed lines link `sklearn` and `requests` to an excerpt chip
`task.py · line 3 (excerpt)` `import requests` and `line 17 (excerpt)` `from sklearn...`; a GRAY note "not in
setup.py".
SAY: That image already ships TensorFlow, scikit-learn and requests. That is why the trainer can import them although setup dot py never names them. Call it luck, not declaration.

SHOW: pip unwraps the tarball inside the VM: the shopping list fetches `wandb` from a GRAY "PyPI" cloud (GREEN ✓), the
`trainer` package lands on the shelf (GREEN ✓). A GRAY log line "Successfully installed cheese-app-trainer … wandb …"
(schematic, `illustration`). Then `python -m trainer.task` lights.
SAY: On the job machine, pip unwraps the tarball. The shopping list fetches wandb, and the trainer package is installed. Then Vertex runs python dash m trainer dot task.

SHOW: The failure. Rewind to the tree: a GREY dashed file `augment.py` (tags `illustration`, `example · not in the
repo`) sits beside `setup.py`, outside `trainer/`. It rides inside the tarball (GREEN outline around the whole
bundle), but the PINK scanner passes over it without lighting it. A GRAY variant note: "same result: a folder with no
`__init__.py`".
SAY: Now add a teammate's module, augment dot py, a made-up example. It sits next to setup dot py, outside the trainer folder. It is uploaded inside the tarball, but find packages never lights it, so it is never installed.

SHOW: In the VM, a schematic line `import augment` (`illustration`) lights; a PINK search beam scans the shelves (the
import path) and finds nothing; a RED box "ModuleNotFoundError: No module named 'augment'" appears directly under the
GREEN "Successfully installed …" line.
SAY: The task reaches import augment, and Python searches its import path. Nothing. Module Not Found Error, printed right under the line that says every dependency installed.

SHOW: The fix (schematic card, `illustration`): `augment.py` slides into `trainer/`, the scanner lights it, and the
import line becomes `from trainer import augment`; rerun → GREEN ✓. A second, smaller option chip: `py_modules=
["augment"]` in `setup(...)`. A RED-struck chip "install_requires=[..., "augment"]" with "not on PyPI".
SAY: The fix: move the module into the trainer folder and import it through the package, or list it in setup dot py. Adding it to install requires is wrong; your module is not on the Python Package Index.

SHOW: Takeaway, YELLOW: "If the question says dependencies installed but ModuleNotFoundError, think: your own module
isn't inside the package that setup.py builds." Fade to an empty frame.
SAY: If the question says dependencies installed but Module Not Found Error, think: your own module is not inside the package that setup dot py builds.

---

## S05 · One machine or many — `s05_mirror.py` · `MirrorsAndIslands`

Lecture: 26–27, 29–30.

SHOW: LECTURE 27. Our redrawing of slide 27 as a three-row ladder: "one machine · one GPU → One Device Strategy"
(GREY dashed, `concept · lecture only`), "one machine · several GPUs → Mirrored Strategy" (PURPLE), "several machines
→ Multi Worker Mirrored Strategy" (GREY dashed). A YELLOW pin "the repo is here" on row 2.
SAY: The lecture sorts training hardware into three shapes. One machine with one GPU uses One Device Strategy. One machine with several GPUs uses Mirrored Strategy. Several machines use Multi Worker Mirrored Strategy.

SHOW: LECTURE 30. The ladder shrinks to the top. CODE(model-training/cli-multi-gpu.sh: 6–12) (7 rows): line 6
`n1-standard-32`, line 7 `REPLICA_COUNT=1`, lines 11–12 `NVIDIA_TESLA_T4`, `2` light. V3: one BLUE machine box
"n1-standard-32" with two BLUE GPU chips "T4", a GRAY caption on line 7 "1 = one machine".
SAY: The repo sits on the middle row. Its multi GPU script asks Vertex AI for one machine, type n1 standard 32, with two T4 GPUs. A replica count of one there means one machine.

SHOW: LECTURE 29. CODE(model-training/package/trainer/task_multi_gpu.py: 286–289) (4 rows): line 287 lights PURPLE
(a PURPLE strategy frame wraps the machine), line 289 lights: a counter `num_replicas_in_sync = 2`. Then the panel
Transforms into CODE(model-training/package/trainer/task_multi_gpu.py: 303–321) folded to 303–306, 314–315, 320–321
(8 lines + 2 gap rows); as line 304 lights, a GREEN model replica appears on each GPU, identical shade.
SAY: The trainer creates the Mirrored Strategy and asks how many replicas are in sync: one per GPU, so two. Then it builds and compiles the model inside strategy dot scope, so every weight and optimizer variable is mirrored, one copy per GPU.

SHOW: One step, slowly. A batch tray splits into two slices (PINK arrows), one per GPU; each GPU grows a gradient
arrow; the two arrows rise into a PINK all-reduce ring, merge into one averaged arrow, split back down; both replicas
change to the same new GREEN shade.
SAY: Here is one training step. Each GPU takes its own slice of the batch and computes a gradient. The gradients meet in an all-reduce and are averaged, and the same update goes back to both copies.

SHOW: Islands. The ladder and code leave. Two BLUE machines side by side, each with its own PURPLE "MirroredStrategy"
frame and its own shard of data ("shard 1", "shard 2"). Inside each, the ring works; between them, a GRAY gap with a
crossed-out wire. Steps tick; the left replicas drift to one shade, the right to another; a RED Δ appears between
the machines.
SAY: Now two machines, each running its own Mirrored Strategy on its own shard of the data. Inside each machine the ring works, but between the machines there is no wire. After a few steps they hold different weights: two separate models, not one.

SHOW: Multi Worker (GREY dashed frame, `concept · lecture only`). A schematic `TF_CONFIG` card appears on each machine
(`illustration`): `"cluster": {"worker": [‹machine-0›, ‹machine-1›]}` and `"task": {"type": "worker", "index": 0}` /
`1`. A PINK cable joins the machines; the ring stretches across all four GPUs; every replica settles to one shade,
the Δ fades.
SAY: To train one model across machines, use Multi Worker Mirrored Strategy. Each machine reads a TF config: the list of all the workers, and its own index in that list. Now the all-reduce spans all four GPUs, and every copy stays the same.

SHOW: A GRAY note under the cable: "on Vertex AI: extra machines go in a second worker pool · Vertex sets TF_CONFIG"
(digest §3.7). Then a naming card, two rows: `num_workers` (`task_multi_gpu.py · line 289 (excerpt)`) → "GPUs on one
machine"; "worker" in Multi Worker → "a machine"; the first row's arrow PINK, the second GREY dashed.
SAY: The repo does not use it; on Vertex AI the extra machines would go in a second worker pool, and Vertex sets the TF config for you. One naming trap: the repo, like the lecture, calls its replica count num workers, but it counts GPUs on one machine.

SHOW: Takeaway, YELLOW: "If the question says several machines must train one model, think MultiWorkerMirroredStrategy
with TF_CONFIG; a MirroredStrategy never looks past its own machine." Fade to an empty frame.
SAY: If the question says several machines must train one model, think Multi Worker Mirrored Strategy with TF config. A Mirrored Strategy never looks past its own machine.

---

## S06 · Global batch, per-replica batch — `s06_batch.py` · `GlobalBatch`

Lecture: 28–29.

SHOW: LECTURE 28–29. V4. A GREEN tray labelled `dataset.batch(n)` holding n image squares; a PURPLE strategy frame
around four GPU chips below it; PINK splitter arrows cut the tray into four equal slices that slide one onto each
GPU. A counter: `global = per-replica × replicas`.
SAY: Now the batch. Under a strategy, dataset dot batch makes the global batch, the whole tray for one step. The strategy cuts that tray into equal slices, one per replica.

SHOW: The counter rewrites as `per-replica = global ÷ num_replicas_in_sync`, then flips back.
SAY: So the per replica batch is the global batch divided by the number of replicas in sync. Turn it around, and the global batch is the per replica batch times the replicas.

SHOW: Dial play with 4 replicas. A dial on the tray set to `batch(64)`: the tray splits, each GPU gets a slice
labelled 16; a RED tag beside it "intended: 64". The dial turns to `batch(256)`: each slice reads 64, GREEN tick.
SAY: Take 4 replicas, and say you want 64 examples on each. Batch by 64, and each GPU gets only 16. Batch by 256. Each GPU gets 64.

SHOW: CODE(model-training/package/trainer/task_multi_gpu.py: 291–301) (11 rows): line 292's comment lights YELLOW,
line 293 `global_batch_size = args.batch_size * num_workers` lights GREEN and the V4 counter flies onto it; line 300
lights PINK. An excerpt chip `task_multi_gpu.py · line 198 (excerpt)` `train_data = train_data.batch(batch_size)`.
Slide 29's call-out in GRAY: "Adjust dataset batch size". A GRAY note: "repo: 32 × 2 replicas = 64".
SAY: The repo does the same multiplication. It takes the batch size flag, multiplies it by the replica count, and hands the product to the dataset. Its own comment says it: batch expects the global batch size.

SHOW: A small GRAY chip "learning rate unchanged as the global batch grows · not on the quiz" (`task_multi_gpu.py`,
digest §3.7).
SAY: One side note, not for the quiz: the global batch grows, but the repo keeps the same learning rate.

SHOW: Everything fades. PONDER card 2 (YELLOW): "A script trained on one GPU with `dataset.batch(32)`. You wrap the
model in a `MirroredStrategy` on a machine with 4 GPUs and change nothing else. How many examples does each GPU see
per step?" A) 32 · B) 128 · C) 8 · D) it raises an error.
SAY: Second question. The script used batch 32 on one GPU. You add a Mirrored Strategy on 4 GPUs and change nothing else. How many examples does each GPU see per step? Pause here if you want.
PONDER(10 s, "How many examples does each GPU see per step?")

SHOW: C turns YELLOW (a mini tray of 32 splits into four slices of 8). RED one-liners: A "global mistaken for per
replica"; B "the strategy does not multiply for you"; D "nothing forbids it". A GREEN chip "keep 32 per GPU →
batch(128)".
SAY: The answer is C. The global batch is still 32, split four ways, so each GPU sees 8. A mistakes the global batch for the per replica batch. B assumes the strategy multiplied for you; it does not. D: nothing raises an error. To keep 32 per GPU, batch by 128.

SHOW: Takeaway, YELLOW: "If the question says per replica, multiply before you batch: global = per-replica ×
replicas." Fade to an empty frame.
SAY: If the question says per replica, multiply before you batch: the global batch is the per replica batch times the replicas.

---

## S07 · Training that outlives the request — `s07_jobs.py` · `DurableJob`

Lecture: 22, 24–25.

SHOW: V5. A schematic web server (`illustration`) with a handler `POST /retrain` and a YELLOW timeout ring around it,
a GREY laptop client on the left sending a request arrow. A clock reads "training: ~1 hour".
SAY: Last mechanism. Suppose a web app has a retrain button, and training takes an hour. Where should that hour run?

SHOW: Design 1: a training bar grows inside the handler; it outgrows the ring; the ring snaps, the connection arrow is
cut, the bar turns RED and dies. RED strike "1 · fit in the handler".
SAY: Design one: call fit inside the request handler. The request has a timeout, the training outgrows it, the connection is cut, and the work dies with it.

SHOW: Design 2: the handler answers at once; a thread spins off inside the server box. The server box is recycled (it
blinks out and a fresh one appears); the thread vanishes with it. RED strike "2 · a background thread".
SAY: Design two: answer at once and start a background thread. The platform can recycle that server whenever it likes, and the thread vanishes with it.

SHOW: Design 3: the client's ring is stretched wide; a GRAY proxy and the server still cut the arrow; then the laptop
lid closes and the waiting client disappears. RED strike "3 · a longer client timeout".
SAY: Design three: raise the client's timeout. The server and the proxies in between still cut the connection, and a sleeping laptop loses the answer anyway.

SHOW: A fourth tile: the V1 ledger miniature with a GRAY "no engine" caption; a RED strike "a tracker records, it
does not run".
SAY: And a tracker is no fourth option: W and B records runs, but has no engine to execute them.

SHOW: LECTURE 22, 24. The right design. The handler drops a BLUE ticket into a BLUE "Vertex AI" box and returns
`job id: ‹job-id›` at once (the ring stays small and GREEN). Inside Vertex a state machine lights in order: `QUEUED →
PENDING → RUNNING → SUCCEEDED` (digest §3.4), on its own BLUE VM with a GOLD per-minute meter ticking. The laptop
closes; the job keeps running; a second client polls the id and reads `RUNNING`.
SAY: The right design: the handler submits a durable job and returns its id at once. The job moves through its states, queued, pending, running, succeeded, on its own machine, billed by the minute. Anyone can poll the id.

SHOW: Our redrawing of slide 22's points as three GRAY chips: "GPU only for the training step", "no server to
manage", "pay only while it runs"; and a GRAY note "serverless ≠ no machine: a VM you don't own".
SAY: That is the lecture's serverless training: hardware rented only for the training step, and no server to manage. There is still a machine; you just do not own its lifetime.

SHOW: CODE(model-training/cli.sh: 30–37) (8 rows): line 32 `gcloud ai custom-jobs create` lights BLUE and becomes the
ticket; lines 33–36 light in turn (region, display name, package URI, worker pool spec); line 36's `machine-type`,
`replica-count`, `executor-image-uri`, `python-module` light inside the wrapped row.
SAY: In the repo, the ticket is one command, gcloud A I custom jobs create, with a region, a name, the package in the bucket, and a worker pool: machine type, replica count, prebuilt image, and module.

SHOW: Everything fades. PONDER card 3 (YELLOW): "You submitted a Vertex AI custom job from your laptop; it shows
RUNNING. You close the laptop and go to bed. What happens to the training?" A) it stops, because the CLI container
that submitted it exits · B) it keeps running on the job's own VM until it finishes or fails · C) it pauses until
W&B reconnects · D) it restarts from epoch 1 when you reopen the laptop.
SAY: Third question. Your custom job shows running, and you close the laptop for the night. What happens to the training? Pause here if you want.
PONDER(10 s, "What happens to the training?")

SHOW: B turns YELLOW. RED one-liners: A "the CLI container only submits"; C "W&B records, it doesn't drive"; D
"nothing on your laptop holds the job's state".
SAY: The answer is B: it keeps running on its own machine until it finishes or fails. A: the CLI container only submitted it. C: W and B records; it never drives training. D: nothing on your laptop holds the job's state.

SHOW: Takeaway, YELLOW: "If the question says training takes longer than the request, think: submit a durable job,
return its id, poll; W&B only watches." Fade to an empty frame.
SAY: If the question says training takes longer than the request, think: submit a durable job, return its id, and poll. W and B only watches.

---

## S08 · Six rules for Tuesday — `s08_recap.py` · `Recap`

Lecture: 5, 10, 15, 24, 27, 29.

SHOW: LECTURE 15. The five miniatures from S01 return as a row, plus a sixth (a bucket object linked to a record
card). The first two move up and each turns into a YELLOW rule line (two rules per frame): rule 1 under the ledger
miniature, rule 2 under the package miniature.
SAY: Six rules for Tuesday. Rule one: a callback logs one entry per epoch into the active run; init opens a run, and finish closes it. Rule two: pip installs what setup dot py packages; your own modules arrive only inside a found package.

SHOW: LECTURE 27, 29. Rules 1–2 fade; the GPU and batch miniatures move up with rules 3 and 4.
SAY: Rule three: a Mirrored Strategy covers the GPUs of one machine; across machines, use Multi Worker Mirrored Strategy with TF config, because separate strategies make separate models. Rule four: dataset dot batch takes the global batch, split across the replicas in sync.

SHOW: LECTURE 10, 24. Rules 3–4 fade; the job and data miniatures move up with rules 5 and 6.
SAY: Rule five: long training goes to a durable job with an id, never into a request handler, a thread, or a longer timeout. Rule six: a data version is an archived snapshot plus the record that points at it.

SHOW: LECTURE 5. The rules fade. Our redrawing of slide 5: three pillars "More Data", "Better/Faster Models", "Faster
Hardware"; the third lights YELLOW. Then fade to an empty frame.
SAY: The lecture began with three levers for better deep learning: more data, better models, and faster hardware. Today was the hardware lever, plus the bookkeeping that shows whether it helped. Good luck on Tuesday.
