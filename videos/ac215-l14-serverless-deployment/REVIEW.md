# Review record: AC215 · Lecture 14 — Serverless deployment: a function, a service and a job on Cloud Run

Follow-along of [dlops-io/serverless-deployment](https://github.com/dlops-io/serverless-deployment) `main` @ `46cc62f`
(HEAD of `main` on 2026-11-04, the four-part README the course page links), `README.md` top to bottom: *Before you
begin* with the Terminal setup, Parts 1–4 and *Clean up*. The old README at `4eaf343` (the course map's pin) is kept
in `assets/source/at-4eaf343/` only to check the slides; `SLIDES.md` was rebased on `46cc62f`. Claude Code sessions
(Claude) produced it. Verified facts and unclaimed reviews are kept in separate sections.

- **Origin:** issue #99. Built end to end on 2026-11-04 by this coordinator's agents: verified digest, live laptop
  captures, brief, script + 4 independent reviews, `scenes/common.py`, 16 scenes each with a fresh critic, zh
  subtitles, `exercises.md`, `README.md` and the study guide (MLOps_Learning PR #5). Milestone commit `1c27071` (its message says "14 scenes + critics"; its tree holds all 16 scene files).
- **Captures:** 2026-11-04 09:24–09:35 UTC (`ASSETS.md`, "terminal/"), in fresh containers: a Docker Engine 29.8.2
  (`docker:29.8.2-dind`) standing in for the laptop, a Debian 12 / Python 3.12.15 / uv 0.13.7 shell (`dev/`) and
  Google Cloud SDK 592.0.0 with no account signed in (`gcloud/`). That machine had **no GCP project, no Google account,
  no credentials and no browser**. Every local step ran live; every gcloud box runs to its first real error (the
  placeholder project ID, then "no active account"); console steps are `illustration`; what only the cloud shows is
  `recorded` from the README and its GIF captions (`assets/terminal/expected/`).
- **QA draft:** the 480p draft (30:44).
- **Whole-video QA:** `/root/ac215-backup/tasks/l14-qa-waaomhlhy.output`, key `result`. 35 agents: seven watchers,
  12 scene fixers (S02–S08, S10, S11, S13, S15, S16), one narration/subtitle fixer and 15 scene verifiers (S01–S08,
  S10–S16). The run log reads "L14: 53 issues from 7/7 watchers". A container restart interrupted the run once; it
  was resumed from its cache (32 agents cached, the last three verifiers ran after the resume). Committed as
  `7ba27ff`.
- **After QA, by the coordinator:** S16's recap reworded to "Two additions." (keeping the shared public image credited
  to the README; `script.md:1358`, `g2.yaml:376`), and the S11 SHOW tracker line fixed (`script.md:1001`, "TRACKER
  [3.3] 2 · opens with step 1 as commands"). Lexicon PR #104 (L14 entries) merged to `main` as `5ea99e7`, which the
  CI release renders with.
- **Finishing pass:** none. The coordinator's list of finishing-pass outputs for L14 is empty (`[]`).
- **1080p60 renders:** all 16 scenes; the renders and the logs in `build/logs/` are dated 2026-11-05 02:06–02:35 UTC.
  None of the 16 logs contains "anchor not found".
- **Final cut:** 30:56.6 (1856.644 s); parts 15:13.5 + 15:43.1. File times (UTC, 2026-11-05): the clean cut and the
  full-cut subtitles 02:49; the burned copy, chapters and transcript 03:05; the parts 03:06–03:07. The MP4s are not in
  Git (release assets).
- **Final-cut checks, two rounds:**
  - **Round 1** (`report-{tags,pairs,measured}-round1.md`, `report-asr.md`, `report-visual.md`, on the cut
    probed at 01:46, 110,421,291 bytes): no render regression, ASR 0 real problems. The tags check found five tags outliving or
    preceding their pictures (S05, S06, S07, S13, S14); the pairs check two zh splits (cues 88–90 and 224). The
    round-1 measured check returned only "Waiting for the decode run." (`report-measured-round1.md`, 27 bytes).
  - **Fix round:** the five tag spans fixed in the scene code (`b92f106`) without changing any scene's duration (the
    round-1 and final cuts both run 1856.644 s with 111,393 video frames), the two zh items reworded (`37796bd`),
    the scenes re-rendered at 1080p, the cut re-stitched and re-burned (the regenerated subtitle files committed as `02f43e3`; the MP4s are not in Git).
  - **Round 2** (`report-tags.md`, `report-pairs.md`, `report-measured.md`, evidence 03:08–03:18 UTC, after the
    last output file of 03:07): all five tags verified; measured all pass; two zh-en residues, accepted (A2).
  - The ASR and visual checks were not re-run on the final cut (see "Not claimed"). All five round-2/round-1 reports
    the coordinator saved exist and were read in full for this record.

**Conventions:**
- **Times** are mm:ss in the full cut (`output/ac215-l14-serverless-deployment.mp4`, 1856.644 s), except in
  "Whole-video QA", which keeps the 480p draft's times (marked *draft*).
- **Cue numbers** name their file: `.srt` (521 cues) or `.zh-en.srt` (517).
- **Evidence paths** are relative to `build/final-review/`. That folder is git-ignored and exists only in the producing
  session; a successor re-runs the checks to reproduce it.

## Content gates (AGENTS.md)

1. **Hook** ✔. S01 opens on a broken thing, not a value proposition: the translation page answers "Bonjour à tous" on
   the laptop (`.srt` cues 1–3, 00:00.0–00:09.3), then "Now send the address to a classmate." (cue 4, 00:09.6) "On
   their laptop, localhost 8086 finds nothing," (cue 5, 00:11.9); the Lecture 1 VM "is billed all night, while nobody
   translates anything." (cues 8–9, 00:24.5–00:30.5).
   - The question: "Can this page have a public URL, and cost nothing while nobody is using it?" (cue 11, 00:32.9).
   - **Payoff:** S08, "the meter moves only while requests are served." (cue 238, 13:41.1); the recap, "a service
     that scales to zero, and a job that exits with a receipt." (cue 502, 29:45.8).
2. **Intuition before formalism, with an animated mechanism for each core idea** ✔. `BRIEF.md` ("Visual set pieces")
   defines eight, each animated next to the commands it explains:
   - **V1, the lecture's 2×2 (`DeployGrid`, slide 10):** built in S02 (from about 01:53), cells lit in S04/S05/S07/S08,
     complete again in the recap ("Here is the whole map.", 29:37.6).
   - **V2, scale to zero (`InstanceStrip`):** S01's preview (from 00:38.2, "A copy of your app appears when a request
     arrives", cue 13); S08's numbers, "Two instances, the ceiling, with 8 slots." (14:11.4).
   - **V3, a function is a container you did not write (`BuildLine`, S05):** "Save sends your three inputs to Cloud
     Build." (06:36.8); the wrong-entry-point run after ponder 1 (07:51.1–08:00).
   - **V4, one URL, many inputs (`QueryToArgs`, S06):** "Step 3: append the query string." (08:35.0); the contrast in
     S07, "The query string from part 1 gets 405 here," (12:01.5).
   - **V5, the container contract (`PortEnvelope`, S07):** "the image has two start-up slots" (11:00.9); "docker ps
     shows the door, 8086 outside and 8080 inside," (11:31.7).
   - **V6, two doors (`IdentityDoors`, S09–S11, S13):** "The first door, who may call it, is Allow public access;"
     (15:21.2); "Calling out goes through the other door" (15:50.5); "on Cloud Run, the badge supplies it." (18:11.5).
   - **V7, one image, two programs (`LifecycleStrips`, S12–S13):** service and job strips from about 21:17.6; the
     eleven argument chips, "each its own chip" (23:48.4), and the one-chip mistake (24:25.0).
   - **V8, a result you can prove (`AttemptFolders`, S14–S15):** "It is the receipt." (26:13.4); "A new attempt folder
     lands beside the first, and create-only uploads cannot overwrite." (26:38.9).

   **Lecture slides:** a GREY "Lecture 14 · slide(s) …" tag top right (`report-tags.md`), 23 tags in S01, S02,
   S04–S08, S10, S12–S14 and S16; none in S03, S09, S11 or S15, which are tutorial-only (`SLIDES.md` §1 and §5). The
   deck is redrawn, never shown; every content slide (5, 6, 8–12, 14–16) is used at least once (`SLIDES.md` §1).
   - Round 2 found all 23 labels correct, none overlapping anything (5 fps sampling of each tag box and a 14 px border,
     `tags-r2/overlap.json`), and none on screen after its picture has gone. A 10 fps scan of the clean cut matched
     every tag to its `events.json` times within 0.4 s (`tags-r2/scan.json`).
   - The five round-1 tags are fixed and verified on new frames: T10 (S05, leaves with the V1 grid at 07:12.5–07:13.1),
     T12 (S06, with V4 at 08:48.4–08:49.2), T14 (S07, with the README card at 10:23.3–10:23.8), T20 (S13, only with
     the V7 job strip, 25:04.1–25:10.9) and T21 (S14, with the where-to-look card, 26:15.4–26:17.5).
   - Open: tags that arrive before their picture and two judgement calls (accepted item A3).
3. **Pause-and-ponder moments and a recap**: ✔ for the ponders, by Conny's decision for the series (accepted item
   A1); ✔ for the recap.
   - **Ponders:** five, each a card followed by a silent timer. Card times are from `measured.json` (each scene's
     `events.json` plus its scene start, minus the 0.6 s fade-in); answers are from the `.srt`.

     | # | scene | card (from `script.md`) | card | timer | answer starts |
     |---|---|---|---|---|---|
     | 1 | S05 | You paste main.py but type translate as the entry point. Does the build fail? If not, what fails, and where do you see it? | 07:42.5 | 8 s | 07:51.1 "Installing the requirements works; they are fine." / 07:54.3 "But the deployment fails." |
     | 2 | S08 | Concurrency 4, max instances 2. Ten people press Translate at once. How many instances — and the last two? | 14:02.7 | 8 s | 14:11.4 "Two instances, the ceiling, with 8 slots." |
     | 3 | S09 | The service allows public access. Does that let it call Agent Platform? | 15:40.6 | 6 s | 15:47.2 "No. That door only admits callers." |
     | 4 | S13 | You fill all eleven argument chips but leave Container command empty. What does the container try to run? | 24:43.9 | 8 s | 24:52.5 "The arguments replace the default command," |
     | 5 | S14 | Execute the same job again, same arguments. Is the first result overwritten? | 26:31.3 | 6 s | 26:37.9 "No." |

   - **Rate:** 5 cards in 30:56.6, 0.32 per 2 minutes (`report-measured.md`), one every 6.2 minutes, against
     AGENTS.md's aim of one per 2 minutes (about 15). The longest stretches without a card are 543.2 s (15:40.6 to
     24:43.9, S09 to S13), 462.5 s (00:00 to the first card), 380.2 s (07:42.5–14:02.7) and 265.4 s (the last card to
     the end).
   - **Decided by Conny (2026-10-21), as recorded in `videos/ac215-l05-rag/REVIEW.md` gate 3:**
     「我觉得可以保留现在的密度」: keep the current density, which that record gives as 3–5 ponders per lecture plus a
     spoken recap and test questions. L14's five ponders are inside that series density and below AGENTS.md's aim.
   - **Recap:** S16 "Clean up, and what serverless costs" from 28:53.6 (122.97 s).
     - 28:53.6–29:16.3: the clean-up checklist, steps 1–4, "Pause and delete them all now." (cue 492, 29:14.2).
     - 29:16.3–29:29.2: "Two additions." Soft-deleted files and the build's source archives and logs; "And, per the
       README, keep the shared public image; others use it." (cues 493–496).
     - 29:29.2–29:37.6: the README's troubleshooting table.
     - 29:37.6–30:15.3: the spoken recap on the complete V1 map (cues 499–502), then the lecture's three downsides and
       the tutorial's answers: cold starts (min instances), limited control and debugging (three places to look),
       vendor lock-in (the image and the Functions Framework ran on the laptop) (cues 503–508).
     - 30:15.5–30:20.9: the pointer to Lecture 15; 30:20.9–30:54.7: "Test yourself, pausing on each." and five
       questions (cues 511–521). The answers are in `exercises.md`, Part A.
4. **Narration written for the ear, with word-anchored cues** ✔.
   - **Spoken style:** identifiers are said in words ("hello underscore HTTP", "the wait flag", "A M D 64"), with the
     literal form in the subtitle's `en_display` (QA added `--wait`, `512 MiB`, `docker top/ps`, `application-default`,
     "View diff & redeploy", "Downloaded results").
   - **Size:** 159 SAY lines, 4,315 words (`measured.json` "narration"), 159 voice blocks in the scene sidecars. Kokoro
     `af_heart` at speed 0.9 gives 150.1 wpm over the 1,724.8 s of voice (92.9 % of the runtime) and 139.4 wpm over
     the runtime.
   - **Anchors:** 613 `wait_until` anchors across the 16 scene files (S01–S16: 24, 31, 26, 50, 26, 40, 48, 53, 34, 51,
     33, 38, 46, 46, 30, 37). None of the 16 render logs contains "anchor not found".
   - **Pronunciation:** the QA ASR watcher found no mispronunciation and needed no new lexicon entry; its three timing
     findings were fixed in narration (S05, S07) or left as nits (S04, S15). The L14 lexicon entries
     (`explainer/lexicon.yaml:414–427`: ports, status codes, "section 3.3", the two greetings, "same/by digest") are
     from the build.
   - **Final ASR** (`report-asr.md`): 0 real mispronunciations or swallowed words; no cue's audio late by more than
     about 1 s. Low-priority listen items are under "Open nits".
5. **Simulated-target-viewer QA over the full draft** ✔.
   - Seven watchers reviewed the 480p draft: two directors and two simulated target viewers ("newcomer"), one of each
     per part; a subtitle watcher, a follow-ups watcher and an ASR watcher. They worked from contact sheets, frames
     pulled from the draft, the scene code, the English `.srt`, the README at `46cc62f` and the captures.
   - **53 timestamped findings: 3 must, 28 should, 22 nit.** All three musts were fixed and verified on fresh preview
     frames; on the final cut the visual check found no overlap and the S15 helper command uncovered (28:36). Each
     scene's fixes were checked by a skeptical verifier; several verifiers tightened or completed a fix (S03, S04, S05,
     S07, S13). What stayed open is listed under "Whole-video QA".
6. **Measured checks** ✔. The numbers are under "Verified" (`measured.json`, measured on the final files).
   - **Duration:** 30:56.6 (1856.644 s), inside the series' 25–35 min. The parts are 15:13.5 (913.538 s) and 15:43.1
     (943.128 s). Their container durations sum to 0.022 s more than the full cut, and their video frame counts sum
     to the clean cut's exactly (54,811 + 56,582 = 111,393). Part 1 ends on the S09 boundary (S01–S08 sum to
     913.507 s), as `video.yaml`'s parts say.
   - **Loudness:** −16.1 LUFS integrated in all four files, LRA 2.3 LU, true peak −2.7 dBTP (part 2: −2.8).
   - **Caption bounds** (`report-visual.md`, `report-pairs.md`): every one of the 517 events in `.zh-en.ass` is one
     Chinese line (Noto Sans CJK 50 px) above one English line (33 px), with a single `\N` and `WrapStyle: 2`; the
     `.ass` text equals the `.zh-en.srt` (0 mismatches). Measured with Noto Sans CJK SC at the nominal 50/33 px, the widest lines are about 1,685 px English
     (11:52.8) and about 1,462 px Chinese (29:24.0), against 1,840 px; on the burned frames they span about 1,170 px and
     1,000 px (`verifier/widths.txt`, `verifier/frames/v_713.5_widest_en.png`, `v_1765.5_widest_zh.png`). In all 619 sheet frames no content falls in the band just above the
     subtitles (about 944–986 px; subtitles start at about 990 px); 12 spot checks over terminals (01:12 to 28:36)
     found no command covered.
   - **Music balance:** does not apply. L14, like L02–L13, has no score: `video.yaml` has no `music:` key.
   - **Subtitle sync** (`report-asr.md`, onset check): no cue's speech starts more than about 1 s after its cue. Cue
     277 (16:05.6) is borderline at about 1.0 s (the previous phrase runs into the cue, then a pause); cues 232
     (13:17.5) and 325 (19:07.0) show 0.6–0.8 s after their words are spoken.

   **Human review:** the series waiver stands in for a listening sign-off.

   Listening sign-off: waived by Conny for the AC215 series (Explainer_Videos#29, 2026-10-15): 「不需要，我现在对视频质量很满意的」 — no human listened to this cut; the ASR round trip below is the substitute.
   Review moments optional since 2026-10-22 (AGENTS.md): 「我大概率是不会进行审片的，因为我觉得做得已经非常好了，就让bugbot来检查就好了」

   **ASR round trip** (`report-asr.md`, on the round-1 clean cut, whose audio and timings the final cut keeps):
   - faster-whisper `base.en` over the whole cut: 521 cues compared, 4,360 words recognised, 236 cues with some
     difference (`asr.json`, `asr-base.log`, `asr-words-base.json`).
   - `large-v3-turbo` re-ran 20 windows: the 17 most doubtful passages and 3 onset checks (`asr-large-clips.json`,
     `asr-large-onset-clips.json`). Every doubtful passage is spoken correctly; two (03:07–03:16, 28:29–28:44) were
     base.en dropouts.
   - The 236 differences are recogniser noise (digits against words, spellings of terms, apostrophes, homophones) and
     words counted across a cue boundary.

## Whole-video QA (480p draft, 30:44; times are *draft* times)

**Watchers and findings** (`l14-qa-waaomhlhy.output`, key `result`):

| watcher | must | should | nit |
|---|---|---|---|
| director, part 1 | 0 | 4 | 3 |
| newcomer, part 1 | 0 | 5 | 2 |
| director, part 2 | 2 | 3 | 4 |
| newcomer, part 2 | 1 | 5 | 2 |
| subtitles | 0 | 9 | 9 |
| follow-ups | 0 | 0 | 0 |
| ASR | 0 | 2 | 2 |
| **total** | **3** | **28** | **22** |

- **By target:** 25 scene, 18 subtitles, 6 narration, 4 shared code.
- **By kind:** 21 subtitle, 10 follow-along, 8 text, 5 picture, 3 sync, 2 continuity, 2 fact, 1 pacing, 1 narration.
- **By scene:** S07 7, S10 7, S16 6, S05 5, S15 5, S04 4, S13 4, S08 3, S11 3, S12 3, S03 2, S01 1, S02 1, S06 1,
  S14 1, S09 0.
- **Facts:** the part-1 director checked the commands and terminal lines against laptop/05, laptop/10, dev/20–29,
  provider-timeout and gcloud/05/18; the part-2 director checked every typed command against README.md @ `46cc62f`
  and every terminal line against dev/10–18, laptop/24, 42, 44, 45 and gcloud/09–11, and found them right. The
  part-1 newcomer followed the README in order and found no wrong fact and no missing step; the part-2 newcomer found
  no step skipped or reordered. All four found no real-looking id or key and no instructor name.
- **Follow-ups watcher:** found no `QA_FOLLOWUPS.md` for L14 (none ever existed); searched the episode folder, the 16
  render logs and the script-stage reviews for deferred findings (none); reported no issues.
- **Subtitle watcher:** zh line breaks inside a term (`hello 下划线 http`, "Serve this revision immediately"), nine
  sentences whose Chinese clause order did not match the English cue cuts (the worst S16 *draft* 28:51, where the Chinese
  for "once nothing uses them" showed under "Step 3: delete your buckets"), and missing `en_display` entries. It left the 04:42 "Cloud
  Functions" split out because no rewording it tried changed the cut (accepted item A2).
- **ASR watcher:** no mispronunciation, no new lexicon entry; three subtitle-timing findings from one toolkit cause
  (`split_cues` places in-sentence cuts by display length), and one heard-as nit.

**The musts, and how each was fixed:**
- **M1, *draft* 28:43, S16: the GOLD "billed until deleted" tag sat on the tracker caption** (director, part 2) for
  the whole checklist. **Fix** (`s16_recap.py`): the checklist card moved down (`CL_TOP` 2.72 → 2.47) with the erratum
  card, and `assert ctag.get_top()[1] < TRACK_BOTTOM - 0.05`. Verified at scene times 1.5, 9, 24 and 34 s.
- **M2, *draft* 23:32, S13: the form's "illustration" tag cut through "python" in "step 4 of 9: Command python"**
  (director, part 2), about 7 s. **Fix** (`s13_job.py:314–315`): the tag sits right of the form, as the arguments
  form's does, with an assert under `TRACK_BOTTOM`. Verified at scene times 56 and 60 s.
- **M3, *draft* 28:20, S15: the helper command README 4.6 asks you to run was never fully visible** (newcomer, part 2):
  its first two rows scrolled off as the output came in. **Fix** (`s15_terminal.py:397–405`): on "Pause and run it"
  the terminal clears and retypes the whole command from the capture, with ▶ your turn, a "README line 1002 · bucket
  names, without gs://" chip, an assert that no row scrolled off, and a 1.0 s hold. Verified at scene time 80 s: all
  five rows on screen.

**The shoulds, examples by kind** (fixed and verified, except those under "Still open"):
- **Follow-along:** S03's seven exports now stand on one README card (lines 75–81) at "Pause and run them", the long
  ones folded after `=`; S07's four extra curl checks each run in a cleared 7-row strip, command and `[HTTP nnn]`
  together; S08's and S10's gcloud alternatives hold 2.5–3 s longer; S13 gained the breadcrumb "Containers,
  Connections, Security → Containers"; S15 names the role to ask for ("Cloud Run Jobs Executor With Overrides ·
  README:726"); S07's Apple Silicon chip says a platform WARNING prints first.
- **Pictures and text:** S05's ponder card moved under V3; S07's `docker top` panel now shows `--threads 4` (ringed)
  and explains `python3.12`; S04's decorator and `hello_http` get a bar and ring instead of an invisible recolour;
  S10's chip reads "captured in part 2: the flag missing" instead of "captured in S07"; S16's "keep the shared public
  image" is a GREEN chip credited to README 1027–1028, no longer an erratum, and the `docker image rm` chip says
  "removes only your laptop's copy".
- **Narration:** "revision" is defined where it is first used (S04, with an on-screen line); the S05 and S07 sentences
  were split so the cues follow the voice; S11's tracker shows step 2 while "Step 2 begins…" is spoken.
- **Subtitles:** the nine out-of-step pairs reworded in `g1.yaml`/`g2.yaml`, the two zh line breaks fixed, the
  `en_display` entries added; `python -m explainer.i18n check … --lang zh` printed OK.

**Nits:** fixed, except those listed next. Examples: S02's roadmap label no longer touches the Prototype box; S06's
second tab keeps S05's folder prompt; S08's gcloud rings all stay visible; S15's extra tag sits inside the terminal;
S16's last card pulses instead of holding 4.0 s still.

**Still open after QA, and why:**
- **S07 *draft* 10:28, "digest" used before it is defined** (newcomer nit): narration edits were limited to must and
  should items; the anchor `wait_until("The digest equals")` would also have to change. Accepted (A5).
- **S04 *draft* 04:27, cue 84 about 1.1 s late** (ASR nit): needs the toolkit's in-sentence cue timing or a
  `script.md` split. Accepted (A5).
- **S15 *draft* 27:48, "a new path and Spanish" heard as "in Spanish"** (ASR nit): same narration rule. Accepted (A5).
- **S10 *draft* 18:19, the drawn page's URL is BLUE in S08, PINK in S10** (director nit): the fix is one argument in
  `s08_service.py:531` (`TranslatePage(SERVICE_URL, CLOUD)`), outside the S10 fixer's scope. Accepted (A5).
- **S13, the README's "expand its chevron if the container row is collapsed" (README:747) is not shown**: the
  breadcrumb was added; the chevron needs a `script.md` SHOW change or a wider form that pushes the help chip off the
  frame. Accepted (A5).
- **Not ruled on by the coordinator** (no `common.py` or toolkit fixer ran):
  - Cloud Build is drawn PURPLE (the tools colour, `common.py:142, 2458`), though the series table makes it BLUE
    (director should; S05 from 06:36, S08, S16).
  - The drawn app page still preselects `es` (`common.py:3740`) where the real page preselects French (director
    should, fact). S10 now pulses `fr` in gold before Translate; S01, S07 and S08 switch it as before.
  - Long single tokens hard-wrap mid-word (director nit, `Terminal.type` folding): S13's `--args` value, S15, the end
    of S10; S08's `docker image inspect --fo|rmat` (newcomer nit, S08 half of the S05 wrap item) is still on the
    final cut at 14:45 (`report-visual.md`).
- **Source drift (not rendered):** `script.md`'s SHOW lines for S05 (the strip), S07 (beats 6, 8–10), S10 ("captured
  in S07", line 961) and S15 (role chip, retyped command) no longer match the scenes; `script.md:1111` and `:1207`
  still put the S13/S14 lecture tags in block 0, and the `s13_job.py:20` docstring still says the tag leaves in block 3
  (`report-tags.md`, documentation drift).

## Final-cut checks (1080p60, 2026-11-05)

- **Tags** (`report-tags.md`, round 2 on the final files): 23 tags, four frames each (`tags-r2/frames/`, sheets in
  `tags-r2/sheets/`), none overlapping, none outliving its picture, all labels correct; the five round-1 defects
  fixed. Remaining items: accepted A3.
- **ASR** (`report-asr.md`, round 1): intelligible throughout; 0 real problems; listen items under "Open nits".
- **Visual** (`report-visual.md`, round 1, on the burned copy `.zh-en.mp4`):
  - 39 contact sheets (619 frames, one every 3 s), all read, plus 9 full-size frames and 12 clean/burned subtitle
    pairs (`sheets/`, `frames/`, `subcheck/`).
  - All 16 chapters present and in order; scenes end on empty frames (04:21 and 21:03 checked); the last frame fades
    to empty.
  - No clipping, nothing outside the frame, no garbled glyphs (Greek at 08:54 and Chinese in recorded output render),
    no stuck tag.
  - Four minor items, none must-fix (Open nits).
  - No instructor name on screen; project, account and bucket values only as placeholders.
- **Pairs** (`report-pairs.md`, round 2): all 517 cues of `.zh-en.srt` read, zh against en. No meaning swap
  anywhere, including every condition or time clause (如果/因为/当/为了/在…/一直等到). The S08 fix pairs correctly; cues
  88–90 still run one phrase ahead and cue 225 shows English over English (accepted A2). Lines, widths, the `.ass` /
  `.srt` match and the part split pass.
- **Measured** (`report-measured.md`, `measured.json`, round 2): all four MP4s decode with 0 errors and 0 warnings.
  Formats, loudness, subtitles, chapters and the part split pass. The ponder density is decided under gate 3.

## Accepted items (coordinator decisions)

- **A1. Five ponders in 30:56.6** (0.32 per 2 minutes), below AGENTS.md's aim of one per 2 minutes. Accepted under
  Conny's 2026-10-21 decision to keep the current density of 3–5 ponders per lecture (「我觉得可以保留现在的密度」);
  see gate 3.
- **A2. Residual zh-en items on the burned copy** (`report-pairs.md`, `report-tags.md` items 6–7). The zh-en splitter
  splits at the long English labels; the `.zh.srt` is clean, meaning is never swapped, and another re-burn costs about
  an hour for a cosmetic gain.
  - Cues 88–90 (04:43.5–04:52.2, S04): the Chinese runs one phrase ahead (「Cloud Functions」 in cue 88 under "One
    name has changed:", 「所以 README 一开始就进」 in cue 89), and cue 90's Chinese row is only
    `Cloud Run、Services、Write a function`. The pairs check gives a tested rewording for a later build.
  - Cue 225 (12:59.4–13:01.8, S08): the Chinese row is `from an existing container image` over the same English.
  - Cues 398 (23:40.8) and 401 (23:48.4): console field labels (`Container command`, `Container arguments`) shown
    verbatim in both rows by design.
  - Seven sentences keep the whole English line under two or three Chinese pieces (cues 26–28, 76–77, 134–135,
    200–201, 207–208, 395–396, 481–482): the splitter's designed fallback, not a defect.
- **A3. Lecture tags that enter before their picture, and two judgement calls** (`report-tags.md`):
  - T13 (S06, "slide 16") about 2.8 s before the cold-start card (10:02.5); T22 (S16, "slide 16") about 1.6 s before
    the three con cards (29:50.9); T08 (S04, "slide 10") about 1.1 s before the sketch card (05:35.2).
  - T10 (S05, "slides 10–11") enters about 1.7 s before the quote card, over the chapter heading (06:26.6). Its timing
    is unchanged from round 1; round 2 is the first report to list it, and the coordinator's accepted list does not
    name it.
  - T18 (S12, "slide 14", 21:04.5–21:30.0): about 13 s early if only V1/V7 count, on screen with the README "That is
    a job" card before them; T07 (S04, "slides 11–12", 04:37.3–05:35.7) over the checklist parked as a small icon.
- **A4. Nothing from the visual check was ruled on**; its items are under "Open nits".
- **A5. QA nits left as is:** S07 "digest" before it is defined (10:34.1, cue "The digest equals the README's…"; the
  definition comes at 14:46.7); S04's cue at 04:29.1 ("like a file upload…", about 1.1 s late on the draft; the final
  onset check did not flag it); S15 "a new path and Spanish" (27:57.3, cue 469, heard as "in Spanish" by both ASR
  models); S10's URL colour (the S08 page, about 15:01.5–15:13, BLUE; S10's PINK); S13's container chevron (step 4,
  from 23:40.8).
- **A6. The instructor's name is masked** everywhere on screen and in the subtitles (series rule); `video.yaml`'s
  Bilibili description credits the course staff, as L02–L13 do. The public image's Docker Hub namespace `cgumb`
  appears only inside verbatim commands, their echoed output and the pasted image-URL fields (10:36, 13:03, 14:48,
  23:39), never in a subtitle file (`report-visual.md`).

## Open nits (not ruled on one by one; left for the coordinator)

None blocks release. Each needs a narration, yaml, `script.md`, scene or toolkit change and a rebuild, which this
record does not make.
- **Visual check** (`report-visual.md`, round-1 burned copy):
  - 13:00–13:06 (S08): the dashed recall box under the Create-service form is labelled **"S07 · laptop"**, an internal
    scene code (`s08_service.py:190`; `frames/f_783.png`).
  - Mid-token wraps in a copyable command: 14:45–14:51 `docker image inspect --fo|rmat … :lect|ure14-…`
    (`frames/f_888.png`); also the traceback at 09:24–09:27 (`.te|xt`) and the curl at 11:57–12:00 (`"Good
    afte|rnoon everyone"`). Found by the verifier, not by the visual check: S03's terminal at about 04:03 wraps the
    `WEB_EMAIL` and `JOB_EMAIL` exports mid-word (`"transla|tion-demo-runtime@…`, `"transla|tion-audio-job@…`;
    `verifier/frames/v_243.png`); the README card that follows holds all seven exports whole.
  - Near-static stretches with narration running: 16:26.6–16:33.1 (6.5 s, S09, the Service Usage Consumer chips) and
    27:19.4–27:24.0 (4.6 s, S15 opening, README 911–914 card).
  - 11:42–12:00 (S07): the browser mockup's bottom edge sits about 4 px above the "laptop · second tab" header (no
    overlap; `subcheck/burn_708.png`).
- **ASR listen items** (`report-asr.md`, `.srt` cues): 17:30.8 cue 301 "ask course staff" heard as "core staff" by both
  models; 24:00 cue 403 "source en" said like the letter N (the screen shows `en`); 00:07 cue 3 "Bonjour à tous" and
  08:28 cue 149 "Bienvenido a AC215" read by an English voice; 16:05 cue 277 "Vertex AI" heard as "Vertex API" by
  turbo only; the sub-second split offsets at cues 232, 277 and 325 (gate 6).
- **Verifier leftovers:** S03 a sub-0.7 s cross-fade of the exports card over the shrinking terminal's title bar
  (about 04:05); S07 a 0.5 s cross-fade of the index.html panel beside the page (*draft* ~11:46), ▶ your turn about 1 s
  after "Pause and try it", and the tracker "step 4 of 4: Ctrl+C" while the voice says "Step 4: Play audio…" (*draft*
  12:00); S05's "README:1038" chip touching the "requirements installed" stamp, and the tracker saying "extra · local
  stand-in" while V3 is up (as in the draft).
- **Stale source text:** the `script.md` lines and docstring listed under "Still open after QA".
- **No `QA_FOLLOWUPS.md`** for L14, and no Bugbot thread was copied into the episode folder.
- **Chapters:** every start is the cumulative scene start rounded down (the largest gap 0.88 s, "Part 1: write a
  function" at 04:22 for 262.882 s). Harmless.
- **Frame rate:** the cut is 60 fps (the 1080p60 scene renders, as in L02–L13); the repo default for new episodes is
  30 fps. The burned copy has one more video frame (111,394) than the clean cut; the audio is identical in length.
- **Stale previews:** four `output/*_480p15*.mp4` files (2026-11-04 20:36–20:43) are from before the fix rounds and
  must not be released as deliverables (`report-measured.md`).

## Verified (final render)

All numbers are from `measured.json` and the round-2 reports, on the files in `output/` as they are now (written
2026-11-05 02:49–03:07 UTC); the ASR and visual numbers are from the round-1 cut probed at 01:46 (see "Not claimed").

- **Files:** H.264 High, yuv420p, 1920×1080 at 60 fps, AAC LC 48 kHz stereo at about 177–180 kb/s, video at about
  278–288 kb/s. Each decodes in full with exit 0 and no error or warning lines (`measured-r2/`).

  | file | duration | video frames | size (bytes) | loudness | LRA | true peak |
  |---|---|---|---|---|---|---|
  | `ac215-l14-serverless-deployment.mp4` | 1856.644 s (30:56.6) | 111,393 | 110,113,952 | −16.1 LUFS | 2.3 LU | −2.7 dBTP |
  | `ac215-l14-serverless-deployment.zh-en.mp4` | 1856.644 s | 111,394 | 108,618,434 | −16.1 | 2.3 | −2.7 |
  | `ac215-l14-serverless-deployment_part1.mp4` | 913.538 s (15:13.5) | 54,811 | 53,994,397 | −16.1 | 2.3 | −2.7 |
  | `ac215-l14-serverless-deployment_part2.mp4` | 943.128 s (15:43.1) | 56,582 | 56,126,980 | −16.1 | 2.3 | −2.8 |

  The 16 scene renders sum to 1856.538 s; each render's duration equals its `events.json` duration within 0.004 s.
- **Subtitles:** `.srt` 521 cues, `.zh.srt` 436, `.zh-en.srt` 517. Part 1 has 263 / 216 / 256, part 2 258 / 220 / 261;
  each language's parts sum to its full file.
  - In the three full files the cues are in order, inside the runtime, with no overlaps; the shortest are 0.96 s
    (`.srt` #263), 1.00 s (`.zh.srt` #374) and 1.00 s (`.zh-en.srt` #393). No part file has a short, overlapping or
    out-of-range cue.
  - The last cue ends at 1854.714 s (30:54.7), 1.9 s before the cut ends.
  - The burned `.zh-en.ass` has the same 517 events as `.zh-en.srt`, text identical; the part SRTs together hold the
    same 517 cues (`report-pairs.md`).
  - Four `.zh-en.srt` cues have no Chinese characters in the Chinese row: 90, 225, 398, 401 (accepted A2).
- **Chapters:** 16 entries, titles equal to `video.yaml`'s in order, each start within 0.88 s of the running total of
  the scene renders (rounded down). `chapters_part1.txt` (8 entries) and `chapters_part2.txt` (8, at 00:00, 01:50,
  03:50, 05:50, 07:34, 10:04, 12:04, 13:40) match, part 2 offset by −913.5 s. `README.md` now carries them and the
  durations.
- **Scenes:** all 16 present and in order; the chapter starts match the scene durations, so no scene is missing or
  doubled.
- **Narration:** 159 SAY lines, 4,315 words, 150.1 wpm over 1,724.8 s of voice; 613 anchors; no "anchor not found" in
  the 16 render logs.
- **Lecture tags:** 23, each found in the video within 0.4 s of its events, none overlapping, none outliving its
  picture (`tags-r2/`).
- **Privacy:**
  - No instructor name on screen (sampled frames) or in the subtitle text and `transcript.md` (`report-visual.md`,
    `report-measured.md`); no key-like string, long digit string, service-account email or image hash in any
    subtitle file (`report-measured.md`, `report-pairs.md`).
  - Project, account and bucket values on screen are the README's placeholders (`YOUR_PROJECT_ID`,
    `YOUR_GLOBALLY_UNIQUE_*`, `YOUR_GOOGLE_ACCOUNT_EMAIL`); the visible sha256 digest and git commit are public
    identifiers.
- **Provenance** (`ASSETS.md`):
  - Terminal lines come from the 2026-11-04 captures in `assets/terminal/`; each README command ran exactly as
    written, in README order, with extras tagged `extra`.
  - Live: the clone at `46cc62f`; the README's `docker run` of the public image on an empty engine (digest
    `sha256:c17b6db0…dbe72e`, equal to README:1069) and gunicorn's start and Ctrl-C shutdown; the page and the JSON
    routes (200, 405, 400, 503); `docker ps`/`top`/`inspect`; `uv sync --frozen` and `uv run … serve`; the image's
    `batch` command with its honest failures (speech disabled, no identity, the one-chip and no-command mistakes);
    the helper's dry run; the lifecycle scripts' plans; Part 1's handler under functions-framework 3.10.2 (tagged
    `local stand-in`).
  - Every gcloud box to its first error: `gcloud/05` (placeholder project ID), `gcloud/18` and `19` (no active
    account), `gcloud/09` and `10` (upload and helper).
  - `recorded` from the README and its GIF captions (`expected/part1–part4-*-recorded.txt`): the function's answers,
    the deployed service, speech, the job's files. The console is an `illustration` with the README's field values,
    never a screenshot.

## Not claimed

- **No human listened to this cut** or watched it. The listening gate rests on the series waiver quoted under gate 6,
  and the audio was checked only by machine (the ASR round trip and the onset check). The ASR listen items are
  unresolved by ear.
- **The ASR and visual checks ran on the round-1 cut** (probed at 01:46, 110,421,291 bytes; the ASR logs date from
  01:35, so the cut itself is older), not on the final files. The fix
  round changed five tag spans and two zh items, kept every scene's duration (both cuts: 1856.644 s, 111,393 frames)
  and the narration, and the round-2 tags and pairs checks covered the changed tags and cues; the rest of the burned
  copy was not re-inspected frame by frame. The round-1 measured check returned nothing beyond "Waiting for the decode
  run."; round 2 measured everything.
- **The Chinese subtitles were reviewed by agents only:** the QA subtitle watcher, the narration/subtitle fixer, the
  scene verifiers and the final pairs check. No human translator or native reviewer read them.
- **No Google Cloud step ran.** The recording had no project, no account, no credentials and no browser. The console
  steps (project, billing, region, the function's console form, the service's form, IAM, the runtime accounts and
  roles, the buckets, the job form), the deployed function's and service's answers, Cloud Build, the speech call, the
  job's execution, its logs and files, every gcloud success, the helper's real run and the clean-up are drawings,
  the README's own recording (`recorded`), the code's own prints or narration. Whether today's console still matches
  the README's field values was not checked.
- **No Docker Hub push and no Mac run.** Only the public image was pulled. The laptop was Docker Engine 29.8.2 (dind)
  on linux/amd64; the Apple Silicon platform warning is described, not captured. Captures `laptop/20`–`48` ran on the
  public image re-tagged with the recording proxy's CA added (`ASSETS.md`, "capture-only"); `10` and the digest check
  ran on the untouched image.
- **The visual check sampled one frame every 3 s**, plus targeted frames; it did not open three of its own pulled
  frames (`f_243.png`, which it labels 14:43 but is 04:03; `f_924.png`, 15:24; the extra end frame). The verifier
  of this record opened the same 04:03 and 15:24 frames re-extracted from the final burned copy (pixel-identical to
  the round-1 ones; `verifier/frames/v_243.png`, `v_924.png`). Motion between samples was checked only by `freezedetect` and by the
  tags check's 10 fps scan of the tag region.
- **Some QA fixes were verified only on previews** (720p or `-q m` frames, before the 1080p60 renders), not one by one
  on the final cut; several subtitle fixes were checked on estimated timings. The final-cut checks cover them only by
  their own sampling and reading of every cue.
- **Review bots:** no `QA_FOLLOWUPS.md` exists for L14 and nothing in this record checks Bugbot threads on the L14 PR.
- **`README.md` durations and chapters were filled in this pass** from `measured.json` and `chapters*.txt`; its
  chapter summaries were not reviewed by a separate agent.
- **Every check in this record is an agent's.**
- **Verifier pass (2026-11-05):** an adversarial agent re-probed the four MP4s, re-ran `ebur128` on all four, recounted
  and re-timed every cue, re-derived the ponder, chapter and anchor numbers, recounted the QA output, and re-extracted
  frames (`build/final-review/verifier/`); its corrections are in this file. It did not re-run the ASR, the full
  contact-sheet pass or the tag scan.
