# AC215 · Lecture 2 — Containers I: one image, from laptop to VM

A follow-along walkthrough of the Lecture 2 tutorial of Harvard's **AC215 (MLOps & LLMOps, Fall
2026)**: [dlops-io/simple-translate](https://github.com/dlops-io/simple-translate) (`main` @
[`62f821b`](https://github.com/dlops-io/simple-translate/tree/62f821bfe09fc1c2ecb0f14354b1f205777c0efa)),
sections *Developing App using Containers* (with its *Pushing Docker Image to Docker Hub* part)
and *Running App on VM using Docker*: the same app as Lecture 1, now written into a Dockerfile,
built and run on your laptop, pushed to Docker Hub and run on a VM that has only Docker.

Watch it with the README open, your own clone on your **laptop**, Docker Desktop running (Tutorial
0), a free Docker Hub account and, for the last part, a VM of your own. The trackers top left show
the README step (A on the laptop, B on Docker Hub, C on the VM); pause at every `▶ your turn` to run
the command; a gray `extra` tag marks a check that isn't in the README. The recording has no Docker
Hub account: the login and the pushes that succeed go to a small local registry tagged
`stand-in`, and the real Docker Hub push shows the refusal you get without an account. Series format:
[`docs/AC215_SERIES.md`](../../docs/AC215_SERIES.md). Study guide with every command:
[MLOps_Learning · guides/L02-containers-1.md](https://github.com/JunyiZhou-Conny/MLOps_Learning/blob/main/guides/L02-containers-1.md).

English narration; Chinese and bilingual subtitles (中文字幕说明见 [`i18n/zh/README.md`](i18n/zh/README.md)).

| file | what it is |
| --- | --- |
| `output/ac215-l02-containers-1.zh-en.mp4` | **the copy to watch**: 1080p60, English narration, bilingual subtitles (Chinese above, English below) burned in, DURATION_FULL. The only video file committed |
| `output/ac215-l02-containers-1.mp4` | the same video without burned-in subtitles; load any `.srt` below in your player. Not committed: rebuild it with `--no-render` (see Rebuild) |
| `output/ac215-l02-containers-1_part1.mp4` | part 1, DURATION_P1: write a Dockerfile, build and run the image (S01–S09). Not committed: rebuilt with `--no-render` |
| `output/ac215-l02-containers-1_part2.mp4` | part 2, DURATION_P2: layers, cache, Docker Hub and a VM (S10–S16). Not committed: rebuilt with `--no-render` |
| `output/ac215-l02-containers-1.srt` | English subtitles (each part has its own `.srt`, `.zh.srt`, `.zh-en.srt` / `.ass`) |
| `output/ac215-l02-containers-1.zh.srt` | Chinese subtitles (on the English timing) |
| `output/ac215-l02-containers-1.zh-en.srt` / `.zh-en.ass` | bilingual subtitles |
| `output/chapters.txt`, `chapters_part1.txt`, `chapters_part2.txt` | chapter timestamps |
| `output/transcript.md` | the full narration by chapter |
| `exercises.md` | do these after watching: the five test-yourself questions, hands-on predict-then-run tasks (including the cache-friendly Dockerfile the video promises), debugging, and think questions, with answers |
| `digest.md` | the tutorial digest: every step, a code tour with `path:line`, gotchas, errata |
| `assets/terminal/` | the **real** terminal sessions every terminal panel prints from (a fresh Docker Engine 29.8.2 standing in for the laptop, fresh Debian 12 and 13 containers standing in for the VM, 2026-10-13); provenance in [`ASSETS.md`](ASSETS.md) |
| `assets/source/` | the tutorial files the code panels quote, unchanged at the pinned commit |
| `BRIEF.md`, `script.md`, `scenes/` | the design, the narration (SAY) + visual plan (SHOW), and the Manim source |
| `i18n/zh/` | the Chinese subtitle text: glossary and sentence-aligned translation |

## Chapters

CHAPTERS

## What you'll learn

Five *pause and ponder* moments ask you to predict before the video shows you: whether
`python cli.py` runs once uv is installed and the code is copied in, what `uv sync` does in an image
whose Python is 3.12 when `pyproject.toml` asks for 3.13 or newer, what command line
`docker run … simple-translate python cli.py` really runs, which build steps run again after you
change one word in `cli.py`, and whether an image built on an M-series Mac runs on an ordinary
Intel/AMD VM. Five test-yourself questions close the video (answers in `exercises.md`).

**Part 1 · write a Dockerfile, build and run the image**

1. **One command on a fresh VM** — a VM with only Docker pulls an image in seven layers and runs
   the app; the recipe says Python 3.12, yet the container reports 3.14.7 (solved twice later);
   the README's four rungs, of which Lecture 1 climbed two; what you need today.
2. **Image, layer, container, registry** — an image is a stack of read-only layers plus a config
   card; RUN and COPY add a layer, CMD only writes on the card; a container is the same layers plus
   a thin writable layer and one main process, and `--rm` deletes it; image = class, container =
   instance; a registry stores images by name, a tag points at one image; containers share one
   Linux kernel, and Docker Desktop brings a hidden Linux VM on a Mac or Windows.
3. **A clean slate, and the clone** — `docker container ls`, `docker system prune` (of the
   images, it removes only dangling ones: named ones survive; `-a` removes every unused image),
   `docker image ls`; clone on your laptop, not on last lecture's VM; the repo has
   `Dockerfile.txt` but no `Dockerfile` and no `uv.lock`, so the build fails until you write one.
4. **Dockerfile step 1: FROM** — create `Dockerfile` (that exact name); `python:3.12-slim-bookworm`
   decoded; the build command's parts (`-t` the name, `-f` the recipe, the final `.` the build
   context); the full log vs the compact view, and `desktop-linux` on Docker Desktop; four base
   layers; the inherited `CMD ["python3"]` gives a Python prompt; the repo's `.gitignore` hides your
   Dockerfile (`git add -f`).
5. **Step 2: ENTRYPOINT** — `CACHED`, nothing downloaded, no new layer: config only; ENTRYPOINT
   is the program, CMD its default arguments, and setting an entrypoint resets the inherited CMD;
   reading the prompt `root@<container ID>:/` (no working directory set).
6. **Step 3: install uv, copy the code** — `RUN pip install uv` and `COPY . ./`; the build context
   travels to the builder whole, `.git` and your Dockerfile included, because there's no
   `.dockerignore`; pip's root warning; the packages aren't installed yet:
   `ModuleNotFoundError: No module named 'art'`.
7. **Step 4: uv sync, and two Pythons** — the 3.12 image doesn't meet `>=3.13`, so uv downloads
   CPython 3.15.0 (at the time of recording) and builds `/.venv`; `python cli.py` still fails
   because nothing activated the venv: PATH finds the base image's 3.12 first; `.venv/bin/python`
   and `source .venv/bin/activate` work; one image, two Pythons.
8. **Step 5: CMD, the solution, the build** — ENTRYPOINT + CMD join into one command line
   (`/bin/bash -c "source .venv/bin/activate && exec bash"`); `exec bash` keeps the venv's PATH; no
   `(app)` in the prompt, but `which python` and `$VIRTUAL_ENV` show the venv is active; what
   `Dockerfile.txt` adds (three ENV lines, one bigger RUN); `cp` it over yours and build: the
   compact view you'll see.
9. **Run it, translate, exit** — `docker run --rm -ti simple-translate` and the README's
   *Good morning* → *Buen día*; a runtime error means Google refused, not Docker; `exit` ends PID 1,
   `--rm` deletes the container; `-i` your keyboard, `-t` a terminal; words after the image name
   replace CMD only: `/bin/bash python cli.py`, exit 126, and the `-c` form that works;
   `docker-shell.sh`.

**Part 2 · layers, cache, Docker Hub and a VM**

10. **What's inside the image** — `docker image ls` (518MB on disk, 144MB of compressed content,
    at the time of recording); `docker history` read bottom-up is the Dockerfile top-down, with
    0B config rows; two Pythons inside; `ls -a /` shows `.git`, `.vscode` and your Dockerfile:
    add a `.dockerignore`.
11. **The layer cache** — a step is reused when its parent and its instruction are unchanged and,
    for COPY, the files' checksum matches; the first change reruns that step and every step after
    it; an edit to `cli.py` reruns COPY and `uv sync`; `git checkout` doesn't bring the cache back
    (`.git/index`), and the Dockerfile in the context explains part 1's reruns; the fix: copy what
    `uv sync` needs first, the rest after, plus a `.dockerignore`.
12. **Tag and push** — an access token with read and write access (a password, shown once);
    `docker login` without `-p`, so the token stays out of your shell history; `docker tag`: two
    names, one ID; reading `docker.io/<account>/<repository>:<tag>`; `push access denied` without
    an account, `Pushed` and a digest on the stand-in, `Layer already exists` the second time; a
    new Docker Hub repository is public.
13. **Platforms: arm64 vs amd64** — `uname -m` and the image's `Os/Architecture`; programs are
    machine code for one CPU; a tag can point at a menu of platforms (`imagetools inspect`); the
    instructor's image is amd64 only; `exec format error`; two fixes not in the README:
    `--platform=linux/amd64` (line 12 of `docker-shell.sh`) or buildx with `docker-build-push.sh`,
    then `docker buildx use default`.
14. **A VM with only Docker** — create the VM (an E2 machine is amd64; billed per second while it
    runs, its disk while it exists) and SSH in; `sudo apt install docker.io` fails on empty
    package lists until you run `sudo apt-get update`; `sudo docker --version` (Debian's own
    Docker); Docker runs right on the VM's kernel; why `sudo`: the Docker socket.
15. **One-command deploy** — `sudo docker run --rm -ti dlops/simple-translate` pulls seven layers,
    `python cli.py` translates, with no clone, no pip, no uv; why 3.14.7: built a month earlier
    with an older uv, and nothing in the recipe is pinned, so ship the image, not the recipe; the
    README runs the instructor's image, not yours; Docker Hub's `toomanyrequests` limit.
16. **Tear down, recap, and what's next** — `sudo docker ps -a`; delete the VM with its boot
    disk; your public repository and `docker system prune -a`; build on the laptop → push to a
    registry → run on a VM; five test-yourself questions; next, Containers II.

The tutorial's small mistakes are pointed out kindly, with the fix: building makes an *image*, not
a container (`README.md:173`, `:146`); `docker system prune` keeps named images, despite the
heading (`:113`); the repo's `.gitignore` hides your `Dockerfile` (`git add -f`); the 3.12 base
image doesn't meet `requires-python = ">=3.13"`, so every build downloads a second Python (start
from `python:3.13-slim-bookworm`); there's no `.dockerignore`, so `.git` ends up in a public image;
every "Build + Run after each step" reruns `uv sync`, because your Dockerfile is in the build
context (expected while learning; the reordered Dockerfile is in `exercises.md`); `docker login -p`
leaves the token in your shell history (type `docker login -u <USER NAME>` and paste it); CPU
platforms are never mentioned, and `docker-build-push.sh` would push both while the published image
is amd64 only; `sudo apt install docker.io` needs `sudo apt-get update` first; the last section
runs the instructor's `dlops/simple-translate`, not the image you pushed
(`<USER NAME>/simple-translate-ac215`, once built for amd64); and that published image lags the
repo: its `cli.py` predates `raise_exception=True`, so a refused request prints your input back.

## Rebuild

```bash
python -m explainer.build videos/ac215-l02-containers-1 -q l                          # fast draft
python -m explainer.build videos/ac215-l02-containers-1 --render-only --jobs 3        # 1080p60 scene renders
python -m explainer.build videos/ac215-l02-containers-1 --no-render --crf 27 --burn   # stitch: video, parts, subtitles, burned-in copy, chapters, transcript
python -m explainer.build videos/ac215-l02-containers-1 --subs-only                   # rewrite subtitles only
python -m explainer.i18n check videos/ac215-l02-containers-1 --lang zh                # Chinese text aligned with the English
```

The clean video and the two part cuts are not in Git: after a fresh clone, render the scenes once,
then the `--no-render` line rebuilds them (and the burned-in copy) from the scene renders.

Narration: Kokoro (`af_heart`, speed 0.9), generated locally.

*Course materials belong to the AC215 teaching staff (Harvard IACS); this video is made for study
with the instructor's permission. The cloud console, the Docker Hub pages and the editor are
schematic drawings (tagged `illustration`), not screenshots; no Docker Hub account, token or real
credential was used or shown.*
