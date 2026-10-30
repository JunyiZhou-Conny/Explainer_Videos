# 项目周记 E2 · What is "thought for 3 seconds"? Hidden reasoning, progress streaming and a receipt

## 00:00 — Eleven seconds of what?
While you wait for an answer, our app says: thinking, eleven seconds.
Afterwards it folds into a receipt: thought for 22 seconds, which is the whole wait. Open it, and the wait splits in two: only 13.5 seconds of thinking, then 8.7 seconds of writing.
Thinking about what? Three years ago, no chat app showed you a model thinking. And why does ours show you a clock, but never the thoughts?

## 00:27 — From "think step by step" to a thinking dial
The idea is older than the apps. In January 2022, Google researchers showed that a model solves more problems if you ask it to write out its steps first. They called it chain of thought. Months later, one sentence did it: let's think step by step. It was a trick in the prompt.
In September 2024, OpenAI released o1, a model trained with reinforcement learning to reason before it answers. OpenAI chose not to show the raw thoughts, citing user experience, competitive advantage, and the chance to monitor them, and showed a summary written by a model instead.
Others chose differently. DeepSeek's R1 handed its reasoning text to developers. Claude 3.7 showed its raw thinking, as a research preview. From Claude 4, long thinking was summarized, and today's Claude API returns only a summary.
Today, thinking is a setting you choose and pay for. OpenAI calls it reasoning effort. Our menu puts it next to the model choice, Luna, Terra and two others, with three levels: low, medium and high.

## 01:36 — Hidden tokens and the stopwatch
Here is what happens inside one call. A model writes one small piece of text at a time, a token. A reasoning model first writes tokens for itself. Those are its thoughts.
OpenAI never sends those tokens back. They stay hidden, but they take up room, and you pay for them at the output price.
Only then does it write the answer, our thirteen-box form. So our stopwatch can tell the two apart. Thinking is the time until the first character of the answer arrives: the model reads the request, then reasons in hidden tokens. Writing runs from there until the model finishes; then the checker runs.
The effort setting sets how much thinking the model may do. Even on the same setting, the model decides how much it needs: your greeting thought for 1.6 seconds, a real question about the student clinic for 13.5.
If the thoughts are hidden, what exactly are you paying for, and how would you know?
Every response ends with a usage report, and it counts the reasoning tokens inside the output tokens. Our server reads it, and the price list turns those counts into the dollar figure on the receipt.

## 02:55 — Two kinds of streaming
Why show anything while you wait? The decision record puts it plainly: ten to thirty seconds of waiting, and nobody can tell what is happening. Most chat apps answer that by streaming: every few words travel to your screen the moment they are written, over a pipe called server-sent events.
Our server does receive that stream from OpenAI. But it does not pass the words on. It reads the form as it fills, notes which box the model is in, counts the characters, and sends the page only progress, one small line of JSON at a time.
That is what you watch: thinking, eleven seconds. Writing the places to go, 320 characters so far. Checking. The page never sees a word before the checker has.

## 03:41 — Why not the words, and who decided
Why not stream the words, the way Claude does, and pull them back if the checker objects?
Because a screen cannot unsay something. If a dose or a made-up phone number flashes for two seconds, a worried parent may already have a screenshot. So the decision record says: stream the progress, not the text.
You asked for streaming. The agent, working unattended, chose this kind on its own, and wrote it down as a proposal that is still waiting for your yes.

## 04:14 — The early 911
Progress streaming has one more trick. The form's first five boxes are all about urgency, so the model writes them first.
The moment those first boxes say emergency, the server raises a flag, and the page shows a warning we wrote ourselves: possibly life-threatening, don't wait, call 911 now.
In a real test, the warning appeared at 3.5 seconds, and the checked answer at about 21 seconds. And since an emergency is never taken back, that answer is bound to agree.

## 04:47 — A replay, and a real stop
When the checked answer finally arrives, the page plays it out in at most two and a half seconds: sentences type themselves, lists drop in whole. It looks like streaming. It is a replay of text that has already passed.
Emergency answers skip the show and appear at once. And the stop button really stops: the page hangs up, and the server cancels the model call it was paying for.

## 05:11 — How it got built
On Wednesday morning, Boston time, the streaming went in within twenty minutes. A few minutes later, a note for the menu: switching model or effort starts a fresh cache, so on Terra that first answer costs about five times as much.
Much of the rest of the day went to what reviews found: keeping the 911 warning through stop, retry and dropped connections, and a test that fails if any four consecutive characters of the model's text show up in the progress lines before the result. That test is the proof that no words reach the page before the checker has passed them.

## 05:48 — A receipt, not the thoughts
So what sits behind "thought for 22 seconds"? Claude's app also shows a timer while it thinks, and, like ChatGPT, opens onto a summary of the model's reasoning. Ours opens onto a receipt: the timings, the sources, the check, the judgment, the model and the price.
The reason is in the decision record. Raw reasoning may contain diagnostic guesses, and nothing has checked it. In a medical product, a guess on screen reads like a diagnosis.

## 06:19 — What else, and what waits for you
Where could this go? OpenAI can return a summary of the hidden reasoning. But a summary is written by a model too, so it would have to pass the same checker before anyone sees it. The progress line could name real steps, like checking the clinic's hours. And the agent raised a developer-only switch to see unchecked drafts while tuning prompts. It was not built.
Three decisions wait for you. Progress-only streaming and the model menu are written down as proposals; the developer switch, as an open question.

## 06:52 — Recap
So, thought for 22 seconds. First thinking: hidden tokens the model writes for itself, billed but never sent. Then writing, which our server watches box by box, passing on progress but not words. An early warning when the first boxes say emergency. A replay once the checker has passed it. And a receipt instead of the thoughts.
Three questions. What exactly does our stopwatch call thinking? Why do the urgency boxes come first in the form? And what would a reasoning summary need before it could be shown?
Next time, the page itself: what we copied from Claude's app, what we refused, and what we could invent.
