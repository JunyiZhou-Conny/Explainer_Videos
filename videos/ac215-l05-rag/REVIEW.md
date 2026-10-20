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
- **Final cut (the cut reviewed here, 31:07):** stitched from those renders on 2026-10-19: the clean
  cut and its subtitles at 23:11, the zh-en copy at 23:28 and the parts at 23:30–23:31 UTC.
  Subtitles, chapters and transcript are committed in `f466f8e` (2026-10-20 01:43 UTC).
- **Final-cut checks:** five agent checks on 2026-10-20 (reports `build/final-review/report-*.md`,
  all five present). The ASR data was written at 01:49 UTC; the tags, pairs and ASR reports were
  saved at 06:43. A usage limit cut the first visual and measured attempts; both were re-run
  (`measured.json` at 06:59, both reports at 07:35 UTC). Each re-run says which earlier files it set
  aside: the visual pass moved the first attempt's sheets to `sheets_prev_label-offset/` (their
  labels ran about 1.5 s ahead of the picture) and did not use its freeze list
  (`visual/freeze_vs_events.txt`, which counted fades as freezes); the measured pass checked the
  first attempt's `measured/` (its light checks are identical on every shared field) and re-ran
  every decode and loudness pass into `measured_v2/`.
- **This record:** written 2026-10-20 at about 07:40–08:00 UTC. **Fix round 1** (plan
  `/root/ac215-backup/args/l05-fix1.json`, 07:37 UTC) runs in parallel and edits `scenes/`,
  `script.md` and `i18n/zh/`. Every defect below is still **open** in the reviewed cut; the planned
  fix is named with each. A re-check after the re-render updates this file.

This record is based on the five checks' reports, `measured.json`, the evidence folders beside
them, the QA and finishing-pass outputs (`/root/ac215-backup/tasks/w6byzicvp.output`,
`we2lzv8iu.output`, `w6tfmzqr5.output`), `script.md` and `BRIEF.md` (as committed in `f466f8e`),
`ASSETS.md` and `SLIDES.md`. Verified facts and unclaimed reviews are kept in separate sections.

**Conventions in this record:**
- **Times** are mm:ss in the full video (`output/ac215-l05-rag.mp4`, 31:07.4), except where marked
  *draft*. Draft times refer to the 480p QA draft (30:42.8). Later fixes made the video 24.6 s
  longer; scene starts moved by up to 19.7 s (S16 started at draft 28:30 and starts at 28:49.7), and
  S16 itself grew by about 5 s, so a draft time can be up to about 25 s earlier than the same moment
  in the final cut (24.6 s at the very end).
- **Cue numbers** say which file they come from: `.srt` (513 cues), `.zh.srt` (423) or `.zh-en.srt`
  (510), all of the reviewed cut.
- **Evidence paths** are relative to `build/final-review/` (`verifier/` holds the frames, cue lists
  and loudness log of the adversarial check of this record). The folder is git-ignored and exists only
  in the producing session, so a successor has to re-run the checks to reproduce the evidence.
  Times taken from a verifier's 720p preview are given as scene time plus the scene's start in the
  final cut, and are marked *preview*.

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
   In the final cut, the tag check found the cited picture on screen across the lecture-slide tag
   spans, except T04, which by design demonstrates the tag itself, and two spans that are "Open",
   items 2 and 3; the visual pass read the burned-in copy every 3 s.
3. **Pause-and-ponder moments and a recap** ⚠ partly met.
   - **Ponders:** five cards, each a 0.6 s fade-in and an 8 s silent timer; each answer starts as its
     timer ends or after it (`measured.json` `ponder`). No English cue plays during a timer: the five
     longest cue gaps (8.8–11.8 s) are these five windows.

     | scene | question (card text, condensed) | card | timer | answer starts |
     |---|---|---|---|---|
     | S06 | 7,808 characters, windows of 350 overlapping by 20: how many chunks? | 10:02.0 | 10:02.6–10:10.6 | 10:10.6 |
     | S07 | Same chunk size, 350: why 14,228 chunks instead of 8,248? | 12:06.5 | 12:07.1–12:15.1 | 12:18.0 |
     | S08 | The database will compare by cosine; these vectors are shorter than 1: does that change which chunks count as nearest? | 15:34.9 | 15:35.5–15:43.5 | 15:43.5 |
     | S12 | The question is about Tolminc; the query keeps one book and only chunks containing "Italian": what will the ten results be about? | 21:43.4 | 21:44.0–21:52.0 | 21:52.0 |
     | S14 | char-split ran the chunk step without a key. Can semantic-split? | 26:14.1 | 26:14.7–26:22.7 | 26:22.7 |

   - **Rate:** one ponder every 6.2 min. AGENTS.md aims for one every 2 min, about 15.6 at this
     length; the series brief fixes 3–5 per lecture (`ac215-video` skill, step 3), and BRIEF.md plans
     these five. None falls in the first 10 minutes: the longest gaps are 00:00–10:02 (S01 to the
     middle of S06) and 15:43–21:43.
   - **Follow-along pauses:** separately, 14 spoken "Pause …" lines tell the viewer to stop and run a
     step, from "Pause and do both, in your course folder." (03:41.3) to "Pause and tear down now, so
     port 8000 is free next time." (29:34.1). They are not ponders.
   - **Recap** ✔: S16 answers the four opening questions in speech, "An embedding is a direction for
     meaning…" (30:15.5–30:30.2), asks five test-yourself questions (30:30.5–30:56.3) and points to
     the answers and the study guide (30:56.6–31:05.6). Part 1 closes on "The top lane is done: the
     index is built. In part 2, we ask it questions." (18:03.5–18:08.5) and part 2 reopens with a
     one-line recap (18:09.9).
   - **Open question for Conny (as for L03 and L04):** does the series format, five ponders plus a
     spoken recap and five questions, satisfy this gate for AC215?
4. **Narration written for the ear, with word-anchored cues** ✔.
   - **Spoken style:** script.md's conventions apply: commands, flags and paths are said in words
     ("dash dash chunk", "chunk type char split", "slash app"), versions that will change are said
     "at the time of recording", no `'s` after a digit, every sentence under 30 words.
   - **Size:** 140 SAY lines and 4,335 words, identical to the 140 narration blocks in the renders
     (`measured.json` `narration`). Kokoro `af_heart` at speed 0.9 in all 16 scenes. Pace 139.3 wpm
     over the runtime, 151.3 wpm over voiced time (28:39.6, 92.1 % of the runtime).
   - **Anchors:** 617 `vo.wait_until` calls across the 16 scene files (23 in S07 to 54 in S09; 6 take
     a variable instead of a literal phrase). The 16 1080p60 render logs have 0 "anchor not found"
     warnings.
   - **Ear fixes after the draft:** "lecture 4's three gates" (the possessive was swallowed) became
     "Remember the three gates from lecture 4" (04:13.9); the spoken numbers in S08, S11 and S12 got
     their own sentences so a voice mark starts their cues ("24 rows of 256 numbers." 15:16.7;
     "0.57, 0.77, 0.43, 0.93." 19:49.6; "Their distances run from 0.28 to 0.31." 22:29.8); "cents"
     (which the QA's ASR heard as "sense") became "a few cents" (14:53.9); "the function the chunker is handed" became
     "the function handed to the chunker" (26:28.8); the new "Our chat" was phonemized and checked by
     ASR not to be heard as "a chat". Tolminc is respelled "tole-mints" in the lexicon.
   - **Caveat:** inside a sentence, cue boundaries are still timed by displayed characters, so a few
     continuation cues appear about 1 s before their words ("Open", item 9).
5. **Simulated-target-viewer QA over the full draft** ✔.
   - Seven watchers reviewed the 480p draft. Two were simulated target viewers ("newcomer", one per
     part): agents that read the draft's contact sheets, pulled frames and read the English `.srt`
     with the README open, step by step. Neither played the draft or listened to it.
   - They reported 71 timestamped findings: 0 must, 41 should and 30 nit; the two newcomers reported
     30 of them.
   - 40 of the 41 shoulds are fixed and were verified on fresh 480p or 720p renders; the one open
     should (mid-sentence cue timing) is a shared-toolkit item that the episode works around where
     it is worst. 27 of the 30 nits are fixed (one by a scene workaround); three shared-code nits are
     open. Details under "Whole-video QA".
6. **Measured checks** ✔. The numbers are under "Verified (final render)" (`measured.json`).
   - **Duration:** 31:07.4 (1867.406 s), inside the series' 25–35 min; parts 18:10.0 and 12:57.5.
   - **Loudness:** −16.1 LUFS integrated, LRA 2.3–2.4 LU and true peak −2.8 dBTP in all four MP4s;
     the build's target is −16 LUFS with true peak at or below −1.5 dBTP.
   - **Caption bounds:** in the zh-en copy every one of the 510 cues is one Chinese line over one
     English line (WrapStyle 2, one `\N` per Dialogue line), in the band under the picture (Chinese
     glyphs y 992–1029, English y 1039–1062; the picture is scaled to 1670×938 at the top). At 23
     command-on-screen frames the picture's lowest content is at y 882 or above, so no subtitle
     covers a command.
   - **Music balance:** does not apply. L05, like L02–L04, has no score: `video.yaml` has no `music:`
     key.
   - **Subtitle sync:** the one measured weakness ("Open", item 9).

   **Human review:** the series waiver below stands in for a listening sign-off.

   Listening sign-off: waived by Conny for the AC215 series (Explainer_Videos#29, 2026-10-15): 「不需要，我现在对视频质量很满意的」 — no human listened to this cut; the ASR round trip below is the substitute.

   The ASR round trip ran on this cut (the 23:11 clean cut; the zh-en copy carries bit-identical
   audio), so it covers every re-voiced line.

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
  item 11 under "Final-cut checks").
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
cues; the splitter itself is unchanged (toolkit PR), and the final ASR still finds four continuation
cues about 1 s early ("Open", item 9).

**The nits: 27 of 30 fixed (one by a scene workaround), three open.** Examples of the fixes: S02's
rule card no longer says "256 numbers" before S08 explains them; S04's tag no longer shows a scene
number ("· S09" → "· Load, step 3"); S05's three version chips name their sources; S09's erratum tag
no longer turns into a red blob; S10 and S12 mark the cut `--get` row with a grey "…"; S13's last
cards hold 1 s longer; S15's underlines clear the next row and its closing row shows three chips for
"three more"; S16's Q1 picture no longer lights the shared embedding box and database at "share"
(the flag chips stay on their lanes, as SHOW asks; final 30:36) and its ticks sit beside the chips;
S16's WARN lines are word-folded (final frame 28:57); the S09/S10 repeat "asks it questions" became "Part 2 puts it to work."
(final 18:13.8); "a few cents" and "handed to the chunker" (gate 4). Open, all in shared code:
- **Terminal scroll over the title bar** (`Terminal._make_room`, `explainer/devops.py`; draft 16:53
  and 12:17). S07 now fades its rows in place; the toolkit is unchanged and the final visual pass
  still caught it twice ("Open", item 15).
- **`_split_like` cuts the S08 step-1 command between two bilingual cues** (draft 14:01). Still in
  the final cut ("Open", item 12).
- **A tag pinned beside a terminal row is taller than the row pitch** (`devops.tag()` 0.465 against
  0.403). The final tag check found S11's cost tag 1–2 px above the next row's ascenders ("Open",
  item 7).

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
    "a prefix the model is trained…" (left to the toolkit; it is "Open", item 9); the shared
    `beside()`/`_make_room`/`_split_like`/spoken-length items (toolkit, own PR); S06's seam copies
    crossing the 8-row strip, S03's re-flowed `ls` (needs a 65-column capture), S16's "your edit"
    box 0.9 s after its anchor, and S11's repeated English line (intended `en_display`).

## Final-cut checks (1080p60, 2026-10-20)

Five agent checks of the stitched deliverables. No human watched or listened.

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
  beat, no slide picture by design); T02 and T08 are "Open", items 2 and 3.
- **New defect:** eight tag swaps double-expose for 0.4–1.3 s ("Open", item 1). S02's sequential
  swap at 01:57.2 is clean.
- **The 11 review-bot items, verified on frames:** S03's extra tag sits on the "Docker version
  29.8.2" output row (03:20.3–03:34.0); S04's box frames exactly `112.26MB` (06:44.6–06:55.4); S08's
  error rows leave before the second `--embed` (14:48.1–15:02.2); S09's recursive load starts in a
  cleared terminal (17:11.4); S11's cost tag covers no text (but see "Open", item 7); S11's strip is
  cleared (20:58.8–21:17.0); S13's tracker captions fade, its chat window morphs as one chrome
  (25:14.2–25:16.2) and only "line 372" turns yellow (25:25.2); S14's shrunk strip stays TEAL
  (26:47.7–27:08.3); and the shared fixes hold: tracker changes cross-fade with no scrambled letters
  and no fly-in (S06, S09, S10, S12, S14, S16; largest single-frame share 0.28), S16's compose view
  keeps every label inside its box (`docker-volumes/` about 16 px inside the laptop box), and the
  pink lane pulse never crosses the prompt card (19:35.2–19:36.2, 30:35.9).
- **Side finding:** S16's section switch to "Agents (L06)" overlaps old and new tracker headers for
  about 0.25 s (29:57.1–29:57.3; "Open", item 8).

**ASR round trip, the substitute for a listen** (`report-asr.md`; `asr.json`,
`asr_words_base.en.json`, `vad.json`, `residual.json`, `lag.json`, `clips_turbo*.json`,
`onset_energy.json`, `clips/`).
- **Files:** the clean cut against `.srt` (byte-identical to `f466f8e`); the zh-en copy has the same
  audio packets (MD5 `1083284a56edd28d31acb19ec833801e`, `audio_md5.txt`), so the result covers the
  Bilibili asset.
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
  0.70 s); four of them appear 1.0–1.6 s before their audio ("Open", item 9).

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
- **Burned subtitles:** all pass (see gate 6); "▶ your turn" chips sit 2–3 px above the next
  terminal line at 10:42 and 11:57 without touching (`visual_pass/frames/zoom4x_0717.00_yourturn_chip.png`).
- **Findings:** one new defect and two cosmetic ones ("Open", items 15–17).

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
- **Found:** 1 medium, 2 low and 2 nits ("Open", items 10–14). By design: cue 459 keeps the Chester
  sentence in English on both lines.
- **For information (soft subtitles only):** the single-language `.srt` and `.zh.srt` break
  `python cli.py --X --chunk_type char-split` across two lines at the flag boundary (`.srt` cues 174,
  230, 272, 339 at 10:24.7, 14:09.0, 16:41.7, 20:33.0; `.zh.srt` 139, 187, 221, 276), the least bad
  place for a command longer than one line. The burned asset is not affected.

**Measured** (`report-measured.md`; `measured.json`, logs and scripts in `measured_v2/`). Its
numbers are under "Verified (final render)"; its findings are "Open", items 18–22.

## Open in the final cut (for the coordinator; fix round 1 runs in parallel)

Every item is open in the reviewed cut, except item 18, which concerned stray files beside it and is
done. "Fix round 1" names the planned fix (`/root/ac215-backup/args/l05-fix1.json`); "not planned"
says why it was left.

**Lecture-slide tags**

1. **Tag swaps double-expose** (`report-tags.md`; `tags/swaps/swaps_sheet.png`, `tags/swaps/swap_*.png`).
   `lref_swap` in `common.py`, and inline swaps in `s01_hook.py:~494` and
   `s15_advanced.py:~470/505/565`, fade the old tag out and the new one in at the same time; both
   texts show at once, and where the widths differ the overlay reads as garbled text ("Lecture 55 ·
   slides A86 A17"):

   | swap | time | mid-swap look |
   |---|---|---|
   | S01 A6–A7 → A8–A10 | 00:42.3–00:43.1 | garbled |
   | S08 A24–A28 → A40–A43 | 13:13.1–13:13.6 | numbers doubled |
   | S08 A40–A43 → A44–A47 | 13:28.1–13:28.6 | numbers doubled |
   | S11 A39 → A48–A53 | 19:46.1–19:46.5 | garbled |
   | S13 A57–A59 → A61–A62 | 24:22.1–24:22.5 | numbers doubled |
   | S15 B6–B10 → B36–B39 | 27:38.6–27:39.9 | garbled |
   | S15 B36–B39 → B42–B48 | 27:51.9–27:53.1 | numbers doubled |
   | S15 B42–B48 → B51–B65 | 28:21.1–28:22.3 | numbers doubled |

   Fix round 1 (SW, S01, S15): make every swap sequential, old out then new in, as S02 does
   (`s02_map.py:242`), with the same total run time.
2. **T02, S01: the A8–A10 tag leaves at "Or let a librarian" (00:49.7–00:50.3)**, before road 3
   (RAG, slide A10) is drawn, so A10's picture never shares the screen with its tag. Fix round 1
   (S01): keep the tag until road 3 is drawn, or cite A8–A9.
3. **T08, S06: the A19–A22 tag ("why chunk") stays about 58 s past its beat** (09:09.3–10:25.4),
   through the visualizer, the 350/20 ruler, the ponder and the count to 24; the script names A19–A22
   for beat 0 only. Fix round 1 (S06): fade it out at the end of beat 0 (about 09:26).
4. **T09, S06 (minor): the B14–B15 tag lands 0.65 s before the previous `wc` output clears**
   (10:49.8–10:50.5). Fix round 1 (S06): let the output clear first.
5. **T12, S08 (minor): the picture fades out 0.5 s before the tag swaps** (13:12.6–13:13.1), so the
   tag sits on an empty stage. Not planned: 0.5 s, and the swap itself changes in item 1.
6. **T19, S11 (minor): the A48–A53 tag arrives about 0.9 s before its score column**, over the A39
   sphere (19:46.1–19:47.0). Not planned: under 1 s; the cited picture follows.
7. **S11's cost tag sits 1–2 px above the ascenders of "chunk_type char-split"** and looks as if it
   touches them (20:37.1–20:49.4; tag x 775–1763, y 262–326; text from y 328). It covers no text.
   Same cause as QA's open nit: `devops.tag()` is taller than the terminal row pitch. Not planned:
   shared toolkit (`bugbot/s11_costtag/zoom3_costtag_edge_1241.967.png`).
8. **Section switch double exposure:** S16's tracker header lifts off while "Agents (L06)" drops in;
   for about 0.25 s both read at once ("README › Run C…(L06)", 29:57.1–29:57.3,
   `bugbot/tracker_s16c/tracker_s16c_montage.png`). The shared-pass verifier saw the same in S03
   (*preview* about 03:46.6 and 04:46.7). Not planned: `switch_section()` is designed this way; it
   reads like the tag swaps of item 1, so the coordinator may want it in the same fix.

**Subtitles**

9. **Mid-sentence cue timing** (`report-asr.md` Finding 1; `onset_energy.json`, `lag.json`). Cues
   that continue a sentence after a number or long command appear before their audio, because
   inside a sentence the splitter times cues by displayed characters (`explainer/build.py`
   `split_cues`, about lines 267–316):

   | `.srt` cue | starts | text | speech starts (energy / VAD) |
   |---|---|---|---|
   | 225 | 13:48.71 | "a prefix the model is trained…" | +1.62 / +1.70 s |
   | 361 | 22:00.98 | "the word Italian keeps 64." | +1.16 / +1.30 s |
   | 231 | 14:13.92 | "the first call to Google." | +1.06 / +1.16 s |
   | 120 (borderline) | 06:46.33 | "mostly git history…" | +1.00 / +1.00 s |

   The same pattern under 1 s: cues 88 (04:54.10), 137 (07:44.53), 167 (09:43.37), 261 (16:01.57),
   294 (18:00.30), 395 (24:03.35) and 414 (25:04.04), +0.60 to +0.94 s. Fix round 1 (T1–T4): give
   the spoken numbers and the step-1 command their own sentences in S08 (twice), S12 and S04, so a
   voice mark starts each cue. Weighting the splitter by spoken length stays a toolkit change.
10. **Pairs F1 (medium): a verb is separated from its command** (`.zh-en.srt` cues 313/314,
    19:07.5–19:14.2; part 2 cues 19/20). Cue 313's Chinese ends on 「就先运行」 ("then first run")
    over "After a git pull that changes the dependencies or the Dockerfile,"; cue 314's Chinese
    line is only "docker compose build" over "run docker compose build first.". The splitter cut at
    the full-width colon. Fix round 1 (P1): reword `g2.yaml:50` so the cut falls at the comma (two
    rewordings tested in `pairs/splitter_tests.log`).
11. **Pairs F2 (low): the whole English sentence repeats under a Chinese sentence split in two**
    (cues 174/175 at 10:24.7, 336/337 at 20:33.0, 435/436 at 26:35.8; 436 is up only 1.27 s). The
    second cue's Chinese covers only part of the English under it. Fix round 1 (P2): shorten each
    Chinese sentence so it stays one cue.
12. **Pairs F3 (low): the step-1 `--embed` command is cut between its flags in both languages**
    (cues 230/231, 14:09.0–14:16.2): "Step 1: python cli.py --embed" / "--chunk_type char-split: the
    first call to Google." This is QA's open `_split_like` nit; the terminal shows the full command.
    Fix round 1 (T3): end the command sentence before "It's the first call to Google", with an
    `en_display` and a Chinese sentence short enough to stay one cue.
13. **Pairs F4 (nit): "finds none" and 没找到 sit one cue apart** (cues 115/116, 06:34.2–06:41.5).
    Fix round 1 (P4, optional): only if a rewording passes the splitter check.
14. **Pairs F5 (nit): "default" and 默认值 sit one cue apart** (cues 204/205, 12:24.5–12:31.3).
    Fix round 1 (P5): 「这个切分器的库默认最多重叠 200 个字符，README 从没提过。」 (tested).

**Picture**

15. **Visual F1 (new; low to medium; shared toolkit): scrolled-off terminal lines cross the title
    bar for 2–5 frames.** At 08:11.95 (S05) the `docker inspect … --format …` command and its
    `… -> /data` output cross "laptop · second terminal" (`visual_pass/frames/burn_0491.95.png`); at
    26:41.17–26:41.25 and 26:42.0 (S14) the semantic-split command crosses "container ·
    llm-rag-cli" (`visual_pass/frames/zoom_1601.18_scroll_ghost.png`). Every terminal scroll goes
    through `Terminal._make_room` (`explainer/devops.py:280-289`), so it probably happens elsewhere
    too; verifiers saw it on previews in S09 (*preview* about 17:02–17:06), S10 (18:46.7–18:47.1)
    and S11 (about 21:10.6). At speed it is a flicker; a paused frame shows garbled text. Fix round 1
    (SG): an L05 version of `_make_room` in `scenes/common.py` that fades the leaving lines in place
    within the same run time; `explainer/` stays untouched (toolkit fix separately).
16. **Visual F2 (low): S12's yellow underline under `n_results=10` (line 356) sits inside the top of
    line 357's pink box**, right above `where={"book"` (21:29.6–21:39.0; box edge y 490–492,
    underline y 500–503, lettering from y 509; `visual_pass/frames/zoom4x_1293.00_underline.png`).
    Fix round 1 (S12): move the underline clear of the box or shorten the box.
17. **Visual F3 (low): in the recap, a question's words cross each other for about 0.4 s as it
    dims**: Q2 at 30:43.4–30:43.8, Q3 at 30:49.3–30:49.8, Q5 at 30:56.7–30:57.1
    (`visual_pass/frames/s16_question_reflow_1842.8-1850.3.png` and the 30:57 tile of
    `sheets/sheet_39.png`). Fix round 1 (S16): dim without reflowing the text.

**Release and format**

18. **Stale 480p15 drafts in `output/` (done: removed at 07:38 UTC).** When measured (06:59),
    `output/` also held `ac215-l05-rag_480p15.mp4` (30:42.8, 102.1 MB), `_480p15.zh-en.mp4`
    (67.9 MB), `_part1_480p15.mp4` (59.4 MB, one decode error: a repeated timestamp) and
    `_part2_480p15.mp4` (42.8 MB), dated 2026-10-19 01:27–01:31. `tools/release_episode.py`
    (lines 147–149) takes every `.mp4`, `.srt` and `.ass` in its outputs folder, so a release run on
    this checkout would have uploaded them; the release workflow renders and stitches in a fresh
    runner, where they do not exist. Fix round 1 listed their deletion as a coordinator item; they
    are gone (the folder last changed at 07:38 UTC), `output/` now holds only the 31:07 deliverables,
    and the `build/qa/draft.mp4` link now dangles.
19. **Release prerequisites:** `video.yaml` has no `publish:` block (L02–L04 have one), so
    `release_episode.py` would refuse to run. Not in fix round 1's plan; the series skill requires it
    (`title_zh`, `description_zh`, `tags_zh`, `tid`) before the release, together with this record's
    sign-off line, which is now in place.
20. **Gate 3 shortfall:** five ponders against the aim of about 15.6. Not planned: it matches BRIEF.md
    and the series rule of 3–5; see gate 3, with its question for Conny.
21. **Narration over its budget:** 4,335 words against BRIEF.md's 3,900–4,300 (35 over); part 1 has
    2,530 against its plan of about 2,410 (5 % over). Not planned: the runtime, 31:07, is inside
    25–35 min.
22. **Burned copy's start (no visible effect):** the zh-en copy's video starts at 0.000 s, the clean
    cut's and the parts' at 0.021 s, and it has one more frame (112,042 against 112,041). Not
    planned: about one frame.

**Smaller nits noted by QA and finishing verifiers on previews** (not in fix round 1; each lasts
under about a second or is still legible; none was reported again by the final checks, which
sample every 3 s, but the four marked *final* were confirmed on single frames of the 31:07 cut for
this record, `verifier/nits_sheet.png`):
- S06: the two seam copies fly across the command rows for about 0.4 s each (*preview* 10:53.3 and
  10:55.2; *final* 10:53.5, the copy crosses the output rows).
- S09: the 0.55 s Indicate fills the Chroma cylinder green and the folder glyph yellow (*preview*
  17:41.6; neither carries text).
- S10: `Indicate` fills the `/data` window yellow (*preview* 18:31.1) and the `:8000` chip pink
  (18:33.7), so their labels cannot be read for a moment (*final* 18:31.05–18:31.15 and
  18:33.65–18:33.75: both labels unreadable); the grey note touches the "docker compose build" chip
  (19:12.6); the "?" badge comes 1.1 s after "does the index survive" (18:18.1).
- S12: during the card flight the id copies cross the staff tag, the terminal title and the ids rows
  (*preview* about 23:16.5; *final* 23:16.5, the overlapping ids read as garbled text).
- S16: the "your edit" box lands 0.9 s after "shows only your edit" (*preview* 29:14.2).

## Verified (final render)

Measured on 2026-10-20 (`measured.json`, re-run after the usage limit; ffprobe, a one-pass full
decode with `ebur128=peak=true` per file, run one at a time; logs in `measured_v2/full_*.log`,
summary in `measured_v2/chain_summary.txt`).

- **Deliverables:**

  | file | size | duration (container / video) | frames | kbps total (video / audio) | integrated | LRA | true peak | decode errors |
  |---|---|---|---|---|---|---|---|---|
  | `ac215-l05-rag.mp4` | 109.92 MB (109,917,887 B) | 1867.406 s (31:07.4) / 1867.350 s | 112,041 | 470.9 (283.4 / 175.8) | −16.1 LUFS | 2.4 LU | −2.8 dBTP | 0 |
  | `ac215-l05-rag.zh-en.mp4` (to Bilibili) | 108.39 MB (108,391,112 B) | 1867.406 s / 1867.367 s | 112,042 | 464.3 (276.9 / 175.8) | −16.1 LUFS | 2.4 LU | −2.8 dBTP | 0 |
  | `ac215-l05-rag_part1.mp4` | 63.31 MB (63,310,083 B) | 1089.993 s (18:10.0) / 1089.883 s | 65,393 | 464.7 (276.5 / 176.5) | −16.1 LUFS | 2.3 LU | −2.8 dBTP | 0 |
  | `ac215-l05-rag_part2.mp4` | 46.62 MB (46,616,965 B) | 777.528 s (12:57.5) / 777.467 s | 46,648 | 479.6 (293.1 / 174.9) | −16.1 LUFS | 2.4 LU | −2.8 dBTP | 0 |

  - **Format:** all four are 1920×1080 at a constant 60 fps, H.264 High yuv420p, with AAC-LC audio
    at 48 kHz stereo. Decoded frame counts match the header counts.
  - **Loudness:** the stitch normalizes to −16 LUFS with true peak at or below −1.5 dBTP, then
    limits at −3 dBFS; every file meets it with 1.3 dB of true-peak headroom to spare. The −2.8 dBTP
    peak is first reached at 03:11.8 (S02); the loudest 400 ms window is −9.9 LUFS at 07:49.2 (S05,
    speech after a pause) and the loudest short-term reading −14.2 LUFS at 14:30.4 (S08).
  - **The zh-en copy** carries audio bit-identical to the clean cut's (packet MD5
    `1083284a56edd28d31acb19ec833801e`); its picture is scaled to 1670×938 at the top with the
    subtitles in the band below, and matches the clean cut's frames when scaled the same way.
  - SHA-256 of each file is in `measured.json` `probes`.
- **Scenes and parts:**
  - 16 stitched scenes whose durations add up to 1867.350 s, exactly the full cut's video stream;
    each scene's stitched file, 1080p60 render and `events.json` have the same length, except S06's
    render, 5 ms (a third of a frame) shorter than its stitched segment.
  - Part 1 (S01–S09) + part 2 (S10–S16): 1089.993 + 777.528 = 1867.521 s against the full cut's
    1867.406 s (+0.115 s, inside ±0.5 s); the two video streams add up to exactly 1867.350 s.
- **Chapters:** `chapters.txt` has 16 entries in the order and with the titles of `video.yaml`'s
  scenes; each time is the rounded-down sum of the stitched scene durations (00:00, 01:40, 03:15,
  05:15, 07:19, 09:09, 11:21, 12:59, 15:56, 18:09, 19:34, 21:27, 23:31, 25:30, 27:23, 28:49). Both
  part files match too (part 2 counts from 18:09.883). `README.md`'s chapter list is copied from
  these files.
- **Subtitles:**

  | track | full | part 1 | part 2 | shortest / longest cue |
  |---|---|---|---|---|
  | `.srt` | 513 | 296 | 217 | 1.003 / 7.275 s |
  | `.zh.srt` | 423 | 240 | 183 | 1.218 / 8.576 s |
  | `.zh-en.srt` | 510 | 294 | 216 | 1.000 / 7.701 s |

  - Every track in all three cuts is numbered 1..N in order, with no overlaps, no empty cue and none
    under 0.8 s, all inside the runtime (the last cue ends at 31:05.607, 1.8 s before the end).
  - The part cues shifted to full time match the full files exactly.
  - `.zh-en.ass` has 510 Dialogue lines with the same text as `.zh-en.srt`, within 5 ms.
  - Three zh-en cues have no Chinese characters on their top line: 314 ("docker compose build",
    "Open", item 10), 324 (19:49.6, only the numbers "0.57、0.77、0.43、0.93") and 459 (the Chester
    sentence, by design).
- **Burned-subtitle layout:** Chinese at 50 px Noto Sans CJK SC (glyphs y 992–1029), English at 33 px
  grey with an outline (y 1039–1062); at most two lines everywhere. The widest lines are about
  1050 px (Chinese, cue at 00:20.2) and 1034 px (English, 13:28.1) by the visual pass's font-metric
  estimate of all 510 cues (`visual_pass/subs/sub_measure.json`), which uses libass's size rule (a
  50 px style is 50 px from ascender to descender, an em of about 34.5 px). Frames agree: the
  00:20.2 line's ink spans x 443–1476 (1033 px; `writer/zhen_cue7_t21.5.png`, re-measured) and the
  13:28.1 English line's x 445–1473 (1028 px; `verifier/zhen_810.0.png`). The pairing check's
  1500 px for the same Chinese line took 50 px as the em, which overstates by that 1.448 ratio; every
  line is inside the 1670 px picture width.
- **Narration and anchors:** 140 SAY lines, 4,335 words (part 1 2,530, part 2 1,805), identical to
  the rendered sidecars; 617 `wait_until` calls; 0 "anchor not found" in the 16 render logs, whose
  only warning is Manim's "Some options were not used".
- **Ponders and recap:** the five ponder windows and the recap beats as in gate 3; one frame from the
  middle of each timer, from the zh-en copy, shows the card with its bar about half drained
  (`measured_v2/ponder_frames/ponder_sheet.png`).
- **Committed files match the cut:** the subtitles, `.ass` files, chapter files and transcript in
  `output/` are byte-identical to `f466f8e` and to HEAD `40bae73`; the episode and toolkit diff from
  `f466f8e` to HEAD was empty when measured. Re-checked for this record at about 08:00 UTC: `output/`
  still has no diff from `f466f8e` (HEAD `e926662`), and the four MP4s' SHA-256 equal the ones in
  `measured.json`. An audio-only `ebur128=peak=true` pass over the zh-en copy gives the same
  −16.1 LUFS, LRA 2.4 LU and −2.8 dBTP (`verifier/ebur128_zhen_audio.log`).
- **Lecture-slide tags:** 30 tags, all worded correctly, cited picture on screen except T02 and T08
  (T04 by design), none at a scene end, none overlapped (tag check above).
- **Narration heard by ASR:** no mispronunciation or swallowed word in 513 cues (ASR round trip
  above).
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

- **No human has watched or listened to this cut.** The listening sign-off is waived for the series
  (gate 6). The ASR round trip shows that a machine can understand the narration; it does not judge
  pacing, tone or how natural the voice sounds. The connected-speech passages under "Final-cut
  checks" (cues 157, 185, 286, 311, 448, 103, 304, 396) and "Tolminc" were judged from transcripts
  and phonemes, not by ear.
- **Agents alone reviewed the Chinese and bilingual subtitles:** the QA subtitle watcher, the
  narration/subtitle fixer, the first finishing pass's proofread, the verifiers and the final
  pairing check. No native-speaker human has read them, and the pairing check left five items to fix
  ("Open", items 10–14). In the final cut the zh-only `.zh.srt` was checked for structure (counts,
  timing, overlaps) and searched for the QA's line-break terms, but not read cue by cue again.
- **The visual review sampled the video.** One frame every 3 s, targeted frames, a motion scan and a
  tag-region scan at 30 fps; not continuous playback of the whole frame. A defect shorter than 3 s
  between samples can be missed: the terminal scroll-over was caught at only two of the scrolls
  ("Open", item 15), and the checks did not look for the smaller verifier nits again (four of them
  were confirmed on single frames for this record; the rest were not looked at).
- **The part files were not visually sampled.** They were decoded and measured, and their subtitles
  and chapters compared with the full files.
- **The QA and finishing fixes were verified on 480p and 720p preview renders, not one by one in
  this cut.** In the final cut they were checked only by the five checks (which re-verified the 11
  review-bot items, the shared `common.py` fixes and every slide tag, and read every 3 s) and by the
  frames looked at for this record (`sheets/sheet_37.png`, `sheet_39.png`, frames at 00:03, 00:14.5,
  00:21.5 and 13:30, the first 14 s, and the four nit frames in `verifier/`).
- **The burned subtitles were not read back by text recognition.** The pairing check compared its 14
  flagged-cue crops and 2 full frames with the subtitle files; the visual pass's 23 spot checks
  looked at placement, not text. Subtitle widths are font-metric estimates checked against ink on
  four frames (gate 6 note).
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
- **The released files will be a different render.** Everything here is about the local stitch of
  2026-10-19 23:11–23:31 UTC. Fix round 1 changes every scene with a terminal scroll or a tag swap
  and re-renders all 16; the release workflow then re-renders with the pinned engine and writes
  `<id>.validation.json`, which does not exist yet. Duration, frames, loudness, true peak, cue
  counts and chapters must be re-checked on those files, and this record updated.
