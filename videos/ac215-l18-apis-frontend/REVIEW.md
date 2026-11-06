# Review record: AC215 · Lecture 18 — APIs and frontend: a FastAPI service, a simple page and a React app

Follow-along of the Lecture 18 tutorials, each README section top to bottom, in two repositories:
[dlops-io/cheese-app-v1](https://github.com/dlops-io/cheese-app-v1) `main` @ `ce03a10` (the whole README) and
[dlops-io/cheese-app-v2](https://github.com/dlops-io/cheese-app-v2) `main` @ `447b5c3` (the course's Tutorials 23 and
25, plus "Setup & Run Cheese App", Troubleshooting and Docker Cleanup), with "Production images" shown as extras from
the README one push earlier (`e98fa55`) and **Tutorial (24): Simple Frontend App** from branch `2025` @ `14f2a14`.
Series decision (`BRIEF.md`, `ASSETS.md` "Which commit"): cheese-app-v2's `main` moved twice on the recording day
(07:23 −0500 to `e98fa55`, 07:52 to `447b5c3`), and `447b5c3` no longer has the simple frontend the lecture teaches,
so Tutorial 24 runs on branch `2025` with its own vector DB and API, last, after `main`'s clean-up; the video says
`git switch 2025` to follow along and `git switch main` to come back. Claude Code sessions (Claude) produced it.
Verified facts and unclaimed reviews are kept in separate sections.

- **Origin:** issue #108. Built end to end on 2026-11-05 by this coordinator's agents: digest, live laptop captures,
  brief, script + 4 independent reviews (`build/review_{accuracy,followalong,pedagogy,spoken}.md`,
  `build/review_merge_log.md`), `scenes/common.py`, 16 scenes each with a fresh critic, zh subtitles, `exercises.md`,
  `README.md` and the study guide (on the MLOps_Learning branch). Milestone commit `62f36ce` (2026-11-05 21:47 UTC).
- **Captures:** 2026-11-05, UTC 12:58–14:16 (`ASSETS.md`, "terminal/"), in a fresh, empty `docker:29.8.2-dind`
  "laptop" (Alpine, linux/amd64, user `student` uid 1000, Compose v5.6.0, git 2.54.0). Everything that runs on a
  laptop ran live: both clones, every `docker-shell.sh`, uvicorn/FastAPI and the demo routes, `/docs` and
  `/api/docs`, the 14,356 chunks loaded into Chroma, `/healthz` and `/readyz`, the CNN naming a cheese photo,
  `pytest` (26 passed), the Vite dev server and its proxy, `npm run check`, the nginx production image,
  `docker compose up --build`, the 2025 simple frontend with CORS, and the clean-up. That machine had **no Google
  account, no project and no key**: its `secrets/ml-workflow.json` is a well-formed file around a throwaway RSA key
  for no account, so every Gemini or embedding call stops at its honest first error, `invalid_grant: account not
  found`, and no Gemini answer appears anywhere. The browser is a schematic drawing tagged `illustration` (filled
  from the captured HTML and JSON); the GCP prerequisites are an `illustration`; the README's Troubleshooting rows
  are `recorded`. Capture-only changes (an HTTPS relay, base images rebuilt with the proxy's CA, part `c` on Docker's
  classic image store) are listed in `ASSETS.md`; none appears as a step.
- **Masking:** the instructor's name in two source files is masked `‹instructor›` in code panels; no capture contained
  it. A git branch name that names a teaching-staff member is cropped or masked wherever its capture lines are shown.
  Project IDs on screen are `ac215-project` (the repository's default, on the minus side of a diff) and
  `your-gcp-project`; session IDs are all zeros.
- **QA draft:** the 480p draft (31:59), linked as `build/qa/draft.mp4` on 2026-11-05 22:13 UTC (the draft file itself
  has since been deleted from `output/`).
- **Whole-video QA:** `/root/ac215-backup/tasks/l18-qa-withs56rz.output`, key `result`. 39 agents: seven watchers,
  15 scene fixers (S01–S03, S05–S16), one narration/subtitle fixer and 16 scene verifiers (S01–S16). The run log
  reads "L18: 62 issues from 7/7 watchers". Committed as `d10f4c8` (2026-11-06 00:50 UTC).
- **After QA, by the coordinator:** the shared fixes the scene fixers could not make in `scenes/common.py`, plus S14's
  hand-folded c14, committed as `b0c2bcf` (02:08 UTC): README trackers renumbered like the README (Vector DB 4 steps,
  Backend APIs 9, React Frontend Setup 6, Setup & Run 5), an opaque dim veil for ponder cards that sit on a set piece,
  `NetworkMap.on_box` backing, `lref()` writing "slide N" for one slide, a shared `trouble_card` (S07 and S09), and
  S14's c14 typed as four hand-folded rows. The toolkit bug found on the way (`Terminal.fold` dropped one character
  on a hard break) was fixed in its own PR #114 (merged as `9c2ea81`); lexicon PR #113 merged to `main` as
  `e867726`, which the CI release renders with (both per the coordinator; neither commit is in this clone).
- **Finishing pass:** none. The coordinator's list of finishing-pass outputs for L18 is empty (`[]`).
- **1080p60 renders:** all 16 scenes, 2026-11-06 02:16–02:57 UTC; S05, S14 and S15 were re-rendered 04:11–04:23 after
  fix round 1 (`e3390a5`, 04:07). None of the 16 logs in `build/logs/` contains "anchor not found" (this record's
  writer grepped them).
- **Final cut:** 32:11.2 (1931.236 s); parts 17:46.2 + 14:25.0. File times (UTC, 2026-11-06): the clean cut and the
  full-cut subtitles 04:29–04:30; the burned copy, `chapters.txt` and `transcript.md` 04:54; part 1 04:56; part 2
  04:57. The MP4s are not in Git (release assets).
- **Final-cut checks:** two rounds of agent checks; the coordinator saved each check's returned text as
  `build/final-review/report-{tags,asr,visual,pairs,measured}.md`, round 1 kept as `report-*-round1.md`. All five
  reports exist and were read in full for this record.
  - Round 1 (evidence 03:43–04:07 UTC) ran on the first stitch: no blocking defect; the tags check found two S15
    tags outliving their picture (about 9 s and 20 s), an S05 tag about 2 s early and an S14 pill missing a space.
  - Fix round 1 (`e3390a5`) changed only `s05_static.py`, `s14_branch.py` and `s15_cors.py`; the three scenes were
    re-rendered, the cut re-stitched and re-burned (still 32:11).
  - Round 2 re-ran **tags, visual and measured** on the files now in `output/` (evidence 16:33–16:51 UTC, after the
    last output file at 04:57): all four items verified, no regression.
  - **The ASR and pairs reports are round 1's** (`report-asr.md` and `report-pairs.md` are byte-identical to their
    `-round1` copies, dated 04:06), run on the pre-fix cut. The fix round touched no `script.md` or `i18n/` file, and
    this record's writer compared the subtitles: the current `.srt`'s 502 cue start/end times and texts equal those
    in `asr.json` (0 differences), and the current `.zh-en.srt`'s 501 cues equal `pairs-dump.txt` (the only 4
    differences are how the dump printed cues 112, 180, 258 and 396, whose top line has no Chinese). The audio of
    the three re-rendered scenes was not transcribed again.

**Conventions:**
- **Times** are mm:ss in the full cut (`output/ac215-l18-apis-frontend.mp4`, 1931.236 s), except in "Whole-video QA",
  which keeps the 480p draft's times (marked *draft*).
- **Cue numbers** name their file: `.srt` (502 cues) or `.zh-en.srt` (501).
- **Evidence paths** are relative to `build/final-review/`. That folder is git-ignored and exists only in the producing
  session; a successor re-runs the checks to reproduce it.

## Content gates (AGENTS.md)

1. **Hook** ✔. S01 opens on a broken expectation, not a value proposition: a request to the frontend's port answered
   by the API's server.
   - "Here is a request to port 3000, where this app's frontend runs." (`.srt` cue 1, 00:00.0); "But look who
     answered:" (cue 3, 00:07.4) "uvicorn, the API's server, and the API listens on port 9000." (cue 4, 00:09.3).
   - The second puzzle: last year's page "called port 9000 directly, and every answer carried a permission slip:"
     (cue 6, 00:17.4) "access-control-allow-origin: *." (cue 7) "This year's API sends no such slip at all." (cue 8,
     00:26.2) "So who carried the request from 3000 to 9000, and why did last year's page need permission?" (cues
     9–10, 00:29.4–00:32.6). The lecture's six steps plus "three and a half, the courier" (cue 13, 00:45.2).
   - **Payoff:** S11, "That is why uvicorn answered on 3000." (cue 320, 20:32.8), then the origin: "the API needs no
     permission slip." (cue 323, 20:42.5); S15 shows last year's CORS and its preflight (28:25–29:44, cues 443–462); S16, "Here is
     the whole trip, with the hook answered:" (cue 478, 30:42.8) to "one origin, no permission needed." (cue 483,
     30:58.9).
2. **Intuition before formalism, with an animated mechanism for each core idea** ✔. `BRIEF.md` ("Visual set pieces")
   defines eight, each animated next to the commands it explains:
   - **V1, the lecture's hop-by-hop request (`RequestTrace`; S01, S03, S05, S09, S11, S12, S15, S16):** the six numbered steps
     and the courier 3½ (00:36–00:49); v1 at `localhost:9000` (04:47–05:20); the static page's first trip, "a file
     comes back, and the browser draws it." (cue 128, 08:04.7); the Vite courier "carries each /api request across
     the network." (cue 319, 20:29.2); "only the outside changes." (cue 367, 23:28.7); the 2025 page's second arrow
     and step zero, "the preflight." (cue 454, 29:07.6).
   - **V2, the lecture's architecture (`ArchitectureMap`; S01, S02, S13, S16):** "the blueprint, one layer at a time."
     (cue 29, 01:36.4); the cluster pulled down onto the laptop (02:03–02:06, see QA); "Your four boxes rise into the
     cluster." (cue 485, 31:06.3).
   - **V3, uvicorn owns the socket, FastAPI is the app (`ServerAppDiagram`; S03, S04):** "uvicorn is the server: it owns
     the port and speaks HTTP." (cue 67, 03:56.1); `--host 0.0.0.0` "every interface" (cues 70–71, 04:11.9–04:17.5);
     after ponder 1, "the forwarded request arrives on the container's network interface," (cue 89, 05:47.7).
   - **V4, a function becomes a URL, routers graft under prefixes (`RouteTree`; S04, S08):** "A letter instead of a
     number bounces off the float type hint with 422." (cue 105, 06:39.8); "FastAPI answers 307" (cue 107, 06:47.3);
     "one function stamps out three chat routers" (cue 221, 13:58.5); "all 25 operations: the leaves of this tree."
     (cue 235, 14:55.2).
   - **V5, published ports vs container names (`TwoLocalhosts`; S06, S10, S11):** "the network's phone book now turns its
     name into an address." (cue 178, 11:09.6); after ponder 3, "Only code inside the network can use them" (cue 328,
     21:13.2); the API unplugged, "The browser gets 502 with an empty body:" (cue 331, 21:24.6).
   - **V6, liveness vs readiness (`ProbeLamps`; S07):** "/healthz says 200: the process is alive." / "/readyz says
     503" (cues 199–200, 12:21.1–12:25.5); "restart on liveness, send traffic on readiness." (cue 214, 13:35.0).
   - **V7, a chat is a file, not a memory (`ChatFile`; S09):** "one random UUID per browser" (cue 249, 15:47.6); "The
     API opens that session's chat file," (cue 250, 15:52.4); "so any copy of the API can answer." (cue 267,
     17:11.3).
   - **V8, one page per feature vs one app shell (`OneShell`; S10):** "Each carries its own header, script and style;"
     (cue 280, 17:56.5); "The app is one shell: a header defined only once, a footer," (cue 285, 18:16.8); the route
     table and the outlet (cues 289–292, 18:31.5–18:42.1).

   **Lecture slides:** a GREY "Lecture 18 · slide(s) … (APIs|Frontend)" tag top right, 29 tags, one per `lref()` call
   in `scenes/*.py` (`report-tags.md`), 30 spans because S15's "slides 24–26" now leaves and returns with its
   picture. Per scene: S01 2, S02 4, S03 3, S04 1, S05 2, S06 1, S08 5, S09 1, S10 3, S11 1, S12 1, S15 2 (3 spans),
   S16 3; none in S07, S13 or S14. Cited: APIs 4–5, 7–13, 14–19, 19–21, 25–26, 27–28, 29, 30–33, 34–41, 39–41, 41,
   42, 43, 44, 45, 46; Frontend 16–17, 18–23, 24–26, 27, 30–31, 32–33, 35–37, 40–41. The decks are redrawn, never
   shown (`SLIDES.md`; its "This video and the slides" map was written before the script, so the per-tag table in
   `report-tags.md` is the scene ↔ slide record for the final cut).
   - All 30 spans pass the hard checks on round-2 frames (`tags-r2/`): correct wording ("slide N" for one slide,
     "slides a–b" for a range, every tag names its deck), no overlap in any crop (closest: the S15 tracker line ends
     about 55 px left of the tag), none on screen at its scene's end (latest fade-out relative to its scene: S16, at
     59.23 s of 104.45 s). Two tags share the spot only during the planned 0.4–0.6 s cross-fades and morphs.
   - Accepted: the S10 and S11 tag nits (item A4).
3. **Pause-and-ponder moments and a recap**: ✔ for the ponders, by Conny's decision for the series (accepted item
   A1); ✔ for the recap.
   - **Ponders:** five, each a card followed by a timer (`measured.json` "ponder_moments": each scene's `events.json`
     plus its scene start; answers from the `.srt`).

     | # | scene | card (from `script.md`) | card | timer | answer starts |
     |---|---|---|---|---|---|
     | 1 | S03 | uvicorn listens on --host 127.0.0.1 inside the container instead. curl from inside the container: works? Your browser on localhost:9000: works? | 05:32.9 | 8 s | 05:42.6 "Inside, yes: the container's own loopback answers." (cue 87), then "From the browser, no:" (cue 88) |
     | 2 | S07 | /healthz says 200, /readyz says 503. Restart the container, or just wait? | 13:10.5 | 8 s | 13:19.1 "Wait: about nine seconds later, /readyz says 200:" (cue 209) |
     | 3 | S11 | Could the page's JavaScript call http://cheese-app-api-service:9000 directly? | 20:56.5 | 8 s | 21:05.1 "No. The JavaScript runs in your browser, on the laptop," (cue 326) |
     | 4 | S12 | The production frontend container won't start while the API is down. Why would a page server care? | 23:53.3 | 6 s | 23:59.9 "It exits at once: host not found in upstream." (cue 374), then why (cue 375) |
     | 5 | S15 | Last year's page needed CORS. This year's React app does not. What changed: the API, the browser, or the origin it calls? | 29:54.9 | 8 s | 30:03.5 "The origin." (cue 466) |

   - **Rate:** 5 cards in 32:11.2, 0.31 per 2 minutes (`measured.json` "ponder_per_2min" 0.311), one every 6.4
     minutes, against AGENTS.md's aim of one per 2 minutes (about 16). Part 1 has 2, part 2 has 3. The longest
     stretches without a card are 465.9 s (13:10.5–20:56.5, S07 to S11), 457.6 s (05:32.9–13:10.5) and 361.6 s
     (23:53.3–29:54.9); the first card comes at 05:32.9 and the last 136.4 s before the end.
   - **Decided by Conny (2026-10-21), as recorded in `videos/ac215-l05-rag/REVIEW.md` gate 3:**
     「我觉得可以保留现在的密度」: keep the current density, which that record gives as 3–5 ponders per lecture plus a
     spoken recap and test questions. L18's five ponders are inside that series density and below AGENTS.md's aim.
   - **Recap:** S16 "Tear down, recap, and what's next" from 30:26.7 (104.45 s).
     - 30:26.7–30:42.8: the clean-up checklist ("Before you go, a cleanup checklist, all done once already.", cue 473):
       exit every container, compose down, back to `main`, prune after checking its list, remove the `node_modules`
       volume and big images by name; "Your key stays in secrets." (cue 477).
     - 30:42.8–31:04.2: the whole trip with the hook answered (cues 478–483).
     - 31:04.2–31:25.3: the lecture's blueprint, "NGINX in front, the registry and the persistent disk are still
       dashed: the next lectures build them." (cues 486–487); the project assignment (cues 488–490).
     - 31:25.3–32:09.0: "Test yourself, pausing on each." (cue 491) and five questions (cues 492–502). The answers are
       in `exercises.md`.
4. **Narration written for the ear, with word-anchored cues** ✔.
   - **Spoken style:** commands and identifiers are said in words where the display differs ("change into" for `cd`,
     "cheese app v2" with the display `cheese-app-v2`, "local storage" displayed `localStorage`), with the literal
     form in the subtitle's `en_display`; the error string is shown verbatim (`Invalid grant: account not found`).
   - **Size:** 159 SAY lines, 4,309 words (`measured.json` "narration"); the `.srt` has 4,149 words. Kokoro `af_heart`
     at speed 0.9: 1,769.9 s of voice (91.6 % of the runtime), 146.1 wpm over the voice and 133.9 wpm over the
     runtime.
   - **Anchors:** 622 `wait_until` anchors across the 16 scene files (S01–S16: 28, 36, 45, 32, 32, 47, 42, 35, 39, 48,
     51, 41, 36, 35, 41, 34; `common.py` none). None of the 16 render logs contains "anchor not found".
   - **Pronunciation:** the QA ASR watcher found no mispronunciation (uvicorn, nginx, Vite "veet", CORS, Tolminc all
     consistent with the lexicon) and two sync problems: S04's was fixed, S16's was left open (see "Whole-video QA").
   - **Final ASR** (`report-asr.md`, round 1, see the header): one minor mispronunciation ("preflight" heard as
     "Proflight", cue 454, 29:07.6) and one cue split 1.31 s ahead of its speech (cue 205, 12:46.4); both open nits.
5. **Simulated-target-viewer QA over the full draft** ✔.
   - Seven watchers reviewed the 480p draft: two directors and two simulated target viewers ("newcomer"), one of each
     per part; a subtitle watcher, a follow-ups watcher and an ASR watcher. They worked from contact sheets, frames
     pulled from the draft, the scene code, the subtitle files, the three READMEs and the captures.
   - **62 timestamped findings: 4 must, 31 should, 27 nit.** The four musts (three about README tracker numbers that
     disagreed with the spoken README step, one about an S14 command typed with a dropped character) were fixed by
     the coordinator after the QA run and are verified on the final cut (`writer/trk_stack.png`,
     `writer/c14c_stack.png`; see "Verified"). Each scene's fixes were checked by a skeptical verifier; several
     verifiers completed or redid a fix (S04, S05, S08, S09, S11, S14, S16). What stayed open is listed under
     "Whole-video QA".
6. **Measured checks** ✔. The numbers are under "Verified" (`measured.json`, measured on the final files).
   - **Duration:** 32:11.2 (1931.236 s), inside the series' 25–35 min. The parts are 17:46.2 (1066.203 s) and 14:25.0
     (865.048 s); their container durations sum to 0.015 s more than the full cut, and their video frame counts sum
     to the clean cut's exactly (63,969 + 51,901 = 115,870). Part 1 ends on the S10 boundary (17:46.15).
   - **Loudness:** −16.0 LUFS integrated in the clean cut, the burned copy and part 2, −16.1 in part 1; LRA 2.4 LU
     (part 1: 2.3); true peak −2.7 dBFS in all four.
   - **Caption bounds** (`report-measured.md`, `report-visual.md`, `report-pairs.md`): every one of the 501
     `.zh-en.srt` cues is exactly two lines, Chinese above English; the burn file `.zh-en.ass` has `WrapStyle: 2`,
     Noto Sans CJK SC at 50 with the English row at `\fs33`, so no cue can wrap to a third line. The widest line,
     cue 380's English (24:25), measures about 1,456 px even at size 50, against 1,840 px usable
     (`pairs-cue380-crop.png`, `pairs-widths.txt`); the longest English line is 93 characters (01:32.8) and the
     longest Chinese lines 48 characters (27:55.7 and 31:35.9), both inside the frame on the sheets. The subtitle band sits at
     about y 990–1070 and terminals end at about y 880; 12 spot checks (03:49–30:22) found no command a viewer must
     copy covered (`frames-r2/subs/stackA.png`, `stackB.png`).
   - **Music balance:** does not apply. L18, like the other AC215 lectures, has no score: `video.yaml` has no `music:`
     key.
   - **Subtitle sync** (`report-asr.md`, onset check with large-v3-turbo word timestamps on 16 boundaries): one cue
     starts more than 1 s before its speech (cue 205, 12:46.4, +1.31 s); every other checked boundary is under 1 s
     (largest: cue 412 +0.89 s, cue 178 +0.88 s, cue 32 +0.82 s).

   **Human review:** the series waiver stands in for a listening sign-off.

   Listening sign-off: waived by Conny for the AC215 series (Explainer_Videos#29, 2026-10-15): 「不需要，我现在对视频质量很满意的」 — no human listened to this cut; the ASR round trip below is the substitute.
   Review moments optional since 2026-10-22 (AGENTS.md): 「我大概率是不会进行审片的，因为我觉得做得已经非常好了，就让bugbot来检查就好了」

   **ASR round trip** (`report-asr.md`, round 1, on the pre-fix clean cut with the same narration and subtitles):
   - faster-whisper `base.en` over the whole cut: 502 cues compared, 4,390 words recognised, 268 cues with some
     difference (`asr.json`, `asr.log`).
   - `large-v3-turbo` re-ran 36 doubtful cues on their own clips (cue ±0.3 s; `asr-clips/`, `large.log`,
     `large.json`). Every word base.en seemed to swallow (cues 25, 39, 57, 58, 59, 151, 153, 209, 255) is spoken;
     cue 205, which base.en dropped whole, is transcribed in full.
   - 266 of the 268 differences are recogniser noise: digits against words, joined or split compounds, spoken forms of
     code (`/api` "slash api", `/healthz` "health z"), names the recogniser cannot know (uvicorn, nginx, Vite, CORS,
     Tolminc), homophones (too/2, git/get, ours/hours) and words counted across a cue boundary. The two real items
     are the "preflight" vowel and the cue-205 split (open nits).

## Whole-video QA (480p draft, 31:59; times are *draft* times)

**Watchers and findings** (`l18-qa-withs56rz.output`, key `result`):

| watcher | must | should | nit |
|---|---|---|---|
| director, part 1 | 1 | 9 | 6 |
| newcomer, part 1 | 2 | 4 | 4 |
| director, part 2 | 1 | 9 | 5 |
| newcomer, part 2 | 0 | 4 | 4 |
| subtitles | 0 | 4 | 7 |
| follow-ups | 0 | 0 | 0 |
| ASR | 0 | 1 | 1 |
| **total** | **4** | **31** | **27** |

- **By target:** 36 scene, 11 subtitles, 10 shared code, 5 narration.
- **By kind:** 16 follow-along, 12 picture, 11 subtitle, 8 text, 6 sync, 5 pacing, 2 continuity, 1 narration, 1 fact.
- **By scene:** S09 8, S11 8, S06 7, S14 5, S16 5, S02 4, S03 4, S07 4, S15 4, S12 3, S01 2, S05 2, S10 2, S13 2,
  S04 1, S08 1.
- **Facts:** the part-1 director checked every terminal panel against its capture (`a01`–`a32`, `b03`–`b46`,
  `p01`–`p06`) and the README sources: all typed commands match, shown output comes only from captures; the part-2
  director confirmed the 14,356 counter (the sum of `c06`'s eleven inserts) and main's model name against the
  digest. No watcher found an instructor name, a key or a real project ID.
- **Follow-ups watcher:** found no `QA_FOLLOWUPS.md` for L18 (none ever existed; not in `git log --all`); no L18 PR and
  so no Bugbot threads; issue #108 had no comments; no TODO/FIXME in the scenes. It reported no issues and noted that
  the scene critics' findings were not saved to a follow-ups file.
- **Subtitle watcher:** read 420 `zh.srt`, 497 `zh-en.srt` and 501 English cues of the draft; mechanical checks clean.
  Three pairings that cut a phrase or put a clause under the wrong English (01:49 一个存 / image, 20:44
  container / 名字, 28:59 the OPTIONS sentence), the S15 header split ("*: permission granted." as its own cue), and
  smaller order and `en_display` items.
- **ASR watcher:** 501 cues against base.en, 39 doubtful cues re-run with large-v3-turbo; no mispronunciation; two
  sync problems: cue 109 (*draft* 06:57) 2.6 s late and cue 494 (*draft* 31:30) 1.4 s early, both where a long
  spoken number or address sits mid-sentence.

**The musts, and how they were fixed:**
- **M1–M3, README tracker numbers one ahead of the spoken README step** (director part 1 and newcomer part 1, S06
  *draft* 10:03–11:15 and S07 *draft* 11:52; the same pattern was reported as should items for S10 and S13 and a nit for
  S14). The tracker split "cd" and "docker-shell" into two steps while the narration read the README's numbers, so
  "Step 2, inside the container" played over "step 3 of 5: Load database". **Fix** (`b0c2bcf`, `scenes/common.py`
  `STEPS`): "cd + docker-shell" is one step in Vector DB (4 steps), Backend APIs (9), React Frontend Setup (6), and
  Setup & Run counts "cd src + compose up" as one (5); every `track()` index in S06–S13 lowered to match. **On the
  final cut** (`writer/trk_stack.png`, crops by this record's writer): "Step 2, inside the container:" (10:23.5) over
  "step 2 of 4: Load database" at 10:26.5; "Step 3: chat." (10:41.5) over "step 3 of 4: Try chat" at 10:42.2; "Step
  2: api_server." (11:50.8) over "step 2 of 9: api_server" at 11:52.0; "Step 3: /healthz says 200" (12:21.1) over
  "step 3 of 9: Check probes" at 12:23.0; "Step 2: npm run dev." (19:17.0) over "step 2 of 6" at 19:18.5; "Step 3:
  open localhost:3000." over "step 3 of 6: Open 3000" at 19:31.5; "Step 3: change into src," (24:41.2) over "step 3 of
  5: cd src + compose up" at 24:44.0. S14's 2025 tracker names the README's own numbers ("step 4 of 7: Backend 1: cd
  api-service…" at 26:57.0 under "Backend steps 1, 2 and 4, in a new terminal", cue 421, 26:52.4).
- **M4, S14 *draft* 27:15: the extra c14 command typed with a dropped character** (director part 2): `json.lo \` then
  `d(sys.stdin)…`, a backslash inside the quoted python. Cause: `Terminal.fold`'s hard-break path. The scene fixer
  switched to a soft wrap; the coordinator replaced that with four hand-folded rows (`C14_PIECES`, `b0c2bcf`) whose
  ` \` continuations sit outside the quotes, asserted to rejoin to the exact capture text, and fixed the toolkit bug
  in PR #114. **On the final cut** at 27:28.5 and 27:29.2 the four rows read `sed -n '35,42p' \` /
  `api/service.py; curl -s http://localhost:9000/openapi.json | \` / `python3 -c 'import json,sys;
  [print(m.upper().ljust(6), p)` / `for p,v in json.load(sys.stdin)["paths"].items() for m in v]'`
  (`writer/c14c_stack.png`); the output follows at 27:30 (`writer/c14b_stack.png`).

**The shoulds, examples by kind** (fixed and verified, except those under "Still open"):
- **Follow-along:** S06's `sed` placeholder gets chips "`your-gcp-project` → your own project ID" and "on a Mac:
  `sed -i '' …`"; S06's extra listing shows a "…" row and "23 names: 1 zip + 11 chunk files + 11 embedding files";
  S09's curl extras fold at spaces with ` \` in a 6-row strip; S09 and S11 explain `/tmp/identify.json` with a chip
  or card; S12's failing restart command stays whole in a 5-row strip above its `[emerg]` rows; S14's Compose v2
  card now names the last line of `docker-shell.sh`; S15's no-key log carries a GREY tag "recorded without a key ·
  with yours: the retired model fails".
- **Pictures and text:** S02's cluster leaves the dashed GCP boundary before it becomes "your laptop"; S03's ponder
  card moved off the objects its question names; S03's CORS ring no longer cuts the comment line; S07's and S09's
  Troubleshooting rows are a symptom / "→ fix" card (`trouble_card`, now shared); S09's "26 passed" badge got an
  opaque backing (and S10's through `NetworkMap.on_box`); S12's ponder card dims the set piece behind it (the shared
  veil); S16's disk chip clears checklist item 6, and NGINX is no longer counted among "your four boxes".
- **Sync and pacing:** S04's codes sentence is its own sentence and each code colours as it is read (the 2.6 s lag is
  gone: no such lag in the final ASR); S05's two ^C / exit strips sit side by side for about 3–6 s; S11's api.js
  17–24 panel holds about 2.9 s and the `server: uvicorn` proof lands on its sentence; S13's `Exited (0)` row holds
  about 2 s.
- **Subtitles:** 13 of 16 narration/subtitle items applied (9 as given, 4 with changes); `python -m explainer.i18n
  check … --lang zh` printed OK. S04, S11 and S14 were re-voiced.

**Still open after QA, and why:**
- **S07 *draft* 12:55, the Troubleshooting card plays with no voice** (newcomer nit): a new SAY sentence for a nit was
  outside the fixer's rules; the card is now readable for about 8 s.
- **S16 *draft* 31:30, recap question 2's cue runs ahead of "0.0.0.0 … reload"** (ASR nit): needs a SAY split; the
  anchor was made split-proof. On the final cut the largest such lag is under 1 s (`report-asr.md`: "and reload each
  do" at 31:42).
- **S11, beat 7** (verifier): the Cheese books command shown is capture `b40`, which calls `localhost:9000`, while the
  narration says those chats go through the proxy on 3000 (needs a new capture or a script change); "▶ your turn"
  there is on screen about 0.7 s; the 502 walker and the courier overlap the Vite chip and the 3½ badge for about
  0.3 s each (`common.py` walk path).
- **S14:** the fallback card is not spoken; no visible `cd ..` (no capture exists for it, and `script.md` says it is
  not typed).
- **S15:** "the same Gemini error" could say "the same 500" (needs a re-voice); the zh.srt line break "…请求会 /
  让浏览器先问一声".
- **Subtitle line breaks the wording could not fix** (fixer): zh.srt "按 container / 名字" (S11 ponder), "切回 / main"
  (S16), and the bilingual English cut at "the lecture / teaches" (S02).
- **Small leftovers named by verifiers:** S16 item 6's text starts about 6 px left of the others; in S16's blueprint the
  dashed outline round "Artifact Registry" touches "data & models"; S06's `sed` folds before an option (valid to
  paste); S15 beat 7's "access-control-allow-methods" row may sit about 0.15 units left (not re-checked on a second
  frame); S09's envelope touches the browser frame at the bounce.
- **Toolkit requests not acted on:** `type_cmd` choosing a soft wrap for long quoted strings; `ChatFile.post(ok=False)`
  still paints a solid red block for other callers.
- **Source drift (not rendered):** `script.md`'s SHOW lines for the S14 fallback card (around line 1214) and S16's "four TEAL
  boxes … NGINX" no longer match the scenes; `i18n/zh/GLOSSARY.md:181` and `glossary.yaml:448` quote S09's old zh
  wording.

## Final-cut checks (1080p60, 2026-11-06)

- **Tags** (`report-tags.md`, round 2): 29 tags, 30 spans, four frames each (`tags-r2/tNN_{a,m,b,x}.png`, sheets,
  `overview_1…6.png`, dense sheets for S05 and S15), timed from the `events.json` sidecars plus scene offsets that
  match `chapters.txt` to the frame. The four round-1 items verified:
  - S15 "slides 24–26 (Frontend)" fades out with the RequestTrace at 28:41.67 and back in with it at 28:49.93; frames
    28:42.68–28:49.68 show only the curl terminal (`dense/s15a_sheet.png`).
  - S15 "slide 27 (Frontend)" fades out with the trace at 29:18.17; frames 29:18.68–29:38.18 show the terminals with no
    tag (round 1: on until 29:38.33) (`dense/s15b_sheet.png`, `t26_x.png`).
  - S05 "slides 16–17 (Frontend)" fades in at 07:22.13 with the page outline (round 1: at the scene start)
    (`dense/s05_sheet.png`).
  - S14's pill reads `localhost:9000/docs (no /api)` with a gap before "(" at 27:16.58, in the clean cut and the burn
    (`s14_pill_27-16.58*.png`).
- **ASR** (`report-asr.md`, round 1): intelligible throughout; 266 of 268 differences noise; 2 minor real items.
- **Visual** (`report-visual.md`, round 2, on the re-burned `.zh-en.mp4`):
  - 41 contact sheets (one frame every 3 s at true frame time, 4×4 tiles), all read, plus full-size frames and grids
    (`sheets/r2_sheet_001…041.png`, `frames-r2/`).
  - All three fixes show; S05, S14, S15 and the film end on an empty background; no black or missing scene; every
    chapter boundary passes through an empty background.
  - No clipped or overlapping text, nothing outside the frame, no tag stuck on screen, no garbled glyph in a settled
    frame; the odd-looking tiles (01:33, 18:33–18:45, 20:30, 21:21, 22:45, 23:18, 30:54) are mid-transition.
  - `freezedetect` on S05 and S14–S15 (fps 10, n=0.001, d=4): 28:37.4 (4.1 s, under narration) and the ponder card at
    29:56.6; a looser run flags 29:39.9–29:51.8 (11.9 s, the "2025 vs main" two-panel, labels writing in). Round 1's
    whole-film run found six holds of 4.0–4.2 s under narration (04:02.7, 04:15.4, 05:26.1, 13:06.5, 13:29.8,
    17:24.8). All accepted (A3).
  - No instructor name on screen; project IDs only as placeholders; session IDs all zeros; the key file is named,
    never shown.
  - The visual agent reports one rule breach of its own: a wildcard `rm -f build/final-review/sheets/r2_sheet_*.png`
    after stopping its own run (inside `final-review/`, limited to files that run could have written).
- **Pairs** (`report-pairs.md`, round 1; the zh-en text is unchanged, see the header): all 501 cues read, zh against
  en. No meaning swap anywhere, including every 如果/因为/当/所以 clause (11 cue groups checked); one Chinese and one
  English line per cue; no break inside a command, path, flag or placeholder. Seven small drifts (open nits).
- **Measured** (`report-measured.md`, round 2, `measured.json`): all four MP4s decode with exit 0 and no error or
  warning lines. Formats, loudness, subtitles, chapters, narration and the part split pass. The ponder density is
  decided under gate 3; zh-en cue 258 is item A2.

## Accepted items (coordinator decisions)

- **A1. Five ponders in 32:11.2** (0.31 per 2 minutes), below AGENTS.md's aim of one per 2 minutes. Accepted under
  Conny's 2026-10-21 decision to keep the current density of 3–5 ponders per lecture (「我觉得可以保留现在的密度」); see
  gate 3.
- **A2. `.zh-en.srt` cue 258 (16:43.7)** keeps the English error string verbatim on the Chinese line (`Invalid grant:
  account not found`): it is quoted terminal output, the string a viewer will see in the API's terminal. Cues 112
  (06:55.1, the status-code list), 180 (11:16.5, "Backend APIs") and 396 (25:26.1, "Docker Cleanup") are literal by
  design (README headings and codes as written).
- **A3. Still pictures under running narration:** the S15 "2025 vs main" two-panel at 29:39.9–29:51.8 (11.9 s nearly
  still at the loose threshold, not a freeze at round-1 sensitivity; quieter since the fix removed the tag fade at
  29:38), and the 4.0–4.2 s holds at 04:02.7, 04:15.4, 05:26.1, 13:06.5, 13:29.8, 17:24.8 and 28:37.4.
- **A4. Lecture-tag nits that follow `script.md`:** S10 "slides 35–37 (Frontend)" leaves at 18:45.62 about 1–1.7 s
  before the shell picture (`tags-r2/t22_x.png`); S11 "slides 24–26 (Frontend)" stays on over api.js after the trace
  leaves at about 20:01 (on until 20:11.10).
- **A5. The QA nits left open** (listed under "Still open after QA"). A narration change needs a re-voice, a re-render
  and a re-burn; none changes meaning.

## Open nits (not ruled on one by one; left for the coordinator)

None blocks release. Each needs a narration, yaml, scene or toolkit change and a rebuild, which this record does not
make.
- **"preflight" heard as "Proflight"** (`report-asr.md`): cue 454 at 29:07.6, "step zero, the preflight." Both models
  hear "Proflight"; Kokoro's phonemes are `pɹɪflˈaɪt`. It is the only spoken "preflight"; the subtitle and the screen
  spell it. Suggested: a lexicon entry `preflight: {say: "pree-flight"}` in a toolkit PR for future episodes
  (`asr-clips/cue454.wav`).
- **Cue 205 appears 1.31 s before its speech** (12:46.4): "404." from cue 204 is still being spoken while cue 205
  ("everything the browser calls is under /api…") is on screen (`asr-boundaries-large.json`, `asr-clips/cue205.wav`).
- **Seven `.zh-en.srt` pairs** where one word or phrase sits one cue early or late in one language (`report-pairs.md`,
  with the yaml item to fix each): 149/150 (09:21, "the API"), 257/258 (16:41, "the same"), 270/271 (17:21,
  "docker-shell.sh again"), 285/286 (18:16, "a footer"), 340/341 (21:55, same as 270/271), 370/371 (23:48, "why …
  care", the closest to a clause swap, meaning intact), 450/451 (28:44, 星号 split from its header,
  `pairs-cue450-crop.png`).
- **Visual, round 1:** the RED "502" badge fades in over the "uvicorn" chip for about 1 s around 21:22.5; in the S16
  checklist the serif "or" sits slightly above the monospace baseline (30:41).
- **Tag leads:** S01 "slide 27" leads its trace by 0.8 s and S02 "slide 43" its tree by 1.5 s, during transitions.
- **Homophones a listener may notice:** "ours" heard as "hours"; "No." heard as "Now," at cue 326 (21:05.1; phonemes
  correct, the 0.6 s pause before "The"); "2025" read as "two thousand twenty-five" (spoken in cues 50, 408, 409, 411, 418 and 428;
  `report-asr.md` names 411 and 417; unverified which reading the audio has).
- **Chapters:** every start is the scene start rounded down (largest gap 0.717 s; part chapters within 0.933 s).
- **Frame rate:** 60 fps (the 1080p60 scene renders, as in L02–L17); the repo default for new episodes is 30 fps. The
  burned copy has one more video frame (115,871) than the clean cut.
- **No `QA_FOLLOWUPS.md`** for L18, and no Bugbot thread was copied into the episode folder.

## Verified (final render)

All numbers are from `measured.json` and the five reports, on the files in `output/` as they are now (written
2026-11-06 04:29–04:57 UTC), except the ASR and pairs results, which are round 1's (see the header).

- **Files:** H.264 High, yuv420p, 1920×1080 at 60 fps, AAC LC 48 kHz stereo at about 175–177 kb/s, video at about
  294–322 kb/s. Each decodes in full with exit 0 and no error or warning lines (`decode_*.log`,
  `decode_status.txt`).

  | file | duration | video frames | size (bytes) | loudness | LRA | true peak |
  |---|---|---|---|---|---|---|
  | `ac215-l18-apis-frontend.mp4` | 1931.236 s (32:11.2) | 115,870 | 119,202,417 | −16.0 LUFS | 2.4 LU | −2.7 dBFS |
  | `ac215-l18-apis-frontend.zh-en.mp4` | 1931.236 s | 115,871 | 116,191,635 | −16.0 | 2.4 | −2.7 |
  | `ac215-l18-apis-frontend_part1.mp4` | 1066.203 s (17:46.2) | 63,969 | 64,048,059 | −16.1 | 2.3 | −2.7 |
  | `ac215-l18-apis-frontend_part2.mp4` | 865.048 s (14:25.0) | 51,901 | 55,163,154 | −16.0 | 2.4 | −2.7 |

  Audio runs longer than video in every file: 69 ms (clean), 53 ms (burned), 53 ms (part 1), 31 ms (part 2). The 16
  scene durations from the sidecars sum to 1931.167 s, equal to the clean cut's video stream. The burned copy has one
  video and one audio stream (subtitles burned in, no soft track).
- **Subtitles:** `.srt` 502 cues, `.zh.srt` 421, `.zh-en.srt` 501. Part 1 has 276 / 232 / 276, part 2 226 / 189 /
  225; each language's parts sum to its full file.
  - In all nine files the indexes are sequential, the cues in order, inside the runtime, with no overlaps and none
    shorter than 0.8 s; the shortest are 1.003 s (`.srt`), 1.273 s (`.zh.srt`) and 1.093 s (`.zh-en.srt`).
  - The last cue ends at 1929.021 s (32:09.0), 2.2 s before the cut ends.
  - Every `.zh-en.srt` cue has exactly two lines; 497 have Chinese on top; the four without are A2's. `.zh.srt` cues
    92 and 151 are the same literal status-code list and heading.
- **Chapters:** 16 entries, titles equal to `video.yaml`'s in order, each start the floor of the scene's real start
  (within 0.717 s). `chapters_part1.txt` (9 entries) and `chapters_part2.txt` (7, at 00:00, 02:09, 04:25, 06:25,
  08:02, 10:09, 12:40) match (within 0.933 s). `README.md` now carries them and the durations.
- **Scenes:** all 16 present and in order (S01 82.63 s … S16 104.45 s; the visual and tags checks matched every
  boundary to the cumulative `events.json` durations); every scene ends on an empty frame.
- **Narration:** 159 SAY lines, 4,309 words, 146.1 wpm over 1,769.9 s of voice; 622 anchors; no "anchor not found"
  in the 16 render logs.
- **Lecture tags:** 29 tags in 30 spans, each checked on frames 0.2 s after fade-in, at the middle, 0.2 s before
  fade-out and 0.5 s after; none overlapping, none outliving its scene; S05 and S15 now on only while their picture is.
- **The QA musts on the final cut:** the README trackers read the spoken step numbers at 10:26.5, 10:42.2, 11:52.0,
  12:23.0, 19:18.5, 19:31.5 and 24:44.0 (`writer/trk_stack.png`); c14 reads exactly as captured at 27:28.5–27:29.2
  (`writer/c14c_stack.png`). Both extracted by this record's writer.
- **Privacy:**
  - No instructor name on screen (sheets, `report-visual.md`); none in the nine subtitle files or `transcript.md`.
    This record's writer grepped those ten files for the staff branch name, 12-digit numbers and `AKIA`/`AIza` key
    patterns: 0 matches.
  - On screen, project IDs are `ac215-project` / `your-gcp-project`, session IDs zeros, the key file named but never
    shown; what remains are container and image hashes, public git SHAs and the repository's sample newsletter UUIDs
    (15:06–15:12).
- **Provenance** (`ASSETS.md`):
  - Terminal lines come from the 2026-11-05 captures in `assets/terminal/` (`p`, `a`, `b`, `d`, `f`, `e`, `c`); each
    README command ran exactly as written, in README order, with extras tagged `extra` (`-x-` in the capture name);
    nothing in a terminal panel is typed by hand. Code panels quote `assets/source/` copied unchanged at `ce03a10`,
    `447b5c3` (with `e98fa55`'s README for "Production images") and `14f2a14`.
  - Live: v1's API (uvicorn 0.38.0 / FastAPI 0.120.4), the `square_root` route, 422 and 307, `/docs`; the simple
    frontend on 8080; main's vector DB (Chroma 1.5.9, 14,356 chunks), API (`/healthz` 200, `/readyz` 503 then 200),
    25 operations in `/api/docs`, the CNN's "parmigiano" at 58 percent, `pytest` 26 passed; Vite 8.3.5 with its proxy
    and the 502 when the API is unplugged; `npm run check`; the nginx 1.31.8 production image (94.8 MB) and its
    `host not found in upstream`; `docker compose up --build` and `down`; `docker system prune`; branch `2025`'s
    vector DB, API and three pages with CORS and the `OPTIONS` preflight.
  - `illustration`: the browser views and the GCP prerequisites console. `recorded`: README text for the
    Troubleshooting rows. `expected`: the chat contract's success shape (`docs/contract.md`), never an answer text.

## Not claimed

- **No human listened to this cut** or watched it. The listening gate rests on the series waiver quoted under gate 6,
  and the audio was checked only by machine (the ASR round trip and the onset check, on the round-1 cut). The
  "preflight" vowel and the "No."/"Now" doubt are unresolved by ear.
- **The ASR and pairs checks did not run on the final files.** They ran on the round-1 cut; the fix round changed
  only three scenes' pictures, and the subtitles are identical (writer's comparison), but the audio of the
  re-rendered S05, S14 and S15 was not transcribed again (the loudness of the whole cut was re-measured).
- **The Chinese subtitles were reviewed by agents only:** the QA subtitle watcher, the narration/subtitle fixer, the
  scene verifiers and the pairs check. No human translator or native reviewer read them.
- **No Google Cloud step ran.** The recording had no Google account, project or key: the Vertex AI API, the
  `ml-workflow.json` key and its role, every Gemini and embedding answer (`--chat`, Ask, Cheese books, the 2025
  chat), and what a real key returns (including whether the 2025 branch's retired Gemini model fails as the S15 tag
  says) are drawings, README text or the contract's shape, never observed. The README's "Gemini: 403/404" rows were
  not reproduced; only the rejected-key 500 was.
- **No Docker Hub login or push** is in this lecture; images were pulled anonymously (with rate-limit retries, a
  capture-only detail). **No browser ran:** the pages, the React app, the Recent tab and the CORS behaviour in a real
  browser are inferred from the captured HTML, JSON and headers and drawn as `illustration`. **No Mac, no Windows:**
  the capture laptop was Alpine linux/amd64; the BSD `sed -i ''` chip is described, not captured. The production
  NGINX in a cluster (Lectures 19–22) and Kubernetes probes are described, not run.
- **The visual check sampled one frame every 3 s**, plus targeted frames; motion between samples was checked only by
  `freezedetect`, and round 2's `freezedetect` covered only S05 and S14–S15 (round 1 covered the whole film before the
  fix). The tags check used frames at fixed points of each span, not a continuous scan. The round-2 contact
  sheets were read on the burned copy only; the two part files were measured (probe, decode, loudness, subtitles,
  chapters, frame counts) but not sampled visually on their own.
- **Some QA fixes were verified only on previews** (720p `--at` frames and `--every 2` sheets before the 1080p60
  renders), not one by one on the final cut. This record's writer re-checked only the four musts on final-cut frames
  (`writer/`); the final-cut checks cover the rest only by their own sampling and reading of every cue.
- **Commits outside this clone:** PR #113 (`e867726`) and PR #114 (`9c2ea81`) are stated as the coordinator gave them;
  this record's writer could not resolve either hash locally.
- **Review bots:** no `QA_FOLLOWUPS.md` exists for L18, and nothing in this record checks Bugbot threads on an L18 PR.
- **`README.md` durations and chapters were filled in this pass** from `measured.json` and `chapters*.txt`; its chapter
  summaries were not reviewed by a separate agent.
- **Every check in this record is an agent's.**

## Fix round after the final-cut checks

- **Round 1 findings fixed** (commit `e3390a5`, 2026-11-06 04:07 UTC):
  - S15: `ref` ("slides 24–26") now fades out and back in with the RequestTrace around the c25 terminal, and `ref6`
    ("slide 27") fades with the trace before the c27 terminal instead of at the two-panel.
  - S05: `ref0` ("slides 16–17") fades in with the page outline instead of at the scene start.
  - S14: the "2025 docs:" pill's gap before "(no /api)" widened (`buff` 0.15 → 0.3).
  - S05, S14 and S15 re-rendered at 1080p60 (04:11–04:23, per their logs), the cut re-stitched (04:29) and re-burned (04:54), still
    32:11 (part 1 17:46, part 2 14:25); scene durations and subtitle timings unchanged to the millisecond.
- **Round-2 checks on the new files** (`report-tags.md`, `report-visual.md`, `report-measured.md`): all four items
  verified, no regressions; measured passes (I −16.0 LUFS, TP −2.7 dBFS). The ASR and pairs reports are from round 1:
  the narration and subtitles did not change.
