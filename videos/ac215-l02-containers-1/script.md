# AC215 · Lecture 2 — Containers I: one image, from laptop to VM — narration script & visual plan (v1)

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

Conventions
- `SAY:` lines are spoken verbatim by the TTS voice (one `voiceover` block each) and become the
  subtitles. Plain spoken English: no backticks, no symbols; commands and paths are said in words
  ("docker run, dash dash rm, dash t i", "slash dot venv", "user local bin" for `/usr/local/bin`,
  "docker dot I-O" for `docker.io`, so the voice doesn't read "io" as a word).
  File names cli.py, pyproject.toml, uv.lock, Dockerfile.txt, docker-shell.sh and
  docker-build-push.sh are written as names (lexicon entries say them). Numbers as digits; never a
  "!" after a digit. Versions and sizes that will change are said with "at the time of recording".
  Foreign-language outputs are on screen, not spoken ("comes back in Spanish").
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
- Terminal size. The house `term()`: 12.6 wide, 22 pt, 65 characters a row, always full width. A
  typed command is never cut: it folds at a space onto an indented row. When a picture needs the
  frame, the terminal shrinks to a 3-row strip along the bottom edge (the last command and its key
  line; "strip (5 rows)" where stated) and the picture uses the frame above it. One exception: the
  three `ls` listings in columns (`laptop/19: 3–7`, `laptop/22: 3–9`, `laptop/33: 22–28`) are up to 73
  characters wide; for those beats the terminal is 13.2 wide at 20 pt (75 characters), so the
  captured columns stay exactly as they are. Row counts below include folded rows; the line a SHOW
  highlights or a SAY reads must be on screen at that moment.
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
  line, and the SAY says so at least the first time that command appears.
- `▶ your turn`: a YELLOW tag beside the command at a real checkpoint (about one per README step);
  the SAY of that block says "pause". The video doesn't wait: the viewer pauses.
- Tags (GREY unless said): `illustration` on every schematic console, Docker Hub page or editor
  drawing (no logos, no screenshots) and on every "what if" picture; `stand-in · local registry,
  not Docker Hub` (`stand_in_tag()`) on every `laptop-push/04–09` and `13` terminal;
  `real capture · 2026-10-13` on the push denial and the rate-limit run; `at the time of
  recording` next to uv 0.13.0, CPython 3.15.0, Python 3.12.15, the Docker versions and image
  sizes when first shown; `erratum` on every README slip (the narration says "a small slip" or
  "a small gap", never "erratum"). `expected` and `recorded` are not needed in this video: every
  terminal line is a real capture, and the steps without one (console clicks, the Docker Hub
  token, `docker login` to Docker Hub) are README cards or `illustration` drawings with no output.
- The cost meter is L1's GOLD dial whose needle sweeps, with no digits. It never rewinds: Delete
  makes it stop where it is.
- Spelling on screen: American.
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
- Length and parts: narration ≈ 4,260 words (`python -m explainer.script`; part 1 ≈ 2,290,
  part 2 ≈ 1,970). L1's 4,287 words gave 29:52 with typing, outputs and ponder timers (the voice
  measured ≈ 151 wpm in L1, not 174), so ≈ 29–31 min. Part 1 = S01–S09 (write the Dockerfile, build and run it; ends on A16), part 2 =
  S10–S16 (layers, cache, Docker Hub, platforms, the VM, teardown). Each part ends on an empty frame.

Notes for scene authors
- TERM/PANEL line numbers are *file* lines (line 1 = the `$` command); `Capture.pick()` indexes the
  output body, so pick index = file line − 1.
- Crops that keep panels honest (ASSETS.md, "Differences"): FROM lines from `laptop/18` on carry the
  capture-only digest `4fb3e77d…`: always `cut` them right after `python:3.12-slim-bookworm` (only
  `laptop/09` and `14`'s `34386ef0…` may be shown, cut after `@sha256:34386ef0`). Never print
  `laptop/34` rows 11–13, the `python:3.12-slim-bookworm` row (row 3) of `laptop/30`, `44` and
  `laptop-push/02`, apt's `Get:` lines, or the VM's `invoke-rc.d: …` lines (no systemd in the
  stand-in). The step-by-step builds (`laptop/09`–`24`, `38`, `40`, `41`) are BuildKit's plain log;
  only `laptop/29` is the compact view.
- `laptop/19` and `22` print `ls` in columns: keep the columns (20 pt exception above), highlight by
  substring.
- Shared code (`scenes/common.py`, from L1's): `tracker_a/b/c`, prompts `P_LAPTOP_HOME`, `P_LAPTOP`,
  `P_VM`, tags incl. `stand_in_tag()`; set pieces `LayerStack` + `ConfigCard` (V2/V3), L1's
  `VersionLine` and `PathDoors` small (V4), `CacheChain` (V5), `NameTags` + `RegistryShelf` (V6),
  `PlatformMenu` (V7), `KernelPicture` (V8), L1's cost dial.
- Layout of V2 when it shares the frame with a strip terminal: the stack stands left of center
  (≈ 3.2 wide), the config card at its right (≈ 3.6 wide), both above y = −2.0; the tracker owns the
  top-left corner, so the stack starts below it.

---

## S01 · One command on a fresh VM — `s01_hook.py` · `Hook`

SHOW: Black frame. No tracker yet. A terminal fades in (12.6 wide, 12 rows, title `ssh · ac215-l02`,
prompt `student@ac215-l02:~$`). A small GREY chip above it: "a fresh VM · only Docker installed".
SAY: Here's a fresh virtual machine in the cloud: no copy of our code, no virtual environment, no uv. It has only Docker, and we type one command.

SHOW: It types `sudo docker run --rm -ti dlops/simple-translate` (README.md line 215) →
TERM(vm-debian12/06: 2–4, …, 10–12; hash12). A small BLUE shelf glyph "Docker Hub" sits at top
right; a PINK arrow pulses from it into the terminal as the `Pull complete` lines print, with a
counter "7 layers" (lines 4–10 are seven `Pull complete` lines). The prompt changes to
`root@c7c280390994:/#` (line 13) and it types `python cli.py` → TERM(vm-debian12/06: 16–20, 24;
wrap, 26–27). The terminal scrolls; `Output: Adoro il formaggio` (line 27) highlights GREEN and stays
on screen.
SAY: Docker downloads an image, in seven layers, and starts a shell inside it. There we run the app, and I love cheese comes back in Italian. No clone, no setup: one command.

SHOW: It types `python --version` (extra) at the same prompt → TERM(vm-debian12/06: 29);
`Python 3.14.7` highlights YELLOW. The terminal shrinks to the bottom strip; CODE(Dockerfile.txt: 2)
slides in above it, `python:3.12` highlighted ORANGE, and a YELLOW "?" sits between `3.12` and
`3.14.7`.
SAY: One extra check, not in the README: which Python is this? It's 3.14.7. Yet the recipe for this image starts from Python 3.12. Hold that thought; we'll solve it twice today.

SHOW: V1, the ladder, header `README.md · lines 9–16`: four rungs with the README's labels, "1 Manual
install on the VM" (ORANGE), "2 Same VM, but with uv" (GREEN), "3 Docker, on your laptop" (a small
TEAL box inside a GREY laptop), "4 Run the Docker image on a VM" (a TEAL box inside a BLUE VM).
Rungs 1–2 are lit softly with a GREY "L1" tag; rungs 3–4 light up with a YELLOW "today" bracket.
SAY: That's where today's tutorial, simple-translate, ends. Last lecture we climbed its first two rungs: a manual install on a VM, then uv. Today, the other two: package the app as a Docker image on your laptop, push it to Docker Hub, and run it on a VM that has only Docker.

SHOW: A layout preview, built piece by piece as named: three tracker chips stack at top-left, each
with an icon, "A · Developing App using Containers · 16" (GREY laptop), "B · Pushing Docker Image to
Docker Hub · 4" (BLUE shelf), "C · Running App on VM using Docker · 7" (BLUE VM), with a YELLOW
circle pulsing around them; a 2-row strip terminal at the bottom (GREY tag "preview") shows
`docker image ls` with a YELLOW `▶ your turn` tag, then `ls -a` with the GREY `extra` tag; a footer
caption: "every command: MLOps_Learning · guides/L02-containers-1.md".
SAY: To follow along, open the README beside this video. Three trackers, top left, show where we are: one for the laptop, one for Docker Hub, one for the VM. When the yellow your-turn tag appears, pause and run the command; a grey extra tag marks a check that isn't in the README. Every command is also in the study guide.

SHOW: The preview clears. A checklist card: "✓ Docker Desktop running (Tutorial 0)", "✓ a free
Docker Hub account", "✓ your GCP project, for the VM at the end", and GREY "✗ no service account,
no keys (README.md · line 23)". A GOLD tag "a VM costs money while it exists" beside the third item.
Fade out.
SAY: You need Docker Desktop running, from Tutorial 0, a free Docker Hub account, and your Google Cloud project for the VM at the end. No service account or keys today.

---

## S02 · Image, layer, container, registry — `s02_nouns.py` · `FourNouns`

SHOW: No tracker (concept scene). L1's closing picture, small at left: a BLUE VM box holding a GREEN
venv box. Beside it, four GREY chips stack up as named: "apt", "git clone", "uv sync", "the right
OS". A TEAL box sweeps in from the right and swallows the four chips plus an ORANGE chip "OS files"
and a GREY chip "your code"; caption under it: "an image".
SAY: First, four words for the whole lecture. In lecture 1, every new VM needed the same setup, and it worked only if the operating system cooperated. A Docker image packs it all into one thing you can copy: operating system files, Python, the packages and the code.

SHOW: V2 on a generic stack, center-left: three translucent slabs with TEAL outlines drop bottom-up,
labelled "OS files" (ORANGE fill), "packages" (GREEN), "your code" (GREY); a small lock glyph on
the stack's side, "read-only". At right, a TEAL config card with four empty rows `ENV`,
`ENTRYPOINT`, `CMD`, `WorkingDir`.
SAY: An image is a stack of read-only layers. Each layer holds the files that one build step added or changed. Beside the stack sits a small config card: settings such as environment variables, and which program to start.

SHOW: A GREY page glyph "Dockerfile" at far left with four lines `FROM …`, `RUN …`, `COPY …`,
`CMD …`. As each highlights: FROM points at the base slab; RUN and COPY each send a slab arrow onto
the stack, tag "adds a layer"; CMD sends an arrow to the card's CMD row, tag "config only".
SAY: The recipe that builds the stack is called a Dockerfile, and it runs one instruction at a time. Instructions that change files, like RUN and COPY, add a layer. Others, like CMD, only write on the card.

SHOW: The page fades. "docker run": a dashed, glowing TEAL glass slab appears on top of the stack
("writable layer") with a TEAL dot "process" inside; the group gets the label "container". A second
container appears: a second glass slab and dot beside the first, both linked by thin lines to the
SAME stack, caption "shared, not copied". The first dot goes out ("process ended → stopped"); a chip
`--rm` dissolves its glass slab. The stack is unchanged: GREEN check "image unchanged".
SAY: Run an image and you get a container: the same layers, shared, not copied, plus one thin writable layer on top, and one running process. When the process ends, the container stops, and the remove flag throws its writable layer away. The image never changes.

SHOW: Two captions under the picture: "image = class" · "container = instance" (TEAL). A README card
(`README.md · line 173`): "Build the docker container", the word "container" struck YELLOW with
"image" written above it, tag `erratum`; a smaller card under it (`README.md · line 146`): "copy
source code into the container".
SAY: Think of the image as a class, and each container as an instance. One small slip in the README: it says build the docker container. Building makes an image; running makes a container.

SHOW: A BLUE shelf unit at right, "registry · Docker Hub". Small TEAL stacks stand on it with sticky
notes `python:3.12-slim-bookworm` and `dlops/simple-translate:latest`. A note `:latest` peels off
and sticks to a newer stack; caption "a tag: a name that points at one image".
SAY: A registry, like Docker Hub, is a set of shelves where images are stored by name. A tag is a name that points at one image, such as latest.

SHOW: V8. Left: a BLUE box "VM" with its own "kernel" bar and an "OS" band on it (L1's server
slice). Right: three TEAL boxes "container" standing side by side on one GREY bar "Linux kernel ·
shared". A GREY laptop outline wraps the right half; a dashed GREY box "Linux VM · Docker Desktop"
slides in under the kernel bar, labelled "Mac · Windows". Then the laptop outline morphs into a BLUE
VM outline and the dashed box fades: caption "on a cloud VM: its own Linux".
SAY: And a container is not a small VM. A VM boots its own kernel, the core of the operating system. Containers are isolated processes that share one Linux kernel. On a Mac or Windows laptop, Docker Desktop quietly runs a small Linux VM to provide it; on a cloud VM, Docker runs right on the VM's Linux.

SHOW: L1's two RED-outlined chips return, "the operating system's files" and "system libraries",
and fly into the TEAL stack, turning ORANGE fills (GREEN check). Fade out.
SAY: Remember what a venv couldn't isolate in lecture 1: the operating system's files and its system libraries. Now they're inside the box.

---

## S03 · A clean slate, and the clone — `s03_cleanup.py` · `CleanSlate`

SHOW: TRACKER A1 (the tracker appears: "README › Developing App using Containers", 16 dots, with a
YELLOW pulse). A full-width laptop terminal fades in (title `laptop`, 10 rows, prompt
`student@laptop:~$`); a GREY note under it: "on a Mac: zsh, a % prompt · same commands". A small
GREY chip "Docker Desktop: running" with a GREEN dot at the terminal's top right.
SAY: Now the README section Developing App using Containers. Open a terminal on your laptop, with Docker Desktop running. On a Mac your prompt looks different, but the commands are the same.

SHOW: TRACKER A1. It types `docker container ls` → TERM(laptop/01: 2). The header row gets a GREY
label "the columns · no rows: nothing running". `▶ your turn`.
SAY: First, docker container ls lists running containers. Ours shows only the header, so nothing is running. Pause and run it.

SHOW: TRACKER A2. A README card (`README.md · line 116`): "Stop any container that is running".
Beside it a GREY chip `docker stop <CONTAINER ID>` with the tag "only if you have one · not run
here".
SAY: Next, stop any running container. There's nothing to stop here; if you have one, docker stop with its ID does it.

SHOW: TRACKER A3. It types `docker system prune` → TERM(laptop/02: 2–9; [y/N] y). The `y` keystroke
flashes YELLOW; line 9 (`Total reclaimed space: 0B`) gets a GREY label "a fresh Docker".
`▶ your turn`.
SAY: Then docker system prune. It lists what it will remove and asks; type y. Ours had nothing to reclaim. Pause and run it.

SHOW: TRACKER A3. Line 5 (`  - all dangling images`) highlights YELLOW with a GREY label "images
with no name"; a small TEAL stack with a name tag gets a GREEN check "named: kept". A README card
(`README.md · line 113`): "clear up an unused images", tag `erratum`; a GREY chip
`docker system prune -a` "every unused image".
SAY: Look at the third item: dangling images, the ones without a name. Despite the README's heading, named images survive; dash a would remove every unused image.

SHOW: TRACKER A4. It types `docker image ls` → TERM(laptop/03: 2; squeeze). The empty table gets a
GREY caption "no images yet" and the tag `at the time of recording` beside the header ("Docker 29's
columns").
SAY: Then docker image ls lists your images. Ours is empty. Your column names may differ: this is Docker 29, at the time of recording.

SHOW: TRACKER A5. A README card (`README.md · lines 122–123`): "If you cloned earlier on a VM, that
doesn't help here — Docker Desktop runs on your laptop". A small BLUE VM glyph holding a folder gets
a RED cross; a GREY laptop glyph gets a folder `simple-translate`. The terminal types
`git clone https://github.com/dlops-io/simple-translate.git` (folds onto a second row) →
TERM(laptop/04: 2), then `cd simple-translate` → (no output); the prompt becomes
`student@laptop:~/simple-translate$` and its new path flashes BLUE. A GREY tag "README.md · lines
50–51 · same as L1". `▶ your turn`.
SAY: Now the code. As the README notes, a clone on last lecture's VM doesn't help, because Docker Desktop runs on your laptop. So clone it here, with the same command as before, then cd into simple-translate. Pause and run both.

SHOW: TRACKER A5 · extra. It types `ls -a` (extra) → TERM(laptop/05: 4–12). `Dockerfile.txt`
highlights with a GREY tag "the solution"; two GREY dashed ghost chips appear beside the listing,
`Dockerfile` and `uv.lock`, captioned "not in the repo".
SAY: An extra check, not in the README: ls dash a. There's the solution, Dockerfile.txt, but no file called just Dockerfile, and no uv.lock.

SHOW: TRACKER A5 · extra. It types `docker build -t simple-translate -f Dockerfile .` (extra here: the
README's build command, run too early) → TERM(laptop/07: 7; wrap), RED. Fade out.
SAY: Try the README's build command now, as an extra, and it fails: failed to read dockerfile, no such file. The README wants you to write that file yourself, in five steps.

---

## S04 · Dockerfile step 1: FROM — `s04_from.py` · `StepFrom`

SHOW: TRACKER A6. A schematic editor sidebar (tag `illustration`): the file tree `simple-translate/`
with the entries of laptop/05 (`.git/`, `.gitignore`, `.vscode/`, `Dockerfile.txt`, `README.md`,
`cli.py`, `docker-build-push.sh`, `docker-shell.sh`, `pyproject.toml`); a new row `Dockerfile`
slides in YELLOW with the tag "exactly this name · no extension". A README card
(`README.md · lines 128–130`): "create a file called Dockerfile … (Do a Build + Run after each
step)". `▶ your turn`.
SAY: Next, inside the simple-translate folder, create a file called Dockerfile: capital D, no extension. The README fills it in five steps, with a build and a run after each one. Pause and create the file.

SHOW: TRACKER A7. CODE(README.md: 135–136) at the top. Under `python:3.12-slim-bookworm`, four
chips decode the name: `python` "official image", `3.12` "Python 3.12", `slim` "fewer packages",
`bookworm` "Debian 12". The strip terminal below types `cat Dockerfile` (extra) →
TERM(laptop/08: 2–3).
SAY: Dockerfile step 1 is one instruction: FROM python, 3.12, slim bookworm. It starts from the official Python image: a slim Debian 12, nicknamed bookworm, with Python 3.12 installed. Paste it in, save, and check with cat, an extra.

SHOW: The panel fades. The build command writes large in the center,
`docker build -t simple-translate -f Dockerfile .` (header `README.md · line 174`), and its parts get
labels in turn: `-t simple-translate` "the image's name" (TEAL), `-f Dockerfile` "the recipe", `.`
"build context: this folder" (PINK, pulsing).
SAY: Now the build command. Dash t names the image simple-translate, and dash f says which recipe to use. And the final dot is the build context: this folder, which Docker sends to the builder. Step 3 shows why that matters.

SHOW: The command slides into a full-width terminal (12 rows, prompt
`student@laptop:~/simple-translate$`) and is typed → TERM(laptop/09: 2, …, 15; cut after
`@sha256:34386ef0`, …, 31–34; hash12, …, 38). `▶ your turn`. The four sizes (`3.34MB`, `15.97MB`,
`28.25MB`, `249B`) highlight ORANGE; `simple-translate:latest` in line 38 highlights TEAL. Then the
terminal shrinks to the strip and V2 starts: four thin ORANGE slabs with TEAL outlines drop as one
group, labelled "python:3.12-slim-bookworm · Debian 12 + Python 3.12", the four sizes beside them.
SAY: Pause and run the build. Docker fetches the base image, four layers, under 50 megabytes compressed, and unpacks the result as simple-translate, latest. Those four layers are the bottom of our stack.

SHOW: The terminal grows back for a moment with two GREY notes: next to line 2's `"default"`,
"Docker Desktop: "desktop-linux""; across the top, "your terminal: a compact view · this is the full
log (--progress=plain)".
SAY: Your terminal shows this build as a compact view that updates in place; ours is the full log, which dash dash progress equals plain prints. And on Docker Desktop, the builder is called desktop linux, not default.

SHOW: TRACKER A7 · extra. Strip terminal (5 rows) types
`docker image inspect simple-translate --format 'Entrypoint={{json .Config.Entrypoint}} Cmd={{json .Config.Cmd}} WorkingDir={{json .Config.WorkingDir}}'`
(extra; folds) → TERM(laptop/10: 2). V3 on the TEAL config card beside the stack: two slots,
ENTRYPOINT `[ ]` (empty, GREY "null") and CMD holding a tile `["python3"]` tagged "inherited from the
base image"; WorkingDir `""`. Below the card, the start-up line assembles in mono: `python3` → a
small `>>>` glyph.
SAY: What will this image do when it starts? Ask its config card, with an extra command, docker image inspect. There's no entrypoint, and the command is python3, inherited from the base image. So we predict a Python prompt.

SHOW: TRACKER A7. Full terminal; it types `docker run --rm -ti simple-translate` (README.md line 180)
→ TERM(laptop/11: 2–3); at the `>>>` prompt it types `exit()` (line 4). `Python 3.12.15` gets the tag
`at the time of recording`. `▶ your turn`.
SAY: Now the run command: docker run, dash dash rm, dash t i, simple-translate. Pause and run it. There's the Python prompt, 3.12.15 at the time of recording. Type exit with parentheses to leave.

SHOW: TRACKER A7 · extra. It types `git status` (extra) → TERM(laptop/12: 2–5); line 5 highlights.
CODE(dot-gitignore.txt: 1–4) slides in (header `.gitignore · lines 1–4`), line 3 `Dockerfile`
highlighted YELLOW, tag `erratum`; a GREEN chip `git add -f Dockerfile` "to commit it anyway".
Fade out.
SAY: One surprise: an extra git status says nothing to commit, although we just made a file. The repo's gitignore lists Dockerfile on line 3, so git hides yours. To commit it anyway, use git add dash f.

---

## S05 · Step 2: ENTRYPOINT — `s05_entrypoint.py` · `StepEntrypoint`

SHOW: TRACKER A8. CODE(README.md: 142) at the top. Strip terminal (5 rows) types `cat Dockerfile`
(extra) → TERM(laptop/13: 2–5); line 5 highlights.
SAY: Step 2 adds one line: ENTRYPOINT, slash bin slash bash. Put it under the FROM line, and save.

SHOW: Full terminal; it types `docker build -t simple-translate -f Dockerfile .` → TERM(laptop/14: 15; cut after `@sha256:34386ef0`, 17, …, 25).
`#4 CACHED` highlights TEAL. `▶ your turn`. The terminal shrinks to the strip: the V2 stack (four
ORANGE slabs) is unchanged, and on the config card the ENTRYPOINT row fills with `["/bin/bash"]`;
caption "config only: nothing downloaded, no new layer".
SAY: Pause and build again. The base layer says CACHED: nothing is downloaded, and no layer is added. ENTRYPOINT only writes on the config card.

SHOW: V3 close-up of the card: the tile `["/bin/bash"]` sits in the ENTRYPOINT slot; the CMD slot
still shows the inherited `["python3"]` tile, now dashed; the start-up line reads
`/bin/bash python3` with a YELLOW "?". Two GREY labels under the slots: ENTRYPOINT "the program",
CMD "its default arguments".
SAY: Think of ENTRYPOINT as the program to start, and CMD as its default arguments. The entrypoint is now bash, and the command slot held python3. So will the container start bash, running python3?

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
SAY: Pause and run it: a bare prompt. Read it left to right. You're root, the administrator, but only inside the container. After the at sign comes the container's ID, which changes every run, so yours will differ.

SHOW: The slash part pulses; the GREY chip `WorkingDir=""` pulses with it. It types `exit` (capture
line 2) → TERM(laptop/16: 3); the laptop prompt returns. Fade out.
SAY: And the slash means you start in the top folder of the image, because this image sets no working directory. Type exit to leave.

---

## S06 · Step 3: install uv, copy the code — `s06_copy.py` · `StepCopy`

SHOW: TRACKER A9. CODE(README.md: 148–151) at the top; line 149 `RUN pip install uv` highlights
(a PURPLE `uv` chip pops beside it), then line 151 `COPY . ./`. Strip terminal (5 rows) types
`cat Dockerfile` (extra) → TERM(laptop/17: 7–10).
SAY: Step 3 adds two instructions. RUN pip install uv uses the base image's pip to install uv. And COPY dot dot slash copies the project folder into the image.

SHOW: V5 seed (strip hidden). The GREY project folder `simple-translate/` with file glyphs, `.git/`
and `Dockerfile` among them. The `.` at the end of the build command (written small above) lights
PINK; the whole folder packs into a parcel labelled "build context" and slides along a PINK arrow
into a PURPLE box "builder". Over the arrow hangs a GREY dashed sieve `.dockerignore`, with the tag
"none in this repo". In the builder, the parcel unpacks into the top folder `/` of the TEAL stack.
SAY: Here's why the final dot matters. Docker packs the whole folder, every file, including the hidden git folder and your Dockerfile, and sends it to the builder: that's the build context. The builder can use only what's in that parcel, and COPY unpacks all of it into the image's top folder.

SHOW: Full terminal (13 rows); it types `docker build -t simple-translate -f Dockerfile .` → TERM(laptop/18: 12–13, 16–17). Line 13
(`transferring context: 2B`) gets the GREY tag "no .dockerignore"; `63.12kB` in line 17 highlights
PINK, "the parcel". `▶ your turn`.
SAY: Pause and build. The log confirms it: the ignore file is empty, and the context, 63 kilobytes here, travels to the builder.

SHOW: The terminal continues → TERM(laptop/18: …, 27, 33, 34; wrap, …, 40–41). `uv-0.13.0` gets the
tag `at the time of recording`; the folded WARNING (line 34) gets a YELLOW bracket. The terminal
shrinks to the strip; V2: an ORANGE slab with a PURPLE `uv` chip, "RUN pip install uv", and a GREY
slab with file glyphs, "COPY . ./", drop onto the stack.
SAY: Then pip installs uv, version 0.13.0 at the time of recording, and COPY runs: two new layers. Pip also warns about running as root. In lecture 1 that warning mattered; here, the image itself is the isolation.

SHOW: The V2 stack with its two new slabs, above the strip.
PONDER(6 s, "uv is installed and the code is copied in.\nWill python cli.py run?")
SAY: Something to ponder: uv is installed, and the code is in the image. Will python cli.py run?

SHOW: Full terminal (13.2 wide, 20 pt for the `ls` columns); it types
`docker run --rm -ti simple-translate` → at the prompt `root@1f2c7df8735d:/#`, `ls` →
TERM(laptop/19: 3–7): `Dockerfile`, `Dockerfile.txt`, `README.md`, `cli.py`, `pyproject.toml`,
`docker-build-push.sh`, `docker-shell.sh` brighten GREY-white, the system folders (`bin`, `etc`,
`usr` …) dim ORANGE. `▶ your turn`.
SAY: No. Pause, run it, and look around with ls: our files sit right next to the system's own folders.

SHOW: At the same prompt it types `python cli.py` → TERM(laptop/19: 9–12), lines 9–12 RED; then
`exit` → TERM(laptop/19: 14). In a corner, the V2 stack: the PURPLE `uv` chip glows, and a dashed
GREY outline "packages: none yet" sits where a layer is missing.
SAY: Then python cli.py: ModuleNotFoundError, no module named art. We installed the installer, not the packages. Type exit.

---

## S07 · Step 4: uv sync, and two Pythons — `s07_uv_sync.py` · `StepUvSync`

SHOW: TRACKER A10. CODE(README.md: 157), `RUN uv sync` GREEN; above it a README card
(`README.md · line 155`): "Setup a virtual environment by running uv sync".
SAY: Step 4 adds RUN uv sync. As on the VM last lecture, uv sync reads pyproject.toml and installs the packages into a virtual environment.

SHOW: CODE(Dockerfile.txt: 2) (`3.12` ORANGE) beside CODE(pyproject.toml: 6) (`>=3.13` GREEN), and
three GREY answer chips: "fail?", "use 3.12 anyway?", "something else?".
PONDER(8 s, "This image's Python is 3.12.\npyproject.toml asks for 3.13 or newer.\nWhat will uv sync do during the build?")
SAY: Now predict. This image's Python is 3.12, and line 6 of pyproject.toml asks for 3.13 or newer. What will uv sync do during the build?

SHOW: Full terminal (12 rows); it types `docker build -t simple-translate -f Dockerfile .` → TERM(laptop/21: 23–24, 26–27). `#6 CACHED`
highlights TEAL; `#7 DONE 0.1s` highlights YELLOW with a GREY note "COPY ran again · part 2".
`▶ your turn`.
SAY: Pause and build. First, notice: the pip step is CACHED, but COPY ran again, although we only added a line at the end. Keep that question for part 2.

SHOW: The terminal continues → TERM(laptop/21: 29, 30; wrap, 32–34, 36–37, …, 47). Line 30
(`Downloading cpython-3.15.0-linux-x86_64-gnu (download) (35.9MiB)`) highlights PURPLE, `3.15.0`
gets the tag `at the time of recording`; `/.venv` (line 33) and `Installed 11 packages` (line 36)
highlight GREEN.
SAY: Now the answer. Just as on the Debian 12 VM in lecture 1, uv downloads a Python of its own: CPython 3.15.0, at the time of recording. Then it creates a virtual environment at slash dot venv, and installs 11 packages.

SHOW: The terminal shrinks to the strip. V4 above it (L1's number line, ticks 3.10 … 3.16): a GREEN
glow covers 3.13 and up, labelled `requires-python = ">=3.13"`. An ORANGE dot
`3.12.15 · /usr/local/bin/python · base image` lands on 3.12 with a RED cross. A PURPLE arrow from a
uv chip drops a GREEN dot `3.15.0 · uv-managed · 35.9 MiB download` into the glow, tag "the newest
uv knew · at the time of recording"; a GREEN chip `/.venv/bin/python` draws a link arrow to it. At
the right, V2: a fat GREEN slab "RUN uv sync · CPython 3.15.0 + /.venv · 11 packages" drops on the
stack.
SAY: On the number line, the requirement lights up 3.13 and newer. The base image's Python, 3.12, falls outside, so uv can't use it. Instead, uv downloads the newest Python it knows in the range, and the venv's python links to it. A fat green layer joins the stack.

SHOW: Full terminal (13.2 wide, 20 pt); it types `docker run --rm -ti simple-translate` → at the
prompt `root@01dca6d0f4d8:/#`, `ls -a` → TERM(laptop/22: 3–9): `.venv` and `uv.lock` highlight
GREEN. Then `python cli.py` → TERM(laptop/22: 11–14), RED. `▶ your turn`.
SAY: Pause and run it. Now ls dash a shows dot venv, and a new uv.lock. But python cli.py fails exactly as before. Why?

SHOW: The terminal shrinks to the strip. V4's PATH half: L1's doors, from the base image's
`ENV PATH=/usr/local/bin:/usr/local/sbin:/usr…` (laptop/34 line 22, as a GREY chip): `/usr/local/bin`
(ORANGE), `/usr/local/sbin`, `…`. A figure carrying `python` knocks on the first door and walks in to
the ORANGE `3.12.15` dot: "no art, no googletrans" → RED. Caption "venv not activated".
SAY: Remember lecture 1: activation is just PATH. Nothing has activated the venv, so the word python finds the base image's Python first, in user local bin. That's 3.12, and it has none of our packages.

SHOW: TRACKER A10 · extra. Full terminal continues at the same prompt: `.venv/bin/python --version`
(extra) → TERM(laptop/22: 16); then `source .venv/bin/activate && python cli.py` (extra) →
TERM(laptop/22: 28; wrap, 30–31): `Output: Adoro il formaggio` GREEN; the next prompt is
`(app) root@01dca6d0f4d8:/#` (line 32), `(app)` GREEN. In the doors picture above (shown again
briefly), a GREEN door `/.venv/bin` slides in at the front and the figure walks in to the GREEN
3.15.0 dot. Then it types `exit` (line 32) → TERM(laptop/22: 33).
SAY: Two extra checks in the same container. The venv's own python reports 3.15.0. And after sourcing the activate script, python cli.py works, I love cheese in Italian, and the prompt shows app in parentheses.

SHOW: The two dots side by side: ORANGE `3.12.15 · base · only ran pip install uv`, GREEN
`3.15.0 · uv-managed · runs the app`. Tag `erratum` (README.md line 133, Dockerfile.txt line 2 vs
pyproject.toml line 6). Two GREEN fix chips: `FROM python:3.13-slim-bookworm` · "or a requires-python
the image already meets". Fade out.
SAY: So this image carries two Pythons: 3.12 from the base, which only installed uv, and 3.15 for the app. That's a small mismatch in the tutorial. In your own projects, start from a Python 3.13 image, or make requires-python match the image you use.

---

## S08 · Step 5: CMD, the solution, the build — `s08_cmd.py` · `StepCmd`

SHOW: TRACKER A11. CODE(README.md: 163–164) at the top. Strip terminal (5 rows) types
`cat Dockerfile` (extra) → TERM(laptop/23: 14–15).
SAY: Step 5 adds the last instruction: CMD, with dash c and one quoted command: source the activate script, and exec bash.

SHOW: V3 card: the tile `["-c", "source .venv/bin/activate && exec bash"]` slides into the CMD slot
beside ENTRYPOINT `["/bin/bash"]`. Strip types
`docker image inspect simple-translate --format 'Entrypoint={{json .Config.Entrypoint}} Cmd={{json .Config.Cmd}}'`
(extra; folds) → TERM(laptop/25: 2; wrap). The start-up line assembles under the card:
`/bin/bash -c "source .venv/bin/activate && exec bash"`. Then a small bash bubble "bash 1" runs
`source …`: a miniature PINK door row gets a GREEN `/.venv/bin` door at the front; `exec bash`
morphs bubble 1 into "bash 2 · interactive", which keeps the same door row.
SAY: On the card, entrypoint plus command make one command line: bash, dash c, then that string. The first bash sources the activate script, which puts the venv's bin folder first in PATH. Then exec bash replaces it with a fresh, interactive bash that keeps the new PATH.

SHOW: Full terminal (12 rows); it types `docker build -t simple-translate -f Dockerfile .` → TERM(laptop/24: 23–24, 26–27, 29, 30; wrap).
`▶ your turn`. Lines 27 and 30 highlight YELLOW, GREY note "one line added · part 2 explains".
SAY: Pause and build. Again COPY and uv sync run, and Python downloads again, for one added line. Part 2 explains why.

SHOW: It types `docker run --rm -ti simple-translate` → at the prompt `root@473b6edd3dab:/#`:
`which python`, `python --version`, `echo $VIRTUAL_ENV` (extras) → TERM(laptop/26: 3, 5, 7), then
`exit` → TERM(laptop/26: 9). `▶ your turn` beside the run. The prompt gets a GREY tag "no (app)";
`/.venv/bin/python`, `Python 3.15.0` and `/.venv` highlight GREEN; a GREY tag "not an error".
SAY: Pause and run it. No app in parentheses this time; is the venv active? These extra checks say yes: which python points into dot venv, it's 3.15.0, and the virtual env variable is set. The fresh bash simply set its own prompt.

SHOW: TRACKER A12 · extra. A README card (`README.md · lines 167–168`): "Solution Dockerfile:
Dockerfile.txt". The terminal clears; it types `diff Dockerfile Dockerfile.txt` (extra) →
TERM(laptop/27: 8–18) (11 rows; `+` lines GREEN, `-` lines dim RED). The three `+ENV` lines
(10, 15, 18) get GREY labels: "no apt questions", "UTF-8 text", "logs appear at once".
SAY: The README then points to a solution, Dockerfile.txt. An extra diff shows how it differs from ours. First, three ENV lines: no questions from apt, a UTF-8 locale, and unbuffered output, so logs appear right away.

SHOW: The terminal continues → TERM(laptop/27: …, 20–26, …, 33–34) (it scrolls). Lines 21–26 get an
ORANGE bracket "one RUN: update, upgrade, clean, newer pip, uv"; lines 33–34 a YELLOW bracket
"ENTRYPOINT moved to the end".
SAY: Second, one bigger RUN: update and upgrade Debian's packages, clean up, upgrade pip, and install uv. And ENTRYPOINT moved to the end; the order of the ENTRYPOINT and CMD lines doesn't matter.

SHOW: TRACKER A12 · extra. It types `cp Dockerfile.txt Dockerfile` (extra) → (no output). GREY note
"the README only names the file". `▶ your turn`.
SAY: The README only names the file, so here's the quickest way to use it, an extra: copy it over yours, with cp. Pause and do that.

SHOW: TRACKER A13. A README card (`README.md · lines 172–174`): "In a terminal make sure you are the
location of simple-translate". The terminal clears; it types
`docker build -t simple-translate -f Dockerfile .` → TERM(laptop/29: 3; fit, 9; cut after
`python:3.12-slim-bookworm`, 13–15; fit, 22; fit) — the compact view. `▶ your turn`. `13.3s` and
`4.9s` highlight; `simple-translate:latest` highlights TEAL; GREY tag "what your terminal shows".
SAY: Now the README's Build Docker Image section: from inside the simple-translate folder, run the same build. Pause and run it. This compact view is what you'll see: four steps, the apt and pip step the slowest, and the image named simple-translate again.

---

## S09 · Run it, translate, exit — `s09_run.py` · `RunIt`

SHOW: TRACKER A14. Full terminal (13 rows). It types `docker run --rm -ti simple-translate` → the
prompt `root@93d61f44d3d7:/#` (laptop/31 line 2). TRACKER A15. It types
`python cli.py -t "Good morning" -s "en" -d "es"` (README.md line 182; folds) →
TERM(laptop/31: 5–9, 13; wrap, 15–16): banner, arguments, `Input: Good morning`, `Output: Buen día`
GREEN. `▶ your turn`.
SAY: Now Run Docker Container: docker run, dash dash rm, dash t i, simple-translate. At the container's prompt, type the README's translation: Good morning, from English to Spanish. Pause and run both.

SHOW: The Output line enlarges. Small picture above the strip: a TEAL container inside a GREY
laptop; a PINK arrow leaves the laptop to a BLUE cloud `translate.googleapis.com` and comes back.
SAY: Good morning comes back in Spanish. The request went from inside the container, out through your laptop's network, to Google's translate service.

SHOW: TRACKER A16. It types `exit` (laptop/31 line 17) → TERM(laptop/31: 18); the prompt
`student@laptop:~/simple-translate$` returns. `▶ your turn`.
SAY: To leave, type exit, and you're back on your laptop. Pause and do it.

SHOW: TRACKER A16 · extra. V2 container picture above the strip: the TEAL stack, the dashed glowing
glass slab on top, a dot "process". The `exit` replays: the dot goes out ("stopped"); a chip `--rm`
dissolves the glass slab; the stack stays (GREEN check "image unchanged"). Strip types
`docker ps -a` (extra) → TERM(laptop/32: 2; squeeze): the header only.
SAY: What did exit do? It ended the container's process, so the container stopped, and dash dash rm then deleted it, writable layer and all. An extra docker ps dash a lists every container, even stopped ones: nothing is left. The image is untouched.

SHOW: TRACKER A16 · extra. Strip (4 rows), a second run (extra): it types
`docker run --rm -ti simple-translate` → at the prompt `root@1d1fecf6ff8f:/#` it types `echo $$`
(line 4) → TERM(laptop/33: 5), then TERM(laptop/33: …) (GREY caption on the `…`: "more checks · part
2"), then it types `exit` (line 29) → TERM(laptop/33: 30). A new glass slab and dot appear on the
picture; the `1` flies to the dot's label "PID 1 · bash". Labels: `-i` "your keyboard → bash",
`-t` "a terminal: prompt, line editing".
SAY: In a second run, the extra check echo dollar dollar shows that bash is process number 1; the container lives exactly as long as it does. Dash i connects your keyboard to it, and dash t gives it a terminal.

SHOW: V3 card: ENTRYPOINT `["/bin/bash"]`, CMD `["-c", "source … && exec bash"]`. Above it a chip
`docker run --rm -ti simple-translate python cli.py` with `python cli.py` boxed YELLOW.
PONDER(8 s, "docker run --rm -ti simple-translate python cli.py\nWhat command line does the container actually run?")
SAY: Now a puzzle. What if you put the command right after the image name: docker run, simple-translate, python cli.py? What command line does the container actually run?

SHOW: A WHITE tile `python cli.py` flies from the end of the chip and knocks the CMD tile off the
card; the start-up line reads `/bin/bash python cli.py` and flashes RED. Bash's view: `python` as a
"script name"; the PINK door row without any venv door; the first door `/usr/local/bin` holds the
ORANGE `python` program, stamped RED "a program, not a script". Strip types
`docker run --rm -ti simple-translate python cli.py` (extra) → TERM(laptop/36: 2; wrap), RED; a RED
tag "exit 126".
SAY: Words after the image name replace CMD, and only CMD. So the container runs bash, python cli.py. Bash takes python as the name of a script, finds the Python program in user local bin, sees a binary, and refuses: cannot execute binary file, exit code 126.

SHOW: A tile `-c "source .venv/bin/activate && python cli.py -d fr"` replaces CMD; the start-up line
turns GREEN. Strip (5 rows) types
`docker run --rm simple-translate -c "source .venv/bin/activate && python cli.py -d fr"` (extra;
folds) → TERM(laptop/37: 12; wrap, 14–15); `Output: j'adore le fromage` GREEN.
SAY: To run it in one go, replace CMD with your own dash c string, as in this extra: activate, then translate to French.

SHOW: CODE(docker-shell.sh: 10–15), lines 11 and 15 highlighted, GREY tag "not in the README".
SAY: The repo also has a helper, docker-shell.sh, that builds and runs in one go; it isn't in the README.

SHOW: Part-1 recap: the full V2 stack (4 ORANGE base slabs, the ORANGE apt/pip slab, the GREY COPY
slab, the GREEN uv sync slab) with the config card; a TEAL check "your image: built and run".
Closing card: "Part 2: what's inside, why it rebuilt, and shipping it to a VM". Fade to an empty
frame (end of part 1).
SAY: You've built and run your own image. In part 2: what's inside it, why it keeps rebuilding, and how to ship it to a VM.

---

## S10 · What's inside the image — `s10_inside.py` · `InsideTheImage`

SHOW: TRACKER A16 · extra (for the whole scene). Full laptop terminal (12 rows); it types
`docker image ls` (extra) → TERM(laptop/30: 2, 4; squeeze) (row 3 never printed). `518MB` and
`144MB` highlight, with GREY labels "disk: unpacked + content" and "content: compressed layers, what
travels"; tag `at the time of recording`; a GREY note "Docker Desktop may show other columns".
SAY: Part 2 starts by opening the image we built; every check in this scene is an extra. First, docker image ls: 518 megabytes on disk, and 144 of content, at the time of recording. Content is the compressed layers that travel to a registry; disk adds the unpacked copy.

SHOW: It types `docker history simple-translate` (extra) → TERM(laptop/34: 2–10; cols CREATED BY,
SIZE). Rows 5 (`125MB`), 6 (`250kB`) and 7 (`97.5MB`) highlight in their slab colours; rows 3–4 and
8–10 (`0B`) GREY, "config only". The terminal shrinks to the strip; V2's slabs rescale to these
sizes: a fat GREEN `uv sync` slab, a GREY sliver for COPY, an ORANGE apt/pip slab; the card lists
the 0B rows.
SAY: Then docker history lists the layers, newest first. Read it bottom-up, and it's the Dockerfile top-down: the apt and pip step, 97.5 megabytes, our code, 250 kilobytes, and uv sync, 125. The ENV, ENTRYPOINT and CMD rows are zero bytes: config only.

SHOW: The terminal grows back and continues → TERM(laptop/34: …, 14–23; cols CREATED BY, SIZE) (it
scrolls). Line 18 `ENV PYTHON_VERSION=3.12.15` highlights ORANGE, line 22 `ENV PATH=/usr/local/bin:…`
PINK, line 23 (`debian.sh … 'bookworm'`, `85.3MB`) ORANGE. V2's base slabs rescale (85.3MB, 9.7MB,
54.5MB, 16.4kB); GREY note "the download in Dockerfile step 1 was compressed · history shows unpacked sizes".
SAY: Below them sit the base image's own rows: Debian bookworm at the bottom, the PATH that puts user local bin first, and Python 3.12.15. Remember, the download in Dockerfile step 1 was compressed; history shows unpacked sizes.

SHOW: The terminal clears and replays the second run from S09 (GREY caption "the second run from
part 1 · its hidden checks"): `docker run --rm -ti simple-translate`, the prompt
`root@1d1fecf6ff8f:/#`, then the `…` of S09 opens up: it types `python --version` (line 8) →
TERM(laptop/33: 9) (`Python 3.15.0` GREEN), `/usr/local/bin/python --version` (line 10) →
TERM(laptop/33: 11) (`Python 3.12.15` ORANGE), `ls /root/.local/share/uv/python` (line 12) →
TERM(laptop/33: 13) (GREEN). V4 coda in a corner: the two dots on the number line flash.
SAY: Back in the second run from part 1, we checked more before typing exit. There, python is 3.15.0, while the base image's Python is still 3.12.15. Most of that 125 megabyte layer is this second Python, in uv's own folder.

SHOW: Terminal (13.2 wide, 20 pt) continues the same run: `ls -a /` (line 21) → TERM(laptop/33: 22–28) (columns kept);
`.git`, `.gitignore`, `.vscode`, `Dockerfile`, `README.md` brighten with a PINK bracket "from the
build context"; then `exit` → TERM(laptop/33: 30). V5's parcel flashes in a corner, its `.git/`
glyph lit.
SAY: Now list the top folder. Beside the system folders sit the hidden git folder, the editor's VS Code folder, the README and your Dockerfile. COPY dot dot slash copied the whole build context, your git history included.

SHOW: Tag `erratum` "no .dockerignore". A small GREY card, tag `illustration` ("a file you'd add"):
`.dockerignore` with three GREEN lines `.git`, `.venv`, `secrets/`. The dashed sieve from S06 fills
in over the parcel and catches `.git/`. A small BLUE shelf glyph pulses with a GREY tag
"public, soon". Fade out.
SAY: That's a gap in the tutorial: there's no dockerignore file. It works like gitignore, but for the build context. In your own projects, list dot git, dot venv and your secrets folder there. It matters most once the image is public, and that's soon.

---

## S11 · The layer cache — `s11_cache.py` · `LayerCache`

SHOW: TRACKER A16 · extra. V5 full, concept first: four boxes in a row, `[1/4] FROM` ·
`[2/4] RUN apt…uv` · `[3/4] COPY . ./` · `[4/4] RUN uv sync`, linked left to right; each carries a
small fingerprint badge "parent + instruction", and COPY's badge adds "+ checksum of the files". A
row of dominoes stands under the boxes.
SAY: So why did COPY and uv sync rerun when we only added a line? Docker caches every build step. A step is reused when its parent, its instruction and, for COPY, a checksum of the copied files all match. The first step that changes runs again, and so does every step after it.

SHOW: A bottom terminal of 8 rows (the boxes stay above it) types
`docker build --progress=plain -t simple-translate -f Dockerfile .` (extra flag; tag "extra · full
log"; folds) → TERM(laptop/38: 23; cut after `apt-get update &&`, 24, 26–27, 29–30). Boxes 2–4 get a TEAL
`CACHED` stamp as their lines print; box 1 gets a TEAL "reused" stamp (the plain log just resolves
the base, `#4 DONE 0.0s`; the compact view calls it `CACHED`, laptop/29 line 9).
SAY: Rebuild with nothing changed, adding the extra flag for the full log. FROM reuses the base, and the three steps after it all say CACHED: nothing runs at all.

SHOW: CODE(cli.py: 45–51) slides in at left, line 49 `default="I love cheese",` highlighted.
PONDER(8 s, "You change one word in cli.py and rebuild.\nWhich of the four steps run again?")
SAY: Now predict. You change one word in cli.py and rebuild. Which of the four steps run again?

SHOW: Line 49 morphs: `"I love cheese"` → `"I love brie"` (YELLOW). The bottom terminal types `git diff` (extra)
→ TERM(laptop/39: 10–11) (`-` RED, `+` GREEN). In V5, the parcel's `cli.py` glyph flips YELLOW and
COPY's checksum badge turns RED.
SAY: Let's try it, as an extra: change the default on line 49 from I love cheese to I love brie. Git diff shows the change, and the build context now has a different checksum.

SHOW: The bottom terminal (8 rows) types
`docker build --progress=plain -t simple-translate -f Dockerfile .` (extra) → TERM(laptop/40: 23; cut after
`apt-get update &&`, 24, 26–27, 29–30; wrap, …, 36). Boxes 1–2 keep their TEAL stamps; a RED wave
knocks over dominoes 3 and 4; a PURPLE "35.9 MiB" download arrow fires into box 4.
SAY: Rebuild. FROM and the apt and pip step are reused. But the copy's checksum changed, so COPY runs, and uv sync after it, Python download and all. Like dominoes: a change knocks over its own step and every step after it.

SHOW: The bottom terminal types `git checkout -q cli.py` (extra; as run in `run_steps.sh` line 139) → (no output);
line 49 morphs back to `"I love cheese"`. Then
`docker build --progress=plain -t simple-translate -f Dockerfile .` (extra) → TERM(laptop/41: 26–27, 29–30; wrap).
In V5, a small glyph `.git/index` inside the parcel flips YELLOW; COPY's badge stays RED and the wave
runs again.
SAY: Now undo the edit with git checkout. Same files, so the cache comes back? No: COPY and uv sync run again. Git rewrote its own index file, inside the hidden git folder, and that folder is part of the build context too.

SHOW: A `Dockerfile` glyph inside the parcel flips YELLOW; caption "Dockerfile steps 4 and 5: every
edit to the Dockerfile changed the parcel". Tag `erratum` "expected while learning".
SAY: That answers the question from part 1. Your Dockerfile sits in the build context too, so every edit to it changed the copy. While you follow the README step by step, that's expected.

SHOW: The fix animates, tag "a pattern for your own projects · not the course solution": the boxes
reorder to `COPY pyproject.toml README.md ./` → `RUN uv sync` → `COPY . ./` (as tested in the digest's
exercise E2); a `.dockerignore` sieve over the parcel catches `.git/` and `Dockerfile`. `cli.py` is
edited again: the RED wave reaches only the last box; `RUN uv sync` keeps `CACHED`. GREY footnote
"full Dockerfile: exercises.md". Fade out.
SAY: In your own projects, put the slow steps first: copy only the files uv sync needs, run it, then copy the rest. A dockerignore keeps the git folder and the Dockerfile out. Now an edit to cli.py reruns only the last COPY. The full file is in the exercises.

---

## S12 · Tag and push — `s12_push.py` · `TagAndPush`

SHOW: TRACKER B1 (the tracker switches to "README › Pushing Docker Image to Docker Hub", 4 dots). A
schematic browser card (tag `illustration`): "Docker Hub · account settings", a row "Personal access
tokens" and a button "Generate new token"; a token field shows `<ACCESS TOKEN>` with a lock glyph.
A README card (`README.md · line 188`). GREY note "a token is a password: never in a file, never in
a repo".
SAY: Now we ship it, with the README section Pushing Docker Image to Docker Hub. First, sign up on Docker Hub and create an access token in your account settings. It works like a password, so keep it out of files and repos.

SHOW: TRACKER B2. CODE(README.md: 189), `<USER NAME>` and `<ACCESS TOKEN>` boxed YELLOW, "yours". A
GREY note: "no Docker Hub account in our recording · not run here".
SAY: Next, log in: docker login, dash u with your user name, dash p with your token. We have no Docker Hub account here, so we couldn't run this one.

SHOW: TRACKER B2 · extra. A terminal (8 rows) with `stand_in_tag()` on its frame types
`docker login localhost:5000 -u student -p not-a-real-token` (folds) → TERM(laptop-push/05: 2, 8).
Line 2 (`WARNING! Using --password via the CLI is insecure. Use --password-stdin.`) highlights
YELLOW; `Login Succeeded` GREEN.
SAY: So for some steps we use a stand-in: a small registry on our own machine. Logging in to it prints a warning: a password on the command line is insecure.

SHOW: Tag `illustration`: a GREY list "~/.bash_history" where the line
`docker login -u <USER NAME> -p <ACCESS TOKEN>` lands, the token part RED; tag `erratum`. Then a
GREEN chip `docker login -u <USER NAME>` followed by a GREY prompt line "Password:" and a paste
glyph; `▶ your turn` beside the chip, with a GREY note "or the README's form".
SAY: That's a small slip in the README: with dash p, your token stays in your shell history. Instead, type docker login dash u with your user name, and paste the token when it asks. Pause and log in.

SHOW: TRACKER B3. CODE(README.md: 190) at the top, with the YELLOW caption "`<USER NAME>` = your
Docker Hub username (here: student)". The laptop terminal (prompt
`student@laptop:~/simple-translate$`) types `docker tag simple-translate student/simple-translate-ac215`
→ TERM(laptop/43) → (no output). `▶ your turn`. Then `docker image ls` (extra) →
TERM(laptop/44: 2, 4–5; squeeze) (row 3 never printed); both `b5c531a6b555` highlight TEAL.
SAY: Then tag the image: docker tag, simple-translate, then your user name, slash simple-translate-ac215. Pause and run it with your own name. An extra image ls shows two names with the same image ID: a tag is a second name, not a copy.

SHOW: V6: a TEAL stack with the ID `b5c531a6b555`; two TEAL sticky notes point at it,
`simple-translate:latest` and `student/simple-translate-ac215:latest`. The long note unfolds into
four parts: `docker.io` "registry · the default", `student` "account", `simple-translate-ac215`
"repository", `latest` "tag". Under it, a GREY chip from the build logs,
`docker.io/library/simple-translate:latest`, "no account → library".
SAY: Read the long name in four parts: the registry, docker dot I-O, the default; your account; the repository; and the tag, latest. Names without an account, like our first one, fall under library.

SHOW: TRACKER B4. CODE(README.md: 191). The laptop terminal clears and types
`docker push student/simple-translate-ac215` → TERM(laptop-push/03: 2–8; wrap), line 8 RED; tag
`real capture · 2026-10-13`. A BLUE shelf "Docker Hub" with its door shut RED. GREY note "if you see
this: log in · the name must start with YOUR username". `▶ your turn`.
SAY: Then push: docker push, with the same name. Pause and run it. Push access denied means you're not logged in, or the name doesn't start with your user name; that's Docker Hub's real answer to us, without an account.

SHOW: TRACKER B4 · extra. The stand-in terminal (tag `stand-in`) types
`docker tag simple-translate localhost:5000/student/simple-translate-ac215` (folds) → (no output),
then `docker push localhost:5000/student/simple-translate-ac215` (folds) →
TERM(laptop-push/07: 3–4, …, 15; hash12). V6: slabs travel a PINK route to a dashed BLUE shelf
"stand-in registry".
SAY: On the stand-in, the push goes through: each layer is pushed, and the registry answers with a digest, a fingerprint of the whole image.

SHOW: The same push again → TERM(laptop-push/08: 4, …, 14–15; hash12). Each slab bounces back off
the shelf, "already exists". Then a schematic Docker Hub repository card (tag `illustration`) with a
BLUE "public" badge and a `.git/` glyph inside its stack. Fade out.
SAY: Push again, and every layer already exists: only missing layers ever travel. On Docker Hub, the base layers may even say mounted from library python. And remember: a new Docker Hub repository is public by default, git folder and all.

---

## S13 · Platforms: arm64 vs amd64 — `s13_platforms.py` · `Platforms`

SHOW: TRACKER B4 · extra (for the whole scene). Laptop terminal types
`uname -m; docker image inspect simple-translate --format '{{.Os}}/{{.Architecture}}'` (extra; folds)
→ TERM(laptop/35: 2–3). Both lines highlight BLUE; a GREY note "Apple Silicon Mac: arm64".
SAY: One more check before the VM, and this whole scene is extras. Our recording machine is an Intel or AMD one, and the image says linux slash amd64. On an Apple Silicon Mac, you'd see arm64.

SHOW: V7 (terminal hidden): two chips, `arm64 · Apple Silicon` (GREY, a laptop glyph) and
`amd64 · Intel/AMD · default GCP VM` (BLUE, a VM glyph), each with its own row of small glyphs,
"machine instructions". A TEAL image box shows `bash`, `python`, `uv` written in amd64 glyphs, with
a GREY note "no kernel inside to translate".
SAY: Why does that matter? Every program in an image, bash, Python, uv, is machine code for one kind of CPU. Intel and AMD chips speak amd64; Apple Silicon speaks arm64. A container has no kernel of its own to translate, so the CPU must speak the image's language.

SHOW: Terminal (13 rows) types `docker buildx imagetools inspect python:3.12-slim-bookworm` (extra;
folds) → TERM(laptop-push/11: 2–3, 9, …, 30, …, 51, …, 72, …, 93). V7: the tag unfolds into a menu
card with five platform rows (`linux/amd64`, `linux/arm/v7`, `linux/arm64/v8`, `linux/386`,
`linux/ppc64le`); GREY dimmed rows "attestation" between them; a BLUE arrow from a VM glyph points
at the amd64 row.
SAY: A tag can point at a menu, with one image per platform. The official python image lists five, amd64, two kinds of arm, and two rarer ones. When you pull, Docker picks the row that matches your machine.

SHOW: It types `docker buildx imagetools inspect dlops/simple-translate` (extra) →
TERM(laptop-push/10: 2–4; hash12). Line 3's `manifest.v2+json` highlights: "a single page, not a
menu"; a GREY chip from vm-debian12/08 line 3: `linux/amd64`. CODE(docker-build-push.sh: 26–27),
`--platform linux/amd64,linux/arm64` highlighted, tag `erratum` "would push both".
SAY: The instructor's image, dlops slash simple-translate, is a single page, amd64 only, although the repo's push script would build both platforms.

SHOW: Stand-in terminal (tag `stand-in`) types
`docker buildx imagetools inspect localhost:5000/student/simple-translate-ac215` (extra; folds) →
TERM(laptop-push/09: 3, 9, 13). V7: a small menu "our push": a BLUE `linux/amd64` row and a dimmed
`unknown/unknown` row, "attestation · how it was built"; a GREY dashed overlay on the first row:
"built on a Mac: linux/arm64".
SAY: Our stand-in push is a small menu: amd64, plus an attestation, a record of how the image was built. On an Apple Silicon Mac, that first row would say arm64.

SHOW: V7: the GREY arm64 chip builds an image in arm64 glyphs; a PINK route carries it past a BLUE
shelf to a BLUE VM with an amd64 chip.
PONDER(8 s, "You built on an M-series Mac and pushed.\nYour VM is an ordinary Intel/AMD machine.\nWill your image run there?")
SAY: Now ponder. You built on an M-series Mac and pushed. Your VM is an ordinary Intel or AMD machine. Will your image run there?

SHOW: The VM orders "amd64" from the arm64-only menu: nothing it can run, RED. Tag
`extra · arm64 image on an amd64 machine`. Terminal types
`docker run --rm --platform linux/arm64 debian:12 uname -m` (extra; folds) →
TERM(laptop-push/12: 2, …, 10); line 10 `exec /usr/bin/uname: exec format error` RED.
SAY: No. Here's the same failure the other way round, for real: an arm64 image on our amd64 machine. Exec format error. A Mac-built image on a default VM fails like this, or Docker refuses it up front with no matching manifest.

SHOW: CODE(docker-shell.sh: 11–12), line 12 (`#docker build -t $IMAGE_NAME --platform=linux/amd64 -f Dockerfile .`)
highlighted YELLOW with the GREY tag "commented out · not in the README". V7: the arm64 chip's build
passes through a GREY "emulation" box and the image's glyphs turn amd64.
SAY: Two fixes in the repo, neither in the README. One: build for the VM's platform, with dash dash platform equals linux slash amd64, as in the commented-out line 12 of docker-shell.sh. On a Mac, that build runs under emulation: slower, but it works.

SHOW: CODE(docker-build-push.sh: 21–27), lines 23 and 27 highlighted; above it CODE(docker-build-push.sh: 11)
`DOCKER_USERNAME="dlops"` with a YELLOW caption "your username". Two GREY chips: `bash docker-build-push.sh`
"not executable" and `docker buildx use default` "afterwards · desktop-linux on Docker Desktop". V7:
buildx cooks two pages, amd64 and arm64, and pushes one menu with both. Fade out.
SAY: Two: docker-build-push.sh builds both platforms with buildx and pushes one menu. Put your user name on line 11, and run it with bash. Afterwards, switch back with docker buildx use default, or desktop linux on Docker Desktop, so plain builds land on your laptop again.

---

## S14 · A VM with only Docker — `s14_vm_docker.py` · `DockerOnVM`

SHOW: TRACKER C1 (the tracker switches to "README › Running App on VM using Docker", 7 dots). A
schematic console (browser, tag `illustration`, as in L1): VM instances → Create instance; form rows
fill: Name `ac215-l02` · Machine type `e2-small` · Boot disk `Debian GNU/Linux 12 (bookworm)`; GREY
footnote "the README gives no settings: sensible choices · Debian 13 works too · E2 = amd64". The
GOLD dial starts sweeping, with tags "billed per second while running" and "disk: billed while it
exists".
SAY: The last README section: Running App on VM using Docker. First, create a VM, as in lecture 1. The README gives no settings; an ordinary E2 machine, which is amd64, with Debian 12 or 13 will do. The meter starts: by the second while it runs, and for its disk while it exists.

SHOW: TRACKER C2. "SSH" is clicked: the browser window transforms into a terminal (title
`ssh · ac215-l02`, prompt `student@ac215-l02:~$`). `▶ your turn`.
SAY: Next, SSH in. Pause until your terminal is open.

SHOW: TRACKER C3. It types `sudo apt install docker.io` (README.md line 210) →
TERM(vm-debian12/01: 4–8; +Done); lines 7–8 RED. `▶ your turn`. A small GREY card "Debian 13" shows
TERM(vm-debian13/01: 7) (`Error: Unable to locate package docker.io`).
SAY: Then install Docker: sudo apt install docker dot I-O. Pause and run it. On a fresh Debian, it fails: unable to locate package. On Debian 13 the line starts with Error.

SHOW: Two README cards side by side: `README.md · line 210` (`sudo apt install docker.io`) and
`README.md · line 44` (`sudo apt-get update`, from the L1 walkthrough); tag `erratum`. An ORANGE
catalog book "package lists" stands empty. TRACKER C3 · extra. It types `sudo apt-get update` (extra)
→ TERM(vm-debian12/02: 8–9; +Done); the book fills. `▶ your turn`.
SAY: A small gap in the README: here it skips sudo apt-get update, which it used in lecture 1. On a fresh VM the package lists are empty, so apt knows no packages yet. Run the update first, an extra, and pause after it.

SHOW: TRACKER C3. It types `sudo apt install docker.io` again →
TERM(vm-debian12/03: 4–6; +Done, 55–56, 57; wrap, 58; [Y/n] Y, …, 560, 581). Lines 55–56 highlight;
GREY tag "package list varies by VM"; the `Y` flashes YELLOW. The small GREY "Debian 13" card shows
TERM(vm-debian13/03: 77–78). `▶ your turn`.
SAY: Now the install works: 92 new packages and 107 megabytes on Debian 12; 91 packages and 118 on Debian 13. Answer Y. On a real Google image the list may be shorter. Pause and run it.

SHOW: TRACKER C4. It types `sudo docker --version` → TERM(vm-debian12/04: 2); the GREY "Debian 13"
card shows TERM(vm-debian13/04: 2). Both get the tag `at the time of recording`; a PURPLE chip
`docker.io · Debian's package`.
SAY: Then sudo docker dash dash version. This is Debian's own Docker package: 20.10.24 on Debian 12, 26.1.5 on Debian 13, at the time of recording. Older than the laptop's, and plenty to run an image.

SHOW: V8, S14 half, above the strip: a BLUE VM box; inside it, a PURPLE `dockerd` block sits directly
on the VM's own bar "Debian · Linux kernel"; an empty TEAL container slot above it; no dashed
Linux VM. TRACKER C4 · extra. Strip types `docker ps` (extra) → TERM(vm-debian12/05: 2; wrap), RED;
a lock glyph on a socket icon `/var/run/docker.sock`, GREY labels "root · docker group". Fade out.
SAY: Here Docker runs right on the VM's Linux kernel; there's no hidden VM. And why sudo? Without it, this extra docker ps is refused: permission denied on the Docker socket. Only root and the docker group may use it.

---

## S15 · One-command deploy — `s15_deploy.py` · `Deploy`

SHOW: TRACKER C5. VM terminal (12 rows) types `sudo docker run --rm -ti dlops/simple-translate`
(README.md line 215) → TERM(vm-debian12/06: 2–4, …, 10–12; hash12). `▶ your turn`. The terminal
shrinks to the strip; V6 above: seven slabs come down a PINK route from the BLUE Docker Hub shelf
into the BLUE VM and stack up; a TEAL glass slab appears on top.
SAY: Then the deploy: sudo docker run, dash dash rm, dash t i, dlops slash simple-translate. Pause and run it. The image isn't on this VM yet, so Docker pulls it from Docker Hub, seven layers, then starts a container.

SHOW: TRACKER C6. Full terminal; the prompt `root@c7c280390994:/#` (line 13); it types `python cli.py`
(README.md line 218) → TERM(vm-debian12/06: 16–20, 24; wrap, 26–27). `Output: Adoro il formaggio`
GREEN. `▶ your turn`.
SAY: Now run the app with python cli.py and its defaults: I love cheese comes back in Italian. Pause and run it. There's no clone, no pip and no uv on this VM: just Docker and one image.

SHOW: TRACKER C6 · extra. It types `python --version` (extra) → TERM(vm-debian12/06: 29). The terminal
shrinks to the strip. V4 coda: the number line returns; next to our GREEN dot
`3.15.0 · our build · 2026-10-13 · uv 0.13.0`, a second GREEN dot lands in the same glow:
`3.14.7 · dlops/simple-translate · built 2026-09-16 · uv 0.12.15`. Two GREY source chips:
TERM(vm-debian12/08: 3) ("created 2026-09-16…", from an extra `sudo docker image inspect`) and
TERM(vm-debian12/10: 8) (`uv = 0.12.15`, the image's `pyvenv.cfg`).
SAY: And the opening question: why 3.14.7, when the recipe says 3.12? The same reason as in our build. This image was built on September 16 with uv 0.12.15, and the newest Python it knew in the range was 3.14.7. Ours, built today, got 3.15.0.

SHOW: Three GREY chips light in turn: `pip install uv` "unpinned" (Dockerfile.txt line 19),
`requires-python = ">=3.13"` "open-ended" (pyproject.toml line 6), `uv.lock` dashed "not in the
repo". Then the TEAL image stack gets a frost glyph, "frozen at build time"; caption "ship the image,
not the recipe".
SAY: Same Dockerfile, a month apart, two different Pythons. Nothing in the recipe is pinned: pip installs the latest uv, the Python range is open, and there's no uv.lock. An image freezes all of that, which is why you ship the image, not the recipe.

SHOW: Full terminal; it types `exit` (line 30) → TERM(vm-debian12/06: 31). Two README cards:
`README.md · line 205` "pull the image you pushed in step 3" and `README.md · line 215`
`sudo docker run --rm -ti dlops/simple-translate`; tag `erratum`. Below them a GREEN chip (text, not
run) `sudo docker run --rm -ti <USER NAME>/simple-translate-ac215`, `<USER NAME>` YELLOW, with a GREY
tag "needs an amd64 build: see Platforms".
SAY: Type exit. One more small mismatch: the README promises to pull the image you pushed, but this command runs the instructor's. Yours would be the same command with your user name, slash simple-translate-ac215, built for amd64.

SHOW: TRACKER C6 · extra. Strip (5 rows) types
`sudo docker run --rm dlops/simple-translate -c 'wc -c cli.py; grep -n Translator cli.py; ls -l .venv/bin/python; cat .venv/pyvenv.cfg'`
(extra; folds) → TERM(vm-debian12/10: 2–4). Line 4 `25:    async with Translator() as translator:`
sits above CODE(cli.py: 25) (the repo's `Translator(raise_exception=True)`); tag `erratum` "the
published image lags the repo".
SAY: Also, the published image lags the repo: its cli.py is the older one, without raise exception equals True. If Google refuses a request, that version quietly prints your input back as the output. That's not a Docker problem.

SHOW: A GREY card "if the pull itself fails:" with TERM(vm-debian13/06-docker-run-rate-limited: 3;
wrap) in RED, tag `real capture · Debian 13 · 2026-10-13`; two GREEN chips "wait a while" and
"docker login". Fade out.
SAY: And if the pull itself fails with too many requests: Docker Hub limits anonymous pulls per network address, which a classroom can hit. Wait a while, or log in first.

---

## S16 · Tear down, recap, and what's next — `s16_recap.py` · `Recap`

SHOW: TRACKER C6 · extra. Strip terminal types `sudo docker ps -a` (extra) →
TERM(vm-debian12/11: 2; squeeze): the header only.
SAY: Before you go, clean up. An extra docker ps dash a shows no containers left behind, thanks to dash dash rm.

SHOW: TRACKER C7. The schematic console (tag `illustration`): `ac215-l02` ticked → Delete → the
confirm dialog "Delete ac215-l02? Its boot disk is deleted with it" (as in L1). The BLUE VM dissolves;
the GOLD dial stops where it is. A checklist "VM instances: empty" · "Disks: empty" ticks GREEN.
`▶ your turn`.
SAY: Last README step: delete the VM, with its boot disk, then check that VM instances and Disks are both empty. Pause and do it now, before you forget.

SHOW: Two GREY optional chips: "Docker Hub repository: public until you delete it or make it
private" and `docker system prune -a` "frees the laptop's disk · said, not typed here".
SAY: Two optional chores. Your Docker Hub repository stays public until you delete it or make it private. And on the laptop, docker system prune dash a reclaims the space your images take.

SHOW: V1 closing picture: a BLUE VM box containing a GREEN venv box; between them a dashed GREY box
"container · L2" fades in, solidifies TEAL, and the venv slides into it with the label `/.venv`.
Then the route draws left to right: GREY laptop "build" → PINK → BLUE Docker Hub shelf "push" →
PINK → BLUE VM "run".
SAY: Here's the whole picture. Lecture 1 gave us a VM with a venv inside. Today a container slid in between: the venv now lives in an image, at slash dot venv. You built it on your laptop, pushed it to a registry, and ran it on a VM with one command.

SHOW: A card "Test yourself", questions appearing one at a time (each stays, smaller, as the next
fades in), each with a small thumbnail that plays one motion: Q1 "What is the difference between an
image and a container, and what does --rm delete?" (V2: the glass slab dissolving); Q2 "What command
line does our container run at start-up, and what happens with docker run --rm -ti simple-translate
python cli.py?" (V3: the tile knocking out CMD).
SAY: Five questions to test yourself. One: what's the difference between an image and a container, and what does dash dash rm delete? Two: what command line does our container run at startup, and what happens if you add python cli.py after the image name?

SHOW: Q3 "The Dockerfile says python:3.12. Why does python --version print 3.15 (or 3.14), and what
does /usr/local/bin/python print?" (V4: two dots); Q4 "You edit one line of cli.py. Which build
steps re-run, and how would you reorder the Dockerfile so uv sync stays cached?" (V5: dominoes);
Q5 "Name two ways to make an image built on Apple Silicon run on a default GCP VM." (V7: the menu).
SAY: Three: the Dockerfile says Python 3.12, so why does python report 3.15, or 3.14, and what does the Python in user local bin report? Four: you edit one line of cli.py; which steps rerun, and how would you reorder the Dockerfile? Five: name two ways to make a Mac-built image run on a default VM.

SHOW: The questions shrink to the top. Two footer cards: "Answers: exercises.md" and "Study guide +
every command: github.com/JunyiZhou-Conny/MLOps_Learning · guides/L02-containers-1.md". A "Next: L3 ·
Containers II" card with a GREY dashed teaser: five small TEAL boxes linked in a row, a chip
`WORKDIR /app`, a chip "non-root user", and a GREY laptop folder with a dashed arrow into a container,
"mounted". Everything fades to an empty frame (end of part 2).
SAY: The answers are in the exercises, and every command is in the study guide. Next time, Containers 2: five containers working together, a working directory, a non-root user, and your laptop's folder mounted inside a container.
