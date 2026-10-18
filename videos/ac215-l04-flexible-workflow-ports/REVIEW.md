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

This record was written on 2026-10-18. It is based on those checks' reports
(`build/final-review/report-*.md`), `measured.json`, the QA and finishing-pass outputs, `script.md`,
`BRIEF.md`, `ASSETS.md` and `SLIDES.md`. Verified facts and unclaimed reviews are kept in separate
sections.

**Conventions in this record:**
- **Times** are mm:ss in the full video (`output/ac215-l04-flexible-workflow-ports.mp4`, 32:09.8),
  except where marked *draft*. Draft times refer to the 480p QA draft. Later fixes made the video
  40.7 s longer, and scene starts moved by up to 39.5 s (S16 started at draft 29:20 and starts at
  29:59.5 in the final cut). So a draft time can be up to about 40 s earlier than the same moment in
  the final cut.
- **Cue numbers** say which file they come from: `.srt` (531 cues) or `.zh-en.srt` (554 cues).
- **Evidence paths** are relative to `build/final-review/`. That folder is git-ignored and exists
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
   - **Size:** 156 SAY lines and 4,377 words, identical to the 156 blocks spoken in the renders
     (`measured.json` `narration`). The voice is Kokoro `af_heart` at speed 0.9 in all 16 scenes.
     The pace is 136.1 wpm over the runtime and 147.2 wpm over voiced time.
   - **Anchors:** 606 `vo.wait_until` call sites and 3 `time_until` calls drive the reveals; 11 of
     them take a variable instead of a literal phrase. Every literal phrase is in script.md, and the
     16 render logs have 0 "anchor not found" warnings.
   - **Ear fixes:**
     - In the draft, "port toy" was heard as "port tie". A lexicon entry (`tˈoɪ`) fixed it, and in
       the final ASR the large model hears "port toy" (18:43).
     - The finishing pass re-voiced S03, S04, S10, S13 and S16 for its narration items.
   - **Caveat:** within a sentence, subtitle cues are cut by the number of characters displayed. So
     two S13 cues around spelled-out addresses are about 2 s off the voice ("Open", item 2).
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
6. **Measured checks** ✔. The numbers are under "Verified (final render)".
   - **Duration:** 32:09.8 (1929.832 s), inside the series' 25–35 min.
   - **Loudness:** −16.1 LUFS integrated in all four MP4s. True peak is −2.8 dBTP, under the build's
     −1.5 dBTP limit.
   - **Caption bounds:** all 554 burned-in cues sit inside the subtitle band, at y 991–1062 px (the
     band starts at y 938). None has more than two rows, and none is clipped.
   - **Music balance:** does not apply. L04, like L02 and L03, has no score: `video.yaml` has no
     `music:` key, and between voice clips the audio is digital silence (the ASR onset check's floor
     is −120 dBFS).
   - **Cue sync:** this is the one measured weakness ("Open", item 2).

   **Human review:** the series waiver below stands in for a listening sign-off.

   Listening sign-off: waived by Conny for the AC215 series (Explainer_Videos#29, 2026-10-15): 「不需要，我现在对视频质量很满意的」 — no human listened to this cut; the ASR round trip below is the substitute.

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
  - The narration line starts at 28:44.60 (`.srt` cue 477).
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
    `.zh-en.srt` #202/#203 paired correctly.
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
  cues early or late. This is still in the final cut ("Open", item 2).

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
  (checked for this record).
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
- **Side findings:**
  - The S02 box crossing ("Open", item 6).
  - The S09 chapter mark ("Open", item 3).

**ASR round trip, the substitute for a listen** (`report-asr.md`; `asr.json`, `align_spoken.json`,
`clips_large-v3-turbo.json`, `onsets_rms*.json`).
- **Raw comparison:** faster-whisper `base.en` transcribed the clean cut's audio, which was compared
  with the 531 cues of `.srt`. 231 cues differ in their raw wording. Most of these are written
  versus spoken forms (digits, "-p" said "dash p", "/app" said "slash app") and words that shift
  across a cue boundary.
- **Against the spoken text:** aligned with the text Kokoro was given (4,422 words), 68 spans needed
  judging. All 68 were judged, and the doubtful ones were transcribed again with `large-v3-turbo`
  (43 clips, 127 cues).
- **Real mispronunciations or swallowed words: none.**
  - **Cues 407–409** (24:17.7–24:23.7, "Ponder this…"): `base.en` returned nothing here. The
    speech is there and in sync, and the large model hears it word for word.
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
  - The known winpty case now pairs correctly: #202 at 11:16.47 and #203 at 11:21.31.
- **Found:** three neighbouring pairs swap meaning, and five are one clause off ("Open", item 1).
  Seven word-level drifts need no change.

**Measured** (`report-measured.md`; `measured.json`, scripts and logs in `measured/`). The numbers
are under "Verified (final render)".

## Open in the final cut (for the coordinator)

1. **Bilingual cues that swap or lag meaning, in the copy that goes to Bilibili.** In each case the
   Chinese puts a condition, time or place clause first, and the builder pairs zh and en clause by
   clause.
   - **Meaning swaps between neighbouring cues:**
     - #108/#109 at 05:43.48–05:49.93 (S04, `g1.yaml:167`)
     - #542/#543 at 31:23.97–31:28.85 (S16, `g2.yaml:376`)
     - #551/#552 at 31:55.25–32:01.61 (S16, `g2.yaml:389`)
   - **One clause off:**
     - #91–93 at 04:42.93–04:52.13 (S03, `g1:148`)
     - #105–107 at 05:32.23–05:43.24 (S04, `g1:164`)
     - #286/#287 at 16:26.92–16:30.91 (S08, `g1:439`)
     - #324/#325 at 18:25.73–18:31.22 (S09, `g1:505`)
     - #515/#516 at 29:47.23–29:53.59 (S15, `g2:315`, minor)
   - **Fix:** put those zh sentences in the English clause order (`report-pairs.md` gives a target
     wording for each), rebuild the subtitles and re-burn the zh-en copy. This needs no re-render
     and no new audio. The fix is not made because the check ran after the stitch; the coordinator
     decides.
2. **Mid-sentence cue timing** (shared `explainer/subtitles.py`; QA's open ASR should).
   - **Two clear cases in S13, in both tracks:**
     - `.srt` cue 398 at 23:42.14 starts 2.28 s before its speech, while "zero dot zero dot zero" is
       still being said.
     - Cue 390 at 23:05.51 shows 2.07 s after its speech starts.
   - **Marginal cases, about 1.0–1.5 s:**
     - Cue up before its speech starts, in `.srt`: cues 465 (28:06.34), 378 (22:20.94), 356
       (20:57.87), 492 (29:43.45) and 363 (21:27.27).
     - The same, in the burned track only: zh-en 527 (30:29.48), 418 (24:02.38) and 201
       (11:12.33).
     - Speech before its cue: cue 120 (06:36.96) by 1.36 s, and cue 358 (21:09.38) by 0.99 s.
   - **Fix options:** weight the English cue split by the spoken form, as `_spoken_weights` already
     does for Chinese, or add word marks at "every address" and "127.0.0.1" in `s13_reach`. Either
     way the subtitles need re-timing and re-burning, but no new audio. Evidence:
     `frames/cue398_t1423.00.png`, `frames/cue390_t1384.50.png` and `onsets_rms*.json`.
3. **S09's chapter mark is 1 s early.**
   - `chapters.txt` and `chapters_part1.txt` say 16:44, but S09's first frame (60300) is at
     1005.000 s, which is 16:45.000. The summed float, 1004.999999 s, was truncated, so the chapter
     lands on S08's last second (`measured/frames/chapter_S09_t1004.0.png`).
   - `fmt_chapter` now rounds to the millisecond before flooring (`23b0407`, committed after this
     stitch). The chapter files, and the README's copy of them, read 16:44 until they are
     regenerated.
4. **Narration over its budget.** 4,377 words against BRIEF.md's 3,900–4,300, so 77 over.
   - S03 (332 words against 280, +18.6 %) and S04 (242 against 210, +15.2 %) are outside ±15 %.
   - Both grew in the finishing pass, with the S03 warning and the S04 bucket sentence.
   - The runtime, 32:09.8, is inside 25–35 min.
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
   - **09:21–09:31, S06:** the pill "the folder you're in" after `$(pwd)` grazes lines 7 and 9 by
     2–4 px (`visual/crops/0930_code_tags.jpg`).
   - **19:03–19:12, S10:** the yellow "9100" labels touch the localhost loop's arrowhead
     (`visual/crops/1906_9100_labels.jpg`).
   - **Overlaps while something moves:**
     - 01:45 (S02): a highlighted label touches its card's edge.
     - 07:36.0 (S05): a role badge comes out from behind the console card (0.3 s).
     - 13:15 (S07): "/app/cli.py" crosses the terminal border while it grows (0.6 s).
     - 28:09.6–28:11.1 (S15): the intended fly-in of the flags passes over the YAML.
   - **24:33.25–24:38.50, S13:** 5.25 s with almost nothing moving (one small dot at 24:36), outside
     the ponder timers. That is borderline against "something moves every ~4 s".
   - **Wrapped rows in S15:** `docker compose ps` and `ps -a` show "process / or" (from about 28:52
     and 29:43), as described under the nits above.
   - **Seen by verifiers on 720p renders, not in the 3 s samples:**
     - Rows scroll over a terminal's title bar for about 0.35 s (about 19:52 and 20:43; shared
       `_make_room`).
     - S09's fix card flashes solid yellow for about 0.3 s at "after the fix" (about 18:03).
     - S16's beat 2 runs about 1.5 s behind "Compose recreates only the gateway" (`up -d` is typed
       at about 30:30). QA did not flag it, and a fix means shortening the extra `git diff`.
7. **Shared-code leftovers** (toolkit PRs, outside this episode's files):
   - `Terminal._make_room` scroll travel and `line_bar` height (`explainer/devops.py`).
   - `_cut_penalty` (`.srt` cue 17, "Tutorial / 0") and `_merge_short` (`.zh-en.srt` #140,
     "一个小疏漏"), in `explainer/subtitles.py`.
   - Cue timing by displayed characters (item 2).
   - `common.second_terminal()`: S06's and S08's second terminals switch to the component folder's
     prompt with only the caption "new terminal: cd here first", and no `cd` is typed. That is the
     pattern behind the S15 must. QA did not flag S06 or S08, and the S15 verifier passed it on to
     the toolkit owner.
   - `caption_extra` scrambles a tracker caption for about 0.3 s while it changes (S14).
8. **Left on purpose:**
   - S03's `rm -r */secrets` needs a new capture (see the nits above).
   - `.zh-en.srt` cue 463 (26:38.71) shows "Empty reply from server" in both rows. Glossary rule A1
     keeps terminal text verbatim (`measured/frames/cue463_emptyreply_t1599.5.png`).
9. **Docs out of step with the cut** (nothing on screen):
   - `script.md:236` still says 4,297 words.
   - `BRIEF.md:324` and `:534` still give ponder 1 as "Cloud Speech Client / transcribe". script.md,
     the scene and the frame say Agent Platform User and `generate_text`.
   - script.md's SHOW lines name only S13's two slide tags, although the scene code has 18.
   - `QA_FOLLOWUPS.md` still heads the S11 underline item "OPEN until checked on frames" and lists
     the S03 skip chip as open for the final review. The final tag check closed both; the S02 box
     crossing it also lists stays a nit (item 6).
10. **Small facts, no action proposed:**
    - The fastest English row in the burned track is `.zh-en.srt` cue 287 (16:28.47): 49 characters
      in 2.43 s, 20.1 characters per second. This leaves out cues 18–20, 480–481 and 502–503,
      where one English sentence stays up under two or three shorter Chinese cues; read across the
      repeats, those run at 13.6–15.6 characters per second.
    - In the clean cut and the parts, video starts 21 ms after audio (the zh-en copy starts both at
      0).
    - Four stale `*_480p15*.mp4` drafts from 2026-10-17 sit in `output/`. The release workflow picks
      files by exact name.
11. **Publishing prerequisite:** `video.yaml` has no `publish:` block (`title_zh`,
    `description_zh`, `tags_zh`, `tid: 231`). The release workflow refuses to start without it.

## Verified (final render)

Measured on 2026-10-18, 13:26–13:45 UTC, on the stitch written at 12:26–12:51 UTC (`measured.json`,
with ffprobe JSON, decode and ebur128 logs in `measured/`). Nothing in `output/` or `scenes/` was
written by the checks.

- **Deliverables:**

  | file | size | duration | frames | kbps total (video / audio) | integrated | LRA | true peak |
  |---|---|---|---|---|---|---|---|
  | `ac215-l04-flexible-workflow-ports.mp4` | 126.2 MB | 1929.832 s (32:09.8) | 115,784 | 523.1 (334.3 / 177.1) | −16.1 LUFS | 2.4 LU | −2.8 dBTP |
  | `….zh-en.mp4` (to Bilibili) | 121.9 MB | 1929.832 s | 115,785 | 505.5 (316.8 / 177.1) | −16.1 LUFS | 2.4 LU | −2.8 dBTP |
  | `…_part1.mp4` | 71.7 MB | 1120.201 s (18:40.2) | 67,207 | 512.3 (323.8 / 176.9) | −16.1 LUFS | 2.4 LU | −2.8 dBTP |
  | `…_part2.mp4` | 54.4 MB | 809.650 s (13:29.7) | 48,577 | 538.0 (348.9 / 177.4) | −16.1 LUFS | 2.3 LU | −2.8 dBTP |

  - **Decode and format:** all four decode in full with 0 errors. All are 1920×1080 at 60 fps,
    H.264 High yuv420p, with AAC-LC audio at 48 kHz stereo, encoded with x264 at crf 27.
  - **The zh-en copy** is a second crf-27 encode, with the picture scaled to 1670×938 above the
    subtitle band. Its audio stream is bit-identical to the clean cut's (MD5 `889bb8f4…`).
- **Parts:**
  - 1120.201 + 809.650 = 1929.851 s, against the full cut's 1929.832 s (+0.019 s).
  - The per-scene frame counts add up to 115,784, which is 67,207 + 48,577.
  - Every sidecar duration equals its stitched scene.
- **Subtitles:**

  | file | cues | part 1 / part 2 | shortest cue |
  |---|---|---|---|
  | `.srt` | 531 | 313 / 218 | 1.000 s |
  | `.zh.srt` | 463 | 272 / 191 | 1.081 s |
  | `.zh-en.srt` (and `.zh-en.ass`) | 554 | 327 / 227 | 1.129 s |

  - **Order and bounds:** in every file the cues are numbered in sequence, ordered, not
    overlapping and not empty. They run from 0.000 to 1927.495 s, inside the runtime.
  - **Parts:** part 1 is the start of the full files. Part 2 is the full files shifted by
    1120.117 s, with the same text.
  - **Burned file:** the `.zh-en.ass` matches the `.zh-en.srt` cue for cue.
  - **Reading speed:** the English `.srt` peaks at 18.9 characters per second (median 14.6).
- **Caption bounds in the burned copy** (`measured/caption_bounds.json`):
  - The `.ass` was rendered on 3,860 frames. All 554 cues sit at y 991–1062 and x 452–1467.
  - None has more than two rows, and none is above the band or clipped.
  - 553 cues are Chinese above English; the exception is cue 463, deliberate (item 8 above).
- **Chapters:**
  - `chapters.txt` has 16 lines, with the titles and order of `video.yaml`. Part 1 has 9 chapters
    and part 2 has 7; part 2's clock starts at S10, which is 18:40.117 in the full video.
  - Every start matches the summed scene durations except S09 ("Open", item 3).
  - The README's chapter lists are copied verbatim from the three chapter files.
- **Narration:**
  - 156 SAY lines (4,377 words), each identical to the rendered `subs.json` text: part 1 has 2,581
    words and part 2 has 1,796.
  - Kokoro `af_heart` at speed 0.9 in all 16 scenes.
  - 1784.4 s of the runtime is voiced (92.5 %).
- **Ponders, recap and anchors:** as in gates 3 and 4. The ponder timers have no cue during them.
  There are 606 `wait_until` call sites, with 0 "anchor not found" warnings.
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
  28:51.0 (`writer/`).

## Not claimed

- **No human has watched or listened to this cut.** The listening sign-off is waived for the series
  (gate 6).
  - The ASR round trip shows that a machine can understand the narration. It does not judge pacing,
    tone or how natural the voice sounds.
  - The "git" passages (02:50, 03:38–03:50 and 17:50) were judged from phonemes, not by ear.
- **Agents alone reviewed the Chinese and bilingual subtitles:** the QA subtitle watcher, the
  narration fixer, the verifiers and the final pairing check. No native-speaker human has read them.
  The pairing check found eight places still to fix ("Open", item 1).
- **The visual review sampled the video.** It used one frame every 3 s plus targeted frames, and
  motion measured every 0.25 s on a 480×270 copy. It was not continuous playback. A defect shorter
  than 3 s between samples could be missed, such as the 0.35 s scroll-overs the verifiers saw on
  720p renders.
- **The part files were not visually sampled.** They were decoded and measured, and their
  subtitles were compared with the full files. The visual pass read the zh-en copy and measured
  motion on the clean cut; in part 1 only the S03 skip chip was checked on frames.
- **The QA and finishing fixes were verified on 480p and 720p preview renders, not one by one in
  this cut.** The 1080p60 cut was checked only by the five checks above. For this record, the two
  musts were also checked on frames, and the "Tutorial / 0" and "一个小疏漏" leftovers in the
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
- **The released files will be a different render.** Everything here is about this local stitch
  (12:26–12:51 UTC).
  - The release workflow re-renders every scene with the pinned engine and writes
    `<id>.validation.json`, which does not exist yet.
  - The released files should be re-checked against these numbers: duration, frames, loudness, true
    peak, cue counts and chapters.
- **Later edits that change no pixel or sample of this stitch:** two edits postdate the 1080p60
  renders. One is the toolkit's `fmt_chapter` change (`23b0407`). The other is a docstring line in
  `scenes/s03_code.py:19` (5:09 → 5:10). Neither is in this stitch.
