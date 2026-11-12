# Incubator verification map

This directory is the maintained source for verifying what users of the incubator see and do.
Read this index before driving anything, then use the matching feature file as the recipe.
`$C` below means `python3 .claude/skills/verify-incubator/scripts/control.py`, run from
the repository root.

## Baseline preconditions

- `python3.12 tools/setup-runtime --dev` has finished once on this machine (see `../SKILL.md`, Launch).
- `$C doctor --run $RUN` prints only `OK` lines.
- `$RUN` is fresh: lowercase letters and digits, never reused across proofs. A reused id
  lets the renderer reuse a cached scene (`Reusing s01` in the log) instead of rendering it.
- The reference episodes are committed and unmodified unless the change under test touches them:
  `videos/skills-ecosystem/` (swiss, 12 scenes, CI's sample) and `videos/git-branch-pointer/`.
- Studio journeys: `$C studio-up --run $RUN` printed `READY http://127.0.0.1:<port>/`.

## Driving conventions

- Renders go through `$C render-sample`. It runs `skill-library/conny-explainer-video/scripts/render.py`
  on a run-owned copy of the episode, never on the episode folder itself.
- Terminal journeys go through `$C cli --run $RUN --name <label> -- <command>`, which keeps
  the command, stdout, stderr and exit code.
- Browser journeys go through `$C browse --run $RUN --name <label> features/steps/<file>.json`
  (paths relative to the skill folder, or absolute). Selectors are ARIA roles and names, ids, or
  rendered `aria-label`s. Never use coordinates.
- The board shows live GitHub state. Assert structure (headings, sections, at least one card), not
  today's counts.
- Treat every command as literal. Keep quoted names and flags unchanged.

## Proof and skip reporting

- Render proof is `<scene>.summary.json` with every check `ok`, the MP4, the validation sidecar
  and at least two cue frames you opened and compared with their `.txt`.
- CLI proof is the command, stdout, stderr and exit code.
- Browser proof is the ARIA snapshot, the full-page screenshot and `<label>.steps.json` with no
  failed step. Note any console errors it lists.
- Mutation proof (scaffold) includes a second, read-only look at what was written.
- Record the feature ID and entry point with every artifact you cite.
- Report an unreachable path with the attempted command and the unmet precondition. Never
  report a skipped entry point as verified through a different path.

## Feature entry contract

Each feature file starts with an H1 title and one paragraph describing the user-visible behavior.
It then uses exactly four H2 sections in this order:

1. `Sub-features` lists short IDs with one line for each behavior.
2. `How to get to it (user POV)` lists every user entry point.
3. `Driving it with control.py` starts with `Preconditions:` and uses labeled bullets that pair
   each user action with an exact command and an observable result.
4. `Gotchas` lists traps that can waste or invalidate a verification run.

## Features

- [Render a narrated sample](./render-sample.md) covers the sample render, captions, score,
  validation sidecar and frames. It is CI's journey and the default proof for engine changes.
- [Prepare speech only](./prepare-only.md) covers `--prepare-only`: speech clips and the timing plan
  without frames.
- [Scaffold a new episode](./new-episode.md) covers `new_episode.py`: the brief, the storyboard, the
  frozen style snapshot and the refusal to overwrite.
- [Studio progress board and library](./studio-board.md) covers the board Conny follows and the
  video library, built by `tools/studio_status.py`.
- [Studio new-episode composer](./studio-composer.md) covers required fields, the prefilled issue
  link, the manual-dispatch note and the kickoff prompt.
