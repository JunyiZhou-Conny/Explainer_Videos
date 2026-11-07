# Assets and where they come from

Everything a scene shows as "real" (a terminal output, a source line, a file listing) is read from
a file in `assets/`, never typed by hand into a scene. This file says where each one came from.
All captures were made on **2026-11-06** (`terminal/laptop/00-env.txt`).

## `source/` — the tutorial's own files

### `source/cheese-app-ci-cd/`

From [dlops-io/cheese-app-ci-cd](https://github.com/dlops-io/cheese-app-ci-cd) at commit
`b8458ff0cc1898700b32a873b4665f43f50df71e` (main, 2025-11-13, "demo class 1"; the only branch, and
still the head of `main` on 2026-11-06: `terminal/laptop/01-ls-remote.txt`), every tracked text file
copied unchanged with `git show b8458ff:<path>`, relative paths preserved. The screenshot
`assets/pipline.png` is **not** copied (see `terminal/expected/readme-screenshot-run-graph.txt`).
Course material by the AC215 teaching staff (Harvard IACS), used for study with the instructor's
permission.

| file | what a panel quotes from it |
| --- | --- |
| `README.md` | Part 5 (277-365): the "Docker containers using Python 3.11" line (279), trigger sentence (283), the six job descriptions (287-330), Key CI/CD Concepts (332-342), Push to GitHub (344-349), Watch GitHub Actions (351-357), the screenshot reference (359-365); Part 6 (369-397) for context |
| `.github/workflows/ci.yml` | **the lecture**: name + triggers (5-11), `build` (15-38), `lint-and-format` (41-67), `unit-tests` (70-102), `integration-tests` (105-125), `system-tests` (128-169), `test-summary` + `$GITHUB_OUTPUT` (172-192), `slack-check` (194-201), Slack step and payload (203-257) |
| `Dockerfile` | base (2), apt layer (12-20), user `app` uid 1000 (23-26), code + tests baked in (38-41), `ENTRYPOINT` (52) |
| `docker-entrypoint.sh` | `PATH` (5), `exec "$@"` (10-13), DEV uvicorn `--reload` (16-19) |
| `.pre-commit-config.yaml` | the local hooks CI only partly repeats: hygiene (12-26), Black 24.1.1 @120 (29-35), Flake8 @120 (38-44) |
| `pyproject.toml`, `pytest.ini` | unpinned `black>=24.1.1` (8); `python_functions = test_*` (8), `pythonpath = .` (9) |
| `src/api-service/api/service.py`, `utils.py` | the app; `utils.py:7` and `:10-12`, the mess Black rejects |
| `tests/unit/test_utils.py`, `tests/integration/test_api.py`, `tests/system/test_system_api.py` | the three test altitudes; `TestClient(app)` (test_api.py:11); `skipif(not is_api_running())` (test_system_api.py:24) |
| `docker-shell.sh`, `.gitignore`, `src/api-service/api/__init__.py`, `tests/__init__.py` | context only |

### `source/cheese-app-ci-cd-history/`

Older versions, each from `git show <sha>:<path>` in the same repo, named `<sha>-<file>` (the L09
convention):

| file | why |
| --- | --- |
| `c3b227f-service.py` | the in-class demo commit: `service.py` cleaned up and `math.sqrt(2 * z)` injected (line 44); `b8458ff` reverts only that line. Run `run-demo` tests it. |
| `140f138-service.py`, `140f138-utils.py` | the clean code before `91eb786` re-added the mess; the README's all-green screenshot matches this state, not `b8458ff` |
| `199abd9-ci.yml`, `199abd9-to-1a5e363-ci.yml.diff` | the first Slack attempt with `secrets.SLACK_WEBHOOK_URL` in an `if:`, and the change to the shell check step that replaced it |
| `git-log-oneline.txt` | `git log --format='%h %ci %s'` (no author names) |

## `terminal/` — real terminal sessions

Re-run with `terminal/capture.sh` (header lists the order) + `terminal/run_steps.sh` (laptop
steps) + `terminal/runner_job.sh` and `terminal/ci_plan.py` (the stand-in runners). Each file starts
with the command (`$ ...`; a multi-line `run:` script continues with `> ` lines) and ends with its
exit status (`[exit N]`; when the output has no final newline, as with `curl`, it ends on the same
line, as in L09). Files whose name starts with `x` and steps marked *extra* below are not in the
README or in `ci.yml`; they are checks the video uses.

### Why there is no hosted GitHub Actions run

Part 5 of the README is "push, then watch the run on GitHub". This sandbox **cannot push to any
GitHub repository** (`laptop/capture-only/12-git-push-sandbox-proxy.txt`: the sandbox's git proxy
refuses the push with its own message, so that file is evidence only and is never shown; on a
laptop the same push to the course's repo is refused by GitHub with "permission denied"/403, and
the video says so). So every job of `ci.yml` was run **locally, live**, in two independent ways:

1. `runner/`: each job in its own fresh container with an empty Docker engine (the way GitHub gives
   every job a fresh VM), executing the workflow's own `run:` scripts verbatim;
2. `laptop/62-act-push.txt`: [nektos/act](https://github.com/nektos/act) 0.2.97 reading `ci.yml`
   and playing GitHub's runner on the laptop (not in the README).

Both agree on every job result. The Actions tab, the run graph page, the Slack message and the
branch-protection settings are drawn as **illustrations** built from `ci.yml` and the README (see
`expected/`), never presented as a real hosted run.

### `laptop/` — the student's machine (README Part 5 "Push to GitHub", the fix, `--no-verify`, act)

Environment: a fresh `docker:29.8.2-dind` container stands in for a laptop with Docker Desktop, as
in L09: Docker 29.8.2 (client and engine), git 2.54.0, Python 3.14.10 (Alpine), user `student` in
the docker group, a virtualenv first on PATH so `pip install` works, `umask 022`. A bare repository
on that laptop, `~/github-standin/student/cheese-app-ci-cd.git`, **stands in for "your repository"
on GitHub** (on a real machine: your fork or new repo, `https://github.com/<you>/cheese-app-ci-cd`).

| file | README step / what it shows |
| --- | --- |
| `00-env.txt` | extra: date, OS, versions |
| `01-ls-remote.txt` | extra: the pin is still `refs/heads/main` (plus PR refs 1-3, not branches) |
| `02-clone.txt`, `03-git-log.txt`, `05-branches.txt` | `git clone` (README "Clone or download", no URL given); the last three commits; `main` is the only branch |
| `04-ls-workflows.txt` | extra: `.github/workflows/ci.yml` at the repo root, where GitHub looks |
| `10-git-add.txt`, `11-git-commit.txt` | **Part 5, Push to GitHub, step 1-2, verbatim** (README.md:346-347) in a plain clone: `nothing to commit, working tree clean`, exit 1. The workflow is already committed; the README never says so (errata) |
| `13-git-remote.txt`, `14-git-status.txt` | extra: `origin` is the course's repo, so `git push` (README.md:348) goes nowhere you can write; the push itself is described, not shown (see above) |
| `20-standin-create.txt`, `21-set-url.txt` | extra: create "your repository" and point `origin` at it (stand-in for `git remote set-url origin <your fork URL>`) |
| `22-git-push.txt` | **Part 5 step 3, `git push`**, to "your" repo: `* [new branch] main -> main`. This push is what starts **run 1** |
| `23-standin-log.txt` | extra: the commit CI checks out in run 1 (`b8458ff…`) |
| `30-pip-install-pre-commit.txt`, `31-pre-commit-install.txt` | README Part 4 (covered by L09), needed for the fix: pre-commit 4.7.0 |
| `32-run-all-files.txt`, `33-git-diff.txt`, `34-run-all-files-again.txt` | the fix for run 1's red Lint job (digest Step 14 Option A): Black hook rewrites `utils.py` (exit 1), the diff (`power(base, exponent)`, one blank line removed), then all hooks pass |
| `35-git-add.txt`, `36-git-commit.txt`, `37-git-push.txt`, `38-standin-log.txt` | `git add .`, commit (hooks pass; message "Format utils.py with Black" is ours, the README has none), `git push` → **run 2** (`2289d89…`) |
| `40-quick-edit.txt` … `47-standin-log.txt` | extra, **lecture slides 29-31**: a hurried edit `z=power(x,2)+power(y,2)`; `git commit -m "quick fix"` is stopped by the Black hook (Flake8 passes because it reads Black's rewritten copy); `git status --short` = `MM`; `git commit --no-verify -m "quick fix"` (the slide's command) goes through; `git push` → **run 3** (`2892b1b…`) |
| `48-git-status.txt`, `49-restore.txt` | the hook's reformatted copy was never committed; restored |
| `50-build.txt` … `58-restore.txt` | context for README Part 6 (369-397), run in the image locally: README's `echo "def broken(): assert False"` → still `11 passed` (pytest never collects `broken`); extra `def test_broken` → `1 failed, 11 passed`, exit 1. `50-build.txt` is a full build of the unmodified Dockerfile from the official `python:3.11-slim-bookworm` (digest `sha256:a83ba18a…`) |
| `60-act-version.txt`, `61-act-list.txt` | extra: act 0.2.97; `act -l` prints the job graph as stages 0 (build) → 1 (four jobs) → 2 (test-summary), read from `ci.yml` |
| `62-act-push.txt` | extra: `act push -P ubuntu-latest=-self-hosted --artifact-server-path /tmp/act-artifacts` at `b8458ff` (751 lines; contains ANSI colour codes in the Docker build progress, scenes strip them). Same verdict as run 1: Lint and Format Check `Job failed` at "Run Black formatter check", the other five `Job succeeded`, `✅ All tests passed!`, `::set-output:: enabled=false`, final `Error: Job 'Lint and Format Check' failed`, exit 1. Also shows the artifact upload ("Final size is 174794992 bytes"), the coverage `PermissionError` and `::warning::No files were found with the provided path: coverage/` |
| `63-images-after.txt` | extra: act's jobs shared one Docker engine (the image is just there; see caveats) |
| `capture-only/12-git-push-sandbox-proxy.txt` | evidence only, never shown: the sandbox's refusal of `git push` to the course repo |

Caveats for the act capture: `-P ubuntu-latest=-self-hosted` runs every job directly on the laptop,
sharing one Docker engine, so it does **not** show the "fresh machine per job" point (use `runner/`
for that); act prints only steps that run, so the skipped Flake8 and Slack steps do not appear; the
build reused layers cached by `50-build.txt`. setup-buildx-action created a `docker-container`
builder, yet the `docker build` step still ran on `docker:default` (line "Building … docker:default"):
evidence for the README's "Uses Docker Buildx for efficient caching" erratum.

### `runner/` — every job of `ci.yml`, each on a fresh stand-in runner

Environment: per job, a fresh container from `l21-runner:capture` (= `docker:29.8.2-dind` + bash,
curl, git; capture-only) with its **own empty Docker engine**, as root, `umask 022`; workspace
`/home/runner/work/cheese-app-ci-cd/cheese-app-ci-cd` (GitHub's path for `github.workspace`).
`ci_plan.py` extracts the job's steps from `source/cheese-app-ci-cd/.github/workflows/ci.yml` and
substitutes `${{ github.sha }}`, `${{ github.workspace }}`, `${{ needs.<job>.result }}` and
`${{ secrets.SLACK_WEBHOOK_URL }}` (not set → empty string, as GitHub does); `runner_job.sh` runs
each `run:` script with `bash --noprofile --norc -eo pipefail` and applies GitHub's rules (skip after
a failure unless `if: always()`, `continue-on-error`, `needs`). `test-summary` runs in a plain
`python:3.12-slim-bookworm` container (it only needs bash). Differences from a hosted
`ubuntu-latest` VM: Alpine, not Ubuntu; the shell user is root (on GitHub `runner`, while Docker
runs as root in both); the `uses:` steps cannot run without GitHub and each is replaced by a
**stand-in** recorded under a `-standin` name:

| `uses:` | stand-in file and command |
| --- | --- |
| `actions/checkout@v4` | `NN-checkout-standin.txt`: `tar -xf /checkout.tar` of `git archive <sha>` from the stand-in remote |
| `docker/setup-buildx-action@v3` | `02-buildx-standin.txt`: `docker buildx version` (v0.37.2) |
| `actions/upload-artifact@v4` (`docker-image`) | `05-upload-artifact-standin.txt`: `ls -l /tmp/cheese-app-api.tar` (176459776 bytes); the host copies the tar into the next jobs |
| `actions/download-artifact@v4` | `02-download-artifact-standin.txt`: `cp /artifact/cheese-app-api.tar /tmp/` |
| `actions/upload-artifact@v4` (`coverage-report-unit`) | `06-upload-artifact-standin.txt`: `find coverage/ -type f \| wc -l` → `0` (what the upload would find) |
| `slackapi/slack-github-action@v1.26.0` | never run (no webhook; its `if:` is false in every run: `00-steps.txt`) |

Per job folder: `00-steps.txt` (each step's outcome, as the run page lists them), `result.txt`, one
file per `run:` step named after the step (`04-run-black-formatter-check.txt` …), and extras:
`x1-images-before-load.txt` (empty engine: jobs share nothing), `x2-images-after-load.txt`,
`x1-images-after-build.txt`, `x3-docker-ps.txt` (system tests), `x3-coverage-dir.txt` (`coverage/`
created `root:root 755`, container user `uid=1000(app)`), `x4-flake8-if-run.txt` (what the skipped
Flake8 step would print), `x5-black-diff.txt`. `results.txt` per run lists all six job results. The
172.17/172.18.x.x addresses in server logs are Docker's private bridge gateways.

| run | commit (how it got there) | results |
| --- | --- | --- |
| `run1/` | `b8458ff0…` (the pin, `laptop/22-git-push.txt`) | build ✓, **lint-and-format ✗** (Black: `would reformat /app/api/utils.py`, `Oh no! 💥 💔 💥`, exit 1; Flake8 **skipped**), unit ✓ 11 passed (coverage step ✗ `PermissionError`, exit 3, `continue-on-error` keeps the job green), integration ✓ 10 passed, system ✓ 5 passed, test-summary ✓ `✅ All tests passed!`, Slack skipped (`enabled=false`). Overall red; summary green (lint is not in `needs`) |
| `run2/` | `2289d89d…` (`laptop/36-37`) | all six ✓; Black `3 files would be left unchanged`, Flake8 runs, exit 0. Matches the README screenshot |
| `run3/` | `2892b1bf…` (`--no-verify`, `laptop/44-45`) | lint ✗ (Black: `would reformat /app/api/service.py`; x4: E225, E231 ×2 on `service.py:43`), all tests ✓, summary ✓. What `--no-verify` let through, CI caught |
| `run-demo/` | `c3b227f4…` (the class demo, `git archive` from the course repo clone; never on the stand-in remote) | lint ✗, unit ✓, **integration ✗** (`1 failed, 9 passed`), **system ✗** (`2 failed, 3 passed`: 3.162… ≠ 2.236, 7.071… ≠ 5.0), **test-summary ✗** (`❌ Some tests failed!`, exit 1) and then **"Check if Slack webhook is configured" skipped**: the failure message could never be sent (digest G8) |
| `noload/` | `b8458ff…` | extra (ponder): a fresh runner that skipped `docker load`: `docker images` empty, then `Unable to find image … locally` / `pull access denied for cheese-app-api, repository does not exist or may require 'docker login'`, exit 125 |

Versions inside the image (unpinned, they drift; say "at the time of recording"): Python 3.11.18,
black 26.10.1, flake8 7.5.0, pytest 9.2.0, pytest-cov 7.1.0, pytest-asyncio 1.4.1.post1, fastapi
0.162.0, starlette 1.10.0, uvicorn 0.54.0, httpx 0.28.1, pip 26.3. Pre-commit on the laptop: 4.7.0
with the config's pinned Black 24.1.1 and Flake8 7.0.0 (they agreed with the image's Black here).

### `expected/` — what the tutorial documents for the steps that need GitHub

| file | source | used as |
| --- | --- | --- |
| `readme-watch-actions.txt` | README.md:351-363, copied unchanged | the "Watch GitHub Actions" steps; the Actions tab is drawn as an `illustration` |
| `readme-screenshot-run-graph.txt` | transcribed from the README's `assets/pipline.png` at `b8458ff` (job names, ✓, 54 s / 18 s / 20 s / 39 s / 22 s / 4 s, edges) | `recorded` run graph, re-drawn (the image is not copied). It is all green because it shows an earlier code state (`140f138`-like); a push of `b8458ff` gives run 1 |
| `job-graph-from-ci-yml.txt` | generated from `ci.yml` with PyYAML (`ci_plan.py`'s parser): job ids, names, `needs`, `if`, step counts | `illustration` source for the DAG and the run graph |

Not captured and how the video shows them: the hosted run page and logs (illustration from `ci.yml`
+ the README screenshot, with the live local equivalents above); the Slack message (illustration
built from the payload template `ci.yml:207-254`, webhook URL only as a placeholder such as
`https://hooks.slack.com/services/<your-webhook-path>`; never a real-looking URL); repository
Settings → Secrets and Settings → Branches (schematic `illustration`s with the README's/workflow's
field values); a push refused by branch protection (described only). Billing minutes are from the
digest (§2), not measured.

### Capture-only helpers (not part of the tutorial)

- `proxy_relay.py` (container `l21-relay`) and `ptyrun.py`: copied unchanged from L09
  (`videos/ac215-l09-ci-testing/assets/terminal/`). The relay makes the sandbox's loopback HTTPS
  proxy reachable from Docker's bridge; the CA bundle is added to the laptop and runner containers.
- Docker Hub pulls by the laptop and the build runner go through `--registry-mirror=https://mirror.gcr.io`
  (the sandbox's shared IPs hit Docker Hub's anonymous rate limit); the check-job runners have no
  mirror, so `noload/` shows Docker Hub's own answer. Runs 1-3 and run-demo were recorded with the
  mirror on every runner (before that change); their check jobs never pull, so nothing differs.
- The CA-patched base image of L09 (`CAPTURE_BASE=1`) was **not** needed: every build here used the
  unmodified official base.
- act was built from source (`CGO_ENABLED=0 go install github.com/nektos/act@v0.2.97` in a
  `golang:1.25-bookworm` container, through the Go module proxy, because GitHub release downloads
  are blocked in the sandbox) and copied in with Node.js 24.22.1 (`apk add nodejs`) for the
  JavaScript actions: `capture.sh laptop act-setup` with `ACT_BIN=<path>`.
- A git identity `student <student@laptop>` exists so commits can be made; it is never shown as a step.
- All capture containers, images and the image tars were removed after capturing.
