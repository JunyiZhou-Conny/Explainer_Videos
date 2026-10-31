# Review record: How an agent proves its change is right (项目周记 E5 · agent 怎么证明自己改对了)

Produced 2026-10-31 by a Claude Code cloud session (issue
[#66](https://github.com/JunyiZhou-Conny/Explainer_Videos/issues/66)) on branch
`claude/funny-cannon-6at1kg`, in the 3Blue1Brown style (the house default since 2026-10-30). Verified
facts and unclaimed reviews are kept separate.

## Content gates (AGENTS.md)

1. **Hook.** s01 opens on a broken booking: a referral valid until 2027-01-22, a page left open past it,
   submit, and the tracker says 「已预约专科」 instead of 「已过期」. Then all 245 existing tests pass and the
   code's own comment claims the case is handled. Nobody had noticed. ✔
2. **Intuition before formalism; an animated mechanism per core idea.**
   - s02: state + one action → the reducer → next state; then a test as one chosen path, and the bug's
     path (time passes → book) off to the side.
   - s03: the small world drawn (2 referral cards, 3 slots, a clock with two moments around the expiry);
     13 first moves fan out from the start, layer two grows, states already seen merge, the counter
     climbs to 13,898; then the five rules, one state turning red and its two-step path lighting back to
     the start, with the tool's verbatim output.
   - s04: why it slipped through as a mechanism: the saved referral's `status` feeds the booking step;
     「已过期」 is worked out for the screen and never saved; the page checks when it draws, not on submit.
     Then the known finding and the two ways the check fails.
   - s05: five breakages, each with the rule that caught it and its steps (our re-run), struck when undone.
   - s06: Amazon's 35-step chain drawn dot by dot against our 2-step one.
   - s07: the agent's own app and browser; a cursor clicks each control of the flow; one control found by
     role and accessible name; what counts as right (screen AND saved data); the evidence; a failure that
     names the visible buttons; `down` stopping only its own processes.
   - s08: the origin timeline, the Claude Code quote, what waits, and E4's layers with two more.

   No code on screen beyond the tool's own output and field names. ✔
3. **Ponder moments and recap.** Two pause-and-ponder cards with a held pause:
   - s02: "A test checks the cases someone thought of. What checks the ones nobody thought of?" s03
     answers it.
   - s05: "Why would an agent break its own code on purpose?" Answered at once.

   That is slightly under the aim of one per two minutes for a 6:20 episode; the hook question and the
   three recap questions (each answered: s03, s05, s04) carry the rest. s09 holds a 5 s pause after the
   questions. ✔
4. **Written for the ear; anchored cues.**
   - Numbers are spoken as the voice reads them well ("thirteen possible moves", "thirty-five steps",
     "twenty-seven minutes"); 13,898 and 245 were checked at the phoneme level.
   - Chinese strings (the rules, the tool's output, the app's labels) are shown, never read.
   - Every reveal waits on a word anchor; a script check confirms every anchor occurs in its narration,
     and the lint reports none missing. ✔
5. **Simulated-viewer QA over the full draft.** Findings and fixes below. ✔
6. **Measured checks + human review.** Measured values under *Verified*. Human review: **waived** by
   Conny (AGENTS.md, 2026-10-22): 「我大概率是不会进行审片的，因为我觉得做得已经非常好了，就让bugbot来检查就好了」.
   No human has listened to this cut. ✔ (waiver)

## Research and script review before scenes

- **Research.** An independent agent read PR #42 at `fe19a23` and ran both tools on a temporary copy:
  `npm run verify` (13,898 states, 173,725 transitions, about a second), `npm test` (245/245), the five
  deliberate breakages (each reproduced and reverted), and the referral → specialist flow with
  verify-app (every step `ok:true`, no browser errors, a screenshot of 「已预约专科」). Outside context
  came from primary sources only (Lamport's TLA+ page, the 2015 CACM paper, DeMillo–Lipton–Sayward 1978,
  Stryker's docs, Claude Code's best-practices page).
- **Accuracy read** (a second independent agent, re-running the same commands): 17 findings, all
  applied. They are listed in `SOURCES.md`. The ones that changed the story:
  - the clock's first moment is right after the referrals are written, not an hour before the expiry;
  - only the exhaustive check was broken on purpose; verify-app was checked by running every flow;
  - four rules at every state and one on every step, not five at every state;
  - the page path (left open → submit → booked) is the agent's reading of the code; nobody reproduced
    it in a browser, and the video says so;
  - the breakage stories are our re-run; the PR recorded results, not traces.

## Whole-video QA (first draft, 6:15; final 6:20)

**Who reviewed.** An independent agent played Conny, working from the bilingual subtitles and one frame
every 3 s. I also made two frame-by-frame passes over every scene (one before and one after the fixes).

**Gates as first judged.** Hook: pass. Mechanisms: **partial** (why it slipped through was three text
cards; the breakages a table; the browser a labelled box). Ponder: pass (two, slightly under the aim).
Recap: pass.

**Fixes.**

- [05:22][WRONG] The caption said nobody had tried the app-driving tool. FIX: narration and caption now
  say it has only run in the cloud; the local laptop is untried.
- [05:26][WRONG] "In the last episode, layers stood in for a human review." E4 asked whether they *can*.
  FIX: "The last episode asked whether layers can stand in for a human review. Here are two more."
- [02:24–02:34][MISSING] Why it slipped through was three cards. FIX: the mechanism in s04 described
  above (saved status → booking step; expired only on screen; checked at draw, not on submit), with the
  two fixes and what each guards (every booking vs this page only).
- [01:28–01:41][SLOW] The small world was three chips for 13 s. FIX: drawn as two referral cards, three
  slots and a clock with its two moments either side of the expiry.
- [01:42][CONFUSING] "4 referral choices" with 2 referrals. FIX: named (none · ref-v1 · ref-v2 · a
  missing one).
- [01:09][CONFUSING] "The clock: outside the data" against "time passing is an event". FIX: a "time passes"
  chip labelled "a move of its own: the clock is not app data".
- [05:51][CONFUSING] "Recipe" was never introduced. FIX: "every flow run end to end".
- [04:13–04:33][MISSING] The browser was a grey box with step names. FIX: each step is a control the
  cursor clicks (the wait for 「预约状态：待确认」 is shown as a wait), then one control found by role and
  accessible name.
- [03:38–03:53][SLOW] The paper title sat alone. FIX: the 35-dot chain draws from "In one database
  service", the data-loss end flashes on the words.
- [03:00][CONFUSING] Why delete the note? FIX: "…so the note can never hide the bug if it comes back."
- [04:54][MISSING] "Shuts down only what it started" had no picture. FIX: `down` dims its own server and
  browser and leaves "your own dev server" running.
- [00:21, 04:15][CONFUSING] A footnote about "the checker" before any checker existed, and an
  unexplained "doctor: 8 checks". FIX: the footnote now reads "how the page gets there: the agent's
  reading of the code"; the doctor chip is cut.
- [03:15][CONFUSING] The "not traces" footnote was opaque. FIX: "which rule broke, in how many steps: our
  own re-run (the PR lists only that all five were caught)".
- [captions] 「一共有 13 种可能的操作」 → 「第一步有 13 种可能」; 「带着的就是最短的复现」 → 「给出的就是打破它的最短步骤」;
  「对，意味着两件事同时成立」 → 「做对了，要两件事同时成立」. s07's long sentence is now two ("From a saved demo
  state, the agent starts its own copy… Then it clicks through: …"), in the same order in both languages:
  in the first final cut its Chinese and English halves were one clause apart (Bugbot), so 「打开转诊」 sat
  under "pick a time". I then read every split sentence of the bilingual track pair by pair.
- [06:09][WRONG] The next card said "how the backend was chosen". FIX: "how do you choose a backend?"
- [00:54][LAYOUT] The action entering the reducer was nearly invisible. FIX: it grows and stays below the
  reducer while its chip dims in the row.
- [LAYOUT] Caught in my frame passes and fixed: the opening's empty 3 s (a title now opens it); the
  state tree touching the rule list; text touching the edges of s04's cards; the tracker label left on
  the page while the example button showed; the dashed "never saved" label crossing its arrow; the
  footnotes raised to 22 pt.
- Not changed: 「TLA plus」 in the caption (the caption rules forbid "+").

## Verified

(filled in after the final render)

## Not claimed

- **No human listened** to this cut; the listen is waived (above). Prosody, pacing by ear and music
  balance by ear are unverified.
- **No ASR round trip.** Risky words were checked at the phoneme level instead, and all read as
  intended: TLA+ ("T L A plus"), 13,898, 245, pstack, reducer, Leslie Lamport, ear, nose and throat,
  January twenty-second.
- **Nobody saw the bug in a browser.** The checker proved the booking step; the page path is the agent's
  reading of the code, and verify-app did not try the expired path.
- **The five breakages' rules and steps** are our re-run of equivalent edits, not the PR's record.
- The test path in s02 and the cursor in s07 are illustrations.
- The Chinese captions were checked by the viewer pass for meaning, not by a separate translator.
- PR #42 is an open draft, so the code may move after `fe19a23`. The fix is not chosen.
