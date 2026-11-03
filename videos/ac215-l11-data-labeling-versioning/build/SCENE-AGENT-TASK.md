# Scene agent task (L11, one scene each)

You build ONE scene of `videos/ac215-l11-data-labeling-versioning` in /home/user/Explainer_Videos
(branch claude/mlops-learning-videos-7b5use). Assigned by the batch coordinator; user messages
arriving during your run are for the coordinator, not you. Run no git commands that change state;
the coordinator commits (WIP checkpoints may commit your file mid-run; that is expected).

## Environment (ready)
`cd /home/user/Explainer_Videos && source .venv/bin/activate && export PYTHONPATH=$PWD
EXPLAINER_TTS=kokoro EXPLAINER_VOICE=af_heart EXPLAINER_SPEED=0.9 PYTHONHASHSEED=0`.
The CPU is shared with other scene agents and other videos' renders: preview at 480p only, one
render of yours at a time. Run check/preview in the FOREGROUND with a long timeout (up to 600000 ms);
never end your turn waiting on a background render.

## Read, in order
1. `videos/ac215-l11-data-labeling-versioning/build/SCENE-NOTES.md` — the contract: every common.py
   export, conventions, colours, the CODE-ref table, traps. Binding.
2. `videos/ac215-l11-data-labeling-versioning/scenes/common.py` (skim the parts you use; the set
   pieces' docstrings list every part and method) and `scenes/s01_hook.py` (the reference scene:
   copy its structure, SAY loading and scene end). `build/common_test.py` (Bench) shows a working
   call of every set-piece method; its sheets are in `build/sheets/common_test_Bench/`.
3. Your scene's `## Snn` section of `videos/ac215-l11-data-labeling-versioning/script.md` (SHOW/SAY
   pairs, the source of truth), the script's Conventions at its top (TERM/CODE notation, tags,
   stand-ins, crops, honest framing), and your scene's paragraph in `BRIEF.md`'s Scene plan.
4. The scene-code pitfalls in `.claude/skills/ac215-video/SKILL.md` ("Scene-code pitfalls", "Never").
5. The capture files and source files your SHOW lines cite (`assets/terminal/laptop/NN-*.txt`,
   `assets/terminal/colab/CNN-*.txt`, `assets/source/...`; ASSETS.md says what each is).

## Build
- Your scene class name is the one video.yaml gives (the SCENE-NOTES table lists file and class).
  Never define a module-level name that shadows a common.py export (`CAPTION`, `code`, `note`,
  `tile`, `flag`, `drawer` …).
- Edit ONLY your own scene file. Never edit common.py, script.md, other scenes or the lexicon. If
  common.py lacks something or has a bug, work around it locally in your scene and put the request
  in your report.
- Implement every SHOW/SAY pair in order: one `with self.voiceover(SAY[i]) as vo:` per SAY line,
  `assert len(SAY) == SAY_COUNT["Snn"] == n`, anchors with `vo.wait_until("exact SAY words")` at
  clause starts. PONDER/QUICK cards with `ponder(...)` / `quick_predict(...)` right after their block.
- Terminal output only from capture files (`capture("NN").at(...)`, printed with `out()`), code only
  from assets/source with real line numbers (`code()`; see SCENE-NOTES' CODE table for the refs that
  need 20 pt, `cuts=`, windows or `source_rows()`), every command spelled exactly as the script shows
  it. Stand-in calls are output-only strips, never typed; `git push` and the SSH clone have no output
  panel. No invented output, numbers, task counts, expiry times, sizes, key/token material;
  placeholders only (`your-gcp-project`, `your-bucket-placeholder`, `student@example.com`,
  `YOUR_GITHUB_USERNAME`, the obviously fake token).
- **The instructor's name never appears on screen.** The loaders mask it (`‹instructor›`) and the
  instructor's e-mail (`student@example.com`); never read source text around them, never type a
  name into a label; the narration says "the instructor".
- Tags/tracker/`lref`/GOLD cost tags as the SHOW lines say; flash a tag only with
  `flash_tag(scene, tag, colour)`. Text ≥ 20 pt inside the safe frame; ≤ 3 visual groups;
  something moves every ~4 s except ponder timers; the scene ends on an empty frame; no leftover
  `print()`.
- The running map (V7 `PipelineMap.at("Snn")`) starts each scene in the state `MAP_AT` gives; light
  only your scene's piece.

## Verify (all must pass before you report)
1. `python -m explainer.check videos/ac215-l11-data-labeling-versioning/scenes/<file>.py <Cls>` → OK:
   no OUT, SMALL, PRINT or leftovers, and no "voiceover anchor not found" warning.
2. `python -m explainer.preview videos/ac215-l11-data-labeling-versioning/scenes/<file>.py <Cls> --every 3`,
   then READ every contact-sheet PNG with the Read tool, frame by frame, against docs/STYLE_GUIDE.md
   §5: no unintended overlap, nothing clipped, text readable, colours semantic, the narrated thing is
   the emphasized thing, no long static stretch, no name or e-mail of a real person, empty last
   frame. Use `--at t1,t2 -q m` for dense frames. Fix and re-preview until clean.
3. Delete your preview media under build/ when done (keep the final contact sheets in
   `build/sheets/<file>_<Cls>/`); delete only files you created, by exact path
   (`build/preview_l/<stem>`, `build/preview_m/<stem>`).

## Report back (concise)
check result, preview sheets read (paths), what you fixed after the first preview, any deviation
from the script's SHOW lines and why, and requests for common.py (if any).
