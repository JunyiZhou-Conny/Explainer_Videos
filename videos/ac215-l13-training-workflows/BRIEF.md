# Brief · AC215 L13 — Advanced training workflows: a run is a record, a job is a rented machine

The design of this video, written before the script. Series rules: `docs/AC215_SERIES.md`.
Facts: `digest.md` (the verified tutorial digest), `SLIDES.md` (the lecture-slide digest and scene
map) and `assets/` (real captures, see `ASSETS.md`). **Where the digest or the slides and the
captures disagree, the captures win.** They are newer (2026-10-23 12:19–12:34 UTC) and were made by
running the README's commands as written, in README order, up to the honest, documented failure
wherever a Google credential, a W&B account, a GPU or a browser would be needed (this sandbox has
none). The decisions below were taken by the coordinator and are not re-opened in later stages:

| topic | digest / slides | captures and decision (use these) |
| --- | --- | --- |
| `sh docker-shell.sh` | digest: fails at `Dockerfile:37` (`google-cloud-sdk` has no candidate); "bullseye suites still answer" | **fails earlier today**, at build step 2/14 (`Dockerfile:18-19`): bullseye-security's pool returns `404 Not Found` for 22 packages (`laptop/21`). **Decision: show both failures and both one-line fixes, kindly, as errata a student will hit** — fix 1 `Dockerfile:2` → `python:3.13-slim-bookworm` (`22`), which reaches the digest's line-37 failure word for word (`23`), fix 2 `Dockerfile:37` → `google-cloud-cli` (`24`) — then the final `git diff` (`25`) and the successful start (`26`) |
| GPU vs CPU | slides 22/24: GPU on demand; README presents GPU first | `cli.sh` runs its CPU block (commit `3efb2d5`). **Decision: follow `cli.sh`'s CPU default** (it runs without any GPU quota). GPU and multi-GPU: the quota beat and the scripts on screen, **no fake success** (`40`, `50` fail at auth like everything else) |
| the Vertex job's logs | digest B12 lists expected lines, incl. epochs, `loss ≈ 100`, timings | **no job log exists anywhere.** Only the code's own prints plus the counts recorded in both notebooks (1156; 936/104/116), tagged `recorded` / `illustration`. **No epoch, loss or timing panels for the repo trainer** |
| W&B dashboard | slide 16: a screenshot full of curves (an earlier app's project) | **schematic only, from notebook B's stored outputs**, names masked (`<W&B user>`, `<team>`, run ids cropped). The repo run's W&B side is shown from its *code* (what `task.py` sends), never as a dashboard with values |
| W&B "logged in" line in a job | digest B12: none at `wandb.login`; ASSETS finding 7: probably one | **unverified either way: never on screen as job output.** The stand-in's offline `Appending key … /root/.netrc` (`86`) is live and tagged; notebook B's `Currently logged in as` is `recorded` (Colab, not a job) |
| W&B key length | digest: "`40` for a classic key" | `40` is the **placeholder's** length and what wandb 0.15.11 accepts (`86` vs `87`: "yours was 47"). Today's key format could not be checked: **never claim a length for a real key**; the check that matters is "not 0" (`11`) |
| prices | digest §2: dollar figures "from memory" | **no prices anywhere.** GOLD cost tags without numbers, pointing to the Vertex AI pricing page; the video still says what bills, what keeps running and what to cancel |
| `sh -x cli.sh` | not in the digest | **live** (`40:63-77`): the GPU image is set, then overridden by `tf-cpu.2-17.py310`, and **the W&B key travels inside `--args`** (digest E18). Shown briefly, as the security point |
| `python cli.py` | digest B16/gotcha 3: predicted | **live** (`60`): `KeyError: 'GCP_REGION'`, then (after `export`) the missing-key error at `cli.py:23`. Shown briefly, as the bridge to L15 |
| the job's first minute | — | local stand-ins (`80`–`87`, tag **`extra · local stand-in`**): `pip install` of the real tarball in a plain Python 3.10 container (wandb 0.15.11 installs, no TensorFlow, no scikit-learn), the trainer can't even print `--help`, and `wandb.login` with three keys (empty / `"16"` / 40-character placeholder). Brief |
| notebook B's `wandb.config = {...}` | digest E14: "likely never sent", checked in 0.15.11 source | **live on today's wandb 0.31.0** (`colab/C38`): `type(wandb.config): dict`, `the run's config: {}`; the fix `wandb.init(config=…)` (`C38b`) keeps all keys plus `execution_time` |
| length | digest §8: ≈32 min, ~4,950 words at 155 wpm | series voice ~174 wpm: plan **~4,130 words ≈ 23.7 min narration**, ~29–31 min with typing, outputs and ponders |

## Audience and goal

An AC215 student who has done L1–L11: they have a GCP project with billing (L1), know images,
containers, bind mounts and `docker-shell.sh` scripts (L2–L4), have trained and fine-tuned in
Colab (L8), and from L10–L11 know service accounts and JSON keys in a sibling `secrets/` folder,
`GOOGLE_APPLICATION_CREDENTIALS`, buckets, and a versioned dataset. New to them: experiment
tracking (by hand and with W&B), the W&B run lifecycle, turning a notebook into a pip-installable
package, Vertex AI custom jobs and prebuilt training containers, the identity that submits a job
versus the one that runs it, GPU quotas, and data-parallel multi-GPU training. They watch with two
Colab copies (notebook A, notebook B) and a clone of
[dlops-io/model-training](https://github.com/dlops-io/model-training) open, a W&B account (free
tier) and a GCP project, pausing to run each step. **This lecture's Vertex AI jobs bill the
project while they run** (a CPU machine by default; more with GPUs): GOLD tags mark each billing
point, without numbers, and the video ends on the teardown checklist.

After the video they can:
- run both notebooks and read their record of five training runs — the `experiment_<ts>/` folder
  of five files per model, the comparison table — and say what that record leaves out (the split,
  the code version, the data version), which is why two copies of the same notebook crowned two
  different winners;
- log runs to W&B from Colab with a secret named `WandB`, explain why only the run with a callback
  draws curves, why `wandb.config = {...}` sends nothing (`{}`), and write the three-line pattern
  correctly (`init(config=…)` · callback · `finish`);
- explain serverless training as "rent the machine for the training step": a tarball of their
  code goes to a bucket, Vertex AI starts a VM with Google's prebuilt TensorFlow container,
  `pip install`s the tarball, runs `python -m trainer.task` with flags, and deletes the VM;
- build the `model-training-cli` cockpit despite today's two Dockerfile failures, and show that it
  only submits (`No module named 'tensorflow'`);
- package and submit with `sh package-trainer.sh` and `sh cli.sh`, read the job in `sh -x`, and
  know that their W&B key sits in the job's arguments (rotate it) and that an un-exported key
  fails only after the data download;
- name who submits (the `model-trainer` key) and who runs (your project's Vertex AI service agent);
- say which three switches must agree for a GPU to be used, and what `MirroredStrategy` splits,
  averages and creates inside `strategy.scope()`;
- tear everything down and know the trained model is not saved anywhere yet (L15 does that).

## Length and parts

~29–31 minutes. Narration 3,900–4,300 words (Kokoro af_heart, speed 0.9 ≈ 174 wpm); the plan below
totals **~4,130**. Word budgets per scene are targets (±15 %).

- **Part 1 = S01–S07** (~1,790 words, ~13 min): **track it, then get ready** — the hook, the
  lecture's map, notebook A's home-made tracker, notebook B's W&B runs, the three-line pattern and
  the assignment that goes nowhere, serverless training as a concept, and the repo's setup
  (clone, API, quota, secrets, service account, bucket, W&B key).
- **Part 2 = S08–S15** (~2,340 words, ~17 min): **ship it** — the cockpit that won't build and its
  two fixes, what goes in the tarball, one command and the key inside it, who submits and who runs
  (and the job's first minute, stand-in), what the job prints and what W&B can show, three
  switches for one GPU, two GPUs and one model, then the missing model, teardown and recap.

The cut is the lecture's own seam (slides 17 → 18: experiment tracking | serverless training), one
scene later so that part 1 ends with everything a job needs in place. Part 1 ends on V1 with the
Colab lane lit and the repo lane drawn dashed, the key in a variable and a bucket with a name:
"next, we build the cockpit — and today it won't build." Part 2 opens on that failure.

## Colours (series table, applied)

| meaning | colour |
| --- | --- |
| your laptop: host shell, host filesystem, the `secrets/` folder's home, the browser | GREY |
| remote machines and services: the GCP project boundary, the bucket, Vertex AI, the job's VM, Cloud Logging, the Colab runtime (T4); `wandb.ai` as a **separate** BLUE building outside the GCP boundary | BLUE |
| containers and images: `model-training-cli` (the cockpit), Google's prebuilt `tf-cpu.2-17.py310` / `tf-gpu.*` containers inside the job VM, the stand-in containers (dashed) | TEAL |
| system-wide, provided, not yours: Debian base images (bullseye → bookworm), apt packages (`google-cloud-sdk` → `google-cloud-cli`), what the prebuilt image is *assumed* to provide (TensorFlow, scikit-learn, requests), the Google-managed service agent's badge | ORANGE |
| project-owned, pinned, protected: `package/` (`setup.py`, `trainer/`), `install_requires = wandb==0.15.11`, `uv.lock`, the tarball, the `model-trainer.json` key, the W&B key while it sits in your shell, a run's `config` | GREEN |
| tools: docker, gcloud, gsutil, uv, pip, tar/gzip, the `wandb` library, `tf.distribute` | PURPLE |
| errors and exposure: the 404s, `no installation candidate`, auth errors, `KeyError`, `no-tty`, `yours was 2`, `Conflict`, the W&B key once it is visible inside `--args`, the config that went to a loose dict | RED |
| your turn, the trackers, the current step, the run under discussion | YELLOW |
| money: the job VM while it runs, a GPU, the 32-vCPU two-T4 machine, bucket storage (tarball, experiment folders) — **never a number** | GOLD |
| routes: `gsutil cp` into the bucket, `--python-package-uris`, the job's stdout → logs, the W&B stream to `api.wandb.ai`, the gradient all-reduce links | PINK |
| future / elsewhere / missing: the trained model that is never saved, L15 (saving, Pipelines), Multi Worker Mirrored, the curves no callback draws | GREY, dashed |

Episode-local semantics (keep consistent): **a run is a WHITE row** in a ledger (neutral record);
its columns are slide 9's seven items, filled cells WHITE, empty cells GREY-dashed. **Curves only
exist where a callback pipe connects `model.fit` to the row** — no pipe, no curve, drawn as a ghost
outline. **The two keys are two GREEN badges** (Google key file, W&B key); the W&B badge turns RED
the moment it is printed inside `--args`. **Your Docker image never leaves the laptop**: in every
drawing the TEAL cockpit stays GREY-side and only the GREEN tarball crosses to BLUE.

## Running example

- **The laptop** (a fresh `docker:29.8.2-dind` engine standing in for Docker Desktop, linux/amd64):
  user `student`, home with `model-training/` and `secrets/` side by side (`05`); terminal title
  `laptop`, prompts `student@laptop:~$`, `…:~/model-training$`. Say once: "`Architecture: x86_64`
  — on a Mac too, because the script builds for amd64; on Apple Silicon that build is emulated and
  slower."
- **Inside the cockpit**: `root@<id>:/app#` (the image creates a user `app` but never switches to
  it; ids change every run — say once, crop them where they appear in outputs).
- **Colab**: a notebook-frame `illustration` with the cells' code verbatim and their **stored
  outputs** (`recorded`, the instructors' runs of 2025-10-20 (A) and 2025-10-14 (B) on a Tesla T4,
  TF 2.19.0). The two pieces run in our signed-out stand-in container (`colab/`) are tagged
  `extra · local stand-in`.
- **The sandbox, honestly** (said once, in S07, then never apologised for): this recording machine
  has no Google credentials, no W&B account, no GPU and no browser. The key in the folder shots
  (`06`) is an obviously invalid stand-in, moved out before the first container start, so every
  cloud step shows **the exact failure a student with a misplaced key gets** (gcloud's "no active
  account"). Success is shown only where a source records it: the notebooks' stored outputs, the
  code itself. A Vertex job's success, `gsutil cp`'s success and gcloud's "submitted" lines are
  recorded nowhere: **command on screen, success described in words, no output panel.**
- **Placeholders, everywhere**: bucket `gs://your-bucket-placeholder` (it exists nowhere, `07`),
  project `your-gcp-project`, W&B key `PLACEHOLDER_NOT_A_REAL_WANDB_KEY_0000000` (`10`, `40`). The
  instructors' resource names (`cheese-app-trainer`, `ac215-project`, `cheese-app-models`) appear
  only inside quoted source lines and `08`, always with "replace this with yours". No person's
  name anywhere (the notebooks' `<W&B user>`; the W&B team shown as `<team>`).
- **Versions**, all "at the time of recording": Docker 29.8.2, git 2.54.0; cockpit after both fixes:
  Python **3.13.17**, uv **0.13.5**, Google Cloud SDK **590.0.0** (gsutil 5.37), aiplatform
  **1.120.0** (locked), image 2.59 GB; build 314.2 s; prebuilt images still served (`09`):
  `tf-cpu.2-17.py310` 4.31 GB, `tf-gpu.2-17.py310` 8.93 GB, `tf-gpu.2-14.py310` 7.61 GB compressed;
  stand-in: Python 3.10, pip 23.0.1, wandb **0.15.11** (the pin); Colab stand-in: Python 3.12.15,
  `pip install wandb -U` → **0.31.0** (`C05b`); notebooks recorded: TF 2.19.0, Keras 3.10.0 (B),
  wandb **0.22.2** (B). The tarball (8 entries, **4016 bytes**) is deterministic for this commit.
- **Crops** (capture-only artefacts, ASSETS "Capture-only deviations"): the `[IP: 172.17.0.1
  38713]` tail on every apt line of `21` (it is the sandbox's proxy relay; a student sees a Debian
  mirror address); the `wandb: Network error (ProxyError), entering retry loop.` lines in `84`,
  `86`, `87`; container ids in prompts and in `71`'s conflict line; the job name's random hex in
  `40:65-66, 77` (show `cheese_training_job_<12 hex>`); BuildKit `sha256` export lines (`26:28-31`);
  W&B run ids, auto run names and the team in notebook B's URLs; image ids (`27`, `91`).

## Visual set pieces (the 3Blue1Brown part)

Class names in `scenes/common.py`; none collides with a scene class (`video.yaml`).

- **V1 · `TrainingMap` — slide 24 in three layers, plus the Colab lane (built S02/S06, closes part
  1 in S07, reopened S08, lit piece by piece, complete and unlit in S15).** Bottom layer, GREY: the
  laptop with the TEAL cockpit `model-training-cli` ("Model Trainer CLI Container", slide 24's
  words, said once) and the GREEN `secrets/` drawer. Middle, inside a BLUE dashed boundary
  `your-gcp-project`: the bucket holding the GREEN `cheese-app-trainer.tar.gz`. Top, Vertex AI:
  job tiles that appear, run and vanish, each labelled with its hardware ("CPU, RAM" for ours; a
  T4 chip only on the GPU tile). Outside the GCP boundary, a separate BLUE building `wandb.ai`.
  Above it all, the Colab lane: two notebook cards (A → its folder → bucket; B → `wandb.ai`). The
  cockpit has exactly two arrows (package & upload; create job) and **none into a job** — the
  picture of "your container submits; it never trains", proved in S09 by `No module named
  'tensorflow'`.
- **V2 · `RunLedger` — experiment tracking as runs on a shared axis (S03 build, S04, S12 audit,
  S15 recap).** Notebook A's `experiment_1760994796/` folder fills with five files per model
  (`.keras`, `.weights.h5`, `.json`, `_train_history.json`, `_model_metrics.json`, from cell 12's
  code) and folds into a **table of five WHITE rows** — the real values of cell 54
  (`nbA:1283-1295`). Copy B's table (`nbB:1703-1715`) slides in beside it: the YELLOW winner is a
  different row (the hook). In S04 the rows become W&B runs in one project: each row grows a slot
  for curves on **one shared epoch axis**. A PURPLE callback pipe connects `model.fit` to the
  `2_block` row only; its curves draw from notebook B's recorded "Run history" sparklines
  (`nbB:1009-1022`, 25 epochs; summary `accuracy 0.72436`, `val_accuracy 0.45192`), the other four
  slots stay ghost outlines. Two MobileNet rows collapse to one label `mobilenetv2_train_base` (the
  shared display name, `nbB:1629`). In S12 the columns become **slide 9's seven items**
  (environment, code, data, model, metrics, artifacts, notes) and the repo run's row is filled
  only from `task.py` (config keys, `execution_time` as `…`, curves ghost, weights a dashed hole):
  the scorecard.
- **V3 · `ConfigBinding` — the assignment that goes nowhere (S05).** The run is a BLUE box with a
  GREEN `Config` drawer inside. The name `wandb.config` is a YELLOW sticky label on a PINK arrow
  that `wandb.init` points **at that drawer**. `wandb.config = {...}` peels the label off and
  sticks it on a loose WHITE dict outside the run (RED outline); `.update({"execution_time": …})`
  writes into the loose dict; `finish` closes the run with its drawer empty → `{}` (`C38`). Replay
  with `wandb.init(config={...})`: the four keys drop straight into the drawer, `update` adds the
  fifth → `C38b`. One line, visual: Python assignment rebinds a name; it never fills the box the
  name used to point at.
- **V4 · `TarballTrip` — what travels from laptop to Vertex (S06 overview, S09 pack, S10 submit,
  S11 unpack, S15 the model that never comes back).** (1) Slide 23 redrawn with real names:
  notebook globals (`epochs = 15`, `batch_size = 32`, the model choice) peel off and come back up
  into `task.py` as flags (`--epochs`, `--batch_size`, `--model_name`, `--train_base`,
  `--wandb_key`). (2) `task.py` + `__init__.py` drop into `trainer/`, `setup.py` clips on as a
  label (`install_requires = wandb==0.15.11`), `tar` wraps `package/`, `gzip` shrinks it to
  **4016 bytes** (`30:54`), PINK `gsutil cp` carries it to the bucket as `cheese-app-trainer.tar.gz`
  (fixed name → a new upload overwrites the old one). (3) The job spec card — `--worker-pool-spec`
  chips `machine-type=n1-standard-4` · `replica-count=1` · `executor-image-uri=…tf-cpu.2-17.py310`
  · `python-module=trainer.task`, plus `--python-package-uris` and `--args` — flies to Vertex. (4)
  A VM materialises (GOLD meter starts, no numbers); Google's TEAL image drops in (ORANGE layers:
  TensorFlow, scikit-learn, requests — *provided*, not declared); the tarball unwraps; `pip
  install` adds wandb; `python -m trainer.task --model_name=mobilenetv2 --train_base --epochs=2
  --batch_size=32 --wandb_key=…` (gcloud splits `--args` on commas into `sys.argv`); a PINK
  stdout stream to logs and a PINK stream to `wandb.ai`. (5) The script exits, the VM dissolves,
  the meter stops — and the trained weights evaporate with it (GREY-dashed ghost; nothing calls
  `model.save`). **Your Docker image never makes the trip.**
- **V5 · `ThreeBadges` — the identity that submits vs the identity that runs (S11; reprise S15).**
  Three badges on three lanyards. GREEN key file → **`model-trainer`** (submitter), its three roles
  as chips (Storage Admin, AI Platform Admin, Vertex AI Administrator, README:62): it may write to
  the bucket and create jobs — the arrow from the cockpit. ORANGE, Google-managed: **your
  project's Vertex AI service agent** (the runner, by default): it carries the job, reads the
  tarball from your bucket, and holds **no key of yours** — the key file never crosses to BLUE.
  GREEN W&B key: a badge for a **different building** (`wandb.ai`), carried *by hand* inside
  `--args`; as it enters the job spec it turns RED and a viewer icon looks over its shoulder
  (anyone who can view the project's jobs can read it — rotate).
- **V6 · `GpuSwitchboard` — three switches for one GPU (S13).** Inside a job tile, three switches
  in a row: **accelerator** (`accelerator-type=NVIDIA_TESLA_T4,accelerator-count=1` in the worker
  pool), **image** (`tf-gpu.*` with CUDA vs `tf-cpu.*`), **quota** (T4s for custom training in
  *this* region — a regional stock counter). The T4 chip lights only when all three are GREEN.
  Replays: CPU image + accelerator → a T4 sits in the slot, dark, while the GOLD meter still counts
  it (`GPU Available:  []`, `task.py:67`, `illustration`); quota 0 in the region → the job never
  starts; both `gcloud ai custom-jobs create` blocks live → two tiles with the same name.
- **V7 · `MirroredReplicas` — data-parallel multi-GPU (S14).** Slide 27's ladder first, three rows:
  one machine · one GPU (One Device), one machine · many GPUs (Mirrored — "you are here"), many
  machines (Multi Worker Mirrored, GREY dashed). Then one `n1-standard-32` box with two T4s, each
  holding an identical replica of the network (same colours). A global batch of 64 tiles
  (`global_batch_size = batch_size × num_workers`, `task_multi_gpu.py:293`) splits 32 + 32; each
  GPU computes gradients on its half (two arrows rise); the arrows meet on a PINK **all-reduce**
  link, average, and return; both replicas update with the same colour change — the copies stay
  identical. `with strategy.scope():` is drawn as a frame around model + optimizer + compile: the
  variables created inside become mirrored (twin) variables; a model built outside stays single.
  Caption, not a claim of speed: "2 GPUs ≠ 2× faster" (start-up, download and image pull don't
  shrink; learning rate unchanged at 0.001, `:275`).

## README step trackers (ReadmeTracker, top-left)

Seven trackers, titled with the notebook / README headings so "step k of N" matches what the viewer
scrolls past. Notebook headings from the extracts (A has a typo, "Image Classificaton Models";
the tracker writes it correctly). README = `model-training/README.md` @ `b9aee1c`.

- **A · Notebook A › Cheese Classification Models**, 6 steps: Setup Notebook · Dataset · Build
  Data Pipelines · Image Classification Models · Experiment Results · Upload Experiment to Cloud
  Storage
- **B · Notebook B › Experiment Tracking with W&B**, 6 steps: Setup (`!pip install -q wandb -U`) ·
  Dataset & pipelines · W&B login (secret `WandB`, cell 34) · Train five models (cells 36–52) ·
  Experiment Results (cells 55–60) · Upload (cells 64, 66)
- **C · model-training › Setup Environments & Credentials** (`README.md:6-81`), 7 steps: Clone ·
  Vertex AI API · GPU Quotas · `secrets` folder · Service account + key · GCS bucket · WandB key
- **D · model-training › Run Container** (`:83-116`), 2 steps: Edit `docker-shell.sh` ·
  `sh docker-shell.sh` — with two `extra` rows: fix 1 (`Dockerfile:2`), fix 2 (`Dockerfile:37`)
- **E · model-training › Package & Upload Python Code** (`:119-129`), 3 steps: Review `setup.py` ·
  Review `task.py` · `sh package-trainer.sh`
- **F · model-training › Create & View Jobs in Vertex AI** (`:132-163`), 5 steps: Review `cli.sh` ·
  `sh cli.sh` · CPU (optional — already the default) · View Jobs · View Training Metrics
- **G · model-training › OPTIONAL: Multi GPU Training** (`:165-170`), 4 steps: Review
  `cli-multi-gpu.sh` · Review `task_multi_gpu.py` · Make changes · `sh cli-multi-gpu.sh`

Steps the README does not have are marked `extra` in the tracker caption and the narration ("this
one isn't in the README"): `git log`, `ls`, `tree`, the bucket curls (`07`, `08`), the prebuilt
image manifests (`09`), `echo ${#WANDB_KEY}` (`10`, `11`), **the two Dockerfile fixes** (`22`,
`24`), `git diff` (`25`), the in-container checks (`26:42-69`), `docker image ls`, `ls -l` /
`tar tzvf` / `gsutil ls` / the host-side check (`30`, `31`), `gcloud auth list`, **`sh -x cli.sh`**,
`gcloud ai custom-jobs list`, the un-exported-key shell and the second shell (`70`, `71`),
**`python cli.py`** (`60`), the stand-ins (`80`–`87`, tag `extra · local stand-in`), notebook B's
`wandb.finish()`, the clean-up (`90`, `91`, `gsutil rm`, `gcloud ai custom-jobs cancel`). S01, S02,
S06 are concept scenes with no tracker; S11's identity beat has none; S15's teardown uses an
`extra · clean-up` tracker (the README has no clean-up section).

## Scene plan

Notation: `laptop/NN` = `assets/terminal/laptop/NN-*.txt`, `colab/CNN` likewise; line numbers are
file lines (line 1 is the `$` command and is never printed; `[exit N]` is never printed). `nbA:` /
`nbB:` = line numbers in `assets/source/colab/notebook-A-1h6xRhjI.cells.txt` /
`notebook-B-1aAE5vR9.cells.txt` (cell numbers are the extracts' 0-based indices). ▶ = README or
notebook step with a `your turn` tag at real checkpoints. CODE(file: a-b) quotes
`assets/source/model-training/` at `b9aee1c`. `lecture_ref(13, "a–b")` per AC215_SERIES rule 9;
spans from SLIDES.md §5.

### Part 1 · Track it

**S01 · Two tables, two winners (~220 words) — `s01_hook.py` · `Hook`.** Cold open, no tracker;
`lecture_ref(13, "8")` on the closing beat. The puzzle, as two real tables side by side (V2's
first frame), `recorded`: copy A of the notebook (cell 54, `nbA:1283-1295`) and copy B (cell 55,
`nbB:1703-1715`), cropped to the columns `name · epochs · accuracy`, values verbatim. Same code,
same 1,156 cheese photos, the same five recipes. Copy A crowns **`mobilenetv2_train_base_True`,
68.97 %** (the fine-tuned MobileNet), copy B crowns **`mobilenetv2_train_base_False`, 68.97 %**
(frozen) and puts fine-tuned at 62.93 %. The question on screen: *which recipe is better — and
from these two tables, can you even tell what was different?* (One clue is visible, and the
narration only points at the column: `epochs`.) "Hold that question; part of the answer is in the
table, and part of it is in what the table never wrote down." Second beat, the road ahead: the
winner leaves Colab, gets packed into a 4-kilobyte tarball and trains on a machine you rent for
minutes, from one command — and that command carries a line we'll read together: the `--args`
of `40:75` with the key in RED (placeholder). How to follow along: two Colab copies (free T4), a
W&B account (free tier), Docker, a GCP project with billing (GOLD: Vertex jobs bill while they run
— no amounts in this video, check the pricing page); seven trackers, `▶ your turn`, the study
guide has every command. Slide 8 in one line: *reproducibility*, *accountability* — today's two
words.

**S02 · Three levers and a missing row (~220) — `s02_levers.py` · `LeversAndRecord`.** No tracker;
`lecture_ref(13, "5–6, 9–12")`. Slide 5 redrawn as three dials — more data, better models,
faster hardware — the third lights: this lecture rents hardware, and adds the bookkeeping that
shows whether it helped. Slide 6's roadmap in ten seconds: POC → Prototype → MVP; the dashed box
"Setup Experiment Tracking + Build Baseline Models" is today (and Milestone 3 asks for tracking
plus one serverless run, logged and reproducible — digest §7). Slide 10's table redrawn: code →
GitHub, data → versioning (L11's DVC, a callback line), environment → `pyproject.toml` / `uv.lock`,
**weights, metrics, logs → "?"** — the row that hangs. Slide 9's seven items as a checklist that
will become V2's columns. Slide 12 in one sentence: W&B here (hosted); MLflow if you must
self-host; the milestone accepts an equivalent. V1 built as the lecture's map: the Colab lane (A
fills a folder, B streams to `wandb.ai`) and the repo lane (laptop → bucket → Vertex → `wandb.ai`),
both still grey — "today we light both".

**S03 · A tracker made of folders (~280) — `s03_notebook_a.py` · `FolderTracker`.** Tracker A1→A6;
`lecture_ref(13, "10–11")`. ▶ Open notebook A (course link; *File → Save a copy in Drive*; *Runtime
→ Change runtime type → GPU*) — notebook-frame `illustration`. Cell 8, `recorded` (`nbA:115-121`):
`tensorflow version 2.19.0`, `Number of replicas: 1`, a `GPU:0` device; cell 10's `nvidia-smi` box
cropped to `Tesla T4` (`nbA:137`). Cell 17: `Full size of the dataset: 1156` (`nbA:353`) and the
label list (`nbA:352`, remember its order). Cell 26: the split, code shown (`nbA:431-443`) then
`train_x count: 936` / `validate_x count: 104` / `test_x count: 116` (`nbA:445-447`). **PONDER 1
(8 s)**: "The cell sets `validation_percent = 0.2`. Yet validation is 104 of 1,156. What did the
code actually do?" Answer: both splits use `test_percent` — 10 % of 1,156 → 116, then 10 % of the
remaining 1,040 → 104 (the line is on screen; digest E4; the repo trainer has the same lines,
`task.py:134-146`). Then V2: cell 31 `create_experiment()` makes `experiment_<unix time>/`; each
model's `evaluate_save_model` (cell 12's code) drops five files per model into it — the home-made
tracker. Cell 54's table assembles (`nbA:1283-1295`), cell 56 picks `best_model`
(`nbA:1304`). Kindly, one line (E22): the table formats accuracy as text *before* sorting, so it
sorts strings — fine here, wrong for a `9.50%`. **The hook's first answer**: this folder records
settings and scores, but not *which* 116 photos were the test set — the split has no seed, so
every run grades on a different 116; one photo is 0.86 points, and copy A's winning margin is
**two photos**. ▶ Cells 62–66: `auth.authenticate_user()`, edit cell 63 (`GCP_PROJECT`,
`GCS_BUCKET_NAME` are the instructors' — use yours), upload → `recorded` lines `uploading file
experiment_1760994796/…` (`nbA:1437-1450`, first lines). GOLD: the uploaded folder is stored in
your bucket (model files of 10–104 MB each, the table's own `model_size`).

**S04 · Runs on a shared axis (~290) — `s04_wandb.py` · `SharedAxis`.** Tracker B1→B6;
`lecture_ref(13, "12–13, 16–17")`. ▶ Cell 5 `!pip install -q wandb -U`: our signed-out stand-in,
`extra · local stand-in` → `C05` (quiet; only pip's notices) and `C05b`: **`0.31.0`** today —
"the stored run used 0.22.2; `-U` means you get whatever is newest, at the time of recording."
One line: cell 16 also downloads a 510 MB `experiments.zip` you don't need — you may delete that
line. ▶ The key: W&B *User settings → API keys* and Colab's key icon → a secret named exactly
**`WandB`**, notebook access on (`illustration`; the key drawn as dots). ▶ Cell 34, code then
`recorded` output (`nbB:612-615`, user and team masked): `Appending key for api.wandb.ai to your
netrc file: /root/.netrc`, `Currently logged in as: <W&B user> (<team>)`. ▶ The five training
cells: each calls `wandb.init(project='cheese-app-demo')` → `recorded` banners (`nbB:773-782`:
`Tracking run with wandb version 0.22.2`, `View run at https://wandb.ai/<team>/cheese-app-demo/
runs/…`). V2: the five rows become runs in one project; the shared epoch axis appears. Only
`2_block` draws curves — its recorded "Run history" (`nbB:1009-1022`). **PONDER 2 (6 s)**: "Five
runs in one project, but only one has loss and accuracy curves. What do the other four lack?"
Answer: a callback — only cell 38 passes `callbacks=[WandbCallback(…)]` (the PURPLE pipe; its
`WandbCallback is deprecated` warning, `nbB:782`, is harmless); `wandb.init` alone records the
config and system metrics, never your curves. The two MobileNet runs share one display name,
`mobilenetv2_train_base` (`nbB:1629`): tell runs apart by id. No cell calls `wandb.finish()` —
run it yourself after cell 52 (`extra`). ▶ Cells 55–60 (copy B's table, `nbB:1703-1715` — the
hook's second winner; note `epochs` 10 vs 15 for the fine-tuned row: not a like-for-like
comparison), ▶ cells 64 and 66: no stored output (the instructors didn't run them); the bucket
and project are hard-coded inside cell 13's `upload_experiment` — edit them there. Slide 16 in
one line (Conflict 5): the lecture's screenshot is an earlier year's project; yours says *cheese*.

**S05 · Three lines, and an assignment that goes nowhere (~240) — `s05_config.py` · `ThreeLines`.**
Tracker B4 (held); `lecture_ref(13, "14–15")`. Slide 14 → 15 redrawn: plain training code, then
three lines slide in, tagged with the lecture's call-outs — *start the run* (`wandb.init`),
*watch the model* (a callback in `model.fit`), *finish the run* (`wandb.run.finish()`). Now
notebook B's real cell 38, CODE from the extract (`nbB:696-705`): `wandb.init(project=…)`, then
**`wandb.config = {...}`**, `wandb.run.name = model_name`, `wandb.run.save("test")`.
**PONDER 3 (8 s)**: "After `wandb.config = {…}` and later `wandb.config.update({"execution_time":
…})`, what does the run's config hold?" V3 plays the answer, then the proof, `extra · local
stand-in` (W&B offline mode, today's wandb 0.31.0): `C38:16-17` — **`type(wandb.config): dict`**,
**`the run's config: {}`**; the fix `C38b:16-17` — `Config`, all four keys plus `execution_time`.
One line: `wandb.run.save("test")` uploads files matching `test`; it does not "save the run". The
repo does it right: CODE(package/trainer/task.py: 312-322) `wandb.init(project=…, config={…},
name=model.name)` and (`: 335-338`) `config.update`, `run.finish()`. But the middle line is gone:
CODE(source/model-training-history/88f3374.diff, the `model.fit` hunk) — `-    callbacks=[WandbCallback()],`
(2025-10-15, "removed ca;llback", 51 minutes after the image moved to TF 2.17 / Keras 3 in
`1c03dd5`; the commit doesn't say why). So the repo's runs will have config and system charts and
**no curves** (S12; exercise 1 puts one small callback back).

**S06 · Rent the machine, not the server (~250) — `s06_serverless.py` · `RentTheMachine`.** No
tracker; `lecture_ref(13, "18–24")`. Slides 19 and 21 as a schematic three-entry sidebar
(`illustration`, no screenshot, no logo): Workbench (notebooks), **Training** (jobs — today, the
*Custom jobs* tab), Pipelines (workflows — L15). Slide 22's "serverless training": the hardware is
rented for the training step only, nobody sets up a server, and billing stops when the step ends
— "there *is* a machine; you just don't manage its life" (digest §3.4). GOLD meter drawn on the
job tile, no numbers. V4 steps 1–2 as the plan of part 2: slide 23's *Move code to a Python file*
and *Pass arguments* with the real flag names (Conflict 6: the slide's `epochs=25` is schematic;
`cli.sh` sends `--epochs=2`); slide 24's layers lit on V1 — cockpit packages & uploads & submits,
the bucket holds the code, Vertex runs each job in its own container with hardware chosen per
job (one tile "CPU, RAM", one with a T4). The two facts that drive everything after: the job
**can't see your laptop** (its data comes from the internet — `task.py:96-100`, a GitHub release —
and anything it should keep must be written somewhere durable), and **the image that runs is
Google's, not yours**. **Quick predict (4 s)**: "Your laptop has no GPU and no TensorFlow. Which
machines in this picture will ever import TensorFlow?" → the Colab runtime and the Vertex job's
container; never the cockpit (proved in S09).

**S07 · A project, two keys and a bucket (~290) — `s07_setup.py` · `KeysAndBucket`.** Tracker
C1→C7; `lecture_ref(13, "25")`. ▶ Clone (README:17) → `01`; extras `02` (`b9aee1cc…`, 2025-10-16
— the course pin; the README hasn't moved), `03` (three shell scripts, `cli.py`, `package/`, six
PNGs — console screenshots this video redraws). ▶ Vertex AI API (README:19-21): schematic console
`illustration` ("API enabled"). ▶ GPU quotas (README:23-44), `illustration` with the README's own
labels — filter `Quota: Custom model training`, `Custom model training Nvidia T4 GPUs per region`,
select regions, `EDIT QUOTAS` → new limit → `NEXT` → `SUBMIT REQUEST`; README:43-44 "usually a few
hours … based on how new your account is, you may not be approved". "Today's `cli.sh` runs on CPU,
so you can finish without it; file the request now if you want a GPU later." ▶ `secrets` folder
next to the clone (README:50-58) → `04`, `05`. ▶ Service account `model-trainer`, roles Storage
Admin, AI Platform Admin, Vertex AI Administrator, *Manage keys → JSON*, renamed
`secrets/model-trainer.json` (README:60-64) — `illustration`; extra `06`: the file is there,
tagged `stand-in`. **The sandbox framing**, said here once and plainly (Running example). ▶ Bucket
(README:66-71), `illustration`: `your-bucket-placeholder`; extras `07` (`404 The specified bucket
does not exist` — our placeholder is nobody's) and `08` (the README's `cheese-app-trainer` →
`401 Anonymous caller does not have storage.buckets.get access…` — it exists and belongs to someone
else: bucket names are global, pick your own). GOLD: the bucket stores your tarball (tiny) and
any experiment folders. ▶ W&B key (README:73-81): *User settings → API keys* `illustration` (dots),
then **`export WANDB_KEY=...`** in the **host** terminal → `10` (placeholder; extra `echo
${#WANDB_KEY}` → `40`, "the placeholder's length — the check that matters is that it isn't zero").
**PONDER 4 (6 s)**: "You exported the key, closed the terminal, opened a new one. What does
`echo ${#WANDB_KEY}` print now?" → extra `11`: **`0`** — exported variables live in one shell
(S10 shows what that costs). Part-1 close on V1 (Length and parts).

### Part 2 · Ship it

**S08 · The cockpit that won't build: two one-line fixes (~340) — `s08_build.py` · `TwoFixes`.**
Tracker D1→D2 (+ the two `extra` rows); `lecture_ref(13, "24")` on the cockpit box (the build
itself is tutorial-only, said so). ▶ Edit `docker-shell.sh` lines 8-9 (README:93-94 "[REPLACE WITH
…]") → `20` (sed is our editor; you use yours). Kindly (erratum 3): the README's listing
(README:89-112) is not the real file — bracketed notes on shell lines, a broken continuation at
:110, an arm64 line — edit `docker-shell.sh` itself. CODE(docker-shell.sh: 12-24) briefly: `set -e`
(:3), the amd64 build, `--rm --name model-training-cli`, two mounts, four `-e`, no `-p` (it serves
nothing). ▶ `sh docker-shell.sh` (README:115, from inside `model-training/`) → `21`, cropped: the
step header `[ 2/14] RUN apt-get update && apt-get install -y curl …` (`21:23`), three `Err:` lines
(`21:65-69`, IP tails cropped), `E: Unable to fetch some archives…` (`21:166`), the `Dockerfile:18`
frame (`21:181-187`), `ERROR: failed to build` (`21:188`) — and `set -e` stops the script before
`docker run`. **PONDER 5 (8 s)**: "Every error is a 404 from a Debian mirror — and your internet
works. Which single line of the Dockerfile decides which Debian you get?" Answer: line 2's `FROM`.
`python:3.13-slim-bullseye` is Debian 11; on 2026-10-23 its security mirror lists packages it no
longer serves (they live on `archive.debian.org` now — say "at the time of recording"). ORANGE base
swaps on V1's cockpit. Fix 1, `extra` → `22`: `FROM python:3.13-slim-bookworm`. ▶ again → `23`:
the build passes steps 2–7 and stops at `[ 8/14]` (`23:330`) — `Package google-cloud-sdk is not
available … However the following packages replace it: google-cloud-cli` and `E: Package
'google-cloud-sdk' has no installation candidate` (`23:344-357`, cropped), the `Dockerfile:36`
frame (`23:372-378`). Kindly: Google renamed its apt package; nothing here needs the GKE plugin.
Fix 2, `extra` → `24`: `apt-get install -y google-cloud-cli jq docker-ce`. Extra `25`: **`git
diff --stat`** `2 files changed, 4 insertions(+), 4 deletions(-)` and the Dockerfile hunks — your
two values and the two fixes, nothing else. ▶ third time → `26:1-41`, cropped: `[+] Building
314.2s (19/19) FINISHED` (slow the first time, much slower emulated on Apple Silicon), then the
banner: `Container is running!!!`, **`ERROR: (gcloud.auth.activate-service-account) Unable to read
file [/secrets/model-trainer.json]`** — the honest no-key state ("with your key in place, this line
confirms the service account instead; and note the script carries on regardless — the entrypoint
has no `set -e`"), `Updated property [core/project].`, `Architecture: x86_64`, `Python version:
Python 3.13.17`, `UV version: uv 0.13.5`, the root prompt. One line (erratum 13): "Environment
ready! Virtual environment activated." is printed *before* the activation line — a label, not a
fact (`docker-entrypoint.sh:13` vs `:19`).

**S09 · What goes in the tarball (~300) — `s09_package.py` · `InsideTheTarball`.** Tracker E1→E3;
`lecture_ref(13, "23–24")`. Extras first, inside the cockpit (`26:42-69`): `/secrets` empty (the
sandbox), `your-gcp-project gs://your-bucket-placeholder 40`, `which python gcloud gsutil uv`,
`Google Cloud SDK 590.0.0`, aiplatform `1.120.0`, and **`ModuleNotFoundError: No module named
'tensorflow'`** — V1's cockpit gets its stamp: it submits, it never trains. Extra `27`: 2.59 GB on
disk. ▶ Review `setup.py` — CODE(package/setup.py: 5-13): the only declared dependency is
`wandb==0.15.11` (GREEN); `find_packages()` finds `trainer` because `__init__.py` exists, which is
why `python -m trainer.task` works. TensorFlow, scikit-learn and requests are *assumed* from
Google's image (ORANGE, erratum 12 — S11 proves it). ▶ Review `task.py` — CODE(package/trainer/
task.py: 45-54): the notebook's globals as flags, and **`--wandb_key` defaulting to `"16"`** (S11
pays off); one line each on `:96-100` (the data comes from a GitHub release — the job can't see
your laptop) and `:153` (`wandb.login` runs *after* the data download). V4 step 2: the box,
`setup.py` label, tar, gzip. ▶ `sh package-trainer.sh` (README:127-129, inside the container) →
`30:42-52`: the eight `tar` entries (directory order), gsutil's notice `Google recommends using
Gcloud storage CLI … instead of gsutil` (new, harmless, cropped at the frame), then
**`BucketNotFoundException: 404 gs://your-bucket-placeholder bucket does not exist.`** — our
placeholder bucket; with yours, the object appears (no panel: no source records gsutil's success
lines — "look for `cheese-app-trainer.tar.gz` in your bucket"). CODE(package-trainer.sh: 1-4):
line 4's fixed object name means every upload **overwrites** the last. Extras `30:53-63`:
**4016 bytes**, `tar tzvf` with sizes (`task.py` 10253 …); extra `31`: on the host the tarball is
owned by root (the container wrote it) and git-ignored (`.gitignore:4`). **PONDER 6 (6 s)**: "You
fix a typo in `task.py`. Rebuild the Docker image, re-run `package-trainer.sh`, or both?" → only
`sh package-trainer.sh`: Vertex runs the tarball in the bucket; the image never travels, and
`/app` is mounted so the cockpit already sees your edit. GOLD: the tarball is stored in your bucket
(tiny).

**S10 · One command, and a key inside it (~310) — `s10_submit.py` · `OneCommand`.** Tracker
F1→F3; `lecture_ref(13, "22, 24–25")`. ▶ Review `cli.sh` — CODE(cli.sh: 5-19): a unique
`DISPLAY_NAME` from `openssl rand -hex 6`, `n1-standard-4`, one replica, the **GPU** image on line
9, package and module, `ACCELERATOR_*`, `GCP_REGION`, and `CMDARGS` with `--wandb_key=$WANDB_KEY`
(:19); then CODE(cli.sh: 21-37): the GPU block **commented out**, line 31 swapping the image to
`tf-cpu.2-17.py310`, and the one `gcloud ai custom-jobs create` that runs. Kindly (erratum 4): the
README presents GPU first and CPU as "optional — edit `cli.sh` to not pass the accelerator"
(README:152-154); the script already does (commit `3efb2d5`). README's accelerator list
(README:136-142) may be out of date — check Google's current list. ▶ `sh cli.sh` (README:150) →
`40:42-55`: **`Using endpoint [https://us-central1-aiplatform.googleapis.com/]`** (live), then
`ERROR: (gcloud.ai.custom-jobs.create) You do not currently have an active account selected.` —
the key that never loaded in S08; extra `40:56-62` `gcloud auth list` → `No credentialed
accounts.` With your key, gcloud reports the job as submitted — described, **no panel** (recorded
nowhere). Extra, the security point: **`sh -x cli.sh`** → `40:64-77` (hex cropped; line 77 folded):
the GPU image set, then overridden by `tf-cpu`; the full `--worker-pool-spec`; and
`--args=--model_name=mobilenetv2,--train_base,--epochs=2,--batch_size=32,--wandb_key=PLACEHOLDER_…`
— V5's W&B badge turns RED. **PONDER 7 (8 s)**: "Your W&B key is now part of the job's
arguments. Who can read it later?" → anyone who can view jobs in this project (the job spec keeps
its args), plus your shell history if you typed it inline — use a dedicated key, rotate it at the
end (a Secret Manager version is an exercise). The other way it goes wrong, extra `70` (a terminal
where the key was never exported): `echo ${#WANDB_KEY}` → `0`; the `--args` end in
**`--wandb_key=`** — the job would start, download its data, and fail at login (S11 shows the
message). Fix: `exit`, `export`, `sh docker-shell.sh`; extra `71:34` if the old shell is still
open: `Conflict. The container name "/model-training-cli" is already in use` (id cropped) — exit
that one first. GOLD: from submission until the script exits, the job's VM bills — no amounts;
the Vertex AI pricing page. V4 step 3: the spec card flies.

**S11 · Who submits, who runs (~300) — `s11_identity.py` · `WhoRunsIt`.** Tracker F2 (held,
`extra · local stand-in` captions); `lecture_ref(13, "24")`. V5 in full: the submitter, the runner,
the third badge. **PONDER 8 (8 s)**: "The job `pip install`s your package from your private bucket
— but your key file never left your laptop. How?" Answer: by default the job runs as your
project's Vertex AI service agent, a Google-managed identity that can read buckets in the same
project; your key only proved who *submitted* (digest §3.5; "if the job ever gets a 403 on your
bucket, that's the identity to grant"). Then V4 step 4, the job's first minute, honestly: "we
can't run Vertex here, so we replay its first step locally — tagged" → `80:1-2, 68-70` (cropped):
`Processing /tmp/trainer.tar.gz` … `Successfully installed … cheese-app-trainer-0.0.1 …
wandb-0.15.11` — in a plain `python:3.10` container, not Google's image. `82` (cropped to the
relevant rows): wandb 0.15.11, requests, **no tensorflow, no scikit-learn** — the ORANGE layer
must come from Google's image (it is still served, `09`: `tf-cpu.2-17.py310`, 4.31 GB compressed,
at the time of recording). `83`: `python -m trainer.task --help` → **`No module named
'tensorflow'`** — the trainer can't even print its flags outside a TF image. Then the trainer's
first W&B step (`task.py:153`) with three keys, three outcomes, ProxyError lines cropped: `85` —
the empty key from S10 → **`api_key not configured (no-tty). call wandb.login(key=[your_api_key])`**
(and on Vertex that happens after the data download: minutes you've paid for); `84` — the `"16"`
default → **`API key must be 40 characters long, yours was 2`**; `86` — a 40-character placeholder
→ `Appending key for api.wandb.ai to your netrc file: /root/.netrc`, exit 0. One line, `87`: this
wandb pin accepts exactly 40 characters ("yours was 47"); if your key is a different length, bump
the pin in `setup.py` — we couldn't check today's key format.

**S12 · What the job prints, what W&B can show (~290) — `s12_logs.py` · `WhatTheJobSays`.** Tracker
F4→F5; `lecture_ref(13, "9–10, 15–16, 25")`. ▶ View Jobs (README:156-158, slide 25's link):
Vertex AI → Training → **Custom jobs**, `illustration` — one row, `cheese_training_job_<hex>`, the
README's words "ready to be provisioned to run"; no durations, no numbers (Conflict 8: `cli.sh`
makes a custom job, not a training pipeline). The log, as an `illustration` built **only from the
code's own prints** (`task.py:57-68`, `:94`, `:107`, `:122`, `:148-150`, `:269`, `:308`, `:333`,
`:341`), with values **only** where both notebooks recorded them for the same code (tag `recorded
· notebooks A/B`): `Full size of the dataset: 1156`, `train_x count: 936`, `validate_x count: 104`,
`test_x count: 116`; `Labels: […]` shown twice with the two recorded orders (`nbA:352`,
`nbB:409`) — `os.listdir` has no order and the trainer saves no label map (erratum 9); the model
summary's stray `None` (`print(model.summary())`, `:308`); where `model.fit` runs, a GREY gap "no
recording of this part" — **no epoch lines, no loss, no timings**; then `Training Job Complete`
(`:341`). ▶ View Training Metrics (README:160-163): "you will view the training metrics tracked and
automatically updated" — kindly (erratum 5, Conflict 1): not with this code. V2: the repo run's
row, **from `task.py` only, no dashboard chrome**: project `cheese-training-vertex-ai`, run name
`mobilenetv2_train_base_True` (`:263`, `:321`), config `learning_rate 0.001` (`:274`), `epochs 2`,
`batch_size 32` (`cli.sh:19`), `model_name`, `execution_time …` (`:336`); system charts named as a
category, not drawn with data; curve slots ghost (no callback, `:326-331`). **PONDER 9 (8 s)**,
slide 9's checklist: "Of the seven things a run record should hold, which does this run record?"
Answer, ticked on V2's columns: model + hyperparameters ✓; environment partly (system metrics;
the image tag lives only in `cli.sh`); metrics only `execution_time`; artifacts — logs yes,
**weights no**; code ✗ (no commit), data ✗ (a fixed release zip, an unseeded split), notes ✗. Hook
callback: that is exactly why tables A and B can't be compared. Exercise 1 adds a `LambdaCallback`
(one line here).

**S13 · Three switches for one GPU (~230) — `s13_gpu.py` · `ThreeSwitches`.** Tracker F3 (the
optional CPU step, read in reverse); `lecture_ref(13, "22, 24")`. CODE(cli.sh: 9-14) and (`: 21-27`)
vs (`: 30-37`). V6 in full: accelerator in the worker pool, a `tf-gpu` image, quota in that region;
the T4 lights only when all three agree. The quota console reprise from S07 (`illustration`). Extra
`09`: the prebuilt images are still served — `tf-cpu.2-17.py310`, `tf-gpu.2-17.py310`,
`tf-gpu.2-14.py310` with their layer counts and compressed sizes (at the time of recording).
To switch: uncomment lines 22–27 **and** comment out 30–37 — leave both and you submit two jobs
with the same name (V6 replay). Honest line: "this recording has no GPU quota and no account; the
GPU block runs the same `gcloud ai custom-jobs create` that failed in S10, so there's nothing new
to show — and nothing we'd fake." GOLD: a GPU adds to the job's bill for every minute it is
attached, used or not. **PONDER 10 (6 s)**: "You add `accelerator-type` to the *CPU* block. The job
runs, and its log says `GPU Available:  []`. Why?" → line 31's `tf-cpu` image has no CUDA: the T4
is attached, idle and billed (V6 dark-chip replay; exercise 5).

**S14 · Two GPUs, one model (~300) — `s14_multigpu.py` · `TwoGpusOneModel`.** Tracker G1→G4;
`lecture_ref(13, "26–30")`. V7 opens with slide 27's ladder; "you are here: one machine, two
GPUs". Kindly (Conflict 9): `task.py:60`'s `MirroredStrategy` only *counts* replicas — the
single-GPU trainer builds its model outside any scope, the lecture's one-device case. Slide 28 → 29
as three edits over ▶ Review `task_multi_gpu.py` — CODE(package/trainer/task_multi_gpu.py:
286-301), then (`: 303-321`): *create the strategy*, *scale the batch* (`global_batch_size =
args.batch_size * num_workers` — `num_workers` here counts GPU replicas, not machines), *build and
compile inside `strategy.scope()`*; `model.fit` unchanged. V7's split / all-reduce / mirrored
update. **PONDER 11 (8 s)**: "Two GPUs, `--batch_size=32`, 936 training images. How many steps per
epoch, and how many images does each GPU see per step?" → global batch 64 → **15 steps** (the last
one partial); 32 per GPU per full step (W&B would record `batch_size 32` and `global_batch_size 64`,
`:324-334`). Two caveats: the learning rate stays 0.001 (`:275`) while the batch doubles; and two
GPUs are not twice as fast (start-up, image pull and the download don't shrink). ▶ Review
`cli-multi-gpu.sh` — CODE(cli-multi-gpu.sh: 4-16): `n1-standard-32`, `NVIDIA_TESLA_T4` × 2,
module `trainer.task_multi_gpu`, `--epochs=5`; kindly (erratum 10): it still uses
`tf-gpu.2-14.py310`, an older TensorFlow than `cli.sh`'s 2.17. ▶ Make changes: you need quota for
2 T4s **and** 32 vCPUs of custom training in the region. ▶ `sh cli-multi-gpu.sh` (README:170) →
`50:42-44`: `Using endpoint …`, the same auth error — no fake success. GOLD: the biggest machine of
the lecture — check the pricing page before you press enter. Slide 30 in one line: everything
else (bucket, key, package) was already done; only the launch script changed.

**S15 · The missing model, teardown, recap (~270) — `s15_recap.py` · `Recap`.** `extra ·
clean-up` tracker; `lecture_ref(13, "5–6, 9–10, 21")`. The launcher the README doesn't mention,
brief, `extra` → `60:42-48`: `python cli.py` → **`KeyError: 'GCP_REGION'`** (`cli.py:7` reads a
variable only `cli.sh` sets); after `export GCP_REGION=us-central1`, `60:119`: `DefaultCredentialsError:
File /secrets/model-trainer.json was not found.` — the Python-SDK route, which L15 picks up (it
also sends no `--wandb_key`: S11's `yours was 2`). V4 step 5: the VM dissolves and the trained
weights evaporate — nothing calls `model.save`, `--model-dir` is parsed and ignored (errata 6, 7);
V2's artifacts cell stays "?"; L15 saves the model to a bucket (GREY dashed; exercise 4 does it
today). **Teardown checklist (GOLD)**, below — with extras `90` (`docker ps -a`: nothing left,
`--rm`) and `91` (the images that stay on your disk; console 2.59 GB, at the time of recording).
V1 complete, then unlit. "Test yourself", five questions one at a time with a thumbnail of their
picture (answers in exercises.md) — see Recap questions. Footer cards: exercises.md and the study
guide (`MLOps_Learning · guides/L13-training-workflows.md`). Next, GREY dashed: L14 serves
containers serverlessly; L15 saves this model and chains the steps in Pipelines (slide 21's third
entry). Close on slide 5's dials: hardware rented, and a record that says what you rented it for.

## Word budget

| scene | words | scene | words |
| --- | --- | --- | --- |
| S01 Hook | 220 | S08 TwoFixes | 340 |
| S02 LeversAndRecord | 220 | S09 InsideTheTarball | 300 |
| S03 FolderTracker | 280 | S10 OneCommand | 310 |
| S04 SharedAxis | 290 | S11 WhoRunsIt | 300 |
| S05 ThreeLines | 240 | S12 WhatTheJobSays | 290 |
| S06 RentTheMachine | 250 | S13 ThreeSwitches | 230 |
| S07 KeysAndBucket | 290 | S14 TwoGpusOneModel | 300 |
| | | S15 Recap | 270 |
| **part 1** | **1,790** | **part 2** | **2,340** |

Total ≈ **4,130** words ≈ 23.7 min of narration; typing, outputs, the three builds and the ponder
timers bring it to ~29–31 min.

## Ponder questions (summary)

Eleven timed ponders and one quick predict — about one every 2.7 minutes (AGENTS content gate 3).
Each is answerable from the picture or capture shown just before it.

| # | scene | question (as on the card) | answer (said right after the timer) |
| --- | --- | --- | --- |
| 1 | S03 (8 s) | "The cell sets `validation_percent = 0.2`.\nYet validation is 104 of 1,156.\nWhat did the code actually do?" | Both splits use `test_percent`: 10 % of 1,156 → 116 test, 10 % of 1,040 → 104 validation, 936 train (`nbA:431-447`; digest E4; same in `task.py:134-146`) |
| 2 | S04 (6 s) | "Five runs in one project, but only one\nhas loss and accuracy curves.\nWhat do the other four lack?" | A callback in `model.fit` — only cell 38 passes `WandbCallback`; `wandb.init` records config and system metrics, not curves (`nbB:1009-1022` vs the other runs; digest E15) |
| 3 | S05 (8 s) | "After `wandb.config = {…}` and\n`wandb.config.update(…)`, what does\nthe run's config hold?" | Nothing: `{}` — the assignment rebinds the name to a loose dict (`C38:16-17`); fix `wandb.init(config=…)` (`C38b`) |
| q | S06 (4 s) | "Your laptop has no GPU and no TensorFlow.\nWhich machines here will ever\nimport TensorFlow?" | The Colab runtime and the Vertex job's prebuilt container — never the cockpit (`26:65-69`, shown in S09) |
| 4 | S07 (6 s) | "You exported the key, closed the terminal,\nopened a new one. What does\n`echo ${#WANDB_KEY}` print?" | `0` (`11`): an exported variable lives in that one shell and its children |
| 5 | S08 (8 s) | "Every error is a 404 from a Debian mirror,\nand your internet works. Which line of\nthe Dockerfile picks your Debian?" | Line 2, `FROM python:3.13-slim-bullseye` (Debian 11, whose security pool no longer serves those files); fix → bookworm (`21`, `22`) |
| 6 | S09 (6 s) | "You fix a typo in `task.py`.\nRebuild the image, re-run\n`package-trainer.sh`, or both?" | Only `sh package-trainer.sh`: Vertex installs the tarball from the bucket; your image never travels and `/app` is mounted (digest gotcha 10, exercise 7) |
| 7 | S10 (8 s) | "Your W&B key is now part of the\njob's arguments. Who can read it later?" | Anyone who can view the project's jobs (the spec keeps `--args`), plus your shell history if typed inline; rotate it, use a dedicated key (`40:75`; digest E18, gotcha 14) |
| 8 | S11 (8 s) | "The job installs your package from your\nprivate bucket, but your key never left\nyour laptop. How?" | It runs as your project's Vertex AI service agent (by default), which can read same-project buckets; your key only identified the submitter (digest §3.5) |
| 9 | S12 (8 s) | "Of the seven things a run record\nshould hold, which does this run record?" | Model + hyperparameters yes; environment partly; metrics only `execution_time`; logs yes, weights no; code, data, notes no (SLIDES gap 1; `task.py:313-338`) |
| 10 | S13 (6 s) | "You add `accelerator-type` to the CPU block.\nThe job runs; its log says\n`GPU Available:  []`. Why?" | Line 31's `tf-cpu.2-17.py310` has no CUDA: the T4 is attached, idle and still billed (digest gotcha 8, exercise 5) |
| 11 | S14 (8 s) | "Two GPUs, `--batch_size=32`, 936 training\nimages. Steps per epoch? Images per GPU\nper step?" | Global batch 64 → 15 steps (last one partial); 32 per GPU per full step (`task_multi_gpu.py:293`; digest ponder 3) |

## Recap questions (S15 "Test yourself"; answers in exercises.md)

1. Copies A and B of the same notebook crowned different MobileNets. Name two things neither
   table recorded that you would need before calling the difference real.
2. What travels from your laptop to Vertex AI, which image does it run in, and what never makes
   the trip?
3. After `wandb.config = {...}`, the run's config is `{}`. Why — and what is the one-line fix?
4. Which identity submits the job, which runs it, and where does your W&B key end up?
5. With `MirroredStrategy` on two GPUs, what is split, what is averaged, and what must be created
   inside `strategy.scope()`?

(Digest recap Q3 — "three settings that must agree for a GPU" — and Q6 — "where is the trained
model?" — are asked inside the video as ponder 10 and the S15 beat; SLIDES' added "which strategy
for two machines?" goes to exercises.md.)

## Errata and version drift to state (kindly, with the fix)

1. **The cockpit build fails at step 2 today** (`21`): `python:3.13-slim-bullseye`'s security mirror
   returns 404 for 22 packages its index still lists (on 2026-10-23; the files live on
   `archive.debian.org`). Fix: `Dockerfile:2` → `FROM python:3.13-slim-bookworm` (`22`) (S08).
2. **…and then at line 37** (`23`, word for word, digest gotcha 20): `google-cloud-sdk` has no
   installation candidate — Google renamed the package. Fix: `Dockerfile:37` → `apt-get install -y
   google-cloud-cli jq docker-ce` (`24`); keep `--platform=linux/amd64`. Final `git diff` (`25`)
   (S08).
3. **The README's `docker-shell.sh` listing is not the file** (README:89-112: `[REPLACE …]` notes on
   shell lines, a broken continuation at :110, an arm64 build line, and an HTML comment at :96 —
   **never shown**, it renders a project-id-like string). Edit the real file (S08).
4. **README says GPU, the code runs CPU** (README:132-154 vs `cli.sh:21-37`, commit `3efb2d5`);
   the accelerator list may be out of date (S10, S13).
5. **"Training metrics tracked and automatically updated"** (README:163): the repo's `model.fit`
   has no callback (`88f3374`); W&B gets config, `execution_time`, system metrics and logs only.
   Exercise 1 adds a `LambdaCallback` (S05, S12).
6. **The trained model is never saved** (no `model.save`, no artifact; the VM takes it) (S15).
7. **Dead flags**: `--model-dir`, `--lr` parsed and ignored (`task.py:27-30`, `:274`) (S15, one
   line).
8. **The W&B key travels in `--args`** (`40:75`): visible in the job spec — dedicated key, rotate,
   or Secret Manager (exercise) (S10). The `"16"` default (`task.py:52`) fails wandb's length check
   (`84`); wandb 0.15.11 accepts exactly 40 characters (`86`/`87`) (S11).
9. **Label order is not deterministic** (`task.py:106`; the notebooks printed two orders) and no
   label map is saved (S12).
10. **Multi-GPU uses an older image** (`tf-gpu.2-14.py310`, `cli-multi-gpu.sh:8`; `cli.py:21`) than
    `cli.sh`'s 2.17 (S14).
11. **`cli.py`** (not in the README): `KeyError: 'GCP_REGION'` (`60`); no `--wandb_key` (S15).
12. **Undeclared dependencies**: TensorFlow, scikit-learn, requests come only from Google's image
    (`82`, `83`) (S09, S11).
13. **"Virtual environment activated."** is echoed before the activation (`docker-entrypoint.sh:13`
    vs `:19`) (S08, one line).
14. **Notebook B**: `wandb.config = {...}` drops config and `execution_time` (`C38`); only `2_block`
    has curves; both MobileNet runs share one name; no `wandb.finish()`; a 510 MB download you
    don't need; bucket and project hard-coded in cell 13 (S04, S05).
15. **Both notebooks**: the validation split uses `test_percent` (ponder 1); the table sorts
    formatted strings (E22); copies A and B use different epochs for the same rows (S01, S03, S04).
16. **Slides vs code, one kind line each** (SLIDES Conflicts): the callback the repo dropped (1,
    S05/S12), `wandb.finish` (2, S04), weights as tracked artifacts (3, S15), GPU by default (4,
    S10/S13), slide 16's older project (5, S04), slide 23's schematic arguments (6, S06), the lock
    file pins the cockpit, not the trainer (7, S09: the trainer's environment is the image tag plus
    `setup.py`), custom jobs vs pipelines (8, S12), the counting-only strategy (9, S14).
17. **Version drift, "at the time of recording"**: every number in the Running-example list; gsutil's
    new deprecation notice (`30:51`); `pip install wandb -U` (0.31.0 today vs 0.22.2 recorded);
    unpinned apt packages; the prebuilt images' sizes.

## Costs and teardown

This lecture **bills a Vertex AI custom job for as long as it runs** and stores a little data in
GCS. Colab (free T4, quota-limited) and W&B (free tier) cost nothing here. **No prices on screen**:
GOLD tags name what bills and point to the Vertex AI and Cloud Storage pricing pages.
- **S03, S07, S09**: bucket storage — experiment folders (models of 10–104 MB each, the notebook's
  own `model_size`), the tarball (4 KB).
- **S10**: the job's `n1-standard-4` VM, from provisioning until the script exits. The real risk is
  a job that fails late (after the data download) and gets resubmitted again and again.
- **S13**: a GPU, billed for every minute it is attached, used or not.
- **S14**: `n1-standard-32` + 2 × T4 — the biggest machine of the lecture.
Nothing in this tutorial keeps running after a job ends: no endpoint, no always-on VM, the cockpit
is `--rm`.

Teardown, captured where possible: `docker ps -a` empty (`90`), images left on disk (`91`). The
checklist card (S15):
- `exit` the cockpit (`--rm` removes it); delete the images if you need the disk (`docker image
  rm …`, at the time of recording 2.59 GB for the cockpit);
- Vertex AI → Training → Custom jobs: **nothing `RUNNING` or `PENDING`**; cancel a stuck one with
  *Cancel* or `gcloud ai custom-jobs cancel JOB_ID --region=us-central1` (extra, not in the README;
  shown, not run); if you tried `cli.py`, also check *Training pipelines*;
- in the cockpit, `gsutil rm $GCS_BUCKET_URI/cheese-app-trainer.tar.gz` (extra, shown, not run), or
  delete the bucket; and the `experiment_<ts>/` folders the notebooks uploaded;
- notebook B: `wandb.finish()`; both notebooks: *Runtime → Disconnect and delete runtime*;
- end of term: delete the `model-trainer` key (IAM → Service accounts → Keys) and **rotate your
  W&B key** — it travelled in a job's arguments.

## README commands checklist (for the follow-along review)

Every README and notebook instruction, verbatim, in order.

**Notebooks** (course-site order: A, then B)

| instruction | where | scene |
| --- | --- | --- |
| A: save a copy, GPU runtime; cells 6, 8, 10, 12 | cells 3–12 | S03 (`illustration`; `nbA:115-121`, `:137` recorded) |
| A: download, load, view, metrics | cells 15–21 | S03 (`nbA:352-353`) |
| A: x/y, split, `tf.data` | cells 24–28 | S03 (`nbA:431-447`, ponder 1) |
| A: `create_experiment()`, five models | cells 31–51 | S03 (V2; cell 12 code) |
| A: compare, best model, predict | cells 54–59 | S03 (`nbA:1283-1304`) |
| A: authenticate, edit project/bucket, upload | cells 62–66 | S03 (`nbA:1437-1450`) |
| B: `!pip install -q wandb -U` | cell 5 | S04 (`C05`, `C05b`, stand-in) |
| B: setup, data, pipelines, `create_experiment()` | cells 7–32 | S04 (one line; same as A) |
| B: secret `WandB`; `wandb.login(key=wandb_key)` | cells 33–34 | S04 (`illustration`; `nbB:612-615`) |
| B: five training cells with `wandb.init(project='cheese-app-demo')` | cells 36–52 | S04, S05 (`nbB:773-782`, `:1009-1022`, `:1629`; `C38`, `C38b`) |
| B: `wandb.finish()` (extra) | after 52 | S04 |
| B: compare, best, predict | cells 55–60 | S04 (`nbB:1703-1724`) |
| B: authenticate, `upload_experiment` (edit cell 13) | cells 64, 66 | S04 (no stored output) |

**model-training README @ `b9aee1c`**

| README instruction | README line | scene |
| --- | --- | --- |
| Have Docker; clone the repository | 7-8, 16-17 | S07 (`01`; extras `02`, `03`) |
| Enable Vertex AI API | 19-21 | S07 (`illustration`) |
| GPU quota: filter, T4 per region, regions, EDIT QUOTAS, NEXT, SUBMIT REQUEST | 23-44 | S07 (`illustration`), S13 (reprise) |
| `secrets` folder beside `model-training` | 50-58 | S07 (`04`, `05`) |
| Service account `model-trainer`, three roles, JSON key → `secrets/model-trainer.json` | 60-64 | S07 (`illustration`; `06` stand-in) |
| Bucket `cheese-app-trainer` [REPLACE WITH YOUR BUCKET NAME] | 66-71 | S07 (`illustration`; extras `07`, `08`) |
| W&B → User settings → API keys; `export WANDB_KEY=...` | 73-81 | S07 (`illustration`; `10`; extra `11`) |
| Edit bucket and project in `docker-shell.sh` | 88-94 | S08 (`20`) |
| From inside `model-training`: `sh docker-shell.sh` | 114-116 | S08 (`21`; fixes `22`, `24`; `23`; `25`; `26`) |
| Review `setup.py`, `task.py` | 121-125 | S09 (CODE) |
| `sh package-trainer.sh` | 127-129 | S09 (`30`; extras `31`) |
| Review `cli.sh`; required changes; accelerator and region lists; `sh cli.sh` | 132-150 | S10 (CODE; `40`; extras `40` `sh -x`, `70`, `71`) |
| OPTIONAL: CPU (edit `cli.sh` to drop the accelerator), `sh cli.sh` | 152-154 | S10 (already the default), S13 |
| View Jobs → Custom Jobs | 156-158 | S12 (`illustration`) |
| View Training Metrics → W&B project `cheese-training-vertex-ai` | 160-163 | S12 (V2 from `task.py`; erratum 5) |
| OPTIONAL Multi GPU: review `cli-multi-gpu.sh`, `task_multi_gpu.py`; changes; `sh cli-multi-gpu.sh` | 165-170 | S14 (CODE; `50`) |

## Notes for script and scene authors

- Shared code (`scenes/common.py`, started from L11's): tracker factories `tracker_a` … `tracker_g`
  (+ `tracker_cleanup`) with the step lists above; prompts `P_LAPTOP` (+ `~/model-training`),
  `P_COCKPIT` (`root@<id>:/app#`, ids from each capture, cropped where they'd be read); a
  `notebook_cell(code, output, cell_no)` frame for Colab with the `recorded` tag; tags
  `extra_tag` (variants `extra · local stand-in`, `extra · clean-up`), `illustration_tag`,
  `recorded_tag`, `your_turn`, the GOLD `cost_tag` (text only, never a number). Set-piece classes:
  `TrainingMap` (V1, persistent state across scenes), `RunLedger` (V2), `ConfigBinding` (V3),
  `TarballTrip` (V4), `ThreeBadges` (V5), `GpuSwitchboard` (V6), `MirroredReplicas` (V7). **Never
  reuse a scene class name** (`video.yaml`) for a helper.
- **The sandbox framing is load-bearing**: once, in S07; afterwards every failure is the lesson,
  every success is `recorded` + source, every stand-in is tagged. Never imply a failure surprised
  us; never show the placeholder key's content.
- **What may show values**: notebook outputs (recorded, with their cell); code constants and the
  args `cli.sh` sends; live captures. **What may not**: any Vertex job line beyond the code's own
  print statements and the two recorded counts; any W&B dashboard value other than notebook B's
  stored output; any epoch, loss, timing, accuracy or price for the repo trainer; any key length
  claim for a real W&B key; the `Currently logged in as` line as job output.
- `istep` captures (`26`, `30`, `40`, `50`, `60`, `70`) hold whole sessions: pick line ranges per
  typed command (ranges above). Tracebacks: first line, `…`, last two lines. `21` (189 lines) and
  `23` (380 lines): only the ranges named in S08. `80`: lines 1–2 and 68–70, the install line
  cropped at the frame. `40:77` and `30:51` are long: fold with `wrap` or crop from the meaningful
  phrase on.
- `gsutil cp`'s success, `gcloud ai custom-jobs create`'s success, the console's job page and the
  W&B pages: **no output panels**; describe what to look for.
- Redraw every lecture diagram in series style; never slide images, the README's six PNGs, console
  or W&B screenshots, logos, the slide-31 photo. One `lecture_ref` per scene as assigned.
- Chinese glossary heads-up: experiment tracking (实验追踪), run, config, callback, W&B / Weights &
  Biases, sweep (not used), project, entity, Vertex AI, custom job, worker pool, prebuilt container,
  accelerator, quota, region, service account, service agent, tarball, package, `setup.py`,
  replica, all-reduce, MirroredStrategy, strategy scope, global batch, data parallelism (数据并行),
  serverless (无服务器) — the code words stay English per the `i18n` glossary conventions.

## Things never to do on screen

Series rules:
- No slide images, console or product screenshots (GCP console, W&B, Colab), Google/GCP/W&B logos,
  memes or the cat: redraw the idea, cite slides via `lecture_ref`; the console, W&B and Colab are
  schematic `illustration`s with README / notebook values and **no invented numbers**.
- No real person's name, e-mail or W&B user/team on screen (placeholders above); no hand-typed
  output: every terminal line comes from `assets/terminal/`, every notebook line from
  `assets/source/colab/`; `recorded` panels name their source; stand-in panels are tagged so.
- No command spelled differently from the README (the `sed` edits in `20`/`22`/`24` are editor
  actions, marked `extra` / "update the file").

Lecture-specific:
- **No prices**, no per-hour figures, no "cents"; never a training time, epoch line, loss value or
  accuracy for the repo trainer's Vertex run; no fake `JOB_STATE_SUCCEEDED`, no fake GPU success.
- Never a real-looking W&B key or JSON key (dots, or the placeholder); never `README.md:96`'s HTML
  comment; never the relay IP, ProxyError lines, container ids or the job name's hex.
- Never say the cockpit trains, that your Docker image runs on Vertex, that `wandb.init` logs
  curves, that serverless means "no machine", that two GPUs halve the time, or that the trained
  model is saved anywhere.
- Never claim the job prints a "logged in" line, never state today's W&B key length, never present
  the stand-ins' output as Vertex's.

## Left for exercises.md (not in the video)

Digest exercises 1 (a `LambdaCallback`, predict the charts), 2 (the `no-tty` failure in full and a
guard line for `cli.sh`), 3 (fix the split, predict 832/208/116 and 26 steps), 4 (save the model
and the label map to `--model-dir`; optional W&B artifact), 5 (CPU image + accelerator), 6
(`strategy.scope()`, linear scaling, wall-clock), 7 (edited code vs what ran); the W&B key via
Secret Manager; `pip install ./package` on Python 3.13 fails at `pathtools`/`imp` (`60:122-178`) —
why the trainer is never installed in the cockpit; `cli.py` made to work (`export GCP_REGION`, a
key, `sync=False` semantics, training pipelines vs custom jobs); `MultiWorkerMirroredStrategy` and
the second worker pool; the loss-near-100 L1-penalty estimate (digest §3.8 — not shown in the video
because no repo run records a loss); notebook E13 (preprocessing mismatch), E16 (mushroom
`experiments.zip`), E10/E11 (legacy Keras imports); BatchNorm with `--train_base` (digest §3.8);
slide 12's tool comparison beyond one sentence; digest recap Q1 (seven items) in full.
