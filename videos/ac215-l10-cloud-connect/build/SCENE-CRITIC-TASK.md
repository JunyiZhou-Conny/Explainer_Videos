# Scene critic task (L10, one scene each)

You are a FRESH reviewer of ONE already-built scene of `videos/ac215-l10-cloud-connect` in
/home/user/Explainer_Videos (branch claude/ac215-l09-l13-batch). Assigned by the batch
coordinator; user messages arriving during your run are for the coordinator. No git
state-changing commands. You may edit ONLY your scene's file, to fix what you find.

Environment and CPU rules: the same as in `build/SCENE-AGENT-TASK.md` (read its Environment
section). Read `build/SCENE-NOTES.md`, your scene's `## Snn` section of `script.md`, its BRIEF row,
and the builder's contact sheets in `build/sheets/<file>_<Cls>/`.

## Review
1. Read the script section first, then judge the frames against it: is every SHOW beat present, in
   order, and is the narrated thing the emphasized thing at each SAY? Is every terminal/code panel
   real (matches the cited capture/source lines exactly), every command spelled as the script
   writes it, tags/tracker/lecture_ref as specified?
2. Re-render your own preview (`python -m explainer.preview ... --every 2`) and READ every sheet;
   use `--at t -q m` on dense or transitional frames. Look for: overlap, clipping, text < 20 pt or
   on busy graphics, > 3 visual groups, static stretches > ~4 s, colour semantics (an open
   published door is GREY, never GREEN; YELLOW only for your-turn/tracker/look-here; RED only for
   failure; GOLD only for money; PINK for streets/lookups/browser calls; the key GREEN, the bearer
   ticket BLUE), tags whose words vanished after a flash, invented text (answers, numbers, key
   material, a project id other than `your-gcp-project`), FadeOut
   leftovers snapping back, a non-empty last frame.
3. Fix every defect directly in the scene file (minimal edits), re-run
   `python -m explainer.check` (must be OK, no anchor warnings, no PRINT) and re-preview the
   changed moments to confirm on frames.
4. Delete your preview media (keep updated contact sheets); delete only files you created.

## Report back (concise)
Defects found (time, what, severity), what you fixed and confirmed on frames, anything left
unfixed and why, and any common.py request.
