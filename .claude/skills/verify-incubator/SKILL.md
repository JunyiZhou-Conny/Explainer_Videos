---
name: verify-incubator
description: Prove a change to the video incubator works by driving it the way its users do — render a narrated sample scene through skill-library/conny-explainer-video/scripts/render.py and inspect the real MP4 (frames, captions, loudness, validation sidecar), scaffold an episode, and drive the Studio site (progress board, library, new-episode composer) in a headless browser. Use after changing explainer/, tools/render_episode.py, the skill's scripts or presets, tools/studio_status.py or site/, or whenever you need evidence that rendering or the Studio still works.
---

# Verify the incubator

The incubator has two surfaces a user touches:

- **The renderer** (primary): `python3 skill-library/conny-explainer-video/scripts/render.py <episode> --sample sNN`
  turns `script.json` + `scenes.py` into a narrated, scored, caption-burned MP4 plus a
  `.validation.json` sidecar. Agents and CI run exactly this command.
- **The Studio site** (`site/`, data from `tools/studio_status.py`): the progress board
  Conny follows, the video library, and the new-episode composer.

Not covered here: the legacy `video.yaml` route (`python -m explainer.build`, needs LaTeX
from `setup/install.sh`), `tools/release_episode.py` and `tools/publish_worker.py`. The last
two act on GitHub releases and Bilibili, so never drive them for verification. The publish
worker has its own exhaustive check in the `verify-publish-worker` skill.

Everything runs from the repository root through one helper,
`.claude/skills/verify-incubator/scripts/control.py`. The helper uses plain `python3` and
calls the repo's `.venv` itself. Pick a fresh run id (lowercase letters and digits, e.g.
`RUN=r$(date +%H%M%S)`) for every proof. The id names everything the run creates.

## Launch

Once per machine or container (about 5 minutes the first time: it downloads ~370 MB of
speech model and fonts, verified against `assets/manifest.json`):

```bash
# Linux (Ubuntu 24.04; CI uses the same line). macOS: brew install python@3.12 ffmpeg cairo pango pkg-config
sudo apt-get install -y python3.12-venv libpango1.0-dev libcairo2-dev pkg-config ffmpeg
python3.12 tools/setup-runtime --dev
```

The renderer has no server. Each drive is one process that exits. **Ready** means
`control.py doctor` prints only `OK` lines. Setup is idempotent: rerun it when doctor
reports missing assets or imports.

The Studio site is a static page over JSON. Start a run-owned copy of it:

```bash
python3 .claude/skills/verify-incubator/scripts/control.py studio-up --run $RUN            # live GitHub data
python3 .claude/skills/verify-incubator/scripts/control.py studio-up --run $RUN --snapshot S # saved API payloads
python3 .claude/skills/verify-incubator/scripts/control.py studio-up --run $RUN --offline    # catalog only, empty board
```

It copies `site/` to `outputs/verify/$RUN/work/site/`, builds `data/` with
`tools/studio_status.py` (the same command `.github/workflows/pages.yml` runs), and serves it on a
free 127.0.0.1 port. It is ready when it prints
`READY http://127.0.0.1:<port>/ (pid …, N episodes on the board)`. That line appears only after
the server returns this run's marker file and a parseable `data/status.json`. Live mode saves the
raw API payloads to `evidence/studio-snapshot.json`, so you can rebuild the same board later
with `--snapshot`. Stop it with `studio-down --run $RUN` (cleanup also stops it).

## Doctor

```bash
python3 .claude/skills/verify-incubator/scripts/control.py doctor --run $RUN
```

This is read-only. It checks the checkout and commit, that `.venv/bin/python` imports manim,
kokoro_onnx and soundfile, that every `assets/manifest.json` file is present at its recorded
size, that ffmpeg has libass and loudnorm, and that ffprobe exists. When this run has a Studio
server, doctor also checks that its port answers with this run's marker, so you never drive
someone else's server. Finally it lists leftover `outputs/*-vfy*` and `videos/verify-*` folders
from earlier runs. For a full sha256 check of the assets, run
`python3 tools/setup-runtime --verify-only` (~3 s). Run doctor first, and again whenever anything
looks off.

## Drive

Start from the feature map: `features/README.md` indexes the user-facing features, and each
feature file is the recipe. The drivers are:

- `control.py render-sample --run $RUN <episode-dir> <scene> [--prepare-only]`: copies the
  episode to `outputs/verify/$RUN/work/<slug>-vfy$RUN/` and runs the real `render.py`
  command on the copy. The renderer then writes to its own `outputs/<slug>-vfy$RUN/`, so a
  user's `outputs/<slug>/` is never touched. Afterwards it asserts on the output and extracts a
  frame at every caption cue.
- `control.py cli --run $RUN --name <label> -- <command…>`: runs any user command from
  the repo root and records its command line, stdout, stderr and exit code.
- `control.py browse --run $RUN --name <label> <steps.json>`: drives the served Studio with
  Playwright (`scripts/browser.cjs`, which documents the step vocabulary). Selectors are ARIA
  roles and names, element ids, or the `aria-label`s the pages render. Ready-made step files
  live in `features/steps/`. github.com is stubbed inside the browser, so no issue is ever
  created.

Two runs with different ids can run side by side: the copies, output folders and ports are
all separate. They do share CPU, and each sample render takes 1–2 minutes on 4 cores.

## Evidence

Every proof lands in `outputs/verify/$RUN/evidence/`. `outputs/` is ignored by Git, and
cleanup never deletes this folder. What a run leaves there:

- `<label>.cmd/.stdout/.stderr/.exit` for every command driven.
- Renders: `<scene>.mp4`, `.validation.json`, `.ffprobe.json`, `.zh-en.ass/.srt`,
  `.plan.json`, `<scene>.frames/cueNN-<t>s.png` (each paired with the cue text it should show),
  and `<scene>.summary.json` with each check, its result and the commit.
- Browser: `<label>-<shot>.png` (full page), `<label>-<name>.aria.txt` (ARIA snapshot),
  `<label>.steps.json` (every step, its result and any console errors), `<label>-failure.png`
  when a step fails.

Proof standards:

- Exercise the user path: `render.py`, `new_episode.py` and the served pages. Do not call
  `explainer.episode` internals or build fake sidecars.
- Capture the action and the resulting state. For a render that is the frames *and* the
  sidecar *and* the summary. A `READY` line alone proves nothing.
- Check side effects next to what is visible. A scaffold writes three files and a style
  snapshot whose sha256 must match `episode.json`. A render writes the plan, the speech clips
  and the sidecar.
- Look at the frames. Open at least two `cueNN` PNGs and confirm that the burned Chinese-above-English
  caption matches the paired `.txt` and that the diagram is visible. The numeric checks cannot
  see pronunciation, layout collisions or teaching quality. Say so, and leave the listening
  review to the episode's `REVIEW.md` as AGENTS.md requires.
- `--prepare-only` really skips frames, not speech: it runs Kokoro and writes the clips and the
  plan. Its evidence is the plan plus the clips, not a video.

## Cleanup

```bash
python3 .claude/skills/verify-incubator/scripts/control.py cleanup --run $RUN
```

Cleanup stops this run's Studio server by the pid it recorded (the server runs in its own
session, so the whole group goes). It never kills by process name. It then removes
`outputs/verify/$RUN/work/`, `outputs/*-vfy$RUN/` and `videos/verify-$RUN*/`, and prints how
many evidence files remain. Run it after every attempt, failed ones included. Before you
commit anything, `git status` must show no `videos/verify-*`.

## Helpers

- `scripts/control.py`: the driver above (`doctor`, `render-sample`, `cli`, `studio-up`,
  `studio-down`, `browse`, `cleanup`). Run `--help` on any subcommand.
- `scripts/browser.cjs`: Playwright step runner, `node browser.cjs <steps.json> <dir> <name>
  [base-url]`. Normally reached through `control.py browse`. It needs `require('playwright')`.
  The cloud container has it. On a Mac, run `npm i -g playwright && npx playwright install chromium` once.
- `features/steps/*.json`: the browser journeys the feature files reference.

Keep the map honest with `/pstack:maintain-verification-skill` when features change.
