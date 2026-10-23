# Exercises · AC215 L9 — CI & unit testing: who gets to say no before a commit?

Do these after watching, **without** re-watching first. Re-watch only the chapter you got wrong
(chapter times are in `output/chapters.txt`). Outputs quoted below are real captures from
2026-10-19 (`assets/terminal/`): `laptop/…` is the cheese-app-ci-cd laptop (Docker 29.8.2 standing in
for Docker Desktop, a Python 3.14.8 virtualenv for host `pip`), `babykev/…` is the guest-lecture
laptop (Debian 12, uv 0.13.2, just 1.59.0, **no Docker**). Line numbers of a capture count its `$`
command as line 1. Nothing was re-run for these exercises: an answer marked *derived from the code*
was worked out by reading the files at the pinned commits (cheese-app-ci-cd `b8458ff`, babykev
`4a14085`), and *recorded · walk.md* means the guest lecture's own notes, not our machine. Versions,
counts with warnings and timings are those at the time of recording; yours may be newer. Commands
marked *(extra)* aren't in the README or walk.md.

---

## Part A · The five questions from the end of the video

**Q1. What runs in a unit, an integration and a system test of this repo — file by file?**

<details><summary>Answer</summary>

Name each kind by what runs in it, not by its folder.

- **Unit**: `tests/unit/test_utils.py`, 11 tests in `TestPower` (lines 13-90). Each one calls
  `power()` from `api/utils.py` directly (`from api.utils import power`, line 7): no app, no HTTP,
  no other part of ours. Normal inputs, edges (`0`, `inf`, `nan`) and invalid ones, where
  `pytest.raises(TypeError)` passes only if the call raises (lines 69-72). The README's run says
  `11 passed` (`laptop/part3-opt1-02`, line 25). The coverage run shows how little runs:
  `api/service.py 17 17 0%` (`laptop/part3-opt1-05`, line 31). The unit tests never import the app.
- **Integration**: `tests/integration/test_api.py`, 10 tests (7 in `TestAPIEndpoints`, 2 in
  `TestCORS`, and the async function at lines 83-84). `client = TestClient(app)` (line 11) hands each
  request straight to the FastAPI app, in the same process: routing, query validation, the handler
  and `power()` all run; no server, no socket. The test that knows the right answer is lines 31-38,
  ending `assert data["distance"] == 5.0`. Result: `10 passed, 1 warning` (`laptop/part3-opt1-03`,
  line 24; the warning count is pytest 9.1.1's, at the time of recording).
- **System**: `tests/system/test_system_api.py`. Its four `TestAPIEndpoints` tests call
  `requests.get` on `API_BASE_URL = "http://localhost:9000"` (line 12): a real uvicorn in another
  container (`api-server`, `README.md:193`), reached over a real socket because the test container
  runs with `--network host` (`README.md:196`). Result: `5 passed` (`laptop/part3-opt2-05`,
  line 19). The fifth, `TestAPIWithoutServer::test_api_structure` (lines 62-75), only imports the
  app and reads its title and version: it lives in the system folder but runs no server.

Two labels in the repo say otherwise: the system file's docstring calls it "Integration tests"
(line 2), and `pytest.ini:22` defines a marker `integration` as tests that "require running
services", which is what a system test needs. Unit and integration tests here are hermetic: only
our code can make them fail. The four live-server tests are not (Q2).
</details>

**Q2. The system tests 'pass' with no server. What does pytest actually print — and are those
four tests hermetic?**

<details><summary>Answer</summary>

It prints a green headline over four skips (`laptop/part3-opt2-07`, lines 20-24):

```
SKIPPED [1] tests/system/test_system_api.py:28: API not running at localhost:9000
SKIPPED [1] tests/system/test_system_api.py:36: API not running at localhost:9000
SKIPPED [1] tests/system/test_system_api.py:43: API not running at localhost:9000
SKIPPED [1] tests/system/test_system_api.py:53: API not running at localhost:9000
========================= 1 passed, 4 skipped in 0.35s =========================
```

and the exit status is 0 (line 25). The `SKIPPED` lines appear only because `pytest.ini:17` adds
`-ra` to every run; without it you'd see four `SKIPPED` rows and a summary line that looks green.
The one that passed is `test_api_structure`, which needs no server (Q1).

Why it skips: `@pytest.mark.skipif(not is_api_running(), …)` (line 24) is decided **once**, when
pytest imports the file to collect it. `is_api_running()` asks `/health` with a 2-second timeout
(line 18), and its bare `except:` turns every problem into `False` (lines 20-21). A server that
starts a second later is too late, and a server that's down looks the same as a test you meant to
skip.

No, those four are not hermetic: a server process, port 9000 and the network can each make them
fail (or skip) when our code is fine. Honest homes for them: check the server before testing, as
CI does (`ci.yml:150-154`), or babykev's `system` marker, which the default run deselects and a
run must ask for, and then pass (B2, B6).
</details>

**Q3. What does `pre-commit install` actually create, and why must every clone run it (or
`just setup`) again?**

<details><summary>Answer</summary>

One file: `pre-commit installed at .git/hooks/pre-commit` (`laptop/part4-02`, line 2). git runs that
file before it makes a commit, and a non-zero exit stops the commit. The file holds no checks: it
only hands over to pre-commit, which reads the repo's `.pre-commit-config.yaml`. babykev's copy,
printed by the walk's `cat "$(git rev-parse --git-path hooks)/pre-commit"` (walk.md:230;
`babykev/s03-05`):

```
INSTALL_PYTHON=/home/student/babykev/.venv/bin/python
ARGS=(hook-impl --config=.pre-commit-config.yaml --hook-type=pre-commit)
…
if [ -x "$INSTALL_PYTHON" ]; then
    exec "$INSTALL_PYTHON" -mpre_commit "${ARGS[@]}"
```

(lines 7-8 and 14-15). The cheese clone's hook is the same kind of file (not printed in our
captures).

Every clone needs it again because git does not track `.git/hooks/`: the config file is
committed and shared, the hook file never is (slides 34, 41). It also names one machine's Python by
its path (line 7). So the cheese README runs `pre-commit install` (`README.md:246`), and babykev
folds it into `just setup` (`justfile:33`; `babykev/s03-02`, line 25). A clone that never ran it
commits with no checks at all, and `git commit --no-verify` skips it (C4): that's why CI checks
again.
</details>

**Q4. black says Failed — files were modified. Is your code broken, and what do you do next?**

<details><summary>Answer</summary>

Not broken. For a formatter, `Failed` means "I changed your files, so I stopped the commit for you
to look" (`laptop/part4-04`, lines 9-13):

```
Format Python code with Black............................................Failed
- hook id: black
- files were modified by this hook

reformatted src/api-service/api/utils.py
```

The change is in your working tree, not in what you staged. So:

1. Look: `git diff` *(extra)* shows exactly what black did: `def power(base,exponent):` became
   `def power(base, exponent):` and one of three blank lines went (`laptop/part4-05`, lines 10-11
   and 16).
2. Re-stage: `git add -u` *(extra)*.
3. Commit again: `git commit -m "Your commit message"` (`README.md:255`). This time all nine hooks
   pass or have nothing to check, and the commit exists: `[main b72d50d] Your commit message`
   (`laptop/part4-07`, line 11; your hash will differ).

If you commit again **without** re-staging, the same staged file meets the same black and fails
the same way. One thing to watch: when a *linter* fails next to it, that one is a real finding a
formatter can't fix, such as `F401 'os' imported but unused` (`laptop/part4-11`, line 22). That needs
you (C2).
</details>

**Q5. babykev had 94% coverage and a wrong mask. What kind of test finally saw the bug — and why
was coverage blind?**

<details><summary>Answer</summary>

A **property-based** test: `test_no_question_sees_another_question` (`tests/unit/test_mask.py:58-65`).
Instead of one hand-drawn picture, it states the rule once (no allowed pair is ever a sibling
pair) and lets hypothesis draw request shapes from `shapes` (line 10): a
state of 1 to 6 tokens and up to 4 questions of 1 to 5 tokens, 4,686 shapes in all (walk.md:625;
slides 78-81). By kind it is a unit test: `branch_mask` alone. Step 05a added it with
the picture test and the isolation tests. Put step 05's mask line back and `just test` says
`8 failed, 95 passed`: three mask tests, four isolation tests and the notebook test
(`babykev/s05a-11`, lines 299-307). The gate now refuses what it waved through at step 05.

Coverage was blind because it only records which lines **ran**. At step 05, `just test` said
`92 passed` with `TOTAL … 94%`, and `model.py` missed only lines `60, 68, 182-185`
(`babykev/s05-03`, lines 26-30): the wrong line 140,
`same = torch.ones_like(causal) | (s[None, :] == 0)` (`babykev/s05-05`), ran in every model test.
No test compared its output with the mask we meant, so `just check` was green
(`babykev/s05-11`, lines 22-23) while the printed mask had a question seeing its sibling
(`babykev/s05-04`, rows `#####.` and `######`). Coverage is necessary (an unrun line is untested)
and never sufficient (slide 73).
</details>

### The five pause-and-ponder questions

**Ponder 1 (pytest, under the hood). README Part 6 appends `def broken(): assert False` to a test
file. Will the unit tests go red?**

<details><summary>Answer</summary>

No. `pytest.ini:8` says `python_functions = test_*`, so a function called `broken` is never
collected and never run: the unit run still says 11 passed (derived from the code; the README's
line 388 was not run in the captures). To really break the build, call it `test_broken`. The
cheese pre-commit hook wouldn't notice either way: black and flake8 only see files under `src/`
(B4).
</details>

**Ponder 2 (the system test and the silent skip). The same system-test command, but the server is
not running. Fail, error, or something else?**

<details><summary>Answer</summary>

Something else: a skip. `1 passed, 4 skipped`, exit status 0, and the reason only in `-ra`'s
summary: `API not running at localhost:9000` (`laptop/part3-opt2-07`, lines 20-25). The full story
is Q2.
</details>

**Ponder 3 (the gate on your machine). black just Failed on utils.py. flake8 runs next — will it
report the E231 and E303 from before?**

<details><summary>Answer</summary>

No: `Check Python code with Flake8…Passed` (`laptop/part4-04`, line 18). The hooks run in the
config's order, and black had already rewritten `utils.py`, so flake8 read clean code. The two
findings of Part 2 (`api/utils.py:7:15: E231`, `api/utils.py:13:1: E303`, `laptop/part2-02`,
lines 4-5) are exactly what black fixes. The commit is still blocked until you look and re-stage
(Q4).
</details>

**Ponder 4 (all green, and the mask is wrong). Every line of branch_mask ran. Coverage reads 94%.
Can any coverage number catch this bug?**

<details><summary>Answer</summary>

No. Coverage counts lines that ran, never whether anyone checked what they produced. Even 100%
would have passed this mask; only a test that compares the mask with the rule can see it (Q5).
</details>

**Ponder 5 (properties, not examples). The wrong fix blocks only the question just before. What is
the smallest request shape that still breaks the rule?**

<details><summary>Answer</summary>

You need a question two steps back: one state token and three questions of one token each,
parts `[0, 1, 2, 3]`. hypothesis finds it on its own and shrinks to `shape = (1, [1, 1, 1])`
(`babykev/s05a-08`, line 25). The six-token picture can't tell (all `ok`, `babykev/s05a-05`); the
four-token one can: `#..# ##.# WRONG` (`babykev/s05a-06`, line 11).
</details>

---

## Part B · Hands-on (predict, then run)

**B1. Put the class bug back.** In your cheese clone, change line 44 of
`src/api-service/api/service.py` from `result = math.sqrt(z)` to `result = math.sqrt(2 * z)`, the
in-class commit (`c3b227f-service.py:44`). Then run the README's Part 3 commands:

```bash
docker build -t cheese-app-api:local .
docker run --rm cheese-app-api:local pytest tests/unit/ -v
docker run --rm cheese-app-api:local pytest tests/integration/ -v
docker run -d --name api-server -p 9000:9000 -e DEV=1 cheese-app-api:local
until curl -sf http://localhost:9000/health; do sleep 1; done; echo     # (extra)
docker run --rm --network host cheese-app-api:local pytest tests/system/ -v
docker stop api-server && docker rm api-server
```

Predict which tests fail in each suite. Then predict: would `git commit` let this change in?

<details><summary>Answer</summary>

Derived from the code (not captured):

- **Unit**: 11 passed; `power()` is untouched.
- **Integration**: exactly one failure, `test_euclidean_distance_endpoint`: it wants `5.0` for
  (3, 4) and gets √50 ≈ 7.07 (`test_api.py:38`). `test_euclidean_distance_default_parameters` only
  checks that the key exists (line 45) and `..._with_floats` only checks the type (line 54), so
  both still pass.
- **System**: two failures. The default point (1, 2) should give ≈ 2.236
  (`test_system_api.py:51`) and gives √10 ≈ 3.162; (3, 4) should give 5.0 (line 58).

Two of the three distance tests check the *shape* of the answer, not its value. And yes, the commit
goes through: the cheese hook runs black and flake8, which have no opinion on `2 * z`. This gate
never runs a test; babykev's does, because its hook runs `just check`. If nothing failed at all,
you skipped the rebuild (C1). Undo with `git restore src/api-service/api/service.py` *(extra)* and
rebuild.
</details>

**B2. What does the silent skip return?** With B1's change undone and the image rebuilt, start the
server and wait for it as in B1, run the system tests, stop and remove the server, then run the
same test command again. After each test run,
type `echo $?` *(extra)*. Predict the summary line and the exit status both times.

<details><summary>Answer</summary>

With the server: `5 passed`, exit 0 (`laptop/part3-opt2-05`, lines 19-20). Without it:
`1 passed, 4 skipped`, exit 0 (`laptop/part3-opt2-07`, lines 24-25). Same status, very different
runs: a script or CI step that only checks the exit status is green both times. That's why CI
checks the server before testing: `ci.yml:150-154` waits a fixed `sleep 10`, then one
`curl -f http://localhost:9000/ || exit 1`, so a dead server fails the job before pytest can skip
anything.
</details>

**B3. Three widths, four answers.** Before running anything, predict how many findings or files
each command reports on a fresh clone:

1. `docker run --rm cheese-app-api:local flake8 --max-line-length=120 api/` (`README.md:109`)
2. `flake8 src/api-service/api/` (`README.md:121`, after `pip install black flake8`)
3. `docker run --rm cheese-app-api:local black --check --diff api/` (`README.md:112`)
4. `docker run --rm cheese-app-api:local black --check --line-length 120 api/` (`README.md:478`,
   under the README's comment "same commands used in CI", line 477)

Then: how would you make the widths agree once and for all?

<details><summary>Answer</summary>

1. Two findings, both in `utils.py`: `E231 missing whitespace after ','` and
   `E303 too many blank lines (3)` (`laptop/part2-02`, lines 4-5).
2. Three: flake8's default width is 79, which adds
   `src/api-service/api/service.py:15:80: E501 line too long (95 > 79 characters)`
   (`laptop/part2-05`, line 2).
3. `2 files would be reformatted, 1 file would be left unchanged.` (`laptop/part2-03`, line 42).
   Without a width, black uses its default of 88 and folds the 95-character `service.py:15` into
   three lines (lines 30-33 of the capture).
4. Only `utils.py`: at 120, black leaves `service.py:15` alone. This one wasn't captured; the
   digest measured it on copies of the files.

The hook and CI both use 120 (`.pre-commit-config.yaml:34`, `:43`; `ci.yml:61`, `:66`). Write the
width down once: `[tool.black]` with `line-length = 120` in `pyproject.toml`, and a `.flake8` file
with `max-line-length = 120` (flake8 doesn't read `pyproject.toml`). One trap: the image copies
`pyproject.toml` (`Dockerfile:32`) but no `.flake8`, so in-image flake8 still needs its flag.
babykev has one tool and one setting, `line-length = 100` (`babykev/pyproject.toml:65`).
</details>

**B4. The tests are never linted.** `tests/system/test_system_api.py` imports `time` and never uses
it (line 8), and line 20 is a bare `except:`. Predict: does `pre-commit run --all-files`
(`README.md:262`) complain? Then edit lines 35 and 44 of `.pre-commit-config.yaml` from
`files: ^src/.*\.py$` to `files: ^(src|tests)/.*\.py$` *(extra)* and predict the next run.

<details><summary>Answer</summary>

No complaint: flake8 says `Passed` (`laptop/part4-04`, line 18) because both black and flake8 only
see files that match `^src/.*\.py$` (`.pre-commit-config.yaml:35`, `:44`), and CI lints only the
image's `api/` folder (`ci.yml:61`, `:66`). With the wider pattern, flake8 reports two findings,
`F401 'time' imported but unused` (line 8) and `E722 do not use bare 'except'` (line 20), and black
reformats two test files: a blank line at the end of `test_system_api.py`, and `power(8, 1/3)` →
`power(8, 1 / 3)` at `test_utils.py:59`. These were measured on copies of the `tests/` folder with
the hooks' arguments (flake8 7.4.1 and black 26.5.1 at the time of recording, not the hooks' pinned
versions), not captured from a pre-commit run: run it and compare. Undo with
`git restore .pre-commit-config.yaml tests/` *(extra)*, or keep the wider pattern and fix what it
finds: test code is code.
</details>

**B5. Break each config file once (babykev, step-03).** After `git switch --detach step-03` and
`just setup`, the walk breaks four config files, one at a time, and restores each
(walk.md:259-283). For each break, predict which checker catches it and what it says:

| break (walk.md) | checker |
| --- | --- |
| `sed -i '' 's/^        args: \[--maxkb=1000\]$/          args: [--maxkb=1000]/' .pre-commit-config.yaml` (260) | `uv run yamllint --strict .` |
| `sed -i '' 's/^requires-python = /requires_python = /' pyproject.toml` (267) | `uv run validate-pyproject pyproject.toml` |
| `sed -i '' 's/"pydantic>=2.11"/"pydantic>=2.12"/' pyproject.toml` (274) | `uv lock --check` |
| `sed -i '' 's/^program := "babykev"/program:="babykev"/' justfile` (281) | `just --fmt --check --unstable` |

On Linux, write `sed -i` instead of `sed -i ''` (`babykev-walk/README.md:66`); the captures ran the
Linux form. Restore after each with `git restore` of that file.

<details><summary>Answer</summary>

- yamllint names the exact place: `10:15     error    syntax error: mapping values are not allowed here (syntax)`
  (`babykev/s03-13`, line 3).
- validate-pyproject: `` [ERROR] `project` must not contain {'requires_python'} properties ``, then
  `Invalid file: pyproject.toml` (`babykev/s03-17`, lines 8 and 34). uv noticed first, on line 2:
  ``warning: No `requires-python` value found in the workspace. Defaulting to `>=3.13`.``
- `uv lock --check`: ``error: The lockfile at `uv.lock` needs to be updated, but `--check` was provided.``
  (`babykev/s03-21`, line 3). The lockfile changes only when someone runs `uv lock` on purpose.
- just's formatter shows the diff (`-program:="babykev"` / `+program := "babykev"`) and ends
  `error: formatted justfile differs from original` (`babykev/s03-25`, lines 4-5 and 74).

All four run in `just lint-config` (`babykev/s03-27`, lines 9-12), and `just check` runs that, so
each break would also stop a commit. Why bother: a broken hook config breaks every commit for
everyone, so it should be caught like code (slides 36-40). hadolint joins the recipe at step-05b
(`justfile:125`; C5).
</details>

**B6. A marker, not a skip (babykev, step-05b).** Run `git switch --detach step-05b`, `just setup`,
`just test`, then `just test -m system`. Predict the `collected …` line of each. Then, from the
walk's record: inside a container with no network (`just image shell --network none`, walk.md:818),
what do `just check`, `just test -m system` and `HF_HOME=/tmp/empty just test -m system` do?

<details><summary>Answer</summary>

`just test`: `collected 104 items / 1 deselected / 103 selected` (`babykev/s05b-03`, line 9). The
config deselects the marker on every run: `addopts = "… -m 'not system'"` and the marker's
declaration (`pyproject.toml:56-57`), on the one test file marked with
`pytestmark = pytest.mark.system` (`tests/system/test_real_model.py:14`). On our Linux machine the
summary is `1 failed, 102 passed, 1 deselected` (line 67): one test demands bit-exact numbers that
this CPU doesn't reproduce (D2). The author's Mac says 103 passed, 1 deselected (recorded ·
walk.md:811).

`just test -m system`: `collected 104 items / 103 deselected / 1 selected` and
`1 passed, 103 deselected` (`babykev/s05b-06`, lines 9 and 26): the real model actually ran, and it
had to pass; a missing model would be a failure, not a skip.

In the no-network container (recorded · walk.md:820-828, not captured here, since this laptop has
no Docker): `just check` is green, which proves everything the hook runs is hermetic. The system
test passes too, but only because the model is in the mounted cache. With the cache pointed at an
empty folder it fails: "We couldn't connect to 'https://huggingface.co' to load the files, and
couldn't find them in the cached files." Don't try that last command on a laptop with a network:
there it would most likely just download the 1 GB model again, into the empty folder.
</details>

**B7. README Part 7: add an endpoint.** Add the `/add/` endpoint (`README.md:406-409`) and its test
(`README.md:415-418`), then build and run all tests the README's way:

```bash
docker build -t cheese-app-api:local .
docker run --rm cheese-app-api:local pytest tests/ -v
```

Predict the summary line. Then predict `docker run --rm cheese-app-api:local black --check --line-length 120 api/`
(`README.md:439`) on a clone where you never committed Part 4's fix.

<details><summary>Answer</summary>

Derived from the code (the digest's count; not captured): **23 passed, 4 skipped**. That's 11 unit,
10 integration, your new `test_add_endpoint`, and `test_api_structure`; with no server the four
live-server tests skip, and `-ra` lists them. Expect pytest 9.1.1 to add `1 warning` too, as on
every integration run at the time of recording (`laptop/part3-opt1-03`, line 24). The headline is
green with four skips in it again (Q2): read the summary.

The black check fails before you've added anything: `would reformat api/utils.py` (the digest
measured this on copies of the files; not captured), because `utils.py` is messy on purpose
(lines 7 and 10-12). Your `/add/` code isn't the cause. If you ran Part 4's loop and rebuilt,
`utils.py` is already fixed (`laptop/part4-05`). The hook won't lint your new test (B4). And skip
the README's auto-format command (`README.md:442`), derived from the code: its
`-v $(pwd)/src/api-service:/app` hides the image's whole `/app`, including the
`docker-entrypoint.sh` that `ENTRYPOINT` runs by a relative path (`Dockerfile:29`, `:52`), so black
never starts. Mount only the package (`-v "$(pwd)/src/api-service/api:/app/api"`, *extra*), or let
the hook's black do it with `pre-commit run --all-files`.
</details>

---

## Part C · Debugging

**C1. "I fixed it, and the container didn't notice."** After `pre-commit run --all-files`
reformatted `utils.py` on your laptop (`laptop/part4-04`), you run
`docker run --rm cheese-app-api:local black --check --diff api/` again and it still shows the old
`def power(base,exponent):` diff. Why, and what's the fix?

<details><summary>Answer</summary>

The image holds a **copy** of the code, made when it was built: `COPY --chown=app:app
src/api-service/api/ ./api/` (`Dockerfile:38`, with the tests and `pytest.ini` on lines 39-40).
`docker run` mounts nothing, and neither does `docker-shell.sh` (lines 15-18), so `--reload` in
Part 1 only ever watched that copy. Rebuild: `docker build -t cheese-app-api:local .`. Only the
steps from the changed `COPY` on re-run; the `pip install` layer stays cached because
`pyproject.toml` didn't change. One more trap: `sh docker-shell.sh` builds a *different* name,
`cheese-app-api-service` (`docker-shell.sh:7`, `11`), so it never refreshes `cheese-app-api:local`.
`docker image ls` lists both (`laptop/clean-03`, lines 3-4).
</details>

**C2. Refused twice.** Reproduce the video's last part-1 demo:

```bash
sed -i '1i import os' src/api-service/api/service.py && git add -u     # (extra)
git commit -m "try an unused import"                                     # (extra)
git status                                                               # (extra)
```

On a Mac, add `import os` as the first line in your editor instead, then `git add -u`. Two hooks
fail (`laptop/part4-11`). (a) Why does black fail too? (b) Why does `git status` list
`service.py` under both "Changes to be committed" and "Changes not staged for commit"
(`laptop/part4-12`, lines 6-13)? (c) What's the real fix?

<details><summary>Answer</summary>

(a) black rewrote the file around the inserted line: `reformatted src/api-service/api/service.py`
(line 13). `git diff` *(extra)* shows what it changed. (b) The commit was refused, so nothing new
exists. The staged copy is still yours, with the import; the working-tree copy is black's rewrite
on top of it. (The "ahead of 'origin/main' by 1 commit" on line 3 is the Part 4 commit, not this
one: `laptop/part4-09`.) (c) flake8's finding,
`src/api-service/api/service.py:1:1: F401 'os' imported but unused` (line 22), needs a person: no
formatter can know whether you meant to use `os`. Delete the import, or use it. To throw the
experiment away, the capture's restore:
`git restore --staged src/api-service/api/service.py && git restore src/api-service/api/service.py`
(`laptop/part4-13`).
</details>

**C3. The `.env` that won't go in (babykev, step-03).** Run the walk's
`echo X=1 > .env && git add -f .env`, then `git commit -m "try"` (walk.md:306-307). Which hook
refuses, where does its message come from, and why does `just check` still say `Passed` in the same
run (`babykev/s03-35`)?

<details><summary>Answer</summary>

The `no-env-file` hook: `no .env file…Failed`, and its message is the config's own sentence,
`A .env file holds the settings and secrets of one machine. It is never committed` (lines 4-8). The
hook is `language: fail` with that sentence as its `entry` (`babykev/.pre-commit-config.yaml:14-18`):
a hook whose only job is to fail for any staged file matching `(^|/)\.env$`. pre-commit runs every
hook and reports each, so `just check` ran and passed (line 12), but one failure is enough: exit 1,
no commit. `git add -f` forces a file past any ignore rule, so the hook is the guard that's left.
Undo with `git rm --cached -q .env && rm .env` (walk.md:311). The cheese repo's version of this
guard is `detect-private-key` (`.pre-commit-config.yaml:25`), which starts to matter in L10, when
real credentials arrive.
</details>

**C4. The walk-around.** With C2's unused import staged again, run
`git commit --no-verify -m "try an unused import"` *(extra)*. Predict what happens. Then read
`ci.yml:7-11` and `:59-67`: once such a commit is pushed to a repo with this workflow, which step
would turn the job red?

<details><summary>Answer</summary>

git skips the hook completely and makes the commit (not captured; that's what `--no-verify` is
for). Undo it with `git reset --soft HEAD~1` *(extra)*, which keeps the change staged, then the
restore from C2. A hook lives on one machine and anyone can walk past it, so CI re-runs the checks
on a server nobody can skip (Lecture 21).

Reading `ci.yml` (derived from the file; the workflow wasn't run): it runs on every push and pull
request to `main` and `develop` (lines 7-11). The black step has `continue-on-error: false`
(line 62), so it fails the job; at HEAD it would already flag `utils.py` (B7) unless the Part 4 fix
was committed. The flake8 step has `continue-on-error: true` (line 67): an F401 alone would show in
the log and leave the job green. A CI step is only as strict as its config says.
</details>

**C5. hadolint refuses the Dockerfile (babykev, step-05b).** Run the walk's two breaks, restoring
after each (walk.md:779-781 and 786-788):

```bash
perl -pi -e 's/^RUN uv tool install "rust-just==\$\{JUST\}" \\$/RUN uv tool install "rust-just==\${JUST}"/; s/^    && git config /RUN git config /' Dockerfile
uv run hadolint Dockerfile
git restore Dockerfile
perl -ni -e 'print unless /^# hadolint ignore=DL3008$/' Dockerfile
uv run hadolint Dockerfile
git restore Dockerfile
```

What does each finding ask for, and is the `# hadolint ignore=DL3008` line cheating?

<details><summary>Answer</summary>

The first break splits one `RUN` into two:
``Dockerfile:69 DL3059 info: Multiple consecutive `RUN` instructions. Consider consolidation.``
(`babykev/s05b-09`, line 2). Each `RUN` makes a layer, so
hadolint asks for one. The second removes the ignore comment:
``Dockerfile:48 DL3008 warning: Pin versions in apt get install. Instead of `apt-get install <package>` use `apt-get install <package>=<version>` ``
(`babykev/s05b-13`, line 2). Both exit 1, and hadolint runs inside
`just lint-config` (`justfile:125`), so either would stop a commit.

The ignore isn't cheating, because the reason sits right above it (`Dockerfile:46-48`): Debian
replaces a package with each security fix, so a pinned version stops building within weeks, and
the base image is the pin. A rule switched off with its reason written beside it is a decision; a
rule switched off silently is a mystery. Compare the cheese hook's
`--extend-ignore=E203,W503` (`.pre-commit-config.yaml:43`), which has no reason in the file.
</details>

**C6. Running the tests on the host.** Outside Docker, in any venv, you install a few packages and
run the Troubleshooting command `pytest tests/ -v` (`README.md:537`) from the repo root. Predict two
problems, one after the other, and their fixes.

<details><summary>Answer</summary>

Derived from the code (not captured):

1. `import api` fails. `pythonpath = .` (`pytest.ini:9`) adds the repo root, but the package lives
   in `src/api-service/api/`; in the image it works only because `Dockerfile:38` copies it to
   `/app/api`. The README's local section gives the fix:
   `PYTHONPATH=src/api-service pytest tests/unit/ -v` (`README.md:512`).
2. The integration file then stops at its `@pytest.mark.asyncio` (`test_api.py:83`): that marker
   is registered only by the `pytest-asyncio` plugin, and `--strict-markers` (`pytest.ini:15`)
   turns an unknown marker into an error. Install `pytest-asyncio` (it's in `pyproject.toml:13`), or
   install the whole project into the venv.

The image exists to close exactly this "works in the container, not on my laptop" gap.
</details>

---

## Part D · Think

**D1. Where should each check live?** Put each in "every commit (hook)", "on push or in CI", or
"by hand / on a schedule": (a) black; (b) `detect-private-key`; (c) the cheese unit and
integration tests; (d) the cheese system tests; (e) babykev's `just test -m system`; (f) a hermetic
check that takes three minutes.

<details><summary>Answer</summary>

The lecture's test: can anything but our code make it fail? Only checks where the answer is no
belong in the hook (slides 94-97).

(a) and (b): hook. Fast, file-level, hermetic. (c) Hermetic and under a second (`11 passed in
0.05s`, `10 passed, 1 warning in 0.41s` at the time of recording: `laptop/part3-opt1-02`, line 25;
`laptop/part3-opt1-03`, line 24), so they *could* run on every
commit, as babykev's hook runs all its hermetic tests through `just check`. The cheese config
chooses not to: its tests run by hand or in CI. (d) CI, which starts a server and fails loudly when
it's down (`ci.yml:146-158`). (e) By hand or on a schedule: it needs the Hub, about 1 GB of weights
and a device (`tests/system/test_real_model.py:1-8`). (f) Hermetic but slow: a `pre-push` hook, the
moment git offers for "checks too slow for every commit" (slide 44), plus CI. A hook people find
slow or flaky gets bypassed.
</details>

**D2. Hermetic, and still different on two machines.** At step-05a, `just test` says
`1 failed, 102 passed` on our Linux machine (`babykev/s05a-03`, line 67) and 103 passed on the
author's Mac (recorded · walk.md:621). The failing assert is `torch.equal(before[2], after[2])`
(`test_model.py:156`), and the two tensors print the same:
`tensor([-0.2021, -0.2099, -0.2119])` (line 48 of the capture). Is the test hermetic? Should it get
the `system` marker? What would you change?

<details><summary>Answer</summary>

It is hermetic by the lecture's definition: no network, no download, no device, no server; the
tiny model is built in memory. Yet the machine made it fail. `torch.equal` asks for bit-for-bit
equality, and rewriting question 2 changes the packed sequence's length; this CPU's kernels sum in
a length-dependent order, so the last bits of question 3's numbers move (ASSETS.md, "Differences").
The Mac happens to be bit-exact. So the test quietly promises more than "only our code can make it
fail": it promises the same floating-point arithmetic everywhere.

A `system` marker would be wrong: it would take a good isolation test out of every commit. Better,
keep the promise the test is about and drop the one it isn't: compare with a tolerance far below
what a leaking mask does (with step 05's mask the scores moved in the second decimal,
walk.md:656). That's a suggestion, not the author's code. The test still fails for the real
reason with the wrong mask (`babykev/s05a-11`). Neither result is the student's mistake or a
babykev bug.
</details>

**D3. One command for everyone.** In the cheese repo, list every black that can judge your code,
and its width. Then sketch what babykev would do instead.

<details><summary>Answer</summary>

- The hook: black 24.1.1, pinned (`.pre-commit-config.yaml:30`), at 120 (`:34`).
- The image: whatever `black>=24.1.1` (`pyproject.toml:8`) resolved to when you built it (not
  printed in our captures), at 88 in `README.md:112`, at 120 in `README.md:439`, `:478` and CI
  (`ci.yml:61`).
- Your laptop: `pip install black flake8` gave black 26.10.1 and flake8 7.4.1 at the time of
  recording (`laptop/part2-04`, line 37), at 88 by default (`README.md:124`).

That's three versions and two widths, and the README itself lists "Black/Flake8 version mismatch
between local and CI" as a common issue (`README.md:564`). babykev's answer: tools pinned once in
`uv.lock`, the setting written once (`line-length = 100`), and one command, `just check`, which
people, the hook (`entry: just check`, `babykev/.pre-commit-config.yaml:21`) and later CI all call
(slide 20). For the cheese repo, the smallest step is the same idea: one script or recipe that runs
black and flake8 with the hook's versions and width, called by the README, by CI and by you.
</details>

**D4. Your milestone repo.** You copy this setup into your project. Name three things that will
bite if you copy blindly.

<details><summary>Answer</summary>

1. **Where the files sit.** pre-commit and GitHub Actions only look at the repository's root:
   `.pre-commit-config.yaml` there, workflows in the root's `.github/workflows/`. A
   `files: ^src/.*\.py$` pattern is relative to that root, so a project nested one folder down
   never matches.
2. **The floor.** Milestone 5 asks for at least 70% coverage; babykev's gate uses 90
   (`justfile:152`). A floor is a gate, not a goal (Ponder 4), and it measures the whole package:
   under `-k` it fails with every selected test green (`babykev/s03-10`: `9 passed`, yet
   `FAIL Required test coverage of 90% not reached. Total coverage: 49.40%`, line 25).
3. **The hook's environment.** A `language: system` hook such as `entry: just check`
   (`babykev/.pre-commit-config.yaml:21-22`) runs whatever `just` is on the committing program's
   `PATH`. A commit from an editor's git button may not see the `PATH` your terminal has, and the
   hook fails there. Start the editor from a terminal, or check from the terminal.
</details>

**D5. What's left behind?** List what this lecture may have left on your machine and how to clear
it. Nothing here was billable.

<details><summary>Answer</summary>

- **Docker**: two images, `cheese-app-api-service` and `cheese-app-api:local`, 731MB on disk each
  (`laptop/clean-03`), and build cache: `docker system prune` (`README.md:573`) reclaimed `95.17MB`
  at the time of recording (`laptop/clean-02`, line 26). Containers: none, if every run used `--rm`
  and Option 2 reached its `docker stop api-server && docker rm api-server`.
- **The hook**: `pre-commit uninstall` *(extra)* prints `pre-commit uninstalled`
  (`laptop/clean-04`); `pre-commit clean` *(extra)* removes the hook environments it downloaded on
  the first commit (`laptop/part4-03`, lines 2-14).
- **babykev**: its `.venv` (step 05's `just setup` downloads a few hundred megabytes) and, if you ran
  the smoke, the base model in the Hugging Face cache, about 1 GB (`babykev-walk/README.md:68-70`).
</details>
