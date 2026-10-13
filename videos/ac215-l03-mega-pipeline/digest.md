# L03 · Containers II — Mega Pipeline App — tutorial digest

- **Ed lesson:** https://edstem.org/us/courses/97373/lessons/166033/ (course-site map: `src/2026-AC215/tutorials_demo.md:46-52`; lecture date Sep 10 per `_modules/week-02.md:9-11`). I could not open Ed itself, so this digest is built from the repo.
- **Repo used:** `dlops-io/mega-pipeline`, branch **`main`**, commit `c6bbc9ba88984e1234b68ccf5cdf7c00f7e9accc`, committed 2026-09-27 06:42:25 -0400 ("fix for Google Speech-to-Text automatically breaks longer audio files into chunks separated by natural pauses."). On lecture day (Sep 10) `main` moved from `86c6fb8` ("before lecture", 01:25, component-README tweaks) to `07e14b9` ("Update README.md", 14:28, which only changed the Canvas key link at `README.md:99`). The only later change is `c6bbc9b`, which touches only `transcribe_audio/cli.py` (see §5).
- **Other branches, read for comparison only (the lecture uses `main`):**
  - `simple` @ `7805aee4ec52f337c0160cd6f449fd7b0b85d9f5` (2025-09-23): last year's student version. Only `transcribe_audio/` ships a `Dockerfile`, `pyproject.toml`, `uv.lock` and a 23-line build-and-run `docker-shell.sh`.
  - `solution` @ `8083187ec0e022ba34440892689145ff703a34e0` (2025-09-22): last year's full solution. It has a `Dockerfile`, a 4-mode `docker-shell.sh`, `pyproject.toml` and `uv.lock` for all five components, plus a Pipenv `test-cloud-run/` folder. Secrets live outside the repo and are mounted at `/secrets`.
  - `pipenv` @ `84b2d64fcdf2af16c50e3257eac8ae3e02e24501` (2025-02-06): the older Pipenv-era README. Its sample Dockerfile uses `pipenv sync` / `pipenv shell`.
  - `flexible-workflow` @ `cc67f3b8fc471f4fe1afe73d03e89466bae7d485` (2026-09-18): **the L04 tutorial** (`tutorials_demo.md:56-63`). Cited in §7 only.
  - Not examined beyond `git ls-tree`: `flexible-workflow-javier`, `pipenv-flexible-workflow`, `validation/mega-pipeline-javier` (staff work branches).
- **Instructor's removed "codecast" script, read from history as context:** `git show 843d8dd:codecast-mega-pipeline.md`. It was added in `bfdda58` (2026-06-24) and removed in `0a4c1eb` (2026-06-25, "Remove codecast script from public repo"). It is the instructor's run-sheet for this exact tutorial on `main` (295 lines at `843d8dd`). It is the only place that spells out `docker build -t transcribe_audio .` and the one-line `uv add` commands. I cite it as `codecast:NN`. It is a removed, unpublished file: use it for context, never quote it on screen as if it were the README.
- **README sections this lecture covers** (`README.md` on `main`; GitHub anchors):
  - Overview `README.md:1-18`; [`#prerequisites`](https://github.com/dlops-io/mega-pipeline#prerequisites) `:22-26`; [`#clone-this-repository`](https://github.com/dlops-io/mega-pipeline#clone-this-repository) `:30-37`; [`#what-youll-learn`](https://github.com/dlops-io/mega-pipeline#what-youll-learn) `:41-46`
  - [`#-youll-work-in-teams--and-theres-a-leaderboard-`](https://github.com/dlops-io/mega-pipeline#-youll-work-in-teams--and-theres-a-leaderboard-) `:50-56`
  - [`#connecting-the-pipeline-components`](https://github.com/dlops-io/mega-pipeline#connecting-the-pipeline-components) `:60-67`, [`#gcs-bucket-details`](https://github.com/dlops-io/mega-pipeline#gcs-bucket-details) `:71-86`
  - [`#gcp-credentials-file`](https://github.com/dlops-io/mega-pipeline#gcp-credentials-file) `:90-101`, [`#-important-note-on-secrets`](https://github.com/dlops-io/mega-pipeline#-important-note-on-secrets) `:103-106`
  - [`#-time-to-build--the-five-components`](https://github.com/dlops-io/mega-pipeline#-time-to-build--the-five-components) `:110-124` → the five component READMEs (`transcribe_audio/README.md`, `generate_text/README.md`, `synthesis_audio_en/README.md`, `translate_text/README.md`, `synthesis_audio/README.md`). Each has the sections `#project-setup`, `#gcp-credentials-file`, `#create-pyprojecttoml`, `#create-dockerfile`, `#docker-build--run`, `#python-packages-required`, `#cli-to-interact-with-your-code`, `#testing-your-code-locally` and `#optional-push-container-to-docker-hub`.
  - [`#quick-reference--running-each-component`](https://github.com/dlops-io/mega-pipeline#quick-reference--running-each-component) `:128-165`; `## Appendix` `:169` with [`#sample-dockerfile`](https://github.com/dlops-io/mega-pipeline#sample-dockerfile) `:171-225` and [`#notes-for-running-on-windows`](https://github.com/dlops-io/mega-pipeline#notes-for-running-on-windows) `:227-236`; [`#solutions`](https://github.com/dlops-io/mega-pipeline#solutions) `:238-239` ("Solutions to this tutorial will be posted here after the assignment deadline.")
  - Component README extras: `synthesis_audio_en/README.md:132-135` has a `### OPTIONAL: You can use the cli_11.py script…` note (wrong folder, §10 E4) and its push section is a `###` heading (`:138`); `synthesis_audio/README.md:132-156` adds `## OPTIONAL: Synthesize with ElevenLabs (Pavlos' voice)` before the push section. The C and E "Testing your code locally" sections have no `-u` line.
- **Colab notebooks used:** none (the `colab/` folder has nothing for L03).
- **Not examined:** the AWS variant `dlops-io/mega-pipeline-aws` (not cloned), Tutorial 0 `dlops-io/ac215-setup` (a clone exists, but this digest relies only on `README.md:24` for what it covers), and the leaderboard app at `http://ac215-mega-pipeline.dlops.io/` (its code is not in the repo).
- **Method note:** there was no access to the course bucket or the Canvas key, so no `--download`/`--transcribe`/… step that talks to Google was run. I checked uv's behaviour with uv 0.11.32 on *copies* of `pyproject.toml` in a sandbox (§6, §10). I extracted (but did not execute) the public wheels `google-cloud-translate 3.28.0`, `google-genai 2.29.0`, `google-cloud-texttospeech 2.38.0`, `google-cloud-speech 2.41.0`, `google-auth 2.61.0` and `ffmpeg-python 0.2.0` and read their source to confirm when credentials are loaded and what the API enums mean.
- **Verification note (fact-check, 2026-10-13, linux/amd64, Docker 29.8.2):** on a `git archive` copy of `c6bbc9b` I ran `uv init --bare` on the host (uv 0.11.32, host default Python 3.13) and built the README's component Dockerfile (`transcribe_audio/README.md:41-90`, assembled as in §4 step 4) in disposable containers, with a capture-only prelude that only adds the sandbox's proxy CA and https apt sources. `pip install uv` inside the image fetched **uv 0.13.0**. Inside the containers I ran `uv add`, `python cli.py --help`, the `ENTRYPOINT` misuse of G16 and the secret check of G1, all without any Google credentials. Lines marked *verified* below come from those runs; the remaining "you should see" lines (anything after `--download`) are still inferred from the code.

---

## 1. What you build

You build an "AI podcast factory" out of **five small, separate Docker containers**, one per folder: `transcribe_audio`, `generate_text`, `synthesis_audio_en`, `translate_text` and `synthesis_audio`. Each one is a given 120-154-line `cli.py` (154, 143, 120, 125 and 120 lines) that does up to three things:
1. **pull** its inputs from a class-wide Google Cloud Storage bucket, `gs://mega-pipeline-bucket`;
2. **call one managed Google AI API**: Speech-to-Text, Gemini on Vertex AI, Text-to-Speech or Cloud Translation;
3. **push** its outputs back to the bucket under a different "folder" (prefix), scoped by your team's `group_name` (the two Google TTS stages skip this step: the TTS service writes into the bucket itself).

The containers never talk to each other. The **bucket is the hand-off**: stage A writes `text_prompts/<group>/`, stage B reads it, and so on (`README.md:60-67`).

Unlike L02, **no Dockerfile is provided**. You write one per folder, line by line, from the component README (`README.md:114`, `transcribe_audio/README.md:36-90`). You scaffold an empty `pyproject.toml` with `uv init --bare`, build the image, and run it with your folder **bind-mounted** at `/app`. Inside the container you `uv add` the packages that `cli.py` imports, then rebuild to bake them in.

Authentication uses one shared service-account JSON key from Canvas. It sits in each component's `secrets/` folder, and the Google libraries find it through `GOOGLE_APPLICATION_CREDENTIALS`. Every API call and every byte stored is billed to the course's GCP project, not to yours: the bucket belongs to it, Gemini and TTS name `ac215-project` explicitly (`generate_text/cli.py:23-25`, `synthesis_audio_en/cli.py:77`), and Speech-to-Text and Translation calls are attributed to the project the shared key belongs to (presumably the same one; `transcribe_audio/cli.py` defines `gcp_project` but never uses it). Progress shows up on a class leaderboard. There are no ports, no web servers, no Docker networks and no Compose here.

```
 YOUR LAPTOP  (Docker Desktop; Apple Silicon builds linux/arm64 images, Intel/most PCs build linux/amd64)
 +--------------------------------------------------------------------------------------------------+
 |  ~/AC215/mega-pipeline/   (git clone, branch main)                                               |
 |   transcribe_audio/  generate_text/  synthesis_audio_en/  translate_text/  synthesis_audio/       |
 |     cli.py (given)   Dockerfile (YOU write)   pyproject.toml + uv.lock (uv init / uv add)        |
 |     secrets/mega-pipeline.json  (from Canvas, git-ignored)                                       |
 |                                                                                                  |
 |   $ docker build -t transcribe_audio .          $ docker run --rm -ti -v "$(pwd):/app" transcribe_audio
 |                                                                                                  |
 |   +---------------- one container per component, started by hand, one at a time --------------+ |
 |   |  user "app" (uid 1000)        WORKDIR /app  <==== bind mount of THIS component folder (rw)  | |
 |   |  /home/app/.venv   <- built by `uv sync` at image build time, lives OUTSIDE the mount       | |
 |   |  ENV GOOGLE_APPLICATION_CREDENTIALS=secrets/mega-pipeline.json   (relative to cwd /app)    | |
 |   |  app@<id>:/app$ python cli.py --download | --transcribe | --upload    (venv on, no prefix) | |
 |   +--------------------------------------------------------------------------------------------+ |
 |   no -p ports, no docker network, no compose                                                     |
 +--------------------------------------------------------------------------------------------------+
            |  HTTPS via google-cloud-* client libraries
            |  (google.auth reads the JSON key -> OAuth2 access token -> Authorization header)
            v
 GOOGLE CLOUD  project "ac215-project"  (course-owned; hard-coded as gcp_project in every cli.py)
 +--------------------------------------------------------------------------------------------------+
 |  Cloud Storage bucket  gs://mega-pipeline-bucket   (us-central1, Standard, not public)           |
 |   input_audios/input-*.mp3                   shared by everyone (no group folder)                |
 |   text_prompts/<group>/input-*.txt           A uploads    -> B downloads                         |
 |   text_paragraphs/<group>/input-*.txt        B uploads    -> C and D download                    |
 |   text_audios/<group>/input-*.mp3            written by the TTS *service* for C                  |
 |   text_translated/<group>/input-*.txt        D uploads    -> E (and bonus) download              |
 |   output_audios/<group>/input-*.mp3          written by the TTS *service* for E                  |
 |   output_audios_pp/<group>/input-*.mp3       bonus: cli_11.py uploads (ElevenLabs voice)         |
 |                                                                                                  |
 |  Speech-to-Text v1 (A)   Vertex AI Gemini, us-central1 (B)   Cloud Translation v2 (D)            |
 |  Text-to-Speech Long Audio, parent projects/ac215-project/locations/us-central1 (C, E)           |
 +--------------------------------------------------------------------------------------------------+
            ^ reads the bucket (inferred; app not in repo)          api.elevenlabs.io (bonus only)
   Leaderboard  http://ac215-mega-pipeline.dlops.io/
```

The data-flow DAG (each arrow is "upload by one container, download by the next"):

```
 input_audios/ --A transcribe--> text_prompts/<g>/ --B generate--> text_paragraphs/<g>/ --+--C synth EN--> text_audios/<g>/
   (Speech-to-Text)                 (Gemini)                                            |    (TTS writes to GCS itself)
                                                                                        +--D translate--> text_translated/<g>/ --E synth FR--> output_audios/<g>/
                                                                                             (Translate v2)        |               (TTS writes to GCS itself)
                                                                                                                   +--bonus cli_11.py--> output_audios_pp/<g>/
```

C and D both depend only on B, so they can run in either order or at the same time. E needs D.

---

## 2. Prerequisites and costs

**Accounts and local installs** (`README.md:22-26`):
- Everything from Tutorial 0 (`dlops-io/ac215-setup`): a GCP account and project, VS Code, Git, **Docker Desktop** and **uv**. In this lecture, though, all API traffic goes to the course project, not yours.
- uv on the **host** is required, because `uv init --bare` runs on the host (`transcribe_audio/README.md:19-34`), and without a `pyproject.toml` the image's `RUN uv sync` fails (verified: ``error: No `pyproject.toml` found in current directory or any parent directory``). The README gives installers (`:26-34`): `curl -LsSf https://astral.sh/uv/install.sh | sh` (macOS/Linux), `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"` (Windows PowerShell), or `pip install uv`, then "restart your terminal".
- **Canvas access** (HarvardKey) to download `mega-pipeline.json` (`README.md:97-99`).
- Windows: run Docker from **Git BASH**, quote `"$(pwd)"`, and prefix `winpty` if you get "the input device is not a TTY" (`README.md:227-236`).
- Optional: a **Docker Hub** account and access token, if you want to push (`transcribe_audio/README.md:136-140`). An **ElevenLabs** account and API key for the bonus (`synthesis_audio/README.md:132-156`).

**Secrets: exactly where the code looks.**

| What | Where you put it on the host | How the code finds it | Cited |
|---|---|---|---|
| GCP service-account key | `<component>/secrets/mega-pipeline.json`, a copy **in each of the 5 folders** | Dockerfile `ENV GOOGLE_APPLICATION_CREDENTIALS=secrets/mega-pipeline.json`, a **relative** path resolved against the process's cwd (`/app`). `google.auth.default()` reads it. | `README.md:97`, `README.md:195`, `transcribe_audio/README.md:16,55` |
| ElevenLabs key (bonus) | `synthesis_audio/secrets/11lab_api_key.txt` containing `XI_API_KEY=your_api_key_here` | `cli_11.py` opens `'secrets/11lab_api_key.txt'` **at import time** and copies it into `os.environ['XI_API_KEY']` | `synthesis_audio/README.md:139-142`, `synthesis_audio/cli_11.py:30-39` |
| Team name (not secret, but critical) | edit `group_name = "pavlos"` in every `cli.py` | becomes the `<group>` path segment in every bucket object name | `transcribe_audio/cli.py:21`, `generate_text/cli.py:19`, `synthesis_audio_en/cli.py:18`, `translate_text/cli.py:18`, `synthesis_audio/cli.py:18`, `synthesis_audio/cli_11.py:19` |

Git protection: the root `.gitignore:4` has `secrets/`, and each component `.gitignore` has `/secrets` (e.g. `transcribe_audio/.gitignore:3`). **There is no `.dockerignore` anywhere on `main`**, so `COPY --chown=app:app . ./` copies `secrets/` into the image (see §6 G1).

**Hard-coded cloud identifiers** (same in every `cli.py`): `gcp_project = "ac215-project"`, `bucket_name = "mega-pipeline-bucket"` (e.g. `transcribe_audio/cli.py:17-18`). Gemini's model comes from the env var **`GEMINI_MODEL`**, default `"gemini-2.5-flash-lite"` (`generate_text/cli.py:73`). Nothing else is read from the environment except `GOOGLE_APPLICATION_CREDENTIALS` (library-side) and, in the bonus, `XI_API_KEY`.

**GCP APIs.** These must be enabled in the project that owns the key. On `main` that is the course's `ac215-project`, so the staff have already done it and you enable nothing: Cloud Storage, Speech-to-Text, Vertex AI, Cloud Translation, Text-to-Speech. You will enable these yourself next lecture. `flexible-workflow:README.md:187-198` lists them with `gcloud services enable storage.googleapis.com aiplatform.googleapis.com speech.googleapis.com texttospeech.googleapis.com translate.googleapis.com`.

**Billable resources and shutdown:**
- **GCP: nothing is billed to you on `main`.** Speech-to-Text, Gemini tokens, Translation characters, TTS characters and GCS storage/egress all bill to `ac215-project`, whose key you are borrowing. There is nothing to shut down: you create no VM, bucket or service account. Two caveats:
  - Do not leak the key (§6 G1).
  - Outputs you upload stay in the shared bucket under your group prefix. Everyone writes every prefix with the same key and the code has no guard, so nothing technical stops you from overwriting another team's objects (a wrong `group_name` does exactly that, G2). What else the course key may do is unknown (§10 Q4).
- **ElevenLabs (bonus):** usage counts against your own ElevenLabs quota/plan.
- **Docker Hub (optional):** free public repos. A pushed image is public by default (see G1).
- **Local disk:** five images, each `python:3.12-slim-bookworm` plus `build-essential` plus Google client libraries. Measured on linux/amd64 before any Python package was baked in: about **0.7 GB** for a `build-essential`-only image and about **1.5 GB** for `transcribe_audio` with `ffmpeg` (that build also carried the extra CPython of G3). Budget several GB for all five. Clean up afterwards with:
  ```bash
  docker image rm transcribe_audio generate_text synthesis_audio_en translate_text synthesis_audio
  docker builder prune
  ```
  (these are standard Docker commands, not from the README). Containers need no cleanup because every run uses `--rm`.

---

## 3. Concepts this tutorial teaches

> ★ = most deserving of an **animated** (3Blue1Brown-style) explanation.

### 3.1 ★ A pipeline of independent stages joined by shared storage ("the bucket is the message bus")
- **Explanation.** Each stage is a separate program in a separate container with one job. It doesn't know who produced its input or who will consume its output. All it knows is a **naming contract**: "I read `text_paragraphs/<group>/input-*.txt` and I write `text_translated/<group>/input-*.txt`" (`translate_text/cli.py:37,81-85`). Because the contract is "files in a bucket" rather than "function calls", you can swap, rerun or scale a stage without touching the others. The README frames this as a stand-in for the API-based microservices that come later (`README.md:60-67`).
- **Mental model.** A relay race where runners never meet. Each runner drops the baton in a numbered locker (a prefix), and the next runner opens that locker whenever they arrive. The pipeline's "wiring" is just the table of prefixes in §1.
- **Analogy.** A restaurant kitchen's pass: the grill cook puts the plate on the pass, and the expediter picks it up. Neither waits on the other's phone call.
- **Misconception.** "The containers form a pipeline, so starting one triggers the next." Nothing triggers anything. You (a human) run each container and each verb (`--download`, `--transcribe`, `--upload`) by hand. Orchestration (one command for the whole pipeline) is the Milestone 2 requirement (`milestone2.md:44-48`) and arrives with later tooling.
- **Animation idea.** Lay out the five containers as boxes along the top and the bucket as a long shelf of labelled drawers along the bottom. A glowing token (the halloumi recording) leaves `input_audios/`, rises into box A, and comes out transformed into a text page that drops into `text_prompts/g/`. Box B lifts it, and it morphs into a longer page. Then it **splits in two**: one copy flows to C and morphs into a sound wave, the other flows to D, turns French and then becomes a sound wave in E. Fade in the DAG edges last.

### 3.2 Namespacing a shared bucket: prefixes, `group_name`, "folders that aren't folders"
- **Explanation.** GCS is a flat key→bytes store. `text_prompts/group-07/input-1.txt` is one object name. The "folders" in the console are just a view of the `/`-separated prefixes. Each `cli.py` builds names as `os.path.join(<prefix>, group_name, filename)` (e.g. `transcribe_audio/cli.py:112`) and lists with a prefix (`transcribe_audio/cli.py:39`) or a glob (`generate_text/cli.py:42`). `group_name` is the only thing that keeps the teams from overwriting each other in one bucket.
- **Mental model.** One giant shared hard drive where everyone agreed to save inside a folder named after their team.
- **Analogy.** Shared office mailboxes: one cabinet, one slot per team label.
- **Misconception.** "If I forget `group_name`, I'll get an error." On `main` the default is `"pavlos"` and there is no guard (`transcribe_audio/cli.py:21`), so your `--upload` silently writes into (and overwrites) the instructor's namespace. Last year's `solution` branch had `assert group_name!="", "Update group name"`, and `flexible-workflow` brings an assert back (`flexible-workflow:README.md:134`).

### 3.3 ★ A Dockerfile, line by line, and image layers
- **Explanation.** Each instruction produces either a filesystem layer (`RUN`, `COPY`, and `WORKDIR` when it has to create the directory) or metadata (`ENV`, `ARG`, `USER`, `ENTRYPOINT`, `CMD`). The component Dockerfile is built from these pieces (`transcribe_audio/README.md:41-90`):
  1. `FROM python:3.12-slim-bookworm`: a Debian 12 base with CPython 3.12 already installed in `/usr/local` (3.12.15 at the time of checking).
  2. `ARG DEBIAN_PACKAGES="build-essential ffmpeg"`: the OS packages, as a build-time variable (`docker build --build-arg DEBIAN_PACKAGES=…` could override it). `ffmpeg` is needed only by the transcribe stage.
  3. Six `ENV`s:
     - `DEBIAN_FRONTEND=noninteractive`: apt never prompts.
     - `LANG=C.UTF-8`: a UTF-8 locale.
     - `PYTHONUNBUFFERED=1`: prints appear immediately.
     - `UV_LINK_MODE=copy`: uv copies package files from its cache into the venv instead of hard-linking them. Hard links only fail (uv then warns and falls back to copying) when the cache and the venv sit on different filesystems, for example with a BuildKit cache mount or a mounted cache volume. In this Dockerfile both live under `/home/app` on the same filesystem, so the line is a harmless convention: verified, a `uv sync --reinstall` with the variable unset hard-linked 26 packages with no warning. (codecast:110 explains it as "different layers — different filesystems"; that is not what happens here.)
     - `UV_PROJECT_ENVIRONMENT=/home/app/.venv`: put the venv **outside** `/app` (see 3.4).
     - `GOOGLE_APPLICATION_CREDENTIALS=secrets/mega-pipeline.json`.
  4. One big `RUN ... && ...` that updates apt, installs the packages, cleans the apt cache, installs uv with pip, creates user `app` (uid 1000, home `/home/app` with Debian's default `.bashrc`) and an `/app` owned by it. It's one layer, so the deleted apt lists never take up space.
  5. `USER app`, `WORKDIR /app`.
  6. `COPY --chown=app:app . ./`, then `RUN uv sync` to build `/home/app/.venv` from `pyproject.toml`.
  7. `ENTRYPOINT ["/bin/bash"]` plus `CMD ["-c", "source /home/app/.venv/bin/activate && exec bash"]`: the container starts as an interactive bash with the venv activated (`VIRTUAL_ENV` and `PATH` are exported, so they survive the `exec`; the `(name)` prompt prefix does not, see §4 step 6).
- **Mental model.** An image is a stack of transparent sheets. Each sheet records only what that step changed. Docker caches each sheet keyed by "the instruction plus everything below it plus the files it consumed". Change something and every sheet **above** it is redrawn.
- **Analogy.** A recipe card where each step is photographed. Change step 4 and you must re-cook steps 4-7, but steps 1-3 come from the photo album.
- **Misconception.** "Editing `cli.py` only rebuilds a tiny layer." Here `COPY . ./` comes **before** `RUN uv sync`, so changing any file in the folder (even `group_name` in `cli.py`) invalidates the `uv sync` layer and re-downloads every package on the next build. Later tutorials copy `pyproject.toml`/`uv.lock` first for exactly this reason (e.g. `llm-rag/Dockerfile:42-48`: `COPY --chown=app:app pyproject.toml uv.lock* ./`, `RUN uv sync --frozen`, then `COPY --chown=app:app . ./`). During development you avoid rebuilding at all, because the bind mount (3.4) makes code edits visible instantly.
- **Animation idea.** Stack seven translucent slabs labelled with their instructions. Highlight `cli.py` on the host and change one character. The `COPY` slab flashes red and the `uv sync` slab above it dissolves and re-forms (package icons raining in), while the `FROM`/`RUN apt` slabs below stay green with a "CACHED" stamp.

### 3.4 ★ Image vs container vs bind mount: where does state live?
- **Explanation.** An **image** is the read-only stack. A **container** is a running process with a thin writable layer on top. `--rm` deletes that writable layer on exit. `-v "$(pwd):/app"` **overlays** your host folder onto `/app`, hiding whatever the image had at `/app` (the `COPY`'d files). Three consequences:
  1. Editing `cli.py` in VS Code changes it inside the container immediately (`transcribe_audio/README.md:102`).
  2. Anything written under `/app` (downloads, outputs, `pyproject.toml`, `uv.lock`) lands on your **host** and survives `--rm`.
  3. Anything written elsewhere (for example `uv add` installing into `/home/app/.venv`) lives in the container's writable layer and **vanishes** on exit.

  This is why the Dockerfile moves the venv to `/home/app/.venv` (`README.md:192`). In L02's simple-translate image the venv was at `.venv` next to the code (`simple-translate/Dockerfile.txt:29`). Mounting over that would have hidden the venv, or exposed a host `.venv` built for macOS.
- **Mental model.** The container is a stage set. The image is the permanent scenery. `/app` is a window cut through the set that looks straight into your laptop's folder. Things placed in the window are on your desk; things placed on the set are swept away when the show ends (`--rm`).
- **Analogy.** A hotel room (container) where one drawer is magically connected to your home desk drawer (bind mount). Anything left in the rest of the room is cleaned out at checkout.
- **Misconception.** "`uv add` inside the container installed the package, so it's in my image now." It is in the container's venv only until you exit (verified: in the next `docker run` of the un-rebuilt image the venv was empty again, and a `uv sync` there had to reinstall all 26 packages). `pyproject.toml` (on the host, through the mount) remembers it, and you must **rebuild** for `uv sync` to bake it in (`transcribe_audio/README.md:110`; codecast:180).
- **Animation idea.** Draw the image as a 3D block with a `/app` cavity filled with grey "copied" files. A tube labelled `-v "$(pwd):/app"` descends from the laptop and slides a blue sheet (host files) over the cavity, and the grey files fade underneath. Then show `/home/app/.venv` as a separate box outside the cavity. Run `uv add`: new package cubes drop into `.venv` (red = ephemeral) while `pyproject.toml` in the blue sheet gains a line. Press "exit": the red cubes evaporate and the blue sheet stays on the laptop.

### 3.5 The uv dependency loop inside a container
- **Explanation.** The tutorial's loop is:
  1. `uv init --bare` on the host, giving an empty `pyproject.toml`;
  2. build the image (`uv sync` installs nothing yet);
  3. run it, and inside run `uv add google-cloud-storage google-cloud-speech ffmpeg-python`, which updates `pyproject.toml` plus `uv.lock` on the host **and** installs into the live venv;
  4. run the code;
  5. exit and rebuild so the deps are baked in (`transcribe_audio/README.md:19-24,104-110`).

  The codecast notes the shortcut: run `uv add` on the host right after `uv init`, and the first build already has everything (codecast:182-187, 279).
- **Mental model.** `pyproject.toml` is the shopping list, `uv.lock` the itemised receipt, and the venv the fridge. `uv add` writes the list, prints a receipt and stocks the fridge. `uv sync` restocks a fridge from the receipt.
- **Analogy.** Trying a recipe in a rental kitchen (the container): you buy ingredients there, but you also write them on your own list so your own kitchen (the image) can be stocked next time.
- **Misconception.** "`uv init --bare` is harmless boilerplate." It stamps `requires-python = ">=X.Y"`, where X.Y is the minor version of the interpreter uv discovers **on your host** (a uv-managed Python if you have one, otherwise the first `python3` on `PATH`). Verified with uv 0.11.32: it wrote `>=3.13` on a host whose default `python3` is 3.13, although 3.11 and 3.12 were also installed. If that is newer than the image's 3.12, `uv sync` inside the image silently **downloads the newest matching CPython** and builds the venv on it (verified: `Downloading cpython-3.15.0-linux-x86_64-gnu`, `Using CPython 3.15.0`; §6 G3).

### 3.6 ★ Service accounts and Application Default Credentials (ADC)
- **Explanation.** GCP checks every request twice:
  - **Authentication**: who is calling? Here that is the service account whose private key is in `mega-pipeline.json`.
  - **Authorisation**: may that identity do this? That is decided by IAM roles on the project or bucket (`README.md:92-95`).

  The client libraries never see your code pass a key. When you construct `storage.Client()`, `translate.Client()`, `TextToSpeechLongAudioSynthesizeClient()` or `speech.SpeechClient()`, they call `google.auth.default()`. That function checks the env var `GOOGLE_APPLICATION_CREDENTIALS` and loads the JSON. On the first request the credentials sign a JWT with the key's private key and exchange it for a short-lived (about one hour) OAuth2 access token, which is sent as an `Authorization: Bearer …` header. The `google.auth.default()` call is at `google/cloud/client/__init__.py:218` of google-cloud-core 2.8.0 (used by `storage.Client` and `translate.Client`); the GAPIC clients (Speech, TTS) make the same call in their transport. `genai.Client(vertexai=True, project=…)` is the exception: it loads credentials lazily on the first request (§5 excerpt 7).
- **Mental model.** The JSON key is a hotel key-card encoder. ADC is the front desk that, when asked, cuts you a 1-hour key card (the access token). IAM is the lock on each door deciding whether that card opens it.
- **Analogy.** A company badge for a robot employee: the robot (your app) badges in, not you.
- **Misconception.** "The key file is just a config file; leaking it is no big deal." It is a long-lived password for the course's project. Anyone holding it can run the APIs on the course's bill and do anything its IAM roles allow to the shared bucket. A second misconception: "`GOOGLE_APPLICATION_CREDENTIALS=secrets/mega-pipeline.json` always works." It's a **relative** path, so it works only while the process's cwd is `/app` (§6 G5).
- **Animation idea.** A JSON file icon is plugged into a "google.auth" machine, which stamps out a glowing token with a countdown timer. The token flies alongside each API request arrow and stops at an IAM gate shaped like a padlock with role names. A green check lets Storage through. A red X appears if you swap the role away.

### 3.7 ★ Managed AI APIs and long-running operations (LROs)
- **Explanation.** Each stage outsources the ML to a hosted API:
  - **Speech-to-Text v1.** ffmpeg converts the MP3 to FLAC, because MP3 is "a Beta feature and only available in v1p1beta1" according to `speech_v1/types/cloud_speech.py:561-563` in google-cloud-speech 2.41.0, and FLAC carries its own sample rate. The code then calls `long_running_recognize` and waits up to 90 s (`transcribe_audio/cli.py:65-78`). Automatic punctuation is off by default, so the raw transcript is unpunctuated, which is one reason stage B "corrects" it.
  - **Gemini on Vertex AI** through `google-genai`, `client.models.generate_content(model=..., contents=prompt)` (`generate_text/cli.py:23-25,73-78`).
  - **Cloud Translation v2** (Basic), `translate_client.translate(..., source_language="en", target_language="fr", format_="text")` (`translate_text/cli.py:58-64`).
  - **Text-to-Speech *Long Audio*.** `synthesize_long_audio` with an `output_gcs_uri`: the **TTS service writes the audio object straight into the bucket**, which is why C and E have no `--upload` (`synthesis_audio_en/cli.py:77-90`; `README.md:151`).

  An LRO returns an `operation` handle immediately; `.result(timeout=…)` polls until the server finishes.
- **Mental model.** Dropping off dry cleaning: you get a ticket (the operation) and come back later. With Long Audio TTS you even tell the cleaner to deliver to your locker (the bucket), so you never carry it home.
- **Analogy.** Ordering delivery to a friend's address versus picking it up yourself (`cli_11.py` picks up locally and then uploads; Google TTS delivers directly).
- **Misconception.** "Synthesis produces a local `.mp3` I can play." No local file is created (`synthesis_audio_en/README.md:8`), and the "skip if local file exists" check at `synthesis_audio_en/cli.py:57-58` can never fire. Also, the object is named `.mp3` but the request asks for `LINEAR16` (`synthesis_audio_en/cli.py:73`), which the TTS enum documents as "Uncompressed 16-bit signed little-endian samples (Linear PCM). Audio content returned as LINEAR16 also contains a WAV header." (`texttospeech_v1/types/cloud_tts.py:90-93`). See §10 E7.
- **Animation idea.** Container C hands a long scroll to a "TTS factory" cloud and receives only a ticket stub. A progress ring fills around the stub while, unseen by the container, a conveyor belt carries a sound-wave crate from the factory directly into the `text_audios/g/` drawer. Contrast with D: the translated page comes back into the container and must be carried up by `--upload`.

### 3.8 Secrets hygiene: `.gitignore` is not `.dockerignore`
- **Explanation.** The README promises the key won't reach GitHub because of `.gitignore` (`README.md:103-106`), and that's true for Git. But `docker build` sends the **whole folder** (the build context) to the builder, and `COPY . ./` copies all of it, `secrets/` included, into an image layer. On `main` no `.dockerignore` excludes it. If you then do the optional `docker push` (`transcribe_audio/README.md:136-140`), you publish the key. The "canonical" fix the README mentions, keeping secrets outside the repo (`README.md:106`), is what `solution`/`flexible-workflow` do: `SECRETS_DIR=$(pwd)/../../secrets/` mounted at `/secrets` at **run** time (`origin/solution:transcribe_audio/docker-shell.sh:9-10,96-99`).
- **Mental model.** `.gitignore` is a filter on what goes into the *history book*. `.dockerignore` is a filter on what goes into the *shipping box*. They are different boxes.
- **Analogy.** You hid your house key from the photo album (Git) but packed it in the moving box (the image) you're about to mail to strangers (Docker Hub).
- **Misconception.** "Docker reads `.gitignore`." It doesn't.

---

## 4. Step-by-step walkthrough

Order of work: A → B → C → D → E (`README.md:114-120`). Run every `docker` command **from inside the component folder**.

**Step 0: Prerequisites.** Finish Tutorial 0 (Docker Desktop running, `uv --version` works on the host) (`README.md:22-24`). *Checkpoint:* `docker run --rm hello-world` prints "Hello from Docker!" (a standard Docker check, not from the README).

**Step 1: Clone** (`README.md:32-35`):
```bash
git clone https://github.com/dlops-io/mega-pipeline.git
cd mega-pipeline
```
*Under the hood:* this gets `main` with five folders, each holding `README.md`, `cli.py`, `secrets/.gitkeep` and a `.gitignore`; `synthesis_audio/` also has the bonus `cli_11.py`, and `generate_text/` also has `pyproject.toml` and a stray `main.py` but **no** `.gitignore`. *Checkpoint:* `ls transcribe_audio` shows `README.md cli.py secrets`; there is **no Dockerfile** (`README.md:114`). The README's "Project Setup" step in each component is just "`cd` into the `<component>` folder" (`transcribe_audio/README.md:11-13`).

**Step 2: Put the key in every component** (`README.md:97-99`, `transcribe_audio/README.md:15-17`). Download `mega-pipeline.json` from Canvas and copy it to `transcribe_audio/secrets/`, `generate_text/secrets/`, `synthesis_audio_en/secrets/`, `translate_text/secrets/` and `synthesis_audio/secrets/`. A loop that does it (my suggestion, not in the README):
```bash
for d in transcribe_audio generate_text synthesis_audio_en translate_text synthesis_audio; do cp ~/Downloads/mega-pipeline.json "$d/secrets/"; done
```
*Checkpoint:* `git status` stays clean. `git check-ignore -v transcribe_audio/secrets/mega-pipeline.json` names the rule (verified: `transcribe_audio/.gitignore:3:/secrets`; for `generate_text`, which has no `.gitignore`, it is the root `.gitignore:4:secrets/`). *If it fails:* check the file name exactly. The code expects `mega-pipeline.json` (`README.md:195`), and browsers sometimes save `mega-pipeline (1).json`. The main README links Canvas file `25687801` (`README.md:99`), while the component READMEs link `23163432` (`transcribe_audio/README.md:17`). Use the main README's link (§10 E5).

### Component A: `transcribe_audio` (the slow, full-depth one)

**Step 3: Scaffold `pyproject.toml`.** Run in `transcribe_audio/` (`transcribe_audio/README.md:20-24`):
```bash
uv init --bare
```
*Under the hood:* writes only `pyproject.toml` with `name = "transcribe-audio"`, `version = "0.1.0"`, `requires-python = ">=X.Y"` and `dependencies = []`, where X.Y is the Python uv discovers on your host, and prints `` Initialized project `transcribe-audio` ``. (Verified: on a host whose `python3` is 3.13 it wrote `>=3.13`; `uv init --bare --python 3.12` wrote `>=3.12`.) *Checkpoint:* `cat pyproject.toml`. **If `requires-python` is above `>=3.12`, change it to `>=3.12`** (or delete the file and re-run as `uv init --bare --python 3.12`; this is a fix the README doesn't give). Otherwise see §6 G3. `git status` won't show the file, because `transcribe_audio/.gitignore:6` ignores `pyproject.toml`.

**Step 4: Write the `Dockerfile`.** The README gives it in pieces (`transcribe_audio/README.md:41-90`). Assembled, with the `FROM` line from `README.md:177`:
```dockerfile
FROM python:3.12-slim-bookworm
ARG DEBIAN_PACKAGES="build-essential ffmpeg"
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8
ENV PYTHONUNBUFFERED=1
ENV UV_LINK_MODE=copy
ENV UV_PROJECT_ENVIRONMENT=/home/app/.venv
ENV GOOGLE_APPLICATION_CREDENTIALS=secrets/mega-pipeline.json
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends $DEBIAN_PACKAGES && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir --upgrade pip && \
    pip install uv && \
    useradd -ms /bin/bash app -d /home/app -u 1000 && \
    mkdir -p /app && \
    chown app:app /app
USER app
WORKDIR /app
COPY --chown=app:app . ./
RUN uv sync
ENTRYPOINT ["/bin/bash"]
CMD ["-c", "source /home/app/.venv/bin/activate && exec bash"]
```
The longer appendix version (`README.md:175-225`) also has `set -ex;` and a `for i in $(seq 1 8); do mkdir -p "/usr/share/man/man${i}"; done` line. That recreates man-page directories that slim images delete, because some Debian packages' install scripts (Java's is the classic case) fail without them. Without it, as in the component README version, the `ffmpeg` install only prints harmless `update-alternatives: warning: skip creation of /usr/share/man/man1/… because associated file … doesn't exist` lines (verified). Its `ARG` is `"build-essential curl"` (`README.md:179`), which **lacks `ffmpeg`**, so don't paste it unchanged into `transcribe_audio`. *Strongly recommended (not in the README):* also create a `.dockerignore` containing `secrets/` (see §6 G1). The ENV still points at `secrets/mega-pipeline.json`, and the bind mount supplies it at run time.

**Step 5: Build.** The README says only "Build your docker image and give your image the name `transcribe_audio`" (`transcribe_audio/README.md:95`). The command (codecast:168):
```bash
docker build -t transcribe_audio .
```
*Under the hood:* the `.` folder is sent as the build context. BuildKit pulls `python:3.12-slim-bookworm` for your machine's architecture, runs the apt/pip/useradd `RUN`, copies the folder (secrets, and the Dockerfile itself, included), and runs `uv sync`. That creates `/home/app/.venv` with no third-party packages yet, plus a `/app/uv.lock` inside the image that lists only the project itself (verified). *You should see* five steps, `[1/5] FROM docker.io/library/python:3.12-slim-bookworm`, `[2/5] RUN apt-get update && …`, `[3/5] WORKDIR /app`, `[4/5] COPY --chown=app:app . ./`, `[5/5] RUN uv sync`; with `requires-python = ">=3.12"` the last one prints `Using CPython 3.12.15 interpreter at: /usr/local/bin/python3`, `Creating virtual environment at: /home/app/.venv`, `Resolved 1 package in …`. It ends with `naming to docker.io/library/transcribe_audio:latest` and a build-check warning (verified with Docker 29.8.2): `1 warning found … SecretsUsedInArgOrEnv: Do not use ARG or ENV instructions for sensitive data (ENV "GOOGLE_APPLICATION_CREDENTIALS")`. Here the value is only a path, but the warning is a good cue for G1. *If it fails or looks odd:* `Downloading cpython-3.15.0…` / `Using CPython 3.15.0` in the `uv sync` step means G3; ``error: No `pyproject.toml` found in current directory or any parent directory`` means step 3 was skipped. On first build the apt step takes the longest (about 50 s here, with `build-essential ffmpeg`).

**Step 6: Run the container** (`transcribe_audio/README.md:97-102`):
```bash
docker run --rm -ti -v "$(pwd):/app" transcribe_audio
```
*Under the hood:* `-ti` gives an interactive TTY. `--rm` deletes the container on exit. `-v "$(pwd):/app"` overlays the host folder on `/app`. Then the entrypoint `/bin/bash -c "source /home/app/.venv/bin/activate && exec bash"` replaces itself with an interactive bash whose venv is active. *You should see* (verified) a plain prompt `app@<container-id>:/app$`, e.g. `app@01560c557936:/app$`, **without** a `(transcribe-audio)` prefix: `activate` does set one (uv wrote `prompt = transcribe-audio` into `pyvenv.cfg`), but the new interactive bash reads `/home/app/.bashrc`, which resets `PS1`. The venv is still active, because `VIRTUAL_ENV` and `PATH` are exported. *Checkpoint (extra checks, not in the README):* `which python` prints `/home/app/.venv/bin/python`; `ls` shows your host files, including `secrets/`; `echo $GOOGLE_APPLICATION_CREDENTIALS` prints `secrets/mega-pipeline.json`. Running `python cli.py --help` **now** fails with `ModuleNotFoundError: No module named 'google'` (verified): the imports at the top of `cli.py` need step 7 first. *Windows:* the README's example is `winpty docker run --rm -ti -v "$(pwd)":/app generate_text` (`README.md:233-236`); swap in the component's name.

**Step 7: Add the Python packages, inside the container** (`transcribe_audio/README.md:104-110`). The packages are `google-cloud-storage`, `google-cloud-speech` and `ffmpeg-python`. As one command (codecast:175):
```bash
uv add google-cloud-storage google-cloud-speech ffmpeg-python
```
*Under the hood:* uv resolves the dependencies, writes them into `/app/pyproject.toml` and creates `/app/uv.lock` (both on your host via the mount), and installs them into `/home/app/.venv` (ephemeral). *Checkpoint:* on the host, `pyproject.toml` now lists three dependencies with lower bounds (verified on 2026-10-13: `"ffmpeg-python>=0.2.0"`, `"google-cloud-speech>=2.41.0"`, `"google-cloud-storage>=3.17.0"`; your versions will differ) and a ~100 KB `uv.lock` exists; inside, `python cli.py --help` now works. *If it fails:* ``error: failed to create file `/app/pyproject.toml`: Permission denied (os error 13)`` means a uid mismatch on a Linux host (G7, verified). `ffmpeg` (the PyPI package) is **not** `ffmpeg-python` (G9).

**Step 8: Set your group name.** On the host in VS Code, change `group_name = "pavlos"` at `transcribe_audio/cli.py:21` (README: `transcribe_audio/README.md:114`). The change is visible inside the container instantly through the mount.

**Step 9: Check the CLI.**
```bash
python cli.py --help
```
*You should see* the usage block in `transcribe_audio/README.md:117-127` (`usage: cli.py [-h] [-d] [-t] [-u]` … `-d, --download    Download audio files from GCS bucket` …); verified identical, line for line, once the packages are installed. `transcribe_audio`'s `--help` needs no key (its clients are created inside the functions), but in C, D and E it does (G5).

**Step 10: Download** (`README.md:134`; short form `python cli.py -d`, `transcribe_audio/README.md:131`):
```bash
python cli.py --download
```
*Under the hood* (`transcribe_audio/cli.py:29-43`):
1. Delete the local `input_audios/`.
2. Recreate `input_audios/` and `text_prompts/<group>/`.
3. `storage.Client()` triggers ADC.
4. `get_bucket("mega-pipeline-bucket")`.
5. List every object under `input_audios/` (shared by all groups), skip the zero-byte "folder" object, and download each file to the same relative path.

*You should see* `Args: Namespace(download=True, transcribe=False, upload=False)`, then `download`, then object names like `input_audios/input-….mp3`. A new `input_audios/` folder appears **on your host**. *If it fails:* `DefaultCredentialsError: File secrets/mega-pipeline.json was not found.` means G5. `403 … does not have storage.buckets.get access` means the key lacks bucket read rights; ask staff.

**Step 11: Transcribe** (`README.md:135`):
```bash
python cli.py --transcribe
```
*Under the hood* (`transcribe_audio/cli.py:46-96`), for each file in `input_audios/`:
1. Derive `uuid` by stripping `.mp3`.
2. Skip it if `text_prompts/<group>/<uuid>.txt` already exists.
3. Convert MP3 to FLAC with ffmpeg in a temp dir.
4. Read the bytes and send them inline to `long_running_recognize` with `language_code="en-US"`.
5. Wait up to 90 s.
6. Join all result segments (the `c6bbc9b` fix) and write the `.txt`.

*You should see* `Transcribing: input_audios/input-….mp3`, a burst of ffmpeg log lines, `response: results { alternatives { transcript: "…" …`, then the joined transcript. *Checkpoint:* `text_prompts/<group>/input-….txt` exists on the host and contains words, not the literal `None` (G20). *If it fails:* `FileNotFoundError: … 'ffmpeg'` means G8. `ModuleNotFoundError: No module named 'ffmpeg'` means step 7 was skipped. A timeout or "inline audio" style error means §10 open question Q2.

**Step 12: Upload** (`README.md:136`):
```bash
python cli.py --upload
```
*Under the hood* (`transcribe_audio/cli.py:99-115`): globs `text_prompts/<group>/input-*.txt` and uploads each file to the identical object name. *You should see* `Uploading: text_prompts/<group>/input-….txt text_prompts/<group>/input-….txt`. *Checkpoint:* your group's Transcribe cell lights up on the leaderboard (`transcribe_audio/README.md:134`). Tip: flags combine, and `python cli.py -d -t -u` runs all three in order (`transcribe_audio/cli.py:121-126`).

**Step 13: Bake the dependencies.** `exit` the container, then re-run `docker build -t transcribe_audio .` (`transcribe_audio/README.md:110`). The README states this right after the `uv add` list, before the CLI sections; in practice you do it once the component works, before you close for the day. *Checkpoint:* the next `docker run …` lets `python -c "import google.cloud.speech"` succeed without `uv add`, because `COPY` brought the new `pyproject.toml` and `uv.lock` and `uv sync` installed the locked versions.

### Component B: `generate_text` (same recipe; drop ffmpeg, add an LLM)

**Step 14: Set up.** `cd ../generate_text` (`generate_text/README.md:13`), copy the key into `secrets/` (`:16`). **Skip `uv init --bare`** (`:20-24`). This folder already has a `pyproject.toml`, so `uv init --bare` fails with ``error: Project is already initialized in `…/generate_text` (`pyproject.toml` file exists)`` and exit code 2 (verified on a copy). The committed file says `requires-python = ">=3.14"` (`generate_text/pyproject.toml:4`), which does not match the 3.12 base image. **Edit it to `>=3.12`** (§10 E1). Write the Dockerfile with `ARG DEBIAN_PACKAGES="build-essential"` (`generate_text/README.md:45`).

**Step 15: Build, run and add the packages:**
```bash
docker build -t generate_text .
docker run --rm -ti -v "$(pwd):/app" generate_text
uv add google-cloud-storage google-genai
```
(The run line is `generate_text/README.md:99`, the packages are `generate_text/README.md:104-106`, and the build and `uv add` lines are codecast:216,219.) Both packages are **already** in the committed `pyproject.toml` (`generate_text/pyproject.toml:5-8`: `"google-cloud-storage>=3.12.0"`, `"google-genai>=2.8.0"`), so the first build's `uv sync` already installs them. `uv add google-cloud-storage google-genai` is then a no-op for `pyproject.toml` (verified: the existing constraints are kept) and only writes `uv.lock` to the host; run it anyway to follow the README. If you skipped the `requires-python` edit, that first build silently runs on a downloaded CPython (3.15.0 when checked) instead of 3.12 (G3).

**Step 16: Set the group and run** (`generate_text/cli.py:19`; `README.md:140-144`):
```bash
python cli.py --download
python cli.py --generate
python cli.py --upload
```
*Under the hood:*
- `--download` deletes the **whole** local `text_prompts/` and fetches only `text_prompts/<group>/input-*.txt` (`generate_text/cli.py:33-44`). If stage A hasn't uploaded for your group, nothing comes down.
- `--generate` builds a cheese-podcast prompt around the transcript, "1000 or more words" with host Pavlos Protopapas (`generate_text/cli.py:65-72`), and calls Gemini on Vertex AI in `us-central1` with model `$GEMINI_MODEL` or `gemini-2.5-flash-lite`.
- `--upload` pushes `text_paragraphs/<group>/input-*.txt`.

*You should see* the prompt printed, three blank lines, `Generated text:` and a long article. To try another model, start the container with `-e GEMINI_MODEL=<model-id>` (an exercise in §9). *If it fails:* `404 … Publisher Model … not found` means a retired or misspelled model name. `429 RESOURCE_EXHAUSTED` means the whole class is sharing one project quota, so wait and retry (G12).

### Component C: `synthesis_audio_en`

**Step 17.** Run in `synthesis_audio_en/`: `uv init --bare` (fix `requires-python`), Dockerfile with `ARG DEBIAN_PACKAGES="build-essential"` (`synthesis_audio_en/README.md:45`; ignore the "keep ffmpeg" sentence at `:38`, see §10 E3), `docker build -t synthesis_audio_en .`, `docker run --rm -ti -v "$(pwd):/app" synthesis_audio_en` (`:99`), then inside `uv add google-cloud-storage google-cloud-texttospeech` (`:104-106`), and set `group_name` (`synthesis_audio_en/cli.py:18`). Then (`README.md:147-151`):
```bash
python cli.py --download
python cli.py --synthesis
```
*Under the hood:* `--download` pulls `text_paragraphs/<group>/input-*.txt`. `--synthesis` checks for each file whether `text_audios/<group>/<uuid>.mp3` **already exists in GCS**; if not, it sends a `SynthesizeLongAudioRequest` (voice `en-US-Standard-B`, `LINEAR16`, `output_gcs_uri=gs://mega-pipeline-bucket/text_audios/<group>/<uuid>.mp3`) and waits up to 300 s (`synthesis_audio_en/cli.py:44-91`). *You should see* `Audio file will be saved to GCS bucket automatically.` and no new local audio file. *Checkpoint:* the leaderboard (or the GCS console) shows `text_audios/<group>/input-….mp3`. There is **no `--upload`** (`README.md:151`).

### Component D: `translate_text`

**Step 18.** Run in `translate_text/`: the same recipe with `ARG DEBIAN_PACKAGES="build-essential"` (`translate_text/README.md:45`), then `uv add google-cloud-storage google-cloud-translate` (`:104-106`); `translate_v2` ships inside `google-cloud-translate`. Set `translate_text/cli.py:18`. Then (`README.md:155-157`):
```bash
python cli.py --download
python cli.py --translate
python cli.py --upload
```
*Under the hood:* this reads `text_paragraphs/<group>/` (the **same** input as C, not C's output) and calls Translation v2 `en→fr` with `format_="text"`. It saves `result["translatedText"]` to `text_translated/<group>/<uuid>.txt` and uploads it (`translate_text/cli.py:42-88`). *You should see* French text printed. *If it fails:* note that `translate.Client()` is created at **import** (`translate_text/cli.py:20`), so even `python cli.py --help` dies with `DefaultCredentialsError` if the key is missing (G5).

### Component E: `synthesis_audio` (French)

**Step 19.** Run in `synthesis_audio/`: the same packages as C (`synthesis_audio/README.md:104-106`) and `ARG DEBIAN_PACKAGES="build-essential"` (`:45`). Set `synthesis_audio/cli.py:18`. Then (`README.md:161-164`):
```bash
python cli.py --download
python cli.py --synthesis
```
*Under the hood:* identical to C, but it reads `text_translated/<group>/` and uses voice `fr-FR-Standard-C`, writing `output_audios/<group>/<uuid>.mp3` (`synthesis_audio/cli.py:43-90`). `python cli.py --help` prints the description "Transcribe audio file to text" (a copy-paste slip at `synthesis_audio/cli.py:105`; the README shows "Synthesis audio from text" at `synthesis_audio/README.md:118`).

**Step 20 (bonus): ElevenLabs in the instructor's voice** (`synthesis_audio/README.md:132-156`). Create an ElevenLabs account and API key (`:138`), create `secrets/11lab_api_key.txt` with `XI_API_KEY=your_api_key_here` (`:139-142`, no spaces around `=`; see §5 excerpt 11), run `uv add requests` (`:144-147`; `requests` is in fact already installed as a dependency of `google-cloud-storage`, verified, so this only makes it an explicit dependency), set `group_name` in `cli_11.py:19` (`:112`), then (`:150-154`):
```bash
python cli_11.py --download
python cli_11.py --synthesis
python cli_11.py --upload
```
*Under the hood:* POSTs to `https://api.elevenlabs.io/v1/text-to-speech/TG3keNw5JZvsEiTtWt7t/stream` with model `eleven_multilingual_v2`, streams the bytes into `output_audios_pp/<group>/<uuid>.mp3` locally (the README's "saves audio **locally first**", `:156`), and `--upload` then pushes them to the same object names (`synthesis_audio/cli_11.py:60-133`). If the API refuses, `--synthesis` just prints the response body and carries on (`:111-113`), so read its output. The key file is read at import (`cli_11.py:33`), so without it even `--download` fails with `FileNotFoundError`. Whether your ElevenLabs account can use that voice ID is open (§10 Q5).

**Step 21 (optional): Push to Docker Hub** (`transcribe_audio/README.md:136-140`; sign up and create an access token first, `:137`):
```bash
docker login -u <USER NAME> -p <ACCESS TOKEN>
docker tag transcribe_audio <USER NAME>/transcribe_audio
docker push <USER NAME>/transcribe_audio
```
**Stop first:** unless you added a `.dockerignore` with `secrets/` and rebuilt, this image contains `/app/secrets/mega-pipeline.json` (G1). Prefer `docker login -u <USER NAME>` and paste the token at the prompt, or use `--password-stdin` (G13). An image built on Apple Silicon is `linux/arm64` and won't run on an amd64 VM without emulation (G6).

**Step 22: Clean up.** Delete the local images (§2). Keep the key out of every repo, including your own study repo (G14). The README's last section only says that solutions "will be posted here after the assignment deadline" (`README.md:238-239`).

---

## 5. Code tour

```
mega-pipeline/  (main @ c6bbc9b)
├── README.md                    overview, bucket layout, credentials, sample Dockerfile, quick reference
├── .gitignore                   ignores secrets/, outputs, .vscode, and staff-only dirs (/api-service, /frontend, …)
├── mega-pipeline-flow.png       6-step flow diagram (1 record → 2 transcribe → 3 generate → 4 synth EN / 5 translate → 6 synth FR, all over a "GCS Bucket")
├── mega-pipeline-bucket.png     GCS console screenshot of the bucket (us-central1, Standard, Not public; 5 prefixes) — never show it on screen; redraw schematically
├── transcribe_audio/   A  README.md · cli.py (Speech-to-Text) · .gitignore (also ignores Dockerfile, pyproject.toml, uv.lock!) · secrets/.gitkeep
├── generate_text/      B  README.md · cli.py (Gemini) · pyproject.toml (requires-python >=3.14!) · main.py (uv-init leftover) · secrets/.gitkeep  [no .gitignore]
├── synthesis_audio_en/ C  README.md · cli.py (TTS Long Audio, en-US) · .gitignore · secrets/.gitkeep
├── translate_text/     D  README.md · cli.py (Translation v2) · .gitignore · secrets/.gitkeep
└── synthesis_audio/    E  README.md · cli.py (TTS Long Audio, fr-FR) · cli_11.py (ElevenLabs bonus) · .gitignore · secrets/.gitkeep
   + files YOU create in each folder: Dockerfile, pyproject.toml (+ uv.lock), secrets/mega-pipeline.json, (recommended) .dockerignore
```

**1. The environment block of the Dockerfile**

```dockerfile
# README.md:187-195
# Tell Python to disable buffering so we don't lose any logs.
ENV PYTHONUNBUFFERED=1

# Tell uv to copy packages from the wheel into the site-packages
ENV UV_LINK_MODE=copy
ENV UV_PROJECT_ENVIRONMENT=/home/app/.venv

# This is done for the tutorial only
ENV GOOGLE_APPLICATION_CREDENTIALS=secrets/mega-pipeline.json
```
- `PYTHONUNBUFFERED=1`: `print()` output reaches your terminal immediately instead of sitting in a buffer, which matters when a 300 s LRO is running.
- `UV_LINK_MODE=copy`: uv normally hard-links files from its cache into the venv; this makes it copy them. Hard links fail (with a warning and a fallback to copying) only when cache and venv are on different filesystems, e.g. a BuildKit cache mount. Here they are not, so the line is a safe default rather than a fix (verified, §3.3).
- `UV_PROJECT_ENVIRONMENT=/home/app/.venv`: **the key line for this lecture.** The venv lives outside `/app`, so the `-v "$(pwd):/app"` mount can't hide it.
- `GOOGLE_APPLICATION_CREDENTIALS=…`: the env var ADC reads. It is relative, so it depends on cwd `/app`. "For the tutorial only": `solution`/`flexible-workflow` remove it from the image and pass `-e GOOGLE_APPLICATION_CREDENTIALS=/secrets/mega-pipeline.json` at run time instead.

**2. The one-layer system setup**

```dockerfile
# README.md:197-210
# Ensure we have an up to date baseline, install dependencies and
# create a user so we don't run the app as root
RUN set -ex; \
    for i in $(seq 1 8); do mkdir -p "/usr/share/man/man${i}"; done && \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends $DEBIAN_PACKAGES && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir --upgrade pip && \
    pip install uv && \
    useradd -ms /bin/bash app -d /home/app -u 1000 && \
    mkdir -p /app && \
    chown app:app /app
```
- `set -ex`: print each command and stop at the first failure.
- `mkdir … man${i}`: slim images strip `/usr/share/man`, and some packages' post-install scripts break without it.
- `--no-install-recommends $DEBIAN_PACKAGES`: install only what you asked for (`build-essential`, plus `ffmpeg` for A).
- `apt-get clean && rm -rf /var/lib/apt/lists/*`: deleted *in the same layer*, so the package index never bloats the image.
- `pip install uv`: plain pip works here because the official Python image doesn't mark its Python "externally managed", unlike the VM in L01 (codecast:124-129; verified: no `/usr/local/lib/python3.12/EXTERNALLY-MANAGED`). pip prints a "Running pip as the 'root' user…" warning, which is harmless here. It installs whatever uv is newest on PyPI (0.13.0 on 2026-10-13), so the uv in the image is not pinned.
- `useradd … -u 1000` and `chown app:app /app`: a non-root user that owns `/app`, so the app never needs root.

**3. User, copy, sync, start**

```dockerfile
# README.md:212-224
# Switch to the new user
USER app
WORKDIR /app

# Copy the source code
COPY --chown=app:app . ./

RUN uv sync

# Entry point
ENTRYPOINT ["/bin/bash"]
# Get into the uv virtual environment shell
CMD ["-c", "source /home/app/.venv/bin/activate && exec bash"]
```
- `USER app` comes before `COPY`/`RUN uv sync`, so the venv and caches are owned by `app`. `--chown=app:app` makes the copied files `app`-owned too, since `COPY` otherwise writes them as root.
- `COPY . ./`: copies **everything** in the build context, including `secrets/` (no `.dockerignore`), the `Dockerfile` itself and any `input_audios/` you already downloaded (verified: `/app/Dockerfile` and `/app/secrets/mega-pipeline.json` were in the image).
- `RUN uv sync`: builds `/home/app/.venv` from `pyproject.toml`/`uv.lock`.
- `ENTRYPOINT` + `CMD`: the container runs `/bin/bash -c "source …activate && exec bash"`. `exec` replaces the wrapper shell with an interactive one that inherits the exported environment (`VIRTUAL_ENV`, `PATH`), but re-reads `~/.bashrc`, so the venv's prompt prefix is lost (verified). Whatever you put after the image name in `docker run` **replaces `CMD`** and is passed to bash. Exercise 4 shows why `docker run … transcribe_audio python cli.py -d` doesn't work.

**4. Stage A download: listing a prefix**

```python
# transcribe_audio/cli.py:29-43
def download():
    print("download")

    # Clear
    shutil.rmtree(input_audios, ignore_errors=True, onerror=None)
    makedirs()

    client = storage.Client()
    bucket = client.get_bucket(bucket_name)

    blobs = bucket.list_blobs(prefix=input_audios+"/")
    for blob in blobs:
        print(blob.name)
        if not blob.name.endswith("/"):
            blob.download_to_filename(blob.name)
```
- `shutil.rmtree(input_audios, …)`: start clean, but only the *inputs*. Outputs in `text_prompts/` survive, which is what makes reruns skip finished work.
- `storage.Client()`: the first ADC call. No key path appears in the code.
- `client.get_bucket(...)` makes an API call (it needs `storage.buckets.get`). A's own `upload()` and the other stages use `storage_client.bucket(...)`, which only builds a local handle.
- `list_blobs(prefix="input_audios/")`: GCS has no folders; this is "every object whose name starts with…". Note there is **no group** in this prefix: all teams transcribe the same audio.
- `endswith("/")`: skips the zero-byte placeholder object the console creates for "folders".
- `download_to_filename(blob.name)`: the local path mirrors the object name. The bind mount puts it on your host.

**5. Stage A transcription: ffmpeg, then a long-running Speech request**

```python
# transcribe_audio/cli.py:64-78
        print("Transcribing:", audio_path)
        with TemporaryDirectory() as audio_dir:
            flac_path = os.path.join(audio_dir, "audio.flac")
            stream = ffmpeg.input(audio_path)
            stream = ffmpeg.output(stream, flac_path)
            ffmpeg.run(stream)

            with io.open(flac_path, "rb") as audio_file:
                content = audio_file.read()

            # Transcribe
            audio = speech.RecognitionAudio(content=content)
            config = speech.RecognitionConfig(language_code="en-US")
            operation = client.long_running_recognize(config=config, audio=audio)
            response = operation.result(timeout=90)
```
- `ffmpeg.input/output/run`: `ffmpeg-python` only builds a command line and runs the **`ffmpeg` binary** via `subprocess.Popen` (`ffmpeg/_run.py:284`). That's why `ffmpeg` must be in the apt `ARG`.
- Why FLAC: v1 Speech doesn't take MP3 (beta-only), and for FLAC/WAV the `encoding` and `sample_rate_hertz` fields are optional because the header carries them. So `RecognitionConfig` needs only `language_code`.
- `RecognitionAudio(content=…)`: the bytes go **inline** in the request (the alternative is `uri="gs://…"`).
- `long_running_recognize(...)` returns an operation handle. `.result(timeout=90)` blocks, polling, for up to 90 s.
- Lines 84-90 (not shown) then concatenate `result.alternatives[0].transcript` for **every** result. That is the `c6bbc9b` fix: the API splits long audio at pauses, and the old code kept only the first chunk.

**6. Stage A upload: the hand-off contract**

```python
# transcribe_audio/cli.py:104-115
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Get the list of text file
    text_files = glob.glob(os.path.join(text_prompts, group_name, "input-*.txt"))

    for text_file in text_files:
        filename = os.path.basename(text_file)
        destination_blob_name = os.path.join(text_prompts, group_name, filename)
        blob = bucket.blob(destination_blob_name)
        print("Uploading:",destination_blob_name, text_file)
        blob.upload_from_filename(text_file)
```
- The glob `input-*.txt` is half of the contract. Stage B downloads with the matching `match_glob=f"{text_prompts}/{group_name}/input-*.txt"` (`generate_text/cli.py:42`). A file not named `input-…` is silently never handed on.
- `os.path.join(text_prompts, group_name, filename)` is the object name, with the group as the namespace. `upload_from_filename` overwrites any existing object of that name, which is why a wrong `group_name` can clobber another team.

**7. Stage B: one LLM call**

```python
# generate_text/cli.py:64-78
        # Generate output
        input_prompt = f"""
            Create a transcript for the podcast about cheese with 1000 or more words.
            Use the below text as a starting point for the cheese podcast.
            Output the transcript as paragraphs and not with who is talking or any "Sound" or any other extra information.
            Do not highlight or make words bold.
            The host's name is Pavlos Protopapas.
            {input_text}
        """
        model_name = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash-lite")
        print(input_prompt,"\n\n\n")
        response = client.models.generate_content(
            model=model_name, contents=input_prompt
        )
        paragraph = response.text
```
- The prompt is a plain f-string. The rough transcript is appended at the end, and the instructions push for TTS-friendly prose: no speaker labels, no "Sound" cues, no bold.
- `os.environ.get("GEMINI_MODEL", …)`: the one runtime knob. Pass `-e GEMINI_MODEL=…` to `docker run` to change models without editing code.
- `client` was created at import as `genai.Client(vertexai=True, project=gcp_project, location='us-central1')` (`generate_text/cli.py:23-25`), so this is Gemini **on Vertex AI**, billed to `ac215-project` and authenticated with the same service-account key. In google-genai 2.29.0, when `project` is given, credentials are loaded lazily on the first request (`_api_client.py:1306-1312`), so a missing key surfaces at `--generate`, not at import.
- `response.text`: the concatenated text of the first candidate.

**8. Stage C/E: the TTS service writes straight to GCS**

```python
# synthesis_audio_en/cli.py:77-90
            parent = f"projects/{gcp_project}/locations/us-central1"
            output_gcs_uri = f"gs://{bucket_name}/{audio_blob_name}"

            request = texttospeech.SynthesizeLongAudioRequest(
                parent=parent,
                input=input,
                audio_config=audio_config,
                voice=voice,
                output_gcs_uri=output_gcs_uri,
            )

            operation = client.synthesize_long_audio(request=request)
            # Set a deadline for your LRO to finish. 300 seconds is reasonable, but can be adjusted depending on the length of the input.
            result = operation.result(timeout=300)
            print("Audio file will be saved to GCS bucket automatically.")
```
- `parent`: the long-audio API is a project- and region-scoped resource (`us-central1`, the same region as the bucket).
- `output_gcs_uri`: the destination object. The API docs say the "bucket must already exist" (`texttospeech_v1/types/cloud_tts_lrs.py:49-53`).
- Just above (`synthesis_audio_en/cli.py:64-69`), the code checks `blob.exists()` first. That GCS check, not the local `os.path.exists` at `:57`, is the real "already done" test. To regenerate, delete the object in the bucket.
- `synthesis_audio/cli.py:76-90` is the same block with voice `fr-FR-Standard-C` (`:47-48`) and prefix `output_audios`.

**9. Stage D: Translation v2**

```python
# translate_text/cli.py:58-64
        result = translate_client.translate(
            input_text,
            source_language="en",
            target_language="fr",
            format_="text",
        )
        translated_text = result["translatedText"]
        print(translated_text)
```
- `translate_client = translate.Client()` was built at import (`translate_text/cli.py:20`) from `google.cloud.translate_v2`, so ADC runs at import.
- `format_="text"` (with the trailing underscore, because `format` is a Python builtin): treat the input as plain text rather than HTML, so the API won't HTML-escape apostrophes and the like.
- The response is a dict, and `translatedText` is the French string. Change `target_language` (and stage E's voice) to retarget the whole downstream pipeline.

**10. Where `solution`/`flexible-workflow` move the secret: the `docker-shell.sh` run block**

```bash
# origin/solution:transcribe_audio/docker-shell.sh:95-100
    # Run Container
    docker run --rm --name $IMAGE_NAME -ti \
    -v "$BASE_DIR":/app \
    -v "$SECRETS_DIR":/secrets \
    -e GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS \
    $CONTAINER_IMAGE
```
- This is not used on `main`, where you type `docker run` by hand, but it is where the course goes next. `BASE_DIR=$(pwd)`, `SECRETS_DIR=$(pwd)/../../secrets/` and `GOOGLE_APPLICATION_CREDENTIALS=/secrets/mega-pipeline.json` are set at `:8-10`.
- The second `-v` mounts a `secrets/` folder that sits **next to** the repo (two levels up from the component folder) at `/secrets`. The key is never in the build context, so it can't be baked into the image, and the absolute `/secrets/…` path works from any cwd.
- `--name $IMAGE_NAME` gives the container a predictable name (`mega-pipeline-transcribe-audio`). `$CONTAINER_IMAGE` is the local image if one exists, otherwise `dlops/<name>` from Docker Hub (`:86-93`). The script's `prod` mode builds `linux/amd64,linux/arm64` with `docker buildx` and pushes (`:51-72`). `simple` has a 23-line build-then-run version of the same script.

**11. The bonus reads its key at import time**

```python
# synthesis_audio/cli_11.py:29-39
#Define the path to the secrets file
secrets_file_path = 'secrets/11lab_api_key.txt'

# Read the file and set the environment variable
with open(secrets_file_path) as f:
    for line in f:
        if 'XI_API_KEY' in line:
            key, value = line.strip().split('=')
            os.environ[key] = value

XI_API_KEY = os.environ['XI_API_KEY']  
```
- This is module-level code, so it runs for every invocation, including `--download` and `--help`. No key file means `FileNotFoundError`.
- `split('=')` assumes exactly one `=`. `strip()` removes a trailing `\r` from a Windows editor, but a second `=` on the line raises `ValueError: too many values to unpack (expected 2)`.
- Spaces matter: `XI_API_KEY = abc` sets a variable named `'XI_API_KEY '` (with a trailing space) to `' abc'`, and the next line then raises `KeyError: 'XI_API_KEY'`.
- `os.environ['XI_API_KEY']` also raises `KeyError` if no line contained `XI_API_KEY` at all.

**12. What Git will and won't keep**

```gitignore
# transcribe_audio/.gitignore:1-9
# misc
.DS_Store
/secrets
docker-shell.sh
Dockerfile
pyproject.toml
uv.lock
/input_audios
/text_prompts
```
- `/secrets`: good, the key stays out of Git.
- `Dockerfile`, `pyproject.toml`, `uv.lock`, `docker-shell.sh`: so the course repo doesn't receive students' solutions, **your own work is invisible to `git status`**. If you mirror this into your own study repo, you must remove these lines or `git add -f` the files.
- `/input_audios`, `/text_prompts`: downloaded data and outputs are not committed. `synthesis_audio_en/.gitignore:8`, `translate_text/.gitignore:8-9` and `synthesis_audio/.gitignore:8-10` do the same for their folders. `generate_text/` has **no** `.gitignore` (deleted in `c8cb0f7`), so its `text_prompts/`, `text_paragraphs/`, `Dockerfile` and `uv.lock` show up as untracked and the edited `pyproject.toml` (tracked) as modified (verified with `git check-ignore --no-index`). The root `.gitignore:4` `secrets/` still protects its key.

---

## 6. Gotchas and common errors

**G1: The service-account key gets baked into your image.**
- *Symptom:* `docker run --rm --entrypoint ls transcribe_audio -la /app/secrets` (no bind mount) lists `mega-pipeline.json` (verified with a dummy key file). The build's `SecretsUsedInArgOrEnv` warning (§4 step 5) is a hint, though it fires on the `ENV`, not on the copied file.
- *Cause:* `COPY --chown=app:app . ./` (`README.md:217`; `transcribe_audio/README.md:82`) and no `.dockerignore` anywhere on `main` (nor on `simple`, `solution` or `flexible-workflow`). `.gitignore` doesn't apply to Docker builds. The optional push (`transcribe_audio/README.md:136-140`) would publish the key.
- *Fix:* add a `.dockerignore` with `secrets/` (and, optionally, `input_audios/`, `text_*/`, `.venv/`) in every component and rebuild. If you already pushed, delete the Docker Hub repo and **tell the staff so the key can be rotated**. Long term, keep secrets outside the repo and mount them at run time (§5 excerpt 10).

**G2: Wrong or default `group_name`.**
- *Symptom:* your leaderboard row stays empty, or your uploads land in `…/pavlos/…`.
- *Cause:* the default is `"pavlos"` with no assert (`transcribe_audio/cli.py:21` and the corresponding line in every `cli.py`). The value must be **identical in all five** `cli.py` files, because each stage downloads `<prefix>/<group_name>/…` written by the previous one.
- *Fix:* set it in all six files (five `cli.py` plus `cli_11.py`). The README warns about this at `README.md:124`.

**G3: `requires-python` newer than the image's Python 3.12.**
- *Symptom:* during `docker build`, the `RUN uv sync` step either:
  - **silently downloads a separate CPython**, the newest that satisfies the constraint, and builds the venv on it. Verified with `>=3.13` and uv 0.13.0 in the image: `Downloading cpython-3.15.0-linux-x86_64-gnu (download) (35.9MiB)`, `Using CPython 3.15.0`, and `.venv/bin/python -> /home/app/.local/share/uv/python/cpython-3.15-linux-x86_64-gnu/bin/python3.15`. The build succeeds, but the `python:3.12` base is now pointless, the image is bigger, and you are on a Python nobody tested; or, if Python downloads are disabled,
  - **fails** with `error: No interpreter found for Python >=3.14 in managed installations or search path` and the hint `A managed Python download is available for Python >=3.14, but Python downloads are set to 'never'` (verified with `UV_PYTHON_DOWNLOADS=never`).
- *Cause:* `uv init --bare` stamps the Python uv finds on your **host** into `requires-python` (verified: `>=3.13` on a 3.13 host). `generate_text/pyproject.toml:4` is committed as `>=3.14`. The instructor's own run-sheet flags this (codecast:152), though it predicts a build failure, which happens only with downloads disabled.
- *Fix:* set `requires-python = ">=3.12"` (last year's README pinned `">=3.12,<3.13"`, `origin/solution:transcribe_audio/README.md:36`), or run `uv init --bare --python 3.12`. *Checkpoint:* the `uv sync` build step says `Using CPython 3.12.15 interpreter at: /usr/local/bin/python3`.

**G4: `uv init --bare` fails in `generate_text`.**
- *Symptom:* `error: Project is already initialized in … (pyproject.toml file exists)` (verified on a copy).
- *Cause:* `generate_text/pyproject.toml` and `main.py` are committed (`c8cb0f7`, `065bdc4`), yet `generate_text/README.md:20-24` still tells you to run `uv init --bare`.
- *Fix:* skip that step. Edit `requires-python` (G3), and optionally delete `main.py`.

**G5: `DefaultCredentialsError: File secrets/mega-pipeline.json was not found.`**
- *Cause:* the env var is a relative path (`README.md:195`), and `google.auth` checks `os.path.exists(filename)` relative to the current directory (`google/auth/_default.py:176-179`). The error appears if:
  - the key isn't in *this* component's `secrets/` (each folder needs its own copy);
  - you `cd` away from `/app` inside the container;
  - you ran `docker run` from the repo root, so `/app` is the whole repo.

  In `translate_text`, `synthesis_audio_en` and `synthesis_audio` the client is created at import (`translate_text/cli.py:20`, `synthesis_audio_en/cli.py:22`, `synthesis_audio/cli.py:21`), so even `--help` fails (verified for `translate_text` and `synthesis_audio_en`: the traceback ends in `google/auth/_default.py`, line 178, `google.auth.exceptions.DefaultCredentialsError: File secrets/mega-pipeline.json was not found.`). In `generate_text` the Gemini client loads credentials lazily, so the error appears only at `--generate` (verified).
- *Fix:* `cd /app`, confirm `ls secrets/` shows the key, and run `docker run` from inside the component folder.

**G6: Apple Silicon image pushed to Docker Hub won't run on an amd64 VM.**
- *Symptom:* on the VM you get `exec format error`, or the warning "requested image's platform (linux/arm64) does not match the detected host platform (linux/amd64)".
- *Cause:* `docker build` on an M-series Mac produces `linux/arm64` (`python:3.12-slim-bookworm` is multi-arch). Locally everything works.
- *Fix:* `docker buildx build --platform linux/amd64,linux/arm64 --push -t <user>/<name> .`, which is what `origin/solution:transcribe_audio/docker-shell.sh:62-70` does in `prod` mode.

**G7: ``error: failed to create file `/app/pyproject.toml`: Permission denied (os error 13)`` from `uv add` (or `PermissionError: [Errno 13] Permission denied: 'input_audios'` from `cli.py`) on a Linux host.**
- *Cause:* the container runs as uid 1000 (`README.md:208`), but on a native Linux host or VM the bind-mounted folder belongs to your uid. Verified with a root-owned folder: `uv add` failed with exactly that message, and with the folder `chown`ed to 1000 the same command worked. The first user on most Linux desktops is uid 1000, so it usually works; it breaks when you are root (e.g. working as root on a VM) or another uid. Docker Desktop on macOS/Windows maps file ownership for you.
- *Fix (suggestions, not from the README):* work in a folder owned by uid 1000 (`sudo chown -R 1000:1000 <component>`), or `chmod -R a+rwX` the component folder. Running with `-u "$(id -u):$(id -g)"` is not a clean fix: that uid has no home directory in the image and doesn't own `/home/app/.venv` (verified with uid 1234: `uv add` failed with `` Failed to initialize cache at `/.cache/uv` `` … `Permission denied (os error 13)`).

**G8: `FileNotFoundError: [Errno 2] No such file or directory: 'ffmpeg'` at `transcribe_audio/cli.py:69`.**
- *Cause:* the Debian `ffmpeg` binary isn't in the image. A common way to get here is copying the appendix Dockerfile, whose `ARG` is `"build-essential curl"` (`README.md:179`).
- *Fix:* `ARG DEBIAN_PACKAGES="build-essential ffmpeg"` (`transcribe_audio/README.md:45`), then rebuild.

**G9: `AttributeError: module 'ffmpeg' has no attribute 'input'` or `ModuleNotFoundError: No module named 'ffmpeg'`.**
- *Cause:* you ran `uv add ffmpeg` or `uv add python-ffmpeg` (different PyPI projects), or forgot the package.
- *Fix:* `uv add ffmpeg-python` (`transcribe_audio/README.md:108`).

**G10: `ModuleNotFoundError: No module named 'google'` on the second day.**
- *Cause:* you ran `uv add` in an earlier `--rm` container but never rebuilt, so the packages lived in that container's writable layer (codecast:180; verified: the next container's venv was empty again).
- *Fix:* `docker build -t <name> .` again. The new `pyproject.toml`/`uv.lock` on the host are picked up by `COPY` + `uv sync`.

**G11: Re-running does nothing.**
- *Symptom:* `--transcribe`, `--generate` or `--translate` prints nothing new; `--synthesis` prints nothing.
- *Cause:* skip-if-exists logic. Local outputs persist on the host across container runs (`transcribe_audio/cli.py:61-62`, `generate_text/cli.py:57-58`, `translate_text/cli.py:52-53`), and synthesis skips if the **GCS** object exists (`synthesis_audio_en/cli.py:69`).
- *Fix:* delete the local output file (or the GCS object for synthesis) to force a redo.

**G12: Quota or model errors on the shared project.**
- *Symptoms and causes:*
  - `429 RESOURCE_EXHAUSTED` from Gemini, Speech or TTS: the whole class shares `ac215-project`'s quotas during lecture.
  - `404 … Publisher Model ... was not found`: the default model has been retired or renamed.
- *Fix:* retry after a minute. For a model error, start the container with `-e GEMINI_MODEL=<current model id>` (`generate_text/cli.py:73`).

**G13: Docker Hub login leaks your token into shell history.**
- *Cause:* `docker login -u <USER NAME> -p <ACCESS TOKEN>` (`transcribe_audio/README.md:138`). Docker itself warns that `--password` on the CLI is insecure.
- *Fix:* `docker login -u <USER NAME>` and paste the token at the prompt, or `echo "$TOKEN" | docker login -u <USER NAME> --password-stdin`.

**G14: Your Dockerfiles and `pyproject.toml` "disappear" when you commit to your own repo.**
- *Cause:* the component `.gitignore` files ignore them (`transcribe_audio/.gitignore:4-7`, and the same lines in `synthesis_audio_en`, `translate_text` and `synthesis_audio`).
- *Fix:* `git add -f transcribe_audio/Dockerfile transcribe_audio/pyproject.toml transcribe_audio/uv.lock`, or remove those lines in your fork. Never remove `/secrets`.

**G15: The run command is mangled on Windows.**
- *Symptoms:* `the input device is not a TTY`, or a path split at a space.
- *Fix:* use Git BASH, quote `"$(pwd)"`, and prefix `winpty` (`README.md:230-236`). If `/app` still looks empty, Git BASH may have rewritten the path. Prefixing the command with `MSYS_NO_PATHCONV=1` is a commonly used workaround (not from the README; I haven't verified it).

**G16: `docker run … transcribe_audio python cli.py -d` fails instead of running the CLI.**
- *Symptom (verified):* `/usr/local/bin/python: /usr/local/bin/python: cannot execute binary file`, exit code 126.
- *Cause:* `ENTRYPOINT ["/bin/bash"]` (`README.md:222`), so the extra words become `bash python cli.py -d`, and bash looks `python` up on `PATH` (the image's `/usr/local/bin/python`, not the venv's, since nothing was activated) and tries to read it as a shell script.
- *Fix:* `docker run --rm -v "$(pwd):/app" transcribe_audio -c "source /home/app/.venv/bin/activate && python cli.py -d"`.

**G17: `ffmpeg.Error` on a file that isn't audio.**
- *Cause:* `transcribe()` processes **every** file in `input_audios/` (`transcribe_audio/cli.py:54-56`). On a Mac, opening the bind-mounted folder in Finder can create `.DS_Store` there.
- *Fix:* delete stray files, or re-run `--download`, which wipes the folder first (`transcribe_audio/cli.py:33`).

**G18: Ports and stale containers.** These don't apply here: nothing is published with `-p`, and `--rm` removes every container on exit. If `docker ps -a` shows leftovers, they came from runs without `--rm`. Remove them with `docker rm <id>`.

**G19: "The venv isn't active" because the prompt has no `(transcribe-audio)` prefix.**
- *Symptom:* the container prompt is just `app@<id>:/app$` (verified).
- *Cause:* `exec bash` starts a new interactive shell that reads `/home/app/.bashrc`, which resets `PS1`; the exported `VIRTUAL_ENV`/`PATH` survive.
- *Fix:* nothing to fix. Check with `which python` (`/home/app/.venv/bin/python`) or `echo $VIRTUAL_ENV`.

**G20: A transcript that says `None`.**
- *Cause:* `text = "None"` (`transcribe_audio/cli.py:80`) is written unchanged when Speech-to-Text returns no results (`:84`, `:95-96`), e.g. silence or wrong audio. The file then counts as done (skip-if-exists, `:61-62`) and `--upload` ships it to stage B.
- *Fix:* `cat` the `.txt` before uploading; delete it and re-run `--transcribe` if it says `None`.

**G21: `docker build` fails at `RUN uv sync` with ``error: No `pyproject.toml` found in current directory or any parent directory``.**
- *Cause:* you skipped `uv init --bare` (step 3; verified by building without the file), or ran it in the wrong folder.
- *Fix:* run `uv init --bare` in the component folder (fix `requires-python`, G3) and rebuild.

---

## 7. Where this sits in the course

**Before: L02, Containers I** (`dlops-io/simple-translate` main @ `62f821bfe09fc1c2ecb0f14354b1f205777c0efa`; `tutorials_demo.md:31-42`). You containerised one tiny CLI with a **given** `Dockerfile.txt`, ran it with no mounts and no secrets, pushed it to Docker Hub and pulled it onto a VM. L01 before that covered venvs/uv and VMs.

**What L03 adds, concretely** (L02's `simple-translate/Dockerfile.txt` vs L03's Dockerfile at `README.md:175-225`):

| Aspect | L02 simple-translate | L03 mega-pipeline (`main`) |
|---|---|---|
| Who writes the Dockerfile | given (`Dockerfile.txt`) | **you**, from the README pieces |
| Number of images | 1 | **5**, one per pipeline stage |
| OS packages | none installed (`Dockerfile.txt:14-19` only updates/upgrades) | `ARG DEBIAN_PACKAGES` + `apt-get install` (`ffmpeg` for A) |
| User | root | non-root `app`, uid 1000 (`README.md:208,213`) |
| Code location / venv | `COPY . ./` with no `WORKDIR` (the default cwd is `/`), venv `.venv` beside the code (`Dockerfile.txt:22-29`) | `WORKDIR /app`; venv at `/home/app/.venv` via `UV_PROJECT_ENVIRONMENT` |
| Run command | `docker run --rm --name $IMAGE_NAME -ti $IMAGE_NAME` (`simple-translate/docker-shell.sh:15`) | `docker run --rm -ti -v "$(pwd):/app" <name>`, a **bind mount** for live code |
| Dependencies | `pyproject.toml` given | `uv init --bare` + `uv add` *inside* the container, then rebuild |
| Cloud | none (unofficial translate endpoint) | GCS + 4 managed Google AI APIs + service-account auth (ADC) |
| Data flow | stdin/args → stdout | containers hand off through a shared bucket |

**What comes next: L04, Containers II-b** (`tutorials_demo.md:56-67`). The same repo, branch `flexible-workflow` (`git diff --stat main origin/flexible-workflow` → `42 files changed, 4227 insertions(+), 625 deletions(-)`), plus the `port_toy` Docker Compose app. The meaningful changes:
- **Your own resources.** You create your own bucket and service account with Storage Admin, "Agent Platform User" (`roles/aiplatform.user`), Cloud Speech Client and Cloud Translation API User, and you enable the five APIs yourself (`flexible-workflow:README.md:169-198`).
- **Blank identifiers.** `gcp_project`, `bucket_name` and `group_name` are blank and must be set, with an assert (`flexible-workflow:README.md:127-134`).
- **Dockerfiles provided, on Python 3.14.** Each component ships a Dockerfile on `FROM python:3.14-slim-bookworm` (`flexible-workflow:README.md:325`) plus a committed `pyproject.toml`/`uv.lock`.
- **The key moves out of the repo.** It is no longer baked into an `ENV` (`:372`). It lives in `../secrets/` beside the repo, mounted at `/secrets` by `docker-shell.sh`.
- **`docker-shell.sh` with four modes** (`flexible-workflow:README.md:212-215`):
  ```bash
  ./docker-shell.sh          # build the image locally and run it (default)
  ./docker-shell.sh dev      # only build the local image
  ./docker-shell.sh run      # run from a prebuilt image (falls back to DockerHub)
  ./docker-shell.sh prod     # build multi-arch (amd64 + arm64) and push to DockerHub
  ```

After that, Milestone 2 asks your project to "Containerize each component" and make "The pipeline … runnable with one command (e.g., `docker compose up` or `make run`)" (`milestone2.md:46-48`). That is exactly the orchestration gap the mega-pipeline leaves open on purpose. The bucket-as-message-bus pattern also reappears in the data and ML-workflow lectures.

This is not a cheese-app version, but within this repo the branch history is:
- `pipenv` (2025-02, Pipenv);
- `simple` / `solution` (2025-09, uv + Python 3.12; secrets outside the repo; `assert group_name`; translate via the unofficial `googletrans`);
- `main` (2026-09, build-your-own Dockerfile; secrets inside each component; `google-cloud-translate` v2; `group_name="pavlos"` default; Gemini model via `GEMINI_MODEL`; multi-segment transcript fix);
- `flexible-workflow` (2026-09, L04).

`git diff --stat origin/solution main` → `49 files changed, 574 insertions(+), 3838 deletions(-)`. Most of the deletions are the solution's Dockerfiles, lock files and `docker-shell.sh` scripts, which `main` deliberately withholds.

---

## 8. Video plan (suggestion)

**Hook question (on screen over a schematic waveform):** *"Five programs that never send each other a single message, and yet together they turn a rough English recording about cheese into a French podcast. How do they cooperate?"* (The recording's length and content are not in the repo; the removed codecast says it is about halloumi, codecast:15.)

**Production constraints for this video:** no credentials exist in the capture environment, so every step after `docker run` that calls Google (`--download` … `--upload`, `--synthesis`) and the leaderboard can only be shown as the command plus what to look for (or the `--help`/`Args:` lines, which need no API call); there is no real final French audio to play. `mega-pipeline-bucket.png` is a console screenshot: redraw it as a schematic tagged `illustration`. Build, run, `uv init`, `uv add`, `--help`, G1, G3, G7 and G16 were all reproduced here and can be captured.

**Chapters** (≈ 34 min total; narration ≈ 4,000-4,300 words at the house voice's ~174 wpm, per `docs/AC215_SERIES.md`; typing, outputs and ponder pauses fill the rest):

1. **The content engine (3 min).** *Idea:* the pipeline is a DAG of single-purpose stages.
   - *Visual:* `mega-pipeline-flow.png` redrawn as five boxes; a halloumi token morphs mic → page → longer page → splits into a sound wave and a French page → sound wave.
   - *On screen:* `README.md:9-15`, and `tree -L 2` of the clone (an extra check, not in the README).
2. **The bucket is the message bus (3.5 min).** *Idea:* communication by naming contract; prefixes and `group_name` as namespaces.
   - *Visual:* a shelf of drawers labelled with the prefixes; each box reaches down to one drawer and up into another; zoom into `text_prompts/` and it splits into `group-01/ … group-20/`; a "pavlos" drawer flashes red when a box with the default name writes into it.
   - *On screen:* the prefix table (§1), `transcribe_audio/cli.py:108-112`, `generate_text/cli.py:42`.
   - **Pause-and-ponder 1:** "Look at the drawers each box reads and writes. Which two stages could run at the same time, and which one must wait for both?" (Answer: C and D both need only B. E needs D. C needs nothing of D.)
3. **Who is calling? Service accounts and ADC (3.5 min).** *Idea:* authentication vs authorisation; the env var points the library at the key.
   - *Visual:* the 3.6 animation (JSON → google.auth machine → expiring token → IAM padlock).
   - *On screen:* `README.md:90-106`; inside the container, `echo $GOOGLE_APPLICATION_CREDENTIALS`.
4. **Write the Dockerfile, layer by layer (6 min).** *Idea:* every line earns its place; layers and the cache.
   - *Visual:* slabs stacking as each line is typed (3.3 animation); the `ffmpeg` slab is coloured only for stage A; then edit `cli.py` and watch the `uv sync` slab dissolve.
   - *On screen:* the assembled Dockerfile from §4 step 4, typed live; `uv init --bare` and `cat pyproject.toml` with the `requires-python` fix highlighted; `docker build -t transcribe_audio .`
   - **Pause-and-ponder 2:** "You change only `group_name` in `cli.py` and rebuild. Which steps come from cache and which re-run? Why is that wasteful?" (Answer: `FROM`, `RUN apt…` and `WORKDIR` are cached; `COPY` and `uv sync` re-run because `COPY . ./` precedes `uv sync`.)
5. **Run it: the window into your laptop (4 min).** *Idea:* image vs container vs bind mount; why the venv lives in `/home/app/.venv`.
   - *Visual:* the 3.4 animation (the blue host sheet slides over `/app`; the `.venv` box sits outside).
   - *On screen:* `docker run --rm -ti -v "$(pwd):/app" transcribe_audio`; the prompt `app@…:/app$` and `which python` → `/home/app/.venv/bin/python` (G19); `ls`; edit `cli.py` in VS Code and `cat` it inside.
   - **Pause-and-ponder 3:** "Suppose the venv were at `/app/.venv`, as it was in L02. What would the container see after the mount?" (Answer: the host's folder, which has no `.venv` or has a macOS one, so the image's venv is hidden and imports fail.)
6. **The dependency loop (3 min).** *Idea:* `uv add` inside the container edits host files but installs into an ephemeral venv, so rebuild to bake.
   - *Visual:* package cubes (red, ephemeral) dropping into `.venv`; the `pyproject.toml` line glowing on the host side; "exit" evaporates the cubes; a rebuild re-materialises them in the image slab.
   - *On screen:* `uv add google-cloud-storage google-cloud-speech ffmpeg-python`, `cat pyproject.toml` on the host, `exit`, `docker build …`
7. **Stage A up close: transcribe (4 min).** *Idea:* download → ffmpeg MP3→FLAC → long-running Speech request → join the segments → upload.
   - *Visual:* an MP3 waveform squeezed through an "ffmpeg" funnel into a FLAC block with a header tag "sample rate" (the real rate is unknown, §10 Q2); a ticket stub (the LRO) with a 90 s timer; several transcript strips snapping together (the `c6bbc9b` fix).
   - *On screen:* `transcribe_audio/cli.py:29-43`, `:64-78`, `:84-90`; type `python cli.py -d`, `-t`, `-u` (no capture possible without the key: describe what to look for); the leaderboard as a schematic `illustration`.
8. **Stages B-E speed round (5 min).** *Idea:* the same recipe, with one new thing per stage.
   - *Visual:* split screen per stage showing the Dockerfile diff (only the `ARG` line changes) and the `uv add` line. For C/E, the 3.7 animation: the TTS factory ships the crate directly into the drawer, hence no `--upload`.
   - *On screen:* `generate_text/cli.py:64-78` (with `-e GEMINI_MODEL=…`), `synthesis_audio_en/cli.py:77-90`, `translate_text/cli.py:58-64`; the `generate_text` `requires-python = ">=3.14"` erratum and the `uv init --bare` "already initialized" error. (No final audio exists to play.)
9. **What goes wrong, and where we go next (3 min).** *Idea:* `.gitignore` ≠ `.dockerignore`; relative credential paths; the arm64 vs amd64 trap; preview of `flexible-workflow`.
   - *Visual:* a moving box (the image) with the key inside, a stamp "PUSHED TO DOCKER HUB", then a rewind; the secrets folder slides outside the repo and becomes a `-v …:/secrets` tube.
   - *On screen:* `docker run --rm --entrypoint ls transcribe_audio -la /app/secrets`, a `.dockerignore` with `secrets/`, `origin/solution:transcribe_audio/docker-shell.sh:95-100`.

**Recap questions (end card):**
1. Which bucket prefix does `translate_text` read from, and which stage wrote it?
2. Why does `-v "$(pwd):/app"` not hide the Python packages, and what would break if `UV_PROJECT_ENVIRONMENT` were removed?
3. After `uv add` inside a `--rm` container, where do the changes survive and where are they lost? What makes them permanent?
4. Name the exact env var the Google libraries read to find the key, and say why its value only works from `/app`.
5. Why do the two synthesis stages have no `--upload` step?
6. You pushed your `transcribe_audio` image to Docker Hub. What secret might it contain, and how do you prevent that next time?

**Target length:** ~34 minutes.

---

## 9. Exercises

**E1 (hands-on, predict then run): switch the LLM.** Start stage B with `docker run --rm -ti -e GEMINI_MODEL=gemini-2.5-flash -v "$(pwd):/app" generate_text` and run `python cli.py -g`. Predict what happens if `text_paragraphs/<group>/input-….txt` already exists from your first run.
> *Answer:* nothing is generated. `generate()` skips any input whose output file exists (`generate_text/cli.py:57-58`), and that file lives on your host through the bind mount, so it survived the old container. Delete `text_paragraphs/<group>/*.txt` on the host first. Then the prompt prints, Gemini (`gemini-2.5-flash`, read at `generate_text/cli.py:73`) answers, and `-u` overwrites the objects in the bucket. Downstream, C won't regenerate English audio unless you also delete `text_audios/<group>/…mp3` in GCS (`synthesis_audio_en/cli.py:69`).

**E2 (hands-on): make it Spanish.** Change stage D to Spanish and stage E to a Spanish voice. Which lines change, and what must you delete for the new language to actually be produced?
> *Answer:* `translate_text/cli.py:61` → `target_language="es"`; `synthesis_audio/cli.py:47-48` → `language_code = "es-ES"` and a Spanish voice name from the TTS voice list (e.g. an `es-ES-Standard-…` voice). You must delete:
> - the local `translate_text/text_translated/<group>/*.txt`, otherwise translate skips (`translate_text/cli.py:52-53`). The upload then overwrites the French text in GCS.
> - the GCS objects `output_audios/<group>/*.mp3`, otherwise synthesis skips (`synthesis_audio/cli.py:68`).
>
> No rebuild is needed: the code is bind-mounted and no dependencies changed.

**E3 (debugging): credentials vanish.** Inside the `translate_text` container you run `cd /tmp && python /app/cli.py --help` and get `google.auth.exceptions.DefaultCredentialsError: File secrets/mega-pipeline.json was not found.` Why, even though `--help` makes no API call?
> *Answer:* two things combine:
> 1. `GOOGLE_APPLICATION_CREDENTIALS=secrets/mega-pipeline.json` is relative (`README.md:195`), so from `/tmp` it points at `/tmp/secrets/…`, which doesn't exist (`google/auth/_default.py:176-179`).
> 2. `translate.Client()` runs at **import** (`translate_text/cli.py:20`) and calls `google.auth.default()` in its constructor (`google/cloud/client/__init__.py:218`), before argparse ever sees `--help`.
>
> *Fix:* `cd /app`, or use an absolute path like `/secrets/mega-pipeline.json` with a mount, as `solution`'s `docker-shell.sh` does.

**E4 (debugging): non-interactive run.** You want to run stage A in one shot from the host: `docker run --rm -v "$(pwd):/app" transcribe_audio python cli.py -d -t -u`. It errors immediately. Explain, and give a working command.
> *Answer:* the image's `ENTRYPOINT` is `["/bin/bash"]` (`README.md:222`). Arguments after the image name replace `CMD`, so the container runs `/bin/bash python cli.py -d -t -u`. Bash treats `python` as a *script file* to read, finds the binary on `PATH`, and refuses: `/usr/local/bin/python: /usr/local/bin/python: cannot execute binary file`, exit 126 (verified). Working command (both forms verified to start the venv's Python):
> `docker run --rm -v "$(pwd):/app" transcribe_audio -c "source /home/app/.venv/bin/activate && python cli.py -d -t -u"`
> Alternatively, `docker run --rm -v "$(pwd):/app" --entrypoint /home/app/.venv/bin/python transcribe_audio cli.py -d -t -u`. `-ti` is unnecessary when nothing is interactive.

**E5 (debugging): yesterday it worked.** Yesterday `python cli.py -d` worked in `synthesis_audio_en`. Today, after `docker run …`, you get `ModuleNotFoundError: No module named 'google'`. `pyproject.toml` on your host lists the packages. What happened, and what's the one-command fix?
> *Answer:* yesterday's `uv add` installed into `/home/app/.venv` inside a `--rm` container, and that layer was deleted on exit. Only `pyproject.toml`/`uv.lock` (on the bind-mounted host folder) persisted (`transcribe_audio/README.md:110`; codecast:180). The image was never rebuilt, so its venv is still empty. Fix: `docker build -t synthesis_audio_en .`, after which `COPY` brings the new `pyproject.toml`/`uv.lock` and `uv sync` installs them.

**E6 (conceptual): where's the venv?** Why does the Dockerfile set `UV_PROJECT_ENVIRONMENT=/home/app/.venv` instead of leaving uv's default `.venv` inside `/app`? Describe precisely what you'd see on a Mac if you removed that line.
> *Answer:* uv's default puts the venv at `/app/.venv`. Removing only the `ENV` line breaks the start command at once: `CMD` still runs `source /home/app/.venv/bin/activate`, which no longer exists, so `&& exec bash` never runs and the container exits immediately with an error, mount or no mount. Suppose you also change `CMD` to activate `/app/.venv` (as L02 did with `.venv`). At run time `-v "$(pwd):/app"` replaces the whole `/app` view with the host folder, so the image's `/app/.venv` becomes invisible:
> - If the host folder has no `.venv`, the `source` fails the same way and the container exits.
> - If you once ran uv on the Mac in that folder, the container sees a **macOS** venv whose `bin/python` points at a Mac interpreter path that doesn't exist in Linux, so nothing runs.
>
> Putting the venv outside the mount point keeps the image's environment and the host's code independent (3.4).

**E7 (security): audit your image.** Without the bind mount, list what's inside your built `transcribe_audio` image's `/app/secrets`. What do you find, why, and what are three fixes, from quickest to best?
> *Answer:* `docker run --rm --entrypoint ls transcribe_audio -la /app/secrets` shows `mega-pipeline.json`. `COPY --chown=app:app . ./` copied the entire build context, and Docker doesn't read `.gitignore`. Fixes:
> 1. Add `.dockerignore` with `secrets/` and rebuild.
> 2. Never push images built from a folder that contains secrets.
> 3. Keep `secrets/` outside the repo and mount it at run time with an absolute `GOOGLE_APPLICATION_CREDENTIALS` (`origin/solution:transcribe_audio/docker-shell.sh:9-10,96-99`; `flexible-workflow:README.md:105-119`).
>
> If an image with the key was ever pushed, the key must be rotated.

**E8 (conceptual): the contract.** Stage A transcribes a file whose name is `podcast.mp3` (no `input-` prefix). Trace exactly how far it gets through the pipeline.
> *Answer:*
> 1. `--download` fetches it, since `list_blobs(prefix="input_audios/")` takes everything (`transcribe_audio/cli.py:39`).
> 2. `--transcribe` produces `text_prompts/<group>/podcast.txt` (`:57-59`).
> 3. `--upload` globs only `input-*.txt` (`:108`), so **the file is never uploaded**. Stage B's `match_glob` also requires `input-*.txt` (`generate_text/cli.py:42`).
>
> The pipeline silently stops after A's local output. Naming conventions are part of the interface.

---

## 10. Errata and open questions

**Errata** (wrong, outdated or inconsistent, with evidence):

- **E1. `generate_text` ships a `pyproject.toml` that contradicts the tutorial.**
  - `generate_text/pyproject.toml:4` has `requires-python = ">=3.14"`, while the README bases the image on `python:3.12-slim-bookworm` (`generate_text/README.md:41`).
  - The README also says to run `uv init --bare` there (`generate_text/README.md:20-24`), which errors because the file exists (verified with uv 0.11.32 on a copy). The README's line 24 even promises `--bare` gives "no sample `main.py`", next to a committed `main.py`.
  - A stray `generate_text/main.py` (`print("Hello from generate-text!")`) is a leftover from a non-bare `uv init` (commit `c8cb0f7`).
- **E2. `uv init --bare` makes `requires-python` depend on the host.** No component README warns that it writes `>=<host Python>` (verified: `>=3.13` on a 3.13 host). With anything above 3.12, `uv sync` in the 3.12 image silently downloads the newest CPython (3.15.0 when checked) and builds the venv on it; it fails only when Python downloads are disabled (G3, both verified). Last year's README pinned `requires-python = ">=3.12,<3.13"` (`origin/solution:transcribe_audio/README.md:36`), and the instructor's run-sheet flags it (codecast:152, which wrongly predicts a build failure), but the published `main` READMEs dropped both.
- **E3. "Keep ffmpeg" vs the given `ARG`.** `synthesis_audio_en/README.md:38` ("keep `ffmpeg` in the system packages") and `synthesis_audio/README.md:38` ("Audio again, so keep `ffmpeg`") conflict with the `ARG DEBIAN_PACKAGES="build-essential"` given a few lines later (`:45` in both). Neither synthesis `cli.py` imports ffmpeg, and last year's solution Dockerfiles for both use `build-essential` only. The prose is wrong; the `ARG` is right. The removed codecast repeats the prose claim (codecast:117,236,249).
- **E4. `cli_11.py` is referenced in the wrong folder.** `synthesis_audio_en/README.md:132-135` tells you to use `cli_11.py`, but that file exists only in `synthesis_audio/`.
- **E5. Two different Canvas links for the key.** `README.md:99` links `files/25687801` (updated in `07e14b9`, 2026-09-10), while all five component READMEs still link `files/23163432` (e.g. `transcribe_audio/README.md:17`), which is probably last year's file.
- **E6. Wrong `--help` description.** `synthesis_audio/cli.py:105` says `"Transcribe audio file to text"`; the README shows "Synthesis audio from text" (`synthesis_audio/README.md:118`).
- **E7. `.mp3` names, WAV contents.** Both synthesis stages request `AudioEncoding.LINEAR16` (`synthesis_audio_en/cli.py:73`, `synthesis_audio/cli.py:72`) but name the objects `….mp3` (`:66` / `:65`). Per the TTS enum, "Audio content returned as LINEAR16 also contains a WAV header" (`texttospeech_v1/types/cloud_tts.py:90-93`), so the files are most likely WAV with an `.mp3` extension (not checked on a real output: no bucket access). Most players sniff the header, but tools that trust the extension may not. Whether Long Audio accepts `MP3` is open (Q3).
- **E8. Dead idempotency check.** `synthesis_audio_en/cli.py:55-58` and `synthesis_audio/cli.py:54-57` test a local `…/<uuid>.mp3` that the code never writes. The real check is `blob.exists()` (`:69` / `:68`).
- **E9. Transcript segments are glued with `""`.** `transcribe_audio/cli.py:90` concatenates segments with no separator. If the API's segment transcripts don't start with a space, words at segment boundaries run together ("…cheeseThe…"). I could not confirm whether segments carry a leading space; `" ".join` would be safer. The LLM stage likely papers over it.
- **E10. Outdated mentions of OpenAI/GPT2.** `generate_text/README.md:7` says "(or OpenAI)" and `:130` says "Gemini or GPT2 API", but the code only calls Gemini on Vertex AI (`generate_text/cli.py:23-25,75-77`).
- **E11. Secret leaks into images.** `README.md:103-106` presents `.gitignore` as the protection for the key, but the build copies it into the image (`README.md:217`, no `.dockerignore`), and the optional Docker Hub push (`transcribe_audio/README.md:136-140`) would publish it. This is the most consequential omission.
- **E12. Student work is git-ignored.** Component `.gitignore` files ignore `Dockerfile`, `pyproject.toml`, `uv.lock` and `docker-shell.sh` (`transcribe_audio/.gitignore:4-7`, etc.). Nothing in the README mentions it, so students who commit their work will silently miss their Dockerfiles. `generate_text/` has no `.gitignore` at all, which is inconsistent with the other four.
- **E13. No build command is given.** The component READMEs never give it (`transcribe_audio/README.md:95` only says "Build your docker image and give your image the name `transcribe_audio`"). The command `docker build -t transcribe_audio .` appears only in the removed codecast (codecast:168).
- **E14. `group_name` has no guard.** It defaults to `"pavlos"` with no assert (`transcribe_audio/cli.py:21` and peers), whereas last year's `solution` asserted it was changed and `flexible-workflow` re-adds an assert (`flexible-workflow:README.md:134`). The README only warns (`README.md:124`).
- **E15. "For each paragraph" is inaccurate.** `README.md:78` says `text_audios/` holds "synthesized English audio clips for each paragraph", but the code synthesises one audio file per input text file (`synthesis_audio_en/cli.py:52-66`).
- **E16. Leaderboard link scheme is inconsistent.** It is `http://` in `README.md:54` and most component READMEs, but `https://` in `translate_text/README.md:132`.
- **E17. Bucket screenshot is incomplete.** `mega-pipeline-bucket.png` shows only `input_audios/`, `text_audios/`, `text_paragraphs/`, `text_prompts/` and `text_translated/`. `output_audios/` and `output_audios_pp/` (listed at `README.md:79-80`) are absent, presumably because the screenshot predates any synthesis run.
- **E18. Ambiguous flow diagram.** In `mega-pipeline-flow.png`, the green line that links the English "Synthesise Audio" box (step 4) to the bucket is drawn straight through the "Translate Text" box (step 5), ending in an arrowhead under box 4, so it reads as "Translate → Synthesise (EN)". The code reads `text_paragraphs/` (`synthesis_audio_en/cli.py:39`), i.e. Generate's output; only the small arrow left of box 4 (from the Generate side) is right.
- **E19. Course-site inconsistency (context).** `tutorials_demo.md:56` calls Lecture 4 "Containers II-b" (flexible-workflow + port_toy), while `_modules/week-03.md:5-7` lists Lecture 4 on Sep 15 as "LLM - RAGs".
- **E20. The prompt the run-sheet promises isn't what you get.** The codecast (codecast:171) says "notice the prompt changed"; it does change, to `app@<id>:/app$`, but without the venv's `(transcribe-audio)` prefix, because `exec bash` re-reads `~/.bashrc` (verified, G19). Not a README error, but viewers will look for the prefix.

**Open questions** (couldn't be determined from the sources):
- **Q1.** What the leaderboard reads and what counts as "success" for a stage. Its code isn't in this repo (the root `.gitignore:11-13` ignores `/api-service`, `/deployment` and `/frontend`, which suggests it lives in a staff-only copy). Presumably it lists `<prefix>/<group>/` objects.
- **Q2.** The size, length, channel count and exact names of the files in `input_audios/` (no bucket access). This matters because:
  - inline `RecognitionAudio(content=…)` is subject to Speech-to-Text content limits (the API docstring points to https://cloud.google.com/speech-to-text/quotas#content);
  - `operation.result(timeout=90)` may be too short for long audio;
  - stereo FLAC may need `audio_channel_count` or ffmpeg `ac=1`.

  The `c6bbc9b` commit message says the audio is long enough to be split into several segments.
- **Q3.** Whether Text-to-Speech Long Audio accepts `MP3` output (the code uses `LINEAR16`; the client library's docstring doesn't say).
- **Q4.** Which IAM roles the shared Canvas key actually has (beyond writing every prefix, which the tutorial relies on), which project it belongs to, and whether staff rotate it after the lecture.
- **Q5.** Whether a student's own ElevenLabs API key can use voice ID `TG3keNw5JZvsEiTtWt7t` (`synthesis_audio/cli_11.py:28`). Voices are usually owned per account or shared through a library, and the README doesn't say how it's shared.
- **Q6.** What the Ed lesson adds (slides, recordings, extra instructions). I could not access Ed.
- **Q7.** Whether the AWS track (`mega-pipeline-aws`) differs materially. It was not examined.
