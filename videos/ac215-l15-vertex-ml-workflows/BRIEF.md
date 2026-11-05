# Brief · AC215 L15 — ML workflows: deploy one model, then let a pipeline run them all

The design of this video, written before the script. Series rules: `docs/AC215_SERIES.md` and
`.claude/skills/ac215-video/SKILL.md` (scene-code pitfalls, never-do list). Facts: `digest.md` (the
tutorial digest, already rebuilt against the two AWS repos), `SLIDES.md` (the lecture-slide digest)
and `assets/` (real captures, see `ASSETS.md`). **Where the digest or the slides and the captures
disagree, the captures win.** The captures are the newest source (2026-11-05 04:00–05:50 UTC). Every
README command was run as written, in README order, on a fresh "laptop" (an empty Docker 29.8.2
engine, x86_64). Every AWS call stops at its honest first error, because this sandbox has no AWS
account.

Conny, 2026-11-02: 「我还是需要每一节Lecture非常仔细的slide by slide然后github repo上一步一步的训练」.
So this is the **full follow-along**: the slides the tutorial applies, and every README step of both
tutorials, in order.

**The tutorial choice (Conny's series decision).** The lecture speaks **Vertex AI**. The course map
(`units.json`) names the GCP repos `dlops-io/model-deployment` and `dlops-io/ml-workflow`. This video
follows the **AWS pair** instead: `dlops-io/model-deployment-aws` @ `077f4db` and
`dlops-io/ml-workflow-aws` @ `f165c6e` (both re-checked with `git ls-remote` on 2026-11-05, see
`ASSETS.md`). The slides decide the *concepts*; the AWS READMEs and the captures decide what the
video *shows*. The video says kindly, once per idea, where the slide's Vertex AI word has an AWS
counterpart (S02 builds the bridge table; later scenes use one bridge sentence each).

The published exam edition `videos/ac215-l15-exam/` (concept-first, 13:23) is a sibling. Reuse its
verified facts, its colour choices for DAG edges and task states, and its lexicon entries
(`Kubeflow`, the cheese names) where they agree. Its deployment and pipeline facts are GCP facts
(`model-deployment` @ `cf0b7c7`, `ml-workflow` @ `3730009`); only its S07 AWS coda
(`ml-workflow-aws` @ `f165c6e`: five steps, edges from property references) carries over directly.

| topic | digest / slides / exam edition | captures and AWS code (use these) |
| --- | --- | --- |
| `sagemaker = "*"` | digest erratum 8: "captures confirm or refute" for the workflow image only | **Both** images break today. Model-deployment (Python 3.9) resolves **sagemaker 3.13.1**, 185 packages with torch 2.8.0 and fifteen CUDA wheels (`laptop/22`). The workflow image (Python 3.11) resolves **3.29.0** (`laptop/85`). SDK 3 has no `sagemaker.tensorflow`, `.serializers`, `.processing` or `.workflow`, and no `get_execution_role` (`laptop/23`, `86`). The fix shown is `sagemaker = "<3"` (`laptop/24`, `88`), which gives 2.257.7; the build then takes 400.6 s (`laptop/25`) |
| arm64 build lines | digest gotcha 1: "emulated (slow) or fails" | It fails here: `exec /bin/sh: exec format error` at the first `RUN` (`laptop/20`, `65`, `70`). The fix is the script's own commented plain line (`laptop/21`, `66`, `71`) |
| `--prepare` | README: download → SavedModel → tar → upload | `cli.py:70-82` **creates the bucket first**: the run stops at `cli.py:73` before anything is downloaded (`laptop/27`). The local half runs for real with only S3 stubbed (`laptop/40`-`43`, tagged `extra · capture stub`) |
| the model's outputs | README's sample output: three numbers, 0 → gouda | `saved_model_cli`: input `(-1, 224, 224, 3)` float, output **`(-1, 4)`** (`laptop/43`). Today `cli.py:41-42` maps 0 → parmigiano |
| what the endpoint would answer | nothing captured in the cloud | A local stand-in: `tensorflow/serving:2.13.1` loads the export (with a `debug_name` warning, `laptop/46`), and `cli.py`'s own `predict()` gets four real numbers per photo; **`parmigiano-1` comes back brie (0.977)** (`laptop/47:33-36`). Tag `extra · local stand-in, not SageMaker` |
| the local training run | digest open question 3 (`tensorflow.python.keras` import) | It imports fine with TF 2.20 and one epoch trains on CPU. The model summary shows **`dense_1 (Dense) (None, 3)`** (`laptop/73:119`, `task.py:68 num_classes = 3`). The save then fails with **`PermissionError: '/persistent/model'`** (`laptop/73:146`), because Docker on Linux created `persistent-folder` as root (`laptop/61`) |
| the pipeline | digest §3.6: edges from property references | The JSON definition, built offline by the SDK with a placeholder account (`laptop/92`), lists five steps (lines 59, 113, 186, 246, 260). The steps are wired by `{"Get": "Steps.…"}` references (143, 212, 254, 264), with `CacheConfig {"Enabled": true, "ExpireAfter": "30d"}`. Tag `extra · built offline, not sent`. **Mask `763104351884` (lines 191, 251) as `<aws-dlc-account>`** |
| every workflow flag | digest: each flag starts its job | All five flags stop at the **same module-level STS call**, `cli.py:32 ACCOUNT_ID = sts_client.get_caller_identity()['Account']`, before any of their own code runs (`laptop/90`) |
| the workflow container | digest: mounts the Docker socket | It has **no `docker` command**: `bash: docker: command not found` (`laptop/90:44`). The ECR push block runs on the laptop |
| `aws configure` | README: four prompts | AWS CLI 2.34.63 prints a new first line: `Tip: … running the command 'aws login'.` (`laptop/13`) |
| SLIDES.md "This video and the slides" | maps the slides onto the GCP plan (`digest.md` §8 of the old GCP digest) | Its slide *ranges* and *gaps* still guide us. Its conflicts 1–3 and 6–9 are GCP-specific. The scene plan below re-maps every scene onto the slides for the AWS code and **supersedes SLIDES.md §1** |

## Audience and goal

An AC215 student who has done L1–L14:
- Docker images and containers, `docker-shell.sh` scripts with bind mounts (L2–L4);
- pipenv and lockfiles (L1 "the older way", L3);
- the cheese collector, processor and TFRecords (L6–L9);
- the trainer package and a managed training job (L13);
- serverless deployment on Cloud Run (L14).

**This is the series' first AWS lecture.** The viewer needs an AWS account with billing and the AWS
CLI v2 on their laptop, and is new to IAM users, access keys and roles, to S3, SageMaker, ECR,
Lambda, endpoints and SageMaker Pipelines. They watch with clones of
[model-deployment-aws](https://github.com/dlops-io/model-deployment-aws) and
[ml-workflow-aws](https://github.com/dlops-io/ml-workflow-aws) open, and they pause to run each step.
**The cloud steps bill**: GOLD tags mark each one, and the video ends on the teardown checklist.

After the video they can:
- map the lecture's Vertex AI words onto AWS. GCS bucket → S3; Model Registry → a SageMaker Model;
  endpoint → endpoint configuration + endpoint; Vertex AI Pipelines → SageMaker Pipelines; the KFP
  DSL compiled to YAML → SageMaker SDK step classes upserted as JSON; Artifact Registry → ECR;
  a service account → an IAM user's key on the laptop and a role in the cloud;
- set up an IAM user with an access key, a SageMaker execution role and a bucket. They can say which
  identity their laptop uses (the user's key) and which the cloud jobs use (the role), and why
  Option 2's exported keys never reach the Part A container;
- build both CLI containers today. They know the two one-line fixes: the plain build line on an
  Intel/AMD machine, and `sagemaker = "<3"`, explained with the L1 idea that a constraint is not a
  pin;
- explain what `--prepare` produces: a SavedModel in a version folder `1/`, in `model.tar.gz`, in
  S3. They can read its signature (floats in, four numbers out) and say where preprocessing lives
  in Part A (on the client) and in the Part B trainer (inside the model: the lecture's slide 14);
- explain what `--deploy` creates (a Model, an endpoint configuration, an endpoint on one
  `ml.m5.xlarge`), what `--predict` sends (150,528 floats per photo) and what it gets back. They
  know why "serverless" here means no server *to manage*, not scale to zero, and what `--delete`
  misses;
- run the collector, processor and trainer containers by hand. They know the four labels come from
  the query strings, the `num_classes = 3` slip, and the root-owned `persistent-folder` on Linux;
- push the two step images to *their own* ECR. They can spot the pasted-bracket trap, and they
  know why the URI comes out starting with a dot;
- read `pipeline()`: five typed steps, edges made by **property references** (not by list order),
  30-day caching, a Lambda that deploys. They know the laptop only defines, upserts and starts,
  that the data travels through the bucket by file name, and that a green `DeployModel` does not
  mean the endpoint is `InService`;
- tear everything down, including the endpoints the scripts forget.

## Length and parts

~31 minutes. Narration **~4,190 words** (Kokoro af_heart, speed 0.9 ≈ 174 wpm ≈ 24 min); typing,
outputs, schematic console fills and four ponder timers bring it to ~30–32 min. Word budgets per
scene are targets (±15 %).

- **Part 1 = S01–S09** (~2,340 words, ~17 min): **deploy one model**, README A
  (`model-deployment-aws`), slides 6–17 and 41.
- **Part 2 = S10–S16** (~1,850 words, ~14 min): **automate the workflow**, README B
  (`ml-workflow-aws`), slides 18–40.

The cut is the lecture's own seam (agenda items 2 and 3, slide 18's divider) and the README seam (one
repo ends, the other begins). Part 1 ends on an **empty endpoint slot with the GOLD meter stopped**
and the parked question: "you ran four commands by hand to deploy one model. The Cheese App has four
stages before that. Who runs all of them, in the right order, every time?" Part 2 opens on that
question (slides 20–21).

## Colours (series table, applied)

| meaning | colour |
| --- | --- |
| your laptop, its terminal, `~/.aws`, the IAM **user's access key** (it lives on your disk), the people at four CLIs (slide 20) | GREY |
| the cloud: S3 buckets, SageMaker (Model, endpoint configuration, endpoint, Processing/Training jobs, the pipeline and its executions), ECR, Lambda, the IAM **role badges** (cloud principals), the AWS console | BLUE |
| containers and images: `model-deployment-cli-aws`, the four `cheese-app-*` images, AWS's prebuilt TensorFlow training and serving images, the TF Serving stand-in | TEAL |
| shared and outside your control: PyPI's "newest release" that `"*"` lets in, AWS-managed policies (`AmazonS3FullAccess` …), the scraped web, root-owned folders Docker made for you | ORANGE |
| what you own and pin: `sagemaker = "<3"`, committed `Pipfile.lock`s, your model artifact (`.keras`, SavedModel, `model.tar.gz`), the TFRecords, the pipeline definition | GREEN |
| tools and libraries: aws CLI, docker, pipenv, git, boto3, the SageMaker Python SDK, TensorFlow | PURPLE |
| errors and "don't": `exec format error`, `ModuleNotFoundError`, `NoCredentialsError`, `InvalidClientTokenId`/`InvalidAccessKeyId`, `PermissionError`, `not a valid identifier`, the `(None, 3)` layer, the forgotten endpoint | RED |
| your turn, the README tracker, "look here now", the ponder timer | YELLOW |
| money: endpoints (`ml.m5.xlarge`, `ml.m5.large`), Processing/Training jobs, S3 storage, ECR storage, Lambda, the teardown card | GOLD |
| routes and references: S3 URIs, the prediction request and its JSON, `-v`/`-e` arrows into a container, **property references** (DAG edges: PINK solid, as the exam edition's data edges) | PINK |
| the past and the future (L13 training job, L14 Cloud Run, L23 automation) and the slide's Vertex AI words beside their AWS counterparts | GREY, dashed |

Pipeline step states, as in the exam edition: pending = WHITE outline; running = YELLOW fill;
succeeded = GREEN ✓ badge at the right end (slide 37's look); failed = RED; cached = GREY dashed
with a small "cached" chip. **Identity badges:** a GREY key card for the IAM user, a BLUE hard-hat
badge for each role (`SageMakerExecutionRole`, `CheeseAppSageMakerExecutionRole`,
`CheeseAppLambdaExecutionRole`).

## Running example

- **The laptop** (`laptop/`: a fresh `docker:29.8.2-dind` engine, linux/x86_64, standing in for
  Docker Desktop): user `student`, terminal title `laptop`, prompts `student@laptop:~$`, then
  `…:~/model-deployment-aws$`, `…:~/ml-workflow-aws/src/data-collector$` and so on. The step files
  carry no prompt; the scenes draw this one. Inside containers, the prompt is taken from each
  capture: `(app) app@<id>:/app$` (Part A, training, workflow) and `root@<id>:/app#` (collector,
  processor). The container id is never read aloud.
- **Say once (S02):** "this recording has no AWS account. Every step that runs on your laptop is
  real. Every AWS call stops at its honest first error. Where the cloud would answer, you see either
  the README's own recording (tagged `recorded`) or a local stand-in (tagged), never a faked
  success." Also once, in S04: "on an Apple-silicon Mac the arm64 line works as written."
- **Placeholders on screen:** bucket `your-models-bucket-placeholder` and role
  `arn:aws:iam::000000000000:role/SageMakerExecutionRole` (Part A, `laptop/17`); keys
  `PLACEHOLDER_NOT_A_REAL_ACCESS_KEY` / `PLACEHOLDER_NOT_A_REAL_SECRET_KEY_000000000000`
  (`laptop/55`); the README's own example ARN account `123456789012` (README A:43, AWS's
  documentation placeholder, say so if shown); the pipeline helper's account `000000000000`.
- **The sample photos** in `data/` are named, never shown (`laptop/12`, `49`). The scraped Bing
  images are never shown, and their URLs are never put on screen: crop `laptop/60` to the
  `Searching for:` / `[%] Done. Downloaded 10 images.` lines.

## Visual set pieces (the 3Blue1Brown part)

Class names go in `scenes/common.py`; none collides with a scene class in `video.yaml`.

- **V1 · `IdentityBadges` — a key on the laptop, roles in the cloud (S03 built, S10, S14, S16).**
  A GREY laptop on the left and the BLUE cloud on the right.
  - `aws configure` writes a GREY key card into `~/.aws/credentials` (a drawer labelled
    `~/.aws`). Next to it is `config` with `us-east-1` / `json`. In the capture only `config`
    exists (`laptop/14`), because no keys were typed.
  - **Part A**: a PINK `-v ~/.aws:/home/app/.aws` arrow carries the whole drawer into the TEAL
    container (`docker-shell.sh:24`).
  - **Option 2**: three `export` cards float in the laptop's shell. When `docker run` starts, they
    hit the container wall and fall off. Only `-e AWS_REGION`, `S3_MODELS_BUCKET_NAME` and
    `SAGEMAKER_ROLE` pass (`docker-shell.sh:22-28`). This is erratum 3, drawn.
  - **Part B** (S10): `docker-shell.sh` reads the key out of the drawer (`aws configure get …`) and
    passes it as `-e AWS_ACCESS_KEY_ID …` (`data-collector/docker-shell.sh:13-26`, `:37-39`).
  - **In the cloud**, every job, the endpoint and the Lambda wear a BLUE role badge. No key crosses
    the border. `_resolve_role()` builds the badge's ARN from *your* account id
    (`model.py:19-34`): that is why a fake key fails at "derive role" (`laptop/73:313`).
- **V2 · `StarVsPin` — the version line for `sagemaker` (S04, reprise S14).** This echoes L1's V4.
  - A number line runs 2.200 … 2.257 | 3.0 … 3.29. `sagemaker = "*"` lights the whole line ORANGE.
    PURPLE `pipenv lock` drops a dot at the newest release that fits: 3.13.1 on Python 3.9
    (`laptop/22`); on Python 3.11 it would be 3.29.0 (`laptop/85`).
  - Under the 2.x half, a shelf of modules (`tensorflow`, `serializers`, `processing`,
    `workflow`, `get_execution_role`). Under 3.x, a different shelf (`core`, `train`, `serve`,
    `mlops`, `lineage`, `ai_registry`, from `laptop/23`). `cli.py`'s import lines reach for their
    module and grab air: RED `ModuleNotFoundError`.
  - `"<3"` slides in as a GREEN wall at 3.0. The dot jumps back to 2.257.7 and the imports click.
    Caption: "a constraint is not a pin" (L1). A side note shows the committed lock (2.250.0)
    sitting unused (`laptop/87`) in the workflow image.
- **V3 · `TwoPipes` — where does preprocessing live? (S05 built, S08, S12).** This draws slide 13.
  - **Left pipe (Part A)**: a JPEG on the GREY laptop goes through gears labelled `resize 224×224`
    and `÷ 255` (`cli.py:221-223`). A 224×224×3 cube of floats travels the PINK wire to the BLUE
    endpoint, enters the model's front door (`inputs['input'] DT_FLOAT (-1, 224, 224, 3)`,
    `laptop/43`), and four bars come out.
  - **Right pipe (Part B's trainer)**: the JPEG's raw bytes travel the wire. The gears now sit
    *inside* the model's front door, labelled `serving_default`: `decode_jpeg → float32 → resize`.
    These are slide 14's three call-outs, filled in by `task.py:276-301`.
  - S05: the label "client-side brittleness" appears over three differently-tuned client gear
    sets (a web app, a phone, a notebook), with slide 13's second reason beside it: one copy is
    easier to roll back and version.
  - S08: the left pipe's cube counts up to **150,528** numbers.
- **V4 · `ArtifactTrip` — slide 12's steps 1–3 on AWS (S06).**
  - A GREY dashed GitHub release box (`v1.0`, `mobilenetv2_train_base_True.zip`) drops a GREEN
    `.keras` file into the TEAL container (`cli.py:84-88`).
  - `model.export(…)` unfolds it into a SavedModel folder: `saved_model.pb`, `variables/`,
    `fingerprint.pb` (`laptop/41`).
  - The folder slides into a sub-folder labelled `1` ("SageMaker expects version number",
    `cli.py:102-104`). `tarfile` wraps it into `model.tar.gz`, with `1/` inside (`laptop/42`).
  - A PINK arrow carries the tarball toward the BLUE S3 bucket at
    `s3://<bucket>/model-mobilenetv2_train_base_True.v1/model.tar.gz`. In the capture the arrow
    stops at a RED wall, because the stub sends nothing (`laptop/40`).
  - The bucket-creation step is drawn **first** in the chain, in RED: that is where the real
    `--prepare` stops (`laptop/27`, `cli.py:73`).
- **V5 · `ThreeObjects` — Model, endpoint configuration, endpoint (S07 built, S09, S15).** Slide 12's
  steps 4–5 in AWS shapes.
  - A **Model** card holds three slots: the artifact (PINK S3 URI), the serving container (TEAL:
    TensorFlow Serving 2.13, `framework_version="2.13"`, `cli.py:154`) and the role (BLUE badge).
    "Nothing runs yet."
  - An **endpoint configuration** names a variant: `AllTraffic`, instance type, count 1, weight 1
    (from `deploy_model_lambda.py:25-36`).
  - An **endpoint** is an address plate with a machine slid under it (`ml.m5.xlarge`, count 1,
    `cli.py:168-174`). A GOLD meter starts and keeps running with zero traffic.
  - The slide's "Model Registry" box sits GREY dashed above the Model card ("the README says
    registry; the code makes a plain Model").
  - S09 (`--delete`): the endpoint goes first (the meter stops), then the configuration, then the
    Model, then the S3 artifact. A second, older timestamped endpoint stays lit: the one
    `endpoint_config.json` no longer names.
  - S15 (Lambda): `update_endpoint` swaps the configuration behind the same plate.
- **V6 · `ManualToPipeline` — four people, four terminals (S10).** Slides 20–21 redrawn: four tiles
  (Data Collector, Data Processor, Model Training, Model Deploy), each with a GREY person at a CLI
  under it. The headline changes from "How do we execute these steps?" to "Can we automate this
  flow?". One BLUE SageMaker Pipelines box replaces the four people (with "Vertex AI Pipelines"
  GREY dashed beside it). Slide 22's duties then appear as a card with ticks for this repo: order ✓
  (references), repeatable ✓ (caching, same definition), resources ✓ (instance types per step),
  monitoring ✓ (Studio's graph), scheduling ✗ (L23).
- **V7 · `CallableImage` — one image, two modes (S11 built, S14).** Slide 36 redrawn as one TEAL
  image with a switch on its input (`data-collector/docker-entrypoint.sh:4-8`):
  - no arguments → `exec bash`, an interactive shell (development mode: what `sh docker-shell.sh`
    gives you);
  - arguments → `exec "$@"`, which runs the command and exits (production mode).
  - S14: SageMaker's `Processor(entrypoint=["python3", "/app/cli.py"])` lifts the switch out and
    plugs its own command in front of the job arguments (`workflow/cli.py:52-80`). Same image, the
    same `cli.py`, run by a machine you never log into.
- **V8 · `ReferenceDAG` — a pipeline drawn by references (S15 built, S16 recap).**
  - The five step boxes from `laptop/92`: `DataCollector`, `DataProcessor`, `ModelTraining`,
    `CreateModel`, `DeployModel`. They start as an unordered pile beside the Python list
    `steps=[step_collect, step_process, step_train, step_create_model, step_deploy_lambda]`.
  - Each property reference in the code lights up in PINK
    (`step_collect.properties.ProcessingOutputConfig.Outputs["raw-data"].S3Output.S3Uri`, …) and
    draws a PINK solid edge between two boxes. The pile falls into a chain.
  - The list is shuffled: the graph does not move.
  - A sheet of JSON (`{"Get": "Steps.DataCollector…"}`) is pressed out of the graph. This is the
    AWS form of slide 29's compile-to-YAML.
  - The laptop's `upsert` hand passes it to BLUE SageMaker; `start()` returns at once.
  - **The shared drawer**: under the chain, the S3 bucket. Each step's *declared* folder
    (`/opt/ml/processing/output` → `s3://<b>/raw`) is drawn as an empty tray. The real files
    `raw.zip`, `clean.zip`, `tfrecords.zip` drop into the bucket root **by name**, GREY dashed
    (`data-collector/cli.py:65`, `data-processor/cli.py:68`, `:95`).
  - A "cached · 30d" chip sits on each box (`cli.py:165`).
  - S16: slide 40's chain runs along the top: recipe (SDK step classes) → printed instructions (the
    JSON definition) → operator (`upsert` + `start`) → engine and manager (SageMaker Pipelines) →
    workers (the jobs' machines); the DAG is their job sheet.

## README step tracker (ReadmeTracker, top-left)

One tracker per README section, titled with the README's own heading (shortened). Step titles are
≤ 3 words. README A = `model-deployment-aws/README.md` @ `077f4db`; README B =
`ml-workflow-aws/README.md` @ `f165c6e`.

| tracker | README lines | steps |
| --- | --- | --- |
| **A1 · Setup Environments** | A:9-52 | Clone repo · Enable services · IAM user · Execution role · S3 bucket (5) |
| **A2 · Run Container** | A:60-99 | aws configure · Env variables · Edit config · chmod +x · docker-shell (5) |
| **A3 · Prepare, deploy, predict** | A:101-148 | Prepare model · Deploy endpoint · Test predictions (3) |
| **A4 · Clean Up** | A:150-176 | Console delete · AWS CLI · CLI script (3) |
| **B1 · Setup Environments** | B:15-81 | Clone repo · AWS services · S3 bucket · IAM user · Access keys · Install CLI · Configure CLI · Test config · IAM roles (9) |
| **B2 · Data Collector** | B:88-100 | docker-shell · Run search · Check bucket (3) |
| **B3 · Data Processor** | B:107-120 | docker-shell · Run clean · Check bucket · Run prepare · Check bucket (5) |
| **B4 · Model Training** | B:126-145 | docker-shell · Local training · Package trainer · Remote training · Monitor jobs (5) |
| **B5 · Build & Push** | B:152-203 | Hub login · Hub build · Hub push · ECR variables · Pull image · Create repo · ECR login · Tag image · Push image · Verify push · Print URI (11) |
| **B6 · Automate Collector** | B:210-224 | docker-shell · Processing job · Check console (3) |
| **B7 · SageMaker Pipelines** | B:226-248 | Run pipeline · Check Studio · Test components (3) |

Steps the README does not have are marked `extra` in the tracker caption and in the narration
("this one isn't in the README"). They include:
- `git log`, `ls`, `tree` (`laptop/11`, `12`, `51`, `52`);
- `~/.aws` and `aws sts get-caller-identity` checks (`14`, `15`), `aws configure list` (`56`);
- the build-line swap (`21`, `66`, `71`) and the pin (`24`, `88`), the resolver checks
  (`22`, `23`, `85`, `86`, `87`, tagged `extra · check`);
- `docker images`, `ls -l` and ownership checks (`19`, `26`, `61`, `62`, `69`, `74`, `91`, `95`-`97`);
- the local stand-ins (`40`-`47`, `92`).

S01, S02 and the S16 recap have no tracker.

## Scene plan

Notation:
- `laptop/NN` = `assets/terminal/laptop/NN-*.txt`; `expected/…` likewise. Line numbers are file
  lines: line 1 is the typed `$` command, never printed as output; `[exit N]` is never printed.
- ▶ = a README step the viewer must do, with a `your turn` tag at real checkpoints (about one per
  tracker).
- CODE(file: a-b) quotes `assets/source/<repo>/…` with real line numbers, ≤ 12 lines on screen.
- CONSOLE = a schematic AWS console form, tagged `illustration`, with the README's own field values.
  Never a screenshot, never a logo.
- `lecture_ref(15, "a–b")`, slide ranges from `SLIDES.md`. **A lecture tag lives exactly as long as
  the picture it cites**: it fades in with the redrawn slide idea and fades out with it, never
  carried into the next beat (the L14 final check found tags outliving their pictures).
- Rich tracebacks (the boxed `│ ❱` frames in `25`-`30`, `73`, `90`, `92`): show the first frame
  line and the final error line, with `…` between.
- SDK and boto3 deprecation warnings (`SageMakerV2DeprecationWarning`,
  `PythonDeprecationWarning: Boto3 will no longer support Python 3.9 starting April 29, 2026`) and
  TensorFlow's CUDA/oneDNN start-up lines are cropped. Say once (S04) "you'll see deprecation
  warnings; they're not the error".

### Part 1 · Deploy one model (`model-deployment-aws`)

**S01 · Three numbers or four? (~200 words) — `s01_hook.py` · `Hook`.** Cold open, no tracker.
- The broken thing, as two panels side by side, both answering "what cheese is this?":
  - left, tagged `recorded` (`expected/md-predict-readme.txt`, the README's own `--predict`
    output): `Result: {'predictions': [[0.0887…, 0.0439…, 0.867…]]}` → `Label: brie`, **three**
    numbers;
  - right, tagged `extra · local stand-in` (`laptop/47:23-26`): same code, **four** numbers →
    `Label: brie`.
- The puzzle: "Same command, same code. One answer has three numbers, the other four. They can't
  both come from the same model. So what *is* behind an endpoint?"
- Three empty slots appear: the **artifact** (which model), the **container** (what runs it), the
  **machine** (where, and who pays). A GOLD meter beside the machine slot ticks while no request
  arrives. `lecture_ref(15, "11")` appears for this beat only (slide 11's "continuous cost to keep
  an endpoint up") and leaves with the meter.
- Teaser for part 2: four stage tiles flicker into a chain. "Then we stop running these steps by
  hand."
- How to follow along: the two READMEs, eleven small trackers, `▶ your turn`; the study guide has
  every command. "This is the series' first AWS lecture: you need an AWS account and the AWS CLI."

**S02 · Where we are, in AWS words (~250) — `s02_map.py` · `LectureMap`.** No tracker.
`lecture_ref(15, "6–10")`, changing its range with each picture (6–7, then 8, then 10).
- Slide 6 redrawn small: POC → Prototype → MVP, with the unlabelled current-position box over
  Prototype (Build Better Models, ML Workflow, the start of Deployment). Then slide 7's four tiles:
  Collector, Processor and Training ticked; **Model Deploy** open. "Part 1 fills that tile; part 2
  connects all four."
- Slide 8 in one line: L14 put containers on Cloud Run. A GREY dashed L14 card stays at the edge.
- Slide 10 redrawn as a four-row sidebar: Workbench, Training (L13, ticked), **Online prediction**,
  **Pipelines** (today's two, YELLOW).
- **The AWS bridge**, built row by row as a two-column card (Vertex word GREY dashed left, AWS word
  right). It returns as a mini-legend in later scenes:
  - GCS bucket → **S3 bucket**;
  - service-account key → **IAM user + access key** (laptop) / **role** (cloud);
  - Model Registry → **SageMaker Model**;
  - Online prediction endpoint → **endpoint configuration + endpoint**;
  - Vertex AI Pipelines (Kubeflow, KFP DSL) → **SageMaker Pipelines** (SDK step classes);
  - Artifact Registry → **ECR**;
  - Cloud Functions → **Lambda**.

  Kindly: "the lecture is written for Vertex AI. This course also ships an AWS version of both
  tutorials, and that's the one we follow. Same ideas, different names; I'll point out each one as
  we meet it."
- **The sandbox, said once** (Running example). Shown at once: `laptop/15:3`
  (`Unable to locate credentials`) as the "honest first error" the viewer will see again.
- Versions at the time of recording, one line: Docker 29.8.2, AWS CLI 2.34.63 (`laptop/00`, `01`).

**S03 · A user, a role and a bucket (~300) — `s03_setup.py` · `UserRoleBucket`.** Tracker A1 1→5,
then A2 1→2. No lecture_ref, except slide 12's bucket box redrawn for one beat:
`lecture_ref(15, "12")`, faded with it.
- ▶ A1·1 Clone: `laptop/10` (tagged `extra` for its spelling: the README says "clone or download"),
  extras `11` (`077f4db`) and `12` (the eight sample photos named, not shown; `docker-shell.sh`
  already executable).
- ▶ A1·2–4 as CONSOLE strips (README A:12-44):
  - services: S3, SageMaker, IAM;
  - IAM user `model-deployment` with three policies, `IAMFullAccess` ORANGE-flagged as broader than
    the code needs (erratum 12 of the digest, one clause);
  - "Create access keys … save" (A:29-30), no key drawn;
  - role `SageMakerExecutionRole`, trusted entity SageMaker, two policies;
  - the ARN shape from README A:43, with its `123456789012` called "AWS's documentation
    placeholder".
- **V1 built**: the user's GREY key card stays on the laptop; the role's BLUE badge goes to the
  cloud. "Your laptop signs requests with the user's key. The endpoint you'll create acts as the
  role."
- ▶ A1·5 bucket `cheese-app-models-demo` "[REPLACE WITH YOUR UNIQUE BUCKET NAME]" (A:51): globally
  unique names (A:52, Troubleshooting 4). GOLD tag: storage bills while objects exist.
- The README's security warning (A:56-58) as a RED card: "never put keys in scripts or Git".
- ▶ A2·1 `aws configure` (`laptop/13`): the new `aws login` tip first (version drift, one
  clause), then the four prompts. Here Enter, Enter, `us-east-1`, `json`; "you paste your two
  keys". Extras `14` (only `config` exists) and `15` (`Unable to locate credentials`).
- ▶ A2·2 Option 2: the three exports verbatim (`laptop/16`); AWS's answer to the README's
  placeholder key: `InvalidClientTokenId`. **V1's Option 2 beat**: the exported cards fall off at
  the container wall. Erratum 3, kindly, with the fix: use Option 1, or add
  `-e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY` to `docker run`.

**S04 · The CLI container: two one-line fixes (~330) — `s04_build.py` · `TwoFixes`.** Tracker A2
3→5. No lecture_ref.
- ▶ A2·3 Edit `docker-shell.sh` (`laptop/17`: lines 5-9 with the placeholders). CODE
  (`docker-shell.sh: 16-27`): the two build lines (17 commented, 19 arm64), and the `docker run`
  with `-v ~/.aws`. Line 8's role in the copied file reads `YOUR_ACCOUNT_ID` (ASSETS.md: masked).
- ▶ A2·4 `chmod +x docker-shell.sh` (`laptop/18`, silent; extra `19`).
- ▶ A2·5 `sh docker-shell.sh` as written (`laptop/20`): the arm64 base is pulled, then
  `exec /bin/sh: exec format error`, `ERROR: failed to build`. **Fix 1**: the script's own line 17
  (`laptop/21`). On an Apple-silicon Mac the arm64 line works; on an Intel Mac or Windows it is
  emulated (slow); on a Linux PC without emulation it fails like this.
- **Fix 2**, the deeper one. PONDER 1 first (see Ponder questions). Then **V2**:
  - CODE(`Pipfile: 8-17`) with `sagemaker = "*"` at line 10, and `.gitignore:68` (the lock is
    ignored);
  - extra · check `laptop/22`: `sagemaker==3.13.1`, `torch==2.8.0`, fifteen `nvidia-*` wheels,
    "185 packages";
  - `laptop/23`: `sagemaker is a namespace package`, then the three import errors at
    `cli.py:21-23`.
  - Say plainly: the unpinned build ran 13 minutes in `pipenv lock` here and then ran out of disk.
    On your laptop it would finish, and then fail at the first import.
  - `laptop/24`: `-sagemaker = "*"` / `+sagemaker = "<3"`.
- ▶ `sh docker-shell.sh` again (`laptop/25`): `Building 400.6s`, `Container is running!!!`,
  `Testing AWS connectivity...`, then `Unable to locate credentials`, and the script goes on to
  `pipenv shell` anyway. Prompt `(app) app@<id>:/app$`. Extras: `Python 3.9.5`, sagemaker
  2.257.7, TF 2.18.0, the three env values echoed, and `python cli.py --help`.
- Erratum 7, kindly: the help says "GCS Bucket", "Vertex AI" and "Data Collector CLI". The AWS
  port kept the GCP wording; the commands are the AWS ones.
- Extra `laptop/26`: the image is 4.01 GB (TensorFlow is most of it).

**S05 · Where does preprocessing live? (~240) — `s05_signature.py` · `FrontDoor`.** Tracker stays
on A2 5/5 (concept beat). `lecture_ref(15, "13–14")` while V3 is on screen.
- Slide 13's contrast: in a notebook you resize and normalise cell by cell. A production endpoint
  should take the raw photo and do all of that itself, in one request.
- **V3 built.** The left pipe is Part A. CODE(`cli.py: 219-225`): the client opens the photo,
  converts it to RGB, resizes it to 224×224, divides by 255, and sends
  `{"instances": [arr.tolist()]}`. Preprocessing lives on **your** side. The extra `laptop/43`
  signature proves it: the front door takes `DT_FLOAT (-1, 224, 224, 3)`.
- "Client-side brittleness", said once: every client must repeat those gears exactly, and a phone
  app that forgets `÷ 255` gets confident nonsense. The lecture's second reason: one copy in the
  model is easier to roll back and version.
- The right pipe is the lecture's slide 14, and it exists in this course's AWS code, just not in
  Part A. It lives in the Part B trainer (CODE `task.py: 276-301`, shown dimmed, "we'll run this
  in part 2"). Three beats, as slide 14's three call-outs: define `preprocess_image`, wrap it in
  the `@tf.function` string-batch signature, save with `serving_default`.
- Misconception, kindly: README A:115 "Prepare the model in TensorFlow SavedModel format" is a
  *format* change, not the lecture's *signature* change.

**S06 · `--prepare`: a SavedModel in a tarball (~250) — `s06_prepare.py` · `PrepareArtifact`.**
Tracker A3 1. `lecture_ref(15, "12")` while V4 shows slide 12's steps 1–3.
- README A:110-117's four bullets on screen as a list; **V4** draws them.
- ▶ `python cli.py --prepare` (`laptop/27`): `Prepare model and save model to GCS Bucket`, then the
  traceback's first frame `cli.py:73 s3_client.create_bucket(...)` → `NoCredentialsError`, and
  `ls: cannot access 'artifacts'`. Erratum 4, kindly: the code creates the bucket **before** it
  downloads anything, a step the README's list doesn't mention. With your keys, it creates the
  bucket (or says it already exists) and goes on.
- "What it would do next", run for real with only S3 stubbed (extra · capture stub, `laptop/40`):
  - the release zip arrives, `Using Keras 3 export()`;
  - `Saved artifact at './artifacts/model-mobilenetv2_train_base_True.v1/1'`;
  - the upload line, then the stub's RED `NOT sent`.
- Extra `laptop/41` (the export's files) and `laptop/42` (`tar tzvf`: everything under `1/`).
  Concept: a SavedModel is a graph, weights and named entry points; TF Serving finds models by
  `<name>/<version>/`.
- Extra `laptop/44` (`git status`): the two edits, `artifacts/` ignored (`.gitignore:33`).
- GOLD tag: the tarball in S3.

**S07 · `--deploy`: Model, endpoint configuration, endpoint (~290) — `s07_deploy.py` ·
`ModelToEndpoint`.** Tracker A3 2. `lecture_ref(15, "11–12")` while V5 is built, then
`lecture_ref(15, "16–17")` for the comparison card only.
- **V5 built** from CODE(`cli.py: 151-174`):
  - `TensorFlowModel(model_data=…, role=…, framework_version="2.13")` fills the Model card's three
    slots;
  - the timestamped `endpoint_name` (`:163-167`);
  - `deploy(initial_instance_count=1, instance_type="ml.m5.xlarge")` (`:168-174`) builds the
    configuration and the endpoint in one call.
  - Bridge kindly: slide 12's "upload to Model Registry" → here a plain SageMaker **Model**. Both
    READMEs say "Model Registry", but no registry package is created (erratum 6).
- The prebuilt serving container: you never write an image URI. The SDK picks AWS's
  TensorFlow-Serving 2.13 image from `framework_version`. Version skew in one sentence: exported by
  TF 2.18, served by 2.13. The stand-in (`laptop/46`) shows that 2.13 loads it, with one ignored
  attribute warning (`debug_name`).
- ▶ `python cli.py --deploy` (`laptop/28`): `Deploying model to SageMaker endpoint...`, then the
  first frame `cli.py:168 tensorflow_model.deploy(` → `NoCredentialsError`. With keys: "5–10
  minutes" (A:127), the endpoint name printed, `endpoint_config.json` written. Command and
  narration only, no output panel.
- "Serverless" qualified: no server for **you** to manage. Still one `ml.m5.xlarge`, running and
  billing 24/7 with zero traffic; it does not scale to zero like L14's Cloud Run service. GOLD tag
  on the endpoint.
- Slides 16–17 in one two-column card: managed model serving (SageMaker endpoint / Vertex Online
  Prediction: deploy a model directly; versioning, A/B variants and monitoring are available) vs
  "run any container yourself" (Cloud Run, L14). The rule of thumb: a model endpoint to serve a
  trained model; a general container service when ML is one part of a bigger app. "Available, not
  used here": this deploy pins one instance, one variant, no monitoring.

**S08 · `--predict`: 150,528 numbers per photo (~280) — `s08_predict.py` · `AskTheEndpoint`.**
Tracker A3 3. `lecture_ref(15, "13")` while V3's left pipe is on screen.
- ▶ `python cli.py --predict` (`laptop/29`):
  - `Error: endpoint_config.json not found` (`:53`): no deploy, no file, so the fallback name;
  - `image_files: […]`;
  - five times `Error invoking endpoint: Unable to locate credentials` (`:62`).
  - Crop to the first image and the last line.
- **V3 left pipe** with numbers. PONDER 2 (see below), then the cube counts to 150,528. Python's
  `json` writes each one as text: a few megabytes per photo. The answer is
  `{"predictions": [[p0, p1, p2, p3]]}`; `np.argmax` and the hard-coded map
  (CODE `cli.py: 36-43`): 0 parmigiano, 1 gruyere, 2 brie, 3 gouda.
- What the endpoint would do, shown by the stand-in (extra · local stand-in, not SageMaker):
  - `laptop/45` (pull `tensorflow/serving:2.13.1`, "SageMaker's TF 2.13 serving image runs
    TensorFlow Serving too; this is the public one");
  - `laptop/46` (`Successfully loaded servable version {name: cheese version: 1}`,
    `"state": "AVAILABLE"`);
  - `laptop/47`: `cli.py`'s own `predict()` gets real answers with **four** numbers;
    `gruyere-1` → gruyere (0.70); **`parmigiano-1` → brie (0.977)**, a real mistake of the
    released model (its metrics file says 72 % accuracy; digest §1).
- The hook resolved: the README's three-number output (`recorded`) came from an older 3-class model
  with another label map. Erratum 5, kindly: "expect four numbers; index 0 is parmigiano."
- Extra `laptop/48`: the stand-in removed.

**S09 · `--delete`: turn off the meter (~200) — `s09_delete.py` · `TurnOffTheMeter`.** Tracker A4
1→3. `lecture_ref(15, "11, 41")` for the meter-and-DELETE beat only.
- Slide 11's alert returns as the GOLD meter. Slide 41 has only the word "DELETE!!" on a picture;
  our reading is a clean-up reminder. It is rendered as a GOLD word card, with no image.
- ▶ A4·1 CONSOLE (A:154-157): SageMaker › Endpoints › select › Delete.
- ▶ A4·2 the three AWS CLI lines (A:161-163). `laptop/31` is the first one exactly as written:
  `syntax error near unexpected token 'newline'`. Erratum 8, kindly: the `<…>` are placeholders,
  and the shell reads `<` as a redirection; type your own names without brackets. `laptop/32`
  (placeholder name): `Unable to locate credentials`. Order: endpoint, then configuration, then
  model.
- ▶ A4·3 `python cli.py --delete` (`laptop/30`): `NoCredentialsError` at its first SageMaker call.
  **V5's teardown beat**: the code deletes the endpoint named in `endpoint_config.json`, then the
  configuration and model "by name convention", then the S3 artifact. A second `--deploy` would
  have made a second, timestamped endpoint; PONDER 3 (below).
- "Confirm in the console" (A:176): `aws sagemaker list-endpoints` (named, not run).
- **End of part 1**: the meter stops on an empty slot. The parked question for part 2: "four
  commands by hand for one model. The Cheese App has four stages before it. Who runs all of them,
  in order, every time?"

### Part 2 · Automate the workflow (`ml-workflow-aws`)

**S10 · From four terminals to one workflow (~280) — `s10_workflow.py` · `FourTerminals`.** Tracker
B1 1→9. `lecture_ref(15, "19–22")` while V6 is on screen, then `lecture_ref(15, "24")` for the
one-line "managed: no cluster to run" beat.
- **V6**: slides 20–21, then slide 22's duty card with this repo's ticks. README B:3-7's four
  components appear on the tiles. Bridge kindly: Vertex AI Pipelines runs on Kubeflow Pipelines;
  this tutorial uses **SageMaker Pipelines**, the same idea of managed steps in a graph.
- ▶ B1·1 Clone (`laptop/50`; extras `51` `f165c6e`, `52` the tree: four folders under `src/`; only
  collector, training and workflow have a `Pipfile.lock`).
- ▶ B1·2–5 CONSOLE at speed:
  - services (B:20-24): SageMaker AI quick setup, Unified Studio domain, S3, ECR, Lambda;
  - bucket `cheese-app-ml-workflow-demo` [REPLACE …];
  - user `ml-workflow-user` with four policies;
  - access keys → Command Line Interface → **Download .csv**.
  - GOLD tag: quick setup and the Studio domain are account resources; check them at teardown.
- ▶ B1·6 Install CLI (B:51-53): brew / snap / curl. Ours: AWS CLI 2.34.63 (`laptop/01`).
- ▶ B1·7 `aws configure` with obviously fake placeholder keys (`laptop/55`; extra `56`, masked
  `****…_KEY`). "You paste the two values from the .csv."
- ▶ B1·8 Test Configuration: `laptop/53` (no keys: `Unable to locate credentials`) and `laptop/57`
  (fake keys: `InvalidClientTokenId`, `InvalidAccessKeyId`). "With your keys, these print your
  account and your buckets. Don't go on until they do: every later command depends on them."
- ▶ B1·9 two roles (B:71-81): `CheeseAppSageMakerExecutionRole` (three policies) and
  `CheeseAppLambdaExecutionRole`. **V1 reprise**: two badges now, and the code finds them **by
  name** (`model.py:19-48`), so spell them exactly.

**S11 · Collector and processor, by hand (~280) — `s11_collect.py` · `CollectAndClean`.** Tracker B2
1→3, then B3 1→5. `lecture_ref(15, "34–36")` while V7 is on screen, then `lecture_ref(15, "37")`
for the duty cards.
- ▶ B2·1 `cd src/data-collector`, `sh docker-shell.sh`. First without keys: `laptop/54`, the
  script's own check `AWS not configured. Run: aws configure`. Then with the placeholder keys
  (`laptop/60`): `Building 40.4s`, the root prompt.
  - Note: this script builds `linux/amd64`, the opposite of Part A, so Apple-silicon Macs emulate
    it.
  - On Linux, `sh` is dash: run `bash docker-shell.sh` (digest gotcha 2).
- **V7 built** from CODE(`docker-entrypoint.sh: 1-8`): no arguments → a shell (development mode,
  what you are in now); arguments → the command runs and the container exits (production mode).
  Slide 36's two modes, without the slide's gcloud login.
- ▶ B2·2 the search command verbatim (`laptop/60:21`): four `Searching for:` and
  `Done. Downloaded 10 images.` lines (photos and URLs not shown). Then
  `uploading file /persistent/dataset/raw.zip` → `S3UploadFailedError … (InvalidAccessKeyId)`
  (`:654`). ▶ B2·3 "check your S3 bucket" cannot pass here. Extra: 4 folders × 10, `raw.zip`
  14 MB.
- Extra `laptop/61`: `~/persistent-folder` appeared beside the clones, **owned by root**. "Remember
  this; it bites in the next container."
- ▶ B3·1 `cd ../data-processor`, `sh docker-shell.sh` as written: `exec format error` again
  (`laptop/65`), fixed by the same swap (`66`). Extra `laptop/67`: no lock file, so
  `pipenv lock` runs inside the build.
- ▶ B3·2 `python cli.py --clean` (`laptop/68`):
  - `Labels: ['parmigiano cheese', …]`;
  - difPy finds no duplicates among these 40 (`Search Results: {}`);
  - the `clean.zip` upload fails (`:107`).
- ▶ B3·4 `python cli.py --prepare`: `Full size of the dataset: 40`, `train_xy count: 32`,
  `validate_xy count: 8`, two real `.tfrecords` files; then the same upload error. ▶ B3·3/5 "check
  your bucket": the local folder instead (extra).
- Slide 37's duty cards: collector "download images, upload"; processor "verify, de-duplicate,
  **convert to TFRecords**". The AWS code really does all three. The four labels are the folder
  names, i.e. the query strings (`tfrecords.py:11-16`); a fifth query would raise `KeyError` (one
  clause; exercises).

**S12 · Train locally, sign the model (~260) — `s12_train.py` · `TrainLocally`.** Tracker B4 1→5.
`lecture_ref(15, "14")` while the signature code is on screen, then `lecture_ref(15, "37")` for the
training card.
- ▶ B4·1 `cd ../model-training`, `sh docker-shell.sh`: arm64 again (`laptop/70`) → swap (`71`).
  Extra `72`: this image *does* use its committed lock (`pipenv sync`, sagemaker 2.250.0), so no
  pin is needed here.
- ▶ B4·2 Local training verbatim (`laptop/73`):
  - `tensorflow version 2.20.0`, CPU only;
  - `TFRecords found at /persistent/dataset/tfrecords`: the processor's output, through the shared
    folder;
  - the model summary's **`dense_1 (Dense) (None, 3)`** (`:119`), in RED;
  - `8/8 … accuracy: 0.4062 … val_accuracy: 0.6250` (`:132`), "one epoch on 32 photos, not a
    result";
  - `Change model signature and save`;
  - **`PermissionError: [Errno 13] Permission denied: '/persistent/model'`** (`:146`).
- Erratum 10, kindly: `task.py:68 num_classes = 3` while the data has four labels; gouda (label 3)
  gets no target. Fix: `4`.
- Erratum 11, kindly: on Linux, Docker created `persistent-folder` as root (S11's note) and the
  container runs as `app`. Fix: create the folder yourself before the first `docker-shell.sh`, or
  `sudo chown -R $USER ../../../persistent-folder`. Docker Desktop on a Mac doesn't do this. The
  successful save was **not** captured, so CODE(`task.py: 303-322`) shows where it would write:
  `/persistent/model/1` locally, `$SM_MODEL_DIR/1` on SageMaker.
- **V3's right pipe, now real**: CODE(`task.py: 276-301`). This is where the lecture's slide 14
  lives in this tutorial. Erratum 9, kindly: README B:7 gives this to Model Deploy; the code does it
  at the end of training.
- ▶ B4·3 `sh package-trainer.sh` (`laptop/73`): the `tar` list, then `upload failed … trainer.tar.gz`.
  CODE(`package-trainer.sh: 1-4`).
- ▶ B4·4 `python cli.py --train`: `Train Model`, then `Unable to derive SageMaker execution role`
  (`:313`). CODE(`cli.py: 53-74`, two excerpts): `TensorFlow(…, framework_version="2.13", py_version="py310",
  instance_type="ml.m5.xlarge")`, `fit(…, wait=False)`. It returns at once; watch the console.
  GOLD tag: the training job.
- ▶ B4·5 CONSOLE (B:141-145): Training › Training jobs › `cheese-…`.

**S13 · Build and push: your own registry (~230) — `s13_push.py` · `PushToECR`.** Tracker B5 1→11.
`lecture_ref(15, "34")` for the "build and push to a registry the platform can pull" beat (slide
34's step 2; slide 39 links it).
- README B:153: "This step has already been done for this tutorial." Erratum 12, kindly:
  CODE(`workflow/cli.py: 34-36`) pulls `…dkr.ecr.<region>…/cheese-app-data-collector:latest` from
  **your** account's ECR. So you push both images yourself, once each.
- ▶ B5·1–3 Docker Hub (B:158-162): the three commands typed, with `<USER NAME>` and
  `<ACCESS TOKEN>` as written, **no output panel**. Two notes:
  - "a token on the command line lands in your shell history; prefer `--password-stdin`";
  - the M1 line builds `amd64/v2`, because SageMaker runs amd64.
- ▶ B5·4 the variable block verbatim (`laptop/80`):
  - `export: '[YOUR': not a valid identifier`;
  - the account lookup's `InvalidClientTokenId`;
  - **`ECR URI: .dkr.ecr.us-east-1.amazonaws.com/…`**.
  - Erratum 13, kindly: paste only the value `us-east-1`. A URI starting with a dot means your
    account lookup failed.
- ▶ B5·5–11: `docker pull` (command only); `create-repository … || true` (`laptop/81`: the error
  printed, exit **0**, so `|| true` hides it); `get-login-password | docker login`, `tag`, `push`,
  `list-images`, `echo` (commands only). "Run these on your laptop: the workflow container has no
  `docker` command" (`laptop/90:44`, shown in S14).
- GOLD tag: ECR storage.

**S14 · The workflow container and one processing job (~230) — `s14_shell.py` · `WorkflowShell`.**
Tracker B6 1→3. `lecture_ref(15, "32–33")` while the "remote control" picture is on screen, then
`lecture_ref(15, "36")` for V7's reprise.
- ▶ B6·1 `cd ../workflow`, `sh docker-shell.sh`. **V2 reprise** at speed:
  - `laptop/87`: the lock exists, but the Dockerfile copies only the Pipfile;
  - `laptop/89`: `Pipfile.lock not found, creating...`;
  - `laptop/85`/`86`: sagemaker 3.29.0, `No module named 'sagemaker.workflow'`;
  - the same fix (`laptop/88`).
- Then `laptop/90`: the banner, `aws sts get-caller-identity` → `InvalidClientTokenId`,
  `pipenv shell` anyway; extras: sagemaker 2.257.7, `aws-cli/2.39.4`, and
  `bash: docker: command not found`.
- Slide 32 redrawn: You (Python) → SDK → SageMaker. "The SDK is a remote control: your laptop
  asks, AWS's machines run."
- ▶ B6·2 `python cli.py --data_collector` (`laptop/90:45-98`): it stops at **`cli.py:32`**, a
  module-level `get_caller_identity`, before `data_collector()` even starts. "Every flag of this
  CLI needs a working key at import time." With keys: CODE(`cli.py: 52-80`):
  - `Processor(image_uri=DATA_COLLECTOR_IMAGE, instance_type="ml.t3.medium",
    entrypoint=["python3", "/app/cli.py"])`;
  - `arguments=[…]`, `wait=True`, `logs=True`.
- **V7 reprise**: SageMaker's entrypoint replaces the image's switch; production mode is SageMaker
  running your `cli.py` with arguments. The job's own credentials are the role's badge, not your
  key. GOLD tag: the Processing job.
- ▶ B6·3 CONSOLE (B:224): Processing › Processing jobs › `cheese-app-data-collector-…`.

**S15 · A pipeline drawn by references (~330) — `s15_pipeline.py` · `PropertyDAG`.** Tracker B7
1→3. `lecture_ref(15, "28–30")` while the graph is built, `lecture_ref(15, "33")` for upsert/start,
`lecture_ref(15, "37–38")` while slide 37's chain is compared.
- Bridge kindly: the slides write steps with the KFP DSL, wire them with `.output` and compile to
  YAML. This tutorial writes them with SageMaker's step classes, wires them with **property
  references**, and the SDK turns them into JSON. Slide 27's point still holds: it's plain Python.
- **V8 built** from CODE(`cli.py: 157-328`), in four ≤ 12-line excerpts:
  1. `CacheConfig` (165) and the `DataCollector` ProcessingStep (170-197);
  2. `step_collect.properties…S3Uri` (219-220) as the processor's input;
  3. `step_process.properties…["tfrecords"]` (266-267) into the TrainingStep, then
     `ModelArtifacts.S3ModelArtifacts` (277) into `TensorFlowModel` and `ModelStep` (283-288);
  4. the `LambdaStep` (297-315) with `ModelName` (309), and `Pipeline(steps=[…])`, `upsert`,
     `start` (320-328).
- PONDER 4 (see below), then the shuffle beat.
- Extra · built offline, not sent (`laptop/92`):
  - `Running within a PipelineSession, there will be No Wait, No Logs, and No Job being started.`;
  - the five step names (lines 59, 113, 186, 246, 260) and one `{"Get": …}` (143), with
    `<aws-dlc-account>` masking 191/251 if those lines show;
  - the stub's `NOT sent`.
  - "This JSON is what `upsert` sends: the AWS cousin of slide 29's YAML."
- Slide 37 compared, kindly: four steps on the slide, five here, because deploy is split into
  `CreateModel` (a Model, V5) and `DeployModel` (a Lambda that creates or updates the endpoint
  `cheese-app-endpoint`; CODE `deploy_model_lambda.py: 39-58`). The TFRecords card holds on AWS.
- **The shared drawer** beat (V8): the arrows say *when* and *what*, but the code moves the files
  by name through the bucket root. Say exactly this much: "the declared folders stay empty; how the
  training step finds `tfrecords.zip` on SageMaker we couldn't verify here." Never claim either way.
- ▶ B7·1 `python cli.py --pipeline` (`laptop/90:100-153`): `cli.py:32` again, the same error. With
  keys, `SageMaker Pipeline started: arn:…` (narrated, no panel). ▶ B7·2 CONSOLE (B:234):
  Unified Studio › Build › ML Pipelines, with the five-box graph redrawn from `92` (the README's
  screenshots are not used).
- Two facts for when it runs: 30-day caching skips unchanged steps (the collector won't scrape
  again), and a green `DeployModel` means the Lambda *asked*: wait for `InService` before
  predicting (digest gotcha 13). GOLD tags on each step's machine.
- ▶ B7·3 the four component flags (B:245-248): `laptop/90` shows all of them stopping at
  `cli.py:32`; one panel, three more prompts collapsed.

**S16 · Tear down, recap, test yourself (~240) — `s16_recap.py` · `TeardownRecap`.** No tracker.
`lecture_ref(15, "41")` with the DELETE card, then `lecture_ref(15, "40")` while V8's chain is the
recap.
- **Teardown card** (GOLD), each line spoken (see Costs and teardown).
- **Content recap** = slide 40's chain on V8 with this lecture's real objects under each link (SDK
  step classes → JSON definition → `upsert`/`start` → SageMaker Pipelines → jobs on managed
  machines; the DAG from references). Below it, Part A's mini-chain: `--prepare` (steps 1–3),
  `--deploy` (4–5), `--predict`, `--delete`.
- "Test yourself": the five recap questions, one at a time (answers in exercises.md).
- Pointer: study guide, exercises; the pipeline's trigger from GitHub Actions comes in L23 (GREY
  dashed).

## Word budget

| scene | words | scene | words |
| --- | --- | --- | --- |
| S01 Hook | 200 | S10 FourTerminals | 280 |
| S02 LectureMap | 250 | S11 CollectAndClean | 280 |
| S03 UserRoleBucket | 300 | S12 TrainLocally | 260 |
| S04 TwoFixes | 330 | S13 PushToECR | 230 |
| S05 FrontDoor | 240 | S14 WorkflowShell | 230 |
| S06 PrepareArtifact | 250 | S15 PropertyDAG | 330 |
| S07 ModelToEndpoint | 290 | S16 TeardownRecap | 240 |
| S08 AskTheEndpoint | 280 | | |
| S09 TurnOffTheMeter | 200 | | |
| **part 1** | **2,340** | **part 2** | **1,850** |

Total ≈ **4,190** words ≈ 24 min of narration. Typing, outputs, CONSOLE fills and four ponder
timers bring it to ~30–32 min. If the script runs long, trim S02's bridge table narration (the card
carries it) and S13's Docker Hub beat, never a README step.

## Ponder questions

Four timed ponders (Conny's 2026-10-21 density decision: 3–5 per video; REVIEW.md marks content
gate 3 met with it). Each is quiz-style, with a YELLOW timer, answerable from what was just shown;
the answer is said right after the timer.

| # | scene | question (as on the card) | answer |
| --- | --- | --- | --- |
| 1 | S04 (8 s) | "The Pipfile says `sagemaker = "*"`.\nThe code worked when it was written.\nNobody changed a line. Why does\n`cli.py` fail at import today?" | `"*"` is a constraint, not a pin (L1): the resolver takes the newest release that installs, today SDK **3** (3.13.1 on Python 3.9), a rewritten package without `sagemaker.tensorflow`, `serializers` or `get_execution_role`. No lock is used. Fix: `sagemaker = "<3"` |
| 2 | S08 (8 s) | "`--predict` resizes one photo to\n224 × 224 with 3 colour channels.\nHow many numbers travel to the\nendpoint for that one photo?" | 224·224·3 = **150,528** floats, written as JSON text (a few MB). A bytes-in signature (slide 13, the trainer) would send the JPEG itself |
| 3 | S09 (6 s) | "You ran `--deploy` twice,\nthen `--delete` once.\nHow many endpoints still bill?" | **One.** Each deploy makes a new timestamped endpoint (`cli.py:163-167`); `endpoint_config.json` names only the last, so `--delete` removes that one. Check with `aws sagemaker list-endpoints` |
| 4 | S15 (8 s) | "Reverse the list `steps=[…]`\nin `Pipeline(...)`.\nDoes the run order change?" | **No.** The order comes from the property references (each step's input names another step's output); the list is a set of steps, not a schedule |

## Recap questions (S16 "Test yourself"; answers in exercises.md)

1. Your laptop and the SageMaker endpoint both reach S3. Which identity does each use, and why do
   Option 2's exported keys never reach the Part A container?
2. Name the three things `--deploy` creates, which one is the address, and which one bills while
   nobody calls it.
3. Where does preprocessing live in Part A, and where in the Part B trainer? Give the lecture's two
   reasons to put it in the model.
4. Which lines make `ModelTraining` wait for `DataProcessor`? What would happen with a literal
   `s3://…/tfrecords` string instead?
5. Which two one-line fixes did today's tutorial need, and which one would an Apple-silicon Mac
   not need?

(Digest E2, E3, E5–E8, the `KeyError` on a fifth query, and the Lambda `python3.8` runtime default
go to exercises.md.)

## Errata and version drift to state (kindly, with the fix)

1. **`sagemaker = "*"` resolves to SDK 3 today** (`model-deployment-aws/Pipfile:10`,
   `src/workflow/Pipfile:9`; no lock enters either image). Imports fail. Fix: `sagemaker = "<3"`
   (or `==2.250.0`, matching the workflow's committed lock; or copy the lock and `pipenv sync`)
   (S04, S14).
2. **arm64 build lines** (`docker-shell.sh:19` in Part A, `:31` processor, `:32` training): `exec
   format error` on an Intel/AMD Linux machine without emulation, slow emulation on Intel Macs and
   Windows. Fix: the script's own plain line. Images pushed for SageMaker must be amd64 (S04, S11,
   S12, S13).
3. **Option 2's exports never reach the Part A container** (`docker-shell.sh:22-28`). Fix:
   Option 1, or add `-e` flags (S03).
4. **`--prepare` creates the bucket first** (`cli.py:70-82`), which the README's list doesn't
   mention; with a taken name it prints "already exists" and the upload then fails. Fix: a unique
   name (S06).
5. **The README's `--predict` output** (A:137-147) has three numbers and an old label map; today's
   model has four outputs and 0 = parmigiano (S08).
6. **"Model Registry"** in both READMEs: the code creates a plain SageMaker Model (S07).
7. **Leftover GCP words** in `--help` ("GCS Bucket", "Vertex AI", "Data Collector CLI"), and a
   `--test` flag that does nothing (S04).
8. **The AWS CLI delete lines** as written are a shell syntax error (`<…>` placeholders). Type your
   names (S09).
9. **README B:7** gives the signature update to Model Deploy; the trainer does it (`task.py:276-318`)
   (S12).
10. **`num_classes = 3`** (`task.py:68`) with four labels. Fix: `4` (S12).
11. **Root-owned `persistent-folder` on Linux** → `PermissionError` in the trainer. Fix: create it
    first or `chown`. Also on Linux, `sh` is dash: use `bash docker-shell.sh` (S11, S12).
12. **"Already done for this tutorial"** (B:153): the pipeline pulls from *your* ECR; push both
    images (S13).
13. **`export REGION=us-east-1 [YOUR DEVELOPMENT REGION]`** pasted whole → `not a valid
    identifier`; a failed account lookup gives a URI starting with a dot; `|| true` hides the
    `create-repository` error (S13).
14. **The workflow container mounts the Docker socket but has no `docker` CLI** (`laptop/90:44`):
    push from the laptop (S13, S14).
15. **Every workflow flag needs a valid key at import** (`workflow/cli.py:31-32`): test
    `aws sts get-caller-identity` first (S14, S15).
16. **Version drift, "at the time of recording"**: AWS CLI's `aws login` tip; the SDK v2 deprecation
    warning; boto3's end of Python 3.9 support (April 2026); TF 2.18 export vs TF Serving 2.13;
    sagemaker 3.x releases weekly; console labels from the READMEs (not seen live: "if a label
    differs, look for the same field").
17. Not in the video (exercises only): the Lambda's default `python3.8` runtime (digest gotcha 11,
    unverified without an account), the Lambda's substring name match (gotcha 10), the README's
    duplicated heading (B:88), `IAMFullAccess` breadth beyond S03's clause.

## Costs and teardown

The cloud steps **bill**. GOLD tags appear exactly where each starts; no prices are stated ("check
the pricing page").
- **S03 / S10**: S3 buckets (storage); SageMaker AI quick setup and the Unified Studio domain
  (account resources: check them at teardown).
- **S06**: `model.tar.gz` in S3.
- **S07**: the Part A endpoint, one `ml.m5.xlarge`, 24/7 while it exists, with zero traffic too.
- **S12**: the training job (`ml.m5.xlarge`, while it runs) and the trainer tarball in S3.
- **S13**: ECR storage for two images.
- **S14**: the Processing job (`ml.t3.medium`).
- **S15**: every pipeline step's machine; a new Lambda function per `--pipeline` run (random
  name); the endpoint `cheese-app-endpoint` (`ml.m5.large`) stays up after the run; each
  `--model_deploy` makes yet another endpoint.

Teardown checklist (S16), each line spoken in the same words:
1. `aws sagemaker list-endpoints`: delete **every** endpoint (Part A's timestamped ones,
   `cheese-app-endpoint`, `cheese-app-endpoint-…`), then their endpoint configurations and models.
2. Empty and delete both buckets (or at least the model and data objects).
3. Delete the two ECR repositories.
4. Delete the `sagemaker-deploy-model-lambda-…` functions and the `cheese-pipeline` pipeline.
5. Deactivate and delete the access keys; delete the users and roles you no longer need.
6. Check SageMaker AI's domain and the Unified Studio domain you created.

Nothing here is captured (no account). `laptop/30`-`32` show the delete commands' honest errors.

## README commands checklist (for the follow-along review)

Every README instruction, verbatim, in README order.

| README instruction | line | scene |
| --- | --- | --- |
| A · Clone or download | A:10 | S03 (`laptop/10`, `extra` spelling) |
| A · Services; IAM user + policies + access keys; SageMaker role; S3 bucket | A:12-52 | S03 (CONSOLE) |
| A · `aws configure` | A:67 | S03 (`laptop/13`) |
| A · three `export` lines | A:80-82 | S03 (`laptop/16`) |
| A · Edit `docker-shell.sh` (bucket, role, region) | A:87-90 | S04 (`laptop/17`) |
| A · `chmod +x docker-shell.sh` | A:98 | S04 (`laptop/18`) |
| A · `sh docker-shell.sh` | A:99 | S04 (`laptop/20`, `25`) |
| A · `python cli.py --prepare` | A:102, 113 | S06 (`laptop/27`; stand-in `40`) |
| A · `python cli.py --deploy` | A:103, 122 | S07 (`laptop/28`) |
| A · `python cli.py --predict` | A:104, 133 | S08 (`laptop/29`; `recorded` `expected/md-predict-readme.txt`; stand-in `47`) |
| A · `python cli.py --delete` | A:107, 169 | S09 (`laptop/30`) |
| A · Console: SageMaker › Endpoints › Delete | A:155-157 | S09 (CONSOLE) |
| A · `aws sagemaker delete-endpoint` / `-endpoint-config` / `delete-model` | A:161-163 | S09 (`laptop/31`, `32`) |
| B · Clone or download | B:16 | S10 (`laptop/50`) |
| B · Services; bucket; IAM user + four policies; access keys (.csv) | B:18-49 | S10 (CONSOLE) |
| B · Install AWS CLI | B:52-53 | S10 (`laptop/01`) |
| B · `aws configure` | B:57 | S10 (`laptop/55`) |
| B · `aws sts get-caller-identity` · `aws s3 ls` | B:67-68 | S10 (`laptop/53`, `57`) |
| B · two IAM roles | B:72-81 | S10 (CONSOLE) |
| B · `src/data-collector`: `sh docker-shell.sh` | B:94-95 | S11 (`laptop/54`, `60`) |
| B · `python cli.py --search --nums 10 --query …`; check bucket | B:99-100 | S11 (`laptop/60`) |
| B · `src/data-processor`: `sh docker-shell.sh` | B:112-113 | S11 (`laptop/65`, `68`) |
| B · `python cli.py --clean`; check; `python cli.py --prepare`; check | B:117-120 | S11 (`laptop/68`) |
| B · `src/model-training`: `sh docker-shell.sh` | B:130-131 | S12 (`laptop/70`, `73`) |
| B · `python -m package.trainer.task --epochs=1 --batch_size=4 --bucket_name=cheese-app-ml-workflow-demo` | B:136 | S12 (`laptop/73`) |
| B · `sh package-trainer.sh` · `python cli.py --train` | B:138-139 | S12 (`laptop/73`) |
| B · Console: Training › Training jobs | B:142-145 | S12 (CONSOLE) |
| B · `docker login -u <USER NAME> -p <ACCESS TOKEN>` · `docker build …` (both lines) · `docker push …` | B:159-162 | S13 (typed, no panel) |
| B · the five `export` lines | B:169-173 | S13 (`laptop/80`) |
| B · `docker pull <YOUR_DOCKER_HUB_USERNAME>/$REPO:$TAG` | B:179 | S13 (typed, no panel) |
| B · `aws ecr create-repository … \|\| true` | B:182 | S13 (`laptop/81`) |
| B · `aws ecr get-login-password … \| docker login …` · `docker tag` · `docker push` · `aws ecr list-images` | B:185-195 | S13 (typed, no panel) |
| B · `echo "ECR URI: $ECR_URI"` | B:198 | S13 (`laptop/80`) |
| B · `src/workflow`: `sh docker-shell.sh` | B:217-218 | S14 (`laptop/89`, `90`) |
| B · `python cli.py --data_collector`; Console: Processing jobs | B:223-224 | S14 (`laptop/90`; CONSOLE) |
| B · `python cli.py --pipeline`; Console: Unified Studio › ML Pipelines | B:233-234 | S15 (`laptop/90`; CONSOLE + `92` graph) |
| B · `--data_collector` · `--data_processor` · `--model_training` · `--model_deploy` | B:245-248 | S15 (`laptop/90`) |

## Notes for script and scene authors

- **Shared code** (`scenes/common.py`, started from L14's or L13's):
  - tracker factories `tracker_a1` … `tracker_a4`, `tracker_b1` … `tracker_b7` with the step
    lists above;
  - prompts `P_LAPTOP` (+ the repo and `src/<stage>` folders), `P_APP` and `P_ROOT` (from the
    captures);
  - tags `your_turn`, `extra_tag` (variants `extra · check`, `extra · capture stub`,
    `extra · local stand-in, not SageMaker`, `extra · built offline, not sent`),
    `illustration_tag`, `recorded_tag`, `cost_tag` (GOLD), `lecture_ref`;
  - `console_form(title, rows)` for the schematic AWS console (no AWS branding, no smile logo, no
    orange header bar);
  - `bridge_card(rows)` for the Vertex ↔ AWS legend (S02, reused small);
  - set-piece classes `IdentityBadges`, `StarVsPin`, `TwoPipes`, `ArtifactTrip`, `ThreeObjects`,
    `ManualToPipeline`, `CallableImage`, `ReferenceDAG`.
  - **Never reuse a scene class name** for a helper.
- **The sandbox framing is load-bearing.** Say it once in S02; after that, every AWS error is just
  the next line. Never imply a deploy, upload, job, push or pipeline run happened. Stand-in and
  stub panels are always tagged; the `recorded` panel names README A:137-147.
- **Commands with no output panel** (Docker Hub, the ECR push lines, a successful `--deploy`): type
  them verbatim and say what to look for ("the endpoint name", "an ARN"). Never invent a line.
- **CONSOLE panels**: field labels and values only from the READMEs (user names, policy names, role
  names, bucket names with their "[REPLACE …]", menu paths such as SageMaker AI › Processing ›
  Processing Jobs). No ARNs with ids, no account numbers, no prices.
- **Long lines**: `laptop/16:5`, `57`, `60:654`, `68:107` and `73:313` fold or crop from the
  meaningful phrase. `22` shows its header and the few named packages, `…`, then the count. The 9,000-line
  `89` shows only `Pipfile.lock not found, creating...` and the success lines.
- **Never read aloud**: container ids, timestamps, the endpoint's timestamp suffix, the scraped
  sites' names, `763104351884` (masked on screen anyway).
- **Personal data**: no instructor name anywhere (‹instructor› if ever needed). The README branch
  names `itamar/…` (ASSETS.md "Other refs") are **never shown**: they carry a person's name.
- **Lexicon heads-up** (script stage): SageMaker ("sage-maker"), boto3 ("bo-toe three"), S3
  ("S-three"), ECR, IAM (exists), ARN ("A-R-N"), STS, `ml.m5.xlarge` ("M-L dot M-five dot extra
  large"), `ml.t3.medium`, `ml.m5.large`, us-east-1 ("U-S east one"), TFRecords ("T-F records"),
  difPy ("diff-pie"), MobileNetV2, Keras, `upsert`, Lambda, Unified Studio, `--nums`, `arm64`,
  `amd64`, `pipenv` (exists), the cheese names (exist), `150,528` (say "a hundred fifty thousand
  five hundred twenty-eight"), `2.257.7`, `3.13.1`, `3.29.0` (key every spoken decimal version, as
  in L13). Check phonemes with `explainer/voice.py`.
- **Chinese glossary heads-up**: these stay English: SageMaker, S3, bucket, IAM, user, role, access
  key, ARN, policy, endpoint, endpoint configuration, Model (the SageMaker object), container,
  image, Docker, ECR, Lambda, pipeline, step, Processing job, Training job, property reference,
  DAG, cache, SavedModel, signature, `serving_default`, TFRecords, Pipfile, lock, pin, Vertex AI,
  Kubeflow, DSL, SDK. Reuse `../ac215-l15-exam/i18n/zh/glossary.yaml` where it agrees (DAG,
  pipeline, endpoint, registry).

## Things never to do on screen

Series rules:
- No slide images, QR codes or memes (slides 3, 11, 26, 31, 38, 41, 42); no AWS console
  screenshots, AWS or Google logos, or the READMEs' images (`serverless-model-deployment.png`,
  `ml-pipeline.png`, `sagemaker-pipeline-*.png`). Redraw the idea and cite the slide with a
  `lecture_ref` that lives only as long as its picture.
- No real person's name on screen or in subtitles: the instructor appears only in the
  `video.yaml` publish credit line; no branch names carrying a name; the prompt user is `student`.
- No hand-typed output: every terminal line comes from `assets/terminal/`.
- No command spelled differently from the README (the clones are marked `extra` for their
  spelling; the fixes are marked `extra`).
- No credentials: no key, token, account id or ARN that looks real. Placeholders only, as listed in
  Running example; `763104351884` masked as `<aws-dlc-account>`.

Lecture-specific:
- Don't call the SageMaker Model a "Model Registry entry" without the qualifier, and don't say
  creating it makes anything callable.
- Don't say "serverless = scale to zero" or "you pay only per request" for the endpoint.
- Don't say the list order of `steps=[…]` is the run order, or that a property is a string.
- Don't claim where the training step's data lands on SageMaker (open question), or that a green
  `DeployModel` means the endpoint answers.
- Don't present the TF Serving stand-in, the S3 stub or the offline pipeline JSON as AWS results.
- Don't show the scraped photos or their source URLs, or the eight sample photos.
- Don't suggest putting keys into an image, a script or `docker-shell.sh` (README A:56-58).
- Don't drop the `-p <ACCESS TOKEN>` warning beat or type a real-looking token.
- Don't show the course map's GCP repos as the tutorial; they are mentioned once, in S02's bridge.

## Left for exercises.md (not in the video)

- Digest E1–E8 (E2 Option 2 by hand; E3 request size; E4 literal string vs reference; E5 removing
  the declared folders; E6 one-hot of label 3 with 3 classes; E7 counting endpoints; E8 arm64
  emulation).
- A fifth `--query` → `KeyError` in `--prepare` (gotcha 7); the Bing scraper's endless loop (gotcha
  8); stale local data in `persistent-folder` winning over S3 (gotcha 6).
- The Lambda's `python3.8` default and its substring name check (gotchas 10–11); `fit(wait=False)`
  vs the workflow's waiting training (gotcha 15).
- The `{"b64": …}` request for a bytes-in signature (digest §3.3: no repo code exercises it).
