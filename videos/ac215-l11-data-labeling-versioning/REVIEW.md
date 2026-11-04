# Review record: AC215 · Lecture 11 — Data labeling and versioning: a label is a record, a version is a fingerprint

Follow-along of two tutorials, each `README.md` top to bottom:
[dlops-io/data-labeling](https://github.com/dlops-io/data-labeling) `main` @ `03c3e27` (part 1: Prerequisites through
Docker Cleanup, including the *Extra* docker-compose section) and
[dlops-io/data-versioning](https://github.com/dlops-io/data-versioning), README @ `b240b1a` (the course map's pin) run
on the starter it tells you to clone, `data-versioning-ac215` @ `23762e4`, with the one-line `Dockerfile:36` fix
(`google-cloud-sdk` → `google-cloud-cli`) (part 2). Today's README (`main` @ `2515e5e`, "clone main") appears only as
a short erratum beat (route T in `ASSETS.md`). Claude Code sessions (Claude) produced it. Verified facts and
unclaimed reviews are kept in separate sections.

- **Origin and takeover:** another session wrote script v2, `scenes/common.py` and S01 on branch
  `claude/ac215-l09-l13-batch` (issue #48). Its claim expired, and this coordinator took L11 over on 2026-11-02. This
  session rebuilt the scene contract (`build/SCENE-NOTES.md`, the task files), built S02–S16 with one critic each
  (`59fd688`), and wrote the Chinese subtitles (`ea5e1b6`).
- **Captures:** 2026-10-23 11:42–12:06 UTC (`ASSETS.md`, "terminal/"), in a fresh Docker Engine 29.8.2
  (`docker:29.8.2-dind`) standing in for a laptop with Docker Desktop. That machine had **no Google credentials, no
  bucket, no browser and no SSH route to GitHub**. Every local step ran live. Every step that needs a credential or a
  bucket was captured up to its documented failure, and the success path is tagged `recorded`.
- **QA draft:** the 480p draft (31:46; part 1 ended at 15:41).
- **Whole-video QA:** `/root/ac215-backup/tasks/l11-qa-watkkh0au.output`, key `result`. 37 agents: seven watchers,
  13 scene fixers (S03–S14 and S16), one narration/lexicon/subtitle fixer and 16 scene verifiers. The run log reads
  "L11: 56 issues from 7/7 watchers".
- **After QA, by the coordinator:** three narration items the verifiers left open were voiced (`38b780b`; see
  "Whole-video QA"). Lexicon PR #96 (dataset phrases, "Mac metadata", gcsfuse, "dvc init") was merged to `main`, which
  the CI release renders with.
- **Finishing pass:** none. The coordinator's list of finishing-pass outputs for L11 is empty (`[]`).
- **1080p60 renders:** all 16 scenes. The render logs in `build/logs/` are dated 2026-11-04 03:46–05:00 UTC. None
  contains "anchor not found".
- **Final-cut checks, round 1** (on the first 1080p stitch): the pairs check found 12 bilingual cue defects: two
  cues that repeated their English line (old cues 170/171 in S06 and 448/449 in S14) and ten pairs with a phrase in the
  wrong cue (`report-pairs-round1.md`). Twelve Chinese sentences were reordered (`745eaba`), then the subtitles were
  rebuilt, the cut re-stitched and the bilingual copy re-burned. The rebuilt full-cut subtitle files were committed in
  `499b6a9` (a WIP commit shared with the L13 work), the part files in `d8b9024`. Round 1's measured check
  (`report-measured-round1.md`) passed the media and flagged the same subtitle items.
- **Final cut:** 32:09.1 (1929.122 s); parts 15:58.6 + 16:10.5. File times (UTC): the clean cut and the full-cut
  subtitles 2026-11-04 07:29; the burned copy, chapters and transcript 08:14; the parts 08:16–08:19. The MP4s are not
  in Git (release assets).
- **Final-cut checks, round 2:** five agent checks. The coordinator saved their returned text as
  `build/final-review/report-{tags,asr,visual,pairs,measured}.md`. All five reports exist and were read in full for
  this record. `report-pairs.md` and `report-measured.md` re-checked the current files. `report-tags.md`,
  `report-asr.md` and `report-visual.md` ran on the first final cut (their evidence is dated 06:31–07:14 UTC). The
  re-stitch rewrote the clean cut at 07:29, but its content is unchanged: the round-1 and round-2 ebur128 decode logs
  (`measured/` and `measured2/`) agree line for line at 100 ms steps once pointer addresses are stripped, the frame count
  is the same (115,743), and three tag frames re-extracted from the current clean cut (2:15.08, 12:44.75, 22:54.68) are
  pixel-identical to the `tags/` frames (`verifier/cmp_*.png`). The re-burn changed only the Chinese subtitles burned
  into the `.zh-en.mp4`. The English cue numbers and times
  that `report-asr.md` cites match the current `.srt` (checked for cues 48, 113, 161, 176, 207, 276, 411, 475 and 476).
  None of the five checks found a blocking defect.

**Conventions:**
- **Times** are mm:ss in the full cut (`output/ac215-l11-data-labeling-versioning.mp4`, 1929.122 s), except in
  "Whole-video QA", which keeps the 480p draft's times (marked *draft*).
- **Cue numbers** name their file: `.srt` (502 cues) or `.zh-en.srt` (513).
- **Evidence paths** are relative to `build/final-review/`. That folder is git-ignored and exists only in the producing
  session; a successor re-runs the checks to reproduce it.

## Content gates (AGENTS.md)

1. **Hook** ✔. S01 opens on a puzzle, not on a value proposition.
   - "Two folders, both called cheese_dataset, with the same file names and the same count." (cue 1, 00:00.0); the
     Friday model got worse "and nobody touched the code" (cue 3, 00:08.6); "So which photos, with which labels, did
     that model see?" (cue 4, 00:12.4) and "And can you get exactly those back?" (cue 5, 00:15.8).
   - The broken habit: "final, final version 2, final final version 3" (cues 6–7, 00:18.1).
   - Two riddles: one md5 line that "will match the instructor's tag in the class repo, character for character. How
     can one line pin down about 600 kilobytes of photos?" (cues 8–11, 00:27.2–00:41.0); and "when someone clicks
     gouda, where does that word actually go?" (cue 12, 00:45.2).
   - **Payoff:** the gouda riddle is answered in S07: "on disk a label is a small JSON note" (cue 189, 11:56.5). The
     md5 riddle is answered in S12: "So one line pins 600 kilobytes: it fingerprints the list of fingerprints." (cue
     370, 23:24.7), then "the instructor's tag in the class repo holds the same fingerprint" (cue 371, 23:30.2). The
     opening question closes the recap: "So Monday's photos come back with one dvc get; their labels join in exercise
     E7." (cues 486–487, 31:02.8).
2. **Intuition before formalism, with an animated mechanism for each core idea** ✔. `BRIEF.md` ("Visual set pieces")
   defines seven, each animated next to the commands it explains:
   - **V1, the station map (S04, S07, S08):** the `docker run` flags become parts of a house: "The flag -d runs it in
     the background," (05:12.9), "a private street" (05:15.3), "a door in your laptop wall" (05:18.7). On Linux the
     house falls over because "It runs as user 1001, but Docker created the missing folder as root." (06:04.7). In S07
     the CLI house calls Label Studio by name, "because the Docker network keeps a phone book of container names"
     (12:35.6), and its `localhost` arrow curls back into itself (ponder 6, answer at 12:29.1). In S08 `depends_on`
     "starts Label Studio first" (14:56.2).
   - **V2, the signed ticket (S05, S07):** "Label Studio holds the key and lists the bucket;" (08:43.1). After the
     ponder: "With a signed ticket." (09:03.2), and "Your browser carries that ticket straight to Google," (09:13.2).
     In S07 the label envelope flies to `cheeses_labeled/` "pointing back at the photo, which never moved." (11:53.2).
   - **V3, the origin gate (S06):** the photo comes "from Google's storage address: a different origin." (09:27.4);
     the browser "hands the answer over only if it carries a header that allows this origin." (09:36.9); `cli.py -c`
     "builds one rule, any origin," (10:36.2); "And curl never met a bouncer: CORS is a browser rule, not access
     control." (11:25.9).
   - **V4, the FUSE mount (S10, S11 replay):** "The entrypoint runs the four stages the lecture draws." (18:42.8):
     "Mount the whole bucket as a folder, with gcsfuse." (18:48.5), the bind to `cheese_dataset` (18:52.1), "Note the
     two bind mounts:" (19:19.8). S11 replays it broken: gcsfuse cannot authenticate "so the bucket never mounts"
     (20:28.8), then "special device does not exist" (20:37.6).
   - **V5, the hash shelf (S12, played as a prediction before the `dvc add` output):** "It fingerprints each photo with
     MD5." (22:28.0), files it "on a shelf named by the first 2 characters" (22:34.2), fingerprints the manifest
     (22:37.1) and writes that into the pointer file (22:41.1).
   - **V6, the tag rope (S13–S15):** the bytes "sit in three places" (24:38.9); "A rope leads from the tag to the
     bytes in your bucket." (25:46.6); v21 adds "5 files and a new manifest fingerprint" (26:56.5) and pushes little
     "because the four old photos are already on the shelf." (27:15.0); "The command dvc get, with a tag, walks the
     rope." (28:29.6).
   - **V7, the running map:** built in S02 from 01:16, it grows every scene and is complete in the recap: "On one map:
     Label Studio runs in a container and signs tickets for the photos." (cue 482, 30:45.3).

   **Lecture slides:** a GREY "Lecture 11 · slide(s) …" tag top right in all 16 scenes (`report-tags.md`). The deck is
   redrawn, never shown.
   - The tags check found no tag overlapping anything and none still on screen in its scene's last frame. It scanned
     the top-right region at 2 fps (3,858 samples) and pulled four frames per tag (`tags/`).
   - S06's tag ("slide 13") is up only for the CLI-container block, 10:01.5–10:43.2, as its SHOW line says. The other
     15 run for the whole scene. The three single-slide tags read "slide N" (S06, S08, S14); the other 13 read
     "slides …".
   - `SLIDES.md` ("This video and the slides", map table) pairs every planned section with the deck's slides.
3. **Pause-and-ponder moments and a recap**: ✔ for the ponders, by Conny's decision for the series (accepted item
   A1); ✔ for the recap.
   - **Ponders:** ten cards and two quick predicts, each a card followed by a silent timer. Timer starts are from
     `measured.json` (each scene's `events.json` plus its chapter start); the card fades in 0.6 s before the timer.
     Lead-ins and answers are from the `.srt`.

     | # | scene | kind | card (condensed) | spoken lead-in | timer | answer starts |
     |---|---|---|---|---|---|---|
     | 1 | S02 | ponder | Docker network, cloud credentials, Docker Compose: where will each one show up today? | 02:00.5 | 02:08.5, 8 s | 02:17.1 "The network lets the command line container call Label Studio by name." |
     | 2 | S03 | quick | The zip held 42 files. How many tasks should Label Studio make? | 03:55.3 | 04:01.2, 4 s | 04:05.8 "21." |
     | 3 | S04 | ponder | It said Up. Now it says Exited (1). Where do you look first? | 05:49.3 | 05:51.9, 6 s | 05:58.5 "The logs." |
     | 4 | S05 | ponder | Label Studio holds the key; your browser never sees it. How can it show a private photo? | 08:48.8 | 08:54.6, 8 s | 09:03.2 "With a signed ticket." |
     | 5 | S06 | ponder | You ran `cli.py -c` and refreshed: still broken thumbnails. Two suspects? | 10:56.5 | 11:04.1, 8 s | 11:12.7 "One: the rule missed your bucket." |
     | 6 | S07 | ponder | Inside the CLI container, what if `LABEL_STUDIO_URL` were `http://localhost:8080`? | 12:18.2 | 12:22.5, 6 s | 12:29.1 "It cannot connect: inside a container," |
     | 7 | S08 | ponder | After `docker system prune`, is your labeled project gone? | 15:29.2 | 15:34.5, 6 s | 15:41.1 "No. The database file is still in the mounted folder," |
     | 8 | S11 | ponder | Inside, `ls cheese_dataset` lists four photos; on your laptop it's empty. Is the mount broken? | 21:04.2 | 21:10.2, 8 s | 21:18.8 "No. Both mounts exist only inside the container." |
     | 9 | S12 | ponder | Rename `Image_2.jpg` → `brie_2.jpg`, `dvc add` again. Which changes? | 23:37.3 | 23:48.6, 8 s | 23:57.2 "Only the manifest fingerprint, because one name in the list changed." |
     | 10 | S14 | ponder | Four photos already in `dvc_store`. You add one. How many objects will `dvc push` upload? | 26:31.5 | 26:40.4, 8 s | 26:49.0 "Two: the new photo and a new manifest." |
     | 11 | S15 | ponder | Cell 19, `dvc get … --quiet --rev dataset_v25`, prints nothing. Did it work? | 29:38.1 | 29:46.4, 6 s | 29:53.0 "No. The next cell fails: no such folder." |
     | 12 | S16 | quick | Three questions, three tools (DVC, lakeFS, Delta Lake / Iceberg): which answers each? | 30:13.8 | 30:21.1, 4 s | 30:25.7 "DVC, lakeFS, then the table formats." |

   - **Rate:** 10 ponders in 32:09, which is 0.62 per 2 minutes (0.75 counting the two quick predicts), against
     AGENTS.md's aim of one per 2 minutes. The longest stretch without a card is 15:34.5–21:10.2 (5:36): S09 and S10
     have none (`report-measured.md`). The visual check saw every card render cleanly.
   - **Decided by Conny (2026-10-21), as recorded in `videos/ac215-l05-rag/REVIEW.md` gate 3:**
     「我觉得可以保留现在的密度」: keep the current density, which that record gives as 3–5 ponders per lecture plus a
     spoken recap and test questions. L11's ten ponders are above that series density and still below AGENTS.md's
     aim.
   - **Recap:** S16 from 30:13.8 (115.2 s).
     - 30:13.8: the quick predict (three questions, three tools) and its answer; "There is no single standard"
       (30:29.2).
     - 30:34.5: monitoring, slides only: "Versioning tells you what changed; monitoring tells you that something
       changed."
     - 30:45.3–31:06.5: the spoken recap on the complete map, one sentence per idea: the container and its signed
       tickets, the rule on the bucket and the browser's bouncer, labels as small notes, the mounted bucket feeding DVC,
       files by fingerprint, the tag that pins the list (cues 482–487).
     - 31:09.4–31:28.5: "5 questions to test yourself." (cues 488–493).
     - 31:37.5–31:54.9: the cleanup ("never delete the dvc_store while any tag should still work", cue 497), then
       "Answers are in the exercises." (cue 500, 31:58.9; there is no `exercises.md` in the episode folder, see "Open
       nits") and the pointer to Lecture 13 (32:01.2).
4. **Narration written for the ear, with word-anchored cues** ✔.
   - **Spoken style:** follows `script.md`'s conventions: identifiers are said in words ("cheese dataset", "dash k"),
     with the literal form in the subtitle's `en_display`; versions and counts that drift take "at the time of
     recording".
   - **Size:** 113 SAY lines, 4,352 words (`measured.json` "script"). Kokoro `af_heart` at speed 0.9 gives 135.4 wpm
     over the runtime and 154.0 wpm over the 1,695.9 s of voice (87.9 % of the runtime). The English `.srt` has 4,297
     words, 55 fewer than the SAY lines.
   - **Anchors:** 651 `vo.wait_until(...)` calls across the 16 scenes (S01–S16: 25, 45, 34, 48, 43, 43, 44, 39, 35,
     42, 36, 54, 44, 41, 45, 33). None of the 16 render logs contains "anchor not found".
   - **Pronunciation:** the QA ASR watcher found four real problems: "dataset" flapped to "day-ruh-set", "metadata"
     stressed "meta-DAY-ta", "gcsfuse" heard as "GCS views", and "dvc init" heard as "in it". Ten L11-only phrase keys
     in `explainer/lexicon.yaml` fix them ("next dataset version", "cheese dataset", "tracks the dataset", "labeled
     dataset", "dataset v20/v21/v25", "Mac metadata", gcsfuse, "dvc init"). The verifiers checked them with
     `KokoroBackend.phonemize`, not by ear; they reached `main` in PR #96.
   - **Final ASR** (`report-asr.md`): 0 real mispronunciations or swallowed words. No cue's speech starts more than
     1 s late; the largest delay is 0.26 s. Three low-severity watch items are under "Open nits".
5. **Simulated-target-viewer QA over the full draft** ✔.
   - Seven watchers reviewed the 480p draft: two directors and two simulated target viewers ("newcomer"), one of each
     per part; a subtitle watcher, a follow-ups watcher and an ASR watcher. They worked from contact sheets, exact
     frames pulled from the draft, preview renders of the current code, the English `.srt`, both READMEs and the
     captures.
   - **56 timestamped findings: 4 must, 31 should, 21 nit.** All four musts were fixed and verified on fresh frames.
     Each scene's fixes were checked by a skeptical verifier; several verifiers found and fixed a new or incomplete
     item. What stayed open is listed under "Whole-video QA".
6. **Measured checks** ✔. The numbers are under "Verified" (`measured.json`, measured on the final files).
   - **Duration:** 32:09.1 (1929.122 s), inside the series' 25–35 min. The parts are 15:58.6 (958.633 s) and 16:10.5
     (970.499 s). Their container durations sum to 0.010 s more than the full cut (within ±0.5 s), and their video
     frame counts sum to the clean cut's exactly (57,516 + 58,227 = 115,743).
   - **Loudness:** −16.1 LUFS integrated in all four files, LRA 2.6–2.8 LU, true peak −2.6 to −2.7 dBTP. That meets
     the toolkit's −16 LUFS target, with peaks below −1 dBTP.
   - **Caption bounds** (`report-pairs.md`, `report-measured.md`, `report-visual.md`): every one of the 513 events in
     `.zh-en.ass` is exactly two lines, Chinese (50 px) above English (33 px), with wrapping off (`WrapStyle: 2`). The
     widest lines are 1,500 px Chinese (four cues, e.g. 08:12.90 and 28:23.26) and 1,453 px English (15:41.13), against 1,840 px
     available. In the first burned copy the subtitles sit at y≈990–1060; at 10 spot checks with a terminal or command on
     screen, the content ends at y≈880, so no command a viewer must copy is covered.
   - **Music balance:** does not apply. L11, like L02–L10, has no score: `video.yaml` has no `music:` key.
   - **Subtitle sync:** speech onset measured on the voice-only scene tracks placed at the scene offsets (-40 dBFS
     RMS, `onsets.json`): no cue's speech starts more than 1 s after its cue; the largest delay is 0.26 s
     (`report-asr.md`). The large model's word times agree (e.g. "Name" at 662.3 s against cue 176 at 662.47 s).

   **Human review:** the series waiver stands in for a listening sign-off.

   Listening sign-off: waived by Conny for the AC215 series (Explainer_Videos#29, 2026-10-15): 「不需要，我现在对视频质量很满意的」 — no human listened to this cut; the ASR round trip below is the substitute.
   Review moments optional since 2026-10-22 (AGENTS.md): 「我大概率是不会进行审片的，因为我觉得做得已经非常好了，就让bugbot来检查就好了」

   **ASR round trip** (`report-asr.md`, on the first final cut; the audio is unchanged since):
   - faster-whisper `base.en` over the whole clean cut: 502 cues compared, 4,430 words recognised, 225 cues with some
     difference (`asr.json`, `asr.log`).
   - `large-v3-turbo` re-ran every doubtful cue, one padded clip each, with word timestamps (`asr_large_1.json` to
     `asr_large_3.json`). Every word or cue base.en dropped is present: the first words after pauses (cues 8, 48, 59,
     67, 84, 113, 238, 259, 276; cues 48, 113 and 276 open S03, S05 and S10, so the stitch does not clip scene starts)
     and whole cues 30–31, 176, 181, 202–203, 245–246, 283 and 411.
   - What remains is recogniser noise: digits versus words, identifiers without underscores (`cheese_dataset`,
     `dvc_store`), words moved across cue boundaries, and homophones (ours/hours, CORS/course, git/get, gcsfuse/"GCS
     views" under base.en only).
   - The about 9 s gap after cue 176 (11:03.9–11:12.7) is the S06 ponder timer; the S06 voice track is silent there.

## Whole-video QA (480p draft, 31:46; times are *draft* times)

**Watchers and findings** (`l11-qa-watkkh0au.output`, key `result`):

| watcher | must | should | nit |
|---|---|---|---|
| director, part 1 | 1 | 6 | 2 |
| newcomer, part 1 | 1 | 5 | 4 |
| director, part 2 | 0 | 7 | 5 |
| newcomer, part 2 | 2 | 3 | 2 |
| subtitles | 0 | 5 | 5 |
| follow-ups | 0 | 1 | 0 |
| ASR | 0 | 4 | 3 |
| **total** | **4** | **31** | **21** |

- **By target:** 29 scene, 13 narration, 11 subtitles, 3 shared code.
- **By kind:** 12 text, 12 subtitle, 11 follow-along, 7 lexicon, 6 picture, 3 continuity, 3 sync, 1 narration,
  1 fact.
- **Facts:** both directors and both newcomers checked the facts against the captures and both READMEs (the md5
  strings, the 21 images, uid 1001, README lines 19–20 and 23, compose line 17, sizes, nfiles, tag names, error texts,
  the 401 path, `ls-remote` tags, the notebook cells) and found them right. The part-1 director reports the masking
  intact (`student@example.com`, `your-bucket-placeholder`, the fake token, no instructor name); the part-2 director
  found no instructor name on screen or in the subtitles; the part-1 newcomer found the name and e-mail masked in the
  subtitles.
- **Follow-ups watcher:** found no `QA_FOLLOWUPS.md` (there is still none for L11). It read the five unresolved Cursor
  Bugbot threads on PR #50 (`claude/ac215-l09-l13-batch`), all on `scenes/common.py`, and checked each on rendered
  frames: all five were already fixed or did not reproduce. It reported one new issue (the ticket's route line, see
  "Still open").
- **Subtitle watcher:** all automated checks passed (overlaps, durations, line counts and lengths, spacing, glossary,
  `en_display`). It found four Chinese clause-order swaps (S01, S03, S04, S08), two cue breaks inside a term (S08, S13),
  one zh sentence split into two cues that repeated the English (S06) and English breaks inside "log in" and
  "username and password" (S04).
- **ASR watcher:** 496 cues on the draft, 215 differing under base.en, all noise after large-v3-turbo re-runs except
  the four pronunciation items under gate 4. No sync problem (no speech more than 1 s late, no trailing silence over
  1.5 s).

**The musts, and how each was fixed.**
- **M1, *draft* 15:30, S08: a stray white underline** under `docker-volumes/label-studio` was never removed and stayed
  across the part-1 closing map (director, part 1). **Fix** (`s08_compose.py`): the underline is kept as `ul` and fades
  with the terminal. The verifier saw the closing map clean at scene times 107 and 110 s.
- **M2, *draft* 06:25, S04: the Linux `sudo chown -R 1001 docker-volumes/label-studio` had scrolled away** when "On
  Linux, pause and do the same" played (newcomer, part 1). **Fix** (`s04_studio.py`): a `chown_card` shows the captured
  command, folded with ` \`, tagged `extra · Linux`, from "Give the folder" through the re-run; the `▶ your turn`
  flash also flashes it. Verified at 720p (scene time 92.5 s), inside the map border with no overlap.
- **M3, *draft* 21:37, S12: the Linux fix `sudo rm -rf .dvc .dvcignore && ls -A` was unreadable**, pushed off a 9-row
  terminal by its own output (newcomer, part 2). **Fix** (`s12_fingerprints.py`): the output is trimmed to two lines
  and `…`, and a card "on your laptop · extra · Linux" holds both laptop commands word for word (asserted against
  captures 91 and 92) through "Pause and run it". Verified at scene times 19.5 and 29.6 s.
- **M4, *draft* 22:30, S12: the chip "the .dir ending marks a folder's list"** was covered by the pointer card after
  about 1.5 s (newcomer, part 2; also a director should). **Fix:** the chip moved inside the `.dvc/cache` rack, beside
  the slip it explains. The verifier lengthened its stay to about 3.5 s.

**The shoulds, examples by kind** (fixed and verified, except those under "Still open"):
- **Follow-along:** S05's stand-in JSON strips fold only after `,` or `[` (no row starts mid-word) and the red "was
  not found" line stays about 3 s; S13 adds a card listing the five git commands at "Pause and run them"; S10's
  `tree -L 2 -I \` command stays above its output; S05's `recorded · README.md:136` tag stays about 5.5 s; S14 puts a
  red "watch only · not on your mount" tag on the terminal before the checkout experiment.
- **Text:** commands fold at a space with ` \` instead of breaking mid-word: S06's `sed` (with a "↩ continues · no
  space" tag), S11's `sed`, S13's `git commit` and `git tag`, S03's curl URL (one marked wrap after `v4.0/`, "one URL ·
  wrapped, no space"); S06's "no CORS editor" chip and S07's "the slide draws what labels mean" chip stay 4–6.5 s.
- **Pictures and continuity:** S08's README line-95 card no longer sits on the laptop wall; S12's chip is clear of the
  pointer card; S13's shelf slips now match the capture (`53853e…` under `5b/`, the grey `d7/` empty-version row);
  S05 adds the chip "the README's example name · yours differs" under the bucket.
- **Fact:** S11's chip now says "already inside since scene 10" (the viewer re-enters the folder in S10).
- **Sync:** S14's `git diff` output now prints during "three lines" (was about 3.7 s late); S16's cleanup terminal is
  up before "pause and run them" and stays about 4.5 s (was about 1.5 s).
- **Narration (applied by the narration fixer):** S05 now says `/secrets` is empty "on purpose, as you will hear in a
  moment" (07:45.1); S08 says "First put your bucket name on line 17 of docker-compose.yml as well." before the run
  (14:10.5); S13 says "The README now opens Colab for version 20;" (26:06.5).
- **Subtitles:** the ten Chinese rewrites the subtitle watcher proposed, and S15's 「暂停一下，一步步做完。」. The
  English "log in" break needs a toolkit change and was not made (see "Accepted items", A2).
- **Lexicon:** see gate 4.

**New problems the verifiers found and fixed:** S03, the curl beat ran behind the narration and the size ring showed
about 0.5 s (now about 1.5 s); S05, the target strip's red message was readable about 1 s (now about 2.5 s) and the new
bucket chip cut the laptop frame (moved below it); S08, the line-17 sentence played over a leftover `your turn` tag
(replaced by a grey chip "first: docker-compose.yml line 17"); S12, a stray pink bar in the pointer card's md5 field
and a caption touching the git box; S14, the diff was still late after the fixer's change (typing sped up); S07, the
final hold grew from 1.2 to 3.2 s so the unspoken "forgot -k" chip can be read; S15, a chip "extra · the class bucket,
asked anonymously" on the unnarrated curl strip.

**Nits:** fixed, except those listed next. Examples: S04's code window now shows the whole key path; S07's "ours: 3 ·
yours: 21" chip leaves with its row; S09's "yours will differ" chip no longer cuts the row above; S10's "passed in ·
read by nothing" chip no longer slides over the output. S06 carries a "first build ≈ 2–3 min" row tag beside the build.

**Still open after QA, and why:**
- **Closed by the coordinator after QA** (`38b780b`): S03's voice now says "a stand-in, explained at the Source
  storage step." (03:38.1), matching the screen; S08 voices the fallback: "if docker-compose is not found, use the
  docker compose form on the card." (14:18.9); S14 gives the warning first: "One extra experiment, to watch, not to
  run on a real mount:" (27:54.0).
- **Accepted as is by the coordinator** (accepted item A3): the S07 "forgot -k" beat has no voice; the diagrams name
  the bucket `cheese-app-data-demo` while the viewer's own screen shows `your-bucket-placeholder`; the on-screen chips
  "a new bucket or part 1's, scene 10" (S02, `s02_map.py:119`) and "a name, not localhost · scene 7" (S06,
  `s06_cors.py:281`) still name scene numbers the video never shows.
- **Shared code, not changed:** the signed-URL ticket still rides with the route line through its text
  (`common.py` `walk()`, line 2032, *draft* 09:10; the followups watcher's should); and the empty-version slip already
  leaves the chute under its shelf name (`HashShelf.empty_run`, line 2685; director nit). Both need a `common.py`
  change and a re-render of S05, S12 and S14. The final visual check did not flag either.
- **Soft-wrapped commands outside the fixed scenes:** `type_cmd(..., soft=True)` remains in `s10_bucket.py:348`
  (capture 85), `s14_v21.py:275` and `:279` (captures 107, 108) and `s15_colab.py:297` (capture 122), so those
  commands can still wrap mid-word. The S13 and S11 fixers named the S14 ones; no scene owner took them.
- **S06's `docker-shell-CLI.sh` window** still cuts line 20 after `"/secrets/` (`s06_cors.py:277`), the truncation
  the S04 fixer noted.
- **S14:** `git log` and `git tag -n` still run in the silence after the narration (about 6.5 s), as the issue's own
  fix accepted.
- **Toolkit:** the English "log in" break (`explainer/subtitles.py`, `_EN_COMPOUNDS`) belongs in a separate toolkit PR
  (AGENTS.md split).

## Final-cut checks (1080p60, 2026-11-04)

- **Tags** (`report-tags.md`): no blocking defect. All 16 tags checked on four frames each, none overlapping, none on
  past its scene; the review-bot list was empty (`[]`). Three notes are under "Open nits".
- **ASR** (`report-asr.md`): intelligible throughout; 0 real problems; three low-severity watch items.
- **Visual** (`report-visual.md`), on the first burned copy (before the re-burn; freezedetect on the clean cut):
  - 41 contact sheets (one frame every 3 s, 4×4 tiles), all read, plus about 60 full-size frames and crops.
  - All 16 chapters have content; the scene boundaries at 15:57 and 21:33 fall on a cleared frame by design; the
    frame at 32:09.0 and the last frame are uniform near-black (luma 14–17).
  - No object outside the frame, no garbled glyph, no tag left stuck. The ponder and quick-predict cards render
    cleanly. No instructor name in any sampled frame; a grep of the 12 `.srt`/`.ass` files found none.
  - Six low findings, none blocking (accepted item A4).
- **Pairs** (`report-pairs.md`, round 2): all 513 cues of `.zh-en.srt` re-read. All 12 round-1 findings are fixed; the
  burned frames show the new text (`pairs-v2-frames/`). No meaning swap anywhere. Four small offsets remain (F1–F4,
  accepted item A2), plus three English-only odd breaks.
- **Measured** (`report-measured.md`, `measured.json`, round 2): all four MP4s decode with 0 errors and 0 warnings.
  Formats, loudness, subtitles, chapters and the part split pass. The ponder density is decided under gate 3.

## Accepted items (coordinator decisions)

- **A1. Ten ponders and two quick predicts in 32:09** (0.62 ponders per 2 minutes), below AGENTS.md's aim of one per
  2 minutes. Accepted under Conny's 2026-10-21 decision to keep the current density of 3–5 ponders per lecture
  (「我觉得可以保留现在的密度」), which L11 exceeds; see gate 3.
- **A2. Residual subtitle pairing items** (`report-pairs.md`, `.zh-en.srt`). None reverses a meaning; another burn
  round costs about an hour of render for a cosmetic gain.
  - F1, cues 167–168 (10:14.6–10:20.2, S06): 按名字 ("by name") shows one cue early, and the English breaks between
    "calls" and its object. A side effect of the round-1 fix.
  - F2, cues 205–206 (12:35, S07): 维护着 ("keeps") one cue early.
  - F3, cues 216–217 (13:19, S07): cue 217 starts with a dangling 里.
  - F4, cues 500–501 (31:16, S16): 为什么 and 你的浏览器 each sit in the other cue from their English.
  - English-only odd breaks (the Chinese is fine): cues 109–110 "log / in" (06:46), 189–190 "repeat / for a few"
    (11:33), 442–443 "pointer file / changed" (27:25).
  - Also noted (`report-measured.md`): cue 349/350 (21:23–21:26), 空目录 one cue after "the empty folder", which a
    Chinese relative clause cannot avoid; and cues 156/157 (09:36) "answer / over" split on the English side.
- **A3. QA nits left as is:** the unspoken S07 "forgot -k" beat (about 13:53–13:57; the chip "forgot -k? · cli.py:123's
  typo: is required" is up about 3.7 s); the diagrams' `cheese-app-data-demo` against the viewer's
  `your-bucket-placeholder` (the stand-in convention is explained on screen, and S05 adds "the README's example name ·
  yours differs"); the "scene 10" (S02) and "scene 7" (S06) chips.
- **A4. Visual-pass low items** (`report-visual.md`):
  - 10:19.5 (S06): the emphasis pulse on `data-label-studio` overlaps its neighbouring glyphs for about 0.25 s
    (`frames/strip_label_url_617.5-620.png`).
  - 22:45–22:52 (S12): hash boxes cross the `.dvc/cache` panel edge for under a second
    (`frames/crop_dvccache_1365-1372.png`); 02:21–02:23 (S02): the "cloud credentials" pill passes over the
    "versioning station" label; crossfades at 04:00, 05:12 and 21:09 show two layers for under 1 s.
  - 08:30 (S05): the step tracker steps back from "step 6 of 6: Target storage" to "step 5 of 6: Source storage" as
    the narration returns to "add both storages and click sync".
  - 58 static stretches of 4.0–8.6 s in `freezedetect.log` (n=0.002, d=4); about 12 are ponder or quick-predict
    timers, the rest are diagrams or terminals held while the narration continues. The longest are 26:06.9 (8.6 s,
    README tool table), 06:32.5 (8.3 s), 23:38.4 (8.3 s) and 01:52.6 (8.0 s); the honest-note card at 08:00–08:27 has
    three holds of about 7 s.
- **A5. The instructor's name is masked** everywhere on screen and in subtitles (series rule): the e-mail shows as
  `student@example.com`, the Chinese says 授课老师 and the English "the instructor". `measured.json` lists no name hit
  in any output file; in the scenes' code the name occurs only in the masking regex and its docstring
  (`scenes/common.py:161`, `:165`).

## Open nits (not ruled on one by one; left for the coordinator)

None blocks release. Each needs a narration, yaml, `script.md` or scene change and a rebuild, which this record does
not make.
- **Tags:** S01's tag ("slides 20, 24") stays from 00:18.1 to the scene end, past its cited picture, which leaves at
  00:27.2; S08's ("slide 12") likewise covers the cleanup and outro beat. Both match their SHOW lines. S09's low tag is
  4 px above the README line-84 card from 16:37.5 to 16:49.0 (`tags/near_999.0_zoom.png`): not an overlap, the tightest
  spot in the video.
- **ASR watch items** (`report-asr.md`): "lakeFS" (cues 475–476, 30:17 and 30:25) is heard as "like FS" in places;
  "API Tokens Settings" (cue 207, 13:19.9) loses its plural "s"; "aarch64" (cue 161, 10:05.9) is heard as "Arch 64",
  an accepted way to say it.
- **The items under "Still open after QA"** that the coordinator did not rule on: the ticket's route line, the
  empty-version slip, the remaining soft wraps (S10, S14, S15), S06's cut code line and S14's silent extras. None was
  re-checked one by one on the final cut.
- **i18n notes:** `i18n/zh/glossary.yaml:713` (`first_use`) and `i18n/zh/GLOSSARY.md:263` still quote the old S12 line
  with 、 (the yaml and the subtitle use the new commas). Neither affects the subtitles.
- **`SLIDES.md` "This video and the slides"** still opens "The video is not scripted yet"; its map is from the
  digest's planned sections.
- **No `exercises.md`** in the episode folder. The recap says "Answers are in the exercises" (cue 500, 31:58.9) and
  "their labels join in exercise E7" (cue 487, 31:06.5); the footer card reads "Answers: exercises.md" beside the study-guide card.
  This record did not check whether the study guide holds those answers.
- **No `README.md` existed** before this pass; it was written now from `video.yaml`, `BRIEF.md`, `ASSETS.md`,
  `i18n/zh/README.md`, the transcript and the chapter files (see "Not claimed").
- **Chapters:** every start is the cumulative scene start rounded down (deltas 0 to −0.89 s). Harmless.

## Verified (final render)

All numbers are from `measured.json` and the five reports, on the files in `output/` as they are now (written
2026-11-04 07:29–08:19 UTC).

- **Files:** H.264 High, yuv420p, 1920×1080 at 60 fps, AAC LC 48 kHz stereo at about 167 kb/s, video at about
  313–348 kb/s. Each decodes in full with exit 0 and no error or warning lines (`measured2/<name>.ffmpeg.log`).

  | file | duration | video frames | size (bytes) | loudness | LRA | true peak |
  |---|---|---|---|---|---|---|
  | `ac215-l11-data-labeling-versioning.mp4` | 1929.122 s (32:09.1) | 115,743 | 123,180,029 | −16.1 LUFS | 2.7 LU | −2.7 dBTP |
  | `ac215-l11-data-labeling-versioning.zh-en.mp4` | 1929.122 s | 115,744 | 118,667,094 | −16.1 | 2.7 | −2.7 |
  | `ac215-l11-data-labeling-versioning_part1.mp4` | 958.633 s (15:58.6) | 57,516 | 59,321,606 | −16.1 | 2.6 | −2.7 |
  | `ac215-l11-data-labeling-versioning_part2.mp4` | 970.499 s (16:10.5) | 58,227 | 63,865,974 | −16.1 | 2.8 | −2.6 |

  In the clean cut the video stream ends 0.07 s before the audio (1929.050 s against 1929.122 s); the zh-en video
  stream is one frame longer than the clean cut's. The 16 scene renders sum to 1929.021 s (part 1 958.583 s, part 2
  970.438 s).
- **Subtitles:** `.srt` 502 cues, `.zh.srt` 432, `.zh-en.srt` 513. The parts have 245 / 218 / 257 and 257 / 214 / 256;
  the English parts sum to the full file (245 + 257 = 502), and the bilingual parts join to the full file cue for cue.
  - In all nine `.srt` files the cues are numbered 1..N and in order, inside the runtime, at least 1.000 s long, with
    no overlaps (0 findings).
  - The last cue ends at 1927.208 s, 1.9 s before the cut ends (part 1: 957.56 s in the English file, 957.88 s in the
    Chinese and bilingual files; part 2: 968.608 s).
  - The English stream of `.zh-en.srt` equals the `.srt` word for word (4,297 words); its Chinese stream equals
    `.zh.srt` once punctuation is ignored; the `.ass` text equals the `.zh-en.srt` for all 513 cues. The `.zh.srt`
    merges cues by design.
- **Chapters:** 16 entries, titles equal to `video.yaml`'s in order, each start the running total of the scene renders
  rounded down (S09 at 958.583 s = 15:58, S16 at 1813.788 s = 30:13). `chapters_part1.txt` (8 entries) and
  `chapters_part2.txt` (8, at 00:00, 01:48, 03:45, 05:35, 08:16, 10:17, 12:21, 14:15) match. `README.md` now carries
  them.
- **Scenes:** all 16 present; the chapter starts match the scene durations, so no scene is missing or doubled.
- **Adversarial re-check** (a separate verifier agent, 2026-11-04, `verifier/`): ffprobe on all four MP4s (durations,
  frame counts, sizes, codecs), an ebur128 pass on the clean cut's audio (−16.1 LUFS, LRA 2.7 LU, −2.7 dBFS true
  peak), the cue counts of all nine `.srt` and three `.ass` files, the chapter starts against the 16 scene renders,
  every quoted cue and time in this record against the `.srt`, the ponder timers against the scene code, the SAY and
  anchor counts, and the QA tallies against the QA output. It corrected two ponder lead-in times, the commit for the
  rebuilt full-cut subtitles, the part-1 last-cue time, the masking attribution and the ponder-density wording.
- **Narration:** 113 SAY lines, 4,352 words, 154.0 wpm over 1,695.9 s of voice; 651 anchors; no "anchor not found" in
  the 16 render logs.
- **Lecture tags:** 16, each found, none overlapping, none left on past its scene (`tags/`).
- **Privacy:**
  - The instructor appears only as "the instructor" / 授课老师 (A5); the login is `student@example.com`, the token the
    obviously fake `student-demo-token-not-a-secret`, the bucket `your-bucket-placeholder`, the project
    `your-gcp-project`, the GitHub user `YOUR_GITHUB_USERNAME` (`ASSETS.md`, "Capture-only deviations").
  - The key in the folder listings is an obviously invalid 422-byte stand-in, moved out before every cloud step, and
    S05 says so.
- **Provenance** (`ASSETS.md`):
  - Terminal lines come from the 2026-10-23 captures in `assets/terminal/`; each README command ran exactly as written,
    in README order, with extras tagged `extra`.
  - Live and local: Label Studio 1.23.0 in its container and its HTTP API, the CLI container, `cli.py -p` / `-t`
    (the 401 and the legacy-token fix), the compose Extra, the DVC image build (the starter's apt failure and the
    `Dockerfile:36` fix), the entrypoint, `dvc init` / `add`, the cache layout, the git commits and tags, and the v20
    fingerprint `89db50de27acfd6822faabc3da39b0a8.dir`, byte-identical to the class repo's `dataset_v20` pointer.
  - Every success that needs a Google credential or bucket (`cli.py -c` / `-m`, *Check Connection*, the gcsfuse
    mount, `dvc push` to GCS, Colab's `dvc get`) is tagged `recorded` with its source; the push counts (5, then 2)
    come from a local stand-in remote, tagged `extra · local remote`.
  - The GCP console, the Label Studio UI, GitHub and Colab pages are drawings tagged `illustration`; Label Studio's
    clicks are replayed through its API and tagged `stand-in` (3 tasks here, 21 for the viewer).
  - Code panels quote `assets/source/` at the pinned commits.

## Not claimed

- **No human listened to this cut** or watched it. The listening gate rests on the series waiver quoted under gate 6,
  and the audio was checked only by machine (the ASR round trip and the onset check, run on the first final cut, whose
  audio the re-burn did not change). The three ASR watch items are unresolved by ear, and the ten lexicon fixes were
  checked by phonemizer and ASR, not by a listener.
- **The Chinese subtitles were reviewed by agents only:** the QA subtitle watcher, the narration/subtitle fixer, the
  scene verifiers and the two final pairs checks. No human translator or native reviewer read them.
- **No Google Cloud step ran.** The recording had no credentials and no bucket, so the console steps (service account,
  role, key, buckets and folders, uploads), Label Studio's *Check Connection* and storage sync against GCS,
  `cli.py -c` / `-m`, the gcsfuse mount, `dvc push` to the bucket and Colab's `dvc get` from it are drawings,
  `recorded` sources or narration. In particular, the thumbnails' CORS failure and fix are browser behaviour that was
  drawn, never observed, and the "5 files pushed" / "2 files pushed" counts are from a local stand-in remote, not GCS.
- **No GitHub push ran** (no SSH route): creating the private repo and `git push --atomic` to it are drawn or
  narrated.
- **No Docker Desktop and no Mac run.** The laptop was Docker Engine 29.8.2 (dind) on linux/amd64; Docker Desktop's handling of the root-owned folder and the "aarch64" line are explained, not run on a Mac.
- **The visual check sampled one frame every 3 s**, plus targeted frames. Motion between samples was checked only by
  `freezedetect`, whose threshold can miss small motion, and by the tags check's 2 fps scan of the tag region. The
  tags, ASR and visual checks ran on the first final cut; the re-burned `.zh-en.mp4` was checked only by the round-2
  pairs check's six burned frames, the measured decode and four frames the verifier pulled (08:30.5, 13:55, 16:57,
  32:08.9).
- **Some QA fixes were verified only on previews** (`-q m` or 720p frames, before the 1080p60 renders), not one by one
  on the final cut; the final-cut checks cover them only by their own sampling.
- **No check in this record looked for credentials on screen**; `ASSETS.md` says no plausible private key is ever
  rendered.
- **Name search:** the output grep finds text in the subtitle, chapter and transcript files, not in burned-in pixels;
  on screen, the mask rests on the masking code (`scenes/common.py:161–165`) and the sampled frames.
  `video.yaml`'s Bilibili description credits the course staff by name, as L02–L10 do; that text is not on screen.
- **Review bots:** the QA follow-ups watcher read the five Bugbot threads on L11 files in PR #50. Nothing in this
  record checks for bot comments posted later. No `QA_FOLLOWUPS.md` exists for L11.
- **`README.md` was written in this pass** from the episode's own files; its chapter summaries were not reviewed by a
  separate agent.
- **Every check in this record is an agent's.**
