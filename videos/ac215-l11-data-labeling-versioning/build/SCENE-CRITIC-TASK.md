# Scene critic task (L11, one scene each)

You are a FRESH reviewer of ONE already-built scene of `videos/ac215-l11-data-labeling-versioning`
in /home/user/Explainer_Videos (branch claude/mlops-learning-videos-7b5use). Assigned by the batch
coordinator; user messages arriving during your run are for the coordinator. No git state-changing
commands. You may edit ONLY your scene's file, to fix what you find.

Environment and CPU rules: the same as in `build/SCENE-AGENT-TASK.md` (read its Environment
section). Read `build/SCENE-NOTES.md`, your scene's `## Snn` section of `script.md` (and the
script's Conventions at the top), its paragraph in `BRIEF.md`'s Scene plan, and the builder's
contact sheets in `build/sheets/<file>_<Cls>/`.

## Review
1. Read the script section first, then judge the frames against it: is every SHOW beat present, in
   order, and is the narrated thing the emphasized thing at each SAY? Is every terminal/code panel
   real (matches the cited capture/source lines exactly; crops respected), every command spelled as
   the script writes it, stand-in strips output-only and tagged, tags/tracker/`lref` as specified?
2. Re-render your own preview (`python -m explainer.preview ... --every 2`) and READ every sheet;
   use `--at t -q m` on dense or transitional frames. Look for: overlap, clipping, text < 20 pt or
   on busy graphics, > 3 visual groups, static stretches > ~4 s, colour semantics (an open published
   door is GREY, never GREEN; YELLOW only for your-turn/tracker/look-here; RED only for failure; GOLD
   only for money; PINK for streets, mount pipes, md5s and the rope; BLUE buckets, dvc_store/ and
   the signed ticket; GREEN key, pointer file and tags; the annotation a WHITE envelope), tags whose
   words vanished after a flash, invented text (outputs, numbers, task counts, expiry times, key or
   token material, a project id other than `your-gcp-project`), **any real person's name or e-mail
   (the instructor's name must read `‹instructor›` if it appears at all; e-mails `student@example.com`)**,
   CORS drawn as access control, photos drawn sorted into class folders or inside the host's
   `cheese_dataset/`, FadeOut leftovers snapping back, a non-empty last frame.
3. Fix every defect directly in the scene file (minimal edits), re-run
   `python -m explainer.check` (must be OK, no anchor warnings, no PRINT) and re-preview the
   changed moments to confirm on frames.
4. Delete your preview media (keep updated contact sheets); delete only files you created.

## Report back (concise)
Defects found (time, what, severity), what you fixed and confirmed on frames, anything left
unfixed and why, and any common.py request.
