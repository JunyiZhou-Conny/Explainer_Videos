# Review record: AC215 · Lecture 15 — ML workflows: deploy one model, then automate the pipeline on SageMaker

Follow-along of the course's AWS version of both Lecture 15 tutorials, each `README.md` top to bottom:
**Part 1** [dlops-io/model-deployment-aws](https://github.com/dlops-io/model-deployment-aws) `main` @ `077f4db`
(README A) and **Part 2** [dlops-io/ml-workflow-aws](https://github.com/dlops-io/ml-workflow-aws) `main` @ `f165c6e`
(README B), both re-checked with `git ls-remote` on 2026-11-05 (`ASSETS.md`, "Which commits"). Series decision: L15
follows AWS while the slides speak Vertex AI; the video maps each Vertex AI word onto its AWS counterpart as it comes up
(GCS bucket → S3, Model Registry → a SageMaker Model, endpoint → endpoint configuration + endpoint, Vertex AI Pipelines
→ SageMaker Pipelines, Artifact Registry → ECR, service account → a user's key on the laptop and a role in the cloud).
Claude Code sessions (Claude) produced it. Verified facts and unclaimed reviews are kept in separate sections.

- **Origin:** issue #106. Built end to end on 2026-11-05 by this coordinator's agents: digest rebuilt against the two AWS
  READMEs, live laptop captures, brief, script + 4 independent reviews (`build/review_merge_log.md`), `scenes/common.py`,
  16 scenes each with a fresh critic, zh subtitles, `exercises.md`, `README.md` and the study guide (on the
  MLOps_Learning branch). Milestone commit `d7952e2` (12:03 UTC); the issue's "CHECKPOINT scenes" comment is dated
  12:04 UTC.
- **Captures:** 2026-11-05 04:00–05:50 UTC (`ASSETS.md`, "terminal/"), in one fresh `docker:29.8.2-dind` "laptop"
  (linux/x86_64, user `student` uid 1000, AWS CLI 2.34.63). That machine had **no AWS account, no access key, no
  SageMaker and no billing**. Every local step ran live (both clones, `aws configure`, every `sh docker-shell.sh` as
  written and after the fixes, all four tutorial images and every README command inside them; the collector scraped 40
  images, the processor wrote real TFRecords, the trainer trained one epoch). Every AWS call stops at its honest first
  error (`Unable to locate credentials`, or AWS's own `InvalidClientTokenId` / `InvalidAccessKeyId` for obviously fake
  placeholder keys). Console steps are `illustration`; the one documented cloud output (`--predict`, README A:137–147)
  is `recorded`; two capture-only stand-ins are tagged (`tensorflow/serving:2.13.1` serving the export, `laptop/45`–`48`;
  the pipeline JSON built offline, `laptop/92`).
- **Two README breakages, shown with their fixes** (`ASSETS.md`, "Two findings"):
  - Unpinned `sagemaker = "*"` with no lock resolves SDK 3 (3.13.1 on Python 3.9, `laptop/22`; 3.29.0 on 3.11,
    `laptop/85`), which has none of the 2.x modules either `cli.py` imports (`laptop/23`, `86`). Fix: `sagemaker = "<3"`
    (`laptop/24`, `88`), shown in S04 (06:33.3 "Fix 2, also an extra: change "*" to "<3".") and again in S14.
  - The `--platform=linux/arm64/v8` build lines fail on Intel/AMD with `exec format error` (05:01.3, `laptop/20`, `65`,
    `70`). Fix: each script's own plain build line (05:15.2 "Swap them: fix 1, an extra.").
- **Masking:** the tutorial author's role ARN in `docker-shell.sh:8` is masked as `YOUR_ACCOUNT_ID` in the copied source;
  AWS's TensorFlow Serving registry account is written `<aws-dlc-account>` and never shown as digits; on screen accounts
  are `000000000000` or `$ACCOUNT_ID`, keys `PLACEHOLDER_NOT_A_REAL_*_000000000000`. The README's own example ARN uses
  AWS's documentation account `123456789012` (accepted item A1).
- **QA draft:** the 480p draft (30:04), rendered 12:22–12:26 UTC.
- **Whole-video QA:** `/root/ac215-backup/tasks/l15-qa-wb4sr7n7g.output`, key `result`. 39 agents: seven watchers, 15
  scene fixers (S01, S03–S16), one narration/subtitle fixer and 16 scene verifiers (S01–S16). The run log reads "L15:
  70 issues from 7/7 watchers". Committed as `22cb670` (14:54 UTC), after the WIP commit `fdebfe5`.
- **After QA, by the coordinator:** lexicon PR #109 merged to `main` as `a1dccf0`, which the CI release renders with.
- **Finishing pass:** none. The coordinator's list of finishing-pass outputs for L15 is empty (`[]`).
- **1080p60 renders:** all 16 scenes; the renders and the logs in `build/logs/` are dated 2026-11-05 15:02–15:33 UTC.
  None of the 16 logs contains "anchor not found".
- **Final cut:** 30:27.2 (1827.225 s); parts 16:27.3 + 14:00.0. File times (UTC, 2026-11-05): the clean cut and the
  full-cut subtitles 15:50 (committed as `891832a`); the burned copy, chapters and transcript 16:08; the parts
  16:09–16:10 (part subtitles, chapters and transcript committed as `35ddd7b`). The MP4s are not in Git (release
  assets).
- **Final-cut checks:** one round, five agent checks, no re-burn. The coordinator saved their returned text as
  `build/final-review/report-{tags,asr,visual,pairs,measured}.md`. All five reports exist and were read in full for
  this record. Their evidence is dated 16:12–16:36 UTC, after the last output file was written (16:10:45), so every
  check ran on the files now in `output/`. None of the five found a blocking defect.

**Conventions:**
- **Times** are mm:ss in the full cut (`output/ac215-l15-vertex-ml-workflows.mp4`, 1827.225 s), except in
  "Whole-video QA", which keeps the 480p draft's times (marked *draft*).
- **Cue numbers** name their file: `.srt` (511 cues) or `.zh-en.srt` (512).
- **Evidence paths** are relative to `build/final-review/`. That folder is git-ignored and exists only in the producing
  session; a successor re-runs the checks to reproduce it.

## Content gates (AGENTS.md)

1. **Hook** ✔. S01 opens on a puzzle, not a value proposition: two real outputs of the same predict code, the README's
   `recorded` one and this recording's local stand-in, that disagree.
   - "Here is a question for a model: what cheese is in this photo?" (`.srt` cue 1, 00:00.0); "Both answers on screen
     come from the same predict code in cli.py." (cue 2, 00:04.0); "And both answers say brie." (cue 3, 00:09.6).
   - The puzzle: "Now count the numbers." (cue 4, 00:11.6) "The top answer, the README output, holds three." (cue 5,
     00:13.3) "The bottom one, from this recording, holds four." (cue 6, 00:16.4) "One model cannot give both." (cue 7,
     00:19.5) "So which model is behind an endpoint, and what else is there?" (cue 8, 00:21.6).
   - **Payoff:** S08, "Now the opening puzzle." (cue 243, 14:23.1) "Same code, different artifact: the README output
     came from an older model, with three classes and another label order." (cues 244–245, 14:24.9–14:29.7); the
     three pieces return in S07 ("Remember the three pieces from the start.", cue 186, 10:43.7) and the recap (cue 496,
     29:30.2).
2. **Intuition before formalism, with an animated mechanism for each core idea** ✔. `BRIEF.md` ("Visual set pieces")
   defines eight, each animated next to the commands it explains:
   - **V1, a key on the laptop, roles in the cloud (`IdentityBadges`, built in S03; the S10, S14 and S16 reprises are drawn with other code in those scenes):** "Why two identities?"
     (03:22.8), "Your laptop signs each request with the user key, and the endpoint you create later acts as the role."
     (03:24.5–03:27.8); Option 2's exports hit the container wall, "So exported keys fall off at the wall." (04:28.6).
   - **V2, a star is not a pin (`StarVsPin`, S04, reprise S14):** "TensorFlow is pinned to one version, but SageMaker
     says "*": any version." (05:25.6); after ponder 1, ""*" is a constraint, not a pin, as in lecture 1:" (05:55.2);
     the imports "find nothing" (06:23.1) and the `"<3"` wall (06:33.3–06:40.4). S14 replays it on 3.29.0 with the
     real import failure on screen (24:19.2 cue, frame at 24:22.5; see "Whole-video QA", M1).
   - **V3, where preprocessing lives (`TwoPipes`, S05, S08, S12):** the left pipe from "The predict code opens the
     photo," (07:39.7) to "Preprocessing sits on your side of the wire." (08:07.3); client-side brittleness
     (08:10.2–08:22.9); the right pipe, "The preprocess function decodes the JPEG, converts it to floats, and resizes it."
     (08:31.0) "Raw bytes in, one score per class out." (08:46.3); S08's cube, "224 times 224 times 3: 150,528 floats."
     (13:19.8).
   - **V4, slide 12's steps 1–3 on AWS (`ArtifactTrip`, S06):** the four README steps (cues 158–160, 09:05.6–09:16.9), "A SavedModel
     is a folder:" (10:09.5), "The code puts it in a folder named 1," (10:18.5), "The tarball holds that folder at its
     top." (10:25.5).
   - **V5, model, endpoint configuration, endpoint (`ThreeObjects`, S01, S07, S09, S15):** S01's preview "Behind an
     endpoint sit three pieces" (00:25.5) with the meter (00:34.5); S07 "That one call creates all three:" (11:30.1–
     11:35.5); S09's teardown and the endpoint left billing, "One. Delete removes only the endpoint the file names."
     (16:03.7).
   - **V6, four people, four terminals (`ManualToPipeline`, S10):** "The lecture draws the problem: four stages, each
     run by a person at a terminal." (16:28.5) "The answer is an orchestrator." (16:38.1).
   - **V7, one image, two modes (`CallableImage`, S11, S14):** "The entry point script has a switch." (19:05.3) "No
     arguments: it opens bash, development mode" (19:07.6) "Arguments: it runs them and exits, production mode."
     (19:12.2).
   - **V8, a pipeline drawn by references (`ReferenceDAG`, S15, S16 recap):** "Not a string: a reference, and it draws
     an edge." (26:16.0) "Each reference draws one more edge." (26:27.6); after ponder 4, "The list is a set of steps,
     not a schedule." (27:05.3).

   **Lecture slides:** a GREY "Lecture 15 · slide(s) …" tag top right (`report-tags.md`), 30 tags, one per `lref()`
   call in `scenes/*.py`, in every scene except S03 and S04 (S01 1, S02 3, S05 3, S06 1, S07 3, S08 1, S09 1, S10 4,
   S11 2, S12 2, S13 1, S14 2, S15 4, S16 2; times in `report-tags.md`). The deck is redrawn, never shown (`SLIDES.md`
   §1 maps scenes to slides). Cited slides: 6–8, 10–14, 16–17, 19–22, 24, 28–30, 32–38, 40, 41.
   - All 30 pass the hard checks: correct text, no overlap on any of the a_in, b_mid or c_before crops
     (`tags/allcrops_*.png`), none on screen when its scene ends. Two tags are on screen together only during the
     in-place crossfades in S07 (t09 → t10) and S10 (t14 → t15 → t16 → t17); in S16, t29 → t30 follow each other
     without overlapping.
   - Accepted by the coordinator: t13 (borderline) and t26 (small deviation from `script.md`), item A2.
3. **Pause-and-ponder moments and a recap**: ✔ for the ponders, by Conny's decision for the series (accepted item
   A3); ✔ for the recap.
   - **Ponders:** four, each a card followed by a silent timer. Card times are from `measured.json` (each scene's
     `events.json` plus its scene start); answers are from the `.srt`.

     | # | scene | card (from `script.md`) | card | timer | answer starts |
     |---|---|---|---|---|---|
     | 1 | S04 | The Pipfile says sagemaker = "*". The code worked when it was written. Nobody changed a line. Why does cli.py fail at import today? | 05:46.6 | 8 s | 05:55.2 ""*" is a constraint, not a pin, as in lecture 1:" (cue 107) |
     | 2 | S08 | --predict resizes one photo to 224 × 224 with 3 color channels. How many numbers travel to the endpoint for that one photo? | 13:11.2 | 8 s | 13:19.8 "224 times 224 times 3: 150,528 floats." (cue 226) |
     | 3 | S09 | You ran --deploy twice, then --delete once. How many endpoints still bill? | 15:57.1 | 6 s | 16:03.7 "One. Delete removes only the endpoint the file names." (cue 269) |
     | 4 | S15 | Reverse the list steps=[…] in Pipeline(...). Does the run order change? | 26:50.5 | 8 s | 26:59.0 "No. The order comes from the references: …" (cue 454) |

   - The visual check's `freezedetect` found exactly these four silent near-static stretches, at 05:48.2 (4.3 s),
     13:11.7 (8.3 s), 15:57.6 (6.3 s) and 26:53.6 (4.8 s) (`freezes.txt`, `freezedetect.log`; `report-visual.md` misquotes the middle two as 8.1 s and 6.1 s).
   - **Rate:** 4 cards in 30:27.2, 0.26 per 2 minutes, one every 7.6 minutes, against AGENTS.md's aim of one per 2
     minutes (about 15, `measured.json` "per_2min_target" 15.2). Part 1 has 3, part 2 has 1. The longest stretches
     without a card are 653.4 s (15:57.1 to 26:50.5, S09 to S15), 444.6 s (05:46.6–13:11.2), 346.6 s (00:00 to the
     first card) and 216.8 s (the last card to the end).
   - **Decided by Conny (2026-10-21), as recorded in `videos/ac215-l05-rag/REVIEW.md` gate 3:**
     「我觉得可以保留现在的密度」: keep the current density, which that record gives as 3–5 ponders per lecture plus a
     spoken recap and test questions. L15's four ponders are inside that series density and below AGENTS.md's aim.
   - **Recap:** S16 "Tear down, recap, test yourself" from 28:39.6 (107.53 s, 8 SAY lines).
     - 28:39.6–29:14.3: the clean-up checklist ("Before you leave, clean up.", cue 482): every endpoint, then their
       configurations and models; both buckets; the two ECR repositories, the deploy Lambdas and the pipeline; the
       access keys, users and roles; the SageMaker AI and Unified Studio domains.
     - 29:14.3–29:34.9: slide 40's recipe-to-factory chain ("The lecture ends on a factory:", cue 491), then today's
       five pictures, "a key on the laptop and a role in the cloud. A star is not a pin. … references draw the edges."
       (cues 493–496).
     - 29:34.9–29:46.3: part 1 in four commands (cue 497 "Under it, part 1 in four commands.").
     - 29:46.3–30:24.8: "Test yourself." (cue 501) and five questions (cards 1/5–5/5), then "The answers are in the
       exercises, and lecture 23 triggers the pipeline from GitHub." (cues 510–511, 30:18.8–30:24.8). The answers are in
       `exercises.md`.
4. **Narration written for the ear, with word-anchored cues** ✔.
   - **Spoken style:** commands, flags and identifiers are said in words ("dash dash prepare", "star", "less than 3",
     "or true", "slash persistent slash model", "M L M5 extra large", "A R M 64", "the who am I call"), with the literal
     form in the subtitle's `en_display` (`--prepare`, `"*"`, `"<3"`, `|| true`, `/persistent/model`, `ml.m5.xlarge`,
     `arm64`, `aws sts get-caller-identity`; `script.md` lines 256–270). Versions are said only as major versions and
     carry "at the time of recording" on screen; no prices.
   - **Size:** 139 SAY lines, 4,338 words (`measured.json` "narration"); all 139 are character-identical to the rendered
     `subs.json` texts, and each scene's SAY count equals its sidecar cue count. Kokoro `af_heart` at speed 0.9 gives
     152.0 wpm over the 1,712.0 s of voice (93.7 % of the runtime) and 142.4 wpm over the runtime. The `.srt` has 4,201
     words: spelled-out acronyms ("A R N" ×7, "M L" ×7, "A M D" ×6, …) display as one word.
   - **Anchors:** 576 `wait_until` anchors across the 16 scene files (S01–S16: 19, 25, 40, 53, 39, 33, 40, 38, 34, 40,
     45, 41, 22, 31, 45, 31; `common.py` none). None of the 16 render logs contains "anchor not found".
   - **Pronunciation:** the QA ASR watcher found no mispronunciation and one nit ("or true", still open). The L15 lexicon
     entries are in PR #109 (`a1dccf0` on `main`).
   - **Final ASR** (`report-asr.md`): 0 real mispronunciations or swallowed words; 0 cues whose speech starts more than
     1 s after the cue. One low-severity doubt, cue 454 at 26:59.0 ("No." heard as "Now", see "Open nits").
5. **Simulated-target-viewer QA over the full draft** ✔.
   - Seven watchers reviewed the 480p draft: two directors and two simulated target viewers ("newcomer"), one of each
     per part; a subtitle watcher, a follow-ups watcher and an ASR watcher. They worked from contact sheets, frames
     pulled from the draft, the scene code, the English `.srt`, both READMEs and the captures.
   - **70 timestamped findings: 1 must, 35 should, 34 nit.** The must (S14, the narration says the imports fail with
     nothing failing on screen) was fixed and verified on fresh frames; on the final cut the RED
     `ModuleNotFoundError: No module named 'sagemaker.processing'` is on screen at 24:22.5
     (`writer/s14_import_1462.5.png`). Each scene's fixes were checked by a skeptical verifier; several verifiers
     tightened or completed a fix (S01, S05, S06, S08, S09, S12, S14, S15). What stayed open is listed under
     "Whole-video QA".
6. **Measured checks** ✔. The numbers are under "Verified" (`measured.json`, measured on the final files).
   - **Duration:** 30:27.2 (1827.225 s), inside the series' 25–35 min. The parts are 16:27.3 (987.318 s) and 14:00.0
     (840.015 s). Their container durations sum to 0.108 s more than the full cut; their video frame counts sum to the
     clean cut's exactly (59,233 + 50,397 = 109,630), and their video streams to the full cut's (987.217 + 839.950 =
     1827.167 s). Part 1 ends on the S10 boundary (S01–S09 sum to 987.217 s), as `video.yaml`'s parts say.
   - **Loudness:** −16.1 LUFS integrated in all four files, LRA 2.1 LU (part 2: 2.2), true peak −2.6 dBTP (part 2:
     −2.5).
   - **Caption bounds** (`report-measured.md`, `report-visual.md`, `report-pairs.md`): every one of the 512 `.zh-en.srt`
     cues is one Chinese line above one Latin-only English line; the burn file `.zh-en.ass` has `WrapStyle: 2` and one
     `\N` per cue (512 of 512), Chinese at 50 px and English at 33 px. Measured with Noto Sans CJK SC at those sizes,
     the widest lines are 1,486 px English (`.zh-en.srt` cue 264, 15:38.6–15:45.1, the 94-character line) and 1,466 px
     Chinese (cue 227, 13:27.8–13:32.6), against 1,840 px usable; the burned frames show each on one line
     (`pairs-cue264-widest-en.png` at 15:42, `pairs-cue227-widest-zh.png` at 13:29; cue 264's English spans about
     x 444–1476, `zhen_longest_942.png`). The subtitle block starts at about y 990 and terminal/code panels end at about y 880 or
     higher; spot checks at 12 times (02:39–27:15) found no command a viewer must copy covered (`subs/check_A–D.png`).
   - **Music balance:** does not apply. L15, like L02–L14, has no score: `video.yaml` has no `music:` key.
   - **Subtitle sync** (`report-asr.md`, onset check): no cue's speech starts more than 1 s after its cue. The four
     base.en candidates (cues 112, 228, 348, 349) were base.en dropouts; large-v3-turbo places their speech within
     0.2 s of the cue start. Cue 454's speech starts about 0.4 s before the cue appears (harmless).

   **Human review:** the series waiver stands in for a listening sign-off.

   Listening sign-off: waived by Conny for the AC215 series (Explainer_Videos#29, 2026-10-15): 「不需要，我现在对视频质量很满意的」 — no human listened to this cut; the ASR round trip below is the substitute.
   Review moments optional since 2026-10-22 (AGENTS.md): 「我大概率是不会进行审片的，因为我觉得做得已经非常好了，就让bugbot来检查就好了」

   **ASR round trip** (`report-asr.md`, on the final clean cut):
   - faster-whisper `base.en` over the whole cut: 511 cues compared, 4,364 words recognised, 234 cues with some
     difference (`asr.json`, `asr.log`, `words-base.json`).
   - `large-v3-turbo` re-ran every doubtful cue on its own clip (cue ±0.6 s): the 30 cues in `lv3-clips.json` (59, 72,
     73, 76, 87, 92, 95, 122, 146, 157, 197, 218, 231, 240, 242, 267, 286, 307, 351, 367, 382, 402, 419, 427, 437, 446,
     454, 466, 474, 475) plus the stretches 111–113, 227–231 and 348–349 (`lv3-c111.json`, `lv3-c226.json`,
     `lv3-c347.json`; `lv3-c454.json`, `lv3-c454b.json`). Every one matches its subtitle apart from the designed
     `en_display` forms (76, 197, 466) and the homophones below (87 "Hours", 286 "weights"), except cue 454 (low doubt).
   - The 234 differences are recogniser noise (digits against words, split or joined compounds, homophones such as
     "ours"/"hours", "waits"/"weights"), the designed `en_display` differences (gate 4; cue 76 "the who am I call" shown
     as `aws sts get-caller-identity`; cue 466 "raw, clean and tfrecords dot zip" shown with the file names) and 1–2
     words counted across a cue boundary.

## Whole-video QA (480p draft, 30:04; times are *draft* times)

**Watchers and findings** (`l15-qa-wb4sr7n7g.output`, key `result`):

| watcher | must | should | nit |
|---|---|---|---|
| director, part 1 | 0 | 3 | 3 |
| newcomer, part 1 | 0 | 5 | 5 |
| director, part 2 | 1 | 7 | 4 |
| newcomer, part 2 | 0 | 6 | 3 |
| subtitles | 0 | 14 | 18 |
| follow-ups | 0 | 0 | 0 |
| ASR | 0 | 0 | 1 |
| **total** | **1** | **35** | **34** |

- **By target:** 32 subtitles, 31 scene, 6 narration, 1 shared code.
- **By kind:** 32 subtitle, 14 follow-along, 8 text, 5 picture, 3 pacing, 3 sync, 2 lexicon, 1 fact, 1 continuity,
  1 narration.
- **By scene:** S15 8, S12 7, S13 6, S03 5, S04 5, S16 5, S01 4, S06 4, S07 4, S08 4, S11 4, S14 4, S09 3, S10 3, S02 2,
  S05 2.
- **Facts:** the part-1 director traced every terminal panel he checked to its capture (laptop/00, 01, 10–19, 21–27,
  29, 31–32, 42–44, 46–48, `expected/md-predict-readme.txt`), every on-screen README line reference, and every README
  command typed as written and in order; the part-2 director checked every S13 command against README B 153–203, the
  panels against laptop/60, 68, 80, 81, 85, 89, 90, 92, and the console forms against README B 18–81. Both newcomers
  found the README order kept and no wrong command. All four found no real-looking id or key and no instructor name.
- **Follow-ups watcher:** found no `QA_FOLLOWUPS.md` for L15 (none ever existed; not in `git log --all`); issue #106 held
  only the "CHECKPOINT scenes" comment and no episode PR existed yet. It checked instead: no unfinished build in the
  16 draft render logs, and no FadeOut snap-back pattern in the scene files. It reported no issues.
- **Subtitle watcher:** read all 449 `zh.srt`, 508 `zh-en.srt` and 508 English cues; mechanical checks clean. Nine
  pairing problems in the bilingual band (06:09, 06:53, 08:33, 11:02, 19:29, 20:31, 20:39, 22:27, and a duplicated
  English line at 12:21–12:27) and 13 zh line breaks inside a word or term (对另 / 一个, 永远到 / 不了, IAM / 用户, …).
  It left two splitter cases out on purpose ("a small function AWS runs / on demand" at 27:13; "Docker" one cue apart
  at 21:09): toolkit `_split_like` behaviour, not yaml.
- **ASR watcher:** 508 cues against base.en, 25 doubtful cues re-run with large-v3-turbo; no mispronunciation, no
  swallowed word, no cue over more than 1 s of silence; one nit (cue 401, "and the or true" heard as "and though OR
  true").

**The must, and how it was fixed:**
- **M1, *draft* 24:05, S14: "The checks show the imports failing." with nothing failing on screen** (director, part 2).
  The panel showed only `sagemaker==3.29.0` (laptop/85) and "Pipfile.lock not found" (laptop/89); `script.md` had
  left laptop/86 out. **Fix** (`s14_shell.py`): laptop/86 lines 9–10 now print after laptop/85, `>>> from
  sagemaker.processing import…` with a grey row tag "import check · on 3.29.0" and `ModuleNotFoundError: No module named
  'sagemaker.processing'` in RED, both asserted against the capture. The verifier tightened the timing (a 0.5 s resize,
  no separate Indicate) after the fixer's version landed about 2 s after the phrase. On the final cut the cue runs
  24:19.2–24:21.1; the import line types from about 24:21.8, the RED error is fully on by about 24:22.0 (about 0.9 s
  after the cue ends, `verifier/s14_import_fine.png`), and the two lines are on screen at 24:22.5 (`writer/s14_import_1462.5.png`); the next strip follows
  (`writer/s14_import_1465.png`).

**The shoulds, examples by kind** (fixed and verified, except those under "Still open"):
- **Fact:** S09's "any one will do" now says "Any one stops the endpoint, but only the third also removes the tarball."
  (cue 252, 14:52.2); the verifier keeps the "only way that also removes the tarball" chip up about 8 s instead of 1.5 s.
- **Follow-along:** S04's "Pause and make both fixes" shows a checklist card with fix 1 and fix 2; S06's extra
  `aws s3 ls` no longer has angle brackets; S09's README delete lines have their brackets faded under bold grey crosses
  (`script.md` requires them typed as written); S11's search command stays pinned while the output scrolls; S12's
  `sh package-trainer.sh` stays on screen and its fix-B narration names the `chown` first, with the card rebuilt to
  match; S13's `<USER NAME>/<IMAGE_NAME>` no longer folds inside the placeholder and a chip says
  `IMAGE_NAME = cheese-app-data-collector`; S15's narration now covers the Lambda runtime erratum (cues 471–472, 28:00.0–28:09.5,
  `runtime="python3.12"`, line 297) and shows line 32 of the `--pipeline` traceback; S03's Option 2 erratum card stays
  about 4.7 s and says where the `-e` flags go.
- **Pictures and text:** S01's hook shows the two photos (`brie-2.jpg`, `brie-1.jpg`) and a chip "two brie photos · count
  the numbers, not the values"; S01's sample `▶ your turn` sits on `git clone`, not `aws configure`; S10's policy chips
  no longer overlap and the bucket name becomes a chip; S15's line 277 is folded so `.S3ModelArtifacts` is visible;
  S16's cards say "part 1/part 2" like the narration, and card 4 asks only the spoken question.
- **Subtitles:** 30 subtitle items applied in `g1.yaml`/`g2.yaml` by the narration/subtitle fixer;
  `python -m explainer.i18n check … --lang zh` printed OK.
- **Shared:** the S03 "AWS" label on the cloud box's top-left corner (`IdentityBadges`, `common.py:2101`) was reported
  against `common.py`. No QA fixer ran on `common.py`; the coordinator fixed it after the final-cut review (see "Fix
  round after the final-cut checks").

**Narration/subtitle fixer** (36 items): 31 applied, 2 applied in part, 3 nits left unchanged; two of those three were
then fixed by verifiers in the picture (S01 "this photo": a chip; S15 `--nums 50`), one stays open (S13 "or true").

**Still open after QA, and why:**
- **S09 *draft* 15:37, zh split** (subtitle nit): the fixer's alternative wording still splits "时间戳也是新的" under "but
  the JSON file keeps only the last name."; the verifier gave two wordings that split correctly but may not edit
  `g1.yaml`. On the final cut this is `.zh-en.srt` cues 265–266 (15:45–15:52). Accepted (A4).
- **S13 *draft* 23:19, "and the or true" heard as "and though OR true"** (ASR nit): narration edits were limited to must
  and should items, and the anchor `s13_push.py:444` would have to change with it. On the final cut, cue 402 (`.srt`)
  at 23:33.3. Accepted (A4).
- **S13, nothing names `cheese-app-data-processor` as the IMAGE_NAME when the scene repeats for the processor**
  (verifier's new nit): the chip has left by then; the "then steps 2–11 again" chip with `REPO=cheese-app-data-processor`
  implies it.
- **Partial fixes:** S12's README line-7 correction is up about 3 s, not the suggested 4 s (moving the strike earlier
  would run ahead of its phrase); S10's bucket form itself is still up about 1.5 s (its value is carried on as a chip);
  S14's import lines land about 1 s after the phrase.
- **S03 *draft* 03:24, the BLUE "AWS" label sits on the cloud box's corner** (director, part 1, should, the one
  `shared` item): fixed after the final-cut review (commit `abff08c`; see "Fix round after the final-cut checks").
- **Toolkit requests not acted on** (no `common.py` or `explainer/` fixer ran): `common.tracker()` re-centres its head
  (every scene uses a `fixed_tracker` workaround); `recorded_card()` cannot show a "…" gap (S08's local `gap_card()`);
  `Terminal.fold` splits `<…>` placeholders (S13's local `type_ph()`); `console_form` row spacing (S10); a `folds=`
  option for `code()` (S15).
- **Source drift (not rendered):** `script.md`'s SHOW lines no longer match the scenes in S01 (line 340, the sample
  tracker "Run Container · step 1 of 5"; the new chip), S06 (line 655, `s3://<your-bucket>/`), S07 (line 688, "shape
  from the part 2 Lambda"), S14 (line 1107, chip "exit the container first"; line 1117, "laptop/86 is not shown") and
  S16 (lines 1258, 1281, 1286, 1292: "Part A/Part B"; line 1297, the dropped `s3://…/tfrecords` question).
  `i18n/zh/GLOSSARY.md:60` and `glossary.yaml:459` quote S01's old zh wording; `exercises.md` uses "Part A/B" for the
  lecture halves and for its own sections.

## Final-cut checks (1080p60, 2026-11-05)

- **Tags** (`report-tags.md`): 30 tags, four or more frames each (`tags/t01…t30_*`, sheets `sheet_tNN_*.png`,
  `allcrops_*.png`), timed from the `events.json` sidecars plus the scene offsets; all labels correct, none
  overlapping, none on screen at its scene's end. Borderline t13; notes on t05 and t26 (item A2). The review-bot list
  it was given was empty.
- **ASR** (`report-asr.md`): intelligible throughout; 0 real problems; 1 low doubt (cue 454).
- **Visual** (`report-visual.md`, on the burned copy `.zh-en.mp4`):
  - 39 contact sheets (one frame every 3 s, 4×4 tiles), all read, plus targeted full-resolution frames.
  - All 16 scenes end empty (checked 0.1 s before each boundary; S09's last FadeOut brightened); no black or missing
    scene; every chapter start shows content.
  - `freezedetect` (picture only, −55 dB, 4 s): 59 near-static stretches, all under running narration except the four
    ponder timers (gate 3).
  - No clipping, no persistent overlap reported (three crossfades under 0.5 s at 17:45, 23:00, 28:09; the S03 "AWS" label
    overlap found by this record's writer was fixed and re-checked in round 2), no garbled glyphs (a
    one-frame ripple at 25:01.0 not visible at 25:00.5 or 25:01.5).
  - Two low items, F1 and F2, both accepted (A1, A5).
  - No instructor name on screen; keys, accounts and ECR URIs only as placeholders.
- **Pairs** (`report-pairs.md`): all 512 cues of `.zh-en.srt` read, zh against en. No meaning swap anywhere, including
  every condition or time clause (rule D9 held); one Chinese and one English line per cue; no break inside a command,
  path, flag or placeholder. Eight small drifts (accepted A4).
- **Measured** (`report-measured.md`, `measured.json`): all four MP4s decode with exit 0 and no error lines. Formats,
  loudness, subtitles, chapters, narration and the part split pass. The ponder density is decided under gate 3.

## Accepted items (coordinator decisions)

- **A1. The README card's `arn:aws:iam::123456789012:role/SageMakerExecutionRole`** (visual F1, S03; on screen about
  03:21.3–03:23.1 with the pill from about 03:22.0, `verifier/s03_arn_fine.png`, not 03:21–03:48 as `report-visual.md`
  gives it from its 3 s sheet): AWS's
  own documented dummy account, quoted verbatim from README A line 43 with an "AWS documentation placeholder" pill; not
  a real account. Every other on-screen ARN uses `000000000000` (04:42, 07:03) (`frames/t0201_readme_arn.png`).
- **A2. Lecture-tag judgement calls** (`report-tags.md`):
  - t13 (S09, "slides 11, 41", 14:44.8–14:50.7) leaves with the DELETE card at "The README gives three ways", while the
    gold cost meter (slide 11's picture in S01) stays about 11 s more, to about 15:01.8; `script.md` names the tag for
    the whole block (borderline, PLAUSIBLE).
  - t26 (S15, "slide 33", 26:38.1–26:44.7) comes in with its picture about 2 s before lines 326–327 light, not "while
    lines 326–327 are lit" as `script.md` says.
  - Note only: t05 (S05, "slide 13", 07:22.5) shows 1.2 s before the slide question and 5.4 s before the redrawn notebook
    (`script.md`'s block-level tag).
- **A3. Four ponders in 30:27.2** (0.26 per 2 minutes), below AGENTS.md's aim of one per 2 minutes. Accepted under
  Conny's 2026-10-21 decision to keep the current density of 3–5 ponders per lecture (「我觉得可以保留现在的密度」); see
  gate 3.
- **A4. Small zh/en drifts and QA nits left as is.** A re-burn costs about an hour; none changes meaning.
  - Eight `.zh-en.srt` pairs where one word or name sits one cue early or late in the Chinese (`report-pairs.md`, with
    the yaml item to fix each): 209–210 (12:08), 219–220 (12:46), 265–266 (15:45, the S09 QA nit), 295–296 (17:27),
    326–327 (19:22), 362–363 (21:17), 463–464 (27:26), 491–492 (29:05, the most visible: 「SageMaker AI 域」 one cue
    late).
  - The QA nits: `script.md`'s stale SHOW lines (listed under "Still open after QA"; the coordinator named S06 and S07),
    the S09 zh split (above) and S13's "or true" (cue 402, 23:33.3).
- **A5. Still pictures under narration** (visual F2): 28:01.1–28:09.8 in S15 after `--pipeline`, 8.6 s still (the
  erratum card, the "with keys" pill and the terminal) while the voice runs (`sheets/sheet_36.png`, `static_gaps.txt`);
  five shorter holds of 4.3–5.0 s at 02:22, 18:57, 20:07 (both "your turn" pauses), 21:30 and 30:22 (the final quiz
  card).

## Open nits (not ruled on one by one; left for the coordinator)

None blocks release. Each needs a narration, yaml, `script.md`, scene or toolkit change and a rebuild, which this record
does not make.
- **ASR listen item** (`report-asr.md`): cue 454 at 26:59.0, the answer to ponder 4, "No. The order comes from the
  references" is heard as "Now, the order comes…" by both models (probability 0.53 base.en, 0.55 large-v3-turbo; every
  other word ≥ 0.99). The subtitle shows "No." Options: a listen at 26:58, or reword ("No, it doesn't.") in a later
  round (`cue454.wav`, `lv3-c454.json`).
- **Homophones a listener may notice:** "ours" heard as "hours" (cues 87, 164, 203, 220, 258; e.g. 04:43.9 "Ours are
  placeholders."), by both models.
- **Chapters:** every start is the cumulative scene start rounded down (the largest gap 0.967 s, "Build and push: your
  own registry" at 22:35 for 1355.967 s). Harmless.
- **Part 2's length:** the brief's "13:59" is the truncated video length (839.95 s); the container rounds to 14:00.0.
- **Frame rate:** the cut is 60 fps (the 1080p60 scene renders, as in L02–L14); the repo default for new episodes is
  30 fps. The burned copy has one more video frame (109,631) than the clean cut; the audio is identical in length.
- **Stale previews:** the four `output/*_480p15*.mp4` QA-draft files were deleted before the episode PR.
- **No `QA_FOLLOWUPS.md`** for L15, and no Bugbot thread was copied into the episode folder.

## Verified (final render)

All numbers are from `measured.json` and the five reports, on the files in `output/` as they are now (written
2026-11-05 15:50–16:10 UTC).

- **Files:** H.264 High, yuv420p, 1920×1080 at 60 fps, AAC LC 48 kHz stereo at about 178 kb/s, video at about
  268–309 kb/s. Each decodes in full with exit 0 and no error, corrupt, invalid, non-monotonic or concealment lines
  (`decode_*.log`).

  | file | duration | video frames | size (bytes) | loudness | LRA | true peak |
  |---|---|---|---|---|---|---|
  | `ac215-l15-vertex-ml-workflows.mp4` | 1827.225 s (30:27.2) | 109,630 | 108,930,318 | −16.1 LUFS | 2.1 LU | −2.6 dBTP |
  | `ac215-l15-vertex-ml-workflows.zh-en.mp4` | 1827.225 s | 109,631 | 106,988,896 | −16.1 | 2.1 | −2.6 |
  | `ac215-l15-vertex-ml-workflows_part1.mp4` | 987.318 s (16:27.3) | 59,233 | 56,552,640 | −16.1 | 2.1 | −2.6 |
  | `ac215-l15-vertex-ml-workflows_part2.mp4` | 840.015 s (14:00.0) | 50,397 | 52,371,447 | −16.1 | 2.2 | −2.5 |

  Audio runs longer than video in every file: 58 ms (clean), 42 ms (burned), 101 ms (part 1), 65 ms (part 2);
  `report-measured.md`'s "58–101 ms" misses the burned copy. The 16 scene durations from the sidecars sum to 1827.167 s,
  equal to the full cut's video stream. The parts carry no burned subtitles (`measured_part1_t12.png`); the burned copy
  shrinks the picture so the captions sit below it (`measured_zhen_t12.png`).
- **Subtitles:** `.srt` 511 cues, `.zh.srt` 456, `.zh-en.srt` 512. Part 1 has 275 / 246 / 275, part 2 236 / 210 / 237;
  each language's parts sum to its full file.
  - In all nine files the indexes are sequential, the cues in order, inside the runtime, with no overlaps; the
    shortest are 1.000 s (`.srt`), 1.230 s (`.zh.srt`) and 1.000 s (`.zh-en.srt`); at most 2 lines per cue; longest
    lines 44 (en), 35 (zh) and 94 (zh-en English row) characters.
  - The last cue ends at 1824.826 s (30:24.8), 2.4 s before the cut ends.
  - No Chinese in any `.srt`; every `.zh.srt` cue has Chinese; every `.zh-en.srt` cue has both languages. The English
    words of `.zh-en.srt` equal the `.srt`'s in order (4,201 = 4,201).
- **Chapters:** 16 entries, titles equal to `video.yaml`'s in order, each start the floor of the running total of the
  scene sidecar durations (within 0.967 s). `chapters_part1.txt` (9 entries) and `chapters_part2.txt` (7, at 00:00,
  02:00, 04:06, 06:08, 07:35, 09:18, 12:12) match, part 2 offset by −987.2 s. `README.md` now carries them and the
  durations.
- **Scenes:** all 16 present and in order (the visual check matched every boundary to the cumulative `events.json`
  durations); every scene ends on an empty frame.
- **Narration:** 139 SAY lines, 4,338 words, 152.0 wpm over 1,712.0 s of voice; 576 anchors; no "anchor not found" in
  the 16 render logs.
- **Lecture tags:** 30, each checked on frames at fade-in, middle (and quarter points for spans over 10 s), before and
  after fade-out; none overlapping, none outliving its scene.
- **The QA must on the final cut:** the RED `ModuleNotFoundError` line is on screen at 24:22.5 under "The checks show
  the imports failing." (cue 414, 24:19.2) (`writer/s14_import_1462.5.png`, extracted by this record's writer).
- **Privacy:**
  - No instructor name on screen (sampled frames, `report-visual.md`) and none in the nine subtitle files or
    `transcript.md`; no 12-digit number and no `AKIA…`/`ASIA…` key pattern in them (the visual check's regex over
    `.zh-en.srt`; this record's writer re-ran the name, 12-digit and key-pattern greps over all nine files and the
    transcript: 0 matches).
  - On screen, keys appear as `PLACEHOLDER_NOT_A_REAL_*_000000000000` labelled "obviously fake · capture only" (17:48);
    `aws configure list` shows masked values (17:57); ECR URIs as `<account>.dkr.ecr…` (23:45) or `$ACCOUNT_ID`
    (23:12); no DLC registry digits (the serving image is "AWS prebuilt TensorFlow Serving image", 11:09); the one
    12-digit account is AWS's documentation placeholder (A1).
- **Provenance** (`ASSETS.md`):
  - Terminal lines come from the 2026-11-05 captures in `assets/terminal/`; each README command ran exactly as written,
    in README order, with extras tagged `extra`; nothing in a terminal panel is typed by hand.
  - Live: both clones at `077f4db` and `f165c6e`; `aws configure` and `sts get-caller-identity` without keys; every
    `docker-shell.sh` (the arm64 `exec format error` and the plain-line fix; the SDK 3 resolution and the `"<3"` fix,
    model-deployment built in 400.6 s with sagemaker 2.257.7); `--prepare` to its bucket error and the capture stub's
    export and tarball; the collector's 40 images, the processor's de-duplication and two TFRecord files, the trainer's
    one CPU epoch and its `PermissionError` on Linux; the ECR variable block and first call; every workflow flag to
    `cli.py:32`.
  - Tagged stand-ins: TensorFlow Serving 2.13.1 serving the export (brie, gruyere, and parmigiano as brie at 98 percent,
    14:11.8) and the SDK's offline pipeline JSON (`laptop/92`).
  - `recorded`: README A's `--predict` output. `illustration`: every console step (IAM, roles, buckets, SageMaker AI
    and Unified Studio domains, Training jobs, the pipeline graph), with the READMEs' field values, never a screenshot.

## Not claimed

- **No human listened to this cut** or watched it. The listening gate rests on the series waiver quoted under gate 6,
  and the audio was checked only by machine (the ASR round trip and the onset check). The cue 454 "No"/"Now" doubt is
  unresolved by ear.
- **The Chinese subtitles were reviewed by agents only:** the QA subtitle watcher, the narration/subtitle fixer, the
  scene verifiers and the final pairs check. No human translator or native reviewer read them.
- **No AWS step ran.** The recording had no account, no access key, no SageMaker and no billing. The console steps (IAM
  user, policies, access keys, the three roles, both buckets, the SageMaker AI and Unified Studio domains), every
  successful AWS CLI call, the S3 uploads, `--deploy` and the endpoint, `--predict` against SageMaker, `--delete`, the
  training job, the ECR push, the Processing job, the pipeline's upsert, run, caching, Lambda and Studio graph, and the
  clean-up are drawings, the README's own output (`recorded`), labelled stand-ins or narration. Whether today's console
  still matches the READMEs' field values was not checked. How the training job finds its data on SageMaker was not
  verified, and the video says so (cues 467–468, 27:44.7–27:50.2). Whether the deploy Lambda's default runtime really fails today is
  shown as a conditional note (28:00.0), not observed.
- **No Docker Hub login or push.** README B 155–162 is shown as commands only (no account or token). No Mac and no
  Apple-silicon run: the laptop was linux/x86_64; the arm64 lines' success on Apple silicon and slow emulation on Intel
  Macs are described, not captured. On Debian/Ubuntu `sh` is dash (the scripts' key check misbehaves): described from
  the digest author's test, not captured; the capture laptop was Alpine (BusyBox ash). The trainer's successful save
  after the permission fix was not captured (`task.py:303-322` is shown instead).
- **The visual check sampled one frame every 3 s**, plus targeted frames; motion between samples was checked only by
  `freezedetect`. It reported no overlap, yet the S03 "AWS" label overlap is visible on the final cut (Open nits), so
  its "no overlap" result is not complete; other small overlaps may remain unseen. The tags check used frames at fixed points of each tag's span, not a continuous scan.
- **Some QA fixes were verified only on previews** (720p `--at` frames and `--every 2` sheets, before the 1080p60
  renders), not one by one on the final cut; several subtitle fixes were checked by simulating the splitter on the
  yaml text. The final-cut checks cover them only by their own sampling and reading of every cue; this record's writer
  re-checked only the must (M1) on two final-cut frames and the S03 `shared` item on one.
- **Review bots:** no `QA_FOLLOWUPS.md` exists for L15, and nothing in this record checks Bugbot threads on an L15 PR.
- **`README.md` durations and chapters were filled in this pass** from `measured.json` and `chapters*.txt`; its chapter
  summaries were not reviewed by a separate agent.
- **One adversarial verifier pass** (an agent) re-measured this record's numbers (ffprobe, the decode logs' ebur128
  summaries plus a 60 s ebur128 sample, cue counts and words, sidecar durations, chapters, anchors, ponder times,
  freezes, the QA output's counts, script.md lines, commits) and re-opened frames for the S03 label, the A1 card and the
  S14 import line (`build/final-review/verifier/`). It corrected wrong times and counts in place. It did not re-run
  ASR, the pairs reading, the tags frames or the 39 visual sheets, and did not check the instructor name on screen.
- **Every check in this record is an agent's.**

## Fix round after the final-cut checks

- **S03 cloud-box labels (the QA `shared` should, missed by the round-1 visual check, found by this record's writer at
  03:26):** in `IdentityBadges.__init__` the grey "laptop" and blue "AWS" labels now sit on one line just above the
  cloud box's top edge (0.12 above it), so the box outline no longer runs through the letters (commit `abff08c`).
  `IdentityBadges` is used only by S03; `explainer.check` printed OK and S03 still runs 124.2 s. S03 was re-rendered at
  1080p and the cut re-stitched and re-burned (still 1827.2 s, 30:27).
- **Round-2 checks on the new files** (`report-visual.md`, `report-tags.md`, `report-measured.md`; round 1 kept as
  `report-*-round1.md`): the visual pass read all 39 sheets of the re-burned cut and confirms the labels sit above the
  box with no overlap and no other change; all 30 lecture tags have the same in/out times as round 1 to the
  millisecond and their 150 frames are pixel-identical to round 1; the measured checks find all four files decoding
  with no errors and the same durations, loudness and cue counts as round 1 (file sizes differ slightly). The ASR and
  pairs reports are from round 1: the narration and subtitles did not change.
