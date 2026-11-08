# Review record: AC215 · Lecture 23 — Final deployment and review (Ansible on one EC2 server, then a commit that redeploys)

Follow-along of the Lecture 23 tutorial, *Final Deployment and Review*, in its AWS variant
[dlops-io/cheese-app-aws](https://github.com/dlops-io/cheese-app-aws) `main` @ `5950118` (2024-11-21, "cleanup"; the
only branch and still its head on 2026-11-08, `assets/terminal/laptop/01`, `03`): the README top to bottom (IAM policy,
user and keys, the EC2 key pair, the toolbox, the six `ansible-playbook` commands, nginx, the delete) and the GitHub
Actions workflow `.github/workflows/ci_cd_aws.yml`, which the README never mentions. The lecture's slides speak Google
Cloud; the video maps them onto the AWS repository (series decision on issue #125, as L15 did). Claude Code sessions
(Claude) produced it. Verified facts and unclaimed reviews are kept in separate sections.

- **Origin:** issue #125. Built on 2026-11-08 by this coordinator's agents: digest, live captures, brief, script,
  `scenes/common.py` and 16 scenes, zh subtitles, `exercises.md`, `README.md`, `SLIDES.md`. Build-complete commit
  `dff8b59` (08:01 UTC, "build complete; SLIDES.md credits the course staff and masks names"); draft subtitles `f802db7`
  (08:28).
- **Captures:** 2026-11-08 01:13–01:20 UTC (`ASSETS.md`), a fresh Ubuntu 24.04.5 "laptop" container with Docker Engine
  29.9.3. **No AWS account, no real key, no GitHub credentials.** Live: the clone, the `secrets/` folder, every
  `docker-shell.sh` run (`sh` → `Syntax error: redirection unexpected`; the Helm `curl: (60)` build failure and the
  build without Helm, 132.8 s), the toolbox (ansible 6.7.0 / ansible-core 2.13.13 on Python 3.8.10, from the unquoted
  `ansible>=9.0.0`) and, at its prompt, all six README playbooks verbatim and in order, each to its real first error
  (`UnrecognizedClientException` / `AuthFailure` for fake keys, `Could not resolve hostname external_ip`, and the delete's
  own `'dict object' has no attribute 'group_id'`). The workflow's `run:` scripts ran by hand to their first error
  (`laptop/50`–`53`). Local stand-ins (Chroma 1.0.0 → 410, 0.5.18 → 200; nginx routing, `laptop/60`–`68`) are tagged
  `extra` and called stand-ins. Masking at capture time: account id → `YOUR_ACCOUNT_ID`, server IP → `<EXTERNAL_IP>`,
  committed `NEXTAUTH_SECRET` → `<nextauth-secret>`, the instructor's name → `‹instructor›`.
- **What could not run, and how it is shown:** the AWS consoles (IAM, ECR, EC2, key pair), the server's side, the browser
  and GitHub's pages (secrets, the Actions run) are `illustration`s; the README documents no output, so there is no
  `expected/` folder and nothing is `recorded` (`ASSETS.md`, "What cannot run here").
- **Slides:** `SLIDES.md` (38-page deck, credited to "the course staff") is redrawn, never shown; 16 "Lecture 23 ·
  slide(s) …" tags in the cut (gate 2).
- **QA draft:** the 480p draft, 29:52 (`build/qa/draft.mp4`; subtitles in `build/qa/`).
- **Whole-video QA:** output `/root/ac215-backup/tasks/l23-qa-wkrp62r0f.output` (2026-11-08 10:51 UTC), key `result`. 34
  agents: seven watchers, 12 scene fixers, one narration/subtitle fixer and 14 verifiers; the run log reads "L23: 56
  issues from 7/7 watchers". Fixes committed in `66f76e9`, `048328c`, `d306bcd`, `b5af081`, `a270e73` and `9237274`
  (09:13–10:52 UTC; the last one "QA round applied; no scene ids on screen (12 chips reworded); script SHOW synced").
  `0336fae` (10:35) tracks the redacted `.env.*` copies (see below).
- **Finishing pass:** none. The coordinator's list of finishing-pass outputs for L23 is empty (`[]`).
- **1080p60 renders:** all 16 scenes, render logs `build/logs/` written 11:02–11:32 UTC; S09 and S15 re-rendered in fix
  round 1 (logs 12:51 and 12:50). None of the 16 logs contains "anchor not found" (this record's writer grepped them).
- **Final cut:** 30:10.3 (1810.34 s); parts 18:17.9 (S01–S10) + 11:52.5 (S11–S16). First stitch `7bbc126` (12:09 UTC).
  Current files (UTC, 2026-11-08): the clean cut and the full-cut subtitles 12:55; the burned copy, `chapters.txt` and
  `transcript.md` 13:13; part 1 13:14; part 2 13:15; subtitles committed in `d40531a` (13:16). The MP4s are not in Git
  (release assets).
- **Final-cut checks:** two rounds; the coordinator saved each check's returned text as
  `build/final-review/report-{tags,asr,visual,pairs,measured}.md`, round 1 kept as `report-*-round1.md`. All five reports
  exist and were read in full for this record.
  - Round 1 (first stitch): tags pass (16 tags, four timing notes); ASR no blocking problem; measured pass (notes: the
    three-times repeat at 12:47, ponder spacing); visual **F1** doubled backslash in the burned subtitle at 29:58 (must),
    **F2** the S15 ponder card over the README chip (26:30–26:36), **F3** a grey flash on the S09 terminal (15:07.2);
    pairs **F1–F5** (one clause swap, three repeated English lines, one command split) and six smaller drifts.
  - Fix round 1 (below, "Fix round after the final-cut checks"): toolkit backslash fix, zh re-cuts, S09 and S15
    re-rendered (same lengths), re-stitched and re-burned. Still 30:10 (part 1 18:17, part 2 11:52).
  - Round 2 re-ran **tags, visual, pairs and measured** on the files now in `output/`: every round-1 item verified, no
    regression, measured passes.
  - **The ASR report is round 1's** (`report-asr.md` is byte-identical to `report-asr-round1.md`), run on the first
    stitch. The English `.srt` did not change: this record's writer compared the current `.srt` with `asr.json` (485 cues
    each, identical text, identical start and end times). The audio of the re-rendered S09 and S15 was not transcribed
    again (the loudness of the whole cut was re-measured).

**Conventions:**
- **Times** are mm:ss in the full cut (`output/ac215-l23-final-cicd.mp4`, 1810.34 s), except in "Whole-video QA", which
  keeps the 480p draft's times (marked *draft*).
- **Cue numbers** name their file: `.srt` (485 cues), `.zh.srt` (424) or `.zh-en.srt` (506). An unlabelled cue number
  is a `.srt` cue in the gates and the ASR items, and a `.zh-en.srt` cue in A2–A4 and the pair drifts D1–D4.
- **Evidence paths** are relative to `build/final-review/`. That folder is git-ignored and exists only in the producing
  session; a successor re-runs the checks to reproduce it.

## Content gates (AGENTS.md)

1. **Hook** ✔. S01 opens on a broken thing and a question, not a value proposition.
   - "This repository has 39 commits, and 33 of them carry the same message:" "/run-deploy-app." (`.srt` cues 1–2,
     00:00.0–00:05.9); "That sentence is a button." (cue 3, 00:07.6); "And once, the slash leans the other way." (cue 5,
     00:13.3); "and nothing runs at all." (cue 7, 00:18.7); "How does a sentence deploy a server, and why did one
     character stop it?" (cue 9, 00:21.7).
   - **Payoff:** S12's sieves: "And the commit from the opening? Its slash is a backslash." (cues 335–336, 21:17.8–21:21.3)
     "That's the one character." (cue 338, 21:26.2); and Test yourself Q5 lists `\run-deploy-app` (cue 483, 29:58.5;
     the subtitle shows one backslash since fix round 1).
2. **Intuition before formalism, with an animated mechanism for each core idea** ✔. `BRIEF.md` ("Visual set pieces")
   defines eight, each animated beside the files and captures it explains:
   - **V1, two sieves on one sentence (`KeywordSieves`):** S01's 33-vs-1 count and the bounce; S12 (20:08) drops four
     ribbons (`update readme`, `fix typo /run-tests`, `/run-deploy-app`, `\run-deploy-app`) through `ci_cd_aws.yml:9`'s
     `/run-` and `:100`'s `/run-deploy-app` (ponder 3).
   - **V2, slide 19's map in AWS words (`TermMap`, S02, 01:19):** the GCP labels transform one by one into one EC2 server,
     ECR, Ansible, IAM key + EC2 key pair, `/run-deploy-app`, nginx; slide 6's five cards become this repo's scorecard
     (tags T02–T03, 01:19.5–02:31.9).
   - **V3, two secrets and every place they end up (`KeyJourney`, S03, S06, S08, S13, S16):** the access key from the CSV
     to the toolbox, Ansible, the server and the four GitHub secrets; S16's instance role and OIDC remove most copies.
   - **V4, inventory → play → task → module (`AnsibleMachine`, S04 04:49, S07, S08, S09):** `hosts: localhost` sparks in
     the toolbox, `hosts: appserver` over SSH; the PLAY RECAP counters; `when:` tiles greyed in S15.
   - **V5, one crate, the laptop's Docker (`SiblingContainers`, S05, S06 08:45, S13):** `docker build` inside the
     toolbox travels down the socket and lands on the laptop's shelf (ponder 1).
   - **V6, one tag from `date` to a running container (`TimestampTrail`, S07 10:39, S14 23:53):** the GREEN tag card into
     three ECR shelves and `.docker-tag`; in S14 through `DOCKER_TAG` and `--extra-vars` to recreated containers, with
     L22's rolling update as a contrast inset (tag T13, 24:47.4–24:59.6).
   - **V7, one server, five containers, one front door (`VmLayout`, S08 12:14, S09 14:16, S10 16:18, S16):** the security
     group's three open doors, Chroma's `latest` → 410 and `0.5.18` → 200 on the stand-in, nginx cutting `/api` off
     `/api/newsletters` (ponder 2); reused as S16's review board (T16, 27:50.8–28:45.5).
   - **V8, the lecture's loop and the release button (`ReleaseLoop`, S11 18:17, S14, S16):** slide 7's loop, slide 36's
     Release box, this repo's Codebase → Build → Release → Deploy with Test dashed, slide 12's delivery/deployment toggle
     (ponder 4; T06–T11, 18:17.8–20:08.6).

   **Lecture slides:** a GREY "Lecture 23 · slide(s) …" tag top right, **16 tags** in the cut (`report-tags.md`): S01 1,
   S02 3, S10 1, S11 6, S12 1, S14 2, S15 1, S16 1; none in S03–S09 and S13. The deck is redrawn, never shown.
   - All 16 pass (round 2, four frames per tag in `tags-r2/`): each on screen while its picture is up, "slide" for one and
     "slides" for several, no overlap, none outliving its scene, no tag carrying a scene id.
   - Cosmetic timing notes, unchanged since round 1: T05 (16:18.6–16:30.2) spends its last 3.5 s over the V7 transform;
     T07 (18:32.2) arrives about 1.7 s before the Release box; T15 (27:09.5) precedes its "cost is a CD challenge" chip
     (about 27:19.1). The tightest gap is T15 to the "illustration" chip, about 25 px, clear.
3. **Pause-and-ponder moments and a recap**: ✔ for the ponders, by Conny's decision for the series; ✔ for the recap.
   - **Ponders:** five, each a card with the question spoken, then a silent linear timer; the answer starts when it ends
     (`measured.json` "ponders"; questions from `script.md` lines 616, 859, 954, 1103, 1120; answers from the `.srt`).

     | # | scene | question (from `script.md`) | asked | timer | answer starts |
     |---|---|---|---|---|---|
     | 1 | S06 | Inside the toolbox, Ansible runs docker build for the frontend. Whose disk does the image land on: the toolbox's, or your laptop's? | 09:01.6 (cues 143–144) | 09:10.5, 8 s | 09:19.1 "Your laptop's." (cue 145) |
     | 2 | S10 | The browser asks nginx for /api/newsletters. Which path does api-service receive? | 16:47.3 (cues 264–266) | 16:57.9, 8 s | 17:06.5 "/newsletters." (cue 267) |
     | 3 | S12 | You push 'fix typo /run-tests' to main. Nothing, build-and-push only, or a full deploy? | 20:41.8 (cues 327–328) | 20:48.6, 8 s | 20:57.2 "Build and push only." (cue 329) |
     | 4 | S14 | By the lecture's definitions, is typing /run-deploy-app continuous delivery or continuous deployment? What would make it the other? | 25:44.0 (cues 408–411) | 25:52.7, 10 s | 26:03.3 "Delivery." (cue 412) |
     | 5 | S15 | cluster_state=absent. Which of these three tasks run? | 26:23.2 (cues 419–421) | 26:30.8, 8 s | 26:39.4 "Run it exactly as written." (cue 422), then "Security group, skipping." |

   - **Rate:** 5 cards in 30:10.3, one per 6.03 minutes (`measured.json`: 0.33 per 2 minutes), against AGENTS.md's aim of
     one per 2 minutes. Part 1 has 2, part 2 has 3. The first timer starts at 09:10.5; gaps between timers 467.4, 230.7,
     304.1 and 38.1 s (the last two 38 s apart).
   - **Decided by Conny (2026-10-21), as recorded in `videos/ac215-l05-rag/REVIEW.md` gate 3:**
     「我觉得可以保留现在的密度」: keep the current density of 3–5 ponders per lecture plus a spoken recap and test
     questions. L23's five ponders are inside that series density and below AGENTS.md's aim.
   - **Recap:** S16 "The course on one server, and recap" from 27:50.8 (139.48 s, to the end).
     - 27:50.8–28:45.0: the lecture's review (slides 21–37) placed on the server (cues 443–458).
     - 28:45.0–28:59.2: where next: tests in front, a role and OIDC instead of copied keys, HTTPS (cues 459–462).
     - 28:59.2–29:18.1: "Once more, the path." in six lines (cues 463–469).
     - 29:18.1–30:06.1: "Test yourself." and five questions (cues 470–484); "Answers are in the exercises." (cue 485).
     - Part 1 (18:17.9) has no recap of its own; it ends on the clean-up warning added in QA ("If you stop here, terminate
       the instance and delete its 50 gigabyte volume in the EC2 console today", cues 282–284, 18:02.0–18:13.0) and the
       bridge "Next, a commit message does the redeploy." (cue 285, 18:13.4).
4. **Narration written for the ear, with word-anchored cues** ✔.
   - **Spoken style:** commands, paths and identifiers are spoken in words with the literal form in the subtitle's
     `en_display` (e.g. "ansible playbook, deploy docker images, dash i, inventory dot yaml"; "line 151" shown as
     `deploy-setup-containers.yml:151`, cue 231 per `report-asr.md`; `script.md:276`).
   - **Size:** 136 SAY blocks, 4,323 words (`measured.json`), 23 words (0.5 %) above `BRIEF.md`'s 3,900–4,300 band after
     the S10 clean-up sentence added in QA. Kokoro `af_heart` at speed 0.9: 1,668.3 s of voice (92.2 % of the runtime),
     155.5 wpm over the voice and 143.3 wpm over the runtime.
   - **Anchors:** 560 `wait_until` anchors across the 16 scene files (S01–S16: 23, 26, 36, 33, 39, 33, 36, 44, 35, 28, 35,
     34, 46, 51, 27, 34). None of the 16 render logs contains "anchor not found".
   - **Pronunciation:** the QA ASR watcher found 0 real problems in 483 cues (two observations: "git" heard as "get" at
     *draft* 24:53–25:08, NEXTAUTH once as "next off"; Kokoro's phonemes are correct for both). The final ASR found no
     mispronunciation that blocks understanding and no swallowed word; two minor notes (open, below).
5. **Simulated-target-viewer QA over the full draft** ✔.
   - Seven watchers reviewed the 480p draft: a director and a simulated target viewer ("newcomer") per part, a subtitle
     watcher, a follow-ups watcher and an ASR watcher, from contact sheets, frames pulled from the draft, re-rendered
     frames, the scene code, the subtitle files, the README, `ci_cd_aws.yml` and the captures.
   - **56 timestamped findings: 6 must, 27 should, 23 nit.** Every must was fixed and checked by an independent verifier;
     what stayed open is listed under "Whole-video QA".
6. **Measured checks** ✔. The numbers are under "Verified" (`measured.json`, round 2, measured on the final files).
   - **Duration:** 30:10.3 (1810.340 s), inside the series' 25–35 min. The parts are 18:17.9 (1097.912 s) and 11:52.5
     (712.548 s); they sum to 0.120 s more than the full cut; part 1 ends on the S10/S11 boundary (1097.83 s, a blank
     frame).
   - **Loudness:** −16.1 LUFS integrated in all four files; LRA 2.3 LU; true peak −2.7 dBFS (part 2 −2.9).
   - **Caption bounds** (`report-measured.md`, `report-visual.md`, `report-pairs.md`): every one of the 506 `.zh-en.srt`
     cues is exactly two lines, one per language; the burn file `.zh-en.ass` uses `WrapStyle: 2` (no wrap) at PlayRes
     1920×1080 and its 506 Dialogue lines match the SRT. The widest Chinese lines (59 half-width units: cue 123, 07:27.7, and
     cue 332, 20:02.6) and the widest English lines (89 characters: 19:01.5 and 19:39.7) fit on their burned frames
     (`pairs-r2/band_00-07-30.0.png`, visual round 2; this record's verifier pulled 20:02.9 and 19:40.5 to
     `verifier/band_1202.9.png`, `verifier/band_1180.5.png`); by a PIL estimate the widest line (cue 332) is about
     1480 px against a 1840 px safe width. The subtitle band
     (about y 990–1065) sits below every terminal and code panel (`frames/r2/subs_spotcheck_10.png`).
   - **Music balance:** does not apply. L23, like the other AC215 lectures, has no score: neither `video.yaml` nor
     `BRIEF.md` mentions music.
   - **Subtitle sync** (`report-asr.md`, onset check with base.en word timestamps and a 20 ms RMS envelope over all 485
     cues): every English cue lies inside a rendered voice block (±0.1 s, `report-measured.md`); only cue 263 (16:43.1)
     starts more than 1 s before its audio (about 1.2 s; open nit).

   **Human review:** the series waiver stands in for a listening sign-off.

   Listening sign-off: waived by Conny for the AC215 series (Explainer_Videos#29, 2026-10-15): 「不需要，我现在对视频质量很满意的」 — no human listened to this cut; the ASR round trip below is the substitute.
   Review moments optional since 2026-10-22 (AGENTS.md): 「我大概率是不会进行审片的，因为我觉得做得已经非常好了，就让bugbot来检查就好了」

   **ASR round trip** (`report-asr.md`, round 1, on the first stitch with the same narration and an identical `.srt`;
   see the header):
   - faster-whisper `base.en` (2 threads) over the whole 30:10 cut: 485 cues compared, 4,230 words recognised, 232 cues
     with some difference (`asr.json`, `asr.log`).
   - `large-v3-turbo` re-ran 33 doubtful cues on their own clips (cue span ±0.3 s, `asr_large.json`, `clips/`). Every
     word base.en lost is spoken (e.g. cue 267 "/newsletters." after the 8 s ponder, 17:06; cue 145 "Your laptop's.",
     09:19; cues 400–403, git, 25:11–25:23).
   - The rest is recogniser noise: numbers, spoken punctuation, identifiers heard the lexicon's way (nginx "engine X",
     kubectl "cube control"), homophones, words moved across a cue boundary; DOCKER_TAG and EXTERNAL_IP heard as "docker
     tag" and "external IP", as intended. **Real problems: 0 blocking**; two minor notes (cue 263's late start, cue 285's
     "the redeploy").

## Whole-video QA (480p draft, 29:52; times are *draft* times)

**Watchers and findings** (`l23-qa-wkrp62r0f.output`, key `result`):

| watcher | must | should | nit |
|---|---|---|---|
| director, part 1 | 2 | 5 | 8 |
| newcomer, part 1 | 2 | 6 | 3 |
| director, part 2 | 1 | 3 | 2 |
| newcomer, part 2 | 1 | 3 | 3 |
| subtitles | 0 | 10 | 7 |
| follow-ups | 0 | 0 | 0 |
| ASR | 0 | 0 | 0 |
| **total** | **6** | **27** | **23** |

- **By target:** 27 scene, 21 subtitles, 4 shared code, 4 narration.
- **By kind:** 23 subtitle, 17 follow-along, 9 picture, 2 text, 2 continuity, 1 sync, 1 pacing, 1 fact.
- **By scene:** S05 8, S15 6, S09 5, S10 5, S13 5, S02 4, S06 4, S12 4, S14 4, S16 3, S01 2, S03 2, S07 2, S08 2.
- **Facts:** the part-1 director found the facts on screen matching the captures and the digest (39/33 commits, nine ECR
  actions, step 9 of 15, 132.8 s, 11 and 38 tasks, 1.0.0 → 410 and 0.5.18 → 200); the part-2 director found the
  workflow lines, the eleven step names, the five `-e` variables, `TAG_CI 20261108011909`, capture 53's error lines and
  the teardown's skipping/skipping/`group_id` failure matching `ci_cd_aws.yml`, `inventory.yml` and the captures. No
  watcher found an instructor or staff name, key, account id, IP or ARN on screen or in the subtitles.
- **Follow-ups watcher:** found no `QA_FOLLOWUPS.md` for L23 and no deferred scene bug elsewhere (`build/review_*.md`,
  scene sources); the 16 draft render logs show only routine Manim warnings.
- **ASR watcher:** 483 cues, 231 differing, 4,188 words, 0 real problems; 18 passages re-checked with large-v3-turbo.

**The musts, and how each was fixed** (fixed by the scene fixers, checked by the verifiers on fresh frames):
- **S09 *draft* 14:27, Chroma stand-in output with no command typed** (director part 1): the scene now types `laptop/60`
  lines 1, 3, 4 and 6 and `laptop/61` lines 1–4, each curl with its answer under it; `/api/v1/heartbeat` flashes red with
  `HTTP 410`; each block ends with a dimmed `docker rm -f vector-db >/dev/null` "clean up before the next test" (also
  closes a should). S09 grew 4.7 s.
- **S10 *draft* 17:09, nginx stand-in answers with no curl shown** (director part 1): block 3 types the three curls
  (`/api/newsletters`, `/`, `/api`) with each answer under it; the `for …` chips are gone. The `-v` path that the shared
  `Terminal.fold` broke mid-word (should) is now hand-folded (`ROWS62`, asserted to equal the captured command).
- **S05 *draft* 07:00, and 08:00 / 08:21, `sed` folded inside single quotes** (newcomer part 1, two musts; also a
  director should): `fold_rows` now breaks only at spaces outside quotes; an over-long quoted expression gets its own
  row cut with `…` and a GREY tag "cut · full command: study guide"; the full result shows in the output lines below.
- **S15 *draft* 27:27, `cd … && git status --short` scrolled its first row off** (director part 2; also a newcomer
  should): the strip keeps both command rows and grows to 5 rows as the "your edits" card collapses into the output.
- **S13 *draft* 21:42, "a fork works too" chip** (newcomer part 2, fact): a fork of the public repo is public and
  S14's `git add .` would publish the account id and `NEXTAUTH_SECRET`; the chip now reads "not a fork: a fork of a public
  repo is public".

**The shoulds, by kind** (fixed and verified, except those under "Still open"):
- **Follow-along:** S03's grep now shows the third file (`ci_cd_aws.yml:81`) when the narration says "in three files",
  and a YELLOW "wait: name it ac215_2024 · see next" chip sits beside the key-pair "your turn"; S05's "Helm download site"
  gets a tag "this curl: `baltocdn.com/helm` · Dockerfile:33"; S07's `docker system prune -a` gets a red "demo · don't
  answer y" chip; S09's "check it there" gets an "on your server: …:<your tag>" chip; S13 gets a dashed "push refused
  without `workflow` scope? … not tested" chip; S14's strip keeps the whole `UnrecognizedClientException` row; S15 adds
  "committed earlier? status is clean: your edits live in your history".
- **Narration:** S10 gets one new sentence ("If you stop here, terminate the instance and delete its 50 gigabyte volume
  in the EC2 console today: the README's delete step fails, as part 2 shows."), and the verifier added GOLD cost tags for
  it; the fixer deliberately did not suggest the README's delete, which fails (S15).
- **Pictures and pacing:** S12's sieves no longer flash green before any ribbon (a purple outline instead), and its "job
  skipped · nothing runs" chip stays until "You push".
- **Subtitles:** 17 of the narration/subtitle fixer's 24 items applied in `g1.yaml`/`g2.yaml` (clause order at S06 09:50,
  S07 11:05, S12 20:40; terms kept whole: "key pair", "prediction web page", `git commit -m`, 站在, 设为, 会不会, 第四 and
  四条信息 with their questions; "Four ../"); `python -m explainer.i18n check … --lang zh` printed OK.
- **Scene ids on screen (coordinator, `9237274`):** 12 chips that named internal scene numbers were reworded ("no
  ecr:CreateRepository → the image build", "remember both", "after the server exists", "mounted earlier", "(part 2)",
  "(part 1)", "inventory.yml · after the switch", "your earlier edits", "part 1 · set_fact: env or .docker-tag", …);
  S12's "typed in S14" chip had been reworded by its fixer ("you type them later"). Round 2's visual check found no
  S01–S16 text in any tile and the measured check none in the nine subtitle files.
- **Nits also fixed:** S01's question card stays top left; S02's "Commits" label clear of the GitHub box; S05's
  account-id chip gets "no AWS CLI yet? AWS console, top-right menu"; S06 shows the toolbox's Python 3.8.10 line; S09's
  stand-ins tagged "made off screen" and the nginx row dimmed until step 13; S10's shrunken browser keeps its address
  row; S14's stray dot (a check mark flying from the frame centre) fixed in the scene; S03's erratum card spacing ("name
  yours ac215_2024").

**Still open after QA, and why:**
- **zh spoken forms of identifiers** (subtitle nits: S09 DOCKER_TAG → "Docker tag 变量", S08 EXTERNAL_IP → "external IP",
  S05 here-string (<<<) → "here string", S04 NEXTAUTH_SECRET → "NextAuth secret"): deliberate. The zh checker rejects
  underscores, brackets and `<` in a zh line without a `say:` field, and the series has no Chinese voice (glossary rule
  A9); the English line shows the literal through `en_display`. Accepted (A3).
- **S16 *draft* 29:45, Test yourself Q5 repeats the S14 ponder** ("And is this pipeline delivery or deployment?", cue
  484, 30:03.3): a nit; the narration fixer's rules allow SAY edits for musts and shoulds only, and the card in
  `s16_review.py` would change with it. `exercises.md` answers the reworded question. Open.
- **S13's push-scope warning is on screen only** (dashed chip, "not tested"); the optional narration sentence was not
  added (it would change S13's length and the subtitles).
- **Shared code requests** (toolkit, not this episode): `Terminal.fold` should never break inside quotes or mid-word
  (worked around in S05 and S10); `common.state_mark("idle")` has an unpositioned inner mark (patched in S14);
  `TermMap`'s label placement (patched in S02); the English `.srt` wraps inside noun phrases ("the account ¦ ID",
  "compose ¦ file", …) and the `.zh.srt` wrapper breaks 账号 ¦ ID (`.zh.srt` cue 356, 25:12.0). Not re-checked one by
  one on the final cut except as noted.
- **S15 *draft* 27:30, the three `git status` rows start a few pixels apart** (shared nit): not fixed; not re-checked on
  the final cut.
- **`.zh.srt` cue at 13:42.7 breaks inside the quoted error** ("UNREACHABLE：Could not resolve" / "hostname external IP，
  这是我们的占位符"; glossary G3), found by the S08 verifier: still so in the final `.zh.srt`. The burned `.zh-en`
  copy keeps the phrase on one line.
- **The study guide** must list the full `laptop/22`, `27` and `30` commands, one per line, because S05's "cut · full
  command: study guide" tag points there; nobody in this run confirmed it.

## Final-cut checks (1080p60, 2026-11-08)

- **Tags** (`report-tags.md`, round 2): 16 tags timed from the `events.json` sidecars plus scene offsets that match
  `chapters.txt` (S10 978.60 = 16:18, S15 1579.83 = 26:19, S16 1670.82 = 27:50); four frames each in `tags-r2/`. No
  defect; the re-rendered S09 (122.083 s) and S15 (90.983 s) kept their durations, so every tag time is round 1's.
- **ASR** (`report-asr.md`, round 1): intelligible throughout; two minor notes (cue 263 at 16:43.1, cue 285 at 18:13.4).
- **Visual** (`report-visual.md`, round 2, on the re-burned `.zh-en.mp4`):
  - 38 new contact sheets (4×4 tiles, one frame every 3 s, 00:00–30:06, about 604 frames), all read
    (`sheets/r2_sheet_01…38.png`), plus exact-time frames (`frames/r2/`) and 10 subtitle spot checks.
  - Every scene ends empty (a frame 0.06 s before each of the 16 ends, brightest pixel 28–29, `frames/r2/ends/`); the
    last ~0.3 s of the film is plain background (30:10.0, 30:10.3).
  - `freezedetect` (4 s) re-run on S09 and S15: 15:27.8 (5.0 s, under narration), 26:31.3 (8.05 s, the ponder timer),
    27:14.8 (4.0 s) and 27:31.6 (4.2 s, under narration with reveals); none a defect. Round 1's freeze log still applies
    to the other scenes (`freezedetect.log`, `freezes.txt`).
  - Transient mid-transition glyphs at 09:33, 11:06 and 23:42, and S02's cross-hatch at 02:12, by design.
  - Series rules on screen: only placeholders (`<EXTERNAL_IP>`, `YOUR_ACCOUNT_ID`, `<aws-access-key-id>`,
    `<nextauth-secret>`, `***`); no instructor or staff name. Shown and noted, not defects: random Docker container ids
    in prompts (`root@a5756497de90`), the README's AWS console link (10:39–10:42), the public Ubuntu image id
    `ami-0e86e20dae9224db8` (05:45–06:09), `github.com/dlops-io/cheese-app-aws` and `<your-user>`.
- **Pairs** (`report-pairs.md`, round 2, 506 cues, all read): F1–F5 and the six round-1 drifts fixed; no cue swaps meaning
  with its neighbour; no English line repeats; one zh and one en line per cue; no IPs, ARNs, `AKIA` prefixes, 12-digit
  account ids, `.com` domains or scene ids in the subtitles; the parts concatenate to the full file. Four optional drifts
  remain (open items).
- **Measured** (`report-measured.md`, round 2, `measured.json`, evidence `r2/`): all four MP4s decode with exit 0 and no
  errors; formats, loudness, subtitles, chapters and durations pass; the round-1 three-times repeat at 12:47 is one cue
  (`.zh-en.srt` 213); the backslash cue renders correctly (`r2/frame_1800.5_subband.png`).

## Accepted items (coordinator decisions)

- **A1. Five ponders in 30:10.3** (one per 6.03 minutes), below AGENTS.md's aim of one per 2 minutes. Accepted under
  Conny's 2026-10-21 decision to keep 3–5 ponders per lecture (「我觉得可以保留现在的密度」); see gate 3.
- **A2. Two deliberate zh exceptions in the burned subtitles:**
  - **S08's AWS credentials error is translated in zh** (`.zh-en.srt` cue 213, 12:50.6: 「AWS 无法验证所提供的访问凭据」
    over "AWS was not able to validate the provided access credentials."): the verbatim quote (about 34 units by
    glossary D8) exceeds the 30-unit zh line (G1), and quoting it whole made the English repeat three times in round 1.
    An exception to glossary A15; the English line keeps the original.
  - **Step 5's zh line drops `-i inventory.yml`** (cue 188, 11:22.3: 「第 5 步：ansible-playbook deploy-docker-images.yml」
    over the full command), like steps 8, 10 and 13; the English line and the terminal show the whole command. The pairs
    check lists it as drift D1; it is intended.
- **A3. zh glossary spoken forms** (rule A9): `DOCKER_TAG` → "Docker tag 变量" (cues 256, 398) and `EXTERNAL_IP` →
  "external IP" (cue 228) are written as spoken words, as are `ci_cd_aws.yml`, `head_commit`, `AWS_SSH_KEY`,
  `NEXTAUTH_SECRET`, `cluster_state=absent` and `group_id`; the English line shows each literal.
- **A4. Four verbatim terminal quotes on the zh line** (`.zh-en.srt` cues 113 "credentials file not found", 227
  "UNREACHABLE", 282 "/newsletters", 444 "EBS volume，skipping"; glossary A15), down from seven in round 1.
- **A5. The tags' cosmetic timing notes** (T05, T07, T15; gate 2) and the visual transients (09:33, 11:06, 23:42, 02:12).

## Open items (nits, left on purpose; none blocks playback)

- **Test yourself Q5 repeats the S14 ponder** (`.srt` cue 484, `.zh-en.srt` 505, 30:03.3, "And is this pipeline delivery or deployment?"; ponder
  4 at 25:44–26:03): changing it needs a SAY edit, a re-voice, the card at `s16_review.py:562`, a re-render and a re-burn,
  for a nit.
- **Four optional pair drifts** (`report-pairs.md` round 2; nothing contradicts the other language):
  - D1, cue 188 (11:22.3): the zh line drops `-i inventory.yml` (deliberate, A2).
  - D2, cues 225–226 (13:37.7–13:42.4) and 288–289 (17:29.2–17:34.0): "run" in the first English cue, 运行 in the second
    zh cue.
  - D3, cues 154–155 (09:23.3–09:28.6): verb and preposition cross over ("talks" / "through the socket").
  - D4, cue 242 (14:41.0): the zh line says 第 151 行 without the file name the English shows.
- **ASR cue boundary at about 16:43** (`.srt` cue 262/263): "9000" is still spoken until about 16:43.6 while cue 263 is up
  from 16:43.06, and its first word starts about 16:44.3: a 1.2 s lead and a split about 0.6 s early. A subtitle-only fix
  (move the boundary to about 16:43.7); left for a nit.
- **"the redeploy" is ambiguous** (cue 285, 18:13.4, "Next, a commit message does the redeploy."): both recognisers
  heard "read-apply"; the subtitle and the context carry it. Rewording ("redeploys the app") needs a re-voice.
- **Single-language subtitle files break inside commands** (outside the burned asset; `report-pairs.md`): `.zh.srt` cues
  161 (11:22), 195 (13:39), 211 (14:59), 244 (17:30) and `.srt` cues 180, 214, 235, 273 wrap a playbook command over two
  lines inside one cue; `.zh.srt` also wraps the 13:42.7 error and 账号 ¦ ID (25:12.0). No cue has more than two lines.
- **Narration 23 words over `BRIEF.md`'s 3,900–4,300 band** (4,323 after S10's QA sentence).
- **Part 1 has no recap of its own** (it ends on the clean-up warning and the bridge to part 2).
- **Chapters:** every start is the scene start rounded down (e.g. S11 18:17 against 18:17.83, S16 27:50 against 27:50.82).
- **Frame rate:** 60 fps (the 1080p60 scene renders, as in L02–L22); the repo default for new episodes is 30 fps. The
  burned copy has one more video frame (108,619) than the clean cut (108,618).
- **Bilibili description:** `video.yaml` `publish.description_zh` (line 72) credits the instructor by name. Not in the
  video or subtitle files, but it goes on the Bilibili page and the series rules say no instructor name.
- **`SLIDES.md` "This video and the slides"** (lines 474ff.) predates the script: it maps the digest's nine planned GCP
  chapters (`cheese-app-v4`), not the 16 scenes. Which scene cites which slide is the 16 tags in gate 2.
- **No `QA_FOLLOWUPS.md`** for L23, and no Bugbot thread was copied into the episode folder.

## Verified (final render)

All numbers are from `measured.json` and the five reports, on the files in `output/` as they are now (written 2026-11-08
12:55–13:15 UTC), except the ASR results, which are round 1's (see the header).

- **Files:** H.264 High, yuv420p, 1920×1080 at 60 fps, AAC 48 kHz stereo at about 172–178 kb/s; one video and one audio
  stream each. Each decodes in full with exit 0 and no errors (`r2/decode_*.log`).

  | file | duration | size (bytes) | loudness | LRA | true peak | SHA-256 (first 12) |
  |---|---|---|---|---|---|---|
  | `ac215-l23-final-cicd.mp4` | 1810.340 s (30:10.3), 108,618 frames | 107,242,448 | −16.1 LUFS | 2.3 LU | −2.7 dBFS | `a3c353f50413` |
  | `ac215-l23-final-cicd.zh-en.mp4` | 1810.340 s, 108,619 frames | 105,565,328 | −16.1 | 2.3 | −2.7 | `3163855611f4` |
  | `ac215-l23-final-cicd_part1.mp4` | 1097.912 s (18:17.9), 65,870 frames | 68,264,773 | −16.1 | 2.3 | −2.7 | `e7af921de00c` |
  | `ac215-l23-final-cicd_part2.mp4` | 712.548 s (11:52.5), 42,748 frames | 38,971,382 | −16.1 | 2.3 | −2.9 | `80e7f3d330e5` |

  The 16 scene renders sum to 1810.297 s (full cut +0.043 s); the parts sum to 1810.460 s (+0.120 s against the full
  cut).
- **Subtitles:** `.srt` 485 cues, `.zh.srt` 424, `.zh-en.srt` 506. Part 1 has 285 / 253 / 301, part 2 200 / 171 / 205; the
  parts add up to the full counts, their text is identical to the full cut's, part 1's timing matches exactly and part
  2's within 0.01 s after the 1097.831 s offset.
  - In all nine files the indexes are sequential, the cues in order, inside the runtime, with no overlaps, no empty cue
    and none shorter than 0.8 s; the shortest are 1.000 s (`.srt`, `.zh-en.srt`) and 1.155 s (`.zh.srt`). The last cue
    ends at 1808.164 s (30:08.2).
  - Every `.zh-en.srt` cue has exactly two lines; no `.ass` line has more than one `\N`; the only backslash in the `.ass`
    files is cue 504's (cue 203 of part 2's) `\` + U+2060 + `run-deploy-app` (29:58.5–30:02.9), drawn as one backslash on both lines.
- **Chapters:** 16 entries, titles equal to `video.yaml`'s in order, each start the floor of the scene's real start
  (rounded to the millisecond first: part 2's S15 starts at 481.9997 s and is listed as 08:02).
  `chapters_part1.txt` has 10 entries, `chapters_part2.txt` 6 (00:00, 01:51, 03:36, 05:36, 08:02, 09:32). `README.md`
  now carries them and the durations (this pass).
- **Scenes:** all 16 present and in order (S01 79.45 s, S02 92.63, S03 117.38, S04 96.48, S05 139.08, S06 113.98, S07
  95.25, S08 122.25, S09 122.08, S10 119.23, S11 111.13, S12 104.98, S13 120.02, S14 145.87, S15 90.98, S16 139.48);
  every scene render is newer than its scene file and `common.py`; every scene ends on an empty frame.
- **Narration:** 136 SAY blocks, 4,323 words, 155.5 wpm over 1,668.3 s of voice; 560 anchors; no "anchor not found" in
  the 16 render logs.
- **Lecture tags:** 16 tags, each checked on frames just after fade-in, mid-span, just before fade-out and 0.5 s after;
  none overlapping, none outliving its scene.
- **Round-1 defects re-checked on the final files:** the backslash at 29:58–30:02 (visual F1; `frames/r2/f_1800.png`,
  `tags-r2/bot/F1_burn_1799.00_band.png`); S15's ponder card cross-fades with the README card in 0.6 s and then sits
  alone (F2; 26:30.5–26:39.2, `tags-r2/bot/F2_sheet.png`); S09's terminal highlight is a thin grey ring, the red
  UNREACHABLE lines stay readable, brightness 29.4–38.8 over 15:04–15:10 (F3; `frames/r2/yavg_904-910.txt`); pairs F1–F5
  and the six drifts (`pairs-r2/band_*.png`, `tags-r2/bot/pairs_burn_bands.png`).
- **Privacy:** no instructor or staff name, key, token, account id or real IP on screen or in the subtitles
  (`report-visual.md`, `report-pairs.md`, `report-measured.md`; QA watchers). The two `.env.*` source copies are tracked
  as `assets/source/src/frontend-react/env.production` and `env.development` (`.gitignore` drops `.env.*`, so CI could not
  render S10 without them; the L22 release failed on exactly this). Their `NEXTAUTH_SECRET` reads `<value not copied: see
  ASSETS.md>`; `scenes/common.py` `_src` reads them under their real names (`0336fae`).
- **Provenance** (`ASSETS.md`):
  - Terminal lines come from the 2026-11-08 captures in `assets/terminal/laptop/`; each README command ran as printed,
    extras tagged `extra`, stand-ins tagged as stand-ins; nothing in a terminal panel is typed by hand. Code panels quote
    `assets/source/` unchanged at `5950118` except the masked values listed in `ASSETS.md`.
  - `illustration`: the IAM/ECR/EC2 consoles, the key pair, the server's side, the browser, GitHub's secrets page and the
    Actions run, the clean-up checklist. Costs are named by GOLD meter tags, never priced.

## Not claimed

- **No human listened to this cut** or watched it. The listening gate rests on the series waiver quoted under gate 6, and
  the audio was checked only by machine (the ASR round trip and the onset check, on the round-1 cut).
- **The ASR check did not run on the final files.** It ran on the first stitch; fix round 1 re-rendered S09 and S15
  (picture changes, same lengths) and changed zh text only; the English `.srt` is identical, but the re-rendered audio
  was not transcribed again.
- **The Chinese subtitles were reviewed by agents only:** the QA subtitle watcher, the narration/subtitle fixer, the scene
  verifiers and the pairs check. No human translator or native reviewer read them.
- **No AWS resource was created.** No AWS account was used: no IAM policy, user or access key, no key pair, no ECR
  repository, no image pushed, no EC2 instance, volume or security group, no `aws configure` on a server, no teardown
  against real resources, no cost measured. The playbooks stop at their first real error, and what they do on a real
  server (11 tasks for the build, 38 for provisioning) is described from the code, not observed. The attach of the 50 GB
  volume was not tested.
- **No GitHub repository, secret, push or Actions run** was made. The workflow's `run:` scripts ran by hand to their
  first error; the run page and the "green run" are illustrations. The `workflow`-scope push refusal is marked "not
  tested" on screen.
- **No GCP step** was followed: the lecture's GKE, Artifact Registry and Pulumi versions are mapped, not run; `SLIDES.md`
  is from the deck's text and renders, not checked against a recording of the lecture.
- **No Docker Hub login or push** is part of the captures; base images came through `mirror.gcr.io` under their Docker Hub
  names (`ASSETS.md`, "Capture-only").
- **The app was never seen running:** the page, the routes on a real server and the recreated containers are drawn from
  the code; nginx's routing was confirmed only on laptop stand-ins.
- **The visual check sampled one frame every 3 s**, plus targeted frames; motion between samples was checked only by
  `freezedetect` (S09 and S15 in round 2, the clean cut in round 1). The two part files were measured (probe, decode,
  loudness, subtitles, chapters) but not sampled visually on their own.
- **Most QA fixes were verified on previews** (720p `--at` frames and `--every 2` sheets before the 1080p60 renders), not
  one by one on the final cut; the final-cut checks cover them by their own sampling and by reading every cue. The shared
  `git status` row alignment (S15) and the English `.srt` noun-phrase wraps were not re-checked.
- **Stated as the coordinator gave them, not checked here:** toolkit PR #130 (the same backslash fix is on this branch as
  `fdfd2ae`); the study guide on MLOps_Learning and whether it lists the three `sed` commands S05 points to; the
  individual script reviews beyond their files.
- **Review bots:** no `QA_FOLLOWUPS.md` exists for L23, and nothing in this record checks Bugbot threads on an L23 PR.
- **`README.md` durations and chapters were filled in this pass** from `measured.json` and `chapters*.txt`; its chapter
  summaries were not reviewed by a separate agent.
- **Every check in this record is an agent's.**

## Fix round after the final-cut checks

- **Round 1 findings fixed** (2026-11-08, 12:33–12:40 UTC; commits `fdfd2ae` and `24fce4d`):
  - Visual F1: the `.ass` export no longer doubles a backslash; it writes `\` + U+2060 (toolkit PR #130, on this branch
    as `fdfd2ae`, "Subtitles: keep a backslash single in .ass").
  - Visual F2: S15's ponder card (`ponder_right`) lands top right as the README card leaves; S15 re-rendered (90.983 s,
    same length).
  - Visual F3: S09's terminal `Indicate` replaced by a thin grey `Circumscribe` ring; S09 re-rendered (122.083 s, same
    length).
  - Pairs F1–F5 and the six drifts re-cut in `g1.yaml`/`g2.yaml`, with the two deliberate exceptions (A2).
  - Re-stitched (12:55) and re-burned (13:13), parts 13:14–13:15, subtitles committed in `d40531a`; still 30:10 (part 1
    18:17, part 2 11:52); every scene duration unchanged.
- **Round-2 checks on the new files** (`report-tags.md`, `report-visual.md`, `report-pairs.md`, `report-measured.md`):
  all items verified, no regressions; measured passes (I −16.1 LUFS, TP −2.7 dBFS). The ASR report is from round 1.
