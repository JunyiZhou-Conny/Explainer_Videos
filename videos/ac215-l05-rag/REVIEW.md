# Review record: AC215 · Lecture 5 — Introduction to RAG: chunk, embed, load, query, chat

Follow-along of [dlops-io/llm-rag](https://github.com/dlops-io/llm-rag), branch `main` @ `e17a39f`
(the whole README up to *Advanced RAG: Semantic Chunking*; *Agents* is previewed for L06). The issue
of record is Explainer_Videos#38. The work is in the series draft PR Explainer_Videos#29 (branch
`claude/mlops-learning-videos-7b5use`). Claude Code cloud sessions (Claude) produced it:

- **Captures:** 2026-10-16, 00:52–00:57 UTC, on a fresh Docker Engine 29.8.2 "laptop" with no
  Google key (`ASSETS.md`).
- **First finishing pass (`we2lzv8iu`, 21 agents, output dated 2026-10-19 01:12 UTC):** critiques of
  S12–S16 (each checked by a verifier), the `QA_FOLLOWUPS.md` review-bot items for S03, S04, S08, S09
  and S11 (fixer and verifier each), and a Chinese proofread that also wrote `i18n/zh/README.md`.
- **QA draft:** the 480p15 draft was stitched on 2026-10-19 at about 01:27–01:32 UTC (draft
  commit `2ec544a`; `build/qa/scenes.json` at 01:32) and runs 30:42.8 (1842.812 s).
- **Whole-video QA (`w6byzicvp`, 39 agents, output dated 2026-10-19 18:16 UTC, commit `c101d80`):**
  seven watchers, one scene fixer for each of S02–S16 (15; S01's only finding was a subtitle line,
  left to the text fixer), one narration/subtitle fixer and one verifier per scene (16).
- **Second finishing pass (`w6tfmzqr5`, 18 agents, output dated 22:20 UTC, commit `8f71867` at
  22:21 UTC):** the shared `scenes/common.py` fixes from the QA (one owner, then a verifier on
  frames), then a plan of 18 text items and 7 scene items, each scene followed by a verifier.
- **1080p60 renders:** all 16 scenes, 2026-10-19 22:21:42–22:55:46 UTC, every one started after the
  last source edit (22:20:35 UTC; `measured.json` `renders`).
- **First final cut (31:07.4):** stitched from those renders on 2026-10-19: the clean cut and its
  subtitles at 23:11, the zh-en copy at 23:28 and the parts at 23:30–23:31 UTC. Subtitles, chapters
  and transcript are committed in `f466f8e` (2026-10-20 01:43 UTC).
- **Final-cut checks:** five agent checks on 2026-10-20 (reports `build/final-review/report-*.md`,
  all five present). The ASR data was written at 01:49 UTC; the tags, pairs and ASR reports were
  saved at 06:43. A usage limit cut the first visual and measured attempts; both were re-run
  (`measured.json` at 06:59, both reports at 07:35 UTC). Each re-run says which earlier files it set
  aside: the visual pass moved the first attempt's sheets to `sheets_prev_label-offset/` (their
  labels ran about 1.5 s ahead of the picture) and did not use its freeze list
  (`visual/freeze_vs_events.txt`, which counted fades as freezes); the measured pass checked the
  first attempt's `measured/` (its light checks are identical on every shared field) and re-ran
  every decode and loudness pass into `measured_v2/`.
- **First version of this record:** written 2026-10-20 at about 07:40–08:00 UTC and committed with the
  `publish:` block in `video.yaml` (`01dac58`, 08:09 UTC). Every defect was then open in the first
  final cut, with its planned fix.
- **Fix round 1** (plan `/root/ac215-backup/args/l05-fix1.json`, 07:37 UTC; output
  `/root/ac215-backup/tasks/w0eoryitz.output`; commit `8b1e030`, 09:16 UTC): one text agent (the
  T1–T4 sentence splits and the P1, P2, P4 and P5 Chinese cues in `script.md`,
  `i18n/zh/narration/g1.yaml` and `g2.yaml`, and the anchor strings in S04 and S08), one shared agent
  (sequential `lref_swap` and an L05 version of `Terminal._make_room` in `scenes/common.py`; the
  `explainer/` toolkit is untouched) and scene fixes in S01 + S15, S06, S12 and S16. A skeptical
  verifier checked the shared and scene fixes on fresh 720p frames (`build/fix1/`); the text agent
  checked its cue pairs with the splitter, and `python -m explainer.i18n check` printed OK.
- **Fix round 1b** (output `/root/ac215-backup/tasks/w8umzlyij.output`; commit `1173d22`, 09:37 UTC):
  the four S10 items and S06's seam copies from the smaller-nits list, plus S06's visualizer bars
  (noticed in fix round 1), each checked by a verifier (`build/fix1b/`).
- **1080p60 re-renders:** all 16 scenes (every scene imports `common.py`), 2026-10-20
  09:16:25–10:10:02 UTC, each started after its last source edit (`recheck/measured.json`
  `provenance`).
- **Re-stitched cut (31:07.3):** scene segments 10:11–10:31 UTC, the clean cut and its subtitles at
  10:34, the zh-en copy at 10:59 and the parts at 11:01–11:02 UTC. Subtitles, chapters and transcript
  are committed in `5c0c800` (11:03 UTC).
- **Re-check:** three agent checks of the re-stitched cut on 2026-10-20, about 11:04–12:03 UTC: the
  changed scenes on frames, the measured checks and an ASR round trip (evidence in `build/recheck/`).
  For the update below, the 11 review-bot items and the shared `common.py` items were re-checked on
  frames of the re-stitched cut (`recheck/bot/`, about 12:05–12:15 UTC).
- **Update after fix rounds 1 and 1b:** 2026-10-20, about 12:15–12:25 UTC (committed in `f6e6398`,
  12:40 UTC). Items those fix rounds closed moved to "Fixed"; the rest stayed under "Still open" with
  their reasons.
- **Adversarial check of that update:** 2026-10-20, about 12:20–12:50 UTC (evidence in
  `recheck/adv/`): `ebur128=peak=true` and ffprobe re-run on all four MP4s, cue counts, gaps and the
  cue-level diff re-derived from the files, chapters recomputed from the stitched segments, and frames
  re-extracted for the visual claims. It corrected the scroll count (31, not 26), the S04, S06, S12
  and S13 timings, the S12 box geometry (items 16 and 26), the scene-join numbers (item 27) and the
  continuation-cue count, and looked at S16's section switch in the re-stitched cut (item 8).
- **Fix round 2** (plan `/root/ac215-backup/args/l05-fix2.json`, 12:41 UTC; output
  `/root/ac215-backup/tasks/wqzc3a236.output`, 8 agents, dated 16:42 UTC; commit `c187f3b`, 17:02
  UTC):
  - **Items:** item 8 in `scenes/common.py` (`switch_section()` sequential) and items 23–26 in S05,
    S10, S12 and S14. A verifier checked each on fresh 720p renders. The S05 verifier replaced a fourth
    copy flight. The S12 verifier moved box 358's bottom edge, which the fix had put on the
    underscores of line 358's own text.
  - **Sweep of all 16 scenes:** copy flights over text, flashes that fill a label's own box, and
    double-exposed swaps. 52 candidates, 29 real. 26 were fixed in 10 scene files and verified frame
    by frame on fresh 720p renders; the verifier found one more (S15's "①ndexing") and fixed it. The
    other three real ones were tracker caption step changes; they were fixed in `common.py`
    (`_swap_caption`: old caption out, a short gap, new caption in). That edit came after the
    eight agents had finished (`common.py` saved at 16:42:50 UTC): no fix-round verifier saw it, only
    the coordinator's one S09 strip (`fix2/coord/s09_step_swap.png`) and then the round-2 frame check.
  - **What did not change:** no scene's length, no existing play's run time, and no narration or
    subtitle text. One play was added: S10's 0.3 s fade before V2's shrink (item 24), so that 1.0 s
    shrink now runs 0.3 s later inside the same narration block. Evidence in `build/fix2/`
    (`shared/`, `S05/`, `S10+S12+S14/`, `sweep/`, each with a `verify/` folder, and `coord/`).
- **1080p60 re-renders:** all 16 scenes, 2026-10-20 17:02:17–17:45:55 UTC, each started after the
  last source edit (`common.py`, 16:42:50 UTC; `recheck2/provenance.json`).
- **Round-2 cut (the cut this record now describes, 31:07.3):**
  - **Stitch:** scene segments 17:46:53–18:08:35 UTC. The clean cut and its subtitles were written at
    18:11, the chapters, the transcript and the zh-en copy at 18:32, and the parts at 18:34–18:35 UTC.
  - **No new output commit:** the stitch rewrote the subtitles, chapters and transcript
    byte-identical to `5c0c800`. `git diff 983e36e -- videos/ac215-l05-rag/output` is empty, and HEAD
    `983e36e` has no episode or toolkit change since `c187f3b`.
- **Re-check 2:** two agent checks of the round-2 cut on 2026-10-20, with evidence in
  `build/recheck2/` (`build/recheck/` keeps the previous round's):
  - the measured checks, 18:36:59–18:48:27 UTC;
  - a frame check of every changed moment, every tracker step change and section switch, and all 16
    scenes, about 18:37–19:03 UTC.
  There was no new ASR round trip: the audio is bit-identical to the re-stitched cut's.
- **This update:** 2026-10-20, about 19:05–19:20 UTC. Items fix round 2 closed moved to "Fixed". The
  new observations went under "Still open" (items 28–30 and smaller nits).
- **Adversarial check of this update:** 2026-10-20, about 19:15–19:35 UTC (evidence in
  `recheck2/adv/`): ffprobe, SHA-256, the audio packet MD5 and `ebur128=peak=true` re-run on all four
  MP4s; cue counts, chapters, scene starts, render times and the tracked-file diffs re-derived; all
  15 tracker step changes and the three section switches decoded frame by frame; frames re-extracted
  for every changed moment, items 28–30 and the open nits, and a subtitle-band pass over the burned
  copy, and the round-2 cut's audio packet timestamps re-read. It corrected the by-design list
  (17:40.5 was not replaced), the "no timing moved" wording (S10's shrink runs 0.3 s later), the
  subtitle-band box (measured at full resolution), the sweep's not-real count, item 27 (timestamps
  now re-read) and the nits it saw again in the round-2 cut.

This record is based on the five checks' reports, `measured.json`, the evidence folders beside
them, the QA and finishing-pass outputs (`/root/ac215-backup/tasks/w6byzicvp.output`,
`we2lzv8iu.output`, `w6tfmzqr5.output`), `script.md` and `BRIEF.md` (as committed in `f466f8e`),
`ASSETS.md` and `SLIDES.md`. The update adds the fix-round outputs (`w0eoryitz.output`,
`w8umzlyij.output`), the re-check's three reports and its evidence (`build/recheck/`:
`measured.json`, `asr-summary.json`, `notes.txt`, `strips/`, `sheets/`, `subcheck/`, `bot/`) and
`script.md` as committed in `5c0c800`. This version adds fix round 2's plan, output and evidence
(`l05-fix2.json`, `wqzc3a236.output`, `build/fix2/`) and re-check 2's two reports and evidence
(`build/recheck2/`: `measured.json`, `provenance.json`, `committed_vs_output.json`, `audio_md5.json`,
`zhen_geometry.json`, `logs/`, and in `visual/`: `findings.json`, `tracker_changes.json`,
`tracker_steps_metric.json`, `subtitle_band.json`, `strips/`, `sheets/`, `frames/`), plus the
adversarial check of this version (`build/recheck2/adv/`). Verified facts and unclaimed reviews are
kept in separate sections.

**Conventions in this record:**
- **Times** are mm:ss in the full video. Gates 3 and 6, both re-check sections, "Fixed", "Still
  open" and "Verified" use the round-2 cut (`output/ac215-l05-rag.mp4`, 31:07.3). Fix round 2 moved
  no scene start and changed no scene's length or frame count (`recheck2/measured.json` `scenes`), so
  a time in the round-2 cut is the same moment of the narration as in the re-stitched cut (only
  S10's shrink, item 24, now runs 0.3 s later in the picture). Gates 1,
  2, 4 and 5, "Whole-video QA" and "Final-cut checks" use the first final cut (31:07.4), except where
  marked *draft* or *preview*. Between the first final cut and the re-stitched cut a scene's start moved by 0 s (S01–S04),
  +0.316/+0.317 s (S05–S08), +0.016/+0.017 s (S09–S12) or −0.116/−0.117 s (S13–S16): S04 grew by
  0.317 s and S08 and S12 shrank by 0.300 s and 0.133 s with the T1–T4 sentences
  (`recheck/scene_starts_old_vs_new.json`). Inside S04, S08 and S12, moments after those sentences
  moved with them.
- **Draft times** refer to the 480p QA draft (30:42.8). Later fixes made the video 24.6 s longer;
  scene starts moved by up to 19.7 s (S16 started at draft 28:30 and at 28:49.7 in the first final
  cut), and S16 itself grew by about 5 s, so a draft time can be up to about 25 s earlier than the
  same moment in the first final cut (24.6 s at the very end).
- **Cue numbers** say which file they come from: `.srt`, `.zh.srt` or `.zh-en.srt`. In the sections
  that use the re-stitched or round-2 cut they number those cuts' files, which are byte-identical
  (514, 424 and 508 cues); elsewhere they number
  the first final cut's (513, 423 and 510). From S04's new sentence on, the two numberings differ
  (`recheck/subtitle_changes_old_vs_new.txt` lists every changed cue in both).
- **Evidence paths** are relative to `build/final-review/` (`verifier/` holds the frames, cue lists
  and loudness log of the adversarial check of the first version), except paths that start with
  `recheck/` (`build/recheck/`), `recheck2/` (`build/recheck2/`), `fix1/`, `fix1b/` or `fix2/`
  (`build/fix1/`, `build/fix1b/`, `build/fix2/`). The folders are
  git-ignored and exist only in the producing session, so a successor has to re-run the checks to
  reproduce the evidence. Times taken from a verifier's 720p preview are given as scene time plus the
  scene's start in the first final cut, and are marked *preview*.

## Content gates (AGENTS.md)

1. **Hook** ✔. S01 opens on a question and a model that cannot answer it, not on a value
   proposition.
   - The README's own sample question types into a chat box: "how is Tolminc cheese made?"
     (00:00.0–00:05.0). The answer "lives in one particular text": the instructor's short story, a
     fictional tale (00:16.6), which "a model trained before that story existed has never read"
     (00:20.2). "How do we make it answer from this story, without retraining it?" (00:26.3–00:29.7).
   - The lecture's four questions (embedding, vector database, query, context) are posed over A11's
     blurred map at 01:01.7, with "This video answers all four" (01:05.9).
   - **Payoffs:** S13 closes the puzzle: "The story is fiction, so an answer about Mara, her
     grandfather and the curd came from your chunks" (25:01.3–25:07.1). S16 answers the four
     questions one by one with thumbnails of the pictures that answered them (30:15.5–30:30.2).
2. **Intuition before formalism, with an animated mechanism for each core idea** ✔.
   BRIEF.md ("Visual set pieces") defines eight. Each appears before the commands it explains:
   - **V1, two lanes, one database (S02; mini-map in S06–S14).** "Here's RAG in four boxes"
     (01:40.2), then "Open the RAG box and you get two lanes" (01:56.8): the books → chunks →
     embedding model → vectors → database lane above the question → same model → query vector lane,
     B5's three phases (02:13.9–02:26.7), the README's flags pinned under the boxes.
   - **V2, two containers, one network, three windows (S04, S05; lifecycle in S10, S16).** "The
     compose file draws the whole picture: one network, by name…" (05:38.0); "The CLI finds Chroma by
     name, through the network's phone book" (07:58.9); `exit` and `docker compose down` remove the
     boxes while the data folder stays (18:46.7; S16 again from 28:51).
   - **V3, ruler and scissors (S06, S07).** "Character splitting is a ruler" (09:35.4): windows of
     350 that add 330 each (10:10.6), the 20-character seam on the real story (B14–B15,
     10:49.8–11:05.3); then scissors "that look for the best gap" (11:28.7) and the hidden overlap.
   - **V4, meaning as direction (S08).** Chunk cards become arrows on a sphere, "similar meanings
     point in similar directions" (13:04.9); the lecture's personality game, cosine against the dot
     product (13:12.6–13:39.5); the real vectors' lengths, 0.369–0.402 (15:20.2).
   - **V5, records, an index, a folder (S09).** SQL table against vector database (A30–A31,
     15:56.3–16:07.9); "Comparing a question with every vector is slow at scale" (16:28.9), the
     pointer scan and the layered-graph illustration of HNSW (A32–A38, to 16:42.1); the files on your
     disk, "two index folders, one per collection, owned by root" (17:45.9).
   - **V6, rank, cut, and filter first (S11, S12).** The lecture's score column, re-sort and top-K
     line (A48–A53, 19:46.1–20:24.5), then the flip to Chroma's distance, "Same order, opposite
     direction" (20:07.1–20:15.0); the cloud of all 8,248 chunks (one dot ≈ 8 chunks) masked to 1,355
     and 64, "The filters act first" (22:34.6), and the filter box sliding before Querying on A54–A55's strip (22:41.6–22:53.2).
   - **V7, the final prompt (S13).** The lecture's three-part prompt (23:33.5), the tutorial's prompt
     card and LLM, the unplugged system instruction: "Line 40 defines one… It's never sent."
     (24:00.2–24:09.0), the one-line fix (24:09.3); "No weights moved. Delete the collection, and the
     knowledge is gone." (24:24.9–24:29.3).
   - **V8, a seismograph of meaning (S14).** The lecture's anchor walk, then the code's rule: every
     window's distance to the next plotted "like a seismograph" (25:53.7–26:00.1) and the 95th
     percentile line (26:00.3).
   - S15 adds the lecture-only levers as dashed concept panels (27:23.5–28:38.3) and S16 the Self-RAG
     "Retrieve?" diamond (30:03.7–30:16.1).

   **How this was checked:** QA's director watchers read every draft sheet against the SHOW lines.
   In the first final cut, the tag check found the cited picture on screen across the lecture-slide
   tag spans, except T04, which by design demonstrates the tag itself, and T02 and T08 (items 2 and
   3); the visual pass read the burned-in copy every 3 s. Fix round 1 fixed T02 and T08: in the
   re-stitched cut A8–A10 stays on through road 3 and A19–A22 leaves with beat 0's picture ("Fixed",
   items 2 and 3).
3. **Pause-and-ponder moments and a recap** ⚠ partly met.
   - **Ponders:** five cards, each a 0.6 s fade-in and an 8 s silent timer; each answer starts as its
     timer ends or after it (`recheck/measured.json` `ponder`). No English cue plays during a timer:
     the five longest cue gaps (8.8–11.8 s) are these five windows.

     | scene | question (card text, condensed) | card | timer | answer starts |
     |---|---|---|---|---|
     | S06 | 7,808 characters, windows of 350 overlapping by 20: how many chunks? | 10:02.3 | 10:02.9–10:10.9 | 10:10.9 |
     | S07 | Same chunk size, 350: why 14,228 chunks instead of 8,248? | 12:06.8 | 12:07.4–12:15.4 | 12:18.4 |
     | S08 | The database will compare by cosine; these vectors are shorter than 1: does that change which chunks count as nearest? | 15:34.9 | 15:35.5–15:43.5 | 15:43.5 |
     | S12 | The question is about Tolminc; the query keeps one book and only chunks containing "Italian": what will the ten results be about? | 21:43.4 | 21:44.0–21:52.0 | 21:52.0 |
     | S14 | char-split ran the chunk step without a key. Can semantic-split? | 26:14.0 | 26:14.6–26:22.6 | 26:22.6 |

   - **Rate:** one ponder every 6.2 min. AGENTS.md aims for one every 2 min, about 15.6 at this
     length; the series brief fixes 3–5 per lecture (`ac215-video` skill, step 3), and BRIEF.md plans
     these five. None falls in the first 10 minutes: the longest gaps are 00:00–10:02 (S01 to the
     middle of S06) and 15:43–21:43.
   - **Follow-along pauses:** separately, 14 spoken "Pause …" lines tell the viewer to stop and run a
     step, from "Pause and do both, in your course folder." (03:41.3) to "Pause, then tear down, so
     port 8000 is free next time." (29:34.0). They are not ponders.
   - **Recap** ✔: S16 answers the four opening questions in speech, "An embedding is a direction for
     meaning…" (30:15.4–30:30.1), asks five test-yourself questions (30:30.4–30:56.2) and points to
     the answers and the study guide (30:56.5–31:05.5). Part 1 closes on "The top lane is done: the
     index is built. In part 2, we ask it questions." (18:03.5–18:08.6) and part 2 reopens with a
     one-line recap (18:09.9).
   - **Open question for Conny (as for L03 and L04):** does the series format, five ponders plus a
     spoken recap and five questions, satisfy this gate for AC215?
4. **Narration written for the ear, with word-anchored cues** ✔.
   - **Spoken style:** script.md's conventions apply: commands, flags and paths are said in words
     ("dash dash chunk", "chunk type char split", "slash app"), versions that will change are said
     "at the time of recording", no `'s` after a digit, every sentence under 30 words.
   - **Size (re-stitched and round-2 cuts):** 140 SAY lines and 4,339 words, identical to the 140
     narration blocks in the renders (`recheck/measured.json` and `recheck2/measured.json`
     `narration`). Kokoro `af_heart` at speed 0.9 in all 16 scenes. Pace 139.4 wpm over the runtime,
     151.4 wpm over voiced time (28:39.5, 92.1 % of the runtime).
   - **Anchors:** 617 `vo.wait_until` calls across the 16 scene files (23 in S07 to 54 in S09; 6 take
     a variable instead of a literal phrase). The 16 1080p60 render logs of each re-render (after fix
     rounds 1/1b and after fix round 2) have 0 "anchor not found" warnings.
   - **Ear fixes after the draft:** "lecture 4's three gates" (the possessive was swallowed) became
     "Remember the three gates from lecture 4" (04:13.9); the spoken numbers in S08, S11 and S12 got
     their own sentences so a voice mark starts their cues ("24 rows of 256 numbers." 15:16.7;
     "0.57, 0.77, 0.43, 0.93." 19:49.6; "Their distances run from 0.28 to 0.31." 22:29.8); "cents"
     (which the QA's ASR heard as "sense") became "a few cents" (14:53.9); "the function the chunker is handed" became
     "the function handed to the chunker" (26:28.8); the new "Our chat" was phonemized and checked by
     ASR not to be heard as "a chat". Tolminc is respelled "tole-mints" in the lexicon.
   - **Fix round 1 (T1–T4; re-stitched cut times):** four more sentences were split so a voice mark
     starts the cue after each number or command: "Its context was 112 megabytes." (S04, 06:44.0),
     "The code asks for the first 256." (S08, 13:46.9), "It's the first call to Google." (S08,
     14:14.5) and "The word Italian keeps 64." (S12, 22:02.1). Kokoro reads each as intended (fixer's
     phonemizer check; the re-check's ASR heard them as written).
   - **Caveat:** inside a sentence, cue boundaries are still timed by displayed characters. After fix
     round 1 no continuation cue appears more than 1.0 s before its words; the largest lead is
     0.94 s ("Fixed", item 9).
5. **Simulated-target-viewer QA over the full draft** ✔.
   - Seven watchers reviewed the 480p draft. Two were simulated target viewers ("newcomer", one per
     part): agents that read the draft's contact sheets, pulled frames and read the English `.srt`
     with the README open, step by step. Neither played the draft or listened to it.
   - They reported 71 timestamped findings: 0 must, 41 should and 30 nit; the two newcomers reported
     30 of them.
   - 40 of the 41 shoulds are fixed and were verified on fresh 480p or 720p renders; the one open
     should (mid-sentence cue timing) is a shared-toolkit item that the episode works around where
     it is worst (fix round 1 added four more workarounds, T1–T4). Of the 30 nits, 27 were fixed
     before the final cut (one by a scene workaround) and three shared-code nits stayed open; fix
     round 1 worked around two of them in the episode (the terminal scroll, by an L05 rebinding of
     `_make_room` in `scenes/common.py`; the split S08 step-1 command, by T3), so one is open (tag
     height, "Still open", item 7). The toolkit (`explainer/`) is unchanged. Details under
     "Whole-video QA".
6. **Measured checks** ✔. The numbers are under "Verified (round-2 cut)" (`recheck2/measured.json`).
   - **Duration:** 31:07.3 (1867.296 s), inside the series' 25–35 min; parts 18:10.0 (1089.988 s)
     and 12:57.4 (777.422 s). Unchanged by fix round 2.
   - **Loudness:** −16.0 LUFS integrated in the clean cut and the zh-en copy and −16.1 LUFS in the
     parts, LRA 2.3–2.4 LU; true peak −2.6 dBTP in the clean cut, the zh-en copy and part 2, and
     −2.8 dBTP in part 1. The build's target is −16 LUFS with true peak at or below −1.5 dBTP:
     **every file meets it**, with at least 1.1 dB to spare. The figures are the same as before fix
     round 2, whose audio is bit-identical to the re-stitched cut's.
   - **Caption bounds:** in the zh-en copy every one of the 508 cues is one Chinese line over one
     English line (WrapStyle 2, exactly one `\N` per Dialogue line in all three `.zh-en.ass` files),
     in the band under the picture (the picture is scaled to 1670×938 at the top). A full-resolution
     pixel check of the round-2 burned copy took one frame every 2 s over all 16 scenes (934 samples,
     835 of them with subtitle ink): every subtitle was inside y 991–1063 and x 443–1476, the same
     box as in the re-stitched copy, and nothing was drawn at y 900–990, between the picture
     (y 0–940) and the subtitles, in any sample (`recheck2/adv/band.json`). The frame check's coarser
     pass on 640×360 samples agrees within its 3 px steps (933 samples, 822 with a subtitle,
     y 990–1059, x 444–1473, nothing at y 948–975; `recheck2/visual/subtitle_band.json`). So no
     subtitle covers a command or a tag.
   - **Music balance:** does not apply. L05, like L02–L04, has no score: `video.yaml` has no `music:`
     key.
   - **Subtitle sync:** the four cues that came 1.0–1.6 s early are sentence starts now and appear
     0.04–0.08 s before their speech; no continuation cue is more than 1.0 s early ("Fixed", item 9).

   **Human review:** the series waiver below stands in for a listening sign-off.

   Listening sign-off: waived by Conny for the AC215 series (Explainer_Videos#29, 2026-10-15): 「不需要，我现在对视频质量很满意的」 — no human listened to this cut; the ASR round trip below is the substitute.

   **No ASR round trip ran on this cut.** Both ASR round trips ran on earlier stitches:
   - **Final-cut checks:** the first final cut, the 31:07.4 clean cut of 2026-10-19 23:11 UTC, whose
     zh-en copy carried bit-identical audio.
   - **Re-check:** the re-stitched cut of 2026-10-20 10:34 UTC (`5c0c800`).

   The round-2 cut's audio packets are bit-identical to the re-stitched cut's: MD5
   `ad24cc8b82ce12d2bed3b27257ba5933` in both the clean cut and the zh-en copy
   (`recheck2/audio_md5.json`). Fix round 2 changed S01, S03, S04, S05, S07, S08, S09, S10, S12, S13,
   S14 and S15, and every scene through `common.py`. **No scene's narration changed in fix round 2:**
   - no SAY line changed: 140 lines and 4,339 words, matching the rendered sidecars;
   - the subtitle files are byte-identical to `5c0c800`.

   Those scenes' audio was checked only as the measured check reports: by that packet MD5, not by ASR
   or by ear.

   Before that, between the first final cut and the re-stitched cut, the narration of three scenes
   changed, all in fix round 1:
   - **S04:** T4, "Its context was 112 megabytes. Most of it is git history, which still holds…".
   - **S08:** T1, "…3,072 numbers. The code asks for the first 256. The model is trained…"; and T3,
     "Step 1: … char split. It's the first call to Google.".
   - **S12:** T2, "…keeps 1,355. The word Italian keeps 64.".

   No other SAY line changed (`git diff f466f8e 5c0c800 -- script.md`). The changed sentences' audio
   was checked by machine only. The changed-scene check measured their speech onsets against the new
   cues. The re-check ran a second ASR round trip over the whole re-stitched cut (the zh-en copy has
   the same audio packets), which heard all four as written ("ASR round trip on the re-stitched cut"
   below). The same audio is in the round-2 cut.

## Whole-video QA (480p draft, 2026-10-19; times are draft times)

**Watchers and findings.** Seven watchers reported 71 findings: 0 must, 41 should and 30 nit
(`w6byzicvp`, key `result`; 14 of them target shared code).

| watcher | lens | must | should | nit |
|---|---|---|---|---|
| director, part 1 (S01–S09) | facts, commands and terminal lines against the README, captures, source and SLIDES.md; tracker; sync | 0 | 3 | 4 |
| newcomer, part 1 | simulated target viewer, README open, own terminal | 0 | 10 | 5 |
| director, part 2 (S10–S16) | the same, plus pauses measured with silencedetect | 0 | 5 | 6 |
| newcomer, part 2 | simulated target viewer | 0 | 8 | 7 |
| subtitles (zh, zh-en, en) | glossary, cue and line breaks, pairing; every proposed line rebuilt in memory | 0 | 11 | 4 |
| follow-ups (`QA_FOLLOWUPS.md`) | the 11 logged review-bot items, on fresh 720p frames and a `beside()` sweep | 0 | 0 | 2 |
| ASR (base.en, large-v3-turbo) | mishearings, cue sync | 0 | 4 | 2 |
| **total** | | **0** | **41** | **30** |

**What held up in the draft:**
- Every number on screen and in the subtitles matched the captures, source and slides: Docker 29.8.2
  and Compose v5.6.0, the 81.5 s build and 112.26MB context, 24 / 8,248 / 35 / 14,228 chunks and
  1 + ⌈7,458/330⌉ = 24, the personality game's 0.986 / 0.976 / 0.886 and 80.2 / 81.2 (recomputed
  from SLIDES.md), 89 and 148 embedding calls, 59781120 bytes, 1,355 / 64 / 0, the RRF values
  0.75 / 0.67 / 0.42. The Chinese numbers matched the English ones.
- Every README command was typed exactly as the README spells it, in README order, and every
  your-turn had a pause instruction and a visible hold. Every scene ended on an empty frame.
- None of the 11 `QA_FOLLOWUPS.md` items was still real (follow-ups watcher).
- `python -m explainer.i18n check videos/ac215-l05-rag --lang zh` printed OK.

**No must.** No watcher found a wrong fact or a missing step that would stop a viewer.

**The shoulds: 40 of 41 fixed, verified on fresh 480p/720p renders.** By theme:
- **Follow-along (10):**
  - S06 (draft 10:50) and S07 (12:15): the extra `python -c` one-liners were complete for only about
    1 s. S06 now keeps its command and output together in an 8-row strip (the command readable for
    about 9.4 s); S07 types its one-liner before the narration and fades it in place, so the output no
    longer scrolls it away (readable for about 2.9 s).
  - S08: the cosine ponder said "collection" and showed `hnsw:space` before S09 explains them; the
    narration and the card now say "Our database will compare by cosine (set when we load)", with a
    grey note "the measure, set at load (next scene)" under the chip. The personality game now asks
    its question aloud ("which of three candidates is most like the instructor?", final 13:15.9)
    with a caption. A grey row "no key yet? the study guide shows how to copy these into
    `outputs/`" points a viewer without a key to the staff's vectors.
  - S09 (17:50): the CORS heading was an elided command; it is now the captured curl, folded onto two
    rows that paste back as one.
  - S11 (20:32): the no-key traceback was readable for about 1.2 s; it now prints earlier and a 4-row
    strip keeps the whole error line. S11 (20:49): "Pause and run both." now ends its block, after
    what to look for (final 21:14.1).
  - S14 (26:46): the 429-retry warning moved onto the ▶ card for the whole pause.
  - S16 (30:32): "Answers: exercises.md" named a file outside the viewer's clone; the card now reads
    "Answers: study guide §8 (exercises.md)", as in L03 (final frame 31:00, `sheets/sheet_39.png`).
- **Facts (3):** S09 said Chroma allows "that one site", but `docker-compose.yml:26` lists two
  origins; it now says "Chroma's settings let the course's site in." (final 18:00.3). S02 said "RAG
  in five boxes" over four; now "four boxes" (final 01:40.2). S14 showed chunk lengths (1,326 and
  742 characters) that came from our illustration; the numbers are gone and the bars, labelled "our
  illustration", now differ about 22×, as "very uneven" says.
- **Picture and text (5):** S03's erratum tag sat beside the role a viewer must keep (now on Storage
  Admin, with a GREEN "needed" tick on the other role); S08's PERMISSION_DENIED card pointed to a
  role "in docker-shell.sh" (now "or the role in IAM (console)"); S16's "Linux: sudo rm -rf
  docker-volumes" chip, reported twice, now reads "only to delete the index later (Linux,
  root-owned): sudo rm -rf docker-volumes" (final frame 29:21, `sheets/sheet_37.png`); S12's fix card
  holds about 4.3 s and names the `*** START OF` / `*** END OF` lines.
- **Sync (3):** S09's highlight on the 60 MB SQLite file (two shoulds and a nit) used to start on
  "file" and now starts on "60"; S08's "24 rows" and lengths highlights now start on their words.
- **Shared code (6):** the tracker caption scrambled its letters at every `· extra` change and step
  change (reported four times), and `ComposeView.fit_top()` let S16's labels touch their box edges
  (twice). Both were fixed in the second finishing pass and re-verified in the final cut (tag check,
  item 11 under "Final-cut checks"; again on the re-stitched cut, "Re-check"). Fix round 2 then made
  the caption's step changes sequential (old out, a short gap, new in), checked frame by frame on
  the round-2 cut ("Re-check of the round-2 cut").
- **Subtitles (12 of 13; the 13th is the open should below):** eight Chinese line breaks inside a
  term or phrase (SQLite 文件, outputs 目录, 256 个 // embedding 值, 10 个 // chunk, 她祖父, chat 命令,
  该怎么表现 and the input-prompt phrase), the zh-only track splitting S08's step-1 command across two
  cues, S03's "第 2 步 / Step 2:" glued to the previous cue, and S04's pairing one clause off (all
  eleven from the subtitle watcher); and S11's four scores, 4 s late in the English track, now their
  own sentence. The final pairing check read all 510 bilingual cues and found none of these again.
  The eight line breaks and the split command were in the zh-only track, which no final check read
  cue by cue; for this record the final `.zh.srt` was searched: six of the terms (and the three nit
  terms 最相关, 原生返回, 两边各一个) sit on one line, the other two phrases were reworded (cues 318
  and 337 break at a comma), and cue 187 holds the whole step-1 command (`verifier/zh_cues.txt`).
- **Lexicon (1):** "lecture 4's" (above, gate 4).

**The open should.** Draft 19:38 (ASR, shared): inside a sentence, English cue boundaries are placed
by display characters (`explainer/build.py` `split_cues` for the `.srt`, `explainer/subtitles.py`
`tracks` for the Chinese and bilingual tracks), and spoken numerals take far longer than their
characters. The episode split the worst number sentences (S08, S11, S12) so voice marks start their
cues; the splitter itself is unchanged (toolkit PR). The first final cut's ASR still found four
continuation cues about 1 s early; fix round 1 split those sentences too (T1–T4), and the re-stitched
cut has none more than 1.0 s early ("Fixed", item 9).

**The nits: 27 of 30 fixed before the final cut (one by a scene workaround), three open then.**
Examples of the fixes: S02's
rule card no longer says "256 numbers" before S08 explains them; S04's tag no longer shows a scene
number ("· S09" → "· Load, step 3"); S05's three version chips name their sources; S09's erratum tag
no longer turns into a red blob; S10 and S12 mark the cut `--get` row with a grey "…"; S13's last
cards hold 1 s longer; S15's underlines clear the next row and its closing row shows three chips for
"three more"; S16's Q1 picture no longer lights the shared embedding box and database at "share"
(the flag chips stay on their lanes, as SHOW asks; final 30:36) and its ticks sit beside the chips;
S16's WARN lines are word-folded (final frame 28:57); the S09/S10 repeat "asks it questions" became "Part 2 puts it to work."
(final 18:13.8); "a few cents" and "handed to the chunker" (gate 4). The three that were open, all
in shared code:
- **Terminal scroll over the title bar** (`Terminal._make_room`, `explainer/devops.py`; draft 16:53
  and 12:17). S07 now fades its rows in place; the final visual pass still caught it twice. Fixed in
  the episode by fix round 1 ("Fixed", item 15); the toolkit is unchanged.
- **`_split_like` cuts the S08 step-1 command between two bilingual cues** (draft 14:01). Worked
  around in the episode by T3 ("Fixed", item 12); `_split_like` is unchanged.
- **A tag pinned beside a terminal row is taller than the row pitch** (`devops.tag()` 0.465 against
  0.403). The final tag check found S11's cost tag 1–2 px above the next row's ascenders; still so in
  the re-stitched cut ("Still open", item 7).

**Process.**
- **Fixers and verifiers:** one fixer per scene for S02–S16, one
  narration/subtitle fixer for script.md, `i18n/zh/narration/g1.yaml` and `g2.yaml` and the
  glossary, and a skeptical verifier per scene on fresh 720p frames and `explainer.check`.
- **Verifier corrections:** S02 and S11 docstrings brought in line; S05's "tag 1.5.9" chip text
  lowered 3 px onto the other chips' baseline; S07's scroll over the title bar fixed in the scene
  with `t.clear`; S08's ponder card and chip note and the personality-game caption added (the
  narration fixer had changed only the SAY lines); S14's caption reworded to "seven of one book's
  chunks · bar length = characters" and its tip card given the "run it again" row.

### Finishing passes

- **Before the draft (`we2lzv8iu`, output dated 2026-10-19 01:12 UTC).**
  - Critiques of S12–S16, each checked by a verifier on 720p frames: beats re-timed to their words
    in S12 and S14 (the S12 verifier re-fixed five anchors that fired 0.6–2 s off), S14's strip keeps
    its TEAL frame, S12's `#` marks pulse in place.
  - The `QA_FOLLOWUPS.md` items for S03, S04, S08, S09 and S11 (fixer and verifier each): S08's
    error row and S09's leftover char-split output were real and fixed with `t.clear`; the others
    did not reproduce. A `beside()` audit found no tag over text.
  - Chinese proofread: clause order brought in line with the English where it crossed a cue
    boundary (four places), cue-split wording, glossary sync, and `i18n/zh/README.md`.
- **After the QA (`w6tfmzqr5`, ending 22:20 UTC, commit `8f71867`).**
  - **Shared `common.py` (one owner, then a verifier on fresh 720p frames):** the tracker caption
    cross-fades in place (`CrossFadeTracker`, `_swap_caption`), with no fly-in from a blank caption;
    `ComposeView.fit_top()` squeezes shapes in height only and re-lays out labels and chips inside
    their boxes (the verifier widened two pads to 0.1); `RagMap.pulse_lane()` flashes only along the
    arrows (`_LaneFlash`). The commit also lists `lref()` reading a single lettered slide as "slide";
    the final tag check confirms all five single-slide tags.
  - **Text (18 items, all applied):** the S08 and S12 number sentences, "a few cents", "Part 2 puts
    it to work.", "handed to the chunker", "…put the others back and run it again", and S16's new
    sentence "Our chat opens the book for every question, and checks nothing." (final 30:10.6), plus
    SHOW/PONDER/BRIEF/README syncs in eleven scenes. `explainer.i18n check` printed OK.
  - **Scenes (7, each with a verifier):** S08 and S12 anchors on the new sentence starts; S09's
    `/data` flash on the label only; S10's anchor and "part 2" pill flash (the verifier made the pill
    readable at its peak); S12's grey "…" after the cut ids row; S13's B78 tag and "a grounding test
    · the lecture's IsSUP check, done by eye"; S15's red "invented details" held 1.57 s instead of
    0.5 s; S16's B68–B76 tag and the "our chat: every question" / "our chat: no check" notes on the
    Self-RAG diagram.
  - **Skipped, with reasons (plan `skipped`):** the optional spoken 429 clause; S08's early cue
    "a prefix the model is trained…" (left to the toolkit; fixed later by T1, "Fixed", item 9); the
    shared `beside()`/`_make_room`/`_split_like`/spoken-length items (toolkit, own PR); S06's seam
    copies crossing the 8-row strip (fixed in fix round 1b), S03's re-flowed `ls` (needs a 65-column
    capture), S16's "your edit" box 0.9 s after its anchor (fixed in fix round 1), and S11's repeated
    English line (intended `en_display`; fixed by P2).

## Final-cut checks of the first final cut (31:07.4, 1080p60, 2026-10-20)

Five agent checks of the first final cut's stitched deliverables. No human watched or listened. Times
in this section are of that cut.

**Lecture-slide tags and review-bot items** (`report-tags.md`; evidence in `tags/`, `bugbot/`).
- **Method:** each tag's fade times from the scene code and `events.json`, converted with the
  summed frame counts of the 16 stitch segments (112,041 frames, matching the file); four frames
  per tag with full-resolution crops; and an overlap scan decoding every tag's full-on span at
  30 fps (about 15,000 frames) against the span's median frame (`tags/overlap_scan.json`).
- **All 30 tags** read "slide" or "slides" correctly (A11, A16, A39, B78 and A63 read "slide"), are
  gone before their scene ends (every tagged scene's last frame is empty background), and nothing
  overlaps any of them (minimum presence 0.999). The closest neighbours are S08's podium header,
  10 px under T13/T14, and the scripted pulse and caption of T04.
- **Cited picture on screen:** yes for 27 spans; T04 demonstrates the tag itself (the how-to-follow
  beat, no slide picture by design); T02 and T08 were items 2 and 3 (both fixed since).
- **New defect then:** eight tag swaps double-exposed for 0.4–1.3 s (item 1, fixed since). S02's
  sequential swap at 01:57.2 is clean.
- **The 11 review-bot items, verified on frames:** S03's extra tag sits on the "Docker version
  29.8.2" output row (03:20.3–03:34.0); S04's box frames exactly `112.26MB` (06:44.6–06:55.4); S08's
  error rows leave before the second `--embed` (14:48.1–15:02.2); S09's recursive load starts in a
  cleared terminal (17:11.4); S11's cost tag covers no text (but see "Still open", item 7); S11's
  strip is cleared (20:58.8–21:17.0); S13's tracker captions fade, its chat window morphs as one
  chrome (25:14.2–25:16.2) and only "line 372" turns yellow (25:25.2); S14's shrunk strip stays TEAL
  (26:47.7–27:08.3); and the shared fixes hold: tracker changes cross-fade with no scrambled letters
  and no fly-in (S06, S09, S10, S12, S14, S16; largest single-frame share 0.28), S16's compose view
  keeps every label inside its box (`docker-volumes/` about 16 px inside the laptop box), and the
  pink lane pulse never crosses the prompt card (19:35.2–19:36.2, 30:35.9). All were re-checked on
  the re-stitched cut ("Re-check").
- **Side finding:** S16's section switch to "Agents (L06)" overlaps old and new tracker headers for
  about 0.25 s (29:57.1–29:57.3; item 8, fixed in round 2).

**ASR round trip, the substitute for a listen** (`report-asr.md`; `asr.json`,
`asr_words_base.en.json`, `vad.json`, `residual.json`, `lag.json`, `clips_turbo*.json`,
`onset_energy.json`, `clips/`).
- **Files:** the clean cut against `.srt` (byte-identical to `f466f8e`); the zh-en copy has the same
  audio packets (MD5 `1083284a56edd28d31acb19ec833801e`, `audio_md5.txt`), so the result covered the
  Bilibili asset of that cut.
- **Passes:** base.en twice over the whole mix (4,415 words both times), silero VAD,
  a whole-video word alignment that cancels boundary and formatting differences, and 47 doubtful
  windows re-run with large-v3-turbo.
- **Numbers:** 513 cues compared; 188 differed per cue, 111 of them only by word boundaries or
  formatting; 120 word-level differences remained after alignment (29 number splits, 23 spoken `--`
  or `/` forms, 68 examined one by one in 65 cues: all recogniser noise).
- **Real mispronunciations or swallowed words: none.** Words the full pass lost (cues 202 at
  12:19.8 and 270 at 16:32.5) were heard verbatim on the clip by both models; the 21 doubled words
  had confidence 0.00–0.39 and vanished on re-runs; base.en mishearings (README → "raid me", pipenv →
  "pip and", git → "get" at 11:04, Querying → "Quirrying") were heard correctly by turbo. "Tolminc"
  is heard as "Tolman's" or "tollments" in all 7 places (cues 2, 3, 357, 362, 415, 489, 509;
  `residual.json`; the report says 8), which matches the lexicon respelling; the
  recogniser does not know the name.
- **Left for a human ear (low):** connected speech both models hear the same way while the command
  is on screen: "in" heard as "and" (cues 157 at 09:01, 185 at 11:04, 286 at 17:32, 311 at 18:57),
  "an extra" as "in extra" (448, 27:15), "onto" as "on a" (103, 05:47), "compose down" as "composed
  down" (304, 18:35), "call" as "calls" (396, 24:06).
- **Sync:** 399 cues start after a pause; speech starts a median 0.20 s after the cue, at most
  0.64 s (cue 359). The 114 cues that continue a sentence lag a median 0.33 s (90th percentile
  0.70 s); four of them appeared 1.0–1.6 s before their audio (item 9, fixed since).

**Visual pass over the burned-in copy** (`report-visual.md`; `sheets/`, `visual_pass/`).
- **Method:** 39 contact sheets, 623 frames (every 180th frame of the 60 fps file, one every 3 s),
  all read, with each label the frame's own time (checked to 0.1 s); motion and still runs on the
  clean cut; an edge scan; structure and font-metric width estimates of all 510 cues from the
  burned `.ass`; spot checks at 23 times with a command on screen.
- **Passed:** no black or missing scene; every scene boundary has 0.3–1.1 s of empty background;
  content reaches the outer 30 px only as S01's bookshelf slides in and out (00:12.6, 00:30.4);
  no tag stuck on screen and no garbled text at rest; the clean and burned pictures match when
  scaled the same way (4 times).
- **Short morphs judged by design:** 05:52, 06:01, 08:13.3, 17:40.5, 26:01.5 and 28:08.4. Fix round
  2 replaced two of them:
  - 08:13.3, S05's `docker-volumes/chromadb/` row (item 23, fixed);
  - 28:08.4, S15's rank-fusion cells, which now flash in place while their blocks fade in.

  So 05:52, 06:01, 17:40.5 and 26:01.5 are still on the list. The sweep counted 17:40.5 as
  replaced, but this report's morph there is "S09 collections shrinking into Chroma at
  17:40.5–17:41.2" (`report-visual.md`), and round 2 changed only the swap just before it (old
  terminal out, then the two collections in, now sequential at 17:40.15–17:40.65 in the round-2
  cut, 0.016 s later than first-cut time). The shrink is unchanged: in the round-2 cut the shrinking "char-split-collection" and "recursive-split-collection"
  labels pass over the fading-in `/data` chip and the start of "docker-volumes/chromadb/" for about
  0.2 s (17:40.97–17:41.17; adversarial check, `recheck2/adv/sheets/S09_1741.png`,
  `S09_1741_zoom.png`), the same kind of moment as items 28 and 29. The round-2 checks are in
  "Re-check of the round-2 cut".
- **Still stretches:** none over 4.8 s outside the ponder timers: 09:04.2–09:08.2 (S05's pause) and
  25:25.0–25:29.7 (S13's end card); at looser tolerances also 03:41.9–03:45.9, 23:26.5–23:30.9
  (S12's end) and 10:31.4–10:35.6 (`visual_pass/still_runs.json`).
- **Burned subtitles:** all passed (Chinese glyphs y 992–1029, English y 1039–1062; at 23
  command-on-screen frames the picture's lowest content was at y 882 or above); "▶ your turn" chips
  sit 2–3 px above the next terminal line at 10:42 and 11:57 without touching
  (`visual_pass/frames/zoom4x_0717.00_yourturn_chip.png`).
- **Findings:** one new defect and two cosmetic ones (items 15–17, fixed since).

**Bilingual pairing** (`report-pairs.md`; `pairs/`).
- **Scope:** all 510 cues of `.zh-en.srt` read zh against en, a token check of Latin words and
  numbers, every cue with a condition or time word listed, and burned frames of every flagged cue
  (`pairs/frames/sheet_flagged.png`).
- **Headline:** the known failure did not occur: no condition or time clause is first in Chinese and
  last in English across a cue boundary, so no two neighbouring cues swap meaning.
- **Verified:** one Chinese line and one English line in all 510 cues; the burned `.ass` files use
  WrapStyle 2 with exactly one `\N` per Dialogue line (510, 294 and 216), so no break falls inside a
  command, path or flag; numbering continuous, no overlaps, every cue at least 1.0 s; part 1 + part 2
  text identical to the full file.
- **Found:** 1 medium, 2 low and 2 nits (items 10–14, all fixed since). By design: cue 459 keeps the
  Chester sentence in English on both lines.
- **For information (soft subtitles only):** the single-language `.srt` and `.zh.srt` break
  `python cli.py --X --chunk_type char-split` across two lines at the flag boundary (`.srt` cues 174,
  230, 272, 339 at 10:24.7, 14:09.0, 16:41.7, 20:33.0; `.zh.srt` 139, 187, 221, 276), the least bad
  place for a command longer than one line. The burned asset is not affected. In the re-stitched cut
  the `.srt` still breaks these commands at the flag boundary (cues 175, 231, 273, 340 at 10:25.0,
  14:08.8, 16:41.7, 20:33.0); the `.zh.srt` now breaks three of them after the step label (cues 139,
  187, 277) and one at the comma (222).

**Measured** (`report-measured.md`; `measured.json`, logs and scripts in `measured_v2/`). Its
numbers were replaced by the later re-checks' (now "Verified (round-2 cut)"); its findings were
items 18–22.

## Re-check of the re-stitched cut (1080p60, 2026-10-20)

Three agent checks of the re-stitched deliverables, and a frame check of the review-bot items for
this update. Evidence under `build/recheck/`. No human watched or listened. Times are of the
re-stitched cut.

**What changed.** Fix rounds 1 and 1b changed 12 scenes and `scenes/common.py`:

| scene | fix |
|---|---|
| S01 `Hook` | inline tag swap A6–A7 → A8–A10 sequential; A8–A10 kept through road 3 (T02) |
| S04 `TwoContainers` | T4 narration: "Its context was 112 megabytes." its own sentence; zh P4 |
| S05 `NamesAndMounts` | terminal scroll ghost: leaving rows fade in place |
| S06 `CharSplit` | A19–A22 leaves at the end of beat 0 (T08); B14–B15 after the `wc` output clears (T09); seam rows fade in place instead of flying; visualizer bars fade in with their window |
| S08 `Embeddings` | T1 and T3 narration; both tag swaps sequential |
| S10 `IndexSurvives` | outline flashes keep `/data` and `:8000` readable; grey note clear of the build chip; "?" badge on its words; zh P1 |
| S11 `NearestNeighbours` | tag swap sequential; zh P2 |
| S12 `FiltersFirst` | T2 narration; underline clear of line 357's box; ids flash in place instead of flying |
| S13 `FinalPrompt` | tag swap sequential |
| S14 `SemanticSplit` | terminal scroll ghost; zh P2 |
| S15 `BeyondNaive` | three tag swaps sequential |
| S16 `Recap` | recap questions dim without words crossing; "your edit" box on its words |
| all 16 | `common.py`: `lref_swap` sequential (S08, S11, S13) and `Terminal._make_room` rebound for L05 (every terminal scroll); all 16 re-rendered at 1080p60 |

The P2 cue of S06 and the P5 cue of S07 changed in the subtitle text only (`i18n/zh/narration/`).

**Scene starts** (`recheck/scene_starts_old_vs_new.json`, `recheck/chapters_git_diff_1173d22.txt`):
S01–S04 unchanged; S05–S08 +0.316/+0.317 s (S04 0.317 s longer); S09–S12 +0.016/+0.017 s (S08
0.300 s shorter); S13–S16 −0.116/−0.117 s (S12 0.133 s shorter). `chapters.txt` is unchanged at
second resolution; in `chapters_part2.txt` "Chat" moved from 05:22 to 05:21 (S13 at 321.900 s into
part 2, against 322.034 s before).

**Changed scenes on frames** (scenes check; `recheck/notes.txt`, `recheck/strips/`, single frames in
`recheck/frames/<scene>/`).
- **Method:** frames extracted from the clean cut at every fixed moment and read; 50 contact sheets
  of the bilingual copy for the 12 changed scenes, one frame every 2 s with full-video labels, all
  read (`recheck/sheets/<scene>_<stem>_zh-en_NN.png`); 26 of the cut's 31 terminal scrolls
  (`recheck/scrolls_all.json`, sheets `recheck/strips/ALL_scrolls_1.png` to `_5.png`); a pixel check
  of the burned subtitles over all 16 scenes (`recheck/subcheck/`).
- **Terminal scrolls:** the cut has 31 (S04 2, S05 16, S09 3, S10 2, S14 2, S16 6): every 0.35 s
  play of a `FadeOut` of the top rows with a shift of the rest in the 16 `events.json` files.
  `scrolls_all.json` missed five (S05 7:44.90 and 8:33.75, S09 17:02.62, S16 28:57.20 and 28:58.75);
  the adversarial check pulled frames across those five (`recheck/adv/scrolls_missed_full.png`,
  `scroll_S09_17m02.png`).
- **Result:** all 12 changed scenes pass; every fix-round item checks out (each is under "Fixed"
  below with its times and evidence). All 31 scrolls are clean. Every changed scene's last frame is
  uniform background (S01 1:40.16, S04 7:19.81, S05 9:09.56, S06 11:21.6, S08 15:56.25, S10 19:34.45,
  S11 21:27.2, S12 23:31.77, S13 25:30.62, S14 27:23.38, S15 28:49.53, S16 31:07.20).
- **The new sentences on the picture:** S04's yellow box draws on `112.26MB` at 6:44.02–6:44.52, on
  the new cue "Its context was 112 megabytes." (6:44.025); the build-context bar draws on "Most of it
  is git history," (cue 6:47.183; bar 6:47.17–6:47.67, ".git · 103 MB" 6:47.67–6:48.17) and "an old
  database copy" joins it on "which still holds an old copy…" (cue 6:48.805; label 6:48.92–6:49.52;
  `recheck/strips/S04_T4_its_context.png`, `recheck/adv/D3_S04_bar.png`). S08's "256"
  highlight comes on "The code asks for the first 256." (13:46.863) and the "first Google call · your
  project pays" chip fades in at 14:14.78, after "It's the first call to Google." (14:14.463;
  `recheck/strips/S08_T1_256_and_trained.png`, `S08_T3_first_call.png`). S12's counts land on their
  words: the counter runs down from 21:59 and reads 1,355 by 22:00.0, inside "…the book filter keeps
  1,355." (`recheck/adv/D2_S12_counter.png`); the `$contains "Italian"` chip comes in at
  22:02.07–22:02.3 and "None" at 22:06.3 (`recheck/strips/S12_T2_counts.png`).
- **Tags in the changed scenes:** one tag at a time at every swap; A48–A53 leaves at 20:24.1; B78
  sits on the grounding-test picture 25:02.7–25:14.1 and fades with it at 25:14.1–25:14.6; B19–B33 on
  its pictures until about 26:09.5; the last
  S15 tag leaves at 28:37.2–28:38.2; the top-right item at 31:04 is the "next: agents · L06" chip,
  not a lecture tag. No subtitle sits over a tag or a command in any sheet.
- **One nit, not from this round:** in S11 the A48–A53 tag is fully in at 19:46.65, about 0.4 s
  before the A39 sphere picture finishes fading (19:46.53–19:47.03; "Still open", item 6).

**Subtitles** (`recheck/subtitle_changes_old_vs_new.txt`, `recheck/cue_onsets.json`,
`recheck/subs_compare.json`). The cue-level diff against `1173d22` matches T1–T4, P1, P2, P4 and P5;
cues outside the edited sentences only moved by their scene's offset. Each new sentence is its own
cue in `.srt`, `.zh.srt` and `.zh-en.srt`, and the cue after each number starts within 0.025–0.06 s
of its speech (onsets measured on each scene's narration audio, which lines up with the final mix to
within 0.045–0.05 s, `recheck/voice_vs_final_lag.json`):

| item | new cue | starts | speech onset | old cue |
|---|---|---|---|---|
| T4 | `.srt` 119 "Its context was 112 megabytes." / `.zh.srt` 93 / `.zh-en.srt` 118 | 6:44.025 | 6:44.05 | – |
| T4, next | `.srt` 120 "Most of it is git history," | 6:47.183 | 6:47.21 | 120 at 6:46.328 |
| T1 | `.srt` 225 "The code asks for the first 256." / 181 / 223 | 13:46.863 | 13:46.90 | – |
| T1, next | `.srt` 226 "The model is trained…" | 13:49.914 | 13:49.94 | 225 at 13:48.707 |
| T3 | `.srt` 232 "It's the first call to Google." / 188 / 231 | 14:14.463 | 14:14.51 | 231 at 14:13.916 |
| T2 | `.srt` 362 "The word Italian keeps 64." / 295 / 357 | 22:02.074 | 22:02.12 | 361 at 22:00.977 |

**Review-bot items, re-checked on frames for the update after fix rounds 1 and 1b** (`recheck/bot/summary.json`; their status in the round-2 cut is under "Verified"; the sheets
named below are in `recheck/bot/`; single frames from the clean cut, read by eye; sequences decode
every frame of a window and report how the change is spread). All 11 `QA_FOLLOWUPS.md` items are
**verified** in the re-stitched cut:
1. **S03, extra tag vs. the full-width `docker --version; docker compose version` row:** the `extra`
   pill sits at the right end of the "Docker version 29.8.2" output row, clear of the command row,
   at 3:20.5, 3:21.95, 3:27.0 and 3:33.8 (`B01_S03_extra_tag_sheet.png`).
2. **S04, build-size box:** it frames exactly `112.26MB`, with "context:" outside, from 6:44.3 and
   after the terminal shrinks (6:44.8, 6:55.7; `B02_S04_box_sheet.png`,
   `recheck/strips/S04_T4_its_context.png`).
3. **S08, error row before the second `--embed`:** the "if it fails" card and the "real run · no key"
   tag are gone by 14:48.6 and the error rows by 14:49.6; the recursive-split command types into an
   empty strip (14:49.6, 14:50.5) and no error row is back at 15:02.3
   (`B03_S08_error_rows_sheet.png`).
4. **S09, recursive load in a cleared terminal:** at 17:11.38 only the prompt and "pyt"; at 17:13.48
   recursive-split output only (`B04_S09_load2_sheet.png`).
5. **S11, long cost tag over the prompt:** it covers no text; the tag spans x 774–1763, y 262–326
   and the command row's ascenders start at y 328, the same 1–2 px as before (20:41.983;
   `B05_S11_costtag_sheet.png`, `B05_S11_costtag_zoom_sheet.png`, `B05_S11_costtag_measure.json`;
   "Still open", item 7).
6. **The `beside()` pattern (S03/S08/S11):** verified where it applies (items 1, 3 and 5); the 2 s
   sheets of the 12 changed scenes show no tag over text.
7. **S13, line 372 highlight:** at 25:25.05 only "line 372" is yellow; "your own question: cli.py",
   the dots and "no rebuild" stay grey (`B08_S13_morph_sheet.png`, last tile).
8. **S14, shrunk strip keeps its teal frame:** frame and title teal at 26:47.55, 26:48.05, 26:50.65,
   27:00.65 and 27:08.15, median RGB (97–107, 201–206, 174–182) (`B10_S14_strip_teal_sheet.png`,
   `B10_S14_strip_teal_measure.json`).
9. **S11, cleared strip leaves no typed command:** typing starts in a cleared strip at 20:58.78, the
   strip is gone by 21:01.28, the band is empty at 21:04.48 and the your-turn card has no leftover
   row at 21:14.78 and 21:16.98 (`B06_S11_strip_clear_sheet.png`).
10. **S13, tracker caption fades instead of popping:** at 24:29.6–24:30.6, 24:34.3–24:35.2 and
    25:14.5–25:15.7 the old caption fades out and the new one fades in, in place, with no scrambled
    letters; the change is spread over 16–32 frames, the largest single-frame share 0.134, 0.088 and
    0.052 (`B07_S13_tracker_a/b/c_seq_sheet.png`, `_seq.json`).
11. **S13, chat-window morph (High):** one window chrome at 25:13.9, 25:14.5, 25:15.0, 25:15.5 and
    25:16.1, morphing from "a chat with an LLM" to `ac215-llm-rag.dlops.io/chat`, no second window;
    the scene's last frame (25:30.62) is empty (`B08_S13_morph_sheet.png`,
    `recheck/strips/S13_tag2_and_last.png`).

The shared `common.py` items also hold, on samples: tracker step changes cross-fade in place in S10
(18:20.2–18:21.2) and S12 (21:27.7–21:28.7; 16 and 20 frames, largest share 0.129 and 0.128;
`B11_S10_tracker_seq_sheet.png`, `B11_S12_tracker_seq_sheet.png`); S16's compose view keeps every
label inside its box (28:52.384, `B11_S16_compose_sheet.png`); the pink lane pulse runs only along
the arrows in S11 (19:35.35–19:35.95) and S16 (30:35.65–30:36.0) (`B11_lane_pulse_sheet.png`). Not
re-checked then: the other tracker changes in S06, S09 and S14. S16's section switch was looked at by the
adversarial check: the double exposure was still there (item 8, fixed in round 2). Fix round 2 made
the step changes sequential instead of cross-faded; they were re-measured on the round-2 cut ("Re-check
of the round-2 cut").

**ASR round trip on the re-stitched cut** (ASR re-check; `recheck/asr-summary.json`, `recheck/asr.json`,
`recheck/asr_base.log`, `recheck/asr/`).
- **Files:** the clean cut against its `.srt` (= `5c0c800`); the zh-en copy has the same audio
  packets (MD5 `ad24cc8b82ce12d2bed3b27257ba5933`, `recheck/audio_md5.json`), so the result covers the
  Bilibili asset.
- **Passes:** the prescribed base.en pass in the foreground (6 min 05 s), a second base.en pass with
  word times plus silero VAD (the same 4,423 words), 36 short clips re-run with large-v3-turbo and
  base.en, and 18 timing clips with turbo.
- **The changed sentences, heard as written,** with no word swallowed or added: S04 (6:44–6:52),
  S08 (13:39–13:53 and 14:08–14:16; the second "--" of the step-1 command is not spoken, as
  scripted) and S12 (21:55–22:04). Two recogniser extras are noise: the full pass doubled "database"
  at 6:51.66 (confidence 0.21), which neither model hears on the clip, and base.en appended "We'll see
  you in the next video. Bye bye." to the silent tail of the S08 clip, which turbo and the full pass
  do not have.
- **Numbers:** 514 cues compared (previously 513); 192 differ per cue (188); 4,423 words recognised
  (4,415); 123 differences left after aligning the whole video (120): 28 number splits, 22 spoken
  forms of on-screen `--` or `/`, 73 others. The 47 that appear only in this run were each re-run on
  a short clip: all are recogniser noise, homophones or display forms. The largest: the full pass
  dropped cue 175 ("Step 2: python cli.py --chunk …", 10:25), which both models hear verbatim on
  the clip; doubled words at cues 158, 328, 419 and 492 (confidence 0.95–1.00) do not appear on the
  clips.
- **Real mispronunciations or swallowed words: none.**
- **Timing (presentation time, what players and the burned subtitles follow):** 147 cues start
  exactly where the previous one ends (151 before); their speech lags the cue by a median 0.26 s,
  90th percentile 0.60 s, at most 0.94 s (energy onset). None is more than 1.0 s early. Largest:
  cue 88 (+0.94 s), 262 (+0.92), 138 (+0.88), 97 (+0.88), 168 (+0.84), 320 (+0.80). Cues 88, 262,
  138 and 168 are on the first review's list (as 88, 261, 137 and 167, unchanged); 97 and 320 were
  not measured there (whisper's word time had hidden 97: turbo put "your" at +0.26 s, the energy
  onset is +0.88 s). By the first review's definition (speech present at the cue start: 107 cues, 114
  before), the base.en word lag of the 106 of them that also start where the previous cue ends is
  median 0.31 s, 90th percentile 0.62 s (0.33 and 0.70 before, over all 114). The S04
  split made one new continuation cue, 121 at 6:48.81 (+0.42 s). Cues shown after their speech
  started (the mirror case, already in the first cut): 368 at 22:20.5 by 0.68 s, 410 at 24:48.8 by
  0.58 s, 170 at 9:50.0 by 0.56 s. The 407 cues that start after a pause (399 before) lag a median
  0.09 s, at most 0.41 s.
- **Audio timing at the scene joins (not new):** read straight through, as the ASR does, the audio
  runs 1–21 ms per join behind the timestamps, 0.204 s by S16, because at each of the 15 joins an
  AAC packet's timestamp spans fewer samples than it decodes to; in that time base cue 262 reaches
  +1.03 s and cue 295 +1.04 s ("Still open", item 27).
- **Optional ear spot-check:** at 0:27.6, cue 9 "answer from this story" is heard as "from the
  story" by both models on the clip (the first cut's full pass heard "this"); S01's narration matches
  the first cut sample for sample.

**Measured** (measured check; `recheck/measured.json`, logs in `recheck/logs/`, scripts
`recheck/chain.sh`, `light.py`, `subs_compare.py`, `narration.py`, `assemble.py`). Its numbers were
replaced by re-check 2's under "Verified (round-2 cut)". Only the file sizes, video bitrates and
SHA-256 hashes differ.

**Seen in passing, outside this round's fix list** (items 23–26, all fixed in round 2), and by
design: short morphs at 18:50.05 (S10's folder group morphs into the top-right chip, over empty
space), 22:02.95 (S12's dot-count label) and 28:19.4 (S15's "rare words" note morphs into the
`$contains` chip) (`recheck/strips/S10_morph_18m49_to_tag.png`, `S12_italian_dots_label_22m03.png`).
This list also had 13:29.2, where S08's dot-product copies passed over "B 0.976" for about 0.2 s.
Fix round 2 replaced it: the cosine cards now flash in place and the dot-product cards fade in. The
round-2 frame check verified this at 13:28.95 (`recheck2/visual/strips/S08_medals_29.45.png`).

## Re-check of the round-2 cut (1080p60, 2026-10-20)

Two agent checks of the round-2 deliverables:
- **Frame check:** evidence in `recheck2/visual/`.
- **Measured check:** evidence in the rest of `build/recheck2/`.

No human watched or listened. Times are of the round-2 cut; they are the same as the re-stitched
cut's.

**What changed.** Fix round 2 (`c187f3b`) changed 12 scene files and `scenes/common.py`. Every scene
imports `common.py`, so all 16 were re-rendered. S02, S06, S11 and S16 changed only through
`common.py`.

| scene | fix (time of the change) |
|---|---|
| all 16 (`common.py`) | `switch_section()` is sequential: the old header lifts out in the first half of the same run time and the new one drops in during the second (S03 3:46.4 and 4:46.4, S16 29:56.75; item 8). `_swap_caption`: at a step change the old caption fades out, then the new one fades in after a short gap. They used to overlap for about 0.25 s. The steady " · extra" swaps are unchanged. |
| S01 `Hook` | the README label leaves before the tracker fades in (01:10.4) |
| S03 `KeyAndProject` | console page changes are sequential (03:49.4, 03:52.4, 03:58.5); the key-file rename fades in place (04:02.2); the "your Project ID · not the name" tag flashes its outline (05:03.5) |
| S04 `TwoContainers` | the swap from the CORS strip to the Dockerfile pair is sequential (06:09.2) |
| S05 `NamesAndMounts` | item 23: four copy flights (07:52.9, 08:02.3, 08:13.3, 08:41.0) flash in place and fade in at their destination |
| S07 `RecursiveSplit` | the 14,228 count flashes in place and fades in by the bar (11:59.4); the lecture tag comes in after the chunk_overlap chips leave (12:46.1) |
| S08 `Embeddings` | the "instructor" header no longer slides through its column (13:20.6); the cosine cards flash in place and the dot-product cards fade in (13:28.9); card "B 81.2" flashes its outline (13:32.3) |
| S09 `LoadChroma` | chip and panel swaps are sequential (16:24.8, 16:28.8, 17:29.2, 17:40.1) |
| S10 `IndexSurvives` | item 24: the `secrets/` row fades out in place before V2's shrink (18:17.45–18:17.75); the rows' grey time tags no longer fill yellow (18:47.6, 18:48.3); terminal swaps are sequential (19:18.0, 19:24.4) |
| S12 `FiltersFirst` | item 26: the boxes of lines 357 and 358 share one edge and both underlines are clear (21:38.6); the "metadata filter" box (22:42.0), the "erratum" tag (22:56.4) and ids -0/-1/-2 (23:21.2) flash their outlines instead of filling |
| S13 `FinalPrompt` | the swap from the prompt stack to the code panel is sequential (23:43.1); the "needs Python 3.12" tag leaves before the new code row (23:54.7) |
| S14 `SemanticSplit` | item 25: the "▶ your turn" chip flashes its outline and pulses its text (27:18.25–27:18.95) |
| S15 `BeyondNaive` | the morph from the pipeline to the strip no longer reads "①ndexing" (27:38.5); the question copies no longer double over their own text (27:43.8, 27:48.5); the rank-fusion cells flash in place and their blocks fade in (28:08.0, 28:10.0); the "What is cheese?" copy no longer crosses the lecture tag (28:31.4) |

**Scene starts, chapters and subtitles** (`recheck2/measured.json`, `recheck2/committed_vs_output.json`).
- **Timing:** the 16 stitched segments have the same lengths and frame counts as before, and they add
  up to the old starts exactly (S05 7:19.833, S10 18:09.900, S16 28:49.567). No fix moved a scene
  start or a narration block; inside S10, V2's shrink now starts 0.3 s later (item 24).
- **Tracked output files:** all 16 tracked files in `output/` are byte-identical to `983e36e`,
  `c187f3b` and `5c0c800`. They are the three chapter files, the subtitles, the `.ass` files and the
  transcript. `git diff 983e36e -- videos/ac215-l05-rag/output` is empty.
- **Confirmed: no narration or subtitle text changed in fix round 2.** The script matches the rendered
  sidecars: 140 SAY lines, 4,339 words, 1719.488 s voiced.

**Changed moments on frames** (frame check; `recheck2/visual/findings.json`; strips in
`recheck2/visual/strips/`, single frames in `recheck2/visual/frames/S*/`).
- **Method:**
  - frames from the clean cut across every changed moment, read by eye;
  - 55 contact sheets of the burned copy, one frame every 2 s over all 16 scenes, all read
    (`recheck2/visual/sheets/`);
  - every tracker step change and section switch, decoded frame by frame;
  - the 16 last frames;
  - the subtitle band (gate 6).
- **Tracker step changes:** the check covered all 15 that the 16 `events.json` files list
  (`recheck2/visual/tracker_changes.json`: S03 ×7, S06, S08, S09 ×2, S11, S13 ×3). No frame shows
  both captions above 8 % of their ink (`recheck2/visual/tracker_steps_metric.json`; strips
  `series_S*_step_*.png`). The adversarial check decoded all 15 again with its own masks and found
  the same: no frame above 8 % for both, the largest overlap 5.5 % (`recheck2/adv/trk/step_*.json`
  and `.png`).
  - **13 of them:** 3–13 empty frames separate the old caption from the new (at that metric's ink
    threshold; the count moves by a few frames with the threshold).
  - **S13 24:29.78:** starts from a blank caption.
  - **S13 25:14.6:** this step runs through S13's own `tracker_to`, which also fades a copy of the old
    caption over the first half. About 5 % of the old caption is left for one or two frames as the
    new one starts.
  - **By design:** the steady " · extra" swaps (same step) still overlap, so the shared "step k of
    N: …" never dims (for example 10:42.617).
- **Section switches (item 8):** never two headers at once.

  | switch | old header's ink until | empty | new header from |
  |---|---|---|---|
  | S03 3:46.367 | 3:46.630 | 3:46.664–3:46.897 | 3:46.914 |
  | S03 4:46.417 | 4:46.680 | 4:46.714–4:46.947 | 4:46.964 |
  | S16 29:56.75 | 29:56.963 | 29:56.997–29:57.163 | 29:57.180 |

  Strips: `series_S03_switch1_Account.png`, `series_S03_switch2_Run.png`,
  `series_S16_switch_Agents.png`. The adversarial check decoded the three again and found the whole
  tracker area empty at 3:46.667–3:46.900, 4:46.717–4:46.950 and 29:57.000–29:57.150, within a frame
  of these times (`recheck2/adv/trk/switch_*.json`).
- **Last frames:** all 16 scene-end frames are empty, with a maximum brightness of 14–16 out of 255
  (`ALL_last_frames_boost4.png`).
- **Per scene:** every scene passes.

  | scene | times checked | what the frames show | strip(s) in `recheck2/visual/strips/` |
  |---|---|---|---|
  | S01 | 1:10.58 | The README label is fully out by 1:10.85 and the tracker fades in from 1:11.067. Tags A6–A7 → A8–A10 swap in sequence (0:42.3–0:43.1). | `S01_readme_to_tracker.png` |
  | S03 | 3:49.42, 3:52.47, 3:58.57, 4:02.18, 5:03.6 | The page changes run in sequence. The key name fades in place, without garbling. The "your Project ID · not the name" tag flashes its outline and pulses its text, and stays readable. | `S03_page_to_34.1.png`, `S03_page_to_37.15.png`, `S03_page_to_43.25.png`, `S03_key_rename_46.87.png`, `S03_yt_tag_108.3.png` |
  | S04 | 6:09.35 | The CORS strip leaves before the Dockerfile pair arrives. | `S04_panel_swap_53.78.png` |
  | S05 | 7:52.9, 8:02.33, 8:13.2, 8:41.05 | All four copies flash in place and fade in at their destination. No glyph crosses terminal rows or titles. | `S05_flight1_33.07.png`, `S05_flight2_42.5.png`, `S05_flight4_53.37.png`, `S05_flight3_81.22.png` |
  | S07 | 11:59.45, 12:46.18 | 14228 flashes in the terminal and fades in by the bar. B16–B19 comes in only after the chunk_overlap chips leave. | `S07_count_37.83.png`, `S07_lref_84.57.png` |
  | S08 | 13:20.58, 13:28.95, 13:32.3 | "instructor" moves only after its numbers leave. The cosine cards flash in place and the dot-product cards fade in. "B 81.2" stays readable. Tags A40–A43 and A44–A47 swap in sequence. | `S08_instructor_21.08.png`, `S08_medals_29.45.png`, `S08_cardB_32.8.png` |
  | S09 | 16:24.88, 16:28.88, 17:29.38, 17:40.23 | All four swaps run in sequence. The by-design shrink of the two collections into Chroma that follows (17:40.65–17:41.35) is unchanged; its labels pass over the fading-in `/data` chip at 17:40.97–17:41.17 (adversarial check, `recheck2/adv/sheets/S09_1741_zoom.png`). | `S09_chips_28.6.png`, `S09_stage_32.6.png`, `S09_chips_93.1.png`, `S09_picture_103.95.png` |
  | S10 | 18:17.45–18:18.75, 18:47.5, 18:48.2, 19:18.07, 19:24.5 | The `secrets/` row is gone before the shrink starts at 18:17.75. The grey time tags stay grey. The terminal swaps run in sequence. | `S10_secrets_shrink_7.55.png`, `S10_timetags_37.6.png`, `S10_term_swap_68.17.png`, `S10_term_swap_74.6.png` |
  | S12 | 21:31.8–21:38.9, 22:42.07, 22:56.55, 23:21.35 | Boxes 357 and 358 share one pink edge at y 542–545; before, there was a double line at 536–539 and 548–551. Both underlines clear the box edges by about 4 px. The filter box, the erratum tag and the ids flash their outlines. Tag A54–A55 spans the pipeline picture. | `S12_boxes_357_358.png`, `S12_boxes_zoom3x_edges_21m38.533.png`, `S12_boxes_old_vs_new_zoom3x.png`, `S12_filter_74.83.png`, `S12_erratum_89.32.png`, `S12_ids_114.12.png` |
  | S13 | 23:43.13, 23:54.7 | Both swaps run in sequence. | `S13_stack_to_code_11.33.png`, `S13_swap_panel_22.9.png` |
  | S14 | 27:18.25–27:18.95 | "▶ your turn" is readable on every frame. The outline stays about 6 px clear of the command row. | `S14_your_turn_107.6.png` |
  | S15 | 27:38.48, 27:43.83, 27:48.53, 28:08.1, 28:10.12, 28:31.57 | No frame reads "①ndexing". The question copies no longer double over their text. The rank cells flash in place and the blocks fade in. "What is cheese?" is clear of the lecture tag. The tag swaps run in sequence. | `S15_strip_morph_15.07.png`, `S15_clean_rewrite_20.42.png`, `S15_vague_rewrite_25.12.png`, `S15_rrf_44.68_46.7.png`, `S15_question_68.15.png` |
  | S16 | 29:56.75 | The section switch is as above. Tags B68–B76 and A63 span their pictures. | `series_S16_switch_Agents.png` |
  | S02, S06, S11 | contact sheets; S06 10:25.03, S11 20:58.20 | Only the tracker changed, and it is clean. | `series_S06_step_75.45.png`, `series_S11_step_83.72.png` |

- **New observations:** these were not on round 2's list, and the code at these moments did not
  change in round 2:
  - two text-over-text moments, S16 at 29:25.87–29:26.0 and S04 at about 06:25.8–06:26.1 (items 28
    and 29 under "Still open");
  - a nit at S03 05:03.97;
  - S10's labels crossing route lines at 18:18.2–18:18.5, which the S10 fixer recorded and which is
    still present (item 30);
  - added by the adversarial check of this record: in S09's by-design shrink of the collections into
    Chroma, their labels pass over the fading-in `/data` chip at 17:40.97–17:41.17 (by-design list
    under "Final-cut checks"; not a new item).

**Review-bot items:** none were assigned to this check. Their status is under "Verified".

**Measured** (measured check; `recheck2/measured.json`, logs in `recheck2/logs/`, scripts
`recheck2/chain.sh`, `light.py`, `narration.py`, `assemble.py`). Its numbers are under "Verified
(round-2 cut)". It compared 177 figures with the previous version of that section: 20 changed (the
four files' sizes, video bitrates and SHA-256 hashes) and 157 are the same.

## Open and fixed items

Fix rounds 1 and 1b closed items 1–4 and 9–17 and every smaller nit except S09's (plus S06's
visualizer bars, noticed during fix round 1); the `publish:` block closed item 19; item 18 was done
before. Fix round 2 closed items 8 and 23–26. Its sweep fixed the real candidates in 10 scene files
(the sweeper's 26 fixes and one more by its verifier) and the tracker's step changes. Three moments
this record had called by design were replaced too: 08:13.3 (by the S05 verifier), and 13:29.2 and
28:08.4 (by the sweep). The sweep also listed 17:40.5 as replaced, but it changed only the swap
before that morph; the morph itself (S09's collections shrinking into Chroma) is unchanged and
stays by design ("Final-cut checks"). Each fixed item gives the times and evidence of the cut it was
checked on. "Not planned" says why an item was left.

### Fixed

Items 1–4 and 9–17 and the smaller nits were checked on the re-stitched cut. The round-2 cut
re-rendered every scene, and its subtitle files and audio are identical to the re-stitched cut's, so
items 9–14 hold as they were checked. The round-2 frame check saw these again on frames:
- the tag swaps of item 1 in S01, S08 and S15;
- the n_results=10 underline of item 16, clear of the box edges by about 4 px.

The other picture fixes appear only in its 2 s contact sheets, where nothing was found. Items 8 and
23–26 were checked on the round-2 cut.

**Lecture-slide tags**

1. **Tag swaps double-exposed** (first cut: `report-tags.md`; `tags/swaps/swaps_sheet.png`). Fix round
   1 made every swap sequential, old out then new in, in the same run time (`lref_swap` in
   `common.py` for S08, S11 and S13; inline in S01 and S15). In the re-stitched cut every swap shows
   one tag at a time, with an empty frame between:

   | swap | first cut | re-stitched cut | evidence (`recheck/strips/`) |
   |---|---|---|---|
   | S01 A6–A7 → A8–A10 | 00:42.3–00:43.1, garbled | 0:42.20–0:43.25 (empty at 0:42.70) | `S01_swap_A6-A7_to_A8-A10.png` |
   | S08 A24–A28 → A40–A43 | 13:13.1–13:13.6, doubled | 13:13.30–13:14.00 (empty 13:13.62) | `S08_swap1_A24-A28_to_A40-A43.png` |
   | S08 A40–A43 → A44–A47 | 13:28.1–13:28.6, doubled | 13:28.38–13:29.05 (empty 13:28.70) | `S08_swap2_A40-A43_to_A44-A47.png` |
   | S11 A39 → A48–A53 | 19:46.1–19:46.5, garbled | 19:46.05–19:46.65 (empty 19:46.33) | `S11_swap_A39_to_A48-A53.png` |
   | S13 A57–A59 → A61–A62 | 24:22.1–24:22.5, doubled | 24:21.9–24:22.55 (empty 24:22.20) | `S13_swap_A57-A59_to_A61-A62.png` |
   | S15 B6–B10 → B36–B39 | 27:38.6–27:39.9, garbled | 27:38.4–27:39.9 (empty 27:39.13) | `S15_swap1_B6-B10_to_B36-B39.png` |
   | S15 B36–B39 → B42–B48 | 27:51.9–27:53.1, doubled | 27:51.7–27:53.1 (empty 27:52.4) | `S15_swap2_B36-B39_to_B42-B48.png` |
   | S15 B42–B48 → B51–B65 | 28:21.1–28:22.3, doubled | 28:20.85–28:22.25 (empty 28:21.53) | `S15_swap3_B42-B48_to_B51-B65.png` |

2. **T02, S01: the A8–A10 tag left at "Or let a librarian" (first cut 00:49.7–00:50.3)**, before
   road 3 was drawn. Fix round 1 kept it on: A8–A10 is on from 0:49.6 through road 3, the librarian
   and "That's RAG" (0:56.3), fades with the whole picture at 0:56.67–0:57.27, the frame is empty at
   0:57.28 and A11 comes in at 0:57.9–0:58.7 (`recheck/strips/S01_T02_road3_span.png`).
3. **T08, S06: the A19–A22 tag stayed about 58 s past its beat** (first cut 09:09.3–10:25.4). It now
   leaves with beat 0's picture at 9:26.27–9:26.87 and is absent at 9:50.0, 10:07.6 (ponder),
   10:25.1–10:25.9 (the old fade-out, no flash-back) and 10:45.0
   (`recheck/strips/S06_T08_tag_leaves_beat0_and_bars.png`, `S06_T08_no_tag_later.png`).
4. **T09, S06: the B14–B15 tag landed 0.65 s before the `wc` output cleared** (first cut
   10:49.8–10:50.5). The output now fades out at 10:50.13–10:50.38 and the tag fades in at
   10:50.38–10:50.78 over the empty terminal; it stays through the seam and the lecture example and
   fades out with the picture at 11:05.13–11:05.63
   (`recheck/strips/S06_T09_tag_after_wc_clears.png`, `S06_tagB_lecture_example.png`,
   `S06_tagB_end.png`).

**Subtitles**

9. **Mid-sentence cue timing** (first cut: `report-asr.md` Finding 1). Four cues that continued a
   sentence after a number or long command appeared 1.0–1.6 s before their audio. Fix round 1 (T1–T4)
   gave the spoken numbers and the step-1 command their own sentences, so each of those cues is now a
   sentence start after a 0.32 s pause, started by a voice mark:

   | first cut `.srt` cue (lead, energy / VAD) | re-stitched `.srt` cue | starts | speech starts after the cue (VAD, presentation time) |
   |---|---|---|---|
   | 225 "a prefix the model is trained…" (+1.62 / +1.70 s) | 226 "The model is trained…" | 13:49.914 | +0.06 s |
   | 361 "the word Italian keeps 64." (+1.16 / +1.30 s) | 362 "The word Italian keeps 64." | 22:02.074 | +0.08 s |
   | 231 "the first call to Google." (+1.06 / +1.16 s) | 232 "It's the first call to Google." | 14:14.463 | +0.06 s |
   | 120 "mostly git history…" (+1.00 / +1.00 s) | 120 "Most of it is git history," | 6:47.183 | +0.04 s |

   No continuation cue is now more than 1.0 s early (largest +0.94 s, cue 88;
   `recheck/asr-summary.json` `lag`). Weighting the splitter by spoken length stays a toolkit change
   (`explainer/build.py` `split_cues`).
10. **Pairs F1 (medium): a verb separated from its command** (first cut `.zh-en.srt` 313/314). Fix
    round 1 (P1) reworded `g2.yaml`: `.zh-en.srt` 314 "先运行：docker compose build / run docker compose
    build first." (19:12.036–19:14.185) and `.zh.srt` 257 hold the verb and the command together; on
    the burned copy at 19:13.9 with the chip on screen (`recheck/notes.txt`, S10 sheets).
11. **Pairs F2 (low): the whole English sentence repeated under a Chinese sentence split in two**
    (first cut 174/175, 336/337, 435/436). Fix round 1 (P2) shortened the three Chinese sentences:
    `.zh-en.srt` 174 (10:25.033), 336 (20:32.966) and 434 (26:35.683) are single cues with the English
    shown once, `.zh.srt` 139, 277 and 359 are single cues, and a scan finds no repeated-English pair
    left (three before).
12. **Pairs F3 (low): the step-1 `--embed` command cut between its flags** (first cut 230/231). Fix
    round 1 (T3): `.zh-en.srt` 230 holds the whole command in both languages, "第 1 步：python cli.py
    --embed，用 char-split / Step 1: python cli.py --embed --chunk_type char-split." (14:08.767), and
    231 "这是首次调用 Google / It's the first call to Google." follows (14:14.463).
13. **Pairs F4 (nit): "finds none" and 没找到 one cue apart** (first cut 115/116). Fix round 1 (P4):
    `.zh-en.srt` 115 "Compose 在 Docker Hub 上没找到叫 llm-rag-cli 的 image / …finds none," (6:34.185)
    and `.zh.srt` 91 have both in the same cue.
14. **Pairs F5 (nit): "default" and 默认 one cue apart** (first cut 204/205). Fix round 1 (P5):
    `.zh-en.srt` 203 "这个切分器的库默认 / The splitter's library default" (12:24.771) and `.zh.srt`
    164 have them in the same cue.

**Picture**

15. **Visual F1: scrolled-off terminal lines crossed the title bar for 2–5 frames** (first cut 08:11.95
    in S05 and 26:41.17–26:42.0 in S14). Fix round 1 rebound `Terminal._make_room` for L05 in
    `scenes/common.py`: the leaving rows fade in place during the first 40 % of the 0.35 s, then the
    rest shift up; `explainer/devops.py` is unchanged (toolkit fix separately). All 31 terminal
    scrolls of the re-stitched cut are clean (26 in the re-check's sheets, the other five in
    `recheck/adv/scrolls_missed_full.png` and `scroll_S09_17m02.png`); at the old moments, S05's
    scroll at 8:12.05 (checked 8:11.98–8:12.70) and S14's at 26:40.85 and 26:41.65 leave nothing over
    the title bars (`recheck/strips/S05_scroll_ghost.png`, `S14_scroll_ghost.png`, `ALL_scrolls_1.png`
    to `_5.png`, `recheck/adv/E_scrolls_old_ghosts.png`).
16. **Visual F2: S12's yellow underline under `n_results=10` sat inside the top of line 357's pink
    box** (first cut 21:29.6–21:39.0). In the re-stitched cut, checked 21:29.6–21:38.6, the underline
    is at y 489–491 (antialiased 488–492) and the box's top edge at y 497–498 (antialiased 496–499),
    with three rows of background (493–495) between them, so they no longer touch
    (`recheck/strips/S12_underline_zoom3x_21m38.6.png`, `S12_underline_n_results.png`; pixel columns
    at 21:31.9 and 21:38.6 re-measured, `recheck/adv/F_S12_underline.png`).
17. **Visual F3: recap questions' words crossed as they dimmed** (first cut 30:43.4, 30:49.3,
    30:56.7). The dimmed copy now keeps the big question's line breaks: Q2 (30:43.15–30:43.85), Q3
    (30:49.05–30:49.75) and Q5 (30:56.4–30:57.1) shrink and grey in place with no word crossing a row
    (`recheck/strips/S16_Q2_dim.png`, `S16_Q3_dim.png`, `S16_Q5_dim.png`).

**Tracker section switch (fix round 2, checked on the round-2 cut)**

8. **Section switch double exposure** (first cut 29:57.1–29:57.3, "README › Run C…(L06)",
   `bugbot/tracker_s16c/tracker_s16c_montage.png`; re-stitched cut 29:56.95–29:57.2,
   `recheck/adv/J2_S16_switch.png`; S03 *preview* about 03:46.6 and 04:46.7).
   - **Fix:** fix round 2 made `switch_section()` in `common.py` sequential, like `lref_swap`. In the
     same run time, the old header lifts out in the first half and the new one drops in during the
     second, so no timing moved.
   - **Round-2 cut:** no frame shows two headers at any of the three switches.
     - S03 3:46.367: old ink until 3:46.630, empty 3:46.664–3:46.897, new from 3:46.914.
     - S03 4:46.417: old until 4:46.680, empty 4:46.714–4:46.947, new from 4:46.964.
     - S16 29:56.75: old until 29:56.963, empty 29:56.997–29:57.163, new from 29:57.180.
   - **Evidence:** `recheck2/visual/strips/series_S03_switch1_Account.png`,
     `series_S03_switch2_Run.png` and `series_S16_switch_Agents.png`. Before the re-render, the
     shared verifier checked the same on 720p60 renders (`fix2/shared/verify/`).

**Seen in the re-check, fixed in round 2 (checked on the round-2 cut)**

23. **S05 copy flights.** In the re-stitched cut three flights crossed terminal text: 7:52.9–7:53.6,
    8:02.33–8:03.23 and 8:41.05–8:41.85 (`recheck/strips/S05_getent_copy_flight_8m02.png`,
    `S05_other_copy_flights.png`).
    - **Fix:** each source now flashes in place while its copy fades in at its destination, as in
      S06 and S12.
    - **A fourth flight:** the S05 verifier found the `docker-volumes/chromadb/` row garbled over the
      CLI and Chroma boxes at about 8:13.3–8:14.2. It had been on the "by design" list as 08:13.3. The
      verifier replaced it the same way.
    - **Round-2 cut:** at 7:52.9, 8:02.33, 8:13.2 and 8:41.05 all four copies flash in place and fade
      in at their destination, and no glyph crosses terminal rows or titles.
    - **Evidence:** `recheck2/visual/strips/S05_flight1_33.07.png`, `S05_flight2_42.5.png`,
      `S05_flight4_53.37.png` and `S05_flight3_81.22.png`; previews in `fix2/S05/verify/`.
24. **S10 shrink morph.** The `secrets/` row slid through the folder labels at 18:17.9–18:18.3
    (`recheck/strips/S10_shrink_morph_18m17_18m18.png`).
    - **Fix:** the parts that have no compact twin now fade out in place over 18:17.45–18:17.75,
      before the 1.0 s shrink starts at 18:17.75. Those parts are the `/secrets` window, the
      `secrets/` row and its key, `.venv` and the secrets route.
    - **Round-2 cut:** checked at 18:17.45–18:18.75; the row is gone before anything moves.
    - **Evidence:** `recheck2/visual/strips/S10_secrets_shrink_7.55.png`.
    - **Still open:** the moving network and 8000:8000 labels crossing route lines (item 30).
25. **S14 your-turn chip.** At 27:18.6 the `Indicate` filled the chip yellow
    (`recheck/strips/S14_your_turn_indicate_27m18.png`).
    - **Fix:** the flash now thickens the outline and pulses the text at 1.08. The chip's dark fill
      no longer changes.
    - **Round-2 cut:** "▶ your turn" is readable on every frame of 27:18.25–27:18.95, and the outline
      stays about 6 px clear of the command row.
    - **Evidence:** `recheck2/visual/strips/S14_your_turn_107.6.png`.
26. **S12 line 357/358 boxes.** At 21:38.6 there was a double pink line between the rows, and the
    underline merged into 357's bottom edge (`recheck/adv/F2_S12_boxes_zoom2x_21m38.6.png`).
    - **Fix:** the two boxes now run from half-gap to half-gap and share one pink edge.
    - **Round-2 cut:** checked at 21:31.8–21:38.9. The shared edge is at y 542–545; before, there were
      edges at 536–539 and 548–551. The "The Complete Book of Cheese" underline and the n_results=10
      underline (item 16) each clear the box edges by about 4 px.
    - **Verifier correction:** the fix had moved 358's bottom edge onto the underscores of
      `where_document` and `search_string`. The S12 verifier moved it, leaving 3 px clear at 1080p
      (`fix2/S10+S12+S14/verify/S12/`).
    - **Evidence:** `recheck2/visual/strips/S12_boxes_357_358.png`,
      `S12_boxes_zoom3x_edges_21m38.533.png` and `S12_boxes_old_vs_new_zoom3x.png`.

**Release and format**

18. **Stale 480p15 drafts in `output/` (done: removed at 07:38 UTC).** When measured (06:59),
    `output/` also held `ac215-l05-rag_480p15.mp4` (30:42.8, 102.1 MB), `_480p15.zh-en.mp4`
    (67.9 MB), `_part1_480p15.mp4` (59.4 MB, one decode error: a repeated timestamp) and
    `_part2_480p15.mp4` (42.8 MB), dated 2026-10-19 01:27–01:31. `tools/release_episode.py`
    (lines 147–149) takes every `.mp4`, `.srt` and `.ass` in its outputs folder, so a release run on
    this checkout would have uploaded them; the release workflow renders and stitches in a fresh
    runner, where they do not exist. They are gone; `output/` now holds only the re-stitched
    deliverables (four MP4s, 12 subtitle files, three chapter files and the transcript), and the
    `build/qa/draft.mp4` link dangles.
19. **Release prerequisites (fixed: the `publish:` block was added after the first version of this
    record listed it as missing).** `video.yaml` has a `publish:` block (committed in `01dac58`) with
    `title_zh`, `description_zh` (601 characters), `tags_zh` (10 tags) and `tid: 231`, as the series
    skill requires. `python tools/release_episode.py videos/ac215-l05-rag --preflight`, which checks
    this record's sign-off line and the publish block, printed all 16 scenes and `latex=false`
    (`recheck/release_preflight.log`; run again on this version of the record,
    `recheck/release_preflight_review_update.log`, and after the adversarial check's corrections,
    `recheck/adv/release_preflight_after_verify.log`, and on this version after fix round 2,
    `recheck2/release_preflight_review_update.log`, and after its adversarial check's corrections,
    `recheck2/adv/release_preflight_after_adv.log`; exit 0 each time).

**Smaller nits, fixed** (from QA and finishing verifiers on previews; fix rounds 1 and 1b):
- **S06 seam copies** flew across the command rows (first cut 10:53.5): the source text now flashes
  purple in place and each row fades in above the terminal, 10:53.5–10:54.55 and 10:55.45–10:56.45
  (`recheck/strips/S06_seam_rowA.png`, `S06_seam_rowB.png`).
- **S06 visualizer bars** showed at full opacity while their window faded in (noticed by the fix
  round 1 verifier): they now fade in with the window (its `FadeIn` runs 9:26.87–9:27.57; frames
  9:27.05–9:28.1, `recheck/strips/S06_T08_tag_leaves_beat0_and_bars.png`).
- **S10 `Indicate` fills** hid `/data` (first cut 18:31.05–18:31.15) and `:8000` (18:33.65–18:33.75):
  at 18:31.15 only the Chroma box outline and title flash and `/data` stays readable; at 18:33.7 the
  `:8000` chip's outline and text flash pink on its dark fill, readable
  (`recheck/strips/S10_outline_flash_data.png`, `S10_chip_8000_flash.png`).
- **S10 grey note** touched the "docker compose build" chip (19:12.6): at the 19:12.62 pulse the chip
  keeps about 19 px from "or the Dockerfile:" (`recheck/strips/S10_grey_note_build_chip.png`).
- **S10 "?" badge** came 1.1 s after "does the index survive" (18:18.1): it fades in at
  18:16.90–18:17.45, and ASR puts "Does" at about 18:17.39 (`recheck/strips/S10_badge_on_does.png`).
- **S12 id copies** crossed the staff tag, the terminal title and the ids rows during the card
  flight (first cut 23:16.5): at 23:16.10–23:17.10 the ids flash in place and nothing crosses
  (`recheck/strips/S12_id_flash_no_flight.png`).
- **S16 "your edit" box** landed 0.9 s after "shows only your edit" (29:14.2): it draws at
  29:13.28–29:13.88, while ASR has "only" at about 29:13.43 and "edit" at about 29:14.09
  (`recheck/strips/S16_your_edit_box.png`).
- **Fix round 2's sweep of all 16 scenes** (checked on the round-2 cut). The sweep looked for copy
  flights over text, flashes that fill a label's own box, and double-exposed swaps. It found 52
  candidates, 29 of them real (table in `fix2/sweep/` and in the fix report).
  - Every fix is listed in "Re-check of the round-2 cut", with its round-2 time and strip, and
    passed there. That includes the tracker step changes from `common.py` (15 measured) and S15's
    "①ndexing" at 27:38.5, which the sweep's verifier found and fixed.
  - Before the re-render, the sweep's verifier checked the sweeper's 26 fixes frame by frame on fresh
    720p renders (`fix2/sweep/verify/`).

### Still open

**Lecture-slide tags**

5. **T12, S08 (minor): the picture fades out before the tag swaps**, so the swap runs on an empty
   stage (picture out 13:12.87–13:13.37; A24–A28 fading 13:13.30–13:13.62, A40–A43 in at
   13:13.75–13:14.00 as the personality-game picture starts). Not planned: under 1 s, and the swap
   is sequential now.
6. **T19, S11 (minor): the A48–A53 tag arrives before its score column**, over the fading A39 sphere
   (tag in 19:46.43–19:46.65, sphere out 19:46.53–19:47.03, similarity picture from 19:47.03). The
   swap is sequential now; the order predates fix round 1. Not planned: under 1 s; the cited picture
   follows.
7. **S11's cost tag sits 1–2 px above the ascenders of "chunk_type char-split"** and looks as if it
   touches them (20:37.1–20:49.4; tag x 774–1763, y 262–326; text from y 328 in the re-stitched cut,
   `recheck/bot/B05_S11_costtag_measure.json`). It covers no text. Same cause as QA's open nit:
   `devops.tag()` is taller than the terminal row pitch. Not planned: shared toolkit. Not looked at
   again in the round-2 cut (S11's code is unchanged; it was re-rendered for `common.py`).

**Release and format**

20. **Gate 3 shortfall:** five ponders against the aim of about 15.6. Not planned: it matches BRIEF.md
    and the series rule of 3–5; see gate 3, with its question for Conny.
21. **Narration over its budget:** 4,339 words against BRIEF.md's 3,900–4,300 (39 over; T1–T4 added
    four); part 1 has 2,534 against its plan of about 2,410 (5 % over). Not planned: the runtime,
    31:07, is inside 25–35 min.
22. **Burned copy's start (no visible effect):** the zh-en copy's video starts at 0.000 s, the clean
    cut's and the parts' at 0.021 s, and it has one more frame (112,035 against 112,034). Not
    planned: about one frame.

**Seen in the re-check of the re-stitched cut** (items 23–26 from that list are fixed; see "Fixed"):

27. **Audio timing at the scene joins (toolkit; no effect in players that follow timestamps):** at
    each of the 15 joins an AAC packet's timestamp spans fewer samples than the 1,024 it decodes to
    (16 short packets of 1–1,023 samples, two of them at the S04/S05 join), so a player or tool that
    plays every decoded sample without re-syncing runs 1–21 ms per join behind the picture, 0.204 s
    by S16 (`recheck/asr/audio_packets.csv`, `recheck/asr/audio_shift.json`; packet list re-read
    with ffprobe, `recheck/adv/audio_packets_clean.csv`). The first cut has the same drift. It looks
    consistent with `explainer/build.py` joining the per-scene files with `concat -c copy` after
    padding each scene's audio; a toolkit fix, not an episode fix. The round-2 cut's audio packets
    are bit-identical to the re-stitched cut's (packet MD5, `recheck2/audio_md5.json`), and the
    adversarial check re-read their timestamps: all 87,538 packets have the same pts and duration as
    in `recheck/adv/audio_packets_clean.csv` (`recheck2/adv/audio_packets_clean.csv`), so the same
    drift is in the round-2 cut.

**Seen in the re-check of the round-2 cut.** None of these is on round 2's list, and the code at
these moments did not change in round 2:

28. **S16 cloud chip (low).** At 29:25.87–29:26.0 the "nothing runs in Google Cloud · you paid only
    for what you sent" chip slides up through "no VM · no bucket · no endpoint" and the "Google Cloud"
    label while those fade out.
    - Text sits over text for about 0.1 s, worst at 29:25.917.
    - The sweep's detector missed it because it is a move, not a transform.
    - Evidence: `recheck2/visual/strips/S16_cloud_chip_move.png`, `S16_cloud_chip_cross_zoom.png`;
      seen again by the adversarial check (`recheck2/adv/sheets/i28_S16_cloud_chip.png`: over the
      note at 29:25.871, over "Google Cloud" at 29:25.938).
    - Not yet planned.
29. **S04 Docker Hub chip (low).** At about 06:25.8–06:26.1 the flying copy of the
    "chromadb/chroma:latest" chip doubles over its own chip's text and the "Docker Hub" label above
    it, worst at 06:25.987.
    - This is the same pattern as S15's question copies, fixed in round 2.
    - Evidence: `recheck2/visual/strips/S04_dockerhub_chip_70.03.png`; seen again by the adversarial
      check (`recheck2/adv/sheets/i29_S04_chip.png`, 06:25.871–06:26.071).
    - Not yet planned.
30. **S10 shrink labels (low).** During V2's shrink, the moving "llm-rag-network" label slides along
    the rail across the pink route lines, and the "8000:8000" label is crossed by its own route line.
    Each lasts about 0.3 s, at about 18:18.2–18:18.5.
    - The S10 fixer and verifier recorded it (`fix2/S10+S12+S14/verify/S10/frame_0008.50.png`), and
      the round-2 frame check found it still present (`recheck2/visual/strips/S10_secrets_shrink_7.55.png`,
      18:18.2–18:18.4; adversarial check `recheck2/adv/sheets/i24_i30_S10_shrink.png`, 18:18.25–18:18.55).
    - It predates round 2: it is visible in `recheck/strips/S10_shrink_morph_18m17_18m18.png`.
    - A line crosses a label, not text over text.
    - Not yet planned; a candidate for the by-design list.

**Smaller nits still open** (not in any fix round):
- **S09 Indicate:** the 0.55 s `Indicate` fills the Chroma cylinder green and the folder glyph
  yellow (*preview* 17:41.6). Neither carries text. Not looked at in the re-stitched cut; in the
  round-2 cut it runs at 17:41.60–17:41.84, the `/data` and "docker-volumes/chromadb/" text turning
  yellow and staying readable (adversarial check, `recheck2/adv/sheets/S09_1741.png`).
- **S03 tag outline:** at the peak of round 2's outline flash on the "your Project ID · not the name"
  tag (05:03.97), the yellow outline comes within 1–2 px of the red row below. The text stays
  readable (`recheck2/visual/strips/S03_yt_tag_108.3.png`, `S03_yt_tag_bottom_edge_zoom4x.png`).
- **From the sweep verifier's 720p previews**, each older than the sweep, with none text over text
  by its account. Times are scene time plus the round-2 scene start, marked *preview*. The round-2
  frame check did not look at them; the adversarial check saw all three again in the round-2 cut
  (`recheck2/adv/sheets/`):
  - S08 *preview* 13:20.57–13:21.06: "instructor" dims while it waits (round-2 cut about
    13:20.65–13:21.0, `S08_instr_1320.png`).
  - S03 *preview* 4:02.47–4:02.71: the gold key icon passes over "Add key", "KEYS" and the crumb for
    a frame or two each (round-2 cut about 4:02.50–4:02.84, where it also crosses "Create new key",
    `S03_key_402.png`).
  - S15 *preview* 27:39.20–27:39.33: the morphing dashed box edge runs through the "Pre-Retrieval"
    label as the label moves into its box (round-2 cut about 27:39.0–27:39.4, `S15_2738.png`).

## Verified (round-2 cut)

Measured on 2026-10-20, 18:36:59–18:48:27 UTC (`recheck2/measured.json`). The method:
- ffprobe;
- a full decode of every video and audio frame;
- an `ebur128=peak=true` pass per file.

`recheck2/chain.sh` ran them one file at a time; the logs are in `recheck2/logs/`. No file changed
while it was being measured. The adversarial check re-ran ffprobe, SHA-256, the audio packet MD5
and `ebur128=peak=true` on all four files (about 19:20–19:25 UTC, `recheck2/adv/ffprobe.txt`,
`sha256.txt`, `audio_md5.txt`, `ebur128_*.log`): every size, duration, frame count, bitrate, hash,
loudness, LRA and true-peak figure in the table below matches, as do the first-peak and
loudest-window times.

The measured check compared 177 figures with this section's previous version, which described the
re-stitched cut and was measured by `recheck/measured.json`. 20 changed: the four files' sizes,
video bitrates and SHA-256 hashes. The other 157 are the same, including durations, frame counts,
loudness, true peak, subtitles and chapters (`recheck2/measured.json`
`comparison_with_REVIEW_verified`).

- **Deliverables:**

  | file | size | duration (container / video) | frames | kbps total (video / audio) | integrated | LRA | true peak | decode errors |
  |---|---|---|---|---|---|---|---|---|
  | `ac215-l05-rag.mp4` | 107.78 MB (107,784,183 B) | 1867.296 s (31:07.3) / 1867.233 s | 112,034 | 461.8 (274.5 / 175.7) | −16.0 LUFS | 2.4 LU | −2.6 dBTP | 0 |
  | `ac215-l05-rag.zh-en.mp4` (to Bilibili) | 106.70 MB (106,702,658 B) | 1867.296 s / 1867.250 s | 112,035 | 457.1 (269.9 / 175.7) | −16.0 LUFS | 2.4 LU | −2.6 dBTP | 0 |
  | `ac215-l05-rag_part1.mp4` | 62.14 MB (62,141,137 B) | 1089.988 s (18:10.0) / 1089.900 s | 65,394 | 456.1 (268.2 / 176.2) | −16.1 LUFS | 2.3 LU | −2.8 dBTP | 0 |
  | `ac215-l05-rag_part2.mp4` | 45.65 MB (45,648,155 B) | 777.422 s (12:57.4) / 777.333 s | 46,640 | 469.7 (283.2 / 174.9) | −16.1 LUFS | 2.4 LU | −2.6 dBTP | 0 |

  - **Format:** all four are 1920×1080 at a constant 60 fps, H.264 High yuv420p, with AAC-LC audio
    at 48 kHz stereo. Decoded frame counts match the header counts.
  - **Loudness:** the stitch normalizes to −16 LUFS in one loudnorm pass, then applies a sample-peak
    limiter at 0.71 (about −3 dBFS) and encodes AAC at 192 kbps. The target is a true peak at or
    below −1.5 dBTP.
    - **The true-peak target is met** by every file: −2.6 dBTP at most, which leaves 1.1 dB of
      headroom (1.3 dB in the first cut).
    - The −2.6 dBTP peak is first reached at 27:56.9 (S15). Part 1 peaks at −2.8 dBTP, first at
      03:11.8 (S02).
    - The loudest 400 ms window is −9.8 LUFS at 14:29.7 (S08), and the loudest short-term reading is
      −14.2 LUFS at 14:30.2 (S08).
    - All these figures are the same as in the re-stitched cut.
  - **Audio:** the zh-en copy carries audio bit-identical to the clean cut's. Both have packet MD5
    `ad24cc8b82ce12d2bed3b27257ba5933`, the same as the re-stitched cut, so fix round 2 changed only
    the picture.
  - **The zh-en picture** is scaled to 1670×938 at the top, with the subtitles in the band below
    (best fit at t = 600 s, `recheck2/zhen_geometry.json`).
  - **SHA-256** (in `recheck2/measured.json` `deliverables`): clean cut `c242b8aa…`, zh-en
    `52f02452…`, part 1 `5e9d097d…`, part 2 `f2fc9a73…`.
- **Scenes and parts:**
  - **Scene durations:** the 16 stitched scenes add up to 1867.233 s and 112,034 frames, exactly the
    full cut's video stream.
  - **No change in fix round 2:** no scene's length, frame count or start changed. The changes
    against the first cut all came from fix round 1: S04 +0.317 s, S08 −0.300 s, S12 −0.133 s.
  - **Render lengths:** each scene's stitched file, 1080p60 render and `events.json` have the same
    length. The exception is S06's render, 5 ms (a third of a frame) shorter than its stitched
    segment, as before.
  - **Render provenance:** all 16 renders started at 17:02:17 UTC or later, after the latest source
    edit (`common.py`, 16:42:50 UTC; `recheck2/provenance.json`). The 16 render logs have 0 "anchor
    not found" and one warning each.
  - **Parts:** part 1 (S01–S09) + part 2 (S10–S16) = 1089.988 + 777.422 = 1867.410 s, against the
    full cut's 1867.296 s. That is +0.114 s, inside ±0.5 s. The two video streams add up to exactly
    1867.233 s.
- **Chapters:**
  - `chapters.txt` has 16 entries in the order and with the titles of `video.yaml`'s scenes. Each time
    is the rounded-down stitched scene start: 00:00, 01:40, 03:15, 05:15, 07:19, 09:09, 11:21, 12:59,
    15:56, 18:09, 19:34, 21:27, 23:31, 25:30, 27:23, 28:49. These are unchanged since `1173d22`.
  - Both part files match their stitched starts too. Part 2 counts from 18:09.900, and its "Chat"
    chapter is 05:21 (05:22 before fix round 1).
  - The three chapter files are byte-identical to `5c0c800` and `983e36e`.
  - `README.md`'s chapter list is copied from these files and still matches them.
- **Subtitles:**

  | track | full | part 1 | part 2 | shortest / longest cue |
  |---|---|---|---|---|
  | `.srt` | 514 | 297 | 217 | 1.003 / 7.360 s |
  | `.zh.srt` | 424 | 241 | 183 | 1.218 / 8.576 s |
  | `.zh-en.srt` | 508 | 294 | 214 | 1.000 / 7.701 s |

  - Every track in all three cuts is numbered 1..N in order, with no overlaps, no empty cue and none
    under 0.8 s, all inside the runtime (the last cue ends at 31:05.491, 1.8 s before the end).
  - The part cues shifted to full time match the full files exactly.
  - `.zh-en.ass` has 508 Dialogue lines (294 and 214 in the parts) with the same text and times as
    `.zh-en.srt`, within 5 ms; WrapStyle 2 with exactly one `\N` per Dialogue line.
  - Every zh-en cue has two non-empty lines. Two have no Chinese characters on their top line: 324
    (19:49.610, only the numbers "0.57、0.77、0.43、0.93") and 457 (27:59.728, the Chester sentence, by
    design); the first cut's third, 314 ("docker compose build"), is fixed by P1. In `.zh.srt` the
    same numbers-only cue (267) is the only cue without a Chinese character; the first cut had it too
    (266), where the CJK comma had been counted as Chinese.
  - The cue-level diff against `1173d22` matches T1–T4, P1, P2, P4 and P5 and nothing else.
  - Fix round 2 changed no subtitle. All subtitle and `.ass` files are byte-identical to `5c0c800`,
    `c187f3b` and `983e36e`, and `git diff 983e36e -- videos/ac215-l05-rag/output` is empty.
- **Burned-subtitle layout:** Chinese at 50 px Noto Sans CJK SC, English at 33 px grey with an
  outline; at most two lines everywhere.
  - **Round-2 burned copy:** one full-resolution frame every 2 s over all 16 scenes (934 samples,
    835 with subtitle ink; `recheck2/adv/band.json`). Every subtitle sits inside y 991–1063 and
    x 443–1476, inside the 1670 px picture width. Nothing is drawn at y 900–990, between the picture
    (y 0–940) and the subtitles. The frame check's pass on 640×360 samples (3 px steps) gives y
    990–1059 and x 444–1473 in 822 of 933 samples (`recheck2/visual/subtitle_band.json`).
  - **Re-stitched burned copy:** y 991–1062 and x 443–1476 (`recheck/subcheck/summary_all_scenes.json`).
  - **Line widths:** the width estimate of every line was made on the first cut's 510 cues
    (`visual_pass/subs/sub_measure.json`), from font metrics. The widest Chinese line is about
    1050 px (cue at 00:20.2). The re-stitched cut's x 443–1476 union matches the ink of that widest
    line in the first cut (`writer/zhen_cue7_t21.5.png`).
- **Narration and anchors:** 140 SAY lines, 4,339 words (part 1 2,534, part 2 1,805), identical to
  the rendered sidecars; voiced time 1719.488 s; 617 `wait_until` calls; 0 "anchor not found" in the
  16 render logs (`recheck2/measured.json` `narration`, `anchors`).
- **Ponders and recap:** the five ponder windows and the recap beats are as in gate 3. The recap beats
  start at 30:15.367, 30:30.367, 30:43.217 and 30:56.467 (`recheck2/measured.json` `ponder`,
  `recap`).
- **Committed files match the cut** (`recheck2/committed_vs_output.json`). When measured (about 18:39
  UTC):
  - the 16 tracked files in `output/` (subtitles, `.ass` files, chapter files and transcript) were
    byte-identical to HEAD `983e36e`, to `c187f3b` and to `5c0c800`;
  - there was no episode or toolkit diff from `c187f3b` to HEAD;
  - nothing was uncommitted in the episode or the toolkit.

  This update of `REVIEW.md` is the only change since. `README.md` needed none: its 31:07
  (1867.3 s), 107 MB, 18:09 and 12:57 and its chapter lists still hold (`recheck2/measured.json`
  `readme_figures`).
- **Lecture-slide tags:**
  - **First cut:** 30 tags, all worded correctly and none overlapped (tag check).
  - **Re-stitched cut:** in the 12 changed scenes, the re-check confirmed one tag at a time at every
    swap, T02 and T08 on their cited pictures, every tag gone before its scene ends and every last
    frame empty. T04 is by design. The tags of S02, S03, S07 and S09, whose code did not change (they
    were re-rendered for `common.py`), were not looked at again except in the review-bot frames of S03
    and S09 and the adversarial check's 5 s samples of the burned copy. Those samples showed one tag
    at a time and none over text.
  - **Round-2 cut:** the frame check saw these swaps in sequence: S01's A6–A7 → A8–A10, S08's A40–A43
    and A44–A47, and S15's swaps. S07's B16–B19 comes in only after the chunk_overlap chips leave.
    A54–A55, B68–B76 and A63 span their pictures, and all 16 last frames are empty. The other tags
    appear only in its 2 s contact sheets, where nothing was found.
- **Review-bot items:** all 11 were verified on frames of the re-stitched cut ("Re-check of the
  re-stitched cut"). None was assigned to the round-2 checks.
  - **Item 10, S13's tracker captions:** re-verified frame by frame on the round-2 cut.
    - The step changes are now sequential: old out, then new in.
    - 24:34.45 has 8 empty frames between the two captions.
    - 24:29.78 starts from a blank caption.
    - At 25:14.6 at most about 5 % of the old caption is left for one or two frames.
    - No frame shows both captions above 8 % (`recheck2/visual/strips/series_S13_step_*.png`,
      `recheck2/visual/tracker_steps_metric.json`).
  - **Items 1–9 and 11:** not re-measured on the round-2 cut, and seen only in its 2 s contact sheets
    (nothing found). The tracker step changes in the same scenes were measured, but in the tracker
    only: S08 14:48.07 (near item 3), S09 17:10.57 (near item 4) and S11 20:58.20 (near item 9).
- **Narration heard by ASR:** no mispronunciation or swallowed word in 514 cues. That is the ASR
  round trip on the re-stitched cut, whose audio packets are bit-identical to the round-2 cut's. The
  first cut's ASR found the same in 513 cues.
- **Evidence provenance** (`ASSETS.md`):
  - **Real captures:** every terminal panel prints from `assets/terminal/`, captured 2026-10-16
    00:52–00:57 UTC on a fresh `docker:29.8.2-dind` laptop with Compose v5.6.0 and no Google key:
    the clone, `sh docker-shell.sh` with its build and Chroma start, both chunkers (24/35 Tolminc
    chunks, 8,248/14,228 in all), the second-terminal checks, the no-key failures of `--embed`,
    `--query` and the semantic run, teardown, the restart test, and the G1/G5 gotchas. Code panels
    quote `assets/source/`, copied unchanged at `e17a39f` (and `96d5fd7`, the `pipenv` branch).
  - **Recorded:** the embeddings are the staff's own `gemini-embedding-001` vectors from `68e0bde`,
    whose 22 chunk files are byte-identical (sha1) to the ones chunked here; loading them, `--get`,
    the vector lengths, the filter counts and the stand-in query are real runs on them (tag
    `recorded`). The L06 preview and the stale-index beat quote the staff's committed `out.txt`.
  - **Illustration (tagged):** the GCP console steps (service account, roles, JSON key), enabling
    the Vertex AI API, Vertex AI answering, and the course web tools (`/chunkviz`, `/chromaui`,
    `/chat`) are schematic drawings; the CORS check behind them is real. Lecture slides are redrawn
    in our pictures, never shown.

## Not claimed

- **No human has watched or listened to any of the three cuts** (first final cut, re-stitched cut,
  round-2 cut). The listening sign-off is waived for the series (gate 6).
  - **What ASR shows:** the two ASR round trips show that a machine can understand the narration.
    They do not judge pacing, tone or how natural the voice sounds.
  - **Judged without an ear:** the connected-speech passages under "Final-cut checks" (cues 157, 185,
    286, 311, 448, 103, 304, 396 of the first cut), "Tolminc" and the cue-9 "this story" / "the
    story" difference ("Re-check") were judged from transcripts and phonemes, not by ear.
- **No ASR ran on the round-2 cut.** Both round trips ran on earlier stitches: the first final cut and
  the re-stitched cut. The round-2 cut's audio is taken as covered because its audio packets are
  bit-identical to the re-stitched cut's (packet MD5, `recheck2/audio_md5.json`). Fix round 2 changed
  no narration, so its scenes' audio was compared by that MD5 only.
- **The changed narration (S04, S08, S12, fix round 1) was checked by machine only:** the fixer's
  phonemizer check, the changed-scene check's speech onsets and the re-check's ASR. Nobody heard it.
- **Agents alone reviewed the Chinese and bilingual subtitles:** the QA subtitle watcher, the
  narration/subtitle fixer, the first finishing pass's proofread, the verifiers, the first cut's
  pairing check, fix round 1's text agent and the re-check's cue-level diff. No native-speaker human
  has read them. The re-stitched `.zh-en.srt` was not read cue by cue again: the re-check compared it
  with the first cut's and read the cues that changed. The zh-only `.zh.srt` was checked for
  structure (counts, timing, overlaps) and by the same diff, not read cue by cue. The round-2
  subtitle files are byte-identical to the re-stitched cut's and were not read again.
- **The visual review sampled the video.** In the first cut: one frame every 3 s, targeted frames, a
  motion scan and a tag-region scan at 30 fps. In the re-stitched cut: targeted frames at every fixed
  moment, one frame every 2 s of the 12 changed scenes, all 31 terminal scrolls, the review-bot
  frames, and the subtitle-band pixel check over all 16 scenes. Not continuous playback. S02, S03,
  S07 and S09 were re-rendered (their code did not change except through `common.py`) and were
  looked at again only through their scrolls (S09), the review-bot frames (S03, S09), the subtitle
  band and one burned-copy frame every 5 s taken by the adversarial check
  (`recheck/adv/M_S02_S03_every5s_zhen.png`, `M_S07_every5s_zhen.png`, `M_S09_every5s_zhen.png`;
  nothing found); their scene lengths are unchanged (`recheck/measured.json` `scenes`), and fix round
  1's shared verifier found S07's and S09's events identical to the first cut's. The smaller
  verifier nits that were not in a fix round were not looked for again.
- **The round-2 visual review also sampled the video.** It covered:
  - targeted frames at every changed moment;
  - all 15 tracker step changes and the 3 section switches, frame by frame;
  - 55 contact sheets of the burned copy (one frame every 2 s, all 16 scenes);
  - the 16 last frames;
  - the subtitle band (933 samples; the adversarial check re-ran it on 934 full-resolution frames).

  The adversarial check of this record re-extracted frames at every changed moment, items 28–30
  and the open nits (`recheck2/adv/sheets/`). Neither was continuous playback. These were not
  re-checked one by one on the round-2 cut:
  - the fixes of rounds 1 and 1b, except the S01, S08 and S15 tag swaps and the S12 underline;
  - the review-bot items, except item 10;
  - the 31 terminal scrolls, though `_make_room`'s L05 rebinding is unchanged since fix round 1.
- **The sweep is not proof that nothing is left.** The sweeper judged 23 candidates not real; its
  verifier spot-checked four of them and found one real (S15's "①ndexing", fixed), so 22 stand as
  judged. They were judged on 1080p renders and 720p previews, not on the round-2 cut. The round-2
  frame check then found two text-over-text moments that the sweep's detector missed (items 28 and
  29), and the sweep also counted the by-design 17:40.5 morph as replaced when it changed only the
  swap before it (see "Final-cut checks", short morphs).
- **Fix round 2's verifiers worked on 720p previews.** Only the round-2 frame check looked at the
  1080p60 round-2 cut.
- **The part files were not visually sampled.** They were decoded and measured, and their subtitles
  and chapters compared with the full files.
- **The QA and finishing fixes were verified on 480p and 720p preview renders, not one by one in
  the 1080p cuts.** In the cuts they were checked only by the five checks of the first cut (which
  re-verified the 11 review-bot items, the shared `common.py` fixes and every slide tag, and read
  every 3 s), the frames looked at for the first version of this record (`sheets/sheet_37.png`,
  `sheet_39.png`, frames at 00:03, 00:14.5, 00:21.5 and 13:30, the first 14 s, and the four nit
  frames in `verifier/`) and, in the re-stitched cut, the re-check above. In the round-2 cut they
  were seen only in the round-2 frame check's 2 s contact sheets.
- **The burned subtitles were not read back by text recognition.** The first cut's pairing check
  compared its 14 flagged-cue crops and 2 full frames with the subtitle files; the visual passes
  looked at placement; the re-check's contact sheets show the changed cues (T1, T2, T3, P1, P2) on
  the burned copy, read by eye. Subtitle widths are font-metric estimates checked against ink on four
  frames of the first cut ("Verified").
- **Nothing that needs a Google account or key was run:**
  - creating the service account, granting its roles, downloading the JSON key, and enabling the
    Vertex AI API (illustrations);
  - a successful `--embed` (the staff's recorded vectors stand in), `--query` and `--chat` with a
    key (the commands are typed, the real no-key errors shown; no `--chat` output exists in the
    video), and the semantic-split run (about 528 embedding calls);
  - the course web tools in a browser (illustrations; the CORS answer is real);
  - L06's `--agent` run (the staff's recorded `out.txt`).

  The "with your key, look for" cards are not observed output, and the call counts ("about 89 and
  148", "about 528") and "a few cents" are our estimates.
- **Docker Hub not used directly:** images were pulled through `mirror.gcr.io`, and the base image
  `python:3.12-slim-bookworm` was rebuilt under the same name inside the laptop for the capture
  proxy, so the build shows no base-image download that a student's first build would show. This
  tutorial has no push or `docker login`.
- **Not run on the other platforms the narration mentions:** a Mac and Windows (WSL or Git Bash),
  Docker Desktop, and Apple Silicon (`aarch64` in the banner, per `ASSETS.md`). The captures ran on
  Linux, in a dind stand-in laptop.
- **The released files will be a different render.** Everything here is about the local round-2
  stitch of 2026-10-20 17:46–18:35 UTC. The release workflow re-renders with the pinned engine and writes
  `<id>.validation.json`, which does not exist yet. Duration, frames, loudness, true peak, cue
  counts and chapters must be re-checked on those files, and this record updated.
