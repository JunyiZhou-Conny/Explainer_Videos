# Explainer Videos

Bespoke, 3Blue1Brown-style explainer videos for the research papers I'm reading, generated with
an LLM, [Manim](https://www.manim.community/) and a neural narrator. Plus the library they come
from, organised so that every paper knows which papers it builds on.

> *"The output format I am most bullish on is fully custom / bespoke explainer videos generated on
> any arbitrary topic."* — Andrej Karpathy

## Why this exists

Reading papers is slow, and LLM summaries are a wall of text you forget by tomorrow. An explainer
video gives the intuition *before* the details: you see the objects move, then you read the
formula that describes what you just saw. But watching is still passive. Learning is training a
neural net — the one in your head — and it only updates when you do the work yourself. So each
video here is built to be a **mentor**, not a substitute:

- **It places the paper on a map.** What problem did it inherit? What changed? What grew out of
  it? Every video opens and closes with the paper's lineage, so papers stop being isolated objects.
- **It asks you to think.** *Pause and ponder* moments in the video, test-yourself questions at the
  end, and an `exercises.md` companion with pen-and-paper problems and a small coding task.
- **It points back into the paper.** A page-referenced `digest.md` tells you exactly which pages
  to read, in what order, and where the paper has typos.

The next step after videos is interactivity — playgrounds where you have to *produce* something
(set the noise, break the mechanism, derive the bound). The pieces here are built with that in mind.

## Videos

| | Video | Papers | Length |
| --- | --- | --- | --- |
| 🎬 | [Calibrating Noise to Sensitivity — the paper that invented differential privacy](videos/dwork2006-calibrating-noise/) | Dwork, McSherry, Nissim, Smith (TCC 2006) | ~24 min, also cut in two parts (~15 + ~9 min) |
| 🎬 | [Why are there exactly 255,168 games of tic-tac-toe?](videos/tictactoe-255168/) (for middle school) | — (counting, recursion and backtracking) | ~12½ min |

Each video folder has: `output/*.mp4` (the video, plus part cuts for long ones), `output/*.srt`
(subtitles), `output/chapters*.txt`, `script.md` (narration + visual plan), `exercises.md`, the
Manim source in `scenes/`, and (for paper videos) `digest.md` (paper notes). Each also has a
`playground.html`, an interactive page that is a first step from watching to doing. In the privacy
video you play the attacker against the Laplace mechanism. In the tic-tac-toe video you play moves
and watch how many games are still possible.

## Repository layout

```
library/                    the papers, filed by category
  catalog.yaml              ← single source of truth: metadata, categories, "builds on" links, reading paths
  README.md                 generated shelf view (by category)
  MAP.md                    generated knowledge graph + reading paths + multi-paper video ideas
  <area>/<topic>/<id>.pdf   e.g. reinforcement-learning/policy-optimization/schulman2017ppo.pdf
videos/<video-id>/          one folder per video (single- or multi-paper)
explainer/                  the toolkit: TTS backends, narration-synced scenes, components, build
tools/                      ingest.py (add a paper) · catalog.py (validate + regenerate) · new_video.py
docs/WORKFLOW.md            paper → digest → script → review → scenes → render, with prompts for Claude
docs/STYLE_GUIDE.md         visual language: semantic colours, layout, timing, checklist
setup/install.sh            one-shot environment setup
```

## Quick start

```bash
bash setup/install.sh && source .venv/bin/activate

# add a paper to the library
python tools/ingest.py ~/Downloads/2402.03300.pdf --category reinforcement-learning/policy-optimization

# render the existing video (fast draft, then final 1080p60)
python -m explainer.build videos/dwork2006-calibrating-noise -q l
python -m explainer.build videos/dwork2006-calibrating-noise

# start a new one
python tools/new_video.py schulman2017ppo --id ppo-explained
```

Narration defaults to **Kokoro** (free, runs locally on CPU). To use ElevenLabs instead:
`export ELEVENLABS_API_KEY=...` and set `voice: {backend: elevenlabs, voice: <voice-id>}` in the
video's `video.yaml` (or `EXPLAINER_TTS=elevenlabs` for one run). See [docs/WORKFLOW.md](docs/WORKFLOW.md).

## Making a video with Claude Code

The whole pipeline is designed to be driven by an agent. A good opening prompt:

> Make a 3Blue1Brown-style explainer video of `library/<category>/<id>.pdf` for a newcomer, about
> 12–15 minutes. Follow docs/WORKFLOW.md and docs/STYLE_GUIDE.md: digest the paper, write
> script.md with a lineage map (before/after), pause-and-ponder moments and recap questions,
> review it for accuracy against the PDF, then build and render the scenes.

For a multi-paper video, name 2–5 papers (see *Multi-paper video ideas* in `library/MAP.md`) and ask
for one story that connects them.
