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
Chinese above English captions, background music (a composed score mixed under the
narration). Current request and saved episode specs take precedence.

## The episode lifecycle

One GitHub issue per episode (template: *Episode request*) is the thread of record; one
draft PR per episode on branch `episode/<slug>`, touching only `videos/<slug>/`. Toolkit,
preset and docs changes go in their own small PRs — CI enforces this split and refuses
tracked media. Everything that matters is a file in the episode folder or a comment on the
issue/PR; if it happened anywhere else, it did not happen.

The `state:` label answers "where is this episode": `scripting → sample-review →
full-review → publishing → published`, plus `blocked:question` when an agent needs Conny.
Files are ground truth when a label drifts. Conny's review moments: the 20–30 s narrated
sample (comment on the PR; plain language is enough), and the full cut with audio — his
sign-off is quoted in `REVIEW.md` before merge.

**Content gates — an episode is not done without them, and `REVIEW.md` records each:**

1. A hook: a question, puzzle or broken thing in the first scene, not a value proposition.
2. Intuition before formalism; at least one real animated mechanism diagram per core idea
   (cards and labels are layout, not teaching).
3. Pause-and-ponder moments (aim for one per 2 minutes) and a content recap at the end.
4. Narration written for the ear, word-anchored cues where the engine gives exact marks.
5. A simulated-target-viewer QA pass over the full draft, with timestamped findings and fixes.
6. The measured checks (duration, loudness, caption bounds, music balance) from the
   validation sidecar, PLUS Conny's listening sign-off. Verified facts and unclaimed
   reviews stay separated, as in `videos/skills-ecosystem/REVIEW.md`.

After merge, `tools/release_episode.py` (run by CI or a producer session with release
rights) tags `episode/<slug>-vN`, uploads the deliverables with checksums, regenerates the
catalog and emits `PUBLISH.md`; the Mac publish worker (`tools/publish_worker.py`) uploads
to Bilibili and closes the issue with the BV link. Work that only a logged-in local machine
can do travels as `local-task` issues.

## Handoffs between agents

Different models and surfaces (Claude, GPT/Astra, Cursor, …) work these episodes, and none
of them can talk to another directly. The issue/PR thread is the only mailbox, and a session
can end without warning (usage limits, closed laptops). Therefore:

- **Same context for everyone.** Every agent starts from `docs/BOOTSTRAP.md` — the canonical
  reading order. A session that skipped it is working from a different map; don't.
- **Claim before working.** First action on an episode: comment on its issue —
  `Claiming. Model: <model>, surface: <claude.ai / Cursor / …>, branch episode/<slug>.`
  An episode with an active claim is not yours to touch. A claim stays active until its
  agent posts a handoff note (which releases it) or falls silent for 24 h (which expires it).
- **Handoff note before stopping.** Whenever a session may end (limit approaching, work
  pausing, question blocking), comment on the issue/PR before anything else:
  **DONE** (what is finished and where), **NEXT** (the single next step, concrete enough to
  execute without this session's memory), **WARN** (traps discovered: flaky anchors, layout
  constraints, decisions already rejected). Push the branch first — unpushed work does not
  exist to the next agent. Posting the note releases your claim: any agent may take over
  from NEXT by claiming anew. Still working and not handing off? Say so instead
  (`Still mine, continuing`) — that keeps the claim without releasing it.
- **Resuming is reading.** A resuming agent (any model) reads, in order: the issue thread,
  the PR thread, the episode folder, the latest handoff note — then continues from NEXT. It
  does not restart work a handoff marks DONE, and does not re-litigate decisions recorded in
  the brief or review threads; disagreements go to the issue as a question for Conny.
- Abandoned claims: a claim with no push and no comment for 24 h is expired even without a
  handoff note; note the takeover in a comment and continue from the last pushed state.
