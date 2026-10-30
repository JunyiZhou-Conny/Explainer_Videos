# 项目周记 E4 · Two days, a hundred-plus commits: how the agents worked, and who decided

## 00:00 — Two days on one clock
This is every commit on our two triage pull requests, on one clock: Boston time, from Tuesday noon to early Thursday. 109 commits, every one made by an agent: 88 changes, and 21 merges of one branch into another. GitHub shows forty of them under your name, because the agent used your git identity.
Two questions. Why are most of them fixes? 53 of the 88 name a review in their message: Bugbot, Codex, or a review agent. And no person has reviewed them yet, so who decided anything?

## 00:35 — How the work is organised
First, the machinery. Each job starts as an issue, gets its own branch, and opens a draft pull request after the first commit. Pushes wake two review bots from different companies: Cursor's Bugbot on every push, and OpenAI's Codex once the pull request is marked ready for review. They may comment, but never change code.
When an agent stops, it writes a handoff note on the pull request, marked unattended when nobody was watching. Big choices become decision records, marked proposed until a person marks them adopted. The team's rule: chat is temporary, the repository is permanent.
Two agent sessions made the commits: the first until just after midnight, the second from one fifty-one on Wednesday morning to a quarter to one on Thursday. The chat page was stacked on top of the triage brain, and pulled in the brain's changes 13 times.

## 01:32 — Day one: a skeleton, then a fact check
Tuesday, at twelve twenty-two, after a night of planning, the first session started committing. Within forty minutes it had a skeleton: fact cards from 15 sources, a rules engine that decided urgency, eleven test cases and an evaluation.
Then it checked its own facts. Four reviewer agents that could not talk to each other read every card against its source and reported 75 problems. Twenty-three minutes after the first 74 cards, there were 97. One had said out-of-network urgent care costs you 20 percent; the source said you pay a five-hundred-dollar deductible first.

## 02:11 — The turn at 9:21
At nine twenty-one that evening, Boston time, Wednesday morning in Beijing, a commit changed the plan. The rules engine matched words, and word lists both missed things and flagged the wrong things; every patch broke something else.
The record says you decided: a demo first, evaluation later; the model judges urgency and where to go, and the checker on its output becomes the only safety layer. The rules engine and the comparison experiments stay in the repository, no longer pursued.
But notice: the checker is also made of word rules, applied to sentences instead of symptoms. What would make it less of a whack-a-mole?

## 02:54 — The loop with the bots
Then came the loop. At ten twenty-three the agent marked the brain's pull request ready for review and asked two teammates to look, and both bots began reviewing every push. Push, the bots review, the agent fixes, push again. Between ten twenty-seven and just after midnight the first session pushed 19 commits, about one every five minutes. On that pull request the bots wrote 72 comments, and 64 led to fixes.
By half past midnight, you and the agent had agreed on one change: batch the fixes before pushing.

## 03:30 — Day two: a queue of fix agents
On Wednesday the second session built the chat page from episode three and kept fixing the brain beside it. In the afternoon a final review looked from five angles at once and found about 30 problems.
Six fix agents took them one after another, each on its own branch, and each first reproduced its bug before fixing it.
Why reproduce a bug before fixing it?
Because a reproduction proves the bug is real, and gives a check that has to flip from failing to passing; a fix for a bug nobody saw fail proves nothing. Merging the branches back took about an hour and had collisions; in one, a branch added a field that another branch's new test rejected. A second review of the merged result found eight more.
Along the way the session hit its five-hour usage limit twice, the second time because the six fix agents ran in a row at about 800,000 tokens each, and the container restarted twice. The agents' rule afterwards: at most three at a time.

## 04:37 — Attack your own checker
Back to the checker. Most of the bots' comments were about it. After the turn it grew from 459 lines to 1,326, and 27 of the 45 commits since touched it. Each fix moved the problem. On Wednesday a parent summary saying don't delay help because of insurance was flagged as putting money first, which cost a needless rewrite; that evening, narrowing a similar rule let a real money-first line slip through, until Bugbot caught it.
So on the second night the agents stopped waiting for the bots. Two rules took the beating: never claim a clinic is open right now unless its hours are checked, and keep cost out of the way of an emergency. Before pushing, the agents attacked those two rules: they wrote about 3,000 ways to say a risky thing, or its harmless twin, and ran them all. The first round found 142 misses and 230 false alarms.
The bots would have found these too. Why attack the checker yourself first?
Because the bots report one finding at a time, and every fix waits for the next review. One probing run found 372 at once. Across both rounds, 1,060 phrasings it got wrong were fixed and kept as tests that run with the unit tests; about twenty harder ones are listed as known misses. In the second round, the first fix even created 20 new false alarms; this time they were caught before the push, not after.

## 06:12 — What it cost
What did it cost? The model calls the product made are on the record: about 4 cents for one real answer, about 77 cents for the whole first day, 27 cents on the last night against a 50-cent cap. The agents' own work is priced nowhere in the repository; the only number is tokens: about 800,000 per fix agent, close to five million for the six, and none recorded for the rest.

## 06:40 — Who decided, and what waits
So who decided? The record, written by the agents, names your calls, among them the model and its effort, the turn to the model's judgement, batching the fixes, copying Claude's page, and the stop rule: stop at 99 percent, finish by Thursday at seven in the evening, Beijing time. The code kept it: the last push came more than six hours early, and four later bot findings were written down for the next person.
Many smaller choices the agents made alone, and wrote down as proposals, marked unattended and not confirmed by a person. One handoff even lists, among the agent's own steps, a click the team's workflow reserves for a person: marking a pull request ready for review. The notes are honest about slips too: one admits an earlier claim that all Bugbot comments were fixed, when two were not.
Which raises a question: with no person having reviewed it yet, what makes this code trustworthy?
No single check does. It is layers: hundreds of tests, one of which replays the 1,060 probes, two review bots, and decision records that stay proposals until you sign them. Decision four itself is still a proposal, and before any real user it asks for an evaluation and a look from the team's medical reviewer. Twelve more questions wait for you, from decision six's addendum to whether a parent should get a dial link for a crisis line.

## 08:17 — Recap
So, two days: a skeleton and a fact check in an afternoon; your turn at nine twenty-one; a night of whack-a-mole with the bots; a queue of fix agents; a second night of attacking the checker before the bots could; and a stop rule that held.
Three questions. Why did so many of the brain's commits touch the checker? Why reproduce a bug before fixing it? And what is still waiting for you?
That ends this week's batch. Next week's episodes start from next week's pull requests.
