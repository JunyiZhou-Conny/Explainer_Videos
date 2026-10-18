# AC215 · Lecture 4 — Containers II-b: build or pull, ports and Compose

A follow-along walkthrough of the Lecture 4 tutorials of Harvard's **AC215 (MLOps & LLMOps, Fall
2026)**, in two parts:

1. [dlops-io/mega-pipeline](https://github.com/dlops-io/mega-pipeline), branch `flexible-workflow` @
   [`cc67f3b`](https://github.com/dlops-io/mega-pipeline/tree/cc67f3b8fc471f4fe1afe73d03e89466bae7d485):
   the whole README (*Prerequisites*, *Get the Code*, *Where We Are, Where We're Going*, *The Five
   Components*, *Configure each `cli.py` before you run it*, *Connecting the Pipeline Components*,
   *GCS Bucket Details*, *Service Account & Secrets*, *How to Run a Component*, *Quick Reference —
   Running Each Component*, *Appendix*) and the five component READMEs it sends you to:
   `transcribe_audio`, `generate_text`, `synthesis_audio_en`, `translate_text`, `synthesis_audio`. The
   same five-container pipeline as Lecture 3, now with your own bucket and service account, committed
   Dockerfiles and one `docker-shell.sh` per component that builds locally or pulls from Docker Hub.
2. [dlops-io/port_toy](https://github.com/dlops-io/port_toy), branch `main` @
   [`d190c71`](https://github.com/dlops-io/port_toy/tree/d190c7122fc35cc1f7e15e467d2babdfc24b5c0c):
   the whole README (*Prerequisites*, *How the app works*, *Step 1: Set up the network by hand*,
   *Step 2: Check the ports*, *Step 3: Change the ports*, *Step 4: Run with Compose*, *Port and
   networking cheat sheet*, *Handy commands*): two containers that talk directly, on a network of
   their own, then the same app with Docker Compose.

A few panels quote two other branches of mega-pipeline for comparison, not followed: `main`
([`c6bbc9b`](https://github.com/dlops-io/mega-pipeline/tree/c6bbc9ba88984e1234b68ccf5cdf7c00f7e9accc),
the Lecture 3 tutorial) and `pipenv-flexible-workflow`
([`32fcdb7`](https://github.com/dlops-io/mega-pipeline/tree/32fcdb7aa3ffb3eaf3d09bdde123a02a42f2be12),
where the old `dlops/mega-pipeline-*` images on Docker Hub come from).

Watch it with both READMEs open and your own clones, `~/AC215/mega-pipeline` (on `flexible-workflow`)
and `~/AC215/port_toy`, Docker Desktop and git from Tutorial 0. Part 1 also needs a Google Cloud
project with billing and `gcloud` logged in; part 2 needs only Docker. The tracker top left shows the
README step; pause at every `▶ your turn` to run the command; a gray `extra` tag marks a check that
isn't in the README. The video was recorded on Linux (Docker Engine 29.8.2) **without a Google
account**: wherever the code calls Google, it shows the command, the real error a missing key gives,
and what to look for with your key. Series format:
[`docs/AC215_SERIES.md`](../../docs/AC215_SERIES.md). Study guide with every command:
[MLOps_Learning · guides/L04-containers-2b-flexible-workflow-ports.md](https://github.com/JunyiZhou-Conny/MLOps_Learning/blob/main/guides/L04-containers-2b-flexible-workflow-ports.md).

English narration; Chinese and bilingual subtitles (中文字幕说明见 [`i18n/zh/README.md`](i18n/zh/README.md)).

| file | what it is |
| --- | --- |
| `output/ac215-l04-flexible-workflow-ports.zh-en.mp4` | **the copy to watch**: 1080p60, English narration, bilingual subtitles (Chinese above, English below) burned in, 32:09 (1929.8 s), 122 MB. Published as a GitHub release asset: no MP4 is kept in Git ([`docs/PUBLISHING.md`](../../docs/PUBLISHING.md)) |
| `output/ac215-l04-flexible-workflow-ports.mp4` | the same video without burned-in subtitles; load any `.srt` below in your player. Not in Git: rebuild it with `--no-render` (see Rebuild) |
| `output/ac215-l04-flexible-workflow-ports_part1.mp4` | part 1, 18:40 (1120.2 s): the flexible workflow — your own cloud, one script, build or pull (S01–S09). Not in Git: rebuilt with `--no-render` |
| `output/ac215-l04-flexible-workflow-ports_part2.mp4` | part 2, 13:29 (809.7 s): port_toy — networks, ports and Compose (S10–S16). Not in Git: rebuilt with `--no-render` |
| `output/ac215-l04-flexible-workflow-ports.srt` | English subtitles (each part has its own `.srt`, `.zh.srt`, `.zh-en.srt` / `.ass`) |
| `output/ac215-l04-flexible-workflow-ports.zh.srt` | Chinese subtitles (on the English timing) |
| `output/ac215-l04-flexible-workflow-ports.zh-en.srt` / `.zh-en.ass` | bilingual subtitles |
| `output/chapters.txt`, `chapters_part1.txt`, `chapters_part2.txt` | chapter timestamps |
| `output/transcript.md` | the full narration by chapter |
| `exercises.md` | do these after watching: the five test-yourself questions, hands-on predict-then-run tasks (EXPOSE vs `-p`, Step 3 in Compose, a fast Ctrl+C, a package that never reached the image, getting your lecture 3 work back, what `prod` leaves behind), debugging and think questions, with answers |
| `digest.md` | the tutorial digest: every step, a code tour with `path:line`, gotchas, errata |
| `assets/terminal/` | the **real** terminal sessions every terminal panel prints from (a fresh Docker Engine 29.8.2 standing in for the laptop, the README's `gcloud` commands on a Cloud SDK with no account, 2026-10-14, no Google key); provenance in [`ASSETS.md`](ASSETS.md) |
| `assets/source/` | the tutorial files the code panels quote, unchanged at the pinned commits (and a few files from `main` and `pipenv-flexible-workflow`) |
| `BRIEF.md`, `script.md`, `scenes/` | the design, the narration (SAY) + visual plan (SHOW), and the Manim source |
| `i18n/zh/` | the Chinese subtitle text: glossary and sentence-aligned translation |

## Chapters

Paste-ready in `output/chapters.txt` (and `chapters_part1.txt`, `chapters_part2.txt` for the parts).

```
00:00 Build or pull? Whose localhost?
01:31 Same pipeline, built like a team
02:44 Get the code: clone, or switch branches
05:10 Your bucket and your three values
06:51 Three gates: account, role, API
09:09 docker-shell.sh: one script, two windows
11:26 Five components, five honest errors
14:06 dev, run, and a stale image
16:44 prod, a stowaway key, and clean-up
18:40 Two little computers, one network
20:09 Build, start, read the logs
21:43 Send a message: ports on the wire
22:56 Who can reach whom
25:31 Change the ports
27:44 Compose: the same app, declared
29:59 Edit, apply, tear down, recap
```

Part 1 uses the first nine lines as they are. Part 2 starts its clock at 0:00:

```
00:00 Two little computers, one network
01:29 Build, start, read the logs
03:03 Send a message: ports on the wire
04:16 Who can reach whom
06:51 Change the ports
09:04 Compose: the same app, declared
11:19 Edit, apply, tear down, recap
```

## What you'll learn

Five *pause and ponder* moments ask you to predict before the video shows you: where
`generate_text` fails when the key and the APIs are in place but the Agent Platform User role is
missing, whether a step that exited with status 0 called Gemini, which Python a teammate gets from
`./docker-shell.sh run` without ever building the image, what answers inside the gateway when you
ask `localhost` instead of `processor`, and which one setting fixes the processor's new port (and
whether any image needs rebuilding). Five test-yourself questions close the video (answers in
`exercises.md`).

**Part 1 · the flexible workflow — your own cloud, one script, build or pull**

1. **Build or pull? Whose localhost?** — `./docker-shell.sh run` on a laptop that never built
   `generate_text` pulls an image whose Python says 3.8.17 and whose Gemini library won't import,
   although the Dockerfile says 3.14; a server on port 9200 the laptop can't reach but another
   container reaches by name; how to follow along, and what a recording without a Google account
   shows.
2. **Same pipeline, built like a team** — what changed since lecture 3: your own bucket, your own
   service account with one key outside the repo, a committed Dockerfile with `pyproject.toml` and
   `uv.lock`, one `docker-shell.sh` per component; the stages still talk only through the bucket;
   two ways to get an image (build from the recipe in Git, or pull a published one from Docker Hub),
   and why a tag points at whatever was pushed last, not at your commit.
3. **Get the code: clone, or switch branches** — `git clone --branch flexible-workflow`; or switch
   your lecture 3 clone: `git fetch origin`, a checkout that refuses twice (an edited `cli.py`,
   untracked files), `git stash` for the first and `git stash -u` for the second; tracked, untracked
   and ignored files; your ignored lecture 3 Dockerfile, `pyproject.toml` and `uv.lock` replaced
   without a word; the old key still in `transcribe_audio/secrets/`: delete it.
4. **Your bucket and your three values** — `secrets/` beside the repo, never inside it; the project
   ID, bucket and group name in all five `cli.py` files, two of which ship the course's project and
   bucket and get past the `assert`; French as the target language; the bucket's prefixes and your
   group's sub-folders; creating the bucket in the console; an `input-<something>.mp3` recording,
   and why only `input-` names travel on.
5. **Three gates: account, role, API** — a service account and its JSON key, turned into a
   short-lived token; the three gates a call passes (who you are, what you may do, whether the API is
   on) and where each one fails; `mega-pipeline-sa` with four roles (Agent Platform User, not
   Vertex AI User; no role for Text-to-Speech); the key renamed to `mega-pipeline.json`, never
   committed or pasted; `gcloud config set project` with your ID, not the bracketed placeholder;
   `gcloud services enable` and the login step from Tutorial 0.
6. **docker-shell.sh: one script, two windows** — the script line by line: image name = container
   name, paths from `pwd` (run it from the component folder), the key's path inside the container,
   the Docker Hub account, four modes from one `case`; two bind mounts (`/app`, `/secrets`) and the
   environment variable as a signpost; the venv outside `/app`; the key never copied; the first
   build (system packages and writing the image take most of its 100 seconds; the image's Python
   3.14.8 satisfies `>=3.14`); inside as user `app`; `docker inspect` shows both mounts; `chmod +x`
   is harmless; `winpty` on Windows.
7. **Five components, five honest errors** — the Quick Reference in every container: without a key,
   `DefaultCredentialsError` at gate 1 and its usual causes; what to look for with your key;
   Speech-to-Text billed per minute, and a long recording cut to its first chunk; a `--generate`
   that exits with status 0 without calling Gemini; `GEMINI_MODEL`; an 8-second build from the cache;
   the `assert` doing its job on an unedited `cli.py`; `--help` that needs the key when the client is
   built at import; Text-to-Speech writing straight into the bucket; Spanish text for a French
   voice; the ElevenLabs bonus's key path.
8. **dev, run, and a stale image** — `dev` only builds; `uv add`, then `dev` to bake the package in;
   `run` uses any local image; without one it runs `dlops/mega-pipeline-*` from Docker Hub: a
   February 18, 2025 build from the `pipenv-flexible-workflow` branch, with Python 3.8.17, pipenv and
   root, your code in its environment, a root-owned `Pipfile` left in your folder, and the first
   puzzle solved; build locally, use `run` only for images your team pushed under its own account.
9. **prod, a stowaway key, and clean-up** — `prod` recreates a `multi-arch` builder, leaves it
   selected (`docker buildx use default` switches back), builds amd64 and arm64 and pushes both
   under one tag; `docker login` with an access token and your own `DOCKER_USERNAME`; why not to run
   `prod` yet: in a switched lecture 3 clone, `dev` copies the old key into the image, because
   `.gitignore` protects Git, not images; the fix (no `secrets/` in a component, a `.dockerignore`,
   delete any pushed key); clean-up for part 1, and what stays in the cloud: the bucket bills
   storage, and the key works, until you delete them.

**Part 2 · port_toy — networks, ports and Compose**

10. **Two little computers, one network** — a gateway and a processor that talk directly; each
    container as its own little computer, with its own `localhost` and ports; a user-defined network
    with a phone book for names; `docker run hello-world`, the clone (the README prints no command),
    `docker network create toynet`, `docker network ls`.
11. **Build, start, read the logs** — two near-identical Dockerfiles (`python -u` for unbuffered
    logs); the gateway's build reuses the processor's apt layer; the processor on `toynet` with
    `PORT=9200` and no `-p`; `-p 127.0.0.1:8090:9100` read as IP address, host port (a street door
    on your laptop) and container port (a room inside); `PROCESSOR_HOST` and `PROCESSOR_PORT`;
    `docker logs`.
12. **Send a message: ports on the wire** — the page on `localhost:8090` (curl stood in for the
    browser in the recording); its three port numbers; the temporary source port the gateway's
    operating system picks, seen unchanged by the processor, and new for every connection; the page
    reads 8090 from its own address bar, because the container can't know which door you gave it.
13. **Who can reach whom** — `docker ps` and its PORTS column (listening isn't published); without
    `127.0.0.1`, "port is already allocated", then `0.0.0.0`: every address; from the laptop, 8090
    answers and 9200 doesn't; from inside the gateway, `processor:9200` answers and `localhost:9200`
    doesn't: the second puzzle; `docker network inspect`, Docker's DNS at `127.0.0.11`;
    `docker exec -it gateway sh`.
14. **Change the ports** — the street door moved to 8095 while the room stays 9100, and why you'd
    do it; the gateway's log still says 8090; the processor moved to 9300 fails quietly (the page has
    no error handling; `docker logs gateway` shows `Connection refused`); the one setting that fixes
    it, with no rebuild; cleaning up before Compose.
15. **Compose: the same app, declared** — `docker-compose.yml` as the by-hand flags written down
    (`container_name`, `build`, `ports`, `environment`, `networks`), plus `volumes` and `depends_on`;
    `docker compose up`, image names from folder and service, `compose ps`, `compose exec`; the
    README's comparison table; Ctrl+C takes about 20 seconds (Python as the first process ignores the
    polite stop, so Docker kills it after 10 seconds: exit code 137); `compose ps -a`, then `down`.
16. **Edit, apply, tear down, recap** — `up -d`, `compose logs -f`, `compose exec gateway sh`; the port
    experiment in the file, where `up -d` recreates only the gateway; changed code copied into an
    image needs `--build`; the mounted gateway folder shows page edits without a rebuild;
    `docker compose down`, and the images that remain; five test-yourself questions; lecture 5.

The README's small mistakes are pointed out kindly, with the fix: the branch-switch note covers only
edited files (an extra `git stash -u` handles the untracked ones), and your ignored lecture 3 files
are replaced without a word (copy them out first); the `assert` only rejects an empty group name,
while `generate_text` and `translate_text` ship the course's project and bucket and the
instructor's group (set all three values in all five files); no command creates the bucket, and the
sample upload is named `test.mp3` (create it in the console, name your recording `input-….mp3`);
`generate_text`'s README still says "Vertex AI User" (search "Agent Platform User"); the
transcription keeps only a long recording's first chunk (use a short clip); `translate_text` targets
Spanish for a French voice (set `"fr"`); the ElevenLabs bonus looks for its key inside `/app` (point
it at `/secrets`); `run` doesn't simply pull from the registry: any local image wins, and the
fallback is a 2025 Python 3.8 image (build locally); "secrets outside the repo" protects Git, not
images, with no `.dockerignore` on any branch (delete in-component `secrets/`, add a `.dockerignore`,
delete any key that was pushed); the processor image has `curl` although the README implies it
doesn't; the gateway's log always says `localhost:8090` (trust `docker ps` and the page); and "it
should fail" fails silently on the page (read `docker logs gateway`). One gotcha is not a slip:
`<your-project-id>` is a placeholder, angle brackets included.

## Rebuild

```bash
python -m explainer.build videos/ac215-l04-flexible-workflow-ports -q l                          # fast draft
python -m explainer.build videos/ac215-l04-flexible-workflow-ports --render-only --jobs 3        # 1080p60 scene renders
python -m explainer.build videos/ac215-l04-flexible-workflow-ports --no-render --crf 27 --burn   # stitch: video, parts, subtitles, burned-in copy, chapters, transcript
python -m explainer.build videos/ac215-l04-flexible-workflow-ports --subs-only                   # rewrite subtitles only
python -m explainer.i18n check videos/ac215-l04-flexible-workflow-ports --lang zh                # Chinese text aligned with the English
```

No MP4 is in Git (the burned-in copy is a release asset): after a fresh clone, render the scenes
once, then the `--no-render` line rebuilds the clean video, the two part cuts and the burned-in copy
from the scene renders.

Narration: Kokoro (`af_heart`, speed 0.9), generated locally.

*Course materials belong to the AC215 teaching staff (Harvard IACS); this video is made for study
with the instructor's permission. The Google Cloud console, the bucket, Docker Hub and the port_toy
page are schematic drawings (tagged `illustration`), not screenshots; no Google account or key was
used or shown.*
