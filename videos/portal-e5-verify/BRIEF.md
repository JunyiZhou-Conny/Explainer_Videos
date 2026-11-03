# Brief: How an agent proves its change is right (项目周记 E5 · agent 怎么证明自己改对了)

Series: [docs/PORTAL_SERIES.md](../../docs/PORTAL_SERIES.md) · batch plan:
[videos/portal-series/README.md](../portal-series/README.md) · issue
[#66](https://github.com/JunyiZhou-Conny/Explainer_Videos/issues/66) · 3Blue1Brown style (the house default).

- **Question.** The owner, 2026-10-31: 「开始做吧」, for the two PRs opened after the week's batch was planned.
  This one is InternationalHealthportal PR #42, 「验证工具：转诊规则的穷举检查（npm run verify）+ 操作真实 App 的 verify-app skill」.
- **Learning objective.** The viewer can:
  - say what a reducer is and why the order of actions matters;
  - explain exhaustive checking as "try every order in a small world, check rules in every state, and report the shortest failing story";
  - retell the expired-referral bug and why tests missed it;
  - explain why the agent broke its own code on purpose (a check never seen to fail proves nothing);
  - describe driving the real app by role and name with evidence;
  - say what waits for a person.
- **Audience.** Conny after E1–E4. He knows the checker and E4's "layers instead of a human review" question. He doesn't know model checking or browser automation, and reads Python, not TypeScript.
- **Style / format.** `3b1b`, `video.yaml` route as in E2–E4: 1080p60, Kokoro `af_heart` 0.95, music, Chinese-above-English subtitles burned in. Target 7–9 minutes, 1,050–1,300 words.
- **Evidence rule.**
  - Every claim comes from PR #42 at `fe19a23`, its files, or the research run of both tools on a temporary worktree (`SOURCES.md`).
  - Outside context comes from primary sources only: Lamport's TLA+ page, the 2015 CACM Amazon paper, DeMillo–Lipton–Sayward 1978, Stryker's docs and Anthropic's Claude Code best practices.
  - The five breakages' traces are our reproduction and are marked as such.
- **Must include.**
  - **The bug.** It must be told verbatim, including that the code comment claims the case is handled and that 245 tests passed.
  - **The reducer and the exhaustive check.** The reducer in plain words. The small world of the exhaustive check: 2 referrals, 3 slots, 2 moments, 13 first moves, breadth-first, 13,898 states, about 1 s.
  - **Rules and the result.** The five rules, and the shortest two-step story.
  - **KNOWN_FINDINGS.** Findings stay findings; the check fails when the bug is fixed.
  - **The five deliberate breakages.**
  - **The Amazon parallel.** A 35-step trace that passed reviews and testing.
  - **verify-app.** Role and name; wait for quiet; the evidence standard; isolation; a failure message with a hint.
  - **Origin.** The pstack skills.
  - **What waits for a person.** The fix choice, the untested local install, and the draft status.
- **Skip.** Code on screen, CLI flags beyond what the story needs, TLA+ syntax.
- **Ponder questions.**
  - S02: A test checks the cases someone thought of. What checks the ones nobody thought of? (Answered in S03.)
  - S05: Why would an agent break its own code on purpose? (Answered at once.)
  - S09 recap questions:
    - What does the exhaustive check try that an ordinary test doesn't?
    - Why break your own code on purpose?
    - Why does the check fail when the bug gets fixed?
