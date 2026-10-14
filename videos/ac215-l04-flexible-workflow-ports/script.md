# AC215 · Lecture 4 — Containers II-b: build or pull, ports and Compose — narration script & visual plan (v1)

Audience: an AC215 student who has done L1 (VMs, venvs, uv), L2 (a given Dockerfile, images, Docker
Hub, platforms) and L3 (the five-container mega-pipeline with the course key, bind mounts, `uv add`,
the key-in-the-image trap). Docker Desktop and git are installed (Tutorial 0); for part 1 they have a
GCP project with billing and the `gcloud` CLI logged in. They watch with two clones open,
`~/AC215/mega-pipeline` (branch `flexible-workflow`) and `~/AC215/port_toy`, pausing to type each
command. New to them: owning a service account, wrapper scripts, build-or-pull workflows, container
networks, ports and Compose.

Goal: after the video they can get the `flexible-workflow` branch by a fresh clone or by switching an
L03 clone (and get past both of `git checkout`'s refusals with `git stash -u`); set the three values
in all five `cli.py` files and say why two files would otherwise use the course's resources; create
their own service account with the four roles, put its key in `secrets/` beside the repo, enable the
five APIs, and name the three gates a call must pass (key, role, API) and where each fails; read
`docker-shell.sh` (four modes, two bind mounts, the env var, why it runs from the component folder);
run the five components and recognise the no-key, unedited-config and silent no-op outcomes; explain
build vs pull, why `run` can hand them a February-2025 Python 3.8 image, and keep an old key out of
their images; explain container networks and ports with port_toy (own `localhost` per container,
names on a user-defined network, published vs listening vs source ports, `-p ip:host:container`),
change a host port and a container port and fix the mismatch with configuration only; run the same
app with Compose, read `docker-compose.yml` as the by-hand commands written down, and know what
`Ctrl+C`, `down`, `up -d` and `up -d --build` each do.

Sources of truth: `BRIEF.md` (design, binding), `digest.md` (tutorial digest), `assets/` (see
`ASSETS.md`). Where the digest and the captures disagree, the captures win (BRIEF.md's table).
Nothing in a terminal panel is typed by hand: every output line below names its capture file and
line numbers. v1, before the four review lenses.

Conventions
- `SAY:` lines are spoken verbatim by the TTS voice (one `voiceover` block each, 1–3 sentences, at
  most about 60 words) and become the subtitles. Plain spoken English: no backticks, no symbols;
  commands and paths are on screen and described in words ("dash p", "slash app", "dash dash
  build"). File names with a lexicon entry (cli.py, pyproject.toml, uv.lock, docker-shell.sh) are
  said as words; folder names are said with spaces ("transcribe audio", "text prompts", "port
  toy"). Numbers as digits, port numbers too (9200, 8090); never a "!" after a digit. Versions that
  will change are said with "at the time of recording" (Docker Engine 29.8.2, Python 3.14.8).
- Every spoken sentence starts with a capital letter or a digit (`explainer.voice.split_sentences`
  splits only there; the split drives the TTS gaps, the subtitle cues and the Chinese alignment).
  No sentence opens with a command or a lower-case file name. No `'s` on a word with a lexicon
  entry (`uv's` and `README's` exist and are used). A component letter is never a bare sentence
  subject (Kokoro reads a lone "A" as "uh"): the SAY names components by folder ("transcribe
  audio"). No bare "a" right before a lexicon word ("its cli.py"). Sentences stay under 30 words.
- `SHOW:` lines describe what is on screen during that `SAY:` line, and what moves.
- `PONDER(n s, "question")`: after that SAY block, `pause_and_ponder(self, "question", seconds=n)`
  (silent timer); the card is removed at the start of the next block, whose SAY gives the answer.
  Five in the video (S05, S07, S08, S13, S14), as in BRIEF.md. The picture on screen during the
  timer never shows the answer.
- `TERM(folder/file: lines)`: a terminal beat. The scene types the command written just before it
  in the SHOW line (in backticks, exactly as the README spells it; extras exactly as captured), then
  prints those lines of `assets/terminal/folder/file`. Line 1 of every capture is its `$ …` command
  and is never printed; the `[exit N]` line is never printed. In the line list: `…` = print one `…`
  line; `wrap` = fold long lines (`Terminal.print(..., wrap=True)`); without `wrap`, a line longer
  than a row is cut with `…`. `session` = an interactive capture whose lines include prompts
  (`mega-laptop/12`, `18`, `31`, `40`, `51`, `61`, `72`, `76`, `gcloud-laptop/01`, `port-laptop/29b`,
  `56d`): a listed line that starts with a prompt is not printed; the scene sets that prompt and
  types the command after it. `→ (no output)`: the prompt simply returns.
- Long prompts. `student@laptop:~/AC215/mega-pipeline/transcribe_audio$` is 54 characters, so
  `./docker-shell.sh` does not fit after it in a 65-character row. A command is never broken inside
  a word: when prompt + command is longer than a row and the command has no space early enough,
  the command starts on the row under the prompt, indented 4 spaces (common.py helper; the fold
  rule of `Terminal.type` otherwise). Rows counted below include these.
- Multi-line README commands (`docker run … \`, `gcloud services enable \`) are typed row by row
  exactly as the README writes them, each row but the last ending in ` \`, continuation rows
  indented two spaces, as in the capture's own `$` lines.
- Captures whose `$` line joins commands with `;` are typed as separate commands, each followed by
  its own lines of the file (as L03 did); commands of that line that are not shown are not typed.
- BuildKit live-view rows (the terminal renders `mega-laptop/12`, `17`, `31`, `40`, `51`, `61`,
  `mega-l03-laptop/12`, `port-laptop/07`, `08`, `47`, `62`) are 79 characters, so they print cut at
  65 without their time: the row's last field (`line.split()[-1]`, e.g. `44.7s`) becomes a small
  GREY tag at the row's end, and that tag is what highlights. The line lists below never include
  `=> =>` sub-lines except `naming to …`, nor `[1/5] FROM` / `[1/4] FROM`, `load metadata`,
  `load .dockerignore`, `load build context` or `transferring` lines (their digests are the
  capture's rebuilt base). BuildKit's `[k/5]` steps are always *build step k* in the SAY and get a
  TEAL badge (`step_badge(..., color=TEAL)`); *step k* alone is always the README tracker's step.
- Full logs. `*.plain.txt` are step-by-step logs replayed after the build. Shown as a PANEL headed
  "the same build, full log"; the SAY never presents a plain-log line as what the viewer's terminal
  printed.
- Wide tables. `docker ps`, `docker compose ps` (98–130 characters) print with `wrap` and the
  `PORTS` cell highlighted. `docker images` / `docker image ls` (68–94 characters) print as a
  *column view*: each line keeps only its IMAGE and DISK USAGE fields (the capture's own text,
  sliced, not retyped), header "docker images · IMAGE and DISK USAGE".
- Terminal width. Every terminal is the house `term()` (12.6 wide, 22 pt, 65 characters a row),
  always full width. When a picture needs the frame, the terminal shrinks to a 3-row strip along
  the bottom edge (the last command and its key output line). Never half width; a second panel
  goes above the strip, never beside a full-width terminal.
- Terminal titles: `laptop` (and `laptop · second terminal` for a second one); `laptop · lecture 3
  clone` in `~/AC215-l03`; inside a container `container · transcribe_audio` (or the component's
  folder, or `container · gateway`), and the terminal's frame turns TEAL there.
- `CODE(path: a–b)`: `code_panel(...)` quoting `assets/source/path` from line a to b; the header is
  the path as it is in the viewer's clone, without the first folder (`transcribe_audio/docker-shell.sh
  · lines 6–14`, `gateway/gateway.py · lines 32–38`); files from other branches carry the branch
  (`main · README.md · line 97`, `pipenv-flexible-workflow · transcribe_audio/Dockerfile · line 2`).
  Never more than 12 lines on screen. A quoted line longer than 65 characters is cut at its
  trailing comment, shown as `# …`, header suffix "· comment cut" (`excerpt(..., cut_comments=True)`).
  `PANEL(capture: lines, "header")`: the same look for lines from `assets/terminal/` (a full log, an
  `expected/` block, a single line); an *excerpt chip* is a mono chip holding the exact
  sub-string of one capture line, headed `file · line N (excerpt)`.
- README cards. While a terminal of 10 or more rows is up, a README card is a one-line chip in the
  top band, right of the tracker: `README.md · line N` + the quoted phrase. A multi-line README card
  appears only above a 3-row strip, or with no terminal.
- "With your key, look for" cards (Google calls that could not be recorded): a GREY caption card,
  one short line per item, each citing the `cli.py` line that prints or writes it; items write in
  when the SAY names them. Never styled as terminal output, never in a terminal frame.
- The bind mount is one folder seen from two sides: nothing travels along a PINK mount route; an
  edit on either side blinks on both sides at once, and the route only pulses.
- The key is always a GOLD key glyph labelled `mega-pipeline.json`; its content is never drawn and
  the 79-byte stand-in (`mega-l03-laptop`) is never `cat`-ed. Docker Hub placeholders stay
  `<USER NAME>` / `<ACCESS TOKEN>`; project and bucket appear only as `your-project-id` /
  `your-team-bucket`, except inside the quoted capture lines the viewer must find and edit.
- The port_toy page. The browser is the README step; the capture's `curl` stand-in is never typed.
  `PAGE(port-laptop/NN)`: a schematic browser window (tag `illustration`), address bar
  `localhost:<port>`, input "hello from the laptop" (what the capture sent), a Send button, the card
  "Processor's reply" with the `upper` value, the port card (three lines, each label padded to 30
  characters as `index.html:84` does: "gateway sent from port", "processor listening on port",
  "processor saw it arrive from") and the page's diagram, all filled from that capture's JSON.
  `REPLY(port-laptop/NN: line)`: that line in a small GREY strip under the page, tag "captured
  reply · curl stood in for the Send button".
- `TRACKER K/3` = the `ReadmeTracker`, top-left in every walkthrough scene, moves to section K,
  step 3; `TRACKER K/3 · extra`: same step, caption gets " · extra" while a command the README
  doesn't have is on screen; `TRACKER QD/1→4` = the dots tick one per typed command. Caption
  "README › section › step k of N" (part 2: "port_toy README › …"). Step titles ≤ 3 words.
  Part 1, mega-pipeline `README.md` (`flexible-workflow`):
  - `F` = "Get the Code · starting fresh" (`:32-37`), 2: 1 Clone branch · 2 cd.
  - `L` = "Get the Code · already have the repo" (`:39-48`), 5: 1 cd · 2 Fetch · 3 Checkout ·
    4 Stash, retry · 5 Confirm branch.
  - `B` = "Before you run" (`:105-158`: layout, Configure each cli.py, GCS Bucket Details), 3:
    1 Secrets folder · 2 Set cli.py · 3 Your bucket.
  - `K` = "Service Account & Secrets" (`:169-203`), 6: 1 Create account · 2 Grant roles · 3 JSON key ·
    4 Save key · 5 Set project · 6 Enable APIs.
  - `R` = "How to Run a Component" (`:207-226`), 6: 1 Build and run · 2 dev · 3 run · 4 prod ·
    5 chmod +x · 6 winpty.
  - Quick Reference (`:230-274` with each component README's `--help`), section = component folder:
    `QA` = "transcribe_audio", 4: 1 Check --help · 2 Download · 3 Transcribe · 4 Upload;
    `QB` = "generate_text", 5: 1 Check --help · 2 Download · 3 Generate · 4 Upload · 5 Other model
    (`generate_text/README.md:91-94`); `QC` = "synthesis_audio_en", 3: 1 Check --help ·
    2 Download · 3 Synthesize; `QD` = "translate_text", 4: 1 Check --help · 2 Download ·
    3 Translate · 4 Upload; `QE` = "synthesis_audio", 3: 1 Check --help · 2 Download · 3 Synthesize.
  - `Y` = "Python packages" (`transcribe_audio/README.md:89`), 1: 1 Add a package.
  - `U` = "Publish the container" (`transcribe_audio/README.md:124-132`), 2: 1 docker login · 2 prod.
  Part 2, port_toy `README.md`:
  - `P0` = "Prerequisites" (`:20-30`), 1: 1 Check Docker.
  - `P1` = "Step 1: Set up the network by hand" (`:75-183`), 7: 1 Get the code · 2 Create network ·
    3 Build images · 4 Start processor · 5 Start gateway · 6 Check logs · 7 Send a message.
  - `P2` = "Step 2: Check the ports" (`:189-325`), 3: 1 Read PORTS · 2 From the laptop ·
    3 From the gateway.
  - `P3` = "Step 3: Change the ports" (`:331-420`), 4: 1 Host port · 2 Processor port ·
    3 Update gateway · 4 Clean up.
  - `P4` = "Step 4: Run with Compose" (`:426-529`), 5: 1 Start the app · 2 Compare commands ·
    3 Apply changes · 4 Rebuild · 5 Stop and remove.
  - `PH` = "Handy commands" (`:557-576`), 5: 1 Shell inside · 2 Follow logs · 3 Compose shell ·
    4 List networks · 5 Inspect network.
  Ordering (said in a clause where it happens, BRIEF.md "Ordering notes"): `R` runs 1, 5, 6 in S06,
  2–3 in S08, 4 in S09; the Compose "Stop and remove" (`P4/5`) closes the foreground `up` in S15 and
  again the background app in S16; handy commands appear where they are useful (S10, S13, S16).
- `(extra)` after a command: not in the README. A small GREY tag `extra` sits beside the typed line,
  and the SAY says so ("an extra check", "not in the README") at least the first time. A command
  the README implies but doesn't print (`cd transcribe_audio`, `cd ../generate_text`, `git clone
  https://github.com/dlops-io/port_toy.git`) gets a GREY caption citing the README line instead.
- `▶ your turn`: a YELLOW tag beside the command at a real checkpoint (about one per README step);
  the SAY of that block says "pause". The video doesn't wait: the viewer pauses. A `▶` never sits
  on a frame that can't be read when paused: montages end on a static GREY card listing what was
  typed.
- Tags (GREY unless stated): `extra`; `illustration` on every schematic (console screens, the
  bucket, Docker Hub, the port_toy page, "what if" pictures); `expected` on panels from
  `assets/terminal/expected/`; `recorded without a key` on the real runs that fail for lack of a key;
  `at the time of recording` next to Docker Engine 29.8.2, Python 3.14.8, uv 0.13.0; `stand-in file
  · not a real key` (S03, S09); `erratum` on every README slip (the SAY says "a small slip" or "a
  small gap", always with the fix); `your numbers will differ` on ephemeral ports and container ids;
  GOLD cost tags ("your project pays") on the bucket, the APIs, the key and each Google call.
- Spelling on screen and in the SAY: American ("gray" in narration; the colour constant stays GREY).
- Semantic colours (series table applied, BRIEF.md):

  | meaning | colour |
  | --- | --- |
  | your laptop: the workspace `~/AC215`, the clones, component folders, `secrets/` beside the repo, the files a bind mount shows inside; the browser and the published (host-side) port doors | GREY |
  | Google Cloud: your project, the bucket and its drawers, the five APIs, IAM and the service account; Docker Hub (a registry shelf) | BLUE |
  | containers and images: the five component images, `gateway` and `processor` boxes, layer stacks, container-side listening doors (`:9100`, `:9200`), the `toynet` rail | TEAL |
  | system parts inside an image: the Debian base, the apt layer (`build-essential`, `ffmpeg`, `curl`), the base image's Python 3.14.8 | ORANGE |
  | project-owned and committed: the recipe card (`Dockerfile` + `pyproject.toml` + `uv.lock`), tracked files at a branch switch, `/home/app/.venv`, `docker-compose.yml` | GREEN |
  | tools: docker, buildx, Compose, git, gcloud, uv; `docker-shell.sh` itself | PURPLE |
  | errors and "avoid this": checkout refusals, `DefaultCredentialsError`, `AssertionError`, the stale `dlops/*` image, the key inside an image, `Could not connect`, `Connection refused`, `Empty reply`, `port is already allocated`, `Conflict` | RED |
  | your turn, the README tracker, "look here now" | YELLOW |
  | money: cost tags on API calls and the bucket; the key glyph (whoever holds it spends your project's money) | GOLD |
  | lookups and routes: the bind-mount routes, the `GOOGLE_APPLICATION_CREDENTIALS` signpost, the tag signpost, the `run` decision diamond, the DNS phone book, packets, `-p` mapping arrows, the ephemeral-port ticket | PINK |
  | a future thing (L05: a CLI container calling ChromaDB by name) | GREY, dashed |

  Untracked files at a branch switch are GREY, ignored files GREY dashed. A gate (S05) is BLUE; it
  shows a white tick when open and turns RED when it refuses.
- Visual set pieces V1–V8 are specified in BRIEF.md ("Visual set pieces"); SHOW lines say which one,
  its state, and what moves.
- Running example (BRIEF.md): user `student`, host `laptop`, workspace `~/AC215` (the README's
  `<your-workspace>`): prompts `student@laptop:~/AC215$`, `student@laptop:~/AC215/mega-pipeline$`,
  `student@laptop:~/AC215/mega-pipeline/transcribe_audio$` (and the other four folders),
  `student@laptop:~/AC215/port_toy$`; the L03 clone in `student@laptop:~/AC215-l03/mega-pipeline$`;
  the gcloud terminal `student@laptop:~$`. Container prompts from the captures: `app@0ceffb272288:/app$`
  (transcribe_audio), `app@45263bb6ca36:/app$` (generate_text), `app@ba0b1df0eadc:/app$`
  (synthesis_audio_en), `app@40d7497c50f2:/app$` (translate_text), `app@6172f2cd7728:/app$`
  (synthesis_audio), `app@631fac50f92b:/app$` (S08 `run`), `(app) root@36615ab6e34b:/app#` (the stale
  image), `#` (`sh` in the gateway). Values `your-project-id`, `your-team-bucket`, `group-01` (the
  captures' placeholders; the SAY says "type your own"). port_toy: gateway on host port 8090 (then
  8095), processor 9200 (then 9300); ephemeral ports 55620, 55634, … ("your numbers will differ").
- Length and parts: see the end of this header block (filled from `python -m explainer.script`).
- Notes for scene authors.
  - `Capture.pick()` indexes the output body: pick index = file line − 1.
  - `expected/mega-*.txt`: line 1 is a `#` source header (never printed), line 2 the `$` command,
    output from line 3. `expected/port_toy-*.txt`: line 1 header, output from line 2.
  - `gcloud-laptop/01`: line 1 is a stage note (never shown); line 2 is prompt + command (typed,
    `session`); lines 4–5 (`exit`, `logout`) are never shown.
  - `mega-laptop/72` lines 22–23 and `76` lines 17–18 are pipenv typing `source …/activate` into its
    own subshell: never typed by the scene; the line lists leave them out.
  - The `mega-<component>/` files ran through `docker exec` and have no prompt: draw the prompt of
    that component's session (Running example) and type the `$` command there.
  - `port-laptop/24` lines 2–4 are curl's progress meter (stderr, no terminal given): S01 replaces
    them with `…`; S13 prints them with a GREY tag "curl's progress meter".
  - Terminal renders wrapped long lines at 80 columns (a line that ends mid-word and continues on the
    next): join such pairs before printing with `wrap` (`mega-laptop/51` and `61` traceback lines,
    e.g. `51` 64–65 and `61` 93–94; `72` 22–23; `76` 17–18; `port-laptop/25` 5–6; `port-laptop/68`
    8–11). Line numbers in this script still name the file's own lines.
  - The browser stand-ins `port-laptop/14`, `15`, `32`, `38`, `43`, `49`, `56c`, `59` are never
    typed (PAGE / REPLY only). `port-laptop/57` and `61` and `mega-laptop/11`, `30`, `41` show edits
    made by a capture-only `sed`: the scene first draws a pencil editing the file (GREY "in your
    editor"), then types the extra `git diff`.
  - The instructor's group name appears only inside unchanged capture lines the viewer must find and
    edit (`mega-laptop/07`, `11`, `41`); the course's project and bucket names likewise. Captions and
    narration say "the course's project and bucket" and "the instructor's group name".
  - `port-laptop/47` is the foreground `docker compose up`: lines 52–54 (the request log lines)
    appear only after the S15 second-terminal beats; lines 55–61 after the Ctrl+C keystroke.
  - Never shown: `--network host`, `proxy_relay.py`, `mirror.gcr.io`, the CA variables, the rebuilt
    bases' digests, apt's `https://` lines, gcloud's `[component_manager]` / `disable_usage_reporting`
    lines, the PNGs of either repo.

---

## S01 · Build or pull? Whose localhost? — `s01_hook.py` · `Hook`

SHOW: Black frame, no tracker. A terminal (12.6 wide, 15 rows, title `laptop`, prompt
`student@laptop:~/AC215/mega-pipeline/generate_text$`) fades in center. It types
`./docker-shell.sh run` (on the row under the long prompt) → TERM(mega-laptop/76-run-registry-b.txt:
2–5, …, 15–16, 19–25; session, wrap) (the first rows scroll away; nothing the next beat needs). Line 4
`Local image not found, using image from registry...` highlights YELLOW as it prints; line 20
`Python 3.8.17` YELLOW; line 25 `ImportError: cannot import name 'genai' from 'google' …` prints RED.
A small GREY tag at the top right: "no local image of generate_text".
SAY: Here's a command from this lecture's README, on a laptop that never built this image. With no local image, it pulls one from Docker Hub. Inside, Python says 3.8.17, and the first import fails.

SHOW: The terminal shrinks to a 3-row strip (lines 20 and 25 stay). Above it, V1 teaser: at left a
GREEN recipe card holding CODE(mega-pipeline/generate_text/Dockerfile: 2) `FROM
python:3.14-slim-bookworm` (header `generate_text/Dockerfile · line 2`); at right a BLUE shelf "Docker
Hub" (tag `illustration`) with a sealed TEAL box, a PINK signpost `dlops/mega-pipeline-generate-text:latest`
pointing at the box, and a small GREY date chip "pushed 2025-02-18" (registry metadata, digest E1). A
YELLOW "?" pulses between card and box.
SAY: Yet this repo's Dockerfile says Python 3.14. The image we just ran was built in February 2025, with Python 3.8. Where did it come from?

SHOW: Cut. A new terminal (12.6 wide, 6 rows, title `laptop`, prompt `student@laptop:~/AC215/port_toy$`)
along the bottom. Above it, two TEAL boxes `gateway` and `processor` (the processor with a small
door `:9200`) and a GREY laptop glyph at left. It types `curl --max-time 3
http://localhost:9200/health` → TERM(port-laptop/23-curl-9200.txt: 2) RED; at the same time a dashed
PINK arrow from the laptop to the `:9200` door bounces back RED. Then it types `docker exec gateway
curl http://processor:9200/health` → TERM(port-laptop/24-exec-processor.txt: …, 5) (the progress
meter replaced by `…`); `ok` highlights GREEN, and a PINK arrow from `gateway` to `processor`
labelled "processor" lands GREEN.
SAY: A second surprise, from the other tutorial: a server listening on port 9200. The laptop can't connect to it. Another container, asking for it by name, gets the answer ok.

SHOW: Both pictures shrink to thumbnails, left (signpost and box) and right (the two boxes). Under
them two YELLOW questions write in, one per thumbnail: "Part 1 · Where did that image come from?"
and "Part 2 · Whose localhost is it?".
SAY: Two puzzles. Part 1: where did that image come from, and should you build or pull? Part 2: whose localhost is it?

SHOW: The questions clear. A layout preview, built piece by piece as named: the ReadmeTracker appears
top-left ("README › Get the Code · starting fresh", 2 dots) with a YELLOW circle pulsing around it; a
code panel slides in with header `transcribe_audio/docker-shell.sh · lines 7–8`
(CODE(mega-pipeline/transcribe_audio/docker-shell.sh: 7–8)); a two-line terminal strip at the bottom
(GREY tag "preview") shows `git clone --branch flexible-workflow
https://github.com/dlops-io/mega-pipeline.git` with a YELLOW `▶ your turn` tag, then `git branch;
git log --oneline -1` with the GREY `extra` tag.
SAY: Follow along with the README open. The tracker, top left, shows the README step; code panels show file and line numbers. Pause at the yellow your-turn tag; gray extra tags mark commands the README doesn't have.

SHOW: The preview clears. A checklist card ticks line by line: "every command: MLOps_Learning ·
guides/L04-containers-2b-flexible-workflow-ports.md" (GREY) · "part 1: Tutorial 0 + a Google Cloud
project with billing · gcloud logged in" (GREEN check, small GOLD coin glyph) · "part 2: only Docker" (GREEN check).
SAY: Every command is also in the study guide, in the MLOps Learning repo. Part 1 needs Tutorial 0 and a Google Cloud project with billing; part 2 needs only Docker.

SHOW: A small GREY card: "recorded 14 October 2026 · Linux laptop" over PANEL(port-laptop/00-env.txt:
4–5, "docker version · docker compose version") with the tag `at the time of recording`. Beside it two
small GREY chips: "macOS: zsh, %" and "Windows: Git BASH" (each with a tiny prompt glyph).
SAY: We recorded on a Linux laptop, with Docker Engine 29.8.2 at the time of recording. On a Mac or in Git BASH the prompt differs; the commands, ports and errors don't.

SHOW: A dashed BLUE cloud with a GREY cross: "no Google account · no key in this recording". Under it
three GREY chips write in as named: "the command" · "the real no-key error" · "with your key, look
for". Everything fades to an empty frame.
SAY: And one honest limit: we had no Google account. Wherever the code calls Google, you'll see the command, the real error a missing key gives, and what to look for.

---

## S02 · Same pipeline, built like a team — `s02_team.py` · `TeamWorkflow`

SHOW: No tracker (concept scene). A GREY README card, header `README.md · lines 58–60`, with "the
same pipeline, built the way a real team would build it" highlighted, condenses into a two-column
card with headers "L03" (GREY) and "L04" (YELLOW). Row 1: "a shared bucket" (a BLUE drawer labelled
"course") morphs into "your own bucket" (a BLUE drawer labelled "your team"). Row 2: "one shared key,
copied into five folders" (five GREY folders, each holding a small GOLD key; chip `main · README.md ·
line 97`) morphs into "your own service account · one key outside the repo" (one GOLD key outside a
GREY repo outline).
SAY: In lecture 3, the course handed you a shared bucket and one shared key, copied into every component folder. This branch is the same pipeline, built the way a real team would build it.

SHOW: Rows 1–2 settle (README chip `README.md · lines 62–63` under them). Row 1's right cell pulses
BLUE; row 2's GOLD key slides a little further outside the repo outline.
SAY: Your team owns its bucket. You create your own service account, and keep its one key outside the repo.

SHOW: Row 3: "you wrote each Dockerfile" (a pencil) morphs into a GREEN recipe card "Dockerfile ·
pyproject.toml · uv.lock · committed". Row 4: "docker run … typed from memory" (a long GREY command
chip) morphs into a PURPLE script chip `docker-shell.sh`. README chip `README.md · lines 64–65`.
SAY: You no longer write the Dockerfile: it's committed, together with pyproject.toml and uv.lock. And the long docker build and docker run commands live in one script per component, docker-shell.sh.

SHOW: The card clears. L03's V1 in miniature (tag "from lecture 3"): five TEAL boxes in a row over a
BLUE cabinet of drawers; a small token hops box → drawer → next box. A GREY README card, header
`README.md · lines 140–142`: "components will communicate indirectly by writing their outputs to
storage". A dashed GREY arrow between two boxes gets a small GREY tag "part 2".
SAY: The five stages haven't changed, and they still never call each other. Each writes its output to the bucket, and the next one reads it there. Containers that talk directly come in part 2.

SHOW: V1 in full (the miniature fades). A GREY README card, header `README.md · lines 67–72`, "Two
ways to work — and we support both". Left: a GREY shelf "Git" with the GREEN recipe card
(`Dockerfile`, `pyproject.toml`, `uv.lock`); a PURPLE arrow `docker build` turns a copy of the card
into a TEAL image box labelled `Python 3.14.8 · uv` on a GREY laptop. Right: a BLUE shelf "Docker
Hub" (tag `illustration`) with a sealed TEAL box. Phase 1, caption "early in development": three
GREY teammate glyphs each draw a PURPLE build arrow from the card. Phase 2, caption "later in
development": one teammate pushes a box up onto the BLUE shelf; the other two draw BLUE pull arrows
down from it.
SAY: Once an image exists, a team can get it two ways. Early in a project, everyone builds it from the recipe in Git. Later, one person publishes finished images to Docker Hub, and everyone else pulls.

SHOW: Zoom on the BLUE shelf: a PINK signpost `dlops/mega-pipeline-transcribe-audio:latest` stands
beside the box, its arrow pointing at the box, not at the recipe card. A dashed GREY line runs from
the card to the box with a GREY "?" and the caption "built on some day, from some commit".
SAY: Look closely at the tag. It's a signpost to one particular image, built on some day, from some version of the recipe. Nothing promises it matches the commit you have.

SHOW: The two halves slide toward the center; between them a PURPLE switchboard silhouette (one
input, four tracks, no labels yet) captioned `docker-shell.sh`. Fade out.
SAY: One script decides which of the two you get, and we'll read it line by line. First, the code.

---

## S03 · Get the code: clone, or switch branches — `s03_code.py` · `GetTheCode`

SHOW: TRACKER F/1 (the tracker appears, mega-pipeline README). Terminal (full width, 12 rows, title
`laptop`, prompt `student@laptop:~/AC215$`); a GREY note under the tracker: "~/AC215 = the README's
<your-workspace>". It types `git clone --branch flexible-workflow
https://github.com/dlops-io/mega-pipeline.git` (folds) → TERM(mega-laptop/01-clone.txt: 2);
`--branch flexible-workflow` gets a GREY label "this tutorial's branch". TRACKER F/2. It types `cd
mega-pipeline` → (no output); the prompt becomes `student@laptop:~/AC215/mega-pipeline$`, the new part
flashing BLUE. `▶ your turn`.
SAY: Starting fresh? From your workspace folder, clone just this branch: git clone, dash dash branch flexible-workflow, and the address. Then cd into mega-pipeline. Pause and run both.

SHOW: TRACKER F/2 · extra. It types `git branch; git log --oneline -1` (extra) →
TERM(mega-laptop/03-x-branch.txt: 2–3); `cc67f3b` gets a GREY tag "the pinned commit · 2026-09-18".
The terminal clears; it types `ls -a transcribe_audio` (extra; the second command of
`mega-laptop/04-x-ls.txt`) → TERM(mega-laptop/04-x-ls.txt: 10–18). `Dockerfile`, `docker-shell.sh`,
`pyproject.toml`, `uv.lock` highlight GREEN one by one, and a small GREEN recipe card "committed"
gathers them.
SAY: Two extra checks: git branch shows flexible-workflow, at the commit this video pins, and transcribe audio now holds its Dockerfile, the script, pyproject.toml and uv.lock. In lecture 3, you wrote those.

SHOW: TRACKER L/1. The terminal clears; title `laptop · lecture 3 clone`, prompt
`student@laptop:~/AC215-l03$`. It types `cd mega-pipeline` → (no output); prompt
`student@laptop:~/AC215-l03/mega-pipeline$`. TRACKER L/1 · extra. It types `git status --short`
(extra) → TERM(mega-l03-laptop/01-x-l03-state.txt: 2–4), then `git status --short --ignored | grep
'^!!'` (extra) → TERM(mega-l03-laptop/01-x-l03-state.txt: 5–8).
SAY: Already have lecture 3's clone? Then you're on main. Step 1: cd into it. Two extra status checks show a typical lecture 3 state.

SHOW: The terminal shrinks to the bottom strip. Above it, V2 builds from those lines: three piles.
Tracked (GREEN): `transcribe_audio/cli.py` with a YELLOW pencil "edited". Untracked (GREY):
`generate_text/Dockerfile`, `generate_text/uv.lock`. Ignored (GREY dashed): `transcribe_audio/Dockerfile`,
`transcribe_audio/pyproject.toml`, `transcribe_audio/uv.lock`, and a `secrets/` folder holding the
GOLD key glyph (tag `stand-in file · not a real key`).
SAY: Three piles. Your edited cli.py is tracked. Two files you added in generate text are untracked. And transcribe audio's Dockerfile, pyproject.toml, uv.lock and the key are ignored: Git acts as if they aren't there.

SHOW: TRACKER L/2. A one-line README chip in the top band: `README.md · line 43` "# get the branches
you don't have yet". The strip types `git fetch origin` → (no output); a GREY tag "nothing to fetch".
SAY: Step 2, git fetch origin. The README says it gets the branches you don't have yet; here it prints nothing, because a clone already has every branch.

SHOW: TRACKER L/3. The terminal grows to 10 rows (V2 shrinks above it). It types `git checkout
flexible-workflow` → TERM(mega-l03-laptop/04-checkout.txt: 2–9). Lines 2–4 get a RED bracket "1",
lines 5–8 a RED bracket "2", `Aborting` underlines RED. In V2, the branch's files slide down from
above and stop at two RED walls: one in front of the edited `cli.py`, one in front of the
untracked pair.
SAY: Step 3, git checkout flexible-workflow, and Git refuses twice. Your edits to cli.py would be overwritten, and two untracked files sit where the branch has files of its own. Nothing changed.

SHOW: TRACKER L/4. The terminal clears to 8 rows. A one-line README chip: `README.md · line 48`
"Either stash them (git stash) or throw them away (git checkout -- .)". It types `git stash` →
TERM(mega-l03-laptop/05-stash.txt: 2) (cut). In V2 the edited `cli.py` lifts into a small box
"stash"; wall 1 falls. It types `git checkout flexible-workflow` → TERM(mega-l03-laptop/06-checkout-after-stash.txt:
2–6); wall 2 flashes RED and stays.
SAY: The README's note covers the first refusal: git stash puts your edits away, and the first wall falls. Retry the checkout, and the untracked files still block it.

SHOW: TRACKER L/4 · extra. The README chip gets the tag `erratum` ("covers only edited files"). It
types `git stash -u` (extra) → TERM(mega-l03-laptop/07-x-stash-u.txt: 2) (cut). In V2 the untracked
pair lifts into a second stash box; wall 2 falls. It types `git checkout flexible-workflow` →
TERM(mega-l03-laptop/08-checkout-ok.txt: 2–3); line 3 highlights GREEN and the branch's files land.
Above the terminal, a GREY chip `git checkout -- .` (shown, never typed) with two notes: RED
"throws your edits away" and GREY "leaves untracked files where they are".
SAY: A small gap: the note covers only edited files. The extra command git stash dash u stashes untracked files too, and now the checkout works. The README's other option, git checkout dash dash dot, discards your edits and leaves untracked files alone.

SHOW: TRACKER L/5. It types `git branch` → TERM(mega-l03-laptop/09-branch.txt: 2–3); `*
flexible-workflow` highlights GREEN. `▶ your turn`.
SAY: Step 5, git branch: star, flexible-workflow. Pause and switch your own clone.

SHOW: TRACKER L/5 · extra. The terminal shrinks to the strip; V2 returns above it. The strip types
`head -2 transcribe_audio/Dockerfile` (extra) → TERM(mega-l03-laptop/11-x-dockerfile-replaced.txt:
2–3). In V2's ignored pile the Dockerfile card flips from `FROM python:3.12-slim-bookworm`
(mega-l03-laptop/01-x-l03-state.txt line 9) to `FROM python:3.14-slim-bookworm` (line 3 of 11), with a
GREY tag "replaced · no warning" and the tag `erratum`; a GREY fix chip: "want your lecture 3
Dockerfile? copy it out before switching".
SAY: Three extra checks reveal what happened quietly. Your ignored lecture 3 Dockerfile was replaced by the branch's, without a word: copy it out first if you want it.

SHOW: The strip types `ls transcribe_audio/secrets` (extra) → TERM(mega-l03-laptop/11-x-dockerfile-replaced.txt:
4); the GOLD key in V2 pulses and stays put. A one-line README chip: `README.md · line 50` "Your
secrets/ folder … stay put". Then `git stash list` (extra) → TERM(mega-l03-laptop/10-x-after.txt:
21–22) (cut); the two stash boxes in V2 get the labels `stash@{0}`, `stash@{1}`. Fade out.
SAY: The old key still sits inside transcribe audio. The README says your secrets stay put; true, and it matters at the end of part 1. Your edits wait in the stash list.

---

## S04 · Your bucket and your three values — `s04_values.py` · `YourValues`

SHOW: TRACKER B/1. Upper half: a file tree from README.md:107–117 (header `README.md · lines
107–117`): `<your-workspace>/` → `mega-pipeline/` (GREY, five component folders) and `secrets/` →
`mega-pipeline.json` (the file row dashed). `secrets/` gets a GREY caption "outside the repo ·
mounted at runtime". Lower half: a terminal (7 rows, title `laptop`, prompt `student@laptop:~/AC215$`).
It types `mkdir secrets` (extra) → (no output), `ls` (extra) → TERM(mega-laptop/06-x-secrets-folder.txt:
2–3), `ls -la secrets` (extra) → TERM(mega-laptop/06-x-secrets-folder.txt: 4–6). The tree's
`secrets/` gets a GREEN check; its `mega-pipeline.json` row stays dashed with a small tag "S05".
SAY: Before you run, the README's folder layout. Your key will live in a secrets folder beside the repo, never inside it. Three extra commands create that folder in your workspace; it stays empty until the next scene.

SHOW: TRACKER B/2. The tree fades. CODE(mega-pipeline/README.md: 128–130) at the top (header
`README.md · lines 128–130`): `gcp_project`, `bucket_name`, `group_name` each get a small label
"project ID", "bucket", "group name".
SAY: Step 2: near the top of every cli.py sit three values: your project ID, your bucket, and your group name.

SHOW: TRACKER B/2 · extra. Terminal (full width, 12 rows, title `laptop`, prompt
`student@laptop:~/AC215/mega-pipeline$`). It types `grep -n -E '^(gcp_project|bucket_name|group_name)
*=' */cli.py` (extra; folds) → TERM(mega-laptop/07-x-cli-values.txt: 2–4, …, 11–16) (cut). Then the
terminal shrinks to the strip and its lines lift into a grid card above (from lines 2–16 of the
same file): five rows (`generate_text`, `synthesis_audio`, `synthesis_audio_en`, `transcribe_audio`,
`translate_text`) × three columns. Three rows hold GREY `""`; the `generate_text` and `translate_text`
rows hold RED-outlined cells labelled "course's project", "course's bucket", "instructor's group"
(the values themselves stay only in the terminal lines).
SAY: An extra grep shows what ships. Three files are blank. Generate text and translate text already hold the course's project and bucket, and the instructor's group name.

SHOW: The grid stays small at the top. A one-line README chip: `README.md · line 134` "if you
forget, the script stops before doing anything", tag `erratum`. CODE(mega-pipeline/generate_text/cli.py:
21) (header `generate_text/cli.py · line 21`): line 21 `assert group_name != "", "Update group
name"` highlights; a GREEN tick lands on the RED-outlined row ("not empty → passes"). From that row
a PINK arrow runs to a BLUE cloud "course project · not yours" and bounces RED.
SAY: A small slip: the README says an assert stops you if you forget. It only rejects an empty value, so in those two files your calls would go to resources you can't use.

SHOW: TRACKER B/2 · extra. The terminal returns (full width, 10 rows; prompt
`student@laptop:~/AC215/mega-pipeline/transcribe_audio$`). A pencil edits `cli.py` in a small editor
panel (GREY "in your editor"), then it types `git diff cli.py` (extra) →
TERM(mega-laptop/11-a-x-edit-cli.txt: 10–17): the `-` lines RED, the `+` lines GREEN;
`your-project-id`, `your-team-bucket` and `group-01` get YELLOW tags "type your own". A GREY chip
"all five folders". `▶ your turn`.
SAY: So set all three values in all five files. Our edit, in an extra git diff, uses the placeholders your-project-id, your-team-bucket and group-01; type your own. Pause and edit all five.

SHOW: TRACKER B/3. The terminal fades. A BLUE cabinet (tag `illustration`) with seven drawers,
labelled as in README.md:152–158: `input_audios/`, `text_prompts/`, `text_paragraphs/`,
`text_translated/`, `text_audios/`, `output_audios/`, and a small dashed `output_audios_pp/` "bonus".
Every drawer but `input_audios/` opens into a sub-drawer `group-01/` (PINK label); a GOLD tag "your
project pays · storage (tiny)" slides onto the cabinet.
SAY: Step 3 is your bucket. The components read and write these prefixes, and every output lands under your group's name.

SHOW: Tag `erratum` ("no command given"). A schematic console (browser window, tag `illustration`,
no logo): "Cloud Storage › Buckets › Create", name field `your-team-bucket`; then the `input_audios/`
drawer receives a small waveform file `input-<something>.mp3`. Under it CODE(mega-pipeline/transcribe_audio/cli.py:
102) with `"input-*.txt"` highlighted PINK and a GREY caption "upload picks only input-*". Fade out.
SAY: Another small gap: the README never says how to create the bucket or fill it. Create it in the console, and upload a short recording named input, dash, something, dot mp3: transcribe only uploads names starting with input.

---

## S05 · Three gates: account, role, API — `s05_gates.py` · `ThreeGates`

SHOW: TRACKER K/1. V3 builds: at left a TEAL container box; a PINK route labelled `/secrets` brings
the GOLD key glyph into it. A GREY README card, header `README.md · line 171`: "an identity for your
code, not for you".
SAY: Your bucket only lets in callers who prove who they are and have permission. For code, that identity is a service account, with one JSON key.

SHOW: Inside the container a small stamp `google.auth` presses the key into a GOLD token tag with a
tiny clock ("short-lived"). The token flies right toward five BLUE doors in a column: Storage,
Speech-to-Text, Vertex AI, Translation, Text-to-Speech. Each door has a lock slot (role) and a
switch (API enabled); Text-to-Speech's door has no lock slot.
SAY: Google's libraries read that key and turn it into a short-lived token. The token goes to Google's API doors, and every call must pass three gates.

SHOW: The three gates label in order. Gate 1 "who?" at the container's edge: the key slot glows;
removed, it flashes RED with the chip `DefaultCredentialsError` "inside the container · S07". Gate 2
"may?": the lock slots glow BLUE. Gate 3 "switched on?": the switches glow BLUE. A RED chip "permission
error · from Google" hangs over gates 2 and 3 (GREY note "said, not shown: nothing here reached
Google").
SAY: Gate 1, who: the key must be there, or the call fails inside your container. Gate 2, may: the account needs a role. Gate 3, switched on: the API must be enabled. Gates 2 and 3 fail at Google, as a permission error.

SHOW: V3 shrinks to the right third. At left a schematic console (browser window, tag
`illustration`, no logo): breadcrumb "IAM & Admin › Service accounts" → "Create service account",
name `mega-pipeline-sa`. TRACKER K/2: a role picker; four roles appear one by one and each flies
onto a lock in V3: "Storage Admin" (`roles/storage.admin`) → the Storage door, with a GREY tag "all
five components"; "Cloud Speech Client" → Speech-to-Text; "Cloud Translation API User" → Translation;
"Agent Platform User" (`roles/aiplatform.user`) → Vertex AI, tag "generate_text · Gemini". README
card `README.md · lines 177–181`.
SAY: In the console, create a service account, say mega-pipeline-sa. Grant it four roles: Storage Admin for every component, Cloud Speech Client, Cloud Translation API User, and Agent Platform User for Gemini.

SHOW: The Text-to-Speech door gets a GREY note "no role needed · README.md line 185". Then a chip
`generate_text/README.md · line 46` "Vertex AI User" (tag `erratum`) is struck through RED; beside it
`README.md · line 179` "Search the role picker for Agent Platform User" gets a GREEN check.
SAY: Text-to-Speech needs no role. A small slip: the generate text README still says Vertex AI User, which finds nothing now; search Agent Platform User.

SHOW: TRACKER K/3. The console: "Keys › Add key › Create new key › JSON". TRACKER K/4. The GOLD key
glyph drops out of the browser into S04's file tree (it slides back in, small) as
`secrets/mega-pipeline.json` (README chip `README.md · line 183`); the dashed row turns solid. A GOLD
tag: "whoever holds this file spends your project's money · never commit it · never paste it".
SAY: Then download a JSON key, and save it as mega-pipeline.json in the secrets folder beside the repo. Whoever holds this file can spend your project's money: never commit it, never paste it anywhere.

SHOW: TRACKER K/5. A GREY README card `README.md · lines 187–189` ("APIs & Services › Library ›
Enable · or all five at once") with a tiny console Library illustration. Terminal (full width, 8
rows, title `laptop`, prompt `student@laptop:~$`). It types `gcloud config set project
<your-project-id>` exactly as the README writes it (TERM(gcloud-laptop/01-config-set-project.txt: 2–3;
session)): line 3 `-bash: syntax error near unexpected token `newline'` prints RED; `<` and `>` in the
typed line get RED circles, tag "bash: redirection". Then it types `gcloud config set project
your-project-id` → TERM(gcloud-laptop/02-config-set-project-filled.txt: 2); `your-project-id` gets a
YELLOW tag "your own ID".
SAY: Next, enable the APIs, in the console or with gcloud. Typed exactly as written, set project fails: the angle brackets belong to the placeholder, and bash reads them as redirections. Type your own project ID, without brackets.

SHOW: TRACKER K/6. The terminal clears (12 rows). It types the README's six rows, `gcloud services
enable \` … `translate.googleapis.com` → TERM(gcloud-laptop/03-services-enable.txt: 7–12, …); line 7
prints RED. A GREY note: "Tutorial 0: gcloud auth login". The terminal shrinks to the strip; in V3
the five API switches flip on one by one (GREY tag `illustration` "with your account"), and a GOLD
tag "calls now bill your project" lands on the doors.
SAY: Then gcloud services enable switches on all five. Our laptop had no Google account, so gcloud reports no active account: that's Tutorial 0's login step. Logged in, it enables them, and calls now bill your project.

SHOW: V3 full: key in place at gate 1 (white tick), all five switches on (white ticks), every lock
filled except Speech-to-Text's, which is dashed and empty. A transcribe chip waits at the container.
PONDER(8 s, "Key in place, every API enabled,\nbut you forgot the Cloud Speech Client role.\nWhere does transcribe fail:\ninside your container, or at Google?")
SAY: Ponder this. Your key is in place and every API is enabled, but you forgot the Cloud Speech Client role. Where does transcribe fail: inside your container, or at Google?

SHOW: The token leaves the container (gate 1 white tick), travels to the Speech-to-Text door, and
bounces RED off its empty lock; a RED chip "permission error · from Google". Caption: "the key says
who · the role says may". `▶ your turn` beside the tracker. Fade out.
SAY: At Google, as a permission error. The key proved who you are; the role decides what you may do. Pause, and set up your account, key and APIs.

---

## S06 · docker-shell.sh: one script, two windows — `s06_script.py` · `DockerShell`

SHOW: TRACKER R/1. CODE(mega-pipeline/transcribe_audio/docker-shell.sh: 6–14) full width (header
`transcribe_audio/docker-shell.sh · lines 6–14`). Line 7 `IMAGE_NAME` highlights, tag "image name =
container name"; lines 8–9 highlight, `$(pwd)` underlined PINK, tag "the folder you're in".
SAY: Every component runs through its docker-shell.sh, so let's read it once. Line 7 names the image, and the container gets the same name. Lines 8 and 9 build paths from pwd, the folder you're in.

SHOW: A YELLOW caption under lines 8–9: "run it from inside the component folder". Line 10
(`GOOGLE_APPLICATION_CREDENTIALS=/secrets/mega-pipeline.json`) highlights PINK, tag "the key's path
inside the container"; line 13 `DOCKER_USERNAME="dlops"` highlights BLUE, tag "Docker Hub account";
line 14 `BUILD_MODE="dev-run"` gets a GREY tag "default".
SAY: So run it from inside the component folder. Line 10 is the key's path inside the container; line 13 names the Docker Hub account, dlops.

SHOW: V4. The panel swaps to CODE(mega-pipeline/transcribe_audio/docker-shell.sh: 28–39) at left
(6.2 wide); at right the `case` becomes a PURPLE switchboard: an input "first word" and four tracks
that light one by one, each with its line chip: (no argument) "build, then run" `:71–76` + `:79–96` ·
`dev` "build only" `:71–76` · `run` "run only" `:79–96` · `prod` "build two architectures, push"
`:51–68`.
SAY: The case statement turns your first word into a mode. No word: build, then run. Dev only builds, run only runs, and prod builds for two processor types and pushes to Docker Hub.

SHOW: A GREY README card `README.md · lines 212–215` lists the four modes side by side; the default
track glows YELLOW, the other three dim with a small GREY tag "later: S08, S09".
SAY: We'll use the default for all five components, then come back to dev, run and prod.

SHOW: V5. The panel fades. Left: the laptop (GREY): `~/AC215/` with `mega-pipeline/transcribe_audio/`
and `secrets/` beside the repo. A small walker starts in `transcribe_audio/`, steps up to
`mega-pipeline/` (label `..`), up to `AC215/` (`../..`), then into `secrets/`; the path
`$(pwd)/../../secrets/` writes itself along the walk (chip `docker-shell.sh · line 9`). Right: the
container (TEAL) with `/app` and `/secrets`, and a GREEN box `/home/app/.venv` outside both. Above,
CODE(mega-pipeline/transcribe_audio/docker-shell.sh: 92–96): line 93 draws a PINK route from the
component folder to `/app`; line 94 a PINK route from `secrets/` to `/secrets`; line 95 raises a PINK
signpost `GOOGLE_APPLICATION_CREDENTIALS=/secrets/mega-pipeline.json` pointing into `/secrets`.
SAY: Running opens two windows into your laptop. Dash v puts the component folder at slash app, and the secrets folder, two levels up, at slash secrets. Dash e sets the signpost Google's libraries follow to the key.

SHOW: CODE(mega-pipeline/transcribe_audio/Dockerfile: 17) `ENV UV_PROJECT_ENVIRONMENT=/home/app/.venv`
appears under the GREEN venv box, which glows; the laptop sheet over `/app` leaves it uncovered. A
TEAL image block "image" sits behind the container: the GOLD key travels along the `/secrets` route
only when a small clock "docker run" ticks, and a GREY bar across the image block reads "never
in here".
SAY: As in lecture 3, the venv lives outside slash app, so the window can't hide it. The key crosses only at run time, never into the image.

SHOW: Terminal (full width, 14 rows, title `laptop`, prompt `student@laptop:~/AC215/mega-pipeline$`).
It types `cd transcribe_audio` → (no output; GREY caption "transcribe_audio/README.md · line 15:
cd into the transcribe_audio folder"); the prompt becomes `student@laptop:~/AC215/mega-pipeline/transcribe_audio$`. It
types `./docker-shell.sh` (on the row under the prompt) → TERM(mega-laptop/12-a-docker-shell.txt:
2–4, 14–18, 24) (BuildKit rows). `Build Mode: dev-run` highlights; `[2/5]` gets a TEAL badge
"build step 2" and its time tag `44.7s` highlights; `exporting to image` tag `52.9s` highlights too;
`[5/5] RUN uv sync` tag `1.6s`; `Building 99.5s` underlines. A GREY note: "first build: Docker also
pulls python:3.14-slim-bookworm". `▶ your turn`.
SAY: Now cd into transcribe audio and run docker-shell.sh, no argument. Build step 2, the system packages, and writing out the image take nearly all the time; a first build also pulls the base image. Pause and run it.

SHOW: The terminal shrinks to the strip. Above it, PANEL(mega-laptop/12-a-docker-shell.plain.txt:
1427–1428, …, 1435, "the same build, full log · lines 1427–1435"): line 1427 `Using CPython 3.14.8
interpreter at: /usr/local/bin/python3` underlines ORANGE, `3.14.8` gets the tag `at the time of
recording`; line 1435 `Installed 26 packages in 87ms` underlines GREEN. Beside it,
CODE(mega-pipeline/transcribe_audio/pyproject.toml: 6) `requires-python = ">=3.14"` and a small
number line (L01's picture in miniature): a GREEN glow from 3.14 rightward, the ORANGE dot `3.14.8`
inside it.
SAY: The full log shows why uv sync is quick: the image's Python, 3.14.8 at the time of recording, already satisfies 3.14 or newer. So uv downloads no Python, and installs 26 packages.

SHOW: The terminal grows back: TERM(mega-laptop/12-a-docker-shell.txt: 26–27). Its title becomes
`container · transcribe_audio` and its frame turns TEAL; the prompt `app@0ceffb272288:/app$`
appears, `app` tagged "user", `/app` PINK "the window", `0ceffb272288` "container ID · your numbers
will differ". TRACKER QA/1. It types `python cli.py --help` → TERM(mega-laptop/12-a-docker-shell.txt:
28–37; session). A one-line README chip `transcribe_audio/README.md · lines 98–107` gets a GREEN check
"identical".
SAY: Then you're inside, as user app, in slash app; after the at sign comes the container ID, new every run. The first check, python cli.py dash dash help, matches the README.

SHOW: TRACKER QA/1 · extra. It types `which python` (extra) → TERM(mega-transcribe_audio/03-x-which-python.txt:
2) (GREEN), `echo $GOOGLE_APPLICATION_CREDENTIALS` (extra) → TERM(mega-transcribe_audio/05-x-credentials-env.txt:
2) (PINK), `ls -la /secrets` (extra) → TERM(mega-transcribe_audio/06-x-ls-secrets.txt: 2–4) with a GREY
tag "empty here · yours lists mega-pipeline.json". The TEAL terminal shrinks to the strip; a second
terminal (title `laptop · second terminal`, 5 rows, prompt
`student@laptop:~/AC215/mega-pipeline/transcribe_audio$`) slides in above it and types `docker inspect
--format '{{range .Mounts}}{{.Source}} -> {{.Destination}}{{println}}{{end}}'
mega-pipeline-transcribe-audio` (extra; folds) → TERM(mega-laptop/14-a-x-mounts.txt: 2–3); a small V5
thumbnail pulses its two PINK routes as each line prints.
SAY: Three extra checks inside: python comes from the venv, the signpost points to slash secrets, and slash secrets is empty here, with no key. From a second terminal, an extra docker inspect lists both mounts.

SHOW: TRACKER R/5. In the second terminal: `ls -l docker-shell.sh` (extra) →
TERM(mega-laptop/19-a-x-ls-l-script.txt: 2), `-rwxr-xr-x` highlights; then `chmod +x docker-shell.sh`
→ (no output); a small tag `erratum` "already executable after a clone · harmless". TRACKER R/6: a GREY
card (README chip `README.md · line 226`): "Windows: Git BASH · 'the input device is not a TTY' → put
winpty in front". Both terminals stay (the container is still open for S07).
SAY: Step 5, chmod plus x, is harmless: an extra ls shows the script is already executable. Step 6, on Windows: use Git BASH, and put winpty in front if Docker says the input device is not a T-T-Y.

---

## S07 · Five components, five honest errors — `s07_components.py` · `RunComponents`

SHOW: TRACKER QA/2. The TEAL terminal from S06 (full width, 14 rows, title `container ·
transcribe_audio`, prompt `app@0ceffb272288:/app$`). It types `python cli.py --download` →
TERM(mega-transcribe_audio/09-download.txt: 2–3, …, 11–12, …, 52; wrap); tag `recorded without a key`.
Line 11 (`File "/app/cli.py", line 39, in download`) highlights YELLOW; line 52 prints RED.
SAY: Back in the container, the Quick Reference. Transcribe's download prints its arguments, then stops: default credentials error, file slash secrets slash mega-pipeline.json was not found.

SHOW: The terminal shrinks to the strip. Above it, a V3 thumbnail: the gate 1 key slot empty, a RED
flash at the container's edge, nothing leaves. Three RED chips write in: "no key in ../../secrets/" ·
"another file name" · "script run from another folder".
SAY: That's gate 1, failing inside the container. The usual causes: no key in the secrets folder, a different file name, or running the script from the wrong folder.

SHOW: TRACKER QA/3 → QA/4. The strip types `python cli.py --transcribe`, then `python cli.py --upload`,
each followed by a small GREY note "same error, same reason" instead of output. Above, a GREY card
"with your key, look for" writes in line by line: "object names printed · cli.py line 44" ·
"Transcribing: … and the transcript · lines 67, 86" · "text_prompts/group-01/input-….txt on your
laptop · line 62" · "Uploading: … · line 108", and a BLUE drawer `text_prompts/group-01/` lights
(tag `illustration`).
SAY: Transcribe and upload stop the same way. With your key, look for object names, the transcript, a text file under text prompts, slash group-01, and after upload, that file in your bucket.

SHOW: A GOLD tag "Speech-to-Text: billed per minute of audio". CODE(mega-pipeline/transcribe_audio/cli.py:
84–86) (header `transcribe_audio/cli.py · lines 84–86`), `results[0]` underlined, tag `erratum` "keeps
only the first chunk"; a small GREY chip "main branch: joins all chunks".
SAY: Speech-to-Text bills per minute of audio, so use a short clip; this branch also keeps only the first chunk of a long transcript.

SHOW: The terminal grows back (14 rows). It types `exit` → TERM(mega-laptop/12-a-docker-shell.txt:
38–39; session); the frame turns GREY, title `laptop`, prompt
`student@laptop:~/AC215/mega-pipeline/transcribe_audio$`. It types `cd ../generate_text` → (no output;
GREY caption "README.md · line 52: cd into each one"). TRACKER QB/1. It types `./docker-shell.sh` →
TERM(mega-laptop/31-b-docker-shell.txt: 4, 14–17, 24, 26–27) (BuildKit rows); `[2/5]` gets the TEAL
badge "build step 2", tag `24.8s`; a GREY note "build-essential only · no ffmpeg"
(CODE(mega-pipeline/generate_text/Dockerfile: 4) as a one-line chip). The TEAL frame returns with
the prompt `app@45263bb6ca36:/app$`; it types `python cli.py --help` → TERM(mega-laptop/31-b-docker-shell.txt:
28–37; session); README chip `generate_text/README.md · lines 114–123` gets a GREEN check.
SAY: Next component: exit, cd into generate text, and run the script. With no ffmpeg, its system layer differs, so it builds afresh, in about 50 seconds. Help matches the README.

SHOW: TRACKER QB/2. The terminal clears. It types `python cli.py --download` →
TERM(mega-generate_text/02-download.txt: 2–3, …, 11–12, …, 52; wrap); tag `recorded without a key`;
line 52 RED. TRACKER QB/3. It types `python cli.py --generate` → TERM(mega-generate_text/03-generate.txt:
2–3); a small GREY chip "exit status 0 · from the capture" appears beside it.
PONDER(6 s, "It exited with status 0.\nDid it call Gemini?")
SAY: Download fails the same way. Generate prints its arguments and the word generate, nothing else, and exits with status 0. Did it call Gemini?

SHOW: The terminal shrinks to the strip. CODE(mega-pipeline/generate_text/cli.py: 52–54) (header
`generate_text/cli.py · lines 52–54`): the `glob.glob(...)` on line 53 highlights, a GREY bubble "[ ]
· no files" pops from it, and the `for` on line 54 dims with a RED "0 rounds". A GREY drawer
`text_prompts/group-01/` on the laptop side shows "empty".
SAY: No. Download had failed, so there were no prompts and the loop had nothing to do. A zero exit status is not proof of work.

SHOW: TRACKER QB/4. The strip types `python cli.py --upload` with a GREY note "needs the key".
TRACKER QB/5. A one-line README chip `generate_text/README.md · lines 91–94`; the strip types `export
GEMINI_MODEL=gemini-2.5-flash`, then `python cli.py --generate` →
TERM(mega-generate_text/05-gemini-model.txt: 3–4). Above, CODE(mega-pipeline/generate_text/cli.py: 73–77):
line 73's `os.environ.get("GEMINI_MODEL", "gemini-2.5-flash-lite")` highlights, the default underlined
GREY. A GOLD tag "Gemini: billed per token".
SAY: Upload needs the key too. The generate text README adds a step: set the Gemini model variable to try another model; line 73 falls back to flash lite. Gemini bills per token.

SHOW: TRACKER QC/1. The terminal grows (14 rows). It types `exit` →
TERM(mega-laptop/31-b-docker-shell.txt: 38–39; session); `cd ../synthesis_audio_en` → (no output);
`./docker-shell.sh` → TERM(mega-laptop/40-c-docker-shell.txt: 4, 14–17, 24, 26–27) (BuildKit rows);
`CACHED [2/5]` highlights GREEN, tag "same as generate_text"; `Building 8.2s` underlines. TEAL frame,
prompt `app@ba0b1df0eadc:/app$`; it types `python cli.py --help` →
TERM(mega-laptop/40-c-docker-shell.txt: 28–33; session); line 33 `AssertionError: Update group name`
RED, with a GREY tag "cli.py left unedited on purpose".
SAY: Next, synthesis audio en builds in 8 seconds, its system layer cached. We left its cli.py unedited on purpose, and help stops at the assert: where a value is blank, the guard works.

SHOW: TRACKER QC/1 · extra. The second terminal (5 rows, prompt
`student@laptop:~/AC215/mega-pipeline/synthesis_audio_en$`) slides in at the top; a pencil edits
`cli.py`, then it types `git diff cli.py` (extra) → TERM(mega-laptop/41-c-x-edit-cli.txt: 16–17); the
same file blinks inside the TEAL terminal's folder icon at the same instant. In the TEAL terminal it
types `python cli.py --help` → TERM(mega-synthesis_audio_en/02-help.txt: 2–4, …, 55; wrap); line 3
(`File "/app/cli.py", line 23`) highlights YELLOW; CODE(mega-pipeline/synthesis_audio_en/cli.py: 23)
appears as a one-line chip "runs on import"; line 55 RED.
SAY: Edit it on the laptop; the window shows the change at once. Now help fails at line 23: this component builds its Google client on import, so even help needs the key.

SHOW: The terminal shrinks to the strip. Above it PANEL(expected/mega-synthesis_audio_en-help.txt:
3–10, "with your key · synthesis_audio_en/README.md · lines 99–107"), tag `expected`. TRACKER QC/2 →
QC/3: the strip types `python cli.py --download`, then `python cli.py --synthesis` (GREY note "needs
the key" each). A one-line README chip `README.md · line 257` "no separate --upload step"; a BLUE
drawer `text_audios/group-01/` receives a waveform written straight from a BLUE Text-to-Speech door
(tag `illustration`); a GOLD tag "Text-to-Speech: billed per character".
SAY: With your key, you'd see the README's help. There's no upload step: Text-to-Speech writes the audio straight into your bucket.

SHOW: Montage, terminal 12 rows. In `translate_text`: TRACKER QD/1→4 ticks as it types `exit`
(TERM(mega-laptop/40-c-docker-shell.txt: 34–35; session)), `cd ../translate_text`, `./docker-shell.sh`
→ TERM(mega-laptop/51-d-docker-shell.txt: 4, 14) (BuildKit rows; `Building 7.9s`, `CACHED [2/5]`), at
`app@40d7497c50f2:/app$` `python cli.py --help` → TERM(mega-laptop/51-d-docker-shell.txt: 28–31, …,
64–65; session, wrap), then `python cli.py --download`, `python cli.py --translate`, `python cli.py
--upload` (no output; GREY "needs the key"). Then in `synthesis_audio`: TRACKER QE/1→3, `exit`
(TERM(mega-laptop/51-d-docker-shell.txt: 66–67; session)), `cd ../synthesis_audio`, `./docker-shell.sh`
→ TERM(mega-laptop/61-e-docker-shell.txt: 4, 14), at `app@6172f2cd7728:/app$` `python cli.py --help`
→ TERM(mega-laptop/61-e-docker-shell.txt: 28–31, …, 93–94; session, wrap), `python cli.py --download`,
`python cli.py --synthesis`. The montage ends on a static GREY card: per folder, the commands typed.
SAY: Translate text and synthesis audio follow the same pattern: an 8-second build, help failing at import, and the Quick Reference commands.

SHOW: Two cards above the strip, tag `erratum` on each. Card 1: CODE(mega-pipeline/translate_text/cli.py:
61–66) with line 64 `target_language="es",` RED, beside CODE(mega-pipeline/synthesis_audio/cli.py:
48–49) (comment cut) with `fr-FR` BLUE; a GREEN fix chip `target_language="fr"`. Card 2: PANEL(mega-synthesis_audio/04-x-cli11-help.txt:
6, "python cli_11.py --help · extra") (cut), caption "the optional ElevenLabs bonus reads
secrets/ inside /app". `▶ your turn` with a GREY note "with your key". Fade out.
SAY: Two small slips. Translate targets Spanish, but the final voice is French: change es to fr. And the optional ElevenLabs bonus looks for its key in slash app. Pause, and run all five with your key.

---

## S08 · dev, run, and a stale image — `s08_run.py` · `DevAndRun`

SHOW: TRACKER R/2. A small V4 switchboard at the top with the `dev` track lit. Terminal (full width,
10 rows, title `laptop`, prompt `student@laptop:~/AC215/mega-pipeline/transcribe_audio$`; GREY caption
"back in transcribe_audio"). It types `./docker-shell.sh dev` → TERM(mega-laptop/17-a-dev.txt: 2–4,
14–17) (BuildKit rows); `Build Mode: dev` highlights; each `CACHED` turns GREEN; `Building 0.3s`
underlines; the prompt returns (GREY tag "no container").
SAY: Back in transcribe audio, step 2 of How to Run: docker-shell.sh dev. It only builds. Nothing changed, so every step comes from the cache, and no container starts.

SHOW: TRACKER Y/1. A one-line README chip `transcribe_audio/README.md · line 89`. The terminal
shrinks to the strip; a TEAL strip above it (prompt `app@0ceffb272288:/app$`) types `uv add
<package>` (command only, GREY tag "placeholder · lecture 3 ran it"). V5 thumbnail: `pyproject.toml`
and `uv.lock` blink on the laptop sheet and inside `/app` at once; a small package chip drops into a
dashed TEAL "throwaway" layer. Then the laptop strip shows `./docker-shell.sh dev` again (no new
typing; an arrow from the earlier line) and the chip moves into a solid TEAL image layer "baked in".
SAY: What is dev for? The component README says: add a package with uv add inside the container, which updates pyproject.toml and uv.lock through the window. Then rebuild with dev to bake it into the image.

SHOW: TRACKER R/3. V4: the `run` track lights; a PINK diamond "local image?" sits on it. The terminal
(10 rows) types `./docker-shell.sh run` → TERM(mega-laptop/18-a-run-local.txt: 2–6; session) (the
prompt `app@631fac50f92b:/app$` appears and `exit` is typed). The diamond takes the "yes" branch to a
TEAL box on the laptop; `Using local image...` highlights.
SAY: Step 3, run, skips the build. It says using local image, because one exists.

SHOW: Tag `erratum`. A GREY README card `README.md · line 74`: "run to pull and run from the
registry". Below, CODE(mega-pipeline/transcribe_audio/docker-shell.sh: 82–89): line 83 `docker image
inspect $IMAGE_NAME` PINK (the diamond), line 85 → "yes: local, however old" (GREY tag), line 88
`CONTAINER_IMAGE=$DOCKER_USERNAME/$IMAGE_NAME` → "no: Docker Hub" (BLUE).
SAY: A small inaccuracy: the README says run pulls from the registry. The script first uses any local image of that name, however old, and goes to Docker Hub only when there's none.

SHOW: V1 returns (recipe card left, BLUE shelf right, signpost `dlops/mega-pipeline-transcribe-audio:latest`)
with the switchboard between. A GREY teammate glyph with an empty laptop: "never built it".
PONDER(8 s, "A teammate has never built this image.\nThey type ./docker-shell.sh run.\nWhich Python do they get?")
SAY: Ponder this. A teammate has never built this image, and types docker-shell.sh run. Which Python do they get?

SHOW: TRACKER R/3 · extra. The terminal (12 rows) types `docker image rm mega-pipeline-transcribe-audio`
(extra) → TERM(mega-laptop/71-x-rm-local-image.txt: 2–3) (cut); the TEAL box on the laptop dissolves.
GREY caption: "now we are that teammate".
SAY: Let's find out. This extra command deletes our local image, so we become that teammate.

SHOW: TRACKER R/3. It types `./docker-shell.sh run` → TERM(mega-laptop/72-run-registry.txt: 2–6, …,
18–21) (cut). `Local image not found, using image from registry...` highlights YELLOW; in V4 the
diamond takes the "no" branch and a BLUE arrow pulls the sealed box down from the shelf;
`Creating a Pipfile for this project...` highlights, with a GREY tag "pipenv: the course's tool
before uv".
SAY: Local image not found, so it pulls the dlops image from Docker Hub. Then a surprise: creating a Pipfile. That's pipenv, the tool this course used before uv.

SHOW: The terminal clears and the session continues: TERM(mega-laptop/72-run-registry.txt: 24–29, …,
33; session). At the prompt `(app) root@36615ab6e34b:/app#` (`root` tagged RED "root") it types
`python --version` (line 24) → line 25, `which python` (26) → 27, `python cli.py --help` (28) → 29,
`…`, 33. `Python 3.8.17` highlights YELLOW; `optional arguments:` gets a GREY tag "Python 3.8's
argparse wording".
SAY: The prompt says root. Python is 3.8.17, in an environment pipenv made. Help still works here, in Python 3.8's older wording.

SHOW: TRACKER R/3 · extra. Above the strip, PANEL(mega-laptop/74-x-registry-image.txt: 4, 6–7,
"docker image inspect dlops/mega-pipeline-transcribe-audio · extra") and the excerpt chip
`PYTHON_VERSION=3.8.17` (header `mega-laptop/74 · line 5 (excerpt)`). In V1 the sealed box opens; four
labels rise out of it as they're said: `2025-02-18`, `Python 3.8.17`, `pipenv shell`, `user: root`
(RED).
SAY: An extra inspect opens the box: created on 18 February 2025, Python 3.8.17, starting pipenv shell, as root.

SHOW: CODE(mega-pipeline-pipenv-flexible-workflow/transcribe_audio/Dockerfile: 2) (header
`pipenv-flexible-workflow · transcribe_audio/Dockerfile · line 2`) `FROM python:3.8-slim-buster`. In
V1, a dashed line runs from the open box to an older GREY recipe card on a second Git shelf labelled
"branch pipenv-flexible-workflow", not to our GREEN card. A GREY sheet (your folder) slides over the
box's `/app`: caption "your code, their environment". A thumbnail of S01's terminal flashes with
line 25 of mega-laptop/76-run-registry-b.txt in RED: "generate_text: the import fails".
SAY: Its build matches an older branch, pipenv flexible workflow, not your recipe. Your folder slides over its slash app: your code, their environment. For generate text, that's the import error from the start.

SHOW: TRACKER R/3 · extra. A laptop strip (title `laptop · second terminal`, prompt
`student@laptop:~/AC215/mega-pipeline/transcribe_audio$`) types `ls -la` (extra) →
TERM(mega-laptop/73-x-host-after-registry.txt: …, 7, …) (`root` in line 7 RED), then `git status --short`
(extra) → TERM(mega-laptop/73-x-host-after-registry.txt: …, 20). In V1 a small GREY file glyph
`Pipfile` with a RED `root` badge drops out of the box into the laptop folder. A GREY fix chip: "delete
it".
SAY: And as root, it left a Pipfile in your folder, owned by root. Delete it.

SHOW: The fix card, two rows: GREEN "build locally · no argument, or dev"; BLUE "run · only images your
team pushed from this branch · your own DOCKER_USERNAME". Fade out.
SAY: So build locally, with no argument or with dev. Use run only for images your own team pushed from this branch, under your own Docker Hub account.

---

## S09 · prod, a stowaway key, and clean-up — `s09_prod.py` · `ProdAndCleanup`

SHOW: TRACKER R/4. V4's `prod` track lights. CODE(mega-pipeline/transcribe_audio/docker-shell.sh:
54–62) (header `transcribe_audio/docker-shell.sh · lines 54–62`): lines 55–57 (inspect, remove) and
line 62 `docker buildx create --driver-opt network=host --use --name multi-arch` highlight in turn;
`--use` gets a PURPLE tag "becomes the current builder · never switched back"; a GREY caption "check
with docker buildx ls".
SAY: Step 4, prod, publishes. It deletes and recreates a builder named multi-arch; the use flag makes it current, and the script never switches back.

SHOW: The panel swaps to CODE(mega-pipeline/transcribe_audio/docker-shell.sh: 64–68): line 66
highlights, `--platform linux/amd64,linux/arm64` PURPLE, `--push` BLUE. A PINK signpost with two
arrows: one to a TEAL box "amd64", one to a TEAL box "arm64", both on the BLUE shelf; two small GREY
glyphs below: an Apple-silicon Mac taking "arm64", a cloud VM taking "amd64" (tag "lecture 2").
SAY: Then one buildx build makes images for two processor types, amd64 and arm64, and pushes both under one tag. As in lecture 2, an Apple-silicon Mac pulls one, a cloud VM the other.

SHOW: TRACKER U/1. A one-line README chip `transcribe_audio/README.md · line 129`. A strip (title
`laptop`, prompt `student@laptop:~/AC215/mega-pipeline/transcribe_audio$`) types `docker login -u
<USER NAME> -p <ACCESS TOKEN>` (command only, GREY tag "not run here"); `-p` gets a GOLD note "the
token stays in your shell history". CODE(mega-pipeline/transcribe_audio/docker-shell.sh: 13) as a chip
with the README chip `README.md · line 76` "update DOCKER_USERNAME". TRACKER U/2 (and R/4): it types
`./docker-shell.sh prod` (command only, GREY tag "not run here: needs a login · publishes an image").
SAY: Before prod, log in with your user name and an access token; dash p leaves the token in your shell history. Set the Docker username in the script to your own account. We don't run prod here: it publishes.

SHOW: TRACKER R/2 · extra. Terminal (full width, 12 rows, title `laptop · lecture 3 clone`, prompt
`student@laptop:~/AC215-l03/mega-pipeline/transcribe_audio$`); a V2 thumbnail with the GOLD key in
the ignored pile. It types `./docker-shell.sh dev` (extra here) →
TERM(mega-l03-laptop/12-x-dev-old-key.txt: 2, 4, 16, 24) (BuildKit rows); `[4/5] COPY --chown=app:app . ./`
(not CACHED: the folder holds the old `secrets/`) highlights YELLOW. It types `docker run --rm
--entrypoint ls mega-pipeline-transcribe-audio -la /app /app/secrets` (extra; folds) →
TERM(mega-l03-laptop/13-x-key-in-image.txt: 2, …, 12, …, 15, 19); line 19 `mega-pipeline.json` RED,
tag `stand-in file · not a real key`.
SAY: Now the switched lecture 3 clone, with its old key still in transcribe audio. Build there with dev, and an extra command lists the new image's slash app. The key is inside the image.

SHOW: The terminal shrinks to the strip. V5 contrast above: CODE(mega-pipeline/transcribe_audio/Dockerfile:
39) `COPY --chown=app:app . ./`; the whole component folder, including `secrets/` with the GOLD key,
packs into a TEAL image layer. CODE(mega-pipeline/transcribe_audio/.gitignore: 3) `/secrets` drawn as
a shield standing only in front of a GREY "Git" shelf; a dashed GREY chip "`.dockerignore`: none, on
every branch". The prod track carries the layer up to the BLUE shelf, which flashes RED.
SAY: The copy line takes the whole folder. The gitignore keeps secrets out of Git, not out of images, and no branch has a dockerignore. Prod would push your key to Docker Hub.

SHOW: Tag `erratum`: a GREY README card `README.md · line 203` "the canonical way to make that mistake
impossible" with a GREY note "for Git: yes · for images: no". A fix card writes in: "delete the
secrets/ folder inside each component" · "add a .dockerignore listing secrets/ (lecture 3)" · RED
"a key was ever pushed? delete that key in IAM". `▶ your turn`.
SAY: So the README's promise holds for Git, not for images. Delete any secrets folder inside a component, add a dockerignore listing secrets, and if a key was ever pushed, delete that key. Pause and check yours.

SHOW: TRACKER R/4 · extra. Terminal (8 rows, title `laptop`, prompt `student@laptop:~/AC215/mega-pipeline$`)
types `docker images` (extra) → TERM(mega-laptop/70-x-images.txt: 2–7; column view); `1.48GB` and
the four ~830 MB sizes highlight. A clean-up card for part 1 writes in beside the strip as the SAY
names it: "exit each container · --rm removes it" · "docker image rm <name> · your five images
(pattern: mega-laptop/71)" · "any dlops/* you pulled (mega-laptop/78)" · "the root-owned Pipfile".
SAY: Clean-up for part 1. Exit each container; dash dash r m deletes it. The transcribe image alone is 1.48 gigabytes: remove all five with docker image rm, along with any dlops images you pulled.

SHOW: Two GOLD rows join the card: "bucket: storage bills until you delete it" and "key: valid until
you delete it · IAM › Service accounts › Keys" (a tiny console illustration). Then a closing card:
"Part 2: containers that talk to each other directly", with the two small TEAL boxes and a PINK arrow
between them. Everything fades to an empty frame (end of part 1).
SAY: In the cloud, the bucket bills storage until you delete it, and the key works until you delete it in the console. In part 2: containers that talk to each other directly.

---

## S10 · Two little computers, one network — `s10_network.py` · `TwoComputers`

SHOW: No tracker yet. Left: part 1's five TEAL boxes over the BLUE cabinet, every arrow through a
drawer (README chip `mega-pipeline · README.md · lines 140–142`). It dims. Right: a GREY browser glyph,
a TEAL box `gateway`, a TEAL box `processor`, joined by direct PINK arrows (GREY card
`port_toy · README.md · line 52`: "Browser → localhost:8090 → Gateway → processor:9200 → Processor").
A GREY chip: "only Docker · README.md line 24".
SAY: In part 1, containers never talked to each other: they left files in a bucket. Port toy makes two containers talk directly, and it needs only Docker. A gateway serves a web page and forwards your text to a processor, which turns it into capitals.

SHOW: V6. The two TEAL boxes grow into glass boxes. Inside each, a small `localhost` loop and a
strip of ports `1 … 65535`; both strips light `9100` at the same time without clashing (caption
"each box: its own ports"). A GREY laptop outline around them has its own third `localhost` loop.
SAY: Think of each container as its own little computer, with its own localhost and its own full set of ports. Two containers can both use port 9100 without any clash.

SHOW: A TEAL rail slides under the boxes, labelled "user-defined network"; a PINK phone-book icon sits
on it with two blank lines. A GREY note: "Docker's default network: no phone book (exercises)".
SAY: A network you create is a small LAN between them, with a phone book that turns container names into addresses. Docker's default network has no such phone book.

SHOW: TRACKER P0/1 (the tracker appears, port_toy README). Terminal (full width, 12 rows, title
`laptop`, prompt `student@laptop:~/AC215$`). It types `docker run hello-world` →
TERM(port-laptop/01-hello-world.txt: 2–3, …, 7, 9–10, …); line 9 `Hello from Docker!` highlights GREEN.
SAY: Prerequisites: docker run hello-world checks that Docker is running. It pulls a tiny image and prints hello from Docker.

SHOW: TRACKER P1/1. A one-line README chip `README.md · line 81` "Clone or download the repository".
It types `git clone https://github.com/dlops-io/port_toy.git` (GREY caption "the README links the repo
but prints no clone command") → TERM(port-laptop/02-clone.txt: 2); then `cd port_toy` → (no output);
prompt `student@laptop:~/AC215/port_toy$`. `▶ your turn`.
SAY: Step 1 sets the app up by hand, starting with the code. The README says clone or download; here's the clone command, which it doesn't print. Then cd into port toy. Pause and run them.

SHOW: TRACKER P1/1 · extra. It types `ls gateway processor` (extra) → TERM(port-laptop/04-ls.txt: 11–18),
then `git log --oneline -1` (extra) → TERM(port-laptop/04-ls.txt: 19); `d190c71` gets a GREY tag "the
pinned commit". Above the terminal, the README's tree (`README.md · lines 59–69`) with a GREEN check
on each file as it prints.
SAY: Two extra checks: the files match the README's tree, a gateway and a processor, and git log shows the commit this video pins.

SHOW: TRACKER P1/2. It types `docker network create toynet` → TERM(port-laptop/05-network-create.txt: 2)
(cut); above, V6's TEAL rail gets the label `toynet`, and the network ID chip flies onto it (tag "your
numbers will differ").
SAY: Next, docker network create toynet. Docker prints the new network's ID: that's the rail both containers will plug into.

SHOW: TRACKER PH/4 (the tracker shows the Handy commands section). It types `docker network ls` →
TERM(port-laptop/06-network-ls.txt: 2–6); `toynet` highlights TEAL, `bridge`, `host`, `none` get a
GREY bracket "built in". `▶ your turn`. Fade out.
SAY: From the README's handy commands, docker network ls lists it, beside Docker's three built-in networks. Pause, and create yours.

---

## S11 · Build, start, read the logs — `s11_start.py` · `BuildAndStart`

SHOW: TRACKER P1/3. CODE(port_toy/gateway/Dockerfile: 1–5) (header `gateway/Dockerfile · lines 1–5`)
at the top; line 1 `FROM python:3.14-slim` ORANGE, line 2 (apt installs `curl`) ORANGE, line 4 `COPY
. .` GREEN, line 5 `CMD ["python", "-u", "gateway.py"]` with `-u` circled and a GREY tag "unbuffered:
prints reach docker logs at once". A GREY chip "processor/Dockerfile: the same, except line 5".
SAY: Next, build two images. The two Dockerfiles are almost identical: a slim Python 3.14 image, plus curl from apt. Each copies its code and runs the script with dash u, so prints reach the logs at once.

SHOW: Terminal (full width, 12 rows, title `laptop`, prompt `student@laptop:~/AC215/port_toy$`). It
types `docker build -t toy-processor ./processor` → TERM(port-laptop/07-build-processor.txt: 3, 13–15,
22) (BuildKit rows); `[2/4] RUN apt-get …` gets the TEAL badge "build step 2", tag `6.4s`; `Building
7.5s` underlines. A GREY note: "first build: Docker also pulls python:3.14-slim".
SAY: The processor builds first, and its apt layer takes a few seconds. Your first build also pulls the Python base image.

SHOW: It types `docker build -t toy-gateway ./gateway` → TERM(port-laptop/08-build-gateway.txt: 3,
13–15, 22) (BuildKit rows); `CACHED [2/4]` and `CACHED [3/4]` highlight GREEN; `Building 0.3s`
underlines. Above, the two Dockerfiles side by side as thin GREEN cards: lines 1–4 linked by GREY
"=" marks, line 5 differs.
SAY: Then the gateway: Docker reuses the processor's apt layer from the cache, because the two files match up to the copy line. It's done in under a second.

SHOW: TRACKER P1/4. It types the README's two rows `docker run -d --name processor --network toynet \`
/ `  -e PORT=9200 toy-processor` → TERM(port-laptop/10-run-processor.txt: 3) (cut). A one-line README
chip `README.md · line 113` "There is no -p flag". The terminal shrinks to the strip; above,
CODE(port_toy/processor/processor.py: 42–45): line 42 reads `PORT` (PINK), line 43
`HTTPServer(("", port), Processor)` with `""` circled, tag "every interface of its own box". V6: the
processor box plugs into the `toynet` rail; its door `:9200` lights TEAL, facing only the rail.
SAY: Then start the processor on toynet, with PORT set to 9200, and no dash p. It listens on 9200, on every interface of its own box, but nothing on your laptop leads to it.

SHOW: TRACKER P1/5. The terminal grows (10 rows). It types the README's five rows `docker run -d
--name gateway --network toynet \` / `  -p 127.0.0.1:8090:9100 \` / `  -e PROCESSOR_HOST=processor \` /
`  -e PROCESSOR_PORT=9200 \` / `  toy-gateway` → TERM(port-laptop/11-run-gateway.txt: 6) (cut). V7: the
three numbers of `127.0.0.1:8090:9100` lift off the flag in order and land as labels: "IP address"
on a GREY door `127.0.0.1:8090` on the laptop, "host port" on the same door, "container port" on the
gateway's TEAL room `:9100`; a PINK arrow goes through the door and bends into the room (README card
`README.md · lines 224–228` "IP address : host port : container port").
SAY: Then start the gateway. Dash p publishes it, in the order IP address, host port, container port: your laptop's 127.0.0.1, port 8090, forwards to port 9100 inside the gateway.

SHOW: The two `-e` rows highlight PINK; CODE(port_toy/gateway/gateway.py: 13–14) appears above the
strip; a PINK dashed arrow from the gateway to "processor : 9200" on the rail (not yet sent).
SAY: The two dash e flags tell the gateway where to call: the name processor, port 9200. Lines 13 and 14 of its code read them, so nothing about the processor is hard-wired.

SHOW: TRACKER P1/6. It types `docker logs processor` → TERM(port-laptop/12-logs-processor.txt: 2) and
`docker logs gateway` → TERM(port-laptop/13-logs-gateway.txt: 2); `9200` and `9100` highlight TEAL. A
small GREY README card `README.md · lines 139–140` with the same two lines. `▶ your turn`. Fade out.
SAY: Now check docker logs for each. The processor listens on 9200, internal only; the gateway listens on 9100. Pause and start both.

---

## S12 · Send a message: ports on the wire — `s12_send.py` · `SendMessage`

SHOW: TRACKER P1/7. PAGE(port-laptop/14-send.txt) builds in three moments as the SAY names them: the
address bar `localhost:8090`; the input "hello from the laptop" and a click on Send; the reply
card `HELLO FROM THE LAPTOP` and the port card (`gateway sent from port 55620`, `processor listening
on port 9200`, `processor saw it arrive from 55620`). A one-line README chip `README.md · lines
147–149`.
SAY: To finish step 1, open localhost 8090 in your browser, type a message, and click Send. The reply comes back in capitals, with three port numbers: where the gateway sent from, where the processor listened, and where it saw the message arrive from.

SHOW: REPLY(port-laptop/14-send.txt: 2) (wrap) under the page; each JSON value links with a thin GREY
line to its place on the page (`upper` → reply card; `gateway_out_port`, `listen_port`, `sender_port`
→ the three port lines).
SAY: We recorded without a browser, so curl sent the page's exact request; this is the reply it got.

SHOW: V7's ticket. The page shrinks to the left third. Right: the gateway and processor boxes on the
`toynet` rail. A packet leaves the gateway; the gateway's operating system (a small GREY gear) prints
a PINK ticket `55620` and staples it to the packet; the packet's destination tag reads `processor :
9200`. A GREY caption: "every connection has two ends, each with a port".
SAY: The processor listened on 9200, the destination. But every connection has two ends, so the gateway's side needs a port too. Its operating system picked a temporary one, 55620, and stapled it to the packet.

SHOW: The packet arrives; the processor reads the ticket `55620` back (it pulses GREEN on both
ends). Above, CODE(port_toy/gateway/gateway.py: 32–38) with line 33 (`HTTPConnection(PROCESSOR_HOST,
PROCESSOR_PORT)`, by name) and line 38 (`getsockname()[1]`) highlighted, then
CODE(port_toy/processor/processor.py: 28–33) with line 32 (`self.client_address[1]`) highlighted. A
GREY README chip `README.md · lines 161–169` "ephemeral source port".
SAY: The processor saw the same number arrive, because nothing rewrites it inside the network. Line 38 of the gateway reads its own port; line 32 of the processor reads the sender's.

SHOW: The page sends again: PAGE(port-laptop/15-send-again.txt) updates its port card to `55634`, and
REPLY(port-laptop/15-send-again.txt: 2) replaces the strip; a new PINK ticket `55634` prints on a new
packet. Tag "your numbers will differ".
SAY: Send again, and the number changes: a new connection, a new temporary port. Yours will differ.

SHOW: The page's diagram zooms in: the label `localhost:8090 → :9100` with `8090` YELLOW.
CODE(port_toy/gateway/index.html: 86–89) above it: line 87 `location.port` highlights, tag "read from
the address bar". The gateway box gets a GREY thought bubble "which door?" with a "?" inside.
`▶ your turn`. Fade out.
SAY: One more detail: the page's diagram shows 8090 by reading its own address bar. The container can't know which door on your laptop you gave it. Pause, and send a message.

---

## S13 · Who can reach whom — `s13_reach.py` · `WhoCanReach`

SHOW: TRACKER P2/1. Terminal (full width, 12 rows, title `laptop`, prompt
`student@laptop:~/AC215/port_toy$`). It types `docker ps` → TERM(port-laptop/16-ps.txt: 2–4; wrap); the
gateway's `127.0.0.1:8090->9100/tcp` highlights YELLOW; the processor's empty PORTS cell gets a dashed
YELLOW box and a GREY tag "listening ≠ published". A one-line README chip `README.md · line 230` "The
host port comes first".
SAY: Step 2 checks the ports. Docker ps shows the gateway's mapping: 127.0.0.1, port 8090, to 9100, host first. The processor's PORTS column is empty: it listens, but nothing is published.

SHOW: TRACKER P2/1 · extra. It types `docker ps --format 'table {{.Image}}\t{{.Ports}}\t{{.Names}}'`
(extra; folds) → TERM(port-laptop/17-ps-short.txt: 2–4); beside it a small GREY card,
PANEL(expected/port_toy-docker-ps.txt: 2–4, "README.md · lines 204–206"), tag `expected`, with GREEN
"=" marks row by row.
SAY: An extra docker ps with three columns matches the README's sample.

SHOW: V7 above a strip. A one-line README chip `README.md · line 239` "-p 8090:9100". It types `docker
run -d --name gateway-all --network toynet -p 8090:9100 toy-gateway` (extra; folds) →
TERM(port-laptop/18-x-all-addresses-taken.txt: 2–3; wrap); the tail of line 3, `Bind for
127.0.0.1:8090 failed: port is already allocated`, highlights RED. In V7, a second PINK arrow aims at
the laptop's door `8090` and is stopped RED; inside, the gateway room `:9100` and the processor room
stay calm (caption "host doors collide · rooms never do"). It types `docker rm gateway-all` (extra) →
TERM(port-laptop/19-x-rm-created.txt: 2), GREY tag "created anyway · remove it".
SAY: Why the 127.0.0.1? Only host ports can collide. This extra run asks for 8090 on every address, and Docker refuses: port is already allocated. The container was still created, so remove it.

SHOW: It types `docker run -d --name gateway-all --network toynet -p 8091:9100 toy-gateway` (extra)
→ TERM(port-laptop/20-x-all-addresses.txt: 2) (cut); then `docker ps --format 'table
{{.Image}}\t{{.Ports}}\t{{.Names}}'` (extra) → TERM(port-laptop/21-x-ps-all-addresses.txt: 2–5) with
`0.0.0.0:8091->9100/tcp` YELLOW; then `docker rm -f gateway-all` (extra) →
TERM(port-laptop/21-x-ps-all-addresses.txt: 6). In V7, a wide GREY door `0.0.0.0:8091` faces the
street (small GREY glyphs of other machines outside), while `127.0.0.1:8090` faces only inward.
SAY: With 8091 it works, and the mapping shows 0.0.0.0: every address, so other machines may connect. Then remove it. The README keeps 127.0.0.1: this laptop only.

SHOW: TRACKER P2/2. The terminal clears. It types `curl http://localhost:8090` →
TERM(port-laptop/22-curl-8090.txt: 2–7, …, 154–155) (cut). Then `curl --max-time 3
http://localhost:9200/health` → TERM(port-laptop/23-curl-9200.txt: 2) RED. In V7, the laptop's dashed
arrow to the processor's `:9200` bounces RED (no door on the laptop). A one-line README chip
`README.md · line 262` "assuming nothing else is using port 9200".
SAY: From the laptop, curl on 8090 returns the gateway's page. Curl on 9200 can't connect: your laptop has no door to it, unless something else of yours happens to use 9200.

SHOW: TRACKER P2/3. It types `docker exec gateway curl http://processor:9200/health` →
TERM(port-laptop/24-exec-processor.txt: 2–5); lines 2–4 get a GREY tag "curl's progress meter"; `ok`
highlights GREEN. V6: a PINK packet leaves the gateway along the `toynet` rail and reaches the
processor's `:9200`.
SAY: From inside the gateway, docker exec runs curl, asking for processor on port 9200 by name. The answer: ok.

SHOW: V6: inside the gateway box, its `localhost` loop glows YELLOW; the command chip `docker exec
gateway curl --max-time 3 http://localhost:9200/health` sits above it, unanswered.
PONDER(6 s, "Same command, but localhost instead of processor:\ndocker exec gateway curl --max-time 3 http://localhost:9200/health\nWhat answers?")
SAY: Ponder this. The same command with localhost instead of processor. What answers?

SHOW: It types `docker exec gateway curl --max-time 3 http://localhost:9200/health` →
TERM(port-laptop/25-exec-localhost.txt: 2–4, 5–6; wrap) (lines 5–6 joined), the last line RED. In V6
the packet loops back into the gateway itself, where no `:9200` door exists. TRACKER P2/3 · extra: it
types `docker exec gateway curl -s http://localhost:9100 | head -4` (extra) →
TERM(port-laptop/26-x-exec-localhost-9100.txt: 2–5); the loop lands on the gateway's own `:9100` door
(GREEN). A one-line README chip `README.md · line 290` "localhost means the gateway itself".
SAY: Nothing. Inside the gateway, localhost is the gateway itself, and nothing there listens on 9200. An extra check: on 9100, its own port, localhost returns the page.

SHOW: TRACKER PH/5. The terminal clears. It types `docker network inspect toynet` →
TERM(port-laptop/28-network-inspect.txt: 4, …, 16, …, 32, …, 35, …, 39, …, 42, …); `172.19.0.0/16`,
`gateway` / `172.19.0.3/16` and `processor` / `172.19.0.2/16` highlight PINK. V6's phone book on the
rail fills its two lines: `processor → 172.19.0.2`, `gateway → 172.19.0.3`.
SAY: So how did the name work? From the handy commands, docker network inspect shows toynet's addresses: one for the processor and one for the gateway, on toynet's own subnet.

SHOW: TRACKER PH/5 · extra. It types `docker exec gateway cat /etc/resolv.conf` (extra) →
TERM(port-laptop/29-x-dns.txt: …, 6, …) (`nameserver 127.0.0.11` PINK), then `docker exec gateway getent
hosts processor gateway` (extra) → TERM(port-laptop/29-x-dns.txt: 13–14). In V6 the phone-book icon
gets the label `127.0.0.11`, drawn inside each box; a GREY note: "addresses may change on restart ·
names stay".
SAY: Inside each container, Docker runs a phone book at 127.0.0.11 that turns names into those addresses. Addresses can change when a container restarts; names stay.

SHOW: TRACKER PH/1. It types `docker exec -it gateway sh` → TERM(port-laptop/29b-exec-it-sh.txt: 2–6;
session) (prompt `#`; `hostname`, `ls`, `exit` typed); `3bf0f65d0cf0` gets a GREY tag "= the gateway's
container ID (docker ps)". Then a small PANEL(port-laptop/27-x-processor-has-curl.txt: 2, "docker exec
processor curl --version | head -1 · extra") (cut) with a tag `erratum` "README.md line 294: the
processor doesn't need curl · it has it anyway". `▶ your turn`. Fade out.
SAY: Another handy command, docker exec dash i t gateway sh, opens a shell inside; its hostname is the container ID that docker ps showed. One aside: the processor image has curl too, though the README implies it doesn't. Pause, and test from both sides.

---

## S14 · Change the ports — `s14_ports.py` · `ChangePorts`

SHOW: TRACKER P3/1. V7 at the top: the laptop's GREY door `127.0.0.1:8090`, a PINK arrow into the
gateway's TEAL room `:9100`; a slider glyph on the door. Terminal (full width, 10 rows, title
`laptop`, prompt `student@laptop:~/AC215/port_toy$`). It types `docker rm -f gateway` →
TERM(port-laptop/30-rm-gateway.txt: 2); then the README's five rows with `-p 127.0.0.1:8095:9100` →
TERM(port-laptop/31-run-gateway-8095.txt: 6) (cut). `8095` highlights YELLOW; the slider moves the
door 8090 → 8095 while the room stays `:9100`.
SAY: Step 3 changes the ports. Think of 8090 as the street door and 9100 as the room inside. First the door: remove the gateway, and start it again on 127.0.0.1, port 8095.

SHOW: PAGE(port-laptop/32-send-8095.txt) (address bar `localhost:8095`; port card `47520`, `9200`,
`47520`) with REPLY(port-laptop/32-send-8095.txt: 2) (wrap). TRACKER P3/1 · extra. The terminal types
`curl --max-time 3 http://localhost:8090` (extra) → TERM(port-laptop/33-curl-8090-gone.txt: 2) RED, then
`docker ps --format 'table {{.Image}}\t{{.Ports}}\t{{.Names}}'` (extra) → TERM(port-laptop/35-ps-8095.txt:
2–4) with `127.0.0.1:8095->9100/tcp` YELLOW.
SAY: The page works on 8095. Two extra checks: 8090 no longer connects, and docker ps shows the new mapping. The room inside, 9100, didn't move.

SHOW: A GREY README card `README.md · lines 357–363`: a second app (a GREY box "another app") already
holds the laptop door `8090`; the gateway takes `8095` beside it; inside, both rooms could be `:9100`
(caption "rooms never collide").
SAY: Why do this? Another app on your laptop might already hold 8090. Doors on the laptop must be unique; ports inside containers never collide.

SHOW: TRACKER P3/1 · extra. It types `docker logs gateway` (extra) → TERM(port-laptop/34-logs-gateway-8095.txt:
2); `open http://localhost:8090` highlights RED, tag `erratum`. CODE(port_toy/gateway/gateway.py: 53)
appears as a one-line chip with `http://localhost:8090` underlined: "a fixed string". Two GREEN chips:
"trust docker ps" · "trust the page's diagram".
SAY: A small slip: the gateway's log still says open localhost 8090. That text is fixed in line 53. Trust docker ps and the page instead.

SHOW: TRACKER P3/2. The terminal clears. It types `docker rm -f processor` →
TERM(port-laptop/36-rm-processor.txt: 2); then the README's two rows with `-e PORT=9300` →
TERM(port-laptop/37-run-processor-9300.txt: 3) (cut). V7: the processor's room moves `:9200` →
`:9300`; the gateway's PINK arrow still aims at `processor : 9200` and turns RED. A one-line README
chip `README.md · line 380` "Send a message from the browser. It should fail."
SAY: Next, the processor's port: remove it, and start it with PORT set to 9300. The README says: send a message, and it should fail.

SHOW: PAGE(port-laptop/32-send-8095.txt) stays exactly as it was (the old reply), a click on Send,
nothing moves; a GREY tag "the page doesn't change" and the tag `erratum` "no error handling ·
index.html lines 95–100". REPLY(port-laptop/38-send-fails.txt: 3) in RED under it.
SAY: It does, but quietly. The page has no error handling, so nothing on it changes; the captured request got only empty reply from server.

SHOW: TRACKER P3/2 · extra. It types `docker logs gateway` (extra) → TERM(port-laptop/39-logs-gateway-refused.txt:
2–5, …, 25–26, …, 55; wrap); line 25 (`File "/app/gateway.py", line 34, in do_POST`) YELLOW, line 55
`ConnectionRefusedError: [Errno 111] Connection refused` RED. Above, a GREY cheat-sheet card
`README.md · lines 551–552`: "Connection refused: nothing is listening" (GREEN tick on "the name
resolved"), and a dashed GREY row "could not resolve host: a wrong name · exercises".
SAY: To see why, an extra docker logs on the gateway. It found the processor by name, but the connection was refused: nobody listens on 9200 anymore. A wrong name would fail differently; that's in the exercises.

SHOW: V7 full: the processor's room `:9300`, the gateway's RED arrow at `9200`, and two settings
shown as chips: the processor's `PORT=9300` and the gateway's `PROCESSOR_PORT=9200`.
PONDER(6 s, "Which one setting fixes it?\nAnd does any image need rebuilding?")
SAY: Ponder this. Which one setting fixes it, and does any image need rebuilding?

SHOW: TRACKER P3/3. The terminal types `docker rm -f gateway` → TERM(port-laptop/41-rm-gateway.txt: 2),
then the README's five rows with `-p 127.0.0.1:8090:9100` and `-e PROCESSOR_PORT=9300` →
TERM(port-laptop/42-run-gateway-9300.txt: 6) (cut); `PROCESSOR_PORT=9300` highlights GREEN. V7: the
gateway's arrow re-aims at `:9300` and turns PINK; the street door slides back to `8090`.
PAGE(port-laptop/43-send-9300.txt) shows `processor listening on port 9300`; REPLY(port-laptop/43-send-9300.txt:
2) (wrap). A GREY chip "no rebuild · configuration only (README.md lines 404–409)".
SAY: The gateway's processor port. Remove the gateway and start it with 9300, back on 8090, and the message goes through. No image was rebuilt: it's only configuration.

SHOW: The two chips `PORT=9300` (processor) and `PROCESSOR_PORT=9300` (gateway) link with a GREEN
"=" sign; caption "the two settings must agree".
SAY: The two settings must agree: the processor's PORT and the gateway's processor port.

SHOW: TRACKER P3/4. It types `docker rm -f gateway processor` → TERM(port-laptop/44-rm-both.txt: 2–3)
and `docker network rm toynet` → TERM(port-laptop/45-network-rm.txt: 2); V6's boxes and rail dissolve.
TRACKER P3/4 · extra: `docker ps -a; docker network ls` (extra; typed as `docker ps -a` →
TERM(port-laptop/46-x-after-cleanup.txt: 2–3; wrap) and `docker network ls` →
TERM(port-laptop/46-x-after-cleanup.txt: 4–7)): only hello-world's exited container; no `toynet`. A
RED excerpt chip `Conflict. The container name "/processor" is already in use` (header
`port-laptop/68 · lines 8–9 (excerpt)`) with a GREY caption "if you skip this: Compose wants these
names". `▶ your turn`. Fade out.
SAY: Finally, clean up before Compose: remove both containers, then the network. An extra check shows only hello-world's old container left. Skip this, and Compose fails with a name conflict. Pause and clean up.

---

## S15 · Compose: the same app, declared — `s15_compose.py` · `ComposeUp`

SHOW: TRACKER P4/1. A one-line README chip `README.md · lines 432–446` "This is an excerpt, not the
complete file." V8 starts. Top band: Step 1's by-hand commands as GREY command chips (20 pt), one per
row: `docker network create toynet`, `docker build -t toy-processor ./processor`, `docker build -t
toy-gateway ./gateway`, `docker run -d --name processor --network toynet -e PORT=9200 toy-processor`,
`docker run -d --name gateway --network toynet -p 127.0.0.1:8090:9100 -e PROCESSOR_HOST=processor -e
PROCESSOR_PORT=9200 toy-gateway` (folded). Below: CODE(port_toy/docker-compose.yml: 12–23) (comment
cut; header `docker-compose.yml · lines 12–23 · comment cut`; if band and panel don't fit together,
the panel shows lines 12–18 first and scrolls to 19–23).
SAY: Step 4: Docker Compose. The README shows an excerpt; open the whole docker-compose.yml. Every flag you typed by hand has a home in it.

SHOW: Each flag lifts off its chip and flies to its YAML key, which highlights GREEN as it lands:
`--name gateway` → `container_name: gateway` (line 13); `docker build ./gateway` → `build: ./gateway`
(14); `-p 127.0.0.1:8090:9100` → `ports:` (15–16); `-e PROCESSOR_HOST=processor -e PROCESSOR_PORT=9200`
→ `environment:` (19–21); `--network toynet` → `networks:` (24, shown as a chip). The panel swaps to
CODE(port_toy/docker-compose.yml: 27–33) for the processor (its chips fly the same way: `--name`,
`build`, `-e PORT=9200`, `--network`), then CODE(port_toy/docker-compose.yml: 37–39), where
`docker network create toynet` lands on `name: toynet`.
SAY: Dash dash name becomes container name, and the build command becomes build. Dash p becomes ports, dash e becomes environment, and the network is named at the bottom of the file.

SHOW: Back on CODE(port_toy/docker-compose.yml: 12–23): two keys with no by-hand ancestor fade in with
GREEN outlines: `volumes:` / `- ./gateway:/app` (17–18, tag "live-mount the gateway's folder") and
`depends_on:` / `- processor` (22–23, tag "start the processor first"). Then the top band's five
chips collapse into one PURPLE chip: `docker compose up`.
SAY: Two keys are new: volumes mounts the gateway's folder into slash app, and depends on starts the processor first. All of step 1 collapses into one command: docker compose up.

SHOW: Terminal (full width, 14 rows, title `laptop`, prompt `student@laptop:~/AC215/port_toy$`). It
types `docker compose up` → TERM(port-laptop/47-compose-up.txt: 3, …, 21–24, …, 31, 39) (BuildKit
rows); `CACHED` rows GREEN; `naming to docker.io/library/port_toy-processor…` and `…port_toy-gateway…`
highlight, tag "folder name + service name". `▶ your turn`.
SAY: Run it. Compose builds both images, all from the cache, and names them after the folder and the service: port toy, dash gateway.

SHOW: The output continues: TERM(port-laptop/47-compose-up.txt: 43–51); `[+] up 5/5` highlights, each
`✔` row ticks in V6 (two images, the `toynet` rail, two boxes); lines 50–51 (the banners, prefixed
`processor  |` and `gateway    |`) highlight TEAL. The terminal keeps running (no prompt).
SAY: Then it creates the network and both containers, attaches to them, and prints both banners, each line prefixed with its service. Pause and run it.

SHOW: The first terminal shrinks to a strip at the bottom (still running). TRACKER P4/1:
PAGE(port-laptop/49-send-compose.txt) flashes in a small window (address `localhost:8090`) with
REPLY(port-laptop/49-send-compose.txt: 2) (README chip `README.md · line 460`). A second terminal
(title `laptop · second terminal`, 10 rows, same prompt) slides in above the strip. TRACKER P4/2: it
types `docker compose ps` → TERM(port-laptop/48-compose-ps.txt: 2–4; wrap), PORTS cell YELLOW.
TRACKER P4/2 · extra: `docker network ls` (extra) → TERM(port-laptop/50-network-ls-compose.txt: 2–6),
`toynet` TEAL, tag "created by Compose". TRACKER P4/2: `docker compose exec gateway curl
http://processor:9200/health` → TERM(port-laptop/51-compose-exec.txt: 2), `ok` GREEN, tag "no progress
meter: compose exec gives curl a terminal"; a GREY caption "the README's table writes curl ...: this is
step 2's command".
SAY: Open the page: it works. In a second terminal, docker compose ps shows the same mapping; an extra network ls shows Compose made toynet, and compose exec reaches the processor by name: ok.

SHOW: The README's comparison table (`README.md · lines 478–484`) as a two-column card, "By hand" |
"With Compose", rows writing in. The first terminal grows back: TERM(port-laptop/47-compose-up.txt:
52–54) appear under the banners (the page's POST and the health check).
SAY: The README's table pairs each by-hand command with its Compose version. Back in the first terminal, the requests you just made appear in the log.

SHOW: TRACKER P4/5. A key glyph `Ctrl` + `C` presses on the first terminal →
TERM(port-laptop/47-compose-up.txt: 55–61): `Gracefully Stopping...`, then `gateway exited with code
137`, then `processor exited with code 137` (both RED). A GREY stopwatch beside it runs to "≈ 20 s"
(Ctrl+C at 3.9 s, done at 24.3 s, capture-only timings). Above, V6: a polite GREY envelope "stop"
reaches the gateway box and is ignored (caption "Python is process 1"); a 10 s clock runs; a RED
"kill" stamp; then the same for the processor. Chip: "137 = 128 + 9: killed".
SAY: Now press Control C. Compose stops gracefully, and it takes about 20 seconds: Python, running as process 1, ignores the polite stop signal, so Docker waits 10 seconds per container, then kills it.

SHOW: The terminal returns to the prompt. It types `docker compose ps -a` →
TERM(port-laptop/52-compose-ps-a-stopped.txt: 2–4; wrap); both `Exited (137)` highlight; V6's boxes
turn GREY but stay, the rail stays.
SAY: Exit code 137 means killed. Docker compose ps dash a: both containers exited, but they're still there.

SHOW: It types `docker compose down` → TERM(port-laptop/53-compose-down.txt: 2–5) (V6's boxes and rail
dissolve) and `docker compose ps -a` → TERM(port-laptop/54-compose-ps-a-after.txt: 2) (just the header).
A one-line README chip `README.md · line 519` "Ctrl+C stops the containers but leaves them in place." `▶ your turn`. Fade
out.
SAY: Docker compose down removes the containers and the network, and ps dash a is empty. Control C stops; down removes. Pause, and run the whole cycle.

---

## S16 · Edit, apply, tear down, recap — `s16_recap.py` · `Recap`

SHOW: TRACKER P4/3. Terminal (full width, 12 rows, title `laptop`, prompt
`student@laptop:~/AC215/port_toy$`). It types `docker compose up -d` →
TERM(port-laptop/55-compose-up-d.txt: 2–5); the prompt returns at once (GREY tag "in the background").
SAY: Now in the background: docker compose up dash d starts the app and gives you your prompt back.

SHOW: TRACKER PH/2. It types `docker compose logs -f gateway` → TERM(port-laptop/56b-compose-logs-f.txt:
2–4) (line 3, the `POST` line, appears when a small PAGE window sends; `^C` ends it). TRACKER PH/3. It
types `docker compose exec gateway sh` → TERM(port-laptop/56d-compose-exec-sh.txt: 2–6; session) (prompt
`#`; `hostname`, `echo $PROCESSOR_HOST $PROCESSOR_PORT`, `exit` typed); `processor 9200` highlights PINK,
linked to `environment:` in a small CODE(port_toy/docker-compose.yml: 19–21) chip.
SAY: From the handy commands: compose logs dash f follows the gateway's log, and compose exec gateway sh opens a shell, where the environment shows processor and 9200.

SHOW: TRACKER P4/3 · extra. A one-line README chip `README.md · line 487` "repeat the port
experiments in docker-compose.yml". A pencil edits line 16 in a small editor panel; it types `git diff`
(extra) → TERM(port-laptop/57-x-edit-port.txt: 10–11) (cut). TRACKER P4/3. It types `docker compose up -d` →
TERM(port-laptop/58-compose-up-d-changed.txt: 2–4): `processor Running` GREEN, `gateway Started 10.5s`
YELLOW. In V8's coda the gateway box re-forms with a door `8095`, while the processor keeps glowing.
PAGE(port-laptop/59-x-send-8095-compose.txt) flashes on `localhost:8095`. Then the pencil changes it
back and it types `docker compose up -d` → TERM(port-laptop/60-compose-up-d-restored.txt: 2–4).
SAY: The README suggests repeating the port experiments in the file. Change 8090 to 8095 and run up dash d again: Compose recreates only the gateway, and the processor keeps running. Then change it back.

SHOW: TRACKER P4/4 · extra. A pencil adds a line to `processor/processor.py`; it types `git diff`
(extra) → TERM(port-laptop/61-x-edit-processor.txt: 10–11). TRACKER P4/4. It types `docker compose up
-d --build` → TERM(port-laptop/62-compose-up-d-build.txt: 3, …, 21–24, …, 43–47) (BuildKit rows); line
24 `[processor 4/4] COPY . .` (not CACHED) highlights YELLOW; line 46 `gateway Running` GREEN, line 47
`processor Started 10.4s` YELLOW.
SAY: If you change something copied into an image, like the processor's code, add dash dash build. Only the copy layer is new, and only the processor is recreated.

SHOW: Tag `illustration` ("what if"). CODE(port_toy/docker-compose.yml: 17–18) (comment cut) beside
CODE(port_toy/gateway/gateway.py: 20) `with open("index.html", "rb") as f:`; a pencil edits
`gateway/index.html` on the laptop, and the same file blinks inside the gateway's `/app` at once; a
browser reload shows the change. GREY caption "no rebuild".
SAY: The gateway's folder is mounted, and it reads its page on every request, so an edit to the page shows on the next reload, with no rebuild.

SHOW: TRACKER P4/5. It types `docker compose down` → TERM(port-laptop/64-compose-down-running.txt: 2–5)
(`Removed 10.2s` twice), `docker compose ps -a` → TERM(port-laptop/65-compose-ps-a-empty.txt: 2).
TRACKER P4/5 · extra: `docker image ls` (extra) → TERM(port-laptop/66-x-images-remain.txt: 2–8; column
view); `port_toy-*` and `toy-*` highlight, `198MB` each. A one-line README chip `README.md · line 515`
"The built images remain." A GREY note: "docker image rm <name> · if you want the space"; a GREEN
chip "port_toy costs nothing". `▶ your turn` beside `docker compose down`.
SAY: To finish, docker compose down, and ps dash a is empty. The images remain, about 200 megabytes each; remove them if you want the space. Nothing in port toy costs money. Pause and tear it down.

SHOW: The terminal fades. A card titled "Test yourself"; questions appear one at a time (each shrinks
upward as the next writes in), each with a small thumbnail of its picture playing one motion. Q1
"Which files define a mega-pipeline image? What does run use when there's no local image?"
(thumbnail: V1's signpost pointing at the 2025 box).
SAY: Five questions to test yourself. One: which files define a mega-pipeline image, and what does run use when there's no local image?

SHOW: Q2 "Which three gates must a call to your bucket pass, and where does each one fail?"
(thumbnail: V3's three gates). Q3 "How does a git-ignored key end up in an image? The fix?"
(thumbnail: V5's COPY packing the key).
SAY: Two: which three gates must a call to your bucket pass, and where does each one fail? Three: how does a git-ignored key end up in an image, and what's the fix?

SHOW: Q4 "In -p 127.0.0.1:8095:9100: which number does the browser use, which does gateway.py bind,
and what does 127.0.0.1 restrict?" (thumbnail: V7's door and room). Q5 "Inside the gateway, what is
localhost, and which name reaches the processor?" (thumbnail: V6's loop and phone book).
SAY: Four: in dash p 127.0.0.1, 8095, 9100, which number does the browser use, which does the gateway bind, and what does 127.0.0.1 restrict? Five: inside the gateway, what is localhost, and which name reaches the processor?

SHOW: The questions shrink to the top. A GREY dashed teaser (tag "L05 · llm-rag"): a TEAL box "CLI"
calls a TEAL box "ChromaDB" by name on a rail labelled "Compose network", with a GOLD key arriving
through a PINK `../secrets` route. Two footer cards: "Answers: exercises.md" and "Study guide + every
command: github.com/JunyiZhou-Conny/MLOps_Learning · guides/L04-containers-2b-flexible-workflow-ports.md".
Then everything fades to an empty frame (end of part 2).
SAY: Next lecture, a command-line container calls a database container by name, on a Compose network, with the same secrets mount: parts 1 and 2 together. Answers are in the exercises, and every command is in the study guide.
