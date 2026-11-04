# AC215 · Lecture 13 — Advanced training workflows: a run is a record, a job is a rented machine

A follow-along walkthrough of the Lecture 13 tutorial of Harvard's **AC215 (MLOps & LLMOps, Fall 2026)**,
*Advanced Training Workflows* (experiment tracking with W&B, serverless training on Vertex AI, multi-GPU):

- **Part 1:** the lecture's two Colab notebooks, *Cheese Classification Models* (notebook A) and *Experiment
  Tracking with W&B* (notebook B), shown from their stored outputs; then the setup sections of the tutorial repo.
- **Part 2:** [dlops-io/model-training](https://github.com/dlops-io/model-training), branch `main` @
  [`b9aee1c`](https://github.com/dlops-io/model-training/tree/b9aee1cc1923dd1f673093ad3ff5bb023049b4ff), `README.md`
  top to bottom: *Run Container*, *Package & Upload Python Code*, *Create Jobs in Vertex AI* (and its optional CPU
  step), *View Jobs*, *View Training Metrics* and *OPTIONAL: Multi GPU Training*. Today the README's
  `sh docker-shell.sh` no longer builds; the video shows both failures and the two one-line fixes
  (`Dockerfile:2` → `python:3.13-slim-bookworm`, `Dockerfile:37` → `google-cloud-cli`), kindly, as errata.

Two copies of the same notebook, the same 1,156 cheese photos, the same five models, and two different winners: which
recipe is better, and can you even tell from the tables? Part 1 shows what a home-made folder of runs keeps and
forgets, puts the runs on one shared axis in W&B (why only the run with a callback has curves, why
`wandb.config = {...}` leaves the config empty) and prepares everything a job needs. Part 2 builds the local
"cockpit" container that submits jobs but never trains, packs the trainer into a 4 KB tarball, submits a Vertex AI
custom job with one command that carries your W&B key, tells apart who submits and who runs, and ends with three
switches for one GPU and `MirroredStrategy` on two.

Watch it with both notebooks copied to your Colab, a clone of `model-training`, Docker Desktop running, a free W&B
account and a Google Cloud project with billing. **This lecture's Vertex AI jobs bill your project while they run**; a
GOLD tag marks each billing point (no amounts: check the pricing page), and the video ends with the teardown
checklist. The tracker top left shows the notebook or README step; pause at every `▶ your turn` to run the command; a
gray `extra` tag marks a check that isn't in the README, and a gray "Lecture 13 · slides …" tag top right points to the
lecture slides the scene stands on.

The terminal sessions were recorded on 2026-10-23 in a fresh Docker Engine 29.8.2 standing in for a laptop with
Docker Desktop. That machine had **no Google credentials, no W&B account, no GPU and no browser**. Everything local ran
live: the clone, the secrets folder, both build failures and both fixes, the cockpit's start, the tarball, the checks
inside the cockpit and `python cli.py`'s errors. Every step that needs Google, Vertex AI or W&B is shown up to its
honest, documented failure; the job's first minute (installing the tarball, the trainer's W&B login with three keys) is
replayed in a plain Python container tagged `extra · local stand-in`. The notebooks' results are their stored outputs
(`recorded`), the job's log lines come from `task.py`'s own prints, and the GCP console, W&B and Colab pages are
schematic drawings tagged `illustration`. The bucket and project on screen are the stand-ins `your-bucket-placeholder`
and `your-gcp-project`, and the W&B key is an obviously fake placeholder. Series format:
[`docs/AC215_SERIES.md`](../../docs/AC215_SERIES.md). Study guide with every command:
[MLOps_Learning · guides/L13-training-workflows.md](https://github.com/JunyiZhou-Conny/MLOps_Learning/blob/main/guides/L13-training-workflows.md).

English narration; Chinese and bilingual subtitles (中文字幕说明见 [`i18n/zh/README.md`](i18n/zh/README.md)).

| file | what it is |
| --- | --- |
| `output/ac215-l13-training-workflows.zh-en.mp4` | **the copy to watch**: 1080p60, English narration, bilingual subtitles (Chinese above, English below) burned in, 31:44 (1904.4 s). Published as a GitHub release asset: no MP4 is kept in Git ([`docs/PUBLISHING.md`](../../docs/PUBLISHING.md)) |
| `output/ac215-l13-training-workflows.mp4` | the same video without burned-in subtitles (1920×1080 at 60 fps, h264/AAC 48 kHz stereo, −16.1 LUFS integrated); load any `.srt` below in your player. Not in Git: rebuild it with `--no-render` (see Rebuild) |
| `output/ac215-l13-training-workflows_part1.mp4` | part 1, 13:52 (832.2 s): experiment tracking, a folder of runs, W&B, and the setup for serverless training (S01–S07). Not in Git: rebuilt with `--no-render` |
| `output/ac215-l13-training-workflows_part2.mp4` | part 2, 17:52 (1072.2 s): Vertex AI custom jobs: build, package, submit, identities, GPUs and `MirroredStrategy` (S08–S15). Not in Git: rebuilt with `--no-render` |
| `output/ac215-l13-training-workflows.srt` | English subtitles (each part has its own `.srt`, `.zh.srt`, `.zh-en.srt` / `.ass`) |
| `output/ac215-l13-training-workflows.zh.srt` | Chinese subtitles (on the English timing) |
| `output/ac215-l13-training-workflows.zh-en.srt` / `.zh-en.ass` | bilingual subtitles |
| `output/chapters.txt`, `chapters_part1.txt`, `chapters_part2.txt` | chapter timestamps |
| `output/transcript.md` | the full narration by chapter |
| `digest.md` | the tutorial digest: the repo, both notebooks, every step, a code tour with `path:line`, gotchas, errata |
| `SLIDES.md` | the lecture behind the tutorial: a digest of the slide deck in our own words, with slide numbers, and which section stands on which slides |
| `assets/terminal/` | the **real** terminal sessions every terminal panel prints from (2026-10-23, a fresh Docker Engine 29.8.2 standing in for the laptop with Docker Desktop, no Google credentials); provenance in [`ASSETS.md`](ASSETS.md) |
| `assets/source/` | the tutorial files the code panels quote, unchanged at the pinned commit, plus extracts of the two notebooks (names masked) |
| `BRIEF.md`, `script.md`, `scenes/` | the design, the narration (SAY) + visual plan (SHOW), and the Manim source |
| `i18n/zh/` | the Chinese subtitle text: glossary and sentence-aligned translation |
| `REVIEW.md` | the review record: content gates, QA findings and fixes, the final-cut checks |

Git keeps the subtitles, the chapter files and the transcript; the MP4s are release assets.

## Chapters

Paste-ready in `output/chapters.txt` (and `chapters_part1.txt`, `chapters_part2.txt` for the parts). Part 1 (13:52) is chapters 00:00–11:09 below; part 2 (17:52) restarts at 00:00 with "The cockpit that won't build: two one-line fixes", its chapters at 00:00, 02:24, 04:49, 07:13, 09:45, 11:49, 13:16, 15:51.

```
00:00 Two tables, two winners
01:24 Three levers and a missing row
02:40 A tracker made of folders
05:12 Runs on a shared axis
07:35 Three lines, and an assignment that goes nowhere
09:20 Rent the machine, not the server
11:09 A project, two keys and a bucket
13:52 The cockpit that won't build: two one-line fixes
16:17 What goes in the tarball
18:41 One command, and a key inside it
21:05 Who submits, who runs
23:37 What the job prints, what W&B can show
25:41 Three switches for one GPU
27:08 Two GPUs, one model
29:43 The missing model, teardown and recap
```

## What you'll learn

Eleven *pause and ponder* moments and one quick prediction ask you to predict before the video shows you: what the
split code actually did; what four of five W&B runs lack; what the run's config holds after `wandb.config = {...}`;
which machines will ever import TensorFlow; what `echo ${#WANDB_KEY}` prints in a new terminal; which Dockerfile line
picks your Debian; whether a typo fix needs a rebuild or a re-package; who can see your W&B key later; how the job reads
your private bucket without your key; which of the seven things a run record should hold this run keeps; why a job
with a T4 says `GPU Available: []`; and the steps per epoch on two GPUs. Five test-yourself questions close the video.

**Part 1 · Track it: a folder of runs, W&B, and the setup for serverless training**

1. **Two tables, two winners** — two copies of the same notebook, the same 1,156 photos and five models, and two
   different winners at 68.97 %; can you even tell what was different? What you need, and what bills.
2. **Three levers and a missing row** — more data, better models, faster hardware: today you rent hardware; the
   seven things a complete run should keep; W&B or MLflow; the map that stays all lecture.
3. **A tracker made of folders** — notebook A's `experiment_<ts>/` folder and its five files per model; the split
   that uses `test_percent` twice and has no seed; the winner that leads by two photos; uploading to your bucket.
4. **Runs on a shared axis** — notebook B: the `WandB` secret, five runs in one project on one epoch axis; only the
   run with a callback draws curves; two runs with one name, told apart by run ID.
5. **Three lines, and an assignment that goes nowhere** — `wandb.config = {...}` rebinds the name and the run's config
   stays `{}`; the fix `wandb.init(config=…)`; init, callback, finish; the repo trainer's own W&B lines.
6. **Rent the machine, not the server** — serverless training: a tarball to a bucket, Vertex AI starts a machine with
   Google's TensorFlow image, runs your trainer with flags, deletes the machine; the job can't see your laptop.
7. **A project, two keys and a bucket** — clone, the Vertex AI API, the GPU quota request, the `secrets/` folder, the
   `model-trainer` service account and its key, a bucket of your own, and the W&B key in a variable (and its length).

**Part 2 · Ship it: build, package, submit, identities, GPUs and MirroredStrategy**

8. **The cockpit that won't build: two one-line fixes** — edit `docker-shell.sh`; the build fails at step 2 (Debian
   11's security mirror) and then at line 37 (`google-cloud-sdk`); two one-line fixes; the cockpit starts without a key.
9. **What goes in the tarball** — inside the cockpit, `import tensorflow` fails: it submits, it never trains;
   `setup.py`, `find_packages()`, `task.py`'s flags and the `"16"` default; `sh package-trainer.sh` and the 4,016-byte
   tarball.
10. **One command, and a key inside it** — `cli.sh` line by line, CPU by default; `sh cli.sh` fails without an
    account here; `sh -x` shows the job spec, with your W&B key inside `--args`; an empty key and a name conflict.
11. **Who submits, who runs** — three badges: the key file submits, the Vertex AI service agent runs, the W&B key
    travels by hand; the job's first minute in a local stand-in: the tarball installs, no TensorFlow, three W&B logins.
12. **What the job prints, what W&B can show** — the job's log from `task.py`'s prints; what the run's W&B side holds
    and lacks; the seven-item run record, and the hook's verdict: these tables cannot crown a recipe.
13. **Three switches for one GPU** — accelerator, image and quota must agree; a CPU image with a T4 attached says
    `GPU Available: []` and still bills; uncomment the GPU block.
14. **Two GPUs, one model** — slide 27's ladder; `MirroredStrategy`: replicas, a global batch split in two, gradients
    averaged by all-reduce, variables created inside `strategy.scope()`; `cli-multi-gpu.sh` and `task_multi_gpu.py`.
15. **The missing model, teardown and recap** — `cli.py`, the Python SDK route; the trained model is never saved; the
    shutdown checklist; the whole lecture on one map; five questions; next, lectures 14 and 15.

## Rebuild

```bash
python -m explainer.build videos/ac215-l13-training-workflows -q l                          # fast draft
python -m explainer.build videos/ac215-l13-training-workflows --render-only --jobs 3        # 1080p60 scene renders
python -m explainer.build videos/ac215-l13-training-workflows --no-render --crf 27 --burn   # stitch: video, parts, subtitles, burned-in copy, chapters, transcript
python -m explainer.build videos/ac215-l13-training-workflows --subs-only                   # rewrite subtitles only
python -m explainer.i18n check videos/ac215-l13-training-workflows --lang zh                # Chinese text aligned with the English
```

No MP4 is in Git (the burned-in copy is a release asset): after a fresh clone, render the scenes once, then the
`--no-render` line rebuilds the clean video, the two part cuts and the burned-in copy from the scene renders.

Narration: Kokoro (`af_heart`, speed 0.9), generated locally.

*Course materials belong to the AC215 teaching staff (Harvard IACS); the model-training tutorial and the two Colab
notebooks are used for study with the instructor's permission and quoted at their pinned versions. The lecture's slides
are redrawn in our own pictures, never shown. The GCP console, W&B, Colab and Vertex AI pages are schematic drawings
(tagged `illustration`), not screenshots; the recording used no Google credentials, and the key and W&B key on screen
are obviously invalid stand-ins.*
