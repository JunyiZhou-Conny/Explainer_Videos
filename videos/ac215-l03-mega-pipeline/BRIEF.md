# Brief · AC215 L3 — Containers II: five containers, one bucket

The design of this video, written before the script. Series rules: `docs/AC215_SERIES.md`.
Facts: `digest.md` (the verified tutorial digest) and `assets/` (real captures, see `ASSETS.md`).
**Where the digest and the captures disagree, the captures win.** They are newer (2026-10-13) and
were made on the machine the video shows:

| topic | digest | captures (use these) |
| --- | --- | --- |
| uv version | uv 0.11.32 checked on the host | uv 0.13.0 on the laptop (`laptop/07`, `08`) and in every image (`12-build.txt:1375`) |
| what `uv init --bare` stamps | `>=3.13` (a 3.13 host) | `>=3.11`: this laptop's Python is 3.11.2 (`laptop/00`, `10`, `40`, `50`, `60`). Narration: "your number depends on your laptop" |
| image sizes | ~0.7 GB / ~1.5 GB | `transcribe_audio` 1.35 GB before packages (`13`), 1.48 GB after (`16`); the other four 842–846 MB (`70`) |
| `uv.lock` size | "~100 KB" | 138,445 bytes (`transcribe_audio/04-ls.txt`, `laptop/14`) |
| google-genai | 2.29.0 (wheel read) | 2.30.0 installed (`32-b-build.plain.txt:366`) |
| first apt step | "about 50 s" | 46.9 s, 237 packages, 205 MB (`12-build.txt:148-150`, `:1377`) |
| container id | `01560c557936` | `5b4d4981ec25` (`transcribe_audio/01-docker-run-tty.txt`) |
| COPY layer | ASSETS.md says 180 kB | `17-history.txt`: 193kB |
| CPython 3.15 download in B | "you should see `Downloading cpython-3.15.0`" | only in the plain log (`32-b-build.plain.txt:341-343`); the live view a student sees shows just `[5/5] RUN uv sync 5.9s` (`32-b-build.txt:17`) |
| clone overview | `tree -L 2` | not captured: use `ls -a` of the five folders (`laptop/05`) |
| TTS request block | `synthesis_audio_en/cli.py:77-90` | the print is line 91: quote `:77-91` (E: `synthesis_audio/cli.py:76-90`) |

## Audience and goal

An AC215 student who has done L1 (a VM, venvs, uv) and L2 (a given Dockerfile, image vs container,
layer cache, ENTRYPOINT + CMD, Docker Hub). Docker Desktop and uv are installed (Tutorial 0). They
watch with the mega-pipeline README and the `transcribe_audio` README open, a clone of
[dlops-io/mega-pipeline](https://github.com/dlops-io/mega-pipeline) on their laptop, the course key
from Canvas and their team's group name, pausing to type each command.

After the video they can:
- draw the five-stage pipeline and say which bucket prefix each stage reads and writes, and why
  `group_name` must be the same in every `cli.py`;
- write the component Dockerfile from the README's pieces and say what each line is for
  (ARG, the six ENVs, the one-layer RUN, the non-root user, `UV_PROJECT_ENVIRONMENT`);
- build and run it with `-v "$(pwd):/app"` and say where each kind of state lives: in the image,
  in the container's throwaway layer, or on the laptop through the mount;
- run the `uv add` → exit → rebuild loop and explain why packages vanish without the rebuild;
- place the service-account key so the Google libraries find it, read a `DefaultCredentialsError`,
  and run `--download`/`--transcribe`/`--upload` knowing what to look for;
- repeat the recipe for B–E (right `ARG`, right packages, `requires-python` fixed in `generate_text`);
- keep the key out of Git **and** out of the image (`.dockerignore`), and clean up the images.

## Length and parts

~31 minutes. Narration 3,900–4,300 words (Kokoro af_heart, speed 0.9 ≈ 174 wpm); the plan below
totals **~4,170**. Part 1 = S01–S07 (the pipeline and component A up to a running container that
can't import yet, ~1,880 words, ~14 min); part 2 = S08–S15 (packages, the key, running A, B–E,
secrets, teardown, ~2,290 words, ~17 min). The cut is a natural cliffhanger: the container runs,
the window into the laptop works, and `python cli.py --help` fails with `ModuleNotFoundError`.
Word budgets per scene are targets (±15 %).

## Colours (series table, applied)

| meaning | colour |
| --- | --- |
| your laptop: the clone, the component folder, the files the bind mount shows inside | GREY |
| Google Cloud: the bucket and its drawers, Speech-to-Text, Gemini, Text-to-Speech, Translation, IAM | BLUE |
| containers and images: the five component boxes A–E, the layer stack, the container's thin writable layer (dashed) | TEAL |
| the base image's system parts: Debian 12, apt packages (`build-essential`, `ffmpeg`), the image's Python 3.12 | ORANGE |
| project-owned: `pyproject.toml`, `uv.lock`, `/home/app/.venv` and its packages, the `requires-python` interval | GREEN |
| tools you install: uv (laptop and image), Docker | PURPLE |
| errors, the key inside an image, "don't push this", the unchanged default group drawer | RED |
| your turn, the README tracker, "look here now" | YELLOW |
| money: "billed to the course project" tags; the service-account key (whoever holds it spends that money) | GOLD |
| lookups, paths, routes: the `-v` mount route, the `GOOGLE_APPLICATION_CREDENTIALS` signpost, object names `prefix/group/file` | PINK |

Package chips are coloured by **where they live** (GREEN in the venv), as in L1; a chip that lives
only in the container's writable layer sits inside the dashed TEAL sheet and evaporates with it.
The key is always a GOLD key glyph; its file content is never drawn.

## Running example

- The laptop: user `student`, host `laptop`, Debian 12 with Python 3.11.2 (as captured):
  `student@laptop:~$`, `student@laptop:~/mega-pipeline$`,
  `student@laptop:~/mega-pipeline/transcribe_audio$` (and the other four folders). Long commands
  fold with ` \` (`Terminal.type`). Say once (S01): on a Mac (zsh, `%`) or in Windows Git BASH the
  prompt looks different and Docker Desktop runs the containers; the commands are the same.
- The container: `app@5b4d4981ec25:/app$` (from `transcribe_audio/01-docker-run-tty.txt`). Say once
  (S07) that the part after `app@` is the container's id and changes every run; B–E reuse the same
  drawn prompt.
- The group name: `group-01` (the README's example, `transcribe_audio/README.md:114`; the captures
  used it).
- Extras are typed exactly as the capture's `$` line. A capture whose `$` line joins commands with
  `;` (e.g. `40-c-uv-init.txt`: `uv init --bare; cat pyproject.toml`) may be typed as separate
  commands, each followed by its own lines of the file.
- Builds: scenes type the README-derived `docker build -t <name> .`, never `--network host`, and cut
  every output line that names the capture-only base (`load metadata for docker.io/l03-capture/…`,
  `[1/5] FROM docker.io/l03-capture/…`), the `transferring dockerfile` line and apt's `Get:` lines.

## Visual set pieces (the 3Blue1Brown part)

- **V1 · The relay through the bucket (S01 teaser, S02 full, S10, S12, S13, S15).** Along the
  bottom, the bucket as a long BLUE cabinet of drawers labelled with the prefixes of
  `README.md:74-80` (`input_audios/`, `text_prompts/`, `text_paragraphs/`, `text_translated/`,
  `text_audios/`, `output_audios/`, and `output_audios_pp/` dashed, "bonus"). Along the top, five
  TEAL boxes A–E with their folder names. A waveform token rises out of `input_audios/` into A and
  comes out as a short page that drops into `text_prompts/`; B lifts it and it lengthens into a long
  page in `text_paragraphs/`; there it **splits**: one copy flows to C and becomes a wave in
  `text_audios/`, the other flows to D, turns into a French page in `text_translated/`, then E
  turns it into a wave in `output_audios/`. The DAG edges fade in last. Then the `text_prompts/`
  drawer opens into sub-drawers `group-01/`, `group-02/`, … and one labelled "default group" that
  flashes RED when a box with the unchanged `group_name` writes into it. Object names appear as PINK
  paths (`text_prompts/group-01/input-….txt`, never invented file names: the real ones are not
  known). No container ever touches another: every arrow goes through a drawer.
- **V2 · Dockerfile → layer stack (S05 build-up, S06 sizes, S11 rebuild, S13 shared slab).** Left:
  the Dockerfile growing line by line. Right: a stack of translucent slabs. `FROM` drops an ORANGE
  base slab ("Debian 12 + Python 3.12"). `ARG` and the six `ENV`s add no slab: they pin sticky notes
  on the side (the `GOOGLE_APPLICATION_CREDENTIALS` note PINK, the `UV_PROJECT_ENVIRONMENT` note
  GREEN). `RUN` drops one fat ORANGE slab whose inside shows apt → pip → uv (PURPLE) → user `app`;
  the apt lists appear and are deleted *inside* the slab, so they never reach the stack. `USER` is
  a note, `WORKDIR` a hairline slab. `COPY` drops a thin GREY slab holding the folder's files,
  among them a tiny GOLD key (not commented on until S14). `RUN uv sync` drops an empty GREEN slab
  ("Resolved 1 package"). `ENTRYPOINT`/`CMD` become a label on top: "start: bash, venv on". In S06
  the slabs take sizes from `17-history.txt` (the apt `RUN` layer 842MB, `COPY` 193kB; it is the
  same cached apt layer in every A build) and the stack reads 1.35 GB (`13-images.txt`). In S11
  `[1/5]`–`[3/5]` get a GREEN "CACHED" stamp while `COPY` and `uv sync` re-form; the uv sync slab
  fills with 26 GREEN chips (105MB) and the stack reads 1.48 GB. In S13 three new stacks (C, D, E)
  point at B's ORANGE apt slab instead of building their own: `CACHED [2/5]`, `Building 0.6s`.
- **V3 · The window: image, container, bind mount (S07, S08, S11).** The image as a TEAL block
  with an `/app` cavity full of GREY copied files (`cli.py`, `Dockerfile`, `pyproject.toml`,
  `secrets/`), and a GREEN `/home/app/.venv` box **outside** the cavity. The container = the image
  plus a thin dashed TEAL writable sheet. The laptop on the left (GREY) with the
  `transcribe_audio/` folder. `-v "$(pwd):/app"` draws a PINK route from the laptop folder to
  `/app`; a GREY sheet carrying the laptop's files slides over the cavity and the copied files dim
  underneath: "`/app` now *is* your folder". An edit on the laptop (S08: `group_name`) appears
  inside at once. Anything written under `/app` travels the route back to the laptop and stays;
  anything written elsewhere lands on the dashed sheet. Ponder 3's variant: slide the `.venv` box
  into the cavity (L2's layout); the laptop sheet covers it and the "activate" arrow hits nothing
  (RED).
- **V4 · uv add: list, receipt, shelf (S08, S11).** Inside V3's frame: `pyproject.toml` (a GREEN
  list) and `uv.lock` (a GREEN scroll) sit on the laptop sheet; the venv is a GREEN shelf on the
  dashed writable sheet. `uv add …` writes three names onto the list, unrolls the scroll (138,445
  bytes), and drops 26 GREEN chips onto the shelf. S11: `exit` → the dashed sheet and its chips
  evaporate; list and scroll stay on the laptop. A new container from the old image: empty shelf →
  `ModuleNotFoundError` (RED). Rebuild: `COPY` carries list and scroll into the image, the uv sync
  slab fills with the same 26 chips, and a new container imports them ("imports ok").
- **V5 · Who is calling? Key, ADC, IAM (S09; callback S13).** Inside the container,
  `storage.Client()` is a small machine. The env var is a PINK signpost reading
  `GOOGLE_APPLICATION_CREDENTIALS=secrets/mega-pipeline.json`, planted at the current folder `/app`.
  The client asks `google.auth` "who am I?"; google.auth follows the signpost from `/app` into
  `secrets/` (through the window, on the laptop) and finds the GOLD key; it cuts a short-lived
  token (a GOLD tag with a small clock); the request arrow carries the token to Google (BLUE),
  where an IAM padlock checks what this service account may do and opens the bucket door. Two
  checks, two words: authentication (who: the key) and authorisation (may it: IAM roles),
  `README.md:92-95`. Error branch: the signpost points into an empty `secrets/` → the real last line
  of `07-download.txt` in RED. If the current folder moves (`cd /tmp`), the signpost's root moves
  with it. S13: in C, D and E the client is built at import, so the signpost is consulted before
  argparse ever sees `--help`.
- **V6 · Two filters, two boxes (S14).** The component folder (GREY) with the GOLD key in
  `secrets/`; two destinations: Git's history book and the image's shipping box (TEAL), with a
  Docker Hub shelf behind the box. `.gitignore` is a sieve over the book: the key is caught (the
  `git check-ignore` line from `20`). `docker build` pours the whole folder (the build context) into
  the box with no sieve; `COPY . ./` lands the key in V2's thin COPY slab, now outlined RED (`22`).
  The box slides toward the Docker Hub shelf and stops under a RED "would publish the key" stamp.
  `.dockerignore` adds a second sieve over the box; rebuild; the key stays out (`25`). The run
  still works: the V3 sheet brings `secrets/` in at run time. Coda: the solution branch moves
  `secrets/` beside the repo and draws a second PINK route to `/secrets`
  (`solution-branch/transcribe_audio/docker-shell.sh:95-100`).
- **V7 · requires-python is an interval (S04, S12).** L1's `VersionLine` (3.10 … 3.16). S04: the
  laptop's 3.11.2 (GREY dot) → `uv init --bare` stamps `>=3.11` (GREEN interval from 3.11); the
  image's 3.12.15 (ORANGE dot) lands inside → uv uses it ("Using CPython 3.12.15 interpreter at:
  /usr/local/bin/python3", `12-build.txt:1386`). A second laptop with 3.13: the interval starts at
  3.13, the ORANGE dot falls outside, and a PURPLE download arrow appears (preview). S12:
  `generate_text`'s committed `>=3.14`; the 3.12 dot is outside (RED); the PURPLE arrow drops
  "3.15.0 · uv-managed · 35.9 MiB" into the interval, "the newest at the time of recording". The
  one-line live view `[5/5] RUN uv sync 5.9s` unfolds into the plain-log lines that show it. Fix:
  drag the interval's start to 3.12; the ORANGE dot is inside again (`35-b-rebuild-312.plain.txt:31`).
- **V8 · Ticket stubs: who carries the result (S10, S13).** A container on the left, a BLUE API
  cloud on the right, the bucket drawers below. Speech-to-Text (S10): A sends the FLAC bytes inline
  and gets back a ticket stub (a long-running operation) with a ring that fills for up to 90 s;
  the transcript returns to A, which writes a local file; `--upload` carries it up later. Long-audio
  Text-to-Speech (S13): C sends the text *and an address* (`output_gcs_uri`), gets a stub (300 s
  ring), and the audio crate travels from the TTS cloud straight into `text_audios/`, never through
  the container: that is why C and E have no `--upload`. Translation (S13): no stub; the French page
  comes straight back to D, is saved locally, and `--upload` carries it up.

## README step tracker (ReadmeTracker, top-left)

The tracker's section is the README heading for the clone and **the component folder** for the
five component READMEs (they share one recipe). Step titles ≤ 3 words.

- *Clone this Repository* (`README.md:30-37`): Clone · cd (2)
- *transcribe_audio* (`transcribe_audio/README.md`): cd folder · Key in secrets · uv init ·
  Write Dockerfile · Build image · Run container · uv add · Group name · Check --help · Download ·
  Transcribe · Upload · Exit, rebuild (13)
- *generate_text*: the same 13, step 11 = Generate.
- *synthesis_audio_en*: the same without Upload (12), step 11 = Synthesize.
- *translate_text*: the same 13, step 11 = Translate.
- *synthesis_audio*: as synthesis_audio_en (12).
- Optional sections: *Push to Docker Hub* (component READMEs `:136-140`): Login · Tag · Push (3);
  *ElevenLabs bonus* (`synthesis_audio/README.md:132-156`): Key file · uv add requests ·
  Run cli_11 (3).

Two ordering notes. (1) `README:110` says to rebuild "after exiting the container"; you exit
after testing the CLI, so "Exit, rebuild" is the last step (the captures ran in that order). At
`uv add` (S08) the narration says: "the README adds: when you exit, rebuild; we'll do it at the end
and see why". (2) The component READMEs test with `-d`/`-t`/`-u` (`transcribe_audio/README.md:131-133`);
the main README's Quick Reference (`README.md:128-165`) spells `--download`/`--transcribe`/
`--upload`. Scenes type the Quick Reference's long forms (that is what was captured,
`07-download.txt`) and show the short forms beside them as the same thing.

Steps the README does not have (`ls`, `cat pyproject.toml`, `which python`, `docker images`,
`docker history`, the gotcha demos, `.dockerignore`, `docker image rm`) are marked `extra` in the
tracker caption and in the narration ("this one isn't in the README").

## Scene plan

**S01 · Five containers, one bucket (~210 words).** Cold open on V1 (teaser, no labels yet): a
recording becomes a French podcast through five boxes that "never send each other a single
message". The question on screen: how do they cooperate, and who pays? What is new since L2, as a
four-row morph (L2 → L3): the Dockerfile was given → you write it; one image → five; no mount →
a bind mount into your laptop; no cloud → a shared bucket and a service-account key. How to follow
along: the tracker (shown once), code panels with `path · lines`, "▶ your turn" tags; the study
guide in MLOps_Learning has every command. What you need: Tutorial 0 (Docker Desktop, uv), the key
from Canvas, your group name. Honest limit, said once: the recording machine had no course key, so
wherever the code talks to Google you will see the command and what to look for, not an output
panel. Captured on a Debian 12 laptop with Docker Engine 29.8.2 (`laptop/00`, `01`, extra; show
two lines, not the whole `docker version`).

**S02 · The bucket is the message bus (~280).** `README.md:60-67` in one sentence: in production,
services call each other's APIs; here they only write files to shared storage. V1 in full with
the prefixes of `README.md:74-80`. A bucket has no real folders: `text_prompts/group-01/input-….txt`
is one object name (PINK). Code panel `transcribe_audio/cli.py:108-112` (the upload builds
`os.path.join(text_prompts, group_name, filename)`; `glob … "input-*.txt"`), then
`generate_text/cli.py:42` (B downloads with the matching `match_glob`): the naming contract *is*
the wiring. `group_name` is the namespace; the default value has no guard, so V1's "default group"
drawer flashes RED (`README.md:124` warns: set it before every run). The leaderboard
(`README.md:54`): a schematic grid of groups × stages whose cells light up, tagged `illustration`.
GOLD tag: every call and every byte is billed to the course's project, not yours.
PONDER 1 (8 s): "Look at which drawer each stage reads and writes. Which two stages could run at
the same time, and which one has to wait?" Answer right after the timer: C and D both read only
B's `text_paragraphs/`; E must wait for D.

**S03 · Clone: five folders, no Dockerfile (~220).** Tracker *Clone this Repository* 1→2. ▶
`git clone https://github.com/dlops-io/mega-pipeline.git` (`laptop/03`), ▶ `cd mega-pipeline`,
extra `ls; git log --oneline -1; git branch` (`04`: the folders, `c6bbc9b`, `main`). Extra
`ls -a transcribe_audio generate_text synthesis_audio_en translate_text synthesis_audio` (`05`):
each folder has `README.md`, `cli.py`, `secrets/` and no Dockerfile (`README.md:114`: you write
all five); `generate_text/` already has `pyproject.toml` and `main.py` and no `.gitignore` ("keep
that in mind"); `synthesis_audio/` has a bonus `cli_11.py`. Tracker *transcribe_audio* step 1:
▶ `cd transcribe_audio`. First look at `transcribe_audio/cli.py`: imports `:4-12` (two
`google.cloud` modules and `ffmpeg` are third-party: where they come from is part 2) and the
constants `:18-21` (bucket, two prefixes, `group_name`; skip line 17), then `main` `:118-126`:
three verbs, run in order.

**S04 · The key, and uv init (~270).** Step 2, *Key in secrets*: a schematic (tagged
`illustration`): the course site (Canvas, text only, no logo) → `mega-pipeline.json` → into
`transcribe_audio/secrets/`, then the same file into all five `secrets/` folders. The name must
be exactly `mega-pipeline.json` (a browser may save `mega-pipeline (1).json`). Erratum, kindly: the
component READMEs link an older Canvas file than the main README (`README.md:99` vs
`transcribe_audio/README.md:17`); use the main README's. "How the code finds this file, and what
happens when it can't, is part 2." Step 3, *uv init*: if you don't have uv (extra `uv --version` →
`command not found`, `06`), the README's installer ▶ `curl -LsSf https://astral.sh/uv/install.sh |
sh` (`07`: uv 0.13.0 into `~/.local/bin`); the PowerShell line and `pip install uv` shown as
commands only; "restart your terminal": `uv --version` → `uv 0.13.0` (`08`). ▶ `uv init --bare` →
``Initialized project `transcribe-audio` `` (`09`). Extra `cat pyproject.toml` (`10`): no
dependencies, and `requires-python = ">=3.11"`. V7, first half: that 3.11 is *this laptop's*
Python (`00`: 3.11.2); the image will have 3.12, inside the interval, so all is well here. If your
laptop has 3.13 or newer you'll see `>=3.13`: change it to `>=3.12` (not in the README; S12 shows
what happens otherwise).

**S05 · Write the Dockerfile, line by line (~350).** Step 4. "No Dockerfile here: you write it"
(`transcribe_audio/README.md:38`). V2 build-up with the file a student ends up with,
`files/transcribe_audio.Dockerfile`, in four panels (≤ 12 lines each) labelled
`transcribe_audio/Dockerfile · lines a–b`, caption "from `transcribe_audio/README.md:41-90`":
lines 1–3 (`FROM python:3.12-slim-bookworm`, from the README's prose at `:41`; `ARG
DEBIAN_PACKAGES="build-essential ffmpeg"`: a build-time variable; `ffmpeg` because `ffmpeg-python`
only runs the `ffmpeg` program, `cli.py:67-69`), lines 5–10 (six ENVs, three in one breath —
no apt prompts, UTF-8, unbuffered prints, uv copies files — then two highlighted:
`UV_PROJECT_ENVIRONMENT=/home/app/.venv`, "the venv lives outside `/app`; this line saves us in S07",
and `GOOGLE_APPLICATION_CREDENTIALS=secrets/mega-pipeline.json`, "where the libraries look for the
key: a relative path"), lines 12–21 (one `RUN`: update, upgrade, install, clean and delete the apt
lists in the *same* layer; upgrade pip; `pip install uv` works here because this Python is the
image's own, not apt's — the L1 refusal doesn't apply; create user `app`, uid 1000, owning `/app`;
`transcribe_audio/README.md:72` on not running as root), lines 23–30 (`USER app`, `WORKDIR /app`, `COPY
--chown=app:app . ./` "everything in this folder — everything", `RUN uv sync`, `ENTRYPOINT`/`CMD`:
bash with the venv activated, as in L2). The appendix's sample (`README.md:175-225`) in one line:
it adds `set -ex` and the man-page loop, and its `ARG` (`:179`) lacks `ffmpeg`, so don't paste it
into `transcribe_audio`. ▶ your turn: write the file.

**S06 · Build: five steps, one fat layer (~250).** Step 5. Erratum, kindly: the README only says
"give your image the name `transcribe_audio`" (`transcribe_audio/README.md:95`); the command is ▶
`docker build -t transcribe_audio .` (the `.` is this folder: the build context). Real output from
`12-build.txt`, first and last lines with `…`: the warning (`:9`), `[2/5] RUN apt-get …` with
`237 newly installed`, `205 MB` (`:148-149`), `Successfully installed pip-26.2.1` (`:1368`),
`Successfully installed uv-0.13.0` (`:1375`), `DONE 46.9s` (`:1377`), `[3/5]`, `[4/5]`, `[5/5] RUN
uv sync` with `Using CPython 3.12.15 interpreter at: /usr/local/bin/python3`, `Creating virtual
environment at: /home/app/.venv`, `Resolved 1 package in 2ms` (`:1385-1388`: only the project
itself, no packages yet), `naming to docker.io/library/transcribe_audio:latest` (`:1399`), and the
closing `SecretsUsedInArgOrEnv` warning (`:1404-1405`): "here the value is only a path; remember the
warning anyway". Say: your first build also pulls `python:3.12-slim-bookworm` (this machine already
had it). Extra `docker images transcribe_audio` → 1.35GB (`13`). V2 sizes. Extra (what if you
skipped `uv init`): `26-g21-no-pyproject.txt`'s ``error: No `pyproject.toml` found…`` at
`[5/5]` (show the error and `ERROR: failed to build` lines only). PONDER 2 (8 s): "You change only
`group_name` in `cli.py` and build again. Which of the five steps run again?" Answer after the
timer, from L2's rule: `[4/5] COPY` and `[5/5] uv sync`, because the copied folder changed and
uv sync comes after it; `[1/5]`–`[3/5]` come from the cache. "We'll see it for real in part 2."

**S07 · Run: a window into your laptop (~300).** Step 6. V3 first (concept before command): the
image, the cavity, the `.venv` box outside, the PINK route, the laptop sheet sliding over `/app`.
PONDER 3 (8 s): "In L2 the venv lived at `/app/.venv`, next to the code. With this mount, what
would the container find there?" Answer: your laptop's folder, which has no `.venv`; the image's
venv is hidden and activation fails. That is what `UV_PROJECT_ENVIRONMENT=/home/app/.venv` (line 9)
prevents. ▶ `docker run --rm -ti -v "$(pwd):/app" transcribe_audio` (`transcribe_audio/01`): the
prompt becomes `app@5b4d4981ec25:/app$` (the id is the container's; yours differs every run). No
`(transcribe-audio)` prefix, yet the venv *is* active: extra `which python` →
`/home/app/.venv/bin/python`, `python --version` → `Python 3.12.15`. Extra `ls -a` → your laptop's
files (`Dockerfile`, `pyproject.toml`, `secrets`): the window. Extra `echo
$GOOGLE_APPLICATION_CREDENTIALS` → `secrets/mega-pipeline.json`. Extra `python cli.py --help` →
`ModuleNotFoundError: No module named 'google'` (RED). Windows: Git BASH, quote `"$(pwd)"`, and
`winpty docker run --rm -ti -v "$(pwd)":/app generate_text` (`README.md:230-235`, command only).
Close part 1: "The container runs and sees your folder, but Python can't find Google. In part 2 we
add the packages, and find out why they vanish." Clean frame.

**S08 · uv add: what lands where (~320).** Opens on the prompt (one line of recap). Step 7: ▶
`uv add google-cloud-storage google-cloud-speech ffmpeg-python` (the README's three packages,
`transcribe_audio/README.md:104-110`, as one command; `transcribe_audio/02`: `Resolved 27
packages`, `Installed 26 packages`, a few `+` lines, `…`, the last line) — three asked, 26
installed, L1's dependency tree again. V4 + V3: the list and the receipt land on the laptop (they
are under `/app`); the 26 chips land on the shelf in `/home/app/.venv`, on the dashed sheet. Extra
`cat pyproject.toml` (`03`): three lower bounds; extra `ls -la` (`04`): `uv.lock`, 138,445 bytes,
owned by `app`; extra `which python; echo $VIRTUAL_ENV; …` (`10`): the venv is `/home/app/.venv`,
outside the window. Two asides, one line each: the package is `ffmpeg-python`, not `ffmpeg`; on a
Linux laptop whose folder isn't owned by uid 1000, `uv add` fails with `Permission denied (os
error 13)` (`13-g7-root-owned.txt`, last line) — Docker Desktop on Mac and Windows handles that
for you. Step 8, *Group name*: in VS Code on the laptop, `transcribe_audio/cli.py:21` → `group-01`
(panel before/after; the README's instruction `:114`); extra `grep -n "^group_name" cli.py`
inside (`06`) already shows it: the window works both ways. Same name in all five `cli.py`. Step 9:
▶ `python cli.py --help` (`05`) — identical, line for line, to the README's block (`:117-127`).
▶ your turn.

**S09 · Who is calling? The key and ADC (~310).** Step 10. ▶ `python cli.py --download`
(`README.md:134`; `-d` in the component README). The real output we have: `Args: Namespace(…)`,
`download`, then a traceback, tagged `recorded without the key: what a missing key looks like`
(`transcribe_audio/07`; show lines 2–3, a `…`, the `cli.py` line 36 frame, the
`google.auth.default()` frame, and the last line). Read it as in L1: the code called
`storage.Client()` (`cli.py:36`), which asked `google.auth`, which looked for a file and didn't find
it. V5 explains the whole chain, then the two words (authentication, authorisation). The three
ways to get this error: the key isn't in *this* component's `secrets/`, you `cd`'d away from
`/app`, or you ran `docker run` from the wrong folder. Extra `ls -la input_audios text_prompts
text_prompts/*` (`08`): even this failed run created `input_audios/` and `text_prompts/group-01/`
on your laptop (the folders are made before the client). With the key in place, what to look for
(`cli.py:29-43`): `download`, then one object name per file under `input_audios/`, and the audio
files appearing in `input_audios/` on your laptop. GOLD tag on the request: billed to the course
project. ▶ your turn (with your key).

**S10 · Transcribe and upload (~240).** Steps 11–12. V8 (Speech-to-Text half). Code panel
`transcribe_audio/cli.py:64-78`: ffmpeg turns the MP3 into FLAC (the reason for `ffmpeg` in the
ARG), the bytes go inline, `long_running_recognize` returns an operation, `.result(timeout=90)`
waits. Then `:84-91`: every segment is joined (the latest commit's fix: long audio comes back in
pieces). ▶ `python cli.py --transcribe` — what to look for (no output panel): `Transcribing:` and a
path, ffmpeg's log, `response:`, the transcript, and a new `text_prompts/group-01/input-….txt` on
your laptop; open it: if it says `None`, Speech-to-Text returned nothing (`:80`). ▶ `python cli.py
--upload` — panel `:104-115`: only `input-*.txt` files are handed on; look for `Uploading:` with
`text_prompts/group-01/…`. V1: the token drops into your group's drawer and the schematic
leaderboard's Transcribe cell lights up (`illustration`, `transcribe_audio/README.md:134`).
Flags combine: `python cli.py -d -t -u` runs all three in order (`cli.py:121-126`). GOLD tag.

**S11 · Exit, and bake it in (~260).** Step 13. ▶ `exit`. V4/V3: the dashed sheet evaporates with
the 26 chips; the laptop keeps the rest. Extra on the laptop (`laptop/14`): `pyproject.toml`
with three dependencies, `uv.lock` (138445), `input_audios/` and `text_prompts/` all survived;
`git status --short` shows only ` M cli.py` (why the others are invisible: S15). Extra (the trap):
a new container from the image you built in S06 → `python cli.py --help` → `ModuleNotFoundError`
again (`transcribe_audio/11-g10-new-container.txt`). The README's fix (`:110`): ▶ `docker build
-t transcribe_audio .` — the live view (`15-rebuild.txt` lines 3, 14–17, cut the capture-base
lines): `CACHED [2/5]`, `CACHED [3/5]`, `[4/5] COPY`, `[5/5] RUN uv sync 2.9s`, `Building 9.9s`:
PONDER 2's answer, for real. The full log (`15-rebuild.plain.txt:30-39`): `Resolved 27 packages`,
`Installed 26 packages`. Extra `docker images` → 1.48GB (`16`); extra `docker history
transcribe_audio` (`17`, only the README's rows: skip the four capture-base rows and the base
image's rows): apt `RUN` 842MB, `uv sync` 105MB, `COPY` 193kB. V2 updates. Extra (`12-after-rebuild`):
a fresh container prints `imports ok` with no `uv add`. One sentence: because `COPY` comes before
`uv sync`, any edit re-runs uv sync; later tutorials copy `pyproject.toml` and `uv.lock` first.

**S12 · generate_text: same recipe, two surprises (~320).** Tracker *generate_text*, fast. ▶
`cd ../generate_text`; key into `secrets/` (tick). Extra `ls -a; cat pyproject.toml` (`30`): a
`pyproject.toml` is already here, with both packages and `requires-python = ">=3.14"`. Step 3: ▶
`uv init --bare` → ``error: Project is already initialized …`` (`31`, exit 2). Erratum, kindly:
the README still says to run it (`generate_text/README.md:20-24`); skip it (and `main.py` is a
leftover). Step 4: the Dockerfile differs by one line: `ARG DEBIAN_PACKAGES="build-essential"` (no
audio). Step 5: ▶ `docker build -t generate_text .` (`32-b-build.txt`: `[2/5] … 22.8s`, `[5/5] RUN
uv sync 5.9s`, `Building 54.0s`). PONDER 4 (8 s): "The image is `python:3.12`. This
`pyproject.toml` says `>=3.14`. Which Python will the venv use?" Reveal: the live view hides it;
the full log does not (`32-b-build.plain.txt:341-343`: `Downloading cpython-3.15.0-linux-x86_64-gnu
(download) (35.9MiB)`, `Using CPython 3.15.0`). V7, second half (L2 showed the same thing). Step 6:
▶ `docker run --rm -ti -v "$(pwd):/app" generate_text`; extra `which python; python --version;
readlink -f $(which python)` (`generate_text/01`): `Python 3.15.0`, from
`/home/app/.local/share/uv/python/…`. Step 7: ▶ `uv add google-cloud-storage google-genai` →
`Resolved 35 packages`, `Checked 34 packages` (`02`): nothing new, both were already listed. Steps
8–9: `group_name` is `generate_text/cli.py:19`; ▶ `python cli.py --help` (`04`, = the README).
Steps 10–12, commands only: ▶ `python cli.py --download`, `--generate`, `--upload`
(`README.md:141-143`); look for the prompt being printed, then `Generated text:` and a long article
(`cli.py:73-81`: Gemini on Vertex AI; the model comes from `GEMINI_MODEL`, default
`gemini-2.5-flash-lite`). Step 13, with the fix: extra edit `requires-python = ">=3.12"`
(`34`, which also shows `git status` listing `?? Dockerfile` — no `.gitignore` here), ▶ rebuild →
`Using CPython 3.12.15 interpreter at: /usr/local/bin/python3` (`35-b-rebuild-312.plain.txt:31`);
inside, `Python 3.12.15` (`generate_text/05`). Best: fix it before your first build.

**S13 · Synthesize, translate, synthesize (~350).** The speed round: C, D, E, tracker racing
through. Common beats, shown once for C and repeated as a montage: ▶ `cd ../synthesis_audio_en`,
key, ▶ `uv init --bare` → `>=3.11` (`40`), the Dockerfile with `ARG
DEBIAN_PACKAGES="build-essential"` (erratum, kindly: the prose says "keep ffmpeg",
`synthesis_audio_en/README.md:38` and `synthesis_audio/README.md:38`; the ARG given at `:45` is
right: neither synthesis `cli.py` uses ffmpeg). ▶ `docker build -t synthesis_audio_en .` →
`CACHED [2/5]`, `Building 0.6s` (`41`): V2's shared slab — the Dockerfile text up to that line is
identical to B's, so Docker reuses B's apt layer. ▶ `docker run …`, ▶ `uv add google-cloud-storage
google-cloud-texttospeech` (`synthesis_audio_en/01`: 24 installed). ▶ `python cli.py --help`: with
the key, the README's block (`expected/synthesis_audio_en-help.txt`, tagged `expected`); without
it, it dies at import (`03`: first frame `cli.py, line 22` and the last line) — V5 callback: in C, D
and E the client is built at import, so even `--help` needs the key. V8: `synthesis_audio_en/cli.py:77-91`
(the request carries `output_gcs_uri`; `print("Audio file will be saved to GCS bucket
automatically.")`), so ▶ `python cli.py --download`, ▶ `python cli.py --synthesis` and no upload
(`README.md:148-151`). D (`translate_text`): `uv add google-cloud-storage google-cloud-translate`
(`translate_text/01`: 25 installed), `--help` (`expected/translate_text-help.txt`; `03` fails at
`cli.py, line 20`), `translate_text/cli.py:58-65` (Translation v2, `en` → `fr`, the French text is
printed), ▶ `--download`, `--translate`, `--upload` (`README.md:155-157`). E (`synthesis_audio`):
the same packages as C (`synthesis_audio/01`), ▶ `--download`, `--synthesis` (`README.md:162-163`);
`--help` (`expected/synthesis_audio-help.txt`); erratum, kindly: the code's description says
"Transcribe audio file to text" (`synthesis_audio/cli.py:105`), a copy-paste slip. Each component
ends with ▶ exit and rebuild (`42`, `52`, `62`: `CACHED [2/5]`). Bonus (ElevenLabs, the
instructor's voice; tracker *ElevenLabs bonus*): a key file `secrets/11lab_api_key.txt` with one
line `XI_API_KEY=…` (`synthesis_audio/README.md:139-142`), ▶ `uv add requests` → `Checked 24
packages` (`04`: it was already there, now it's listed), ▶ `python cli_11.py --download`,
`--synthesis`, `--upload` (`:151-153`); without the key file even `--download` fails
(`05`: `FileNotFoundError … 'secrets/11lab_api_key.txt'`, because `cli_11.py:30-39` reads it at
import); it uses your own ElevenLabs quota. (C's README mentions `cli_11.py` at `:132-135`; the
file lives in `synthesis_audio/`.) V1 lights up C, D, E's drawers and leaderboard cells. GOLD tags.

**S14 · Keep the key out of the image (~280).** PONDER 5 (8 s) first: "Your key is git-ignored.
You build the image and push it to Docker Hub. Is the key inside?" V6. Extra demos, all made with
an 82-byte **stand-in file**, never a real key (tag it on screen; never `cat` it): `ls secrets; git
status --short; git check-ignore -v secrets/mega-pipeline.json` (`20`): Git ignores it
(`transcribe_audio/.gitignore:3`); after a rebuild, `docker run --rm --entrypoint ls
transcribe_audio -la /app/secrets` (`22`) lists `mega-pipeline.json`: `COPY . ./` copied it, and
Docker doesn't read `.gitignore`. The build's `SecretsUsedInArgOrEnv` warning from S06 was a hint.
The README's optional push (`transcribe_audio/README.md:136-140`, tracker *Push to Docker Hub*),
commands only: `docker login -u <USER NAME> -p <ACCESS TOKEN>`, `docker tag transcribe_audio <USER
NAME>/transcribe_audio`, `docker push <USER NAME>/transcribe_audio`, under a RED "would publish
the key" stamp; and prefer `docker login -u <USER NAME>` with the token pasted at the prompt (`-p`
leaves it in your shell history). Erratum, kindly: `README.md:103-106` presents `.gitignore` as the
protection; it protects Git only. The fix (extra, recommended, ▶ your turn): a `.dockerignore`
containing `secrets/` (`23`), rebuild, and the same `ls` → `ls: cannot access '/app/secrets': No
such file or directory` (`25`). The run still works: the mount brings `secrets/` at run time. If
you ever pushed an image with the key: delete it and tell the staff so the key can be replaced.
Where the course goes: keep secrets outside the repo and mount them, panel
`solution-branch/transcribe_audio/docker-shell.sh:95-100` (with `:8-10`), caption "the solution
branch, last year: not today's steps".

**S15 · Clean up, recap, and what's next (~210).** Teardown (V1 zooms out): nothing to delete in
the cloud (you created no VM, bucket or account; the course project paid every call; your outputs
stay in the shared bucket under your group). Locally: extra `docker image ls --filter …` (`70`:
`transcribe_audio` 1.48GB, the other four about 845MB each), ▶ extra `docker image rm
transcribe_audio generate_text synthesis_audio_en translate_text synthesis_audio` (`72`); no
containers to remove, every run used `--rm`. Keeping your work: extra `git status` at the repo root
(`71`): only `generate_text/` shows up, because the other four `.gitignore` files hide `Dockerfile`,
`pyproject.toml` and `uv.lock` (`transcribe_audio/.gitignore:5-7`); erratum, kindly: in your own
repo use `git add -f` for those, and never remove `/secrets`. Recap questions (5, on screen one at
a time, answers in exercises.md): which prefix `translate_text` reads and who wrote it; why the
mount doesn't hide the packages and what breaks without `UV_PROJECT_ENVIRONMENT`; after `uv add` in
a `--rm` container, what survives, what is lost, what makes it permanent; which variable tells the
libraries where the key is and why it only works from `/app`; why an image can contain a
git-ignored key and the fix. Next (L4, the `flexible-workflow` branch): your own bucket and
service account, the key kept outside the repo, and a `docker-shell.sh` that builds and runs for
you. Point to the study guide and exercises in MLOps_Learning. Clean frame.

## Ponder questions (summary)

| # | scene | question | answer (said right after the timer unless noted) |
| --- | --- | --- | --- |
| 1 | S02 | Which two stages could run at the same time, and which must wait? | C and D both read only B's `text_paragraphs/`; E waits for D |
| 2 | S06 | Change only `group_name`, rebuild: which steps run again? | `[4/5] COPY` and `[5/5] uv sync`; `[1/5]`–`[3/5]` cached (confirmed by `15-rebuild.txt` in S11) |
| 3 | S07 | With the mount, what would a venv at `/app/.venv` (L2's layout) look like? | hidden by your laptop's folder; activation fails; hence `/home/app/.venv` |
| 4 | S12 | `python:3.12` image, `>=3.14` in pyproject: which Python? | 3.15.0, downloaded by uv (at the time of recording) |
| 5 | S14 | The key is git-ignored; you push the image. Is the key inside? | yes: `COPY . ./` copies the build context; Docker doesn't read `.gitignore` |

## Errata to state (kindly, with the fix)

1. **No build command** (`transcribe_audio/README.md:95` and peers): use `docker build -t
   <component> .` from inside the component folder (S06).
2. **`uv init --bare` stamps your laptop's Python** into `requires-python`: check with
   `cat pyproject.toml`; above `>=3.12`, edit it to `>=3.12` (S04, S12).
3. **`generate_text` ships a `pyproject.toml`** with `requires-python = ">=3.14"`
   (`generate_text/pyproject.toml:4`) while its README says to run `uv init --bare`
   (`generate_text/README.md:20-24`): skip `uv init`, edit to `>=3.12`; `main.py` is a leftover (S12).
4. **"Keep ffmpeg"** in the C and E prose (`:38`) vs the given `ARG DEBIAN_PACKAGES="build-essential"`
   (`:45`): the ARG is right (S13).
5. **`synthesis_audio`'s `--help` says "Transcribe audio file to text"** (`synthesis_audio/cli.py:105`):
   a harmless copy-paste slip (S13).
6. **Two Canvas links** (`README.md:99` vs `transcribe_audio/README.md:17` and peers): use the main
   README's (S04).
7. **The key is baked into the image**: `README.md:103-106` relies on `.gitignore`, but `COPY . ./`
   copies `secrets/` into the image: add `.dockerignore` with `secrets/`; never push such an image
   (S14).
8. **Your work is git-ignored** in four folders (`transcribe_audio/.gitignore:5-7` and peers):
   `git add -f` in your own repo, keep `/secrets` ignored (S15).
9. **No `(transcribe-audio)` prompt prefix**: not a README error; the venv is active, check with
   `which python` (S07).
10. **`cli_11.py` is mentioned in `synthesis_audio_en/README.md:132-135`** but lives in
    `synthesis_audio/` (S13, one clause).

Not on screen (exercises or study guide only): the OpenAI/GPT2 mentions in
`generate_text/README.md:7,130`; `.mp3` names for `LINEAR16` audio (unverified); transcript
segments joined with `""`; the dead local "already exists" check in the synthesis stages.

## Costs and teardown

- **You pay nothing on GCP today.** Every Speech, Gemini, Translation and TTS call and every byte
  in the bucket bills the course's project, because you use its key. GOLD tag "billed to the
  course project" on every Google call (S02, S09, S10, S12, S13). You create no VM, bucket or
  service account, so there is nothing to shut down in the cloud.
- **The key spends that money**: don't leak it (S14). If an image with the key was ever pushed,
  delete it and tell the staff.
- **Local disk**: five images, `transcribe_audio` 1.48 GB, the others about 845 MB each as
  reported here (they share base layers). Teardown (S15): `docker image rm transcribe_audio
  generate_text synthesis_audio_en translate_text synthesis_audio` (extra, captured in `72`). No
  containers remain (`--rm`).
- Optional: Docker Hub repos are public by default; the ElevenLabs bonus uses your own quota.

## README commands checklist (for the follow-along review)

| README command | where | scene |
| --- | --- | --- |
| `git clone https://github.com/dlops-io/mega-pipeline.git`, `cd mega-pipeline` | `README.md:33-34` | S03 |
| `uv init --bare` | each component `:22` | S04 (A), S12 (B, fails), S13 (C, D, E) |
| `curl -LsSf https://astral.sh/uv/install.sh \| sh`; PowerShell line; `pip install uv` | `transcribe_audio/README.md:29`, `:32`, `:34` | S04 (the last two: command only) |
| the Dockerfile pieces | `transcribe_audio/README.md:41-90`; B–E `:45` | S05; S12, S13 (ARG diff) |
| (build, no command in README) `docker build -t <name> .` | `:95` | S06, S11, S12, S13, S14 |
| `docker run --rm -ti -v "$(pwd):/app" <name>` | `:99` | S07, S12, S13 |
| `winpty docker run --rm -ti -v "$(pwd)":/app generate_text` | `README.md:235` | S07 (command only) |
| `uv add` of the listed packages | `:104-110` | S08, S12, S13 |
| `python cli.py --help` | `:117` (B–E `:115`) | S08, S12, S13 |
| `python cli.py --download / --transcribe / --upload` (and `-d -t -u`) | `README.md:134-136`, `transcribe_audio/README.md:131-133` | S09, S10 |
| `--download / --generate / --upload` | `README.md:141-143` | S12 (command only) |
| `--download / --synthesis` (C), `--download / --translate / --upload` (D), `--download / --synthesis` (E) | `README.md:148-149`, `:155-157`, `:162-163` | S13 (commands; `--help` real or expected) |
| `uv add requests`; `python cli_11.py --download / --synthesis / --upload` | `synthesis_audio/README.md:146`, `:151-153` | S13 |
| `docker login -u <USER NAME> -p <ACCESS TOKEN>`, `docker tag …`, `docker push …` | component READMEs `:138-140` | S14 (commands only) |

## Things never to do on screen

Series rules:
- No Google/GCP logos or console screenshots: schematic drawings tagged `illustration` (the bucket,
  the leaderboard, the Canvas download). Never show `mega-pipeline-bucket.png` or
  `mega-pipeline-flow.png`; V1 redraws the flow.
- No real person's name in captions, labels or narration. The prompt user is `student`; the
  narration says "the instructor" and "the default group name". The only place a name appears is
  where a source line is quoted unchanged because the viewer must find and replace it
  (`group_name = "…"` at `cli.py:21`/`:19`/`:18`). Never quote `generate_text/cli.py:65-71` (the
  prompt names the instructor): quote `:73-81`. Never quote `README.md:9`, `:15` or `:80` text.
- No hand-typed "output": every terminal line comes from `assets/terminal/`; `expected/` panels
  carry the `expected` tag; "what to look for" is a caption list citing `cli.py` lines, never
  styled as terminal output.
- No command spelled differently from the README (the build command is the one exception the
  README forces, said as such).
- No credentials, keys, tokens or project ids that look real. Never draw the key's content or `cat`
  the stand-in file; Docker Hub placeholders stay `<USER NAME>` / `<ACCESS TOKEN>`; avoid
  `cli.py:17` (the course's project id) in panels and never put it in a caption.

Lecture-specific:
- Never show `--network host`, the `l03-capture/` base image, `https://deb.debian.org` apt lines or
  the four capture-only `docker history` rows.
- Never present a Google call as if it ran: no output panels for `--download` (except the
  recorded missing-key run), `--transcribe`, `--upload`, `--generate`, `--synthesis`,
  `--translate`; no audio is played (none exists).
- Never show `docker push` of an image built with the key as something to do; the push commands
  appear only under the RED stamp, after the `.dockerignore` fix is explained.
- Never quote the removed codecast file or present the `solution` branch as today's steps.

## Left for exercises.md (not in the video)

`docker run … transcribe_audio python cli.py -d` → exit 126 and the `-c "source … && python cli.py
…"` fix (`laptop/18`, `19`); arm64 vs amd64 when pushing from a Mac; `-e GEMINI_MODEL=…`;
retargeting D and E to Spanish (what must be deleted to force a redo); the `podcast.mp3` naming
contract; `cd /tmp && python /app/cli.py --help` in `translate_text`; `uv tree --depth 1`
(`transcribe_audio/09`); the `uv sync` layer re-running on every edit and the copy-lock-first
Dockerfile order.
