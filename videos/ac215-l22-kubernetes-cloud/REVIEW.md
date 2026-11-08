# Review record: AC215 · Lecture 22 — Scaling: Kubernetes in the cloud (the cheese app on GKE)

Follow-along of the Lecture 22 tutorial, *Scaling: Kubernetes (cloud)*, on
[dlops-io/cheese-app-v3](https://github.com/dlops-io/cheese-app-v3) `main` @ `3ecef56` (2025-11-28, "v4->v3"; still the
head of `main` on 2026-11-07, `assets/terminal/laptop/p03-x-ls-remote.txt`): the README's *Create Simple Kubernetes
Cluster Tutorial* (README:517–581, done first, as the lecture does), *Deployment with Scaling using Kubernetes*
(README:392–434), *Create & Deploy Cluster* (README:436–512) and the Kubernetes half of *Debugging Containers*
(README:618–657). An unmerged staff branch (`work/‹staff›`) exists on the remote; it is context only, never followed and
never named on screen (`digest.md`, `ASSETS.md`, "Which commit"). Claude Code sessions (Claude) produced it. Verified
facts and unclaimed reviews are kept in separate sections.

- **Origin:** issue #122. Built end to end on 2026-11-07/08 by this coordinator's agents: digest (re-checked; Chroma's
  `/data` against the PVC's `/chroma/chroma` confirmed from the registry config; real IPs and a domain removed), live
  captures, brief, script + four independent reviews (`build/review_{accuracy,followalong,pedagogy,spoken}.md`,
  `build/review_merge_log.md`), `scenes/common.py`, 16 scenes each with a fresh critic, zh subtitles, `exercises.md`,
  `README.md`, and the study guide (MLOps_Learning, committed on the branch; per the coordinator). Build-complete commit
  `ea751e0` (2026-11-08 03:21 UTC; "SLIDES.md credits the course staff and masks the story role"). Usage-limit
  interruptions and container restarts were resumed from run ids (per the coordinator).
- **Captures:** 2026-11-07, 20:47–21:16 UTC (`ASSETS.md`). The laptop stand-in is `docker:29.8.2-dind` with the
  deployment toolbox built from `src/deployment/` (Google Cloud SDK 592.0.0, Helm v3.22.1, Pulumi v3.274.1, Python
  3.13.18). **No Google account and no credentials.** Live: the toolbox failing as committed (`laptop/b02`: Debian
  bullseye-security 404s, then `pull access denied`, exit 125), the two one-line fixes shown (`b02a`: bookworm,
  `google-cloud-cli` with its GKE auth plugin; as in L20), the build (92.3 s, `b03`); every gcloud, Pulumi and kubectl
  command of the README, each up to its honest first error (`You do not currently have an active account selected`,
  `PULUMI_ACCESS_TOKEN must be set`, `invalid_grant: account not found`). Pulumi on its local file backend (tagged
  `extra`): `deploy_images`, then `deploy_k8s`'s `TypeError: 'NoneType' object is not subscriptable` (`c13`) and, with a
  capture-only stand-in image stack (placeholder tags), the real plan **`+ 23 to create`** (`c20`) and `pulumi up`
  stopping at the VPC (`c21`). The README's kubectl commands ran verbatim against a **real but labelled stand-in
  cluster**, kind v0.31.0 / Kubernetes v1.34.11 (1 control plane, 2 workers), tagged `stand-in: kind, not GKE` on every
  panel.
- **What could not run, and how it is shown:** GKE cluster creation, the console, the browser, a successful `pulumi up`
  and the teardown against real resources are schematic `illustration`s; the README's `Outputs:` block is the one
  `expected` panel (IPs replaced by placeholders). Nothing was faked: each cloud step stops at its first real error or is
  labelled (`ASSETS.md`, "What cannot run here").
- **Slides:** `SLIDES.md` (45-page deck, credited to "the course staff"; the deck's story character is masked as
  `‹instructor›`, on 7 lines) is redrawn, never shown. 48 "Lecture 22 · slide(s) …" tags in the cut (gate 2).
- **QA draft:** the 480p draft, 29:59 (QA output; `build/qa/draft.mp4` is now a dangling link to the deleted
  `output/ac215-l22-kubernetes-cloud_480p15.mp4`, so it was not re-measured); subtitles in `build/qa/` dated 2026-11-08
  03:46 UTC.
- **Whole-video QA:** run `wf_ad298988-703`, output `/root/ac215-backup/tasks/l22-qa-wr2h0zyrw.output` (2026-11-08 05:50
  UTC), key `result`. 40 agents: seven watchers, 15 scene fixers (one of them for S09–S16's scene ids), one
  narration/subtitle fixer and 17 verifiers. The run log reads "L22: 51 issues from 7/7 watchers". QA fixes committed in
  `ea2b441`, `586de06` and `3a4f51b` (2026-11-08 04:30–05:51 UTC; the last one "S12 troubleshooting card now narrated":
  the coordinator added the line the S12 verifier asked for). Lexicon PR #126 merged to `main` as `fcd34c9` (per the
  coordinator).
- **Finishing pass:** none. The coordinator's list of finishing-pass outputs for L22 is empty (`[]`).
- **1080p60 renders:** all 16 scenes, render logs written 2026-11-08 06:02–06:43 UTC (`build/logs/`); S12 re-rendered in
  fix round 1 (log 08:22). None of the 16 logs contains "anchor not found" (this record's writer grepped them).
- **Final cut:** 30:26.3 (1826.318 s); parts 14:19.7 + 16:06.7. File times (UTC, 2026-11-08): the clean cut and the
  full-cut subtitles 08:26; the burned copy, `chapters.txt` and `transcript.md` 08:51; part 1 08:52; part 2 08:53. The
  MP4s are not in Git (release assets).
- **Final-cut checks:** two rounds; the coordinator saved each check's returned text as
  `build/final-review/report-{tags,asr,visual,pairs,measured}.md`, round 1 kept as `report-*-round1.md`. All five reports
  exist and were read in full for this record.
  - Round 1 ran on the first stitch (`48fa0fe`, 07:39 UTC): ASR no real problem; visual no must (four cosmetic notes);
    measured pass; tags 49, of which S12's "slides 24–25" sat over the V6 graph it did not cite (20:05.9–20:19.5) and the
    second led its picture by 4.4 s (20:50.6 against 20:54.9); pairs: one condition-first swap (A1), three commands
    split across cues (B1–B3), three English sentences repeated over two zh halves (C1–C3), list drifts (D6, D7).
  - Fix round 1 (`a4521cf`, 08:16 UTC): nine zh items (and the glossary examples) re-cut; S12's bare-graph tag removed and
    the other moved onto its inset; S12 re-rendered (134.149 s, same length), re-stitched and re-burned. Still 30:26
    (part 1 14:19, part 2 16:06).
  - Round 2 re-ran **tags, visual, pairs and measured** on the files now in `output/`: every round-1 item verified, no
    regression, measured passes.
  - **The ASR report is round 1's** (`report-asr.md` is byte-identical to `report-asr-round1.md`), run on the pre-fix
    clean cut. The fix round changed no narration: this record's writer compared the current `.srt` with `asr.json`
    (500 cues each, identical text, start and end times equal to within 1e-12 s). The audio of the re-rendered S12 was
    not transcribed again (the loudness of the whole cut was re-measured).

**Conventions:**
- **Times** are mm:ss in the full cut (`output/ac215-l22-kubernetes-cloud.mp4`, 1826.318 s), except in "Whole-video QA",
  which keeps the 480p draft's times (marked *draft*).
- **Cue numbers** name their file: `.srt` (500 cues) or `.zh-en.srt` (508).
- **Evidence paths** are relative to `build/final-review/`. That folder is git-ignored and exists only in the producing
  session; a successor re-runs the checks to reproduce it.

## Content gates (AGENTS.md)

1. **Hook** ✔. S01 opens on a broken thing and a question, not a value proposition.
   - "Here is a small app on one virtual machine:" (`.srt` cue 1, 00:00.0); "If one of them crashes in the night, who
     restarts it?" (cue 3, 00:07.4); "At two in the morning, one API container crashes." (cue 4, 00:10.7); "the operator
     logs in over SSH and restarts it by hand." (cue 6, 00:17.3); "if the machine itself failed, the whole site waited for
     you." (cue 9, 00:27.1); three machines with a backup beside each API (cues 10–12), then ponder 1.
   - **Payoff:** the lecture's three asks (failover, load balancing, scaling) as a checklist card (slide 12, 01:07.3) that
     "comes back each time we see what does one of these jobs" (`.srt` cue 22, 01:19.2; `.zh-en.srt` cue 19) and is ticked in S07 (failover, tag T29
     12:16.1), S13 (load balancing) and S15 (scaling, "That ticks scaling, in two levels", cue 463, 28:16.4), then
     answered in the recap "Back to the three asks." (cue 476, 29:06.0).
2. **Intuition before formalism, with an animated mechanism for each core idea** ✔. `BRIEF.md` ("Visual set pieces")
   defines eight, each animated beside the files, logs and kubectl output it explains:
   - **V1, the cluster re-drawn for GKE (`MasterDiagram`, slides 22–26):** built in S03 in the deck's three beats
     (control plane and workers; "run by Google"; API server, etcd, scheduler, controllers; kubelet, kube-proxy, a
     `containerd` strip with the slide's "Docker" struck through), tags T10–T14 03:05.4–04:33.1; reused as a symptom map
     in S06 (`EXTERNAL-IP <pending>` lights the cloud-provider arrow, T24 10:15.3), S07 and S12 (the V1 inset, T38
     20:54.9–21:07.2).
   - **V2, one box to a fleet (`FleetMorph`, slides 4–13, 19):** S01's VM, the 2 a.m. crash and the SSH operator; three
     VMs with backups, VM 2 going dark and the switch "by hand" (T03–T04, 00:31.2–01:07.7); S02's morph from one Docker
     host to a cluster (T07, 01:42.0–02:00.8).
   - **V3, two objects, one sticker (`LabelLink`, slide 39 made honest):** S06 splits the real
     `deploy-k8s-tic-tac-toe.yml` into Deployment and Service and lights the `run: web` lines slide 39 trims (cue 160,
     09:04.9 "The template gives every Pod a label, run: web;"); S08 turns the lasso into the endpoints list and the DNS
     name `web.default.svc.cluster.local`.
   - **V4, desired state kept (`ControllerLoop`, slides 18, 30, 36):** Deployment → ReplicaSet → Pods with the
     three-part name, observe → compare → act (T28, 11:17.7), a deleted Pod replaced (ponder 3, answer "Two." cue 205,
     12:01.5; "Its name keeps the ReplicaSet hash, with a new suffix." cue 207, 12:06.6).
   - **V5, the whole cheese app on GKE (`CheeseBlueprint`, slides 21–22):** S09 dissolves L20's VM into the cluster, one
     row of the L20 → L22 table at a time (containers → Deployments, loader → Job, network names → Services + DNS,
     folders → two PVCs, nginx → Ingress controller + Ingress, the JSON key → Workload Identity), T35–T36
     14:19.6–14:48.0; at 15:05 the three Deployment cards show their labels clear of the Pod dots
     (`writer/s09_cards_905.png`).
   - **V6, the plan grows in dependency order (`ResourceTree`):** S11 turns `c20`'s 23 lines into a tree counting to
     `+ 23 to create`; S12 fills it in build order (illustration) after the real capture stops at the VPC; S16 empties it
     in reverse.
   - **V7, one click, every hop (`RequestJourney`, slides 5, 21, 24, 26, 38):** S13's packet from `<IP>.sslip.io`
     through the load balancer, the nginx controller and the Ingress rule to `api:9000` / `frontend:3000`, the README
     diagram's reversed loader arrow corrected, and the bare IP bouncing with a 404 (ponder 4; T39–T40,
     21:57.4–22:46.0).
   - **V8, two levels of scaling (`BinPacking`, slides 18, 43):** S15's node shelf filled by requests, `kubectl scale
     … --replicas=3`, a `Pending` copy and the autoscaler's second node, the API's `ReadWriteOnce` disk and
     `Multi-Attach` (ponder 5; T43–T44, 27:00.6–27:29.1).

   **Lecture slides:** a GREY "Lecture 22 · slide(s) …" tag top right, **48 tags** in the cut (`report-tags.md`): S01 5,
   S02 4, S03 6, S04 1, S05 4, S06 5, S07 4, S08 5, S09 2, S11 1, S12 1, S13 2, S14 2, S15 2, S16 4; none in S10. The
   deck is redrawn, never shown (`SLIDES.md`).
   - All 48 pass (round 2, four frames per tag in `tags-r2/`; 190 of the 192 frames pixel-identical to round 1's, the two
     that differ being the fixed S12 tag): each on screen while its picture is up, "slide" for one and "slides" for
     several, no overlap, none outliving its scene.
   - Accepted (coordinator): small leads at block starts, T03 about 1–2 s (00:31.2), T08 about 1.2 s (02:00.4), T15 about
     2.1 s (04:32.7); T14 (04:21.1) has no LECTURE mark in its script SHOW line; T09 (02:35.3) is the legend's sample tag
     and cites no picture, by design.
3. **Pause-and-ponder moments and a recap**: ✔ for the ponders, by Conny's decision for the series (accepted item A1); ✔
   for the recap.
   - **Ponders:** five, each a card with the question spoken, then a silent linear timer; no narration overlaps any timer
     and the answer starts exactly when it ends (`measured.json` "ponders"; questions from `script.md` lines 310, 594,
     648, 995, 1117; answers from the `.srt`).

     | # | scene | question (from `script.md`) | asked | timer | answer starts |
     |---|---|---|---|---|---|
     | 1 | S01 | Each backup sits on the same VM as its original. What still takes that API down, and who switches to the backup? | 00:42.7 (cues 13–14) | 00:48.9, 8 s | 00:56.9 "The machine itself:" (cue 15) |
     | 2 | S06 | EXTERNAL-IP is still `<pending>` after 43 seconds. Which part of the cluster is waiting, and on what? | 10:03.3 (cue 174) | 10:07.4, 8 s | 10:15.4 "The controllers, waiting on the cloud provider." (cue 175) |
     | 3 | S07 | Delete one of the two web Pods. A second later: how many? Which part of the new name stays the same? | 11:47.6 (cues 203–204) | 11:53.5, 8 s | 12:01.5 "Two." (cue 205) |
     | 4 | S13 | `http://<IP>/` — the same load balancer, without .sslip.io. What answers? | 23:34.5 (cues 392–393) | 23:42.1, 8 s | 23:50.1 "The nginx controller answers 404 Not Found." (cue 394) |
     | 5 | S15 | Suppose api had 3 replicas. Some Pods land on node 2. What happens to them, and can the autoscaler fix it? | 27:47.6 (cues 458–459) | 27:57.3, 10 s | 28:07.3 "They stay stuck creating, with a Multi-Attach error:" (cue 460) |

   - **Rate:** 5 cards in 30:26.3, one per 6.09 minutes (`measured.json`), against AGENTS.md's aim of one per 2 minutes
     (about 15 for this length). Part 1 has 3, part 2 has 2. Timers total 42 s. The first timer starts at 00:48.9; the
     longest gap between two timers is 708.6 s (11:53.5 to 23:42.1); after the last timer ends (28:07.3) the video runs
     139.0 s more.
   - **Decided by Conny (2026-10-21), as recorded in `videos/ac215-l05-rag/REVIEW.md` gate 3:**
     「我觉得可以保留现在的密度」: keep the current density, which that record gives as 3–5 ponders per lecture plus a
     spoken recap and test questions. L22's five ponders are inside that series density and below AGENTS.md's aim.
   - **Recap:** S16 "Destroy, audit, recap" from 28:30.0 (116.28 s).
     - 28:30.0–29:06.0: `pulumi destroy --stack dev --refresh -y` in reverse order, and the audit of what may survive
       (clusters, forwarding rules, `pvc-…` disks, firewall rules; registry images on purpose; the L20 VM), "Pause and
       check." (cues 466–475).
     - 29:06.0–29:23.9: "Back to the three asks." failover, load balancing, scaling and what did each job (cues 476–480).
     - 29:23.9–29:41.1: the lecture's five payoffs (cues 481–486).
     - 29:41.1–30:16.5: "Test yourself." and five questions (cues 487–497); "Answers are in the exercises and the study
       guide." (cue 498, 30:13.1).
     - 30:16.5: next, lecture 23 (cues 499–500).
     - Part 1 (14:20) has no recap of its own; it ends on "Don't forget to delete" (T34, 14:10.6) after the test cluster is
       deleted (open nit).
4. **Narration written for the ear, with word-anchored cues** ✔.
   - **Spoken style:** commands, flags and error codes are spoken in words with the literal form in the subtitle's
     `en_display` (`'NoneType' object` said "none type is not subscriptable", `invalid_grant: Invalid grant` said "invalid
     grant, account not found", `<pod-name>` said "pod name in angle brackets", `-c wait-for-chromadb` said "wait for
     chromadb"; `report-asr.md` item 4, with the `script.md` lines).
   - **Size:** 151 SAY blocks, 4,346 words (`measured.json`), 46 words (1.1 %) above the script's 3,900–4,300 band after
     the QA additions (`script.md`'s own count, 4,297, predates them; open item). Kokoro `af_heart` at speed 0.9: 1,680.9 s
     of voice (92.0 % of the runtime), 155.1 wpm over the voice and 142.8 wpm over the runtime; the longest block is 48
     words.
   - **Anchors:** 576 `wait_until` anchors across the 16 scene files (S01–S16: 22, 31, 37, 41, 43, 49, 41, 28, 25, 35, 38,
     48, 40, 30, 41, 27; none in `common.py`). None of the 16 render logs contains "anchor not found".
   - **Pronunciation:** the QA ASR watcher found no lexicon problem and one nit ("frontend" heard as "front ten",
     *draft* 27:02, left open). The final ASR found no mispronunciation and no swallowed word, and heard that sentence
     correctly ("Scale the frontend to 3.", cue 454, 27:29.1; `asr.json`). "Pulumi" is written by the recognisers as
     "pull me" and similar with the right syllables (a watch item, `report-asr.md`).
5. **Simulated-target-viewer QA over the full draft** ✔.
   - Seven watchers reviewed the 480p draft: a director and a simulated target viewer ("newcomer") per part, a subtitle
     watcher, a follow-ups watcher and an ASR watcher, from contact sheets, frames pulled from the draft, the scene code,
     the subtitle files, the README and the captures.
   - **51 timestamped findings: 0 must, 32 should, 19 nit.** The shoulds were fixed and checked by independent verifiers
     (one, the S12 card's narration, finished by the coordinator); what stayed open is listed under "Whole-video QA". This
     record's writer re-checked several on the final cut and found one should still open (S02's "(S06)", below).
6. **Measured checks** ✔. The numbers are under "Verified" (`measured.json`, round 2, measured on the final files).
   - **Duration:** 30:26.3 (1826.318 s), inside the series' 25–35 min. The parts are 14:19.7 (859.707 s) and 16:06.7
     (966.730 s); they sum to 0.119 s more than the full cut; part 1 ends on the S08/S09 boundary (scene sum 859.600 s).
   - **Loudness:** −16.1 LUFS integrated in all four files; LRA 2.2 LU (full cuts; parts 2.1 and 2.3); true peak −2.6 dBTP
     (full cuts; parts −2.7).
   - **Caption bounds** (`report-measured.md`, `report-visual.md`, `report-pairs.md`): every one of the 508 `.zh-en.srt`
     cues is exactly two lines, one per language; the burn file `.zh-en.ass` uses `WrapStyle: 2` (no wrap) and its 508
     Dialogue lines match the SRT. The widest lines are the Chinese of cue 217 (60 half-width units) and the English of
     cue 497 (93 characters at `\fs33`), each on one row in the burned frame (`r2/pairs/band_1785.5.png` for cue 497;
     `verify/cue217_band.png`, 12:24.5, for cue 217). Terminal and code panels end at about y = 980 and the subtitles sit at about y = 1000–1075 (12 spot checks over commands,
     `r2/subs/quad_1…3.png`).
   - **Music balance:** does not apply. L22, like the other AC215 lectures, has no score: neither `video.yaml` nor
     `BRIEF.md` mentions music.
   - **Subtitle sync** (`report-asr.md`, onset check with base.en word timestamps over all 500 cues plus a 20 ms RMS
     onset): median lag 0.09 s; no cue's audio starts more than 1 s after the cue; the largest real lags are 0.87 s (cue
     296), 0.67 s (cue 317) and 0.64 s (cue 497). The two base.en flags (cues 329–330, 19:29–19:32) are recognition gaps:
     energy onsets 0.20 s and 0.40 s, and large-v3-turbo hears both lines from their start.

   **Human review:** the series waiver stands in for a listening sign-off.

   Listening sign-off: waived by Conny for the AC215 series (Explainer_Videos#29, 2026-10-15): 「不需要，我现在对视频质量很满意的」 — no human listened to this cut; the ASR round trip below is the substitute.
   Review moments optional since 2026-10-22 (AGENTS.md): 「我大概率是不会进行审片的，因为我觉得做得已经非常好了，就让bugbot来检查就好了」

   **ASR round trip** (`report-asr.md`, round 1, on the pre-fix clean cut with the same narration and identical `.srt`;
   see the header):
   - faster-whisper `base.en` (2 threads) over the whole 30:26 cut: 500 cues compared, 4,424 words recognised, 234 cues
     with some difference (`asr.json`, `asr-base.log`).
   - `large-v3-turbo` re-ran 44 doubtful cues on their own padded clips (`asr-large-clips.json`). Every word base.en lost
     is spoken: e.g. cue 261 (15:22), 329–330 (19:29–19:32), 486–487 (29:37–29:41); cue 102 "Use WSL." (05:39); cue 151
     "Component statuses prints a deprecation warning" (08:31).
   - The rest is recogniser noise: command names heard the lexicon's way (kubectl "cube control", etcd "at cd", nginx
     "engine x", containerd "container d", sslip.io "slip.io"), spelling and numbers, captions written with symbols but
     read in words, words counted across a cue boundary, homophones. **Real problems: 0.**

## Whole-video QA (480p draft, 29:59; times are *draft* times)

**Watchers and findings** (`l22-qa-wr2h0zyrw.output`, key `result`):

| watcher | must | should | nit |
|---|---|---|---|
| director, part 1 | 0 | 8 | 2 |
| newcomer, part 1 | 0 | 4 | 1 |
| director, part 2 | 0 | 7 | 4 |
| newcomer, part 2 | 0 | 4 | 5 |
| subtitles | 0 | 9 | 6 |
| follow-ups | 0 | 0 | 0 |
| ASR | 0 | 0 | 1 |
| **total** | **0** | **32** | **19** |

- **By target:** 27 scene, 14 subtitles, 5 narration, 5 shared code.
- **By kind:** 16 subtitle, 9 follow-along, 8 text, 4 picture, 4 continuity, 4 narration, 3 pacing, 2 sync, 1 fact.
- **By scene:** S15 7, S06 5, S08 5, S09 5, S11 5, S05 4, S12 3, S14 3, S01 2, S02 2, S04 2, S10 2, S16 2, S03 1, S07 1,
  S13 1, S09–S16 1.
- **Facts:** the part-1 director found every typed command matching the README or its capture's line 1 and the terminal
  output matching the captures; the part-2 director found every README command (README:405–413, 437–443, 452, 457,
  478–492, 510) in order, output only from captures and the README's real IPs replaced by `<IP>`. The one fact should
  (S15 *draft* 27:12: four 2Gi frontends drawn on a node that cannot hold them) was fixed by scene-local block sizes:
  node 2 now holds three and the fourth pends. No watcher found an instructor or staff name, real IP, key or project id.
- **Follow-ups watcher:** found no `QA_FOLLOWUPS.md` for L22 (repo-wide, only L02–L05 and L08 have one), no comments on
  issue #122 and no review comments on L22 paths in PR #44. No issues.
- **Subtitle watcher:** one clause-order swap (S05 *draft* 07:21), four names or ranges cut across zh-en cues (README
  heading, 一到 | 两个, gcp-service | 上的, Kubernetes | 服务账号), flags translated instead of copied (06:57, 13:53), the
  English `.srt` cutting `run: web` and the create command across cues, and the A6 respelling of underscored file names
  in zh lines (open, below).
- **ASR watcher:** 4,392 words recognised, 228 of 494 cues differing, all noise or intended; one nit (below).

**The musts:** none.

**The shoulds, by kind** (fixed and verified, except those under "Still open"):
- **Scene ids on screen:** S08's chips ("recorded before the delete in S07", "the Service's CLUSTER-IP · S06", "README:
  the same exec, into the API → S14") and every S-id in S09–S16 ("Ingress → S13", "registry images outlive destroy (S16)",
  "the condition → S11", …) replaced by words ("→ later", "· see the end", "· next"). **Not fixed:** S02's note from
  `common.py:3453` (see "Still open").
- **Follow-along:** S06 gets `▶ your turn` markers on `kubectl apply` and `kubectl get services`; S08 shows `gcloud
  container clusters list` at "Pause, check that your test cluster is gone"; S14's "inside the API Pod" card now starts
  with `kubectl exec --stdin --tty <your api pod> --namespace=cheese-app-namespace -- /bin/bash`; S15's Job command fits
  its terminal without scrolling; S04 adds an "or edit by hand · line 4 … line 30 …" chip under the soft-wrapped `sed`;
  S11 prints `pulumi stack ls`'s rows; S12's "if yours stops" card is now narrated (cues 366–367, 21:41.7–21:46.8: "If
  yours stops, the card shows the four usual causes: pause and match your error.").
- **Continuity, text, pictures, pacing, sync:** S08's kind rows leave with the stand-in tags when the panel is retitled
  `laptop · toolbox`; S06's ponder cluster keeps its two Pods, and the worker names stay yellow about 2.8 s; S10 clears
  the terminal before the README-backend `PULUMI_ACCESS_TOKEN` error and tags it "README backend · before login --local";
  S11's code panel prints line 9 verbatim (`pulumi.Config(…)` wrapped, no `…`); S15's Chroma `/data` chip arrives with its
  line and the fix `line 150: mount_path="/data",` (narration re-written: "…today's Chroma image writes to slash data…
  Change line 150 to slash data, or run the loader Job again after a restart."); S02's underline spans "deployment"; S03's
  5 s still on "line 52" now pulses; S09's registry chip and S12's cost tag stay readable about 4.5 s and 3.5 s.
- **Narration and subtitles:** S01 "This card comes back each time we see what does one of these jobs, and we tick it
  then." (the card no longer "stays in the corner"); 14 of 15 subtitle items applied (clause order, flags copied, the
  heading, ranges and terms kept in one cue, "Create & Deploy Cluster", "API version: 3.0"); `python -m explainer.i18n
  check … --lang zh` printed OK; S01 and S15 re-voiced.
- **Nits also fixed:** S01's three-VM spacing (a scene-local `Fleet(FleetMorph)` subclass), S07's crowded controller loop
  (scene-local `RoomyLoop`), S14's inset head "c20 · line 40" → "our preview's Outputs · today's key", S15's tracker
  leaving at the scaling half, S16's checklist notes from S07 and S13, S16's panel printing `-  pulumi:pulumi:Stack
  deploy-k8s-dev deleted` above "- 1 deleted", S11's code panel, S13's swapped names, S05/S06 clause shifts.

**Still open after QA, and why:**
- **S02's note still prints an internal scene id** (should, director part 1, *draft* 01:54; target shared code). The
  scene-id fixer covered S08 and S09–S16 only; two verifiers reported `common.py:3453` (`deployment_note`, ", the object
  (S06)") as still open in a file they could not edit. **On the final cut** the dashed note reads "deployment = a way of
  deploying · ≠ Deployment, the object (S06)" from about 01:55 to 02:01 (this record's writer:
  `writer/s02_note_117.png` at 01:57; `writer/s02_note_span.png`: on at 02:01, gone at 01:53.5 and 02:02; verifier:
  `verify/s02_note_span_verify.png`, on at 01:55, 01:55.5, 01:56, 02:01 and 02:01.5; absent at 01:54.5). Not listed in
  the coordinator's accepted items. **Fixed in fix round 2:** the coordinator changed the label in `common.py:3453` to
  ", the object (later)", re-rendered S02 at 1080p and re-stitched and re-burned (still 30:26). The coordinator checked
  the new final-cut frame at 01:57: the note reads "… ≠ Deployment, the object (later)"; no scene id is on screen.
- **S11 18:33.4, setupSSL wording** (narration nit; `.srt` cues 312–313: "two leftovers from the committed file,
  setupSSL and an SSH user, which the program never uses", while S09 had shown line 17's `setupSSL = False` switching
  HTTPS off): a SAY edit for a nit was outside the fixer's rules.
- **S10, the README-backend error is not spoken** (verifier's note): the tag carries it on screen; a SAY clause would
  need a re-voice.
- **S15 27:29.1, "frontend" heard as "front ten"** (ASR nit, *draft* 27:02): left; the final ASR heard it correctly.
- **S16 28:35.2, "Ours has nothing real to delete"** (narration nit; cue 467) while the panel shows "- 1 deleted":
  mitigated on screen (the Stack line now names the one deleted resource).
- **S15 about 26:02, the README card for lines 620–656 sets its 14 commands in the serif label font** (nit): the longest
  command is 88 characters against about 74 per mono row at 20 pt, so mono rows would fold and the card would not fit.
- **`common.py`'s `FleetMorph` numbers** stay cramped for any other caller; S01 overrides them locally.
- **The A6/B3 glossary respelling** of underscored names in zh lines (deploy k8s, setup containers, ROOT PATH, app URL,
  ip address …; subtitle should, *draft* 15:25): reverses a glossary decision, left to the coordinator; the English line
  under each shows the literal (`report-pairs.md`, "Spoken forms").
- **Source drift (not rendered):** `script.md`'s SHOW lines for S09, S10, S12, S14 and S16 still spell the old S-id chips;
  `script.md:1187` still says "five ponder timers (46 s)" (rendered: 42 s); `i18n/zh/glossary.yaml:525` and
  `GLOSSARY.md` lines 172 and 178 quote older zh wordings (verifier notes).

## Final-cut checks (1080p60, 2026-11-08)

- **Tags** (`report-tags.md`, round 2 on the re-stitched cut): 48 tags timed from the `events.json` sidecars plus scene
  offsets that match `chapters.txt` (the stitch about +0.03 s off), four frames each (`tags-r2/TNN_{in,mid,preout,
  after}.png`, `TNN_sheet.png`, `crops_1…4.png`). No defect. **S12 verified:** the bare-graph tag is gone (frames at
  20:05.9, 20:10, 20:15 and 20:19.3 show none; `tags-r2/s12/s12_topright_every2s.png`), and "slides 24–25" fades in at
  20:54.9–20:55.5 with the V1 inset and out with it at 21:06.6–21:07.2.
- **ASR** (`report-asr.md`, round 1): intelligible throughout; no real problem; the "Pulumi" watch item.
- **Visual** (`report-visual.md`, round 2, on the re-burned `.zh-en.mp4`, 08:51):
  - 39 contact sheets regenerated from the new file (4×4 tiles, one frame every 3 s, 00:00–30:24), all read
    (`sheets/sheet_01…39.png`), plus 20 full-size S12 frames (`r2/s12/`), 12 subtitle spot checks (`r2/subs/`) and chip
    frames (`r2/misc/`).
  - `freezedetect` (−60 dB, 4 s) over S12 (19:43.2–21:57.4): no frozen stretch (`r2/s12_freezedetect.log`, empty); the
    other scenes keep round 1's result on the pre-fix clean cut (`freezedetect.log`, 07:57: 31 stretches of 4 s or more,
    not the 19 that `report-visual-round1.md` counts; four lie inside ponder timers, at 10:10.6, 11:56.8, 23:45.7 and
    28:01.3; the longest is 01:08.4–01:19.6, 11.3 s, under the three-asks card; round 1 read the rest as narration over a
    held picture, but did not classify each of the 31 one by one).
  - No black or missing scene (14:18 is the planned part seam), no garbled glyphs, no persistent overlap, no tag stuck,
    ponder cards free of subtitles, the video ends empty (30:24).
  - Series rules: no instructor or staff name, no staff branch; only placeholders (`your-gcp-project`, `<your project>`,
    `<IP>.sslip.io`, `ac215-project` boxed "README default · change it", `sa_000…`), in-cluster 10.96.x / 10.244.x
    addresses on the kind stand-in, and `client-certificate-data: <redacted>` (21:15).
  - Five cosmetic notes (accepted item A5).
- **Pairs** (`report-pairs.md`, round 2, `.zh-en.srt` written 08:26, 508 cues): the condition-first failure is gone; A1,
  B1, B2, C1–C3, D6 and D7 fixed; every 如果/因为/当/时/直到/只有…才 clause in English order; one zh and one en line per
  cue; no break inside a command, path, flag or placeholder within a cue; the burned `.ass` matches the SRT in all 508
  lines; the parts concatenate to the full file.
  - The three commands still cut across two cues (`gcloud container clusters create test-cluster` | `--num-nodes 2 --zone
    us-east1-c`, 06:56.1–07:01.8, cues 123–124; `… delete test-cluster` | `--zone us-east1-c`, 13:58.5–14:03.6, cues
    245–246; `gcloud container clusters get-credentials` | `cheese-app-cluster`, 24:30.8–24:35.3, cues 412–413). They now
    break at the same point in both languages (the pairs check marks B3 "not fixed" for the cut, the tags check
    "verified" for the pairing; both describe this state). Accepted (A2).
  - Five minor one-item drifts (cues 28–29, 134–135, 146–147, 183–184, 284–285) and the English cut "there / is no
    cluster" (cues 115–116, D2): accepted (A3). Cue 345 (19:52.1) leaves out `invalid_grant:` in zh (rule against
    underscores in zh lines).
- **Measured** (`report-measured.md`, round 2, `measured.json`, evidence `r2m/`): all four MP4s decode with exit 0 and no
  errors; formats, loudness, subtitles, chapters and durations pass; SHA-256 unchanged over the run. Three notes: the S12
  tail (N1, below), seven zh-en cues whose top line is verbatim Latin (N2), `script.md:1187`'s 46 s (N3).

## Accepted items (coordinator decisions)

- **A1. Five ponders in 30:26.3** (one per 6.09 minutes), below AGENTS.md's aim of one per 2 minutes. Accepted under
  Conny's 2026-10-21 decision to keep the current density of 3–5 ponders per lecture (「我觉得可以保留现在的密度」); see
  gate 3.
- **A2. Three commands still cut across two cues** (06:56.1, 13:58.5, 24:30.8; see "Pairs"): each is wider than one zh
  line; they now break at the same point in both languages, and the full command is on screen in the terminal panel at
  each point (`r2/subs/s_420.5.png`, `s_841.png`, `s_1474.5.png`).
- **A3. The remaining minor one-item drifts** in `.zh-en.srt` (cues 28–29 at 01:46.5, 134–135 at 07:31.1, 146–147 at
  08:06.0, 183–184 at 10:18.5, 284–285 at 16:26.3; `report-pairs.md` lists the yaml item for each). Nothing is reversed
  or contradicted.
- **A4. Small tag leads at block starts** (T03, T08, T15) and T14 without a LECTURE mark (gate 2).
- **A5. The visual cosmetic notes** (`report-visual.md`): the chip pulse crossing its own text at 07:06.8–07:07.4 (S05)
  and 13:22.0–13:22.6 (S08); the "active account" pulse squeezing word spacing at 24:30 (S14); resource popovers covering
  a neighbouring node for 1–3 s at 19:18, 20:09 and 20:51–20:54 (S11, S12; the intended pattern); seven cues whose top
  line repeats the command or error verbatim.
- **A6. The QA nits left open** (listed under "Still open after QA", except S02's "(S06)", which is a should and is not
  in the coordinator's accepted list). A narration change needs a re-voice, a re-render and a re-burn; none changes
  meaning.

## Open items (not ruled on one by one; left for the coordinator)

None blocks playback; the first is a QA should that the coordinator's summary counts as fixed.
- ~~S02's "(S06)" on screen at about 01:55–02:01~~: fixed in fix round 2 (see "Still open after QA").
- **Bilibili description:** `video.yaml` `publish.description_zh` (line 64) credits the instructor by name. Not in the
  video or subtitle files, but it goes on the Bilibili page and the series rules say no instructor name.
- **Narration 46 words over the script's 3,900–4,300 band** (4,346 words after the QA additions: S01, S12's card, S15's
  Chroma note); `script.md`'s word-count section still reports 4,297.
- **The S12 tail:** the "if yours stops" card is narrated (21:41.7–21:46.8), then holds 10.6 s of digital silence
  (21:46.8–21:57.5, the longest non-ponder silence; `report-measured.md` N1) while its four lines are highlighted in
  turn. Intended as a pause-and-match hold, not a defect.
- **The English `.srt` wraps `run: web` over two lines inside cue 160** (09:04.9: "…a label, run:" / "web;"). The cue
  boundary fix holds and the burned `.zh-en` copy shows "run: web" on one line (`.zh-en.srt` cue 165).
- **Seven `.zh-en.srt` cues whose top line has no Chinese** (`measured.json` "top_line_without_cjk"): cues 123, 245, 253,
  325, 328, 399, 412 (e.g. 18:46.5 `pulumi preview --stack dev --refresh`, 18:53.3 `NoneType object is not
  subscriptable`); `.zh.srt` has four of the same kind (103, 274, 335, 348). Verbatim commands, errors and a heading,
  per the glossary's verbatim rule.
- **Part 1 has no recap of its own** (14:20; it ends on "Don't forget to delete").
- **Chapters:** every start is the scene start rounded down (up to 0.983 s early, S16: 28:29 against 28:29.98).
- **Frame rate:** 60 fps (the 1080p60 scene renders, as in L02–L21); the repo default for new episodes is 30 fps. The
  burned copy has one more video frame (109,577) than the clean cut (109,576).
- **Report discrepancies:** `report-measured.md` says silencedetect found 37 silences of 1 s or more; `measured.json` and
  `r2m/silencedetect-clean.log` hold 34. It also lists "Test yourself, 3 questions" by the three block starts (29:41.10,
  29:53.50, 30:06.95); the `.srt` has five questions (cues 488–497).
- **No `QA_FOLLOWUPS.md`** for L22, and no Bugbot thread was copied into the episode folder.

## Verified (final render)

All numbers are from `measured.json` and the five reports, on the files in `output/` as they are now (written 2026-11-08
08:26–08:53 UTC), except the ASR results, which are round 1's (see the header).

- **Files:** H.264 High, yuv420p, 1920×1080 at 60 fps, AAC LC 48 kHz stereo at about 177 kb/s. Each decodes in full with
  exit 0 and no errors (`r2m/<name>.decode.log`).

  | file | duration | size (bytes) | loudness | LRA | true peak | SHA-256 (first 12) |
  |---|---|---|---|---|---|---|
  | `ac215-l22-kubernetes-cloud.mp4` | 1826.318 s (30:26.3), 109,576 frames | 108,050,054 | −16.1 LUFS | 2.2 LU | −2.6 dBTP | `2bbaa7431a73` |
  | `ac215-l22-kubernetes-cloud.zh-en.mp4` | 1826.318 s, 109,577 frames | 105,555,668 | −16.1 | 2.2 | −2.6 | `d627404c3162` |
  | `ac215-l22-kubernetes-cloud_part1.mp4` | 859.707 s (14:19.7) | 51,548,419 | −16.1 | 2.1 | −2.7 | `68f2211294c9` |
  | `ac215-l22-kubernetes-cloud_part2.mp4` | 966.730 s (16:06.7) | 56,494,800 | −16.1 | 2.3 | −2.7 | `4648d87d1ab3` |

  The 16 scene renders sum to 1826.266 s (full cut +0.052 s); parts sum to 1826.437 s (+0.119 s against the full cut).
  S01–S08 sum to 859.600 s, S09–S16 to 966.667 s.
- **Subtitles:** `.srt` 500 cues, `.zh.srt` 429, `.zh-en.srt` 508. Part 1 has 243 / 209 / 250, part 2 257 / 220 / 258; the
  parts add up to the full counts.
  - In all nine files the indexes are sequential, the cues in order, inside the runtime, with no overlaps and none shorter
    than 0.8 s; the shortest are 1.000 s (`.srt`) and 1.294 s (`.zh.srt`, `.zh-en.srt`). The last cue ends at 1824.521 s
    (30:24.5).
  - Every `.zh-en.srt` cue has exactly two lines, no English line with Chinese characters.
  - The fix round changed only Chinese lines, in nine places (01:19, 05:14, 06:54, 12:45, 13:17, 13:56, 20:28, 24:27,
    26:04; `report-measured.md`), adding two cues; no new overlap.
- **Chapters:** 16 entries, titles equal to `video.yaml`'s in order, each start the floor of the scene's real start (within
  0.983 s). `chapters_part1.txt` has 8 entries, `chapters_part2.txt` 8 (part 2 at 00:00, 01:40, 03:33, 05:23, 07:37, 09:53,
  11:40, 14:10). `README.md` now carries them and the durations (this pass).
- **Scenes:** all 16 present and in order (S01 89.27 s, S02 96.13, S03 109.15, S04 119.87, S05 112.78, S06 122.73, S07
  110.02, S08 99.65, S09 100.13, S10 113.63, S11 109.85, S12 134.15, S13 135.63, S14 107.48, S15 149.50, S16 116.28);
  round 1's visual check found the last frame before each of the 15 scene boundaries, and the final frame, empty
  (`frames/scene_ends_sheet.png`), and round 2 S12's
  (`r2/misc/s12_end.png`).
- **Narration:** 151 SAY blocks, 4,346 words, 155.1 wpm over 1,680.9 s of voice; 576 anchors; no "anchor not found" in
  the 16 render logs.
- **Lecture tags:** 48 tags, each checked on frames 0.3 s after fade-in, mid-span, 0.3 s before fade-out and 0.5 s after;
  none overlapping, none outliving its scene.
- **QA fixes re-checked on the final cut** (by this record's writer, from the `.srt`, `.zh-en.srt` and frames): S12's
  card narration (cues 366–367, 21:41.7–21:46.8); S01's "This card comes back…" (`.srt` cue 22, `.zh-en.srt` cue 19, 01:19.2); S15's Chroma note
  ("Change line 150 to slash data…", in the `.srt`); `run: web` in one `.zh-en.srt` cue (165, 09:04.9); S09's card
  labels clear of the Pod dots at 15:05 (`writer/s09_cards_905.png`). S02's "(S06)" was still on screen
  (`writer/s02_note_117.png`) and is fixed in fix round 2 (the note now ends "(later)").
- **Privacy:** no instructor or staff name, staff branch, key, token or real IP on screen, in the subtitles, the
  transcript or the chapters (`report-visual.md`, `report-pairs.md`; this record's writer grepped `output/*.srt`,
  `transcript.md`, `chapters*.txt` for dotted-quad addresses outside 10.x and for the instructor's name: none).
- **Provenance** (`ASSETS.md`):
  - Terminal lines come from the 2026-11-07 captures in `assets/terminal/` (`laptop/`, `kind/`); each README command ran
    as printed, extras tagged `extra`, kind panels tagged `stand-in: kind, not GKE`; nothing in a terminal panel is typed
    by hand. Code panels quote `assets/source/` unchanged at `3ecef56` (one credential-like value left out).
  - Live: the toolbox build failure and fixed build, every tool check, every gcloud/Pulumi/kubectl command up to its
    first error, the local-backend Pulumi runs (`TypeError`, `+ 23 to create`, the stop at the VPC), and all kubectl on
    the kind stand-in (Deployment, Service `<pending>`, ReplicaSet, Pod replacement, DNS, exec, namespaces, the
    debugging block's real `namespace … not found` errors, a Job).
  - `expected`: the README's `Outputs:` block (IPs replaced). `illustration`: the console, the browser and the app, a
    successful `pulumi up` in dependency order, the request journey's cloud parts, the teardown and leftover audit. Costs
    are the digest's estimates ("roughly five to eight dollars a day by our estimate"), not measured.

## Not claimed

- **No human listened to this cut** or watched it. The listening gate rests on the series waiver quoted under gate 6, and
  the audio was checked only by machine (the ASR round trip and the onset check, on the round-1 cut).
- **The ASR check did not run on the final files.** It ran on the round-1 cut; the fix round re-rendered S12 (picture
  only, same length) and changed zh subtitle text only; the English `.srt` is identical, but the re-rendered S12 audio was
  not transcribed again.
- **The Chinese subtitles were reviewed by agents only:** the QA subtitle watcher, the narration/subtitle fixer, the scene
  verifiers and the pairs check. No human translator or native reviewer read them.
- **No GCP or GKE resource was created.** No Google account was used: no API was enabled, no service account or key
  created, no Artifact Registry repository made, no image built into or pushed to a registry, no GKE cluster (test or
  `cheese-app-cluster`) created or deleted, no `pulumi up` or `destroy` reached Google, no load balancer, NAT, disk or
  Workload Identity binding existed, and no cost was measured. Those steps stop at their first real error or are
  `illustration`s. The kubectl output comes from the kind stand-in, which has no cloud load balancer, node pool,
  autoscaler or Workload Identity; whether GKE prints the same on a later day was not checked. The README's suspected
  missing role (Service Account Admin on `gcp-service`) is marked unverified in the video.
- **No Docker Hub login or push** is part of the captures; base images came from `mirror.gcr.io` under their Docker Hub
  names after Docker Hub's anonymous limit answered 429 (`ASSETS.md`).
- **The app was never seen running:** the page, the footer's `API version: 3.0`, the RAG reply and the 502/503 while the
  API loads are drawn from the code, not observed.
- **The visual check sampled one frame every 3 s**, plus targeted frames; motion between samples was checked only by
  `freezedetect` (S12 in round 2, the clean cut in round 1). The two part files were measured (probe, decode, loudness,
  subtitles, chapters) but not sampled visually on their own. One frame of part 1 (01:57, during `_part1.srt` cue 32)
  shows no burned subtitle (`verify/parts_bands.png`); the parts were not checked further for burned text.
- **Most QA fixes were verified only on previews** (720p `--at` frames and `--every 2` sheets before the 1080p60 renders),
  not one by one on the final cut. This record's writer re-checked the items listed under "Verified"; the final-cut checks
  cover the rest only by their own sampling and by reading every cue.
- **Stated as the coordinator gave them, not checked here:** lexicon PR #126 (`fcd34c9`); the digest's re-check
  (Chroma's path from the registry config, the removed IPs and domain); the study guide on the MLOps_Learning branch; the
  independent script reviews and per-scene critics beyond their files; the resumed interruptions.
- **Review bots:** no `QA_FOLLOWUPS.md` exists for L22, and nothing in this record checks Bugbot threads on an L22 PR.
- **`README.md` durations and chapters were filled in this pass** from `measured.json` and `chapters*.txt`; its chapter
  summaries were not reviewed by a separate agent.
- **Every check in this record is an agent's.**

## Fix round after the final-cut checks

- **Round 1 findings fixed** (commit `a4521cf`, 2026-11-08 08:16 UTC):
  - S12: the "slides 24–25" tag over the bare V6 graph (round-1 T38, 20:05.9–20:19.5) removed; the remaining one fades in
    with the V1 inset (20:54.9) instead of 4.4 s before it.
  - Nine zh items (and the glossary examples) re-cut: A1's condition-first swap (01:19), B1–B3's commands (06:54, 13:56,
    24:27; each command on a cue of its own), C1–C3's repeated English (05:14, 12:45, 13:17), D6 and D7's drifts (20:28,
    26:04).
  - S12 re-rendered at 1080p60 (log 08:22, 134.149 s), the cut re-stitched (08:26) and re-burned (08:51), still 30:26
    (part 1 14:19, part 2 16:06); every scene duration unchanged.
- **Round-2 checks on the new files** (`report-tags.md`, `report-visual.md`, `report-pairs.md`, `report-measured.md`):
  all items verified, no regressions; measured passes (I −16.1 LUFS, TP −2.6 dBTP). The ASR report is from round 1.
