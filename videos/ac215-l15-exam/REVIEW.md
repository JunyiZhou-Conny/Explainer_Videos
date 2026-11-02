# Review — AC215 L15 ML Workflows with Vertex AI (exam edition)

Exam edition for Quiz 4 (Tuesday 2026-11-03), issue #79. The final cut is 13:23 (803.721 s), 1080p60, one
part, English narration (Kokoro af_heart 0.9), with Chinese and bilingual subtitles. It is a concept-first
explainer: no README walkthrough, no captures. Code panels quote `assets/source/` (ml-workflow @ `3730009`,
model-deployment @ `cf0b7c7`, ml-workflow-aws @ `f165c6e`), and invented examples are tagged `illustration`.

## How it was made (shorter than a follow-along)
1. **Design and script:** brief → script → two independent reviews (accuracy against slides and repo; exam
   pedagogy and spoken flow) → merge.
2. **Chinese subtitles:** glossary, translation and proofread.
3. **Scenes:** one builder per scene, each self-critiquing (`explainer.check` OK, previews read). The usual
   per-scene critic and 480p whole-video QA were skipped to make the quiz deadline.
4. **Final cut:** rendered at 1080p and stitched; the bilingual copy burned with the build's own command.
5. **QA:** five independent checks on the final cut (tags, ASR round trip, visual pass, subtitle pairs,
   measured), reports in `build/final-review/report-*.md`.

## Content gates
1. **Hook:** S01 "The 2 a.m. race" opens on a broken thing: preparation (1:00) runs long, training starts at 2:00
   on a half-written file anyway, every job exits 0, and the endpoint serves a model trained on half the data.
2. **Mechanisms:** each core idea is an animated diagram:
   - a pipeline as a DAG: tasks are nodes, data dependencies are edges (S02);
   - `task.output` as the wire that both passes the value and creates the edge (S03);
   - maximum safe overlap: fan-out and fan-in on a DAG and its Gantt chart (S04);
   - edges vs clocks: cron offsets and background jobs race, `.after()` and outputs do not (S05);
   - registry → endpoint → deploy → predict, with the serving signature (S06);
   - the Cheese App pipeline and the same DAG on AWS (S07).
3. **Ponders and recap:** three quiz-style multiple-choice ponders, each with a timer and an answer that explains
   every wrong option, then a seven-rule recap (S08). Three ponders in 13:23 is below one per 2 minutes; it is
   inside Conny's 2026-10-21 decision to keep 3–5 per lecture (「我觉得可以保留现在的密度」).
4. **Narration:** 76 SAY blocks, 1,950 words (157 wpm over voiced time). Every `wait_until` anchor resolved
   (266 call sites).
5. **Simulated-viewer QA:** done only as the final-cut checks. There was no separate newcomer watcher. The visual
   pass read all 17 contact sheets (one frame every 3 s) plus 13 full frames for the burned subtitles, with
   timestamped findings.
6. **Measured checks** (`build/final-review/measured.json`):
   - both MP4s decode with 0 errors;
   - −16.1 LUFS integrated, LRA 2.2 LU, true peak −2.7 dBTP;
   - `.srt` 238 cues, last cue ends 801.551 s, shortest 1.000 s; no overlaps;
   - chapters match the scenes; scene durations sum to the cut (803.700 s vs 803.721 s).

   Listening sign-off: waived by Conny for the AC215 series (Explainer_Videos#29, 2026-10-15): 「不需要，我现在对视频质量很满意的」 — no human listened to this cut; the ASR round trip below is the substitute.
   Review moments optional since 2026-10-22 (AGENTS.md): 「我大概率是不会进行审片的，因为我觉得做得已经非常好了，就让bugbot来检查就好了」

## Final-cut checks
| Check | Result |
|---|---|
| Lecture tags | All 21 correct and readable, none left at a scene end, no overlap. Three should-fix overstays, accepted (A1). |
| Subtitle pairs | No swapped clauses. One misaligned pair, fixed (F1). |
| Visual | No must-fix. Low-motion holds and three cosmetic items, accepted (A2, A3). |
| ASR round trip | No swallowed words, no cue whose audio starts more than 1 s late. Two mispronunciations, fixed in the lexicon (F2, F3). |
| Measured | No must-fix (above). |

## Fixed after the checks
- **F1, cues 156–157 (8:55):** 后台命令 sat in the Chinese of one cue and "background commands" in the English of
  the next. The zh clause split was moved to match; subtitles regenerated and the bilingual copy re-burned.
- **F2, "preprocess" (S05–S06):** Kokoro said "prih-PRAH-sess". The toolkit lexicon now has whole-word entries
  (#83, merged).
- **F3, "Keras" (9:31):** said "KEER-uhz", heard as "Kira's". Phrase entry "Keras export archive" in the toolkit
  lexicon (#85), the same approach as L13-exam's "that Keras holds".

The release renders on CI from main's toolkit, so it carries F2 and F3; the local QA cut predates them.

## Accepted for release (with reason)
- **A1, tag overstays (S03 ~76 s, S04 ~41 s, S05 ~64 s):** the grey slide tag stays after its picture leaves,
  over the ponder and takeaway. The script rule ("the tag stays until a SHOW changes it") allows it; changing it
  means re-rendering three scenes before the quiz.
- **A2, low-motion holds:** 20 stretches of 4–7.7 s (DAG definition, a ponder answer, the recap rows) with only
  highlights and ticks changing; the narration plays through each.
- **A3, cosmetic:** a 2×8 px stub left by each ponder timer; the registry → bucket arrow crossing the "t" of
  "bucket" (9:39–10:24); two highlight flashes of ~0.2 s.

## Not claimed
- No human listened to the cut.
- No per-scene critic and no whole-video QA ran before the final-cut checks.
- F2 and F3 were checked on phonemes, not on a re-rendered final cut.
