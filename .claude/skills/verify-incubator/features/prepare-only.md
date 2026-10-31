# Prepare speech only

Before rendering frames, a user can synthesize the narration and save the timing plan, to check
that the script fits its duration and that every line speaks, without spending minutes on Manim.

## Sub-features

- `prepare-speech` writes one Kokoro clip per narration line into the output's `.tts-cache`.
- `prepare-plan` writes `plan-<scene>.json` (or `plan.json` for the whole episode) with the
  resolved settings, script sha256, voice, speed and each scene's minimum duration.
- `prepare-budget` refuses a full episode whose narration exceeds `duration_seconds`.

## How to get to it (user POV)

- Run `python3 skill-library/conny-explainer-video/scripts/render.py videos/<slug> --prepare-only` (whole episode).
- Add `--sample sNN` for one scene.

## Driving it with control.py

Preconditions:

- Baseline preconditions in `README.md` hold.
- This `$RUN` has not rendered or prepared this episode yet. Otherwise the speech comes from
  `outputs/<copy>/.tts-cache` and synthesis is not exercised (`render exit code 0  0s` in the summary).

- **Prepare one scene.** Run `$C render-sample --run $RUN videos/skills-ecosystem s01 --prepare-only`. Exit code `0`.
  The summary prints `PASS render exit code 0`, `PASS plan written` and `PASS one speech clip per narration line`.
  No `.mp4` appears in `evidence/`.
- **Read the plan.** Open `evidence/s01-prepare.plan.json`. `narration_key` is `en`, `voice` is `af_heart`, `speed` is
  `0.95`, `sample` is `s01`, and `scenes[0].audio` lists two clip paths that exist.
- **Whole episode.** After the step above has created the copy, run
  `$C cli --run $RUN --name prepare-all -- python3 skill-library/conny-explainer-video/scripts/render.py outputs/verify/$RUN/work/skills-ecosystem-vfy$RUN --prepare-only`.
  Exit code `0`. Stdout shows one `Speech sNN:` line per scene and ends with the path of `plan.json`.

## Gotchas

- "Prepare only" still loads the Kokoro model and synthesizes speech. Only frames, captions and the
  mix are skipped. Its evidence is the plan and the clips, never a video.
- The whole-episode budget check (`Narration needs …s; target is …s`) runs only without `--sample`.
- Clips are cached by text in `outputs/<copy>/.tts-cache`, so a second prepare in the same run is
  instant and proves nothing new about synthesis.
