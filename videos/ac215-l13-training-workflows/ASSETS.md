# Assets and where they come from

Everything a scene shows as "real" (a terminal output, a source line, a file listing) is read from
a file in `assets/`, never typed by hand into a scene. This file says where each one came from.

**The one thing to know about this lecture's captures:** the recording sandbox has **no GCP
credentials, no W&B account, no GPU and no browser** (see the skill's environment rules). Everything
local is captured live: the clone, the secrets folder, the console image build (`sh docker-shell.sh`),
its entrypoint, `sh package-trainer.sh`'s tarball, the in-container checks, `python cli.py`'s first
error, and two labelled **local stand-ins** (the first thing a Vertex job does, `pip install` of the
tarball in a Python 3.10 container, plus the trainer's W&B login line offline; and notebook B's
`pip install wandb` plus an offline check of its `wandb.config = {...}` pattern). Every step that
needs Google, Vertex AI or W&B (`gsutil cp`, `gcloud ai custom-jobs create` in `sh cli.sh` and
`sh cli-multi-gpu.sh`, the job itself, the W&B dashboard) is captured up to its **honest, documented
failure**, and what a student would see on success is listed under "What cannot run here" with its
source. No output was invented.

**Read this before the brief: the README's `sh docker-shell.sh` fails today, earlier than the digest
says.** The digest (2026-10-13) expected the build to stop at `Dockerfile:37` (`google-cloud-sdk` has
no installation candidate) and noted that bullseye's apt suites "still answered". On 2026-10-23 the
**bullseye-security pool no longer has the files its index lists**. The index on `deb.debian.org`
and `security.debian.org` is still served (dated 2026-09-12), but its `…deb11u…` packages return
404; only `archive.debian.org` has them. The first `apt-get install` (`Dockerfile:18-19`, build step
2/14) fails with `404 Not Found` for 22 packages (`21`), long before line 37. Two one-line fixes get the build
through: `Dockerfile:2` → `python:3.13-slim-bookworm` (`22`), which brings back the digest's
line-37 failure word for word (`23`), then `Dockerfile:37` → `google-cloud-cli` (`24`, the digest's
fix). The diff is in `25`, the successful start in `26`. The brief must decide how to present the two
fixes (see the report's BRIEF questions).

## `source/` — the tutorial's own files

Copied unchanged with `git show <commit>:<path>`, relative paths preserved, except the two Colab
extracts (see below). Course material by the AC215 teaching staff (Harvard IACS), used for study
with the instructor's permission.

**Personal data in the snapshots (scenes must mask it):** none in `source/model-training/` (checked
for names and e-mail addresses). The notebooks name the instructor and the notebook author in cell
0 and the W&B user who ran notebook B in cell 34's stored output. Those three strings are replaced
in the extracts (below), so the extracts can be quoted as they are.

### `source/model-training/`

[dlops-io/model-training](https://github.com/dlops-io/model-training) `main` at
`b9aee1cc1923dd1f673093ad3ff5bb023049b4ff` (2025-10-16 07:31:56 -0400, "remove pipfiles and do minor
edits"). This is the course map's pin (`b9aee1c`) and the digest's commit, and still the head of `main` on
2026-10-23 (`terminal/laptop/02-git-log.txt`), so the README has not moved. The README's six PNGs
(quota pages, W&B key page, architecture) are console/product screenshots. They are **not**
snapshotted: the series never shows them, and scenes redraw them as `illustration`.

| file | what a panel quotes from it |
| --- | --- |
| `README.md` | the whole tutorial (170 lines): prerequisites (6-8), clone (16-17), Vertex AI API (19-21), GPU quotas (23-44), secrets folder (50-58), SA + roles + key (60-64), bucket (66-71), W&B key + `export WANDB_KEY=...` (73-81), the README's *copy* of docker-shell (89-112, with `[REPLACE …]` notes at 93-94, the HTML comment at 96, the arm64 line at 100-101, the broken continuation at 110), `sh docker-shell.sh` (114-116), review trainer (121-125), `sh package-trainer.sh` (127-129), jobs + accelerator/region lists (132-150), optional CPU (152-154), view jobs (156-158), W&B metrics claim (160-163), multi-GPU (165-170) |
| `Dockerfile` | `python:3.13-slim-bullseye` (2), `UV_PROJECT_ENVIRONMENT=/.venv` (15), apt step (18-19) **= today's first failure**, cloud-sdk repo (22-25), docker repo (28-33), **`google-cloud-sdk google-cloud-sdk-gke-gcloud-auth-plugin`** (37), `pip install uv` (40), user `app` never used (44-47), `uv sync --frozen` (56), entrypoint (62) |
| `docker-shell.sh` | `set -e` (3), `SECRETS_DIR=$(pwd)/../secrets/` (7), bucket/project to edit (8-9), `--platform=linux/amd64` build (14), `docker run --rm --name … -ti` with both mounts and four `-e` (17-24) |
| `docker-entrypoint.sh` | the banner, `gcloud auth activate-service-account` (6), `gcloud config set project` (8), the "venv activated" line printed *before* activation (13 vs 19), `exec /bin/bash` (22) |
| `package-trainer.sh` | the four lines: `rm -f`, `tar cvf`, `gzip`, `gsutil cp … cheese-app-trainer.tar.gz` |
| `cli.sh` | `UUID`/`DISPLAY_NAME` (5-6), machine/replicas (7-8), the GPU image (9), package/module (10-11), accelerator (12-13), region (14), `CMDARGS` with `--wandb_key=$WANDB_KEY` (19), the commented GPU block (22-27), the CPU image override (31) and the job command (32-37) |
| `cli-multi-gpu.sh` | `n1-standard-32`, `tf-gpu.2-14.py310`, `trainer.task_multi_gpu`, `NVIDIA_TESLA_T4` × 2, 5 epochs (4-16), the job command (19-24) |
| `cli.py` | `os.environ["GCP_REGION"]` (7), `aip.init` (16), `CustomPythonPackageTrainingJob` (23-29), `CMDARGS` without a key (31), `job.run(… sync=False)` (42-51) |
| `package/setup.py`, `setup.cfg`, `PKG-INFO`, `trainer/__init__.py` | `REQUIRED_PACKAGES = ["wandb==0.15.11"]` (setup.py:5), `find_packages()` (11); the leftover metadata ("Cheese App Trainer") |
| `package/trainer/task.py` | imports incl. legacy Keras (1-22), argparse flags and the `"16"` default (26-54), the startup prints (56-68), the 305 MB download (93-102), `os.listdir` labels (105-107), the split bug (134-150), `wandb.login` (153), `get_dataset` (157-225), MobileNetV2 + L1 head (228-266), training params (269-283), `print(model.summary())` (308), `wandb.init` (312-322), `model.fit` without callbacks (324-333), `wandb.config.update` / `wandb.run.finish()` (335-338), "Training Job Complete" (341) |
| `package/trainer/task_multi_gpu.py` | `MirroredStrategy`, `num_replicas_in_sync`, `global_batch_size` (287-301), `strategy.scope()` (304-321), the second W&B project |
| `pyproject.toml`, `uv.lock`, `.gitignore` | the `uv init` template (`name = "app"`), `google-cloud-aiplatform>=1.120.0` → locked 1.120.0; `trainer.tar.gz` ignored (`.gitignore:4`) |

### `source/model-training-history/`

Three commits of the same repo, from `git show --format='commit %H%nDate: %ci%n%n    %s%n' <commit>`.
That format leaves out the author line, so no names or e-mails appear. The diffs are unchanged.

| file | what it shows |
| --- | --- |
| `88f3374.diff` | 2025-10-15 "removed ca;llback": `callbacks=[WandbCallback()],` deleted from both trainers, and `dtype="float32"` dropped from `to_categorical` (the digest's E1/Excerpt 10 evidence) |
| `1c03dd5.diff` | 2025-10-15 "Updated TF image": ubuntu+pipenv → python:3.13-slim-bullseye + uv, `--platform` arm64 → amd64, `cli.sh` 2.14 → 2.17 (922 lines, incl. the deleted Pipfile.lock and LICENSE, "Copyright (c) 2023 DLOps") |
| `3efb2d5.diff` | 2024-10-15 "Updated cli to default to CPU": the commit behind the README-vs-code mismatch (digest E2) |

### `source/colab/` — extracts of the two notebooks (edited, see notes)

Downloaded 2026-10-23 from Google Drive with the course map's ids. The md5 of both `.ipynb` files
**equals the digest's**, so the notebooks have not changed. The `.ipynb` files are **not** in the repo
(their metadata and cells can name people). Each extract holds the cell sources and the stored
outputs only. Cell numbers are the 0-based indices the digest uses; ANSI colours are dropped; progress
lines are collapsed to their final state; images read `[image output omitted]`. W&B's HTML banners
(stored as text/html, with text/plain `<IPython.core.display.HTML object>`) are rendered to text and
marked `[HTML output, rendered as text]`. The extractor is not part of the repo; it is described
here so the conversion can be repeated.

| file | notebook | notes |
| --- | --- | --- |
| `notebook-A-1h6xRhjI.cells.txt` | A, `1h6xRhjILxaUosXlZ5ZC1NZbP0AOHALTl` ("Cheese Classification Models"; md5 `0f4a5c78…`) | **`recorded`** source for the home-made tracker: TF 2.19.0, `Number of replicas: 1`, the Tesla T4 `nvidia-smi` box (lines 115-140), `Full size of the dataset: 1156` (353), `train_x count: 936` … (445-447), per-model `Training execution time (mins)` (643, 850, 1037, 1154, 1245), the cell-54 comparison table (1284-1288: 68.97 % / 67.24 % / 34.48 % / 31.03 % / 25.86 %), the cell-66 upload lines `uploading file experiment_1760994796/…` (from 1437). Edited: cell 0's instructor/author lines read `<course instructor>` / `<notebook author>`. |
| `notebook-B-1aAE5vR9.cells.txt` | B, `1aAE5vR9r6Syh4heZboDbQNZS048VToxS` ("Experiment Tracking with W&B"; md5 `ac692e0a…`) | **`recorded`** source for W&B in a notebook: TF 2.19.0 / Keras 3.10.0 (127-130); the cell-34 login, `wandb: Appending key for api.wandb.ai to your netrc file: /root/.netrc` then `Currently logged in as: <W&B user> (ac215-harvard)` (612-615); per training cell the banners **`Tracking run with wandb version 0.22.2`**, `Run data is saved locally in /content/wandb/run-…`, `Syncing run clear-tree-13 …` (an auto-name, renamed later), `View run at https://wandb.ai/ac215-harvard/cheese-app-demo/runs/…` (773-781, 1031-1039 …); the `WandbCallback is deprecated` warning (782); **only the 2_block run** has a W&B "Run history" sparkline block and "Run summary" (`accuracy 0.72436`, `val_accuracy 0.45192`, `best_epoch 15`, 1005-1022), which is digest E15, visible; at each next `wandb.init` the finishing banner says `View run 2_block at: …` (1024) and `View run mobilenetv2_train_base at: …` (1629), which is digest A8's shared display name; cell 55 table; cells 64/66 have no stored output. Edited: cell 0 as above, and cell 34's W&B user name reads `<W&B user>` (the team name `ac215-harvard` is kept: it is the course's W&B team, not a person). |

## `terminal/` — real terminal sessions

Captured **2026-10-23 12:19–12:34 UTC** by `terminal/capture.sh`, which runs `terminal/run_steps.sh`
inside fresh disposable containers. Segments: `setup`, `pre`, `cloud`, `wandb`, then `bases` + `shell`
(a first `shell` attempt was redone after the build failed at step 2; see "Capture-only deviations"),
then `pkg`, `job`, `mgpu`, `clipy`, `nokey`, `vtx`, `clean`, `colab`. Each README command runs exactly
as written, in README order, and its output goes to its own file. The file starts with the command
(`$ ...`), then the output, then its exit status (`[exit N]`). Steps that are not in the README are
marked *extra* below and in `run_steps.sh`.

Two kinds of file, as in L10/L11: **`step` files** (no terminal, plain output; colours dropped) and
**`istep` files** (a real pseudo-terminal via `ptyrun.py`, 110×50; the lines a person would type at
the container prompt are typed when the `…:/app#` prompt appears; BuildKit's progress is redrawn as
a terminal shows it; colours are dropped). An `istep` file's `[exit N]` is the status of the shell's
last command before `exit`. Each NN prefix maps to exactly one file.

| folder | environment | source it follows |
| --- | --- | --- |
| `laptop/` | a fresh, empty Docker engine standing in for the student's machine with Docker Desktop: `docker:29.8.2-dind` (client + engine 29.8.2, linux/amd64), user `student` in the `docker` group with sudo, git 2.54.0, curl, tree, python3 | `model-training/README.md` top to bottom, then extras and the Vertex stand-in |
| `colab/` | a `python:3.12-slim-bookworm` container, root in `/content` like a Colab runtime, **no Google sign-in, no GPU, no W&B account** (`capture-only/colab-standin.Dockerfile`) | notebook B cell 5, plus an offline check of its cell-38 pattern |

### `laptop/` — README top to bottom

| file | README step | what it shows |
| --- | --- | --- |
| `00-env.txt` | extra | date, `Linux x86_64`, Docker 29.8.2, git 2.54.0 |
| `01-clone.txt` | "Clone the github repository", README:17 | `git clone https://github.com/dlops-io/model-training` |
| `02-git-log.txt` | extra | HEAD = `b9aee1cc…` 2025-10-16 = the pin |
| `03-ls.txt` | extra | the repo's top level (six PNGs, three shell scripts, `cli.py`, `package/`, `uv.lock` …) |
| `04-mkdir-secrets.txt` | "Create a local secrets folder", README:52 (the README shows the tree, not a command) | `mkdir secrets` next to the repo |
| `05-tree.txt`, `06-ls-secrets.txt` | README:54-58 tree (extra) / the key's name | `model-training` beside `secrets`; `secrets/model-trainer.json`, which is the **placeholder** key (below) |
| `07-bucket-placeholder.txt` | extra (for README:66-71, a console step) | `your-bucket-placeholder` → `404 The specified bucket does not exist.`: the placeholder used everywhere below is nobody's bucket |
| `08-bucket-readme.txt` | extra (digest gotcha #18) | the README's `cheese-app-trainer` → `401 Anonymous caller does not have storage.buckets.get access…`. **It exists and belongs to someone else**, so a student must pick another name |
| `09-prebuilt-images.txt` | extra (digest §10 open question) | `docker manifest inspect` (no pull): `tf-cpu.2-17.py310:latest` **29 layers, 4.31 GB compressed**; `tf-gpu.2-17.py310:latest` 40 layers, 8.93 GB; `tf-gpu.2-14.py310:latest` 38 layers, 7.61 GB. All three are still served |
| `10-export-wandb-key.txt` | "Get WandB Account API Key", README:80 `export WANDB_KEY=...` (+ extra `echo ${#WANDB_KEY}`) | `40`, from the obviously fake placeholder (below) |
| `11-wandb-key-new-terminal.txt` | extra (digest gotcha #1) | a new terminal: `0`, so the variable is gone |
| `20-edit-docker-shell.txt` | README:93-94 "[REPLACE WITH YOUR BUCKET NAME]" / "[REPLACE WITH YOUR PROJECT]" (sed is the editor) | lines 8-9 now `gs://your-bucket-placeholder`, `your-gcp-project` |
| `21-docker-shell-fails.txt` | README:115 `sh docker-shell.sh`, unmodified repo | **new failure, live:** step `[ 2/14] RUN apt-get update && apt-get install -y curl …` fetches the bullseye indexes, then `Err:… https://deb.debian.org/debian-security bullseye-security/main amd64 … 404  Not Found` for 22 packages, `E: Unable to fetch some archives, maybe run apt-get update or try with --fix-missing?` (line 166), `ERROR: failed to build: failed to solve: … exit code: 100` (188); exit 1 (`set -e` stops before `docker run`). Crop or blur the `[IP: 172.17.0.1 38713]` tail on each `Err`/`E:` line: it is the sandbox's proxy relay, and a student sees a Debian mirror address there |
| `22-fix-base-image.txt` | extra (fix 1) | `Dockerfile:2` → `FROM python:3.13-slim-bookworm` |
| `23-docker-shell-fails-again.txt` | README:115 again | the build now passes steps 2-7 (bookworm indexes, the cloud-sdk and Docker repos) and **digest gotcha #20, live, word for word** at `[ 8/14]`: `Package google-cloud-sdk is not available, but is referred to by another package. … However the following packages replace it: google-cloud-cli`, the same for `google-cloud-sdk-gke-gcloud-auth-plugin` → `google-cloud-cli-gke-gcloud-auth-plugin`, `E: Package 'google-cloud-sdk' has no installation candidate` (lines 344-358), `ERROR: failed to build` (379); exit 1 |
| `24-fix-dockerfile.txt` | extra (fix 2 = digest gotcha #20's fix) | `Dockerfile:37` → `apt-get install -y google-cloud-cli jq docker-ce` |
| `25-git-diff.txt` | extra | the two fixes plus the two lines in `docker-shell.sh`, and nothing else (`2 files changed, 4 insertions(+), 4 deletions(-)`) |
| `26-docker-shell.txt` | README:115 a third time; typed inside, extras: `ls -la /secrets`, `echo $GCP_PROJECT $GCS_BUCKET_URI ${#WANDB_KEY}`, `which python gcloud gsutil uv`, `gcloud --version`, the aiplatform version, `python -c "import tensorflow"`, `exit` | BuildKit summary (`[+] Building 314.2s (19/19) FINISHED`; step 8 139 s); the entrypoint banner: `Container is running!!!`, **`ERROR: (gcloud.auth.activate-service-account) Unable to read file [/secrets/model-trainer.json]: [Errno 2] No such file or directory: '/secrets/model-trainer.json'`** (the honest no-key state; digest B8 "If it fails"), `Updated property [core/project].`, `Architecture: x86_64`, `Environment ready! Virtual environment activated.`, `Python version: Python 3.13.17`, `UV version: uv 0.13.5`, `Activating virtual environment...`; the `root@<id>:/app#` prompt anyway (no `set -e`); `/secrets` empty; `your-gcp-project gs://your-bucket-placeholder 40`; `/.venv/bin/python`, `/usr/bin/gcloud`, `/usr/bin/gsutil`, `/usr/local/bin/uv`; Google Cloud SDK 590.0.0 (gsutil 5.37); aiplatform `1.120.0`; **`ModuleNotFoundError: No module named 'tensorflow'`**: the console never trains (digest §3.3); exit 1 = that last import |
| `27-docker-images.txt` | extra | `model-training-cli:latest` 2.59 GB on disk (539 MB content) |
| `30-package-trainer.txt` | "Run `sh package-trainer.sh`", README:127-129, typed inside; extras `ls -l trainer.tar.gz`, `tar tzvf trainer.tar.gz`, `gsutil ls $GCS_BUCKET_URI` | `tar cvf` lists the 8 entries (`package/`, `package/trainer/`, `task.py`, `__init__.py`, `task_multi_gpu.py`, `setup.py`, `setup.cfg`, `PKG-INFO`; directory order, not the digest's); gsutil's new notice **`Google recommends using Gcloud storage CLI (…) instead of gsutil. …`**, then the **honest failure** `BucketNotFoundException: 404 gs://your-bucket-placeholder bucket does not exist.` (with no credentials gsutil asks anonymously, and the placeholder bucket does not exist; it is the digest's B10 "If it fails" text); `trainer.tar.gz` **4016 bytes**; `tar tzvf` shows each file's size (task.py 10253, task_multi_gpu.py 10775 …) |
| `31-host-tarball.txt` | extra | on the host the tarball is owned by **root** (written by the container); `git status` shows only the two edited files; `.gitignore:4:trainer.tar.gz` ignores it |
| `40-cli-sh.txt` | "Create Jobs in Vertex AI", README:150 `sh cli.sh` typed inside; extras `gcloud auth list`, `sh -x cli.sh`, `gcloud ai custom-jobs list --region=us-central1` | `Using endpoint [https://us-central1-aiplatform.googleapis.com/]` (the digest's first checkpoint line, live), then the **honest failure** `ERROR: (gcloud.ai.custom-jobs.create) You do not currently have an active account selected.` + gcloud's own "Please run: $ gcloud auth login" advice; `No credentialed accounts.`; **`sh -x` shows the expanded job**: `DISPLAY_NAME=cheese_training_job_<12 hex>`, the GPU image set first and then overridden by `tf-cpu.2-17.py310`, and the full `gcloud ai custom-jobs create --region=us-central1 … --worker-pool-spec=machine-type=n1-standard-4,replica-count=1,executor-image-uri=…tf-cpu.2-17.py310:latest,python-module=trainer.task --args=--model_name=mobilenetv2,--train_base,--epochs=2,--batch_size=32,--wandb_key=PLACEHOLDER_…` (**the key sits in the job's arguments**, digest E18, live); `custom-jobs list` → the same auth error |
| `50-cli-multi-gpu.txt` | "OPTIONAL: Multi GPU Training", README:170 `sh cli-multi-gpu.sh` | `Using endpoint …`, the same honest auth failure |
| `60-cli-py.txt` | extra (digest B16; not in the README) | **digest gotcha #3, live:** `KeyError: 'GCP_REGION'` at `cli.py:7`; after `export GCP_REGION=us-central1` the SDK fails at **`cli.py:23`** (constructing `CustomPythonPackageTrainingJob`, before `job.run`) with `google.auth.exceptions.DefaultCredentialsError: File /secrets/model-trainer.json was not found.`; `which pip` → `/usr/local/bin/pip`; **digest gotcha #17, live (the digest had not tested it):** `pip install ./package` on the console's Python 3.13 → `pathtools-0.1.2.tar.gz` … `ModuleNotFoundError: No module named 'imp'` → `ERROR: Failed to build 'pathtools' …` |
| `70-docker-shell-no-wandb-key.txt` | extra (digest gotcha #1) | a terminal where `WANDB_KEY` was never exported: inside, `echo ${#WANDB_KEY}` → `0`; `sh -x cli.sh … | grep` → `--args=--model_name=mobilenetv2,--train_base,--epochs=2,--batch_size=32,--wandb_key=`, so the job would receive an empty key |
| `71-docker-shell-second.txt` | extra (digest gotcha #22) | a second `sh docker-shell.sh` while `70`'s container is open: `docker: Error response from daemon: Conflict. The container name "/model-training-cli" is already in use by container "…"`; exit 125 |
| `80-standin-pip-install.txt` | **capture-only stand-in** for "the job pip-installs your package" (digest B12) | in a plain `python:3.10-slim-bookworm` container (the images are "py310"): `Processing /tmp/trainer.tar.gz` … `Successfully built cheese-app-trainer pathtools` … `Successfully installed … cheese-app-trainer-0.0.1 … wandb-0.15.11` (pip 23.0.1). This is not Google's image and not its install command |
| `81-standin-commit.txt` | capture-only | keeps the installed container as an image for `82`-`87` |
| `82-standin-pip-list.txt` | stand-in, extra (digest E12) | what `install_requires` brings: wandb 0.15.11, protobuf 4.25.9, requests …. **No tensorflow and no scikit-learn**: the trainer relies on Google's image for them |
| `83-standin-task-help.txt` | stand-in | `python -m trainer.task --help` → `task.py, line 9 … ModuleNotFoundError: No module named 'tensorflow'`. The trainer cannot even print its flags outside a TF image (argparse runs after `import tensorflow`) |
| `84-standin-login-default.txt` | stand-in for `task.py:153` with the default `--wandb_key` `"16"` (digest gotcha #2; what `cli.py` sends) | **`ValueError: API key must be 40 characters long, yours was 2`** (`wandb/sdk/lib/apikey.py:239`) |
| `85-standin-login-empty.txt` | stand-in for `task.py:153` with `--wandb_key=` empty (digest gotcha #1; `70`'s args) | **`wandb: ERROR api_key not configured (no-tty). call wandb.login(key=[your_api_key])`** + `wandb.errors.UsageError: …` (`wandb_login.py:228`): the digest's text, verbatim |
| `86-standin-login-placeholder.txt` | stand-in for `task.py:153` with a 40-character key | `wandb: W&B API key is configured. Use \`wandb login --relogin\` to force relogin`, **`wandb: Appending key for api.wandb.ai to your netrc file: /root/.netrc`**; exit 0. **Crop the two `wandb: Network error (ProxyError), entering retry loop.` lines** (here and in `84`, `87`): Docker passed the sandbox's proxy variables into a `--network none` container, so they are a sandbox artifact |
| `87-standin-login-long.txt` | stand-in, extra (digest §10 key-format question) | a 47-character placeholder → `API key must be 40 characters long, yours was 47`. wandb 0.15.11 accepts **exactly** 40; today's wandb 0.31.0 checks "40+ characters" (its `wandb/sdk/lib/wbauth/validation.py`, read, not run) |
| `90-docker-ps.txt`, `91-docker-images.txt` | extra (the README has no clean-up section) | nothing running (`--rm`); the images left behind (console 2.59 GB, the stand-in, the bases) |
| `capture-only/` | not part of the tutorial | the three base-image re-tags (Dockerfiles + build logs), the placeholder key and its move log |

### `colab/` — notebook B, signed out

| file | cell | what it shows |
| --- | --- | --- |
| `C00-env.txt` | extra | Python 3.12.15 |
| `C05-pip-install-wandb.txt` | cell 5 `!pip install -q wandb -U` | quiet install; pip's root warning and upgrade notice only |
| `C05b-wandb-version.txt` | extra | today `-U` gives **wandb 0.31.0** (the notebook's stored run: 0.22.2) |
| `C38-config-rebind.txt` | extra (digest E14 / gotcha #21, on today's wandb, W&B offline mode) | cell 38's pattern `wandb.init(...)`, `wandb.config = {...}`, `wandb.config.update({"execution_time": …})` → **`type(wandb.config): dict`, `the run's config: {}`**: the config and the execution time never reach the run. Offline banner lines (`Tracking run with wandb version 0.31.0`, `W&B syncing is set to \`offline\``, `Run data is saved locally in /content/wandb/offline-run-…`) |
| `C38b-config-init.txt` | extra (the fix the repo's `task.py:313-322` uses) | `wandb.init(..., config={...})` → `type(wandb.config): Config`, the run's config holds all four keys **plus** `execution_time` |

## What cannot run here, and what was recorded instead

- **The GCP console** (enable the Vertex AI API, README:19-21; GPU quota request, README:23-44; the
  service account and key, README:60-64; the bucket, README:66-71; the Custom Jobs page,
  README:156-158). Browser clicks. Scenes draw a schematic console tagged `illustration` (never a
  screenshot, never the README's PNGs, never a logo) with the README's own field values: filter
  **`Quota: Custom model training`**, **`Custom model training Nvidia T4 GPUs per region`**, *select a
  few regions*, **`EDIT QUOTAS`** → new limit → **`NEXT`** → name → **`SUBMIT REQUEST`**; service account
  **`model-trainer`** with **Storage Admin**, **AI Platform Admin**, **Vertex AI Administrator**;
  *Actions ⋮ → Manage keys → JSON → Create*; renamed `model-trainer.json` in `secrets/`; bucket
  `cheese-app-trainer` "[REPLACE WITH YOUR BUCKET NAME]" (`08`: that name is taken). Never render a
  plausible private key (the placeholder's fields are in `laptop/capture-only/placeholder-key.json`).
- **The W&B key page** (README:73-81) and **the W&B dashboard** (README:160-163). Browser. Draw them
  as `illustration`; never draw a real-looking key (use a row of dots or the placeholder). For what a
  dashboard holds, the **`recorded`** source is notebook B's stored output (the run banners, the
  2_block "Run history"/"Run summary" block, the shared `mobilenetv2_train_base` name), from the
  instructors' 2025-10-14 Colab run with wandb 0.22.2. For the repo trainer's runs, source code is the
  only evidence: project `cheese-training-vertex-ai`, run name `mobilenetv2_train_base_True`, config
  keys `learning_rate`, `epochs`, `batch_size`, `model_name` + `execution_time` (`task.py:313-336`),
  and **no metric curves** (no callback, `task.py:326-331`; `88f3374.diff`). Draw it without numbers.
- **`gsutil cp` success** (`package-trainer.sh:4`). Captured to its honest failure (`30`). No source
  documents the success text. Scenes show the command and say what to look for (the object
  `cheese-app-trainer.tar.gz` in the bucket) **without an output panel**. The digest's
  "Copying file://… / Operation completed over 1 objects" is its expectation, not a record. The
  tarball itself (8 entries, 4016 bytes) is live.
- **`sh cli.sh` / `sh cli-multi-gpu.sh` success** (README:150, 170). Captured to the honest failure
  (`40`, `50`). The first line, `Using endpoint [https://us-central1-aiplatform.googleapis.com/]`,
  is live. The submitted-job lines are documented nowhere in the sources: show the command, the
  expanded `--worker-pool-spec`/`--args` from `40`'s `sh -x`, and describe success without a panel.
- **The job running on Vertex AI** (provisioning, logs, `JOB_STATE_SUCCEEDED`). No job log exists in
  the repo or the notebooks. What a job prints comes from **the code's own prints**, tagged
  `recorded` (code) or `illustration`: `task.py:57-68` (`tensorflow version …`, `Number of replicas:`,
  `GPU Available: …`), `:94`/`:102` (download), `:107` (`Labels: …`), `:122` (`Full size of the
  dataset: …`), `:148-150` (split counts), `:269` (`Train model`), `:308` (summary + a stray `None`),
  `:333` and `:341` (`Training Job Complete`). The **values** 1156 and 936/104/116 are recorded in both
  notebooks' outputs of the same code (A 353/445, B 410/502-503). The label order varies (digest
  gotcha #16). Do not show a TF version beyond the image name (`2-17`), epoch lines, loss values or
  timings for the repo trainer: nothing records them. The ~100 loss in the digest is its own
  estimate. The W&B lines a job would print: `Appending key … /root/.netrc` is **live** in the
  stand-in `86` (wandb 0.15.11); the `Tracking run …`/`View run at …` banner shape is recorded only
  from notebook B (wandb 0.22.2, HTML in Colab). Say so if it is shown.
- **The GPU and multi-GPU runs** (`cli.sh:22-27` uncommented; `cli-multi-gpu.sh`). There is no GPU
  quota and no account; the GPU variant of `cli.sh` fails exactly like the CPU one (same
  `gcloud ai custom-jobs create`), so it was not captured separately. `Number of replicas: 2` and
  `GPU Available: [PhysicalDevice(...GPU:0...)]` are code prints (`task_multi_gpu.py`,
  `task.py:67`): use them only as `illustration`. The prebuilt images still exist (`09`).
- **The Colab notebooks themselves** (a T4 GPU, Google sign-in for `auth.authenticate_user()`, a W&B
  secret `WandB`, the 305 MB dataset and, in notebook B, the 510 MB `experiments.zip`). Every Colab output a scene shows
  is **`recorded`** from the two extracts above (instructors' runs of 2025-10-14 and 2025-10-20). The
  stand-in ran only cell 5 and an offline E14 check (`colab/`).
- **A local CPU smoke of the trainer**: not done. `task.py` downloads the 305 MB dataset at module
  level (`task.py:96-100`) before any flag is used, and needs TensorFlow (the CPU training image is
  4.31 GB compressed, `09`). The stand-in therefore stops at `ModuleNotFoundError: No module named
  'tensorflow'` (`83`) and runs only the W&B login line (`84`-`87`), which is honest about the
  trainer's first W&B step without its data.
- **Prices.** Nothing here records a price. The digest's dollar figures are "from memory": the
  brief must not put them on screen as facts (cite the pricing page or drop the numbers).

## Capture-only deviations (the recording sandbox vs a student's machine)

None of the tutorial's commands were changed. These things around them were:

- **Placeholder names.** Bucket **`gs://your-bucket-placeholder`** (checked not to exist on
  2026-10-23, `07`), project **`your-gcp-project`**, W&B key **`PLACEHOLDER_NOT_A_REAL_WANDB_KEY_0000000`**
  (exactly 40 characters, so it passes wandb 0.15.11's length check in `86`; obviously fake). It
  appears in `10` and in `40`'s `sh -x` trace.
- **The placeholder key.** `secrets/model-trainer.json` in `05`/`06` is an obviously invalid stand-in
  (`project_id: "your-gcp-project"`, zeroed ids, `PLACEHOLDER-THIS-IS-NOT-A-REAL-KEY`;
  `laptop/capture-only/placeholder-key.json`, 415 B; a real key is about 2.3 KB). It was moved out
  before the first container start (`capture-only/placeholder-key-moves.txt`), so gcloud and
  google-auth fail with their *documented* missing-file errors rather than an undocumented parse
  error.
- **The two Dockerfile fixes** (`22`, `24`) are not capture-only: a student needs them too today.
  They are marked *extra* because the README does not contain them.
- **Proxy relay, Docker client proxies, base images.** The sandbox reaches the internet only through
  a TLS-intercepting HTTPS proxy on the host's loopback that refuses plain http. `proxy_relay.py`
  (container `l13-relay`, port 38713) forwards the bridge gateway to it. The laptop engine and its
  containers get it through `~/.docker/config.json`'s `proxies` (Docker Desktop: *Settings ›
  Resources › Proxies*). Visible effects to crop: `[IP: 172.17.0.1 38713]` on apt's lines in `21`
  (a student sees a Debian mirror's address), and wandb's `Network error (ProxyError), entering retry
  loop.` in `84`/`86`/`87` (proxy variables inside a `--network none` container).
  `python:3.13-slim-bullseye` (the repo's base), `python:3.13-slim-bookworm` (fix 1's base) and
  `python:3.10-slim-bookworm` (the stand-in) were rebuilt with the proxy's CA, https Debian sources,
  and the CA env vars (`SSL_CERT_FILE`, `PIP_CERT`, `REQUESTS_CA_BUNDLE`, `UV_NATIVE_TLS`,
  `CLOUDSDK_CORE_CUSTOM_CA_CERTS_FILE`), then re-tagged under the same names
  (`laptop/capture-only/python3.*-base.Dockerfile` + build logs). **The bullseye 404s are not caused
  by this:** the unmodified image's `/etc/apt/sources.list` points at
  `http://deb.debian.org/debian-security bullseye-security main`, the same mirror path. On
  2026-10-23 the security pool on `deb.debian.org` and `security.debian.org` lists only deb12/deb13
  files for `curl`, while `archive.debian.org` still serves the deb11 file (checked with direct
  requests). The main `bullseye` pool still serves its files. A student's build pulls the base layers
  and talks to the mirrors over http.
- **A redone segment.** The first `shell` run edited `Dockerfile:37` before it was clear the build
  fails earlier. The segment now starts with `git checkout -- Dockerfile docker-shell.sh` (silent,
  capture-only) and was re-run whole. The stale files of the first run were deleted, so each NN prefix
  is one current capture (a mid-run WIP checkpoint had briefly carried them).
- **Concurrency for `71`.** `70` runs in the background (it types `sleep 40` to stay open) while
  `71` starts a second container. Only the order matters for the error.
- **The Vertex stand-in** (`80`-`87`) is a plain Python 3.10 container in the laptop's engine, not
  Google's prebuilt image and not its install command. The `--network none` runs (`83`-`87`) execute
  only `import tensorflow` / `wandb.login(...)`. Tag those panels `extra · local stand-in`.
- **The Colab stand-in** is a container, not Colab: no `!`, no GPU, W&B in `mode="offline"` for the
  E14 check (`colab/capture-only/`).
- **Ownership details.** The laptop's home directory is setgid (Alpine's `adduser`), so files written
  by the container show group `app`/`student` (`30`, `31`). On a Mac the owner column differs. Do not make it
  load-bearing.
- **sudo / umask.** `umask 022` is set in `run_steps.sh` (docker exec defaults to 0000). sudo was
  installed but not needed. `hub_retry` (Docker Hub 429s) was armed but unused: there is no
  `hub-retries.txt`.

## Differences and findings vs the digest, found while running

**New (not in the digest):**

1. **The build fails at Dockerfile step 2 today** (`21`): bullseye-security's pool no longer holds
   the deb11 files its stale index lists. Fix: `FROM python:3.13-slim-bookworm` (`22`). Only then is
   the digest's gotcha #20 reached (`23`). The digest's "bullseye suites still answer" was true of the
   indexes, not the packages, by 2026-10-23.
2. **`sh -x cli.sh`** makes the hidden job visible (`40`): the GPU image is set, then overridden, and
   the W&B key travels inside `--args` (E18).
3. **`gsutil` prints a deprecation notice** ("Google recommends using Gcloud storage CLI …") before
   any result, in Cloud SDK 590.0.0 / gsutil 5.37 (`30`). A student sees it too.
4. **`cli.py` fails earlier than `job.run`**: the credential error comes from constructing
   `CustomPythonPackageTrainingJob` (`cli.py:23`, `60`), so its two `print`s (37-38) never run.
5. **The prebuilt images are still served** with their sizes (`09`), which answers the digest's §10
   question for `tf-cpu/tf-gpu.2-17` and `tf-gpu.2-14`. Whether they still contain scikit-learn,
   requests or a working `wandb==0.15.11` import was not checked (too big to pull).
6. **wandb 0.15.11 accepts exactly 40 characters** (`86` vs `87`). Today's wandb accepts "40+"
   (source read). If W&B now issues longer keys, the repo's pin would reject them: still open, since
   the current key format could not be checked without an account.
7. **Possible erratum in digest B12** (not verified live): the digest says that on a fresh VM wandb
   0.15.11 prints no "logged in" line at `wandb.login`. In the stand-in, `wandb.login(key=…)` treats
   the passed key as already configured and runs `login_display()` (`wandb_login.py:131-160`),
   printing `W&B API key is configured …` (`86`, offline). With network and a valid key, the same
   function prints `Currently logged in as: <user> (<entity>)`. So a real job probably prints that
   line at `task.py:153` already. Do not put either line on screen as job output without saying it is
   expected, not recorded.
8. **Today `pip install wandb -U` gives 0.31.0** (`C05b`). The notebook's stored run used 0.22.2.

**Digest confirmed live:** gotcha #1 (empty `--wandb_key=`, `70`; the `api_key not configured
(no-tty)` text verbatim, `85`), #2 (`yours was 2`, `84`), #3 (`KeyError: 'GCP_REGION'`, `60`), #17
(`pathtools` / `imp` on Python 3.13, `60`; previously untested), #18 (the README's bucket is someone
else's, `08`), #20 (word for word, once the base is fixed, `23`), #22 (name conflict, `71`); E12
(no TF / sklearn from `install_requires`, `82`, `83`); E14/#21 on today's wandb (`C38`, with the fix
`C38b`); E18 (`40`); §3.3 "the console never trains" (`26`: no tensorflow); B8's banner lines and
order (`26`), including the "activated" line printed before activation; B10's eight tar entries and
`BucketNotFoundException` (`30`); B11's `Using endpoint …` line (`40`); `.gitignore:4` (`31`); the
notebook md5s; notebook B's 2_block-only curves (E15) and shared MobileNet run name.

**Digest details to correct:** the tar order is directory order, not alphabetical (`30`); B8's
expected checkpoint line `Activated service account credentials for: …` needs a real key (here the
`ERROR` line appears instead, `26`); the digest's line-37 fix alone no longer gets the build through
(item 1).

## Versions at the time of recording (2026-10-23)

| what | version |
| --- | --- |
| laptop Docker (stand-in for Docker Desktop) | client + engine 29.8.2, BuildKit, linux/amd64; git 2.54.0 |
| `model-training-cli` image (after both fixes) | `python:3.13-slim-bookworm` → **Python 3.13.17**, **uv 0.13.5**; `google-cloud-cli` → **Google Cloud SDK 590.0.0** (core 2026.10.16, gsutil 5.37, bundled Python 3.14.8); uv.lock: **google-cloud-aiplatform 1.120.0**; 2.59 GB on disk |
| the repo's own base | `python:3.13-slim-bullseye` (Docker Hub image created 2025-08-06; `apt-get install` fails, `21`) |
| prebuilt training images (manifests only) | `tf-cpu.2-17.py310:latest` 4.31 GB, `tf-gpu.2-17.py310:latest` 8.93 GB, `tf-gpu.2-14.py310:latest` 7.61 GB compressed |
| Vertex stand-in | `python:3.10-slim-bookworm`, pip 23.0.1 → cheese-app-trainer 0.0.1, **wandb 0.15.11**, pathtools 0.1.2, protobuf 4.25.9, requests 2.34.2 … |
| Colab stand-in | Python 3.12.15; `pip install wandb -U` → **wandb 0.31.0** |
| notebooks' stored runs (recorded) | TF 2.19.0, Keras 3.10.0 (B), wandb 0.22.2 (B), Tesla T4; October 2025 |

Things that vary between runs and must be said with "at the time of recording" or cropped:
container ids in prompts, `DISPLAY_NAME`'s random hex, image ids/sizes, build timings (314 s here),
gcloud/gsutil versions (apt, unpinned), pip's resolution of wandb's unpinned dependencies (`80`,
`82`), today's `wandb -U`, timestamps and W&B offline run ids. The tarball's size (4016 B) and
entries are deterministic for this commit (up to tar's directory order).

## Re-running the captures

```
export HTTPS_PROXY=http://127.0.0.1:<port>  CA_BUNDLE=<proxy CA bundle>   # sandbox only
bash assets/terminal/capture.sh laptop setup
bash assets/terminal/capture.sh laptop pre cloud wandb shell pkg job mgpu clipy nokey vtx clean
bash assets/terminal/capture.sh laptop teardown
bash assets/terminal/capture.sh colab run
docker rm -f l13-relay
```

Needs Docker with privileged containers. The laptop container persists between segment calls.
Order matters: `pre` (clone, key, bases) → `shell` (edits, build) → the in-container segments; `vtx`
needs `pkg`'s `trainer.tar.gz`. `shell` resets the two edited files first, so it can be re-run. The
full run takes about 15 minutes (one 5-minute console build). Without `HTTPS_PROXY`/`CA_BUNDLE` the
capture-only parts (relay, CA, base re-tags, hub retries) are skipped. If the bullseye-security
mirror is ever repaired, `21` will instead fail at line 37 like `23`.

## Gate

Every README command has a capture above, exactly as written, in README order: `git clone`
(`01`), `export WANDB_KEY=...` (`10`), `sh docker-shell.sh` (`21`, `23`, `26`), `sh package-trainer.sh`
(`30`), `sh cli.sh` (`40`; the README's optional CPU variant is what `cli.sh` already runs), and `sh
cli-multi-gpu.sh` (`50`). The README steps without a live success have a documented reason and
source: the GCP console and the W&B pages (browser → `illustration`, README field values), `gsutil
cp` and job submission (honest failures captured; no source documents success → no output panel),
the Vertex job and its logs (code prints → `recorded`/`illustration`; counts from the notebooks'
stored outputs), the W&B dashboard (notebook B's stored output, the code's `wandb.init`), the GPU
variants (no quota; the same failing command), and the Colab notebooks (stored outputs; stand-in for
cell 5). The two Dockerfile fixes are documented as *extra*. No output was invented. Capture-only
logs live under `laptop/capture-only/` and `colab/capture-only/`.
