# Assets and where they come from

Everything a scene shows as "real" (a terminal output, a source line, a file listing) is read from
a file in `assets/`, never typed by hand into a scene. This file says where each one came from.

**The one thing to know about this lecture's captures:** the lecture speaks Vertex AI, the tutorial
(Conny's series decision) is the AWS pair `model-deployment-aws` + `ml-workflow-aws`, and the
recording sandbox has **no AWS account, no access key, no SageMaker and no billing**. Everything
that runs on the student's laptop is captured live, in a fresh empty Docker engine: both clones,
`aws configure`, every `sh docker-shell.sh` (as written and after the fixes), all four tutorial
images, and inside them every README command. The data stages really ran on the laptop: the
collector scraped 40 cheese images from Bing, the processor de-duplicated them and wrote real
TFRecords, the trainer trained one epoch of MobileNetV2 on them. Every AWS call stops at its
**honest first error**: `Unable to locate credentials` (model-deployment, no keys) or AWS's own
`InvalidClientTokenId` / `InvalidAccessKeyId` (ml-workflow, obviously fake placeholder keys). The
console steps are `illustration` (field values from the READMEs); the one cloud output the
tutorial documents (`--predict`) is `recorded` from the README. Two capture-only stand-ins show
what the cloud would do without pretending to be it: the exported model served by the public
TensorFlow Serving 2.13.1 image (`laptop/45`-`48`), and the pipeline's JSON definition built by
the SDK with a placeholder account (`laptop/92`). No output was invented.

**Two findings change the tutorial today (2026-11-05); the video must teach the fix:**

1. **Unpinned `sagemaker` resolves to SDK 3.** `model-deployment-aws/Pipfile:10` and
   `ml-workflow-aws/src/workflow/Pipfile:9` say `sagemaker = "*"`, and neither image uses a lock
   (model-deployment ignores `Pipfile.lock` in `.gitignore:68`; the workflow Dockerfile copies
   only the Pipfile, `Dockerfile:40-42`, and its build log says `Pipfile.lock not found,
   creating...`). Today that resolves **sagemaker 3.13.1** on the model-deployment image's
   Python 3.9 (with torch 2.8.0, 15 `nvidia-*` CUDA packages, mlflow and gevent: 185 packages,
   `laptop/22`) and **sagemaker 3.29.0** on the workflow image's Python 3.11 (`laptop/85`). SDK 3
   is a namespace package without the 2.x modules: `from sagemaker.tensorflow import ...`,
   `from sagemaker.serializers import ...`, `from sagemaker.processing import ...`,
   `from sagemaker.workflow.pipeline import ...` all raise `ModuleNotFoundError`, and
   `from sagemaker import get_execution_role` an `ImportError` (`laptop/23`, `86`). On this
   machine the unpinned model-deployment build ran 13+ minutes in `pipenv lock` and then ran out of
   disk (several GB of CUDA wheels and source builds); that failed build is not kept (environment).
   **Fix (extra, `laptop/24`, `88`):** `sagemaker = "<3"` in the Pipfile. With it the
   model-deployment image builds in 400.6 s (`laptop/25`) with sagemaker **2.257.7**, and the
   workflow image with 2.257.7 too. (The model-training image is not affected: it copies its
   committed lock and runs `pipenv sync`, sagemaker 2.250.0.) Every 2.x call prints
   `SageMakerV2DeprecationWarning: You are using the SageMaker Python SDK v2, which is on path of
   deprecation` (crop it, or say it once).
2. **The arm64 build lines.** `docker-shell.sh` builds `--platform=linux/arm64/v8` in
   model-deployment (`:19`), data-processor (`:31`) and model-training (`:32`) — "M1/2 chip macs use
   this line". On this x86_64 laptop with no arm64 emulation the first `RUN` fails with
   `exec /bin/sh: exec format error` (`laptop/20`, `65`, `70`). The fix is the script's own
   commented line above it, the plain `docker build -t $IMAGE_NAME -f Dockerfile .` (`laptop/21`,
   `66`, `71`). On an Apple-silicon Mac the arm64 line works natively; Docker Desktop on an Intel
   Mac or Windows emulates it (slowly). data-collector (`:31`) and workflow (`:29`) build
   `linux/amd64` instead, which Apple-silicon Macs emulate.

## Which commits

| repo | pinned | date, subject | how checked |
| --- | --- | --- | --- |
| [dlops-io/model-deployment-aws](https://github.com/dlops-io/model-deployment-aws) | `main` @ **`077f4dbc7b13ccef208c65a8e29489331261029e`** | 2025-08-25 17:13:00 −0300, "Merge pull request #1 from dlops-io/itamar/aws-initial-commit" | `git ls-remote` on 2026-11-05: `HEAD` = `refs/heads/main` = `077f4db`; the fresh clone's `laptop/11-git-log.txt` shows the same |
| [dlops-io/ml-workflow-aws](https://github.com/dlops-io/ml-workflow-aws) | `main` @ **`f165c6e17895d3d6c33a150d349f4b2649c807db`** | 2025-08-19 08:50:13 −0400, "Migrate ml-workflow from GCP to AWS" | `git ls-remote` on 2026-11-05: `HEAD` = `refs/heads/main` = `f165c6e`; `laptop/51-git-log.txt` |

Other refs of model-deployment-aws (not used): branches `itamar/aws-initial-commit` @ `1e34bff`,
`itamar/new-trained-mobile-net` @ `00a4f08` (both merged into `077f4db`), tag `v1.0` @ `6ecc50b`
(README only; its release asset `mobilenetv2_train_base_True.zip` is what `--prepare` downloads,
`cli.py:84-88`). ml-workflow-aws has only `main`.

The batch `units.json` and the course map name the GCP repos (`model-deployment` @ `3fbf63f`,
`ml-workflow` @ `972ffbb`); this video follows the AWS pair instead (series decision). The published
exam edition `videos/ac215-l15-exam/` quotes `ml-workflow-aws` at the same `f165c6e`.

## `source/` — the tutorials' own files

Copied unchanged with `git show <commit>:<path>`, the repos' relative paths preserved under
`source/model-deployment-aws/` and `source/ml-workflow-aws/`. Course material by the AC215 teaching
staff (Harvard IACS), used for study with the instructor's permission. Not copied: `images/`
(architecture and console screenshots: never in a frame or the repository) and `data/*.jpg` (the
eight sample photos; the captures list them).

**One masked value:** `source/model-deployment-aws/docker-shell.sh:8` holds, at `077f4db`, a
SageMaker role ARN with a real-looking 12-digit AWS account id. The copy has it replaced by
`YOUR_ACCOUNT_ID` (`arn:aws:iam::YOUR_ACCOUNT_ID:role/model-deployment-sagemaker`); every other
byte is unchanged. No capture prints the original line (`17` shows the edited lines 5-9). The
README's own example ARN (`README.md:43`, `cli.py:143`) uses AWS's documentation placeholder
account `123456789012`; it is kept as written (it is the README's placeholder, say so if shown).

### `source/model-deployment-aws/` (Part A)

| file | what a panel quotes from it |
| --- | --- |
| `README.md` | the whole tutorial (203 lines): clone (9-10), services (12-16), IAM user + policies (21-30), SageMaker execution role (32-44, example ARN 43), S3 bucket (46-52), security warning (56-58), Option 1 `aws configure` (64-75), Option 2 exports (77-83), Update Configuration (85-90), Quick Start block (92-108), Prepare (110-117), Deploy (119-129, "typically 5-10 minutes" 127), Test Predictions + sample output (131-148), clean-up: console (154-157), AWS CLI (159-164), CLI script (166-176), troubleshooting (178-197) |
| `cli.py` | constants (30-43: `BEST_MODEL`, the 4-label map 41-42), `download_file` (46-63), `prepare()` (66-123: create bucket 70-82, download the release 84-88, Keras export into version folder `1` 97-112, `model.tar.gz` 114-117, upload 119-123), `deploy()` (126-185: role 131-145, `TensorFlowModel(framework_version="2.13")` 151-159, timestamped endpoint name 163-167, `deploy(instance_type="ml.m5.xlarge")` 168-174, `endpoint_config.json` 180-185), `predict()` (188-239: payload `{"instances": [...]}` 225, argmax + label 230-234), `delete()` (242-312), leftover GCP words (318 "GCS Bucket", 342-358 "Vertex AI", 337 "Data Collector CLI") |
| `Dockerfile` | `FROM ubuntu:20.04` (2), AWS CLI v2 by architecture (15-23), Docker CE (26-36), `python3.9` + `pip install pipenv` (39-42), user `app` uid 1000 (44-47), `ADD Pipfile` + `RUN cd /app && pipenv lock && pipenv sync` (52-55), entrypoint (62) |
| `Pipfile` | the six unpinned-but-one packages (8-14: `sagemaker = "*"` at 10, `tensorflow = "==2.18.0"`), `python_version = "3.9"` (17) |
| `docker-shell.sh` | the three values to edit (7-9, line 8 masked as above), the two build lines (17 commented, 19 arm64), `docker run ... -v ~/.aws:/home/app/.aws -e AWS_REGION ...` (22-28: no key variables are passed) |
| `docker-entrypoint.sh` | `Container is running!!!`, `aws sts get-caller-identity` (7), `pipenv shell` (10) |
| `.gitignore` | `.aws/`, `credentials` (27-29), `artifacts/`, `*.tar.gz`, `model.tar.gz` (33-38), `endpoint_config.json` (41), `Pipfile.lock` (68) |

### `source/ml-workflow-aws/` (Part B)

| file | what a panel quotes from it |
| --- | --- |
| `README.md` | the whole tutorial (248 lines): the four components (4-7), clone (15-16), services (18-24), bucket (26-30), IAM user + keys (35-49), install + configure + test the CLI (51-69), roles (71-81), data collector (88-100), data processor (107-120), model training local/remote/monitor (126-145), Build & Push: Docker Hub (155-162), ECR variables (167-174), push block (176-199), standalone processing job (210-224), pipeline (226-240), components (243-248) |
| `src/data-collector/` `Dockerfile`, `Pipfile`, `Pipfile.lock`, `cli.py`, `downloader.py`, `docker-shell.sh`, `docker-entrypoint.sh` | `python:3.11-slim`, root, `pipenv install --system --deploy` from the lock; `cli.py` search → zip → `upload_file(..., "raw.zip")` (35-65); the Bing scraper (`downloader.py`); the key check (`docker-shell.sh:13-26`), amd64 build (31), mounts incl. `../../../persistent-folder/` (9, 36) |
| `src/data-processor/` `Dockerfile`, `Pipfile`, `cli.py`, `cleanser.py`, `tfrecords.py`, `docker-shell.sh`, `docker-entrypoint.sh` | no lock: `RUN pipenv lock && pipenv install --system --deploy` (`Dockerfile:29`); `--clean` (37-68) and `--prepare` (69-95); difPy de-duplication (`cleanser.py:7-32`); label folders → indices (`tfrecords.py:11-16`) |
| `src/model-training/` `Dockerfile`, `Pipfile`, `Pipfile.lock`, `cli.py`, `package-trainer.sh`, `package/setup.py`, `setup.cfg`, `PKG-INFO`, `package/trainer/{__init__,task}.py`, `docker-shell.sh`, `docker-entrypoint.sh` | `pipenv sync` from the lock (TF 2.20.0, sagemaker 2.250.0); `cli.py --train` = `TensorFlow(... framework_version="2.13", py_version="py310", instance_type="ml.m5.xlarge")` + `fit(wait=False)` (40-74); `task.py`: `num_classes = 3` (68), SageMaker vs local data paths (71-111), MobileNetV2 (182-222), the serving signature with JPEG preprocessing (276-301), save under `.../1` (303-322); `package-trainer.sh` tar + `aws s3 cp` |
| `src/workflow/` `Dockerfile`, `Pipfile`, `Pipfile.lock`, `cli.py`, `model.py`, `deploy_model_lambda.py`, `docker-shell.sh`, `docker-entrypoint.sh` | `ADD Pipfile` only + `RUN pipenv install` (`Dockerfile:40-42`); `cli.py`: module-level STS call (31-32), ECR image URIs (35-36), `data_collector()` (44-80), `pipeline()` (157-328: five steps, `CacheConfig` 165, property references 219-220, 266-267, 277, 309, `upsert` + `start` 326-327); `model.py` role derivation (19-48), `model_training` (51-100), `model_deploy` (103-178); the Lambda handler (`deploy_model_lambda.py`) |
| `.gitignore`, `LICENSE` | context only |

There is no Colab notebook for this lecture.

## `terminal/` — real terminal sessions

Captured **2026-11-05 04:00–05:50 UTC** by `terminal/capture.sh`, which runs
`terminal/run_steps.sh` inside one fresh "laptop" container, one segment at a time. Each README
command runs exactly as written, in README order, and its output goes to its own file: the file
starts with the command (`$ ...`), then the output, then its exit status (`[exit N]`). Steps that
are not in the README are marked *extra* below and in `run_steps.sh`.

Two kinds of file, as in L13/L14: **`step` files** (no terminal, plain output) and **`istep` files**
(a real pseudo-terminal via `ptyrun.py`, 110×50, commands typed at the container's prompt — every
`sh docker-shell.sh` that opens a container: `13`, `25`, `27`-`30`, `55`, `60`, `68`, `73`, `90`).
In the `istep` files the build's TTY progress view is the final screen; for the three big images the
build ran first as a plain `step` (`67`, `72`, `89`: same command docker-shell.sh runs, plain log),
so the `istep` that follows shows a cached build and the container session.

**The environment.** `laptop/`: `docker:29.8.2-dind` (Docker client + engine 29.8.2, linux/x86_64,
Alpine), a fresh empty engine; user `student` (uid 1000) in the `docker` group; git 2.54.0, curl,
GNU sed, tree, python3 (for `ptyrun.py`), and **AWS CLI 2.34.63** from Alpine's packages (README
B:51-53 "Install AWS CLI": brew / snap / curl installer; `laptop/01`). Home is `/home/student`, the
two clones sit side by side in it, so `../../../persistent-folder` (ml-workflow's shared data folder)
is `~/persistent-folder`.

Versions inside the tutorial images (at the time of recording):

| image (README section) | base, Python | key packages | size |
| --- | --- | --- | --- |
| `model-deployment-cli-aws` (A, with the `<3` pin) | `ubuntu:20.04`, **Python 3.9.5** (pipenv runs under the system 3.8) | tensorflow **2.18.0**, keras 3.10.0, sagemaker **2.257.7**, sagemaker-core 1.0.78, boto3 1.42.97, numpy 2.0.2, pillow 11.3.0 | 4.01 GB |
| `cheese-app-data-collector` (B) | `python:3.11-slim` (Debian 13 trixie), Python 3.11.18 | from its lock: boto3 1.40.11, requests, beautifulsoup4 | 600 MB |
| `cheese-app-data-processor` (B) | same | resolved at build: tensorflow **2.13.1**, difPy 4.2.1, dask 2026.8.0, scikit-learn 1.9.1, boto3 1.43.124 | 2.58 GB |
| `cheese-app-training-cli` (B) | same | from its lock: tensorflow **2.20.0**, keras 3.11.2, sagemaker **2.250.0**, boto3 1.40.11 (+ `awscli` v1 from pip, system-wide) | 2.7 GB |
| `cheese-app-workflow` (B, with the `<3` pin) | same + AWS CLI **2.39.4** | sagemaker **2.257.7**, sagemaker-core 1.0.78, boto3 1.43.124 | 1.09 GB |
| `tensorflow/serving:2.13.1` (extra stand-in) | Docker Hub, digest `sha256:057ad7f532fc…caf55` | TensorFlow Serving 2.13.1 | 518 MB |

### `laptop/` — Part A, model-deployment-aws

| file | README step | what it shows |
| --- | --- | --- |
| `00-env.txt`, `01-aws-version.txt` | extra | date, `Linux x86_64`, Docker 29.8.2, git 2.54.0, an empty image list; `aws-cli/2.34.63`, `/usr/bin/aws` |
| `10-clone.txt` | "Clone the github repository" (A:9-10; the README links the repo, this is the usual `git clone`) | `Cloning into 'model-deployment-aws'...` |
| `11-git-log.txt`, `12-ls.txt` | extra | `077f4dbc7b13…` + date + subject; the repo root (`docker-shell.sh` is already executable, `-rwxr-xr-x`) and the eight images in `data/` |
| `13-aws-configure.txt` | Option 1 (A:64-75), `aws configure`, **no keys** (the two key prompts answered with Enter), `us-east-1`, `json` | the AWS CLI's new tip first: `Tip: You can deliver temporary credentials to the AWS CLI using your AWS Console session by running the command 'aws login'.`, then the four prompts `AWS Access Key ID [None]:` … `Default output format [None]: json` |
| `14-aws-files.txt` | extra (A:75 "This will create ~/.aws/credentials and ~/.aws/config") | only `config` exists (no keys were typed): `[default] region = us-east-1 output = json` |
| `15-sts-no-keys.txt` | extra (what the container's entrypoint will try, `docker-entrypoint.sh:7`) | `aws: [ERROR]: An error occurred (NoCredentials): Unable to locate credentials. You can configure credentials by running "aws login".`, exit 253 |
| `16-option2-exports.txt` | Option 2 (A:79-83), the three `export` lines verbatim (the README's own placeholders), then `aws sts get-caller-identity` (extra) | AWS's answer to the placeholder key: `An error occurred (InvalidClientTokenId) when calling the GetCallerIdentity operation: The security token included in the request is invalid.`, exit 254 |
| `17-edit-docker-shell.txt` | "Update Configuration" (A:85-90; sed is the editor) | lines 5-9 after the edit: `S3_MODELS_BUCKET_NAME="your-models-bucket-placeholder"`, `SAGEMAKER_ROLE="arn:aws:iam::000000000000:role/SageMakerExecutionRole"` (placeholder account), `AWS_REGION="us-east-1"` |
| `18-chmod.txt`, `19-ls-l.txt` | Quick Start (A:98) `chmod +x docker-shell.sh`; extra `ls -l` | silent, exit 0; `-rwxr-xr-x … docker-shell.sh` |
| `20-docker-shell-arm64.txt` | A:99 `sh docker-shell.sh`, **as written** | the arm64 `ubuntu:20.04` is pulled, then `[ 2/14] RUN apt-get update && …` → `exec /bin/sh: exec format error` (lines 36, 40), `ERROR: failed to build`, exit 1 (`set -e` stops before `docker run`) |
| `21-use-plain-build.txt` | extra (the script's own line 17) | lines 17-21 after the swap: `docker build -t $IMAGE_NAME -f Dockerfile .` active, the arm64 line commented |
| `22-resolve-today.txt` | extra, capture-only check (`helpers/resolve_check.sh`): what pip's resolver (the one inside `pipenv lock`) picks today for the Pipfile's `[packages]` on Python 3.9, dry run, nothing installed (`python:3.9-slim` + a current pip 26.0.1) | `185 packages would be installed, among them:` `sagemaker==3.13.1`, `sagemaker-core==2.13.1`, `-train/-serve/-mlops==1.13.1`, `torch==2.8.0`, fifteen `nvidia-*-cu12`, `mlflow==3.1.4`, `gevent==26.7.0`, `tensorflow==2.18.0`, `keras==3.10.0`, `numpy==2.0.2`, `boto3==1.42.97`. (3.13.1 is the last SDK 3 release that still allows Python 3.9; 3.14.0 and later need ≥ 3.10, PyPI metadata) |
| `23-sagemaker3-imports.txt` | extra, capture-only check (`helpers/sagemaker_import_check.sh`): the five SDK 3.13.1 packages without their dependencies, then `cli.py`'s own import lines | `sagemaker is a namespace package`, `its modules: ['ai_registry', 'core', 'lineage', 'mlops', 'serve', 'train']`; `ModuleNotFoundError: No module named 'sagemaker.tensorflow'` (`cli.py:21`), `ImportError: cannot import name 'get_execution_role' from 'sagemaker'` (`:22`), `ModuleNotFoundError: No module named 'sagemaker.serializers'` (`:23`) |
| `24-pin-sagemaker.txt` | extra, **the fix** | `git diff Pipfile`: `-sagemaker = "*"` / `+sagemaker = "<3"` |
| `25-docker-shell.txt` | A:99 a third time (plain build line + pin); extras typed inside | `[+] Building 400.6s (19/19) FINISHED`, step `[13/14] RUN cd /app && pipenv lock && pipenv sync` 334.7 s; `Container is running!!!`, `Testing AWS connectivity...`, `aws: [ERROR]: … (NoCredentials): Unable to locate credentials …` (line 32: the entrypoint goes on), `Launching subshell in virtual environment...`, prompt `(app) app@<id>:/app$`; `Python 3.9.5`, the venv python, `/usr/local/bin/pipenv`, `/usr/local/bin/aws`; the pip list above; `your-models-bucket-placeholder us-east-1 arn:aws:iam::000000000000:role/SageMakerExecutionRole`; `/home/app/.aws` = the laptop's `~/.aws` (config only); `python cli.py --help` (after the SDK and TensorFlow start-up lines): `Data Collector CLI`, `--prepare  Prepare model and save model to GCS Bucket`, `--deploy  Deploy saved model to Vertex AI`, `--predict  Make prediction using the endpoint from Vertex AI`, `--test  Test deployment to Vertex AI` (the leftover GCP words, erratum) |
| `26-docker-images.txt` | extra | `model-deployment-cli-aws:latest … 4.01GB` |
| `27-prepare.txt` | Quick Start A:102 / "Prepare Model for Deployment" (A:110-117), typed inside a new `sh docker-shell.sh` session; extra `ls -la artifacts` | `Prepare model and save model to GCS Bucket`, boto3's `PythonDeprecationWarning: Boto3 will no longer support Python 3.9 starting April 29, 2026` (crop or mention), then a rich traceback ending at **`cli.py:73 s3_client.create_bucket(...)`** → `NoCredentialsError: Unable to locate credentials`: the bucket is created *before* the download (erratum), so nothing is downloaded; `ls: cannot access 'artifacts'` |
| `28-deploy.txt` | A:103 / "Upload & Deploy" (A:119-129) | `Deploy model`, `Deploying model to SageMaker endpoint...`, traceback through `cli.py:168 tensorflow_model.deploy(` → `NoCredentialsError: Unable to locate credentials` |
| `29-predict.txt` | A:104 / "Test Predictions" (A:131-148) | `Error: endpoint_config.json not found. Please deploy the model first.`, `image_files: ['data/brie-1.jpg', 'data/gruyere-2.jpg', 'data/parmigiano-2.jpg', 'data/brie-2.jpg', 'data/parmigiano-1.jpg']` (the first five of an unsorted glob, not the sampled ones), then five times `Image: …` / `Error invoking endpoint: Unable to locate credentials` / `Make sure the endpoint 'model-mobilenetv2-train-base-True-v1-endpoint' exists and is in service` (the sample is drawn with replacement: `brie-2` three times); exit 0 |
| `30-delete.txt` | A:107 / "Using the CLI Script" (A:166-176) | `Delete endpoint, model, and S3 artifacts`, traceback → `NoCredentialsError: Unable to locate credentials` (first SageMaker call: `list_endpoint_configs`) |
| `31-aws-cli-delete-as-written.txt` | "Using AWS CLI" (A:161), exactly as written | `bash: -c: line 1: syntax error near unexpected token 'newline'`: the `<…>` are placeholders the shell reads as redirections |
| `32-aws-cli-delete.txt` | A:161 with a placeholder name (extra) | `(NoCredentials): Unable to locate credentials`, exit 253. A:162-163 (endpoint config, model) behave the same and were not run separately |

### `laptop/` — Part A extras: what the cloud would do, shown locally

| file | what | what it shows |
| --- | --- | --- |
| `40-prepare-local.txt` | **capture-only helper** `helpers/prepare_offline.py`: `cli.py`'s own `prepare()` in the tutorial image with the same mount, the S3 client replaced by a stub that sends nothing (`create_bucket` prints a `[capture stub] … NOT sent` line; `upload_file` raises) | the real local half: the release zip downloaded, `Using Keras 3 export()`, `Saved artifact at './artifacts/model-mobilenetv2_train_base_True.v1/1'`, the export's input/output signature, `Uploading model to s3://your-models-bucket-placeholder/model-mobilenetv2_train_base_True.v1/model.tar.gz`, then `RuntimeError: [capture stub] upload_file(...) NOT sent: no AWS account in this recording`. Tag the panel `extra · capture stub`; never show it as a successful upload |
| `41-artifacts.txt` | extra | what the release zip holds (`.keras` 9.8 MB, `.weights.h5`, `.json`, metrics + history JSON) and the export: `…v1/1/saved_model.pb`, `variables/…`, `fingerprint.pb`, `assets/`, `…v1/model.tar.gz` |
| `42-tarball.txt` | extra (`cli.py:114-117`: "SageMaker expects version number") | `tar tzvf model.tar.gz`: everything under `1/` |
| `43-signature.txt` | extra (`saved_model_cli show`, in the image) | `inputs['input']` `DT_FLOAT` `(-1, 224, 224, 3)`; `outputs['output_0']` `(-1, 4)`: **four classes** (the README's sample shows three numbers, erratum); `Method name is: tensorflow/serving/predict` |
| `44-git-status.txt` | extra | ` M Pipfile`, ` M docker-shell.sh` (the two edits), `artifacts/` ignored by `.gitignore:33` |
| `45-serving-pull.txt` | extra stand-in | `docker pull tensorflow/serving:2.13.1` (SageMaker's TF 2.13 serving image, `cli.py:154`, runs TensorFlow Serving too; this is the public image, **not** SageMaker's) |
| `46-serving-start.txt` | extra stand-in | the exported folder served as model `cheese`: `NodeDef mentions attribute debug_name which is not in the op definition … Unknown attributes will be ignored` (TF 2.18 export, 2.13 server: digest open question 2, it loads), `SavedModel load for tags { serve }; Status: success: OK`, `Successfully loaded servable version {name: cheese version: 1}`, `Exporting HTTP/REST API at:localhost:8501`; `GET /v1/models/cheese` → version `1`, `"state": "AVAILABLE"` |
| `47-predict-local.txt` | **capture-only helper** `helpers/predict_local.py`: `cli.py`'s own `predict()` with only `sagemaker.Predictor`/`Session` replaced by a client that POSTs the same `{"instances": [...]}` to the local server (random sample seeded) | `[capture stand-in] endpoint 'model-mobilenetv2-train-base-True-v1-endpoint' -> local TensorFlow Serving at …`, then five real predictions with **four** numbers each, e.g. `Image: data/gouda-2.jpeg` / `Result: {'predictions': [[0.00427136, 0.18224588, 0.0100982478, 0.803384542]]}` / `… 3` / `Label:    gouda`; `brie-1` → brie (0.45), `gruyere-1` → gruyere (0.70); **`parmigiano-1` → `brie` (0.977)**: a real mistake of the released model. Tag `extra · local stand-in, not SageMaker` |
| `48-serving-stop.txt`, `49-md-images.txt` | extra | the server removed; the images before removal (4.01 GB) and the cleaned engine |

### `laptop/` — Part B, ml-workflow-aws

| file | README step | what it shows |
| --- | --- | --- |
| `50-clone.txt`, `51-git-log.txt`, `52-tree.txt` | "Clone the github repository" (B:15-16); extras | `Cloning into 'ml-workflow-aws'...`; `f165c6e1…`; the tree: four folders under `src/`, only collector, training and workflow have a `Pipfile.lock` |
| `53-test-config.txt` | "Test Configuration" (B:65-69), after `13`'s keyless `aws configure` (B:55-63) | both commands: `(NoCredentials): Unable to locate credentials …` |
| `54-collector-docker-shell-no-keys.txt` | B:94-95 `sh docker-shell.sh` in `src/data-collector` | the script's own check (`docker-shell.sh:13-26`): `AWS not configured. Run: aws configure`, exit 1, nothing built |
| `55-aws-configure-placeholder.txt` | B:57-63 `aws configure` again, **capture-only placeholder keys** (`PLACEHOLDER_NOT_A_REAL_ACCESS_KEY` / `PLACEHOLDER_NOT_A_REAL_SECRET_KEY_000000000000`, obviously fake); region and output kept with Enter (`[us-east-1]`, `[json]`) | the four prompts; a student types the keys from the downloaded `.csv` here (B:49) |
| `56-aws-configure-list.txt` | extra | `access_key : ****************_KEY : shared-credentials-file`, `secret_key : ****************0000`, `region : us-east-1 : config-file : ~/.aws/config` |
| `57-test-config-placeholder.txt` | B:67-68 again | AWS's real answers to a key that does not exist: `(InvalidClientTokenId) when calling the GetCallerIdentity operation: The security token included in the request is invalid.`; `(InvalidAccessKeyId) when calling the ListBuckets operation: The AWS Access Key Id you provided does not exist in our records.` |
| `60-collector.txt` | B:95 `sh docker-shell.sh`; "Test Data Collector" B:99, verbatim; extras | `[+] Building 40.4s (11/11) FINISHED`, the root prompt `root@<id>:/app#` (no banner: `exec bash`); `CLI Arguments: Namespace(search=True, nums=10, query=[…], bucket='')`, `S3_BUCKET_NAME: cheese-app-ml-workflow-demo`, four times `Searching for: …` … `[%] Done. Downloaded 10 images.` (lines 24-610, real Bing results; four `[!] Issue getting:` lines of skipped links), `uploading file /persistent/dataset/raw.zip`, then `boto3.exceptions.S3UploadFailedError: Failed to upload /persistent/dataset/raw.zip to cheese-app-ml-workflow-demo/raw.zip: An error occurred (InvalidAccessKeyId) …` (B:100 "check your S3 bucket" cannot pass); extras: `raw  raw.zip`, the four label folders with `10` files each, `raw.zip` 14,171,510 bytes |
| `61-persistent-on-laptop.txt` | extra | `~/persistent-folder` appeared beside the clones, **owned by root** (Docker created the missing mount folder; digest gotcha 16), with `dataset/raw`, `raw.zip` |
| `62-collector-image.txt` | extra | `cheese-app-data-collector:latest … 600MB` |
| `65-processor-docker-shell-arm64.txt` | B:113 `sh docker-shell.sh` as written | `exec /bin/sh: exec format error` at the first `RUN` (lines 50, 54), exit 1 |
| `66-use-plain-build.txt` | extra | `docker-shell.sh:29-34` after the swap (the script also carries a third, `amd64/v2` line, commented) |
| `67-processor-build.txt` | extra: the build line alone, plain log | `#9 [5/6] RUN pipenv lock && pipenv install --system --deploy`: `Locking dependencies...`, `✔ Success!` after 13 s, `Installing dependencies from Pipfile.lock`, step `DONE 183.8s` |
| `68-processor.txt` | B:113 again; "Test Data Processor" B:117 `python cli.py --clean`, B:119 `python cli.py --prepare`; extras | `--clean`: raw found locally, `Labels: ['parmigiano cheese', 'gruyere cheese', 'brie cheese', 'gouda cheese']`, per label `difPy preparing files: [100%]`, `Search Results: {}` (no duplicates among these 40), `uploading file /persistent/dataset/clean.zip` → `S3UploadFailedError … (InvalidAccessKeyId)`; `--prepare`: clean found locally, `Full size of the dataset: 40`, `train_xy count: 32`, `validate_xy count: 8`, `/persistent/dataset/tfrecords/train_0000.tfrecords`, `val_0000.tfrecords`, `uploading file /persistent/dataset/tfrecords.zip` → same upload error; extras: the dataset folder (`clean`, `raw`, `tfrecords` + three zips), the two TFRecord files (4.8 MB, 1.2 MB), `10` per clean label, the versions |
| `69-processor-image.txt` | extra | 2.58 GB; removed afterwards (the sandbox's disk) |
| `70-training-docker-shell-arm64.txt`, `71-use-plain-build.txt` | B:131 as written; extra | `exec /bin/sh: exec format error` (lines 53, 57); the swap |
| `72-training-build.txt` | extra: the build line alone | `pip install pipenv awscli` 21.0 s, `RUN pipenv sync` 70.0 s |
| `73-training.txt` | B:131 again; "Local Training" B:136 verbatim; "Remote Training" B:138 `sh package-trainer.sh`, B:139 `python cli.py --train`; extras | `Container is running!!!`, `(app) app@<id>:/app$`; `Python 3.11.18`, the versions; `/persistent` and `dataset` owned by root. **Local training:** `tensorflow version 2.20.0`, CPU only, `TFRecords found at /persistent/dataset/tfrecords`, MobileNetV2 weights downloaded from the Keras applications store, the model summary with **`dense_1 (Dense) (None, 3)`** (line 119: `num_classes = 3`, `task.py:68`, while the data has four labels; erratum), `8/8 … accuracy: 0.4062 - loss: 108.4501 - val_accuracy: 0.6250 - val_loss: 107.7770` (line 132; the L1 regularizers dominate the loss), Keras's `Your input ran out of data` warning, `Change model signature and save`, then **`PermissionError: [Errno 13] Permission denied: '/persistent/model'`** (line 146, `task.py:312`): the container runs as `app` (uid 1000) and the root-owned folder from `61` refuses it (digest gotcha 16, live; on Docker Desktop for Mac the mount is not root-owned). `from tensorflow.python.keras import backend as K` imports fine with TF 2.20 (digest open question 3). **package-trainer:** the `tar` file list (`package/trainer/task.py` … `package/PKG-INFO`), `upload failed: ./trainer.tar.gz to s3://cheese-app-ml-workflow-demo/cheese-app-trainer.tar.gz An error occurred (InvalidAccessKeyId) …`; `trainer.tar.gz` 3,632 bytes. **--train:** `Train Model`, then `sagemaker.get_execution_role()` → `InvalidClientTokenId` → `RuntimeError: Unable to derive SageMaker execution role. Please ensure CheeseAppSageMakerExecutionRole exists in your AWS account.` (line 313) |
| `74-training-image.txt` | extra | 2.7 GB; removed afterwards |
| `80-ecr-variables.txt` | "Pushing Docker Image to Amazon ECR", B:169-173 verbatim, then B:198's `echo` | **`export: '[YOUR': not a valid identifier`, `export: 'REGION]': not a valid identifier`** (the bracket note pasted with the command; `REGION` itself is still set), the account lookup's `InvalidClientTokenId`, and **`ECR URI: .dkr.ecr.us-east-1.amazonaws.com/cheese-app-data-collector:latest`**: with no account id the URI starts with a dot; exit 0, nothing stops |
| `81-ecr-create.txt` | B:182 (extra: the first AWS call of the push block) | `(UnrecognizedClientException) when calling the CreateRepository operation: The security token included in the request is invalid.`, exit **0**: `|| true` hides it |
| `85-resolve-today.txt` | extra, capture-only check (as `22`) for `src/workflow/Pipfile` on Python 3.11 | `133 packages would be installed`: `sagemaker==3.29.0`, `sagemaker-core==2.29.0`, `-train/-serve/-mlops==1.29.0`, `mlflow==3.18.0`, `boto3==1.43.124` |
| `86-sagemaker3-imports.txt` | extra, capture-only check (as `23`) with `src/workflow/cli.py`'s imports | `ModuleNotFoundError: No module named 'sagemaker.processing'` (`cli.py:13`), `… 'sagemaker.workflow'` (`:15-19`), `… 'sagemaker.tensorflow'` (`:21-22`) |
| `87-committed-lock.txt` | extra | `Pipfile.lock pins sagemaker ==2.250.0 and boto3 ==1.40.11`; `Dockerfile` lines 40 (`ADD … Pipfile /app/`), 42 (`RUN pipenv install`), 45: the lock never enters the image |
| `88-pin-sagemaker.txt` | extra, the same fix as `24` | `git diff`: `-sagemaker = "*"` / `+sagemaker = "<3"` |
| `89-workflow-build.txt` | extra: the build line alone (`docker-shell.sh:29`, `--platform=linux/amd64`) | the AWS CLI installer's long file list (lines ~40-9290: show only its ends), `Pipfile.lock not found, creating...` (line 9334), `✔ Success!`, `Installing dependencies from Pipfile.lock` |
| `90-workflow.txt` | B:217-218 `sh docker-shell.sh` in `src/workflow`; B:223 `python cli.py --data_collector`; B:233 `--pipeline`; B:246-248 `--data_processor`, `--model_training`, `--model_deploy`; extras | the entrypoint banner `Container is running!!!`, `AWS Region: us-east-1`, `S3 Bucket: cheese-app-ml-workflow-demo`, `Package URI: s3://cheese-app-ml-workflow-demo`, `aws sts get-caller-identity` → `InvalidClientTokenId`, then `pipenv shell` anyway; versions (`aws-cli/2.39.4`); `/data-collector` and `/data-processor` mounted; `bash: docker: command not found` (the Docker socket is mounted, `docker-shell.sh:34`, but the image has no Docker CLI); **every one of the five commands stops at the same place, before its own code runs:** `INFO:botocore.credentials:Found credentials in environment variables.`, traceback at **`cli.py:32 ACCOUNT_ID = sts_client.get_caller_identity()['Account']`** (module level) → `ClientError: An error occurred (InvalidClientTokenId) when calling the GetCallerIdentity operation: The security token included in the request is invalid.` (no region error for the bare STS client: digest open question 6) |
| `91-workflow-image.txt` | extra | 1.09 GB |
| `92-pipeline-definition.txt` | **capture-only helper** `helpers/pipeline_offline.py`: `cli.py`'s own `pipeline()` in the workflow image; account lookups answer with the placeholder `000000000000`, the default bucket and the Lambda ARN are placeholders, `Pipeline.upsert()` prints `Pipeline.definition()` instead of sending it and stops | `Using derived SageMaker execution role: arn:aws:iam::000000000000:role/CheeseAppSageMakerExecutionRole`, the SDK's v3 migration notes (`Processor` → `DataProcessor`, `TensorFlow` → `ModelTrainer`, `TensorFlowModel` → `ModelBuilder`), `Running within a PipelineSession, there will be No Wait, No Logs, and No Job being started.`, then the pipeline JSON: five steps `DataCollector` (59), `DataProcessor` (113), `ModelTraining` (186), `CreateModel-CreateModel` (246), `DeployModel` (260), wired by property references `{"Get": "Steps.DataCollector.ProcessingOutputConfig.Outputs['raw-data'].S3Output.S3Uri"}` (143), `…DataProcessor…Outputs['tfrecords']…` (212), `Steps.ModelTraining.ModelArtifacts.S3ModelArtifacts` (254), `Steps.CreateModel-CreateModel.ModelName` (264); `CacheConfig {"Enabled": true, "ExpireAfter": "30d"}`; then `[capture stub] Pipeline.upsert() and start() NOT sent`. Tag `extra · built offline, not sent`. **Mask `763104351884`** (lines 191, 251: AWS's public Deep Learning Containers registry account inside the training and inference image URIs) as `<aws-dlc-account>` on screen: it is AWS's, not a secret, but it reads like an account id (series rule) |
| `95-docker-ps.txt`, `96-docker-images.txt`, `97-laptop-files.txt` | extra | nothing running (`--rm`); the images left; `~/persistent-folder/dataset` (root-owned) with the three stages' output; `git status`: the two `docker-shell.sh` edits, the workflow `Pipfile` pin, `__pycache__/` |

### `laptop/capture-only/`

The capture-only base images (Dockerfiles + build logs: `ubuntu-20.04-base`, `python-3.11-slim-base`,
and `python-3.9-slim` built the same way for `22`/`23`), `hub-retries.txt` (Docker Hub rate-limit retries during the capture, if any).

### `expected/` — what only the cloud shows (not run here)

| file | tag | source |
| --- | --- | --- |
| `md-predict-readme.txt` | `recorded` | `model-deployment-aws/README.md:137-147` verbatim (the code fence dropped): the `--predict` output against a live endpoint. Three numbers per image and `0` → `gouda`: an older 3-class model; today's release has four outputs and `cli.py:42` maps 0 → parmigiano (`laptop/43`, `47`). Show it with that note |

## What cannot run here, and how each is shown

| README step | why not | how the video shows it |
| --- | --- | --- |
| A:12-16, B:18-24 enable services; A:21-30, B:35-49 IAM user, policies, access keys; A:32-44, B:71-81 roles; A:46-52, B:26-30 S3 bucket; B:20-21 SageMaker AI quick setup, Unified Studio domain | AWS console, needs an account | schematic console drawings tagged `illustration` with the README's own values (`model-deployment` / `ml-workflow-user`, the policy names, `SageMakerExecutionRole` / `CheeseAppSageMakerExecutionRole` / `CheeseAppLambdaExecutionRole`, buckets `cheese-app-models-demo` / `cheese-app-ml-workflow-demo` "[REPLACE WITH YOUR UNIQUE BUCKET NAME]"); no screenshots, no logos |
| real access keys in `aws configure` (A:67, B:57) | no account | `13` (no keys) and `55` (obviously fake placeholders), said as such |
| `--prepare` upload, `--deploy` (5-10 min, A:127), `--predict` against the endpoint, `--delete` | no credentials | `27`-`30` honest errors; the local half in `40`-`43`; the endpoint's job by the local TF Serving stand-in `45`-`47` (tagged); the documented cloud output `expected/md-predict-readme.txt` (`recorded`) |
| A:162-163 `delete-endpoint-config`, `delete-model` | same as A:161 | `31`/`32` stand for all three |
| "check your S3 bucket" (B:100, 118, 120) | no bucket | the local files the stages wrote (`60`, `61`, `68`) + the upload errors |
| B:138 the upload of `trainer.tar.gz`, B:139 the training job, B:141-145 monitoring in the console | no account | `73` (tar real, upload error, role error); console = `illustration` (Training › Training jobs, job name `cheese-…`) |
| B:155-162 Docker Hub login/build/push (`<USER NAME>`, `<ACCESS TOKEN>`) | needs a Docker Hub account and token | the commands only (no output panel); B:153 says it "has already been done for this tutorial", but `src/workflow/cli.py:35-36` pulls from the student's own ECR (digest erratum 5) |
| B:176-199 ECR push (`get-login-password`, tag, push, list-images) | needs an account | `80`, `81` (the variable block and the first call, real); the rest command-only |
| B:223 processing job, B:233 pipeline run, B:234-240 Unified Studio view, B:245-248 component jobs | needs an account | `90` (each stops at `cli.py:32`); the DAG from `92` (built offline, tagged) and drawn as a diagram; the README's two pipeline screenshots are **not** used (re-draw: five boxes DataCollector → DataProcessor → ModelTraining → CreateModel → DeployModel, as `92` lists them) |
| a GPU | none here | not needed by this tutorial (all CPU: `ml.m5.*`, `ml.t3.medium`) |

## Capture-only deviations (the recording sandbox vs a student's machine)

None of the tutorial's commands were changed. These things around them were:

- **Placeholders.** Bucket `your-models-bucket-placeholder` and role
  `arn:aws:iam::000000000000:role/SageMakerExecutionRole` in Part A (`17`); the ml-workflow scripts'
  own bucket `cheese-app-ml-workflow-demo` is left as committed (it is the README's placeholder;
  every upload fails before reaching it). Keys `PLACEHOLDER_NOT_A_REAL_ACCESS_KEY` /
  `PLACEHOLDER_NOT_A_REAL_SECRET_KEY_000000000000` (`55`). The pipeline helper's account
  `000000000000` (`92`).
- **The fixes are not capture-only.** The plain build line (`21`, `66`, `71`) and the `<3` pin
  (`24`, `88`) are what a student on an x86_64 machine, or anyone today, needs too. They are marked
  *extra* because the README does not contain them.
- **Proxy relay, CA, https apt sources.** The sandbox reaches the internet only through a
  TLS-intercepting HTTPS proxy on the host's loopback that refuses plain http. `proxy_relay.py`
  (container `l15-relay`, port 38715) forwards the bridge gateway to it; the laptop engine and its
  containers get it through `~/.docker/config.json`'s `proxies`. `ubuntu:20.04`, `python:3.11-slim`
  and `python:3.9-slim` were rebuilt with the proxy's CA, https apt sources and the CA env vars
  (`SSL_CERT_FILE`, `PIP_CERT`, `REQUESTS_CA_BUNDLE`, `AWS_CA_BUNDLE`) plus `PIP_NO_CACHE_DIR=1`
  (disk), then re-tagged under the same names (`laptop/capture-only/*-base.Dockerfile`). Visible
  effect: apt lines say `https://deb.debian.org` / `https://archive.ubuntu.com` where a student sees
  `http://`. For the arm64 attempts the amd64-only re-tag is removed first, so the build pulls
  Docker Hub's own arm64 base as a student's would (`arm64_attempt` in `run_steps.sh`).
- **Disk.** The sandbox's disk is small and shared: the laptop's Docker storage is a 9 GB tmpfs,
  the classic overlay2 store is used (`containerd-snapshotter: false`), each big image is removed
  after its segment (`49`, `69`, `74`), and a watchdog in `capture.sh` stops builds if free disk
  drops below 1.5 GB. The unpinned model-deployment build (13+ minutes in `pipenv lock`, then
  `No space left on device`) is **not** kept as a capture: it fails for the sandbox's reason, not
  the student's; `22`/`23` show what it would have installed and what that does.
- **The laptop is Alpine.** `sh` there is BusyBox ash, which understands the scripts' `[[ … ]]`
  and `&>` like bash (and like macOS's `sh`), so `54`'s refusal is what a Mac shows. On
  Debian/Ubuntu `sh` is dash, where the check misbehaves (digest gotcha 2, tested by the digest's
  author, not captured here): on Linux run `bash docker-shell.sh`.
- **Ownership.** Linux Docker creates a missing bind-mount folder as root (`61`), which is why `73`
  hits `PermissionError`; Docker Desktop on a Mac maps the mount to the user. The video says "on
  Linux" when it shows `73`'s error, with the fix: create `persistent-folder` yourself before the
  first `docker-shell.sh` (or `sudo chown -R $USER ../../../persistent-folder`). The trainer's
  successful save after that fix was **not** captured (the image was removed for disk); show
  `task.py:303-322` instead of an output.
- **Rich tracebacks.** The SageMaker SDK installs `rich` tracebacks (boxed frames, `❱` marks) in
  `25`-`30`, `73`, `90`, `92`; the panels pick the first frame line and the final error line.
- **`22`-`23`, `85`-`86` run in plain `python:3.9-slim` / `python:3.11-slim` containers** (the
  images' Python minor versions), with pip's resolver, not `pipenv lock` itself; `23`/`86` install
  the SDK packages with `--no-deps` (enough to see its modules). Tag them `extra · check`.
- **The `14`/`25` `.aws` folder.** Part A mounts `~/.aws` read-write; the AWS CLI inside creates
  `~/.aws/cli/` on the laptop (seen in `25`).

## How to re-run

`bash assets/terminal/capture.sh setup`, then `pre md-setup md-shell md-local md-clean`, then
`mw-setup mw-coll mw-proc mw-train mw-push mw-flow mw-dag mw-end`, then `teardown` (behind the
sandbox proxy, export `HTTPS_PROXY` and `CA_BUNDLE` first; `docker rm -f l15-relay` at the end).
`md-resolve` and `mw-lock` re-run `22` and `87` alone. Versions move: sagemaker 3.x releases weekly
(3.29.0 on 2026-11-05), and the arm64/amd64 lines behave differently on Apple silicon; the narration
says "at the time of recording" wherever a version or a resolved package list appears.
