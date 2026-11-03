# Sources

The source repository is private: `JunyiZhou-Conny/InternationalHealthportal`, read on 2026-10-30
at branch `junyi/40-triage-chat-ui` @ `b7ab98e` (PR #41, draft), which merges PR #36's branch
`claude/affectionate-franklin-igh419` @ `17228bd`. Both PRs were open on that date; the code may
have moved since. Paths below are relative to that repository.

## Screens (s01, s04, s06)

Conny's screenshots, sent in the production chat on 2026-10-30 (not stored in git):

| Shown | Exact strings |
|---|---|
| Answer to a greeting | 你好呀！我能参考本次对话里你告诉我的信息。 |
| Receipt, opened | 思考了 3 秒 · 过程 思考 1.6 秒 → 写 1.5 秒（85 字）→ 检查通过 · 依据 这次没有写出依据 · 检查 通过（剂量、诊断、电话和金额的来源、紧急时先说行动）。 · 判断 只是规则或保险问题 · 给出规则或保险信息 · 模型 gpt-6-luna · 思考强度 中 · 模型用时 3.1 秒 · $0.0004 |
| Parent summary, opened | 给家长的摘要 · 孩子目前只是打了招呼，没有提到身体不适或安全问题。家长暂时无需采取行动。 |
| User's message | not visible in the screenshots; drawn as 「你好」 and tagged `illustration` |

The receipt's rows, their labels and the fallback wording come from
`src/features/triage/ThinkingRow.tsx` (`ThinkingDone`, `checkText`, `CitationList`); the folded
「给家长的摘要」 block and the 「复制给家长」 button from `src/features/triage/TriageAnswer.tsx`;
the order of blocks on the page from `src/features/triage/answerBlocks.ts`.

## The harness (s02–s06)

| Claim | Source |
|---|---|
| The page talks to our server; the key is only on the server | PR #36 description (「key 只在后端」); `prototypes/triage/src/server.ts` |
| Request = BU pages, verified facts, rules, output contract (instructions); then the conversation so far, the context (first turn only; later turns get the time) and the student's words | `prototypes/triage/src/mvp.ts` (`mvpInstructions`, `mvpContext`, `mvpTurn`) |
| "Fixed part first so repeated calls hit the cache" | `mvp.ts` comment on `mvpInstructions` (「固定不变的部分放在最前面……能命中缓存」) |
| 15 official pages | `prototypes/triage/knowledge/snapshots/` (15 files); PR #36 description |
| About 25,000 tokens | `docs/decisions/0004-triage-v0.md`, 10-28 revision (「约 2.5 万 token」) |
| 89 checked facts sent; each card quotes its source sentence, but only `id：claim｜值：value` is sent | `prototypes/triage/knowledge/facts/bu.facts.json` (97 cards: 89 `verified`, 8 `conflict`); `mvp.ts` `usableFacts`, `factTable`; `profile.ts` `sourced` (verified and not in an unresolved conflict). A student without SHIP gets fewer (SHIP plan cards dropped); the default context is SHIP |
| Rules: no diagnosis, no dose, action before money, parents cannot dial 911 from China, parent summary always filled | `mvp.ts` `MVP_RULES`; `prototypes/triage/src/llm/prompts.ts` `OUTPUT_CONTRACT` |
| Cached input on Luna costs a tenth ($0.01 vs $0.10 per million tokens) | `prototypes/triage/src/providers/pricing.ts`, prices checked 2026-10-27 |
| The cache matches a request from its start, so what never changes goes first | OpenAI, *Prompt caching* (developers.openai.com/api/docs/guides/prompt-caching, read 2026-10-30): "Cache reuse requires the entire rendered prefix to match"; "Put stable developer instructions and shared reference material first" |
| The fixed top (pages, facts, rules, form) is the `instructions` field of the request, the system prompt of chat apps | `openai.ts` `buildRequestBody` (`instructions: req.instructions`); `mvp.ts` `mvpInstructions` |
| One call returns the whole form as JSON text | `openai.ts` (one `POST /v1/responses`; `parseResponseBody` reads `output_text` and parses JSON) |
| Luna is a reasoning model; hidden reasoning is billed but not returned; the effort setting (低/中/高) is `reasoning.effort` | `openai.ts` (`reasoning: { effort }`, `output_tokens_details.reasoning_tokens`); `ModelMenu.tsx`; `pricing.ts` (output price covers reasoning tokens); decision 0006 (raw reasoning is not shown) |
| The page times each phase: thinking until the first word of the reply arrives, then writing | `server.ts` `streamTriage` (stage `thinking` at call start, `writing` at the first text delta); `stages.ts` `timelineText`; receipt 「思考 1.6 秒 → 写 1.5 秒（85 字）」 |
| The checker reads the judgment (acuity, disposition) to make sure an emergency comes first | `lint.ts` `isEmergencyOutput`, `emergency_first` |
| $0.0004 for the greeting, model gpt-6-luna | Conny's screenshot |
| Time in Boston and China, whether SHS is open now, computed by code from the posted hours; 「待确认」 when it cannot know (e.g. holidays) | `mvp.ts` `mvpContext` (`shsStatusZh`, `holidayOn`); `prompts.ts` (dual-time rule) |
| Strict structured outputs (`json_schema`, `strict: true`) | `prototypes/triage/src/providers/openai.ts` `buildRequestBody` |
| 13 top-level boxes; urgency has 6 levels | `prototypes/triage/src/llm/schema.ts` `OUTPUT_SCHEMA`, `ACUITIES` |
| Parent-summary instruction (two or three sentences: what is happening, where to go, what the parent can do; always) lives in the rules, not on the box; strict mode requires the box but an empty string would pass it; the `parent_summary` check rejects it | `mvp.ts` `MVP_RULES` (last line), `mvpTurn`; `schema.ts` |
| Sources row = `citations`; judgment row = acuity + disposition; process = the page's stopwatch over the server's stage events; model, model time and cost = server `meta` (`pricing.ts`) | `ThinkingRow.tsx`, `stages.ts`, `TriageChatPage.tsx` |
| More than twenty checker rules | `prototypes/triage/src/lint.ts`: 20 distinct rule names; `mvp.ts` adds `parent_summary`, `pending_discipline`, `emergency_downgraded` |
| One rewrite with the findings sent back; then the fallback | `mvp.ts` `mvpTurn` (two attempts), `fallbackOutput` |
| An emergency is never taken back (only emergency → non-emergency is blocked; other levels may change on a rewrite) | `mvp.ts` (`emergency_downgraded`, `sawEmergency`, `earlierEmergency`) |
| Nothing reads the citations at run time | `lint.ts` (`allText` leaves them out), `pending.ts` strips them; only the offline grader `eval/graders.ts` (`citations_valid`) checks them |
| Dose / diagnosis examples | illustrations of what `no_dosing` / `no_diagnosis` block |

## The path (s07)

| Claim | Source |
|---|---|
| 60 commits over 36 hours (10-27 12:22 → 10-29 00:45, Boston) | week digest [2026-w44](../portal-series/weeks/2026-w44.md), PR #36 (60 own commits + 3 merges) |
| Written with Claude Code | PR #36 and #41 descriptions and handoffs (Claude Code sessions) |
| Sources disagree: out-of-pocket maximum $5,550 (SBC) vs $5,500 (certificate) | `docs/decisions/0004-triage-v0.md`, "数据" |
| Seven conflicts ruled on or marked to be confirmed | `prototypes/triage/knowledge/facts/conflicts.json` (7); decision 0004 |
| First engine: rules decide urgency, the model extracts and explains | decision 0004, architecture option 3 |
| An evaluation of six approaches (R, A, A-web, B, C, D) was built, then shelved before the comparison ran | decision 0004; commit `6ca2941` (arms implemented); `eval/reports/2026-10-27.md` and `2026-10-28.md` contain only arm R; PR #36 description (「本周不再推进」) |
| The turn at 21:21 on Tuesday 10-27 (Boston): the model judges, the output check is the only safety layer; Conny's decision; keyword lists both missed and over-flagged | commit `8f13b18`; decision 0004, "10-28 修订" (dated 10-28 in UTC/Beijing time) |
| Plain chat box at 21:43 (22 minutes later) | commit `2cffee5` |
| Forty more commits, most of them checker hardening | digest: 40 commits after `2cffee5`; by subject, about 23–26 are checker rules, the rest grading, budget and page fixes |
| The safety net is still word rules | `lint.ts` (phrase and clause matching), PR #41 handoff (about 3,000 probed phrasings) |
| Decision 0004 is still "proposed", waiting for the medical reviewer | decision 0004 status line |

## Comparison (s08)

General chat apps are described only as "free prose, guided by a system prompt and the model's
training", which is the public description of how such assistants work; no claim is made about
how ChatGPT or Claude are built internally. The three example new boxes (a note for a roommate,
questions for the doctor, a needs-a-person flag) are proposals, not features of the product.
