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

Defaults for new episodes: 3b1b (since 2026-10-30, owner: 「以后默认用3blue1brown的style」; Swiss
before), five minutes, 1920×1080 at 30 fps, English narration, Chinese above English captions,
background music (a composed score mixed under the narration). Current request and saved episode
specs take precedence; existing episodes keep the preset in their own spec.

## The episode lifecycle

One GitHub issue per episode (template: *Episode request*) is the thread of record; one
draft PR per episode on branch `episode/<slug>`, touching only `videos/<slug>/`. Toolkit,
preset and docs changes go in their own small PRs — CI enforces this split and refuses
tracked media. Everything that matters is a file in the episode folder or a comment on the
issue/PR; if it happened anywhere else, it did not happen.

The `state:` label answers "where is this episode": `scripting → sample-review →
full-review → publishing → published`, plus `blocked:question` when an agent needs Conny.
Files are ground truth when a label drifts. Conny's review moments are optional by default
since 2026-10-22 (「我大概率是不会进行审片的，因为我觉得做得已经非常好了，就让bugbot来检查就好了」):
post the 20–30 s narrated sample on the PR for the record and keep going, rely on the QA
passes and review bots, and quote this waiver in `REVIEW.md` in place of a listening sign-off
(as `videos/ac215-l02-containers-1/REVIEW.md` does for the AC215 series). If he does listen
or comment, his words take precedence and are quoted instead.

**Content gates — an episode is not done without them, and `REVIEW.md` records each:**

1. A hook: a question, puzzle or broken thing in the first scene, not a value proposition.
2. Intuition before formalism; at least one real animated mechanism diagram per core idea
   (cards and labels are layout, not teaching).
3. Pause-and-ponder moments (aim for one per 2 minutes) and a content recap at the end.
4. Narration written for the ear, word-anchored cues where the engine gives exact marks.
5. A simulated-target-viewer QA pass over the full draft, with timestamped findings and fixes.
6. The measured checks (duration, loudness, caption bounds, music balance) from the
   validation sidecar, PLUS Conny's listening sign-off or the recorded waiver above. Verified facts and unclaimed
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
- **One session per episode.** A session's working memory (what it tried, why, Conny's
  in-chat taste notes) does not survive a switch; files do. A session that hits a usage
  limit waits for the reset and continues in the same session. Passing an episode to another
  model or session is a last resort, not a routine.
- **Claim before working.** First action on an episode: comment on its issue —
  `Claiming. Model: <model>, surface: <claude.ai / Cursor / …>, branch episode/<slug>.`
  An episode with an active claim is not yours to touch. A claim stays active until its
  agent posts a `HANDOFF` (which releases it) or falls silent for 24 h (which expires it).
  Checkpoints keep it active.
- **Checkpoint at every stage boundary.** Limits cut a session off without warning, so there
  is no last moment to write a note. Instead, at each stage boundary — `brief`, `script`,
  `sample`, `scenes`, `full-cut` — push the branch, then comment on the issue with a first
  line `CHECKPOINT <stage>` followed by **DONE** (what is finished and where), **NEXT** (the
  single next step, concrete enough to execute without this session's memory) and **WARN**
  (traps discovered: flaky anchors, layout constraints, decisions already rejected). An
  interruption then costs at most the stage in progress. Unpushed work does not exist to the
  next agent.
- **Handoff only on purpose.** An agent that deliberately gives the episode away posts a
  comment whose first line is `HANDOFF`, with DONE / NEXT / WARN. That releases the claim:
  any agent may take over from NEXT by claiming anew.
- **Resuming is reading.** A resuming agent (any model) reads, in order: the issue thread,
  the PR thread, the episode folder, the latest `CHECKPOINT` or `HANDOFF` — then continues
  from NEXT. It does not restart work marked DONE, and does not re-litigate decisions
  recorded in the brief or review threads; disagreements go to the issue as a question for
  Conny. Rendered outputs and TTS caches are not in git: a successor re-renders before
  relying on them.
- Abandoned claims: a claim with no push and no comment for 24 h is expired even without a
  `HANDOFF`; note the takeover in a comment and continue from the last checkpoint.

## Progress on the Studio board

Conny follows production on the Studio site (`site/`, built by `tools/studio_status.py` on every
issue label or comment), not in your chat. It can only show what the issue says, so keep the
issue telling the truth:

- **Stage vocabulary.** An episode moves through `brief → script → scenes → qa → finish →
  render → stitch`, then `ready` (episode PR waits for merge), `publishing` (released, waits
  for the Mac worker) and `published`. Checkpoint names map onto it (`captures`/`brief`,
  `script`, `sample`/`scenes`, `qa`, `full-cut`; `CHECKPOINT <stage>` means that stage is done).
  Between checkpoints, keep exactly one stage label on the issue: `▶ 制作场景`, `▶ 整片审查`,
  `▶ 收尾修改`, `▶ 渲染 1080p`, `▶ 拼接与检查`, `✔ 等待合并发布`. The newer of the stage label
  and the latest checkpoint wins; the `state:` labels win once an episode is ready.
- **Progress inside a long stage (optional).** A line `Progress: <stage> <done>/<total>` in a
  checkpoint or any comment (e.g. `Progress: scenes 9/16`) fills that stage's bar on the board.
- **Say when you stop.** When Conny pauses you, or you wait for anything only he can give,
  put it on the issue: `⏸ 暂停` for a pause, `blocked:question` plus the question as a
  comment for a decision. A question asked only in chat is invisible to the board.
- Batch sessions pipeline several episodes on one branch; the board treats a claimed episode
  with no progress as queued behind its siblings, and judges liveness by the branch's last
  push, so push WIP at least daily while working.
