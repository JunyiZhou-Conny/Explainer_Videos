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
- **Re-stitched cut (the cut this record now describes, 31:07.3):** scene segments 10:11–10:31 UTC,
  the clean cut and its subtitles at 10:34, the zh-en copy at 10:59 and the parts at 11:01–11:02 UTC.
  Subtitles, chapters and transcript are committed in `5c0c800` (11:03 UTC).
- **Re-check:** three agent checks of the re-stitched cut on 2026-10-20, about 11:04–12:03 UTC: the
  changed scenes on frames, the measured checks and an ASR round trip (evidence in `build/recheck/`).
  For this update the 11 review-bot items and the shared `common.py` items were re-checked on frames of
  the re-stitched cut (`recheck/bot/`, about 12:05–12:15 UTC).
- **This update:** 2026-10-20, about 12:15–12:25 UTC. Items the fix rounds closed moved to "Fixed";
  the rest stay under "Still open" with their reasons.
- **Adversarial check of this update:** 2026-10-20, about 12:20–12:50 UTC (evidence in
  `recheck/adv/`): `ebur128=peak=true` and ffprobe re-run on all four MP4s, cue counts, gaps and the
  cue-level diff re-derived from the files, chapters recomputed from the stitched segments, and frames
  re-extracted for the visual claims. It corrected the scroll count (31, not 26), the S04, S06, S12
  and S13 timings, the S12 box geometry (items 16 and 26), the scene-join numbers (item 27) and the
  continuation-cue count, and looked at S16's section switch in the re-stitched cut (item 8).

This record is based on the five checks' reports, `measured.json`, the evidence folders beside
them, the QA and finishing-pass outputs (`/root/ac215-backup/tasks/w6byzicvp.output`,
`we2lzv8iu.output`, `w6tfmzqr5.output`), `script.md` and `BRIEF.md` (as committed in `f466f8e`),
`ASSETS.md` and `SLIDES.md`. The update adds the fix-round outputs (`w0eoryitz.output`,
`w8umzlyij.output`), the re-check's three reports and its evidence (`build/recheck/`:
`measured.json`, `asr-summary.json`, `notes.txt`, `strips/`, `sheets/`, `subcheck/`, `bot/`) and
`script.md` as committed in `5c0c800`. Verified facts and unclaimed reviews are kept in separate
sections.

**Conventions in this record:**
- **Times** are mm:ss in the full video. Gates 3 and 6, "Re-check of the re-stitched cut", "Fixed",
  "Still open" and "Verified" use the re-stitched cut (`output/ac215-l05-rag.mp4`, 31:07.3). Gates 1,
  2, 4 and 5, "Whole-video QA" and "Final-cut checks" use the first final cut (31:07.4), except where
  marked *draft* or *preview*. Between the two cuts a scene's start moved by 0 s (S01–S04),
  +0.316/+0.317 s (S05–S08), +0.016/+0.017 s (S09–S12) or −0.116/−0.117 s (S13–S16): S04 grew by
  0.317 s and S08 and S12 shrank by 0.300 s and 0.133 s with the T1–T4 sentences
  (`recheck/scene_starts_old_vs_new.json`). Inside S04, S08 and S12, moments after those sentences
  moved with them.
- **Draft times** refer to the 480p QA draft (30:42.8). Later fixes made the video 24.6 s longer;
  scene starts moved by up to 19.7 s (S16 started at draft 28:30 and at 28:49.7 in the first final
  cut), and S16 itself grew by about 5 s, so a draft time can be up to about 25 s earlier than the
  same moment in the first final cut (24.6 s at the very end).
- **Cue numbers** say which file they come from: `.srt`, `.zh.srt` or `.zh-en.srt`. In the sections
  that use the re-stitched cut they number its files (514, 424 and 508 cues); elsewhere they number
  the first final cut's (513, 423 and 510). From S04's new sentence on, the two numberings differ
  (`recheck/subtitle_changes_old_vs_new.txt` lists every changed cue in both).
- **Evidence paths** are relative to `build/final-review/` (`verifier/` holds the frames, cue lists
  and loudness log of the adversarial check of the first version), except paths that start with
  `recheck/` (`build/recheck/`), `fix1/` or `fix1b/` (`build/fix1/`, `build/fix1b/`). The folders are
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
     step, from "Pause and do both, in your course folder." (03:41.3) to "Pause and tear down now, so
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
   - **Size (re-stitched cut):** 140 SAY lines and 4,339 words, identical to the 140 narration blocks
     in the renders (`recheck/measured.json` `narration`). Kokoro `af_heart` at speed 0.9 in all 16
     scenes. Pace 139.4 wpm over the runtime, 151.4 wpm over voiced time (28:39.5, 92.1 % of the
     runtime).
   - **Anchors:** 617 `vo.wait_until` calls across the 16 scene files (23 in S07 to 54 in S09; 6 take
     a variable instead of a literal phrase). The 16 1080p60 render logs of the re-renders have 0
     "anchor not found" warnings.
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
6. **Measured checks** ✔. The numbers are under "Verified (re-stitched cut)" (`recheck/measured.json`).
   - **Duration:** 31:07.3 (1867.296 s), inside the series' 25–35 min; parts 18:10.0 (1089.988 s)
     and 12:57.4 (777.422 s).
   - **Loudness:** −16.0 LUFS integrated in the clean cut and the zh-en copy and −16.1 LUFS in the
     parts, LRA 2.3–2.4 LU; true peak −2.6 dBTP in the clean cut, the zh-en copy and part 2, and
     −2.8 dBTP in part 1. The build's target is −16 LUFS with true peak at or below −1.5 dBTP: every
     file meets it, with at least 1.1 dB to spare.
   - **Caption bounds:** in the zh-en copy every one of the 508 cues is one Chinese line over one
     English line (WrapStyle 2, exactly one `\N` per Dialogue line in all three `.zh-en.ass` files),
     in the band under the picture (the picture is scaled to 1670×938 at the top). A pixel check of
     the burned copy over all 16 scenes, one sample every 2 s, found every subtitle inside y 991–1062
     and x 443–1476 and nothing burned over the picture (`recheck/subcheck/summary_all_scenes.json`),
     so no subtitle covers a command or a tag.
   - **Music balance:** does not apply. L05, like L02–L04, has no score: `video.yaml` has no `music:`
     key.
   - **Subtitle sync:** the four cues that came 1.0–1.6 s early are sentence starts now and appear
     0.04–0.08 s before their speech; no continuation cue is more than 1.0 s early ("Fixed", item 9).

   **Human review:** the series waiver below stands in for a listening sign-off.

   Listening sign-off: waived by Conny for the AC215 series (Explainer_Videos#29, 2026-10-15): 「不需要，我现在对视频质量很满意的」 — no human listened to this cut; the ASR round trip below is the substitute.

   The ASR round trip of the final-cut checks ran on the previous stitch (the 31:07.4 clean cut of
   2026-10-19 23:11 UTC, whose zh-en copy carried bit-identical audio). Since then the narration of
   three scenes changed: S04 (T4, "Its context was 112 megabytes. Most of it is git history, which
   still holds…"), S08 (T1, "…3,072 numbers. The code asks for the first 256. The model is trained…";
   T3, "Step 1: … char split. It's the first call to Google.") and S12 (T2, "…keeps 1,355. The word
   Italian keeps 64."). No other SAY line changed (`git diff f466f8e 5c0c800 -- script.md`). The
   changed sentences' audio was checked by machine only: the changed-scene check measured their speech
   onsets against the new cues, and the re-check ran a second ASR round trip over the whole
   re-stitched cut (the zh-en copy has the same audio packets), which heard all four as written ("ASR
   round trip on the re-stitched cut" below).

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
  item 11 under "Final-cut checks"; again on the re-stitched cut, "Re-check").
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
  about 0.25 s (29:57.1–29:57.3; "Still open", item 8).

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
  no tag stuck on screen and no garbled text at rest; the short morphs at 05:52, 06:01, 08:13.3,
  17:40.5, 26:01.5 and 28:08.4 are by design; the clean and burned pictures match when scaled the
  same way (4 times).
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
numbers were replaced by the re-check's under "Verified (re-stitched cut)"; its findings were items
18–22.

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

**Review-bot items, re-checked on frames for this update** (`recheck/bot/summary.json`; the sheets
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
re-checked: the other tracker changes in S06, S09 and S14. S16's section switch was looked at by the
adversarial check: the double exposure is still there ("Still open", item 8).

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
`recheck/chain.sh`, `light.py`, `subs_compare.py`, `narration.py`, `assemble.py`). Its numbers are
under "Verified (re-stitched cut)".

**Seen in passing, outside this round's fix list** (items 23–26 under "Still open"), and by design:
short morphs at 13:29.2 (S08's dot-product copies pass over "B 0.976" for about 0.2 s), 18:50.05
(S10's folder group morphs into the top-right chip, over empty space), 22:02.95 (S12's dot-count
label) and 28:19.4 (S15's "rare words" note morphs into the `$contains` chip)
(`recheck/strips/S08_dot_product_flight_13m29.png`, `S10_morph_18m49_to_tag.png`,
`S12_italian_dots_label_22m03.png`).

## Open and fixed items

Fix rounds 1 and 1b closed items 1–4 and 9–17 and every smaller nit except S09's (plus S06's
visualizer bars, noticed during fix round 1); the `publish:` block closed item 19; item 18 was done
before. Each fixed item gives its re-stitched-cut times and evidence.
"Not planned" says why an item was left.

### Fixed (checked on the re-stitched cut)

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
    `recheck/adv/release_preflight_after_verify.log`; exit 0 each time).

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
   `devops.tag()` is taller than the terminal row pitch. Not planned: shared toolkit.
8. **Section switch double exposure:** S16's tracker header lifts off while "Agents (L06)" drops in;
   in the first cut both read at once for about 0.25 s ("README › Run C…(L06)", 29:57.1–29:57.3,
   `bugbot/tracker_s16c/tracker_s16c_montage.png`). The shared-pass verifier saw the same in S03
   (*preview* about 03:46.6 and 04:46.7). `switch_section()` was not changed. The re-stitched cut has
   the same double exposure, 0.116 s earlier: both headers show at 29:56.95–29:57.2 and read
   "README › Run C…(L06)" at 29:57.05–29:57.1; from 29:57.3 only "README › Agents (L06)"
   (`recheck/adv/J2_S16_switch.png`; S03's switches were not looked at). Not planned:
   `switch_section()` is designed this way; it reads like the tag swaps of item 1, so the coordinator
   may want the same sequential fix.

**Release and format**

20. **Gate 3 shortfall:** five ponders against the aim of about 15.6. Not planned: it matches BRIEF.md
    and the series rule of 3–5; see gate 3, with its question for Conny.
21. **Narration over its budget:** 4,339 words against BRIEF.md's 3,900–4,300 (39 over; T1–T4 added
    four); part 1 has 2,534 against its plan of about 2,410 (5 % over). Not planned: the runtime,
    31:07, is inside 25–35 min.
22. **Burned copy's start (no visible effect):** the zh-en copy's video starts at 0.000 s, the clean
    cut's and the parts' at 0.021 s, and it has one more frame (112,035 against 112,034). Not
    planned: about one frame.

**Seen in the re-check, outside this round's fix list** (each predates fix round 1; none was in an
earlier review):

23. **S05 copy flights (low):** three `TransformFromCopy` flights still cross terminal text, each
    under 1 s: at 7:52.9–7:53.6 the `/secrets/llm-service-account.json` copy rises across the
    `GOOGLE_APPLICATION_CREDENTIALS=…` row; at 8:02.33–8:03.23 the `llm-rag-chromadb → 172.19.0.2`
    copies cross the `total 8 / drwxr…` rows and the terminal title, garbled at about 8:02.8
    (`recheck/strips/S05_getent_copy_flight_8m02.png`); at 8:41.05–8:41.85 the `llm-rag-main/
    secrets/` copies lift out over "Cloning into" (`recheck/strips/S05_other_copy_flights.png`). The
    same kind of flight was fixed in S06 and S12 this round. Not yet planned.
24. **S10 shrink morph (low):** during V2's shrink to the compact layout the vanishing `secrets/` row
    slides half-transparent through the folder labels at 18:17.9–18:18.3, gone by 18:18.45
    (`recheck/strips/S10_shrink_morph_18m17_18m18.png`). Not in the by-design morph list. Not yet
    planned.
25. **S14 your-turn chip (low):** the `Indicate` at 27:18.25–27:18.95 fills the "▶ your turn" chip
    yellow, so its text is unreadable for about 0.3 s at 27:18.6
    (`recheck/strips/S14_your_turn_indicate_27m18.png`); the same whole-chip fill was fixed in S10.
    Not yet planned.
26. **S12 line 357/358 boxes (low; noticed by the S12 fixer, flagged by no review):** at the end of
    beat 0 the pink boxes of lines 357 and 358 overlap: 358's top edge (y 536–539) runs inside 357's
    box, just under line 357's text, and 357's bottom edge (y 548–551) runs above line 358's text, so
    a double pink line separates the two rows; under "The Complete Book of Cheese" the pink underline
    (about y 544–547) merges into 357's bottom edge (21:38.6; `recheck/notes.txt`,
    `recheck/adv/F2_S12_boxes_zoom2x_21m38.6.png`). Text stays readable. Not yet planned.
27. **Audio timing at the scene joins (toolkit; no effect in players that follow timestamps):** at
    each of the 15 joins an AAC packet's timestamp spans fewer samples than the 1,024 it decodes to
    (16 short packets of 1–1,023 samples, two of them at the S04/S05 join), so a player or tool that
    plays every decoded sample without re-syncing runs 1–21 ms per join behind the picture, 0.204 s
    by S16 (`recheck/asr/audio_packets.csv`, `recheck/asr/audio_shift.json`; packet list re-read
    with ffprobe, `recheck/adv/audio_packets_clean.csv`). The first cut has the same drift. It looks
    consistent with `explainer/build.py` joining the per-scene files with `concat -c copy` after
    padding each scene's audio; a toolkit fix, not an episode fix.

**Smaller nit still open** (not in either fix round): S09's 0.55 s `Indicate` fills the Chroma
cylinder green and the folder glyph yellow (*preview* 17:41.6; neither carries text; not looked at
in the re-stitched cut).

## Verified (re-stitched cut)

Measured on 2026-10-20, about 11:05–11:20 UTC (`recheck/measured.json`; ffprobe, a full decode of
every video and audio frame and an `ebur128=peak=true` pass per file, run one at a time by
`recheck/chain.sh`; logs in `recheck/logs/`).

- **Deliverables:**

  | file | size | duration (container / video) | frames | kbps total (video / audio) | integrated | LRA | true peak | decode errors |
  |---|---|---|---|---|---|---|---|---|
  | `ac215-l05-rag.mp4` | 108.64 MB (108,643,796 B) | 1867.296 s (31:07.3) / 1867.233 s | 112,034 | 465.5 (278.2 / 175.7) | −16.0 LUFS | 2.4 LU | −2.6 dBTP | 0 |
  | `ac215-l05-rag.zh-en.mp4` (to Bilibili) | 107.36 MB (107,360,446 B) | 1867.296 s / 1867.250 s | 112,035 | 460.0 (272.7 / 175.7) | −16.0 LUFS | 2.4 LU | −2.6 dBTP | 0 |
  | `ac215-l05-rag_part1.mp4` | 62.58 MB (62,579,184 B) | 1089.988 s (18:10.0) / 1089.900 s | 65,394 | 459.3 (271.4 / 176.2) | −16.1 LUFS | 2.3 LU | −2.8 dBTP | 0 |
  | `ac215-l05-rag_part2.mp4` | 46.07 MB (46,069,721 B) | 777.422 s (12:57.4) / 777.333 s | 46,640 | 474.1 (287.6 / 174.9) | −16.1 LUFS | 2.4 LU | −2.6 dBTP | 0 |

  - **Format:** all four are 1920×1080 at a constant 60 fps, H.264 High yuv420p, with AAC-LC audio
    at 48 kHz stereo. Decoded frame counts match the header counts.
  - **Loudness:** the stitch normalizes to −16 LUFS in one loudnorm pass, then a sample-peak limiter
    at 0.71 (about −3 dBFS) and AAC at 192 kbps; the target is true peak at or below −1.5 dBTP. **The
    true-peak target is met** by every file: −2.6 dBTP at most, 1.1 dB of headroom (1.3 dB in the
    first cut). The −2.6 dBTP peak is first reached at 27:56.9 (S15); part 1 peaks at −2.8 dBTP,
    first at 03:11.8 (S02). The loudest 400 ms window is −9.8 LUFS at 14:29.7 (S08) and the loudest
    short-term reading −14.2 LUFS at 14:30.2 (S08).
  - **The zh-en copy** carries audio bit-identical to the clean cut's (packet MD5
    `ad24cc8b82ce12d2bed3b27257ba5933`); its picture is scaled to 1670×938 at the top with the
    subtitles in the band below.
  - SHA-256 of each file is in `recheck/measured.json` `deliverables`.
- **Scenes and parts:**
  - 16 stitched scenes whose durations add up to 1867.233 s, exactly the full cut's video stream.
    Only three scenes changed length: S04 +0.317 s, S08 −0.300 s, S12 −0.133 s. Each scene's stitched
    file, 1080p60 render and `events.json` have the same length, except S06's render, 5 ms (a third
    of a frame) shorter than its stitched segment, as in the first cut. All 16 renders started after
    their latest source edit; the 16 render logs have 0 "anchor not found" and one warning each.
  - Part 1 (S01–S09) + part 2 (S10–S16): 1089.988 + 777.422 = 1867.410 s against the full cut's
    1867.296 s (+0.114 s, inside ±0.5 s); the two video streams add up to exactly 1867.233 s.
- **Chapters:** `chapters.txt` has 16 entries in the order and with the titles of `video.yaml`'s
  scenes; each time is the rounded-down stitched scene start (00:00, 01:40, 03:15, 05:15, 07:19,
  09:09, 11:21, 12:59, 15:56, 18:09, 19:34, 21:27, 23:31, 25:30, 27:23, 28:49), unchanged since
  `1173d22`. Both part files match their stitched starts too (part 2 counts from 18:09.900; its
  "Chat" chapter is now 05:21, was 05:22). `README.md`'s chapter list is copied from these files.
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
- **Burned-subtitle layout:** Chinese at 50 px Noto Sans CJK SC, English at 33 px grey with an
  outline; at most two lines everywhere. In the re-stitched burned copy every subtitle sits inside
  y 991–1062 and x 443–1476 (one sample every 2 s over all 16 scenes,
  `recheck/subcheck/summary_all_scenes.json`), inside the 1670 px picture width. The width estimate
  of every line (font metrics, about 1050 px for the widest Chinese line, cue at 00:20.2) was made on
  the first cut's 510 cues (`visual_pass/subs/sub_measure.json`); the re-stitched cut's x 443–1476
  union matches the ink of that widest line in the first cut (`writer/zhen_cue7_t21.5.png`).
- **Narration and anchors:** 140 SAY lines, 4,339 words (part 1 2,534, part 2 1,805), identical to
  the rendered sidecars; voiced time 1719.488 s; 617 `wait_until` calls; 0 "anchor not found" in the
  16 render logs.
- **Ponders and recap:** the five ponder windows and the recap beats as in gate 3 (recap beats start
  at 30:15.367, 30:30.367, 30:43.217 and 30:56.467; `recheck/measured.json` `ponder`, `recap`).
- **Committed files match the cut:** when measured (about 11:20 UTC) the subtitles, `.ass` files,
  chapter files and transcript in `output/` were byte-identical to `5c0c800` and to HEAD `d17c002`,
  with no episode or toolkit diff from `5c0c800` to HEAD and nothing uncommitted in the episode or
  the toolkit (`recheck/measured.json` `committed_vs_output`). This update of `REVIEW.md` and
  `README.md` is the only change since.
- **Lecture-slide tags:** 30 tags, all worded correctly and none overlapped (tag check of the first
  cut). In the re-stitched cut the re-check confirmed, in the 12 changed scenes, one tag at a time
  at every swap, T02 and T08 on their cited pictures, every tag gone before its scene ends and every
  last frame empty; T04 is by design. The tags of S02, S03, S07 and S09, whose code did not change
  (they were re-rendered for `common.py`), were not looked at again except in the review-bot frames
  of S03 and S09 and the adversarial check's 5 s samples of the burned copy (one tag at a time, none
  over text, at those samples).
- **Review-bot items:** all 11 verified on frames of the re-stitched cut ("Re-check").
- **Narration heard by ASR:** no mispronunciation or swallowed word in 514 cues (ASR round trip on
  the re-stitched cut), as in the first cut's 513.
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

- **No human has watched or listened to either cut.** The listening sign-off is waived for the series
  (gate 6). The two ASR round trips show that a machine can understand the narration; they do not
  judge pacing, tone or how natural the voice sounds. The connected-speech passages under "Final-cut
  checks" (cues 157, 185, 286, 311, 448, 103, 304, 396 of the first cut), "Tolminc" and the cue-9
  "this story" / "the story" difference ("Re-check") were judged from transcripts and phonemes, not
  by ear.
- **The changed narration (S04, S08, S12) was checked by machine only:** the fixer's phonemizer
  check, the changed-scene check's speech onsets and the re-check's ASR. Nobody heard it.
- **Agents alone reviewed the Chinese and bilingual subtitles:** the QA subtitle watcher, the
  narration/subtitle fixer, the first finishing pass's proofread, the verifiers, the first cut's
  pairing check, fix round 1's text agent and the re-check's cue-level diff. No native-speaker human
  has read them. The re-stitched `.zh-en.srt` was not read cue by cue again: the re-check compared it
  with the first cut's and read the cues that changed. The zh-only `.zh.srt` was checked for
  structure (counts, timing, overlaps) and by the same diff, not read cue by cue.
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
- **The part files were not visually sampled.** They were decoded and measured, and their subtitles
  and chapters compared with the full files.
- **The QA and finishing fixes were verified on 480p and 720p preview renders, not one by one in
  the 1080p cuts.** In the cuts they were checked only by the five checks of the first cut (which
  re-verified the 11 review-bot items, the shared `common.py` fixes and every slide tag, and read
  every 3 s), the frames looked at for the first version of this record (`sheets/sheet_37.png`,
  `sheet_39.png`, frames at 00:03, 00:14.5, 00:21.5 and 13:30, the first 14 s, and the four nit
  frames in `verifier/`) and, in the re-stitched cut, the re-check above.
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
- **The released files will be a different render.** Everything here is about the local re-stitch of
  2026-10-20 10:11–11:02 UTC. The release workflow re-renders with the pinned engine and writes
  `<id>.validation.json`, which does not exist yet. Duration, frames, loudness, true peak, cue
  counts and chapters must be re-checked on those files, and this record updated.
