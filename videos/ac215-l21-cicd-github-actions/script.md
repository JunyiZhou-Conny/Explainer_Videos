# AC215 · Lecture 21 — CI/CD with GitHub Actions II: one push, six fresh machines — narration script & visual plan (v2, review merge, 2026-11-06)

Audience: an AC215 student who has done L1–L20, in particular Docker images and containers,
`-p HOST:CONTAINER`, `docker save`/`load` (L2–L4) and **L09**: this same repo's Parts 1–4 (the
FastAPI toy with `/`, `/health`, `/euclidean_distance/`; Black vs Flake8 at 120 columns; 11 unit,
10 integration and 5 system tests inside the image; the silent `skipif`; `pre-commit install` with
its seven hygiene hooks + Black + Flake8). They have seen Lecture 21. They watch with a fresh clone
of `dlops-io/cheese-app-ci-cd` open, Docker running, a GitHub account and a repository of their own
(a fork or a new repo), pausing to run each step. **No GCP, no keys, no cloud bill**; Actions minutes
are free on public repos (GOLD tags where minutes and storage count on private ones).

Goal (BRIEF "Audience and goal"): after the video they can explain why local hooks are not a team
guarantee and where the lecture's server-side ideas sit on GitHub.com (Actions reports after the
push; branch protection refuses); read `ci.yml` as event → workflow → jobs → steps and say when it
runs; push the repo to a repository of their own and find every job's log; explain why the image is
built once and carried as an artifact, and predict the error when a job forgets `docker load`; read
the job graph (`needs`, fan-out, fan-in, `if: always()`) and explain why the run is red while Test
Summary says `✅ All tests passed!`; tell a blocking step from an advisory one; turn the first red
run green with `pre-commit run --all-files`, and say which local checks CI repeats and which it does
not; set up the Slack secret correctly and know why the failure message never arrives as written;
protect `main` with the right check names and break a test that pytest actually collects.

Sources of truth: `BRIEF.md` (design, binding), `digest.md` (tutorial digest), `SLIDES.md`
(lecture-slide digest, binding next to the digest: docs/AC215_SERIES.md rule 9), `assets/` (see
`ASSETS.md`). Where the digest or the slides and the captures disagree, the captures win, and the
video says so kindly. The README is `dlops-io/cheese-app-ci-cd` @ `b8458ff` (main, the only branch,
still the head on 2026-11-06: `laptop/01`), section **Part 5: GitHub Actions (Remote CI)**
(README.md:277–365), then the optional **Part 6: Branch Protection** (369–397). Parts 1–4 were
followed in L09 (`videos/ac215-l09-ci-testing/`): this video refers back and never redoes them.
Nothing in a terminal or log panel is typed by hand: every output line below names its capture file
and line numbers.

Conventions
- `SAY:` lines are spoken verbatim by the TTS voice (one `voiceover` block each, 1–3 sentences, at
  most about 60 words) and become the subtitles. Plain spoken English: no backticks, no markdown, no
  raw symbols (`/`, `=`, `%`, `&`, `$`, `→`, `_`, `!`); commands, flags and paths are on screen and
  said in words ("git add dot", "git commit, dash m, Add CI pipeline", "pre-commit run, all files",
  "git commit, no verify, dash m, quick fix", "docker load, dash i, the tar", "curl, dash f",
  "network host", "runs on, ubuntu latest", "if always", "continue on error, true"). File names are
  said "C I dot yaml", "utils dot py", "service dot py" (lexicon), "dot github, workflows", "dot git,
  hooks". The commit id `github.sha` is said "the commit ID" (never "SHA", never a hex string);
  `$GITHUB_OUTPUT` "GitHub output"; `SLACK_WEBHOOK_URL` "Slack webhook URL"; job ids by their names
  ("the lint and format job", "the unit tests job"); `def broken` "def broken".
- Every spoken sentence starts with a capital letter or a digit (`explainer.voice.split_sentences`
  splits only there; the same split drives TTS gaps, subtitle cues and the one-to-one Chinese
  alignment). No sentence opens with a lower-case command, tool or file name ("Because pytest …",
  "Then pre-commit …", "Git add dot …", "Docker save …"). No `'s` after a digit or a word with a
  lexicon entry or candidate (pytest, FastAPI, Flake8, pre-commit, Buildx, uvicorn): "the FastAPI
  test client", never "FastAPI's". No bare "a" right before such a word. No homographs: never
  "read", "live", "lives", "close", "lead", "tear", "minute" (singular), "content", "record"
  ("ran right here", "go through the log", "the loop comes full circle"); "minutes" only after a
  number. No spoken decimals (the demo's 7.0710678… is "about 7"). Numbers are digits; never a "!"
  after a digit. Tool versions sit on screen with the chip "at the time of recording" and are not
  spoken. American spelling on screen and in SAY ("color", "gray"); colour constants stay GREY etc.
  The main clause comes first, so the Chinese subtitles keep English clause order.
- `SHOW:` lines describe what is on screen during that `SAY:` line, and what moves. Something moves
  about every 4 s except under a ponder timer; at most 3 visual groups at once; every scene ends on
  an empty frame. Text ≥ 20 pt inside the safe frame.
- `PONDER(n s, "question")`: after that SAY block, `pause_and_ponder(self, "question", seconds=n)`
  (silent YELLOW timer; the card is removed at the start of the next block). The SAY before the card
  speaks the question; the next SAY gives the answer. Nothing during the timer shows the answer.
  Five in the video, BRIEF's table, Conny's 2026-10-21 density decision: P1 S04, P2 S07, P3 S08,
  P4 S11, P5 S13, all 8 s; the cards carry no number.
- `TERM(laptop/NN: lines)`: a laptop terminal beat, full width (12.6 units, the house `term()`),
  title `laptop`, prompt `student@laptop:~/cheese-app-ci-cd$` (constructed; the captures hold only
  the command). The scene types the command written just before it in the SHOW line (in backticks,
  exactly as the README spells it; extras exactly as the capture's line 1 spells it, folding with
  ` \`), then prints the listed **file** lines of `assets/terminal/laptop/NN-*.txt`. Line 1 is the
  `$ …` command: typed, never printed; `[exit N]` is never printed. Inside the list: `…` = print one
  `…` line; `wrap` = fold long lines (`Terminal.print(…, wrap=True)`); `→ (no output)` = the prompt
  simply returns; `crop7` = every 40-character id on that line is cut to 7 characters + `…`. Blank
  output lines are dropped. When a picture needs the frame, the terminal shrinks to a 3-row strip
  along the bottom (the last command and its key line); a full terminal and a picture never share
  the frame.
- `LOG(runX/<job>/NN: lines)`: a **job-log panel** (`run_log(job_name, step_name, capture, pick=…)`)
  quoting `assets/terminal/runner/runX/<job>/NN-*.txt`. Title "Job name › Step name" (the names from
  `ci.yml`, e.g. "Lint and Format Check › Run Black formatter check"); the capture's `$` line (and
  its `> ` continuation lines) becomes the step's heading in GREY monospace, never typed
  character by character; `[exit N]` becomes a small GREY badge "exit N" on the panel edge (RED
  outline when N ≠ 0), never text; GREY tag `live · stand-in runner`, bottom right. Every
  `cheese-app-api:<40 hex>` in a log is cropped to `cheese-app-api:b8458ff…` (7 characters).
  Container ids, timestamps and the client addresses `172.18.0.1:…` in server logs are cropped.
- `STEPS(runX/<job>: lines)`: the job's step list as the run page lists it, from that job's
  `00-steps.txt` (line 1, the header with the full commit id, is never shown): one row per step
  with a GREEN ✓ (`success`), RED ✗ (`failure`) or GREY dashed ⊘ (`skipped`), the step name WHITE;
  the parenthesised note of a row (e.g. `(continue-on-error: the job stays green)`) as a small GREY
  chip. Tagged `illustration · from our live runs`.
- `GRAPH(runX)`: the run graph (`run_graph(results, layout="github")`, V4): six nodes in GitHub's
  layout (build → four → summary), each coloured from `runner/runX/results.txt` (GREEN ✓, RED ✗,
  YELLOW while running, GREY before), a run badge top-left (RED "failure" / GREEN "success"), tag
  `illustration · colors from our live runs`. `RECORDED(screenshot)`: the README screenshot's
  transcription (`expected/readme-screenshot-run-graph.txt`), re-drawn small (six GREEN nodes with
  their times 54s/22s/18s/20s/39s/4s), tag `recorded · README screenshot` (the image is never
  copied).
- `ACT(lines)`: lines of `laptop/62-act-push.txt` with the ANSI codes stripped, printed in a
  laptop terminal strip after typing line 1 of `62` (folds); only the cited lines, each on its own row
  with `…` between non-adjacent ones. Tag `extra` on the typed line.
- `CODE(path: a–b)`: `code_panel(...)` quoting `assets/source/cheese-app-ci-cd/path` with the real
  line numbers, header `path · lines a–b`; at most 12 lines on screen at once (longer ranges are
  given as two panels, the second replacing the first by a Transform). `history/<file>` =
  `assets/source/cheese-app-ci-cd-history/<file>`, header `c3b227f · service.py · lines a–b` (or
  `199abd9 → 1a5e363 · ci.yml (diff)`). `README(a–b)`: a GREY README card, header
  `README.md · lines a–b`, markdown stripped, list markers kept. A README card is on screen for its
  block only (and for a later block only where the SHOW puts an `erratum` chip on it): on the next
  block it shrinks into the tracker's caption (Transform), and the code panel takes its place.
- `TRACKER P5 n` / `TRACKER P6 n`: the `ReadmeTracker`, top-left, at that step:
  - P5 = "README › Part 5: GitHub Actions (Remote CI)" (README.md:277–365), 8 steps: 1 Pipeline
    file · 2 Six jobs · 3 Key concepts · 4 git add · 5 git commit · 6 git push · 7 Actions tab ·
    8 Read results. (Step 1 = 279–283, 2 = 285–330, 3 = 332–342, 4–6 = 346–348, 7 = 351–357,
    8 = 359–365 and every job log after it.)
  - P6 = "README › Part 6: Branch Protection (Optional)" (369–397), 6 steps: 1 Add rule · 2 Pick
    checks · 3 New branch · 4 Break tests · 5 Commit, push · 6 Open PR.
  `TRACKER P5 n · extra` = same step, caption " · extra" while a command the README does not have is
  on screen; `TRACKER P5 8 · Part 4 · L09` = caption "Part 4 · L09" while the fix (README Part 4)
  is on screen. S01, S02 and S16 have no tracker; S13 and S14 show `TRACKER P5 8 · extra` (the
  README has neither `--no-verify` nor Slack).
- `STRIP <box>`: V2's thin pipeline strip (slide 26's five boxes `Commit → Build Container → Lint
  and Format → Test → Summary`, WHITE outlines) under the tracker in every Part 2 scene except S16;
  the named box fills YELLOW.
- `LECTURE 21 · a–b` in a SHOW line: from that block on, the GREY `lecture_ref(21, "a–b")` tag
  (`explainer.devops`) sits top right ("Lecture 21 · slides a–b"; "slide" for one) **only while that
  slide's picture or idea is on screen**; `LECTURE off` removes it. Slide numbers are the PDF pages
  of `SLIDES.md`, never the footers. Every lecture picture is our own redrawing in series colors with
  the slide's structure and terms: no slide image, meme, logo, QR code or screenshot; the lecture's
  pastel boxes and red loop are not copied.
- `(extra)` after a command: not in the README. A small GREY tag `extra` sits beside the typed line,
  and the SAY says "extra" the first time each kind appears.
- `▶ your turn`: a YELLOW tag beside the command at a real checkpoint (`git push` in S06, `pre-commit
  run --all-files` and `git push` in S12, the PR in S15); the SAY of that block says "pause". The
  video doesn't wait: the viewer pauses.
- Tags (GREY unless said): `illustration` on every GitHub page (Actions tab, run graph, step lists,
  Settings → Secrets, Settings → Branches), the Slack chat card and the lecture's wish-list card;
  `recorded · README screenshot` on the screenshot transcription and its timings; `live · stand-in
  runner` on every job log; `erratum` on every README or slide slip (the SAY says "a small slip",
  "a small gap" or "a kind note", never "erratum"); `at the time of recording` beside versions on
  first show; GOLD `cost_tag(text)`: S04 (one run per spark), S05 ("about 6 billed minutes ·
  private repos"), S08 ("artifact · about 176 MB · 1 day"), S15 ("private repo: paid plan"). No
  price anywhere.
- Spelling on screen and in subtitles: American.

Colours (BRIEF "Colours", fixed for the whole video)

| meaning | colour |
| --- | --- |
| the laptop: your clone, your terminal, the **local** pre-commit hooks, slide 14's chain | GREY |
| GitHub: your repository, the Actions tab, every GitHub-hosted runner (one `ubuntu-latest` VM per job), the artifact store, the secrets vault | BLUE |
| the image `cheese-app-api:<sha>`, the tar "suitcase", the containers (`api-server`, the test container) | TEAL |
| shared, not yours: the course's repo `dlops-io/cheese-app-ci-cd` (your `origin` until you change it), Docker Hub, port 9000 on the runner | ORANGE |
| what the project owns and pins: `ci.yml`, `.pre-commit-config.yaml`, `pyproject.toml`; a ✓ / `success` / `11 passed`; your branch `main` | GREEN |
| tools: GitHub Actions, Docker, Buildx, Black, Flake8, pytest, pre-commit, act, the Slack action | PURPLE |
| errors and "don't": ✗ / `failure`, exit codes ≠ 0, `would reformat`, `PermissionError`, `pull access denied`, `--no-verify`'s bypass, a key in the repo | RED |
| your turn, the README tracker, the strip's current box, a run in progress (GitHub's yellow dot), the ponder timer | YELLOW |
| money: Actions minutes on private repos, artifact storage, protected branches on private repos | GOLD |
| events and routes: push and PR arrows, the webhook POST, `localhost:9000` arrows, `$GITHUB_OUTPUT` notes, `needs.<job>.result` tokens | PINK |
| *skipped* (a step or job that never ran) | GREY, dashed |
| the past and the future (L09's hooks, L23's CD, Milestone 5's retraining) | GREY, dashed |

GitHub is a BLUE rounded box labelled "GitHub", Slack a GREY chat window labelled "#build-alerts":
no GitHub, GitLab, Playwright, Slack or Docker logos anywhere.

Running example
- **The laptop**: a fresh `docker:29.8.2-dind` container stands in for a laptop with Docker Desktop
  (`laptop/00`: Docker 29.8.2, git 2.54.0), user `student`, terminal title `laptop`, prompt
  `student@laptop:~/cheese-app-ci-cd$` (a fresh clone, S06; L09's folder has the Black fix committed). A GREY chip, once (S06): "your prompt
  shows your own user"; said once.
- **Your repository**: on the viewer's machine `https://github.com/<you>/cheese-app-ci-cd` (a fork or
  a new repo). Here a bare repo `~/github-standin/student/cheese-app-ci-cd.git` stands in
  (`laptop/20`, `21`): said once in S06, shown as `extra`; afterwards the narration says "your
  repository".
- **The runs**: **run 1** = the push of the untouched clone, `b8458ff` (`laptop/22`); **run 2** =
  after the Black fix, `2289d89` here ("your commit ID will differ"; `laptop/37`); **run 3** = after
  `git commit --no-verify -m "quick fix"`, `2892b1b` (`laptop/45`); **the demo run** = the in-class
  demo commit `c3b227f` ("demo class 1", 2025-11-13), from the course repo's history, never pushed;
  **no-load** = one check job without its `docker load` step (the ponder).
- **The illustration framing** (load-bearing, said once in S07 and once lightly in S01): every job of
  `ci.yml` ran right here, each on a brand-new machine with an empty Docker (`runner/`), and `act`
  ran the whole file a second way (`laptop/62`); both gave the same verdict. GitHub pages are
  drawings built from the workflow file, tagged `illustration`; every log line in them is real.
  Never "on GitHub, this printed …". The sandbox's refused push (`laptop/capture-only/12`) is never
  shown or mentioned.
- **Placeholders**: the webhook URL only as `https://hooks.slack.com/services/<your-webhook-path>`;
  a secret's value only as `***`; `<you>` for the GitHub user. No real-looking token, URL, IP or id.
- **Versions** (on screen with "at the time of recording", never spoken): Docker 29.8.2, git
  2.54.0, pre-commit 4.7.0 (config: Black 24.1.1, Flake8 7.0.0), act 0.2.97; in the image (unpinned):
  Python 3.11.18, black 26.10.1, flake8 7.5.0, pytest 9.2.0, pytest-cov 7.1.0.
- **Never quoted**: the stand-in runners' timings; the act artifact URL line (`62:404`); the
  artifact's exact bytes (said "about 176 megabytes"); a full 40-character id.

Length and parts: narration target 3,900–4,300 words (`python -m explainer.script`, which counts SAY
words; its minute figure assumes 155 wpm and is ignored). At Kokoro af_heart speed 0.9 (≈174 wpm)
that is ≈24.5 min of narration, ≈31–33 min with typing, run logs, graph drawings and five ponder
timers. Per-scene counts below.
Part 1 = S01–S07 (read it, push it, watch it; ends on run 1's verdict, the hook reproduced on the
viewer's own push). Part 2 = S08–S16 (the run job by job, then around the loop; ends on the last
test-yourself card). The cut is the README's own seam between "Watch GitHub Actions" and reading
each job's log. Each part ends on an empty frame.

| scene | words (BRIEF · band) | scene | words (BRIEF · band) |
| --- | --- | --- | --- |
| S01 Hook | 242 (220 · 187–253) | S08 BuildOnce | 318 (340 · 289–391) |
| S02 LocalHooks | 285 (300 · 255–345) | S09 ExitCodes | 225 (260 · 221–299) |
| S03 CiPipeline | 272 (290 · 247–334) | S10 TestJobs | 294 (300 · 255–345) |
| S04 WhenItRuns | 240 (230 · 196–265) | S11 TheSummary | 266 (260 · 221–299) |
| S05 SixJobs | 262 (290 · 247–334) | S12 RedToGreen | 213 (240 · 204–276) |
| S06 PushIt | 297 (270 · 230–311) | S13 NoVerify | 315 (290 · 247–334) |
| S07 WatchTheRun | 274 (250 · 213–288) | S14 SlackBell | 287 (270 · 230–311) |
| | | S15 ProtectMain | 253 (220 · 187–253) |
| | | S16 Recap | 249 (220 · 187–253) |
| **part 1** | **1,872** (1,850) | **part 2** | **2,420** (2,400) |

Total **4,292** words after the review merge (`build/review_merge_log.md`), every scene inside its
band. Tight: the total sits 8 under the series ceiling (4,300); S15 (253 of 253), S16 (249 of 253),
S09 (225, 4 above its floor) and S07 (274 of 288): any later addition names its cut in the same scene
(BRIEF's order: S05's Gantt beat, S08's Buildx erratum, S16's ML beat; never a
README step). Re-run the counter after any edit.

Notes for scene authors
- Shared code (`scenes/common.py`, started from L09's and L18's): `tracker_p5(k, extra=None)`,
  `tracker_p6(k)` with the step lists above and the caption variants " · extra" and " · Part 4 ·
  L09"; `P_LAPTOP = "student@laptop:~/cheese-app-ci-cd$"`; tags `your_turn`, `extra_tag`,
  `illustration_tag`, `recorded_tag`, `erratum_tag`, `cost_tag` (GOLD), `standin_tag` ("live ·
  stand-in runner"), `lecture_ref`; helpers `run_log(...)`, `steps_list(...)`, `run_graph(...)`,
  `readme_panel(a, b)`, `pipeline_strip(current)`; set pieces `HookChain` (V1), `CiLoop` +
  `PipelineStrip` (V2), `TriggerLanes` (V3), `JobGraph` (V4), `ImageSuitcase` (V5), `ExitGates`
  (V6), `SystemTestRig` (V7), `SlackRoute` (V8). A helper never reuses a scene class name.
- Capture line numbers are *file* lines (line 1 = the `$` command); `Capture.pick()` indexes the
  output body, so pick index = file line − 1. Assert the picked text of every highlighted line.
- Long outputs: `run1/build/03` (657 lines: lines 2, 4–5, `…`, 653, 656); `laptop/30` (line 2, `…`,
  line 39 wrapped); `laptop/62` (only the cited lines); `run1/unit-tests/05` (line 3, `…`, 75, 77);
  `laptop/32` (lines 15–31, the `[INFO]`/`[WARNING]` lines 2–14 collapsed into one `…`).
- Emoji in captures (`💥 💔 💥`, `✅`, `❌`, `✨ 🍰 ✨`, act's `🏁`, the Slack payload headers): the house mono font
  drops emoji silently and the toolkit has no emoji font path. Copy L13's `_emoji_guard` /
  `strip_emoji` (`videos/ac215-l13-exam/scenes/common.py`) into `common.py`, so any glyph the mono
  font drops fails loudly. Draw ✅ as `devops.check_mark` (GREEN) and ❌ as `devops.cross_mark` (RED)
  in a one-cell box at the emoji's position; 💥 💔 💥, ✨ 🍰 ✨ and 🏁 as GREY one-cell glyph boxes of the
  same width. Never drop the surrounding text.
- **BRIEF corrections found while scripting** (captures win):
  - `run1/integration-tests/04:28` reads `10 passed, 1 warning`, not just "10 passed" (S10 shows the
    line as is; the SAY says "10 passed").
  - On a **fork** the pinned commit is already on GitHub, so the README's `git push` prints
    `Everything up-to-date` and no run 1 starts (digest G20; there is no `workflow_dispatch` in
    `ci.yml`). S06 says so in one sentence: for fork users the first run is run 2 (S12), which is
    green; the new-empty-repo route gives run 1 exactly as shown. The BRIEF's "if you already pushed
    this commit" sentence becomes this one.
  - BRIEF S05/S10 cite `ci.yml` 146–169 and 15–38 etc. as one panel; they are longer than 12 lines,
    so each is split in two panels (see the scenes).
  - `.pre-commit-config.yaml` Black/Flake8 sit at 29–35 and 37–44 (two panels; BRIEF 29–44).
- Lexicon (merged 2026-11-06, `explainer/lexicon.yaml` under `# AC215 L21`): `Buildx` (capitalised;
  only the lower-case `buildx` existed, so the voice said "bildks") and `under uses` (the YAML key, said
  as the verb "yoo-ziz"). Checked with `KokoroBackend.phonemize` and fine without an entry: act,
  ubuntu, Flake8, pre-commit / pre-push / pre-receive / post-receive (never key these: "A pre-commit
  hook" would leave "A" alone, read as the letter), webhook(s), Jenkins, C I dot yaml, 125, 176, def
  broken, cheese app API, utils dot py, service dot py, localhost 9000.
- Subtitle display for the i18n stage (`en_display`): git add dot → `git add .`; git commit, dash m,
  Add CI pipeline → `git commit -m "Add CI pipeline"`; git push → `git push`; git remote, dash v →
  `git remote -v`; git remote set-url origin → `git remote set-url origin`; pre-commit run, all
  files → `pre-commit run --all-files`; pre-commit install → `pre-commit install`; git commit, no
  verify, dash m, quick fix → `git commit --no-verify -m "quick fix"`; git status, short →
  `git status --short`; docker load, dash i → `docker load -i`; docker save → `docker save`; curl,
  dash f → `curl -f`; network host → `--network host`; runs on, ubuntu latest → `runs-on:
  ubuntu-latest`; if always → `if: always()`; continue on error → `continue-on-error`; needs →
  `needs`; C I dot yaml → `ci.yml`; dot github, workflows → `.github/workflows`; dot git, hooks →
  `.git/hooks`; utils dot py / service dot py → the file names; GitHub output → `$GITHUB_OUTPUT`;
  Slack webhook URL → `SLACK_WEBHOOK_URL`; localhost 9000 → `localhost:9000`; feature, test
  protection → `feature/test-protection`; feature login → `feature/login`; def broken, assert False
  → `def broken(): assert False`; test broken → `test_broken`; actions checkout → `actions/checkout`;
  cheese app API → `cheese-app-api`; cheese app API, colon, the commit ID → `cheese-app-api:<commit
  ID>`; docker images → `docker images`; docker ps → `docker ps`; Git diff → `git diff`; Git status
  → `git status` (S06) / `git status --short` (S13); git restore → `git restore`; git checkout (S15
  last block) → `git checkout --`; git checkout, dash b → `git checkout -b`; git push origin feature,
  test protection → `git push origin feature/test-protection`; Intentionally break tests →
  `"Intentionally break tests"`; Pip install pre-commit → `pip install pre-commit`; the api folder →
  `api/`; files under src → `src/`; enabled, true or false → `enabled=true` / `enabled=false`; three
  stars → `***`; the load docker image step → the "Load Docker image" step; the run unit tests step →
  "Run unit tests"; Check test results → "Check test results"; GitHub dot com → `GitHub.com`;
  Settings, Branches → `Settings → Branches`; Settings, Secrets and variables, Actions → `Settings →
  Secrets and variables → Actions`; the README's IDs → `lint-and-format, …`; test protection branch
  → `feature/test-protection` branch; Require a pull request before merging / Require status checks
  to pass → the checkbox labels in quotes. In zh all of these stay English (glossary rule). Metaphors for
  the zh glossary, rendered the same way every time: "the bell, not the gate" → 是铃，不是门;
  "suitcase" → 行李箱; "gate" (a step) → 关卡; "shunt" (continue-on-error) → 旁路; "token" → 结果令牌.
- Never: the instructor's name (`‹instructor›` if ever needed; slide 11's author and reply are never
  drawn); a slide image, meme or QR code; a logo; hand-typed output; a command spelled differently
  from the README; a real-looking key, token, webhook URL, IP or project id; a full 40-character id;
  "pre-commit runs on the server"; "Actions refuses a push"; "someone used --no-verify to land the
  messy utils.py" (it was put back on purpose, `91eb786`); the stand-in timings; an illustration
  presented as a real hosted run.

---

## S01 · Red run, green summary — `s01_hook.py` · `Hook`

SHOW: Black frame, no tracker. The picture first: GRAPH(run1) builds with every node GREY (tag
`illustration · colors from our live runs`). The Test Summary node expands (Transform) into a
job-log panel: LOG(run1/test-summary/01: 13–16), title "Test Summary › Check test results" (the
`$`/`>` heading lines 1–12 collapsed into one GREY heading row "Check test results"). The three
`success` words light GREEN one by one on "success", then line 16 `✅ All tests passed!` grows GREEN
(✅ drawn as `check_mark`). Tag `live · stand-in runner`. The log collapses back into its node, which
turns GREEN.
SAY: You push the course's own code, untouched, to a repository of your own. Soon after, one log says: unit tests, success. Integration tests, success. System tests, success. All tests passed.

SHOW: A laptop strip along the bottom prints act's last line ACT(750) `Error: Job 'Lint and Format
Check' failed` in RED (no typing in this scene; the strip's typed line is hidden), with a small GREY
tag `act · same file`. On the phrase, the graph's other nodes fill: Build and the three tests GREEN,
"Lint and Format Check" RED; the run badge flips RED on "failed".
SAY: And the same file, run end to end, ends like this: job Lint and Format Check failed. Five machines green, one red, and the whole run red. The pipeline says every test passed, and the pipeline failed. Both are true.

SHOW: The act strip fades; the graph dims except the RED lint node and the GREEN summary node, which
pulse together. A YELLOW question card drops between them: "Which machine said no, and why didn't the
summary hear it?" It stays pinned small, top right, until the end of the scene.
SAY: So which machine said no, and why didn't the summary hear it? By the end of part 1 you will see this on your own push. In part 2 we open every log.

SHOW: The graph fades. Left: a GREY laptop outline with three small gates (GREY dashed, chip
"lecture 9 · your hooks"); a GREEN commit dot passes them. A PINK arrow carries it right into a BLUE
rounded box "GitHub", where six small BLUE machine boxes light one after another.
SAY: In lecture 9 these checks ran on your laptop, before a commit. Today they move to GitHub, and they run on every push to main, on fresh machines that nobody owns.

SHOW: LECTURE 21 · 1, 4. Four WHITE-outlined labels appear in a row, one per phrase: "Remote Git
hooks", "GitHub webhooks", "Continuous integration", "Continuous deployment". Under them a GREY
caption: "slide by slide · README Part 5 step by step".
SAY: Lecture 21 has four sections: remote Git hooks, GitHub webhooks, continuous integration, and continuous deployment. We follow it slide by slide, and the README Part 5 step by step.

SHOW: LECTURE off. The labels fade. Four GREY chips line up, one per phrase: "a fresh clone (L09's has
the fix committed)", "Docker running", "a GitHub account + a repository of your own", and a GREEN chip
"no cloud · no keys · public repo: no bill".
SAY: To follow along, you need a fresh clone of the course's repository, Docker running, a GitHub account, and a repository of your own. No cloud and no keys, and on a public repository, no bill.

SHOW: The chips fade. Four samples, each appearing on its phrase while the previous one dims to 30 %
(only the one being named is bright): top-left a YELLOW `ReadmeTracker` ("README › Part 5: GitHub
Actions (Remote CI) · step 1 of 8"); in the middle a code panel header `.github/workflows/ci.yml ·
lines 7–11`; a sample `git push` with a YELLOW `▶ your turn`; at the bottom right a GREY tag
`illustration` beside a tiny run graph. Everything fades; empty frame.
SAY: The tracker names the README step, code panels name their file and lines, and a yellow tag, your turn, means pause and run it. The runs you will see ran right here on fresh machines; the GitHub pages are drawings, and they say so.

---

## S02 · Hooks stay on your laptop — `s02_hooks.py` · `LocalHooks`

SHOW: No tracker. LECTURE 21 · 2–3. **V1 `HookChain`** builds left: a GREY laptop frame labelled
"Git local hooks". Two small GREY tags fall onto its edge as they are named: `pre-commit` (on the
commit arrow inside the laptop) and `pre-push` (on the laptop's outer door). A GREY dashed chip
"lecture 9 · README Part 4" sits under the frame.
SAY: The lecture opens with a recap: local Git hooks. A pre-commit hook runs on your laptop, before the commit even exists. A pre-push hook runs before your commits leave. In lecture 9 you installed this repo's set.

SHOW: Inside the frame, three boxes appear in a row joined by arrows: `hygiene ×7` → `Black` →
`Flake8` (PURPLE outlines). Beside the frame, CODE(.pre-commit-config.yaml: 29–35) then a Transform to
CODE(.pre-commit-config.yaml: 37–44): line 30 `rev: 24.1.1` with the chip "at the time of
recording", lines 34 and 43 (the 120 flags) YELLOW, lines 35 and 44 `files: ^src/.*\.py$` YELLOW. On
"ends with tests" a fourth box "Tests" slides in GREY dashed at the end of the chain and is struck
RED; a GREY label under it: "CI runs these".
SAY: Here is that chain, with this repo's boxes: seven hygiene checks, then Black, then Flake8, both at 120 columns, and only on files under src. The lecture's chain ends with tests. This repo's hooks run none: it leaves the tests to CI.

SHOW: The code panel leaves. A GREEN commit dot passes the three gates of the laptop (each flashes
GREEN). A second GREY laptop appears below it with an empty frame and the GREY label "no pre-commit
install"; its dot goes straight through.
SAY: The lecture's catch: hooks run only on a machine where someone ran pre-commit install. A teammate's laptop without them sends its commit through unchecked. So the checks depend on the laptop.

SHOW: LECTURE 21 · 5–6. The laptop group shrinks to a small GREY icon at the left edge. Right: a BLUE
server box "shared repository" with a door. In front of the door a GREY gate labelled `pre-receive`;
a dot arrives, the gate shuts, the dot bounces back (RED flash). On "one branch at a time" a GREY chip
"update: per branch" lands on the gate (no separate lanes).
SAY: That's where remote hooks come in: they run on the server that receives the push. A pre-receive hook runs before the push is accepted, so it can refuse it. The update hook does the same, one branch at a time.

SHOW: Behind the door, inside the server, a GREY bell labelled `post-receive`. A dot enters through
the open door, lands, and only then does the bell ring (three small PINK arcs) with three GREY chips:
"integration tests", "notifications", "clean-up".
SAY: A post-receive hook runs after the code is in, for integration tests, notifications and clean-up. It can report, but it can no longer say no.

SHOW: The bell's three chips fade first. The server box gets the label "GitHub.com". The `pre-receive` gate turns GREY dashed with a
small GREY chip "your own scripts: not on GitHub.com". Two new pieces slide in: a BLUE "Actions"
badge that docks on the bell, and a GREEN "branch protection" gate that docks in front of the door.
A GREY caption writes under the server: "Actions on a push is the bell, not the gate." It stays for
the rest of the scene.
SAY: One honest note: GitHub dot com doesn't run your own pre-receive scripts. It gives you two pieces instead: Actions, which runs after the push, and branch protection, which can say no.

SHOW: LECTURE 21 · 7. A small GREY chat window "#build-alerts" outside the server, and a dashed PINK
arrow toward it with a "?" on it.
SAY: And hooks act only inside Git. To tell a chat what happened, the lecture reaches for webhooks.

SHOW: LECTURE 21 · 14–16. The server and chat clear; the laptop icon grows back. V1's move: the first laptop's chain (`hygiene
×7` → `Black` → `Flake8`) flashes GREY as a dot passes; then `git push`: the dot flies PINK out of
the laptop into a BLUE frame "Shared Repository", where there are no gates at all; it lands and
nothing checks it (an empty GREY outline where gates would be).
SAY: Now the lecture's motivation, in three slides. On your laptop, the checks fire on every commit. Then you push, and on the shared repository, nothing runs them at all.

SHOW: The BLUE frame fills with slide 16's three boxes, one per phrase: `Build Container` (TEAL
inside), `Check Code`, `Test Summary`, joined by arrows. The second laptop's dot arrives too and
passes through the same three boxes. A GREEN caption: "continuous integration". Fade; empty frame.
SAY: So the checks move to the server: build a container, check the code, summarize the tests. Same idea, new home, for every push to main from every laptop. That move is continuous integration.

---

## S03 · The CI loop and the workflow file — `s03_pipeline.py` · `CiPipeline`

SHOW: No tracker yet. LECTURE 21 · 22. The picture first: a GREEN commit dot lands on a GREY code
box; three `>_` script glyphs light in sequence by themselves ("run automatically whenever the code
changes"); on the second clause another dot lands and they run again. Then four GREEN chips dock
onto the glyph row, one per phrase: "integrate continuously", "test automatically", "enforce coding
standards", "static code analysis".
SAY: The lecture defines continuous integration as a series of scripts that run automatically whenever the code changes. They integrate changes continuously, test automatically, enforce coding standards, and run static analysis.

SHOW: LECTURE 21 · 17. The four chips fade. Three small icons fly out of the glyph row, one per
phrase: a short arrow ("faster releases"), a `check_mark` ("better code"), a `person_icon` pair
("easier coordination"); then a GREY dashed chip "+ machine learning: S16" pulses once.
SAY: In ordinary software, that buys faster releases, better code, and easier teamwork. Machine learning adds a twist; we come back to it at the end.

SHOW: LECTURE 21 · 21. The chips clear. **V2 `CiLoop`**, drawn open: bottom left "Developers"; a
PINK arrow "Commits" up into a top row `Codebase` → `Build` → `Test` (WHITE outlines, inside a
GREY dashed frame); two dashed PINK lines from `Build` and `Test` down into a GREY vertical bar
"Notifications" beside "Developers". On "still a question mark", a YELLOW "?" sits on the return
lines.
SAY: Slide 21 draws it as a loop. Developers commit to the codebase; the codebase is built, then tested; and notifications flow back to the developers. For now, the way back is a question mark.

SHOW: LECTURE 21 · 25–27. The loop shrinks to the top-left corner. **V2 `PipelineStrip`** at full
size: five WHITE-outlined boxes `Commit → Build Container → Lint and Format → Test → Summary`; under
each, slide 27's one-line purpose writes on as it is named: "a push triggers it", "one image, same
environment", "Black + Flake8", "unit · integration · system", "pass / fail to the developers". A
GREY chip "built with GitHub Actions".
SAY: The course's pipeline has five stages. A commit triggers it, the container is built, Black and Flake8 check the code, the tests run, and a summary reports pass or fail.

SHOW: LECTURE off. The strip shrinks to a thin row and slides off the top. TRACKER P5 1 (tracker
appears: "README › Part 5: GitHub Actions (Remote CI)", 8 dots). README(277–283) card: the heading
and the lines 279 and 283; "Python 3.11 (same as production)" YELLOW; a GREY `erratum` chip beside
it: "no production yet · read: the same image you would deploy".
SAY: Now the README, Part 5: GitHub Actions, remote CI. It says all CI tests run inside Docker containers using Python 3.11, the same as production. This repo has no production yet: take it as the same image you would deploy.

SHOW: TRACKER P5 1 · extra. The card moves up; a full-width terminal `laptop` types
`ls -la .github/workflows/` (extra) → TERM(laptop/04: 2–5); line 5 `ci.yml` GREEN. A small tree
drawing beside it: the repo root folder (GREEN) → `.github` → `workflows` → `ci.yml`; a GREY dashed
ghost "my-project/subfolder/.github/workflows/" appears below with a RED ✗ "never runs"; under it a
GREY chip "fix: move to the root `.github/workflows/` + `defaults: run: working-directory:` · study
guide". (The terminal shrinks to a 3-row strip before the tree draws.)
SAY: This one isn't in the README, it's extra: list the workflows folder. One file, C I dot yaml, in dot github, workflows, at the root of the repository. GitHub looks only there; a workflow in a subfolder never runs.

SHOW: TRACKER P5 1. The terminal shrinks away. CODE(.github/workflows/ci.yml: 5–11): line 5 `name:
CI Pipeline` YELLOW on "a name", lines 7–11 (`on:`) PINK on "events". Then a Transform to
CODE(.github/workflows/ci.yml: 13–20): line 13 `jobs:` and line 15 `build:` YELLOW, line 17
`runs-on: ubuntu-latest` BLUE on "its own machine".
SAY: Open it. The file gives the workflow a name, CI Pipeline. Next comes the key called on, just the word on. It lists the events that start the workflow. Under jobs, each job gets its own machine, called a runner: runs on, ubuntu latest.

SHOW: **V4 `JobGraph`, S03 form**: the code panel transforms into the tree (its `on:` line becomes
the PINK root, `jobs:` becomes the column). Layout: top-left the PINK root "on: push · pull_request"
→ a WHITE "workflow: CI Pipeline"; below it the six job ids as a vertical column `build`,
`lint-and-format`, `unit-tests`, `integration-tests`, `system-tests`, `test-summary` (BLUE outlines);
only `build` opens to the right into its five steps (`ci.yml:19–38`), the other five jobs dim:
"Checkout code" and "Set up Docker Buildx"
and "Upload Docker image artifact" with a small PURPLE puzzle piece (`uses:`), "Build Docker image"
and "Save Docker image" with a `>_` glyph (`run:`). Each layer pulses on its word in "Event, workflow,
jobs, steps". Fade; empty frame.
SAY: Inside a job, steps run in order. A step is either a shell script, under run, or a reusable action, under uses, like actions checkout, which copies your repository onto the machine. Event, workflow, jobs, steps: that is the whole grammar.

---

## S04 · When does the pipeline wake up? — `s04_triggers.py` · `WhenItRuns`

SHOW: TRACKER P5 1. LECTURE 21 · 25. A GREY quote chip from the slide: "on every push or pull
request". Beside it CODE(.github/workflows/ci.yml: 7–11): lines 8–9 (`push: branches: [main,
develop]`) PINK, then lines 10–11 (`pull_request: branches: [main, develop]`) PINK; the slide chip
gets a small GREY "more precisely:" arrow pointing at the panel.
SAY: When does the pipeline wake up? The slide says on every push or pull request. The file is more precise: pushes to main or develop, and pull requests into main or develop.

SHOW: LECTURE off. The panel shrinks to the top right. **V3 `TriggerLanes`**: three horizontal lanes
`main` (GREEN), `develop`, `feature/login` (WHITE), each with commit dots. A push dot lands on
`main`: a PINK spark and a BLUE runner icon lights; the same on `develop`; a dot on `feature/login`:
no spark, the runner icon stays GREY. A GREY `erratum` chip near the panel's line 2 comment: "the
comment says main only · the triggers say main and develop".
SAY: Push to main, and a runner wakes up. Push to develop, the same. Push to a feature branch, and nothing happens: on any other branch, the pipeline waits for your pull request. A small note: the comment at the top of the file says main only; the triggers say main and develop.

SHOW: The lanes stay; `feature/login` gets three new GREY dots, one per beat. A dashed PINK arrow
"PR → main" waits, unlit, between `feature/login` and `main`.
PONDER(8 s, "You push three commits to feature/login.\nHow many CI runs start?\nThen you open a PR into main:\nhow many now?")
SAY: Quick test. You push three commits to feature login. How many runs start? Then you open a pull request into main. How many now?

SHOW: The card leaves. The three pushes: no sparks (GREY "0 runs" chip). The PR arrow lights PINK: one
spark, one BLUE runner icon ("1 run"); a fourth dot pushed to `feature/login` adds a second spark
("+1 per push while it's open").
SAY: None for the three pushes: the branch filter. One when the pull request opens, and one more for every later push while it stays open.

SHOW: LECTURE 21 · 23. Above `main`, a GREY dashed **ghost merge commit** appears where the two lanes
meet, labelled `github.sha`; the runner's arrow re-aims from the branch tip to the ghost. A GREY
caption: "each merge is tested".
SAY: And it doesn't test your branch tip. GitHub makes a temporary merge of your branch into main, and the commit ID the jobs see names that merge. What will land is what gets tested: each merge is tested, as the lecture says.

SHOW: LECTURE 21 · 24. A GOLD meter under the lanes ticks once per spark so far; three GREY chips
dock on it, one per phrase: "branch filter", "one shared build", "image kept 1 day". GOLD
`cost_tag("private repos: every run counts · public: free")`.
SAY: The lecture warns that integrating often costs compute. This file answers with a branch filter, one build shared by every job, and an image kept one day. On private repositories every run counts against your plan; public ones run free.

SHOW: LECTURE off. The lanes shrink. A small replay of S02's door: a dot passes the open door into the
BLUE server, lands; only then does the PINK spark fire and the bell ring. GREY caption from S02
returns: "Actions on a push is the bell, not the gate." Fade; empty frame.
SAY: And timing matters: the run starts after GitHub has accepted your push. It's the bell, not the gate: a red run doesn't undo the push.

---

## S05 · Six jobs, one graph — `s05_jobs.py` · `SixJobs`

SHOW: TRACKER P5 2. README(285–287) card: "The pipeline consists of 6 jobs that run in parallel
(except for dependencies)". Six chips appear in two rows, one per name, each with the job id (GREY,
small) above its `name:` from `ci.yml` (WHITE): `build` · Build Docker Image, `lint-and-format` ·
Lint and Format Check, `unit-tests` · Unit Tests, `integration-tests` · Integration Tests,
`system-tests` · System Tests, `test-summary` · Test Summary.
SAY: Next, the README: 6 jobs that run in parallel, except for dependencies. Each has an ID and a name: Build Docker Image, Lint and Format Check, Unit Tests, Integration Tests, System Tests, and Test Summary.

SHOW: The six names (WHITE) pulse YELLOW together; the ids dim. A GREY chip: "GitHub shows the
names · S15".
SAY: Remember the names: GitHub shows them, not the IDs, and we'll need them to protect main.

SHOW: LECTURE 21 · 26–27. The chips clear. Slide 26's row at full size (V2 strip): `Commit → Build
Container → Lint and Format → Test → Summary`. `Commit` lifts out and turns PINK: "the event, not a
job". `Build Container` slides to the left edge and gets the label `build`.
SAY: Start from the lecture's row of five. Commit drops out first: it's the event, not a job. Build Container stays on the left: it's the build job.

SHOW: **V4 `JobGraph`, S05 form.** `Lint and Format` and `Test` slide right into parallel lanes;
`Test` splits into three boxes `unit-tests`, `integration-tests`, `system-tests`. A narrow
CODE(.github/workflows/ci.yml) strip on the left shows one line at a time: line 44 `needs: build` →
one arrow build → lint draws; line 73 → build → unit; line 108 → build → integration; line 131 →
build → system. The four lanes light BLUE: "each on its own machine".
SAY: Now each needs line draws one arrow. Lint and format needs build. Unit tests, integration tests and system tests each need build too. So after the build, four jobs run side by side, each on its own machine.

SHOW: The code strip shows lines 175–176 (`needs: [unit-tests, integration-tests, system-tests]`,
`if: always()`); three arrows draw from the test boxes into `Summary` (now `test-summary`). Between
the lint box and the summary, a GREY dashed gap with a YELLOW "?" stays on screen. A GREY `erratum`
chip on the lecture's row ghost: "a straight row → a graph".
SAY: Test summary needs the three test jobs. Look closely: the lint job isn't on that list. The lecture lists the stages in order; on GitHub, four of them run side by side, and the summary listens only to the tests. Keep that gap in mind.

SHOW: LECTURE off. TRACKER P5 2 · extra. A laptop strip at the bottom types `act -l` (extra; chip
"act 0.2.97 · at the time of recording") → TERM(laptop/61: 3–9) (squeezed columns: Stage, Job ID,
Job name only). Above the graph, three GREY column labels appear: "stage 0", "stage 1", "stage 2".
SAY: An extra check, not in the README: a tool called act, which you don't need, takes the same file and lists the jobs in stages. Stage 0, build. Stage 1, the four checks. Stage 2, the summary.

SHOW: TRACKER P5 3. The strip leaves. README(332–342) as five chips, each flying to its place on the
graph as named: "Artifact Sharing" and "Unique Image Tags" → the build node (GREY "S08"); "Parallel
Execution" → the four lanes (pulse); "Conditional Execution" and "Network Modes" → the system-tests
node (GREY "S10").
SAY: Then the key concepts. Artifact sharing and unique image tags come with the build job; parallel execution, you just saw; conditional execution and network modes come with the system tests.

SHOW: Times from RECORDED(screenshot), tag `recorded · README screenshot`: each graph node stretches
sideways into its Gantt bar (Transform: node → bar, left edge at its start time), so the graph
becomes the timeline: build 54 s, then four bars starting together (22 / 18 / 20 / 39 s), then the
summary's 4 s; the critical path (build → system → summary) glows YELLOW and a WHITE ruler under it
reads "about 2 min on the clock". On "billed", a GOLD ruler slides in under it: six blocks, one per
job, each rounded **up** to a whole minute, summing to "about 6 billed minutes", with
`cost_tag("private repos · public: free · digest §2, not measured here")`. Fade; empty frame.
SAY: The README's screenshot gives the times: about 2 minutes on the clock, with four jobs side by side. On a private repository, each job is billed and rounded up separately: about 6 billed minutes.

---

## S06 · Push to a repo of your own — `s06_push.py` · `PushIt`

SHOW: TRACKER P5 4 · extra. Full-width terminal `laptop`, prompt `student@laptop:~$`. It types
`git clone https://github.com/dlops-io/cheese-app-ci-cd.git` (extra) → TERM(laptop/02: 2). Then
`cd cheese-app-ci-cd` (no output); the prompt changes to `student@laptop:~/cheese-app-ci-cd$`, and
the change is highlighted YELLOW. Then `git status` (extra) → TERM(laptop/14: 2–5), line 5
`nothing to commit, working tree clean` GREEN. GREY chip: "L09 folder in the way? clone into another
folder, or in it: git reset --hard b8458ff (drops L09's commit)".
SAY: Time to push. Start from a fresh clone, not your lecture 9 folder: that one has the Black fix committed, and your first run would come out green. Clone, change into the folder, and git status says the tree is clean.

SHOW: TRACKER P5 4 · extra. A GREY chip near the prompt "your prompt shows your own user". The
terminal types `git ls-remote https://github.com/dlops-io/cheese-app-ci-cd.git` (extra; folds) →
TERM(laptop/01: 3 crop7) (`b8458ff…  refs/heads/main`, GREEN); then `git log -3 --format='%h %ci %s'`
(extra) → TERM(laptop/03: 2–4); lines 2–3 ("demo class 1" twice) YELLOW, with a GREY chip "→ S11"
beside them.
SAY: Your prompt shows your own user. Two extra checks first: the pinned commit is still the head of main on the course's repository, and the last two commits are both called demo class 1. The second undid a bug planted in class; we'll run it later.

SHOW: TRACKER P5 4. A README(344–349) card, top right: the three commands. The terminal types
`git add .` → TERM(laptop/10: → (no output)). TRACKER P5 5. It types `git commit -m "Add CI
pipeline"` → TERM(laptop/11: 2–5); line 5 `nothing to commit, working tree clean` RED, a small RED
"exit 1" badge beside it.
SAY: Now the README block, Push to GitHub. Git add dot: no output. Then git commit, dash m, Add CI pipeline. And Git answers: nothing to commit, working tree clean.

SHOW: The terminal shrinks to a 3-row strip (last line `nothing to commit, working tree clean`). A
GREY `erratum` chip on the README card's line 347: "already committed in a clone or fork". In the
middle, a small tree drawing: `ci.yml` already sits GREEN inside the clone's history (a commit dot
labelled "already there").
SAY: A small slip, and a harmless one: in a clone or a fork, the pipeline is already committed, so there is nothing to add.

SHOW: TRACKER P5 6 · extra. The terminal grows back and types `git remote -v` (extra) →
TERM(laptop/13: 2–3); both `dlops-io/cheese-app-ci-cd` URLs ORANGE. Then the terminal shrinks to a
3-row strip, and the drawing takes the frame: the laptop's PINK push arrow aims at an ORANGE box
"dlops-io/cheese-app-ci-cd · the course's"; a RED stamp "permission denied" (no terminal output for
it).
SAY: Before the README's git push, an extra check: git remote, dash v. Origin is still the course's repository, and you can't write to it. GitHub would refuse a push from here: permission denied.

SHOW: The ORANGE box slides aside; two BLUE boxes appear, one per phrase: "fork it on GitHub" (with a
small GREY "Actions tab → enable workflows" chip) and "new empty repo" (GREY chips under it: "empty:
no README · no license · no .gitignore" and "HTTPS + token? it needs the workflow scope"). Under
**both** boxes, a GREY code card (tag "shown, not run"): `git remote set-url origin
https://github.com/<you>/cheese-app-ci-cd.git`, with a YELLOW `▶ your turn` beside it. A GREY chip:
"asked to sign in? a personal access token or `gh auth login` · never your password".
SAY: So point origin at a repository you own. Either fork the course's repository and enable workflows on its Actions tab, or create a new empty repository. Either way, run git remote set-url origin, with your own address. Pause and set yours up.

SHOW: The drawing shrinks to the top right. The terminal grows back and types `git init --bare -b main
/home/student/github-standin/student/cheese-app-ci-cd.git` (extra; folds) → TERM(laptop/20: 2 wrap),
then `git remote set-url origin /home/student/github-standin/student/cheese-app-ci-cd.git` (extra;
folds) → TERM(laptop/21: → (no output)). A GREY chip on the BLUE box: "stand-in for your GitHub
repository".
SAY: This recording machine can't push to GitHub, so an empty repository on the same machine stands in for yours. From now on we just say your repository.

SHOW: TRACKER P5 6. It types `git push` → TERM(laptop/22: 2–3); line 3 `* [new branch]      main ->
main` GREEN (line 2's stand-in path GREY); a GREY chip on the terminal: "on GitHub: more lines first,
same last line". `▶ your turn`. The terminal shrinks to a strip; a PINK arrow flies from the laptop
into the BLUE "your repository" box; a PINK spark: "event · run 1"; a TEAL tag chip
`cheese-app-api:b8458ff…` forms beside it.
SAY: Now the README's git push. New branch, main to main. This push is the event, and run 1 starts now. Pause and push yours.

SHOW: The fork box from block 6 returns small with a GREY chip "Everything up-to-date · no run" and a
dashed GREY arrow to "first run: part 2 (S12)". Fade; empty frame.
SAY: On a fork, that commit is already on GitHub, so git push says everything up to date and starts nothing. To get run 1 anyway, push an empty commit: git commit, allow empty, dash m, Trigger CI, then git push. Or wait, and your first run then comes with the fix in part 2.

---

## S07 · Watch the run: six colors — `s07_watch.py` · `WatchTheRun`

SHOW: TRACKER P5 7. README(353–357) as a five-line card (left). Right, a schematic Actions tab (BLUE
frame, tag `illustration`): tabs "Code · Issues · Pull requests · Actions" with "Actions" YELLOW; one
run row "demo class 1 · CI Pipeline · main" with a YELLOW dot ("in progress"); a GREEN ✓ and a RED ✗
legend chip appear on "green checkmark" and "red X". A YELLOW `▶ your turn` on the "Actions" tab.
GREY chips: "no run? `ci.yml` not at the repo root (S03) · branch not main/develop (S04) · fork:
workflows not enabled (S06)" and "yellow annotations? deprecation notices · the run still counts".
SAY: Watch GitHub Actions: go to your repository, and click the Actions tab. Your run is listed under the commit message, with a yellow dot: in progress. A green checkmark means success; a red X means failure. Pause and open yours.

SHOW: The row is clicked (a GREY cursor dot). GRAPH(run1) at the start state: six GREY nodes in
GitHub's layout with the job names; `Build Docker Image` turns YELLOW (running).
SAY: Click it, and GitHub draws the run as the graph you just built: build first, four jobs side by side, the summary last.

SHOW: The graph shrinks right. Inset left: six BLUE boxes in the graph's layout, each with a small
empty "Docker" shelf and the caption "a fresh machine · empty Docker"; below them a GREY laptop with a
PURPLE "act" chip, "second witness". Both get a GREEN "same verdict" tick.
SAY: A word on how we show it. We ran every job of this file right here, each on a brand-new machine with an empty Docker, as GitHub does. And a tool called act ran the whole file a second way, with the same verdict.

SHOW: The inset shrinks into a GREY note on the graph's `illustration` tag: "drawn from ci.yml · log
lines real".
SAY: So the GitHub pages you see are drawings built from the workflow file, marked illustration. Every log line in them is real.

SHOW: The graph returns to the center, build node YELLOW, the other five GREY. On "on main", S04's
door replay icon (the dot already inside the BLUE server) pulses small beside the graph; on "refuse
it" the run badge pulses once. No colors change.
PONDER(8 s, "This run turns red, as in the opening.\nIs your push on main in your repository,\nor did the red run refuse it?")
SAY: A question, before the colors come in. You already know this run turns red. Is your push on main in your repository now, or did the red run refuse it?

SHOW: The card leaves. The reveal from `runner/run1/results.txt`, node by node on each phrase: Build
✓ GREEN; Lint and Format Check ✗ RED; Unit Tests, Integration Tests, System Tests ✓ GREEN (YELLOW
first, then GREEN); Test Summary ✓ GREEN; the run badge ✗ RED.
SAY: Yes, it's on main: the push landed before any job started, and a red run can't undo it. Build: green. Lint and Format Check: red. The three tests and Test Summary: green. The run: red.

SHOW: LECTURE 21 · 21. The CiLoop from S03 returns small, top right: the ✓/✗ marks fly from the graph
onto its "Notifications" bar. TRACKER P5 7 · extra. A laptop strip types line 1 of `laptop/62` (extra;
folds) → ACT(421, 513, 567, 682, 732, 749, 750): five `🏁  Job succeeded` lines GREEN, `Job failed`
(513) and `Error: Job 'Lint and Format Check' failed` (750) RED.
SAY: Those checks and crosses next to your commit are the lecture's notifications. And act, the second witness, agrees: five jobs succeeded, one failed.

SHOW: LECTURE off. TRACKER P5 8. The strip leaves. RECORDED(screenshot) slides in small beside the
graph: six GREEN nodes with their times. A GREY `erratum` chip: "an earlier version of the code".
SAY: A kind note: the README's screenshot is all green. It shows an earlier version of the code. Your first run is red, and in part 2 you turn it green.

SHOW: The screenshot leaves. The RED lint node and the GREEN summary node pulse together; S01's
question card returns small between them: "Which machine said no, and why didn't the summary hear
it?" Fade; empty frame.
SAY: And here is the hook, on your own push: two of these six machines disagree. In part 2 we open every log, one job at a time.

---

## S08 · Build once; every job starts empty — `s08_artifact.py` · `BuildOnce`

SHOW: TRACKER P5 8. STRIP Build Container (the strip slides in under the tracker; `Build Container`
YELLOW). LECTURE 21 · 27, 31. A GREY chip from slide 27: "Build Container: one environment, build
problems found early". A single BLUE box "remote CI server" (the lecture's one, named in slide 31's
text).
SAY: Part 2, job by job. First, build container: the lecture builds it first, so every check runs in the same environment, and build problems show up early.

SHOW: The single BLUE box splits into six (V5's six rooms in the graph's layout). A narrow
CODE(.github/workflows/ci.yml) strip shows lines 17, 43, 72, 107, 130, 174 one after another, each
`runs-on: ubuntu-latest` flying to its room. Each room shows an empty "Docker" shelf.
SAY: The lecture speaks of one remote CI server. GitHub gives you a new one for every job: runs on, ubuntu latest, six times in this file. Each job starts on an empty machine.

SHOW: LECTURE off. README(289–294) card, left; CODE(.github/workflows/ci.yml: 15–26) right, then a
Transform to CODE(.github/workflows/ci.yml: 27–38); each README bullet lights with its line: "Builds
the Docker image once" ↔ 27, "Tags … github.sha" ↔ 27's `${{ github.sha }}` PINK, "Saves … tar" ↔ 31,
"uploads it as an artifact" ↔ 33–38.
SAY: The README's build job builds the image once, tagged with the commit ID. It saves it as a tar file and uploads it as an artifact, so every other job gets the exact same image.

SHOW: The README card shrinks into the tracker's caption; the code panel leaves. A small GRAPH(run1)
(tag `illustration`): a GREY cursor dot clicks the Build node; its step list opens beside it, and the
"Build Docker image" row expands into the LOG panel while the graph leaves: LOG(run1/build/03: 2,
4–5, …, 653, 656), title "Build Docker Image › Build docker image"; line 653 `naming to …
cheese-app-api:b8458ff…` TEAL. **V5 `ImageSuitcase`** in the build room: Dockerfile layers stack into
a TEAL cube stamped `cheese-app-api:b8458ff…`. A GREY chip under the cube: "this commit's image ·
nothing else" (README 340).
SAY: On GitHub, click a job, then a step, to open its log. Docker builds the image from the Dockerfile and names it cheese app API, colon, the commit ID. That tag means this commit's image, nothing else.

SHOW: The build log stays; its line 2 `#0 building with "default" instance using docker driver`
lights YELLOW. README line 291 "Uses Docker Buildx for efficient caching" returns as a one-line GREY
card with a GREY `erratum` chip. A laptop strip types line 1 of `laptop/62` (extra) → ACT(313):
`docker:default` YELLOW. A small GREY dashed "cache" box beside the build room stays empty; a GREY
chip "no cache-to / cache-from".
SAY: A small slip: the README promises Buildx caching, but the build runs on the default builder, and nothing saves a cache, so every fresh machine rebuilds from scratch. The exercises show how.

SHOW: The strip, the card and the build log leave. LOG(run1/build/04: heading only) (title "› Save
Docker image", no output, badge "exit 0"): the cube folds into a TEAL tar suitcase. LOG(run1/build/05:
2) (title "› Upload Docker image artifact", the stand-in's `ls -l`; the byte count is shown as "≈ 176
MB" in a GREY overlay chip, the exact number masked). The suitcase flies out to a BLUE shelf "artifact
store" outside the rooms with a GOLD `cost_tag("artifact · about 176 MB · 1 day")`. The build room
dissolves.
SAY: Docker save folds the image into one file, about 176 megabytes. The upload step carries it to the artifact store, kept for one day. Then the build machine is thrown away.

SHOW: The lint room zooms in (BLUE). Inside it, LOG(run1/lint-and-format/x1: 2) (title "Lint and
Format Check · extra: docker images"), tag `extra`: just the header row, GREY; the room's Docker shelf
is empty.
SAY: Now step into a fresh check job. An extra command, docker images, shows just the header. No image at all.

SHOW: CODE(.github/workflows/ci.yml: 49–57) beside the room: lines 49–53 (download) PINK, 55–57
(`docker load -i /tmp/cheese-app-api.tar`) TEAL. A suitcase copy flies from the store into each of the
four rooms (none into the summary room: GREY chip "needs only bash"); in the lint room it unfolds back
into the cube. LOG(run1/lint-and-format/03: 2) (`Loaded image: cheese-app-api:b8458ff…`), the proof.
The README chip "Artifact Sharing" lands on the store. On "after a day", the suitcase left on the
store shelf pulses GOLD "1 day" and fades.
SAY: So every check job downloads the artifact and runs docker load, dash i, on the tar: the same tag, unpacked from the suitcase. That's artifact sharing. And the artifact expires after a day, so re-running a failed job tomorrow fails at the download.

SHOW: A fresh room without the load step: on "Delete" a strike draws across the CODE strip's lines
84–86 (unit tests' "Load Docker image"), GREY dashed; on "Which step fails" the room's empty shelf
pulses.
PONDER(8 s, "Delete the 'Load Docker image' step\nfrom unit-tests.\nWhich step fails, and with what error?")
SAY: Your turn to predict. Delete the load docker image step from the unit tests job. Which step fails, and with what error?

SHOW: The card leaves. LOG(noload/x1: 2) (empty header), extra; then LOG(noload/x2: 2–3, crop7)
(title "Unit Tests › Run unit tests (no load)", tag `extra`): line 2 `Unable to find image … locally`
GREY, line 3 `pull access denied for cheese-app-api, repository does not exist …` RED; badge "exit
125". V5: the room asks its shelf (nothing), walks out to an ORANGE "Docker Hub" door, and is turned
away RED. Fade; empty frame.
SAY: The run unit tests step. Docker looks for the image on the machine and finds nothing, then asks Docker Hub, where no such image exists: pull access denied. Exit code 125: the step fails, so the job fails.

---

## S09 · Gates speak in exit codes — `s09_gates.py` · `ExitCodes`

SHOW: TRACKER P5 8. STRIP Lint and Format. LECTURE 21 · 22, 27. Two GREY chips from slide 22,
"coding standards" and "static code analysis", slide onto two PURPLE boxes "Black" and "Flake8". Under
them a GREY line: "formatter: rewrites · linter: reports" (L09).
SAY: Next, lint and format. The lecture's coding standards are Black here, and its static code analysis is Flake8. Remember lecture 9: a formatter rewrites your code; a linter only reports.

SHOW: LECTURE off. README(296–301) card shrinks to the left; CODE(.github/workflows/ci.yml: 59–67):
lines 61 and 66 show `api/` YELLOW and the two 120 flags YELLOW; line 62 `continue-on-error: false`
RED with a chip "blocking"; line 67 `continue-on-error: true` GREY with a chip "advisory".
SAY: Both run inside the image, on the api folder, at 120 columns. The Black step says continue on error, false: it blocks. The Flake8 step says true: it's advisory, a warning that never fails the job.

SHOW: **V6 `ExitGates`**: the job as a column of five step gates (Checkout, Download, Load, Black,
Flake8). A demo token: each command holds up a `0` and its gate opens GREEN; then a generic gate holds
up `1`: it shuts RED, and the red climbs to a "job" badge, then to a "run" badge; the gates below grey
out, dashed.
SAY: How does a step fail? Every command ends with an exit code. Zero opens the gate. Anything else shuts it, and the red climbs from the step to the job to the whole run.

SHOW: The demo resets to run 1. LOG(run1/lint-and-format/04: 4–7, crop7) (title "Lint and Format
Check › Run Black formatter check"): line 4 `would reformat /app/api/utils.py` RED, line 6 `Oh no! 💥 💔
💥`, line 7 `1 file would be reformatted, 2 files would be left unchanged.`; badge "exit 1" RED. The
Black gate holds up `1` and shuts.
SAY: Run 1, the Black step: would reformat utils dot py. One file would be reformatted. Exit code 1, so the gate shuts.

SHOW: STEPS(run1/lint-and-format: 2–7): Checkout ✓, Download ✓, Load ✓, Run Black formatter check ✗
RED, Run Flake8 linter ⊘ GREY dashed "skipped"; job result ✗. On V6 the Flake8 gate greys out, dashed.
SAY: The step list shows what happened next. Black, failure. Flake8, skipped. The steps below a failed step don't run, unless they ask to run always.

SHOW: CODE(src/api-service/api/utils.py: 7–13): line 7 `def power(base,exponent):` with the comma
RED-ringed; lines 10–12 (three blank lines) shaded RED. A GREY chip: "the mess from L09 · kept on
purpose for teaching".
SAY: The cause is the mess you met in lecture 9, still in the repository on purpose: no space after the comma, and three blank lines where two belong.

SHOW: A GREY dashed ghost of the Flake8 gate replays: LOG(run1/lint-and-format/x4: 4–5) (title "Lint
and Format Check · extra: Flake8, if it had run", tag `extra`): `api/utils.py:7:15: E231 …`, `api/
utils.py:13:1: E303 …`; badge "exit 1". The ghost gate holds up `1`, but a GREY shunt arc
(continue-on-error) carries the flow around it; the job badge would stay where Black put it, a small
warning dot.
SAY: What would the skipped Flake8 have said? An extra run shows two warnings on those same lines. But even then it's advisory: only Black decides the job.

SHOW: V6 condenses into one line of text under the column: "exit code ≠ 0 → the step fails". Fade;
empty frame.
SAY: So that's the whole rule: a step fails when its command exits with anything but zero. It's the only thing CI listens to.

---

## S10 · Three test jobs, three altitudes — `s10_tests.py` · `TestJobs`

SHOW: TRACKER P5 8. STRIP Test. LECTURE 21 · 27. The strip's `Test` box grows down into three boxes
`Unit Tests` (GREEN-edged), `Integration Tests` (TEAL-edged), `System Tests` (BLUE-edged), stacked
like altitudes, the unit box lowest.
SAY: Now the tests. The lecture's one test box is three jobs here, side by side, each at a different altitude.

SHOW: LECTURE off. `Unit Tests` YELLOW. README(303–308) card small; CODE(.github/workflows/ci.yml:
88–95) beside it (line 90 YELLOW). LOG(run1/unit-tests/04: 15, …, 29, crop7) (title "Unit Tests › Run
unit tests"): `collected 11 items`, `…`, `11 passed` GREEN.
SAY: Unit tests check one function at a time, with no outside dependencies. The log collects 11 tests, and 11 pass.

SHOW: LOG(run1/unit-tests/05: 3, …, 75, 77) (title "Unit Tests › Generate coverage report"): line 3
GREY, line 75 `INTERNALERROR> PermissionError: [Errno 13] Permission denied:
'coverage/style_cb_4667309f.css'` RED (wrap), line 77 `11 passed` GREEN; badge "exit 3" RED.
SAY: Then the coverage step runs them again, and all 11 pass again. But pytest hits an internal error: permission denied, writing into the coverage folder. Exit code 3.

SHOW: STEPS(run1/unit-tests: 2–8) replaces the code panel and the log; `ci.yml` lines 95
(`continue-on-error: true`, GREY) and 102 (`if: always()`, PINK) ride in as chips onto their rows.
"Generate coverage report" ✗ with the chip "(continue-on-error: the job stays green)", "Upload
coverage report" ✓, job result ✓. V6 is drawn on the step rows themselves: the coverage row holds up
`3`, a GREY shunt arc jumps past it on "shunted aside"; a PINK "always" bridge reaches the upload row
on "if always", which opens on an empty box: LOG(run1/unit-tests/06: 2) `0`, the stand-in's count,
with a GREY chip beside it: "on GitHub: a warning, No files were found … coverage/ · expected, not
captured".
SAY: Yet the job is green. The step says continue on error, so the failure is shunted aside. Then the upload, marked if always, finds no files; on GitHub, a yellow warning says so.

SHOW: A GREY `erratum` chip on the README card's lines 307–308 ("terminal, XML, and HTML"). Extra:
LOG(run1/unit-tests/x3: 3, 7) (tag `extra`): line 3 `drwxr-xr-x … root root … .` ORANGE, line 7
`uid=1000(app) …` TEAL. A small drawing: a folder owned by "root" (ORANGE) on the runner, mounted
into the TEAL container where a user "app" bounces off it (RED). GREY chip "fix: exercises.md".
SAY: The README has a small gap: it promises terminal, XML and HTML reports. Docker creates the missing coverage folder as root, and the container's user, app, can't write into it. Create the folder writable first; the exercises have the fix.

SHOW: `Integration Tests` YELLOW. README(310–314) card small; CODE(tests/integration/test_api.py:
7–11): line 11 `client = TestClient(app)` YELLOW. A TEAL container with the app and a "test client"
inside the same box, a PINK arrow staying inside. LOG(run1/integration-tests/04: 15, …, 28, crop7):
`collected 10 items`, `…`, `10 passed, 1 warning` GREEN.
SAY: Integration tests use the FastAPI test client: the app is called inside the same Python process. No server, no port. 10 passed.

SHOW: `System Tests` YELLOW. README(316–323) card small; CODE(.github/workflows/ci.yml: 146–154)
(later a Transform to CODE(.github/workflows/ci.yml: 156–158) for the `--network host` block).
**V7 `SystemTestRig`** inside one BLUE runner: line 148 → a TEAL `api-server` container appears
(`-p 9000:9000` → an ORANGE door 9000 on the runner wall; `-e DEV=1` chip). LOG(run1/system-tests/04:
heading only, badge "exit 0"; the container id on line 2 hidden); extra LOG(run1/system-tests/x3: 2–3,
crop7, container id cropped) with `0.0.0.0:9000->9000/tcp` PINK.
SAY: System tests need the real thing. One container starts the server in the background and publishes port 9000 on the runner. An extra command, docker ps, shows it running, with 9000 mapped.

SHOW: Line 150–154 of the panel; a `sleep 10` hourglass empties; a PINK `curl -f` arrow knocks on the
door: LOG(run1/system-tests/05: 4, 8) (line 8 shown up to `}`: `{"message":"Welcome to the Cheese App
CI/CD Tutorial!"}` GREEN; the progress lines 5–7 hidden). The next gate opens.
SAY: Then the job waits 10 seconds, and curl, dash f, knocks on localhost 9000. Only when the welcome message comes back does the next gate open.

SHOW: The panel transforms to lines 156–158; line 158: a second TEAL container (the tests) starts with its own bubble; `--network host`
dissolves the bubble into the runner, and its PINK `localhost:9000` arrow reaches the door.
LOG(run1/system-tests/06: 15, …, 23, crop7): `collected 5 items`, `5 passed` GREEN. The README chip
"Network Modes" lands on the dissolved bubble.
SAY: A second container runs the tests with network host: it shares the runner's network, so localhost 9000 reaches the server. 5 passed.

SHOW: CODE(.github/workflows/ci.yml: 160–169): lines 161 and 166 `if: always()` PINK. LOG(run1/
system-tests/07: 3, 9, 10–15) (title "System Tests › Show server logs"; client addresses `172.18.0.1:…`
cropped to `…`): `Running in DEV mode`, `Application startup complete.`, the six requests `GET /`,
`GET /health`, …, `GET /euclidean_distance/?x=3&y=4 … 200 OK` scrolling in as PINK arrivals at the
door; line 10 `GET /` labelled GREY "curl", line 11 `GET /health` labelled GREY "skipif probe", lines
12–15 "tests". Then LOG(run1/system-tests/08: 3–4) `api-server` twice: the container fades. The README chip
"Conditional Execution" lands on the two `always` steps.
SAY: Two steps marked if always come last, even after a failure: show the server log, where every test request arrives, then stop and remove the container. That's the README's conditional execution.

SHOW: Small and GREY in a corner, L09's trapdoor (`skipif`, a dashed hatch) drawn shut; the `curl -f`
gate glows beside it. GREY caption: "in CI: a missing server fails loudly". Fade; empty frame.
SAY: In lecture 9, a missing server made these tests skip quietly. Here the curl gate makes it fail loudly instead.

---

## S11 · The summary listens only to tests — `s11_summary.py` · `TheSummary`

SHOW: TRACKER P5 8. STRIP Summary. LECTURE 21 · 16, 26–27. A GREY chip from slide 27: "Summary:
collects the results, reports pass / fail". README(325–330) card small; CODE(.github/workflows/ci.yml:
172–183): line 175 `needs: [unit-tests, integration-tests, system-tests]` YELLOW, line 176 `if:
always()` PINK.
SAY: Last job: the summary, which the lecture says collects the results and reports pass or fail. Its needs line names the three test jobs. And if always lets it run even when one of them failed: it runs, which isn't the same as passing.

SHOW: LECTURE off. Transform to CODE(.github/workflows/ci.yml: 181–192): lines 181–183 (the three
`needs.<job>.result` echoes) PINK; line 185 (the `if` comparison) YELLOW; lines 187 and 191
(`>> $GITHUB_OUTPUT`) PINK with a small "for later steps" note; line 188 `exit 1` RED.
SAY: Its script prints each job's result, writes a status to GitHub output for later steps, and exits with 1 if any result isn't success.

SHOW: **V4, S11 form**: the run 1 graph (GRAPH(run1), small). Three PINK tokens `success` slide along
the three `needs` arrows into the summary node. Beside it LOG(run1/test-summary/01: 13–16) (heading
collapsed): the three lines GREEN, line 16 `✅ All tests passed!` GREEN.
SAY: In run 1, three success tokens arrive: unit, integration, system. All tests passed.

SHOW: The RED lint node pulses; no token leaves it; the GREY dashed gap with its "?" from S05 returns
between lint and summary and the "?" turns into a GREY "not in needs". The run badge RED pulses: a
GREY chip "any failed job → the run is red".
SAY: And here is the hook, answered. Lint isn't in needs, so its failure never reaches the summary. The run is still red, because any failed job turns the whole run red.

SHOW: A plain GREY note (no `erratum` tag) on README line 328 "Checks the results of all test jobs":
"true · lint is not a test job". A GREY dashed arrow "after the fix" draws from lint to the summary; GREY chip
"exercises.md: add lint-and-format to needs + the check".
SAY: The README says the summary checks the results of all test jobs, and that's literally true: lint isn't a test job. Add lint and format to needs and to the check if you want it counted.

SHOW: The graph shrinks. CODE(history/c3b227f-service.py: 38–44), header `c3b227f · service.py ·
lines 38–44`: line 40's docstring `sqrt(x^2 + y^2)` WHITE, line 44 `result = math.sqrt(2 * z)` RED. A
GREY chip "demo class 1 · 2025-11-13". A GREY chip under the panel: "unit tests → utils.py ·
/euclidean_distance/ → integration + system".
SAY: Now the bug from class. In the demo commit, the distance function takes the square root of 2 times z, instead of z. We ran this one for you: just watch.

SHOW: Beside the panel, GRAPH(run-demo) at the start state: six GREY nodes, a GREY chip "the demo
commit". On "Which jobs" the six GREY nodes pulse left to right; on "Test Summary" the summary node
pulses. No colors change.
PONDER(8 s, "The demo commit computes sqrt(2·z)\ninstead of sqrt(z).\nWhich jobs turn red,\nand what does Test Summary say now?")
SAY: Predict before the run. Which jobs turn red now, and what does Test Summary say?

SHOW: The card leaves. GRAPH(run-demo) colors node by node from `runner/run-demo/results.txt`:
Integration Tests ✗ RED with LOG(run-demo/integration-tests/04: 32, 35) (`assert 7.0710678118654755
== 5.0`, `1 failed, 9 passed, 1 warning` RED).
SAY: Integration: red, 1 failed and 9 passed. The distance for 3 and 4 came back as about 7, not 5.

SHOW: System Tests ✗ RED with LOG(run-demo/system-tests/06: 27, 35, 51) (the two `assert … ==` lines
and `2 failed, 3 passed` RED; GREY chips on the asserts: line 35 "x=3, y=4", line 27 "default x=1,
y=2"); Unit Tests ✓ GREEN with a GREY chip "only power() has unit tests";
Lint and Format Check ✗ RED with a GREY chip "still utils.py".
SAY: System: red, 2 failed and 3 passed: 3 and 4 again, and the default point, 1 and 2, which came back too large as well. Unit: green, because only the power function has unit tests. Lint: red anyway, for utils dot py.

SHOW: Two PINK tokens `failure` and one `success` slide into the summary node; it turns RED. LOG(run-
demo/test-summary/01: 13–16): `Integration Tests: failure`, `System Tests: failure` RED, line 16 `❌
Some tests failed!` RED; badge "exit 1". Fade; empty frame.
SAY: And the summary now says some tests failed, and exits with 1. This time the summary heard it.

---

## S12 · Fix, push, green: one turn of the loop — `s12_green.py` · `RedToGreen`

SHOW: TRACKER P5 8. STRIP Lint and Format. LECTURE 21 · 21. **V2 `CiLoop`** at full size with run 1's
marks on the "Notifications" bar (RED ✗ on lint); the bar's arrow back to "Developers" lights PINK; a
GREY "fix" chip appears beside "Developers".
SAY: Back to run 1 and the lecture's loop. The notification came back red, so now the developer fixes the code and commits again, and the loop goes around once more.

SHOW: LECTURE off. TRACKER P5 8 · Part 4 · L09. The loop shrinks to the top right. Full-width terminal
`laptop` types `pip install pre-commit` → TERM(laptop/30: 2, …, 39 wrap) (`pre-commit-4.7.0` YELLOW,
chip "at the time of recording"); then `pre-commit install` → TERM(laptop/31: 2).
SAY: The fix is the tool from lecture 9, Part 4 of the same README, so these steps are extras here. Pip install pre-commit, then pre-commit install, which puts the hook into dot git, hooks.

SHOW: It types `pre-commit run --all-files` (README.md:262, caption "Part 4 · L09") → TERM(laptop/32:
…, 15–22, 24, 26, 29, 31) (the `[INFO]`/`[WARNING]` lines 2–14 collapsed into one `…`, with a GREY chip on it: "first run: a
few minutes (downloads the hook environments)"): the hygiene
lines `Passed` GREEN, line 19 `Skipped` GREY, line 22 `Format Python code with Black…Failed` RED, line
24 `- files were modified by this hook`, line 26 `reformatted src/api-service/api/utils.py` YELLOW,
line 31 Flake8 `Passed` GREEN. `▶ your turn`.
SAY: Then pre-commit run, all files. The hygiene checks pass; Black fails, because it modified a file: reformatted utils dot py. Flake8 then passes. Pause and run it.

SHOW: It types `git diff` → TERM(laptop/33: 6, 10–17): line 10 RED, line 11 `def power(base,
exponent):` GREEN, line 16 (the removed blank line) RED.
Under the strip, `def power(base,exponent):` → TransformMatchingShapes → `def power(base, exponent):`
(the new space glows GREEN), and three blank-line bars become two (one fades RED).
SAY: Git diff shows exactly what Black changed: a space after the comma, and one blank line gone.

SHOW: It types `pre-commit run --all-files` → TERM(laptop/34: 2–10): every line `Passed` GREEN
(`Skipped` GREY).
SAY: Run it again, and every hook passes. Nothing is left to fix.

SHOW: It types `git add .` → TERM(laptop/35: → (no output)); `git commit -m "Format utils.py with
Black"` (GREY chip "our message · the README has none") → TERM(laptop/36: 9–12) (the Black and Flake8
hook lines `Passed` GREEN, `[main 2289d89] Format utils.py with Black`, chip "your commit ID will
differ"); `git push` → TERM(laptop/37: 3) `b8458ff..2289d89  main -> main` GREEN. `▶ your turn`.
SAY: Now git add dot, and git commit with a message: Format utils dot py with Black. The message is ours; the README has none. The hooks run on the commit and pass. Then git push. Pause and push yours.

SHOW: TRACKER P5 8. The terminal leaves. GRAPH(run2): all six nodes turn GREEN one after another, the
run badge GREEN. STEPS(run2/lint-and-format: 5–6): Black ✓, Flake8 ✓ (no longer skipped);
LOG(run2/lint-and-format/04: 4–5) `All done! ✨ 🍰 ✨`, `3 files would be left unchanged.` GREEN.
SAY: Run 2: all six green. In the lint job, Black is happy, and this time Flake8 runs too, and passes. On a fork, this is your first run, and it's green.

SHOW: RECORDED(screenshot) slides in beside GRAPH(run2), its six GREEN nodes matching. The loop in the
corner grows back: a new commit dot goes around Commits → Codebase → Build → Test, and GREEN ✓ marks
come back along the return lines; the "?" from S03 is gone. Fade; empty frame.
SAY: Now your run matches the README's screenshot. One turn of the loop: a red notification, a fix, a commit, and a green run.

---

## S13 · The local conundrum: --no-verify — `s13_noverify.py` · `NoVerify`

SHOW: TRACKER P5 8 · extra. STRIP Lint and Format. LECTURE 21 · 29–31. A GREY title chip from the
slides: "The local conundrum". Beside it two icons: a GREY laptop with its three gates (V1) and a BLUE
server with `Check Code`, joined by a YELLOW "why twice?".
SAY: The lecture calls this one the local conundrum. If the hooks already ran on your laptop, why run the same checks again on a server?

SHOW: Full-width terminal `laptop` types line 1 of `laptop/40` (extra; folds) → TERM(laptop/40:
10–11): line 10 `-    z = power(x, 2) + power(y, 2)` RED, line 11 `+    z=power(x,2)+power(y,2)`
GREEN-outlined but YELLOW-highlighted (the squeezed spaces).
SAY: These steps are extras, and you can just watch. A quick edit squeezes the spaces out of one line in service dot py, and git diff shows it.

SHOW: It types `git add .` → TERM(laptop/41: → (no output)); `git commit -m "quick fix"` →
TERM(laptop/42: 9–13) (line 9 `Format Python code with Black…Failed` RED, line 13 `reformatted
src/api-service/api/service.py` YELLOW). Then the terminal shrinks to a 3-row strip, and V1 small
takes the middle: the commit dot stops at the laptop's Black gate.
SAY: Git add dot, then git commit, dash m, quick fix. The Black hook fails and reformats the file, so the hook stopped the commit.

SHOW: It types `git status --short` → TERM(laptop/43: 2) `MM src/api-service/api/service.py`; the
two M's label two small file icons: "staged: messy" (RED) and "working copy: reformatted" (GREEN).
SAY: Git status, short, shows the letter M, for modified, twice. Black fixed your working copy, but the staged copy is still the messy one.

SHOW: Slide 30's command: it types `git commit --no-verify -m "quick fix"` (extra; `--no-verify` RED) →
TERM(laptop/44: 2–3) `[main 2892b1b] quick fix`. Then the terminal shrinks to a 3-row strip, and V1
takes the middle: a RED bypass arc swings around all three laptop gates; the dot passes without
touching them.
SAY: Now the lecture's command: git commit, no verify, dash m, quick fix. No hook ran, and the commit exists: no verify skips every pre-commit check.

SHOW: The strip types `git push` → TERM(laptop/45: 3) `2289d89..2892b1b  main -> main`. The dot flies
into the BLUE server; the strip leaves as GRAPH(run3) arrives and colors from
`runner/run3/results.txt`: lint ✗ RED, the tests ✓, summary ✓, run badge ✗. The graph shrinks left and
LOG(run3/lint-and-format/04: 4–7, crop7) takes its right half: line 4 `would reformat
/app/api/service.py` RED; badge "exit 1".
SAY: We push it. Run 3: lint and format, red, on service dot py. The tests and the summary all pass.

SHOW: LOG(run3/lint-and-format/x4: 4–6) (tag `extra`, title "Lint and Format Check · extra: Flake8,
if it had run"): `api/service.py:43:6: E225 …`, `api/service.py:43:14: E231 …`, `api/service.py:43:25:
E231 …`. The server's `Check Code` box flashes RED: "caught".
SAY: The skipped Flake8 would have flagged that line three times. CI caught what no verify let through: slide 31, at your terminal.

SHOW: LECTURE off. The graph shrinks. It types `git status --short` → TERM(laptop/48: 2) ` M
src/api-service/api/service.py`; then `git restore src/api-service/api/service.py && git status
--short` → TERM(laptop/49: → (no output)). Beside it a GREY code card (tag "shown, not run"), headed
"pushed it too?": `pre-commit run --all-files` · `git add .` · `git commit -m "Format service.py"` ·
`git push`.
SAY: Clean up the experiment. Here, git restore only throws away Black's fix in the working copy. If you followed along, the messy commit is on your main now, pushed or not. Not pushed yet? Git reset, hard, head tilde 1, drops it. Pushed? Run pre-commit run, all files, then add, commit and push, before part 6.

SHOW: Two columns: left "local hooks" (GREY) lists nine rows (`trailing-whitespace`, `end-of-file`,
`check-yaml`, `large files`, `check-json`, `merge conflicts`, `detect-private-key`, `Black`,
`Flake8`, from `.pre-commit-config.yaml:12–44`); right "CI" (BLUE): only `Black` and `Flake8` get
GREEN ticks with a chip "api/ only" (`ci.yml:61, 66`); the seven hygiene rows get GREY dashed "not in
CI". A GREY `erratum` chip: "the slides: CI repeats the checks · this CI: two of them".
SAY: But CI repeats only Black and Flake8, and only on the api folder. The seven hygiene hooks never run in CI: trailing whitespace, end of file, YAML, large files, JSON, merge markers, and private keys.

SHOW: Two small version chips: GREY "pre-commit: Black 24.1.1 (pinned)" and TEAL "image: black
26.10.1 (newest)", chip "at the time of recording"; a GREEN "=" between them that wobbles into a GREY
dashed "≠ some day".
SAY: One more gap: the hooks pin an older Black than the image installs. At the time of recording they agreed, but they can drift apart.

SHOW: The table and the version chips clear. A GREY key-file icon (labelled "key file", no content)
sits on the laptop; on "with no verify" it rides a RED `--no-verify` arc into the BLUE server, where
GRAPH(run3)'s six job nodes wait GREY; on "pushes to main" it lands. No hook names on screen.
PONDER(8 s, "A teammate commits a private key file\nwith --no-verify and pushes to main.\nWhich job of this pipeline catches it?")
SAY: A teammate commits a private key file with no verify and pushes to main. Which job of this pipeline catches it?

SHOW: The card leaves. The key icon passes all six job nodes untouched (each flashes GREY). LECTURE 21
· 11. A GREY chat-card fragment, re-drawn and tagged `illustration`: "Failed step: Run python3 -m
pre-commit run --all-files"; a GREEN dashed new step slides into the lint job: "pre-commit run
--all-files". A RED chip "rotate the key: it's already on GitHub". Fade; empty frame.
SAY: None. Detect private key is a local hook only. The fix is one CI step, pre-commit run, all files: the very step that fails on the lecture's imagined Slack message. And rotate that key; it's already on GitHub.

---

## S14 · Webhooks, secrets and the Slack bell — `s14_slack.py` · `SlackBell`

SHOW: TRACKER P5 8 · extra. STRIP Summary. LECTURE 21 · 7, 9. **V8 `SlackRoute`, arrow 1**: a BLUE
"GitHub" box fires a PINK "POST" arrow *out* to three GREY targets, one per phrase: "external CI
(Jenkins)", "deploy server", "chat".
SAY: That imagined message brings us back to the lecture's webhooks. A webhook is GitHub calling an outside address when something happens: to start an outside CI system such as Jenkins, to deploy, or to post to a chat.

SHOW: LECTURE off. **V8, arrow 2**: inside a BLUE runner, the last step of `test-summary` fires a PINK
"POST" arrow *in* to the GREY Slack window's "incoming webhook" slot; the arrow-1 picture shrinks to a
GREY dashed ghost above it: "the other direction". A GREY chip: "optional · your own Slack workspace ·
Slack app → Incoming Webhooks → Add New Webhook".
SAY: This part is optional: it needs your own Slack workspace. And this webhook works the other way round. Slack gives you an incoming webhook, an address, and the last steps of the test summary job call it. GitHub doesn't ring this bell; your workflow does.

SHOW: LECTURE 21 · 10–12. The two arrows clear. Left, a GREY card "the lecture's wish" (tag
`illustration`, no names: the author is "a teammate", no reply drawn): "Build failed · failed step ·
tests: failing / passing · lint: errors / warnings · duration". Right, a GREY chat window
"#build-alerts", caption "what this workflow sends", with the real payload re-drawn (tag
`illustration`) from `ci.yml:207–252` (header 209–216: "✅ CI Pipeline Passed / ❌ CI Pipeline Failed";
fields 219–236: Repository, Branch, Commit, Author; test lines 243 with ✅/❌; links 250: "View Commit"
· "View Workflow Run"). On "This workflow sends less", the wish lines the payload also carries (build
status, a mark per test job) fly into the chat window's fields; "failed step", the counts and
"duration" stay behind, dimmed, with a GREY chip "not sent". A friendly RED bell (not a meme) replaces
slide 12's "shame".
SAY: The lecture imagines a Slack channel told about every push, failures included, with the failed step, counts and duration. This workflow sends less: passed or failed, the repository, branch, commit and author, one mark per test job, and two links.

SHOW: LECTURE off. A schematic Settings page (BLUE frame, tag `illustration`): breadcrumb "Settings → Secrets and
variables → Actions → New repository secret"; Name `SLACK_WEBHOOK_URL`; Secret
`https://hooks.slack.com/services/<your-webhook-path>` (placeholder, GREY). A struck GREY tab
"Settings → Webhooks" with a RED ✗ "not here". The secret drops into a BLUE vault; a log line beside
it shows `***`; a GREY chip "PRs from forks: no secrets".
SAY: The webhook address is a secret. Add it under Settings, Secrets and variables, Actions, as a new repository secret named Slack webhook URL, not under Webhooks. It never goes in the repository, logs show it as three stars, and pull requests from forks don't get it.

SHOW: CODE(.github/workflows/ci.yml: 194–205): line 197 `if [ -n "${{ secrets.SLACK_WEBHOOK_URL }}"
]` YELLOW; lines 198, 200 PINK; line 204 `if: always() && steps.slack-check.outputs.enabled == 'true'`
YELLOW. Then CODE(history/199abd9-to-1a5e363-ci.yml.diff: 9–20): line 19 (`- if: always() &&
secrets.SLACK_WEBHOOK_URL != ''`) RED, lines 9–16 and 20 GREEN.
SAY: The check step tests whether the secret is set, and writes enabled, true or false. Why not test the secret right in the if line? GitHub doesn't allow secrets there; the repository's own history tried it, and replaced it with this shell check.

SHOW: LOG(run1/test-summary/02: 1–5 as heading) (title "Test Summary › Check if Slack webhook is
configured"): `if [ -n "" ]` with the empty string YELLOW; an `enabled=false` note PINK.
STEPS(run1/test-summary: 2–5): "Send Slack notification" ⊘ skipped with its chip "(steps.slack-check.
outputs.enabled is 'false')".
SAY: In run 1 there's no secret, so enabled is false, and the Slack step is skipped, as it should be.

SHOW: STEPS(run-demo/test-summary: 2–5): "Check test results" ✗ RED; "Check if Slack webhook is
configured" ⊘ GREY dashed; "Send Slack notification" ⊘ with its chip "(… enabled is '')". **V6** is
drawn on the step rows themselves (no second column): the first row shuts RED; the second greys out
(no PINK "always" bridge reaches it); the third reads the empty `''` → `'' == 'true'`: false. The GREY chat window stays silent; the RED bell gets a slash.
SAY: Now the demo run. Check test results fails. The check step has no if always, so it's skipped too, enabled stays empty, and the Slack step's condition is false.

SHOW: A GREEN fix overlay on CODE line 194–195: `if: always()` added to the check step (GREY chip
"exercises.md · hardened with env:"); the gate re-opens, the bell rings ❌ into the chat window. Fade;
empty frame.
SAY: As written, the bell only rings for good news. The fix is one line: if always, on the check step. The exercises have a hardened version.

---

## S15 · Branch protection: from report to gate — `s15_protect.py` · `ProtectMain`

SHOW: TRACKER P6 1 (the P6 tracker replaces P5: "README › Part 6: Branch Protection (Optional)", 6
dots). LECTURE 21 · 5–6. S02's door returns: the `post-receive` bell with the BLUE "Actions" badge
behind the door; in front of it the GREEN "branch protection" gate lights and shuts.
SAY: Part 6 of the README is optional, and it's the lecture's gate. A push-triggered run is the post-receive bell. On GitHub dot com, the gate that refuses is branch protection, with required status checks.

SHOW: LECTURE off. README(373–379) card left. Right, a schematic Settings → Branches page (BLUE frame,
tag `illustration`): "Add rule"; Branch name pattern `main`; ☑ "Require a pull request before
merging"; ☑ "Require status checks to pass before merging". A GREY chip: "today's page: may say
classic branch protection rule · or offer rulesets".
SAY: Go to Settings, Branches, and add a rule for main. Tick the boxes Require a pull request before merging, and Require status checks to pass. Today's page may call it a classic rule, or offer rulesets instead.

SHOW: TRACKER P6 2. A check picker under the checkboxes: four rows with the job **names** `Lint and
Format Check`, `Unit Tests`, `Integration Tests`, `System Tests` (GREEN ticks); the README's ids
(`lint-and-format`, …, README line 378) as a GREY `erratum` overlay struck through: "names, not ids ·
listed after a recent run". GOLD `cost_tag("private repo: paid plan · public: free")` and a GREY chip
"GitHub Pro: Student Developer Pack".
SAY: Then pick the checks. A small slip: the picker lists jobs by their names, like Lint and Format Check and Unit Tests, not the README's IDs. They appear only after a recent run. On a private repository this needs a paid plan.

SHOW: TRACKER P6 3. README(383–396) as a GREY code card (tag "shown, not run"): `git checkout -b
feature/test-protection` YELLOW. S04's lanes return small: a dot pushed to `feature/test-protection`
gives no spark; the PR arrow into `main` gives one.
SAY: Then test it: git checkout, dash b, feature, test protection. Pushing that branch starts nothing, as you saw with the triggers; the run starts when you open the pull request.

SHOW: TRACKER P6 4. Full-width terminal `laptop` types `echo "def broken(): assert False" >>
tests/unit/test_utils.py` → TERM(laptop/51: → (no output)). TRACKER P6 4 · extra: it types `docker
build -t cheese-app-api:local .` (extra) → TERM(laptop/52: 2, …, 61) and `docker run --rm
cheese-app-api:local pytest tests/unit/ -v` (extra) → TERM(laptop/53: 15, …, 29): `collected 11 items`,
`11 passed` YELLOW. A GREY `erratum` chip on the card's line 388. On "start with test", the terminal
shrinks to a 3-row strip and CODE(pytest.ini: 6–8) takes the middle: line 8 `python_functions =
test_*` YELLOW.
SAY: The README breaks the tests by appending def broken, assert False. An extra run in the image still says 11 passed, because pytest only collects functions whose names start with test.

SHOW: The pytest.ini panel leaves; the terminal grows back. The restore (`laptop/54`, `git checkout --
tests/unit/test_utils.py`, extra) is not typed: a GREY chip "test file restored". It types `echo "def
test_broken(): assert False" >> tests/unit/test_utils.py` (extra) → TERM(laptop/55: → (no output)); the
rebuild (`laptop/56`, not printed: GREY chip "rebuilt") and `docker run --rm cheese-app-api:local
pytest tests/unit/ -v` → TERM(laptop/57: 28, 37–38): `test_broken FAILED`, `1 failed, 11 passed` RED.
On the README code card, the line 388 `def broken` is struck GREY and `def test_broken` is written
above it: commit the corrected line.
SAY: So name it test broken instead, an extra fix. Now 1 failed and 11 passed. That's the one that turns the pull request red, and with protection on, the merge button stays locked.

SHOW: TRACKER P6 5, then TRACKER P6 6. The terminal leaves. The code card's lines 391–393 (`git add
.`, `git commit -m "Intentionally break tests"`, `git push origin feature/test-protection`) light in
turn (shown, not run); then the card shrinks into a 3-line strip and a schematic PR row takes the
frame (tag `illustration`, described, no real page): "Unit Tests ✗ · required" and a GREY locked
"Merge" button; a GREY chip on the row: "fork: set base repository to <you>/cheese-app-ci-cd".
`▶ your turn`. The PR row fades; in a bottom strip the terminal types `git checkout --
tests/unit/test_utils.py && git status --short` (extra) → TERM(laptop/58: → (no output)). Fade; empty
frame.
SAY: Then git add dot, git commit, dash m, Intentionally break tests, and git push origin feature, test protection. Open the pull request on GitHub: the merge stays locked until the tests pass. Pause and try it on yours. Here, git checkout puts the test file back.

---

## S16 · Non-determinism, CD next, and recap — `s16_recap.py` · `Recap`

SHOW: No tracker, no strip. LECTURE 21 · 18–20. Four GREY stage boxes in a row, "training", "data",
"tests", "deployment", each gets a small wobbling "?" (non-determinism). Then four GREEN answer chips
drop under them, one per phrase: "version everything (L11: DVC)", "automate retraining and testing",
"monitor in production", "controlled rollout"; the second gets a YELLOW chip "Milestone 5".
SAY: The twist the lecture promised: non-determinism enters every stage when the code trains a model. Its answers: version everything; automate retraining and testing, which Milestone 5 asks for; monitor; and roll out with care.

SHOW: LECTURE 21 · 32–34. The CiLoop's "Test" box grows a GREY dashed arrow to a GREY dashed box "Deploy (CD) ·
lecture 23"; the repo name `cheese-app-ci-cd` with "CI" GREEN and "CD" GREY dashed.
SAY: Continuous deployment, the lecture's last section, automates the release: that's lecture 23.

SHOW: LECTURE off. A teardown card (GREY), four lines, each ticking GREEN on its phrase: "Part 6:
`git checkout main` · `git branch -D feature/test-protection` · `git push origin --delete
feature/test-protection` (closes the PR) · Settings → Branches: delete the rule"; "Slack: delete the secret + the incoming webhook";
"private repo: Actions → CI Pipeline → ⋯ → Disable workflow"; "local: git restore · L09's Docker
cleanup (README 568–574) · act's images".
SAY: Clean up: switch to main, and delete the test protection branch here and on GitHub; that closes its pull request. Remove the branch rule, and the Slack secret and webhook, if you made them. Disable the workflow on a private repository, and run the Docker cleanup from lecture 9.

SHOW: The card fades. **V2 `CiLoop`** one last time, each part lighting on its phrase: the PINK
Commits arrow ("event"); six BLUE rooms flash under Build and Test ("fresh machine"); a TEAL suitcase
rides Build → Test ("artifact"); the Test box shows a `0` / `1` gate ("exit code"); three PINK tokens
reach Notifications while the lint box stays outside ("only the jobs it needs").
SAY: Once more, the loop. Your push is the event. Each job gets a fresh machine, so the image travels as an artifact. Every step is a gate that reads an exit code, and the summary hears only the jobs it needs.

SHOW: A YELLOW "Test yourself" card, question 1 of 5 (answers in `exercises.md`): "Name two ways code
reaches the shared repository without passing your local hooks. Which checks does this pipeline
repeat, and which not?" A small V1 laptop beside it.
SAY: Test yourself, pausing on each. One: name two ways code reaches the shared repository without passing your local hooks. Which checks does this pipeline repeat?

SHOW: Question 2 (a small V5 room icon; its shelf empties on "fresh machine"): "Which unit gets a fresh machine, a job or a step? Why does
that force the image tar and a docker load in every check job?"
SAY: Two: which unit gets a fresh machine, a job or a step? And why does that force a docker load in every check job?

SHOW: Question 3 (V4's gap, small; the lint token stops at the gap on "red"): "Your run is red but Test Summary says ✅ All tests passed!
Explain, and give the one-line fix."
SAY: Three: your run is red, but the summary says all tests passed. Why, and what is the one-line fix?

SHOW: Question 4 (V6's shunt, small; the arc swings on "without failing"): "Why can Flake8 fail without failing its job, and why don't you
see Flake8's output when Black fails?"
SAY: Four: why can Flake8 fail without failing its job, and why don't you see its output when Black fails?

SHOW: Question 5 (S02's door and bell, small; the dot crosses the door, then the bell rings): "In the lecture's terms, is a push-triggered Actions
run a pre-receive or a post-receive check, and what turns it into a gate on GitHub.com?" A GREY chip
"answers: exercises.md · every command: the study guide". Fade out; empty frame.
SAY: Five: is a push-triggered run a pre-receive or a post-receive check, and what makes it a gate? Answers are in the exercises and the study guide.
