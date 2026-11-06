# AC215 · Lecture 20 — Deployment: by hand, then Pulumi to a single VM

A follow-along walkthrough of the Lecture 20 tutorial of Harvard's **AC215 (MLOps & LLMOps, Fall
2026)**, *Deployment: Pulumi*:
[dlops-io/cheese-app-v3](https://github.com/dlops-io/cheese-app-v3), branch `main` @
[`3ecef56`](https://github.com/dlops-io/cheese-app-v3/tree/3ecef56fea879ac480d260c0906cd95baf05179a)
(2025-11-28, "v4->v3"), its README sections *Deployment to GCP (Manual)* (README:4–222),
*Deployment to GCP (Single VM Instance)* (README:225–383) and *Delete the Compute Instance /
Persistent disk* (README:387–390).

**Which commit.** The course page links the repository's default branch, unpinned. On the recording
day, 2026-11-05, `git ls-remote` still gave `main` = `3ecef56` (`laptop/p03`), and so did a re-check on
2026-11-06, so the video follows that README. An unmerged staff branch rewrites the README and replaces
`deploy_single_vm/`; if it is merged into `main`, part 2 of this video no longer matches the README you
open: check `git log -1` in your clone. Details in [`ASSETS.md`](ASSETS.md), "Which commit".

One container stops, the frontend, and the whole site goes dark, the API's address included, although
the API is still running. Why? The video builds the answer twice. Part 1 deploys the cheese app by
hand, the lecture's four manual stages: images to Docker Hub, a VM with Docker, folders, a key and a
Docker network, five containers (the vector DB, a one-shot loader with 14,356 chunks, the API, the
frontend) and nginx in front as the one public door. Part 2 does the same deployment as code, the
lecture's six steps: Pulumi's desired state, state and reality, a deployment toolbox (which needed two
one-line fixes to build that day), two service accounts and an SSH key for OS Login, then two Pulumi
projects: images with timestamp tags, and a VM with its fences, provisioning over SSH, containers over
SSH and nginx, then `pulumi destroy`.

Watch it with your own clone of cheese-app-v3 next to a `secrets/` folder, Docker running, a GCP
project with billing and a Docker Hub account, and pause at every `▶ your turn` to run the command.
**This lecture creates billable resources**: a VM with its boot disk (part 1), then a VM, a data disk,
an external IP, Artifact Registry storage and a state bucket (part 2); a GOLD tag marks each place, and
each part ends by deleting what it made. The tracker top left shows the README step; a gray `extra` tag
marks a command that isn't in the README, and a gray "Lecture 20 · slides …" tag top right points to the
lecture slides the scene stands on.

The terminal sessions were recorded on 2026-11-05 in fresh containers: a Debian 12 machine standing in
for your VM (Docker 29.9.3 from the README's `get-docker.sh`, nginx 1.30.6, Chroma 1.0.0) and a Docker
29.8.2 engine standing in for your laptop, with the deployment toolbox built from `src/deployment/`
(Python 3.13.18, uv 0.13.7, Google Cloud SDK 592.0.0, Pulumi v3.274.0). That machine had **no Google
account, no Docker Hub login and no credentials**. Everything that runs on a machine you own ran live:
the whole manual deployment on the stand-in VM, from `get-docker.sh` to nginx answering on port 80 with
the frontend and the API behind it; `docker-hub.sh` building the production frontend; the toolbox's
build (and its two failures); every tool check and `ssh-keygen`. Every command that needs Google or
Docker Hub is shown up to its honest first error (`push access denied`, `invalid_grant: account not
found`, `PULUMI_ACCESS_TOKEN must be set`, `403 Forbidden` on the push), and the video says what yours
prints. Pulumi's previews were also run on its local file backend, tagged `extra · not for you`, up to
their first Google call. The console, the browser and a successful `pulumi up` are schematic drawings
tagged `illustration`; the README's own OS Login output is the one `expected` panel. Project IDs and
`sa_…` users on screen are placeholders. Series format:
[`docs/AC215_SERIES.md`](../../docs/AC215_SERIES.md). Study guide with every command:
[MLOps_Learning · guides/L20-deployment-pulumi.md](https://github.com/JunyiZhou-Conny/MLOps_Learning/blob/main/guides/L20-deployment-pulumi.md).

English narration; Chinese and bilingual subtitles (中文字幕说明见 [`i18n/zh/README.md`](i18n/zh/README.md)).

| file | what it is |
| --- | --- |
| `output/ac215-l20-deployment-pulumi.zh-en.mp4` | **the copy to watch**: 1080p60, English narration, bilingual subtitles (Chinese above, English below) burned in, DURATION_FULL. Published as a GitHub release asset: no MP4 is kept in Git ([`docs/PUBLISHING.md`](../../docs/PUBLISHING.md)) |
| `output/ac215-l20-deployment-pulumi.mp4` | the same video without burned-in subtitles; load any `.srt` below in your player. Release asset, not in Git: rebuild it with `--no-render` (see Rebuild) |
| `output/ac215-l20-deployment-pulumi_part1.mp4` | part 1, DURATION_P1: deploy by hand — Docker Hub, a VM, five containers and nginx (S01–S08). Release asset, not in Git |
| `output/ac215-l20-deployment-pulumi_part2.mp4` | part 2, DURATION_P2: the same deployment as code — Pulumi, two stacks, one destroy (S09–S16). Release asset, not in Git |
| `output/ac215-l20-deployment-pulumi.srt` | English subtitles (each part has its own `.srt`, `.zh.srt`, `.zh-en.srt` / `.ass`) |
| `output/ac215-l20-deployment-pulumi.zh.srt` | Chinese subtitles (on the English timing) |
| `output/ac215-l20-deployment-pulumi.zh-en.srt` / `.zh-en.ass` | bilingual subtitles |
| `output/chapters.txt`, `chapters_part1.txt`, `chapters_part2.txt` | chapter timestamps |
| `output/transcript.md` | the full narration by chapter |
| `exercises.md` | do these after watching: the five test-yourself questions, hands-on predict-then-run tasks, debugging and think questions, with answers; what was run to check them is in [`assets/exercise-checks/`](assets/exercise-checks/README.md) |
| `digest.md` | the tutorial digest: every step, a code tour with `path:line`, gotchas, errata |
| `SLIDES.md` | the lecture behind the tutorial: a digest of the slide deck in our own words, with slide numbers, and which scene stands on which slides |
| `assets/terminal/` | the **real** terminal sessions every terminal panel prints from (2026-11-05, fresh containers, no Google account); provenance in [`ASSETS.md`](ASSETS.md) |
| `assets/source/` | the tutorial files the code panels quote, unchanged at `3ecef56` |
| `BRIEF.md`, `script.md`, `scenes/` | the design, the narration (SAY) + visual plan (SHOW), and the Manim source |
| `i18n/zh/` | the Chinese subtitle text: glossary and sentence-aligned translation |

Git keeps the subtitles, the chapter files and the transcript; the MP4s (the burned-in copy, the clean
video and the two part cuts) are release assets.

## Chapters

CHAPTERS

## What you'll learn

Five *pause and ponder* moments ask you to predict before the video shows you: whether the 14,356
chunks are gone with the loader; whether port 9000, published on the VM, answers from your laptop;
what the plan shows when you run `pulumi up` again without changing anything; why the format step
checks with `blkid` before `mkfs.ext4`; and which of the two keys you would hand the VM. Five
test-yourself questions close the video (answers in `exercises.md`).

**Part 1 · deploy by hand: Docker Hub, a VM, five containers and nginx**

1. **One container stops, the site goes dark** — the frontend stopped and nginx restarted, the API
   still up, yet nothing answers; the puzzle; the lecture's target picture; the roadmap; what you need
   (cheese-app-v3 with `secrets/` beside it, a GCP project with billing, a Docker Hub account) and the
   cost; the tracker and `▶ your turn`; what the recording machine can and cannot show.
2. **From your laptop to one VM** — the request path: browser → port 80 → nginx → frontend 3000 or API
   9000 → vector DB 8000; the slide's arrowheads, and a fifth container (the loader); the lecture's
   four manual stages; the README's local check, and why `/status` (version 3.0) is a better API check
   than `/docs`; L18 now teaches a refactored v2, here you run v3; the clone and `git log`.
3. **Images to Docker Hub** — an access token; `docker login` typed as printed fails (angle brackets
   are redirections); `--password-stdin`; `docker-hub.sh`: `DOCKER_USERNAME="dlops"` (change it), a new
   BuildKit builder, two platforms for the API, one for the frontend; the frontend's build and the push
   refusal; the other two scripts; skipping this stage with the public `dlops` images.
4. **A VM with Docker, folders and a network** — the console's VM (N2D, 50 GB, HTTP and HTTPS
   allowed), network tags and the default firewall, what bills; SSH in (a Debian 12 stand-in);
   `get-docker.sh`; the six folder commands (listed twice: run them once) and their `0777`; the app's
   key written with `echo`; `cheese-app-network`, where containers find each other by name.
5. **The vector DB and its loader** — `|| true` makes the stop and remove safe to repeat; the Chroma
   container (network, port 8000, `--restart always`, a mount); the heartbeat; the loader finds the
   database by name and loads eleven files, 14,356 chunks (precomputed embeddings); `--rm`; where the
   chunks live, and the mount slip: Chroma saves to `/data`.
6. **The API and the frontend** — `api-service` (pulled on first run): mounts, port 9000, key path,
   database by name, a bucket name passed but never used; the CNN model from a GitHub release; a 5 GB
   image; `/` and `/docs` answer, `/status` says 404 (the public image is older than your clone); the
   interactive variant's name conflict; the frontend on 3000 and `BASE_API_URL: /api-service`.
7. **nginx: one public door** — a reverse proxy on port 80; `location ^~ /api-service/` and the one
   slash in `proxy_pass` that strips the prefix; everything else to the frontend; the README's `echo`
   eats the `log_format` (write the file with a quoted heredoc); nginx, four containers, the home page
   and `/api-service/` through nginx; port 9000 is open on the VM but shut at the fence; the puzzle
   answered: nginx looks names up at start; start order and restart policies.
8. **Twenty-one commands: repeat, review, undo?** — the tally; three questions; the lecture's answer,
   infrastructure as code in a real language, kept in Git; the course's earlier Ansible version; delete
   the part 1 VM with its boot disk (the README never says so).

**Part 2 · the same deployment as code: Pulumi, two stacks, one destroy**

9. **Pulumi: desired state, not steps** — one firewall rule from the repo (constructor, logical name,
   arguments); constructors only register; the engine loop: program → desired state, state from your
   bucket, `--refresh` against reality, the plan's `+ ~ - +-`, providers; the lecture's seven commands
   and the five the tutorial uses; `pulumi up --stack dev --refresh -y`, what `-y` skips, `preview`; a
   second run with no change plans nothing.
10. **Setup: four APIs, two keys** — the lecture's six steps and their files; four APIs (and Vertex AI
    for the chat); the `deployment` account (six roles) and `gcp-service` (three), and why two; the keys
    in `secrets/` next to the clone, three folders up from `src/deployment`; the missing step: create the
    Artifact Registry repository.
11. **The deployment toolbox, fixed twice** — `docker-shell.sh`'s environment and mounts (the Docker
    socket, `/app`, `/secrets`); `GCP_PROJECT`; the committed build fails (Debian 11 security updates
    archived: fix 1, bookworm), then `google-cloud-sdk` has no installation candidate (fix 2,
    `google-cloud-cli`); the entrypoint's five steps and our first error; tool checks (kubectl newer
    than the pin); `gcloud auth list`; the extra `gcloud artifacts repositories create` line.
12. **SSH keys and OS Login** — Pulumi logs in to the VM as the deployment account through OS Login;
    the template's angle brackets again; `ssh-keygen` with no passphrase; the two files in `secrets/`;
    the key upload and the `sa_…` username; the `inventory.yml` step is an Ansible leftover.
13. **Step 2: images with timestamps** — GCR on the slide, Artifact Registry today; stacks (dev,
    staging, prod) and the tutorial's two projects; `organization/deploy-images/dev` (don't rename it);
    `pulumi stack init dev` without a bucket login, and `pulumi stack select dev`; the local backend for
    the recording; `Pulumi.dev.yaml`; the timestamp tag, `docker_build.Image` (push, `retain_on_delete`,
    amd64); a preview never builds; `up` builds and the push is refused here; every `up` rebuilds.
14. **Steps 3–4: the VM, its fences, provisioning** — the slide's network share is a second disk at
    `/mnt/disk-1`; stack init and three config sets (your values); the four calls of `__main__.py`; a
    cloud network and three firewall gates; the data disk, the Ubuntu image lookup, the IP as an
    Output; the preview stops at the first Google call; check the plan before `-y`; roughly two dollars a
    day; nine provisioning commands over SSH, and the `blkid … || mkfs.ext4` guard: scripts must be safe
    to run twice.
15. **Steps 5–6: containers over SSH, then test** — the `StackReference` (run the images stack first);
    a Docker provider over SSH; three containers (the frontend on 3000, not 80); nginx on top and port
    80; the config's checksum as a trigger; what a successful `up` builds and its six outputs; the
    exported `ssh_command` needs `-i`; which key the VM should hold, and what this repo actually does;
    test the app; the README's container checks on the VM; the retired Gemini model.
16. **Destroy, recap, and what's next** — "don't forget to delete"; `pulumi destroy` in
    `deploy_single_vm`, in reverse order; images stay, retained on delete; the six-item teardown
    checklist (registry repository, state bucket last, the part 1 VM, Docker Hub, the keys); the six
    steps as recap; the lecture's principles scored; a single point of failure, and Lectures 21–23.

The README's and the slides' small slips are pointed out kindly, with the fix: the README's `<…>`
placeholders are shell redirections (replace them entirely, `docker login` and the OS Login template);
`docker-hub.sh` pushes to `dlops` (set your Docker Hub name); the README's API check is `/docs`, but on
v3's code `/status` tells you which version runs, and the public images on the VM are older than your
clone (`/status` gives 404 there); the folder commands appear twice (run them once); the Chroma mount
misses today's `/data`; the interactive API variant clashes with the running container's name; the
`log_format` is mangled by the nested quotes of the `echo` (use a quoted heredoc); only the vector DB
gets a restart policy; the manual VM is never deleted; nothing creates the Artifact Registry repository
(one `gcloud artifacts repositories create` line); "cd into `deployment`" means `src/deployment`; the
toolbox's Dockerfile doesn't build as committed (bookworm instead of bullseye, `google-cloud-cli`
instead of `google-cloud-sdk`); the SSH key must have no passphrase; `inventory.yml` belongs to the
earlier Ansible version; the README's project and `sa_…` user must be replaced with yours; the exported
`ssh_command` lacks `-i /secrets/ssh-key-deployment`; the chat's Gemini model is retired (change
`GENERATIVE_MODEL` and `up` both projects); and `pulumi destroy` belongs in `deploy_single_vm` and
leaves the images, the repository and the state bucket. Where the slides differ from the repository:
the registry is Artifact Registry, not GCR; the "network share" is an attached disk; the frontend is on
3000 and nginx on 80; the model comes from a GitHub release, not a bucket; and in this repo the VM runs
as the deployment account, capped by scopes, while the narrow key serves the containers.

## Rebuild

```bash
python -m explainer.build videos/ac215-l20-deployment-pulumi -q l                          # fast draft
python -m explainer.build videos/ac215-l20-deployment-pulumi --render-only --jobs 3        # 1080p60 scene renders
python -m explainer.build videos/ac215-l20-deployment-pulumi --no-render --crf 27 --burn   # stitch: video, parts, subtitles, burned-in copy, chapters, transcript
python -m explainer.build videos/ac215-l20-deployment-pulumi --subs-only                   # rewrite subtitles only
python -m explainer.i18n check videos/ac215-l20-deployment-pulumi --lang zh                # Chinese text aligned with the English
```

No MP4 is in Git (the burned-in copy is a release asset): after a fresh clone, render the scenes
once, then the `--no-render` line rebuilds the clean video, the two part cuts and the burned-in copy
from the scene renders. The captures can be re-run with `assets/terminal/capture.sh` (see
[`ASSETS.md`](ASSETS.md), "`terminal/` — real terminal sessions"); the exercise checks with the scripts
in [`assets/exercise-checks/logs/`](assets/exercise-checks/README.md).

Narration: Kokoro (`af_heart`, speed 0.9), generated locally.

*Course materials belong to the AC215 teaching staff (Harvard IACS); the cheese-app-v3 tutorial is used
for study with the instructor's permission and quoted at its pinned commit. The lecture's slides are
redrawn in our own pictures, never shown. The Google Cloud console, the Docker Hub page and the browser
are schematic drawings (tagged `illustration`), never screenshots; the recording used no Google account,
no Docker Hub login and no credentials, and every project ID and `sa_…` user on screen is a placeholder.*
