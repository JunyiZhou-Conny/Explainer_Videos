# AC215 · Lecture 9 — CI & unit testing: who gets to say no before a commit? — narration script & visual plan (v1)

Audience: an AC215 student who has done L1–L4 (a VM, venvs and uv, Docker images and containers —
the `docker-shell.sh` / entrypoint pattern returns here) and can run Docker Desktop. They have
never written a pytest test, run black or flake8 deliberately, or installed a git hook. They watch
with their own clones of `dlops-io/cheese-app-ci-cd` and (part 2) `rahuldave/babykev` open,
pausing to type every command. Nothing in this lecture needs GCP, credentials or any paid service.

Goal: after the video they can say what runs in a unit, an integration and a system test of this
repo, file by file, and why the first two are hermetic and the third is not; run the app and the
three suites inside the Docker image and explain why an edit on the host changes nothing until a
rebuild; read a pytest run (discovery rules, `pytest.raises`, `-ra`'s summary, why
`1 passed, 4 skipped` is not the same green as `5 passed`); explain what black fixes and what
flake8 can only report, and why every command must carry the same width (120) as the hook and CI;
install pre-commit, survive "files were modified by this hook", and show a commit being refused;
describe babykev's gate (one lockfile, one command `just check`, a coverage floor, config linting);
explain why 94% coverage proved nothing about `branch_mask` and how a hypothesis property test
shrank the counter-example; put non-hermetic tests behind a marker instead of a silent `skipif`.

Sources of truth: `BRIEF.md` (design, binding), `digest.md` (tutorial digest), `SLIDES.md`
(lecture-slide digest), `assets/` (see `ASSETS.md`). Where the digest or the slides and the
captures disagree, the captures win. Nothing in a terminal panel is typed by hand: every output
line below names its capture file and line numbers.

Conventions
- `SAY:` lines are spoken verbatim by the TTS voice (one `voiceover` block each) and become the
  subtitles. Plain spoken English: no backticks, no symbols, no parentheses; commands and paths are
  said in words ("docker run, dash dash rm", "tests slash unit", "dot git slash hooks slash
  pre-commit"). File and tool names written as they are and said by lexicon entries
  (`explainer/lexicon.yaml`, "# AC215 L09"): pytest, uvicorn, flake8, pre-commit, ruff, ty,
  hadolint, yamllint, hypothesis, babykev, justfile, utils.py, service.py, pytest.ini,
  conftest.py, docker-entrypoint.sh, docker-shell.sh, cheese-app-ci-cd, cheese-app-api,
  api-server, pyproject.toml, uv.lock, Dockerfile, F401, E501, and the versions said in this
  script (0.13.2, 1.59.0, 3.13.16, 2.14.1, 4.7.0, 26.10.1, 7.4.1, plus the two-part numbers 3.9,
  5.0, 7.07, 0.77, 49.4). Any new `a.b.c` version needs its own entry. "dash a" is always followed
  by a comma or a full stop. No sentence opens with "Ours". Numbers as digits, sizes with their
  unit; never a "!" after a digit. Versions, counts with warnings, timings and reclaimed sizes are
  said with "at the time of recording". The babykev step tags are spoken as words ("step zero
  zero", "step five a") while the screen shows `step-00`, `step-05a`.
- Every spoken sentence starts with a capital letter or a digit (`explainer.voice.split_sentences`
  splits only there; the same split drives TTS gaps, subtitle cues and the Chinese alignment). No
  sentence opens with a command or file name ("The command docker build…", "Then pytest…").
- `SHOW:` lines describe what is on screen during that `SAY:` line, and what moves.
- `PONDER(n s, "question")`: after that SAY block, `pause_and_ponder(self, "question", seconds=n)`
  (silent timer); the card is removed at the start of the next block. Five in the video (BRIEF).
- `TERM(folder/file: lines)`: a terminal beat. The scene types the command written just before it
  in the SHOW line (in backticks, exactly as the README/walk spells it; extras exactly as written
  here), then prints those lines of `assets/terminal/folder/file`. Line 1 of every capture is its
  `$ …` command and is never printed; the `[exit N]` line is never printed. Inside the line list:
  - `…` = print one `…` line;
  - `wrap` = fold long lines (`Terminal.print(..., wrap=True)`): the pip and pre-commit warnings,
    the `SKIPPED …` summary lines, the coverage `Missing` columns;
  - `squeeze` = a table re-aligned with two-space gutters, an empty trailing column dropped;
  - `[y/N] y` = cut that line after the bracket, pause 0.6 s, type the answer;
  - `→ (no output)`: the prompt simply returns.
- Typed lines at a container prompt. The `istep` captures (`laptop/part1-01`, `laptop/part3-opt3-01`)
  hold the prompt and the typed line together (`app@44b7ce455073:/app$ uvicorn …`). The scene sets
  the terminal's prompt to the capture's own `app@<id>:/app$` and types the rest of that line, so
  prompt and command are the capture's text. Every run the viewer does ends with a spoken "type
  exit" (or control C) before the next laptop command.
- Terminal size: the house `term()` (12.6 wide, 22 pt, 65 characters a row, full width). A typed
  command is never cut: it folds at a space onto an indented row. When a picture needs the frame,
  the terminal shrinks to a 3-row strip along the bottom edge (the last command and its key line);
  a full terminal and a picture never share the frame. Coverage tables and the `docker image ls`
  table keep their columns (`squeeze` where needed); highlight by substring.
- `CODE(path: a–b)`: `code_panel(...)` quoting `assets/source/path` from line a to b, header
  `path · lines a–b`; never more than 12 lines on screen at once. History files are under
  `cheese-app-ci-cd-history/` and `babykev-history/` with the sha in the name; their headers say
  so (`c3b227f · service.py · lines a–b`). A "README card" is a GREY quote of README text with the
  header `README.md · line n`.
- `TRACKER A3`: the `ReadmeTracker`, top-left, in every walkthrough scene, moves to that step.
  `TRACKER A3 · extra`: same step, caption gets " · extra" while a command the README/walk doesn't
  have is on screen. Six trackers (BRIEF):
  - A = "Part 1: Understanding the Codebase" (`README.md:19-93`), 5 steps: 1 Clone ·
    2 docker-shell · 3 Start server · 4 Browser checks · 5 Exit.
  - B = "Part 2: Identifying Code Quality Issues" (`README.md:96-127`), 6 steps: 1 Build image ·
    2 flake8 (Option A) · 3 black --check (Option A) · 4 pip install (Option B) · 5 flake8 local ·
    6 black local.
  - C = "Part 3: Testing with Pytest" (`README.md:130-230`), 10 steps: 1 Build · 2 Unit tests ·
    3 Integration tests · 4 Both · 5 Coverage · 6 Start server (Opt 2) · 7 System tests ·
    8 Clean up · 9 Interactive shell (Opt 3) · 10 Tests inside.
  - D = "Part 4: Automating with Pre-commit Hooks" (`README.md:233-275`), 5 steps: 1 Install
    pre-commit · 2 pre-commit install · 3 git commit · 4 run --all-files · 5 pre-commit run.
  - E = "babykev walk (walk.md, steps 00–05b)", 8 steps: 1 step-00 env · 2 step-01 tests ·
    3 step-02 format+lint · 4 step-03 the hook · 5 step-04/04b docs · 6 step-05 the model ·
    7 step-05a properties · 8 step-05b marker+images.
  - F = "Docker Cleanup" (`README.md:568-574`), 3 steps: 1 container ls · 2 system prune ·
    3 image ls.
  S02, S03 and S06 are concept scenes with no tracker; S01 has none until the preview.
- `(extra)` after a command: not in the README/walk. A small GREY tag `extra` sits beside the
  typed line, and the SAY says so at least the first time that kind of command appears (`git log`,
  `ls`, the readiness wait, `docker ps`, `git diff`/`git add`, the blocked-commit demo,
  `pre-commit uninstall`, the uv/just installs).
- `▶ your turn`: a YELLOW tag beside the command at a real checkpoint (about one per README step);
  the SAY of that block says "pause". The video doesn't wait: the viewer pauses.
- Tags (GREY unless said): `illustration` on the schematic browser (no screenshots, no logos);
  `recorded · walk.md` (`recorded_tag()`) on every number that comes from the walk's own record
  and not from a capture (the image sizes 1.15/1.84 GB, the `--network none` green check, "103
  passed" at steps 05a/05b); `at the time of recording` beside versions, warning counts, timings
  and reclaimed sizes when first shown; `erratum` on every README/walk slip (the narration says "a
  small slip" or "a small gap", never "erratum"). `expected` is not needed: this episode invented
  no expected panels.
- A SKIPPED or deselected test is a GREY dashed dot — never GREEN, never counted as passed. The
  system-test row never sits inside the hermetic border.
- `lecture_ref(9, "a–b")` (GREY, top right): one per scene as assigned in the BRIEF; spans from
  SLIDES.md. Lecture diagrams are redrawn in series style; no slide images, memes or photos.
- Spelling on screen and in the subtitles: American ("gray", "behavior").
- Semantic colours (BRIEF, fixed for the whole video):

  | meaning | colour |
  | --- | --- |
  | your laptop: the clone, the working tree, the staging area, the host shell | GREY |
  | remote things: GitHub, the CI runner (L21, dashed), the Hugging Face Hub | BLUE |
  | images and containers: `cheese-app-api:local`, the baked-in code slabs, babykev's dev/run images (said, recorded) | TEAL |
  | system-wide / host-owned: host pip installs, the host PATH | ORANGE |
  | project-owned, isolated, hermetic: the venv `uv sync --locked` builds, `uv.lock`, the tiny model, the dashed hermetic border, passing checks | GREEN |
  | tools: pytest, black, flake8, pre-commit, uv, just, ruff, ty, hypothesis, docker, hadolint | PURPLE |
  | errors and refusals: failing tests, F401/E231/E303/E501, the wrong mask cells, "Failed", an aborted commit, the failed coverage floor | RED |
  | your turn, the README tracker, the gate-table row being filled now | YELLOW |
  | money: nothing billable this lecture (GOLD unused on screen) | GOLD |
  | lookups and routes: the request token's path, the network wire to port 9000 | PINK |
  | future things (CI/L21, L10 credentials) and skipped/deselected tests | GREY, dashed |

  Episode-local semantics: test kinds are coloured by what runs — unit GREEN (one function, fully
  ours), integration TEAL (our parts in-process, `TestClient` / the tiny model), system BLUE (the
  real thing over the network). The hermetic border is a GREEN dashed box; whatever stands outside
  it (the live server, the Hub, the real model) is drawn outside.
- Running example. The laptop: user `student`, prompts `student@laptop:~$` /
  `student@laptop:~/cheese-app-ci-cd$`, terminal title `laptop` (the captures' fresh Docker 29.8.2
  engine stands in for Docker Desktop; host pip is a Python 3.14.8 virtualenv standing in for a
  laptop Python that allows `pip install` — on a Homebrew Mac it refuses with
  `externally-managed-environment`, so one spoken caveat lands at S05 B4 and a GREY remedy chip
  at S09 D1 (`pipx install pre-commit`), per the BRIEF). Inside the cheese container the prompt is
  each capture's own (`app@<id>:/app$`); S04 says once that the id changes every run and that
  `app` is not root. The babykev laptop: prompts `student@laptop:~$` / `student@laptop:~/babykev$`,
  terminal title `laptop · babykev` (a fresh Debian 12 container without Docker stands in).
- The gate table (V1's running fixture): four columns — what is checked / how / command / on every
  commit? — opened empty in S03, filled row by row (tests S07, system tests S08 "no: not hermetic",
  format+lint S09, babykev's docs/config rows S11, types S13, complete in S14). Current row
  YELLOW; non-hermetic rows GREY dashed, outside the turnstile.
- Length and parts: narration 4,300 words (`python -m explainer.script`, which counts words;
  its minute figure assumes 155 wpm and is ignored; part 1 = 2,578, part 2 = 1,722). At Kokoro
  af_heart speed 0.9 (≈174 wpm raw, ≈150 wpm with sentence gaps) that is ≈28.5 min of
  narration, ≈30–32 min with typing, outputs and ponder timers.
  Part 1 = S01–S09 (the cheese tutorial, ending on a refused commit), part 2 = S10–S15 (the
  guest lecture). Each part ends on an empty frame.

Notes for scene authors
- TERM/PANEL line numbers are *file* lines (line 1 = the `$` command); `Capture.pick()` indexes
  the output body, so pick index = file line − 1.
- Never print `[exit N]` lines. Never print the `python:3.11-slim-bookworm` row of
  `laptop/clean-03` (capture-only base image, ASSETS.md); builds show no base-pull rows. The
  `s05a-03`/`s05b-03` failure lines are printed only in S13's and S14's platform beats, nowhere
  else; any "103 passed" claim carries `recorded · walk.md`.
- Long lines fold with `wrap`: pip's download rows, pre-commit's `[WARNING]`, the `SKIPPED …`
  summary lines, the coverage `Missing` columns, BuildKit's `RUN set -ex; …` rows.
- The `istep` captures hold whole interactive sessions; pick line ranges per typed command.
- Shared code (`scenes/common.py`, started from L02's): tracker factories `tracker_a` …
  `tracker_f` with the step lists above; prompts `P_LAPTOP_HOME`, `P_LAPTOP` (cheese clone),
  `P_BABYKEV`; tags `extra_tag`, `illustration_tag`, `recorded_tag`, `your_turn`. Set pieces:
  `GateTable` + `Turnstile` (V1), `TestPyramid` + `HermeticBorder` + `RequestToken` (V2),
  `Collector` + `FixtureWiring` (V3), `RibbonFunnel` (V4), `HandoverChain` (V5), `MaskGrid` (V6),
  L02's `LayerStack` reused small (V7).
- Never: slide images or memes; logos; a real person's name on screen (narration credits "Rahul
  Dave's guest lecture" once, S10); hand-typed output; a command spelled differently from the
  README/walk; "the hook runs the tests" about the cheese repo; "integration tests need running
  services"; calling the cheese Dockerfile multi-stage; a SKIPPED dot in green; presenting the
  bit-exactness failure as babykev's bug or the student's mistake; credentials that look real
  (the `.env` demo content stays `X=1`).

---

## S01 · Who gets to say no? — `s01_hook.py` · `Hook`

SHOW: Black frame, no tracker. CODE(cheese-app-ci-cd-history/c3b227f-service.py: 38–50), header
`c3b227f · service.py · lines 38–50`; line 44 `result = math.sqrt(2 * z)` glows RED, the
docstring's `sqrt(x^2 + y^2)` (line 40) stays WHITE above it. A GREY chip beside the panel:
"committed live, in class" (source `cheese-app-ci-cd-history/git-log-oneline.txt`).
SAY: Here is a line of code that a Harvard instructor committed, live, in class. The distance from a point to the origin is the square root of x squared plus y squared. This line takes the square root of twice that. Nothing crashed; the app started fine. The answer was just wrong.

SHOW: The panel dims. V1 teaser: a GREY envelope "your commit" slides toward a vault door labelled
"HISTORY"; an unlabeled turnstile of empty scanner arches drops between them and the envelope stops.
A GREY label "a gate" fades onto the turnstile exactly on the spoken word "gate". GREY tag
`Lecture 9 · slides 41, 98–99` (top right, until the checklist).
SAY: You type git commit. Before that commit exists, who gets to say no, and what can they actually catch? The lecture has a word for whoever can say no: a gate, anything that can fail and stop you. Today we build one on your machine, and watch it refuse a commit.

SHOW: The turnstile shrinks to a corner. A grid of 26 GREY tiles (slides 4–6 redrawn, no tag of its
own): 9 tiles light GREEN "data and model", the rest stay GREY with the caption "engineering".
SAY: Step back once: in a machine learning system, the model is a few tiles in a big grid; the rest is engineering. Today is that engineering: tests, formatters, linters, and the hook that runs them.

SHOW: A checklist card: "✓ your clone of cheese-app-ci-cd", "✓ Docker Desktop running",
"✓ Python 3.9 or newer", and GREEN "✗ no cloud, no credentials, no bill".
SAY: To follow along you need your own clone of cheese-app-ci-cd, Docker Desktop running, and Python 3.9 or newer. No cloud, no credentials, no bill: everything runs on your laptop, which is the point.

SHOW: Layout preview, built as named: `tracker_a(1)` appears top-left with a YELLOW ring ("README ›
Part 1: Understanding the Codebase", 5 dots); the ring cycles the six tracker titles A–F as "six
sections" is said. A 2-row strip terminal (GREY tag "preview", prompt `student@laptop:~$`) types
`docker container ls` with a YELLOW `▶ your turn` row tag; once that clears, `ls -la` with the GREY
`extra` row tag (the two tags appear one after the other, never stacked). No footer caption: the
study-guide pointer lives in S15's outro. Fade out.
SAY: The tracker in the top left shows which README step we are on; 6 sections today: 4 from the cheese README, 1 for the guest lecture, 1 for cleanup. When the yellow your-turn tag appears, pause and run the command. A gray extra tag marks a check not in the README. Every command is in the study guide, linked below.

---

## S02 · The bug that almost shipped — `s02_bug.py` · `BugAlmostShipped`

SHOW: No tracker (concept scene). The repo's history as a GREY commit chain, drawn from
CODE(cheese-app-ci-cd-history/git-log-oneline.txt: 1–8), oldest left, newest right, under a small
GREY time arrow pointing right: `91eb786` "readd messy code" → `c2dce32` "with wrong variable"
(RED dot) → `8eb63fc` "fixed the a problem" → one GREY ellipsis dot (the three omitted commits
`1a5e363`, `199abd9`, `3dea317`) → `c3b227f` "demo class 1" (RED dot, the sqrt bug) → `b8458ff`
"demo class 1" (the revert, GREEN, HEAD). GREY tag `Lecture 9 · slides 25, 27–28` (top right,
whole scene). Under it a 3-row strip terminal types `git log -1 --format='%H %ci'` (extra) →
TERM(laptop/02: 2).
SAY: The bug is real history. This repo's own log tells the story: messy code re-added on purpose, then a crash, then a fix. Then the class demo slipped the wrong square root in, and the revert took it out. An extra git log confirms the clone sits at that last commit, from November 2025.

SHOW: The chain fades. A plane with the point (3, 4); a GREEN radius sweeps to a circle of radius 5,
label "5". A RED arrow overshoots the circle to length √50, label "√50 ≈ 7.07". No error icon
anywhere: a GREY caption "no crash · just wrong".
SAY: Picture the point 3 comma 4. Its true distance from the origin is 5, the radius of this circle. The buggy line returns the square root of 50, about 7.07: it overshoots the circle. No crash, no error message, only a wrong number.

SHOW: CODE(cheese-app-ci-cd/tests/integration/test_api.py: 31–38); line 38
`assert data["distance"] == 5.0` highlights GREEN. The RED arrow from the plane bounces off the
panel.
SAY: One existing test already knew the right answer. It asks the app for the distance of 3 comma 4 and insists on exactly 5.0. A test is an executable specification, and this one would have said no before anyone saw the demo.

SHOW: A card with two suspects: a TEAL chip "the code" and a GREEN chip "the test"; a YELLOW arrow
stamps "fix this" on the code chip. GREY caption "slide 28: when a test fails, fix the code".
SAY: When a test fails, there are two suspects, the code and the test. The lecture's rule: first believe the test, and fix the code. Rewriting the test to match a bug turns your specification into a diary.

SHOW: Three trays slide in (slide 25 redrawn): "normal", "edge", "invalid". Chips drop in as named:
`power(2, 3)` into normal; `0`, `inf`, `nan` into edge; then
CODE(cheese-app-ci-cd/tests/unit/test_utils.py: 69–76) appears above the invalid tray and a chip
`power("3", 4)` drops in. Fade out.
SAY: What is worth testing? The lecture sorts inputs into three trays: normal, edge, and invalid. For the power function here, 2 to the power 3 is normal; zero exponents, infinity and not a number are edges. And for invalid input, pytest dot raises inverts the test: it passes only if power on a string raises a type error.

---

## S03 · Three kinds of test, and a gate — `s03_kinds.py` · `ThreeKinds`

SHOW: No tracker. V2: a glowing PINK token `GET /euclidean_distance/?x=3&y=4` at top. Unit beat:
a small `power()` chip visibly detaches from the handler box; then the camera zooms to a GREEN box
holding only `power(3, 2)`; the token shrinks to just the numbers 3 and 2 entering it, a GREEN
check pops out. GREY tag `Lecture 9 · slides 66, 95` (top right, whole scene).
SAY: Now the lecture's vocabulary, on one request: get euclidean distance, with x 3 and y 4. Inside the handler, squaring x is one call, power of 3 and 2. A unit test skips the app entirely and calls that one function alone. It is fast, and when it fails you know where to look.

SHOW: Integration beat: a TEAL box `TestClient` wraps the FastAPI router, handler and a small
`power()` chip; the token passes straight in with no wire, bounces through "routing → validation →
handler → power", and exits as a JSON chip. Caption "in-process · no socket".
SAY: An integration test wires several of our parts. The test client hands the request straight to the FastAPI app, in process: routing, validation, handler and power all run, but no server and no network. Ten of those run here in under a second, at the time of recording.

SHOW: System beat: the token leaves a BLUE test box, travels a PINK wire to "port 9000" on a second
BLUE box "the running server", and returns `{"distance": 5.0}`.
SAY: A system test treats the running program as a black box. The request leaves the test, crosses a real network wire to port 9000, and comes back as JSON. It is the most honest test, and the slowest and most fragile.

SHOW: The three boxes stack into the README's pyramid: wide GREEN base "unit · many, fast", TEAL
middle, narrow BLUE top "system · few, slow".
SAY: Stacked, that is the testing pyramid: many cheap unit tests at the bottom, few expensive system tests on top.

SHOW: The pyramid re-draws as nested boxes and a GREEN dashed border closes around the unit and
integration boxes; the system box sits half outside, its wire crossing the border.
SAY: The lecture adds a sharper lens: a border. A test is hermetic when only your code can make it fail. Unit and integration tests live inside that border. The system test crosses it: a live server can be down for reasons that are not your bug.

SHOW: Two faint extra rows under the pyramid: "smoke · does it answer at all" and "acceptance ·
none yet". Then two cards side by side, tag `erratum`:
CODE(cheese-app-ci-cd/tests/system/test_system_api.py: 1–4) with line 2 "Integration tests" struck
YELLOW and "system" written above it, and CODE(cheese-app-ci-cd/pytest.ini: 19–23) with a GREY
caption "markers defined, never used".
SAY: Two more kinds get faint rows: a smoke test, which only asks whether it answers, and acceptance tests, which this project lacks, for now. One note about kinds: a test's kind is named by what runs, not by its folder. This repo's system test file calls itself integration tests, and its pytest config defines markers, labels for selecting tests, that nobody uses; markers return in part 2.

SHOW: The cards fade. V1: the gate table slides in, empty, four column headers lit YELLOW in turn:
"what is checked" · "how" · "command" · "on every commit?". It shrinks to its resting place. Fade
out.
SAY: Last picture: an empty table, four columns. What is checked, how, with which command, and does it run on every commit. Part 1 fills it in.

---

## S04 · Clone, and run the app — `s04_run_app.py` · `RunTheApp`

SHOW: TRACKER A1 (the tracker appears: "README › Part 1: Understanding the Codebase", 5 dots, a
YELLOW pulse). Full-width laptop terminal (title `laptop`, prompt `student@laptop:~$`). A README
card (`README.md · line 20`): "Clone or download from your repository", GREY caption "the README
gives no address; this is the repo". It types
`git clone https://github.com/dlops-io/cheese-app-ci-cd.git` (folds) → TERM(laptop/01: 2), then
`cd cheese-app-ci-cd` → (no output); the prompt becomes `student@laptop:~/cheese-app-ci-cd$` and
flashes. `▶ your turn`.
SAY: Time to type. The README says clone or download from your repository, without an address, so here is the repo. Clone it, then cd into cheese-app-ci-cd. Pause and run both.

SHOW: TRACKER A1 · extra. It types `ls -la` (extra) → TERM(laptop/03: 5–17). Highlights in turn:
`tests` (line 17), `pytest.ini` (15), `.pre-commit-config.yaml` (8), `Dockerfile` (9); a GREY
caption "three test folders live under tests/".
SAY: An extra look around, not in the README: ls dash l a. Everything today is here: three test folders under tests, a pytest config, a pre-commit config, and the Dockerfile that bakes them into one image.

SHOW: TRACKER A2. It types `sh docker-shell.sh` (README.md line 73) → TERM(laptop/part1-01: 2–3,
…, 17, …, 31–33): the 59-second build to `(16/16) FINISHED`, line 17's `pip install` row, then
`Container is running!!!`, `Executing command: /bin/bash`, and the prompt `app@44b7ce455073:/app$`.
`▶ your turn`. The prompt is copied large above the terminal and splits: `app` "a user the
Dockerfile created · not root" · `44b7ce455073` "the container's ID · new every run" · `/app` "the
working folder".
SAY: Now the README's first command: sh docker-shell.sh. It builds the image, about a minute at the time of recording, and drops you into a shell inside the container. Pause and run it. Read the prompt: the user is app, not root, and the ID changes every run.

SHOW: TRACKER A3. At the container prompt it types
`uvicorn api.service:app --host 0.0.0.0 --port 9000 --reload` (README.md line 82, the capture's
line 34) → TERM(laptop/part1-01: 35–40). `Application startup complete.` highlights GREEN.
TRACKER A4 · extra (the caption carries "· extra" while the curls type): a schematic browser (tag
`illustration`) shows the three README URLs as tabs; beside it three small terminal cards (each
with a GREY `extra` tag, "the browser's evidence"), typing `curl -s http://localhost:9000`,
`curl -s http://localhost:9000/health` and
`curl -s 'http://localhost:9000/euclidean_distance/?x=3&y=4'` →
TERM(laptop/part1-02: 2), TERM(laptop/part1-03: 2), TERM(laptop/part1-04: 2; wrap). The three
`GET … 200 OK` access lines print in the server terminal (part1-01: 41–43). `▶ your turn`.
SAY: Inside, start the server: uvicorn api dot service colon app, host 0.0.0.0, port 9000, with reload. When it says application startup complete, open the three README URLs in your browser; pause and do it. Here three curl calls stand in for the browser: welcome, health, and the distance answer.

SHOW: The distance card enlarges: `{"x":3.0,"y":4.0,"distance":5.0,"message":…}`; a README card
(`README.md · line 90`) "returns 5.0" with tag `erratum`; CODE(cheese-app-ci-cd/src/api-service/api/service.py: 45–50)
beside it, the `"distance": result` row highlighted.
SAY: One small gap: the README says this endpoint returns 5.0. Really it returns a JSON object whose distance field is 5.0, as the code shows.

SHOW: TRACKER A5. The server terminal gets `^C` → TERM(laptop/part1-01: 44–49), then types `exit`
(line 51) → the laptop prompt returns. TRACKER A5 · extra: it types `docker ps -a` (extra) →
TERM(laptop/part1-05: 2; squeeze), header only. A 2-line CODE crop of
CODE(cheese-app-ci-cd/docker-shell.sh: 15–16) appears at "dash dash rm", `--rm` highlighted; the
flag chip flies to the empty `docker ps -a` output. Then beside the terminal a GREY laptop folder
and a TEAL image box, with a crossed dashed arrow between them, caption "not mounted · --reload
watches the copy inside". Fade out.
SAY: Stop the server with control C, then type exit. Because the shell script used dash dash rm, nothing is left behind; an extra docker ps dash a, confirms it. One warning that pays off soon: your files are not mounted into this container. The reload flag watches the copy baked into the image, so an edit on your laptop changes nothing until you rebuild.

---

## S05 · Formatter vs linter — `s05_format_lint.py` · `FormatterLinter`

SHOW: TRACKER B1 (tracker B appears: "README › Part 2: Identifying Code Quality Issues", 6 dots).
Concept card first: a PURPLE chip "formatter · rewrites" with an arrow looping code back onto
itself tidied, and a PURPLE chip "linter · reports" with an arrow to a RED findings list. GREY tag
`Lecture 9 · slides 29–31` (top right, until the funnel).
SAY: Part 2 hunts for quality issues with two tools not to confuse. A formatter rewrites code into one layout and never changes behavior. A linter only reports: style issues, likely bugs, things needing a person. Format first, then lint.

SHOW: TRACKER B1. Full terminal types `docker build -t cheese-app-api:local .` (README.md line 106)
→ TERM(laptop/part2-01: 2, …, 26–27, …, 59). The `CACHED` rows highlight TEAL; `naming to …
cheese-app-api:local` underlined. `▶ your turn`.
SAY: First build the image, cheese-app-api tagged local. Every step says CACHED: the shell script already built this Dockerfile. Pause and run it.

SHOW: TRACKER B2. It types `docker run --rm cheese-app-api:local flake8 --max-line-length=120 api/`
(README.md line 109; folds) → TERM(laptop/part2-02: 2–5), lines 4–5 RED. Beside it
CODE(cheese-app-ci-cd/src/api-service/api/utils.py: 7–14), the comma of line 7 and the blank lines
before line 13 highlighted RED. `▶ your turn`.
SAY: Now the linter, inside the image: flake8, max line length 120, on the api folder. Pause and run it. Two findings in utils.py, a missing space after a comma, and too many blank lines: mess left on purpose.

SHOW: TRACKER B3. It types `docker run --rm cheese-app-api:local black --check --diff api/`
(README.md line 112; folds) → TERM(laptop/part2-03: 2–3, …, 12–13, …, 21, 39, …, 42). Line 42
`2 files would be reformatted, 1 file would be left unchanged.` highlights; a YELLOW "2?" beside it.
`▶ your turn`.
SAY: Then black, in check and diff mode. Pause and run it. It reports 2 files would be reformatted, not one. This command gives black no width, so it falls back to its default of 88 and also folds a 95 character line in service.py.

SHOW: V4 ribbon: `service.py` line 15 drawn as a ribbon of 95 character cells. A width post at 88:
the ribbon folds to three lines; the post slides to 120: it unfolds to one. The fold–unfold loops
twice. Under it a card, tag `erratum`: "hook + CI: 120 (`.pre-commit-config.yaml:34,43`) · this
README command: black's default 88 · host flake8 default: 79". After the SAY ends, the ribbon loop
holds for a 5-second silent beat before the next block (an unprompted pause; not a PONDER card).
SAY: Watch the trap. At width 88, black folds that line into three; at 120, it unfolds to one. The hook and CI here both use 120, but several README commands pass no width, so the same file gets different answers. Always pass 120, or set it once in config.

SHOW: TRACKER B4. It types `pip install black flake8` (README.md line 118) → TERM(laptop/part2-04:
2–5, …, 37; wrap). ORANGE row tag "on the host" beside the command; `black-26.10.1` and
`flake8-7.4.1` in line 37 get the tag `at the time of recording`. A small GREY chip under the
command: "pip refuses? (PEP 668, Homebrew/Debian) → any venv, or pipx · study guide". `▶ your turn`.
SAY: Option B runs the same checks on your laptop: install black and flake8 with pip, on the host, 26.10.1 and 7.4.1 at the time of recording. Pause and run it. If pip refuses with externally managed environment, as Homebrew Pythons do, use any lecture 3 virtual environment, or pipx; the study guide has the one-liner.

SHOW: TRACKER B5: it types `flake8 src/api-service/api/` (README.md line 121) →
TERM(laptop/part2-05: 2–4); line 2's `E501 (95 > 79)` highlights RED, caption "flake8's default:
79". TRACKER B6: it types `black --check --diff src/api-service/api/` (README.md line 124) →
TERM(laptop/part2-06: …, 19, 37, …, 40). `▶ your turn` on each.
SAY: Pause and run both. The local flake8, at its default of 79, adds a third finding, that same 95 character line; local black wants the same two files changed.

SHOW: V4 funnel on the pre-demo file: CODE(cheese-app-ci-cd-history/8eb63fc-service.py: 7–14),
header `8eb63fc · service.py · lines 7–14`, line 10 `import os` RED. A RED findings bar shrinks as
a black broom sweeps the panel; 2 RED survivors remain as chips: `F401 'os' imported but unused`
and `E501 · a 147-character line · a string black must not break`. GREY caption "the class fixed these two by hand". Fade out.
SAY: What can a formatter fix? On the messy service.py from the repo's history, black sweeps away almost every finding, and exactly 2 survive: an unused import, which a formatter cannot delete, and a long quoted sentence black must not rewrite. The class fixed both by hand.

---

## S06 · pytest, under the hood — `s06_pytest.py` · `PytestInside`

SHOW: No tracker (concept scene). CODE(cheese-app-ci-cd/pytest.ini: 4–17); lines 6–8 (the three
`test_*` rules) highlight in turn, then line 17 `-ra` YELLOW with the caption "the summary where
skips confess". GREY tag `Lecture 9 · slides 26, 58–61` (top right, whole scene).
SAY: Before running tests in bulk, meet the machine that finds them. The config file pytest.ini sets the rules: files named test underscore something, classes named Test, functions named test underscore. It also adds options to every run, and the one to remember is dash r a, the summary of everything not plainly passed.

SHOW: V3 collector: the `tests/` tree with its three folders; a YELLOW scanner sweeps, every
matching `test_*` name lights GREEN with a counter rising to 26 (no `broken` chip yet: that
function does not exist in the clone).
SAY: Watch the collector sweep the tests folder: every matching name lights up, 26 tests in all.

SHOW: The tree dims; a README card (`README.md · line 388`):
`echo "def broken(): assert False" >> tests/unit/test_utils.py`. A GREY chip `broken` drops out of
the card into the unit folder, dark.
PONDER(8 s, "README Part 6 appends def broken(): assert False\nto a test file. Will the unit tests go red?")
SAY: Something to ponder. A later README part appends the line def broken, assert False, to a test file, hoping to break the build. Will the unit test run go red?

SHOW: The scanner sweeps again; the appended `broken` chip stays dark beside a GREY ruler
`python_functions = test_*`; a GREEN chip `test_broken` lights up instead, tag `erratum` on the
README card.
SAY: No. Watch the collector: the appended name stays dark. The name does not match test underscore star, so it is never collected, never run. To really break the build, call it test underscore broken. Discovery by convention cuts both ways.

SHOW: Three mini-cards in a row: "assert shows both values" (a failed compare with both sides
printed), "approx for floats" (two dots within a tolerance band), and
CODE(cheese-app-ci-cd/tests/unit/test_utils.py: 69–72) with `pytest.raises(TypeError)` GREEN.
SAY: Three more pytest verbs in 30 seconds. A plain assert is rewritten so a failure shows both values. For floats, pytest dot approx compares with a tolerance. And pytest dot raises passes only when the block raises the named error: the invalid tray from earlier.

SHOW: CODE(cheese-app-ci-cd/tests/integration/test_api.py: 7–11), line 11 `client = TestClient(app)`
highlighted. Then V3 wiring, GREY caption "what it could look like · not this repo's code": tests
on the right asking for `client` by name, a `conftest.py` box in the middle building it; a
session-scope fixture drawn once and shared, default scope as a stack of fresh copies; then
`parametrize` folds four identical `power()` test cards into one card with four input chips. Fade
out.
SAY: One gift from the lecture that this repo does not use yet. The integration tests build their test client once, as a module global. A fixture would do it better. A test asks for client by name, and pytest builds and injects it. A setting says whether each test gets a fresh one or the whole run shares one. And parametrize folds four copies into one function with four inputs.

---

## S07 · Tests inside the shipping image — `s07_container_tests.py` · `TestsInImage`

SHOW: TRACKER C1 (tracker C appears: "README › Part 3: Testing with Pytest", 10 dots). V7 first,
concept before command: CODE(cheese-app-ci-cd/Dockerfile: 27–41) at left; as lines highlight, L02's
layer slabs stack at right, small: a thin `pyproject.toml` slab, a fat ORANGE slab
`pip install --user .`, then four thin TEAL-outlined COPY slabs `api/`, `tests/`, `pytest.ini`,
`docker-entrypoint.sh`. Then CODE(cheese-app-ci-cd/docker-entrypoint.sh: 5–13) replaces the
Dockerfile panel; line 5 (PATH) PINK, line 12 `exec "$@"` YELLOW. GREY tag `Lecture 9 ·
slides 87–90` (top right, until the gate table).
SAY: Part 3 runs tests where the app lives, inside the image, by three routes: docker run per suite, a live server for the system tests, or an interactive shell. The Dockerfile copies pyproject.toml and installs the dependencies, one fat layer. Then four thin copy lines bake in the api code, the tests, the pytest config and the entrypoint. The entrypoint puts pytest on PATH, and its exec line hands the container to whatever command you pass. The container's exit code is how docker run can fail a CI step.

SHOW: TRACKER C1. Full terminal types `docker build -t cheese-app-api:local .` (README.md line 169)
→ TERM(laptop/part3-opt1-01: 2, …, 23–24, …, 59), all `CACHED`. TRACKER C2: it types
`docker run --rm cheese-app-api:local pytest tests/unit/ -v` (README.md line 172; folds) →
TERM(laptop/part3-opt1-02: 2–3, 11, 13, …, 23, 25). Line 25 `11 passed` GREEN. `▶ your turn` on
both.
SAY: Build again, all cached, then run the unit tests: docker run, dash dash rm, the image, pytest tests slash unit: 11 passed. Pause and run both.

SHOW: TRACKER C3. It types `docker run --rm cheese-app-api:local pytest tests/integration/ -v`
(README.md line 175; folds) → TERM(laptop/part3-opt1-03: 13, …, 22, 24). TRACKER C4: it types
`docker run --rm cheese-app-api:local pytest tests/unit/ tests/integration/ -v` (README.md
line 178; folds) → TERM(laptop/part3-opt1-04: 35). Both summary lines highlight; `1 warning` gets
the tag `at the time of recording`. `▶ your turn`.
SAY: The integration suite says 10 passed, 1 warning; both suites together, 21 passed, 1 warning. Pause and run them. The 1 warning is pytest 9's summary line counting a warning this config hides, at the time of recording: same tests, same results.

SHOW: TRACKER C5. It types
`docker run --rm cheese-app-api:local pytest tests/unit/ --cov=api --cov-report=term` (README.md
line 181; folds) → TERM(laptop/part3-opt1-05: 28–35). The `api/service.py 17 17 0%` row
highlights RED. `▶ your turn`.
SAY: Now the coverage run: unit tests, measuring the api package. Pause and run it. Look at service.py: 0 percent; the unit tests never import it. Coverage is a list of lines nobody has asked about, not a score. Hold that thought.

SHOW: V1: the gate table slides in and its first row fills (YELLOW, then GREEN): "unit +
integration tests / pytest in the image / docker run … pytest / yes — hermetic". TRACKER C9. Strip
terminal types `sh docker-shell.sh` (README.md line 210) → TERM(laptop/part3-opt3-01: 31–33);
TRACKER C10: at the prompt `app@f738c22fed33:/app$` it types the four README commands in turn
(README.md lines 216–225), showing only the last: `pytest tests/unit/ -v`, `pytest tests/integration/ -v` and
`pytest tests/unit/ tests/integration/ -v`, each collapsed to its summary line
(TERM(laptop/part3-opt3-01: 56), (78), (111)), then `pytest tests/unit/ --cov=api --cov-report=html`
→ TERM(laptop/part3-opt3-01: 137–138), then `ls htmlcov/ | head -4` (extra) →
TERM(laptop/part3-opt3-01: 140–143), then `exit`. A RED dashed box around the `htmlcov` listing,
caption "inside a --rm container · gone on exit".
SAY: The gate table gets its first row: unit and integration tests, hermetic, one docker command. Option 2 waits; it gets the next scene. Option 3 is the same interactively: docker-shell again, the same pytest commands, the same counts. One trap: the HTML report lands inside a container that dash dash rm deletes, gone when you exit. Prefer the terminal report.

SHOW: A comparison card, one line each, tag `erratum` on the left column: left, TEAL "this image:
black, flake8, pytest, pre-commit ship as runtime deps · `>=` pins · no lockfile"
(CODE cheese-app-ci-cd/pyproject.toml: 7–19 behind it, dimmed); right, GREEN dashed "part 2:
dev tools in groups · one lockfile". Then the S04 warning pays off: the GREY host file `utils.py`
glows with an edit; the TEAL `api/` slab does not change; a rebuild arrow replaces only the four
COPY slabs, caption "packages before code". Fade out.
SAY: This image ships its dev tools as runtime dependencies, open ended pins, no lockfile; the guest lecture keeps them in groups behind one lockfile. And the part 1 warning pays off: edit utils.py on your laptop, and this container still tests yesterday's copy. Rebuild, or you test the past.

---

## S08 · The system test and the silent skip — `s08_silent_skip.py` · `SilentSkip`

SHOW: TRACKER C6. A title card, slide 94's question redrawn: "can anything but our code make it
fail?" over the GREEN dashed border. GREY tag `Lecture 9 · slides 94–97` (top right, whole scene).
A small GREY chip quoting the command: "the README repeats the build first (line 190):
`docker build -t cheese-app-api:local .` — already built, all CACHED (`laptop/part3-opt2-01`)".
The terminal types
`docker run -d --name api-server -p 9000:9000 -e DEV=1 cheese-app-api:local`
(README.md line 193; folds) → TERM(laptop/part3-opt2-02: 2). `▶ your turn`.
SAY: Option 2 is the system test, and the lecture's question: can anything but our code make it fail? Start a live server, detached, named api-server, on port 9000, with DEV equals 1. All you get back is a container ID. Pause and run it.

SHOW: TRACKER C6 · extra. It types `until curl -sf http://localhost:9000/health; do sleep 1; done; echo`
(extra; folds) → TERM(laptop/part3-opt2-03: 2), then `docker ps` (extra) →
TERM(laptop/part3-opt2-04: 2–3; squeeze). A GREY note: "CI waits too · ci.yml:150–154".
SAY: The README runs the tests immediately. We add one extra first: a loop curling the health endpoint until it answers. CI waits too, in its own way; you will see why soon. A second extra, docker ps, shows the server up.

SHOW: TRACKER C7. It types `docker run --rm --network host cheese-app-api:local pytest tests/system/ -v`
(README.md line 196; folds) → TERM(laptop/part3-opt2-05: 13–17, 19). Line 19 `5 passed` GREEN; the
V2 wire picture pulses beside the terminal, token crossing to port 9000. `▶ your turn`.
SAY: Now the README's system command: docker run with network host, pytest tests slash system. 5 passed, and this time the request really crossed the wire. Pause and run it.

SHOW: The terminal shrinks to the strip; five BLUE test dots above it, all GREEN-checked, the wire
lit.
PONDER(8 s, "The same system-test command,\nbut the server is not running.\nFail, error, or something else?")
SAY: Something to ponder: the same command again, with no server running. What exactly does pytest print?

SHOW: TRACKER C8. Full terminal types `docker stop api-server && docker rm api-server` (README.md
line 199) → TERM(laptop/part3-opt2-06: 2–3). `▶ your turn`.
SAY: The README's next step answers it: stop and remove the server. Pause and do it; the cleanup doubles as our experiment.

SHOW: TRACKER C8 · extra. It types the same
`docker run --rm --network host cheese-app-api:local pytest tests/system/ -v` (extra: the
README command with no server; folds) → TERM(laptop/part3-opt2-07: 13–17, 19–24; wrap). The four
`SKIPPED` dots above the terminal fade to GREY dashed "s"; the summary line `1 passed, 4 skipped`
stays GREEN on screen with a YELLOW "still green" bracket. The four `SKIPPED [1] … API not running
at localhost:9000` lines (20–23) highlight.
SAY: Here is the answer, as an extra run. 1 passed, 4 skipped, and the headline is still green. Four gray dots, not failures. Only the summary from dash r a, tells the truth: skipped, API not running at localhost 9000.

SHOW: CODE(cheese-app-ci-cd/tests/system/test_system_api.py: 11–25); line 24's `skipif` highlights,
a YELLOW clock chip "evaluated once · at collection" beside it. Under it a small smoke-detector
drawing: a detector with its battery removed and a GREY zzz.
SAY: Why does it skip? The test file probes the server once, when pytest collects the module. That one answer marks the whole class: a server that comes up a second late is too late. A smoke detector with its battery removed will never beep, and that is not the same as no fire.

SHOW: The border picture returns: 22 dots inside the hermetic border (the 21 GREEN from S07, plus
one TEAL dot for the system-folder test that runs no server — colored by what runs, as S03
taught), 4 BLUE dots outside, GREY dashed. A GREY dashed card:
CODE(cheese-app-ci-cd/.github/workflows/ci.yml: 150–154), the `curl -f … || exit 1` line
RED-outlined, caption "CI fails loudly · lecture 21". The border picture and the CI card fade
before the gate table arrives. V1: the gate table's system row fills, GREY dashed, drawn outside
the turnstile: "system tests / real HTTP / docker run --network host / no: not hermetic". Fade out.
SAY: On the border picture, 22 tests live inside: the 21 from last scene, plus the one system folder test that never needed the server. These 4 stand outside. The honest remedy is a marker the run must select on purpose; part 2 shows it. CI's version is loud: it curls the server first, and if the server is down, the whole job fails. The system row enters the gate table outside the turnstile: not on every commit, not hermetic.

---

## S09 · The gate on your machine — `s09_precommit.py` · `PreCommitGate`

SHOW: TRACKER D1 (tracker D appears: "README › Part 4: Automating with Pre-commit Hooks", 5 dots).
The terminal types `pip install pre-commit` (README.md line 240) → TERM(laptop/part4-01: 2–3, …,
35; wrap); `pre-commit-4.7.0` gets `at the time of recording`; an ORANGE tag "on the host ·
outside the container"; a small GREY chip under the command: "pip refuses? (PEP 668) →
`pipx install pre-commit`, or any venv · said at S05". TRACKER D2: it types `pre-commit install`
(README.md line 246) →
TERM(laptop/part4-02: 2). `▶ your turn` on both. GREY tag `Lecture 9 · slides 34, 41–44` (top
right, until the refusal).
SAY: Part 4 installs the gate. Outside the container, pip install pre-commit, 4.7.0 at the time of recording; then, from the repo root, pre-commit install: a hook file now sits in dot git. Pause and run both.

SHOW: V5 hand-over chain, left to right: a GREY `git commit` chip → a small file card
`.git/hooks/pre-commit` (GREY, tag "machine-specific · never committed") → a PURPLE `pre-commit`
tool chip → a card `.pre-commit-config.yaml` (in the repo, TEAL outline) → nine empty arches.
SAY: Git runs that hook file before every commit. It lives in dot git, outside the repository: every clone installs it again. It hands over to pre-commit, which reads the repo's config.

SHOW: CODE(cheese-app-ci-cd/.pre-commit-config.yaml: 7–44; the comment lines 28 and 37 cropped to
their hook names — the stale "L17, Slide" references are never shown). The nine arches take their
names as the panel scrolls: seven hygiene hooks, then black and flake8. Lines 35 and 44
`files: ^src/.*\.py$` highlight YELLOW; a GREY dashed chip "tests/ · never matched" beside them.
SAY: The config names nine hooks: seven hygiene guards, from whitespace to private keys. Then black and flake8, both at width 120, both seeing only Python files under src: the tests are never linted.

SHOW: TRACKER D3. It types `git commit -m "Your commit message"` (README.md line 255) →
TERM(laptop/part4-03: 2–3; wrap, 4–6, …, 15–23, 27). The `[WARNING]` line gets `at the time of
recording`; the nine `(no files to check)Skipped` rows print in a block; line 27 `nothing to
commit, working tree clean` highlights. `▶ your turn`.
SAY: Now the README's commit, on a clean tree. Pause and run it. The first run downloads each hook's pinned environment, plus a harmless warning at the time of recording. Then every hook says skipped and git says nothing to commit: hooks check staged files, and nothing was staged.

SHOW: TRACKER D4. It types `pre-commit run --all-files` (README.md line 262) →
TERM(laptop/part4-04: 2–16). Line 9 `Format Python code with Black…Failed` RED, line 11 `files
were modified by this hook` YELLOW, line 13 `reformatted src/api-service/api/utils.py`. The black
arch flashes amber and the envelope bounces back to the GREY staging tray. `▶ your turn`.
PONDER(6 s, "black just Failed on utils.py.\nflake8 runs next — will it report\nthe E231 and E303 from before?")
SAY: To exercise them anyway, pre-commit run, dash dash all dash files. Pause and run it. Six hooks pass, one has no files to check, then black fails: files were modified by this hook; it reformatted utils.py. A quick ponder: flake8 runs next. Does it report part 2's two findings?

SHOW: TERM(laptop/part4-04: 18) prints: `Check Python code with Flake8…Passed` GREEN. A before and
after utils.py pair beside it, the comma fixed.
SAY: No. Black had already rewritten the file, so flake8 saw clean code and passed. Failed here does not mean broken; it means the hook changed files: look at the change, then re-stage.

SHOW: TRACKER D4 · extra. It types `git diff` (extra) → TERM(laptop/part4-05: 2, …, 10–11, …,
16–18), then `git add -u` (extra) → (no output). TRACKER D3 (back): it types
`git commit -m "Your commit message"` (README.md line 255 again) → TERM(laptop/part4-07: 2–12).
Seven arches go GREEN and two (Check YAML, Check JSON) GREY dashed "(no files to check)Skipped";
the envelope passes the turnstile, the vault opens; line 11 `[main b72d50d] Your commit message`
highlights GREEN. TRACKER D5: it types `pre-commit run` (README.md line 265) →
TERM(laptop/part4-08: 2–10). `▶ your turn`.
SAY: Two extras close the loop: git diff shows the fix; git add dash u, re-stages it. Commit again: seven hooks pass, two have nothing to check, and a real commit enters history; pause and walk the loop. The README's last variant, plain pre-commit run, checks only staged files; everything skips.

SHOW: TRACKER D5 · extra. It types `sed -i '1i import os' src/api-service/api/service.py && git add -u`
(extra; folds) → (no output), then `git commit -m "try an unused import"` (extra) →
TERM(laptop/part4-11: 9–13, 18–22). Both RED: black's `files were modified` and flake8's
`F401 'os' imported but unused`. Then `git status` (extra) → TERM(laptop/part4-12: 2–3, 6–8),
caption "still staged · not committed" on lines 6–8, and
`git restore --staged src/api-service/api/service.py && git restore src/api-service/api/service.py`
(extra; folds) → (no output). The vault stays shut; a parked YELLOW question card slides to the
corner: "this gate never ran a test". Fade to an empty frame (end of part 1).
SAY: A last demo, as an extra: sed adds and stages an unused import; on a Mac, sed dash i, needs empty quotes after it. The commit fails twice: black reformats the file, and flake8 reports F401, which no formatter can fix; git status confirms no commit exists. Restore the file: your machine now says no. But this gate never ran a single test. Part 2 builds one that does, and shows what even it can miss.

---

## S10 · Guest lecture: uv, just, and two failing tests — `s10_babykev.py` · `OneCommand`

SHOW: TRACKER E1 (tracker E appears: "guest lecture › babykev walk, steps 00–05b", 8 dots).
Terminal title `laptop · babykev`, prompt `student@laptop:~$`. Two PURPLE chips install as extras:
it types `uv --version` (extra) → TERM(babykev/02: 2) and `just --version` (extra) →
TERM(babykev/04: 2); both get `at the time of recording`. GREY tag `Lecture 9 · slides 14–20,
25–28` (top right, whole scene).
SAY: Part 2 is the guest lecture, by Rahul Dave. It builds the same gate around a small machine learning project, babykev, which answers questions about cheese and reports how confident it is; a pure guess should score zero. No Docker until the very end. Two tools first, as extras: the package manager uv from lecture 2, 0.13.2 at the time of recording, and the command runner just, 1.59.0.

SHOW: It types `git clone https://github.com/rahuldave/babykev` → TERM(babykev/05: 2), `cd babykev`
→ (no output), then `git tag -n1 --list 'step-*'` (babykev README.md line 148) →
TERM(babykev/07: 2–10). The nine tag lines light in turn; a GREY caption "the repo is its own
slide deck". `▶ your turn`.
SAY: Clone babykev and list its tags: 9 steps, one per lecture stage. The repo is its own slide deck, and git switch, dash dash detach, moves you to any step. Pause and run both.

SHOW: TRACKER E1. It types `git switch --detach step-00` (babykev README.md line 150) →
TERM(babykev/s00-01: 2), then `uv sync --locked` (walk step-00) → TERM(babykev/s00-02: 2–4, 6;
wrap, 9–10). `Using CPython 3.13.16` GREEN; the uv-build warning line 6 gets `at the time of
recording`. The lockfile as a 3-second mechanism, not a card: two dependency columns side by side;
the unlocked one's version numbers tick upward over time, the locked one hits a GREEN lock glyph
on a `uv.lock` card and prints a RED "stop" instead of silently upgrading. Beside it a TEAL frost
glyph "the cheese way: freeze an image" for contrast. Then it types `just` →
TERM(babykev/s00-05: 2–6). `▶ your turn`.
SAY: At step zero zero, one command builds the environment: uv sync, dash dash locked. It installs Python 3.13.16 and the project exactly as the lockfile says. Locked means stop rather than silently upgrade. Its warning is harmless, at the time of recording. The cheese repo froze an image; babykev pins a lockfile. Typing just, alone, lists the recipes: one name per task, for people, hook, and later CI. Pause and run these.

SHOW: TRACKER E2. It types `git switch --detach step-01` → TERM(babykev/s01-01: 3), `just setup` →
TERM(babykev/s01-02: 2–3, 9, …, 19), then `uv run pytest` (walk step-01) → TERM(babykev/s01-03:
10–11, …, 53–55). Line 55 `2 failed, 50 passed` RED-and-GREEN; beside the terminal,
TERM(babykev/s01-06: 32–35; wrap) as a small card showing `score_confidence` expecting 0.
`▶ your turn`.
SAY: Step 1 brings the contract and its tests. Run uv run pytest: 2 failed, 50 passed, and the tests are right. One failure is a pure guess scored as half confident; the other is 77 rounded probabilities that sum to 0.77. Same rule as the cheese demo: fix the code, not the tests. Pause and run it.

SHOW: TRACKER E3. V4 funnel reprise: a RED findings bar steps down as chips type in a strip
terminal: `uv run ruff check --statistics` (walk step-02) → TERM(babykev/s02-12: 2–6, …, 14–15),
`Found 70 errors.`; then `just lint --fix` → TERM(babykev/s02-14: 692), `70 errors, 1 fixed, 69
remaining`; then `just lint --fix --unsafe-fixes` → TERM(babykev/s02-15: 360), `32 fixed, 37
remaining`. A faint first notch above 70 carries a GREY chip `recorded · walk.md: 79 before just
fmt` (slide 31; not spoken). The bar settles at 37 with the caption "the rest need a person". A GREEN card:
CODE(babykev/pyproject.toml: 60–65), `line-length = 100` highlighted. Fade out.
SAY: Step 2 is format and lint at scale, ruff in both roles. After formatting, the linter counts 70 findings. Safe automatic fixes remove one. Unsafe fixes, applied deliberately, remove 32 more; 37 remain; those need a person. And the width war from part 1 is settled in one line, line length 100, written once in pyproject.toml; the formatter and the linter both follow it.

---

## S11 · One command is the gate — `s11_just_check.py` · `JustCheck`

SHOW: TRACKER E4. It types `git switch --detach step-03` → TERM(babykev/s03-01: 3), then
`just setup` (walk step-03) → TERM(babykev/s03-02: 2, …, 19, 25). Line 25 `pre-commit installed at
.git/hooks/pre-commit` highlights. It types
`cat "$(git rev-parse --git-path hooks)/pre-commit"` (walk.md:230; folds) → TERM(babykev/s03-05:
2–3, 6–9, …, 15). Line 7's venv path highlights YELLOW, caption "this machine's path · why it is
never committed". GREY tag `Lecture 9 · slides 34–43` (top right, until the refusals). `▶ your
turn` on the setup.
SAY: Step 3 installs the gate with one recipe, just setup: lockfile sync and hook install together. Pause and run it. The walk's next command prints the hook file: the same hand-over chain as before, with one difference. This machine's own venv path is baked inside, so it is never committed.

SHOW: CODE(babykev/.pre-commit-config.yaml: 5–24); the four hooks light as arches beside S09's
nine (V5 side by side): large files, merge markers, `no-env-file`, and `just check` with
`always_run: true` and `pass_filenames: false` highlighted. Then a strip terminal types
`just --show check` (walk.md:245) → TERM(babykev/s03-08: 9–12).
SAY: The config here has four hooks, not nine: large files, merge markers, a policy hook refusing any dot env file, and one local hook that runs just check. So the hook runs exactly what you type. At this step, just check means format check, lint, tests with a 90 percent coverage floor, and config linting.

SHOW: TRACKER E4. It types `just check` (walk step-03) → TERM(babykev/s03-09: 2–7, 18–21). Line 18
`Required test coverage of 90% reached. Total coverage: 100.00%` GREEN. Then it types
`just test -k confidence --cov-fail-under=90` (walk step-03) → TERM(babykev/s03-10: 2, 11–12,
25–26). Line 25 `FAIL Required test coverage of 90% not reached. Total coverage: 49.40%` RED.
`▶ your turn` on both (BRIEF: the floor biting is the lesson).
SAY: Run just check: everything green, the floor reads 100 percent. Now watch it bite: ask for only the confidence tests, keeping the floor. 9 tests pass, half the code is never exercised, and the run fails at 49.4 percent coverage. A floor is a gate, not a goal. Pause and run both.

SHOW: Config beat: it types the walk's mis-indent sed
`sed -i 's/^        args: \[--maxkb=1000\]$/          args: [--maxkb=1000]/' .pre-commit-config.yaml`
(walk.md:260, shown small, folds; the walk spells it for a Mac as `sed -i ''` — the capture ran
the Linux form) → TERM(babykev/s03-12: → (no output)), then `uv run yamllint --strict .` (walk
step-03) → TERM(babykev/s03-13: 2–3), the error line RED with its exact line number; then
`git restore .pre-commit-config.yaml` (walk.md:262, small) → (no output), and `just lint-config` →
TERM(babykev/s03-28: 7–8). Three GREY chips beside it: `validate-pyproject` · `uv lock --check` ·
`just --fmt --check`.
SAY: Config files are checked too: a broken hook config breaks every commit. One wrong indent in the pre-commit config, and yamllint names the exact line. Restored, the recipe runs green; it also validates pyproject.toml and checks the lockfile.

SHOW: TRACKER E4. The refusals: it types the walk's perl line
`perl -pi -e 's/^(from typing)/import os\n$1/' src/babykev/api.py` (walk.md:296, shown small,
folds) → (no output), then `git commit -am "try"` (walk step-03) → TERM(babykev/s03-31: 6–9,
16–17, …, 32). `▶ your turn` on the commit (BRIEF: the hook refuses, live). `just check…Failed`
and `F401` RED; `git status` (walk.md:301) → TERM(babykev/s03-32: 2–3, 6) "no commit";
`git restore src/babykev/api.py` (walk.md:302, small). Then `echo X=1 > .env && git add -f .env`
(walk step-03; folds) → (no output) and `git commit -m "try"` → TERM(babykev/s03-35: 2–10); line
8, the config's own sentence, highlights RED; the undo `git rm --cached -q .env && rm .env`
(walk.md:311, small).
SAY: Now the gate refuses, twice; pause and try the first. An unused import goes in; the commit fails on F401, no commit made. Then a dot env file is staged, and the refusal is the config's own sentence: a dot env file holds the settings and secrets of one machine. It is never committed.

SHOW: TRACKER E5. Two style cards: GREEN "babykev: check points, you run just fmt yourself" ·
TEAL "cheese: black rewrites, you look and re-stage"; the style cards clear before the docs
terminals arrive. Then two small terminals: `just docs check`
at step-04 → TERM(babykev/s04-04: 2–7, …, 93), `50 of 88` RED; and at step-04b →
TERM(babykev/s04b-03: 2–9), `88 of 88` GREEN; a chip from TERM(babykev/s04b-09: 5–7, 35–36) "one
deleted description blocks the commit". V1: the gate table grows rows "docs" and "config files",
GREEN inside the turnstile. Fade out.
SAY: Two gate styles, both fine: this one points and you run just fmt; the cheese gate rewrites and makes you look. Steps 4 and 4 b put documentation in the gate: first 50 of 88 functions, methods and classes typed and documented, one step later 88 of 88; deleting one description blocks a commit. Two rows join the table.

---

## S12 · All green, and the mask is wrong — `s12_green_wrong.py` · `GreenButWrong`

SHOW: TRACKER E6. It types `git switch --detach step-05` → TERM(babykev/s05-01: 3), then
`just setup` → TERM(babykev/s05-02: 2, 4; wrap, 8, 44, 46–47, 49). `torch==2.14.1+cpu` highlights;
`at the time of recording` beside it; the uv-build warning (line 4) keeps its earlier tag. Then
`just test` (walk step-05) → TERM(babykev/s05-03: 11–15, 29–30). Line 30 `92 passed` and the
`TOTAL … 94%` row GREEN. GREY tag `Lecture 9 · slides 53–55, 72–75` (top right, whole scene).
`▶ your turn`.
SAY: Step 5 brings the model: the setup recipe now pulls the model stack, 38 packages including torch 2.14.1 for the CPU, at the time of recording. Then just test: 92 passed, coverage 94 percent, all green. Pause and run both.

SHOW: The model in one picture (slides 54–55 redrawn): a sequence bar packs a GREEN "state" block
and three TEAL "question" blocks; V6's 6×6 grid assembles beside it, the rule drawn as one GREY
sentence under it: "a question sees the state and itself — never a sibling". A 2-second motive
beat: question 2's attention arrow sneaks toward question 1's tokens and is crossed out RED. One
cell of the grid pulses YELLOW: "this cell is the whole difference".
SAY: What does the model do? A request packs one state and several questions into one sequence. A mask enforces one rule: a question may see the state and itself, never a sibling question. Questions must be answered independently; a peek would leak one answer into another. That one forbidden cell is the whole difference from a causal mask.

SHOW: TRACKER E6. The walk's one-liner
`uv run python -c "from babykev.model import branch_mask; m = branch_mask([0, 0, 1, 1, 2, 2], 'cpu')[0, 0] == 0; print('\n'.join(''.join('#' if x else '.' for x in r) for r in m))"`
types in a strip (walk.md:589, folds, shown small) → TERM(babykev/s05-04: 2–7): the six `#`/`.`
rows print into the V6 grid. Rows 5 and 6 (`#####.`, `######`) flash RED. `▶ your turn` (BRIEF:
the pivotal observation). Then `sed -n '140p' src/babykev/model.py` (walk step-05) →
TERM(babykev/s05-05: 2), the `torch.ones_like` line RED.
SAY: The walk prints the mask the code builds, for two state tokens and two questions of two; pause and print yours. Rows 5 and 6 say question 2 sees everything, including question 1. The cause is one line: torch dot ones like marks every pair of tokens as the same question.

SHOW: The comparison script, a here-document, types collapsed to its first line
`uv run python - <<'EOF'` plus one `…` row (walk.md:594–600; the full six-line script is in the
study guide, said by the caption "full script: study guide") → TERM(babykev/s05-06: 8–13): the
should-be grid beside the built one, the two `WRONG` rows RED. A GREY caption: "nothing in just
check runs this".
PONDER(8 s, "Every line of branch_mask ran.\nCoverage reads 94%.\nCan any coverage number catch this bug?")
SAY: A checker script compares the built mask against the one we meant, and prints WRONG on those rows. But nothing in just check runs it; a printout you read by eye is not a test. Something to ponder: every line of branch mask ran, and coverage reads 94 percent. Can any coverage number catch this bug?

SHOW: The coverage highlighter sweeps every line of a `branch_mask` panel GREEN while the RED rows
stay wrong beside it.
SAY: No. Coverage counts lines that ran, never whether anyone checked what they produced. Necessary, and never sufficient.

SHOW: TRACKER E6. It types `uv run ty check` (walk step-05) → TERM(babykev/s05-07: 2–3, …, 55).
`Found 6 diagnostics` RED. Then `just check` (walk
step-05) → TERM(babykev/s05-11: 2–6, 22–23), `92 passed`, `Required test coverage of 90% reached`
GREEN; a YELLOW bracket pairs the GREEN check with the RED diagnostics.
SAY: Also green and blind: the type checker, which reads declared types without running the code. Running ty finds 6 diagnostics, yet just check is green: types are not in the gate yet, and a check outside the gate protects nobody.

SHOW: TRACKER E6. It types `just smoke local` (walk step-05) → TERM(babykev/s05-12: 2, 5, …,
22–25, 32–33). `▶ your turn` (BRIEF). Line 5 `503M parameters, 9.3M of them trainable`; line 32
`6 of 15 right` YELLOW; line 33 `Nothing is trained yet: these are guesses.` GREY. The ms figure
is not highlighted. Fade out.
SAY: Last, the smoke on the real model: half a billion parameters, downloaded once from the Hugging Face Hub, a public model host, answering 15 cheese questions on CPU; pause and run it. 6 of 15 right. Nothing is trained, these are guesses; hold that number.

---

## S13 · Properties, not examples — `s13_properties.py` · `PropertyTests`

SHOW: TRACKER E7. It types `git switch --detach step-05a` → TERM(babykev/s05a-01: 3), `just setup`
(small), then `just test` (walk step-05a) → TERM(babykev/s05a-03: 11–17, 66–67). Line 67
`1 failed, 102 passed` prints honestly; beside the terminal a GREY card, tag `recorded · walk.md`:
"the author's Mac: 103 passed". A two-dot picture: GREEN "same to 4 decimals", RED "last bits
differ". GREY tag `Lecture 9 · slides 78–84` (top right, whole scene). `▶ your turn`.
SAY: Step five a answers with tests that could tell. First, honesty: on this machine just test says 1 failed, 102 passed. The failing test demands bit for bit equal outputs. On this Linux CPU, torch sums in a different order than the author's Mac; there all 103 pass, as the walk records. Hermetic means only your code can make it fail; bit exactness across machines is a stronger promise; this machine measured it.

SHOW: TRACKER E7. The walk's wrong fix types:
`perl -pi -e 's/^    same = \(s\[None, :\] == s\[:, None\]\) \| \(s\[None, :\] == 0\)$/    same = (s[None, :] == s[:, None]) | (s[None, :] == 0) | (s[None, :] < s[:, None] - 1)/' src/babykev/model.py`
(walk.md:627, shown small, folds) → (no output). The wrong fix is drawn on the V6 grid as it is
spoken: the adjacent-question cells correctly blocked RED, the two-back cell wrongly open and
pulsing YELLOW. The six-token checker, a here-document collapsed to `uv run python - <<'EOF'` +
`…` (walk.md:628–635; caption "full script: study guide") → TERM(babykev/s05a-05: 8–13), all `ok`
— a GREY shrug glyph. The four-token checker, collapsed the same way (walk.md:636–641) →
TERM(babykev/s05a-06: 8–11), row 4 `WRONG` RED; the checker card carries the caption
"state 1 · questions 1, 1, 1".
SAY: Now the lesson. A deliberately wrong fix goes in, one that blocks only the question just before. The six token picture says all ok; it cannot tell. A four token picture can: its last row reads WRONG.

SHOW: CODE(babykev/tests/unit/test_mask.py: 58–65) with line 10's `shapes` strategy shown as a
caption chip above it ("a state of 1 to 6 tokens · up to 4 questions of 1 to 5"). After the chip
lands, the counter spins up beside it: "shapes to cover with pictures: 4,686". The assert line
highlights GREEN.
PONDER(8 s, "The wrong fix blocks only the question just before.\nWhat is the smallest request shape\nthat still breaks the rule?")
SAY: State the rule once instead. The property test lets hypothesis draw any request shape: a state of 1 to 6 tokens, up to 4 questions of 1 to 5. Those sizes allow 4,686 shapes, too many for pictures. It asserts that no allowed pair is ever a sibling pair. Something to ponder before we run it.

SHOW: TRACKER E7. It types `just test -k no_question_sees_another` (walk step-05a) →
TERM(babykev/s05a-08: 9, 11, 25, 41–45). `▶ your turn` (BRIEF). Line 25 `shape = (1, [1, 1, 1])`
highlights YELLOW; V6 dice roll shapes and a RED counter-example grid shrinks step by step to 4×4;
the allowed grid overlays the siblings grid, one overlapping cell lit RED.
SAY: You need a question two steps back, so one state token and three questions of one token each. And hypothesis finds it on its own: the one test fails, then shrinks the counter example to exactly that shape. Pause and run it. A property test does not only say no; it hands you the smallest witness.

SHOW: `git restore src/babykev/model.py` (walk.md:654, small). Then the walk's perl line writes
step-05's mask back:
`perl -pi -e 's/^    same = \(s\[None, :\] == s\[:, None\]\) \| \(s\[None, :\] == 0\)$/    same = torch.ones_like(causal) | (s[None, :] == 0)/' src/babykev/model.py`
(walk.md:667, shown small, folds) → (no output), and `just test` → TERM(babykev/s05a-11: 14–17, …,
306–307). `▶ your turn` (BRIEF). Line 307 `8 failed, 95 passed` RED. Then
`git restore src/babykev/model.py` (walk.md:669, small) and `sed -n '151p' src/babykev/model.py`
(walk step-05a) → TERM(babykev/s05a-13: 2), the fixed line GREEN.
SAY: Proof the gate grew teeth: put step 5's wrong mask line back and run just test; pause and try it. 8 failed, 95 passed; code that sailed through before is refused. A gate refuses only what its tests can see. The real fix is one line: same question means same segment ID.

SHOW: TRACKER E7. It types `just types` (walk step-05a) → TERM(babykev/s05a-14: 2–3), `All checks
passed!` GREEN; `just --show check` → TERM(babykev/s05a-15: 9–14), the new `just types` line
YELLOW. V1: the types row joins the gate table. Then `just smoke local` → TERM(babykev/s05a-17: 2,
4, …, 31–32). `▶ your turn` on the smoke (BRIEF). `4 of 15 right` YELLOW. Fade out.
SAY: Types join the gate too: the new recipe, just types, passes, and check has six lines. And the smoke, with the right mask? 4 of 15, lower than before. Pause and run the smoke. The 6 was luck; an untrained score means nothing.

---

## S14 · Hooks are local; CI checks again — `s14_ci.py` · `HooksThenCI`

SHOW: TRACKER E8. It types `git switch --detach step-05b` → TERM(babykev/s05b-01: 3), `just setup`
(small), then `just test` (walk step-05b) → TERM(babykev/s05b-03: 9, 67). Line 9 `collected 104
items / 1 deselected / 103 selected` highlights; `1 deselected` gets a GREY dashed dot, and the
platform failure in line 67 keeps S13's GREY `recorded · walk.md` card beside it, small.
CODE(babykev/pyproject.toml: 53–57), the `-m 'not system'` line YELLOW. GREY tag `Lecture 9 ·
slides 20, 94–99` (top right, whole scene).
SAY: Step five b gives non hermetic tests an honest home. A new real model test is marked system, and the config deselects that marker by default: every just test says 1 deselected, on purpose.

SHOW: TRACKER E8. It types `just test -m system` (walk step-05b) → TERM(babykev/s05b-06: 9, 11,
26). Line 26 `1 passed, 103 deselected` GREEN, the one dot solid BLUE outside the hermetic border.
`▶ your turn`.
SAY: Asked for explicitly, just test, dash m system, says 1 passed, 103 deselected: the real model ran, and it had to pass, not skip. That is the honest version of part 1's silent skip. Pause and run both forms.

SHOW: TRACKER E8. It types `uv run hadolint Dockerfile` (walk step-05b) → (no output), a
GREEN check. Then `docker build --target run --tag babykev-run .` (walk step-05b) →
TERM(babykev/s05b-18: 2) RED, and `just image build run` → TERM(babykev/s05b-19: 2). A GREY card,
tag `recorded · walk.md`: "run image 1.15 GB · dev image 1.84 GB · `just check` green inside
`--network none`".
SAY: Smaller rows join the gate: hadolint lints the Dockerfile, clean. Part 2 was recorded on a plain machine without Docker, so the recipes fail politely: docker build is command not found, and the image recipe explains itself. On your laptop, with Docker Desktop, both images build for real. The walk's record shows the rest. Two images from one lockfile, 1.15 and 1.84 gigabytes. And just check runs green inside a container with no network: the hermetic claim, proved by experiment.

SHOW: V1 finale: the gate table complete, six rows, the system row GREY dashed outside the
turnstile. Then the limit: a GREY chip `git commit --no-verify` walks an envelope around the whole
turnstile.
SAY: The gate table is full: six rows, system outside the turnstile. Now the limit. A hook runs on one machine, and git commit, dash dash no verify, walks straight past it.

SHOW: The gate table clears before the server arrives. A GREY dashed BLUE server appears above
with the same turnstile duplicated on it;
CODE(cheese-app-ci-cd/.github/workflows/ci.yml: 13–17) small and dimmed, caption "Part 5 of this
same repo · lecture 21". A kind card, tag `erratum`: "here: hook pins black 24.1.1 · image installs
the newest · README widths vary — one command for everyone is the lesson".
SAY: So CI re-runs the same checks on a server nobody can skip: part 5 of this same repo, in lecture 21. It is also why the hook, CI and the README should spell the checks one way; the cheese repo does not quite manage that. One command for everyone is the lesson for your milestone. Coverage floors in one line: babykev chose 90; milestone 5 asks at least 70.

---

## S15 · Tear down, recap, and what's next — `s15_recap.py` · `Recap`

SHOW: TRACKER F1 (tracker F appears: "README › Docker Cleanup", 3 dots). Laptop terminal (title
`laptop`) types `docker container ls` (README.md line 571) → TERM(laptop/clean-01: 2; squeeze),
header only; a README card (`README.md · line 572`) "Stop any container that is running" with the
GREY chip "nothing to stop here". TRACKER F2: it types `docker system prune` (README.md line 573)
→ TERM(laptop/clean-02: 2–8; [y/N] y, …, 26). `Total reclaimed space: 95.17MB` gets `at the time
of recording`. TRACKER F3: it types `docker image ls` (README.md line 574) → TERM(laptop/clean-03:
2–4; squeeze; the `python:3.11-slim-bookworm` row is never printed). Then `pre-commit uninstall`
(extra) → TERM(laptop/clean-04: 2). `▶ your turn` on the prune.
SAY: Before the recap, clean up. The README's Docker cleanup: docker container ls shows nothing running, so nothing to stop. Then docker system prune; type y: about 95 megabytes of build cache, at the time of recording. A final docker image ls shows the two cheese images. One extra undoes the hook: pre-commit uninstall. On the babykev side, delete the venv; and if you ran the smoke, the roughly 1 gigabyte model in the Hugging Face cache. Nothing today was billable: the gate lives on your laptop, and that is the point.

SHOW: A card "Test yourself". One question at a time (≥ 24 pt, ≤ 3 lines), each with a text-free
icon from its set piece: Q1 "What runs in a unit, an integration and a system test of this repo —
file by file?" (the three nested boxes); Q2 "The system tests 'pass' with no server. What does
pytest actually print — and are those four tests hermetic?" (four gray dashed dots, green
headline). When the next question arrives, the previous one becomes a one-line label in a list at
left: "three kinds" · "silent skip".
SAY: 5 questions to test yourself. One: what runs in a unit, an integration and a system test of this repo, file by file? Two: the system tests pass with no server at all. What does pytest actually print, and are those four tests hermetic?

SHOW: Q3 "What does pre-commit install actually create, and why must every clone run it (or just
setup) again?" (the hand-over chain); Q4 "black says Failed — files were modified. Is your code
broken, and what do you do next?" (the amber arch and bounced envelope); Q5 "babykev had 94%
coverage and a wrong mask. What kind of test finally saw the bug — and why was coverage blind?"
(the mask grid with two red rows). Labels join the list: "the hook file" · "modified by black" ·
"properties over coverage".
SAY: Three: what does pre-commit install actually create, and why must every clone run it again? Four: black says failed, files were modified. Is your code broken, and what do you do next? Five: babykev had 94 percent coverage and a wrong mask. What kind of test finally saw the bug, and why was coverage blind to it?

SHOW: The label list stays at left. Two footer cards: "Answers: exercises.md" and "Study guide +
every command: github.com/JunyiZhou-Conny/MLOps_Learning · guides/L09-ci-testing-precommit.md". A
"Next" card, GREY dashed: a key glyph with the `detect-private-key` arch ("L10: credentials"), and
a BLUE server with the turnstile ("L21: this repo's checks on GitHub"). Everything fades to an
empty frame (end of part 2).
SAY: The answers are in the exercises, and every command is in the study guide. Next lecture brings cloud credentials, where the detect private keys hook earns its keep. And in lecture 21, this very repo's checks run on GitHub, where nobody can walk past them with dash dash no verify.
