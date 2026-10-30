# Review record: Isn't it just an API call? (项目周记 E1)

Produced 2026-10-30 by a Claude Code cloud session (issue
[#58](https://github.com/JunyiZhou-Conny/Explainer_Videos/issues/58)), on branch
`claude/funny-cannon-6at1kg` together with the series setup. Verified facts and unclaimed reviews
are kept separate.

## Content gates (AGENTS.md)

1. **Hook.** s01 opens on a real screen: one word in, three answers out (greeting, parent summary,
   receipt), and the question it raises ("an API call returns text; who decided on a parent
   summary, and who checked it?"). ✔
2. **Intuition before formalism; an animated mechanism per core idea.** s02 the server sliding in
   between page and model; s03 the request built as a stack with the cached prefix; s04 the 13-box
   form and its parent-summary box; s05 the two-try check flow with the fallback; s06 the receipt
   rows tied to their origins and the thinking/writing lane; s07 the 60 real commit ticks. No
   TypeScript on screen. ✔
3. **Ponder moments and recap.** Three pause-and-ponder questions with the frame dimmed and a held
   pause (s03 the clock, s05 why check again, s06 which row nothing checks), plus the hook question;
   s09 recaps the four jobs with three test-yourself questions, each answered in the episode. ✔
4. **Written for the ear; anchored cues.** Field names are shown, not read; numbers as digits only
   where Kokoro reads them right ("$5,550" read "dollar five thousand…", so "5,550 dollars"); "911"
   got a lexicon entry (it was read "nine hundred eleven"). Word anchors drive the reveals; the full
   build fails on a missing anchor. ✔
5. **Simulated-viewer QA over the full draft.** Findings and fixes below. ✔
6. **Measured checks + human review.** Measured values under *Verified*. Human review: **waived** by
   Conny (AGENTS.md, 2026-10-22): 「我大概率是不会进行审片的，因为我觉得做得已经非常好了，就让bugbot来检查就好了」.
   No human has listened to this cut. ✔ (waiver)

## Script review before scenes

- **Accuracy read** (an independent agent against the portal code at `b7ab98e`, the decision records
  and the week digest): 12 findings, all fixed. The ones that changed the story: the model is sent 89
  checked facts as `id：claim｜值：value`, not 97 cards with quotes; the six-arm evaluation was built
  but shelved before the comparison ran; only emergency → non-emergency is blocked ("an emergency is
  never taken back", not "urgency only goes up"); strict mode guarantees the parent-summary box
  exists, the `parent_summary` check rejects it empty; the process row is the page's stopwatch; the
  conversation so far precedes the context in the request; "gets it right every time" became "the
  same way every time, 'to be confirmed' when it cannot know".

## Whole-video QA (first full cut, 9:06)

Simulated target viewer (an independent agent playing Conny, from the bilingual captions and a
frame every 5 s), then a frame-by-frame layout pass:

- [05:31][WRONG] The thinking row was explained only as a stopwatch, so "thinking" sounded cosmetic,
  though it was his first question. FIX: s06 now says Luna is a reasoning model that reasons in
  hidden, billed steps, that the menu's effort setting (思考强度) sets how much, and that the page
  times thinking until the first word arrives; drawn as a lane with the greeting's real 1.6 s / 1.5 s.
- [05:40][WRONG] "One of the five rows is never read by any check" was false (process and model are
  not checked either) and had no pause. FIX: "two of the five rows are the model's own words; the
  checker reads one; which one does nothing ever check?", a held pause, then the answer.
- [00:33, 03:05][CONFUSING] "Not one call" plus a separate form job suggested a second call for the
  parent summary. FIX: s02 retitled "More than a call"; s04 says it is still one call returning text
  shaped like the form, one call fills all 13 boxes.
- [01:42][CONFUSING] Why "first" matters for caching was not said, yet the recap asked it. FIX:
  "OpenAI's cache matches a request from its very first word" (checked against OpenAI's prompt-caching
  guide, see SOURCES.md).
- [04:37][CONFUSING] The never-downgrade rule had no reason, yet the recap asked it. FIX: "a rewrite
  should fix what the checker flagged, not change its mind about danger; if we must be wrong, we'd
  rather be wrong toward 911".
- [07:42][WRONG impression] The comparison implied our app has no system prompt. FIX: s03 names the
  fixed top "the instructions … chat apps call them the system prompt"; s08 "ours has a system prompt
  too, and adds…".
- [08:06][WRONG-ish] "A flag that says a person should look" needs a receiver the prototype lacks.
  FIX: dropped; two examples remain.
- [pacing] Ponder gaps were 0.3–1.4 s while scene tails idled 6–11 s. FIX: the scenes' `pause()`
  spends the slack after each question.
- [terms] "token" glossed in s03; "SHS" glossed on screen as 学校医疗中心 SHS; "the look was borrowed
  from Claude's app on purpose, that is episode three" added (his "what did we copy" question).
- [layout, frame pass] Fact-card text overlapping (s03); a stamp covering the urgency list (s04); the
  LINT label on the gate edge (s05); labels overlapping receipt rows (s06, twice); the 21:21 and
  40-commit labels over the title line (s07); crowded proposed rows (s08); `Indicate` painting filled
  boxes solid red (s03–s05, s08, replaced by an outline sweep); the s02 on-screen title not following
  the script (headers now come from `script.json`). All fixed and re-rendered.

## Verified (final render)

- 584.085 s (9:44), 1920×1080 @30 fps H.264 + AAC; the whole file decodes without error
  (`ffmpeg -v error -i … -f null -`); 144 bilingual cues; validation sidecar in `delivery/`, made
  from the committed `script.json` (`script_sha256` 20c705d9…).
- 1,487 narration words; 538.2 s of speech (Kokoro `af_heart`, 0.95), measured by `--prepare-only`.
- Composed score under the narration: voice −16.03 LUFS, music −22.03 LUFS in gaps / −32.65 under
  speech, mix −16.29 LUFS, true peak −0.97 dBTP, nothing dropped in silences. Score coverage is 0.76
  (the reference episode has 0.96): the held ponder pauses are partly silent by design; unheard.
- Swiss pixel style check passed on sampled frames of the clean render (background dominance,
  caption band clear); `explainer.check` reports no OUT, SMALL or BAND problem in any of the nine
  scenes and no missing voice anchor.
- Every on-screen string copied from the product matches SOURCES.md; every number is listed there
  with its source.
- Rendered MP4s are not in git (release assets after merge, `docs/PUBLISHING.md`).

## Not claimed

- **No human listened** to this cut or watched it through; the listen is waived (above). Prosody,
  pacing by ear and music balance by ear are unverified.
- **No ASR round trip**: no speech recognizer is installed in this environment. Instead the risky
  words were checked at the phoneme level (`phonemize`): 911 (fixed by a lexicon entry), JSON, lint,
  harness, Luna, Claude Code, 25,000, 89, 13, 36, 60, "5,550 dollars".
- The Chinese captions were checked by the viewer pass for meaning, not by a separate translator.
  Known engine behaviour not changed here: a few cues split an English sentence where the Chinese is
  not split, and a stray space can appear after 。 when a long Chinese line is divided.
- The portal PRs (#36, #41) are open; the code may move after `b7ab98e`. Decisions 0004 and 0006 are
  still "proposed"; the video says so for 0004.
