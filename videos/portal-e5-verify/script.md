# 项目周记 E5 · How an agent proves its change is right — script & visual plan

Series: *项目周记* (`docs/PORTAL_SERIES.md`). Watch after E4. Brief: `BRIEF.md`; every claim's source:
`SOURCES.md`.

Audience: Conny, after E1–E4. Goal: he can explain exhaustive checking as "every order, in a small
world, with rules checked in every state", retell the expired-referral bug and why tests missed it,
say why the agent broke its own code on purpose, describe driving the real app with evidence, and
say what waits for a person.

**Narrated.** SAY lines are spoken (Kokoro `af_heart`, 0.95×, over a quiet music bed) and shown as
subtitles (Chinese above, English below). Times are Boston time.

Colours: app state BLUE · actions ORANGE · rules YELLOW · a broken rule RED · passed GREEN · the real
browser WHITE outlines.

---

## S01 · A bug nobody had seen — `s01_hook.py` · `Hook`

SHOW: A referral card: ENT, 「有效期至」 2027-01-22 (fictional demo data). A booking page left open; a clock passes the expiry; the parent presses 「提交模拟预约申请」; the expired referral is attached anyway, and the tracker says 「已预约专科」, not 「已过期」. A small caption: "the page path: the agent's reading of the code; the checker proved the booking step".
SAY: Here is a bug in our prototype. A student has a referral to an ear, nose and throat specialist, valid until January twenty-second. Their parent opens the booking page, leaves it open past that moment, and presses submit. By the agent's reading of the code, the expired referral is attached anyway, and the tracker shows the specialist as booked, never expired.

SHOW: Beside it: "245 existing tests: all passed · none books after the expiry", and the code comment that claims the case is handled, 「过期…的转诊保持不变」, struck through in RED. Then: "reported Friday 16:13 by an agent · PR #42".
SAY: All 245 existing tests passed; none of them books after the expiry. The code even carries a comment saying expired referrals are left alone. No person had noticed. On Friday afternoon an agent reported it, after trying every order of a few actions in a small world. This episode is about how an agent can prove a change is right before anyone looks.

---

## S02 · One function, many orders — `s02_reducer.py` · `Reducer`

SHOW: The app's data as a box (appointments, referrals), with the clock drawn outside it. An action arrives (book · confirm · reschedule · cancel · complete); a single function, the reducer, turns old state + action into new state. A strip of actions in one order, then the same actions shuffled.
SAY: Every change to the app's data goes through one function, called the reducer. It takes the current state and a single action, such as book, confirm, reschedule, cancel or complete, and returns the next state. The booking page checks the referral when it draws, but the booking reaches the reducer later. So the order of events matters, and time passing is an event too.

SHOW: A test as one hand-picked path through the actions; the bug's path (time passes → book) off to the side, untested.
SAY: A test follows a path someone chose. The bug lives on a path nobody chose: first time passes, then the booking goes through.

SHOW: Pause-and-ponder card.
SAY: A test checks the cases someone thought of. What checks the ones nobody thought of?

---

## S03 · Try every order in a small world — `s03_explore.py` · `Explore`

SHOW: The small world: 2 referrals (ref-v1, ref-v2), 3 specialist slots (S1–S3), a clock with two moments: right after the referrals are written, and an hour after they expire. From the start state, 13 possible first moves fan out (1 clock tick + 3 slots × 4 referral choices); each new state spawns its own moves, layer by layer (breadth-first); states already seen merge instead of repeating. A counter climbs to 13,898 states and 173,725 transitions, in about a second.
SAY: Build a small world instead: two referrals, three specialist slots, and a clock with just two moments, right after the referrals are written and an hour after they expire. From the starting state there are thirteen possible moves. Make each one, then every move from each result, layer by layer, merging any state you've already seen. In this world that is 13,898 states, reached in about a second, and every one of them comes from the real reducer, not a copy.

SHOW: Five YELLOW rules: four checked at every state, the last on every step: 「一张转诊最多一个有效预约」 · 「有效预约上的转诊指回这个预约」 · 「已预约的转诊有一个有效预约」 · 「已用完的转诊来自一次完成的专科就诊」 · 「过期的转诊不会关联到新预约」. One state turns RED; its path back to the start lights up, two steps long. The tool's own output: 「最短复现：1. 时间过去，转诊过了有效期（validUntil） 2. appointment/book S1 referralId=ref-v1」.
SAY: Four rules are checked at every state and a fifth on every step, all written in plain language, such as one referral backs at most one live appointment, and an expired referral is never newly attached. Because the search goes layer by layer, the first broken rule it meets comes with the shortest story that breaks it. Here, two steps: time passes, then book with that referral.

---

## S04 · Why it slipped through, and what the agent did not do — `s04_finding.py` · `Finding`

SHOW: Three cards: the booking step checks only the referral's stored status · 「已过期」 is never stored, only computed for display · the page checks when it draws, not when it submits. Then a note pinned to the checker: 「已知发现（未修）」 with the two-step story.
SAY: Why did it slip through? Booking looks only at the referral's stored status. Expired is never stored; it is only worked out for the screen. And the page checks when it draws, not when you submit. The agent did not change the product code. It recorded the bug as a known finding and left the fix to a person: compare the expiry date inside the reducer, or check again on submit.

SHOW: The check's two failure modes: any new broken rule → fail; the known finding disappears (because someone fixed it) → also fail, with 「修好后把它从 KNOWN_FINDINGS 删掉」.
SAY: The rule was not loosened to make the check pass. And the check is built to fail in two ways: if any new rule breaks, and if this known bug ever disappears. That second failure reminds whoever fixes it to delete the note, so the note can never hide the bug if it comes back.

---

## S05 · Breaking it on purpose — `s05_mutants.py` · `Mutants`

SHOW: Pause-and-ponder card.
SAY: Why would an agent break its own code on purpose?

SHOW: The quote "A check that you have never seen fail proves nothing" (the pstack skill). Five deliberate breakages of the reducer as cards: 预约时不要求原预约已取消 · 转诊不能用时保留 referralId · 取消时不退回 issued · 取消时改成 completed · 改期时丢掉 referralId. Each card gets a RED rule and a short story (one or two steps; our re-run: the PR recorded results, not traces), then is crossed out: caught. A footnote: "mutation testing, DeMillo, Lipton & Sayward, 1978".
SAY: Because a check you have never seen fail proves nothing. Maybe it can't fail at all. So the agent broke the reducer five times on purpose, in five different ways, and ran the check after each. All five were caught, each with a story of two steps or fewer, and each breakage was then undone. It is a hand-made version of what testers call mutation testing; the classic paper on it is from 1978.

---

## S06 · The same idea, at Amazon's scale — `s06_amazon.py` · `Amazon`

SHOW: A timeline card: 2015, "How Amazon Web Services Uses Formal Methods" (Communications of the ACM). A long chain of 35 steps ending RED in a data-loss state; the note "passed unnoticed through extensive design reviews, code reviews, and testing". Beside it, our chain of 2 steps.
SAY: The idea is old and serious. In 2015 Amazon described checking its designs this way, using TLA+, a language created by Leslie Lamport. In one database service it found a data-loss bug whose shortest story was thirty-five steps long, a bug that had passed design reviews, code reviews and testing. Ours is tiny by comparison, two steps in a one-second check, but it is the same move: let a machine walk every order a person would never try.

---

## S07 · Driving the real app — `s07_drive.py` · `Drive`

SHOW: The second tool: an agent at a real browser on the running page. Steps as a strip: start its own server and browser from a saved demo state → health check → open the referral → read 「转诊 不等于 事先授权」 → choose an in-network clinic → pick a time → 「提交模拟预约申请」 → wait for 「预约状态：待确认」 → open the tracker. Each step names a control by its role and accessible name (the heading shows 「转诊 ≠ 事先授权」; its accessible name reads 「转诊 不等于 事先授权」); after each step it waits for the page to go quiet.
SAY: The second tool drives the app itself, the way a parent would. From a saved demo state, the agent starts its own copy of the app and its own browser. Then it clicks through: open the referral, choose an in-network clinic, pick a time, submit, wait for pending, open the tracker. It finds each control by its role and accessible name, the label a screen reader announces, and waits for the page to settle after each step.

SHOW: "What counts as right": the tracker shows 「已预约专科」 AND the saved state shows the referral scheduled, pointing to the new appointment. Evidence: screenshot · saved state · no browser errors · no sideways scroll at phone width · 「模拟」 labels and both time zones present. A failure example: 「没有找到可见的 button「预约」」 with the hint listing the visible buttons. `down` stops only its own processes and keeps the evidence.
SAY: Right means two things at once: the screen says the specialist is booked, and the saved data says the referral now points to that new appointment. Each run is required to keep evidence: screenshots, the saved state, and no browser errors. When a step fails, it says which buttons it could see instead. And when it's done, it shuts down only what it started.

---

## S08 · Where it came from, and what waits — `s08_waits.py` · `Waits`

SHOW: Origin: two skills from pstack, a public plugin of agent skills, 「create-formal-verification-skill」 and 「create-verification-skill」, tried in a conversation; no issue. Timeline Fri 16:13 → 16:40, two commits; Bugbot twice, nothing found. The Claude Code best-practices line: "If it has nothing to run that tells it whether the work actually is done, 'looks done' is all it has to go on. In practice that makes you the test suite."
SAY: Both tools came from trying two skills in a public plugin called pstack, on Friday afternoon, in two commits twenty-seven minutes apart. Anthropic's own advice for Claude Code says the same thing plainly: give the agent a check to run, or you become the test suite.

SHOW: What waits for a person (YELLOW): 1 · the expired-referral fix, in the reducer or on submit · 2 · verify-app was only run in the cloud container; the first local install is untested · 3 · the pull request is a draft. Then E4's layers again, with two more added: every order, and the real app.
SAY: What waits for you: choosing the fix for the expired referral, and trying the app-driving tool on your own laptop; so far it has only run in the cloud. And the pull request is still a draft. The last episode asked whether layers can stand in for a human review. Here are two more: a check that tries every order, and an agent that uses the real app.

---

## S09 · Recap — `s09_recap.py` · `Recap`

SHOW: The two tools side by side: every order in a small world → the shortest story; the real app, by role and name → evidence.
SAY: So: one tool walks every order of actions in a small world and hands back the shortest story that breaks a rule. The other uses the real app like a parent and keeps the evidence. The first was checked by breaking it on purpose; the second, by running every flow end to end.

SHOW: Three test-yourself questions, then a held pause.
SAY: Three questions. What does the exhaustive check try that an ordinary test doesn't? Why break your own code on purpose? And why does the check fail when the bug gets fixed?

SHOW: Next card: E6 「后端怎么选」, "how do you choose a backend?".
SAY: Next: before any backend code is written, how do you choose the backend?
