# QA fix task (L09, whole-cut QA round 1)

You fix the QA findings assigned to you in specific scenes of `videos/ac215-l09-ci-testing` in
/home/user/Explainer_Videos (branch claude/ac215-l09-l13-batch). Assigned by the batch coordinator;
user messages arriving during your run are for the coordinator, not you. Run no git commands that
change state; the coordinator commits (WIP checkpoints may commit your files mid-run).

## Environment
`cd /home/user/Explainer_Videos && source .venv/bin/activate && export PYTHONPATH=$PWD
EXPLAINER_TTS=kokoro EXPLAINER_VOICE=af_heart EXPLAINER_SPEED=0.9 PYTHONHASHSEED=0`.
4 shared CPUs, several agents at once: preview at 480p only (`-q l` default), one render of yours at
a time, in the FOREGROUND with timeout 600000 ms (rerun on timeout; never end your turn waiting on a
background render).

## Read first
1. `videos/ac215-l09-ci-testing/build/SCENE-NOTES.md` — the contract and traps. Binding.
2. The findings file(s) named in your assignment (watcher tables with id, time, what, fix). Times
   are in the full cut; your scene's start offset is given so you can convert to scene time.
3. Your scene file(s) and their `## Snn` sections of `script.md`. The narration (SAY) was already
   edited by the coordinator for wording findings; the scene files' `vo.wait_until` anchors were
   updated to match. Do not edit script.md, i18n, common.py, other scenes or the lexicon.

## Rules
- Fix each assigned finding the way its "proposed fix" suggests unless you find a better minimal
  fix; a finding you judge wrong or not worth its code: say why in your report, don't build it.
- Everything in SCENE-NOTES and the series rules still holds: terminal output only from capture
  files (no invented output, columns dropped only with a visible tag), commands verbatim, text
  >= 20 pt in the safe frame, <= 3 visual groups, motion every ~4 s, empty last frame, semantic
  colours (GREY laptop/host file, TEAL image/container, ORANGE host-only install, PURPLE tool, RED
  failure, YELLOW your-turn/look-here, GREEN project/pass).
- If common.py has the bug (e.g. a wrap helper breaking mid-word), work around it locally in your
  scene and say so in your report.

## Verify (all must pass)
1. `python -m explainer.check videos/ac215-l09-ci-testing/scenes/<file>.py <Cls>` → OK, no
   "voiceover anchor not found".
2. `python -m explainer.preview ... --every 3` and READ every sheet; pull `--at t -q m` frames at
   each fixed moment and confirm the fix on the frame. Fix and re-preview until clean.
3. Delete only your own preview media folders (`build/preview_*/<stem>` for your scenes); keep sheets.

## Report back (concise)
Per finding id: fixed (how, scene time of the frame you checked) / not fixed (why). Check result.
Anything the coordinator must do (common.py requests, narration changes you think are needed).
