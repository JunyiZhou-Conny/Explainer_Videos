# Exercises · AC215 L21 — CI/CD with GitHub Actions II: one push, six fresh machines

Do these after watching, **without** re-watching first. Re-watch only the chapter you got wrong
(chapter times are in `output/chapters.txt`). Outputs quoted below are real: the captures of
2026-11-06 (`assets/terminal/`: `laptop/` is a fresh Docker 29.8.2 engine standing in for your
laptop, `runner/` every job of `ci.yml` on its own fresh stand-in runner; provenance in
[`ASSETS.md`](ASSETS.md)), and the extra checks run for these exercises, listed with their scripts
and logs in [`assets/exercise-checks/`](assets/exercise-checks/README.md). The repository is
`dlops-io/cheese-app-ci-cd` at `b8458ff` (`main`); `README:NN` means line NN of its README,
`ci.yml:NN` a line of `.github/workflows/ci.yml`. No hosted GitHub Actions run was possible here
(this machine cannot push to GitHub), so whatever only GitHub can show (the run page, a Slack
message, the branch-protection page) is answered from the workflow file and GitHub's documented
rules, and the answer says so. Versions are those at the time of recording; yours may be newer.
Parts 1–4 of the same README (the three test levels, Black vs Flake8, `pre-commit`) have their own
exercises in [Lecture 9's](../ac215-l09-ci-testing/exercises.md); these build on them.

---

## Part A · The five questions from the end of the video

**Q1. Name two ways code reaches the shared repository without passing your local hooks. Which
checks does this pipeline repeat, and which not?**

<details><summary>Answer</summary>

Hooks live in `.git/hooks/` of one clone and run only where someone ran `pre-commit install`, so:
(1) a teammate who never installed them commits and pushes unchecked; (2) `git commit --no-verify`
skips every pre-commit hook (the video's run 3: `[main 2892b1b] quick fix`,
`laptop/44-commit-no-verify.txt`). A third: an edit made on GitHub's web page never touches a laptop.

The pipeline repeats only **Black** (`ci.yml:61`, blocking) and **Flake8** (`ci.yml:66`,
advisory), both at 120 columns and only on `api/` inside the image, the same files the hooks'
`files: ^src/.*\.py$` select. The seven hygiene hooks of `.pre-commit-config.yaml:12-26`
(trailing whitespace, end of file, YAML, large files, JSON, merge conflicts, private keys) never run
in CI. In the other direction, CI runs the three test levels, which no hook runs. And the two Blacks
differ: the hook pins 24.1.1 (`.pre-commit-config.yaml:30`), the image installs the newest that
satisfies `black>=24.1.1` (26.10.1 at the time of recording). They agreed on this code; they can drift.
</details>

**Q2. Which unit gets a fresh machine, a job or a step? Why does that force the image tar and a
`docker load` in every check job?**

<details><summary>Answer</summary>

A **job**: each `runs-on: ubuntu-latest` (six in this file) is a new virtual machine with an empty
Docker engine. Steps of one job run in order on the same machine and share its files and its Docker.
The image that `build` made dies with the build machine, so `build` saves it
(`docker save … -o /tmp/cheese-app-api.tar`, `ci.yml:31`) and uploads the tar as the artifact
`docker-image` (`ci.yml:33-38`, kept 1 day); every check job downloads it and runs
`docker load -i /tmp/cheese-app-api.tar` (`ci.yml:57` and the same in the other three). Proof: in a
fresh check job `docker images` prints only its header (`runner/run1/lint-and-format/x1-images-before-load.txt`);
skip the load and "Run unit tests" fails with `Unable to find image … locally`, then
`pull access denied for cheese-app-api, repository does not exist or may require 'docker login'`,
exit 125 (`runner/noload/x2-unit-tests-without-load.txt`). The summary job loads nothing: it only
runs bash. The alternatives (rebuild in each job, or push to a registry) are slower or need
credentials, and rebuilding would no longer test the *same* bits.
</details>

**Q3. Your run is red, but the summary says `✅ All tests passed!`. Why, and what is the fix?**

<details><summary>Answer</summary>

`test-summary` lists only the three test jobs in `needs` (`ci.yml:175`) and checks only their
results (`ci.yml:185`). Lint failed (Black, `would reformat /app/api/utils.py`), but its result never
reaches the summary, which sees three `success` and prints `✅ All tests passed!`
(`runner/run1/test-summary/01-check-test-results.txt`). The run is red anyway because **any** failed
job makes the run fail. The fix is one line to wire it in, `needs: [lint-and-format, unit-tests,
integration-tests, system-tests]`, **plus** the same job in the script's check: with `needs` alone
the summary waits for lint but still tests only three results and still says all passed. Exercise B2
has the whole step; played with run 1's results it prints `Lint and Format: failure`,
`❌ Some tests failed!`, exit 1 ([`workflow.log`](assets/exercise-checks/logs/workflow.log)).
</details>

**Q4. Why can Flake8 fail without failing its job, and why don't you see Flake8's output when
Black fails?**

<details><summary>Answer</summary>

Every step fails when its command exits with anything but 0. Flake8 exits 1 on this code
(`api/utils.py:7:15: E231 missing whitespace after ','`, `api/utils.py:13:1: E303 too many blank
lines (3)`), but its step says `continue-on-error: true` (`ci.yml:67`): the step's failure is
recorded and the job carries on as if it passed. Black's step says `continue-on-error: false`
(`ci.yml:62`), so its exit 1 fails the job. And steps run with the default condition "only if
everything before succeeded": after Black fails, Flake8 is **skipped**, so it prints nothing
(`runner/run1/lint-and-format/00-steps.txt`: `04 failure Run Black formatter check`,
`05 skipped Run Flake8 linter`). The two warnings above are what it *would* have printed
(`runner/run1/lint-and-format/x4-flake8-if-run.txt`, re-run in [`image.log`](assets/exercise-checks/logs/image.log)).
</details>

**Q5. In the lecture's terms, is a push-triggered Actions run a pre-receive or a post-receive
check, and what turns it into a gate on GitHub.com?**

<details><summary>Answer</summary>

**Post-receive.** The `push` event fires after GitHub has accepted the push, so the commit is
already on `main` when the first job starts; a red run reports, it cannot undo the push (ponder 2).
GitHub.com doesn't run your own pre-receive scripts. The gate is **branch protection** on `main`
(README Part 6, `README:369-397`): "Require a pull request before merging" stops direct pushes, and
"Require status checks to pass before merging" with the jobs' **names** (`Lint and Format Check`,
`Unit Tests`, `Integration Tests`, `System Tests`) keeps the merge button locked until the
`pull_request` run is green. The check still runs after the push to the feature branch; what it
refuses is the merge.
</details>

### The five ponders

**Ponder 1 (triggers).** You push three commits to `feature/login`, then open a PR into `main`.
<details><summary>Answer</summary>

0 runs for the three pushes: `push` only fires for `main` and `develop` (`ci.yml:8-9`). 1 run when
the PR opens (`pull_request` into `main`, `ci.yml:10-11`), then 1 more for every later push to the
branch while the PR stays open. The PR run tests a temporary merge of your branch into `main`, not
the branch tip.
</details>

**Ponder 2 (bell or gate).** The run turns red: is your push on `main`?
<details><summary>Answer</summary>

Yes. The run started *because* GitHub accepted the push; nothing in a workflow can refuse a push
that already happened. To keep red code out of `main`, use branch protection (Q5).
</details>

**Ponder 3 (no load).** Delete "Load Docker image" from `unit-tests`: which step fails, and how?
<details><summary>Answer</summary>

"Run unit tests": Docker finds no `cheese-app-api:<commit>` on the fresh machine, asks Docker Hub,
gets `pull access denied for cheese-app-api, repository does not exist or may require 'docker login'`,
exit 125; the job fails, and so does the summary (`unit-tests` is in its `needs`). Captured in
`runner/noload/`.
</details>

**Ponder 4 (the class demo).** `c3b227f` computes `math.sqrt(2 * z)`. Which jobs turn red, and what
does Test Summary say?
<details><summary>Answer</summary>

Integration red (`assert 7.0710678118654755 == 5.0`, `1 failed, 9 passed, 1 warning`); system red
(`2 failed, 3 passed`: the point 3, 4 and the default point 1, 2); unit **green** (only `power()` in
`utils.py` has unit tests); lint red (still `utils.py`); Test Summary red: `❌ Some tests failed!`,
exit 1 (`runner/run-demo/`). And then "Check if Slack webhook is configured" is skipped, so the
failure message could never be sent (C1).
</details>

**Ponder 5 (a key file).** A teammate commits a private key file with `--no-verify` and pushes to
`main`. Which job catches it?
<details><summary>Answer</summary>

None. `detect-private-key` is a local hook only, and CI's two linters read `api/` only (`ci.yml:61,
66`). Checked: the hook stops the commit (`Detect private keys…Failed`, `Private key found: id_rsa`),
`git commit --no-verify` goes through, and `pre-commit run --all-files` flags the committed file
again ([`git.log`](assets/exercise-checks/logs/git.log); the file held placeholder text, not a key).
So the fix is one CI step that runs `pre-commit run --all-files` (`pip install pre-commit` first on
the runner). And rotate the key: once pushed, it is in the history on GitHub, even if a later commit
deletes it.
</details>

---

## Part B · Hands-on (predict, then run)

**B1. Run the lint job before you push.** In your fresh clone, build the image and run the lint
job's two commands with your own tag (`ci.yml:61, 66`):

```bash
docker build -t cheese-app-api:local .
docker run --rm cheese-app-api:local black --check --line-length 120 api/; echo "exit $?"
docker run --rm cheese-app-api:local flake8 --max-line-length=120 --extend-ignore=E203,W503 api/; echo "exit $?"
```

Predict both exit codes and which one would fail the CI job. Then fix the code with
`pre-commit run --all-files` (Part 4), rebuild and run both again.

<details><summary>Answer</summary>

Black: `would reformat /app/api/utils.py`, `1 file would be reformatted, 2 files would be left
unchanged.`, exit 1, which fails the job. Flake8: `api/utils.py:7:15: E231 …` and `api/utils.py:13:1:
E303 too many blank lines (3)`, exit 1, which CI would ignore (`continue-on-error: true`), if it ran
at all. After the fix (a space after the comma in `def power(base, exponent):`, one blank line
removed) and a rebuild: Black `All done! ✨ 🍰 ✨`, `3 files would be left unchanged.`, exit 0; Flake8
prints nothing, exit 0 ([`image.log`](assets/exercise-checks/logs/image.log), "B1"). `unused_function`
is not a Flake8 error. **Rebuild first**: the code is baked into the image (`Dockerfile:38`), so the
old image still holds the messy file. Without pre-commit, `docker run --rm -v
"$(pwd)/src/api-service/api":/app/api cheese-app-api:local black --line-length 120 api/` rewrites
your files from inside the image; mount only the `api` folder: README Part 7's
`-v $(pwd)/src/api-service:/app` hides the entrypoint and fails with `/bin/bash: docker-entrypoint.sh:
No such file or directory`, exit 127 (same log).
</details>

**B2. Make the summary count lint.** Change `test-summary` so lint counts, and make the run page show
a table of results. Predict what the summary prints for run 1's results (lint failed, the three test
jobs passed), and the colour of the summary node.

<details><summary>Answer</summary>

Three edits in `test-summary`
([`ci-exercises.yml`](assets/exercise-checks/logs/ci-exercises.yml) has them all):

```yaml
    needs: [lint-and-format, unit-tests, integration-tests, system-tests]
```

and in "Check test results", an `echo "Lint and Format: ${{ needs.lint-and-format.result }}"`, a
table appended to `$GITHUB_STEP_SUMMARY`, and the lint result in the test:

```yaml
          {
            echo "| Job | Result |"
            echo "|---|---|"
            echo "| Lint and Format | ${{ needs.lint-and-format.result }} |"
            echo "| Unit | ${{ needs.unit-tests.result }} |"
            echo "| Integration | ${{ needs.integration-tests.result }} |"
            echo "| System | ${{ needs.system-tests.result }} |"
          } >> "$GITHUB_STEP_SUMMARY"

          if [ "${{ needs.lint-and-format.result }}" != "success" ] || [ "${{ needs.unit-tests.result }}" != "success" ] || …
```

Played with run 1's results: `Lint and Format: failure`, the three `success` lines,
`❌ Some tests failed!`, `status=failure`, exit 1, so the summary node turns **red** and now agrees
with the run badge; with run 2's results (all green): `✅ All tests passed!`, exit 0. actionlint
1.7.12 reads the edited file with no findings ([`workflow.log`](assets/exercise-checks/logs/workflow.log)).
On GitHub the table appears on the run's **Summary** page under "Test Summary" (not observed here).
Side effect: the summary now waits for lint too, a few seconds at most.
</details>

**B3. Make the coverage report real.** The README promises terminal, XML and HTML reports uploaded as
an artifact (`README:307-308`). In an empty folder, run the coverage command the way the runner does
(`ci.yml:94`, your tag instead of the commit ID):

```bash
docker run --rm -v $(pwd)/coverage:/app/coverage cheese-app-api:local pytest tests/unit/ --cov=api --cov-report=term --cov-report=xml --cov-report=html:coverage
ls -ld coverage; find coverage -type f | wc -l
```

Predict the exit code and how many files the upload step would find. Then fix it.

<details><summary>Answer</summary>

On Linux (a hosted runner, or a Linux laptop): the 11 tests pass, then
`INTERNALERROR> PermissionError: [Errno 13] Permission denied: 'coverage/style_cb_4667309f.css'`,
exit 3; `coverage` is `drwxr-xr-x root root` (Docker created the missing folder as root) while the
container runs as `uid=1000(app)`; 0 files, so the upload finds nothing (on GitHub, the warning "No
files were found with the provided path: coverage/"). And `--cov-report=xml` would write
`/app/coverage.xml` *outside* the mount, lost with the `--rm` container. In CI the job stays green
because of `continue-on-error: true` (`ci.yml:95`). Fix (in `ci-exercises.yml`):

```yaml
        run: |
          mkdir -p coverage && chmod 777 coverage
          docker run --rm -v ${{ github.workspace }}/coverage:/app/coverage cheese-app-api:${{ github.sha }} pytest tests/unit/ --cov=api --cov-report=term --cov-report=xml:coverage/coverage.xml --cov-report=html:coverage/html
```

Checked: the coverage table prints (`TOTAL 21 18 14%`), `Coverage HTML written to dir
coverage/html`, `Coverage XML written to file coverage/coverage.xml`, exit 0, 13 files in `coverage/`
([`image.log`](assets/exercise-checks/logs/image.log), "B3"). On Docker Desktop for Mac the
bind-mount ownership is relaxed, so the original command may work on your laptop and still fail on
the runner (not checked here).
</details>

**B4. A coverage bar.** Add `--cov-fail-under=50` to the coverage command. Predict pass or fail for
unit tests only, then for `tests/unit/ tests/integration/`. What else must change in `ci.yml` for the
bar to stop a merge?

<details><summary>Answer</summary>

Unit only: **fails**. `--cov=api` counts every file of the package: `service.py` 17 statements, 0 %
(the unit tests never import it), `utils.py` 4 statements, 75 % (line 14, `pass` in
`unused_function`, never runs): `FAIL Required test coverage of 50% not reached. Total coverage:
14.29%`, exit 1. Unit + integration: **passes**, `service.py` 94 % (missing line 35, `/health`'s
return: no integration test calls `/health`), `Required test coverage of 50% reached. Total coverage:
90.48%`, `21 passed, 1 warning`, exit 0 ([`image.log`](assets/exercise-checks/logs/image.log), "B4").
System tests can't add anything: the server runs in another process. In `ci.yml` you must also remove
`continue-on-error: true` from that step (otherwise a missed bar keeps the job green) and apply B3's
folder fix first, or the step fails on the `PermissionError` before the bar is even measured.
</details>

**B5. Wait for the server, not for 10 seconds.** Replace the "Wait for server to be ready" script
(`ci.yml:151-154`) with a loop that goes on as soon as the server answers and gives up after 30
seconds, printing the server's log. Predict how long it waits here.

<details><summary>Answer</summary>

```yaml
        run: |
          echo "Waiting for server to start..."
          for i in $(seq 1 30); do
            curl -sf http://localhost:9000/health && exit 0
            sleep 1
          done
          docker logs api-server
          exit 1
```

Checked with the server on host port 19000: `{"status":"healthy"}`, `ready on try 2 after
1.076815515 s`; with a container that never starts a server: `gave up after 31 s`, then its log,
exit 1 ([`image.log`](assets/exercise-checks/logs/image.log), "B5"). The job gets about 9 s
shorter, and a slow start no longer fails it. `-s` hides curl's progress meter, `-f` turns an HTTP
error into a non-zero exit. The original hits `/`, this one `/health`; both exist in `service.py`.
</details>

**B6. Make "Buildx caching" true.** The README says the build "uses Docker Buildx for efficient
caching" (`README:291`), but the build runs on the `default` builder with no cache
(`runner/run1/build/03-build-docker-image.txt` line 2; `laptop/62-act-push.txt`: `docker:default`).
Change the "Build Docker image" step so a second run reuses the layers.

<details><summary>Answer</summary>

Replace the `run:` step with the Buildx action, using GitHub's cache backend, and keep the "Save
Docker image" step after it:

```yaml
      - name: Build Docker image
        uses: docker/build-push-action@v6
        with:
          context: .
          tags: cheese-app-api:${{ github.sha }}
          load: true
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

`load: true` puts the image into the runner's Docker so `docker save` finds it; `mode=max` caches
every layer, including the slow `apt-get` and `pip install` ones. A plain `docker build` never uses
the builder that `setup-buildx-action` creates, and even a Buildx build caches nothing across fresh
machines unless the cache is exported and imported. **Partly checked:** actionlint reads the edited
file with no findings ([`workflow.log`](assets/exercise-checks/logs/workflow.log)); the cache itself
needs GitHub's cache service and was not run here. Check the action's current major version before
you copy this.
</details>

---

## Part C · Debugging

**C1. Slack only ever says "Passed".** You added the secret `SLACK_WEBHOOK_URL` and Slack posts
"✅ CI Pipeline Passed" for green runs. Then a test breaks, the run is red, and Slack stays silent.
Why, and what is the fix?

<details><summary>Answer</summary>

"Check test results" exits 1 (`ci.yml:188`). The next step, "Check if Slack webhook is configured"
(`ci.yml:194-201`), has no `if:`, so it gets the default (only after success) and is **skipped**;
its output `enabled` stays empty, and the Slack step's `if: always() &&
steps.slack-check.outputs.enabled == 'true'` (`ci.yml:204`) is false. The demo run shows exactly
that: `01 failure Check test results`, `02 skipped Check if Slack webhook is configured`,
`03 skipped Send Slack notification (steps.slack-check.outputs.enabled is '')`
(`runner/run-demo/test-summary/00-steps.txt`). The "❌ CI Pipeline Failed" branch of the payload
(`ci.yml:209, 215`) can never be sent. Fix: `if: always()` on the check step. Hardened: pass the
secret in through `env:` instead of pasting it into the script:

```yaml
      - name: Check if Slack webhook is configured
        id: slack-check
        if: always()
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
        run: |
          if [ -n "$SLACK_WEBHOOK_URL" ]; then
            echo "enabled=true" >> $GITHUB_OUTPUT
          else
            echo "enabled=false" >> $GITHUB_OUTPUT
          fi
```

Checked: actionlint finds nothing, and the script writes `enabled=false` with the variable empty and
`enabled=true` with a placeholder URL ([`workflow.log`](assets/exercise-checks/logs/workflow.log)).
Real Slack delivery needs your own workspace and was not tested. Remember: the secret goes under
**Settings → Secrets and variables → Actions**, not Settings → Webhooks; logs print it as `***`, and
runs for pull requests from forks don't get it.
</details>

**C2. Why the shell check at all?** The repository's first Slack attempt (`199abd9`) had
`if: always() && secrets.SLACK_WEBHOOK_URL != ''` on the Slack step. What is wrong with it?

<details><summary>Answer</summary>

The `secrets` context is not available in a step's `if:`. actionlint 1.7.12 on that file:
`.github/workflows/ci.yml:195:25: context "secrets" is not allowed here. available contexts are
"env", "github", "inputs", "job", "matrix", "needs", "runner", "steps", "strategy", "vars"`
([`workflow.log`](assets/exercise-checks/logs/workflow.log)). GitHub refuses such a workflow file
when it reads it (not observed here). Eleven minutes later, `1a5e363` replaced it with the check step
that writes `enabled` to `$GITHUB_OUTPUT`
(`assets/source/cheese-app-ci-cd-history/199abd9-to-1a5e363-ci.yml.diff`). The `env:` version of C1
is the other documented way: map the secret into an environment variable, then test the variable.
</details>

**C3. "I pushed and no run appears."** You forked the course's repository, cloned your fork, and
typed the README's three commands. `git commit` says `nothing to commit, working tree clean`;
`git push` says `Everything up-to-date`. Why, and how do you get a run?

<details><summary>Answer</summary>

`ci.yml` is already committed, so there is nothing to add or commit, and your fork already has that
commit, so the push sends nothing and no `push` event fires (checked with a stand-in fork:
[`git.log`](assets/exercise-checks/logs/git.log), "C3"). Make a real change (the Black fix of the
video, run 2), or `git commit --allow-empty -m "Trigger CI"` and push: `b8458ff..<new>  main ->
main`. `ci.yml` has no `workflow_dispatch`, so there is no "Run workflow" button. Other reasons for
no run: the file isn't in `.github/workflows/` at the **root** of the repository (a project
subfolder in a monorepo never runs; move it and add `defaults: run: working-directory:`); you pushed
a branch other than `main` or `develop`; on a fork, workflows aren't enabled yet (Actions tab →
enable). And if `git push` says permission denied: `origin` still points at `dlops-io` (`git remote
-v`); `git remote set-url origin https://github.com/<you>/cheese-app-ci-cd.git`.
</details>

**C4. The hook stopped my commit, so I committed again.** As in the video, you squeeze the spaces
out of line 43 of `service.py`, `git add .`, and `git commit -m "quick fix"` fails at Black, which
reformats the file; `git status --short` shows `MM`. You simply run `git commit -m "quick fix"` once
more. Predict, then explain.

<details><summary>Answer</summary>

It fails again, with a new message: `[WARNING] Unstaged files detected.`, Black `Failed`, then
`[WARNING] Stashed changes conflicted with hook auto-fixes... Rolling back fixes...`, exit 1, still
`MM` ([`git.log`](assets/exercise-checks/logs/git.log), "C4"). pre-commit checks the **staged**
copy, which is still the messy one; it sets your unstaged (reformatted) copy aside, Black reformats
the staged copy again, and the two edits collide, so pre-commit rolls its fix back. The way out:
look at Black's change, `git add` it, then commit. Here that gives `nothing to commit, working tree
clean`: Black put back exactly the original line, so the "quick fix" was only a formatting change and
vanished. Only `--no-verify` could have committed it, which is how run 3 went red.
</details>

**C5. The protected branch that didn't protect.** You followed Part 6 exactly: your pull request with
`def broken(): assert False` is green, and the check picker had no `unit-tests`. Explain both.

<details><summary>Answer</summary>

pytest collects only functions named `test_*` (`pytest.ini:8`), so `broken` never runs: the image
still says `11 passed` (`laptop/53-unit.txt`). Append `def test_broken(): assert False` instead:
`tests/unit/test_utils.py::test_broken FAILED`, `1 failed, 11 passed`, exit 1 (`laptop/57-unit.txt`),
and the PR's Unit Tests check turns red. The picker lists checks by the jobs' `name:` (`Lint and Format
Check`, `Unit Tests`, `Integration Tests`, `System Tests`: `ci.yml:42, 71, 106, 129`), not by the
README's job IDs (`README:378`), and only after they have run at least once in the repository. The
PR's run comes from the `pull_request` trigger: pushing `feature/test-protection` alone starts
nothing. On a private repository, protected branches need a paid plan (GitHub Pro is free with the
Student Developer Pack). These GitHub pages were not observed here; they follow the workflow file and
GitHub's documented behaviour.
</details>

**C6. One typo, three red jobs.** A push adds a syntax error to `service.py` (say `def oops(:` at
the end). Predict each job's result and the line in its log that tells you why.

<details><summary>Answer</summary>

Checked with an image built from such a copy ([`image.log`](assets/exercise-checks/logs/image.log),
"C6"): **build** green (nothing imports the code during the build); **lint** red: `error: cannot
parse: /app/api/service.py:52:9`, exit 123; **unit** green, `11 passed` (`test_utils.py` imports only
`api.utils`); **integration** red: `E   SyntaxError: invalid syntax`, `Interrupted: 1 error during
collection`, exit 2; **system** red at the wait step: `curl: (56) Recv failure: Connection reset by
peer`, because uvicorn's reloader holds the port while the app fails to import (the server log shows
`SyntaxError: invalid syntax`, and "Show server logs" prints it, thanks to `if: always()`); the
**summary** red, `❌ Some tests failed!`. Read the first red step of the first red job: the log line
names the file and the line.
</details>

**C7. "Re-run failed jobs" the next day.** A system test failed on a flaky network call yesterday.
Today you click "Re-run failed jobs", and it fails at "Download Docker image". Why?

<details><summary>Answer</summary>

The image artifact is kept for one day (`retention-days: 1`, `ci.yml:38`). Re-running only the failed
job skips `build`, so there is no artifact left to download. Use "Re-run all jobs" (the build makes a
new artifact), or raise the retention, which costs storage on private repositories. Reasoned from the
file and GitHub's documented retention; not run here.
</details>

---

## Part D · Think

**D1. Where should each check live?** For each, choose "local hook", "CI job", "branch protection",
or a combination: (a) Black formatting; (b) a committed private key; (c) the three test levels;
(d) "no red code reaches `main`"; (e) trailing whitespace in `README.md`.

<details><summary>Answer</summary>

(a) Both: the hook for fast feedback before the commit, CI because hooks are optional (Q1); pin one
Black version for both. (b) A hook catches it before it exists, and only CI can't be skipped: add
`pre-commit run --all-files` as a CI step (Ponder 5). Neither un-leaks a pushed key: rotate it.
(c) CI: too slow for every commit, and the system tests need a server. (d) Branch protection with
the four required checks (or a fixed Test Summary, D4): only it can refuse. (e) A hook; this CI never
checks it (`.pre-commit-config.yaml:12-13`, not in `ci.yml`).
</details>

**D2. Count the runs.** With the triggers of `ci.yml:7-11`, how many runs start for: (a) a push to
`develop`; (b) opening a PR from `feature/x` into `develop`; (c) merging that PR; (d) opening a PR
from `develop` into `main`, then merging it; (e) a push to `docs/typo`?

<details><summary>Answer</summary>

(a) 1 (`push`, `develop`). (b) 1 (`pull_request` into `develop`). (c) 1: a merge is a push of the merge
commit to `develop`. (d) 1 when the PR opens, 1 more when the merge lands on `main` as a push: 2.
(e) 0, until a PR into `main` or `develop` is opened. Every run on a private repository costs the
minutes of its six jobs (D3).
</details>

**D3. Two minutes or six?** The README's screenshot shows build 54 s, then four jobs side by side
(22, 18, 20, 39 s), then the summary 4 s. How long does a developer wait, and what does a private
repository pay? Would merging the three test jobs into one job save money?

<details><summary>Answer</summary>

The wait is the critical path, 54 + 39 + 4 s ≈ 1.6 min (about 2 with queueing). GitHub bills each
job separately and rounds each up to a whole minute (as the digest records; check GitHub's current
billing page): 6 jobs, about 6 billed minutes, the 4-second summary alone costing a minute. One test
job instead of three would bill fewer rounded minutes but run the tests one after another (a longer
wait) and lose the separate check names that branch protection uses. Public repositories pay
nothing on standard runners.
</details>

**D4. One required check?** A teammate proposes requiring only "Test Summary" in branch protection,
since it already collects the results. Good idea at `b8458ff`? After B2?

<details><summary>Answer</summary>

At `b8458ff`, no: the summary ignores lint, so a PR with a red lint job would pass the gate. After
B2 it works well: the summary waits for all four check jobs and, with `if: always()`, runs even when
one fails; a failed or skipped job (for example all of them, when `build` fails) gives a result that
isn't `success`, so the summary exits 1. One stable name in the rule, and adding a job later only
changes `ci.yml`.
</details>

**D5. When the code trains a model.** The lecture says non-determinism enters every stage once code
trains a model. Your milestone repository has a training script. What would you put in the
push-triggered CI, and what not?

<details><summary>Answer</summary>

On every push: the same as here (formatting, linting, unit tests of data and feature code,
integration tests of the API), plus a tiny training smoke test on a fixed sample with fixed seeds
that checks shapes, that the loss goes down and that a model file is written, with tolerances instead
of exact numbers. Not on every push: full training, full-data evaluation and anything that needs a
GPU or cloud credentials; those run on a schedule or a manual trigger, against versioned data (L11's
DVC), with results compared to the previous model before a controlled rollout (Lecture 23's CD).
</details>
