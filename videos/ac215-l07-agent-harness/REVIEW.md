# Review record: AC215 · Lecture 7 — LLM: Agents II: the agent harness

Follow-along of [dlops-io/agent-harness](https://github.com/dlops-io/agent-harness) `main` @ `e25dfe9` (the whole
README: Setup and verification, Acts 1–6, Evaluation, Additional Resources, Troubleshooting) and the course Colab
notebook "Agent Harness" (saved outputs only). The issue of record is Explainer_Videos#52. Claude Code cloud
sessions (Claude) produced it. Verified facts and unclaimed reviews are kept in separate sections.

- **Captures:** 2026-10-20, 20:17–20:24 UTC, on a fresh "laptop" with Docker Engine 29.8.2 and the tutorial's own
  image, **without an OpenAI key** (`ASSETS.md`).
- **QA draft:** the 480p draft (31:11, parts 13:44 + 17:27), committed in `a9db242` (2026-10-29 09:09 UTC).
- **Whole-video QA** (`/root/ac215-backup/tasks/wcf7p3z4u.output`, key `result`): seven watchers on that draft,
  a fixer and a verifier for each of the 16 scenes, and one narration/subtitle fixer. Committed in `f051156`
  (2026-10-30 06:30 UTC).
- **Finishing pass** (`/root/ac215-backup/tasks/w87jd5weh.output`, 8 agents): a plan, one text agent (11 items),
  and three code entries (`common.py`, S11, S09), each with a verifier. Committed in `60c7512` (07:07 UTC).
- **1080p60 renders:** all 16 scenes, render logs `build/logs/` dated 2026-10-30 07:12–07:52 UTC.
- **Final cut (the cut this record describes):** 31:21.75, parts 13:51.25 + 17:30.61; subtitles, chapters and
  transcript committed in `b3367b3` (08:35 UTC).
- **Final-cut checks:** five agent checks on 2026-10-30. The coordinator saved their returned text as
  `build/final-review/report-{tags,asr,visual,pairs,measured}.md`. All five reports exist and were read in full
  for this record. All five pass, with no blocking defect.
- **Coordinator decision (2026-10-30):** no fix round for this cut. Every finding in the five reports is accepted
  for release, and each is recorded below with its reason (minor, optional or by design).

**Conventions:**
- **Times** are mm:ss in the full cut (`output/ac215-l07-agent-harness.mp4`, 31:21.75), except in "Whole-video QA",
  which keeps the 480p draft's times (marked *draft*).
- **Cue numbers** name their file: `.srt` (502 cues), `.zh.srt` (429) or `.zh-en.srt` (497).
- **Evidence paths** are relative to `build/final-review/`, which is git-ignored and exists only in the producing
  session. A successor re-runs the checks to reproduce it.

## Content gates (AGENTS.md)

1. **Hook** ✔. S01 opens on a broken thing from the staff's saved Colab run, not on a value proposition.
   - One request ("12 guests in Pennsylvania, a $150 budget, no nuts…", 00:00.0) gets two answers from the same
     model and tools. The second claims 6,400 cents is "within a budget with the comma in the wrong place: a
     malformed number" (the on-screen `1,5000¢`, held 00:25.0–00:30.1).
   - The question: "Which of these would you let charge a customer's card?" (cue 8, 00:30.4).
   - **Payoff:** "Code checked the cart itself: …The cart was valid; only the sentence was garbled. Nothing checked
     the first answer's final cart." (from 00:38.7). Then the rule, "the model proposes; the harness decides"
     (cue 15, 00:54.0), which the whole video sorts output into and which the recap returns to (30:30.9).
2. **Intuition before formalism, with an animated mechanism for each core idea** ✔. `BRIEF.md` ("Visual set
   pieces") defines eight; each is animated with the commands it explains:
   - **V1, two columns → the action boundary:** the columns (00:54); slide 22's table built full screen in S05
     (lecture tag 05c, 08:51–09:05); a mini-map row lit per act in S06–S13; the table filled in S16 (30:16.0).
   - **V2, the loop, measured (S04):** model ↔ five tool paddles from the recorded trace, message cards and the
     GOLD token meter, "and the loop stops" (07:04.2), "about 21,000 billed input tokens" (07:12.9).
   - **V3, rings and a turnstile (S05):** the harness rings around the agent, "Budget is a turnstile" (08:20.3),
     the counter to 8/8 and the RED lock; `.without("trace")` on a copy (ponder 1).
   - **V4, sieves and lanes (S06–S07):** the slide-16 stack (S06), twelve cheeses through three sieves (12:12.4),
     "instructions in the system lane, evidence in the user lane" (12:50.7).
   - **V5, rails, a ticket and one shelf (S08, S09, S13):** the Act 3 graph as a railway (S08, from 13:51), the
     SHA-256 fingerprint (16:00.9), two orders on one shelf, "Request 1 is placed, leaving 1,400" (24:51.2).
   - **V6, drawers, a jar and a capsule (S10–S11):** five drawers (17:50–18:06), the context jar and truncation,
     "A capsule." (20:05.4).
   - **V7, a staircase of skills (S12):** "three steps of rising token cost" (21:44.7), slide 28's staircase
     (lecture tag 12c, 22:34–22:43).
   - **V8, one change, k runs, a diff (S14–S15):** Outcome / Trajectory / Cost pills (25:42.8–25:51), the
     six-step evaluation cycle (27:21–27:38), the three judges (28:54–29:04).

   **Lecture slides:** a GREY "Lecture 7 · slide(s) …" tag top right in 15 of the 16 scenes (S02's `script.md`
   header says `Lecture: none`): 36 real `lecture_ref` tags plus S01's specimen tag "Lecture 7 · slide N", which
   explains the convention. The slides are redrawn, never shown. The tags check confirmed on frames that every tag
   arrives with the picture it cites, stays while that picture is on screen, never overlaps another mobject and is
   gone before its scene ends (all 16 scene-end frames empty; `report-tags.md`, `tags/`). `SLIDES.md` maps the
   chapters to the deck. Its "This video and the slides" section predates the script and marks no proposal "do"
   (finishing plan).
3. **Pause-and-ponder moments and a recap** ✔, by Conny's decision for the series: five ponders against
   AGENTS.md's aim of one every 2 minutes.
   - **Ponders:** five cards, each followed by a silent timer; the card text is `script.md`'s `PONDER` line, and
     the answer is said right after the timer (`measured.json` "ponders", `.srt`):

     | scene | question (condensed) | card | timer | answer starts |
     |---|---|---|---|---|
     | S05 | `harness.without("trace")`: is a tool call still counted and audited, does the original still trace? | 09:14.8 | 8 s | 09:23.4 "Yes, and yes." |
     | S07 | The enriched packet removed Comté for PA: can the model still put it in its cart, and does anything in act 2 stop it? | 13:04.6 | 8 s | 13:13.2 "Yes: the get_catalog tool still returns all twelve" |
     | S09 | After the approval another order takes the Mimolette: what does checkout do, and why doesn't the approval protect it? | 16:48.9 | 8 s | 16:57.5 "Checkout revalidates, finds a stock violation, and blocks." |
     | S11 | Compaction dropped 21 of 26 messages: how does every call still know about the nut allergy? | 19:56.8 | 8 s | 20:05.4 "A capsule." |
     | S12 | An edited vendor skill adds another recipient: will the email go there? | 22:54.3 | 6 s | 23:00.9 "No. Whatever the skill says, the guards are in code" |

   - **Rate:** 5 in 31:21.75, one per 6.3 min (the gate's aim would be about 15). The longest stretches without
     one are 00:00–09:14.8 and from 22:54.3 (+6 s timer) to the end, about 8.5 min (`report-measured.md` §5).
     `BRIEF.md` ("Ponder questions") plans exactly five. S13's "the act 3 ponder · for real" chip (about 24:43)
     is a callback, not a sixth ponder. Separately, 18 English cues contain a spoken "Pause…" that sends the viewer to run a step.
   - **Decided by Conny (2026-10-21), as recorded in `videos/ac215-l05-rag/REVIEW.md` gate 3:**
     「我觉得可以保留现在的密度」: keep the current density of 3–5 ponders per lecture, plus a spoken recap and
     test questions.
   - **Recap** ✔: S16 (29:17.3, 124.47 s) tears down, fills the action boundary row by row ("Here is the action
     boundary, filled in", 30:16.0), restates the rule ("The model proposes, on the left.", 30:30.9), then the
     README's five reflection questions and five test-yourself questions (30:42.9), with answers in the study
     guide's Exercises. Part 1 closes on "In part 2, the harness takes the cart's route out of the model's
     hands." (13:45.2).
4. **Narration written for the ear, with word-anchored cues** ✔.
   - **Spoken style:** `script.md`'s conventions (1–4 sentences, at most about 60 words per SAY; commands, money
     and versions said in words; "at the time of recording" for versions; customer IDs never said).
   - **Size:** 155 SAY lines, matching the 155 voice blocks in the render sidecars; 4,287 words, inside the
     series' 3,900–4,300 (`script.md` line 231 still says 4,274, a stale note). Kokoro `af_heart` at speed 0.9:
     136.7 wpm over the runtime, 151.1 wpm over the 1,702.4 s of voice (90.5 % of the runtime).
   - **Anchors:** 617 `vo.wait_until(...)` call sites across the 16 scene files, plus one docstring mention in
     `s03_verify.py` (a plain grep finds 618). None of the 16 render logs in `build/logs/` contains
     "anchor not found".
   - **Ear fixes after the draft:** the QA's ASR watcher found six stress errors (the verbs "records" ×2 and
     "contrasts" said as nouns, "Jupyter", the noun "recap", the noun "outreach"). Six L07-only lexicon entries in
     `explainer/lexicon.yaml` fixed them. S12's answer was reworded to open on "No." (QA should). The finishing
     pass reworded four narration nits: S06 "harness policy check" (was "state check") and "Steps 6 and 7" (step 7
     makes no model calls), S10 "you saw in the tests", S14 "Dash dash inspect run…" (was "Inspect run takes…").
   - **Caveats (final ASR):** four P3 wording weak spots and a few caption timing slips, accepted below (items
     A2, A3).
5. **Simulated-target-viewer QA over the full draft** ✔.
   - Seven watchers reviewed the 480p draft: two directors (one per part), two simulated target viewers
     ("newcomer", one per part), a subtitle watcher, a follow-up watcher and an ASR watcher. The newcomers worked
     from contact sheets, exact frames and the English `.srt`, with the README open.
   - **88 timestamped findings: 2 must, 44 should, 42 nit.** The two musts are one problem, reported by both
     part-2 watchers. Both musts and every should are fixed, except one should that needs a toolkit change (cue
     timing inside a sentence, item A3). Each fix was checked by a verifier on fresh 720p or preview frames.
     Details under "Whole-video QA".
6. **Measured checks** ✔. The numbers are under "Verified" (`measured.json`, measured on the final cut).
   - **Duration:** 31:21.75 (1881.754 s), inside the series' 25–35 min; parts 13:51.25 (831.254 s) and 17:30.61
     (1050.610 s), whose container durations sum to 0.110 s more than the full cut (within ±0.5 s).
   - **Loudness:** −16.1 LUFS integrated in all four MP4s, LRA 2.6 LU; true peak −2.7 dBTP (clean cut and zh-en)
     and −2.8 dBTP (both parts). That meets the −16 LUFS voice target, with peaks well under −1 dBTP.
   - **Caption bounds:** in the burned copy the picture is scaled to about 0.87 (x 124–1794, y 0–940) and the
     subtitles sit in the band below it, from about y 990, so they cannot cover on-screen text. Every one of the
     497 events is exactly two lines, Chinese above English. Wrapping is off (WrapStyle 2). The widest lines are
     1,500 px (Chinese) and 1,664 px (English, cue #167), inside the 1,840 px usable width. Ten spot checks with a
     terminal low on screen show the subtitle about 100 px below it (`report-visual.md` F1–F2,
     `frames-visual/subs_spotcheck_bottom.png`; `report-pairs.md`, `pairs_widths.json`).
   - **Music balance:** does not apply. L07, like L02–L06, has no score: `video.yaml` has no `music:` key.
   - **Subtitle sync:** no narration sentence's speech starts more than 0.11 s after its first cue (155
     sentences). Across 489 cues matched to word timestamps the median offset is +0.10 s, and 90 % fall between
     −0.54 and +0.55 s. The voice sits a constant 0.05 s after its scene timing. The exceptions inside sentences
     are item A3.

   **Human review:** the series waiver stands in for a listening sign-off.

   Listening sign-off: waived by Conny for the AC215 series (Explainer_Videos#29, 2026-10-15): 「不需要，我现在对视频质量很满意的」 — no human listened to this cut; the ASR round trip below is the substitute.
   Review moments optional since 2026-10-22 (AGENTS.md): 「我大概率是不会进行审片的，因为我觉得做得已经非常好了，就让bugbot来检查就好了」

   **ASR round trip** (`report-asr.md`): base.en over the whole clean cut (502 cues compared, 249 with some
   difference, `asr-base.log`, `asr.json`); a second opinion with large-v3-turbo on 53 doubtful cues, on clips of
   the final mix (`asr_large_clips.json`); large-v3-turbo with word timestamps on the voice-only scene tracks
   (`asr_large_voiceonly_{1,2}.json`); speech onsets for all 155 sentences (`onset.json`) and cue-by-cue timing
   (`cue_sync.json`). Everything outside the items below is recogniser noise: numbers as words, words split at
   cue edges, code names, homophones, the French cheese names (heard the same way every time), and 18 cues whose
   first word base.en dropped after a pause, all of which large-v3-turbo hears. No swallowed words, no cut-off
   scene openings, no real full names in any transcript.

## Whole-video QA (480p draft `a9db242`, 2026-10-29/30; times are *draft* times)

**Watchers and findings** (`wcf7p3z4u.output`, key `result`; the run log reads "88 issues from 7/7 watchers"):

| watcher | must | should | nit |
|---|---|---|---|
| director, part 1 | 0 | 9 | 13 |
| newcomer, part 1 | 0 | 8 | 6 |
| director, part 2 | 1 | 7 | 4 |
| newcomer, part 2 | 1 | 4 | 7 |
| subtitles | 0 | 8 | 6 |
| follow-ups (build-time findings, review bots) | 0 | 3 | 3 |
| ASR | 0 | 5 | 3 |
| **total** | **2** | **44** | **42** |

By target: 58 scene, 14 subtitles, 11 narration, 5 shared code. Some problems were reported twice (the S08 must;
the S05 turnstile; the S02 erratum flash; the S08 banner flash). The follow-ups watcher found no `QA_FOLLOWUPS.md`
and no review-bot thread on L07 (Bugbot had run out of usage, then reported the series PR too large), so it
checked the build-time critiques instead.

**The must, and how it was fixed.**
- *draft* 14:45–14:56, S08: the "Before" half of the shipping lesson was narrated over the "After" command
  (`--scenario pa-shipping`) and tracker step 3, so a viewer could tie WORKFLOW BLOCKED to the command that
  revises.
- **Fix** (`s08_workflow.py` beat 4, split in two): the tracker stays on step 2 while `python cli.py --act 3`
  types, prints and shrinks to a strip holding the blocked run's command and scenario. The rail, RED bar, README
  382–383 quote and the stop at validate play under it. On "After, the revise loop" the tracker moves to step 3
  and the step-3 command types into the strip. The SAY is unchanged. The S08 verifier checked it on a fresh
  render; the finishing pass rewrote S08's SHOW line to this order.

**The shoulds, examples by kind** (all fixed and verified, except the one listed under "Still open"):
- **Filled flashes hiding their own labels** (the L05/L06 lesson): S02 erratum pill, S04 answer card, S06 context
  packet, S08 banner. Each now pulses only its outline or text.
- **Things on screen too briefly or missing:** S02 extras added to the ▶ card and the key-length echo held ~2.5 s;
  S03 `check_sdk` command kept on screen; S05 Budget values ringed as named and the labelled onion held 1.5 s;
  S09 the "60 guests · NY" ask shown; S10 the ▶ card lands during "Pause and run step 1"; S11 the memory rows held
  readable; S15 the extra cards held through their commands.
- **Pictures:** S05 turnstile redrawn as a waist-high gate (finishing pass, `common.py`); S06 copied column no
  longer slides over labels; S07 lanes order and lecture tag span; S11 notes take the drawn route; S12 the
  broken-seal badge no longer snaps back; S16 the recap table's cell text and its tag.
- **Subtitles:** 12 yaml rewordings (`g1.yaml` 6, `g2.yaml` 6; cross-paired clauses at *draft* 00:20 and 13:50, line breaks inside dates,
  counts and glossary terms), three `en_display` capitals (UNRESOLVED, DECLINED, Invalid or unauthorized), and
  the glossary alternative "vendor document".
- **Narration:** the five stress errors via the lexicon, and S12's answer ("No. Whatever the skill says…").

**Nits:** fixed in the QA round or in the finishing pass (the four narration nits above, `script.md` SHOW lines
for S01, S04, S05, S06, S08, S09 and S16, the `.animate` legs in four `common.py` helpers), except those listed
next.

**Still open after QA and the finishing pass, and why:**
- **Cue timing inside sentences** (ASR, should, shared): `explainer/subtitles.py` splits a sentence's span by
  character count, so numbers and comma pauses throw cues off by more than 1 s. A toolkit change, deferred to its
  own toolkit PR (AGENTS.md split). It is what remains in item A3.
- **`.zh.srt` breaks `python cli.py | --act 1 …`** (subtitles, nit, shared): a toolkit change in
  `explainer/subtitles.py`; `g1.yaml`'s header records the wrap as accepted.
- **Five English lines split tight phrases** ("transmitted: no", "status: error", "Evaluation step 3", "path,
  scripted:", "batch establish"; nit): `explainer/i18n.py` turns no-break spaces back into spaces, so it needs a
  toolkit change.
- **`resize()` shows an empty full-height terminal for ~0.7 s** (*draft* 10:41, nit, shared): merging the fades
  would change every resize in every scene.
- **S04 `--show-json` skips lines 2–7 with no "…" row** (nit): a "…" row would push the command off the
  13-row terminal.
- **S11's half-size table shows bars for the non-context rows, while S07's shows text** (continuity, from the S07
  verifier): tried in the finishing pass, it pushed the "Move to harness" label onto the README chip (`apart`
  assert), so it was reverted rather than redesigned.
- **Cosmetic, left by the verifiers:** the turnstile's upper-right arm rises above the cabinet; S11's rising note
  card crosses the dashed 50 %/80 % lines; S13's opening anchor is reached 0.30 s after it is spoken; `row_tag` is
  duplicated in S14 and S16 (a refactor, no effect on screen).

## Final-cut checks (1080p60, `b3367b3`, 2026-10-30)

- **Tags** (`report-tags.md`): pass, no defects. 36 tags plus the specimen, each with 4 frames (in, mid, pre,
  post) and a contact sheet (`tags/frames/`, `tags/sheets/`). An automated overlap check and a whole-film sweep of
  the top-right corner at 4 fps found no missing, stray or overlapping tag. Two differences from `script.md`:
  item A1.
- **ASR** (`report-asr.md`): intelligible throughout. 4 P3 wording items, 1 P2-minor caption slip and smaller
  timing slips: items A2–A3.
- **Visual** (`report-visual.md`): 627 frames of the burned copy on 40 sheets (one every 3 s) plus about 60
  full-size frames and crops. No render regression. Every scene ends on an empty, uniform frame (luma mean 14.0). No
  clipping, overlap, off-frame text or garbled glyph; the accented cheese names render. The customer IDs appear
  only as ‹customer 1› / ‹customer 2›, and no real full name was seen. Five freezes of 4 s or more outside the
  ponders: item A5.
- **Pairs** (`report-pairs.md`): all 497 bilingual cues read. No swapped neighbours, no line broken inside a
  command, no cue over two lines, no full names; the two part files together equal the full file. Optional
  items: A4.
- **Measured** (`report-measured.md`, `measured.json`): all four MP4s decode with no errors; loudness, true peak,
  subtitles, chapters and the part split pass. Notes: A6. The report's ponder-rate shortfall is decided under
  gate 3.

## Accepted items (coordinator decision, 2026-10-30: no fix round for this cut)

- **A1. Two tag exits that differed from `script.md` (by design; text fixed).**
  - 16a, "slide 22": the code (`s16_recap.py:595–597`) removes it at the "TRACKER Res 2" block with the table's
    texts (gone at 30:38.0), one block before the recap questions, where `script.md` had "The lecture tag leaves".
    The code comment gives the reason: a tag sits only over its picture.
  - 10a, "slides 8, 13–16": `script.md` named no exit; the code (`s10_planner.py:429`) removes it at 18:06.1 when
    the cabinet shrinks for the Act 4 terminal. The cited memory chips are already in the drawers.
  - Both were one-line text changes, so `script.md`'s SHOW lines now follow the code: S16's "TRACKER Res 2" line
    reads "The lecture tag leaves with the table's texts; the table shrinks.", "The lecture tag leaves." was taken
    off the recap-questions line, and S10's "TRACKER Act4 1" line reads "The lecture tag leaves; the cabinet
    shrinks to the right." (this record's update; no scene file changed).
- **A2. Four P3 wording weak spots (minor; meaning survives in context).**
  - 00:38.7, cue 11: "Code checked the cart" heard as "check the card" (voice-only p 0.70). The next cue's numbers
    make the meaning clear.
  - 18:58.0, cue 304: "nut allergy included" heard as "not allergy" in the mix (voice-only "nut" p 0.70). "Nut
    allergy" is said clearly at 12:19, 12:23, 19:50 and 20:13.
  - 23:00.9, cue 365: the one-word "No." comes out clipped (p 0.36) and is heard as "Now"; the rest of the
    sentence gives the answer.
  - 28:29.0, cue 455: "errored" heard as "erred" (p 0.63); nearly the same meaning, and the word is a
    `wait_until` anchor in `s15_compare.py`.
- **A3. Caption timing slips (minor; toolkit cause, see "Still open").**
  - 04:16.9–04:21, cues 69–70: about 1.5 s late. "at the time of recording:" shows 04:18.1–04:20.5 after it is
    spoken (04:16.9–04:18.3), and "Python 3.13.16, …" starts at 04:20.5, 1.6 s after "Python" is spoken. Version
    numbers take longer to say than their characters suggest.
  - 07:12.9, cue 115: about 1.2 s early ("tokens," of cue 114 is still being spoken).
  - 00:24.1, cue 6 (+1.4 s) and 10:19.3, cue 166 (+1.0 s): the cue's first word starts more than 1 s after it
    appears.
- **A4. Pairs report's optional items.**
  - English shown twice under two Chinese halves: #45–46 (02:48.8–02:53.9, "Step 3, bash docker-shell.sh…") and
    #347–348 (21:59.0–22:03.0, "The lecture's skill also has a scripts folder…"). Meaning correct; cosmetic.
  - #179 → #180 (11:07.1–11:14.7): "fails" is in English #179 and 不通过 in Chinese #180. Each pair still reads.
  - #390–391 (24:51–25:00): 订单 1 / 订单 2 for "Request 1 / Request 2". A terminology choice, not a pairing fault.
- **A5. Low-severity freezes (by design; narration continues over a still picture).** 00:25.0–00:30.1 (the
  malformed `1,5000¢`), 04:18.1–04:24.3 (the `check_sdk` output; 7.5 s in the clean cut), 18:32.1–18:36.1 (the
  Époisses stock bar), 23:46.9–23:51.9 (S13's slow fade-in of "graph of agents"), 24:55.4–24:59.5 (stock bars
  after request 1). The clean cut's other picture-only holds fall on "your turn" cards, terminal results meant to
  be read and the end cards.
- **A6. Measured notes (harmless).**
  - `chapters.txt` truncates each scene start to the whole second, so every mark is 0–0.933 s before its cut
    (worst: S15, 27:16 against 1636.917 s).
  - Part 2's audio runs 0.11 s past its video (1050.61 against 1050.50 s).
  - The clean file and both parts have a video `start_time` of 0.021 s (about one frame); the zh-en copy 0.000.
  - `.zh.srt` cues 331 (24:23.1) and 358 (26:17.9), and zh-en cue 414, are code identifiers joined by 、, by
    design.
  - The cue counts differ by language (502 / 429 / 497), as expected.
  - `script.md` line 231's word count (4,274) is stale; the measured count is 4,287.
- **A7. Burned layout (by design).** The burned copy scales the picture to about 0.87 to give the subtitles their
  own band, leaving about 124 px of black at each side (`report-visual.md` F1). This is the toolkit's layout.

## Verified (final render, `b3367b3`)

All numbers from `measured.json` and the five reports, measured on 2026-10-30.

- **Files:** H.264 High (level 5.0), yuv420p, progressive, 1920×1080 at 60 fps; AAC-LC 48 kHz stereo, about 174
  kbps. Each decodes in full with `ffmpeg -v error` with exit 0 and no errors (`decode_*.log`, 0 bytes).

  | file | duration | frames | size | loudness | LRA | true peak |
  |---|---|---|---|---|---|---|
  | `ac215-l07-agent-harness.mp4` | 1881.754 s (31:21.75) | 112,904 | 116.4 MiB | −16.1 LUFS | 2.6 LU | −2.7 dBTP |
  | `ac215-l07-agent-harness.zh-en.mp4` | 1881.750 s | 112,905 | 113.7 MiB | −16.1 | 2.6 | −2.7 |
  | `ac215-l07-agent-harness_part1.mp4` | 831.254 s (13:51.25) | 49,874 | 51.1 MiB | −16.1 | 2.6 | −2.8 |
  | `ac215-l07-agent-harness_part2.mp4` | 1050.610 s (17:30.61) | 63,030 | 65.3 MiB | −16.1 | 2.6 | −2.8 |

  The two parts' frame counts sum to the full cut's exactly.
- **Subtitles:** `.srt` 502 cues, `.zh.srt` 429, `.zh-en.srt` 497; the last cue ends at 1877.386 s in each. In
  every file the cues are in order, inside the runtime, at least 1.000 s long, and none overlap. The part files
  together equal the full files cue for cue; part 2's offset (831.233 s) is part 1's video length.
- **Chapters:** 16 entries whose titles match `video.yaml`'s scene titles in order; the scene durations sum to
  1881.733 s, the full cut's video length. `chapters_part1.txt` (7) and `chapters_part2.txt` (9, re-based to 0)
  match too.
- **Scenes:** all 16 end on an empty frame (visual F3, tags check); each chapter start lands on its new scene.
- **Narration:** 155 SAY lines = 155 rendered voice blocks; 4,287 words; 151.1 wpm over voice time.
- **Lecture tags:** 36 + 1 specimen, each on its picture and gone before its scene ends (frames in `tags/`).
- **Privacy:** customer IDs masked on screen; only `student@laptop`, `vendor@example.com` and
  `other@example.com` as identities; no real full names in frames read, subtitles or ASR transcripts.
- **Provenance** (`ASSETS.md`): every terminal line comes from the 2026-10-20 captures in `assets/terminal/`; code
  panels quote `assets/source/` at `e25dfe9` (126/126 files checked against their git blob hashes); live answers
  are the staff's saved Colab outputs, tagged `recorded`, and README descriptions, tagged `expected`; Colab, its
  Secrets panel, the browser scorecard and the editor are drawings tagged `illustration`.

## Not claimed

- **No human listened to this cut** or watched it. The listening gate rests on the series waiver quoted under
  gate 6, and the audio was checked only by machine (the ASR round trip).
- **The Chinese subtitles were reviewed by agents only** (the QA subtitle watcher, the text fixer and the pairs
  check); no human translator or native reviewer read them.
- **Nothing live ran past the first model call.** The captures had no OpenAI key: every live command stops at
  OpenAI's 401 for the README's placeholder key. What a live run prints after that (Act 1–6 answers, the
  `--compare` table, the live evaluation batches) is shown from the staff's saved Colab run or the README's
  descriptions, not from our own run.
- **The Colab path was not run** (no Colab session, no Secrets key): its cells are quoted from the downloaded
  notebook and its outputs are the saved ones. The HTML scorecard was not opened in a browser, and the editor
  step was not performed interactively.
- **The visual check read frames every 3 s**, plus targeted frames; motion between those samples was checked only
  by `freezedetect` and the tags check's 4 fps corner sweep.
- **Subtitle timing** is measured with base.en word times (about ±0.5 s accurate) and voice-only large-v3-turbo
  checks on selected ranges, not cue by cue by ear.
- **No review-bot pass on this episode:** the QA's follow-ups watcher found no bot thread on L07.
