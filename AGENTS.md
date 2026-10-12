# Working in the video incubator

Read `skill-library/conny-explainer-video/SKILL.md` for video production and named presets.
The repository copy is the shared source of truth; `.agents/skills` and `.claude/skills`
contain relative aliases. If a client does not discover them, read the canonical file explicitly.
Do not depend on a personal skill with the same name being the same version.

- Start with the requested audience, learning outcome and actual topic sources. Use
  `docs/VIDEO-WORKFLOW.md` for short prompts and `docs/STYLES.md` to choose a style.
- Preserve existing `video.yaml` episodes and the `explainer/` toolkit. Their legacy route is
  in `docs/WORKFLOW.md`; new `episode.json` projects use `tools/render_episode.py`.
- A preset is visual guidance. Author topic-specific diagrams and prove a representative
  narrated scene before claiming a new style is implemented. Track technical validation and
  listening/full-playback review separately in the episode's `REVIEW.md`.
- Keep each episode's brief, script, sources, style snapshot, scenes and handoff together in
  `videos/<slug>/`. Assign separate files to concurrent agents; one agent owns integration.
- Changes intended for future videos belong in the versioned skill/preset. One-episode
  experiments belong in its brief. Use `docs/STYLE-LIFECYCLE.md` when adding or refining styles.
- Store rendered movies as release assets and index them in `catalog/videos.json` and
  `docs/VIDEOS.md`. Existing tracked movies remain available. Keep reference downloads,
  credentials, local user inventories, models, caches and private working files out of Git.
- Work on a topic branch, inspect the diff, run relevant checks, and publish only the work
  requested. Never merge other agents' unrelated open PRs as a shortcut to obtain a toolkit.

Defaults for new episodes: Swiss, five minutes, 1920×1080 at 30 fps, English narration,
Chinese above English captions. Current request and saved episode specs take precedence.
