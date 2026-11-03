# Review record: AC215 · Lecture 9 — CI & unit testing: the pre-commit gate

Follow-along of [dlops-io/cheese-app-ci-cd](https://github.com/dlops-io/cheese-app-ci-cd) `main` @ `b8458ff` (README
Parts 1–4 and Docker Cleanup) and of the guest lecture's babykev at `4a14085`, walked on its tags `step-00` …
`step-05b` with `walk.md` from babykev-walk @ `82adb14`. Claude Code sessions (Claude) produced it. Verified facts and
unclaimed reviews are kept in separate sections.

- **Origin and takeover:** another session built the episode on branch `claude/ac215-l09-l13-batch` and ran QA round 1
  there. It was imported into the series branch in `bbdf2ff` (2026-11-02 22:33 UTC) and taken over on 2026-11-02
  (issue #46).
- **Captures:** 2026-10-19 (`ASSETS.md`). The cheese track ran 21:21–21:40 UTC in a fresh Docker Engine 29.8.2
  (`docker:29.8.2-dind`) standing in for a laptop with Docker Desktop. The babykev track ran 21:42–22:30 UTC in a fresh
  container **without Docker**, with uv 0.13.2 and just 1.59.0.
- **QA draft:** the 480p draft (30:09.4; part 1 ended at 18:01).
- **Whole-video QA (round 2):** `/root/ac215-backup/tasks/l09-qa-wvlqd4zmv.output`, key `result`. The run used 34
  agents: seven watchers, 12 scene fixers, one narration/subtitle fixer and a verifier for 14 scenes (all but S02, which
  had no finding). Committed in `f489a21` (2026-11-03 04:14 UTC), together with two post-QA narration and glossary
  edits (see M1).
- **Finishing pass:** none. The coordinator's list of finishing-pass outputs for L09 is empty.
- **1080p60 renders:** all 15 scenes. Render logs are `build/logs/`, dated 2026-11-03 04:20–05:33 UTC. None contains
  "anchor not found".
- **Final cut:** 30:22.4, parts 18:11.5 + 12:11.0. The full-cut subtitles (`.srt`, `.zh.srt`, `.zh-en.srt`,
  `.zh-en.ass`) are committed in `f29303b` (06:17 UTC); the part subtitles, chapters and transcript in `051fe99`
  (07:23 UTC). The clean cut was written at 06:10 UTC, the burned copy at 07:16 UTC and the parts at 07:19–07:21 UTC.
- **Final-cut checks:** five agent checks. The coordinator saved their returned text as
  `build/final-review/report-{tags,asr,visual,pairs,measured}.md`. All five reports exist and were read in full for
  this record. None found a blocking defect. Their decision items are recorded under "Accepted items" and "Open nits".

**Conventions:**
- **Times** are mm:ss in the full cut (`output/ac215-l09-ci-testing.mp4`, 1822.417 s), except in "Whole-video QA",
  which keeps the 480p draft's times (marked *draft*).
- **Cue numbers** name their file: `.srt` (497 cues) or `.zh-en.srt` (515).
- **Evidence paths** are relative to `build/final-review/`, which is git-ignored and exists only in the producing
  session. A successor re-runs the checks to reproduce it.

## Content gates (AGENTS.md)

1. **Hook** ✔. S01 opens on a broken thing from the repo's own history, not on a value proposition.
   - "Here is a line of code that a Harvard instructor committed, live, in class." (cues 1–2, 00:00.0)
   - "This line takes the square root of twice that." (cue 5, 00:10.9), then "The answer was just wrong." (cue 7,
     00:16.4).
   - The question the video answers: "Before that commit exists, who gets to say no," (cue 9, 00:20.0).
   - **Payoff:** "Today we build one on your machine, and watch it refuse a commit." (cue 13, 00:31.2). The refusal
     comes at the end of part 1: "The commit fails twice:" (cue 293, 17:47.7), then "your machine now says no." (cue
     296, 17:59.0).
2. **Intuition before formalism, with an animated mechanism for each core idea** ✔. `BRIEF.md` ("Visual set pieces")
   defines seven. Each is animated next to the commands it explains:
   - **V1, the gate, the vault and the gate table (S01, S09, S11, S14):**
     - The commit envelope and turnstile appear in S01 (from 00:18).
     - The nine named arches come in S09 ("The config names nine hooks:", cue 265, 16:02.7), and babykev's four in
       S11 (cue 340, 20:38.3).
     - The gate table opens empty in S03 and fills row by row: first row at 12:26.2 (cue 204), the system row outside
       the turnstile at 15:26.8 (cue 254), full at 28:05.4 (cue 460).
   - **V2, one request, three sizes of test (S03, S08):** the PINK request through unit, integration ("in process",
     cue 57, 03:18.1) and system ("crosses a real network wire", cue 63, 03:39.4); the pyramid (03:48.8); the
     hermetic border (cue 68, 03:59.3). In S08 the wire is unplugged and "1 passed, 4 skipped, and the headline is
     still green." (cue 238, 14:30.5).
   - **V3, the collector and the fixture wiring (S06):** "Watch the collector sweep the tests folder:" (cue 159,
     09:35.9). `broken` stays dark (cue 165, 10:02.5). Then fixtures and `parametrize`.
   - **V4, the ribbon and the funnel (S05, S10):**
     - The 95-character line folds at 88 (cue 131, 07:47.7).
     - "exactly 2 survive" black on `8eb63fc` (cue 150, 08:57.2).
     - babykev's 79 → 70 → 69 → 37 (from cue 327, 19:53.6).
   - **V5, the hand-over chain (S09, S11):** "It hands over to pre-commit" (cue 264, 15:58.8); the same chain with
     babykev's venv path (cue 337, 20:29.9).
   - **V6, the mask grid (S12, S13):**
     - "Rows 5 and 6 say question 2 sees everything" (cue 383, 23:20.3).
     - Hypothesis draws 4,686 shapes (cue 423, 25:44.3) and shrinks the counter-example (cue 429, 26:14.1).
     - The one-line fix, "same question means same segment ID" (cue 436, 26:39.2).
   - **V7, baked-in code (S07):** the fat dependency layer and the four thin COPY slabs (cue 185, 11:17.0); "Rebuild,
     or you test the past." (cue 217, 13:12.2).

   **Lecture slides:** a GREY "Lecture 9 · slides …" tag top right in 13 of the 15 scenes. S04 and S15 have none, and
   `script.md` gives them none. The deck is redrawn, never shown.
   - Each tag's wording matches its SHOW line and reads "slides …" (every tag cites several slides).
   - The tags check found 0 changes inside any tag box in a 4 fps scan of every span (`tags/scan.log`, `scan.json`)
     and no tag left on past its scene.
   - `SLIDES.md` ("This video and the slides", map table) pairs every chapter with the deck's slides.
3. **Pause-and-ponder moments and a recap**: ✔ for the ponders, by Conny's decision for the series (accepted item
   A2). The recap takes the script's form: see the note below.
   - **Ponders:** five cards, each followed by a silent timer. Card times are the card's FadeIn in each scene's
     `events.json` sidecar plus the scene's chapter start; answer times are from the `.srt`. `measured.json` ("ponder")
     gives the same times except for S09, where it lists the timer start minus 0.6 s (16:56.1); that card goes up
     during the narration, at 16:52.5 (frames `verifier/s09_ponder_1012.2.jpg`, `…_1013.3.jpg`).

     | # | scene | card (condensed) | card in | timer | answer starts |
     |---|---|---|---|---|---|
     | 1 | S06 | README Part 6 appends `def broken(): assert False`. Will the unit tests go red? | 09:53.9 | 8 s | 10:02.5 "No. Watch the collector: the appended name stays dark." |
     | 2 | S08 | The same system-test command, but the server is not running. Fail, error, or something else? | 14:11.2 | 8 s | 14:19.8 "The README's next step answers it…"; result at 14:30.5 "1 passed, 4 skipped…" |
     | 3 | S09 | black just Failed on utils.py. Will flake8 report the E231 and E303 from before? | 16:52.5 (timer 16:56.7) | 6 s | 17:02.7 "No. Black had already rewritten the file…" |
     | 4 | S12 | Every line of branch_mask ran, coverage reads 94%. Can any coverage number catch this bug? | 23:51.3 | 8 s | 23:59.9 "No. Coverage counts lines that ran…" |
     | 5 | S13 | The wrong fix blocks only the question just before. What is the smallest request shape that still breaks the rule? | 25:55.7 | 8 s | 26:04.3 "You need a question two steps back," |

   - **Rate:** 5 cards in 30:22, one every 6.1 min, against AGENTS.md's aim of one every 2 minutes (about 15). The
     longest stretches between card appearances are 00:00–09:54, 16:52–23:51 (6:59) and 25:56–30:22 (4:26). `BRIEF.md`
     ("Ponder questions (summary)") plans exactly five. The SAY lines also say "pause" 32 times; those are prompts to
     run a command, not ponder cards.
   - **Decided by Conny (2026-10-21), as recorded in `videos/ac215-l05-rag/REVIEW.md` gate 3:**
     「我觉得可以保留现在的密度」: keep the current density of 3–5 ponders per lecture.
   - **Recap:** S15 from 28:47.4 (`measured.json` "recap").
     - 28:47.4–29:23.8: the Docker teardown.
     - 29:23.8–30:01.9: "5 questions to test yourself." Each question leaves a one-line topic label in a list at
       left: three kinds · silent skip · the hook file · modified by black · properties over coverage. Answers are in
       `exercises.md`.
     - From 30:01.9: the pointers to the study guide, L10 and L21.
     - The completed six-row gate table in S14 (28:05.4) restates every check of the lecture.
     - **Note:** the measured check reports that this "is a set of self-test questions with a list of topic labels,
       not a spoken summary of the ideas". `script.md` and `BRIEF.md` plan it this way. The coordinator has not
       recorded a separate ruling on this form; it is listed under "Open nits".
4. **Narration written for the ear, with word-anchored cues** ✔.
   - **Spoken style:** follows `script.md`'s conventions: commands and paths are said in words, versions take "at the
     time of recording" (one exception: S10's lockfile-pinned "Python 3.13.16" sentence; the same SAY block carries
     the phrase two sentences later), every sentence starts with a capital or a digit, and the step tags are spoken
     as words ("step zero zero", "Step five a").
   - **Size:** 92 SAY lines, 4,351 words (`measured.json` "narration"). Kokoro `af_heart` at speed 0.9 gives 143.2 wpm
     over the runtime and 152.0 wpm over the 1,717.3 s of voice (94.2 % of the runtime).
   - **Anchors:** 692 `vo.wait_until(...)` calls across the 15 scenes (S01–S15: 25, 40, 46, 35, 54, 34, 52, 51, 59,
     56, 54, 53, 51, 40, 42). None of the 15 render logs contains "anchor not found".
   - **Pronunciation:** the QA ASR watcher found the draft voiced without the L09 lexicon block. babykev was said
     "bay-bye-kev", cheese-app-ci-cd was "cheese-app-sigh-C-D", and decimals were split ("five. zero"). The L09
     entries are now in `explainer/lexicon.yaml`, from main's superset, merged in `04c4702`: `babykev`, `F401`,
     `cheese-app-ci-cd` and the decimals block from line 392. The final ASR heard "cd into CheeseAppCICD" (cue 85,
     04:59) and "baby kev".
   - **Final ASR** (`report-asr.md`): no mispronunciation or swallowed word that needs a fix. No cue's speech starts
     more than 1 s late; the latest is cue 71 at 04:08, 0.55 s late (`cue-onset-lag.json`). Four optional doubts:
     accepted item A3.
5. **Simulated-target-viewer QA over the full draft** ✔.
   - Seven watchers reviewed the 480p draft:
     - two directors and two simulated target viewers ("newcomer"), one of each per part;
     - a subtitle watcher, a follow-ups watcher and an ASR watcher.
   - The newcomers worked from contact sheets, exact frames, the English `.srt`, the README, `walk.md` and the
     captures.
   - **66 timestamped findings: 7 must, 41 should, 18 nit.** The 7 musts are 5 distinct problems, all fixed. Each scene's
     fixes were checked by a skeptical verifier on fresh preview or 720p frames. What stayed open is listed under
     "Whole-video QA".
6. **Measured checks** ✔. The numbers are under "Verified" (`measured.json`, measured on the final files).
   - **Duration:** 30:22.4 (1822.417 s), inside the series' 25–35 min. The parts are 18:11.5 (1091.490 s) and 12:11.0
     (731.042 s). Their container durations sum to 0.115 s more than the full cut (within ±0.5 s), and their frame
     counts sum to the clean cut's exactly (65,485 + 43,857 = 109,342).
   - **Loudness:** −16.1 LUFS integrated in all four files, LRA 2.1–2.2 LU, true peak −2.7 to −2.8 dBTP. That meets
     the toolkit's −16 LUFS target with peaks below −1.5 dBTP.
   - **Caption bounds** (`report-visual.md`): every one of the 515 events in `.zh-en.ass` is exactly two lines,
     Chinese (50 px) above English (33 px), with wrapping off (`WrapStyle: 2`). The widest lines are 1,500 px Chinese
     (00:35.7, 04:12.5, 23:59.9) and 1,461 px English (24:54.9), against 1,840 px available. In the burned copy the
     subtitles sit at y≈990–1060 and every terminal and code panel ends at y≈880 or higher, so no command a viewer
     must copy is covered.
   - **Music balance:** does not apply. L09, like L02–L08, has no score: `video.yaml` has no `music:` key.
   - **Subtitle sync:** by silence detection, no cue's speech starts more than 1 s after the cue; the only cue over
     0.5 s is cue 71 (0.55 s) (`silence.log`, `cue-onset-lag.json`). Speech starting before its cue was not measured.

   **Human review:** the series waiver stands in for a listening sign-off.

   Listening sign-off: waived by Conny for the AC215 series (Explainer_Videos#29, 2026-10-15): 「不需要，我现在对视频质量很满意的」 — no human listened to this cut; the ASR round trip below is the substitute.
   Review moments optional since 2026-10-22 (AGENTS.md): 「我大概率是不会进行审片的，因为我觉得做得已经非常好了，就让bugbot来检查就好了」

   **ASR round trip** (`report-asr.md`):
   - faster-whisper base.en over the whole clean cut: 497 cues compared, 4,457 words recognised, 242 cues with some
     difference (231 after cross-cue alignment); `asr.json`, `asr.log`.
   - large-v3-turbo on 50 doubtful cues in two batches (`asr-large-recheck.json`, `asr-large-recheck2.json`). It
     recovered every dropped first word, cleared every repeated word, and read the garbled base-model cues correctly.
     For example, cues 389–391 (23:42–23:48) "Something to ponder: every line of branch_mask ran, and coverage reads
     94 percent." came back word for word.
   - What remains is recogniser noise: homophones (ruff/rough, sed/said, cache/cash), tool names it cannot know
     (pytest, flake8, hadolint, uvicorn), and numbers and symbols.
   - **Names:** the narration's one spoken credit ("Part 2 is the guest lecture by Rahul Dave", cue 299, 18:11.4) is
     shown in the subtitle as "Part 2 is the guest lecture." Neither model heard the instructor's name; cue 2 says
     "a Harvard instructor".

## Whole-video QA (480p draft, 30:09.4, 2026-11-02/03; times are *draft* times)

**Watchers and findings** (`l09-qa-wvlqd4zmv.output`, key `result`; the run log reads "L09: 66 issues from 7/7
watchers"):

| watcher | must | should | nit |
|---|---|---|---|
| director, part 1 | 2 | 4 | 4 |
| newcomer, part 1 | 1 | 6 | 4 |
| director, part 2 | 2 | 8 | 3 |
| newcomer, part 2 | 2 | 7 | 1 |
| subtitles | 0 | 13 | 5 |
| follow-ups | 0 | 0 | 0 |
| ASR | 0 | 3 | 1 |
| **total** | **7** | **41** | **18** |

- **By target:** 37 scene, 19 subtitles, 5 narration, 5 shared.
- **By kind:** 24 follow-along, 20 subtitle, 7 picture, 6 text, 4 lexicon, 2 fact, 1 pacing, 1 sync, 1 continuity.
- **Follow-ups watcher:** found no `QA_FOLLOWUPS.md`; there is still none in the episode folder. Instead it read the 8
  Bugbot inline threads on L09 files in PR #50 (`claude/ac215-l09-l13-batch`) and checked each against the current
  code and draft frames. It found none still a problem (each was already fixed or did not reproduce), so it reported
  no issue.

**The five musts, and how each was fixed.**
- **M1, *draft* 17:46, S09: `git status` unreadable and contradicting the narration** (director part 1 and newcomer
  part 1). The status scrolled through a 3-row strip in about 1.5 s. Its first rows, "Your branch is ahead of
  'origin/main' by 1 commit", were on screen as the narration said "no commit exists".
  - **Fix** (`s09_precommit.py`): the strip grows to 7 rows. `git status` prints capture lines 6–8 and a `…`; the
    "ahead" lines are gone. The "still staged · not committed" tag stays, and the restore folds in under the rows.
    The verifier measured about 4.5 s readable, up from 1.5 s.
  - **Post-QA (`f489a21`):** the SAY now reads "Unstage and restore the file, both copies:" (cue 296, 17:59.0), with
    its zh line.
- **M2, *draft* 06:01, the zh and zh-en subtitle files stale and drifting** (director part 1; the subtitle watcher
  filed the same as a shared should). The files came from an older cut: up to about 9 s early, some English lines
  from older narration.
  - **Fix:** regenerated from the current `i18n/zh/narration/*.yaml` at the 1080p stitch (full-cut files in
    `f29303b`, part files in `051fe99`). In the final
    files `.srt`, `.zh.srt` and `.zh-en.srt` all end at 1820.728 s, and the pairs check read all 515 bilingual cues
    and found no meaning swap.
- **M3, *draft* 19:39, S10: step-02 never entered** (director part 2 and newcomer part 2). The video went from
  step-01's pytest straight to `uv run ruff check --statistics`, so a viewer could not reproduce "70".
  - **Fix** (`s10_babykev.py`): beat 4 now types `git switch --detach step-02`, then `just setup` (showing
    `+ ruff==0.16.10`), then `just fmt` with a `▶ your turn`. The statistics command follows on "After formatting"
    (cue 327, 19:53.6).
- **M4, *draft* 20:09, S11: `git switch --detach step-03` would abort over step 2's `lint --fix` edits.** The capture
  had hidden a `git restore .`.
  - **Fix** (`s11_just_check.py`): a GREY chip "step 2's lint --fix edits? drop them first: `git restore .`" appears
    above the switch. It is on screen from scene 0.9 s to 8.5 s, about 20:19.8–20:27.4 in the final cut.
- **M5, *draft* 21:58, S11: the docs beat ran `just docs check` at step-04/04b without `git switch` or `just setup`**
  (newcomer part 2; the director filed the same as a should).
  - **Fix:** `git switch --detach step-04` and `just setup` (`+ fastcore==2.2.32`) are typed before the first
    `just docs check`, and the same for step-04b.
  - The deletion that blocks the commit is now typed live, from the walk's sed, with a GREY chip "walk.md:446 deletes
    one description on purpose". Then come `git commit -am "try"` and the undo.

**The shoulds, examples by kind** (fixed and verified, except those under "Still open"):
- **On screen too briefly:**
  - S04's two `▶ your turn` tags: the `cd` tag now readable about 3.3 s, the `sh` tag held longer by its verifier.
  - S07's Option 3 commands, now on a GREY `README.md · lines 210–225` card with a moving ring.
  - S07's "packages before code" caption, now about 2.3 s.
  - S09 `pre-commit run --all-files` with its tag.
  - S11's two undo commands, with "undo" tags and 1.5 s holds.
  - S12's mask one-liner.
  - S13's `just --show check`, now about 2 s.
- **Follow-along gaps:**
  - S08: a GREY Docker Desktop fallback chip (`docker exec api-server python -m pytest tests/system/ -v` · study
    guide).
  - S09 and S11: Mac notes.
  - S12: "The first run downloads about a gigabyte" (cue 402, 24:35.5).
  - S13: "one line · copy from study guide" tags on the two soft-wrapped perl one-liners.
  - S15: an extra `cd ~/cheese-app-ci-cd` before `pre-commit uninstall`, and a GREY chip with the babykev cleanup
    paths.
- **Facts:**
  - S09's Mac advice was wrong for BSD sed. The narration now says to add `import os` in the editor, then
    `git add -u` (cues 290–292, 17:35–17:47), and the S09 chip matches.
  - S10's `uv.lock` card showed step-01 versions at step-00; it now shows symbolic `x.y` pins.
- **Pictures and sync:**
  - S08's SKIPPED rows no longer break mid-word.
  - S12's sequence bar now matches the 6×6 grid (two questions).
  - S11's "format + lint" row fills only after "the cheese gate rewrites".
- **Subtitles and names:**
  - 15 zh pairing and line-break rewrites in `g1.yaml`/`g2.yaml`.
  - The guest's name was taken out of the subtitle display text: `en_display` "Part 2 is the guest lecture.", zh
    「第二部分是客座讲座。」.
- **Lexicon:** the four ASR items are covered by main's L09 lexicon entries (`04c4702`). No re-voice was needed beyond
  the 1080p renders.

**Nits:** fixed or answered on screen, except those listed next:
- S01's static open, now with a pulse on line 43.
- S05's broom label and the E501 and `service./py` wraps.
- S07's erratum card.
- S10's "step 1 of 8", now with the tag "04 + 04b: one tracker step".
- S12: "this block is the whole difference".
- S14: the hadolint row change, and the doubled arch names.
- S01's "which four": the label now reads `cheese README · Parts 5–7 not today`.
- S06's `conftest.py`: the caption "pytest loads this file itself · shared fixtures".
- One nit did not reproduce: S14's row-name alignment. All row names start at the same x.

**Still open after QA, and why:**
- **Narration-only halves of fixed items:** the screen was fixed, but the spoken addition needs `script.md` and zh
  edits plus re-anchoring, which the scene fixers could not make and which were not made afterwards:
  - S07 "Pause and run them." after Option 3 (cue 207, 12:35.7; the card and `▶ your turn` are on screen);
  - S11 SAY[0] "drop step 2's edits, then switch";
  - S11 SAY[4] "restore it" after "no commit made" (cue 359, 21:43.1);
  - S11 SAY[5], a clause on switching and setup per step.
- **S11's docs and config rows fill about 1–2.5 s after "Two rows join the table."** (cue 369, 22:24.9). The beat now
  holds two switches, two setups, the sed and the restore inside one sentence. Only the SAY[5] clause above would
  remove the lag.
- **S08's `▶ your turn` arrives about 2 s after "Pause and run it"** (cue 232, 14:01.6), because the token animation
  overruns. The S08 verifier made the tag stay longer (about 16 s) and left the timing.
- **S09 shows `git status` lines 6–8, not lines 10–13** (the unstaged block). Nine rows plus the restore do not fit
  under the gate without crossing the tracker, which a scene assert forbids. A GREY tag "+ unstaged: black's reformat"
  and the post-QA "both copies" narration cover it.
- **`script.md` SHOW lines lag the scenes:** they do not list the S08 fallback chip, the S10 switch/setup/fmt rows or
  the S15 `cd` and paths chip. S12's SHOW still says "three TEAL question blocks"; the scene's docstring records the
  change to two.
- **S15's tracker** still reads "step 3 of 3: image ls · extra" during the babykev cleanup card. This was there before
  QA and is minor.
- **Toolkit:** `Terminal.print(wrap=True)` breaks at the character limit, so S05 and S08 carry local `soft()` copies.
  Fixing it belongs in a later toolkit PR (AGENTS.md split).

## Final-cut checks (1080p60, 2026-11-03)

- **Tags** (`report-tags.md`): no blocking defect.
  - 13 tags, each with four frames (in, mid, before, after), crops and contact sheets (`tags/`, 144 files).
  - A 4 fps scan of every span found 0 changes in any tag box. The only halo hit is S06 (accepted item A5).
  - Each tag's text equals its SHOW line.
  - Two advisories: under "Open nits".
- **ASR** (`report-asr.md`): intelligible throughout, no real problem. Four optional doubts: accepted item A3.
- **Visual** (`report-visual.md`), on the burned copy:
  - 38 contact sheets (608 frames, one every 3 s), all read, plus full-size re-pulls of every suspicious spot.
  - No clipped or garbled text in a final state, nothing off-frame, no stuck tag, no black or missing scene.
  - All 15 scenes fade to near-black (`ends/`).
  - Three decision items: the guest's handle in the clone URL (accepted item A1), long static holds and one
    low-contrast chip (both under "Open nits").
- **Pairs** (`report-pairs.md`): all 515 cues of `.zh-en.srt` read.
  - No meaning swaps; every condition- or time-first zh clause stays in its cue.
  - The part files have exactly the full file's text.
  - Two cues show the same English twice (accepted item A4). Three cues split a command, and five have small drifts
    (under "Open nits").
- **Measured** (`report-measured.md`, `measured.json`): all four MP4s decode with 0 errors. Formats, loudness,
  subtitles, chapters and the part split pass. The ponder shortfall is decided under gate 3.

## Accepted items (coordinator decisions)

- **A1. The guest lecturer's GitHub handle stays in the clone URL.** In S10 the terminal shows
  `git clone https://github.com/<handle>/babykev`, because viewers must copy that command (`frames/f_01125.jpg`,
  `sheets/sheet_24.jpg`). The decision names 18:45–18:57; measured on the clean cut, the URL is typed over
  18:43.3–18:44.5 and the terminal clears at 18:54.4 (S10 `events.json`; `verifier/s10_clone_sheet.jpg`,
  `verifier/s10_clone_sheet2.jpg`).
  - No person's name is shown anywhere else. The scan of all `.srt` and `.ass` files in `output/` found no "rahul",
    "dave", "pavlos" or "protopapas".
  - The instructor's name never appears.
- **A2. Five ponder moments in 30:22**, below AGENTS.md's one per 2 minutes. Accepted under Conny's 2026-10-21 decision
  to keep 3–5 per lecture (「我觉得可以保留现在的密度」); see gate 3.
- **A3. ASR doubts (optional; no re-voice).** Both models agree on each, so each may be a real but small slur that
  leaves the meaning intact:
  - cue 405 (24:46) "Step 5a" heard as "Step five";
  - cue 465 (28:23) "this same repo" heard as "the same repo";
  - cues 341, 360 and 362 (20:43, 21:49, 21:54) ".env" heard as "dot end" or ".n". The subtitle and terminal show
    `.env`.
  - cue 413 (25:13) "bit exactness" heard as "but" or "bid". "bit-for-bit" would be more robust, but it needs a TTS
    re-render.
- **A4. English shown twice in two bilingual cue pairs.** In each, the zh sentence is split and the English is not:
  - `.zh-en.srt` 37/38 (02:05.8–02:11.6), "It asks the app for the distance of (3, 4) and insists on exactly 5.0.";
  - 500/501 (29:26.1–29:32.1), quiz question 1. The QA text fixer chose this form on purpose so that the English is
    no longer cut mid-phrase.
  - Each zh half is a correct part of its English, and nothing is swapped.
- **A5. Tight tag spacing in S06.** The `README.md · line 388` card sits about 12–14 px under the "slides 26, 58–61"
  tag from 09:44 to 10:08 (584–608 s), with no overlap (`tags/s06_flag_584.65.png`).

## Open nits (not ruled on one by one; left for the coordinator)

None blocks release. Each needs a zh/yaml, `script.md` or scene change and a rebuild, which this record does not make.
- **Commands split across two bilingual cues** (`report-pairs.md` B). The command is whole in the terminal at the same
  moment in each case.
  - 97/98 (05:37–05:48), the uvicorn command. Cue 98's "Chinese" line is the verbatim `--host 0.0.0.0 --port 9000
    --reload`, with no Hanzi (`measured.json` "missing_lang").
  - 165/166 (09:44–09:51), `def broken(): assert False`. The QA text fixer applied the *draft* 09:42 nit to the yaml,
    but the split persists in the final file.
  - 195/196 (11:39–11:45), `docker run --rm … pytest tests/unit/`. This one is low severity because the command is
    spelled half in words.
- **Small drifts** (pairs C1–C5, `.zh-en.srt`): a word one cue early in 50/51 (02:55), 189/190 (11:20), 356/357
  (20:51) and 482/483 (28:27); in 460/461 (27:14) the result "1 passed, 103 deselected" is split across the two cues
  in both languages. There is no meaning swap.
- **`.zh-en.srt` cue 248** (14:40.4) carries the verbatim pytest output `SKIPPED，API not running at localhost:9000` on its zh line.
  This is informational.
- **Long static holds with narration** (`freeze.log`): 86 stretches over 4 s, almost all 4–7 s. Ten are 8 s or longer:
  01:52.2 (10.5 s), 08:26.9 (11.4 s), 12:16.0 (10.4 s), 14:52.1 (9.0 s), 16:53.1 (8.6 s, a running ponder timer),
  22:59.4 (8.7 s), 23:40.1 (11.4 s), 25:07.7 (9.5 s), 27:19.4 (9.2 s), 27:49.4 (9.0 s).
  - The threshold misses small motion. For example, the timer bar at 16:53 was counted although it moves.
  - The visual check calls none a defect.
- **Low-contrast chip, 16:16–16:18 (S09):** the grey dashed "tests/ · never matched" chip sits on the olive highlight
  of `files: ^src/.*\.py$`. It covers no code, but its dashed border runs past the band (`frames/c_0976_tag.jpg`).
- **Tag advisories** (`report-tags.md`):
  - S05's "slides 29–31" leaves as the funnel starts (531.93 s, 08:51.9), as SHOW asks ("until the funnel"), so
    slide 31's funnel is never tagged.
  - 8 tags leave with their scene's closing FadeOut, as their "whole scene" SHOW lines ask.
- **The recap form** (gate 3): self-test questions with topic labels, not a spoken summary of the ideas.
- **Written copies of the name:** `output/transcript.md` line 81 reads "Part 2 is the guest lecture, by Rahul Dave."
  It is the spoken credit that `BRIEF.md` allows once in S10, not on screen. The README and `ASSETS.md` link the
  guest's public repos as attribution.
- **README chapter 9's summary** still describes the old Mac advice ("on a Mac, `sed -i` needs empty quotes after
  it"). The narration and chip now say to edit in the editor, then `git add -u`. Only the durations and chapters were
  updated in this pass.

## Verified (final render)

All numbers are from `measured.json` and the five reports (2026-11-03), on the files in `output/` as they are now.

- **Files:** H.264, yuv420p, 1920×1080 at 60 fps, AAC 48 kHz stereo at about 179 kb/s. Each decodes in full with
  `ffmpeg -v error -f null` with exit 0 and an empty error log (`decode_*.log`).

  | file | duration | video frames | size (bytes) | loudness | LRA | true peak |
  |---|---|---|---|---|---|---|
  | `ac215-l09-ci-testing.mp4` | 1822.417 s (30:22.4) | 109,342 | 105,203,989 | −16.1 LUFS | 2.2 LU | −2.7 dBTP |
  | `ac215-l09-ci-testing.zh-en.mp4` | 1822.417 s | 109,343 | 103,900,212 | −16.1 | 2.2 | −2.7 |
  | `ac215-l09-ci-testing_part1.mp4` | 1091.490 s (18:11.5) | 65,485 | 62,807,438 | −16.1 | 2.2 | −2.7 |
  | `ac215-l09-ci-testing_part2.mp4` | 731.042 s (12:11.0) | 43,857 | 42,400,860 | −16.1 | 2.1 | −2.8 |

  The zh-en video stream is one frame (17 ms) longer than the clean cut's. The 15 scene renders sum to 1822.358 s.
- **Subtitles:** `.srt` 497 cues, `.zh.srt` 429, `.zh-en.srt` 515. The parts have 298 / 255 / 308 and 199 / 174 / 207,
  which sum exactly to the full files.
  - In every file the cues are numbered 1..N and in order, inside the runtime, at least 1.000 s long, at most 2 lines,
    with no overlaps.
  - The last cue ends at 1820.728 s (parts: 1090.382 and 729.312 s), 1.7 s before the clean cut ends.
  - The three languages are cut into cues differently, so their cue times do not line up one-to-one, by design.
  - The masked token `‹instructor›` appears in 0 cues.
- **Chapters:** 15 entries in `video.yaml` order. Each start equals the running total of the scene render durations
  (S10 at 1091.411 s = 18:11, S15 at 1727.424 s = 28:47). `chapters_part1.txt` (9 entries) and `chapters_part2.txt`
  (6, at 00:00, 02:07, 04:18, 06:34, 08:49, 10:36) match too. `README.md` now carries these.
- **Scenes:** all 15 end on a near-black frame (`ends/scene_ends.jpg`). The chapter starts match the scene durations,
  so no scene is missing.
- **Narration:** 92 SAY lines, 4,351 words, 152.0 wpm over the voice's 1,717.3 s; 692 anchors; no "anchor not found"
  in the 15 render logs.
- **Lecture tags:** 13, each found, none overlapping, none on past its scene (`tags/`).
- **Privacy:**
  - The instructor appears only as "a Harvard instructor" (cue 2). The masked token `‹instructor›` appears in 0 cues,
    and the S02 `git log` line prints hash and date only (`--format='%H %ci'`).
  - The guest's name is spoken once (cue 299, 18:11.4) and never in a subtitle.
  - The guest's handle is on screen only inside the clone URL (A1). The only other capture with the guest's name,
    `assets/terminal/babykev/s00-09-pyproject.txt` line 9 (`authors`), is not shown: S10 and S14 quote
    `pyproject.toml` lines 65 and 53–57 only.
  - No check in this record looked for credentials on screen; `BRIEF.md` fixes the `.env` demo content at `X=1`.
- **Provenance** (`ASSETS.md`):
  - Terminal lines come from the 2026-10-19 captures in `assets/terminal/`. Every covered README command and every
    `walk.md` command of steps 00–05b runs exactly as written, in order; extras are tagged `extra`.
  - Code panels quote `assets/source/` at the pinned commits, plus the history files `8eb63fc`, `c3b227f`, step-01's
    `api.py` and step-05's `model.py`.
  - The walk's own outputs that could not run here are tagged `recorded · walk.md`: the image sizes 1.15/1.84 GB, the
    `--network none` run, the author's Mac "103 passed" at 05a/05b, and the Quarto/site renders.
  - The browser is a drawing tagged `illustration`.
  - S05's "8 → 2 findings" was re-measured on 2026-10-23 with the hook's pinned flake8 7.0.0 and black 24.1.1.
  - S14's "Milestone 5 · at least 70%" comes from the course handout.

## Not claimed

- **No human listened to this cut** or watched it. The listening gate rests on the series waiver quoted under gate 6,
  and the audio was checked only by machine (the ASR round trip). The four ASR doubts (A3) are unresolved by ear.
- **The Chinese subtitles were reviewed by agents only:** the QA subtitle watcher, the text fixer, the scene verifiers
  and the final pairs check. No human translator or native reviewer read them.
- **No Docker Desktop run.**
  - The cheese track ran in Docker Engine 29.8.2 (dind) on Linux x86_64, standing in for Docker Desktop.
  - `--network host` on Docker Desktop for Mac/Windows is untested (the digest's open question Q2).
  - The S08 fallback `docker exec api-server python -m pytest tests/system/ -v` was never run; the digest marks it
    *(suggested)*.
  - The Mac advice (S09's editor route, S11's `sed -i ''` chips) was not run on a Mac.
- **babykev's Docker and site steps did not run.** The babykev machine had no Docker, so `docker build`, the two
  images, `just image shell`, the `--network none` run and the smoke in the run image are the walk's records
  (`recorded`), not ours. Quarto and the docs site were not installed or rendered.
- **The author's Mac result (103 passed at 05a/05b) is the walk's record.** Our machine gave `1 failed, 102 passed`.
  The bit-exactness explanation follows the walk and the test's own failure; it was not tested on a second machine.
- **No cloud, Docker Hub or GitHub Actions step** is part of this lecture. Part 5 (CI) is only previewed and was not
  run.
- **The visual check sampled one frame every 3 s**, plus targeted frames. Motion between samples was checked only by
  `freezedetect`, whose threshold can miss small motion, and by the tags check's 4 fps scan of the tag regions.
- **The measured check did not itself search for real names.** The name checks are the ASR report's search of the
  nine `.srt` files, the visual report's search of the `.srt` and `.ass` files, and the frames each read.
- **Review bots:** the QA follow-ups watcher read the 8 Bugbot threads on L09 files in PR #50. Nothing in this record
  checks for bot comments posted later. No `QA_FOLLOWUPS.md` exists for L09.
- **The QA fixes were verified by agents** on fresh preview or 720p renders of each scene, before the 1080p60
  renders. They were not re-checked one by one on the final cut, which the five final-cut checks cover only by their
  own sampling.
- **Every check in this record is an agent's.**
