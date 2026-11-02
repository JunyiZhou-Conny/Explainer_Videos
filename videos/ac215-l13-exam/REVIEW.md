# Review — AC215 L13 Advanced Training Workflows (exam edition)

Exam edition for Quiz 4 (Tuesday 2026-11-03), issue #77. The final cut is 15:14 (914.408 s), 1080p60, one
part, English narration (Kokoro af_heart 0.9), with Chinese and bilingual subtitles. It is a concept-first
explainer: no README walkthrough, no captures. Code panels quote `assets/source/` (model-training @ `b9aee1c`,
Colab cell 38), and invented examples are tagged `illustration`.

## How it was made (shorter than a follow-along)
1. **Design and script:** brief → script → two independent reviews (accuracy against slides and repo; exam
   pedagogy and spoken flow) → merge.
2. **Chinese subtitles:** glossary, translation and proofread.
3. **Scenes:** one builder per scene, each self-critiquing (`explainer.check` OK, previews read). The usual
   per-scene critic and 480p whole-video QA were skipped to make the quiz deadline.
4. **Final cut:** rendered at 1080p and stitched with `--burn`.
5. **QA:** five independent checks on the final cut (tags, ASR round trip, visual pass, subtitle pairs,
   measured), reports in `build/final-review/report-*.md`.

## Content gates
1. **Hook:** S01 "The run with no curves" opens on a broken W&B run (config logged, no loss curves) and asks why.
2. **Mechanisms:** each core idea is an animated diagram:
   - W&B run ledger with the `wandb.run` pointer (S02–S03);
   - what pip installs vs what the package carries (S04);
   - one machine vs many: MirroredStrategy islands and MultiWorker (S05);
   - the global-batch splitter (S06);
   - a request handler vs a durable job (S07).
3. **Ponders and recap:** three new quiz-style multiple-choice ponders, each with a timer and an answer that
   explains every wrong option, then a six-rule recap (S08). That is one ponder every ~5 min, which passes by
   Conny's 2026-10-21 decision to keep 3–5 per lecture (「我觉得可以保留现在的密度」).
4. **Narration:** 73 SAY lines, 2,264 words. Every `wait_until` anchor resolved (no "anchor not found" in the
   render logs).
5. **Simulated-viewer QA:** done only as the final-cut checks. There was no separate newcomer watcher. The visual
   pass read all 20 contact sheets (one frame every 3 s) plus ~35 full frames, with timestamped findings.
6. **Measured checks** (`build/final-review/measured.json`):
   - both MP4s decode with 0 errors;
   - −16.0 LUFS integrated, LRA 2.3 LU, true peak −2.8 dBFS;
   - `.srt` 257 cues, last cue ends 912.377 s, shortest 1.003 s;
   - chapters match the scenes.

   Listening sign-off: waived by Conny for the AC215 series (Explainer_Videos#29, 2026-10-15): 「不需要，我现在对视频质量很满意的」 — no human listened to this cut; the ASR round trip below is the substitute.
   Review moments optional since 2026-10-22 (AGENTS.md): 「我大概率是不会进行审片的，因为我觉得做得已经非常好了，就让bugbot来检查就好了」

## Final-cut checks
| Check | Result |
|---|---|
| Lecture tags | All 17 correct, on their pictures, none left at a scene end, no overlap. No must-fix. |
| Subtitle pairs | All 241 bilingual cues paired correctly; no swapped clauses. No must-fix. |
| Visual | No must-fix. One should-fix, accepted (below). |
| ASR round trip | No mispronounced or swallowed word. Low-match cues are code identifiers spoken as words (`MultiWorkerMirroredStrategy`, `TF_CONFIG`, `wandb.run`, `install_requires`). |
| Measured | No must-fix (above). |

## Accepted for release (with reason)
- **A1, 5:08–5:12 (S03):** the green loss/accuracy curves draw while the grey "no data logged" placeholder is
  still visible, for ~3 s. It is cosmetic, and the narration makes the change clear. A re-render would have cost
  the quiz deadline.
- **A2:** ASR heard "wandb dot init" as "wand be dot in air". This is the recogniser's spelling of a spoken
  identifier; the on-screen text and subtitles are exact.

## Not claimed
- No human listened to the cut.
- No per-scene critic and no whole-video QA ran before the final-cut checks.
- The W&B behaviour (callback writes to the active run; `wandb.log` after `finish` raises) was read from the
  wandb 0.15.11 source the repo pins, not run.
