# Review record: AC215 · Lecture 4 — Containers II-b: build or pull, ports and Compose

Follow-along of [dlops-io/mega-pipeline](https://github.com/dlops-io/mega-pipeline)
(`flexible-workflow` @ `cc67f3b`) and [dlops-io/port_toy](https://github.com/dlops-io/port_toy)
(`main` @ `d190c71`). The issue of record is #37. The work is in the series draft PR #29 and moves
to `episode/ac215-l04-flexible-workflow-ports` for the release. Claude Code cloud sessions (Claude)
produced the episode:

- terminal captures on 2026-10-14, 00:29–00:40 UTC (ASSETS.md);
- whole-video QA on the 480p draft of 2026-10-17, with its fixers and verifiers (output saved
  2026-10-18 04:21 UTC, `/root/ac215-backup/tasks/wjgb45ot6.output`);
- a finishing pass on 2026-10-18: a first run that applied nothing, a scoped re-run of the text items
  and S01–S15 (reports saved 09:35 UTC), a separate run for S16 after a container restart cut the
  re-run (10:01 UTC), and a run on two review-bot findings (10:23 UTC);
- 1080p60 renders of all 16 scenes. After a second container restart S15 and S16 were rendered
  again, and S03 once more, for its skip chip only (5:09 → 5:10). The stitch finished at 12:51 UTC
  on 2026-10-18;
- the final-cut measurement, finished 2026-10-18 13:41:29 UTC (`build/final-review/measured.json`).

This record was written on 2026-10-18 after that measurement. Verified facts and unclaimed reviews
are kept in separate sections.

**The final-cut checks left no reports.** Five agent checks of the final cut were to write
`build/final-review/report-tags.md`, `report-asr.md`, `report-visual.md`, `report-pairs.md` and
`report-measured.md`. None of the five files exists (looked for at 13:42 and at 13:56 UTC, on the
whole machine). Each missing report counts here as a check that produced nothing. The measuring
check did leave its data, `measured.json`: this record takes its numbers from that file and from
the output files themselves. The other four checks left working files (frames, transcripts, scans,
running notes) and no verdict. This record claims nothing from them; what they point at is listed
under "Open" as leads.

Times are mm:ss in the full video (`output/ac215-l04-flexible-workflow-ports.mp4`, 32:09.8), except
where marked *draft*. Draft times refer to the 480p QA draft, which ran 31:29.1 (1889.144 s in
`build/qa/scenes.json`). Later fixes lengthened the video by 40.7 s. Scene starts moved later by
1.0 s (S02) up to 39.5 s (S16), so a draft time sits up to about 40 s earlier than the same moment
in the final cut. Evidence files named below are in `build/final-review/` unless the path says
otherwise. That folder is git-ignored and exists only in the producing session.

## Content gates (AGENTS.md)

1. **Hook** ✔. S01 opens on a broken thing, not a value proposition.
   - `./docker-shell.sh run`, on a laptop that never built `generate_text`, pulls an image from
     Docker Hub. Inside, Python says 3.8.17 and the Gemini library won't import, although the repo's
     Dockerfile says 3.14. "Where did it come from?" is asked at 00:25.0.
   - A second puzzle follows from port_toy: port 9200 doesn't answer the laptop, but another
     container gets a reply by name. "Two puzzles…" names both at 00:38.8–00:46.6 (`measured.json`,
     `content_gates.hook`).
   - S08 pays off the first puzzle (ponder 3 and the opened box), S13 the second (ponder 4).
2. **Intuition before formalism, with an animated mechanism per core idea** ✔ (on the draft).
   BRIEF.md's eight set pieces are animated before the commands they explain, as script.md's SHOW
   lines specify:
   - V1, recipe card or frozen meal: build or pull (S01 teaser, S02, S08: the box opens on
     2025-02-18, Python 3.8.17, pipenv, root);
   - V2, three piles at a branch switch (S03);
   - V3, three gates: who, may, switched on (S05; callback in S07);
   - V4, the `docker-shell.sh` switchboard (S06, S08, S09);
   - V5, two windows into the laptop: the two bind mounts and the env var (S06; S09's contrast,
     where `COPY` carries the key into a layer);
   - V6, little computers on one network, with the phone book (S10, S13);
   - V7, doors, rooms and tickets: published, listening and source ports (S11–S14);
   - V8, commands become one file: the by-hand flags fly to their Compose keys (S15, S16).

   The two director watchers read every draft contact sheet against script.md, and the two newcomer
   watchers watched as target viewers. On the final cut this gate rests on that QA, because the
   final visual pass left no report.
3. **Pause-and-ponder moments and a recap** ⚠ partly met.
   - **Ponders:** five cards with silent timers: S05 08:45.8 (8 s), S07 12:35.9 (6 s), S08 15:07.6
     (8 s), S13 24:23.9 (6 s) and S14 27:00.6 (6 s). No subtitle cue falls inside a timer, and each
     answer starts as its timer ends (`measured.json`, `ponder`; frames
     `measured/frames/ponder*_*.png`).
   - **Rate:** that is one ponder every 6.4 min. AGENTS.md aims for one every 2 min, about 16 for
     this length. The first comes 525.8 s in, and the longest gap is 556.3 s (15:07.6 → 24:23.9).
   - **Series rule:** BRIEF.md and the ac215-video skill (step 3) fix 3–5 ponders per lecture, so
     the series count is met. Separately, 21 SAY lines tell the viewer to pause and do a README step,
     from 02:55.9 to 31:12.6 (`measured.json`, `pause_prompts`).
   - **Recap:** S16's "Test yourself" runs 31:14.3–31:55.0. It asks five questions, with "pause after
     each question" spoken and on screen and Q1–Q3 tagged "part 1". The answers are in
     `exercises.md`, not narrated. There is no spoken summary of the content. Part 1 (S01–S09, also
     published on its own) ends on its clean-up card, with no recap of its own. The L05 teaser closes
     the video (31:55.3–32:07.5).
   - **Open question for Conny** (the same as L03's): does the series format, five ponders and a
     recap made of questions, satisfy this gate for AC215?
4. **Narration written for the ear, with word-anchored cues** ✔.
   - **Spoken style:** following script.md's conventions, commands, flags and paths are spoken in
     words ("dash p", "slash app"), versions are said "at the time of recording", and no sentence
     opens with a command. Kokoro lexicon entries cover file names, ports and addresses. The draft
     ASR watcher heard "port toy" as "port tie", so the QA text fixer added `"port toy"` →
     `pˈɔːɹt tˈoɪ` to the shared `explainer/lexicon.yaml`.
   - **Size:** 156 SAY lines with 4,377 words. The 156 voice blocks in the renders carry exactly that
     text, in order (`measured.json`, `narration`). The pace is 136.1 wpm over the runtime and
     147.2 wpm over the 1,784.4 voiced seconds (92.5 % of the runtime).
   - **Anchors:** the scene code has 606 `vo.wait_until` call sites and 3 time-based waits. Every
     literal anchor phrase occurs in script.md, and the 1080p render logs hold no "anchor not found"
     warning (`measured.json`, `anchors` and `content_gates`).
   - **Length:** 4,377 words is 77 over BRIEF.md's 3,900–4,300. S03 (+18.6 %) and S04 (+15.2 %) are
     outside their ±15 % budgets; QA fixes lengthened both (the copy-out warning, the bucket's
     your-turn). script.md's header still states 4,297.
   - **Not re-measured here:** cue timing inside a sentence. On the draft, the ASR watcher found cues
     up to 2.5 s late or 1.7 s early in 7 places where the spoken form is much longer than the shown
     one (spelled-out IP addresses, flags). That is a toolkit item (Open, item 5), and the final ASR
     check left no report.
5. **Simulated-target-viewer QA over the full draft** ✔. Seven watchers reviewed the 480p draft,
   two of them simulated target viewers. They reported 62 timestamped findings: 2 must, 26 should
   and 34 nit. Both musts are fixed, and this record checked both in the final cut (below). 22 of
   the 26 shoulds and 30 of the 34 nits are fixed. The rest are listed with reasons under
   "Whole-video QA".
6. **Measured checks** ✔ for the four MP4s; the ASR substitute ⚠ has no result for this cut.
   - **Numbers:** see "Verified (final render)". The cut runs 32:09.8 at 1080p60. All four files
     measure −16.1 LUFS integrated and −2.8 dBTP true peak, against the build's −1.5 dBTP target.
     In the burned-in copy the subtitles stay inside their band.
   - **Music balance does not apply.** The series has no music bed: `video.yaml` has no `music:`
     block, and the build takes the narration-only loudnorm path (`measured.json`, notes).
   - **Human review:** the series waiver below stands in for a listening sign-off.

   Listening sign-off: waived by Conny for the AC215 series (Explainer_Videos#29, 2026-10-15): 「不需要，我现在对视频质量很满意的」 — no human listened to this cut; the ASR round trip below is the substitute.

   - **The ASR round trip of this cut has no result:** `report-asr.md` does not exist. See
     "Final-cut checks".

## Whole-video QA (480p draft; times are draft times)

**Watchers and findings.** Seven watchers reviewed the draft (`wjgb45ot6.output`, key `result`).
Each read the contact sheets against `script.md` and the English `.srt` and pulled exact frames
where a tile was doubtful.

| watcher | lens | must | should | nit |
|---|---|---|---|---|
| director, part 1 (S01–S09) | facts, commands vs captures and sources, tracker, sync | 0 | 6 | 8 |
| newcomer, part 1 | simulated target viewer, README and clone open | 1 | 6 | 8 |
| director, part 2 (S10–S16) | the same, plus `explainer.check` on all seven scenes | 0 | 5 | 1 |
| newcomer, part 2 | simulated target viewer | 1 | 3 | 6 |
| subtitles (zh, zh-en, en) | glossary, line and cue breaks, reading speed, pairing | 0 | 4 | 10 |
| follow-ups (`QA_FOLLOWUPS.md`) | the logged review-bot items | 0 | 1 | 0 |
| ASR (base.en, large-v3-turbo) | mishearings, cue sync | 0 | 1 | 1 |
| **total** | | **2** | **26** | **34** |

Six findings target shared code (4 should, 2 nit). Some problems were reported by two watchers and
are counted twice: S03's "which you wrote in lecture 3", S16's "Step 3", the S07/S11 terminal
scroll, S07's `git diff` excerpt, S09's clean-up `docker images`, and S13's capitalised commands.
Apart from the findings, the directors found the commands, README and source line numbers and
terminal outputs consistent with the READMEs, sources and captures.

**The two musts, and how they were fixed.**

- *Draft 04:30, S03 (newcomer, part 1):* the warning to copy out the lecture 3 `Dockerfile`,
  `pyproject.toml` and `uv.lock` came 2 s after "Pause and switch your own clone". A viewer who
  paused there would lose those ignored files for good: the switch replaces them, and `git stash -u`
  does not save ignored files. Fixed in two steps:
  - **QA's S03 fixer:** the your-turn card opens with "first: copy out your lecture 3 Dockerfile,
    pyproject.toml, uv.lock · the switch replaces them" (tagged `extra`), flashed on "Pause and
    switch".
  - **The finishing pass** put the warning into the narration before the pause: "…Before you switch
    your own clone, copy out any lecture 3 Dockerfile, pyproject.toml and uv.lock you want to keep:
    the switch replaces them. Pause and switch." (zh to match). S03 grew by about 10 s. The scene
    agent added a flash on "copy out any", so the card no longer stands still for 7.3 s (now 3.2 s
    at most).
  - **In the final cut:** the warning's cue starts at 04:31.1 (`.srt` #84), before "Pause and
    switch." at 04:41.5.
- *Draft 28:05, S15 (newcomer, part 2):* the narration said "In a second terminal, cd into port toy
  first", but no `cd` was typed. The prompt jumped from `~$` to `~/AC215/port_toy$`.
  - **QA's S15 fixer** types `cd ~/AC215/port_toy` and flashes the new prompt (`CD_TOY`, asserted
    against the prompt). Its verifier saw this on fresh 720p frames.
  - **In the final cut** the line is spoken at 28:44.6. The visual pass's own frame at 28:51.0
    (`visual/frames3s/f_0578.jpg`, read for this record) shows the typed `cd` and the new prompt.
  - The same silent prompt switch remains in `common.second_terminal()`, which S06 and S08 use
    (Open, item 5).

**The shoulds: 22 fixed.**

- **Narration and facts (8 findings):**
  - "which you wrote in lecture 3" → "which this branch commits" (S03, two watchers; final 03:06.4);
  - "Prod is optional: after the fix, run it only if your team publishes.", with the tracker reading
    "Publish the container (optional)" (S09; final 18:01.8);
  - the ambiguous "Step 3" → "Next, the README says to repeat the port experiments in the file."
    (S16, two watchers; final 30:22.1);
  - a definition of Compose: "Step 4: Docker Compose, which builds and starts the whole app from one
    YAML file." (S15; final 27:44.4);
  - S16's `--build` sentence reordered to match the picture (final 30:40.3);
  - S07's ElevenLabs chip now shows the real `cli_11.py` line 30, then a separate fix chip.
- **Follow-along and picture (11):**
  - S04 gains a your-turn card for creating the bucket and uploading `input-<something>.mp3`, and
    the narration says "Bucket names are global: pick a unique one. Pause and create yours." (final
    06:44.3);
  - S06's chmod/winpty hint appears at "Pause and run it";
  - S06's folded `docker inspect` no longer breaks inside its quotes;
  - S06's strip keeps the command with its output;
  - S06's "Docker Hub account" tag no longer covers line 14's comment;
  - S07's `git diff` marks its cut with "…" and "gcp_project and bucket_name edited too";
  - S08's extra inspect is typed as the real captured command;
  - S10's `ls gateway processor` and its output are readable together;
  - S14's first your-turn card is fully up for about 4.3 s, and its closing card for about 3.2 s;
  - S14's `docker network rm toynet` stays readable for about 3.8 s;
  - S15's yellow box around `127.0.0.1:8090->9100/tcp` no longer vanishes for 1.9 s.
- **Subtitles (3):** "the input device is not a TTY" is no longer split (S06); a zh cue no longer
  cuts a subject from its verb (S03); a bilingual cue no longer ends on "push 到" (S08).

**The nits: 30 fixed.** Among them: S01's container session now has a TEAL container frame; S05's
tracker now uses the README's step numbers; S08's stale box turns RED; S09's cloud VM is BLUE; S09's
clean-up `docker images` adds the pulled `dlops/*` rows; S10's caption says both boxes could use 9100, so the lit 9100 no longer reads as the processor's
port;
S11 explains why an identical `COPY` line is rebuilt; S13 shows a tag for "subnet" and now says
"address range" aloud; S16 explains the 10 s waits and tags Q1–Q3 "part 1"; the English line
shows terminal text as printed (`en_display`); and the S03 skip chip names a time.

**Left open from QA, with the reasons.**

- **Shoulds (4), all in shared toolkit code (`explainer/`), for a separate toolkit PR:**
  - **Terminal scroll** (S07, draft 12:07; S11, draft 20:10; one problem): rows leaving a terminal
    slide up by the whole overflow and cross what sits above it for about 0.35 s
    (`Terminal._make_room`). S07 and S10 now avoid it locally; the other scenes still show it.
  - **"Tutorial / 0"** (S01): the English `.srt` still breaks the name across lines (final `.srt`
    #17, 01:00.7).
  - **Cue timing inside a sentence** follows the shown characters, not the speech: on the draft,
    7 places were up to 2.5 s late or 1.7 s early. Not re-measured on the final cut.
- **Nits (4):**
  - S03, draft 04:50: there is no command or pause for deleting each component's old `secrets/`
    folder. Adding one needs a new capture taken after captures 12–13, because S09's stowaway-key
    demo relies on the old key still being there.
  - Mid-word wraps: fixed in S13. S15's `docker compose ps` and `ps -a` tables still print with the
    65-column wrap (`s15_compose.py:744`, `:889`) that split "process / or" in the draft.
  - Shared: the code-panel highlight bars are taller than the line pitch (`line_bar`). S06's visible
    case was fixed by moving its tag.
  - Shared: the bilingual track merges the label "一个小疏漏" (A small slip:) into the previous
    sentence's cue (S05, draft 07:23). No zh rewrite avoids it.

**Process.**

- **QA (36 agents):** the seven watchers; one fixer per scene with findings (14 scenes) plus one
  narration/subtitle fixer; then a skeptical verifier per scene, on fresh 720p frames and with
  `explainer.check`.
- **The verifiers found and fixed incomplete fixes:**
  - S04's card came up after 8.7 s of silence and lacked "after gcloud login";
  - S07's old output slid through the second terminal;
  - S13's laptop-side error was still cut mid-phrase;
  - S14's cards had a messy half-faded frame right after "Pause";
  - S15's new Compose sentence left the screen still for 4.1 s;
  - S16's `git diff` was readable for under 1 s (now about 2.8 s).

  They also corrected two fixer claims: S04's card timing, and S06's caption, which is up for 4.3 s,
  not 5.5 s.
- **The finishing pass** (2026-10-18) applied the items QA had left in files its fixers could not
  edit, plus the lecture-slide items that SLIDES.md §5 marks "do":
  - **The first run** (`wf5a69r10.output`) changed nothing. Its agents took a status question about
    L02/L03, which reached them mid-run, as their task.
  - **A scoped re-run** (`/root/ac215-backup/args/l04scoped/`) did the 12 text items in script.md,
    BRIEF.md and `i18n/zh/`:
    - the S03 warning, and "the commit we recorded" (final 02:58.7);
    - S04's bucket sentence;
    - S10's bridge, "The lecture calls this a network namespace…" (final 19:06.2);
    - S13's "from toynet's own address range, its subnet." (final 24:55.9);
    - S16's "To test yourself, pause after each question." (final 31:14.3);
    - the SHOW and BRIEF sync for S05, S07, S08, S09 and S15.

    Then a scene agent and a verifier per scene did S01–S15. The verifiers fixed a FadeOut glitch in
    S02 (the laptops' images vanished early) and moved S10's namespace flash 0.7 s later, onto
    "namespace".
  - **S16:** a container restart cut that run before S16, and a separate run (`wy9fj1vih.output`)
    finished it: the slide-29 tag and the pause-caption flash. Its verifier put the `^C` row back
    on time.
  - **Review-bot findings:** a last run (`w5vfyl23g.output`) checked two on fresh frames, and neither
    reproduces. S02's slide tag stays 0.22 units from the README card. S03's flashed glyphs leave
    nothing behind after `FadeOut(card9)`.
- **QA_FOLLOWUPS.md:** the S11 underlines, the S16 bracket, S15's `swap_panel` and the `col_box`
  positions were checked and closed (fixed, or do not reproduce). Two items were left "open for
  the final review":
  - the S03 skip chip against the 1080p chapters: it now matches (Verified);
  - the S02 box crossing the "Docker Hub · images" caption mid-move: still open (Open, item 2).

## Final-cut checks (1080p60, 2026-10-18)

Five agent checks were to review the stitched deliverables. No human watched or listened.

| check | report | status for this record |
|---|---|---|
| lecture-slide tags and review-bot items | `report-tags.md` missing | produced nothing; working files in `tags/` |
| ASR round trip (the substitute for a listen) | `report-asr.md` missing | produced nothing; working files `asr.json`, `asr-base.log`, `align*.json`, `onsets*.json`, `clips/`, `clips_large-v3-turbo.json` |
| visual pass over the burned-in copy | `report-visual.md` missing | produced nothing; frames every 3 s, contact sheets, motion and scene-end scans, running notes `visual/notes.md` |
| bilingual pairing | `report-pairs.md` missing | produced nothing; working files in `pairs/` |
| measurements | `report-measured.md` missing | `measured.json` (13:41:29 UTC) and its logs in `measured/` exist; its numbers are under "Verified" |

**ASR round trip: no result for this cut.**

- **What the working files show:** `base.en` transcribed the final audio and was compared with the
  531 cues of the `.srt`. Its log ends "531 cues, 231 with differences, 4505 words recognised", and
  43 clips were cut and re-transcribed with `large-v3-turbo`.
- **What is missing:** no triage of those differences exists. This record therefore makes no claim
  about mispronunciations, swallowed words or late cues in the final audio.
- **The draft's ASR pass doesn't cover it.** On the 480p draft, base.en and large-v3-turbo found no
  missing or wrong word. But S03, S04, S09, S10, S13, S15 and S16 were re-voiced after it, so it
  does not cover the final narration.

**Lecture-slide tags.**

- **In the scene code:** 18 `lecture_ref(4, …)` tags, the 18 tag items that SLIDES.md §5 marks "do":
  - S01: slides 42–43;
  - S02: 37–40;
  - S06: 23–24, then 26;
  - S08: 7, and 37–38;
  - S09: 13, and 8, 15;
  - S10: 33, then 34;
  - S11: 12, and 35;
  - S13: 35, and 33–34;
  - S14: 26;
  - S15: 17–20, then 27;
  - S16: 29.
- **Checked:** each tag's finishing-pass verifier checked it on 720p previews.
- **Not checked:** on the final cut, the tags check produced no report.

**Visual pass and bilingual pairing:** no report, so nothing from them is claimed. Leads from their
working files are under "Open", item 2.

## Open (for the coordinator)

1. **The final-cut checks.** The tags, ASR, visual and pairing checks need to be re-run or finished,
   with their reports written. Until then the ASR round trip that gate 6's waiver line names as the
   substitute has not reached a verdict on this cut.
2. **Leads from the checks' working files.** These are not verdicts; each needs a check.
   - **Visual running notes:**
     - 09:21–09:31: S06's two-line pill "the folder you're in" grazes code lines 7 and 9 by about
       2–4 px;
     - 07:36.0: a role badge flies out from behind the console card for about 0.3 s;
     - 13:15.0: the yellow `cli.py` and `/app/cli.py` chips cross the container terminal's border
       for about 0.6 s;
     - 19:03–19:12: the yellow "9100" labels touch the `localhost` loops' arrowheads;
     - 20:42: S11's tag "same line · different files copied → rebuilt" is marked "CHECK full frame",
       and the notes never resolve it.
   - **Motion scan** (`visual/motion/freezes_th30_4.0.json`): 24:33.25–24:38.50 in S13 is 5.25 s
     with at most 30 changed pixels, outside any ponder timer. The notes record only a 0.5 s dot
     appearing at 24:36 in that stretch.
   - **Tags scan** (`tags/box_cross.json`): S02's box flying to the shelf crosses the
     "Docker Hub · images" caption at 02:23.20–02:23.37. This is QA_FOLLOWUPS.md's open item.
   - **ASR:** 231 of 531 cues differ in base.en, untriaged.
3. **Gate 3, for Conny:** five ponders against about 16, a recap made of questions, and no recap of
   its own for part 1.
4. **Left as built, with the reasons.** These were found by verifiers and the finishing pass, not
   raised by QA. Times are from their 720p renders, converted to the full video.
   - **S16 beat 2, about 30:28–30:32:** `up -d` is typed about 2 s after "and run up dash d", and
     the gateway re-forms about 1.5 s after "Compose recreates only the gateway". The extra
     `git diff` and the pencil take longer than the gap; fixing it means shortening or dropping that
     extra.
   - **S09, about 18:03:** the "after the fix" flash fills the whole fix card with yellow for about
     0.3 s, which makes its text hard to read. An outline-only flash would change the scene's look.
   - **S16, about 32:08.6–32:09.5, the final fade:** the dashed L05 teaser frame shows through the
     "L05 · llm-rag" tag, which looks struck through until the fade ends.
   - **S06 beat 7, about 10:31–10:44:** four visual groups are on screen, one over the "about 3"
     rule. The extra one is the chmod/winpty hint, which must stay up for a viewer who pauses.
   - **S10** still calls `d190c71` "the pinned commit", where S03 now says "the commit we recorded".
   - **Optional:**
     - a RED tag on the stale box in the S01 teaser;
     - the study guide (MLOps_Learning, `guides/L04-containers-2b-flexible-workflow-ports.md`
       line 353) lists only `--format '{{.Created}}'`, not the full inspect command S08 types.
5. **Toolkit items** (for a separate toolkit PR, never the episode PR):
   - `Terminal._make_room`'s scroll travel;
   - the English `.srt` break in "Tutorial / 0" (01:00.7);
   - cue timing by shown characters;
   - `line_bar`'s height;
   - the zh-en merge of "一个小疏漏";
   - `Terminal.fold` adding ` \` inside quotes;
   - `caption_extra`'s 0.3 s letter scramble while the tracker caption changes;
   - `common.second_terminal()` switching the prompt without typing the `cd`. S06 and S08 use it;
     this is the S15 must's pattern, which QA did not flag there;
   - `explainer/build.py`'s chapter rounding (item 6).
6. **Chapter S09 reads 16:44, but S09 starts at 16:45.000** (frame 60,300).
   - **Cause:** `chapters.txt` and `chapters_part1.txt` truncate 1004.999999 s, the sum of the eight
     scene encodes before S09.
   - **Effect:** a jump to 16:44 lands in S08's last second, its fade to an empty frame
     (`measured/frames/chapter_S09_t1004.0.png`, `chapter_S09_t1005.1.png`). This is harmless, and
     the README copies `chapters.txt` as it is.
7. **Subtitle points:**
   - **zh-en #463** (26:38.7; part 2 #136 at 07:58.6) has English on both rows, "Empty reply from
     server". Terminal text stays verbatim (glossary A1), so this is by design.
   - **Repeated English rows:** zh-en repeats one English sentence under two or three Chinese cues at
     01:00.7 (#18–20), 27:44.4 (#480–481) and 29:02.8 (#502–503). Per cue the English row then runs
     24.8–52.2 characters/s, but 13.6–15.6 over each run.
   - **#287** (16:28.5) shows 49 English characters for 2.43 s, 20.1 characters/s.
8. **Documents:**
   - The narration is 77 words over BRIEF.md's range, and script.md's header still states 4,297
     words.
   - BRIEF.md's ponder table, row 1, still names Cloud Speech Client and transcribe. script.md, the
     scene and the frame (`measured/frames/ponder1_S05_t530.4.png`) ask about the Agent Platform
     User role and generate text.
   - script.md's SHOW lines name the slide tags only in S13; the 16 others exist only in the scene
     code.
   - `scenes/s03_code.py:19`'s docstring still says "skip to 5:09". This is a comment only.
9. **Publishing prerequisites, outside the cut:**
   - **`video.yaml` has no `publish:` block** (`title_zh`, `description_zh`, `tags_zh`,
     `tid: 231`), and the release workflow refuses to start without one.
   - **Review-bot thread tn9i7** on PR #29 (S03 `SKIP_TO`) can be answered from "Verified": the chip
     reads 5:10, and S04 starts at 05:10.55. Thread states on PR #29 were not checked for this
     record.
   - **`output/` still holds four 480p15 draft MP4s** from 2026-10-17. They are not deliverables.

## Verified (final render)

Measured on the current files in `output/` (the stitch finished at 12:51 UTC). The source is
`measured.json`, finished 2026-10-18 13:41:29 UTC, with its logs in `measured/`. The decodes ran
one at a time, 13:30–13:41 (`measured/heavy_progress.log`).

- **Deliverables:** all four MP4s decode in full (`ffmpeg -v error … -f null -`) with exit code 0
  and no error lines. All are H.264 High, yuv420p, 1920×1080, 60 fps constant, with AAC-LC audio at
  48 kHz stereo. The video is x264 at crf 27. The zh-en copy is a second crf-27 encode, with the
  picture scaled to 1670×938 and the subtitles burned in below it.

  | file | size | duration | frames | video / audio kbps | integrated | LRA | true peak |
  |---|---|---|---|---|---|---|---|
  | `ac215-l04-flexible-workflow-ports.mp4` | 126.2 MB | 1929.832 s (32:09.8) | 115,784 | 334.3 / 177.1 | −16.1 LUFS | 2.4 LU | −2.8 dBTP |
  | `ac215-l04-flexible-workflow-ports.zh-en.mp4` (to Bilibili) | 121.9 MB | 1929.832 s | 115,785 | 316.8 / 177.1 | −16.1 LUFS | 2.4 LU | −2.8 dBTP |
  | `ac215-l04-flexible-workflow-ports_part1.mp4` | 71.7 MB | 1120.201 s (18:40.2) | 67,207 | 323.8 / 176.9 | −16.1 LUFS | 2.4 LU | −2.8 dBTP |
  | `ac215-l04-flexible-workflow-ports_part2.mp4` | 54.4 MB | 809.650 s (13:29.7) | 48,577 | 348.9 / 177.4 | −16.1 LUFS | 2.3 LU | −2.8 dBTP |

  - **Loudness and true peak** are ebur128's summary readings; its log labels the true peak "dBFS".
  - **Runtime:** inside the series' 25–35 min.
  - **Parts:** they add up to 1929.851 s, 0.019 s more than the full cut. The 16 scene encodes add
    up to 115,784 frames, and so do the parts' frames.
  - **Start times:** the clean cut and the parts start their video at 0.021 s and their audio at
    0.000 s. The zh-en copy starts both at 0.000 s and has one frame more.
  - **Audio:** the clean and zh-en audio streams are identical (stream MD5
    `889bb8f49d9e743c53b7aa402099abe8`).
- **True peak:** −2.8 dBTP in every file, so the build's −1.5 dBTP target is met with 1.3 dB to
  spare. No per-window peak scan was run for this cut.
- **Subtitles:**
  - **Cue counts:** `.srt` has 531 cues, `.zh.srt` 463 and `.zh-en.srt` 554. The `.zh-en.ass` has
    554 events with the same text as the `.zh-en.srt` (0 mismatches).
  - **Order and bounds:** in all files the cues are numbered in sequence, ordered, not overlapping,
    not empty and inside the runtime, with at most 2 lines.
  - **Shortest cues:** 1.000 s in `.srt`, 1.081 s in `.zh.srt` and 1.129 s in `.zh-en.srt`, so none
    is under 0.8 s.
  - **End and gaps:** the last cue ends at 32:07.5, 2.3 s before the end. The longest gap between
    cues (8.8 s) is the S05 ponder timer.
  - **Both languages:** `measured.json`'s language check flags one zh-en cue only, #463 (Open,
    item 7).
  - **English reading speed:** at most 18.9 characters/s in `.srt` (median 14.6), none over 20.
  - **Parts:** the part files hold 313 + 218, 272 + 191 and 327 + 227 cues, with the same text and
    timing as the full files (0 mismatches; part 2 is offset by 1120.117 s).
- **Burned-in layout (zh-en):** 3,860 sampled frames covered all 554 cues. The picture ends at row
  938. Subtitle ink stays in rows 991–1062 and columns 452–1467, in at most two rows, with none
  clipped or outside the margins. The widest cues are #317 (18:01.8, "Prod is optional…") and
  #244 (13:43.0).
- **Chapters:**
  - `chapters.txt` has 16 lines for 16 scenes. The titles match `video.yaml` in order, and every
    start matches the summed scene durations as printed; `chapters_part1.txt` (9 lines) and
    `chapters_part2.txt` (7 lines) too.
  - The parts cover every scene once.
  - The exception to frame-exact starts is S09 (Open, item 6).
  - The README's chapter list is copied from these files.
- **S03's skip chip** reads "cloned fresh? skip to 5:10" (`measured/frames/skipchip_S03_t199.5.png`,
  03:19.5). S04 starts at 310.55 s (05:10.55, chapter 05:10), so the chip's time lands 0.55 s
  before S04 starts, as its rule requires (never after).
- **Narration:**
  - The 156 SAY lines (4,377 words) are spoken in order, and each scene's voice blocks equal its SAY
    lines. Part 1 has 2,581 words and part 2 1,796.
  - Every scene's `voice.json` records Kokoro `af_heart` at speed 0.9, and every scene's
    `events.json` duration equals its stitched length.
- **QA fixes in the final subtitles** (read from `output/*.srt` for this record):
  - 02:58.7 "…at the commit we recorded,"
  - 03:06.4 "…which this branch commits."
  - 04:31.1 the copy-out warning, before "Pause and switch." at 04:41.5
  - 06:44.3 "Bucket names are global: pick a unique one."
  - 18:01.8 "Prod is optional: after the fix, run it only if your team publishes."
  - 19:06.2 "The lecture calls this a network namespace:"
  - 24:55.9 "from toynet's own address range, its subnet."
  - 27:44.4 "Step 4: Docker Compose, which builds and starts the whole app from one YAML file."
  - 30:22.1 "Next, the README says to repeat the port experiments in the file."
  - 31:14.3 "To test yourself, pause after each question."
- **Provenance** (ASSETS.md):
  - **Real captures:** every terminal panel prints from sessions captured 2026-10-14, 00:29–00:40
    UTC. A fresh Docker Engine 29.8.2 "laptop" (a `docker:29.8.2-dind` container standing in for
    Docker Desktop; Linux bash, user `student`, workspace `~/AC215`) ran:
    - port_toy's whole README;
    - every `docker-shell.sh` mode that runs without Google, for all five components, and the
      registry fallback;
    - a lecture 3 clone switched to `flexible-workflow`;
    - the README's `gcloud` commands, on a Cloud SDK with no account.

    The capture-only parts (proxy relay, registry mirror, base images rebuilt with the proxy CA) are
    never shown.
  - **Source quotes:** every code panel quotes `assets/source/` at the pinned commits, copied with
    `git show` and checked against the blob hashes.
  - **Recorded without a key:** the real failing Google calls (`DefaultCredentialsError` and the
    others) carry that tag.
  - **Expected:** C's, D's and E's `--help` panels with a key come from their READMEs and are tagged
    `expected`.
  - **Illustrations** (tagged `illustration`): the GCP console (service account, roles, key, APIs),
    the bucket and its prefixes, Docker Hub, and the port_toy page in a browser. The page is filled
    from the captured JSON; `curl` stood in for its Send button.
  - **Stand-in:** the old lecture 3 key in the branch-switch demo is a 79-byte stand-in, tagged as
    such and never shown.

## Not claimed

- **No human has listened to or watched this cut.** The listening sign-off is waived for the series
  (gate 6).
- **The ASR round trip of this cut has no result.** base.en ran and 43 clips were cut for
  large-v3-turbo, but nobody triaged the differences and no report exists. So the substitute that
  gate 6 names is not in place for this cut. The draft's ASR pass predates the re-voicing of seven
  scenes.
- **No final-cut visual review, tags check or pairing check reached a report.** The frames read for
  this record (one visual-pass frame at 28:51.0 and the measuring check's frames named above) are
  spot checks, not a review.
- **The QA and finishing fixes were verified on 480p/720p previews** of the scene files, not one by
  one on the 1080p cut.
- **The Chinese and bilingual subtitles were reviewed by agents only:** the QA subtitle watcher on
  the draft, the fixers' and verifiers' simulations, and `explainer.i18n check`. No native-speaker
  human has read them, and the pairing check of the final files produced no report.
- **Chinese reading speed is not compared with the series rule.** `measured.json` reports at most
  15.3 characters/s in `.zh.srt` (median 7.6), with 126 cues above 9/s. It does not record how it
  counts, so this is not compared with the series' 9 units/s rule. On the draft, the subtitle
  watcher found that rule met with the i18n tool's units.
- **Nothing that needs a Google account or key was run:**
  - the service account, its four roles and its JSON key;
  - enabling the APIs, in the console or with `gcloud services enable`;
  - the bucket and the `input-*.mp3` upload;
  - every Quick Reference command doing its job (`--download`, `--transcribe`, `--generate`,
    `--synthesis`, `--translate`, `--upload`).

  The "with your key, look for" cards describe what `cli.py` prints, from reading the code. The
  console pictures are illustrations drawn from README.md:169–203.
- **Other steps not run:**
  - `docker login` and `./docker-shell.sh prod`: there is no Docker Hub account, and pushing would
    publish an image;
  - the ElevenLabs bonus (no key);
  - `git checkout -- .`;
  - `uv add <package>` (a placeholder);
  - the Windows and macOS paths (Git BASH, `winpty`, Docker Desktop's UI): the captures ran on
    Linux only;
  - the browser: the page is drawn.
- **Review-bot threads on PR #29 were not inspected for this record.**
- **The released files will be a different render.** The release workflow re-renders every scene
  with the pinned engine and writes its own `<id>.validation.json`. The released files should be
  re-checked against the numbers here, at least for duration, frames, loudness, true peak and cue
  counts.
