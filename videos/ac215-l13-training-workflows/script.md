# AC215 · Lecture 13 — Advanced training workflows: a run is a record, a job is a rented machine — narration script & visual plan (v2)

Audience: an AC215 student who has done L1–L11: a GCP project with billing (L1), images,
containers, bind mounts and `docker-shell.sh` scripts (L2–L4), training and fine-tuning in Colab
(L8), service accounts and JSON keys in a sibling `secrets/` folder, `GOOGLE_APPLICATION_CREDENTIALS`,
buckets and a versioned dataset (L10–L11). New to them: experiment tracking by hand and with W&B,
the W&B run lifecycle, turning a notebook into a pip-installable package, Vertex AI custom jobs and
prebuilt training containers, the identity that submits a job versus the one that runs it, GPU
quotas, and data-parallel multi-GPU training. They watch with two Colab copies (notebooks A and B),
a clone of `dlops-io/model-training`, a free W&B account and a GCP project open, pausing to run
each step. This lecture's Vertex AI jobs bill the project while they run: GOLD tags mark each
billing point **without amounts**, and the video ends on the shutdown checklist.

Goal: after the video they can run both notebooks and say what their folder of five runs and the
comparison table leave out (the split, the code version, the data version), which is why the two
notebooks crowned different winners; log runs to W&B from Colab with a secret named `WandB`, say
why only the run with a callback draws curves and why `wandb.config = {...}` leaves the run's
config at `{}`, and write the three-line pattern correctly (`init(config=…)` · callback ·
`finish`); explain serverless training as "rent the machine for the training step" (a tarball goes
to a bucket, Vertex AI starts a VM with Google's prebuilt TensorFlow container, installs the
tarball, runs `python -m trainer.task` with flags, deletes the VM); build the `model-training-cli`
cockpit through today's two Dockerfile failures and show that it only submits; package and submit
with `sh package-trainer.sh` and `sh cli.sh`, read the job in `sh -x`, know that the W&B key sits
in the job's arguments and that an un-exported key fails only after the data download; name who
submits (the `model-trainer` key) and who runs (the project's Vertex AI service agent); say which
three switches must agree for a GPU and what `MirroredStrategy` splits, averages and creates inside
`strategy.scope()`; shut everything down, knowing the trained model is not saved anywhere yet.

Sources of truth: `BRIEF.md` (design, binding, with the coordinator's decisions table), `digest.md`
(tutorial digest), `SLIDES.md` (lecture-slide digest), `assets/` (see `ASSETS.md`). Where the digest
or the slides and the captures disagree, the captures win. Nothing in a terminal panel is typed by
hand: every output line below names its capture file and line numbers, and every notebook line its
extract and line numbers.

Conventions
- `SAY:` lines are spoken verbatim by the TTS voice (one `voiceover` block each) and become the
  subtitles. Plain spoken English: no backticks, no symbols (no `&`, `%`, `/`, `#`), no
  parentheses; commands and paths are said in words ("sh docker-shell.sh", "sh dash x cli.sh",
  "python dash m trainer dot task", "slash secrets") while the exact spelling is on screen. W&B is
  written and said "W and B" (once in full, "Weights and Biases", in S02); the library and its calls
  are written `wandb` ("wandb init", "wandb config", "wandb finish", "model fit"). Underscored names
  are said as words ("the two block run", "the W and B key variable", "the region variable", "the
  model dir flag"); the run name `mobilenetv2_train_base` is said "both MobileNet runs". File, tool
  and service names are written as they are and said by lexicon entries (`explainer/lexicon.yaml`;
  existing and used here: docker-shell.sh, cli.py, uv.lock, pyproject.toml, Colab, CUDA, "3.10",
  "401", "a 403", README's, entrypoint). Words this script needs that have no entry yet are listed
  in **Lexicon candidates** at the end; this script does not edit the lexicon. The lexicon splice
  turns an "a" directly before an entry into the letter name, so no SAY line puts a bare "a" before
  an entry or a candidate ("one T4", "a free account on W and B", "one JSON key",
  "one n1-standard-4 machine"); "a 403" is the one guarded form. No `'s` after a word with an entry
  or a candidate (never "TensorFlow's", "Vertex's"); `README's` is an entry. Numbers as digits
  (thousands with a comma: "1,156", "4,016"); never a "!" after a digit; no prices, no "cents".
  Versions are said with "at the time of recording" the first time they are spoken (v2 speaks only
  wandb 0.31.0 today vs 0.22.2 stored); every other drifting version or size (TensorFlow 2.19.0,
  Python 3.13.17, uv 0.13.5, Cloud SDK 590.0.0, the Vertex AI library 1.120.0, 2.59 GB, the image
  sizes) is on screen only, with its `at the time of recording` tag; the wandb pin 0.15.11 is said
  as "pinned"; the image tags 2.14 and 2.17 are fixed names; the tarball's 4,016 bytes, the eight
  entries and the notebooks' counts are deterministic or stored and are said plainly. Never write
  "notebook A's" (the `notebook A` entry would leave a bare "'s"): say "the folder from notebook
  A", "the winner in notebook A".
- Every spoken sentence starts with a capital letter or a digit (`explainer.voice.split_sentences`
  splits only there; the same split drives TTS gaps, subtitle cues and the Chinese alignment). No
  sentence opens with a lowercase command, flag, tool or file name ("The call wandb init…", "The
  script's set dash e line…", "Its find packages call…"). No homographs: never "read", "live",
  "lives", "close", "lead", "tear" (so "shut down", never "teardown"), "minute" (singular),
  "content", "object", "record" or "records" as a noun or verb ("recorded" and "recording" are fine;
  a run's history is "what the run keeps", "a log"; `record` appears only on screen). The main
  clause comes first so the Chinese subtitles keep English clause order.
- `SHOW:` lines describe what is on screen during that `SAY:` line, and what moves.
- `PONDER(n s, "question")`: after that SAY block, `pause_and_ponder(self, "question", seconds=n)`
  (silent timer); the card is removed at the start of the next block. Eleven in the video (BRIEF):
  S03, S05, S08, S10, S11, S12, S14 (8 s) and S04, S07, S09, S13 (6 s). `QUICK(4 s, "question")` is
  the same call with 4 s for the BRIEF's one quick predict (S06); the card says "quick predict".
  Each card's text is the BRIEF's (`\n` = line break); the answer is said in the next SAY block.
- `TERM(laptop/NN: lines)`: a terminal beat. `laptop/NN` is the one file
  `assets/terminal/laptop/NN-*.txt` (`colab/CNN` likewise under `assets/terminal/colab/`). The scene
  types the command written just before it in the SHOW line (in backticks, exactly as the README
  spells it; extras exactly as the capture's line 1 spells them), then prints those lines. Line 1 of
  every capture is its `$ …` command and is never printed; the `[exit N]` line is never printed.
  Inside the line list:
  - `…` = print one `…` line;
  - `wrap` = fold long lines (`Terminal.print(..., wrap=True)`): tracebacks, `08`'s JSON message,
    `21`'s Docker error, `40:77`, `71:34`;
  - `from "…"` = print that long line from the quoted phrase on, after a `…`;
  - `cut` = print the line cut at the frame's right edge (no fold), e.g. `30:51`, `80:70`;
  - `squeeze` = a table re-aligned with two-space gutters, an empty trailing column dropped;
  - `→ (no output)`: the prompt simply returns (the capture holds only `[exit 0]`, or the command
    has no capture because it prints nothing, e.g. `cd`).
- Typed lines at the cockpit prompt. The `istep` captures (`26`, `30`, `40`, `50`, `60`, `70`)
  hold a whole session: `sh docker-shell.sh`, the build, the entrypoint banner (lines 34–41) and
  then each typed line after the prompt (`root@44bbacf7e181:/app# ls -la /secrets`). The scene
  shows the prompt as **`root@<id>:/app#`** (BRIEF crops: container ids are never shown) and types
  the rest of that line; the line numbers in a TERM after such a command are its output lines. The
  capture opened a fresh cockpit for each segment (`26`, `30`, `40`, `50`, `60`, `70`); the scenes
  do not re-type `sh docker-shell.sh` when the narrative stays in one cockpit (S09 → S10 → S12),
  and a GREY chip at the first prompt of a new segment says "our capture: a fresh cockpit for each
  step · stay in yours". The `exit` lines that ended a capture are never typed.
- Crops (BRIEF "Crops", ASSETS "Capture-only deviations"): the `[IP: 172.17.0.1 38713]` tail of
  every apt line of `21` (cut at "404  Not Found"); every `wandb: Network error (ProxyError),
  entering retry loop.` line (`84:2`, `86:2`, `86:5`, `87:2` are never printed); container ids in
  prompts and in `71:34` (rendered `"…"`); the job name's random hex in `40:65–66` and `40:77`
  (rendered `cheese_training_job_<12 hex>`); the BuildKit `sha256` export lines `26:28–31` (never
  printed); image IDs in `27`, `91` (the ID column dropped by `squeeze`); W&B run ids, auto run names
  and the team in notebook B's URLs (`https://wandb.ai/<team>/cheese-app-demo/runs/…`). The W&B
  team is shown as **`<team>`** everywhere (coordinator decision), the user as `<W&B user>` (already
  masked in the extract). The placeholder JSON key's size (`06`, 415 B) is never highlighted and its
  content is never shown. `README.md` line 96 is never shown or quoted: README cards quote only the
  line spans named below.
- Terminal size: the house `term()` (12.6 wide, 22 pt, 65 characters a row, full width). A typed
  command is never cut: it folds at a space onto an indented row; the long one-liners (`07`, `08`,
  `09`, the three `sed` edits, `80`, `83`–`86`, `70:44`) are shown small in a strip and fold. When a
  picture needs the frame, the terminal shrinks to a 3-row strip along the bottom edge; a full
  terminal and a picture never share the frame.
- `CODE(path: a–b)`: `code_panel(...)` quoting `assets/source/model-training/path` from line a to b
  (`assets/source/model-training-history/` for the `.diff`, header prefix "history ·"), header
  `path · lines a–b`; never more than 12 lines on screen at once (a longer span is a 12-line window
  that scrolls). A "README card" is a GREY quote of `README.md` text with the header
  `README.md · line n` (model-training @ `b9aee1c`). Instructors' resource names
  (`cheese-app-trainer`, `ac215-project`, `cheese-app-models`) appear **only** inside quoted source
  or README lines and in `08`, each time with a GREY chip "replace this with yours" (coordinator
  decision); the narration says "the README's name", "the instructors' bucket", never the names.
- `NB(A: a–b)` / `NB(B: a–b)`: a notebook-frame `illustration` (a schematic Colab cell, no product
  chrome, no logo) quoting `assets/source/colab/notebook-A-1h6xRhjI.cells.txt` /
  `notebook-B-1aAE5vR9.cells.txt` lines a–b; the frame's header says "notebook A · cell n" (cell
  numbers are the extracts' 0-based indices). Code lines are printed as code; lines after
  `----- stored output` are printed in an output well tagged `recorded · notebook A, 2025-10-20` or
  `recorded · notebook B, 2025-10-14` (the instructors' runs on a Tesla T4). `[HTML output,
  rendered as text]` markers are never printed. The stand-in strip for Colab is titled
  `colab stand-in · signed out`, prompt `$`, tag `extra · local stand-in`.
- `TRACKER B3`: the `ReadmeTracker`, top-left, in every walkthrough scene, moves to that step.
  `TRACKER B3 · extra`: same step, caption gets " · extra" while a command the README (or the
  notebook) doesn't have is on screen (variants `extra · local stand-in`, `extra · clean-up`).
  Seven trackers (BRIEF), titled with the notebook and README headings (the typo in notebook A,
  "Image Classificaton Models", is written correctly); README = `model-training/README.md` @
  `b9aee1c`:
  - A = "Notebook A › Cheese Classification Models", 6 steps: 1 Setup Notebook · 2 Dataset ·
    3 Build Data Pipelines · 4 Image Classification Models · 5 Experiment Results · 6 Upload
    Experiment to Cloud Storage.
  - B = "Notebook B › Experiment Tracking with W&B", 6 steps: 1 Setup (`!pip install -q wandb -U`) ·
    2 Dataset & pipelines · 3 W&B login · 4 Train five models · 5 Experiment Results · 6 Upload.
  - C = "model-training › Setup Environments & Credentials" (`README.md:6-81`), 7 steps: 1 Clone ·
    2 Vertex AI API · 3 GPU Quotas · 4 `secrets` folder · 5 Service account + key · 6 GCS bucket ·
    7 WandB key.
  - D = "model-training › Run Container" (`:83-116`), 2 steps: 1 Edit `docker-shell.sh` ·
    2 `sh docker-shell.sh` — plus two `extra` rows: "fix 1 · Dockerfile:2", "fix 2 · Dockerfile:37".
  - E = "model-training › Package & Upload Python Code" (`:119-129`), 3 steps: 1 Review
    `setup.py` · 2 Review `task.py` · 3 `sh package-trainer.sh`.
  - F = "model-training › Create & View Jobs in Vertex AI" (`:132-163`), 5 steps: 1 Review
    `cli.sh` · 2 `sh cli.sh` · 3 CPU (optional — already the default) · 4 View Jobs · 5 View
    Training Metrics.
  - G = "model-training › OPTIONAL: Multi GPU Training" (`:165-170`), 4 steps: 1 Review
    `cli-multi-gpu.sh` · 2 Review `task_multi_gpu.py` · 3 Make changes · 4 `sh cli-multi-gpu.sh`.
  - `tracker_cleanup` = "extra · clean-up" (the README has no clean-up section), 3 steps:
    1 jobs & bucket · 2 cockpit & images · 3 notebooks & keys (the cockpit-only lines come before
    `exit`).
  S01, S02, S06 are concept scenes with no tracker; S11's badges beat has none until the stand-in;
  S14's ladder and the V7 picture before G1, and S15's `cli.py` beat and recap have none.
- `(extra)` after a command: not in the README or the notebook. A small GREY tag `extra` (or a
  variant) sits beside the typed line, and the SAY says "extra" the first time each kind appears in a
  scene. Commands the README describes without spelling (the clone, `mkdir secrets`, the
  `docker-shell.sh` edit) carry a GREY chip saying so ("the README links the repo", "the README
  shows a tree, not a command", "our editor; use yours"); the README's own words stand beside them on
  a README card. The two Dockerfile fixes are `extra` rows of tracker D, said as "the first fix, an
  extra" / "the second fix, also an extra".
- `▶ your turn`: a YELLOW tag beside the command at a real checkpoint (about one per README or
  notebook step); the SAY of that block says "pause". The video doesn't wait: the viewer pauses.
- Tags (GREY unless said): `illustration` on every console step, W&B page, notebook frame, the
  sidebar, the job-log shape (S12), the repo run's ledger row (S12, coordinator decision: config
  keys from `task.py`, empty curve slots, **no numbers**), the quota page, the GPU log line in S13;
  `recorded · <source>` on every success a student sees that this machine could not produce
  (notebook outputs with their cell; the counts in S12, `recorded · notebooks A/B`); `extra · local
  stand-in` on `colab/C05`, `C05b`, `C38`, `C38b` and `laptop/80`–`87` (the Vertex job's first
  step, replayed in a plain Python 3.10 container; `09` is a live manifest check and is plain
  `extra`); `stand-in` on the key file in `06`; `plan · drawn` on V4 step 4's miniature in S06 and
  `what Vertex does · drawn, not recorded` on the full V4 step 4 in S11 (no output panels in
  either); `extra · not captured` on S07's optional `read -rs` chip;
  `at the time of recording` beside every version and image size when first shown; `erratum` on
  every README/repo/notebook slip (the narration says "a small slip", never "erratum"); the GOLD
  `cost_tag()` — **text only, never a number** — at S01 (checklist), S03 (experiment folder in the
  bucket), S07 (bucket), S09 (tarball), S10 (the job's VM), S13 (a GPU), S14 (`n1-standard-32` +
  2 × T4) and on S15's checklist card. Every cost tag that names compute ends "see the Vertex AI
  pricing page". There are no `expected` panels in this episode.
- The honest framing (BRIEF "The sandbox, honestly"): S07's fifth block says once, plainly, that
  this machine has no Google credentials, no W&B account, no GPU and no browser, and that the key in
  the folder listing is an obviously invalid stand-in moved out before the first container start.
  From then on every cloud failure is taught as the missing-key lesson, every success carries
  `recorded` + its source or is described in words with no output panel (`gsutil cp`'s upload, the
  submitted job, the console's job page, the W&B project), every stand-in is tagged, and nothing
  apologises again.
- `lecture_ref(13, "a–b")` (GREY, top right): one per scene as assigned in the BRIEF, spans from
  SLIDES.md §5. Lecture diagrams are redrawn in series style; no slide images, console, W&B or Colab
  screenshots, logos, the README's six PNGs, or the slide-31 photo.
- Spelling on screen and in the subtitles: American ("traveled", "gray").
- Semantic colours (BRIEF, fixed for the whole video):

  | meaning | colour |
  | --- | --- |
  | your laptop: host shell, host filesystem, the `secrets/` folder's home, the browser | GREY |
  | remote machines and services: the GCP project boundary, the bucket, Vertex AI, the job's VM, Cloud Logging, the Colab runtime (T4); `wandb.ai` as a separate BLUE building outside the GCP boundary | BLUE |
  | containers and images: `model-training-cli` (the cockpit), Google's prebuilt `tf-cpu.2-17.py310` / `tf-gpu.*` containers in the job VM, the stand-in containers (dashed) | TEAL |
  | system-wide, provided, not yours: Debian base images (bullseye → bookworm), apt packages (`google-cloud-sdk` → `google-cloud-cli`), what the prebuilt image is assumed to provide (TensorFlow, scikit-learn: expected, not verified here; `requests` arrives with wandb), the service agent's badge | ORANGE |
  | project-owned, pinned, protected: `package/` (`setup.py`, `trainer/`), `wandb==0.15.11`, `uv.lock`, the tarball, the `model-trainer.json` key, the W&B key while it sits in your shell, a run's `config` | GREEN |
  | tools: docker, gcloud, gsutil, uv, pip, tar/gzip, the `wandb` library, `tf.distribute` | PURPLE |
  | errors and exposure: the 404s, `no installation candidate`, auth errors, `KeyError`, `no-tty`, `yours was 2`, `Conflict`, the W&B key once visible in `--args`, the config that went to a loose dict | RED |
  | your turn, the trackers, the current step, the run under discussion | YELLOW |
  | money: the job VM while it runs, a GPU, the 32-vCPU two-T4 machine, bucket storage — never a number | GOLD |
  | routes: `gsutil cp` into the bucket, `--python-package-uris`, stdout → logs, the stream to `api.wandb.ai`, the all-reduce links | PINK |
  | future / elsewhere / missing: the model that is never saved, L15, Multi Worker Mirrored, the curves no callback draws | GREY, dashed |

  Episode-local semantics (BRIEF): a run is a WHITE row in a ledger (V2); its columns become slide
  9's seven items, filled cells WHITE, empty cells GREY-dashed. Curves exist only where a PURPLE
  callback pipe connects `model.fit` to the row; no pipe, a ghost outline. The two keys are two
  GREEN badges (Google key file, W&B key); the W&B badge turns RED the moment it is printed inside
  `--args`. Your Docker image never leaves the laptop: the TEAL cockpit stays GREY-side, and only
  the GREEN tarball crosses to BLUE.
- Running example. The laptop: a fresh `docker:29.8.2-dind` engine standing in for Docker Desktop
  (linux/amd64), user `student`, home with `model-training/` and `secrets/` side by side (`05`);
  terminal title `laptop`, prompts `student@laptop:~$` and `student@laptop:~/model-training$`. A
  second host terminal (S07 ponder 4, S10's no-key beat) is titled `laptop · new terminal`. Inside
  the cockpit: `root@<id>:/app#` (the image creates a user `app` but never switches to it). Colab:
  notebook frames with stored outputs; the Colab stand-in strip as above. Placeholders: bucket
  `gs://your-bucket-placeholder` (`07`: it exists nowhere), project `your-gcp-project`, W&B key
  `PLACEHOLDER_NOT_A_REAL_WANDB_KEY_0000000` (`10`, `40:75`, `40:77`, `86`), drawn in full only where
  a capture prints it; on W&B pages and Colab's secret panel the key is a row of dots.
- V1 `TrainingMap` (persistent state across scenes): built dark in S02 (Colab lane above, repo lane
  below: laptop with the TEAL cockpit and GREEN `secrets/` drawer · BLUE dashed `your-gcp-project`
  with the bucket · Vertex AI job tiles · a separate BLUE building `wandb.ai`); the Colab lane lights
  in S03–S04; S06 lights slide 24's layers as a plan; S07 ends part 1 with the Colab lane lit, the
  repo lane dashed, the key chip in a variable and the bucket named; S08–S14 light the repo lane piece
  by piece (the cockpit gets its "submits · never trains" stamp in S09); S15 shows it complete, then
  unlit. The cockpit has exactly two arrows (package & upload; create job) and none into a job.
- Length and parts: narration **4,292** words after the v2 review merge (`python -m
  explainer.script`, which counts SAY words; its minute figure assumes 155 wpm and is ignored;
  ceiling 4,300). At Kokoro af_heart speed 0.9 (≈174 wpm) that is ≈24.7 min of narration, ≈29–31
  min with typing, outputs, three builds and the ponder timers. Part 1 = S01–S07 (track it, then
  get ready; ends on V1 with "today it won't build"), part 2 = S08–S15 (ship it). Each part ends on
  an empty frame. Per scene (BRIEF target in brackets, ±15 % band):

  | scene | words (BRIEF) | scene | words (BRIEF) |
  | --- | --- | --- | --- |
  | S01 Hook | 205 (220) | S08 TwoFixes | 333 (340) |
  | S02 LeversAndRecord | 190 (220) | S09 InsideTheTarball | 311 (300) |
  | S03 FolderTracker | 317 (280) | S10 OneCommand | 339 (310) |
  | S04 SharedAxis | 325 (290) | S11 WhoRunsIt | 318 (300) |
  | S05 ThreeLines | 242 (240) | S12 WhatTheJobSays | 297 (290) |
  | S06 RentTheMachine | 259 (250) | S13 ThreeSwitches | 205 (230) |
  | S07 KeysAndBucket | 321 (290) | S14 TwoGpusOneModel | 332 (300) |
  |  |  | S15 Recap | 298 (270) |
  | **part 1** | **1,859** (1,790) | **part 2** | **2,433** (2,340) |

  Every scene is within the BRIEF's ±15 %. Tight edges: S02 (floor 187), S03 (cap 322), S04 (cap
  333), S07 (cap 333), S15 (cap 310) and the total (8 words under 4,300): any later addition there
  names its cut in the same scene. Re-run the counter after any review edit.

Notes for scene authors
- TERM line numbers are *file* lines (line 1 = the `$` command); `Capture.pick()` indexes the
  output body, so pick index = file line − 1. NB line numbers are extract lines.
- Shared code (`scenes/common.py`, started from L11's): tracker factories `tracker_a` … `tracker_g`
  and `tracker_cleanup` with the step lists above; prompts `P_LAPTOP` (+ `~/model-training`) and
  `P_COCKPIT` (`root@<id>:/app#`); `notebook_cell(code, output, cell_no, notebook)` with the
  `recorded` tag; tags `extra_tag` (and its variants), `illustration_tag`, `recorded_tag`,
  `your_turn`, `erratum_tag`, the GOLD `cost_tag` (text only). Set pieces: `TrainingMap` (V1),
  `RunLedger` (V2), `ConfigBinding` (V3), `TarballTrip` (V4), `ThreeBadges` (V5), `GpuSwitchboard`
  (V6), `MirroredReplicas` (V7). Never reuse a scene class name for a helper.
- `21` (189 lines) and `23` (380 lines): print only the lines named in S08. `26`: lines 28–31 are
  never printed. `80`: lines 2 and 68, then 70 with `wrap` (six rows, so both highlighted packages
  are visible). `84`: only line 14 after a `…` (line 3, printed before the check, reads as a
  success). `40:77` is folded with `wrap`; its hex is
  replaced before printing. The ProxyError lines are dropped before any `…` is computed.
- What may show values: notebook outputs (recorded, with their cell); code constants and the
  arguments `cli.sh` sends (in CODE panels and in `40`'s trace); live captures. What may not: any
  Vertex job line beyond the code's own prints and the two recorded counts; any W&B dashboard value
  other than notebook B's stored output; any epoch, loss, timing, accuracy or price for the repo
  trainer; any length claim for a real W&B key (the pinned wandb 0.15.11's 40-character rule,
  `84:14` and `87:14`, is a fact about the pin, said in S07, S09, S10 and S11); the `Currently
  logged in as` line as job output (it
  appears only inside NB(B: 614–615), tagged as notebook B's Colab login).
- Never: slide images, console/W&B/Colab screenshots, logos, the README's PNGs; a real person's
  name, e-mail, W&B user or team; a real-looking key; `README.md:96`; the relay IP, ProxyError
  lines, container ids or the job name's hex; `JOB_STATE_SUCCEEDED`, a "submitted" line, a
  `gsutil cp` success line or a GPU success; "the cockpit trains", "your image runs on Vertex",
  "wandb init logs curves", "serverless means no machine", "two GPUs halve the time", "the model is
  saved"; the stand-ins' output presented as Vertex's; a training time, epoch line, loss or accuracy
  for the repo trainer; any price.

---

## S01 · Two tables, two winners — `s01_hook.py` · `Hook`

SHOW: Black frame, no tracker. Two notebook-frame tables slide in side by side (V2's first frame):
left NB(A: 1283–1295) headed "notebook A · cell 54", right NB(B: 1703–1715) headed "notebook B ·
cell 55", both cropped to the columns `name · epochs · accuracy` (values verbatim, rows in the
tables' own order), each tagged `recorded`. A YELLOW ring settles on each top row:
`mobilenetv2_train_base_True · 15 · 68.97%` (A) and `mobilenetv2_train_base_False · 15 · 68.97%`
(B); on "62.93", B's second row `mobilenetv2_train_base_True · 10 · 62.93%` flashes WHITE. A GREY
chip under both: "same pipeline · same 1,156 photos · same five models", and a second GREY chip:
"train_base True = fine-tuned · False = frozen".
SAY: Two notebooks from this lecture, run by the instructors: the same data pipeline, the same 1,156 cheese photos, the same five models. Notebook A crowns the fine-tuned MobileNet, at 68.97 percent. Notebook B crowns the frozen MobileNet, also at 68.97 percent, and puts the fine-tuned one at 62.93.

SHOW: A YELLOW question card settles above the tables: "Which recipe is better — and from these two
tables, can you even tell what was different?" On "look at the epochs column", a GREY pointer
slides along both `epochs` columns (15 vs 10 on the fine-tuned rows); nothing else is explained.
SAY: So which recipe is better, fine-tuning or freezing? And from these two tables, can you even tell what was different? One clue is visible: look at the epochs column. Hold that question. Part of the answer is in the table, and part of it is in what the table never wrote down.

SHOW: The tables fade. V4 preview: the winning row lifts out of a Colab frame, shrinks into a
GREEN parcel "4 KB tarball" and slides into a BLUE job tile with a GOLD meter (no numbers). A
strip below (GREY tag "preview · scene 10") shows TERM(laptop/40: 75 from "--model_name") — the
`CMDARGS` value — with `--wandb_key=PLACEHOLDER_NOT_A_REAL_WANDB_KEY_0000000` outlined RED.
SAY: Then the fine-tuned MobileNet leaves Colab. It gets packed into a 4 kilobyte tarball and trains on a machine you rent for the length of one job, from one command. That command carries your W and B key.

SHOW: A checklist card: "✓ two Colab copies (free T4)", "✓ W&B account (free tier)", "✓ Docker",
"✓ a GCP project with billing" with a GOLD `cost_tag()` beside it: "Vertex AI jobs bill while they
run · no amounts in this video · see the Vertex AI pricing page". Layout preview: `tracker_a(1)`
top-left; a 2-row strip (GREY tag "preview") shows only the YELLOW `▶ your turn` row tag (the other
tags explain themselves on first use). On "two words", GREY tag `lecture_ref(13, "8")` top
right and two GREY words settle centre: "reproducibility · accountability". Fade out.
SAY: To follow along you need two Colab copies with a free T4 GPU, a free account on W and B, Docker, and a Google Cloud project with billing. Vertex AI jobs cost money while they run; gold tags mark each point, without amounts. A yellow tag means pause and run it, and the study guide has every command. Today's two words, from the lecture: reproducibility and accountability.

---

## S02 · Three levers and a missing row — `s02_levers.py` · `LeversAndRecord`

SHOW: No tracker. GREY tag `lecture_ref(13, "5–6, 9–12")` top right, whole scene. Slide 5 redrawn
as three dials side by side: "More Data" · "Better/Faster Models" · "Faster Hardware"; on "the
third", the third dial turns and lights; a small GREY ledger icon pops up beside it on
"bookkeeping".
SAY: The lecture starts from three levers for better deep learning: more data, better models, and faster hardware. Today we pull the third one: you rent hardware. And you add the bookkeeping that shows whether it helped.

SHOW: Slide 6 redrawn: an arrow POC → Prototype → MVP with pastel bars; the dashed box around
"Setup Experiment Tracking" + "Build Baseline Models" turns YELLOW with a chip "today". A GREY chip
below: "Milestone 3: experiment tracking + one serverless training run, logged and reproducible".
SAY: On the Cheese App roadmap, the dashed box around experiment tracking and baseline models is today. Your third milestone asks for exactly this.

SHOW: Slide 10 redrawn as four rows that snap into homes: "code → GitHub" · "data → versioning
(L11, DVC)" · "environment → pyproject.toml, uv.lock" · "weights, metrics, logs → ?" — the last row
hangs, its "?" RED. Then slide 9's seven items build as a GREY checklist at the right: environment ·
code · data · model · metrics · artifacts · notes, with a small chip "→ the ledger's columns".
SAY: Where does each piece of an experiment go? Code to GitHub, data to the versioning from lecture 11, and the environment to pyproject.toml and uv.lock. Weights, metrics and logs have no home yet. A complete run should keep seven things: environment, code, data, model, metrics, artifacts and notes.

SHOW: Slide 12 in one line, plain text, no logos: "W&B · hosted" (YELLOW) · "MLflow · self-host" ·
GREY chip "the milestone accepts an equivalent". The "?" row is caught by a W&B box.
SAY: The course uses Weights and Biases, W and B for short, which is hosted for you. MLflow is the usual choice if you must host it yourself.

SHOW: V1 builds dark: the Colab lane on top (notebook card A → a folder → a bucket; notebook card B
→ the BLUE `wandb.ai` building) and the repo lane below (GREY laptop with a hollow TEAL cockpit →
BLUE dashed `your-gcp-project` with a bucket → Vertex AI job tiles → `wandb.ai`). Each piece flashes
as it is named, then dims. Caption: "today we light both". Fade out.
SAY: Here is the map. On top, the Colab lane: notebook A fills a folder and uploads it, and notebook B streams its runs to W and B. Below, the repo lane: your laptop packs the code, a bucket holds it, Vertex AI runs it, and the run reports to W and B. Today we light both.

---

## S03 · A tracker made of folders — `s03_notebook_a.py` · `FolderTracker`

SHOW: TRACKER A1 (tracker A appears: "Notebook A › Cheese Classification Models", 6 dots). GREY tag
`lecture_ref(13, "10–11")` top right, whole scene. A Colab menu `illustration`: "File → Save a copy
in Drive", then "Runtime → Change runtime type → GPU"; `▶ your turn`. Then NB(A: 101, 106, 112)
with its output NB(A: 115, 117, 120) (`tensorflow version 2.19.0`, `Number of replicas: 1`,
`GPU Available:  [PhysicalDevice(…GPU:0…)]`, the last cut at the frame) and cell 10's
`!nvidia-smi` box cropped to NB(A: 137), `Tesla T4` YELLOW. A GREY chip on the menu: "the study
guide links notebooks A and B · the badges inside them open older copies".
SAY: Open notebook A from the course page, save a copy, and switch the runtime to a GPU; pause and set it up. Its stored outputs show the instructors' run on one Tesla T4.

SHOW: TRACKER A2. NB(A: 318) (the download line) then cell 17's output NB(A: 352–353):
`Labels: ['brie', 'gouda', 'parmigiano', 'gruyere']` with a YELLOW pin "remember this order", and
`Full size of the dataset: 1156`. TRACKER A3: cell 26, NB(A: 432–443) as code, then its output
NB(A: 445–447): `train_x count: 936` / `validate_x count: 104` / `test_x count: 116`. `▶ your turn`.
SAY: Run the dataset cells: 1,156 photos from one GitHub release, with four cheese labels. Remember their order. Then the split: 936 to train, 104 to validate, 116 to test. Pause and run them.

SHOW: The code panel stays; line 433 `validation_percent = 0.2` and the three counts glow.
PONDER(8 s, "The cell sets validation_percent = 0.2.\nYet validation is 104 of 1,156.\nWhat did the code actually do?")
SAY: Something to ponder. The cell sets the validation percent to 0.2, yet validation is 104 out of 1,156. What did the code actually do?

SHOW: The answer: in NB(A: 436–439) both `test_size=test_percent` light RED; a GREY bar of 1,156
tiles splits: 10 % → 116 (test), then 10 % of the remaining 1,040 → 104 (validation), 936 left; tag
`erratum` with the chip "same lines in task.py:134–146".
SAY: Both splits use the test percent. 10 percent of 1,156 is 116 for testing, then 10 percent of the remaining 1,040 is 104, the validation set. A small slip, copied into the repo trainer.

SHOW: TRACKER A4. V2 builds: NB(A: 527–528) `create_experiment()` → a GREY folder card
`experiment_1760994796/` (the name from NB(A: 1304)). Cell 12's helper as a short excerpt,
NB(A: 242, 245, 249, 289, 307) (the five `save`/`open` lines); for each of the five models a WHITE
stack of five file chips drops into the folder: `.keras` · `.weights.h5` · `.json` ·
`_train_history.json` · `_model_metrics.json`. `▶ your turn` on the training cells.
SAY: Now the home-made tracker. Cell 31 makes a folder named after the current Unix time. After each model trains, the helper from cell 12 drops five files into it: the model, its weights, its structure, its history and its metrics. Pause and train the five models.

SHOW: TRACKER A5. The metric chips fly out and fold into a table of five WHITE rows: NB(A:
1283–1295) (all columns, small), then NB(A: 1304) `experiment_1760994796/mobilenetv2_train_base_True.keras`
under it, YELLOW. A GREY chip with the tag `erratum`, beside NB(A: 1272) and NB(A: 1280): "accuracy
turned into text before sorting · 9.50% would rank above 68.97%". A GREY chip "cells 54–59, through
the predictions"; `▶ your turn`.
SAY: Cell 54 gathers the metric files into one table, and cell 56 picks its top row as the best model; pause and run through the predictions. A small slip: accuracy becomes text before sorting, so it sorts strings; 9.5 percent would rank above 68 percent.

SHOW: The hook's first answer. A GREY strip of 1,156 small tiles; 116 of them light as "test" —
then the lit set reshuffles twice (chip "no seed: a different 116 every run"). A ruler: "1 photo =
0.86 points" (1/116); copy A's top two rows, 68.97 % vs 67.24 %, with "2 photos" between them,
YELLOW.
SAY: Here is a first answer. The folder keeps settings and scores, but not which 116 photos were the test set. The split has no seed, so every run is graded on a different 116. One photo is worth 0.86 points, and the winner in notebook A leads by two photos.

SHOW: TRACKER A6. NB(A: 1396–1397) `auth.authenticate_user()`; NB(A: 1400–1402) with the
instructors' project id and bucket name and GREY chips "replace this with yours" (YELLOW), plus a
GREY chip "your bucket: one from lecture 11, or create it now · scene 7 shows how"; then NB(A: 1437,
1439–1442) (`Uploadin Experiment: experiment_1760994796`, the first upload lines; the bucket line
1438 is not shown) and a `…`. `▶ your turn`. V1's Colab lane: notebook A → folder → bucket lights.
GOLD `cost_tag()`: "stored in your bucket · weights of 10–104 MB per model (the table's model_size),
plus a .keras copy of each". Fade out.
SAY: Sign in with cell 62, put your own project and bucket into cell 63, and run cell 66. Any bucket of yours works; scene 7 creates one. Pause and run it. A gold tag: those files now sit in your bucket, 10 to 104 megabytes of weights per model, plus a copy.

---

## S04 · Runs on a shared axis — `s04_wandb.py` · `SharedAxis`

SHOW: TRACKER B1 (tracker B appears: "Notebook B › Experiment Tracking with W&B", 6 dots). GREY tag
`lecture_ref(13, "12–13, 16–17")` top right, whole scene. A GREY chip, not spoken: "open notebook B ·
save a copy · GPU runtime (cell 3, NB(B: 26–31))". NB(B: 37) `!pip install -q wandb -U`.
Below it the Colab stand-in strip (`extra · local stand-in`; `TRACKER B1 · extra · local stand-in`
while it is on screen), prompt `$`: `pip install -q wandb -U`
→ TERM(colab/C05: 2 cut, 4–5); then `python -c 'import wandb; print(wandb.__version__)'` (extra) →
TERM(colab/C05b: 2), `0.31.0` YELLOW with `at the time of recording`; a GREY chip "stored run:
0.22.2" (NB(B: 773)). `▶ your turn`.
SAY: Notebook B adds W and B. Its first cell installs it, and the dash U flag means whatever is newest. An extra check in our signed-out stand-in shows 0.31.0 at the time of recording, while the stored run used 0.22.2. Pause and run it.

SHOW: TRACKER B2. GREY chip "cells 7–32: the same data and pipelines as notebook A". NB(B:
373–375): line 375 (`experiments.zip`) gets a GREY strike-through chip "about 510 MB you never use
· you may delete this line". `▶ your turn`.
SAY: The data cells, through cell 32, match notebook A, but one also downloads a zip of about 510 megabytes you never use. You may delete that line; then pause and run them.

SHOW: TRACKER B3. A W&B page `illustration`: "User settings → API keys", the key as a row of dots;
then Colab's key-icon panel (`illustration`): a secret named `WandB`, value dots, "Notebook access"
switched on. `▶ your turn`. Then NB(B: 603–606) and its output NB(B: 614–615):
`wandb: Appending key for api.wandb.ai to your netrc file: /root/.netrc`,
`wandb: Currently logged in as: <W&B user> (<team>) …` (cut at the frame; the team masked as
`<team>`), tag `recorded · notebook B, cell 34 (Colab)`.
SAY: Copy your API key from the user settings on W and B. In Colab, open the key icon and add a secret named exactly as on screen, with notebook access on. Pause and add yours. Cell 34 signs in with it.

SHOW: TRACKER B4. NB(B: 697) `wandb.init(project='cheese-app-demo')` YELLOW; the stored banners of
the first training cell, NB(B: 773, 781) (`Tracking run with wandb version 0.22.2`,
`View run at https://wandb.ai/<team>/cheese-app-demo/runs/…`). V2: the five WHITE rows from S03
slide into one BLUE project frame `cheese-app-demo` inside the `wandb.ai` building, and each row
grows an empty slot over one shared epoch axis. `▶ your turn` on the five training cells.
SAY: Now pause and run the five training cells. Each starts its run with wandb init in one project, cheese app demo. In the ledger, the five rows become five runs on one shared epoch axis.

SHOW: Only the `2_block` slot draws curves, from its stored "Run history" sparklines NB(B: 1009–1014)
(25 epochs); the other four slots stay ghost outlines (GREY dashed). On "Compare", two small
panels side by side, neither highlighted: NB(B: 710–716) (cell 38, the `2_block` run's
`model.fit`) and NB(B: 940–945) (cell 42's `model.fit`), identical but for line 715.
PONDER(6 s, "Five runs in one project, but only one\nhas loss and accuracy curves.\nWhat do the other four lack?")
SAY: But only the two block run shows curves. Compare its model fit call with another cell's. Something to ponder: what do the other four lack?

SHOW: The answer: in NB(B: 710–716) line 715 `callbacks=[WandbCallback(save_graph=False,
save_model=False)],` lights YELLOW (the cell-42 panel has no such line); a PURPLE callback pipe runs
from `model.fit` to the `2_block` row only. The warning NB(B: 782) appears small, GREY chip
"deprecated · harmless here". The row's summary cells fill from NB(B: 1016, 1021): `accuracy
0.72436`, `val_accuracy 0.45192`. The four ghost slots stay ghosts. On "system charts", a GREY chip:
"system charts = the machine's CPU · GPU · memory over time".
SAY: A callback: code that model fit calls after every epoch. Only the two block cell passes the W and B callback, so only its loss and accuracy arrive, epoch by epoch. Without one, wandb init gives you system charts, never your curves.

SHOW: The two MobileNet rows collapse under one label, `mobilenetv2_train_base` (NB(B: 1629),
URL masked), GREY chip "tell runs apart by run id". Then a small notebook cell, tagged `extra`
(`TRACKER B4 · extra`): `wandb.finish()` after cell 52.
SAY: Both MobileNet runs share one name, so tell them apart by run ID. No cell finishes the last run, so add wandb finish after cell 52, an extra.

SHOW: TRACKER B5. NB(B: 1703–1715) (cell 55, cropped to `name · epochs · accuracy`) slides in
beside the table from notebook A: the hook's second winner, YELLOW; the fine-tuned rows' `epochs` 10 vs 15
glow, chip "not like for like". On "the frozen MobileNet", both frozen rows ring YELLOW — A's
`mobilenetv2_train_base_False · 15 · 67.24%` (NB(A: 1285, 1292)) and B's `mobilenetv2_train_base_False
· 15 · 68.97%` (NB(B: 1704, 1711)) — with the chip "same settings · 15 epochs · 2 photos apart"; S03's
ruler "1 photo = 0.86 points" returns between them. A GREY chip: "run cells 55–60 too · pause at the
next step".
SAY: Cell 55 builds the second table from the opening. The fine-tuned MobileNet trained 10 epochs here and 15 in notebook A: not a fair comparison. Now the frozen MobileNet, with the same settings and epochs: 67.24 in notebook A, 68.97 here. Two photos apart by chance alone: the size of the winning margin.

SHOW: TRACKER B6: NB(B: 254, 257) (cell 13's `upload_experiment`, the instructors' bucket and
project) with "replace this with yours" chips and a GREY chip "edited? run cell 13 again"; then
NB(B: 1819–1820), GREY chip "cells 64 and 66: no stored output". A last GREY chip, slide 16 (not
spoken): "the lecture's dashboard screenshot shows an earlier project · yours says cheese".
`▶ your turn`. V1: notebook B → `wandb.ai` lights. Fade out.
SAY: To upload, edit the bucket and project inside cell 13 and run cell 13 again, then run cells 64 and 66; pause and do it.

---

## S05 · Three lines, and an assignment that goes nowhere — `s05_config.py` · `ThreeLines`

SHOW: TRACKER B4 (held). GREY tag `lecture_ref(13, "14–15")` top right, whole scene. Slide 14's
baseline redrawn as plain code (`learning_rate = 0.001`, `batch_size = 32`, `epochs = 10`, data,
model, `training_results = model.fit(...)`); three lines slide in, each tagged with the slide's own
call-out (SLIDES.md:40): BLUE "Initialize wandb run" → `wandb.init(...)`; GREEN "Add a callback to
monitor model" → `callbacks=[WandbCallback()]` inside `model.fit`; RED "Let wandb know to finish the
run" → `wandb.run.finish()`.
SAY: The lecture shows the pattern as three lines around unchanged training code. Start the run with wandb init. Watch the model with a callback inside model fit. And finish the run when training ends.

SHOW: Notebook B's real cell 38: NB(B: 696–705); line 698 `wandb.config = {` YELLOW, lines
704–705 GREY.
SAY: Now notebook B's real cell. It starts the run, then assigns a dictionary to wandb config, renames the run, and calls run save.

SHOW: The panel stays; NB(B: 732) `wandb.config.update({"execution_time": execution_time})` joins
it, YELLOW.
PONDER(8 s, "After wandb.config = {…} and\nwandb.config.update(…), what does\nthe run's config hold?")
SAY: Something to ponder. After that assignment, and a later update with the execution time, what does the run's config hold?

SHOW: V3 `ConfigBinding`: a BLUE run box with a GREEN `Config` drawer inside; the name
`wandb.config` is a YELLOW sticky label on a PINK arrow that `wandb.init` points at the drawer. On
"moves the name", the assignment peels the label off and sticks it on a loose WHITE dict outside
the run (RED outline) holding four keys; `.update(...)` writes `execution_time` into the loose
dict; `finish` shuts the run box with its drawer empty, and `{}` stamps on it.
SAY: Watch the name. The call wandb init points the name wandb config at the run's config drawer. The assignment does not fill that drawer; it moves the name onto a new, loose dictionary. The update then writes into the loose one, and the run finishes with its drawer empty.

SHOW: The proof, in the Colab stand-in strip (`extra · local stand-in`; GREY chip "W&B offline
mode · today's wandb"): `cat /tmp/e14.py; python /tmp/e14.py` → TERM(colab/C38: 2–8, 9, …, 16–17);
`type(wandb.config): dict` and `the run's config: {}` RED. Then
`cat /tmp/e14-fixed.py; python /tmp/e14-fixed.py` → TERM(colab/C38b: 3–4, …, 16–17); line 17 GREEN.
V3 replays: with `config={...}` inside `init`, the four keys drop straight into the drawer, the
update adds the fifth.
SAY: The proof, on today's W and B in offline mode, as our stand-in. The name points at a plain dict, and the run's config is empty. The fix passes the dictionary to wandb init itself, and the config holds all four keys plus the execution time.

SHOW: NB(B: 705) `wandb.run.save("test")` with a GREY chip "uploads files matching test · does not
save the run".
SAY: The call run save with the word test uploads files matching test; it does not save the run.

SHOW: The repo does it right: CODE(package/trainer/task.py: 312–322) (`wandb.init(project=…,
config={…}, name=model.name)`), then CODE(package/trainer/task.py: 335–338) (`config.update`,
`run.finish()`), both GREEN ticks. The middle line: CODE(88f3374.diff: 30–36), line 34
`-    callbacks=[WandbCallback()],` RED; a GREY chip "2025-10-15 · removed ca;llback · 51 min after
`1c03dd5` moved the image to TF 2.17 · no reason given". V2: the repo run's row appears with its
curve slot as a ghost. Fade out.
SAY: The repo's trainer gets the first and last lines right: config inside wandb init, then update and finish. But the middle line is gone. One commit in October 2025 removed the callback, without saying why. So its runs get config and system charts, and no curves; exercise 1 adds the callback again.

---

## S06 · Rent the machine, not the server — `s06_serverless.py` · `RentTheMachine`

SHOW: No tracker. GREY tag `lecture_ref(13, "18–24")` top right, whole scene. Slides 19 and 21 as a
schematic three-entry sidebar (`illustration`, no logo): "Workbench → notebooks" · "Training →
jobs" (YELLOW, a small tab "Custom jobs") · "Pipelines → workflows" (GREY dashed chip "L15").
SAY: The second half of the lecture is Vertex AI, Google Cloud's machine learning platform. Three console entries matter: Workbench for notebooks, Training for jobs, and Pipelines for workflows. Today is Training, on the custom jobs tab; lecture 15 uses Pipelines.

SHOW: Slide 22: a BLUE job tile materialises, a GOLD meter on it starts (no numbers), the training
step runs, the tile dissolves and the meter stops. Caption: "there is a machine · you don't manage
its lifetime".
SAY: Serverless training means you rent the hardware only for the training step. Nobody sets up a server, and billing stops when the step ends. There is still a machine; you just don't manage its lifetime.

SHOW: V4 step 1, slide 23 with real names: a notebook card with globals `epochs = 15`,
`batch_size = 32`, `model = …`; the values peel off and re-enter a GREEN `task.py` card from below
as flags `--epochs`, `--batch_size`, `--model_name`, then `--train_base`, `--wandb_key`. A small
GREY chip: "slide: epochs=25 · cli.sh sends --epochs=2".
SAY: Step one: move the notebook code into a Python file, and turn its hard-coded choices into flags. The flags are epochs, batch size and model name, plus train base and your W and B key.

SHOW: V1 lights slide 24's layers as a plan: the GREEN `task.py` wraps into a tarball, an arrow
carries it into the bucket ("2 · package & upload"); at the bottom the label "Model Trainer CLI
Container" appears over the TEAL cockpit, then morphs into `model-training-cli`; its second arrow
goes to Vertex AI ("3 · create jobs"). Two job tiles appear: one labelled "CPU, RAM", one with a T4
chip; each runs its own TEAL container. Then the "CPU, RAM" tile plays V4 step 4 in miniature, in
step with the last sentence's clauses: a machine appears (GOLD meter on), Google's ORANGE-banded
image drops in, the GREEN tarball unwraps, `python -m trainer.task` runs with flag chips, the
machine dissolves. GREY tag "plan · drawn".
SAY: Step two packs that file into a tarball, one compressed archive, and uploads it to a bucket. Step three runs from what the lecture calls the Model Trainer CLI Container, our cockpit on your laptop: it asks Vertex AI for a job. Vertex AI then starts a machine, CPU only or with one T4. It loads Google's prebuilt TensorFlow image, installs your tarball, runs your trainer with your flags, and deletes the machine.

SHOW: Two GREY cards over the map. (1) "the job can't see your laptop": a PINK arrow from the
internet into the job tile, CODE(package/trainer/task.py: 96–100) small (the GitHub release URL);
an "anything to keep → somewhere durable" chip. (2) "the image that runs is Google's": the job's
TEAL container gets an ORANGE "Google" band; the laptop's cockpit stays put.
SAY: Two facts drive everything after this. The job cannot see your laptop: its data comes from the internet, and anything it should keep must be written somewhere durable. And the image is Google's, not yours.

SHOW: The map, all machines outlined.
QUICK(4 s, "Your laptop has no GPU and no TensorFlow.\nWhich machines here will ever\nimport TensorFlow?")
SAY: A quick prediction. Your laptop has no GPU and no TensorFlow. Which machines in this picture will ever import TensorFlow?

SHOW: The answer: the Colab runtime and the Vertex job's container light GREEN; the cockpit gets a
GREY "never · proved in scene 9" chip. Fade out.
SAY: Two: the Colab runtime, and the container inside each Vertex job. Never the cockpit on your laptop; scene 9 proves it.

---

## S07 · A project, two keys and a bucket — `s07_setup.py` · `KeysAndBucket`

SHOW: TRACKER C1 (tracker C appears: "model-training › Setup Environments & Credentials", 7 dots).
GREY tag `lecture_ref(13, "25")` top right, whole scene. Full-width laptop terminal (title `laptop`,
prompt `student@laptop:~$`); a GREY chip on the title, not spoken: "Docker 29.8.2 · git 2.54.0 ·
at the time of recording" (`00:4–5`). A README card (`README.md · line 17`) with a GREY chip "the
README links the repo · we use git clone". It types
`git clone https://github.com/dlops-io/model-training` → TERM(laptop/01: 2); `▶ your turn`. Then
`cd model-training` → (no output); prompt `student@laptop:~/model-training$`.
TRACKER C1 · extra: `git log -1 --format='%H %ci %s'` (extra) → TERM(laptop/02: 2), `b9aee1cc…`
and `2025-10-16` YELLOW, chip "the course pin". Then `ls -la` (extra) → TERM(laptop/03: 7–23;
squeeze); the five `.sh` rows (9, 11, 16, 17, 19), `cli.py` (10) and `package` (18) YELLOW, the six
PNG rows (12–15, 21, 23) GREY with a chip "screenshots and a diagram · redrawn in this video".
SAY: Clone the model training repo and move into it; pause and run it. Two extras show the course pin and the repo's files.

SHOW: TRACKER C2. Schematic console (`illustration`, no logo): search "Vertex AI API" → ENABLE →
"API enabled". `▶ your turn`. TRACKER C3: the quota page (`illustration`) with the README's own
labels (README.md lines 25–39): filter `Quota: Custom model training` → row `Custom model training
Nvidia T4 GPUs per region` → a few regions ticked → `EDIT QUOTAS` → "new limit" → `NEXT` → name →
`SUBMIT REQUEST`; among the ticked regions `us-central1` YELLOW with a chip "cli.sh's region ·
line 14". A README card (`README.md · lines 43–44`). A GREY chip: "cli.sh runs on CPU today · the
request is for later". `▶ your turn`.
SAY: In the console, enable the Vertex AI API. Then request GPU quota, an allowance per region. Filter for custom model training, pick T4 GPUs, include us-central1, where cli.sh runs, set a new limit and submit. Pause and do both. Approval may take hours or be refused; cli.sh runs on CPU without it.

SHOW: TRACKER C4. It types `cd ..` → (no output); prompt `student@laptop:~$`. Then `mkdir secrets`
(GREY chip "the README shows a tree, not a command") → TERM(laptop/04: → (no output)); then
`TRACKER C4 · extra`: `tree -L 1 .` (extra) → TERM(laptop/05: 2–6) beside a README card (`README.md · lines 55–58`), the
two trees matching row for row. `▶ your turn`. On V1 a GREEN `secrets/` drawer settles beside the
laptop's repo, outside it.
SAY: Next, a secrets folder beside the repo, never inside it; pause and make it.

SHOW: TRACKER C5. Console `illustration` (README.md line 62–64's values): "IAM & Admin → Service
accounts" → "Create · model-trainer" → three role chips "Storage Admin", "AI Platform Admin",
"Vertex AI Administrator" → "Actions ⋮ → Manage keys → JSON → Create"; a file icon drops into
`secrets/` and is renamed `model-trainer.json`. `▶ your turn`. TRACKER C5 · extra: `ls -la secrets`
(extra) → TERM(laptop/06: 2–5); line 5's file name highlighted (not its size), GREY tag `stand-in`.
SAY: Then the identity: a service account called model trainer, with Storage Admin, AI Platform Admin and Vertex AI Administrator, and one JSON key saved in secrets as model-trainer.json. Pause and create yours.

SHOW: The honest card (GREY), three lines building on their sentences: "This recording machine has
no Google credentials, no W&B account, no GPU and no browser." · "The key in that listing is an
obviously invalid stand-in, moved out before the first container start." · "Every cloud step shows
the failure a misplaced key gives." (one line per content sentence below). On "named sources", two
GREY chips settle under it: `recorded · source named`, `extra · local stand-in`.
SAY: One honest note. This recording machine has no Google credentials, no W and B account, no GPU and no browser. The key in that listing is an obviously invalid stand-in, moved out before the container starts. So each cloud step shows the failure a misplaced key gives, and successes come from named sources.

SHOW: TRACKER C6. Console `illustration`: "Create bucket · `your-bucket-placeholder`" beside a README
card (`README.md · line 71`, the instructors' bucket name with its own "[REPLACE WITH YOUR BUCKET
NAME]"). TRACKER C6 · extra, a strip:
`curl -s -w 'HTTP %{http_code}\n' https://storage.googleapis.com/storage/v1/b/your-bucket-placeholder`
(extra; folds) → TERM(laptop/07: 5, …, 15); then
`curl -s -w 'HTTP %{http_code}\n' https://storage.googleapis.com/storage/v1/b/cheese-app-trainer`
(extra; folds) → TERM(laptop/08: 5 wrap, …, 17), chip "the README's name · taken · replace this with
yours". `▶ your turn`. On V1 the bucket lights with the placeholder name. GOLD `cost_tag()`: "the
bucket stores your tarball (tiny) and any experiment folders · see the Cloud Storage pricing page".
SAY: Then create a bucket with your own name; pause and create it. Two extras show why: our placeholder returns 404, it exists nowhere, while the README's name returns 401, it belongs to someone else. A gold tag: the bucket stores your code and experiment folders.

SHOW: TRACKER C7. A W&B page `illustration`: "User settings → API keys", the key as dots, "Copy".
A README card (`README.md · line 80`): "Set an environment variable using your terminal: `export
WANDB_KEY=...`". In the laptop terminal it types the capture's line,
`export WANDB_KEY=PLACEHOLDER_NOT_A_REAL_WANDB_KEY_0000000; echo ${#WANDB_KEY}` (GREY chip "README:
`...` = your key · ours: an obvious placeholder"; the `; echo …` part tagged `extra`, `TRACKER C7 ·
extra` while it is on screen) → TERM(laptop/10: 2), `40` with a chip "the placeholder's length ·
the check: not 0 · and the trainer's pinned wandb 0.15.11 accepts only 40 (scene 11: `84:14`,
`87:14`)". `▶ your turn`. An optional GREY chip, tagged `extra · not captured`: "keep it out of
your shell history: `read -rs WANDB_KEY && export WANDB_KEY` (bash, zsh)". On V1 a GREEN key chip
settles in the laptop's shell.
SAY: Last, copy your W and B key and export it in the terminal you'll use for the container. Pause and do it. An extra echo prints its length, 40 for our placeholder. It must not be zero, and the trainer's pinned wandb accepts exactly 40.

SHOW: A second terminal slides in (title `laptop · new terminal`, prompt `student@laptop:~$`),
empty.
PONDER(6 s, "You exported the key, closed the terminal,\nopened a new one. What does\necho ${#WANDB_KEY} print?")
SAY: Something to ponder. You exported the key, closed that terminal, and opened a new one. What does the same echo print now?

SHOW: The answer: `echo ${#WANDB_KEY}` (extra) → TERM(laptop/11: 2), `0` RED. The terminals fade.
Part-1 close on V1: the Colab lane lit, the repo lane dashed, the GREEN key chip in the laptop's
shell, the bucket named; the hollow TEAL cockpit flickers. Caption: "next: the cockpit — and today
it won't build". Fade to an empty frame (end of part 1).
SAY: Zero: an exported variable exists only in that shell and its children. Part 1 is done: the key is set, the bucket has a name. Next, we build the cockpit, and today it won't build.

---

## S08 · The cockpit that won't build: two one-line fixes — `s08_build.py` · `TwoFixes`

SHOW: On "Part 2 ships the trainer", V1's repo lane flashes in the three spoken stages (cockpit →
bucket → job tile), then dims. TRACKER D1 (tracker D appears: "model-training › Run Container", 2
dots + 2 `extra` rows). GREY tag `lecture_ref(13, "24")` on V1's cockpit box, with a GREY chip "the
build itself is tutorial-only". Laptop terminal, prompt `student@laptop:~$`, with a GREY chip "same
terminal as your export · new terminal? export again first": `cd model-training` → (no output). A
README card (`README.md · lines 93–94`, the instructors' bucket and project with the README's own
"[REPLACE …]" notes; GREY chips "replace this with yours" and "project ID, not its name · keep
gs://"). It types the edit (GREY chip "our editor; use yours · this sed -i is GNU syntax · macOS sed:
sed -i ''"; the `sed` of TERM laptop/20's line 1; folds) → TERM(laptop/20: 2–6), lines 5–6
`gs://your-bucket-placeholder` and `your-gcp-project` GREEN. `▶ your turn`.
SAY: Part 2 ships the trainer: build the cockpit, pack the code, send one job. Put your bucket and project on lines 8 and 9 of docker-shell.sh; pause and edit yours.

SHOW: A kind card, tag `erratum`: README cards (`README.md · lines 100–101`, the arm64 build line)
and (`README.md · line 110`, `-e WANDB_KEY=$WANDB_KEY \ [MAKE SURE YOU HAVE THIS VARIABLE SET]`), a
GREY chip "the README's listing is not the file · edit docker-shell.sh itself". Then
CODE(docker-shell.sh: 12–24): line 14 (`--platform=linux/amd64`) YELLOW; line 17 (`--rm --name …`)
GREY; lines 18–19 become two GREY→TEAL pipes on V1 ("your code → /app", "secrets → /secrets");
lines 20–23 stick on as four notes; a GREY chip "no -p · it serves nothing". CODE(docker-shell.sh:
3) small beside it, `set -e`.
SAY: A small slip: the README's copy of this script is not the real file. It has notes in brackets and an older line for Apple chips, so edit the script itself. It builds for amd64 and mounts your code and secrets.

SHOW: TRACKER D2. A README card (`README.md · lines 114–115`). It types `sh docker-shell.sh` →
TERM(laptop/21: 23, …, 65–70, …, 166, …, 181–188 wrap) — every `[IP: …]` tail cut; the three `Err:`
rows and their `404  Not Found` RED, line 166 RED, the `Dockerfile:18` frame (181–187) with lines
18–19 RED. `▶ your turn`. A GREY chip "22 packages · all 404" and, on "before docker run", CODE
chip `set -e` flashes. V1's cockpit outline cracks RED.
SAY: Now run sh docker-shell.sh from inside the repo; pause and run it. Today it fails at step 2 of 14. All 22 packages return 404 Not Found from the Debian mirror, and the build stops at line 18. The script's set dash e, exit on error, then stops it before docker run.

SHOW: The error panel shrinks to a strip.
PONDER(8 s, "Every error is a 404 from a Debian mirror,\nand your internet works. Which line of\nthe Dockerfile picks your Debian?")
SAY: Something to ponder. Every error says 404 from the Debian mirror, and your internet works. Which line of the Dockerfile picks your Debian?

SHOW: The answer: CODE(Dockerfile: 1–2), line 2 `FROM python:3.13-slim-bullseye` YELLOW. On V1 the
cockpit's ORANGE base layer is labelled "bullseye · Debian 11"; a GREY chip: "on 2026-10-23 its
security mirror lists packages it no longer serves · they are on archive.debian.org · at the time
of recording". TRACKER D · extra, row "fix 1 · Dockerfile:2": it types the `sed` of TERM
laptop/22's line 1 (extra; folds; GREY chip "our editor; use yours · macOS sed: sed -i ''") →
TERM(laptop/22: 2–3), line 3 GREEN and shown large as "your new line 2"; the ORANGE base swaps to
"bookworm · Debian 12". `▶ your turn`.
SAY: Line 2, the FROM line. Bullseye is Debian 11, and at the time of recording its security mirror lists packages it no longer serves; they moved to an archive. The first fix, an extra, switches the base to bookworm, Debian 12; pause and make it.

SHOW: TRACKER D2. It types `sh docker-shell.sh` → TERM(laptop/23: 330, …, 344–348, …, 356, …,
372–378); steps 2–7 tick GREEN on a small step counter; line 348 `google-cloud-cli` YELLOW, line
356 RED, the `Dockerfile:36` frame with line 37 RED. A GREY chip: "renamed by Google · no
Kubernetes plugin needed here". `▶ your turn`.
SAY: Pause and run it again. Now it stops at step 8: google-cloud-sdk has no installation candidate, and google-cloud-cli replaces it. Google renamed its apt package.

SHOW: TRACKER D · extra, row "fix 2 · Dockerfile:37": it types the `sed` of TERM laptop/24's line 1
(extra; folds; GREY chip "our editor; use yours · macOS sed: sed -i ''") → TERM(laptop/24: 2–4),
line 4 GREEN and shown large as "your new line 37"; the ORANGE apt layer relabels
`google-cloud-cli`. `▶ your turn`. Then `git diff --stat; git diff Dockerfile` (extra) →
TERM(laptop/25: 2–4, …, 11–12, …, 20–21); line 4 `2 files changed, 4 insertions(+), 4 deletions(-)`
YELLOW (either editing route ends here).
SAY: The second fix, also an extra: install google-cloud-cli instead, on line 37; pause and make it. An extra git diff shows everything you changed: your two values, the two fixes, and nothing else.

SHOW: TRACKER D2. It types `sh docker-shell.sh` → TERM(laptop/26: 3, …, 19, …, 32, 34–36); line 3
`[+] Building 314.2s (19/19) FINISHED` with `at the time of recording` and a chip "much slower
emulated on Apple Silicon"; line 34 `Container is running!!!`; line 35 (`ERROR:
(gcloud.auth.activate-service-account) Unable to read file [/secrets/model-trainer.json] …`, wrap)
RED with a GREY chip "the honest no-key state"; line 36 `Updated property [core/project].`. `▶ your
turn`. V1's cockpit becomes solid TEAL.
SAY: Pause and run it a third time: it builds, about 5 minutes here, longer on Apple Silicon, where amd64 is emulated. The banner says running, then gcloud cannot open the key file: our missing key. With yours, this line confirms the service account. The script carries on anyway, because the entrypoint has no set dash e.

SHOW: TERM(laptop/26: 37–41) prints under it: `Architecture: x86_64` (chip "x86_64 on a Mac too ·
built for amd64"), `Environment ready! Virtual environment activated.`, `Python version: Python
3.13.17`, `UV version: uv 0.13.5 (x86_64-unknown-linux-gnu)` (both with `at the time of
recording`), `Activating virtual environment...`; then the prompt `root@<id>:/app#` with a GREY
chip "root · the id changes every run". A kind card, tag `erratum`: CODE(docker-entrypoint.sh:
13–19), line 13 vs line 19 YELLOW, "a label, not a fact". Fade out.
SAY: The architecture is x86 64, on a Mac too; the versions are on screen. A small slip: activated is printed before the activation, a label, not a fact.

---

## S09 · What goes in the tarball — `s09_package.py` · `InsideTheTarball`

SHOW: TRACKER E1 · extra (tracker E appears: "model-training › Package & Upload Python Code", 3
dots). GREY tag `lecture_ref(13, "23–24")` top right, whole scene. Cockpit prompt `root@<id>:/app#`
(same cockpit as S08, `26`). It types, one after another: `ls -la /secrets` (extra) →
TERM(laptop/26: 43–45); `echo $GCP_PROJECT $GCS_BUCKET_URI ${#WANDB_KEY}` (extra) →
TERM(laptop/26: 47), the last field `40` YELLOW, `▶ your turn`, GREY chip "0? exit · export
WANDB_KEY=… · sh docker-shell.sh"; `which python gcloud gsutil uv` (extra) → TERM(laptop/26: 49–52);
`gcloud --version` (extra) → TERM(laptop/26: 54, …, 61); `python -c "import
google.cloud.aiplatform as aip; print(aip.__version__)"` (extra; folds) → TERM(laptop/26: 64);
`590.0.0` and `1.120.0` with `at the time of recording`. Then `python -c "import tensorflow"`
(extra) → TERM(laptop/26: 66, …, 69), line 69 RED. V1's cockpit gets its stamp: "submits · never
trains". A host strip (`student@laptop:~/model-training$`): `docker image ls model-training-cli`
(extra) → TERM(laptop/27: 2–3; squeeze), `2.59GB` with `at the time of recording`.
SAY: Inside the cockpit, a few extra checks. Slash secrets is empty, our sandbox. Project, bucket and key came through; gcloud, gsutil and uv are here. Pause and check yours: the last number must be 40, not 0. But importing TensorFlow fails: this container submits jobs, it never trains.

SHOW: TRACKER E1. CODE(package/setup.py: 5–13): line 5 `REQUIRED_PACKAGES = ["wandb==0.15.11"]`
GREEN; line 11 `packages=find_packages(),` YELLOW → V4: a GREEN `trainer/` folder with
`__init__.py` lit (chip "this file makes it a package"). An ORANGE layer floats beside it:
"TensorFlow · scikit-learn — assumed from Google's image", tag `erratum`, chip "expected in
tf-cpu.2-17 · not verified here"; a GREY chip beside the GREEN pin: "requests: via wandb". A small
GREY chip (slides vs code): "uv.lock pins the cockpit, not the trainer". `▶ your turn` (open the
file).
SAY: Review setup.py; pause and open it. It is the label pip uses to install the tarball. The only declared dependency is wandb, pinned to 0.15.11. Its find packages call finds the trainer folder because the folder has its own init file, so once installed, python dash m trainer dot task works. TensorFlow and scikit-learn are not declared: they are assumed to come from the image Google provides, and scene 11 shows the tarball lacks them. Requests only arrives because wandb needs it.

SHOW: TRACKER E2. CODE(package/trainer/task.py: 45–54): line 52 `default="16"` YELLOW, pin "scene
11". Then two small panels: CODE(package/trainer/task.py: 96–100) (chip "from a GitHub release ·
the job can't see your laptop") and CODE(package/trainer/task.py: 152–153) (chip "after the
download"). `▶ your turn` (open the file).
SAY: Review task.py next; pause and open it. The notebook choices are flags now, and the key flag defaults to the text 16: remember that. The data comes from one GitHub release, since the job cannot see your laptop, and the W and B login runs after that download.

SHOW: TRACKER E3. V4 step 2: `task.py` and `__init__.py` drop into `trainer/`, `setup.py` clips on
as a label (`install_requires = wandb==0.15.11`), `tar` wraps `package/`, `gzip` shrinks it. A
README card (`README.md · lines 128–129`). At the cockpit prompt a GREY chip: "our capture: a fresh
cockpit for this step · stay in yours". It types `sh package-trainer.sh` → TERM(laptop/30: 43–50, 51
cut, 52); line 51 GREY chip "new notice · harmless"; line 52 RED. `▶ your turn`. A PINK `gsutil cp`
arrow reaches the bucket and stops at a RED "404". CODE(package-trainer.sh: 1–4), line 4 YELLOW,
chip "fixed name · a new upload overwrites the old one". A GREY chip, no panel: "with your bucket:
`gsutil ls $GCS_BUCKET_URI` lists cheese-app-trainer.tar.gz" (the command of `30:64`; its output
here is the placeholder's 404 and is not shown).
SAY: Now pack it: run sh package-trainer.sh inside the container; pause and run it. Tar lists eight entries, and the upload fails: our placeholder bucket does not exist. Line 4 uses a fixed name, so each upload overwrites the last.

SHOW: TRACKER E3 · extra. `ls -l trainer.tar.gz` (extra) → TERM(laptop/30: 54), `4016` YELLOW;
`tar tzvf trainer.tar.gz` (extra) → TERM(laptop/30: 56–63; squeeze), `10253` beside `task.py`
YELLOW. The host strip: `ls -l trainer.tar.gz; git status --short; git check-ignore -v
trainer.tar.gz` (extra; folds) → TERM(laptop/31: 2–5); `root` and `.gitignore:4` YELLOW, chip on
`root`: "Linux engine · Docker Desktop: your user".
SAY: Extra checks: the tarball is 4,016 bytes. On our Linux engine it belongs to root, because the container wrote it; on Docker Desktop, to you. Git ignores it either way.

SHOW: V1 with the cockpit, the `/app` mount pipe, the bucket holding the tarball, a job tile.
PONDER(6 s, "You fix a typo in task.py.\nRebuild the image, re-run\npackage-trainer.sh, or both?")
SAY: Something to ponder. You fix a typo in task.py. Do you rebuild the image, run the package script again, or both?

SHOW: The answer: only `sh package-trainer.sh` lights YELLOW; on V1 only the GREEN tarball crosses
to BLUE, the TEAL cockpit stays GREY-side, and the `/app` pipe glows ("already sees your edit").
GOLD `cost_tag()`: "the tarball is stored in your bucket · tiny". Fade out.
SAY: Only the package script. Vertex AI runs the tarball in your bucket, and your image never travels. The cockpit mounts your code folder, so it already sees the edit. A gold tag: the tarball is stored in your bucket, and it is tiny.

---

## S10 · One command, and a key inside it — `s10_submit.py` · `OneCommand`

SHOW: TRACKER F1 (tracker F appears: "model-training › Create & View Jobs in Vertex AI", 5 dots).
GREY tag `lecture_ref(13, "22, 24–25")` top right, whole scene. CODE(cli.sh: 5–19) (a 12-line
window that scrolls): line 5 `openssl rand -hex 6`, line 7 `n1-standard-4`, line 8 `REPLICA_COUNT=1`,
line 9 the **GPU** image YELLOW, lines 10–11 package and module, 12–13 accelerator, 14 region, line
19 `CMDARGS` with `--wandb_key=$WANDB_KEY` outlined GREEN; on line 10 (`PYTHON_PACKAGE_URI=…`) a
PINK arrow to the tarball in the bucket. `▶ your turn` (open the file). Beside the window, V4 step
3's job-spec card assembles one chip per spoken item (name, machine, image, package URI, module,
`--args`), so the later `sh -x` trace confirms it.
SAY: Review cli.sh; pause and open it. It names the job with random hex, asks for one n1-standard-4 machine, and sets a GPU image. Then it points at your tarball in the bucket and the module to run, and builds the arguments, ending with your W and B key.

SHOW: CODE(cli.sh: 21–37): lines 22–27 GREY (commented out), line 31
`export EXECUTOR_IMAGE_URI="us-docker.pkg.dev/vertex-ai/training/tf-cpu.2-17.py310:latest"`
YELLOW, lines 32–37 the one `gcloud ai custom-jobs create` that runs. A kind card, tag `erratum`:
README card (`README.md · lines 152–154`) with a chip "already done in cli.sh · commit 3efb2d5";
TRACKER F3 flashes with the caption "already the default". A small README card (`README.md · lines
136–142`) with a GREY chip "may be out of date · check Google's current list" (not spoken).
SAY: Further down, the GPU block is commented out and line 31 swaps in the CPU image, so only the CPU command runs. A small slip: the README shows GPU first and CPU as optional, but the script already runs on CPU.

SHOW: TRACKER F2. First the GOLD `cost_tag()`: "the job's VM bills while it is up: from provisioning
until the script exits · see the Vertex AI pricing page"; V4 step 3: the assembled job-spec card
(worker-pool chips, `--python-package-uris`, `--args` with the key still GREEN) flies from the
cockpit to Vertex AI, and a BLUE job tile appears with a GOLD meter (no numbers). On "key length", a
GREY chip "scene 9's check: the last number · 40 for wandb 0.15.11". A README card (`README.md ·
line 150`). Cockpit prompt `root@<id>:/app#` (GREY chip "our capture: a fresh cockpit for this step
· stay in yours"). It types `sh cli.sh` →
TERM(laptop/40: 43–44, …, 47); line 43 `Using endpoint [https://us-central1-aiplatform.googleapis.com/]`
GREEN, line 44 RED. `▶ your turn`. TRACKER F2 · extra: `gcloud auth list` (extra) →
TERM(laptop/40: 58), RED. On V5's preview the GREEN key-file badge is missing from the cockpit's
lanyard. A GREY chip, no panel: "with your key: gcloud reports the job as created".
SAY: A gold tag first: once the job's machine is provisioned, your project pays until the script exits. Check that your key length is 40; if not, watch scene 11 before you submit. Now sh cli.sh; pause and run it. The first line is real: the Vertex AI endpoint in us-central1. Then it stops with no active account, because the key never loaded; an extra auth list confirms it. With your key, gcloud reports the job as created.

SHOW: TRACKER F2 · extra. It types `sh -x cli.sh` (extra) → TERM(laptop/40: 64–66, 69, 75–77 wrap)
— the hex in 65–66 and 77 rendered `<12 hex>`; line 69 (the GPU image) YELLOW, then line 76 (the
CPU image) strikes it through; line 77 folds into chips: `--worker-pool-spec=machine-type=n1-standard-4`
· `replica-count=1` · `executor-image-uri=…tf-cpu.2-17.py310:latest` · `python-module=trainer.task`,
then `--args=--model_name=mobilenetv2,--train_base,--epochs=2,--batch_size=32,--wandb_key=PLACEHOLDER_NOT_A_REAL_WANDB_KEY_0000000`
with the key RED. V5's GREEN W&B badge turns RED.
SAY: An extra trace with sh dash x shows the job it tried to send. The GPU image is set, then overridden by the CPU image. Then the full command. The worker pool spec is the job's machine order: machine type, one replica, meaning one machine, image and module. Last come the arguments, ending with your W and B key in plain text.

SHOW: The RED badge, large.
PONDER(8 s, "Your W&B key is now part of the\njob's arguments. Who can read it later?")
SAY: Something to ponder. Your W and B key is now part of the job's arguments. Who can see it later?

SHOW: The answer: a GREY viewer icon looks over the badge's shoulder; chips settle: "anyone who can
view jobs in this project (the job spec keeps --args)" · "your shell history, if typed inline" ·
"use a dedicated key · rotate it at the end" · "Secret Manager: exercises".
SAY: Anyone who can view jobs in this project, because the job spec keeps its arguments, plus your shell history if typed inline. Use a dedicated key and rotate it at the end; the exercises use Secret Manager.

SHOW: TRACKER F2 · extra. The second terminal (`laptop · new terminal`, prompt
`student@laptop:~/model-training$`, the key never exported): `sh docker-shell.sh` →
TERM(laptop/70: 34, …, 41); prompt `root@<id>:/app#`. `echo ${#WANDB_KEY}` (extra) →
TERM(laptop/70: 43), `0` RED; `sh -x cli.sh 2>&1 | grep -o -- "--args=.*"` (extra; folds) →
TERM(laptop/70: 45), `--wandb_key=` RED. A GREY chip: "fix: exit · export · sh docker-shell.sh".
A third strip (`laptop`), while that cockpit is open: `sh docker-shell.sh` → TERM(laptop/71: 34
wrap, the container id rendered `"…"`), RED, with a GREY chip "fixed name: model-training-cli". Fade
out.
SAY: The other way it goes wrong: a terminal where the key was never exported. Inside, its length is 0, and the arguments end with an empty key. So the job would download its data, and only then fail at login. Exit, export, and start again; first exit any old cockpit, which holds the name.

---

## S11 · Who submits, who runs — `s11_identity.py` · `WhoRunsIt`

SHOW: No tracker for the badges beat. GREY tag `lecture_ref(13, "24")` top right, whole scene. V5
`ThreeBadges`: three badges on three lanyards. The first, GREEN key file → `model-trainer`
(submitter), with three role chips (Storage Admin · AI Platform Admin · Vertex AI Administrator,
README.md line 62); an arrow from the cockpit to the bucket ("write") and to Vertex AI ("create
job").
SAY: Three badges take part in every job. The first is your key file, for the model trainer service account. Its three roles let it write to your bucket and create jobs: it submits.

SHOW: The third badge, the W&B key, RED since S10, carried by hand inside `--args` to the separate
BLUE `wandb.ai` building. The middle lanyard hangs empty, with a GREY "?" on it.
SAY: The third is your W and B key, for a different building altogether, carried by hand inside the job's arguments. The middle lanyard is still empty.

SHOW: The private bucket glows; the key file sits on the laptop.
PONDER(8 s, "The job installs your package from your\nprivate bucket, but your key never left\nyour laptop. How?")
SAY: Something to ponder. The job installs your package from your private bucket, but your key file never left your laptop. How?

SHOW: The answer: the second badge settles on the middle lanyard, ORANGE, Google-managed: "Vertex AI
Custom Code Service Agent · service-…@gcp-sa-aiplatform-cc" (runner, by default, digest §3.5); it
rides the job tile and holds no key of yours (the GREEN key file stays GREY-side). The ORANGE badge
opens the bucket (same project); the GREEN key file's job was only the submit arrow. A GREY chip: "a
403 on your bucket → grant this identity access".
SAY: The second badge: your project's Vertex AI service agent, a service account Google manages. By default the job runs as it, and it can open buckets in the same project. Your key only proved who submitted. If a job ever gets a 403 on your bucket, that is the identity to grant access.

SHOW: First the real V4 step 4, once, GREY tag "what Vertex does · drawn, not recorded", no output
panels: a BLUE VM materialises (GOLD meter on), Google's TEAL image drops in with its ORANGE layer
(chip "expected · not verified here"), the GREEN tarball unwraps, `pip install` adds wandb, then
`python -m trainer.task --model_name=mobilenetv2 --train_base --epochs=2 --batch_size=32
--wandb_key=…`: S10's `--args` string splits at its commas into argv tokens that land on S09's
`task.py` flag lines. Then a dashed TEAL container labelled "plain python:3.10 · not Google's image"
replaces the BLUE VM. TRACKER F2 · extra (variant `extra · local stand-in`). A laptop strip
(prompt `student@laptop:~/model-training$`):
`docker run --name trainer-standin -v "$PWD/trainer.tar.gz":/tmp/trainer.tar.gz python:3.10-slim-bookworm pip install /tmp/trainer.tar.gz`
(extra; folds; small) → TERM(laptop/80: 2, …, 68, 70 wrap) — line 70 folds into six rows, so
`cheese-app-trainer-0.0.1` and `wandb-0.15.11` are on screen, both YELLOW. On the dashed container
the tarball unwraps and `pip install` adds wandb.
SAY: On Vertex, the job's first step installs your tarball into Google's image. We can't run Vertex here, so we rerun that step on the laptop, tagged as a stand-in. In a plain Python 3.10 container, pip installs the tarball: your package, plus wandb 0.15.11.

SHOW: `docker commit trainer-standin trainer-standin >/dev/null && docker rm trainer-standin` (extra;
folds; small) → TERM(laptop/81: 2) (it saves the stand-in as an image for the next runs). Then
`docker run --rm trainer-standin pip list` (extra) → TERM(laptop/82: 2–3, …, 7, …, 19, …, 26;
squeeze), then a GREY chip "no tensorflow · no scikit-learn". The ORANGE layer slot on V4 stays
empty. `for i in tf-cpu.2-17.py310 …` (tag plain `extra`: a live manifest check of Google's real
image, not a stand-in; folds; small) → TERM(laptop/09: 2–3), `4.31 GB compressed` with `at the time
of recording`; the ORANGE layer slot fills only inside a TEAL band labelled `tf-cpu.2-17.py310`,
GREY chip "expected in tf-cpu.2-17 · not verified here". Then
`docker run --rm --network none trainer-standin python -m trainer.task --help` (extra; folds) →
TERM(laptop/83: 2, …, 7–9), line 9 RED.
SAY: An extra pip list shows wandb, requests and their helpers, but no TensorFlow and no scikit-learn. The trainer counts on the prebuilt image for those, which we did not pull to check. Without it, the trainer cannot even print its help.

SHOW: The trainer's first W&B step: CODE(package/trainer/task.py: 152–153). Three keys, three
strips, the ProxyError lines never printed:
`docker run --rm --network none trainer-standin python -c "import wandb; wandb.login(key='')"`
(extra; folds) → TERM(laptop/85: 2), RED, chip "the empty key from scene 10 · on Vertex: after the
download, on billed machine time"; `… wandb.login(key='16')"` → TERM(laptop/84: …, 14) (line 3,
printed before the check, is not shown), line 14 RED, chip "the default `\"16\"`"; `…
wandb.login(key='PLACEHOLDER_NOT_A_REAL_WANDB_KEY_0000000')"` → TERM(laptop/86: 4), YELLOW (not
GREEN), chip "length check only · offline · nothing asked W&B". (Each command is typed in full,
folded, small.)
SAY: Then the trainer's first W and B step, line 153, with three keys. The empty key from scene 10 fails with api key not configured, and on Vertex that comes after the data download, on billed machine time. The default of 16 fails: API key must be 40 characters long, yours was 2. Our 40 character placeholder passes the offline length check, and nothing more.

SHOW: One more strip: `… wandb.login(key='PLACEHOLDER_NOT_A_REAL_WANDB_KEY_0000000_LONGER')"`
(extra; folds) → TERM(laptop/87: 14), `yours was 47` RED. A GREY card: "wandb 0.15.11 accepts
exactly 40 characters · today's key format: not checked · a different length? raise the pin, then
sh package-trainer.sh again · a tested route: see the study guide". Fade out.
SAY: One more: this old wandb pin accepts exactly 40 characters, and 47 fails. We could not check which key format W and B gives out today. If yours differs, the study guide has a workaround.

---

## S12 · What the job prints, what W&B can show — `s12_logs.py` · `WhatTheJobSays`

SHOW: TRACKER F4. GREY tag `lecture_ref(13, "9–10, 15–16, 25")` top right, whole scene. A README
card (`README.md · lines 157–158`). A console `illustration`: "Vertex AI → Training → Custom jobs",
one row `cheese_training_job_<12 hex>`, no status values, no durations; GREY chip "a custom job ·
not a training pipeline". The row opens to a job page wireframe with a "logs" link (`illustration`;
the console's labels were not captured), which leads to the log shape below. `▶ your turn`.
SAY: To view jobs, open Vertex AI, then Training, then Custom jobs; pause and look for yours. It is a custom job, not a training pipeline, so look on that tab. Open your job and follow its logs link; wait for the line training job complete.

SHOW: A log panel, tag `illustration · built from task.py's print lines`, every line labelled with
its source line in a GREY gutter: `tensorflow version …` (:57), `Number of replicas: …` (:61),
`GPU Available: …` (:67), `Downloading data...` (:94), `Download execution time (mins) …` (:102),
`Labels: […]` (:107), `Full size of the dataset: 1156` (:122), `train_x count: 936`,
`validate_x count: 104`, `test_x count: 116` (:148–150) — the four values with the tag `recorded ·
notebooks A/B` (NB(A: 353, 445–447), NB(B: 410, 502–504)).
SAY: What will the job print? No job log exists for this video, so here is its shape, built from the code's own print lines. The counts are the ones both notebooks printed for the same code.

SHOW: The `Labels:` line splits into two, NB(A: 352) and NB(B: 409), the two orders side by side
(chip "os.listdir has no order · no label map is saved", tag `erratum`), a YELLOW chip "class 0:
brie in A · gruyere in B", and S03's pin icon returns beside it. Then `Train model` (:269),
the model summary as a GREY block ending in a stray `None` (:308, chip "print(model.summary())");
where `model.fit` runs, a GREY-dashed gap "no recording of this part"; `Training execution time
(mins) …` (:333); `Training Job Complete` (:341).
SAY: The labels line has no fixed order, as the two notebooks show, and no label map is saved. The summary ends with a stray None, because the code prints what summary returns. Training itself is a gap here, with no epochs, loss or times, then the line training job complete.

SHOW: TRACKER F5. A README card (`README.md · lines 161–163`, "You will view the training metrics
tracked and automatically updated"), tag `erratum`, chip "not with this code · no callback". V2: the
repo run's row, tag `illustration` (coordinator decision), no dashboard chrome, **no numbers**:
project `cheese-training-vertex-ai` (task.py:314), run name `mobilenetv2_train_base_True` (:263,
:321), config keys as chips pointing to their sources — `learning_rate ← task.py:274`,
`epochs ← --epochs`, `batch_size ← --batch_size`, `model_name ← model.name`,
`execution_time ← :336` (inside the config chips) — a GREY chip "system charts · CPU · GPU · memory"
(named, not drawn), and the curve slots as ghost outlines (CODE(package/trainer/task.py: 326–331)
small, no `callbacks=`). `▶ your turn`.
SAY: To view metrics, the README sends you to the W and B project cheese training vertex AI. It promises training metrics, tracked and updated automatically. To put it kindly, not with this code. From task.py, the run named after the model gets its config, including the execution time, and system charts, and its curve slots stay empty. Pause and open your project.

SHOW: Slide 9's seven items become the row's columns (environment · code · data · model · metrics ·
artifacts · notes), all unticked.
PONDER(8 s, "Of the seven things a run record\nshould hold, which does this run record?")
SAY: Something to ponder, with the lecture's list of seven. Which of them does this run actually keep?

SHOW: The answer, ticked on V2's columns: model ✓ (hyperparameters); environment ◐ (chip "system
charts and run metadata · not the image tag (cli.sh)"); metrics ✗ ("execution_time is in config · no
metric logged"); artifacts ◐ ("logs ✓ · weights ✗", a dashed hole); code ✗ ("no commit"); data ✗
("a fixed release zip · an unseeded split"); notes ✗. On "notebook A", the hook's two tables slide
in small beside the ledger and the folder card from notebook A gets "no commit · no split (it keeps sizes and the label map, NB(A: 1412–1419)) · no notes". On "cannot crown",
S01's YELLOW question card returns small and its "?" resolves to "can't tell · yet". GREY chips:
"exercise 1: a LambdaCallback" · "exercise 3: seed the split". Fade out.
SAY: The model and its settings, yes. The environment only partly: system charts, while the image tag sits in cli.sh. Metrics, none: the execution time goes into the config. Logs yes, weights no. Code, data and notes, no: no commit, a fixed zip, and an unseeded split. The folder from notebook A has no commit, no split and no notes either. So the verdict: these tables cannot crown a recipe. Seed the split, match the epochs, keep the code version, then compare. Exercise 1 adds a small callback.

---

## S13 · Three switches for one GPU — `s13_gpu.py` · `ThreeSwitches`

SHOW: TRACKER F3 (caption "optional · read in reverse"). GREY tag `lecture_ref(13, "22, 24")` top
right, whole scene. CODE(cli.sh: 9–14) small, then CODE(cli.sh: 21–27) beside CODE(cli.sh:
30–37). V6 `GpuSwitchboard` inside a job tile: three switches in a row — **accelerator**
(`accelerator-type=NVIDIA_TESLA_T4,accelerator-count=1` in the worker pool: values from lines 12–13,
used on line 26),
**image** (`tf-gpu.*` with CUDA vs `tf-cpu.*`), **quota** (T4s for custom training in this region,
a regional stock counter). On "all three", the switches flip GREEN one by one and the T4 chip
lights.
SAY: Now the reverse of the README's optional CPU step: what would it take to train on a GPU? Three switches must agree. The accelerator: one T4 in the worker pool spec. The image: TensorFlow built for GPUs, with CUDA, the GPU libraries. And the quota: T4s for custom training in this region. The chip lights only when all three are on.

SHOW: The quota page from S07 (`illustration`) flashes by the quota switch. TRACKER F3 · extra:
cockpit-free laptop strip, the long loop of TERM laptop/09's line 1 (extra; folds; small) →
TERM(laptop/09: 2–7), the three sizes with `at the time of recording` (on screen, not spoken).
SAY: The quota is the console request from scene 7. An extra check shows Google still serves both GPU images, at the time of recording.

SHOW: CODE(cli.sh: 21–37): lines 22–27 uncomment (YELLOW), lines 30–37 comment out (GREY). V6
replay: with both blocks left live, two job tiles appear with the same name
`cheese_training_job_<12 hex>`, RED chip "two jobs, two bills".
SAY: To switch, uncomment the GPU block and comment out the CPU block. Leave both active, and you submit two jobs with the same name.

SHOW: A GREY honest card: "no GPU quota, no account here · the GPU block runs the same
gcloud ai custom-jobs create that failed in scene 10 · nothing new to show, nothing faked".
SAY: Here the GPU block would fail the same way as in scene 10, with no active account, so there is nothing new to show, and nothing we fake.

SHOW: GOLD `cost_tag()` on the T4 chip: "a GPU adds to the bill while it is attached, used or not ·
see the Vertex AI pricing page".
SAY: A gold tag: a GPU adds to the bill for as long as it is attached, used or not.

SHOW: The CPU block with `accelerator-type` added (drawn, GREY chip "a thought experiment").
PONDER(6 s, "You add accelerator-type to the CPU block.\nThe job runs; its log says\nGPU Available:  []. Why?")
SAY: Something to ponder. You add the accelerator to the CPU block. The job runs, and its log says GPU available, with an empty list. Why?

SHOW: The answer, V6 replay: the image switch is `tf-cpu` (CODE(cli.sh: 31) YELLOW), the T4 sits in
the slot, dark, while the GOLD meter still counts; the log line `GPU Available:  []` (task.py:67,
tag `illustration`). Chip "exercise 5". Fade out.
SAY: Line 31 sets a CPU image, which has no CUDA. The T4 is attached, idle, and still billed. Exercise 5 lets you try it.

---

## S14 · Two GPUs, one model — `s14_multigpu.py` · `TwoGpusOneModel`

SHOW: No tracker yet. GREY tag `lecture_ref(13, "26–30")` top right, whole scene. V7 opens with
slide 27's ladder, three rows: "one machine · one GPU — One Device", "one machine · many GPUs —
Mirrored" (YELLOW, "you are here"), "many machines — Multi Worker Mirrored" (GREY dashed). A kind
GREY chip under the first row: CODE(package/trainer/task.py: 60) "only counts replicas · the model
is built outside any scope".
SAY: The last idea of the lecture is multi-GPU training, in three shapes: one machine with one GPU, one machine with several, and several machines. Today is the middle one, the mirrored strategy. The single-GPU trainer also creates one, but only to count GPUs.

SHOW: Still no tracker: the picture comes before the code. V7 `MirroredReplicas`: one
`n1-standard-32` box with two T4s, each holding an identical
replica of the network (same colours). A global batch of 64 tiles splits 32 + 32; each GPU computes
gradients on its half (two arrows rise); the arrows meet on a PINK "all-reduce" link, average, and
return; both replicas update with the same colour change. Then `with strategy.scope():` is drawn as
a frame around model + optimizer + compile; the variables inside split into twin (mirrored)
variables; a model built outside the frame stays single, with a GREY chip "not mirrored".
SAY: Here is the idea. Each GPU holds an identical copy of the model, called a replica. A global batch of 64, one step's worth, splits into two halves of 32. Each GPU computes gradients on its half. The two are averaged across a link called all-reduce, and both copies take the same step, so they stay identical. Variables created inside the scope are mirrored, one synced copy per GPU; a model built outside is not mirrored.

SHOW: TRACKER G1 (tracker G appears: "model-training › OPTIONAL: Multi GPU Training", 4 dots).
CODE(cli-multi-gpu.sh: 4–16): line 6 `n1-standard-32`, lines 11–12 `NVIDIA_TESLA_T4` × 2, line
10 `trainer.task_multi_gpu`, line 16 `--epochs=5`; line 8 `tf-gpu.2-14.py310` with a kind chip,
tag `erratum`: "older than cli.sh's tf-cpu.2-17". `▶ your turn` (open the file).
SAY: Review cli-multi-gpu.sh first, in README order; pause and open it. It asks for one n1-standard-32 machine with two T4s, for 5 epochs. A small slip: its TensorFlow image is older, 2.14, where cli.sh uses 2.17.

SHOW: TRACKER G2. Slide 28 → 29 as three edits over CODE(package/trainer/task_multi_gpu.py:
286–301), then CODE(package/trainer/task_multi_gpu.py: 303–321), each tagged with the slide's own
call-out (SLIDES.md:46), one per spoken sentence, while V7 shrinks to a thumbnail beside the code:
BLUE "Create distribution Strategy" (287–289), GREEN "Adjust dataset batch size" (293, chip
"num_workers counts GPU replicas here, not machines"), RED "Create & Compile model in strategy
scope" (304–321).
`model.fit` (CODE(package/trainer/task_multi_gpu.py: 338–343), small) with a GREY "unchanged".
`▶ your turn` (open the file).
SAY: Then review the multi-GPU trainer; pause and open it. These are the lecture's three changes. It creates the mirrored strategy. It multiplies the batch size by the number of replicas. And it builds and compiles the model inside the scope of the strategy. Model fit is unchanged.

SHOW: The two GPUs and a stack of 936 training tiles.
PONDER(8 s, "Two GPUs, --batch_size=32, 936 training\nimages. Steps per epoch? Images per GPU\nper step?")
SAY: Something to ponder. Two GPUs, a batch size flag of 32, and 936 training images. How many steps per epoch, and how many images does each GPU see per step?

SHOW: The answer: `global_batch_size = 32 × 2 = 64` (CODE(package/trainer/task_multi_gpu.py: 293));
936 tiles fall in 15 batches, the last one partial (14 full + 40); "32 per GPU per full step". Two
config chips from CODE(package/trainer/task_multi_gpu.py: 324–334): `batch_size`,
`global_batch_size` (no values). Two caveat cards: "learning_rate = 0.001 (:275) while the batch
doubles" · "2 GPUs ≠ 2× faster: start-up, image pull and download don't shrink".
SAY: The global batch is 64, so 15 steps, the last one partial, and 32 images per GPU on each full step. Two caveats. The learning rate stays at 0.001 while the batch doubles. And two GPUs are not twice as fast, because start-up, image pull and download don't shrink.

SHOW: TRACKER G3: a GREY card "quota: 2 × T4 and 32 vCPUs of custom training, in your region"
over the quota page `illustration`. Then the GOLD `cost_tag()` on the 32-vCPU two-T4 box, before
the step: "the biggest machine of the lecture · check the Vertex AI pricing page before you press
enter". TRACKER G4: a README card (`README.md · line 170`). Cockpit prompt `root@<id>:/app#` (chip
"our capture: a fresh cockpit for this step · stay in yours"). It types `sh cli-multi-gpu.sh` →
TERM(laptop/50: 43–44), line 44 RED. `▶ your turn` with a GREY chip "optional · only with GPU quota".
Slide 30 in one GREY line, not spoken: "bucket, key and package: already done · only the launch
script changes". Fade out.
SAY: You need quota for two T4s and 32 virtual CPUs of custom training in your region. A gold tag: this is the biggest machine of the lecture, so check the pricing page first. If your quota came through, pause and run sh cli-multi-gpu.sh. Here it fails like cli.sh, with no active account.

---

## S15 · The missing model, teardown, recap — `s15_recap.py` · `Recap`

SHOW: No tracker. GREY tag `lecture_ref(13, "5–6, 9–10, 21")` top right, whole scene. Cockpit
prompt `root@<id>:/app#` (chip "our capture: a fresh cockpit"). It types `python cli.py` (extra)
→ TERM(laptop/60: 43, …, 47–48), line 48 `KeyError: 'GCP_REGION'` RED; CODE(cli.py: 7) small.
Then `export GCP_REGION=us-central1` (extra) → (no output); `python cli.py` (extra) →
TERM(laptop/60: 51–52, …, 119 wrap), RED. A GREY chip: "the Python SDK route · L15 · sends no
--wandb_key (scene 11: yours was 2)".
SAY: One launcher the README never mentions is cli.py, the Python SDK route. As an extra run, it fails at once, because only cli.sh sets the region variable. Export it, and it fails at the missing key file.

SHOW: V4 step 5: the job's script exits, the VM dissolves, the GOLD meter stops — and the trained
weights evaporate as a GREY-dashed ghost. Chips, tag `erratum`: "nothing calls model.save" ·
CODE(package/trainer/task.py: 27–30) small, "--model-dir and --lr: parsed, never used". V2's artifacts cell
stays "?". A GREY-dashed arrow to "L15 · saves the model to a bucket"; chip "exercise 4: today".
SAY: And where is the trained model? When the script ends, the machine is deleted, and the weights with it: nothing calls model save, and the model dir flag is ignored. Lecture 15 saves the model to a bucket; exercise 4 does it today.

SHOW: TRACKER cleanup 1 (`tracker_cleanup` appears: "extra · clean-up", 3 dots). The GOLD-framed
shutdown checklist card builds one line per sentence, in this order (every command shown, not run,
with no output panel):
(1) "in the cockpit: `gcloud ai custom-jobs list --region=us-central1` (finds the JOB_ID; the
capture's typed line `40:91`) · `gcloud ai custom-jobs cancel JOB_ID --region=us-central1` ·
nothing RUNNING or PENDING · tried cli.py? also check Training pipelines";
(2) "`gsutil rm $GCS_BUCKET_URI/cheese-app-trainer.tar.gz` · the `experiment_<ts>/` folders
(notebook B: under your account's folder) · or delete the bucket";
(3) "or in the console: Vertex AI → Training → Custom jobs → Cancel · Cloud Storage → your bucket →
delete";
(4) TRACKER cleanup 2: "then `exit` the cockpit (`--rm` removes it)". Laptop prompt
`student@laptop:~/model-training$`: `docker ps -a` (extra) → TERM(laptop/90: 2; squeeze), nothing
listed, chip "--rm"; `docker image ls` (extra) → TERM(laptop/91: 2–7; squeeze), `2.59GB` with
`at the time of recording`. Card line: "need the disk? `docker image rm model-training-cli
python:3.13-slim-bookworm python:3.13-slim-bullseye` · ran our extras? also `trainer-standin
python:3.10-slim-bookworm` · Linux: `sudo rm trainer.tar.gz`" (names from `91`);
(5) TRACKER cleanup 3: "notebook B: `wandb.finish()` · both notebooks: Runtime → Disconnect and
delete runtime";
(6) "end of term: delete the model-trainer key in IAM and its JSON in secrets · rotate your W&B key
and update the Colab secret `WandB` · the old export lives on in that terminal: open a new one".
`▶ your turn`.
SAY: Time to shut down; pause and work through the list. From inside the cockpit, or in the console, make sure no custom job is running or pending. Remove the tarball and experiment folders too. Then exit; an extra docker ps shows nothing left. Finish the last W and B run, and disconnect the Colab runtimes. At the end of term, delete the model trainer key and rotate your W and B key, which traveled in a job.

SHOW: The recap on V1, complete: one lit group per sentence (same relight order as before): "what
it keeps" → the folder of runs and the WHITE ledger with its seven columns (V2); "callback ·
config" → the shared axis with its one PURPLE pipe, and the drawer with config inside `init` (V3);
"Only the tarball travels" → the GREEN tarball crossing into Google's ORANGE-banded image while the
TEAL cockpit stays home (V4), the ORANGE service-agent badge (V5) and the job spec with the RED key;
"three switches · split the batch" → the three switches (V6) and the two replicas on their
all-reduce link (V7). Then everything unlit.
SAY: The whole lecture on one map. A run is only as useful as what it keeps. Curves need a callback; config goes into wandb init. Only the tarball travels, into Google's image, run as the service agent, your key in its arguments. One GPU needs three switches; two GPUs split the batch and average gradients.

SHOW: A card "Test yourself". One question at a time (≥ 24 pt, ≤ 3 lines), each with a thumbnail of
its picture; earlier ones collapse into a label list at left. Q1 "Notebooks A and B crowned different
MobileNets. Name two things neither table wrote down that you'd need before calling the difference
real." (the two tables) · Q2 "What travels from your laptop to Vertex AI, which image does it run
in, and what never makes the trip?" (the tarball trip) · Q3 "After wandb.config = {...}, the run's
config is {}. Why, and what is the one-line fix?" (the label on a loose dict) · Q4 "Which identity
submits the job, which runs it, and where does your W&B key end up?" (three badges) · Q5 "With
MirroredStrategy on two GPUs, what is split, what is averaged, and what must be created inside
strategy.scope()?" (two replicas). Labels: "two tables" · "the trip" · "the config" · "badges" ·
"replicas".
SAY: 5 questions to test yourself. One: what did neither table write down? Two: what travels to Vertex AI, and what never does? Three: why is the config empty? Four: who submits, who runs, and where does your key end up? Five: with two GPUs, what is split, averaged, and created inside the scope?

SHOW: The label list stays at left. Footer cards: "Answers: exercises.md" and "Study guide + every
command: MLOps_Learning · guides/L13-training-workflows.md". A "Next" card, GREY dashed: "L14 ·
serving containers, serverless" · "L15 · save this model, chain the steps in Pipelines (slide 21's
third entry)". Close on slide 5's three dials, the third lit, with a small ledger beside it.
Everything fades to an empty frame (end of part 2).
SAY: Answers are in the exercises. Next, lecture 14 serves containers without servers, and lecture 15 saves this model and chains the steps. Hardware rented, and a log of what you rented it for.

---

## Lexicon candidates

**Status after the v2 merge.** The flow review's Appendix B block (33 required keys plus the
optional `gsutil` and `scikit-learn`) is in `explainer/lexicon.yaml` (commit 09e7e2f): every
dotted file name, `wandb`, `us-central1`, `T4s`, `404`, `model dir`, `notebook A` / `Notebook A`
and every decimal the v1 script spoke now have entries; the rows below that needed one are
covered, and the rest were found fine as phonemized (flow review, Appendix A). v2 no longer speaks
2.19.0, 3.13.17, 0.13.5, 590.0.0, 1.120.0, 2.59, 4.31, 8.93 or 7.61 (on screen only; their keys are
harmless). New in v2: **67.24** (S04, "67.24 in notebook A, 68.97 here"): mid-sentence, it
phonemizes clean today (`sˈɪksti sˈɛvən pɔɪnt tˈuː fˈɔːɹ`); a robustness key beside 68.97 is
optional, needed only if an edit moves it to the end of a sentence. Every new or changed v2
sentence was phonemized with `KokoroBackend.phonemize`: no mid-sentence stop, no "a" before a key,
no "'s" after a key except `README's`. Avoided by rewrite: "opening's" (stressed on "-ING"), "reads"
(homograph rule), "notebook A's".

Words the SAY lines contain that `explainer/lexicon.yaml` has no entry for and Kokoro af_heart may
misread. **Not added**: the lexicon stage checks each with `explainer/voice.py` (phonemes) and adds
only the ones it gets wrong, each with `ipa` + `say`. The SAY lines already avoid a bare "a" and a
`'s` directly before every word below, so no "a X" guard is needed unless the reviewer adds one.
Nothing in the hex family is spoken: the commit (`b9aee1cc…`), the job-name hex and container ids
are on screen only. "W and B" is written as three words in SAY, so it needs no entry unless the
voice says "double-you" oddly; it is listed for the check.

| word as written in SAY | scenes | intended reading | why it is a candidate |
| --- | --- | --- | --- |
| TensorFlow | S03, S05, S06, S09, S11, S13, S14 | "tensor flow" | camel-case product name |
| MobileNet | S01, S04 | "mobile net" | camel-case model name |
| wandb (in "wandb init", "wandb config", "wandb finish", "wandb, pinned to", "this old wandb pin") | S04, S05, S09, S11, S15 | "W and B" | library name; would be read "wand-b" |
| W and B | S01, S02, S04–S07, S09–S12, S15 | "double-you and B" | written as three words; check the letter reading in "your W and B key" |
| Weights and Biases | S02 | "weights and biases" | probably fine; listed for the "biases" vowel |
| Vertex AI | S01, S02, S06, S07, S09–S12, S15 | "vertex A I" | product name; "AI" as letters |
| gcloud | S08, S09, S10 | "G cloud" | tool name |
| gsutil | S09 | "G S util" | tool name |
| uv | S08, S09 | "you-vee" | tool name; only `uv.lock`, `uv's`, `uvx` have entries |
| google-cloud-sdk | S08 | "google cloud S D K" | package name (L11 lists the same) |
| google-cloud-cli | S08 | "google cloud C L I" | package name (L11 lists the same) |
| apt | S08 | "apt" (one syllable) | Debian tool; may be spelled out |
| sed | S08 | "sed" | Unix tool |
| FROM (in "the FROM line") | S08 | "from" | capitals; may be spelled out |
| Bullseye, bookworm | S08 | "bullseye", "bookworm" | Debian code names; probably fine |
| Debian | S08 | "DEB-ee-an" | distribution name |
| Dockerfile | S08 | "docker file" | probably fine (`Dockerfile.txt` has an entry) |
| Kubernetes | S08 | "koo-ber-NET-eez" | product name |
| amd64 | S08 | "A M D sixty-four" | architecture name |
| x86 64 | S08 | "x eighty-six sixty-four" | architecture name (written as two tokens) |
| sh (in "sh docker-shell.sh", "sh package-trainer.sh", "sh cli.sh", "sh cli-multi-gpu.sh", "sh dash x") | S08, S09, S10, S14 | "S H" (as L10/L11 shipped it) | lowercase two-letter command |
| ps (in "docker ps") | S15 | "P S" | Unix command |
| Tar | S09 | "tar" | sentence-initial tool name |
| task.py | S09, S12 | "task dot pie" | file name |
| setup.py | S09, S11 | "setup dot pie" | file name |
| cli.sh | S07, S10, S12, S14, S15 | "C L I dot S H" | file name (`cli.py` has an entry) |
| package-trainer.sh | S09 | "package trainer dot S H" | file name |
| cli-multi-gpu.sh | S14 | "C L I multi G P U dot S H" | file name |
| model-trainer.json | S07 | "model trainer dot JSON" | file name |
| cheese-app-trainer.tar.gz | S09 | "cheese app trainer dot tar dot G Z" | object name |
| JSON | S07 | "jay-son" | check it is not spelled out |
| api (in "api key not configured") | S11 | "A P I" | lowercase, quoted from the error text |
| ID (in "run ID", "its ID") | S04, S08 | "I D" | `IDs` has an entry, `ID` does not |
| scikit-learn | S09, S11 | "sy-kit learn" | package name |
| MLflow | S02 | "M L flow" | product name |
| init (in "wandb init", "its own init file") | S04, S05, S09, S15 | "in-it" | Python abbreviation |
| dict | S05 | "dict" | Python type |
| hex | S10 | "hex" | probably fine |
| T4, T4s | S01, S03, S06, S07, S13, S14 | "T four", "T fours" | GPU name |
| n1-standard-4 | S10 | "N one standard four" | machine type |
| n1-standard-32 | S14 | "N one standard thirty-two" | machine type |
| us-central1 | S10 | "U S central one" | region name (`us-east-1` has an entry) |
| all-reduce | S14 | "all reduce" | hyphenated term |
| Unix | S03 | "you-nix" | probably fine |
| GitHub | S02, S03, S09 | "git hub" | probably fine |
| Workbench, Cheese App | S06, S02 | "work bench", "cheese app" | probably fine |
| 404 | S07, S08 | "four oh four" | status code ("401", "403" have entries) |
| 2.19.0 | S03 | "two point nineteen point zero" | new `a.b.c` version |
| 0.31.0 | S04 | "zero point thirty-one point zero" | new version; the entry "0.31" may splice inside it |
| 0.22.2 | S04 | "zero point twenty-two point two" | new version |
| 0.15.11 | S09, S11 | "zero point fifteen point eleven" | the wandb pin |
| 3.13.17 | S08 | "three point thirteen point seventeen" | new version ("3.13" has an entry) |
| 0.13.5 | S08 | "zero point thirteen point five" | new version ("0.13" has an entry) |
| 590.0.0 | S09 | "five ninety point zero point zero" | Cloud SDK version |
| 1.120.0 | S09 | "one point one twenty point zero" | Vertex AI library version |
| 2.14, 2.17 | S14 | "two point fourteen", "two point seventeen" | TensorFlow image versions |
| 3.10 (existing entry) | S11 | "three point ten" | confirm the entry fires in "Python 3.10 container" |
| 68.97, 62.93 | S01 | "sixty-eight point nine seven", "sixty-two point nine three" | two-decimal accuracies |
| 0.86 | S03 | "zero point eight six" | two-decimal number |
| 0.2, 0.001 | S03, S14 | "zero point two", "zero point zero zero one" | small decimals |
| 2.59, 4.31, 8.93, 7.61 | S09, S13 | "two point five nine", "four point three one", … | sizes in gigabytes |
| 1,156, 1,040, 4,016 | S01, S03, S09, S12 | "one thousand one hundred fifty-six", … | comma thousands; check not read as two numbers |
| 936, 104, 116 | S03, S12, S14 | "nine hundred thirty-six", … | three-digit counts; pick one style |
| 510 | S04 | "five hundred ten" | probably fine |
