# AC215 · Lecture 21 — CI/CD with GitHub Actions II: one push, six fresh machines

A follow-along walkthrough of the Lecture 21 tutorial of Harvard's **AC215 (MLOps & LLMOps, Fall
2026)**, *Automating Software Development: CI/CD with GitHub Actions II*:
[dlops-io/cheese-app-ci-cd](https://github.com/dlops-io/cheese-app-ci-cd), branch `main` (its only
branch) @ [`b8458ff`](https://github.com/dlops-io/cheese-app-ci-cd/tree/b8458ff0cc1898700b32a873b4665f43f50df71e)
("demo class 1", 2025-11-13; still the head of `main` on the recording day), README sections
**Part 5: GitHub Actions (Remote CI)** step by step and the optional **Part 6: Branch Protection**.
Parts 1–4 of the same README (the FastAPI toy, Black and Flake8, the three test levels inside the image,
pre-commit) are Lecture 9's: [`../ac215-l09-ci-testing/`](../ac215-l09-ci-testing/). This video refers
back to them and doesn't redo them.

You push the course's own code, untouched, to a repository of your own. One log says unit, integration
and system tests all succeeded, `✅ All tests passed!`; the same run ends red, `Lint and Format Check`
failed. Which machine said no, and why didn't the summary hear it? The video follows the lecture slide
by slide, from local Git hooks and the server-side hooks GitHub.com replaces with Actions and branch
protection, to the CI loop and the course's five-stage pipeline, then reads `.github/workflows/ci.yml`
as event → workflow → jobs → steps, pushes it, and opens every job's log: the image built once and
carried as an artifact to six fresh machines, exit codes as gates, three test altitudes, a summary that
listens only to the tests, the fix that turns the run green, `--no-verify` caught by CI, Slack and
secrets, and branch protection.

Watch it with a **fresh clone** of the repository open (not your Lecture 9 folder, which has the Black fix
committed), Docker running, a GitHub account and a repository of your own (a fork or a new empty repo),
and pause at every `▶ your turn` to run the command. **No cloud, no keys:** Actions minutes are free on
public repositories; a GOLD tag marks where minutes, artifact storage and protected branches count on a
private one. The tracker top left shows the README step; a gray `extra` tag marks a command that isn't in
the README, and a gray "Lecture 21 · slides …" tag top right points to the lecture slides the scene stands
on.

**What is real and what is drawn.** The recording machine cannot push to GitHub, so no hosted run was
recorded. Instead every job of `ci.yml` ran **live** on 2026-11-06, each on its own fresh stand-in runner
with an empty Docker engine (the way GitHub gives every job a fresh `ubuntu-latest` machine), executing the
workflow's own `run:` scripts, and [act](https://github.com/nektos/act) 0.2.97 ran the whole file a second
way with the same verdict. A bare repository on the same machine stands in for "your repository". The
laptop was a fresh Docker 29.8.2 engine (git 2.54.0, pre-commit 4.7.0). The GitHub pages (the Actions tab,
the run graph, step lists, Settings → Secrets, Settings → Branches, a pull request) and the Slack message
are drawings built from the workflow file and the README, tagged `illustration`; every log line in them is
real. The webhook URL is only ever a placeholder. Details in [`ASSETS.md`](ASSETS.md). Series format:
[`docs/AC215_SERIES.md`](../../docs/AC215_SERIES.md). Study guide with every command:
[MLOps_Learning · guides/L21-cicd-github-actions.md](https://github.com/JunyiZhou-Conny/MLOps_Learning/blob/main/guides/L21-cicd-github-actions.md).

English narration; Chinese and bilingual subtitles (中文字幕说明见 [`i18n/zh/README.md`](i18n/zh/README.md)).

| file | what it is |
| --- | --- |
| `output/ac215-l21-cicd-github-actions.zh-en.mp4` | **the copy to watch**: 1080p60, English narration, bilingual subtitles (Chinese above, English below) burned in, DURATION_FULL. Published as a GitHub release asset: no MP4 is kept in Git ([`docs/PUBLISHING.md`](../../docs/PUBLISHING.md)) |
| `output/ac215-l21-cicd-github-actions.mp4` | the same video without burned-in subtitles; load any `.srt` below in your player. Release asset, not in Git: rebuild it with `--no-render` (see Rebuild) |
| `output/ac215-l21-cicd-github-actions_part1.mp4` | part 1, DURATION_P1: from local hooks to a pipeline on GitHub — read it, push it, watch it (S01–S07). Release asset, not in Git |
| `output/ac215-l21-cicd-github-actions_part2.mp4` | part 2, DURATION_P2: the run job by job — artifacts, exit codes, tests, `--no-verify`, Slack and branch protection (S08–S16). Release asset, not in Git |
| `output/ac215-l21-cicd-github-actions.srt` | English subtitles (each part has its own `.srt`, `.zh.srt`, `.zh-en.srt` / `.ass`) |
| `output/ac215-l21-cicd-github-actions.zh.srt` | Chinese subtitles (on the English timing) |
| `output/ac215-l21-cicd-github-actions.zh-en.srt` / `.zh-en.ass` | bilingual subtitles |
| `output/chapters.txt`, `chapters_part1.txt`, `chapters_part2.txt` | chapter timestamps |
| `output/transcript.md` | the full narration by chapter |
| `exercises.md` | do these after watching: the five test-yourself questions and the five ponders, hands-on predict-then-run tasks, debugging and think questions, with answers; what was re-run to check them is in [`assets/exercise-checks/`](assets/exercise-checks/README.md) |
| `digest.md` | the tutorial digest: every step, a code tour with `path:line`, gotchas, errata |
| `SLIDES.md` | the lecture behind the tutorial: a digest of the slides in our own words, with slide numbers, and which scene stands on which slides |
| `assets/terminal/` | the **real** terminal sessions and job logs every panel prints from (2026-11-06: `laptop/` your machine, `runner/` each job of `ci.yml` on a fresh stand-in runner, `expected/` what the README documents for the GitHub pages); provenance in [`ASSETS.md`](ASSETS.md) |
| `assets/source/` | the tutorial files the code panels quote, unchanged at `b8458ff`, and older versions from the repository's history (`cheese-app-ci-cd-history/`) |
| `BRIEF.md`, `script.md`, `scenes/` | the design, the narration (SAY) + visual plan (SHOW), and the Manim source |
| `i18n/zh/` | the Chinese subtitle text: glossary and sentence-aligned translation |

Git keeps the subtitles, the chapter files and the transcript; the MP4s (the burned-in copy, the clean video and
the two part cuts) are release assets.

## Chapters

CHAPTERS

## What you'll learn

Five *pause and ponder* moments ask you to predict before the video shows you: how many runs three pushes to a
feature branch and then a pull request into `main` start; whether your push is on `main` after the run turns red;
which step fails, and how, when a check job forgets `docker load`; which jobs the class's planted bug turns red and
what Test Summary says then; and which job catches a private key committed with `--no-verify`. Five test-yourself
questions close the video (answers in `exercises.md`).

**Part 1 · from local hooks to a pipeline on GitHub — read it, push it, watch it**

1. **Red run, green summary** — one log says every test passed, the same file run end to end says
   `Error: Job 'Lint and Format Check' failed`: five machines green, one red, the run red; the checks of
   Lecture 9 move to GitHub; the lecture's four sections (remote Git hooks, GitHub webhooks, continuous
   integration, continuous deployment); what you need; how the tracker, code panels, `▶ your turn` and the
   `illustration` tag work.
2. **Hooks stay on your laptop** — the lecture's recap of local hooks, pre-commit and pre-push; this repo's chain
   (seven hygiene checks, Black, Flake8, at 120 columns, only under `src`) and no tests in it; a laptop without
   `pre-commit install` sends its commit through; remote hooks: pre-receive and update can refuse a push,
   post-receive runs after it and can only report; GitHub.com runs no pre-receive scripts of yours, it gives
   Actions (after the push) and branch protection (which can say no); webhooks for a chat; the lecture's
   motivation: the checks move to the server, which is continuous integration.
3. **The CI loop and the workflow file** — the lecture's definition of CI and what it buys; slide 21's loop
   (developers → codebase → build → test → notifications); the course's five-stage pipeline; README Part 5's
   "same as production" (this repo has no production yet); `ls -la .github/workflows/` (extra): one file at the
   repository root, where GitHub looks, and a subfolder never runs; `name`, `on`, `jobs`, `runs-on:
   ubuntu-latest`; steps are `run:` scripts or `uses:` actions such as `actions/checkout`: event, workflow, jobs,
   steps.
4. **When does the pipeline wake up?** — pushes to `main` or `develop` and pull requests into them (the file's
   comment says `main` only); a feature branch waits for its pull request; the pull request run tests a temporary
   merge into `main`; what frequent integration costs and how this file keeps it down (branch filter, one shared
   build, an image kept one day); the run starts after GitHub accepted the push: the bell, not the gate.
5. **Six jobs, one graph** — the README's six jobs, their IDs and the names GitHub shows (you need the names in
   Part 6); from the lecture's row of five stages to a graph: `needs: build` fans out to four jobs side by side,
   Test Summary needs only the three test jobs (lint isn't on the list); `act -l` (extra) lists the stages 0, 1,
   2; the README's key concepts placed on the graph; about 2 minutes on the clock, about 6 billed minutes on a
   private repository.
6. **Push to a repo of your own** — a fresh clone, not your Lecture 9 folder; `git ls-remote` and `git log`
   (extras): the pin and the two "demo class 1" commits; `git add .` and `git commit -m "Add CI pipeline"`:
   `nothing to commit, working tree clean`; `git remote -v` (extra): `origin` is the course's repository, which
   refuses your push; fork it (and enable workflows) or create a new empty repository, then `git remote set-url
   origin`; a stand-in repository on the recording machine; `git push` starts run 1; on a fork, `Everything
   up-to-date` and no run, so your first run comes with the fix in part 2.
7. **Watch the run: six colors** — the Actions tab, the yellow dot, the green check and the red X; the run graph;
   how the video shows the run (fresh stand-in runners, act as a second witness, GitHub pages as illustrations);
   the push is on `main` even though the run turns red; run 1: build green, lint red, the three tests and the
   summary green, the run red; act agrees; the README's all-green screenshot shows an earlier version of the code.

**Part 2 · the run job by job — artifacts, exit codes, tests, `--no-verify`, Slack and branch protection**

8. **Build once; every job starts empty** — the lecture's single CI server vs a new machine per job; the build job
   builds the image once, tagged with the commit ID, saves it as a tar (about 176 MB) and uploads it as an
   artifact kept one day; the README's "Buildx caching" is a small slip (the default builder, no cache); a fresh
   check job's `docker images` is empty; download and `docker load -i` in every check job; an expired artifact
   breaks a re-run tomorrow; without the load: `pull access denied`, exit 125.
9. **Gates speak in exit codes** — Black for coding standards, Flake8 for static analysis; both on `api/` at 120
   columns; `continue-on-error: false` blocks, `true` is advisory; exit code 0 opens a gate, anything else shuts it
   and the red climbs from step to job to run; run 1's Black: `would reformat … utils.py`, exit 1; Flake8 skipped;
   the mess from Lecture 9, kept on purpose; what Flake8 would have said.
10. **Three test jobs, three altitudes** — unit tests (11 passed); the coverage step's `PermissionError` (exit 3),
    shunted aside by `continue-on-error`, and an upload that finds no files: the README's promised reports, and
    why (a root-owned folder, a container user `app`); integration tests with the FastAPI test client, in one
    process (10 passed); system tests: a server container on port 9000, `sleep 10`, the `curl -f` gate, a test
    container with `--network host` (5 passed), the server log and clean-up under `if: always()`; in CI a missing
    server fails loudly instead of skipping.
11. **The summary listens only to tests** — `needs` names the three test jobs and `if: always()` makes it run (not
    pass); its script prints each result, writes `$GITHUB_OUTPUT` and exits 1 on any failure; the hook answered:
    lint isn't in `needs`, and any failed job turns the run red; add lint to `needs` and to the check; the class
    demo's `math.sqrt(2 * z)`: integration and system red, unit green, lint red, and `❌ Some tests failed!`.
12. **Fix, push, green: one turn of the loop** — the fix from Lecture 9 (README Part 4): `pip install pre-commit`,
    `pre-commit install`, `pre-commit run --all-files` (Black reformats `utils.py`), `git diff`, run it again,
    `git add .`, a commit, `git push`; run 2: all six green, Flake8 runs too; it matches the README's screenshot.
13. **The local conundrum: `--no-verify`** — why run the checks twice; a hurried edit stopped by the Black hook;
    `git status --short` shows `MM`; `git commit --no-verify -m "quick fix"` skips every hook; run 3: lint red on
    `service.py`, CI caught what `--no-verify` let through; clean up with `git restore` (and fix it if you pushed
    it); CI repeats only Black and Flake8, never the seven hygiene hooks; the hooks pin an older Black than the
    image; a private key pushed with `--no-verify` passes every job: add `pre-commit run --all-files` to CI, and
    rotate the key.
14. **Webhooks, secrets and the Slack bell** — the lecture's webhooks (GitHub calls an outside address) vs Slack's
    incoming webhook that your workflow calls (optional: your own workspace); the lecture's wished-for message vs
    what this workflow sends; the secret under Settings → Secrets and variables → Actions, named
    `SLACK_WEBHOOK_URL`, not under Webhooks; why a shell step checks the secret (not allowed in `if:`, as the
    repository's history shows); in run 1 the Slack step is skipped; in the demo run the check step is skipped too,
    so the failure message never goes out; the one-line fix, `if: always()`.
15. **Branch protection: from report to gate** — Part 6: a rule for `main` with "Require a pull request before
    merging" and "Require status checks to pass" (today's page may say classic rule or offer rulesets); pick the
    checks by their names, listed after a recent run; a paid plan on private repositories; `git checkout -b
    feature/test-protection`; `def broken(): assert False` still gives 11 passed (pytest collects only `test_*`),
    `def test_broken` gives 1 failed; commit, push, open the pull request: the merge stays locked.
16. **Non-determinism, CD next, and recap** — the lecture's machine-learning twist (non-determinism in every
    stage; version everything, automate retraining and testing as Milestone 5 asks, monitor, roll out with care);
    continuous deployment is Lecture 23; the clean-up checklist; the loop once more (event, fresh machines, the
    artifact, exit codes, the summary's `needs`); five test-yourself questions.

The README's and the slides' small slips are pointed out kindly, with the fix: "Python 3.11 (same as production)"
in a repository with no production yet (read: the same image you would deploy); `ci.yml`'s comment says `main`
only while the triggers say `main` and `develop`; Part 5's `git add .` / `git commit -m "Add CI pipeline"` find
nothing to commit in a clone or fork (the workflow is already committed), `git push` to the course's repository is
refused (point `origin` at your own), and on a fork it says `Everything up-to-date` and starts no run; the README's
all-green screenshot shows an earlier version of the code (your first run is red until you run the Lecture 9 fix);
"Uses Docker Buildx for efficient caching" (the build uses the default builder and saves no cache; `exercises.md`
B6 has a cached build); the promised terminal, XML and HTML coverage reports (a root-owned folder stops them, and
`continue-on-error` hides it; B3 has the fix); "checks the results of all test jobs" is literally true, but lint is
not a test job (B2 adds it); the Slack failure message can never be sent, and the README never mentions the Slack
step or its secret (C1); Part 6 lists job IDs where the picker shows job names, and `def broken()` is never
collected (use `def test_broken()`); and where the slides differ from the repository: the lecture's straight row
of stages is a graph on GitHub, the lecture's single CI server is a fresh machine per job, and "CI repeats the
checks" means only Black and Flake8 here.

## Rebuild

```bash
python -m explainer.build videos/ac215-l21-cicd-github-actions -q l                          # fast draft
python -m explainer.build videos/ac215-l21-cicd-github-actions --render-only --jobs 3        # 1080p60 scene renders
python -m explainer.build videos/ac215-l21-cicd-github-actions --no-render --crf 27 --burn   # stitch: video, parts, subtitles, burned-in copy, chapters, transcript
python -m explainer.build videos/ac215-l21-cicd-github-actions --subs-only                   # rewrite subtitles only
python -m explainer.i18n check videos/ac215-l21-cicd-github-actions --lang zh                # Chinese text aligned with the English
```

No MP4 is in Git (the burned-in copy is a release asset): after a fresh clone, render the scenes once, then the
`--no-render` line rebuilds the clean video, the two part cuts and the burned-in copy from the scene renders. The
captures can be re-run with `assets/terminal/capture.sh` (see [`ASSETS.md`](ASSETS.md)); the exercise checks with
the scripts in [`assets/exercise-checks/logs/`](assets/exercise-checks/README.md).

Narration: Kokoro (`af_heart`, speed 0.9), generated locally.

*Course materials belong to the AC215 teaching staff (Harvard IACS); the cheese-app-ci-cd tutorial is used for study
with the instructor's permission and quoted at its pinned commit. The lecture's slides are redrawn in our own
pictures, never shown. The GitHub pages and the Slack message are schematic drawings (tagged `illustration`), never
screenshots; the recording used no GitHub credentials, no Slack workspace and no keys, and every webhook URL on
screen is a placeholder.*
