# Review record: Two days, a hundred-plus commits (项目周记 E4 · 两天、一百多个提交)

Produced 2026-10-30 by a Claude Code cloud session (issue
[#61](https://github.com/JunyiZhou-Conny/Explainer_Videos/issues/61)) on branch
`claude/funny-cannon-6at1kg`, in the 3Blue1Brown style (the house default since 2026-10-30). Verified
facts and unclaimed reviews are kept separate.

## Content gates (AGENTS.md)

1. **Hook.** s01 puts all 109 commits of PR #36 and PR #41 on one Boston-time clock, every one made by
   an agent. Then it asks two questions: why are most of them fixes (the 53 that name a review light
   up), and, with no person reviewing yet, who decided anything? ✔
2. **Intuition before formalism; an animated mechanism per core idea.**
   - s02 shows the pipeline issue → branch → draft PR, pushes waking two bots that only comment, a
     decision record moving 提议 → 已采纳, two session bars, and the stacked PR with its 13 merge arrows.
   - s03 shows session 1's first seven commits after a night of planning: 15 sources become 74 fact
     cards. Four walled-off reviewers find 75 problems (97 cards). One card is shown before and after.
   - s04 shows a word-list engine missing one phrasing and tripping on a harmless one, then the new
     shape: the model judges, and the checker on its output guards.
   - s05 shows a token going round push → bots → fix, and 19 commits in about 100 minutes.
   - s06 shows the five-angle review, then six fix branches leaving one after another. Each reproduces
     its bug first, a check flips from ✗ to ✓, and the branches merge back with collisions. One
     usage-limit wall stands alone; a second stands over the queue of six agents.
   - s07 shows the checker's bar growing 459 → 1,326 lines and a rule window that flags a harmless
     phrasing, then misses a risky one. Prober agents fire phrasings at it, then the bots' one-at-a-time
     findings are set against 372 at once, and the 1,060 failures fill a jar that runs with the unit tests.
   - s08 has two receipts: bars for the stated model costs against a $0.50 cap, and token blocks with
     "$ ?" for the agents.
   - s09 sets your recorded calls against the agents' own calls, shows the stop rule's deadline and the
     last push on one Thursday axis, layers with holes stopping three bugs, and the twelve waiting items.
   - s10 marks the six phases on the clock.

   No code on screen. ✔
3. **Ponder moments and recap.** Four pause-and-ponder cards, each with a held pause:
   - s04: "The checker is word rules too. What would make it less of a whack-a-mole?" s07 answers it.
   - s06: "Why reproduce a bug before fixing it?" Answered at once.
   - s07: "The bots would have found these too. Why attack the checker yourself first?" Answered at once.
   - s09: "With no person having reviewed it yet, what makes this code trustworthy?" The layers answer
     it at once.

   s10 recaps the six phases in order and asks three bilingual test-yourself questions, each answered in
   the episode (s07, s06, s09), then holds a 5 s pause. ✔
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

## Whole-video QA (first draft, 7:44; final 8:55)

**Who reviewed.** An independent agent played Conny, working from the bilingual subtitles and one frame every 3 s. I also made two frame-by-frame passes over every scene.

**Gates as first judged.**

- Hook: pass.
- Mechanisms: pass, with gaps.
- Ponder: marginal (two cards in 7:43).
- Recap: **fail**. Question 2 was never answered.

**Fixes.**

- [04:38 / 07:29][MISSING] "Why reproduce a bug before fixing it?" was asked but never answered. FIX:
  - s06 now asks it on a ponder card.
  - The answer comes at once, with a check flipping ✗ → ✓: a reproduction proves the bug is real, and gives a check that has to flip from failing to passing.
- [03:48–04:23][CONFUSING] Wednesday ran out of order: the night's probing came before the afternoon's fix agents. FIX: the scenes are now chronological.
  - Tuesday night's loop ends on the batching agreement of 00:26.
  - Day two (s06) follows.
  - Then the checker's whack-a-mole and the second night's probing (s07).
  - The recap follows the same order.
- [04:38][WRONG] The fix branches looked parallel. FIX: each later agent leaves later and merges later, over a "time →" line. The stagger is labelled illustrative.
- [03:41][WRONG] The batching quote (Wed 00:26) came after Wednesday's examples. FIX: it now closes the Tuesday-night loop: "By half past midnight…".
- [00:22][CONFUSING] "Most of them are fixes" was said but not shown. FIX:
  - The 53 of 88 commits whose message names Bugbot, Codex or a review agent light up on the hook's clock, with the count.
  - Recap question 1 now reads "Why did so many of the brain's commits touch the checker?"
- [04:04][CONFUSING] 372 errors versus 1,060 tests did not add up. FIX:
  - A second ponder card asks why the agents attacked the checker themselves first.
  - The answer: the bots report one finding at a time, while one probing run found 372 at once.
  - The jar shows round 1's 371 + round 2's 689 = 1,060.
- [03:52][MISSING] The two rules were never named, and there was no example pair. FIX: the narration names both rules (no "open now" unless the hours are checked; keep cost out of the way of an emergency). A real pair from the handoff is shown: 「网络外的急诊也是更贵」 must be flagged, 「多休息」 must pass.
- [05:27][MISSING] Cost had no scale. FIX: about 800,000 tokens per fix agent, close to five million for the six, and nothing recorded for the rest.
- [07:01][CONFUSING] The twelve items flashed by, and decision 0006 was unexplained. FIX: a note says what 0006 is and what its addendum covers, and the list holds 4 s longer.
- [03:23–03:45][gate 2] The whack-a-mole was two static lines. FIX: a rule drawn as a window over phrasings (an illustration). Too wide, it flags a harmless one; narrowed, it misses a risky one.
- [00:41][WRONG] Bugbot was narrated first, but Codex's arrow appeared first. FIX: one arrow per bot, each on its own name.
- [04:57][WRONG] Both usage-limit walls sat over the queue. FIX: the first wall stands alone and the second sits over the six queued agents, each on its own words.
- [00:54][CONFUSING] 「无人值守」 was shown before it was explained, and "two teammates asked" was never said. FIX:
  - s02 says handoffs are "marked unattended when nobody was watching" and highlights the title.
  - s05 says the agent "asked two teammates to look".
- [02:03][CONFUSING] "The date decision 0004 uses" was cryptic, and there were few Beijing times. FIX: s03, s04, s05 and s07 now carry Beijing times in their headers.
- [SLOW] These openings had a bare header for 6–9 s, each now fixed:
  - s03: session 1's first seven commits on a strip, after "a night of planning".
  - s04: the rules engine shown from the start.
  - s05: the loop drawn at once.
  - s06: the checker shown first.
  - s07: the checker label shown at once.
  - s08: the cost labels.
  - s09: the "who decided?" card.
- [LAYOUT] These were caught in my frame passes and fixed:
  - the session labels over each other;
  - "13 merges…" over the #41 label;
  - the two whack-a-mole quotes over each other;
  - "pushes" on the PR box;
  - the review label crossing the pentagon;
  - the double arrow through "Thursday";
  - the honesty quote over the stop-rule card;
  - the cap line through "≈ $0.27" (now a dashed budget outline);
  - the spinning loop turning its text sideways (now a token travels the loop);
  - dimmed yellow cards filling solid;
  - the end card over question 3.
- [captions] Three lines were reworded so the line breaks no longer split a phrase:
  - 「一个规则引擎来决定紧急程度」;
  - 「做出了聊天页，也就是第三集讲的那一页」;
  - 「修复先攒起来，再一起推送」.

The ponder count is now four (s04, s06, s07, s09). The recap's three questions are each answered in the episode (s07; s06; s09).

## Verified (final render, 2026-10-30)

- **Files:**
  - `portal-e4-build-log.mp4` (clean, 40.1 MB) and `portal-e4-build-log.zh-en.mp4` (33.4 MB) both decode in full with no error (`ffmpeg -v error -i … -f null -`, exit 0).
  - The `.zh-en.mp4` has the bilingual subtitles burned in, with the picture scaled above the subtitle band.
  - Both run 535.296 s (8:55.3): 1920×1080 at 60 fps, H.264 High, yuv420p; AAC-LC 48 kHz stereo; 32,112 / 32,113 video frames.
  - s02 and s05 were re-rendered after Bugbot's two findings on 2750089 (97890f6), and the cut was restitched from them.
- **Loudness** (EBU R128): −16.1 LUFS integrated, LRA 2.6 LU, true peak −1.0 dBFS.
  - The two files have the same audio (MD5 `4fe6309e…`).
  - The build's mix report: voice −15.98 LUFS, music −32.47 LUFS under speech and −21.98 LUFS in the gaps.
- **Subtitles** (`output/*.srt`, committed):
  - 151 English, 112 Chinese and 136 bilingual cues.
  - All are numbered in order, never overlap and are never empty. None has more than two lines or lasts under 1.0 s.
  - Every bilingual cue has Chinese above English, and the `.zh-en.ass` has the same 136 events.
  - The last cue ends at 8:53.5, 1.8 s before the end.
  - `python -m explainer.i18n check videos/portal-e4-build-log --lang zh`: OK.
- **Layout:**
  - `python -m explainer.check` reports no OUT, SMALL or missing-anchor problem in any of the ten scenes.
  - Four 480p drafts were read frame by frame.
  - Four burned 1080p frames were spot-checked: s01's lit review commits, s07's rule window, s07's jar, and s09's layers with decision 0004.
- **Narration:** 1,329 words (`python -m explainer.script`), Kokoro `af_heart` at 0.95.
- **Sources:** every figure on screen and every quote is listed in SOURCES.md, which also lists the accuracy-pass corrections. Rendered MP4s are not in git; they become release assets after merge.

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
