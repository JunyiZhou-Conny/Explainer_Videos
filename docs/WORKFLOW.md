# From paper to explainer video

The production pipeline, step by step, with the prompts that work well when you hand a step to
Claude Code. Every step leaves a file behind, so you can stop, review, and resume.
[PLAYBOOK.md](PLAYBOOK.md) has the lessons from the first videos: where the time went, and the
rules that make the next one faster.

```
PDF ──ingest──▶ library/catalog.yaml ──plan──▶ videos/<id>/
                                                 ├─ digest.md     what the paper actually says (with page refs)
                                                 ├─ script.md     SAY/SHOW narration plan  ◀── reviewed
                                                 ├─ scenes/*.py   Manim scenes, timed to the narration
                                                 ├─ exercises.md  active-learning companion
                                                 └─ output/       <id>.mp4 · <id>.srt · chapters.txt · transcript.md
```

## 0. Setup (once)

```bash
bash setup/install.sh          # ffmpeg, LaTeX, cairo/pango, Python venv, Kokoro voice model
source .venv/bin/activate
python -m explainer.voice "Calibrating noise to sensitivity."   # prints the path of a test clip
```

## 1. Ingest papers

```bash
python tools/ingest.py ~/Downloads/paper.pdf --category reinforcement-learning/policy-optimization
python tools/ingest.py --arxiv 2402.03300 --category reinforcement-learning/policy-optimization
python tools/ingest.py --list-categories
python tools/ingest.py paper.pdf --category robotics/imitation-learning --new-category "Imitation learning"
```

The PDF is filed under `library/<category>/<id>.pdf` and a stub entry is appended to
`library/catalog.yaml`. Then:

> **Prompt:** *Catalogue the new paper `<id>` in library/catalog.yaml: read the PDF, fill in
> short_name, venue, one_liner, key_ideas, tags, and builds_on/cites (only library papers you can
> find in its reference list). Then run `python tools/catalog.py`.*

`python tools/catalog.py` validates the catalog and regenerates `library/README.md` (the shelf,
by category) and `library/MAP.md` (a Mermaid graph of which paper builds on which, reading paths,
and multi-paper video ideas).

## 2. Plan the video

Single paper or a story across several? Look at `library/MAP.md` → *Multi-paper video ideas*.

```bash
python tools/new_video.py dwork2006calibrating --id dwork2006-calibrating-noise
python tools/new_video.py shao2024deepseekmath yu2025dapo --id grpo-to-dapo --title "From GRPO to DAPO"
```

## 3. Digest → script

> **Prompt:** *Read `library/.../<paper>.pdf` completely and write `videos/<id>/digest.md`:
> problem, setting, every definition/theorem with page numbers, the proof ideas, the examples,
> what is new vs prior work, and any errata. Then write `script.md` following the format of
> `videos/dwork2006-calibrating-noise/script.md`: a hook, a "where this paper sits" map (prior
> work → this paper), intuition before each formula, at least one pause-and-ponder, a legacy map
> (what grew from it), and recap questions. Target ~N minutes (≈155 spoken words per minute).*

Rules of thumb for `script.md`:
- `SAY:` lines are read aloud by TTS: spell out symbols ("e to the epsilon", "one over n").
- Each `SAY:` line is one beat; its `SHOW:` line says what the viewer sees during it.
- Keep a fixed semantic colour table at the top.
- Check length with `python -m explainer.script videos/<id>/script.md`.

## 4. Review the script (before any animation)

> **Prompt (ultracode):** *Review `videos/<id>/script.md` with independent reviewers: (1) technical
> accuracy against the PDF, (2) fact-check of historical claims with web sources, (3) a newcomer's
> pedagogy pass, (4) tightening to N words. Merge the fixes.*

Fixing a sentence here costs seconds; fixing it after animation costs a re-render.

## 5. Build the scenes

One file per scene in `videos/<id>/scenes/`, each a `VoiceScene` that pulls its narration from
`script.md` (`NARRATION["S04"][i]`) — see `docs/STYLE_GUIDE.md` and the scenes of the first video.

```bash
python -m explainer.preview videos/<id>/scenes/s04_definition.py Definition      # contact sheet PNG
python -m explainer.preview videos/<id>/scenes/s04_definition.py Definition --tts silent  # no TTS
python -m explainer.check videos/<id>/scenes/s04_definition.py Definition      # lint: off-frame, < 20 pt, leftovers
```

> **Prompt (ultracode):** *Implement every scene of `videos/<id>/script.md` (one agent per scene or
> pair), following docs/STYLE_GUIDE.md. Each agent previews its scene, inspects the contact sheets,
> fixes overlaps; then an independent reviewer checks the frames against the script.*

## 6. Render

```bash
python -m explainer.build videos/<id> -q l      # fast 480p draft of the whole video
python -m explainer.build videos/<id>           # final 1080p60
python -m explainer.build videos/<id> --only s07_laplace   # re-render one scene, re-stitch
python -m explainer.build videos/<id> --crf 26  # smaller file for sharing
```

Output in `videos/<id>/output/`: the mp4 (loudness-normalised), `.srt` subtitles,
`chapters.txt` (paste into a YouTube/Bilibili description), `transcript.md`.

A build re-renders a scene when its movie is missing or older than what it is built from: the
scene's folder, `script.md`, `video.yaml`, `assets/`, and the toolkit modules a scene imports.
Command-line tooling (`build.py`, `check.py`, `preview.py`), the after-render modules (`music.py`,
`finishing.py`) and, for narrated videos, the short-only modules (`short.py`, `grid.py`,
`captions.py`) do not count; a change to the render command itself needs `--only`.

Background music composed from the picture (every scene writes `<Scene>.events.json` as it renders):
`python -m explainer.build videos/<id> --music` mixes it under the narration and keeps the
narration-only master as `<id>.nomusic.mp4`. A condensed, music-led short of a video is its own
project (`format: short`): see [SHORTS.md](SHORTS.md).

## Voices

| backend | cost | quality | how |
| --- | --- | --- | --- |
| `kokoro` (default) | free, local CPU | natural, slightly flat | `voice: af_heart` (also `am_michael`, `bf_emma`, `bm_george`, …) |
| `elevenlabs` | paid API | best | `export ELEVENLABS_API_KEY=...`, `voice.backend: elevenlabs`, `voice.voice: <voice id>` |
| `edge` | free, online | good | `pip install edge-tts`, `voice.backend: edge`, `voice.voice: en-US-AndrewNeural` |
| `espeak` | free, local | robotic | fallback |
| `silent` | — | — | layout previews without audio |

Set it per video in `video.yaml` (`voice:`), or per run: `EXPLAINER_TTS=elevenlabs python -m explainer.build ...`.
Clips are cached in `.cache/tts/`, so switching voices only re-synthesises once.
Mispronounced word? Add it to `explainer/lexicon.yaml` (IPA for Kokoro, respelling for others).

## 7. Learn from it (the point of all this)

- Watch once straight through. Then do `exercises.md` *without* re-watching.
- Re-watch only the chapter you got wrong (chapters are in `output/chapters.txt`).
- Write one paragraph in your own words in the paper's catalog entry (`notes:`) and set
  `status: read` — or make the next video yourself.
