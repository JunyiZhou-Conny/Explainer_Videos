# Review — AC215 L14 Serverless Deployment (exam edition)

Exam edition for Quiz 4 (Tuesday 2026-11-03), issue #78. The final cut is 15:20 (920.218 s), 1080p60, one
part, English narration (Kokoro af_heart 0.9), with Chinese and bilingual subtitles. It is a concept-first
explainer: no README walkthrough, no captures. Code panels quote `assets/source/` (serverless-deployment @
`46cc62f`, model-deployment @ `cf0b7c7`), and invented examples are tagged `illustration`. The serving-signature
half cites Lecture 15 slides 11–17, which is where the course teaches it.

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
1. **Hook:** S01 "A job that never finishes" opens on a broken thing: a Cloud Run job that never exits and is
   stopped at its timeout.
2. **Mechanisms:** each core idea is an animated diagram:
   - the service vs job lifecycle (request → response vs run → exit status) (S02);
   - two billing meters, function vs VM, as idle time grows (S03);
   - the 2×2 of what you hand over: code file vs container, VM vs serverless (S04);
   - who may call the service vs the identity it runs as (S05);
   - preprocessing on every client vs once at the endpoint, with a rollback (S06);
   - the serving signature: `serve` = preprocess, then model (S07).
3. **Ponders and recap:** three quiz-style multiple-choice ponders, each with a timer and an answer that explains
   every wrong option, plus one one-line ponder (S06), then a seven-rule recap (S08). Four ponders in 15:20 is
   below one per 2 minutes; it is inside Conny's 2026-10-21 decision to keep 3–5 per lecture
   (「我觉得可以保留现在的密度」).
4. **Narration:** 66 SAY blocks, 2,155 words (157 wpm over voiced time). Every `wait_until` anchor resolved
   (255 call sites, 262 runs).
5. **Simulated-viewer QA:** done only as the final-cut checks. There was no separate newcomer watcher. The visual
   pass read all 20 contact sheets (one frame every 3 s) plus 18 full frames and 10 subtitle spot checks, with
   timestamped findings.
6. **Measured checks** (`build/final-review/measured.json`):
   - both MP4s decode with 0 errors;
   - −16.1 LUFS integrated, LRA 2.2 LU, true peak −2.7 dBFS;
   - `.srt` 254 cues, last cue ends 918.012 s, shortest 1.000 s; no cue during a ponder timer;
   - chapters match the scenes; scene durations sum to the cut (920.150 s video stream).

   Listening sign-off: waived by Conny for the AC215 series (Explainer_Videos#29, 2026-10-15): 「不需要，我现在对视频质量很满意的」 — no human listened to this cut; the ASR round trip below is the substitute.
   Review moments optional since 2026-10-22 (AGENTS.md): 「我大概率是不会进行审片的，因为我觉得做得已经非常好了，就让bugbot来检查就好了」

## Final-cut checks
| Check | Result |
|---|---|
| Lecture tags | All 14 correct, on their pictures, none left at a scene end, no overlap. No must-fix. |
| Subtitle pairs | All 250 bilingual cues paired correctly; no swapped clauses; widest lines 1101 px (en) / 1026 px (zh) of 1840. No must-fix. |
| Visual | No must-fix. Four should-fix: one fixed (F1), three accepted (A1–A3). |
| ASR round trip | One real defect, fixed (F2). No swallowed words, no cue whose audio starts more than 1 s late. Other differences are recogniser noise (identifiers, homophones, cue boundaries). |
| Measured | No must-fix (above). |

## Fixed after the checks (in the source; the release re-renders from it)
- **F1, 8:33–8:43 (S05):** the README panel stopped mid-sentence ("…to attach it. This is"). It now quotes
  lines 432–434, so the sentence ends; a medium-quality preview at the panel's time shows it inside the band.
- **F2, "preprocess" (19 places, S06–S08):** Kokoro said "prih-PRAH-sess". The toolkit lexicon now has whole-word
  entries for preprocess / preprocesses / preprocessing / Preprocessing / preprocess_image (#83, merged).

The local QA cut predates F1 and F2; the release, rendered on CI from main's toolkit and this source, carries
both.

## Accepted for release (with reason)
- **A1, 4:07–4:19 (S03):** the two billing meters hold still for ~12 s while the narration says the VM meter
  grows; the VM bar is already nearly full. The comparison is still legible, and a re-timing would have cost the
  quiz deadline.
- **A2, 12:36–12:44 (S07):** ~8 s of a dimmed, unchanged diagram while P3's question is read, before its card
  and timer.
- **A3, recap (S08):** each rule row holds still for 4–8 s while it is read.
- The image name `cgumb/ac215-translation-demo:…` on screen is the course repo's own registry handle
  (BRIEF.md), not a person's name; the instructor's name appears nowhere in the deliverables.

## Not claimed
- No human listened to the cut.
- No per-scene critic and no whole-video QA ran before the final-cut checks.
- F1 and F2 were checked on a preview frame and on phonemes respectively, not on a re-rendered final cut.
