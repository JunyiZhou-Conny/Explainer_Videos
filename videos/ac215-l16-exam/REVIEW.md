# Review — AC215 L16 System Tradeoffs, with L10 networking (exam edition)

Exam edition for Quiz 4 (Tuesday 2026-11-03), issue #80. The final cut is 16:52 (1012.611 s), 1080p60, one
part, English narration (Kokoro af_heart 0.9), with Chinese and bilingual subtitles. It is a concept-first
explainer of Lecture 16 that also covers the Lecture 10 quiz items: no README walkthrough, no captures. Code
panels quote `assets/source/` (cheese-app-v0 @ `cb6fb94`, cheese-app-v2 @ `14f2a14`), and invented examples are
tagged `illustration`. Lecture tags cite Lecture 10 or Lecture 16 slides.

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
1. **Hook:** S01 "Launch day: three alarms" opens on broken things: on launch day the model-API calls time out
   while the database answers, the Predict button fails in every visitor's browser, new replicas hit "too many
   connections", and the production key sits inside the container image.
2. **Mechanisms:** each core idea is an animated diagram:
   - localhost vs a private address vs the public front door (laptop, `-p` tunnel, DNS → ALB) (S02);
   - VPC, subnets, route tables and the NAT path, including what fails when NAT is down (S03);
   - the browser outside the VPC: why browser code must call the public API endpoint (S04);
   - one image on a conveyor through dev/staging/prod, with values and secrets supplied at startup (S05);
   - autoscaling bounded by the database connection budget (S06);
   - relational plus vectors in one database: PostgreSQL + pgvector vs a second database (S07).
3. **Ponders and recap:** three quiz-style multiple-choice ponders, each with a 10 s timer and an answer that
   explains every wrong option (answers C, D, B, checked against script and scene code), then a seven-rule recap
   (S08). Three ponders in 16:52 is below one per 2 minutes; it is inside Conny's 2026-10-21 decision to keep 3–5
   per lecture (「我觉得可以保留现在的密度」).
4. **Narration:** 74 SAY blocks, 2,299 words (146 wpm over voiced time). Every `wait_until` anchor resolved
   (264 call sites).
5. **Simulated-viewer QA:** done only as the final-cut checks. There was no separate newcomer watcher. The visual
   pass read all 22 contact sheets (one frame every 3 s) plus full-size frames and 10 subtitle spot checks, with
   timestamped findings.
6. **Measured checks** (`build/final-review/measured.json`):
   - both MP4s decode with 0 errors;
   - −16.1 LUFS integrated, LRA 2.1 LU, true peak −2.5 dBFS;
   - `.srt` 278 cues, last cue ends 1010.606 s, shortest 1.000 s; no overlaps;
   - chapters match the scenes; the scene renders add up to the cut's 60,753 frames.

   Listening sign-off: waived by Conny for the AC215 series (Explainer_Videos#29, 2026-10-15): 「不需要，我现在对视频质量很满意的」 — no human listened to this cut; the ASR round trip below is the substitute.
   Review moments optional since 2026-10-22 (AGENTS.md): 「我大概率是不会进行审片的，因为我觉得做得已经非常好了，就让bugbot来检查就好了」

## Final-cut checks
| Check | Result |
|---|---|
| Lecture tags | All 25 correct, no overlap, none left at a scene end. One should-fix overstay, accepted (A1). |
| Subtitle pairs | All 266 bilingual cues paired correctly; no swapped clauses; widest lines ~1015 px (zh) / ~987 px (en) of 1840. One repeated English line, accepted (A3). |
| Visual | No must-fix. Eight minor cosmetic items, accepted (A2). |
| ASR round trip | No mispronounced terms, no swallowed words, no cue whose audio starts late. One taste note (A4). |
| Measured | No must-fix (above). |

## Accepted for release (with reason)
None of these changes what a viewer learns; a fix round would have cost the quiz deadline.
- **A1, 10:20–10:29 (S05):** the "Lecture 10 · slide 42" tag stays ~9 s after its `docker run` picture leaves.
- **A2, cosmetic:**
  - an orphan red "inbound" label for ~3 s at 8:57;
  - packets grazing nearby labels in S03 (5:03, 5:39);
  - a route-table heading over a 25 %-opacity background label (4:24);
  - text touching the laptop frame (7:45);
  - a tight fit in the connection-budget grid (12:06–13:02);
  - capability chips touching (14:42);
  - the first recap row sitting high (15:42);
  - one context tag worded "lecture's picture" instead of "the lecture's picture" (8:09).
- **A3, cue 258–259 (16:23):** the whole English sentence stays up under both Chinese halves. The toolkit does
  this on purpose when the line fits; it is the only place in the video.
- **A4:** Kokoro says "PostgreSQL" as "Postgre-S-Q-L", a common, recognisable variant of "Post-gres-Q-L".

## Not claimed
- No human listened to the cut.
- No per-scene critic and no whole-video QA ran before the final-cut checks.
- There is no background music in this cut (none is configured for the exam editions), so no music balance was
  measured.
