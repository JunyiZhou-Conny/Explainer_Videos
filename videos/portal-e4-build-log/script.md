# 项目周记 E4 · Two days, a hundred-plus commits — script & visual plan

Series: *项目周记* (`docs/PORTAL_SERIES.md`). Watch after E3. Brief: `BRIEF.md`; every claim's source:
`SOURCES.md`.

Audience: Conny, after E1–E3. Goal: he can retell the two days as a few phases on one clock, explain
why most commits fixed the checker and how probing changed that, name how the work is organised,
say which calls were his and which the agents made alone, state what it cost from the figures on
record, and list what waits for him.

**Narrated.** SAY lines are spoken (Kokoro `af_heart`, 0.95×, over a quiet music bed) and shown as
subtitles (Chinese above, English below). Times are Boston time unless the line says Beijing.

Colours: PR #36 (the triage brain) ORANGE ticks · PR #41 (the chat page) BLUE ticks · merges GREY ·
review bots GREY outlines · the owner's decisions YELLOW · agents' unattended choices WHITE with a
「提议」 tag · problems RED · fixed GREEN.

---

## S01 · Two days on one clock — `s01_hook.py` · `Hook`

SHOW: One Boston-time axis from Tuesday noon to Thursday 01:00. All 88 own commits rise as ticks (PR #36 ORANGE above the line, PR #41 BLUE below), then the 21 merges in GREY. Counters: 88 changes · 21 merges · 109 in all, every one made by an agent (40 show the owner as author: the agent used his git identity).
SAY: This is every commit on our two triage pull requests, on one clock: Boston time, from Tuesday noon to early Thursday. 109 commits, every one made by an agent: 88 changes, and 21 merges of one branch into another. GitHub shows forty of them under your name, because the agent used your git identity.

SHOW: Two question cards: "why are most of them fixes?" (the 53 of 88 commits whose messages cite Bugbot, Codex or a review light up) · "who decided?". Under the second: "reviews by a person so far: 0 · two teammates asked, Tue 22:23".
SAY: Two questions. Why are most of them fixes? 53 of the 88 name a review in their message: Bugbot, Codex, or a review agent. And no person has reviewed them yet, so who decided anything?

---

## S02 · How the work is organised — `s02_machinery.py` · `Machinery`

SHOW: A flow: issue → branch → draft pull request → pushes wake two bots (Bugbot on every push · Codex once the PR is ready for review; GREY outlines, "comment only") → fixes → push. Quote AGENTS.md 「review bot（Cursor Bugbot、Codex 等）只提意见，不直接改代码。」
SAY: First, the machinery. Each job starts as an issue, gets its own branch, and opens a draft pull request after the first commit. Pushes wake two review bots from different companies: Cursor's Bugbot on every push, and OpenAI's Codex once the pull request is marked ready for review. They may comment, but never change code.

SHOW: A handoff note card (its headings: 做了什么 · 没做完的 · 下一步（等 Junyi 定） · 踩过的坑); a decision record moving 「提议」 → 「已采纳」 with a hand icon: "only a person". The rule 「聊天是临时的，仓库是永久的」.
SAY: When an agent stops, it writes a handoff note on the pull request, marked unattended when nobody was watching. Big choices become decision records, marked proposed until a person marks them adopted. The team's rule: chat is temporary, the repository is permanent.

SHOW: Two session bars on the clock, from each session's first to last commit: session 1, Tue 12:22 → Wed 00:07; session 2, Wed 01:51 → Thu 00:45. The chat page's branch stacked on the brain's, with 13 GREY merge arrows from #36 into #41.
SAY: Two agent sessions made the commits: the first until just after midnight, the second from one fifty-one on Wednesday morning to a quarter to one on Thursday. The chat page was stacked on top of the triage brain, and pulled in the brain's changes 13 times.

---

## S03 · Day one: a skeleton, then a fact check — `s03_dayone.py` · `DayOne`

SHOW: Tue 12:22–13:03 on the clock, after a night of planning (research, two designs, reviews): 15 sources → 74 fact cards · a rules engine (word lists) · 11 test cases · an evaluation.
SAY: Tuesday, at twelve twenty-two, after a night of planning, the first session started committing. Within forty minutes it had a skeleton: fact cards from 15 sources, a rules engine that decided urgency, eleven test cases and an evaluation.

SHOW: Four reviewer agents in separate boxes, no lines between them: 「4 个互不通信的 agent…只读文件，不改文件」. Counter: 75 problems → 97 cards, 7 conflicts, 23 minutes after the first 74 cards. One card before and after: out-of-network urgent care 「保险付 80%，自付 20%」 → 「先付网络外 deductible（$500），再自付 20%，可能另收差额」.
SAY: Then it checked its own facts. Four reviewer agents that could not talk to each other read every card against its source and reported 75 problems. Twenty-three minutes after the first 74 cards, there were 97. One had said out-of-network urgent care costs you 20 percent; the source said you pay a five-hundred-dollar deductible first.

---

## S04 · The turn at 9:21 — `s04_turn.py` · `Turn`

SHOW: The clock at Tue 21:21 Boston, the commit 8f13b18, with "Wed 09:21 Beijing" under it (the date decision 0004 uses; when the call itself was made is not recorded). A word-list engine: some symptoms slip through (RED misses), some harmless words trip it (RED false alarms), a patch here breaks something there. Quote 0004: 「词表（keyword spotting）同时有漏判和误报，越补越多，补一处又会坏另一处。」
SAY: At nine twenty-one that evening, Boston time, Wednesday morning in Beijing, a commit changed the plan. The rules engine matched words, and word lists both missed things and flagged the wrong things; every patch broke something else.

SHOW: The new shape: the model judges urgency and the destination; the checker on its output is the only safety layer. Quote 0004, written by the agent: 「Junyi 2026-10-28 决定：先做能演示的 MVP，评估以后再做。紧急程度和去处交给推理模型判断，不再由确定性规则或正则词表决定。」 The rules engine and the experiments greyed: 「留在仓库里，不再推进」.
SAY: The record says you decided: a demo first, evaluation later; the model judges urgency and where to go, and the checker on its output becomes the only safety layer. The rules engine and the comparison experiments stay in the repository, no longer pursued.

SHOW: Pause-and-ponder card.
SAY: But notice: the checker is also made of word rules, applied to sentences instead of symptoms. What would make it less of a whack-a-mole?

---

## S05 · The loop with the bots — `s05_loop.py` · `Loop`

SHOW: Tue 22:23 Boston (Wed 10:23 Beijing): PR #36 marked ready for review, two teammates asked. A loop diagram: push → bots review → agent fixes → push, a token going round. The clock zooms into Tue 22:27 → Wed 00:07: 19 ORANGE ticks. Counters for PR #36: bot comments 72 (Bugbot 42 · Codex 30), fixed 64.
SAY: Then came the loop. At ten twenty-three that night, Boston time, the agent marked the brain's pull request ready for review and asked two teammates to look, and both bots began reviewing every push. Push, the bots review, the agent fixes, push again. Between ten twenty-seven and just after midnight the first session pushed 19 commits, about one every five minutes. On that pull request the bots wrote 72 comments, and 64 led to fixes.

SHOW: Quote from the handoff: 「已和 Junyi 商定：以后把修复攒在一起再推。」 (Wed 00:26)
SAY: By half past midnight, you and the agent had agreed on one change: batch the fixes before pushing.

---

## S06 · Day two: a queue of fix agents — `s06_daytwo.py` · `DayTwo`

SHOW: Wed on the clock: 01:59 the chat page (E3) · the brain's fixes beside it · 15:37 a final review from five angles (安全和状态 · 流式后端 · 排版和无障碍 · 文案和文档 · 测试和检查规则), about 30 problems.
SAY: On Wednesday the second session built the chat page from episode three and kept fixing the brain beside it. In the afternoon a final review looked from five angles at once and found about 30 problems.

SHOW: Six fix branches (fix41/labels · state · layout · tests · fix36/parent-911 · cost-shs) leaving one after another (fix commits 16:52 → 19:07, order illustrative), each with "reproduced" ✓ before its fix.
SAY: Six fix agents took them one after another, each on its own branch, and each first reproduced its bug before fixing it.

SHOW: Pause-and-ponder card.
SAY: Why reproduce a bug before fixing it?

SHOW: One check flipping: ✗ fails before the fix → ✓ passes after (an illustration). The branches merge back 18:24 → 19:11. A collision: a branch adds a field, another branch's new test rejects it, 4 failures, fixed at 19:04. Then a second review of the merged result: 8 more fixes (fix41/review3, merged 19:16).
SAY: Because a reproduction proves the bug is real, and gives a check that has to flip from failing to passing; a fix for a bug nobody saw fail proves nothing. Merging the branches back took about an hour and had collisions; in one, a branch added a field that another branch's new test rejected. A second review of the merged result found eight more.

SHOW: Session 2 (times not recorded): a first RED wall "5-hour usage limit" on its own, a second over the queue of six fix agents, "≈ 800,000 tokens each"; two container restarts (local commits survive, a running test is cut off); the new rule "at most 3 per round".
SAY: Along the way the session hit its five-hour usage limit twice, the second time because the six fix agents ran in a row at about 800,000 tokens each, and the container restarted twice. The agents' rule afterwards: at most three at a time.

---

## S07 · Attack your own checker — `s07_probing.py` · `Probing`

SHOW: The checker's size as a bar, from the turn: 459 → 1,326 lines; "27 of the 45 commits since touched it". A whack-a-mole, both on Wednesday: 11:04, 「不要因为保险或费用问题延误救援」 flagged as money-first in a real run (RED false alarm, an extra rewrite; 6f9394e); 19:07, a similar rule narrowed (26a2d89); 「Use my insurance first」 slips through (RED miss), Bugbot flags it, restored 19:23 (2662221). Under it, an illustrated rule window over a line of phrasings: too wide catches a harmless one, narrowed it misses a risky one.
SAY: Back to the checker. Most of the bots' comments were about it. After the turn it grew from 459 lines to 1,326, and 27 of the 45 commits since touched it. Each fix moved the problem. On Wednesday a parent summary saying don't delay help because of insurance was flagged as putting money first, which cost a needless rewrite; that evening, narrowing a similar rule let a real money-first line slip through, until Bugbot caught it.

SHOW: Wed 21:04 → Thu 00:45 Boston (Thu 09:04 → 12:45 Beijing). The two rules: never claim a clinic is open right now unless its hours are checked · keep cost out of the way of an emergency. A pair: must be flagged 「网络外的急诊也是更贵」 · must pass 「多休息」 (once a false alarm). Round 1: four prober agents and a fifth that checks them (round 2: three angles), writing phrasings: round 1 ≈ 2,000 (opening hours ≈ 1,400, emergency cost ≈ 640), round 2 ≈ 1,000; total ≈ 3,000. Round 1's result: 142 misses, 230 false alarms.
SAY: So on the second night the agents stopped waiting for the bots. Two rules took the beating: never claim a clinic is open right now unless its hours are checked, and keep cost out of the way of an emergency. Before pushing, the agents attacked those two rules: they wrote about 3,000 ways to say a risky thing, or its harmless twin, and ran them all. The first round found 142 misses and 230 false alarms.

SHOW: Pause-and-ponder card.
SAY: The bots would have found these too. Why attack the checker yourself first?

SHOW: The bots' way: one finding per review, one push per round; the probes: 372 at once. The phrasings the checker got wrong fall into a jar labelled `lint.probes.json`: round 1, 371 · round 2, 689 → 1,060 (506 must be flagged · 554 must pass), fixed and run with the unit tests (`npm test`); about 20 harder ones listed as known misses. In round 2, a first fix that produced 20 new false alarms, caught before the push.
SAY: Because the bots report one finding at a time, and every fix waits for the next review. One probing run found 372 at once. Across both rounds, 1,060 phrasings it got wrong were fixed and kept as tests that run with the unit tests; about twenty harder ones are listed as known misses. In the second round, the first fix even created 20 new false alarms; this time they were caught before the push, not after.

---

## S08 · What it cost — `s08_cost.py` · `Cost`

SHOW: A receipt of the stated figures: one real model call $0.036 · the first day's model runs ≈ $0.77 · the last night ≈ $0.27 (cap $0.50); caps on the record: $2 per server start, $10 for an evaluation. A second, empty receipt for the agents: "≈ 800,000 tokens per fix agent · no dollar figure on record".
SAY: What did it cost? The model calls the product made are on the record: about 4 cents for one real answer, about 77 cents for the whole first day, 27 cents on the last night against a 50-cent cap. The agents' own work is priced nowhere in the repository; the only number is tokens: about 800,000 per fix agent, close to five million for the six, and none recorded for the rest.

---

## S09 · Who decided, and what waits — `s09_decided.py` · `Decided`

SHOW: YELLOW cards, some of the owner's calls as the agents recorded them: the model and its effort (Tue) · the turn at 21:21 · batch the fixes · copy Claude's page one to one (#40) · the stop rule 「做到 99% 就停……最晚周四晚上 7 点（按北京时间算）收尾」. The clock: deadline Thu 19:00 Beijing = Thu 07:00 Boston; the last push Thu 00:45 Boston, 6 h 15 min early.
SAY: So who decided? The record, written by the agents, names your calls, among them the model and its effort, the turn to the model's judgement, batching the fixes, copying Claude's page, and the stop rule: stop at 99 percent, finish by Thursday at seven in the evening, Beijing time. The code kept it: the last push came more than six hours early, and four later bot findings were written down for the next person.

SHOW: Some of the agents' own choices as WHITE cards tagged 「提议」 and 「无人值守，未经人确认」, one of them "mark PR #36 ready for review" against the workflow's 「两次点击都由人来做」. A handoff line: 「agent 早先说「Bugbot 意见都修了」，实际有 2 条没修」.
SAY: Many smaller choices the agents made alone, and wrote down as proposals, marked unattended and not confirmed by a person. One handoff even lists, among the agent's own steps, a click the team's workflow reserves for a person: marking a pull request ready for review. The notes are honest about slips too: one admits an earlier claim that all Bugbot comments were fixed, when two were not.

SHOW: Pause-and-ponder card.
SAY: Which raises a question: with no person having reviewed it yet, what makes this code trustworthy?

SHOW: Layers, each with holes (an illustration): 807 unit tests (one of them replays the 1,060 probes) · two review bots · decision records that stay 「提议」 until signed; decision 0004 itself still 「提议」, and before any real user: an evaluation and the medical teammate's review of the red-flag cases. Then the twelve items 「下一步（等 Junyi 定）」, the first and fifth highlighted: decision 0006's 10-28 addendum · a dial link for crisis lines on the parent page.
SAY: No single check does. It is layers: hundreds of tests, one of which replays the 1,060 probes, two review bots, and decision records that stay proposals until you sign them. Decision four itself is still a proposal, and before any real user it asks for an evaluation and a look from the team's medical reviewer. Twelve more questions wait for you, from decision six's addendum to whether a parent should get a dial link for a crisis line.

---

## S10 · Recap — `s10_recap.py` · `Recap`

SHOW: The clock again, the phases labelled as they are named.
SAY: So, two days: a skeleton and a fact check in an afternoon; your turn at nine twenty-one; a night of whack-a-mole with the bots; a queue of fix agents; a second night of attacking the checker before the bots could; and a stop rule that held.

SHOW: Three test-yourself questions, then a held pause.
SAY: Three questions. Why did so many of the brain's commits touch the checker? Why reproduce a bug before fixing it? And what is still waiting for you?

SHOW: Next card: 「下一集 · agent 怎么证明自己改对了」 (E5, PR #42); two more pull requests arrived on Friday.
SAY: Two more pull requests arrived on Friday. Next: how an agent proves its change is right.
