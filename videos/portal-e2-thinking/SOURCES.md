# Sources: 项目周记 E2 · What is "thought for 3 seconds"?

Everything on screen or in the narration comes from one of the sources below. The portal repository
is private; paths are given so a reader with access can check them.

## The product (JunyiZhou-Conny/InternationalHealthportal)

Branch `junyi/40-triage-chat-ui` at `b7ab98e` (PR #41, the chat page, stacked on PR #36 at `17228bd`),
read 2026-10-30. Week digest: [`../portal-series/weeks/2026-w44.md`](../portal-series/weeks/2026-w44.md).

| Claim in the video | Source |
| --- | --- |
| The live line 「正在思考 · 11 秒」, the folded 「思考了 22 秒」, the rows 过程 / 依据 / 检查 / 判断 / 模型 with 「思考 13.5 秒 → 写 8.7 秒（1717 字）→ 检查通过」 and 「gpt-6-luna · 思考强度 中 · 模型用时 22.1 秒 · $0.0013」; the greeting's 「思考 1.6 秒 → 写 1.5 秒（85 字）→ 检查通过」 | Conny's screenshots, 2026-10-30 (shared in chat; not committed) |
| The stopwatch: thinking until the first character of the answer, then writing, then checking; the folded 「思考了 N 秒」 is the whole wait | `src/features/triage/ThinkingRow.tsx` (the page's clock over the server's `stage` events; `ThinkingDone` rounds the turn's `elapsedMs`) |
| Thinking time = the model reading the request, then reasoning (the video does not claim how the 13.5 s divides) | OpenAI reasoning guide (below); the typical turn's 150 reasoning tokens are not the clinic turn's |
| The model menu: Astra 最贵 · Sol · Terra · Luna 最便宜, then 思考强度 低 / 中 / 高 | `prototypes/triage/src/server.ts` (`MODEL_INFO`, `TRIAGE_MODELS` defaults to the whole price table); `docs/design/README.md` (the menu's layout) |
| "Ten to thirty seconds of waiting, and nobody can tell what is happening" | `docs/decisions/0006-triage-chat-copies-claude.md` line 70: 「干等 10–30 秒，人不知道在发生什么」 |
| The first five boxes are about urgency: acuity, disposition, followUp (red-flag questions), redFlagsPositive, emergency | `prototypes/triage/src/llm/schema.ts:58-62` |
| The answer is a 13-box form, written in schema order with urgency first | `prototypes/triage/src/llm/schema.ts` (`acuity`, `disposition`, `followUp`, `redFlagsPositive`, `emergency`, … `citations`) |
| Reasoning tokens counted inside output tokens; the server reads them | `prototypes/triage/src/providers/openai.ts:68,89` (`usage.output_tokens_details.reasoning_tokens`) |
| The typical turn (26,500 input, 25,600 cached, 1,000 output, 150 reasoning) and its price; "≈ $0.0009 on Luna" | `prototypes/triage/src/server.ts:50-54` (`TYPICAL_TURN`, its comment: from recent real requests in `runs/`; used for the menu's price estimates, so the card says "the typical turn server.ts assumes for prices") × `prototypes/triage/src/providers/pricing.ts` |
| On Terra the first answer after a switch costs about five times as much ($0.038 vs $0.0074) | same: `firstTurnUsd` (no cached input) vs `turnUsd`, Terra's prices in `pricing.ts` |
| SSE in from OpenAI (`stream: true`) | `prototypes/triage/src/providers/openai.ts:12,253` |
| The server tracks the box, the character count and the emergency flag, and sends progress at most every 150 ms; never the text | `prototypes/triage/src/streamProgress.ts`, `prototypes/triage/src/server.ts:218` (`PROGRESS_EVERY_MS = 150`) |
| The event shapes on screen (`start`, `stage`, `progress`, `result`) | `prototypes/triage/src/apiTypes.ts` (`TriageStreamEvent`); fields left out on screen are marked "…" |
| 「正在写回答 · 去处和步骤 · 已写 320 字」 | the design doc's example: `docs/design/README.md:23` (tagged "example" on screen) |
| The early warning text 「初步判断可能危及生命。不用等回答写完，现在就打 911。」 (student wording) | `src/features/triage/ThinkingRow.tsx:44` (`EarlyEmergency`) |
| The warning at 3.5 s; the checked answer at about 21 s | PR #41's verification notes: 「紧急时第 3.5 秒就提醒打 911，约 21 秒后出现「现在就做」」. Read as about 21 s after sending: the same note's ordinary turns took 14.6 s and 21.6 s in total, and the series plan reads it the same way. The other reading (21 s after the warning) would put the answer at about 24.5 s; the video says "about 21 seconds" and "≈ 17 s sooner". |
| An emergency is never taken back | `prototypes/triage/src/mvp.ts` (E1, SOURCES) |
| The replay: at most 2.5 s; text blocks type, structural blocks drop in whole | `src/features/triage/reveal.ts:10,66` (`MAX_REVEAL_MS = 2500`, `STRUCT_UNITS`) |
| Emergency answers appear at once | `src/features/triage/answerBlocks.ts:57` (`shouldAnimate`) |
| Stop cancels the model call | `prototypes/triage/src/server.ts:209-221,310` (`abortOnDisconnect`) |
| The leak test: no 4 consecutive characters of the model's text in the progress lines before the result; its purpose | `prototypes/triage/src/server.test.ts` (the streaming tests, around line 170); decision 0006 line 110 (「进度里没有模型写的文字」) |
| Commit times on Wednesday 2026-10-28, Boston time (10:40, 10:57, 11:04, 11:09, 17:09, 18:44) | the week digest, PR #41 section |
| "You asked for streaming"; progress-only, chosen unattended, status 提议; the verbatim-streaming option considered and not done; raw reasoning not shown; the developer-only switch as an open question | `docs/decisions/0006-triage-chat-copies-claude.md` (10-28 addendum) |

## Outside the product (read 2026-10-30)

| Claim | Source |
| --- | --- |
| Chain-of-thought prompting, January 2022, Google Research | Wei et al., arXiv [2201.11903](https://arxiv.org/abs/2201.11903) (first posted 28 Jan 2022); [Google Research blog](https://research.google/blog/language-models-perform-reasoning-via-chain-of-thought/) |
| "Let's think step by step", May 2022 | Kojima et al., arXiv [2205.11916](https://arxiv.org/abs/2205.11916) (24 May 2022) |
| o1, September 2024, trained with reinforcement learning to reason | [OpenAI API changelog](https://developers.openai.com/api/docs/changelog) (12 Sep 2024); o1 System Card, arXiv [2412.16720](https://arxiv.org/abs/2412.16720) |
| Raw chain of thought hidden "after weighing multiple factors including user experience, competitive advantage, and the option to pursue the chain of thought monitoring"; a model-generated summary shown instead | [Learning to reason with LLMs](https://openai.com/index/learning-to-reason-with-llms/) (OpenAI, 2024; the page refused automated fetches, wording checked against a verbatim copy: [Simon Willison, 2024-09-12](https://simonwillison.net/2024/Sep/12/openai-o1/)) |
| Reasoning tokens not returned, occupy context, billed as output; the `summary` parameter; effort values are model-dependent | [OpenAI reasoning guide](https://developers.openai.com/api/docs/guides/reasoning) |
| Streaming over server-sent events | [OpenAI streaming guide](https://developers.openai.com/api/docs/guides/streaming-responses) |
| DeepSeek-R1, January 2025; reasoning text returned in the API (`reasoning_content`) | [DeepSeek news, 2025-01-20](https://api-docs.deepseek.com/news/news250120); [thinking mode guide](https://api-docs.deepseek.com/guides/thinking_mode/) |
| Claude 3.7 Sonnet: raw thinking made visible, a research preview | [Claude 3.7 Sonnet](https://www.anthropic.com/news/claude-3-7-sonnet); [Visible extended thinking](https://www.anthropic.com/news/visible-extended-thinking) |
| From Claude 4, long thinking summarized | [Claude 4](https://www.anthropic.com/news/claude-4) ("thinking summaries … only needed about 5% of the time") |
| Today's Claude API returns a summary only | [Extended thinking docs](https://platform.claude.com/docs/en/build-with-claude/thinking) ("what you see is never the raw chain of thought") |
| Claude's app: a "Thinking" indicator with a timer, an expandable summary | [Claude help: using extended thinking](https://support.claude.com/en/articles/10574485-using-extended-thinking) |
| ChatGPT shows a summary of the reasoning | OpenAI 2024 (above). The exact labels in today's ChatGPT ("Thought for N seconds") were not verified, so the video draws ChatGPT's panel as an illustration and does not quote a label. |

## Illustrations (tagged on screen)

- s03: the three lines of "thoughts" for the clinic question are invented to show what hidden reasoning is like; the real ones are never returned to us.
- s05: the phone with a streamed dose line.
- s09: ChatGPT's panel.

## Not claimed

- That "Thought for N seconds" is any app's exact wording, other than our own product's strings.
- That DeepSeek's app showed the complete reasoning (only the API is claimed).
- Any effort values beyond our menu's three (OpenAI's list is model-dependent).
