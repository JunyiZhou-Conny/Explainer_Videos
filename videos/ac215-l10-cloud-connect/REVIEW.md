# Review record: AC215 · Lecture 10 — Connecting to the cloud: one key, three containers, one browser

Follow-along of [dlops-io/cheese-app-v0](https://github.com/dlops-io/cheese-app-v0) `main` @ `cb6fb94` (2026-10-08),
its `README.md` top to bottom (Prerequisites, Build the Vector DB, Run API Service Container, Run Frontend Container,
the five app pages, API Endpoints; the optional LLM RAG tutorial is L05 material and not followed). Claude Code
sessions (Claude) produced it. Verified facts and unclaimed reviews are kept in separate sections.

- **Origin and takeover:** another session built S01–S09 on branch `claude/ac215-l09-l13-batch`. The folder was
  imported into the series branch in `bbdf2ff` (2026-11-02 22:33 UTC) and taken over on 2026-11-02 (issue #47). This
  coordinator built S10–S15 and the Chinese subtitles (`6047069`, `524c67a`, 2026-11-03 01:01–01:36 UTC) and masked
  the instructor's name on screen (`46a1fdc`).
- **Captures:** 2026-10-19 22:11–22:18 UTC and 2026-10-20 01:44–01:49 UTC (`ASSETS.md`), in a fresh Docker Engine
  29.8.2 (`docker:29.8.2-dind`) standing in for a laptop with Docker Desktop, with **no Google credentials**. Every
  step that needs a key is captured up to its documented failure; the success path is tagged `recorded`.
- **QA draft:** the 480p draft (30:22; part 1 ended at 17:34).
- **Whole-video QA (round 1):** `/root/ac215-backup/tasks/l10-qa-w2y5li0uz.output`, key `result`. 37 agents: seven
  watchers, 14 scene fixers (S02–S15), one narration/subtitle fixer and 15 scene verifiers. The fixes were checkpointed
  in `110dc51` (2026-11-03 18:18 UTC). A narration follow-up round followed (`97c5480`, `50e83f9`, 18:21–18:42 UTC):
  see "Still open after QA".
- **Finishing pass:** none. The coordinator's list of finishing-pass outputs for L10 is empty.
- **1080p60 renders:** all 15 scenes. Render logs are `build/logs/`, dated 2026-11-03 22:30–23:33 UTC. None contains
  "anchor not found".
- **Final-cut checks, round 1** (on the first 1080p stitch) found four defects: the S10 README card touching the
  lecture tag, the S12 tag arriving before its map, the S14 terminal covering the map (F7), and bilingual cues 98/99
  swapped. All four were fixed (`2a0aa99`, 22:25 UTC; cues in `4b8cbd6`, `61e1dfd`), re-rendered, re-stitched and
  re-checked.
- **Final cut:** 30:50.6, parts 17:46.8 + 13:04.0. The clean cut and the full-cut subtitles were written at
  2026-11-04 00:11 UTC, the burned copy, chapters and transcript at 00:58, the parts at 01:00–01:01. The text outputs
  (subtitles, `.ass`, chapters, transcript) are committed as of `678618e` (01:02 UTC); the MP4s are not in Git (release
  assets).
- **Final-cut checks, round 2:** five agent checks. The coordinator saved their returned text as
  `build/final-review/report-{tags,asr,visual,pairs,measured}.md`. All five reports exist and were read in full for
  this record. `report-tags.md`, `report-visual.md`, `report-pairs.md` and `report-measured.md` are the re-check of the
  current files (2026-11-04). `report-asr.md` is from round 1 (2026-11-03 22:02), on the first stitch; the narration
  did not change in the fix round, and the English cue numbers and times it cites match the current `.srt` (checked for
  cues 2, 176, 363, 418, 419, 463, 474, 492, 501). None found a blocking defect.

**Conventions:**
- **Times** are mm:ss in the full cut (`output/ac215-l10-cloud-connect.mp4`, 1850.648 s), except in "Whole-video QA",
  which keeps the 480p draft's times (marked *draft*).
- **Cue numbers** name their file: `.srt` (513 cues) or `.zh-en.srt` (511).
- **Evidence paths** are relative to `build/final-review/`, which is git-ignored and exists only in the producing
  session. A successor re-runs the checks to reproduce it.

## Content gates (AGENTS.md)

1. **Hook** ✔. S01 opens on a working app and the questions it hides, not on a value proposition.
   - "Here is a cheese chatbot, running on your laptop." (cue 1, 00:00.0); "Behind that one answer, your browser makes
     three calls." (cue 4, 00:09.8).
   - The two questions: "So who checks that it is really you?" (cue 7, 00:23.8) and "And how does a web page find a
     database inside a container?" (cue 8, 00:26.0).
   - Three riddles (cues 9–12, 00:30.0–00:41.8): the two numbers of `-p 3200:3000`, which machine `localhost:9000` is,
     and where the name `llm-rag-chromadb` gets its address; then "once anything can knock, who is allowed in?"
     (00:48.2).
   - **Payoff:** each riddle is answered on screen: the name at 18:13.7 ("Names work through Docker DNS…") and 19:09.3;
     the tunnel at 21:04.5 ("The flag -p 3200:3000 means host port 3200 forwards to container port 3000."); and
     `localhost:9000` at 22:29.6 ("localhost:9000, never a container name."). "Who is allowed in" closes S12: "An
     unprotected AI endpoint, spending your key, is running on your laptop." (cues 418–419, 25:04.6).
2. **Intuition before formalism, with an animated mechanism for each core idea** ✔. `BRIEF.md` ("Visual set pieces")
   defines six. Each is animated next to the commands it explains:
   - **V1, the auth chain (S06, S07, S09):** it breaks at the first link in S06 ("a bearer token, which needs a key.",
     cue 167, 09:33.0, then the `DefaultCredentialsError`); S07 builds it: the signed JSON Web Token (cue 207, 12:02.5),
     Google's token desk (12:08.6), the bearer header (12:23.2); S09 closes it: "And the whole chain lights up, through
     to a 200." (cue 295, 17:11.5, tagged `recorded`).
   - **V2, the IAM grid (S08, reprise S13):** "a grid of identities, roles, and resources" (cue 232, 13:25.5); three
     request arrows test three cells (13:41.9), one refused with a 403 (13:58.2); S13 re-fires the parked tuned-model
     arrow into the instructor's column (26:28.0).
   - **V3, the secrets portal (S04):** the cursor "climbs up twice and lands on the secrets folder" (cue 94, 05:11.0),
     the tube to `/secrets`; the ponder replay where Docker "silently creates that folder, empty" (06:52.4).
   - **V4, one server, two addresses (S10, S11):** each container's own localhost and Docker DNS as a phone book per
     street (18:13.7); the API cannot resolve the database until `docker network connect` (19:09.3); the
     `3200→3000` door morphing the port number (21:04.5); the port-band number line (21:33.8); `0.0.0.0` twice
     (21:43.9).
   - **V5, the browser as integrator and the CORS bouncer (S01 teaser, S12):** three PINK calls (22:59.1); the
     preflight (23:31.6), Chroma's guest list (23:35.7) and "Your browser is the bouncer" (23:43.3); the `:3300` replay
     after the ponder (24:25.1).
   - **V6, the running map (built S02 from 01:26.7, grows every scene):** complete in S15, "The whole lecture, on one
     map." (cue 491, 29:26.2), then torn down.

   **Lecture slides:** a GREY "Lecture 10 · slides …" tag top right in 13 of the 15 scenes. S09 and S13 have none, as
   `script.md` (line 134) says. The deck is redrawn, never shown.
   - The tags check found no tag overlapping anything and none still on screen 0.5 s after it leaves, in a 5 fps scan
     of the top-right region (9,253 frames) plus frames at each tag's in, mid, pre-out and post points (`tags-final/`).
   - S01's tag is up 00:30.7–00:53.7, S06's ("slide 13") only for the GOLD cost block, 09:12.2–09:26.3, and S12's on
     the closing beat, 24:59.0–25:11.0. Every tag citing several slides reads "slides …".
   - `SLIDES.md` ("This video and the slides", map table) pairs every planned chapter with the deck's slides.
3. **Pause-and-ponder moments and a recap**: ✔ for the ponders, by Conny's decision for the series (accepted item A1);
   ✔ for the recap.
   - **Ponders:** five cards, each followed by a silent timer. Timer starts are from `measured.json` (each scene's
     `events.json` plus its chapter start); the card fades in 0.6 s before the timer; lead-ins and answers are from
     the `.srt`.

     | # | scene | card (condensed) | spoken lead-in | timer | answer starts |
     |---|---|---|---|---|---|
     | 1 | S04 | You save the key inside the repo and run the script from `api-service/`. What is in `/secrets`, and what happens on the first embedding call? | 06:24.4 | 06:40.1, 8 s | 06:48.1 "The cursor still climbs twice, to a folder that does not exist." |
     | 2 | S08 | You paste the instructor's endpoint `projects/129349313346/…`. Which part decides whose IAM is checked: `GCP_PROJECT`, the key's `project_id`, or the path? | 14:37.5 | 14:55.5, 8 s | 15:03.5 "The path." |
     | 3 | S10 | You want the API itself to query Chroma. What URL does it use, and what must change on the map for that name to resolve? | 18:50.3 | 19:01.3, 8 s | 19:09.3 "Put the database on the API's street as well," |
     | 4 | S12 | You republish the frontend at `-p 3300:3000` and ask a question. Which of the three calls fails, and does curl care? | 24:08.2 | 24:17.1, 8 s | 24:25.1 "Call one works: the API allows any origin." |
     | 5 | S14 | After `docker compose down`, are your embeddings gone? What would make them gone? | 27:37.3 | 27:44.7, 6 s | 27:50.7 "No. An extra listing shows the database file still on disk," |

   - **Rate:** 5 cards in 30:50, one every 6.2 min, against AGENTS.md's aim of one every 2 minutes (about 15). The first
     comes at 06:40, the longest gap is 06:40–14:55 (8:15), and the last is 3:06 before the end. `BRIEF.md` ("Ponder
     questions (summary)") plans exactly five.
   - **Decided by Conny (2026-10-21), as recorded in `videos/ac215-l05-rag/REVIEW.md` gate 3:**
     「我觉得可以保留现在的密度」: keep the current density of 3–5 ponders per lecture.
   - **Recap:** S15 from 28:57.5 (113.1 s).
     - 28:57.5–29:26.2: the teardown (compose down, the shared network) and key hygiene (29:06.8–29:26.2).
     - 29:26.2–29:56.3: a spoken summary on the complete map, one sentence per idea: the badge and the one-hour ticket,
       the IAM cell, the mount to `/secrets`, names versus localhost, the `3200 to 3000` doors facing the Wi-Fi, the
       three calls past the CORS bouncer, the vectors in a mounted folder (cues 491–498).
     - 29:56.3–30:14.7: "When something breaks, find its layer." (credentials error, 401, 403, CORS, a taken port,
       line 14; cues 499–505).
     - 30:14.7–30:39.8: "5 questions to test yourself." (cues 506–511). "Answers are in the exercises" (cue 512): the
       episode folder has no `exercises.md` (see "Open nits"); the study guide's §8 Q1–Q5 are the same five questions
       with answers.
4. **Narration written for the ear, with word-anchored cues** ✔.
   - **Spoken style:** follows `script.md`'s conventions: flags and paths are said in words ("The flag dash p, 3200
     colon 3000", "slash secrets"), with the literal form in the subtitle's `en_display`; versions and counts take "at
     the time of recording"; no project number is spoken (0 matches of `129349313346` in all nine `.srt` files).
   - **Size:** 90 SAY lines, 4,367 words (`measured.json` "narration"), matching the 90 narration blocks in the scenes'
     `subs.json`. Kokoro `af_heart` at speed 0.9 gives 141.6 wpm over the runtime and 150.4 wpm over the 1,741.8 s of
     voice (94.1 % of the runtime).
   - **Anchors:** 635 `vo.wait_until(...)` calls across the 15 scenes (S01–S15: 26, 40, 50, 42, 43, 50, 42, 43, 57, 34,
     52, 57, 34, 36, 29). None of the 15 render logs contains "anchor not found".
   - **Pronunciation:** the QA ASR watcher's one item, "aarch64" (*draft* 08:06), is covered by an L10-only lexicon
     key, `"says aarch64."` in `explainer/lexicon.yaml`, so L11's bare "aarch64" is unchanged. The verifier checked the
     key in code, not by ear.
   - **Final ASR** (`report-asr.md`): no mispronunciation or swallowed word that needs a fix. No cue's speech starts
     more than 1 s late (`late-onsets.json`, the list of such cues, is empty); the latest is cue 176 at 10:04, 0.55 s
     late (`report-asr.md`, from `silence.log`). Two low-severity notes: under "Open nits".
5. **Simulated-target-viewer QA over the full draft** ✔.
   - Seven watchers reviewed the 480p draft: two directors and two simulated target viewers ("newcomer"), one of each
     per part; a subtitle watcher, a follow-ups watcher and an ASR watcher. They worked from contact sheets, exact
     frames pulled from the draft, the English `.srt`, the README and the captures.
   - **52 timestamped findings: 1 must, 29 should, 22 nit.** The must was fixed and verified. Each scene's fixes were
     checked by a skeptical verifier on fresh preview or 720p frames; three verifiers found and fixed a new problem
     each. What stayed open is listed under "Whole-video QA".
6. **Measured checks** ✔. The numbers are under "Verified" (`measured.json`, measured on the final files).
   - **Duration:** 30:50.6 (1850.648 s), inside the series' 25–35 min. The parts are 17:46.8 (1066.804 s) and 13:04.0
     (783.952 s). Their container durations sum to 0.108 s more than the full cut (within ±0.5 s), and their frame
     counts sum to the clean cut's exactly (64,004 + 47,033 = 111,037).
   - **Loudness:** −16.1 LUFS integrated in all four files, LRA 2.1–2.2 LU, true peak −2.5 to −2.7 dBTP. That meets the
     toolkit's −16 LUFS target with peaks below −1.5 dBTP.
   - **Caption bounds** (`report-visual.md`, `report-pairs.md`): every one of the 511 events in `.zh-en.ass` is exactly
     two lines, Chinese above English (`\fs33`), with wrapping off (`WrapStyle: 2`). The widest lines are 1,493 px
     Chinese (`.zh-en.srt` cue 142, 08:19.9) and the full service-account email in English (`.zh-en.srt` cue 56,
     03:12.8: 1,469 px in the visual check, 1,502 px in the pairs check), against 1,840 px available. In the burned copy the subtitles sit at
     y≈990–1062 and, at 11 spot checks with a terminal or command on screen, the content ends at y≈880 or higher, so no
     command a viewer must copy is covered.
   - **Music balance:** does not apply. L10, like L02–L09, has no score: `video.yaml` has no `music:` key.
   - **Subtitle sync:** by silence detection on the round-1 stitch (`silence.log`, -40 dB, 0.12 s), no cue's speech
     starts more than 1 s after the cue (`late-onsets.json`, the list of such cues, is empty); the latest are cues 176
     (0.55 s), 291 (0.50 s), 257 (0.47 s) and 304 (0.44 s) (`report-asr.md`). The verifier re-ran the same silencedetect
     on the current clean cut: all 1,688 silence boundaries equal `silence.log`'s, and the same four lags follow from
     the current `.srt` (`verify/silence-now.log`, `verify/onset.py`). Speech starting before its cue was not measured.

   **Human review:** the series waiver stands in for a listening sign-off.

   Listening sign-off: waived by Conny for the AC215 series (Explainer_Videos#29, 2026-10-15): 「不需要，我现在对视频质量很满意的」 — no human listened to this cut; the ASR round trip below is the substitute.
   Review moments optional since 2026-10-22 (AGENTS.md): 「我大概率是不会进行审片的，因为我觉得做得已经非常好了，就让bugbot来检查就好了」

   **ASR round trip** (`report-asr.md`):
   - faster-whisper base.en over the whole clean cut: 513 cues compared, 199 with some difference (`asr.json`,
     `asr.log`).
   - large-v3-turbo on 29 doubtful cues, one clip per cue (`asr-large-doubtful.json`). Every cue base.en heard as
     empty is present: cue 363 (21:23), cues 418–419 (25:04–25:06), cue 501 (30:01), and cue 502 (30:04) with its
     "role". Base-model misses such as "idea" for "The ID" (cue 158) and "builds" for "bills" (cue 163) read correctly.
   - What remains is recogniser noise: digits versus words, split compounds ("local host", "front end"), words it
     cannot know (pipenv, uvicorn_server, aarch64, splitext, DefaultCredentialsError), homophones (buy/by, role/roll,
     CORS/cores), and words moved across cue boundaries.
   - The voice shortens two on-screen strings on purpose: the service-account email (cue 58, 03:12) and
     `Local: http://localhost:3000` (cue 349, 20:29).

## Whole-video QA (480p draft, 30:22, 2026-11-03; times are *draft* times)

**Watchers and findings** (`l10-qa-w2y5li0uz.output`, key `result`; the run log reads "L10: 52 issues from 7/7
watchers"):

| watcher | must | should | nit |
|---|---|---|---|
| director, part 1 | 0 | 3 | 7 |
| newcomer, part 1 | 1 | 7 | 6 |
| director, part 2 | 0 | 6 | 3 |
| newcomer, part 2 | 0 | 7 | 3 |
| subtitles | 0 | 6 | 2 |
| follow-ups | 0 | 0 | 0 |
| ASR | 0 | 0 | 1 |
| **total** | **1** | **29** | **22** |

- **By target:** 36 scene, 9 subtitles, 7 narration.
- **By kind:** 14 follow-along, 9 text, 9 subtitle, 5 picture, 5 pacing, 4 continuity, 3 fact, 2 narration,
  1 lexicon.
- **Facts:** both directors checked the facts against the captures and digest (commit, Docker 29.8.2, chunk counts,
  `"1.0.0"`, 170 pinned packages, 773 npm packages, Next.js 14.2.4, the CORS guest list, `MAX_AGENT_STEPS` 5) and found
  them right; both report the instructor's name masked everywhere they looked.
- **Follow-ups watcher:** found no `QA_FOLLOWUPS.md` (there is still none for L10). Instead it read the 11 Cursor
  Bugbot threads on L10 files in PR #50 (`claude/ac215-l09-l13-batch`) and checked each against the code and the draft.
  All 11 were already fixed or did not reproduce; the S09 double-fade thread was the only one still unresolved on
  GitHub at the time, with no reply. It reported no issue.
- **ASR watcher:** 506 cues on the draft, 209 with a difference under base.en, all ASR noise after a large-v3-turbo
  re-run of 31 spans; one nit ("aarch64", see gate 4).

**The must, and how it was fixed.**
- **M1, *draft* 15:51, S09: the "your new line 14" fix drawn as three bare lines** (newcomer part 1). Copied as shown
  into `docker-shell.sh`, it would have become a shell syntax error.
  - **Fix** (`s09_api.py`): one fold with a real continuation, `docker network inspect cheese-app-network >/dev/null
    2>&1 \` then `    || docker network create cheese-app-network`, asserted to rejoin to the captured line (which equals
    README.md line 74), with a grey note "README.md line 74 has it on one line". The verifier confirmed it on fresh
    frames.

**The shoulds, examples by kind** (fixed and verified, except those under "Still open"):
- **Follow-along (commands unreadable or gone too soon):** S05's `ls -la /secrets` now shows with its key-file row;
  S10's `docker network inspect` held about 3 s, and the `docker exec` probes folded at spaces into a 6-row strip so
  the prompt row stays; S12's step-1 `curl` in a 6-row strip (about 2.9 s readable, was under 1 s); S14's
  `ls -la docker-volumes/chromadb` in a 5-row strip; S11's ringed `docker ps` cell held 1.5 s; S03's gcloud card up
  about 11 s.
- **Text:** S07's ADC one-liner and the S05/S09 `sed` lines now break at spaces, never mid-word; S11's README 177 card
  no longer prints raw Markdown; S15's key-hygiene card stays at full contrast.
- **Pictures:** S09's Swagger page fits its window (4 rows); S11's 0.0.0.0 beat now pairs the API house with its own
  `0.0.0.0:9000->9000/tcp` cell from capture 39; S11's `127.0.0.1:` caption sits left of its chip; S13's orphan caption
  joins the 403 picture.
- **Facts and narration:** S01 "follows the README in six stages, from setup to shutdown" (the README has 11 sections);
  S12 adds "Even 127.0.0.1, port 3200, is a different origin from localhost 3200, so open the app at localhost."
  (24:42.3 in the final cut); S13's 403 is hedged, "so expect a 403, or a not-found error" (26:28.0), with grey
  `expected` tags and a pointer to the study guide's base URL note.
- **Continuity:** S14's map after the restart shows the Chroma house, street and folder; S15's README tracker leaves at
  the start of the recap.
- **Subtitles:** six zh pairing rewrites (S01, S06, S08, S09, S14, S15), the S11 zh line now copies
  `Local: http://localhost:3000` verbatim, and S10's English line gets the captured `Name or service not known`; the
  final pairs check confirms the result.

**New problems the verifiers found and fixed:** S05, the `sed` command scrolled away before "Pause and edit it" (strip
grown to 8 rows); S10, the red cross of the localhost probe sat on the green `secrets/` tube (moved left); S13, the
new 404 highlight filled the README 249 card solid yellow and pointed at the wrong card (replaced by a ring on
`genai.Client` at rag.py line 111 and a grey note). The S01 verifier also added the hold on the "Shut down" tracker that
the fix asked for, and the S12 verifier broke a 7.4 s still stretch.

**Nits:** fixed, except those listed next. Examples: S06's "≈ 7 M characters embedded" on screen, S04's `mv` template
row, S08's `--project=your-gcp-project` and the four-dot ellipsis, S12's "ours: empty (no key in our capture)", S10's
capitalised "Name or service not known".

**Still open after QA, and why:**
- **Closed by the narration follow-up round** (after the QA run): the S06 sentence "If instead you see a 403 saying
  the API is disabled, enable the Vertex AI API; the IAM scene shows the command." (cue 175, 09:57.5); S07's "So what
  failed? The loader's Google client, like the API's, …" (cue 195, 11:15.5); the S01 glossary entries for "six stages"; the S08
  SHOW text; and the S11 caption timing.
- **S13 "one agent question costs one embedding"** (cue at 25:37.6) is kept by coordinator decision: both agent tools
  require `search_content`, so every agent question makes exactly one embedding (`agent_tools.py:15–17`,
  `rag.py:160–163`). The newcomer's premise (no embedding for `get_book_by_author`) does not hold.
- **No sixth ponder in S06** (newcomer part 1, should): it falls mid-sentence and needs a `script.md` split; the
  density is Conny's decision (accepted item A1).
- **S13 "Its neighbor, the agent tools file, is not watched"** (26:07.3, nit): `agent_tools.py` sits two folders up
  from `api/routers/rag.py`, not beside it. The instruction itself (restart for that file) is right; the wording needs
  `script.md`, i18n and an anchor change.
- **S03 narration reads the email short**, "llm-service-account, at your project" (03:12, nit): kept for the ear; the
  subtitle shows the badge's full address.
- **S12's step-1 command leaves at "Step 2"**, before "Pause and try both." (22:44.8): the chromaui browser fills the
  frame, so there is no room to keep it.
- **S03's gcloud card is a sketch** (`--member=serviceAccount:… --role=roles/aiplatform.user`), titled "sketch · repeat
  for roles/storage.admin · full text: study guide": the full flag is wider than the frame. The study guide has both
  bindings in full.
- **S02's `▶ your turn`** sits beside the `Cloning into…` output row, not the command: next to the command it would
  leave the frame; `SCENE-NOTES.md` allows it.
- **Small leftovers seen by verifiers on previews:** in S10, after the `docker network connect` probe only the tail of
  that command stays in the top row, and the red ring covers "Name or service" of the wrapped error; in S06 the "≈" line
  starts about 15 px right of the warning line.
- **Toolkit:** the S10 fixer reports that `Terminal.fold` in `explainer/devops.py` drops a character on a hard break
  and can put ` \` inside quotes; S05, S07, S09, S10 and S12 carry local folding helpers. Fixing it belongs in a later
  toolkit PR (AGENTS.md split).

## Final-cut checks (1080p60, 2026-11-04)

- **Tags** (`report-tags.md`): no blocking defect. All 13 tags, all four round-1 bot items verified on new frames:
  the S10 README card sits 18 px below the tag (19:35–19:52), the S12 tag fades in with the map after the wireframe
  (24:59.0), the S14 terminal covers no part of the map (27:52–27:57), and cues 98/99 pair correctly in the `.zh-en.srt` and
  in the burned frames (05:37.7–05:44.0). Two documentation notes: under "Open nits".
- **ASR** (`report-asr.md`, round 1): intelligible throughout; two low-severity notes.
- **Visual** (`report-visual.md`), on the burned copy:
  - 39 contact sheets (one frame every 3 s, 0:00–30:48), all read, plus full-size frames of every suspect spot.
  - All 15 scenes present; no black stretch over 0.6 s apart from one beat transition; the video fades in from black
    and out to black at 30:49–30:50.6; the part seam at about 17:45 is a fade.
  - No garbled glyphs; no tag left on screen; F7 fixed. F1–F6 remain, all cosmetic (accepted item A2); long still
    frames, one near-empty frame and wrapped commands are under "Open nits".
- **Pairs** (`report-pairs.md`): all 511 cues of `.zh-en.srt` re-read. Cues 98/99 fixed; no meaning swap and no
  clause-order failure anywhere; the `.ass` text equals the `.srt`; the part files join to the full file cue for cue.
  Four small pairing items remain (accepted item A3); cue 324 is informational.
- **Measured** (`report-measured.md`, `measured.json`): all four MP4s decode with 0 errors. Formats, loudness,
  subtitles, chapters and the part split pass. The ponder shortfall is decided under gate 3.

## Accepted items (coordinator decisions)

- **A1. Five ponder moments in 30:50**, below AGENTS.md's one per 2 minutes. Accepted under Conny's 2026-10-21 decision
  to keep 3–5 per lecture (「我觉得可以保留现在的密度」); see gate 3.
- **A2. Cosmetic visual items F1–F6** (`report-visual.md`, evidence in `vis2/`). None hides text a viewer must read or
  copy; each fix would need a scene or shared map change and a re-render.
  - F1, 05:26 (S04): the pink arrow now starts just right of the final "n" of `/secrets/llm-service-account.json`, a
    few pixels away (it used to cross it).
  - F2, every map 00:30–29:50: the Google building's roof line runs through the "🔒IAM" label. The label stays legible.
  - F3, 07:29.5 (S05): for about 1 s the semi-transparent "inspect … || create" card passes over the `docker network ls`
    terminal on its way to its slot.
  - F4, 08:09–08:20 (S05): the `x86_64` and `Python 3.12.15` highlight boxes touch the tops of the next line.
  - F5, every map with the pill (07:12, 08:15, 11:00, 27:53, 29:30): the green `secrets/` pill is narrow; its outline
    clips the leading "s". The folder-tree view (05:45) fits.
  - F6, 18:15–19:33 (S10): the pink phone-book cards hide the 8000 and 9000 doors and touch the browser icon. The QA
    director noted the doors are faded on purpose during the DNS beat.
- **A3. Minor subtitle pairing items** (`report-pairs.md`, `.zh-en.srt`); no meaning swap in any:
  - 148/149 (08:41.8–08:46.7) and 202/203 (12:02.5–12:08.4): the zh sentence is split and the English is not, so the
    same English line shows twice.
  - 320/321 (19:09.3–19:17.7): "with an extra (command)" is in cue 320's Chinese but cue 321's English.
  - 329/330 (19:38.0–19:45.3): the English is cut inside "docs path" and the Chinese elsewhere.
  - Cue 324 (19:24.5) shows "Connection refused" on both lines: verbatim terminal text by glossary rule A1
    (`i18n/zh/glossary.yaml:420–423`).
- **A4. The real project number `129349313346`** appears only inside quoted repo code and RED story beats, a script
  decision: the IAM grid's third column and the parked tuned-model path `projects/129349313346/…` under it (S08,
  reprise S13), the S08 ponder card and the `rag.py` line 22 panel in S13. It is never spoken and in no subtitle file. The project ID on screen is
  `your-gcp-project`; the repo's default `ac215-project` appears likewise in quoted code and the grid.
- **A5. The instructor's name is masked as ‹instructor›** everywhere on screen and in subtitles (series rule). The
  visual check found the mask at 10:51 (chunk text), 25:13 (agent prompt), 25:33 (`‹instructor›_fun_fact_tool`), 25:48
  (JSX) and in the step-5 tracker, and a case-insensitive grep of every file in `output/` found no name.

## Open nits (not ruled on one by one; left for the coordinator)

None blocks release. Each needs a narration, yaml, `script.md` or scene change and a rebuild, which this record does
not make.
- **ASR, cue 2 "Tolminc"** (00:03; also cues 159 and 189, 09:06 and 10:49): both models hear "Tolman's"; Kokoro
  probably says "TOL-mink". The subtitle spells it right. A phonetic respelling in the narration would fix it.
- **ASR, cue 463 "No. An extra listing…"** (27:50.7): after the ponder's silence the "No." runs into "An", and both
  models hear "Now". A slightly longer pause after "No." would remove the doubt.
- **Long still frames with narration** (`sheets/freeze_summary.txt`): 45 stretches of at least 4 s, 224.2 s in all,
  the longest 01:32.1 (8.4 s), 06:32.0 (7.7 s, S04 ponder setup), 05:45.7 (7.1 s) and 21:11.6 (7.0 s). The visual check
  calls none a stall.
- **Near-empty frame, 29:56.7–29:59.0 (S15):** the map fades out and only the faint "error / its layer" headers stay
  until the first row appears; the subtitle is on screen throughout.
- **Wrapped commands look like real newlines** (F9): long one-line commands wrap in the terminal with no continuation
  marker, e.g. the `sed -i` edits at 07:39–07:44 and 15:30, the line-14 `sed` at 16:03, `localhost:` / `9000/openapi.json`
  at 17:27, and the chroma listing at 23:54–24:03. The study guide has the exact text.
- **Tag documentation:** `script.md:224–225` says S01's tag stays "to the end of the scene", and `script.md:820` says
  S12's tag is "during this block"; the code follows the rules (fade at 00:53.7; on the closing beat).
- **`script.md` SHOW lines lag the scenes:** S11's 0.0.0.0 beat still names the `0.0.0.0:3200->3000/tcp` cell
  (line 737; the scene shows `9000->9000`); S12's caption still reads "ours: empty" (line 764); line 128 says "There are
  no `expected` panels in this episode", while S13 now carries grey `expected` tags.
- **i18n notes:** `i18n/zh/GLOSSARY.md` lines 81 and 300 still give the D4 form `llm-service-account@your-project`
  (the yaml and the subtitle use the full address); `glossary.yaml:286` (`first_use`) quotes the old S06 zh sentence.
  Neither affects the subtitles.
- **`SLIDES.md` "This video and the slides"** still opens "The video is not scripted yet"; its map is from the digest's
  planned chapters.
- **No `exercises.md`** in the episode folder (L01–L09 have one). The recap says "Answers are in the exercises"
  (cue 512, 30:39.8); the study guide's §8 Q1–Q5 hold the same five questions with answers, and the new README points
  there. The ponders have no answer file in the episode folder; the study guide's §8 answers ponders 2 and 5 as Q7 and
  Q6, takes up ponders 4 and 3 as exercises E1 and E5, and covers ponder 1's key-inside-the-repo case in §6.
- **No `README.md` existed** before this pass; it was written now from `video.yaml`, `BRIEF.md`, `ASSETS.md`, the
  transcript and the chapter files (see "Not claimed").
- **Chapters:** S14's listed 26:59 is 0.01 s after its computed start (1618.990 s); every other entry is rounded down.
  Harmless.

## Verified (final render)

All numbers are from `measured.json` and the five reports, on the files in `output/` as they are now (written
2026-11-04 00:11–01:01 UTC). An adversarial verifier then re-measured independently (`verify/`): ffprobe durations,
frame counts and sizes of the four MP4s; ebur128 on the clean cut (−16.1 LUFS, 2.2 LU, −2.5 dBTP) and part 2 (−16.1,
2.1, −2.5); cue counts, numbering, overlaps, the 1 s minimum and the last cue end in all nine `.srt` files; the
chapter starts against the scene renders; and the five ponder cards on frames at their timers. All matched.

- **Files:** H.264 High, yuv420p, 1920×1080 at 60 fps, AAC LC 48 kHz stereo at about 178 kb/s, video at about
  270 kb/s. Each decodes in full with `ffmpeg -v error -f null` with exit 0 and no error lines (each
  `measured/decode_*.log` holds only its `exit=0 secs=…` line).

  | file | duration | video frames | size (bytes) | loudness | LRA | true peak |
  |---|---|---|---|---|---|---|
  | `ac215-l10-cloud-connect.mp4` | 1850.648 s (30:50.6) | 111,037 | 106,803,374 | −16.1 LUFS | 2.2 LU | −2.5 dBTP |
  | `ac215-l10-cloud-connect.zh-en.mp4` | 1850.648 s | 111,038 | 105,730,115 | −16.1 | 2.2 | −2.5 |
  | `ac215-l10-cloud-connect_part1.mp4` | 1066.804 s (17:46.8) | 64,004 | 60,682,780 | −16.1 | 2.2 | −2.7 |
  | `ac215-l10-cloud-connect_part2.mp4` | 783.952 s (13:04.0) | 47,033 | 46,125,907 | −16.1 | 2.1 | −2.5 |

  The zh-en video stream is one frame longer than the clean cut's; the containers are equal. The 15 scene renders sum
  to 1850.604 s.
- **Subtitles:** `.srt` 513 cues, `.zh.srt` 443, `.zh-en.srt` 511. The parts have 304 / 259 / 299 and 209 / 184 / 212,
  which sum exactly to the full files.
  - In every file the cues are numbered 1..N and in order, inside the runtime, at least 1.000 s long, with no
    overlaps; every `.zh-en.srt` cue has two lines.
  - The last cue ends at 1848.973 s (parts: 1064.497 and 782.240 s), 1.7 s before the cut ends.
  - The `.zh.srt` merges cues by design, so its times do not line up one-to-one with the `.srt`.
- **Chapters:** 15 entries, titles equal to `video.yaml`'s in order. Each start is within 0.973 s early to 0.01 s late
  of the running total of the scene renders (S10 at 1066.725 s = 17:46, S15 at 1737.523 s = 28:57).
  `chapters_part1.txt` (9 entries) and `chapters_part2.txt` (6, at 00:00, 02:06, 04:36, 07:24, 09:12, 11:10) match.
  `README.md` now carries these.
- **Scenes:** all 15 present; the chapter starts match the scene durations, so no scene is missing or doubled.
- **Narration:** 90 SAY lines, 4,367 words, 150.4 wpm over 1,741.8 s of voice; 635 anchors; no "anchor not found" in
  the 15 render logs.
- **Lecture tags:** 13, each found, none overlapping, none on past its scene (`tags-final/`).
- **Privacy:**
  - The instructor appears only as "the instructor" (spoken at 14:41.2 and 26:24.2) and as the ‹instructor› mask on
    screen (A5).
  - The project number is never spoken or subtitled (A4).
  - The key in the folder listings is an obviously invalid stand-in (`ASSETS.md`, "Capture-only deviations"), and
    S05 says so ("One honest note about this recording.", cue 147, 08:26.7).
- **Provenance** (`ASSETS.md`):
  - Terminal lines come from the 2026-10-19/20 captures in `assets/terminal/`; each README command ran exactly as
    written, in README order, with extras tagged `extra`.
  - Every success that needs a Google credential (the embed/load checkpoints, the `/rag/embedding` 200 with 256
    numbers, the populated Chroma UI) is tagged `recorded` with its source; no chat, agent or tuned-model answer text
    is shown, because none is documented.
  - The GCP console and the browser pages are drawings tagged `illustration`.
  - Code panels quote `assets/source/` at the pinned commits.

## Not claimed

- **No human listened to this cut** or watched it. The listening gate rests on the series waiver quoted under gate 6,
  and the audio was checked only by machine (the ASR round trip, run on the round-1 stitch). The two ASR notes are
  unresolved by ear.
- **The Chinese subtitles were reviewed by agents only:** the QA subtitle watcher, the text fixer, the scene verifiers
  and the final pairs check. No human translator or native reviewer read them.
- **No Google Cloud step ran.** The recording had no credentials, so the console steps (service account, roles, key),
  every Vertex AI call (embed, chat, agent, tuned model), `gcloud services enable aiplatform.googleapis.com` and the
  GCS bucket material are drawings, `recorded` sources or narration. In particular:
  - the 403 for an un-enabled Vertex AI API (S06, S08) and the `/finetunechat` 403 or not-found (S13) were never
    observed; the video says "expect" and tags the 403 `expected`;
  - the IAM grid's 403 for the unedited default project is the digest's reasoning, not a capture;
  - the gcloud card in S03 is a sketch and was not run.
- **No Docker Desktop and no Mac run.** The laptop was Docker Engine 29.8.2 (dind) on linux/amd64; the Mac
  `GOOGLE_APPLICATION_CREDENTIALS` mix-up and the "aarch64" line are explained, not run on Apple Silicon.
- **The visual check sampled one frame every 3 s**, plus targeted frames. Motion between samples was checked only by
  `freezedetect`, whose threshold can miss small motion, and by the tags check's 5 fps scan of the tag region.
- **Some QA leftovers were seen only on previews**, not re-checked one by one on the final cut (e.g. S10's command
  tail, S06's "≈" offset). The QA fixes were verified by agents on preview or 720p renders before the 1080p60 renders,
  and the final-cut checks cover them only by their own sampling.
- **No check in this record looked for credentials on screen**; `ASSETS.md` says the private-key field is never
  rendered as a plausible key.
- **Name search:** the visual check grepped every file in `output/` (a grep finds text in the subtitle, chapter and
  transcript files, not in burned-in pixels); on screen, the mask rests on the masking code
  (`scenes/common.py:142–146`) and the visual check's sampled frames, not on reading every frame. The measured check
  did not search for names.
  `video.yaml`'s Bilibili description credits the course staff by name, as L02–L09 do; that text is not on screen.
- **Review bots:** the QA follow-ups watcher read the 11 Bugbot threads on L10 files in PR #50. Nothing in this record
  checks for bot comments posted later. No `QA_FOLLOWUPS.md` exists for L10.
- **`README.md` was written in this pass** from the episode's own files; its chapter summaries were not reviewed by a
  separate agent.
- **Every check in this record is an agent's.**
