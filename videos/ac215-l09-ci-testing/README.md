# AC215 · Lecture 9 — CI & unit testing: the pre-commit gate

A follow-along walkthrough of the Lecture 9 tutorials of Harvard's **AC215 (MLOps & LLMOps, Fall
2026)**, *Automating Software Development: CI, unit testing*, in two parts:

1. [dlops-io/cheese-app-ci-cd](https://github.com/dlops-io/cheese-app-ci-cd), branch `main` @
   [`b8458ff`](https://github.com/dlops-io/cheese-app-ci-cd/tree/b8458ff0cc1898700b32a873b4665f43f50df71e),
   sections *Part 1: Understanding the Codebase*, *Part 2: Identifying Code Quality Issues*, *Part 3:
   Testing with Pytest*, *Part 4: Automating with Pre-commit Hooks* and *Docker Cleanup*. A small
   FastAPI service whose one maths endpoint, `/euclidean_distance/`, calls a helper `power()`: unit,
   integration and system tests run inside the same Docker image that serves the app, black and
   flake8 check the code, and a pre-commit hook puts them in front of every `git commit`. Part 5
   (GitHub Actions) is lecture 21 and is only previewed; Part 7 is an exercise in `exercises.md`.
2. The guest lecture's project, [rahuldave/babykev](https://github.com/rahuldave/babykev), branch
   `main` @
   [`4a14085`](https://github.com/rahuldave/babykev/tree/4a14085bb25620f37dca5c2bfeb27843c82dbe9e)
   (step-05b plus a README table), walked on its tags `step-00` … `step-05b` with the step notes
   `walk.md` from
   [rahuldave/babykev-walk](https://github.com/rahuldave/babykev-walk) @
   [`82adb14`](https://github.com/rahuldave/babykev-walk/tree/82adb14c0f3e73a0a836a3655f7dc4ffcdf76670).
   The same gate around a small machine learning project: one lockfile (`uv sync --locked`), one
   command (`just check`) run by people and by the hook, a coverage floor, config linting, and a
   hypothesis property test that finds the bug 94% coverage let through.

A few panels quote older commits of cheese-app-ci-cd from the repo's own history, for comparison,
not followed: `8eb63fc` (the messy `service.py` before the class demo) and `c3b227f` (the class
demo's commit with the wrong square root); and two older babykev files, step-01's `api.py` and
step-05's `model.py`.

Watch it with the README open and your own clones of cheese-app-ci-cd and (part 2) babykev, Docker
Desktop running and Python 3.9 or newer; part 2 also uses uv and just. Nothing in this lecture needs
a cloud account, credentials or any paid service. The tracker top left shows the README (or walk)
step; pause at every `▶ your turn` to run the command; a gray `extra` tag marks a check that isn't
in the README or the walk, and a gray "Lecture 9 · slides …" tag top right points to the lecture
slides the scene stands on. The cheese tutorial was recorded on 2026-10-19 in a fresh Docker Engine
29.8.2 standing in for a laptop with Docker Desktop. The guest lecture was recorded the same day on a
fresh Debian 12 machine **without Docker** (uv 0.13.2, just 1.59.0): its Docker recipes fail
politely, and the walk's own record of the image sizes and of `just check` without a network is
shown tagged `recorded · walk.md`. At steps 05a and 05b one test that demands bit-for-bit equal
outputs fails on that Linux x86 machine (`1 failed, 102 passed`), where the author's Mac passes all
103 (also tagged `recorded · walk.md`); the video says why, and it is neither babykev's bug nor your
mistake. Series format: [`docs/AC215_SERIES.md`](../../docs/AC215_SERIES.md). Study guide with every
command:
[MLOps_Learning · guides/L09-ci-testing-precommit.md](https://github.com/JunyiZhou-Conny/MLOps_Learning/blob/main/guides/L09-ci-testing-precommit.md).

English narration; Chinese and bilingual subtitles (中文字幕说明见 [`i18n/zh/README.md`](i18n/zh/README.md)).

| file | what it is |
| --- | --- |
| `output/ac215-l09-ci-testing.zh-en.mp4` | **the copy to watch**: 1080p60, English narration, bilingual subtitles (Chinese above, English below) burned in, 30:00 (1800.4 s). Published as a GitHub release asset: no MP4 is kept in Git ([`docs/PUBLISHING.md`](../../docs/PUBLISHING.md)) |
| `output/ac215-l09-ci-testing.mp4` | the same video without burned-in subtitles (1920×1080 at 60 fps, h264/AAC 48 kHz stereo, −16.1 LUFS integrated); load any `.srt` below in your player. Not in Git: rebuild it with `--no-render` (see Rebuild) |
| `output/ac215-l09-ci-testing_part1.mp4` | part 1, 17:56: pytest, black & flake8, and the pre-commit gate (S01–S09). Not in Git: rebuilt with `--no-render` |
| `output/ac215-l09-ci-testing_part2.mp4` | part 2, 12:04: one command, green-but-wrong, and property tests (S10–S15). Not in Git: rebuilt with `--no-render` |
| `output/ac215-l09-ci-testing.srt` | English subtitles (each part has its own `.srt`, `.zh.srt`, `.zh-en.srt` / `.ass`) |
| `output/ac215-l09-ci-testing.zh.srt` | Chinese subtitles (on the English timing) |
| `output/ac215-l09-ci-testing.zh-en.srt` / `.zh-en.ass` | bilingual subtitles |
| `output/chapters.txt`, `chapters_part1.txt`, `chapters_part2.txt` | chapter timestamps |
| `output/transcript.md` | the full narration by chapter |
| `exercises.md` | do these after watching: the five test-yourself questions and the five pause-and-ponder questions, hands-on predict-then-run tasks (put the class bug back, what the silent skip returns, three widths and four answers, the tests that are never linted, breaking each babykev config file once, a marker instead of a skip, README Part 7's new endpoint), debugging (a fix the container didn't notice, a commit refused twice, the `.env` that won't go in, walking around the hook, hadolint refusing the Dockerfile, running the tests on the host) and think questions (where each check should live, hermetic yet different on two machines, one command for everyone, your milestone repo, what's left behind), with answers |
| `digest.md` | the tutorial digest: both repos, every step, a code tour with `path:line`, gotchas, errata |
| `SLIDES.md` | the lecture behind the tutorial: a digest of the guest lecture's slide deck in our own words, with slide numbers, and which scene stands on which slides |
| `assets/terminal/` | the **real** terminal sessions every terminal panel prints from (2026-10-19: a fresh Docker Engine 29.8.2 standing in for the laptop with Docker Desktop for cheese-app-ci-cd; a fresh Debian 12 container without Docker, with uv 0.13.2 and just 1.59.0, for babykev); provenance in [`ASSETS.md`](ASSETS.md) |
| `assets/source/` | the tutorial files the code panels quote, unchanged at the pinned commits (and the history files from `8eb63fc` and `c3b227f`, step-01's `api.py`, step-05's `model.py` and the walk's notes) |
| `BRIEF.md`, `script.md`, `scenes/` | the design, the narration (SAY) + visual plan (SHOW), and the Manim source |
| `i18n/zh/` | the Chinese subtitle text: glossary and sentence-aligned translation |

Git keeps the subtitles, the chapter files and the transcript; the MP4s are release assets.

## Chapters

Paste-ready in `output/chapters.txt` (and `chapters_part1.txt`, `chapters_part2.txt` for the parts).

```
00:00 Who gets to say no?
01:24 The bug that almost shipped
02:55 Three kinds of test, and a gate
04:50 Clone, and run the app
06:40 Formatter vs linter
09:07 pytest, under the hood
10:58 Tests inside the shipping image
13:10 The system test and the silent skip
15:25 The gate on your machine
17:56 Guest lecture: uv, just, and two failing tests
20:04 One command is the gate
22:13 All green, and the mask is wrong
24:27 Properties, not examples
26:39 Hooks are local; CI checks again
28:25 Tear down, recap, and what's next
```

## What you'll learn

Five *pause and ponder* moments ask you to predict before the video shows you: whether the unit
tests go red when README Part 6 appends `def broken(): assert False` to a test file, what pytest
prints when the system-test command runs with no server, whether flake8 still reports part 2's two
findings right after black has failed on `utils.py`, whether any coverage number can catch a wrong
mask when every line of `branch_mask` ran and coverage reads 94%, and the smallest request shape
that still breaks the rule after a fix that blocks only the question just before. Five
test-yourself questions close the video (answers in `exercises.md`).

**Part 1 · pytest, black & flake8, and the pre-commit gate**

1. **Who gets to say no?** — a line committed live, in class: the distance from a point to the
   origin is the square root of x squared plus y squared, and the line takes the square root of
   twice that; nothing crashed, the answer was just wrong; who can say no before a commit exists:
   the lecture's gate, anything that can fail and stop you; in a machine learning system the model
   is a few tiles in a big grid and the rest is engineering; what you need (your clone, Docker
   Desktop, Python 3.9 or newer; no cloud, no credentials, no bill); the tracker's six sections and
   the `▶ your turn` and `extra` tags.
2. **The bug that almost shipped** — the repo's own history: messy code re-added on purpose, a
   crash, a fix, the class demo's wrong square root and the revert, and an extra `git log` showing
   the clone at that last commit, from November 2025; the point (3, 4): true distance 5, the bug
   returns √50 ≈ 7.07, no error, only a wrong number; the integration test that insists on exactly
   5.0, a test as an executable specification; two suspects when a test fails, and the lecture's
   rule: believe the test, fix the code; the three trays of inputs (normal, edge, invalid), and
   `pytest.raises` for `power` on a string.
3. **Three kinds of test, and a gate** — one request, `GET /euclidean_distance/?x=3&y=4`: a unit
   test calls `power(3, 2)` alone; an integration test hands the request to the FastAPI app in
   process through the test client (no server, no network; ten run in under a second, at the time
   of recording); a system test crosses a real wire to port 9000; the testing pyramid; the
   lecture's hermetic border (a test is hermetic when only your code can make it fail), with the
   system test crossing it; smoke and acceptance tests; a test's kind is named by what runs, not by
   its folder (the system test file calls itself integration tests, and `pytest.ini` defines
   markers nobody uses); the empty gate table: what is checked, how, which command, on every commit?
4. **Clone, and run the app** — the README gives no address:
   `git clone https://github.com/dlops-io/cheese-app-ci-cd.git` and `cd cheese-app-ci-cd`; an extra
   `ls -la` (three test folders, a pytest config, a pre-commit config, the Dockerfile);
   `sh docker-shell.sh`: about a minute to build, at the time of recording, then a shell inside
   the container, and its prompt (the user `app`, not root; an ID that changes every run);
   `uvicorn api.service:app --host 0.0.0.0 --port 9000 --reload`, the three README URLs, and three
   extra `curl` calls standing in for the browser (welcome, health, distance); the endpoint returns a
   JSON object whose `distance` is 5.0; Ctrl+C, `exit`, and an extra `docker ps -a` that is empty
   thanks to `--rm`; your files are not mounted: `--reload` watches the copy baked into the image.
5. **Formatter vs linter** — a formatter rewrites code into one layout and never changes behavior;
   a linter only reports; format first, then lint; Option A inside the image:
   `docker build -t cheese-app-api:local .` (every step `CACHED`),
   `docker run --rm cheese-app-api:local flake8 --max-line-length=120 api/` (two findings in
   `utils.py`, mess left on purpose) and `docker run --rm cheese-app-api:local black --check --diff api/`
   (2 files would be reformatted: with no width, black's default 88 also folds a 95-character line
   in `service.py`); the width trap, folded at 88 and unfolded at 120: always pass 120, or set it
   once in config; Option B on the host: `pip install black flake8` (26.10.1 and 7.4.1 at the time
   of recording; if pip refuses with externally managed environment, a lecture 1 virtual
   environment or pipx), `flake8 src/api-service/api/` at its default 79 adds that 95-character
   line, `black --check --diff src/api-service/api/` wants the same two files changed; what a
   formatter can fix: on the messy `service.py` from the repo's history, exactly 2 findings survive
   black, an unused import and a long quoted sentence, and the class fixed both by hand.
6. **pytest, under the hood** — `pytest.ini`'s discovery rules (files `test_*`, classes `Test`,
   functions `test_*`) and `-ra`, the summary of everything not plainly passed; the collector sweeps
   `tests/`: 26 tests; README Part 6's `def broken(): assert False` is never collected, so name it
   `test_broken`; a plain `assert` that shows both values, `pytest.approx` and `pytest.raises`; the
   test client built once as a module global, and what a fixture would do instead (asked for by
   name, built and injected by pytest, fresh per test or shared by the run); `parametrize` folding
   four copies into one function.
7. **Tests inside the shipping image** — Part 3's three routes; the Dockerfile: `pyproject.toml` and
   the dependencies in one fat layer, then four thin copy lines baking in the api code, the tests,
   the pytest config and the entrypoint, whose `exec "$@"` runs whatever command you pass (and
   whose exit code is how `docker run` can fail a CI step); Option 1:
   `docker run --rm cheese-app-api:local pytest tests/unit/ -v` → 11 passed, integration → 10
   passed, 1 warning, both → 21 passed, 1 warning (pytest 9 counting a warning the config hides, at
   the time of recording); the coverage run: `service.py` at 0%, coverage as a list of lines nobody
   has asked about, not a score; the gate table's first row; Option 3, the same commands in
   `sh docker-shell.sh`, the same counts, and an HTML report that lands inside a `--rm` container
   and is gone on exit; dev tools shipped as runtime dependencies with open-ended pins and no
   lockfile; an edit to `utils.py` on your laptop leaves the container testing yesterday's copy:
   rebuild.
8. **The system test and the silent skip** — the lecture's question, can anything but our code make
   it fail?; Option 2: `docker run -d --name api-server -p 9000:9000 -e DEV=1 cheese-app-api:local`;
   two extras the README doesn't have, a loop curling `/health` until it answers (CI waits too) and
   `docker ps`; `docker run --rm --network host cheese-app-api:local pytest tests/system/ -v`: 5
   passed across the wire; `docker stop api-server && docker rm api-server`; the same command with
   no server (extra): `1 passed, 4 skipped`, the headline still green, and only `-ra`'s summary
   says API not running at localhost:9000; why: `skipif` probes the server once, at collection; a
   smoke detector with its battery removed; 22 tests inside the hermetic border, 4 outside; the
   honest remedy is a marker (part 2); CI's loud version, which curls the server first and fails
   the job; the system row enters the gate table outside the turnstile.
9. **The gate on your machine** — outside the container, `pip install pre-commit` (4.7.0 at the
   time of recording) and `pre-commit install`; git runs the hook file before every commit, it
   lives in `.git`, outside the repository, so every clone installs it again, and it hands over to
   pre-commit, which reads the repo's config; nine hooks, seven hygiene guards from whitespace to
   private keys, then black and flake8 at width 120, both seeing only Python files under `src`: the
   tests are never linted; `git commit -m "Your commit message"` on a clean tree: each hook's pinned
   environment downloads once, a harmless warning, every hook skipped, nothing to commit (hooks
   check staged files); `pre-commit run --all-files`: black fails, files were modified by this
   hook; flake8 then passes on the rewritten file, so Failed means changed: look, then re-stage;
   extras `git diff` and `git add -u`, the commit again, and a real commit enters history; plain
   `pre-commit run` checks only staged files; a last extra: an unused import added with `sed` (on a
   Mac, `sed -i` needs empty quotes after it) is refused twice, black reformats and flake8 reports
   F401, and `git status` confirms no commit; your machine now says no, but this gate never ran a
   single test.

**Part 2 · one command, green-but-wrong, and property tests**

10. **Guest lecture: uv, just, and two failing tests** — the guest lecture's babykev, a small
    machine learning project that answers questions about cheese and reports how confident it is (a
    pure guess should score zero); extras `uv --version` and `just --version` (0.13.2 and 1.59.0, at
    the time of recording); `git clone https://github.com/rahuldave/babykev` and
    `git tag -n1 --list 'step-*'`: 9 steps, the repo as its own slide deck,
    `git switch --detach` to move between them; step-00: `uv sync --locked` installs Python 3.13.16
    and the project exactly as the lockfile says (locked means stop rather than silently upgrade),
    the cheese repo froze an image where babykev pins a lockfile, and `just` alone lists the
    recipes; step-01: `uv run pytest` → 2 failed, 50 passed, and the tests are right (a pure guess
    scored as half confident; 77 rounded probabilities that sum to 0.77): fix the code; step-02:
    ruff as formatter and linter, 70 findings, 1 removed by safe fixes, 32 more by unsafe fixes
    applied deliberately, 37 left for a person; the width war settled in one line,
    `line-length = 100` in `pyproject.toml`.
11. **One command is the gate** — step-03: `just setup` syncs the lockfile and installs the hook;
    the hook file, the same hand-over chain with this machine's venv path baked in, so it is never
    committed; four hooks, not nine: large files, merge markers, a policy hook refusing any `.env`
    file, and one local hook that runs `just check` (format check, lint, tests with a 90 percent
    coverage floor, config linting); `just check` green at 100%, then
    `just test -k confidence --cov-fail-under=90` failing at 49.4%: a floor is a gate, not a goal;
    one wrong indent in the pre-commit config and `uv run yamllint --strict .` names the line;
    `just lint-config` also validates `pyproject.toml` and checks the lockfile; two refusals, an
    unused import (F401, no commit made) and a staged `.env` refused with the config's own
    sentence; two gate styles (babykev points and you run `just fmt`; the cheese gate rewrites and
    makes you look); steps 04 and 04b put documentation in the gate, 50 of 88 then 88 of 88, and
    deleting one description blocks a commit; the docs and config rows join the table.
12. **All green, and the mask is wrong** — step-05 brings the model: `just setup` pulls 38 packages
    including torch 2.14.1 for the CPU, at the time of recording; `just test` → 92 passed, coverage
    94%; the model in one picture: one state and several questions packed into one sequence, and a
    mask whose rule is that a question sees the state and itself, never a sibling; the walk's
    one-liner prints the mask the code builds, and rows 5 and 6 let question 2 see question 1; the
    cause, one line with `torch.ones_like`; a checker script prints WRONG, but nothing in
    `just check` runs it; coverage counts lines that ran, never whether anyone checked what they
    produced; `uv run ty check` finds 6 diagnostics while `just check` stays green (types are not in
    the gate yet); `just smoke local`: half a billion parameters from the Hugging Face Hub, 15 cheese
    questions on CPU, 6 of 15 right, and nothing is trained: these are guesses.
13. **Properties, not examples** — step-05a, honestly: `just test` here says 1 failed, 102 passed,
    because one test demands bit-for-bit equal outputs and torch on this Linux CPU sums in a
    different order than the author's Mac, where all 103 pass (as the walk records); hermetic means
    only your code can make it fail, bit-exactness across machines is a stronger promise; a
    deliberately wrong fix that blocks only the question just before: the six-token picture says all
    ok, a four-token picture reads WRONG; the property test states the rule once and lets hypothesis
    draw any request shape (a state of 1 to 6 tokens, up to 4 questions of 1 to 5: 4,686 shapes);
    `just test -k no_question_sees_another` fails and shrinks the counter-example to
    `shape = (1, [1, 1, 1])`, the smallest witness; step-05's wrong mask line put back → 8 failed,
    95 passed: a gate refuses only what its tests can see; the real fix, same question means same
    segment ID; `just types` passes and `check` has six lines; the smoke with the right mask, 4 of
    15: the 6 was luck.
14. **Hooks are local; CI checks again** — step-05b: a real-model test marked `system` and
    deselected by default, so every `just test` says 1 deselected; `just test -m system` → 1 passed,
    103 deselected, the honest version of part 1's silent skip; `uv run hadolint Dockerfile`, clean;
    without Docker, `docker build --target run --tag babykev-run .` is command not found and
    `just image build run` explains itself; the walk's record: two images from one lockfile, 1.15 and
    1.84 GB, and `just check` green inside a container with no network; the gate table complete, six
    rows, the system row outside the turnstile; the limit: `git commit --no-verify` walks past a
    hook; CI re-runs the same checks on a server nobody can skip (Part 5 of this repo, lecture 21),
    and why the hook, CI and the README should spell the checks one way; coverage floors: babykev
    chose 90, milestone 5 asks at least 70.
15. **Tear down, recap, and what's next** — the README's Docker Cleanup: `docker container ls`
    (nothing to stop), `docker system prune` (type y; about 95 MB of build cache, at the time of
    recording) and `docker image ls` (the two cheese images); an extra `pre-commit uninstall`; on
    the babykev side, delete the venv and, if you ran the smoke, the roughly 1 GB model in the
    Hugging Face cache; nothing billable; five test-yourself questions; next, lecture 10's cloud
    credentials, where the detect-private-key hook earns its keep, and lecture 21, where this repo's
    checks run on GitHub and `--no-verify` can't walk past them.

The README's small mistakes are pointed out kindly, with the fix: it says to clone your repository
but gives no address (the clone command is above); "returns 5.0" is really a JSON object whose
`distance` field is 5.0; several commands pass no line width, so black falls back to 88 and host
flake8 to 79 while the hook and CI use 120 (always pass 120, or set it once in config);
the system test file calls itself integration tests and `pytest.ini` defines markers nobody uses
(name a test's kind by what runs); Part 6's `def broken(): assert False` is never collected (call
it `test_broken`); `--cov-report=html` writes its report inside a `--rm` container that is gone on
exit (prefer the terminal report); the image ships its dev tools as runtime dependencies, with
open-ended pins and no lockfile (babykev's dependency groups and one lockfile are the fix to copy);
the system tests run straight after the server starts, so a server that comes up late gives silent
skips (wait on `/health`, as CI does); the black and
flake8 hooks see only Python files under `src`, so the tests are never linted; and the hook pins
black 24.1.1 while the image installs the newest, which is the lesson itself: one command for
everyone. Version drift is said "at the time of recording": pytest 9's "1 warning", pre-commit
4.7.0's warning on the first run and uv 0.13.2's warning on every babykev build are harmless.

## Rebuild

```bash
python -m explainer.build videos/ac215-l09-ci-testing -q l                          # fast draft
python -m explainer.build videos/ac215-l09-ci-testing --render-only --jobs 3        # 1080p60 scene renders
python -m explainer.build videos/ac215-l09-ci-testing --no-render --crf 27 --burn   # stitch: video, parts, subtitles, burned-in copy, chapters, transcript
python -m explainer.build videos/ac215-l09-ci-testing --subs-only                   # rewrite subtitles only
python -m explainer.i18n check videos/ac215-l09-ci-testing --lang zh                # Chinese text aligned with the English
```

No MP4 is in Git (the burned-in copy is a release asset): after a fresh clone, render the scenes
once, then the `--no-render` line rebuilds the clean video, the two part cuts and the burned-in copy
from the scene renders.

Narration: Kokoro (`af_heart`, speed 0.9), generated locally.

*Course materials belong to the AC215 teaching staff (Harvard IACS); the cheese-app-ci-cd tutorial
is used for study with the instructor's permission, and babykev and babykev-walk, the guest
lecture's public repositories, are quoted at their pinned commits. The lecture's slides are redrawn
in our own pictures, never shown. The browser is a schematic drawing (tagged `illustration`), not a
screenshot; no cloud account, credential or paid service was used.*
