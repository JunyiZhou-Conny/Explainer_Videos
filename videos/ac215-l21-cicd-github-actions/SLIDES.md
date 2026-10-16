# L21 lecture slides — Automating Software Development: CI/CD with GitHub Actions and other tools II

Source: one deck, `L21_cicd_with_github_actions` (35 slides), titled "Lecture 21: Automating
Software Development: CI/CD with GitHub Actions and other tools II" (AC215/E115, Pavlos
Protopapas, SEAS/Harvard). These are the instructor's lecture slides (PDF), provided by the
student for study; the PDFs are not in this repository; slide numbers are PDF page numbers.
The page numbers printed in the slide footers drift from slide 16 on (slide 16 prints "17",
slides 17–35 print "19"–"37"), so two pages of the original deck are missing from the PDF; this
file always uses the PDF page. This digest was written from the deck's extracted text and from
every contact sheet, with enlarged tiles for slides 11, 18, 21, 28 and 29. Everything below is
paraphrased; only short titles, terms, URLs and single code lines are quoted. The tutorial side
of the lecture is in [`digest.md`](digest.md).

## Outline

The deck has four sections (slide 4). Divider slides repeat the outline with the current section
in bold. Two recap slides come before the first outline.

- Slide 1 · title slide
- Slides 2–3 · **Recap: local Git hooks** (no section number)
  - 2 · "Git Hooks": last lecture's local hooks, with `pre-commit` and `pre-push` as examples
  - 3 · their limitation: they run only on one developer's machine; "That's where remote hooks
    come in."
- Slides 4–7 · **Remote Git Hooks**
  - 4 · outline / section divider ("Remote Git Hooks" in bold)
  - 5 · what remote hooks are; `pre-receive`
  - 6 · `update` and `post-receive`
  - 7 · remote hooks only act inside Git; to reach Slack or a dashboard, "That's where Webhooks
    come in."
- Slides 8–12 · **GitHub Webhooks**
  - 8 · section divider
  - 9 · what a webhook is, and three uses (external CI such as Jenkins, deploying, notifications)
  - 10 · "GitHub Webhooks: Example": no Slack webhook is actually set up, so imagine one (meme)
  - 11 · the imagined result: a mock Slack message about a failed build
  - 12 · the point: real-time updates outside GitHub, even "shame" when something breaks (meme)
- Slides 13–31 · **Continuous Integration**
  - 13 · section divider
  - 14–16 · "Motivation": local hooks run linters, formatters and tests (14); they stop once code
    reaches the shared repository (15); CI runs the checks there instead (16)
  - 17 · "Continuous Integration (CI)": CI's benefits in ordinary software; MLOps adds a layer:
    "Non-determinism" (meme)
  - 18 · what non-determinism means: uncertainty in training, data, testing and deployment
  - 19–20 · "How do we address this uncertainty?": four remedies (two per slide)
  - 21 · the CI loop diagram: developers, commits, codebase → build → test, notifications
  - 22 · the definition of CI and its four jobs
  - 23 · CI in ML: merging code, data and models; fast detection matters
  - 24 · "Challenges": integration frequency vs compute cost
  - 25 · "Continuous Integration (CI): Example": from concept to a GitHub Actions pipeline
  - 26 · the course's CI pipeline: Commit → Build Container → Lint and Format → Test → Summary
  - 27 · the same pipeline with each stage explained
  - 28 · "jump into the actual GitHub Actions configuration": tutorial link and QR code
  - 29–31 · "The Local Connundrum" [sic]: why run the checks again remotely? Because
    `--no-verify` skips local hooks
- Slides 32–34 · **Continuous Deployment (Lec21)**
  - 32 · section divider
  - 33 · "Wait… We haven't even learned Deployment Yet!": CD is postponed (meme)
  - 34 · what CD aims to do, in one sentence: "DON'T FORGET" (meme)
- Slide 35 · closing "Thank you" (meme)

## Key ideas

1. **Local hooks are per-machine, so they cannot be a team guarantee.** Last lecture's Git hooks
   are scripts on your own laptop that check code before a commit or a push. Because each
   developer installs and runs them separately, the team gets inconsistent automation. The
   lecture asks how to make the same checks happen for everyone. (Slides 2, 3)
2. **Remote (server-side) hooks enforce rules where code is received.** They run on the server
   that hosts the repository and act as organization-wide enforcers. `pre-receive` runs before
   a push is accepted (standards, tests, linters, notifications). `update` does the same job one
   branch at a time, for branch-specific policies. `post-receive` runs after the code is in, for
   integration tests, notifications or clean-up such as purging large files. (Slides 5, 6)
3. **Webhooks carry repository events to services outside Git.** Hooks enforce rules inside
   Git; a webhook fires on an event such as a push and calls an external service. The examples
   are starting an external CI system (Jenkins), deploying to a production server, and posting
   to Slack or Discord. The lecture's picture is a Slack channel that hears about every push in
   real time, including failures. (Slides 7, 9–12)
4. **Once code is pushed, the local checks are gone, so they must be centralized.** Locally,
   linters, formatters and tests run automatically on every commit. On the shared repository
   nothing runs them, so we need a central, automatic place that does: that is CI. (Slides
   14–16)
5. **CI means running a series of scripts automatically whenever something changes.** Its jobs
   are to integrate changes continuously, test automatically, enforce coding standards and run
   static analysis. In ordinary software it buys faster releases, better code and easier
   coordination. (Slides 17, 22)
6. **The CI loop closes back on the developers.** Developers commit to the codebase; the
   codebase is built and then tested; build and test both send notifications back to the
   developers, who fix and commit again. (Slide 21)
7. **MLOps adds non-determinism.** Uncertainty enters at every stage: how models train and
   behave, data that keeps changing, tests whose results vary, and models that drift after
   deployment. (Slides 17, 18)
8. **Four answers to that uncertainty.** (1) Version code, data and models so results can be
   reproduced (DVC, MLflow, Git-based tracking). (2) Automate retraining and testing so models are
   retrained and validated when data or code changes. (3) Monitor production: model performance,
   input data quality and drift. (4) Roll out with a controlled, safe deployment strategy before
   a full release (deferred to later). (Slides 19, 20)
9. **CI in ML integrates code, data and models.** Each merge into the shared repository triggers
   tests that check nothing broke. Catching a problem in code, data or a model quickly matters,
   because late detection costs time and money. (Slide 23)
10. **CI frequency is a cost trade-off.** Integrating often is good, but training and testing
    models is computationally expensive. How often CI runs, and how it is set up, depends on the
    organization's resources and workflow. (Slide 24)
11. **The course's pipeline has five stages.** A commit triggers it. The container is built
    first (a Docker image, for a consistent environment and to catch build problems early). Then
    Black and Flake8 check format and style. Then unit, integration and system tests run. Finally
    a summary collects the results and reports pass or fail to the developers. It is built with
    GitHub Actions and runs on every push or pull request. (Slides 25–27)
12. **Remote CI repeats the local checks on purpose.** A developer can skip every local
    pre-commit check with `--no-verify`, deliberately or by accident. Anything that slips through
    can only be caught by running the same checks again on the CI server. (Slides 29–31)
13. **CD is the next step, not today's topic.** Continuous deployment automates the release once
    everything has been tested and approved. The lecture only names it and defers the details.
    (Slides 32–34)

## Diagrams

- **Slide 14 · local hooks chain.** A rounded rectangle labelled "Git local hooks" (bottom right)
  holds three boxes in a row joined by block arrows: "Linters" → "Formatters" → "Tests". The
  first two are pale blue; "Tests" is a stronger blue. Below: all of this is local and fires
  automatically on each commit attempt. Purpose: the "before" picture, checks that live on one
  laptop.
- **Slide 16 · the same idea moved to the server.** Same layout and styling as slide 14, but the
  container is now labelled "Shared Repository" and the three boxes read "Build Container" →
  "Check Code" → "Test Summary". Purpose: CI is the slide-14 chain relocated to the shared
  repository, with a build step in front and a report at the end. A re-draw can morph slide 14
  into slide 16 (the frame slides from laptop to server, the labels change).
- **Slide 21 · the CI loop.** Top row: a red dashed rectangle encloses three solid red boxes
  joined by arrows, "Codebase" → "Build" → "Test". Above "Codebase" sit the GitHub (Octocat) and
  GitLab (fox) logos, i.e. where the code lives; above "Test" sits a pair of red-and-green theatre
  masks (the Playwright logo, a testing tool). Bottom left: the word "Developers", with a solid
  arrow labelled "Commits" going up into "Codebase". To its right stands a thick black vertical
  bar labelled "Notifications". Two dashed blue lines run from the bottoms of "Build" and "Test"
  down and left into that bar. Purpose: the feedback loop, code goes up, build and test results
  come back to the people who wrote it.
- **Slide 26 · the course's CI pipeline.** A rounded frame labelled "CI Pipeline" (bottom right)
  holds five rounded boxes in a row joined by light-blue block arrows, each in its own pastel
  colour: "Commit" (grey-teal) → "Build Container" (peach) → "Lint and Format" (pale yellow) →
  "Test" (pink) → "Summary" (lavender). Purpose: the shape of the workflow students will run.
  Note for scene authors: the slide draws a straight line, but the tutorial's `ci.yml` fans out:
  after `build`, the lint job and three test jobs (unit, integration, system) run in parallel,
  and the summary job waits only for the three test jobs, not for lint (see digest §3 C4).
- **Slide 27 · the pipeline, annotated.** The slide-26 row again, with a thin curved arrow from
  each box down to a short caption, captions staggered at different heights:
  - Commit: developers push changes to the repository, which triggers the pipeline.
  - Build Container: builds a Docker image so the environment is consistent and build problems
    show up.
  - Lint and Format: tools such as Black and Flake8 check style and quality.
  - Test: runs automated unit, integration and system tests.
  - Summary: collects the results and reports pass/fail back to the developers.

  Purpose: what each stage is for, one sentence each.
- **Slide 11 · anatomy of a CI notification (mock Slack message).** Not a mechanism diagram,
  but it carries content. A Slack channel ("#build-alerts") shows a message from a GitHub bot:
  a red ✗ "Build failed" for a service on a `cheese-app` repository, by a named developer, with
  the joke "Achievement unlocked: 'Works on my machine'". A card below reads "STATUS: FAILED ·
  GitHub Actions • ci.yml" and lists Commit (a short SHA and a joke message), Triggered by,
  Failed step (`Run python3 -m pre-commit run --all-files`), Tests (128 failing, 0 passing),
  Lint (53 errors, 12 warnings) and Duration (about 2 min). A tip suggests running
  `pre-commit install` locally before pushing. Buttons: View checks, Open PR, Re-run job, Assign
  a senior developer. Underneath, a reply from "Pavlos" jokes that the commit message is a
  firing offence. Purpose: what a webhook delivers (who, which commit, which step failed,
  counts, links back). Slide 10 says it is imagined; it is not output of the tutorial, whose
  `ci.yml` does not run pre-commit.
- **Slides 30 and 31** show the command `git commit --no-verify -m "quick fix"` in a framed box
  (with `--no-verify` in green), not a diagram.
- **Pictures that are jokes, not diagrams:** slide 10 (SpongeBob, "IMAGINATION"), 12 (a
  "SHAME. SHAME. SHAME." scene, the shamer labelled "Webhooks"), 17 (SpongeBob captioned
  "Non-determinism"), 18 and 29 (animated GIFs whose first frame renders as noise or stripes in
  the PDF), 30 (a confused cartoon character with a loading spinner), 33 (a dog beside "Wait… We
  haven't even learned Deployment Yet!"), 34 (Kermit in the rain, "DON'T FORGET"), 35 (Kung Fu
  Panda, "That feeling when you finally understand the topic"). Slide 28 carries a QR code for
  the tutorial link.

## Terms the lecture uses

| Lecture term | Slides | Note on the tutorial README / digest |
|---|---|---|
| "Local Git hooks" / "Git local hooks" | 2, 3, 14 | The README says "Pre-commit hooks" (Part 4) and uses the `pre-commit` framework. In this course they were taught in L9. |
| `pre-commit`, `pre-push` | 2 | Slide 2 says `pre-commit` "Runs before code is accepted on the server"; that wording belongs to `pre-receive`. A `pre-commit` hook runs on your machine before the commit is created (as L9 slide 44 and README Part 4 say). Do not repeat the slip in narration. |
| "Remote hooks" / "Remote Git hooks" | 3, 5–7 | Git's own name is server-side hooks. The README never uses "remote hooks"; its nearest phrase is "Remote CI" (Part 5 heading). Slide 5 lists GitHub Actions and GitLab as examples, but GitHub.com does not let users install custom `pre-receive` hooks (only GitHub Enterprise Server does); on GitHub.com the enforcing role is played by Actions checks plus branch protection (README Part 6). |
| `pre-receive`, `update`, `post-receive` | 5, 6 | Not in the tutorial. |
| "Webhooks" / "GitHub Webhooks" | 7, 9–12 | The tutorial has no GitHub repository webhook. Its Slack step is the reverse direction: a workflow step POSTs to a Slack *incoming* webhook stored as the secret `SLACK_WEBHOOK_URL` (`ci.yml` 194–257). The README never mentions it (digest §2, errata 9). |
| "external CI pipelines (i.e., Jenkins)" | 9 | Not in the tutorial; the tutorial's CI is GitHub Actions itself. |
| "Shared Repository" | 15, 16 | The GitHub repo that Actions runs on. |
| "Continuous Integration (CI)" | 13–31 | Same. The README's Part 5 heading is "GitHub Actions (Remote CI)". |
| "Non-determinism" | 17, 18 | Not in the tutorial; it is an MLOps framing. |
| "drift", "model performance", "input data quality" | 18, 20 | Monitoring vocabulary (L17); not in the tutorial. |
| "Version Everything", "Automate Retraining and Testing", "Monitor in Production", "Use Controlled Deployment" | 19, 20 | Not in the tutorial. "Version Everything" points to DVC (L11) and MLflow. |
| "Codebase", "Build", "Test", "Commits", "Notifications", "Developers" | 21 | The tutorial's "Notifications" are the green/red checks and the optional Slack message. |
| "Static code analysis", "coding standards" | 22 | The tutorial does this with Black and Flake8. |
| "CI Pipeline" | 26, 27 | Matches the workflow's `name: CI Pipeline` and the README's "CI Pipeline (`.github/workflows/ci.yml`)". |
| "Build Container" / "Check Code" | 16, 26, 27 | `ci.yml` job `build`, named "Build Docker Image"; the README says "Build Job". |
| "Lint and Format" | 26, 27 | Job `lint-and-format`, named "Lint and Format Check". In the tutorial Black is blocking and Flake8 is advisory (`continue-on-error`). |
| "Test" (unit, integration and system tests) | 26, 27 | Three separate parallel jobs in `ci.yml`: "Unit Tests", "Integration Tests", "System Tests" (11, 10 and 5 tests). |
| "Summary" / "Test Summary" | 16, 26, 27 | Job `test-summary`, named "Test Summary". It checks the three test jobs only, not lint. |
| "Linters", "Formatters", "Tests" (inside local hooks) | 14 | The tutorial's `.pre-commit-config.yaml` runs generic checks, Black and Flake8, but no tests. |
| "The Local Connundrum" [sic] | 29–31 | Slide title, misspelled on all three slides. |
| `--no-verify` flag | 30, 31 | Not in the README. |
| "remote CI server" | 31 | In the tutorial: a fresh GitHub-hosted `ubuntu-latest` runner per job. |
| "push", "pull request" | 25, 27 | The workflow's triggers: `push` and `pull_request` to `main` or `develop`. |
| "Continuous Deployment" / "CD" | 4, 32–34 | Not built in this tutorial (the repo is CI only). CD arrives in L23 (`cheese-app-v4`, `/deploy-app`). |
| "Continuous Deployment (Lec21)" | 4, 8, 13, 32 | An outline label pointing to this very lecture, which then defers CD. It looks carried over from a "part I" deck. |

## Commands and code on the slides

The slides show no workflow YAML and no Docker or pytest commands; the configuration itself is
only in the tutorial.

- Slides 30, 31: `git commit --no-verify -m "quick fix"`
- Slide 11 (inside the mock Slack message): failed step `Run python3 -m pre-commit run --all-files`
- Slide 11 (same message, the tip): `pre-commit install`
- Slide 11 (same message, the workflow file): `ci.yml`
- Hook names on slides 2, 5 and 6: `pre-commit`, `pre-push`, `pre-receive`, `update`,
  `post-receive`
- Slide 28: the tutorial URL (see Pointers)

## What the lecture stresses

- **Local automation is inconsistent across a team.** It runs only on each developer's system
  (slide 3) and stops working once code is pushed (slide 15). The checks need a central,
  automated home (slides 15, 16).
- **Remote hooks are enforcers for the whole organization** (slide 5), but they stay inside Git.
  Use webhooks to act outside it (slide 7).
- **Real-time feedback, with a social edge.** Webhooks alert people, trigger builds, deploy code
  and can publicly "shame" whoever broke the build (slide 12); the mock message hands out a
  "Works on my machine" achievement (slide 11).
- **Never trust the local checks alone.** `--no-verify` skips every local pre-commit check,
  on purpose or by accident, and only the remote CI run will catch what slips through
  (slides 29–31). The mock message's tip makes the same point from the other side: install
  pre-commit locally before pushing (slide 11).
- **MLOps is harder than ordinary CI because of non-determinism** in models, data, tests and
  deployment (slides 17, 18). The counter-measures: version everything, automate retraining and
  testing, monitor in production, roll out in a controlled way (slides 19, 20).
- **Fast detection is crucial**; delays cost time and money (slide 23).
- **Design trade-off: how often to integrate.** Frequent integration competes with the high
  compute cost of training and testing models; the right setup depends on the organization's
  resources and workflow (slide 24).
- **Build the container first.** It gives every later check the same environment and surfaces
  build problems early (slide 27).
- **Report back to the developers.** The pipeline ends with a summary of pass/fail (slide 27),
  and the CI loop ends with notifications (slide 21).
- **Remember what CD is for** ("DON'T FORGET"): automate the release once everything has been
  tested and approved (slide 34).

## Pointers

- **Slide 28: the tutorial.**
  `https://github.com/dlops-io/cheese-app-ci-cd/blob/main/README.md#part-5-github-actions-remote-cicd`,
  with a QR code. The anchor matches an older README heading ("…Remote CI/CD"). Since commit
  `91eb786` the heading is "Part 5: GitHub Actions (Remote CI)", whose anchor is
  `#part-5-github-actions-remote-ci`, so the slide link now opens at the top of the README. Use
  the current anchor on screen.
- **Slide 2: "the previous lecture" on local Git hooks.** In this course's sequence that is L9
  (cross-reference, not on the slide: the L9 deck's slides 34, 41, 43 and 44, and README
  Part 4, "Automating with Pre-commit Hooks").
- **Slides 10–11: the Slack webhook is imaginary on the slides.** The tutorial's `ci.yml` does
  contain an optional Slack notification, enabled by the repository secret `SLACK_WEBHOOK_URL`
  (digest §2 and Step 15).
- **Slide 19: tools for versioning:** DVC, MLflow, Git-based tracking (DVC is covered in L11).
- **Slide 20: controlled deployment** is announced for later ("we'll look more into this
  later").
- **Slides 33–34: continuous deployment** is announced for later ("we'll get there soon"). In
  this course that is L23 (cross-reference: the L23 deck's slides 11–20 and the `cheese-app-v4`
  workflow triggered by `/deploy-app` in the commit message).
- **Slide 9: Jenkins** is named as an example of an external CI system.
- No readings, homework or milestone notes appear on the slides. (The tutorial digest, §7, ties
  this CI pipeline to Milestone 4.)

## This video and the slides

**Basis.** The video is not scripted yet. This folder holds only [`digest.md`](digest.md) and this
file: there is no `BRIEF.md`, `script.md`, `ASSETS.md` or `assets/terminal/`. So the map below uses
the ten planned chapters in `digest.md` §8, the study guide
(`MLOps_Learning/guides/L21-cicd-github-actions.md`) and every slide: the extracted text and all four
contact sheets. With no captures yet, "the tutorial today" means `dlops-io/cheese-app-ci-cd` at the
digest's pinned commit `b8458ff` (still the head of `main` in a fresh clone on 2026-10-16), plus the
Black and Flake8 output that the digest reproduced on a copy of the code. For this section I
re-checked these at the source, in that clone:
- README.md: Part 4's wording, "before each commit" (`:234`, `:249`, `:253`); the Part 5 heading
  (`:277`); Part 6 (`:369-397`); no mention of `--no-verify`, webhooks or Slack anywhere;
- the anchor history: the "Remote CI/CD" heading was added in `d03607d` and renamed in `91eb786`;
- `ci.yml`: triggers (`:7-11`), job names, `needs` and `if:` lines (`:16`, `:42-44`, `:71-73`,
  `:106-108`, `:129-131`, `:173-176`, `:194-204`) and the Slack payload (`:207-257`);
- `.pre-commit-config.yaml`: seven hygiene hooks (`:12-25`), Black `24.1.1` (`:30-34`) and Flake8
  `7.0.0` (`:39-43`), with the same flags as CI; `pyproject.toml:8` (`black>=24.1.1`).

When `assets/terminal/` and `ASSETS.md` exist, re-check Conflicts 2 and 4–8 against them. If they
disagree, the captures win.

### 1. Map: planned chapters ↔ slides

| # | Planned chapter (`digest.md` §8) | Slides on the same ground | Relation |
|---|---|---|---|
| 1 | One push, six machines (2 min) | 14–16 (the local hook chain, then the same idea on the shared repository); 22 (CI defined); 25 (GitHub Actions on push or pull request); 26 (the five-stage pipeline); 21 (the CI loop); 2–3 (the recap: local hooks run only on one machine) | Same concept; the tutorial applies it. The plan opens on the demo bug and never makes the lecture's move from laptop to shared repository (gap 1). Six VMs per run is tutorial-only. |
| 2 | When does the robot wake up? (2 min) | 25 (every push or pull request); 27 (Commit: a push triggers the pipeline); 23 (each merge triggers the tests); 24 (frequency vs compute cost) | The tutorial applies it, with a branch filter the slides don't mention (Conflict 4). The merge commit on PR runs is slide 23 made literal. Slide 24 is not used yet (gap 5). |
| 3 | Machines with amnesia (2 min) | 31 (one "remote CI server"); 27 (Build Container for "environment consistency") | Tutorial-only. The lecture draws one server; the tutorial's fresh VM per job is what makes the image artifact necessary. |
| 4 | Build once, ship a suitcase (3 min) | 16, 26–27 (Build Container comes first: one environment for every check, build problems surface early) | Same concept. `docker save`, the artifact, the SHA tag and the entrypoint's `exec "$@"` are tutorial-only. |
| 5 | The dependency graph (2.5 min) | 26–27 (five boxes in one straight line) | The tutorial applies it in a different shape: a fan-out/fan-in graph (Conflict 5). |
| 6 | Gates speak in exit codes (3 min) | 14 (linters and formatters in the local chain); 22 (coding standards, static code analysis); 27 (Lint and Format: Black and Flake8); 29–31 (`--no-verify`) | Same concept; the tutorial applies it. Exit codes, blocking vs advisory steps and the skipped Flake8 are tutorial-only. The plan does not use 29–31 (gap 1, Conflict 8). |
| 7 | Three altitudes of tests (3 min) | 27 (unit, integration and system tests); 14 (Tests inside the local chain) | The tutorial applies it. In-process vs HTTP, `--network host`, `skipif` and the `curl -f` gate are tutorial-only. This repo's local hooks run no tests (Conflict 3). |
| 8 | Collecting the verdict (2.5 min) | 16 (Test Summary); 26–27 (Summary reports pass/fail to the developers); 21 (Notifications) | Same concept, narrower in the tutorial: the summary reads the three test jobs, not lint (Conflict 5). `needs.<job>.result`, `$GITHUB_OUTPUT` and job summaries are tutorial-only. |
| 9 | Secrets and the Slack bell (2.5 min) | 7, 9–12 (webhooks; the imagined Slack message on 11; the "shame" on 12) | Same goal, different mechanism (Conflicts 6–7). Secrets, masking and the `if:` workaround are tutorial-only. |
| 10 | Do it yourself: red → green → protected (3 min) | 21 (the loop: fix and commit again); 5–6 (`pre-receive`, `update`: rules enforced on the server); 28 (the tutorial link); 33–34 (CD comes next) | The tutorial applies it. Branch protection is GitHub.com's form of the lecture's server-side enforcement (gap 2, Conflict 2). The plan does not use 33–34 (gap 7). |
| — | not in the plan | 1, 4, 8, 13, 32, 35 (title, outline, dividers, close); 17–20 (non-determinism in ML and four remedies); the ML half of 23 (merging data and models) | Lecture-only. 17–20 and 23 are gap 6. |

### 2. Already in common

| # | Concept | Chapter ↔ slides | Does the video's framing agree with the lecture's? |
|---|---|---|---|
| 1 | Local hooks stop at the push, so the same kind of checks must run centrally, on the shared repository | ch1, and `digest.md` §7 ("What L21 adds") ↔ 3, 14–16 | Yes. Digest §7 says it in the lecture's terms: the same checks, run remotely and automatically. The plan's ch1 leaves it implicit and starts at the push (gap 1). |
| 2 | CI runs a series of scripts automatically whenever the code changes: integrate, test, enforce standards, analyse the code | ch1 (C1, workflow anatomy) ↔ 22, 25 | Yes. The plan's "a robot that reacts to repo events by running a YAML recipe" is the mechanism under slide 22's definition; `ci.yml` is the series of scripts. |
| 3 | A push or a pull request starts the pipeline | ch2 ↔ 25, 27 (the Commit box) | Yes, with one qualifier: only pushes to `main`/`develop` and PRs into them (Conflict 4). |
| 4 | Each merge is tested before it lands | ch2 ↔ 23 | Yes. The tutorial makes slide 23 literal: on a `pull_request` run, `github.sha` is a temporary merge of the PR into its base, and that merge is what gets built and tested. |
| 5 | Build the container first, so every check runs in the same environment and build problems show up early | ch4 ↔ 16, 26–27 | Yes. The plan adds why it is built only *once*: jobs share nothing, so the image travels as an artifact under one SHA tag. |
| 6 | Black and Flake8 check format and style | ch6 ↔ 22, 27 | Yes. Slide 22's "coding standards" is Black; "static code analysis" is Flake8. The plan adds what the slide's single box hides: Black is blocking, Flake8 advisory, and Flake8 is skipped when Black fails. |
| 7 | Unit, integration and system tests run automatically | ch7 ↔ 27 | Yes. The slide's one Test box is three parallel jobs in the tutorial (11, 10 and 5 tests). |
| 8 | A summary collects the results and reports pass or fail | ch8 ↔ 16, 26–27 | Partly. `test-summary` reads the three test jobs only, not lint, and reports in its job log (Conflict 5). |
| 9 | Results go back to the people who pushed, in real time, Slack included | ch9, ch10 ↔ 11–12, 21 | Partly. The green and red checks on commits and PRs are slide 21's notifications. The Slack message exists, but it is sent another way (Conflict 6) and says less (Conflict 7). |
| 10 | The developer fixes the problem and pushes again until the run is green | ch10 (red → green) ↔ 21 | Yes. Ch10's red first run, the Black fix and the second push are one turn of slide 21's loop. |
| 11 | Local hooks can be skipped, so the remote run is the safety net | guide §8 E8 ("local hooks and remote CI are different safety nets") ↔ 29–31 | Yes in principle. The tutorial shows the net has holes (Conflict 8). None of the plan's chapters uses it (gap 1). |

### 3. Gaps (ranked by value to a student doing the tutorial)

1. **Why run the checks twice: local hooks don't travel, and `--no-verify` skips them (slides 2–3,
   14–16, 29–31).** The student installed this repo's pre-commit hooks in L9 (Part 4), so the first
   question is "why again?" The lecture answers it with one command, `git commit --no-verify`, and
   with the plain fact that hooks run only where someone ran `pre-commit install`. It also tells
   the student, without blame, how a repo that has hooks can still contain the messy `utils.py` that
   makes their first run red. The twist that makes it worth the time: this CI re-runs only two of the
   local checks (Conflict 8), so a key file committed with `--no-verify` still goes through (guide
   §8 E8). **Carry it in** ch1 (first 45 s: slide 14's chain inside a laptop frame slides into slide
   16's "Shared Repository" frame) and ch6 (a new pause-and-ponder; see the proposals).
2. **Enforcement on the server, and where GitHub.com puts it (slides 5–7).** `pre-receive` can
   refuse a push; `post-receive` runs after the code is in. A push-triggered Actions run is the
   second kind: when it turns red, the commit is already on `main`. GitHub.com does not run your own
   `pre-receive` scripts (GitHub Enterprise Server does); the gate that refuses is branch protection,
   with a required pull request and required status checks (README Part 6). Students often believe a
   red run blocked their push. **Carry it in** ch10 (40 s, at the protect step) and one sentence in
   ch2 ("the robot wakes up after the push is accepted").
3. **Webhooks: who calls whom (slides 7, 9–12).** A GitHub webhook is GitHub calling an outside URL
   when an event happens. The tutorial's `SLACK_WEBHOOK_URL` works the other way round: Slack gives
   you a URL (an *incoming webhook*), and the last step of your workflow calls it. A student who goes
   to the repo's Settings → Webhooks to "add the Slack webhook" is in the wrong place; the URL goes
   under Settings → Secrets and variables → Actions. **Carry it in** ch9 (30 s, before the vault).
4. **The CI loop (slide 21).** Commit → build → test → notifications → fix → commit. It is the shape
   of ch10 and a clean frame for the end card, but the plan never draws it. **Carry it in** ch1 (last
   15 s, as the promise) and close it in ch10.
5. **How often, at what cost (slides 23–24).** The lecture treats frequency against compute cost as
   a design choice. This workflow's answers are concrete: the branch filter (a feature-branch push
   runs nothing), parallel jobs (about 2 minutes of wall-clock time), every job billed separately and
   rounded up (about 6 billed minutes per run on a private repo) and a 1-day artifact (`digest.md`
   §2). **Carry it in** ch2 (the branch filter as a cost decision) or ch5 (a second ruler under the
   Gantt chart: wall-clock vs billed minutes).
6. **What changes when the code trains a model (slides 17–20, 23).** Non-determinism in training,
   data, tests and deployment, and four remedies: version everything, automate retraining and
   testing, monitor in production, roll out in a controlled way. You don't need it to finish the
   tutorial (the app is a deterministic toy), but it is what Milestones 4–5 ask the student to put
   under CI, and it links back to L11 (DVC) and L13/L15 (pipelines). **Carry it in** ch10's outro
   (20–30 s) or the recap card.
7. **CD comes next (slides 33–34).** One line: CD automates the release once everything is tested
   and approved. In this course that is L23 (`cheese-app-v4`, a workflow started by `/deploy-app` in
   the commit message), using the same secrets mechanism as ch9. The repo is named "ci-cd" but holds
   CI only. **Carry it in** ch10, last 15 s.

### 4. Conflicts

| # | Slides say | Tutorial today (the repo at `b8458ff`) | Current | How the video should put it |
|---|---|---|---|---|
| 1 | **`pre-commit`** (slide 2) is described as running before code is accepted on the server. | The hooks run on your machine before each commit is created; `pre-commit install` puts them in your local clone (README.md:234, `:249`, `:253`). "Before the server accepts the code" is `pre-receive`, as slide 5 itself defines it. | The repo, and slide 5's own definition | Say it correctly and don't point at the slip: "pre-commit runs on your laptop, before the commit even exists." |
| 2 | **GitHub Actions as a remote hook** (slide 5): remote hooks run on the server, for example in GitHub Actions or GitLab, and enforce rules across the organization. | Actions is not a Git hook. A `push` run starts after the push has been accepted and cannot refuse it (`ci.yml:7-9`). GitHub.com does not run custom `pre-receive` scripts. The refusing gate is branch protection (README.md:369-397): it blocks the merge of a PR whose required checks fail, and direct pushes to `main`. A repo owner can bypass a classic rule unless "Do not allow bypassing the above settings" is ticked (GitHub's behaviour, not captured yet). | GitHub.com as documented; capture it in ch10 | Ch10: "In the lecture's terms, a push-triggered run is a post-receive check: it reports, it doesn't refuse. Branch protection is what turns it into a gate." |
| 3 | **The local chain** (slide 14): Linters → Formatters → Tests, run on every commit. | `.pre-commit-config.yaml` runs seven hygiene hooks, then Black (a formatter), then Flake8 (a linter), and no tests; README.md:14 calls them local checks for "linting/formatting". CI also runs Black before Flake8 (`ci.yml:59-67`), and the order matters: Flake8 is skipped when Black fails. | The repo | Ch1 re-draws slide 14 with this repo's boxes: "The lecture's chain is the general idea. This repo's hooks format first, then lint, and leave the tests to CI." |
| 4 | **When it runs** (slide 25): on every push and every pull request. | Only on pushes to `main` or `develop` and on PRs whose base is one of them (`ci.yml:7-11`). README Part 6's own flow pushes `feature/test-protection`, which starts nothing until the PR is opened. | The repo | Ch2's three lanes show it. One bridge sentence: "Every push to main or develop. On any other branch, the robot waits for your pull request." |
| 5 | **The pipeline's shape** (slides 26–27, also 16): one straight line, Commit → Build Container → Lint and Format → Test → Summary, with the Summary reporting pass/fail. | Six jobs; "Commit" is the event, not a job. After `build`, four jobs run in parallel: lint and three test jobs (`ci.yml:44`, `:73`, `:108`, `:131`). `test-summary` needs only the three test jobs (`:175`), so when Black fails the run is red while the summary prints "✅ All tests passed!". Flake8 is advisory (`:67`). | The repo | Ch5's best moment: start from the lecture's row, then pull it apart into the graph. "The lecture lists the stages in order. On GitHub the four checks run side by side, and the summary listens only to the tests." Ch8 draws the missing arrow from lint as a dashed line. |
| 6 | **The webhook** (slides 9–12): GitHub messages the team's Slack channel whenever someone pushes. | No repository webhook is configured. The message comes from the last steps of `test-summary` (`ci.yml:194-257`): the workflow calls a Slack incoming-webhook URL stored as the secret `SLACK_WEBHOOK_URL`. It runs only on the filtered pushes and PRs, after the three test jobs, and only if the secret exists. Because `slack-check` has no `if: always()`, it never runs when tests fail (guide §6 G8). The README never mentions it. | The repo | Ch9: "The lecture imagines a webhook that shames whoever broke the build. The repo has the bell, but GitHub doesn't ring it: your workflow calls Slack, through the URL you stored as a secret. And as written, it only rings for good news." Then pause-and-ponder #3. |
| 7 | **The message** (slide 11, labelled imaginary on slide 10): a failed run, the failed step `Run python3 -m pre-commit run --all-files`, failing and passing test counts, lint errors and warnings, the duration, and action buttons. | The real payload (`ci.yml:207-254`): a ✅ or ❌ header, repository, branch, commit, author, ✅ or ❌ for each of the three test jobs, and two links. No failed step, counts, lint or duration. This CI never runs pre-commit, and the ❌ version cannot be sent (Conflict 6). | The repo | Ch9: re-draw slide 11's card as the lecture's wish list beside the real message. "This is what the lecture wishes for; this is what this workflow sends today." Keep the joke friendly. Slide 11's failed step is the fix for Conflict 8. |
| 8 | **The safety net** (slides 29–31): what `--no-verify` let through is caught by running the checks again on the remote CI server. | CI re-runs two of the local checks, Black and Flake8, only on `api/` (`ci.yml:61`, `:66`), with the same flags as the hooks (`.pre-commit-config.yaml:34`, `:43`). The seven hygiene hooks (trailing whitespace, end of file, YAML, large files, JSON, merge-conflict markers, private keys; `:12-25`) never run in CI. Pre-commit pins Black `24.1.1`, while the image installs the newest `black>=24.1.1` (`pyproject.toml:8`). A private key committed with `--no-verify` passes CI (guide §8 E8 (b)). | The repo | Ch6 pause-and-ponder: "A teammate commits a key file with --no-verify. Does this pipeline catch it?" No. "The lecture's principle holds; this pipeline just doesn't re-run every check yet." The fix is one step, `pre-commit run --all-files`, the step slide 11 shows. |
| 9 | **The tutorial link** (slide 28): `README.md#part-5-github-actions-remote-cicd`. | The heading is "Part 5: GitHub Actions (Remote CI)" (README.md:277), so the anchor is `#part-5-github-actions-remote-ci`. The "Remote CI/CD" heading was added in `d03607d` and renamed in `91eb786`, so the slide's link opens at the top of the README. | The README heading | No narration. On screen, the README tracker shows "Part 5: GitHub Actions (Remote CI)"; the guide's Links use the current anchor. |

Not counted as conflicts:
- The page numbers printed in the footers run ahead of the PDF pages from slide 16 on. The outline's
  label "Continuous Deployment (Lec21)" sits in a deck that then defers CD. Both are inside the deck.
- Slide 21 draws notifications coming from both Build and Test. GitHub reports every job, the build
  included, as its own check on the commit, so the two agree.
- Slide 21's GitLab and Playwright logos and slide 9's Jenkins are examples of other tools, not
  claims about the tutorial.
- Slides 17–20 and 23 talk about data and models; this repo has neither. That is an omission
  (gap 6), not a contradiction.
- The repo is named `cheese-app-ci-cd` but holds CI only. The slides also postpone CD (33–34), so
  they agree.

### 5. Proposals for the BRIEF and script authors

**General**
- Tag each chapter that stands on lecture ground with one GREY `lecture_ref`. L21 has one deck, so
  plain ranges are enough: `lecture_ref(21, "14–16")` reads "Lecture 21 · slides 14–16". Use the
  PDF page numbers listed here, never the footers. Re-draw every lecture diagram in the series
  style; never show slide images or the memes. The lecture's "shame" can become a friendly red
  bell.
- **Make the lecture's pipeline row the video's progress strip.** Re-draw slide 26's five boxes
  (Commit → Build Container → Lint and Format → Test → Summary) as a thin strip under the
  chapter titles. Ch2 lights Commit, ch4 Build Container, ch6 Lint and Format, ch7 Test, ch8
  Summary. In ch5, unfold the strip into the real graph (Conflict 5): four boxes slide into
  parallel lanes, Test splits into three, and the arrow from lint to Summary fades to a dashed gap.
  Colours: the GitHub runners BLUE, the image and containers TEAL, failures RED, the strip's current
  box YELLOW.
- **Second frame: slides 14 → 16 → 21.** Open ch1 on slide 14's chain inside a GREY laptop frame,
  slide it into slide 16's "Shared Repository" frame (BLUE), and close slide 21's loop in ch10.
- **Hook.** Keep the plan's hook: the demo commit `c3b227f` with `math.sqrt(2 * z)`, six machines,
  one already red for another reason. Answer the "why a second set of checks?" question in ch1 with
  slide 29's question and slide 30's command. Don't claim the instructor used `--no-verify`; the git
  history doesn't show how the messy `utils.py` got in.
- **One new pause-and-ponder (ch6), from slides 29–31 and Conflict 8.** "A teammate commits a
  private key with `git commit --no-verify` and pushes to `main`. Which job catches it?" *Answer:*
  none. CI runs only Black and Flake8 on `api/`; `detect-private-key` lives only in the local hooks.
  The fix is to add `pre-commit run --all-files` as a CI step.
- **Time.** The plan is about 24–25.5 minutes. Gaps 1–7 add about 3–3.5 minutes, which brings the
  video to about 28 minutes, inside the 25–35 range, so nothing needs to be cut.
- **Captures.** When they are made, record:
  - with the hooks installed, a `git commit` stopped by Black, then the same commit with
    `--no-verify` going through;
  - the first red run: Black's `would reformat …/api/utils.py`, Flake8 skipped, and "✅ All tests
    passed!" in the same run's summary log;
  - the passing Slack message, then a failing run that sends nothing;
  - with `main` protected and bypassing disallowed, a direct `git push` to `main` refused by the
    server (GitHub reports the rule as a declined hook);
  - the README tracker on "Part 5: GitHub Actions (Remote CI)".

  Then re-check Conflicts 2 and 4–8 against them.

**Per chapter**
- **Ch1 · `lecture_ref(21, "14–16, 21–22")`.**
  - First 45 s (gap 1): slide 14's chain with this repo's boxes (hygiene checks → Black → Flake8,
    Conflict 3), a push arrow, then the frame slides to the shared repository and the boxes become
    slide 16's (Build Container → Check Code → Test Summary). Narrate slide 3's point: the hooks run
    only where someone installed them.
  - Then the plan's unfolding `ci.yml` tree; slide 22's definition as a single caption.
  - Last 15 s: slide 21's loop, drawn open (gap 4).
- **Ch2 · `lecture_ref(21, "23–25")`.**
  - State slide 25's promise, then let the three lanes qualify it (Conflict 4).
  - Slide 23's "each merge is tested" lands on the ghost merge commit.
  - One sentence each: the branch filter is a cost decision (gap 5, slide 24); the robot wakes up
    after the push is accepted (gap 2).
- **Ch3 · no `lecture_ref`** (tutorial-only). Bridge once: "The lecture draws one CI server. GitHub
  gives you a new one for every job."
- **Ch4 · `lecture_ref(21, "26–27")`.** Light Build Container on the strip; slide 27's purpose
  (one environment, build problems caught early) becomes the subtitle of the image cube.
- **Ch5 · `lecture_ref(21, "26")`.** The unfold (Conflict 5). Optionally add a GOLD ruler under the
  Gantt chart: about 2 minutes of wall-clock time, about 6 billed minutes (gap 5).
- **Ch6 · `lecture_ref(21, "27, 29–31")`.** Light Lint and Format. The gates show Black before
  Flake8 (Conflict 3). End with the new `--no-verify` pause-and-ponder (Conflict 8).
- **Ch7 · `lecture_ref(21, "27")`.** The strip's Test box splits into three jobs before the
  pyramid appears.
- **Ch8 · `lecture_ref(21, "16, 27")`.** Light Summary; the dashed lint arrow (Conflict 5).
- **Ch9 · `lecture_ref(21, "9–12")`.**
  - Open with two arrows (gap 3): GitHub → an outside URL (the lecture's webhook), then
    workflow → Slack's incoming webhook (the tutorial's step). Only the second exists here
    (Conflict 6).
  - Put a re-drawn slide 11 card, captioned as the lecture's wish list, beside the real message
    (Conflict 7). Then the vault and the bug, as planned.
- **Ch10 · `lecture_ref(21, "5–6, 21")`.**
  - Red → green as one turn of slide 21's loop; the loop closes.
  - Protect `main` (gap 2, Conflict 2): "This is the lecture's `pre-receive` idea, the way
    GitHub.com offers it." Show the refused direct push if it was captured.
  - Outro: 20–30 s on slides 17–20 (gap 6), then 10 s on slide 34 and L23 (gap 7).
- **Recap card.** Keep the plan's six questions, and add two:
  - "Name two ways code reaches the shared repository without passing your local hooks."
    (`--no-verify`; a clone where nobody ran `pre-commit install`.)
  - "In the lecture's terms, is a push-triggered Actions run a pre-receive or a post-receive check,
    and what turns it into a gate?" (Post-receive; branch protection with required checks.)

**Terms**
- Use the lecture's words: *local Git hooks*, *remote* (server-side) *hooks*, `pre-receive`,
  `post-receive`, *webhook*, *shared repository*, *CI pipeline*, *Build Container*, *Lint and
  Format*, *Summary*, *notifications*, *coding standards*, *static code analysis*, `--no-verify`,
  *non-determinism*, *drift*, *continuous deployment*.
- Add the tutorial's words where the lecture stops: *workflow*, *event*, *job*, *step*, *runner*,
  *artifact*, `needs`, `if: always()`, *exit code*, *blocking* and *advisory* (`continue-on-error`),
  *status check*, *branch protection*, *repository secret*, *incoming webhook*.
- Bridge each pair once:
  - the lecture's Build Container is the `build` job ("Build Docker Image");
  - the lecture's Summary is `test-summary` ("Test Summary"), which reads the tests only;
  - the lecture's remote hook is, on GitHub.com, branch protection with required status checks;
  - the lecture's webhook calls out of GitHub; the tutorial's Slack step calls in to Slack.
- Avoid "remote hooks such as GitHub Actions" (Conflict 2) and "pre-commit runs on the server"
  (Conflict 1).
