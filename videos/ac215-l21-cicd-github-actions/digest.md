# L21 · Automating Software Development: CI/CD with GitHub Actions II — tutorial digest

- **Ed lesson:** https://edstem.org/us/courses/97373/lessons/166046/ (I could not open Ed itself. The lecture-to-tutorial mapping comes from the course-site source, `tutorials_demo.md:270-275`, which titles the lecture "Automating Software Development: CI/CD with GitHub Actions and other tools II" and links only README Part 5.)
- **Primary repo:** `dlops-io/cheese-app-ci-cd`, branch `main`, commit `b8458ff0cc1898700b32a873b4665f43f50df71e`, committed 2025-11-13 13:59:04 -0500 (message "demo class 1"). It has a single branch.
- **Context-only repos (used in §7):**
  - `dlops-io/cheese-app-v3`, branch `main`, commit `3ecef56fea879ac480d260c0906cd95baf05179a`, 2025-11-28 16:00:06 -0500 (the API you deployed in L20)
  - `dlops-io/cheese-app-v4`, branch `main`, commit `033f18713b9e1e7985a3080e85edab3ff01cefef`, 2025-12-02 14:13:03 -0500 (the CD workflows used in L23)
- **README sections this lecture covers:**
  - Primary: [`#part-5-github-actions-remote-ci`](https://github.com/dlops-io/cheese-app-ci-cd/blob/main/README.md#part-5-github-actions-remote-ci) (README.md:277-365)
  - Context (L9 covered Parts 3-4): `#part-1-understanding-the-codebase` (51-92), `#part-2-identifying-code-quality-issues` (95-128), `#part-3-testing-with-pytest` (132-228), `#part-4-automating-with-pre-commit-hooks` (232-273)
  - Natural follow-ons that need a working Part 5: `#part-6-branch-protection-optional` (369-397), `#part-7-student-exercise---add-a-new-endpoint-with-full-ci` (401-453)
- **Colab notebooks:** none for this lecture.
- **Files read in full:** all 17 tracked files: `.github/workflows/ci.yml`, `.gitignore`, `.pre-commit-config.yaml`, `Dockerfile`, `README.md`, `assets/pipline.png`, `docker-entrypoint.sh`, `docker-shell.sh`, `pyproject.toml`, `pytest.ini`, `src/api-service/api/{__init__,service,utils}.py`, `tests/__init__.py`, `tests/{unit/test_utils,integration/test_api,system/test_system_api}.py`. I also read the full git history (14 commits), which includes a deleted second workflow (`docker-build.yml`) and the instructor's in-class demo commits.
- **How claims were checked:** every `path:line` below was checked with `sed -n`/`grep -n`. I ran Black 26.5.1 and Flake8 7.3.0 on a *copy* of `src/api-service/api/` to get real linter output. I did **not** run the repo's Dockerfile, scripts or tests. Claims I reasoned out but could not run are marked *(reasoned, not run)*.

---

## 1. What you build

You start with a tiny FastAPI service: three endpoints (`/`, `/health`, `/euclidean_distance/`), a `power()` helper, and 26 pytest tests at three levels (11 unit, 10 integration, 5 system). You get GitHub to check every push to `main`/`develop` and every pull request into them, with no one watching. The workflow file `.github/workflows/ci.yml` runs on GitHub-hosted Ubuntu VMs. It **builds the Docker image once**, tags it with the commit SHA and saves it as a tar. It then passes that tar as an **artifact** to four **parallel jobs**, each on its own fresh VM: Black/Flake8, unit tests with coverage, integration tests using FastAPI's `TestClient`, and system tests that start the real server in one container and call it over HTTP from a second container. A final **summary job** reads the three test jobs' results. If a `SLACK_WEBHOOK_URL` **repository secret** exists, it also posts to Slack. You see the outcome as green or red checks on your commits and PRs. Part 6 turns those checks into a merge gate. Nothing here touches GCP, so there is no cloud bill.

```
 YOUR LAPTOP (Docker Desktop)                           GITHUB.COM
 +-------------------------------------+                  +-------------------------------------+
 | cheese-app-ci-cd/ (git work tree)   |    git push      | repo <you>/cheese-app-ci-cd         |
 | pre-commit hooks run here (Part 4)  | ---------------> | .github/workflows/ci.yml  (at ROOT) |
 | sh docker-shell.sh ->               | (main/develop    | Settings > Secrets and variables >  |
 |   container cheese-app-api-service  |  or open a PR)   |   Actions: SLACK_WEBHOOK_URL (opt.) |
 |   uvicorn :9000 <-> localhost:9000  | <--------------- | checks: green/red on commit & PR    |
 +-------------------------------------+  status checks   +-------------------------------------+
                                                                            | event: push / pull_request
                                                                            v
 GITHUB ACTIONS  (each box = a brand-new ubuntu-latest VM, destroyed when its job ends)
 +------------------------------------------------------------+
 | build: checkout -> docker build -t cheese-app-api:<sha> .  |
 |        -> docker save -o /tmp/cheese-app-api.tar           |
 +------------------------------------------------------------+
                               | upload-artifact "docker-image" (kept 1 day)
                               v
             [ artifact store: docker-image = cheese-app-api.tar ]
          download-artifact + docker load, separately in EACH job below
          |                   |                  |                             |
          v                   v                  v                             v
 +-----------------+  +---------------+  +--------------+  +----------------------------------------+
 | lint-and-format |  | unit-tests    |  | integration- |  | system-tests                           |
 |  black --check  |  |  pytest unit  |  | tests        |  |  +--------------+  HTTP  +-----------+ |
 |  flake8 (soft)  |  |  pytest --cov |  |  pytest +    |  |  | api-server   |<-------| pytest    | |
 +-----------------+  |  -> artifact  |  |  TestClient  |  |  | uvicorn      | :9000  | system    | |
                      |  coverage-    |  |  (no server) |  |  | -p 9000:9000 |        | --network | |
                      |  report-unit  |  +--------------+  |  +--------------+        | host      | |
                      +---------------+                    |                          +-----------+ |
                                                           +----------------------------------------+
  (lint is NOT an input to test-summary)
                              |                  |                             |
                              +------------------+-----------------------------+
                                                      | needs.<job>.result: success / failure / skipped / cancelled
                                                      v
                                       +-------------------------------+
                                       | test-summary  (if: always())  | --- HTTPS POST, only if the secret is set ---> Slack
                                       +-------------------------------+
```

---

## 2. Prerequisites and costs

**Accounts**
- A GitHub account. Required: Actions only runs on a repo **you** can push to.
- Optional: a Slack workspace where you can create an app with an *Incoming Webhook*, to try the notification step.
- No GCP, no service accounts, no JSON keys. Of the late-course tutorials, this is the one that runs entirely outside GCP.

**Local installs** (README.md:5-9): Docker (Docker Desktop on macOS), Git, and Python 3.9+ with `pip`. Local Python is used to install `pre-commit` for Part 4 (README.md:240), and optionally for Part 2's Option B (`pip install black flake8`, README.md:118) and the "Run Locally Without Docker" commands (README.md:499-514). The image itself uses `python:3.11-slim-bookworm` (Dockerfile:2). It is a multi-arch base, so on Apple Silicon it builds natively as arm64, while CI builds amd64. The dependencies are pure-Python or ship wheels, so this tutorial has no architecture pitfalls.

**A repo where Actions will run.** The README only says "Clone or download from your repository" (README.md:19-20). GitHub runs workflows **only** from `.github/workflows/` at the **root** of a repository. Your options:
- **Fork** `dlops-io/cheese-app-ci-cd` on GitHub. On forks, Actions is disabled until you click the "enable workflows" button on the Actions tab.
- Create a new empty repo such as `<you>/cheese-app-ci-cd`, point your clone's `origin` at it, and push `main`.
- If you keep everything in one monorepo (for example `JunyiZhou-Conny/MLOps_Learning` with this project in a subfolder), `ci.yml` inside the subfolder will **never run**. You must move it to the monorepo's root `.github/workflows/` and adapt it (see §6, G2). Also, copying a `git clone` (with its own `.git/`) into another repo makes Git record an *embedded repository* (a gitlink), not the files.

**Secrets (optional).**
- `SLACK_WEBHOOK_URL` is a repository secret. Create it under repo **Settings → Secrets and variables → Actions → New repository secret**.
- It is read in two places:
  - the shell check at `.github/workflows/ci.yml:197`
  - the Slack action's environment at `.github/workflows/ci.yml:255-257`, together with `SLACK_WEBHOOK_TYPE: INCOMING_WEBHOOK`.
- Nothing in this repo reads secrets from disk. `.gitignore:48-52` ignores `secrets/`, `*.key`, `*.pem` and `.env` anyway, and the pre-commit hook `detect-private-key` (`.pre-commit-config.yaml:25-26`) is a second guard.
- The README never mentions the Slack step or this secret.

**Costs and what to shut down**
- **GitHub Actions minutes:**
  - On standard GitHub-hosted runners, public repos are free.
  - Private repos use your plan's included minutes. At the time of writing, GitHub Free includes 2,000 minutes per month; check Settings → Billing.
  - GitHub bills each *job* separately and rounds it **up** to a whole minute. A full run has 6 jobs, so it costs about **6 billed minutes** even though it finishes in about 2 minutes of wall-clock time (the README screenshot shows 54 s + 22/18/20/39 s + 4 s).
- **Artifact storage:**
  - Each run uploads the image tar `docker-image`, which is large because the image includes `build-essential` (Dockerfile:15-16). It is kept for 1 day (`ci.yml:38`).
  - Each run also uploads `coverage-report-unit` with the repo's default retention.
  - On private repos these count toward your plan's storage quota. You can delete old artifacts on each run page.
- **To stop CI:** Actions tab → "CI Pipeline" → "⋯" → *Disable workflow*, or delete the file.
- **Local cleanup** (README.md:568-574): `docker container ls`, stop leftovers (in particular `docker stop api-server && docker rm api-server`, README.md:199), `docker system prune`, `docker image ls`.
- **No billable cloud resources** are created.

---

## 3. Concepts this tutorial teaches

### C1. Workflow anatomy: event → workflow → jobs → steps   **[ANIMATE]**
- **Explanation:** A *workflow* is a YAML file in `.github/workflows/`. An *event* (`on:`), such as a push or a PR, starts a *run*. A run contains *jobs*, and each job is a list of *steps*. A step is either a shell script (`run:`) or a reusable *action* (`uses: actions/checkout@v4`).
- **Mental model:** A recipe card that GitHub executes whenever the doorbell (the event) rings. Jobs are separate cooks, and steps are the lines on each cook's card.
- **Analogy:** A restaurant ticket. The order comes in (event), the ticket (workflow) splits into stations (jobs), and each station follows its own checklist (steps).
- **Misconception:** "The workflow runs on my laptop" or "it runs once per file". It runs on GitHub's machines, once per triggering event, against the commit that event points to.
- **Animation:** A commit dot on a branch line emits a pulse. The YAML file unfolds into a tree: `on` at the root, six job nodes, each job expanding into its step list. Steps light up one by one.

### C2. Runners are disposable machines; jobs share nothing   **[ANIMATE]**
- **Explanation:** `runs-on: ubuntu-latest` asks for a fresh GitHub-hosted VM for **each job**. When the job ends, the VM is destroyed. Files, Docker images and environment variables do not carry over from one job to another. Within a job, steps share the same machine and filesystem.
- **Mental model:** Every job wakes up with amnesia in an empty room containing only Docker, Git and the tools GitHub pre-installs.
- **Analogy:** Hotel rooms. Housekeeping wipes everything between guests, so if you want something in the next room, you must carry it there.
- **Misconception:** "The image built in `build` is already there in `unit-tests`." It is not. That is why every downstream job has `Download Docker image` + `Load Docker image` steps (`ci.yml:49-57`, `78-86`, `113-121`, `136-144`).
- **Animation:** Six empty rooms appear. The build room fills its Docker shelf with an image. The camera moves to another room: the shelf is empty, and an arrow trying to reach across bounces off the wall.

### C3. Build once, test the same bits (artifact + SHA tag)   **[ANIMATE]**
- **Explanation:** The `build` job runs `docker build -t cheese-app-api:${{ github.sha }} .`, then `docker save` writes the image to a tar file, and `actions/upload-artifact@v4` stores it in GitHub (`ci.yml:25-38`). Each test job downloads the tar, runs `docker load`, and then runs the *same* image by the same tag. Tagging with the commit SHA makes the tag unique to that commit.
- **Mental model:** The image is a sealed, labelled suitcase. Every inspector opens an identical copy, so a pass in one job and a pass in another are statements about the *same* thing.
- **Analogy:** A factory makes a single prototype and ships identical copies of that finished prototype (not the blueprint) to four independent QA labs, so no lab rebuilds it. The blueprint is the Dockerfile; the prototype is the built image.
- **Misconception:** "CI checks the files I checked out." Here, lint and tests run **inside the image** against `/app/api` and `/app/tests`, which were copied in at build time (Dockerfile:38-41). The `actions/checkout` steps in the lint, integration and system jobs are not used by the checks themselves.
- **Second misconception:** "Docker Buildx gives us caching." Nothing caches between runs: there are no `cache-from`/`cache-to` settings, and each run rebuilds from scratch, including `apt-get upgrade` (Dockerfile:12-20).
- **Animation:** Image layers stack into a cube. The cube shrinks into a tar suitcase stamped with a SHA, flies to an "artifact shelf", and four copies fly into four rooms, where each one unpacks back into a cube.

### C4. The job graph: `needs`, fan-out/fan-in, result propagation, `if: always()`   **[ANIMATE]**
- **Explanation:**
  - With no `needs`, jobs start in parallel.
  - `needs: build` makes the four check jobs wait for `build` (`ci.yml:44, 73, 108, 131`). This is the fan-out.
  - `test-summary` has `needs: [unit-tests, integration-tests, system-tests]` (`ci.yml:175`). This is the fan-in.
  - Normally, a job whose dependency failed is *skipped*. `if: always()` (`ci.yml:176`) makes `test-summary` run anyway, so it can read `needs.<job>.result`, which is one of `success`, `failure`, `cancelled` or `skipped`.
  - The same idea applies to steps: a step is skipped after an earlier step fails, unless it says `if: always()` (`ci.yml:102, 161, 166`).
- **Mental model:** A directed acyclic graph (DAG). Time flows left to right, and the longest path (`build` 54 s → `system-tests` 39 s → `test-summary` 4 s in the screenshot) sets the run time.
- **Analogy:** A relay race with one runner handing off to four runners at once, and a judge at the finish who reads all four stopwatches even if some runners fell.
- **Misconception:** "`if: always()` means it will pass." It only means it will *run*. The summary step then decides pass or fail itself (`ci.yml:185-188`). A second misconception: "the summary covers everything." `lint-and-format` is **not** in the `needs` list, so a Black failure never reaches the summary or Slack.
- **Animation:** Draw the DAG from the YAML: each `needs:` line becomes an arrow. Then overlay a timeline (Gantt). Make one test node turn red: the arrow to `test-summary` stays solid because of `always()`, and the summary node evaluates the incoming tokens and turns red too.

### C5. Exit codes are the only language CI understands (formatter vs linter, `continue-on-error`)   **[ANIMATE]**
- **Explanation:** A step fails if and only if its command exits with a non-zero code. A failed step fails the job, which fails the run.
  - `black --check` exits 1 if any file *would be reformatted*. It is a formatter: it rewrites layout deterministically.
  - `flake8` exits 1 on style or quality violations. It is a linter: it reports, but does not fix.
  - The workflow makes Black **blocking** (`continue-on-error: false`, `ci.yml:62`) and Flake8 **advisory** (`continue-on-error: true`, `ci.yml:67`). An advisory step can fail while its job stays green.
- **Mental model:** Each step is a gate that emits 0 (open) or non-zero (closed). Red propagates upward from step to job to run.
- **Analogy:** A spell-checker that auto-corrects (Black) versus a proofreader's margin notes (Flake8).
- **Misconception:** "The lint job ran Flake8 and only Black complained." If Black fails, the Flake8 step is **skipped** (it has no `if: always()`), so on a messy commit you never see Flake8's output in CI.
- **Animation:** A row of gates. Black's gate shows "1" and slams shut, red climbs to the job box and then the run badge, and Flake8's gate greys out (skipped). In a second pass, flip `continue-on-error: true` on Black: its gate still shows "1", but a shunt carries the flow around it and the job stays green.

### C6. Test altitudes in CI: unit, integration, system (and "skip is not pass")
- **Explanation:**
  - *Unit* tests (`tests/unit/test_utils.py`) call `power()` directly.
  - *Integration* tests (`tests/integration/test_api.py:9-11`) call the FastAPI app in-process through `TestClient`, with no server and no network.
  - *System* tests (`tests/system/test_system_api.py`) make real HTTP calls to `http://localhost:9000`. CI starts the server container with `-p 9000:9000`, waits `sleep 10`, checks it with `curl -f`, and then runs the tests from a *second* container that shares the runner's network via `--network host` (`ci.yml:146-158`).
  - The system test class is decorated with `skipif(not is_api_running())` (`test_system_api.py:24`). If the server is unreachable, the four HTTP tests are **skipped**, and pytest still exits 0.
- **Mental model:** Each level up the pyramid swaps a fake for something real: a function call, then an in-process ASGI call, then a TCP connection to a separate process.
- **Analogy:** Testing a car's spark plug on a bench (unit), the engine on a stand (integration), and driving the car around the block (system).
- **Misconception:** "Green means the system tests ran." Without the `curl -f … || exit 1` guard (`ci.yml:154`), a server that never started would produce "1 passed, 4 skipped" and a green job.

### C7. Passing information around: step outputs, job results, job summaries
- **Explanation:**
  - A step writes `key=value` lines to the file named by `$GITHUB_OUTPUT` (`ci.yml:187, 191, 198, 200`). Later steps read them as `steps.<id>.outputs.<key>` (`ci.yml:204, 209`).
  - Jobs read other jobs' outcomes through `needs.<job>.result` (`ci.yml:181-185`).
  - What the code does **not** use is GitHub's *job summary* feature: Markdown appended to `$GITHUB_STEP_SUMMARY` shows up on the run's summary page. The "Test Summary" here is a *job*, and its report lives only in the job log (`echo` lines).
- **Mental model:** Steps pass sticky notes to later steps of the same job, jobs pass report cards to the jobs that `need` them, and `$GITHUB_STEP_SUMMARY` is the bulletin board on the run's front page.
- **Misconception:** "`echo` output appears on the run summary page." It appears only in the log. Exercise 4 adds a real job summary.

### C8. Secrets in Actions
- **Explanation:**
  - Repository secrets are stored encrypted, injected only at run time via `${{ secrets.NAME }}`, and **masked** as `***` in logs.
  - They are **not** given to workflows triggered by PRs from forks.
  - They cannot be referenced directly in `if:` conditions. The repo's own history shows this: commit `199abd9` tried `if: always() && secrets.SLACK_WEBHOOK_URL != ''`, and commit `1a5e363` replaced it with a separate step that tests the secret in shell and exports `enabled=true/false` (`ci.yml:194-201`) for the Slack step's `if:` (`ci.yml:204`).
- **Mental model:** A vault that lends a key to a specific job for its lifetime and blacks it out on every log page.
- **Analogy:** A hotel safe: the job can open it while checked in, and visitors (fork PRs) cannot.
- **Misconception:** "Masked means safe to interpolate anywhere." `${{ secrets.X }}` is pasted into the script text before bash runs. The more robust pattern passes it through `env:` and tests `"$SLACK_WEBHOOK_URL"` in shell. A related point: the step at `ci.yml:194-201` has no `if: always()`, so it is skipped when tests fail. As a result, the "❌ CI Pipeline Failed" Slack message can never be sent (see §6, G8).

---

## 4. Step-by-step walkthrough

Paths are relative to the repo root `cheese-app-ci-cd/`. Commands in fenced blocks are verbatim from the README unless labelled **(not in README)**.

### Step 0 — Put the repo somewhere Actions can run it (not in README)
- **Action:** fork `dlops-io/cheese-app-ci-cd`, or create an empty GitHub repo and push your clone to it. If you fork, open the **Actions** tab once and enable workflows.
- **Under the hood:** GitHub scans `.github/workflows/*.yml` at the repo root on every event.
- **Checkpoint:** the Actions tab lists a workflow called **CI Pipeline** (`ci.yml:5`).
- **If it fails:** no workflow is listed means the file is not at the repo root (monorepo case, §6 G2), or Actions is disabled on the fork or in Settings → Actions.

### Step 1 — Part 1: run the API locally (README.md:67-92, context)
```bash
sh docker-shell.sh
```
- **Under the hood:** `docker-shell.sh:7-18` builds an image named `cheese-app-api-service` and runs it interactively with `-p 9000:9000`. Passing `/bin/bash` as an argument makes the entrypoint `exec` a shell (`docker-entrypoint.sh:10-13`) after it puts `/home/app/.local/bin` on `PATH` (`docker-entrypoint.sh:5`).
- Inside the container:
```bash
uvicorn api.service:app --host 0.0.0.0 --port 9000 --reload
```
- **Checkpoint:**
  - `http://localhost:9000` → `{"message":"Welcome to the Cheese App CI/CD Tutorial!"}` (service.py:28-30)
  - `/health` → `{"status":"healthy"}` (service.py:33-35)
  - `/euclidean_distance/?x=3&y=4` → `distance` 5.0, plus a `"message"` field (service.py:38-50)
- **If it fails:**
  - "port is already allocated" means another container, often the `cheese-app-v2`/`v3` api-service, which also uses port 9000 and **the same image and container name** `cheese-app-api-service`, is still running. Stop it.
  - `--reload` does nothing useful here: the code is baked into the image and no volume is mounted, so after editing `src/` you must rerun `sh docker-shell.sh`.
- **Before Part 2:** the README says "Please exit and remove your container after this, before starting with the next Part" (README.md:92). Type `exit`. `docker-shell.sh` runs the container with `--rm` (`docker-shell.sh:15`), so exiting removes it and frees port 9000.

### Step 2 — Part 2: see the lint and format problems (README.md:95-128, context)
```bash
# Build the image first
docker build -t cheese-app-api:local .

# Check code quality
docker run --rm cheese-app-api:local flake8 --max-line-length=120 api/

# Check formatting with diff
docker run --rm cheese-app-api:local black --check --diff api/
```
- **Under the hood:**
  - The Dockerfile copies `pyproject.toml` first and runs `pip install --user .`. This installs every dependency, including black, flake8, pytest and pre-commit, into the image (Dockerfile:32-35; pyproject.toml:7-19).
  - It then copies `src/api-service/api/` to `/app/api` and `tests/` to `/app/tests` (Dockerfile:38-41).
  - Any arguments after the image name replace the default server command (`docker-entrypoint.sh:10-13`).
- **Checkpoint:** after the entrypoint banner lines `Container is running!!!` and `Executing command: …`, Flake8 prints (I verified this with flake8 7.3.0 on a copy of the code):
  ```
  api/utils.py:7:15: E231 missing whitespace after ','
  api/utils.py:13:1: E303 too many blank lines (3)
  ```
  `black --check --diff api/` uses Black's **default 88-column** limit here. It reports *two* files: `utils.py` (`def power(base,exponent):` and an extra blank line) and `service.py`, because line 15 is 95 characters long. CI uses 120 columns and flags only `utils.py`.
- **README vs code:**
  - Option B's local commands `flake8 src/api-service/api/` and `black --check --diff src/api-service/api/` (README.md:121, 124) use the defaults of 79 and 88 columns, so they also flag `service.py:15:80: E501 line too long (95 > 79 characters)`. CI never flags that line.
  - Neither `pyproject.toml` nor a `.flake8` file sets these limits; only the command lines do.

### Step 3 — Part 3: run tests in Docker (README.md:159-228, context from L9)
```bash
# Run unit tests only
docker run --rm cheese-app-api:local pytest tests/unit/ -v

# Run integration tests only
docker run --rm cheese-app-api:local pytest tests/integration/ -v
```
- **Under the hood:** `pytest.ini:9` sets `pythonpath = .`, which is `/app` in the image, so `from api.utils import power` works. `addopts` adds `-v --tb=short --strict-markers --disable-warnings -ra` (pytest.ini:12-17).
- **Checkpoint:** 11 unit tests (`tests/unit/test_utils.py`) and 10 integration tests (`tests/integration/test_api.py`) collected and passing. I counted these from source and did not run them.
- The same README block also runs both folders together (README.md:178) and a terminal coverage report (README.md:181):
```bash
# Run both unit and integration tests
docker run --rm cheese-app-api:local pytest tests/unit/ tests/integration/ -v

# Run with coverage
docker run --rm cheese-app-api:local pytest tests/unit/ --cov=api --cov-report=term
```
  The coverage table lists `service.py` at 0%, because `--cov=api` covers the whole package and unit tests never import `service.py` (see E6).
- System tests need a live server:
```bash
# Start the API server
docker run -d --name api-server -p 9000:9000 -e DEV=1 cheese-app-api:local

# Run system tests against the live server
docker run --rm --network host cheese-app-api:local pytest tests/system/ -v

# Clean up when done
docker stop api-server && docker rm api-server
```
- **Checkpoint:** 5 passed. If you instead see `1 passed, 4 skipped` with the reason `API not running at localhost:9000`, the test container could not reach the server (test_system_api.py:15-24).
- **If it fails:**
  - On Docker Desktop, host networking behaves differently from Linux. A robust local alternative **(not in README)**: `docker run --rm --network container:api-server cheese-app-api:local pytest tests/system/ -v`, which joins the server container's own network namespace, so `localhost:9000` *is* the server.
  - "Conflict. The container name "/api-server" is already in use" means a previous run never cleaned up. Run `docker rm -f api-server` **(not in README)**.
- **Option 3 (README.md:204-228):** the same `pytest` commands typed inside `sh docker-shell.sh`. `pytest tests/unit/ --cov=api --cov-report=html` (README.md:225) writes `htmlcov/` *inside* the `--rm` container, so the report is gone when you exit.

### Step 4 — Part 4: pre-commit (README.md:232-273, context)
```bash
pip install pre-commit
```
```bash
# From the root directory
pre-commit install
```
```bash
# Run on all files
pre-commit run --all-files
```
- The README also shows the two other ways the hooks run (README.md:253-266): automatically on `git commit -m "Your commit message"`, or manually on staged files only with `pre-commit run`.
- **Under the hood:** `.pre-commit-config.yaml` pins the following:
  - generic hooks at `v4.5.0` (lines 9-26)
  - Black `24.1.1` with `--line-length 120` on `^src/.*\.py$` (lines 29-35)
  - Flake8 `7.0.0` with `--max-line-length=120 --extend-ignore=E203,W503` (lines 38-44)

  These are the same flags CI uses (`ci.yml:61, 66`).
- **Checkpoint:** the Black hook reports *Failed* with "files were modified by this hook" and rewrites `src/api-service/api/utils.py`. Run the hooks again and everything passes.
- **Decision for the video:** **don't commit that fix yet** if you want to watch CI catch the problem in Step 9. Run `git stash` or `git checkout -- src/api-service/api/utils.py` **(not in README)** to undo the rewrite.

### Step 5 — Part 5: read the trigger block (README.md:281-283)
- **File:** `.github/workflows/ci.yml:5-11`. The run is called "CI Pipeline". It fires on `push` to `main` or `develop`, and on `pull_request` whose *base* is `main` or `develop`.
- **Under the hood:**
  - A push to `feature/x` triggers nothing until you open a PR into `main`.
  - For `pull_request` runs, `github.sha` is the SHA of a temporary **merge commit** (your PR merged into the base). That merged code is what gets built and tested.
- **README vs code:** the README (283) correctly says `main` and `develop`, while the comment at `ci.yml:2` says only "main branch".

### Step 6 — The `build` job (README.md:289-294; ci.yml:15-38)
- **What it does:**
  - checkout (`ci.yml:19-20`)
  - `docker/setup-buildx-action@v3` (`22-23`)
  - `docker build -t cheese-app-api:${{ github.sha }} .` (`25-27`)
  - `docker save … -o /tmp/cheese-app-api.tar` (`29-31`)
  - upload as artifact `docker-image` with `retention-days: 1` (`33-38`)
- **Checkpoint (in the run log):** the Docker build output ends successfully, and the artifact `docker-image` is listed on the run page. The README screenshot shows this job at 54 s (`assets/pipline.png`).
- **If it fails:** `pip install` errors usually mean a dependency problem in `pyproject.toml`. Network flakiness during `apt-get upgrade` (Dockerfile:12-20) can be fixed by re-running the job.
- **README vs code:** "Uses Docker Buildx for efficient caching" (README.md:291). There is no cache configuration, so every run rebuilds every layer.

### Step 7 — The `lint-and-format` job (README.md:296-301; ci.yml:41-67)
- **What it does:** `needs: build`, downloads and loads the tar (`49-57`), then runs:
  - `black --check --line-length 120 api/`, blocking (`59-62`)
  - `flake8 --max-line-length=120 --extend-ignore=E203,W503 api/`, advisory (`64-67`)
- **Checkpoint at the current commit:** **this job fails.** `src/api-service/api/utils.py:7` (`def power(base,exponent):`) and the triple blank line at `utils.py:10-12` make Black print `would reformat …/api/utils.py` and `1 file would be reformatted, 2 files would be left unchanged.`, then exit 1. I reproduced this on a copy with Black 26.5.1. The Flake8 step is then **skipped**.

### Step 8 — The `unit-tests` job (README.md:303-308; ci.yml:70-102)
- **What it does:**
  - `pytest tests/unit/ -v --tb=short` (`88-90`). This is the gate.
  - A second, advisory pytest run with coverage, which mounts `${{ github.workspace }}/coverage` onto `/app/coverage` and writes the HTML report there (`92-95`).
  - Uploads `coverage/` as artifact `coverage-report-unit`, even after failures (`97-102`).
- **Checkpoint:** 11 passed, and a coverage table in the log.
- **README vs code:** README.md:307-308 promises terminal, XML and HTML reports, all uploaded.
  - The XML report is written to `/app/coverage.xml` *inside* the container, which `--rm` deletes, so it never reaches the runner.
  - *(Reasoned, not run.)* Docker creates the missing host directory `coverage/` as root, while the container runs as uid 1000 (Dockerfile:23-28). The HTML write is therefore likely to hit a permission error, which `continue-on-error` hides, and the upload then warns that no files were found. Check your own run's log. Exercise 6 has a fix.

### Step 9 — The `integration-tests` job (README.md:310-314; ci.yml:105-125)
- **What it does:** `pytest tests/integration/ -v --tb=short` (`123-125`) runs inside the image. `TestClient(app)` (test_api.py:11) calls the ASGI app in-process, so no port is involved.
- **Checkpoint:** 10 passed.

### Step 10 — The `system-tests` job (README.md:316-323; ci.yml:128-169)
- **What it does:**
  - Starts `api-server` detached in DEV mode. With no command arguments, the entrypoint starts `uvicorn … --reload --log-level debug` (docker-entrypoint.sh:16-19).
  - `sleep 10`, then `curl -f http://localhost:9000/ || exit 1` (`150-154`).
  - Runs the tests from a second container with `--network host` (`156-158`).
  - Always prints the server logs and always stops and removes the server (`160-169`).
- **Checkpoint:** 5 passed. The "Show server logs" step shows `Running in DEV mode` and uvicorn access lines for `/health`, `/` and `/euclidean_distance/`.
- **If it fails:** a `curl: (7) Failed to connect` in the wait step means the server needed more than 10 s or crashed. Read the logs step, which runs because of `if: always()`.

### Step 11 — The `test-summary` job (README.md:325-330; ci.yml:172-257)
- **What it does:**
  - `needs` the three test jobs and runs `if: always()`.
  - Echoes the three results, writes `status=success|failure` to `$GITHUB_OUTPUT`, and exits 1 if any result is not `success` (`178-192`).
  - Checks whether the secret exists (`194-201`) and, if so, posts a Block-Kit message through `slackapi/slack-github-action@v1.26.0` (`203-257`).
- **Checkpoint at the current commit:** the log shows the three results as `success`, then `✅ All tests passed!`. The Slack step is skipped unless you added the secret.
- **README vs code:** the README (325-330) does not mention Slack at all, and "Checks the results of all test jobs" omits that lint is not checked.

### Step 12 — Push (README.md:344-349)
```bash
git add .
git commit -m "Add CI pipeline"
git push
```
- **Checkpoint:** within seconds, a yellow dot appears next to the commit on GitHub, and the Actions tab shows a run named after the commit message.
- **If nothing starts:** you pushed a branch other than `main`/`develop`, or the workflow is not at the repo root.
- **Gotcha:** `git add .` also stages anything you generated locally that `.gitignore` misses. For example, a `coverage/` folder is not ignored; for coverage output, `.gitignore:29-35` covers only `.coverage`, `htmlcov/`, `*.cover` and `coverage.xml`.

### Step 13 — Watch the run (README.md:351-365)
- **Action:** Actions tab → the run → the graph view.
- **What you should see at commit `b8458ff`:**
  - Build Docker Image ✓
  - **Lint and Format Check ✗** (Black)
  - Unit Tests ✓, Integration Tests ✓, System Tests ✓
  - Test Summary ✓
  - **Overall run ✗**

  This does **not** match the all-green screenshot `assets/pipline.png`. That screenshot was committed in `3dea317`, when both `utils.py` and `service.py` were in their messy state (since `91eb786`), so it comes from another code state. It is consistent with the clean code before `91eb786`: Black 120 and Flake8 both pass on the `140f138` versions of `src/api-service/api/` (I checked copies), while the `3dea317` versions fail both.
- **Checkpoint:** you can click into each job and read every step's log. The artifacts are listed at the bottom of the run summary page.

### Step 14 — Turn it green (not spelled out in the README)
- **Option A:** run `pre-commit run --all-files` (README.md:262), then commit the rewritten `utils.py` and push.
- **Option B (not in README):** run Black inside the image, mounting only the `api` folder:
  ```bash
  docker run --rm -v "$(pwd)/src/api-service/api":/app/api cheese-app-api:local black --line-length 120 api/
  ```
  This needs the `cheese-app-api:local` image from Step 2. Black runs as uid 1000 inside the container and writes to your host files. On Docker Desktop (macOS) that works; on a Linux host whose user is not uid 1000 the write fails with a permission error *(reasoned, not run)*, so use Option A or C there.
- **Option C:** edit by hand. Change the signature to `def power(base, exponent):` and delete one of the three blank lines.
- **Checkpoint:** after the push, all six jobs are green, which now matches the screenshot.

### Step 15 — (Optional) Slack notifications
1. Create a Slack app with Incoming Webhooks and copy the webhook URL.
2. In the repo, go to Settings → Secrets and variables → Actions → New repository secret, name it `SLACK_WEBHOOK_URL`, and paste the URL.
3. Re-run the workflow.

- **Checkpoint:** a Slack message headed "✅ CI Pipeline Passed", with repository, branch, commit, author, per-test results and links (`ci.yml:207-254`).
- **Known bug:** when tests fail, *no* message is sent (§6 G8).
- **Known bug:** on PR runs, the "View Commit" link is empty, because `github.event.head_commit` exists only for push events. On the same runs the "Branch" field (`github.ref_name`, `ci.yml:227`) shows `<PR number>/merge` rather than your branch name.

### Step 16 — Part 6: branch protection (README.md:369-397), with fixes
- **Action:** Settings → Branches → add a rule for `main`, requiring a PR and passing status checks. GitHub's current UI labels this "Add classic branch protection rule" or offers "rulesets".
- **Choosing the checks:** the README says to select `lint-and-format`, `unit-tests`, … (README.md:378). Those are job **IDs**. The status checks GitHub lists use each job's **`name:`**:
  - `Lint and Format Check` (`ci.yml:42`)
  - `Unit Tests` (`71`)
  - `Integration Tests` (`106`)
  - `System Tests` (`129`)

  Checks appear in the picker only after they have run at least once.
- **Do Step 14 first.** If `Lint and Format Check` is required while `utils.py` is still messy, every PR is blocked by Black regardless of what the PR changes.
- **Plan limits:** protected branches on **private** repos need a paid plan (Pro, Team, …). On GitHub Free they are available for public repos.
- **The README's "break the tests" command doesn't break anything:**
```bash
echo "def broken(): assert False" >> tests/unit/test_utils.py
```
  `broken` does not match `python_functions = test_*` (pytest.ini:8), so pytest never collects it, and the PR stays green. Use **(not in README)** `echo "def test_broken(): assert False" >> tests/unit/test_utils.py`.
- **Also note:** pushing `feature/test-protection` triggers nothing (push filter). The run starts when you open the PR (`pull_request` into `main`).

### Step 17 — Part 7: add `/add/` with tests (README.md:401-453)
- **Action:** add the endpoint snippet to `service.py` and the test function to `test_api.py` (README.md:405-419). Add `test_add_endpoint` at module level (it has no `self`), like `test_api_health_check`. Then rebuild, because code and tests are baked into the image, and run:
```bash
# Build the image first
docker build -t cheese-app-api:local .

# Run all tests
docker run --rm cheese-app-api:local pytest tests/ -v
```
- **Checkpoint:** all unit and integration tests pass, now including `test_add_endpoint`. The system tests show 1 passed and 4 skipped, because no server is running.
- **Then (README.md:445-453):** `git add .`, `git commit -m "Add addition endpoint with tests"`, `git push`, and watch the run.
- **README auto-format command is broken:**
```bash
docker run --rm -v $(pwd)/src/api-service:/app cheese-app-api:local black --line-length 120 api/
```
  It mounts `src/api-service` (which contains only `api/`) **over `/app`**. That hides `/app/docker-entrypoint.sh`, which the relative `ENTRYPOINT ["/bin/bash", "docker-entrypoint.sh"]` (Dockerfile:52) needs, so bash fails with "docker-entrypoint.sh: No such file or directory" *(reasoned, not run)*. Use the Step 14 Option B command instead.

### Step 18 — Clean up (README.md:568-574)
- **Action:** `docker container ls`, stop leftovers (`api-server`, `cheese-app-api-service`), `docker system prune`, `docker image ls`.
- **Optional:** disable the workflow on GitHub if you don't want CI minutes used on a private repo.

---

## 5. Code tour

```
cheese-app-ci-cd/
├── .github/workflows/ci.yml        # THE lecture: 6-job CI pipeline (build → 4 checks → summary + Slack)
├── .pre-commit-config.yaml         # local mirror of CI's checks (Black/Flake8 @120 cols + hygiene hooks)
├── Dockerfile                      # python:3.11-slim image; non-root 'app'; bakes code + tests into /app
├── docker-entrypoint.sh            # args → exec them; no args → uvicorn (DEV=1: --reload, else 4 workers)
├── docker-shell.sh                 # local: build 'cheese-app-api-service' and open a bash shell, port 9000
├── pyproject.toml                  # unpinned deps: fastapi, uvicorn, pytest(+cov,+asyncio), black, flake8…
├── pytest.ini                      # testpaths, pythonpath=., default flags (-v --tb=short -ra …)
├── src/api-service/api/
│   ├── service.py                  # FastAPI app: /, /health, /euclidean_distance/
│   └── utils.py                    # power(); intentionally mis-formatted (makes Black fail)
├── tests/unit/test_utils.py        # 11 tests of power()
├── tests/integration/test_api.py   # 10 tests through TestClient (in-process)
├── tests/system/test_system_api.py # 5 tests; 4 hit http://localhost:9000 (skip if down)
└── assets/pipline.png              # screenshot of an all-green run graph
```

**`.github/workflows/ci.yml:5-11`**
```yaml
name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
```
- `name` is the label you see in the Actions sidebar.
- `on.push.branches` filters by the branch you pushed **to**.
- `on.pull_request.branches` filters by the PR's **base** branch. The default PR activity types are opened, synchronize (new commits) and reopened.

**`.github/workflows/ci.yml:25-38`**
```yaml
      - name: Build Docker image
        run: |
          docker build -t cheese-app-api:${{ github.sha }} .

      - name: Save Docker image
        run: |
          docker save cheese-app-api:${{ github.sha }} -o /tmp/cheese-app-api.tar

      - name: Upload Docker image artifact
        uses: actions/upload-artifact@v4
        with:
          name: docker-image
          path: /tmp/cheese-app-api.tar
          retention-days: 1
```
- `${{ … }}` is an expression GitHub substitutes *before* the shell runs. `github.sha` is the 40-character commit (or merge-commit) SHA.
- `docker save` serialises all image layers and metadata into a single tar.
- `upload-artifact@v4` stores it under the run with the name `docker-image`. `retention-days: 1` keeps storage low, but it also means that re-running a single failed job more than a day later cannot download the image (§6 G13).

**`.github/workflows/ci.yml:43-57`**
```yaml
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Download Docker image
        uses: actions/download-artifact@v4
        with:
          name: docker-image
          path: /tmp

      - name: Load Docker image
        run: |
          docker load -i /tmp/cheese-app-api.tar
```
- `needs: build` means: wait for `build`, and skip this job if `build` failed.
- `download-artifact@v4` with a `name` extracts the files straight into `path`, so `/tmp/cheese-app-api.tar` reappears on this VM.
- `docker load` restores the image with its original tag, `cheese-app-api:<sha>`.
- This same 15-line block is copy-pasted into four jobs. That is a natural candidate for a composite action or a reusable workflow later.

**`.github/workflows/ci.yml:59-67`**
```yaml
      - name: Run Black formatter check
        run: |
          docker run --rm cheese-app-api:${{ github.sha }} black --check --line-length 120 api/
        continue-on-error: false

      - name: Run Flake8 linter
        run: |
          docker run --rm cheese-app-api:${{ github.sha }} flake8 --max-line-length=120 --extend-ignore=E203,W503 api/
        continue-on-error: true
```
- `api/` resolves to `/app/api`, the WORKDIR (Dockerfile:29), so the checks lint the image's copy of the code.
- `--check` makes Black report instead of rewrite, exiting 1 if anything would change.
- `E203` (whitespace before `:`, e.g. in slices) and `W503` (line break before a binary operator) are the classic pycodestyle rules that conflict with Black's style. `W503` is already in Flake8's default ignore list, and `--extend-ignore` keeps that list, so in practice only `E203` changes anything here.
- `continue-on-error: false` is the default, written out for teaching. `true` lets Flake8 fail without failing the job, though Flake8 only runs at all if Black passed.

**`.github/workflows/ci.yml:88-102`**
```yaml
      - name: Run unit tests
        run: |
          docker run --rm cheese-app-api:${{ github.sha }} pytest tests/unit/ -v --tb=short

      - name: Generate coverage report
        run: |
          docker run --rm -v ${{ github.workspace }}/coverage:/app/coverage cheese-app-api:${{ github.sha }} pytest tests/unit/ --cov=api --cov-report=term --cov-report=xml --cov-report=html:coverage
        continue-on-error: true

      - name: Upload coverage report
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report-unit
          path: coverage/
        if: always()
```
- The first step is the real gate.
- The second step runs the unit tests **again**, now measuring `api` with pytest-cov:
  - `term` prints a table.
  - `xml` writes `/app/coverage.xml`, which is not mounted and therefore lost.
  - `html:coverage` writes into the bind-mounted folder.
- Because `--cov=api` points at the package directory, coverage also lists files the unit tests never import (`service.py` at 0%).
- `if: always()` uploads even after a failure, which is good practice for diagnostics.

**`.github/workflows/ci.yml:146-158`**
```yaml
      - name: Start API server container
        run: |
          docker run -d --name api-server -p 9000:9000 -e DEV=1 cheese-app-api:${{ github.sha }}

      - name: Wait for server to be ready
        run: |
          echo "Waiting for server to start..."
          sleep 10
          curl -f http://localhost:9000/ || exit 1

      - name: Run system tests
        run: |
          docker run --rm --network host cheese-app-api:${{ github.sha }} pytest tests/system/ -v --tb=short
```
- `-d` detaches.
- `-p 9000:9000` publishes the container port on the runner's port 9000.
- `-e DEV=1` selects the `--reload` branch of the entrypoint.
- `curl -f` turns an HTTP error or connection failure into a non-zero exit, so the readiness check is a *gate*. `sleep 10` is a fixed guess; a retry loop is more robust (Exercise 7).
- `--network host` puts the test container in the runner's network namespace, so `localhost:9000` reaches the published port.

**`.github/workflows/ci.yml:174-187`**
```yaml
    runs-on: ubuntu-latest
    needs: [unit-tests, integration-tests, system-tests]
    if: always()
    steps:
      - name: Check test results
        id: test-results
        run: |
          echo "Unit Tests: ${{ needs.unit-tests.result }}"
          echo "Integration Tests: ${{ needs.integration-tests.result }}"
          echo "System Tests: ${{ needs.system-tests.result }}"

          if [ "${{ needs.unit-tests.result }}" != "success" ] || [ "${{ needs.integration-tests.result }}" != "success" ] || [ "${{ needs.system-tests.result }}" != "success" ]; then
            echo "❌ Some tests failed!"
            echo "status=failure" >> $GITHUB_OUTPUT
```
- The fan-in job. `if: always()` makes it run even when a dependency failed or was skipped. If `build` fails, all three are `skipped`, which is "not success", so the summary also fails.
- `id: test-results` names the step so later steps can read `steps.test-results.outputs.status`.
- `echo "key=value" >> $GITHUB_OUTPUT` is the current way to set a step output; the old `::set-output` command is deprecated.
- The step finishes with `exit 1` (line 188), which fails the job and makes it visibly red.
- `lint-and-format` is absent from `needs`, so formatting failures are invisible to this job.

**`.github/workflows/ci.yml:194-205`**
```yaml
      - name: Check if Slack webhook is configured
        id: slack-check
        run: |
          if [ -n "${{ secrets.SLACK_WEBHOOK_URL }}" ]; then
            echo "enabled=true" >> $GITHUB_OUTPUT
          else
            echo "enabled=false" >> $GITHUB_OUTPUT
          fi

      - name: Send Slack notification
        if: always() && steps.slack-check.outputs.enabled == 'true'
        uses: slackapi/slack-github-action@v1.26.0
```
- `if:` cannot read `secrets` directly, so this step converts "secret present?" into an ordinary step output.
- An unset secret expands to the empty string, which makes `-n` false.
- **Bug:** this check step has no `if: always()`. When the previous step exits 1, it is skipped, its output is empty, and the Slack step's condition is false, so failures are never announced.
- The action version `v1.26.0` uses the `SLACK_WEBHOOK_URL`/`SLACK_WEBHOOK_TYPE` env interface (`ci.yml:255-257`). Newer major versions changed their inputs.

**`Dockerfile:27-41`**
```dockerfile
# Switch to non-root user
USER app
WORKDIR /app

# Copy pyproject.toml first for better caching
COPY --chown=app:app pyproject.toml ./

# Install Python dependencies
RUN pip install --no-cache-dir --user .

# Copy application code
COPY --chown=app:app src/api-service/api/ ./api/
COPY --chown=app:app tests/ ./tests/
COPY --chown=app:app pytest.ini ./
COPY --chown=app:app docker-entrypoint.sh ./
```
- The image runs as the non-root user `app` (uid 1000, Dockerfile:23).
- Copying `pyproject.toml` before the code means a code-only change reuses the dependency layer. This helps locally, but CI rebuilds from scratch every run anyway.
- `pip install --user .` puts console scripts in `/home/app/.local/bin`. That folder is not on PATH by default, which is why the entrypoint exports it (`docker-entrypoint.sh:5`).
- Tests are **baked into the image**. That is why CI can run `pytest tests/...` with no mount.

**`docker-entrypoint.sh:10-24`**
```bash
if [ $# -gt 0 ]; then
  echo "Executing command: $@"
  exec "$@"
fi

# Otherwise, start the server
if [ "${DEV}" = "1" ]; then
  echo "Running in DEV mode"
  # Development: auto-reload on code changes
  uvicorn api.service:app --host 0.0.0.0 --port 9000 --reload --log-level debug
else
  echo "Running in PROD mode"
  # Production: optimized settings
  uvicorn api.service:app --host 0.0.0.0 --port 9000 --workers 4
fi
```
- This one script makes the same image serve every role in CI:
  - with arguments, it is a tool runner (`pytest …`, `black …`, `flake8 …`)
  - with no arguments, it is a server
- `exec` replaces bash, so the tool's exit code becomes the container's exit code, which becomes the step's exit code. That chain is exactly what CI needs.
- Note the different meaning of `DEV` compared with `cheese-app-v3`, where `DEV=1` drops you into a shell (§7).

**`tests/system/test_system_api.py:12-24`**
```python
API_BASE_URL = "http://localhost:9000"


def is_api_running():
    """Check if API is accessible"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False


@pytest.mark.skipif(not is_api_running(), reason="API not running at localhost:9000")
```
- The URL is hard-coded.
- `is_api_running()` runs at **import or collection time**, once.
- The bare `except:` swallows every error, including DNS errors and timeouts.
- `skipif` turns "server down" into *skipped*, which pytest does not count as a failure. CI compensates with the `curl -f` gate.

**`src/api-service/api/utils.py:7-14`**
```python
def power(base,exponent):
    """Calculate base raised to the power of exponent"""
    return base**exponent



def unused_function():
    pass
```
- This is the deliberately messy code. It was re-added in commit `91eb786` ("readd messy code").
- Line 7 has a missing space after the comma (Flake8 E231, a Black rewrite). Lines 10-12 hold three blank lines (Flake8 E303, a Black rewrite).
- `unused_function` is dead code that neither tool flags. Flake8 reports unused *imports*, not unused functions.
- This file alone makes the lint job red at HEAD.

---

## 6. Gotchas and common errors

| # | Symptom | Cause | Fix |
|---|---|---|---|
| G1 | First run is red. "Lint and Format Check" fails at "Run Black formatter check" with `would reformat …/api/utils.py`, and Flake8 shows as skipped. | `src/api-service/api/utils.py:7` and `:10-12` are intentionally not Black-formatted. Black is blocking (`ci.yml:62`). | Run `pre-commit run --all-files` (README.md:262) or the mount command in §4 Step 14, then commit and push. |
| G2 | You pushed and **no run appears**. | One of three things: (a) the workflow is not at the repo root, e.g. it sits in `MLOps_Learning/<subfolder>/.github/workflows/`; (b) you pushed a branch other than `main`/`develop` (`ci.yml:7-11`); (c) Actions is disabled on a fork. | (a) Move it to the root `.github/workflows/`. Add `defaults: run: working-directory: <subfolder>` so `docker build … .` uses the right context, and optionally `on.push.paths: ['<subfolder>/**']`. The `-v ${{ github.workspace }}/coverage` mount and the `path: coverage/` upload both resolve to the workspace root, so they stay consistent. (b) Push to `main` or open a PR. (c) Enable workflows on the Actions tab. |
| G2b | In the monorepo, `pre-commit` never reformats `utils.py`, or the commit hook says no config was found *(reasoned, not run)*. | pre-commit works from the **git root**: the installed hook looks for `.pre-commit-config.yaml` there, and the `files: ^src/.*\.py$` patterns (`.pre-commit-config.yaml:35, 44`) are matched against paths relative to the root, so `<subfolder>/src/...` never matches. | Put one `.pre-commit-config.yaml` at the monorepo root with patterns like `^<subfolder>/src/.*\.py$`, or keep this project in its own repo. |
| G3 | `git add` warns "adding embedded git repository" and the files never reach GitHub. | You copied a `git clone` (with its `.git/`) into another repo, such as the monorepo. | Remove the inner `.git`, or use `git subtree`/a separate repo. A submodule's own workflows will not run in the parent. |
| G4 | README Part 7 auto-format fails: `bash: docker-entrypoint.sh: No such file or directory` *(reasoned, not run)*. | `-v $(pwd)/src/api-service:/app` (README.md:442) hides `/app/docker-entrypoint.sh`, which the relative ENTRYPOINT (Dockerfile:52) needs. | Mount only the package: `docker run --rm -v "$(pwd)/src/api-service/api":/app/api cheese-app-api:local black --line-length 120 api/`. |
| G5 | Part 6's "break the tests" PR is still green. | `def broken()` is never collected because `python_functions = test_*` (pytest.ini:8). | Append `def test_broken(): assert False` instead. |
| G6 | You can't find `lint-and-format`/`unit-tests` in the required-checks picker. | The checks are listed under the jobs' `name:` (`ci.yml:42, 71, 106, 129`), and only after they have run at least once. Private repos on GitHub Free cannot use protected branches. | Search for "Unit Tests", "Integration Tests", "System Tests", "Lint and Format Check". Make the repo public or use GitHub Pro (free via the Student Developer Pack). |
| G7 | The `coverage-report-unit` artifact is missing or empty ("No files were found with the provided path: coverage/") *(reasoned, not run)*. | Docker creates the missing host dir `coverage/` as root, while the container user is uid 1000 (Dockerfile:23-28), so the HTML write fails, hidden by `continue-on-error: true` (`ci.yml:95`). `coverage.xml` is written to `/app` inside the container and discarded. On Docker Desktop for Mac, bind-mount ownership is relaxed, so the same command may work locally. | Add a step `mkdir -p coverage && chmod 777 coverage` before the run, and write XML into the mount: `--cov-report=xml:coverage/coverage.xml`. Optionally drop `continue-on-error` so problems are visible. |
| G8 | Slack only ever says "✅ Passed"; failures are silent. | "Check test results" exits 1 (`ci.yml:188`), so "Check if Slack webhook is configured" (`194-201`), which has no `if:`, is skipped. `steps.slack-check.outputs.enabled` is then empty and the Slack condition (`204`) is false. | Add `if: always()` to the `slack-check` step. Better still, pass the secret via `env:` and test `"$SLACK_WEBHOOK_URL"` in shell. |
| G9 | Slack step is skipped on PRs from forks, or the "View Commit" link is broken. | Secrets are not provided to workflows triggered from forks. `github.event.head_commit` exists only on `push` events (`ci.yml:231, 250`). | Expected behaviour. For links, use `${{ github.server_url }}/${{ github.repository }}/commit/${{ github.sha }}`. |
| G10 | The run is red but the summary job (and Slack) say "All tests passed". | `test-summary` `needs` only the three test jobs (`ci.yml:175`); lint is not included. | Add `lint-and-format` to `needs` and to the check (Exercise 4). |
| G11 | Local Black/Flake8 disagree with CI. | Local commands use the default 88/79 columns: README.md:112, 121, 124, 495-496, 502-504, 528-531. CI uses 120 (`ci.yml:61, 66`). There is no `[tool.black]` in `pyproject.toml`. | Always pass `--line-length 120` / `--max-line-length=120`, or add `[tool.black]\nline-length = 120` to `pyproject.toml` and a `.flake8` file. |
| G12 | Pre-commit passes locally but CI's Black fails, or vice versa. | Pre-commit pins Black `24.1.1` (`.pre-commit-config.yaml:30`). The image installs whatever is newest that satisfies `black>=24.1.1` (pyproject.toml:8), so the two drift as Black's yearly style changes land. README.md:564 hints at this. | Pin the same version in both places, or lock the dependencies. |
| G13 | "Re-run failed jobs" the next day fails at "Download Docker image". | The image artifact expires after 1 day (`ci.yml:38`). | Use "Re-run all jobs", or raise the retention. |
| G14 | `Bind for 0.0.0.0:9000 failed: port is already allocated`, or the container name `cheese-app-api-service` is already in use. | `docker-shell.sh:7, 15-18` uses the **same image name, container name and port** as `cheese-app-v2`/`v3`'s `src/api-service/docker-shell.sh` (lines 7, 20, 23, 27 there). A leftover `api-server` from README.md:193 also holds 9000. | `docker ps`, then stop or remove the other container. Building here also overwrites the `cheese-app-api-service:latest` tag used by v2/v3, so rebuild that one before going back to it. |
| G15 | You edit `service.py`, but the server started with `--reload` in `docker-shell.sh` doesn't change. | No volume is mounted (`docker-shell.sh:15-18`); the code is baked into the image (Dockerfile:38). | Rerun `sh docker-shell.sh`, which rebuilds the image, or add `-v "$(pwd)/src/api-service/api":/app/api` yourself. |
| G16 | System tests show "1 passed, 4 skipped" and the job is green. | The server is unreachable from the test container, and `skipif` (test_system_api.py:24) hides it. In CI the `curl -f` gate (`ci.yml:154`) protects you; locally nothing does. | Read the `-ra` summary (pytest.ini:17). Locally, use `--network container:api-server`. |
| G17 | `docker run --entrypoint pytest …` → `executable file not found`. | Tools live in `/home/app/.local/bin`, which only the entrypoint adds to PATH (docker-entrypoint.sh:5). | Keep the default entrypoint and pass the command as arguments, as CI does. |
| G18 | Running the tests without Docker fails with `ModuleNotFoundError: No module named 'api'`, including the README's own Troubleshooting command `pytest tests/ -v` (README.md:537). | `pythonpath = .` (pytest.ini:9) is the repo root locally, but the package lives in `src/api-service/`. The `sys.path` insert in `test_system_api.py:70` points to `tests/src/api-service`, which does not exist. | Use `PYTHONPATH=src/api-service pytest …` (README.md:512-513). |
| G19 | Deprecation annotations on the run page. | The workflow pins `actions/*@v4` and `slackapi/slack-github-action@v1.26.0`. GitHub periodically retires the Node.js runtimes that action majors were built on. | If you see warnings, bump to the current major versions and read their changelogs. Slack v2 renamed its inputs. |

---

## 7. Where this sits in the course

**Before (what you already have)**
- **L9 (CI, unit testing; guest lecture):** the *same repo's* Parts 3-4: the pytest pyramid and pre-commit hooks (`tutorials_demo.md:122-135`). Everything there ran **on your laptop**.
- **L18 (APIs + Frontend):** FastAPI services (`cheese-app-v2`). The CI repo's `service.py` is a stripped-down FastAPI app built the same way, with CORS middleware and async route handlers.
- **L20 (Pulumi deployment):** `cheese-app-v3` taught you to build and push images and stand up a VM automatically.

**What L21 adds:** the same checks, run **remotely and automatically** on every push or PR, on clean machines, with a visible pass/fail signal per commit. It also covers the plumbing of Actions: runners, artifacts, `needs`, conditions, outputs and secrets. This is the CI half that Milestone 4 asks for: "Implement CI using GitHub Actions … Automate building, linting, and testing on every commit or pull request" (`milestone4.md:55-58`), with "code coverage must be at least 50%" (`milestone4.md:104`).

**After**
- **L22 (Kubernetes in the cloud)** deploys `cheese-app-v3` to GKE.
- **L23 (Final deployment):** `cheese-app-v4` adds **CD**:
  - `.github/workflows/app-ci-cd-gcp.yml` triggers on push to `main` only if the commit message contains `/deploy-app` (`app-ci-cd-gcp.yml:9`).
  - It authenticates to GCP with a **secret** `GOOGLE_APPLICATION_CREDENTIALS` (`app-ci-cd-gcp.yml:21`), the same secrets mechanism you meet here with Slack.
  - It builds a deployment container and runs Pulumi/kubectl updates.

  The v4 README states that "The CI part is not implemented in this tutorial" (`cheese-app-v4/README.md:157`), so *this* repo's pipeline is the CI piece you are expected to combine with v4's CD (Milestone 5 asks for tests on PRs plus deploy on merge, at 70% coverage: `milestone5.md:41-48`).

**This is not a cheese-app version.** It is a standalone teaching repo, so there is no v(N-1)→vN diff. Two comparisons are useful instead.

*(a) The repo's own evolution:* `git diff --stat 140f138 HEAD`, from the first complete commit to HEAD:
```
 .github/workflows/ci.yml           |  69 +++++++-
 .github/workflows/docker-build.yml |  62 -------
 README.md                          | 348 ++++++++++++++++++++++++-------------
 assets/pipline.png                 | Bin 0 -> 95374 bytes
 src/api-service/api/service.py     |  20 +--
 src/api-service/api/utils.py       |   7 +-
 6 files changed, 306 insertions(+), 200 deletions(-)
```
The meaningful changes:
- `docker-build.yml` was deleted in `199abd9`. It was a second workflow with `paths:` filters that built the image and curl-tested the server.
- Slack and step outputs were added in `199abd9`, and the `if: secrets…` fix in `1a5e363`.
- Clean code was replaced with **messy code** in `91eb786` (`service.py` and `utils.py`).
- `c2dce32` deliberately introduced `math.sqrt(a)`, a NameError, which `8eb63fc` fixed.
- In class (`c3b227f`), the instructor cleaned `service.py` and introduced `math.sqrt(2 * z)` to make integration and system tests fail. The next commit (`b8458ff`) reverted that to `math.sqrt(z)`.
- `utils.py` was left messy, which is why HEAD's lint job is red.

*(b) Compared with the API service you deployed in L20 (`cheese-app-v3/src/api-service`):*

| Aspect | cheese-app-v3 api-service | cheese-app-ci-cd |
|---|---|---|
| Dependency install | `uv` with `uv.lock` and a venv at `/home/app/.venv` | `pip install --user .`, unpinned `>=` ranges, no lock |
| `DEV=1` meaning | entrypoint drops into an interactive shell | entrypoint runs `uvicorn --reload --log-level debug` |
| Args to the container | n/a (shell helpers such as `uvicorn_server`) | `exec "$@"`, which turns the image into a tool runner for CI |
| API surface | many routers (newsletter, podcast, llm_chat, …) | 3 toy endpoints + `power()` |
| Tests | ad-hoc (`_test.py`) | 26 tests in unit/integration/system folders, baked into the image |

---

## 8. Video plan (suggestion)

**Working title:** *Six Machines per Push: GitHub Actions CI, Line by Line*

**Hook question:** "During class on November 13, 2025, the instructor's demo commit (`c3b227f`) slipped a bug into the API: `math.sqrt(z)` became `math.sqrt(2 * z)`. Push that commit to your own repo, and within a couple of minutes six brand-new Linux machines are born, test it, and are destroyed. Which of them catches the bug, and which one is *already* red for a completely different reason?"

**Target length:** ~24 minutes (about 3,700 spoken words at ~155 wpm).

**Chapters**

1. **One push, six machines** (2 min)
   - *Idea:* CI is a robot that reacts to repo events by running a YAML recipe on fresh machines.
   - *Visual:* A commit dot on a branch line pulses. `ci.yml` unfolds into a tree (`on` → 6 jobs → steps), and the six job nodes become six small server icons.
   - *On screen:* `.github/workflows/ci.yml:5-17`, and the Actions tab of your own repo.

2. **When does the robot wake up?** (2 min)
   - *Idea:* triggers and filters. A push to `main`/`develop` triggers; a feature-branch push does not; a PR into `main` does, and it tests a *merge commit*.
   - *Visual:* Three branch lanes. Sparks appear only on `main`, `develop` and the PR merge preview; a ghost merge commit forms and gets the `github.sha` label.
   - *On screen:* `ci.yml:7-11`.

3. **Machines with amnesia** (2 min)
   - *Idea:* each job gets a fresh VM, so nothing is shared.
   - *Visual:* Six rooms, each with an empty "Docker shelf". The build room fills its shelf; the camera pans to the unit-tests room, the shelf is empty, and an arrow across the wall bounces off.
   - *On screen:* the `runs-on: ubuntu-latest` lines (`ci.yml:17, 43, 72, 107, 130, 174`).

4. **Build once, ship a suitcase** (3 min)
   - *Idea:* `docker build` → `docker save` → artifact → `docker load`, all under one SHA tag.
   - *Visual:* Layers stack into a cube labelled `cheese-app-api:<sha>`. The cube compresses into a tar suitcase, flies to an artifact shelf (timer "1 day"), copies fly into four rooms, and each unpacks into a cube.
   - *On screen:* `ci.yml:25-38`, `ci.yml:49-57`, Dockerfile:27-41, docker-entrypoint.sh:10-13.
   - **Pause & ponder #1:** "Delete the *Load Docker image* step from `unit-tests`. What exact error do you get, and from which step?" *Answer:* "Run unit tests" fails. `docker run` can't find `cheese-app-api:<sha>` locally, tries to pull `cheese-app-api` from Docker Hub, and gets "pull access denied / repository does not exist". The step exits non-zero.

5. **The dependency graph** (2.5 min)
   - *Idea:* `needs` builds a DAG; parallel fan-out shortens wall-clock time; the critical path sets the duration.
   - *Visual:* The DAG draws itself from each `needs:` line, then morphs into a Gantt chart using the screenshot's timings (54 s, then 18/20/22/39 s in parallel, then 4 s). The critical path glows.
   - *On screen:* `ci.yml:44, 73, 108, 131, 175-176` and `assets/pipline.png`.

6. **Gates speak in exit codes** (3 min)
   - *Idea:* every step is a 0/non-zero gate. Black is blocking, Flake8 advisory. Your first run is red because of `utils.py`.
   - *Visual:* A row of gates. Black shows `1` and slams shut; red climbs step → job → run badge; Flake8's gate greys out (skipped). Replay with `continue-on-error: true` on Black: a bypass pipe appears and the job turns green with a warning. Then zoom into `utils.py`: the comma gets a space and a blank line evaporates.
   - *On screen:* `ci.yml:59-67`, `utils.py:7-14`, and the real Black and Flake8 output from §4 Step 2.

7. **Three altitudes of tests** (3 min)
   - *Idea:* unit tests call a function, integration tests use an in-process client, system tests make real HTTP calls to a separate server. Skip is not pass.
   - *Visual:* A pyramid. Then, on the runner, two containers sit as bubbles. `--network host` dissolves the test container's bubble into the host, so its `localhost:9000` arrow reaches the server's published port. Finally the `skipif` decorator acts as a trapdoor that drops four tests into a "skipped" bin when the server is gone, while the `curl -f` gate stands guard above it.
   - *On screen:* `test_api.py:9-11`, `test_system_api.py:12-24`, `ci.yml:146-158`.
   - **Pause & ponder #2:** "With `math.sqrt(2 * z)`, which of the 26 tests fail, and which jobs turn red?" *Answer:*
     - Unit tests: all 11 pass, because only `power()` is tested.
     - Integration: `test_euclidean_distance_endpoint` fails (√50 ≈ 7.07, not 5.0); the other 9 pass.
     - System: `test_euclidean_distance_endpoint_default` fails (√10 ≈ 3.16, not ≈ 2.236) and `…_custom_values` fails (7.07, not 5.0).
     - Jobs: Integration ✗, System ✗, Unit ✓, Test Summary ✗. Lint is ✗ anyway because of `utils.py`.

8. **Collecting the verdict** (2.5 min)
   - *Idea:* `if: always()`, `needs.<job>.result`, `$GITHUB_OUTPUT`, and what a real job summary (`$GITHUB_STEP_SUMMARY`) would add.
   - *Visual:* Three result tokens (success/failure/skipped) slide along the arrows into the summary box, and a comparator lights up. The missing arrow from lint is drawn as a dashed "gap". A Markdown table then materialises on the run's summary page (after Exercise 4).
   - *On screen:* `ci.yml:172-192`.

9. **Secrets and the Slack bell** (2.5 min)
   - *Idea:* repo secrets, masking, why `if:` can't read secrets, the check-step workaround, and the bug that silences failures.
   - *Visual:* A vault hands a key to the summary job; in the log, the key renders as `***`. A replay of a failing run: "Check test results" turns red, the next step greys out (skipped), and its output arrow carries an empty string, so the bell never rings.
   - *On screen:* `ci.yml:194-205`, `ci.yml:255-257`, and the history `git show 1a5e363`.
   - **Pause & ponder #3:** "Tests fail and the secret is set. Does Slack get '❌ CI Pipeline Failed'?" *Answer:* No. The `slack-check` step is skipped after the failing step, `enabled` is empty, and the Slack step's `if:` is false. Add `if: always()` to `slack-check`.

10. **Do it yourself: red → green → protected** (3 min)
    - *Idea:* set up the repo, push, read the red run, fix Black, go green, then protect `main` correctly.
    - *Visual:* A screen recording of the Actions graph. One red node flips green after the push (it now matches `pipline.png`). Then the branch-protection page, with the correct check names highlighted, and a PR blocked by a *real* failing test.
    - *On screen:* README.md:344-349; §4 Step 14 commands; `echo "def test_broken(): assert False" >> tests/unit/test_utils.py`.

**Recap questions (end card)**
1. Which unit gets a fresh machine, a job or a step? And why does that force the image-tar artifact?
2. What do `needs:` and `if: always()` each do, and what does `test-summary` do when `build` fails?
3. Why can Flake8 fail without failing the job, and why do you never see Flake8's output when Black fails?
4. Why do system tests need `--network host` (or a shared network namespace), and what would a green run mean if the `curl -f` gate were deleted and the server crashed?
5. Why can't you write `if: secrets.SLACK_WEBHOOK_URL != ''`, and which pattern replaces it?
6. On a pull-request run, which commit does `github.sha` refer to?

---

## 9. Exercises

**E1 — Hands-on: predict, then turn the run green.**
- *Task:* Before changing anything, push HEAD as it is and predict the colour of all six nodes. Then fix `utils.py` and push again.
- *Answer:*
  - Prediction for HEAD: Build ✓, Lint ✗ (Black: `would reformat …/api/utils.py`; Flake8 skipped), Unit ✓, Integration ✓, System ✓, Summary ✓, overall ✗.
  - Fix: `pre-commit run --all-files` (or `docker run --rm -v "$(pwd)/src/api-service/api":/app/api cheese-app-api:local black --line-length 120 api/`), commit and push. All six turn green.
  - Bonus: after the fix, Flake8 runs and reports nothing. `unused_function` is not a Flake8 error.

**E2 — Debugging: README Part 7 auto-format fails.**
- *Task:* `docker run --rm -v $(pwd)/src/api-service:/app cheese-app-api:local black --line-length 120 api/` prints `bash: docker-entrypoint.sh: No such file or directory`. Why?
- *Answer:*
  - The bind mount replaces the image's entire `/app` with your `src/api-service`, which contains only `api/`.
  - The ENTRYPOINT runs `/bin/bash docker-entrypoint.sh` with a *relative* path in WORKDIR `/app` (Dockerfile:29, 52), and that file is now hidden.
  - Mount just the package: `-v "$(pwd)/src/api-service/api":/app/api`.

**E3 — Debugging and concept: the protected branch that didn't protect.**
- *Task:* You followed Part 6 exactly. Your PR with `def broken(): assert False` shows all green, and in the settings you couldn't find `unit-tests` in the checks list. Explain both.
- *Answer:*
  - pytest only collects functions matching `test_*` (pytest.ini:8), so `broken` is never run. Use `def test_broken(): assert False`.
  - Required checks are listed by job display name ("Unit Tests", etc., `ci.yml:71`), not by job id, and they appear only after a run has reported them.
  - The PR's run comes from the `pull_request` trigger; pushing the feature branch alone did nothing.

**E4 — Hands-on: add a real job summary and include lint.**
- *Task:* Make the run page show a Markdown table of job results, and make lint count.
- *Answer:* Change `needs:` (`ci.yml:175`) to `[lint-and-format, unit-tests, integration-tests, system-tests]`, add `lint-and-format` to the `if` test, and add this step (not in repo) before the Slack steps, with `if: always()`:
  ```yaml
      - name: Write job summary
        if: always()
        run: |
          {
            echo "| Job | Result |"
            echo "|---|---|"
            echo "| Lint | ${{ needs.lint-and-format.result }} |"
            echo "| Unit | ${{ needs.unit-tests.result }} |"
            echo "| Integration | ${{ needs.integration-tests.result }} |"
            echo "| System | ${{ needs.system-tests.result }} |"
          } >> "$GITHUB_STEP_SUMMARY"
  ```
  - *Prediction:* the table appears on the run's **Summary** page under the "Test Summary" job.
  - With the messy `utils.py`, the summary job itself now turns red. That is the desired behaviour: the summary agrees with the run badge.

**E5 — Debugging: Slack never reports failures.**
- *Task:* With `SLACK_WEBHOOK_URL` set, break a test. You get no Slack message. Find the cause and fix it.
- *Answer:*
  - Step-level default is `if: success()`. After "Check test results" exits 1 (`ci.yml:188`), the next step "Check if Slack webhook is configured" (`ci.yml:194-201`) is *skipped*. Its `enabled` output is empty, so the Slack step's `if: always() && steps.slack-check.outputs.enabled == 'true'` (`ci.yml:204`) is false.
  - Fix: add `if: always()` to `slack-check`.
  - Hardening: move the secret into `env: { SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }} }` and test `[ -n "$SLACK_WEBHOOK_URL" ]`.

**E6 — Change X, predict Y: enforce the Milestone 4 coverage bar.**
- *Task:* Add `--cov-fail-under=50` to the coverage command at `ci.yml:94` and remove `continue-on-error`. Predict pass or fail. Then also add `tests/integration/` to that command and predict again. Finally, make the artifact actually upload.
- *Answer:*
  - **Unit tests only:**
    - `--cov=api` reports all files in the package.
    - By my AST count, `utils.py` has 4 statements (3 executed: the two `def` lines and `return`). `service.py` has 14 statements, never imported by unit tests, so 0%.
    - Total ≈ 3/18 ≈ 17% → **fails** with pytest-cov's "Required test coverage of 50% not reached".
  - **Unit + integration:**
    - `service.py` executes everything except `/health`'s `return` (no integration test calls `/health`), so 13/14. `utils.py` stays at 3/4.
    - Total ≈ 16/18 ≈ 89% → the coverage threshold **passes**. (Counts are from my AST statement count, not a coverage run; expect small differences.)
    - System tests add nothing, because the server runs in another process.
    - Caveat: once `continue-on-error` is gone, the step can still go red for a different reason: the HTML write into the root-owned `coverage/` mount (G7) *(reasoned, not run)*. Apply the artifact fix below at the same time.
  - **Artifact fix:** before the `docker run`, add `mkdir -p coverage && chmod 777 coverage`, and use `--cov-report=xml:coverage/coverage.xml --cov-report=html:coverage/html`.

**E7 — Hands-on: replace `sleep 10` with a readiness loop.**
- *Task:* Replace the wait step (`ci.yml:150-154`) so it proceeds as soon as the server answers and fails after 30 s.
- *Answer (one option):* `for i in $(seq 1 30); do curl -sf http://localhost:9000/health && exit 0; sleep 1; done; docker logs api-server; exit 1`.
- *Prediction:* the System Tests job gets a few seconds shorter, since uvicorn usually starts in about 1-2 s, and slow starts no longer cause flaky failures.

**E8 — Conceptual: what does CI actually check?**
- *Task:* Which of these would CI at HEAD catch?
  - (a) trailing whitespace in `README.md`
  - (b) a committed private key file `id_rsa`
  - (c) a Flake8 error in `tests/unit/test_utils.py`
  - (d) a syntax error in `src/api-service/api/service.py`
- *Answer:*
  - (a) and (b): **no**. Those are pre-commit hooks (`.pre-commit-config.yaml:12-26`). CI never runs pre-commit, and pre-commit only runs where you ran `pre-commit install`.
  - (c): **no**. CI lints only `api/` (`ci.yml:61, 66`), and the pre-commit linters are restricted to `^src/` (`.pre-commit-config.yaml:35, 44`).
  - (d): **yes**, in three jobs. Black fails to parse it (lint job), the integration tests fail on import (`test_api.py:9`), and the server container cannot import `api.service`, so the system-tests job should fail at the `curl -f` gate (`ci.yml:154`) *(reasoned, not run)*. Unit tests stay green, because `test_utils.py` imports only `api.utils`.
  - Lesson: local hooks and remote CI are *different* safety nets. Add `pre-commit run --all-files` as a CI step if you want them aligned.

---

## 10. Errata and open questions

**Errata (with evidence)**
1. **The README's all-green screenshot does not match the code.** At HEAD `b8458ff`, Black fails on `src/api-service/api/utils.py:7` and `:10-12` (I reproduced this on a copy). `assets/pipline.png` was added in `3dea317` (2025-11-13 10:08 +0530), when `utils.py` and `service.py` were already messy (since `91eb786`), so the screenshot comes from another code state, most likely the clean code before `91eb786` (Black and Flake8 at 120 columns pass on the `140f138` copies and fail on the `3dea317` copies; I checked both). README Part 5 never warns that the first run will be red.
2. **Part 6's break-test command doesn't break tests.** `echo "def broken(): assert False"` (README.md:388) adds a function that pytest won't collect (`pytest.ini:8`, `python_functions = test_*`).
3. **Part 6 lists job IDs as status checks.** README.md:378 lists `lint-and-format`, `unit-tests`, … but the checks are named after the jobs' `name:` values (`ci.yml:42, 71, 106, 129`). The "Settings → Branches → Add rule" path (README.md:373) also predates GitHub's current "classic rule / ruleset" UI.
4. **Part 7's auto-format command hides the entrypoint.** README.md:442 mounts over `/app` and hides `docker-entrypoint.sh` (Dockerfile:52). *(Reasoned, not run.)*
5. **"Uses Docker Buildx for efficient caching"** (README.md:291). No cache import/export is configured (`ci.yml:22-27`), and every run rebuilds from scratch.
6. **Coverage claims.** README.md:307-308 says XML and HTML reports are generated and uploaded. XML goes to `/app/coverage.xml` inside a `--rm` container and is lost (`ci.yml:94`). The HTML report probably fails to write because of root-owned bind-mount vs uid 1000 permissions (`Dockerfile:23-28`), which `continue-on-error` masks. *(Reasoned, not run.)*
7. **Slack failure notifications are unreachable.** `slack-check` (`ci.yml:194-201`) lacks `if: always()`, so the "❌ CI Pipeline Failed" branch (`ci.yml:209, 215`) can never be sent.
8. **The test summary ignores lint.** `needs` (`ci.yml:175`) omits `lint-and-format`, so the summary and Slack can say "passed" while the run is red. README.md:325-330 calls it a summary of all tests, which is literally true but misleading.
9. **The README never documents the Slack step or the `SLACK_WEBHOOK_URL` secret** (a grep for "slack|secret" in README.md finds nothing).
10. **Line-length inconsistency** between the README's local commands (default 88/79 columns: README.md:112, 121, 124, 495-496, 502-504, 528-531) and CI (120: `ci.yml:61, 66`). There is no `[tool.black]` in `pyproject.toml`.
11. **Unpinned Black in the image vs pinned Black in pre-commit:** `pyproject.toml:8` (`black>=24.1.1`) vs `.pre-commit-config.yaml:30` (`rev: 24.1.1`).
12. **`ci.yml:2`** says "Runs on every push and pull request to main branch", but the triggers include `develop` (`ci.yml:9, 11`).
13. **`Dockerfile:1`** says "Multi-stage Dockerfile", but there is a single `FROM` (Dockerfile:2).
14. **`tests/system/test_system_api.py:2`** calls itself "Integration tests". Its `sys.path` insert (line 70) points to the non-existent `tests/src/api-service`; it works in Docker only because of `pytest.ini:9`.
15. **`pytest.ini:22`** describes the `integration` marker as "(require running services)", which contradicts README.md:147 ("No real HTTP server needed"). The markers are unused anyway.
16. **Outdated lecture references in comments:** `pytest.ini:2` ("from L18"), `tests/integration/test_api.py:4` ("Based on L18, Slide 11-12") and `.pre-commit-config.yaml:2, 28, 37` ("L17, Slide …") refer to an older numbering. In 2026 this material is L9.
17. **`--reload` has no effect in the README's Part 1 flow** (README.md:82): `docker-shell.sh:15-18` mounts no source.
18. **The course site's lecture numbering is inconsistent.** `tutorials_demo.md` has L19 = K8s (local), L20 = Pulumi, L22 = K8s (cloud), L23 = Final. `_modules/week-11.md`/`week-12.md`/`week-14.md` have L19 = Pulumi, L20 = K8s (cloud), L22 = Final. L21 is consistent in both (Nov 19 in `week-12.md:9-11`).
19. **README Troubleshooting "Tests fail locally"** (README.md:534-544) runs `pytest tests/ -v` from the project root without `PYTHONPATH`. Outside Docker that fails with `ModuleNotFoundError: No module named 'api'` (G18); the README's own working form is `PYTHONPATH=src/api-service pytest …` (README.md:512-513).

**Open questions / could not determine**
- **The Ed lesson itself** (slides, recording, any extra steps): I could not access it. The in-class demo is inferred from commits `c3b227f`/`b8458ff` ("demo class 1").
- **Whether the Buildx builder is actually used.** Docker's documentation says plain `docker build` keeps using the default builder unless `--builder`, `BUILDX_BUILDER` or `docker buildx install` is used, and the version of `setup-buildx-action@v3` the runner resolves may export `BUILDX_BUILDER`. Either way no caching is configured, and the screenshot shows the build, save and load chain working. Not run.
- **The exact behaviour of the coverage step on a hosted runner** (permission error vs success), and therefore whether `coverage-report-unit` ever contains files. Check the log of your own run.
- **Local `--network host` behaviour on your Docker Desktop version** (host networking is a newer, opt-in Docker Desktop feature). If system tests skip locally, use `--network container:api-server`.
- **Whether `pip install --user .` emits a warning about `readme = "README.md"`** (pyproject.toml:5). `README.md` is not copied before that layer (Dockerfile:32-35). Setuptools normally only warns about a missing readme file, and the screenshot's successful build suggests it is non-fatal. Not run.
- **Size of the `docker-image` artifact.** It is large because of `build-essential`, which the pure-Python dependencies probably don't need. Not measured.
- **Current Actions deprecations** (Node runtime of `actions/*@v4`, Slack action v1 vs v2) at the time you run this. Check the run annotations.
