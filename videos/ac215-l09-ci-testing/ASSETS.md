# Assets and where they come from

Everything a scene shows as "real" (a terminal output, a source line, a file listing) is read from
a file in `assets/`, never typed by hand into a scene. This file says where each one came from.

## `source/` — the tutorials' own files

### `source/cheese-app-ci-cd/` and `source/cheese-app-ci-cd-history/`

From [dlops-io/cheese-app-ci-cd](https://github.com/dlops-io/cheese-app-ci-cd) at commit
`b8458ff0cc1898700b32a873b4665f43f50df71e` (main, 2025-11-13; still the head of `main` on
2026-10-19, verified with `git ls-remote` and in `terminal/laptop/02-git-log.txt`), copied
unchanged with `git show <commit>:<path>`, relative paths preserved. Course material by the AC215
teaching staff (Harvard IACS), used for study with the instructor's permission.

| file | what a panel quotes from it |
| --- | --- |
| `README.md` | the covered sections: Prerequisites (5-9), Clone (19-20), the project tree (22-47), Part 1 (51-93), Part 2 (96-127), Part 3 (130-230), Part 4 (233-275), Docker Cleanup (564-574) |
| `Dockerfile` | the one image for dev, tests and serving: base (2), apt + pip layers (12-20), user `app` (23-26), `COPY pyproject.toml` before the code (32-35), the four `COPY` lines that bake code in (38-41), `ENTRYPOINT` (52) |
| `docker-shell.sh` | `IMAGE_NAME` (7), build (11), `docker run --rm -ti … -p 9000:9000` (15-18) |
| `docker-entrypoint.sh` | the `PATH` line (5), `exec "$@"` (10-13), DEV/PROD uvicorn branches (16-24) |
| `pyproject.toml` | dev tools mixed into runtime deps (7-19), `>=` pins, no lockfile |
| `pytest.ini` | discovery rules (5-8), `pythonpath = .` (9), `addopts` (12-17), the unused markers (20-23) |
| `.pre-commit-config.yaml` | the 9 hooks (12-44): 7 hygiene + black 24.1.1 at 120 + flake8 7.0.0 at 120, both `files: ^src/.*\.py$` |
| `.github/workflows/ci.yml` | lecture 21, shown for the skip lesson: build (15-38), lint (54-66), the system job's sleep + `curl -f` + `--network host` run (146-158), summary (171-257) |
| `src/api-service/api/service.py` | the FastAPI app: `/` (28-30), `/health` (33-35), `/euclidean_distance/` (38-50) |
| `src/api-service/api/utils.py` | `power()` with the intentional E231/E303 mess (7-14) |
| `tests/unit/test_utils.py` | the 11 unit tests; `pytest.raises` (69-76), booleans (86-90) |
| `tests/integration/test_api.py` | `client = TestClient(app)` (11), the distance test (31-38), `@pytest.mark.asyncio` (83) |
| `tests/system/test_system_api.py` | `API_BASE_URL` + `is_api_running()` + the class `skipif` (11-25), the "Integration tests" mislabel (2, 26) |

`source/cheese-app-ci-cd-history/` holds the class-demo versions, each from `git show <sha>:path`,
named `<sha>-<file>`: `8eb63fc-service.py` and `8eb63fc-utils.py` (the pre-demo messy version the
digest's §3.4 lint numbers were measured on), `c3b227f-service.py` (the in-class commit that
cleaned `service.py` and injected `math.sqrt(2 * z)`), and `git-log-oneline.txt` (the history the
video narrates: `91eb786` → `c2dce32` → `8eb63fc` → `c3b227f` → `b8458ff`).

### `source/babykev/`, `source/babykev-history/` and `source/babykev-walk/`

From [rahuldave/babykev](https://github.com/rahuldave/babykev) at commit
`4a14085bb25620f37dca5c2bfeb27843c82dbe9e` (main = step-05b + a README table, 2026-10-06; still
the head of `main` on 2026-10-19, verified in `terminal/babykev/06-git-log.txt`), and
[rahuldave/babykev-walk](https://github.com/rahuldave/babykev-walk) at
`82adb14c0f3e73a0a836a3655f7dc4ffcdf76670` (main, 2026-10-06). Guest-lecture material by Rahul
Dave.

| file | what a panel quotes from it |
| --- | --- |
| `babykev/justfile` | the interface: `setup` (28-34), `image` (36-…), `lint-config` (120-128), `check` (142-154), `smoke` (181-189) |
| `babykev/pyproject.toml` | dependency groups (26-40), `[tool.pytest.ini_options]` with `-m 'not system'` and the marker (50-57), `line-length = 100` (65) |
| `babykev/.pre-commit-config.yaml` | the 4 hooks, `no-env-file` (`language: fail`) and `just check` (`language: system`, `always_run`) |
| `babykev/.python-version`, `babykev/Dockerfile`, `babykev/.dockerignore` | Python 3.13; the run image (11-39) and dev image (41-77), the `hadolint ignore=DL3008` comment (46-48) |
| `babykev/src/babykev/api.py`, `model.py`, `smoke.py` | the contract; `branch_mask` docstring (131-135 at step-05 numbering) and the fix (151 at HEAD), `delimiter_ids`/`load_tokenizer` guards (64-80); `BASE = "Qwen/Qwen2.5-0.5B"` (smoke.py:25) |
| `babykev/tests/conftest.py`, `tests/tiny.py` | the `tok`/`model`/`record` fixtures (16-40), the hypothesis deadline-off profile (43-51), the tiny tokenizer/backbone |
| `babykev/tests/unit/test_mask.py`, `test_model.py` | `shapes` (10), the property test (58-65); the isolation test (145-157), forgery tests (96-112) |
| `babykev/tests/system/test_real_model.py` | `pytestmark = pytest.mark.system` (14) and the docstring that says why it is apart |
| `babykev/README.md` | the "without the page" commands (148-150) |
| `babykev-history/step-01-api.py` | step-01's `api.py` with the two real bugs (`score_confidence` 82-86, rounding 89-99) |
| `babykev-history/step-05-model.py` | step-05's `model.py` with the wrong mask, line 140 |
| `babykev-history/step-tags.txt` | the step tags with their one-line messages |
| `babykev-walk/walk.md`, `README.md`, `justfile` | the step notes the captures follow; prerequisites (README:10-14), the Linux `sed -i` note (README:66), the unpinned timewalk (justfile:8-9) |

There is no Colab notebook for this lecture.

## `terminal/` — real terminal sessions

Captured on **2026-10-19** (laptop 21:21-21:40 UTC; babykev 21:42-22:30 UTC, after two earlier
partial runs the same evening were discarded and redone as one clean pass) by
`terminal/capture.sh`, which starts a fresh disposable container per track and runs
`terminal/run_steps.sh` inside it, one segment at a time. Each README/walk command runs exactly as
written, in README/walk order, and its output goes to its own file: the file starts with the
command (`$ ...`), then the output, then its exit status (`[exit N]`). Steps that are not in the
README/walk are marked *extra* below and in `run_steps.sh`.

Two kinds of file, as in L02:

- **`step` files**: the command runs without a terminal, like in a script (BuildKit's plain
  `#N … DONE` log, pytest's plain output).
- **`istep` files**: the command runs in a real pseudo-terminal (`ptyrun.py`, 80×24 or 100×50 as
  noted), and the lines a person would type at the prompt are typed when the prompt appears
  (`uvicorn …`, `pytest …`, `exit`, the `y` of `docker system prune`, Ctrl-C as the `^C` byte).
  The file holds what the terminal shows at the end; progress bars appear redrawn, colours are
  dropped.

| folder | environment | source it follows |
| --- | --- | --- |
| `laptop/` | a fresh, empty Docker engine standing in for the student's machine with Docker Desktop: `docker:29.8.2-dind` (client + engine 29.8.2, linux/amd64), user `student` in the `docker` group, git 2.54.0, and a Python 3.14.8 virtualenv first on `PATH` (see capture-only notes) | cheese-app-ci-cd README: clone, Parts 1-4, Docker Cleanup |
| `babykev/` | a fresh `python:3.12-slim-bookworm` container standing in for a laptop **without Docker**: user `student`, git 2.39.5, curl; uv 0.13.2 and just 1.59.0 installed as captured prerequisite steps; babykev's own Python 3.13.16 comes from `uv sync` | the guest lecture: `babykev-walk/walk.md` steps 00-05b, run on a plain clone of babykev per `babykev/README.md:148-150` |

### `laptop/` — cheese-app-ci-cd, clone + Parts 1-4 + cleanup

| file | README step | what it shows |
| --- | --- | --- |
| `00-env.txt` | extra | date, `Linux x86_64`, Docker 29.8.2, git 2.54.0, Python 3.14.8 |
| `01-clone.txt` | "Clone or download" (README:20 gives no URL; this is the repo's address, also used by the course site) | `Cloning into 'cheese-app-ci-cd'...` |
| `02-git-log.txt` | extra | HEAD = `b8458ff0…` 2025-11-13: the clone equals the pin, no checkout needed |
| `03-ls.txt` | extra | the tree of README:22-47, plus `.gitignore`, `assets/`, `README.md` |
| `part1-01-docker-shell.txt` | Part 1: `sh docker-shell.sh` (README:73), then typed inside: `uvicorn api.service:app --host 0.0.0.0 --port 9000 --reload` (README:82), Ctrl-C, `exit` (README:92) | 100×50 terminal: the compact build (59 s, 16/16), `Container is running!!!`, `Executing command: /bin/bash`, the `app@…:/app$` prompt, uvicorn's startup to `Application startup complete.`, the three `GET … 200 OK` access lines from the curls, `^C`, the clean shutdown, `exit` |
| `part1-02/03/04-curl-*.txt` | extra (README:88-90 says "Open your browser"; a browser cannot run here, so the three URLs are fetched with `curl -s` from a second shell while the server runs — these are the browser checks' evidence) | the welcome JSON, `{"status":"healthy"}`, and `{"x":3.0,"y":4.0,"distance":5.0,"message":…}` — the endpoint returns an object, not the bare `5.0` README:90 promises (digest E16) |
| `part1-05-ps-after.txt` | extra | `docker ps -a` empty: `--rm` removed the container, as README:92 asks |
| `part2-01-build.txt` | Part 2 Option A (README:106) | `docker build -t cheese-app-api:local .`: all layers `CACHED` (the same Dockerfile was built in Part 1) |
| `part2-02-flake8.txt` | README:109 | `api/utils.py:7:15: E231 …`, `api/utils.py:13:1: E303 …`, exit 1 |
| `part2-03-black.txt` | README:112 | black at its default 88: diffs for `utils.py` **and** `service.py`, `2 files would be reformatted, 1 file would be left unchanged.`, exit 1 (the width mismatch of digest E5) |
| `part2-04-pip-install.txt` | Part 2 Option B (README:118) | `pip install black flake8` → black 26.10.1, flake8 7.4.1 |
| `part2-05-flake8-local.txt` | README:121 | flake8 at its default 79 adds `service.py:15:80: E501 (95 > 79)` to the two utils findings |
| `part2-06-black-local.txt` | README:124 | same two reformat diffs as Option A |
| `part3-opt1-01-build.txt` … `05-coverage.txt` | Part 3 Option 1, the five commands (README:169-181) verbatim | build `CACHED`; **11 passed** (unit); **10 passed, 1 warning** (integration); **21 passed, 1 warning** (both); coverage (`--cov-report=term`, no Missing column): `api/service.py 0%`, `api/utils.py 75%`, `11 passed` |
| `part3-opt2-01-build.txt` … `06-cleanup.txt` | Part 3 Option 2, the four commands (README:190-199) verbatim | build `CACHED`; the detached server's container id; **5 passed** system tests over `--network host`; `docker stop api-server && docker rm api-server` |
| `part3-opt2-03-wait.txt` | extra — the README runs the tests right away; this readiness wait mirrors `ci.yml:150-154` and is why `05-system` shows 5 passed instead of a race-dependent skip (digest E9) | `until curl -sf http://localhost:9000/health; do sleep 1; done` → `{"status":"healthy"}` |
| `part3-opt2-04-ps.txt` | extra | `api-server` up, `0.0.0.0:9000->9000/tcp` |
| `part3-opt2-07-system-no-server.txt` | extra — the same README command with no server: the silent skip README:202 warns about | **1 passed, 4 skipped**, with the four `SKIPPED … API not running at localhost:9000` lines from `-ra` |
| `part3-opt3-01-shell.txt` | Part 3 Option 3 (README:210, 216-225), typed inside the interactive container | 100×50 terminal: cached build, then `pytest tests/unit/ -v` (11 passed), `tests/integration/` (10 passed, 1 warning), both (21 passed, 1 warning), `--cov-report=html` (`Coverage HTML written to dir htmlcov`), extra `ls htmlcov/ | head -4` (the report exists only inside this `--rm` container, digest G13), `exit` |
| `part4-01-pip-install-pre-commit.txt` | README:240 | pre-commit 4.7.0 |
| `part4-02-pre-commit-install.txt` | README:246 | `pre-commit installed at .git/hooks/pre-commit` |
| `part4-03-git-commit-clean.txt` | README:255, run exactly where the README puts it, with a clean tree | the first hook run: `[INFO] Initializing/Installing environment for …` (the one-time downloads), pre-commit 4.7.0's deprecation `[WARNING]` about the v4.5.0 hooks' stage names, every hook `(no files to check)Skipped`, then `nothing to commit, working tree clean`, exit 1 |
| `part4-04-run-all-files.txt` | README:262 | 7 hygiene hooks pass (`Check JSON syntax` Skipped), **black Failed — files were modified**, `reformatted src/api-service/api/utils.py`, flake8 (running after, on the fixed file) **Passed**; exit 1 |
| `part4-05-git-diff.txt` | extra | the fix black made: `power(base,exponent)` → `power(base, exponent)`, one blank line removed |
| `part4-06-git-add.txt` | extra | `git add -u` re-stages it |
| `part4-07-git-commit.txt` | README:255 again, now with the fix staged | all 9 hooks run and pass, `[main b72d50d] Your commit message, 1 file changed` — a real commit created through the gate |
| `part4-08-run-staged.txt` | README:265 | `pre-commit run` with nothing staged: every hook `(no files to check)Skipped` |
| `part4-09-git-log.txt` | extra | the new commit on top of `b8458ff` |
| `part4-10-break.txt` … `13-restore.txt` | extra — the commit flake8 blocks (the digest A10 demo) | `sed -i '1i import os' service.py && git add -u`; the commit attempt: black Failed (it also re-places the import) **and flake8 Failed with `F401 'os' imported but unused`**, commit aborted; `git status` shows no commit; both stage and worktree restored |
| `clean-01-container-ls.txt` | Docker Cleanup (README:571) | nothing running (so README's `docker stop <container_id>` on line 572 has nothing to stop — not captured, nothing to act on) |
| `clean-02-prune.txt` | README:573 | typed `y`; `Deleted build cache objects`, `Total reclaimed space: 95.17MB` |
| `clean-03-image-ls.txt` | README:574 | `cheese-app-api-service`, `cheese-app-api:local` (both 731MB disk / 178MB content) and the capture-only `python:3.11-slim-bookworm` row |
| `clean-04-uninstall.txt` | extra (digest A13) | `pre-commit uninstalled` |
| `capture-only/` | not part of the tutorial | `base.Dockerfile` + `base-build.txt`: the capture-only base image, see below |

### `babykev/` — the guest lecture, walk.md steps 00-05b

Setup files (the walk's prerequisites, `babykev-walk/README.md:10-14`, which names uv, git, just
and Quarto but no install commands; the commands used are uv's own installer and
`uv tool install rust-just`, the same way babykev's own Dockerfile installs just):

| file | step | what it shows |
| --- | --- | --- |
| `00-env.txt` | extra | date, Debian 12, git 2.39.5 |
| `01-install-uv.txt`, `02-uv-version.txt` | prerequisite | uv 0.13.2 installed to `~/.local/bin` |
| `03-install-just.txt`, `04-just-version.txt` | prerequisite | `rust-just==1.59.0`, `just 1.59.0` |
| `05-clone.txt` | `git clone https://github.com/rahuldave/babykev` (the walk clones via `just setup` in babykev-walk; `babykev/README.md:148-150` is the equivalent "without the page" route used here) | the clone |
| `06-git-log.txt` | extra | HEAD = `4a14085…` 2026-10-06: the clone equals the pin |
| `07-tags.txt` | `git tag -n1 --list 'step-*'` (babykev README:148) | the nine steps with their messages |

Per-step files `sNN-*`: each step starts with `git switch --detach step-NN` (babykev README:150)
and the walk's `just setup`, then the step's walk.md commands in walk order. The walk's macOS
`sed -i ''` is written `sed -i`, as the walk's own README:66 says to do on Linux. Highlights (every
file is `$ command`, output, `[exit N]`; the full list is the folder):

| files | step / walk section | what they show |
| --- | --- | --- |
| `s00-01` … `s00-09` | step-00 | `uv sync --locked` (Python 3.13.16 + babykev alone), `just --show setup`, `just setup` (`Checked 1 package`), the recipe list, `uv run babykev help`, `babykev train` refused with exit 2, `cat pyproject.toml` |
| `s01-01` … `s01-07` | step-01 | `just setup` (+13 packages), **`uv run pytest` → 2 failed, 50 passed** with the coverage table ("52 runs, two fail, and the tests are right"), `addopts` found in pyproject, the `test` recipe, the two failures selected with `-k`, the four help tests (`4 passed, 48 deselected`) |
| `s02-01` … `s02-20` | step-02 | the two fixes pass; `just test` → 52 passed, `api.py` 1 missed (line 90); `ruff format --check` → 1 file would be reformatted; `just fmt` → reformatted, tests still pass; **`ruff check --statistics` → 70 errors**; `just lint --fix` → 1 fixed/69; `--unsafe-fixes` → 32 fixed/37; after both, format and tests still green; the hand-written `__init__.py` docstring drops it to 36 |
| `s03-01` … `s03-36` | step-03 | `just setup` installs the hook; `just lint` green; `ls`/`cat` of `.git/hooks/pre-commit`; `just test` → 53 passed, Missing empty; **`just check` green** (coverage 100.00%); the floor failing at 49.40% on `-k confidence`; yamllint, validate-pyproject, `uv lock --check` and `just --fmt --check --unstable` each clean → broken by one `sed` → caught → restored; `just lint-config`; `cat .pre-commit-config.yaml`; **the commit the hook refuses** (`import os` → `just check...Failed`, `F401`, no commit made) and **the `.env` commit refused** by the `no-env-file` hook with the sentence from the config |
| `s04-01` … `s04-04` | step-04 (skimmed, per the digest) | `just setup` (+fastcore, and "Quarto is not on this machine…"), `babykev docs list` (41 symbols), **`just docs check` → 84 gaps, `50 of 88`, exit 1** |
| `s04b-01` … `s04b-11` | step-04b | `just docs check` → **88 of 88**, exit 0; a docment (`render`, api.py:68-72); `just check` green with `docs check` in it; one docment deleted → `87 of 88` → **the hook refuses the commit at `docs check`**; restored |
| `s05-01` … `s05-12` | step-05 | `just setup` brings the model stack (38 packages installed: torch 2.14.1+cpu, transformers 5.18.0, peft 0.21.2, hypothesis 6.168.4, ty 0.0.84…); **`just test` → 92 passed, 94% coverage** (model.py 96%, smoke.py 71%); the walk:589 one-liner printing the wrong mask (rows 5-6 `#####.`/`######`); model.py:140 (the `torch.ones_like` line); the six-token picture comparison → rows 5-6 **WRONG**; **`uv run ty check` → Found 6 diagnostics**; `just --show check` (no `types` line yet); **`just check` green anyway**; `just smoke local` on the real Qwen2.5-0.5B, CPU: `503M parameters, 9.3M of them trainable`, **6 of 15 right** (the walk's Mac got 6 of 15 too), "Nothing is trained yet: these are guesses." |
| `s05a-01` … `s05a-17` | step-05a | `just test` → 102 passed **and 1 environment-dependent failure, see below**; the wrong fix written in → six-token picture all `ok` (it cannot tell) → four-token picture row 4 **WRONG** → **`just test -k no_question_sees_another`: hypothesis shrinks to `shape = (1, [1, 1, 1])`**; restored; step-05's mask written back → **`just test` → 8 failed, 95 passed** (the three mask tests, four isolation tests, the notebook test — the walk's exact count); restored; model.py:151 (the one-line fix); **`just types` → All checks passed!**; `check` now has six lines; `just smoke local` → **4 of 15 right** (the walk's Mac: 4 of 15) |
| `s05b-01` … `s05b-19` | step-05b | `just setup` adds hadolint-bin 2.15.1; `just test` → "…, 1 deselected" (the `system` marker works); pyproject:53-57 and the system test file; **`just test -m system` → 1 passed, 103 deselected** — the real model, from the cache, actually ran; `hadolint Dockerfile` clean; the DL3059 and DL3008 breaks each caught and restored; `just lint-config` green; `just check` (same one environment-dependent failure); **`docker build …` → `docker: command not found` (exit 127)** and **`just image build run` → "image: there is no docker here…" (exit 2)** — this laptop has no Docker, which is the honest state the recipe itself handles |
| `capture-only/prewarm.txt` | not part of the walk | the capture-only cache prewarm log, see below |

## What cannot run here, and what was recorded instead

- **Browser steps.** README Part 1's "Open your browser" (README:88-90) and the walk's
  `just present` page, `open docs/_site/...` and the timewalk terminals are browser UI. Evidence
  captured instead: the three `curl -s` fetches (`laptop/part1-02…04`, marked extra) show exactly
  the JSON the browser would render. The walk was followed "without the page" on the tags, the
  route `babykev/README.md:148-150` documents. Scenes that show a browser draw it as a schematic
  tagged `illustration`.
- **Quarto / the docs site.** Quarto is deliberately absent from the babykev laptop (installing it
  is heavy and no planned scene renders the site). `just setup` honestly prints "Quarto is not on
  this machine; just docs needs it" from step-04 on. The site-rendering walk commands
  (`uv run python docs/apidocs.py build`, `uv run quarto render docs`, `just docs`, `open …`,
  `just docs publish`) are **not captured**; what they print is in `walk.md` steps 04/04b/05a/05b
  (tag `recorded`, source: `assets/source/babykev-walk/walk.md`). `just docs check`, `docs list`
  and `docs module` need no Quarto and are captured for the checks the video teaches.
- **The walk's Docker sections (step-05b B-F, I-J).** The babykev container stands in for a laptop
  without Docker, so the image builds, `just image shell`, the `--network none` experiment and the
  amd64 build cannot run in it (and Docker-in-Docker checks that need `--network host` are out of
  bounds in this sandbox). Captured honestly instead: `s05b-18` (`docker: command not found`) and
  `s05b-19` (the recipe's own no-Docker message). The walk's outputs for those sections — image
  sizes 1.15/1.84 GB, the smoke in the run image (4 of 15, identical answers, cpu), `just check`
  green inside `--network none`, the `HF_HOME=/tmp/empty` failure text — are tagged `recorded`,
  source: `assets/source/babykev-walk/walk.md` step-05b.
- **walk.md's "103 passed" at steps 05a/05b** is tagged `recorded` where a scene claims it: on
  this machine one test fails for an environment reason (below). Every other count was captured
  live.
- **Display-only walk commands** (`sed -n 'N,Mp' file` prints of source lines) were captured where
  a scene plan needs the terminal form (`s02-06`, `s04b-04`, `s05-05`, `s05a-07`, `s05a-13`,
  `s05b-04`, `s05b-05`, `s05b-11`); other quotations come from `assets/source/` at the pin, which
  is the same text.
- **cheese README Part 5-7** are out of this lecture's scope (Part 5 is lecture 21; Part 7 is the
  exercise and lives in `exercises.md`); `README:572`'s `docker stop <container_id>` had nothing
  to stop (see `clean-01`).

## Capture-only deviations (the recording sandbox vs a student's machine)

The sandbox reaches the internet only through a TLS-intercepting HTTPS proxy on the host's
loopback. None of the tutorial's commands were changed; the environment around them was:

- **Proxy relay and Docker client proxies.** `proxy_relay.py` (container `l09-relay`) forwards the
  bridge gateway to that proxy. The laptop engine gets it through `~/.docker/config.json`'s
  `proxies` setting (the same setting Docker Desktop has under Settings › Resources › Proxies),
  which passes `HTTPS_PROXY`/`NO_PROXY` into builds and containers without changing any command.
  Nothing of this shows in the outputs.
- **The proxy's CA** replaces `/etc/ssl/certs/ca-certificates.crt` in both containers (all TLS is
  re-signed by it). On the laptop, `PIP_CERT` points pip (and pre-commit's internal pips) at it;
  in the babykev container, `SSL_CERT_FILE`, `REQUESTS_CA_BUNDLE` and `UV_SYSTEM_CERTS=1` do the
  same for uv, hf-hub and pytest's requests. Invisible in the outputs.
- **Capture-only base image (laptop).** The cheese `Dockerfile`'s `FROM python:3.11-slim-bookworm`
  needs the CA during `apt-get` and `pip install`. Instead of editing the tutorial's Dockerfile,
  the real base (`sha256:34386ef0…`) was rebuilt with the CA added, apt sources switched to
  https and `SSL_CERT_FILE`/`PIP_CERT`/`REQUESTS_CA_BUNDLE` set, and re-tagged under the same name
  (`laptop/capture-only/base.Dockerfile`, `base-build.txt`). Effects a student will not see:
  `docker image ls` (`clean-03`) lists a `python:3.11-slim-bookworm` row; a fresh student build
  shows the base layers being pulled where `part1-01`'s build shows none; `docker history` of the
  cheese image would show three extra ~0.7 MB rows. Scenes crop those.
- **The laptop's Python is a virtualenv.** `docker:dind` is Alpine, whose system Python is PEP
  668-protected (`pip install` would refuse with `externally-managed-environment`, the same
  refusal Homebrew users see — digest G10). A virtualenv owned by `student` sits first on `PATH`,
  standing in for a laptop Python that allows `pip install`, as the README assumes. `pip`,
  `black`, `flake8`, `pre-commit` in the captures are this venv's (Python 3.14.8).
- **A throwaway git identity** (`student@laptop` / `student`) is configured before the commit
  steps in both containers, silently; git refuses to create commits without one.
- **Cache prewarm (babykev).** Before the captured pass, a throwaway clone at step-05 ran
  `uv sync --locked` and downloaded `Qwen/Qwen2.5-0.5B` (~950 MB) into uv's and Hugging Face's
  caches (`babykev/capture-only/prewarm.txt`). The captured steps therefore print cache-hit
  timings (`just setup` at step-05 "Installed 38 packages in 216ms"; the smoke loads in ~4 s with
  no download bar). A student's first step-05 `just setup` downloads a few hundred MB and the
  first smoke fetches ~1 GB, as the walk says; the *text* of the outputs is otherwise the same.
- **`git restore .` before each `git switch`** stands in for timewalk's `--discard-edits`: the
  walk's live edits are dropped when moving to the next step. Each step's own break/restore pairs
  are captured as steps.
- **`sed -i` for the walk's `sed -i ''`** (Linux form, per `babykev-walk/README.md:66`).
- **Readiness wait** `part3-opt2-03` (extra) between `docker run -d` and the system tests, so the
  captured README run shows the 5-passed outcome rather than a race; the no-server skip is
  captured separately (`part3-opt2-07`).
- **Retry machinery, unused this run:** `hub_retry` (Docker Hub 429s) and `flaky_retry`
  (hypothesis `DeadlineExceeded` on torch's first call, which the walk itself hit once in
  rehearsal) re-run a step and log the failed attempts under `capture-only/`. No retries were
  needed: the only `capture-only` files are the base image pair and the prewarm log.

## Differences from the tutorials' own records, found while running

- **babykev `test_a_question_cannot_see_its_sibling` fails on this machine** (step-05a onward:
  `s05a-03`, `s05a-16`, `s05b-03`, `s05b-17` each show `1 failed, 102 passed`). The test demands
  bit-exact equality (`torch.equal`) of question 3's logits before and after question 2 is
  rewritten. The logits print identically to 4 decimals; they differ in the last bits because
  rewriting question 2 changes the packed sequence length, and torch 2.14.1+cpu's x86 kernels sum
  in a length-dependent order. On the author's Mac the comparison is bit-exact (walk: "103
  passed"). Not fixable by `OMP_NUM_THREADS=1`, `ATEN_CPU_CAPABILITY=default` or disabling
  mkldnn (tried). Everything the failing assertion is *about* is still shown by the captures:
  `before[0] == after[0]` passes, and with the wrong masks the test fails for the real reason
  (`s05a-11`). Scenes that claim "103 passed / check green at 05a" must tag it `recorded`
  (walk.md) or use the green checks captured at steps 03, 04b and 05.
- **pytest 9.1.1 prints "N passed, 1 warning"** for the cheese integration runs
  (`part3-opt1-03/04`, `opt3`) although `--disable-warnings` is in `addopts`; the digest's
  expected counts said "10 passed" / "21 passed". Same tests, same results; the summary line
  carries the warning count.
- **pre-commit 4.7.0 warns** that the pinned `pre-commit-hooks v4.5.0` uses deprecated stage
  names (`part4-03`), and black (24.1.1, the hook's pin) still runs fine. Version drift a student
  will also see.
- **uv 0.13.2 warns** `build_system.requires = ["uv-build>=0.12.13,<0.13.0"] does not contain the
  current uv version` on every babykev build; and validate-pyproject prints a one-line
  `packaging>=24.2` note inside `just lint-config` at steps 05/05b. Both real, both harmless.
- **The cheese image builds although `pyproject.toml` names a README the build context lacks**
  (digest Q3 answered: pip 25.x + current setuptools still tolerate it; `part1-01` built clean).
- **The blocked-commit demo (`part4-11`)**: black *also* fails ("files were modified") because it
  re-places the inserted `import os`; flake8 then reports the F401. Both gates fire.

## Versions at the time of recording (2026-10-19)

| what | version |
| --- | --- |
| laptop Docker (stand-in for Docker Desktop) | client + engine 29.8.2, buildx, containerd image store, linux/amd64 |
| laptop git / Python | git 2.54.0; Python 3.14.8 (virtualenv) |
| in-image (cheese) | base `python:3.11-slim-bookworm` → Python 3.11.17; pytest 9.1.1, pluggy 1.7.0, pytest-asyncio 1.4.0, anyio 4.15.1, cov 7.1.0 |
| laptop pip installs | black 26.10.1, flake8 7.4.1, pre-commit 4.7.0 |
| hook pins (from `.pre-commit-config.yaml`) | pre-commit-hooks v4.5.0, black 24.1.1, flake8 7.0.0 |
| babykev container | Debian 12, git 2.39.5; uv 0.13.2; just 1.59.0 (rust-just) |
| babykev `.venv` | Python 3.13.16 (uv-managed); pytest 9.1.1; ruff 0.16.10; pre-commit 4.6.2; torch 2.14.1+cpu; transformers 5.18.0; peft 0.21.2; hypothesis 6.168.4; ty 0.0.84; hadolint-bin 2.15.1; yamllint 1.38.0; validate-pyproject 0.26; fastcore 2.2.32 |
| the real model | `Qwen/Qwen2.5-0.5B` (~950 MB), on `cpu` |

Things that vary between runs and must be said with "at the time of recording" or cropped:
container ids and image digests, build/test timings, the prune's cache-object ids and reclaimed
size, pip's "new release" notices, the smoke's ms-per-request (the *scores* — 6 of 15 at step-05,
4 of 15 at step-05a — are seeded and reproduced the walk's Mac numbers exactly), and the pip/uv
package versions above.

## Re-running the captures

```
export HTTPS_PROXY=http://127.0.0.1:<port>  CA_BUNDLE=<proxy CA bundle>   # sandbox only
bash assets/terminal/capture.sh laptop setup
bash assets/terminal/capture.sh laptop a-pre a-part1 a-part2 a-part3 a-part4 a-clean
bash assets/terminal/capture.sh laptop teardown
bash assets/terminal/capture.sh babykev setup
bash assets/terminal/capture.sh babykev b-setup b-prewarm b-s00 b-s01 b-s02 b-s03 b-s04 b-s04b b-s05 b-s05a b-s05b
bash assets/terminal/capture.sh babykev teardown
docker rm -f l09-relay
```

Needs Docker with privileged containers. Containers persist between segment calls so a long
capture can run in parts; a re-run of a segment overwrites only that segment's files. Without
`HTTPS_PROXY`/`CA_BUNDLE` the capture-only parts (relay, CA, base image, retries) are skipped.

## Gate

Every command of the covered cheese-app-ci-cd README sections (clone, Parts 1-4, Docker Cleanup)
has a capture above, exactly as written, in README order; the only README lines without one are
the browser checks (curl evidence captured, `illustration` for the browser), Parts 5-7 (out of
scope for L09) and `docker stop <container_id>` with nothing running (`clean-01` shows why).
Every walk.md command of steps 00-05b is captured or listed above under "What cannot run here"
with its recorded source (Quarto/site renders, the Docker sections of step-05b, the timewalk
page). No output was invented; the three capture-only logs are under `capture-only/`.

## Numbers shown in pictures (not terminal panels)

- **S05 findings funnel, "8 findings → 2 findings" on `8eb63fc` service.py.** Re-measured
  2026-10-23 with the hook's pinned versions (flake8 7.0.0, black 24.1.1), `flake8 --isolated
  --max-line-length=120` on an unchanged copy of `assets/source/cheese-app-ci-cd-history/8eb63fc-service.py`:
  8 findings (F401, E302 ×2, E225, E231 ×2, E501 187 > 120, W391); after `black --line-length 120`
  the same file has 2 (F401 `os` unused; E501 147 > 120). Matches digest.md:190. Not a terminal
  panel, so no capture file; the measurement is recorded here.
