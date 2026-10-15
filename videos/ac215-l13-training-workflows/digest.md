# L13 · Advanced Training Workflows: experiment tracking (W&B), multi-GPU, serverless training (Vertex AI) — tutorial digest

- **Ed lesson:** https://edstem.org/us/courses/97373/lessons/166038/. I could not open it because Ed needs a login. This digest is built from the course site source (`tutorials_demo.md:167-184`, which links this Ed lesson at line 168), the repo, and the two Colab notebooks.
- **Repo:** `dlops-io/model-training`, branch `main`, commit `b9aee1cc1923dd1f673093ad3ff5bb023049b4ff`, committed 2025-10-16 07:31:56 -0400 ("remove pipfiles and do minor edits").
  - The other branch is `origin/pipenv` @ `fdc1f57ff1c2f5997b12db8e2cade127df3d73c0`, committed 2025-03-14 07:03:20 -0400 ("update"). It is the older Ubuntu + Pipenv version. Section 7 has the diff.
- **README sections this lecture covers** (all of the README): `#prerequisites`, `#setup-environments`, `#clone-the-github-repository`, `#apis-to-enable-in-gcp-for-project`, `#setup-gpu-quotas`, `#setup-gcp-credentials`, `#create-a-local-secrets-folder`, `#setup-gcp-service-account`, `#create-gcs-bucket`, `#get-wandb-account-api-key`, `#run-container`, `#run-docker-shellsh`, `#package--upload-python-code`, `#review-trainer-code`, `#run-sh-package-trainersh`, `#create-jobs-in-vertex-ai`, `#optionalcreate-jobs-in-vertex-ai-using-cpu`, `#view-jobs-in-vertex-ai`, `#view-training-metrics`, `#optional-multi-gpu-training`.
- **Colab notebooks used.** I read the cells and skipped the embedded images. "cell N" below means the 0-based index of the cell in the `.ipynb` JSON.
  - **Notebook A:** `colab/L13_cheese_classification.ipynb` ("Tutorial - Cheese Classification Models, Experimental Tracking"; md5 `0f4a5c78698b744f46178dc36818f88c`). The course site links it as "Colab Notebook A: Cheese Classification Models" (`tutorials_demo.md:172`).
  - **Notebook B:** `colab/L13_wandb_tracking.ipynb` ("Tutorial - Cheese Classification Models, Experiment Tracking", with W&B; md5 `ac692e0ab9b407c35cccd497843332bb`). The course site links it as "Colab Notebook B: Experiment Tracking with W&B" (`tutorials_demo.md:173`).
  - Both notebooks carry saved outputs from Colab runs in October 2025 (`nvidia-smi` dates: notebook B Oct 14, notebook A Oct 20) on a Tesla T4 with TF 2.19.0. Keras 3.10.0 is printed only by notebook B (cell 9); notebook A does not print the Keras version.
- **Third-party code I read to check behaviour.** I downloaded these from PyPI, read them, and never ran them:
  - `wandb==0.15.11`, the exact pin in `model-training/package/setup.py:5`;
  - `google-cloud-aiplatform==1.121.0`. The container locks 1.120.0 (`model-training/uv.lock:147-148`), which I assume is the same for the call used.
  - I also listed the two GitHub release zips the code downloads (I read only their central directories, plus two small JSON files from `experiments.zip`).
- **AWS variant:** `model-training-aws` is private and not linked (`tutorials_demo.md:180-184`). It is not covered here.

Paths are written from the folder that holds your clones. For example, `model-training/package/trainer/task.py:153` means line 153 of `package/trainer/task.py` inside your `model-training` clone.

---

## 1. What you build

The lecture has two halves.

**Notebooks.** You first train five image classifiers on 1,156 photos of four cheeses (brie, gouda, gruyere, parmigiano) in Colab on a free T4 GPU. Notebook A tracks experiments **by hand**: every run writes a `.keras` model, its weights, its training history and a metrics JSON into a folder `experiment_<unix time>/`. A pandas table then ranks the runs and the folder is uploaded to a GCS bucket. Notebook B repeats the same runs but also logs them to **Weights & Biases (W&B)**, a hosted experiment-tracking service.

**Repo.** Then you take the winning recipe (MobileNetV2 transfer learning) out of the notebook and turn it into a **Python package** (`package/setup.py` + `package/trainer/task.py`). You zip it into `trainer.tar.gz` and copy it to a GCS bucket. Then you ask **Vertex AI custom training** to run it. Vertex AI rents a VM of the size you choose (optionally with an NVIDIA T4), starts one of Google's **prebuilt TensorFlow training containers** on it, `pip install`s your package, and runs `python -m trainer.task --epochs=... --wandb_key=...`. When the script exits, the VM is deleted. You pay only for the minutes it ran. The trainer logs the run to W&B. An optional second trainer (`task_multi_gpu.py`) runs the same model on **two T4s on one machine** with `tf.distribute.MirroredStrategy`.

Your laptop never trains anything in the repo half. The Docker container you build locally is only a **control console**: it holds `gcloud`/`gsutil` and your service-account key, packages the code, and submits jobs.

```
 YOUR LAPTOP                                                      GOOGLE CLOUD  (project $GCP_PROJECT)
 +------------------------------------------------------+
 |  AC215/                                               |
 |   +- model-training/  --bind mount--> /app            |
 |   +- secrets/model-trainer.json --bind mount--> /secrets
 |                                                       |
 |  +-------------------------------------------------+  |  (1) gsutil cp trainer.tar.gz        +--------------------------------+
 |  | container "model-training-cli"  (no ports)      |--+------------------------------------>| GCS bucket  gs://<your-bucket> |
 |  | python:3.13-slim-bullseye, linux/amd64          |  |      package-trainer.sh:4           |   cheese-app-trainer.tar.gz    |
 |  | gcloud + gsutil, venv /.venv (aiplatform SDK)   |  |                                     +---------------+----------------+
 |  | env: GOOGLE_APPLICATION_CREDENTIALS=/secrets/.. |  |  (2) gcloud ai custom-jobs create                   | pip install
 |  |      GCP_PROJECT  GCS_BUCKET_URI  WANDB_KEY     |--+------------------------------------>+---------------v----------------+
 |  +-------------------------------------------------+  |      cli.sh:32-37 (HTTPS API)       | Vertex AI Training (us-central1)|
 +------------------------------------------------------+                                      |  provisions a VM per job        |
                                                                                               +---------------+----------------+
                                                                                                               |
              +------------------------------------------------------------------------------------------------v--+
              | Vertex-managed VM: n1-standard-4 (+1 T4)   or   n1-standard-32 + 2 T4 (multi-GPU)                   |
              |  prebuilt container  us-docker.pkg.dev/vertex-ai/training/tf-cpu.2-17.py310 (or tf-gpu.2-17/2-14)  |
              |    pip install cheese-app-trainer  (+ wandb==0.15.11)                                               |
              |    python -m trainer.task  --model_name=mobilenetv2 --train_base --epochs=2 --batch_size=32 ...     |
              |      |-- HTTPS GET github.com/dlops-io/datasets/releases/download/v4.0/cheese_4_labels.zip (~305 MB)|
              |      |-- tf.data pipeline -> MobileNetV2 (+Dense 128 +Dense 4) -> model.fit                         |
              |      |-- wandb.login / init / config.update / finish -------------------------> wandb.ai            |
              |      |                                                     project cheese-training-vertex-ai         |
              |      +-- stdout / stderr ------------------------------------------------------> Cloud Logging       |
              |  VM is torn down when the script exits. The trained model is NOT saved anywhere (see section 10).   |
              +-----------------------------------------------------------------------------------------------------+

 BROWSER: Colab (T4 runtime) -- Notebook A --> experiment_<ts>/ files --> GCS bucket (cheese-app-models)
                             -- Notebook B --> same + wandb.ai project cheese-app-demo
```

---

## 2. Prerequisites and costs

**Accounts**
- A GCP project with billing enabled (`README.md:14`).
- A W&B account at https://wandb.ai (`README.md:14`, `README.md:73-81`). The free tier is enough.
- A Google account for Colab.

**Local installs**
- Docker (`README.md:7`) and git.
- That is all. `gcloud`, `gsutil`, `uv` and Python 3.13 live inside the container (`model-training/Dockerfile:2`, `model-training/Dockerfile:36-41`). TensorFlow is *not* installed anywhere locally; it only exists inside Vertex AI's prebuilt container.
- Windows: there is no `.bat` script any more (an empty `docker-shell.bat` was deleted in commit `1c03dd5`), so use WSL2 or Git Bash.

**GCP APIs to enable**
- **Vertex AI API** (`aiplatform.googleapis.com`), listed at `README.md:19-21`.
- Cloud Storage is also used (by `gsutil` and by the job, which reads the tarball). It is enabled by default on new projects, but check it if `gsutil` reports that the API is disabled.

**GPU quota (only for the GPU and multi-GPU runs)**
- In IAM & Admin → Quotas, filter `Custom model training`. Request `Custom model training Nvidia T4 GPUs per region` in the region you will use (`README.md:23-44`).
- Approval can take hours, or be refused for new accounts (`README.md:43-44`).
- The default `cli.sh` runs on **CPU**, so you can finish the tutorial without any GPU quota.
- The multi-GPU job needs **2** T4s and a 32-vCPU machine (`model-training/cli-multi-gpu.sh:6`, `model-training/cli-multi-gpu.sh:11-12`). Check the CPU quota for custom training as well.

**Service account and key**
- Create SA `model-trainer` with roles **Storage Admin**, **AI Platform Admin** and **Vertex AI Administrator** (`README.md:62`).
- Download a JSON key and rename it `model-trainer.json` (`README.md:64`).
- Put it in a `secrets/` folder that sits **next to** the clone, not inside it (`README.md:50-58`):
  ```
  AC215/
    model-training/
    secrets/model-trainer.json
  ```
- Where the code expects it:
  - `docker-shell.sh` mounts `$(pwd)/../secrets/` at `/secrets` (`model-training/docker-shell.sh:7`, `model-training/docker-shell.sh:19`).
  - It sets `GOOGLE_APPLICATION_CREDENTIALS=/secrets/model-trainer.json` (`model-training/docker-shell.sh:20`).
  - The entrypoint runs `gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS` (`model-training/docker-entrypoint.sh:6`).
- The job running on Vertex AI does **not** use this key. It runs as Google's Vertex AI service agent in your project, which can read buckets in the same project. The key only identifies *you* when you submit.

**Environment variables**

| Variable | Set where | Used where |
|---|---|---|
| `GCS_BUCKET_URI` | `model-training/docker-shell.sh:8` (`"gs://cheese-app-trainer"`; **change it**: bucket names are global) | `model-training/package-trainer.sh:4`, `model-training/cli.sh:10`, `model-training/cli-multi-gpu.sh:9`, `model-training/cli.py:8` |
| `GCP_PROJECT` | `model-training/docker-shell.sh:9` (`"ac215-project"`; **change it**) | `model-training/docker-entrypoint.sh:8`, `model-training/cli.py:6` |
| `WANDB_KEY` | **your host shell**: `export WANDB_KEY=...` (`README.md:80`) before `sh docker-shell.sh`; forwarded by `model-training/docker-shell.sh:23` | `model-training/cli.sh:19`, `model-training/cli-multi-gpu.sh:16` → `--wandb_key` → `model-training/package/trainer/task.py:153` |
| `GCP_REGION` | inside `model-training/cli.sh:14` and `model-training/cli-multi-gpu.sh:13` (`"us-central1"`) | the same scripts; `model-training/cli.py:7` reads it from the environment but nothing exports it (section 6) |
| `GOOGLE_APPLICATION_CREDENTIALS` | `model-training/docker-shell.sh:20` | `model-training/docker-entrypoint.sh:6` |

- **Notebook B** reads the W&B key from a Colab secret named exactly `WandB` (`userdata.get('WandB')`, notebook B cell 34).

**Bucket**
- One bucket for the code tarball (`README.md:66-71`). Create it in the same region you train in, to keep things simple.
- Notebook A cell 63 and notebook B cell 13 point at a *different* bucket, `cheese-app-models`, in project `ac215-project`. Those are the instructors' resources. Replace them with your own.

**What costs money, and how to stop it.** Prices are approximate list prices for us-central1 that I remember; check the Vertex AI pricing page before you rely on them.

| Resource | Rough cost | Lifetime | Shut down |
|---|---|---|---|
| Vertex AI custom job, `n1-standard-4`, CPU only | ≈ $0.22/h | from provisioning until the script exits | It stops by itself. To stop a stuck or queued job: `gcloud ai custom-jobs cancel JOB_ID --region=us-central1` (my command, not in the README), or **Cancel** in the console |
| … plus 1 × `NVIDIA_TESLA_T4` | ≈ +$0.40/h | same | same |
| Multi-GPU: `n1-standard-32` + 2 × T4 | ≈ $1.75/h + 2 × $0.40/h ≈ $2.55/h | same | same |
| GCS: one tarball of a few KB | ~0 | until deleted | `gsutil rm $GCS_BUCKET_URI/cheese-app-trainer.tar.gz`, or delete the bucket |
| Colab T4 | free tier (quota-limited) | session | Runtime → Disconnect and delete runtime |
| W&B | free personal tier | — | delete runs/projects in the UI if you like |

- No resource in this tutorial keeps running after your job finishes: no endpoints and no always-on VMs. The local container is started with `--rm` (`model-training/docker-shell.sh:17`).
- The real money risks are:
  - a job that fails late, for example after the 305 MB dataset download, and that you resubmit many times;
  - the multi-GPU machine.
- **Security clean-up after the course:**
  - Delete the `model-trainer` key in IAM.
  - Rotate your W&B key. It travels as a plain command-line argument and is visible in the job's spec (section 6).

---

## 3. Concepts this tutorial teaches

### 3.1 Experiment tracking: every training run is a record **[ANIMATE]**
- **Explanation.** An *experiment tracker* stores, for every run:
  - the inputs: code version, hyperparameters (`config`) and data version;
  - the outputs: metrics over time, final scores and artifacts (model files);
  - the environment: hardware and runtime.
  This lets you compare runs, reproduce the best one, and know which file came from which settings.
- **The two trackers in this lecture.**
  - Notebook A builds a home-made tracker. `create_experiment()` makes `experiment_<ts>/`, and `evaluate_save_model()` writes `<model>.keras`, `<model>.weights.h5`, `<model>.json`, `<model>_train_history.json` and `<model>_model_metrics.json` (notebook A cell 12). The compare cell turns those JSONs into a sorted table (cell 54).
  - W&B is the managed version of exactly that table. It adds live charts, system metrics (CPU/GPU utilisation) and a shared web UI.
- **Mental model.** A spreadsheet in which each **row is a run**, the columns are config + summary metrics, and each row links to time-series charts and files.
- **Analogy.** A lab notebook in which every experiment is dated, the settings are written down *before* you start, and the result is pasted in afterwards. W&B is a lab notebook that fills itself in.
- **Common misconception.** "W&B tracks my training automatically once I call `wandb.init`." It does not. `wandb.init` creates the row and records `config` plus system metrics. Loss and accuracy curves appear only if something *logs* them: a Keras callback (`WandbCallback`, `WandbMetricsLogger`) or your own `wandb.log(...)`. The current repo trainer logs none (section 10, E1).
- **Animation idea.** The notebook-A table of five runs (2_block, 4_block, vgg_style, mobilenet ×2) rearranges itself into a W&B "runs" table. Each row then unfolds into its loss curve. A MobileNet row glows as the winner. (Which MobileNet variant wins differs between the two saved notebook runs: fine-tuned in notebook A, frozen in notebook B. With 116 test images, one image is 0.86 %. In notebook A the gap is 2 images (68.97 % vs 67.24 %), which is noise. In notebook B the gap is 7 images (68.97 % vs 62.93 %), but the fine-tuning cell runs only `epochs = 10` (cell 52) against 15 for the frozen cell (cell 50), so that comparison is not like-for-like.) Its recipe then flies into the `cli.sh` `CMDARGS` line (`--model_name=mobilenetv2,--train_base,...`).

### 3.2 The W&B run lifecycle and where the data goes
- **Explanation.** The run goes through four calls.
  1. `wandb.login(key=...)` writes the key to `~/.netrc`.
  2. `wandb.init(project, config, name)` starts a background process that streams to `api.wandb.ai`. Files are also written locally under `./wandb/run-*`.
  3. `wandb.log` / callbacks append metric rows; `wandb.config.update` adds config keys.
  4. `wandb.run.finish()` (or process exit) flushes and closes.
- **In the repo:**
  - login at `model-training/package/trainer/task.py:153`;
  - init at `model-training/package/trainer/task.py:313-322`;
  - config update at `model-training/package/trainer/task.py:336`;
  - finish at `model-training/package/trainer/task.py:338`.
- **Mental model.** A flight recorder that radios its data home. The project is the airline, the run is one flight, `config` is the flight plan and `log` is the telemetry.
- **Analogy.** Uploading a fitness-watch workout. The watch (your script) records locally and syncs to the app (wandb.ai).
- **Common misconceptions.**
  - "`wandb.config = {...}` sets the config." In wandb's module design, `wandb.config` is a plain module attribute that `wandb.init` points at the run's Config object (I checked `wandb/sdk/lib/module.py` `set_global` in 0.15.11). Re-assigning it to a dict just replaces the reference, so (at least in that version) the dict is never synced. Notebook B does exactly this (section 10, E14). The repo does it correctly with `wandb.init(config=...)`.
  - "The project/entity is chosen in the code." The project yes. The entity (user or team) is not set anywhere in this code, so W&B uses the default entity of the account that owns the key. You could override it with `wandb.init(entity=...)`. Notebook B's saved login line shows `shivasj (ac215-harvard)`: user `shivasj`, default entity the `ac215-harvard` team (cell 34 output).

### 3.3 From notebook to Python package **[ANIMATE]**
- **Explanation.** Vertex AI's prebuilt containers run *Python packages*, not notebooks. The repo's `package/` folder looks like a source distribution (sdist):
  - `setup.py` (`model-training/package/setup.py:1-13`): name `cheese-app-trainer`, `install_requires=["wandb==0.15.11"]`, `packages=find_packages()`, which finds the `trainer` package because `trainer/__init__.py` exists;
  - `PKG-INFO` and `setup.cfg` metadata;
  - the module `trainer/task.py`.
- **What packaging does.** `package-trainer.sh` tars the folder and gzips it (`model-training/package-trainer.sh:1-3`). The result has the layout pip expects from an sdist: one top-level directory that contains `setup.py`. On the VM, the prebuilt container runs `pip install` on that tarball and then `python -m trainer.task <args>`.
- **What the notebook globals become.** They turn into `argparse` flags (`model-training/package/trainer/task.py:26-54`), so the *same* code can be launched with different hyperparameters from the command line.
- **Mental model.** Notebook cells → one script → a script with flags → a pip-installable tarball → a file in a bucket that any machine can install.
- **Analogy.** A recipe card. The notebook is you cooking in your own kitchen. The package is a recipe card plus a shopping list (`install_requires`) that you post to a commercial kitchen (Vertex), which supplies the oven (TensorFlow) itself.
- **Common misconceptions.**
  - "The Docker image I built is what runs on Vertex." No. Your image only *submits*. The job runs in Google's image `tf-cpu.2-17.py310` (`model-training/cli.sh:31`). Your code reaches it only through the tarball.
  - So after editing `task.py` you must re-run `sh package-trainer.sh`, but you do **not** need to rebuild your Docker image.
- **Animation idea.**
  1. Notebook cells slide together into one long `task.py`.
  2. Hard-coded numbers (`epochs = 15`) peel off and become `--epochs` flags.
  3. `task.py` drops into a `trainer/` box, `setup.py` clips on as a label, and the box is shrink-wrapped into `trainer.tar.gz`.
  4. It flies into a bucket icon, then down into a VM where it unwraps and `pip install` progress bars run.

### 3.4 Serverless training with Vertex AI custom jobs **[ANIMATE]**
- **Explanation.** A *custom job* is a request: "run this code on this hardware once." You describe a **worker pool**:
  - `machine-type` (`n1-standard-4`), `replica-count`;
  - optional `accelerator-type` / `accelerator-count`;
  - the container (`executor-image-uri`, one of Google's prebuilt training images);
  - the code (`--python-package-uris` + `python-module`);
  - and `--args`.
  Vertex provisions the VM, pulls the image, installs your package, runs it and streams stdout to Cloud Logging. The VM is deleted at the end.
- **Job states.** `QUEUED → PENDING → RUNNING → SUCCEEDED/FAILED/CANCELLED`.
- **Two ways to submit in the repo:**
  - the `gcloud ai custom-jobs create` CLI (`model-training/cli.sh:32-37`), which the README uses;
  - the Python SDK `aiplatform.CustomPythonPackageTrainingJob(...).run(...)` (`model-training/cli.py:23-51`), which is present but not mentioned in the README.
- **Mental model.** A print shop. You upload a file, choose paper and colour (machine and GPU), pay per page (per minute), and pick up the result. You never own the printer.
- **Analogy.** A rideshare for compute. Order the car size you need, ride, get out, and the car leaves.
- **Common misconceptions.**
  - "Serverless means no machine." There *is* a VM, sized by you; you just don't manage its lifecycle.
  - "The job can see my laptop." It can't. The data must come from the internet or GCS (here: a GitHub release, `model-training/package/trainer/task.py:96-100`), and the outputs must be written somewhere durable, or they vanish with the VM.
- **Animation idea.**
  1. `gcloud ai custom-jobs create` fires a request arrow at a "Vertex AI" cloud.
  2. A VM box materialises, with a T4 chip snapping into a slot when `accelerator-count=1`.
  3. The prebuilt-image layer stack drops in, then the tarball, then the logs scroll out to a "Cloud Logging" panel.
  4. At `Training Job Complete` the VM dissolves, and a meter showing "$ per minute" stops.

### 3.5 Two identities: who submits and who runs
- **Explanation.**
  - **Submitter.** Your container authenticates as `model-trainer@…` using the key file (`model-training/docker-entrypoint.sh:6`). That identity needs permission to write to the bucket (Storage Admin) and to create jobs (Vertex AI Administrator).
  - **Runner.** The job itself runs as a Google-managed *service agent* of your project (the Vertex AI Custom Code Service Agent, `service-<project-number>@gcp-sa-aiplatform-cc.iam.gserviceaccount.com`, unless you pass `--service-account`). That is why it can `pip install` from your bucket without any key.
  - **W&B.** It has its own, separate credential (the API key), which you pass in by hand.
- **Mental model.** Three badges: your keycard opens the building (GCP API); the contractor you hire has their own badge (service agent); the W&B key is the password to a different building.
- **Common misconception.** "I must copy `model-trainer.json` into the package." Never do this. The job doesn't need it, and the tarball sits in a bucket.

### 3.6 GPUs, quotas, regions and prebuilt images
- **Explanation.** Picking a GPU is three choices that must agree:
  1. an accelerator type and count in the worker pool (`model-training/cli.sh:12-13`);
  2. a **GPU-enabled image** (`tf-gpu.*`, `model-training/cli.sh:9`) so that CUDA libraries exist;
  3. **quota** for that GPU type in that **region** (`model-training/cli.sh:14`).
- TF reports what it sees: `tf.config.list_physical_devices("GPU")` (`model-training/package/trainer/task.py:67`).
- **Mental model.** Car rental: you need the right car class, a driver's licence for it (the CUDA image), and a branch that has the car in stock today (regional quota).
- **Common misconceptions.**
  - "Asking for a GPU makes training use it." Not with the `tf-cpu` image: the GPU sits idle.
  - The reverse case is fine: a `tf-gpu` image on a CPU-only machine just falls back to CPU.
  - "Quota is per project." It is per project **and region** **and** GPU type.

### 3.7 Multi-GPU data parallelism with `MirroredStrategy` **[ANIMATE]**
- **Explanation.** `tf.distribute.MirroredStrategy()` (`model-training/package/trainer/task_multi_gpu.py:287`) makes one **replica** of the model per GPU on *one* machine. On each step:
  1. a **global batch** is split across the replicas;
  2. each GPU computes gradients on its slice;
  3. the gradients are **all-reduced** (summed/averaged across GPUs, via NCCL on NVIDIA);
  4. every replica applies the same update, so the copies stay identical.
- **Global batch size.** Because `Dataset.batch` must produce the *global* batch, the code multiplies: `global_batch_size = args.batch_size * num_workers` (`model-training/package/trainer/task_multi_gpu.py:293`).
- **`strategy.scope()`.** Variables (model weights, optimizer slots) must be created inside `with strategy.scope():` (`model-training/package/trainer/task_multi_gpu.py:304-321`) so they become *mirrored* variables.
- **Other strategies the code does not use.**
  - `MultiWorkerMirroredStrategy`: the same idea across several machines. Vertex treats the first worker pool as the single chief replica, so the extra machines go in a second `--worker-pool-spec`. The SDK does that split for you: `replica_count=N` becomes 1 chief + N−1 workers, and a chief count above 1 raises `ValueError` (`aiplatform/utils/worker_spec_utils.py:184-185`, `:225-227` in 1.121.0). Vertex sets the cluster config (`TF_CONFIG`) on each machine.
  - `TPUStrategy`.
  - `ParameterServerStrategy`: asynchronous, with weights held on parameter servers.
  - Model/pipeline parallelism splits *the model* rather than the data; it is needed only when one model doesn't fit on one GPU, which is not the case for MobileNetV2 (≈2.4 M parameters).
  - Vertex's SDK also has a "reduction server" option for faster all-reduce (`reduction_server_replica_count` in `CustomPythonPackageTrainingJob.run`, `aiplatform/training_jobs.py:7779` in 1.121.0).
- **Mental model.** Two students grade halves of the same exam pile with the same rubric. After each pile they meet and average their rubric tweaks, so both rubrics stay identical.
- **Common misconceptions.**
  - "2 GPUs = 2× faster." Not quite. You add all-reduce communication and input-pipeline pressure. On a 936-image dataset, start-up time dominates the total.
  - "The batch size I pass is per GPU, so the learning dynamics are unchanged." The *effective* batch doubles (64) while the learning rate stays 0.001 (`model-training/package/trainer/task_multi_gpu.py:275`), so convergence per epoch changes.
- **Animation idea.**
  1. A stack of 64 cheese images splits into two piles of 32 that slide onto GPU0 and GPU1, each holding an identical copy of the network.
  2. Two gradient arrows rise from the GPUs, meet in the middle (all-reduce), average, and split back down.
  3. Both networks' weights update in sync, with the same colour change on both.

### 3.8 The ML payload: transfer learning with MobileNetV2 (feature extraction vs fine-tuning)
- **Explanation.**
  - `keras.applications.MobileNetV2(weights="imagenet", include_top=False)` gives a pretrained convolutional base (`model-training/package/trainer/task.py:235-237`).
  - `trainable = train_base` (`model-training/package/trainer/task.py:240`) decides between:
    - *feature extraction*: base frozen, about 164 K trainable params;
    - *fine-tuning*: base unfrozen, about 2.39 M trainable params (notebook B outputs, cells 50 and 52).
  - The head is GlobalAveragePooling → Dense(128, relu) → Dense(4, softmax), with **L1 regularisation 0.02** on the kernels and biases of both Dense layers (`model-training/package/trainer/task.py:243-261`). The optimizer is plain SGD (`model-training/package/trainer/task.py:304`).
  - **One difference from the notebooks.** The notebooks call `base_model(input, training=False)` (notebook A cell 47, notebook B cell 48), so MobileNet's BatchNorm layers stay in inference mode even when the base is unfrozen. The repo puts the base straight into a `Sequential` without `training=False` (`model-training/package/trainer/task.py:246-264`), so with `--train_base` the BatchNorm layers run in training mode and update their statistics on each batch of 32.
- **Mental model.** Borrow a trained eye; teach it only the last word, or retrain the whole eye a little.
- **Common misconception.** "A loss of ~100 means training is broken." With L1 = 0.02 on a 1280×128 kernel, the penalty alone starts at roughly 0.02 × Σ|w| ≈ 0.02 × (163,840 × 0.033) ≈ **107**. This is my estimate from Glorot-uniform initialisation. Keras adds that penalty to the reported `loss`, so the repo trainer's loss stays near 100 for a 2-epoch run even when accuracy improves. The notebooks' MobileNet has no regulariser, and their loss is ~0.9. The instructors' own 2021 mushroom run logged `"loss": 82.35` with `"accuracy": 0.873` (the `mobilenetv2_train_base_True_model_metrics.json` inside `dlops-io/models` release v1.0 `experiments.zip`).

---

## 4. Step-by-step walkthrough

### Part A: Colab notebooks (experiment tracking)

**A1. Open Notebook A and get a GPU.**
- **Action:** open the course-site link (`tutorials_demo.md:172`), then File → Save a copy in Drive. Runtime → Change runtime type → GPU (notebook A cell 3).
- **Under the hood:** Colab gives you a VM with a T4. Notebook A's saved output shows TF 2.19.0 (cell 8); the Keras version (3.10.0) is printed only in notebook B (cell 9).
- **Checkpoint:** cell 8 prints `Number of replicas: 1` and lists a `GPU:0` device. `!nvidia-smi` (cell 10) shows `Tesla T4`.
- **If it fails:** with no GPU, everything still runs, but the CNN cells take many times longer.

**A2. Imports and utils.**
- **Action:** run cells 6 and 12.
- **Under the hood:** cell 12 defines `download_file`, `compute_dataset_metrics`, `create_experiment`, `save_model` and `evaluate_save_model`, which together are the home-made tracker.
- **If it fails:** cell 6 imports `tensorflow_hub` and `cv2` but never uses `hub`. If a future Colab image lacks `tensorflow_hub`, delete that line.

**A3. Download and inspect the data.**
- **Action:** run cells 15, 17, 19 and 21.
- **Under the hood:** cell 15 downloads `https://github.com/dlops-io/datasets/releases/download/v4.0/cheese_4_labels.zip` and extracts `datasets/cheese/<label>/*`.
- **Checkpoint:**
  - `Full size of the dataset: 1156` (cell 17 output). The `cheese/` folder in the zip holds 1,018 `.jpg`, 19 `.JPG`, 55 `.jpeg` and 64 `.png` files. The zip also carries a `__MACOSX/` folder of macOS metadata files; it is extracted to `datasets/__MACOSX/` and never read, because the code lists only `datasets/cheese`.
  - The label order differs between runs: notebook A printed `['brie', 'gouda', 'parmigiano', 'gruyere']`, notebook B printed `['gruyere', 'brie', 'parmigiano', 'gouda']`.
  - Cell 21 shows 288–291 images per class, images from 160 px up to 7200 px wide, and "Size in memory: 6679.46 MB" (same output in notebook B cell 22). The PNGs still load, because `tf.image.decode_jpeg` also decodes PNG.
- **If it fails:** a GitHub rate limit or network error appears as `requests.exceptions.HTTPError`. Re-run the cell.

**A4. Split and build `tf.data` pipelines.**
- **Action:** run cells 24, 26 and 28.
- **Checkpoint:** `train_x count: 936`, `validate_x count: 104`, `test_x count: 116`.
- **Pause and ponder:** `validation_percent = 0.2` is defined, so why is validation only 104? See section 10, E4.

**A5. Train five models with the home-made tracker.**
- **Action:** run cell 31 (`create_experiment()`), then the model cells: 33/35/36/37 (2-block CNN: define, train, show `experiment_name`, evaluate+save), 39/41 (4-block), 43/45 (VGG-style), 47/49 (MobileNet frozen) and 51 (MobileNet fine-tuned).
- **Under the hood:** each model ends with a call to `evaluate_save_model(...)` (in the training cell itself, except for the 2-block model, where it is the separate cell 37), which plots curves, evaluates on test and writes the five files per model into `experiment_<ts>/`.
- **Checkpoint:** 30 steps per epoch (936/32 rounded up). In the saved run, MobileNet reaches 67–69 % test accuracy and the scratch CNNs 26–34 %. Times are about 4–8 min per model on a T4; notebook A's 2-block cell is set to `epochs = 1` and took 1.4 min (notebook A cell 54 output).
- **If it fails:** an out-of-memory error on the VGG model means you should lower `batch_size` or restart the runtime. Note that the cell does `K.clear_session()`, but it imports `K` from the legacy `tensorflow.python.keras` (cell 6), so it does not clear Keras 3 state.

**A6. Compare and predict.**
- **Action:** run cells 54, 56, 58 and 59.
- **Checkpoint:** a table sorted by accuracy (as text, see section 10, E22), and `best_model` printed as `experiment_<ts>/mobilenetv2_train_base_….keras`.
- **Watch out:** the prediction cell uses `keras.applications.mobilenet.preprocess_input` (scales to [-1, 1]), while training used `image/255` (scales to [0, 1]). The predictions you see are therefore made on differently scaled inputs (section 10, E13).

**A7. Upload the experiment to GCS.**
- **Action:** run cell 62 (`auth.authenticate_user()`), edit cell 63 (`GCP_PROJECT`, `GCS_BUCKET_NAME`), then run cell 66.
- **Checkpoint:** lines like `uploading file experiment_<ts>/2_block.keras`.
- **If it fails:** you get 403 or `NotFound` if you kept the instructors' bucket `cheese-app-models`.

**A8. Notebook B: the same pipeline with W&B.**
- **Action:**
  - Run `!pip install -q wandb -U` (notebook B cell 5).
  - In Colab's key icon (Secrets), add a secret named `WandB` holding your W&B key and enable notebook access.
  - Run the setup cells: 7 (imports), 9 and 11 (versions, GPU), 13 (utils), 16 (download), 18, 20 and 22 (load, sample images, metrics), 25, 27 and 29 (x/y, split, `tf.data` pipelines; notebook B builds them inline in cell 29, not through a `get_dataset` function), 32 (`create_experiment()`).
  - Run cell 34 (W&B login), then the training cells: 36/38 (2-block), 40/42 (4-block), 44/46 (VGG-style), 48/50 (MobileNet frozen) and 52 (MobileNet fine-tuned).
  - Then 55 (compare), 57 (best model), 59/60 (predict), 64 (`auth.authenticate_user()`) and 66 (upload, step A9).
  - The epochs differ from notebook A: 25 for the 2-block CNN (cell 38, against 1 in notebook A) and 10 for fine-tuned MobileNet (cell 52, against 15).
- **Under the hood:**
  - Cell 7 imports `from wandb.integration.keras import WandbCallback`.
  - Cell 32 sets `LOAD_PREV_TRAINED = False`. Leave it that way (section 10, E16).
  - Each training cell calls `wandb.init(project='cheese-app-demo')`.
  - **Only** the 2-block cell (38) passes `callbacks=[WandbCallback(save_graph=False, save_model=False)]`.
- **Checkpoint:**
  - Cell 34 output: `wandb: Currently logged in as: <you>`.
  - Cell 38 prints `WandbCallback is deprecated…`, which is harmless.
  - On wandb.ai, project `cheese-app-demo` has five runs. Only `2_block` has epoch charts; the others show system metrics only.
  - The two MobileNet runs share one W&B display name, `mobilenetv2_train_base`: cells 50 and 52 set `wandb.run.name = model_name`, and `model_name` there lacks the `_False`/`_True` suffix that `model.name` (and hence the local files) carries.
  - The saved notebook-B copy has no outputs for cells 64 and 66 (execution count empty): the instructors did not run the upload in that copy, so there is no reference output for step A9.
  - No cell calls `wandb.finish()`, so the last run (fine-tuned MobileNet) stays open until the runtime ends. Run `wandb.finish()` yourself after cell 52.
- **If it fails:**
  - `userdata.get` raises `SecretNotFoundError` if the secret name is not exactly `WandB`, or `NotebookAccessError` if notebook access is off.
  - Cell 16 also downloads a **510 MB** legacy `experiments.zip` that you don't need. You can delete that line.

**A9. Notebook B upload.**
- **Action:** run cell 64 (`auth.authenticate_user()`) first, then cell 66, which calls `upload_experiment(data_details)`, defined in cell 13.
- **Under the hood:** it reads your account with `!gcloud config get-value account` (which is why the auth cell must run first), uploads to `cheese-app-models/<your gcloud account>/experiment_<ts>/…` and writes `submit.txt`.
- **Watch out:** the bucket and project are hard-coded *inside* the function (`bucket_name = "cheese-app-models"`, `storage.Client(project="ac215-project")`). Edit cell 13, not a config cell.

### Part B: model-training repo (serverless training)

**B1. Clone and lay out folders.**
- **Action:** clone `https://github.com/dlops-io/model-training` (`README.md:16-17`). Create `secrets/` as a sibling (`README.md:50-58`).
- **Checkpoint:** `ls ..` from inside the repo shows `model-training` and `secrets`.

**B2. Enable the Vertex AI API** (`README.md:19-21`).
- **Checkpoint:** the API page shows "API enabled".

**B3. (For GPU runs) request quota** (`README.md:23-44`).
- **Action:** filter `Quota: Custom model training`, pick `Custom model training Nvidia T4 GPUs per region`, select regions, then EDIT QUOTAS → new limit → SUBMIT REQUEST.
- **Checkpoint:** the approval email arrives, often within hours. Skip this step if you will train on CPU.

**B4. Service account and key** (`README.md:60-64`).
- **Action:** create `model-trainer` with Storage Admin, AI Platform Admin and Vertex AI Administrator. Manage keys → JSON → move the file to `../secrets/model-trainer.json`.
- **If it fails:** an org policy `iam.disableServiceAccountKeyCreation` blocks key creation. Ask the course staff for an exception, or use a personal project.

**B5. Bucket** (`README.md:66-71`).
- **Action:** create a bucket, e.g. `<yourname>-cheese-app-trainer`. The README's `cheese-app-trainer` is surely taken, because bucket names are global.

**B6. W&B key on the host** (`README.md:73-81`).
- **Action:** log in to wandb.ai, open User settings (https://wandb.ai/settings), scroll to `API keys` and copy the key (`README.md:76-79`).
- **Command:**
  ```bash
  export WANDB_KEY=...
  ```
- **Under the hood:** `docker-shell.sh` forwards the *host* variable into the container (`model-training/docker-shell.sh:23`).
- **Checkpoint (my addition):** `echo ${#WANDB_KEY}` prints `40` for a classic W&B key. If it prints `0`, the job will crash later (section 6).

**B7. Edit `docker-shell.sh`.**
- **Action:** change `model-training/docker-shell.sh:8-9` to your bucket and project:
  ```bash
  export GCS_BUCKET_URI="gs://cheese-app-trainer"
  export GCP_PROJECT="ac215-project"
  ```
  (These are the original lines; replace the values.)
- **Note:** the README's copy of this file (`README.md:89-112`) is *not* the real file. It builds without `--platform` and contains bracketed notes like `[REPLACE WITH YOUR BUCKET NAME]` inside shell lines. Edit the real file instead of pasting from the README.

**B8. Build and enter the container.**
- **Command** (`README.md:114-115`; run from inside `model-training/`):
  ```bash
  sh docker-shell.sh
  ```
- **Under the hood:**
  - `docker build -t $IMAGE_NAME --platform=linux/amd64 -f Dockerfile .` (`model-training/docker-shell.sh:14`) builds an amd64 image on any host, emulated on Apple Silicon.
  - The Dockerfile installs the Google Cloud SDK and Docker CE with apt (`model-training/Dockerfile:36-37`), `uv` with pip (`model-training/Dockerfile:40`), and `google-cloud-aiplatform` into `/.venv` (`model-training/Dockerfile:15`, `model-training/Dockerfile:56`).
  - `docker run --rm ... -v "$BASE_DIR":/app -v "$SECRETS_DIR":/secrets ...` (`model-training/docker-shell.sh:17-24`) mounts your repo over `/app`. The venv lives at `/.venv`, so the bind mount does not hide it.
  - The entrypoint activates the service account, sets the project, prints versions, activates the venv and `exec`s bash (`model-training/docker-entrypoint.sh:3-22`).
- **Checkpoint:** you should see
  - `Container is running!!!`
  - `Activated service account credentials for: [model-trainer@<project>.iam.gserviceaccount.com]`
  - `Updated property [core/project].`
  - `Architecture: x86_64`
  - `Environment ready! Virtual environment activated.` (printed *before* the venv is activated, so it is only a label)
  - `Python version: Python 3.13.x`
  - `UV version: uv …`
  - `Activating virtual environment...`
  - then a root shell in `/app`.
- **If it fails:**
  - **The build stops at `model-training/Dockerfile:36-37` (expected in 2026).** That line runs `apt-get install -y google-cloud-sdk google-cloud-sdk-gke-gcloud-auth-plugin jq docker-ce`. Google's `cloud-sdk` apt index (Release dated 2026-10-07, which I fetched for amd64) has no package with either name, only `google-cloud-cli` and `google-cloud-cli-gke-gcloud-auth-plugin` 588.0.0-0, which declare `Replaces/Breaks: google-cloud-sdk (<< 467.0.0-0)`. apt therefore reports that `google-cloud-sdk` has no installation candidate, `docker build` exits non-zero, and `set -e` (`model-training/docker-shell.sh:3`) ends the script before `docker run`. Fix: in `model-training/Dockerfile:37` replace the two `google-cloud-sdk…` names with `google-cloud-cli` (the auth plugin is not needed here), then re-run `sh docker-shell.sh`. This works for the amd64 build that `docker-shell.sh` forces; a native arm64 build needs a newer base image as well. See section 6, item 20.
  - An `ERROR: (gcloud.auth.activate-service-account) …` line saying the key file `/secrets/model-trainer.json` cannot be read means the secrets folder is in the wrong place or the file is misnamed. The script continues into bash anyway, because the entrypoint has no `set -e`.
  - A slow build on M-series Macs is expected (QEMU/Rosetta emulation of apt and pip).

**B9. Review the trainer** (`README.md:121-125`).
- **Action:** open `model-training/package/setup.py` and `model-training/package/trainer/task.py`. Section 5 tours them.
- **Note:** the only declared dependency is `wandb==0.15.11` (`model-training/package/setup.py:5`). TensorFlow, scikit-learn and requests are assumed to be present in Google's prebuilt image.

**B10. Package and upload.**
- **Command** (`README.md:127-129`; run **inside the container**, where `gsutil` and `GCS_BUCKET_URI` exist):
  ```bash
  sh package-trainer.sh
  ```
- **Under the hood** (`model-training/package-trainer.sh:1-4`):
  - `rm -f trainer.tar trainer.tar.gz`
  - `tar cvf trainer.tar package`
  - `gzip trainer.tar`
  - `gsutil cp trainer.tar.gz $GCS_BUCKET_URI/cheese-app-trainer.tar.gz`
  - The local `trainer.tar.gz` is git-ignored (`model-training/.gitignore:4`).
- **Checkpoint:**
  - `tar` lists `package/`, `package/PKG-INFO`, `package/setup.cfg`, `package/setup.py`, `package/trainer/`, `package/trainer/__init__.py`, `package/trainer/task.py` and `package/trainer/task_multi_gpu.py`;
  - `gsutil` prints `Copying file://trainer.tar.gz …` and `Operation completed over 1 objects`;
  - `gsutil ls $GCS_BUCKET_URI` (my addition) lists `…/cheese-app-trainer.tar.gz`.
- **If it fails:**
  - `AccessDeniedException: 403` means the SA lacks Storage Admin on that bucket, or the bucket is in another project.
  - `BucketNotFoundException` means a typo in `GCS_BUCKET_URI`.

**B11. Submit the job.**
- **Action first** (`README.md:133-149`): open `cli.sh` and make "any required changes", in practice `GCP_REGION` (`model-training/cli.sh:14`) if your quota or bucket is elsewhere, and `ACCELERATOR_TYPE` (`model-training/cli.sh:12`) if you switch to the GPU block. The README lists accelerator types and regions for this.
- **Command** (`README.md:150`):
  ```bash
  sh cli.sh
  ```
- **Under the hood:**
  - `cli.sh` builds a unique `DISPLAY_NAME` from `openssl rand -hex 6` (`model-training/cli.sh:5-6`).
  - It sets `CMDARGS="--model_name=mobilenetv2,--train_base,--epochs=2,--batch_size=32,--wandb_key=$WANDB_KEY"` (`model-training/cli.sh:19`).
  - It then runs the **CPU** variant. The GPU block at `model-training/cli.sh:22-27` is commented out, and the CPU block overrides the image to `tf-cpu.2-17.py310` (`model-training/cli.sh:31-37`).
  - `gcloud` splits `--args` on commas, so the job's `sys.argv` becomes `['--model_name=mobilenetv2', '--train_base', '--epochs=2', '--batch_size=32', '--wandb_key=…']`.
- **Checkpoint:** approximately:
  ```
  Using endpoint [https://us-central1-aiplatform.googleapis.com/]
  CustomJob [projects/<num>/locations/us-central1/customJobs/<id>] is submitted successfully.
  ```
  followed by suggested `gcloud ai custom-jobs describe …` and `… stream-logs …` commands.
- **If it fails:** see section 6, items 4–8 (API disabled, permission, quota, region).

**B12. Watch the job** (`README.md:156-158`).
- **Action:** open Vertex AI → Training → Custom jobs (https://console.cloud.google.com/vertex-ai/training/custom-jobs), or from the container run (my additions):
  ```bash
  gcloud ai custom-jobs list --region=us-central1
  gcloud ai custom-jobs stream-logs <JOB_ID> --region=us-central1
  ```
- **Checkpoint:** after a few minutes of provisioning, the logs show, in order:
  - `pip` installing `cheese-app-trainer` and `wandb-0.15.11`;
  - `tensorflow version 2.17.…` and `Number of replicas: 1`;
  - `Downloading data...`, `Labels: [...]`, `Full size of the dataset: 1156`, and `train_x count: 936`, `validate_x count: 104`, `test_x count: 116`;
  - `wandb: Appending key for api.wandb.ai to your netrc file: /root/.netrc` (from `wandb.login`, `model-training/package/trainer/task.py:153`; on a fresh VM wandb 0.15.11 prints no "logged in" line at this point, because its `login()` finds no configured key before it writes yours: `wandb/sdk/wandb_login.py:132-142`, `:288-298`);
  - `Train model`, then the model summary, followed by a stray `None` (from `print(model.summary())`, `model-training/package/trainer/task.py:308`);
  - at `wandb.init` (`model-training/package/trainer/task.py:313`): ``wandb: Currently logged in as: <user> (<entity>). Use `wandb login --relogin` to force relogin`` (printed by the login check inside `wandb.init`, `wandb/sdk/wandb_init.py:308-314`), `wandb: Tracking run with wandb version 0.15.11`, and `wandb: … View run at https://wandb.ai/<entity>/cheese-training-vertex-ai/runs/<id>` (a rocket emoji may precede "View run" if the log is UTF-8);
  - `Epoch 1/2`, `Epoch 2/2` with `loss` values around 100 (section 3.8);
  - `Training execution time (mins) …` and `Training Job Complete`.
  The state ends as `JOB_STATE_SUCCEEDED`.
- **If it fails:** the job page shows "Failed" with an error snippet. Click "View logs".

**B13. (Optional) GPU instead of CPU.**
- **Action:** in `cli.sh`, uncomment `model-training/cli.sh:22-27` **and** comment out `model-training/cli.sh:31-37`. If you do only the first, you submit *two* jobs with the same display name.
- **Checkpoint:** the logs show `GPU Available:  [PhysicalDevice(name='/physical_device:GPU:0', device_type='GPU')]`.
- **If it fails:** a quota error (section 6).
- **README mismatch:** the README presents GPU as the main path and CPU as optional (`README.md:132-154`), but the code defaults to CPU (commit `3efb2d5`, "Updated cli to default to CPU").

**B14. View W&B** (`README.md:160-163`).
- **Action:** open wandb.ai → project `cheese-training-vertex-ai`.
- **Checkpoint:**
  - a run named `mobilenetv2_train_base_True` (from `name=model.name`, `model-training/package/trainer/task.py:321`, and the model name built at `model-training/package/trainer/task.py:263`);
  - Config: `learning_rate`, `epochs`, `batch_size`, `model_name`, plus `execution_time` added at the end;
  - System charts (CPU, memory, GPU if any) and the console output in the Logs tab.
- **Not there:** loss and accuracy curves. The README says "You will view the training metrics tracked and automatically updated" (`README.md:163`), but `model.fit` has no callback (`model-training/package/trainer/task.py:326-331`). Exercise 1 adds one.

**B15. (Optional) Multi-GPU** (`README.md:165-170`).
- **Command:**
  ```bash
  sh cli-multi-gpu.sh
  ```
- **Under the hood:**
  - `n1-standard-32`, `NVIDIA_TESLA_T4` × 2, image `tf-gpu.2-14.py310`, module `trainer.task_multi_gpu`, 5 epochs (`model-training/cli-multi-gpu.sh:4-16`).
  - The trainer creates `MirroredStrategy`, doubles the batch, builds the model in `strategy.scope()`, and logs to W&B project `cheese-training-multi-gpu-vertex-ai` (`model-training/package/trainer/task_multi_gpu.py:286-334`).
- **Checkpoint:** the logs show `Number of replicas: 2`. W&B config shows `batch_size: 32` and `global_batch_size: 64`. Each epoch has 15 steps (936/64 rounded up).
- **If it fails:** you need quota for 2 T4s *and* 32 vCPUs of custom training in that region.

**B16. (Not in README) the Python-SDK launcher `cli.py`.**
- **Command:** `python cli.py` would submit a `CustomPythonPackageTrainingJob` with a T4 and `tf-gpu.2-14` (`model-training/cli.py:21-51`).
- **As shipped it does not work:**
  - It reads `os.environ["GCP_REGION"]` (`model-training/cli.py:7`), which nothing exports, so you get `KeyError: 'GCP_REGION'`.
  - Its `CMDARGS = ["--epochs=15", "--batch_size=16"]` (`model-training/cli.py:31`) omits `--wandb_key`, so the job crashes at `wandb.login` (section 6).
- **How the SDK version differs from `cli.sh`** (`model-training/cli.py:40-51`):
  - `CustomPythonPackageTrainingJob.run` creates a *training pipeline*, which in turn creates a custom job, so look under Training → Training pipelines in the console.
  - `base_output_dir=MODEL_DIR` makes Vertex set `AIP_MODEL_DIR=<base_output_dir>/model/` inside the job (documented in the `run()` docstring, `aiplatform/training_jobs.py:7936` in 1.121.0). `task.py` ignores it.
  - `sync=False` makes `run()` return immediately, but the work continues in a thread of the SDK's `concurrent.futures.ThreadPoolExecutor` (`aiplatform/initializer.py:707`, `aiplatform/base.py:413` in 1.121.0). Python joins those worker threads at interpreter exit, so `python cli.py` still does not return to the prompt until the pipeline finishes (or you press Ctrl-C).
  - No Model Registry upload happens, because the job is constructed without `model_serving_container_image_uri` (`model-training/cli.py:23-29`). In the SDK that is the switch: only when a serving image is set does `run()` upload a model, naming it `<display_name>-model` if `model_display_name` is None; passing a `model_display_name` *without* a serving image raises `RuntimeError` (`aiplatform/training_jobs.py:1493-1502` in 1.121.0). So `model_display_name=None` here changes nothing.
- **Value:** the SDK version of the same idea. It is the bridge to L15, where `ml-workflow/src/model-training/cli.py` is used.

**B17. Clean up.**
- **Action:**
  - `exit` the container (it is `--rm`).
  - Optionally `gsutil rm $GCS_BUCKET_URI/cheese-app-trainer.tar.gz`.
  - Confirm no job is `RUNNING`/`PENDING` in the console.
  - At the end of term, delete the SA key.

---

## 5. Code tour

```
model-training/
├── README.md                 the tutorial (170 lines)
├── Dockerfile                control-console image: python:3.13-slim + gcloud/gsutil + uv venv (/.venv)
├── docker-shell.sh           builds (linux/amd64) and runs that image; mounts repo + ../secrets; passes env
├── docker-entrypoint.sh      activates the service account, sets project, activates venv, opens bash
├── pyproject.toml / uv.lock  console's Python deps: only google-cloud-aiplatform (used by cli.py)
├── package-trainer.sh        tar+gzip package/ and gsutil cp it to $GCS_BUCKET_URI/cheese-app-trainer.tar.gz
├── cli.sh                    gcloud ai custom-jobs create: 1 replica, n1-standard-4, CPU by default
├── cli-multi-gpu.sh          same, n1-standard-32 + 2×T4, module trainer.task_multi_gpu
├── cli.py                    (not in README) Python-SDK launcher: CustomPythonPackageTrainingJob
├── package/
│   ├── PKG-INFO, setup.cfg   leftover sdist-style metadata; pip rebuilds metadata from setup.py (PKG-INFO even says "Cheese App Trainer")
│   ├── setup.py              name cheese-app-trainer, install_requires wandb==0.15.11
│   └── trainer/
│       ├── __init__.py       makes trainer a package (empty)
│       ├── task.py           the single-device trainer (argparse → data → MobileNetV2 → fit → W&B)
│       └── task_multi_gpu.py same + MirroredStrategy, global batch, strategy.scope()
└── *.png                     README screenshots (quota pages, W&B key, architecture)
```

**Excerpt 1: the console container is a cockpit, not a trainer.**
`model-training/docker-shell.sh:14-24`
```bash
docker build -t $IMAGE_NAME --platform=linux/amd64 -f Dockerfile .

# Run Container
docker run --rm --name $IMAGE_NAME -ti \
-v "$BASE_DIR":/app \
-v "$SECRETS_DIR":/secrets \
-e GOOGLE_APPLICATION_CREDENTIALS=/secrets/model-trainer.json \
-e GCP_PROJECT=$GCP_PROJECT \
-e GCS_BUCKET_URI=$GCS_BUCKET_URI \
-e WANDB_KEY=$WANDB_KEY \
$IMAGE_NAME
```
- `--platform=linux/amd64`: everyone, including Apple Silicon users, gets an amd64 image. It is emulated on M-series Macs, which only matters for build speed, because the container runs only `gcloud`/`gsutil`.
- `-v "$BASE_DIR":/app` makes your edits to `task.py` visible inside without a rebuild.
- `-v "$SECRETS_DIR":/secrets` plus `GOOGLE_APPLICATION_CREDENTIALS` is the key hand-off.
- `-e WANDB_KEY=$WANDB_KEY` copies a *host* variable. If you forgot to export it, the container gets an empty string and nothing warns you.
- No `-p`: this container serves nothing.

**Excerpt 2: why the bind mount doesn't erase the venv.**
`model-training/Dockerfile:52-62`
```dockerfile
# Copy dependency files first for better layer caching
COPY --chown=app:app pyproject.toml uv.lock* ./

# Install dependencies in a separate layer for better caching
RUN uv sync --frozen

# Copy the rest of the source code
COPY --chown=app:app . ./

# Entry point
ENTRYPOINT ["/bin/bash","docker-entrypoint.sh"]
```
- `UV_PROJECT_ENVIRONMENT=/.venv` (`model-training/Dockerfile:15`) puts the venv *outside* `/app`, so `-v "$BASE_DIR":/app` hides the copied source but not the installed packages.
- `uv sync --frozen` installs exactly `uv.lock` (google-cloud-aiplatform 1.120.0, `model-training/uv.lock:147-148`).
- There is no `USER app` line, so the shell runs as root even though the `app` user is created at `model-training/Dockerfile:44-47`.

**Excerpt 3: packaging is four shell lines.**
`model-training/package-trainer.sh:1-4`
```bash
rm -f trainer.tar trainer.tar.gz
tar cvf trainer.tar package
gzip trainer.tar
gsutil cp trainer.tar.gz $GCS_BUCKET_URI/cheese-app-trainer.tar.gz
```
- Line 2 tars the *folder* `package`, so the archive's single top-level directory contains `setup.py`. That is the sdist layout pip expects.
- Line 4 gives the object a fixed name. Every new upload **overwrites** the previous code, so a queued job that has not started yet may pick up the newer tarball (the VM fetches the package when the job starts). Use versioned names if you run several variants at once.

**Excerpt 4: the package's declared dependencies.**
`model-training/package/setup.py:5-13`
```python
REQUIRED_PACKAGES = ["wandb==0.15.11"]

setup(
    name="cheese-app-trainer",
    version="0.0.1",
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    description="Cheese App Trainer Application",
)
```
- `install_requires` is what Vertex's `pip install` adds on top of the prebuilt image, here only wandb, pinned to a 2023 release.
- `find_packages()` discovers `trainer`; this is why `python-module=trainer.task` works.
- Everything else (TF, scikit-learn, requests) is *assumed* to be in the image. That is fragile: pin what you import.

**Excerpt 5: the job definition, part 1 (variables).**
`model-training/cli.sh:5-19`
```bash
export UUID=$(openssl rand -hex 6)
export DISPLAY_NAME="cheese_training_job_$UUID"
export MACHINE_TYPE="n1-standard-4"
export REPLICA_COUNT=1
export EXECUTOR_IMAGE_URI="us-docker.pkg.dev/vertex-ai/training/tf-gpu.2-17.py310:latest"
export PYTHON_PACKAGE_URI=$GCS_BUCKET_URI/cheese-app-trainer.tar.gz
export PYTHON_MODULE="trainer.task"
export ACCELERATOR_TYPE="NVIDIA_TESLA_T4"
export ACCELERATOR_COUNT=1
export GCP_REGION="us-central1" # Adjust region based on you approved quotas for GPUs

# Change the number of epochs
#export CMDARGS="--model_name=mobilenetv2,--epochs=2,--batch_size=32,--wandb_key=$WANDB_KEY"
#export CMDARGS="--model_name=mobilenetv2,--train_base,--epochs=2,--batch_size=32,--wandb_key=$WANDB_KEY"
export CMDARGS="--model_name=mobilenetv2,--train_base,--epochs=2,--batch_size=32,--wandb_key=$WANDB_KEY"
```
- `UUID`/`DISPLAY_NAME` give each submission a unique, findable name.
- `MACHINE_TYPE`, `ACCELERATOR_TYPE` and `ACCELERATOR_COUNT` are the hardware.
- `EXECUTOR_IMAGE_URI` is Google's prebuilt TF 2.17 GPU image. It is overridden for CPU at line 31.
- `PYTHON_PACKAGE_URI` must match what `package-trainer.sh` uploaded.
- `PYTHON_MODULE` is what `python -m` runs.
- `CMDARGS` is a comma-separated list. `--train_base` is a bare flag, which means fine-tune the whole MobileNet: slower, especially on CPU. The secret key is embedded here.

**Excerpt 6: the job definition, part 2 (the actual call; CPU path).**
`model-training/cli.sh:30-37`
```bash
# Run training with No GPU
export EXECUTOR_IMAGE_URI="us-docker.pkg.dev/vertex-ai/training/tf-cpu.2-17.py310:latest"
gcloud ai custom-jobs create \
  --region=$GCP_REGION \
  --display-name=$DISPLAY_NAME \
  --python-package-uris=$PYTHON_PACKAGE_URI \
  --worker-pool-spec=machine-type=$MACHINE_TYPE,replica-count=$REPLICA_COUNT,executor-image-uri=$EXECUTOR_IMAGE_URI,python-module=$PYTHON_MODULE \
  --args=$CMDARGS
```
- `--worker-pool-spec` packs one worker pool into `key=value` pairs. There is no `accelerator-type` here, which makes this the CPU path.
- `--python-package-uris` tells the prebuilt image what to `pip install`.
- `--args=$CMDARGS` is unquoted. That is fine as long as no value contains spaces.

**Excerpt 7: the flags the trainer accepts.**
`model-training/package/trainer/task.py:45-54`
```python
parser.add_argument(
    "--epochs", dest="epochs", default=10, type=int, help="Number of epochs."
)
parser.add_argument(
    "--batch_size", dest="batch_size", default=16, type=int, help="Size of a batch."
)
parser.add_argument(
    "--wandb_key", dest="wandb_key", default="16", type=str, help="WandB API Key"
)
args = parser.parse_args()
```
- `--wandb_key` defaults to `"16"`: a placeholder that is guaranteed to fail wandb's 40-character check (section 6).
- `--epochs` and `--batch_size` are honoured.
- `--lr` (line 30) and `--model-dir` (lines 27-29) are parsed but never used: `learning_rate = 0.001` is hard-coded at line 274, and no model is saved.

**Excerpt 8: the split (and its bug).**
`model-training/package/trainer/task.py:138-146`
```python
# Split data into train / test
train_validate_x, test_x, train_validate_y, test_y = train_test_split(
    data_x, data_y, test_size=test_percent
)

# Split data into train / validate
train_x, validate_x, train_y, validate_y = train_test_split(
    train_validate_x, train_validate_y, test_size=test_percent
)
```
- Both calls use `test_percent`. `validation_percent = 0.2` (line 136) is dead.
- Result: test = ceil(0.1 × 1156) = 116, validation = ceil(0.1 × 1040) = 104, train = 936. This matches the logs.
- There is no `random_state` and no `stratify`, so every job sees a different split.

**Excerpt 9: creating the W&B run.**
`model-training/package/trainer/task.py:312-322`
```python
# Initialize a W&B run
wandb.init(
    project="cheese-training-vertex-ai",
    config={
        "learning_rate": learning_rate,
        "epochs": epochs,
        "batch_size": batch_size,
        "model_name": model.name,
    },
    name=model.name,
)
```
- `project=` groups runs.
- `config=` is the correct way to record hyperparameters; contrast notebook B in Excerpt 12.
- `name=model.name` makes every fine-tuning run share the display name `mobilenetv2_train_base_True`. Tell runs apart by their id or by adding the job's `DISPLAY_NAME`.
- The run starts *after* data download and model build. A crash before line 313 never appears in W&B, only in Cloud Logging.

**Excerpt 10: training, and why W&B shows no curves.**
`model-training/package/trainer/task.py:324-338`
```python
# Train model
start_time = time.time()
training_results = model.fit(
    train_data,
    validation_data=validation_data,
    epochs=epochs,
    verbose=1,
)
execution_time = (time.time() - start_time) / 60.0
print("Training execution time (mins)", execution_time)

# Update W&B
wandb.config.update({"execution_time": execution_time})
# Close the W&B run
wandb.run.finish()
```
- `model.fit(...)` has **no `callbacks=`**. Commit `88f3374` ("removed ca;llback") deleted `callbacks=[WandbCallback()]` on 2025-10-15, less than an hour after the image moved from TF 2.14 to 2.17 (commit `1c03dd5`).
- TF 2.17 ships Keras 3. The same commit also dropped `dtype="float32"` from `to_categorical`, which Keras 3 no longer accepts. Both point to Keras 3 incompatibility with `wandb==0.15.11`'s legacy callback; that is my inference.
- Line 336: `wandb.config.update` stores the run time as config.
- Line 338: `wandb.run.finish()` flushes the run.

**Excerpt 11: data parallelism: strategy, replicas, global batch.**
`model-training/package/trainer/task_multi_gpu.py:287-301`
```python
strategy = tf.distribute.MirroredStrategy()
# Get number of replicas
num_workers = strategy.num_replicas_in_sync

# Batch size needs to be scaled up to number of workers
# `tf.data.Dataset.batch` expects the global batch size
global_batch_size = args.batch_size * num_workers

# Data
train_data, validation_data, test_data = get_dataset(
    image_width=image_width,
    image_height=image_height,
    num_channels=num_channels,
    batch_size=global_batch_size,
)
```
- Line 287 creates one replica per visible GPU.
- Line 289: `num_replicas_in_sync` is 2 on a 2×T4 machine.
- Line 293: global batch = 32 × 2 = 64, because `Dataset.batch` must yield the global batch and Keras splits it across replicas.
- Lines 304-321, which follow this excerpt, wrap model creation, the optimizer and `compile` in `with strategy.scope():` so that the weights become mirrored variables.
- The learning rate is *not* scaled with the batch.
- A second `MirroredStrategy` is also created at line 62, only for printing; the model uses the one from line 287.

**Excerpt 12: notebook B's W&B setup (the anti-pattern to avoid).**
`colab/L13_wandb_tracking.ipynb` cell 38, source lines 41-50:
```python
# W&B
wandb.init(project='cheese-app-demo')
wandb.config = {
  "learning_rate": learning_rate,
  "epochs": epochs,
  "batch_size": batch_size,
  "model_name": model_name
}
wandb.run.name = model_name
wandb.run.save("test")
```
- `wandb.config = {...}` *rebinds* the module attribute to a plain dict, so this config is likely never sent. I verified in wandb 0.15.11 that `wandb.config` is just a module attribute set by `set_global`. The notebook installs the latest wandb, where I assume the same design. Prefer `wandb.init(project=..., config={...}, name=...)`, as the repo does.
- `wandb.run.save("test")` is not "save the run". `Run.save(glob)` uploads files matching the glob `test`.
- Line 60 of this cell, `callbacks=[WandbCallback(save_graph=False, save_model=False)]`, is what produces the curves, and it appears only in this first model's cell.

---

## 6. Gotchas and common errors

1. **`WANDB_KEY` not exported on the host → job dies minutes after you pay for it.**
   - **Symptom:** the job fails after the dataset download with `wandb.errors.UsageError: api_key not configured (no-tty). call wandb.login(key=[your_api_key])`.
   - **Cause:**
     - `docker-shell.sh` forwards an empty variable (`model-training/docker-shell.sh:23`);
     - `cli.sh` then sends `--wandb_key=` (`model-training/cli.sh:19`);
     - with an empty key, `wandb.login` falls through to prompting (`wandb/sdk/wandb_login.py:290-298` in 0.15.11), which raises on a no-TTY VM (`wandb/sdk/wandb_login.py:228`).
   - **Fix:** `export WANDB_KEY=...` in the **host** terminal *before* `sh docker-shell.sh`. Check with `echo ${#WANDB_KEY}` inside the container.

2. **Using `cli.py`, or omitting `--wandb_key` → "API key must be 40 characters long, yours was 2".**
   - **Cause:** the default `"16"` (`model-training/package/trainer/task.py:52`) is passed to `wandb.login`, and `write_key` checks the length (`wandb/sdk/lib/apikey.py:238-239` in 0.15.11).
   - **Fix:** always pass a real `--wandb_key`. Better: make the default `os.environ.get("WANDB_API_KEY")` and fail fast.
   - **Related:** if your W&B account issues keys in a format that is not 40 characters, the old pin `wandb==0.15.11` would reject even a correct key. Bump the pin in `model-training/package/setup.py:5`. I could not check the current W&B key format (section 10).

3. **`KeyError: 'GCP_REGION'` when running `python cli.py`.**
   - **Cause:** `model-training/cli.py:7` reads an env var that `docker-shell.sh` never sets (only `model-training/cli.sh:14` sets a shell-local one).
   - **Fix:** `export GCP_REGION=us-central1` in the container first.

4. **Vertex AI API not enabled.**
   - **Symptom:** `PERMISSION_DENIED: Vertex AI API has not been used in project … or it is disabled`.
   - **Fix:** enable `aiplatform.googleapis.com` (`README.md:19-21`), wait a minute, and retry.

5. **IAM errors.**
   - `403 … does not have storage.objects.create access` from `gsutil` → add Storage Admin to `model-trainer`.
   - `Permission 'aiplatform.customJobs.create' denied` from `gcloud ai custom-jobs create` → add Vertex AI Administrator. The README lists three roles (`README.md:62`).
   - Make sure the key is for the **same project** as `GCP_PROJECT`.

6. **GPU quota.**
   - **Symptom:** job creation (or the job itself) fails with a message that quota `aiplatform.googleapis.com/custom_model_training_nvidia_t4_gpus` is exceeded in `us-central1`.
   - **Cause:** new projects often have 0. The multi-GPU job needs 2, plus 32 vCPUs on the CPU quota for custom training.
   - **Fix:** request quota (`README.md:23-44`), change `GCP_REGION` to a region where it was approved (`model-training/cli.sh:14`), or use the CPU default.

7. **Long `PENDING`/`QUEUED`.**
   - **Symptom:** the job sits for 10+ minutes.
   - **Cause:** no capacity for that GPU in that region right now.
   - **Fix:** wait, cancel and retry in another region, or use CPU.

8. **Image/hardware mismatch.**
   - `tf-cpu.*` with `accelerator-type=…` gives a GPU you pay for but never use: the logs show `GPU Available:  []`.
   - `tf-gpu.*` without accelerators works but pulls a larger image.
   - Keep `EXECUTOR_IMAGE_URI` (`model-training/cli.sh:9`, `model-training/cli.sh:31`) consistent with the accelerator lines.

9. **Uncommenting the GPU block without commenting the CPU block → two jobs.**
   - **Cause:** `cli.sh` would run both `gcloud ai custom-jobs create` blocks (`model-training/cli.sh:22-27` and `model-training/cli.sh:32-37`), with the same `DISPLAY_NAME`.

10. **Edited `task.py` but the job runs the old code.**
    - **Cause:** Vertex runs the tarball in GCS, not your working tree.
    - **Fix:** re-run `sh package-trainer.sh` after every edit (`model-training/package-trainer.sh:4`). Conversely, rebuilding the Docker image is *not* needed for trainer edits.

11. **Secrets folder in the wrong place.**
    - **Symptom:** the banner shows a `gcloud.auth.activate-service-account` error about `/secrets/model-trainer.json`, and then every `gcloud` or `gsutil` call says there is no active account.
    - **Cause:** `SECRETS_DIR=$(pwd)/../secrets/` (`model-training/docker-shell.sh:7`) depends on **where you run the script**. Run it from inside `model-training/`.

12. **Copy-pasting the README's docker-shell block.**
    - **Symptom:** syntax errors, or a variable that contains `[REPLACE`.
    - **Cause:** `README.md:93-94` and `README.md:110` put bracketed notes on the same line as shell code. On line 110 this also breaks the `\` line continuation.
    - **Fix:** edit `model-training/docker-shell.sh` itself.

13. **Apple Silicon.**
    - The script forces `linux/amd64` (`model-training/docker-shell.sh:14`). On M1–M4 this is emulated: the build is slow, but runtime is fine for `gcloud`.
    - The README still shows an `arm64/v8` line "for M1/2 chip macs" (`README.md:100-101`). Ignore it.
    - `Architecture: x86_64` in the banner is expected.

14. **W&B key leaks.**
    - **Cause:** `--wandb_key=<key>` becomes part of the job spec. Anyone with Vertex AI viewer access on the project can read it in the console or with `gcloud ai custom-jobs describe`. It is also in your shell history if you typed it inline.
    - **Fix:** use a dedicated W&B key and rotate it, or read it inside the job from Secret Manager. Never commit it.

15. **Loss ≈ 100 looks like divergence.** It isn't. It is the L1 penalty (`model-training/package/trainer/task.py:243-261`); see section 3.8. Judge by `accuracy`/`val_accuracy`, or log the cross-entropy separately.

16. **Labels can change order between runs.**
    - **Cause:** `label_names = os.listdir(base_path)` (`model-training/package/trainer/task.py:106`) has no guaranteed order. The two notebooks printed different orders.
    - **Consequence:** the trainer doesn't save `label2index`, so a model from one run cannot be decoded reliably.
    - **Fix:** `sorted(os.listdir(...))`, and save the mapping next to the model.

17. **Old pins vs new runtimes.**
    - `wandb==0.15.11` depends on `pathtools` (wheel METADATA). That is fine in the job's Python 3.10, but if you try to `pip install` the package locally on Python 3.12+ it is a likely failure point (pathtools' setup uses the removed `imp` module; I did not test this).
    - The local console container is Python 3.13 and has no TensorFlow. Don't try to run `task.py` there.

18. **Bucket name.** `gs://cheese-app-trainer` (`model-training/docker-shell.sh:8`) almost certainly belongs to someone else (bucket names are global). You get `403` or `BucketNotFound` until you change it.

19. **Notebook B pulls 510 MB you don't need.** Cell 16 downloads `models/releases/download/v1.0/experiments.zip` (509,683,967 bytes). Remove that call unless you deliberately set `LOAD_PREV_TRAINED`, which you shouldn't (section 10, E16).

20. **`docker build` fails: `google-cloud-sdk` has no installation candidate.**
    - **Symptom:** during `sh docker-shell.sh`, the `RUN apt-get update && apt-get install -y google-cloud-sdk google-cloud-sdk-gke-gcloud-auth-plugin jq docker-ce` step fails with apt's "Package google-cloud-sdk is not available, but is referred to by another package … However the following packages replace it: google-cloud-cli" and "has no installation candidate". The script stops there because of `set -e` (`model-training/docker-shell.sh:3`).
    - **Cause:** `model-training/Dockerfile:36-37` uses the old package names. Google's `cloud-sdk` apt index (Release dated 2026-10-07) lists only `google-cloud-cli` and `google-cloud-cli-gke-gcloud-auth-plugin` (588.0.0-0), which `Replaces/Breaks` the old names below 467.0.0.
    - **Fix:** change `model-training/Dockerfile:37` to `apt-get install -y google-cloud-cli jq docker-ce`. `google-cloud-cli` ships `gcloud` and `gsutil` (its index entry `Conflicts: gsutil`, the standalone package). Nothing in this tutorial needs the GKE auth plugin.
    - **Keep `--platform=linux/amd64` with this fix.** The fix works because the **amd64** `google-cloud-cli` packages in the index declare no `python3` dependency (they bundle their own Python). The **arm64** packages from 554.0.0-0 on declare `Depends: python3 (>= 3.10)` (588.0.0-0: `python3 (>= 3.10), python3 (<< 3.16)`), and Debian bullseye's `python3` is 3.9; the Python 3.13 in `python:3.13-slim-*` is built into `/usr/local` and is invisible to apt. So a native arm64 build (for example the README's variant without `--platform`, `README.md:99-101`) would still fail with an unmet `python3 (>= 3.10)` dependency. For a native arm64 build, also switch the base to `python:3.13-slim-bookworm` (bookworm's `python3` is 3.11).

21. **Notebook B's `execution_time` never reaches W&B either.** After cell 38 rebinds `wandb.config` to a plain dict, the final `wandb.config.update({"execution_time": execution_time})` in the same cell is `dict.update` on that dict (section 10, E14). Use `wandb.run.config.update(...)` or pass `config=` to `wandb.init`.

22. **A second `sh docker-shell.sh` while the first container is still open.**
    - **Symptom:** after the (cached) build, `docker run` fails with `Conflict. The container name "/model-training-cli" is already in use by container …`, and `set -e` ends the script.
    - **Cause:** `docker run --rm --name $IMAGE_NAME` (`model-training/docker-shell.sh:17`) gives the container a fixed name; only one can exist at a time.
    - **Fix:** use the open shell, or open a second shell in the same container with `docker exec -it model-training-cli bash` (my command; note that this skips the entrypoint, so run `source /.venv/bin/activate` yourself if you need `cli.py`).

---

## 7. Where this sits in the course

**What earlier lectures gave you**
- **L2–L4 (containers, mega-pipeline):** the "one container per job + a bind-mounted source folder" pattern. `docker-shell.sh` here is the same idiom.
- **L10 (cheese-app-v0, cloud connect):** service-account keys kept in a sibling `secrets/` folder, `GOOGLE_APPLICATION_CREDENTIALS`, and buckets.
- **L11 (data labeling and DVC versioning):** how to version a dataset. Note that L13's trainer does *not* use a versioned dataset from GCS/DVC; it downloads a fixed GitHub release zip (`model-training/package/trainer/task.py:96-100`).
- **L12 (App Design):** no tutorial (`tutorials_demo.md:162-163`).

**What L13 adds**
1. A tracked experiment loop: a home-made tracker, then W&B.
2. Notebook → script → pip-installable package.
3. Cloud training on rented hardware (CPU/GPU) without managing VMs.
4. One-machine multi-GPU data parallelism.

**What comes next**
- **L14 (`serverless-deployment`):** Cloud Run / Cloud Functions for serving containers. It does not reuse this repo.
- **L15 (`model-deployment` + `ml-workflow`)** builds directly on L13:
  - `ml-workflow/src/model-training/` is a copy of this repo whose `task.py` comments out every W&B line, replaces `--wandb_key` with `--bucket_name`, and adds a serving signature plus `ARTIFACT_URI = f"gs://{args.bucket_name}/model"` and `tf.saved_model.save(model, ARTIFACT_URI, signatures={"serving_default": serving_function})` (`ml-workflow/src/model-training/package/trainer/task.py:347-383`). That is exactly the "save the model" step L13 lacks.
  - `model-deployment/README.md:54` says the weights "are stored in WandB following the serverless training we did in the previous tutorials". The commented-out code expects a W&B artifact `ac215-harvard/cheese-app-demo/model-mobilenetv2_train_base_True` (`model-deployment/cli.py:70-77`). Nothing in today's L13 code creates such an artifact: both the repo and notebook B disable model saving. So L15 actually downloads the model from a GitHub release (`model-deployment/cli.py:80-84`; README line 56 explains why).
- **Milestone 3** requires "Experiment tracking using Weights & Biases (W&B) or an equivalent tool" and "Serverless training on Vertex AI … with at least one training run logged and reproducible" (`milestone3.md:43-44`), plus multi-GPU "If applicable" (`milestone3.md:45`).

**This repo is not a cheese-app vN.** Its only other branch is the pre-uv version. `git diff --stat origin/pipenv main`:

```
 Dockerfile                        |  40 ++-
 LICENSE                           |  21 --
 Pipfile                           |  12 -
 Pipfile.lock                      | 480 -------------------------
 cli.sh                            |   4 +-
 docker-entrypoint.sh              |  14 +-
 docker-shell.bat                  |   0
 docker-shell.sh                   |   3 +-
 package/trainer/task.py           |  13 +-
 package/trainer/task_multi_gpu.py |  13 +-
 pyproject.toml                    |   9 +
 uv.lock                           | 731 ++++++++++++++++++++++++++++++++++++++
 12 files changed, 788 insertions(+), 552 deletions(-)
```

The meaningful changes, all from commits `1c03dd5`, `88f3374` and `b9aee1c` (2025-10-15/16):
- **Console image:** `ubuntu:20.04` + Python 3.9 + Pipenv became `python:3.13-slim-bullseye` + uv. The venv is at `/.venv`, and the entrypoint sources it instead of `pipenv shell`.
- **Build platform:** `docker-shell.sh` changed from `--platform=linux/arm64/v8` to `--platform=linux/amd64`.
- **Training image:** `cli.sh` moved from `tf-gpu/cpu.2-14.py310` to `2-17.py310`. `cli-multi-gpu.sh` and `cli.py` were **not** updated and still use 2-14.
- **Trainers:** `callbacks=[WandbCallback()]` was removed and `to_categorical(..., dtype="float32")` became `to_categorical(...)`, the Keras 3 compatibility edits.

Earlier history: commit `a3d2e0b` (2024-10-15) converted the repo from the "Mushroom App" (3 classes, `mushrooms_3_labels.zip`) to the cheese app and removed a TF-Hub model variant. Commit `3efb2d5` made CPU the default.

---

## 8. Video plan (suggestion)

**Hook question.** "Your notebook trained five models last night. Which settings produced the best one, and could you re-run it on a GPU you don't own, from your terminal, in one command?"

**Target length:** about 32 minutes (the chapters below sum to 32; ≈ 4,950 spoken words at 155 wpm). The viewer should have the clone open and a terminal in `model-training/`.

| # | Chapter | The one idea | Visual (what is drawn / what moves) | On screen |
|---|---|---|---|---|
| 1 | Five models, one question (3 min) | Without records, you can't pick or reproduce a winner | Five training curves scribbled on a whiteboard fade. Then notebook A's results table assembles row by row | Notebook A cells 31, 37, 54; `experiment_<ts>/` file list |
| 2 | Experiment tracking, by hand and by W&B (4 min) | A run = config + metrics + artifacts + environment | The home-made JSON files morph into a W&B runs table. One row expands into charts. A "callback" pipe connects `model.fit` to the chart: when the pipe is removed, the chart stays empty | Notebook B cells 34, 38 (Excerpt 12), the W&B UI |
| 3 | Notebook → package (4 min) | Code must be shippable with flags and a dependency list | Cells slide into `task.py`; numbers peel into `--flags`; `trainer/` + `setup.py` shrink-wrap into `trainer.tar.gz` | `model-training/package/trainer/task.py:26-54`, `model-training/package/setup.py:5-13`, `model-training/package-trainer.sh:1-4` |
| 4 | The cockpit container (3 min) | Your container submits; it never trains | The laptop box with two bind-mount pipes (`/app`, `/secrets`) and env-var tags; the venv at `/.venv` stays visible when `/app` is overlaid | `model-training/docker-shell.sh:14-24`, `model-training/Dockerfile:52-62`, run `sh docker-shell.sh` |
| 5 | Ship it: package and submit (5 min) | A custom job = worker pool + image + package + args | The request arrow flies to Vertex. A VM materialises, image layers stack, the tarball unpacks, and the args unroll as `sys.argv` | `sh package-trainer.sh`, `model-training/cli.sh:5-19`, `model-training/cli.sh:30-37`, `sh cli.sh`, console Custom jobs page, `stream-logs` |
| 6 | Reading the logs and W&B (4 min) | Know what "success" looks like, and what is missing | The log stream scrolls; checkpoint lines light up (`Number of replicas`, `train_x count`, `View run at`). The W&B page shows config and system metrics, and a ghost outline where the loss chart should be | `model-training/package/trainer/task.py:312-338`; README claim `README.md:163` |
| 7 | GPUs: type, image, quota, region (3 min) | Three switches must agree | Three toggles (accelerator / tf-gpu image / regional quota). Only when all are green does a T4 chip light up inside the VM | `model-training/cli.sh:9-14`, `model-training/cli.sh:22-27`, quota screenshots |
| 8 | Two GPUs, one model (4 min) | MirroredStrategy = split the batch, all-reduce the gradients | 64 images split 32/32 onto twin networks. Gradient arrows meet, average and return. Both networks update in sync | `model-training/package/trainer/task_multi_gpu.py:287-321`, `model-training/cli-multi-gpu.sh:4-16` |
| 9 | What's still missing (2 min) | Metrics without artifacts is half a story | The VM dissolves and the trained weights evaporate with it. An arrow points to L15, where `tf.saved_model.save` writes to `gs://…/model` | `ml-workflow/src/model-training/package/trainer/task.py:376-383` (preview), cleanup commands |

**Pause-and-ponder questions** (place them where the viewer can work the answer out before it is revealed):
1. *(End of chapter 2, after the split output)* "The code sets `validation_percent = 0.2`, yet you see `validate_x count: 104` out of 1,156 images. What did the code actually do?" Answer: both splits use `test_percent`, so validation is 10 % of the remaining 1,040.
2. *(Chapter 6, when the epoch line shows a `loss` of roughly 100 next to rising accuracy)* "Accuracy goes up but loss is above 100. What term in the model could produce a loss that large?" Answer: the L1 penalty; estimate it from 163,840 weights × mean |w| ≈ 0.033 × 0.02.
3. *(Chapter 8, before showing the W&B config)* "With 2 GPUs, `--batch_size=32` and 936 training images, how many steps per epoch, and how many images does each GPU process per step?" Answer: global batch 64 → 15 steps (the last one partial); 32 images per GPU per step.

**Recap questions** (end card):
1. Name the four things a good experiment record contains.
2. Which file must you regenerate and upload after editing `task.py`, and why don't you need to rebuild the Docker image?
3. What three settings must agree for a Vertex job to really use a GPU?
4. Which identity submits the job, and which identity runs it?
5. Why must the model be built inside `strategy.scope()`?
6. After a successful job, where is the trained model? (Trick question: nowhere.)

---

## 9. Exercises

**Exercise 1 (hands-on): get loss and accuracy curves into W&B.**

*Task.* Add per-epoch logging to `model-training/package/trainer/task.py` without depending on the old `WandbCallback`. Predict what new charts appear. Then re-package, submit, and verify.

*Worked answer.* Insert a `LambdaCallback`, which works with both Keras 2 and 3, and pass it to `fit`:
```python
log_cb = keras.callbacks.LambdaCallback(
    on_epoch_end=lambda epoch, logs: wandb.log({**logs, "epoch": epoch})
)
training_results = model.fit(
    train_data,
    validation_data=validation_data,
    epochs=epochs,
    callbacks=[log_cb],
    verbose=1,
)
```
- Prediction: four new metric charts, `loss`, `accuracy`, `val_loss` and `val_accuracy`, each with one point per epoch (2 points for `--epochs=2`), plus an `epoch` chart because `epoch` is logged as a value too.
- Re-run `sh package-trainer.sh` and then `sh cli.sh`. If you forget the first, the job runs the old code (section 6, item 10).
- `WandbMetricsLogger` (already imported at `model-training/package/trainer/task.py:22`) is the official option. Its 0.15.11 code subclasses `tensorflow.keras.callbacks.Callback`, which is Keras 3 in TF 2.17. I could not verify that combination, so if you use it, bump the `wandb` pin in `setup.py`.

**Exercise 2 (debugging): a job fails with `api_key not configured (no-tty)`.**

*Task.* Your Vertex job runs for about 3 minutes and fails with `wandb.errors.UsageError: api_key not configured (no-tty). call wandb.login(key=[your_api_key])`. You never touched `task.py`. Why?

*Worked answer.*
- `--wandb_key=` was empty. You opened a new host terminal and ran `sh docker-shell.sh` without `export WANDB_KEY=...`. `-e WANDB_KEY=$WANDB_KEY` (`model-training/docker-shell.sh:23`) then forwarded an empty string, and `cli.sh` embedded it (`model-training/cli.sh:19`).
- `wandb.login(key="")` treats the key as missing and tries to prompt, which raises on a VM without a terminal.
- The "3 minutes" was provisioning plus the dataset download, because login happens at `model-training/package/trainer/task.py:153`, after the data steps.
- Fix: exit, export the key, restart the container, and resubmit.
- Hardening: at the top of `cli.sh`, add `[ -z "$WANDB_KEY" ] && echo "WANDB_KEY not set" && exit 1`.

**Exercise 3 (hands-on): fix the split and predict the counts.**

*Task.* Change the second `train_test_split` to use `validation_percent`. Before running, predict the three counts and the steps per epoch at `--batch_size=32`.

*Worked answer.*
- Change `test_size=test_percent` to `test_size=validation_percent` at `model-training/package/trainer/task.py:145`.
- scikit-learn rounds the test share up: test = ceil(0.10 × 1156) = **116**; validation = ceil(0.20 × 1040) = **208**; train = 1040 − 208 = **832**.
- Steps per epoch = ceil(832/32) = **26** (was 30).
- Also add `random_state=42` (and `stratify=`) so that runs are comparable.

**Exercise 4 (hands-on): don't lose the model.**

*Task.* Make the trainer save the trained model and the label map to your bucket. Use the existing but unused `--model-dir` flag.

*Worked answer.*

In `task.py`, after training and before `wandb.run.finish()` (line 338):
```python
import json
model.save("model.keras")
with open("label2index.json", "w") as f:
    json.dump(label2index, f)
for fname in ["model.keras", "label2index.json"]:
    tf.io.gfile.copy(fname, f"{args.model_dir}/{fname}", overwrite=True)
```

In `cli.sh`, append to `CMDARGS`: `,--model-dir=$GCS_BUCKET_URI/models/$DISPLAY_NAME`.

- `tf.io.gfile` understands `gs://` paths in TF's prebuilt images. L15's trainer writes to `gs://…/model` the same way (`ml-workflow/src/model-training/package/trainer/task.py:376-383`).
- The job runs as your project's Vertex AI service agent, which normally has access to buckets in the same project. If the copy fails with a 403, grant that agent write access to the bucket, or run the job under your own service account (`--service-account` on `gcloud ai custom-jobs create`).
- Also make the labels deterministic with `sorted(os.listdir(base_path))` (section 6, item 16).
- Optional: `wandb.log_artifact("model.keras", name=f"model-{model.name}", type="model")` gives you a W&B model artifact named like the one L15's commented-out code expects (`model-mobilenetv2_train_base_True`, `model-deployment/cli.py:70-77`).

**Exercise 5 (debugging): GPU job accepted but slow, logs show `GPU Available:  []`.**

*Task.* You edited `cli.sh` to add `accelerator-type=$ACCELERATOR_TYPE,accelerator-count=$ACCELERATOR_COUNT` to the CPU block at `model-training/cli.sh:36`. The job runs, but the logs show no GPU. Why?

*Worked answer.* Line 31 overrides `EXECUTOR_IMAGE_URI` to `tf-cpu.2-17.py310`, a TensorFlow build with no CUDA. The VM has a T4 attached that TF can't use, so you pay for the T4 anyway. Use the GPU block (`model-training/cli.sh:22-27`), which keeps the `tf-gpu` image from line 9.

**Exercise 6 (conceptual): multi-GPU math and scope.**

*Task.* (a) In `task_multi_gpu.py`, what would go wrong if `build_mobilenet_model` and `compile` were moved *outside* `with strategy.scope():`? (b) The single-GPU run used batch 32 and lr 0.001. With 2 GPUs the global batch is 64. Should you change the learning rate? (c) Will the 2-GPU job finish in half the wall-clock time?

*Worked answer.*
- **(a)** The variables would be created as ordinary, single-device variables, not `MirroredVariable`s. Depending on the TF/Keras version you either get an error when `fit` runs under the strategy, or the model trains without true replication. Either way you lose the point of the strategy.
- **(b)** The usual heuristic is the linear scaling rule: lr ∝ global batch, so 0.002. Halving the number of steps per epoch with the same lr means fewer updates per epoch. The code does not scale it: `learning_rate = 0.001` is hard-coded (`model-training/package/trainer/task_multi_gpu.py:275`).
- **(c)** No.
  - Provisioning, image pull, `pip install` and the 305 MB download are fixed costs that don't shrink.
  - On 936 images the per-epoch work is small, so all-reduce and input-pipeline overheads matter.
  - The machine also differs (`n1-standard-32`).
  - Measure it: compare `execution_time` in the two W&B projects.

**Exercise 7 (conceptual/debugging): "the code I edited isn't what ran".**

*Task.* You edit `task.py`, run `sh cli.sh` immediately, and the logs show the old prints. Then you rebuild the Docker image and try again, and it still shows the old prints. Explain both observations.

*Worked answer.* The Vertex VM installs `gs://…/cheese-app-trainer.tar.gz` (`model-training/cli.sh:10`). Only `sh package-trainer.sh` refreshes that object (`model-training/package-trainer.sh:4`). Rebuilding the console image is irrelevant: that image never runs on Vertex, and `/app` is bind-mounted anyway, so it already sees your edit.

---

## 10. Errata and open questions

**Errata (evidence-based)**

- **E1. README promises training metrics in W&B; the code logs none.**
  - `README.md:160-163`: "You will view the training metrics tracked and automatically updated".
  - `model.fit` has no callbacks (`model-training/package/trainer/task.py:326-331`, `model-training/package/trainer/task_multi_gpu.py:338-343`); commit `88f3374` removed `WandbCallback`.
  - W&B gets only config, `execution_time`, system metrics and console logs.
  - `WandbCallback, WandbMetricsLogger` are still imported but unused (`model-training/package/trainer/task.py:22`).
- **E2. README says GPU, the code defaults to CPU.**
  - "Create Jobs in Vertex AI" (`README.md:132-150`) describes GPU parameters.
  - "OPTIONAL: … using CPU" (`README.md:152-154`) tells you to remove the accelerator, but `cli.sh` already runs the CPU block, and the GPU block is commented out (`model-training/cli.sh:21-37`; commit `3efb2d5`).
- **E3. The README's docker-shell listing doesn't match `docker-shell.sh`.**
  - Platform handling differs: `README.md:99-101` vs `model-training/docker-shell.sh:13-14`.
  - The listing embeds non-shell annotations (`README.md:93-94`, `README.md:110`) and an HTML comment `<!-- mlproject01-207413 -->` that renders inside the code block (`README.md:96`).
- **E4. Validation split bug.**
  - `validation_percent = 0.2` is unused; both splits use `test_percent` (`model-training/package/trainer/task.py:135-146`).
  - The same code is in both notebooks (notebook A cell 26, notebook B cell 27). Their outputs confirm 936/104/116.
- **E5. Dead flags.**
  - `--lr` (`model-training/package/trainer/task.py:30`) is ignored; `learning_rate = 0.001` is hard-coded (`model-training/package/trainer/task.py:274`).
  - `--model-dir` (`model-training/package/trainer/task.py:27-29`) is ignored.
- **E6. The trained model is discarded.**
  - Neither trainer calls `model.save`, writes to GCS, or logs a W&B artifact, so every Vertex run's weights vanish with the VM.
  - `model-deployment/README.md:54` ("Our model weights are stored in WandB following the serverless training we did in the previous tutorials") does not hold for the current L13 code.
- **E7. A placeholder default makes `cli.py` (and any run without `--wandb_key`) crash.** The default is `"16"` (`model-training/package/trainer/task.py:52`). `cli.py` passes no key (`model-training/cli.py:31`) and needs an unset `GCP_REGION` (`model-training/cli.py:7`). It is also not mentioned anywhere in the README.
- **E8. Inconsistent TF images.**
  - `cli.sh` uses 2.17 (Keras 3) at `model-training/cli.sh:9` and `model-training/cli.sh:31`.
  - `model-training/cli-multi-gpu.sh:8` and `model-training/cli.py:21` still use `tf-gpu.2-14.py310` (Keras 2).
  - The single-GPU and multi-GPU runs therefore differ in framework version as well as in hardware.
- **E9. Outdated accelerator list.**
  - `README.md:136-142` lists `NVIDIA_TESLA_K80`. As far as I know, K80s were retired from Google Cloud in 2024. Treat this as an unverified claim and check the current Vertex AI GPU list.
  - Newer types such as L4 aren't mentioned.
- **E10. Misleading legacy imports.**
  - `from tensorflow.python.keras import backend as K` and `count_params` (`model-training/package/trainer/task.py:13-14`) come from TF's legacy internal Keras.
  - Under TF 2.17, `K.clear_session()` (`model-training/package/trainer/task.py:283`) clears that legacy session, not Keras 3's.
  - `count_params` is unused.
- **E11. A misleading strategy in the single-GPU trainer.** `model-training/package/trainer/task.py:60` creates a `MirroredStrategy` only to print the replica count. The model is built outside any scope. It is harmless, but it suggests distribution that isn't happening.
- **E12. Undeclared dependencies.** `sklearn` and `requests` are imported (`model-training/package/trainer/task.py:3`, `model-training/package/trainer/task.py:17`), but only `wandb` is declared (`model-training/package/setup.py:5`). The trainer works only because the prebuilt image ships them.
- **E13. Preprocessing mismatch in the notebooks.** Training normalises with `image/255` (notebook A cell 28; notebook B cell 29, where `preprocess_input` is commented out). The prediction cells use `keras.applications.mobilenet.preprocess_input` (notebook A cell 59, notebook B cell 60), so the displayed test predictions run on differently scaled inputs.
- **E14. Notebook B's W&B config never reaches W&B.**
  - Cells 38/42/46/50/52 assign `wandb.config = {...}` after `wandb.init` (see Excerpt 12). The assignment rebinds the module attribute, so the config is dropped.
  - The same cells end with `wandb.config.update({"execution_time": execution_time})`. By then `wandb.config` is the plain dict, so this is `dict.update` and `execution_time` is dropped too. The next cell's `wandb.init` points `wandb.config` back at a fresh run's Config, and the cycle repeats.
  - `wandb.run.save("test")` is a file-upload call, not a save of the run.
- **E15. Notebook B logs curves for only one of five models.** Only cell 38 passes `WandbCallback`; cells 42, 46, 50 and 52 call `fit` without callbacks.
- **E16. Notebook B's legacy path loads the wrong models.**
  - Cell 16 downloads `dlops-io/models` release v1.0 `experiments.zip` (≈510 MB).
  - Its `experiment_1632250736/data_details.json` has `"num_classes": 3` and labels `crimini`, `oyster`, `amanita`. These are mushroom models.
  - So `LOAD_PREV_TRAINED = True` (cell 32) would load 3-class mushroom `.hdf5` models into a 4-class cheese run. The download is also wasted when the flag is False.
- **E17. Hard-coded course resources.** Notebook B's `upload_experiment` hard-codes bucket `cheese-app-models` and project `ac215-project` (cell 13). Notebook A also defaults to them (cell 63). The repo defaults to `gs://cheese-app-trainer` and `ac215-project` (`model-training/docker-shell.sh:8-9`).
- **E18. Secret passed on the command line.** The W&B key goes in `--args` (`model-training/cli.sh:19`, `model-training/cli-multi-gpu.sh:16`) and is stored in the job spec.
- **E19. Non-deterministic label order.**
  - `os.listdir` (`model-training/package/trainer/task.py:106`) gives a different order from run to run; the two notebook outputs prove it.
  - The trainer does not persist `label2index`. (The notebooks do, via `data_details.json`.)
- **E20. Leftovers in the console image.**
  - The Dockerfile installs `docker-ce` and `google-cloud-sdk-gke-gcloud-auth-plugin`, which are not needed (`model-training/Dockerfile:28-37`).
  - It creates user `app` but never switches to it (`model-training/Dockerfile:44-47`).
  - `pyproject.toml` is the `uv init` template (`name = "app"`, "Add your description here"; `model-training/pyproject.toml:2-4`).
- **E21. Course-site inconsistencies.**
  - The Colab links on the course site (`tutorials_demo.md:172-173`) differ from the "Open in Colab" badges saved inside the notebooks (`1GIslUzm…`, `1VrNXEm…`).
  - `_modules/week-08.md:5-13` labels the Oct 20 session (this lecture's title) "Lecture 12", and the Oct 22 session (Serverless Deployment, i.e. L14's topic) "Lecture 13".
- **E22. The notebooks' "sorted by accuracy" table sorts strings.** The compare cells (notebook A cell 54, notebook B cell 55) first format `accuracy` as text (`'{:,.2f}%'.format`) and then call `sort_values(by=['accuracy'], ascending=False)`, so the sort is lexicographic. It happens to be right in the saved runs because every value has two digits before the point; a model at `9.50%` would sort above `68.97%`, and `100.00%` below it, and `best_model` (`view_metrics.iloc[0]`, notebook A cell 56, notebook B cell 57) would then pick the wrong file. Sort on the numeric column before formatting.

**Open questions (could not determine from the sources)**
- **Ed lesson:** I could not see what it adds (slides, a video, which multi-GPU strategies the lecture covers beyond `MirroredStrategy`).
- **Prebuilt images in 2026:**
  - Are `us-docker.pkg.dev/vertex-ai/training/tf-cpu.2-17.py310:latest` and `tf-gpu.2-17.py310:latest` still offered?
  - Do they still include scikit-learn and requests?
  - Does `wandb==0.15.11` import cleanly in them? Its Keras integration calls `patch_tf_keras()` at import (`wandb/integration/keras/keras.py:231`) and, for TF ≥ 2.13, imports `tensorflow.python.keras.engine`. TF 2.19 in Colab still had `tensorflow.python.keras`, since notebook B's imports ran.
  - The last commits suggest the instructors ran the job successfully in October 2025, but no job log is in the repo.
- **`python:3.13-slim-bullseye`** (`model-training/Dockerfile:2`): checked on 2026-10-13. Docker Hub still lists the tag as active, but its last push was 2025-08-07, so it is frozen (no security updates); `python:3.13-slim-bookworm` was pushed 2026-10-06. Debian's `bullseye` and `bullseye-security` apt suites and Docker's `bullseye` repo still answered on the same day, so the `apt-get update` lines (`model-training/Dockerfile:18`, `model-training/Dockerfile:36`) should still work. Whether they keep working once bullseye moves to archive.debian.org is open.
- **`tf-gpu.2-14.py310`** (`model-training/cli-multi-gpu.sh:8`, `model-training/cli.py:21`): I could not check whether Vertex still serves this older prebuilt image.
- **W&B API key format:** if keys issued to new accounts are not 40 characters, `wandb==0.15.11` would reject them (`wandb/sdk/lib/apikey.py:238-239`). Check `echo ${#WANDB_KEY}`.
- **Prices:** the dollar figures in section 2 are approximate list prices from memory. Check https://cloud.google.com/vertex-ai/pricing.
- **Console naming:** another digest in this series (L10) observed newer console wording for Vertex AI. If the console search doesn't find "Vertex AI", look for "custom jobs" or "Training".
- **`wandb.config = {...}`:** I verified this in 0.15.11's source, while the notebook installs the newest wandb. I assume the module-attribute design is unchanged but did not verify it in the latest release.
- **Run length:** expected run times on Vertex (CPU `--train_base`, 2 epochs; provisioning delay) are my estimates. No job logs are included in the repo.

_Verified against the repos on 2026-10-13 (adversarial check)._
