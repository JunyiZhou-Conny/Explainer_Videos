# AC215 · Lecture 2 — Containers I: one image, from laptop to VM — narration script & visual plan (v2)

Audience: an AC215 student who has done L1 (a Compute Engine VM, venvs, uv, `pyproject.toml`) and
Tutorial 0 (Docker Desktop running, VS Code, git, a GCP project with billing), but has never written
a Dockerfile or thought about what an image is. They watch with the README of
`dlops-io/simple-translate` open, a clone on their **laptop**, a free Docker Hub account and, for the
last part, a VM of their own, pausing to type every command.

Goal: after the video they can check and clean their Docker setup and say what `prune` keeps; write
the README's five-step Dockerfile and say which lines add a layer and which only write on the
config; build with `docker build -t simple-translate -f Dockerfile .` and read the log (`CACHED`,
`naming to …`, the final `.`); predict a container's start-up command line from ENTRYPOINT + CMD and
explain exit 126; explain why a `python:3.12` image runs Python 3.15 (3.14 in the instructor's
image); say what `--rm`, `-t`, `-i` and `exit` do; predict which build steps a rebuild re-runs; tag
and push with a token kept off the command line; check an image's platform and make a Mac-built
image run on a default VM; deploy on a fresh VM that has only Docker, and delete it.

Sources of truth: `BRIEF.md` (design, binding), `digest.md` (tutorial digest), `assets/` (see
`ASSETS.md`). Where the digest and the captures disagree, the captures win. Nothing in a terminal
panel is typed by hand: every output line below names its capture file and line numbers.
v2 merges the four reviews in `build/` (log: `build/review_merge_log.md`).

Conventions
- `SAY:` lines are spoken verbatim by the TTS voice (one `voiceover` block each) and become the
  subtitles. Plain spoken English: no backticks, no symbols; commands and paths are said in words
  ("docker run, dash dash rm, dash t i", "slash dot venv", "user local bin" for `/usr/local/bin`,
  "docker dot I-O" for `docker.io`, so the voice doesn't read "io" as a word).
  File names cli.py, pyproject.toml, uv.lock, Dockerfile.txt, docker-shell.sh and
  docker-build-push.sh, the name simple-translate-ac215, the words RUN, ENV, ENTRYPOINT and buildx,
  and the three-part versions (3.12.15, 3.14.7, 0.12.15, 20.10.24, 26.1.5) are written as they are:
  lexicon entries say them (`explainer/lexicon.yaml`, "# AC215 L02"). Any new `a.b.c` version needs
  its own entry. "dash a" is always followed by a comma or a full stop (before a word the voice reads
  "a" as the article). No sentence opens with "Ours" (heard as "Hours"). Numbers as digits, sizes
  always with their unit; never a "!" after a digit. Versions and sizes that will change are said
  with "at the time of recording". Foreign-language outputs are on screen, not spoken ("comes back in
  Spanish").
- Every spoken sentence starts with a capital letter or a digit (`explainer.voice.split_sentences`
  splits only there; the same split drives TTS gaps, subtitle cues and the Chinese alignment). No
  sentence opens with a command or file name ("The command docker build…", "Then python cli.py…").
  No 's after a word that has a lexicon entry, except `uv's` and `README's`.
- The tutorial's own wording is respected: the README numbers only its five Dockerfile steps, so
  the narration says "Step 1" to "Step 5" only for those. Other README bullets are "first, next,
  then"; the tracker shows their number.
- `SHOW:` lines describe what is on screen during that `SAY:` line, and what moves.
- `PONDER(n s, "question")`: after that SAY block, `pause_and_ponder(self, "question", seconds=n)`
  (silent timer); the card is removed at the start of the next block. Five in the video (BRIEF).
- `TERM(folder/file: lines)`: a terminal beat. The scene types the command written just before it
  in the SHOW line (in backticks, exactly as the README spells it; extras exactly as written here),
  then prints those lines of `assets/terminal/folder/file`. Line 1 of every capture is its `$ …`
  command and is never printed; the `[exit N]` line is never printed. Inside the line list:
  - `…` = print one `…` line;
  - `cut` = the line is cut where the SHOW says and ends in `…` (the FROM lines: see Notes);
  - `hash12` = every long `sha256:` digest in the line is shortened to its first 12 hex digits
    followed by `…` (Docker's own short-ID length), so the line fits one row; nothing else changes;
  - `fit` = a line of the compact build view (`laptop/29`): the padding before the time on the
    right collapses to two spaces and the step text is cut with `…` so that the time stays visible,
    as Docker draws the same view on a narrower terminal;
  - `squeeze` = a table re-aligned with two-space gutters, an empty trailing column dropped;
  - `cols A, B` = only those columns of a table are printed (re-aligned); a GREY caption on the
    terminal names them;
  - `wrap` = fold long lines (`Terminal.print(..., wrap=True)`);
  - `[y/N] y`, `[Y/n] Y` = cut that line after the bracket, pause 0.6 s, type the answer;
  - `+Done` = append apt's " Done" to each "Reading package lists... / Building dependency tree...
    / Reading state information..." line (lost without a terminal; ASSETS.md, as in L1).
  `→ (no output)`: the prompt simply returns.
- Typed lines at a container prompt. The `istep` captures hold the prompt and the typed line
  together (`root@93d61f44d3d7:/# python cli.py …`). The scene sets the terminal's prompt to the
  capture's own `root@<id>:/#` and types the rest of that line, so prompt and command are the
  capture's text. The laptop prompt returns after `exit` (the last `exit` echo line is printed).
  Every run the viewer does ends with a spoken "type exit" before the next laptop command.
- Terminal size. The house `term()`: 12.6 wide, 22 pt, 65 characters a row, always full width. A
  typed command is never cut: it folds at a space onto an indented row. When a picture needs the
  frame, the terminal shrinks to a 3-row strip along the bottom edge (the last command and its key
  line; "strip (5 rows)" where stated) and the picture uses the frame above it. A full terminal and
  a picture never share the frame: the terminal prints first, then shrinks, then the picture moves.
  One exception to the width: the three `ls` listings in columns (`laptop/19: 3–7`, `laptop/22: 3–9`,
  `laptop/33: 22–28`) are up to 73 characters wide; for those beats the terminal is 13.2 wide at
  20 pt (75 characters), so the captured columns stay exactly as they are. Row counts below include
  folded rows; the line a SHOW highlights or a SAY reads must be on screen at that moment.
- `CODE(path: a–b)`: `code_panel(...)` quoting `assets/source/path` from line a to b, header
  `path · lines a–b`; never more than 12 lines on screen at once. The repo's `.gitignore` is stored
  as `assets/source/dot-gitignore.txt`; its panel header says `.gitignore · lines 1–4`. A
  "README card" is a GREY quote of README text with the header `README.md · line n`.
- `TRACKER A3`: the `ReadmeTracker`, top-left, in every walkthrough scene, moves to that step.
  `TRACKER A2 · extra`: same step, caption gets " · extra" while a command the README doesn't have
  is on screen. Three trackers (BRIEF):
  - A = "Developing App using Containers" (`README.md:106-184`), 16 steps: 1 container ls ·
    2 Stop containers · 3 system prune · 4 image ls · 5 Clone repo · 6 Create Dockerfile ·
    7 FROM (1/5) · 8 ENTRYPOINT (2/5) · 9 uv, COPY (3/5) · 10 uv sync (4/5) · 11 CMD (5/5) ·
    12 Solution file · 13 Build image · 14 Run container · 15 Translate · 16 Exit. Steps 7–11 each
    include the README's "Build + Run after each step" (`README.md:130`).
  - B = "Pushing Docker Image to Docker Hub" (`README.md:186-191`), 4 steps: 1 Access token ·
    2 Login · 3 Tag · 4 Push.
  - C = "Running App on VM using Docker" (`README.md:203-220`), 7 steps: 1 Create VM · 2 SSH ·
    3 Install Docker · 4 Docker version · 5 Run image · 6 Run cli · 7 Delete VM.
  S10, S11 and S13 are all extras: the tracker stays on A16, A16 and B4 with " · extra".
- `(extra)` after a command: not in the README. A small GREY tag `extra` sits beside the typed
  line, and the SAY says so at least the first time that command appears. Commands typed inside a
  container during Steps 1–5 (`ls`, `ls -a`, `python cli.py`, `which python` …) are extras too: the
  README's Steps 1–5 only say "Build + Run".
- `▶ your turn`: a YELLOW tag beside the command at a real checkpoint (about one per README step);
  the SAY of that block says "pause". The video doesn't wait: the viewer pauses.
- Tags (GREY unless said): `illustration` on every schematic console, Docker Hub page or editor
  drawing (no logos, no screenshots) and on every "what if" picture; `stand-in · local registry,
  not Docker Hub` (`stand_in_tag()`) with a second line `watch only · don't type` on every
  `laptop-push/04–09` and `13` terminal (the local registry only exists on our machine);
  `stand-in · empty package lists` on the VM's failing `apt install` (S14); `real capture ·
  2026-10-13` on the push denial and the rate-limit run; `at the time of recording` next to
  uv 0.13.0, CPython 3.15.0, Python 3.12.15, the Docker versions and image sizes when first shown;
  `erratum` on every README slip (the narration says "a small slip" or "a small gap", never
  "erratum"). `expected` and `recorded` are not needed in this video: every terminal line is a real
  capture, and the steps without one (console clicks, the Docker Hub token, `docker login` to
  Docker Hub) are README cards or `illustration` drawings with no output.
- The cost meter is L1's GOLD dial whose needle sweeps, with no digits. It never rewinds: Delete
  makes it stop where it is.
- Spelling on screen and in the subtitles: American ("gray", "around").
- Semantic colours (BRIEF, fixed for the whole video):

  | meaning | colour |
  | --- | --- |
  | your laptop: the clone, the files `COPY . ./` brings in, Docker Desktop's hidden Linux VM (dashed) | GREY |
  | the cloud: the VM `ac215-l02`, Docker Hub (a registry shelf), Google's translate endpoint | BLUE |
  | images and containers: every layer's outline, the config card and its ENTRYPOINT/CMD tiles, image IDs and names, the container's thin writable layer (dashed, glowing) | TEAL |
  | OS-owned inside the image: the Debian bookworm base, apt, the base image's Python 3.12.15 at `/usr/local/bin/python` | ORANGE |
  | project-owned: `/.venv`, `uv.lock`, the CPython 3.15.0 uv downloaded for the venv, the `>=3.13` interval | GREEN |
  | tools: docker (CLI, dockerd, BuildKit/buildx, "builder"), uv, Debian's `docker.io` package | PURPLE |
  | errors and "avoid this": `ModuleNotFoundError`, exit 126, `push access denied`, `exec format error`, `Unable to locate package`, `toomanyrequests`, the cache's rebuild wave | RED |
  | your turn, the README tracker, "look here now" | YELLOW |
  | money: the VM's cost tag and dial | GOLD |
  | lookups and routes: PATH lookups, the build context's trip to the builder, push and pull routes, the HTTPS call to Google | PINK |
  | a future thing (L3: five containers, bind mounts) | GREY, dashed |

  Layer slabs always have a TEAL outline and a fill coloured by what they hold: ORANGE for the
  base and the apt/pip `RUN`, GREY for `COPY . ./`, GREEN for `RUN uv sync`. CPU platforms are
  coloured by the machine they belong to: `arm64 · Apple Silicon` GREY, `amd64 · default GCP VM`
  BLUE. Something merely absent (no `Dockerfile` yet, no `uv.lock`, no `.dockerignore`) is GREY
  dashed, not RED.
- Running example. The laptop: user `student`, host `laptop`, prompt `student@laptop:~$`, after
  `cd` `student@laptop:~/simple-translate$`, terminal title `laptop` (the captures' fresh Docker
  29.8.2 engine on linux/amd64 stands in for Docker Desktop). Containers: each prompt comes from
  its own capture. Docker Hub: the README's `<USER NAME>` is `student`; the README line is shown
  with its placeholders and the terminal types the capture's line, with the YELLOW caption
  "`<USER NAME>` = your Docker Hub username (here: student)". The VM: `ac215-l02`, prompt
  `student@ac215-l02:~$`, title `ssh · ac215-l02` (fresh `debian:12` / `debian:13` containers stand
  in, as in L1); Debian 13 appears as a small GREY card where its output differs.
- Length and parts: narration 4,294 words (`python -m explainer.script`; part 1 = 2,348,
  part 2 = 1,946). Measured on v1: 150 wpm with Kokoro af_heart at 0.9 (sentence gaps included),
  so ≈ 28.5 min of narration, ≈ 31–33 min with typing, outputs and ponder timers (L1's 4,287 words
  gave 29:52). Part 1 = S01–S09 (write the Dockerfile, build and run it; ends on A16), part 2 =
  S10–S16 (layers, cache, Docker Hub, platforms, the VM, teardown). Each part ends on an empty frame.

Notes for scene authors
- TERM/PANEL line numbers are *file* lines (line 1 = the `$` command); `Capture.pick()` indexes the
  output body, so pick index = file line − 1.
- `vm-debian12/03` and `vm-debian13/03` contain lone `\r` (dpkg's `(Reading database ... N%`
  progress). Read captures with `open(p, encoding='utf-8', newline='')` and split on `\n` only:
  L1's `Path.read_text()` splits on `\r` too and shifts every later line, so file line 560 would come
  back as a `Created symlink …` line and 581 as an empty one. Or pick `Setting up docker.io` and
  `Processing triggers` by content. (Lines 4–58 of `vm-debian12/03` and 77–78 of `vm-debian13/03`
  come before the first `\r` and are unaffected.)
- Crops that keep panels honest (ASSETS.md, "Differences"): FROM lines from `laptop/18` on carry the
  capture-only digest `4fb3e77d…`: always `cut` them right after `python:3.12-slim-bookworm` (only
  `laptop/09` and `14`'s `34386ef0…` may be shown, cut after `@sha256:34386ef0`). Never print
  `laptop/34` rows 11–13, the `python:3.12-slim-bookworm` row (row 3) of `laptop/30`, `44` and
  `laptop-push/02`, apt's `Get:` lines, or the VM's `invoke-rc.d: …` lines (no systemd in the
  stand-in). The step-by-step builds (`laptop/09`–`24`, `38`, `40`, `41`) are BuildKit's plain log;
  only `laptop/29` is the compact view.
- `laptop/19` and `22` print `ls` in columns: keep the columns (20 pt exception above), highlight by
  substring.
- Labels at ≥ 20 pt are wide (`/usr/local/bin` alone is 2.3 units in mono 20). Slab labels are the
  short Dockerfile line only (≤ 18 characters: "RUN pip install uv", "COPY . ./", "RUN uv sync");
  the base slabs share one brace "base image" with `python:3.12-slim-bookworm` as a mono caption
  under the stack. Version dots get two-line labels (version on top, a 2–3 word role under it).
  Extra facts are said, or sit in a GREY note beside the stack only while no terminal is shown.
- Shared code (`scenes/common.py`, from L1's): `tracker_a/b/c`, prompts `P_LAPTOP_HOME`, `P_LAPTOP`,
  `P_VM`, tags incl. `stand_in_tag()` (two lines, see Tags); set pieces `LayerStack` + `ConfigCard`
  (V2/V3), L1's `VersionLine` and `PathDoors` small (V4), `CacheChain` (V5), `NameTags` +
  `RegistryShelf` (V6), `PlatformMenu` (V7), `KernelPicture` (V8), L1's cost dial.
- Layout of V2 when it shares the frame with a strip terminal: the stack stands left of center
  (≈ 3.2 wide), the config card at its right (≈ 3.6 wide), both above y = −2.0; the tracker owns the
  top-left corner, so the stack starts below it.
- What became what: when a build finishes, the new Dockerfile line(s) on screen (README code panel
  or the strip's `cat` output) are copied down (`TransformFromCopy`) into what they made: a slab for
  RUN and COPY ("adds a layer"), a tile on the config card for ENTRYPOINT and CMD ("config only").

---

## S01 · One command on a fresh VM — `s01_hook.py` · `Hook`

SHOW: Black frame. No tracker yet. A terminal fades in (12.6 wide, 12 rows, title `ssh · ac215-l02`,
prompt `student@ac215-l02:~$`). Above it, three GREY chips "code", "venv", "uv", each crossed RED as
named; a PURPLE `docker` chip gets a GREEN check at "only Docker". At "we type one command" the
typing of `sudo docker run --rm -ti dlops/simple-translate` starts (README.md line 215); a GREY tag
"preview · you'll run it in part 2".
SAY: Here's a fresh virtual machine in the cloud: no copy of our code, no virtual environment, no uv. It has only Docker, and we type one command. Just watch; you'll run it yourself at the end.

SHOW: The command finishes typing → TERM(vm-debian12/06: 2–4, …, 10–12; hash12). The chips fade. A
small BLUE shelf glyph "Docker Hub" sits at top right; a PINK arrow pulses from it into the terminal
as the `Pull complete` lines print, with a counter "7 layers" (lines 4–10 are seven `Pull complete`
lines). The prompt changes to `root@c7c280390994:/#` (line 13) and it types `python cli.py` →
TERM(vm-debian12/06: 16–20, 24; wrap, 26–27). The terminal scrolls; `Output: Adoro il formaggio`
(line 27) highlights GREEN and stays on screen.
SAY: Docker downloads an image, in seven layers, and starts a shell inside it. There we run the app, and its default text, I love cheese, comes back in Italian.

SHOW: It types `python --version` (extra) at the same prompt → TERM(vm-debian12/06: 29);
`Python 3.14.7` highlights YELLOW. The terminal shrinks to the bottom strip; CODE(Dockerfile.txt: 2)
slides in above it, `python:3.12` highlighted ORANGE, and a YELLOW "?" sits between `3.12` and
`3.14.7`.
SAY: One extra check, not in the README: which Python is this? It's 3.14.7. Yet the recipe for this image starts from Python 3.12. Hold that thought; we'll solve it twice today.

SHOW: V1, the ladder, header `README.md · lines 9–16`: four rungs with the README's labels, "1 Manual
install on the VM" (ORANGE), "2 Same VM, but with uv" (GREEN), "3 Docker, on your laptop" (a small
TEAL box inside a GREY laptop), "4 Run the Docker image on a VM" (a TEAL box inside a BLUE VM).
Rungs 1–2 are lit softly with a GREY "L1" tag; rungs 3–4 light up with a YELLOW "today" bracket.
SAY: That's where today's tutorial, simple-translate, ends. Last lecture we climbed its first two rungs: a manual install on a VM, then uv. Today, the other two: package the app as a Docker image on your laptop, push it to Docker Hub, and run it on a VM.

SHOW: A layout preview, built piece by piece as named: a README page glyph appears; at "Three
trackers" its outline flies to the top-left corner and becomes a YELLOW ring around the real tracker
A (`tracker_a(1)`: "README › Developing App using Containers", 16 dots, "step 1 of 16: container
ls"), with a GREY laptop icon beside the ring at "on the laptop"; at "on Docker Hub" the tracker
changes in place to `tracker_b(1)` (icon: a BLUE shelf), at "on the VM" to `tracker_c(1)` (a BLUE
VM); the ring follows each tracker's width. At "When the yellow" a 2-row strip terminal at the
bottom (GREY tag "preview", prompt `student@laptop:~$`) fades in, the tracker goes back to A, step 1,
and the strip types `docker container ls` (README A1) with a YELLOW `▶ your turn` row tag; then
`ls -a` with the GREY `extra` row tag, and the tracker caption gains " · extra"; a footer caption:
"every command: MLOps_Learning · guides/L02-containers-1.md · link in the description".
SAY: To follow along, open the README beside this video. Three trackers, top left, show where we are: on the laptop, on Docker Hub, on the VM. When the yellow your-turn tag appears, pause and run the command; a gray extra tag marks a check that isn't in the README.

SHOW: The preview clears. A checklist card: "✓ Docker Desktop running (Tutorial 0)", "✓ a free
Docker Hub account", "✓ your GCP project, for the VM at the end", and GREY "✗ no service account,
no keys (README.md · line 23)". A GOLD tag "a VM costs money while it exists" beside the third item.
Fade out.
SAY: You need Docker Desktop running, a free Docker Hub account, and your Google Cloud project for the VM at the end. No service account or keys today.

---

## S02 · Image, layer, container, registry — `s02_nouns.py` · `FourNouns`

SHOW: No tracker (concept scene). A GREY header across the top, `image · layer · container ·
registry`; each word turns TEAL when it is defined (image and layer in block 2, container in
block 4, registry in block 6). L1's closing picture, small at left: a BLUE VM box holding a GREEN
venv box. At "the same setup", three GREY chips appear beside it, `apt`, `git clone`, `uv sync`,
plus a RED-outlined "the right OS". At "packs it all into one thing", each setup chip transforms
into what it produced, lighting as named: `apt` → ORANGE "OS files" and ORANGE "Python", `uv sync` →
GREEN "packages", `git clone` → GREY "your code"; a TEAL box closes around the four; caption under it:
"an image".
SAY: First, four words for the whole lecture. In lecture 1, every new VM needed the same setup, on an operating system that had to cooperate. A Docker image packs it all into one thing you can copy: system files, Python, the packages and the code.

SHOW: V2 on a generic stack, center-left: the TEAL box opens into three translucent slabs with TEAL
outlines that drop bottom-up, labelled "OS files" (ORANGE fill), "packages" (GREEN), "your code"
(GREY); a small lock glyph on the stack's side, "read-only". At right, a TEAL config card with four
empty rows `ENV`, `ENTRYPOINT`, `CMD`, `WorkingDir`. GREY tag `Lecture 2 · slides 30–31, 35` (top
right, from "An image is a stack of read-only layers" through "Think of the image as a class").
SAY: An image is a stack of read-only layers. Each layer holds the files added or changed by one build step. Beside it sits a small config card: settings like environment variables, and which program to start.

SHOW: A GREY page glyph "Dockerfile" at far left with four lines `FROM …`, `RUN …`, `COPY …`,
`CMD …`. As each highlights: FROM points at the base slab; RUN and COPY each send a slab arrow onto
the stack, tag "adds a layer"; CMD sends an arrow to the card's CMD row, tag "config only".
SAY: The recipe is a Dockerfile, read one instruction at a time. Instructions that change files, like RUN and COPY, add a layer. Others, like CMD, only write on the card.

SHOW: The page fades. "docker run": a dashed, glowing TEAL glass slab appears on top of the stack
("writable layer") with a TEAL dot "main process" inside; the group gets the label "container". A
second container appears: a second glass slab and dot beside the first, both linked by thin lines to
the SAME stack, caption "shared, not copied". The first dot goes out ("process ended → stopped"); a
chip `--rm` dissolves that whole container, its glass slab and its label. The stack is unchanged:
GREEN check "image unchanged".
SAY: Run an image and you get a container: the same layers, shared, plus a thin writable layer on top, and one main process. When that process ends, the container stops, and dash dash rm deletes it, writable layer and all. The image never changes.

SHOW: The container picture shrinks left; two captions under it: "image = class" · "container =
instance" (TEAL). The captions fade; a README card (`README.md · line 173`): "Build the docker
container", the word "container" struck YELLOW with "image" written above it, tag `erratum`; a
second card slides in under it as part of the same group (`README.md · line 146`): "copy source code
into the container", "container" struck the same way.
SAY: Think of the image as a class, and each container as an instance. One small slip in the README: it says build the docker container. Building makes an image; running makes a container.

SHOW: The cards fade. A BLUE shelf unit at right, "registry · Docker Hub". Small TEAL stacks stand
on it with sticky notes `python:3.12-slim-bookworm` and `dlops/simple-translate:latest`. A note
`:latest` peels off and sticks to a newer stack; caption "a tag: a name that points at one image".
SAY: A registry, like Docker Hub, stores images by name, on shelves. A tag is a name that points at one image, such as latest.

SHOW: V8, first half. Three BLUE VM boxes side by side, each with its own "kernel" bar and an "OS"
band (L1's server slices). At "share one Linux kernel", the three kernel bars slide down and merge
into one GREY bar "Linux kernel · shared", and the VM outlines shrink into three TEAL "container"
boxes standing on it; caption "isolated processes, not machines". Two small GREY chips sit on the
shared kernel bar, "namespaces" and "cgroups", and a GREY caption "user space" beside the containers.
GREY tag `Lecture 2 · slides 9–12, 22–24` (top right, from "And a container is not a small VM" to
the end of the scene).
SAY: And a container is not a small VM. A VM boots its own kernel, the core of the operating system. Containers are isolated processes that share one Linux kernel.

SHOW: V8, second half. A GREY laptop outline wraps the picture; a dashed GREY box "Linux VM · Docker
Desktop" slides in under the kernel bar, labelled "Mac · Windows". Then the laptop outline morphs
into a BLUE VM outline and the dashed box fades: caption "on a cloud VM: its own Linux".
SAY: On a Mac or Windows laptop, Docker Desktop provides that kernel with a small, hidden Linux VM. On a cloud VM, Docker runs right on the VM's own Linux.

SHOW: L1's three chips return: two RED-outlined, "the operating system's files" and "system
libraries", fly into the TEAL stack, turning ORANGE fills (GREEN check); the third, "GPU drivers",
stays outside and, at "GPU drivers still come from the host", turns GREY, "still the host's". Fade
out.
SAY: What a venv couldn't isolate in lecture 1, the system's files and libraries, is now inside the box. GPU drivers still come from the host.

---

## S03 · A clean slate, and the clone — `s03_cleanup.py` · `CleanSlate`

SHOW: TRACKER A1 (the tracker appears: "README › Developing App using Containers", 16 dots, with a
YELLOW pulse). A full-width laptop terminal fades in (title `laptop`, 10 rows, prompt
`student@laptop:~$`); a GREY note under it: "on a Mac: zsh, a % prompt · on Windows: Git Bash ·
same commands". A small GREY chip "Docker Desktop: running" with a GREEN dot at the terminal's top
right.
SAY: Now the README section Developing App using Containers. Open a terminal on your laptop. On a Mac your prompt looks different; on Windows, use an Ubuntu terminal in WSL, or Git Bash. In Git Bash, put winpty in front of docker run if it says stdin is not a terminal.

SHOW: TRACKER A1. It types `docker container ls` → TERM(laptop/01: 2). The header row gets a GREY
label "the columns · no rows: nothing running". `▶ your turn`. A GREY chip under the terminal:
"cannot connect? → start Docker Desktop" (the error is said, not printed: no capture). GREY tag
`Lecture 2 · slides 54, 61–62, 73` (top right, from "First, docker container ls lists running
containers" to the end of the scene).
SAY: First, docker container ls lists running containers. Here it shows only the header, so nothing is running. If yours can't connect to the Docker daemon, start Docker Desktop and try again. Pause and run it.

SHOW: TRACKER A2. A README card (`README.md · line 116`): "Stop any container that is running".
Beside it a GREY chip `docker stop <CONTAINER ID>` with the tag "only if you have one · not run
here".
SAY: Next, stop any running container. There's nothing to stop here; if you have one, docker stop with its ID does it.

SHOW: TRACKER A3. It types `docker system prune` → TERM(laptop/02: 2–9; [y/N] y). The `y` keystroke
flashes YELLOW; line 9 (`Total reclaimed space: 0B`) gets a GREY label "a fresh Docker · yours may
reclaim hello-world's container". `▶ your turn`.
SAY: Then docker system prune. It lists what it will remove and asks; type y. Nothing to reclaim here; yours may delete the stopped hello-world container from Tutorial 0. Pause and run it.

SHOW: TRACKER A3. Line 5 (`  - all dangling images`) highlights YELLOW with a GREY label "images
with no name". Beside the terminal, two small TEAL stacks: one with a name tag gets a GREEN check
"named: kept"; one tagged `<none>` is swept away (FadeOut + shift) as "without a name" is said. A
README card (`README.md · line 113`): "clear up an unused images", tag `erratum`; a GREY chip
`docker system prune -a` "every unused image".
SAY: Look at the third item: dangling images, the ones without a name. Despite the README's heading, named images survive. With dash a, prune would remove every unused image.

SHOW: TRACKER A4. It types `docker image ls` → TERM(laptop/03: 2; squeeze). The empty table gets a
GREY caption "no images yet · yours may list hello-world" and the tag `at the time of recording`
beside the header ("Docker 29's columns"). `▶ your turn`.
SAY: Then docker image ls lists your images. The list is empty here; yours may still show hello-world: it has a name, so it survived. Your columns may differ: this is Docker 29, at the time of recording.

SHOW: TRACKER A5. A README card (`README.md · lines 122–123`): "If you cloned earlier on a VM, that
doesn't help here — Docker Desktop runs on your laptop". A small BLUE VM glyph holding a folder gets
a RED cross; a GREY laptop glyph gets a folder `simple-translate`. The terminal types
`git clone https://github.com/dlops-io/simple-translate.git` (folds onto a second row) →
TERM(laptop/04: 2), then `cd simple-translate` → (no output); the prompt becomes
`student@laptop:~/simple-translate$` and its new path flashes BLUE. A GREY tag "README.md · lines
50–51 · same as L1". `▶ your turn`.
SAY: Now the code. As the README notes, a clone on last lecture's VM doesn't help: Docker Desktop runs on your laptop. Clone it here, then cd into simple-translate. Pause and run both.

SHOW: TRACKER A5 · extra. It types `ls -a` (extra) → TERM(laptop/05: 4–12). `Dockerfile.txt`
highlights with a GREY tag "the solution"; two GREY dashed ghost chips appear beside the listing,
`Dockerfile` and `uv.lock`, captioned "not in the repo".
SAY: An extra check, not in the README: ls dash a. There's the solution, Dockerfile.txt, but no file called just Dockerfile, and no uv.lock.

SHOW: TRACKER A5 · extra. It types `docker build -t simple-translate -f Dockerfile .` (extra here: the
README's build command, run too early) → TERM(laptop/07: 7; wrap), RED. Fade out.
SAY: Run the README's build command now, as an extra: failed to read dockerfile. The README wants you to write it, in five steps.

---

## S04 · Dockerfile step 1: FROM — `s04_from.py` · `StepFrom`

SHOW: TRACKER A6. A schematic editor sidebar (tag `illustration`): the file tree `simple-translate/`
with the entries of laptop/05 (`.git/`, `.gitignore`, `.vscode/`, `Dockerfile.txt`, `README.md`,
`cli.py`, `docker-build-push.sh`, `docker-shell.sh`, `pyproject.toml`); a new row `Dockerfile`
slides in YELLOW with the tag "exactly this name · no extension". A README card
(`README.md · lines 128–130`): "create a file called Dockerfile … (Do a Build + Run after each
step)". `▶ your turn`.
SAY: Next, inside the simple-translate folder, create a file called Dockerfile: capital D, no extension. The README fills it in five steps, with a build and a run after each. Pause and create the file.

SHOW: TRACKER A7. CODE(README.md: 135–136) at the top. Under `python:3.12-slim-bookworm`, four
chips decode the name: `python` "official image", `3.12` "Python 3.12", `slim` "fewer packages",
`bookworm` "Debian 12". The strip terminal below types `cat Dockerfile` (extra) →
TERM(laptop/08: 2–3).
SAY: Dockerfile step 1 is one instruction: FROM python, 3.12, slim bookworm. That's the official Python image, on a slim Debian 12 called bookworm. Paste it in, save, and check with cat, an extra.

SHOW: The panel fades. The build command writes large in the center,
`docker build -t simple-translate -f Dockerfile .` (header `README.md · line 174`), and its parts get
labels in turn: `-t simple-translate` "the image's name" (TEAL), `-f Dockerfile` "the recipe", `.`
"build context: this folder" (PINK, pulsing). At "sends to the builder", a small GREY folder glyph
slides from the `.` along a PINK arrow into a PURPLE chip "builder" (S06's parcel reuses this chip).
GREY tag `Lecture 2 · slides 32, 56` (top right, from "Now the build command. Dash t names the image
simple-translate", through the build).
SAY: Now the build command. Dash t names the image simple-translate; dash f picks the recipe. And the final dot is the build context: this folder, which Docker sends to the builder. Step 3 shows why that matters.

SHOW: The command slides into a full-width terminal (13 rows, prompt
`student@laptop:~/simple-translate$`) and is typed → TERM(laptop/09: 2, …, 15; cut after
`@sha256:34386ef0`, …, 31–34; hash12, …, 38). `▶ your turn`. Two GREY notes appear as said: across
the top, "your terminal: a compact view · this is the full log (--progress=plain)"; next to line 2's
`"default"`, "Docker Desktop: builder "desktop-linux" · and a "View build details" link at the end".
A third GREY note fades in at the bottom edge: "stops with toomanyrequests? → wait a while, or
docker login (part 2)".
SAY: Pause and run the build. Your terminal shows a compact view. Here you see the full log; to get it, add dash dash progress equals plain. On Docker Desktop, the builder is called desktop linux, not default.

SHOW: The notes fade. The four sizes (`3.34MB`, `15.97MB`, `28.25MB`, `249B`) highlight ORANGE in
turn, then `simple-translate:latest` in line 38 highlights TEAL. The terminal shrinks to the strip
and V2 starts: four equal thin ORANGE slabs with TEAL outlines drop as one group under one brace
"base image", with `python:3.12-slim-bookworm` as a mono caption under the stack; the four download
sizes fly out of the strip into a small list beside the brace, "≈ 47.6 MB compressed" (no size sits
on any one slab).
SAY: Docker fetches the base image, four layers, under 50 megabytes compressed, and saves the result as simple-translate, tagged latest. Those four layers are the bottom of our stack.

SHOW: TRACKER A7 · extra. Strip terminal (5 rows) types
`docker image inspect simple-translate --format 'Entrypoint={{json .Config.Entrypoint}} Cmd={{json .Config.Cmd}} WorkingDir={{json .Config.WorkingDir}}'`
(extra; folds) → TERM(laptop/10: 2). V3 on the TEAL config card beside the stack: two slots,
ENTRYPOINT `[ ]` (empty, GREY "null") and CMD holding a tile `["python3"]` tagged "inherited from the
base image"; WorkingDir `""`. Below the card, the start-up line assembles in mono: `python3` → a
small `>>>` glyph.
SAY: What will it do when it starts? An extra docker image inspect reads the config card: no entrypoint, and the command python3, inherited from the base image. So we predict a Python prompt.

SHOW: TRACKER A7. Full terminal; it types `docker run --rm -ti simple-translate` (README.md line 180);
two GREY labels appear under the flags as they are said, `--rm` "clean up on exit", `-ti` "type into
it" → TERM(laptop/11: 2–3); at the `>>>` prompt it types `exit()` (line 4). `Python 3.12.15` gets the
tag `at the time of recording`. `▶ your turn`.
SAY: Now the run command: docker run, dash dash rm, dash t i, simple-translate. Dash dash rm cleans up afterwards; dash t i lets you type into it. Pause and run it. There's the Python prompt, 3.12.15 at the time of recording. Type exit with parentheses to leave.

SHOW: TRACKER A7 · extra. It types `git status` (extra) → TERM(laptop/12: 2–5); line 5 highlights.
CODE(dot-gitignore.txt: 1–4) slides in (header `.gitignore · lines 1–4`), line 3 `Dockerfile`
highlighted YELLOW, tag `erratum`; a GREEN chip `git add -f Dockerfile` "to commit it anyway".
Fade out.
SAY: One surprise: an extra git status says nothing to commit, though we just made a file. The gitignore file here lists Dockerfile on line 3, so git hides yours. To commit it anyway, use git add dash f.

---

## S05 · Step 2: ENTRYPOINT — `s05_entrypoint.py` · `StepEntrypoint`

SHOW: TRACKER A8. CODE(README.md: 142) at the top. Strip terminal (5 rows) types `cat Dockerfile`
(extra) → TERM(laptop/13: 2–5); line 5 highlights.
SAY: Step 2 adds one line: ENTRYPOINT, slash bin slash bash. Put it under the FROM line, and save.

SHOW: Full terminal; it types `docker build -t simple-translate -f Dockerfile .` → TERM(laptop/14: 15; cut after `@sha256:34386ef0`, 17, …, 25).
`#4 CACHED` highlights TEAL. `▶ your turn`. The terminal shrinks to the strip: the V2 stack (four
ORANGE slabs) is unchanged, and the README panel's line `ENTRYPOINT ["/bin/bash"]` is copied down
(TransformFromCopy) into the config card's ENTRYPOINT row as the tile `["/bin/bash"]`; caption
"config only: nothing downloaded, no new layer".
SAY: Pause and build again. The FROM step says CACHED: nothing is downloaded, and no layer is added. ENTRYPOINT only writes on the config card.

SHOW: V3 close-up of the card: the tile `["/bin/bash"]` sits in the ENTRYPOINT slot; the CMD slot
still shows the inherited `["python3"]` tile, now dashed; the start-up line reads
`/bin/bash python3` with a YELLOW "?". Two GREY labels under the slots: ENTRYPOINT "the program",
CMD "its default arguments". GREY tag `Lecture 2 · slides 32–33` (top right, from "Think of ENTRYPOINT
as the program to start").
SAY: Think of ENTRYPOINT as the program to start, and CMD as its default arguments. The entrypoint is now bash, and the command slot still says python3. So will the container start bash, running python3?

SHOW: TRACKER A8 · extra. Strip types
`docker image inspect simple-translate --format 'Entrypoint={{json .Config.Entrypoint}} Cmd={{json .Config.Cmd}}'`
(extra; folds) → TERM(laptop/15: 2). `Cmd=null` highlights; the `["python3"]` tile falls off the
card and fades; the start-up line becomes `/bin/bash`.
SAY: This extra inspect says no: the entrypoint is bash, and the command is now null. Setting an entrypoint resets the command you inherited from the base image. So bash starts on its own.

SHOW: Full terminal; it types `docker run --rm -ti simple-translate` → the prompt
`root@f72851da4a58:/#` appears (laptop/16 line 2). `▶ your turn`. The prompt is copied large above the terminal
and splits into three labelled parts: `root` "you, the administrator, inside" · `f72851da4a58` "the
container's ID · new every run" · `/` "the top folder", with a GREY chip from laptop/10 line 2,
`WorkingDir=""`, "no WORKDIR".
SAY: Pause and run it: a bare prompt. Read it left to right. You're root, the administrator, inside the container. After the at sign comes the container's ID, which changes every run, so yours will differ.

SHOW: The slash part pulses; the GREY chip `WorkingDir=""` pulses with it. It types `exit` (capture
line 2) → TERM(laptop/16: 3); the laptop prompt returns. Fade out.
SAY: And the slash means you start in the top folder of the image, because this image sets no working directory. Type exit to leave.

---

## S06 · Step 3: install uv, copy the code — `s06_copy.py` · `StepCopy`

SHOW: TRACKER A9. CODE(README.md: 148–151) at the top; line 149 `RUN pip install uv` highlights
(a PURPLE `uv` chip pops beside it), then line 151 `COPY . ./`: the first `.` gets a GREY label "this
folder", `./` "the image's top folder". Strip terminal (5 rows) types `cat Dockerfile` (extra) →
TERM(laptop/17: 7–10).
SAY: Step 3 adds two instructions. RUN pip install uv uses the pip of the base image to install uv. And the COPY line copies this folder, dot, into the image's top folder, dot slash. Add both at the end, and save.

SHOW: V5 seed (strip hidden). The GREY project folder `simple-translate/` with file glyphs, `.git/`
and `Dockerfile` among them. The `.` at the end of the build command (written small above) lights
PINK; the whole folder packs into a parcel labelled "build context" and slides along a PINK arrow
into S04's PURPLE "builder" chip, now a box. Over the arrow hangs a GREY dashed sieve
`.dockerignore`, with the tag "none in this repo". In the builder, the parcel unpacks into the top
folder `/` of the TEAL stack.
SAY: Here's why the final dot matters. Docker packs the whole folder into one parcel, the build context, and sends it to the builder. Every file goes in, the hidden git folder and your Dockerfile too; a file called dot dockerignore could leave some out, but this repo has none. The COPY line unpacks it all into the image's top folder.

SHOW: Full terminal (13 rows); it types `docker build -t simple-translate -f Dockerfile .` → TERM(laptop/18: 12–13, 16–17). Line 13
(`transferring context: 2B`) gets the GREY tag "no .dockerignore"; `63.12kB` in line 17 highlights
PINK, "the parcel". `▶ your turn`.
SAY: Pause and build. The log confirms it: there's no dockerignore file, so nothing is filtered out, and the whole context, 63 kilobytes here, travels to the builder.

SHOW: The terminal continues → TERM(laptop/18: …, 27, 33, 34; wrap, …, 40–41). `uv-0.13.0` gets the
tag `at the time of recording`; the folded WARNING (line 34) gets a YELLOW bracket. The terminal
shrinks to the strip; the panel's two lines are copied down into V2: `RUN pip install uv` becomes an
ORANGE slab with a PURPLE `uv` chip, `COPY . ./` a GREY slab with file glyphs; caption "adds a
layer" on each.
SAY: Then pip installs uv, version 0.13.0 at the time of recording, and COPY runs: two new layers. Pip also warns about running as root. In lecture 1 that warning mattered; here, the image itself is the isolation.

SHOW: The V2 stack with its two new slabs, above the strip.
PONDER(6 s, "uv is installed and the code is copied in.\nWill python cli.py run?")
SAY: Something to ponder: uv is installed, and the code is in the image. Will python cli.py run?

SHOW: TRACKER A9. Full terminal (13.2 wide, 20 pt for the `ls` columns); it types
`docker run --rm -ti simple-translate` with `▶ your turn` beside it → at the prompt
`root@1f2c7df8735d:/#`, TRACKER A9 · extra, `ls` (extra) → TERM(laptop/19: 3–7): `Dockerfile`,
`Dockerfile.txt`, `README.md`, `cli.py`, `pyproject.toml`, `docker-build-push.sh`, `docker-shell.sh`
brighten GREY-white, the system folders (`bin`, `etc`, `usr` …) dim ORANGE.
SAY: No. Pause and run it, then look around with ls, an extra: our files sit right next to the system's own folders.

SHOW: TRACKER A9 · extra. At the same prompt it types `python cli.py` (extra) → TERM(laptop/19: 9–12),
lines 9–12 RED; then `exit` → TERM(laptop/19: 14). Then the terminal shrinks to a 3-row strip
keeping the RED `ModuleNotFoundError` line; above it the V2 stack: the PURPLE `uv` chip glows, and a
dashed GREY slot "packages: none yet" appears on top of the stack. Fade out.
SAY: Then python cli.py, another extra: ModuleNotFoundError, no module named art. We installed the installer, not the packages. Type exit.

---

## S07 · Step 4: uv sync, and two Pythons — `s07_uv_sync.py` · `StepUvSync`

SHOW: TRACKER A10. CODE(README.md: 157), `RUN uv sync` GREEN; above it a README card
(`README.md · line 155`): "Setup a virtual environment by running uv sync".
SAY: Step 4 adds RUN uv sync; add it at the end, and save. Like on last lecture's VM, it reads pyproject.toml and installs the packages into a venv.

SHOW: CODE(Dockerfile.txt: 2) (`3.12` ORANGE) beside CODE(pyproject.toml: 6) (`>=3.13` GREEN), and
three GREY answer chips: "fail?", "use 3.12 anyway?", "something else?".
PONDER(8 s, "This image's Python is 3.12.\npyproject.toml asks for 3.13 or newer.\nWhat will uv sync do during the build?")
SAY: Now predict. This image's Python is 3.12, and line 6 of pyproject.toml asks for 3.13 or newer. What will uv sync do during the build?

SHOW: Full terminal (12 rows); it types `docker build -t simple-translate -f Dockerfile .` → TERM(laptop/21: 23–24, 26–27). `#6 CACHED`
highlights TEAL; `#7 DONE 0.1s` highlights YELLOW with a GREY note "COPY ran again · part 2".
`▶ your turn`.
SAY: Pause and build. First, notice: the pip step says CACHED, but COPY says DONE: it ran again, although we only added a line. Keep that question for part 2.

SHOW: The terminal continues → TERM(laptop/21: 29, 30; wrap, 32–34, 36–37, …, 47). Line 30
(`Downloading cpython-3.15.0-linux-x86_64-gnu (download) (35.9MiB)`) highlights PURPLE, `3.15.0`
gets the tag `at the time of recording`, and a GREY note "Apple Silicon: …linux-aarch64-gnu";
`/.venv` (line 33) and `Installed 11 packages` (line 36) highlight GREEN.
SAY: Now the answer. As on the Debian 12 VM in lecture 1, uv downloads its own Python: CPython 3.15.0, at the time of recording. Then it creates a venv at slash dot venv, and installs 11 packages.

SHOW: The terminal shrinks to the strip; the stack is hidden. V4 full width above the strip (L1's
number line, ticks 3.10 … 3.16): a GREEN glow covers 3.13 and up, labelled `requires-python =
">=3.13"`. An ORANGE dot lands on 3.12 with a RED cross, two-line label `3.12.15` / "base image". A
PURPLE arrow from a uv chip drops a GREEN dot into the glow, label `3.15.0` / "uv download ·
35.9 MiB", tag "newest stable · at the time of recording"; a GREEN chip `/.venv/bin/python` draws a
link arrow to it. Then the number line fades except the GREEN dot; the stack slides in from the
right, and the README panel's `RUN uv sync` line and the dot fly into it together and expand into a
fat GREEN slab "RUN uv sync"; a 2-line GREY note beside it, "CPython 3.15.0 + /.venv · 11 packages".
SAY: On the number line, the requirement covers 3.13 and newer. The base image's 3.12 falls outside, so uv downloads the newest stable Python it knows in the range, and the python in the venv links to it.

SHOW: TRACKER A10. Full terminal (13.2 wide, 20 pt); it types `docker run --rm -ti simple-translate`
with `▶ your turn` beside it → at the prompt `root@01dca6d0f4d8:/#`, TRACKER A10 · extra, `ls -a`
(extra) → TERM(laptop/22: 3–9): `.venv` and `uv.lock` highlight GREEN. Then `python cli.py` (extra)
→ TERM(laptop/22: 11–14), RED.
SAY: Pause and run it, then two extras: ls dash a, which also lists hidden files, and python cli.py. Now the listing shows dot venv, and a new uv.lock. But python cli.py fails exactly as before. Why?

SHOW: The terminal shrinks to the strip. V4's PATH half: L1's doors, from the base image's
`ENV PATH=/usr/local/bin:/usr/local/sbin:/usr…` (laptop/34 line 22, as a GREY chip): `/usr/local/bin`
(ORANGE), `/usr/local/sbin`, `…`. A figure carrying `python` knocks on the first door and walks in to
the ORANGE `3.12.15` dot: "no art, no googletrans" → RED. Caption "venv not activated".
SAY: Remember lecture 1: activation is just PATH. Nothing has activated the venv, so the word python first finds the Python in user local bin, from the base image. That's 3.12, and it has none of our packages.

SHOW: Picture first: a GREEN door `/.venv/bin` slides in at the front of the door row
(`PathDoors.insert_front`) and the `python` figure walks through it to the GREEN `3.15.0` dot. Then
the strip (5 rows, TRACKER A10 · extra) types `.venv/bin/python --version` (extra) → TERM(laptop/22: 16),
then `source .venv/bin/activate && python cli.py` (extra) → TERM(laptop/22: 28; wrap, 30–31) (it
scrolls; `Output: Adoro il formaggio` GREEN stays visible); the prompt `(app) root@01dca6d0f4d8:/#`
(line 32) with `(app)` GREEN; then `exit` → TERM(laptop/22: 33): the laptop prompt returns.
SAY: Activating the venv would put its bin folder in front, and python would find 3.15.0. Two extra checks confirm it: the venv's own python reports 3.15.0, and after sourcing the activate script, python cli.py works. The prompt now shows app in parentheses. Type exit to get back to your laptop.

SHOW: The two dots side by side, two-line labels: ORANGE `3.12.15` / "base · only ran pip install uv",
GREEN `3.15.0` / "uv download · runs the app". S01's YELLOW "?" returns between `3.12` and a GREY
`3.14.7`, now half solved. Tag `erratum` (README.md line 133, Dockerfile.txt line 2 vs
pyproject.toml line 6). Two GREEN fix chips: `FROM python:3.13-slim-bookworm` · "or a requires-python
the image already meets". Fade out.
SAY: So this image carries two Pythons: 3.12 from the base, which only installed uv, and 3.15 for the app. That's half of the opening puzzle, and a small mismatch in the tutorial. In your own projects, start from a Python 3.13 image, or make requires-python match the image.

---

## S08 · Step 5: CMD, the solution, the build — `s08_cmd.py` · `StepCmd`

SHOW: TRACKER A11. CODE(README.md: 163–164) at the top. Strip terminal (5 rows) types
`cat Dockerfile` (extra) → TERM(laptop/23: 14–15).
SAY: Step 5 adds the last instruction, CMD. It holds dash c and one quoted command: source the activate script, then exec bash. Add it at the end, and save.

SHOW: V3 card (the strip hidden): the panel's CMD line is copied down (TransformFromCopy) into the
tile `["-c", "source .venv/bin/activate && exec bash"]`, which slides into the CMD slot beside
ENTRYPOINT `["/bin/bash"]`. Both tiles slide down and merge (TransformMatchingStrings) into the
start-up line `/bin/bash -c "source .venv/bin/activate && exec bash"`; GREY note "bash -c: run this
string, then exit".
SAY: On the card, the entrypoint and the command join into one command line: bash, dash c, then that string. On its own, bash dash c runs the string and exits.

SHOW: The card fades; the start-up line moves up. A bubble "bash 1" runs `source …`: a two-door row
(`/usr/local/bin` ORANGE, `…`) gets a GREEN `/.venv/bin` door at the front; at "exec bash", bubble 1
morphs in place (Transform) into "bash 2 · interactive", the door row unchanged, a prompt cursor
blinking in it.
SAY: Here the string first sources the activate script, which puts the bin folder of the venv first in PATH. Then exec bash swaps this bash for an interactive one that keeps the new PATH and gives you a prompt.

SHOW: Full terminal (12 rows); it types `docker build -t simple-translate -f Dockerfile .` → TERM(laptop/24: 23–24, 26–27, 29, 30; wrap).
`▶ your turn`. Lines 27 and 30 highlight YELLOW, GREY note "one line added · part 2 explains".
SAY: Pause and build. Again COPY and uv sync run, and Python downloads again, for one added line. Part 2 explains why.

SHOW: It types `docker run --rm -ti simple-translate` → at the prompt `root@473b6edd3dab:/#`
(TRACKER A11 · extra): `which python`, `python --version`, `echo $VIRTUAL_ENV` (extras) →
TERM(laptop/26: 3, 5, 7), then `exit` → TERM(laptop/26: 9). `▶ your turn` beside the run. The prompt
gets a GREY tag "no (app)"; `/.venv/bin/python`, `Python 3.15.0` and `/.venv` highlight GREEN; a GREY
tag "not an error". GREY tag `Lecture 2 · slides 64, 75` (top right, during the bridge, from "The
lecture's run command"). After `exit`, the returned prompt `student@laptop:~/simple-translate$` holds
for a beat with a YELLOW pulse.
SAY: Pause and run it. No app in parentheses this time; is the venv active? These extra checks say yes: which python points into dot venv, it's 3.15.0, and the virtual env variable is set. The fresh bash set its own prompt. The lecture's run command adds dash dash entrypoint, which drops this CMD, and the venv with it. Then type exit, back to your laptop.

SHOW: TRACKER A12 · extra. A README card (`README.md · lines 167–168`): "Solution Dockerfile:
Dockerfile.txt". The terminal clears (the laptop prompt stays); it types
`diff Dockerfile Dockerfile.txt` (extra) → TERM(laptop/27: 8–18) (11 rows; `+` lines GREEN, `-` lines
dim RED); a GREY note on the frame "our diff prints + and − · on a Mac, Linux or Git Bash: diff -u
for this layout". The three `+ENV` lines (10, 15, 18) get GREY labels: "no apt questions", "UTF-8
text", "logs appear at once". A GREY note under the diff: "lecture slide 57: a different version ·
build this file"; GREY tag `Lecture 2 · slides 57` (top right, from "The README then points to a
solution, Dockerfile.txt.").
SAY: The README then points to a solution, Dockerfile.txt. An extra diff shows what it adds; if yours prints less-than and greater-than signs, add dash u. First, three ENV lines: no questions from apt, a UTF-8 locale, and unbuffered logs.

SHOW: The terminal continues → TERM(laptop/27: …, 20–26, …, 33–34; wrap) (it scrolls). Lines 21–26
get an ORANGE bracket "one RUN: update, upgrade, clean, newer pip, uv"; lines 33–34 a YELLOW bracket
"ENTRYPOINT moved to the end".
SAY: Second, one bigger RUN: update and upgrade the Debian packages, clean up, upgrade pip, and install uv. And ENTRYPOINT moved to the end: the order of ENTRYPOINT and CMD doesn't matter.

SHOW: TRACKER A12 · extra. It types `cp Dockerfile.txt Dockerfile` (extra) → (no output). GREY note
"the README only names the file". `▶ your turn`.
SAY: The README only names the file. So here's the quickest way, an extra command: copy it over yours with cp. Pause and do that.

SHOW: TRACKER A13. A README card (`README.md · lines 172–174`): "In a terminal make sure you are the
location of simple-translate". The terminal clears; it types
`docker build -t simple-translate -f Dockerfile .` → TERM(laptop/29: 3; fit, 9; cut after
`python:3.12-slim-bookworm`, 13–15; fit, 22; fit) — the compact view. `▶ your turn`. `13.3s` and
`4.9s` highlight; `simple-translate:latest` highlights TEAL; GREY tag "what your terminal shows".
Fade out.
SAY: Now the README's Build Docker Image section: from the simple-translate folder, the same build. Pause and run it. This compact view is what you'll see: four steps, the apt and pip step the slowest.

---

## S09 · Run it, translate, exit — `s09_run.py` · `RunIt`

SHOW: TRACKER A14. Full terminal (13 rows). It types `docker run --rm -ti simple-translate` → the
prompt `root@93d61f44d3d7:/#` (laptop/31 line 2). TRACKER A15. It types
`python cli.py -t "Good morning" -s "en" -d "es"` (README.md line 182; folds) →
TERM(laptop/31: 5–9, 13; wrap, 15–16): banner, arguments, `Input: Good morning`, `Output: Buen día`
GREEN. `▶ your turn`. GREY tag `Lecture 2 · slides 63–65, 74` (top right, from "Now the README's Run
Docker Container step" to the docker ps dash a beat).
SAY: Now the README's Run Docker Container step: docker run, dash dash rm, dash t i, simple-translate. At the prompt, type the README's translation: Good morning, from English to Spanish. Pause and run both.

SHOW: The terminal shrinks to the strip, keeping `Output: Buen día`, which enlarges. Small picture
above the strip: a TEAL container inside a GREY laptop; a PINK arrow leaves the laptop to a BLUE
cloud `translate.googleapis.com` and comes back. A GREY chip appears as the error is named:
"a runtime error? → Google said no · not Docker" (the error text is said, not printed: no capture).
SAY: Good morning comes back in Spanish: the request went from the container, through your laptop's network, to Google. If yours ends in a runtime error, Google refused the request: try later; Docker is fine.

SHOW: TRACKER A16. The terminal grows back; it types `exit` (laptop/31 line 17) → TERM(laptop/31: 18);
the prompt `student@laptop:~/simple-translate$` returns. `▶ your turn`.
SAY: To leave, type exit, and you're back on your laptop. Pause and do it.

SHOW: TRACKER A16 · extra. The terminal shrinks to the strip. V2 container picture above the strip:
the TEAL stack, the dashed glowing glass slab on top, a dot "main process". The `exit` replays: the dot
goes out ("stopped"); a chip `--rm` dissolves the whole container, glass slab and label; the stack
stays (GREEN check "image unchanged"). Strip types `docker ps -a` (extra) → TERM(laptop/32: 2;
squeeze): the header only.
SAY: What did exit do? It ended the container's process, so the container stopped, and dash dash rm deleted it. An extra check, docker ps dash a, lists every container, even stopped ones. Nothing is left; the image is untouched.

SHOW: TRACKER A16 · extra. Strip (4 rows), a second run (extra): it types
`docker run --rm -ti simple-translate` → at the prompt `root@1d1fecf6ff8f:/#` it types `echo $$`
(line 4) → TERM(laptop/33: 5), then TERM(laptop/33: …) (GREY caption on the `…`: "more checks · part
2"), then it types `exit` (line 29) → TERM(laptop/33: 30). A new glass slab and dot appear on the
picture; the `1` flies to the dot's label "PID 1 · bash". Labels: `-i` "your keyboard → bash",
`-t` "a terminal: prompt, line editing". At "Type exit", the dot goes out and the slab dissolves.
GREY tag `Lecture 2 · slides 13–14` (top right, from "In a second run", through the PID namespace
bridge).
SAY: In a second run, an extra check, echo dollar dollar, shows that bash is process number 1. That's the PID namespace from today's lecture: each container counts its own processes from 1. The container lives as long as that process. Dash i connects your keyboard, and dash t gives it a terminal. Then type exit.

SHOW: The picture clears. V3 card: ENTRYPOINT `["/bin/bash"]`, CMD `["-c", "source … && exec bash"]`;
S05's two GREY labels return under the slots, ENTRYPOINT "the program", CMD "its default
arguments". Above it a chip `docker run --rm -ti simple-translate python cli.py` with `python cli.py`
boxed YELLOW. GREY tag `Lecture 2 · slides 40–41` (top right, from "Now a puzzle").
PONDER(8 s, "docker run --rm -ti simple-translate python cli.py\nWhat command line does the container actually run?")
SAY: Now a puzzle. Remember, CMD only holds the default arguments. What if you put words right after the image name: docker run, simple-translate, python cli.py? What command line does the container run?

SHOW: A WHITE tile `python cli.py` flies from the end of the chip and knocks the CMD tile off the
card; the start-up line reads `/bin/bash python cli.py` and flashes RED. Then the card fades (the
start-up line stays). Bash's view: `python` as a "script name"; a door row with two doors
(`/usr/local/bin` ORANGE, `…`), no venv door; the first door holds the ORANGE `python` program,
stamped RED "a program, not a script". Strip types
`docker run --rm -ti simple-translate python cli.py` (extra) → TERM(laptop/36: 2; wrap), RED; a RED
tag "exit 126".
SAY: Words after the image name replace CMD, and only CMD. So the container runs bash, python cli.py. Bash takes python as a script name, and finds the Python program in user local bin. That's a binary, so bash refuses: cannot execute binary file, exit code 126.

SHOW: The door row fades; the card returns. A tile `-c "source .venv/bin/activate && python cli.py -d fr"`
replaces CMD; the start-up line turns GREEN. Strip (5 rows) types
`docker run --rm simple-translate -c "source .venv/bin/activate && python cli.py -d fr"` (extra;
folds; the missing `-ti` gets a GREY label "nothing to type") → TERM(laptop/37: 12; wrap, 14–15);
`Output: j'adore le fromage` GREEN.
SAY: To run it in one go, replace CMD with your own dash c string, as in this extra: activate, then translate to French.

SHOW: CODE(docker-shell.sh: 10–15), lines 11 and 15 highlighted, GREY tag "not in the README · builds
and runs in one go". Under the panel a 1-row strip types `sh docker-shell.sh` (laptop/42 line 1, row
tag `extra`); the command glows when it is said.
SAY: A repo helper, docker-shell.sh, builds and runs in one go: run it with sh docker-shell.sh.

SHOW: Part-1 recap: the full V2 stack (the base brace, the ORANGE "RUN apt…uv" slab, the GREY
"COPY . ./" slab, the GREEN "RUN uv sync" slab) with the config card; a TEAL check "your image:
built and run". Closing card: "Part 2: what's inside, why it rebuilt, and shipping it to a VM". Fade
to an empty frame (end of part 1).
SAY: You've built and run your own image. In part 2: what's inside it, why it keeps rebuilding, and how to ship it to a VM.

---

## S10 · What's inside the image — `s10_inside.py` · `InsideTheImage`

SHOW: TRACKER A16 · extra (for the whole scene). It opens on part 1's closing picture (the full V2
stack and card); GREY caption "part 2 · two extra scenes, then we ship". The stack slides left and
shrinks as a full laptop terminal (12 rows) fades in; it types `docker image ls` (extra) →
TERM(laptop/30: 2, 4; squeeze) (row 3 never printed). `518MB` and `144MB` highlight; tag `at the time
of recording`; a GREY note "Docker Desktop may show other columns". Then the terminal shrinks to the
strip: at "Content is the compressed layers that travel", a small bundle of compressed parcels
appears by the stack under `144MB`; at "disk adds the unpacked copy", the bundle unpacks onto the
stack and one brace over both reads `518MB`.
SAY: Part 2 opens the image we built; this scene and the next are extras. First, docker image ls: 518 megabytes on disk, and 144 megabytes of content, at the time of recording. Content is the compressed layers that travel to a registry; disk adds the unpacked copy.

SHOW: The terminal grows back; it types `docker history simple-translate` (extra) →
TERM(laptop/34: 2–10; cols CREATED BY, SIZE), with the GREY tag "columns: CREATED BY · SIZE" above
the SIZE column. Rows 5 (`125MB`), 6 (`250kB`) and 7 (`97.5MB`)
highlight in their slab colours; rows 3–4 and 8–10 (`0B`) GREY, "config only". The terminal shrinks
to the strip; V2's slabs rescale to these sizes: a fat GREEN `RUN uv sync` slab, a GREY sliver for
`COPY . ./`, an ORANGE apt/pip slab; the card lists the 0B rows. The ORANGE slab's name changes to
`RUN apt…uv` (S11's name). GREY tag `Lecture 2 · slides 34–37, 59` (top right, from "Then docker
history lists the layers, newest first").
SAY: Then docker history lists the layers, newest first. Read it bottom-up, and it's the Dockerfile top-down: the apt and pip step at 97.5 megabytes, our code at 250 kilobytes, and uv sync at 125 megabytes. The ENV, ENTRYPOINT and CMD rows are zero bytes: config only.

SHOW: The terminal grows back and continues → TERM(laptop/34: …, 14–23; cols CREATED BY, SIZE) (it
scrolls). Line 18 `ENV PYTHON_VERSION=3.12.15` highlights ORANGE, line 22 `ENV PATH=/usr/local/bin:…`
PINK, line 23 (`debian.sh … 'bookworm'`, `85.3MB`) ORANGE. Then the terminal shrinks to the strip;
the four base slabs rescale bottom-up to rows 23, 20, 16
and 15 (`85.3MB`, `9.7MB`, `54.5MB`, `16.4kB`), each size written on its slab as it grows, while
S04's list of download sizes turns into the GREY note "≈ 47.6 MB compressed download / → unpacked
on disk" beside the base.
SAY: Below them sit the base image's own rows: Debian bookworm at the bottom, the PATH that puts user local bin first, and Python 3.12.15.

SHOW: The picture clears; the wide terminal (13.2 wide, 20 pt) shows the second run from S09, GREY
caption "our second run from part 1 · yours: docker run --rm -ti simple-translate":
`docker run --rm -ti simple-translate`, the prompt `root@1d1fecf6ff8f:/#`, then the `…` of S09
opens up: it types `which python` (line 6) → TERM(laptop/33: 7) (`/.venv/bin/python` GREEN),
`python --version` (line 8)
→ TERM(laptop/33: 9) (`Python 3.15.0` GREEN), `/usr/local/bin/python --version` (line 10) →
TERM(laptop/33: 11) (`Python 3.12.15` ORANGE), `ls /root/.local/share/uv/python` (line 12) →
TERM(laptop/33: 13) (GREEN), with the GREY platform tag "▲ on an Intel/AMD machine · Apple Silicon:
…linux-aarch64-gnu" under it.
SAY: To look yourself, start a container again; these are from our second run in part 1. There, python is 3.15.0, while the base Python is still 3.12.15. Most of that 125 megabyte layer is this second Python, in uv's own folder.

SHOW: Terminal (13.2 wide, 20 pt) continues the same run: `ls -a /` (line 21) → TERM(laptop/33: 22–28) (columns kept);
`.git`, `.gitignore`, `.vscode`, `Dockerfile`, `README.md` brighten with a PINK bracket "from the
build context", and the other build-context entries (`Dockerfile.txt`, `cli.py`,
`docker-build-push.sh`, `docker-shell.sh`, `pyproject.toml`) turn PINK too; then `exit` →
TERM(laptop/33: 30).
SAY: Now list the top folder. Beside the system folders sit the hidden git folder, the editor's VS Code folder, the README and your Dockerfile. The COPY line copied the whole build context, your git history included. Type exit to get back to your laptop.

SHOW: The terminal fades. S06's parcel returns, its `.git/` glyph lit. Tag `erratum` "no
.dockerignore". A small GREY card, tag `illustration` ("a file you'd add"): `.dockerignore` with
three GREEN lines `.git`, `.venv`, `secrets/`. The dashed sieve from S06 fills in over the parcel
and catches `.git/`. A small BLUE shelf glyph pulses with a GREY tag "public, soon". Fade out.
SAY: That's a gap in the tutorial: there's no dockerignore file. In your own projects, add one listing dot git, dot venv and your secrets folder. It matters most once the image is public, and that's soon.

---

## S11 · The layer cache — `s11_cache.py` · `LayerCache`

SHOW: TRACKER A16 · extra. V5 full, concept first, in time with the SAY: (a) at "caches every build
step", four boxes appear left to right, `[1/4] FROM` · `[2/4] RUN apt…uv` · `[3/4] COPY . ./` ·
`[4/4] RUN uv sync`, each dropping a domino under it. (b) At "its parent step and its instruction",
for each box two thin arrows, one from the previous box and one from its instruction text, merge
into a TEAL fingerprint badge. (c) At "For COPY, the checksum", a small GREY parcel (S06's build
context) docks under COPY's badge and feeds it a third arrow. (d) At "The first step that changes",
a generic example: box 2's instruction text flickers YELLOW (an edit to that RUN line), its badge
turns RED, and dominoes 2, 3, 4 topple in sequence; domino 1 stays. (e) The dominoes stand back up;
the badges return to TEAL. A GREY caption under the four boxes: "one numbered step per
instruction". GREY tag `Lecture 2 · slides 36, 58–60` (top right, from "Docker caches every build
step").
SAY: So why did COPY and uv sync rerun when we only added a line? Docker caches every build step. A step is reused when its parent step and its instruction are unchanged. For COPY, the checksum of the copied files must match too. The first step that changes runs again, and so does every step after it.

SHOW: A bottom terminal of 8 rows (the boxes stay above it) types
`docker build --progress=plain -t simple-translate -f Dockerfile .` (extra flag; tag "extra · full
log"; folds) → TERM(laptop/38: 23; cut after `apt-get update &&`, 24, 26–27, 29–30). Boxes 2–4 get a TEAL
`CACHED` stamp as their lines print; box 1 gets a TEAL "reused" stamp (the plain log just resolves
the base, `#4 DONE 0.0s`; the compact view calls it `CACHED`, laptop/29 line 9).
SAY: Rebuild with nothing changed, adding the extra flag for the full log. FROM reuses the base, and the three steps after it all say CACHED: nothing runs.

SHOW: The parcel under COPY enlarges; its `cli.py` glyph highlights YELLOW, and CODE(cli.py: 49)
docks beside it (header `cli.py · line 49`), `default="I love cheese",` highlighted.
PONDER(8 s, "You change one word in cli.py and rebuild.\nWhich of the four steps run again?")
SAY: Now predict. You change one word in cli.py and rebuild. Which of the four steps run again?

SHOW: In the panel, `"I love cheese"` morphs to `"I love brie"` (YELLOW). The bottom terminal types
`git diff` (extra) → TERM(laptop/39: 10–11) (`-` RED, `+` GREEN). COPY's checksum badge turns RED.
SAY: Try it, as an extra: on line 49, change I love cheese to I love brie. The git diff shows the change; the build context now has a different checksum.

SHOW: The bottom terminal (8 rows) types
`docker build --progress=plain -t simple-translate -f Dockerfile .` (extra) → TERM(laptop/40: 23; cut after
`apt-get update &&`, 24, 26–27, 29–30; wrap, …, 36). Boxes 1–2 keep their TEAL stamps; a RED wave
knocks over dominoes 3 and 4; a PURPLE "35.9 MiB" download arrow fires into box 4.
SAY: Rebuild. FROM and the apt and pip step are reused. But the checksum of the copied files changed, so COPY runs, and uv sync after it, Python download and all.

SHOW: The dominoes stand back up. The bottom terminal types `git checkout -q cli.py` (extra; as run in
`run_steps.sh` line 139) → (no output); the panel line morphs back to `"I love cheese"`. Then
`docker build --progress=plain -t simple-translate -f Dockerfile .` (extra) → TERM(laptop/41: 26–27, 29–30; wrap).
In V5, a small glyph `.git/index` inside the parcel flips YELLOW; COPY's badge stays RED and the wave
runs again.
SAY: Now undo the edit with git checkout. Same files, so the cache comes back? No: COPY and uv sync run again. Git rewrote its own index file, inside the hidden git folder, and that folder is in the build context too.

SHOW: A `Dockerfile` glyph inside the parcel flips YELLOW; caption "Dockerfile steps 4 and 5: every
edit to the Dockerfile changed the parcel". Tag `erratum` "expected while learning".
SAY: That answers the question from part 1. Your Dockerfile sits in the build context too, so every edit to it changed that checksum. While you follow the README step by step, that's expected.

SHOW: The fix animates, tag "a pattern for your own projects · not the course solution": the
`COPY . ./` box splits in two: a small `COPY pyproject.toml README.md ./` moves left of
`RUN uv sync`, the rest stays after it; a fifth domino stands up. S10's `.dockerignore` card returns
(`.git`, `.venv`, `secrets/`) and a fourth line `Dockerfile` slides in YELLOW; the sieve over the
parcel catches `.git/`, `.venv/` and `Dockerfile`. `cli.py` is edited again: the RED wave reaches
only the last box; `RUN uv sync` keeps `CACHED`. GREY footnote "full Dockerfile: exercises.md". Fade
out.
SAY: In your own projects, put the slow steps first: copy only the files uv sync needs, run it, then copy the rest. A dockerignore keeps the git folder, any local venv and the Dockerfile out. Now an edit to cli.py reruns only the last COPY.

---

## S12 · Tag and push — `s12_push.py` · `TagAndPush`

SHOW: TRACKER B1 (the tracker switches to "README › Pushing Docker Image to Docker Hub", 4 dots). A
schematic browser card (tag `illustration`): "Docker Hub · account settings", a row "Personal access
tokens", a button "Generate new token", a row "Access permissions: Repo Read & Write" (YELLOW, with a
GREY note "default: Repo Public Read-only · can't push"); a token field
shows `<ACCESS TOKEN>` with a lock glyph, `▶ your turn` beside it and a GREY note "copy it now:
shown only once". A README card (`README.md · line 188`). GREY note "a token is a password: never in
a file, never in a repo".
SAY: Now the README section Pushing Docker Image to Docker Hub. First, sign up and create an access token, with read and write access, not the default. Copy it right away: it's shown only once, and it works like a password. Pause and make yours.

SHOW: TRACKER B2. CODE(README.md: 189), `<USER NAME>` and `<ACCESS TOKEN>` boxed YELLOW, "yours". A
GREY note: "no Docker Hub account in our recording · not run here". GREY tag
`Lecture 2 · slides 67–69` (top right, from "Next, log in", through the push).
SAY: Next, log in: docker login, dash u with your user name, dash p with your token. We have no account, so we couldn't run it.

SHOW: TRACKER B2 · extra. A terminal (8 rows) with `stand_in_tag()` on its frame ("stand-in · local
registry, not Docker Hub" / "watch only · don't type") types
`docker login localhost:5000 -u student -p not-a-real-token` (folds) → TERM(laptop-push/05: 2, 8).
Line 2 (`WARNING! Using --password via the CLI is insecure. Use --password-stdin.`) highlights
YELLOW; `Login Succeeded` GREEN.
SAY: So some steps use a stand-in, a small registry on our own machine: just watch those. Logging in to it warns that a password on the command line is insecure.

SHOW: Tag `illustration`: a GREY list "~/.bash_history" where the line
`docker login -u <USER NAME> -p <ACCESS TOKEN>` lands, the token part RED; tag `erratum`. Then a
GREEN chip `docker login -u <USER NAME>` followed by a GREY prompt line "Password:" and a paste
glyph; `▶ your turn` beside the chip, with a GREY note "or the README's form".
SAY: That's a small slip in the README: with dash p, your token stays in your shell history. Instead, type docker login, dash u, and your user name, then paste the token when it asks. Pause and log in.

SHOW: TRACKER B3. CODE(README.md: 190) at the top, with the YELLOW caption "`<USER NAME>` = your
Docker Hub username (here: student)". The laptop terminal (prompt
`student@laptop:~/simple-translate$`) types `docker tag simple-translate student/simple-translate-ac215`
→ TERM(laptop/43) → (no output). `▶ your turn`. Then TRACKER B3 · extra: `docker image ls` (extra) →
TERM(laptop/44: 2, 4–5; squeeze) (row 3 never printed); both `b5c531a6b555` highlight TEAL.
SAY: Then tag the image: docker tag, simple-translate, then your user name, slash simple-translate-ac215. Pause and run it with your own name. An extra image ls shows two names, one ID: a second name, not a copy.

SHOW: V6: a TEAL stack with the ID `b5c531a6b555`; two TEAL sticky notes point at it,
`simple-translate:latest` and `student/simple-translate-ac215:latest`. The long note unfolds into
four parts: `docker.io` "registry · the default", `student` "account", `simple-translate-ac215`
"repository", `latest` "tag". Under it, a GREY chip from the build logs,
`docker.io/library/simple-translate:latest`, "no account → library".
SAY: Read the long name in four parts: the registry, docker dot I-O, the default; your account; the repository; and the tag, latest. Names without an account, like our first, fall under library.

SHOW: TRACKER B4. CODE(README.md: 191). Picture first: V6, the TEAL stack's slabs lift off one by
one along a PINK route to a BLUE shelf "Docker Hub · student/simple-translate-ac215", each checked at
the door ("missing? → upload"). Then the laptop terminal clears and types
`docker push student/simple-translate-ac215` → TERM(laptop-push/03: 2–8; wrap), line 8 RED; tag
`real capture · 2026-10-13` and a GREY label "what we got · no Docker Hub account"; the shelf's door
shuts RED. A GREEN note under it: "logged in: Pushed … latest: digest: … (next)". GREY note "if you
see this: log in · a token that can write · the name must start with YOUR username". `▶ your turn`.
SAY: Then push: docker push, with the same name. Pause and run it. Yours should upload each layer and end with a digest line. Without an account, Docker Hub refused ours: push access denied. If you see it, log in, and check your token can write and the name starts with your user name.

SHOW: TRACKER B4 · extra. The stand-in terminal (`stand_in_tag()`, "watch only") types
`docker tag simple-translate localhost:5000/student/simple-translate-ac215` (folds) → (no output),
then `docker push localhost:5000/student/simple-translate-ac215` (folds) →
TERM(laptop-push/07: 3–4, …, 15; hash12). V6: slabs travel a PINK route to a dashed BLUE shelf
"stand-in registry".
SAY: On the stand-in, the push goes through, ending with a digest: a fingerprint of the whole image.

SHOW: The same push again → TERM(laptop-push/08: 4, …, 14–15; hash12). Each slab bounces back off
the shelf, "already exists". Then the four ORANGE base slabs get a GREY link line to a `python` stack
already standing on a BLUE "Docker Hub" shelf (tag `illustration`), caption "already on Docker
Hub · from the official python image" (the message itself is said, never printed: no capture).
SAY: Push again: every layer already exists, and only missing layers travel. On Docker Hub, even the base layers may say mounted from library python: it already has them.

SHOW: A schematic Docker Hub repository card (tag `illustration`) with a BLUE "public" badge; the
`.git/` glyph in its stack pulses RED; S10's `.dockerignore` card flashes beside it. Fade out.
SAY: And remember: a new Docker Hub repository is public by default. Anyone can pull it, git folder and all.

---

## S13 · Platforms: arm64 vs amd64 — `s13_platforms.py` · `Platforms`

SHOW: TRACKER B4 · extra (for the whole scene). Laptop terminal types
`uname -m; docker image inspect simple-translate --format '{{.Os}}/{{.Architecture}}'` (extra; folds)
→ TERM(laptop/35: 2–3). Both lines highlight BLUE; a GREY note "Apple Silicon Mac: arm64".
SAY: One more check before the VM; this scene is all extras. Our machine is Intel or AMD, and the image says linux slash amd64. On an Apple Silicon Mac, you'd see arm64.

SHOW: V7 (terminal hidden): two chips, `arm64 · Apple Silicon` (GREY, a laptop glyph) and
`amd64 · Intel/AMD · default GCP VM` (BLUE, a VM glyph), each with its own row of small glyphs,
"machine instructions". At "machine code", a TEAL image box writes `bash`, `python`, `uv` (Write) in
amd64 glyphs; the BLUE chip's glyph row, then the GREY chip's row, glow as each is named. At "run
directly", the image box slides down onto the BLUE chip and the glyph rows click together (GREEN
check); GREY note "runs directly on the CPU · unless an emulator steps in". At "Docker Desktop has
one built in", a small GREY "emulator" box appears inside the GREY laptop glyph; the BLUE VM glyph
gets a dashed empty slot "no emulator".
SAY: Why does that matter? Every program in an image, bash, Python, uv, is machine code for one kind of CPU: amd64 for Intel and AMD, arm64 for Apple Silicon. A container's programs run directly on the CPU, so unless an emulator steps in, the CPU must speak the image's language. Docker Desktop has one built in; a plain Linux VM doesn't.

SHOW: Terminal (13 rows) types `docker buildx imagetools inspect python:3.12-slim-bookworm` (extra;
folds) → TERM(laptop-push/11: 2–3, 9, …, 30, …, 51, …, 72, …, 93). Then the terminal shrinks to the
strip, and the five `Platform:` lines fly out of it (TransformFromCopy) and become the rows of a menu
card under the tag's name: `linux/amd64`, `linux/arm/v7`, `linux/arm64/v8`, `linux/386`,
`linux/ppc64le`; GREY dimmed rows "attestation" between them; a BLUE arrow from a VM glyph points at
the amd64 row.
SAY: A tag can point at a menu, one image per platform. This python tag lists five platforms: amd64, two kinds of arm, and two rarer ones. Docker pulls the row that matches your machine.

SHOW: The terminal grows back; it types `docker buildx imagetools inspect dlops/simple-translate` (extra) →
TERM(laptop-push/10: 2–4; hash12). Line 3's `manifest.v2+json` highlights: "one image, not a menu";
a GREY chip from vm-debian12/08 line 3: `linux/amd64`.
SAY: The instructor's image, dlops slash simple-translate, is no menu: one image, amd64 only.

SHOW: Stand-in terminal (`stand_in_tag()`, "watch only") types
`docker buildx imagetools inspect localhost:5000/student/simple-translate-ac215` (extra; folds) →
TERM(laptop-push/09: 3, 9, 13). The terminal shrinks to the strip; V7: a small menu "our push": a
BLUE `linux/amd64` row and a dimmed `unknown/unknown` row, "attestation · how it was built"; at
"Built on an M-series Mac", a GREY dashed overlay on the first row: "built on a Mac: linux/arm64";
a GREY note on the menu "containerd image store · the older store pushes one image, no menu".
SAY: Our stand-in push is a small menu: amd64, plus an attestation, a record of how the image was built. Built on an M-series Mac, the amd64 row would say arm64.

SHOW: V7: the GREY arm64 chip builds an image in arm64 glyphs; a PINK route carries it past a BLUE
shelf to a BLUE VM with an amd64 chip and its empty "no emulator" slot.
PONDER(8 s, "You built on an M-series Mac and pushed.\nYour VM is an ordinary Intel/AMD machine.\nWill your image run there?")
SAY: Now ponder. You built on an M-series Mac and pushed. Your VM is an ordinary Intel or AMD machine. Will your image run there?

SHOW: The VM orders "amd64" from the arm64-only menu: nothing it can run, RED. Tag
`extra · arm64 image on an amd64 machine` and a GREY tag "no emulator here · Docker Desktop would
run it". Terminal types `docker run --rm --platform linux/arm64 debian:12 uname -m` (extra; folds) →
TERM(laptop-push/12: 2, …, 10); line 10 `exec /usr/bin/uname: exec format error` RED.
SAY: No. Here's the same failure the other way around, on our machine, which has no emulator: exec format error. Docker Desktop would just run it, emulated. A Mac-built image on a default VM fails like this, or with no matching manifest.

SHOW: CODE(docker-shell.sh: 11–12), line 12 (`#docker build -t $IMAGE_NAME --platform=linux/amd64 -f Dockerfile .`)
highlighted YELLOW with the GREY tag "commented out · not in the README". V7: the arm64 chip's build
passes through the GREY "emulation" box and the image's glyphs turn amd64. Under the panel a GREEN
text chip (not run), three lines:
`docker build -t simple-translate --platform=linux/amd64 -f Dockerfile .` ·
`docker tag simple-translate <USER NAME>/simple-translate-ac215` ·
`docker push <USER NAME>/simple-translate-ac215`.
SAY: Two fixes, neither in the README. One: build for the VM's platform, with the flag dash dash platform equals linux slash amd64. It's the commented-out line 12 of docker-shell.sh. On a Mac, it runs emulated: slower, but it works. Then tag and push again, as before.

SHOW: The panel and chip clear. Picture first: V7, buildx cooks two images, one amd64 and one arm64
(the second through the "emulation" box), and pushes one menu with both rows. Then
CODE(docker-build-push.sh: 21–27), lines 23 (`docker buildx create … --name multi-arch`) and 27
(`--platform linux/amd64,linux/arm64 --push`) highlighted; tag `erratum` "would push both · the
published image has only amd64".
SAY: Two: docker-build-push.sh uses buildx, Docker's multi-platform builder, to build both and push one menu.

SHOW: The panel changes to CODE(docker-build-push.sh: 7–11), lines 7 (`IMAGE_NAME="simple-translate"`)
and 11 (`DOCKER_USERNAME="dlops"`) highlighted, YELLOW caption "your username (11) ·
simple-translate-ac215 (7)". One chip row under it: `docker login` "first" · `bash docker-build-push.sh`
"not executable" · `docker buildx use default` "afterwards: builds land on your laptop again · desktop-linux on
Docker Desktop". Fade out.
SAY: Put your user name on line 11, and simple-translate-ac215 on line 7, the README's name. Log in first, then run it with bash. Afterwards, switch back with docker buildx use default, or desktop linux on Docker Desktop.

---

## S14 · A VM with only Docker — `s14_vm_docker.py` · `DockerOnVM`

SHOW: TRACKER C1 (the tracker switches to "README › Running App on VM using Docker", 7 dots). A
schematic console (browser, tag `illustration`, as in L1): VM instances → Create instance; form rows
fill: Name `ac215-l02` · Machine type `e2-small` · Boot disk `Debian GNU/Linux 12 (bookworm)`; GREY
footnote "the README gives no settings: sensible choices · Debian 13 works too · E2 = amd64". The
GOLD dial starts sweeping, with tags "billed per second while running" and "disk: billed while it
exists". GREY tag `Lecture 2 · slides 77` (top right, from "The last README section").
SAY: The last README section: Running App on VM using Docker. First, create a VM, as in lecture 1. The README gives no settings. An ordinary E2 machine with Debian 12 or 13 will do; E2 machines are amd64. The meter starts: the VM bills by the second while it runs, its disk while it exists.

SHOW: TRACKER C2. "SSH" is clicked: the browser window transforms into a terminal (title
`ssh · ac215-l02`, prompt `student@ac215-l02:~$`). `▶ your turn` (create + SSH).
SAY: Next, SSH in. Pause now: create your VM, and wait until its SSH terminal is open.

SHOW: TRACKER C3. It types `sudo apt install docker.io` (README.md line 210) →
TERM(vm-debian12/01: 4–8; +Done); lines 7–8 RED; GREY tag `stand-in · empty package lists`.
`▶ your turn`. A small GREY card "Debian 13" shows TERM(vm-debian13/01: 7) (`Error: Unable to locate
package docker.io`). A GREY note on two lines: "it asks [Y/n]? answer Y" / "→ skip to step 4:
Docker version".
SAY: Then install Docker: sudo apt install docker dot I-O. Pause and run it. In our stand-in, a fresh Debian with empty package lists, it fails: unable to locate package. If yours installed, skip ahead to the version check.

SHOW: Two README cards side by side: `README.md · line 210` (`sudo apt install docker.io`) and
`README.md · line 44` (`sudo apt-get update`, from the L1 walkthrough); tag `erratum`. An ORANGE
catalog book "package lists" stands empty, with a GREY label "empty, or out of
date". TRACKER C3 · extra. It types `sudo apt-get update` (extra) → TERM(vm-debian12/02: 8–9;
+Done); the book fills. `▶ your turn`.
SAY: A small gap in the README: this section skips sudo apt-get update, used in lecture 1. Without it, the package lists may be empty, as here, or out of date, with Not Found errors. Run the update first, an extra, and pause after it.

SHOW: TRACKER C3. It types `sudo apt install docker.io` again →
TERM(vm-debian12/03: 4–6; +Done, 55–56, 57; wrap, 58; [Y/n] Y, …, 560, 581) (see Notes: these two
lines come after the `\r` lines). Lines 55–56 highlight, `107 MB` with a GREY label "download";
GREY tag "package list varies by VM"; the `Y` flashes YELLOW. The small GREY "Debian 13" card shows
TERM(vm-debian13/03: 77–78). `▶ your turn`.
SAY: Now the install works: 92 new packages, a 107 megabyte download, on Debian 12; 91 packages and 118 megabytes on Debian 13. Answer Y. Pause and run it.

SHOW: TRACKER C4. It types `sudo docker --version` → TERM(vm-debian12/04: 2); the GREY "Debian 13"
card shows TERM(vm-debian13/04: 2). Both get the tag `at the time of recording`; a PURPLE chip
`docker.io · Debian's package`. At "Older than the laptop's", a GREY note "our laptop: Docker 29.8.2"
(laptop/00 line 4) under the chip, with its own GREY tag `at the time of recording` under it.
SAY: Then sudo docker dash dash version. This is Debian's own Docker package: 20.10.24 on Debian 12, 26.1.5 on Debian 13, at the time of recording. Older than the laptop's, but plenty.

SHOW: The terminal shrinks to the strip. V8, S14 half, above it: a BLUE VM box; inside it, the VM's
own bar is split into "Linux kernel" with "user space · Debian" above it, and a PURPLE `dockerd`
block sits on user space; an empty TEAL container
slot above it; no dashed Linux VM (S02's dashed box flashes small beside it, crossed: "Docker
Desktop only"). GREY tag `Lecture 2 · slides 12, 24` (top right, from "Here Docker runs right on the
VM's Linux kernel").
SAY: Here Docker runs right on the VM's Linux kernel; there's no hidden VM, unlike Docker Desktop on a Mac.

SHOW: V8 fades. TRACKER C4 · extra. Strip types `docker ps` (extra) → TERM(vm-debian12/05: 2; wrap),
RED. Above it, a door glyph `/var/run/docker.sock` with a lock, a PURPLE `dockerd` box behind it, and
GREY labels "root · docker group" on two keys. Fade out.
SAY: And why sudo? Without it, this extra docker ps is refused: permission denied on the Docker socket, the door to Docker's background service. Only root and the docker group may open it.

---

## S15 · One-command deploy — `s15_deploy.py` · `Deploy`

SHOW: TRACKER C5. VM terminal (12 rows) types `sudo docker run --rm -ti dlops/simple-translate`
(README.md line 215) → TERM(vm-debian12/06: 2–4, …, 10–12; hash12). `▶ your turn`. The terminal
shrinks to the strip; V6 above: seven slabs come down a PINK route from the BLUE Docker Hub shelf
into the BLUE VM and stack up; a TEAL glass slab appears on top. GREY tag `Lecture 2 · slides 70–71`
(top right, from "Then the deploy").
SAY: Then the deploy: sudo docker run, dash dash rm, dash t i, dlops slash simple-translate. Pause and run it. The image isn't on this VM yet, so Docker pulls it from Docker Hub, seven layers, then starts a container.

SHOW: TRACKER C6. Full terminal; the prompt `root@c7c280390994:/#` (line 13); it types `python cli.py`
(README.md line 218) → TERM(vm-debian12/06: 16–20, 24; wrap, 26–27). `Output: Adoro il formaggio`
GREEN. `▶ your turn`.
SAY: Now run the app with python cli.py and its defaults: I love cheese comes back in Italian. Pause and run it. No clone, no pip, no uv on this VM: just Docker and one image.

SHOW: TRACKER C6 · extra. It types `python --version` (extra) → TERM(vm-debian12/06: 29). The terminal
shrinks to the strip. V4 coda: the number line returns; our GREEN dot sits above the line, label
`3.15.0` / "our build · uv 0.13.0"; a second GREEN dot lands in the same glow below the line, label
`3.14.7` / "dlops image · uv 0.12.15". Two GREY source chips carry the dates:
TERM(vm-debian12/08: 3) ("created 2026-09-16…"; its caption is the inspect command itself, GREY mono
on two rows, `sudo docker image inspect dlops/simple-translate \` /
`--format '{{.Os}}/{{.Architecture}} created {{.Created}}'`, with the row tag "extra · on the VM")
and TERM(vm-debian12/10: 8) (`uv = 0.12.15`, the image's `pyvenv.cfg`).
SAY: And the opening question: why 3.14.7, when the recipe says 3.12? The same reason as in our build. This image was built on September 16 with uv 0.12.15, and the newest stable Python that uv knew in the range was 3.14.7. Our build today got 3.15.0.

SHOW: Three GREY chips light in turn: `pip install uv` "unpinned" (Dockerfile.txt line 19),
`requires-python = ">=3.13"` "open-ended" (pyproject.toml line 6), `uv.lock` dashed "not in the
repo · each build writes its own". Then the TEAL image stack gets a frost glyph, "frozen at build
time"; caption "ship the image, not the recipe".
SAY: Same Dockerfile, a month apart, two Pythons. Nothing in the recipe is pinned: pip installs the latest uv, the Python range is open, and the repo has no uv.lock, so each build writes its own. An image freezes all that: ship the image, not the recipe.

SHOW: Full terminal; it types `exit` (line 30) → TERM(vm-debian12/06: 31). Two README cards:
`README.md · line 205` "pull the image you pushed in step 3" and `README.md · line 215`
`sudo docker run --rm -ti dlops/simple-translate`; tag `erratum`. Below them a GREEN chip (text, not
run) `sudo docker run --rm -ti <USER NAME>/simple-translate-ac215`, `<USER NAME>` YELLOW, with a GREY
tag "Intel/AMD laptop: already amd64 · Apple Silicon Mac: rebuild first (see Platforms)".
SAY: Type exit. One more small mismatch: the README promises to pull the image you pushed, but this command runs the instructor's. Your image is your user name, slash simple-translate-ac215. Run it with the same command, once it's built for amd64.

SHOW: TRACKER C6 · extra. Strip (5 rows) types
`sudo docker run --rm dlops/simple-translate -c 'wc -c cli.py; grep -n Translator cli.py; ls -l .venv/bin/python; cat .venv/pyvenv.cfg'`
(extra; folds) → TERM(vm-debian12/10: 2–4, …, 8), with a YELLOW underline on `uv = 0.12.15` and the
GREY tag "where uv 0.12.15 came from". Line 4 `25:    async with Translator() as translator:`
sits above CODE(cli.py: 25) (the repo's `Translator(raise_exception=True)`); tag `erratum` "the
published image lags the repo".
SAY: Also, an extra check shows the published image lags the repo: its cli.py is the older one, without raise exception equals True. If Google refuses a request, that version quietly prints your input back. That's not a Docker problem.

SHOW: A GREY card "if the pull itself fails:" with TERM(vm-debian13/06-docker-run-rate-limited: 3;
wrap) in RED, tag `real capture · Debian 13 · 2026-10-13`; two GREEN chips "wait a while" and
`sudo docker login -u <USER NAME>`. Fade out.
SAY: And if pulling the image fails with too many requests: Docker Hub limits how often anonymous users can pull, per network address, which a classroom can hit. Wait a while, or log in first, with sudo docker login.

---

## S16 · Tear down, recap, and what's next — `s16_recap.py` · `Recap`

SHOW: TRACKER C6 · extra. Strip terminal types `sudo docker ps -a` (extra) →
TERM(vm-debian12/11: 2; squeeze): the header only.
SAY: Before you go, clean up. An extra check, sudo docker ps dash a, shows no containers left behind, thanks to dash dash rm.

SHOW: TRACKER C7. The schematic console (tag `illustration`): `ac215-l02` ticked → Delete → the
confirm dialog "Delete ac215-l02? Its boot disk is deleted with it" (as in L1). The BLUE VM dissolves;
the GOLD dial stops where it is. A checklist "VM instances: empty" · "Disks: empty" ticks GREEN.
`▶ your turn`.
SAY: Last README step: delete the VM, with its boot disk, then check that VM instances and Disks are both empty. Pause and do it now.

SHOW: GREY optional chips: "Docker Hub repository: public until you delete it or make it private",
`docker system prune -a` "frees the laptop's disk · said, not typed here", and, smaller,
`docker buildx rm multi-arch` "if you ran the push script" · `docker logout` "optional". GREY tag
`Lecture 2 · slides 73` (top right, from "And to reclaim the space").
SAY: Two optional chores. Your Docker Hub repository stays public until you delete it or make it private. And to reclaim the space your images take on the laptop, run docker system prune dash a.

SHOW: V1 closing picture: a BLUE VM box containing a GREEN venv box; between them a dashed GREY box
"container · L2" fades in, solidifies TEAL, and the venv slides into it with the label `/.venv`.
Then this nested VM shrinks and slides right to become the route's "run" end, and the route draws
in to its left: GREY laptop "build" → PINK → BLUE Docker Hub shelf "push" → PINK → the VM "run".
SAY: Lecture 1 gave us a VM with a venv inside. Today a container slid in between: the venv now lives in an image, at slash dot venv. You built it on your laptop, pushed it to a registry, and ran it on a VM with one command.

SHOW: A card "Test yourself". One question at a time (≥ 24 pt, ≤ 2 lines), each with a text-free
icon made from its set piece's shapes: Q1 "What is the difference between an image and a container,
and what does --rm delete?" (a glass slab dissolving on a stack); Q2 "What command line does our
container run at start-up, and what happens with docker run --rm -ti simple-translate python
cli.py?" (a WHITE tile knocking another off a card). When the next question arrives, the previous
one transforms into a one-line label in a list at left: "image vs container" · "start-up command
line".
SAY: Five questions to test yourself. One: what's the difference between an image and a container, and what does dash dash rm delete? Two: what does our container run at startup, and what happens if you add python cli.py after the image name?

SHOW: Q3 "The Dockerfile says python:3.12. Why does python --version print 3.15 (or 3.14), and what
does /usr/local/bin/python print?" (an ORANGE and a GREEN dot on a line); Q4 "You edit one line of
cli.py. Which build steps re-run, and how would you reorder the Dockerfile so uv sync stays
cached?" (four dominoes, the last two falling); Q5 "Name two ways to make an image built on Apple
Silicon run on a default GCP VM." (two chips with different glyph rows). Each joins the label list
in turn: "two Pythons" · "cache order" · "platforms".
SAY: Three: the Dockerfile says Python 3.12, so why does python report 3.15, or 3.14? Four: you edit one line of cli.py; which steps rerun, and how would you reorder the Dockerfile? Five: name two ways to make a Mac-built image run on a default VM.

SHOW: The label list stays at left. Two footer cards: "Answers: exercises.md" and "Study guide +
every command: github.com/JunyiZhou-Conny/MLOps_Learning · guides/L02-containers-1.md". A "Next: L3 ·
Containers II" card with a GREY dashed teaser: five small TEAL boxes linked in a row, a chip
`WORKDIR /app`, a chip "non-root user", and a GREY laptop folder with a dashed arrow into a container,
"mounted". GREY tag `Lecture 2 · slides 42–51, 78–79` (top right, on the Next card). Everything
fades to an empty frame (end of part 2).
SAY: The answers are in the exercises, and every command is in the study guide. Next time, Containers 2: five containers working together, a working directory, a non-root user, and your laptop's folder mounted inside a container.
