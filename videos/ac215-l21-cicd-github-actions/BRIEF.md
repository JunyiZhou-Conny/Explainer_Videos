# Brief · AC215 L21 — CI/CD with GitHub Actions II: one push, six fresh machines

The design of this video, written before the script. Series rules: `docs/AC215_SERIES.md`.
Facts: `digest.md` (the verified tutorial digest), `SLIDES.md` (the lecture deck and its scene map)
and `assets/` (real captures, see `ASSETS.md`). **Where the digest or the slides and the captures
disagree, the captures win.** The captures are the newest source (2026-11-06, `laptop/00-env.txt`):
every README Part 5 command run as written on a stand-in laptop (`docker:29.8.2-dind`, user
`student`), and every job of `ci.yml` run live, each on its own fresh stand-in runner with an empty
Docker engine (`runner/`), cross-checked by `act` 0.2.97 reading the same `ci.yml` (`laptop/62`).

Conny, 2026-11-02: 「我还是需要每一节Lecture非常仔细的slide by slide然后github repo上一步一步的训练」.
So this is the **full follow-along**: the L21 deck slide by slide wherever the tutorial applies it,
and README **Part 5: GitHub Actions (Remote CI)** of `dlops-io/cheese-app-ci-cd` step by step, in
order. Parts 1–4 of the same README were followed in L09 (`videos/ac215-l09-ci-testing/`): this
video refers back to them and never redoes them. Part 6 (branch protection, optional) is the
README's next section and the lecture's "remote hook" idea, so it closes the walkthrough as extras.

| topic | digest / slides | captures (use these) |
| --- | --- | --- |
| which commit | `b8458ff` (main, 2025-11-13, "demo class 1") | unchanged: `git ls-remote` on 2026-11-06 shows `refs/heads/main` = `b8458ff0…`, the only branch (`laptop/01`, `05`); `refs/pull/1-3` are PR refs, never mentioned |
| the first run's colour | digest Step 13: red (Black); README screenshot: all green | **red, confirmed live**: `runner/run1` and `act` (`62:750`, `Error: Job 'Lint and Format Check' failed`). Lint and Format Check ✗ at Black (`would reformat /app/api/utils.py`), Flake8 **skipped**, the other five ✓, and Test Summary prints **`✅ All tests passed!`** (`run1/test-summary/01:16`). The screenshot is an earlier code state (`expected/readme-screenshot-run-graph.txt`); run 2 after the Black fix matches it |
| `git commit -m "Add CI pipeline"` | digest G20 (reasoned) | `laptop/11`: `nothing to commit, working tree clean`, exit 1 |
| where the push goes | digest G21: 403 from GitHub | `laptop/13`: `origin` is the course's repo. The sandbox's own refusal (`capture-only/12`) is **never shown**; the video says in words that GitHub answers "permission denied" (403) and shows the fix: your own repo, `git remote set-url origin …` (`laptop/20`, `21` on a stand-in; `22` the push) |
| Buildx caching | digest open question | **not used**: the build runs on the default builder (`run1/build/03:2` `building with "default" instance using docker driver`; act `62:313-334` `docker:default` although setup-buildx created a `docker-container` builder, `62:251-257`). README.md:291 is an erratum |
| the artifact | digest: "large, not measured" | `run1/build/05`: `/tmp/cheese-app-api.tar` **176,112,128 bytes** (≈ 176 MB); act's upload `62:399` "Final size is 174794992 bytes". Say "about 176 megabytes", never the exact bytes |
| jobs share nothing | digest C2 (reasoned) | live: every check job's `x1-images-before-load.txt` is an **empty** `docker images`; `x2` after `docker load` shows `cheese-app-api:b8458ff…`; `noload/x2`: without the load, `Unable to find image … locally` → `pull access denied for cheese-app-api …`, exit 125 |
| coverage step | digest G7 (reproduced locally) | live on the fresh runner: `PermissionError: [Errno 13] … 'coverage/style_cb_4667309f.css'`, `11 passed`, **exit 3** (`run1/unit-tests/05`), job still ✓ (`00-steps:6`); `coverage/` is `root:root`, the container user `uid=1000(app)` (`x3`); the upload finds **0** files (`06`); act: `::warning::No files were found with the provided path: coverage/` (`62:677`) |
| demo commit `c3b227f` | digest ponder answer | `runner/run-demo`: integration **1 failed, 9 passed** (`7.0710678118654755 == 5.0`), system **2 failed, 3 passed** (`3.162… vs 2.236`, `7.071… vs 5.0`), unit ✓, lint ✗ (still `utils.py`), Test Summary ✗ `❌ Some tests failed!` |
| Slack on failure | digest G8 (reasoned) | **confirmed**: in `run-demo/test-summary/00-steps.txt` "Check if Slack webhook is configured" is *skipped* after the failing step, so the Slack step's condition is `''`; in run 1 it runs and writes `enabled=false` (no secret) |
| `--no-verify` | SLIDES 29–31, a gap in the digest | captured end to end: `laptop/40-47` (hook stops `quick fix`, `MM`, `--no-verify` goes through, push) → `run3` lint ✗ `would reformat /app/api/service.py`; what the skipped Flake8 step would say: `E225`, `E231` ×2 on `service.py:43` (`run3/lint-and-format/x4`) |
| Part 6 break-the-tests | digest G5 | `laptop/51`+`53`: `def broken()` → still **11 passed**; extra `55`+`57`: `def test_broken` → **1 failed, 11 passed**, exit 1 |
| base image | digest: CA-patched base for the verifier | the unmodified official `python:3.11-slim-bookworm` built fine (`laptop/50`); nothing to say about it |
| Black versions | digest G12 (drift risk) | pre-commit pins Black 24.1.1, the image installed black 26.10.1; **they agreed** on this code at the time of recording. One clause in S13 |
| timings | screenshot: 54 s / 22 / 18 / 20 / 39 / 4 s | the stand-in runners' timings are not GitHub's: **never quote them**. Durations come only from the README screenshot transcription, tagged `recorded` |
| slide 2 / slide 5 wording | SLIDES Conflicts 1, 2 | say it right without pointing at the slip: pre-commit runs on your laptop before the commit exists; a push-triggered Actions run reports after the push was accepted; branch protection is what refuses |

## Audience and goal

An AC215 student who has done L1–L20, in particular:
- Docker images, containers, `-p HOST:CONTAINER`, `docker save`/`load` (L2–L4);
- **L09**: this same repo's Parts 1–4: the FastAPI toy (`/`, `/health`, `/euclidean_distance/`),
  Black vs Flake8 at 120 columns, the three test levels (11 unit, 10 integration, 5 system) inside
  the image, the silent `skipif` skip, and `pre-commit install` with its seven hygiene hooks + Black
  + Flake8;
- L18's FastAPI service (context only).

They have seen Lecture 21. They watch with their clone of
[dlops-io/cheese-app-ci-cd](https://github.com/dlops-io/cheese-app-ci-cd) open, Docker running, a
**GitHub account** and a repository of their own (a fork or a new repo), pausing to run each step.
**No GCP, no keys, no cloud bill**; GitHub Actions minutes are free on public repos (GOLD tags where
minutes and storage count on private ones).

After the video they can:
- explain why local hooks are not a team guarantee (they live on one laptop, and `--no-verify`
  skips them) and where the lecture's server-side ideas live on GitHub.com (Actions reports after
  the push; branch protection with required checks refuses);
- read `ci.yml` as event → workflow → jobs → steps, and say when it runs (pushes to `main`/`develop`,
  PRs into them; a PR run tests a merge commit);
- push the repo to a repository of their own, find the run in the Actions tab, and read every job's
  log;
- explain why the image is built once and carried as an artifact (every job starts on an empty
  machine), and predict the error when a job forgets `docker load`;
- read the job graph (`needs`, fan-out, fan-in, `if: always()`) and explain why the run is red while
  Test Summary says `✅ All tests passed!`;
- tell a blocking step from an advisory one (`continue-on-error`), and why Flake8 is skipped when
  Black fails;
- turn the first red run green with `pre-commit run --all-files`, and say which checks CI repeats
  and which it does not;
- set up the Slack secret correctly (incoming webhook URL as a repository secret, never in the repo)
  and know why the failure message never arrives as written;
- protect `main` with the right check names, and break a test that pytest actually collects.

## Length and parts

~31–33 minutes. Narration 3,900–4,300 words (Kokoro af_heart, speed 0.9 ≈ 174 wpm). The plan below
totals **~4,250 words ≈ 24.5 min of narration**; typing, run logs, the run-graph drawings and five
ponder timers bring it to ~31–33 min. Word budgets per scene are targets (±15 %).

- **Part 1 = S01–S07** (~1,850 words, ~13–14 min): **read it, push it, watch it.** The hook; the
  lecture's way from local hooks to a shared repository; the CI loop and the workflow file; when it
  runs; the six jobs as one graph; the push to your own repo; the Actions tab and the six colours.
- **Part 2 = S08–S16** (~2,400 words, ~18–19 min): **the run, job by job, then around the loop.**
  Build once and carry the image; exit codes; the three test jobs; the summary; the fix and the
  green run; `--no-verify`; webhooks, secrets and Slack; branch protection; ML's non-determinism, CD
  next, teardown and recap.

The cut is the README's own seam between "Watch GitHub Actions" (the graph appears) and what the
README leaves to you (reading each log). Part 1 ends on run 1's real verdict, the hook reproduced on
the viewer's own push: **Lint and Format Check red, Test Summary green, the run red**, and the parked
question: "two of these six machines disagree. In part 2 we open every log."

**Why the push comes before the job-by-job reading.** README Part 5 describes the six jobs (287–342),
then pushes (344–349) and watches (351–365). We follow that order: S05 reads the six descriptions and
the key concepts as a graph, S06–S07 push and watch, and Part 2 opens each job with its **real** log.
That way no output appears before the run that made it. The tracker stays on "Read results" through
Part 2, and each deep dive quotes the README's bullets for that job again (README.md:289–330).

## Colours (series table, applied)

| meaning | colour |
| --- | --- |
| the laptop: your clone, your terminal, the **local** pre-commit hooks, slide 14's chain | GREY |
| GitHub: the shared repository (your fork / new repo), the Actions tab, every GitHub-hosted runner (one `ubuntu-latest` VM per job), the artifact store, the secrets vault | BLUE |
| the image `cheese-app-api:<sha>`, the tar "suitcase", the containers (`api-server`, the test container) | TEAL |
| shared, not yours: the course's repo `dlops-io/cheese-app-ci-cd` (your `origin` until you change it), Docker Hub (where a forgotten image is looked for), port 9000 on the runner | ORANGE |
| what the project owns and pins: `ci.yml`, `.pre-commit-config.yaml` (Black 24.1.1), `pyproject.toml`; a ✓ / `success` / `11 passed`; your branch `main` | GREEN |
| tools: GitHub Actions (the runner program), Docker, Buildx, Black, Flake8, pytest, pre-commit, act, the Slack action | PURPLE |
| errors and "don't": ✗ / `failure`, exit codes ≠ 0, `would reformat`, `PermissionError`, `pull access denied`, `--no-verify`'s bypass, a key in the repo | RED |
| your turn, the README tracker, the pipeline strip's current box, a run in progress (GitHub's own yellow dot), the ponder timer | YELLOW |
| money: Actions minutes on private repos (billed per job, rounded up), artifact storage, protected branches on private repos needing a paid plan | GOLD |
| events and routes: the push and PR arrows, the webhook POST, `localhost:9000` HTTP arrows, `$GITHUB_OUTPUT` notes, `needs.<job>.result` tokens | PINK |
| *skipped* (a step or job that never ran) | GREY, dashed |
| the past and the future (L09's hooks, L23's CD, Milestone 5's retraining) | GREY, dashed |

The lecture's pastel colours (slide 26's five boxes, slide 21's red codebase box) are **not** copied:
the strip's boxes are WHITE outlines whose current box fills YELLOW; Build Container is TEAL inside
(an image), the runner around it BLUE. No GitHub, GitLab, Playwright or Slack logos anywhere: GitHub
is a BLUE rounded box labelled "GitHub", Slack a GREY chat window labelled "#build-alerts".

## Running example

- **The laptop**: user `student`, terminal title `laptop`, prompt `student@laptop:~/cheese-app-ci-cd$`
  (`laptop/02` clones into `~`; every later capture runs in the clone). Say once: "your prompt shows
  your own user".
- **Your repository**: on your machine, `https://github.com/<you>/cheese-app-ci-cd` (a fork or a new
  repo). On the recording laptop a bare repo `~/github-standin/student/cheese-app-ci-cd.git` stands
  in for it (`laptop/20`, `21`): said once in S06, shown as `extra`, and the narration always says
  "your repository on GitHub".
- **The runs**, named as the captures name them and nothing more:
  - **run 1** = the push of the untouched clone, `b8458ff` (the same commit for every viewer, so the
    same image tag `cheese-app-api:b8458ff0…`);
  - **run 2** = after the Black fix (`2289d89` here; "your commit id will differ");
  - **run 3** = after `git commit --no-verify -m "quick fix"` (`2892b1b` here);
  - **the demo run** = the in-class demo commit `c3b227f` ("demo class 1", 2025-11-13), checked out
    from the course repo's history, never pushed anywhere;
  - **no-load** = one check job with its `docker load` step removed (the ponder).
- **How the runs were made, said once (S06/S07), then never apologised for**: "This recording
  machine can't push to GitHub. So we ran every job of `ci.yml` right here, live, each on a brand-new
  machine with an empty Docker, the way GitHub gives each job a fresh VM, and we ran the whole file
  a second way with `act`, a tool that plays GitHub's runner on your laptop. Both gave the same
  verdict. The GitHub pages you'll see are drawings built from the workflow file, marked
  *illustration*; every log line in them is real."
- **Run logs** are drawn as a job-log panel (`run_log(job, step, capture)`): title "Lint and Format
  Check › Run Black formatter check", the captured text inside (the `$` line becomes the step's
  heading, `[exit N]` is shown as a small GREY "exit 1" badge on the panel, never as text), tag
  `live · stand-in runner` (GREY, bottom right). The `uses:` stand-ins (`*-standin.txt`) are never
  shown as if they were the action: the panel says "download-artifact" with the stand-in's output
  only where it proves a point (the tar size, `0` coverage files).
- **The run graph** (`run_graph(results)`): six nodes in GitHub's layout (build → four → summary),
  tagged `illustration · colours from our live runs`. Beside it in S07/S12, the README screenshot's
  transcription (`expected/readme-screenshot-run-graph.txt`), re-drawn small and tagged `recorded`
  with its timings.
- **Placeholders**: the webhook URL only as `https://hooks.slack.com/services/<your-webhook-path>`;
  the secret's value only ever as `***`; `<you>` for the GitHub user. No real-looking token, URL or
  id anywhere.
- **Versions, all "at the time of recording"**: Docker 29.8.2, git 2.54.0, pre-commit 4.7.0 (config:
  Black 24.1.1, Flake8 7.0.0), act 0.2.97; in the image (unpinned): Python 3.11.18, black 26.10.1,
  flake8 7.5.0, pytest 9.2.0, pytest-cov 7.1.0.
- **Crops**: commit ids beyond 7 characters, container ids, timestamps and the access-log client
  addresses (`172.18.0.1:…`) are cropped or never read aloud; long build logs show first lines, `…`,
  last lines; ANSI codes in `62` are stripped.

## Visual set pieces (the 3Blue1Brown part)

Class names go in `scenes/common.py`. None collides with a scene class in `video.yaml`.

- **V1 · `HookChain` — slides 14 → 15 → 16: the checks move from one laptop to the shared repository
  (S02, S13).** A GREY laptop frame labelled "Git local hooks" holds slide 14's chain re-drawn with
  *this repo's* boxes: `hygiene ×7` → `Black` → `Flake8` (Conflict 3: formatter first, then linter,
  **no tests**: a "Tests" box slides in GREY dashed and is struck out, "CI runs these"). A
  commit dot passes through each gate. Then `git push`: the dot flies (PINK) out of the laptop into
  a BLUE "Shared Repository" frame, where **nothing** checks it (slide 15: the gates stay behind on
  the laptop). The frame then fills with slide 16's three boxes: `Build Container` → `Check Code` →
  `Test Summary`. A second laptop appears with no hooks installed (slide 3: "only where someone ran
  `pre-commit install`"); its dot reaches the server unchecked too.
  - S02: the remote-hook row (slides 5–6): a gate *in front of* the server door labelled
    `pre-receive` (can refuse: the dot bounces), `update` (the same, one branch at a time), and a
    bell *behind* the door, `post-receive` (runs after the code is in: it can only report). The
    caption that carries to S15: "Actions on a push is the bell, not the gate."
  - S13: `git commit --no-verify` draws a RED bypass arc around all three laptop gates (slide 30's
    command); the dot reaches the server, and only there does `Check Code` catch it.
- **V2 · `CiLoop` + `PipelineStrip` — slide 21's loop and slide 26's row (S03, S07, S12, S16; the
  strip in every Part 2 scene).** The loop: "Developers" → (PINK `Commits`) → `Codebase` → `Build` →
  `Test`, and two dashed PINK return lines into a "Notifications" bar that leads back to the
  developers. It is drawn *open* in S03 (the return lines dashed, a "?"), carries real checks in S07
  (✓/✗ beside the commit), and closes in S12 (the fix commit goes around once and comes back green).
  The row: slide 26's five boxes `Commit → Build Container → Lint and Format → Test → Summary`, then
  shrunk to a thin strip under the tracker for Part 2; the current box fills YELLOW (S08 Build
  Container, S09 Lint and Format, S10 Test, S11 Summary).
- **V3 · `TriggerLanes` — when the robot wakes up (S04).** Three horizontal branch lanes, `main`,
  `develop`, `feature/login`, with commit dots. `on: push: branches: [main, develop]` (`ci.yml:7-9`)
  becomes two PINK sparks: a push to `main` or `develop` lights a BLUE runner icon; a push to
  `feature/login` lights nothing. Then `pull_request: branches: [main, develop]` (`10-11`): opening a
  PR from `feature/login` into `main` makes a GREY dashed **ghost merge commit** above `main` (the
  feature merged into main, not yet real), labelled `github.sha`; *that* is what gets built and
  tested (slide 23 made literal: "each merge is tested"). A GOLD meter under the lanes ticks one
  run per spark (slide 24: frequency vs compute cost; the branch filter is a cost decision). Last
  beat: the sparks fire **after** the push lands on the server (the bell of V1), never before.
- **V4 · `JobGraph` — the YAML becomes a graph (S03, S05, S07, S11).**
  - S03: `ci.yml` (WHITE text panel) unfolds into a tree: `on` at the root, six job nodes
    (`build` … `test-summary`), one job expands into its steps; `run:` steps get a `>_` glyph,
    `uses:` steps a small PURPLE puzzle piece (a reusable action).
  - S05: slide 26's straight row is the start: `Commit` drops out ("the event, not a job"), `Build
    Container` stays left, `Lint and Format` and a `Test` box slide into **parallel lanes**, `Test`
    splits into three, `Summary` sits right. Each `needs:` line (`ci.yml:44, 73, 108, 131, 175`)
    draws one arrow as it is highlighted; the arrow from `lint-and-format` to `test-summary` is
    **missing**, drawn as a GREY dashed gap with a "?" (Conflict 5; answered in S11). The columns get
    `act -l`'s labels `stage 0 / 1 / 2` (`laptop/61`). A Gantt bar row under it from the screenshot's
    timings (`recorded`): 54 s, then four bars in parallel (22/18/20/39 s), then 4 s; the critical
    path glows; a GOLD second ruler adds the six job durations each rounded **up** to a minute:
    "about 2 minutes on the clock, about 6 billed minutes" (digest §2; not measured here).
  - S07: the same graph, node by node coloured as run 1 finishes (YELLOW running → GREEN/RED).
  - S11: three PINK result tokens (`success`, `success`, `success`) slide along the three `needs`
    arrows into the summary node; the lint node is RED, but no token leaves it (the dashed gap).
- **V5 · `ImageSuitcase` — build once, every job starts empty (S08).** Six BLUE rooms in the job
  graph's layout, each with an empty "Docker" shelf (the real empty `docker images` header, `x1`).
  In the build room, Dockerfile layers stack into a TEAL cube stamped `cheese-app-api:<sha>`
  (`github.sha`: "this commit, nothing else"). `docker save` folds the cube into a TEAL tar suitcase
  ("about 176 MB"); `upload-artifact` carries it to a BLUE "artifact store" shelf outside the rooms
  with a GOLD "1 day" tag; the build room **dissolves** (the VM is destroyed). Four copies fly into
  four rooms; `docker load` unfolds each back into the same cube (`x2`). The summary room gets no
  suitcase (it needs only bash). The ponder variant: a room without `docker load` asks its shelf
  for the cube, finds nothing, walks out to an ORANGE "Docker Hub" door and is turned away RED
  (`pull access denied`, `noload/x2`).
- **V6 · `ExitGates` — every step is a gate that reads an exit code (S09, S10, S13).** A job is a
  column of step gates; each command ends by holding up its exit code. `0` = the gate opens GREEN;
  `1` = the gate shuts RED, red climbs **step → job → run badge**, and the steps below grey out,
  dashed (*skipped*), except those marked `if: always()`, which a small PINK "always" bridge still
  reaches. `continue-on-error: true` is a GREY shunt around a gate: the code still shows `1` (or
  `3`), the flow goes on, the job stays GREEN with a small warning dot.
  - S09: Black `1` shuts; Flake8 greys out (skipped); a ghost replay shows what it *would* have said
    (`x4`), passing through its shunt.
  - S10: the coverage gate shows `3` and is shunted; "Upload coverage report" (`if: always()`)
    still runs and carries an empty box (0 files).
  - S13: run 3: Black `1` again, on `service.py` this time.
- **V7 · `SystemTestRig` — one runner, two containers, one port (S10).** Inside one BLUE runner: a
  TEAL `api-server` container (`docker run -d … -p 9000:9000 -e DEV=1`) with an ORANGE door 9000 on
  the runner; a `sleep 10` hourglass; a `curl -f` guard that knocks and gets
  `{"message":"Welcome to the Cheese App CI/CD Tutorial!"}` (`05:8`): only then does the next gate
  open. A second TEAL container (the tests) starts with its own bubble; `--network host` dissolves
  its bubble into the runner, so its PINK `localhost:9000` arrow reaches the door. The server's log
  scrolls the arrivals (`07:10-15`). L09's trapdoor (`skipif`) is drawn small and shut: "in CI the
  curl guard means a missing server fails loudly, not skips quietly". The two `if: always()` steps
  (logs, stop) fire after.
- **V8 · `SlackRoute` — who calls whom, and the bell that can't ring (S14).** Two arrows, one after
  the other (slides 7, 9 vs the tutorial; Conflict 6): (1) the lecture's **webhook**: a BLUE GitHub
  box fires a PINK POST *out* to an outside URL (Jenkins, a deploy server, a chat); (2) the
  tutorial's step: inside a BLUE runner, the last step of `test-summary` POSTs *in* to Slack's
  **incoming webhook**, a URL Slack gave you. A BLUE vault (Settings → Secrets and variables →
  Actions, `illustration`) holds `SLACK_WEBHOOK_URL`; it lends the key to the job and every log line
  shows `***`. Then the run-demo replay with V6's gates: "Check test results" shuts RED (`exit 1`),
  "Check if Slack webhook is configured" greys out (skipped), its `enabled` output stays empty, and
  the Slack step's condition reads `'' == 'true'`: false. The GREY chat window stays silent; a RED
  bell with a slash. Fix overlay: `if: always()` on `slack-check` (one line) lets the bell ring ❌.

## README step tracker (ReadmeTracker, top-left)

One tracker for the assigned section, titled with the README's own heading; one short tracker for
the optional Part 6. Steps the README does not have are marked `extra` in the tracker caption and in
the narration ("this one isn't in the README"). Step titles are ≤ 3 words.

| tracker | README lines | steps |
| --- | --- | --- |
| **P5 · Part 5: GitHub Actions (Remote CI)** | 277–365 | Pipeline file · Six jobs · Key concepts · git add · git commit · git push · Actions tab · Read results (8) |
| **P6 · Part 6: Branch Protection (Optional)** | 369–397 | Add rule · Pick checks · New branch · Break tests · Commit, push · Open PR (6) |

- P5 step 1 = README 279–283 (the Python 3.11 line, the file, the triggers); step 2 = 285–330 (the
  six job descriptions); step 3 = 332–342; steps 4–6 = 346–348; step 7 = 351–357; step 8 = 359–365
  ("CI Pipeline in Action") and every job log after it.
- Extras (captured, marked `extra`): `laptop/01` (the pin), `02` (clone; the README says "Clone or
  download", no URL), `03`, `04` (`.github/workflows/` at the root), `05`, `13`, `14`, `20`–`23`
  (your repo, stand-in), `23`/`38`/`47` (the commit the runner checks out: shown once), `30`–`38`
  (the fix: README **Part 4**, from L09, caption "Part 4 · L09"), `40`–`49` (`--no-verify`, slides
  29–31), `55`–`57` (`test_broken`), `60`–`62` (act), every `runner/*/x*.txt`, `noload/`, `run-demo/`.
- S01 has no tracker; S02 is lecture only (no tracker); S16's recap has none.

## Scene plan

Notation:
- `laptop/NN` = `assets/terminal/laptop/NN-*.txt`; `run1/<job>/NN` = `assets/terminal/runner/run1/<job>/NN-*.txt`
  (likewise `run2`, `run3`, `run-demo`, `noload`); `expected/…` = `assets/terminal/expected/`.
  Line 1 of a capture is the `$` command (typed in a laptop terminal; the step heading in a run log);
  `[exit N]` is never printed as text.
- ▶ = a README step the viewer must do; a YELLOW `▶ your turn` tag at real checkpoints only.
- CODE(path: a-b) quotes `assets/source/cheese-app-ci-cd/` with real line numbers, ≤ 12 lines on
  screen; `history/<file>` = `assets/source/cheese-app-ci-cd-history/`.
- `lecture_ref(21, "a–b")`, GREY, top right, **only while that slide's picture or idea is on screen**.
  Slide numbers are the PDF pages of `SLIDES.md`, never the footers.

### Part 1 · Read it, push it, watch it

**S01 · Red run, green summary (~220 words) — `s01_hook.py` · `Hook`.** Cold open, no tracker.
- The broken thing, real text side by side: a run log "Test Summary › Check test results" with
  `Unit Tests: success` / `Integration Tests: success` / `System Tests: success` / **`✅ All tests
  passed!`** (`run1/test-summary/01:13-16`), and under it act's last line for the same commit,
  **`Error: Job 'Lint and Format Check' failed`** (`62:750`, RED). Then the run graph
  (`illustration`): five green nodes, one red, the run badge red. "You pushed the course's own code,
  untouched. The pipeline says the tests all passed, and the pipeline failed. Both are true." On
  screen, the question that stays: *"Which machine said no, and why didn't the summary hear it?"*
- One beat of where this sits: in L09 these checks ran on **your** laptop, before a commit; today
  they move to GitHub and run on every push, on machines nobody owns.
- `lecture_ref(21, "1, 4")`: the deck's four sections as four small labels (remote Git hooks, GitHub
  webhooks, continuous integration, continuous deployment), "slide by slide, and the README's Part 5
  step by step".
- How to follow along: your clone from L09, Docker, a GitHub account and a repository of your own;
  the tracker, code panels with path and lines, `▶ your turn`; the study guide has every command.
  No cloud, no keys, no bill on a public repo. One sentence: "the runs you'll see ran live on fresh
  machines here; the GitHub pages are drawings, marked as such."

**S02 · Hooks stay on your laptop (~300) — `s02_hooks.py` · `LocalHooks`.** No tracker (lecture).
- `lecture_ref(21, "2–3")`: recap: last lecture's local Git hooks, `pre-commit` and `pre-push`.
  Said correctly (Conflict 1): "pre-commit runs on your laptop, before the commit even exists." V1's
  chain with this repo's boxes; CODE(`.pre-commit-config.yaml`: 29-44) one beat: Black 24.1.1,
  Flake8, both at 120, both only on `^src/`. The "Tests" box struck: this repo's hooks run no tests.
- Slide 3's limit: hooks run only where someone installed them; a second laptop without
  `pre-commit install` sends its commit through unchecked.
- `lecture_ref(21, "5–7")`: V1's server door: `pre-receive` (before the push is accepted; can refuse),
  `update` (per branch), `post-receive` (after; integration tests, notifications, clean-up). Kindly
  (Conflict 2): "GitHub.com doesn't run your own pre-receive scripts. It gives you two pieces instead:
  Actions, which runs after the push, and branch protection, which can say no. We'll meet both."
  Slide 7: hooks act inside Git; to tell Slack, you need a webhook (S14).
- `lecture_ref(21, "14–16")`: V1's move: slide 14's chain, the push (slide 15: on the shared repo
  nothing runs the checks), slide 16's three boxes on the server: `Build Container`, `Check Code`,
  `Test Summary`. "That move is continuous integration."

**S03 · The CI loop and the workflow file (~290) — `s03_pipeline.py` · `CiPipeline`.** Tracker P5
step 1.
- `lecture_ref(21, "17, 21–22")`: slide 22's definition as one caption: a series of scripts that
  run automatically whenever the code changes: integrate continuously, test automatically, enforce
  coding standards, run static analysis. Slide 17's payoff in ordinary software, one line (faster
  releases, better code, easier coordination); "ML adds a twist; we come back to it at the end."
  V2's loop drawn open.
- `lecture_ref(21, "25–28")`: slide 25 "from concept to GitHub Actions"; slide 26's row (V2), slide
  27's one-line purpose under each box. Slide 28 points to this README: the tracker shows "Part 5:
  GitHub Actions (Remote CI)" (no narration about the slide's old anchor).
- ▶ (reading) README 279–283 as a README panel: "All CI tests run inside Docker containers using
  Python 3.11 (same as production)". Kindly, one clause: this repo has no production yet; read it as
  "the same image you would deploy".
- Extra `laptop/04`: `ls -la .github/workflows/` → `ci.yml` **at the repository root**: GitHub looks
  only there (a monorepo subfolder never runs; digest G2, one sentence).
- V4 (S03 form): CODE(`.github/workflows/ci.yml`: 5-17) — `name: CI Pipeline`, `on:`, `jobs:`,
  `build:` with `runs-on: ubuntu-latest` — unfolds into event → workflow → jobs → steps. A step is a
  shell script (`run:`) or a reusable action (`uses: actions/checkout@v4`).

**S04 · When does the pipeline wake up? (~230) — `s04_triggers.py` · `WhenItRuns`.** Tracker P5
step 1 (the trigger sentence, README 283).
- `lecture_ref(21, "25")`: the slide says "on every push or pull request". CODE(`ci.yml`: 7-11) and
  V3: only pushes to `main` or `develop`, and pull requests **into** them (Conflict 4). "On any other
  branch, the pipeline waits for your pull request." Kindly, one clause: the comment on `ci.yml:2`
  says main only; the triggers say main and develop.
- `lecture_ref(21, "23")`: on a PR run, `github.sha` names a temporary merge of your branch into
  `main`: what will land is what gets tested.
- `lecture_ref(21, "24")`: how often to integrate is a cost decision; this file's answers: a branch
  filter, parallel jobs, a one-day artifact (GOLD meter).
- The bell, not the gate: the run starts after the push is accepted; a red run does not undo it.
- **PONDER 1** (8 s), answered right after with V3.

**S05 · Six jobs, one graph (~290) — `s05_jobs.py` · `SixJobs`.** Tracker P5 steps 2–3.
- ▶ (reading) README 287 "6 jobs that run in parallel (except for dependencies)" and the six
  headings (289, 296, 303, 310, 316, 325) as six chips, each with its job id and its `name:` from
  `ci.yml` (`Build Docker Image`, `Lint and Format Check`, `Unit Tests`, `Integration Tests`,
  `System Tests`, `Test Summary`): "remember the names; GitHub shows these" (S15 needs it).
- `lecture_ref(21, "26–27")`: V4's unfold from slide 26's row into the graph, one `needs:` line at a
  time (CODE `ci.yml`: 44, 73, 108, 131, 175-176, highlighted in turn). Kindly (Conflict 5): "The
  lecture lists the stages in order. On GitHub four of them run side by side, and the summary listens
  only to the tests." The dashed gap from lint stays on screen with a "?".
- Extra `laptop/61` (`act -l`): the same graph, read from the file by a tool: stages 0, 1, 2.
- ▶ (reading) README 332–342 "Key CI/CD Concepts" as five chips — Artifact Sharing, Parallel
  Execution, Conditional Execution, Unique Image Tags, Network Modes — each pinned to the place in
  the graph where Part 2 opens it (S08, S05, S10/S11, S08, S10).
- Gantt + GOLD ruler (V4), from the screenshot (`recorded`): about 2 minutes on the clock, about 6
  billed minutes on a private repo; public repos are free.

**S06 · Push to a repo of your own (~270) — `s06_push.py` · `PushIt`.** Tracker P5 steps 4–6.
- Extras `laptop/01`, `03`: the pin is still the head of `main`; the last commits ("demo class 1",
  twice: "the second one undid a bug planted in class; we'll run that bug later").
- ▶ `laptop/10` `git add .` (no output) → ▶ `laptop/11` `git commit -m "Add CI pipeline"`:
  `nothing to commit, working tree clean` (RED, exit 1). Erratum, kindly: in a clone or fork the
  pipeline is already committed; nothing new to add, and that's fine.
- Extra `laptop/13` `git remote -v`: `origin` is the course's repository (ORANGE). The README's
  `git push` from here would be refused by GitHub, "permission denied" (said, not shown). Your
  `origin` must be a repository **you** own: a fork (then enable workflows on its Actions tab), or a
  new empty repo + `git remote set-url origin https://github.com/<you>/cheese-app-ci-cd.git` (shown
  as a code card, not run).
- The stand-in, said once (Running example): extras `laptop/20`, `21` on this machine.
- ▶ `laptop/22` `git push`: `* [new branch]      main -> main`. YELLOW `▶ your turn`. "This push is
  the event. Run 1 starts now." Extra `laptop/23`: the commit the runners will check out, `b8458ff`
  (7 characters shown): "the same commit you just pushed, so the same image tag".
- One sentence (digest G20): if you already pushed this commit, a push says `Everything up-to-date`
  and starts nothing; make a real change (part 2 makes one).

**S07 · Watch the run: six colours (~250) — `s07_watch.py` · `WatchTheRun`.** Tracker P5 steps 7–8.
- ▶ README 353–357 as a five-line card; the schematic Actions tab (`illustration`): a list with one
  run named after the commit, a YELLOW dot (in progress). Click → the run graph (V4), all six nodes
  grey, `build` turning YELLOW.
- The honest sentence (Running example), with a small inset: six BLUE boxes, each "a fresh machine,
  empty Docker", and `act` on the laptop as the second witness.
- **PONDER 2** (8 s) before any node turns colour.
- The reveal, node by node from `run1/results.txt`: Build ✓, Lint and Format Check ✗, Unit ✓,
  Integration ✓, System ✓, Test Summary ✓; the run badge ✗. `lecture_ref(21, "21")`: those ✓/✗ marks
  next to your commit are the loop's notifications (V2). Extra `laptop/62` act's verdict lines
  (`62:421, 513, 567, 682, 732, 749, 750`): five `Job succeeded`, one `Job failed`, the same answer.
- Kindly (errata 1): the README's screenshot (`recorded` transcription beside the graph) is all green;
  it shows an earlier version of the code. Your first run is red; part 2 turns it green.
- Part 1 ends on the hook reproduced: the red Lint node and the green Summary node pulse together.
  "Two of these six machines disagree. In part 2 we open every log, one job at a time." Clean frame.

### Part 2 · The run, job by job, then around the loop

Every Part 2 scene except S16 carries V2's thin pipeline strip under the tracker, the current box
YELLOW. Run logs are `run_log` panels tagged `live · stand-in runner`.

**S08 · Build once; every job starts empty (~340) — `s08_artifact.py` · `BuildOnce`.** Tracker P5
step 8; strip: Build Container.
- `lecture_ref(21, "27, 31")`: slide 27's reason to build the container first: one environment for
  every check, build problems found early. The lecture draws one remote CI server; GitHub gives you a
  new one **for every job** (`runs-on: ubuntu-latest`, six times: `ci.yml:17, 43, 72, 107, 130, 174`).
- README 289–294 (Build Job bullets) as a README panel; CODE(`ci.yml`: 15-38).
- V5, with the real logs: `run1/build/03` (first lines incl. line 2 `building with "default"
  instance using docker driver`, `…`, last lines `naming to … cheese-app-api:b8458ff0…`), `04`
  (`docker save … -o /tmp/cheese-app-api.tar`, no output), `05` (`ls -l` → about 176 MB), `x1`
  (the image on the build runner). The SHA tag: "this commit's image, nothing else" (README 340).
- Erratum, kindly (README 291, "Docker Buildx for efficient caching"): the Buildx step sets up a
  builder, but the build runs on the default one and nothing is cached between runs (`03:2`; extra
  act `62:313`, `docker:default`). Every run rebuilds from scratch: fine for a toy, slow for a big
  image; caching would need `cache-from`/`cache-to` (exercises).
- Into a check job: `run1/lint-and-format/x1` → empty `docker images` (just the header); download
  (CODE `ci.yml`: 49-57) and ▶ `run1/lint-and-format/03` `docker load -i /tmp/cheese-app-api.tar`;
  `x2` → `cheese-app-api:b8458ff…` is there. README 334 "Artifact Sharing" chip lands here. The
  artifact's GOLD "1 day" tag (`ci.yml:38`): "re-running a failed job tomorrow fails at the download"
  (digest G13, one clause).
- **PONDER 3** (8 s), answered with V5's ORANGE door and `noload/x1`, `noload/x2` (`Unable to find
  image … locally`, `pull access denied for cheese-app-api, repository does not exist or may require
  'docker login'`, exit 125): Docker looks on the machine, then on Docker Hub, where no such image
  exists. The step fails, so the job fails.

**S09 · Gates speak in exit codes (~260) — `s09_gates.py` · `ExitCodes`.** Tracker P5 step 8;
strip: Lint and Format.
- `lecture_ref(21, "22, 27")`: slide 22's "coding standards" = Black, "static code analysis" =
  Flake8; L09's distinction in one line: a formatter rewrites, a linter reports.
- README 296–301 panel; CODE(`ci.yml`: 59-67): `continue-on-error: false` on Black (blocking),
  `true` on Flake8 (advisory); both at 120 columns, only on `api/`.
- V6 with `run1/lint-and-format/04`: `would reformat /app/api/utils.py`, `Oh no! 💥 💔 💥`, `1 file
  would be reformatted, 2 files would be left unchanged.`, exit 1; `00-steps.txt`: Black `failure`,
  **Flake8 `skipped`**. "A step fails when its command exits with anything but zero. That is the
  only thing CI listens to."
- CODE(`src/api-service/api/utils.py`: 7-13): `def power(base,exponent):` and three blank lines: the
  mess L09 met, still in the repo (put back on purpose for teaching; never say anyone skipped hooks).
- Extra `run1/lint-and-format/x4`: what the skipped Flake8 step would have said (`E231` at 7:15,
  `E303` at 13:1), through its shunt: "even then, advisory: the job would still turn on Black alone".

**S10 · Three test jobs, three altitudes (~300) — `s10_tests.py` · `TestJobs`.** Tracker P5 step 8;
strip: Test.
- `lecture_ref(21, "27")`: the slide's one Test box splits into three jobs (V4).
- **Unit** (README 303–308; CODE `ci.yml`: 88-102): `run1/unit-tests/04` → `11 passed` (first/last
  lines). Then `05`, the coverage run: `11 passed` again, but an `INTERNALERROR> … PermissionError:
  [Errno 13] Permission denied: 'coverage/style_cb_4667309f.css'` and exit 3; `00-steps.txt:6`
  `failure (continue-on-error: the job stays green)`; `06`: the upload finds `0` files. V6's shunt.
  Erratum, kindly (README 307–308 promise terminal, XML and HTML reports, uploaded): Docker creates
  the missing `coverage/` folder as `root` (extra `x3`: `root root`, `uid=1000(app)`), the container
  user can't write into it. Fix in one line: create the folder writable first and point XML into it
  (exercises).
- **Integration** (README 310–314; CODE `tests/integration/test_api.py`: 9-11, `TestClient(app)`):
  `run1/integration-tests/04` → `10 passed`: the app called in-process, no server, no port.
- **System** (README 316–323; CODE `ci.yml`: 146-169): V7 with `04` (`docker run -d --name api-server
  -p 9000:9000 -e DEV=1 …`, container id cropped), extra `x3` `docker ps` (`0.0.0.0:9000->9000/tcp`),
  `05` (`sleep 10`, `curl -f` → `{"message":"Welcome to the Cheese App CI/CD Tutorial!"}`), `06` →
  `5 passed`, `07` server log (`Running in DEV mode`, `Application startup complete.`, then the
  requests: `GET /`, `GET /health`, …, `GET /euclidean_distance/?x=3&y=4 … 200 OK`; client addresses
  cropped), `08` stop and remove. README 338 and 342 chips land: "Conditional Execution" = the two
  `if: always()` steps; "Network Modes" = `--network host`. L09 callback, one sentence: the
  `curl -f` gate is why a dead server fails here instead of skipping.

**S11 · The summary listens only to tests (~260) — `s11_summary.py` · `TheSummary`.** Tracker P5
step 8; strip: Summary.
- `lecture_ref(21, "16, 26–27")`: Summary "collects the results and reports pass or fail". README
  325–330 panel; CODE(`ci.yml`: 172-192): `needs: [unit-tests, integration-tests, system-tests]`,
  `if: always()` (runs even when a dependency failed: it runs, it doesn't pass), the three
  `needs.<job>.result` lines, `status=…` written to `$GITHUB_OUTPUT` for later steps, `exit 1` when
  any result isn't `success`.
- V4's tokens: run 1's three `success` tokens arrive (`run1/test-summary/01:13-16`, `✅ All tests
  passed!`). The hook answered: lint is **not** in `needs`, so its failure never reaches the summary;
  the run is red because *any* failed job makes the run red. Kindly (Conflict 5, errata): "Checks the
  results of all test jobs" is literally true; lint isn't a test job. Fix: add `lint-and-format` to
  `needs` and to the check (exercises). The dashed gap closes in a GREY dashed "after the fix" arrow.
- The demo commit: CODE(`history/c3b227f-service.py`: 38-44) — `result = math.sqrt(2 * z)` (the
  in-class demo bug, 2025-11-13).
- **PONDER 4** (8 s), answered with `run-demo/results.txt` on the graph: unit ✓ (only `power()` is
  tested), integration ✗ (`04`: `1 failed, 9 passed`, `assert 7.0710678118654755 == 5.0`), system ✗
  (`06`: `2 failed, 3 passed`, `3.162…` vs `2.236`, `7.071…` vs `5.0`), lint ✗ (still `utils.py`), and
  now **Test Summary ✗**: `❌ Some tests failed!` (`run-demo/test-summary/01:13-16`). "This time the
  summary heard it."

**S12 · Fix, push, green: one turn of the loop (~240) — `s12_green.py` · `RedToGreen`.** Tracker P5
step 8, then extras with the caption "Part 4 · L09".
- `lecture_ref(21, "21")`: V2's loop: the notification came back; now the developer fixes and
  commits again.
- The fix is L09's tool, briefly (extras): `laptop/30` (`pip install pre-commit`: first and last
  lines, `pre-commit-4.7.0`), `31` (`pre-commit installed at .git/hooks/pre-commit`), ▶ `32`
  `pre-commit run --all-files` (README.md:262): the hygiene hooks pass, **Black `Failed`**, `files
  were modified by this hook`, `reformatted src/api-service/api/utils.py`; `33` `git diff`:
  `power(base, exponent)` and one blank line gone; `34`: all hooks pass.
- `35`–`37`: `git add .`, `git commit -m "Format utils.py with Black"` (the hooks run and pass;
  "the message is ours, the README has none"), `git push` → `b8458ff..2289d89  main -> main`. ▶ your
  turn.
- Run 2 on the graph: all six ✓ (`run2/results.txt`); `run2/lint-and-format/00-steps.txt`: Black
  `success` **and** Flake8 `success` (it ran this time). Now it matches the README screenshot
  (`recorded`, beside it, with its timings). The loop closes GREEN.

**S13 · The local conundrum: --no-verify (~290) — `s13_noverify.py` · `NoVerify`.** Extras (slides);
strip: Lint and Format.
- `lecture_ref(21, "29–31")`: slide 29's question: why run the checks again, remotely, if the hooks
  already ran them? A hurried edit, extra `laptop/40` (`z=power(x,2)+power(y,2)` in `service.py`),
  `41` `git add .`, `42` `git commit -m "quick fix"`: **Black `Failed`**, `reformatted
  src/api-service/api/service.py`, exit 1: the hook stopped it. `43` `git status --short` → `MM`: the
  hook fixed your working copy, but the staged copy is still the messy one.
- Slide 30's command, extra `44`: `git commit --no-verify -m "quick fix"` → `[main 2892b1b] quick
  fix`: no hook ran. V1's RED bypass arc. `45` `git push`. Run 3: lint ✗ (`run3/lint-and-format/04`:
  `would reformat /app/api/service.py`), all tests ✓, summary ✓ (`run3/results.txt`); extra `x4`:
  the skipped Flake8 would have flagged `service.py:43` (`E225`, `E231` twice). "What `--no-verify`
  let through, CI caught. Slide 31, live."
- Clean up the experiment: `48` (` M`: the hook's reformatted copy, never committed), `49` `git
  restore …`. (On your repo: fix it and push again, as in S12.)
- The holes, kindly (Conflict 8): CI re-runs **two** of the local checks, Black and Flake8, on
  `api/` only. The seven hygiene hooks — trailing whitespace, end of file, YAML, large files, JSON,
  merge-conflict markers, private keys — never run in CI. One clause: pre-commit pins Black 24.1.1,
  the image installs the newest (26.10.1 at the time of recording); they agreed here, but they can
  drift.
- **PONDER 5** (8 s), answered: no job catches it. The fix is one CI step, `pre-commit run
  --all-files` — `lecture_ref(21, "11")`: exactly the failed step the lecture's imagined Slack
  message shows.

**S14 · Webhooks, secrets and the Slack bell (~270) — `s14_slack.py` · `SlackBell`.** Extras (the
README never mentions Slack); strip: Summary.
- `lecture_ref(21, "7, 9")`: a webhook is GitHub calling an outside URL when something happens:
  start an external CI such as Jenkins, deploy, post to a chat. V8 arrow (1).
- `lecture_ref(21, "10–12")`: the lecture *imagines* a Slack channel told about every push, failures
  included ("shame" becomes a friendly RED bell). Slide 11's card re-drawn as **the lecture's wish
  list** (failed step, test counts, lint counts, duration; no names: the author is "a teammate", the
  reply is not drawn), beside the **real payload** (CODE `ci.yml`: 207-217 and 239-245: ✅/❌ header,
  repository, branch, commit, author, one ✅/❌ per test job, two links), drawn as a GREY chat card
  tagged `illustration`. "This is what the lecture wishes for; this is what this workflow sends."
- V8 arrow (2), Conflict 6: the tutorial's bell works the other way round: Slack gives you an
  **incoming webhook** URL, and the last steps of `test-summary` call it. Where it goes: Settings →
  Secrets and variables → Actions → New repository secret, name `SLACK_WEBHOOK_URL`, value a
  placeholder `https://hooks.slack.com/services/<your-webhook-path>` (schematic, `illustration`; not
  Settings → Webhooks). Never in the repo; masked `***` in logs; not given to PRs from forks.
- CODE(`ci.yml`: 194-205): the check step. Why not `if: secrets…` directly: CODE(`history/199abd9-to-
  1a5e363-ci.yml.diff`: 1-21) — the repo's own history tried it and replaced it with a shell check
  that writes `enabled=true/false` to `$GITHUB_OUTPUT`. Run 1, no secret: `run1/test-summary/02`
  (`if [ -n "" ]` → `enabled=false`), `00-steps.txt:4` Slack `skipped`.
- The bug, with V6/V8 on the demo run: `run-demo/test-summary/00-steps.txt`: "Check test results"
  `failure`, "Check if Slack webhook is configured" **`skipped`**, Slack `skipped (… enabled is '')`.
  "As written, the bell only rings for good news." Fix: `if: always()` on the check step (exercises
  has the hardened version with `env:`).

**S15 · Branch protection: from report to gate (~220) — `s15_protect.py` · `ProtectMain`.** Tracker
P6 1–6 (optional section).
- `lecture_ref(21, "5–6")`: back to V1's door: a push-triggered run is the `post-receive` bell; on
  GitHub.com the gate that refuses is **branch protection** with required status checks.
- README 373–379 as a schematic Settings → Branches page (`illustration`): pattern `main`, "Require a
  pull request before merging", "Require status checks to pass before merging". Erratum, kindly: the
  picker lists checks by the jobs' **names** (`Lint and Format Check`, `Unit Tests`, `Integration
  Tests`, `System Tests`), not the ids the README lists, and only after they have run once; today's
  page may call it a "classic branch protection rule" or offer rulesets. GOLD: on a private repo
  this needs a paid plan (free for public repos; GitHub Pro comes with the Student Developer Pack).
- README 383–396 as a CODE card (the commands are not captured on GitHub; shown, not run). Kindly:
  pushing `feature/test-protection` starts nothing (S04's lanes); the run starts when you open the
  PR. The README's breaking line, run locally: ▶ `laptop/51` `echo "def broken(): assert False" >>
  tests/unit/test_utils.py`, extra `53` → still **`11 passed`**: pytest only collects functions named
  `test_*` (CODE `pytest.ini`: 8). Extra `55` `def test_broken(): …` → `57`: `1 failed, 11 passed`.
  "That's the one that turns the PR red, and with protection on, the merge button stays locked." The
  blocked PR itself is described, not drawn as a real page.

**S16 · Non-determinism, CD next, and recap (~220) — `s16_recap.py` · `Recap`.** No tracker.
- `lecture_ref(21, "17–20")`, ~25 s: when the code trains a model, non-determinism enters at every
  stage (training, data, tests, deployment); the four answers: version everything (L11's DVC), automate
  retraining and testing, monitor in production, roll out in a controlled way. "Milestone 5 asks for
  the second one." `lecture_ref(21, "23–24")` in one clause: fast detection, at a cost you choose.
- `lecture_ref(21, "32–34")`, ~10 s: continuous deployment automates the release once everything is
  tested; in this course that is L23. The repo is called ci-cd but holds the CI half.
- Teardown card (see "Costs and teardown"), each line spoken briefly.
- V2's loop one last time, all four arcs lit; then the recap questions (5, one at a time; answers in
  exercises.md). Point to the study guide and exercises in MLOps_Learning.

## Word budget

| scene | words | scene | words |
| --- | --- | --- | --- |
| S01 Hook | 220 | S08 BuildOnce | 340 |
| S02 LocalHooks | 300 | S09 ExitCodes | 260 |
| S03 CiPipeline | 290 | S10 TestJobs | 300 |
| S04 WhenItRuns | 230 | S11 TheSummary | 260 |
| S05 SixJobs | 290 | S12 RedToGreen | 240 |
| S06 PushIt | 270 | S13 NoVerify | 290 |
| S07 WatchTheRun | 250 | S14 SlackBell | 270 |
| | | S15 ProtectMain | 220 |
| | | S16 Recap | 220 |
| **part 1** | **1,850** | **part 2** | **2,400** |

Total ≈ **4,250** words ≈ 24.5 min of narration. If the script runs long, trim S05's Gantt beat,
S08's Buildx erratum and S16's ML beat first; never trim a README step.

## Ponder questions

Five timed ponders, as Conny decided on 2026-10-21 (3–5 per video); REVIEW.md marks content gate 3
met with that decision. Each is quiz-style with a YELLOW timer and answerable from what was shown
just before. The answer is said right after the timer.

| # | scene | question (as on the card) | answer |
| --- | --- | --- | --- |
| 1 | S04 (8 s) | "You push three commits to feature/login.\nHow many CI runs start?\nThen you open a PR into main: how many now,\nand which commit does it test?" | None for the pushes (the branch filter). One when the PR opens (and one per later push to that branch while it's open); it tests a temporary merge of `feature/login` into `main` (`github.sha`), not your branch tip |
| 2 | S07 (8 s) | "This is the course's code, untouched:\nutils.py is still messy (L09).\nPredict all six: Build, Lint, Unit,\nIntegration, System, Test Summary." | Build ✓, Lint and Format Check ✗ (Black), Unit ✓, Integration ✓, System ✓, Test Summary ✓, run ✗ — the summary's `needs` leaves lint out (`run1/results.txt`) |
| 3 | S08 (8 s) | "Delete the 'Load Docker image' step\nfrom unit-tests.\nWhich step fails, and with what error?" | "Run unit tests": the fresh machine has no image, Docker tries Docker Hub: `Unable to find image … locally`, `pull access denied for cheese-app-api …`, exit 125 (`noload/x2`) |
| 4 | S11 (8 s) | "The demo commit computes sqrt(2·z)\ninstead of sqrt(z).\nWhich jobs turn red,\nand what does Test Summary say now?" | Integration ✗ (1 of 10), System ✗ (2 of 5), Unit ✓ (only `power()` is unit-tested), Lint ✗ anyway (`utils.py`), Test Summary ✗ `❌ Some tests failed!` (`run-demo`) |
| 5 | S13 (8 s) | "A teammate commits a private key file\nwith --no-verify and pushes to main.\nWhich job of this pipeline catches it?" | None. `detect-private-key` is a local hook only; CI runs Black and Flake8 on `api/`. Add `pre-commit run --all-files` as a CI step (then rotate the key: it is already on GitHub) |

## Recap questions (S16 "Test yourself"; answers in exercises.md)

1. Name two ways code reaches the shared repository without passing your local hooks. Which checks
   does this pipeline repeat, and which does it not?
2. Which unit gets a fresh machine, a job or a step? Why does that force the image tar and a
   `docker load` in every check job?
3. Your run is red but Test Summary says `✅ All tests passed!`. Explain, and give the one-line fix.
4. Why can Flake8 fail without failing its job, and why don't you see Flake8's output when Black
   fails?
5. In the lecture's terms, is a push-triggered Actions run a `pre-receive` or a `post-receive` check,
   and what turns it into a gate on GitHub.com?

(SLIDES' and the digest's other recap items — `--network host`, the `curl -f` gate, `if:` on secrets,
the PR merge commit — go to exercises.md.)

## Errata and drift to state (kindly, with the fix)

1. **The first run is red; the README's screenshot is all green** (README 359–365, `assets/pipline.png`
   from an earlier code state) → `pre-commit run --all-files`, commit, push: run 2 matches it (S07,
   S12).
2. **`git commit -m "Add CI pipeline"` has nothing to commit** in a clone or fork (README 347,
   `laptop/11`) → the workflow is already there; push to your own repo (S06).
3. **`origin` is the course's repo**, so the README's `git push` is refused by GitHub → fork, or
   `git remote set-url origin https://github.com/<you>/cheese-app-ci-cd.git`; on a fork, enable
   workflows (S06).
4. **Test Summary ignores lint** (README 325–330 vs `ci.yml:175`): the run is red while the summary
   says all passed → add `lint-and-format` to `needs` and to the check (S11).
5. **The coverage step fails quietly** (README 307–308 vs `run1/unit-tests/05`, `06`, `x3`):
   `PermissionError`, exit 3, hidden by `continue-on-error`, 0 files uploaded → make `coverage/`
   writable first, write XML into it (S10).
6. **"Uses Docker Buildx for efficient caching"** (README 291): the build runs on the default builder,
   nothing is cached (S08).
7. **The Slack step can never report a failure, and the README never mentions it** (`ci.yml:194-201`,
   `run-demo/test-summary/00-steps.txt`) → `if: always()` on the check step; the secret goes under
   Actions secrets, not Webhooks (S14).
8. **Part 6** (README 378, 388): the checks picker uses job **names**, not ids; `def broken()` is
   never collected (`laptop/53`) → `def test_broken` (`laptop/57`); a feature-branch push starts
   nothing until the PR (S15).
9. **CI re-runs only Black and Flake8 on `api/`** (slides 29–31's promise vs `ci.yml:61, 66`): the
   hygiene hooks (a private key, merge markers) never run in CI → add `pre-commit run --all-files` as
   a step (S13).
10. Small, one clause each: `ci.yml:2`'s comment says main only (S04); "same as production" means the
    same image (S03); pinned Black 24.1.1 vs the image's newest (S13); the artifact expires after one
    day (S08).
11. **Slides vs repo** (SLIDES Conflicts, updated by the captures): pre-commit runs on the laptop
    (said right, S02); Actions is not a remote hook, it reports after the push, protection refuses
    (S02, S15); the local chain here formats, lints and runs no tests (S02); "every push" is pushes to
    `main`/`develop` and PRs into them (S04); the straight five-box row is a fan-out/fan-in graph whose
    summary skips lint (S05, S11); the lecture's webhook calls out of GitHub, the tutorial's step calls
    in to Slack, and sends less than slide 11 (S14); slide 28's link anchor (tracker only, no
    narration).
12. Not in the video (exercises only): README Part 7's auto-format mount hides the entrypoint; local
    Black/Flake8 at default widths vs CI's 120; `ci.yml` links that are empty on PR runs; the
    `Dockerfile:1` "multi-stage" comment; `docker-build.yml`'s history.

## Costs and teardown

No cloud resource is created. GOLD tags appear only for GitHub's meters:
- Actions minutes: free on public repos; private repos use the plan's included minutes, billed **per
  job, rounded up**: a full run is about 6 billed minutes for about 2 minutes on the clock (digest §2,
  from the screenshot's timings; not measured here) (S05);
- artifact storage: the image tar, about 176 MB, kept 1 day (S08);
- branch protection on a private repo needs a paid plan (S15).

Teardown card (S16), each line spoken:
1. If you broke a test for Part 6: close the PR, delete `feature/test-protection`.
2. If you made a Slack app only to try this: delete the repository secret and the incoming webhook.
3. A private repo you won't use: Actions tab → CI Pipeline → ⋯ → Disable workflow (or delete old
   artifacts on the run page).
4. Locally: `git restore` any experiment (`laptop/49`, `58`); the Docker cleanup is L09's (README
   568–574: `docker container ls`, `docker system prune`, `docker image ls`); act users: its images
   (`laptop/63`) can go too.

## README commands checklist (for the follow-along review)

Every README Part 5 instruction, verbatim, in README order (and Part 6, optional).

| README instruction | README line | capture | scene |
| --- | --- | --- | --- |
| "All CI tests run inside Docker containers using Python 3.11 …" | 279 | source panel | S03 |
| CI Pipeline: `.github/workflows/ci.yml`, push / PR to `main` and `develop` | 281–283 | `laptop/04` (extra), CODE `ci.yml` 5-17, 7-11 | S03, S04 |
| Understanding the Pipeline Structure: six jobs | 285–330 | CODE `ci.yml`, `laptop/61` (extra) | S05; each job again in S08–S11 |
| Key CI/CD Concepts | 332–342 | chips | S05; S08, S10 |
| `git add .` | 346 | `laptop/10` | S06 |
| `git commit -m "Add CI pipeline"` | 347 | `laptop/11` | S06 |
| `git push` | 348 | `laptop/22` (to your repo; `13`, `20`, `21` extras) | S06 |
| Go to your repository · Actions tab · runs · ✅ · ❌ | 351–357 | `illustration` + `run1/results.txt`, `laptop/62` | S07 |
| CI Pipeline in Action (the screenshot) | 359–365 | `expected/readme-screenshot-run-graph.txt` (`recorded`) | S07, S12 |
| (each job's log) | — | `run1/<job>/*` | S08–S11 |
| Part 6 · Settings → Branches → Add rule, `main`, two checkboxes, select checks, save | 373–379 | `illustration` | S15 |
| Part 6 · `git checkout -b feature/test-protection` | 385 | shown, not run | S15 |
| Part 6 · `echo "def broken(): assert False" >> tests/unit/test_utils.py` | 388 | `laptop/51`, `53` (+ `55`, `57` extra) | S15 |
| Part 6 · `git add .` · `git commit -m "Intentionally break tests"` · `git push origin feature/test-protection` · open a PR | 391–396 | shown, not run | S15 |

## Things never to do

Series list: no slide images or PDF pages in a frame or the repo (re-draw, cite the PDF page number);
no memes (slides 10, 12, 17, 18, 29, 30, 33, 34, 35); no logos (GitHub/Octocat, GitLab, Playwright,
Slack, Docker); no real person's name on screen or in subtitles (the instructor is `‹instructor›`
if ever needed; slide 11's author and its reply are never drawn); no hand-typed "output"; no command
spelled differently from the README; no credentials, keys, tokens, webhook URLs, IPs or project ids
that look real.

Lecture-specific:
- **Never present an illustration as a real hosted run.** The Actions tab, the run graph, the Slack
  card and the Settings pages are always tagged `illustration`; log text inside them is real and
  comes from `runner/` or `laptop/62`. Never say "on GitHub, this printed …".
- Never show `laptop/capture-only/12-git-push-sandbox-proxy.txt` or say anything about the sandbox's
  proxy; the refused push is described as GitHub's "permission denied".
- Never quote the stand-in runners' timings, or the act artifact URL line (`62:404`); durations come
  only from the screenshot transcription.
- Never read a full 40-character SHA aloud or show it uncropped beside a narration of it; 7
  characters on screen.
- Never claim anyone used `--no-verify` to land the messy `utils.py` (the history shows it was put
  back on purpose, `91eb786`).
- Never say pre-commit runs on the server, or that Actions refuses a push.
- Never put a webhook URL in a code panel except the placeholder; never show a secret's value other
  than `***`.
- `act` is an extra witness, not a step the viewer needs.

## Notes for script and scene authors

- **Shared code** (`scenes/common.py`, start from L09's and L18's):
  - tracker factories `tracker_p5`, `tracker_p6` with the step lists above, and an `extra` caption
    variant "Part 4 · L09";
  - the prompt `P_LAPTOP = "student@laptop:~/cheese-app-ci-cd$"`, terminal title `laptop`;
  - tags `your_turn`, `extra_tag`, `illustration_tag`, `expected_tag`, `recorded_tag`, `cost_tag`
    (GOLD), `standin_tag` ("live · stand-in runner"), `lecture_ref`;
  - helpers `run_log(job_name, step_name, capture_path, pick=…)` (the job-log panel, exit badge),
    `run_graph(results: dict, layout="github")` (six nodes, `illustration`), `readme_panel(a, b)`
    (README lines with numbers), `pipeline_strip(current)` (V2's thin strip);
  - set-piece classes `HookChain` (V1), `CiLoop` + `PipelineStrip` (V2), `TriggerLanes` (V3),
    `JobGraph` (V4), `ImageSuitcase` (V5), `ExitGates` (V6), `SystemTestRig` (V7), `SlackRoute`
    (V8). A helper never reuses a scene class name from `video.yaml`.
- **The illustration framing is load-bearing.** Said once in S06/S07; afterwards every log line is
  simply "the log", and every GitHub page carries its tag.
- **Long outputs**: `run1/build/03` (657 lines: first 3 build steps, `…`, the last 5), `laptop/30`
  (first and last lines), `laptop/62` (only the verdict lines and the three cited lines),
  `run1/unit-tests/05` (first line, `…`, the `PermissionError` line, the `11 passed` line).
- **Emoji in captures** (`💥 💔 💥`, `✅`, `❌`, `✨ 🍰 ✨`): render with the toolkit's emoji-safe font
  path or replace with a GREY glyph box of the same width; never drop the surrounding text.
