# Storyboard

The narration and each scene's visual intent are in `script.json`; the reasons and the evidence for
each claim are in `BRIEF.md` and `SOURCES.md`. This table is the one-line map.

| Scene | Teaching point | On screen, before → after | Evidence |
|---|---|---|---|
| s01 | One word, three answers: who decided, who checked? | Redrawn chat (greeting, parent summary) and the opened receipt, numbered 1–3 → the question card | Conny's screenshots |
| s02 | More than a call: the page talks to our server; the code around the model is a harness with four jobs | page ↔ model → page ↔ server ↔ model, key in the server → HARNESS frame around page + server → four numbered job cards | `server.ts`, PR #36 |
| s03 | Job 1: the request; fixed parts first so they are cached; code supplies the clock | "你好" alone → full stack (pages, 89 facts, rules, form; conversation, context, 你好), cache brace, price bars, $0.0004 → ponder → hours + time zone → code → open / closed / 待确认 | `mvp.ts`, `pricing.ts`, decision 0004 |
| s04 | Job 2: a 13-box form, strict structured outputs; the parent summary is a required box | empty sheet → 13 rows → six urgency levels → STRUCTURED OUTPUTS stamp → parent-summary row + its rule → "空着交上来：检查不让过" → receipt rows linked to boxes | `schema.ts`, `openai.ts`, `MVP_RULES` |
| s05 | Job 3: the checker, one rewrite, the fallback, emergencies never taken back | form enters the LINT gate → five blocked examples → two-try flow with the note and the fallback → 紧急不收回 → ponder → the check row's three values | `lint.ts`, `mvp.ts`, `ThinkingRow.tsx` |
| s06 | Job 4: the page; where each receipt row comes from; the thinking is real (reasoning model, effort, the page's stopwatch); sources is never read by a check | schematic page in block order → five receipt rows with their origins → thinking/writing lane with the greeting's 1.6 s / 1.5 s → two model-written rows marked, "?" → 依据 flagged | `answerBlocks.ts`, `TriageAnswer.tsx`, `ThinkingRow.tsx`, `server.ts` |
| s07 | How PR #36 got here | 60 commit ticks on a Boston-time axis → knowledge base and the $5,550 / $5,500 conflict → rules engine, evaluation shelved → 21:21 turn → 21:43 chat box, 40 commits → the twist | week digest, decision 0004 |
| s08 | Same look (copied from Claude, E3), different machine; a new feature is a new box | two flows side by side, both with a system prompt → form with two proposed boxes → three ticks each | `schema.ts`, `lint.ts` |
| s09 | Recap, three questions, next episode | four job cards → three questions → E2 card | — |
