# Review record: AC215 · Lecture 8 — LLM: Finetuning

Follow-along of [dlops-io/llm-finetuning](https://github.com/dlops-io/llm-finetuning) `main` @ `44ef6f0` (the whole
README: Prerequisites, Generate Question Answer Dataset, Fine-tune Gemini) and the course Colab "Tutorial - Finetuning
with QLoRA" (Part A setup, Part B the "Q" in QLoRA, Part C steps 1–6; saved outputs only). The issue of record is
Explainer_Videos#68. Claude Code cloud sessions (Claude) produced it. Verified facts and unclaimed reviews are kept in
separate sections.

- **Captures:** 2026-10-31, 02:35–02:37 UTC, on a fresh "laptop" with Docker Engine 29.8.2 and the tutorial's two
  images, **without a service-account key and without a GPU** (`ASSETS.md`).
- **QA draft:** the 480p draft (32:38, parts 17:05 + 15:32), committed in `e7ddece` (2026-10-31 10:32 UTC).
- **Whole-video QA** (`/root/ac215-backup/tasks/wkdm8p7wi.output`, key `result`): seven watchers on that draft,
  14 scene fixers (every scene but S06 and S15), one narration/subtitle fixer, and a verifier for each of the 16
  scenes. Committed in `2678243` (2026-11-01 05:40 UTC).
- **Finishing pass** (`/root/ac215-backup/tasks/wekfpq4lq.output`): a plan, one text agent (the plan's 14
  text items, all applied; the agent's own report says "13"), and five scene entries (S06, S07, S10, S14, S16), each with a verifier. Committed in `2f9178e` (06:25 UTC).
- **1080p60 renders:** all 16 scenes, render logs `build/logs/` dated 2026-11-01 06:28–07:01 UTC; none contains
  "anchor not found".
- **Final cut:** 33:29.75, parts 17:27.33 + 16:02.52; committed in `73928e7` (07:42 UTC).
- **Final-cut checks:** five agent checks on 2026-11-01. The coordinator saved their returned text as
  `build/final-review/report-{tags,asr,visual,pairs,measured}.md`. All five reports exist and were read in full for
  this record. No blocking defect except the pairs report's two "must" items.
- **Fix round** (`648a0ad` 08:13 UTC, `6b88321` 08:40 UTC): six Chinese cue pairs re-ordered in
  `i18n/zh/narration/g1.yaml` and `g2.yaml` to follow the English clause order; subtitles regenerated; the cut
  re-stitched with `--burn`. Picture and audio unchanged. **This record describes the cut at `6b88321`.**
- **Coordinator decision (2026-11-01):** accepted for release; every remaining finding is listed below under
  "Accepted items" with its reason.

**Conventions:**
- **Times** are mm:ss in the full cut (`output/ac215-l08-llm-finetuning.mp4`, 33:29.75), except in "Whole-video QA",
  which keeps the 480p draft's times (marked *draft*).
- **Cue numbers** name their file: `.srt` (521 cues), `.zh.srt` (435) or `.zh-en.srt` (513). The five checks ran on
  `73928e7`, where `.zh.srt` had 436 cues and `.zh-en.srt` 514; zh-en cue numbers in their reports after old cue 355
  are one higher than today's (see "Fix round").
- **Evidence paths** are relative to `build/final-review/`, which is git-ignored and exists only in the producing
  session. A successor re-runs the checks to reproduce it.

## Content gates (AGENTS.md)

1. **Hook** ✔. S01 opens on a broken thing from the staff's saved Colab run, not on a value proposition.
   - "Why is the sky blue?" (cue 1, 00:00.0) goes to two versions of Qwen3-0.6B: as downloaded and fine-tuned. The
     fine-tuned one "opens with a cheesy greeting in the instructor's voice" (cue 5, 00:11.5).
   - "Both are wrong: air molecules scatter blue light more than red." (cue 9, 00:22.7) and "The voice changed
     completely; the facts did not get better." (cue 10, 00:26.7).
   - The question the video answers: "So what did it learn, and what didn't it?" (cue 16, 00:51.0).
   - **Payoff:** "And the sky: the voice transferred, the physics did not." (cue 480, 30:40.5), restated in the recap:
     "fine-tuning changes the weights, and here it taught a voice, not facts." (cue 509, 32:32.6).
2. **Intuition before formalism, with an animated mechanism for each core idea** ✔. `BRIEF.md` ("Visual set
   pieces") defines eight; each is animated with the commands or cells it explains:
   - **V1, three dials (S02, S15):** prompt / context / weights on one model box (from 01:43); OPT-350m against an
     instruction-tuned model against the fine-tuned Qwen (lecture tag 4, 02:16–03:04); in S15 the weights dial
     becomes the `disable_adapter()` switch (29:46.6, lecture tag 29).
   - **V2, the stage (S03, S04, S07–S09):** laptop, two TEAL containers from one recipe, PINK bind mounts, the BLUE
     cloud with its `global`, bucket, `us-central1` and `us` pins; each Track A command lights its route and stops at
     the RED "no key" wall.
   - **V3, teacher, mould and bricks (S05–S06):** the lecture's three-part card fades to the two-part brick (07:06–
     07:24, lecture tag 5); the no-key net catches five errors with exit code 0, and the `KeyError` lands one command
     later (S06, from 09:29); `drop_duplicates` strikes the 20th brick (cue 183, 10:53.9).
   - **V4, one pair, five shapes (S07, S12):** CSV row → `human:`/`bot:` → Gemini JSONL on a conveyor (11:12.8,
     lecture tag 7), the 17 / 2 split (cue 200, 12:02.7); Qwen's chat template as a ribbon (S12, 23:32.8) and
     integers with "loss on every token" (24:01–24:06).
   - **V5, the memory column (S10, S14, S16):** 10 B → 120 GB (18:30.8), ≈40 GB LoRA (19:08.2), ≈12 GB QLoRA
     (19:21.4); the Qwen-sized `estimate` column (26:55.5); the 120 → 40 → 12 ladder in the recap (32:47.7).
   - **V6, buckets (S11, 19:31–21:35):** 27 / 55.3 / 83.78 into fine and coarse buckets; absmax rows to Int8 and back
     with the dequantization error (19:59–20:52); NF4's 16 quantile levels on a bell curve (20:52–21:17); stored in
     NF4, computed in FP16 (21:17–21:35).
   - **V7, the LoRA block diagram (S13, S14, S16):** a 5×5 grid at ranks 1 and 2, then `q_proj` at real size against
     two rank-8 strips (24:29.7–25:08.8); `W₀ + (α/r)·B·A` (25:08.8); the block diagram and the 28-layer count to
     1,146,880 (25:19.9–25:52.7); the backward pass through a frozen W₀ (28:36.8); the merge into a fresh FP16 W₀
     (31:26.7).
   - **V8, memory under pressure (S14):** the checkpointing chain (27:18.8), GPU ↔ CPU paging (27:49.6), FP32 / FP16
     / BF16 bit strips (27:59.3).

   **Lecture slides:** a GREY "Lecture 8 · slide(s) …" tag top right in 13 of the 16 scenes (none in S03, S04 and
   S09, whose `script.md`
   headers say `Lecture: none.`): 34 `lecture_ref` tags, one of them S01's specimen in the layout
   preview (01:10.0–01:19.5, the real "7–8", by design). The slides are redrawn, never shown. The tags check found
   every tag, no overlap, no tag left at a scene end, and a whole-cut 4 fps sweep of the top-right corner with 0
   mismatches in 8,039 samples (`report-tags.md`, `tags/scan_result.txt`). Five tags arrive well before or leave
   well after their picture (notes N1–N3; accepted, item A1). `SLIDES.md` maps the chapters to the deck; its "This
   video and the slides" section predates the script and marks no proposal "do" (finishing plan).
3. **Pause-and-ponder moments and a recap** ✔, by Conny's decision for the series: five ponders against AGENTS.md's
   aim of one every 2 minutes.
   - **Ponders:** five cards (`script.md` lines 514, 701, 789, 885, 973), each followed by an 8 s silent timer; the
     answer is said right after the timer (`measured.json` "content_gates", `.srt`):

     | scene | question (condensed) | card | timer ends, answer starts |
     |---|---|---|---|
     | S05 | The teacher gets a pH value wrong: what happens to it after fine-tuning? | 09:08.6 | 09:17.2 "It becomes a training target." |
     | S08 | `--train` returns after a minute: where is the training, and what would deleting the container lose? | 15:24.6 | 15:33.2 "On Google's hardware in us-central1, reading your bucket directly." |
     | S10 | Full fine-tuning: what else sits in GPU memory, and how much? | 18:40.4 | 18:49.0 "The gradients, one per weight, take another 20 gigabytes." |
     | S12 | 596 million parameters: why does the notebook count 375.8 million? | 22:33.5 | 22:42.1 "The 440 million weights in linear layers are packed two 4-bit values to a byte," |
     | S13 | How many trainable parameters at r = 16, and at r = 8 on all seven ("all-linear")? | 26:22.0 | 26:30.6 "Rank 16 doubles it, to 2,293,760." |

   - **Rate:** 5 in 33:29.75, one per 6.7 min (0.149 per min; the gate's aim would be about 17). The longest stretches
     without one are 00:00–09:08.6 (about 9.1 min) and from the last timer's end (26:30.6) to the end (about 7.0 min).
     `BRIEF.md` ("Ponder questions") plans exactly five.
   - **Decided by Conny (2026-10-21), as recorded in `videos/ac215-l05-rag/REVIEW.md` gate 3:**
     「我觉得可以保留现在的密度」: keep the current density of 3–5 ponders per lecture, plus a spoken recap and
     test questions.
   - **Recap** ✔: S16 (from 31:07.5) ships and tears down, then "Here's where we are." (cue 507, 32:28.7): prompts and
     retrieval vs weights, voice not facts, track A, track B and the 120 → 40 → 12 ladder; "Five questions to test
     yourself." (cue 513, 32:54.4; answers in `exercises.md`); then lectures 9 and 10 (cue 519, 33:17.3).
4. **Narration written for the ear, with word-anchored cues** ✔.
   - **Spoken style:** `script.md`'s conventions (1–3 sentences per SAY, about 60 words at most; commands and paths
     said in words; money in words; "at the time of recording" for versions; the persona never named).
   - **Size:** 119 SAY lines, matching the 119 voice blocks in the render sidecars; 4,366 words. Kokoro `af_heart` at
     speed 0.9: 130.3 wpm over the runtime, 141.4 wpm over the 1,852.9 s of voice (92.2 % of the runtime).
   - **Anchors:** 627 `vo.wait_until(...)` calls across the 16 scene files (S01–S16: 33, 20, 42, 40, 41, 38, 34,
     47, 37, 33, 54, 40, 42, 41, 42, 43). None of the 16 render logs contains "anchor not found".
   - **Ear fixes after the draft:** the QA narration fixer renamed the Colab steps by the notebook's own section
     numbers (the must, below) and added L08-only lexicon keys for them ("4.2" … "6.3"; Kokoro had read "4.3 builds"
     as "four. three"), for "llm-finetune-dataset-small", "dataset section", "dataset-creator", "the pretrained one".
     The finishing pass added "a torchao" (read "a" as the letter A before a lexicon word) and "test.jsonl", and
     reworded three narration nits (S06 "Drop duplicates on line 233 removed it.", S07 "17 examples in train.jsonl,
     2 in test.jsonl", S14 "cannot handle" for "cannot unscale").
   - **Final ASR** (`report-asr.md`): no mispronunciation or swallowed word; no cue's speech starts more than 1 s late
     (latest: cue 413 at 26:02.2, 0.571 s).
5. **Simulated-target-viewer QA over the full draft** ✔.
   - Seven watchers reviewed the 480p draft: two directors (one per part), two simulated target viewers ("newcomer",
     one per part), a subtitle watcher, a follow-ups watcher and an ASR watcher. The newcomers worked from contact
     sheets, exact frames, the English `.srt`, the README and the notebook cells.
   - **68 timestamped findings: 3 must, 33 should, 32 nit.** All three musts (newcomer, part 2) are fixed. Every
     should is fixed except two, both under "Still open": S13's "about 1 percent" (narration half declined) and the
     English `.srt` line breaker (shared, deferred to a toolkit PR). One should fix did not hold: the S10 *draft*
     17:21 torchao pairing was applied in the QA round but the final-cut pairs check found the same split again (old
     cues 293/294); the fix round corrected it. Each scene's fixes were checked by a verifier, on fresh preview or
     720p frames for picture changes; subtitle-only fixes were checked with the i18n check or a simulated cue split.
     Details under "Whole-video QA".
6. **Measured checks** ✔. The numbers are under "Verified" (`measured.json`, measured on `73928e7`; the burned copy
   re-checked after the fix round).
   - **Duration:** 33:29.75 (2009.754 s), inside the series' 25–35 min; parts 17:27.33 (1047.333 s) and 16:02.52
     (962.524 s), whose container durations sum to 0.103 s more than the full cut (within ±0.5 s); the video streams
     sum to the full cut's 2009.733 s exactly.
   - **Loudness:** −16.0 LUFS integrated (clean cut and zh-en), −16.1 LUFS (both parts); LRA 2.4–2.5 LU; true peak
     −2.8 dBTP in all four. That meets the toolkit's −16 LUFS target with peaks under −1.5 dBTP.
   - **Caption bounds:** in the burned copy the picture is scaled to about 87 % in the top ~935 px and the subtitles
     sit at about y 985–1075, so they cannot cover scene content. Every event is exactly two lines, Chinese (50 px)
     above English (33 px); wrapping is off (`WrapStyle: 2`); the widest line measured 1,500 px against 1,840 px
     available on `73928e7` (`report-visual.md`; old cue 33 at 01:57, shortened in the fix round). In today's
     `.zh-en.ass` the widest lines are 1,474 px (English, 29:57) and 1,450 px (Chinese, 02:40), measured with the
     style's Noto Sans CJK SC at 50 / 33 px.
   - **Music balance:** does not apply. L08, like L02–L07, has no score: `video.yaml` has no `music:` key.
   - **Subtitle sync:** every cue's narration starts within 0.571 s of the cue (`onset-vad.json`, 709 speech regions);
     the five long silences (8.99–9.12 s) are the five ponder timers.

   **Human review:** the series waiver stands in for a listening sign-off.

   Listening sign-off: waived by Conny for the AC215 series (Explainer_Videos#29, 2026-10-15): 「不需要，我现在对视频质量很满意的」 — no human listened to this cut; the ASR round trip below is the substitute.
   Review moments optional since 2026-10-22 (AGENTS.md): 「我大概率是不会进行审片的，因为我觉得做得已经非常好了，就让bugbot来检查就好了」

   **ASR round trip** (`report-asr.md`): faster-whisper base.en over the whole clean cut (521 cues compared, 4,588
   words recognised, 241 cues with some difference, mean word ratio 0.916; `asr.json`, `asr.log`); large-v3-turbo on
   47 doubtful windows covering 64 cues (`asr-recheck-large.json`); speech onsets over the full audio
   (`onset-vad.json`). Every difference is recogniser noise: words placed in the neighbouring cue (all heard in order
   by large-v3-turbo), numbers as words, identifiers, possessives, and names it cannot know (Qwen, LoRA, PEFT, NF4).
   Six homophones heard the same way by both models (cues 3, 69, 105, 164, 288, 499) change no meaning in context.
   No real name in any transcript; all 11 cues that say "the instructor" were recognised as such.

## Whole-video QA (480p draft `e7ddece`, 2026-10-31/11-01; times are *draft* times)

**Watchers and findings** (`wkdm8p7wi.output`, key `result`; the run log reads "L08: 68 issues from 7/7 watchers"):

| watcher | must | should | nit |
|---|---|---|---|
| director, part 1 | 0 | 7 | 3 |
| newcomer, part 1 | 0 | 5 | 5 |
| director, part 2 | 0 | 5 | 9 |
| newcomer, part 2 | 3 | 4 | 3 |
| subtitles | 0 | 11 | 9 |
| follow-ups | 0 | 0 | 0 |
| ASR | 0 | 1 | 3 |
| **total** | **3** | **33** | **32** |

By target: 34 scene, 19 subtitles, 14 narration, 1 shared (the toolkit's English line breaker). By kind: 19
subtitle, 16 follow-along, 10 text, 8 pacing, 5 sync, 4 picture, 2 fact, 2 lexicon, 1 narration, 1 continuity. The
follow-ups watcher found no `QA_FOLLOWUPS.md` (L08 had none yet) and no review-bot comment on any L08 file (the newest
bot reviews on the series PR, 2026-10-20, predate L08's scenes); it read the scene code for the series' recurring
snap-back defect instead and reported nothing.

**The three musts, and how each was fixed.**
- **M1, *draft* 17:05, S10: no way to open the notebook.** Part 2 said "the course Colab" but never where it is, and
  the README has no Colab link. **Fix:** a GREY two-row chip under the Colab title ("open it from the L08 Ed lesson" +
  the notebook URL; `s10_memory.py`, QA round) and, in the finishing pass, the spoken sentence "Open it from the
  lecture's Ed lesson; the link is on screen." (cue 287, 17:32.4) with its zh line; the chip now fades in on that
  sentence (finishing S10 entry, verified on frames at scene 5.0 / 6.3 / 8.0 s).
- **M2, *draft* 26:54, S14–S16: the narration numbered steps by the tracker, not the notebook's headings.** "Step 2,
  the training arguments", "Step 5, TensorBoard", "Step 1 measures it" pointed to the wrong cells. **Fix** (narration
  fixer): "Section 4.2, the training arguments" (cue 434, 27:32.5), "4.3 builds the trainer" (cue 445, 28:15.1),
  "4.4, train", "And 4.5, TensorBoard", "Section 5.1 measures it", "5.2 compares answers", "Pause, and run section 5",
  "Section 6.3 can push…" (cue 496, 31:50.5); anchors moved in `s14_train.py` and `s15_eval.py`; lexicon keys for the
  section numbers.
- **M3, *draft* 22:45, S12: the fallback chip led to an error.** "…or use your own train.jsonl from part 1" would
  feed 17 rows to `df.sample(n=1000)` (`ValueError`). **Fix:** the chip reads "Too many users …? retry the gdown cell
  later" (`s12_qwen.py:429`); `script.md`'s SHOW line updated in the finishing pass.

**The shoulds, examples by kind** (all fixed and verified, except the two under "Still open"; the
S10 torchao pairing needed the fix round, see above):
- **On screen too briefly:** S03 commit output held; S07 extra `ls -la data; wc` strip; S08 "identical" chips; S12
  openers note; S13 the ratio "24,576 / 2,097,152 ≈ 1.2 %" now held about 2.5 s with a flash.
- **Sync and pacing:** S05 dead stretch at *draft* 08:08 and the "enthusiastic exclamations" line; S07 the
  "code's comment" sentence now over its code; S10 GOLD "A100 · L4" chip; S16 torchao chip on its own sentence.
- **Follow-along gaps:** S03 the `gcloud services enable` / bucket card with `--project=<your-project>`; S08 "keep
  the folder, llm-finetune-dataset-small"; S08 "Before you pause, watch the cost table…"; S10 the Hugging Face token
  steps (a GREY huggingface.co › Settings › Access Tokens chip and the spoken path); S11 "Section 1 also tokenizes";
  S12 "Part C, step 1" named; S16 "If the merge raises a torchao import error, rerun the install cell and restart
  the session." (cue 494, 31:42.1).
- **Subtitles:** 15 zh rewrites in `g1.yaml`/`g2.yaml` (cross-paired clauses at *draft* 05:35, 17:21, 27:22; cuts
  inside verb phrases; the 列 ambiguity; breaks inside `prepare model / for k-bit training`, `2048 乘 / 1024`,
  `Tuned model info: / None`), lower-case cue starts, the serving location `US` → `us`, kept-English lines for
  "Sure, here's", "The" and the notebook title.
- **Narration:** S06's command made its own sentence ("Type python cli.py dash dash prepare."), so the cue no longer
  lags the voice.

**Nits:** fixed in the QA round or in the finishing pass (the three narration nits above, the S14 and S16 `▶ your
turn` tags without a spoken pause, the S13 ponder card's "all seven ("all-linear")", `script.md` SHOW and PONDER
lines for S03, S07, S11, S12, S13, S14 and S16, glossary rows A10, S03 first_use and D6), except those listed next.

**Still open after QA and the finishing pass, and why:**
- **English `.srt` line breaker splits artifacts** (subtitles, should, shared): `docker ps` / `-a` (13:08),
  `source:` / `not found` (05:11), `KeyError:` / `'question'` (09:40) in the English `.srt` (the burned bilingual band
  keeps each on one line). A toolkit change in `explainer/subtitles.py`, deferred to its own toolkit PR (AGENTS.md
  split); recorded in `QA_FOLLOWUPS.md`.
- **S13 "about 1 percent of the matrix" not spoken** (should, narration half): the picture half is fixed (ratio held
  and flashed); the finishing plan declined the added sentence because `script.md` says later changes trim, not add.
- **S11's small Colab chip is not repeated in S13–S16** (nit, continuity): needs `mini_colab()` moved to
  `scenes/common.py` and placed in four scenes; out of scope for minimal changes.
- **S04 tracker numbering vs the README's three steps** (nit): the "README's step 3" suffix was judged consistent;
  renumbering would touch `common.py`, SAY, zh and BRIEF.
- **S12 `SECTIONS['Qwen']` step 1 name in `common.py`** (optional cleanup): the scene-local override already shows
  "1.2–1.3 Load".
- **Noticed by the QA or finishing-pass agents, not changed:** S10 still shows the older GREY chip "SecretNotFoundError?
  name it HF_TOKEN · turn notebook access on" beside the new Access Tokens chip (about 18:10; both readable, left to
  the coordinator); S14's last two loss values overlap for one transition frame as they move to the chart (about
  29:02); S16 recap question 5 on screen ("…and what does QLoRA keep in GPU memory here?") is longer than the spoken
  "And where does 1,146,880 come from?" (cue 518, 33:09.0; reported by the QA S16 verifier, skipped in the finishing
  plan because the on-screen clause is SLIDES.md's recap proposal);
  S06's `▶ your turn` tag briefly touches a card border while fading in; brief mid-transition overlaps in S10.

## Final-cut checks (1080p60, `73928e7`, 2026-11-01)

- **Tags** (`report-tags.md`): no blocking defect. 34 tags, each with four frames (in, mid, before, after) and a
  contact sheet (`tags/`); whole-cut 4 fps corner sweep, 0 mismatches outside ±0.6 s of each fade; wording "slide N" /
  "slides …" correct; no real name in 136 frames. Timing notes N1–N4: item A1.
- **ASR** (`report-asr.md`): intelligible throughout, no real problem; one caption/narration wording difference
  (item A3).
- **Visual** (`report-visual.md`): 670 frames of the burned copy on 42 sheets (one every 3 s) plus targeted frames
  and strips. No clipped or garbled text, nothing off-frame, no stuck tag, no black or missing scene, no real
  instructor name; every scene ends on an empty frame (peak brightness 14/255). Four cosmetic notes: item A2.
- **Pairs** (`report-pairs.md`): all 514 bilingual cues read. Structure passes (two lines per cue, zh above en, no
  command broken inside a cue, timings increasing, en lines equal the `.srt`, part files equal the full file, no
  real name). **Two must-fix pairs** (swapped meaning: cues 352/353 and 471/472) and **four boundary shifts** (354/355,
  33/34, 293/294, 454/455): fixed in the fix round below.
- **Measured** (`report-measured.md`, `measured.json`): all four MP4s decode with 0 errors; formats, loudness,
  subtitles, chapters, part split and name scan pass. Notes: item A5; the ponder rate is decided under gate 3.

## Fix round (`648a0ad`, `6b88321`) and its verification

Six Chinese cue pairs re-ordered to follow the English clause order; subtitles regenerated and the cut re-stitched
with `--burn`. Checked for this record against the current files (`output/ac215-l08-llm-finetuning.zh-en.srt`, cues
by today's numbers) and on frames of the burned copy (`writer/pairs_sheet.png`, crops `writer/frames/pair_*.png`):

| old cues (`73928e7`) | now | time | zh now | en | result |
|---|---|---|---|---|---|
| 352 / 353 (swapped meaning) | 352 / 353 | 22:06.1 / 22:09.7 | 「Part C 的第 1 步加载真正的学生模型」 / 「Qwen3 0.6B，用的是同样的 4 位配方」 | "Part C, step 1, loads the real student," / "Qwen3 0.6B, with the same 4-bit recipe." | ✔ each zh line says its en line |
| 471 / 472 (swapped meaning; 472 had no Chinese) | 470 / 471 | 30:33.7 / 30:37.5 | 「两个奶酪问题的回答现在都以 welcome welcome welcome」 / 「cheese lovers 开头，用的是授课老师的口吻」 | "Both cheese answers now open with welcome welcome welcome," / "cheese lovers, in the instructor's voice." | ✔ both lines now carry Chinese; 471 opens on the kept-English quote (item A4) |
| 354 / 355 (boundary) | 354 / 355 | 22:13.6 / 22:17.2 | 「接着 prepare model for k-bit training 冻结所有权重」 / 「并打开梯度检查点，这是一个省显存的技巧，训练那一章会讲」 | "Then prepare_model_for_kbit_training freezes every weight" / "and turns on gradient checkpointing, a memory trick the training chapter shows." | ✔ "freezes every weight" in both 354 lines |
| 33 / 34 (boundary) | 33 / 34 | 01:57.0 / 02:00.8 | 「微调转的是第三个旋钮：它改的是权重，办法是给模型看」 / 「大量由一个输入和你想要的输出组成的例子」 | "Fine-tuning turns the third dial: it changes the weights," / "by showing the model many examples of an input and the output you want." | ✔ "many examples" in both 34 lines |
| 293 / 294 (boundary) | 293 / 294 / 295 | 17:48.4 / 17:52.2 / 17:55.7 | 「第 3 节 pin 住 transformers、bitsandbytes 和 trl」 / 「并卸载 torchao，notebook 里说」 / 「有它在的话 peft 不肯添加 LoRA 层」 | "Section 3 pins transformers, bitsandbytes and trl," / "and removes torchao, which, the notebook notes," / "makes peft refuse to add LoRA layers." | ✔ "removes" in both 294 lines; the old 1.3 s cue 294 is now 3.5 s |
| 454 / 455 (boundary) | 453 / 454 | 29:20.7 / 29:24.3 | 「困惑度就是平均每个 token 的 loss 取指数」 / 「大致相当于模型在多少个等可能的下一个 token 里做选择」 | "Perplexity is the exponential of the average token loss:" / "roughly how many equally likely next tokens the model is choosing among." | ✔ "roughly" opens both 454 lines |

- **Counts:** `.zh-en.srt` 514 → 513 (old 355/356 merged into today's 355); `.zh.srt` 436 → 435; part 2 `.zh-en.srt`
  228 → 227, `.zh.srt` 194 → 193; part 1 cue counts (286 / 242) and every English `.srt` unchanged (part 1's `.zh-en.srt`,
  `.zh.srt` and `.ass` differ from `73928e7` only at the 33/34 pair). The `.zh-en.ass` files hold 513,
  286 and 227 events.
- **Nothing else moved:** a cue-by-cue diff of `.zh-en.srt` against `73928e7` shows only these five replaced
  ranges. The English `.srt` (521 cues) and both part `.srt` files equal `73928e7`'s in timings and text. In the
  current `.zh-en.srt` every cue has two lines, no cue is shorter than 1.000 s, none overlap, the last ends at
  2006.398 s, and the English lines joined equal the English `.srt`.
- **The burned copy:** `ac215-l08-llm-finetuning.zh-en.mp4` re-burned (110,067,149 bytes, 105.0 MiB; was
  110,063,837): 2009.750 s, 120,585 frames at 60 fps, as measured before. A full decode (`ffmpeg -v error`) exited 0
  with no output (`writer/decode_zh-en_rebuilt.log`). Its audio stream is bit-identical to the clean cut's (MD5
  `4d0e6ab0…`), so the clean cut's loudness holds for it. The clean MP4 and both part MP4s have the same byte sizes and
  durations as in `measured.json`.

## Accepted items (coordinator decision, 2026-11-01)

- **A1. Tag timing notes N1–N4 (by the script's rule).** `script.md` makes a tag run "from that SAY block on, until a
  SHOW changes it", so these follow the script, though not the stricter "only over its picture":
  - N1: S02 "slides 7–8" stays 18.2 s after its three-row picture clears (02:45.5 → 03:03.7).
  - N2: S05 "slides 4–5" stays 18.4 s over the V3 teacher (07:24.2 → 07:42.6); `SLIDES.md` maps the whole persona
    chapter to 4–5.
  - N3: tags that arrive before their picture: S12 "slide 8" (23:52.2; picture at 24:01–24:06, about 9 s later), S15
    "slide 40" (30:48.9; bars grow at 30:57.4, +8.5 s), S16 "slides 41, 71–72" (32:29.3; strips at 32:41.7, ladder at
    32:47.7; the SHOW line says 71–72 only, the code adds 41).
  - N4: small leads, S10 "slides 11–16" (+2.8 s, while "the lecture's question" is spoken) and S15 "slide 36"
    (+3.7 s).
  - Observations: S11's tags share the top row with the "QLoRA notebook · Colab" chip about 130 px apart; S12's
    Colab chips sit 14 px below the tag; S06's tag and in-body chip both cite slide 5 (the script asks for the chip).
- **A2. Visual notes (cosmetic, no re-render).**
  - 08:14.4–08:14.9 (S05, about 0.4 s): the enlarging highlight on "enthusiastic exclamations" covers the spaces
    ("Incorporateenthusiastic exclamationsand phrases"); normal from 08:15.0.
  - 04:43 (S03): the yellow `<your-project>` chip touches the "=" in `--project=`; readable.
  - Mid-animation overlaps that clear within about 1 s: 11:41–11:43, 18:24, 22:42, 30:20.5–30:24.5, 32:24.
  - Static holds over 4 s with narration and changing subtitles over them: 12:05.4–12:10.9 (5.5 s), 12:12–12:16.5,
    31:44–31:48.5 (4.5 s each), 18:02.6, 28:32.2 and about 28:56 (4.0 s each). Of 67 freezedetect stretches, 13 were
    measured at 2 fps; 54 were not.
- **A3. ASR minor items (wording, not defects).** Six homophones heard the same way by both models (cue 3 00:05
  "course staff's", 69 03:58 "and name it", 105 06:07 "Ours", 164 09:52 "except", 288 17:36 "in Drive", 499 32:02
  "endpoint"); the report names cues 3 and 105 as the ones worth hearing if a human listens. Cues 294–295 (17:58–
  18:11, `.srt` numbering of `73928e7`): the English caption shows the written forms `huggingface.co` and `HF_TOKEN`
  where the narration says "the Hugging Face website" and "HF token" (`en_display`, as for W₀ and α/r).
- **A4. Cue 471 opens on a lower-case kept-English quote** (`.zh-en.srt` 471, 30:37.5, 「cheese lovers 开头，…」).
  Glossary A5 forbids a sentence opening on a lower-case kept-English word, "so no subtitle starts in lower case";
  this cue is the second half of one sentence, but it is a subtitle that starts in lower case. The words are the
  model's printed opener, kept as printed (A10). The same pattern, a sentence continuing on a
  kept-English artifact, is already in cues 128, 225, 232 and 371. `.zh-en.srt` cue 288 (17:29.8) keeps the
  notebook's title "Tutorial - Finetuning with QLoRA" on the Chinese line (A10).
- **A5. Measured notes (harmless).** The zh-en video stream is one frame (17 ms) longer than the clean cut's; `.zh.srt`
  drops or adds line-end punctuation where the bilingual layout breaks lines (text otherwise identical); 60 fps is
  the series' rate, not AGENTS.md's 30 fps default; the clean cut ends 3.3 s after the last cue.
- **A6. Deferred toolkit item:** the English `.srt` splits `docker ps -a`, `source: not found` and `KeyError:
  'question'` across lines (see "Still open"; `QA_FOLLOWUPS.md`).

## Verified (final render, `6b88321`)

All numbers from `measured.json` and the five reports (measured on `73928e7`, 2026-11-01), plus this record's own
checks of the fix round (above).

- **Files:** H.264 High, yuv420p, 1920×1080 at 60 fps; AAC 48 kHz stereo, 174–177 kbps. Each decodes in full with
  `ffmpeg -v error` with exit 0 and no errors (`decode_*.log`; the re-burned zh-en copy in
  `writer/decode_zh-en_rebuilt.log`). The re-stitch rewrote the clean MP4 (08:15 UTC) and both part MP4s
  (08:38–08:39) after those first decodes and loudness runs (08:02–08:10); their sizes, frame counts and durations
  are unchanged, and all three were decoded again after the rewrite with exit 0 and no errors
  (`verifier/decode_*.log`). Their loudness was not re-measured in full; a 120 s sample of the clean cut (10:00–12:00)
  reads −16.1 LUFS, LRA 2.2 LU, true peak −2.8 dBTP.

  | file | duration | frames | size | loudness | LRA | true peak |
  |---|---|---|---|---|---|---|
  | `ac215-l08-llm-finetuning.mp4` | 2009.754 s (33:29.75) | 120,584 | 105.3 MiB | −16.0 LUFS | 2.5 LU | −2.8 dBTP |
  | `ac215-l08-llm-finetuning.zh-en.mp4` | 2009.750 s | 120,585 | 105.0 MiB | −16.0 | 2.5 | −2.8 |
  | `ac215-l08-llm-finetuning_part1.mp4` | 1047.333 s (17:27.33) | 62,837 | 58.1 MiB | −16.1 | 2.4 | −2.8 |
  | `ac215-l08-llm-finetuning_part2.mp4` | 962.524 s (16:02.52) | 57,747 | 47.1 MiB | −16.1 | 2.5 | −2.8 |

  The two parts' frame counts sum to the clean cut's exactly (62,837 + 57,747 = 120,584).
- **Subtitles:** `.srt` 521 cues, `.zh.srt` 435, `.zh-en.srt` 513; parts 285 / 242 / 286 and 236 / 193 / 227. The
  last cue ends at 2006.398 s (parts: 1045.236 and 959.114 s). In every file the cues are in order, inside the
  runtime, at least 0.949 s long (`.zh-en.srt` 1.000 s), and none overlap.
- **Chapters:** 16 entries whose titles match `video.yaml`'s scenes in order; each start equals the cumulative
  scene durations (S16 at 1867.517 s = 31:07); `chapters_part1.txt` (9) and `chapters_part2.txt` (7, from 00:00 to
  13:40) match too.
- **Scenes:** all 16 end on an empty frame (`scene-ends/`); the scene segments sum to 2009.733 s, the clean cut's
  video length.
- **Narration:** 119 SAY lines = 119 rendered voice blocks; 4,366 words; 141.4 wpm over voice time.
- **Lecture tags:** 34 (one the S01 specimen), each found, none overlapping, none left at a scene end (`tags/`).
- **Privacy:** the persona appears only as the `‹instructor›` chip and "the instructor"; the name scan of all nine
  `.srt` files, `chapters.txt` and `transcript.md` found 0 hits, and no real name was seen in the frames read or the
  ASR transcripts. The endpoint at `gemini-finetuner/cli.py:107` is shown redacted; no key, project number or endpoint
  ID is shown.
- **Provenance** (`ASSETS.md`): terminal lines come from the 2026-10-31 captures in `assets/terminal/` (every README
  command in README order, exactly as written; extras tagged `extra`; the five hand-written files tagged `scripted`);
  code panels quote `assets/source/` at `44ef6f0`, checked against the git blob hashes (line 107 redacted); the
  README's documented outputs are tagged `expected`; the Colab outputs are the staff's saved A100 run, tagged
  `recorded`; the GCP console, the tuning page, the training monitor and the Colab menus are drawings tagged
  `illustration`.

## Not claimed

- **No human listened to this cut** or watched it. The listening gate rests on the series waiver quoted under gate 6,
  and the audio was checked only by machine (the ASR round trip).
- **The Chinese subtitles were reviewed by agents only** (the QA subtitle watcher, the text fixer, the pairs check and
  this record's check of the six re-ordered pairs); no human translator or native reviewer read them.
- **Nothing that talks to Google ran past the missing key.** `--generate`, `--upload`, `--train` and `--chat` stop
  at the real `File /secrets/llm-service-account.json was not found` / `DefaultCredentialsError`. No dataset was
  generated by Gemini, nothing was uploaded, no tuning job ran, no endpoint was chatted with: those steps are shown
  from the README's outputs (`expected`) and schematic drawings (`illustration`). The service-account and key steps,
  enabling the APIs and creating the bucket were not performed. The tuning job's duration and real cost are not
  measured; the README's cost table is shown as stale, not checked against today's pricing.
- **No Docker Hub, Apple Silicon or Debian-`sh` run of our own beyond the captures:** the image was built on Linux
  x86_64; the `dash` failure is from `laptop/20`.
- **The Colab path was not run** (no GPU, no Colab session, no Hugging Face token): its cells are quoted from the
  downloaded notebook and its outputs are the staff's saved A100 run. The video's T4 memory figures are our
  arithmetic, tagged `estimate`, not a measured peak.
- **The visual check read frames every 3 s**, plus targeted frames; motion between samples was checked only by
  `freezedetect` (13 of 67 stretches measured) and the tags check's 4 fps corner sweep. The visual and pairs checks
  ran on the burned copy before the fix round; after it, only the subtitle band at the six re-ordered pairs was
  re-read on frames (`writer/frames/`).
- **The loudness of the re-stitched files was not re-measured in full** (the re-burned zh-en copy, and the clean
  and part MP4s rewritten at 08:15–08:39 UTC). It rests on the zh-en audio stream being bit-identical to the clean
  cut's (MD5 `4d0e6ab0…`), on the unchanged sizes and durations, and on one 120 s sample of the clean cut.
- **No review-bot pass on this episode** as of the QA run: its follow-ups watcher found no bot comment on any L08
  file. Nothing in this record checks for bot comments posted later.
- **The QA fixes were verified by agents** on fresh preview or 720p renders of each scene, before the 1080p60
  renders; they were not re-checked one by one on the final cut, which the five final-cut checks cover only by their
  own sampling.
- **Every check in this record is an agent's.**
