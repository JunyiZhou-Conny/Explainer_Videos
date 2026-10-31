# 项目周记 E2 · What is "thought for 3 seconds"? — script & visual plan

Series: *项目周记* (`docs/PORTAL_SERIES.md`). Watch after E1. Brief: `BRIEF.md`; every claim's source:
`SOURCES.md`.

Audience: Conny, after E1. Goal: he can say what "thinking" is in a reasoning model, what our
stopwatch measures, what the page is really streamed and why, how the 911 warning comes early, why
the "typing" is a replay, why the receipt replaces the thoughts, and which decisions wait for him.

**Narrated.** SAY lines are spoken (Kokoro `af_heart`, 0.95×, over a quiet music bed) and shown as
subtitles (Chinese above, English below). Field names are shown, not read.

Colours: our code BLUE · the model / API ORANGE · hidden reasoning GREY · visible text WHITE, checked
text GREEN · the user's words YELLOW · danger RED · Claude / ChatGPT GREY outline (names only, no
logos) · time = a horizontal axis in seconds.

---

## S01 · Eleven seconds of what? — `s01_hook.py` · `Hook`

SHOW: A dark panel redraws the live line from Conny's screenshot: an orange dot and 「正在思考 · 11 秒」, the counter ticking 9, 10, 11.
SAY: While you wait for an answer, our app says: thinking, eleven seconds.

SHOW: It folds into 「思考了 22 秒 ›」, which opens: 过程 「思考 13.5 秒 → 写 8.7 秒（1717 字）→ 检查通过」, 模型 「gpt-6-luna · 思考强度 中 · 模型用时 22.1 秒 · $0.0013」. Two bars under it: GREY 13.5 s, WHITE 8.7 s.
SAY: Afterwards it folds into a receipt: thought for 22 seconds, which is the whole wait. Open it, and the wait splits in two: only 13.5 seconds of thinking, then 8.7 seconds of writing.

SHOW: A question mark over the GREY bar. Then the question card.
SAY: Thinking about what? Three years ago, no chat app showed you a model thinking. And why does ours show you a clock, but never the thoughts?

---

## S02 · From "think step by step" to a thinking dial — `s02_history.py` · `History`

SHOW: A timeline 2022 → 2026. January 2022: "Chain-of-thought prompting · Wei et al., Google"; May 2022: a prompt ending in YELLOW "Let's think step by step." with numbered steps under it; label "a trick in the prompt".
SAY: The idea is older than the apps. In January 2022, Google researchers showed that a model solves more problems if you ask it to write out its steps first. They called it chain of thought. Months later, one sentence did it: let's think step by step. It was a trick in the prompt.

SHOW: September 2024: an ORANGE box "o1 · OpenAI · trained with reinforcement learning to reason"; its steps slide behind a GREY curtain; in front, a short "summary" card. OpenAI's three reasons as chips: user experience · competitive advantage · monitoring the thoughts.
SAY: In September 2024, OpenAI released o1, a model trained with reinforcement learning to reason before it answers. OpenAI chose not to show the raw thoughts, citing user experience, competitive advantage, and the chance to monitor them, and showed a summary written by a model instead.

SHOW: 2025: "DeepSeek-R1 · Jan · reasoning text in the API" · "Claude 3.7 · Feb · raw thinking, a research preview" · "Claude 4 · May · long thinking summarized" · "Claude API today · summary only". Each a GREY outline with the name.
SAY: Others chose differently. DeepSeek's R1 handed its reasoning text to developers. Claude 3.7 showed its raw thinking, as a research preview. From Claude 4, long thinking was summarized, and today's Claude API returns only a summary.

SHOW: Today: a dial "reasoning effort" with our menu's three stops 「思考强度 低 / 中 / 高」, beside our model menu redrawn from the design doc and server.ts: Astra 最贵 · Sol · Terra · Luna 最便宜, then 思考强度 低 / 中 / 高.
SAY: Today, thinking is a setting you choose and pay for. OpenAI calls it reasoning effort. Our menu puts it next to the model choice, Luna, Terra and two others, with three levels: low, medium and high.

---

## S03 · Hidden tokens — `s03_tokens.py` · `HiddenTokens`

SHOW: An ORANGE model box writes small squares one at a time onto a tape. Label: "one token at a time". Over the GREY run, an illustration of what such thoughts might say for the clinic question (tagged: illustration; the real ones are never sent to us).
SAY: Here is what happens inside one call. A model writes one small piece of text at a time, a token. A reasoning model first writes tokens for itself. Those are its thoughts.

SHOW: The first tokens are GREY and slide behind a curtain marked "hidden · billed as output". A meter fills: reasoning tokens.
SAY: OpenAI never sends those tokens back. They stay hidden, but they take up room, and you pay for them at the output price.

SHOW: Then WHITE tokens appear on the tape: the form's first boxes (acuity, disposition …). Above the tape a stopwatch splits the time at the first WHITE token: "thinking" | "writing".
SAY: Only then does it write the answer, our thirteen-box form. So our stopwatch can tell the two apart. Thinking is the time until the first character of the answer arrives: the model reads the request, then reasons in hidden tokens. Writing runs from there until the model finishes; then the checker runs.

SHOW: The effort dial turns: low → a short GREY run, high → a long one, the WHITE answer the same length in both. Then two real receipts as bar pairs: greeting 1.6 s | 1.5 s; a question that ended in 「近期预约学校医疗中心」 13.5 s | 8.7 s, both "gpt-6-luna · 中".
SAY: The effort setting sets how much thinking the model may do. Even on the same setting, the model decides how much it needs: your greeting thought for 1.6 seconds, a real question about the student clinic for 13.5.

SHOW: Pause-and-ponder card.
SAY: If the thoughts are hidden, what exactly are you paying for, and how would you know?

SHOW: The usage report of the typical turn server.ts assumes for its price estimates (from recent runs; reasoning varies by question): input tokens, cached input tokens, output tokens, and inside them the reasoning tokens. Our server reads it; the price list prices the output tokens, reasoning included, into the receipt's price.
SAY: Every response ends with a usage report, and it counts the reasoning tokens inside the output tokens. Our server reads it, and the price list turns those counts into the dollar figure on the receipt.

---

## S04 · Two kinds of streaming — `s04_streams.py` · `TwoStreams`

SHOW: Decision 0006's reason for showing progress at all: 「干等 10–30 秒，人不知道在发生什么」. Then a GREY-outlined "typical chat app": model → page, words flowing as they are written. Label "token streaming · server-sent events".
SAY: Why show anything while you wait? The decision record puts it plainly: ten to thirty seconds of waiting, and nobody can tell what is happening. Most chat apps answer that by streaming: every few words travel to your screen the moment they are written, over a pipe called server-sent events.

SHOW: Right: ours. ORANGE model → BLUE server: the words arrive (SSE) and stop there. The server reads the form as it fills: which box, how many characters. Out of the server, to the page, only small JSON lines (NDJSON), in the real event shapes: `{"type":"start","model":…,"effort":"medium","mode":"live"}` · `{"type":"stage","stage":"thinking","attempt":1}` · `{"type":"progress","attempt":1,"section":"options","chars":320,"emergency":false}` · `{"type":"stage","stage":"checking","attempt":1}` · `{"type":"result","response":{…}}`.
SAY: Our server does receive that stream from OpenAI. But it does not pass the words on. It reads the form as it fills, notes which box the model is in, counts the characters, and sends the page only progress, one small line of JSON at a time.

SHOW: Each line becomes the page's text: 「正在思考 · 11 秒」 → 「正在写回答 · 去处和步骤 · 已写 320 字」 (example from the design doc) → 「正在检查」 → the answer.
SAY: That is what you watch: thinking, eleven seconds. Writing the places to go, 320 characters so far. Checking. The page never sees a word before the checker has.

---

## S05 · Why not the words? — `s05_why.py` · `WhyNot`

SHOW: Pause-and-ponder card.
SAY: Why not stream the words, the way Claude does, and pull them back if the checker objects?

SHOW: A streamed sentence with a dose in it (illustration) flashes on a phone; a camera-shutter flash; then it is struck out, too late. Decision 0006, considered and not done: 「直接流式显示模型的原文（像 Claude 那样）：没有经过检查，可能出现剂量、诊断、编造的电话，出来以后再收回更糟。不做。」
SAY: Because a screen cannot unsay something. If a dose or a made-up phone number flashes for two seconds, a worried parent may already have a screenshot. So the decision record says: stream the progress, not the text.

SHOW: The decision card with status 「提议」 and the line 「具体做法是无人值守时定的，还没有人确认」.
SAY: You asked for streaming. The agent, working unattended, chose this kind on its own, and wrote it down as a proposal that is still waiting for your yes.

---

## S06 · The early 911 — `s06_early911.py` · `Early911`

SHOW: The form's boxes in order, the first five glossed (acuity 紧急程度 · disposition 去哪里 · followUp 追问 · redFlagsPositive 危险信号 · emergency 紧急行动); they light up as the WHITE tokens reach them.
SAY: Progress streaming has one more trick. The form's first five boxes are all about urgency, so the model writes them first.

SHOW: A RED flag `"emergency": true` rises in the progress line; on the page, the fixed warning (student version): 「初步判断可能危及生命。不用等回答写完，现在就打 911。」 tagged "written by us, not by the model"; the parent version asks someone local to call.
SAY: The moment those first boxes say emergency, the server raises a flag, and the page shows a warning we wrote ourselves: possibly life-threatening, don't wait, call 911 now.

SHOW: A time axis: warning at 3.5 s; the full checked answer, with 「现在就做」 at the top, at about 21 s (PR #41: 「第 3.5 秒就提醒打 911，约 21 秒后出现「现在就做」」, read as 21 s after sending, see SOURCES.md). The checker's rule from E1: an emergency is never taken back.
SAY: In a real test, the warning appeared at 3.5 seconds, and the checked answer at about 21 seconds. And since an emergency is never taken back, that answer is bound to agree.

---

## S07 · A replay, and a real stop — `s07_replay.py` · `Replay`

SHOW: The checked answer arrives whole (GREEN); a playhead runs over it: the explanation types itself, the numbered places drop in as blocks, all within 2.5 s.
SAY: When the checked answer finally arrives, the page plays it out in at most two and a half seconds: sentences type themselves, lists drop in whole. It looks like streaming. It is a replay of text that has already passed.

SHOW: An emergency answer appears at once, no animation. Then the stop button: the page hangs up, the BLUE server cuts the ORANGE call.
SAY: Emergency answers skip the show and appear at once. And the stop button really stops: the page hangs up, and the server cancels the model call it was paying for.

---

## S08 · How it got built — `s08_path.py` · `Path`

SHOW: PR #41's 28 own commits on a Wednesday axis, Boston time. Marked: 10:40 "the server streams progress; model and effort menu" · 10:57 "the page streams progress" · 11:04 "switching model or effort starts without the cache".
SAY: On Wednesday morning, Boston time, the streaming went in within twenty minutes. A few minutes later, a note for the menu: switching model or effort starts a fresh cache, so on Terra that first answer costs about five times as much.

SHOW: The rest of the day: 11:09 "keep the 911 warning when you press stop" · 17:09 "… across stop, retry and dropped connections" · 18:44 "make the tests fail when what they guard is broken". A test card: "before the result, no 4 consecutive characters of the model's text may appear in the progress lines" (server.test.ts).
SAY: Much of the rest of the day went to what reviews found: keeping the 911 warning through stop, retry and dropped connections, and a test that fails if any four consecutive characters of the model's text show up in the progress lines before the result. That test is the proof that no words reach the page before the checker has passed them.

---

## S09 · A receipt, not the thoughts — `s09_receipt.py` · `Receipt`

SHOW: The folded 「思考了 22 秒 ›」 again; then three panels. Claude's app: "Thinking" with a timer, opening onto a summary (GREY outline; per Anthropic's help page). ChatGPT: a model-written summary of the reasoning (GREY outline, illustration). Ours: the stopwatch and the five rows of the receipt, each glossed (过程 timings · 依据 sources · 检查 check · 判断 judgment · 模型 model + price).
SAY: So what sits behind "thought for 22 seconds"? Claude's app also shows a timer while it thinks, and, like ChatGPT, opens onto a summary of the model's reasoning. Ours opens onto a receipt: the timings, the sources, the check, the judgment, the model and the price.

SHOW: Decision 0006's line: 「不显示模型的推理原文：里面可能有诊断性的猜测，又没有经过检查。」
SAY: The reason is in the decision record. Raw reasoning may contain diagnostic guesses, and nothing has checked it. In a medical product, a guess on screen reads like a diagnosis.

---

## S10 · What else, and what waits for you — `s10_next.py` · `Next`

SHOW: Three idea cards. 1 "a reasoning summary, put through the checker first" · 2 "progress that names real steps: 「正在核对 SHS 营业时间」 (idea)" · 3 "a developer-only view of unchecked drafts (an open question, not built)".
SAY: Where could this go? OpenAI can return a summary of the hidden reasoning. But a summary is written by a model too, so it would have to pass the same checker before anyone sees it. The progress line could name real steps, like checking the clinic's hours. And the agent raised a developer-only switch to see unchecked drafts while tuning prompts. It was not built.

SHOW: Under 「等你决定」: two chips marked 「提议」 (progress-only streaming · the model menu) and one marked 「待定」 (the developer switch).
SAY: Three decisions wait for you. Progress-only streaming and the model menu are written down as proposals; the developer switch, as an open question.

---

## S11 · Recap — `s11_recap.py` · `Recap`

SHOW: The tape again, annotated end to end: GREY hidden thinking → WHITE writing watched box by box → RED flag if emergency → GREEN checked answer replayed → the receipt.
SAY: So, thought for 22 seconds. First thinking: hidden tokens the model writes for itself, billed but never sent. Then writing, which our server watches box by box, passing on progress but not words. An early warning when the first boxes say emergency. A replay once the checker has passed it. And a receipt instead of the thoughts.

SHOW: Three test-yourself questions.
SAY: Three questions. What exactly does our stopwatch call thinking? Why do the urgency boxes come first in the form? And what would a reasoning summary need before it could be shown?

SHOW: Next-episode card: 「照着 Claude 抄」.
SAY: Next time, the page itself: what we copied from Claude's app, what we refused, and what we could invent.
