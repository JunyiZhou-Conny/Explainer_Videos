# L09 lecture slides — Software Development for Machine Learning

Source: one deck, `Lecture09_babykev.pdf` (PDF title "babykev", 100 slides): the guest lecture
"Software Development for Machine Learning" by Rahul Dave. These are the instructor's lecture
slides (PDF), provided by the student for study; the PDFs are not in this repository; slide
numbers are PDF page numbers. I wrote this digest from the deck's extracted text and from all
twelve contact sheets. I also enlarged slides 4, 5, 6, 11, 17, 18, 42, 45, 54, 55, 56, 90 and 99
to read their diagrams and small print. Everything below is in my own words. Only short titles,
terms, commands and single lines of code are quoted. The tutorial side of the lecture is in
[`digest.md`](digest.md).

Read this first:

- **Footer numbers match the PDF pages.** Every footer shows "babykev", the step with its title
  and a running count (for example "step-03 · Clean, and kept clean (4 of 12)"), and a page number
  equal to the PDF page. The steps are the git tags `step-00` … `step-05b` of the `babykev` repo
  (digest Track B). So any slide can be paired with the code at its tag.
- **The deck is the babykev walk, not the cheese tutorial.** It covers Track B of the digest.
  The tutorial repo `cheese-app-ci-cd` (Track A) appears once, as a QR code on slide 9. Slide 8
  says that second example "will be released later today". Nothing on the slides covers FastAPI's
  `TestClient`, black, flake8, the cheese Dockerfile or GitHub Actions.
- **The deck has no lecture number.** The title slide names no lecture number or course. The
  series' L09 label comes from the course site (digest §7), which calls the lecture "Automating
  Software Development: CI, unit testing".
- **The same deck is public.** Apart from the footers, the extracted text matches, line for
  line, `babykev.pdf` in `rahuldave/babykev-walk` at commit `82adb14` (the commit the digest
  pins). The walk's copy has no step titles in its footers. Its Markdown sources are
  `babykev-walk/slides/*.md`, which the digest already cites (for example `slides/03-check.md`).
  Their image alt texts say that slide 2's cartoon is Pavlos and slide 3's photo is the speaker.
- **CI is named but never shown.** "Continuous integration" appears in a list (6). Slide 20
  says people, agents, the git hook and CI all run the same recipes, and slide 89 lists CI as one
  use of the dev image. No workflow file is on the slides. Slide 13 defers `serve.py` to the
  "class on ci/cd with github actions" (L21 in this series).
- **One count drifts between slides.** Slide 31 leaves 37 lint findings for a person; slide 33
  says 36. The walk notes explain why: during the demo one docstring (rule D104, in
  `__init__.py`) was written by hand (`walk.md`, step-02 H).
- **Annotated code extracts badly.** On slides 18, 19, 43, 90 and 91 the margin notes are mixed
  into the code lines in the text. Read the code and the notes separately. The `#`/`.` grids
  (72–74, 79, 81) extract cleanly.

## Outline

The deck has nine parts, one per git step of the babykev project; each footer names its step.
There is no agenda slide per part and no closing slide.

- Slides 1–20 · **step-00 · Where we start**: why ML needs software engineering, the babykev
  project, uv and just
  - 1 · title "Software Development for Machine Learning", Rahul Dave
  - 2 · a cartoon of Pavlos, worried, palm raised (the same cartoon returns on 75)
  - 3 · a photo of the speaker in a T-shirt that reads "You're Absolutely Right!", a joke about
    the stock reply of AI coding agents
  - 4 · "What goes into a machine-learning project?": eight areas, 26 aspects, of which only 9
    are model and data
  - 5 · "The ML code is a small box": the Sculley et al. figure
  - 6 · "What goes into writing software?": nine areas
  - 7 · "Today": the plan, one bullet per step, each with the tools it brings
  - 8 · babykev: a small model that makes decisions, rebuilt step by step from kev's first
    commit (about 830 lines, no tests, types or docs)
  - 9 · the second example, the cheese app: QR code for `github.com/dlops-io/cheese-app-ci-cd`
  - 10 · one request (a state and three questions) and its answer
  - 11 · "A model that decides": request → pack → Qwen2.5-0.5B → pointer head
  - 12 · the three tools you install yourself: uv, just and Quarto
  - 13 · kev's files, their line counts, and the step or later class where each arrives
  - 14 · uv replaces pyenv, venv with pip, pip-tools or poetry, and pipx
  - 15 · two files describe the environment: `pyproject.toml` and `uv.lock`
  - 16 · just: a recipe is a named command
  - 17 · "Why automate" (xkcd 1319, *Automation*)
  - 18 · the justfile, line by line (annotated code)
  - 19 · the `help` recipe, line by line (annotated code), and two runs of it
  - 20 · four ways to ask what a recipe does
- Slides 21–27 · **step-01 · The contract, and its tests**
  - 21 · `api.py` is the contract: four names it defines
  - 22 · three kinds of question (`noul`, `choice`, `score`), one mechanism
  - 23 · Pydantic: types checked when the data arrives
  - 24 · "Check what comes in" (xkcd 327, *Exploits of a Mom*)
  - 25 · pytest: a test is a function that asserts; coverage; 52 runs, 2 failures
  - 26 · testing the command line: fixtures and parametrize
  - 27 · the two failing tests, and why the tests are right
- Slides 28–32 · **step-02 · Format and lint arrive**
  - 28 · the two fixes, worked through with numbers
  - 29 · `ruff format`: style without arguments
  - 30 · ruff as a linter, and its rule families
  - 31 · how many findings each tool removes: 79 → 70 → 69 → 37
  - 32 · uv dependency groups: keep developer-only packages apart
- Slides 33–44 · **step-03 · Clean, and kept clean**
  - 33 · the findings a person fixed; result 53 tests, coverage 100%, 0 findings
  - 34 · what `pre-commit install` writes into `.git/hooks/pre-commit`
  - 35 · `just check`: everything a commit must pass
  - 36 · `just lint-config`: four checks for the files that are not Python
  - 37 · yamllint
  - 38 · validate-pyproject
  - 39 · `uv lock --check`
  - 40 · `just --fmt --check`
  - 41 · pre-commit: the checks run themselves
  - 42 · "The indentation question" (CommitStrip): a tabs-versus-spaces argument that ends when
    a pre-commit hook blocks the commit
  - 43 · the hook's config, line by line (annotated code)
  - 44 · the other moments git can run a hook, and other hook managers
- Slides 45–50 · **step-04 · Documentation from the code**
  - 45 · "Documentation, just before a holiday" (CommitStrip): "documentation" that is only
    comments repeating each function's name
  - 46 · the program documents itself: `babykev docs list`, `module`, `check`
  - 47 · types and docs written once: the docment
  - 48 · the gaps: 50 of 88 functions typed and documented
  - 49 · the site is built from the same text (Quarto)
  - 50 · docments and the formatter: why lines stay at 100 characters
- Slides 51–52 · **step-04b · Every function documented**
  - 51 · 84 gaps filled; `just docs check` joins `just check`
  - 52 · what documented code looks like: a function and a pydantic field
- Slides 53–75 · **step-05 · A second file: model.py**
  - 53 · `model.py` in four ideas: pack, mask, restart the positions, point
  - 54 · packing: one sequence for everything
  - 55 · the mask as designed: questions cannot see each other
  - 56 · the pointer head: compare, do not classify
  - 57 · what is trained: about 494 M parameters frozen, about 9.3 M trained
  - 58 · fixtures: what a test needs, passed to it
  - 59 · writing a fixture (from a helper function to a fixture)
  - 60 · `conftest.py`: fixtures for every test file
  - 61 · fixtures in use: three tests
  - 62 · the tiny model: a test that uses it
  - 63 · the tiny model: where `model` and `tok` come from
  - 64 · the tiny model: what the two builder functions build
  - 65 · the tiny model: why it is enough; "hermetic"
  - 66 · kinds of tests (table)
  - 67 · what a smoke test is
  - 68 · the smoke on the real model: 6 of 15 right
  - 69 · ty: a type checker
  - 70 · ty's six findings
  - 71 · five of them come from one call
  - 72 · the mask as it should be, token by token (6×6 grid)
  - 73 · "All green, and the mask is wrong"
  - 74 · a plain Python check that sees the bug, but is not a test
  - 75 · "Normally we would fix before we commit" (the Pavlos cartoon; a joke that the
    speaker committed the bug and left for Pavlos's class)
- Slides 76–86 · **step-05a · The tests that could tell**
  - 76 · the two problems left over from step 05: types and the mask
  - 77 · the tiny model again: how a test gets it
  - 78 · test properties, not examples
  - 79 · a picture checks one size
  - 80 · hypothesis: state the rule, let the computer try the shapes
  - 81 · hypothesis finds the failing size on its own
  - 82 · how isolation was tested
  - 83 · the tests see the bug (8 failed, 95 passed), and the one-line fix
  - 84 · the smoke on Qwen again: 4 of 15
  - 85 · the type problem: two guards
  - 86 · ty joins `just check`
- Slides 87–100 · **step-05b · Two images from one lockfile**
  - 87 · not everyone has a Mac
  - 88 · "How Docker was born" (the "it works on my machine" meme)
  - 89 · two images from one lockfile: dev and run
  - 90 · the run image is built in stages, and only the last one ships (annotated)
  - 91 · the dev image: the same Python, with the tools (annotated)
  - 92 · `just image`: build, shell, start, run
  - 93 · hadolint: a linter for Dockerfiles
  - 94 · what should not go in the hook?
  - 95 · kinds of tests, and which can run on every commit
  - 96 · "2 unit tests, 0 integration tests" (GIF)
  - 97 · hermetic, by experiment (`--network none`)
  - 98 · a test is anything that can fail and stop you
  - 99 · "You may even call it a gate" (meme)
  - 100 · the docs, published to GitHub Pages

## Key ideas

1. **An ML project is mostly a software project.** Of the 26 aspects the speaker lists for an ML
   project, only 9 (data and model) are about ML. The rest is engineering. In a real ML system
   the ML code is a small box among configuration, data, serving, monitoring and more. (4–6)
2. **One environment from one lockfile.** People write `pyproject.toml` and state loosely what
   the project needs. uv writes `uv.lock`, which pins every package exactly, for every platform.
   Both files are committed. `uv sync --locked` installs exactly the lock. If a new package would
   need an upgrade, it stops with an error instead of upgrading silently; the lock changes only
   when someone runs `uv lock` on purpose. The justfile sets `UV_LOCKED=1`, so every recipe
   behaves this way. (14–15, 39)
3. **One named interface for every task.** A just recipe gives each task a name. Whoever calls
   it (a person, an agent, the git hook or CI) doesn't need to know the command behind it, so the
   command can change while the call stays the same. Extra words pass through to the tool behind
   the recipe. (16, 18–20)
4. **Developer tools stay out of what ships.** Dependency groups (`test`, `lint`, `dev`) hold
   the packages only developers need. `uv sync --no-dev` builds an environment with only what the
   program needs to run, which is what goes into the run image. (32, 90)
5. **The contract is checked at the door.** `api.py` defines requests and answers as pydantic
   models. Bad input is refused before any code runs. Three kinds of question (yes/no, named
   options, ordered levels) all become one thing: a list of options that the model points at.
   (21–24)
6. **A failing test can be the right test.** Test normal inputs, edge cases and invalid inputs.
   On day one, two edge-case tests failed: a pure guess was reported as half-confident, and 77
   rounded probabilities added up to 0.77. The tests were right. The fix changed the code, not
   the tests. kev's author only found these bugs days later. (25, 27–28)
7. **pytest gives you fixtures and parametrize.** A fixture is a named argument: pytest builds
   it and passes it in. Some are built in (`monkeypatch`, `capsys`); your own go in
   `conftest.py`. A fixture's scope decides whether it is built once per run or fresh for each
   test. `parametrize` turns one function into several tests. (26, 58–61)
8. **A formatter rewrites; a linter reports.** A formatter changes how the code looks, never
   what it does. It has almost no options, so nobody argues about style any more. A linter finds
   some genuinely wrong code (an undefined name, a mutable default). Tools fix most findings
   automatically. The rest need a person, or an agent. (29–31, 33)
9. **One command is the gate.** `just check` runs the format check, the linter, the tests with a
   90% coverage floor, and the config-file checks. The docs check joins it at step 04b and the
   type check at step 05a. (35, 51, 86)
10. **Configuration files get checked too.** YAML, `pyproject.toml`, the lockfile, the justfile
    and later the Dockerfile each have a checker: yamllint, validate-pyproject, `uv lock --check`,
    just's own formatter and hadolint. A broken hook config would break every commit, so the
    checker should catch it first. (36–40, 93)
11. **The hook makes the gate automatic.** `pre-commit install` writes a small,
    machine-specific script into `.git/hooks/`. That script only hands over to pre-commit. The
    hook runs `just check`, so the hook and your terminal run the same thing. Two more hooks
    refuse files over 1 MB and any `.env` file. A commit that fails the check never happens.
    `.git/hooks/` is not part of the repository, so every clone installs its own hook through
    `just setup`. (34, 41, 43–44)
12. **Documentation comes from the code.** The type goes in the signature. The meaning goes in a
    comment beside each parameter (a "docment"). The purpose goes in the docstring. Each is written
    once, so they can't disagree. `babykev docs check` counts the gaps and becomes part of the
    gate. Quarto builds a site from the same text. (46–52, 100)
13. **The model in four ideas.** Pack the state and every question into one sequence. Mask it so
    each question sees only the state and itself. Restart the positions so that every question
    sits right after the state. Score each option against its question's `<decide>` token. One
    forward pass then answers every question as if each had been asked alone. (53–56)
14. **A tiny model makes the model tests hermetic.** The tests use a tokenizer with one token per
    character (106 tokens) and a 2-layer Qwen2 backbone with 24,224 random but seeded weights, both
    built in memory. That means no download, no GPU, and a few seconds per run. It is enough
    because the tested facts (which token sees which, where positions start, which parameters get
    gradients) hold for any weights. It can't tell whether the answers are any good. Testers call
    such a stand-in a "fake". (62–65)
15. **Name the kind of test by what runs in it.** Unit: one function. Integration: several of our
    parts, with stand-ins for whatever comes from outside. End-to-end or system: the whole program
    with its real parts. Smoke: a quick end-to-end run that asks only whether the program starts
    and answers. Acceptance: whether a promise to users is kept (babykev has none yet). A test's
    name says what it calls, not what kind of test it is. A test is hermetic when only our code
    can make it fail. (65–67, 95)
16. **A type checker reads code; it doesn't run it.** ty compares every call and return with the
    declared types. It believes the library when the library says a call may return one number,
    even though the code works at run time. Two small guards fix that, and then ty joins the gate.
    (69–71, 85–86)
17. **Green does not mean correct.** At step 05 the gate reports 92 tests passing, 94% coverage
    and 139 of 139 functions documented. Yet the mask lets question 2 see question 1. Coverage
    counts the lines that ran, not whether anyone checked what they produced. (72–74)
18. **Test properties, not examples.** A hand-drawn picture checks one request size. Instead,
    state each rule once: isolation, packed equals separate, order doesn't matter, no question
    sees another. Then hypothesis draws request shapes (4,686 are possible) and shrinks any
    failure to the smallest shape that still breaks the rule. (78–81)
19. **A gate refuses only what its tests can see.** With the new tests, putting step 05's bug
    back gives 8 failed and 95 passed, and the hook refuses the commit. At step 05 the same commit
    went through. The fix is one line. (82–83)
20. **An untrained model's score means nothing.** The smoke on the real model got 6 of 15 right
    with the wrong mask and 4 of 15 with the right one. Pure guessing expects 4.75. A smoke proves
    the pieces fit together, not that the answers are good. (67–68, 84)
21. **Two images, one Dockerfile, one lockfile.** The dev image has every tool and starts a shell
    on your mounted folder; it is for working on the project and for CI. The run image has only
    Python and the program; it is built in stages and only the last stage ships. Packages go in
    before code, so a code change doesn't reinstall torch. In a container on the CPU it gives the
    same 15 answers as the Mac's GPU, eight times slower. (87–92)
22. **Only hermetic checks belong in the hook.** A check that needs the network, a download, a
    GPU or a lot of time can fail for reasons outside our code. A hook that fails like that is
    not trusted, and people learn to skip it. Such tests get a marker (`system`) and stay out of
    `just test`. You prove a check is hermetic by running it with the network off. (94–97)
23. **A test is anything that can fail and stop a commit, so call it a gate.** Most of babykev's
    gates are not pytest (ty, ruff, docs check, the config linters), but all are just recipes. The
    closing meme suggests that a gate is what keeps a coding agent's attention. (98–99)

## Diagrams

Memes, comics and photos (decoration with a point, not mechanisms): 2 and 75 (the Pavlos
cartoon), 3 (the speaker's T-shirt), 17 (xkcd 1319: in "theory" a burst of coding gives way to
automation and free time; in "reality" writing code turns into debugging, rethinking and endless
"ongoing development", with no time left for the original task; an ironic "Why automate"), 24
(xkcd 327: a school loses its records to a student named with an SQL injection, so check what
comes in), 42 (CommitStrip: two developers argue about tabs and spaces until a pre-commit hook
blocks the commit, "Tab must be used to indent lines"), 45 (CommitStrip: "documentation" made of
comments that only restate each function's name), 88 ("It works on my machine" / "Then we'll ship
your machine" / "And that is how Docker was born"), 96 (two window handles that each work and
block each other: "2 unit tests, 0 integration tests") and 99 (the distracted-partner stock
photo: the figure labelled "agent" turns to look at "gate" while "general test" looks on).

The deck uses one visual pattern again and again: **annotated code.** A grey code panel sits on
the left and short notes on the right. An orange arrow runs from each note to its line, and
square brackets group lines that share a note (18, 19, 43, 90, 91). A scene can reuse it as a
code panel with call-outs that appear one at a time.

- **4 and 6 · two inventories.** Each is a two-column table. Slide 4 has eight rows: Design,
  Data, Model, Developing, Utilities, Testing, Reproducibility, Production. Together they hold 26
  aspects (for example Data: Preparation, Exploration, Preprocessing, Distributed). Slide 6 has
  nine rows: Source, Environment, Code, Quality, Tests, Documentation, Automation, Shipping,
  Running. Some items are underlined. The deck doesn't say why, but they match what the babykev
  project touches (Environment, Code, Quality, Tests, Documentation and Automation are fully
  underlined; Running is not). Purpose: the punch line "9/26": only Data (4) and Model (5) are
  ML. A re-draw can show 26 tiles and light up the 9 ML ones.
- **5 · the ML code is a small box.** A light-grey canvas packed with twelve pale boxes of
  different sizes: Configuration (tall, left), Automation (below it), Data collection (top),
  Data verification, Feature engineering (bottom), Testing and debugging, Resource management,
  Model analysis, Process management, Metadata management, Serving infrastructure (right) and
  Monitoring (bottom right). One small, darker box in the middle is labelled "ML code". The
  credit is Google Cloud's MLOps article, after Sculley et al. (NeurIPS 2015). Purpose: the
  model is a small part of the system. A re-draw can show the ML code box alone, then grow the
  others around it.
- **10 · one request, one answer.** Two stacked code panels. The request: a `state:` sentence
  about Roquefort, then `questions:` `milk` (a `choice` among cow, goat, sheep, buffalo and
  mixed), `vegetarian` (a `noul`, commented "yes or no") and `intensity` (a `score` over the
  levels mild, medium, pronounced and strong). The answer: `milk` sheep with confidence 0.81,
  `vegetarian` 0.08, `intensity` score 2.7. Caption: every answer is a probability, and no text is
  generated. Purpose: the input and output shape of the whole project.
- **11 · the decision pipeline.** Four rounded boxes in a row, joined by arrows:
  - "A request" (grey): a state, and questions, each with its options;
  - "Pack" (blue): everything into one sequence of tokens;
  - "Qwen2.5-0.5B" (green): a small language model with a LoRA adapter and a special mask;
  - "Pointer head" (orange): scores each option against the decision token.

  A down arrow from the head leads to a box "A probability per option" with `milk: sheep 0.81 cow
  0.12` and `vegetarian: 0.08`. Text on the left says the language model, about half a billion
  parameters, is frozen; the adapter and the head, about nine million, are trained. Bottom line:
  "Questions are not allowed to see each other." Purpose: the map that step 05 fills in.
- **14 · before uv / with uv.** A two-column mapping: pyenv → nothing (uv fetches the Python
  that `.python-version` names); venv and pip → `uv sync`; pip-tools or poetry → `uv lock`; pipx
  → `uvx ruff`; "activate the environment first" → `uv run <command>`. A re-draw can collapse
  four tool icons into one.
- **18 · the justfile, line by line.** Annotated code. Notes, top to bottom:
  - the header comment is for whoever opens the file;
  - `program := "babykev"` is a variable;
  - `set positional-arguments` passes each word after a recipe's name to its commands whole
    (`"$1"`, `"$2"`, `"$@"`);
  - `[private]` keeps a recipe out of the list, `default` is the recipe that bare `just` runs,
    and `@` runs a command without echoing it;
  - the comment above a recipe is its description in the list;
  - `[no-exit-message]` stops just adding its own failure line;
  - `help *verb` takes any number of words, and `#!` makes the body one shell script;
  - `[group('setup')]` puts a heading in the list;
  - `setup *args` uses just's own `{{ if … }}`, so `just setup help` explains the recipe and
    `just setup` runs `uv sync --locked`.
- **19 · the help recipe, line by line.** The same pattern, zoomed in on `help`. It does four
  things in order: with no words, print the list; otherwise fetch the recipe's text with
  `just --show`; print its first line (the description, with the `#` removed); and if the recipe
  runs the program under the same name, also ask the program for its own help. Below are two
  terminal runs: `just help setup` prints the description, and `just help nosuch` prints just's
  "does not contain recipe" error.
- **28 · the confidence yardstick, worked through.** No picture, just numbers that make a good
  scene. A score has three levels (0, 1 and 2 steps from the first), and a pure guess gives each a
  third. The answer's spread is the expected distance from the most likely level, which here is
  ⅓×0 + ⅓×1 + ⅓×2 = 1 step. Confidence is 1 minus spread divided by a yardstick.
  - **Old yardstick:** the whole scale, 2 steps, so confidence is 1 − 1/2 = 0.5, which is wrong.
  - **New yardstick:** how spread out a guess is around the middle level, ⅓×1 + ⅓×0 + ⅓×1 ≈ 0.67
    steps. Then 1 − 1/0.67 = −0.5, which is clipped to 0.

  The second fix: 77 options rounded to two decimals give 0.01 each, which sums to 0.77.
  Rounding to four decimals fixes it. A re-draw: three bars on a number line with distance
  brackets, then two rulers of different lengths.
- **31 · the findings funnel.** A small table: 79 findings at the commit, 70 after `just fmt`,
  69 after `just lint --fix`, 37 after `just lint --fix --unsafe-fixes`. The rest need a person.
  A re-draw can show a bar shrinking in steps.
- **34 · the hook's hand-over chain** (code, but the chain is the point). Before a commit, git
  runs `.git/hooks/pre-commit` if it exists. The generated file holds the path to this machine's
  `.venv` Python and starts `pre_commit` with the config `.pre-commit-config.yaml`. Because the
  path belongs to one machine, the file is never committed. Two lines (`#!/bin/sh` and
  `just check`) would do the same job. A re-draw: git → hook file → pre-commit → config → `just
  check`.
- **35–36 · what `just check` is made of.** Four lines (`just fmt --check`, `just lint`,
  `just test -q --cov-fail-under=90`, `just lint-config`). `lint-config` opens into a table of four
  checks with "The file it reads" and "New package?" columns: yamllint (every YAML file, yes),
  validate-pyproject (`pyproject.toml`, yes), `uv lock --check` (`uv.lock` against
  `pyproject.toml`, no, it's uv), `just --fmt --check --unstable` (the justfile, no, it's just).
  `set -e` stops at the first failure. A re-draw: a gate built from stacked checks, one of which
  unfolds into four.
- **43 · the hook's config, line by line.** Annotated YAML with two sources of hooks.
  - **The remote repo** `pre-commit-hooks` at `v6.0.0`, downloaded once and cached. It provides
    `check-added-large-files` with `--maxkb=1000` and `check-merge-conflict`, which refuses
    leftover `<<<<<<<` markers.
  - **`repo: local`**, with nothing to download. It holds two hooks of babykev's own:
    - `no-env-file`: `language: fail` (it does nothing but fail) on any file matching a `.env`
      name in any folder. Its message says a `.env` holds one machine's settings and secrets and
      is never committed.
    - `check`: `entry: just check` with `language: system` (the command as installed on this
      machine). `pass_filenames: false` and `always_run: true` make it run once on every commit,
      whatever changed.
- **44 · when git runs hooks.** A three-column table (hook / when git runs it / what it is for):
  - pre-commit, before a commit is made: refuse what must not go in ("Ours");
  - commit-msg, on the message: require a shape for it;
  - pre-push, before a push: checks too slow for every commit;
  - post-checkout and post-merge, after moving to another commit: follow the move, for example
    update the environment;
  - prepare-commit-msg, pre-rebase and post-commit, around a commit: templates, guards, notices.

  Text: a hook is like a callback in a training loop, code that runs at a set moment. Servers such
  as GitHub have server-side hooks of their own. A re-draw: a git timeline (edit → commit → push →
  checkout) with a flag at each hook moment, and only the pre-commit flag lit.
- **48 · the gaps.** A table of typed-and-documented counts per file: `babykev.docs` 26 of 26,
  `babykev.cli` 1 of 1, `babykev.api` 0 of 12, `test_api.py` 23 of 29, `test_cli.py` 0 of 4,
  `test_docs.py` 0 of 16. That makes 50 of 88, with 84 gaps in all. A re-draw can use one progress
  bar per file.
- **54 · packing: one sequence for everything.** Three rows of token boxes.
  - Segment 0, "the state" (positions 0 … S−1): an orange `<state>` box, then one long blue box
    with the Roquefort text.
  - Segment 1, "question 1" (positions S, S+1, …): `<q>`, then "Which milk?", `<opt>`, cow,
    `</opt>`, `<opt>`, sheep, `</opt>`, `<decide>`.
  - Segment 2, "question 2" (positions S, S+1, … **again**): `<q>`, then "Vegetarian?", `<opt>`,
    no, `</opt>`, `<opt>`, yes, `</opt>`, `<decide>`.

  Legend: orange fill = a delimiter token; blue = the caller's text; green with a thick border = a
  delimiter the answer is read from (`</opt>` and `<decide>`). Caption: five delimiter tokens mark
  the parts, and a caller's text can never produce one. Purpose: show packing and the position
  restart. A re-draw should animate each question's position counter jumping back to S.
- **55 · the mask, as designed.** A 3×3 grid. Rows: "A token of …" the state / question 1 /
  question 2. Columns: "… may look at earlier tokens of" the state / question 1 / question 2.
  - Green "yes": state→state, q1→q1, q2→q2. Green "yes, all of it": q1→state, q2→state.
  - Grey "no: it comes later": the three cells above the diagonal.
  - **Red, thick border: "NO, hidden by the mask"** in the q2→question-1 cell.

  Notes on the right: question 2 gets the same answer whether or not question 1 was asked; an
  ordinary causal mask would say yes in the red cell; "That one cell is the whole difference", with
  a red line from the cell. The rule underneath: `attend(i, j) if j <= i and (seg[j] == 0 or
  seg[j] == seg[i])`. A re-draw: start from a plain causal triangle, then flip the one block to
  red.
- **56 · the pointer head: compare, do not classify.** Under "What the model computed at …", on
  the left: a green `<decide>` box, and below it three green boxes `</opt> cow`, `</opt> sheep`,
  `</opt> goat`.
  - `<decide>` → an orange box "Linear q, to 256 numbers".
  - The option boxes → an orange box "Linear k, to 256 numbers, per option".
  - Both curve into a blue "dot product: one score per option" → a blue "softmax: scores to
    probabilities" → cow 0.12, sheep 0.81, goat 0.07.

  Caption: the options are compared with the question, so there is no fixed list of classes: any
  number of options, any text. It works like a single attention query: one query against several
  keys.
- **57 · what is trained.** Table: Qwen2.5-0.5B about 494 million, frozen; the LoRA adapter
  (rank 16) about 8.8 million, trained; the pointer head about 0.5 million, trained. The smoke run
  prints 503 M parameters, 9.3 M trainable. A re-draw needs a log scale, or a 494-block square
  with a sliver highlighted.
- **58–63 · how fixtures reach a test** (code slides; the wiring is the diagram).
  - Three fixtures live in `tests/conftest.py`: `tok` (scope `session`: built once per run),
    `model` (which itself asks for `tok`; rebuilt for each test) and `record` (one request with
    three questions; rebuilt for each test).
  - They are built by two ordinary functions in `tests/tiny.py`, `tiny_tokenizer` and
    `tiny_backbone`. These are deliberately not fixtures: the adapter test needs a tiny model
    *with* an adapter (`lora=4`), so it calls the builder itself.
  - Usage: 8 test functions use the fixtures (all 8 use `tok`, 4 use `record`, 2 use `model`).
    pytest runs them as 12 tests, because one function runs once for each of the five
    delimiters.

  A re-draw: tests on the right, fixtures in the middle, builders on the left, with arrows for
  "asks for". A session fixture is drawn once and shared; a per-test fixture is a stack of fresh
  copies.
- **64 · the tiny model next to the real one.** Tokenizer: 100 printable characters + 5
  delimiters + `[UNK]` = 106 tokens, so "Roquefort" is 9 tokens. Backbone: Qwen's own `Qwen2Model`
  built small, 2 layers of width 32 instead of 24 layers of width 896, with 24,224 random seeded
  parameters against 494 million. A re-draw: two stacks of layers drawn to scale.
- **66 and 95 · kinds of tests.** Tables with the columns Kind / What it runs / Our example / Is
  ours hermetic?
  - unit: one function (a confidence function on a list of numbers): yes;
  - integration: several of our parts, with stand-ins for what comes from outside (packing, the
    mask, the model and the head on the tiny model): yes;
  - end-to-end or system: the whole program with its real parts: no;
  - smoke: a quick end-to-end run (`just smoke local`): no;
  - acceptance: a requirement such as an answer within 50 ms: none yet.

  On 66 (step 05) the end-to-end example is the whole smoke on the real model. On 95 (step 05b)
  it is `test_real_model.py`, marked `system`. A re-draw: nested boxes that widen (one function →
  our parts with a fake model → the whole program, the real model and the network), with a dashed
  "hermetic" border that the last box crosses.
- **70–71 · six findings, two causes.** A table (where / code / what ty says):
  - `model.py:68` `invalid-return-type`;
  - `model.py:97` `not-iterable`;
  - `test_model.py:49` `not-iterable`;
  - `test_model.py:100` `not-subscriptable`;
  - `test_model.py:111` `invalid-argument-type`;
  - `test_model.py:120` `not-iterable`.

  Five trace back to one call that the library declares as returning `int | list[int]`. A
  re-draw: one source call fanning out into five red marks.
- **72 · the mask, token by token.** Six tokens: 1–2 state, 3–4 question 1, 5–6 question 2. The
  rows read `#.....`, `##....`, `###...`, `####..`, `##..#.`, `##..##` (`#` = may look, `.` =
  may not). Everything right of the diagonal is `.`, and rows 5–6 have `.` in columns 3–4.
- **73 · should be / step 05 builds.** The same six rows side by side. The built rows 5 and 6
  read `#####.` and `######`. The cause is one line (`model.py` line 140), where `ones_like` makes
  "same question" true for every pair. A re-draw: two grids, with rows 5–6 of the right one
  flashing.
- **74 · a check that sees it, but isn't a test.** A five-line function prints the wanted row,
  the built row, and "ok" or "WRONG". The first four rows are ok; rows 5 and 6 are WRONG. Nothing
  in `just check` runs it.
- **79 · a picture checks one size.** A wrong "fix" blocks only the question right before. The
  two-question picture can't tell, so it prints ok six times. A second picture for parts
  `[0, 1, 2, 3]` (one state token, three one-token questions) is needed: wanted `#...`, `##..`,
  `#.#.`, `#..#`; the wrong fix gives a fourth row of `##.#`, so question 3 sees question 1.
  Covering 1–6 state tokens and 0–4 questions of 1–5 tokens would take 4,686 such pictures.
- **81 · allowed ∩ siblings.** For the shrunk shape `(1, [1, 1, 1])`, two 4×4 grids side by
  side. "allowed" (the mask) reads `#...`, `##..`, `#.#.`, `##.#`. "siblings" (pairs in two
  different questions) reads `....`, `..##`, `.#.#`, `.##.`. The rule says no cell may be yes in
  both. Row 4, column 2 is, so the assert fails. A re-draw: lay one grid over the other and light
  up the overlap.
- **82 · the isolation test as an experiment.** Score the three-question record, rewrite question
  2 (three options become two: "Where from?" Spain or Italy), and score again. Questions 1 and 3
  must not move, and question 2 must now have a different number of scores. With step 05's mask,
  question 3's scores move from about −0.230/−0.233/−0.234 to −0.227/−0.230/−0.231, while
  question 1 (which comes first) stays put. A re-draw: three meters; change question 2 and watch
  question 3's needle twitch.
- **84 · the smoke tally.** 6 of 15 right with the wrong mask, 4 with the right one, 4.75
  expected by chance (five yes/no questions at ½, five 5-option at ⅕, five 4-level at ¼). It
  makes a good bar chart with a "chance" line.
- **89–91 · two images from one Dockerfile.**
  - **89**, a table. Dev: every dependency plus the dev tools, uv, just, Quarto and git; starts a
    shell with your folder mounted; for working on any system and for CI; 1.84 GB. Run: Python and
    what the program needs; starts `babykev`; for a platform that runs the program; 1.15 GB.
  - **90**, annotated, the run image. Stage 1 `uv` is uv's own image; nothing runs in it, and the
    next stage copies the uv binary out. Stage 2 `build` is a fresh Python that is not shipped. It
    copies the lock files and installs the packages without the project; that layer is reused
    until the lockfile changes. Then it copies `src` and installs the project, so a code change
    reinstalls one package, not torch. Stage 3 `run` is a fresh Python that copies only the
    finished `/opt/venv` and `data`, with no uv, just, Quarto or build leftovers. Its
    `ENTRYPOINT ["babykev"]` with `CMD ["help"]` means no word gives help.
  - **91**, annotated, the dev stage: its own fresh Python, sharing nothing with build or run. It
    gets git and curl from Debian, Quarto from its release, uv copied from stage 1, just from PyPI,
    and every folder marked `safe.directory` (the mounted folder belongs to the host's user). The
    packages, with the dev group, go in first, then the whole project. It exposes port 8765 for the
    step browser and starts `bash`.

  A re-draw: three boxes left to right (uv → build → run), the first two greyed out as "not
  shipped", `COPY --from` arrows between them, and a separate dev box branching off uv.
- **92 · who runs what.** `just` runs on the host and calls `docker`. The run image has no just,
  so `just image run smoke` becomes `babykev smoke` inside the container. In the dev image every
  recipe works as on the Mac. An image is a file on disk; a container is a running copy of it. A
  re-draw: a host box (just) → docker → a container box (babykev).
- **97 · hermetic, by experiment.** Under `--network none`: `just check` passes; `just test -m
  system` with the model already cached passes; the same with an empty cache fails (it can't
  reach the Hub). Whatever still passes with the network pulled can run on every commit.
- **98 · every gate in one table.** Columns: what is checked / how / recipe / on every commit?
  - functions, the mask and the model: pytest, hypothesis and the tiny model; `just test`; yes;
  - types: ty; `just types`; yes;
  - documentation: `babykev docs check`; `just docs check`; yes;
  - format and lint: ruff; `just fmt --check` and `just lint`; yes;
  - config files and the Dockerfile: yamllint, validate-pyproject, uv and hadolint;
    `just lint-config`; yes;
  - the real model from the Hub: the smoke, marked `system`; `just test -m system`; no, not
    hermetic.

  Caption: most of these are not pytest; all of them are just. A re-draw: a turnstile whose
  scanners are these six rows, with the last one standing outside the gate.

## Terms the lecture uses

| Lecture term | Slides | Note on the tutorial README / digest |
|---|---|---|
| "Software Development for Machine Learning" | 1 | The course site's name for L09 is "Automating Software Development: CI, unit testing" (digest title). |
| "babykev", "kev", "jev", "a decider model", "a special head" | 8 | babykev is the walk's repo. kev and jev are the speaker's other projects; neither is in the course repos. |
| "step" (`step-00` … `step-05b`) | footers, 12–13 | git tags in `babykev`; the digest's Track B follows them. |
| "state", "questions", "options", "`noul`", "`choice`", "`score`", "confidence" | 10, 22, 27–28 | "noul" is babykev's name for a yes-or-no question, not a typo. |
| "the contract" (`api.py`), `SystemOneRequest` | 21 | No counterpart in the cheese README, whose "API" is a FastAPI service (`api/service.py`). |
| "recipe", "justfile", "the project's interface", "verb", `[group]` | 16, 18–20 | The cheese README has no task runner. It types raw `docker run … pytest …`, `black`, `flake8` and `pre-commit` commands. |
| "lockfile" (`uv.lock`), "locked" | 12, 15, 39, 89 | The cheese repo has no lockfile: `pip install` from `>=` pins (digest E20). |
| "dependency groups"; "sequester packages only developers need" | 32 | The cheese `pyproject.toml` lists black, flake8, pre-commit and pytest as runtime dependencies. |
| "formatter" / "linter" | 29–30 | The README uses the same words ("Black formatter", "Flake8 linter"), but the tools differ: `ruff format` / `ruff check` here, black / flake8 there. Line length: 100 here, 120 in the cheese hook (digest E5). |
| "findings", "rules" (E, W, F, I, B, UP, SIM, S, N, ANN, D1), "unsafe fixes" | 30–31 | The cheese hook runs flake8 with no plugins, so it reports only pycodestyle (E, W) and pyflakes (F) codes. Families such as B, S, N, ANN and D have no counterpart there. |
| `just check`: "everything a commit must pass"; "coverage floor" | 7, 35 | The cheese repo has no single gate command, and its README never sets a coverage floor (Milestone 5 asks for 70%, digest §3.6). |
| `lint-config` | 36 | The cheese hook's `check-yaml` / `check-json` are the nearest equivalent. |
| "git hook", "the hook", "hooks on dev", "server-side hooks" | 6, 34, 41, 44 | README: "Pre-commit hooks" for "local code quality checks (linting/formatting)". In the cheese repo the hook runs **no tests**; in babykev it runs everything through `just check`. |
| "docment" | 47, 52 | fastcore's term. Not in the tutorial. |
| "gaps", `docs check`, "Guide" | 48, 51, 100 | Not in the tutorial. |
| "segment", "delimiter token", `<decide>`, "pack/packing", "restart the positions", "pointer head", "the mask", `branch_mask` | 53–56, 72–74 | babykev only. |
| "frozen" / "trained", "LoRA adapter, rank 16" | 11, 57 | Same vocabulary as L08 (LoRA). |
| "fixture" (pytest's own vs "ours"), `scope="session"`, `conftest.py` | 26, 58–61 | The cheese README never says "fixture", and the cheese tests use none. |
| "stand-in", "fake", "the tiny model" | 58, 62–65 | Not in the tutorial. |
| "hermetic" | 65–66, 95, 97–98 | Not in the README. Its nearest line: system tests "will skip if the server isn't running" (README:202). The digest adopts the lecture's term (§3.3). |
| "Kind:" unit / integration / "End-to-end, or system" / smoke / acceptance | 25–27, 61–62, 66, 68, 81–82, 95 | README: "The Testing Pyramid" with three layers. **Integration** there means FastAPI's `TestClient` in-process; here it means our parts with a fake model. **System** there means a live server over HTTP; here it means the real model from the Hub. The slides never say "pyramid". The course site promises acceptance tests; the slides say "none yet" (digest E4). |
| "marker" (`system`), `-m NAME` | 95, 97 | The cheese repo defines `unit`, `integration` and `slow` markers but never uses them, and guards its system tests with `skipif` instead (digest E11). |
| "property tests", "Test properties, not examples", "shrinks" | 6, 78–81 | Not in the tutorial (hypothesis). |
| "type checker", `ty` | 69–71, 85–86 | Not in the cheese tutorial. |
| "smoke", "smoke test" | 67–68, 84 | Not in the README. |
| "dev image", "run image", "stage", "only the last one ships" | 89–91 | The cheese repo has one image, `cheese-app-api:local`. Its Dockerfile is commented "Multi-stage" but has a single `FROM` (digest E14). |
| "image" vs "container" | 92 | Same words as L02–L04. |
| "gate" | 99 | The digest uses "gate" throughout (§1, §3.5). Slide 99 is where the lecture names it. |
| "agent(s)" | 7, 20, 33, 46, 99 | The lecture counts AI coding agents among those who run recipes, fix findings and read the docs. |
| "CI", "continuous integration" | 6, 20, 89 | README Part 5, "GitHub Actions (Remote CI)", which this series covers in L21. |

Slips on the slides, so a scene does not copy them:

- Slide 4 says "9/26 lessons aspects": the count is of aspects, not lessons.
- Slide 69 has "Here we will we run ty by hand", and twice says "negative ty finding(s)" where it
  means any ty finding.
- Slide 75 spells "comitted".
- Slide 31 leaves 37 findings and slide 33 says 36; the difference is one docstring written by
  hand during the demo.
- Slide 17's comic argues that automation can cost more than it saves, so the title "Why
  automate" is ironic.

## Commands and code on the slides

Single lines only; multi-line files are described under Diagrams. Grouped by step.

**step-00 · uv and just**

- 14 · `uv sync` · `uv lock` · `uvx ruff` · `uv run <command>`: what replaces pyenv, venv and
  pip, pip-tools or poetry, and pipx
- 15 · `uv sync --locked` · `UV_LOCKED=1`: install exactly the lock; the justfile sets the
  variable for every recipe
- 16 · `just setup` · `just --show setup`: run a recipe; print what is behind it
- 18 · `program := "babykev"` · `set positional-arguments` · `@just --list --unsorted` ·
  `[group('setup')]`: justfile lines
- 18 · `@{{ if args == "help" { "just help setup" } else { "uv sync --locked" } }}`: the `setup`
  recipe's body
- 19 · `shown=$(just --show "$1") || exit 1`: the `help` recipe fetches a recipe's text
- 19 · `just help setup` · `just help nosuch`: the first prints the description; the second gives
  ``error: Justfile does not contain recipe `nosuch` ``
- 20 · `just help test` · `just test help` · `just --show test` · `just test -k render`: ways to
  ask; extra words go to pytest

**step-01 · the contract and its tests**

- 23 · `criteria: list[JSONContent] = Field(min_length=2, max_length=MAX_OPTIONS)`: a pydantic
  constraint
- 23 · `data/cheese/sample.jsonl`: the sample requests
- 25 · `assert choice_confidence([0.25, 0.25, 0.25, 0.25]) == 0.0`: a unit test
- 25 · `just test -k`: run a subset by name
- 26 · `monkeypatch.setattr("sys.argv", ["babykev", *words])`: fake the command line
- 26 · `@pytest.mark.parametrize("words", [(), ("help",), ("--help",), ("-h",)])`: one function,
  four tests
- 26 · `just test -k help_is_printed -v`: lists them as `[words0]` … `[words3]`
- 27 · `assert score_confidence([1 / 3] * 3) == pytest.approx(0)`: the first failing test
- 27 · `sed -n '82,86p' src/babykev/api.py` · `just test -k score_confidence_is_zero`
- 27 · `sed -n '89,90p;99p' src/babykev/api.py` · `just test -k rounded_probabilities`
- 27 · `assert 0.5 == 0 ± 1.0e-12` · `assert 0.77 == 1 ± 0.02`: pytest's failure lines

**step-02 · format and lint**

- 29 · `ruff format` · `just fmt` · `just fmt --check`: rewrite files, or only list the ones it
  would change
- 30 · `ruff rule F821` · `ruff check`: explain a rule; run the linter
- 31 · `ruff check --fix` · `just lint --fix` · `just lint --fix --unsafe-fixes` · `ruff rule CODE`
- 32 · `dev = [{include-group = "test"}, {include-group = "lint"}]`: a dependency group made of
  two others
- 32 · `uv sync --no-dev`: only what the program needs

**step-03 · the gate and the hook**

- 34 · `pre-commit install` · `.git/hooks/pre-commit`: the command and the one file it writes
- 34 · `exec "$INSTALL_PYTHON" -mpre_commit "${ARGS[@]}"`: the hand-over line in that file
- 35 · `just fmt --check` · `just lint` · `just test -q --cov-fail-under=90` · `just lint-config`:
  the four lines of `just check`
- 36 · `yamllint --strict .` · `validate-pyproject pyproject.toml` · `uv lock --check` ·
  `just --fmt --check --unstable`: the four config checks
- 36 · `just --show lint-config` · `set -e`
- 37 · `uv run yamllint --strict .` · `line-length: {max: 100}` · `ignore-from-file: .gitignore`
- 37 · `10:15 error syntax error: mapping values are not allowed`: one over-indented line in the
  hook config
- 38 · `uv run validate-pyproject pyproject.toml` · `Valid file: pyproject.toml`
- 38 · `` `project` must not contain {'requires_python'} properties ``: the error for a misspelt key
- 39 · `Resolved 29 packages`: the lock agrees
- 39 · `` error: The lockfile at `uv.lock` needs to be updated, but `--check` was provided. ``
- 40 · `+program := "babykev"` · `error: Formatted justfile differs from original.`
- 43 · `rev: v6.0.0` · `args: [--maxkb=1000]` · `- repo: local` · `language: fail` ·
  `entry: just check` · `language: system` · `pass_filenames: false` · `always_run: true`
- 44 · `git config` · `core.hooksPath`: point git at a folder of hook scripts in the repo

**step-04 / 04b · documentation**

- 46 · `babykev docs list` · `babykev docs module api` · `babykev docs check`
- 47 · `sym: Code, # A function, method or class`: a docment
- 48 · `just docs check`
- 49 · `docs/apidocs.py` · `just docs` · `docs/_site/`
- 52 · `type: Literal["noul"] = Field(description="Marks the question as yes-or-no")`

**step-05 · the model, fixtures, ty, and the bug**

- 55 · `attend(i, j) if j <= i and (seg[j] == 0 or seg[j] == seg[i])`: the mask's rule
- 58 · `@pytest.fixture(scope="session")`
- 60 · `just test --fixtures`
- 61 · `just test --fixtures-per-test -k "probabilities_sum or positions_restart"`
- 61 · `assert [len(p) for p in probs] == [2, 3, 3]`
- 63 · `DecisionModel("tiny", "cpu", lora=4, backbone=tiny_backbone(len(tok)))`: the adapter test
  builds its own tiny model
- 64 · `chars = sorted(set(string.printable))`: the tiny tokenizer's alphabet
- 68 · `just smoke local`: the smoke, on the real model
- 69 · `ty check` · `just types`
- 70 · `invalid-return-type` · `not-iterable` · `not-subscriptable` · `invalid-argument-type`:
  ty's codes
- 71 · `s_id, q_id, o_id, c_id, d_id = tok.convert_tokens_to_ids(SPECIAL)`: the line behind five
  findings
- 73 · `sed -n '140p' src/babykev/model.py`
- 73 · `same = torch.ones_like(causal) | (s[None, :] == 0)`: the bug
- 74 · `mask = branch_mask([0, 0, 1, 1, 2, 2], "cpu")[0, 0] == 0`

**step-05a · property tests and the fix**

- 77 · `sed -n '16,27p' tests/conftest.py`
- 79 · `same = (s[None, :] == s[:, None]) | (s[None, :] == 0) | (s[None, :] < s[:, None] - 1)`:
  the deliberately wrong fix
- 80 · `shapes = st.tuples(st.integers(1, 6), st.lists(st.integers(1, 5), max_size=4))`: the
  request shapes hypothesis may draw
- 80 · `@given(shapes)` · `sed -n '10p;58,59p' tests/unit/test_mask.py` ·
  `sed -n '43,51p' tests/conftest.py`
- 81 · `siblings = (seg[:, None] != seg[None, :]) & (seg[:, None] > 0) & (seg[None, :] > 0)`
- 81 · `assert not (allowed(seg.tolist()) & siblings).any()`: the rule as an assert
- 81 · `just test -k no_question_sees_another` · `shape = (1, [1, 1, 1])` ·
  `git restore src/babykev/model.py`
- 82 · `sed -n '145,157p' tests/unit/test_model.py` · `just test -k a_question_cannot_see_its_sibling`
- 82 · `assert torch.equal(before[0], after[0])`
- 83 · `just test`, which prints 8 failed, 95 passed · `sed -n '151p' src/babykev/model.py`
- 83 · `same = (s[None, :] == s[:, None]) | (s[None, :] == 0)`: the fix
- 85 · `sed -n '64,80p' src/babykev/model.py` · `return ids if isinstance(ids, list) else [ids]`
- 85 · `raise TypeError(f"{name} has no tokenizer this model can use")`
- 86 · `just --show check` · `just check`

**step-05b · images, markers, publishing**

- 90 · `FROM ghcr.io/astral-sh/uv:0.12.13 AS uv` · `FROM python:3.13-slim-trixie AS build`
- 90 · `RUN uv sync --locked --no-dev --no-install-project` · `RUN uv sync --locked --no-dev --no-editable`
- 90 · `COPY --from=build /opt/venv /opt/venv` · `ENTRYPOINT ["babykev"]` · `CMD ["help"]`
- 90 · `docker build --target run`: stops at the stage named `run`
- 91 · `FROM python:3.13-slim-trixie AS dev` · `ARG JUST=1.50.0` · `ARG QUARTO=1.8.26`
- 91 · `RUN UV_COMPILE_BYTECODE=1 uv sync --locked --no-install-project` · `EXPOSE 8765` ·
  `CMD ["bash"]`
- 91 · `docker build --target dev`: needs only the `uv` stage
- 92 · `just image build dev` · `just image shell` · `just image start` · `just image run smoke`
- 93 · `uv run hadolint Dockerfile`
- 93 · ``DL3059 info: Multiple consecutive `RUN` instructions. Consider consolidation.``
- 93 · `DL3008 warning: Pin versions in apt get install.`: declined, with the reason written
  beside the line
- 95 · `@pytest.mark.NAME` · `-m NAME`
- 97 · `--network none` · `just test -m system`
- 100 · `just docs publish` · `gh-pages`

## What the lecture stresses

- **Most of an ML project is engineering**, and an ML project is a software project with a
  model and data in it. (4–6)
- **You install three tools; the project installs the rest** from the lockfile through
  `just setup`. (12)
- **Never let the environment drift silently.** `--locked` stops with an error rather than
  upgrade quietly, and the lock changes only when someone means it to. Both environment files are
  committed. (15, 39)
- **One interface for people, agents, the hook and CI.** The call stays stable when the command
  behind it changes. (16, 20)
- **Validate at the boundary.** Validation happens before the code runs. (23–24)
- **What to test: normal inputs, edge cases, invalid inputs.** Both day-one failures were edge
  cases. A test written on the first day finds then what a user would find later. (25, 27)
- **When a test fails, fix the code, not the test.** "The tests did not change. The code did."
  (28)
- **The formatter never changes behaviour**: after `just fmt`, the same 52 tests pass. Choose a
  formatter with no options and stop arguing about style. (29)
- **Write down why for every lint rule**: each rule in `pyproject.toml` has a comment. (30)
- **Some findings need a person**, such as a docstring, a type or a name. (31, 33)
- **The hook file is machine-specific and never committed**; every clone runs `just setup`. (34,
  44)
- **Coverage below 90% fails the check.** (35)
- **Use `--strict`**: a YAML warning counts as a failure. A broken hook config would break every
  commit. (37)
- **The hook and your terminal run the same command**, so a commit that fails the check does not
  happen. Refuse large files and `.env` secrets. (41, 43)
- **Add a hook only when something needs it.** babykev uses only pre-commit and leaves the other
  hooks until they are needed. (44)
- **Nothing written twice, so nothing can disagree.** A docment says what the type can't. (47,
  52)
- **Keep lines at 100 characters.** A longer line gets wrapped by the formatter, its docment ends
  up away from its parameter, and only `docs check` notices. (50)
- **One forward pass, every question as if asked alone**, and a caller's text can never forge a
  delimiter. (53–54)
- **The whole difference between this mask and a causal mask is one cell.** (55)
- **Compare, don't classify**: no fixed class list. (56)
- **Build fixtures fresh** so no test can spoil the next; share only what is safe to share
  (`scope="session"`). (58)
- **A fixture's data is known in advance**, so a test can expect exact numbers. (61)
- **Test what holds for any weights**: then a random tiny model is enough, and the tests run on
  every commit. (62, 65, 78)
- **Say what runs in a test.** Teams draw the lines between kinds differently. (66)
- **Run the fast, shallow smoke first**, before the slow, deep tests. It proves the pieces fit,
  not that the answers are right. (67–68)
- **ty trusts the library's declared types**: "It may be one number" is enough for a finding.
  Fix with a guard in one place. (71, 85)
- **All green can still be wrong.** Coverage counted `branch_mask` as tested because its lines
  ran. (73)
- **A printout you read by eye is not a test**, because nothing in the gate runs it. (74)
- **Normally you fix a bug before you commit.** The speaker didn't, on purpose, as a teaching
  device. (75)
- **State the rule once and let the computer try the shapes.** hypothesis looks for the case you
  didn't think of. (79–81)
- **Turn off hypothesis's 200 ms deadline, and say why in a comment.** The first torch call can be
  slow, and the test would then fail by chance. (80)
- **The gate refuses only what its tests can see.** (83)
- **Right for the wrong reason.** With the wrong mask the untrained model scored above chance by
  luck. (84)
- **Not everyone has a Mac**, and the training platforms run Linux. An image describes a Linux
  machine in one file. (87)
- **Packages first, code after**, so a code change doesn't reinstall torch. Ship only the last
  stage. (89–90)
- **A linter's rule is a default, not a law.** Decline it with the reason written beside the
  line. (93)
- **Ask of every check: can anything but our code make it fail?** Only checks where the answer is
  no belong in the hook. Otherwise people learn to skip the hook. (94)
- **An end-to-end test is never hermetic.** An integration test is hermetic only when what comes
  from outside is replaced. (66, 95)
- **Prove a test is hermetic by pulling the network.** (97)
- **A test is anything that can fail and stop a commit, and you may call it a gate.** (98–99)
- **The built site never enters `main`**; it lives on `gh-pages`. (100)

## Pointers

- **The tutorial repo.** Slide 9: `github.com/dlops-io/cheese-app-ci-cd` (QR code), "A FastAPI
  app in Docker, with linters, formatters, tests and pre-commit hooks". It is digest Track A.
  Slide 8 says it "will be released later today".
- **Later classes named on the slides.** Slide 13 says `data.py`, `train.py` and `evaluate.py`
  arrive in the "class on training", and `serve.py` in the "class on ci/cd with github actions"
  (L21 in this series).
- **babykev's own artefacts.** The step tags `step-00` … `step-05b` (footers). The sample data
  `data/cheese/sample.jsonl` (23), whose 15 questions the smoke runs (67–68). The docs site at
  `rahuldave.github.io/babykev`, built from the `gh-pages` branch, with reference pages and a Guide
  (the model in four ideas, and the mask as a grid in a notebook) (100). Port 8765 is the "step
  browser" of the dev image (91), the walk's replay page (digest B0).
- **Readings and credits.** Google Cloud, *MLOps: continuous delivery and automation pipelines in
  machine learning*; Sculley et al., *Hidden technical debt in machine learning systems*,
  NeurIPS 2015 (5).
- **Tools and sites named.** `pre-commit.com` (34); `github.com/pre-commit/pre-commit-hooks` at
  `v6.0.0` (43); husky, lefthook and overcommit as other hook managers (44); fastcore's docments
  (46); Quarto (12, 49); `ghcr.io/astral-sh/uv` (90).
- **Comics and memes** (credits on the slides): xkcd 1319 *Automation* (17) and 327 *Exploits of a
  Mom* (24), both CC BY-NC 2.5; CommitStrip *The Indentation Question*, 14 February 2013 (42), and
  *Documentation just before vacation*, 27 July 2016 (45); `imgflip.com/i/24ac74` (88); the "2 unit
  tests, 0 integration tests" GIF on giphy, credited to Randal Olson, January 2016 (96);
  `imgflip.com/memetemplate/118429510`, with the labels added by the speaker (99).
- **No homework, milestone, Ed lesson or reading list** is on the slides. The pairing with the
  course's L09 comes from the course site (digest §7). For scenes, the nearest tutorial anchors
  are:
  - 25–27 (a unit test) → cheese `tests/unit/test_utils.py` (`power()`);
  - 66 and 95, integration → cheese `tests/integration/test_api.py` (`TestClient`, in-process);
  - 66 and 95, end-to-end or system → cheese `tests/system/test_system_api.py` (live server on
    9000, `skipif`);
  - 29–31 (formatter and linter) → the black and flake8 hooks at 120 columns;
  - 34, 41 and 43 (the hook) → `pre-commit install` and the cheese `.pre-commit-config.yaml`
    (nine hooks, digest E3);
  - 89–91 (images) → the cheese single-stage `Dockerfile`;
  - 94–97 (hermetic) → the cheese system tests that silently skip without a server (digest §3.3,
    G3).
