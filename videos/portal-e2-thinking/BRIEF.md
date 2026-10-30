# Brief: What is "thought for 3 seconds"? (项目周记 E2)

Series: [docs/PORTAL_SERIES.md](../../docs/PORTAL_SERIES.md) · batch plan:
[videos/portal-series/README.md](../portal-series/README.md) · issue
[#59](https://github.com/JunyiZhou-Conny/Explainer_Videos/issues/59) · the first episode in the
3Blue1Brown style (owner, 2026-10-30: 「以后用 3BLUE1BROWN STYLE PLEASE」).

- **Question.** Conny, 2026-10-30: "there are thinking parts that show thinking for 3 seconds, and I
  can click and expand it … 我相信可能在 2–3 年前其实并不存在这个什么所谓的思考链，也不存在把这些内容展示给观众，
  我也不知道他们展示这个背后的逻辑是怎么样的 … 还有什么可以做的".
- **Learning objective.** The viewer can say what "thinking" is in a reasoning model (hidden tokens,
  billed, set by the effort dial), what our stopwatch measures (until the first character of the
  answer, then writing), what the page is actually streamed (progress lines, never the words, and
  why), how the 911 warning can come before the answer, that the "typing" is a replay of checked
  text, and why the receipt replaces the thoughts. He can name the open decisions waiting for him.
- **Audience.** Conny after E1 (knows harness, instructions / system prompt, token, prompt caching,
  structured outputs, the 13-box form, lint, fallback, "an emergency is never taken back"; reasoning
  model and effort only named). Reads Python, not TypeScript.
- **Style / format.** `3b1b`, `video.yaml` route as in the CareOneX series: 1080p60, Kokoro
  `af_heart` 0.95, music, Chinese-above-English subtitles burned in. Target 8–9 minutes,
  1,150–1,300 words.
- **Evidence rule.** Screens are redrawn from Conny's screenshots (2026-10-30) or from the UI strings
  in the source. Event shapes on screen are the real `TriageStreamEvent` types. Numbers come from
  PR #41's verification notes, the code and the week digest. Claims about OpenAI, Anthropic,
  DeepSeek and the history of chain of thought come from their own papers and docs, read on
  2026-10-30 (SOURCES.md). The example progress line (「已写 320 字」) is the design doc's example
  and is tagged as such.
- **Must include.** The live line and the folded receipt from the screenshots; a short history from
  chain-of-thought prompting to reasoning models and the effort dial; the hidden-token tape; the
  stopwatch phases with real numbers; token streaming vs. our progress streaming (SSE in, NDJSON out);
  why not stream the words; the agent's unattended choice and its "proposed" status; the early 911
  warning (3.5 s vs about 21 s); the 2.5 s replay; stop really stops; the receipt instead of a
  summary; the open decisions.
- **Skip.** The chat page's layout and what was copied from Claude's app (E3); the agents' night and
  the review bots in detail (E4); TypeScript.
- **Ponder questions.** s03: if the thoughts are hidden, what are you paying for, and how would you
  know? s06: why not stream the words and pull them back if the checker objects?
- **Structure.** s01 hook (eleven seconds of what?) → s02 from "think step by step" to a thinking
  dial → s03 hidden tokens and the stopwatch → s04 two kinds of streaming → s05 why not the words,
  and who decided → s06 the early 911 → s07 a replay, and a real stop → s08 how PR #41 got there →
  s09 a receipt, not the thoughts → s10 what else, and what waits for you → s11 recap.
