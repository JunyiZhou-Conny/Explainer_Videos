# AC215 · Lecture 3 — Containers II: five containers, one bucket — narration script & visual plan (v1)

Audience: an AC215 student who has done L1 (a VM, venvs, uv) and L2 (a given Dockerfile, image vs
container, the layer cache, ENTRYPOINT + CMD, Docker Hub), with Docker Desktop and uv installed
(Tutorial 0). They watch with the mega-pipeline README and the `transcribe_audio` README open, a
clone of `dlops-io/mega-pipeline` on their laptop, the course key from Canvas and their team's group
name, pausing to type every command.

Goal: after the video they can draw the five-stage pipeline and say which bucket prefix each stage
reads and writes (and why `group_name` must match in every `cli.py`); write the component
Dockerfile from the README's pieces and say what each line is for; build and run it with
`-v "$(pwd):/app"` and say where each kind of state lives (image, the container's throwaway layer,
the laptop through the mount); run the `uv add` → exit → rebuild loop and say why packages vanish
without the rebuild; place the service-account key so the Google libraries find it and read a
`DefaultCredentialsError`; repeat the recipe for B–E; keep the key out of Git **and** out of the
image; clean up.

Sources of truth: `BRIEF.md` (design, binding), `digest.md` (tutorial digest), `assets/` (see
`ASSETS.md`). Where the digest and the captures disagree, the captures win (BRIEF.md's table).
Nothing in a terminal panel is typed by hand: every output line below names its capture file and
line numbers. v1 is the first draft, before the four review lenses.

Conventions
- `SAY:` lines are spoken verbatim by the TTS voice (one `voiceover` block each, 1–3 sentences,
  at most about 60 words) and become the subtitles. Plain spoken English: no backticks, no symbols;
  commands and paths are on screen and described in words ("dash dash r m", "slash app", "the dot
  venv folder"). File names with a lexicon entry (cli.py, pyproject.toml, uv.lock) are said as
  words; other folder names are said with spaces ("transcribe audio", "text prompts"). Numbers as
  digits; never a "!" after a digit. Versions that will change are said with "at the time of
  recording" (uv 0.13.0, Python 3.15.0, Docker Engine 29).
- Every spoken sentence starts with a capital letter or a digit (`explainer.voice.split_sentences`
  splits only there; the split drives the TTS gaps, the subtitle cues and the Chinese alignment).
  No sentence opens with a command or a lower-case file name. No `'s` on a word with a lexicon
  entry (`uv's` and `README's` exist and are used).
- `SHOW:` lines describe what is on screen during that `SAY:` line, and what moves.
- `PONDER(n s, "question")`: after that SAY block, `pause_and_ponder(self, "question", seconds=n)`
  (silent timer); the card is removed at the start of the next block, whose SAY gives the answer
  (in S14 the answer is shown by the next three blocks' captures). Five in the video (S02, S06,
  S07, S12, S14), as in BRIEF.md.
- `TERM(folder/file: lines)`: a terminal beat. The scene types the command written just before it
  in the SHOW line (in backticks, exactly as the README spells it; extras exactly as written here),
  then prints those lines of `assets/terminal/folder/file`. Line 1 of every capture is its `$ …`
  command and is never printed; the `[exit N]` line is never printed. In the line list: `…` = print
  one `…` line; `wrap` = fold long lines (`Terminal.print(..., wrap=True)`); without `wrap`, lines
  longer than a row are cut with `…`, which is what BuildKit's own view does. `→ (no output)`: the
  prompt simply returns.
- Captures whose `$` line joins commands with `;` (e.g. `laptop/14-host-after-uv-add.txt`) are
  typed as separate commands, each followed by its own lines of the file, as BRIEF.md allows; the
  SHOW line says which. Commands of that line that are not shown are simply not typed.
- Every build capture's `$` line has `--network host`: never typed, never shown. The scene types the
  README-derived `docker build -t <name> .`, and never prints a line that names the capture-only
  base (`load metadata for docker.io/l03-capture/…`, `[1/5] FROM docker.io/l03-capture/…`), the
  `transferring dockerfile` line or apt's `Get:` lines. The line lists below already leave them out.
- Terminal width. Every terminal is the house `term()` (12.6 wide, 22 pt, 65 characters a row),
  always full width. A typed command is never cut: it folds at a space onto an indented second row
  ending in ` \` (`Terminal.type`). When a picture needs the frame, the terminal shrinks to a 3-row
  strip along the bottom edge (the last command and its key output line). Never half width.
- Terminal titles: `laptop` while typing on the laptop; `container · transcribe_audio` (or the
  component's name) while inside a container, and the terminal's frame turns TEAL there.
- `CODE(path: a–b)`: `code_panel(...)` quoting `assets/source/path` from line a to b, header
  `path · lines a–b`; never more than 12 lines on screen. `PANEL(capture: lines, "header")`: the
  same look for a file or log shown from `assets/terminal/` (the student's Dockerfile in
  `files/`, a full build log), header as given. `files/transcribe_audio.Dockerfile` is the file
  the README has a student write; its panels are headed `transcribe_audio/Dockerfile · lines a–b`
  with the caption "from transcribe_audio/README.md · lines 41–90".
- `TRACKER A5` etc.: the `ReadmeTracker`, top-left in every walkthrough scene, moves to that step.
  Sections (step titles ≤ 3 words):
  - `R` = "Clone this Repository" (README.md:30–37), 2 steps: 1 Clone · 2 cd.
  - `A` = "transcribe_audio" (its README), 13 steps: 1 cd folder · 2 Key in secrets · 3 uv init ·
    4 Write Dockerfile · 5 Build image · 6 Run container · 7 uv add · 8 Group name ·
    9 Check --help · 10 Download · 11 Transcribe · 12 Upload · 13 Exit, rebuild.
  - `B` = "generate_text": the same 13, step 11 = Generate.
  - `C` = "synthesis_audio_en": 12 steps, the same without Upload (10 Download · 11 Synthesize ·
    12 Exit, rebuild).
  - `D` = "translate_text": the same 13, step 11 = Translate.
  - `E` = "synthesis_audio": as C, 12 steps.
  - `H` = "Push to Docker Hub" (optional, component READMEs `:136–140`), 3 steps: Login · Tag · Push.
  - `X` = "ElevenLabs bonus" (optional, `synthesis_audio/README.md:132–156`), 3 steps: Key file ·
    uv add requests · Run cli_11.
  `TRACKER A7 · extra`: same step, caption gets " · extra" while a command the README doesn't have
  is on screen. `TRACKER C1→C9` = the dots tick through quickly, one per typed command.
- `(extra)` after a command: not in the README. A small GREY tag `extra` sits beside the typed line,
  and the SAY says so ("an extra check", "not in the README") at least the first time.
- `▶ your turn`: a YELLOW tag beside the command at a real checkpoint (about one per README step);
  the SAY of that block says "pause". The video doesn't wait: the viewer pauses.
- Tags (GREY unless stated): `extra`; `illustration` on every schematic (the Canvas download, the
  bucket's sub-drawers, the leaderboard, "what if" pictures); `expected` on panels from
  `assets/terminal/expected/` (the README's own `--help` blocks for C, D, E);
  `recorded without the key` on the real runs that fail for lack of a key
  (`transcribe_audio/07`, `synthesis_audio_en/03`, `translate_text/03`, `synthesis_audio/03`,
  `synthesis_audio/05`); `at the time of recording` next to uv 0.13.0, Docker 29.8.2, CPython
  3.15.0 and the first package-version list; `stand-in file · not a real key` in S14; `erratum`
  on every README slip (the SAY says "a small mistake" or "a small slip", always with the fix);
  GOLD `billed to the course project` on every Google call.
- "What to look for" lists (Google calls that could not be recorded): a GREY caption card titled
  "with your key, look for", one short line per item, each citing the `cli.py` line that prints it.
  Never styled as terminal output, never in a terminal frame.
- The key is always a GOLD key glyph labelled `mega-pipeline.json`; its content is never drawn, and
  the stand-in file is never `cat`-ed. Docker Hub placeholders stay `<USER NAME>` / `<ACCESS TOKEN>`.
  `cli.py` line 17 (the project id) is never in a panel.
- Notes for scene authors. `Capture.pick()` indexes the output body, so pick index = file line − 1.
  `expected/*.txt`: line 1 is a `#` header (never printed), line 2 the `$` command, output from
  line 3. `transcribe_audio/01-docker-run-tty.txt` holds the prompts too (lines 2, 4, 6, 8, 10, 15
  are `app@5b4d4981ec25:/app$ <command>`): type each command at the drawn prompt and print only the
  output lines listed. All other in-container captures have no prompt: draw `app@5b4d4981ec25:/app$`.
  `transcribe_audio/06-group-name.txt` line 2 starts with grep's `21:`: as a code-panel "after",
  strip it and pass `first_line=21`. `laptop/17-history.txt`: never print lines 17–30 (the four
  capture-base rows and the base image's rows).
- Spelling on screen: American.
- Semantic colours (fixed for the whole video; series table applied, BRIEF.md):

  | meaning | colour |
  | --- | --- |
  | your laptop: the clone, the component folder, the files the bind mount shows inside | GREY |
  | Google Cloud: the bucket and its drawers, Speech-to-Text, Gemini, Text-to-Speech, Translation, IAM | BLUE |
  | containers and images: the five boxes A–E, the layer stack, the container's thin writable sheet (dashed) | TEAL |
  | the base image's system parts: Debian 12, apt packages (`build-essential`, `ffmpeg`), the image's Python 3.12 | ORANGE |
  | project-owned: `pyproject.toml`, `uv.lock`, `/home/app/.venv` and its packages, the `requires-python` interval | GREEN |
  | tools you install: uv (laptop and image), Docker | PURPLE |
  | errors, the key inside an image, "don't push this", the unchanged default group drawer | RED |
  | your turn, the README tracker, "look here now" | YELLOW |
  | money: "billed to the course project" tags; the service-account key glyph | GOLD |
  | lookups, paths, routes: the `-v` mount route, the `GOOGLE_APPLICATION_CREDENTIALS` signpost, object names `prefix/group/file` | PINK |

  Package chips are coloured by where they live (GREEN in the venv); a chip that lives only in the
  container's writable sheet sits inside the dashed TEAL sheet and evaporates with it.
- Visual set pieces V1–V8 are specified in BRIEF.md ("Visual set pieces"); SHOW lines below say
  which one, which state it is in, and what moves.
- Running example: the laptop is Debian 12 with Python 3.11.2, user `student`, host `laptop`:
  `student@laptop:~$`, `student@laptop:~/mega-pipeline$`,
  `student@laptop:~/mega-pipeline/transcribe_audio$` (and the other four folders). The container
  prompt is `app@5b4d4981ec25:/app$` (from `transcribe_audio/01-docker-run-tty.txt`), reused for
  every container. Group name `group-01` (the README's example). Images `transcribe_audio`,
  `generate_text`, `synthesis_audio_en`, `translate_text`, `synthesis_audio`.
- Length and parts: narration ≈ 4,250 words (BRIEF.md: 3,900–4,300, planned ≈ 4,170); part 1
  ≈ 1,915, part 2 ≈ 2,335. At the nominal 174 wpm that is ≈ 24.5 min of voice (the pilot measured
  ≈ 151 wpm for af_heart at 0.9, which would make it ≈ 28 min); typing, outputs and five ponder
  timers bring the video to ≈ 31–34 min. Part 1 = S01–S07 (the pipeline, and component A up to a
  running container that can't import yet), part 2 = S08–S15 (packages, the key, running A, B–E,
  secrets, teardown). Each part ends on an empty frame.

---

## S01 · Five containers, one bucket — `s01_hook.py` · `Hook`

SHOW: Black frame. V1 teaser, no labels yet: five TEAL boxes in a row along the top, a long BLUE
cabinet of seven drawers along the bottom (the seventh drawer dashed). A small waveform token
rises out of drawer 1 into box 1, comes out as a short page and drops into drawer 2; box 2 lifts it
and it lengthens into a long page that drops into drawer 3. There the page splits: one copy rises
through box 3 and falls into drawer 5 as a waveform; the other rises through box 4, turns into a
page with a small "FR" chip, drops into drawer 4, then rises through box 5 and falls into drawer 6
as a waveform. No arrow ever joins two boxes directly.
Then the picture dims, and two questions write in YELLOW above it, one after the other: "How do
they cooperate?" and "Who pays?".
SAY: A voice recording goes in on the left. Five programs, each in its own container, turn it into a longer podcast in English and in French, without ever sending each other a single message. So how do they cooperate, and who pays for what they use?

SHOW: The questions fade. A two-column card, headers "L2" (GREY) and "L3" (YELLOW). Four rows; as
each is said, its left cell transforms into its right cell: "a given Dockerfile" → "you write the
Dockerfile" · "one image" → "five images" (five small TEAL boxes) · "no mount" → "a bind mount
into your laptop" (a PINK route) · "no cloud" → "a shared bucket + a service-account key" (a BLUE
drawer and a GOLD key glyph).
SAY: Since last lecture, four things change: you write the Dockerfile, and you build five images, not one. A bind mount opens a window into your laptop, and the containers reach Google Cloud through a shared bucket and a service account key.

SHOW: A layout preview, built piece by piece as named: the ReadmeTracker appears top-left
("README › Clone this Repository", 2 dots) with a YELLOW circle pulsing around it; a code panel
slides in with header `transcribe_audio/cli.py · lines 18–21` (CODE(transcribe_audio/cli.py:
18–21)); a two-line terminal at the bottom (GREY tag "preview") shows
`git clone https://github.com/dlops-io/mega-pipeline.git` with a YELLOW `▶ your turn` tag, then
`ls` with the GREY `extra` tag.
SAY: To follow along, open the mega-pipeline README beside this video. The tracker, top left, shows the README step, and code panels show file and line numbers. Pause when the yellow your-turn tag appears; a grey extra tag marks a command that isn't in the README.

SHOW: The preview clears. A checklist card ticks GREEN line by line: "Tutorial 0: Docker Desktop +
uv" · "the course key, from Canvas" (GOLD key glyph) · "your team's group name". Footer caption:
"every command: MLOps_Learning · guides/L03-containers-2-mega-pipeline.md".
SAY: You'll need Tutorial 0 done, for Docker Desktop and uv, plus the course key from Canvas and your group name. Every command is also in the study guide, in the MLOps Learning repo.

SHOW: A GREY card: "recorded without the course key" → two lines: "Google calls: the command + what
to look for" and "no output panel". A BLUE cloud glyph behind it is dashed.
SAY: One honest limit: we recorded without a course key, so wherever the code talks to Google, you'll see the command and what to look for, not its output.

SHOW: A 3-row terminal strip at the bottom (title `laptop`, prompt `student@laptop:~$`) types
`docker version` (extra) → TERM(laptop/01-docker-version.txt: 2–3); `29.8.2` gets the tag
`at the time of recording`. A GREY caption above it: "Debian 12 · Python 3.11.2"
(laptop/00-laptop.txt lines 2, 6). Two small GREY chips: "macOS: zsh, %" and "Windows: Git BASH".
Fade out.
SAY: We recorded on a Debian 12 laptop with Docker Engine 29, at the time of recording. On a Mac or Windows your prompt differs and Docker Desktop runs the containers, but the commands are the same.

---

## S02 · The bucket is the message bus — `s02_bucket.py` · `BucketBus`

SHOW: No tracker (concept scene). A GREY README card, header `README.md · lines 60–67`, condenses
into two rows: top, "production: services call each other's APIs" with five TEAL boxes joined by
direct GREY arrows; the arrows fade and get a GREY cross. Bottom, "here: write outputs to shared
storage; the next stage reads them", with the same boxes over a BLUE cabinet.
SAY: In production, services call each other's APIs. This tutorial simplifies: each component writes its output to shared storage, where the next one reads it.

SHOW: V1 in full. The bottom cabinet's drawers get their labels from `README.md · lines 74–80`:
`input_audios/`, `text_prompts/`, `text_paragraphs/`, `text_translated/`, `text_audios/`,
`output_audios/`, and `output_audios_pp/` (dashed, small tag "bonus"). Tag `illustration` on the
cabinet. The boxes get letters and folder names: A `transcribe_audio`, B `generate_text`. The
token replays: from `input_audios/` up into A, down as a short page into `text_prompts/`; up into
B, down as a long page into `text_paragraphs/`.
SAY: That storage is one Google Cloud Storage bucket, drawn as a cabinet of drawers. A turns recordings from input audios into transcripts in text prompts, and B turns each transcript into a long article, in text paragraphs.

SHOW: Boxes C `synthesis_audio_en`, D `translate_text`, E `synthesis_audio` get their labels. The
long page splits: one copy up into C and down as a waveform into `text_audios/`; the other up into
D, down as a French page into `text_translated/`, up into E and down as a waveform into
`output_audios/`. Then the reads and writes fade in as thin arrows, every one between a box and a
drawer; a caption: "every arrow goes through a drawer".
SAY: From there the path splits. C turns the article into English speech, in text audios, while D translates it into French, in text translated, and E speaks the French, in output audios.

SHOW: A small GREY hand glyph taps A, then B, then C: "you run each one, by hand".
SAY: Notice that nothing triggers anything. You run each component yourself, in this order.

SHOW: Zoom into the `text_prompts/` drawer. A PINK object name writes across it:
`text_prompts/group-01/input-….txt`; its two slashes pulse; caption "one object name · no real
folders".
SAY: A bucket has no real folders: a name like text prompts, slash, group-01, slash, input dash something dot t x t is one single object name.

SHOW: CODE(transcribe_audio/cli.py: 108–112) at the top, full width: line 108's `"input-*.txt"`
and line 112's `os.path.join(text_prompts, group_name, filename)` highlight PINK, and line 112
links to the PINK object name. Then the panel swaps to CODE(generate_text/cli.py: 42), whose
`match_glob=f"{text_prompts}/{group_name}/input-*.txt"` highlights PINK and links to the same name.
SAY: Here's how A names its uploads: prefix, group name, file name, and only files starting with input. B downloads with the same pattern: that naming contract is the whole wiring.

SHOW: The `text_prompts/` drawer opens into sub-drawers `group-01/`, `group-02/`, `group-03/`, …,
and one labelled "default group" (tag `illustration`). A TEAL box with a GREY tag "group_name
unchanged" drops a page into "default group", which flashes RED. A GREY README card, header
`README.md · line 124`: "Set your group name inside cli.py before you run each component."
SAY: The group name keeps teams apart, and its default has no guard: a component you forgot to edit writes into the default group's drawer, maybe over someone else's work. Set it before every run.

SHOW: A schematic leaderboard (tag `illustration`; caption "ac215-mega-pipeline.dlops.io ·
README.md line 54"): rows `group-01`, `group-02`, `group-03`; columns Transcribe, Generate,
Synthesize EN, Translate, Synthesize FR; a few cells light up GREEN. A GOLD tag slides in over the
cabinet: "billed to the course project".
SAY: Each stage that succeeds lights up your row on a live leaderboard, and every call and every byte here is billed to the course's Google Cloud project, not yours.

SHOW: V1 full again, all labels on, arrows visible.
PONDER(8 s, "Look at which drawer each stage reads and writes.\nWhich two stages could run at the same time,\nand which one has to wait?")
SAY: Look at which drawer each stage reads and writes. Which two stages could run at the same time, and which one has to wait?

SHOW: C's and D's input arrows both pulse from `text_paragraphs/` (a YELLOW "side by side" bracket
over C and D); then E's input arrow pulses from `text_translated/`, D's drawer, with a small clock
glyph "waits for D". Fade out.
SAY: C and D both read only B's text paragraphs, so they could run side by side. E reads what D writes, so E has to wait for D.

---

## S03 · Clone: five folders, no Dockerfile — `s03_clone.py` · `CloneRepo`

SHOW: TRACKER R1. Terminal (full width, 12 rows, title `laptop`, prompt `student@laptop:~$`). It
types `git clone https://github.com/dlops-io/mega-pipeline.git` → TERM(laptop/03-clone.txt: 2).
`▶ your turn`. A GREY README card, header `README.md · lines 32–34`, flashes its clone line YELLOW:
"copy it from here".
SAY: The README's first section: clone the repo. Type git clone and the address, copied from the README, and pause to run it.

SHOW: TRACKER R2. It types `cd mega-pipeline` → (no output); the next prompt is
`student@laptop:~/mega-pipeline$` and its new path part flashes BLUE. TRACKER R2 · extra. It
types `ls; git log --oneline -1; git branch` (extra) → TERM(laptop/04-ls.txt: 2–11). The five folder names highlight GREY; line 10's `c6bbc9b` gets a
small GREY tag "the commit in this video"; line 11 `* main`.
SAY: Then cd mega-pipeline. An extra check, not in the README, lists the files and shows the commit: five component folders, on the main branch, at the commit this video was made from.

SHOW: It types `ls -a transcribe_audio generate_text synthesis_audio_en translate_text synthesis_audio`
(extra; folds onto a second row); the terminal prints `…` and shrinks to the bottom strip, and the
listing TERM(laptop/05-ls-components.txt: 2–42) is drawn above it as five GREY folder columns
(`file_tree`), in the order A–E: each shows `README.md`, `cli.py`, `secrets/` and, for four of them,
`.gitignore`. Under each column a dashed GREY ghost file `Dockerfile` with a YELLOW caption "you
write it" (`README.md · line 114`).
SAY: Another extra lists all five folders. Each has a README, a cli.py, and a secrets folder, and not one has a Dockerfile: the README says you write all five yourself.

SHOW: In the `generate_text` column, `pyproject.toml` and `main.py` highlight YELLOW and a dashed
gap where `.gitignore` would be gets a YELLOW tag "no .gitignore · keep in mind". In the
`synthesis_audio` column, `cli_11.py` gets a GREY tag "bonus".
SAY: Two differences to remember. The generate text folder already has a pyproject.toml and a main.py, but no dot gitignore file, and synthesis audio has a bonus script.

SHOW: The columns fade. The terminal grows back. The tracker switches section: "README ›
transcribe_audio", 13 dots. TRACKER A1. It types `cd transcribe_audio` → (no output); the prompt
becomes `student@laptop:~/mega-pipeline/transcribe_audio$`. `▶ your turn`.
SAY: Now the first component. The tracker switches to the transcribe audio README, whose step 1 is cd transcribe audio. Pause, and catch up to here.

SHOW: The terminal shrinks to the bottom strip. CODE(transcribe_audio/cli.py: 4–12) at the top,
full width. Lines 4–8 get a GREY side tag "comes with Python"; lines 9–11 a PINK side tag "where
from? · part 2", with `google.cloud` and `ffmpeg` turning PINK.
SAY: Open cli.py in your editor. The first imports come with Python, but the two Google Cloud modules and ffmpeg don't; where they come from is the second half of this video.

SHOW: The panel swaps to CODE(transcribe_audio/cli.py: 18–21). Line 18 (bucket) gets a BLUE tag
"the bucket", lines 19–20 a BLUE tag "its two drawers", line 21 `group_name` highlights YELLOW
with a tag "you'll change this".
SAY: Next come four settings: the bucket's name, the two drawers this stage uses, and on line 21 the group name, which you'll change soon.

SHOW: The panel swaps to CODE(transcribe_audio/cli.py: 118–126). Lines 121–126 get three numbered
YELLOW badges: 1 download, 2 transcribe, 3 upload. Fade out.
SAY: At the bottom, main runs up to three verbs, always in this order: download, transcribe, upload.

---

## S04 · The key, and uv init — `s04_setup.py` · `KeyAndInit`

SHOW: TRACKER A2. Schematic (tag `illustration`): a GREY card "course site · Files" (text only, no
logo) with a GOLD key glyph `mega-pipeline.json`; an arrow carries it into the GREY folder
`transcribe_audio/secrets/`. Then four copies fly into `generate_text/secrets/`,
`synthesis_audio_en/secrets/`, `translate_text/secrets/`, `synthesis_audio/secrets/`. A GREY README
card, header `README.md · lines 97–99`.
SAY: Step 2 is the key: a service account key file from Canvas, called mega-pipeline dot json. Put it in this folder's secrets folder, and a copy in each of the other four.

SHOW: The file name enlarges: `mega-pipeline.json` (GREEN check) above `mega-pipeline (1).json`
(RED cross, struck through), caption "exact name".
SAY: The name must be exact. If your browser saved it with a 1 in parentheses, rename it.

SHOW: Two GREY link cards side by side, tag `erratum`: left `README.md · line 99` "Canvas file
25687801" (GREEN check, "use this one"), right `transcribe_audio/README.md · line 17` "Canvas file
23163432" (GREY, "older"). A small GREY note: "how the code finds the key: part 2".
SAY: A small mistake to know about: the component READMEs link to an older Canvas file, so use the main README's link. How the code finds this key, and what happens when it can't, is part 2.

SHOW: TRACKER A3. Terminal (full width, 12 rows, title `laptop`, prompt
`student@laptop:~/mega-pipeline/transcribe_audio$`). A GREY README card, header
`transcribe_audio/README.md · lines 26–34`: "Don't have uv installed?". TRACKER A3 · extra. It
types `uv --version` (extra) → TERM(laptop/06-uv-missing.txt: 2), printed RED.
SAY: Step 3 uses uv, so first, an extra check that you have it. On a laptop without uv, the shell says command not found.

SHOW: TRACKER A3. It types `curl -LsSf https://astral.sh/uv/install.sh | sh` →
TERM(laptop/07-uv-install.txt: 2–6, …, 10) (no `▶ your turn`: only for viewers without uv).
`uv 0.13.0` gets the tag `at the time of recording`; a PURPLE `uv` chip drops into a folder glyph
`~/.local/bin`. Under the terminal, two GREY command chips (shown, not typed): `powershell -ExecutionPolicy ByPass -c "irm
https://astral.sh/uv/install.ps1 | iex"` "Windows (PowerShell)" and `pip install uv`
"alternative".
SAY: The README's note gives the installer: on macOS or Linux, this curl line, which installed uv 0.13.0 at the time of recording. On Windows, use the PowerShell line, or install it with pip.

SHOW: TRACKER A3 · extra. The terminal clears (a GREY caption "new terminal"; prompt
`student@laptop:~$`). It types `cd mega-pipeline/transcribe_audio` (extra) → (no output; the prompt
becomes `student@laptop:~/mega-pipeline/transcribe_audio$`), then `uv --version` (extra) →
TERM(laptop/08-uv-version.txt: 2).
SAY: Then restart your terminal, as the README says, cd back into transcribe audio, and uv answers.

SHOW: TRACKER A3. It types `uv init --bare` → TERM(laptop/09-uv-init.txt: 2). `▶ your turn`. A
GREEN file glyph `pyproject.toml` appears beside the terminal.
SAY: Now the step itself: uv init dash dash bare. It writes just one file, pyproject.toml, for a project named transcribe dash audio. Pause and run it.

SHOW: TRACKER A3 · extra. It types `cat pyproject.toml` (extra) → TERM(laptop/10-cat-pyproject.txt:
2–6). Line 6 `dependencies = []` gets a GREY tag "none yet"; line 5 `requires-python = ">=3.11"`
highlights YELLOW.
SAY: An extra look inside: a name, a version, an empty list of dependencies, and requires Python, 3.11 or newer.

SHOW: The terminal shrinks to the bottom strip. V7, first half: the number line 3.10 … 3.16. A GREY
dot "laptop · 3.11.2" drops onto 3.11; a GREEN interval grows from 3.11 to the right, labelled
`requires-python = ">=3.11"`. An ORANGE dot "image · Python 3.12" lands inside it with a GREEN
check.
SAY: That 3.11 comes from this laptop's own Python, 3.11.2. The image will have Python 3.12, inside that range, so all is well here.

SHOW: Tag `illustration` ("another laptop"). The GREY dot slides to 3.13; the GREEN interval's
start follows it; the ORANGE 3.12 dot is now outside and turns RED, and a dashed PURPLE download
arrow appears above the line (caption "preview: generate_text"). Then a GREEN edit chip
`requires-python = ">=3.12"` drags the interval's start back to 3.12; the ORANGE dot is inside
again. Caption: "your number depends on your laptop". Fade out.
SAY: Your number depends on your laptop. If yours says 3.13 or newer, the image's 3.12 falls outside, so edit it to 3.12 or newer; that fix isn't in the README, and generate text shows what happens without it.

---

## S05 · Write the Dockerfile, line by line — `s05_dockerfile.py` · `WriteDockerfile`

SHOW: TRACKER A4. A GREY README card, header `transcribe_audio/README.md · line 38`: "Notice:
there's no Dockerfile in this folder. You write it yourself, from scratch, piece by piece". V2
begins: an empty GREY editor tab `Dockerfile` on the left (6.6 wide), an empty slab area on the
right.
SAY: Step 4 is the heart of this lecture: there's no Dockerfile here, so you write it yourself, piece by piece.

SHOW: PANEL(files/transcribe_audio.Dockerfile: 1–3, "transcribe_audio/Dockerfile · lines 1–3")
types in on the left, caption "from transcribe_audio/README.md · lines 41–90". Line 1 `FROM
python:3.12-slim-bookworm` highlights; on the right an ORANGE base slab drops in, labelled
"Debian 12 + Python 3.12". A GREY note under the panel: "line 1: from the README's text, line 41".
SAY: Line 1 starts from the official Python 3.12 image on Debian 12; the README gives that name in its text, not in a code block.

SHOW: Line 3 `ARG DEBIAN_PACKAGES="build-essential ffmpeg"` highlights; a small ORANGE sticky note
"DEBIAN_PACKAGES · build time only" pins to the side of the stack (no slab). `ffmpeg` underlines;
a small CODE(transcribe_audio/cli.py: 67–69) inset slides in under the panel, line 69
`ffmpeg.run(stream)` highlighted, tag "runs the ffmpeg program".
SAY: Line 3 declares a build argument, the Debian packages to install: build essential and ffmpeg. We need the ffmpeg program, because the Python package ffmpeg dash python only runs that program.

SHOW: The panel swaps to PANEL(files/transcribe_audio.Dockerfile: 5–10, "transcribe_audio/Dockerfile ·
lines 5–10"). Six sticky notes pin to the side of the stack, one per line, no slabs. Lines 5–8
highlight together; their notes read "no apt questions", "Unicode text", "print at once", "uv
copies files".
SAY: Lines 5 to 10 set six environment variables, which pin notes on the image but add no layers. The first four: apt never asks questions, text is Unicode, Python prints at once, and uv copies package files instead of linking them.

SHOW: Line 9 `ENV UV_PROJECT_ENVIRONMENT=/home/app/.venv` highlights; its note turns GREEN and
grows: "the venv lives in /home/app/.venv · outside /app". A YELLOW tag: "remember this line".
SAY: Line 9 matters most: it tells uv to build the venv in slash home, slash app, slash dot venv, outside slash app. In a few minutes, this line saves us.

SHOW: Line 10 `ENV GOOGLE_APPLICATION_CREDENTIALS=secrets/mega-pipeline.json` highlights; its note
turns PINK, a small signpost glyph: "where the key is · a relative path". The `secrets/` at the
start of the value underlines PINK.
SAY: Line 10 tells Google's libraries where the key is: secrets, slash, mega-pipeline dot json, a relative path.

SHOW: The panel swaps to PANEL(files/transcribe_audio.Dockerfile: 12–21, "transcribe_audio/Dockerfile ·
lines 12–21"). The `&& \` at each line end pulses. One fat ORANGE slab drops onto the stack; inside
it, in order: small "apt lists" pages appear (line 12), packages fill in (lines 13–14), then the
pages crumple and vanish (lines 15–16), all inside the slab, never reaching the stack.
SAY: Lines 12 to 21 are one RUN instruction, chained with double ampersands, so they make one layer. It updates Debian, installs our packages, and deletes apt's package lists in that same layer, so they never take up space.

SHOW: Lines 17–18 highlight; a PURPLE `uv` chip drops into the slab beside a small ORANGE `pip`
chip. A GREY note: "this Python is the image's own (/usr/local), not Debian's → pip may install".
SAY: Then it upgrades pip and installs uv with it. Unlike Debian's system Python in lecture 1, this Python belongs to the image itself, so pip is allowed to install into it.

SHOW: Lines 19–21 highlight; a GREY user glyph "app · uid 1000" appears in the slab, and an arrow
"owns" points to a folder glyph `/app`. A GREY README card, header `transcribe_audio/README.md ·
line 72`: "Why a non-root user? Running containers as root is a security risk."
SAY: Last, it creates a user called app, with user ID 1000, who owns slash app; as the README explains, running a container as root is a security risk.

SHOW: The panel swaps to PANEL(files/transcribe_audio.Dockerfile: 23–30, "transcribe_audio/Dockerfile ·
lines 23–30"). Line 23 `USER app` pins a note; line 24 `WORKDIR /app` drops a hairline slab. Line
26 `COPY --chown=app:app . ./` drops a thin GREY slab holding small file glyphs (`cli.py`,
`Dockerfile`, `pyproject.toml`, `secrets/` with a tiny GOLD key, not commented on); "everything"
underlines YELLOW.
SAY: Lines 23 and 24 switch to that user and make slash app the working folder. Line 26 copies everything in this folder into the image; hold on to that word, everything.

SHOW: Line 27 `RUN uv sync` drops an empty GREEN slab "venv · /home/app/.venv". Lines 29–30 become
a label on top of the stack: "start: bash, venv on".
SAY: Line 27 runs uv sync to build the venv from pyproject.toml, and lines 29 and 30 start bash with the venv activated, as in lecture 2.

SHOW: The four panels shrink into one thumbnail of the whole file. Beside it a GREY card, header
`README.md · lines 175–225` "Appendix · Sample Dockerfile", with three lines picked out: `set -ex;`,
the man-page `for` loop, and line 179 `ARG DEBIAN_PACKAGES="build-essential curl"`, where `curl`
is RED with a tag "no ffmpeg".
SAY: The main README's appendix has a sample Dockerfile too, but its build argument has curl instead of ffmpeg, so don't paste it into transcribe audio.

SHOW: The thumbnail grows back into the full 30-line file at reduced size, line numbers visible.
`▶ your turn` beside the tab `Dockerfile`. Fade out.
SAY: Pause now, and write your Dockerfile, line by line.

---

## S06 · Build: five steps, one fat layer — `s06_build.py` · `BuildImage`

SHOW: TRACKER A5. A GREY README card, header `transcribe_audio/README.md · line 95`: "Build your
docker image and give your image the name transcribe_audio", tag `erratum` ("no command given").
Terminal (full width, 14 rows, title `laptop`, prompt
`student@laptop:~/mega-pipeline/transcribe_audio$`). It types `docker build -t transcribe_audio .`
but doesn't press enter. `-t transcribe_audio` gets a GREY label "the image's name"; the final `.`
gets a PINK label "this folder = the build context".
SAY: Step 5 builds the image, and the README has a small gap: it names the image, transcribe audio, but gives no command. Here it is: docker build, dash t and the name, then a dot for this folder, the build context.

SHOW: Enter is pressed → TERM(laptop/12-build.txt: 9, 23, …, 148–149, …, 1368, 1375, 1377). `▶ your
turn`. Line 23's `[2/5]` highlights YELLOW; `237 newly installed` and `205 MB` (lines 148–149)
underline ORANGE; `uv-0.13.0` (line 1375) PURPLE; `DONE 46.9s` YELLOW. A GREY note: "first build:
Docker also pulls python:3.12-slim-bookworm".
SAY: Pause and run it, and watch for the landmarks. Step 2 of 5 is our big RUN: apt installs 237 packages from a 205 megabyte download, then pip installs uv, all in 46.9 seconds. Your first build also downloads the Python base image.

SHOW: TERM(laptop/12-build.txt: 1379, 1382, 1385–1388, …, 1399, …, 1404–1405; wrap). `[3/5]`,
`[4/5]`, `[5/5]` highlight in turn; line 1386 `Using CPython 3.12.15 interpreter at:
/usr/local/bin/python3` underlines ORANGE; line 1387 `/home/app/.venv` GREEN; line 1388 `Resolved
1 package` gets a GREY tag "only the project itself".
SAY: Steps 3 and 4 set the working folder and copy our files. Step 5 runs uv sync with the image's own Python 3.12, creates the venv, and resolves 1 package: the project itself, since there are no dependencies yet.

SHOW: Line 1399 `naming to docker.io/library/transcribe_audio:latest` highlights GREEN; lines
1404–1405 (the `SecretsUsedInArgOrEnv` warning, `(line 10)`) highlight YELLOW, with a small
CODE-style inset of Dockerfile line 10 linked to it.
SAY: It ends by naming the image, and with a warning about secrets in an environment variable, pointing at line 10. Here the value is only a path, but remember that warning.

SHOW: TRACKER A5 · extra. The terminal clears and shrinks to the bottom strip. It types
`docker images transcribe_audio` (extra) → TERM(laptop/13-images.txt: 2–3); `1.35GB` highlights.
Above, V2 takes sizes: the apt RUN slab swells and reads `842MB` (`laptop/17-history.txt` line 9:
the same cached apt layer in every A build), the COPY slab stays thin, labelled "context 11.84kB"
(`laptop/12-build.txt` line 27; its 193kB of S11 includes `uv.lock`), the empty uv sync slab is a
hairline; the whole stack gets a brace "1.35 GB".
SAY: An extra check, docker images, says 1.35 gigabytes. Most of it is that one RUN layer, 842 megabytes of compilers, ffmpeg and their libraries, while the copied folder is tiny.

SHOW: Tag `illustration` ("what if"). A small RED-bordered panel, header "if you skipped uv init",
shows TERM(laptop/26-g21-no-pyproject.txt: 34, 51; wrap) in RED.
SAY: And if you skipped uv init, step 5 fails, because there's no pyproject.toml to sync.

SHOW: The panel fades. V2's five slabs get step badges [1/5]…[5/5]. A small GREY chip "edit:
group_name in cli.py" hovers beside the stack.
PONDER(8 s, "You change only group_name in cli.py\nand build again.\nWhich of the five steps run again?")
SAY: Something to ponder. You change only the group name in cli.py, then build again: which of the five steps run again?

SHOW: The chip drops into the COPY slab, which flashes YELLOW; the COPY slab and the uv sync slab
above it dissolve and re-form; slabs 2–3 get GREEN "CACHED" stamps and the base slab stays as is.
Caption: "part 2: for real".
Fade out.
SAY: Steps 4 and 5. The copied folder changed, so the copy runs again, and so does every step after it, uv sync included, while steps 1 to 3 come from the cache. We'll see it for real in part 2.

---

## S07 · Run: a window into your laptop — `s07_run.py` · `RunContainer`

SHOW: TRACKER A6. No terminal yet. V3 builds: the image as a TEAL block with an `/app` cavity
holding GREY copied files (`cli.py`, `Dockerfile`, `pyproject.toml`, `secrets/`), and a GREEN box
`/home/app/.venv` outside the cavity. A thin dashed TEAL sheet settles on top: "container =
image + a thin writable sheet".
SAY: Step 6 runs the image, so first, a picture. The copied files sit in slash app, the venv sits outside it in slash home, and a running container adds a thin writable sheet that dash dash r m throws away on exit.

SHOW: The laptop (GREY) appears at left with the folder `transcribe_audio/`. A PINK route labelled
`-v "$(pwd):/app"` runs from the laptop folder to the cavity; a GREY sheet carrying the laptop's
files slides along it and covers the cavity; the copied files dim underneath. Caption: "/app now
is your folder".
SAY: Dash v mounts the current folder, pwd, onto slash app: your folder slides over the copied files and hides them, so slash app is now your folder.

SHOW: A pencil glyph edits `cli.py` on the laptop: the same file inside the cavity blinks at once.
A small page written under `/app` travels the PINK route back to the laptop and stays (GREEN
check); a page written in `/tmp` lands on the dashed sheet (GREY "throwaway").
SAY: So your edits in VS Code show up inside at once, and anything written under slash app lands on your laptop and stays; anything written elsewhere lands on the throwaway sheet.

SHOW: Tag `illustration` ("lecture 2's layout: .venv next to the code"; L2's `Dockerfile.txt` had
no WORKDIR and activated `.venv` beside the copied code). The GREEN `.venv` box slides into the
cavity, under the laptop sheet, as `/app/.venv`.
PONDER(8 s, "In lecture 2 the venv sat right next to the code.\nIf it sat next to the code here, at /app/.venv,\nwhat would the container find there with this mount?")
SAY: Ponder this: in lecture 2, the venv sat right next to the code. If it sat next to the code here, in slash app, what would the container find there with this mount?

SHOW: The laptop sheet covers the `.venv` box completely; an arrow "activate" from the label on top
hits the sheet and turns RED: "no .venv on your laptop". Then the box slides back out to
`/home/app/.venv`, and Dockerfile line 9 (`ENV UV_PROJECT_ENVIRONMENT=/home/app/.venv`) appears
under it, GREEN.
SAY: It would find your laptop's folder, with no venv in it, so activation would fail. That's exactly what line 9, uv project environment, prevents.

SHOW: V3 shrinks to the upper half. Terminal (full width, 10 rows, title `laptop`, prompt
`student@laptop:~/mega-pipeline/transcribe_audio$`). It types
`docker run --rm -ti -v "$(pwd):/app" transcribe_audio`; small GREY labels pop under the parts:
`--rm` "delete on exit", `-ti` "interactive terminal", `-v "$(pwd):/app"` "the window", and the
image name. A GREY README card, header `transcribe_audio/README.md · line 99`. `▶ your turn`.
SAY: Type docker run, dash dash r m, dash t i, dash v with the mount, and the image name. Copy it from the README, quotes included, and pause to run it.

SHOW: The terminal's title becomes `container · transcribe_audio` and its frame turns TEAL; the
prompt `app@5b4d4981ec25:/app$` appears (transcribe_audio/01-docker-run-tty.txt line 2). `app`
gets a tag "user", `5b4d4981ec25` a tag "container id · yours differs", `/app` a PINK tag "the
window".
SAY: The prompt changes: you're user app, in slash app, and the part after the at sign is the container's ID, different on every run.

SHOW: TRACKER A6 · extra. It types `which python` (extra) → TERM(transcribe_audio/01-docker-run-tty.txt:
3), then `python --version` (extra) → TERM(transcribe_audio/01-docker-run-tty.txt: 5). A GREY
note: "no (transcribe-audio) in the prompt · the venv is active anyway".
SAY: No venv name shows in the prompt, yet the venv is active: two extra checks find python in slash home, version 3.12.

SHOW: It types `ls -a` (extra) → TERM(transcribe_audio/01-docker-run-tty.txt: 7); `Dockerfile`,
`pyproject.toml` and `secrets` highlight GREY, linked to the laptop sheet in V3. It types
`echo $GOOGLE_APPLICATION_CREDENTIALS` (extra) → TERM(transcribe_audio/01-docker-run-tty.txt: 9),
which links PINK to Dockerfile line 10.
SAY: Two more extras: listing the folder shows your laptop's files, and the key variable from line 10 is set.

SHOW: It types `python cli.py --help` (extra) → TERM(transcribe_audio/01-docker-run-tty.txt: 11–14);
line 14 `ModuleNotFoundError: No module named 'google'` prints RED.
SAY: Last extra: ask cli.py for its help. Module not found, no module named google: the packages aren't installed yet.

SHOW: The terminal shrinks to the strip. A GREY card "Windows" (from `README.md · lines 230–235`):
"Git BASH" · "quote "$(pwd)"" · "the input device is not a TTY → winpty", and the command chip
`winpty docker run --rm -ti -v "$(pwd)":/app generate_text` (shown, not typed).
SAY: On Windows, run these commands in Git BASH, keep the quotes around pwd, and if you see that the input device is not a T-T-Y, put winpty in front.

SHOW: V3 returns: the window works (PINK route lit), the GREEN venv box is empty, and a RED "?"
hovers between `cli.py` and a BLUE "google" chip. Caption: "Part 2: packages, and why they
vanish". Everything fades to an empty frame (end of part 1).
SAY: The container runs and sees your folder, but Python can't find Google. In part 2, we add the packages, and find out why they vanish.

---

## S08 · uv add: what lands where — `s08_uv_add.py` · `UvAdd`

SHOW: TRACKER A7. Terminal (full width, 14 rows, title `container · transcribe_audio`, TEAL frame,
prompt `app@5b4d4981ec25:/app$`), showing the last two lines of part 1
(transcribe_audio/01-docker-run-tty.txt lines 10 and 14, the second RED).
SAY: Welcome back. We're inside the transcribe audio container, and Python can't find Google's packages yet.

SHOW: A GREY README card, header `transcribe_audio/README.md · lines 104–110`, lists the three
packages. It types `uv add google-cloud-storage google-cloud-speech ffmpeg-python` (folds onto a
second row) → TERM(transcribe_audio/02-uv-add.txt: 2, 7–8, 9–13, …, 18–19, …, 34). `▶ your turn`.
The three asked-for names highlight GREEN in the `+` lines; the version list gets the tag
`at the time of recording`.
SAY: Step 7: the README lists three packages to add, so type all three in one uv add command. Pause and run it.

SHOW: A counter chip "asked for 3" transforms into "installed 26" (GREEN), pointing at line 8.
SAY: Three packages asked for, and 26 installed. As in lecture 1, each package brings its own dependencies, and uv resolves the whole tree.

SHOW: The terminal shrinks to the bottom strip. V3 + V4 above it: `pyproject.toml` (a GREEN list)
gains three lines and `uv.lock` (a GREEN scroll) unrolls, both on the GREY laptop sheet over
`/app`, and both copy along the PINK route onto the laptop; 26 small GREEN chips drop onto a GREEN
shelf in `/home/app/.venv`, which sits on the dashed TEAL writable sheet.
SAY: But where did everything land? The list, pyproject.toml, and the receipt, uv.lock, sit in slash app, so they're written to your laptop. The 26 packages went into the venv in slash home, on the container's throwaway sheet.

SHOW: TRACKER A7 · extra. The terminal grows back. It types `cat pyproject.toml` (extra) →
TERM(transcribe_audio/03-cat-pyproject.txt: 2–10); lines 7–9 highlight GREEN. Then `ls -la`
(extra) → TERM(transcribe_audio/04-ls.txt: 2–11); line 11 (`uv.lock`, `138445`) highlights GREEN
and its owner `app` underlines.
SAY: Two extra checks. The pyproject.toml now lists the three packages, each with a lower bound, and a new uv.lock of about 138 kilobytes sits next to cli.py, owned by user app.

SHOW: It types `which python` (extra) → TERM(transcribe_audio/10-venv-where.txt: 2), `echo
$VIRTUAL_ENV` (extra) → TERM(transcribe_audio/10-venv-where.txt: 3), and
`ls /home/app/.venv/lib/python3.12/site-packages | head -5` (extra) →
TERM(transcribe_audio/10-venv-where.txt: 4–8). `/home/app/.venv` underlines GREEN, with a tag
"outside the window".
SAY: Another extra: the venv is in slash home, slash app, outside the window, and its site-packages folder now holds the new packages.

SHOW: Two small cards at the right. Top: a GREEN chip `ffmpeg-python` with a check beside a GREY
chip `ffmpeg` with a cross, caption "different PyPI projects". Bottom, tag `extra` and "Linux,
folder not owned by uid 1000": TERM(transcribe_audio/13-g7-root-owned.txt: 4; wrap) in RED, and a
GREY note "Docker Desktop (macOS, Windows) handles this".
SAY: Two quick asides. The package is ffmpeg dash python; plain ffmpeg is a different project. And on a Linux laptop whose folder isn't owned by user ID 1000, uv add fails with permission denied, which Docker Desktop on Mac and Windows avoids.

SHOW: The README card `transcribe_audio/README.md · line 110` returns with "After exiting the
container, re-build the image" highlighted YELLOW; a small GREY tag "step 13".
SAY: The README adds one more thing here: when you exit, rebuild the image. We'll do that at the end, and see why.

SHOW: TRACKER A8. Beside the terminal strip, a GREY editor window titled "VS Code · on your laptop"
shows CODE(transcribe_audio/cli.py: 21); the string transforms into `"group-01"` (the "after" line
from transcribe_audio/06-group-name.txt line 2, prefix `21:` stripped, first line 21).
`▶ your turn`. A GREY note: "the same name in all five cli.py".
SAY: Step 8: set your group name. On your laptop, in VS Code, open cli.py and change line 21 to your team's name; ours is group-01.

SHOW: TRACKER A8 · extra. In the container terminal it types `grep -n "^group_name" cli.py` (extra) →
TERM(transcribe_audio/06-group-name.txt: 2); `group-01` highlights, and a PINK arrow runs from the
editor through V3's window to the terminal line.
SAY: Inside, an extra grep already shows the new line: the window works both ways. Use the same name in all five cli.py files, or the stages won't find each other's work.

SHOW: TRACKER A9. It types `python cli.py --help` → TERM(transcribe_audio/05-help.txt: 2–10).
Beside it, a GREY README card, header `transcribe_audio/README.md · lines 117–126`; the two blocks
match line for line (GREEN checks along the edge). `▶ your turn`. Fade out.
SAY: Step 9: python cli.py dash dash help. This time it works, and it matches the README's block line for line. Pause, and get to this point.

---

## S09 · Who is calling? The key and ADC — `s09_credentials.py` · `WhoIsCalling`

SHOW: TRACKER A10. Terminal (full width, 13 rows, TEAL frame, prompt `app@5b4d4981ec25:/app$`). A
GREY README card, header `README.md · line 134`, with a chip beside it "same as -d ·
transcribe_audio/README.md line 131". It types `python cli.py --download` →
TERM(transcribe_audio/07-download.txt: 2–3, …, 9–10, …, 22–23, …, 36; wrap); tag
`recorded without the key`; line 36 prints RED.
SAY: Step 10 downloads the recordings: python cli.py dash dash download, or dash d for short. Our machine had no key, so here's what a missing key looks like.

SHOW: Line 2 (`Args: Namespace(…)`) and line 3 (`download`) get GREEN checks, "printed before any
Google call"; line 36 `google.auth.exceptions.DefaultCredentialsError: File
secrets/mega-pipeline.json was not found.` highlights RED.
SAY: It printed the arguments and the word download, then a traceback. The last line says default credentials error: the file secrets, slash, mega-pipeline dot json was not found.

SHOW: A YELLOW eye glyph reads upward: line 9 `File "/app/cli.py", line 36, in download` → line 10
`client = storage.Client()` (YELLOW) → line 23 `_, project = google.auth.default()` (PINK) →
line 36 (RED). Three small labels: "our code", "the client asks", "google.auth looks for the file".
SAY: Read it as in lecture 1. Our code, at line 36, built a storage client, the client asked Google's auth library for credentials, and that library looked for a file that wasn't there.

SHOW: The terminal shrinks to the bottom strip. V5: inside a TEAL container outline, a small
machine `storage.Client()`. It asks a GREY box `google.auth` "who am I?". A PINK signpost planted
at `/app` reads `GOOGLE_APPLICATION_CREDENTIALS=secrets/mega-pipeline.json` (from Dockerfile line
10, a small tag).
SAY: Here's the chain when it works. Your code never passes the key: the client asks Google's auth library who it is, and the library reads the variable from line 10.

SHOW: `google.auth` follows the signpost from `/app` into `secrets/`, across V3's PINK window onto
the GREY laptop folder, and finds the GOLD key glyph `mega-pipeline.json`.
SAY: That variable is a signpost: secrets, slash, mega-pipeline dot json, starting from the current folder, slash app. Through the window, it leads to the key on your laptop.

SHOW: The key stamps out a GOLD token tag with a small clock ("short-lived"). A request arrow
carrying the token leaves the container toward a BLUE cloud "Google Cloud" on the right. A GOLD
tag on the arrow: "billed to the course project".
SAY: From the key, the library makes a short-lived access token, and every request to Google carries it.

SHOW: At the BLUE cloud, two gates in a row, from `README.md · lines 92–95`: gate 1 "authentication
· who is calling?" checks the token: "the course's service account" (GREEN check); gate 2, an
IAM padlock, "authorization · may it do this?", shows role tags and opens a BLUE bucket door.
SAY: Google then checks twice, as the README says. Authentication asks who is calling, and the key says it's the course's service account; authorization asks whether it may do this, and IAM roles open the bucket.

SHOW: Error branch: the signpost points into an empty GREY `secrets/` (no key) → line 36 in RED.
Then three causes appear as small cards, each animating the signpost: (1) "the key isn't in this
component's secrets/" (empty folder); (2) "you cd'd away from /app" (the signpost's root slides to
`/tmp` and points at nothing); (3) "docker run from the wrong folder" (the PINK window opens onto
`mega-pipeline/` instead of `transcribe_audio/`).
SAY: So this error has three usual causes. The key isn't in this component's own secrets folder, you changed directory away from slash app, or you ran docker run from the wrong folder on your laptop.

SHOW: TRACKER A10 · extra. The terminal grows back. It types
`ls -la input_audios text_prompts text_prompts/*` (extra) →
TERM(transcribe_audio/08-ls-after-download.txt: 2, …, 7, …, 11, 13); `group-01` highlights GREY,
and two empty GREY folder glyphs appear on the laptop in V3: `input_audios/`,
`text_prompts/group-01/`.
SAY: One extra check: even this failed run created two folders on your laptop, input audios, and text prompts with your group inside, because the code makes them before it builds the client.

SHOW: The terminal shrinks to the strip. CODE(transcribe_audio/cli.py: 32–43) at the top; lines
33–34 tag "clear, then make the folders", line 36 "the client: ADC", line 41 `print(blob.name)`
highlights. A caption card "with your key, look for" (no terminal frame): "download" (line 30) ·
"one object name per recording: input_audios/…" (line 41) · "the audio files in input_audios/
on your laptop" (line 43). GOLD tag "billed to the course project". `▶ your turn` (on the
README card). Fade out.
SAY: With your key in place, look for the word download, one object name per recording, and the audio files appearing in input audios on your laptop. Pause, put your key in secrets, and run it.

---

## S10 · Transcribe and upload — `s10_transcribe.py` · `TranscribeUpload`

SHOW: TRACKER A11. V8, Speech-to-Text half: a TEAL container on the left holding a GREY `input-….mp3`
page, a BLUE cloud "Speech-to-Text" on the right, the bucket drawers below. CODE(transcribe_audio/cli.py:
67–78) at the top; lines 67–69 highlight: the MP3 page passes through an ORANGE funnel "ffmpeg"
and comes out as a FLAC block.
SAY: Step 11 transcribes. For each recording, ffmpeg first converts the MP3 into FLAC, and that's why ffmpeg is in the build argument.

SHOW: Lines 71–72 and 75 highlight: the FLAC bytes ride inside the request arrow to the BLUE cloud.
Line 77 highlights: a ticket stub (TEAL outline) comes back at once; line 78 highlights: a ring
around the stub fills, labelled "up to 90 s". Then a transcript page returns to the container.
SAY: The audio bytes travel inside the request. Long running recognize hands back an operation at once, like a ticket stub, and its result call waits up to 90 seconds for the transcript.

SHOW: The panel swaps to CODE(transcribe_audio/cli.py: 84–91). Three short transcript strips snap
together into one page as line 90 `text = "".join(transcripts)` highlights; a GREY tag "the latest
commit's fix".
SAY: Long audio comes back in pieces, so lines 84 to 91 join every piece; that was the latest commit's fix.

SHOW: The panel fades. Terminal strip (TEAL frame, prompt `app@5b4d4981ec25:/app$`). A GREY README
card, header `README.md · line 135`, chip "same as -t". It types `python cli.py --transcribe` (no
output panel). A caption card "with your key, look for": "Transcribing: input_audios/…" (line 64)
· "ffmpeg's log" (line 69) · "response: …" (line 79) · "the transcript" (line 91) · "a new
text_prompts/group-01/input-….txt on your laptop" (line 95). GOLD tag "billed to the course
project".
SAY: Type python cli.py dash dash transcribe, or dash t. Look for transcribing and a file name, ffmpeg's log, the response, and the transcript itself.

SHOW: Tag `illustration` ("with your key"). In V3, a GREY page `text_prompts/group-01/input-….txt`
appears on the laptop and opens, its text shown only as grey bars. A small RED-bordered variant: the page reads `None`, with a pointer to CODE(transcribe_audio/cli.py: 80)
`text = "None"` and a GREY note "delete it, transcribe again".
SAY: Then open the new text file under text prompts, group-01, on your laptop. If it just says None, Speech-to-Text returned nothing, so delete it and transcribe again.

SHOW: TRACKER A12. A GREY README card, header `README.md · line 136`, chip "same as -u". It types
`python cli.py --upload`. CODE(transcribe_audio/cli.py: 104–115) at the top: line 108's
`"input-*.txt"` and line 112 highlight PINK; a caption card "with your key, look for":
"Uploading: text_prompts/group-01/input-….txt …" (line 114).
SAY: Step 12: python cli.py dash dash upload, or dash u. It uploads only files whose names start with input, to the same name in the bucket, so look for uploading, then text prompts, your group, and the file.

SHOW: V1 returns, small: the transcript token drops into `text_prompts/group-01/`; the schematic
leaderboard (tag `illustration`; caption "check: transcribe_audio/README.md · line 134") lights
the `group-01` × Transcribe cell. `▶ your turn` beside the three commands, listed together.
SAY: Your transcript drops into your group's drawer, and the transcribe cell lights up on the leaderboard, which is how the README says to check. Pause and run all three steps, with your key.

SHOW: A chip `python cli.py -d -t -u` (extra; not typed) with three small arrows to the three verbs
of CODE(transcribe_audio/cli.py: 121–126). The GOLD tag stays. Fade out.
SAY: An extra tip: the flags combine, so dash d, dash t, dash u in one command runs all three, in order. Each of these calls is billed to the course project.

---

## S11 · Exit, and bake it in — `s11_rebuild.py` · `BakeItIn`

SHOW: TRACKER A13. Terminal strip (TEAL frame) types `exit` → (the container ends; the title
returns to `laptop`, the frame to GREY, the prompt to
`student@laptop:~/mega-pipeline/transcribe_audio$`). Above, V3 + V4: the dashed
TEAL sheet evaporates, and the 26 GREEN chips on the venv shelf evaporate with it; the GREY laptop
folder keeps `pyproject.toml`, `uv.lock`, `input_audios/` and `text_prompts/`.
SAY: Step 13: exit, and rebuild. Type exit, and the container is removed with its throwaway sheet, and the 26 packages go with it.

SHOW: TRACKER A13 · extra. The terminal grows (13 rows). It types `ls -a` (extra) →
TERM(laptop/14-host-after-uv-add.txt: …, 8–12), `cat pyproject.toml` (extra) →
TERM(laptop/14-host-after-uv-add.txt: …, 17–21), `wc -c uv.lock` (extra) →
TERM(laptop/14-host-after-uv-add.txt: 35). The survivors highlight GREEN.
SAY: Back on the laptop, an extra check: the pyproject.toml with three dependencies, the lock file, and the two new folders all survived, because they were in the window.

SHOW: It types `git status --short` (extra) → TERM(laptop/14-host-after-uv-add.txt: 36); a GREY
tag "the rest is hidden from Git · S15".
SAY: Git status shows only cli.py as changed; we'll see why the rest is invisible at the end.

SHOW: The trap, tag `extra`. It types `docker run --rm -ti -v "$(pwd):/app" transcribe_audio`
(extra here: the image built in step 5); the frame turns TEAL, prompt `app@5b4d4981ec25:/app$`. It
types `python cli.py --help` (extra) → TERM(transcribe_audio/11-g10-new-container.txt: 2–5), line 5
RED. V4 above: a new dashed sheet on the old image, its venv shelf empty.
SAY: Now the trap, as an extra. Start a new container from the image you built earlier, ask for help again, and it's module not found once more, because the packages lived only in the old container.

SHOW: It types `exit` (the frame turns GREY). The README card `transcribe_audio/README.md · line 110`
("re-build the image"). TRACKER A13. It types `docker build -t transcribe_audio .` →
TERM(laptop/15-rebuild.txt: 3, 14–17). `▶ your turn`.
SAY: The README's fix: exit, and rebuild the image with the same docker build command. Pause and run it.

SHOW: `CACHED [2/5]` and `CACHED [3/5]` (lines 14–15) get GREEN stamps; `[4/5] COPY` and `[5/5] RUN
uv sync 2.9s` (lines 16–17) highlight YELLOW; `Building 9.9s` (line 3) underlines. Above, V2: slabs
2–3 stamped CACHED (the base slab is reused as is), the COPY and uv sync slabs dissolve and
re-form. A GREY tag "ponder 2".
SAY: Here's the ponder's answer, for real: steps 2 and 3 are cached, while step 4 copies the changed folder and step 5, uv sync, runs again. The whole build took under ten seconds.

SHOW: PANEL(laptop/15-rebuild.plain.txt: 30–33, 38–39, "the same build, full log · lines 30–39").
`Resolved 27 packages` and `Installed 26 packages` highlight GREEN; in V2 the uv sync slab fills
with 26 GREEN chips, carried in from the `pyproject.toml` list and `uv.lock` scroll that the COPY
slab brought in.
SAY: The full log shows what uv sync did this time: the copy brought in the lock file, and uv installed the same 26 packages, into the image.

SHOW: TRACKER A13 · extra. It types `docker images transcribe_audio` (extra) →
TERM(laptop/16-images-after.txt: 2–3), `1.48GB` highlights; then `docker history transcribe_audio`
(extra) → TERM(laptop/17-history.txt: 2–9, …, 16). Row 5 (`105MB`) GREEN, row 6 (`193kB`) GREY,
row 9 (`842MB`) ORANGE. V2's brace changes "1.35 GB" → "1.48 GB".
SAY: Two more extras. The image grew to 1.48 gigabytes, and docker history lists one row per Dockerfile line: the uv sync layer now holds 105 megabytes of packages, above the 842 megabyte system layer.

SHOW: It types `docker run --rm -ti -v "$(pwd):/app" transcribe_audio` (extra), then
`python -c "import google.cloud.storage, google.cloud.speech, ffmpeg; print(\"imports ok\")"`
(extra) → TERM(transcribe_audio/12-after-rebuild.txt: 2); `imports ok` GREEN. Then `exit`.
SAY: And a fresh container now imports all three packages with no uv add at all: they're baked in.

SHOW: V2 alone: an edit chip "group_name" drops into the COPY slab; the uv sync slab above it
dissolves and its 26 chips rain in again (the cache can't help). A GREY note: "later tutorials:
COPY pyproject.toml uv.lock first, then uv sync, then the rest". Fade out.
SAY: One thing to notice: because the copy comes before uv sync, any edit, even the group name, reinstalls every package on the next build. Later tutorials copy pyproject.toml and uv.lock first, to avoid that.

---

## S12 · generate_text: same recipe, two surprises — `s12_generate.py` · `GenerateText`

SHOW: The tracker switches section: "README › generate_text", 13 dots. TRACKER B1. Terminal (full
width, 12 rows, title `laptop`, prompt `student@laptop:~/mega-pipeline/transcribe_audio$`). It
types `cd ../generate_text` → (no output); the prompt becomes
`student@laptop:~/mega-pipeline/generate_text$`. TRACKER B2: a GOLD key glyph drops into a GREY
`secrets/` folder glyph beside the terminal (tag `illustration`).
SAY: Component B, generate text, follows the same recipe, so we'll go faster. Steps 1 and 2: cd into its folder, and copy the key into its secrets folder.

SHOW: TRACKER B2 · extra. It types `ls -a` (extra) → TERM(laptop/30-b-ls.txt: 2–8), then
`cat pyproject.toml` (extra) → TERM(laptop/30-b-ls.txt: 9–16); line 12
`requires-python = ">=3.14"` highlights YELLOW; lines 14–15 GREEN "already listed".
SAY: An extra look: this folder already has a pyproject.toml, with both packages listed, and requires Python 3.14 or newer.

SHOW: TRACKER B3. It types `uv init --bare` → TERM(laptop/31-b-uv-init.txt: 2; wrap), printed RED.
A GREY README card, header `generate_text/README.md · lines 20–24`, tag `erratum`, with a GREY
strike line and the note "skip it · main.py is a leftover".
SAY: Surprise one: uv init fails, because the project is already initialized. The README still says to run it, a small mistake, so skip step 3 and ignore the leftover main dot py file.

SHOW: TRACKER B4. PANEL(files/generate_text.Dockerfile: 3, "generate_text/Dockerfile · line 3")
`ARG DEBIAN_PACKAGES="build-essential"` slides in under A's line 3 (from
files/transcribe_audio.Dockerfile, with `ffmpeg` struck through); caption "the only difference ·
generate_text/README.md line 45".
SAY: Step 4 is the same Dockerfile, with one change on line 3: no ffmpeg, because this component never touches audio.

SHOW: TRACKER B5. It types `docker build -t generate_text .` → TERM(laptop/32-b-build.txt: 3,
14–17). `[2/5] … 22.8s` highlights ORANGE ("line 3 changed → not cached"); `[5/5] RUN uv sync
5.9s` highlights YELLOW.
SAY: Step 5 builds it, and the big RUN step runs again, since line 3 changed.

SHOW: V7 at the top, the number line 3.10 … 3.16: an ORANGE dot "image · Python 3.12" and a GREEN
interval from 3.14 labelled `requires-python = ">=3.14"`, the dot outside it. Three GREY answer
chips: "fail?", "use 3.12 anyway?", "something else?".
PONDER(8 s, "The image has Python 3.12.\nThis pyproject.toml says >=3.14.\nWhich Python will the venv use?")
SAY: Now ponder. The image has Python 3.12, and this pyproject.toml asks for 3.14 or newer: which Python will the venv use?

SHOW: The live view's line 17 `[5/5] RUN uv sync 5.9s` unfolds into
PANEL(laptop/32-b-build.plain.txt: 341–344, "the same build, full log · lines 341–344");
`3.15.0` gets the tag `at the time of recording`, `(35.9MiB)` underlines GREY.
SAY: The live view hides it, but the full log shows it: uv downloaded its own Python, 3.15.0 at the time of recording, and built the venv on that.

SHOW: V7: the ORANGE 3.12 dot turns RED, outside the interval; a PURPLE download arrow drops a
GREEN-ringed dot onto 3.15, labelled "3.15.0 · uv-managed · 35.9 MiB" and "the newest at the time
of recording".
SAY: On the number line, the image's 3.12 falls outside the interval, so uv fetched the newest Python in range, as you saw in lecture 2.

SHOW: TRACKER B6. It types `docker run --rm -ti -v "$(pwd):/app" generate_text` (TEAL frame,
prompt `app@5b4d4981ec25:/app$`). TRACKER B6 · extra. It types `python --version` (extra) →
TERM(generate_text/01-python-version.txt: 3), then `readlink -f $(which python)` (extra) →
TERM(generate_text/01-python-version.txt: 4; wrap); `/home/app/.local/share/uv/python/` underlines
PURPLE.
SAY: Step 6 runs it, and an extra check confirms it: Python 3.15.0, from uv's own folder, not the image's.

SHOW: TRACKER B7. It types `uv add google-cloud-storage google-genai` →
TERM(generate_text/02-uv-add.txt: 2–3). A GREY tag "nothing new: both already listed · writes
uv.lock".
SAY: In step 7, uv add finds nothing new, since both packages were already listed, so it only writes the lock file.

SHOW: TRACKER B8 → B9. A small editor inset shows CODE(generate_text/cli.py: 19), `group_name`
YELLOW ("line 19 here"). It types `python cli.py --help` → TERM(generate_text/04-help.txt: 2–10),
with a GREEN check "= generate_text/README.md · lines 116–124".
SAY: Steps 8 and 9: set the group name, here on line 19, and check the help, which matches the README.

SHOW: TRACKER B10 → B12. A GREY README card, header `README.md · lines 141–143`. The terminal
strip types the three commands, one after another, with no output: `python cli.py --download`,
`python cli.py --generate`, `python cli.py --upload`. CODE(generate_text/cli.py: 73–81) at the top:
line 73 (`GEMINI_MODEL`, default `"gemini-2.5-flash-lite"`) highlights, then line 75. A BLUE cloud
"Gemini · Vertex AI" with a GOLD tag "billed to the course project".
SAY: Steps 10 to 12: download, generate, upload. Generate sends each transcript to Gemini on Vertex AI, using Gemini 2.5 Flash Lite unless an environment variable names another model.

SHOW: A caption card "with your key, look for": "your prompt, printed" (line 74) · "Generated
text:" (line 80) · "a long article" (line 81) · "text_paragraphs/group-01/input-….txt on your
laptop" (line 84) · "Uploading: text_paragraphs/group-01/…" (generate_text/cli.py line 103).
`▶ your turn`.
SAY: Look for your prompt, generated text and a long article, then the upload. Pause and run all three, with your key.

SHOW: TRACKER B13. The terminal types `exit` (frame GREY, laptop prompt). An editor inset changes
`generate_text/pyproject.toml` line 4 to `requires-python = ">=3.12"` (GREEN; tag "the fix · not in
the README"). TRACKER B13 · extra. It types `grep -n requires-python pyproject.toml` (extra) →
TERM(laptop/34-b-fix-requires-python.txt: 2), then `git status --short .` (extra) →
TERM(laptop/34-b-fix-requires-python.txt: 3–5); `?? Dockerfile` gets a GREY tag "no .gitignore here".
SAY: Step 13, exit and rebuild, comes with the fix: edit requires Python to 3.12 or newer. Git status lists the Dockerfile too, since this folder has no dot gitignore.

SHOW: TRACKER B13. It types `docker build -t generate_text .` → TERM(laptop/35-b-rebuild-312.txt:
3, 14–17); `▶ your turn`; then PANEL(laptop/35-b-rebuild-312.plain.txt: 31, "full log · line 31")
`Using CPython 3.12.15 interpreter at: /usr/local/bin/python3` ORANGE. In V7, the interval's start
drags back to 3.12 and the ORANGE dot is inside again. It types
`docker run --rm -ti -v "$(pwd):/app" generate_text` (extra; TEAL frame), then
`python --version; readlink -f $(which python)` (extra) →
TERM(generate_text/05-python-version-312.txt: 2–3). Fade out.
SAY: Pause and rebuild: uv sync now uses the image's own Python 3.12, and so does the next container. Better still, make this fix before your first build.

---

## S13 · Synthesize, translate, synthesize — `s13_speed_round.py` · `SpeedRound`

SHOW: The tracker switches section: "README › synthesis_audio_en", 12 dots. TRACKER C1 → C3,
ticking per command. Terminal (full width, 12 rows, title `laptop`). It types
`cd ../synthesis_audio_en` → (no output; prompt `student@laptop:~/mega-pipeline/synthesis_audio_en$`);
a GOLD key glyph drops into a `secrets/` glyph (tag `illustration`); it types `uv init --bare` →
TERM(laptop/40-c-uv-init.txt: 2), then `cat pyproject.toml` (extra) → TERM(laptop/40-c-uv-init.txt:
3–7), line 6 `>=3.11` GREEN.
SAY: Now a speed round: C, D and E. For C, synthesis audio E-N, cd into it, copy the key, and run uv init, which stamps 3.11 or newer again.

SHOW: TRACKER C4. PANEL(files/synthesis_audio_en.Dockerfile: 3, "synthesis_audio_en/Dockerfile ·
line 3") `ARG DEBIAN_PACKAGES="build-essential"`. Two GREY README cards, tag `erratum`:
`synthesis_audio_en/README.md · line 38` "keep ffmpeg" (struck GREY) vs `· line 45` the ARG (GREEN
check, "right"). A GREY note: "neither synthesis cli.py uses ffmpeg".
SAY: A small slip: the README's text says to keep ffmpeg, but its code block leaves it out, and the code block is right: neither synthesis component uses ffmpeg.

SHOW: TRACKER C5. It types `docker build -t synthesis_audio_en .` → TERM(laptop/41-c-build.txt: 3,
14–17); `Building 0.6s` and `CACHED [2/5]` highlight GREEN. V2 at the top: B's stack with its
ORANGE apt slab; C's new stack forms beside it and points at B's slab instead of building its own
(a GREEN "shared" bracket), because the Dockerfile text up to line 21 is identical.
SAY: Build it: step 2 is cached and the build takes 0.6 seconds, because C's Dockerfile matches B's up to that line, so Docker reuses B's big layer.

SHOW: TRACKER C6 → C7. It types `docker run --rm -ti -v "$(pwd):/app" synthesis_audio_en` (TEAL
frame), then `uv add google-cloud-storage google-cloud-texttospeech` →
TERM(synthesis_audio_en/01-uv-add.txt: 2, 8).
SAY: Run it, and add storage and text to speech: 24 packages.

SHOW: TRACKER C8 → C9. A small editor inset: CODE(synthesis_audio_en/cli.py: 18), YELLOW. It types
`python cli.py --help` → TERM(synthesis_audio_en/03-help.txt: 2–4, …, 25; wrap); tag `recorded
without the key`; line 25 RED. Beside it, PANEL(expected/synthesis_audio_en-help.txt: 3–10,
"synthesis_audio_en/README.md · lines 116–123"), tag `expected`, "with your key".
Then V5 callback, small: the PINK signpost is consulted at the top of the file (an arrow from
`cli.py` line 22 to `google.auth`), before an `argparse` chip ever lights. The expected panel's
help text highlights.
SAY: Then a surprise: without a key, even help fails, because line 22 builds the Text-to-Speech client the moment the file is imported. With your key, you'd see the README's help text instead.

SHOW: V8, Text-to-Speech half: a TEAL container C on the left, a BLUE cloud "Text-to-Speech · long
audio" on the right, the drawers below. CODE(synthesis_audio_en/cli.py: 77–86) at the top: line 78
`output_gcs_uri = f"gs://{bucket_name}/{audio_blob_name}"` and line 85 highlight PINK. The request
carries a text page and a PINK address label to the cloud.
SAY: The request, lines 77 to 86, sends the text and an address in the bucket, and Google's long audio service writes the speech straight into text audios, never through your container.

SHOW: A ticket stub comes back to C, with a ring that fills, "up to 300 s"; meanwhile a waveform
crate travels from the BLUE cloud straight down into `text_audios/group-01/`. The panel swaps to
CODE(synthesis_audio_en/cli.py: 88–91), line 91 `print("Audio file will be saved to GCS bucket
automatically.")` highlights. A GREY README card `README.md · line 151`: "no separate --upload".
SAY: The container just holds a ticket stub for up to 300 seconds, then prints that the audio will be saved to the bucket. That's why C has no upload step.

SHOW: TRACKER C10 → C12. A GREY README card `README.md · lines 148–149`. It types
`python cli.py --download`, `python cli.py --synthesis` (no output; a GOLD tag "billed to the course
project"), then `exit`, then `docker build -t synthesis_audio_en .` →
TERM(laptop/42-c-rebuild.txt: 3, 14–17), `CACHED [2/5]` GREEN. `▶ your turn`.
SAY: So in C, pause to run download and synthesis, then exit and rebuild.

SHOW: The tracker switches: "README › translate_text", 13 dots. TRACKER D1 → D9, racing: a montage
in one terminal: `cd ../translate_text` → (a GOLD key glyph drops into `secrets/`) →
`uv init --bare` → TERM(laptop/50-d-uv-init.txt: 2) → (PANEL(files/translate_text.Dockerfile: 3,
"translate_text/Dockerfile · line 3") flashes by) → `docker build -t translate_text .` → TERM(laptop/51-d-build.txt: 3, 14) → `docker run --rm -ti -v
"$(pwd):/app" translate_text` → `uv add google-cloud-storage google-cloud-translate` →
TERM(translate_text/01-uv-add.txt: 2, 8) → (editor inset CODE(translate_text/cli.py: 18)) →
`python cli.py --help` → TERM(translate_text/03-help.txt: 2–4, …, 22; wrap) (tag `recorded without
the key`, line 22 RED) beside PANEL(expected/translate_text-help.txt: 3–11,
"translate_text/README.md · lines 116–124") (tag `expected`).
SAY: D, translate text, races through the same steps, with storage and translate as its packages; like C, it needs the key even for help.

SHOW: V8, Translation half: CODE(translate_text/cli.py: 58–65); lines 60–61 (`"en"` → `"fr"`)
highlight. The request goes to a BLUE cloud "Translation"; no stub: a French page (small "FR" chip)
comes straight back into D, line 65 `print(translated_text)` highlights, and the page is saved to
`text_translated/group-01/` on the laptop (line 68).
SAY: Translation is different: no ticket stub. The French text comes straight back, is printed and saved under text translated, so D needs an upload.

SHOW: TRACKER D10 → D13. A GREY README card `README.md · lines 155–157`. It types
`python cli.py --download`, `python cli.py --translate`, `python cli.py --upload` (no output; GOLD
tag), `exit`, `docker build -t translate_text .` → TERM(laptop/52-d-rebuild.txt: 3, 14–17).
`▶ your turn`.
SAY: Pause to run download, translate and upload, then exit and rebuild.

SHOW: The tracker switches: "README › synthesis_audio", 12 dots. TRACKER E1 → E9, montage:
`cd ../synthesis_audio` → (a GOLD key glyph drops into `secrets/`) → `uv init --bare` →
TERM(laptop/60-e-uv-init.txt: 2) → (PANEL(files/synthesis_audio.Dockerfile: 3,
"synthesis_audio/Dockerfile · line 3") flashes by) → `docker build -t synthesis_audio .` → TERM(laptop/61-e-build.txt: 3, 14) →
`docker run --rm -ti -v "$(pwd):/app" synthesis_audio` →
`uv add google-cloud-storage google-cloud-texttospeech` → TERM(synthesis_audio/01-uv-add.txt: 2, 8)
→ (editor inset CODE(synthesis_audio/cli.py: 18)) → `python cli.py --help` →
PANEL(expected/synthesis_audio-help.txt: 3–10, "synthesis_audio/README.md · lines 116–123") (tag
`expected`). Then CODE(synthesis_audio/cli.py: 105) appears under it, tag `erratum`: the
description `"Transcribe audio file to text"` RED beside the README's "Synthesis audio from text"
(expected panel line 5). In V1, a GREY "FR" voice chip on E: `fr-FR-Standard-C`.
SAY: E, synthesis audio, is C again, speaking the French text with a French voice. One harmless slip: its help text in the code says transcribe audio file to text, copied from A.

SHOW: TRACKER E10 → E11. A GREY README card `README.md · lines 162–163`. It types
`python cli.py --download`, `python cli.py --synthesis` (no output; GOLD tag).
SAY: Run download and synthesis with your key.

SHOW: The tracker switches: "README › ElevenLabs bonus" (tag "optional"), 3 dots. TRACKER X1: a
GREY file glyph `secrets/11lab_api_key.txt` with one line `XI_API_KEY=…` (from
`synthesis_audio/README.md · lines 139–142`; the value is never shown). TRACKER X2: it types
`uv add requests` → TERM(synthesis_audio/04-bonus-uv-add-requests.txt: 2–3); a GREY tag "already
installed · now listed". A small GREY note: "synthesis_audio_en/README.md mentions cli_11.py too ·
the file is in synthesis_audio/".
SAY: An optional bonus in E speaks the French with ElevenLabs, in the instructor's voice, on your own ElevenLabs key and quota: a key file in secrets, plus uv add requests.

SHOW: TRACKER X3. A GREY README card `synthesis_audio/README.md · lines 151–153`. It types
`python cli_11.py --download` → TERM(synthesis_audio/05-bonus-cli11-download.txt: 2–3, 6; wrap)
(tag `recorded without the key`, line 6 RED); CODE(synthesis_audio/cli_11.py: 30–39) slides in,
lines 33–37 highlighted "read at import". Then the chips `python cli_11.py --synthesis` and
`python cli_11.py --upload` (shown, not typed), with a GOLD tag "your own ElevenLabs quota".
SAY: Then run its three commands. Without the key file, even download fails, because the script reads that file at import.

SHOW: The tracker returns to "synthesis_audio", TRACKER E12: `exit`, `docker build -t synthesis_audio .`
→ TERM(laptop/62-e-rebuild.txt: 3, 14–17). `▶ your turn`. Then V1 fills: C, D and E light up,
pages and waveforms drop into `text_audios/group-01/`, `text_translated/group-01/` and
`output_audios/group-01/`, and the schematic leaderboard row `group-01` lights all five cells (tag
`illustration`). GOLD tags on C, D, E. Fade out.
SAY: Pause to exit and rebuild E. With all five done, your group's drawers fill across the bucket, and your leaderboard row lights up.

---

## S14 · Keep the key out of the image — `s14_secrets.py` · `KeepTheKeyOut`

SHOW: No tracker yet. V6: the GREY `transcribe_audio/` folder with a GOLD key in `secrets/`; on the
right, two destinations: a GREY book "Git history" and a TEAL shipping box "image", with a
"Docker Hub" shelf behind the box.
PONDER(8 s, "Your key is git-ignored.\nYou build the image and push it to Docker Hub.\nIs the key inside?")
SAY: Before we finish, a question about the key. It's git-ignored, so it never reaches GitHub, but now you build the image and push it to Docker Hub: is the key inside the image?

SHOW: The tracker returns: "README › transcribe_audio", TRACKER A13 · extra. Terminal (full width,
12 rows, title `laptop`, prompt `student@laptop:~/mega-pipeline/synthesis_audio$`). It types
`cd ../transcribe_audio` (extra) → (no output). A GREY tag on the folder: `stand-in file · not a
real key` (82 bytes, never opened). It types `ls secrets` (extra) →
TERM(laptop/20-g1-git-ignores-key.txt: 2), `git status --short` (extra) →
TERM(laptop/20-g1-git-ignores-key.txt: 3), and
`git check-ignore -v secrets/mega-pipeline.json` (extra) → TERM(laptop/20-g1-git-ignores-key.txt:
4). In V6, a sieve labelled `.gitignore` lowers over the book and catches the key
(CODE(transcribe_audio/.gitignore: 3) `/secrets`).
SAY: Let's test it, with an 82 byte stand-in for the real key. These extra Git commands show it's ignored, by line 3 of the dot gitignore file.

SHOW: It types `docker build -t transcribe_audio .` (extra here) → TERM(laptop/21-g1-rebuild-with-key.txt:
30–31). In V6 the whole folder pours into the box with no sieve; the key lands in V2's thin COPY
slab, now outlined RED. It types `docker run --rm --entrypoint ls transcribe_audio -la /app/secrets`
(extra) → TERM(laptop/22-g1-key-in-image.txt: 2–6); line 6 `mega-pipeline.json` RED.
SAY: Now rebuild, and list the secrets folder inside the image itself, with no mount. There it is: mega-pipeline dot json, inside the image.

SHOW: The `COPY --chown=app:app . ./` line (Dockerfile line 26) and the build's
`SecretsUsedInArgOrEnv` warning (laptop/12-build.txt line 1405) appear side by side, small; a
caption "Docker doesn't read .gitignore". A GREY README card, header `README.md · lines 103–106`,
tag `erratum`: "we've already added a .gitignore entry so the file won't be pushed accidentally"
→ caption "protects Git only".
SAY: Docker doesn't read dot gitignore: the copy line takes the whole build context, and the build's secrets warning was a hint. So here's a small mistake in the README's secrets note: it relies on dot gitignore, which protects Git only.

SHOW: The fix, tag `extra` "recommended". It types `cat .dockerignore` (extra) →
TERM(laptop/23-g1-dockerignore.txt: 2), with a GREY note "create it with one line: secrets/".
`▶ your turn`. In V6 a second sieve, `.dockerignore`, lowers over the box.
SAY: The fix is an extra we recommend: a dot dockerignore file, in the component folder, containing secrets. Pause and add one.

SHOW: It types `docker build -t transcribe_audio .` → TERM(laptop/24-g1-rebuild-dockerignore.txt:
12–13, …, 30–31), `load .dockerignore` highlights; then
`docker run --rm --entrypoint ls transcribe_audio -la /app/secrets` (extra) →
TERM(laptop/25-g1-key-not-in-image.txt: 2), GREEN. In V6 the folder pours in again; the key is
caught by the second sieve; the COPY slab is clean.
SAY: Rebuild, and list again: cannot access, no such file or directory. The key stayed out of the image.

SHOW: V3 returns, small: `docker run --rm -ti -v "$(pwd):/app" transcribe_audio` brings the laptop
sheet with `secrets/` and its GOLD key over `/app` at run time; the PINK signpost finds it.
SAY: And the run still works, because the mount brings your secrets folder in when the container starts.

SHOW: The tracker switches: "README › Push to Docker Hub" (tag "optional"), TRACKER H1 → H3. A GREY
README card `transcribe_audio/README.md · lines 136–140`. Three command chips, shown, not typed:
`docker login -u <USER NAME> -p <ACCESS TOKEN>`, `docker tag transcribe_audio <USER
NAME>/transcribe_audio`, `docker push <USER NAME>/transcribe_audio`. Over them, the V6 box slides
toward the Docker Hub shelf and stops under a RED stamp "without .dockerignore: would publish the
key"; beside it a GREEN tag "only after the .dockerignore fix".
SAY: The README's optional last section pushes your image to Docker Hub: log in, tag, push. Only ever push an image built with that dot dockerignore.

SHOW: The `-p <ACCESS TOKEN>` part of the login chip gets a YELLOW underline and a GREY note "stays
in your shell history"; a GREEN chip below: `docker login -u <USER NAME>` "paste the token at the
prompt". A RED card: "pushed one with the key? delete it · tell the staff".
SAY: Log in with just your user name and paste the token at the prompt, since a token after dash p stays in your shell history. And if you ever pushed an image with the key, delete it and tell the staff, so the key can be replaced.

SHOW: Coda. CODE(solution-branch/transcribe_audio/docker-shell.sh: 8–10) then
CODE(solution-branch/transcribe_audio/docker-shell.sh: 95–100), header `transcribe_audio/docker-shell.sh ·
lines 95–100 · solution branch`, caption "last year's solution branch: not today's steps". Line 98
`-v "$SECRETS_DIR":/secrets` highlights; in V6 the `secrets/` folder slides out of the repo, beside
it, and a second PINK route runs from it to `/secrets` in the container. Fade out.
SAY: Where the course is heading: last year's solution kept the secrets folder outside the repo, and mounted it into the container at slash secrets at run time. That way, no key ever enters the image.

---

## S15 · Clean up, recap, and what's next — `s15_recap.py` · `Recap`

SHOW: No tracker (a GREY caption top-left: "after the README · clean up"). V1 zooms out: the five
boxes and the cabinet, small; a checklist card: "cloud: nothing to delete" with three GREY
sub-items "no VM · no bucket · no service account", and "your outputs stay in the bucket, under
group-01".
SAY: Time to clean up. In the cloud there's nothing to delete: you created no machine, bucket or account, and your outputs stay in the bucket.

SHOW: Terminal (full width, 12 rows, title `laptop`, prompt `student@laptop:~/mega-pipeline$`).
It types `docker image ls --filter reference=transcribe_audio --filter reference=generate_text
--filter reference=synthesis_audio_en --filter reference=translate_text --filter
reference=synthesis_audio` (extra; folds onto three rows) → TERM(laptop/70-images-all.txt: 2–7);
`1.48GB` and the four `84xMB` sizes highlight.
SAY: Locally, an extra command lists the five images: transcribe audio at 1.48 gigabytes, and the other four at about 845 megabytes each.

SHOW: It types `git status` (extra) → TERM(laptop/71-git-status.txt: 5–9, 11–14). Lines 8–9 and
13–14 highlight; four GREY ghost chips appear beside them, struck through: "the other four
Dockerfiles, pyproject.toml, uv.lock". CODE(transcribe_audio/.gitignore: 5–7) slides in.
SAY: To keep your work, check Git. An extra git status shows your edited cli.py and generate text's files, but the other four folders hide their Dockerfiles and project files from Git.

SHOW: Tag `erratum`. A GREEN chip `git add -f` beside the ghosts (they turn solid GREY), and a RED
lock on `/secrets` (CODE(transcribe_audio/.gitignore: 3)): "keep ignoring this".
SAY: In your own repo, add those files with git add dash f, and never stop ignoring secrets.

SHOW: It types `docker image rm transcribe_audio generate_text synthesis_audio_en translate_text
synthesis_audio` (extra; folds onto two rows) → TERM(laptop/72-cleanup.txt: 2–11). `▶ your turn`.
In V1, the five TEAL boxes dissolve; the cabinet stays.
SAY: Then pause, and remove the five images with docker image rm, another extra; every run used dash dash r m, so no containers are left.

SHOW: A card titled "Test yourself"; questions appear one at a time (each stays, smaller, as the
next appears), each with a small thumbnail of its set piece: Q1 "Which prefix does translate_text
read, and which stage wrote it?" (V1) · Q2 "Why doesn't the mount hide the packages? What breaks
without UV_PROJECT_ENVIRONMENT?" (V3).
SAY: Five questions to test yourself. One: which drawer does translate text read, and who wrote it? Two: why doesn't the mount hide the packages, and what breaks without uv project environment?

SHOW: Q3 "After uv add in a --rm container: what survives, what is lost, what makes it permanent?"
(V4) · Q4 "Which variable tells the libraries where the key is, and why only from /app?" (V5) · Q5
"How can an image contain a git-ignored key? The fix?" (V6).
SAY: Three: after uv add in a throwaway container, what survives, what's lost, and what makes it permanent? Four: which variable points to the key, and why only from slash app? Five: how can an image hold a git-ignored key, and what's the fix?

SHOW: The questions shrink to the top. Two footer cards: "Answers: exercises.md" and "Study guide +
every command: github.com/JunyiZhou-Conny/MLOps_Learning · guides/L03-containers-2-mega-pipeline.md".
A "Next: L4" card: "your own bucket + service account · the key outside the repo · docker-shell.sh
builds and runs for you" (branch `flexible-workflow`). Everything fades to an empty frame (end of
part 2).
SAY: The answers are in the exercises, and every command is in the study guide. Next lecture: your own bucket and service account, the key outside the repo, and a script that builds and runs each container for you.
