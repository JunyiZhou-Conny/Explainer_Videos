# L13 lecture slides — Advanced Training Workflows: experiment tracking (W&B), multi-GPU, serverless training (Vertex AI)

**Provenance.** One deck: `Lecture13_L13_advanced_training_workflows.pdf` (deck name `L13_advanced_training_workflows`), 31 slides, AC215/E115, Pavlos Protopapas, SEAS/Harvard. These are the instructor's lecture slides (PDF), provided by the student for study; the PDFs are not in this repository; slide numbers are PDF page numbers. Everything below is a digest in our own words, made from the extracted slide text and from reading every slide image (the contact sheets and the single pages, which are small 40 dpi renders, so tiny screenshot text is marked as uncertain where it matters). The tutorial side is documented in [`digest.md`](digest.md); "tutorial" and "repo" below mean `dlops-io/model-training` and its two Colab notebooks as recorded there.

## Outline

The deck repeats a six-item agenda slide as a section divider, with the current item in bold. Sections 3 and 5 (the tutorials) have no divider of their own; each is a single slide at the end of the section before it.

- **Slides 1–3 · opening.** Title (1), announcements (2), agenda (3).
- **Slides 4–6 · 1. Recap.** Divider (4); the three levers for better deep learning (5); Cheese App roadmap with today's work boxed (6).
- **Slides 7–16 · 2. Experiment tracking.** Divider (7); why it matters (8); what to track (9); where each item is already tracked, and the gap (10); the case for automation (11); tool comparison (12); what W&B is (13); plain Keras training code (14); the same code with W&B added (15); W&B dashboard screenshot (16).
- **Slide 17 · 3. Tutorial: experiment tracking.** Two Colab notebooks.
- **Slides 18–24 · 4. Vertex AI, serverless training.** Divider (18); what Vertex AI is (19); console dashboard screenshot (20); console sidebar map (21); what serverless training is (22); step 1, notebook to Python file (23); steps 2–3, package, upload, run jobs (24).
- **Slide 25 · 5. Tutorial: serverless training.** Steps and links.
- **Slides 26–30 · 6. Multi GPU training.** Divider (26); three kinds of distribution and their TensorFlow strategies (27); plain training code again (28); the multi-GPU version (29); multi-GPU tutorial steps (30).
- **Slide 31 · close.** "THANK YOU" with a photo of a cat.

## Key ideas

1. **Three levers make deep learning better: more data, better or faster models, faster hardware.** Data means the whole pipeline (extract, transform, label, version, store, process, feed to training); models means state-of-the-art architectures, transfer learning, distillation, compression; hardware means scaled data processing, GPUs/TPUs and multi-GPU server training. This lecture works mainly on the hardware lever, plus the bookkeeping that lets you compare models. *Slide 5.*
2. **Experiment tracking belongs at the very start of the project.** On the Cheese App roadmap (POC → Prototype → MVP) the lecture boxes "Setup Experiment Tracking" together with "Build Baseline Models", right after data collection and before "Build Better Models" and "ML Workflow". *Slide 6.*
3. **Tracking pays off in five ways:** organisation, reproducibility, automatic logging, collaboration, and accountability (being able to say exactly what produced a model's result, good or bad). *Slide 8.*
4. **A complete record of a run has seven parts:** environment (Python, dependencies, hardware), code (scripts and configs), data (version, splits, preprocessing), model (architecture, hyperparameters), metrics, artifacts (weights, logs, sample predictions) and free-form notes. *Slide 9.*
5. **Most of that already has a home; weights, metrics and logs do not.** Code lives in GitHub, data in a versioning system (DVC or GCS buckets), environments in `pyproject.toml`/`uv.lock`; the row for model weights, metrics and logs is a "?". Recording those by hand is messy and gets forgotten, so it should be automatic. *Slides 10–11.*
6. **Several trackers exist; the course uses Weights & Biases.** W&B (hosted, easy UI), MLflow (open source, can be self-hosted, suits private infrastructure), Comet (comparison and team dashboards), Neptune (metadata store, flexible APIs). W&B is chosen for simplicity, visuals and its Keras/TensorFlow and PyTorch integrations; it logs hyperparameters, metrics, model versions and system performance, and has a free tier for education. *Slides 12–13.*
7. **Adding W&B to a Keras script is three small edits:** start a run before training, pass a W&B callback to `model.fit` so the model is monitored, and finish the run afterwards. The payoff is a dashboard where every run's curves (loss, accuracy, validation loss and accuracy) sit on shared axes. *Slides 14–16.* (Tutorial check: the current repo trainer has no callback in `model.fit`, so its runs show config and system charts but no loss/accuracy curves; see `digest.md` §3.1 and B14.)
8. **Vertex AI is Google Cloud's single ML platform** that joins data engineering, data science and ML engineering workflows (deploy, monitor, automate) so a team uses one toolset. In its console, notebooks live under Workbench, training under Training ("training pipelines and jobs"), and ML workflows under Pipelines. *Slides 19–21.*
9. **Serverless training means you rent the GPU only for the training step.** Jobs run on demand, nobody sets up a server, and you stop paying when the step ends, which lowers cost. *Slide 22.*
10. **Getting from notebook to cloud job is three steps.** (1) Move the notebook code into a Python file whose choices (which model, epochs, batch size) arrive as arguments; (2) package the files into a `.tar.gz` and upload it to a GCS bucket; (3) from a "Model Trainer CLI" container, create training jobs on Vertex AI, each a container with its own CPU/RAM and optionally a GPU. *Slides 23–24.*
11. **The serverless tutorial is four actions:** create a bucket for the packaged code, get a W&B API key, package and upload, create jobs in Vertex AI; then watch the jobs in the Vertex AI console and the metrics on wandb.ai. *Slide 25.*
12. **Distribution comes in three shapes, each with a TensorFlow strategy:** one machine with one GPU (One Device Strategy), one machine with several GPUs (Mirrored Strategy), several machines with several GPUs (Multi Worker Mirrored Strategy). You organise the code around the chosen strategy and then train as usual. *Slide 27.*
13. **Going multi-GPU changes three things in the training code:** create the strategy, multiply the batch size by the number of replicas so each GPU still gets the per-device batch, and build and compile the model inside the strategy's scope. `model.fit` itself is unchanged. *Slides 28–29.*
14. **Multi-GPU serverless training reuses the whole serverless setup;** only the job submission changes, to the `cli-multi-gpu.sh` script. *Slide 30.*

## Diagrams

- **Slide 5 · "The 3 components for better Deep Learning".** Three coloured column headers side by side, each with an icon: blue "More Data", green "Better/Faster Models", red "Faster Hardware", each with a bullet list underneath (contents in key idea 1). For: framing the lecture as a hardware-lever lecture. Re-draw as three pillars or three dials, then light up the third.
- **Slide 6 · Cheese App status (Gantt-style roadmap).** A long light-blue arrow across the top labelled POC, Prototype, MVP left to right, with dashed vertical lines marking the phase boundaries. Below, horizontal bars in pastel colours: "Design Cheese App" spans POC and Prototype; "Data Collection" sits in POC; "Setup Experiment Tracking" and "Build Baseline Models" are staggered at the POC/Prototype boundary and enclosed together in a **red dashed box** (today's work); "Build Better Models" and "ML Workflow" sit in Prototype; "Build Cheese App" in MVP; "Deployment, Scaling & Automation" stretches from mid-Prototype to the end of MVP. For: placing L13 in the project timeline.
- **Slide 10 · "Where Do We Track What?" table.** Two columns, Item → Where it's tracked: code/scripts → GitHub repository; data and versions → data versioning (DVC, GCS buckets); environments and configs → `pyproject.toml`, `uv.lock` in GitHub; model weights, metrics, logs → "?". For: showing the one empty cell an experiment tracker fills. Re-draw as four rows that each snap into a home, with the last row left hanging until a W&B box catches it.
- **Slides 14 → 15 · annotated code diff (plain Keras → Keras + W&B).** Slide 14 is the baseline: three blocks commented `# Training Params`, `# Data`/`# Model`, `# Train`. Slide 15 is the same code with three insertions, each tied by an arrow (two curved, the last straight) to a coloured call-out on the right: blue "Initialize wandb run" → the `wandb.init(...)` line before training; green "Add a callback to monitor model" → `callbacks=[WandbCallback()]` inside `model.fit`; red "Let wandb know to finish the run" → `wandb.run.finish()` after training. For: showing that tracking is a thin wrapper around unchanged training code. Re-draw as the slide-14 code with three lines sliding in, each tagged start / watch / close.
- **Slide 16 · W&B workspace screenshot.** Left panel: a list of four runs with coloured dots (names look like `tfhub_mobilenetv2…` and `mobilenetv2_train_…`; too small to read reliably). Main area: a "Charts" grid of five line plots titled loss, epoch, val_accuracy, accuracy, val_loss, each with a four-run legend and an x-axis of steps 0–14 (some lines overlap, and two runs stop near step 9, so fewer than four lines are distinct in the loss, val_loss and epoch panels); accuracy curves rise and flatten, loss curves fall. The breadcrumb appears to show a project from an earlier app demo, not the cheese project (uncertain at this resolution). For: what "automatic" tracking looks like: runs as rows, metrics as overlaid curves. Re-draw from our own runs or as a stylised runs table plus overlaid curves.
- **Slide 20 · Vertex AI console dashboard (screenshot).** Google Cloud console with the Vertex AI left sidebar and a Dashboard of "Get started" and "Tutorials" panels and tiles (Vertex AI Studio, Model Garden, Colab Enterprise, Prepare Data, Model Development, Deploy & Use). For: orientation only.
- **Slide 21 · Vertex AI console map (annotated screenshot).** The console's left sidebar with three items outlined in red, each linked by a long arrow to a coloured label on the right: Workbench (under the Notebooks group) ← green "JupyterLab notebooks"; Training (under Model development) ← pink "Training pipelines and jobs"; Pipelines (under Deploy and use) ← blue "Build ML Workflow". For: which part of the console serves which stage. Re-draw as a three-entry sidebar with arrows to "notebooks / training jobs / workflows"; L13 uses the middle one, L15 the third.
- **Slide 23 · Step 1, "Move Code to Python File".** Two code panels joined by a thick green arrow. Left, "Notebook" (Colab icon): `get_dataset`, `get_model_1`, `get_model_2` definitions, then data, a hard-wired `model_1 = build_model_1(...)`, and `model_1.fit(...)`. Right, "Python File" (Python icon): the same function definitions, but the model line has become a generic `model = ...` and training is `model.fit(...)`. Under the right panel, "Pass Arguments:" with three red arrows pushing up into the file: `model=model_1`, `epochs=25`, `batch_size=32`. For: the notebook's hard-coded choices become command-line arguments, so one file can train any variant. Re-draw as values peeling off the notebook and re-entering the file from below as flags.
- **Slide 24 · Steps 2–3, the serverless training pipeline (the lecture's central mechanism).** Left to right with green arrows: Notebook thumbnail → Python File thumbnail → "Packaged Python files" (a TAR.GZ document icon) → a long arrow into a dashed box labelled **GCP**. Inside GCP, top: a "GCS Bucket" holding the TAR.GZ; a green arrow runs down from the bucket into a "Vertex AI" panel containing three "Job" tiles, each a "Container" box with a hardware label under it: "CPU, RAM, GPU", "CPU, RAM, GPU", "CPU, RAM" (the third has no GPU). Bottom left: a green box "Model Trainer CLI Container" with two dark arrows up into the packaging arrow and the upload arrow (it does both), and a grey arrow right to the Vertex AI jobs. Red step badges: "2 Package & Upload to GCP" (top), "3 Create & Run Training Jobs" (bottom). For: who does what. Your local CLI container only packages, uploads and submits; the bucket holds the code; Vertex AI runs each job in its own container on hardware chosen per job. Re-draw in three layers: laptop (CLI container), storage (bucket), compute (job containers that appear, run and vanish, with a GPU chip per job only where requested).
- **Slides 28 → 29 · annotated code diff (single-GPU → multi-GPU).** Slide 28 repeats the baseline code from slide 14. Slide 29 adds three call-outs with curved arrows: blue "Create distribution Strategy" → `strategy = tf.distribute.MirroredStrategy()` (followed by `num_workers = strategy.num_replicas_in_sync`); green "Adjust dataset batch size" → the `batch_size=batch_size * num_workers` argument of `get_dataset`, which is also printed in red; red "Create & Compile model in strategy scope" → `with strategy.scope():` with `build_model` indented under it. `model.fit` is untouched. For: the three edits that turn a script into a data-parallel one. Re-draw as the slide-28 code with three lines sliding in, then cut to two GPUs each receiving half of the enlarged batch.

## Terms the lecture uses

- **"The 3 components for better Deep Learning"**, "More Data", "Better/Faster Models", "Faster Hardware", "Multi GPU Server Training" (slide 5).
- **"Cheese App"** and its phases **"POC"**, **"Prototype"**, **"MVP"**; bars "Setup Experiment Tracking", "Build Baseline Models", "Build Better Models", "ML Workflow", "Deployment, Scaling & Automation" (slide 6).
- **"Experiment Tracking"** (slides 3, 7–17); the five benefits **Organization, Reproducibility, Logging, Collaboration, Accountability** (slide 8); the seven tracked items **Environment, Code, Data, Model, Metrics, Artifacts, Notes** (slide 9). The lecture's "Artifacts" means weights, logs and sample predictions in general, not specifically W&B's versioned "Artifact" objects.
- **"Weights & Biases (W&B)"** (slides 12–13; slide 11 writes "Weights & Biases" without the abbreviation), **"WandB"** (slides 15–16), lowercase **"wandb run"** (slide 15), and **"Weights & Bias"** (sic, slides 17, 25, 30). The tutorial README writes only "WandB" (e.g. section `#get-wandb-account-api-key`).
- **"run"**, **"callback"** ("Add a callback to monitor model", slide 15).
- Tool names **MLflow, Comet, Neptune** (slide 12).
- **"Vertex AI: Google's Unified ML Platform"**; its three parts **"Data Engineering"**, **"Data Science"**, **"ML Engineering Workflows"** (slide 19).
- Console labels **"JupyterLab notebooks"** (the Workbench item), **"Training pipelines and jobs"** (Training), **"Build ML Workflow"** (Pipelines) (slide 21). Slide 25's "View Training Jobs" link and the README's "View Jobs in Vertex AI" step both point at Training → **Custom jobs**; `cli.sh` creates a custom job, and only the unused SDK launcher `cli.py` creates a *training pipeline* (`digest.md` B12, B16).
- **"Serverless Training"**, executed "on an as-need basis" (slide 22).
- **"Move Code to Python File"**, **"Pass Arguments"** (slide 23); **"Package & Upload to GCP"**, **"Packaged Python files"**, **"GCS Bucket"**, **"Model Trainer CLI Container"**, **"Create & Run Training Jobs"**, **"Job"** / **"Container"** (slide 24). Repo names for the same things: the local image and container are `model-training-cli` (the service account is `model-trainer`); the package is `trainer.tar.gz`, uploaded as `cheese-app-trainer.tar.gz`; a job is a Vertex AI **custom job** with a **worker pool**, and its container is one of Google's **prebuilt TensorFlow training images** (`tf-cpu.2-17.py310` etc.), not an image you build (`digest.md` §3.3–3.4).
- **"distributed training"**, **"One Device Strategy"**, **"Mirrored Strategy"**, **"Multi Worker Mirrored Strategy"** (slide 27); **"distribution Strategy"**, **"strategy scope"** (slide 29). The repo uses only `MirroredStrategy`.
- **`num_workers`** (slide 29) is the number of GPU *replicas* on one machine (`num_replicas_in_sync`), not machines; in "Multi Worker Mirrored Strategy" a *worker* is a machine. The repo keeps the slide's variable name and calls the product `global_batch_size` (`digest.md` §3.7).
- **"Multi GPU Training"** (slides 3, 26–27); **"multi-GPU Serverless Training"** (slide 30). The README section is "OPTIONAL: Multi GPU Training" (`#optional-multi-gpu-training`).

## Commands and code on the slides

Slides 14 and 28 (identical baseline):

```python
learning_rate = 0.001
batch_size = 32
epochs = 10
train_data, validation_data = get_dataset(...)
model = build_model(...)
training_results = model.fit(...)
```

Slide 15 (the W&B additions):

```python
wandb.init(...)
training_results = model.fit(...,callbacks=[WandbCallback()])
wandb.run.finish()
```

Slide 23 (notebook vs Python file):

```python
def get_dataset():
def get_model_1():
def get_model_2():
train_data, val_data = get_dataset(...)
model_1 = build_model_1(...)        # notebook side
training_results = model_1.fit(...)  # notebook side
model = ...                          # Python-file side
training_results = model.fit(...)    # Python-file side
```

Arguments shown: `model=model_1`, `epochs=25`, `batch_size=32`. (The notebook panel defines `get_model_1` but calls `build_model_1`; the slide is schematic.)

Slide 29 (multi-GPU):

```python
strategy = tf.distribute.MirroredStrategy()
num_workers = strategy.num_replicas_in_sync
train_data, validation_data = get_dataset(...,batch_size=batch_size * num_workers)
with strategy.scope():
      model = build_model(...)
training_results = model.fit(...)
```

Slide 30: `cli-multi-gpu.sh`. Slide 10: `pyproject.toml`, `uv.lock`. Slide 2: staff account `@ac215harvard`.

How these compare with the tutorial (from `digest.md`): the repo's single-GPU trainer calls `wandb.login`, `wandb.init(project=..., config=..., name=...)` and `wandb.run.finish()` but passes **no callback** (removed in commit `88f3374`); notebook B uses `WandbCallback(save_graph=False, save_model=False)` in one cell and prints a deprecation warning. The repo's arguments are `--model_name=mobilenetv2 --train_base --epochs=2 --batch_size=32 --wandb_key=...` (`cli.sh`), not the slide's `epochs=25`. The slide-29 pattern matches `task_multi_gpu.py` closely, which also builds the optimizer and calls `compile` inside the scope.

## What the lecture stresses

- **Manual tracking fails.** It is messy and error-prone, people forget model versions, metrics or configs, and only automation keeps experiments consistent (slide 11).
- **Know what produced a result** ("Accountability"), good or bad; be able to repeat it and trust it ("Reproducibility") (slide 8).
- **Track all seven things**, including the environment and hardware and free-form notes, not just metrics (slide 9).
- **Weights, metrics and logs are the gap** that GitHub, data versioning and lock files leave open (slide 10, bottom note).
- **Pick a tracker to fit the setting:** hosted W&B for ease, MLflow when you need self-hosted or private infrastructure (slide 12).
- **Set tracking up early**, alongside the baseline models, not after the good model exists (slide 6).
- **Close every run** ("Let wandb know to finish the run", slide 15).
- **Pay for GPUs only during training:** serverless training gives GPU hardware only for the training step, needs no server setup, and lowers cost (slide 22).
- **Parametrise before you package:** a notebook with hard-coded model choices becomes a Python file whose model, epochs and batch size are arguments (slide 23).
- **Hardware is chosen per job:** the slide-24 jobs differ, two with a GPU and one with CPU and RAM only (slide 24).
- **Distribution is mostly organisation, not new training code:** pick the strategy for your hardware shape, organise the code around it, then "Train as usual" (slide 27).
- **Two multi-GPU rules:** scale the dataset batch by the number of replicas, and create and compile the model inside the strategy scope (slide 29).
- **Reuse the serverless setup for multi-GPU:** slide 30 greys out bucket, key and packaging as already done, leaving only the job-creation step (slide 30).

## Pointers

- **Milestone 2** due on the day of the lecture; add the staff GitHub account `@ac215harvard` as a collaborator (see the Ed post). **Milestone 3** is the midterm presentations on **10/28** (slide 2). The tutorial digest notes that Milestone 3 asks for experiment tracking with W&B or an equivalent and for serverless training on Vertex AI (`digest.md`, "Milestone 3").
- Data versioning (DVC, GCS buckets) is flagged "[MORE ON THIS LATER]" (slide 10). In the tutorial, the trainer does not use versioned data; it downloads a fixed GitHub release zip (`digest.md`, L11 note).
- **Tutorial: Experiment Tracking**, two Colab notebooks (slide 17): "Explore models for cheese classifications" (`https://colab.research.google.com/drive/1h6xRhjILxaUosXlZ5ZC1NZbP0AOHALTl?usp=sharing`, the tutorial's Notebook A) and "Experiment Tracking using Weights & Bias" (`https://colab.research.google.com/drive/1aAE5vR9r6Syh4heZboDbQNZS048VToxS?usp=sharing`, Notebook B).
- **Vertex AI console:** `https://console.cloud.google.com/vertex-ai` (slide 20).
- **Tutorial: Serverless Training** (slide 25, with a QR code): repo `https://github.com/dlops-io/model-training`; training jobs page `https://console.cloud.google.com/vertex-ai/training/custom-jobs`; W&B home `https://wandb.ai/home`.
- **Tutorial: Serverless Training, multi-GPU** (slide 30, with a QR code): `https://github.com/dlops-io/model-training?tab=readme-ov-file#optional-multi-gpu-training`, submitting with `cli-multi-gpu.sh`.
- **Next steps on the roadmap:** "Build Better Models", "ML Workflow" (Vertex AI Pipelines, slide 21's "Build ML Workflow"), then "Build Cheese App" and "Deployment, Scaling & Automation" (slide 6).

## This video and the slides

**Basis.** The video is not scripted yet. This folder has no `BRIEF.md`, `script.md`, `ASSETS.md` or `assets/terminal/`. The map below therefore uses the nine planned chapters in [`digest.md`](digest.md) §8, the study guide (`MLOps_Learning/guides/L13-training-workflows.md`) and every slide: the extracted text, all four contact sheets, and slides 16 and 24 upscaled from the single pages. With no captures yet, "what the tutorial does today" means the repo at `b9aee1c` as verified in `digest.md` on 2026-10-13. When `assets/terminal/` and `ASSETS.md` exist, re-check the Conflicts against them. If they disagree, the captures win.

**A closer reading of slide 16** (from an upscaled 40 dpi render, so the names are likely, not certain). The breadcrumb most likely reads `mushroom-app-demo`. The run legends read like `tfhub_mobilenetv2_train_base_False`, `mobilenetv2_train_base_True` and `mobilenetv2_train_base_False`. The loss and val_loss panels have a 0–100 axis: the top curve starts just above 100 and falls to about 70 over 15 steps, while accuracy climbs to about 0.8–0.9. That is the same "loss ≈ 100 while accuracy rises" pattern that `digest.md` §3.8 explains as the L1 penalty on the classifier head.

### 1. Map: planned chapters ↔ slides

| # | Planned chapter (`digest.md` §8) | Slides on the same ground | Relation |
|---|---|---|---|
| 1 | Five models, one question (3 min) | 6, 8, 11 | Same concept. The lecture makes the case for tracking, and the tutorial applies it with notebook A's five runs. |
| 2 | Experiment tracking, by hand and by W&B (4 min) | 9–17 | Same concept, and the tutorial applies it. Notebook A is the manual way of slides 10–11, notebook B is slides 13–16, and slide 17 is the tutorial itself. |
| 3 | Notebook → package (4 min) | 23, 24 (step 2, left half) | Same concept. The repo applies it with `argparse` flags, `setup.py` and `package-trainer.sh`. |
| 4 | The cockpit container (3 min) | 24 (only the "Model Trainer CLI Container" box) | Mostly tutorial-only. The lecture names the box. Bind mounts, the secrets folder and env vars come from the repo, and the 2026 Dockerfile fix from the digest (§6, item 20). |
| 5 | Ship it: package and submit (5 min) | 19–22, 24, 25 | Same concept. The tutorial applies it with `sh package-trainer.sh`, `sh cli.sh` and the Custom jobs page. |
| 6 | Reading the logs and W&B (4 min) | 15–16, 25 ("View Training Jobs", "View Experiment Metrics") | The tutorial applies it, with conflicts: today's runs show no metric curves (Conflicts 1, 5). |
| 7 | GPUs: type, image, quota, region (3 min) | 22, 24 (the per-job "CPU, RAM, GPU" vs "CPU, RAM" labels) | Mostly tutorial-only. The lecture shows that hardware is chosen per job. Quota, region and the `tf-gpu` image come from the repo. |
| 8 | Two GPUs, one model (4 min) | 26–30 | Same concept. The tutorial applies it with `task_multi_gpu.py` and `cli-multi-gpu.sh`. |
| 9 | What's still missing (2 min) | 6 (next bars), 9–10 (artifacts, the "?" row), 21 (Pipelines) | The lecture frames it, but the content is tutorial-only: the model is never saved, and L15 adds the save. |
| — | not in the plan | 1–5, 7, 18, 31 | Lecture-only: title, milestones, agenda and dividers, the three levers, and the close. Slides 12 and 19–20 fall inside the ch2 and ch5 ranges, but the plan does not cover their content (the tool comparison, the Vertex AI overview and console home page); divider 26 opens the ch8 range. |

### 2. Already in common

| # | Concept | Chapter ↔ slides | Does the video's framing agree with the lecture's? |
|---|---|---|---|
| 1 | Track runs so you know what produced a result and can repeat it | ch1 ↔ 8, 11 | Yes. The hook ("which settings produced the best one … could you re-run it") asks the lecture's *Accountability* and *Reproducibility* as questions. |
| 2 | Manual tracking is error-prone, so automate it | ch2 ↔ 10–11 | Yes, and the tutorial stages it literally: notebook A's `experiment_<ts>/` folder of JSON files is the manual way, and notebook B's W&B is the automatic one. |
| 3 | What a run record holds | ch2 ↔ 9 | It agrees in spirit but is coarser. The plan's "config + metrics + artifacts + environment" (four items) folds code, data and notes away, and recap question 1 asks for "four things". The lecture lists seven. See Proposals. |
| 4 | Why W&B, and what it logs | ch2 ↔ 12–13 | Yes on the choice of tool. "Automatically logs … Metrics" holds only with a callback or `wandb.log`, which `digest.md` §3.1 already flags as a misconception (Conflict 1). |
| 5 | The run lifecycle: start, monitor, finish | ch2, ch6 ↔ 14–15 | Yes on `wandb.init` → `model.fit` → `wandb.run.finish()`. Like the slide, the repo starts the run after the data and model are built. Only the middle line (the callback) differs (Conflict 1). |
| 6 | Runs as rows, metrics as overlaid curves | ch2, ch6 ↔ 16 | Yes. The plan's W&B runs table, where one row "expands into charts" (§8; §3.1 has each row unfold into its loss curve), is the slide-16 view. Today's repo run lacks the curves (Conflicts 1, 5). |
| 7 | Serverless training: runs on demand, you pay only for the training step, there is no server to set up | ch5 ↔ 22 | Yes. The digest (§3.4) adds a useful correction: "serverless" still means a VM, you just don't manage it. |
| 8 | A notebook becomes a Python file whose choices arrive as arguments | ch3 ↔ 23 | Yes, closely. The plan's "numbers peel into `--flags`" (§8 ch3) is the slide's "Pass Arguments" arrows. The plan goes one step further, to a pip-installable package. |
| 9 | Package and upload to a bucket. A local CLI container submits the job, and Vertex AI runs each job in its own container | ch3–5 ↔ 24–25 | Yes. The plan's "cockpit" is the lecture's "Model Trainer CLI Container". The plan adds what the slide leaves implicit: the job container is Google's prebuilt TF image, not your image. |
| 10 | Hardware is chosen per job | ch7 ↔ 24 | Yes. Slide 24's GPU and no-GPU jobs are the plan's accelerator switch. The plan adds the image and the regional quota, which must agree with it. |
| 11 | Three edits make a script data-parallel: create a strategy, use a global batch, build and compile the model in its scope; `fit` stays the same | ch8 ↔ 28–29 | Yes, line for line. `task_multi_gpu.py` keeps the slide's `num_workers` name and `batch_size * num_workers`. The slide says nothing about the learning rate, and the repo does not scale it. |
| 12 | Multi-GPU reuses the serverless setup, and only the launch script changes | ch8 ↔ 30 | Yes (`sh cli-multi-gpu.sh`). The digest (§2, B15) adds the quota the slide does not mention: 2 × T4 plus 32 vCPUs of custom training. |

### 3. Gaps (ranked by value to a student doing the tutorial)

1. **The record checklist as an audit of this tutorial (slides 9–10).** The plan never holds the tutorial up against the lecture's seven items. Done item by item, the audit is the clearest answer to "is my run reproducible?":
   - environment: partly (W&B records system metrics, but the image tag exists only in `cli.sh`);
   - code: no (no git commit or package hash goes into the run);
   - data: no (a fixed `cheese_4_labels.zip` v4.0 release, an unseeded split, nothing in `config`);
   - model and hyperparameters: yes (`learning_rate`, `epochs`, `batch_size`, `model_name`);
   - metrics: only `execution_time` (stored in config), until a callback is added;
   - artifacts: partly (the console logs reach W&B's Logs tab, but no weights or sample predictions; the weights vanish with the VM);
   - notes: no.

   Milestone 3 asks for a training run that is "logged and reproducible" (`digest.md` §7). **Carry it in** ch2 (introduce the seven), ch6 (score the real run), ch9 (what is still "?").
2. **The distribution ladder (slide 27).** One machine with one GPU, one machine with many GPUs, many machines, each with its own TF strategy. The repo sits on the second row. The third row would need a second worker pool and `TF_CONFIG` (`digest.md` §3.7). **Carry it in** ch8 as the opener.
3. **Where things live in the Vertex AI console (slides 19–21).** Vertex AI is one platform. Notebooks live under Workbench, jobs under Training and workflows under Pipelines. This tutorial uses Training (the Custom jobs tab), and L15 uses Pipelines. **Carry it in** ch5 (the console beat) and ch9 (the bridge to L15).
4. **Where L13 sits in the project (slides 2, 6).** On the roadmap, tracking is set up together with the baseline models at the POC → Prototype boundary, before "Build Better Models" and "ML Workflow". Milestone 3 (the midterm presentation, 10/28) is the deadline it serves. **Carry it in** ch1 (a 10-second "you are here"), or in ch9.
5. **Choosing a tracker (slide 12).** W&B is hosted and easy to use. MLflow suits a team that must self-host. Milestone 3 accepts "W&B … or an equivalent tool". **Carry it in** ch2, in one sentence.
6. **Collaboration (slide 8).** Runs land in a shared *entity*. Notebook B's saved login shows a course team entity (`ac215-harvard`). The repo never sets `entity`, so its runs go to the key owner's default entity (`digest.md` §3.2). **Carry it in** ch6, on the W&B page.
7. **The three levers (slide 5).** Better deep learning comes from more data, better models or faster hardware. This lecture pulls the hardware lever (serverless GPUs, multi-GPU) and adds the bookkeeping that shows whether it helped. The slide's "Transfer Learning" bullet is the MobileNetV2 recipe the tutorial trains. **Carry it in** ch1 or the ch9 recap.

### 4. Conflicts

| # | Slides say | Tutorial today (repo `b9aee1c`, notebooks as saved) | Current | How the video should put it |
|---|---|---|---|---|
| 1 | **The W&B callback** (slides 13, 15, 16): `model.fit(...,callbacks=[WandbCallback()])`; W&B "automatically logs" metrics; the dashboard is full of curves. | Both repo trainers call `fit` with no callback. Commit `88f3374` removed it on 2025-10-15, less than an hour after commit `1c03dd5` moved `cli.sh` to TF 2.17 / Keras 3; `WandbCallback` and `WandbMetricsLogger` are still imported but unused. Notebook B passes `WandbCallback(save_graph=False, save_model=False)` in only one of its five training cells, and that cell prints a deprecation warning. A repo run therefore shows config, `execution_time` and system charts, but no loss or accuracy. | The repo | "This is the lecture's pattern. The middle line, the callback, is the one the repo dropped when it moved to Keras 3, and it is the line that draws the curves. One small callback puts them back" (Exercise 1, `LambdaCallback`). |
| 2 | **Closing the run** (slide 15): "Let wandb know to finish the run". | The repo does this (`task.py:338`). Notebook B never calls `wandb.finish()`, so its last run stays open until the Colab runtime ends. | The slide is the better practice | "Notebook B skips the lecture's last line. Run `wandb.finish()` yourself after the last training cell." |
| 3 | **Weights and model versions** (slides 9, 10, 13): weights are an artifact to track, W&B logs "Model versions", and a tracker answers slide 10's "?". | Neither trainer saves the model or logs a W&B artifact. Notebook B passes `save_model=False`. The Vertex VM is deleted, and the weights with it (`digest.md` E6). | The repo | "W&B can hold model versions, as the lecture says, but only if the code hands it the file. This trainer doesn't yet. Exercise 4 does, and L15 saves the model to a bucket." |
| 4 | **GPU by default** (slides 22, 24): serverless training is about getting a GPU for the training step, and two of the three slide-24 jobs have one. | `cli.sh` runs its CPU block (`n1-standard-4`, `tf-cpu.2-17.py310`). The GPU block is commented out (commit `3efb2d5`), even though the README still presents GPU first. | The repo (CPU default) | "The lecture's point is GPUs on demand. The script starts you on CPU so that everyone can finish without a GPU quota. Once your quota is approved, switch to the GPU block: uncomment it *and* comment out the CPU block." |
| 5 | **The dashboard** (slide 16): a W&B workspace that most likely belongs to an earlier mushroom version of this app (`mushroom-app-demo`, `tfhub_mobilenetv2…` runs, 15 steps of curves). | The projects are now `cheese-app-demo` (notebook B), `cheese-training-vertex-ai` and `cheese-training-multi-gpu-vertex-ai` (repo). Commit `a3d2e0b` (2024-10-15) removed the TF-Hub variant. A repo run is 2 epochs long (`cli.sh`; the multi-GPU run is 5). | The repo's names | "The lecture's screenshot comes from an earlier year's version of this app. Yours will say *cheese*, and until you add the callback it will show system charts only." Draw the view again as a schematic with today's names. |
| 6 | **The arguments** (slide 23): `model=model_1`, `epochs=25`, `batch_size=32`. | The flags are `--model_name=mobilenetv2,--train_base,--epochs=2,--batch_size=32,--wandb_key=$WANDB_KEY` (`cli.sh:19`), passed comma-separated in `--args`. The defaults in `task.py` are `--epochs` 10 and `--batch_size` 16. | The repo (the slide is schematic) | "Same idea, real names: this is what the flags are called in this repo." |
| 7 | **Where the environment is pinned** (slide 10): environments and configs live in `pyproject.toml`, `uv.lock`. | In this repo those two files pin only the console container (its one dependency is `google-cloud-aiplatform`). The training environment is the prebuilt image tag in `cli.sh` (`tf-cpu.2-17.py310`; `cli-multi-gpu.sh` uses `tf-gpu.2-14.py310`) plus `wandb==0.15.11` in `setup.py`. scikit-learn and requests are not declared at all (`digest.md` E8, E12). | The repo | "Here the lock file pins the cockpit, not the trainer. The trainer's environment is the image tag plus `setup.py`, so record both." |
| 8 | **Where the job shows up** (slides 21, 25): slide 21 labels Training as "Training pipelines and jobs", on 2025 console screenshots. | `sh cli.sh` creates a *custom job*, listed under Training → Custom jobs, which is exactly where slide 25's link points. Only the unused `cli.py` creates a training pipeline. The console wording may also have changed since (`digest.md` §10, open questions). | Custom jobs | "Your job is on the Custom jobs tab, where the lecture's link goes." The video draws the console as a schematic tagged `illustration`, with these names. |
| 9 | **The single-GPU case** (slide 27): one machine with one GPU uses One Device Strategy. | `task.py:60` creates a `MirroredStrategy` only to print `Number of replicas: 1`, then builds the model outside any scope, so TF uses its default strategy (`digest.md` E11). | The repo's behaviour, which is in effect the one-device case | "Don't let that line fool you: it only counts GPUs. With no scope, the single-GPU trainer runs as the lecture's one-device case." |

Not counted as a conflict: the deck is "Lecture 13", while the course site's week page labels this session "Lecture 12" (`digest.md` E21). The series and the `lecture_ref` tags follow the deck.

### 5. Proposals for the BRIEF and script authors

**General**
- Tag each chapter that stands on lecture ground with one grey `lecture_ref(13, "a–b")`, using the ranges below. Re-draw every idea in the series style. Slide 16 (W&B) and slides 20–21 (console) become schematic drawings tagged `illustration`, with today's project and tab names (Conflicts 5, 8).
- Make slide 9's seven items a **running scorecard**: introduce it in ch2, score the real run in ch6, show what is still "?" in ch9. This is gap 1 and the video's strongest link to the lecture.
- When captures are made, record the notebook's saved outputs as `recorded`, and the README/log lines the digest documents as `expected`. Then re-check Conflicts 1, 4 and 8 against them.

**Per chapter**
- **Ch1 · Lecture 13 · slides 6–8.** After the hook, spend 10 seconds re-drawing slide 6's roadmap with its red dashed box around "Setup Experiment Tracking" and "Build Baseline Models": that box is today. Name the two slide-8 words that answer the hook: *reproducibility*, *accountability*. Optionally add slide 5's three levers as three dials with the third (hardware) lit, or save them for the recap.
- **Ch2 · Lecture 13 · slides 9–16.** Re-draw slide 10's "Where do we track what?" table: code → GitHub, data → versioning, environment → lock files, and the last row left as "?". Notebook A fills the "?" by hand (the `experiment_<ts>/` folder), and W&B fills it automatically (slide 11). Turn slide 9's seven items into the columns of the runs table. Then play the slide 14 → 15 diff as three lines sliding into unchanged code, tagged with the lecture's call-outs: *initialize the run*, *add a callback to monitor the model*, *finish the run*. Add one sentence from slide 12: W&B here, MLflow if you must self-host, and Milestone 3 accepts an equivalent. Keep notebook B's `wandb.config = {...}` (Excerpt 12) as the contrast with the repo's `wandb.init(config=...)`.
- **Ch3 · Lecture 13 · slides 23–24.** Re-draw slide 23 with the real code: notebook globals peel off and come back into `task.py` as flags. Then show slide 24's first arrows (Python file → TAR.GZ). Use the lecture's captions *Move Code to Python File* and *Pass Arguments*, then show the real flag names (Conflict 6).
- **Ch4 · Lecture 13 · slide 24.** Name the box the lecture's way first, then the repo's way: "Model Trainer CLI Container" = `model-training-cli`. Draw its two arrows from slide 24 (package & upload; create jobs), and none into the job containers. That is the visual proof that "your container submits, it never trains".
- **Ch5 · Lecture 13 · slides 19–25.** This is the central diagram: slide 24 drawn in three layers with the series colours. The laptop (GREY) holds the CLI container (TEAL). Next comes the GCS bucket holding the tarball. Vertex AI (BLUE) holds per-job containers labelled with their hardware, which appear, run and vanish. Keep the lecture's three numbered steps (1 move code, 2 package & upload, 3 create & run training jobs). Before the mechanism, give slide 22's four reasons as a five-second "why". End on a schematic sidebar from slide 21 (Workbench / Training / Pipelines) with Training → Custom jobs highlighted (Conflict 8).
- **Ch6 · Lecture 13 · slides 15–16.** Put slide 15's three-line pattern next to `task.py:312-338`. The callback line fades out (Conflict 1) and the loss chart becomes a ghost outline. The fix from Exercise 1 brings it back, and slide 16's view, redrawn with cheese names, is "what you see afterwards". Add a pause-and-ponder: "Of the lecture's seven items, which ones does this run record?" (answers in gap 1). In the existing loss-≈-100 pause, add one bridging sentence after the reveal: the lecture's own dashboard shows the same thing, loss near 100 while accuracy rises.
- **Ch7 · Lecture 13 · slides 22–24.** Start from slide 24's three job tiles (two with a GPU, one without) and zoom into one tile to show the three switches: accelerator, `tf-gpu` image, regional quota. Slide 22's "GPU only for the training step" is the money reason. Say clearly that the shipped script is on CPU (Conflict 4).
- **Ch8 · Lecture 13 · slides 27–30.** Open with slide 27's three-row ladder, with "you are here" on the second row. Then play the slide 28 → 29 diff with its three call-outs (*create distribution strategy*, *adjust dataset batch size*, *create & compile model in strategy scope*), and only then the 64 → 32 + 32 split animation. Say "replicas" aloud while the code says `num_workers`, and note that in Multi Worker Mirrored Strategy a *worker* is a machine. For slide 30, grey out everything except the launch script.
- **Ch9 · Lecture 13 · slides 9–10.** Bring the scorecard back. Metrics are filled after Exercise 1. Weights are still "?" because the VM takes them with it (Exercise 4; L15 saves to a bucket). Then show slide 6's next bars (Build Better Models, ML Workflow) and slide 21's Pipelines item as the road to L15.
- **Recap card.** Change question 1 to the lecture's version: "Name the seven things a run record should hold. Which ones does this trainer record?" Add "Which strategy for one machine with two GPUs, and which for two machines?" (slide 27). Keep the other questions.

**Terms**
- Use the lecture's words: *experiment tracking*, *run*, *callback*, *Weights & Biases (W&B)* (the slides' "Weights & Bias" is a typo), *serverless training*, *Move Code to Python File*, *Pass Arguments*, *Package & Upload*, *GCS bucket*, *Model Trainer CLI Container* (once, then `model-training-cli`), *Create & Run Training Jobs*, *One Device / Mirrored / Multi Worker Mirrored Strategy*, *strategy scope*.
- Add the repo's words where the lecture is vague: *custom job*, *worker pool*, *prebuilt training container*, *replica*, *global batch*.
- Qualify, don't repeat: "W&B logs automatically" (only with a callback); the lecture's "Artifacts" (weights, logs and predictions in general, not only W&B Artifact objects); `num_workers` (here it counts GPUs on one machine).
