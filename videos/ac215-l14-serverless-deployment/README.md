# AC215 · Lecture 14 — Serverless deployment: a function, a service and a job on Cloud Run

A follow-along walkthrough of the Lecture 14 tutorial of Harvard's **AC215 (MLOps & LLMOps, Fall
2026)**, *Serverless Deployment: Cloud Functions, Cloud Run*:
[dlops-io/serverless-deployment](https://github.com/dlops-io/serverless-deployment), branch `main` @
[`46cc62f`](https://github.com/dlops-io/serverless-deployment/tree/46cc62fd8b1ac94ce733571a834b46002d8dd8c4)
(2026-10-22, "Point student setup instructions to the main repository"), its `README.md` top to
bottom: *Before you begin* (with the Terminal setup), *Part 1: Deploy a translation function*,
*Part 2: Deploy a translation web app*, *Part 3: Give the web app access to Agent Platform*,
*Part 4: Generate and save a translated audio edition* and *Clean up after the tutorial*.

**Which commit.** The course map still pins `4eaf343` (2025), whose ~150-line README had the sections
*Running App as Cloud Function* and *Running App in Cloud Run*. The course page links the repository's
default branch, and on 2026-11-04 that was `46cc62f`, a rewritten four-part tutorial: this is the
README a student opens today, so the video follows it (the course page's two section links now land
at the top of the README; the video says so kindly). Details in [`ASSETS.md`](ASSETS.md), "Which
commit". The concept-first exam edition of this lecture is [`../ac215-l14-exam/`](../ac215-l14-exam/).

A translation page works on `localhost:8086`, but a classmate's `localhost` is their own machine.
Can the page have a public URL and cost nothing while nobody uses it? Part 1 hands Cloud Run a
six-line handler and lets Cloud Build make the image; Part 2 deploys a prebuilt image as a service
that scales to zero; Part 3 gives it an identity (no key file) so it can speak through Gemini; Part 4
runs the same image as a job that reads a passage from a private bucket, saves its text, audio and a
completion manifest, and exits.

Watch it with the README open, your own clone, Docker running, gcloud installed and your own Google
Cloud project with billing. **This lecture creates billable resources and calls a paid model**: a
Cloud Run function (with its build and stored image), a service, a job, two buckets, and a Gemini
speech call per Play audio; a GOLD tag marks each place, and the video ends with the clean-up
checklist. The tracker top left shows the README step; pause at every `▶ your turn` to run the command;
a gray `extra` tag marks a check that isn't in the README, and a gray "Lecture 14 · slides …" tag top
right points to the lecture slides the scene stands on. Follow the console steps; the README's gcloud
boxes are alternatives, shown after each one.

The terminal sessions were recorded on 2026-11-04 in fresh containers: a Docker 29.8.2 engine standing
in for your laptop, a Debian 12 shell (Python 3.12.15, uv 0.13.7) for section 3.3 and the function's
local stand-in, and Google Cloud SDK 592.0.0. That machine had **no Google account, no project and no
credentials**. Everything that runs on your own machine ran live: the clone, the README's `docker run`
of the public image (its digest matches the README's), the web app's page and JSON routes,
`uv sync --frozen` and `uv run … serve`, the image's `batch` command, the helper's dry run, and Part
1's handler under the same Functions Framework the cloud build installs (tagged `local stand-in`).
Every gcloud box runs to its first honest error; console steps are schematic drawings tagged
`illustration`; what only the cloud shows (the function's answers, the deployed service, speech, the
job's files) is quoted from the README's own recording and tagged `recorded`. Project IDs and buckets
on screen are the README's placeholders. Series format:
[`docs/AC215_SERIES.md`](../../docs/AC215_SERIES.md). Study guide with every command:
[MLOps_Learning · guides/L14-serverless-deployment.md](https://github.com/JunyiZhou-Conny/MLOps_Learning/blob/main/guides/L14-serverless-deployment.md).

English narration; Chinese and bilingual subtitles (中文字幕说明见 [`i18n/zh/README.md`](i18n/zh/README.md)).

| file | what it is |
| --- | --- |
| `output/ac215-l14-serverless-deployment.zh-en.mp4` | **the copy to watch**: 1080p60, English narration, bilingual subtitles (Chinese above, English below) burned in, DURATION_FULL. Published as a GitHub release asset: no MP4 is kept in Git ([`docs/PUBLISHING.md`](../../docs/PUBLISHING.md)) |
| `output/ac215-l14-serverless-deployment.mp4` | the same video without burned-in subtitles; load any `.srt` below in your player. Release asset, not in Git: rebuild it with `--no-render` (see Rebuild) |
| `output/ac215-l14-serverless-deployment_part1.mp4` | part 1, DURATION_P1: hand over code, hand over an image — a Cloud Run function and a service (S01–S08). Release asset, not in Git |
| `output/ac215-l14-serverless-deployment_part2.mp4` | part 2, DURATION_P2: identity and finite work — a runtime service account, speech and a Cloud Run job (S09–S16). Release asset, not in Git |
| `output/ac215-l14-serverless-deployment.srt` | English subtitles (each part has its own `.srt`, `.zh.srt`, `.zh-en.srt` / `.ass`) |
| `output/ac215-l14-serverless-deployment.zh.srt` | Chinese subtitles (on the English timing) |
| `output/ac215-l14-serverless-deployment.zh-en.srt` / `.zh-en.ass` | bilingual subtitles |
| `output/chapters.txt`, `chapters_part1.txt`, `chapters_part2.txt` | chapter timestamps |
| `output/transcript.md` | the full narration by chapter |
| `exercises.md` | do these after watching: the five test-yourself questions, hands-on predict-then-run tasks, debugging and think questions, with answers; what was re-run to check them is in [`assets/exercise-checks/`](assets/exercise-checks/README.md) |
| `digest.md` | the tutorial digest: every step, a code tour with `path:line`, gotchas, errata |
| `SLIDES.md` | the lecture behind the tutorial: a digest of the slide deck in our own words, with slide numbers, and which scene stands on which slides |
| `assets/terminal/` | the **real** terminal sessions every terminal panel prints from (2026-11-04, fresh containers, no Google account); provenance in [`ASSETS.md`](ASSETS.md) |
| `assets/source/` | the tutorial files the code panels quote, unchanged at `46cc62f` (and the old README at `4eaf343`, for comparison) |
| `BRIEF.md`, `script.md`, `scenes/` | the design, the narration (SAY) + visual plan (SHOW), and the Manim source |
| `i18n/zh/` | the Chinese subtitle text: glossary and sentence-aligned translation |

Git keeps the subtitles, the chapter files and the transcript; the MP4s (the burned-in copy, the clean
video and the two part cuts) are release assets.

## Chapters

CHAPTERS

## What you'll learn

Five *pause and ponder* moments ask you to predict before the video shows you: whether a wrong entry
point fails the build; how many instances ten simultaneous users start with concurrency 4 and a
maximum of 2, and what happens to the last two; whether public access lets the service call Agent
Platform; what a job runs with eleven arguments and no command; and whether executing the same job
again overwrites the first result. Five test-yourself questions close the video (answers in
`exercises.md`).

**Part 1 · hand over code, hand over an image: a Cloud Run function and a service**

1. **It works on localhost** — a translation page answering *Bonjour à tous* on your laptop, and why
   `localhost:8086` finds nothing on a classmate's; a Lecture 1 VM bills all night; serverless's
   promise; the job you will build by the end; how the tracker, `▶ your turn` and the gcloud
   alternatives work.
2. **One app, four ways to deploy it** — the lecture's map: a code file or a container, on a rented
   machine or serverless; the README's four parts in the serverless row; we deploy the application code
   around the model, not the model; the course page's old section links, and the commit we follow.
3. **Before you begin: project, region, clone** — project ID vs display name, billing and permissions;
   Toronto for the services, `us-central1` for the speech model; the worksheet's names; the clone and
   the 2025 files at the root not to build; `gcloud auth login` (gcloud's login, not the app's) and the
   seven exports; what this recording machine can and cannot show.
4. **Part 1: write a function** — Cloud Functions are now Cloud Run functions; **Write a function**:
   name, region, Python 3.12 (the older README said 3.10), **Allow public access**; the handler
   `hello_http` with three defaults; the lecture's positional sketch would swap source and destination;
   two exact pins; the **Function entry point**.
5. **What runs your function?** — Cloud Build turns three inputs into an image in Artifact Registry,
   and Cloud Run starts a revision; the Functions Framework runs Flask under gunicorn on `$PORT`; the
   same two pins on your laptop as a local stand-in; a wrong entry point's `MissingTargetException`,
   found in the logs.
6. **Call it with a query string** — the service URL, the default *Bienvenido a AC215*, `?`, `&` and
   `%20`; Greek, Hindi and `zh-cn`; the logs; a provider timeout during the recording (a 500 from
   line 12); the gcloud box's placeholder and sign-in errors; what a cold start is.
7. **Part 2: the prebuilt app on your laptop** — `docker run --rm -p 8086:8080`; the digest equals the
   README's; gunicorn on `0.0.0.0:8080`; an empty entrypoint and the command `translation_demo serve`,
   which replaces itself with gunicorn (1 worker, 4 threads); JSON posts, 405 for a query string, 400
   for a made-up language, 503 for speech; `PORT=9090` and the pipe that must follow it.
8. **Deploy the same image** — **Deploy container**: public, request-based, min 0 / max 2, port 8080,
   512 MiB, 1 CPU, timeout 120, concurrency 4 (= gunicorn's threads); when "pay only when your code
   runs" holds; ten users at once; revisions; nothing built; tag vs digest; the parked question: who is
   the app when it calls an API?

**Part 2 · identity and finite work: a runtime service account, speech and a Cloud Run job**

9. **Who may call it, and who it runs as** — two doors: **Allow public access**
   (`--no-invoker-iam-check`, 403 under an organization policy) and the runtime identity (the default
   compute account until you attach one); enable the Agent Platform API; create
   `translation-demo-runtime` with Agent Platform User and Service Usage Consumer; no key to download.
10. **Attach the identity, turn on speech** — your own Service Account User; the **Security** tab;
    three environment variables (service in Toronto, model in `us-central1`); a new revision; the speech
    path: checks, an ADC token from the attached account, Gemini TTS, audio straight back; reload,
    Play audio, and the messages to read when it fails.
11. **Develop locally with ADC** (optional section 3.3) — impersonation with Token Creator, no private
    key; `gcloud auth application-default login` and its quota project, separate from
    `gcloud auth login`; `uv sync --frozen` (41 packages); `uv run … serve` on port 8086; the 503 you get
    without the sign-in.
12. **Finite work: a job and two buckets** — a job reads, translates, speaks, saves and exits; one
    image, two programs (`serve` and `batch`); last week's training job had the same shape; no URL and no
    lasting disk, so input and output live in two private buckets; `run-001` is a prefix, not a folder.
13. **Command, arguments and the job's badge** — `translation-audio-job` with Object Viewer on the input
    and Object Creator on the output; Container command `python` fills the empty entrypoint, eleven
    argument chips replace the command; timeout 5 minutes, retries 0; the one-chip mistake; arguments
    without a command; a job that starts the web server instead.
14. **Execute it and collect the files** — Execute and History; an honest exit 1; the task log's JSON
    summary; a random attempt folder with `translated.txt`, `speech.wav` and `manifest.json`, written
    create-only with the manifest last: the receipt; a second execution lands beside the first; the
    download; `--wait`.
15. **From the terminal, then the helper** — your own run-with-overrides permission; upload a new
    passage under `run-002`; overrides replace the whole argument list (a flag you leave out is not
    taken from the saved job); the helper's dry run, its fresh run folders, and "Downloaded results"
    only after a complete manifest.
16. **Clean up, and what serverless costs** — the README's four clean-up steps plus what they leave out;
    the troubleshooting table; the whole map; the lecture's three downsides (cold starts, limited
    control and debugging, vendor lock-in) and what the tutorial gives you for each; next, Lecture 15.

The README's and the slides' small slips are pointed out kindly, with the fix: the course page links
to sections the rewritten README no longer has (start at the top; Part 1 is the function, Parts 2–4
are Cloud Run), and the course map pins an older commit; the 2025 files at the repository root are
never used (don't build that `Dockerfile`; the image comes from `tutorial/app/`); Cloud Functions are
now *Cloud Run functions*, the runtime is Python 3.12 (not 3.10), and the slide's "create a Python
file" really means the file, its requirements and the entry point; the slide's positional
`translate(text, src, dest)` would swap source and destination (pass them by name); a function has no
container *to manage*, but Google builds one, which is why there is an image to delete; "pay only when
your code runs" holds with request-based billing and minimum 0; the console pastes a movable tag
(deploy by digest to reproduce); the README promises your developer access in section 3.3, which
grants Token Creator, not the Service Account User needed to attach the account (owners have it; in a
restricted project, ask course staff); and the clean-up list leaves out soft-deleted files and the
build's source archives and logs.

## Rebuild

```bash
python -m explainer.build videos/ac215-l14-serverless-deployment -q l                          # fast draft
python -m explainer.build videos/ac215-l14-serverless-deployment --render-only --jobs 3        # 1080p60 scene renders
python -m explainer.build videos/ac215-l14-serverless-deployment --no-render --crf 27 --burn   # stitch: video, parts, subtitles, burned-in copy, chapters, transcript
python -m explainer.build videos/ac215-l14-serverless-deployment --subs-only                   # rewrite subtitles only
python -m explainer.i18n check videos/ac215-l14-serverless-deployment --lang zh                # Chinese text aligned with the English
```

No MP4 is in Git (the burned-in copy is a release asset): after a fresh clone, render the scenes
once, then the `--no-render` line rebuilds the clean video, the two part cuts and the burned-in copy
from the scene renders. The captures can be re-run with `assets/terminal/capture.sh` (see
[`ASSETS.md`](ASSETS.md), "Re-running the captures").

Narration: Kokoro (`af_heart`, speed 0.9), generated locally.

*Course materials belong to the AC215 teaching staff (Harvard IACS); the serverless-deployment
tutorial is used for study with the instructor's permission and quoted at its pinned commit. The
lecture's slides are redrawn in our own pictures, never shown. The Google Cloud console is a schematic
drawing (tagged `illustration`), never a screenshot, and the README's console GIFs are not shown; the
recording used no Google account or credentials, and every project ID and bucket on screen is a
placeholder.*
