# Review record: AC215 · Lecture 3 — Containers II: five containers, one bucket

Follow-along of [dlops-io/mega-pipeline](https://github.com/dlops-io/mega-pipeline) (`main` @
`c6bbc9b`). The issue of record is #36. The work is in the series draft PR #29. Claude Code cloud
sessions (Claude) produced the episode from 2026-10-13 to 2026-10-17: captures on 10-13, the
whole-video QA on the 480p draft of 10-15 (its fixes and verifiers ran through 10-16), one finishing
pass on 10-17 that a usage limit split into two runs (01:23–03:35 and 14:53–16:20 UTC), a
bilingual-order audit of the subtitles on 10-17 (`0c4d0e9`), and the 1080p60 final cut, measured on
2026-10-17 at 23:52 UTC. A fix round on 10-18 changed S06, S07 and S13 for three items the final-cut
checks had left open. Those three scenes were re-rendered at 1080p60, and the video was re-stitched
with a sample-peak limiter after loudnorm (`explainer/build.py`, then `alimiter=limit=0.79` and AAC
at 128k). The re-stitch was measured on 2026-10-18 at 06:26 UTC, and its three changed scenes were
rechecked on frames. Two encoder commits then changed only the final audio encode (`8a092e4`: no AAC
noise substitution; `5833542`: limit 0.71 and AAC at 192k), and the video was stitched again from
the same scene renders with `--no-render --crf 27 --burn` (files written 09:38–10:23 UTC) and
re-measured; measuring finished at 10:48 UTC. A stitch in between, after `8a092e4` alone
(07:20–08:27 UTC, still 0.79 at 128k), was overwritten by it and is not measured in this record.
This record was written on 2026-10-18 from the final cut's checks and updated the same day from the
recheck and the remeasure. Below, "final cut" means
the 2026-10-17 stitch and "re-stitch" means the current files in `output/`. The frame checks of the
recheck and the ASR audio comparison ran on the earlier stitch, the one measured at 06:26 UTC ("the
06:26 stitch" below), which has the same scene renders: picture and narration are unchanged, and
only the final audio encode differs. Verified facts and unclaimed reviews are kept in separate
sections.

Times are mm:ss in the full video (`output/ac215-l03-mega-pipeline.mp4`, 30:56.4), except where
marked *draft*. Draft times refer to the 480p QA draft, which ran 30:11.7 (1811.72 s in its
`build/qa/scenes.json`). Later fixes, mostly longer narration, lengthened the video by 44.6 s in all.
Scene starts moved by up to about 47 s (S13–S15; S15 itself got 1.9 s shorter), so a draft time sits
up to about 47 s earlier than the same moment in the final cut. The re-stitch moved nothing: every
scene starts at the same millisecond as in the final cut, and the runtime is the same. The evidence
files named below are in `build/final-review/`, except those written with a `build/recheck/` prefix,
which come from the 2026-10-18 recheck, and those with a `build/remeasure/` prefix, which come from
the 10:48 UTC remeasure. All three folders are git-ignored and exist only in the producing session,
so a successor has to re-run the checks to reproduce the evidence.

## Content gates (AGENTS.md)

1. **Hook** ✔. S01 opens on a puzzle, not a value proposition. A voice recording goes in on the
   left, and five programs, "each in its own container", turn it into an English and a French
   podcast "without ever sending each other a message. So how do they cooperate, and who pays?"
   (00:00–00:13.5). The V1 relay plays under the question, its boxes and drawers unlabelled (only
   an `illustration` tag). The answer, that the bucket is the message bus, comes in S02.
2. **Intuition before formalism, with an animated mechanism per core idea** ✔. Eight set pieces
   (BRIEF.md, "Visual set pieces") are each animated before the commands they explain, as
   script.md's SHOW lines specify. The director watchers read every draft sheet against those
   lines:
   - V1, the relay through the bucket's drawers (S01, S02): the split at `text_paragraphs/`, and the
     default-group drawer flashing RED.
   - V2, Dockerfile → layer stack (S05, S06, S11, S13): the apt lists are deleted inside the RUN
     slab, the slab is 842 MB, and the CACHED stamps.
   - V3, the window (S07, S08, S11): the image, the throwaway writable sheet, and the laptop sheet
     that covers `/app` through the bind mount.
   - V4, uv add as list, receipt and shelf (S08, S11): the chips evaporate on `exit`.
   - V5, who is calling (S09): signpost → key → token → IAM padlock.
   - V6, two sieves, one for Git and one for the image (S14).
   - V7, `requires-python` as an interval (S04, S12).
   - V8, ticket stubs for long-running operations (S10, S13): Text-to-Speech writes straight to the
     bucket.
3. **Pause-and-ponder moments and a recap** ⚠ partly met.
   - **Ponders:** there are five ponder cards, each with an 8 s timer: S02 02:54.6, S06 11:03.6,
     S07 12:14.7, S12 22:30.4 and S14 27:21.9. Each answer starts as its timer ends, and all five are
     visible on the burned-in copy. That is one ponder every 6.2 min. AGENTS.md aims for one every
     2 min, which would be about 15 for this length. The longest gap is 615.7 s, from 12:14 to 22:30.
   - **Series rule:** the series brief fixes 3–5 ponders per lecture (ac215-video skill, step 3).
     Separately, 27 SAY blocks tell the viewer to pause (`measured.json`): 26 follow-along pauses at
     README steps (run, type, edit or catch up), plus S01's "Pause at the yellow your-turn tag",
     which explains the convention. The longest gap between them is 192.9 s (05:47.9–09:00.9).
     These are follow-along pauses, not ponders.
   - **Recap:** S15 starts at 29:14.5 and runs 101.8 s. It closes with five test-yourself
     questions, one per core idea, each with its set piece's icon (30:13.7–30:41.1). The answers are
     in `exercises.md` (study guide §8). There is no spoken summary of the content.
   - **Open question for Conny:** does the series format (five ponders, a recap made of questions)
     satisfy this gate for AC215?
4. **Narration written for the ear, with word-anchored cues** ✔.
   - **Spoken style:** following script.md's conventions, commands, flags and paths are spoken in
     words ("dash dash r m", "slash app"). Versions are said "at the time of recording", and every
     sentence starts with a capital letter. Two sentences open with a command name, capitalised:
     "Git status shows only cli.py as changed." (S11) and "Git status lists the Dockerfile too"
     (S12), against script.md's convention "No sentence opens with a command".
   - **Size:** 158 SAY lines with 4,402 words, identical in order to the 158 blocks spoken in the
     renders. The longest block is 62 words.
   - **Anchors:** the scenes have 643 anchor calls: 594 direct `vo.wait_until` calls, 46 through
     S06's `at()` and 3 through S09's `wait_said()`. Counting each loop's phrases separately gives
     656 anchors, and every phrase is found in its own narration block.
   - **QA fixes:** the draft's ASR pass found three phrases a listener would mishear, and QA
     reworded them: "apt's" → "the apt", "secrets slash" → "secrets, slash", "covers Git only" →
     "only covers Git". QA also split three sentences whose cues ran 1.06–1.45 s ahead of the voice
     (S09, S11, S12).
5. **Simulated-target-viewer QA over the full draft** ✔. Seven watchers reviewed the 480p draft.
   Two of them were simulated target viewers ("newcomer", one for each part), who watched with the
   README open. The seven produced 77 timestamped findings (the two newcomers 32 of them). The one
   must and all 30 shoulds were fixed, re-rendered and verified on fresh frames. The nits left open are listed below with the reasons.
6. **Measured checks** ✔ for all four MP4s. The numbers, measured on the re-stitch's current files
   (remeasure finished 2026-10-18 at 10:48 UTC), are under "Verified (re-stitched final render)".
   - **True peak, met in every file:** −2.7 dBTP in the full cut, in the zh-en copy (the Bilibili
     asset), in part 1 and in part 2, so the build's −1.5 dBTP target is met with more than 1 dB to
     spare. The final cut, before the limiter, peaked at −0.9. The 06:26 stitch peaked at −1.6 in
     the full cut, the zh-en copy and part 1, and at +0.9 in part 2, in one 100 ms window of its left
     channel (29:01.3 on the full clock); the audio re-encode fixed both ("Fixed in the fix round",
     item 6).
   - The music-balance check does not apply. This series has no music bed: `video.yaml` has no
     `music:` block, and between the voice clips the audio is digital silence (zero samples; the
     onset check's meter floor is −120 dBFS), apart from each clip's last few milliseconds.

   **Human review:** the series waiver below stands in for a listening sign-off.

   Listening sign-off: waived by Conny for the AC215 series (Explainer_Videos#29, 2026-10-15): 「不需要，我现在对视频质量很满意的」 — no human listened to this cut; the ASR round trip below is the substitute.

## Whole-video QA (480p draft, 2026-10-15; times are draft times)

**Watchers and findings.** Seven watchers reviewed the draft and reported 77 findings: 1 must, 30
should and 46 nit. Each watcher read the contact sheets against `script.md` and the English `.srt`,
and pulled exact frames for anything doubtful.

| watcher | lens | must | should | nit |
|---|---|---|---|---|
| director, part 1 (S01–S07) | sync, facts, commands vs captures, tracker | 0 | 2 | 6 |
| newcomer, part 1 | simulated target viewer, README and clone open | 0 | 6 | 10 |
| director, part 2 (S08–S15) | same as part 1 | 0 | 4 | 5 |
| newcomer, part 2 | simulated target viewer | 1 | 5 | 10 |
| subtitles (zh, zh-en, en) | glossary, line breaks, reading speed, pairing | 0 | 8 | 8 |
| follow-ups (`QA_FOLLOWUPS.md`) | every logged review-bot item | 0 | 2 | 3 |
| ASR (base.en, large-v3-turbo) | mishearings, cue sync | 0 | 3 | 4 |

The director and newcomer watchers found that the facts, commands and terminal lines match the
captures and sources. That
covers the README and `cli.py` line numbers, the sizes (842 MB, 1.35 → 1.48 GB), the 26 packages and
the 138,445 bytes. There were no wrong facts or wrong commands.

**The must, and how it was fixed.**

- *Draft 22:49, S12:* Google retires Gemini 2.5 Flash Lite on 2026-10-20, and the note gave viewers
  no model to switch to. Fixed in two rounds:
  - **The fixer** added "pick one on Vertex AI's 'Model versions' page · listed replacement
    `gemini-3.1-flash-lite`" and a red 404 fail line.
  - **The verifier** found that newer models are not served in the `us-central1` region that
    `generate_text/cli.py:24` hard-codes. The note card therefore gained "in cli.py line 24, set
    `location='global'`", and the narration gained "Newer models aren't served in the region cli.py
    uses, so also set the location on line 24 to global." (final 23:42.9–23:51.2). The same change
    went into README.md and `digest.md:365`.

**The shoulds, and how they were fixed.** All 30 are fixed. By theme:

- **Follow-along** (15):
  - ▶ your turn now appears on "Pause" for the key (S04). Before, it appeared only after the
    sentence had ended, and stayed up about 1.4 s.
  - S03 adds a chip and a spoken line: "open the README in the transcribe audio folder".
  - The narration now explains the line-continuation backslash (S05) and one blank line between
    blocks, so line numbers match (S05).
  - The narration says the build landmarks come from the full log, not the compact live view (S06).
  - Part 1 ends with "rerun the same docker run … before part 2" (S07), and part 2 shows that
    `docker run` with "new terminal? run this" (S08).
  - The study guide is "linked in the description", with an on-screen tag (S01).
  - The `sudo chown` fix now says where to run it and stays up 5 s (S08).
  - `--entrypoint ls` is explained (S14).
  - S15's `git status` caption mentions the viewer's five untracked `.dockerignore` files.
  - S14's beat-1 extras and the `.dockerignore` rebuild no longer scroll away before they can be
    read. The `#3 [internal] load .dockerignore` line stays, and the tag reads ".dockerignore: was
    2B, now a file".
- **Picture and continuity** (4):
  - The S06 note is now a framed row tag, not text that looks like log output.
  - S08's "Docker Desktop handles this" line is up 11.5 s instead of 1.5 s.
  - S10's window lists the same files as S08 and S11.
  - S08's opening recap no longer shows the GREEN shelf line, so it matches S07's last frame.
- **Subtitles** (8):
  - Splits inside a glossary unit are gone: the TTY error text, the `-v` description, 用完就扔,
    the retirement date, and the help string "Transcribe audio file to text".
  - S13's zh said build step 2 took 0.6 s. It now says the whole build did.
  - The `-d -t -u` flag list stays in one cue.
  - Quiz question 5 is now at 6.8 units/s, down from 10.3.
- **ASR** (3): the S12 cue that ran 1.45 s early is fixed by a sentence split. "apt's" and
  "secrets slash" are reworded.

**Process.**
- One fixer per scene (13 scenes) and one narration/subtitle fixer applied the fixes. A skeptical
  verifier per scene then re-checked them on fresh 720p frames and with `explainer.check`.
- The verifiers found and fixed several incomplete fixes:
  - S01's on-screen link tag was missing.
  - S03's chip was missing.
  - S04's ▶ came 0.7 s late.
  - S05's tag nearly touched row 200.
  - S06's leader line ran through the terminal border.
  - S07's part-1 rerun strip was missing.
  - S12 lacked the region step.
  - S13 had a dim blink and a stray letter.
  - S14 left an orphaned continuation row.
- A finishing pass, interrupted by a usage limit and then resumed, did the rest:
  - It applied 11 narration and subtitle items, and re-voiced S01, S03, S06, S09, S11, S12 and S14.
  - It added the 12 `lecture_ref` slide tags that SLIDES.md marks "do", and the S07 "host folder" /
    "container path" labels.
  - It fixed, in the scene files, the items of the S01 and S13 review-bot threads and the toolkit
    workarounds that a scene file can close. Both threads (`PRRT_kwDOU7eKAs6tWpWM`,
    `PRRT_kwDOU7eKAs6tbH32`) were answered with the final-cut evidence at 04:29 UTC on 2026-10-18 and
    are resolved on PR #29 (checked 2026-10-18 at 06:36 UTC).
- QA's follow-ups watcher closed every `QA_FOLLOWUPS.md` item in the scenes: fixed, or shown not
  to reproduce. An audit of 1,122 FadeOuts found no snap-back. The shared-code requests in that file
  stay unimplemented in `scenes/common.py`; the scenes carry local workarounds.

**Left open on purpose (nits), with the reasons.**
- **S14, draft 27:24: the `erratum` tag on README.md:103–106.** That README note is true for Git
  but says nothing about the image. The tag is required by a recorded decision: script.md, BRIEF.md:439
  and the series rule "erratum on every README slip". This is a question for Conny, not a scene edit.
- **S06: pip's "running as root" warning is not narrated.** Explaining it would add 20 words to a
  script already over budget. The warning appears only in the plain log, not in the viewer's compact
  view.
- **S13: the C, D and E editor insets (shown 0.25–0.35 s) still read `group_name = "pavlos"`.** The
  yellow underline marks the line to edit, and S12 shows the full edit.
- **Toolkit items, for separate toolkit PRs:**
  - `explainer/subtitles.py` divides cue times by display characters (GLOSSARY I2). The cues it put
    more than 1 s early were fixed instead by the three sentence splits.
  - `ReadmeTracker`'s empty caption placeholder makes the first step caption fly in from mid-frame.
    The scenes use a one-line workaround (S12, S13, S14).
  - `Window.blink()` pulses the route without any visible change. S07, S08 and S10 now pulse the
    route's stroke themselves, and S11 pulses its shelf the same way.
  - The laptop prompt makes short commands fold with ` \` (PROMPT_DIRTRIM). The folds are honest
    continuations, and changing the prompt would touch 13 scenes.
  - Renaming the tracker steps was replaced by the S01 line "splits the README into numbered steps".
- **S15's recap card shows the study-guide URL `github.com/JunyiZhou-Conny/MLOps_Learning`.** L01,
  L02 and L04 do the same. Whether an owner handle may appear on screen is a question for Conny.

## Final-cut checks (1080p60, 2026-10-17/18)

Five agent checks of the stitched deliverables. No human watched or listened. The fix round's
changes were then rechecked on the re-stitch (see "Fixed in the fix round"); where that changed a
result here, this section says so. Those frame checks ran on the 06:26 stitch; the current files
share its scene renders and differ only in the final audio encode.

**Lecture-slide tags and review-bot items.**
- **Method:** tag times come from each scene's `events.json`, converted to full-video time. Four
  frames were checked per tag, and a 10 fps scan looked for anything within 14 px of a tag.
- **Results:** none of the 12 tags overlaps anything, every label is correct, and none is still on
  screen at its scene's end.
- **Span rule:** in the final cut, 9 tags spanned their cited picture (the check's own summary line
  said "10 of 12", but its table supported 9). For S01 and S02 "slides 7, 15" that holds with a
  note: the S01 tag's last 3.3 s are on the tracker, and the S02 tag arrives 2.6 s before its row is
  drawn. The fix round made S13 "slides 23–24" span its picture and kept S07 "slides 51–52" on
  through the ponder, so 10 tags now span their picture. S02 "slide 25" and S07 "slides 51–52"
  still do not, for the reasons under "Open", item 1.
- **The S06, S07 and S13 rows below are from the re-stitch:** times from the re-rendered scenes'
  `events.json`, checked on frames and against the pixel counts in
  `build/recheck/scenes/tag_lit.json` and `topright_s07.json` (summary in
  `build/recheck/scenes/summary.json`). The other nine rows are from the final cut; their scenes
  were not re-rendered.

| tag | scene | on (fade in) | off (fade out) | spans its picture? |
|---|---|---|---|---|
| Lecture 3 · slides 24–28 · Tutorial 5 | S01 | 00:28.9 | 00:36.7–00:37.5 | yes (README page, then the tracker) |
| Lecture 3 · slides 7, 15 | S02 | 01:19.9 | 01:30.3–01:31.5 | yes (production row, drawn 01:22.5–01:24.8) |
| Lecture 3 · slide 25 | S02 | 01:35.0 | 02:05.8–02:07.1 | starts 4.6 s after its anchor (01:30.3) |
| Lecture 3 · slides 23, 70 | S04 | 04:45.2 | 04:52.5–04:53.2 | yes |
| Lecture 3 · slide 40 | S05 | 07:44.1 | 08:03.3–08:03.6 | yes |
| Lecture 3 · slide 33 | S06 | 11:12.2 | 11:28.9–11:29.6 (scene fade) | yes |
| Lecture 3 · slides 51–52 | S07 | 11:45.6 | 12:24.75–12:25.05 (was 12:05.7–12:06.3) | through the ponder; leaves 7.3 s before the mount picture (12:32.3), clear of the label that fades in from 12:25.47 |
| Lecture 3 · slide 38 | S11 | 20:44.8 | 21:02.5–21:02.9 | yes |
| Lecture 3 · slide 33 | S11 | 21:19.5 | 21:24.8–21:25.6 (scene fade) | yes |
| Lecture 3 · slides 23–24 | S13 | 26:41.4 | 27:03.0–27:03.4 (was 26:55.2–26:55.6) | yes (leaves with the bonus tracker and the cli_11.py panel) |
| Lecture 3 · slides 34, 43 | S14 | 28:10.2 | 28:32.6–28:33.1 | yes |
| Lecture 3 · slide 70 | S15 | 30:46.1 | 30:55.1–30:56.0 (final fade) | yes |

The review-bot items:
- **S01 "link in the description" (thread PRRT_kwDOU7eKAs6tWpWM): verified.** The tag fades in
  00:54.8–00:55.4; ASR puts "linked" at 00:54.8. The tag sits under "MLOps_Learning", left-aligned,
  and clears with the footer at 00:56.6–00:57.3. **Still true in the re-stitch:** frames at 00:55.40
  and 00:56.50 re-extracted from the clean cut are pixel-identical to the final review's
  (`build/recheck/bot/s01_link_*.png`, `build/recheck/bot/compare.json`). The thread is resolved.
- **S13 beat 11, the terminal and ▶ at "Pause to run" (thread PRRT_kwDOU7eKAs6tbH32): verified in
  substance.** The terminal fades in 26:15.2–26:15.5, as "Pause" is spoken. ▶ fades in
  26:15.5–26:15.9 and is solid 0.08 s after "run". Before the fix it landed about 0.9 s late.
  **Still true in the re-stitch:** the re-rendered S13's `events.json` puts the terminal fade at
  26:15.22–26:15.52 and ▶ at 26:15.52–26:15.92, and frames at 26:15.40, 26:15.75, 26:15.95 and
  26:16.30 are pixel-identical to the final review's (`build/recheck/bot/s13_b11_*.png`,
  `build/recheck/bot/compare.json`). The thread is resolved.
- **S06 build step 1 badge (Bugbot 4300879315, thread PRRT_kwDOU7eKAs6tb1ui): not fixed in the
  final cut; fixed and verified in the re-stitch.** See "Fixed in the fix round", item 1. The thread
  is still unresolved (see "Open", item 5).
- **In the burned-in copy:** the tags keep their times and do not clash with the subtitle band.

**ASR round trip (the substitute for a listen).** faster-whisper `base.en` transcribed the final
mp4's audio and was compared with the 503 cues of the `.srt`.
- **Run on the final cut, not on the re-stitch.** The re-stitch takes its narration from the same
  Kokoro voice clips: it re-rendered only S06, S07 and S13, changed no SAY line, anchor or
  subtitle, and changed only the final audio encode: a limiter after loudnorm, now at 0.71 with AAC
  at 192k and no noise substitution ("Fixed in the fix round", item 6). It was not transcribed again.
  Instead the 06:26 stitch's audio (limit 0.79, AAC at 128k) was compared with the 16 kHz audio the
  ASR heard (`build/final-review/asr/final_16k.wav`, the same length, 1856.448 s). Per scene,
  including the three re-rendered ones, the correlation is 0.9982–0.9985 at a constant 5 ms delay,
  and the difference sits 24.5–25.1 dB below the signal
  (`build/recheck/narration_vs_asr/compare.json`). That difference is consistent with the limiter
  and a fresh AAC encode; how much each contributes was not measured. The 5 ms delay matches the
  limiter's look-ahead: `alimiter` delays its output by its attack time (default 5 ms) unless
  `latency` is set, and the build leaves both at their defaults. It is negligible next to the cue
  timing. **This comparison was not re-run on the current encode:** its correlation, delay and
  difference are the 06:26 stitch's.
- **Per cue:** it recognised 4,476 words, and 236 of the 503 cues differ. These are mostly
  cue-boundary effects.
- **Whole text:** aligned against the text sent to the voice (from `subs.json`), 4,616 expected
  words meet 4,618 recognised words, a 0.955 match with 190 places that differ.
- **Recheck:** `large-v3-turbo` rechecked 48 clips that span 93 cues (`asr/clips*/clips.json`;
  the check put the doubtful ones at about 60). Every doubtful word was either heard correctly or
  is explained by known noise:
  - sound-alikes ("changed" heard as "change", "at sign");
  - terms the recogniser doesn't know: venv, git, ffmpeg, uv add. Their Kokoro phonemes were checked
    and are correct, and the same words are recognised elsewhere in the video;
  - spoken forms versus display forms (`/app`, `--rm`);
  - 04:39–04:45, which `base.en` skipped and the large model hears word for word.
- **Real mispronunciations or swallowed words: none.**
- **Late audio:** no cue's audio starts more than 1 s after the cue. This was checked at −40 and −30
  dBFS. The largest delay is 0.60 s at −40 dBFS (cue 488, 29:54.1) and 0.74 s at −30 dBFS (cue 409,
  24:56.7); `asr/verdicts.json` reports only the −40 figure.
- **End:** the last cue ends at 30:54.0, and the video runs to 30:56.4.
- **Evidence:** `asr.json`, `asr/verdicts.json`, `asr/global_diffs.json`, `asr/large_clips*.log`,
  `asr/onsets*.json`.

**Visual pass over the burned-in copy (`zh-en.mp4`).** The pass read 39 contact sheets: 619 frames,
one every 3 s, with tile labels corrected by +1.5 s. Suspect moments got full-size frames and short
frame strips.
- **Passed:**
  - All 15 scenes end on an empty frame.
  - There is no black stretch of 0.5 s or more, and every scene starts at its `chapters.txt` time.
  - No text is outside the frame, and no tag is stuck on screen.
  - Every overlap seen clears within about 1 s as an animation settles. Garbled text appears only in
    mid-morph animations.
- **Subtitles, spot-checked at 11 places:**
  - Chinese is always above English.
  - The picture is scaled into y 0–939, and the subtitles sit in the band at y 992–1062. They cannot
    cover a terminal command.
- **Seven minor findings:** they are listed under "Open". Evidence is in `sheets/` and
  `visual/findings.json`.

**Bilingual pairing (all 509 cues of `.zh-en.srt`).**
- **Meaning:** no meaning swaps. Where a condition or time clause appears, both languages put it in
  the same cue and in the same order.
- **winpty:** the known failure is fixed. Cue #204 (12:48.2) pairs 如果 docker run 报错：the input
  device is not a TTY with its English, and #205 pairs "put winpty in front".
- **Line breaks:** no break falls inside a command, path, flag or placeholder. Every cue has exactly
  one Chinese and one English line, because `WrapStyle: 2` turns off automatic wrapping.
- **Widths:** measured in Noto Sans CJK SC, the widest lines are 1511 px (zh, #314) and 1593 px
  (en, #47), against 1840 px of usable width.
- **Parts:** the part files (220 + 289 cues) have the same text as the full file.
- **Evidence:** `bilingual/findings.json` and `bilingual/cues.txt`.

**Measured** (`measured.json`, scripts and logs in `measured/`). These were the final cut's numbers.
The 06:26 stitch was measured again (`build/recheck/measured.json`, scripts and logs in
`build/recheck/`), and the current files once more after the audio re-encode
(`build/remeasure/measured.json`, scripts and logs in `build/remeasure/`). The current numbers are
under "Verified (re-stitched final render)".

## Fixed in the fix round (re-stitched cut, 2026-10-18)

A fixer and a separate verifier per scene changed and checked S06, S07 and S13 on `-q m` previews
(`explainer.check` OK; each scene's length unchanged: S06 133.6 s, S07 134.87 s, S13 165.38 s at
1080p60). The three scenes were then re-rendered at 1080p60 and the video re-stitched. Two agent
checks of the re-stitch followed. One read frames, 2 s contact sheets of the zh-en copy and pixel
counts for the three scenes (`build/recheck/scenes/`, numbers in `summary.json`; frame names carry
the full-video second, from the clean cut unless marked zh-en). The other re-measured the
deliverables (`build/recheck/measured.json`). No human watched or listened. Chapters did not move
and no subtitle changed. Item 6 came later: a re-stitch from the same scene renders that changed
only the final audio encode, re-measured at 10:48 UTC (`build/remeasure/measured.json`). The frame checks in items 1–3 and 5 ran
on the 06:26 stitch and were not repeated on the current files.

1. **S06, 11:19.9–11:23.8: build step 1's badge no longer takes the cached green** (Bugbot
   4300879315, thread `PRRT_kwDOU7eKAs6tb1ui`; was "Open", item 1).
   - **The change:** `scenes/s06_build.py:823–824` now recolours badge 1 to `SYSTEM` (ORANGE, the
     base slab's colour and the series colour for system parts) and pulses it once, on the same
     anchor "and build step 1 is the base image". It used to be `recolor(badges[0], VENV)`.
   - **On the re-stitch:** badges 2 and 3 turn green at 11:19.9–11:20.5, and their CACHED stamps
     arrive at 11:20.5–11:21.4. Badge 1 stays teal up to the anchor (11:22.733; its cue starts at
     11:22.591, #182 in `.zh-en.srt` and #188 in `.srt`). On the anchor it turns orange and pulses
     until 11:23.83, then stays orange to the end of the scene.
   - **Ring colours:** badges 2 and 3 measure (130,176,111). Badge 1 measures (99,188,163) before
     the anchor and (213,134,80) after it. The final cut had badge 1 at (138,191,132), matching the
     cached green. Midway through the teal-to-orange change (11:23.00, `g_025.png`), badge 1 passes
     through a grey-green for a few frames: its closest approach is an RGB distance of 42.5 to the
     green of badges 2 and 3 in the same frames, and 29.4 to the final cut's (138,191,132). Its teal
     sits 61 from the green of badges 2 and 3.
   - **The "slide 33" tag** still fades in at 11:12.2–11:12.8, stays clear of the "edit: group_name
     in cli.py" chip, and leaves with the scene fade at 11:28.9–11:29.6. The last frame is empty.
   - **Evidence:** `build/recheck/scenes/t_s06_a.png`, `t_s06_b.png`, `t_s06_c.png`, every frame
     from 11:22.60 to 11:23.88 (`build/recheck/scenes/s06_strip60/g_001.png`–`g_078.png`),
     `build/recheck/scenes/s06_strip/badge_colours.json` and
     `build/recheck/scenes/s06_strip60/badge1_vs_green.json`.
2. **S13, 26:41.4–27:03.4: the "slides 23–24" tag now spans the ElevenLabs bonus picture** (was
   "Open", item 2).
   - **The change:** `scenes/s13_speed_round.py` no longer fades the tag in beat 15. It leaves in
     beat 16's `reset(...)` play (line 1434), with the bonus tracker and the cli_11.py panel.
   - **On the re-stitch:** the tag fades in at 26:41.4–26:41.8 with the bonus picture. It stays past
     the old exit (26:55.2), beside the gold "your own ElevenLabs key and quota" chip, the README card
     and the cli_11.py panel ("read at start-up"), and nothing overlaps it. It fades out at
     27:03.0–27:03.4 in the same move as the bonus tracker and the panel, and is gone by 27:03.5.
     The last frame is empty.
   - **Unchanged older effect:** during the 0.4 s cross-fade at 27:03.0–27:03.4, the old and new
     tracker captions overlap at the top left, and the fading cli_11.py panel lies over the terminal's
     title bar as the terminal grows upward (frame at 27:03.18 in
     `build/recheck/verify2/s13/full_1623.18.png`). Both clear as the animation settles.
   - **Evidence:** `build/recheck/scenes/t_s13_a.png`, `t_s13_b.png`, `t_s13_c.png`,
     `st_s13_a.png`, `st_s13_b.png`, and `build/recheck/scenes/tag_lit.json`.
3. **S07, 11:45.6–12:25.0: the "slides 51–52" tag now stays through the ponder** (was "Open", item
   2; fixed as far as the layout allows, and the rest stays open as item 1).
   - **The change:** `scenes/s07_run.py` no longer fades the tag in beat 3. It fades inside beat 4's
     existing play (line 498), just before the answer's label arrives.
   - **On the re-stitch:** the tag fades in at 11:45.6–11:46.3 with the laptop folder and the mount.
     It stays past the old exit (12:05.7) and through the ponder (card at 12:14.7, timer until
     12:23.3), about 0.4 units clear of the writable layer. `events.json` puts its fade-out at
     12:24.75–12:25.05 and the fade-in of "start: bash, venv on" at 12:25.47–12:25.87. On frames,
     the tag is gone by about 12:24.97 and the label shows from about 12:25.55, so the corner is
     empty for about half a second. The last frame is empty.
   - **Evidence:** `build/recheck/scenes/t_s07_a.png`, `t_s07_b.png`, `t_s07_c.png`,
     `st_s07_a.png`, `st_s07_b.png`, `st_s07_c.png`, `build/recheck/scenes/topright_s07.json`,
     `build/recheck/scenes/tag_lit.json`, and every frame from 12:24.67 to 12:25.85
     (`build/recheck/verify2/s07/fine/f_000000.png`–`f_000071.png`, cut frames 44680–44751).
4. **True peak in the full cut, the zh-en copy and part 1: −0.9 → −1.6 dBTP** (was "Open", item 3;
   the 06:26 stitch, superseded by item 6). The limiter after loudnorm brought all three under the
   build's −1.5 dBTP target. No 100 ms window in them went above −1.5 dBTP
   (`build/recheck/ftpk_windows.json`). Part 2 went the other way, to +0.9; item 6 fixes it.
5. **The new renders are in the cut, and nothing else moved.**
   - At 11:24.0, 12:15.0 and 26:58.0, a frame of the clean cut matches the new scene render at 45.9,
     41.5 and 39.3 dB PSNR. At 12:15.0 and 26:58.0 those frames show the tags the final cut did not.
   - All 15 scene starts equal the final cut's to the millisecond (S06 556.05 s, S07 689.65 s, S13
     1466.783 s), and `chapters.txt` is identical to the README's chapter list.
   - Every tracked file in `output/` (every `.srt`, `.zh.srt`, `.zh-en.srt` and `.ass` file, the
     parts' included, the three chapter files and `transcript.md`; no MP4 is tracked) has the same
     bytes as the commit the final review measured. The cues at the fixed moments are unchanged
     (numbered as in `.zh-en.srt`): #182 (11:22.591), #197 (12:23.250–12:28.007) and #448
     (27:02.983).
   - In the zh-en copy, a 4 fps scan of the three scenes (1,736 frames) found picture content no
     lower than about row 890 (rows 888–891, depending on the brightness threshold), subtitles no
     higher than row 992, and nothing in rows 940–991, so no
     subtitle covers a tag or a command (`build/recheck/scenes/bandscan_s06.json`,
     `bandscan_s07.json`, `bandscan_s13.json`). The contact sheets
     `build/recheck/scenes/sheets_zhen/s06_01.png`–`s13_10.png` were all read.
6. **Audio re-encode: every MP4 now peaks at −2.7 dBTP, and part 2's +0.9 spike is gone** (was
   "Open", item 1, in the 06:26 stitch's record).
   - **What was wrong:** the 06:26 stitch's part 2 peaked at +0.9 dBTP, in one 100 ms window of its
     left channel at part-2 time 916.83 s (29:01.3 on the full clock, S14), and only when decoded
     from the start. `8a092e4` attributes the spike to the AAC encoder's noise substitution (on by
     default); `5833542` reports that AAC at 128k overshoots a sample-peak limit by about 1.1 dB
     even with noise substitution off.
   - **The change:** `8a092e4` turns noise substitution off and `5833542` lowers the limit to 0.71
     and encodes at 192k, so the final audio is now
     `loudnorm=I=-16:TP=-1.5:LRA=11,alimiter=limit=0.71:level=disabled`, then AAC with
     `-aac_pns 0` at 192k. The video was stitched again with `--no-render --crf 27 --burn`; all 15
     normalised scene files predate it.
   - **New numbers** (10:48 UTC, `build/remeasure/measured.json`): all four MP4s peak at −2.7 dBTP
     (−2.66 to −2.73 to two decimals), and no 100 ms window in any of them goes above −1.5 dBTP.
     Part 2 at 916.827 s now reads −7.2 / −7.2 dBTP (was +0.9 / −3.9). Integrated loudness
     (−16.1 LUFS), LRA, durations, frames and video bitrates are unchanged; audio is 177.9–180.3
     kbps (was 117.5–118.8), so the files grew by 6.3–14.2 MB.

## Open in the re-stitched cut (for the coordinator)

1. **The tag-span rule is partly met.** Each case is left as built unless the coordinator decides
   otherwise:
   - **S02 "slide 25":** it starts at 01:35.0, 4.6 s after "That storage is…". This is on purpose:
     the prefix card would sit about 16 px from it (`extra/s02_bucket_before_tag_92.20.png`).
   - **S07 "slides 51–52":** after the fix round it stays through the ponder and is gone by
     12:25.05, but the mount picture stays until 12:32.3, so the picture runs 7.3 s without its
     tag (it was 26 s). It cannot stay: the tag and the ponder answer's "start: bash, venv on"
     label (fading in from 12:25.47) would overlap at about x 1377–1420 px, y 103–118 px.
2. **Gate 3 shortfall:** five ponders against the aim of about 15, and the recap is made of
   questions rather than a spoken summary. See gate 3.
3. **Minor visual findings (nits):**
   - **Still stretches of about 4 s outside ponder timers, with narration running over each**
     (times from the scenes' `events.json`; freezedetect, blind to small animations, reports them a
     little longer):
     - 13:39.5–13:43.7 (4.2 s): the end of S07, before its fade-out. It is unchanged in the
       re-rendered S07.
     - 23:48.0–23:52.0 (4.0 s): the Vertex AI note.
     - Nearly still, 11:21.4–11:26.4: the layer stack with the CACHED tags. In the re-stitch only
       badge 1's recolour and pulse (11:22.7–11:23.8) move, so the longest fully still part is
       2.6 s (11:23.8–11:26.4). It was 3.2 s in the final cut.
   - **Small layout points:**
     - 16:55–17:14: the "token" tag sits across two panel borders, though it stays readable.
     - 12:07–12:25, during the ponder: the floating folder copy sits flush against the `/app` box.
     - 01:25.6, from the tags check: the five boxes cross the "here: write outputs…" caption for
       about 1 s as they move down.
     - 27:03.0–27:03.4, from the recheck: during a 0.4 s cross-fade the old and new tracker
       captions overlap, and the fading cli_11.py panel lies over the rising terminal's title bar.
     - 12:05.9–12:06.3, from the fix round's S07 verifier and older than the fix: the fading
       "/tmp · throwaway" tag crosses the rising writable layer's dashed border
       (`build/recheck/verify2/s07/x_sheet.png`).
   - **Intended by the scene code, kept as is:**
     - 18:50–18:53: the page badge sits on the `text_prompts/` icon (`s10_transcribe.py:502`).
     - 05:30–05:37: the installer line breaks mid-word, "shell o" / "r run:". This is the real
       terminal's wrap, asserted at `s04_setup.py:498`.
4. **The same English line repeats under split Chinese cues** in zh-en: #21–22 (01:05.7–01:11.7),
   #40–42, #383–384 and #441–442.
   - Here one English sentence carries two or three Chinese pieces, so `.zh-en.srt`'s English is not
     word for word the `.srt`. The Chinese matches `.zh.srt` exactly.
   - The pairing check rates all four as intended: each Chinese piece is part of the English
     sentence above it. #21–22 is the case the S01 verifier flagged, though. The finishing pass
     applied the one-clause zh with no comma (`43eea56`). The bilingual-order audit (`0c4d0e9`,
     2026-10-17 19:38) then rewrote `i18n/zh/narration/g1.yaml:38` to follow the English order,
     "我们录制时用的是一台 Debian 12 笔记本，装着 Docker Engine 29。", and its comma splits the line
     again. A nit.
5. **Publishing prerequisites, outside the cut:**
   - `video.yaml` now has a `publish:` block (added in `661cc16`): `title_zh`, `description_zh` with
     the tutorial repo and the study-guide URL that S01 announces as "linked in the description",
     `tags_zh` and `tid: 231`. The release preflight, which refuses to start without that block, has
     not been run against it.
   - One L03 review-bot thread on PR #29 is unresolved (checked 2026-10-18 at 06:36 UTC): S06
     (`PRRT_kwDOU7eKAs6tb1ui`). It is fixed and verified in the re-stitch ("Fixed in the fix round",
     item 1) and waits for a reply and a resolve. The last reply on it (2026-10-17) promised that the
     beat-8 anchor would become "Build steps 2 and 3", that only `badges[1:3]` take the cached
     colour, and that step 1 keeps its base-image look. The cut does the first two. Step 1 now turns
     ORANGE, the colour of its base slab, and pulses once, so the closing reply should say that. The
     S01 (`PRRT_kwDOU7eKAs6tWpWM`) and S13 (`PRRT_kwDOU7eKAs6tbH32`) threads were answered and
     resolved on 2026-10-18.
   - `QA_FOLLOWUPS.md` records no outcome for five entries that QA closed: the S07→S08 continuity
     check, the S07 unused imports (`ruff --select F401` now passes), the S07 GREEN shelf line, the
     all-scenes FadeOut grep and the S14 full read. They still read as to-dos. Its snap-back and
     `Window.blink()` entries were marked done on 10-17 (`43fa0c7`).

## Verified (re-stitched final render)

Measured on the re-stitch's current files on 2026-10-18; measuring finished at 10:48 UTC
(`build/remeasure/measured.json`, logs in `build/remeasure/logs/`). Every ffmpeg job ran one at a
time, and the MP4s' mtimes and part 2's sha256 were the same before and after. Against the 06:26
measurement (`build/recheck/measured.json`), 344 values are unchanged, among them the durations,
frames, codecs, video bitrates, integrated loudness and LRA (to 0.1), every subtitle figure, the
chapters and the part sums. What changed is the audio encode ("Fixed in the fix round", item 6):
the true peaks, the audio and overall bitrates, the sizes and the audio MD5. The "was" values below
are the 06:26 stitch's. The 06:26 measurement had in turn left 274 of the final cut's compared
values unchanged; it changed the true peaks, part 1's integrated loudness (−16.0 → −16.1 LUFS),
and the sizes and bitrates, slightly.

- **Deliverables:** all four MP4s decode in full (`ffmpeg -v error … -f null -`) with exit code 0 and
  no error lines. All are H.264 High, yuv420p, 1920×1080, 60 fps constant, with AAC-LC audio at
  48 kHz stereo, one video and one audio stream each.

  | file | size | duration | frames | video / audio kbps | integrated | LRA | true peak (L, R) |
  |---|---|---|---|---|---|---|---|
  | `ac215-l03-mega-pipeline.mp4` | 115.21 MB (was 101.06) | 1856.354 s (30:56.4) | 111,377 | 305.8 / 179.0 (was 118.0) | −16.1 LUFS (−16.10) | 2.3 LU | −2.7 dBTP (−2.7, −2.7; −2.66); was −1.6 |
  | `ac215-l03-mega-pipeline.zh-en.mp4` (to Bilibili) | 112.46 MB (was 98.31) | 1856.354 s | 111,378 | 294.0 / 179.0 (was 118.0) | −16.1 LUFS (−16.10) | 2.3 LU | −2.7 dBTP (−2.7, −2.7; −2.66); was −1.6 |
  | `ac215-l03-mega-pipeline_part1.mp4` | 46.29 MB (was 39.96) | 824.543 s (13:44.5) | 49,471 | 257.2 / 180.3 (was 118.8) | −16.1 LUFS (−16.09) | 2.2 LU | −2.7 dBTP (−2.7, −2.7; −2.67); was −1.6 |
  | `ac215-l03-mega-pipeline_part2.mp4` | 68.91 MB (was 61.10) | 1031.814 s (17:11.8) | 61,906 | 344.7 / 177.9 (was 117.5) | −16.1 LUFS (−16.09) | 2.5 LU | −2.7 dBTP (−2.7, −2.7; −2.73); was **+0.9 (+0.9, −1.8)** |

  Integrated loudness and the per-channel true peaks are ebur128's readings; the two-decimal figures
  are loudnorm's measuring pass. The overall bitrates are 496.5, 484.7, 449.1 and 534.2 kbps (were
  435.5, 423.7, 387.7 and 473.8). The runtime is inside the series' 25–35 min. The parts add up to
  1856.357 s, 0.003 s more than the full cut. The 15 scene renders add up to the full cut's 111,377 frames, and so do the parts'
  frames. The zh-en cut has one extra frame and starts at 0.000 s instead of 0.021 s, which is
  negligible. Its audio packets are identical to the full cut's: the same packet MD5
  (`54172da069211a346c4846dc7f90cdf0`) and the same per-packet framemd5 over 87,022 packets. The
  06:26 stitch's MD5 was `a8f8b512…`, so the audio is a new encode, as expected.
- **True peak:** the build's −1.5 dBTP target is met in all four files, with more than 1 dB to
  spare. Each peaks at −2.7 dBTP. The full cut and the zh-en copy reach it at 06:50.5 (410.458 s,
  S05) and at 17:18.5 (1038.52 s, S09, right channel); part 1 at 06:50.5; part 2 at part-2 times
  494.359 s and 1027.01 s, which are 21:58.9 (S12) and 30:51.5 (S15) on the full clock. No 100 ms
  window in any file goes above −1.5 dBTP (`build/remeasure/measured.json`, per-window logs in
  `build/remeasure/logs/`). At the old spike spot, part 2 at 916.827 s now reads −7.2 / −7.2 dBTP
  (was +0.9 / −3.9), and the full cut and the zh-en copy at 1741.37 s read −7.2 / −7.2 (was
  −1.6 / −7.6).
- **Subtitles:** unchanged since the final cut. The re-stitch rewrote every tracked file in
  `output/` with the same bytes as the committed copies the final review measured. The 10:48
  remeasure found all 16 tracked output files byte-identical to HEAD (`86fb60c`) and to `2de1be4`,
  the commit the 06:26 recheck measured; only their mtimes changed.
  - **Cue counts:** `.srt` has 503 cues, `.zh.srt` 420 and `.zh-en.srt` 509. The `.zh-en.ass` has
    509 events.
  - **Order and bounds:** in all three files the cues are numbered in sequence, ordered, not
    overlapping and not empty. They run from 0.000 to 1854.043 s, inside the runtime.
  - **Shortest cues:** 1.000 s in `.srt`, 1.234 s in `.zh.srt` and 1.245 s in `.zh-en.srt`, so
    none is under 0.8 s.
  - **Both languages:** all 509 zh-en cues are one Chinese line followed by one English line.
  - **Parts:** the part files add up to the full files (224 + 279, 186 + 234, 220 + 289) with the
    same text, and their timings match within 0.0007 s. No cue crosses the part boundary.
- **Chapters:** `chapters.txt` has 15 chapters for 15 scenes. The titles match `video.yaml` in
  order, and every start time matches the scene durations added up. Both part chapter files match
  too. All 15 scene durations and frame counts, including the re-rendered S06, S07 and S13, are the
  same as in the final cut, and `chapters.txt` matches the README's chapter list.
- **Narration:** the 158 SAY lines (4,402 words) are spoken in order, with no line missing and none
  added. That is about 100 words over BRIEF.md's range of 3,900–4,300. The pace is 142.3 wpm over the
  runtime. The Kokoro voice is `af_heart`, at speed 0.9. This was checked on the final cut; the fix
  round changed no SAY line, and the 06:26 stitch's audio matched the final cut's per scene (see the
  ASR round trip). The current audio encode was not compared.
- **Burned-in layout:** the picture is scaled to the top 87 % of the frame, and the subtitles sit in
  the band below it. The longest lines fit inside the 1840 px usable width. In the 06:26 stitch's
  S06, S07 and S13, the picture never reaches below about row 890 and the subtitles never above
  row 992.
- **Provenance:** this comes from ASSETS.md. The QA watchers checked the draft's terminal lines
  against the captures, and lines added later are asserted against their capture lines in the scene
  code.
  - **Real captures:** every terminal panel prints from real sessions on 2026-10-13. These used a
    fresh Debian 12 "laptop" (Python 3.11.2, user `student`) and Docker Engine 29.8.2, and the five
    images were built from the README's Dockerfile. Commands are typed as the README spells them;
    the capture-only `--network host` and base-image lines are never shown.
  - **Source quotes:** every code panel quotes `assets/source/` at the pinned commit.
  - **Recorded without the key:** the real failing runs are tagged "recorded without the key".
  - **Expected:** C's, D's and E's `--help` panels are tagged `expected`, taken from their READMEs.
  - **Illustrations:** the Canvas download, the bucket, its drawers and the leaderboard are
    schematics tagged `illustration`.
  - **Stand-in key:** S14 uses an 82-byte placeholder, tagged as a stand-in and never shown.
- **Lecture slides:** 12 `lecture_ref` tags cite slides 7, 15, 23–28, 33, 34, 38, 40, 43, 51–52 and
  70. They are the 12 tags that SLIDES.md §5 marks "do", and each tag's label was checked on
  frames.
- **S04's "have uv? skip to 5:47" chip** points 0.9 s before the cue "Now the step itself"
  (05:47.9), so a viewer who jumps there misses nothing, as the comment above `SKIP_TO` requires.

## Not claimed

- **No human has listened to or watched this cut**, neither the final cut nor the re-stitch. The
  listening sign-off is waived for the series (gate 6). The ASR round trip shows the narration is
  intelligible to a machine. It does not judge pacing, tone or how natural the voice sounds.
- **The ASR round trip was not re-run on the re-stitch.** It transcribed the final cut. The
  re-stitch is covered by the audio comparison under "ASR round trip", which shows the same
  narration, not a fresh transcription. That comparison ran on the 06:26 stitch (limit 0.79, AAC at
  128k); the current encode was neither transcribed nor compared.
- **The Chinese and bilingual subtitles were reviewed by agents only:** the subtitle watcher, the
  verifiers and the pairing check. No native-speaker human has read them.
- **The visual review sampled the video.** It used contact sheets every 3 s plus targeted frames,
  not continuous playback, so a defect shorter than 3 s between samples could be missed.
- **The recheck looked at three scenes.** On the 06:26 stitch, only S06, S07 and S13 were checked
  on frames (contact sheets every 2 s, targeted frames and pixel counts). The other 12 scenes were
  not re-rendered and were not re-watched. The final cut's visual pass stands for them. The current
  files, which differ from the 06:26 stitch only in the final audio encode, were measured but not
  checked on frames.
- **The QA fixes were verified on preview renders, not one by one in this cut.** The fixers and
  verifiers checked them on 480p/720p renders of the scene files. The 1080p60 cut was checked only
  by the five final-cut checks above, and the re-stitch only by the 2026-10-18 recheck and
  remeasure.
- **What removed part 2's +0.9 dBTP spike is not isolated.** The remeasure shows it gone after
  `8a092e4` (no noise substitution) and `5833542` (limit 0.71, AAC at 192k) together; it does not
  separate noise substitution from the limit and bitrate change. The −1.8 dBTP that `8a092e4`
  reports for noise substitution off alone is that commit's own claim and was not reproduced here.
  How the limiter and the fresh AAC encode share the −25 dB difference between the 06:26 stitch's
  audio and the final cut's was not measured either.
- **Nothing that needs the course key was run:**
  - `--download` with a key, `--transcribe`, `--generate`, `--synthesis`, `--translate` and
    `--upload`, for all five components.
  - The "with your key, look for" cards describe what `cli.py` prints, from reading the code. They
    are not observed output.
  - The Gemini fix is untested here, since there was no GCP access. That covers the replacement
    model `gemini-3.1-flash-lite`, `location='global'` at `cli.py:24`, and the 2026-10-20 retirement
    date. It rests on Google's model pages, fetched 2026-10-16, and on the google-genai client code.
- **Other steps not run:**
  - The Docker Hub login, tag and push: there is no account, and pushing would publish the key.
  - The ElevenLabs bonus.
  - The Canvas download.
  - `docker image prune -f`, which was not captured.
  - The Windows and macOS paths: Git BASH, `winpty`, the PowerShell installer and Docker Desktop's
    uid handling. The captures ran on Linux only.
- **The released files are a different render.** Every claim above is about this local stitch of
  the 1080p60 scene renders (the re-stitch, where the numbers are concerned). The release workflow
  re-renders every scene with the pinned engine, and its `<id>.validation.json` does not exist yet.
  The released files should be re-checked against the numbers here, at least for duration, frames,
  loudness, true peak and cue counts.
