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
- **Slide 6 · Cheese App status (Gantt-style roadmap).** A long light-blue arrow across the top labelled POC, Prototype, MVP left to right, with dashed vertical lines marking the phase boundaries. Below, horizontal bars in pastel colours: "Design Cheese App" spans POC and Prototype; "Data Collection" sits in POC; "Setup Experiment Tracking" and "Build Baseline Models" are staggered at the POC/Prototype boundary and enclosed together in a **red dashed box** (today's work); "Build Better Models" and "ML Workflow" sit in Prototype; "Build Cheese App" in MVP; "Deployment, Scaling & Automation" stretches from late Prototype to the end of MVP. For: placing L13 in the project timeline.
- **Slide 10 · "Where Do We Track What?" table.** Two columns, Item → Where it's tracked: code/scripts → GitHub repository; data and versions → data versioning (DVC, GCS buckets); environments and configs → `pyproject.toml`, `uv.lock` in GitHub; model weights, metrics, logs → "?". For: showing the one empty cell an experiment tracker fills. Re-draw as four rows that each snap into a home, with the last row left hanging until a W&B box catches it.
- **Slides 14 → 15 · annotated code diff (plain Keras → Keras + W&B).** Slide 14 is the baseline: three blocks commented `# Training Params`, `# Data`/`# Model`, `# Train`. Slide 15 is the same code with three insertions, each tied by a curved arrow to a coloured call-out on the right: blue "Initialize wandb run" → the `wandb.init(...)` line before training; green "Add a callback to monitor model" → `callbacks=[WandbCallback()]` inside `model.fit`; red "Let wandb know to finish the run" → `wandb.run.finish()` after training. For: showing that tracking is a thin wrapper around unchanged training code. Re-draw as the slide-14 code with three lines sliding in, each tagged start / watch / close.
- **Slide 16 · W&B workspace screenshot.** Left panel: a list of four runs with coloured dots (names look like `tfhub_mobilenetv2…` and `mobilenetv2_train_…`; too small to read reliably). Main area: a "Charts" grid of five line plots titled loss, epoch, val_accuracy, accuracy, val_loss, each with four coloured lines over steps 0–14; accuracy curves rise and flatten, loss curves fall. The breadcrumb appears to show a project from an earlier app demo, not the cheese project (uncertain at this resolution). For: what "automatic" tracking looks like: runs as rows, metrics as overlaid curves. Re-draw from our own runs or as a stylised runs table plus overlaid curves.
- **Slide 20 · Vertex AI console dashboard (screenshot).** Google Cloud console with the Vertex AI left sidebar and a Dashboard of "Get started" and "Tutorials" panels and tiles (Vertex AI Studio, Model Garden, Colab Enterprise, Prepare Data, Model Development, Deploy & Use). For: orientation only.
- **Slide 21 · Vertex AI console map (annotated screenshot).** The console's left sidebar with three items outlined in red, each linked by a long arrow to a coloured label on the right: Workbench (under the Notebooks group) ← green "JupyterLab notebooks"; Training (under Model development) ← pink "Training pipelines and jobs"; Pipelines (under Deploy and use) ← blue "Build ML Workflow". For: which part of the console serves which stage. Re-draw as a three-entry sidebar with arrows to "notebooks / training jobs / workflows"; L13 uses the middle one, L15 the third.
- **Slide 23 · Step 1, "Move Code to Python File".** Two code panels joined by a thick green arrow. Left, "Notebook" (Colab icon): `get_dataset`, `get_model_1`, `get_model_2` definitions, then data, a hard-wired `model_1 = build_model_1(...)`, and `model_1.fit(...)`. Right, "Python File" (Python icon): the same function definitions, but the model line has become a generic `model = ...` and training is `model.fit(...)`. Under the right panel, "Pass Arguments:" with three red arrows pushing up into the file: `model=model_1`, `epochs=25`, `batch_size=32`. For: the notebook's hard-coded choices become command-line arguments, so one file can train any variant. Re-draw as values peeling off the notebook and re-entering the file from below as flags.
- **Slide 24 · Steps 2–3, the serverless training pipeline (the lecture's central mechanism).** Left to right with green arrows: Notebook thumbnail → Python File thumbnail → "Packaged Python files" (a TAR.GZ document icon) → a long arrow into a dashed box labelled **GCP**. Inside GCP, top: a "GCS Bucket" holding the TAR.GZ; a green arrow runs down from the bucket into a "Vertex AI" panel containing three "Job" tiles, each a "Container" box with a hardware label under it: "CPU, RAM, GPU", "CPU, RAM, GPU", "CPU, RAM" (the third has no GPU). Bottom left: a green box "Model Trainer CLI Container" with two dark arrows up into the packaging arrow and the upload arrow (it does both), and a grey arrow right to the Vertex AI jobs. Red step badges: "2 Package & Upload to GCP" (top), "3 Create & Run Training Jobs" (bottom). For: who does what. Your local CLI container only packages, uploads and submits; the bucket holds the code; Vertex AI runs each job in its own container on hardware chosen per job. Re-draw in three layers: laptop (CLI container), storage (bucket), compute (job containers that appear, run and vanish, with a GPU chip per job only where requested).
- **Slides 28 → 29 · annotated code diff (single-GPU → multi-GPU).** Slide 28 repeats the baseline code from slide 14. Slide 29 adds three call-outs with curved arrows: blue "Create distribution Strategy" → `strategy = tf.distribute.MirroredStrategy()` (followed by `num_workers = strategy.num_replicas_in_sync`); green "Adjust dataset batch size" → the `batch_size=batch_size * num_workers` argument of `get_dataset`, which is also printed in red; red "Create & Compile model in strategy scope" → `with strategy.scope():` with `build_model` indented under it. `model.fit` is untouched. For: the three edits that turn a script into a data-parallel one. Re-draw as the slide-28 code with three lines sliding in, then cut to two GPUs each receiving half of the enlarged batch.

## Terms the lecture uses

- **"The 3 components for better Deep Learning"**, "More Data", "Better/Faster Models", "Faster Hardware", "Multi GPU Server Training" (slide 5).
- **"Cheese App"** and its phases **"POC"**, **"Prototype"**, **"MVP"**; bars "Setup Experiment Tracking", "Build Baseline Models", "Build Better Models", "ML Workflow", "Deployment, Scaling & Automation" (slide 6).
- **"Experiment Tracking"** (slides 3, 7–17); the five benefits **Organization, Reproducibility, Logging, Collaboration, Accountability** (slide 8); the seven tracked items **Environment, Code, Data, Model, Metrics, Artifacts, Notes** (slide 9). The lecture's "Artifacts" means weights, logs and sample predictions in general, not specifically W&B's versioned "Artifact" objects.
- **"Weights & Biases (W&B)"** (slides 11–13), **"WandB"** (slides 15–16), lowercase **"wandb run"** (slide 15), and **"Weights & Bias"** (sic, slides 17, 25, 30). The tutorial README uses "WandB"/"W&B" (section `#get-wandb-account-api-key`).
- **"run"**, **"callback"** ("Add a callback to monitor model", slide 15).
- Tool names **MLflow, Comet, Neptune** (slide 12).
- **"Vertex AI: Google's Unified ML Platform"**; its three parts **"Data Engineering"**, **"Data Science"**, **"ML Engineering Workflows"** (slide 19).
- Console labels **"JupyterLab notebooks"** (the Workbench item), **"Training pipelines and jobs"** (Training), **"Build ML Workflow"** (Pipelines) (slide 21). The README's step and link say "View Training Jobs" and point at Training → **Custom jobs**; `cli.sh` creates a custom job, and only the unused SDK launcher `cli.py` creates a *training pipeline* (`digest.md` B12, B16).
- **"Serverless Training"**, executed "on an as-need basis" (slide 22).
- **"Move Code to Python File"**, **"Pass Arguments"** (slide 23); **"Package & Upload to GCP"**, **"Packaged Python files"**, **"GCS Bucket"**, **"Model Trainer CLI Container"**, **"Create & Run Training Jobs"**, **"Job"** / **"Container"** (slide 24). Repo names for the same things: the local image and container are `model-training-cli` (the service account is `model-trainer`); the package is `trainer.tar.gz`, uploaded as `cheese-app-trainer.tar.gz`; a job is a Vertex AI **custom job** with a **worker pool**, and its container is one of Google's **prebuilt TensorFlow training images** (`tf-cpu.2-17.py310` etc.), not an image you build (`digest.md` §3.3–3.4).
- **"distributed training"**, **"One Device Strategy"**, **"Mirrored Strategy"**, **"Multi Worker Mirrored Strategy"** (slide 27); **"distribution Strategy"**, **"strategy scope"** (slide 29). The repo uses only `MirroredStrategy`.
- **`num_workers`** (slide 29) is the number of GPU *replicas* on one machine (`num_replicas_in_sync`), not machines; in "Multi Worker Mirrored Strategy" a *worker* is a machine. The repo keeps the slide's variable name and calls the product `global_batch_size` (`digest.md` §3.7).
- **"Multi GPU Training"** (slides 3, 26–27); **"multi-GPU Serverless Training"** (slide 30). The README section is "Optional: Multi GPU Training" (`#optional-multi-gpu-training`).

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
