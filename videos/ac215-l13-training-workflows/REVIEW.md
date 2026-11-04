# Review record: AC215 · Lecture 13 — Advanced training workflows: a run is a record, a job is a rented machine

Follow-along of [dlops-io/model-training](https://github.com/dlops-io/model-training) `main` @ `b9aee1c` (the course
map's pin, still the head of `main` on 2026-10-23), `README.md` top to bottom, run with the two one-line Dockerfile
fixes today's build needs (`Dockerfile:2` → `python:3.13-slim-bookworm`, `Dockerfile:37` → `google-cloud-cli`, both
tagged `extra`), plus the lecture's two Colab notebooks (A, "Cheese Classification Models"; B, "Experiment Tracking
with W&B"), shown from their stored outputs. Claude Code sessions (Claude) produced it. Verified facts and unclaimed
reviews are kept in separate sections.

- **Origin and takeover:** another session wrote script v2 on branch `claude/ac215-l09-l13-batch` (issue #49). Its
  claim expired, and this coordinator took L13 over on 2026-11-02. This session wrote `scenes/common.py`, the scene
  contract (`build/SCENE-NOTES.md`, bench `build/common_test.py`) and S01–S15 with one fresh critic each (milestone
  commit `852e9b1`; the scene files themselves landed in earlier WIP commits on the branch),
  and the Chinese subtitles on 2026-11-04 (`45133af`), reusing the term decisions of the L13 exam edition.
- **Captures:** 2026-10-23 12:19–12:34 UTC (`ASSETS.md`, "terminal/"), in a fresh Docker Engine 29.8.2
  (`docker:29.8.2-dind`) standing in for a laptop with Docker Desktop, plus a Python 3.12 container standing in for
  Colab. That machine had **no GCP credentials, no W&B account, no GPU and no browser**. Every local step ran live
  (clone, secrets folder, both build failures and both fixes, the cockpit image, the tarball, the in-container checks,
  `python cli.py`'s errors). Every step that needs Google, Vertex AI or W&B was captured up to its documented failure;
  the job's first minute is replayed in a labelled local stand-in (`extra · local stand-in`).
- **QA draft:** the 480p draft (31:09; part 1 ended at 13:39).
- **Whole-video QA:** `/root/ac215-backup/tasks/l13-qa-wngtkslh1.output`, key `result`. 34 agents: seven watchers,
  12 scene fixers (S01, S03–S12, S15), one narration/lexicon/subtitle fixer and 14 scene verifiers (S01, S03–S15). The
  run log reads "L13: 51 issues from 7/7 watchers". Committed as `c9d3be6`.
- **After QA, by the coordinator:** the narration fixer had removed every spoken "scene N" reference (chapter names
  instead); the verifiers renamed most on-screen chips; the coordinator renamed the last three: S01 "preview · chapter
  One command" (`s01_hook.py:144`), S09 "→ Who submits" (`s09_package.py:199`), S15 "(Who submits: yours was 2)"
  (`s15_recap.py:44`). Lexicon PR #100 ("slip, copied", "Two GPUs") was merged to `main`, which the CI release renders
  with.
- **Finishing pass:** none. The coordinator's list of finishing-pass outputs for L13 is empty (`[]`).
- **1080p60 renders:** all 15 scenes. The render logs in `build/logs/` are dated 2026-11-04 11:26–12:48 UTC. None
  contains "anchor not found".
- **Final cut:** 31:44.4 (1904.440 s); parts 13:52.2 + 17:52.2. File times (UTC, 2026-11-04): the clean cut and the
  full-cut subtitles 13:28; the burned copy, chapters and transcript 14:22; the parts 14:24–14:27. The MP4s are not in
  Git (release assets).
- **Final-cut checks:** one round, five agent checks, no re-burn. The coordinator saved their returned text as
  `build/final-review/report-{tags,asr,visual,pairs,measured}.md`. All five reports exist and were read in full for
  this record. Their evidence is dated 14:29–15:35 UTC, after the last output file was written (14:27), so every check
  ran on the files now in `output/`. None of the five found a blocking defect.

**Conventions:**
- **Times** are mm:ss in the full cut (`output/ac215-l13-training-workflows.mp4`, 1904.440 s), except in
  "Whole-video QA", which keeps the 480p draft's times (marked *draft*).
- **Cue numbers** name their file: `.srt` (490 cues) or `.zh-en.srt` (503).
- **Evidence paths** are relative to `build/final-review/`. That folder is git-ignored and exists only in the producing
  session; a successor re-runs the checks to reproduce it.

## Content gates (AGENTS.md)

1. **Hook** ✔. S01 opens on a puzzle, not a value proposition: two real tables (notebook A cell 54, notebook B cell
   55, `recorded`) that crown different winners.
   - "Two notebooks from this lecture, run by the instructors:" (`.srt` cue 1, 00:00.0) … "the same 1,156 cheese
     photos, the same five models." (cue 3, 00:06.4); "Notebook A crowns the fine-tuned MobileNet, at 68.97 percent."
     (cue 4, 00:10.9); "Notebook B crowns the frozen MobileNet, also at 68.97 percent, and puts the fine-tuned one at
     62.93." (cues 5–6, 00:16.7).
   - The questions: "So which recipe is better, fine-tuning or freezing?" (cue 7, 00:26.6); "And from these two
     tables, can you even tell what was different?" (cue 8, 00:30.0); "One clue is visible: look at the epochs
     column." (cue 9, 00:33.9); "Hold that question." (cue 10, 00:37.1).
   - A second thread: the model "gets packed into a 4 kilobyte tarball" and "That command carries your W&B key."
     (cues 14–16, 00:47.1–00:54.7).
   - **Payoff:** S03, "The split has no seed, so every run is graded on a different 116." (cue 71, 04:36.5) and "the
     winner in notebook A leads by two photos." (cue 73, 04:44.3); S04, "The fine-tuned MobileNet trained 10 epochs
     here and 15 in notebook A" (cue 108, 06:59.4); S12's verdict, "So the verdict: these tables cannot crown a
     recipe." (cue 392, 25:30.0), "Seed the split, match the epochs, keep the code version, then compare." (cue 393,
     25:33.7); recap question one, "what did neither table write down?" (cue 482, 31:11.6).
2. **Intuition before formalism, with an animated mechanism for each core idea** ✔. `BRIEF.md` ("Visual set pieces")
   defines seven, each animated next to the commands it explains:
   - **V1, the training map (`TrainingMap`, S02, S06–S08, S15):** "Here is the map." (02:18.6), the Colab lane and the
     repo lane (02:20.0–02:28.3). S06 plays the trip: the cockpit "asks Vertex AI for a job" (10:15.2), "Vertex AI then
     starts a machine" (10:19.5), "installs your tarball, runs your trainer with your flags, and deletes the machine."
     (10:24.7–10:28.9). S09 proves the cockpit's role: "this container submits jobs, it never trains." (16:40.1). The
     recap: "The whole lecture on one map." (30:46.3).
   - **V2, the run ledger (`RunLedger`, S03, S04, S12):** notebook A's folder fills with "five files" (03:56.9–04:01.8);
     "the five rows become five runs on one shared epoch axis." (06:07.9); after ponder 2, "A callback: code that
     model.fit calls after every epoch." (06:28.0). S12 turns the columns into the lecture's seven items (from 24:50.2)
     and audits the repo run (25:04.7–25:25.0).
   - **V3, the assignment that goes nowhere (`ConfigBinding`, S05):** "The call wandb.init points the name wandb.config
     at the run's config drawer." (08:15.1); "it moves the name onto a new, loose dictionary." (08:23.1); "the run
     finishes with its drawer empty." (08:26.2). Backed by the live capture `colab/C38` (`the run's config: {}`) and the
     fix `C38b`.
   - **V4, the tarball trip (`TarballTrip`, S06, S09–S11, S15):** "Step two packs that file into a tarball," (10:03.3);
     "the tarball is 4,016 bytes." (17:58.0); "Vertex AI runs the tarball in your bucket, and your image never travels."
     (18:26.8); "the job's first step installs your tarball into Google's image." (22:05.3); "When the script ends, the
     machine is deleted, and the weights with it" (30:04.5–30:07.3).
   - **V5, three badges (`ThreeBadges`, S11, S15):** "Three badges take part in every job." (21:05.8); the key file
     "submits" (21:12.6); the W&B key "carried by hand inside the job's arguments." (21:21.5); "The middle lanyard is
     still empty." (21:24.8), filled after ponder 9: "your project's Vertex AI service agent" (21:44.7).
   - **V6, the GPU switchboard (`GpuSwitchboard`, S13):** "Three switches must agree." (25:47.7): accelerator, image,
     quota (25:49.7–25:59.1); "The chip lights only when all three are on." (26:03.0). The replay after ponder 11: "The
     T4 is attached, idle, and still billed." (27:01.9).
   - **V7, mirrored replicas (`MirroredReplicas`, S14):** "Each GPU holds an identical copy of the model, called a
     replica." (27:28.6); the global batch of 64 splits 32 + 32 (27:33.4); "averaged across a link called all-reduce"
     (27:42.3); "Variables created inside the scope are mirrored" (27:49.5).

   **Lecture slides:** a GREY "Lecture 13 · slide(s) …" tag top right in all 15 scenes (`report-tags.md`). The deck is
   redrawn, never shown.
   - The tags check found all 15 tags, worded correctly ("slide N" for S01, S07, S08, S11; "slides …" for the rest),
     none overlapping anything (2 fps sweep of the top-right region, 3,809 crops; four frames per tag in `tags/`), and
     every one fading out with its scene's final fade. The tightest gap is 7 px, S06's notebook-B box at
     10:51.5–11:08.5.
   - S01's tag ("slide 8") is up only on the closing beat, 01:19.2–01:24.7, as scripted. The other 14 run for the whole
     scene; S08's is the one the check flagged (accepted item A3).
   - `SLIDES.md` ("This video and the slides", map table) pairs every planned chapter with the deck's slides.
3. **Pause-and-ponder moments and a recap**: ✔ for the ponders, by Conny's decision for the series (accepted item
   A1); ✔ for the recap.
   - **Ponders:** eleven ponders and one quick predict, each a card followed by a silent timer. Card times are from
     `measured.json` (each scene's `events.json` plus its scene start); the timer starts 0.6 s after the card. Answers
     are from the `.srt`.

     | # | scene | kind | card (condensed) | card | timer | answer starts |
     |---|---|---|---|---|---|---|
     | 1 | S03 | ponder | `validation_percent = 0.2`, yet validation is 104 of 1,156: what did the code do? | 03:24.6 | 8 s | 03:33.2 "Both splits use test_percent." |
     | 2 | S04 | ponder | Five runs, only one has curves: what do the other four lack? | 06:21.4 | 6 s | 06:28.0 "A callback: code that model.fit calls after every epoch." |
     | 3 | S05 | ponder | After `wandb.config = {…}` and `.update(…)`, what does the run's config hold? | 08:05.1 | 8 s | 08:13.7 "Watch the name." (empty drawer at 08:26.2) |
     | 4 | S06 | quick | No GPU, no TensorFlow on your laptop: which machines will ever import TensorFlow? | 10:55.0 | 4 s | 10:59.6 "Two: the Colab runtime, and the container inside each Vertex job." |
     | 5 | S07 | ponder | Exported, closed the terminal, opened a new one: what does `echo ${#WANDB_KEY}` print? | 13:32.0 | 6 s | 13:38.6 "Zero: an exported variable exists only in that shell and its children." |
     | 6 | S08 | ponder | Every error is a 404 from a Debian mirror: which Dockerfile line picks your Debian? | 14:49.5 | 8 s | 14:58.0 "Line 2, the FROM line." |
     | 7 | S09 | ponder | You fix a typo in `task.py`: rebuild, re-package, or both? | 18:18.4 | 6 s | 18:25.0 "Only the package script." |
     | 8 | S10 | ponder | Your W&B key is part of the job's arguments: who can see it later? | 20:22.3 | 8 s | 20:30.9 "Anyone who can view jobs in this project," |
     | 9 | S11 | ponder | The job reads your private bucket, but your key never left the laptop: how? | 21:36.1 | 8 s | 21:44.7 "The second badge: your project's Vertex AI service agent," |
     | 10 | S12 | ponder | Of the seven things a run record should hold, which does this run keep? | 24:56.1 | 8 s | 25:04.7 "The model and its settings, yes." |
     | 11 | S13 | ponder | Accelerator added to the CPU block, log says `GPU Available: []`: why? | 26:51.2 | 6 s | 26:57.8 "Line 31 sets a CPU image, which has no CUDA." |
     | 12 | S14 | ponder | Two GPUs, `--batch_size=32`, 936 images: steps per epoch, images per GPU per step? | 28:50.4 | 8 s | 28:59.0 "The global batch is 64, so 15 steps, the last one partial," |

   - **Rate:** 12 cards in 31:44 (11 ponders and one quick predict), one every 2.64 minutes (`report-measured.md`),
     against AGENTS.md's aim of one per 2 minutes (about 16). The longest stretches without a card are 208.9 s
     (14:49–18:18, S08 to S09), 204.6 s (00:00 to the first card), 200.1 s (21:36–24:56) and 174.0 s (the last card to
     the end). The visual check (one frame every 3 s) found no defect in any card; its freezedetect pass found the voiceless still
     stretches at 08:05.6, 20:22.8, 21:36.6, 24:56.8 and 28:51.0 to be ponder timers.
   - **Decided by Conny (2026-10-21), as recorded in `videos/ac215-l05-rag/REVIEW.md` gate 3:**
     「我觉得可以保留现在的密度」: keep the current density, which that record gives as 3–5 ponders per lecture plus a
     spoken recap and test questions. L13's eleven ponders and one quick predict are above that series density and
     still below AGENTS.md's aim.
   - **Recap:** S15 from 29:43.7 (120.7 s).
     - 29:43.7–30:13.0: `cli.py`, the Python SDK route the README never mentions (fails on `GCP_REGION`, then on the
       missing key file); "And where is the trained model?" (30:02.5): nothing calls `model.save`; "Lecture 15 saves
       the model to a bucket; exercise 4 does it today." (30:13.0).
     - 30:18.4–30:44.4: the shutdown checklist ("Time to shut down; pause and work through the list."), ending with
       "delete the model-trainer key and rotate your W&B key, which traveled in a job." (cues 471–473).
     - 30:46.3–31:04.1: the spoken recap on the complete map, one sentence per idea (cues 474–480): a run keeps only
       what it records; curves need a callback, config goes into `wandb.init`; only the tarball travels, into Google's
       image, run as the service agent, the key in its arguments; three switches for one GPU; two GPUs split the batch
       and average gradients.
     - 31:09.3–31:29.6: "5 questions to test yourself." (cues 481–487), then "Answers are in the exercises." (there is
       no `exercises.md` in the episode folder; see "Open nits").
     - 31:32.0–31:39.9: the pointers to lectures 14 and 15 and the closing line.
4. **Narration written for the ear, with word-anchored cues** ✔.
   - **Spoken style:** follows `script.md`'s conventions: identifiers are said in words ("wand B init", "the key flag",
     "the region variable", "a batch size flag of 32"), with the literal form in the subtitle's `en_display`; versions
     that drift take "at the time of recording".
   - **Size:** 106 SAY lines, 4,371 words (`measured.json` "narration"), 106 voice blocks rendered. Kokoro `af_heart`
     at speed 0.9 gives 151.0 wpm over the 1,736.98 s of voice (91.2 % of the runtime) and 137.7 wpm over the runtime.
     The English `.srt` has 4,275 words (counted for this record), 96 fewer than the SAY lines, because captions show
     the short literal form (e.g. `--wandb_key` for "the key flag").
   - **Anchors:** 605 `wait_until` anchors across the 15 scene files (S01–S15: 25, 28, 51, 50, 28, 36, 60, 48, 44, 46,
     42, 41, 26, 44, 36). None of the 15 render logs contains "anchor not found".
   - **Pronunciation:** the QA ASR watcher found two real problems, both from Kokoro's G2P: "copied" sounded like "cop
     it" (*draft* 03:47) and "Two GPUs" lost its plural (*draft* 28:05). Two L13-only keys in `explainer/lexicon.yaml`
     (lines 412–413, `"slip, copied"` and `Two GPUs`) fix them; the verifiers checked them with
     `KokoroBackend.phonemize`, not by ear; they reached `main` in PR #100. On the final cut base.en hears cue 57
     (03:47.6) as "A small slip copied into the repo trainer" (`asr.json`), and `report-asr.md` reports "Two GPUs"
     heard in cues 441 and 446–450.
   - **Final ASR** (`report-asr.md`): 0 real mispronunciations or swallowed words, no cue whose speech starts more than
     1 s late. Four low-priority listen items are under "Open nits".
5. **Simulated-target-viewer QA over the full draft** ✔.
   - Seven watchers reviewed the 480p draft: two directors and two simulated target viewers ("newcomer"), one of each
     per part; a subtitle watcher, a follow-ups watcher and an ASR watcher. They worked from contact sheets, frames
     pulled from the draft, the current scene code, the English `.srt`, the README and the captures.
   - **51 timestamped findings: 3 must, 29 should, 19 nit.** All three musts (two distinct problems, both in S08) were
     fixed and verified on fresh preview frames, and the final visual check saw the S08 commands on screen long enough
     to copy. Each scene's fixes were checked by a skeptical verifier; several verifiers found and fixed a new or
     incomplete item. What stayed open is listed under "Whole-video QA".
6. **Measured checks** ✔. The numbers are under "Verified" (`measured.json`, measured on the final files).
   - **Duration:** 31:44.4 (1904.440 s), inside the series' 25–35 min. The parts are 13:52.2 (832.236 s) and 17:52.2
     (1072.221 s). Their container durations sum to 0.017 s more than the full cut (within ±0.5 s), and their video
     frame counts sum to the clean cut's exactly (49,932 + 64,332 = 114,264). Part 1 ends on the S08 boundary (S01–S07
     sum to 832.2 s), as `video.yaml`'s parts say.
   - **Loudness:** −16.1 LUFS integrated in all four files, LRA 2.3–2.4 LU, true peak −2.7 dBFS. Without a `music:`
     block the stitch normalises with `loudnorm=I=-16:TP=-1.5:LRA=11` followed by `alimiter=limit=0.71` (about −3 dBFS)
     and 192k AAC (`explainer/build.py:636`); the measured values sit within 0.1 LU of the −16 target, with true peaks
     under the −1.5 dBTP ceiling.
   - **Caption bounds** (`report-pairs.md` and `report-visual.md`; `report-measured.md` checked cue timing and the
     `Dialogue` counts, not on-screen bounds): every one of the 503 events in
     `.zh-en.ass` is exactly two lines, Chinese (50 px) above English (33 px), with wrapping off (`WrapStyle: 2`); the
     `.ass` text equals the `.zh-en.srt`. The widest lines are 1,624 px English (cue 240) and 1,500 px Chinese (cues
     221 and 240), against 1,840 px available. The burn uses `mode="scale"` (the default of `burn()`, `explainer/subtitles.py:1801`; the scale filter at `:1820`;
     `BAND = 0.13` at `:1756`):
     the picture is scaled to 87 % and the subtitles sit in a band beneath it, so they cannot cover a command; 12 spot
     checks (11:15 to 30:27) found none covered, including the `sed`, `export WANDB_KEY`, `sh -x cli.sh` and
     `gcloud ai custom-jobs` lines.
   - **Music balance:** does not apply. L13, like L02–L11, has no score: `video.yaml` has no `music:` key.
   - **Subtitle sync:** no cue's speech starts more than 1 s after its cue (first recognised word and the first 50 ms
     above −35 dB, `onsets.json`). The one flag, cue 431 (27:57.7, 1.38 s by base.en's word timing), has its energy
     onset at 0.24 s and turbo places "Review" at 27:57.56.

   **Human review:** the series waiver stands in for a listening sign-off.

   Listening sign-off: waived by Conny for the AC215 series (Explainer_Videos#29, 2026-10-15): 「不需要，我现在对视频质量很满意的」 — no human listened to this cut; the ASR round trip below is the substitute.
   Review moments optional since 2026-10-22 (AGENTS.md): 「我大概率是不会进行审片的，因为我觉得做得已经非常好了，就让bugbot来检查就好了」

   **ASR round trip** (`report-asr.md`, on the final clean cut):
   - faster-whisper `base.en` over the whole cut (2 threads): 490 cues compared, 4,482 words recognised, 200 cues with
     some difference (`asr.json`, `asr-base.log`, `asr-words.json`).
   - `large-v3-turbo` re-ran 40 doubtful cues, each cut from the final mix at ±0.3 s (`cues/turbo.json`), plus two
     wider windows (cue 114, 07:23.5–07:31.5; cue 431, 27:56.0–28:00.5).
   - The 200 differences break down as about 70 cues with a word counted across a cue boundary, about 80 spelling
     differences (digits, compounds, command names, apostrophes), 5 intended short captions (`wandb.run.save` said "run
     save", `--wandb_key` "the key flag", `GCP_REGION` "the region variable", `--batch_size=32` "a batch size flag of
     32", `test_percent` "the test percent"), 6 near-homophones and 13 base-model errors that turbo heard correctly.

## Whole-video QA (480p draft, 31:09; times are *draft* times)

**Watchers and findings** (`l13-qa-wngtkslh1.output`, key `result`):

| watcher | must | should | nit |
|---|---|---|---|
| director, part 1 | 0 | 7 | 5 |
| newcomer, part 1 | 0 | 4 | 3 |
| director, part 2 | 2 | 4 | 3 |
| newcomer, part 2 | 1 | 3 | 0 |
| subtitles | 0 | 9 | 8 |
| follow-ups | 0 | 0 | 0 |
| ASR | 0 | 2 | 0 |
| **total** | **3** | **29** | **19** |

- **By target:** 26 scene, 17 subtitles, 7 narration, 1 shared code.
- **By kind:** 17 subtitle, 10 follow-along, 7 pacing, 7 picture, 6 text, 2 continuity, 2 lexicon.
- **By scene:** S07 12, S08 7, S04 5, S11 5, S03 4, S01 3, S10 3, S15 3, S05 2, S06 2, S12 2, S09 1, S13 1, S14 1.
- **Facts:** the part-1 director checked the notebook tables and the two-photo margin, the split counts, the 9.50 % vs
  68.97 % sort slip, the C05/C05b/C38/C38b outputs, README lines 17, 43–44, 55–58, 71 and 80, captures 01–11 (the
  404/401 bucket checks, the 40/0 key lengths) and the commit message "removed ca;llback", and found them right. The
  part-2 director checked the 22 `Err` 404 rows, "Building 314.2s (19/19) FINISHED", the 4016-byte tarball and its
  owners, the 2.59 GB image, the manifest sizes (4.31, 8.93, 7.61 GB), "yours was 2" / "yours was 47", the `sh -x`
  trace and 936 = 14 × 64 + 40, and found them right. Both directors and the part-1 newcomer found no instructor name
  and no real-looking key on screen.
- **Follow-ups watcher:** found no `QA_FOLLOWUPS.md` for L13 (none ever existed on any branch). It checked the 15
  render logs (all complete), grepped the scenes, `SCENE-NOTES.md` and `BRIEF.md` for TODO/FIXME/bugbot (none), and
  reported no issues. Bugbot threads on the L13 PR were never copied into a file, so it could not check them.
- **Subtitle watcher:** `explainer.i18n check --lang zh` OK; no banned terms (镜像, 作业, 存储桶, 回调, 配置), no
  timing faults, `en_display` coverage complete. It found line breaks inside a word or phrase (e.g. "pin / 住", "Apple /
  芯片", "管 / 服务器"), four zh/en pairs out of step (00:57, 07:17, 20:14, 24:52), and one cue pair that showed the
  same English sentence twice (13:44). All fixed in `i18n/zh/narration/g1.yaml` and `g2.yaml`.
- **ASR watcher:** 479 cues, 201 differing under base.en; 18 re-run with large-v3-turbo; two real problems ("copied",
  "Two GPUs", gate 4); no cue more than 1 s late.

**The musts, and how each was fixed** (both in `s08_build.py`):
- **M1, *draft* 14:56, S08: fix 1's command was never readable in full** (director and newcomer, part 2, both must).
  `sed -i '2s/python:3.13-slim-bullseye/python:3.13-slim-bookworm/' Dockerfile && sed -n '1,2p' Dockerfile` was typed
  with a hard ` \` fold into a 3-row strip and scrolled away while being typed. **Fix:** typed with `soft=True`, the
  terminal at 20 pt from beat 2 (72 characters a row), the strip grown to 4 rows (2 command + 2 output), the corner map
  moved up 0.3. The verifier saw the prompt, the whole command, both output lines and ▶ your turn at "pause and make
  it" (scene time 82.46 s).
- **M2, *draft* 15:17, S08: fix 2's command was pushed off by its output** (director must; newcomer should). **Fix:**
  `resize(self, t, 6)` before `type_cmd(..., c24.cmd, soft=True)`, the layered map moved up 1.0, asserts on the row
  count and clearance. Verified at scene time 103.46 s: prompt, 3 command rows, 3 output rows, ▶ your turn.
- The same fix pass also grew the first terminal for the `docker-shell.sh` sed (*draft* 13:50, should). On the final
  cut the visual check found the S08 `sed` commands (14:03, 15:15, 15:30) on screen long enough to copy.

**The shoulds, examples by kind** (fixed and verified, except those under "Still open"):
- **Follow-along:** S07's step-4 `your turn` no longer lingers through step 5 and step 5's tag holds about 2.5 s; the
  `ls -la` second page holds 3 s; S07 and S11 now say what to do if your W&B key is not 40 characters ("One fix,
  untested here: raise the wandb pin in setup.py…"), with a matching chip.
- **Pacing:** the hook's four 4.7–5.7 s stills now carry cell flashes (longest still 3.8 s); notebook B's cell-34
  sign-in panel reads about 3 s; S11's `--help` traceback about 3 s; S15's missing-key error about 2.2 s; S07's
  "honest note" card builds line by line.
- **Pictures:** the S03, S04, S05 ponder cards and the S06 quick-predict card no longer hide the code or tiles they
  ask about (S03 got a narrow cell-26 panel; S06 lifts the map 0.35 and uses a compact card).
- **Continuity:** S05's tracker reads "repo preview · cloned later" over the repo code; S11's title-bar tag drops to
  plain `extra` during the real-registry manifest check.
- **Text / narration:** every spoken "scene N" became a chapter name; the on-screen chips followed (verifiers in S03,
  S06, S07, S10, S11, S13; the coordinator for S01, S09, S15).
- **Subtitles and lexicon:** as above and gate 4.

**Nits:** fixed, except those listed next. Examples: S04's cell-52 URL now ends in a `<run-id>` placeholder with a
ring; S09's `tar tzvf` listing holds about 2.6 s; S10's ponder card says "see", matching the narration; S12's ledger
moved down with wider columns; the zh 运行时 ambiguity at 01:07 was reworded; the S07 roles cue (*draft* 11:57), which
the subtitle watcher could not re-pair by zh wording, was fixed by the narration fixer through the English display
line (`en_display`), and the final `.zh-en.srt` cue 193 (12:03.2) pairs 角色是 Storage Admin、AI Platform Admin with
"with Storage Admin, AI Platform Admin".

**Still open after QA, and why:**
- **S06 *draft* 10:33, the "the job can't see your laptop" card covers the laptop** (director nit). Fixer and verifier
  both measured that no placement fits (the card is 4.3 units tall, the free band about 2.3) without cutting the
  card's content, a script decision. Accepted by the coordinator (A5).
- **S03 *draft* 02:40, "from the course page" vs the study-guide chip** (newcomer nit): needs a `script.md` and anchor
  change; nits did not qualify for SAY edits. Accepted (A5).
- **S07 *draft* 12:51, the bucket title `your-bucket-placeholder` touches its box edges** (director nit, shared code
  `TrainingMap.name_bucket`, `common.py:2214`): no `common.py` fixer ran; unchanged. Not flagged by the final visual
  check.
- **`script.md` and glossary notes not updated:** the SHOW and PONDER lines still quote old chip texts (`script.md`
  lines 307, 400, 566, 633, 811, 829 "read it later", 902, 993, 1075), and `i18n/zh/glossary.yaml:206–209, 317–320,
  437, 467–470, 522, 562–565, 570–572` / `GLOSSARY.md:135, 177, 221, 234, 252, 272, 274` still carry old examples with
  "scene 7/9/10/11" (第 N 个场景). None of these files is rendered; the scenes and
  `g1.yaml`/`g2.yaml` hold the current text.

## Final-cut checks (1080p60, 2026-11-04)

- **Tags** (`report-tags.md`): no hard defect. 15 tags, four frames each, none overlapping, none on past its scene;
  the review-bot list was empty (`[]`). One judgement item: S08 (accepted item A3).
- **ASR** (`report-asr.md`): intelligible throughout; 0 real problems; four low-priority listen items (Open nits).
- **Visual** (`report-visual.md`), on the burned copy (`.zh-en.mp4`):
  - 40 contact sheets (635 frames, one every 3 s), all read, plus about 30 full-size frames and crops.
  - All 15 scenes in order; every scene ends on a blank frame (luma 13–18); the last frame is plain background.
  - No clipped or overlapping text at rest, nothing outside the frame, no garbled glyphs, no tofu in the CJK lines, no
    tag stuck on screen.
  - Two sub-second cosmetic findings (accepted item A4).
  - No instructor name on screen or in the `.srt`/`.ass` files; keys only as the placeholder; projects and buckets
    only as stand-ins.
- **Pairs** (`report-pairs.md`): all 503 cues of `.zh-en.srt` read. No meaning swap anywhere. Three small zh/en
  offsets and two cues that repeat a string in both rows (accepted item A2). Line counts, widths, the `.ass`/`.srt`
  match and the part split all pass.
- **Measured** (`report-measured.md`, `measured.json`): all four MP4s decode with 0 errors and 0 warnings. Formats,
  loudness, subtitles, chapters and the part split pass. The ponder density is decided under gate 3.

## Accepted items (coordinator decisions)

- **A1. Eleven ponders and one quick predict in 31:44** (one card every 2.64 minutes), below AGENTS.md's aim of one
  per 2 minutes. Accepted under Conny's 2026-10-21 decision to keep the current density of 3–5 ponders per lecture
  (「我觉得可以保留现在的密度」), which L13 exceeds; see gate 3.
- **A2. Residual subtitle pairing items** (`report-pairs.md`, `.zh-en.srt`). None reverses a meaning; a re-burn costs
  about an hour of render for a cosmetic gain.
  - Cues 64–65 (03:58.5, S03): the Chinese lags; 模型、权重 sit in cue 65 while "the model, its weights," is in cue 64.
  - Cues 317–318 (19:40.9, S10): the Chinese runs ahead; 从来没加载过 shows in cue 317, "never loaded" in cue 318.
  - Cues 471–472 (29:43.7, S15): the Chinese lags; `cli.py` is in English cue 471 but Chinese cue 472.
  - Cues 367 (22:59.96) and 393 (24:28.07) show the error string `API key must be 40 characters long, yours was 2` and
    the W&B project name `cheese-training-vertex-ai` verbatim in both rows. This follows the glossary's decision to
    keep error and status text verbatim.
  - Not a defect, per the A6 notes in `g1.yaml:11` and `g2.yaml:10–11`: some Chinese lines write identifiers as
    spoken ("test percent", "model dir 参数", "region 变量").
- **A3. S08's "Lecture 13 · slide 24" tag stays the whole scene** (13:52.2–16:17.2), although the SHOW line ties it to
  V1's cockpit box, which leaves at about 14:01.6 (`tags/s08_v1_sheet.png`). Accepted: the whole scene builds that
  same container.
- **A4. Visual-pass cosmetic items** (`report-visual.md`), both under a second:
  - F1, 29:27.9–29:28.7 (S14): an `Indicate` pulse scales the gold tag's second line ("check the Vertex AI pricing
    page before you press enter") past its rounded frame (`frames/crop_tag_indicate_29m27-29m28.png`).
  - F2, about 00:45–00:47 (S01): the chip `mobilenetv2_train_base_True` crosses the "notebook A · Colab" card title
    while moving (`frames/crop_hookchip_stack_00m44-00m46.png`).
- **A5. QA nits left as is:**
  - S06: the "the job can't see your laptop" card covers the laptop and bucket of the map from about 10:35 (cue 162,
    "The job cannot see your laptop", 10:35.3); frame at 10:40.5 in `writer/s06_card1_10m40.png`. No placement fits
    without cutting the card (see "Still open"). The coordinator's note calls it the "S06 ponder card"; it is the
    card before the quick predict, which itself was fixed.
  - S03: "Open notebook A from the course page" (cue 43, 02:40.3) while the chip names the study guide.
- **A6. The instructor's name is masked** everywhere on screen and in subtitles (series rule): the notebooks' cell 0
  reads `<course instructor>` / `<notebook author>` and the W&B user `<W&B user>` (`ASSETS.md`), the Chinese says
  授课老师. Cue 1 says "run by the instructors" (generic plural). `video.yaml`'s Bilibili description credits the
  course staff by name, as L02–L11 do; that text is not on screen.

## Open nits (not ruled on one by one; left for the coordinator)

None blocks release. Each needs a narration, yaml, `script.md` or scene change and a rebuild, which this record does
not make.
- **ASR listen items** (`report-asr.md`, `.srt` cue numbers):
  - Cue 114 (07:27.0) "then run cells 64 and 66; pause and do it.": the speech starts about 07:26.4, so the caption
    appears about 0.6 s after "then run" is spoken (this block has no inner word marks); base.en heard nothing, turbo
    every word (`cues/cue114.wav`).
  - Cue 393 (25:33.7) "Seed the split…": heard as "See the split"; the final /d/ is weak (`cues/cue393.wav`).
  - Cues 352 (22:56.0) "billed machine time" and 416 (27:01.9) "still billed": both models hear "build".
  - Cue 95 (06:03.1) `wandb.init`: a one-off weak "init" (elsewhere heard as "wand be in it").
- **Long narrated stills** (`report-visual.md`, freezedetect, narration running): 23:25.5 (11.2 s, S11, the wandb pin
  card), 22:49.4 (8.7 s), 23:16.8 (8.7 s), 00:29.2 (8.4 s, the hook question), 25:05.6 (8.4 s, S12 verdict), 24:27.9
  (7.6 s).
- **Verifier nits left as is:** S08, the line-37 text flying up to "your new line 37" crosses the `ed3` editor chip for
  about 0.8 s (scene time about 101 s, near 15:33); S12, the bottom ~40 % of the frame stays empty from about 87 s to
  108 s scene time (about 25:04–25:25) until the folder card arrives; S07's "why" card shows two lines with an empty row
  for about 4 s before the third line (deliberate).
- **The bucket title on the map** touches its box (S07 onward, `common.py:2214`), see "Still open after QA".
- **Stale source text:** `script.md`, `i18n/zh/glossary.yaml` and `GLOSSARY.md` lines listed under "Still open after
  QA"; the docstrings at `s01_hook.py:14` ("preview · scene 10") and `s09_package.py:14` ("scene 11") are comments,
  not rendered.
- **`SLIDES.md` "This video and the slides"** still opens "The video is not scripted yet"; its map is from the
  digest's planned chapters.
- **No `exercises.md`** in the episode folder. The video says "Exercise 1 adds a small callback." (25:37.9), "exercise
  4 does it today" (30:13.0) and "Answers are in the exercises." (31:29.6). This record did not check whether the study
  guide holds those exercises.
- **No `QA_FOLLOWUPS.md`** for L13, and no Bugbot thread was copied into the episode folder.
- **Chapters:** every start is the cumulative scene start rounded down (e.g. S08 at 832.2 s = 13:52). Harmless.
- **Frame rate:** the cut is 60 fps (the 1080p60 scene renders, as in L02–L11); the repo default for new episodes is
  30 fps. The burned copy's video starts at 0.000 s with one more frame (114,265) than the clean cut (start 0.021 s);
  the audio is identical.

## Verified (final render)

All numbers are from `measured.json` and the five reports, on the files in `output/` as they are now (written
2026-11-04 13:28–14:27 UTC).

- **Files:** H.264 High, yuv420p, 1920×1080 at 60 fps, AAC LC 48 kHz stereo at about 173 kb/s, video at about
  279–321 kb/s. Each decodes in full with exit 0 and no error or warning lines (`<name>.decode.log`).

  | file | duration | video frames | size (bytes) | loudness | LRA | true peak |
  |---|---|---|---|---|---|---|
  | `ac215-l13-training-workflows.mp4` | 1904.440 s (31:44.4) | 114,264 | 116,199,452 | −16.1 LUFS | 2.4 LU | −2.7 dBFS |
  | `ac215-l13-training-workflows.zh-en.mp4` | 1904.440 s | 114,265 | 114,209,387 | −16.1 | 2.4 | −2.7 |
  | `ac215-l13-training-workflows_part1.mp4` | 832.236 s (13:52.2) | 49,932 | 48,297,931 | −16.1 | 2.4 | −2.7 |
  | `ac215-l13-training-workflows_part2.mp4` | 1072.221 s (17:52.2) | 64,332 | 67,909,582 | −16.1 | 2.3 | −2.7 |

  The 15 scene renders sum to 1904.4 s (`events.json`).
- **Subtitles:** `.srt` 490 cues, `.zh.srt` 427, `.zh-en.srt` 503. Part 1 has 209 / 182 / 220, part 2 281 / 245 / 283;
  the English parts sum to the full file (209 + 281 = 490) and the bilingual parts join to the full file cue for cue
  (220 + 283 = 503, `report-pairs.md`).
  - In all nine `.srt` files the cues are numbered 1..N and in order, inside the runtime, at least 0.8 s long (the
    shortest is 1.000 s), with no overlaps.
  - The last cue ends at 1903.180 s, 1.3 s before the cut ends (part 1: 830.366 s; part 2: 1070.98 s).
  - The English stream of `.zh-en.srt` equals the `.srt` word for word (4,275 words, checked for this record); the
    `.ass` text equals the `.zh-en.srt` for all 503 cues; the three `.zh-en.ass` files hold 503, 220 and 283
    `Dialogue` lines.
- **Chapters:** 15 entries, titles equal to `video.yaml`'s in order, each start within 1 s of the running total of the
  scene renders (rounded down). `chapters_part1.txt` (7 entries) and `chapters_part2.txt` (8, at 00:00, 02:24, 04:49,
  07:13, 09:45, 11:49, 13:16, 15:51) match, part 2 offset by −832.2 s. `README.md` now carries them.
- **Scenes:** all 15 present and in order; the chapter starts match the scene durations, so no scene is missing or
  doubled.
- **Narration:** 106 SAY lines, 4,371 words, 151.0 wpm over 1,736.98 s of voice; 605 anchors; no "anchor not found"
  in the 15 render logs.
- **Lecture tags:** 15, each found, none overlapping, none left on past its scene (`tags/`, `sweep_result.json`).
- **Privacy:**
  - No instructor name on screen (sampled frames) or in the subtitle text (`report-visual.md`, `report-measured.md`).
  - Every key shown is `PLACEHOLDER_NOT_A_REAL_WANDB_KEY_0000000` or a 47-character `…_LONGER` variant; no key-like
    token of 32 or more characters in any subtitle track.
  - Projects and buckets appear only as `your-gcp-project`, `your-bucket-placeholder` or the README's `[REPLACE…]`
    text; `ac215-project` / `cheese-app-models` only on notebook illustrations labelled "replace this with yours".
  - The key in the `secrets/` listings is an obviously invalid 415-byte stand-in, moved out before the first
    container start, and S07 says so.
- **Provenance** (`ASSETS.md`):
  - Terminal lines come from the 2026-10-23 captures in `assets/terminal/`; each README command ran exactly as written,
    in README order, with extras tagged `extra`.
  - Live: the clone at the pin, both build failures (`21`: 22 packages 404 at step 2; `23`: `google-cloud-sdk` has no
    installation candidate) and both fixes (`22`, `24`, diff `25`), the cockpit start with no key (`26`, including
    `No module named 'tensorflow'`), the 4016-byte tarball and its 8 entries (`30`), `Using endpoint …` and the `sh -x`
    trace with the key in `--args` (`40`), `cli.py`'s `KeyError: 'GCP_REGION'` and missing-key error (`60`), the
    empty-key and name-conflict extras (`70`, `71`), and the Colab stand-in's `wandb.config = {...}` → `{}` and its fix
    (`C38`, `C38b`).
  - Local stand-ins, tagged `extra · local stand-in`: `pip install` of the tarball in plain Python 3.10 and the
    trainer's `wandb.login` with three keys (`80`–`87`).
  - `recorded` from the notebooks' stored outputs (instructors' runs, October 2025): the two tables, the split counts,
    the W&B banners and the 2_block run history.
  - The GCP console, the W&B pages, Colab and the Vertex job are drawings tagged `illustration`; the job's log lines
    come from `task.py`'s own prints.

## Not claimed

- **No human listened to this cut** or watched it. The listening gate rests on the series waiver quoted under gate 6,
  and the audio was checked only by machine (the ASR round trip and the onset check). The four ASR listen items are
  unresolved by ear, and the two lexicon fixes were checked by phonemizer and ASR, not by a listener.
- **The Chinese subtitles were reviewed by agents only:** the QA subtitle watcher, the narration/subtitle fixer, the
  scene verifiers and the final pairs check. No human translator or native reviewer read them.
- **No Google Cloud or W&B step ran.** The recording had no credentials, no W&B account, no GPU and no browser. The
  console steps (Vertex AI API, GPU quota request, service account, roles, key, bucket), `gsutil cp` success, job
  submission with `sh cli.sh` and `sh cli-multi-gpu.sh`, the running Vertex job and its logs, the GPU and multi-GPU
  runs, and the W&B dashboard are drawings, the code's own prints, notebook outputs or narration. Whether a real job
  prints a W&B "logged in" line, what today's W&B key length is, and whether Google's prebuilt images still carry
  scikit-learn and a working `wandb==0.15.11` were not checked (`ASSETS.md` findings 5–7). The "untested fix" for a key
  that is not 40 characters is said to be untested on screen.
- **No Colab run.** The notebooks' results are their stored outputs; the stand-in ran only cell 5 and the offline
  `wandb.config` check.
- **No Docker Desktop and no Mac run.** The laptop was Docker Engine 29.8.2 (dind) on linux/amd64; Mac-specific lines
  (the `sed -i ''` form, Apple-chip notes, file ownership) are explained, not run.
- **The visual check sampled one frame every 3 s**, plus targeted frames. Motion between samples was checked only by
  `freezedetect` (whose threshold can miss small motion) and by the tags check's 2 fps scan of the tag region.
- **Some QA fixes were verified only on previews** (`-q m` or 720p frames, before the 1080p60 renders), not one by one
  on the final cut; the final-cut checks cover them only by their own sampling.
- **Lexicon PR #100 on `main`:** stated by the coordinator; this record saw the two entries in the working tree
  (`explainer/lexicon.yaml:412–413`) but did not confirm the merge against a fetched `origin/main`.
- **Name search:** the checks grep text in the subtitle files, not burned-in pixels; on screen, the mask rests on the
  edited extracts and the sampled frames.
- **Review bots:** no `QA_FOLLOWUPS.md` exists for L13 and nothing in this record checks Bugbot threads on the L13 PR.
- **`README.md` was written in this pass** from the episode's own files; its chapter summaries were not reviewed by a
  separate agent.
- **Every check in this record is an agent's.**
