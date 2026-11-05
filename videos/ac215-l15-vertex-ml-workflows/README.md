# AC215 · Lecture 15 — ML workflows: deploy one model, then automate the pipeline on SageMaker

A follow-along walkthrough of the Lecture 15 tutorials of Harvard's **AC215 (MLOps & LLMOps, Fall
2026)**, *ML Workflows*, in their AWS version:

- **Part 1** · [dlops-io/model-deployment-aws](https://github.com/dlops-io/model-deployment-aws), branch
  `main` @ [`077f4db`](https://github.com/dlops-io/model-deployment-aws/tree/077f4dbc7b13ccef208c65a8e29489331261029e)
  (2025-08-25), its `README.md` top to bottom: *Setup Environments* (clone, AWS services, the IAM user and
  the SageMaker execution role, the S3 bucket), *Run Container* (configure AWS credentials, update the
  configuration, the quick-start commands), *Prepare Model for Deployment*, *Upload & Deploy Model to
  SageMaker*, *Test Predictions* and *Clean Up Resources*.
- **Part 2** · [dlops-io/ml-workflow-aws](https://github.com/dlops-io/ml-workflow-aws), branch `main` @
  [`f165c6e`](https://github.com/dlops-io/ml-workflow-aws/tree/f165c6e17895d3d6c33a150d349f4b2649c807db)
  (2025-08-19), its `README.md` top to bottom: *Setup Environments*, *Run Data Collector Container & Test
  CLI*, *Run Data Processor Container & Test CLI*, *Run Model Training Container & Test CLI*, *Build & Push
  Images*, *Automate Running Data Collector Container* and *Cheese App: SageMaker Pipelines*.

**Which tutorials.** The lecture slides speak Vertex AI, and the course map pins the Google Cloud repos
(`dlops-io/model-deployment`, `dlops-io/ml-workflow`). This series follows the course's AWS version of both
tutorials instead; the slides decide the concepts, the AWS READMEs and the captures decide what the video
shows, and the video maps each Vertex AI word onto its AWS counterpart as it comes up (GCS bucket → S3,
Model Registry → a SageMaker Model, endpoint → endpoint configuration + endpoint, Vertex AI Pipelines →
SageMaker Pipelines, Artifact Registry → ECR, service account → an IAM user's key on the laptop and a role in
the cloud). Both pins were re-checked with `git ls-remote` on 2026-11-05 (`HEAD` = `main`); details in
[`ASSETS.md`](ASSETS.md), "Which commits". The concept-first exam edition of this lecture is
[`../ac215-l15-exam/`](../ac215-l15-exam/).

A model answers *brie*, twice, from the same predict code, once with three numbers and once with four: what
is behind an endpoint? Part 1 deploys one model by hand: a SavedModel in a tarball in S3, a SageMaker Model, an
endpoint configuration and an endpoint on one machine that bills around the clock, the 150,528 numbers each
photo becomes, and the clean-up that misses an endpoint. Part 2 turns the Cheese App's four stages, run by four
people at four terminals, into one SageMaker Pipeline: the collector, processor and trainer containers by hand,
the step images in your own ECR, one Processing job, and a five-step pipeline whose edges are drawn by property
references.

Watch it with both READMEs open, both clones, Docker running, the AWS CLI v2 installed and your own AWS
account with billing. **This lecture creates billable resources**: S3 buckets, endpoints (`ml.m5.xlarge`,
`ml.m5.large`, around the clock while they exist), Processing and Training jobs, ECR storage, Lambda
functions, the SageMaker AI and Unified Studio domains; a GOLD tag marks each place (no prices: check the
pricing pages), and the video ends with the clean-up checklist. The tracker top left shows the README step;
pause at every `▶ your turn` to run the command; a gray `extra` tag marks a command that isn't in the README,
and a gray "Lecture 15 · slides …" tag top right points to the lecture slides the scene stands on, only while
their picture is on screen.

The terminal sessions were recorded on 2026-11-05 in a fresh, empty Docker 29.8.2 engine standing in for your
laptop, with AWS CLI 2.34.63; inside the tutorial images: Python 3.9.5 with TensorFlow 2.18 and SageMaker SDK
2.257.7 (Part 1), Python 3.11.18 with TensorFlow 2.13/2.20 and SageMaker SDK 2.250.0/2.257.7 (Part 2). That
machine had **no AWS account, no access key and no SageMaker**. Everything that runs on your laptop ran live:
both clones, `aws configure`, every `sh docker-shell.sh` (as written and after the fixes), all four tutorial
images, and inside them every README command; the collector really scraped 40 cheese images, the processor
really wrote TFRecords, the trainer really trained one epoch. Every AWS call stops at its honest first error
(`Unable to locate credentials`, or AWS rejecting obviously fake placeholder keys). Console steps are
schematic drawings tagged `illustration`; the one cloud output the README documents (`--predict`) is quoted and
tagged `recorded`; two stand-ins show what the cloud would do without pretending to be it, each tagged: the
exported model served by the public TensorFlow Serving 2.13 image, and the pipeline's JSON definition built
offline by the SDK. Buckets, roles and keys on screen are placeholders. Series format:
[`docs/AC215_SERIES.md`](../../docs/AC215_SERIES.md). Study guide with every command:
[MLOps_Learning · guides/L15-vertex-ml-workflows.md](https://github.com/JunyiZhou-Conny/MLOps_Learning/blob/main/guides/L15-vertex-ml-workflows.md).

English narration; Chinese and bilingual subtitles (中文字幕说明见 [`i18n/zh/README.md`](i18n/zh/README.md)).

| file | what it is |
| --- | --- |
| `output/ac215-l15-vertex-ml-workflows.zh-en.mp4` | **the copy to watch**: 1080p60, English narration, bilingual subtitles (Chinese above, English below) burned in, DURATION_FULL. Published as a GitHub release asset: no MP4 is kept in Git ([`docs/PUBLISHING.md`](../../docs/PUBLISHING.md)) |
| `output/ac215-l15-vertex-ml-workflows.mp4` | the same video without burned-in subtitles; load any `.srt` below in your player. Release asset, not in Git: rebuild it with `--no-render` (see Rebuild) |
| `output/ac215-l15-vertex-ml-workflows_part1.mp4` | part 1, DURATION_P1: deploy one model — a SageMaker model, an endpoint and the request (S01–S09). Release asset, not in Git |
| `output/ac215-l15-vertex-ml-workflows_part2.mp4` | part 2, DURATION_P2: automate the workflow — four containers, ECR and a SageMaker Pipeline (S10–S16). Release asset, not in Git |
| `output/ac215-l15-vertex-ml-workflows.srt` | English subtitles (each part has its own `.srt`, `.zh.srt`, `.zh-en.srt` / `.ass`) |
| `output/ac215-l15-vertex-ml-workflows.zh.srt` | Chinese subtitles (on the English timing) |
| `output/ac215-l15-vertex-ml-workflows.zh-en.srt` / `.zh-en.ass` | bilingual subtitles |
| `output/chapters.txt`, `chapters_part1.txt`, `chapters_part2.txt` | chapter timestamps |
| `output/transcript.md` | the full narration by chapter |
| `exercises.md` | do these after watching: the five test-yourself questions, hands-on predict-then-run tasks, debugging and think questions, with answers; what was re-run to check them is in [`assets/exercise-checks/`](assets/exercise-checks/README.md) |
| `digest.md` | the tutorial digest, rebuilt against the two AWS repos: every step, a code tour with `path:line`, gotchas, errata |
| `SLIDES.md` | the lecture behind the tutorial: a digest of the slide deck in our own words, with slide numbers, and which scene stands on which slides |
| `assets/terminal/` | the **real** terminal sessions every terminal panel prints from (2026-11-05, a fresh Docker engine, no AWS account); provenance in [`ASSETS.md`](ASSETS.md) |
| `assets/source/` | the tutorial files the code panels quote, unchanged at `077f4db` and `f165c6e` (one real-looking role ARN masked, see ASSETS.md) |
| `BRIEF.md`, `script.md`, `scenes/` | the design, the narration (SAY) + visual plan (SHOW), and the Manim source |
| `i18n/zh/` | the Chinese subtitle text: glossary and sentence-aligned translation |

Git keeps the subtitles, the chapter files and the transcript; the MP4s (the burned-in copy, the clean video
and the two part cuts) are release assets.

## Chapters

CHAPTERS

## What you'll learn

Four *pause and ponder* moments ask you to predict before the video shows you: why `cli.py` fails at import
today although nobody changed a line; how many numbers travel to the endpoint for one photo; how many
endpoints still bill after two deploys and one delete; and whether reversing the pipeline's list of steps
changes the run order. Five test-yourself questions close the video (answers in `exercises.md`).

**Part 1 · deploy one model: a SageMaker model, an endpoint and the request (model-deployment-aws)**

1. **Three numbers or four?** — the README's predict output and this recording's local stand-in both say
   brie, one with three numbers, one with four; the three pieces behind an endpoint (an artifact, a
   container, a machine with a meter that runs with no requests); part 2's four stages as one pipeline; what
   you need to follow along; the tracker and `▶ your turn`.
2. **Where we are, in AWS words** — the course project in its prototype phase, model deploy the open tile;
   from Lecture 14's Cloud Run to a container that serves a trained model; the lecture's console map (online
   prediction and pipelines today); why we follow the AWS tutorials, and the first three words of the bridge
   (bucket, key and role, endpoint); what this recording, with no AWS account, can and cannot show.
3. **A user, a role and a bucket** — the clone and the commit we follow; the console steps: three services,
   the IAM user `model-deployment` with three policies (the third broader than the code needs), access keys,
   the `SageMakerExecutionRole` and its ARN, a bucket with a name of your own; why two identities (your
   laptop signs with the user's key, the endpoint acts as the role); `aws configure` and the who-am-I check;
   Option 2's exports, which never reach the container.
4. **The CLI container: two one-line fixes** — edit `docker-shell.sh`, `chmod`; `sh docker-shell.sh` stops
   at `exec format error` (the arm64 line for Apple-silicon Macs; fix 1, the script's own plain build line);
   `sagemaker = "*"` with no lock resolves SDK 3, whose rewritten package lacks the modules `cli.py` imports
   (fix 2, `sagemaker = "<3"`: a constraint is not a pin); the build in about 7 minutes; Python 3.9, SDK
   version 2 and TensorFlow 2.18 inside; `--help`'s leftover GCS and Vertex AI words.
5. **Where does preprocessing live?** — the lecture's notebook vs a production endpoint; in this tutorial the
   client resizes, divides by 255 and sends JSON; the model's front door (its signature) takes floats and
   gives four numbers; client-side brittleness, and one copy in the model to version and roll back; the
   part 2 trainer's bytes-in `serving_default`; the README's "SavedModel format" is a format change, not the
   signature change.
6. **`--prepare`: a SavedModel in a tarball** — the README's four steps and slide 12's steps 1 and 3; ours
   stops at once, at the bucket creation the README's list doesn't mention; a capture stub shows the rest
   (download, export, the upload never sent); a SavedModel is a folder (graph, entry points, weights) inside
   a version folder `1/` that TensorFlow Serving needs; your two edits in `git status`; the tarball's storage
   cost.
7. **`--deploy`: model, endpoint configuration, endpoint** — a TensorFlow model described in Python (the
   tarball, the serving container, the role); "Model Registry" in the lecture and the READMEs vs the plain
   SageMaker Model the code creates; the SDK picks the TensorFlow Serving 2.13 image for a model exported by
   2.18; one `ml.m5.xlarge`, a timestamped name, and the three objects one call creates; "serverless" means no
   server to manage, not scale to zero; the lecture's endpoint vs container-service comparison and its rule of
   thumb.
8. **`--predict`: 150,528 numbers per photo** — the fallback endpoint name and five honest failures; 224 × 224
   × 3 floats as JSON text, a few megabytes per photo; argmax and the four-label map; a local TensorFlow
   Serving stand-in (not SageMaker) loads the export and answers brie and gruyere, and parmigiano as brie at
   98 percent, a real mistake of the released model; the opening puzzle solved: the README's output came from
   an older three-class model.
9. **`--delete`: turn off the meter** — the lecture's warning; three ways to clean up: the console, three AWS
   CLI commands (typed with your own names, not angle brackets), `python cli.py --delete`; deploy twice,
   delete once, and one endpoint keeps billing; `aws sagemaker list-endpoints`; four commands by hand for
   one model, and the question that opens part 2.

**Part 2 · automate the workflow: four containers, ECR and a SageMaker Pipeline (ml-workflow-aws)**

10. **From four terminals to one workflow** — the lecture's four people at four CLIs; an orchestrator:
    Vertex AI Pipelines on Kubeflow in the slides, SageMaker Pipelines here; what workflow management does
    (order, repeatability, a machine per step, monitoring; scheduling waits for Lecture 23); the clone and its
    four folders; the console set-up (quick setup, a Unified Studio domain, bucket, `ml-workflow-user`, an
    access key's `.csv`); `aws configure` with obviously fake keys and AWS's real rejections; the two roles,
    found by exact name.
11. **Collector and processor, by hand** — put your bucket in all four scripts; the script's own key check;
    a root shell; on Ubuntu or Debian `sh` is dash, so run `bash docker-shell.sh`; the callable container
    (no arguments: a shell; arguments: run and exit); the search scrapes 40 images and the upload fails on
    the fake key; a root-owned `persistent-folder` on Linux; the processor's arm64 line again; `--clean` finds
    no duplicates; `--prepare` splits 32/8 into two real TFRecord files; the labels are your query strings.
12. **Train locally, sign the model** — the trainer installs from its committed lock (no pin needed); local
    training on the CPU finds the TFRecords through the shared folder, with a last layer of three outputs;
    `PermissionError` on `/persistent/model`, and two fixes (`num_classes = 4`; create or `chown` the folder);
    where the model would be saved, locally and in a job; the lecture's signature change sits in the trainer,
    not in model deploy as README B says; `package-trainer.sh`; `--train` stops at the role lookup; Training
    jobs in the console.
13. **Build and push: your own registry** — "already done for this tutorial", but the workflow pulls from your
    own ECR; the lecture's step 2 for your containers; the Docker Hub route and the amd64 line; the five
    variables, the pasted bracket note and a URI that starts with a dot; `|| true` hides an error; log in,
    tag (a second name for the same image), push, list; both images, from your laptop.
14. **The workflow container and one processing job** — its committed lock never enters the image, so make
    the `<3` fix first; the banner, SDK version 2, and no `docker` inside; the SDK as your remote control;
    `--data_collector` stops at a module-level account lookup; with keys, a Processor from your ECR image on
    `ml.t3.medium`; production mode of the callable container, acting as the role, not with your key.
15. **A pipeline drawn by references** — the slides' KFP DSL and YAML vs SageMaker step classes and JSON;
    30-day caching; five steps whose edges come from property references, not a string and not the list
    order; the offline JSON definition; create model plus a Lambda that creates or updates the endpoint; files
    also travel by name through the bucket (and how training finds its data was not verified); `--pipeline`,
    the Lambda runtime note, the Unified Studio graph (illustration); a green `DeployModel` is not an
    endpoint in service; the four component flags, and the extra endpoint `--model_deploy` makes.
16. **Tear down, recap, test yourself** — the clean-up checklist (every endpoint, then configurations and
    models; both buckets; the ECR repositories, the deploy Lambdas and the pipeline; the access keys, users
    and roles; both domains); the lecture's recipe-to-factory picture; today's five pictures and part 1 in
    four commands; five test-yourself questions; next, Lecture 23 triggers the pipeline from GitHub.

The READMEs' and the code's small slips are pointed out kindly, with the fix: `sagemaker = "*"` resolves SDK
3 today and the imports fail (pin `"<3"`; the workflow image ignores its own lock); the arm64 build lines fail
on an Intel/AMD Linux machine (use each script's plain line; push amd64 images for SageMaker); Option 2's
exported keys never reach the Part A container (use `aws configure`, or add `-e` flags); `--prepare` creates the
bucket before anything else, a step the README's list doesn't mention; the README's predict output comes from
an older three-class model (expect four numbers, index 0 = parmigiano); "Model Registry" in both READMEs is a
plain SageMaker Model in the code; `--help` still speaks GCS and Vertex AI, and `--test` does nothing; the AWS
CLI delete lines need your own names, not angle brackets; all four part 2 scripts carry the README's bucket
name; on Ubuntu or Debian `sh` skips the scripts' key check (run `bash`); README B gives the signature change to
model deploy, but the trainer does it; `num_classes = 3` with four labels (use 4); Docker creates
`persistent-folder` as root on Linux (create it yourself, or `chown` it); "already done for this tutorial" still
means pushing both images to your own ECR; the pasted `[YOUR DEVELOPMENT REGION]` note and a failed account
lookup (a URI that starts with a dot); the workflow container has no `docker` (push from your laptop); every
workflow flag needs a working key at import; and the deploy Lambda's default runtime may need
`runtime="python3.12"`.

## Rebuild

```bash
python -m explainer.build videos/ac215-l15-vertex-ml-workflows -q l                          # fast draft
python -m explainer.build videos/ac215-l15-vertex-ml-workflows --render-only --jobs 3        # 1080p60 scene renders
python -m explainer.build videos/ac215-l15-vertex-ml-workflows --no-render --crf 27 --burn   # stitch: video, parts, subtitles, burned-in copy, chapters, transcript
python -m explainer.build videos/ac215-l15-vertex-ml-workflows --subs-only                   # rewrite subtitles only
python -m explainer.i18n check videos/ac215-l15-vertex-ml-workflows --lang zh                # Chinese text aligned with the English
```

No MP4 is in Git (the burned-in copy is a release asset): after a fresh clone, render the scenes once, then the
`--no-render` line rebuilds the clean video, the two part cuts and the burned-in copy from the scene renders.
The captures can be re-run with `assets/terminal/capture.sh` (see [`ASSETS.md`](ASSETS.md), "How to re-run");
the exercise checks with the scripts in [`assets/exercise-checks/logs/`](assets/exercise-checks/README.md).

Narration: Kokoro (`af_heart`, speed 0.9), generated locally.

*Course materials belong to the AC215 teaching staff (Harvard IACS); the model-deployment-aws and
ml-workflow-aws tutorials are used for study with the instructor's permission and quoted at their pinned
commits. The lecture's slides are redrawn in our own pictures, never shown, and the READMEs' images are not
shown. The AWS console is a schematic drawing (tagged `illustration`), never a screenshot, with no AWS logo;
the recording used no AWS account or credentials, and every bucket, role, key and account id on screen is a
placeholder.*
