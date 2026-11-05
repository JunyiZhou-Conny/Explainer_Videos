# AC215 · Lecture 15 — ML workflows: deploy one model, then let a pipeline run them all — narration script & visual plan (v2, after the four reviews: build/review_merge_log.md)

Audience: an AC215 student who has done L1–L14: Docker images, containers and `docker-shell.sh`
scripts with bind mounts (L2–L4), pipenv and lockfiles (L1 "the older way", L3), the cheese
collector, processor and TFRecords (L6–L9), the trainer package and a managed training job (L13),
Cloud Run (L14). They have seen Lecture 15, which speaks Vertex AI. **This is the series' first AWS
lecture**: new to them are IAM users, access keys and roles, S3, SageMaker models, endpoint
configurations and endpoints, ECR, Lambda and SageMaker Pipelines. They watch with clones of
`dlops-io/model-deployment-aws` and `dlops-io/ml-workflow-aws` open, Docker running, the AWS CLI v2
installed and their own AWS account with billing, pausing to run each step. **The cloud steps bill**
(GOLD tags where each starts, no amounts; the clean-up checklist at the end).

Goal (BRIEF "Audience and goal"): after the video they can map the lecture's Vertex AI words onto
AWS (GCS bucket → S3; Model Registry → a SageMaker Model; endpoint → endpoint configuration +
endpoint; Vertex AI Pipelines → SageMaker Pipelines; KFP DSL compiled to YAML → SDK step classes
upserted as JSON; Artifact Registry → ECR; service account → an IAM user's key on the laptop and a
role in the cloud); set up the IAM user, the execution role and the bucket, and say which identity
the laptop uses and which the cloud uses, and why Option 2's exports never reach the Part A
container; build both CLI containers today with the two one-line fixes (the plain build line on an
Intel/AMD machine, `sagemaker = "<3"`: a constraint is not a pin); explain what `--prepare` makes (a
SavedModel in a version folder `1/`, in `model.tar.gz`, in S3), read its signature (floats in, four
numbers out) and say where preprocessing sits in Part A (client) and in the Part B trainer (inside
the model, slide 14); explain what `--deploy` creates (a Model, an endpoint configuration, an
endpoint on one `ml.m5.xlarge`), what `--predict` sends (150,528 floats per photo) and gets back,
why "serverless" here means no server to manage (not scale to zero), and what `--delete` misses;
run the collector, processor and trainer containers by hand and know the query-string labels, the
`num_classes = 3` slip and the root-owned `persistent-folder` on Linux; push the step images to their
own ECR and spot the pasted-bracket trap and the URI that starts with a dot; read `pipeline()`: five
typed steps, edges from **property references** (not list order), 30-day caching, a Lambda that
deploys; know that the laptop defines the pipeline, creates the deploy Lambda, upserts and starts, that
data also travels by file name
through the bucket, and that a green `DeployModel` does not mean `InService`; and clean everything up.

Sources of truth: `BRIEF.md` (design, binding), `digest.md` (rebuilt against the two AWS repos),
`SLIDES.md` (lecture-slide digest, binding next to the digest: docs/AC215_SERIES.md rule 9; the
BRIEF's scene plan supersedes SLIDES.md §1's GCP scene map), `assets/` (see `ASSETS.md`). Where the
digest or the slides and the captures disagree, the captures win, and the video says so kindly.
**README A = `model-deployment-aws/README.md` @ `077f4db`; README B = `ml-workflow-aws/README.md` @
`f165c6e`** (both `main`, re-checked with `git ls-remote` on 2026-11-05, ASSETS.md "Which commits").
The lecture's GCP repos appear only in S02's bridge sentence. Nothing in a terminal panel is typed
by hand: every output line below names its capture file and line numbers.

Conventions
- `SAY:` lines are spoken verbatim by the TTS voice (one `voiceover` block each, 1–3 sentences, at
  most about 60 words) and become the subtitles. Plain spoken English: no backticks, no markdown,
  no raw symbols (`/`, `=`, `%`, `<`, `*`, `$`, `→`); commands, flags and paths are on screen and
  said in words: "python cli.py dash dash prepare" (the README command, said in full at its tracker
  step; afterwards "prepare", "the deploy step"), "sh docker-shell.sh", "star", "less than 3", "or
  true", "slash persistent slash model". File names with lexicon entries are written as files
  (`cli.py`, `docker-shell.sh`, `Pipfile.lock`); others are said in words ("model dot tar dot G Z",
  "endpoint config dot JSON", "raw dot zip", "saved model dot P B"). Spelled letters: "A R N", "A R
  M 64", "A M D 64", "C S V", "R G B", "D S L", "M L M5 extra large", "M L T3 medium" (subtitle
  `en_display` restores `ARN`, `arm64`, `amd64`, `.csv`, `RGB`, `DSL`, `ml.m5.xlarge`,
  `ml.t3.medium`). Numbers are digits; 150,528 is said in words ("one hundred fifty thousand, five
  hundred twenty-eight"); never a "!" after a digit. Tool and package versions are said only as a
  major version ("SageMaker SDK version 3", "TensorFlow 2.18", "Serving 2.13") and sit on screen
  with `at the time of recording`; no patch version is spoken. No prices anywhere.
- Every spoken sentence starts with a capital letter or a digit (`explainer.voice.split_sentences`
  splits only there; the same split drives TTS gaps, subtitle cues and the one-to-one Chinese
  alignment). No sentence opens with a lower-case command, tool or file name ("The script
  docker-shell.sh …", "Its cli.py …"). No `'s` on a word with a lexicon entry or candidate
  (SageMaker, AWS, README, S3, ECR, Kubeflow, Lambda: "the AWS serving image", never "AWS's"). No bare
  "a" right before a lexicon entry or candidate ("one SageMaker model", "an S3 bucket", "the ECR
  registry"). No homographs: never "read", "live", "lives", "close", "lead", "tear" (so "clean up"),
  "minute", "content", "record", "object" (an S3 file is "a file"), "refuse", "invalid" (AWS
  "rejects" a key). American spelling on screen and in SAY ("gray", "color"; the colour constants
  stay GREY). The main clause comes first so the Chinese subtitles keep English clause order.
- `SHOW:` lines describe what is on screen during that `SAY:` line, and what moves. Something moves
  about every 4 s except under a ponder timer; at most 3 visual groups at once; every scene ends on
  an empty frame.
- `PONDER(n s, "question")`: after that SAY block, `pause_and_ponder(self, "question", seconds=n)`
  (silent YELLOW timer; the card is removed at the start of the next block). Four in the video, the
  BRIEF's table, Conny's 2026-10-21 density decision: P1 S04 (8 s), P2 S08 (8 s), P3 S09 (6 s), P4
  S15 (8 s). The SAY before each card speaks the question; the answer is the next SAY. Nothing on
  screen during the timer shows the answer. Card texts are the BRIEF's (`\n` = line break), without
  backticks (`pause_and_ponder` renders plain `Text`, so a backtick would print) and with American
  spelling.
- `TERM(laptop/NN: lines)`: a terminal beat. `laptop/NN` is the one file
  `assets/terminal/laptop/NN-*.txt`. The scene types the command written just before it in the SHOW
  line (in backticks, exactly as the README spells it; extras exactly as the capture's line 1
  spells them), then prints the listed **file** lines. The `$ …` command lines are typed, never
  printed; a multi-line command occupies lines 1–k (`laptop/16:1–4`, `53:1–2`, `57:1–2`,
  `80:1–6`, `81:1–2`); `[exit N]` is never printed. Inside the line list: `…` = print one `…`
  line; `wrap` = fold long lines; `cut` = cut the line at the frame's right edge (no fold);
  `from "…"` = print that long line from the quoted phrase on, after a `…`; `to "…"` = print it up
  to and including the quoted phrase; `squeeze` = a table re-aligned with two-space gutters, the
  ID and empty columns dropped; `→ (no output)` = the prompt simply returns. Rich traceback lines
  (`│ … │`, `❱`) are printed without the box borders (`│`, `╭`, `╰`), as plain text. Blank output
  lines are dropped.
- **Typed lines inside a container.** The `istep` captures (`25`, `27`–`30`, `60`, `68`, `73`, `90`)
  hold a whole session: `sh docker-shell.sh`, the build, the entrypoint banner, then each line typed
  at the container prompt (`(app) app@6fd3f31d3da7:/app$ python --version; …`). The scene shows the
  prompt as **`(app) app@<id>:/app$`** or **`root@<id>:/app#`** (container ids are never shown or
  said) and types the rest of that line; the line numbers in a TERM after such a typed line are its
  output lines. `27`–`30` each opened a fresh container from the same image: the scenes stay in one
  container from S04's prompt to S09 and never re-type `sh docker-shell.sh` there; a GREY chip at
  S06's first prompt says "our capture: a fresh container per step · stay in yours". The
  `source …/activate` line pipenv prints and the `exit` lines are never shown.
- **No output panel**: a command whose success only the cloud can show (Docker Hub login, build and
  push; the ECR pull, login, tag, push and list; a successful deploy, training job or pipeline run)
  is typed verbatim and gets a GREY chip "needs your account · no output shown"; the SAY says what to
  look for. Never an invented line.
- `CODE(path: a–b)`: `code_panel(...)` quoting `assets/source/<repo>/path` from line a to b with the
  real line numbers, header `path · lines a–b`; at most 12 lines on screen. Paths: Part A files are
  under `model-deployment-aws/`, Part B under `ml-workflow-aws/` (`src/workflow/cli.py` etc.;
  the header shows the repo-relative path). Two ranges separated by `+` are two stacked panels. A
  "README card" is a GREY quote of README text, header `README.md · lines a–b` (A or B named in a
  small chip; markdown stripped; no images).
- `CONSOLE(title, README lines)`: a schematic AWS console form drawn with `console_form(title, rows)`
  (no AWS branding, no smile logo, no orange header bar, never a screenshot), tag `illustration`,
  with field labels and values only from the README lines named; buttons as the README writes them
  (**Create role**, **Create user**, **Create access key**, **Download .csv file**, **Delete**). No
  ARNs with ids, no account numbers, no prices. A small GREY chip on the first form: "labels from the
  README · if yours differ, look for the same field".
- `RECORDED(expected/md-predict-readme.txt: lines)`: a GREY-outlined panel quoting those lines (the
  three `#` provenance lines never shown), tag `recorded · README A:137–147`.
- `TRACKER Xk n`: the `ReadmeTracker`, top-left in every walkthrough scene, for README section `Xk`
  at step n. `TRACKER Xk n · extra` = same step, caption " · extra" while a command the README does
  not have is on screen; variants `· extra · check` (`22`, `23`, `85`, `86`, `87`), `· extra ·
  capture stub` (`40`), `· extra · local stand-in, not SageMaker` (`45`–`48`), `· extra · built
  offline, not sent` (`92`). The trackers (BRIEF table; titles are the README's headings, shortened;
  step titles ≤ 3 words):
  - A1 "README A › Setup Environments" (A:9-52), 5: 1 Clone repo · 2 Enable services · 3 IAM user ·
    4 Execution role · 5 S3 bucket.
  - A2 "README A › Run Container" (A:60-99), 5: 1 aws configure · 2 Env variables · 3 Edit config ·
    4 chmod +x · 5 docker-shell.
  - A3 "README A › Prepare, deploy, predict" (A:101-148), 3: 1 Prepare model · 2 Deploy endpoint ·
    3 Test predictions.
  - A4 "README A › Clean Up" (A:150-176), 3: 1 Console delete · 2 AWS CLI · 3 CLI script.
  - B1 "README B › Setup Environments" (B:15-81), 9: 1 Clone repo · 2 AWS services · 3 S3 bucket ·
    4 IAM user · 5 Access keys · 6 Install CLI · 7 Configure CLI · 8 Test config · 9 IAM roles.
  - B2 "README B › Data Collector" (B:88-100), 3: 1 docker-shell · 2 Run search · 3 Check bucket.
  - B3 "README B › Data Processor" (B:107-120), 5: 1 docker-shell · 2 Run clean · 3 Check bucket ·
    4 Run prepare · 5 Check bucket.
  - B4 "README B › Model Training" (B:126-145), 5: 1 docker-shell · 2 Local training · 3 Package
    trainer · 4 Remote training · 5 Monitor jobs.
  - B5 "README B › Build & Push" (B:152-203), 11: 1 Hub login · 2 Hub build · 3 Hub push · 4 ECR
    variables · 5 Pull image · 6 Create repo · 7 ECR login · 8 Tag image · 9 Push image · 10 Verify
    push · 11 Print URI.
  - B6 "README B › Automate Collector" (B:210-224), 3: 1 docker-shell · 2 Processing job · 3 Check
    console.
  - B7 "README B › SageMaker Pipelines" (B:226-248), 3: 1 Run pipeline · 2 Check Studio · 3 Test
    components.
  S01, S02 and S16 have no tracker.
- `(extra)` after a command: not in the README. A small GREY tag `extra` (or a variant) sits beside
  the typed line, and the SAY says "extra" the first time each kind appears (S03: the clone's
  spelling, git log, listings; S04: the two fixes and the resolver checks; S06: the capture stub;
  S08: the local stand-in; S15: the offline definition). Later extras are marked on screen and named
  briefly.
- `▶ your turn`: a YELLOW tag beside the command or form at a real checkpoint (about one per README
  section); the SAY of that block says "pause". The video doesn't wait: the viewer pauses.
- Tags (GREY unless said): `illustration` on every CONSOLE form and on the V-diagrams' pictures of
  cloud machinery; `recorded · README A:137–147` on the README's predict output; the extra variants
  above; `erratum` on every README/code slip (the SAY says "a small gap" or "a small slip", never
  "erratum"); `at the time of recording` beside every version on first show; the GOLD `cost_tag()`
  at S03 (bucket storage), S06 (the tarball in S3), S07 (the endpoint, 24/7), S10 (quick setup, the
  Studio domain, the bucket), S12 (the training job, the trainer tarball), S13 (ECR storage), S14
  (the Processing job), S15 (each step's machine, the Lambda per run, `cheese-app-endpoint`) and
  S16's checklist card. No price anywhere: each cost tag says what bills, and "check the pricing
  page".
- `LECTURE 15 · a–b` in a SHOW line: the GREY `lecture_ref(15, "a–b")` tag (`explainer.devops`) sits
  top right ("Lecture 15 · slides a–b"; "slide" for one) **for that SHOW block only**: it fades in
  with the redrawn lecture picture and fades out with it at the end of the block. `LECTURE (held)`
  in the next block keeps it, only while the same picture stays on screen. A SHOW line without a
  LECTURE mark has no lecture tag (the L14 final check found tags outliving their pictures). Every
  lecture picture is our own redrawing in series colours with the slide's structure and terms: no
  slide image, QR code, logo, meme or screenshot.
- **The sandbox framing** (BRIEF, load-bearing): said once, in S02 (block 8). Afterwards every AWS
  error is just the next line of the lesson; every cloud answer is `recorded` (README A:137-147) or a
  tagged stand-in/stub. Never imply that a deploy, upload, job, push or pipeline run happened.

Colours (BRIEF "Colours", fixed for the whole video)

| meaning | colour |
| --- | --- |
| your laptop, its terminal, `~/.aws`, the IAM **user's access key** (a GREY key card on your disk), the people at four CLIs (slide 20) | GREY |
| the cloud: S3 buckets, SageMaker (Model, endpoint configuration, endpoint, Processing and Training jobs, the pipeline and its executions), ECR, Lambda, the IAM **role badges** (BLUE hard-hat badges), the AWS console | BLUE |
| containers and images: `model-deployment-cli-aws`, the four `cheese-app-*` images, the AWS prebuilt TensorFlow training and serving images, the TF Serving stand-in | TEAL |
| shared and outside your control: PyPI's "newest release" that `"*"` lets in, AWS-managed policies (`AmazonS3FullAccess` …), the scraped web, root-owned folders Docker made for you | ORANGE |
| what you own and pin: `sagemaker = "<3"`, committed `Pipfile.lock`s, your model artifact (`.keras`, SavedModel, `model.tar.gz`), the TFRecords, the pipeline definition | GREEN |
| tools and libraries: aws CLI, docker, pipenv, git, boto3, the SageMaker Python SDK, TensorFlow | PURPLE |
| errors and "don't": `exec format error`, `ModuleNotFoundError`, `NoCredentialsError`, `InvalidClientTokenId` / `InvalidAccessKeyId`, `PermissionError`, `not a valid identifier`, the `(None, 3)` layer, the forgotten endpoint | RED |
| your turn, the README tracker, "look here now", the ponder timer | YELLOW |
| money: endpoints (`ml.m5.xlarge`, `ml.m5.large`), Processing and Training jobs, S3 storage, ECR storage, Lambda, the clean-up card | GOLD |
| routes and references: S3 URIs, the prediction request and its JSON, `-v` / `-e` arrows into a container, **property references** (DAG edges: PINK solid) | PINK |
| the past and the future (L1, L13 training job, L14 Cloud Run, L23 automation) and the slide's Vertex AI words beside their AWS counterparts | GREY, dashed |

Pipeline step states (as in the exam edition): pending = WHITE outline; running = YELLOW fill;
succeeded = GREEN ✓ badge at the right end; failed = RED; cached = GREY dashed with a small "cached"
chip. Identity badges: a GREY key card for the IAM user; a BLUE hard-hat badge per role
(`SageMakerExecutionRole`, `CheeseAppSageMakerExecutionRole`, `CheeseAppLambdaExecutionRole`).

Running example
- **The laptop** (`laptop/`: a fresh `docker:29.8.2-dind` engine, linux/x86_64, standing in for
  Docker Desktop; AWS CLI 2.34.63; git 2.54.0): terminal title `laptop`, prompts
  `student@laptop:~$`, then `student@laptop:~/model-deployment-aws$` (Part A),
  `student@laptop:~/ml-workflow-aws$`, `…:~/ml-workflow-aws/src/data-collector$`,
  `…/src/data-processor$`, `…/src/model-training$`, `…/src/workflow$` (Part B). The step files carry
  no prompt; the scenes draw these.
- **Inside containers** (prompts from the captures, ids masked): `(app) app@<id>:/app$` (Part A,
  training, workflow) and `root@<id>:/app#` (collector, processor).
- **Placeholders on screen**: bucket `your-models-bucket-placeholder` and role
  `arn:aws:iam::000000000000:role/SageMakerExecutionRole` (Part A, `laptop/17`); keys
  `PLACEHOLDER_NOT_A_REAL_ACCESS_KEY` / `PLACEHOLDER_NOT_A_REAL_SECRET_KEY_000000000000`
  (`laptop/55`); the README's own example ARN account `123456789012` (README A:43, AWS's
  documentation placeholder; shown only inside the README card, chip "AWS documentation
  placeholder"); the pipeline helper's account `000000000000` (`laptop/92`); `763104351884`
  (`laptop/92:191`, `251`) masked as `<aws-dlc-account>` if those lines ever show. The README
  example bucket names are shown with their "[REPLACE WITH YOUR UNIQUE BUCKET NAME]" note.
- **Never shown or said**: the eight sample photos and the 40 scraped images (only their file
  names; `laptop/60`'s URL lines 44–45, 144–147, 218–219, 373–374 etc. are never printed); the
  scraped sites' names; container ids; timestamps and the endpoint's timestamp suffix; the commit
  subject's branch name (`laptop/11:2`, `to "#1 from"` then `…`: it carries a person's name; BRIEF
  "Personal data"); the instructor's name.

Length and parts: BRIEF target narration **~4,190** words (`python -m explainer.script`, which
counts SAY words; its minute figure assumes 155 wpm and is ignored). At Kokoro af_heart speed 0.9
(≈174 wpm) that is ≈24 min of narration, ≈30–32 min with typing, outputs, CONSOLE fills and four
ponder timers. Part 1 = S01–S09 (deploy one model, README A; ends on the empty endpoint slot with
the GOLD meter stopped and the parked question). Part 2 = S10–S16 (automate the workflow, README B;
ends on the last test-yourself card, then an empty frame). Per-scene counts: see the table at the
end of "Notes for scene authors" (re-run the counter after any edit).

Notes for scene authors
- Shared code (`scenes/common.py`, started from L14's): tracker factories `tracker_a1` … `tracker_a4`,
  `tracker_b1` … `tracker_b7` with the step lists above; prompts `P_LAPTOP`, `P_MD`
  (`~/model-deployment-aws`), `P_MW` and `P_SRC(stage)`, `P_APP`, `P_ROOT`; tags `your_turn`,
  `extra_tag` (+ the four variants), `illustration_tag`, `recorded_tag(source)`, `erratum_tag`,
  `cost_tag(text)` (GOLD), `lecture_ref`; `console_form(title, rows)`; `bridge_card(rows)` (S02,
  reused small as a mini-legend); set pieces `IdentityBadges` (V1), `StarVsPin` (V2), `TwoPipes`
  (V3), `ArtifactTrip` (V4), `ThreeObjects` (V5), `ManualToPipeline` (V6), `CallableImage` (V7),
  `ReferenceDAG` (V8). Never reuse a scene class name for a helper.
- TERM line numbers are *file* lines (line 1 = the `$` command); `Capture.pick()` indexes the output
  body, so pick index = file line − 1. For the multi-line commands listed under TERM, check how
  `capture()` splits command and output before picking, and assert the picked text. In `istep`
  files the typed container lines are themselves file lines (`laptop/25:35`): type their text after
  the masked prompt, never print them.
- Long output lines: `laptop/16:6`, `53:4/6`, `57:4/6`, `60:654`, `68:107/178`, `73:146/157/313`,
  `90:98–99`, `92:30` fold (`wrap`) or start `from` the meaningful phrase as marked. `laptop/22`
  shows its header and the named packages only. `laptop/89` (9,356 lines) shows only line 9334.
- Crops: SDK and boto3 deprecation warnings (`SageMakerV2DeprecationWarning`,
  `PythonDeprecationWarning: Boto3 will no longer support Python 3.9 …`), TensorFlow's CUDA,
  oneDNN and AVX start-up lines, protobuf `UserWarning`s and the `sagemaker.config INFO` lines are
  never printed (S04 block 12 says once that warnings are not the error). The `[capture stub]` and
  `[capture stand-in]` lines are always printed: they say what is not real.
- Lexicon (`explainer/lexicon.yaml`, block `# AC215 L15`, phonemes checked with
  `KokoroBackend('af_heart', 0.9).phonemize()`): `aws configure`, `aws sagemaker` (phrase keys: a bare
  lower-case `aws` is read "awes", and another video says it), `A R N`, `A R M 64`, `A B testing`,
  `2.13`, `2.18`, `2.20`, `TFRecord`, `TFRecords`, `tfrecords`, `S3 URI` (phrase: L13/L14 say a bare
  "URI"), `upsert`, `Upsert`, `upserts`, `or updates`. Read correctly without entries: SageMaker, S3,
  ECR, SDK, YAML, D S L, C S V, R G B, JPEG, Lambda, PyTorch, Unified Studio, the instance types.
  Words kept out of SAY instead of adding a key that finished videos would hit: "dot gitignore"
  (said "the git ignore file" / "Git ignores"), "chown" (on screen only). "difPy" is never said ("a
  duplicate finder"). Existing entries used: `AWS`, `us-east-1`, `IAM`, `pipenv`, `Pipfile.lock`,
  `cli.py`, `docker-shell.sh`, `package-trainer.sh`, `Kubeflow`, `A M D 64`, `3.9`.
- Subtitle display (`en_display` in `i18n/zh/narration/*.yaml`): dash dash prepare / deploy /
  predict / delete / clean / train / pipeline → `--prepare` …; dash dash data collector →
  `--data_collector`; star → `"*"`; less than 3 → `"<3"`; or true → `|| true`; slash persistent
  slash model (slash 1) → `/persistent/model(/1)`; model dot tar dot G Z → `model.tar.gz`; endpoint
  config dot JSON → `endpoint_config.json`; raw dot zip, clean dot zip, tfrecords dot zip → the file
  names; saved model dot P B → `saved_model.pb`; A R N → `ARN`; A R M 64 → `arm64`; A M D 64 →
  `amd64`; C S V → `.csv`; M L M5 extra large → `ml.m5.xlarge`; M L T3 medium → `ml.t3.medium`;
  arg max → `argmax`; R G B → `RGB`; D S L → `DSL`; python 3 → `python3`; the who am I call →
  `aws sts get-caller-identity`; cheese app endpoint → `cheese-app-endpoint`; the git ignore file →
  the `.gitignore` file; dash e → `-e`; A B testing → `A/B testing`; model deployment (the user) →
  `model-deployment`; ml workflow user → `ml-workflow-user`; clone ml workflow AWS → `ml-workflow-aws`;
  SageMaker Execution Role → `SageMakerExecutionRole`; Cheese App SageMaker Execution Role / Cheese
  App Lambda Execution Role → `CheeseAppSageMakerExecutionRole` / `CheeseAppLambdaExecutionRole`; the
  pipeline step names in S15 (data collector, deploy model, create model) → `DataCollector`,
  `DeployModel`, `CreateModel`; raw data (the declared output) → `raw-data`; python 3 → `python3`.
  In zh all of these stay English (glossary rule).
- Chinese glossary heads-up: BRIEF "Notes"; reuse `../ac215-l15-exam/i18n/zh/glossary.yaml` where it
  agrees (DAG, pipeline, endpoint, registry).
- Never: a real-looking key, token, account id or ARN; the instructor's name; a console screenshot
  or the READMEs' images; an invented output line, endpoint name, job name or ARN; the TF Serving
  stand-in, the S3 stub or the offline pipeline JSON presented as AWS results; "serverless = scale
  to zero" or "pay per request" for the endpoint; the `steps=[…]` list called the run order; a
  property reference called a string; a claim about where the training step's data lands on
  SageMaker; a green `DeployModel` called a working endpoint; keys suggested for an image, a script
  or `docker-shell.sh`; a real-looking Docker Hub token.
- Word counts (`python -m explainer.script`, v2 after the review merge; BRIEF target · ±15 % band):

  | scene | words (BRIEF · band) | scene | words (BRIEF · band) |
  | --- | --- | --- | --- |
  | S01 Hook | 181 (200 · 170–230) | S10 FourTerminals | 295 (280 · 238–322) |
  | S02 LectureMap | 213 (250 · 213–288) | S11 CollectAndClean | 297 (280 · 238–322) |
  | S03 UserRoleBucket | 304 (300 · 255–345) | S12 TrainLocally | 280 (260 · 221–299) |
  | S04 TwoFixes | 364 (330 · 281–380) | S13 PushToECR | 225 (230 · 196–265) |
  | S05 FrontDoor | 246 (240 · 204–276) | S14 WorkflowShell | 234 (230 · 196–265) |
  | S06 PrepareArtifact | 247 (250 · 213–288) | S15 PropertyDAG | 374 (330 · 281–380) |
  | S07 ModelToEndpoint | 290 (290 · 247–334) | S16 TeardownRecap | 261 (240 · 204–276) |
  | S08 AskTheEndpoint | 259 (280 · 238–322) | | |
  | S09 TurnOffTheMeter | 227 (200 · 170–230) | | |
  | **part 1** | **2,331** (2,340) | **part 2** | **1,966** (1,850) |

  Total **4,297** (BRIEF ≈ 4,190; series ceiling 4,300). Every scene is inside its band. Tight: S02
  (213, at the floor), S15 (374/380), S04 (364/380), S09 (227/230) and the total (4,297 of 4,300), so
  any later addition names its cut in the same scene (BRIEF: S13's Docker Hub beat is already
  trimmed; S02 is at its floor; never a README step).

---

## S01 · Three numbers or four? — `s01_hook.py` · `Hook`

SHOW: Black frame, no tracker. Two full-width panels stacked. Top: RECORDED(expected/md-predict-readme.txt:
7–10), tag `recorded · README A:137–147`: `Image: data/brie-2.jpg`, `Result: {'predictions':
[[0.0887121782, 0.0439011417, 0.867386699]]}`, `… 2`, `Label:    brie`. Bottom: a terminal strip
(title `laptop`) printing TERM(laptop/47: 23–26), tag `extra · local stand-in, not SageMaker`:
`Image: data/brie-1.jpg`, four numbers, `… 2`, `Label:    brie`. Above the top panel only, a YELLOW chip types
`python cli.py --predict`; the bottom panel keeps its `extra · local stand-in` tag. On "same predict
code", a GREY chip `cli.py · predict()` links both panels. On "brie", both `Label:` lines glow GREEN
together.
SAY: Here is a question for a model: what cheese is in this photo? Both answers on screen come from the same predict code in cli.py. And both answers say brie.

SHOW: Small YELLOW brackets count the numbers inside each `predictions` list: 1, 2, 3 over the top
panel; 1, 2, 3, 4 over the bottom one. A big "3" and a big "4" settle at the right edge of each
panel; a RED "≠" pulses between them. A YELLOW question card fades in centre bottom: "What is
behind an endpoint?"
SAY: Now count the numbers. The top answer, the README output, holds three. The bottom one, from this recording, holds four. One model cannot give both. So which model is behind an endpoint, and what else is there?

SHOW: The panels and the card slide away. **V5 `ThreeObjects` preview**: three empty slots appear in
a row, each with a label writing in on its phrase: GREEN "artifact · which model", TEAL "container ·
what runs it", BLUE "machine · where it runs". On "who pays", a GOLD meter beside the machine slot
starts ticking and LECTURE 15 · 11 fades in with it (slide 11's continuous cost of an endpoint; the
three-slot split is ours, SCENE-NOTES says so); a thin PINK request lane above the slots stays empty
(no pulses). On "no request", the lane flashes "0 requests" in GREY while the meter keeps rising. At
block end the meter and the lecture tag fade together.
SAY: Behind an endpoint sit three pieces: an artifact, which model; a container, what runs it; and a machine, where it runs, and who pays. The meter beside the machine keeps running while no request arrives.

SHOW: The slots shrink to the upper left. Four GREY tiles flicker in along the bottom, "Data
Collector", "Data Processor", "Model Training", "Model Deploy", then PINK edges snap between them
into a chain; a single BLUE "pipeline" frame closes around all four.
SAY: In part 2, we stop running these steps by hand. The four stages of the Cheese App become one pipeline that the cloud runs for you.

SHOW: Clear to a checklist of four GREY chips, one per phrase: "AWS account + billing", "AWS CLI
v2", "Docker", "both clones: model-deployment-aws · ml-workflow-aws". A small BLUE "first AWS
lecture" badge on the first chip.
SAY: To follow along, you need an AWS account with billing, the AWS CLI, Docker, and both repositories cloned. This is our first lecture on AWS.

SHOW: The chips fade. Top left, a sample YELLOW `ReadmeTracker` ("README A › Run Container · step 1
of 5") fades in; beside a sample command a YELLOW `▶ your turn` tag pulses; a GREY chip "eleven small
trackers · two READMEs". On "study guide", a GREY card "study guide: every command + real outputs".
Everything fades; empty frame.
SAY: A tracker in the corner names the README step, and a yellow tag, your turn, means pause and run it. Every command is also in the study guide.

---

## S02 · Where we are, in AWS words — `s02_map.py` · `LectureMap`

SHOW: No tracker. LECTURE 15 · 6–7. Slide 6 redrawn small: a wide GREY arrow with "POC",
"Prototype", "MVP"; three thin bars under it ("Build Better Models", "ML Workflow", "Deployment,
Scaling & Automation"); an unlabelled dashed YELLOW box over the Prototype block. The roadmap slides
up; four tiles in a row (our shapes, series colours, no slide icons): "1 Data Collector", "2 Data
Processor", "3 Model Training", "4 Model Deploy". Ticks write into tiles 1–3; tile 4 pulses YELLOW.
SAY: First, where this lecture sits. The course project is in its prototype phase, and of the four parts of the Cheese App, three are done. Model deploy is still open.

SHOW: LECTURE 15 · 6–7 (held). Under tile 4 a YELLOW chip "part 1"; a PINK bracket under all four
tiles, chip "part 2". Then the tiles fade with the tag.
SAY: Part 1 of this video fills that tile. Part 2 connects all four.

SHOW: LECTURE 15 · 8. A GREY-dashed card "L14 · Cloud Run · containers" slides in at the left edge,
holding a small TEAL box; the TEAL box gains a GREEN model bulb ("today: the container serves a
trained model"). The card parks at the left edge, small; the tag fades with the picture.
SAY: Last week, lecture 14 put containers on Cloud Run. Today, the container serves a trained model.

SHOW: LECTURE 15 · 10. Slide 10 redrawn as a four-row sidebar (no screenshot): "Workbench ·
notebooks", "Training · L13" with a GREY tick, "Online prediction", "Pipelines"; on "today's two"
the last two rows light YELLOW. The sidebar shrinks away with the tag.
SAY: The lecture maps its console onto the course: notebooks, training from lecture 13, and today's two, online prediction and pipelines.

SHOW: `bridge_card` builds: two column headers, "the lecture · Vertex AI" (GREY dashed) and "this
tutorial · AWS" (BLUE). A GREY chip under it: "course map: dlops-io/model-deployment ·
dlops-io/ml-workflow (GCP) → we follow model-deployment-aws · ml-workflow-aws".
SAY: The lecture is written for Vertex AI on Google Cloud. This course also ships an AWS version of both tutorials, and that is the one we follow. Same ideas, different names. I'll point out each one as we meet it.

SHOW: Three rows only, each writing in on its phrase: "GCS bucket → S3 bucket"; "service-account key →
IAM user + access key (laptop) / role (cloud)" (a GREY key card and a BLUE badge icon); "Online
prediction endpoint → endpoint configuration + endpoint". The card shrinks to the lower right as a
mini-legend icon and fades. The other four rows of the bridge appear later as a small `bridge_card`
mini-legend chip in the scene where each word first matters (no words added there): "Model Registry →
SageMaker Model" in S07, "Vertex AI Pipelines (Kubeflow, KFP DSL) → SageMaker Pipelines (SDK step
classes)" in S10, "Artifact Registry → ECR" in S13, "Cloud Functions → Lambda" in S15.
SAY: A Google Cloud bucket becomes S3. A service account key becomes an IAM user with a key on your laptop, plus a role in the cloud. And an endpoint becomes a configuration plus an endpoint.

SHOW: A GREY card: "this recording: no AWS account". Three lines write in on their phrases: GREEN
"laptop steps · real"; RED "AWS calls · honest first error"; GREY "cloud answers · `recorded` or a
tagged stand-in". Under it, a terminal strip types `aws sts get-caller-identity` (extra) →
TERM(laptop/15: 3 wrap), RED. A RED-struck chip "faked success" on "Never".
SAY: One thing about this recording: it has no AWS account. Every step that runs on your laptop is real. Every AWS call stops at its honest first error, like this one. Where the cloud would answer, you see the README output, or a tagged local stand-in. Never a faked success.

SHOW: The card fades. Two version chips with `at the time of recording`: "Docker 29.8.2"
(TERM(laptop/00: 4) as a one-line strip) and "AWS CLI 2.34.63" (TERM(laptop/01: 2 to
"aws-cli/2.34.63")). Fade to empty.
SAY: Versions at the time of recording are on screen.

---

## S03 · A user, a role and a bucket — `s03_setup.py` · `UserRoleBucket`

SHOW: TRACKER A1 1 (tracker appears: "README A › Setup Environments", 5 dots). Full-width
terminal, title `laptop`, prompt `student@laptop:~$`. A README card (`README.md · lines 9–10`,
chip "A"): "Clone or download from here", GREY chip "the README spells no command". It types
`git clone https://github.com/dlops-io/model-deployment-aws.git` (extra: its spelling) →
TERM(laptop/10: 2); `▶ your turn`. `cd model-deployment-aws` → (no output); prompt
`student@laptop:~/model-deployment-aws$`. TRACKER A1 1 · extra: `git log -1 --format='%H %ci %s'`
(extra) → TERM(laptop/11: 2 to "#1 from", then `…`), `077f4dbc7b13…` YELLOW, chip "main · the
commit we follow".
SAY: Step 1: clone the repository. The README says clone or download, so our git clone is extra, and so is the git log that shows the commit we follow. Pause and clone it.

SHOW: TRACKER A1 1 · extra. It types `ls -la; ls data` (extra) → TERM(laptop/12: 7–10, 12–13, …,
15–22), the eight photo names in two columns (names only, no thumbnails); line 13
`-rwxr-xr-x … docker-shell.sh` YELLOW on "already executable".
SAY: An extra listing: the CLI, a Dockerfile, a Pipfile, eight sample photos, and docker-shell.sh, already executable.

SHOW: The terminal fades out (nothing is typed in this block). TRACKER A1 2. CONSOLE("Services",
A:12-16): three GREY checks "Amazon S3", "Amazon SageMaker", "AWS IAM". TRACKER A1 3. On "Then", the
services form **Transforms** into CONSOLE("IAM › Create user", A:21-30) (one form on screen at a
time): user name `model-deployment`; three ORANGE policy chips `AmazonS3FullAccess`,
`AmazonSageMakerFullAccess`, `IAMFullAccess`; on "broader", the third chip gets a small ORANGE flag
"broader than this code needs". Then a row "Create access keys · save both", no key drawn; only on
"save both" a GREY laptop icon appears at the left and a GREY key card drops into its drawer labelled
`~/.aws`.
SAY: Steps 2 and 3 are in the AWS console. Check that you can use S3, SageMaker and IAM. Then create an IAM user called model deployment, with three policies. The third is broader than this code needs. Create access keys and save both.

SHOW: TRACKER A1 4. CONSOLE("IAM › Roles › Create role", A:36-44): trusted entity "SageMaker";
policies `AmazonSageMakerFullAccess`, `AmazonS3FullAccess`; name `SageMakerExecutionRole`. A README
card (`README.md · line 43`): `arn:aws:iam::123456789012:role/SageMakerExecutionRole`, the digits
GREY with a chip "AWS documentation placeholder". A BLUE hard-hat badge labelled
`SageMakerExecutionRole` forms in a BLUE cloud at the right.
SAY: Step 4 creates a role named SageMaker Execution Role, trusted by SageMaker, with the SageMaker and S3 policies. Copy its A R N.

SHOW: **V1 `IdentityBadges` built**: GREY laptop left (the key card in its `~/.aws` drawer), BLUE
cloud right (the badge). A PINK request arrow leaves the laptop stamped with the key card ("signed
by the user"). A small BLUE endpoint box (dashed: "later") appears in the cloud and puts the badge
on. A GREY border line between laptop and cloud: the key card bounces off it on "stays".
SAY: Why two identities? Your laptop signs each request with the user key, and the endpoint you create later acts as the role. The key stays on your laptop.

SHOW: TRACKER A1 5. V1 shrinks to the right. CONSOLE("S3 › Create bucket", A:46-52): bucket name
`cheese-app-models-demo` with the README's "[REPLACE WITH YOUR UNIQUE BUCKET NAME]" note in ORANGE;
a GREY chip "unique across all AWS accounts". A BLUE bucket joins the cloud. GOLD `cost_tag("S3
storage · while files exist · check the pricing page")`. `▶ your turn` on the form. Then a RED card
(README card `README.md · lines 56–58`): "NEVER hardcode AWS credentials directly in scripts or
commit them to Git!"
SAY: Step 5, then pause: create a bucket with a name of your own, because bucket names are unique across all of AWS. Storage bills while files sit in it. And as the README warns, never put keys in a script, and never commit them to Git.

SHOW: TRACKER A2 1 (tracker changes: "README A › Run Container", 5 dots). Full-width terminal again.
It types `aws configure` → TERM(laptop/13: 3 wrap, 5–8); line 3 (the `aws login` tip) with a GREY
chip "newer than the README · at the time of recording"; lines 5–6 GREY with a chip "paste your two
keys here · we have none"; `us-east-1` and `json` YELLOW. `▶ your turn`.
SAY: Run Container, step 1: aws configure. Then come four prompts. You paste your two keys. We have none, so we press Enter twice, then type us-east-1 and json.

SHOW: TRACKER A2 1 · extra. It types `ls -la ~/.aws; cat ~/.aws/config` (extra) → TERM(laptop/14:
5–8); only `config`, GREY chip "no credentials file: no keys typed". V1's drawer shows one GREY
`config` card, no key card. Then the terminal clears and types `aws sts get-caller-identity`
(extra; chip "the who-am-I call") → TERM(laptop/15: 3 wrap) RED; a GREEN chip "with your keys: your
account id". `▶ your turn`.
SAY: Two extras: only the config file exists, since we typed no keys, and the who am I call cannot find credentials. With your keys, it prints your account. Pause and make yours print it.

SHOW: TRACKER A2 2. It types the three README exports plus the who-am-I check (extra, line 4) →
TERM(laptop/16: 6 wrap) RED: the security token is invalid.
SAY: Step 2 offers a second option: three exports in your shell. AWS rejects our placeholder key.

SHOW: TRACKER A2 2. The terminal goes out. V1 returns large; CODE(docker-shell.sh: 22–28) as a narrow
strip under it, its lines lighting in step with the arrows. First line 24's `-v ~/.aws:/home/app/.aws`
arrow carries the whole drawer into the container (PINK). Then three GREY `export` cards float in the
laptop shell; a TEAL container wall rises; only three PINK `-e` arrows (`AWS_REGION`,
`S3_MODELS_BUCKET_NAME`, `SAGEMAKER_ROLE`, lines 25–27 YELLOW) pass; on "fall off", the two key cards
hit the wall and drop. Then tag `erratum`, chip "use option 1 · or add -e AWS_ACCESS_KEY_ID -e
AWS_SECRET_ACCESS_KEY". Fade to empty.
SAY: There is a subtler gap: the script passes only the region, the bucket and the role into the container. So exported keys fall off at the wall. Use option 1, or add the keys with dash e.

---

## S04 · The CLI container: two one-line fixes — `s04_build.py` · `TwoFixes`

SHOW: TRACKER A2 3. Prompt `student@laptop:~/model-deployment-aws$`. It types the `sed` of
laptop/17's line 1 (extra: our editor; folds; GREY chip "use your editor") → TERM(laptop/17: 4–6);
the three values YELLOW: `your-models-bucket-placeholder`, `arn:aws:iam::000000000000:role/
SageMakerExecutionRole` (chip "placeholder account"), `us-east-1`. `▶ your turn`.
SAY: Step 3: edit docker-shell.sh with your bucket, the A R N of your role, and your region. Ours are placeholders.

SHOW: TRACKER A2 4. It types `chmod +x docker-shell.sh` → (no output). TRACKER A2 4 · extra:
`ls -l docker-shell.sh` (extra) → TERM(laptop/19: 2), `-rwxr-xr-x` GREEN.
SAY: Step 4, chmod, prints nothing. An extra listing shows the script was already executable.

SHOW: TRACKER A2 5. It types `sh docker-shell.sh` → TERM(laptop/20: 19 cut, …, 35 cut, 36, …, 49
cut); line 19 `FROM docker.io/library/ubuntu:20.04@sha256:…` with a chip "arm64 variant pulled";
line 36 `exec /bin/sh: exec format error` RED; line 49 `ERROR: failed to build` RED. A small picture
beside it: an ARM chip-shaped TEAL image trying to run on an x86 GREY laptop CPU, a RED cross.
SAY: Step 5: sh docker-shell.sh. It pulls the base image for A R M 64, then stops at the first RUN line: exec format error. Our Intel style laptop cannot run those programs.

SHOW: TRACKER A2 5 · extra. CODE(docker-shell.sh: 16–19): line 19 (`--platform=linux/arm64/v8`) RED
with chip "M1/2 chip macs use this line", line 17 (`#docker build -t $IMAGE_NAME -f Dockerfile .`)
GREEN. On "swap", the two lines exchange their `#`. It types the `sed` of laptop/21's line 1 (extra;
folds) → TERM(laptop/21: 2–4); a GREEN chip "fix 1 · plain build line". Three platform chips:
"Apple silicon Mac: arm64 line works", "Intel Mac / Windows: emulated, slow", "Linux PC: this error".
SAY: The fix is in the script. Line 19 is for Apple silicon Macs, and line 17, commented out, is the plain build. Swap them: fix 1, an extra. On Apple silicon the original line works. Elsewhere it means slow emulation, or this error.

SHOW: CODE(Pipfile: 8–17): line 10 `sagemaker = "*"` ORANGE, line 13 `tensorflow = "==2.18.0"`
GREEN, line 17 `python_version = "3.9"`. Two small panels beside it: CODE(.gitignore: 67–68), line 68
`Pipfile.lock` GREY with chip "keeps a lock out of the repository"; then CODE(Dockerfile: 52–55),
line 52 `ADD --chown=app:app Pipfile /app/` PINK and line 55 `RUN cd /app && pipenv lock && pipenv
sync` ORANGE with chip "the lock is made at build time".
SAY: Now look at the Pipfile. TensorFlow is pinned to one version, but SageMaker says star: any version. And no lock is used: Git ignores the lock file, and the Dockerfile runs pipenv lock at build time.

SHOW: The two panels dim. A YELLOW card.
SAY: Something to ponder. The code worked when it was written, and nobody changed a line. Why does cli.py fail at import today?
PONDER(8 s, "The Pipfile says sagemaker = \"*\".\nThe code worked when it was written.\nNobody changed a line. Why does\ncli.py fail at import today?")

SHOW: **V2 `StarVsPin` built.** A number line "2.200 … 2.257 | 3.0 … 3.29"; on "star", the whole line
lights ORANGE. TRACKER A2 5 · extra · check: a terminal strip types laptop/22's line 1 (extra;
cut) → TERM(laptop/22: 4, …, 12, …, 26, …, 35); line 4 `185 packages would be installed` YELLOW,
`sagemaker==3.13.1` RED, `torch==2.8.0` and one `nvidia-cublas-cu12` line ORANGE with a chip
"14 CUDA packages" (laptop/22: 12–25), all with `at the time of recording`. A PURPLE arrow labelled
"resolver" drops a dot at 3.13 on the line.
SAY: Star is a constraint, not a pin, as in lecture 1: the resolver takes the newest release that installs. At the time of recording, on Python 3.9, that is SageMaker SDK version 3, with PyTorch and 14 CUDA packages.

SHOW: TRACKER A2 5 · extra · check. TERM(laptop/23: 7–8, 9–14), laptop/23's line 1 typed (extra;
cut). Under the 3.x half of V2, a shelf of six GREY module boxes (`ai_registry`, `core`, `lineage`,
`mlops`, `serve`, `train`, from line 8); under 2.x, another shelf (`tensorflow`, `serializers`,
`processing`, `workflow`, `get_execution_role`). Three PURPLE import arrows from `cli.py: 21–23`
reach into the 3.x shelf, find nothing and turn RED with `ModuleNotFoundError` / `ImportError`.
SAY: Version 3 is a rewritten package, without the modules cli.py imports: no tensorflow module, no serializers, no get execution role. The imports find nothing.

SHOW: A GREY note card (no terminal): "here: the unpinned build ran 13 min in `pipenv lock`, then
ran out of disk · not kept as a capture". Under it a GREY `pipenv lock` progress bar crawls while a
"13 min" counter runs, until a RED "disk full" stamp lands on "ran out of disk". On "On your laptop",
a GREY laptop icon shows its own bar finishing, then a RED `ImportError` stamp on "fail".
SAY: Here, the unpinned build ran 13 minutes, then ran out of disk. On your laptop it would finish, then fail at the first import.

SHOW: TRACKER A2 5 · extra. It types `sed -i 's/^sagemaker = "\*"/sagemaker = "<3"/' Pipfile && git
diff Pipfile` (extra) → TERM(laptop/24: 9–12); line 10 RED, line 11 GREEN. On V2 a GREEN wall
slides in at 3.0; the dot jumps back to "2.257"; the imports click into the 2.x shelf. Caption: "a
constraint is not a pin (L1)". Chip "fix 2". `▶ your turn`.
SAY: Fix 2, also an extra: change star to less than 3. The resolver stops at the last version 2 release, and the imports work. Pause and make both fixes.

SHOW: TRACKER A2 5. It types `sh docker-shell.sh` → TERM(laptop/25: 3 cut, …, 23 cut, …, 29–30,
32 wrap, 33); line 3 `[+] Building 400.6s (19/19) FINISHED` with `at the time of recording`; line
23 `[13/14] RUN cd /app && pipenv lock && pipenv sync … 334.7s` YELLOW; line 29 `Container is
running!!!`; line 32 RED; line 33 `Launching subshell in virtual environment...`; then the prompt
`(app) app@<id>:/app$` with a GREY chip "the id changes every run". V2 fades.
SAY: Run step 5 again. It builds in almost 7 minutes, mostly locking and installing packages. The AWS check fails without keys, but the shell still opens.

SHOW: TRACKER A2 5 · extra. At the container prompt it types `python --version; which python
pipenv aws` (extra) → TERM(laptop/25: 36); `pip list 2>/dev/null | grep -i -E "^(tensorflow|keras|
sagemaker|sagemaker-core|boto3|numpy|pillow) "` (extra; folds) → TERM(laptop/25: 45, 47); `echo
$S3_MODELS_BUCKET_NAME $AWS_REGION $SAGEMAKER_ROLE` (extra) → TERM(laptop/25: 49). Versions with
`at the time of recording`. A GREY chip "deprecation warnings ahead: not the error".
SAY: Inside, extras show Python 3.9, SageMaker version 2 and TensorFlow 2.18, and the three values from the script. Deprecation warnings are not the error.

SHOW: TRACKER A2 5 · extra. It types `python cli.py --help` (extra) → TERM(laptop/25: 73, 75,
78–83); lines 75 `Data Collector CLI`, 79 `GCS Bucket`, 80–82 `Vertex AI` ORANGE with tag
`erratum` and chip "kept from the Google version · the commands are AWS"; line 82 `--test` with chip
"does nothing". Then a host strip (`student@laptop:~/model-deployment-aws$`): `docker image ls
model-deployment-cli-aws` (extra) → TERM(laptop/26: 2–3; squeeze), `4.01GB` with `at the time of
recording`. Fade to empty.
SAY: A small slip: the help text still says GCS bucket and Vertex AI, and the test flag does nothing. The commands are the AWS ones. The image is about 4 gigabytes.

---

## S05 · Where does preprocessing live? — `s05_signature.py` · `FrontDoor`

SHOW: TRACKER A2 5 (concept beat, the tracker stays dim). LECTURE 15 · 13. Slide 13's contrast
redrawn: left a GREY notebook with three cells ("resize", "normalize", "predict") lighting one by
one; right a BLUE endpoint box with a JPEG icon going in and one answer coming out, chip "one
request".
SAY: Before we prepare the model, a design question from the lecture: where does preprocessing happen? In a notebook, you resize and normalize cell by cell. A production endpoint should take the raw photo and do all of that itself.

SHOW: **V3 `TwoPipes`, left pipe built.** A JPEG on the GREY laptop passes two PURPLE gears,
`resize 224×224` and `÷ 255`, becomes a TEAL-outlined cube "224 × 224 × 3 floats", and travels a
PINK wire to the BLUE endpoint. CODE(cli.py: 219–225) beside it: line 222 lights with the resize
gear, 223 with the ÷ 255 gear, 225 `payload = {"instances": [arr.tolist()]}` PINK with the wire.
SAY: In this tutorial, the client does it. The predict code opens the photo, converts it to R G B and resizes it to 224 by 224. Then it divides by 255 and sends the numbers as JSON.

SHOW: TRACKER A2 5 · extra. A terminal strip types laptop/43's line 1 (extra; cut) → TERM(laptop/43:
13–15, 18–20); `DT_FLOAT` and `(-1, 224, 224, 3)` YELLOW, `(-1, 4)` GREEN. The model's front door
on V3 gets the label `inputs['input'] · floats (-1, 224, 224, 3)`; four bars come out of the back.
SAY: An extra check reads the model's front door, which TensorFlow calls a signature. It takes floats, shaped any number by 224 by 224 by 3, and gives four numbers per photo. Preprocessing sits on your side of the wire.

SHOW: LECTURE 15 · 13. Three client icons appear at the left, each with its own gear set: "web
app" (correct), "phone app" (the `÷ 255` gear missing, RED), "notebook" (a different resize).
The phone's cube enters the endpoint and a confident wrong bar shoots up RED. A label writes over
them: "client-side brittleness". Then a GREEN "one copy in the model" chip with two small arrows
"roll back · version".
SAY: The lecture names the risk: client-side brittleness. Every client must repeat those steps exactly, and a phone app that forgets to divide by 255 gets confident nonsense. One copy inside the model is also easier to roll back and version.

SHOW: LECTURE 15 · 14. **V3 right pipe**, picture only (no code panel here: the code's first full
showing is S12), with a GREY chip "part 2 · task.py": the JPEG's raw bytes travel the PINK wire; the
left pipe's gears **Transform** across the wire and settle *inside* the model's front door, labelled
`serving_default`, so the same three operations visibly change sides; they light in turn as
`decode_jpeg → float32 → resize`. First callout: "define preprocessing".
SAY: The fix from the lecture sits in the part 2 trainer. The preprocess function decodes the JPEG, converts it to floats, and resizes it.

SHOW: LECTURE 15 · 14 (held). Picture only: a stack of JPEG strings enters the door (callout 2 "new
signature: a batch of strings"); the door gets a GREEN tag `serving_default` (callout 3 "save as
serving default"). The right pipe's door: "bytes in", class bars out, their count drawn as "?" (the
part 2 trainer's class count is S12's fix A).
SAY: A function marked as the model's front door takes a batch of JPEG strings, prepares each one, and calls the model. It is saved as the serving default. Raw bytes in, one score per class out.

SHOW: A README card (`README.md · line 115`, chip "A"): "Prepare the model in TensorFlow SavedModel
format", with two labels under it: GREEN "format change ✓" and GREY-struck "signature change". Fade
to empty.
SAY: One trap to avoid. The README says the prepare step converts the model to the SavedModel format. That is a change of format, not the change of signature from the lecture.

---

## S06 · --prepare: a SavedModel in a tarball — `s06_prepare.py` · `PrepareArtifact`

SHOW: TRACKER A3 1 (tracker changes: "README A › Prepare, deploy, predict", 3 dots). LECTURE 15 · 12.
A README card (`README.md · lines 113–117`, chip "A") lists the four bullets. **V4 `ArtifactTrip`**
draws them left to right as they are spoken: a GREY-dashed "GitHub release · v1.0" box; a TEAL
container; a GREEN SavedModel folder; a GREEN `model.tar.gz`; a BLUE S3 bucket; small pink step
numbers 1 and 3 (slide 12's steps 1 and 3) above the arrows, and a GREY-struck "2 · signature" chip
between them.
SAY: Step 1: python cli.py dash dash prepare. The README lists four things. Download the model from GitHub, convert it to the SavedModel format, pack it as model dot tar dot G Z, and upload it to your bucket. Those are steps 1 and 3 of the lecture deployment picture. Step 2, the signature change, is not in part 1.

SHOW: The diagram shrinks to the top. Container prompt `(app) app@<id>:/app$` with a GREY chip "our
capture: a fresh container per step · stay in yours". It types `python cli.py --prepare` →
TERM(laptop/27: 52, …, 74, 79, …, 227); line 79 `❱  73 │ … s3_client.create_bucket(Bucket=S3_MODELS_BUCKET_NAME)` RED;
line 227 `NoCredentialsError: Unable to locate credentials` RED. Then `ls -la artifacts` (extra) →
TERM(laptop/27: 229) RED. `▶ your turn`. On V4 a RED "create bucket" box appears **first** in the
chain, before the download, and the chain stops there.
SAY: Pause and run it. Ours stops right away: no credentials, at line 73 of cli.py, which creates the bucket. And the artifacts folder does not exist, so nothing was downloaded.

SHOW: CODE(cli.py: 70–88): lines 70–82 (create bucket) YELLOW, lines 84–88 (download) GREY; tag
`erratum`, chip "the README list skips this". Lines 79–82 (`BucketAlreadyExists`,
`BucketAlreadyOwnedByYou`) GREEN on "already exists". A second GREY chip on lines 79–80: "someone
else's name → 'already exists', then AccessDenied on upload · pick a unique name (README A:195–197)".
SAY: A small gap in the README: the code creates the bucket before it downloads anything, a step the list does not mention. With your keys, it creates the bucket, or reuses yours if it already exists.

SHOW: TRACKER A3 1 · extra · capture stub. A host strip types laptop/40's line 1 (extra; cut) →
TERM(laptop/40: 18–19 wrap, 21, 22 wrap, …, 293 wrap, …, 323–327 wrap); line 19 `[capture stub]
create_bucket(…) NOT sent` GREY; line 22 `Saved artifact at './artifacts/model-mobilenetv2_train_base_True.v1/1'`
GREEN; lines 323–327 `[capture stub] upload_file(…) NOT sent` RED with tag `extra · capture stub`.
V4's chain runs to the bucket and the PINK arrow stops at a RED wall "not sent".
SAY: To show what comes next, an extra: the same prepare function, with S3 replaced by a stub that sends nothing. The release zip downloads, the model is exported, and the stub stops the upload. Nothing reaches AWS.

SHOW: TRACKER A3 1 · extra. It types laptop/41's line 1 (extra; folds) → TERM(laptop/41: 12–20). On
V4, the GREEN `.keras` file unfolds into a folder: `saved_model.pb` (the graph), `variables/` (the
weights), `fingerprint.pb`, `assets/`; the label "named entry points · serving_default" sits inside
`saved_model.pb`, beside "the graph".
SAY: Here is what it made. A SavedModel is a folder: the graph and its named entry points in saved model dot P B, and the weights in a variables folder.

SHOW: TRACKER A3 1 · extra. CODE(cli.py: 101–117): lines 102–104 (`"1"  # SageMaker expects version
number`) YELLOW, 116–117 (`tarfile`, `arcname="1"`) GREEN. It types `tar tzvf
artifacts/model-mobilenetv2_train_base_True.v1/model.tar.gz` (extra) → TERM(laptop/42: 2–8); the
`1/` prefix YELLOW on every line. On V4, the folder slides into a sub-folder labelled `1`, then a
tarball wraps it; a GREY chip "TF Serving: <name>/<version>/".
SAY: The code puts it in a folder named 1, because TensorFlow Serving finds models by name, then version. The tarball holds that folder at its top.

SHOW: TRACKER A3 1 · extra. It types laptop/44's line 1 (extra) → TERM(laptop/44: 2–4); ` M Pipfile`
and ` M docker-shell.sh` YELLOW ("your two edits"), line 4 `.gitignore:33:artifacts/` GREY. V4's
bucket shows `s3://<bucket>/model-mobilenetv2_train_base_True.v1/model.tar.gz` in PINK (dashed:
"with your keys"); GOLD `cost_tag("the tarball in S3 · storage")`. A host strip types `aws s3 ls
s3://<your-bucket>/ --recursive` (extra; README A:185 "Verify the model.tar.gz was uploaded") with a
GREY chip "needs your account · no output shown". Fade to empty.
SAY: An extra git status shows your two edits, and Git ignores the artifacts folder. In your account, the tarball now sits in S3, and storage bills while it exists.

---

## S07 · --deploy: model, endpoint configuration, endpoint — `s07_deploy.py` · `ModelToEndpoint`

SHOW: TRACKER A3 2. LECTURE 15 · 11–12. CODE(cli.py: 151–159). **V5 `ThreeObjects` built from S01's
preview**: the three slots of S01 come back (artifact, container, machine). On "describes", the
artifact and container slots **Transform** into the two slots of a GREY-dashed **TensorFlowModel**
card as lines light: line 152 `model_data=` → a PINK S3 URI in "artifact"; line 154
`framework_version="2.13"` → a TEAL "TF Serving 2.13" in "container"; on "role", line 153 `role=` →
the BLUE badge drops into a third slot. The machine slot waits, dimmed, on the right. A GREY caption
"a description in Python · nothing in AWS yet".
SAY: Step 2: deploy. Remember the three pieces from the start. In code, it first describes a TensorFlow model: the tarball in S3 and the serving container, plus the role. Nothing exists in AWS yet.

SHOW: LECTURE 15 · 12. Above the model card a GREY-dashed box "Model Registry (the lecture)" with a
GREY arrow down to the card, chip "README: 'Model Registry' · code: a plain Model"; tag `erratum`.
The S02 mini-legend chip "Model Registry → SageMaker Model" sits in the lower right for this block.
SAY: The lecture uploads to a model registry here. Both READMEs say model registry too, but the code creates a plain model in SageMaker.

SHOW: The registry box fades. The TEAL container slot zooms: "AWS prebuilt TensorFlow Serving image ·
picked from framework_version" (no URI). Two chips: GREEN "exported by TF 2.18", TEAL "served by
2.13", both `at the time of recording`; on "step 3", a GREY-dashed arrow points ahead: "checked
locally in step 3". (No stand-in log here: S08 introduces the stand-in.)
SAY: You never write an image name: the SDK picks the AWS TensorFlow Serving image from framework version 2.13. Our model was exported by TensorFlow 2.18. In step 3, a local check shows that Serving 2.13 loads it.

SHOW: TRACKER A3 2. CODE(cli.py: 163–174): lines 164–167 (timestamped `endpoint_name`) YELLOW, lines
169–170 (`initial_instance_count=1`, `instance_type="ml.m5.xlarge"`) GOLD. On "creates", line 168's
`deploy(` lights and the three AWS objects appear in order: the dashed TensorFlowModel card turns
into a solid BLUE **Model** card ("the model in SageMaker"); the waiting machine slot **Transforms**
into an **endpoint configuration** card (variant `AllTraffic` · instance type · count 1 · weight 1,
chip "shape from the part 2 Lambda") and an **endpoint** address plate with a BLUE machine sliding
under it (`ml.m5.xlarge × 1`). The plate's name ends `-endpoint-<timestamp>`.
SAY: Then deploy, with one instance of type M L M5 extra large, under a name with a timestamp. That one call creates all three: the model in SageMaker, an endpoint configuration, which names the machine and the model, and the endpoint, the address you call.

SHOW: TRACKER A3 2. V5 shrinks to the top. Container prompt; it types `python cli.py --deploy` →
TERM(laptop/28: 52, 58, …, 78, 83, …, 308); line 83 `❱ 168 │ predictor = tensorflow_model.deploy(` RED;
line 308 RED. `▶ your turn`. Then a GREY chip "with your keys · 5–10 min (A:127) · the endpoint name ·
endpoint_config.json written · no output shown", and a second GREY chip "fails? the endpoint's
CloudWatch logs · the tarball in S3 · README A:184–186".
SAY: Pause and run python cli.py dash dash deploy. Ours stops at line 168, the deploy call: no credentials. With yours, the README says 5 to 10 minutes, then it prints the endpoint name and saves it in endpoint config dot JSON.

SHOW: V5 returns: the GOLD meter under the machine starts; a PINK request lane above stays empty;
the meter keeps rising. A GREY-dashed L14 card beside it: a Cloud Run dashed instance blinking off
to zero. Labels: BLUE "serverless = no server to manage"; RED-struck "scale to zero". GOLD
`cost_tag("endpoint · ml.m5.xlarge · 24/7 while it exists")`.
SAY: The lecture calls this serverless, meaning no server for you to manage. It is still one machine, billing around the clock, even with zero traffic. Unlike Cloud Run in lecture 14, this endpoint, as the code creates it, does not scale to zero.

SHOW: LECTURE 15 · 16–17. A two-column card (our layout): left BLUE "managed model serving ·
SageMaker endpoint / Vertex AI online prediction", each feature writing in on its phrase: "deploy a
model directly", "versioning", "A/B variants", "monitoring"; then the right column GREY-dashed "run
any container · Cloud Run (L14)": "you containerize", "you configure", "you add monitoring".
SAY: The lecture compares two ways to serve. A model endpoint deploys a trained model directly, with versioning, A B testing and monitoring available. A general container service like Cloud Run runs anything, and you build the rest yourself.

SHOW: LECTURE 15 · 16–17 (held). A rule-of-thumb line writes under the card; on "Here", a small V5
plate slides in under the left column and three GREY chips "available · not used here" fly from the
features onto it: "1 instance", "1 variant", "no monitoring". Fade to empty.
SAY: Its rule of thumb: an endpoint to serve a trained model, a container service when the model is one part of a larger app. Here, those features go unused.

---

## S08 · --predict: 150,528 numbers per photo — `s08_predict.py` · `AskTheEndpoint`

SHOW: TRACKER A3 3. Container prompt; it types `python cli.py --predict` → TERM(laptop/29: 52–54,
60, 61–63, …, 73–75); line 53 `Error: endpoint_config.json not found` RED with chip "no deploy ·
no file"; line 63 `'model-mobilenetv2-train-base-True-v1-endpoint'` GREY with chip "fallback name";
line 62 RED. `▶ your turn`. A GREY chip "fails with keys? the endpoint must be InService · README
A:188–191".
SAY: Step 3: python cli.py dash dash predict. Ours finds no endpoint config dot JSON and falls back to a default name. It picks five photos and fails five times: unable to locate credentials. Pause and run yours.

SHOW: LECTURE 15 · 13. V3's left pipe returns: one JPEG icon, the two gears, the TEAL-outlined cube
"224 × 224 × 3" with three edge labels, the PINK wire to the endpoint. A YELLOW card.
SAY: Each try would send one photo. The client resizes it to 224 by 224, with 3 color channels. How many numbers travel to the endpoint for that one photo?
PONDER(8 s, "--predict resizes one photo to\n224 × 224 with 3 color channels.\nHow many numbers travel to the\nendpoint for that one photo?")

SHOW: LECTURE 15 · 13 (held). The cube's counter runs up to **150,528** (YELLOW); the cube turns into
a long PINK ribbon of text digits ("0.4313725…, 0.4352941…, …") labelled `{"instances": [ … ]}` with
a chip "JSON text · a few MB per photo". A small GREY-dashed alternative under it: "bytes-in
signature (the trainer, part 2) · sends the JPEG itself".
SAY: 224 times 224 times 3: one hundred fifty thousand, five hundred twenty-eight floats. Python writes each one as text in JSON, so a few megabytes per photo. A signature that takes bytes would send the JPEG itself.

SHOW: CODE(cli.py: 36–43) + CODE(cli.py: 230–234): lines 41–42 (the four-label map) YELLOW; line
232 `np.argmax(prediction)` PURPLE. The answer shape `{"predictions": [[p0, p1, p2, p3]]}` draws as
four bars; the tallest gets an arrow to its index and the map entry.
SAY: The answer is a list of four probabilities. The code takes the largest with arg max and looks it up: 0 parmigiano, 1 gruyere, 2 brie, 3 gouda.

SHOW: TRACKER A3 3 · extra · local stand-in, not SageMaker. A host terminal (prompt
`student@laptop:~/model-deployment-aws$`, chip "extra · a second terminal on your laptop") types
`docker pull tensorflow/serving:2.13.1` (extra) → TERM(laptop/45: 26–27), then laptop/46's line 1
(extra; folds) → TERM(laptop/46: 5 from "NodeDef mentions attribute debug_name" cut, 7 from
"SavedModel load" cut, 9 from "Successfully loaded", 15 from "Exporting HTTP/REST", 20–21); line 5
ORANGE with chip "ignored attribute · loads anyway" (S07's "checked in step 3"), line 7 GREEN,
`"state": "AVAILABLE"` GREEN. A TEAL box "tensorflow/serving 2.13 (public image)" beside a
GREY-dashed "the AWS serving image runs TF Serving too"; tag on the panel.
SAY: To see a real answer, we use an extra local stand-in, not SageMaker. The AWS serving image runs TensorFlow Serving, so we started the public Serving 2.13 image on our export. It loads version 1.

SHOW: TRACKER A3 3 · extra · local stand-in, not SageMaker. It types laptop/47's line 1 (extra;
cut) → TERM(laptop/47: 21 wrap, 23–26, 28–31); line 21 `[capture stand-in] endpoint … -> local
TensorFlow Serving` GREY; the four numbers of each `Result` line under four small bars.
SAY: Then the same predict function sends the same JSON to it. Brie comes back brie, and gruyere comes back gruyere, four numbers each.

SHOW: TERM(laptop/47: 33–36) prints next; line 33 `Image: data/parmigiano-1.jpg` YELLOW, line 36
`Label:    brie` RED, the 0.977 bar towering. A GREY chip "released model · metrics file: accuracy
0.724 (digest §1)".
SAY: And parmigiano comes back brie, at 98 percent. That is a real mistake of the released model. Its own metrics file reports about 72 percent accuracy.

SHOW: The hook returns: RECORDED(expected/md-predict-readme.txt: 7–8, 12–15) above, the stand-in
lines below; "3" and "4" again. Between the two panels, V5's artifact slot (small): on "different
artifact", an older GREY-dashed "3-class model · 0 = gouda" card slides out of the slot and the GREEN
"4-class model (v1 release) · 0 = parmigiano (cli.py:42)" card slides in; the top panel dims as the
bottom one lights; tag `erratum`.
SAY: Now the opening puzzle. Same code, different artifact: the README output came from an older model, with three classes and another label order. A small gap: expect four numbers, and index 0 is parmigiano.

SHOW: TRACKER A3 3 · extra. It types `docker rm -f cheese-serving` (extra) → TERM(laptop/48: 2). The
TEAL stand-in box dissolves. Fade to empty.
SAY: An extra command removes the stand-in. It never touched AWS.

---

## S09 · --delete: turn off the meter — `s09_delete.py` · `TurnOffTheMeter`

SHOW: TRACKER A4 1 (tracker changes: "README A › Clean Up", 3 dots). LECTURE 15 · 11, 41. V5's
endpoint with its GOLD meter running large; a GOLD word card "DELETE" (no image) stamps beside it.
Then a GREY chip "three ways · pick one" (README A:154, 159, 166 are alternatives), and
CONSOLE("SageMaker › Endpoints", A:154-157): a list row "your endpoint" selected, a **Delete** button
pulses (no `▶ your turn` here: it sits on way 3).
SAY: The lecture warns that an endpoint costs money while it is up, and the slides shout one word: delete. The README gives three ways. Any one stops the endpoint, but only the third also removes the tarball. Way 1, the console: SageMaker, Endpoints, select yours, Delete.

SHOW: TRACKER A4 2. Full-width terminal, prompt `student@laptop:~/model-deployment-aws$`, GREY chip
"in the container, or a second terminal on your laptop" (the Part A image has `aws`, laptop/25:39). A
README card (`README.md · lines 161–163`, chip "A") shows the three lines. It types `aws sagemaker
delete-endpoint --endpoint-name <your-endpoint-name>` → TERM(laptop/31: 2–3); RED; the `<` and `>`
ring RED with a chip "the shell reads < as a redirection"; tag `erratum`.
SAY: Way 2 gives three AWS CLI commands. Typed exactly as written, the first one is a shell error: the angle brackets are placeholders, and the shell takes them as a redirection.

SHOW: TRACKER A4 2 · extra. It types `aws sagemaker delete-endpoint --endpoint-name
cheese-endpoint-placeholder` (extra) → TERM(laptop/32: 3 wrap) RED. TRACKER A4 2. Then it types the
README's other two lines as written, `aws sagemaker delete-endpoint-config --endpoint-config-name
<your-endpoint-config-name>` and `aws sagemaker delete-model --model-name <your-model-name>`, each
with its brackets struck GREY and a GREY chip "your own name · needs your account · no output
shown"; a chip "names: `aws sagemaker list-endpoint-configs` · `aws sagemaker list-models`". Three
numbered chips: "1 endpoint · 2 endpoint config · 3 model".
SAY: A small gap: type your own names, without brackets. Ours then fails: no credentials. Delete in this order: the endpoint, then its configuration, then the model.

SHOW: TRACKER A4 3. Container prompt; it types `python cli.py --delete` → TERM(laptop/30: 52, …,
74, 79, …, 260); line 79 `❱ 270 │ for page in paginator.paginate():` RED. `▶ your turn` (chip "the
only way that also removes the tarball", README A:171–174). CODE(cli.py: 255–260 + 283–293) beside it
in a strip. **V5's clean-up beat**: the endpoint goes first (the meter stops), then the configuration
card, then the Model card, then the tarball in the bucket.
SAY: Way 3: python cli.py dash dash delete stops at its first SageMaker call. Pause and run it. With keys, it deletes the endpoint named in the JSON file. Then come matching configurations and the model, by naming convention, then the tarball in S3.

SHOW: On V5, two endpoint plates side by side, both with GOLD meters: an older `…-endpoint-<t1>`
and a newer `…-endpoint-<t2>`; a GREY card `endpoint_config.json` sits between them with no arrow
yet (CODE(cli.py: 163–167) small). A YELLOW card.
SAY: Each deploy makes a new endpoint with a new timestamp, but the JSON file keeps only the last name. You ran deploy twice, then delete once. How many endpoints still bill?
PONDER(6 s, "You ran --deploy twice,\nthen --delete once.\nHow many endpoints still bill?")

SHOW: The GREY `endpoint_config.json` card draws its arrow to `<t2>` only. The newer plate and its
meter vanish; the older one keeps its GOLD meter running, RED ring
"forgotten". A strip types `aws sagemaker list-endpoints` with a GREY chip "extra · needs your
account · no output shown"; a GREY README card (`README.md · line 176`): "Make sure to confirm in
your AWS console to avoid charges." A small GREY chip on the older plate: "its config and model are
already gone · it still bills" (cli.py:268–286).
SAY: One. Delete removes only the endpoint the file names. The older one keeps running. Check with aws sagemaker list endpoints, and confirm in the console.

SHOW: Everything clears to **V5's empty endpoint slot** with the GOLD meter stopped at its last
value. Under it, the four GREY stage tiles of S01 fade in, each with a small person at a terminal. A
YELLOW question card: "four commands by hand for one model · who runs all four stages, in order,
every time?" Fade to empty. End of part 1.
SAY: That is part 1. You ran four commands by hand to deploy one model. The Cheese App has four stages before that. Who runs all of them, in the right order, every time?

---

## S10 · From four terminals to one workflow — `s10_workflow.py` · `FourTerminals`

SHOW: No tracker yet. LECTURE 15 · 19–21. **V6 `ManualToPipeline`**: slides 20–21 redrawn: four tiles
(Data Collector, Data Processor, Model Training, Model Deploy), each with a GREY person at a "CLI"
under it, two-headed arrows. Headline "How do we execute these steps?" types, then rewrites to "Can
we automate this flow?".
SAY: Part 2. The lecture draws the problem: four stages, each run by a person at a terminal. How do we execute these steps? And can we automate this flow?

SHOW: LECTURE 15 · 21. One BLUE "SageMaker Pipelines" box slides in under the tiles and the four
people fade; a GREY-dashed "Vertex AI Pipelines · Kubeflow" box sits beside it with a GREY "≈".
README B card (`README.md · lines 4–7`) shrinks into four one-line chips on the tiles. The S02
mini-legend chip "Vertex AI Pipelines (Kubeflow, KFP DSL) → SageMaker Pipelines (SDK step classes)"
sits in the lower right for this block.
SAY: The answer is an orchestrator. The lecture uses Vertex AI Pipelines, on Kubeflow. This tutorial uses SageMaker Pipelines, the same idea of managed steps in a graph.

SHOW: LECTURE 15 · 22. A duty card with ticks for this repo, one per phrase: "order ✓ (references)",
"repeatable ✓ (caching, same definition)", "resources ✓ (instance type per step)", "monitoring ✓
(Studio's graph)", "scheduling ✗ → L23" (GREY dashed). Then LECTURE 15 · 24 replaces the tag for a
GREY chip "managed · no cluster to run".
SAY: Workflow management runs the steps in order, makes a run repeatable, gives each step its machine, and shows it. This repo covers those four. Scheduling waits for lecture 23. And it is managed: no cluster for you to run.

SHOW: TRACKER B1 1 (tracker appears: "README B › Setup Environments", 9 dots). Prompt
`student@laptop:~$`. It types `git clone https://github.com/dlops-io/ml-workflow-aws.git` (extra:
its spelling) → TERM(laptop/50: 2); `cd ml-workflow-aws`; TRACKER B1 1 · extra: `git log -1
--format='%H %ci %s'` (extra) → TERM(laptop/51: 2), `f165c6e1…` YELLOW; `tree -a -I .git --dirsfirst .`
(extra) → TERM(laptop/52: 7–8, 16, 24, 39, …, 52); the four `src/` folders YELLOW, three with a GREY
chip "stage" and `workflow` with a BLUE chip "the orchestrator". `▶ your turn`.
SAY: Setup, step 1: clone ml workflow AWS. Our git clone is extra again. An extra tree shows four folders under source: three stages and the workflow.

SHOW: TRACKER B1 2–5 (the dots tick as each form fills). One form on screen at a time, each
**Transforming** into the next on its phrase: CONSOLE("AWS services", B:18-24): "SageMaker AI → Set
up for single user (Quick setup)", "SageMaker Unified Studio → Create domain" (on "watch the
pipeline", a small GREY-dashed preview of S15's graph flickers inside the domain row), "S3", "ECR",
"Lambda"; → CONSOLE("S3 › Create bucket", B:26-30): `cheese-app-ml-workflow-demo` "[REPLACE WITH YOUR
BUCKET NAME]"; → CONSOLE("IAM › Create user", B:35-43): `ml-workflow-user`, four ORANGE policy chips.
(The cost tag comes in the next block.)
SAY: Steps 2 to 5 are console work: quick setup for SageMaker AI, and a Unified Studio domain, where you will watch the pipeline. Then your bucket, and a user named ml workflow user, with four policies.

SHOW: TRACKER B1 5. CONSOLE("ml-workflow-user › Security credentials", B:45-49): "Create access key ·
Command Line Interface (CLI)" → **Download .csv file** (a GREY `.csv` icon falls to the laptop; no
values drawn). GOLD `cost_tag("quick setup · Studio domain · bucket · check at clean-up")` writes in
on "stay in your account" and pulses once.
SAY: Create an access key for the command line, and download the C S V file. Quick setup and the Studio domain stay in your account: check them when you clean up.

SHOW: TRACKER B1 6. A README card (`README.md · lines 51–53`, chip "B"): `brew install awscli` /
`sudo snap install aws-cli --classic`, chip "ours: AWS CLI 2.34.63 from the laptop's packages ·
at the time of recording". TRACKER B1 7. It types `aws configure` → TERM(laptop/55: 2–5); the two
PLACEHOLDER values ORANGE with chip "obviously fake · capture only"; `[us-east-1]` and `[json]`
kept with Enter; a GREY chip "replaces part 1's default profile · clean up part 1 first". TRACKER
B1 7 · extra: `aws configure list` (extra) → TERM(laptop/56: 4–6), `****************_KEY` GREY.
SAY: Steps 6 and 7: install the AWS CLI, then aws configure, and paste the two values from the C S V. From here on, we typed obviously fake placeholders, so AWS answers with real errors.

SHOW: TRACKER B1 8. It types `aws sts get-caller-identity` / `aws s3 ls` → TERM(laptop/57: 4 wrap, 6
wrap); both RED. A small GREY chip quoting TERM(laptop/53: 4 to "Unable to locate credentials"):
"before configuring: no keys at all". A GREEN chip "with your keys: your account · your buckets".
`▶ your turn`.
SAY: Step 8 tests the configuration. AWS itself rejects the fake token and the fake key. With yours, these print your account and your buckets. Don't go on until they do.

SHOW: TRACKER B1 9. CONSOLE("IAM › Roles", B:71-81): two roles, `CheeseAppSageMakerExecutionRole`
(three policies) and `CheeseAppLambdaExecutionRole` (two). **V1 reprise**: two BLUE badges now.
CODE(src/workflow/model.py: 26–28): line 28 `role_arn = f"arn:aws:iam::{account_id}:role/CheeseAppSageMakerExecutionRole"`,
the role name YELLOW, chip "found by name"; the `{account_id}` PINK. `▶ your turn` on the roles form.
Fade to empty.
SAY: Step 9 creates two roles: Cheese App SageMaker Execution Role, for every job, and Cheese App Lambda Execution Role. The code builds each A R N from your account number and the exact role name, so spell them exactly, and pause here.

---

## S11 · Collector and processor, by hand — `s11_collect.py` · `CollectAndClean`

SHOW: TRACKER B2 1 (tracker appears: "README B › Data Collector", 3 dots). Prompt
`student@laptop:~/ml-workflow-aws$`. It types `cd src/data-collector` → (no output). First
CODE(src/data-collector/docker-shell.sh: 10): `export S3_BUCKET_NAME="cheese-app-ml-workflow-demo"`,
the value YELLOW, tag `erratum`, chip "edit in all four: data-collector :10 · data-processor :10 ·
model-training :9–10 · workflow :8–9", `▶ your turn`. Then `sh docker-shell.sh` → TERM(laptop/54: 2)
RED, with a chip "captured before aws configure"; a second GREY chip on that line "our sh is not dash ·
on Ubuntu or Debian this check is skipped". CODE(src/data-collector/docker-shell.sh: 13–21) small:
lines 14–15 `aws configure get …` PINK; V1's drawer: a PINK arrow pulls the key out of `~/.aws` and
carries it as `-e AWS_ACCESS_KEY_ID` (lines 37–38); the arrow says it, no words needed.
SAY: Data collector, step 1. A small gap first: all four part 2 scripts name the bucket from the README, so put yours in each one. Then, in this folder, run sh docker-shell.sh. Without keys, the script stops itself: AWS not configured.

SHOW: TRACKER B2 1. It types `sh docker-shell.sh` again → TERM(laptop/60: 3 cut), `Building 40.4s`
with `at the time of recording`; the prompt `root@<id>:/app#`. Two GREY chips, one per phrase:
"builds linux/amd64 (line 31) · Apple silicon emulates it" and "Ubuntu/Debian: sh is dash · skips
the key check · run `bash docker-shell.sh`". `▶ your turn`.
SAY: With keys, it builds in 40 seconds and opens a root shell. Two notes. This script builds for A M D 64, which Apple silicon emulates. And on Ubuntu or Debian, sh is dash, which skips the key check, so run bash docker-shell.sh.

SHOW: LECTURE 15 · 34–36. **V7 `CallableImage` built** from CODE(src/data-collector/docker-entrypoint.sh: 1–8):
one TEAL image with a switch on its input. Line 4 `if [[ $# -eq 0 ]]` YELLOW: the switch; line 5
`exec bash` → a GREY "development · a shell (you are here)" branch; line 7 `exec "$@"` → a BLUE
"production · run the command, exit" branch. A GREY-dashed chip "the slide's version also logs in
gcloud · not here".
SAY: Why a shell? The entry point script has a switch. No arguments: it opens bash, development mode, where you are now. Arguments: it runs them and exits, production mode. The lecture calls that a callable container.

SHOW: TRACKER B2 2. It types `python cli.py --search --nums 10 --query "brie cheese" "gouda cheese"
"gruyere cheese" "parmigiano cheese"` (folds) → TERM(laptop/60: 22 wrap, 24, …, 117, 118, …, 182,
183, …, 340, 341, …, 610–611, 654 from "S3UploadFailedError" wrap); the four `Searching for:` lines
and the four `Done. Downloaded 10 images.` lines YELLOW; line 654's `(InvalidAccessKeyId)` RED. No
image, URL or site name on screen. Two GREY chips on the command: "type the four queries exactly ·
other names → KeyError in the processor" and "stuck on one cheese? Ctrl-C and run again".
`▶ your turn`.
SAY: Step 2: the search command, four cheeses, ten images each. It scrapes the web, writes four folders, zips them, and tries to upload raw dot zip. AWS rejects our fake key.

SHOW: TRACKER B2 3 · extra. It types `for d in /persistent/dataset/raw/*; do echo "$(ls "$d" | wc -l)
$d"; done; ls -l /persistent/dataset/raw.zip` (extra; folds) → TERM(laptop/60: 659–663 cut). A host
strip (`student@laptop:~/ml-workflow-aws/src/data-collector$`) types `ls -la ~; ls -la
~/persistent-folder/dataset` (extra) → TERM(laptop/61: 9, 13–14); line 9 `root root …
persistent-folder` ORANGE, chip "Docker made it · owned by root", and a GREY chip "rerun from
scratch: delete persistent-folder first (old data wins over the bucket)".
SAY: Step 3, check your bucket, cannot pass here. An extra listing shows 40 images on disk. On the laptop, a root-owned persistent folder appeared beside the clones.

SHOW: TRACKER B3 1 (tracker changes: "README B › Data Processor", 5 dots). It types `cd
../data-processor` (chip "exit the container first · this runs on your laptop") → (no output), `sh docker-shell.sh` → TERM(laptop/65: 50 cut, …, 71 cut) RED;
TRACKER B3 1 · extra: the swap `sed` (extra; folds) → TERM(laptop/66: 2–5), chip "fix 1 again"; a
GREY chip "no Pipfile.lock here · the build resolves at build time" (laptop/67:730–733 as one strip
line `Locking dependencies… ✔ Success!`). `sh docker-shell.sh` → prompt `root@<id>:/app#`. Typing
time short for `cd` and the rebuild, so the block does not drift long.
SAY: Data processor, step 1: the A R M 64 line fails again, and the same swap fixes it.

SHOW: TRACKER B3 2. It types `python cli.py --clean` → TERM(laptop/68: 30, 31, 34–35, …, 64, 107
from "S3UploadFailedError" wrap); line 30's four labels YELLOW; `Search Results: {}` GREEN with
chip "no duplicates among these 40"; line 107 RED. `▶ your turn` on the `python cli.py --clean`
line.
SAY: Step 2: python cli.py dash dash clean. A duplicate finder checks each label, finds none among these 40, and the upload of clean dot zip fails. Pause and run it.

SHOW: TRACKER B3 3 (chip "check your bucket · cannot pass here"), then TRACKER B3 4. It types `python
cli.py --prepare` → TERM(laptop/68: 124, 126–127, 129, 133, 178 from "S3UploadFailedError" wrap);
lines 126–127 YELLOW, 129 and 133 GREEN. TRACKER B3 5 · extra: `ls -la /persistent/dataset; ls -la
/persistent/dataset/tfrecords` (extra) → TERM(laptop/68: 192–193).
SAY: Steps 3 and 4: check your bucket, then dash dash prepare. All 40 images split into 32 for training and 8 for validation, in two real TFRecord files. The upload fails again. Step 5 finds them only on disk.

SHOW: LECTURE 15 · 37. Slide 37's duty cards redrawn (our pastel-free style): "Data Collector ·
download images, upload"; "Data Processor · verify, de-duplicate, convert to TFRecords", each with a
GREEN tick "AWS code does this". CODE(src/data-processor/tfrecords.py: 10–17): lines 12–15 (the
four folder names → 2, 3, 1, 0) YELLOW, arrows back to the four query strings. Fade to empty.
SAY: The duty cards from the lecture match: download, then verify, remove duplicates and convert to TFRecords. And the four labels are just the folder names: your search queries, so type them exactly.

---

## S12 · Train locally, sign the model — `s12_train.py` · `TrainLocally`

SHOW: TRACKER B4 1 (tracker changes: "README B › Model Training", 5 dots). It types `cd
../model-training` (chip "exit the container first · this runs on your laptop"), `sh docker-shell.sh` → TERM(laptop/70: 53 cut) RED; the swap (extra) →
TERM(laptop/71: 3–5); `sh docker-shell.sh` → TERM(laptop/73: 16 cut, 22–23); line 16 `RUN pipenv
sync` GREEN with chip "from its committed lock · sagemaker 2.250.0 · no pin needed" (laptop/73:29).
Prompt `(app) app@<id>:/app$`.
SAY: Model training, step 1. Same A R M 64 line, same swap. This image installs from its committed lock, with SageMaker version 2, so it needs no pin.

SHOW: TRACKER B4 2. It types `python -m package.trainer.task --epochs=1 --batch_size=4
--bucket_name=cheese-app-ml-workflow-demo` (folds; the bucket value ringed YELLOW with chip "your
bucket") → TERM(laptop/73: 95, 99 cut, 103, …, 110, 117, 119, …, 132 cut, 134); line 103 `TFRecords found at /persistent/dataset/tfrecords` PINK with an arrow
back to S11's processor ("through the shared folder"); line 119 `dense_1 (Dense) … (None, 3)` RED;
line 132 with a GREY chip "one epoch on 32 photos · not a result". `▶ your turn`.
SAY: Step 2, local training. TensorFlow 2.20 on the CPU finds the TFRecords from the processor, through the shared folder. Look at the last layer: three outputs. One epoch runs. Its accuracy means nothing yet.

SHOW: TERM(laptop/73: 142–143, 146) prints next; line 146 `PermissionError: [Errno 13] Permission
denied: '/persistent/model'` RED. Two numbered YELLOW chips "fix A", "fix B" appear empty.
SAY: Then saving fails: permission denied, slash persistent slash model. Pause here for two small fixes.

SHOW: CODE(src/model-training/package/trainer/task.py: 66–69): line 68 `num_classes = 3` RED → GREEN
`4`; tag `erratum`. A small picture: four label folders, but only three output bars; gouda's bar
missing. Chip "fix A".
SAY: First, line 68 says three classes, while the data has four labels, so gouda gets no target. Change it to 4.

SHOW: TERM(laptop/61: 9) as a one-line strip (`root root … persistent-folder`, ORANGE) beside a TEAL
container whose user badge says `app · uid 1000`; a RED lock between them. Chip "fix B": "create
`persistent-folder` yourself before the first docker-shell.sh · or `sudo chown -R $USER
../../../persistent-folder` · works when your uid is 1000 (`id -u`) · Docker Desktop on a Mac: not
needed". Tag `erratum`. On "Exit", a host strip (`student@laptop:~/ml-workflow-aws/src/model-training$`)
types `sudo chown -R $USER ../../../persistent-folder`, then `sh docker-shell.sh` and the step 2
training command again, both with a GREY chip "after the fixes · not captured"; `▶ your turn` on the
strip.
SAY: Second, on Linux, Docker created the persistent folder as root, and this container runs as the app user. Exit, and on your laptop change its owner with the chown command on the card. On a fresh clone, create the folder yourself before the first docker-shell.sh. Then run step 2 again. Docker Desktop on a Mac avoids this.

SHOW: CODE(src/model-training/package/trainer/task.py: 303–312): line 310 `os.path.join("/persistent",
"model", "1")` GREEN, line 307 `os.path.join(sm_model_dir, "1")` BLUE; GREY chip "the save after
the fixes was not captured". On "on your laptop", a PINK arrow draws from line 310 to a GREY laptop
folder `persistent-folder/model/1`; on "inside a training job", a second arrow draws from line 307 to a
BLUE job box. A caption for the expected end state: "ls -laR /persistent/model → a 1/ folder with
saved_model.pb".
SAY: It would write to slash persistent slash model slash 1: the persistent folder on your laptop, or the SageMaker model folder inside a training job.

SHOW: LECTURE 15 · 14. **V3's right pipe, now real**: S05's right pipe returns small, and the code grows
out of it (the code's first full showing): CODE(src/model-training/package/trainer/task.py: 276–289) +
CODE(…: 292–301) in two short panels, the three slide-14 callouts lighting in turn. A
README card (`README.md · line 7`, chip "B"): "Model Deploy: Updates the model signature …" with a
GREY arrow re-pointed to "Model Training"; tag `erratum`.
SAY: Just before the save sits the signature change from the lecture: decode, convert, resize, inside the model. A small slip: the README gives this job to model deploy. The trainer does it.

SHOW: TRACKER B4 3. It types `sh package-trainer.sh` → TERM(laptop/73: 150–156, 157 to
"(InvalidAccessKeyId)"); line 157 RED. CODE(src/model-training/package-trainer.sh: 1–4) small: line 4
`aws s3 cp … cheese-app-trainer.tar.gz` PINK. A YELLOW chip "after fix A · the tarball carries it".
GOLD `cost_tag("trainer tarball in S3")`.
SAY: Step 3: sh package-trainer.sh packs the package folder and copies it to S3. The tar file is real. The upload fails on our fake key.

SHOW: TRACKER B4 4. It types `python cli.py --train` → TERM(laptop/73: 163, …, 313–314); lines
313–314 RED. CODE(src/model-training/cli.py: 53–60 + 73–74): `instance_type="ml.m5.xlarge"`,
`framework_version="2.13"`, `py_version="py310"`, then `fit(…, wait=False)` YELLOW with chip "returns
at once". GOLD `cost_tag("training job · ml.m5.xlarge · while it runs")`. LECTURE 15 · 37: a small
duty card "Model Training · train, save the model" beside the code, with a GREY chip "the AWS
trainer also signs the model"; it fades with the block.
SAY: Step 4: python cli.py dash dash train. It asks AWS who you are, to build the role A R N, and stops there. With keys, it starts a training job on M L M5 extra large, and returns at once.

SHOW: TRACKER B4 5. CONSOLE("SageMaker AI › Training › Training jobs", B:141-145): one row
`cheese-…` (the README's prefix only) with a status chip "InProgress" drawn GREY-dashed
(`illustration`). Fade to empty.
SAY: Step 5: watch it in the console, under Training, then Training jobs. Its name starts with cheese.

---

## S13 · Build and push: your own registry — `s13_push.py` · `PushToECR`

SHOW: TRACKER B5 1 (tracker appears: "README B › Build & Push", 11 dots, all dim). A README card
(`README.md · line 153`, chip "B"): "This step has already been done for this tutorial." Beside it
CODE(src/workflow/cli.py: 34–36): `{ACCOUNT_ID}.dkr.ecr.{AWS_REGION}…/cheese-app-data-collector:latest`,
`{ACCOUNT_ID}` YELLOW with chip "your account"; tag `erratum`. Two TEAL image boxes march toward a
BLUE "your ECR" shelf. The S02 mini-legend chip "Artifact Registry → ECR" sits in the lower right for
this block.
SAY: Build and push. The README says this step has already been done for you. A small gap: the workflow code pulls both images from the ECR registry of your own account, so you push them yourself, once each.

SHOW: LECTURE 15 · 34. Slide 34's three steps as three numbered GREY cards: "1 make the container
callable ✓ (S11)", "2 build and push to a registry the platform can pull" YELLOW, "3 describe the
DAG (S15)". The tag fades with the cards.
SAY: That is the second step the lecture gives for your own containers: push the images to a registry the platform can pull from.

**Registry route (the S13 trunk, under blocks 3–6; commands stay in a 3-row strip at the bottom,
never half-width):** a TEAL image cube on the GREY laptop → PINK arrow up to a GREY-dashed "Docker
Hub" shelf (B5 1–3) → back down (B5 5 pull) → on "tag", a second **name label**
`<account>.dkr.ecr.us-east-1…/cheese-app-…:latest` clips onto the *same* cube (the cube does not
duplicate) → PINK arrow into the BLUE "your ECR" shelf (B5 9). The tracker dots tick along the route.

SHOW: TRACKER B5 1–3. Registry route: the cube rises to the Docker Hub shelf. A 3-row strip, prompt
`student@laptop:~/ml-workflow-aws/src/model-training$`: it types `cd ../data-collector` (chip "exit
the container first · these run on your laptop"), and the prompt becomes
`student@laptop:~/ml-workflow-aws/src/data-collector$`. It types, one under another, as the README
writes them: `docker login -u <USER NAME> -p <ACCESS TOKEN>`, `docker
build -t <USER NAME>/<IMAGE_NAME> -f Dockerfile .`, `docker build -t <USER NAME>/<IMAGE_NAME>
--platform=linux/amd64/v2 -f Dockerfile .` (chip "M1/2 Macs"), `docker push <USER NAME>/<IMAGE_NAME>`;
GREY chip "needs your Docker Hub account · no output shown". On "push", `-p <ACCESS TOKEN>` rings
ORANGE with chip "lands in your shell history · prefer --password-stdin" (on screen only); on "A M D
64", the `amd64/v2` flag YELLOW, chip "SageMaker runs amd64". A GREY chip "extra · amd64 image already
local? `docker tag cheese-app-data-collector \"$ECR_URI\"` skips Docker Hub" (not for an Apple-silicon
processor image).
SAY: Steps 1 to 3 go through Docker Hub: log in, build, push. The Mac line builds A M D 64, because SageMaker runs that.

SHOW: TRACKER B5 4. It types the five README `export` lines plus B:198's `echo` (lines 1–6) →
TERM(laptop/80: 7–8, 10 wrap, 11); lines 7–8 `not a valid identifier` RED; line 10 RED; line 11
`ECR URI: .dkr.ecr.us-east-1…` with the leading `.` ringed RED. `▶ your turn`.
SAY: Step 4 sets five variables. Pasted exactly as written, the first line prints two errors, because export rejects the bracket note, though the region is still set. The account lookup fails on our fake key, and the URI starts with a dot.

SHOW: The README's line 169 `export REGION=us-east-1 [YOUR DEVELOPMENT REGION]` shown alone; the
bracket part GREY-struck, `us-east-1` GREEN; tag `erratum`. A RED chip "URI starts with '.' → account
lookup failed → fix your keys".
SAY: So paste only the value, us-east-1. And if your URI starts with a dot, the account lookup failed: fix your keys first.

SHOW: TRACKER B5 5. Registry route: the cube comes back down. It types `docker pull
<YOUR_DOCKER_HUB_USERNAME>/$REPO:$TAG` (no output panel).
TRACKER B5 6. It types laptop/81's line 1 (extra; chip "our capture re-sets the two variables") and
`aws ecr create-repository --repository-name "$REPO" --region "$REGION" || true` → TERM(laptop/81: 4
wrap) RED; a GREY chip `[exit 0]` with "|| true hides it" ORANGE.
SAY: Step 5 pulls your image. Step 6 creates the repository, and the or true at the end hides the error: the command exits with zero.

SHOW: TRACKER B5 7–11, dots ticking as each is typed; registry route: on "tag", the ECR name label
clips onto the same cube, and on "push" the cube rides the PINK arrow into the BLUE "your ECR" shelf. `aws ecr get-login-password --region "$REGION" \`
/ `| docker login --username AWS --password-stdin "$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com"`; `docker
tag <YOUR_DOCKER_HUB_USERNAME>/$REPO:$TAG "$ECR_URI"`; `docker push "$ECR_URI"`; `aws ecr list-images
--repository-name "$REPO" --region "$REGION" --output table`; `echo "ECR URI: $ECR_URI"`; GREY chip
"needs your account · no output shown". A GREY chip "on your laptop · the workflow container has no
docker (S14)". A README card (`README.md · lines 201–203`): "Repeat for both images"; under it a
host strip types `cd ../data-processor` and `export REPO=cheese-app-data-processor` (README B:171's
comment), chip "then steps 2–11 again". GOLD `cost_tag("ECR storage · two images")`. Fade to empty.
SAY: Steps 7 to 11 log Docker in to ECR, tag the image, push it, list it, and print the URI. Tag only adds a second name to the same image. Run them on your laptop, not in the workflow container, which has no docker command. Then repeat for the processor image.

---

## S14 · The workflow container and one processing job — `s14_shell.py` · `WorkflowShell`

SHOW: TRACKER B6 1 (tracker appears: "README B › Automate Collector", 3 dots). It types `cd
../workflow` (chip "exit the container first · this runs on your laptop"). **The lock that never
boards (picture):** two GREEN file cards, `Pipfile` and `Pipfile.lock · 2.250.0`, sit on the GREY
laptop. A TEAL image wall with a PINK `ADD` arrow (the Dockerfile line `40:ADD --chown=app:app
Pipfile /app/` as a one-line strip, laptop/87: 3) lets only `Pipfile` through; the lock bounces off.
Inside, a PURPLE "resolver" arrow drops **V2**'s dot at 3.29 (ORANGE). A GREY chip "before your first
sh docker-shell.sh here".
SAY: Automate the data collector, step 1, in the workflow folder. Before you run sh docker-shell.sh, the star problem returns. A lock is committed, but the Dockerfile copies only the Pipfile, so the build would resolve version 3.

SHOW: TRACKER B6 1 · extra · check. One terminal strip: laptop/85's line 1 (extra · check) →
TERM(laptop/85: 10) `sagemaker==3.29.0` RED, then the build strip TERM(laptop/89: 9334 from
"Pipfile.lock not found") RED (laptop/86 is not shown: it repeats the RED point). TRACKER B6 1 ·
extra: the fix `sed … && git diff Pipfile` (extra) → TERM(laptop/88: 10–11), `▶ your turn`. V2's dot
jumps from 3.29 back behind the GREEN wall.
SAY: The checks show the imports failing. So make the same fix first: less than 3.

SHOW: TRACKER B6 1. It types `sh docker-shell.sh` → TERM(laptop/90: 24–27, 29 wrap, 30); prompt
`(app) app@<id>:/app$`. TRACKER B6 1 · extra: it types laptop/90's line 32 (extra) → TERM(laptop/90:
35, 37 to "aws-cli/2.39.4"); then line 38 (extra) → TERM(laptop/90: 44) `bash: docker: command not
found` RED. CODE(src/workflow/docker-shell.sh: 33–34) small: `-v /var/run/docker.sock…` GREY chip
"socket mounted · no docker program inside". `▶ your turn`.
SAY: Now run sh docker-shell.sh. The banner shows region and bucket, and the who am I check fails. Extras: SageMaker version 2 now, and no docker command. The socket is mounted, but no docker program is inside.

SHOW: LECTURE 15 · 32–33. Slide 32 redrawn: a GREY "You (Python)" box → a PURPLE "SDK" box (a
remote-control icon) → a BLUE "SageMaker" cloud. On "AWS machines run", small BLUE machines light up
in the cloud while the laptop stays still.
SAY: From here, the SDK is your remote control, as the lecture puts it. Your Python asks, and AWS machines run.

SHOW: TRACKER B6 2. It types `python cli.py --data_collector` → TERM(laptop/90: 53, 55, 60, …, 98–99
wrap); line 60 `❱  32 ACCOUNT_ID = sts_client.get_caller_identity()['Account']` RED; CODE(src/workflow/cli.py:
30–32) small with a chip "top of the file · runs at import". `▶ your turn`.
SAY: Step 2: python cli.py dash dash data collector. It stops at line 32, a lookup of your account at the top of the file, before the function even starts. Every flag of this CLI needs a working key at import time.

SHOW: TRACKER B6 2. CODE(src/workflow/cli.py: 52–59 + 63–80) in two short panels: `image_uri=DATA_COLLECTOR_IMAGE`
TEAL, `instance_type="ml.t3.medium"` GOLD, `entrypoint=["python3", "/app/cli.py"]` YELLOW; then
`arguments=[…]`, `wait=True`, `logs=True`. GOLD `cost_tag("Processing job · ml.t3.medium · while it
runs")`.
SAY: With keys, it builds a processor from your ECR image, on one M L T3 medium. Its entry point is python 3 with the collector cli.py. Then it runs the job with the search arguments, and waits, showing the logs.

SHOW: LECTURE 15 · 36. **V7 reprise**: the TEAL image with its switch; a BLUE arrow labelled
"SageMaker" flips the switch and plugs `python3 /app/cli.py` + the job arguments into the production
branch; the
machine wears the BLUE `CheeseAppSageMakerExecutionRole` badge, and a GREY key card bounces off the
cloud border ("your key stays home").
SAY: This is production mode. SageMaker puts its own command in front of the arguments. Same image, same cli.py, on a machine you never log in to. The job acts as the role, not with your key.

SHOW: TRACKER B6 3. CONSOLE("SageMaker AI › Processing › Processing jobs", B:224): one row
`cheese-app-data-collector-…` (the prefix from `cli.py:61` only), status chip GREY-dashed. Fade to
empty.
SAY: Step 3: watch it under Processing, then Processing jobs.

---

## S15 · A pipeline drawn by references — `s15_pipeline.py` · `PropertyDAG`

SHOW: TRACKER B7 1 (tracker appears: "README B › SageMaker Pipelines", 3 dots, dim). LECTURE 15 ·
28–29. Two columns: GREY-dashed "the lecture · KFP DSL": `@dsl.component` → `.output` → "compile →
YAML"; BLUE "this tutorial · SageMaker SDK": "step classes" → "property references" → "JSON
definition". A GREEN chip spanning both: "plain Python".
SAY: Now the whole pipeline. The slides write steps in the Kubeflow D S L, wired by dot output and compiled to YAML. Here: SageMaker step classes, property references and JSON.

SHOW: **V8 `ReferenceDAG` begins**: five WHITE-outlined step boxes in an unordered pile on the
right (`DataCollector`, `DataProcessor`, `ModelTraining`, `CreateModel`, `DeployModel`).
CODE(src/workflow/cli.py: 165 + 180–197) on the left (12 lines: line 165, then 180–190 with 191–197
folded as `…`): line 165 `CacheConfig(enable_caching=True, expire_after="30d")` GREEN; lines 190–193
(`ProcessingOutput(output_name="raw-data", …)`) PINK. One "cached · 30d" chip settles on
`DataCollector`, then copies (`LaggedStart(TransformFromCopy)`) to `DataProcessor`, `ModelTraining`
and `DeployModel`; `CreateModel` gets a GREY chip "no cache_config" (cli.py:283–288).
SAY: First, caching, for 30 days. The first step is a processing step named data collector, with one declared output, raw data.

SHOW: CODE(src/workflow/cli.py: 212–222): lines 219–220 `step_collect.properties.ProcessingOutputConfig
.Outputs["raw-data"].S3Output.S3Uri` light PINK token by token; a PINK solid edge draws from
`DataCollector` to `DataProcessor`; the two boxes pull into line. A RED-struck chip "a string" beside
the expression; GREEN "a reference".
SAY: The second step, the processor, takes as input a property of the collector: its raw data output, S3 URI. Not a string: a reference, and it draws an edge.

SHOW: CODE(src/workflow/cli.py: 262–268) then CODE(…: 276–288): lines 266–267 (`…Outputs["tfrecords"]…`)
PINK → edge `DataProcessor → ModelTraining`; line 277 (`step_train.properties.ModelArtifacts
.S3ModelArtifacts`) PINK → edge `ModelTraining → CreateModel`. The pile is now a chain of four.
SAY: Training takes the TFRecords output of the processor the same way, and the model step takes the trained model artifacts. Each reference draws one more edge.

SHOW: CODE(src/workflow/cli.py: 305–315) then CODE(…: 320–327): line 309 (`step_create_model
.properties.ModelName`) PINK → edge `CreateModel → DeployModel`; line 322 (`steps=[…]`) YELLOW;
lines 326–327 (`upsert`, `start`) PURPLE. The chain of five is complete. LECTURE 15 · 33 while
lines 326–327 are lit (slide 33's "create the job, run it", our redrawing as two PURPLE arrows from
the laptop to a BLUE SageMaker box); it fades with them.
SAY: Last, the Lambda step named deploy model takes the model name from the model step. Then the pipeline lists all five steps, creates the deploy Lambda from your laptop, upserts its definition, and starts it.

SHOW: Line 322's list enlarged: `steps=[step_collect, step_process, step_train, step_create_model,
step_deploy_lambda]`. A YELLOW card. The graph stays dimmed and unchanged under the timer.
SAY: Something to ponder. Reverse the list of steps in the Pipeline call. Does the run order change?
PONDER(8 s, "Reverse the list steps=[…]\nin Pipeline(...).\nDoes the run order change?")

SHOW: The list reverses with a shuffle animation, then shuffles again; the graph does not move; its
PINK edges pulse once. Chip "order = references · list = a set".
SAY: No. The order comes from the references: each input names the output of another step. The list is a set of steps, not a schedule.

SHOW: TRACKER B7 1 · extra · built offline, not sent. A host strip types laptop/92's line 1 (extra;
cut) → TERM(laptop/92: 30 from "Running within a PipelineSession" wrap, …, 59, 113, 143, 186, 246,
260, …, 279); the five `"Name"` lines YELLOW (line 246 reads `CreateModel-CreateModel`: chip "the SDK
adds the suffix"); line 143 `{"Get": "Steps.DataCollector…S3Uri"}`
PINK; line 279 `[capture stub] Pipeline.upsert() and start() NOT sent` GREY. (Lines 191 and 251
are not printed; if a scroll shows them, `763104351884` reads `<aws-dlc-account>`.) A JSON sheet is
pressed out of V8's graph; a GREY-dashed "YAML (the lecture, slide 29)" sheet beside it. LECTURE 15 ·
30 for this block only.
SAY: An extra, built offline and never sent: the JSON definition from the SDK. Five steps, each edge a get on a property of another step. Upsert sends this.

SHOW: LECTURE 15 · 37–38. Slide 37's four-node chain redrawn small above V8's five boxes: "Model
Deploy" splits into `CreateModel` (a V5 Model card icon) and `DeployModel` (a BLUE Lambda icon).
CODE(src/workflow/deploy_model_lambda.py: 47–58): `update_endpoint` (line 49) and `create_endpoint`
(line 55) YELLOW; V5's plate `cheese-app-endpoint` with its configuration swapping behind it. On "a
small function", the S02 mini-legend chip "Cloud Functions → Lambda" sits in the lower right.
SAY: The lecture draws four steps. Here, deploy splits in two. Create model makes the model, and a Lambda, a small function AWS runs on demand, creates or updates the endpoint.

SHOW: **The shared drawer** under the chain: a BLUE bucket. Each step's declared output folder is an
empty tray (`/opt/ml/processing/output → s3://<b>/raw`, …). GREY-dashed files `raw.zip`, `clean.zip`,
`tfrecords.zip` drop into the bucket root **by name** (CODE refs as chips:
`src/data-collector/cli.py:65`, `src/data-processor/cli.py:68`). A GREY "?" chip on the training
box's input: "not verified here". The PINK edges stay lit above the drawer: "edges set the order ·
files travel by name".
SAY: One honest caveat. The edges set the order, but files also travel by fixed names through the bucket: raw, clean and tfrecords dot zip. We could not check, without an account, how the training job finds its data on SageMaker.

SHOW: TRACKER B7 1. Container prompt; it types `python cli.py --pipeline` → TERM(laptop/90: 108, …,
153–154 wrap), RED; GREY chip "with keys: SageMaker Pipeline started: <ARN> · no output shown".
A GREY chip, tag `erratum`: "if upsert fails on the Lambda runtime: add `runtime=\"python3.12\"` to
`Lambda(...)` (cli.py:297) · from the code, not run". `▶ your turn`. TRACKER B7 2. CONSOLE("SageMaker
Unified Studio › Build › ML Pipelines", B:234): the five-box graph redrawn from laptop/92 (not the
README's screenshots), the fourth box labelled `CreateModel-CreateModel` (the SDK adds the suffix),
all boxes pending.
SAY: Step 1: python cli.py dash dash pipeline stops at the same line 32. With keys, it prints that the pipeline started. If instead upsert fails on the Lambda runtime, add runtime equals python 3.12 to the Lambda call, line 297. Step 2: in Unified Studio, under Build, ML Pipelines, you would see this graph.

SHOW: TRACKER B7 2. The console graph runs as an illustration (tag `illustration · not run here`):
boxes go YELLOW then GREEN ✓ in turn;
on "caching", a re-run shows `DataCollector` GREY dashed "cached". On "green", `DeployModel` turns
GREEN while V5's endpoint plate beside it shows "Creating" ORANGE, then a YELLOW chip "wait for
InService". GOLD `cost_tag("each step's machine · a new Lambda per run · cheese-app-endpoint (ml.m5.large) stays up")`.
SAY: If every step succeeds, caching skips unchanged steps for 30 days, so the collector won't scrape again. And a green deploy model only means the Lambda asked: wait until the endpoint is in service.

SHOW: TRACKER B7 3. It types `python cli.py --data_collector` (chip "shown in S14"), then `python
cli.py --data_processor`, `python cli.py --model_training`, `python cli.py --model_deploy`, each followed by its own last error line
only, one RED line per command: TERM(laptop/90: 98 to "(InvalidClientTokenId)"), (… 208 to …),
(… 263 to …), (… 318 to …) (typed lines 45, 155, 210, 265). A GREY chip "each flag:
its own step, as a separate job · --model_deploy makes another endpoint · delete it before the next
--pipeline, or DeployModel fails (from the code, not run)". Fade to empty.
SAY: Step 3 tests each component with its own flag. Here, all four stop at that line. With keys, model deploy makes yet another endpoint.

---

## S16 · Tear down, recap, test yourself — `s16_recap.py` · `TeardownRecap`

SHOW: No tracker. LECTURE 15 · 41. The GOLD "DELETE" word card returns small. The GOLD clean-up card
builds line by line, each line ticking as it is spoken: "1 `aws sagemaker list-endpoints` → delete
every endpoint (Part A's timestamped ones, `cheese-app-endpoint`, `cheese-app-endpoint-…`), then their
endpoint configurations and models".
SAY: Before you leave, clean up. List your endpoints and delete every one: the timestamped ones from part 1, and cheese app endpoint. Then delete their configurations and models.

SHOW: LECTURE 15 · 41 (held). Lines 2–4 tick: "2 empty and delete both buckets"; "3 delete the two
ECR repositories"; "4 delete the `sagemaker-deploy-model-lambda-…` functions and `cheese-pipeline`".
SAY: Empty and delete both buckets. Delete the two ECR repositories, the deploy Lambda functions, and the cheese pipeline.

SHOW: Lines 5–6 tick: "5 deactivate and delete the access keys; delete users and roles you no longer
need"; "6 check the SageMaker AI domain and the Unified Studio domain, and any
`sagemaker-<region>-<account>` bucket the SDK may have made"; then a GREY line "7 optional · your
laptop: `docker image rm` the ~4 GB `model-deployment-cli-aws` and the `cheese-app-*` images ·
`persistent-folder`" (no words). The card shrinks to a GOLD corner icon; the lecture tag fades with
it.
SAY: Deactivate and delete the access keys, and the users and roles you no longer need. Finally, check the SageMaker AI domain and the Unified Studio domain you created.

SHOW: LECTURE 15 · 40. Slide 40's chain writes along the top in one move ("recipe → … → factory",
"your Python = the recipe", "SageMaker Pipelines runs it"), then fades with the tag. Five small
thumbnails of today's set pieces appear in a row, each lighting as it is named: V1 (key on the laptop,
badge in the cloud), V2 (star vs pin), V3 (the two pipes), V5 (three pieces), V8 (edges by
references).
SAY: The lecture ends on a factory: your Python is the recipe, and SageMaker Pipelines runs it. Today's pictures: a key on the laptop and a role in the cloud. A star is not a pin. Preprocessing sits in the client or in the model. Three pieces stand behind an endpoint, and references draw the edges.

SHOW: Under the thumbnails, Part A's mini-chain: "`--prepare` (slide 12 steps 1 and 3)" →
"`--deploy` (steps 4–5)" → "`--predict`" → "`--delete`", each with a small V4/V5 icon.
SAY: Under it, part 1 in four commands. Prepare packs the model, deploy builds the model, configuration and endpoint. Predict sends the numbers, and delete turns off the meter.

SHOW: Clear. A YELLOW card "Test yourself · 1/5": "Your laptop and the SageMaker endpoint both reach
S3. Which identity does each use, and why do Option 2's exported keys never reach the Part A
container?"
SAY: Test yourself. Your laptop and the endpoint both reach S3: which identity does each use? And why do the option 2 exports never reach the part 1 container?

SHOW: One card on screen at a time: card 1/5 **Transforms** into card 2/5 and card 2/5 into 3/5 on
the SAY's sentence boundaries (`vo.wait_until`). Card 2/5: "Name the three things `--deploy`
creates. Which is the address, and which bills while nobody calls it?" Card 3/5: "Where does preprocessing sit in Part A, and where in the Part B
trainer? Give the lecture's two reasons to put it in the model."
SAY: Name the three things deploy creates. Which one is the address, and which one bills while nobody calls it? Where does preprocessing sit in part 1, and in the part 2 trainer, and why move it into the model?

SHOW: One card at a time again: card 3/5 Transforms into 4/5, then 5/5, on the sentence boundaries.
Card 4/5: "Which lines make `ModelTraining` wait for `DataProcessor`? What would a literal
`s3://…/tfrecords` string change?" Card 5/5: "Which two one-line fixes did today's tutorial need,
and which one would an Apple-silicon Mac not need?" After card 5 fades: a GREY pointer card
"answers: exercises.md · study guide", then a GREY-dashed "L23 · trigger the pipeline from GitHub
Actions". Fade to empty.
SAY: Which lines make training wait for the processor? Which two one-line fixes did today need, and which would an Apple silicon Mac skip? The answers are in the exercises, and lecture 23 triggers the pipeline from GitHub.
