# Brief · AC215 L9 — CI & unit testing: who gets to say no before a commit?

The design of this video, written before the script. Series rules: `docs/AC215_SERIES.md`.
Facts: `digest.md` (the verified tutorial digest), `SLIDES.md` (the lecture-slide digest and scene
map) and `assets/` (real captures, see `ASSETS.md`). **Where the digest or the slides and the
captures disagree, the captures win.** They are newer (2026-10-19, 21:21–22:30 UTC) and were made
by running the README's and the walk's commands as written:

| topic | digest / slides | captures (use these) |
| --- | --- | --- |
| integration-test counts | "10 passed", "21 passed" (digest §4 A5, from reading the code) | `10 passed, 1 warning`, `21 passed, 1 warning` (`laptop/part3-opt1-03/04`): pytest 9.1.1 counts a warning `--disable-warnings` can't silence. Same tests, same results; say "at the time of recording". |
| `just test` at steps 05a/05b | walk.md and the slides: "103 passed" | **`1 failed, 102 passed`** live on this Linux x86 machine (`babykev/s05a-03`, `s05a-16`, `s05b-03`, `s05b-17`): `test_a_question_cannot_see_its_sibling` demands bit-exact logits (`torch.equal`), and torch 2.14.1+cpu sums in a length-dependent order here; the author's Mac is bit-exact. See the decision under S13. |
| first `pre-commit` run | digest A9 suggests `run --all-files` first | the captures follow README order: `git commit` (README:255) first, on a clean tree — the one-time environment downloads and pre-commit 4.7.0's deprecation `[WARNING]` land there, then `nothing to commit`, exit 1 (`laptop/part4-03`) |
| cheese `--network none` run | SLIDES.md gap 1 proposed capturing it | not capturable in this sandbox; the silent-skip lesson uses the captured no-server run instead: `1 passed, 4 skipped` (`laptop/part3-opt2-07`) |
| blocked-commit demo | digest A10: flake8 blocks with F401 | **both** gates fire: black Failed ("files were modified": it re-places the `import os`) *and* flake8 Failed with F401 (`laptop/part4-11`) |
| versions | black 24.1.1 / flake8 7.0.0 pins etc. | host pip installs black 26.10.1, flake8 7.4.1, pre-commit 4.7.0; uv 0.13.2 warns about babykev's `uv-build` pin on every build; all said with "at the time of recording" (`ASSETS.md` versions table) |
| chapter order | digest §8 teaches tests (ch2–5) before lint (ch6) | the captures (and the README) run Part 2 (lint) before Part 3 (tests); the scene plan follows README order — concept scenes carry the test ideas earlier, command scenes stay in README order |

## Audience and goal

An AC215 student who has done L1–L4 (a VM, venvs and uv, Docker images and containers — the
`docker-shell.sh` / entrypoint pattern returns here) and can run Docker Desktop. The L5–L8 LLM
block is not needed. They have never written a pytest test, run black or flake8 deliberately, or
installed a git hook. They watch with their own clones of
[dlops-io/cheese-app-ci-cd](https://github.com/dlops-io/cheese-app-ci-cd) and (part 2)
[rahuldave/babykev](https://github.com/rahuldave/babykev) open, pausing to type each command.
Nothing in this lecture needs GCP, credentials or any paid service: it all runs on the laptop.

After the video they can:
- say what runs in a unit, an integration and a system test of this repo, file by file, and why
  the first two are hermetic and the third is not;
- run the app and the three test suites inside the Docker image (`docker run … pytest …`) and
  explain why an edit on the host changes nothing until a rebuild;
- read a pytest run: discovery rules, `pytest.raises`, `-ra`'s summary, and why
  `1 passed, 4 skipped` is not the same green as `5 passed`;
- explain what black fixes and what flake8 can only report (F401, E501), and why every command
  must carry the same line width (120) as the hook and CI;
- install pre-commit, read `.pre-commit-config.yaml`, survive "files were modified by this hook"
  (diff → add → commit again), and show a commit being refused;
- describe babykev's version of the same gate: one lockfile (`uv sync --locked`), one command
  (`just check`) run by people, the hook and (later) CI, with a coverage floor and config linting;
- explain why 94% coverage proved nothing about `branch_mask`, and how a hypothesis property test
  found and shrank the counter-example a hand-drawn picture missed;
- put non-hermetic tests behind a marker (`-m system`) instead of a silent `skipif`.

## Length and parts

~28–30 minutes. Narration 3,900–4,300 words (Kokoro af_heart, speed 0.9 ≈ 174 wpm); the plan below
totals **~4,190**. Word budgets per scene are targets (±15 %).

- **Part 1 = S01–S09** (~2,550 words, ~17 min): the cheese tutorial, in README order — the bug a
  test catches, the three kinds of test, run the app (Part 1), formatter vs linter (Part 2), the
  tests inside the image and the silent skip (Part 3), the pre-commit gate (Part 4), ending on a
  real commit passing through it and a bad one refused.
- **Part 2 = S10–S15** (~1,640 words, ~11.5 min): the guest lecture (babykev) — one lockfile and
  one command, the gate that grows, all-green-but-wrong, property tests, markers for the
  non-hermetic, then CI as the gate you can't skip (L21 teaser), teardown and recap.

The cut is the lecture's own seam: part 1 ends when the student's **own machine refuses a bad
commit** (tracker D complete, the vault shut on `F401`), with one question parked for part 2
("this gate checked format and lint — it never ran a single test; what would, and what can a fully
green gate still miss?"). Part 2 is the guest lecture answering it.

## Colours (series table, applied)

| meaning | colour |
| --- | --- |
| your laptop: the clone, the working tree, the staging area, the host shell | GREY |
| remote things: GitHub, the CI runner (L21, dashed), the Hugging Face Hub | BLUE |
| images and containers: `cheese-app-api:local`, the baked-in code slabs, babykev's dev/run images (said, recorded) | TEAL |
| system-wide / host-owned: host pip installs (`pip install black flake8 pre-commit`), the host PATH | ORANGE |
| project-owned, isolated, **hermetic**: the venv `uv sync --locked` builds, `uv.lock`, the tiny model, the dashed *hermetic border*, passing checks | GREEN |
| tools: pytest, black, flake8, pre-commit, uv, just, ruff, ty, hypothesis, docker, hadolint | PURPLE |
| errors and refusals: failing tests, F401/E231/E303/E501, the wrong mask cells, "Failed", an aborted commit, `FAIL Required test coverage` | RED |
| your turn, the README tracker, the gate-table row being filled now | YELLOW |
| money: nothing billable this lecture (see Costs) | GOLD (unused on screen) |
| lookups and routes: the HTTP request token's path, the network wire to port 9000, push to GitHub | PINK |
| future things (CI/L21 workflow, L10 credentials) and **skipped/deselected** tests | GREY, dashed |

Episode-local semantics (keep consistent): **test kinds** are coloured by what runs — unit GREEN
(one function, fully ours), integration TEAL (our parts in-process, `TestClient` / the tiny
model), system BLUE (the real thing over the network). A SKIPPED test is a GREY dashed dot — never
GREEN. The hermetic border is a GREEN dashed box; whatever stands outside it (the live server, the
Hub, the real model) is drawn outside.

## Running example

- **The laptop** (the captures' fresh Docker 29.8.2 engine standing in for Docker Desktop): user
  `student`, prompts `student@laptop:~$` / `student@laptop:~/cheese-app-ci-cd$`; terminal title
  `laptop`. Host pip is a Python 3.14.8 virtualenv standing in for a laptop Python that allows
  `pip install` (ASSETS.md capture-only notes; on a Homebrew Mac, `pip install` may refuse —
  digest G10, narration only).
- **Inside the cheese container**: the prompt is each capture's own (`app@<id>:/app$`); say once
  (S04) that the id changes every run and that `app` (uid 1000, not root) comes from the
  Dockerfile.
- **The babykev laptop**: a fresh Debian 12 container **without Docker** standing in for a laptop;
  uv 0.13.2 and just 1.59.0 installed as captured prerequisite steps; terminal title `laptop ·
  babykev`. The walk was followed "without the page" on the step tags
  (`babykev/README.md:148-150`), as ASSETS.md records; `just present`'s browser page is drawn as a
  schematic tagged `illustration` if shown at all.
- **Versions**: pytest 9.1.1's "…, 1 warning" on the integration counts, pre-commit 4.7.0's
  deprecation `[WARNING]` about the pinned v4.5.0 hooks, uv's `uv-build` pin warning, black
  26.10.1 / flake8 7.4.1 on the host — all real, all shown, all "at the time of recording".
- **Capture-only crops**: the `python:3.11-slim-bookworm` row in `clean-03` (the capture-only
  rebuilt base) is never shown; builds show no base-pull rows a student would see — say nothing,
  crop as in ASSETS.md.

## Visual set pieces (the 3Blue1Brown part)

- **V1 · The gate and the vault (S01, S09, S11, S14).** A commit envelope slides toward a
  "HISTORY" vault; a turnstile of scanner arches drops in front (slide 41, redrawn). In S01 the
  arches are unlabeled: the hook question. In S09 they become the cheese config's 9 named hooks;
  black's arch flashes amber "files were modified", the envelope bounces back to the GREY staging
  tray; on the retry all arches go GREEN and the vault opens (`part4-07`'s real
  `[main b72d50d]`). In S11 babykev's 4-arch version stands beside it, the last arch labelled
  `just check`. Running under the whole video: **the gate table** (slide 98, redrawn): four
  columns — *what is checked / how / command / on every commit?* — opened empty in S03 and filled
  row by row (tests S07, system tests S08 with "no: not hermetic" and the row standing outside the
  turnstile, format+lint S09, babykev's extra rows — types, docs, config files — in S11–S14).
  Current row YELLOW, non-hermetic rows GREY dashed.
- **V2 · One request, three sizes of test (S02–S03, S08).** A glowing PINK token
  `GET /euclidean_distance/?x=3&y=4`. Unit: the camera zooms to `power(3, 2)` alone (GREEN).
  Integration: the token enters a `TestClient` box and passes straight into the FastAPI router —
  no wire (TEAL). System: the token leaves the test container, crosses a network wire to port 9000
  on another container, and returns `{"distance": 5.0}` (BLUE). The three boxes stack into the
  README's pyramid (width = how many, height = cost per test), then re-draw as the lecture's
  **nested boxes** with a GREEN dashed *hermetic border* that only the system box crosses
  (slides 66/95). Smoke and acceptance appear as faint extra rows, acceptance marked "none yet".
  S08 reuses it: unplug the wire, four dots fade to GREY dashed "s", the headline stays green —
  the trap.
- **V3 · The collector and the fixture wiring (S06).** A sweep over the `tests/` tree lighting
  only `test_*` names (from `pytest.ini:5-8`); a function named `broken` stays dark (sets up
  Ponder 1). Then slide 58's wiring, shown as "what it could look like", not the repo's code:
  tests on the right, fixtures in the middle (`conftest.py`), arrows for "asks for"; a
  session-scope fixture drawn once and shared, default scope as a stack of fresh copies;
  `parametrize` folds four would-be `power()` tests into one function with IDs.
- **V4 · The ribbon and the funnel (S05, reprise S10).** `service.py:15` (95 characters) drawn as
  a ribbon: at width 88 black folds it to three lines; at 120 it unfolds back — loop the
  flip-flop when two commands disagree on width. Then the funnel: findings as a shrinking RED bar.
  Cheese size in S05: the messy `8eb63fc` file's findings drop to **2 survivors after black**
  (F401 `'os' imported but unused`, E501) — a formatter cannot delete an import. babykev size in
  S10: 79 → 70 (`just fmt`) → 69 (`--fix`) → 37 (`--unsafe-fixes`), "the rest need a person"
  (`s02-12/14/15`, slide 31).
- **V5 · The hand-over chain (S09, S11).** Slide 34 redrawn: git → `.git/hooks/pre-commit` (a
  small machine-specific file, never committed — that is why every clone runs `pre-commit install`
  or `just setup` again) → the pre-commit tool → `.pre-commit-config.yaml` → the hooks. In S11 the
  two configs side by side: nine arches here (seven hygiene + black + flake8, `files: ^src/`),
  four there (large files, merge markers, `no-env-file`, `just check` with `always_run`), sharing
  the large-file and merge-marker guards.
- **V6 · The mask grid (S12, S13).** The 6×6 `#`/`.` grid (tokens 1–2 state, 3–4 question 1, 5–6
  question 2; slides 72–73). A coverage highlighter sweeps every line of `branch_mask` GREEN —
  94%. Then the should-be grid fades in beside the built one and rows 5–6 (`##..#.`/`##..##` vs
  `#####.`/`######`) flash RED. In S13: hypothesis dice roll request shapes, a RED counter-example
  shrinks step by step to a 4×4 grid, and slide 81's overlay — the "allowed" grid laid over the
  "siblings" grid, the one overlapping cell lit — shows the rule failing.
- **V7 · Baked-in code (S07).** L02's layer slabs return, small: `pyproject.toml` slab, the fat
  `pip install --user .` slab, then four thin COPY slabs (`api/`, `tests/`, `pytest.ini`, the
  entrypoint; `Dockerfile:27-41`) — TEAL outlines, fills by owner. An edit glows on the GREY host
  file and the TEAL slab does not change; the rebuild replaces only the COPY slabs
  ("packages before code" — the same move as babykev's `--no-install-project` layer, slide 90,
  said in one line). Never call this Dockerfile multi-stage (digest E14).

## README step tracker (ReadmeTracker, top-left)

Six trackers: four README parts, the guest-lecture walk, and the cleanup. The README's Part
headings are the tracker titles, so "step k of N" matches what the viewer scrolls past.

- **A · Part 1: Understanding the Codebase** (`README.md:19-93`), 5 steps: Clone · docker-shell ·
  Start server · Browser checks · Exit
- **B · Part 2: Identifying Code Quality Issues** (`README.md:96-127`), 6 steps: Build image ·
  flake8 (Option A) · black --check (Option A) · pip install (Option B) · flake8 local ·
  black local
- **C · Part 3: Testing with Pytest** (`README.md:130-230`), 10 steps: Build · Unit tests ·
  Integration tests · Both · Coverage · Start server (Opt 2) · System tests · Clean up ·
  Interactive shell (Opt 3) · Tests inside
- **D · Part 4: Automating with Pre-commit Hooks** (`README.md:233-275`), 5 steps: Install
  pre-commit · pre-commit install · git commit · run --all-files · pre-commit run
- **E · babykev walk (walk.md, steps 00–05b)**, 8 steps: step-00 env · step-01 tests ·
  step-02 format+lint · step-03 the hook · step-04/04b docs · step-05 the model · step-05a
  properties · step-05b marker+images
- **F · Docker Cleanup** (`README.md:568-574`), 3 steps: container ls · system prune · image ls

Steps the README/walk does not have (`git log`, `ls`, the readiness wait, the no-server run,
`git diff`/`git add`, the blocked-commit demo, `pre-commit uninstall`, uv/just installs, `docker
ps`) are marked `extra` in the tracker caption and the narration ("this one isn't in the README").
S02, S03 and S06 are concept scenes with no tracker.

## Scene plan

Notation: `laptop/NN` = `assets/terminal/laptop/NN-*.txt`, `babykev/sNN-MM` =
`assets/terminal/babykev/sNN-MM-*.txt`; line numbers are file lines (line 1 is the `$` command and
is never printed; `[exit N]` is never printed). ▶ = README/walk command with a `your turn` tag at
real checkpoints. CODE(file: a-b) quotes `assets/source/` at the pin. `lecture_ref(9, "a–b")` per
AC215_SERIES rule 9; spans from SLIDES.md.

**S01 · Who gets to say no? (~230 words) — `s01_hook.py` · `Hook`.** Cold open, no tracker.
CODE(`source/cheese-app-ci-cd-history/c3b227f-service.py`, the distance lines): one changed line,
`result = math.sqrt(2 * z)` glowing RED — the bug the class demo really committed
(`source/cheese-app-ci-cd-history/git-log-oneline.txt`). "You type `git commit`. Before that
commit exists — who gets to say *no*, and what can they actually catch?" V1 teaser: an envelope,
an unlabeled turnstile, the HISTORY vault. The lecture's name for it, `lecture_ref(9, "41, 98–99")`:
a gate — anything that can fail and stop you. Optional 10 s of slides 4–6 redrawn: 26 tiles of an
ML project, only 9 light up as data and model; the rest is engineering, and today is about the
engineering. How to follow along: your own clone, Docker Desktop running, Python 3.9+; **no cloud,
no credentials, no bill** — this whole lecture runs on your laptop. Six trackers, `▶ your turn`,
the study guide has every command.

**S02 · The bug that almost shipped (~260) — `s02_bug.py` · `BugAlmostShipped`.** Concept scene +
history panels; `lecture_ref(9, "25, 27–28")`. The repo's story: `git-log-oneline.txt` as a GREY
commit chain (`91eb786` mess re-added → `c2dce32` a crash → `8eb63fc` fixed → `c3b227f` demo bug in
→ `b8458ff` reverted); extra `laptop/02` (HEAD = the pin, 2025-11-13). The picture: point (3,4) on
a plane, the true radius 5 animates; the buggy √50 ≈ 7.07 overshoots the circle, RED.
CODE(tests/integration/test_api.py: 31-38): the test that expects `data["distance"] == 5.0` —
tests are an executable spec, and this one would have said no. Slide 28's lesson, one line: when a
test fails, fix the code, not the test. Then slide 25's three trays — normal, edge, invalid —
with `power()` tests dropping in: nan/inf and zero exponents into *edge*,
CODE(tests/unit/test_utils.py: 69-76) `pytest.raises(TypeError)` into *invalid*.

**S03 · Three kinds of test, and a gate (~290) — `s03_kinds.py` · `ThreeKinds`.** Concept scene,
no terminal; `lecture_ref(9, "66, 95")`. V2 in full: the request token through unit → integration
→ system; the pyramid (lower layers: fast, many, precise about *where*; higher: slow, few, honest
about *whether*); the nested boxes and the GREEN dashed **hermetic border** — hermetic means only
your code can make it fail; the system box crosses the border (a live server can be down for
reasons that are not your bug). Smoke and acceptance as faint rows ("a quick does-it-answer-at-all
run"; "none yet"). Kindly, erratum: the kind is named by what runs, not by the folder — this repo
mostly matches, but `test_system_api.py`'s own docstring says "Integration tests" (lines 2, 26)
and `pytest.ini:20-23` defines markers it never uses; in the lecture's project the folders and the
kinds are allowed to differ. V1: the gate table opens, four columns, empty — "by the end of part 1
this repo has filled it in."

**S04 · Clone, and run the app (~260) — `s04_run_app.py` · `RunTheApp`.** Tracker A1→A5. ▶
`git clone https://github.com/dlops-io/cheese-app-ci-cd.git` → `laptop/01`; `cd` (prompt changes).
Extra `ls` → `laptop/03`: highlight `tests/{unit,integration,system}`, `pytest.ini`,
`.pre-commit-config.yaml`, `Dockerfile` — "everything today is one of these". ▶ `sh docker-shell.sh`
(README:73) → `laptop/part1-01`: the build (16/16), `Container is running!!!`, `Executing command:
/bin/bash`, the `app@…:/app$` prompt (read it: user `app`, uid 1000, not root; the id changes
every run). ▶ `uvicorn api.service:app --host 0.0.0.0 --port 9000 --reload` (README:82) → startup
to `Application startup complete.`. Browser checks (README:88-90) as a schematic browser tagged
`illustration`; the real evidence: extra `curl` panels `laptop/part1-02/03/04` — the welcome JSON,
`{"status":"healthy"}`, and the distance object. Kindly (erratum): README:90 says the endpoint
"returns 5.0"; it returns a JSON object whose `distance` is 5.0 (CODE service.py: 38-50). `^C`, ▶
`exit`; extra `docker ps -a` → `laptop/part1-05` (empty: `--rm`). One warning that pays off in S07:
your files are **not mounted** — `--reload` watches the copy inside the image (digest G1).

**S05 · Formatter vs linter (~300) — `s05_format_lint.py` · `FormatterLinter`.** Tracker B1→B6;
`lecture_ref(9, "29–31")`. Concept first: a formatter *rewrites* code into one layout and never
changes behaviour; a linter *reports* what needs a person. ▶ `docker build -t cheese-app-api:local .`
(README:106) → `laptop/part2-01` (all `CACHED` — same Dockerfile as Part 1). ▶ flake8 at 120
(README:109) → `laptop/part2-02`: `E231 missing whitespace after ','`, `E303 too many blank lines`
in `utils.py` — left messy on purpose (CODE utils.py: 7-14). ▶ black `--check --diff`
(README:112) → `laptop/part2-03`: **2 files would be reformatted** — black got no width, so its
default 88 wants to fold `service.py:15` too. V4 ribbon: fold at 88, unfold at 120, loop. Kindly
(erratum, the big one): the hook and CI use 120 (`.pre-commit-config.yaml:34,43`); README commands
that pass no width get black's 88 and flake8's 79 and give different answers — always pass 120, as
the README's own Quick Reference does. ▶ `pip install black flake8` (README:118) →
`laptop/part2-04` (black 26.10.1, flake8 7.4.1, "at the time of recording"; ORANGE: a host
install). ▶ flake8 local (README:121) → `laptop/part2-05`: the defaults add
`service.py:15:80: E501 (95 > 79)`. ▶ black local (README:124) → `laptop/part2-06`. The funnel on
the pre-demo file (CODE `8eb63fc-service.py`): black sweeps, **two RED survivors remain** — F401
(an unused import) and E501 (a 147-char string) — a formatter cannot delete an import or split
your sentence; the class fixed exactly those two by hand.

**S06 · pytest, under the hood (~280) — `s06_pytest.py` · `PytestInside`.** Concept scene, no
tracker; `lecture_ref(9, "26, 58–61")`. CODE(pytest.ini: 4-17): discovery by convention
(`test_*.py`, `Test*`, `test_*`), `pythonpath = .`, `addopts` (`--strict-markers`, `-ra` — "read
that summary; it is where skips confess"). V3 collector sweep; `broken` stays dark. **PONDER 1
(8 s)**: "README Part 6 appends `def broken(): assert False` to a test file to 'break the build'.
Will the unit-test run go red?" Answer: no — `broken` doesn't match `python_functions = test_*`,
so it is never collected (kindly: the README's own demo needs `test_broken`; digest E2). pytest's
other verbs in 30 s: assert rewriting shows both values; `pytest.approx` for floats;
`pytest.raises` inverts a test (CODE test_utils.py: 69-76). Then the lecture's gift the repo
doesn't use yet, shown as "what it could look like": a `client` fixture in `conftest.py` replacing
the module-global `client = TestClient(app)` (CODE test_api.py: 11), and `parametrize` folding
four cases into one function — V3 wiring, session scope drawn once, default scope as fresh copies.

**S07 · Tests inside the shipping image (~280) — `s07_container_tests.py` · `TestsInImage`.**
Tracker C1→C5, then C9→C10; `lecture_ref(9, "87–90")`. V7 first (concept before command): the code
and tests are **baked in** by four COPY lines (CODE Dockerfile: 27-41); `pip install` from
`pyproject.toml` lands tools in `/home/app/.local`, and the entrypoint's one PATH line makes them
findable (CODE docker-entrypoint.sh: 5-13; `exec "$@"` is how `docker run … pytest` can fail a CI
step). ▶ build (README:169) → `laptop/part3-opt1-01` (`CACHED`). ▶ `docker run --rm
cheese-app-api:local pytest tests/unit/ -v` → `laptop/part3-opt1-02`: **11 passed**. ▶ integration
→ `part3-opt1-03`: **10 passed, 1 warning** ("pytest 9, at the time of recording, counts one
warning the config can't silence — same ten tests"). ▶ both → `part3-opt1-04`: 21 passed, 1
warning. ▶ coverage (README:181) → `part3-opt1-05`: `api/service.py 0%` — the unit tests never
import it; coverage is a *list of lines nobody has asked a question about*, not a score (pays off
in S12). Gate table: the tests row goes in. Option 3 in one beat: ▶ `sh docker-shell.sh`
(README:210) and the same commands inside → `laptop/part3-opt3-01` (same counts); the
`--cov-report=html` trap: the report exists only inside this `--rm` container and vanishes on
`exit` — prefer `term-missing` (digest G13). Comparison card, one line each (erratum, kindly):
this image ships black, flake8, pre-commit and pytest as runtime deps from `>=` pins, no lockfile;
the lecture's project will keep dev tools in groups behind one lockfile (S10). Edit-on-host beat:
the S04 warning pays off — rebuild, or you test yesterday's code (G1).

**S08 · The system test and the silent skip (~320) — `s08_silent_skip.py` · `SilentSkip`.**
Tracker C6→C8; `lecture_ref(9, "94–97")`. Title card: slide 94's question — *can anything but our
code make it fail?* ▶ `docker run -d --name api-server -p 9000:9000 -e DEV=1 …` (README:193) →
`laptop/part3-opt2-02`. Extra readiness wait → `part3-opt2-03` (`until curl -sf …/health` →
healthy): kindly, the README runs the tests right away; CI waits (`ci.yml:150-154`), and so do we —
a race gives silent skips (digest E9). Extra `docker ps` → `part3-opt2-04`. ▶ system tests over
`--network host` (README:196) → `part3-opt2-05`: **5 passed** — V2's wire carries the token for
real. **PONDER 2 (8 s)**: "Same command, but the server is not running. What exactly does pytest
print?" Answer, extra run → `part3-opt2-07`: **`1 passed, 4 skipped`** — four GREY dashed dots,
the headline still green, and only `-ra`'s four `SKIPPED … API not running at localhost:9000`
lines tell the truth. Why: CODE(test_system_api.py: 11-25) — `skipif(not is_api_running())` is
evaluated once, at *collection*; a smoke detector that switches itself off when the battery is
missing will never beep. Hermetic border: 21 tests inside, these 4 outside. The honest remedy is a
marker the run must *select* — babykev shows it in part 2. CI's turnstile in GREY dashed (L21):
CODE(ci.yml: 146-158), `curl -f` fails the job loudly. ▶ `docker stop api-server && docker rm
api-server` (README:199) → `part3-opt2-06`. Gate table: the system row goes in, **outside** the
turnstile, "on every commit? no: not hermetic".

**S09 · The gate on your machine (~330) — `s09_precommit.py` · `PreCommitGate`.** Tracker D1→D5;
`lecture_ref(9, "34, 41–44")`. ▶ `pip install pre-commit` (README:240) → `laptop/part4-01`
(4.7.0). ▶ `pre-commit install` (README:246) → `part4-02`: `pre-commit installed at
.git/hooks/pre-commit`. V5 hand-over chain: the hook file lives in `.git/`, is machine-specific
and never committed — every clone installs again. CODE(.pre-commit-config.yaml: 12-44, cropping
the stale "L17, Slide" comment lines): nine hooks — seven hygiene guards (whitespace, end of
file, YAML/JSON, large files, merge markers, private keys — "that one matters from L10 on") plus
black and flake8 at 120, both only on `files: ^src/.*\.py$` (one kind line: the tests are never
linted, which is how a bare `except:` survives there; digest G15). ▶ `git commit -m "…"`
(README:255) → `part4-03`: the first run downloads the hook environments (`[INFO] Initializing…`),
prints pre-commit 4.7.0's deprecation `[WARNING]` about the v4.5.0 pins ("version drift, at the
time of recording — harmless"), then every hook `(no files to check)Skipped` and `nothing to
commit`: hooks check *staged* files, and nothing was staged. ▶ `pre-commit run --all-files`
(README:262) → `part4-04`: 7 pass, **black `Failed` — "files were modified by this hook"**,
`reformatted src/api-service/api/utils.py`, and flake8 **Passed**. **PONDER 3 (6 s)**: "black
failed on `utils.py`. flake8 runs next — will it report the E231 and E303 from S05?" Answer: no —
black already rewrote the file on disk, so flake8 sees clean code; but nothing is committed until
*you* look and re-stage. Extra `git diff` → `part4-05` (the one-character fix), extra `git add -u`
→ `part4-06`. ▶ commit again → `part4-07`: all nine arches GREEN, `[main b72d50d]` — a real
commit, through the gate, into the vault (V1). ▶ `pre-commit run` (README:265) → `part4-08`
(nothing staged: all Skipped). The refusal, extra (`part4-10`–`13`): `import os` added and staged
→ the commit attempt fails **twice** — black "files were modified" (it re-places the import) and
flake8 `F401 'os' imported but unused`; `git status` shows no commit was made; restore. End of
part 1: "Your machine now says no. But notice what this gate never did: it never ran a test. Part
2: the guest lecture builds a gate that does — and shows what even that one can miss."

**S10 · Guest lecture: uv, just, and two failing tests (~280) — `s10_babykev.py` · `OneCommand`.**
Tracker E1→E3; `lecture_ref(9, "14–20, 25–28")`. Bridge, one sentence (narration only, no name on
screen): the guest lecture — Rahul Dave's — built the same gate around a small ML model, babykev,
with no Docker until the very end; we borrow its words as we go. Prereqs as extras: uv 0.13.2,
just 1.59.0 (`babykev/02`, `04`, "at the time of recording"). ▶ `git clone
https://github.com/rahuldave/babykev` → `babykev/05`; ▶ `git tag -n1 --list 'step-*'` →
`babykev/07`: nine steps, one per lecture stage — the deck's footers name them. step-00: ▶
`git switch --detach step-00` (`s00-01`), ▶ `uv sync --locked` → `s00-02`: Python 3.13.16 and the
project, from `uv.lock` — one lockfile pins everything, and `--locked` *stops* rather than upgrade
silently (the S07 card's other column, GREEN). `just` → `s00-05`: recipes — one name per task, the
same name for people, agents, the hook and CI (slide 20). step-01: `just setup` (`s01-02`), ▶
`uv run pytest` → `s01-03`: **2 failed, 50 passed** — "and the tests are right": a pure guess
reported as half-confident, and 77 rounded probabilities summing to 0.77 (`s01-06` selects the
pair). Slide 28 again, now for real: the fix changed the code, not the tests. step-02 in one beat:
V4 funnel reprise — `ruff check` finds 70 (`s02-12`), `--fix` 69 (`s02-14`), `--unsafe-fixes` 37
(`s02-15`): the rest need a person. One width, written once (`line-length = 100` in
`pyproject.toml`) — the fix for S05's flip-flop.

**S11 · One command is the gate (~290) — `s11_just_check.py` · `JustCheck`.** Tracker E4→E5;
`lecture_ref(9, "34–43")`. step-03: ▶ `just setup` → `s03-02` (now also installs the hook); extra
`cat .git/hooks/pre-commit` → `s03-05`: the same hand-over chain as S09, with this machine's venv
path inside — which is why it is never committed. CODE(babykev/.pre-commit-config.yaml): four
hooks; the last is `entry: just check`, `always_run: true`, `pass_filenames: false` — the hook
runs exactly what you type. V5 side-by-side: nine arches vs four. CODE(justfile: 142-154):
`just check` = fmt --check, lint, tests over a 90% coverage floor, config lint; `set -e`, cheap
checks first. ▶ `just check` → `s03-09`: green, coverage 100%. The floor bites: ▶ `just test -k
confidence --cov-fail-under=90` → `s03-10`: `FAIL Required test coverage of 90% not reached. Total
coverage: 49.40%` — a floor is a gate, not a goal. Config files are checked too (one beat, one
shown): yamllint `--strict` catches one broken line (`s03-12/13/14`); validate-pyproject,
`uv lock --check` and `just --fmt --check` are named (`s03-27/28`) — a broken hook config would
break every commit, so it is checked first. The hook refuses, live: `import os` →
▶ `git commit -am "try"` → `s03-31`: `just check` fails on F401, no commit (`s03-32`); a `.env`
staged → `s03-35`: refused with the config's own sentence — secrets never board. Two styles of
gate (kindly): babykev's check only *points* (`fmt --check`) and you run `just fmt` yourself; the
cheese gate *rewrites* and makes you look before re-staging — both are gates. step-04/04b in two
lines: the docs check joins the gate (`s04-04`: 84 gaps → `s04b-03`: 88 of 88; `s04b-09`: one
deleted docment blocks a commit). Gate table grows: docs, config rows.

**S12 · All green, and the mask is wrong (~290) — `s12_green_wrong.py` · `GreenButWrong`.**
Tracker E6; `lecture_ref(9, "53–55, 72–75")`. step-05: ▶ `just setup` → `s05-02`: the model stack
arrives (torch 2.14.1+cpu and friends, 38 packages, "at the time of recording"; the uv `uv-build`
pin warning shows — real, harmless). ▶ `just test` → `s05-03`: **92 passed**, 94% coverage. The
model in one picture (slides 54–55, redrawn): packing puts the state and every question in one
sequence; the mask's one rule — a question may see the state and itself, never a sibling; "that
one cell is the whole difference" from a plain causal mask. V6: the walk's one-liner ▶ →
`s05-04` prints the built mask: rows 5–6 read `#####.` / `######` — **question 2 sees question 1**.
The cause, one line: `s05-05` / CODE(`babykev-history/step-05-model.py`: 140) — `torch.ones_like`
makes "same question" true for every pair. The picture-check `s05-06` prints WRONG — but nothing
in `just check` runs it (a printout you read by eye is not a test). **PONDER 4 (8 s)**: "Every
line of `branch_mask` ran under the tests — coverage says 94%. Can any coverage number catch this
bug?" Answer: no — coverage counts lines that *ran*, not whether anyone checked what they
produced; it is necessary, never sufficient. Also green-but-blind: `uv run ty check` → `s05-07`:
**6 diagnostics** — and `just check` is green anyway (`s05-11`): types are not in the gate yet.
The smoke: ▶ `just smoke local` → `s05-12`: 503M parameters, 9.3M trainable, **6 of 15 right**
(seeded; the walk's Mac got the same) — chance expects 4.75, nothing is trained; hold that number.

**S13 · Properties, not examples (~300) — `s13_properties.py` · `PropertyTests`.** Tracker E7;
`lecture_ref(9, "78–84")`. step-05a: ▶ `just test` → `s05a-03`: **102 passed, 1 failed** — the kind
platform sentence (see decision below), then on with the lesson. The wrong "fix" is written in
(`s05a-04`): the six-token picture says all ok (`s05a-05`) — it cannot tell; a four-token picture
can (`s05a-06`, row 4 WRONG) — and covering every shape would take 4,686 pictures. State the rule
once instead: CODE(tests/unit/test_mask.py: 10, 58-65) — shapes hypothesis may draw, and the
assert "no allowed pair is a sibling pair". **PONDER 5 (8 s)**: "The wrong fix blocks only the
question *just before*. What is the smallest request shape that still breaks the rule?" Answer:
one state token and three one-token questions — and ▶ `just test -k no_question_sees_another` →
`s05a-08`: hypothesis finds it alone and shrinks to **`shape = (1, [1, 1, 1])`** (file line 25);
V6 dice + the allowed∩siblings overlay. Restore (`s05a-09`). Proof the gate grew teeth: step-05's
mask line put back (`s05a-10`) → ▶ `just test` → `s05a-11`: **8 failed, 95 passed** — the same
commit that sailed through at step-05 is now refused; the gate refuses only what its tests can
see. The real fix is one line (`s05a-13`, `model.py:151`). ty joins the gate: `just types` →
`s05a-14`: All checks passed; `check` now has six lines (`s05a-15`). ▶ `just smoke local` →
`s05a-17`: **4 of 15** — *lower* with the right mask: the 6 was luck, an untrained model's score
means nothing (slide 84).

**S14 · Hooks are local; CI checks again (~250) — `s14_ci.py` · `HooksThenCI`.** Tracker E8, then
GREY dashed; `lecture_ref(9, "20, 94–99")`. step-05b, the honest home for non-hermetic tests: ▶
`just test` → `s05b-03`: "…, 1 deselected" — the real-model test is *deselected by default*
(CODE babykev/pyproject.toml: 50-57, `-m 'not system'`), not skipped at random. ▶ `just test -m
system` → `s05b-06`: **1 passed, 103 deselected** — selected on purpose, the real model actually
ran, and it must *pass*, not skip. That is the honest version of S08's `skipif`. One line each:
hadolint lints the Dockerfile (`s05b-07`; a declined rule carries its reason in a comment); this
capture laptop has no Docker and the recipes say so honestly (`s05b-18/19`) — the walk's image
sizes (1.15/1.84 GB) and its `--network none` experiment (the hermetic proof: `just check` green
with the network off) are shown tagged `recorded`, source `assets/source/babykev-walk/walk.md`
step-05b. Gate table complete (slide 98): six rows, the system row outside the turnstile. Then the
limit of every hook: it runs on *one machine*, and `git commit --no-verify` walks straight past it
— so CI re-runs the checks where nobody can skip them. GREY dashed: the `ci.yml` job graph (build
→ lint | unit | integration | system → summary), "that is Part 5 of this same repo — lecture 21".
Slide 20's promise vs this repo (kindly): the hook, CI and the README each spell the checks their
own way here (pinned black 24.1.1 vs the image's newest; 120 vs none) — one command for everyone
is what you take to your milestone. Coverage floors in one line: babykev chose 90; Milestone 5
asks for at least 70.

**S15 · Tear down, recap, and what's next (~230) — `s15_recap.py` · `Recap`.** Tracker F1→F3. ▶
`docker container ls` (README:571) → `laptop/clean-01` (nothing running — the README's `docker
stop <container_id>` has nothing to stop, narration only). ▶ `docker system prune` (README:573) →
`clean-02`: pause at `[y/N]`, type `y`; `Total reclaimed space: 95.17MB` ("your number will
differ"). ▶ `docker image ls` (README:574) → `clean-03`: the two cheese images (731MB disk / 178MB
content; **crop the `python:3.11-slim-bookworm` row** — capture-only). Extra `pre-commit
uninstall` → `clean-04`. babykev cleanup, said: delete `.venv` (a few hundred MB) and the ~1 GB
model in the Hugging Face cache if you ran the smoke. Nothing was billable this lecture — the
whole gate lives on your laptop, which is the point. "Test yourself", five questions one at a
time with a thumbnail of their picture (answers in exercises.md):
1. Name what runs in a unit, an integration and a system test of this repo, file by file.
2. The system tests "pass" with no server at all. What does pytest actually print, and are those
   four tests hermetic?
3. What does `pre-commit install` actually create, and why must every clone run it (or
   `just setup`) again?
4. black says `Failed — files were modified by this hook`. Is your code broken, and what do you
   do next?
5. babykev at step-05 had 94% coverage and a wrong mask. What kind of test finally saw the bug,
   and why couldn't coverage?
Footer cards: exercises.md, and the study guide (`MLOps_Learning · guides/L09-ci-testing-precommit.md`).
Next, GREY dashed: L10 brings cloud credentials — the `detect-private-key` arch from S09 starts
earning its keep — and L21 runs this very repo's checks on GitHub, where `--no-verify` doesn't
exist.

## Ponder questions (summary)

| # | scene | question (as on the card) | answer (said right after the timer) |
| --- | --- | --- | --- |
| 1 | S06 (8 s) | "README Part 6 appends `def broken(): assert False`\nto a test file. Will the unit tests go red?" | No: `broken` doesn't match `python_functions = test_*` and is never collected; use `test_broken` to really break it (digest E2) |
| 2 | S08 (8 s) | "The same system-test command,\nbut the server is not running.\nWhat exactly does pytest print?" | `1 passed, 4 skipped` — green headline, four SKIPPED lines only in `-ra`'s summary (`laptop/part3-opt2-07`); `skipif` ran once, at collection |
| 3 | S09 (6 s) | "black just Failed on utils.py.\nflake8 runs next — will it report\nthe E231 and E303 from before?" | No: black already rewrote the file, so flake8 sees clean code and passes — but the commit stays blocked until you `git diff`, `git add`, and retry (`laptop/part4-04`) |
| 4 | S12 (8 s) | "Every line of branch_mask ran.\nCoverage reads 94%.\nCan any coverage number catch this bug?" | No: coverage counts lines that ran, not whether their output was checked — necessary, never sufficient (`babykev/s05-03`, slide 73) |
| 5 | S13 (8 s) | "The wrong fix blocks only the question just before.\nWhat is the smallest request shape\nthat still breaks the rule?" | One state token and three one-token questions: hypothesis finds and shrinks it to `shape = (1, [1, 1, 1])` on its own (`babykev/s05a-08`) |

Each is answerable from the picture or capture shown just before it.

## Errata and version drift to state (kindly, with the fix)

1. **Line widths disagree** (digest E5/G9): hook and CI use 120; README commands without a width
   get black's 88 and flake8's 79 and give different answers (README:112 vs :109). Fix: always
   pass 120, or set it once in config as babykev does (`line-length = 100`, written once) (S05).
2. **No readiness wait before the system tests** (digest E9/G3): README:190-196 runs them straight
   after `docker run -d`; a slow server gives silent skips. Fix: wait on `/health` as CI does
   (`ci.yml:150-154`; our extra `part3-opt2-03`) (S08).
3. **"Returns 5.0"** (digest E16): the endpoint returns a JSON object whose `distance` is 5.0
   (S04).
4. **Part 6's `def broken()` breaks nothing** (digest E2): not collected; use `test_broken`
   (Ponder 1, S06).
5. **README lists 5 hooks; the config runs 9** (digest E3), and black/flake8 see only
   `^src/.*\.py$`, so the tests are never linted (G15) — widen `files:` in your own projects
   (S09, one line each).
6. **Stale labels**: the system-test file's docstring says "Integration tests" and `pytest.ini`
   defines markers never used (E11) — name the kind by what runs (S03); the config's "L17,
   Slide …" comments point at last year's deck (E12) — crop/dim them, the `lecture_ref` tag gives
   the right slides; `Dockerfile:1` says "Multi-stage" over a single FROM (E14) — never repeat it.
7. **Dev tools ship in the production image** from `>=` pins with no lockfile (E20) — the
   comparison card; babykev's groups + `uv.lock` are the fix to copy (S07, S10).
8. **`--cov-report=html` inside a `--rm` container** leaves no report (G13) — `term-missing`, or
   mount the folder (S07).
9. **Version drift, "at the time of recording"**: pytest 9.1.1 adds "1 warning" to the
   integration counts (`part3-opt1-03/04`); pre-commit 4.7.0 prints a deprecation `[WARNING]`
   about the pinned v4.5.0 hooks on the first run (`part4-03`); uv 0.13.2 warns about babykev's
   `uv-build` pin on every build; host black is 26.10.1 while the hook pins 24.1.1 — which is
   itself the "one command for everyone" lesson (S05, S09, S12, S14).
10. **Platform note — hermetic ≠ bit-portable** (ASSETS.md "Differences"): babykev's
    `test_a_question_cannot_see_its_sibling` fails on our Linux x86 capture machine at steps
    05a/05b (`1 failed, 102 passed`): it demands bit-exact logits and torch's CPU kernels sum in a
    length-dependent order here; the author's Mac is bit-exact. **Decision (recorded):** S13 shows
    the live `1 failed, 102 passed` honestly and spends one kind sentence turning it into a
    teaching point — "hermetic means only your code can make it fail; bit-exactness *across CPUs*
    is a stronger promise this assertion quietly makes, and our Linux machine just proved it" —
    never as babykev's bug or the student's mistake. Everything the assertion is *about* still
    holds live (`before[0] == after[0]` passes; the wrong mask fails it for the real reason,
    `s05a-11`). Any claim of "103 passed" or "check green" at steps 05a/05b carries the
    `recorded` tag (source: walk.md); live green checks come from steps 03, 04b and 05 only.

## Costs and teardown

**Nothing billable.** No GCP resource, no API key, no paid service: the GOLD cost-tag rule is
satisfied trivially (no scene creates a billable resource, so no GOLD tag appears). What the
tutorial spends is disk, and the teardown is Docker cleanup, fully captured:
- the README's own Docker Cleanup (`clean-01` nothing running, `clean-02` prune reclaims ~95MB,
  `clean-03` the images that remain) (S15);
- extra `pre-commit uninstall` (`clean-04`) and, said only: `pre-commit clean` for the
  `~/.cache/pre-commit` environments;
- babykev, said only: delete `.venv` (a few hundred MB) and `Qwen/Qwen2.5-0.5B` (~1 GB) from the
  Hugging Face cache if the smoke ran.

## README/walk commands checklist (for the follow-along review)

Cheese README, Parts 1–4 + Cleanup (every command verbatim, in README order):

| README command | README line | scene |
| --- | --- | --- |
| Clone (`git clone https://github.com/dlops-io/cheese-app-ci-cd.git`; README:20 gives no URL — narration says so) | 19-20 | S04 |
| `sh docker-shell.sh` | 73 | S04 |
| `uvicorn api.service:app --host 0.0.0.0 --port 9000 --reload` | 82 | S04 |
| Browser checks (three URLs) | 88-90 | S04 (illustration + curl evidence) |
| exit / remove container | 92 | S04 |
| `docker build -t cheese-app-api:local .` | 106 | S05 |
| `docker run --rm cheese-app-api:local flake8 --max-line-length=120 api/` | 109 | S05 |
| `docker run --rm cheese-app-api:local black --check --diff api/` | 112 | S05 |
| `pip install black flake8` | 118 | S05 |
| `flake8 src/api-service/api/` | 121 | S05 |
| `black --check --diff src/api-service/api/` | 124 | S05 |
| Part 3 Option 1: build + 4 pytest commands | 169-181 | S07 |
| Part 3 Option 2: run -d, system tests, cleanup | 190-199 | S08 |
| Part 3 Option 3: `sh docker-shell.sh` + 4 commands inside | 210, 216-225 | S07 (one beat) |
| `pip install pre-commit` | 240 | S09 |
| `pre-commit install` | 246 | S09 |
| `git commit -m "Your commit message"` | 255 | S09 (×2: clean tree, then with the fix staged) |
| `pre-commit run --all-files` | 262 | S09 |
| `pre-commit run` | 265 | S09 |
| Docker Cleanup: `docker container ls`, `docker system prune`, `docker image ls` | 568-574 | S15 |

Parts 5–7 are out of this lecture's scope (Part 5 = L21; Part 7 lives in exercises.md).
babykev walk (steps 00–05b): every walk.md command of those steps is captured as
`babykev/sNN-MM-*.txt` in walk order (`ASSETS.md` is the full list); the scenes show the files
named in the plan above, and whatever a scene does not show is covered by the step tracker E
caption and the study guide. The Quarto/site commands and the step-05b Docker sections are the
documented `recorded` cases (ASSETS.md "What cannot run here").

## Notes for script and scene authors

- Shared code (`scenes/common.py`, started from L02's): tracker factories `tracker_a` … `tracker_f`
  with the step lists above; prompts `P_LAPTOP_HOME`, `P_LAPTOP` (cheese clone), `P_BABYKEV`
  (babykev clone) — container prompts come from each capture; tags `extra_tag`, `illustration_tag`,
  `recorded_tag`, `your_turn`. Set-piece classes: `GateTable` + `Turnstile` (V1), `TestPyramid` +
  `HermeticBorder` + `RequestToken` (V2), `Collector` + `FixtureWiring` (V3), `RibbonFunnel` (V4),
  `HandoverChain` (V5), `MaskGrid` (V6), and L02's `LayerStack` reused small (V7).
- `istep` captures (`part1-01`, `part3-opt3-01`) hold a whole interactive session: pick line
  ranges per typed command; progress bars appear redrawn — crop to the stable lines.
- Long lines (`SKIPPED …` summary lines, pip/pre-commit warnings, the coverage `Missing` columns)
  fold with `wrap`; coverage tables keep their columns, highlight by substring.
- Never print `[exit N]` lines or the capture-only rows (the `python:3.11-slim-bookworm` row of
  `clean-03`; any base-image pull rows). The `s05a-03`/`s05b-03` failure lines are printed only in
  S13's platform beat, nowhere else.
- Redraw every lecture diagram in series style; the memes/comics/cartoons/photos on the slides
  are never shown (their *point* may be spoken). One `lecture_ref` per scene as assigned.
- Chinese glossary heads-up: commit, hook, pre-commit, pytest, fixture, marker, black, flake8,
  ruff, uv, just, lockfile, coverage, CI stay English; 形式检查/格式化工具 vs linter per
  `i18n` glossary conventions when that stage comes.

## Things never to do on screen

Series rules:
- No slide images, memes, comics, the Pavlos cartoon or the speaker's photo: redraw the idea,
  cite slides via `lecture_ref`. No logos (GitHub, Docker, Slack); tools are PURPLE chips.
- No real person's name on screen: the prompt user is `student`; narration may credit "the guest
  lecture" / "Rahul Dave's guest lecture" once (S10) and "the instructor's repo"; the publish
  block carries the written attribution.
- No hand-typed output: every terminal line comes from `assets/terminal/`; the walk-only outputs
  (image sizes, `--network none`, Quarto/site, "103 passed" at 05a/05b) only with the `recorded`
  tag naming walk.md; `expected/` nothing — this episode invented no expected panels.
- No command spelled differently from the README/walk (the only substitution is the walk's
  macOS `sed -i ''` → `sed -i`, which the walk's own README prescribes for Linux — say it once if
  a sed appears).
- No credentials or secrets that look real: the `.env` demo content stays `X=1`.

Lecture-specific:
- **Never claim "103 passed" or a green `just check` live at steps 05a/05b**: on this machine it
  is `1 failed, 102 passed`. Use the `recorded` tag (walk.md) or the live green checks at steps
  03, 04b and 05 (erratum 10's decision).
- Never say "the hook runs the tests" about the cheese repo (its hook runs format and lint only);
  never say "integration tests need running services"; never call the cheese Dockerfile
  multi-stage; never attribute ruff or 100 columns to the cheese repo; never follow the config's
  "L17, Slide …" comments (crop or dim them).
- Never colour a SKIPPED test green or count it as passed; never show the system-test row inside
  the hermetic border.
- Never state version numbers, counts with warnings, timings, reclaimed sizes or smoke
  milliseconds without "at the time of recording" (the smoke *scores* 6/15 and 4/15 are seeded
  and stable; the ms are not).
- Never present the bit-exactness failure as a bug in babykev or a mistake by the student.

## Left for exercises.md (not in the video)

README Part 7 (the `/add/` endpoint with its expected 23 passed, 4 skipped; the pre-existing lint
failure G23/E19); re-injecting the demo bug and predicting which suites catch it (digest 9.1); the
broken auto-format mount (9.2/E1/G2); running the tests on the host (PYTHONPATH + pytest-asyncio,
9.4/G7/G8); unifying the line length in config (9.5); where each check belongs (9.6); the
TestClient fixture (9.7); hypothesis predicting the shrink at the keyboard (9.8); `pre-push` and
`core.hooksPath` (slide 44); babykev's docs site and `just docs publish`; G12 (don't nest the
course repos in your monorepo); G16 (GUI commits can't find `just`).
