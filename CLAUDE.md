# CLAUDE.md

3Blue1Brown-style explainer videos of research papers (Manim CE 0.21 + the toolkit in `explainer/`),
with Chinese versions and music-led shorts. Read [docs/PLAYBOOK.md](docs/PLAYBOOK.md) before planning
a video. It records what slowed the first videos down and the rules that came from it.

## Environment
- Python: `.venv` from `bash setup/install.sh`. The cloud container already has `/opt/explainer-venv`.
- Run from the repo root with `PYTHONPATH=<repo root>` (the package is not installed).
- 4 shared CPUs. Many agents preview at once, so render only what changed.

## Commands
```bash
python -m explainer.script videos/<id>/script.md                      # word count / duration, caches the voice
python -m explainer.check  videos/<id>/scenes/s03_x.py Class          # lint: off-frame, < 20 pt, leftovers (no render)
python -m explainer.preview videos/<id>/scenes/s03_x.py Class --every 3   # 480p + contact sheets; -q m --at t1,t2
python -m explainer.build videos/<id> -q l                            # 480p draft of the whole video
python -m explainer.build videos/<id> --only s03_x                    # re-render one scene, re-stitch
python -m explainer.build videos/<id>                                 # final 1080p60 (--crf 25 for a smaller file)
python -m explainer.build videos/<id> --lang zh                       # Chinese version -> output/zh/
python -m explainer.build videos/<id> --music                         # score from the event logs
python -m pytest -q tests                                             # toolkit tests (subtitles, music, shorts)
```

## Rules
- `script.md` is the source of the narration. One `with self.voiceover(SAY[i]) as vo:` per SAY line.
  Never hard-code narration in a scene.
- After any SAY edit, re-run `check` and `preview` for that scene. The build only *warns*
  "voiceover anchor not found", so treat that warning as an error. Anchor at sentence or clause
  starts: timing inside a sentence is estimated from character counts.
- Review the script before animating. Fix the length there: the word count is known before rendering.
- Shared visual vocabulary goes in `videos/<id>/scenes/common.py`, built first, with one reference
  scene. Each file has one owner when agents work in parallel.
- Every cache key and staleness rule must cover every input (voice, lexicon, language, assets).
- Values that change while a video is made (cost, counts, "not done yet") go in `video.yaml`
  `live:`. Refresh them just before the final render.
- The Chinese voice: the free Edge endpoint is for drafts only. Published Chinese videos are rendered
  through Azure AI Speech (`AZURE_SPEECH_KEY`, `AZURE_SPEECH_REGION`); see docs/LANGUAGES.md.
- Agents cannot hear. Run the ASR round trip for each narration language, and ask a human to listen
  before anything is published.
- Lexicon entries (`explainer/lexicon.yaml`) change the English cache keys of every video that uses
  the word. Check with `grep` across `videos/*/script.md` first.

## Long runs (usage limits and restarts happen)
- Small resumable steps that leave files behind. Commit a WIP checkpoint before launching or resuming a
  long run. Never commit a half-written mp4: `output/` keeps only final cuts, and drafts
  (`*_480p15.*`, `*_720p30.*`) are gitignored.
- Workflows run at most 2 agents at once. Resume with `resumeFromRunId`, and add notes for the
  resumed agents only conditionally, so cached prompts stay unchanged.
- Keep an hourly `send_later` check-in while long runs are in flight.

## Docs
- [docs/WORKFLOW.md](docs/WORKFLOW.md): the steps, paper to video.
- [docs/STYLE_GUIDE.md](docs/STYLE_GUIDE.md): the look and the scene checklist.
- [docs/LANGUAGES.md](docs/LANGUAGES.md): translations, voices, bilingual subtitles.
- [docs/SHORTS.md](docs/SHORTS.md): condensed, music-led shorts.
- [docs/PLAYBOOK.md](docs/PLAYBOOK.md): speed and safety lessons.
