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
