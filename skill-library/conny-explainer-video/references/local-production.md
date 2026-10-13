# Production from a checkout

Run commands from the repository root. macOS and Linux are the supported setup targets.
Use Python 3.12 and an isolated `.venv`. Install system prerequisites first: FFmpeg (including
ffprobe and libass), Cairo/Pango development libraries and pkg-config. On macOS with Homebrew:

```bash
brew install python@3.12 ffmpeg cairo pango pkg-config
python3.12 tools/setup-runtime
```

The setup script installs the episode route's Python requirements and downloads local Kokoro
speech models and OFL fonts verified against `assets/manifest.json`. It does not install global
Python packages, register system fonts or change the original toolkit's `requirements.txt`.
On Linux (verified on Ubuntu 24.04, including GitHub Actions runners) install exactly:

```bash
sudo apt-get install -y python3.12-venv libpango1.0-dev libcairo2-dev pkg-config ffmpeg
python3.12 tools/setup-runtime --dev
```

ManimPango has no Linux wheel, so the pangocairo *development* headers are required (the
runtime libraries are not enough); the setup now preflights this and fails fast with the
command above. `--dev` also installs pytest. **The test command is `python -m pytest -q tests`**;
`unittest discover` silently collects only a fraction of the suite — never trust its green.
`setup/install.sh` remains the original full-toolkit setup, including
LaTeX for equation-heavy episodes; inspect its system-package actions before running it.
The Swiss example uses text/vector diagrams and does not require LaTeX.

## New episode route

```bash
python3 skill-library/conny-explainer-video/scripts/new_episode.py git-branches --topic "Explain Git branches" --preset nasa-punk --workspace .
```

This writes `videos/git-branches/episode.json`, `storyboard.md` and a `style.md` snapshot.
It does not author the script or scenes. The agent inspects topic evidence, writes bilingual
`script.json`, and implements topic-specific diagrams in `scenes.py`. Use
`videos/skills-ecosystem/` as the working timing/voice example, not as a diagram template for
unrelated lessons. Scene IDs `s01`, `s02`, … map to Manim classes `S01`, `S02`, …; each narration
line supplies `en` and `zh`. `EpisodeScene` shows `VoiceScene.voiceover()` and the measured
caption sidecars required by the engine. Register project fonts in each scene process.

```bash
python3 skill-library/conny-explainer-video/scripts/render.py videos/git-branches --sample s01
python3 skill-library/conny-explainer-video/scripts/render.py videos/git-branches
```

The helper selects this checkout's `.venv/bin/python`. The direct command is
`.venv/bin/python tools/render_episode.py videos/git-branches`. `--prepare-only` synthesizes
speech and saves timing without rendering frames. `--sample s01` renders one narrated scene;
`--jobs 2` bounds parallel scene jobs. Saved episode settings override shared defaults.
Outputs go to `outputs/<slug>/` and are ignored by Git.

The engine (explainer/episode.py) speaks **English (Kokoro, sentence-exact timing)** or
**Chinese (`narration.language: zh-CN`; edge-tts by default, upgraded to Azure when
`AZURE_SPEECH_KEY/REGION` are set — timing marks are then estimated)**, always with burned
Chinese-above-English captions, and mixes a **composed score by default** (`music.enabled`
in defaults/episode.json; `--no-music` for one build) from the scenes' event logs, ducked
under the narration and asserted in the validation sidecar. 1920×1080@30 is the validated
profile; other resolutions render with a warning and need their own sample review. Any other
voice/subtitle format still requires an implemented and sample-reviewed route; a preference
in JSON does not add a backend. Presets specify design: scenes must implement them. The
existing Swiss example is the complete implementation supplied here.

## Original episode route

Existing `video.yaml` projects continue to use:

```bash
.venv/bin/python -m explainer.build videos/tictactoe-255168 -q l
.venv/bin/python -m explainer.build videos/tictactoe-255168
```

Read `docs/WORKFLOW.md`, `docs/STYLE_GUIDE.md`, `docs/LANGUAGES.md`, and the episode's own specs.
Use the root `requirements.txt` and original setup for these projects. They may require CMU
fonts, LaTeX and optional narration services. Do not feed `video.yaml` to the JSON runner or
assume the newer five-minute/30 fps defaults alter an existing episode's 60 fps specification.

## Review and delivery

Inspect the actual speech, captions, diagrams, pacing and boundaries as well as ffprobe
metadata. A complete review includes playback/listening; numerical validation cannot establish
pronunciation or teaching quality. Save a candid `REVIEW.md`. Publish final MP4s as GitHub
release assets and keep editable sources, caption sidecars, source notes and a release checksum
in Git. See `docs/PUBLISHING.md`. Rendering alone does not publish anything.
