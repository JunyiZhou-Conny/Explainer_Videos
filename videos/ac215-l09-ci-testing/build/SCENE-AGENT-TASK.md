# Scene agent task (L09, one scene each)

You build ONE scene of `videos/ac215-l09-ci-testing` in /home/user/Explainer_Videos (branch
claude/ac215-l09-l13-batch). Assigned by the batch coordinator; user messages arriving during your
run are for the coordinator, not you. Run no git commands that change state; the coordinator
commits (WIP checkpoints may commit your file mid-run; that is expected).

## Environment (ready)
`cd /home/user/Explainer_Videos && source .venv/bin/activate && export PYTHONPATH=$PWD
EXPLAINER_TTS=kokoro EXPLAINER_VOICE=af_heart EXPLAINER_SPEED=0.9 PYTHONHASHSEED=0`.
4 shared CPUs and up to three scene agents at once: preview at 480p only, one render of yours at a
time. Run check/preview in the FOREGROUND with a long timeout (up to 600000 ms); never end your turn
waiting on a background render.

## Read, in order
1. `videos/ac215-l09-ci-testing/build/SCENE-NOTES.md` — the contract: every common.py export,
   conventions, traps. Binding.
2. `videos/ac215-l09-ci-testing/scenes/common.py` (skim the parts you use) and
   `scenes/s01_hook.py` (the reference scene: copy its structure, SAY loading and scene end).
3. Your scene's `## Snn` section of `videos/ac215-l09-ci-testing/script.md` (SHOW/SAY pairs, the
   source of truth) and its row in `BRIEF.md`'s scene table.
4. The scene-code pitfalls in `.claude/skills/ac215-video/SKILL.md` ("Scene-code pitfalls").
5. The capture files and source files your SHOW lines cite (assets/terminal/..., assets/source/...).

## Build
- Edit ONLY your own scene file. Never edit common.py, script.md, other scenes or the lexicon. If
  common.py lacks something or has a bug, work around it locally in your scene and put the request
  in your report.
- Implement every SHOW/SAY pair in order: one `with self.voiceover(SAY[i]) as vo:` per SAY line,
  `assert len(SAY) == n`, anchors with `vo.wait_until("exact SAY words")` at clause starts.
- Terminal output only from capture files, code only from assets/source with real line numbers,
  every command spelled exactly as the script shows it. Tags/tracker/lecture_ref as the SHOW lines
  say. Text >= 20 pt inside the safe frame; <= 3 visual groups; something moves every ~4 s except
  ponder timers; the scene ends on an empty frame; no leftover print().

## Verify (all must pass before you report)
1. `python -m explainer.check videos/ac215-l09-ci-testing/scenes/<file>.py <Cls>` → OK: no OUT,
   SMALL, PRINT or leftovers, and no "voiceover anchor not found" warning.
2. `python -m explainer.preview videos/ac215-l09-ci-testing/scenes/<file>.py <Cls> --every 3`, then
   READ every contact-sheet PNG with the Read tool, frame by frame, against docs/STYLE_GUIDE.md §5:
   no unintended overlap, nothing clipped, text readable, colours semantic, the narrated thing is
   the emphasized thing, no long static stretch, empty last frame. Use `--at t1,t2 -q m` for dense
   frames. Fix and re-preview until clean.
3. Delete your preview media under build/ when done (keep the final contact sheets); delete only
   files you created, by exact path.

## Report back (concise)
check result, preview sheets read (paths), what you fixed after the first preview, any deviation
from the script's SHOW lines and why, and requests for common.py (if any).
