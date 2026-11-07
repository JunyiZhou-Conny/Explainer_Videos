# Exercise checks · ac215-l21-cicd-github-actions (2026-11-07, 04:52–05:06 UTC; 2026-11-06 evening, US Eastern)

What was run to verify [`exercises.md`](../../exercises.md), beyond the captures in `assets/terminal/`, which
the answers cite directly (`laptop/` the student's machine, `runner/run1`, `run2`, `run3`, `run-demo`, `noload`
the jobs of `ci.yml` on fresh stand-in runners; provenance in [`ASSETS.md`](../../ASSETS.md)). The check scripts and
their logs are in [`logs/`](logs/). Every step in a log starts with its command (`$ …`) and ends with `[exit N]`, as
in `assets/terminal/run_steps.sh`; where a step pipes into `grep`, `tail` or `sed`, `[exit N]` is the last command's
status, and the step prints the command's own status as `exit code: N` before it. In the logs, `$SCRATCH` stands for
the session's scratch folder, `$W` for the work copy, `$IMG` for the check image's tag and `$HTTPS_PROXY` for the
session proxy.

**No GitHub, no Slack, no credentials.** This machine cannot push to GitHub, so nothing here is a hosted Actions run:
the workflow checks read the file with [actionlint](https://github.com/rhysd/actionlint) (the linter that applies
GitHub's workflow syntax and context rules) and play individual `run:` scripts in bash with the values GitHub would
substitute. The webhook URL is only ever the placeholder `https://hooks.slack.com/services/<your-webhook-path>`, and
nothing called it. The "private key" in `git.log` is three lines of placeholder text with a PEM header, not a key.

## Setup (disposable; nothing from the repository ran on the host)

- The repository: `dlops-io/cheese-app-ci-cd` at `b8458ff0cc1898700b32a873b4665f43f50df71e`, still the head of
  `main` (`git ls-remote`, [`setup.log`](logs/setup.log)). The work copy `$W` is a `git archive b8458ff` of the
  read-only clone.
- Docker Engine 29.8.2 on the session machine (its daemon was started for these checks).
- [`setup.sh`](logs/setup.sh) builds the **tutorial's image from its unchanged Dockerfile**, tagged
  `cheese-app-api:b8458ff-l21ex`. Only the `FROM` image is swapped, through a named build context, for
  [`py311-ca-check.Dockerfile`](logs/py311-ca-check.Dockerfile) (check-only: the official `python:3.11-slim-bookworm`,
  digest `sha256:a83ba18a…`, the same as the captures, pulled from `mirror.gcr.io`, plus the session proxy's CA and
  https apt sources), so the build can download through the sandbox's TLS-intercepting proxy. Inside: Python 3.11.18,
  black 26.10.1, flake8 7.5.0, pytest 9.2.0, pytest-cov 7.1.0, fastapi 0.162.0, uvicorn 0.54.0, the same versions as
  the captures. [`lib.sh`](logs/lib.sh) holds `step` and the same `build` for the modified copies.
- [`laptop-check.Dockerfile`](logs/laptop-check.Dockerfile) → `l21ex/laptop:check` (check-only): the same base plus
  git 2.39.5, pre-commit 4.7.0 (the captures' version), PyYAML and actionlint 1.7.12 (from PyPI's `actionlint-py`
  wheel, which bundles the binary), user `student`.
- [`ci-exercises.yml`](logs/ci-exercises.yml): `ci.yml` at `b8458ff` with the exercises' answers applied (B2, B3, B5,
  B6, C1), a check file, **not** the tutorial's; `diff` it against
  [`../source/cheese-app-ci-cd/.github/workflows/ci.yml`](../source/cheese-app-ci-cd/.github/workflows/ci.yml).
  [`runstep.py`](logs/runstep.py) prints one step's `run:` script with `needs.<job>.result` and `secrets.<NAME>`
  filled in, as GitHub substitutes them before bash runs.
- Containers and ports: every container is named `l21ex-…`; host ports **19000** and **19001** stand in for the
  runner's 9000, so nothing collided with other work on the machine.

## Checks

| exercise | what was run | result |
| --- | --- | --- |
| B1, Q4 | [`image.sh`](logs/image.sh) "B1": `ci.yml:61` and `:66` in the image; Black run from the image on a copy with only `api/` mounted; rebuild; both again ([`image.log`](logs/image.log)) | Black `would reformat /app/api/utils.py`, exit 1; Flake8 `api/utils.py:7:15: E231`, `api/utils.py:13:1: E303`, exit 1; the fix's diff (`power(base, exponent)`, one blank line removed); after the rebuild Black `3 files would be left unchanged.`, exit 0, Flake8 silent, exit 0 |
| B1 (aside) | `image.sh` "B1 (aside)": README Part 7's `-v $(pwd)/src/api-service:/app` | `/bin/bash: docker-entrypoint.sh: No such file or directory`, exit 127 |
| B3 | `image.sh` "B3": the coverage command of `ci.yml:94` in an empty folder, then with `mkdir -p coverage && chmod 777 coverage` and the reports written into the mount | as written: `INTERNALERROR> PermissionError: [Errno 13] Permission denied: 'coverage/style_cb_4667309f.css'`, exit 3, `coverage` is `drwxr-xr-x root root`, 0 files, container `uid=1000(app)`; fixed: `TOTAL 21 18 14%`, HTML and XML written, exit 0, 13 files |
| B4 | `image.sh` "B4": `--cov-fail-under=50`, unit only, then unit + integration | `FAIL Required test coverage of 50% not reached. Total coverage: 14.29%`, exit 1; `service.py 17 1 94% 35`, `utils.py 4 1 75% 14`, `Required test coverage of 50% reached. Total coverage: 90.48%`, `21 passed, 1 warning`, exit 0 |
| B5 | `image.sh` "B5": the readiness loop against the server (`-e DEV=1`) on 19000, then against a container that only sleeps, on 19001 | `{"status":"healthy"}`, `ready on try 2 after 1.076815515 s`; `gave up after 31 s` + the container's log, exit 1 |
| C6, D1 | `image.sh` "C6": a copy with `def oops(:` appended to `service.py`, built as `cheese-app-api:syntax-l21ex` | Black `error: cannot parse: /app/api/service.py:52:9`, exit 123; unit `11 passed`, exit 0; integration `SyntaxError: invalid syntax`, `Interrupted: 1 error during collection`, exit 2; server + `sleep 10` + `curl -f`: `curl: (56) Recv failure: Connection reset by peer`, server log `Started reloader process`, `SyntaxError: invalid syntax` |
| B2, B6, C1, Q3 | [`workflow.sh`](logs/workflow.sh) in `l21ex/laptop:check` ([`workflow.log`](logs/workflow.log)): actionlint on `ci.yml` and on `ci-exercises.yml` | both: no findings |
| B2, Q3 | `workflow.sh` "B2": the exercises' "Check test results" with run 1's results, with run 2's, and the original step with run 1's | `Lint and Format: failure` … `❌ Some tests failed!`, `status=failure`, the Markdown table, exit 1; `✅ All tests passed!`, exit 0; original: `✅ All tests passed!`, exit 0 (lint never seen) |
| C1 | `workflow.sh` "C1": the hardened check step with `SLACK_WEBHOOK_URL` empty, then set to the placeholder | `enabled=false`; `enabled=true` |
| C2 | `workflow.sh` "C2": actionlint on `199abd9`'s `ci.yml` | `ci.yml:195:25: context "secrets" is not allowed here. available contexts are "env", "github", "inputs", "job", "matrix", "needs", "runner", "steps", "strategy", "vars"`, exit 1 |
| C3 | [`git.sh`](logs/git.sh) in `l21ex/laptop:check` ([`git.log`](logs/git.log)) "C3": a clone at `b8458ff` whose `origin` is a bare stand-in fork that already holds `b8458ff`; README Part 5's three commands; then an empty commit | `nothing to commit, working tree clean`, exit 1; `Everything up-to-date`; `git commit --allow-empty -m "Trigger CI"` + push: `b8458ff..<new>  main -> main` |
| C4 | `git.sh` "C4": `pre-commit install`, the video's quick edit of `service.py:43`, commit, commit again, then `git add .` + commit | first commit: Black `Failed`, `reformatted src/api-service/api/service.py`, `MM`; again: `[WARNING] Unstaged files detected.`, `[WARNING] Stashed changes conflicted with hook auto-fixes... Rolling back fixes...`, exit 1, still `MM`; after `git add .`: `nothing to commit, working tree clean` (Black restored the original line) |
| Ponder 5, D1 | `git.sh` "Ponder 5 / D1": an `id_rsa` with placeholder text, committed with the hooks, then with `--no-verify`; `ci.yml`'s lint lines; `pre-commit run --all-files` | `Detect private keys…Failed`, `Private key found: id_rsa`, exit 1; `--no-verify`: `[main …] add key`; CI lints only `api/` (`ci.yml:61, 66`); `pre-commit run --all-files`: `Detect private keys…Failed`, exit 1 |

## Not run (and why)

- **Anything that needs GitHub**: a hosted run, the run page and its Summary tab (B2's table), "Re-run failed jobs"
  after the artifact expired (C7), GitHub's own refusal of `199abd9`'s workflow file (C2: actionlint's verdict is
  shown instead), the check picker and the locked merge button of branch protection (C5, D4), the GitHub Actions
  cache that B6 configures. The answers rely on the workflow file, the captures and GitHub's documented behaviour, and
  say so.
- **Slack**: no workspace, no webhook; only the shell logic of the check step ran (C1).
- **Docker Desktop for Mac**: B3's remark that the original coverage command may work there (relaxed bind-mount
  ownership) is from the digest, not checked.
- **Billing** (D3): the per-job rounding comes from the digest's reading of GitHub's billing rules, not a bill.
- **D2, D4, D5** are reasoning questions; their facts come from `ci.yml`, the captures and the checks above.

## Cleanup

After the checks: the images `cheese-app-api:b8458ff-l21ex`, `cheese-app-api:fixed-l21ex`,
`cheese-app-api:syntax-l21ex`, `l21ex/laptop:check`, `l21ex/py311-ca:check` and
`mirror.gcr.io/library/python:3.11-slim-bookworm` were removed by name; every container ran with `--rm` or was
removed by name (`l21ex-api-server`). The engine's build cache was not pruned (`docker builder prune` acts on the
whole shared engine). The work copies stay in the session's scratch folder, outside the repository.
