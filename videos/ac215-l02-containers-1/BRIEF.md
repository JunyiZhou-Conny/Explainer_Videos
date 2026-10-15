# Brief · AC215 L2 — Containers I: one image, from laptop to VM

The design of this video, written before the script. Series rules: `docs/AC215_SERIES.md`.
Facts: `digest.md` (the verified tutorial digest) and `assets/` (real captures, see `ASSETS.md`).
**Where the digest and the captures disagree, the captures win.** They are newer (2026-10-13,
01:43-02:00 UTC) and were made by running the README's commands as written:

| topic | digest | captures (use these) |
| --- | --- | --- |
| final image in `docker image ls` | `DISK USAGE 517MB` | `518MB` disk / `144MB` content (`laptop/30`) |
| layer sizes of a fresh build | 111 MB / 0.5 MB / 127 MB on a ~141 MB base | `docker history`: `uv sync` 125MB, `COPY . ./` 250kB, apt/pip/uv `RUN` 97.5MB; base rows 85.3MB, 9.7MB, 54.5MB, 16.4kB (`laptop/34`) |
| published image on the VM | "7 layers, ~146 MB compressed" | 7 `Pull complete`, `347MB` in `docker images` (`vm-debian12/06`, `07`); history 114MB / 209kB / 108MB on a `PYTHON_VERSION=3.12.14` base (`vm-debian12/09`) |
| the Step 2 prompt | `root@e8c2e6d6e51d:/#` | `root@f72851da4a58:/#` (`laptop/16`); every container prompt comes from its own capture |
| `sudo apt install docker.io` on the VM | "may need `apt-get update`" | **fails** on fresh Debian 12 and 13: `Unable to locate package docker.io`, exit 100 (`vm-debian1{2,3}/01`) |
| Docker on the VM | package candidates only | installed and run: `20.10.24+dfsg1, build 297e128` (Debian 12), `26.1.5+dfsg1, build a72d7cd` (Debian 13) (`04`) |
| Apple Silicon errors (`no matching manifest…`, `exec format error` on the VM) | *expected* wording | **not captured**: described in narration only, never as a terminal panel; the real reverse case is `laptop-push/12` |
| `Mounted from library/python` on push | *expected* | not reproducible here (no account): narration only |
| restoring `cli.py` with `git checkout` | not covered | the cache does **not** come back: `.git/index` changed and is copied too (`laptop/41`) |
| translation | might be refused or silently untranslated | translated every time: `Buen día`, `Adoro il formaggio`, `j'adore le fromage` |

## Audience and goal

An AC215 student who has done L1 (a Compute Engine VM, venvs, uv, `pyproject.toml`) and Tutorial 0
(Docker Desktop running, VS Code, git, a GCP project with billing). They have never written a
Dockerfile or thought about what an image is. They watch with the README of
[dlops-io/simple-translate](https://github.com/dlops-io/simple-translate) open, a clone on their
**laptop**, a free Docker Hub account, and (for the last part) a VM of their own, pausing to type
each command.

After the video they can:
- check and clean their Docker setup (`docker container ls`, `docker system prune`,
  `docker image ls`) and say what `prune` does and does not remove;
- write the README's five-step Dockerfile and say, for each line, whether it adds a layer or only
  writes on the image's config;
- build with `docker build -t simple-translate -f Dockerfile .` and read the build log (steps,
  `CACHED`, `naming to …`), including what the final `.` sends to the builder;
- predict what a container starts with from ENTRYPOINT + CMD, and explain why
  `docker run --rm -ti simple-translate python cli.py` fails with exit 126;
- explain why a `python:3.12` image runs Python 3.15 (3.14 in the instructor's image), and which
  `python` is which inside it;
- run the app in a container, and say what `--rm`, `-t`, `-i` and `exit` do to it;
- predict which build steps a rebuild re-runs, and how a reordered Dockerfile and a `.dockerignore`
  keep `uv sync` cached;
- tag and push to Docker Hub with a token (not on the command line), and read `push access denied`;
- check an image's platform, and make an image built on an Apple Silicon Mac run on a default
  (amd64) VM;
- deploy the app on a fresh VM that has only Docker (with `apt-get update` first), then delete it.

## Length and parts

~29–31 minutes. Narration 3,900–4,300 words (Kokoro af_heart, speed 0.9 ≈ 174 wpm); the plan below
totals **~4,170** (L1: 4,287 words gave 29:52). Word budgets per scene are targets (±15 %).

- **Part 1 = S01–S09** (~2,290 words, ~16 min): what an image is, then the README's Dockerfile in
  five steps with a build and a run after each, the solution, the final build, the run.
- **Part 2 = S10–S16** (~1,880 words, ~13 min): what's inside the image, the layer cache, Docker
  Hub, CPU platforms, the VM deploy, teardown.

The cut is the README's own seam: part 1 ends where *developing* ends (tracker A16, `exit`, the
container gone, the image built), with one question parked for part 2 ("why did `uv sync` run
again when we only added a line?"). Part 2 is *shipping* it.

## Colours (series table, applied)

| meaning | colour |
| --- | --- |
| your laptop: the clone, the files `COPY . ./` brings in, Docker Desktop's hidden Linux VM (dashed) | GREY |
| the cloud: the GCP VM `ac215-l02`, Docker Hub (a registry shelf), Google's translate endpoint | BLUE |
| images and containers: every layer's outline, the config card with its ENTRYPOINT/CMD tiles, image IDs and names, the container's thin writable layer (dashed, glowing) | TEAL |
| OS-owned inside the image: the Debian bookworm base, apt, the base image's Python 3.12.15 at `/usr/local/bin/python` | ORANGE |
| project-owned: `/.venv`, `uv.lock`, the CPython 3.15.0 that uv downloaded for the venv, the `>=3.13` interval | GREEN |
| tools: docker (the CLI, dockerd, BuildKit/buildx), uv, Debian's `docker.io` package | PURPLE |
| errors and "avoid this": `ModuleNotFoundError`, exit 126, `push access denied`, `exec format error`, `Unable to locate package`, `toomanyrequests`, the cache's rebuild wave | RED |
| your turn, the README tracker, "look here now" | YELLOW |
| money: the VM's cost tag and meter | GOLD |
| lookups and routes: the PATH lookup of `python`, the build context's trip to the builder, push and pull routes, the HTTPS call to Google | PINK |
| a future thing (L3: five containers, bind mounts) | GREY, dashed |

Layer slabs always have a **TEAL outline** (they are part of an image) and a **fill coloured by
what they hold**: ORANGE for the base and the apt/pip `RUN`, GREY for the `COPY` of your files,
GREEN for the `uv sync` layer (the venv and its Python). This matches L3's slab picture. CPU
platforms are coloured by the machine they belong to: `arm64 · Apple Silicon` GREY (a laptop),
`amd64 · default GCP VM` BLUE.

## Running example

- **The laptop** (the captures' fresh Docker 29.8.2 engine standing in for Docker Desktop): user
  `student`, host `laptop`: `student@laptop:~$`, after `cd` `student@laptop:~/simple-translate$`.
  Terminal title `laptop`. Say once (S03): on a Mac the prompt looks different (zsh, `%`); the
  commands are the same. Say once (S04): Docker Desktop's build log names its builder
  `desktop-linux` where ours says `default`.
- **Containers**: the prompt is part of each capture (`root@f72851da4a58:/#` …). Say once (S05)
  that the part after `root@` is the container's ID and changes every run.
- **Docker Hub**: the README's `<USER NAME>` is `student` in the captures. The README line is shown
  with its placeholders; the terminal types the capture's `$` line, with a YELLOW caption
  "`<USER NAME>` = your Docker Hub username (here: student)".
- **The VM** (fresh `debian:12` / `debian:13` containers standing in, as in L1): `ac215-l02`,
  prompt `student@ac215-l02:~$`, terminal title `ssh · ac215-l02`. Debian 13 is shown as the
  alternative where it changes the output (`Error:` vs `E:`, Docker 26.1.5 vs 20.10.24, 91 vs 92
  packages).
- **Builds**: the step-by-step builds (`laptop/09`–`24`, `38`, `40`, `41`) were captured without a
  terminal, so they are BuildKit's plain log. Say once (S04): "your terminal draws this as a
  compact view that updates in place; this is the same build written out in full — add
  `--progress=plain` to get it". The final build (`laptop/29`) is the compact view.

## Visual set pieces (the 3Blue1Brown part)

- **V1 · The ladder and the nesting dolls (S01, S16).** The README's four rungs (`README.md:9-16`):
  manual install (ORANGE), uv on a VM (GREEN), Docker on your laptop (TEAL in a GREY laptop),
  Docker on a VM (TEAL in a BLUE VM). In S01 rungs 1–2 are lit softly with an "L1" tag, then rungs
  3–4 light up: today. In S16 L1's closing picture returns: a BLUE VM box containing a GREEN
  venv, with the dashed box "container · L2" between them. The dashed box solidifies TEAL, and the
  venv slides into it at `/.venv`. Then the route of the whole lecture draws left to right: GREY
  laptop (build) → PINK route → BLUE Docker Hub shelf → PINK route → BLUE VM (run).
- **V2 · The layer stack (S02 intro; S04–S08 grow it; S09 container; S10 real sizes; S12, S15
  push and pull).** Translucent slabs stacked bottom-up, each labelled with its Dockerfile line.
  Beside the stack, a TEAL **config card** (ENV, ENTRYPOINT, CMD, WorkingDir) that never adds a
  slab. S04: four thin ORANGE slabs drop as one group ("python:3.12-slim-bookworm · Debian 12 +
  Python 3.12", with the four download sizes from `laptop/09`: 3.34MB, 15.97MB, 28.25MB, 249B);
  the card shows `CMD ["python3"]`, inherited. S05: ENTRYPOINT is written on the card, no slab
  ("config-only: nothing downloaded"). S06: a `RUN pip install uv` slab (ORANGE, a PURPLE `uv` chip
  inside) and a `COPY . ./` slab (GREY, file glyphs incl. `.git/` and `Dockerfile`). S07: a fat
  GREEN `RUN uv sync` slab ("CPython 3.15.0 + /.venv, 11 packages"). S09: `docker run` makes a
  **container**: the same stack (shared, not copied) plus a dashed glowing TEAL glass slab on top
  and a process dot "PID 1 · bash". `exit` puts the dot out; `--rm` dissolves the glass slab; the
  stack below is untouched. S10: the slabs rescale to the real `docker history` sizes
  (`laptop/34`: 125MB, 250kB, 97.5MB, 0B rows on the card; base 85.3MB + 9.7MB + 54.5MB + 16.4kB —
  downloads are compressed, history shows unpacked sizes).
- **V3 · The start-up command line (S04, S05, S08, S09).** On the config card two slots,
  ENTRYPOINT `[ ]` and CMD `[ ]`; below them the command line the container will run, assembled in
  mono. S04: ENTRYPOINT empty, CMD tile `["python3"]` (inherited, from `laptop/10`) → `python3` →
  the REPL. S05: `["/bin/bash"]` drops into ENTRYPOINT and the inherited CMD tile falls away
  (`laptop/15`: `Cmd=null`) → `/bin/bash` → a bare prompt. S08: the CMD tile
  `["-c", "source .venv/bin/activate && exec bash"]` slides in → `/bin/bash -c "source
  .venv/bin/activate && exec bash"`; the first bash puts the PINK `/.venv/bin` door at the front of
  PATH (L1's doors, miniature), then `exec bash` morphs that bash into a fresh interactive one that
  keeps the doors. S09: a WHITE tile `python cli.py` arrives from the end of the `docker run` line
  and knocks the CMD tile out → `/bin/bash python cli.py` flashes RED: bash reads `python` as the
  name of a *script*, walks PATH (no venv door now) to `/usr/local/bin/python`, finds a binary, and
  refuses (exit 126). Then a tile `-c "source .venv/bin/activate && python cli.py -d fr"` replaces
  CMD and the line works.
- **V4 · Two Pythons in one image (S07; coda in S10 and S15).** L1's number line (3.10 … 3.16), the
  interval `>= 3.13` glowing GREEN (from `pyproject.toml:6`). An ORANGE dot
  `3.12.15 · /usr/local/bin/python` (the base image's) lands outside it with a RED cross. A PURPLE
  arrow from uv drops a GREEN dot `3.15.0 · uv-managed · 35.9 MiB download` into the interval
  ("the newest uv knew, at the time of recording"); `/.venv/bin/python` draws a symlink arrow to
  it. Then PATH: without activation, `python` knocks on `/usr/local/bin` first (the base image's
  `ENV PATH=/usr/local/bin:…`, `laptop/34:22`) → 3.12 → `ModuleNotFoundError`; after
  `source .venv/bin/activate` the GREEN `/.venv/bin` door slides in front → 3.15.0 → works. S15
  coda: a second GREEN dot `3.14.7 · dlops/simple-translate · built 2026-09-16 · uv 0.12.15` lands in
  the same interval: same Dockerfile, a month earlier, a different Python.
- **V5 · The build context and the cache (S06 seed, S11 full).** S06: the project folder (GREY)
  with its files, `.git/` and `Dockerfile` among them. The `.` at the end of the build command
  lights up PINK; the whole folder packs into a parcel labelled "build context" and slides to a
  PURPLE "builder" box; `COPY . ./` unpacks all of it into `/` (no WORKDIR). There is no
  `.dockerignore` sieve (the log's real line `load .dockerignore … transferring context: 2B`).
  S11: the four steps as boxes in a row, `[1/4] FROM` · `[2/4] RUN apt…uv` · `[3/4] COPY . ./` ·
  `[4/4] RUN uv sync`, each with a small fingerprint badge (parent + instruction; for COPY, a
  checksum of the parcel). Unchanged rebuild: every badge matches, every box gets a TEAL `CACHED`
  stamp. Edit `cli.py`: the parcel's fingerprint changes, COPY's badge turns RED, and a RED wave
  knocks over COPY and `uv sync` like dominoes (a PURPLE "35.9 MiB" download arrow fires again);
  the boxes to the left keep `CACHED`. `git checkout` puts `cli.py` back, but a `.git/index` glyph
  inside the parcel changed: the badge stays RED and the wave runs again. The fix animates: the
  boxes reorder to `COPY pyproject.toml` → `RUN uv sync` → `COPY . ./`, a `.dockerignore` sieve
  catches `.git/` and `Dockerfile`; edit `cli.py` and the wave only reaches the last box. Tag:
  "a pattern for your own projects · not the course solution".
- **V6 · Names and the registry (S12, S15).** The image as a TEAL stack with its ID `b5c531a6b555`;
  two TEAL sticky notes point at the same stack: `simple-translate:latest` and
  `student/simple-translate-ac215:latest` (`laptop/44`): a second name, no copy. The long name
  unfolds into `docker.io / student / simple-translate-ac215 : latest` (registry, account,
  repository, tag; `docker.io/library/…` for names without a slash, as in every build log). Push:
  slabs travel a PINK route to a BLUE shelf; the second push sends nothing: each slab bounces back
  "already exists" (`laptop-push/08`). Without login the shelf's door stays shut (RED,
  `laptop-push/03`). S15: seven slabs come down the PINK route into the BLUE VM (`vm-debian12/06`).
- **V7 · Platforms (S13).** Two chips: `arm64 · Apple Silicon` (GREY) and `amd64 · Intel/AMD,
  default GCP VM` (BLUE), each with its own small alphabet of glyphs (machine instructions). The
  binaries in an image (bash, python, uv) are written in one alphabet, and the image has no kernel
  to translate. A tag can be a **menu** (an index): `python:3.12-slim-bookworm` unfolds into five
  platform rows (`laptop-push/11`; attestation rows dimmed); `dlops/simple-translate` is a single
  page, amd64 (`laptop-push/10`, `vm-debian12/08`); your push is amd64 + an attestation row
  (`laptop-push/09`) — on a Mac it would be arm64. The BLUE VM orders "amd64" from the menu; an
  arm64-only menu has nothing it can run → RED `exec format error`. Fixes: `--platform=linux/amd64`
  turns the page amd64; buildx cooks two pages (one through an "emulation" box) and pushes a menu
  with both.
- **V8 · Container ≠ VM (S02, S14).** Left: a VM, L1's slice of a server with **its own kernel**
  and OS (BLUE). Right: containers as TEAL boxes standing side by side on **one shared kernel bar**:
  isolated processes with their own files, not machines. On a Mac or Windows, a dashed GREY "Linux
  VM" appears under the bar inside the GREY laptop: Docker Desktop runs one to provide the Linux
  kernel. S14: on the GCP VM, a PURPLE `dockerd` sits directly on the VM's Debian kernel, and the
  TEAL container sits inside the BLUE VM.

## README step tracker (ReadmeTracker, top-left)

Three trackers. The README nests *Pushing Docker Image to Docker Hub* (an H3, `README.md:186-191`)
inside *Developing App using Containers*; it gets its own tracker so the dot rows stay short and
match the two parts. The README numbers its Dockerfile steps 1–5; the tracker keeps that number in
the step title so "step 9 of 16: uv, COPY (3/5)" matches the README's "Step 3".

- **A · Developing App using Containers** (`README.md:106-184`), 16 steps: container ls · Stop
  containers · system prune · image ls · Clone repo · Create Dockerfile · FROM (1/5) ·
  ENTRYPOINT (2/5) · uv, COPY (3/5) · uv sync (4/5) · CMD (5/5) · Solution file · Build image ·
  Run container · Translate · Exit
- **B · Pushing Docker Image to Docker Hub** (`README.md:186-191`), 4 steps: Access token · Login ·
  Tag · Push
- **C · Running App on VM using Docker** (`README.md:203-220`), 7 steps: Create VM · SSH ·
  Install Docker · Docker version · Run image · Run cli · Delete VM

Each Dockerfile step (A7–A11) includes the README's "Build + Run after each step"
(`README.md:130`). Steps the README does not have (`ls -a`, `docker image inspect`, `git status`,
`diff`, `cp`, `docker ps -a`, `docker history`, `--progress=plain`, `imagetools`, `apt-get update`
on the VM, `docker ps` without sudo …) are marked `extra` in the tracker caption and in the
narration ("this one isn't in the README"). S10, S11 and S13 are all extras: the tracker stays on
A16, B4 and B4 with the caption "extra".

## Scene plan

Notation as in L1's script: `laptop/NN` = `assets/terminal/laptop/NN-*.txt`, line numbers are
**file** lines (line 1 is the `$` command and is never printed; `[exit N]` is never printed).
▶ = README command with a `your turn` tag at real checkpoints.

**S01 · One command on a fresh VM (~210 words).** Cold open, no tracker yet: terminal
`ssh · ac215-l02`. ▶-less preview of the README's last section: `sudo docker run --rm -ti
dlops/simple-translate` → `vm-debian12/06`: 2-3, first `Pull complete` (4), `…`, 10-12 (Digest,
Status), prompt 13; `python cli.py` → banner (16-20, trimmed), 24, 26-27 → `Output: Adoro il
formaggio`. "A fresh VM. No git clone, no Python setup, no uv: one command." Then `python --version`
→ 28-29 `Python 3.14.7`, while CODE(Dockerfile.txt: 2) `FROM python:3.12-slim-bookworm` slides in
beside it: "the recipe says 3.12; hold that thought" (paid off in S07 and S15). V1 ladder
(`README.md:9-16`): rungs 1–2 tagged L1, rungs 3–4 light up. How to follow along: three trackers
(laptop, Docker Hub, VM); `▶ your turn`; you need Docker Desktop running (Tutorial 0), a free
Docker Hub account, and your GCP project for the VM at the end (no service account,
`README.md:23`). The study guide has every command.

**S02 · Image, layer, container, registry (~290).** Concept scene, no terminal. V2 introduced on a
generic stack: an **image** is a read-only stack of layers plus a config card; instructions that
change files (RUN, COPY) add a layer, the others only write on the card. A **container** is the
image plus a thin writable layer plus one running process; when the process ends the container
stops, and `--rm` throws the writable layer away; the image is never changed. Mental model: image =
class, container = instance. Kindly: the README says "Build the docker container"
(`README.md:173`) and "copy source code into the container" (`:146`): build makes an *image*, run
makes a *container*. A **registry** (Docker Hub) is shelves of images stored by name; a **tag** is a
name pointing at one image (`:latest`). V8: VM vs container (own kernel vs shared kernel; Docker
Desktop's hidden Linux VM on a Mac or Windows; on the GCP VM later, Docker runs right on its
Linux). What a venv couldn't isolate in L1 (the OS, system libraries) is now inside the box.

**S03 · A clean slate, and the clone (~230).** Tracker A1→A5. Laptop terminal (`laptop`,
`student@laptop:~$`). ▶ `docker container ls` → `laptop/01`: 2 (header only). A2: "Stop any
container that is running": nothing to stop here; if you have one, `docker stop` and its ID
(narration only, not typed). ▶ `docker system prune` → `laptop/02`: 2-9, cut line 8 after `[y/N]`,
pause, type `y`. Kindly (README `:113` says "clear up unused images"): *dangling* = images without a
name; named images survive; add `-a` to remove every unused image. ▶ `docker image ls` →
`laptop/03`: 2 (an empty table; "your columns may differ with your Docker version; ours is 29, at
the time of recording"). README note `:122-123`: clone on your laptop; L1's VM clone doesn't help.
▶ `git clone https://github.com/dlops-io/simple-translate.git` (`README.md:50`) → `laptop/04`: 2;
`cd simple-translate` (`README.md:51`, no output; prompt changes). Extra `ls -a` → `laptop/05`: 4-12:
highlight `Dockerfile.txt`; no `Dockerfile`, no `uv.lock`. Extra: the README's build command before
the file exists → `laptop/07`: 7 (RED, wrap) `failed to read dockerfile: open Dockerfile: no such
file or directory`. "The README wants you to write it, in five steps."

**S04 · Dockerfile step 1: FROM (~270).** Tracker A6→A7. Create `Dockerfile` in VS Code (exactly
that name, no extension). CODE(README.md: 135-136); ▶ extra `cat Dockerfile` → `laptop/08`: 2-3.
The build command anatomy (`README.md:174`): `-t simple-translate` the name (TEAL), `-f Dockerfile`
the recipe, `.` the build context (PINK; "this folder: Step 3 shows why it matters"). ▶
`docker build -t simple-translate -f Dockerfile .` → `laptop/09`: 15 (cut after `@sha256:34386ef0`
with `…`), 31-34 (the four layers), 26 (`naming to docker.io/library/simple-translate:latest`). The
plain-log and `desktop-linux` notes (Running example). V2: four ORANGE base slabs drop. Concept
before command: extra `docker image inspect simple-translate --format …` → `laptop/10`: 2
(`Entrypoint=null Cmd=["python3"] WorkingDir=""`); V3 slots appear with the inherited CMD tile →
predict: a Python prompt. ▶ `docker run --rm -ti simple-translate` (`README.md:180`) →
`laptop/11`: 2-4 (`Python 3.12.15 …`, `>>> exit()`), "3.12.15 at the time of recording". Extra
`git status` → `laptop/12`: 2-5 (`nothing to commit, working tree clean`) although we just made a
file: CODE(dot-gitignore.txt: 1-4) with header `.gitignore · lines 1–4`, line 3 `Dockerfile`
highlighted. Kindly: the repo ignores your Dockerfile; `git add -f Dockerfile` if you want to
commit it (narration).

**S05 · Step 2: ENTRYPOINT (~190).** Tracker A8. CODE(README.md: 142); extra `cat Dockerfile` →
`laptop/13`: 2-5. ▶ build → `laptop/14`: 15 (cut as above), 17 (`CACHED`), 25 (naming). "Nothing
downloaded, no new layer": V2 writes ENTRYPOINT on the card. V3: `["/bin/bash"]` drops into
ENTRYPOINT. Spoken question, no timer: "so will it start bash running python3?" Extra inspect →
`laptop/15`: 2 (`Entrypoint=["/bin/bash"] Cmd=null`): the inherited CMD tile falls away. Setting
ENTRYPOINT resets the CMD you inherited. ▶ run → `laptop/16`: 2-3 (`root@f72851da4a58:/# exit`).
Read the prompt: `root` (you are root inside), the container's ID (new every run), `/` as the
working directory (no WORKDIR: `laptop/10` said `WorkingDir=""`).

**S06 · Step 3: install uv, copy the code (~220).** Tracker A9. CODE(README.md: 148-151); extra
`cat Dockerfile` → `laptop/17`: 7-10. V5 seed: the context parcel; `COPY . ./` copies *everything*
in the folder into `/`. ▶ build → `laptop/18`: 27 (`[2/3] RUN pip install uv`), 33
(`Successfully installed uv-0.13.0`), 34 (the root-user WARNING, wrap; "in L1 this warning mattered;
inside an image the image is the isolation"), 40-41 (`[3/3] COPY . ./`). V2: the uv slab and the
COPY slab drop. PONDER 1 (6 s). ▶ run → `laptop/19`: 2-7 (`ls`: `cli.py`, `Dockerfile`,
`pyproject.toml` among `bin`, `etc`, `usr` — highlight the repo files), 8-12
(`python cli.py` → `File "//cli.py", line 8` … `ModuleNotFoundError: No module named 'art'`, RED),
13-14 (exit). "We installed the installer, not the packages."

**S07 · Step 4: uv sync, and two Pythons (~330).** Tracker A10. CODE(README.md: 157). PONDER 2
(8 s), with CODE(pyproject.toml: 6) beside the base line `FROM python:3.12-slim-bookworm`. ▶ build
→ `laptop/21`: 23-24 (`RUN pip install uv` · `CACHED`), 26-27 (`[3/4] COPY . ./` · `DONE` —
"it ran again although we only added a line: keep that question for part 2"), 30, 32-34, 36
(`Downloading cpython-3.15.0-linux-x86_64-gnu (download) (35.9MiB)`, `Using CPython 3.15.0`,
`Creating virtual environment at: /.venv`, `Resolved 13 packages`, `Installed 11 packages`), 37, `…`,
47. V4 (number line, PURPLE download into the interval); V2 drops the GREEN slab. ▶ run →
`laptop/22`: 2-9 (`ls -a`: `.venv`, `uv.lock` highlighted GREEN), 10-14 (`python cli.py`: the same
`ModuleNotFoundError`, RED). Why: V4's PATH half (the venv is not activated; L1: "activation is just
PATH"). Extra typed checks from the same capture: 15-16 (`.venv/bin/python --version` →
`Python 3.15.0`), 17 + 28-31 (`source .venv/bin/activate && python cli.py` → `Output: Adoro il
formaggio`, GREEN, banner trimmed), 32 (`(app) root@01dca6d0f4d8:/#`). Erratum 1, kindly (the 3.12
image vs `>=3.13`), with the fix.

**S08 · Step 5: CMD, the solution, the build (~280).** Tracker A11→A13. CODE(README.md: 163-164);
extra `cat Dockerfile` → `laptop/23`: 14-15. V3: the CMD tile slides in; `exec bash`. ▶ build →
`laptop/24`: 23-24, 26-27, 30 (COPY and the CPython download again: "we only added one line; part 2
explains"). ▶ run → `laptop/26`: 2-9: no `(app)` in the prompt, but `which python` →
`/.venv/bin/python`, `Python 3.15.0`, `echo $VIRTUAL_ENV` → `/.venv`: active, just not shown (the
fresh bash sets its own prompt). A12, *Solution Dockerfile* (`README.md:167-168`): extra
`diff Dockerfile Dockerfile.txt` → `laptop/27`, the `+` lines only, ≤ 12 on screen, in two groups:
9-18 (three ENV lines: no apt prompts, a UTF-8 locale, unbuffered logs) and 20-26 (one RUN: apt-get
update, upgrade, clean, a newer pip, uv); then 33-34 (ENTRYPOINT moved to the end: the order of
ENTRYPOINT and CMD lines doesn't matter). Extra ▶ `cp Dockerfile.txt Dockerfile` → `laptop/28` (no
output): "the README only names the file; this is the quickest way to use it". A13 ▶
`docker build -t simple-translate -f Dockerfile .` → `laptop/29`: 3 (`[+] Building 28.1s (9/9)
FINISHED`), 9 (cut after `python:3.12-slim-bookworm` with `…`), 13-15 (`RUN set -ex; …` 13.3s,
`COPY . ./`, `RUN uv sync` 4.9s), 22 (naming). "This compact view is what you'll see."

**S09 · Run it, translate, exit (~270).** Tracker A14→A16. ▶ `docker run --rm -ti
simple-translate` → `laptop/31`: 2; ▶ `python cli.py -t "Good morning" -s "en" -d "es"` →
3-16 (banner trimmed; `Arguments: Namespace(text='Good morning', file='', src='en', dest='es')`,
`Input: Good morning`, `Output: Buen día` GREEN); ▶ `exit` → 17-18. V2 container beat: the glass
layer + PID 1 (extra, `laptop/33`: 4-5, `echo $$` → `1`); `-t` a terminal, `-i` your keyboard;
`exit` ends PID 1, the container stops, `--rm` deletes it: extra `docker ps -a` → `laptop/32`: 2
(empty). PONDER 3 (8 s). V3 knock-out → extra `docker run --rm -ti simple-translate python cli.py`
→ `laptop/36`: 2 (`cannot execute binary file`, RED; exit 126). The working form, extra:
`docker run --rm simple-translate -c "source .venv/bin/activate && python cli.py -d fr"` →
`laptop/37`: 12, 14-15 (`Output: j'adore le fromage`). In passing: the repo's `docker-shell.sh`
builds and runs in one go (CODE(docker-shell.sh: 10-15); not in the README). End of part 1: "You
built and ran your own image. Part 2: what's inside it, why it rebuilt, and shipping it to a VM."

**S10 · What's inside the image (~230).** Tracker A16 (extra). Extra `docker image ls` →
`laptop/30`: 2, 4 (crop row 3): `518MB` disk, `144MB` content (content = the compressed layers that
travel to a registry; disk adds the unpacked copy; Docker Desktop may show other columns). Extra
`docker history simple-translate` → `laptop/34`: 2-10, `…`, 23 (never rows 11-13): V2 rescales.
Read bottom-up, it is the Dockerfile top-down; most of the 125MB `uv sync` layer is the Python uv
downloaded. Inside (`laptop/33`): 8-11 (`python --version` → `3.15.0`,
`/usr/local/bin/python --version` → `3.12.15`: V4 coda, two Pythons), 12-13 (uv's Python folder),
21-28 (`ls -a /`: `.git`, `.vscode`, `Dockerfile`, `README.md` highlighted). `COPY . ./` copied the
whole context, your git history included. Erratum 8: no `.dockerignore`; add one with `.git`,
`.venv`, `secrets/`. "This matters most when the image goes public, which is next."

**S11 · The layer cache (~300).** Tracker A16 (extra). V5 full, concept first (the rule: a step is
reused when its parent, its instruction and, for COPY, the files' checksum all match; the first
change re-runs that step and every step after it). Extra `docker build --progress=plain -t
simple-translate -f Dockerfile .` (extra flag, said) → `laptop/38`: 23-24, 26-27, 29-30 (all
`CACHED`). PONDER 4 (8 s). The edit: CODE(cli.py: 45-51), line 49 `default="I love cheese"` morphs to
`"I love brie"`; extra `git diff` → `laptop/39`: 10-11. Rebuild → `laptop/40`: 23-24 (`CACHED`),
26-27 (COPY ran), 30 (CPython downloaded again), 36 (`Installed 11 packages`): the RED wave. Twist:
`git checkout -q cli.py` (as run in `run_steps.sh:139`, no output) → rebuild → `laptop/41`: 26-27,
30: still re-runs (`.git/index` changed, and it's in the context). This answers part 1's question:
the Dockerfile itself is in the context, so every edit to it re-ran COPY and `uv sync` (erratum 7,
kindly: expected while learning). The fix animates (V5); the full Dockerfile is in exercises.md.

**S12 · Tag and push (~290).** Tracker B1→B4. B1: a schematic card tagged `illustration`: Docker
Hub account → create an access token (`README.md:188`); it is a password: keep it out of files and
repos. B2: CODE(README.md: 189) with `<USER NAME>` and `<ACCESS TOKEN>` in YELLOW ("yours"); not
runnable here (no account). The stand-in, tagged `stand-in · local registry, not Docker Hub`:
`laptop-push/05`: 2, 8 (`WARNING! Using --password via the CLI is insecure. Use
--password-stdin.`, `Login Succeeded`). Erratum 5: `-p` leaves the token in your shell history;
type `docker login -u <USER NAME>` and paste the token when it asks. B3 ▶ `docker tag
simple-translate student/simple-translate-ac215` (`README.md:190`) → `laptop/43` (no output), with
the `<USER NAME>` caption. Extra `docker image ls` → `laptop/44`: 2, 4-5 (crop row 3): two names,
one ID. V6 sticky notes and the unfolding name. B4 ▶ `docker push student/simple-translate-ac215`
(`README.md:191`) → first the real answer from Docker Hub when you are not logged in:
`laptop-push/03`: 2-8 (RED, wrap): "if you see this: log in, and check the name starts with *your*
username". Then the stand-in push → `laptop-push/07`: 3-4, `…`, 15 (`Pushed`, `latest: digest:`)
and again → `laptop-push/08`: 4, `…`, 15 (`Layer already exists`): only missing layers travel. On
Docker Hub, the base layers may say "Mounted from library/python" (narration only). Your
repository is public by default: anyone can pull it, `.git` included (S10).

**S13 · Platforms: arm64 vs amd64 (~300).** Tracker B4 (extra). Extra `uname -m; docker image
inspect simple-translate --format '{{.Os}}/{{.Architecture}}'` → `laptop/35`: 2-3 (`x86_64`,
`linux/amd64`): "on an M-series Mac you'd see arm64". V7, concept first. Extra
`docker buildx imagetools inspect python:3.12-slim-bookworm` → `laptop-push/11`: 2-3, then the five
`Platform:` lines 9, 30, 51, 72, 93 with `…` between: a menu. Extra
`docker buildx imagetools inspect dlops/simple-translate` → `laptop-push/10`: 2-4: a single page
(amd64, `vm-debian12/08`), although CODE(docker-build-push.sh: 26-27) would push both platforms
(erratum 4). Your stand-in push → `laptop-push/09`: 3, 9, 13 (amd64 + an attestation). PONDER 5
(8 s). Answer: no. The same failure the other way round, real, tagged `extra · arm64 image on an
amd64 machine`: `laptop-push/12`: 2, 10 (`exec /usr/bin/uname: exec format error`, RED). What a
Mac-built image does on the VM is said, not shown: a "no matching manifest" refusal or that same
`exec format error`. Fixes: CODE(docker-shell.sh: 11-12) (line 12, commented out:
`--platform=linux/amd64`), or CODE(docker-build-push.sh: 11, 23, 27): buildx builds both and pushes
a menu; change `DOCKER_USERNAME="dlops"` to yours (else S12's denial), run it with `bash` (it isn't
executable), then `docker buildx use default` (`desktop-linux` on Docker Desktop) so plain builds
load locally again.

**S14 · A VM with only Docker (~240).** Tracker C1→C4. V8 (S14 half). C1: schematic console,
tagged `illustration` (as in L1): the README gives no settings (`expected/vm-console.txt`); an
ordinary E2 machine (amd64, see S13) with Debian 12 or 13 are sensible choices, not requirements.
GOLD tag: billed per second while it runs; its disk bills while it exists. C2: SSH → terminal
`ssh · ac215-l02`. C3 ▶ `sudo apt install docker.io` (`README.md:210`) → `vm-debian12/01`: 4-8
(`E: Unable to locate package docker.io`, RED; Debian 13 says `Error:`). Erratum 2, kindly: the
package lists are empty; the README ran `sudo apt-get update` first in L1's sections
(`README.md:44`, `:74`) but not here. Extra ▶ `sudo apt-get update` → `vm-debian12/02`: 8-9
(`Fetched …`, `Reading package lists...`). ▶ `sudo apt install docker.io` again →
`vm-debian12/03`: 4-6, 55-58 (`1 upgraded, 92 newly installed`, `Need to get 107 MB`, cut 58 after
`[Y/n]`, type `Y`), `…`, 560, 581 (Debian 13: 91 packages, 118 MB). C4 ▶ `sudo docker --version` →
`vm-debian12/04`: 2 (`20.10.24+dfsg1`) and `vm-debian13/04`: 2 (`26.1.5+dfsg1`): "Debian's own,
older Docker; plenty to run an image". Extra `docker ps` without sudo → `vm-debian12/05`: 2 (wrap,
`permission denied … docker.sock`): that is why the README says `sudo` (the alternative, the
`docker` group, is narration only).

**S15 · One-command deploy (~280).** Tracker C5→C6. ▶ `sudo docker run --rm -ti
dlops/simple-translate` (`README.md:215`) → `vm-debian12/06`: 2-4, `…`, 10-12, 13 (V6: seven slabs
come down). ▶ `python cli.py` (`README.md:218`) → 14-27 (banner trimmed; `Arguments:
Namespace(text='I love cheese', …, dest='it')`, `Input: I love cheese`, `Output: Adoro il
formaggio`). Extra `python --version` → 28-29 (`Python 3.14.7`): the hook's question, answered with
V4's coda: built 2026-09-16 (`vm-debian12/08`: 3) with uv 0.12.15 (`vm-debian12/10`: 8), whose
newest match for `>=3.13` was 3.14.7; our build today got 3.15.0. Same Dockerfile, a month apart:
`pip install uv` is unpinned, `>=3.13` floats, there is no `uv.lock` (L1's erratum). An image
freezes all of that — that is why you ship the image, not the recipe. ▶ `exit` → 30-31. Erratum 3,
kindly: `README.md:205` promises "pull the image you pushed in step 3", but `:215` runs the
instructor's image; yours is `sudo docker run --rm -ti <USER NAME>/simple-translate-ac215` (shown
as text with the placeholder, not run; needs an amd64 build, S13). Erratum 12: the published image
has an older `cli.py` (`vm-debian12/10`: 2-4, `1266 cli.py`, `Translator()` without
`raise_exception=True`): if Google refuses, `Output:` silently repeats your input — not a Docker
problem. If the pull itself fails: `vm-debian13/06-docker-run-rate-limited.txt`: 3 (RED, wrap,
`toomanyrequests: You have reached your unauthenticated pull rate limit.`): anonymous pulls are
limited per network address; wait, or log in.

**S16 · Tear down, recap, and what's next (~240).** Tracker C7. Extra `sudo docker ps -a` →
`vm-debian12/11`: 2 (empty: `--rm`). ▶ Delete the VM (schematic console, `illustration`): the BLUE
VM dissolves, the GOLD meter stops; checklist "VM instances: empty · Disks: empty". Optional, said
only: the Docker Hub repository stays public until you delete it; images on the laptop can be
removed with `docker system prune -a`. V1 closing picture. "Test yourself", five questions one at
a time with a thumbnail of their picture (answers in exercises.md):
1. What is the difference between an image and a container, and what does `--rm` delete?
2. What command line does our container run at start-up, and what happens with
   `docker run --rm -ti simple-translate python cli.py`?
3. The Dockerfile says `python:3.12`. Why does `python --version` print 3.15 (or 3.14), and what
   does `/usr/local/bin/python` print?
4. You edit one line of `cli.py`. Which build steps re-run, and how would you reorder the
   Dockerfile so `uv sync` stays cached?
5. Name two ways to make an image built on Apple Silicon run on a default GCP VM.
Footer cards: exercises.md, and the study guide (`MLOps_Learning · guides/L02-containers-1.md`).
Next: L3, Containers II: five containers, your own Dockerfiles, a working directory and a non-root
user, and your laptop's folder mounted into the container (GREY dashed teaser).

## Ponder questions (summary)

| # | scene | question (as on the card) | answer (said right after the timer) |
| --- | --- | --- | --- |
| 1 | S06 (6 s) | "uv is installed and the code is copied in.\nWill python cli.py run?" | No: `ModuleNotFoundError: No module named 'art'`; nothing has installed the packages (`laptop/19`) |
| 2 | S07 (8 s) | "This image's Python is 3.12.\npyproject.toml asks for 3.13 or newer.\nWhat will uv sync do during the build?" | Download a newer CPython into the image: 3.15.0, at the time of recording (`laptop/21`) — L1's S10, inside a build |
| 3 | S09 (8 s) | "docker run --rm -ti simple-translate python cli.py\nWhat command line does the container actually run?" | `/bin/bash python cli.py`: your words replace CMD only; exit 126 (`laptop/36`) |
| 4 | S11 (8 s) | "You change one word in cli.py and rebuild.\nWhich of the four steps run again?" | `COPY . ./` and `uv sync` (with the 35.9 MiB download); FROM and the apt/pip RUN stay `CACHED` (`laptop/40`) |
| 5 | S13 (8 s) | "You built on an M-series Mac and pushed.\nYour VM is an ordinary Intel/AMD machine.\nWill your image run there?" | No: arm64 binaries on an amd64 CPU; build with `--platform=linux/amd64` or push both with buildx |

Each is answerable from L1 or from the picture shown just before it.

## Errata to state (kindly, with the fix)

1. **3.12 image, `>=3.13` project** (`README.md:133`, `Dockerfile.txt:2` vs `pyproject.toml:6`): every
   build downloads a second Python (35.9 MiB; 3.15.0 today, 3.14.7 in the instructor's image). Fix
   in your own projects: `FROM python:3.13-slim-bookworm`, or a matching `requires-python` (S07, S15).
2. **`sudo apt install docker.io` without `apt-get update`** (`README.md:210`): on a fresh Debian 12
   or 13 it fails with `Unable to locate package` (exit 100). Run `sudo apt-get update` first (S14).
3. **Step 4 runs the instructor's image, not yours** (`README.md:14`, `:205` vs `:215`): to deploy
   yours, `sudo docker run --rm -ti <USER NAME>/simple-translate-ac215` (S15).
4. **Platforms are never mentioned** (no `platform`, `amd64` or `arm64` in the README): a plain
   build on Apple Silicon makes an arm64 image that a default VM can't run. Fix: `--platform=linux/amd64`
   (`docker-shell.sh:12`) or buildx (`docker-build-push.sh:27`, with your username at `:11`). And
   `dlops/simple-translate` itself is amd64 only, though that script would push both (S13).
5. **`docker login -p <ACCESS TOKEN>`** (`README.md:189`) puts the token in your shell history;
   Docker warns about it. Use `docker login -u <USER NAME>` and paste the token at the prompt (S12).
6. **`.gitignore` hides your `Dockerfile`** (`.gitignore:3`): `git status` says clean;
   `git add -f Dockerfile` to commit it (S04).
7. **"Build + Run after each step" re-runs `uv sync` from Step 4 on**, download included, because
   the Dockerfile is in the build context; `git checkout` doesn't bring the cache back. Expected
   while learning; copy `pyproject.toml` first and add a `.dockerignore` in real projects (S07, S08,
   explained in S11).
8. **No `.dockerignore`**: `.git`, `.vscode` and the Dockerfile end up in the image (S10), and the
   image goes to a public repository (S12). Add `.git`, `.venv`, `secrets/`.
9. **`docker system prune` keeps named images** ("clear up unused images", `README.md:113`): it
   removes only dangling ones; `-a` removes every unused image (S03).
10. **"Build the docker container"** (`README.md:173`, also `:146`): build makes an image (S02).
11. **No `(app)` in the final container's prompt**: not an error; the venv is active, check with
    `which python` (S08).
12. **The published image lags the repo**: its `cli.py` is an older version without
    `raise_exception=True`, so a refused request prints your input back as the "translation" (S15).

## Costs and teardown

- **The VM** (S14, S16): billed per second while it runs, its boot disk while it exists (L1's
  lesson: delete, don't stop). GOLD cost tag on the console drawing in S14, the meter stops in S16.
  Checklist: *VM instances* empty, *Disks* empty.
- **Docker Hub** (S12): free; a new repository is **public** by default, so anything in the image
  (`.git` history, a key in later lectures) is public too. Delete the repository or make it private
  when you're done. Anonymous pulls are rate-limited per network address (S15), which a class on
  one network can hit; logging in raises the limit.
- **Laptop disk** (S10, S16): the image is 518MB as Docker 29 counts it, plus build cache.
  `docker system prune -a` reclaims it (said, not typed). If you ran `docker-build-push.sh`:
  `docker buildx use default` (S13).
- **Containers**: none left behind: every run used `--rm` (`laptop/32`, `vm-debian12/11`).

## README commands checklist (for the follow-along review)

| README command | README line | scene |
| --- | --- | --- |
| `docker container ls` | 115 | S03 |
| "Stop any container that is running" (no command) | 116 | S03 (narration) |
| `docker system prune` | 117 | S03 |
| `docker image ls` | 118 | S03 |
| "Clone or download": `git clone https://github.com/dlops-io/simple-translate.git`, `cd simple-translate` | 125 (command 50-51) | S03 |
| "create a file called `Dockerfile`" | 128 | S04 |
| Step 1 block `FROM python:3.12-slim-bookworm` | 135-136 | S04 |
| Step 2 block `ENTRYPOINT ["/bin/bash"]` | 142 | S05 |
| Step 3 block `RUN pip install uv`, `COPY . ./` | 148-151 | S06 |
| Step 4 block `RUN uv sync` | 157 | S07 |
| Step 5 block `CMD ["-c", "source .venv/bin/activate && exec bash"]` | 163-164 | S08 |
| `docker build -t simple-translate -f Dockerfile .` ("Build + Run after each step", 130) | 174 | S04, S05, S06, S07, S08 (×2) |
| `docker run --rm -ti simple-translate` | 180 | S04, S05, S06, S07, S08, S09 |
| Solution `Dockerfile.txt` | 167-168 | S08 (`diff`, `cp`: extras) |
| `python cli.py -t "Good morning" -s "en" -d "es"` | 182 | S09 |
| `exit` | 184 | S05–S09 (`exit()` in S04's REPL) |
| Sign up, create an Access Token | 188 | S12 (illustration) |
| `docker login -u <USER NAME> -p <ACCESS TOKEN>` | 189 | S12 (README panel + stand-in) |
| `docker tag simple-translate <USER NAME>/simple-translate-ac215` | 190 | S12 |
| `docker push <USER NAME>/simple-translate-ac215` | 191 | S12 (real denial + stand-in) |
| Create a VM Instance | 207 | S14 (illustration) |
| SSH into your instance | 208 | S14 |
| `sudo apt install docker.io` | 210 | S14 (fails, then again after `apt-get update`) |
| `sudo docker --version` | 213 | S14 |
| `sudo docker run --rm -ti dlops/simple-translate` | 215 | S01 (preview), S15 |
| `python cli.py` | 218 | S01 (preview), S15 |
| Delete your VM | 220 | S16 (illustration) |

## Notes for script and scene authors

- Shared code (`scenes/common.py`, from L1's): the three tracker factories (`tracker_a`,
  `tracker_b`, `tracker_c`), prompts `P_LAPTOP_HOME`, `P_LAPTOP`, `P_VM`, and a new
  `stand_in_tag()` ("stand-in · local registry, not Docker Hub") next to `extra_tag`,
  `illustration_tag`, `expected_tag`, `recorded_tag`. Set-piece classes: `LayerStack` + `ConfigCard`
  (V2/V3), L1's `VersionLine` and `PathDoors` reused small (V4), `CacheChain` (V5), `NameTags` +
  `RegistryShelf` (V6), `PlatformMenu` (V7), `KernelPicture` (V8); L1's `CostMeter` for the VM.
- Crops that keep panels honest (ASSETS.md, "Differences"): FROM lines from `laptop/18` on carry
  the capture-only digest `4fb3e77d…`: cut them after `python:3.12-slim-bookworm` with `…` (only
  `laptop/09`'s `34386ef0…` may be shown). Never print `laptop/34` rows 11-13, the
  `python:3.12-slim-bookworm` row of `laptop/30`, `44` and `laptop-push/02`, apt's `Get:` lines,
  or the VM's `invoke-rc.d: …` lines (no systemd in the stand-in).
- Long lines: the root-user WARNING (`laptop/18:34`), `laptop-push/03:8`, `vm-debian12/05:2` and
  the rate-limit line fold with `wrap`. Long typed commands fold at a space (L1 convention).
- `laptop/19` and `22` print `ls` in columns: keep the columns, highlight by substring.

## Things never to do on screen

Series rules:
- No Google/GCP or Docker logos, no Docker whale, no console or Docker Hub screenshots: schematic
  drawings tagged `illustration` (the VM console, the token card). `docker` is a PURPLE chip.
- No real person's name: the prompt user is `student`; the narration says "the instructor's image";
  the Docker Hub account in commands is `<USER NAME>` or `student`. Never show the contents of any
  `.git` folder (a published image's commit authors and e-mails live there).
- No hand-typed output: every terminal line comes from `assets/terminal/`; `expected/` text only
  as README panels; the Apple Silicon messages and "Mounted from library/python" are said, never
  printed.
- No command spelled differently from the README. The only substitutions are the placeholders
  (`<USER NAME>` → `student`, captioned) and the local-registry stand-in commands, which carry the
  stand-in tag and are never called the README's.
- No credentials, tokens or project ids that look real: the token stays `<ACCESS TOKEN>`; the
  stand-in's `not-a-real-token` is visibly fake.

Lecture-specific:
- Never call the local registry "Docker Hub"; never show a push to Docker Hub "succeeding".
- Never present the capture-only base image (`4fb3e77d…`, the CA rows, `https://` apt lines in
  builds) as what a student sees.
- Never imply `dlops/simple-translate` is the student's own image, or that it is multi-arch.
- Never say a container "is a small VM" or "has its own kernel"; never say `docker build` builds a
  container.
- Never state version numbers that will change (uv, CPython, Docker, package versions, image
  sizes) without "at the time of recording".

## Left for exercises.md (not in the video)

`ENV UV_PYTHON_DOWNLOADS=never` and its error (digest E1); the full reordered Dockerfile (digest
E2); `--entrypoint /.venv/bin/python` as a second fix for exit 126; a note written inside a
container with and without `--rm`, `docker start -ai` (E5); translating a laptop file with
`-v` (E6, previews L3); `-i` vs `-t` (E7); the silent non-translation (E8); `docker-shell.sh`'s
`--name` conflict (G12); the buildx builder left active (G2); uppercase image names; the `pipenv`
branch's Dockerfile (`python:3.11-slim-buster`, `--platform=linux/amd64` active, a committed lock
file; `assets/source/pipenv-branch/`); Dockerfile hygiene (apt lists and pip cache left in the
image, digest E11); the README's broken in-page links (digest E6).
