# Render a narrated sample

A user (an agent producing an episode, or CI on every PR) renders one scene of an
`episode.json`-route episode and gets a 1920×1080, 30 fps MP4 with Kokoro narration, a composed
score ducked under it, burned Chinese-above-English captions, a style check on sampled frames
and a `.validation.json` sidecar recording what was measured.

## Sub-features

- `sample-speech` synthesizes one clip per narration line and sizes the sample to the speech.
- `sample-frames` renders the Manim scene at the episode's resolution and frame rate.
- `sample-captions` burns one bilingual cue per spoken sentence, Chinese above English.
- `sample-score` mixes the composed score under the narration and reports its loudness.
- `sample-style` checks the preset's tokens on sampled frames (presets that ship tokens, e.g. swiss).
- `sample-sidecar` writes `.validation.json` and refuses output whose script changed mid-render.

## How to get to it (user POV)

- Run `python3 skill-library/conny-explainer-video/scripts/render.py videos/<slug> --sample s01`.
- Run `.venv/bin/python tools/render_episode.py videos/<slug> --sample s01` (the direct runner).
- Open a PR: `.github/workflows/episode-check.yml` renders the first scene of the PR's episode,
  or of `videos/skills-ecosystem` for toolkit PRs.

## Driving it with control.py

Preconditions:

- Baseline preconditions in `README.md` hold, and doctor is all `OK`.
- The episode has `script.json` and `scenes.py`. `videos/skills-ecosystem` is the reference.

- **Render.** Render the reference sample. Run
  `$C render-sample --run $RUN videos/skills-ecosystem s01`. Stdout ends with `READY …sample-s01.mp4 — 22.200s, narrated, scored, 5 bilingual cues`,
  then one `PASS` line per check and `PASS: outputs/verify/$RUN/evidence/s01.summary.json`. The exit code is `0`.
- **Speech.** Confirm the clips. In `evidence/s01.summary.json`, `one speech clip per narration line` is `ok`
  (2 clips for 2 lines in `skills-ecosystem` s01). `render-s01.stdout` shows `Speech s01: …s minimum`.
- **Format.** Confirm the container. `1920x1080 @ 30 fps`, `has an audio stream` and `duration matches the plan`
  (within 0.1 s of `target_duration_seconds` in `s01.plan.json`) are `ok`.
- **Captions.** Look at the burned captions. Open `evidence/s01.frames/cue01-*.png` and one later cue. Each shows the
  diagram with the Chinese line above the English line from the paired `.txt`. In the summary,
  `every cue: Chinese line above English line` is `ok`.
- **Score.** Confirm the mix. `render-s01.stdout` prints `Music: voice … LUFS, music … under speech / … in gaps`. The
  summary's `validation: music measured` detail has all three numbers, with music under speech
  well below the voice (e.g. −31 vs −16 LUFS).
- **Style.** Confirm the preset gate ran. `render-s01.stdout` contains `Style check passed: swiss tokens hold on sampled frames`.
- **Sidecar.** Read `evidence/s01.validation.json`. `source_matches_plan` is `true`, `caption_cues` equals the
  number of cues in `s01.zh-en.srt`, and `audio_mean_db` is above −45.
- **Episode under change.** When the change is to one episode, repeat **Render** with that episode's folder and a
  scene it touches. For a full-length proof, add no `--sample`: run
  `$C cli --run $RUN --name full -- python3 skill-library/conny-explainer-video/scripts/render.py outputs/verify/$RUN/work/<slug>-vfy$RUN`
  after a sample has created the copy. That run also enforces `duration_seconds`, missing anchors and `golden.json`.

## Gotchas

- A sample's length is its speech plus 0.8 s, not the episode's `duration_seconds`. The full-length
  duration gate, the anchor-not-found gate and the golden-frame check run only without `--sample`.
- Scene renders are cached by a stamp over `scenes.py`, the scene and six toolkit files
  (`scene.py voice.py i18n.py style.py subtitles.py events.py`). A change elsewhere in `explainer/`
  (e.g. `music.py`, `finishing.py`) only reruns post-processing, which is still fine because those
  steps run every time. A reused `$RUN` prints `Reusing s01`. Use a fresh id to prove the scene
  render itself.
- `narration.language: zh-CN` uses edge-tts, an online service, and needs network. Kokoro English is
  local.
- `render-sample` refuses `video.yaml` episodes (no `script.json`/`scenes.py`). Those use
  `python -m explainer.build`, which this map does not cover.
- A failing render leaves `outputs/<slug>-vfy$RUN/build/s01/render.log`. Read its tail, which is also in
  `render-s01.stderr`, before rerunning. Then run cleanup so the half-built copy does not linger.
