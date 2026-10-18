# Review record: AC215 · Lecture 3 — Containers II: five containers, one bucket

Follow-along of [dlops-io/mega-pipeline](https://github.com/dlops-io/mega-pipeline) (`main` @
`c6bbc9b`). The issue of record is #36. The work is in the series draft PR #29. Claude Code cloud
sessions (Claude) produced the episode from 2026-10-13 to 2026-10-17: captures on 10-13, the
whole-video QA on the 480p draft of 10-15 (its fixes and verifiers ran through 10-16), one finishing
pass on 10-17 that a usage limit split into two runs (01:23–03:35 and 14:53–16:20 UTC), a
bilingual-order audit of the subtitles on 10-17 (`0c4d0e9`), and the 1080p60 final cut, measured on
2026-10-17 at 23:52 UTC. This record was written on 2026-10-18 from the final cut's checks.
Verified facts and unclaimed reviews are kept in separate sections.

Times are mm:ss in the full video (`output/ac215-l03-mega-pipeline.mp4`, 30:56.4), except where
marked *draft*. Draft times refer to the 480p QA draft, which ran 30:11.7 (1811.72 s in its
`build/qa/scenes.json`). Later fixes, mostly longer narration, lengthened the video by 44.6 s in all.
Scene starts moved by up to about 47 s (S13–S15; S15 itself got 1.9 s shorter), so a draft time sits
up to about 47 s earlier than the same moment in the final cut. The evidence files named below are
in `build/final-review/`. That folder is git-ignored and exists only in the producing session, so a
successor has to re-run the checks to reproduce the evidence.

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
6. **Measured checks** ✔, with two notes. The numbers are under "Verified (final render)".
   - The true peak is −0.9 dBTP, above the build's −1.5 target.
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
    `PRRT_kwDOU7eKAs6tbH32`) are still unresolved on PR #29 (checked 2026-10-18).
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

Five agent checks of the stitched deliverables. No human watched or listened.

**Lecture-slide tags and review-bot items.**
- **Method:** tag times come from each scene's `events.json`, converted to full-video time. Four
  frames were checked per tag, and a 10 fps scan looked for anything within 14 px of a tag.
- **Results:** none of the 12 tags overlaps anything, every label is correct, and none is still on
  screen at its scene's end.
- **Span rule:** 9 tags span their cited picture. For S01 and S02 "slides 7, 15" that holds with a
  note: the S01 tag's last 3.3 s are on the tracker, and the S02 tag arrives 2.6 s before its row is
  drawn. The other three do not span their picture; they are listed under "Open". The check's own
  summary line says "10 of 12", but its table supports 9.

| tag | scene | on (fade in) | off (fade out) | spans its picture? |
|---|---|---|---|---|
| Lecture 3 · slides 24–28 · Tutorial 5 | S01 | 00:28.9 | 00:36.7–00:37.5 | yes (README page, then the tracker) |
| Lecture 3 · slides 7, 15 | S02 | 01:19.9 | 01:30.3–01:31.5 | yes (production row, drawn 01:22.5–01:24.8) |
| Lecture 3 · slide 25 | S02 | 01:35.0 | 02:05.8–02:07.1 | starts 4.6 s after its anchor (01:30.3) |
| Lecture 3 · slides 23, 70 | S04 | 04:45.2 | 04:52.5–04:53.2 | yes |
| Lecture 3 · slide 40 | S05 | 07:44.1 | 08:03.3–08:03.6 | yes |
| Lecture 3 · slide 33 | S06 | 11:12.2 | 11:28.9–11:29.6 (scene fade) | yes |
| Lecture 3 · slides 51–52 | S07 | 11:45.6 | 12:05.7–12:06.3 | leaves 26 s before the mount picture (12:32.3) |
| Lecture 3 · slide 38 | S11 | 20:44.8 | 21:02.5–21:02.9 | yes |
| Lecture 3 · slide 33 | S11 | 21:19.5 | 21:24.8–21:25.6 (scene fade) | yes |
| Lecture 3 · slides 23–24 | S13 | 26:41.4 | 26:55.2–26:55.6 | leaves before the key chip (27:00.0) and the bonus (27:03.0) |
| Lecture 3 · slides 34, 43 | S14 | 28:10.2 | 28:32.6–28:33.1 | yes |
| Lecture 3 · slide 70 | S15 | 30:46.1 | 30:55.1–30:56.0 (final fade) | yes |

The review-bot items:
- **S01 "link in the description" (thread PRRT_kwDOU7eKAs6tWpWM): verified.** The tag fades in
  00:54.8–00:55.4; ASR puts "linked" at 00:54.8. The tag sits under "MLOps_Learning", left-aligned,
  and clears with the footer at 00:56.6–00:57.3.
- **S13 beat 11, the terminal and ▶ at "Pause to run" (thread PRRT_kwDOU7eKAs6tbH32): verified in
  substance.** The terminal fades in 26:15.2–26:15.5, as "Pause" is spoken. ▶ fades in
  26:15.5–26:15.9 and is solid 0.08 s after "run". Before the fix it landed about 0.9 s late.
- **S06 build step 1 badge (Bugbot 4300879315): not fixed.** It is listed under "Open".
- **In the burned-in copy:** the tags keep their times and do not clash with the subtitle band.

**ASR round trip (the substitute for a listen).** faster-whisper `base.en` transcribed the final
mp4's audio and was compared with the 503 cues of the `.srt`.
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

**Measured** (`measured.json`, scripts and logs in `measured/`). The numbers are under "Verified".

## Open in the final cut (for the coordinator)

1. **S06, 11:22.7–11:23.2: a real defect (Bugbot 4300879315 is not fixed).**
   - At 11:19.9–11:20.5, build steps 2 and 3 turn green with their CACHED stamps.
   - Then badge 1 turns the same green on "and build step 1 is the base image". The tags check
     measured the ring at (128,187,117), against (134,184,110) for badges 2 and 3; a re-sample of the
     ring pixels gives (138,191,132) against (142,186,120). Badge 1 gets no stamp, but its colour
     matches the cached steps.
   - The cause is `scenes/s06_build.py:821`, `self.play(recolor(badges[0], VENV), run_time=0.5)`.
     `VENV` is also the CACHED stamp colour. The finishing plan specified this line (S06 item
     "qa-text"), in line with the QA verifier's reading of green badges as "does not run again". But
     the reply on the thread (`PRRT_kwDOU7eKAs6tb1ui`) had promised that only `badges[1:3]` take the
     cached colour and that step 1 keeps its base-image look.
   - The choice: change or drop that recolour, then re-render S06 and re-stitch. Or answer the
     thread with the reason.
   - Evidence: `bot/s06_badges_{672.90,681.50,684.00}.png`, `bot/s06_badges_strip.png`.
2. **The tag-span rule is partly met.** Each case is left as built unless the coordinator decides
   otherwise:
   - **S02 "slide 25":** it starts at 01:35.0, 4.6 s after "That storage is…". This is on purpose:
     the prefix card would sit about 16 px from it (`extra/s02_bucket_before_tag_92.20.png`).
   - **S07 "slides 51–52":** it leaves at 12:06.3, but the mount picture stays until 12:32.3.
     Keeping the tag would make it collide with the ponder answer's "start: bash, venv on" label at
     12:25.5–12:28.3.
   - **S13 "slides 23–24":** it leaves at 26:55.6, but the key-and-quota chip stays until 27:00.0
     and the bonus section until 27:03.0. Nothing blocks keeping the tag longer.
3. **True peak −0.9 dBTP** in the full cut, the zh-en cut and part 1, highest at about 08:16.8 (S05).
   That is above the build's loudnorm target of −1.5 and misses a −1 dBTP ceiling by 0.1 dB. Part 2
   peaks at −1.2. The integrated loudness is on target.
4. **Gate 3 shortfall:** five ponders against the aim of about 15, and the recap is made of
   questions rather than a spoken summary. See gate 3.
5. **Minor visual findings (nits):**
   - **Still stretches of about 4 s outside ponder timers, with narration running over each**
     (times from the scenes' `events.json`; freezedetect, blind to small animations, reports them a
     little longer):
     - 13:39.5–13:43.7 (4.2 s): the end of S07, before its fade-out.
     - 23:48.0–23:52.0 (4.0 s): the Vertex AI note.
     - Nearly still, 11:21.4–11:26.4: the layer stack with the CACHED tags. Only the 0.5 s badge-1
       recolour (11:22.7–11:23.2) moves, so the longest fully still part is 3.2 s.
   - **Small layout points:**
     - 16:55–17:14: the "token" tag sits across two panel borders, though it stays readable.
     - 12:07–12:25, during the ponder: the floating folder copy sits flush against the `/app` box.
     - 01:25.6, from the tags check: the five boxes cross the "here: write outputs…" caption for
       about 1 s as they move down.
   - **Intended by the scene code, kept as is:**
     - 18:50–18:53: the page badge sits on the `text_prompts/` icon (`s10_transcribe.py:502`).
     - 05:30–05:37: the installer line breaks mid-word, "shell o" / "r run:". This is the real
       terminal's wrap, asserted at `s04_setup.py:498`.
6. **The same English line repeats under split Chinese cues** in zh-en: #21–22 (01:05.7–01:11.7),
   #40–42, #383–384 and #441–442.
   - Here one English sentence carries two or three Chinese pieces, so `.zh-en.srt`'s English is not
     word for word the `.srt`. The Chinese matches `.zh.srt` exactly.
   - The pairing check rates all four as intended: each Chinese piece is part of the English
     sentence above it. #21–22 is the case the S01 verifier flagged, though. The finishing pass
     applied the one-clause zh with no comma (`43eea56`). The bilingual-order audit (`0c4d0e9`,
     2026-10-17 19:38) then rewrote `i18n/zh/narration/g1.yaml:38` to follow the English order,
     "我们录制时用的是一台 Debian 12 笔记本，装着 Docker Engine 29。", and its comma splits the line
     again. A nit.
7. **Publishing prerequisites, outside the cut:**
   - `video.yaml` has no `publish:` block yet, and the release preflight refuses to start without
     one. That block is also where the study-guide URL goes, which S01 announces as "linked in the
     description".
   - Three L03 review-bot threads on PR #29 are unresolved (checked 2026-10-18): S01
     (`PRRT_kwDOU7eKAs6tWpWM`) and S13 (`PRRT_kwDOU7eKAs6tbH32`), both fixed and verified in this cut
     and waiting for a reply and resolve, and S06 (`PRRT_kwDOU7eKAs6tb1ui`, item 1).
   - `QA_FOLLOWUPS.md` records no outcome for five entries that QA closed: the S07→S08 continuity
     check, the S07 unused imports (`ruff --select F401` now passes), the S07 GREEN shelf line, the
     all-scenes FadeOut grep and the S14 full read. They still read as to-dos. Its snap-back and
     `Window.blink()` entries were marked done on 10-17 (`43fa0c7`).

## Verified (final render)

- **Deliverables:** all four MP4s decode in full (`ffmpeg -v error … -f null -`) with exit code 0 and
  no error lines. All are H.264 High, yuv420p, 1920×1080, 60 fps constant, with AAC-LC audio at
  48 kHz stereo.

  | file | size | duration | frames | integrated | LRA | true peak |
  |---|---|---|---|---|---|---|
  | `ac215-l03-mega-pipeline.mp4` | 100.89 MB | 1856.354 s (30:56.4) | 111,377 | −16.1 LUFS | 2.3 LU | −0.9 dBTP |
  | `ac215-l03-mega-pipeline.zh-en.mp4` (to Bilibili) | 98.13 MB | 1856.354 s | 111,378 | −16.1 LUFS | 2.3 LU | −0.9 dBTP |
  | `ac215-l03-mega-pipeline_part1.mp4` | 39.89 MB | 824.543 s (13:44.5) | 49,471 | −16.0 LUFS | 2.2 LU | −0.9 dBTP |
  | `ac215-l03-mega-pipeline_part2.mp4` | 61.00 MB | 1031.814 s (17:11.8) | 61,906 | −16.1 LUFS | 2.5 LU | −1.2 dBTP |

  The runtime is inside the series' 25–35 min. The parts add up to 1856.357 s, 0.003 s more than
  the full cut. The 15 scene renders add up to the full cut's 111,377 frames. The zh-en cut has one
  extra frame and starts at 0.000 s instead of 0.021 s, which is negligible.
- **Subtitles:**
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
  too.
- **Narration:** the 158 SAY lines (4,402 words) are spoken in order, with no line missing and none
  added. That is about 100 words over BRIEF.md's range of 3,900–4,300. The pace is 142.3 wpm over the
  runtime. The Kokoro voice is `af_heart`, at speed 0.9.
- **Burned-in layout:** the picture is scaled to the top 87 % of the frame, and the subtitles sit in
  the band below it. The longest lines fit inside the 1840 px usable width.
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

- **No human has listened to or watched this cut.** The listening sign-off is waived for the series
  (gate 6). The ASR round trip shows the narration is intelligible to a machine. It does not judge
  pacing, tone or how natural the voice sounds.
- **The Chinese and bilingual subtitles were reviewed by agents only:** the subtitle watcher, the
  verifiers and the pairing check. No native-speaker human has read them.
- **The visual review sampled the video.** It used contact sheets every 3 s plus targeted frames,
  not continuous playback, so a defect shorter than 3 s between samples could be missed.
- **The QA fixes were verified on preview renders, not one by one in this cut.** The fixers and
  verifiers checked them on 480p/720p renders of the scene files. The 1080p60 cut was checked only
  by the five final-cut checks above.
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
  the 1080p60 scene renders. The release workflow re-renders every scene with the pinned engine, and
  its `<id>.validation.json` does not exist yet. The released files should be re-checked against the
  numbers here, at least for duration, frames, loudness and cue counts.
