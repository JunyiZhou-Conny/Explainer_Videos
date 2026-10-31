# Brief: Two days, a hundred-plus commits (项目周记 E4 · 两天、一百多个提交)

Series: [docs/PORTAL_SERIES.md](../../docs/PORTAL_SERIES.md) · batch plan:
[videos/portal-series/README.md](../portal-series/README.md) · issue
[#61](https://github.com/JunyiZhou-Conny/Explainer_Videos/issues/61) · 3Blue1Brown style (the house default).

- **Question.** Conny, 2026-10-30: 「一步一步我们的 Claude 花这么多时间去做，他都干了些什么，他解决什么问题」.
- **Learning objective.** The viewer can retell the two days of PR #36 and PR #41 as a handful of
  phases on one Boston-time axis; explain why so many commits were fixes (the checker's
  whack-a-mole, and the switch to probing many phrasings before pushing); name how the work is
  organised (issue → branch → PR, stacked PRs, decision records, handoff notes, review bots,
  parallel fix agents, unattended runs and usage limits); say where a human decided and where an
  agent decided alone; state what it cost, using only the figures the PRs state; and list the
  decisions waiting for him.
- **Audience.** Conny after E1–E3 (knows the harness, the checker, the receipt, progress streaming,
  decision 0006, the chat page and its review rounds). Reads Python, not TypeScript.
- **Style / format.** `3b1b`, `video.yaml` route as in E2–E3: 1080p60, Kokoro `af_heart` 0.95,
  music, Chinese-above-English subtitles burned in. Target 8–9 minutes, 1,150–1,300 words.
- **Evidence rule.** Times, counts and quotes come from git (commit times converted to Boston), the
  week digest, the PR descriptions, handoff comments and review threads; costs only as stated in
  the PR text; decisions only as recorded. Nothing estimated is shown as measured.
- **Must include.**
  - All 109 commits on one clock: every one made by an agent; 40 under the owner's name.
  - The machinery:
    - issue → branch → draft PR;
    - Bugbot on every push and Codex once a PR is ready, both comment-only;
    - handoff notes, and decision records that a person adopts;
    - two sessions;
    - #41 stacked on #36.
  - Day one: a skeleton in forty minutes, then a fact check by four isolated reviewers (75 problems, 97 cards).
  - The turn at 21:21: word lists → the model judges, and the checker is the only safety layer. Quote decision 0004, and say that the agent wrote it.
  - The loop with the bots: 19 commits; 72 comments, 64 fixed. After the turn the checker grew from 459 to 1,326 lines, and 27 of the 45 commits since touched it. A whack-a-mole pair from Wednesday.
  - Probing before pushing: ≈ 3,000 phrasings, 142 misses and 230 false alarms. 1,060 kept as tests, with ≈ 20 known misses. 20 new false alarms caught before the push.
  - Queued fix agents: each reproduces its bug first; there are collisions, and a second review finds 8 more. Two usage limits; at most three agents per round afterwards.
  - Cost, only as stated: $0.036, ≈ $0.77, ≈ $0.27 against a $0.50 cap. Agents' cost appears only as tokens.
  - Who decided:
    - the owner's calls, as recorded;
    - the stop rule and how it was kept;
    - the agents' own calls, marked 「提议」 / 「无人值守」, including a click the workflow reserves for a person;
    - one honesty slip.
  - The layers that stand in for a human review. Decision 0004 is still 「提议」. Twelve questions wait for him.
  - The corrections from the accuracy pass are listed in `SOURCES.md`.
- **Skip.** The harness's four jobs (E1); thinking and streaming (E2); the chat page's design (E3).
- **Ponder questions.**
  - S04: the checker is word rules too. What would make it less of a whack-a-mole? (Answered in S07: attack it with thousands of phrasings before pushing, and keep the failures as tests.)
  - S06: why reproduce a bug before fixing it? (Answered at once: a check that has to flip from failing to passing.)
  - S07: the bots would have found these too; why attack the checker yourself first? (Answered: the bots report one at a time; one probing run found 372.)
  - S09: with no person having reviewed it yet, what makes this code trustworthy? (Answered at once: layers, plus decisions that wait for a signature.)
  - S10 recap questions:
    - Why did so many of the brain's commits touch the checker?
    - Why reproduce a bug before fixing it?
    - What is still waiting for you?
