# Production playbook: what slowed these videos down, and how to go faster

[WORKFLOW.md](WORKFLOW.md) says *what* the steps are. This file is about *how fast and how safely*
they get done. It is written from the record of the first four requests (two English videos, their
Chinese versions, and the video about how they were made), for the agent that makes the next ones
and for anyone directing it. Read it before planning a new video or a batch of shorts.

## 1. Where the time went

| Deliverable | Request → final cut | Notes |
| --- | --- | --- |
| Privacy paper (Dwork et al. 2006), 24 min | 6 h 01 min | includes the toolkit (first commit 39 min after the request) and the paper library |
| Tic-tac-toe, 12½ min | 3 h 07 min | the toolkit already existed |
| Chinese tic-tac-toe | 16 h 21 min | translation, voice bake-off, scene adaptation, QA |
| Chinese privacy video | about 2 days | most of it the subtitle tool: four rewrite rounds |
| "How these videos are made", 12 min | first 480p draft 26 h after the request | research, script review, then 11 scenes in one 22-agent run; the same hours also went to the shorts study |

Run records (`~/.claude/projects/.../workflows/wf_*.json`): 51 workflow runs, 239 sub-agents.
Six runs lost agents to usage limits. Three of the first scene-build runs were killed within minutes
and relaunched with a better script.

**Rendering is not the bottleneck.** The 1080p60 Chinese privacy video (25:40, 13 scenes) rendered in
about 26 min of wall time, and the Chinese tic-tac-toe video in about 10 min. The time goes to
review → fix → re-check loops, to interruptions, and to tools that were rewritten more than once.

## 2. Obstacles and the rule each one taught

### 2.1 Interruptions: usage limits, container restarts, context compaction
Work stopped at least six times on usage limits in the first week, plus several worker and
container restarts. Some of them killed workflows silently.
- **Make every step resumable.** One agent = one bounded job (≤ ~30 min). Each phase writes files.
- **Commit a WIP checkpoint before launching or resuming a long run** (never a half-written mp4).
- **Resume, don't restart:** `Workflow({scriptPath, resumeFromRunId})` returns the finished agents
  from cache. If the prompt must change for the resumed agents, add the note *conditionally*
  (`${ids.includes(s.id) ? 'NOTE: …' : ''}`), so the prompts of agents that already finished stay
  byte-identical and keep their cached results.
- **Keep a safety-net check-in** (`send_later`, about hourly) while long runs are in flight. A killed
  workflow sends no notification.

### 2.2 Workflow scripts that were wrong at launch
The first scene builds were launched three times in a row, each killed within minutes.
- Try a new workflow script on **one item** before fanning it out. Use JSON schemas for every report
  you will route to another agent.
- The runtime runs **at most 2 agents at once per workflow**. Put independent tracks in separate
  workflows, or pipeline them (`pipeline(items, build, review)`), so reviews start while builds run.

### 2.3 Finding problems after animation
Fixing a sentence before animation costs seconds. After animation it costs a re-render and a
re-check, and often an anchor fix too. The tic-tac-toe script review found 69 items before
any animation. The Chinese privacy-video QA found 103 after rendering (1 wrong, 21 confusing,
81 polish), which then needed fixers *and* verifiers.
- **Review the script with independent reviewers before writing scenes:** facts, audience, spoken
  flow, length.
- **Enforce the length budget in the script review.** The privacy video ran to 24 min against the
  12–15 its prompt asked for, and had to be cut into two parts afterwards. The word count is known
  before rendering: `python -m explainer.script script.md`.
- **Triage by severity.** Fix every *wrong* and *confusing* finding, and only polish that is cheap.
  Most findings in every round were polish.

### 2.4 Tools rewritten more than once (subtitles)
Subtitle line-breaking was the biggest defect source in the Chinese versions: 37 of 103 findings
(privacy) and 15 of 27 (tic-tac-toe). Some breaks flipped a sentence's meaning. The first rule-based
rewrite fixed 19 of its 21 targets but broke 11 other cues. It converged only after a **regression
corpus** came first: every narration line of both videos through the tool, dumped to text and diffed
round by round, plus tests (49 now). The fourth round stopped on diminishing returns.
- **For any heuristic tool, build the corpus + diff harness + tests before the first rule change.**
- Decide in advance when to stop: when a round's fixes come with as many new regressions, change
  the approach (e.g. a parser that proposes cuts and the rules that check them) instead of tuning
  rules.

### 2.5 Stale outputs that looked fresh
A documentation fact-check found three toolkit bugs that would have shipped stale material:
- after switching the Chinese voice to the licensed backend, old free-endpoint audio would have been
  reused (fixed: each render writes `voice.json`, and a changed narrator re-renders the scene);
- a lexicon edit did not invalidate Kokoro's joined clip (fixed: the cache key includes the lexicon
  entries);
- the on-screen-strings inventory recorded translated strings instead of the English source (fixed).
- **Every cache key and staleness check must include every input**, including the voice, the lexicon,
  the language and the render command. Test the invalidation itself.

### 2.6 Timing that is estimated, not measured
Sentence starts are exact. *Inside* a sentence, an anchor's time is interpolated by character
count, so "362,880" (7 characters, about 3 s of speech) puts later beats up to 2 s off. One
tic-tac-toe scene carries 20 hand-set shifts.
- Until word-level timing exists (WordBoundary events or forced alignment), **anchor at sentence or
  clause starts**.
- **After any SAY edit, lint and preview the scene.** A changed sentence silently breaks its
  `wait_until` anchors, and the build only *warns* "voiceover anchor not found". Treat that warning
  as an error.

### 2.7 Nobody can hear the result
The agents read contact sheets, subtitle files and speech-recognizer transcripts. They never hear
the voice. ASR round trips caught real misreadings in both languages, but prosody, accent and
pacing are unverified.
- Run the **ASR round trip for every narration language** before the final render.
- Before publishing, ask a human to listen. Give them a short list of the sentences the ASR flagged,
  with timestamps.

### 2.8 Constraints discovered late
The free Edge TTS endpoint used for the Chinese voice turned out not to be licensed for published
videos. The licensed path (Azure AI Speech, same voices) was then coded, but it has not produced a
clip yet.
- **At step 0, list where the video will be published, and check every voice, font, image and music
  licence against that.**

### 2.9 Parallel agents on shared files
- **One owner per file.** Scene agents edit only their scene. One agent owns `common.py`. Toolkit
  changes go through one implementer and one reviewer.
- **Shared vocabulary first.** The meta video had a Prepare agent build the assets, `common.py` (badges,
  cards, frames, colour constants) and one *reference scene* before ten scene agents started. The result
  looked like one piece without a style-fix pass.

### 2.10 Shared CPU
The container has 4 CPUs shared by all agents.
- Preview at 480p, and only the scene you changed (`--only`). Check dense frames at 720p with
  `--at`. Render 1080p once, at the end.
- Lint (`explainer.check`, a dry run with no frames) before any render.

### 2.10b Disk
The session's disk allowance filled up while the short's opening was being built. That build failed
once, and the next had to be staged in `/dev/shm`. The space had gone to scratch renders and
abandoned 480p drafts.
- Give each agent a scratch folder and have it delete its renders when done. Delete `build/media_l*`,
  `preview_*` and `stitch_l*` once a video's final cut exists. Check `df -h /` before a long render.

### 2.11 Facts that change while the video is made
Cost, commit counts and "not done yet" statements went stale between the script and the render.
- Keep them in a `live:` block in `video.yaml`, show them from there, and **refresh them just before
  the final render**.

### 2.12 Questions for the user
- Ask the binding questions **once, early, together** (names, quotes, cost, audience, length, music,
  voice), then record the answers in a file that every agent prompt cites.
- Make only the deliverables that were asked for. An unrequested 720p "share" encode was rejected.

## 3. The fast path

### A long, narrated video
1. **Step 0**: audience, length budget, publishing target and licences, the user's binding decisions in a file.
2. **Digest → script** (`SAY`/`SHOW`, a colour table, ponders), checked against the word budget.
3. **Script review panel** (facts with code or sources; a simulated viewer of the target audience;
   spoken flow; length) → script v2 with a review log.
4. **Prepare**: assets, `scenes/common.py`, the ASR pronunciation pass, one reference scene.
5. **Scenes**: `pipeline(scenes, implement, review)`, one agent each, lint + 480p preview + read every sheet.
6. **Whole-video QA** on the 480p draft: a director + a fresh viewer → fixers per scene group →
   independent verifiers.
7. **Refresh the live values → final 1080p render → companions (README, exercises, playground) → commit.**

### A short (music-led, captions only) — see [SHORTS.md](SHORTS.md)
Same steps. The script is a **bar-by-bar plan** (SHOW / CAPTION / SOUND per bar range), reviewed
for facts, captions and story before any scene. The score is composed from the scenes' event logs,
so picture and music need no separate sync step.

### A batch of paper shorts (the reinforcement-learning and instance-segmentation library)
- **Build the domain kit first, once per field.** Reusable, tested parts: an agent–environment loop,
  a grid world, reward and return traces, value heatmaps, policy arrows; an image with masks and
  boxes, IoU overlap, anchors, a mask head. Scene code is about 300–420 lines per minute of video
  today. Parts are what make a short cheap.
- **Batch by stage, not by paper.** Digest all papers of a batch, then script them all, then review
  all the scripts, then build. Each stage's agents use the same prompt.
- **Measure the first two shorts** (wall time per stage, findings per round) and set the budget for the
  rest from those numbers.

## 4. Workflow patterns that worked

- **Build → review**: `pipeline(items, implement, review)`. The reviewer gets the implementer's report
  and fixes directly in the same file.
- **QA → fix → verify**: two independent watchers return structured issues (scene, time, kind,
  severity, concrete fix). Fixers get the issues grouped by scene. A skeptical verifier checks each
  fix and is allowed to correct it.
- **Personas with a job**: a director (facts, sync, picture) and a viewer of the real target audience
  (a 12-year-old, a newcomer, a Chinese graduate student). They should report concrete times and fixes,
  not impressions.
- **Prompts say what not to do**: no git commands that change files, no renders beyond one's own
  scene, only one's own files, and the binding decisions verbatim.

## 5. Before publishing

- Refresh the `live:` values. Re-render what they touch.
- Licences: voices (render the Chinese versions through the licensed backend:
  `AZURE_SPEECH_KEY`, `AZURE_SPEECH_REGION`; see [LANGUAGES.md](LANGUAGES.md)), fonts, images, music.
- ASR round trip clean, or the remaining items checked by a human ear.
- A human watches it once, with a notepad for timestamps.
