# Sources: 项目周记 E5 · How an agent proves its change is right

Everything on screen or in the narration comes from one of the sources below. The portal repository
is private; paths are given so a reader with access can check them. Read 2026-10-31.

## The record (JunyiZhou-Conny/InternationalHealthportal)

- **PR #42**, draft, open: 「验证工具：转诊规则的穷举检查（npm run verify）+ 操作真实 App 的 verify-app skill」
  (renamed at 16:41 from 「形式化检查：转诊 ↔ 专科预约的关联规则（npm run verify）」). Branch
  `claude/lucid-cannon-44cg7u`, read at `fe19a23`; base `main` at `c05cd2e`; +1,389 / −1 across 18 files. No issue.
- **Commits** (Boston time, EDT; Beijing is 12 hours ahead), Fri 2026-10-30:
  - `c0920b0`, 16:13:42: the exhaustive check;
  - `fe19a23`, 16:40:41: verify-app.
- **Files** (paths on the branch):
  - the exhaustive check: `verify/model.ts`, `verify/referral-links.verify.ts`, `verify/verify.ts`, `vitest.verify.config.ts`, and the skill `.claude/skills/verify-referral-links/SKILL.md`;
  - the app driver: `.claude/skills/verify-app/` (`SKILL.md`, `control-app.mjs`, `features/README.md`, `features/referral-specialist.md`);
  - the product code read for the bug: `src/state/reducer.ts`, `src/state/selectors.ts`, `src/types.ts`, `src/pages/BookingPage.tsx`, `src/state/AppProvider.tsx`.

**Our own runs.** We ran `npm run verify`, `npm test` and the five deliberate breakages on a temporary
copy of `fe19a23` (Node 22, Vitest 5.0.5). We also drove the referral flow once with verify-app.
Every edit was reverted, and nothing was pushed to the portal repository. An independent
accuracy pass over the script did the same runs again and corrected the points marked ✱.

| Claim in the video | Source |
| --- | --- |
| The referral: ENT, 「有效期至」 2027-01-22 (fictional demo data); valid 90 days from T0 = 2026-10-24 15:00Z | `model.ts`:15 (T0); `buildVisitOutcome` (`visitOutcome.ts`:121), `content.ts`:268 (90 days) |
| The page path (left open past the expiry → submit → the expired referral attached → the tracker shows 「已预约专科」) is the agent's reading of the code; the checker proved the booking step, and nobody reproduced it in a browser ✱ | PR body; verify-referral-links `SKILL.md`:63; `BookingPage.tsx`:166–177 (check at render), :298, :403–409 (submit sends `attachReferral?.id`); badge 「已预约专科」 `StatusBadges.tsx`:201, `TrackerPage.tsx`:379 |
| The parent opens the booking page ✱ | verify-app `SKILL.md`:9 (the app is for parents); `reducer.ts`:302 logs the booking as the parent's action |
| 245 existing tests, all passed; none books after the expiry ✱ | `npm test`: 245/245 across 14 files (re-run). Expiry display (`reducer.test.ts`:145) and one-referral-one-appointment (:123–137) are tested separately |
| The code comment claims expired referrals are left alone: 「过期…的转诊保持不变」 (abridged) | `reducer.ts`:288 |
| Reported Friday 16:13 by an agent, PR #42 ✱ | commit `c0920b0` 16:13:42 (when the work was committed; when the bug was first seen is not recorded); PR opened as a draft 16:14:02 |
| The reducer: every change to app data goes through one function, one action at a time; the checker calls the real one, not a copy | `reducer.ts`:217; `model.ts`:10; verify-referral-links `SKILL.md`:17 |
| Actions: book · confirm · reschedule · cancel · complete | `model.ts`:72–95 |
| The page checks the referral when it draws; the booking reaches the reducer later | `AppProvider.tsx`:147–181 (`bookAppointment` awaits the mock adapter, then dispatches); `model.ts`:4–5 |
| The clock is outside the app's data; time passing is a move of its own ✱ | `model.ts`:31–32, :98 (the clock is a flag in the model; a tick does not go through the reducer) |
| The small world: 2 referrals (`ref-v1`, `ref-v2`), 3 slots (S1–S3), a clock with two moments: right after the referrals are written (T0 + 1 h) and an hour after they expire ✱ | `model.ts`:7–8, 15–20, 49–70; moments at :66–69 print as 2026-10-24T16:00Z and 2027-01-22T16:00Z. The comment at :65 is misleading on this point |
| 13 first moves: 1 clock tick + 3 slots × 4 referral choices (none, `ref-v1`, `ref-v2`, `ref-missing`) | `model.ts`:72–95; counted from the start state |
| Breadth-first, merging states already seen; the first violation of each rule is the shortest | `model.ts`:175–201 (FIFO queue), :105–109 (`key()`), :183 (first violation kept) |
| 13,898 states, 173,725 transitions, about a second ✱ | our runs: `explore()` 0.68–1.01 s over 8 runs; the whole `npm run verify` about 1.4–2.0 s. The PR: 「约 1.4 万个状态、17 万次转移，用时约 1 秒」 (verify-referral-links `SKILL.md`:25) |
| Four rules at every state and one on every step, verbatim: 「一张转诊最多一个有效预约」 · 「有效预约上的转诊指回这个预约」 · 「已预约的转诊有一个有效预约」 · 「已用完的转诊来自一次完成的专科就诊」 · 「过期的转诊不会关联到新预约」 ✱ | `model.ts`:114–145 (state rules), :148–160 and :193 (the step rule); verify-referral-links `SKILL.md`:30–39 |
| The output, verbatim: 「✗ 过期的转诊不会关联到新预约：ref-v1 在 2027-01-22T16:00:00.000Z 被关联到 S1，但它的有效期到 2027-01-22T15:00:00.000Z / 最短复现：1. 时间过去，转诊过了有效期（validUntil） 2. appointment/book S1 referralId=ref-v1」 | `npm run verify` at `fe19a23` |
| Why it slipped through: booking reads only the stored status, never `validUntil`; the status value `expired` is never stored, only computed for display (「已过期」 is its label); the page checks when it draws, not on submit ✱ | `reducer.ts`:286–294 (`free` at :291); `types.ts`:566 (`'expired'` in the type); `selectors.ts`:104–140 (`lapsed` at :110), :148; `BookingPage.tsx` as above |
| The agent did not change product code; the fix is left to a person: compare the expiry inside the reducer, or check again on submit | PR diff (no `src/` changes); verify-referral-links `SKILL.md`:65 |
| 「已知发现（未修）」; the rule was not loosened; the check fails on any other violation and also when the known one disappears: 「修好后把它从 KNOWN_FINDINGS 删掉」 | `referral-links.verify.ts`:4–14; `verify.ts`:16 (a known finding matches rule plus exact trace), :31–34; verify-referral-links `SKILL.md`:65, :77 |
| "A check that you have never seen fail proves nothing" | pstack, `create-formal-verification-skill/SKILL.md`:26 |
| Five deliberate breakages, all caught within two steps, then undone: 预约时不要求原预约已取消 · 转诊不能用时保留 referralId · 取消时不退回 issued · 取消时改成 completed · 改期时丢掉 referralId | PR body (「故意改坏 reducer 5 次，检查都抓到了，并给出两步以内的最短反例」); verify-referral-links `SKILL.md`:108–113 lists the first four |
| The rule and story on each breakage card are **our re-run** (the PR recorded results, not traces) ✱: 1 → rules 1 and 2, `book S1 ref-v1` → `book S2 ref-v1`; 2 → rule 2 in one step, `book S1 referralId=ref-missing`; 3 → rule 3, `book S1 ref-v1` → `cancel S1`; 4 → rule 4, `book S1 ref-v1` → `cancel S1`; 5 → rule 3, `book S1 ref-v1` → `reschedule S1` | our edits to `reducer.ts`, equivalent to the PR's wording, each reverted; confirmed independently by the accuracy pass |
| "a hand-made version of what testers call mutation testing; the classic paper is from 1978" ✱ | R. A. DeMillo, R. J. Lipton, F. G. Sayward, "Hints on Test Data Selection: Help for the Practicing Programmer", *IEEE Computer* 11(4):34–41, April 1978, doi:10.1109/C-M.1978.218136; Stryker's definition, <https://stryker-mutator.io/docs/> |
| Amazon, 2015: "How Amazon Web Services Uses Formal Methods", *Communications of the ACM*; TLA+; a DynamoDB data-loss bug whose shortest trace was 35 high-level steps; "passed unnoticed through extensive design reviews, code reviews, and testing" | C. Newcombe et al., *CACM* 58(4):66–73, April 2015; excerpt at <https://lamport.azurewebsites.net/tla/amazon-excerpt.html> |
| TLA+, created by Leslie Lamport | <https://lamport.azurewebsites.net/tla/tla.html> ("the creator of TLA+") |
| verify-app starts its own server and browser from a saved demo state, on a free port with its own profile; `doctor` runs 8 checks ✱ | verify-app `SKILL.md`:31–65; `control-app.mjs`:263–345, :279, :294; `referral-specialist.md`:22 (`seed after-visit`) |
| The flow: open the referral → in-network clinic → pick a time → 「提交模拟预约申请」 → 「预约状态：待确认」 → open the tracker | `features/referral-specialist.md`:24–31 |
| Controls found by role and accessible name, the label a screen reader announces; the heading shows 「转诊 ≠ 事先授权」, its accessible name reads 「转诊 不等于 事先授权」 ✱ | `control-app.mjs`:174 (`getByRole(role, {name})`, visible elements only); verify-app `SKILL.md`:69, :84–86; `referralParts.tsx`:327–329 (screen-reader-only text); commit `fe19a23` message |
| Waits for quiet after each step: no 「查询中…」, no `aria-busy`, 400 ms without change | verify-app `SKILL.md`:92; `control-app.mjs`:113–126 |
| What counts as right: the tracker shows 「已预约专科」 **and** the saved state shows `ref-demo` `scheduled`, pointing to the new specialist appointment | `features/referral-specialist.md`:24–31; our run: `ref-demo` → `apt-mvvo1vn14`, `scheduled`, kind `specialist`, every step `ok:true`, `browserErrors: []` |
| Evidence the agent is required to keep: screenshot, saved state, no browser errors, no sideways scroll at 390 px, 「模拟」 labels and both time zones ✱ | verify-app `SKILL.md`:106–113 (the skill's standard for the agent; `browserErrors` comes back in each step's JSON) |
| A failure names what it could see: 「没有找到可见的 button「预约」」 / 「可见的 button 有：最新在前 \| 最早在前 \| 转诊 \| …」 | `control-app.mjs` error and hint format; our run |
| `down` stops only the processes it recorded and keeps the evidence | verify-app `SKILL.md`:122–124; `control-app.mjs`:377–390 (process groups from `run.json`, never by name); our run: 0 leftover processes |
| Both tools came from trying two pstack skills, 「create-formal-verification-skill」 and 「create-verification-skill」, in a conversation; no issue. pstack is a public, MIT-licensed plugin of agent skills | PR body (「在对话里试用 pstack 的 `create-formal-verification-skill` 和 `create-verification-skill` 时」); <https://github.com/cursor/plugins/tree/main/pstack> (plugin.json v0.15.36) |
| Two commits, 27 minutes apart; Bugbot ran twice and found nothing; no other comments or reviews | git log; check runs (16:19; 16:40:51–16:47:13 "no issues found"); 0 issue comments, 0 review comments, 0 reviews |
| "If it has nothing to run that tells it whether the work actually is done, 'looks done' is all it has to go on. In practice that makes you the test suite." ✱ | Claude Code best practices, <https://code.claude.com/docs/en/best-practices>, section "Give Claude a check to run" (undated; fetched 2026-10-31) |
| What waits: the fix choice; verify-app only run in the cloud container, the local install (`npx playwright install chromium`) untested ✱; the PR is a draft | verify-referral-links `SKILL.md`:65; PR body (「只在云端容器里验证过」); PR state |
| The first tool was checked by breaking it on purpose; the second by running every recipe end to end ✱ | PR body: 65 consecutive desktop steps exited 0, each feature also at phone size, a parallel `--run b` did not interfere; a duplicate `up` refused (「run=main 已经在运行」); `fe19a23` message |
| E4's layers, with two more added | E4 (`videos/portal-e4-build-log`), the episode's own synthesis |

## Corrections from the accuracy pass

These were wrong or imprecise in the first draft of the script and are fixed in the video:

- the clock's first moment was "an hour before the expiry"; it is an hour after the referrals are written;
- "both tools were checked by breaking things on purpose" (only the exhaustive check was);
- "five rules at every state" (four state rules and one step rule);
- "in under a second" (about a second);
- "the way a screen reader does … names a button" (role and accessible name, and the targets include links and regions);
- the tracker label 「已预约」 (the badge reads 「已预约专科」);
- "a student opens the booking page" (the parent does);
- "found Friday 16:13" (reported then; the commit time) and "all 245 tests" (existing tests; none books after the expiry);
- "which nobody has done yet" (the local install hasn't been tried);
- the clock drawn inside the app's data (it is outside it);
- the breakage stories now say they are our re-run;
- the Claude Code quote is now the full sentence from the page's body.
