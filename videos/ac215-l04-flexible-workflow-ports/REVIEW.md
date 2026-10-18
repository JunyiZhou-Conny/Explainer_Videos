# Review record: AC215 · Lecture 4 — Containers II-b: build or pull, ports and Compose

Follow-along of two tutorials: [dlops-io/mega-pipeline](https://github.com/dlops-io/mega-pipeline),
branch `flexible-workflow` @ `cc67f3b` (part 1, S01–S09), and
[dlops-io/port_toy](https://github.com/dlops-io/port_toy), `main` @ `d190c71` (part 2, S10–S16).
The issue of record is Explainer_Videos#37. The work is in the series draft PR Explainer_Videos#29
(branch `claude/mlops-learning-videos-7b5use`). Claude Code cloud sessions (Claude) produced it:

- **Captures:** 2026-10-14, 00:29–00:40 UTC (`ASSETS.md`).
- **QA draft:** the 480p draft was stitched on 2026-10-17 (01:53 UTC; the QA copy in `build/qa/`
  was set up at 02:11) and runs 31:29.1 (`build/qa/scenes.json`, 1889.14 s).
- **Whole-video QA:** seven watchers, then one fixer for each of the 14 scenes with findings, one
  narration/subtitle fixer and one verifier per fixed scene (36 agents). Its output (`wjgb45ot6`)
  is dated 2026-10-18 04:21 UTC.
- **Finishing pass:** 2026-10-18, about 05:30–10:20 UTC (see "Finishing pass").
- **Re-render after a container restart:** S03, S15 and S16 were re-rendered at 1080p60. S03 was
  re-rendered only for its skip chip, 5:09 → 5:10 (`fd9ffe0`). The latest scene render is from
  12:05 UTC.
- **Final cut:** stitched with `--no-render --crf 27 --burn` on 2026-10-18: the clean cut at 12:26,
  the zh-en copy at 12:48 and the parts at 12:50–12:51 UTC.
- **Final-cut checks:** five agent checks, 12:55–13:45 UTC (`measured.json` written 13:41 UTC).
- **Verifier pass on this record:** about 14:15–14:35 UTC. An agent re-measured the deliverables
  (ffprobe, audio MD5, ebur128 and a full decode of the zh-en copy, cue counts, chapter starts,
  SAY and anchor counts, ponder windows), re-read the QA and finishing-pass outputs, pulled new
  frames and corrected this record (evidence in `build/final-review/verifier/`).
- **Publish block:** `video.yaml` gained its `publish:` block at 14:37 UTC (`f13ae03`).
- **Fix round 1 (`w0g41hm1o`, 14:38–15:31 UTC, `3821b69`):** a text agent reordered eight Chinese
  sentences (A1–A3, B1–B5), split S13's two address sentences (T9) and synced the docs (T10, D1–D3);
  scene agents fixed S06's pill, S10's "9100" labels and S13's anchors and still stretch, each
  followed by a verifier on fresh 720p frames (items in `/root/ac215-backup/args/l04-fix1.json`).
- **Re-render and re-stitch:** S10, S06 and S13 were re-rendered at 1080p60 (15:36, 15:39 and 15:42
  UTC; S13 re-voiced). The cut was re-stitched with the chapter rounding fix (`23b0407`): the clean
  cut and subtitles at 15:48, the zh-en copy at 16:10 and the parts at 16:12–16:13 UTC. The new
  subtitle, chapter and transcript files are in `de06df0`.
- **Re-checks of the re-stitched cut:** 16:14–16:45 UTC, two agents (evidence in `build/recheck/`).
  One read frames, audio and subtitle files of the changed scenes and items (see "Re-check after fix
  round 1"). The other re-measured all four deliverables, their subtitles and chapters
  (`recheck/measured.json`, written 16:26 UTC).
- **Record update:** about 16:48–16:58 UTC (file times in `recheck/record/`; `README.md` written at
  16:53, this record at 16:58). This record took the re-measured numbers, and
  `README.md`'s chapter list and durations were brought in line with the re-stitch (F10). Small
  checks were added for it (`recheck/record/`): the part files' frames at the three fixed moments,
  the audio envelope outside S13 against the final review's, the cues around the five ponder
  timers, and one more frame of S13 (23:13.55).
- **Verifier pass on the update:** from 17:00 UTC. An agent re-measured the four deliverables
  (ffprobe, ebur128 with true peak, audio MD5), the cue counts, cue shifts, ponder windows and all
  32 chapter lines, re-ran the audio envelope comparison and the S13 speech onsets on a full decode,
  pulled new frames for the visual claims and corrected this record (evidence in
  `build/recheck/adversarial/`). Its main correction: the re-check's S13 onsets were 0.14 s too
  small (F2).

This record was written on 2026-10-18 and updated after fix round 1. It is based on those checks'
reports (`build/final-review/report-*.md`), `measured.json` (final review) and `recheck/measured.json`
(re-stitch), the QA and finishing-pass outputs, the fix round's reports (`w0g41hm1o`), `script.md`,
`BRIEF.md`, `ASSETS.md` and `SLIDES.md`. Verified facts and unclaimed reviews are kept in separate
sections.

**Conventions in this record:**
- **Times** are mm:ss in the full video (`output/ac215-l04-flexible-workflow-ports.mp4`, 32:09.8 at
  the 12:26 stitch, 32:10.0 after the re-stitch), except where marked *draft*. Draft times refer
  to the 480p QA draft. Later fixes made the video 40.7 s longer, and scene starts moved by up to
  39.5 s (S16 started at draft 29:20 and starts at 29:59.5 in the final cut). So a draft time can
  be up to about 40 s earlier than the same moment in the final cut.
- **Re-stitch shift:** the re-stitch made S13 0.2 s longer (155.05 → 155.25 s). Times before S13
  (22:56.75) are unchanged. Inside S13, moments between its two re-voiced sentences moved by up to
  −0.05 s, and from "Remove it." (23:48) on they are about 0.2 s later. Times from S14 on (25:32 and
  later) quoted from the 12:26 stitch are 0.2 s earlier than in the re-stitched cut. "Fixed after
  the final review", "Verified (final render)" and "Re-check after fix round 1" give re-stitched
  times.
- **Cue numbers** say which file they come from: `.srt` (531 cues) or `.zh-en.srt` (554 cues) of the
  12:26 stitch. The re-stitched files have 533 and 553 cues, and some numbers moved; where an old
  number is still cited, its new number follows in brackets.
- **Evidence paths** are relative to `build/final-review/`; paths that start with `recheck/` are
  relative to `build/` (the re-check after fix round 1). Both folders are git-ignored and exist
  only in the producing session, so a successor has to re-run the checks to reproduce the evidence.

## Content gates (AGENTS.md)

1. **Hook** ✔. S01 opens on something broken, not a value proposition.
   - On a laptop that never built `generate_text`, `./docker-shell.sh run` pulls an image whose
     Python says 3.8.17 and whose Gemini library won't import (00:00–00:15). The repo's Dockerfile
     says 3.14, so the narration asks "Where did it come from?" (00:25.0).
   - A second surprise comes from the other tutorial: the laptop can't reach a server on port 9200,
     but another container that asks for it by name gets "ok".
   - "Two puzzles" (00:38.8–00:46.6) gives one question to each part. Where did that image come
     from? S08 pays this off: its ponder at 15:07.6 asks which Python a teammate gets. Whose
     localhost is it? S13 pays this off with its "puzzle 2" tick at 24:38.9.
2. **Intuition before formalism, with an animated mechanism for each core idea** ✔.
   BRIEF.md ("Visual set pieces") defines eight set pieces. script.md's SHOW lines place each one
   before the commands it explains:
   - **V1, recipe card or frozen meal (build or pull).** A tag is a signpost that points at a box,
     not at your commit. It appears as the S01 teaser and in S02 (01:31). The payoff is in S08
     (from 14:06): at 15:52 an extra inspect opens the box on 2025-02-18, Python 3.8.17, pipenv
     and root.
   - **V2, three piles at a branch switch.** The piles are tracked, untracked and ignored.
     `git checkout` hits two RED walls, `git stash` lowers one and `git stash -u` the other. S03
     (02:44).
   - **V3, three gates: who, may, switched on.** Key → token → role lock → API switch. S05 (06:51),
     with a callback in S07.
   - **V4, the `docker-shell.sh` switchboard.** Four tracks come from one `case`, and the run track
     has a local-image diamond. S06 (09:09), S08 and S09.
   - **V5, two windows into the laptop.** `$(pwd)/../../secrets/` is drawn as a walk, next to the
     `/app` and `/secrets` mounts and the credentials signpost. S06. The contrast is in S09
     (17:25–17:49), where a key rides `COPY --chown=app:app . ./` (Dockerfile line 39) into a layer.
   - **V6, little computers on one network.** Each box has its own `localhost` loop and port strip,
     on the `toynet` rail, with the phone book at 127.0.0.11. S10 (18:40) and S13. S10 carries the
     lecture's "network namespace" bridge: both box frames flash at 19:06.9–19:08.8.
   - **V7, doors, rooms and tickets.** `-p 127.0.0.1:8090:9100` becomes a street door and a room.
     The other pieces are the ephemeral-port ticket 55620, `0.0.0.0` against `127.0.0.1`, and the
     moves to 8095 and 9300. S11–S14 (20:09–27:44).
   - **V8, commands become one file.** The by-hand flags flash at 27:54.8 and fly to their
     `docker-compose.yml` keys (through 28:11.1). Then come Ctrl+C, `down`, and `up -d` re-forming
     only the gateway. S15 and S16.

   **How this was checked:**
   - QA's director watchers read every draft sheet against the SHOW lines.
   - In the final cut, the tag check found the cited picture on screen for all 18 slide tags. These
     include the bind-mount route, the glass boxes and the rail, the `-p` door and room, and the
     flags flying to their YAML keys.
   - The visual pass read the burned-in copy every 3 s.
3. **Pause-and-ponder moments and a recap** ⚠ partly met.
   - **Ponders:** there are five cards, each with a silent timer. Each answer starts as its timer
     ends, and no cue plays during a timer: the silent windows run 6.8–8.8 s (`measured.json`
     `ponder`).

     | scene | question (README wording) | card | timer |
     |---|---|---|---|
     | S05 | where `generate_text` fails when the key and APIs are in place but the Agent Platform User role is missing | 08:45.82 | 08:46.42–08:54.42 (8 s) |
     | S07 | whether a step that exited with status 0 called Gemini | 12:35.93 | 12:36.53–12:42.53 (6 s) |
     | S08 | which Python a teammate gets from `./docker-shell.sh run` without building | 15:07.62 | 15:08.22–15:16.22 (8 s) |
     | S13 | what answers inside the gateway for `localhost` instead of `processor` | 24:23.92 | 24:24.52–24:30.52 (6 s) |
     | S14 | which one setting fixes the processor's new port, and whether any image needs rebuilding | 27:00.63 | 27:01.23–27:07.23 (6 s) |

   - **Rate:** that is one ponder every 6.4 min. AGENTS.md aims for one every 2 min, which would be
     about 16 at this length. The series brief fixes 3–5 per lecture (`ac215-video` skill, step 3),
     and BRIEF.md plans these five. The longest gaps between ponder cards are 00:00–08:45.8
     (525.8 s) and 15:07.6–24:23.9 (556.3 s).
   - **Follow-along pauses:** separately, 21 narrated "Pause and …" prompts tell the viewer to stop
     and run a step, from "Pause and run both." (02:55.9) to "Pause and shut it down." (31:12.6).
     These are follow-along pauses, not ponders.
   - **Recap:** S16 closes with "To test yourself, pause after each question." and five questions,
     31:14.3–31:55.0. There is one per core idea: build or pull, the three gates, the key in an
     image, `-p ip:host:container`, and `localhost` and names. The answers are in `exercises.md`
     and are not spoken. The L05 teaser follows (31:55.3–32:07.5).
   - **No spoken summary:** the recap has no spoken summary of the content. Part 1 has no recap of
     its own; it ends on the clean-up card.
   - **Open question for Conny (as for L03):** does the series format, five ponders and a recap
     made of questions, satisfy this gate for AC215?
4. **Narration written for the ear, with word-anchored cues** ✔.
   - **Spoken style:** script.md's conventions apply. Commands, flags and paths are said in words
     ("dash p", "slash app", "dash dash build"). Ports and addresses go through the L04 lexicon block.
     Versions that will change are said "at the time of recording".
   - **Size:** 156 SAY lines and 4,379 words, identical to the 156 blocks spoken in the renders
     (`recheck/measured.json` `narration`). It was 4,377 before fix round 1's S13 sentences (S13:
     294 → 296). The voice is Kokoro `af_heart` at speed 0.9 in all 16 scenes. The pace is 136.1 wpm
     over the runtime and 147.2 wpm over voiced time, as before.
   - **Anchors:** 606 `vo.wait_until` call sites and 3 `time_until` calls drive the reveals; 11 of
     them take a variable instead of a literal phrase. Every literal phrase is in script.md, and the
     16 render logs have 0 "anchor not found" warnings. This was counted again on the re-rendered
     scenes, with the same result (`recheck/measured.json` `anchors`, `render_logs`).
   - **Ear fixes:**
     - In the draft, "port toy" was heard as "port tie". A lexicon entry (`tˈoɪ`) fixed it, and in
       the final ASR the large model hears "port toy" (18:43).
     - The finishing pass re-voiced S03, S04, S10, S13 and S16 for its narration items.
   - **Caveat:** within a sentence, subtitle cues are cut by the number of characters displayed. So
     two S13 cues around spelled-out addresses were about 2 s off the voice. Fix round 1 gave each
     address its own sentence, and in the re-stitched cut those cues appear 0.22–0.26 s before their
     words (F2), like most cues (the final review's median was +0.18 s). The marginal mid-sentence
     cases elsewhere stay ("Open", item 2).
5. **Simulated-target-viewer QA over the full draft** ✔.
   - Seven watchers reviewed the 480p draft. Two of them were simulated target viewers ("newcomer",
     one per part): agents that read the draft's contact sheets, pulled frames and the English
     `.srt` as a viewer following along with the README, step by step. Neither of them played the
     draft or listened to it.
   - They reported 62 timestamped findings: 2 must, 26 should and 34 nit. The two newcomers reported
     25 of them.
   - Both musts are fixed and checked in the final cut. 22 of the 26 shoulds are fixed and were
     verified on fresh renders; the four still open are shared-toolkit items. Details are under
     "Whole-video QA".
6. **Measured checks** ✔. The numbers are under "Verified (final render)", re-measured on the
   re-stitch (`recheck/measured.json`).
   - **Duration:** 32:10.0 (1930.018 s) after the re-stitch (32:09.8, 1929.832 s, at the 12:26
     stitch), inside the series' 25–35 min.
   - **Loudness:** −16.1 LUFS integrated in all four re-stitched MP4s. True peak is −2.8 dBTP and
     sample peak −2.8 dBFS in every file, so the build's target (true peak at or below −1.5 dBTP) is
     met, with 1.3 dB to spare.
   - **Caption bounds:** all 553 cues of the re-stitch's `.zh-en.ass` (the file burned into the
     zh-en copy) sit inside the subtitle band, at y 991–1062 px (the band starts at y 938). None has
     more than two rows, and none is clipped. This was measured again by rendering that `.ass` on a
     blank 1920×1080 canvas at 2 fps (3,862 frames, `recheck/measured/caption_bounds.json`), with
     the same bounds as the 12:26 burn's 554 cues. The burned copy itself was looked at on frames
     (the re-check's contact sheets and the swap frames in F1), not measured cue by cue.
   - **Music balance:** does not apply. L04, like L02 and L03, has no score: `video.yaml` has no
     `music:` key, and between voice clips the audio is digital silence (the ASR onset check's floor
     is −120 dBFS).
   - **Cue sync:** this is the one measured weakness ("Open", item 2). Its two clear S13 cases are
     fixed (F2).

   **Human review:** the series waiver below stands in for a listening sign-off.

   Listening sign-off: waived by Conny for the AC215 series (Explainer_Videos#29, 2026-10-15): 「不需要，我现在对视频质量很满意的」 — no human listened to this cut; the ASR round trip below is the substitute.

   **The ASR round trip ran on the previous stitch** (the 12:26 clean cut), not on the re-stitch.
   - **Narration changed since then in one scene, S13:** its two address sentences were re-voiced
     (fix round 1, T9). Their audio was checked only as the re-check reports: speech onsets, and a
     machine transcript of those sentences cut from the final cut (F2). No whole-video ASR was run
     on the re-stitch.
   - **S06 and S10 were re-rendered without narration changes.** In the re-stitched clean cut, the
     10 ms audio envelope of S01–S12 is identical to the one the ASR round trip used
     (`rms10ms.npy`), and that includes S06 and S10 (`recheck/record/rms_compare.json`).
     S14–S16 follow it 0.213 s later (3,413 samples at 16 kHz, the best shift in a search from
     3,100 to 3,600; about ten 1,024-sample AAC frames), within 0.43 dB at the 99th percentile in
     speech: the same narration, re-encoded behind the longer S13. The verifier pass reproduced
     both results from its own decode (`recheck/adversarial/audio_check.json`); the shift search is
     not in `rms_compare.py`, only its result in the JSON's `after_s13_fractional_shift` key. Their
     picture moved 0.200 s, so their sound now sits 13 ms later against it than in the 12:26
     stitch, which is under one frame at 60 fps.

## Whole-video QA (480p draft, 2026-10-17; times are draft times)

**Watchers and findings.** Seven watchers reported 62 findings: 2 must, 26 should and 34 nit
(`wjgb45ot6`, key `result`).

| watcher | lens | must | should | nit |
|---|---|---|---|---|
| director, part 1 (S01–S09) | facts, commands and terminal lines against the README and captures, tracker, sync | 0 | 6 | 8 |
| newcomer, part 1 | simulated target viewer, README and clone open | 1 | 6 | 8 |
| director, part 2 (S10–S16) | the same, plus `explainer.check` on all seven scenes | 0 | 5 | 1 |
| newcomer, part 2 | simulated target viewer | 1 | 3 | 6 |
| subtitles (zh, zh-en, en) | glossary, cue and line breaks, reading speed, pairing | 0 | 4 | 10 |
| follow-ups (`QA_FOLLOWUPS.md`) | the logged review-bot items, on fresh 720p frames | 0 | 1 | 0 |
| ASR (base.en, large-v3-turbo) | mishearings, cue sync | 0 | 1 | 1 |
| **total** | | **2** | **26** | **34** |

**What held up in the draft:**
- The commands, README chips and line numbers, code-panel headers and terminal lines matched the
  README, the sources and the captures. Examples: the `2025-02-18T21:04:17…` inspect line, the
  build times 99.5 / 52.6 / 8.2 / 7.9 s, 137 = 128 + 9, and the DNS server at 127.0.0.11.
- Every scene ended on an empty frame, and no ponder card showed its answer.
- `python -m explainer.i18n check --lang zh` printed OK.

**Two factual slips, both fixed:**
- S03 said the student wrote `docker-shell.sh` in lecture 3. The branch adds it, and the line now
  ends "which this branch commits" (final 03:06.4).
- S07's fix chip, headed "cli_11.py · line 30", showed the corrected text instead of line 30.

**The two musts, and how each was fixed.**

- **Draft 04:30, S03 (newcomer, part 1).** The warning to copy out your ignored lecture 3
  Dockerfile, pyproject.toml and uv.lock came 2 s after "Pause and switch your own clone". A viewer
  who paused there lost those files: checkout overwrites ignored files, and `git stash -u` doesn't
  save them. It was fixed in two steps:
  - The S03 fixer opened the your-turn card with a GREY `extra` row: "first: copy out your lecture
    3 Dockerfile, pyproject.toml, uv.lock · the switch replaces them".
  - The finishing pass moved the spoken warning before the pause.

  **In the final cut:**
  - "Before you switch your own clone, copy out any lecture 3 Dockerfile, …" starts at 04:31.07
    (`.srt` cue 84), and "Pause and switch." at 04:41.50 (cue 86).
  - The card with that first row is on screen at 04:38.0 (`writer/clean_t278.0.png`).
  - S03 grew about 10 s, which moved S04 to 05:10.55 and the skip chip to "5:10".
- **Draft 28:05, S15 (newcomer, part 2).** The narration said "cd into port toy first", but the
  second terminal's prompt jumped from `~$` to `~/AC215/port_toy$` with nothing typed. The fix in
  `s15_compose.py` types `cd ~/AC215/port_toy`, which is asserted against the prompt, and then the
  new prompt flashes.

  **In the final cut:**
  - The narration line starts at 28:44.60 (`.srt` cue 477) [479, 28:44.80].
  - The `cd` is being typed at 28:49.6, and the new prompt shows at 28:51.0
    (`writer/clean_t1729.6.png`, `writer/clean_t1731.0.png`).

**The shoulds: 22 of 26 fixed, and verified on fresh 720p renders.** By theme:
- **Follow-along and narration (13):**
  - **S04:** a ▶ your-turn card for creating the bucket and uploading `input-<something>.mp3`. It
    says names are globally unique and shows the gcloud alternative "after gcloud login". The
    narration gained "Bucket names are global: pick a unique one. Pause and create yours." (final
    06:44.25–06:48.75).
  - **S06:**
    - The "Permission denied → `chmod +x`" and Windows (`winpty`) hint now appears at "Pause and
      run it" and stays about 14 s.
    - The extra `docker inspect` folds inside its quotes with a GREY ↪. Its "copy it from the study
      guide" caption is up about 4.3 s instead of 0.5 s.
    - The 3-row strip keeps `ls -la /secrets` with its output.
  - **S07:** `git diff cli.py` shows "…" and the note "gcp_project and bucket_name edited too".
  - **S08:** the extra `docker image inspect --format …` is typed as captured, so the 3-line panel
    can be reproduced.
  - **S09:** "Prod is optional: after the fix, run it only if your team publishes." (final
    18:01.77). The tracker reads "Publish the container (optional)".
  - **S10:** `ls gateway processor` lifts into a chip, and the strip is wiped between output
    batches, so the command and its output are readable together.
  - **S14:**
    - The "move your door" card is fully up about 4.3 s instead of about 1.3 s.
    - `docker network rm toynet` stays readable about 3.9 s.
    - The closing card holds about 3.2 s.
  - **S15:** one sentence now says what Compose is: "Step 4: Docker Compose, which builds and
    starts the whole app from one YAML file" (final 27:44.43).
  - **S16:** "Step 3: repeat the port experiments in the file." became "Next, the README says to
    repeat the port experiments in the file." (final 30:22.08). Two watchers reported this one.
- **Facts (3):** the two slips above; the S03 one was reported twice.
- **Picture and sync (3):**
  - S06's "Docker Hub account" tag no longer cuts line 14's comment.
  - S15's yellow box around `127.0.0.1:8090->9100/tcp` no longer vanishes for 1.9 s.
  - S16's picture now follows "We added a comment… Changed code… needs --build" in order (final
    30:40.30–30:46.91), with the diff readable about 2.8 s instead of under 1 s.
- **Subtitles (3):**
  - The error text "the input device is not a TTY" is no longer split; the final pairing check finds
    `.zh-en.srt` #202/#203 [#201/#202] paired correctly.
  - A zh cue no longer cuts S03's subject from its verb.
  - A bilingual cue no longer ends on "push 到".

**The four open shoulds.** All four are in shared code, outside this episode's files:
- **Draft 12:07 (S07) and 20:10 (S11): the terminal scroll.** `Terminal._make_room`
  (`explainer/devops.py`) slides the rows leaving a terminal up by the whole overflow, so for about
  0.35 s they cross the title bar and whatever sits above it. Two of these four findings are this
  one.
  - The toolkit is unchanged. S07 and S10 now avoid the effect in the scene: S07 fades the old rows
    in place, and S10 wipes the strip between batches.
  - The S11 verifier still saw it at scene time 33.6–34.0 s (about 20:43), and the S10 verifier at
    about 72.3 s (about 19:52).
  - The final visual pass samples every 3 s and did not catch an instance.
- **Draft 01:00 (S01): "Tutorial / 0".** The English `.srt` breaks "Tutorial / 0" across two lines:
  `_cut_penalty` in `explainer/subtitles.py` reads "0 and a" as "and a half". It is still in the
  final `.srt`, cue 17 at 01:00.66, which was checked for this record. The burned-in copy keeps
  that English sentence on one line.
- **Draft 22:30 (S13, ASR): cue timing.** Inside a sentence, cue boundaries are timed by the
  characters displayed (`explainer/subtitles.py:1086`), so spelled-out addresses and flags leave
  cues early or late. Fix round 1 fixed the S13 case in the episode's text: each address is now its
  own sentence, so a voice mark anchors its cue (F2). The shared splitter is unchanged, so the
  marginal cases elsewhere stay ("Open", item 2).

**The nits: 30 of 34 fixed, one partly fixed, three open.** Examples of the fixes:
- S01's container session is now TEAL.
- S08's stale image turns RED when the box opens.
- S09's cloud VM is BLUE, and S09's clean-up `docker images` shows the pulled `dlops/*` rows.
- S05's tracker numbers match the README's 1–5.
- S06 shows the line numbers it cites.
- S11 explains why an identical COPY line is rebuilt.
- S13's RED error phrases no longer break mid-word, and "subnet" is explained in speech and on
  screen.
- S16 explains the ≈10 s waits and labels the part-1 quiz questions.
- The English line keeps terminal text as printed.

Not fixed, with the reasons:
- **S03, draft 04:50 (open):** "delete each component's secrets folder now" has no command.
  Adding `rm -r */secrets` needs a new capture taken after `mega-l03-laptop/12–13`, and S09 relies
  on the old key still being there. It was out of scope for the finishing pass.
- **S06, draft 09:15 (open):** the translucent highlight bars (`line_bar`, shared
  `explainer/devops.py`, unchanged) are taller than the line pitch and tint the ascenders of the
  next line. This was not re-checked in the final cut.
- **S05, draft 07:23 (open):** in the bilingual track, the label "一个小疏漏" merges back into the
  previous cue (shared `_merge_short`). It is still in the final cut: `.zh-en.srt` #140 at 07:37.63
  reads "Text-to-Speech 不需要角色。一个小疏漏 / Text-to-Speech needs no role. A small slip:"
  (checked for this record; #139 in the re-stitched file, same text).
- **S13 and S15, draft 23:00 / 28:12 (partly fixed):** wrapped capture lines broke mid-word. S13
  now folds at word boundaries (`fold_words`). S15's `docker compose ps` and `ps -a` still wrap
  at column 65 inside the SERVICE column, as "process / or": capture lines 48:4 and 52:4 are 103
  and 127 characters long, and `s15_compose.py` still prints them with `wrap=True`. In the final cut
  the wrapped rows print at about 28:52 and 29:43.

**Process.**
- **Fixers and verifiers:**
  - One fixer per scene for the 14 scenes with findings.
  - One narration/subtitle fixer for 22 issues in script.md, `i18n/zh/narration/g1.yaml` and
    `g2.yaml` and the lexicon.
  - A skeptical verifier per scene, on fresh 720p frames and `explainer.check`.
- **Verifier corrections:** the verifiers corrected or completed several fixes.
  - **S03:** the warning lines now flash with the reworded sentence.
  - **S04:** the gate animation is faster, so the card lands on its sentence, and "after gcloud
    login" is back.
  - **S06:** the inspect caption measured 4.3 s, not the fixer's 5.5 s.
  - **S07:** the scroll through the second terminal is fixed in the scene, and two crossfades are
    staggered.
  - **S09:** the tracker reads "(optional)", and the card notes the base image.
  - **S13:** an on-screen gloss for "subnet" was added, and the laptop's curl error now breaks
    just before "Could not connect to server", which keeps that RED phrase on one row.
  - **S14:** both your-turn cards were tightened.
  - **S15:** a chip flash now plays during the new Compose sentence, which had left 4.1 s with
    nothing moving.
  - **S16:** beat 4 is shorter, so the diff prints before "Changed code".
- **QA_FOLLOWUPS.md:** the follow-ups watcher confirmed:
  - the S11 underlines and the S16 brace are fixed;
  - S15's `swap_panel` problem does not reproduce;
  - the `col_box` positions are right.

  It also found the S15 box flicker, which is fixed (see the shoulds above).

### Finishing pass (2026-10-18)

- **Plan (`wf5a69r10`):** 12 text items for script.md, BRIEF.md and the zh files, and scene items
  for 13 scenes (the "do" proposals of SLIDES.md, lecture-slide tags and diagram labels, plus a few
  open QA items), each scene with a verifier. The 12 text items were six narration changes (S03
  twice, S04, the S10 slide bridge, S13, S16), five SHOW/BRIEF syncs (S05, S07, S08, S09, S15) and
  the slide-tag lines for the SHOW.
  - That first run (about 05:34 UTC) applied almost nothing. Its agents took a user's status
    question about L02/L03, sent mid-run, as their task and declined their edits.
  - The exception is the S13 scene agent: it added S13's two slide tags (slide 35, slides 33–34),
    and its verifier passed them on fresh 720p frames.
- **Scoped rerun (`args/l04scoped/`, about 06:45–09:35 UTC): 11 of the 12 text items applied, the
  12th only in part.** The slide-tag lines went into the SHOW for S13 only, because no other scene
  had its tags yet; that is why script.md names only S13's tags ("Open", item 9).
  - **S03:** the warning before the pause, and "the commit we recorded".
  - **S04:** the bucket sentence.
  - **S10:** the bridge "The lecture calls this a network namespace: each container is isolated
    until you wire it." (final 19:06.18).
  - **S13:** "from toynet's own address range, its subnet" (final 24:55.91).
  - **S16:** "To test yourself, pause after each question." (final 31:14.33).
  - **Sync:** SHOW and BRIEF were brought in line with the scenes for S05, S07, S08, S09 and S15,
    and the zh lines and glossary terms were updated to match.

  S03, S04, S10, S13 and S16 were re-voiced, and `explainer.i18n check --lang zh` printed OK.
- **Scene agents, each followed by a verifier:**
  - **Lecture tags:** they added the `lecture_ref` tags in S01, S02, S06, S08, S09, S10, S11, S14,
    S15 and S16. S13's two tags were already in the code from the first run, which makes 18 in
    all.
  - **Diagram labels:**
    - S02: "· images", "source control" and the lead-developer label.
    - S06: "host folder" and "container path".
    - S08: "lecture's order: lock files first, code last".
    - S09: the `.dockerignore` continuation row and "remove images built before the fix".
    - S10: the bridge flash and "Docker DNS".
    - S15: "lecture's by-hand run: -v", "= your typing order" and "started, not ready".
  - **Verifier fixes:**
    - S02: the laptop images had vanished ahead of their laptops (`FadeOut(mates)`).
    - S10: the flash had landed before "namespace"; a 0.7 s wait fixes it.
    - S16: the `^C` row had slipped 0.2 s and is back in place.
  - **S16:** it was finished after a container restart (`wy9fj1vih`).
- **Two review-bot findings, checked on frames (`w5vfyl23g`, 10:20 UTC):** neither reproduces.
  S02's tag and README card keep a 0.22-unit gutter, and S03 leaves no glyphs after
  `FadeOut(card9)`. The S02 box crossing the "Docker Hub · images" caption was left to this review
  ("Open", item 6).

## Final-cut checks (1080p60, 2026-10-18)

Five agent checks of the stitched deliverables. No human watched or listened.

**Lecture-slide tags and review-bot items** (`report-tags.md`; evidence in `tags/`).
- **All 18 tags pass:**
  - Each one reads correctly, arrives with the picture it cites and keeps that picture on screen.
  - Each one leaves before its scene ends.
  - Nothing overlaps any of them: 0 changed pixels inside any tag box (plus 4 px), over 3,575
    frames sampled at 20 fps (`tags/overlap_scan.json`).

  | # | scene · tag | in | out |
  |---|---|---|---|
  | t01 | S01 · slides 42–43 | 00:39.6 | 00:46.9–00:47.6 |
  | t02 | S02 · slides 37–40 | 02:15.6 | 02:27.6–02:28.4 |
  | t03 | S06 · slides 23–24 | 09:50.9 | becomes "slide 26" at 09:57.9 |
  | t04 | S06 · slide 26 | 09:57.9 | 10:03.6–10:04.0 |
  | t05 | S08 · slide 7 | 14:17.9 | 14:22.4–14:23.0 |
  | t06 | S08 · slides 37–38 (mid-right) | 14:23.9 | 14:35.2–14:35.8 |
  | t07 | S09 · slide 13 | 17:01.2 | 17:13.2–17:13.8 |
  | t08 | S09 · slides 8, 15 (under the line-39 panel) | 17:40.5 | 17:46.7–17:46.9 |
  | t09 | S10 · slide 33 | 18:56.4 | becomes "slide 34" at 19:12.4 |
  | t10 | S10 · slide 34 | 19:12.4 | 19:22.5–19:22.8 |
  | t11 | S11 · slide 12 | 20:11.4 | 20:31.7–20:32.0 |
  | t12 | S11 · slide 35 | 20:58.5 | 21:18.1–21:18.6 |
  | t13 | S13 · slide 35 | 23:50.1 | 23:55.7–23:56.2 |
  | t14 | S13 · slides 33–34 | 24:38.9 | 24:48.8–24:49.6 |
  | t15 | S14 · slide 26 (top band, left of the page's `illustration` tag) | 27:16.0 | 27:27.6–27:28.1 |
  | t16 | S15 · slides 17–20 (bottom right) | 27:54.8 | becomes "slide 27" at 28:17.1 |
  | t17 | S15 · slide 27 (bottom right) | 28:17.1 | 28:24.8–28:25.4 |
  | t18 | S16 · slide 29 | 30:01.2 | 30:08.8–30:09.1 |

- **After fix round 1:** the tags of the re-rendered S06, S10 and S13 (t03, t04, t09, t10, t13,
  t14) were checked again on frames of the re-stitched cut: same text and spans. t13 now comes in at
  23:50.35 and t14 at 24:39.12, about 0.2 s later; t15–t18 are 0.2 s later (see the re-check).
- **Tags off the top-right corner:** five tags sit elsewhere because the top-right slot is taken
  (marked in the table). The scene code documents each one. In the zh-en copy, the bottom-right S15
  tags never touch the burned subtitles (eight frames, `tags/frames/zhen_S15_*.png`).
- **The review-bot items, verified on frames:**
  - **S03 skip chip:** it reads "cloned fresh? skip to 5:10" and is fully visible 03:15.5–03:23.1,
    with nothing over it. S04 starts at 05:10.550, so the chip lands 0.55 s early, inside S03's
    fade-out. The same holds in part 1 and in the zh-en copy (`tags/sheets/s03_skip_sheet.png`).
  - **S02 lead label:** it ends at x 6.27, inside the 6.6 limit.
  - **S02 tag and README card:** they stay 0.25 units apart.
  - **S03 leftover glyphs:** none, in frames from 04:43.4 to 04:44.0, just after beat 10 starts.
  - **S10 bridge:**
    - Both box frames flash at 19:06.9–19:08.8 while "network namespace" is said (19:07.6–19:08.2).
    - The localhost loops are indicated at 19:09.1–19:10.1, on "isolated".
    - The PINK "Docker DNS" label is up 19:16.2–19:22.5.
  - **S11:** the underlines sit under their own lines in gateway.py 13–14.
  - **S16 shared-layers brace:** it sits right of the size column and inside the terminal
    (31:08.7–31:12.6).
  - **`col_box` in S13 and S15:** the outlines frame exactly their characters.
- **The review-bot items in the re-stitched cut.** No new review-bot item came with fix round 1.
  Each of the eight items above is marked here as verified on the 12:26 stitch only, or verified
  again on the re-stitch:
  - **Verified again, S10 bridge (S10 was re-rendered):** both box frames flash at 19:07.72, and the
    loops' pulse peaks at 19:09.63 (`recheck/S10/clean_S10_frameflash_s0027.60_f19m07.717.png`,
    `recheck/S10/clean_S10_loop_peak_s0029.52_f19m09.633.png`). The PINK "Docker DNS" label is up at
    19:22.37 (`recheck/S10/clean_S10_lref34_late_s0042.25_f19m22.367.png`). The start of the label
    (19:16.2) was not checked again.
  - **Verified again, `col_box` in S13 (S13 was re-rendered):** the dashed outline on the
    processor's empty PORTS cell spans the column of `127.0.0.1:8090->9100/tcp` above it, at 23:13.55
    (`recheck/record/clean_S13_tag_s0016.80_f23m13.55.png`). S15's `col_box` was not checked again;
    S15 is the same render as before, 0.2 s later.
  - **Verified again, S03 skip chip, by scene start only:** S04 still starts at 05:10.550
    (`recheck/scene_starts.json`), so "skip to 5:10" still lands 0.55 s before S04. The chip's frames
    were not pulled again; S03 is the same render.
  - **Verified on the 12:26 stitch only:** the S02 lead label, the S02 tag and README card, the S03
    leftover glyphs, the S11 underlines and the S16 brace. Fix round 1 did not touch S02, S03, S11 or
    S16, and their render logs predate it (the latest is S03's, 12:05 UTC; `recheck/measured.json`
    `render_logs`). Their frames were not pulled again.
- **Side findings:**
  - The S02 box crossing ("Open", item 6).
  - The S09 chapter mark ("Open", item 3; fixed in the re-stitch, F3).

**ASR round trip, the substitute for a listen** (`report-asr.md`; `asr.json`, `align_spoken.json`,
`clips_large-v3-turbo.json`, `onsets_rms*.json`). It ran on the 12:26 stitch. Since then only S13's
narration changed; its two new sentences were checked on the re-stitch as F2 reports, and the audio
outside S13 matches what this round trip heard (gate 6).
- **Raw comparison:** faster-whisper `base.en` transcribed the clean cut's audio, which was compared
  with the 531 cues of `.srt`. 231 cues differ in their raw wording. Most of these are written
  versus spoken forms (digits, "-p" said "dash p", "/app" said "slash app") and words that shift
  across a cue boundary.
- **Against the spoken text:** aligned with the text Kokoro was given (4,422 words), 68 spans needed
  judging. All 68 were judged, and the doubtful ones were transcribed again with `large-v3-turbo`
  (43 clips, 127 cues).
- **Real mispronunciations or swallowed words: none.**
  - **Cues 407–409** [409–411] (24:17.7–24:23.7, "Ponder this…"): `base.en` returned nothing here.
    The speech is there and in sync, and the large model hears it word for word.
  - **"docker" at 30:07 and 30:13:** it is missing from the speech by design. The narration says
    "Compose logs dash f…", while the subtitle shows the full command.
- **Left for a human ear (low severity):** "git" is heard as "get" at 02:50, 03:38, 03:48 and
  03:50, and "for Git" as "forget" at 17:50.
  - Kokoro's phonemes are right (ɡˈɪt), and the command is on screen each time.
  - Clips for a listener: `clips/G46_c49-50_163.37-171.61.wav` (02:50),
    `clips/G4_c66-71_214.41-233.50.wav` (03:38–03:50) and `clips/G12_c299-300_1065.67-1073.72.wav`
    (17:50).
- **Sync:** the mix falls to digital silence between sentences, so speech onsets are exact. All 438
  cues that start in silence begin speaking within 1 s (median +0.18 s). The cues that are off by
  about 1 s or more all start mid-sentence ("Open", item 2).

**Visual pass over the burned-in copy** (`report-visual.md`; `sheets/`, `visual/`).
- **Method:**
  - 644 frames, one every 3 s, on 41 contact sheets, all read.
  - Motion measured every 0.25 s on the clean cut.
  - The first and last frame of every scene.
  - A scan of all 644 frames for subtitle rows and for content at the frame edges.
- **Passed:**
  - No scene is black or missing, and all 16 scenes start and end on an empty frame.
  - No content comes within 6 px of the frame edge, and no tag is stuck on screen.
  - No glyph is garbled. The port strip's "1 ▯▯▯▯ 65535" is eight drawn rectangles, not missing
    glyphs.
  - All 662 distinct subtitle characters render.
  - The re-rendered S15 and S16 are clean.
- **Burned-in layout:**
  - The picture is scaled to 1670×938 at the top of the frame, and the subtitles sit in the band
    below it (y 992–1062). So they cannot cover a terminal command; 12 spot checks with a command on
    screen confirm it.
  - All 554 cues are one Chinese line (50 px) above one English line (33 px).
  - The widest lines are 1472 px for Chinese (18:01.77) and 1422 px for English (29:59.53), against
    1840 px of usable width.
- **Findings:** all cosmetic, listed under "Open", item 6.

**Bilingual pairing** (`report-pairs.md`; `pairs/`).
- **Scope:** all 554 cues of `.zh-en.srt`, read against `i18n/zh/narration/g1.yaml` and `g2.yaml`.
- **Verified:**
  - SRT and ASS agree on all 554 cues, with start times within 10 ms.
  - 22 frames from the zh-en copy show the SRT's text.
  - The part files have the same text as the full file.
  - Every cue is one zh line and one en line.
  - No command, path, flag or `<placeholder>` is broken across a line or a cue.
  - The known winpty case now pairs correctly: #202 at 11:16.47 and #203 at 11:21.31 [#201/#202,
    same times].
- **Found:** three neighbouring pairs swap meaning, and five are one clause off ("Open", item 1).
  Seven word-level drifts need no change. Fix round 1 fixed all eight (F1).

**Measured** (`report-measured.md`; `measured.json`, scripts and logs in `measured/`). Its numbers
for the 12:26 stitch were replaced by the re-stitch's under "Verified (final render)"; the values that
changed are listed there.

## Fixed after the final review (fix round 1, re-stitch 16:13 UTC)

Fix round 1 fixed F1–F9, and the re-checks confirmed each one on the re-stitched deliverables. F10
was fixed with this record's update. Times are in the re-stitched cut. Paths that start with
`recheck/` are under `build/`.

**F1. The eight bilingual pairs** (was "Open", item 1). The zh sentences now follow the English
clause order (`i18n/zh/narration/g1.yaml`, `g2.yaml`; the text agent's pairs are in
`build/fix1/pairs_AB.txt`). Each new cue was found by its English in the new `.zh-en.srt`. In every
one, the zh half says what the en half says. `.zh.srt` carries the same zh text, and the part files
equal the full files cue for cue (`recheck/subs/pairs_new.json`, `recheck/subs/parts_check.json`).

| item | was (`.zh-en.srt`, 12:26 stitch) | now | en halves of the new cues |
|---|---|---|---|
| A1 (S04) | #108/#109, 05:43.48–05:49.93 | #107/#108, 05:43.48–05:49.93 | "A small slip: … if you forget," / "but it only rejects an empty value." |
| A2 (S16) | #542/#543, 31:23.97–31:28.85 | #541/#542, 31:24.17–31:29.05 | "Two: which three gates must a call" / "to your bucket pass, and where does each one fail?" |
| A3 (S16) | #551/#552, 31:55.25–32:01.61 | #550–#552, 31:55.45–32:05.33 | "Next lecture, … calls a database" / "container by name on a Compose network," / "with the same secrets mount: …" |
| B1 (S03) | #91–93, 04:42.93–04:52.13 | #91–#93, 04:42.93–04:54.88 | "Extra checks show your ignored lecture 3 Dockerfile," / "pyproject.toml and uv.lock were replaced by the branch's," / "without a word: copy them out first if you want them." |
| B2 (S04) | #105–107, 05:32.23–05:43.24 | #104–#106, 05:32.23–05:43.24 | "An extra grep shows what ships: three files are blank," / "but … already hold the course's project and bucket," / "and the instructor's group name." |
| B3 (S08) | #286/#287, 16:26.92–16:30.91 | #285, 16:26.92–16:30.91 | one cue: "If you tried this, delete it and run dev to get your own image back." |
| B4 (S09) | #324/#325, 18:25.73–18:31.22 | #322–#324, 18:25.73–18:34.14 | "…until you delete it," / "when the course is over;" / "the key works until you delete it in the console." |
| B5 (S15) | #515/#516, 29:47.23–29:53.59 | #514/#515, 29:47.43–29:53.79 | "docker compose down removes the containers and the network," / "and nothing is left in ps -a." |

- **On purpose:** A1, B2 and B5 differ from the target wording in the item list. A1 adds 其实 so
  that 一个小疏漏 stays in its cue. B2 and B5 are shortened so that 已有 sits with "already hold" and
  和网络 with "and the network".
- **Word-level drift, no change needed:** in A3 the English splitter cuts "a database / container",
  while the zh first cue already has 数据库 container.
- **Burned frames of the three former swaps** read the new text: `recheck/subs/frames/m_swaps.png`
  (A1 at 05:45.57 and 05:48.78, A2 at 31:25.15 and 31:27.60, A3 at 31:57.32, 32:00.48 and 32:03.57).
  The full frames are `recheck/subs/frames/zhen_A*.png`.
- **Everything else unchanged:** outside these items and S13, every cue keeps its text. Cues before
  S13 keep their times, and cues from S14 on are 0.20 s later (`recheck/subs/cue_shift_vs_old.json`).

**F2. S13 cue timing** (was "Open", item 2, its two clear cases). T9 split the two sentences so that
each address starts a sentence: "Docker ps shows the gateway's mapping, host side first. It reads
127.0.0.1, port 8090, to 9100." and "With door 8091 it works. The mapping shows 0.0.0.0. That means
every address: other machines on your network could connect."

Speech onsets were measured in the final cut's audio with the final review's method (`onset_rms`):
10 ms RMS of the whole clean cut decoded from its start, the timeline of `rms10ms.npy`. A speech run
starts above −45 dBFS after at least 120 ms below it. Every sentence gap here is digital silence
(−120 dBFS). Onset = speech start − cue start (`recheck/adversarial/onsets_s13_corrected.json`, from
`audio_check.json`).

The re-check's first figures (`recheck/s13_audio/onsets_s13.json`: +0.08 to +0.12 s, and +0.50 s
for `.srt` #400) were 0.139 s too small. Its WAV, `final_1370-1440.wav`, starts at 1370.139 s on
the cut's timeline, not at the 1370.000 s its script assumed (three 10 s probes match the full
decode sample for sample, `recheck/adversarial/wav_offset.json`). The corrected onsets below agree
with the final review's for the unchanged S13 cues around them (+0.23 to +0.29 s).

| cue (`.srt` / `.zh-en.srt`) | cue starts | onset | before the fix round |
|---|---|---|---|
| "It reads 127.0.0.1, port 8090, to 9100." #390 / #403 | 23:02.681 | +0.22 s | `.srt` cue 390 at 23:05.51, 2.07 s after its speech |
| "The mapping shows 0.0.0.0." #398 / #412 | 23:39.761 | +0.26 s | the end of cue 397 ("…and the mapping shows 0.0.0.0:") |
| "That means every address:" #399 / #413 (the whole sentence) | 23:43.835 | +0.23 s | cue 398 at 23:42.14, 2.28 s before its speech |
| "other machines on your network could connect." `.srt` #400 only | 23:45.245 | +0.64 s | (part of cue 398) |
| "That's why the README writes 127.0.0.1: this laptop only." `.srt` #402 / zh-en #414, which starts with "Remove it." at 23:48.102 | 23:49.382 | +0.25 s (#414: +0.24 s) | cue 400 at 23:49.18 |

- **Every address cue starts within 0.5 s of its words,** in `.srt` and `.zh-en.srt`.
- **`.srt` #400** is the English track's mid-sentence cut ("That means every address: / other
  machines …"). It comes up while "address:" is still being said (that speech run ends at
  23:45.52), 0.64 s before "other" (23:45.88). That is under the 1 s of the marginal cases in
  "Open", item 2, and the burned track keeps the sentence in one cue.
- **The 57-character sentence** "That's why the README writes 127.0.0.1: this laptop only." is one
  two-line `.srt` cue (6.25 s) that starts on its own sentence mark, 0.25 s before its words. It is
  in sync, so it is not a nit.
- **ASR:** faster-whisper large-v3-turbo (int8, beam 5) ran on clips cut from the final cut's mix
  at the silence gaps (`recheck/s13_audio/asr_s13_large-v3-turbo.json`, clips in
  `recheck/s13_audio/asr/`). It hears:
  - "Docker PS shows the gateway's mapping, host side first. It reads 127.0.0.1, port 8090 to 9100."
  - "With door 8091, it works. The mapping shows 0.0.0.0. That means every address. Other machines on
    your network could connect."
  - "Remove it. That's why the ReadMe writes 127.0.0.1, this laptop only."

  Every word is there, and nothing is swallowed.
- **Spoken forms:** a second pass used a prompt that asks for numbers in words
  (`recheck/s13_audio/asr_s13_large-v3-turbo_wordsprompt.json`). It hears "one two seven dot zero dot
  zero dot one", "port eighty-ninety, to ninety-one hundred" and "zero dot zero dot zero dot zero".
  These are the lexicon's forms (`explainer/lexicon.yaml`: 127.0.0.1, 0.0.0.0, 8090, 9100). The
  sentence-final "0.0.0.0." has no extra "dot". This is a machine's hearing, not a listen.
  - **Weaker evidence than the first pass:** the prompt gives examples in the lexicon's style, and a
    few words carry low probabilities ("one" of 127 at 0.02, "eighty" at 0.03). The first, unprompted
    pass, which hears every digit group in place, is the stronger check.

**F3. Chapters** (was "Open", item 3).
- **S09:** `chapters.txt` and `chapters_part1.txt` read 16:45. S09 starts at 1004.999999 s, which is
  frame 60300 and 16:45.000; `23b0407` rounds to the millisecond before flooring.
- **S14:** it moved 25:31 → 25:32. It starts at 1532.000 s, 0.2 s later, because S13 is 0.2 s
  longer (9,303 → 9,315 frames). The fix list said 0.1 s; the stitched scene files say 0.2 s.
- **All lines checked:** each line of the three chapter files equals its scene's start, floored after
  rounding to the millisecond. The starts are summed from the stitched scene files' durations
  (`recheck/chapters_check.json`, `recheck/scene_starts.json`).
- **Against the previous commit** (`git diff de06df0^ de06df0`; `de06df0` already holds the new
  files, so `git diff HEAD` is empty): only those two lines changed. `chapters_part2.txt` is
  unchanged. `transcript.md` changed the same two headings and S13's two sentences.
- **Every other scene start is unchanged,** S06 and S10 included.

**F4. The S06 pill** (was "Open", item 6). The pill "the folder you're in" beside line 8 is now a
slim 0.31-unit pill (20 pt), centred between lines 7 and 9.
- **Gap:** in the 1080p frames there are 3 px of background above and below it. Line 7's ink ends at
  row 469, the pill's border runs from row 473 to 517, and line 9's ink starts at row 521
  (`recheck/S06/pill_gap_scan.json`; 3× crops `recheck/S06/crop3x_pill_*.png`).
- **Text and timing:** its text reads. It fades in at 09:20.70–09:21.20 on "the folder you're in",
  stays with the other beat 0–1 tags, and leaves with them at 09:32.58–09:32.88
  (`recheck/S06/m_S06_pill_seq.png`).

**F5. The S10 "9100" labels** (was "Open", item 6). Both yellow labels now start at the left edge
of "localhost" and clear the loop's arrowhead (`recheck/S10/gap_9100_loop.json`,
`recheck/S10/m_S10_9100_crops3x.png`). The nearest pixels are:
- 24 px apart at rest (19:02.72, 19:12.32);
- 18 px at the labels' 1.15 pulse on "without any clash" (19:05.02);
- 20–21 px at the loops' pulse (19:09.63).

The labels come in at 19:01.53 with "Two containers can both use port 9100" and leave at
19:12.43–19:12.93.

**F6. The S13 still stretch** (was "Open", item 6). Right after the red cross (24:36.03–24:36.53),
the error row's `localhost port 9200` flashes yellow at scale 1.05 (24:36.53–24:37.23) while "nothing
there listens on 9200" is said. At the peak the words keep their spaces
(`recheck/S13/m_S13_still.png`, `recheck/S13/m_S13_errrow.png`).
- **Motion,** measured every 0.25 s as in the final review (`recheck/S13/motion_s13.json`): the
  stretch is now 3.0 s still (24:33.50–24:36.50), then 1.5 s still (24:37.25–24:38.75).
- **S13's only still run of 4 s or more** is the ponder timer (24:24.75–24:30.50).

**F7. Docs out of step** (was "Open", item 9; the text agent's D1–D3 and T10, `3821b69`):
- `script.md:236` gives `explainer.script`'s count: 4,379 words, 2,581 in part 1 and 1,798 in
  part 2. The re-check ran the tool again and got 4,379.
- `BRIEF.md:324` and `:534` give ponder 1 as the Agent Platform User role and `generate_text`.
- script.md's SHOW lines name all 18 lecture tags.
- `QA_FOLLOWUPS.md` marks the S11 underline item and the S03 skip chip DONE, with a pointer to this
  record. The S02 box crossing stays an open nit.

**F8. Stale drafts** (was "Open", item 10): `output/` holds only the 20 deliverables, and no
`*_480p15*` file is left.

**F9. Publishing prerequisite** (was "Open", item 11): `video.yaml` has a `publish:` block with
`title_zh`, `description_zh`, `tags_zh` (9 tags) and `tid: 231` (`f13ae03`).

**F10. README.md after the re-stitch** (was "Open", item 12; fixed with this record update, no render
or stitch). `README.md`'s full chapter list now equals `output/chapters.txt`: S09 reads 16:45 and S14
25:32. Its part-2 list already equalled `chapters_part2.txt` and is unchanged. The zh-en copy is now
given as 32:10 (1930.0 s) and part 2 as 13:29 (809.8 s); part 1 stays 18:40 (1120.2 s) and the size
122 MB. Evidence: `recheck/measured/readme_check.json` (the mismatch before the edit) and
`recheck/measured.json` `readme_vs_deliverables` (the new values).

**The fixes are in the part files too.** At the three fixed moments, the part file's frame equals
the full cut's frame pixel for pixel: the S06 pill in part 1 (frame 33,689, 09:21.50), the S10 labels
at their pulse in part 2 (frame 1,493, 19:05.02 in the full video) and the S13 flash at its peak in
part 2 (frame 21,405, 24:36.89) (`recheck/record/parts/parts_frames.json`, frames in
`recheck/record/parts/`).

## Open in the final cut (for the coordinator)

Items 1, 3, 9 and 11, and parts of items 2, 6 and 10, were fixed in fix round 1 and moved to
"Fixed after the final review" above. Item 12, found by the re-check, was fixed with this record's
update (F10). Their numbers are kept so that references stay valid.

1. *Fixed: the eight bilingual pairs (F1).*
2. **Mid-sentence cue timing** (shared `explainer/subtitles.py`; QA's open ASR should).
   - **The two clear cases in S13** (`.srt` cue 398 at 23:42.14, +2.28 s, and cue 390 at 23:05.51,
     −2.07 s) are fixed: F2.
   - **Marginal cases, about 1.0–1.5 s** (still open; not re-measured, because cue and speech moved
     together in the re-stitch):
     - Cue up before its speech starts, in `.srt`: cues 465 (28:06.34) [467, 28:06.54], 378
       (22:20.94), 356 (20:57.87), 492 (29:43.45) [494, 29:43.65] and 363 (21:27.27).
     - The same, in the burned track only: zh-en 527 (30:29.48) [526, 30:29.68], 418 (24:02.38)
       [417, 24:02.58] and 201 (11:12.33) [200].
     - Speech before its cue: cue 120 (06:36.96) by 1.36 s, and cue 358 (21:09.38) by 0.99 s.
   - **Fix option for the rest:** weight the English cue split by the spoken form, as
     `_spoken_weights` already does for Chinese (a toolkit change). The subtitles then need re-timing
     and re-burning, but no new audio. Evidence of the old S13 cases: `frames/cue398_t1423.00.png`,
     `frames/cue390_t1384.50.png` and `onsets_rms*.json`.
3. *Fixed: S09's chapter mark (F3).*
4. **Narration over its budget.** 4,379 words against BRIEF.md's 3,900–4,300, so 79 over (4,377 and
   77 over before fix round 1's S13 sentences; `recheck/measured.json` `narration.brief_budget`).
   - S03 (332 words against 280, +18.6 %) and S04 (242 against 210, +15.2 %) are outside ±15 %.
   - Both grew in the finishing pass, with the S03 warning and the S04 bucket sentence.
   - The runtime, 32:10.0, is inside 25–35 min.
   - *Fixed after the re-check: `script.md:238` said "Every scene is within ±15 % of its BRIEF.md
     budget"; it now names S03 and S04 as the two exceptions (text only, no render).*
5. **Gate 3 shortfall:** five ponders against the aim of about 16, and a recap made of questions.
   See gate 3, with its question for Conny.
6. **Minor visual findings (nits).** Each was left because it is cosmetic: the text stays legible,
   or the moment lasts under a second.
   - **02:23.1–02:23.4, S02:** the box flying to the Docker Hub shelf crosses the left end of the
     `illustration` tag (02:23.12–02:23.28) and "Docker Hub · images" (02:23.20–02:23.37); at its
     peak it covers the "Do" of "Docker".
     - That is about 0.25 s over text in all, and it never stops there.
     - A possible fix: route the box right of the caption, with the opposite `path_arc` or a
       waypoint right of x ≈ 5.8 (`tags/sheets/s02_box_cross.png`, `tags/box_cross.json`).
   - *Fixed: the S06 pill "the folder you're in" (F4) and S10's "9100" labels (F5).*
   - **Overlaps while something moves:**
     - 01:45 (S02): a highlighted label touches its card's edge.
     - 07:36.0 (S05): a role badge comes out from behind the console card (0.3 s).
     - 13:15 (S07): "/app/cli.py" crosses the terminal border while it grows (0.6 s).
     - 28:09.6–28:11.1 (S15): the intended fly-in of the flags passes over the YAML.
     - 19:50.7–19:51.3 (S10, found by the re-check): the commit hash `d190c71` flies from the
       terminal to its pill across the terminal's prompt row, the README tree (its processor/ rows
       at 19:50.97, the `docker-compose.yml` comment at 19:51.05) and the top-left border of the
       `ls gateway processor` chip (19:51.15) (0.6 s; `recheck/S10/m_S10_topband_70s.png`,
       `recheck/S10/clean_S10_topband_c_s0070.85_f19m50.967.png`,
       `recheck/adversarial/frames/m_S10_flyover.png`, `m_S10_chip_cross.png`). This part of S10
       was not changed by fix round 1.
   - *Fixed: the 5.25 s still stretch in S13 at 24:33 (F6).*
   - **Wrapped rows in S15:** `docker compose ps` and `ps -a` show "process / or" (from about 28:52
     and 29:43), as described under the nits above.
   - **Seen by verifiers on 720p renders, not in the 3 s samples:**
     - Rows scroll over a terminal's title bar for about 0.35 s (about 19:52 and 20:43; shared
       `_make_room`).
     - S09's fix card flashes solid yellow for about 0.3 s at "after the fix" (about 18:03).
     - S16's beat 2 runs about 1.5 s behind "Compose recreates only the gateway" (`up -d` is typed
       at about 30:30). QA did not flag it, and a fix means shortening the extra `git diff`.
   - **Noticed by fix round 1's fixers and verifiers, left alone** (outside its items; all but the
     last are older than the fix round; `w0g41hm1o`):
     - **23:13.5 (S13):** the "listening ≠ published" tag sits on the bottom of the dashed box on
       the empty PORTS cell. The verifier's 720p frame showed it almost touching; on the final
       1080p frame (23:13.55) the tag's top border (rows 699–702) lies on the box's bottom dashes
       (rows 700–703) and hides them across the tag's width. The tag and the box both stay legible
       (`recheck/record/clean_S13_tag_s0016.80_f23m13.55.png`,
       `recheck/adversarial/frames/clean_f83612_2313.55_tag_crop3x.png`).
     - **19:09.6 (S10):** at the loops' 1.12 pulse on "isolated", each loop comes close to the "l" of
       its "localhost" for a few frames, without touching it on the final frame
       (`recheck/S10/crop3x_clean_S10_loop_peak_s0029.52_f19m09.633.png`).
     - **About 23:50 (S13 beat 3):** the picture change for "That's why the README writes" runs
       23:49.95–23:50.75 in the 1080p render's sidecar: 0.57 s after that sentence's mark (23:49.38)
       and 0.32 s after its speech starts (23:49.63), because typing `docker rm -f` outlasts
       "Remove it." It ends about as "127" is spoken (about 23:50.9 in the machine transcript). The
       verifier also saw, on its 720p render, the "this laptop only" anchor fire about 0.46 s early;
       that was not measured in the final cut.
     - **S06 beat 0 (new with F4):** the pill's text is 20 pt, while the panel's other tags are
       22 pt (a design choice so the text fits a row-high pill).
7. **Shared-code leftovers** (toolkit PRs, outside this episode's files):
   - `Terminal._make_room` scroll travel and `line_bar` height (`explainer/devops.py`).
   - `_cut_penalty` (`.srt` cue 17, "Tutorial / 0") and `_merge_short` (`.zh-en.srt` #140 [#139],
     "一个小疏漏"), in `explainer/subtitles.py`.
   - Cue timing by displayed characters (item 2; S13 worked around in the episode, F2).
   - `common.second_terminal()`: S06's and S08's second terminals switch to the component folder's
     prompt with only the caption "new terminal: cd here first", and no `cd` is typed. That is the
     pattern behind the S15 must. QA did not flag S06 or S08, and the S15 verifier passed it on to
     the toolkit owner.
   - `caption_extra` scrambles a tracker caption for about 0.3 s while it changes (S14). The
     re-check saw the same scramble in S13's tracker caption at 23:56.1
     (`recheck/S13/m_S13_rest.png`).
8. **Left on purpose:**
   - S03's `rm -r */secrets` needs a new capture (see the nits above).
   - `.zh-en.srt` cue 463 (26:38.71) [#462, 26:38.91] shows "Empty reply from server" in both
     rows. Glossary rule A1 keeps terminal text verbatim
     (`measured/frames/cue463_emptyreply_t1599.5.png`).
9. *Fixed: the four docs out of step (F7). README.md was out of step again after the re-stitch
   (item 12, fixed: F10). One doc line is still out of step: `script.md:238` (item 4).*
10. **Small facts, no action proposed:**
    - The fastest English row in the burned track was `.zh-en.srt` cue 287 (16:28.47): 49 characters
      in 2.43 s, 20.1 characters per second. This leaves out cues 18–20, 480–481 and 502–503,
      where one English sentence stays up under two or three shorter Chinese cues; read across the
      repeats, those run at 13.6–15.6 characters per second. After fix round 1 (B3), that sentence is
      one cue (#285, 16:26.92, 68 characters in 3.99 s), and the fastest single English row is 18.9
      characters per second (#300 at 17:18.83 and #145 at 07:56.41); the repeats are cues 18–20,
      479–480 and 501–502.
    - In the clean cut and the parts, video starts 21 ms after audio (the zh-en copy starts both at
      0).
    - *Fixed: the four stale `*_480p15*.mp4` drafts are gone from `output/` (F8).*
11. *Fixed: `video.yaml` has its `publish:` block (F9).*
12. *Fixed: README.md's chapter list and durations now match the re-stitch (F10).*

## Verified (final render)

Measured on 2026-10-18, 16:15–16:26 UTC, on the re-stitch written at 15:48–16:13 UTC
(`recheck/measured.json`, with ffprobe JSON, decode and ebur128 logs and per-check JSON in
`recheck/measured/`; scripts in `recheck/tools/`). The scene re-check measured the same values
independently (`recheck/measured_recheck.json`). The 19 output files other than `transcript.md` had
the same size and time before and after the checks, and their 15 text files the same SHA-256
(`recheck/measured/inputs_stat_*.txt`, `text_sha256_*.txt`); nothing in `output/` or `scenes/` was
written by them. The
first measurement (13:26–13:45 UTC, on the 12:26–12:51 stitch) is in `measured.json`;
what changed since is listed at the end of this section.

- **Deliverables:**

  | file | size | duration | frames | kbps total (video / audio) | integrated | LRA | true peak |
  |---|---|---|---|---|---|---|---|
  | `ac215-l04-flexible-workflow-ports.mp4` | 126.2 MB (126,224,911 B) | 1930.018 s (32:10.0) | 115,796 | 523.2 (334.5 / 177.1) | −16.1 LUFS | 2.4 LU | −2.8 dBTP |
  | `….zh-en.mp4` (to Bilibili) | 122.0 MB (121,965,225 B) | 1930.018 s | 115,797 | 505.6 (316.9 / 177.1) | −16.1 LUFS | 2.4 LU | −2.8 dBTP |
  | `…_part1.mp4` | 71.7 MB (71,738,719 B) | 1120.201 s (18:40.2) | 67,207 | 512.3 (323.8 / 176.9) | −16.1 LUFS | 2.4 LU | −2.8 dBTP |
  | `…_part2.mp4` | 54.5 MB (54,481,427 B) | 809.838 s (13:29.8) | 48,589 | 538.2 (349.3 / 177.2) | −16.1 LUFS | 2.3 LU | −2.8 dBTP |

  - **True peak:** every file is at −2.8 dBTP (sample peak −2.8 dBFS), so the target of −1.5 dBTP
    or lower is met in all four.
  - **Decode and format:** all four decode in full with 0 errors. All are 1920×1080 at 60 fps,
    H.264 High yuv420p, with AAC-LC audio at 48 kHz stereo, encoded with x264 at crf 27.
  - **The zh-en copy** is a second crf-27 encode, with the picture scaled to 1670×938 at x 125
    above the subtitle band (checked on 3 frames, `recheck/measured/zh_en_picture.json`). Its audio
    stream is bit-identical to the clean cut's (MD5 `356c3254…`).
  - **Part 1's audio** is bit-identical to the 12:26 stitch's (MD5 `18a9d5a7…`). Part 2's changed
    (`fa6c8038…` → `015bd974…`) because S13 was re-voiced.
  - **Video start:** in the clean cut and the parts, video starts 21 ms after audio; the zh-en copy
    starts both at 0.
- **Parts:**
  - 1120.201 + 809.838 = 1930.039 s, against the full cut's 1930.018 s (+0.021 s).
  - The per-scene frame counts add up to 115,796, which is 67,207 + 48,589.
  - Every scene's stitched file, its 1080p60 render and its events sidecar have the same frame
    count. Only S13's length changed (9,303 → 9,315 frames, 155.050 → 155.250 s); S06 and S10 kept
    theirs.
- **Subtitles:**

  | file | cues | part 1 / part 2 | shortest cue |
  |---|---|---|---|
  | `.srt` | 533 | 313 / 220 | 1.000 s |
  | `.zh.srt` | 463 | 272 / 191 | 1.081 s |
  | `.zh-en.srt` (and `.zh-en.ass`) | 553 | 325 / 228 | 1.129 s |

  - **Order and bounds:** in every file the cues are numbered in sequence, ordered, not
    overlapping, not empty and none under 0.8 s. They run from 0.000 to 1927.695 s, inside the
    runtime.
  - **Parts:** part 1 is the start of the full files. Part 2 is the full files shifted by
    1120.117 s, with the same text.
  - **Burned file:** the `.zh-en.ass` matches the `.zh-en.srt` cue for cue (within 5 ms), in the full
    file and both parts.
  - **Reading speed:** the English `.srt` peaks at 18.9 characters per second (median 14.6).
  - **Text changes against the 12:26 stitch** (`recheck/measured/cue_diff.json`): in `.srt`, only
    S13's two re-voiced sentences changed text. The cues between them (391–396) moved −0.04 to
    −0.05 s; from "Remove it." on they moved +0.206 s (401–402) and then +0.200 s (403–533). The zh
    files changed in 9 blocks: the eight pairs (F1) and S13.
- **Caption bounds in the burned copy** (`recheck/measured/caption_bounds.json`):
  - The `.ass` was rendered on 3,862 frames. All 553 cues sit at y 991–1062 and x 452–1467.
  - None has more than two rows, and none is above the band or clipped.
  - 552 cues are Chinese above English; the exception is cue 462 (26:38.910), deliberate (item 8
    above).
- **Chapters** (`recheck/measured/chapters_check.json`, `recheck/chapters_check.json`):
  - `chapters.txt` has 16 lines, with the titles and order of `video.yaml`. Part 1 has 9 chapters
    and part 2 has 7; part 2's clock starts at S10, which is 18:40.117 in the full video.
  - All 32 lines equal their scene's start, rounded to the millisecond and then floored, both by
    summed durations and by frame counts. S09 reads 16:45 (start 1004.999999 s) and S14 25:32
    (start 1532.000 s) (F3).
  - The README's chapter lists are copied verbatim from the three chapter files (after F10).
- **Narration:**
  - 156 SAY lines (4,379 words), each identical to the rendered `subs.json` text: part 1 has 2,581
    words and part 2 has 1,798.
  - Kokoro `af_heart` at speed 0.9 in all 16 scenes.
  - 1784.6 s of the runtime is voiced (92.5 %).
- **Ponders, recap and anchors:** as in gates 3 and 4. There are 606 `wait_until` call sites, with
  0 "anchor not found" warnings in the 16 render logs. In the re-stitch, the S13 and S14 ponders are
  0.2 s later than the times in gate 3's table (see the re-check). No cue of the three re-stitched
  subtitle files plays during any of the five timers, and the next cue starts within 4 ms of each
  timer's end; the silent windows in `.srt` run 6.8–8.8 s (`recheck/record/ponder_windows.json`).
- **Provenance** (from `ASSETS.md`):
  - **Real captures:**
    - Every terminal panel prints from sessions captured 2026-10-14, 00:29–00:40 UTC.
    - They ran on a fresh stand-in laptop: Docker Engine 29.8.2 in a dind container, user
      `student`, workspace `~/AC215`. Inside the images were Python 3.14.8 and uv 0.13.0.
    - Each README command was typed in README order, exactly as written. The extras are the `x-`
      files, tagged `extra` on screen.
    - Lines added by the QA fixes are asserted against their capture lines in the scene code (for
      example S06's and S08's folded inspect commands).
  - **Source quotes:** every code panel quotes `assets/source/` at the pinned commits:
    mega-pipeline `cc67f3b` and port_toy `d190c71`, plus `main` `c6bbc9b` and
    `pipenv-flexible-workflow` `32fcdb7` for comparison. The files were copied with `git show` and
    checked against their blob hashes.
  - **Recorded without a key:** there was no Google account or key, and every Google call stops at
    `DefaultCredentialsError`. Those runs are tagged "recorded without a key". The "with your key,
    look for" cards come from reading the code.
  - **Expected:** the C, D and E `--help` panels with a key are taken from their READMEs and tagged
    `expected`.
  - **Illustrations:** these are schematics tagged `illustration`, with no screenshots, logos, key
    content or real project id:
    - the GCP console: service account, roles, key and APIs;
    - the bucket and its prefixes;
    - the key going into `secrets/`;
    - the port_toy page;
    - Docker Hub.
  - **Stand-in key:** S03 and S09 use a 79-byte stand-in, tagged "stand-in file · not a real key"
    and never shown.
  - **Browser:** in the captures, `curl` sent the page's exact request. The page is drawn from that
    JSON, and the curl stand-in is never typed on screen.
- **Lecture slides:** 18 `lecture_ref` tags cite slides 7; 8, 15; 12; 13; 17–20; 23–24; 26 (twice);
  27; 29; 33; 34; 33–34; 35 (twice); 37–38; 37–40; and 42–43. No slide image or PDF page appears.
- **Skip chip:** S03's "cloned fresh? skip to 5:10" points 0.55 s before S04 (05:10.550), in the
  full cut and in part 1.
- **The two musts in the 1080p60 cut:** checked on frames for this record, at 04:38.0, 28:49.6 and
  28:51.0 (`writer/`), on the 12:26 stitch. S03 and S15 are the same renders in the re-stitch, where
  the S15 moments are 0.2 s later (28:49.8 and 28:51.2); those frames were not pulled again.
- **Changed against the 12:26 stitch** (old → new; `recheck/measured.json` `changed_vs_review`):
  - **Clean cut:** 1929.832 → 1930.018 s; 115,784 → 115,796 frames; 523.1 (334.3) → 523.2 (334.5)
    kbps; audio MD5 `889bb8f4…` → `356c3254…`.
  - **zh-en copy:** 121.9 → 122.0 MB; 1929.832 → 1930.018 s; 115,785 → 115,797 frames; 505.5
    (316.8) → 505.6 (316.9) kbps.
  - **Part 2:** 54.4 → 54.5 MB; 809.650 → 809.838 s; 48,577 → 48,589 frames; 538.0 (348.9 / 177.4)
    → 538.2 (349.3 / 177.2) kbps; audio MD5 `fa6c8038…` → `015bd974…`. Part 1: same numbers and
    audio; its video bytes changed with S06 (71,736,766 → 71,738,719 B).
  - **Parts sum:** 1929.851 → 1930.039 s (+0.019 → +0.021 s against the full cut).
  - **Cues:** `.srt` 531 → 533 (part 2: 218 → 220); `.zh-en.srt` and `.ass` 554 → 553 (parts
    327 / 227 → 325 / 228); `.zh.srt` 463, unchanged. Last cue end 1927.495 → 1927.695 s. The
    one-language exception moved from cue 463 to 462. Caption frames rendered 3,860 → 3,862.
  - **Chapters:** S09 16:44 → 16:45; S14 25:31.800 → 25:32.000 (line 25:31 → 25:32); S15 and S16
    start 0.2 s later (27:44.633, 29:59.733) with unchanged lines. "All but S09 match" is now "all
    32 lines match".
  - **Narration:** 4,377 → 4,379 words (part 2 1,796 → 1,798); voiced 1784.4 → 1784.6 s (92.5 %).
  - **Unchanged:** loudness, LRA and true peak in all four files; 0 decode errors; format; shortest
    cues; `.srt` reading speed; caption bounds; 606 anchors with 0 warnings; the voice in all 16
    scenes.

## Re-check after fix round 1 (re-stitched cut, 2026-10-18)

Two agents re-checked the re-stitched deliverables between 16:14 and 16:45 UTC (evidence in
`build/recheck/`; paths below start with `recheck/`). One read the changed scenes and items on
frames, audio and subtitle files (this section and F1–F9). The other re-measured all four
deliverables (`recheck/measured.json`; its numbers are under "Verified (final render)").
- **Frames:** they were cut from `output/…mp4` and `….zh-en.mp4` by exact frame number. The clean
  cut's video starts 21 ms after its audio, and the cut accounts for it. All of them were read,
  most as tiled montages (`m_*.png`).
- **Contact sheets:** one frame every 2 s from the zh-en copy, with the frame's own time burned in.
- **Nothing written:** nothing in `output/`, `scenes/` or git was written by the re-checks, and
  nothing was rendered.
- **Added for this record** (`recheck/record/`): the part files' frames at the three fixed moments
  ("The fixes are in the part files too", after F10), the audio envelope outside S13 against the
  final review's (gate 6) and the cues around the ponder timers ("Verified").

**Deliverables** (`recheck/measured_recheck.json`; ebur128 logs in `recheck/loudness/`, decode
logs in `recheck/decode/`). The sizes, durations, frames, bit rates and loudness equal those of
`recheck/measured.json` in "Verified (final render)".

- **Peaks:** every file's true peak (−2.8 dBTP) and sample peak (−2.8 dBFS) is under the −1.5 dBTP
  limit.
- **The zh-en copy's audio packets** are identical to the clean cut's (MD5 `356c3254…`).
- **Length:** the video is 12 frames (0.2 s) longer, all in S13. The container's duration grew by
  0.186 s.
- **Parts:** 67,207 + 48,589 = 115,796 frames.
- **Full decode:** all four files decode to the end with exit 0 and no error lines (zh-en 247 s,
  clean 217 s, part 1 126 s, part 2 92 s; `recheck/decode/summary.txt`).

**Scene starts and chapters** (`recheck/scene_starts.json`, `recheck/chapters_check.json`). Only
S13 changed length. S06 (137.133 s) and S10 (89.267 s) kept theirs, so S14–S16 start 0.2 s later
(S14 at 1532.000 s, S15 at 1664.633 s and S16 at 1799.733 s). All 16 chapter lines and both part
files match their scenes (F3). The ponder card in S13 is now at 24:24.12 (timer 24:24.72–24:30.72)
and the one in S14 at 27:00.83 (timer 27:01.43–27:07.43). S16's test-yourself block runs
31:14.53–31:55.21.

**Subtitles** (`recheck/subs/parts_check.json`): the same cue counts as in "Verified (final
render)": 533, 463 and 553 cues (parts 313 / 220, 272 / 191 and 325 / 228).

- **Order:** the cues are numbered in sequence, ordered and not overlapping. The last cue ends at
  1927.695 s.
- **Parts:** part 1 is the start of the full files. Part 2 is the full files shifted by 1120.117 s,
  with the same text.
- **Burned file:** the `.zh-en.ass` matches the `.zh-en.srt` cue for cue.
- **Reading speed:** the `.srt` peaks at 18.9 characters per second (median 14.6).

**The changed scenes, on the final frames.** The fixed moments were read on the clean cut and the
2-s contact sheets on the zh-en copy.
- **S06 `DockerShell`, 09:09.33–11:26.47. Verdict: fixed.**
  - **Times checked:**
    - 09:20.40 (no pill yet) and 09:20.95 (fading in);
    - 09:21.50, 09:22.53, and 09:23.00 with "run it from the component folder";
    - 09:26.73, and 09:30.50 with all the beat 0–1 tags;
    - 09:32.48, 09:32.75 (fading out), 09:33.03, and 09:34.03 (beat 2, nothing left);
    - the last frame, 11:26.45 (empty).
  - **The pill:** F4. No other tag in the panel touches it, and all of them read: "image name =
    container name", "run it from the component folder", "the key's path inside the container",
    "Docker Hub account" and "default".
  - **Lecture tags:** "Lecture 4 · slides 23–24" comes in at 09:50.92 with the bind-mount route. It
    becomes "slide 26" at 09:57.85 and leaves with the picture at 10:03.55–10:03.95. Nothing overlaps
    the top right (`recheck/S06/m_S06_lref_seq.png`; crops in `recheck/S06/m_S06_tr_crops.png`).
  - **Contact sheets** (`recheck/S06/sheets/zhen_S06_sheet_01.png` to `_05.png`): the burned
    subtitles stay in the band under the picture and cover no tag or command.
  - **Frames:** `recheck/S06/clean_S06_*.png`.
- **S10 `TwoComputers`, 18:40.12–20:09.38. Verdict: fixed.**
  - **Times checked:**
    - 19:01.42 (before the labels), 19:01.92 and 19:02.72;
    - 19:04.52, 19:05.02 (the labels' pulse peak) and 19:05.52;
    - 19:07.72 (the frame flash) and 19:09.63 (the loops' pulse peak);
    - 19:12.32, 19:12.67 (leaving) and 19:13.12 (gone);
    - the last frame, 20:09.37 (empty).
  - **The labels:** F5.
  - **Lecture tags:** "Lecture 4 · slide 33" arrives with the laptop outline at 18:56.38. It becomes
    "slide 34" at 19:12.43 and leaves with the network picture at 19:22.47–19:22.77
    (`recheck/S10/m_S10_seq.png`).
  - **Contact sheets** (`recheck/S10/sheets/zhen_S10_sheet_01.png` to `_03.png`): the subtitles
    cover nothing. There is one transient overlap, which is not from this round: the `d190c71`
    fly-over at 19:50.7–19:51.3 ("Open", item 6).
  - **Frames:** `recheck/S10/clean_S10_*.png`.
- **S13 `WhoCanReach`, 22:56.75–25:32.00. Verdict: fixed.**
  - **Beat 0 (re-voiced):** the cue "It reads 127.0.0.1" starts at 23:02.68 and its speech at
    23:02.90. The 127.0.0.1 flash (23:02.67–23:03.27, peak 23:02.97) is anchored on the sentence's
    start, so it plays on "It reads" and ends about as "127" begins (about 23:03.3 in the machine
    transcript). The 8090 flash (peak 23:07.22) and the 9100 flash (peak 23:08.23) land on their
    spoken numbers (`recheck/S13/m_S13_beat0.png`,
    `recheck/adversarial/frames/m_S13_beat0_flashes.png`). At their peaks, the enlarged numbers
    overlap the neighbouring characters for about 0.3 s, as they did before the fix round.
  - **Beat 3 (re-voiced):** "The mapping shows 0.0.0.0" starts at 23:39.76. `0.0.0.0:8091` turns
    yellow, with the IPv6 note, at 23:41.70–23:42.40. The door and `0.0.0.0` flash on "That means
    every address" at 23:43.83–23:44.53 (`recheck/S13/m_S13_beat3.png`).
  - **The still stretch:** F6.
  - **Lecture tags:** each is up with its picture.
    - "Lecture 4 · slide 35": 23:50.35–23:56.37.
    - "Lecture 4 · slides 33–34": 24:39.12–24:49.77. It comes in on "That's the second puzzle" and
      leaves at the next beat's first play.

    The last frame (25:31.98) is empty (`recheck/S13/m_S13_lref.png`).
  - **Contact sheets** (`recheck/S13/sheets/zhen_S13_sheet_01.png` to `_05.png`): the subtitles
    cover nothing. The burned cues show the new sentences at their times
    (`recheck/subs/frames/m_s13cues.png`).
  - **Cue sync and ASR:** F2.
  - **Frames:** `recheck/S13/clean_S13_*.png`.

**Review-bot items:** none were assigned to this re-check, and fix round 1 brought no new one. The
status of the eight earlier items in the re-stitched cut is under "Final-cut checks" (S10 bridge and
S13 `col_box` verified again on frames, the S03 chip by scene start, the other five on the 12:26
stitch only).

**Audio outside S13** (`recheck/record/rms_compare.json`): the 10 ms envelope of S01–S12 equals the
final review's exactly, S06 and S10 included; S14–S16's follows it 0.213 s later (gate 6).

**New findings:**
- README.md's chapter list and durations were out of step with the re-stitch ("Open", item 12);
  fixed with this record (F10).
- `script.md:238` says every scene is within ±15 % of its budget; S03 and S04 are not ("Open",
  item 4).
- Two transient or overlap nits, both older than fix round 1: the `d190c71` fly-over at
  19:50.7–19:51.3 and the S13 tag lying on its dashed box at 23:13.5 ("Open", item 6). The S13
  tracker caption scramble at 23:56.1 ("Open", item 7).

## Not claimed

- **No human has watched or listened to this cut.** The listening sign-off is waived for the series
  (gate 6).
  - The ASR round trip shows that a machine can understand the narration. It does not judge pacing,
    tone or how natural the voice sounds.
  - The whole-video ASR round trip ran on the 12:26 stitch. On the re-stitch, only S13's two
    re-voiced sentences were transcribed (F2); the rest of the audio was compared with the 12:26
    stitch's by its 10 ms envelope (gate 6), not transcribed again.
  - The "git" passages (02:50, 03:38–03:50 and 17:50) were judged from phonemes, not by ear.
- **Agents alone reviewed the Chinese and bilingual subtitles:** the QA subtitle watcher, the
  narration fixer, the verifiers and the final pairing check. No native-speaker human has read them.
  The pairing check found eight places still to fix ("Open", item 1). Fix round 1 fixed them, and
  the re-check read the eight new pairs in the files and on frames (F1); no human read them.
- **The visual review sampled the video.** It used one frame every 3 s plus targeted frames, and
  motion measured every 0.25 s on a 480×270 copy. It was not continuous playback. A defect shorter
  than 3 s between samples could be missed, such as the 0.35 s scroll-overs the verifiers saw on
  720p renders.
- **The part files were not visually sampled.** They were decoded and measured, and their
  subtitles were compared with the full files. The visual pass read the zh-en copy and measured
  motion on the clean cut; in part 1 only the S03 skip chip was checked on frames. After the
  re-stitch, three frames of the part files (the S06, S10 and S13 fixes) were compared with the full
  cut pixel for pixel ("The fixes are in the part files too", after F10); nothing else in the parts
  was looked at.
- **The QA and finishing fixes were verified on 480p and 720p preview renders, not one by one in
  this cut.** The 12:26 cut was checked only by the five checks above, and the re-stitch by the two
  re-checks, the small checks added for this record and the verifier pass on it. For this record,
  the two musts were also checked on frames, and the "Tutorial / 0" and "一个小疏漏" leftovers in the
  subtitle files.
- **The burned subtitles were not read back by text recognition.** They were compared with the
  subtitle files on 22 frames (pairing check) and 12 spot checks (visual pass).
- **Nothing that needs a Google account or key was run:**
  - `--download` with a key, `--transcribe`, `--generate`, `--synthesis`, `--translate` and
    `--upload`;
  - creating the service account, granting its roles and downloading its JSON key;
  - enabling the APIs in the console, or a successful `gcloud services enable` (only the no-account
    error was captured);
  - creating the bucket and uploading a recording;
  - the ElevenLabs bonus.

  The "with your key, look for" cards are not observed output.
- **Docker Hub steps not run:** `docker login` and `./docker-shell.sh prod` (the buildx multi-arch
  build and push). There is no account, and a push would publish an image; the video shows the
  command and the script lines it runs. The `dlops/*` images were pulled through a registry mirror
  (`ASSETS.md`).
- **Not run on the other platforms the narration mentions:** Windows (Git BASH, `winpty`, path
  mangling) and macOS (zsh, Docker Desktop). The captures ran on Linux, in a dind stand-in laptop.
  `git checkout -- .` and `uv add <package>` are shown as commands only.
- **No real browser:** the port_toy page was never opened in a browser. `curl` sent its exact
  request, and the page is drawn from the reply.
- **The re-check after fix round 1 sampled the changed scenes.** It read frames at the fixed
  moments and every 2 s of S06, S10 and S13 in the zh-en copy, and measured motion every 0.25 s in
  S13 only. Neither re-check re-ran the tag overlap scan, the 3-s visual pass or the whole-video
  ASR round trip on the re-stitched cut; the caption-bounds measurement was re-run (gate 6). The
  other 13 scenes are the same renders as before: their render logs predate fix round 1, and their
  frame counts are unchanged. Their stitched scene files in `build/stitch_h/` still carry their
  12:06–12:23 UTC times, so the re-stitch reused them; they were not compared byte for byte. Their
  English cues changed only by the 0.2 s shift after S13; their `.zh.srt` and `.zh-en.srt` cues
  also changed in the eight pairs (F1), in S03, S04, S08, S09, S15 and S16.
- **No one listened to the re-voiced S13 sentences.** Their check is the ASR transcript (F2).
- **The released files will be a different render.** Everything here is about the local stitches
  (12:26–12:51 UTC, and the re-stitch at 15:48–16:13 UTC).
  - The release workflow re-renders every scene with the pinned engine and writes
    `<id>.validation.json`, which does not exist yet.
  - The released files should be re-checked against these numbers: duration, frames, loudness, true
    peak, cue counts and chapters.
- **Later edits that change no pixel or sample of this stitch:** two edits postdate the 1080p60
  renders of the 12:26 stitch. One is the toolkit's `fmt_chapter` change (`23b0407`). The other is a
  docstring line in `scenes/s03_code.py:19` (5:09 → 5:10). Neither is in the 12:26 stitch. The
  re-stitch includes the `fmt_chapter` change (F3). S03 was not re-rendered, so its render still
  predates the docstring line, which changes no pixel.
