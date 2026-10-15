# Brief · AC215 L4 — Containers II-b: build or pull, ports and Compose

The design of this video, written before the script. Series rules: `docs/AC215_SERIES.md`.
Facts: `digest.md` (the verified tutorial digest) and `assets/` (real captures, see `ASSETS.md`).
**Where the digest and the captures disagree, the captures win.** They are newer (2026-10-14,
00:29–00:40 UTC) and were made on the machine the video shows:

| topic | digest | captures (use these) |
| --- | --- | --- |
| branch switch from an L03 clone | one refusal (untracked files; the experiment had no edited `cli.py`) | **both** refusals at once: the edited `cli.py` *and* the untracked `generate_text/Dockerfile`, `uv.lock` (`mega-l03-laptop/04`); the README's `git stash` clears only the first (`06`); `git stash -u` is needed (`07`, `08`) |
| `git fetch origin` | "get the branches you don't have yet" | prints nothing: a clone already has every branch (`mega-l03-laptop/03`) |
| Python in the images | "3.14.x" | Python 3.14.8, uv 0.13.0, `Using CPython 3.14.8 interpreter at: /usr/local/bin/python3` — no download this time (`mega-transcribe_audio/04`, `08`; `mega-laptop/12-a-docker-shell.plain.txt:1427`) |
| builds and sizes | not measured | transcribe first build `Building 99.5s` (apt layer 44.7 s, `uv sync` 1.6 s, 26 packages), 1.48 GB; generate_text 52.6 s (own apt layer), 34 packages, 821 MB; C, D, E 8.2 / 7.9 / 7.9 s (`CACHED [2/5]`, B's apt layer), 833–836 MB (`mega-laptop/12`, `31`, `40`, `51`, `61`, `70`) |
| where a missing key fails | *expected*: at `-d` in A/B, at import (even `--help`) in C, D, E | confirmed: A `--download` fails at `storage.Client()` **cli.py:39** (`mega-transcribe_audio/09`; the digest's `get_bucket` line 40 is never reached); B `--help` works, `--download` fails (`mega-generate_text/01`, `02`); C fails at the `assert` before the edit (`mega-laptop/40`) and at import after it (`mega-synthesis_audio_en/02`); D, E fail at import (`mega-laptop/51`, `61`) |
| B `--generate` without a key | not discussed | exit 0, prints only `Args: …` and `generate`: nothing was downloaded, so Gemini is never called (`mega-generate_text/03`, `05`) |
| `run` with no local image | *expected*: Python 3.8, pipenv, maybe a root-owned `Pipfile` | real: pull of `dlops/mega-pipeline-*:latest`, `Creating a Pipfile for this project...`, `(app) root@…:/app#`, **Python 3.8.17**; A's `--help` still works, B's fails with `ImportError: cannot import name 'genai'`; a **root-owned `Pipfile`** lands in your folder (`mega-laptop/72`, `73`, `74`, `76`, `77`) |
| the L03 key after the switch | stays in `transcribe_audio/secrets/` (G6, inferred) | real: still there (`mega-l03-laptop/10`, `11`) and **inside the image** after `./docker-shell.sh dev` (`13`; a 79-byte stand-in, not a key) |
| `gcloud config set project <your-project-id>` | typed as the README shows | typed literally, bash refuses: `-bash: syntax error near unexpected token 'newline'` (`gcloud-laptop/01`); filled in: `Updated property [core/project].` (`02`); `gcloud services enable` without an account: `ERROR: (gcloud.services.enable) You do not currently have an active account selected.` (`03`) |
| `curl localhost:9200` | `curl: (7) Failed to connect to localhost port 9200 …` (*expected*) | `curl: (7) Failed to connect to localhost:9200 after 0 ms: Could not connect to server` (`port-laptop/23`); inside the gateway `… localhost port 9200 …` with curl's progress meter above it (`25`) |
| `docker exec gateway curl http://processor:9200/health` | `ok` | curl's progress meter (stderr), then `ok` (`port-laptop/24`); `docker compose exec` shows only `ok` (`51`: it gives curl a terminal) |
| Step 3 "It should fail" | *expected*: page does nothing, `ConnectionRefusedError` in the log | real: `curl: (52) Empty reply from server` for the page's request (`38`); the gateway's log ends `ConnectionRefusedError: [Errno 111] Connection refused` (`39`) |
| network and addresses | example `172.18.0.3` | `toynet` is `172.19.0.0/16`, processor `.2`, gateway `.3`; inside the gateway `nameserver 127.0.0.11` (`28`, `29`) |
| ephemeral port | README's `44456` | `55620`, then `55634` on the next send, `47520`, `39938`, `47534`, `56572` later (`14`, `15`, `32`, `43`, `49`, `59`) |
| Ctrl+C / `down` | *expected* ~10–20 s | Ctrl+C at 3.9 s, done at 24.3 s, both `exited with code 137` (`47`); `down` of the running app `Removed 10.2s` each, 20.8 s (`64`); `up -d` after the port edit recreates the gateway in 10.5 s (`58`) |
| leftovers before Compose (G11, Q5) | network: refuse ("incorrect label") or reuse, version-dependent | Compose v5.6.0: leftover containers → `Conflict. The container name "/processor" is already in use` (`68`); a leftover network alone only **warns** and is used, and `down` then leaves it behind (`69b`, `69c`) |
| image names | `port_toy-*` (*expected*) | `port_toy-gateway`, `port_toy-processor`, 198 MB each beside `toy-*` (`47`, `66`) |
| processor image and curl (E14) | Dockerfile installs it | confirmed: curl 8.14.1 in the processor (`27`) |

## Audience and goal

An AC215 student who has done L1 (VMs, venvs, uv), L2 (a given Dockerfile, images, Docker Hub,
platforms) and L3 (the five-container mega-pipeline with a course key, bind mounts, `uv add`, the
key-in-the-image trap). Docker Desktop and git are installed (Tutorial 0), and for part 1 they have
a GCP project with billing and the `gcloud` CLI logged in. They watch with two clones open,
`~/AC215/mega-pipeline` (branch `flexible-workflow`) and `~/AC215/port_toy`, pausing to type each
command.

After the video they can:
- get the `flexible-workflow` branch either by a fresh clone or by switching an L03 clone, and get
  past both of `git checkout`'s refusals (`git stash -u`) without losing their L03 work;
- set the three values in all five `cli.py` files, and say why two files would otherwise silently
  use the course's project, bucket and group;
- create their own service account with the four roles, place its JSON key in `secrets/` *beside*
  the repo, enable the five APIs, and name the three gates a call must pass (key, role, API) and
  the error each one gives;
- read `docker-shell.sh` top to bottom: the four modes, the two bind mounts (`/app`, `/secrets`),
  the env var, and why it must be run from the component folder;
- run the five components through the Quick Reference and recognise the no-key, unedited-config
  and silent no-op outcomes;
- explain build vs pull: why `run` can hand you a February-2025 Python 3.8 image, and when to use
  `dev`, `run` and `prod`; keep an old key out of their images;
- explain container networks and ports with port_toy: own `localhost` per container, name lookup on
  a user-defined network, published vs listening vs source ports, `-p ip:host:container`; change a
  host port and a container port and fix the mismatch with configuration only;
- run the same app with Compose, read `docker-compose.yml` as the by-hand commands written down,
  and know what `Ctrl+C`, `down`, `up -d` and `up -d --build` each do.

## Length and parts

~32 minutes. Narration 3,900–4,300 words (Kokoro af_heart, speed 0.9 ≈ 174 wpm); the plan below
totals **~4,220** (part 1 ~2,370, part 2 ~1,850). Two tutorials, so the cut is natural:
- **Part 1 = S01–S09**, mega-pipeline `flexible-workflow`: the team workflow, your own cloud
  resources, `docker-shell.sh`, the five components, build vs pull, publishing and clean-up
  (~13.6 min of narration, ~17 min with typing, outputs and ponders). It ends on part 1's teardown
  card and "in part 2, containers that talk to each other directly".
- **Part 2 = S10–S16**, port_toy: networks, names, ports, Step 3's breakage, Compose (~10.6 min of
  narration, ~15 min with the many short commands).
Word budgets per scene are targets (±15 %).

## Colours (series table, applied)

| meaning | colour |
| --- | --- |
| your laptop: the workspace `~/AC215`, the clones, component folders, the `secrets/` folder beside the repo, the files a bind mount shows inside; the browser and the published (host-side) port doors | GREY |
| Google Cloud: your project, the bucket and its drawers, the five APIs, IAM and the service account; Docker Hub (a registry shelf) | BLUE |
| containers and images: the five component images, `gateway` and `processor` boxes, layer stacks, container-side listening doors (`:9100`, `:9200`), the `toynet` rail (Docker's network) | TEAL |
| system parts inside an image: the Debian base, the apt layer (`build-essential`, `ffmpeg`, `curl`), the base image's Python 3.14.8 | ORANGE |
| project-owned and committed: the recipe card (`Dockerfile` + `pyproject.toml` + `uv.lock`), tracked files at a branch switch, `/home/app/.venv`, `docker-compose.yml` | GREEN |
| tools: docker, buildx, Compose, git, gcloud, uv; `docker-shell.sh` itself (a tool the repo ships) | PURPLE |
| errors and "avoid this": checkout refusals, `DefaultCredentialsError`, `AssertionError`, the stale `dlops/*` image, the key inside an image, `Could not connect`, `Connection refused`, `Empty reply`, `port is already allocated`, `Conflict` | RED |
| your turn, the README tracker, "look here now" | YELLOW |
| money: your own project now pays — cost tags on API calls and the bucket; the service-account key (whoever holds it spends your project's money) | GOLD |
| lookups and routes: the bind-mount routes (`/app`, `/secrets`), the `GOOGLE_APPLICATION_CREDENTIALS` signpost, the `run` decision diamond's arrows, the DNS phone book, packets, `-p` mapping arrows, the ephemeral-port ticket | PINK |
| a future thing (L05: a CLI container calling ChromaDB by name) | GREY, dashed |

The key is always a GOLD key glyph; its file content is never drawn. Untracked files at a branch
switch are GREY, ignored files GREY dashed. A gate (S05) is BLUE; it shows a white tick when open
and turns RED when it refuses.

## Running example

- The laptop: user `student`, host `laptop`, workspace `~/AC215` (the README's `<your-workspace>`),
  as captured: `student@laptop:~/AC215$`, `student@laptop:~/AC215/mega-pipeline$`,
  `student@laptop:~/AC215/mega-pipeline/transcribe_audio$` (and the other four), and
  `student@laptop:~/AC215/port_toy$`. The L03 path uses a second workspace,
  `student@laptop:~/AC215-l03/mega-pipeline$`. Say once (S01): on a Mac (zsh, `%`) or in Windows
  Git BASH the prompt looks different and Docker Desktop runs the containers; the commands, ports
  and errors are the same.
- Containers: `app@0ceffb272288:/app$` (A, `mega-laptop/12`), `app@45263bb6ca36` (B), `app@ba0b1df0eadc`
  (C), `app@40d7497c50f2` (D), `app@6172f2cd7728` (E); the stale image `(app) root@36615ab6e34b:/app#`
  (`72`). Say once (S06) that the part after `app@` is the container id and changes every run.
- Values: `gcp_project = "your-project-id"`, `bucket_name = "your-team-bucket"`,
  `group_name = "group-01"` — the captures' placeholders (`mega-laptop/11`); narration: "type your
  own". Never a real-looking project id.
- port_toy: the gateway on host port `8090` (then `8095`), processor `9200` (then `9300`); ephemeral
  ports from the captures (`55620`, `55634`, …): "your numbers will differ".
- Builds: show `Building …s`, the numbered `[n/5]` / `[n/4]` steps and `naming to …`; cut every
  `=> =>` sub-line, the `transferring …` lines and the `[1/5] FROM …@sha256:…` / `[1/4] FROM …` lines
  (their digests are the capture's rebuilt base, not Docker Hub's). Say once (S06, S11): your first
  build also downloads the base image (`python:3.14-slim-bookworm`, `python:3.14-slim`).
- Long outputs: first and last lines with a `…` line (series rule). Tracebacks: the first `cli.py`
  frame and the last line. Wide outputs (`docker ps`, `docker compose ps`, ~150 columns) wrap at 80
  columns as the capture terminal would; highlight the `PORTS` cell.
- Versions are "at the time of recording": Docker Engine 29.8.2, Compose v5.6.0, buildx v0.37.2,
  git 2.54.0, Python 3.14.8, uv 0.13.0, Cloud SDK 570.0.0.

## Visual set pieces (the 3Blue1Brown part)

- **V1 · Recipe card or frozen meal: build or pull (S01 teaser, S02, S08).** Left: a Git shelf with
  a GREEN recipe card listing `Dockerfile`, `pyproject.toml`, `uv.lock`. A PURPLE `docker build`
  arrow turns the card into a TEAL local image labelled `Python 3.14.8 · uv`. Right: a BLUE Docker
  Hub shelf with a sealed box; on it a tag `dlops/mega-pipeline-transcribe-audio:latest` drawn as a
  signpost whose arrow points *at* the box, not at the recipe. Early in a project everyone builds
  (arrows from the card); later one person publishes and everyone pulls (arrows from the shelf),
  `README.md:69-72`. The signpost's point: a tag names *an* image built on some day from some
  commit; it does not promise it came from the commit you have. S08 payoff: the box opens — date
  `2025-02-18`, `Python 3.8.17`, `pipenv shell`, `user: root` (all from `mega-laptop/74`) — and a GREY
  sheet (your folder) slides over its `/app`: "your code, their environment". A small GREY `Pipfile`
  owned by root drops out of the box onto your laptop (`73`).
- **V2 · Three piles at a branch switch (S03).** The L03 working tree as three piles (real names from
  `mega-l03-laptop/01`): tracked (GREEN, `transcribe_audio/cli.py` marked edited), untracked (GREY:
  `generate_text/Dockerfile`, `generate_text/uv.lock`), ignored (GREY dashed: `transcribe_audio/Dockerfile`,
  `pyproject.toml`, `uv.lock`, and the GOLD key in `secrets/`). `git checkout flexible-workflow`
  slides the branch's files in from above: it stops at two RED walls — the edited tracked file and
  the untracked files sitting where branch files go. `git stash` lifts only the edited file into a
  box (one wall falls); `git stash -u` lifts the untracked pair too (second wall falls); the branch
  lands. Coda: in the ignored pile, `Dockerfile` silently flips from `FROM python:3.12-slim-bookworm`
  to `FROM python:3.14-slim-bookworm` (`01`, `11`), and the GOLD key stays put.
- **V3 · Three gates: who, may, switched on (S05; callback S07).** A container on the left; through
  a PINK `/secrets` route comes the GOLD key; `google.auth` stamps it into a short-lived token (a GOLD
  tag with a small clock). The token flies right toward four BLUE API doors (Storage,
  Speech-to-Text, Vertex AI, Translation) and a fifth, Text-to-Speech, with no role lock
  (`README.md:185`). Gate 1, *who*: the key must exist and be readable — fails inside the container,
  before any request (`DefaultCredentialsError`, real in S07). Gate 2, *may*: an IAM role lock on
  each door. Gate 3, *switched on*: an "API enabled" switch on each door. A door opens only when its
  lock and switch both show a tick (`README.md:187`: "two separate steps"). Gates 2–3 fail at Google
  as a permission error (said, not shown: nothing here reached Google).
- **V4 · The switchboard: `docker-shell.sh` (S06, S08, S09).** The script's `case "$1"`
  (`docker-shell.sh:28-46`) as a railway switch with four PURPLE tracks: *(no argument)* → build,
  then run; `dev` → build only; `run` → run only; `prod` → buildx, two trains (amd64, arm64), push.
  Each track lights the real script lines it executes (`:71-76`, `:79-96`, `:51-68`). On the run
  track a PINK diamond asks `docker image inspect mega-pipeline-…`: yes → the local image; no →
  `$DOCKER_USERNAME/…` on the BLUE shelf (`:82-89`). S06 drives the default track, S08 the `dev`
  and `run` tracks and the diamond's "no" branch, S09 the `prod` track.
- **V5 · Two windows into the laptop (S06; contrast in S09).** L3's window, doubled. The laptop
  (GREY): `~/AC215/` with `mega-pipeline/transcribe_audio/` and `secrets/` beside the repo. The
  container (TEAL): `/app`, `/secrets`, and the GREEN `/home/app/.venv` outside both
  (`Dockerfile:17`). `$(pwd)/../../secrets/` is drawn as a walk: from the component folder up two
  levels, then into `secrets/` (`docker-shell.sh:8-9`). Two PINK routes: the component folder →
  `/app` (`:93`), `secrets/` → `/secrets` (`:94`); a PINK signpost `GOOGLE_APPLICATION_CREDENTIALS=
  /secrets/mega-pipeline.json` (`:95`). The real `docker inspect` mounts line by line (`mega-laptop/14`).
  The key crosses only at run time, never into an image. S09 contrast: a key left *inside* the
  component folder rides `COPY . ./` into a layer instead.
- **V6 · Little computers on one LAN (S10, S13).** Two glass TEAL boxes, `gateway` and `processor`,
  each with its own `localhost` loop drawn inside and its own strip of ports 1…65535. `docker network
  create toynet` lays a TEAL rail under them; joining the network plugs each box in. On the rail a
  PINK phone book: `processor → 172.19.0.2`, `gateway → 172.19.0.3` (`port-laptop/28`, `29`), served
  at `127.0.0.11` inside each box. "Where is processor?" goes to the phone book, the answer comes
  back, a packet travels the rail. `localhost` inside the gateway loops back into the gateway
  itself (`26`); the laptop's `localhost` is a third, separate loop outside both.
- **V7 · Doors, rooms and tickets: ports (S11, S12, S13, S14).** The laptop (GREY) has street doors;
  the boxes have rooms. `-p 127.0.0.1:8090:9100` draws a GREY door `127.0.0.1:8090` on the laptop and
  a PINK arrow through it that bends into the gateway's TEAL room `:9100`, the three numbers lifting
  off the flag in order *ip : host : container* (`README.md:224-230`). The processor's room `:9200`
  opens only onto the rail. A dashed arrow from the laptop to `:9200` bounces RED (`Could not
  connect`). S12: the gateway's kernel prints a PINK ticket `55620`, staples it to the outgoing
  packet, and the processor reads the same `55620` back (`14`). S13: a second door `0.0.0.0:8091`
  faces the street (all addresses) while `127.0.0.1` faces only inward; a second request for 8090
  hits a RED "port is already allocated" (`18`, `20`, `21`). S14: a slider moves the street door
  8090 → 8095 while room 9100 stays; then the processor's room moves 9200 → 9300 while the gateway's
  arrow still aims at 9200 and turns RED; setting `PROCESSOR_PORT=9300` re-aims it.
- **V8 · Commands become one file (S15, S16).** Left: the by-hand commands of Step 1 (network
  create, two builds, two runs). Each flag lifts and flies to its YAML key on the right
  (`docker-compose.yml`): `docker build ./gateway` → `build: ./gateway`; `--name gateway` →
  `container_name: gateway`; `-p 127.0.0.1:8090:9100` → `ports:`; `-e …` → `environment:`;
  `--network toynet` → `networks: [toynet]` and the bottom `networks: toynet: name: toynet`. Two keys
  have no by-hand ancestor and fade in GREEN-outlined: `volumes: ./gateway:/app` and `depends_on`.
  The left side collapses into one line, `docker compose up`. Lifecycle: `Ctrl+C` greys the boxes
  (still there, `Exited (137)`); `down` removes boxes and rail; the images stay on the shelf. S16:
  an edit to `ports:` re-forms only the gateway box while the processor keeps glowing (`58`).

## README step tracker (ReadmeTracker, top-left)

Step titles ≤ 3 words. The tracker's section is the README heading (or the component folder for
the five component READMEs, which share one recipe).

**mega-pipeline (`flexible-workflow`), `README.md`**
- *Get the Code* (`:30-52`). Starting fresh: Clone branch · cd (2). Already have the repo: cd ·
  Fetch · Checkout · Stash, retry · Confirm branch (5).
- *Before you run* (`:105-160`: folder layout, Configure each `cli.py`, GCS Bucket Details):
  Secrets folder · Set cli.py · Your bucket (3).
- *Service Account & Secrets* (`:169-203`): Create account · Grant roles · JSON key · Save key ·
  Set project · Enable APIs (6).
- *How to Run a Component* (`:207-226`): Build and run · dev · run · prod · chmod +x · winpty (6).
- *Quick Reference* (`:230-274`, with each component README's `--help` and "Testing" blocks), section
  = component folder: `transcribe_audio`: Check --help · Download · Transcribe · Upload (4);
  `generate_text`: Check --help · Download · Generate · Upload · Other model (5, the last from
  `generate_text/README.md:91-94`); `synthesis_audio_en`: Check --help · Download · Synthesize (3);
  `translate_text`: Check --help · Download · Translate · Upload (4); `synthesis_audio`: Check --help ·
  Download · Synthesize (3).
- Component READMEs, other blocks: *Python packages* (`transcribe_audio/README.md:89`): Add a package
  (1); *Publish the container* (`:124-132`): docker login · prod (2).

**port_toy, `README.md`**
- *Prerequisites* (`:20-30`): Check Docker (1).
- *Step 1: Set up the network by hand* (`:75-183`): Get the code · Create network · Build images ·
  Start processor · Start gateway · Check logs · Send a message (7).
- *Step 2: Check the ports* (`:189-325`): Read PORTS · From the laptop · From the gateway (3).
- *Step 3: Change the ports* (`:331-420`): Host port · Processor port · Update gateway · Clean up (4).
- *Step 4: Run with Compose* (`:426-529`): Start the app · Compare commands · Apply changes · Rebuild ·
  Stop and remove (5).
- *Handy commands* (`:557-576`), the five not used elsewhere: Shell inside · Follow logs · Compose
  shell · List networks · Inspect network (5).

Ordering notes (say them in a clause where they occur):
1. `README.md:212-215` lists the four modes as alternatives. The walkthrough uses the default mode to
   run the five components (S06–S07), then comes back to `dev`, `run` (S08) and `prod` (S09) — the
   order of the captures, and the component READMEs also put "Publish" last. The tracker shows
   *How to Run* step 1 and 5–6 in S06, 2–3 in S08, 4 in S09.
2. The cloud setup follows the README's order (folder layout → `cli.py` → bucket → service account →
   APIs, S04–S05) although the key only matters once a component runs.
3. port_toy *Step 4*: "Stop and remove" (`Ctrl+C`, `down`, `ps -a`, `:505-529`) belongs to the
   foreground `docker compose up` of step 1, so S15 does it there (as captured, `47`, `52`–`54`); S16
   runs steps 3–4 in the background with `up -d` and closes step 5 again with the final `down` (`64`).
4. *Handy commands* are a reference table: `docker network ls` appears in S10 and S15, `docker
   network inspect toynet` and `docker exec -it gateway sh` in S13, `docker compose logs -f gateway`
   and `docker compose exec gateway sh` in S16, each where it is useful.

Steps the README does not have (`git branch; git log`, `ls`, `mkdir secrets`, `grep`, `git diff`,
`which python`, `echo $…`, `docker inspect`, `docker images`, `docker image rm`, `git stash -u`,
`docker run --entrypoint ls …`, `docker ps --format …`, the `-p 8090:9100` / `8091` demo, the
`curl … :8090` after the move, `docker logs` in Step 3, `/etc/resolv.conf`) are marked `extra` in the
tracker caption and in the narration ("this one isn't in the README").

## Scene plan

### Part 1 — mega-pipeline, `flexible-workflow`

**S01 · Build or pull? Whose localhost? (~210 words).** Cold open on two real surprises, no
explanation yet. (a) `./docker-shell.sh run` in `generate_text` (`mega-laptop/76`, trimmed: lines
2–5, `…`, 15–16, 19–25): `Local image not found, using image from registry...`, `Python 3.8.17`,
`ImportError: cannot import name 'genai' from 'google'`. "The repo you cloned builds Python 3.14.
The image you just ran is Python 3.8, from February 2025." V1 teaser: the signpost and the sealed
box, a question mark. (b) port_toy: `curl --max-time 3 http://localhost:9200/health` → `curl: (7)`
(`port-laptop/23`), then `docker exec gateway curl http://processor:9200/health` → `ok` (`24`, the
meter lines cut to `…`). "The processor *is* listening on 9200. Your laptop can't reach it; the
other container can, by name." Two questions on screen: *Where did that image come from?* (part 1)
*Whose localhost is it?* (part 2). How to follow along (tracker shown once, code panels with
`path · lines`, ▶ your turn; every command is in the study guide in MLOps_Learning). What you need:
Tutorial 0, a GCP project with billing for part 1, only Docker for part 2. Honest limit, said once:
recorded on 14 October 2026 on a Linux laptop with Docker Engine 29.8.2 and Compose v5.6.0
(`port-laptop/00`, two lines), with no Google account and no key — wherever the code calls Google
you see the command, the real error a missing key gives, and what to look for.

**S02 · Same pipeline, built like a team (~220).** No commands. `README.md:58-65` as a four-row
morph, L03 → L04: a shared bucket → your own bucket; one shared key copied into five folders
(`mega-pipeline-main/README.md:97`) → your own service account, one key *outside* the repo; you
wrote each Dockerfile → `Dockerfile`, `pyproject.toml`, `uv.lock` committed for you; a `docker run`
typed from memory → `docker-shell.sh`. The five stages are the same and still never call each other:
they pass files through the bucket (`README.md:140-142`; a quick reprise of L3's five TEAL boxes over
BLUE drawers) — "how containers talk directly is part 2". V1 in full with `README.md:67-74`
("Two ways to work — and we support both"): build from the recipe or pull the frozen meal; the tag
is a signpost. End on the switchboard's silhouette: "one script decides which, and we'll read it."

**S03 · Get the code: clone, or switch branches (~280).** Tracker *Get the Code*. Starting fresh: ▶
`git clone --branch flexible-workflow https://github.com/dlops-io/mega-pipeline.git` (`mega-laptop/01`),
▶ `cd mega-pipeline` (`02`); extra `git branch; git log --oneline -1` (`03`: `* flexible-workflow`,
`cc67f3b`, the pinned commit), extra `ls; ls -a transcribe_audio` (`04`): `Dockerfile`,
`docker-shell.sh`, `pyproject.toml`, `uv.lock` are now in the repo. ▶ your turn. Already have L03's
clone: V2 first, with the real L03 state (`mega-l03-laptop/01`). ▶ `cd mega-pipeline` (`02`), ▶ `git
fetch origin` (`03`: prints nothing — your clone already had the branch), ▶ `git checkout
flexible-workflow` (`04`): both refusals, read slowly (the edited `cli.py`; the untracked
`generate_text/Dockerfile` and `uv.lock`). The README's note (`README.md:48`): ▶ `git stash` (`05`),
retry (`06`): the second refusal stays. Erratum, kindly: the note covers only edited files; extra
`git stash -u` (`07`) also stashes untracked files → ▶ `git checkout flexible-workflow` (`08`: `Switched
to a new branch`), ▶ `git branch` (`09`). `git checkout -- .` shown as a command only: it throws your
edits away and leaves untracked files where they are. V2 coda (extra `10`, `11`): the ignored L03
`Dockerfile` was replaced without a word (copy it out first if you want it); `transcribe_audio/secrets/`
still holds the old key — "the README says your secrets stay put (`README.md:50`); true, and it
matters in S09"; your L03 edits wait in `git stash list` (`10`, last two lines). ▶ your turn.

**S04 · Your bucket and your three values (~210).** Tracker *Before you run*. Step 1: the folder
layout (`README.md:107-117`) drawn as a tree; extra from `~/AC215`: `mkdir secrets; ls; ls -la secrets`
(`mega-laptop/06`): `mega-pipeline  secrets`, the folder empty — "your key goes here, beside the repo,
in S05". Step 2: the three values (`README.md:127-131`, panel). Extra `grep -n … */cli.py` (`07`):
blank in three files, filled in two. Erratum, kindly: `generate_text` and `translate_text` ship the
course's project and bucket and the instructor's group, and the `assert` only rejects an empty
string, so forgetting them sends your calls to resources you can't use (`README.md:133-134` promises
the assert stops you; it stops you only in the other three). The edit, as `git diff cli.py` (`11`):
the placeholders `your-project-id`, `your-team-bucket`, `group-01` — "type your own, in all five
files". ▶ your turn. Step 3: the bucket (`README.md:150-158`) as BLUE drawers with the seven
prefixes, each opening into `<group_name>/`. Erratum, kindly: the README gives no command to create
the bucket or to put audio in it; create it in the console (schematic, tagged `illustration`) and
upload a short recording named `input-<something>.mp3` (transcribe hands on only `input-*` files,
`transcribe_audio/cli.py:102`). GOLD tag: storage in your project (tiny).

**S05 · Three gates: account, role, API (~290).** Tracker *Service Account & Secrets*. V3 first:
"identity for your *code*" (`README.md:171`), the key, the token, the doors with locks and switches.
Steps 1–4 as a schematic console (tagged `illustration`, no logo, `README.md:175-182`): IAM & Admin ›
Service accounts › Create `mega-pipeline-sa`; the four roles appear one by one on V3's locks —
Storage Admin (all five), Agent Platform User (`generate_text`; search that name: "Vertex AI User"
finds nothing, and `generate_text/README.md:46` still says Vertex AI User — erratum, kindly), Cloud
Speech Client (`transcribe_audio`), Cloud Translation API User (`translate_text`); Text-to-Speech needs
none (`:185`). Keys › Add key › Create new key › JSON. Step 4: the GOLD key drops into the S04 folder
as `secrets/mega-pipeline.json` (`:183`). GOLD tag: "this file spends your project's money: never
commit it, never paste it anywhere". Steps 5–6, the APIs (`:187-199`): in the console (Library ›
Enable, illustration) or ▶ `gcloud config set project <your-project-id>` typed literally →
`-bash: syntax error near unexpected token 'newline'` (`gcloud-laptop/01`): the angle brackets are part
of the placeholder; with a value → `Updated property [core/project].` (`02`). ▶ `gcloud services enable
\ …` (`03`): our laptop has no account → `ERROR: … You do not currently have an active account
selected.` — that is Tutorial 0's `gcloud auth login`; with it, the five APIs are enabled (the README
shows no output). V3's switches flip. GOLD tag: calls to these APIs now bill your project.
PONDER 1 (8 s): "Your key is in place and every API is enabled, but you forgot Cloud Speech Client.
Where does transcribe fail — inside your container, or at Google?" Answer right after: at Google, as
a permission error; the key proved *who*, the role decides *may*. ▶ your turn.

**S06 · docker-shell.sh: one script, two windows (~310).** Tracker *How to Run a Component*. V4: read
the script once. Panel `transcribe_audio/docker-shell.sh · lines 6-14`: `IMAGE_NAME` (image name,
container name and registry name at once), `BASE_DIR` and `SECRETS_DIR` built from `$(pwd)` — so run
it from the component folder —, the in-container key path, `DOCKER_USERNAME="dlops"`, `BUILD_MODE`.
The `case` (`:28-46`) becomes the four tracks. V5 with panel `:92-96`: two `-v` windows and the
`-e` signpost; the venv outside both (`Dockerfile:17`, L3's reason). Concept done, then: `cd
transcribe_audio` (`transcribe_audio/README.md:15`), ▶ `./docker-shell.sh` (`mega-laptop/12`):
`Docker Username: dlops, Build Mode: dev-run`, `[2/5]` 44.7 s … `[5/5] RUN uv sync` 1.6 s, `Building
99.5s`, `Run Docker container...`, `Using local image...`, the prompt, `python cli.py --help` — identical
to `transcribe_audio/README.md:98-107`. One line from the full log (`12-a-docker-shell.plain.txt:1427`):
`Using CPython 3.14.8 interpreter at: /usr/local/bin/python3` — inside `>=3.14`, no download (L3
callback). Extras inside (`mega-transcribe_audio/03`, `05`, `06`): `which python` → `/home/app/.venv/bin/python`;
`echo $GOOGLE_APPLICATION_CREDENTIALS` → `/secrets/mega-pipeline.json`; `ls -la /secrets` → empty on this
machine (yours lists the key). Extra from a second terminal (`mega-laptop/14`): the two mounts, as V5
predicted. Say once: the id after `app@` changes every run. Step 5, ▶ `chmod +x docker-shell.sh` (`20`,
prints nothing) with extra `ls -l` (`19`: already `-rwxr-xr-x`): harmless, needed only if the bit got
lost (erratum, small). Step 6, Windows: Git BASH, and `winpty` in front if you see "the input device is
not a TTY" (`README.md:226`, text only). ▶ your turn.

**S07 · Five components, five honest errors (~320).** Tracker *Quick Reference* by component. A, in
the S06 container: ▶ `python cli.py --download` (`mega-transcribe_audio/09`: lines 2–3, `…`, the `cli.py,
line 39` frame (11–12), last line), tagged `recorded without a key`. V3 callback: gate 1 failed before
anything left the container. Three ways to get it: no key at `../../secrets/`, a different file name,
or the script run from another folder. ▶ `--transcribe`, ▶ `--upload`: commands only — "the same
error, for the same reason". With your key, what to look for (caption, citing `cli.py`): object names
printed, then `text_prompts/group-01/input-….txt` on your laptop and, after upload, in the bucket (V3
drawer lights, illustration). GOLD: Speech-to-Text bills per audio minute; use a short clip (this
branch keeps only the first chunk of a long transcript, `transcribe_audio/cli.py:84-86`; `main`'s
newer version joins them). B: `exit`, `cd ../generate_text`, ▶ `./docker-shell.sh` (`mega-laptop/31`:
its own apt layer, `Building 52.6s`), ▶ `python cli.py --help` (`mega-generate_text/01`, = README), ▶
`--download` (`02`, the same last line), ▶ `--generate` (`03`): `Args: …`, `generate`, nothing more.
PONDER 2 (6 s): "It exited with status 0. Did it call Gemini?" — No: nothing was downloaded, so there
was nothing to generate; exit 0 is not proof. ▶ `export GEMINI_MODEL=gemini-2.5-flash` + `python cli.py
--generate` (`05`): panel `generate_text/cli.py · lines 73-77` (the model comes from the env var, default
`gemini-2.5-flash-lite`). ▶ `--upload` command only. GOLD: Gemini bills per token. C: ▶ `./docker-shell.sh`
(`40`: `CACHED [2/5]`, `Building 8.2s` — B's apt layer reused) and `--help` before the edit →
`AssertionError: Update group name` (`40`, lines 29–33): the guard works where the value is blank.
After the edit (extra `41`, made on the laptop while the container runs: the window shows it at
once), `--help` (`mega-synthesis_audio_en/02`) → `DefaultCredentialsError` at `cli.py, line 23`: C, D
and E build their Google client at import, so even `--help` needs the key; with it, the README's
block (`expected/mega-synthesis_audio_en-help.txt`, tagged `expected`). ▶ `--download`, ▶ `--synthesis`
(commands); no upload: Text-to-Speech writes into the bucket itself (`README.md:257`). D and E as a
montage: ▶ `./docker-shell.sh` (`51`, `61`: `Building 7.9s`), `--help` fails at import (first frame,
last line), ▶ D `--download`, `--translate`, `--upload`; ▶ E `--download`, `--synthesis`. Erratum, kindly:
`translate_text/cli.py:64` targets `"es"` while the story and E's voice are French
(`synthesis_audio/cli.py:48-49`): change it to `"fr"`. One clause on the bonus: `cli_11.py` reads its
ElevenLabs key file relative to `/app`, not the `secrets/` folder the README names
(`mega-synthesis_audio/04`, last line). ▶ your turn (with your key).

**S08 · dev, run, and a stale image (~280).** Tracker *How to Run a Component* steps 2–3. V4's `dev`
track: ▶ `./docker-shell.sh dev` (`mega-laptop/17`): `Build Mode: dev`, every step `CACHED`, no
container. What it's for (component README *Python packages*, `transcribe_audio/README.md:89`): after
`uv add <package>` inside the container (command only; L3 showed why), `dev` bakes the change into the
image. ▶ `./docker-shell.sh run` (`18`): `Using local image...`, prompt, `exit`. Erratum, kindly:
`README.md:74` says `run` pulls from the registry; it uses any local image of that name first, however
old (`docker-shell.sh:83-85`), and pulls only when there is none. PONDER 3 (8 s): "A teammate has never
built this image. They type `./docker-shell.sh run`. Which Python do they get?" Extra `docker image rm
mega-pipeline-transcribe-audio` (`71`) stands in for that teammate. ▶ `./docker-shell.sh run` (`72`,
trimmed): `Local image not found, using image from registry...`, the pull, `Creating a Pipfile for this
project...`, `(app) root@36615ab6e34b:/app#`, `Python 3.8.17`, the pipenv `which python`; `--help` still
works here (old packages; Python 3.8's argparse says `optional arguments:`). Extra (`74`): created
`2025-02-18`, `PYTHON_VERSION=3.8.17`, `cmd ["-c","pipenv shell"]`, `user ""` — root. V1 payoff: built
from the older `pipenv-flexible-workflow` branch (panel
`mega-pipeline-pipenv-flexible-workflow/transcribe_audio/Dockerfile`, its `FROM` line), not from the
recipe you have; your folder slid over its `/app`. For `generate_text` that is S01's `ImportError`
(`76`). Extra (`73`): a `Pipfile` owned by root appeared in your folder (`?? Pipfile`); delete it. The
fix: build locally (the default or `dev`); use `run` for images *your team* pushed from this branch,
with your own `DOCKER_USERNAME`.

**S09 · prod, a stowaway key, and clean-up (~250).** Tracker *How to Run a Component* step 4 and
*Publish the container*. V4's `prod` track, panel `docker-shell.sh · lines 51-68`: remove and recreate
a builder named `multi-arch` (`--use` makes it current, and the script never switches back — `docker
buildx ls` shows which is current), then one `docker buildx build --platform linux/amd64,linux/arm64
--push`: one tag, two architectures (L2: a Mac pulls arm64, a cloud VM amd64). Before it: `docker login
-u <USER NAME> -p <ACCESS TOKEN>` (`transcribe_audio/README.md:129`, command only; L2: `-p` leaves the
token in your shell history) and your own `DOCKER_USERNAME` (`README.md:76`). `./docker-shell.sh prod`
is shown as a command, not run here (it needs a login and publishes an image). The stowaway: back in
the switched L03 clone, extra `./docker-shell.sh dev` (`mega-l03-laptop/12`), extra `docker run --rm
--entrypoint ls mega-pipeline-transcribe-audio -la /app /app/secrets` (`13`): `mega-pipeline.json`
inside the image (a stand-in file, tagged). V5 contrast: `COPY --chown=app:app . ./` (`Dockerfile:39`)
copies the build context; `/secrets` in `transcribe_audio/.gitignore:3` protects Git only; no branch has
a `.dockerignore`; `prod` would push it. Erratum, kindly: `README.md:203` ("makes that mistake
impossible") holds for Git, not for images. Fix (▶ your turn): delete the in-component `secrets/`
folders; add a `.dockerignore` with `secrets/` (L3 showed it); if a key was ever pushed, delete that
key in IAM. Clean-up card for part 1: `exit` each container (`--rm` removes it); local images, extra
`docker images` (`70`: 1.48 GB + four of ~830 MB) and any `dlops/*` you pulled (`78`), removed with
`docker image rm …` (`71` as the pattern); in the cloud, the bucket keeps billing storage until you
delete it when the course no longer needs it, and the key is a long-lived credential: delete it in the
console when you're done (illustration). GOLD tags. Close: "In part 2: containers that talk to each
other directly." Clean frame.

### Part 2 — port_toy

**S10 · Two little computers, one network (~230).** Bridge: part 1's containers only left files in a
bucket (`mega-pipeline/README.md:140-142`); port_toy makes two talk directly (`port_toy/README.md:5`,
`:52`). Only Docker is needed (`:24`). V6 first: each container is its own little computer, its own
`localhost`, its own ports; a user-defined network is a LAN with a phone book. Tracker
*Prerequisites*: ▶ `docker run hello-world` (`port-laptop/01`, trimmed to the pull lines, `Hello from
Docker!`, `…`). Tracker *Step 1* step 1: the README says "Clone or download"; the clone command (not
printed in the README) ▶ `git clone https://github.com/dlops-io/port_toy.git` (`02`), ▶ `cd port_toy`
(`03`); extra `ls -a; ls gateway processor; git log --oneline -1` (`04`: `d190c71`, the files of
`README.md:59-69`). Step 2: ▶ `docker network create toynet` (`05`: the network id) — V6's rail appears;
*Handy commands* ▶ `docker network ls` (`06`: `bridge`, `host`, `none`, `toynet`). ▶ your turn.

**S11 · Build, start, read the logs (~230).** Tracker *Step 1* steps 3–6. Panel
`gateway/Dockerfile · lines 1-5` (the processor's differs only in its last line): `python:3.14-slim`,
apt installs `curl`, `COPY . .`, `CMD ["python", "-u", …]` (`-u`: prints reach `docker logs` at once).
▶ `docker build -t toy-processor ./processor` (`07`: `[2/4] RUN apt-get …` 6.4 s, `Building 7.5s`), ▶
`docker build -t toy-gateway ./gateway` (`08`: `CACHED [2/4]`, `CACHED [3/4]`, `Building 0.3s` — the two
files are identical up to `COPY`, L2's cache). ▶ `docker run -d --name processor --network toynet \ -e
PORT=9200 toy-processor` (`10`: an id): no `-p` (`README.md:113`); panel `processor/processor.py · lines
42-45` (reads `PORT`, binds `""` = every interface *of its own box*). V7: ▶ the gateway's `docker run`
(`11`): `-p 127.0.0.1:8090:9100` lifts into *ip : host : container*; `-e PROCESSOR_HOST=processor -e
PROCESSOR_PORT=9200` is where the gateway will call (`gateway.py:13-14`). ▶ `docker logs processor`,
`docker logs gateway` (`12`, `13`): the two banners. ▶ your turn.

**S12 · Send a message: ports on the wire (~200).** Tracker *Step 1* step 7. Open
`http://localhost:8090`, type, Send (`README.md:147-149`): the page drawn (tagged `illustration`) and
filled with the captured reply (`14`): `HELLO FROM THE LAPTOP`; `gateway sent from port 55620`,
`processor listening on port 9200`, `processor saw it arrive from 55620`. The reply line itself in a
small strip tagged `captured reply (curl stands in for the Send button)` (`14`, line 2). V7's ticket:
the gateway's operating system picks a temporary source port for the outgoing connection; the
processor sees the same number because nothing rewrites it inside the network (`README.md:161-169`).
Panels: `gateway/gateway.py · lines 32-38` (connect *by name*; read the real source port) and
`processor/processor.py · lines 28-33`. Send again (`15`): `55634` — new connection, new ticket; your
numbers differ. The page learns the host port from its own address bar (`gateway/index.html · lines
86-89`): a container can't know which street door you gave it. ▶ your turn.

**S13 · Who can reach whom (~320).** Tracker *Step 2*. Step 1: ▶ `docker ps` (`16`, wrapped): the
gateway's `127.0.0.1:8090->9100/tcp`, the processor's empty PORTS — listening is not published
(`README.md:209-211`); extra, the README's three columns (`17`). Why `127.0.0.1` (`:232-244`), V7: extra
`docker run … -p 8090:9100 …` while 8090 is taken (`18`, last part): `Bind for 127.0.0.1:8090 failed: port is
already allocated` — host doors collide, container rooms never do; extra with 8091 (`20`, `21`):
`0.0.0.0:8091->9100/tcp`, a door onto every address. Step 2: ▶ `curl http://localhost:8090` (`22`,
first lines, `…`), ▶ `curl --max-time 3 http://localhost:9200/health` (`23`): no street door to 9200 (the
RED bounce; `:262`: unless something else of yours uses 9200). Step 3: ▶ `docker exec gateway curl
http://processor:9200/health` (`24`): `ok` through the rail, by name. PONDER 4 (6 s): "Same command with
`localhost` instead of `processor`. What answers?" ▶ (`25`): exit 7 — inside the gateway, `localhost` is
the gateway (`README.md:290`); extra `26`: `localhost:9100` there returns the gateway's own page. V6's
phone book: *Handy commands* ▶ `docker network inspect toynet` (`28`: lines 16, 32, 35, 39, 42: subnet,
the two names and addresses), extra (`29`): `nameserver 127.0.0.11`, `getent hosts` → both names. Names survive
restarts; addresses may not. ▶ `docker exec -it gateway sh` (`29b`: `hostname`, `ls`, `exit`). One clause:
the README says the processor image doesn't need curl — it has it anyway (`27`). ▶ your turn.

**S14 · Change the ports (~310).** Tracker *Step 3*. V7's slider. Step 1: ▶ `docker rm -f gateway`
(`30`), ▶ the run with `-p 127.0.0.1:8095:9100` (`31`); the page on 8095 works (`32`), extra `curl
--max-time 3 http://localhost:8090` refused (`33`), extra PORTS `127.0.0.1:8095->9100/tcp` (`35`). Room
9100 didn't move; why you'd do this: something else holds 8090 (`README.md:357-363`). Erratum, kindly:
`docker logs gateway` still says `open http://localhost:8090` (`34`) — a fixed string
(`gateway.py:53`); trust `docker ps` and the page's diagram. Step 2: ▶ `docker rm -f processor` (`36`), ▶
the run with `-e PORT=9300` (`37`). "Send a message. It should fail." (`:380`) The gateway's arrow still
aims at 9200, RED. Real (`38`): the page's request gets `curl: (52) Empty reply from server` — on the
page, nothing changes (no error handling, `index.html:95-100`; erratum, kindly). Where the error is:
extra `docker logs gateway` (`39`: first 3 lines, `…`, `File "/app/gateway.py", line 34`, the last line
`ConnectionRefusedError: [Errno 111] Connection refused`): the name resolved, nobody listens on 9200
(cheat sheet `:551-552`; a wrong name would say "could not resolve host" instead — exercises).
PONDER 5 (6 s): "Which one setting fixes it, and does any image need rebuilding?" Step 3: ▶ `docker rm
-f gateway` (`41`), ▶ the run with `-e PROCESSOR_PORT=9300`, back on 8090 (`42`); the page works,
`processor listening on port 9300` (`43`): the two settings must agree; configuration, no rebuild
(`:404-409`). Step 4: ▶ `docker rm -f gateway processor` (`44`), ▶ `docker network rm toynet` (`45`);
extra (`46`): nothing left but hello-world's exited container. Why now: Compose will want these exact
names (one line from `68`: `Conflict. The container name "/processor" is already in use`). ▶ your turn.

**S15 · Compose: the same app, declared (~300).** Tracker *Step 4*. V8 first, with panels
`docker-compose.yml · lines 11-25` and `· lines 27-39` (`README.md:432-444` shows an excerpt; open the
whole file). ▶ `docker compose up` (`47`): the build view (cut to `Building 0.3s`, `CACHED` steps,
`naming to docker.io/library/port_toy-processor` and `…-gateway` — Compose names images
`<folder>-<service>`), `[+] up 5/5` (two images, network `toynet`, two containers), `Attaching to
gateway, processor`, the two banners prefixed by service. A second terminal: ▶ `docker compose ps`
(`48`, wrapped, PORTS highlighted), the page works (`49`, illustration + strip), extra `docker network
ls` (`50`: Compose made `toynet`), ▶ `docker compose exec gateway curl http://processor:9200/health`
(`51`: just `ok` — `compose exec` gives curl a terminal, so no meter). The README's comparison table
(`:478-484`) as a two-column card. Back in the first terminal the request lines have appeared (`47`,
lines 52–54). ▶ `Ctrl+C` (`47`, last lines): `Gracefully Stopping...`, `gateway exited with code 137`,
`processor exited with code 137`, about 20 seconds: Python as PID 1 ignores the polite stop signal,
Docker waits 10 s, then kills (137 = killed), gateway first, then processor. ▶ `docker compose ps -a`
(`52`): both `Exited (137)`, still there. ▶ `docker compose down` (`53`): two containers and the network
removed; ▶ `docker compose ps -a` (`54`): empty. "`Ctrl+C` stops; `down` removes" (`:517-529`). ▶ your
turn.

**S16 · Edit, apply, tear down, recap (~260).** Tracker *Step 4* steps 3–5, *Handy commands*. ▶
`docker compose up -d` (`55`: `[+] up 3/3`, back to your prompt). Step 3 "repeat the port experiments"
(`:487`): extra edit `8090` → `8095` (`57`, the diff line), ▶ `docker compose up -d` (`58`): `Container
processor Running`, `Container gateway Started 10.5s` — Compose recreated only what changed (V8 coda);
the page on 8095 works (`59`); the edit undone and `up -d` again (`60`). Step 4: extra one-line edit to
`processor.py` (`61`), ▶ `docker compose up -d --build` (`62`): only `[processor 4/4] COPY` is new, the
processor is recreated, the gateway keeps `Running`; the gateway's folder is mounted (`volumes:`), so
an `index.html` edit shows on the next page load without a rebuild (`gateway.py:20`). *Handy commands*:
▶ `docker compose logs -f gateway` (`56b`: the banner and a `POST` line, `^C`), ▶ `docker compose exec
gateway sh` (`56d`: `echo $PROCESSOR_HOST $PROCESSOR_PORT` → `processor 9200`). Step 5: ▶ `docker compose
down` (`64`: `Removed 10.2s` each), ▶ `docker compose ps -a` (`65`): empty; extra `docker image ls` (`66`):
"the built images remain" (`:515`) — `port_toy-*` and `toy-*`, 198 MB each; `docker image rm` them if
you want the space. Nothing in port_toy costs money. Recap questions (5, on screen one at a time,
answers in exercises.md): (1) which files define a mega-pipeline image, and what does `run` use when
there's no local image; (2) the three gates a call to your bucket must pass, and where each one fails;
(3) how a git-ignored key ends up in an image, and the fix; (4) in `-p 127.0.0.1:8095:9100`, which
number the browser uses, which `gateway.py` binds, and what `127.0.0.1` restricts; (5) inside the
gateway, what `localhost` is and which name reaches the processor. Next (L05, `llm-rag`): a CLI
container calls a ChromaDB container by name on a Compose network, with the same `../secrets`
mount — parts 1 and 2 together (GREY dashed teaser). Study guide and exercises in MLOps_Learning.
Clean frame.

## Ponder questions (summary)

| # | scene | question | answer (said right after the timer) |
| --- | --- | --- | --- |
| 1 | S05 | Key in place, APIs enabled, Cloud Speech Client forgotten: where does transcribe fail? | at Google, as a permission error: the key proved who; the role decides what it may do |
| 2 | S07 | `--generate` exited with status 0: did it call Gemini? | no: `--download` had failed, so there was nothing to generate (`mega-generate_text/03`) |
| 3 | S08 | A teammate never built the image and types `./docker-shell.sh run`: which Python? | whatever `dlops/…:latest` holds: Python 3.8.17 from 2025-02-18 (`72`, `74`) |
| 4 | S13 | `docker exec gateway curl … http://localhost:9200/health`: what answers? | nothing: inside the gateway, `localhost` is the gateway (`25`, `26`) |
| 5 | S14 | Processor on 9300, gateway calling 9200: which setting fixes it, and is a rebuild needed? | the gateway's `PROCESSOR_PORT=9300`; no rebuild: it's configuration (`42`, `43`) |

## Errata to state (kindly, with the fix)

1. **`run` prefers any local image, and otherwise pulls a 2025 image** (`README.md:74`, `:214` vs
   `docker-shell.sh:83-88`; real `18`, `72`, `74`, `76`): `dlops/mega-pipeline-*:latest` is a Python
   3.8.17 / pipenv / root build from the `pipenv-flexible-workflow` branch, and it writes a root-owned
   `Pipfile` into your folder → build locally; use `run` only for images your team pushed from this
   branch, with your own `DOCKER_USERNAME` (S08; teased in S01).
2. **The branch switch refuses twice** (`README.md:48` covers only edited files; real
   `mega-l03-laptop/04`, `06`) → `git stash -u` (S03).
3. **Ignored L03 files are replaced without a word** (`mega-l03-laptop/11`) → copy your L03
   `Dockerfile` out first if you want it (S03).
4. **"Your secrets stay put"** (`README.md:50`) — and so does L03's key inside `transcribe_audio/secrets/`,
   which `dev` copies into the image (`mega-l03-laptop/13`); `README.md:203` holds for Git only →
   delete in-component `secrets/`, add `.dockerignore`, revoke any key that was pushed (S09).
5. **Two `cli.py` files ship the course's project and bucket and the instructor's group**, and the
   `assert` only rejects `""` (`README.md:133-134` vs `mega-laptop/07`); the component READMEs show yet
   another set of defaults (`transcribe_audio/README.md:51-53`) → set all three values in all five
   files (S04).
6. **No command creates the bucket or fills `input_audios/`** → create it in the console; name the
   audio `input-<something>.mp3` (S04).
7. **"Vertex AI User"** in `generate_text/README.md:46` → search "Agent Platform User"
   (`README.md:179`) (S05).
8. **Spanish text, French voice**: `translate_text/cli.py:64` targets `"es"` while the README and
   `synthesis_audio/cli.py:48-49` are French → set `"fr"` (S07).
9. **Long recordings are cut to their first chunk** (`transcribe_audio/cli.py:84-86`; `main` joins
   them) → use a short clip (S07, one clause).
10. **The ElevenLabs key file is read relative to `/app`** (`cli_11.py:30-33`, real
    `mega-synthesis_audio/04`), not from the `secrets/` folder the README names (S07, one clause).
11. **`chmod +x` is not needed after a clone** (`mega-laptop/05`, `19`) — harmless (S06).
12. **The gateway banner always says 8090** (`gateway.py:53`; real `34`) → trust `docker ps` and the
    page (S14).
13. **"It should fail" — but the page just doesn't update** (`index.html:95-100`; real `38`) → watch
    `docker logs gateway` (`39`) (S14).
14. **The processor image has curl** although `README.md:294` implies it doesn't need it (real `27`) —
    one clause (S13).

Gotcha, not an erratum: `<your-project-id>` is a placeholder, angle brackets included
(`gcloud-laptop/01`) (S05).

Not on screen (exercises or study guide only): `LINEAR16` audio saved as `.mp3`; the `prod` builder
left selected and its effect on later builds (inferred, not run); `cli_11.py`'s hard-coded bucket and
group; the course-site schedule mismatch (E17).

## Costs and teardown

- **Your own project pays now.** Speech-to-Text (per audio minute), Gemini on Vertex AI (per token),
  Translation and Text-to-Speech (per character), and bucket storage (tiny). GOLD tags in S04
  (bucket), S05 (enabling APIs; the key spends your money) and on each component's calls in S07.
  Nothing here was billed: the recording had no account.
- **The key** is a long-lived credential: never commit, paste or bake it in (S05, S09); delete it in
  the console when the course is over; revoke at once if it was ever pushed.
- **Part 1 teardown (S09 card):** `exit` each container (`--rm` deletes it); remove local images
  (`mega-laptop/70`: 1.48 GB + four of ~830 MB; `78`: any `dlops/*` you pulled), pattern `71`; delete
  the stray root-owned `Pipfile` if you ran the fallback (`73`); the bucket keeps billing storage until
  you delete it when the course no longer needs it; Docker Hub repos you pushed are public by default.
- **Part 2 teardown (S16):** `docker compose down` (README), `docker compose ps -a` empty; the images
  remain (`66`, 198 MB each): `docker image rm` if you want the space. port_toy costs nothing.

## README commands checklist (for the follow-along review)

**mega-pipeline (`flexible-workflow`)**

| README command | where | scene (capture) |
| --- | --- | --- |
| `git clone --branch flexible-workflow https://github.com/dlops-io/mega-pipeline.git`, `cd mega-pipeline` | `README.md:35-36` | S03 (`mega-laptop/01`, `02`) |
| `cd mega-pipeline`, `git fetch origin`, `git checkout flexible-workflow`, `git branch` | `:42-45` | S03 (`mega-l03-laptop/02`–`09`) |
| `git stash` / `git checkout -- .` | `:48` | S03 (`05`; the second as a command only) |
| `gcloud config set project <your-project-id>` | `:192` | S05 (`gcloud-laptop/01`, `02`) |
| `gcloud services enable \ …` (five services) | `:193-198` | S05 (`03`) |
| `./docker-shell.sh` | `:212`; component READMEs `:65` | S06 (`12`), S07 (`31`, `40`, `51`, `61`) |
| `./docker-shell.sh dev` | `:213` | S08 (`17`), S09 (`mega-l03-laptop/12`) |
| `./docker-shell.sh run` | `:214` | S08 (`18`, `72`), S01 (`76`) |
| `./docker-shell.sh prod` | `:215` | S09 (command only) |
| `chmod +x docker-shell.sh` | `:223` | S06 (`20`) |
| `winpty` | `:226`, `:380` | S06 (text only) |
| `python cli.py --help` | component READMEs (`transcribe_audio/README.md:98` …) | S06 (`12`), S07 (`mega-generate_text/01`, `40`, `mega-synthesis_audio_en/02`, `51`, `61`; `expected/` for C–E with a key) |
| A: `python cli.py --download / --transcribe / --upload` | `README.md:237-239` | S07 (`mega-transcribe_audio/09`; the other two command only) |
| B: `--download / --generate / --upload` | `:245-247` | S07 (`02`, `03`; upload command only) |
| `export GEMINI_MODEL=gemini-2.5-flash`, `python cli.py --generate` | `generate_text/README.md:92-93` | S07 (`05`) |
| C: `--download / --synthesis` | `README.md:253-254` | S07 (command only) |
| D: `--download / --translate / --upload` | `:262-264` | S07 (command only) |
| E: `--download / --synthesis` | `:270-271` | S07 (command only) |
| `uv add <package>` | `transcribe_audio/README.md:89` and peers | S08 (command only) |
| `docker login -u <USER NAME> -p <ACCESS TOKEN>` | `transcribe_audio/README.md:129` and peers | S09 (command only) |

**port_toy**

| README command | where | scene (capture) |
| --- | --- | --- |
| `docker run hello-world` | `README.md:29` | S10 (`01`) |
| "Clone or download" → `git clone https://github.com/dlops-io/port_toy.git`; `cd port_toy` | `:81`, `:84` | S10 (`02`, `03`) |
| `docker network create toynet` | `:92` | S10 (`05`) |
| `docker build -t toy-processor ./processor`, `docker build -t toy-gateway ./gateway` | `:100-101` | S11 (`07`, `08`) |
| `docker run -d --name processor --network toynet \ -e PORT=9200 toy-processor` | `:109-110` | S11 (`10`) |
| `docker run -d --name gateway --network toynet \ -p 127.0.0.1:8090:9100 \ …` | `:120-124` | S11 (`11`) |
| `docker logs processor`, `docker logs gateway` | `:132-133` | S11 (`12`, `13`) |
| browser: open `localhost:8090`, Send | `:147-149` | S12 (`14`, `15`: illustration + captured reply) |
| `docker ps` | `:198` | S13 (`16`; `17` extra) |
| `curl http://localhost:8090`; `curl --max-time 3 http://localhost:9200/health` | `:251`, `:259` | S13 (`22`, `23`) |
| `docker exec gateway curl http://processor:9200/health`; the same with `localhost` | `:273`, `:285` | S13 (`24`, `25`) |
| `docker rm -f gateway`; gateway on `8095`; open `localhost:8095` | `:340`, `:346-350`, `:353` | S14 (`30`, `31`, `32`) |
| `docker rm -f processor`; processor on `9300`; send (should fail) | `:370`, `:376-377`, `:380` | S14 (`36`, `37`, `38`) |
| `docker rm -f gateway`; gateway with `PROCESSOR_PORT=9300`; send | `:389`, `:395-399`, `:402` | S14 (`41`, `42`, `43`) |
| `docker rm -f gateway processor`, `docker network rm toynet` | `:416-417` | S14 (`44`, `45`) |
| `docker compose up`; open `localhost:8090` | `:455`, `:460` | S15 (`47`, `49`) |
| `docker compose ps`, `docker compose exec gateway curl ...` | `:480-481` | S15 (`48`, `51`) |
| `Ctrl+C`, `docker compose down`, `docker compose ps -a` | `:507`, `:512`, `:524` | S15 (`47` tail, `53`, `52`, `54`); S16 (`64`, `65`) |
| `docker compose up -d`; `docker compose up -d --build` | `:492`, `:500` | S16 (`55`, `58`, `60`; `62`) |
| Handy: `docker exec -it gateway sh` | `:566` | S13 (`29b`) |
| Handy: `docker compose logs -f gateway`, `docker compose exec gateway sh` | `:572-573` | S16 (`56b`, `56d`) |
| Handy: `docker network ls`, `docker network inspect toynet` | `:575-576` | S10 (`06`), S15 (`50`); S13 (`28`) |

## Things never to do on screen

Series rules:
- No Google/GCP logos or console screenshots: schematic drawings tagged `illustration` (service
  account form, roles, keys, API library, bucket, Docker Hub shelf, the port_toy page). Never show
  `mega-pipeline-bucket.png`, `mega-pipeline-flow.png` or `browser-gateway-processor.png`; redraw.
- No real person's name in captions, labels or narration: the prompt user is `student`; narration
  says "the instructor" and "the instructor's group name". Never quote `mega-pipeline/README.md:9`,
  `:15`, `:158`, `synthesis_audio/README.md:125-127` or `generate_text/cli.py:65-72` (the prompt names
  the host): quote `:73-77`. The instructor's group name appears only inside unchanged source or diff
  lines the viewer must find and edit (`mega-laptop/07`, `11`, `30`, `41`, `50`).
- No hand-typed output: every terminal line comes from `assets/terminal/`; `expected/` panels carry
  the `expected` tag; "what to look for" is a caption citing `cli.py` lines, never styled as output.
- No command spelled differently from the README. Commands the README implies but doesn't print
  (`git clone …port_toy.git`, `cd transcribe_audio`) are said as such.
- No credentials, keys, tokens or real-looking project ids: placeholders only (`your-project-id`,
  `your-team-bucket`, `<USER NAME>`, `<ACCESS TOKEN>`); never draw a key's content or `cat` the
  79-byte stand-in. The course's project and bucket names appear only inside quoted lines the viewer
  must edit, never in captions, labels or narration.

Lecture-specific:
- Never show the capture's plumbing: the stand-in laptop, `--network host`, `proxy_relay.py`,
  `mirror.gcr.io`, the CA variables, the rebuilt base images' digests (`@sha256:d86a6f2…`,
  `dcc61fa5…`) and `[1/5] FROM` / `[1/4] FROM` lines, `https://deb.debian.org` apt lines from the
  `.plain.txt` logs, gcloud's `[component_manager]` / `disable_usage_reporting` lines.
- Never type the browser stand-in (`curl -sS -X POST …`) as a README step: the step is the browser;
  draw the page (`illustration`) and show the reply line as "captured reply".
- Never present a Google call as if it succeeded: no output panel for a working `--download`,
  `--transcribe`, `--upload`, `--generate`, `--synthesis` or `--translate`; no audio is played.
- Never show `./docker-shell.sh prod` or `docker login` as if they ran; never present pushing an
  image that contains a key as something to do.
- Never present the ElevenLabs bonus's voice model as something to use: one clause only.

## Left for exercises.md (not in the video)

A second `./docker-shell.sh` of the same component → rebuild + `Conflict` (`mega-laptop/15`, G9);
`-e GEMINI_MODEL` in `docker-shell.sh`; `uv add` then `run` without a rebuild; what `prod` would
publish from an L03 folder (`mega-l03-laptop/13`); recovering L03 edits with `git stash pop`;
`EXPOSE` is not publish; two containers on the same container port; the processor without
`--network` (`port-laptop/70`–`73`: `Could not resolve host: processor`, `socket.gaierror`); binding
`127.0.0.1` inside a container; Compose after the by-hand steps (`67`–`69c`: the container
`Conflict`, the leftover network only warned about and left behind by `down`); `LINEAR16` saved as
`.mp3`; the `multi-arch` builder left selected; Linux hosts whose uid isn't 1000; Git BASH path
conversion (`MSYS_NO_PATHCONV=1`).
