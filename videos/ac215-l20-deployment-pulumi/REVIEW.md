# Review record: AC215 · Lecture 20 — Deployment: by hand, then Pulumi to a single VM

Follow-along of the Lecture 20 tutorial, *Deployment: Pulumi*, on
[dlops-io/cheese-app-v3](https://github.com/dlops-io/cheese-app-v3) `main` @ `3ecef56` (2025-11-28, "v4->v3"): the README's
*Deployment to GCP (Manual)* (README:4–222), *Deployment to GCP (Single VM Instance)* (README:225–383) and *Delete the
Compute Instance / Persistent disk* (README:387–390), top to bottom. An unmerged staff branch rewrites that README and
`deploy_single_vm/`; it is context only, never followed and never named on screen (`ASSETS.md`, "Which commit"). Claude
Code sessions (Claude) produced it. Verified facts and unclaimed reviews are kept in separate sections.

- **Origin:** issue #112. Built end to end on 2026-11-05/06 by this coordinator's agents: digest, live captures, brief,
  script + four independent reviews (`build/review_{accuracy,followalong,pedagogy,spoken}.md`,
  `build/review_merge_log.md`), `scenes/common.py`, 16 scenes each with a fresh critic, zh subtitles, `exercises.md`,
  `README.md`; the study guide (MLOps_Learning) follows after release. Build-complete commit `daeb2b1` (2026-11-06
  18:49 UTC). Two usage-limit interruptions and container restarts were resumed from run ids; no work was lost (per the
  coordinator).
- **Captures:** 2026-11-05, 22:06–23:42 UTC (`ASSETS.md`, "terminal/"), in fresh disposable containers. The VM
  stand-in is `debian:12` with Docker 29.9.3 from the README's `get-docker.sh`; the laptop stand-in is
  `docker:29.8.2-dind`. Everything that runs on a machine you own ran live: the whole manual deployment on the
  stand-in VM (folders, network, Chroma 1.0.0, the loader's 14,356 chunks, the API, the frontend, nginx 1.30.6 on port
  80), `docker-hub.sh` building the production frontend, the deployment toolbox's build and its two failures, every
  tool check and `ssh-keygen`. The recording had **no Google account, no Docker Hub login and no credentials**: every
  cloud command is shown up to its honest first error (`push access denied`, `invalid_grant: account not found`,
  `PULUMI_ACCESS_TOKEN must be set`, `403 Forbidden`), Pulumi's previews ran on the local file backend (tagged `extra ·
  not for you`) up to their first Google call, and the console, the browser and a successful `pulumi up` are
  `illustration`s; the README's OS Login output is the one `expected` panel.
- **The toolbox as committed does not build** (2026-11-05): `sh docker-shell.sh` stops on Debian 11's archived
  security updates, then on `google-cloud-sdk` having no installation candidate. The video shows the two one-line
  fixes (bullseye → bookworm, `google-cloud-sdk` → `google-cloud-cli`) with the real diff (17:24–18:50).
- **Masking:** the staff branch's name is masked in the captures (`work/‹staff›` in `ASSETS.md`); S02 now types only
  the `git log` command, not the recording-only `sed` that masked it (QA fix, below). Project IDs on screen are
  `ac215-project`, `your-gcp-project` or `<YOUR_GCP_PROJECT>`; OS Login users `sa_000…`; the VM address
  `<instance_ip>` / `<VM IP>`; the private `172.19.0.x` client addresses of the S15 log are printed as `…`.
- **QA draft:** the 480p draft (30:46), subtitles in `build/qa/` dated 2026-11-06 19:17 UTC.
- **Whole-video QA:** run `wf_8b93ad63-b69`, output `/root/ac215-backup/tasks/l20-qa-wk0trso3u.output` (2026-11-07
  05:25 UTC), key `result`. 39 agents: seven watchers, 15 scene fixers, one narration/subtitle fixer and 16 scene
  verifiers. The run log reads "L20: 52 issues from 7/7 watchers". QA fixes committed in `77cd7aa`, `af71b91`,
  `e2ae38a` and `78dc7e5` (2026-11-06 19:52 to 2026-11-07 05:28 UTC).
- **After QA, by the coordinator:** two narration lines the verifiers asked for (S04 "Pause, create yours, and SSH in
  with the SSH button in the VM instances list.", S07 "If you used the echo, rewrite the file this way first. Then run
  nginx…"), with their zh lines; i18n check OK, all 16 scenes re-checked OK (`78dc7e5`, per the coordinator). Lexicon
  PR #118 merged to `main` as `bbe7674` (per the coordinator; the hash is not in this clone).
- **Finishing pass:** none. The coordinator's list of finishing-pass outputs for L20 is empty (`[]`).
- **1080p60 renders:** all 16 scenes, 2026-11-07 05:42–06:13 UTC (`build/logs/`); S05, S06 and S15 re-rendered
  07:31–07:37 after fix round 1 (`4750fb8`, 07:24). None of the 16 logs contains "anchor not found" (this record's
  writer grepped them).
- **Final cut:** 31:09.8 (1869.840 s); parts 13:30.1 + 17:39.8. File times (UTC, 2026-11-07): the clean cut and the
  full-cut subtitles 07:42; the burned copy, `chapters.txt` and `transcript.md` 08:05; part 1 08:06; part 2 08:08. The
  MP4s are not in Git (release assets).
- **Final-cut checks:** two rounds; the coordinator saved each check's returned text as
  `build/final-review/report-{tags,asr,visual,pairs,measured}.md`, round 1 kept as `report-*-round1.md`. All five
  reports exist and were read in full for this record.
  - Round 1 (evidence 06:56–07:24 UTC) ran on the first stitch: no blocking defect; the tags check found the S05 tag
    citing slides 7–8 over slide 8's picture only, the S06 tag readable for about 2 s, and the S15 slide-19 tag staying
    about 7 s past its strip.
  - Fix round 1 (`4750fb8`) changed only `s05_vector_db.py`, `s06_api_frontend.py` and `s15_containers.py`: S05's tag
    reads "slide 8", S06's tag is removed, S15's tag fades with the strip. The three scenes were re-rendered, the cut
    re-stitched and re-burned; every scene duration stayed the same to the millisecond (still 31:09).
  - Round 2 re-ran **tags, visual and measured** on the files now in `output/` (evidence 08:09–08:32 UTC): all three
    items verified, no regression, measured passes.
  - **The ASR and pairs reports are round 1's** (`report-asr.md` and `report-pairs.md` are byte-identical to their
    `-round1` copies), run on the pre-fix cut. The fix round touched no `script.md` or `i18n/` file, and this record's
    writer compared the subtitles (`writer/cmp_subs.py`): the current `.srt`'s 498 cue times and texts equal
    `asr.json` (0 differences), and the current `.zh-en.srt`'s 519 cues equal `pairs-cues.json` (0 differences). The
    audio of the three re-rendered scenes was not transcribed again.

**Conventions:**
- **Times** are mm:ss in the full cut (`output/ac215-l20-deployment-pulumi.mp4`, 1869.840 s), except in "Whole-video
  QA", which keeps the 480p draft's times (marked *draft*).
- **Cue numbers** name their file: `.srt` (498 cues) or `.zh-en.srt` (519).
- **Evidence paths** are relative to `build/final-review/`. That folder is git-ignored and exists only in the producing
  session; a successor re-runs the checks to reproduce it.

## Content gates (AGENTS.md)

1. **Hook** ✔. S01 opens on a broken thing, not a value proposition: one container stopped, and the whole site dark.
   - "We stopped one container, the frontend, and restarted the web server in front of it." (`.srt` cue 1, 00:01.8);
     "The API container is still up, and so is the vector database." (cue 2); "Yet the whole site answers nothing, the
     address of the API included." (cue 3, 00:11.5); "Today's puzzle: the API is running, so why is its address dead
     too?" (cue 4, 00:16.0); "We answer it once we have built this by hand." (cue 5).
   - **Payoff:** S07, "Now the puzzle." (cue 182, 11:54.6) "The web server looks up frontend and api-service once, at
     start." (cue 183) "With the frontend stopped, the restart fails that lookup and exits," (cue 184) "taking the API
     route with it." (cue 185, 12:05.1); then start order and restart policies (cues 186–188).
2. **Intuition before formalism, with an animated mechanism for each core idea** ✔. `BRIEF.md` ("Visual set pieces")
   defines eight, each animated next to the commands it explains:
   - **V1, the lecture's deployment picture (`MasterDiagram`):** the goal, "the containers from your laptop move to one
     virtual machine in Google Cloud, with port 80 the only door." (cues 7–8, 00:27.4–00:32.4); the request path in
     travel order and the fifth container, the loader (cues 25–32, 01:26.0–01:49.4); the four manual stages (cues
     33–34); in part 2 the three containers, the frontend on 3000 not 80, then nginx and port 80 (cues 425–429,
     26:25.8–26:41.8).
   - **V2, containers find each other by name (`NamePhoneBook`):** "Its name goes into the phone book." (cue 108,
     06:54.3); the loader "finds the database by name, cheese-app-vector-db, not by address." (cue 112, 07:06.5); the
     hook's answer at 11:56.0 (above).
   - **V3, one public door and the prefix slash (`ProxyRoute`):** the `location` block on line 35, "one slash", "so
     /api-service/status reaches the API as just /status." (cues 156–160, 09:58.8–10:17.2); after ponder 2, "Port
     9000 is open on the VM but shut at the network edge:" (cue 180, 11:48.3).
   - **V4, desired state in, API calls out (`EngineLoop`):** desired, state from your bucket, `--refresh` against
     reality, "each difference becomes a plan line:" "+ to create, ~ to update, - to delete, +- to replace." (cues
     218–225, 13:58.6–14:29.6). Each glyph now has a visible cause (QA must M1, below): at 14:26.5 desired reads
     Network / Firewall · 80 / a ghost Disk / Instance · image v2 against state and reality's ghost Network / Firewall
     · 22 / Disk / Instance · image v1 (`writer/must_866.5.png`).
   - **V5, the deployment toolbox and its wires (`ControlRoom`):** "Lines 34 to 43 wire it to your laptop. They mount
     the Docker socket, so it builds on your Docker" (cues 278–280, 17:36.9–17:42.6); the two broken bricks and their
     fixes (cues 288–297, 18:11.6–18:39.0); the entrypoint's first error (cue 300, 18:50.0).
   - **V6, two stacks joined by one fact (`TimestampPipe`):** "Line 13 makes a timestamp, down to the second," (cue
     359, 22:21.6); "Lines 34 and 35 export the tag for the other project." (cue 365); every `up` rebuilds "because the
     timestamp is new every run." (cue 376, 23:20.3); the stack reference to `organization/deploy-images/dev` (cues
     420–421, 26:04.2–26:07.9); images stay after destroy, `retain_on_delete` (cues 468–469, 29:21.1–29:26.5).
   - **V7, the VM's fences, then the provisioning dominoes (`VmFences`):** the cloud network and three firewall gates,
     the data disk, the IP as "a sealed envelope that opens once the VM exists." (cues 393–399, 24:13.2–24:34.4); "Nine
     remote commands run in a chain" (cue 409, 25:12.7); after ponder 4, "Scripts Pulumi cannot inspect must be safe
     to run twice." (cue 418, 25:57.1).
   - **V8, three keys, three doors (`KeyRing`):** the two service accounts and their roles, "Why two?" (cues 254–262,
     16:10.6–16:40.3); the OS Login key and its derived Linux username (cues 319–320, 19:53.7–19:57.3; cue 332,
     20:46.1); slide 26's callouts and the code's amendments (cues 437–448, 27:15.9–28:02.0).

   **Lecture slides:** a GREY "Lecture 20 · slide(s) …" tag top right, 31 tags in the final cut (`report-tags.md`): S01
   2, S02 2, S03 1, S04 1, S05 1, S07 1, S08 2, S09 4, S10 3, S11 1, S13 2, S14 2, S15 5, S16 4; none in S06 (removed in
   fix round 1) or S12. Cited: slides 4, 4–5, 7, 8, 8 + 24, 9, 10–11, 12, 13 + 18, 14, 14 + 19, 14 + 20, 15, 16, 17,
   19, 19 + 21, 19 + 22, 20, 23, 24, 25, 25–26, 27, 29. The deck is redrawn, never shown (`SLIDES.md`; its "This video
   and the slides" map was written before the script, so the per-tag table in `report-tags.md` is the scene ↔ slide
   record for the final cut).
   - All 31 tags pass on round-2 frames (`r2/tag_*`, `r2/tagm_*`): each is on screen only while the picture it cites is
     up, "slide" for one and "slides" for several, no overlap in any span (`r2/tag_overlap.py`: at most 1 pixel changed
     by more than 40 levels in any tag box plus a 12 px margin), none on at its scene's end.
   - Accepted: S15's slide-19 tag is now short (item A3).
3. **Pause-and-ponder moments and a recap**: ✔ for the ponders, by Conny's decision for the series (accepted item A1);
   ✔ for the recap.
   - **Ponders:** five, each a card followed by an 8 s timer (`measured.json` "ponder_rendered": each scene's
     `events.json` plus its scene start; card time is when the card starts to fade in; answers from the `.srt`).

     | # | scene | card (from `script.md`) | card | timer | answer starts |
     |---|---|---|---|---|---|
     | 1 | S05 | The loader ran with --rm and is gone. Are the 14,356 chunks gone too? | 07:41.5 | 8 s | 07:50.1 "No. The loader only sent them;" (cue 122) |
     | 2 | S07 | Port 9000 is published on the VM. From your laptop, does http://<VM IP>:9000/ answer? | 11:33.1 | 8 s | 11:41.7 "No. The two ticks opened only 80 and 443; no rule opens 9000." (cue 179) |
     | 3 | S09 | You run pulumi up again, changed nothing. What should the plan show? | 15:23.8 | 8 s | 15:32.4 "Nothing to do." (cue 243) |
     | 4 | S14 | Why blkid … \|\| mkfs.ext4 instead of just mkfs.ext4? | 25:36.6 | 8 s | 25:45.2 "Because formatting erases." (cue 415) |
     | 5 | S15 | The running app needs one key. Which would you hand the VM, and why not the other? | 27:30.8 | 8 s | 27:39.4 "The gcp-service key: …" (cue 442) |

   - **Rate:** 5 cards in 31:09.8, 0.32 per 2 minutes (`measured.json` "ponder_per_2min"), against AGENTS.md's aim of one
     per 2 minutes (about 16). Part 1 has 2, part 2 has 3. The longest stretch without a card is 612.8 s (15:23.8 to
     25:36.6, S10–S13 have none); the first card comes at 07:41.5.
   - **Decided by Conny (2026-10-21), as recorded in `videos/ac215-l05-rag/REVIEW.md` gate 3:**
     「我觉得可以保留现在的密度」: keep the current density, which that record gives as 3–5 ponders per lecture plus a
     spoken recap and test questions. L20's five ponders are inside that series density and below AGENTS.md's aim.
   - **Recap:** S16 "Destroy, recap, and what's next" from 28:54.7 (135.15 s).
     - 28:58.8–29:30.1: `pulumi destroy` in `deploy_single_vm`, in reverse order; images stay, `retain_on_delete`
       (cues 461–469).
     - 29:30.1–29:54.8: the six-item teardown checklist (cues 470–476).
     - 29:54.8–30:07.8: "The recap is the lecture's six steps, each with its file:" (cues 477–479).
     - 30:07.8–30:33.8: the lecture's six principles scored, a single point of failure, Lectures 21–23 (cues 480–487).
     - 30:33.8–31:04.9: "Test yourself." (cue 488) and five questions (cues 489–497); "Answers are in the exercises and
       the study guide." (cue 498).
4. **Narration written for the ear, with word-anchored cues** ✔.
   - **Spoken style:** identifiers are spoken in words where the display differs (QEMU spelled out "Q E M U" in S03,
     `inventory.yml` read "inventory dot yml" and kubectl "cube control" per the lexicon, nginx "engine x" as
     Kokoro reads it with no lexicon entry) with the
     literal form in the subtitle's `en_display`; error strings shown verbatim (`invalid_grant: Invalid grant: account not found`).
   - **Size:** 155 SAY lines, 4,370 words (`measured.json` "narration"), above the script's 3,900–4,300 target after
     the QA additions (S03 QEMU, S12 OS Login, the two coordinator lines); the `.srt` has 4,203 words. Kokoro
     `af_heart` at speed 0.9: 1,746.5 s of voice (93.4 % of the runtime), 144.4 wpm over the voice and 140.2 wpm over
     the runtime.
   - **Anchors:** 585 `wait_until` anchors across the 16 scene files (S01–S16: 23, 24, 34, 39, 34, 33, 45, 11, 40, 33,
     50, 34, 43, 53, 50, 39). None of the 16 render logs contains "anchor not found".
   - **Pronunciation:** the QA ASR watcher found one real ear problem ("And where inside?" heard as "And we're
     inside.", fixed to "But where inside that container?", cue 125, 07:59.5) and one caption that said more than the
     voice (fixed). The final ASR found no mispronunciation; lowercase "pulumi" in command lines comes out short (open
     nit).
5. **Simulated-target-viewer QA over the full draft** ✔.
   - Seven watchers reviewed the 480p draft: a director and a simulated target viewer ("newcomer") per part, a subtitle
     watcher, a follow-ups watcher and an ASR watcher, from contact sheets, frames pulled from the draft, the scene
     code, the subtitle files, the README and the captures.
   - **52 timestamped findings: 3 must, 28 should, 21 nit** (the 3 musts are 2 distinct problems: S09 was reported by
     two watchers). Both were fixed by the scene fixers, checked by independent verifiers, and are verified on the
     final cut by this record's writer (`writer/must_*.png`; see "Verified"). What stayed open is listed under
     "Whole-video QA".
6. **Measured checks** ✔. The numbers are under "Verified" (`measured.json`, measured on the final files).
   - **Duration:** 31:09.8 (1869.840 s), inside the series' 25–35 min. The parts are 13:30.1 (810.124 s) and 17:39.8
     (1059.818 s); they sum to 0.102 s more than the full cut; part 1 ends on the S08/S09 boundary (810.033 s).
   - **Loudness:** −16.1 LUFS integrated in all four files; LRA 2.3 LU (part 1: 2.2); true peak −2.7 dBTP.
   - **Caption bounds** (`report-measured.md`, `report-visual.md`, `report-pairs.md`): every one of the 519 `.zh-en.srt`
     cues is exactly two lines, Chinese-position line on top (50 px), English below (33 px); the burn file
     `.zh-en.ass` has `WrapStyle: 2`, so no cue wraps to a third line. Measured with Noto Sans CJK, the widest top
     line is 1,475 px (25:12.7) and the widest English line 1,564 px (12:49.7), against 1,840 px usable. The subtitle
     band sits at y ≈ 992–1062; clean-frame content ends at or above y ≈ 972 (12 spot checks, `visual-r2/spot/`).
   - **Music balance:** does not apply. L20, like the other AC215 lectures, has no score: `video.yaml` has no `music:`
     key.
   - **Subtitle sync** (`report-asr.md`, onset check with base.en word timestamps and VAD over all 498 cues): no cue
     starts more than 1 s before its speech; the largest gap is 0.72 s (cues 95 and 388); fifteen cues are between 0.5
     and 0.72 s.

   **Human review:** the series waiver stands in for a listening sign-off.

   Listening sign-off: waived by Conny for the AC215 series (Explainer_Videos#29, 2026-10-15): 「不需要，我现在对视频质量很满意的」 — no human listened to this cut; the ASR round trip below is the substitute.
   Review moments optional since 2026-10-22 (AGENTS.md): 「我大概率是不会进行审片的，因为我觉得做得已经非常好了，就让bugbot来检查就好了」

   **ASR round trip** (`report-asr.md`, round 1, on the pre-fix clean cut with the same narration and subtitles):
   - faster-whisper `base.en` (2 threads) over the whole cut: 498 cues compared, 4,404 words recognised, 251 cues with
     some difference (`asr.json`, `asr-base.log`).
   - `large-v3-turbo` re-ran 50 doubtful cues on their own clips (cue −0.4 s to +0.4 s; `clips/`,
     `asr-large-clips.json`, `asr-large-clips2.json`). Every word base.en lost or changed is spoken: cues 37–38 (02:10),
     195 (12:36 "Review"), 341 (21:15), 349 (21:47 "Change"), 409 (25:12 "Nine") and 484–486 (30:19–30:29).
   - The rest is recogniser noise: words counted across a cue boundary, digits against words, homophones (ours/hours,
     sudo/pseudo), and code names spoken as intended (kubectl "cube control" per the lexicon, nginx "engine x" as
     Kokoro reads it, blkid "block ID" and mkfs "make file system" written as plain words in the SAY). No real problem.

## Whole-video QA (480p draft, 30:46; times are *draft* times)

**Watchers and findings** (`l20-qa-wk0trso3u.output`, key `result`):

| watcher | must | should | nit |
|---|---|---|---|
| director, part 1 | 0 | 5 | 4 |
| newcomer, part 1 | 0 | 7 | 1 |
| director, part 2 | 1 | 3 | 4 |
| newcomer, part 2 | 2 | 4 | 5 |
| subtitles | 0 | 8 | 6 |
| follow-ups | 0 | 0 | 0 |
| ASR | 0 | 1 | 1 |
| **total** | **3** | **28** | **21** |

- **By target:** 29 scene, 14 subtitles, 7 narration, 2 shared code.
- **By kind:** 15 follow-along, 15 subtitle, 7 text, 4 picture, 3 continuity, 2 fact, 2 pacing, 2 narration, 1 sync,
  1 lexicon.
- **By scene:** S09 6, S15 6, S16 5, S04 4, S05 4, S07 4, S13 4, S01 3, S02 3, S12 3, S03 2, S08 2, S11 2, S14 2, S06 1,
  S10 1.
- **Facts:** the part-1 director checked README line refs, nginx.conf and docker-hub.sh lines, `service.py` returning
  "3.0", the 14,356 counter (the sum of the eleven Finished lines), 5.07 GB, Docker 29.9.3 and the 21-command tally
  against the captures and README@3ecef56: all match. No watcher found an instructor name, a real key or an IP in the
  subtitles; the part-2 director found the S15 private client addresses on screen (should, fixed).
- **Follow-ups watcher:** found no `QA_FOLLOWUPS.md` for L20 (none exists in the episode folder); the 16 render logs
  hold only harmless Manim warnings; a scan of the scene code for the bug patterns other lectures' follow-up files
  record found one match (`s05_vector_db.py:247`), safe by construction. No issues.
- **Subtitle watcher:** read 492 `.srt`, 431 `.zh.srt` and 511 `.zh-en.srt` cues of the draft; mechanical checks clean.
  Four clause-order swaps between neighbouring bilingual cues (S08, S09, S14, S15), splits inside a term or a date,
  `.zh.srt` line breaks inside commands, and the shared splitter's preference for a Latin space over a full-width
  colon (glossary I2).
- **ASR watcher:** no mispronunciation; "And where inside?" heard as "And we're inside." (S05, fixed); S13's caption
  added "because some inputs are unknown", which the voice does not say (fixed).

**The musts, and how they were fixed:**
- **M1 (two reports), S09 *draft* 13:58 / 14:00: plan glyphs next to identical trees** (director part 2, newcomer
  part 2). Desired, state and reality all held Network / Firewall / Disk / Instance while `+ ~ - +-` popped beside
  desired, so "each difference becomes a plan line" had no visible difference, and the same identical trees then
  answered ponder 3 as "no changes". **Fix** (`s09_desired_state.py`, beat 4 and the compact replay): the trees differ
  one way per row before the glyphs pop: Network a GREY dashed ghost in state and reality (`+`), Firewall · 80 against
  · 22 (`~`), Disk a ghost in desired (`-`), Instance · image v2 against image v1 (`+-`); beats 9–10 rebuild identical
  trees. **On the final cut:** 14:26.5 shows the differing trees with the plan `+ ~ - +-` (`writer/must_866.5.png`);
  15:35.5, during the answer to ponder 3, shows identical trees, "plan  no changes" and "desired = state = reality"
  (`writer/must_935.5.png`).
- **M2, S10 *draft* 16:42: one ls panel made `deployment.json` look like it sits beside `secrets/`** (newcomer part 2).
  `ls -la` and `ls -la secrets` were merged into one four-row listing, and the last row wrapped. **Fix**
  (`s10_setup.py`): the home listing (`cheese-app-v3`, `secrets`), then a GREY `…` row tagged "inside `secrets/`", then
  `deployment.json` and `gcp-service.json`, each on one row (asserted). **On the final cut** at 17:07.8
  (`writer/must_1027.8.png`).

**The shoulds, examples by kind** (fixed and verified, except those under "Still open"):
- **Follow-along:** S01's "your turn" sample now sits on `sudo docker --version` (step 5), not on the README's
  `docker login` with angle brackets that S03 shows failing; S03's card defines `TOKEN` with `read -s TOKEN` before
  `--password-stdin`; S03 says the two-platform builds are slow and emulated and shows the one-time QEMU registration
  chip `docker run --privileged --rm tonistiigi/binfmt --install all` (on the final cut at 04:22.5,
  `writer/s03_qemu_262.5.png`; the coordinator's list counts this chip as left open, but the S03 verifier added
  it, `s03_docker_hub.py:105` and `:461`, and it is on screen); S04's VM form carries "▶ your turn" and an "SSH button" chip, plus the coordinator's
  pause line (cues 79–80, 05:06.8–05:08.3); S05 and S07's terminal strips keep each command with its output; S07 shows
  `docker logs nginx` after nginx exists, and the coordinator's line says to rewrite an echo'd file first (cue 168,
  10:50.2); S11's strip reprints the head of the `pull access denied` error; S15's card names the retired
  `gemini-2.0-flash-001` and the four `llm_*_utils.py` files to change; S16's checklist gives `gcloud compute instances
  list → empty` for item 1 and adds "after `pulumi destroy` in `deploy_images` too" to item 3 (on screen only; the
  narration of item 3 is unchanged).
- **Facts and text:** S02 types only `git -C cheese-app-v3 log -1 --format='%H %ci %s'`, without the recording-only
  `sed` that masked the staff branch (on the final cut at 02:47, `writer/s02_git_167.png`); S04's chip says "made in
  part 2", not "S10"; S09's sticky no longer names "S13"; S12 says "the VM stack's config needs it", not "step 3"; S15's
  log rows print `INFO:     … - "GET /api-service/ …"` with no address, and its chip no longer shows a capture id.
- **Pictures, pacing, continuity:** S04's RED "never commit · never show" chip stays about 5 s instead of 1 s; S08's
  VM panel and cost dial clear on the Delete click; S13's README tracker no longer runs 9 → 10 → 9; S14's tipped
  provisioning tiles turn as whole tiles; S16's card 5 fades before the answers pointer; S06's VM is drawn with the
  title inside and S04's 80/443 gates.
- **Narration and subtitles:** 18 of 21 items applied by the narration/subtitle fixer (S03 QEMU sentence, S12 OS Login
  clause, S12 "step 3", S05 "But where inside that container?", the four clause swaps and the line-break items);
  `python -m explainer.i18n check … --lang zh` printed OK; S03, S05 and S12 were re-voiced. The S04 scene fixer's
  report was cut off ("The preview is still rendering…"); the S04 verifier checked its fixes in the files.

**Still open after QA, and why:**
- **S02 *draft* 02:04, how to start the v3 containers locally** (newcomer nit): a SAY edit for a nit was outside the
  fixer's rules.
- **S13 *draft* 22:03, `retain_on_delete` read out with no meaning** (nit): same reason; it is explained at destroy
  (cues 468–469, 29:21.1–29:26.5).
- **S15 *draft* 27:49, the narration does not explain why `/status` says 404 on the VM** (nit): same reason; the
  grey tag "public image: no /status yet" carries it, and S06 says it aloud (cue 142, 09:03.0).
- **S05 *draft* 07:15, "Pause and run both containers now" comes before the `/data` erratum** (newcomer should):
  fixed scene-side only (an `erratum → :/data` tag on the run row and "typed :/data at the run step already? nothing
  to redo"); the voice still says it at 07:31.8 (cue 118), before the slip at 08:01.7 (cue 126).
- **VM drawn differently across part 1** (director nit): S06 fixed; `common.py` `NamePhoneBook` (S04 block 8 to S05)
  still puts the title above the VM with no fence, and S07's moved-up variant puts it bottom right. Shared code, not
  in any scene fixer's files.
- **Toolkit and shared code:** the zh splitter still breaks long error strings at a Latin space rather than after a
  full-width colon (03:03, 18:26, 18:50 in `.zh.srt`); `common.py` `ProvisionDominoes.fall()` / `stand()` keep the
  rotate-and-restroke bug (S14 no longer calls them).
- **Small leftovers named by verifiers:** S09's compact trees at slide 15 bring Disk back as a plain card; S04's chip
  shows the console SSH button only, not `gcloud compute ssh`; two faint marks on S08's console frame border around the
  Delete click (not confirmed on the final cut); faint vertical stripes in S10's ls panel background (likely encoding).
- **Source drift (not rendered):** `script.md`'s SHOW lines still say "step 1 of 15" for S01's sample, "line 1 of
  `p02`" for S02, omit S03's binfmt chip, keep "hold that thought: S13" (S09) and "(vm/37:20)" (S15), and say "LECTURE
  20 · 7–8" for S05 (line 527) and S06 (line 584); the docstrings `s05_vector_db.py:5` and `s06_api_frontend.py:5`
  say the same; `i18n/zh/glossary.yaml` and `GLOSSARY.md` quote several old zh wordings as `first_use` notes.

## Final-cut checks (1080p60, 2026-11-07)

- **Tags** (`report-tags.md`, round 2): 31 tags, four frames each (`r2/tag_<scene>_<name>_{a_in,b_mid,c_pre,d_post}_*.png`,
  montages `r2/tagm_*.png`), timed from the `events.json` sidecars plus scene offsets that match `chapters.txt`; a
  presence scan at 10 fps over S05+S06 and S15 (`r2/tag_scan_seg.json`). The three round-1 items verified:
  - S05 reads "Lecture 20 · slide 8" from 06:32.97 to 06:46.27, over slide 8's stage chips and the terminal
    (`r2/tagm_s05_ref.png`).
  - S06 (from 08:16.67) has zero tag pixels in every scanned frame (`r2/xm_s06.png`).
  - S15's slide-19 tag fades out at 26:04.62–26:05.12, right after the six-step strip (26:04.22–26:04.62); none over
    the `setup_containers.py:27–31` panel at 26:05.40–26:15.00 (`r2/xm_s15_ref0.png`).
- **ASR** (`report-asr.md`, round 1): intelligible throughout; no real problem; one observation (lowercase "pulumi").
- **Visual** (`report-visual.md`, round 2, on the re-burned `.zh-en.mp4`, written 08:05:54):
  - 39 contact sheets (4×4 tiles, one frame every 3 s, 00:02.98–31:08.98), all read (`sheets/r2/sheet_001…039.png`),
    plus full-size frames and crops (`visual-r2/`).
  - The three fixes show; nothing regressed in the other 13 scenes; no black or missing scene, nothing outside the frame, no tag
    stuck, no garbled settled text, no clipped or overlapping settled text.
  - Every scene ends empty: frames 0.03 s before each of the 16 ends have peak luma 14–15 and no pixel above 40
    (`visual-r2/ends/`).
  - Odd-looking tiles are transient `Indicate` scale-ups or morphs of 1 s or less: 02:35.98 (S02), 05:32.98 (S04),
    04:32.98, 12:41.98, 16:23.98, 23:56.98, 27:50.98.
  - Frozen stretches over 4 s outside ponder timers: only S03 at 04:08.07–04:14.85 (6.78 s), under continuous
    narration (A5). `freezedetect` (n=0.0005, d=4) also flagged 01:40.75–01:45.67, a false positive (small dashed
    lines animate there per the sidecar; `visual-r2/freeze.log`).
  - "Test yourself · 5/5" is on screen about 1.9 s (31:03.0–31:04.9) before the answers pill; legible
    (`visual-r2/f_1864.2.png`).
  - Series rules: no instructor name, staff branch name, real-looking key, ARN, account id or real IP on any sheet;
    the long hex strings are Docker container and network ids, image digests and the public commit hash.
- **Pairs** (`report-pairs.md`, round 1; the zh-en text is unchanged, see the header): all 519 cues read, zh against en.
  No meaning swap, including every 如果/因为/当/等…以后 clause (cues 43, 76–77, 141, 156, 288, 322, 327, 365, 367, 431,
  494); one zh and one en line per cue; no break inside a command, path, flag or placeholder. Ten small drifts (open
  nits).
- **Measured** (`report-measured.md`, round 2, `measured.json`, evidence `measured-r2/`): all four MP4s decode with exit 0
  and no output. Formats, loudness, subtitles, chapters, narration and the part split pass; durations and frame counts
  equal round 1's. The ponder density is decided under gate 3; the 10 zh-en cues without Chinese are item A2.

## Accepted items (coordinator decisions)

- **A1. Five ponders in 31:09.8** (0.32 per 2 minutes), below AGENTS.md's aim of one per 2 minutes. Accepted under
  Conny's 2026-10-21 decision to keep the current density of 3–5 ponders per lecture (「我觉得可以保留现在的密度」); see
  gate 3.
- **A2. Ten `.zh-en.srt` cues without Chinese**, each verbatim terminal output, a command or file names that
  `i18n/zh/GLOSSARY.md` says to copy exactly: 52 (03:03.3 `syntax error near unexpected token newline`), 63 (03:50.3
  `Compiled successfully`), 247 (14:55.5 `pulumi up --stack dev --refresh -y`), 274 (16:29.6 role names), 308 (18:26.6
  `google-cloud-sdk has no installation candidate`), 310 (18:34.9 `google-cloud-cli`), 370 (22:04.0 "Pulumi access
  token must be set"), 480 (29:00.6 `pulumi destroy --stack dev --refresh -y`), 499 (29:58.7 `docker-shell.sh、deploy
  images`), 500 (30:00.7 `create instance、provision instance`). In the parts: part 1 cues 52 and 63, part 2 cues 24,
  51, 85, 87, 147, 257, 276 and 277.
- **A3. S15's slide-19 tag is short:** the presence scan sees it 26:02.52–26:04.82 (2.3 s; 3.0 s with its fades, about
  1.9 s at full opacity), about as short as the S06 tag that fix round 1 removed. Kept because it is on screen only
  while its picture, the six-step strip, is up (`report-tags.md` finding A).
- **A4. `script.md` SHOW lines still say "LECTURE 20 · 7–8"** for S05 (line 527) and S06 (line 584), as do the two
  scene docstrings: spec text, not on screen (`report-tags.md` finding B). The cut shows "slide 8" in S05 and no tag in
  S06.
- **A5. The 6.78 s still stretch in S03** at 04:08.07–04:14.85, under the running narration "Run the same script in
  api-service and vector-db…" (`report-visual.md`; unchanged since round 1).
- **A6. The S05 lone backslash wrap:** about 07:10 the long `GOOGLE_APPLICATION_CREDENTIALS` line wraps and leaves a lone
  `\` on its own row; the command stays readable (`report-visual-round1.md`, `frames/f_430.5.png`).
- **A7. The QA nits left open** (listed under "Still open after QA"). A narration change needs a re-voice, a re-render
  and a re-burn; none changes meaning.

## Open nits (not ruled on one by one; left for the coordinator)

None blocks release. Each needs a narration, yaml, scene or toolkit change and a rebuild, which this record does not
make.
- **Lowercase "pulumi" in command lines comes out short** (`report-asr.md`): both models hear "pull me up" at 14:53
  (cue 232), 26:57 (cue 432), 30:29 (cue 487) and 30:46 (cue 492); capitalised "Pulumi" is recognised in about 20 cues,
  with "Polomi" at 15:19 (cue 241) and "Polamy" at 30:57 (cue 495). The lexicon target is "PULL-oo-mee"
  (`explainer/lexicon.yaml` lines 464–465); a viewer should still recognise it.
- **Ten `.zh-en.srt` pairs** where a trailing phrase sits one cue early or late in the Chinese (`report-pairs.md`, with
  the yaml item to fix each): 102/103 (06:06.7, "ours holds"), 213/214 (12:49.7, "Python here"), 262/263 (15:46.3, "into
  six steps"), 322/323 (19:18.5, "with a higher version"), 344/345 (20:37.9, "the private key"), 389/390 (23:07.0,
  "slowly"), 479/480 (28:58.9, 运行 "run"), 485/486 (29:15.4, "then the VM"), 493/494 (29:40.2, "last"), 511/512
  (30:35.2, "which gate"). Nothing is reversed or contradicted.
- **"Test yourself · 5/5" holds about 1.9 s** (31:03.0–31:04.9) before the answers pill (`report-visual.md`).
- **The S15 "this repo: …" chip ends about 25 px left of the slide 25–26 tag** (28:10); the overlap scan found no contact.
- **Chapters:** every start is the scene start rounded down (0.00–0.98 s early; the largest gap S14, 23:28 against
  1408.983 s; part chapters within 0.97 s).
- **Frame rate:** 60 fps (the 1080p60 scene renders, as in L02–L18); the repo default for new episodes is 30 fps. The
  burned copy has one more video frame (112,190) than the clean cut (112,189).
- **No `QA_FOLLOWUPS.md`** for L20, and no Bugbot thread was copied into the episode folder.

## Verified (final render)

All numbers are from `measured.json` and the five reports, on the files in `output/` as they are now (written
2026-11-07 07:42–08:08 UTC), except the ASR and pairs results, which are round 1's (see the header).

- **Files:** H.264 High, yuv420p, 1920×1080 at 60 fps, AAC LC 48 kHz stereo at about 179 kb/s, video at about
  284–301 kb/s. Each decodes in full with `ffmpeg -v error … -f null -`, exit 0 and no output (`measured-r2/decode_*.log`).

  | file | duration | video frames | size (bytes) | loudness | LRA | true peak |
  |---|---|---|---|---|---|---|
  | `ac215-l20-deployment-pulumi.mp4` | 1869.840 s (31:09.8) | 112,189 | 113,612,618 | −16.1 LUFS | 2.3 LU | −2.7 dBTP |
  | `ac215-l20-deployment-pulumi.zh-en.mp4` | 1869.840 s | 112,190 | 111,044,167 | −16.1 | 2.3 | −2.7 |
  | `ac215-l20-deployment-pulumi_part1.mp4` | 810.124 s (13:30.1) | 48,602 | 48,519,819 | −16.1 | 2.2 | −2.7 |
  | `ac215-l20-deployment-pulumi_part2.mp4` | 1059.818 s (17:39.8) | 63,587 | 65,097,395 | −16.1 | 2.3 | −2.7 |

  Audio runs longer than video in every file: 23 ms (clean), 7 ms (burned), 91 ms (part 1), 35 ms (part 2). The 16 scene
  durations from the sidecars sum to 1869.817 s (part 1's eight 810.033 s, part 2's 1059.783 s), matching each video
  stream.
- **Subtitles:** `.srt` 498 cues, `.zh.srt` 434, `.zh-en.srt` 519. Part 1 has 210 / 182 / 223, part 2 288 / 252 / 296;
  each language's parts sum to its full file.
  - In all nine files the indexes are sequential, the cues in order, inside the runtime, with no overlaps, none empty
    and none shorter than 0.8 s; the shortest are 1.000 s (`.srt`, `.zh.srt`) and 1.187 s (`.zh-en.srt`).
  - The first cue starts at 1.800 s; the last ends at 1868.080 s (31:08.1), 1.8 s before the cut ends.
  - Every `.zh-en.srt` cue has exactly two lines; 509 have Chinese on top; the ten without are A2's.
  - A scan of all nine files for IPv4 addresses and key patterns (AKIA, arn:aws, ghp_, sk-…, pul-…, email domains)
    matched nothing (`report-measured.md`); this record's writer grepped the subtitle files and `transcript.md` for
    `AKIA`, `AIza`, 12-digit numbers, `172.x.x.x` addresses and `work/`: 0 matches.
- **Chapters:** 16 entries, titles equal to `video.yaml`'s in order, each start the floor of the scene's real start
  (within 0.98 s). `chapters_part1.txt` and `chapters_part2.txt` have 8 entries each (part 2 at 00:00, 02:16, 03:54,
  06:14, 07:42, 09:58, 12:32, 15:24) and match (within 0.97 s). `README.md` now carries them and the durations.
- **Scenes:** all 16 present and in order (S01 84.03 s … S15 172.55 s, S16 135.15 s; the visual and tags checks matched
  every boundary to the cumulative `events.json` durations); every scene ends on an empty frame.
- **Narration:** 155 SAY lines, 4,370 words, 144.4 wpm over 1,746.5 s of voice; 585 anchors; no "anchor not found" in
  the 16 render logs.
- **Lecture tags:** 31 tags, each checked on frames 0.3 s after fade-in, mid-span, 0.25 s before fade-out and 0.5 s after;
  none overlapping, none outliving its scene; S05 cites slide 8, S06 has none, S15's slide-19 tag leaves with its strip.
- **The QA musts on the final cut** (frames extracted by this record's writer): S09's differing trees and plan glyphs at
  14:26.5 and the identical "no changes" trees at 15:35.5 (`writer/must_866.5.png`, `writer/must_935.5.png`); S10's
  separate listings with `deployment.json` and `gcp-service.json` under "inside `secrets/`" at 17:07.8
  (`writer/must_1027.8.png`). Also re-checked: S02's typed git command without the masking `sed` at 02:47
  (`writer/s02_git_167.png`) and S03's QEMU chip at 04:22.5 (`writer/s03_qemu_262.5.png`).
- **Privacy:** no instructor name, staff branch name, key or real IP on screen (sheets, `report-visual.md`); project IDs
  are placeholders, OS Login users `sa_000…`, the VM address `<instance_ip>` / `<VM IP>`; the S15 log's private client
  addresses print as `…` (from 28:33); what remains are container and network ids, image digests and the public
  `3ecef56…` commit hash.
- **Provenance** (`ASSETS.md`):
  - Terminal lines come from the 2026-11-05 captures in `assets/terminal/` (`vm/`, `laptop/`); each README command ran
    exactly as printed, in README order, with extras tagged `extra` (`-x-` in the capture name); nothing in a terminal
    panel is typed by hand. Code panels quote `assets/source/` copied unchanged at `3ecef56`.
  - Live: the manual deployment on the Debian 12 stand-in (Docker 29.9.3, `cheese-app-network`, Chroma 1.0.0 and its
    heartbeat, the loader's 14,356 chunks, the API's 5 GB image with `/` and `/docs` answering and `/status` 404, the
    frontend on 3000, nginx 1.30.6 on 80 with the home page and `/api-service/` through it, the mangled `log_format`);
    `docker-hub.sh` building the frontend and the push refusal; the toolbox's two failed builds and the fixed build
    (Python 3.13.18, uv 0.13.7, Google Cloud SDK 592.0.0, Pulumi v3.274.0); `ssh-keygen`; the local-backend previews up
    to `b35b`'s push 403 and `b43`'s `get_image` `invalid_grant`.
  - `illustration`: the Google Cloud console, the Docker Hub token page, the browser, a successful `pulumi up` and its
    resource graph, the reverse-order teardown. `expected`: the README's own OS Login output snippet. The binfmt chip is
    Docker's documented command, shown as a note with no output panel.

## Not claimed

- **No human listened to this cut** or watched it. The listening gate rests on the series waiver quoted under gate 6,
  and the audio was checked only by machine (the ASR round trip and the onset check, on the round-1 cut). The
  lowercase "pulumi" vowel is unresolved by ear.
- **The ASR and pairs checks did not run on the final files.** They ran on the round-1 cut; the fix round changed only
  three scenes' pictures, and the subtitles are identical (writer's comparison), but the audio of the re-rendered S05,
  S06 and S15 was not transcribed again (the loudness of the whole cut was re-measured).
- **The Chinese subtitles were reviewed by agents only:** the QA subtitle watcher, the narration/subtitle fixer, the
  scene verifiers and the pairs check. No human translator or native reviewer read them.
- **No Google Cloud step ran.** No project, billing, API enablement, service account, key, OS Login profile, Artifact
  Registry repository, state bucket, Compute Engine VM, firewall, disk or external IP was created; no `pulumi up`
  succeeded and no `pulumi destroy` removed a real resource. What a real run prints (the ~30-resource plan, the six
  outputs, `instance_ip`, the app through a real VM's port 80, the chat with a current Gemini model) is described from
  the code and the README, or drawn as `illustration`, never observed. The README's own OS Login snippet is the only
  success output shown, as `expected`.
- **No Docker Hub login or push succeeded:** the login with a token, the multi-platform `api-service` and `vector-db`
  builds (no arm64 emulation on the recording machine; the QEMU chip was not run) and the pushes are not captured; the
  VM pulled the public `dlops` images. **No browser ran:** the browser views are drawings. **No Mac, no Windows:** the
  laptop stand-in was Alpine linux/amd64; the Apple-silicon emulation remark is described, not measured. The VM was a
  privileged container, not a GCP VM (no systemd; `dockerd` started by hand, `ASSETS.md` "capture-only").
- **The toolbox fixes are shown as of 2026-11-05;** whether the committed Dockerfile builds on a later day was not
  re-checked.
- **The visual check sampled one frame every 3 s**, plus targeted frames; motion between samples was checked only by the
  sidecar gap scan and `freezedetect`. The tags check used four fixed frames per tag plus a 10 fps presence scan over S05,
  S06 and S15 only. The round-2 contact sheets were read on the burned copy only; the two part files were measured
  (probe, decode, loudness, subtitles, chapters, frame counts) but not sampled visually on their own.
- **Most QA fixes were verified only on previews** (720p `--at` frames and `--every 2` sheets before the 1080p60
  renders), not one by one on the final cut. This record's writer re-checked the two musts, S02's git command and S03's
  QEMU chip on final-cut frames (`writer/`); the final-cut checks cover the rest only by their own sampling and reading of
  every cue.
- **Stated as the coordinator gave them, not checked here:** lexicon PR #118 (`bbe7674`, not in this clone); the two
  coordinator narration lines' i18n check and the re-check of all 16 scenes; the resumed interruptions.
- **Review bots:** no `QA_FOLLOWUPS.md` exists for L20, and nothing in this record checks Bugbot threads on an L20 PR.
- **`README.md` durations and chapters were filled in this pass** from `measured.json` and `chapters*.txt`; its chapter
  summaries were not reviewed by a separate agent.
- **Every check in this record is an agent's.**

## Fix round after the final-cut checks

- **Round 1 findings fixed** (commit `4750fb8`, 2026-11-07 07:24 UTC):
  - S05: the tag reads "Lecture 20 · slide 8" (was "slides 7–8" over slide 8's picture only).
  - S06: the opening tag, on screen about 2 s while the VM was up, is removed.
  - S15: the slide-19 tag fades out with the six-step strip instead of staying about 7 s over the code panel.
  - S05, S06 and S15 re-rendered at 1080p60 (07:31–07:37, per their logs), the cut re-stitched (07:42) and re-burned
    (08:05), still 31:09 (part 1 13:30, part 2 17:39); scene durations and subtitle timings unchanged.
- **Round-2 checks on the new files** (`report-tags.md`, `report-visual.md`, `report-measured.md`): all three items
  verified, no regressions; measured passes (I −16.1 LUFS, TP −2.7 dBTP). The ASR and pairs reports are from round 1:
  the narration and subtitles did not change.
