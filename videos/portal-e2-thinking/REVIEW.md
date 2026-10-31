# Review record: What is "thought for 3 seconds"? (项目周记 E2)

Produced 2026-10-30 by a Claude Code cloud session (issue
[#59](https://github.com/JunyiZhou-Conny/Explainer_Videos/issues/59)) on branch
`claude/funny-cannon-6at1kg`, the first portal episode in the 3Blue1Brown style (owner, 2026-10-30:
「以后用 3BLUE1BROWN STYLE PLEASE」). Verified facts and unclaimed reviews are kept separate.

## Content gates (AGENTS.md)

1. **Hook.** s01 opens on the owner's own screenshot, redrawn: 「正在思考 · 11 秒」 ticking, folding
   into 「思考了 22 秒 ›」, opening into 13.5 s of thinking and 8.7 s of writing; then the puzzle:
   "Thinking about what? … why does ours show you a clock, but never the thoughts?" ✔
2. **Intuition before formalism; an animated mechanism per core idea.** s02 a timeline from
   chain-of-thought prompting (2022) to the effort dial and our model menu; s03 the token tape: grey
   reasoning tokens slide behind a curtain, white answer tokens follow, the stopwatch splits at the
   first white token, the effort dial lengthens only the grey run, the usage report flows into the
   price; s04 two pipes side by side (words to the screen vs. words stopping at our server, progress
   lines going on) with the real event shapes driving the page's line; s05 a phone that cannot unsay
   a dose; s06 the form filling in order and the 911 flag firing at 3.5 s on a time axis; s07 a
   playhead replaying the checked answer, and the stop button cutting both links; s08 PR #41's 28
   real commit ticks; s09 three thinking panels side by side; s11 the whole path on one tape. No
   code on screen beyond the event shapes and field names. ✔
3. **Ponder moments and recap.** Two pause-and-ponder cards with a held pause (s03 "If the thoughts
   are hidden, what are you paying for, and how would you know?", answered by the usage report;
   s05 "Why not stream the words and pull them back?", answered by the screenshot), plus the hook
   question. s11 recaps the path and asks three test-yourself questions, each answered in the
   episode (stopwatch: s03; the urgency boxes first: s06; a summary must pass the checker: s10). ✔
4. **Written for the ear; anchored cues.** Field names and event shapes are shown, not read; risky
   words checked at the phoneme level (below); every reveal waits on a word anchor in the narration,
   and the build fails on a missing anchor. ✔
5. **Simulated-viewer QA over the full draft.** Findings and fixes below. ✔
6. **Measured checks + human review.** Measured values under *Verified*. Human review: **waived** by
   Conny (AGENTS.md, 2026-10-22): 「我大概率是不会进行审片的，因为我觉得做得已经非常好了，就让bugbot来检查就好了」.
   No human has listened to this cut. ✔ (waiver)

## Script review before scenes

- **Accuracy read against the code** (an independent agent, portal at `b7ab98e`): 12 findings, all
  fixed. Among them: decision 0006's verbatim line; the real NDJSON event shapes (`start`, `stage`
  with `attempt`, `progress`, `result`); "on Terra that first answer costs about five times as much"
  (from `pricing.ts` × the typical turn), not a made-up multiple; "any four consecutive characters"
  for the leak test; the developer-only switch is an open question, not a proposal; `followUp` in the
  form's order; the student wording of the early warning.
- **History read against the primary sources** (papers, OpenAI, DeepSeek and Anthropic pages, read
  2026-10-30): chain-of-thought prompting dates from January 2022 (Wei et al.) and "let's think step
  by step" from May 2022 (Kojima et al.), so the owner's "2–3 years ago there was no chain of
  thought" is corrected gently ("the idea is older than the apps"; what is new is showing it); o1's
  three stated reasons for hiding raw thoughts are quoted from OpenAI; Claude 4 summarizes long
  thinking (not all thinking); today's Claude API returns a summary only. Not verified and therefore
  not claimed: a "Thought for N seconds" label in ChatGPT, and DeepSeek's app showing the complete
  reasoning.

## Whole-video QA (first draft, 7:01)

Simulated target viewer (an independent agent playing Conny from the bilingual subtitles and a frame
every 3 s), plus my own frame-by-frame layout pass over the same contact sheets:

- [00:04–00:15, 06:21][CONFUSING] 「思考了 22 秒」 vs. 13.5 s of "thinking": two meanings of 思考. FIX:
  s01 now says the 22 seconds "is the whole wait" and "only 13.5 seconds of thinking"; the recap opens
  "So, thought for 22 seconds. First thinking: …" (checked: `ThinkingDone` rounds the whole turn's
  `elapsedMs`).
- [02:27][WRONG] The usage card (150 reasoning tokens of 1,000) undercut "most of the 13.5 s is hidden
  reasoning". FIX: the claim is gone ("the model reads the request, then reasons in hidden tokens");
  the card is labelled "the typical turn server.ts assumes for prices · reasoning varies", which is
  what `TYPICAL_TURN` is.
- [04:12][WRONG] The arrow ran 3.5 → 21 s on the axis but was labelled "≈ 20 s after". FIX: the answer
  is drawn at about 21 s after sending and the gap labelled "≈ 17 s sooner"; the narration says "at
  about 21 seconds". PR #41's 「约 21 秒后」 is ambiguous; SOURCES.md records why it is read as after
  sending.
- [03:51][CONFUSING] "Urgency first", but the list starts with `acuity` and `emergency` is fifth. FIX:
  the first five boxes carry Chinese glosses (紧急程度, 去哪里, 追问危险信号, 已有的危险信号, 紧急行动) and
  the narration says "the form's first five boxes are all about urgency"; recap question 2 follows.
- [00:15–01:31][MISSING] "Thinking about what?" had no example. FIX: s03 shows three lines of what the
  clinic question's hidden reasoning might say, tagged "illustration: the real thoughts are never
  sent to us"; it also sets up s09's "diagnostic guesses".
- [00:53–01:20][MISSING] Why show anything at all? FIX: s04 opens with decision 0006's reason,
  「干等 10–30 秒，人不知道在发生什么」, before the two kinds of streaming.
- [04:57, 06:13][CONFUSING] Terra and Luna, and "the model menu" as a pending decision, were never
  shown. FIX: s02 draws our model menu (Astra 最贵 · Sol · Terra · Luna 最便宜, 思考强度 低 / 中 / 高,
  from `MODEL_INFO` and the design doc) next to the effort dial.
- [02:09][WRONG] Equal-length 低 / 高 tapes implied that more thinking shortens the answer. FIX: the
  white answer run is the same length in both; only the grey run grows.
- [02:18–02:24, 03:25][SLOW] The 1.6 s vs 13.5 s comparison was dimmed at once, and the ponder cards
  left about 1.5 s of quiet. FIX: a 2 s hold before the ponder; each ponder now holds 3.5 s after the
  question (plus the card's 4 s timer).
- [05:18][SLOW] A blank screen under the episode's central question. FIX: the folded 「思考了 22 秒 ›」
  returns, then gives way to the three panels.
- [05:31][WRONG] Six things named, five bare labels shown. FIX: the rows carry glosses (过程 timings ·
  依据 sources · 检查 the check · 判断 judgment · 模型 model · price).
- [05:09][CONFUSING] The four-character test's purpose was unstated. FIX: "That test is the proof that
  no words reach the page before the checker has passed them" (decision 0006 lists it as such).
- [02:54–03:09][CONFUSING] "NDJSON" unexplained. FIX: 「每行一个 JSON」 under the arrow.
- [01:06][MISSING, not changed] DeepSeek's app showing 「已深度思考」 with the full text: not verified
  against a primary source, so the episode keeps to what DeepSeek's API docs say.
- [captions] 「举起一面旗」 → 「打上紧急标记」; 「播放出来」 → 「展示出来：句子逐字打出来，列表整块出现」.
  Long sentences still split into two cues where the engine divides them (known behaviour).
- [layout, frame pass] Timeline dates colliding (Jan/May 2022, Sep 2024/Jan 2025; labels now
  stacked); the stopwatch over the receipt's first row (moved to the screen's right end);
  「答案的第一个字到达」 over the billing note (the note leaves first, the label sits under the grey
  run); the greeting's two bar labels on top of each other (the write label goes to the right);
  "NDJSON: progress only" and "SSE: the words" running into the boxes (shorter labels, wider gaps);
  "≈ 20 s" under the answer label; "abort" over the model box; the s08 callout lines striking
  through their labels (now highlighted ticks with a legend); an orphan 「。」 on its own line (the
  wrapper no longer starts a line with closing punctuation); the 「pulled back: too late」 label over
  the phone's edge; a wrapped status quote. All fixed and re-linted.

## Verified (final render, 2026-10-30; ponder scenes re-rendered 2026-10-31)

- **Files**: `portal-e2-thinking.mp4` (clean) and `portal-e2-thinking.zh-en.mp4` (bilingual subtitles
  burned in) both decode in full with no error (`ffmpeg -v error -i … -f null -`, exit 0). 452.906 s
  (7:32.9), 1920×1080 at 60 fps, H.264 High, yuv420p; AAC-LC 48 kHz stereo. 27,169 / 27,170 video
  frames; 30.8 MB / 26.6 MB. S03 and S05 were re-rendered on 2026-10-31 after Bugbot found that the
  ponder card dropped its Chinese line (b78d2b6), and the cut restitched; the duration is unchanged.
- **Loudness** (EBU R128): −16.1 LUFS integrated, LRA 2.6 LU, true peak −1.1 dBTP, identical in both
  files (the burned copy's AAC stream has the same MD5, `72e1dc21…`). The build's mix report: voice
  −16.0 LUFS, music −32.84 LUFS under speech and −22.01 LUFS in the gaps.
- **Subtitles**: 135 English / 101 Chinese / 125 bilingual cues (`output/*.srt`, committed), numbered
  in order, never overlapping or empty, at most two lines, none shorter than 1.0 s; every bilingual cue
  has Chinese above English; the `.zh-en.ass` has the same 125 events. The last cue ends at 7:31.1,
  1.8 s before the end. `python -m explainer.i18n check videos/portal-e2-thinking --lang zh`: OK
  (sentence alignment, punctuation, spacing).
- **Layout**: `python -m explainer.check` reports no OUT, SMALL or missing-anchor problem in any of the
  11 scenes. Two 480p drafts were read frame by frame (a frame every 3 s); four burned 1080p frames
  were spot-checked (s01 receipt and stopwatch, s03 hidden tape, s06 axis, s08 commit ticks), with
  the picture above the subtitle band and nothing under it.
- **Narration**: 1,169 words (`python -m explainer.script`), Kokoro `af_heart` at 0.95.
- **Release preflight**: `tools/release_episode.py videos/portal-e2-thinking --preflight` passes
  (sign-off line, `publish:` block, no LaTeX needed).
- Every on-screen string copied from the product matches SOURCES.md, and every number there has a
  source. Rendered MP4s are not in git (release assets after merge).

## Not claimed

- **No human listened** to this cut or watched it through; the listen is waived (above). Prosody,
  pacing by ear and music balance by ear are unverified.
- **No ASR round trip**: no speech recognizer is installed here. The risky words were checked at the
  phoneme level instead (`phonemize`): o1, R1, DeepSeek, Claude 3.7, Claude 4, Terra, Luna, JSON,
  server-sent events, token, 911, 13.5 / 1.6 / 3.5 / 8.7 seconds, 320, 2022, 2024, "Let's think step
  by step"; all read as intended.
- The Chinese captions were checked by the viewer pass for meaning, not by a separate translator.
- The portal PRs (#36, #41) are open; the code may move after `b7ab98e`. Decision 0006 is still
  "proposed"; the video says so.
