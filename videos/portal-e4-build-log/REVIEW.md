# Review record: Two days, a hundred-plus commits (项目周记 E4 · 两天、一百多个提交)

Produced 2026-10-30 by a Claude Code cloud session (issue
[#61](https://github.com/JunyiZhou-Conny/Explainer_Videos/issues/61)) on branch
`claude/funny-cannon-6at1kg`, in the 3Blue1Brown style (the house default since 2026-10-30). Verified
facts and unclaimed reviews are kept separate.

## Content gates (AGENTS.md)

1. **Hook.** s01 puts all 109 commits of PR #36 and PR #41 on one Boston-time clock, every one made by
   an agent, then asks two questions: why are most of them fixes, and with no person reviewing yet,
   who decided anything? ✔
2. **Intuition before formalism; an animated mechanism per core idea.**
   - s02 shows the pipeline issue → branch → draft PR, pushes waking two bots that only comment, a
     decision record moving 提议 → 已采纳, two session bars, and the stacked PR with its 13 merge arrows.
   - s03 shows session 1's first seven commits after a night of planning: 15 sources become 74 fact
     cards. Four walled-off reviewers find 75 problems (97 cards). One card is shown before and after.
   - s04 shows a word-list engine missing one phrasing and tripping on a harmless one, then the new
     shape: the model judges, and the checker on its output guards.
   - s05 shows a token going round push → bots → fix. 19 commits in about 100 minutes. The checker's
     bar grows 459 → 1,326 lines, and a whack-a-mole pair shows a false alarm, then a miss.
   - s06 shows prober agents firing phrasings at the checker; the 1,060 failures fill a jar that runs
     with the unit tests.
   - s07 shows the five-angle review, then six fix branches leaving one base and merging back after
     reproducing their bugs, with one collision. Usage-limit walls stand over a queue of six agents.
   - s08 has two receipts: bars for the stated model costs against a $0.50 cap, and token blocks with
     "$ ?" for the agents.
   - s09 sets your recorded calls against the agents' own calls, shows the stop rule's deadline and the
     last push on one Thursday axis, layers with holes stopping three bugs, and the twelve waiting items.
   - s10 marks the six phases on the clock.

   No code on screen. ✔
3. **Ponder moments and recap.** Two pause-and-ponder cards, each with a held pause:
   - s04: "The checker is word rules too. What would make it less of a whack-a-mole?" s06 answers it
     with probing before the push and failures kept as tests.
   - s09: "With no person having reviewed it yet, what makes this code trustworthy?" The layers answer it
     at once, along with decisions that wait for a signature.

   s10 recaps the six phases and asks three bilingual test-yourself questions, each answered in the
   episode (s05/s06, s07, s09), then holds a pause. ✔
4. **Written for the ear; anchored cues.**
   - Times are spelled out ("nine twenty-one", "one fifty-one", "a quarter to one").
   - "0004" and "0006" are spoken "decision four" and "decision six".
   - "7 p.m." became "seven in the evening", because the abbreviation split the sentence.
   - Chinese strings are shown, never read.
   - Every reveal waits on a word anchor; none is missing in the lint. ✔
5. **Simulated-viewer QA over the full draft.** Findings and fixes below. ✔
6. **Measured checks + human review.** Measured values under *Verified*. Human review: **waived** by
   Conny (AGENTS.md, 2026-10-22): 「我大概率是不会进行审片的，因为我觉得做得已经非常好了，就让bugbot来检查就好了」.
   No human has listened to this cut. ✔ (waiver)

## Research and script review before scenes

- **Research.** Two independent agents worked from the portal repository:
  - PR #36's history: phases, the checker's growth, bot threads, probing rounds, costs, and the
    owner's recorded decisions.
  - PR #41's process: the workflow docs, handoffs and the stop rule, the fix branches, the usage
    limits, and the twelve waiting items.

  I read the PR #41 handoff and its addendum myself for the twelve headings and the round-one split
  (80 + 62 misses, 148 + 82 false alarms).
- **Accuracy read** (a third independent agent, against `gh api` and `git log` with Boston time): 15
  findings, all applied. They are listed in `SOURCES.md`. The ones that changed the story:
  - **Bots.** Codex reviews only once a PR is marked ready. It never commented on draft #41.
  - **Review state.** No person has reviewed yet; two teammates were asked when #36 was marked ready.
    The handoff lists that click among the agent's own steps, though the workflow reserves it for a
    person (shown in s09).
  - **Whack-a-mole.** Both examples were on Wednesday, not Tuesday night. The first came from a real
    model run, not a bot.
  - **The checker.** It grew 459 → 1,326 lines after the turn, paired with 27 of the 45 commits since,
    not 39 of 60.
  - **Probes.** About 20 phrasings are still known misses, and there is no CI. The probes run with the
    unit tests.
  - **Fix agents.** They were queued, not run in parallel. There were collisions, and a second review
    found 8 more.
  - **Who decided.** Every recorded owner decision is an agent's paraphrase, and the owner made other
    calls too. Decision 0004 itself is still 「提议」.

## Whole-video QA (first draft, 7:44)

(filled after the viewer pass)

## Verified (final render)

(filled after the final render)

## Not claimed

- **No human listened** to this cut; the listen is waived (above). Prosody, pacing by ear and music
  balance by ear are unverified.
- **No ASR round trip.** Risky words were checked at the phoneme level instead, and all read as
  intended: Bugbot, Codex, the spelled-out times, 1,326, 1,060, 800,000, whack-a-mole, money-first,
  decision six's addendum, five-hundred-dollar deductible.
- **When the decisions were made** is not recorded; only when the commits landed. The 21:21 turn is
  the commit.
- **When the usage limits hit** is not recorded; the walls in s07 are not placed on the clock.
- **The agents' own spend** in dollars is not on record and is not estimated.
- The word-list examples in s04 and the layers-with-holes picture in s09 are illustrations.
- The Chinese captions were checked by the viewer pass for meaning, not by a separate translator.
- The portal PRs (#36, #41) are open, so the code may move after `17228bd` / `b7ab98e`.
  Decisions 0004 and 0006 are still "proposed".
